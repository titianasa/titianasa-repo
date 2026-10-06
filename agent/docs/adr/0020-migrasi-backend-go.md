# ADR-0020: Migrasi backend — Rust/Axum/sqlx → Go (modular monolith)

Status: **Accepted** (2026-10-05, keputusan langsung user). Pelaksanaan: `tickets/phase-51-go-migration.md`.
Date: 2026-10-05
Supersedes: ADR-0009 (runtime Bun/Elysia, yang sudah dibatalkan de facto oleh Phase 30) dan baris "backend Rust" di semua dokumen hidup
Superseded by: -
Related: ADR-0001…0008 (model data, mastery, FRSS, AI gateway, ekonomi, RBAC — **tidak dibuka ulang**), ADR-0013 §3.1 (antrean job di Postgres), ADR-0016/0017 (hub realtime & suara Pare)

## Context

`titian-backend-rust` adalah backend aktif untuk `titian-web` dan `alr/game` (Kampung Bahasa Pare). Ukurannya saat keputusan ini dibuat (dihitung dari kode, 2026-10-05):

| Hal | Jumlah |
|---|---|
| Kode `src/` | ±70.000 baris Rust (163 berkas service, 55 handler) |
| Route HTTP | 381 (24 berkas route) |
| Query SQL | ±1.150 (723 `query!` terperiksa compile-time + 431 dinamis) |
| Migrasi | 96 berkas (`0000`–`0096`) |
| WebSocket | 3 (`/ws/pare`, kanvas pesan, kolaborasi Yjs) + 1 SSE (Live AI Chat) |
| Proses | 2 (`titian-backend-rust` API, `titian-worker`) + 13 binary alat sekali-jalan |
| Job terjadwal | 6 handler (`metrics_rollup`, `content_factory`, `group_league`, `league_circuit`, `pare_push`, `pare_voice`) |
| Test | 229 unit + 55 berkas integrasi (±20.000 baris) |

User memutuskan pindah penuh ke Go. Alasannya: beban aplikasi dominan I/O dan logika bisnis, sehingga kecepatan pengembangan lebih bernilai daripada efisiensi memori Rust; waktu build Rust dan pemakaian disk (`target/` pernah memenuhi SSD sampai Postgres mati, lihat STATE) menghambat kerja harian.

ADR ini **hanya** mengganti bahasa dan pustaka. Kontrak API, skema database, rumus, dan aturan bisnis tidak berubah.

## Keputusan

### 1. Bentuk: modular monolith Go, satu repo `titian-backend-go`

Satu binary API + satu binary worker, satu modul Go. Tiap domain adalah paket sendiri di `internal/` dengan batas impor yang jelas, sehingga bagian yang ramai (hub realtime Pare) bisa dipisah jadi service kelak tanpa menulis ulang.

```
titian-backend-go/
  cmd/api/            # server HTTP + WebSocket (port 8090)
  cmd/worker/         # konsumen antrean job
  cmd/tools/<nama>/   # alat sekali-jalan (pengganti src/bin/*)
  internal/
    platform/         # config, db, migrate, redisx, httpx, auth, rbac, jobs, storage, ai, obs
    identity/ org/ catalog/ module/ quiz/ learning/ gamification/ economy/
    marketplace/ attendance/ drive/ messaging/ proctoring/ admin/
    contentfactory/ studygroup/ pare/
  db/migrations/      # 96 berkas SQL, disalin apa adanya
  db/queries/         # SQL untuk sqlc, satu berkas per domain
  data/pare/          # content.json, missions.json, langrule_cases.json (go:embed)
```

Tiap paket domain berisi `routes.go` (daftar route), `handler.go` (HTTP ↔ DTO), `service.go` (aturan bisnis), dan query sqlc-nya. Padanan dengan Rust: `routes/x.rs` → `internal/x/routes.go`, `handlers/x.rs` → `handler.go`, `services/x.rs` → `service.go` atau berkas bernama sama.

### 2. Pustaka

| Kebutuhan | Rust sekarang | Go |
|---|---|---|
| Router, middleware | axum, tower-http | `go-chi/chi/v5`, `go-chi/cors` |
| Postgres | sqlx | `jackc/pgx/v5` + `pgxpool`; query statis lewat `sqlc`, query dinamis lewat pgx langsung |
| Redis | redis-rs | `redis/go-redis/v9` |
| JWT | jsonwebtoken | `golang-jwt/jwt/v5` (HS256 token akses, RS256 JWKS Google, HS256 token LiveKit) |
| WebSocket | axum `ws` | `coder/websocket` |
| Kompresi | tower-http gzip + brotli | middleware kompresi chi + `andybalholm/brotli` |
| Object storage R2 | aws-sdk-s3 | `aws-sdk-go-v2` (S3 + presign) |
| Vertex AI | gcp_auth + reqwest | `golang.org/x/oauth2/google` (ADC) + `net/http` |
| OpenRouter (teks, OCR, STT, TTS) | reqwest | `net/http` |
| Web Push (RFC 8291 + VAPID) | ring, tulis sendiri | `SherClockHolmes/webpush-go` |
| Label perangkat dari User-Agent | woothee | `woothee/woothee-go` (aturan sama, label sama) |
| Teks dari PDF / DOCX | pdf-extract, zip + quick-xml | `ledongthuc/pdf`, `archive/zip` + `encoding/xml` |
| Normalisasi Unicode, regex | unicode-normalization, regex | `golang.org/x/text/unicode/norm`, `regexp` (sama-sama RE2, tanpa lookaround) |
| Log | tracing | `log/slog` (JSON di produksi) |
| Kolaborasi Yjs | yrs + yrs-axum | lihat §6 |

### 3. Yang sengaja **tidak** diambil dari saran arsitektur umum

Saran awal menyebut Redis untuk leaderboard/streak/XP dan NATS/Redis Streams/`asynq` untuk antrean. Keduanya **ditunda sampai setelah cutover**, karena mengganti tempat penyimpanan di tengah port membuat paritas tidak bisa dibuktikan:

- **Antrean tetap tabel `jobs` di Postgres** (`FOR UPDATE SKIP LOCKED`, ADR-0013 §3.1). Job yang sedang menunggu, jadwal, dan riwayatnya ikut pindah tanpa konversi. Worker Go memakai tabel yang sama, jadi worker Rust dan Go bisa bergantian selama transisi.
- **XP, streak, liga, leaderboard tetap di Postgres** sebagai sumber kebenaran. Redis tetap dipakai persis seperti sekarang: pembatas laju, kunci & status ruang suara Pare, dan cek kesehatan. Leaderboard `ZSET` Redis dicatat sebagai optimasi pasca-cutover (tiket G16), bukan bagian port.
- **Event progres** (`learning_events`, terpartisi bulanan) sudah ada sejak Phase 39 dan dipertahankan apa adanya.
- **Microservice**: tidak. Satu aplikasi dulu.

### 4. Kontrak yang harus identik (daftar jebakan paritas)

Klien (`titian-web`, `alr/game`) tidak diubah. Perbedaan perilaku bawaan Go vs Rust berikut wajib ditangani di `internal/platform/httpx` sekali, bukan per handler:

| Hal | Rust sekarang | Yang dilakukan di Go |
|---|---|---|
| Bentuk galat | `{"error": "kode", "detail": …}` dengan 4 pengecualian (`attempt_already_in_progress`, `missing_required_answers`, `insufficient_credit`, `duplicate_value` dari SQLSTATE 23505) | `httpx.Error` dengan tabel yang sama; 23505 dibaca dari `pgconn.PgError` |
| Body JSON tak valid | 422 `invalid_json_body` (field wajib hilang atau tipe salah ditolak serde) | `encoding/json` **diam-diam mengisi nol** untuk field yang hilang. `httpx.DecodeJSON` wajib memeriksa field wajib (tag `validate:"required"`) dan membalas 422 yang sama |
| Route tak cocok | path tak dikenal: 404 `{"error":"not_found","detail":null}`; method salah: 405 tanpa body; parameter path/query rusak: 400 teks polos | 404 sama. 405 dan 400 mempertahankan status, body-nya kini memakai amplop galat (`method_not_allowed`, `invalid_path_parameter`, `invalid_query_parameter`) |
| Array kosong | `[]` | slice `nil` menjadi `null` di Go. Semua slice respons diinisialisasi; dicek oleh alat banding (§7) |
| Waktu | RFC 3339 UTC berakhiran `Z` | pgx mengembalikan zona lokal. `time.Local = time.UTC` di `main`, tanggal murni memakai tipe `Date` yang menulis `YYYY-MM-DD`. Pecahan detik: chrono menulis 3/6/9 digit, Go memangkas nol di belakang — instan yang sama, diterima |
| Angka pecahan | `1.0`, `50.0` | Go menulis `1`, `50`. Diterima: klien sudah lolos uji dengan bentuk ini saat regresi Bun-vs-Rust (Phase 30) |
| Escape HTML | tidak | `SetEscapeHTML(false)` |
| Batas ukuran body | 2 MB bawaan, 6 MB avatar, `ASSET_MAX_BYTES` untuk aset | `http.MaxBytesReader` dengan angka yang sama, 413 `payload_too_large` |
| CORS | daftar asal dari `FRONTEND_ORIGIN`, header `content-type`, `authorization`, `x-organization-id` | sama |
| Auth | Bearer JWT; org aktif dari `X-Organization-Id` atau peran paling awal; sentuhan presence di latar | sama; goroutine untuk presence |
| WebSocket | token di query `?token=`, kode tutup 1008/1011 dengan alasan teks | sama |
| SSE Live AI Chat | keep-alive, tanpa buffer | kompresi dilewati untuk `text/event-stream`, `Flush` tiap event |
| Nama variabel lingkungan, port 8090, nama tabel `_sqlx_migrations` | — | **tidak berubah**, supaya `.env` dev dan produksi dipakai apa adanya |

Migrasi: runner Go membaca dan menulis `_sqlx_migrations` dengan bentuk baris yang sama (versi, deskripsi, checksum SHA-384) dan aturan toleransi yang sama ("objek sudah ada" dicatat sebagai sudah diterapkan). Dengan begitu kedua backend bisa menyala bergantian di database yang sama selama transisi.

### 5. Kinerja setara

Go memakai lebih banyak memori (GC) dan JSON bawaannya lebih lambat dari serde. Untuk alur yang didominasi database, latensinya realistis setara; untuk alur berat-CPU tidak dijamin tanpa diukur. Karena itu "setara" dijadikan **gerbang ukur**, bukan asumsi:

- **Gerbang cutover (G15):** uji beban yang sama ke Rust `:8090` dan Go `:8091` di mesin dan database yang sama. Lulus bila p95 Go ≤ 1,15 × p95 Rust untuk 20 endpoint terpanas, dan fan-out `/ws/pare` (`game/scripts/loadtest.ts`) tidak kehilangan pesan pada jumlah pemain yang sama.
- **Bawaan yang dipasang sejak G0:** `pgxpool` dengan cache prepared statement dan protokol biner; ukuran pool dari `DB_MAX_CONNS` (bawaan 10, sama dengan sekarang); `GOMEMLIMIT` disetel di compose; kompresi gzip + brotli; `content.json` Pare (4,9 MB) dilayani sebagai byte yang sudah jadi dan sudah terkompresi, bukan di-encode ulang per permintaan.
- **Cadangan bila gerbang gagal di satu endpoint:** ganti encoder JSON endpoint itu (`encoding/json/v2` atau `goccy/go-json`), cache respons kurikulum yang besar, atau perbaiki query. Bukan kembali ke Rust.
- **Alur berat-CPU yang diberi benchmark tersendiri:** pencocokan jawaban (`answer_match`), aturan bahasa chat Pare (`pare_langrule`, 370 baris + berkas kasus uji), penyusun kertas soal, ekstraksi PDF.

### 6. Kolaborasi Yjs (`/ws/module-items/{id}/collab`) — satu-satunya bagian tanpa padanan Go yang matang

Server sekarang memakai `yrs` (CRDT Yjs versi Rust) untuk: menggabungkan update, menjawab sinkronisasi awal, menyiarkan awareness, dan menyimpan checkpoint ke `module_items.yjs_state` tiap 15 detik. Tidak ada pustaka CRDT Yjs untuk Go yang setara kematangannya.

Urutan pilihan, diputuskan di tiket G12 setelah diuji:

1. **Go penuh dengan port Yjs komunitas** (`skyterra/y-crdt`), bila lolos uji kompatibilitas: dokumen yang disimpan `yrs` terbaca, hasil gabungan terbaca klien Yjs, dan dua klien browser konvergen.
2. **Sidecar Rust kecil `titian-collab`** (±250 baris: `collab_hub.rs` + `collab_ws.rs` yang sudah ada), bila pilihan 1 gagal uji. Go tetap memegang auth dan izin; Caddy mengarahkan satu path WebSocket ke sidecar. Ini satu-satunya Rust yang tersisa.

Pilihan 2 berarti migrasi tidak 100% Go. Itu dicatat terbuka di sini supaya tidak jadi kejutan.

### 7. Cara membuktikan paritas

- **Alat banding (`cmd/tools/paritydiff`)**: memutar daftar permintaan yang sama ke Rust dan Go dengan token yang sama di database dev yang sama, lalu membandingkan status dan JSON (mengabaikan beda `1.0` vs `1`). Cara ini yang menemukan 5 bug kontrak saat Bun→Rust; test suite tidak menemukannya.
- **Test integrasi diport per domain** bersama kodenya. Tiap test memakai database baru hasil `CREATE DATABASE … TEMPLATE` dari templat yang sudah dimigrasi (padanan `#[sqlx::test]`). 26–27 test Rust yang sudah lama gagal karena tertinggal dari kode **tidak** diport apa adanya; diganti test terhadap perilaku sekarang.
- **Unit test rumus** (mastery, FRSS, skor kuis, langrule, backoff) diport dengan angka contoh yang sama.

### 8. Transisi

- Rust tetap backend aktif di `:8090` sampai G15. Go berjalan di `:8091` selama pengerjaan.
- Selama transisi, endpoint atau migrasi baru yang masuk ke Rust (mis. sisa Pare-9) **wajib** ditambahkan ke daftar paritas di tiket fase 51. Migrasi SQL baru ditulis sekali dan disalin ke kedua repo.
- Cutover: tukar image di `docker-compose.prod.yml`, nama service dan port tetap. Rollback: kembalikan tag image Rust; skema database tidak berubah sehingga rollback tidak butuh migrasi balik.
- Setelah 2 minggu stabil: `titian-backend-rust` diarsipkan (tar ke `/home/john/backups/` + commit dulu, baru dihapus dari workspace aktif), sama seperti Bun.

## Konsekuensi

- (+) Build detik, bukan menit; image runtime kecil (binary statis); tidak ada lagi `target/` puluhan GB.
- (+) Satu bahasa backend; goroutine cocok untuk hub WebSocket dan worker.
- (−) Kehilangan pemeriksaan SQL saat compile dari `sqlx::query!`. Diganti `sqlc` untuk query statis; ±430 query dinamis hanya terlindungi test.
- (−) Kehilangan jaminan tipe Rust (`Option`, enum lengkap). Field wajib dan slice kosong harus dijaga lewat `httpx` dan alat banding.
- (−) Pekerjaan besar: ±70.000 baris dan 55 berkas test ditulis ulang, sementara fitur baru (Pare-9, Phase 46–50) tertahan atau harus dikerjakan dobel.
- (−) Kolaborasi Yjs mungkin tetap butuh sidecar Rust (§6).

## Alternatif yang ditolak

- **Tetap Rust**: ditolak user.
- **Go untuk fitur baru saja, Rust dibiarkan** (strangler permanen): dua bahasa selamanya, beban tim bertambah.
- **Sekalian pindah ke microservice / Redis sebagai sumber data / asynq**: menumpuk dua perubahan besar; lihat §3.
