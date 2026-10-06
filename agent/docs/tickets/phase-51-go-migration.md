> **2026-10-07:** direktori `titian-backend-rust` dihapus seluruhnya (atas permintaan; repo jarak jauh `titianasa-be-rust` tetap ada di GitHub). Semua rujukan ke jalurnya di dokumen lain bersifat sejarah; kode aktif ada di `titian-backend-go`.

# Phase 51 — Migrasi backend ke Go

Keputusan: [ADR-0020](../adr/0020-migrasi-backend-go.md). Repo baru: `alr/titian-backend-go`. Sumber port: `alr/titian-backend-rust` (tetap backend aktif di `:8090` sampai G15; Go berjalan di `:8091` selama pengerjaan).

## Aturan umum (berlaku untuk semua tiket G)

1. **Port 1:1, kecuali bug.** Tidak ada perubahan kontrak API, skema, rumus, atau aturan bisnis. **Bug yang ditemukan di Rust diperbaiki di Go saat itu juga** (keputusan pengguna 2026-10-05), diberi test, dan dicatat di bagian "Bug Rust yang diperbaiki di Go" supaya selisih `paritydiff`-nya bisa dijelaskan. Perbaikan yang butuh migrasi baru dihindari selama Rust masih berbagi database dev. Optimasi dan perubahan desain tetap dicatat di "Pasca-cutover", tidak dikerjakan di tengah port.
2. **Satu tiket = satu berkas route Rust** (atau sekelompok kecil). Selesai bila: semua route di berkas itu ada di Go, test integrasinya diport dan hijau, dan `paritydiff` terhadap Rust bersih untuk route GET-nya.
3. **Query**: `sqlx::query!` statis → `db/queries/<domain>.sql` (sqlc). Query dinamis (`sqlx::query(...)` dengan SQL yang dirangkai) → pgx langsung di service, SQL disalin apa adanya.
4. **Jebakan paritas** di ADR-0020 §4 ditangani lewat `internal/platform/httpx`, bukan diulang per handler. Slice respons selalu diinisialisasi (`[]`, bukan `null`).
5. **Komentar "kenapa"** di kode Rust (banyak yang mencatat keputusan produk) ikut dipindahkan, diringkas.
6. **Migrasi SQL baru** selama transisi ditulis sekali, disalin ke `titian-backend-rust/migrations/` dan `titian-backend-go/db/migrations/` dengan nama berkas yang sama.
7. Dokumen `api-contract.md` dan `domain-model.md` tidak berubah isinya (kontrak sama); hanya rujukan berkas sumber yang diperbarui saat tiketnya selesai.
8. Jangan commit tanpa diminta. Jangan menyentuh database produksi.

## Peta padanan berkas

| Rust | Go |
|---|---|
| `src/main.rs`, `src/bin/titian-worker.rs` | `cmd/api/main.go`, `cmd/worker/main.go` |
| `src/bin/<alat>.rs` | `cmd/tools/<alat>/main.go` |
| `src/config.rs`, `state.rs`, `db/`, `errors.rs`, `extract.rs`, `observability/` | `internal/platform/{config,app,db,httpx,obs}` |
| `src/middleware/auth.rs`, `services/{token,permissions,request_meta,rate_limit}.rs` | `internal/platform/{auth,rbac,ratelimit}` |
| `src/services/job_queue.rs` | `internal/platform/jobs` |
| `src/routes/x.rs` + `handlers/x.rs` + `services/x*.rs` | `internal/<domain>/{routes,handler,service}.go` |
| `migrations/*.sql` | `db/migrations/*.sql` (salinan persis) |
| `.sqlx/` (cache query offline) | tidak ada padanan; diganti `sqlc generate` |
| `tests/integration/x_test.rs` | `internal/<domain>/x_test.go` + `internal/platform/testdb` |
| `cargo test --lib` / `cargo test --test integration` | `go test ./...` |

## Daftar tiket

Ukuran: S < 500 baris Rust, M < 1.500, L < 4.000, XL lebih. Jumlah route dihitung dari `src/routes/*.rs` pada 2026-10-05.

| Tiket | Isi | Sumber Rust | Route | Ukuran | Status |
|---|---|---|---|---|---|
| **G0** | Fondasi: kerangka repo, config, galat, JSON, router (CORS, kompresi, 404), pgxpool, runner migrasi, Redis, log, auth + presence, RBAC, token, pembatas laju, kesehatan, antrean job + worker, Dockerfile/compose/deploy, harness test, `paritydiff` | `main.rs`, `state.rs`, `config.rs`, `db/`, `errors.rs`, `extract.rs`, `middleware/`, `job_queue.rs`, `bin/titian-worker.rs` | 1 (`/health`) | M | ✅ selesai 2026-10-05 |
| **G1** | Identitas & organisasi: login Google, refresh/rotasi token, sesi, profil, avatar, organisasi & anggota, persetujuan data, profil belajar | `auth`, `google_oauth`, `organization`, `user_data_consent`, `learning_profile` | 18 | M | ✅ selesai 2026-10-05 (1 kait tertunda, lihat catatan) |
| **G2** | Katalog & kelas: registri kanonik (`/catalog` 6 route baca), program, mapel, prasyarat konsep, periode, kelas organisasi + sesi + kehadiran (manual, QR, sinkron Meet), penyedia rapat | `catalog`, `program`, `subject`, `concept`, `period`, `org_class*`, `org_attendance*`, `attendance_qr`, `meeting_provider` | 26 | M | ✅ selesai 2026-10-05 (lihat catatan) |
| **G3** | Modul & konten: pohon modul, item, versi, label, jalur belajar, jalur kanonik (termasuk 10 route `/catalog/learning-paths`, `/catalog/subjects`, `/catalog/sessions` dari `canon_path.rs`), rencana pelajaran, skema blok, parser ALM, guard/progres/proctor item, checkpoint bagian, berbagi, laporan konten, heatmap | `module*`, `learning_path`, `canon_path`, `lesson_plan`, `block_schema`, `alm_parser`, `item_*`, `section_checkpoint`, `resource_share`, `content_report`, `learning_heatmap`, `interactive_block` | 60 | XL | ✅ 2026-10-05 (G3a–G3f, lihat catatan) |
| **G4** | Soal, kuis & penilaian: bank soal, konfigurasi & templat kuis, taksonomi, kertas soal, attempt, penilaian, pencocokan jawaban, fakta jawaban | `question*`, `quiz_*` (tanpa `quiz_generation`), `assessment`, `grading`, `answer_match`, `answer_facts`, `assignment`, `gradebook`, `exam_session`, `evaluation` | 16 | XL | belum |
| **G5** | Mesin belajar & jejak: mastery, FRSS, rescue, antrean ulang, `learning_events` (partisi + retensi saat boot), event klien | `mastery`, `frss`, `rescue`, `learning_queue`, `learning_event`, `client_events`, `module_completion` | 8 | M | ✅ 2026-10-05 (6 dari 8 route; `completion-status` / `skip-completion` selesai di G6) |
| **G6** | Gamifikasi & ekonomi: XP, streak, pencapaian, liga, leaderboard, misi harian, kredit, langganan, pesanan (penyedia bayar stub) | `xp`, `streak`, `achievement`, `league`, `leaderboard`, `daily_mission`, `economy`, `wallet`, `subscription`, `order`, `payment_provider`, `ad` | 13 | M | ✅ 2026-10-05 (13 route + 4 titipan: `completion-status`, `skip-completion`, progres blok interaktif, webhook pembayaran) |
| **G7** | Marketplace & tutor: produk belajar, kohort, enrolmen, sertifikat, tutor, ulasan tutor | `learning_product`, `cohort`, `enrollment`, `certificate`, `tutor*` | 24 | M | ✅ 2026-10-05 (29 route; angka 24 di tabel tidak menghitung enam route tutor/tugas) |
| **G8** | Kehadiran, sesi kelas, Speaking Room, proctoring; penyedia rapat Google Meet | `attendance*`, `class_session`, `meeting_provider`, `speaking_room`, `proctoring*` | 18 | M | ✅ 2026-10-05 untuk kehadiran, sesi kelas, proctoring (16 route); **4 route Speaking Room pindah ke G10** (butuh penyedia AI: giliran, ringkasan, TTS, transkripsi) |
| **G9** | Drive & aset: R2 (unggah, URL bertanda tangan, presigned PUT), folder, izin, aktivitas, ekstraksi teks PDF/DOCX | `storage`, `asset`, `folder`, `drive*`, `resource_activity`, `document_extract`, `paste_normalizer` | 25 | M | ✅ 2026-10-05 untuk Drive & aset (25 route, `internal/drive`); **ekstraksi teks PDF/DOCX pindah ke G10** (hanya dipakai penyusun AI) |
| **G10** | AI: penyedia OpenRouter & Vertex + perutean, pengaturan model per peran, gateway + tagihan kredit, konten AI, OCR, evaluasi menulis/berbicara, rencana pelajaran AI, generator kuis, kode web AI, Live AI Chat (SSE), tutor chat | `ai_*`, `vertex_ai_provider`, `metered_ai`, `lesson_plan_ai`, `quiz_generation`, `code_web_ai`, `live_chat`, `tutor_chat`, `alm_generation`, `content_qa`, `interactive_web_qa`, `curriculum_constitution` | 19 + 4 Speaking Room + ekstraksi dokumen | XL | **✅ 2026-10-05 selesai seluruhnya.** Dipecah: **G10a ✅ 2026-10-05** (lapisan penyedia, pengaturan model, gateway kredit; 2 route), **G10b ✅ 2026-10-05** (konten AI, OCR, evaluasi menulis/berbicara, transkripsi, ekstraksi dokumen; 5 route), G10c rencana pelajaran + generator kuis + kode web (**G10c ✅ 2026-10-05**: G10c-1 rencana pelajaran AI, edit bagian, terjemahan, fragmen ALM, 4 route · G10c-2 generator kuis + kode web AI, 5 route), **G10d ✅ 2026-10-05** Live AI Chat (turn + SSE), tutor chat, Speaking Room, audio prompt (8 route) |
| **G11** | Admin Pusat & Pabrik Konten: log audit, agregat harian (job), peserta, pengaturan AI, pabrik konten (job) | `admin_*`, `metrics_rollup`, `content_factory/*`, `content_context` | 31 | XL | dipecah: **G11a ✅ 2026-10-06** Admin Pusat (19 route: log audit, 6 metrik, peserta, tiket konten, heatmap platform, 6 route Pengaturan AI), **G11b ✅ 2026-10-06** job `metrics_rollup` + alat backfill, **G11c ✅ 2026-10-06** Pabrik Konten (12 route + mesin job `content_generation` untuk `bab_plan` dan `bab_content`), 2 route suara Pare pindah ke G14 |
| **G12** | Pesan & realtime: percakapan, kanvas (WS), kolaborasi Yjs (WS, lihat ADR-0020 §6) | `conversation`, `canvas*`, `collab_hub`, `handlers/collab_ws.rs` | 8 + 2 WS | M | **✅ 2026-10-06** (9 route REST + 2 WS; tanpa sidecar Rust, lihat catatan) |
| **G13** | Grup, liga, Ruang Kelas: grup belajar, konten grup, liga grup (job), sirkuit liga (job), ruang kelas, moderasi | `study_group*`, `group_league`, `league_circuit`, `classroom`, `group_moderation` | 42 | L | **✅ 2026-10-06** (42 route + 2 job: `league_season_close`, `league_circuit_close`) |
| **G14** | Kampung Bahasa Pare: pemain, konten, pelajaran, kertas soal, simulasi hidup, ekonomi, harian, chat + aturan bahasa, hub `/ws/pare`, push (job), voice note & panggilan (LiveKit, Redis, job), premium & boost, jalur, misi, avatar, audio | `pare_*`, `web_push` | 61 + 1 WS | XL | ✅ selesai 2026-10-06 (G14a–f) |
| **G15** | Cutover: semua handler job terdaftar di worker, alat `cmd/tools`, gerbang kinerja, regresi `paritydiff` penuh, tukar image produksi, perbarui skrip ekspor `alr/game` (`missions.ts`, `gen-langrule-cases.ts`) ke `titian-backend-go/data/pare/`, arsip Rust | — | — | M | ✅ produksi ditukar 2026-10-06 (tinggal arsip Rust) |

Urutan: G0 → G1 → G2 → G3 → G4 → G5 → G6, lalu G7–G13 dalam urutan apa pun. G14 hanya bergantung pada G0–G1 dan G6 (pesanan Premium), jadi bisa dikerjakan sejajar. G15 terakhir.

## Yang ditambahkan agar semua fitur tetap jalan dan kinerjanya setara

Hal-hal ini tidak ada di saran arsitektur awal, tetapi dibutuhkan kode yang sekarang:

| # | Tambahan | Kenapa | Tiket |
|---|---|---|---|
| 1 | Runner migrasi yang kompatibel dengan `_sqlx_migrations` | Database dev dan produksi sudah punya riwayat migrasi sqlx; kedua backend harus bisa menyala bergantian | G0 |
| 2 | Antrean job tetap tabel `jobs` Postgres (bukan asynq/NATS) | Job tertunda dan jadwal ikut pindah; ADR-0013 §3.1 | G0 |
| 3 | Proses worker terpisah dengan 3 loop (klaim, penjadwal, pemulih) dan `WORKER_CONCURRENCY` | Sama dengan `titian-worker` | G0, G15 |
| 4 | Pemeriksa field wajib pada body JSON | Go tidak menolak field hilang; Rust menolak dengan 422 | G0 |
| 5 | `time.Local = UTC`, tipe `Date`, slice kosong `[]`, tanpa escape HTML | Bentuk JSON identik | G0 |
| 6 | Kompresi brotli di samping gzip | Respons kurikulum ±440 KB, pengguna data seluler | G0 |
| 7 | Sentuhan presence di latar pada tiap permintaan terautentikasi, label perangkat (woothee), IP dari `X-Forwarded-For` | Halaman Peserta Admin Pusat | G0 |
| 8 | Pembuatan partisi `learning_events` dan `question_answer_facts` + retensi 24 bulan saat boot | Tanpa ini insert gagal di bulan baru | G5 |
| 9 | SSE tanpa buffer untuk Live AI Chat | Kompresi tidak boleh menahan aliran | G10 |
| 10 | Vertex AI lewat ADC, opsional; jatuh ke penyedia "noop" bila kredensial GCP tidak ada | Produksi di Hetzner hanya memakai OpenRouter | G10 |
| 11 | Retry berjeda untuk 429/5xx dan penolakan `finishReason` selain STOP | Perilaku generator konten sekarang | G10 |
| 12 | Ekstraksi teks PDF dan DOCX | Lampiran untuk penyusun AI | G10 |
| 13 | R2: URL GET bertanda tangan, presigned PUT, hapus objek | Drive, avatar, voice note | G9 |
| 14 | Web Push RFC 8291 + VAPID | Notifikasi Pare | G14 |
| 15 | Token & webhook LiveKit (JWT HS256), pemanggilan API LiveKit untuk mengeluarkan pemain | Panggilan suara Pare | G14 |
| 16 | Kunci & status ruang di Redis (`SET NX EX`), pembatas laju Redis | Panggilan suara, login, event klien | G0, G14 |
| 17 | Tiga hub WebSocket di memori (Pare, kanvas, kolaborasi) dengan pembersihan ruang kosong | Realtime | G12, G14 |
| 18 | CRDT Yjs: port Go atau sidecar Rust | ADR-0020 §6 | G12 |
| 19 | `pg_advisory_xact_lock` dan transaksi yang sama untuk kuota grup dan klaim | Mencegah balapan kuota | G13 |
| 20 | Data Pare di-embed ke binary (`go:embed`), `content.json` dilayani sebagai byte jadi | Sama dengan `include_str!`; kinerja | G14 |
| 21 | Gerbang kinerja dan uji beban WS sebelum cutover | "Setara" harus terukur | G15 |
| 22 | `paritydiff` Rust-vs-Go | Menemukan beda kontrak yang tidak tertangkap test | G0, G15 |

## Alat sekali-jalan (`src/bin/*`)

| Alat Rust | Di Go |
|---|---|
| `titian-worker` | `cmd/worker` (G0) |
| `pare_vapid_keys`, `pare_qa_tokens` | diport (G14) |
| `seed_content_factory`, `import_canonical_registry`, `generate_units`, `conform_banks`, `tag_all_banks`, `benchmark_bab_content`, `lean_bab_content`, `lean_benchmark` | diport bersama G11 |
| `backfill_metrics` | diport (G11); dipakai lagi tiap tabel agregat baru |
| `backfill_question_uids`, `backfill_section_gates` | **tidak diport** — sudah dijalankan di dev dan produksi; tetap tersedia di arsip Rust |

## Catatan pengerjaan

### G0 — Fondasi ✅ (2026-10-05)

Yang ada di `titian-backend-go`:

- `internal/platform/config` (semua variabel `config.rs`, nama dan bawaan sama; tambahan `DB_MAX_CONNS`), `httpx` (amplop galat, `DecodeJSON` dengan pemeriksa field wajib, `PathUUID`/`QueryUUID`/`QueryInt`), `db` (pgxpool + runner migrasi kompatibel `_sqlx_migrations`), `auth` (JWT HS256 dengan kelonggaran 60 detik seperti `jsonwebtoken`, resolver org aktif, presence di latar, `RequestMeta` + woothee), `rbac` (matriks ADR-0006), `ratelimit`, `jobs` (antrean + registry), `storage` (R2 + in-memory), `obs` (slog), `app` (router: CORS, gzip + brotli, 404/405, `/health`).
- `cmd/api`, `cmd/worker` (3 loop; registry handler masih kosong sampai domain pemilik job diport), `cmd/tools/paritydiff`.
- Harness test: `internal/platform/testdb` (database per test dari templat) dan `apitest`.
- `sqlc.yaml` + `db/schema.sql` (dump skema dev; `make schema`), `Dockerfile` (image 53 MB; image Rust 261 MB), `docker-compose.prod.yml`, `deploy.sh`, `Makefile`, `go.sh`.

Verifikasi: `go vet` bersih; `go test ./...` hijau; API Go dijalankan di `:8091` terhadap database dev (96 migrasi dikenali sudah diterapkan, tidak ada yang dijalankan ulang) berdampingan dengan image Rust produksi lokal di `:8090`.

Temuan saat membandingkan dengan Rust:

- Method salah pada path yang ada: Rust menjawab **405 tanpa body** (bukan amplop galat, berbeda dari catatan Phase 30). Go menjawab 405 `{"error":"method_not_allowed","detail":null}`.
- Parameter path/query tak valid (UUID rusak, `limit=abc`): Rust menjawab **400 teks polos** dari axum. Go menjawab 400 dengan amplop galat (`invalid_path_parameter` / `invalid_query_parameter`).
- `detail` pada 422 `invalid_json_body`: Go tanpa akhiran "at line X column Y". Kode galatnya sama.
- Pecahan detik timestamp: chrono menulis 3/6/9 digit, Go memangkas nol di belakang. `paritydiff` menormalkan ini.

Belum dikerjakan dari G0: test integrasi `job_queue_test.rs` (9 test, termasuk balapan 4 pekerja) — diport bersama handler job pertama (G11 `metrics_rollup`).

### G3 — Modul & konten 🔨 (mulai 2026-10-05)

Tiket ini dipecah karena `module_item.rs` bergantung pada hampir semua berkas lain di domainnya. Urutan dari bawah ke atas:

| Bagian | Isi | Status |
|---|---|---|
| **G3a** | Pohon modul (10 route: `/modules*`, prasyarat modul, hapus subpohon), pustaka konten murni (`paste_normalizer`, `alm_parser`, `block_schema`, `publish_flow`), progres item (`item_progress`), guard akses & kehadiran (`item_guard`) | ✅ 2026-10-05 |
| **G3b** | Model kuis (`quiz_subtype` 40 subtipe, tipe `quiz_config` + flatten, `ensure_question_uids`, `detect_order_constraints`, `learner_view`, `quiz_config_schema`), `lesson_plan` (parse/normalize/checkpoint/`learner_view`/`to_alm`/`sanitize_generated`), JSON kanonik untuk hash konten | ✅ 2026-10-05 |
| **G3c** | Item modul (15 route: `/modules/{id}/items`, `/module-items/*` detail, buat, ubah, konten, kuis, rencana pelajaran, mapel, urut, hapus, duplikat, ajukan/terbit/tolak, versi, berbagi; `/quiz-subtypes`) | ✅ 2026-10-05 |
| **G3d** | Aturan item (11 route): simpan guard, tandai artikel selesai, daftar progres, persetujuan tutor, proctor (konfigurasi berjenjang modul→folder→item, konfigurasi efektif, sesi pengawasan, kejadian + kunci otomatis, geofence, buka kunci), status gerbang sesi kelas | ✅ 2026-10-05 |
| **G3e** | Label modul (5 route), endpoint publik landing (3), sinkron jalur belajar + validasi kurikulum (3), laporan konten dari siswa (1), heatmap belajar saya + kelas (2) | ✅ 2026-10-05 |
| **G3f** | Jalur kanonik `canon_path.rs` (10 route `/catalog`: mapel, tangga Tahap, unit per level, jalur belajar, simpul, unit topik, sesi latihan mulai/baca/jawab/selesai) + penyegaran ringkasan bank bab + XP & streak (`internal/gamification`) | ✅ 2026-10-05 |

### Catatan G11a–G11b (Admin Pusat, rollup metrik)

- `internal/admin`: log audit (kursor `(created_at, id)`, format kursor sama dengan chrono: `+00:00`, lewat `dbtype.RFC3339`), Ringkasan (peringatan penurunan pendapatan >40%, gagal AI >10%, job macet >1 jam), Penjualan (MRR, GMV, Diamond masuk/keluar, iklan), Kurikulum (target Bloom/kesukaran dari `contentfactory.StandardTargets`), Operasional AI + kesehatan antrean, Organisasi, Peserta (DAU/WAU/MAU, retensi, sebaran, corong), pencarian + detail peserta (setiap pembukaan dicatat di log audit; wilayah dicari malas lewat ip-api dan di-cache 24 jam), heatmap platform. `internal/module/tickets.go`: tiga route tiket laporan konten (daftar berkursor, detail dengan kunci jawaban, ubah status + audit). `internal/ai/routes.go`: enam route Pengaturan AI (layanannya sudah dari G10a). `internal/contentfactory/standard.go`: tabel sebaran standar 50 soal (dipakai halaman Kurikulum; sisa paket menyusul di G11c).
- `internal/metrics`: `metrics_rollup` (penjualan, langganan, pendaftar, AI, peserta, soal per hari; 3 hari terakhir tiap jam + snapshot konten hari ini + kohort retensi), idempoten karena semua `insert … on conflict do update`. Terdaftar di `cmd/worker` (jadwal tiap jam) dan `cmd/tools/backfillmetrics`.
- **Bug Rust #26 diperbaiki**: pencarian peserta memperlakukan `%` dan `_` sebagai wildcard LIKE, jadi mencari `_` atau `%` menampilkan semua pengguna; kini literal. #24 meluas ke `/admin/ai/catalog`, `/admin/content-tickets/{id}` (PATCH) dan route admin lain yang memakai `Json<T>` mentah: galat badan kini berupa amplop `invalid_json_body`.
- `paritydiff` `parity/g11a-admin.txt` (54 permintaan, sebagai ndsanja = platform_admin; hanya GET dan tulis yang ditolak sebelum menulis; detail peserta sengaja tidak ikut karena menulis baris audit di kedua backend): **50 identik, termasuk seluruh isi Ringkasan/Penjualan/Kurikulum/Peserta**; 4 beda hanya bentuk galat (#24). Baris `admin_audit_log`, `content_tickets`, `ai_role_settings`, `ai_model_catalog` tidak berubah.
- **Catatan jujur untuk rollup:** saya menjalankan `backfillmetrics` Go pada DB dev. Hash tabel agregat hari lampau: penjualan identik dengan yang disimpan Rust; langganan, pendaftar, AI, peserta berbeda. Nilai lama sudah tertimpa dan tidak bisa dibandingkan baris demi baris. Penyebab yang masuk akal: worker Rust tidak berjalan sejak lama sehingga baris tersimpan basi (churn bergantung `now()`, harga model katalog berubah, org/profil pengguna berubah), dan SQL-nya disalin verbatim. Test Go memverifikasi hitungan dengan data buatan (termasuk jsonpath `strict` yang tidak menggandakan soal). Tabel itu turunan dan dihitung ulang tiap jam; tidak ada data sumber yang berubah.


### Catatan G11c (Pabrik Konten)

- `internal/contentfactory`: `Engine{DB, AI, Module}`. Mesin: `plan.go`/`validate.go`/`qa.go`/`apply.go`/`runner.go` (`bab_plan`: hasilkan → cek aturan → hakim `agent_qa` → perbaiki hanya topik yang gagal → terapkan, kemajuan disimpan tiap putaran), `content.go`/`contentrunner.go`/`contentqa.go` (`bab_content`: materi, checkpoint, bank 50 soal standar atau `lean_bank_size`, hakim satu bab), `blueprint.go`, `gates.go`, `tagging.go`, `benchmark.go` (laporan gerbang), `admin.go` + `routes.go` (12 route `/admin/content-factory/*`). Handler `content_generation` terdaftar di `cmd/worker` (dilewati dengan peringatan bila tidak ada `OPENROUTER_API_KEY`).
- Prompt `bab_plan` diekstrak byte-identik dari Rust (`prompts_plan_gen.go`). Pengisi bank memakai `ai.GeneratePlan` / `ai.GenerateQuizGroup` dari G10 langsung.
- Test: unit (port test Rust blueprint, gates, tagging, hakim, validasi) + integrasi dengan penyedia palsu (run penuh, perbaikan satu topik, tinjauan setujui/tolak/regenerasi, jeda/lanjut/batal/ulang, standar, seed, bab_content standar & lean, balasan terpotong, hakim mati lalu lanjut). `paritydiff` (`parity/g11c-content-factory.txt`, ndsanja, hitungan baris tidak berubah): 41 permintaan, selisih hanya amplop galat (4), `GET /tahap/bukan-uuid` (amplop), dan bug #28.
- **Belum diport (G15 `cmd/tools`):** `rebalance_bank_lean`, mode benchmark `bab_content`, dan skrip `bin/*` (seed, conform_banks, tag_all_banks, lean_*).
- Urutan kunci JSON dan `HashMap` Rust yang acak (mode `seed`) dibuat deterministik di Go.


### Catatan G12 (pesan, kanvas, kolaborasi Yjs)

- `internal/messaging`: percakapan (satu per cohort+siswa, buka idempoten, siswa atau pengelola cohort), pesan, tanda baca, dan Kanvas (sesi menulis bersama pada item kuis dengan grup `essay`). WebSocket `/ws/canvas/{id}?token=` memakai `coder/websocket`: auth lewat query (ditutup 1008 `unauthorized`/`forbidden`), hub sendiri yang tidak mengirim balik ke pengirim, kehadiran daring/luring, mode `learning`/`assessment`/`exam` ditegakkan di server, hanya komentar dan ganti mode yang disimpan sebagai `canvas_events`, snapshot dibatasi sekali per 10 detik. Submit memakai `assessment.BeginWritingSubmit` + `ai.RunWritingEvaluation` (potongan `submit_writing_attempt` Rust; satu-satunya pemakainya adalah kanvas).
- `internal/collab`: `/ws/module-items/{id}/collab` kompatibel y-websocket, memakai `skyterra/y-crdt`. Satu ruang per item, dimuat dari `yjs_state`, checkpoint tiap `COLLAB_CHECKPOINT_INTERVAL_SECONDS` dan sekali lagi saat koneksi terakhir keluar (ruang dibuang), awareness pemilik koneksi dibersihkan saat keluar, pesan rusak hanya memutus koneksinya. Izin: peran penulis, atau hibah editor pada item; item `published`/`archived` ditolak.
- **Keputusan ADR-0020 §6: pilihan 1 (Go penuh) lolos uji, sidecar Rust tidak diperlukan.** Dibuktikan dengan Yjs asli (Node `y-websocket`, skrip di `agent/tools/qa/` bila perlu diulang; server uji `TestServeForRealYjsClients`): dua klien menyatu untuk Text, XmlFragment, Map dan awareness; sesi baru setelah ruang kosong memuat status dari Postgres; **32 `yjs_state` yang ditulis `yrs` di database dev terbaca Go, ditulis ulang, dan hasilnya identik di Yjs (state vector dan JSON)**. `TestReadStatesWrittenByYrs` mengulang pemeriksaan sisi Go.
- Test: 5 test messaging (termasuk WebSocket sungguhan), 3 test collab (dua penyunting menyatu + checkpoint, izin, pesan rusak). `paritydiff` (`parity/g12-messaging.txt`, ndsanja, hitungan baris tidak berubah): 13 permintaan, 3 selisih (amplop galat).
- Belum: kunci ruang hanya di satu proses, seperti Rust (tanpa fan-out lintas instance); perlu diingat saat Go berjalan lebih dari satu replika.


### Catatan G15 (cutover) 🔨 2026-10-06 — semua yang aman dikerjakan sudah selesai; tinggal tukar produksi

- **Worker**: registry memuat keenam jenis job Rust (`metrics_rollup`, `content_generation`, `league_season_close`, `league_circuit_close`, `pare_push_reminders`, `pare_voice_purge`).
- **Alat `cmd/tools`**: `backfillmetrics`, `devtoken`, `paritydiff`, **`benchcmp`** (gerbang kinerja), `pare_vapid_keys`, `pare_qa_tokens`, `seed_content_factory`, `tag_all_banks` (dry run di dev: 704 bank, sama dengan Rust), `backfill_question_uids` (70 `quiz_config` tak valid dilewati, data lama), `backfill_section_gates` (dry run: 80 artikel/320 Bagian). **Sengaja tidak diport** (eksperimen biaya AI sekali jalan, bukan fitur produk; tetap ada di arsip Rust): `conform_banks`, `lean_bab_content`, `lean_benchmark`, `benchmark_bab_content`, `generate_units`, `import_canonical_registry`, `backfill_*` Rust lain yang sudah dijalankan di DB dev dan prod.
- **Gerbang kinerja** (`parity/perf-gate.txt`, 22 endpoint terpanas, 200 permintaan × 8 pekerja, A/B berselang-seling melawan Rust `:wip`): **lulus, p95 Go ≤ Rust di semua endpoint** (rasio 0,17–0,92; `/pare/content` 0,45). Dua temuan diperbaiki sebelum lulus: tangga level di-parse ulang tiap baris misi (di-cache sekali) dan daftar misi N+1 (kini 3 query, rasio `/pare/missions` 14,6 → 0,23).
- **Regresi `paritydiff` penuh** (30 daftar): semua selisih termasuk kelas yang sudah dikenal (penolakan teks-polos axum untuk parameter/JSON salah bentuk, `next_cursor` data uji, URL presigned beda tanda tangan, perbaikan bug yang disengaja #1–#29); `g14b` 17/17, `g3-rules` dan `g4-checkpoints-templates` (149) identik.
- **Skrip `alr/game`** (`export-content`, `missions`, `gen-langrule-cases`, `journey`, `check-benchmark-plan`, `audio/lib`, README) kini menunjuk `titian-backend-go/data/pare/` (berkas identik byte-per-byte dengan Rust).
- **Image produksi** `titian-backend-go:prod` terbangun (72,5 MB, biner statis API + worker) dan lulus smoke test terhadap DB dev (`/health`, `/pare/content` 4,8 MB).
- **Audit akhir (2026-10-06)**: 446 route Rust = 446 route Go (himpunan identik, diekstrak dari `routes/*.rs` dan `chi.Walk`; `cmd/api/routes_dump_test.go`, `ROUTES_OUT=… go test`), 96/96 migrasi identik dan memakai tabel `_sqlx_migrations` yang sama, semua variabel env terbaca, `-race` bersih (pare, messaging, collab, jobs).
- **Uji beban WebSocket** (`game/scripts/loadtest.ts`, 1000 klien, 6 ruang, 4 langkah/dtk, 30 dtk, DB scratch): Go online 1000/1000, 3.682 pesan/dtk terkirim, 10.972 diterima, step→peer p50 56 ms / p95 102 ms; Rust `:wip` p50 61 ms / p95 102 ms (jumlah pesan setara). Memori setelah uji: Go 102 MiB, Rust 172 MiB.
- **Kapasitas maksimal Go** (server dikunci 2 core, generator beban di 2 core lain, loopback, tiap klien ±3,7 pesan/dtk): 1000 klien CPU 73% p95 103 ms · 2000 CPU 122% p95 157 ms · **3000 CPU 163% p95 227 ms (nyaman)** · 4000 CPU 187% p95 345 ms (jenuh: pesan diterima mendatar ±30 rb/dtk) · 5000 menurun (p99 5,6 dtk). Memori ±85 KB/koneksi (425 MiB di 5000). Tanpa pembatasan core (4 core dibagi generator): 3000 p95 233 ms, 6000 p95 457 ms, 10000 runtuh. Batas praktis VM 2 vCPU yang juga memuat Postgres/Redis/Caddy: perkirakan ±1500–2000 pemain serentak; bila lebih, naikkan vCPU atau pecah hub (G16 di Pasca-cutover).
- **PRODUKSI DITUKAR 2026-10-06 (01:09 UTC)**: produksi ternyata di VPS **Hetzner** `ubuntu-4gb-nbg1-1` (`ssh hetzner`, `/home/debian/titian-backend`), bukan GCP (VM GCP tak terjangkau; `api.titianasa.com` → 91.98.231.251; host dipakai bersama parelabs/nanyang/livekit, hanya `titian_api`/`titian_worker` disentuh). Urutan: backup DB (`/home/debian/backups/titian_pre_go_20261006T010732Z.sql.gz`, salinan di `/home/john/backups/`), simpan compose lama (`docker-compose.prod.yml.rust-bak`), `deploy.sh sync` + `local-build` + `restart`. DB prod baru 93 migrasi; Go otomatis memasang 0094–0096 (aditif: kolom nullable, tabel baru, CHECK dilonggarkan) → 96/96 sukses. Hasil: `/health` ok, `/pare/content` 974 KB gzip + ETag 304, CORS benar, log 0 WARN/ERROR, api 27 MiB, worker 3,5 MiB, worker memuat semua jenis job. **Rollback**: `ssh hetzner 'cd /home/debian/titian-backend && cp docker-compose.prod.yml.rust-bak docker-compose.prod.yml && docker compose -f docker-compose.prod.yml up -d --pull never'` (image `titian-backend-rust:prod` masih ada di server; migrasi 0094–0096 aditif sehingga Rust lama tetap jalan).
- **Belum**: mengarsipkan `titian-backend-rust` (tar ke `/home/john/backups/` + commit dulu) — tunggu Go stabil beberapa hari.

### Catatan G14 (Kampung Bahasa Pare) ✅ 2026-10-06

Dipecah jadi G14a–f; semuanya di paket `internal/pare` (satu paket karena layanan Pare saling bergantung: tampilan pemain → hidup/premium, ekonomi → misi, harian → misi, tick → hub).

- **G14a inti** — `content` (JSON ter-embed `data/pare/*.json`, ETag kuat `"pare-<sha256[:8]>"`), `economy`, `life` (simulasi hidup, stamina/kenyang, beli/laundry/sepeda/taman/tidur), `daily` (hash FNV-1a UTF-16 identik dengan Rust, uji dengan tanggal uji Rust), `premium` (+ voucher, `ActivatePremium` didaftarkan ke `economy.Service.ActivateParePremium`), `boost`, `player`, `media` (foto profil, klip & manifes audio, `/pare/state`).
- **G14b pelajaran & kertas soal** — `question.go` (semua jenis soal: pilihan, susun, ucap, tulis, karangan; `Public`/`Reveal`/`Translation`/`Hint`; JSON identik dengan serde Rust karena kertas disimpan sebagai JSON dan dibaca kedua backend), `paper.go` (buat/bantu/jawab/selesai kertas, ujian lompat level, tantangan, kesempatan terakhir, `/pare/levels`), `compose.go` (penilaian menulis oleh AI dengan pemeriksaan panjang/aksara sebagai cadangan), `path.go` (jalur belajar: Level → Bab → Pelajaran → Materi/Latihan/Praktik/Cek/Misi, `settle`).
- **G14c misi & perjalanan** — `mission.go` (mesin misi dari `missions.json`: langkah pergi/bicara/dialog/beli/lakukan/baca/dengar/temukan/sosial, skor Hasil 40 + Bahasa 40 + Mandiri 20, bintang 60/80/90, `OnEvents` dipanggil dari `Bump`), `journey.go` (Buku Perjalanan, `TryLevelUp`). Pengacakan varian per pemain memakai PCG Go, bukan ChaCha Rust: sebuah run disimpan sekali dibuat, jadi kedua backend saling membaca.
- **G14d chat & hub** — `langrule.go` (aturan bahasa; **551 kasus nyata dari `judgeMessage()` TypeScript lulus** lewat `data/pare/langrule_cases.json`), `hub.go` (hub realtime: kanal ≤ 50 pemain, `moves` per 100 ms, satu koneksi per pemain, antrean terbatas, chat all/near/private/grup, permintaan pesan, blokir dua arah, penalti ½ nyawa & poin bahasa), `socket.go` (`/ws/pare?token=`, batas pesan 4 KB, kode tutup 1008/4404), `chat.go` (inbox, status percakapan, baca/terima/hapus/keluar grup).
- **G14e push** — `webpush.go` (RFC 8291 `aes128gcm` + VAPID ES256 dengan pustaka standar; **nilai antara RFC 8291 §5 cocok persis**), `push.go` (langganan, pengaturan, batas harian 12, throttle per percakapan, pengingat misi/streak/tidur sebagai job `pare_push_reminders` tiap 5 menit di worker). `cmd/tools/pare_vapid_keys`.
- **G14f suara** — `voice.go` (gerbang & persetujuan, voice note: unggah presigned PUT → selesai → kirim sebagai pesan `kind: "voice"`, putar, ekspor/hapus data, purge per jam sebagai job `pare_voice_purge`), `voicelive.go` (panggilan LiveKit: kamar di Redis `pare:call:room:*`/`pare:call:player:*` dengan `SET NX EX`, undangan 45 dtk, webhook `/webhooks/livekit` terverifikasi JWT+SHA-256, batas waktu bicara harian), `livekit.go`, `moderation.go` (blokir, laporan, antrean moderator `/admin/voice/reports*` — dipindah dari G11 ke sini). Kait penghapusan akun (`identity.OnAccountDelete`) sekarang mendaftarkan `PurgeUser` + `RemoveAvatar`.
- **Pembayaran Premium**: `economy.Service.CheckoutPareOrder` (`POST /pare/premium/checkout`, pesanan QRIS Rp10.000, respons = bidang pesanan + `qris_payload`), webhook QRIS mengaktifkan lewat `ActivateParePremium`.
- **Tes**: `question_test` (semua pembangun soal, misi sah, skor, pengacakan), `langrule_test`, `webpush_test`, `routes_test` (pemain, kelas sempurna, jalur, misi sampai 3 bintang, ujian/ lastchance ditolak), `hub_test` (kehadiran, `moves`, chat, aturan bahasa, DM sebagai permintaan, kick tab kedua), `voice_test` (gerbang, note, blokir/laporan/kunci, panggilan + webhook + batas waktu; bagian panggilan butuh Redis di `127.0.0.1:6379`, dilewati bila tak ada).
- **paritydiff** `parity/g14a-pare-core.txt`, `g14b-pare-papers.txt` (GET sebagai ndsanja; tulis hanya yang ditolak sebelum mengubah apa pun, isi soal acak tak bisa dibandingkan). Image Rust `:prod` **basi**: dibangun tanpa perubahan Pare yang belum di-commit (konten 3 bukan 4 paket, tanpa `chapters`, tanpa `avatar` di `/pare/me`, kode galat `not_found`, tanpa jenis kertas `path`), jadi selisihnya bukan regresi Go. Go mengikuti kode sumber Rust. Dengan image pembanding baru `titian-backend-rust:wip` (dari working tree), `g14b` **identik 17/17**, `g14c` (42 permintaan: perjalanan, misi, chat, push, suara, admin) identik kecuali penolakan teks-polos axum untuk parameter/query salah bentuk (kelas beda yang sudah dikenal, Go memakai amplop `{error, detail}`), dan `g14a` hanya beda pesan galat parameter path serupa; `confidence` transkrip (f32 Rust dilebarkan ke f64) disamakan.

### Catatan G13 (grup, liga, sirkuit, Ruang Kelas)

- `internal/studygroup` (satu paket, seperti kelompok berkas Rust): `group.go` (CRUD, gabung/keluar/kode undangan, anggota, moderasi peran, ban, transfer kepemilikan; kuota & kapasitas dari `economy.LimitsFor`/`GroupCapacity`, kunci advisory per pengguna lalu `for update` pada baris grup), `content.go` (konten terlampir, kemajuan, target; tidak ada angka yang disimpan klien), `moderation.go` (laporan, tangguhkan), `league.go` (mesin skor: poin selalu diturunkan dari data, bonus XP tiga besar anggota dengan batas 500/7 hari, papan Global sintetis, tamu lewat kode, nilai manual teraudit, penutupan musim), `circuit.go` (liga berjenjang: bekukan semua divisi dulu, baru pindahkan), `classroom.go` (Ruang Kelas = `cohorts` ber-`owner_id` + produk latar belakang tersembunyi, Grup Kelas, konversi/lepas, ikhtisar kelas), `routes.go`/`routes2.go`.
- Job: `studygroup.Handlers()` + `Schedules()` didaftarkan di `cmd/worker` (tiap 5 menit, prioritas 50). Tambahan kecil di tempat lain: `marketplace.EnsureTutorProfile` (penyediaan profil tutor malas untuk pemilik kelas).
- Test: 16 test integrasi + unit (peringkat, bonus, kode). `paritydiff` (`parity/g13-groups.txt`): 62 permintaan terhadap fixture sementara (grup, undangan, konten, target, liga, musim) yang disemai lewat SQL dan **dihapus lagi**, dijalankan sebagai ndsanja (pemilik) dan p2016-dev (anggota), hitungan baris tidak berubah. Selisih hanya: amplop galat (parameter query/badan JSON/405) dan stempel waktu papan Global yang memang "sekarang".
- Tidak ada bug Rust baru di berkas ini.
- Belum teruji dengan data nyata: sirkuit dan Ruang Kelas berbayar (dev tidak punya langganan Pro; dicakup test integrasi saja).

### Catatan G10d (Live AI Chat, tutor chat, Speaking Room, audio prompt)

- `internal/ai/livechat.go`: `POST /ai/live-chat-turn` dan `/stream`. Validasi dan penyusunan permintaan satu kode untuk keduanya (`prepareTurn`): izin baca item, harus artikel, pesan ≤ 4000 karakter, bahasa, rencana dari klien, indeks bagian dijepit, satu event `live_chat_question` per giliran siswa (terpotong 500 karakter, dicatat hanya bila ada consent `ai_chat_storage`, tidak untuk preview). Non-stream: satu coba-ulang, balasan kosong = galat. Stream: SSE `chunk` / `done` / `error`, tanpa coba-ulang (gagal membuka stream = galat biasa 422), baris data dipecah per newline, keep-alive `:` tiap 15 dtk, tiap event langsung di-flush, `text/event-stream` tidak dikompres.
- `internal/ai/tutorchat.go`: tutor bebas modul. Rantai model dari `TUTOR_CHAT_MODELS` (hanya yang aktif di katalog OpenRouter), model yang gagal diistirahatkan (429 → 2 mnt, 404/guardrail → 15 mnt, lain → 45 dtk) dan dilewati kecuali semuanya istirahat, semua gagal = 502 `tutor_unavailable`, batas 40 pesan per 10 menit per pengguna (dalam memori, dihitung sebelum validasi seperti Rust), daftar isi 3–6 bagian dengan cadangan bawaan.
- `internal/ai/speakingroom.go`: 4 route tanpa cek peran, tanpa `ai_tasks`, tanpa kredit; `turn` dan `summary` mengembalikan JSON model apa adanya (camelCase), `tts` mengembalikan byte audio, `transcribe` base64 → STT. Galat penyedia pada `tts`/`transcribe` tetap 500 seperti Rust. Route modul `GET /module-items/{id}/speaking-prompt-audio` (suara dari blok `speaking_prompt`, gerbang terbit seperti membuka item) kini ada (`module.SpeakingPromptText`).
- `internal/ai/prompts_gen.go` dihasilkan dari teks Rust (placeholder `‹nama›`), bukan diketik ulang, supaya prompt tutor bebas modul, tutor Live Chat, dan Speaking Room identik byte demi byte.
- **Bug Rust #22–#25 diperbaiki** (tabel di bawah): giliran Live Chat yang ditinggal klien tidak tercatat di `ai_tasks`; `transcribe` dengan base64 rusak → 500; galat decode `tutor-chat` berupa teks polos bukan amplop `{error, detail}`; `parse_outline` panik pada balasan `} {` (dan peta batas laju tak pernah dibersihkan). #20 kini juga mencakup Live Chat.
- `paritydiff` `parity/g10d-chat.txt` (31 permintaan, sebagai p2016-dev non-admin; hanya yang ditolak sebelum penyedia dipanggil atau hanya-baca): 20 identik, 11 beda (teks galat body, amplop galat tutor-chat, dan `transcribe` base64 rusak 500 vs 422, semuanya disengaja). Baris `ai_tasks`, `learning_events` (live_chat_question), `content_blocks`, `credits`, `module_items` tidak berubah.
- **Batas pembanding:** giliran obrolan, aliran SSE, tutor, ringkasan, tts, dan transkripsi sungguhan hanya teruji dengan penyedia palsu; urutan frame SSE, pemisahan baris data, keep-alive, putus di tengah, dan klien yang pergi diuji dengan test.

### Catatan G10c-2 (generator kuis, kode web AI)

- `internal/ai/quizgen.go`: `POST /ai/generate-quiz-group` (mode `replace` / `append` / `rewrite` / `answer_only`; prompt berlapis BENTUK → SUBTIPE → VARIAN → KONTEKS; sumber gambar, teks tempelan, rujukan bagian Modul Belajar; slot bank dengan `fungsi`; soal di topik yang sama dikirim sebagai "jangan diulang" kecuali ekstraksi/`lean`/`answer_only`; hasil digabung ke grup, bacaan/pool hanya mengisi yang kosong, nomor dihitung ulang dari nomor bebas terendah dan rentang multi-poin dipertahankan, soal mirip (Jaccard ≥ 0,6 atas kata isi) dibuang dan jumlahnya dilaporkan; LaTeX yang rusak karena `\t`/`\f`/`\b` dipulihkan; penulisan memakai kunci baris `for update` dalam satu transaksi, `uid` baru diberikan, struktur divalidasi sebelum disimpan, lalu ringkasan bank bab disegarkan), `POST /ai/quiz/convert-group-type` (pembungkus tipis di atasnya, tanda draf), `POST /ai/quiz/suggest-group-types` (usulan struktur, subtipe tak dikenal dibuang dari blok), `POST /ai/quiz/generate-batch` (3 grup serentak, tiap kegagalan dilaporkan sendiri dengan pesan yang sama seperti satu grup).
- `internal/ai/codeweb.go`: `POST /ai/generate-code-web` (dokumen HTML utuh dengan token warna Titian dan jembatan `window.Titian`; dua kali coba; lalu **juri QA** lima dimensi, sepenuhnya best-effort: gagal jalan = `qa: null`, html tetap dikembalikan; isu boleh datang sebagai string "major: …"). Teks prompt web dan panduan ALM dibandingkan byte demi byte dengan sumber Rust.
- `internal/quiz/shape.go` + `data/shapes.json` (15 bentuk keluaran, 19 petunjuk subtipe, aturan varian; diekstrak dari sumber Rust, bukan diketik ulang) dan `taxonomy_prompt.go` (definisi Bloom/kesukaran, `TargetSpread`, `StemReadability`, `TaxonomyPromptRules`; memakai `Apportion` yang sudah ada).
- **Bug Rust #20 diperluas**: nama penyedia pada `ai_tasks` untuk generator kuis ("routing"), usulan tipe, dan kode web + QA ("openrouter" ditulis mati) kini nama penyedia yang sungguh melayani. **#21**: juri QA web mengiris JSON dari `{` pertama sampai `}` terakhir tanpa memeriksa urutan, sehingga balasan seperti `} {` membuat Rust panik; Go membalas "penilai tidak mengembalikan JSON".
- Beda yang disengaja (bukan bug): hasil `generate-batch` dikembalikan menurut urutan grup di item (Rust menurut urutan selesai).
- `paritydiff` `parity/g10c-quizgen.txt` (29 permintaan, sebagai p2016-dev non-admin; hanya yang ditolak sebelum penyedia dipanggil): 23 identik, 6 beda teks galat body. Baris `ai_tasks`, `module_items`, isi `quiz_config` semua kuis (hash), `credits` tidak berubah.
- **Batas pembanding:** pembuatan, ekstraksi, batch, konversi, usulan, dan kode web sungguhan hanya teruji dengan penyedia palsu. `lean` dan `slots` tidak punya padanan HTTP di route ini selain `slots`; `lean` dipakai pengisi bank (G11).

### Catatan G10c-1 (rencana pelajaran AI, edit bagian, terjemahan, fragmen ALM)

- `internal/ai/lessonplan.go`: `POST /ai/generate-lesson-plan` (protokol berbatas `<<<PLAN>>>`/`<<<SECTION>>>`, bukan JSON, supaya LaTeX dan blok ALM tidak rusak oleh escape; balasan yang terpotong **dilanjutkan** sampai 5 putaran dengan menyebut bagian yang sudah ada, tidak diminta ulang dari awal; satu coba-ulang biasa untuk gangguan penyedia atau balasan tanpa bagian; token semua putaran dijumlahkan; hasil tidak disimpan), `POST /ai/edit-lesson-section` (rencana yang sedang diedit dikirim klien; bagian rujukan `@N` dan item rujukan `@@` dalam modul yang sama; checkpoint bagian dipertahankan), `POST /ai/translate-lesson-plan` (selalu menerjemahkan rencana TERSIMPAN, bagian + judul secara paralel, cache per bahasa dengan kunci hash isi, hasil sebagian tidak di-cache, pembaca tanpa hak kunci jawaban tidak menerima checkpoint), `POST /ai/generate-alm-fragment` (asisten klik-kanan). Urutan galat sama dengan Rust, termasuk model tak diizinkan (422) sebelum cek izin.
- `internal/ai/almguide.go`: panduan dialek ALM yang sama untuk komposer dan asisten; `internal/quiz/stage.go`: `InferStage` (SD/SMP/SMA/Kuliah/Pascasarjana/Umum dari teks tingkat bebas) dipakai oleh kalibrasi keterbacaan dan nanti taksonomi kuis (G10c-2).
- Dikerjakan di `module`: `RequireEditItem` diekspor.
- **Bug Rust #20 diperbaiki**: `ai_tasks.provider` untuk semua tugas yang lewat `RoutingProvider` berisi `"routing"` (nama pengarah, bukan API yang melayani), dan fragmen ALM selalu menulis `"openrouter"` walau Vertex yang menjawab. Go mencatat penyedia yang benar-benar melayani model itu.
- `paritydiff` `parity/g10c-lessonplan.txt` (25 permintaan, sebagai p2016-dev non-admin; hanya yang ditolak sebelum penyedia dipanggil atau hanya-baca): 17 identik, 8 beda teks galat body. Baris `ai_tasks`, `module_items`, `module_item_translations`, `content_blocks`, `credits` tidak berubah.
- **Batas pembanding:** pembuatan, edit, dan terjemahan sungguhan hanya teruji dengan penyedia palsu (tidak membakar token di kedua backend). Terjemahan ke bahasa lain dijalankan paralel tanpa batas seperti Rust; jika kelak sering kena 429, batasi jumlah serentak.

### Catatan G10b (konten AI, OCR, evaluasi, transkripsi, dokumen)

- `internal/ai/content.go`: `POST /ai/generate-lesson` (prompt dibentuk dari mata pelajaran modul/item: keluarga bahasa vs bahasa asing vs rumus; kerangka "Konstitusi Grammar" 11 bagian bila ada `grammar_target`; parse ALM → validasi blok → cek Konstitusi di dalam loop coba-ulang, baru item dibuat dengan `generated_by='ai'`) dan `POST /ai/generate-questions` (array JSON, `JSONMode` tak pernah dipasang, tiap soal divalidasi dulu, tak ada batch setengah jadi; jumlah salah = `invalid_ai_output_count` tanpa coba-ulang). Biaya platform: nol kredit. Izin dicek **sebelum** panggilan penyedia.
- `internal/ai/ocr.go`: `POST /ai/ocr-to-question`; aset harus terbaca oleh pemanggil (izin Drive), URL gambar ditandatangani ulang, tiap butir menjadi draf dengan `ocr_verification` (dan `ocr_uncertain_type` bila tidak dikenali).
- `internal/ai/evaluation.go`: penilai esai (4 kriteria) dan berbicara (STT lalu 5 kriteria + `correction` bila grammar/naturalness < 65) sebagai kait `assessment.EvaluateRubric`; gagal apa pun = tanpa evaluasi, attempt tetap `submitted`. Rubrik tetap `…00f1` / `…00f2`. Posisi umpan balik tetap **offset byte** (sama dengan Rust; klien belum memakainya, lihat Pasca-cutover).
- `internal/ai/document.go`: `POST /documents/extract` (PDF lewat `github.com/ledongthuc/pdf` dengan `recover`, DOCX lewat `archive/zip` + `encoding/xml`; 60.000 karakter; 10 MB), `POST /ai/transcribe-audio` (hanya aset Drive audio/video yang boleh dibaca pemanggil).
- Dikerjakan di `module`: `ValidateBlocks`, `CreateGeneratedItem`, `GrammarSections` / `MissingGrammarSections` diekspor; QA submit-review tetap memakai fungsi yang sama.
- **Bug Rust #18–#19 diperbaiki** (tabel di bawah): alasan kegagalan generator hilang (`{e}` mencetak nama varian), dan nama tipe lama `mcq`/`fill_blank` di prompt soal + OCR.
- `paritydiff` `parity/g10b-ai-content.txt` (14 permintaan, sebagai p2016-dev non-admin; hanya yang ditolak sebelum penyedia dipanggil): 6 identik, 8 beda teks galat body. Baris `ai_tasks`, `module_items`, `questions`, `content_blocks`, `evaluations`, `assets`, `credits` tidak berubah.
- **Batas pembanding:** jalur yang memanggil penyedia sungguhan (generate lesson/soal, OCR, evaluasi, STT) hanya teruji dengan penyedia palsu, supaya tidak membakar token di kedua backend. Pembaca PDF berbeda dari Rust (`pdf-extract`): spasi dan urutan teks pada PDF rumit bisa berbeda; kasus teks sederhana setara.

### Catatan G10a (lapisan penyedia AI)

- `internal/ai`: antarmuka `Provider` (`Generate`, `Transcribe`, `Synthesize`, `Stream` sebagai `iter.Seq2`), `OpenRouter` (chat, STT multipart, TTS; PCM Gemini dibungkus WAV), `Vertex` (Gemini lewat ADC `golang.org/x/oauth2/google`; coba ulang 429/5xx dan sambungan putus dengan jeda 4/12/30 dtk ±25%, timeout tidak diulang; balasan terpotong = galat kecuali `AllowPartial`; bagian "thought" tak pernah masuk jawaban; gambar OCR diunduh lalu diinline base64), `Routing` (id berisi "/" → OpenRouter, selain itu Vertex; STT/TTS selalu OpenRouter), `NoopVertex`, `Metered`, dan pemalsu untuk test (`Fake`, `Flaky`, `Scripted`). `NewProviders` membaca `OPENROUTER_API_KEY` (wajib) dan Vertex (opsional: gagal ADC → `NoopVertex`, sama seperti Rust).
- Pengaturan AI (`settings.go`): katalog model + 19 peran dengan fallback env yang sama dengan Rust (`quiz_generation`, `curriculum_planning`, `interactive_web_generation` memakai kolom `lesson_generation`), `Resolve` (baris peran yang aktif, kalau tidak fallback env; peran tak dikenal = panic karena itu salah ketik di pemanggil), cache snapshot yang dibuang setiap tulis, `SaveRole` (ganti penuh; model harus ada, aktif, dan punya semua kemampuan yang dibutuhkan peran), `TestRole`, `PatchCatalogEntry`, `CreateCatalogEntry`, `ResolveModel` (daftar izin penulis = baris katalog aktif berkemampuan `text`), `ResolveMaxTokens` (plafon katalog, atau daftar `/models` OpenRouter yang di-cache saat berhasil; selalu dipotong ke estimasi pemanggil), `GenerateWithFallback`. Setiap tulis admin dicatat lewat `internal/platform/audit`.
- Gateway `Evaluate` (`POST /ai/evaluate`, tugas `grammar_evaluation`): iklan yang belum dipakai membayar tanpa menyentuh saldo, kalau tidak cek saldo; satu kali coba ulang pada penyedia yang sama **sebelum** biaya dipotong; gagal = baris `ai_tasks` berstatus `failed` tanpa potongan. Route `GET /ai/models`. Route admin (`/admin/ai/*`) memakai layanan ini dan dipasang di G11.
- **Bug Rust #17 diperbaiki**: aliran Vertex (Live AI Chat) mendekode tiap bacaan jaringan sebagai UTF-8 sendiri-sendiri, sehingga karakter multibyte (emoji, CJK, huruf beraksen) yang terbelah di antara dua bacaan menjadi U+FFFD di balasan. Go menyangga **byte** dan baru memecah di batas event.
- Test: pembungkus kode ```, routing, fallback model, plafon token, Metered, Flaky/Scripted, header WAV, OpenRouter dan Vertex terhadap server palsu (badan permintaan, usage, content null, 429, parts terbelah, thought, MAX_TOKENS dengan/tanpa partial, SAFETY, gambar inline, retry hanya untuk yang sementara, endpoint global vs regional), SSE (CRLF, banyak event, event setengah jadi, event tanpa teks, karakter terbelah), lalu DB: resolve + override + nonaktif + ganti penuh + cache langsung berlaku, validasi tulis peran/katalog + audit, `TestRole`, daftar izin penulis, `/ai/models`, `/ai/evaluate` (iklan, saldo, ditolak tanpa biaya, retry sekali, gagal tak dipotong, penyedia mati).
- `paritydiff` `parity/g10a-ai.txt` (11 permintaan, sebagai p2016-dev; hanya yang ditolak sebelum penyedia dipanggil): 6 identik, 5 beda teks galat body. Baris `ai_tasks`, `credits`, `ad_views`, `ai_role_settings`, `ai_model_catalog`, `admin_audit_log` tidak berubah. **Batas pembanding:** panggilan penyedia sungguhan (evaluasi tata bahasa, STT/TTS, Vertex) hanya teruji lewat server palsu; Vertex tidak punya kredensial ADC di kontainer Go dev, jadi Go jatuh ke `NoopVertex` (sesuai desain) dan model `gemini-*` baru bisa dicoba di mesin yang punya `gcloud auth application-default login`.

### Catatan G9 (Drive & aset)

- `internal/drive/{drive,ops,routes}.go`: `ResolveAccess` (platform_admin = editor atas apa pun yang ada, pemilik = editor, lalu izin langsung + izin folder induk untuk pengguna/peran; terbaik menang), `requireAccess` (tanpa akses sama sekali = 404, kurang = 403 `insufficient_permission`), `requireOwner` (berbagi dan tempat sampah: pemilik/admin saja, aset tanpa pemilik = 403 `owner_only`), unggah multipart (batas 32 MB di pembaca + `AssetMaxBytes` → 413 `file_too_large`), presigned PUT + konfirmasi, rename/pindah/hapus/pulihkan/hapus permanen untuk aset dan folder (folder menyeret isinya ke sampah), berbagi + cabut, aktivitas (dicatat sebisanya, kegagalan tidak menggagalkan permintaan), daftar `/drive`, `/drive/trash`, `/drive/shared-with-me`, `/drive/share-candidates`.
- **Bug Rust #12–#16 diperbaiki** (tabel di bawah): daftar akar `/drive` dan `/assets` bocor ke semua pengguna; cabut berbagi lintas sumber daya; kursor halaman melewatkan satu baris; hapus permanen folder berisi file → 500; admin atas id yang tak ada → 500/204; nama kosong diterima.
- Pembanding `parity/g9-drive.txt` (55 permintaan, sebagai pengguna **non-admin** p2016-dev): 20 beda, semuanya sudah dikenal atau disengaja: daftar akar (Rust menampilkan aset ndsanja ke p2016-dev), `next_cursor` sampah, URL presigned yang berbeda tiap permintaan, teks galat serde/UUID.
- **Insiden pembanding (dev, bukan produksi):** putaran pertama saya jalankan sebagai ndsanja (platform_admin) dengan daftar yang saya kira hanya-baca. Ternyata admin boleh menghapus permanen aset orang lain dan membuat folder berspasi: **satu baris aset sampah milik p2016-dev (`f6fb3ca9…`, image/png) terhapus**, dua folder dan 10 baris aktivitas tercipta, `updated_at` aset `2208f1d5…` berubah. Folder dan aktivitas sudah dibersihkan; baris aset tidak bisa dipulihkan (objek R2-nya tetap ada karena Rust tak pernah menghapus objek). Daftar kini dikunci ke non-admin dan header berkas menjelaskan alasannya.
- Dev hanya punya 7 aset, 0 folder, dan 4 berbagi (semuanya `module_item`), jadi folder, berbagi aset, dan unggah hanya teruji lewat test Go (`internal/drive/drive_test.go`: unggah + folder + sampah, privasi akar, berbagi + warisan folder, presigned, paginasi tanpa baris terlewat, kandidat berbagi, admin atas id hilang + nama kosong).
- Belum: objek R2 tidak pernah dihapus saat hapus permanen (sama seperti Rust; dicatat di Pasca-cutover).

### Catatan G8 (kehadiran, sesi kelas, proctoring)

- `internal/marketplace/session.go`: absensi kohort (manual, dengan jatah sesi paket yang hanya berubah saat benar-benar masuk/keluar dari `present`), sesi kelas (jadwal + rapat lewat penyedia), verifikasi kehadiran dari laporan peserta (`partial` bila hadir < 75% jadwal, `late` bila masuk > 10 menit, selain itu `present`; siswa tanpa bukti ditulis `absent` eksplisit; peran tutor tidak pernah dipercaya dari penyedia), simulasi peserta khusus sesi stub, laporan per sesi (pengelola lihat semua, siswa hanya tutor + dirinya), status rekaman. Pembantu Ruang Kelas yang dibutuhkan (`study_groups` / `study_group_members`, kolom `group_id`) ditulis sebagai kueri kecil; fiturnya sendiri tetap G13.
- `internal/assessment/proctoring.go`: kebijakan, sesi berpersetujuan (tanpa persetujuan tidak ada baris), event (hanya pemilik ujian, bukti harus aset milik sendiri, pesan galat sengaja samar), skor risiko 1/3/7 (maks 100, hanya ditampilkan, tidak pernah disimpan atau memutuskan apa pun), tampilan pemilik vs staf, retensi malas, antrean tinjauan, keputusan tinjauan (boleh ditinjau ulang, siswa pemilik pun ditolak).
- **Bug Rust #11 diperbaiki**: `POST /cohorts/{id}/sessions/{date}/attendance` menulis entri satu per satu, jadi status salah atau siswa tak terdaftar di tengah daftar membalas 422 **setelah** entri sebelumnya tersimpan dan jatah paketnya terpotong. Go memvalidasi semua status dan semua enrolmen lebih dulu; daftar yang ditolak tidak menyimpan apa pun.
- Perbaikan kecil di `meeting`: badan galat dari Google kini dipadatkan (JSON tanpa spasi) seperti Rust, sebelumnya diteruskan mentah.
- Perbaikan efisiensi tanpa mengubah hasil: antrean tinjauan proctoring mengambil severity dengan satu kueri, bukan satu kueri per sesi.
- Test: absensi + paket (daftar ditolak tidak menyimpan apa pun, hadir→hadir tidak memotong dua kali, keluar dari hadir mengembalikan jatah, baca pengelola/siswa/orang lain), sesi + verifikasi (jadwal terbalik/tanggal rusak/grup asing, simulasi hanya untuk sesi stub dan hanya oleh pengelola, peran tutor harus tutor sungguhan, bukti diganti bukan digandakan, sinkronisasi idempoten: present/late/partial/absent, enrolmen batal tidak ikut roster, baris verifikasi tanpa `marked_by`, laporan pengelola vs siswa), proctoring alur penuh (validasi kebijakan, persetujuan, pemilik saja, bukti, tampilan pemilik tanpa `events`/`risk_score`, skor 11, retensi memutus tautan bukti tetapi aset tetap, antrean, tinjau ulang).
- `paritydiff` `parity/g8-sessions-proctoring.txt` sebagai tiga pengguna: 33 permintaan, 28 identik; sisanya teks galat body yang sudah dikenal (dan, sebelum perbaikan di atas, bentuk badan galat Google). Baris kelas/absensi/peserta/kebijakan/proctoring/enrolmen dev tidak berubah.
- **Batas pembanding:** dev hanya punya 3 sesi kelas, 2 catatan absensi, 6 catatan peserta, 0 kebijakan proctoring, 0 sesi proctoring. Penulisan (tandai absensi, buat sesi, simulasi, sinkron) dan seluruh alur proctoring hanya teruji lewat test Go. Dua pembacaan rekaman memanggil Google sungguhan di kedua backend dan sama-sama gagal `invalid_grant` — kredensial dev Google Meet di `.env` kedaluwarsa.

### Catatan G7 (marketplace & tutor)

- `internal/marketplace`: profil tutor (promosi anggota org, daftar, ubah milik sendiri), produk belajar (validasi urut seperti Rust, penyediaan profil tutor malas untuk admin platform, draf hanya terlihat pemiliknya dan 404 untuk orang lain), kohort, enrolmen (idempoten, kuota kursi, jatah sesi paket), pembatalan siswa dengan kebijakan pengembalian (>24 jam penuh, 6–24 jam separuh, kurang dari itu nol) dan pembatalan tutor (selalu penuh), sertifikat (perkiraan CEFR dari mastery, ringkasan per keterampilan, pembekuan Ruang Kelas milik pemilik non-Pro, verifikasi publik yang selalu 200), tugas, pengumpulan, penilaian, rapor kohort, ulasan, reputasi publik tutor (termasuk waktu balas pesan).
- **Webhook pembayaran kini menyelesaikan pesanan kelas juga** (aktifkan enrolmen + 70% ke tutor, 30% platform dicatat di referensi); kait `SettleEnrollment` yang dijanjikan di G6 tidak diperlukan lagi dan dihapus. Satu perbaikan urutan: tutor dicari **sebelum** pesanan ditandai `paid`, jadi pesanan yang enrolmennya sudah hilang tidak terselesaikan setengah jalan. Yang masih menunggu hanya `economy.ActivateParePremium` (tiket Pare).
- **3 bug Rust baru diperbaiki** (tabel "Bug Rust yang diperbaiki di Go" #8–#10): paginasi `GET /products`, rentang skor penilaian tugas, dan ulasan yang bisa ditempelkan ke tutor mana pun.
- Test: tujuh alur — validasi produk + siklus penuh (draf → terbit → kohort → enrolmen → kursi penuh → checkout → webhook → dompet 70.000 → pembatalan penuh), kebijakan pengembalian dan CEFR (unit), pembatalan terlambat (pesanan tetap `paid`), pembatalan tutor oleh tutor/pemilik org (baris `refund`, pesanan `refunded`/`failed`), selesai → sertifikat (B2, ringkasan, kode 12 karakter, 409 kedua, verifikasi publik) → ulasan → reputasi dan waktu balas, tugas → kumpul ulang sebelum dinilai → 409 sesudahnya → rapor (kehadiran 66,7 + tugas 90 → 78,4), paginasi produk menelusuri semua halaman, profil tutor (peran `teacher`, PATCH sebagian).
- `paritydiff` `parity/g7-marketplace.txt` sebagai tiga pengguna (tutor pemilik produk, siswa terdaftar, orang lain): 60 permintaan, ±50 identik; selisih sisanya teks galat yang sudah dikenal ditambah **dua selisih yang disengaja**: `GET /products?limit=1` (`next_cursor` Go = baris terakhir halaman, Rust = baris berikutnya) dan `POST /submissions/{id}/grade` dengan skor di luar rentang untuk submission yang tak ada (Rust 404, Go 422 karena rentang divalidasi lebih dulu). Baris transaksi/pesanan/enrolmen/produk/kohort/profil/sertifikat/peran dev sama sebelum dan sesudah.
- **Batas pembanding:** dev hanya punya 2 produk, 1 kohort, 1 enrolmen (dengan 1 pesanan), 1 sertifikat, 0 ulasan, 0 tugas. Jalur tulis (enrolmen, checkout, webhook, batal, selesai, terbit sertifikat, tugas, nilai, ulasan) hanya teruji lewat test Go.

### Catatan G6 (gamifikasi & ekonomi)

- **G6a** `internal/gamification`: pencapaian (belajar / keterampilan / peningkatan mastery terhadap baseline), misi harian (80 XP sekali per hari), tier liga dari skor komposit streak + mastery + aktivitas (`CompositeScore`, juga `WeeklyGlobalScores` untuk papan liga Global nanti), leaderboard mingguan dengan alias untuk yang memilih disamarkan, ringkasan XP dan streak. 6 route `/me/xp`, `/me/streak`, `/me/achievements`, `/me/daily-mission`, `/me/league`, `/leaderboard/weekly`.
- **G6b** `internal/economy`: buku besar Diamond (sapu jatah kedaluwarsa secara malas, satu baris `expire` per jatah), tier langganan + `Entitlements` + kuota grup (`LimitsFor`, satu-satunya tempat kuota), checkout langganan lewat penyedia bayar stub QRIS, pesanan, tonton iklan. 7 route + webhook publik `POST /payments/{payment_id}/webhook`.
- `internal/completion`: progres blok `interactive_web` (XP mengikuti kurva kuis, sekali untuk blok eksplorasi, streak + pencapaian + event `module_item_completed`), gerbang penyelesaian item (akurasi + mastery) dan lewati-berbayar.
- **Kait terisi**: `assessment.OnActivity` dan `question.OnActivity` → `gamification.Activity`. Sekarang satu-satunya kait kosong dari tiket sebelumnya adalah penilaian AI esai/suara (G10).
- **Kait yang menunggu**: `economy.ActivateParePremium`. Webhook untuk pesanan `pare_premium` membalas 500 di Go sampai tiket Pare; pesanan langganan dan pesanan kelas (sejak G7) berjalan penuh.
- **Bug Rust yang ditemukan**: mengulang checkout langganan selagi pesanan sebelumnya masih `pending` gagal 500. Sudah **diperbaiki** di Go — lihat "Bug Rust yang diperbaiki di Go" #6.
- Test: gamifikasi alur penuh (misi dibayar sekali, lima pencapaian, liga `silver` 36,1, leaderboard + alias + persentil, skor global berdasarkan komposit bukan XP mentah) + unit skor komposit/tier; ekonomi (bebas → checkout tanpa hak → webhook sekali → `pro` + 300 Diamond → belanja → kedaluwarsa disapu sekali → periode lewat kembali bebas → iklan sekali pakai); blok interaktif (gagal/lulus/turun/naik = 0/20/0/1 XP, eksplorasi sekali, 5 penolakan) dan gerbang (tak bergerbang, separuh, selesai alami, lewati 402 → 15 Diamond → gratis diulang).
- `paritydiff` `parity/g6-gamification.txt` (9 permintaan, 8 identik) dan `parity/g6-economy.txt` (19 permintaan, 16 identik), masing-masing sebagai beberapa pengguna; semua beda adalah teks galat yang sudah dikenal. Jumlah baris transaksi/pesanan/event/XP dev tidak berubah.
- **Batas pembanding:** dev tidak punya langganan, tidak ada XP dalam 7 hari terakhir (leaderboard terbanding dalam keadaan kosong), tidak ada progres blok interaktif maupun lewati-berbayar. Jalur tulis (checkout, webhook, iklan, skor blok, lewati) hanya teruji lewat test Go.

### Catatan G5 (mesin belajar)

- `internal/learning/mastery.go` (rumus mastery ADR-0002: bobot kebaruan × kesulitan, kepercayaan `n/n_min`; `GET /mastery/{id}`, rincian dua tingkat, Rescue Mode ADR-0012), `frss.go` (jadwal ulang SM-2 ADR-0003, antrean ulang, antrean belajar gabungan dengan eskalasi prasyarat, variasi tipe soal), `clientevents.go` (`POST /events`: batas 50 per batch, 600 per menit lewat Redis yang gagal-terbuka, jendela 7 hari, daftar putih kanal klien, idempoten, gerbang consent).
- **Kait yang kini terisi**: `assessment.OnConceptAnswers` → `learning.ConceptAnswers`; `question.OnConceptReviewed` → `learning.ConceptReviewed`; `question.RescueStatus` → `learning.RescueStatus`. Submit asesmen dan cek satu soal sekarang menghitung ulang mastery, memajukan jadwal ulang, dan memicu rescue seperti Rust.
- Kait yang **masih kosong**: penilaian AI esai/suara (G10) dan pencapaian + misi harian (G6).
- Beda yang disengaja: antrean belajar Rust mengumpulkan entri di `HashMap`, jadi urutan entri berprioritas sama (dan prasyarat mana yang diperiksa lebih dulu) acak antar permintaan; Go memakai urutan temuan yang tetap. Isi dan prioritasnya sama.
- Test: seluruh unit test `mastery.rs` dan `frss.rs` diport (rumus, tabel lima siklus, batas ease, lantai interval) + nama partisi; satu test integrasi alur penuh (skor ditahan di bawah ambang kepercayaan, jawaban tak ternilai tidak dihitung, tiga salah beruntun memicu rescue dengan saran item, rincian bertingkat + tanda lemah, jadwal `forgot` satu hari dibulatkan ke jam, jeda 4 jam, saran soal bertipe beda lebih dulu, antrean belajar: lemah diblokir prasyarat tak dikenal yang menjadi kritis, due + lemah = kritis, batas limit); batch event klien (11 kasus: tercatat, ulang-kirim idempoten, tujuh jenis penolakan dengan pesannya, tanpa consent dilewati).
- `paritydiff` `parity/g5-learning.txt` sebagai tiga pengguna (pemilik baris mastery, pelajar, pengembang): 27 permintaan, 23 identik; empat beda adalah teks galat parameter/body yang sudah dikenal. Jumlah baris `learning_events` / `masteries` / `frss_schedule` dev sama sebelum dan sesudah.
- **Batas pembanding:** database dev hanya punya 1 baris mastery, 1 jadwal ulang, 6 konsep, dan 0 prasyarat, jadi antrean, rincian bertingkat, rescue yang terpicu, dan penulisan event klien hanya teruji lewat test Go, bukan terhadap Rust.

### Rincian G4 (kuis: soal, kertas soal, attempt, penilaian)

| Sub | Isi | Status |
|---|---|---|
| **G4a** | Mesin penilaian murni: `answer_match.rs` + `grading.rs` + `quiz_score.rs` → `internal/grading`; pembangun kertas soal `quiz_paper.rs` + `apportion` → `internal/quiz/paper.go` | ✅ 2026-10-05 |
| **G4b** | `learning_event` + `answer_facts` → `internal/learning`; siklus attempt `assessment.rs` + `exam_session.rs` + `evaluation.rs` + submit kuis & penilaian manual `quiz_attempt.rs` → `internal/assessment` (9 route: `/assessments` ×2, `/assessments/{id}/attempts`, `/assessments/{id}/exam-sessions`, `/exam-sessions/{id}`, `/lessons/{id}/attempts`, `/attempts/{id}/submit`, `/attempts/{id}/grade`, `/module-items/{id}/pending-reviews`) | ✅ 2026-10-05 |
| **G4c** | Bank soal `question.rs` + `question_schema.rs` + QA soal (`content_qa::run_question_qa`) → `internal/question` (10 route: `/question-banks` ×2, `/question-banks/{id}/questions` ×2, `/questions/{id}`, `/stem`, `/submit-review`, `/publish`, `/reject`, `/check`) | ✅ 2026-10-05 |
| **G4d** | Checkpoint bagian `section_checkpoint.rs` → `internal/assessment/checkpoint.go` (5 route); taksonomi kuis + templat kuis → `internal/quiz/template.go` (4 route: `/quiz-taxonomy`, `/quiz-templates`, `/quiz-templates/{id}`, `/quiz-templates/{id}/apply`) | ✅ 2026-10-05 |

Catatan G4a:

- `internal/grading/match.go` (pencocok teks longgar: glyph, `%`, artikel, tanda hubung, angka↔kata, desimal Indonesia/Inggris, kunci berupa angka JSON, bank kata berlabel), `typed.go` (amplop bertipe `{"index": 2}` untuk bank soal lama; persamaan nilai meniru `serde_json::Value` — bilangan bulat tidak pernah sama dengan pecahan), `score.go` (skor per soal `quiz_config`: bobot opsi TKP, set-jawaban dengan nilai parsial, perlu-evaluasi, susun-ulang, teks longgar, kunci eksak).
- `internal/quiz/paper.go`: undian berstrata (grup × Bloom) dengan jatah `Apportion`, utamakan soal yang belum dilihat, giliran antar bagian sumber, rantai `order_locked` utuh, `choices_fixed` dihormati, huruf pilihan mengikuti posisi, penomoran ulang 1..N hanya untuk kertas datar, terjemahan jawaban dan pembahasan ke huruf yang tampil.
- **Generator acak kertas tidak disamakan dengan Rust (`StdRng`/ChaCha12), dan itu disengaja**: kertas dibangun sekali saat attempt dimulai, disimpan di `attempts.paper`, lalu selalu dibaca ulang dari sana. Kertas yang sudah dibuat Rust tetap dibaca apa adanya (bentuk JSON `Paper`/`PaperQuestion` sama); hanya kertas baru yang diundi generator Go (PCG, tetap deterministik per `attempt_id`).
- Test: seluruh unit test Rust keempat berkas diport (21 + 9 + 14 + 7 kasus), ditambah kasus tepi (kunci `null`/boolean, angka negatif, awalan label, `1.0` ≠ `1`), dan test kertas dijalankan atas 20 benih, bukan satu. Belum ada route, jadi belum ada `paritydiff` untuk G4a; paritas ujung-ke-ujung datang bersama submit di G4b.

Catatan G4d:

- Alat baru `cmd/tools/devtoken <user-id> <email>`: mencetak access token dev berumur 30 menit untuk pengecekan manual dengan `curl`.

- Checkpoint: status per bagian (`none`/`locked`/`open`/`reread`/`passed`), undian 2 soal dari pool bagian, submit dinilai di server, salah → wajib baca ulang (15 detik per menit baca, minimal 30 detik) lalu undian baru yang mengutamakan soal belum dilihat, XP 2 per soal sekali seumur hidup, semua checkpoint lulus → artikel selesai. Pratinjau penulis (undi + nilai) tidak menyimpan apa pun.
- **Katalog templat dan kosakata taksonomi tidak diketik ulang.** 65 templat ujian dan tabel taksonomi adalah data tetap, jadi disimpan sebagai JSON yang persis dilayani Rust (`internal/quiz/data/templates.json`, `taxonomy.json`, diambil dari image `titian-backend-rust:prod`; kedua berkas sumber Rust tidak berubah sejak sebelum image itu dibuat) dan di-embed. `ApplyTemplate` diport sebagai kode. Mengubah templat sekarang berarti mengubah berkas JSON itu; `TestEveryTemplateIsValid` menjaga subtype dan referensi bagian tetap sah.
- Yang **belum** diport dari `quiz_taxonomy.rs`: `Stage`, `target_spread`, `prompt_rules`, `stem_readability` — hanya dipakai generator AI, masuk G10.
- Test: checkpoint gerbang-per-bagian (urutan, undian tidak diundi ulang, salah → kunci → terlalu cepat → undian baru tanpa soal lama → lulus, bagian tanpa checkpoint bebas, selesai di checkpoint terakhir, event/fakta/percobaan/XP), pratinjau tanpa jejak, 65 templat sah + terapan lolos `ValidateStructure`, penomoran 1..N.
- `paritydiff` `parity/g4-checkpoints-templates.txt` sebagai pelajar yang punya progres checkpoint: **150 permintaan, 150 identik** — taksonomi, daftar templat, detail dan hasil terapan ke-65 templat, status checkpoint dua artikel, dan semua penolakan.
- **Catatan jujur soal uji paritas:** daftar itu saya jalankan juga sebagai pengguna pengembang, dan ternyata tidak bebas-tulis untuk pengguna tanpa progres — `GET .../checkpoints` menyimpan undian pertama, lalu satu `POST .../checkpoint` benar-benar dinilai oleh Rust (Go kemudian menjawab 422 "perlu baca ulang", yang memang benar untuk keadaan itu). Akibatnya 2 baris progres, 2 event, dan 2 fakta jawaban tertulis untuk akun pengembang di database dev; semuanya sudah saya hapus, dan baris progres milik pelajar tidak tersentuh. Baris `POST` itu sudah dibuang dari daftar dan kepala berkasnya kini menyebut harus dijalankan sebagai pelajar yang sudah punya progres.
- Submit checkpoint yang berhasil dan pratinjau belum terbanding dengan Rust (menulis ke akun dev); hanya lewat test Go.
- Handler checkpoint Rust memakai `Json` biasa, jadi body yang rusak dibalas teks polos; Go membalas amplop `invalid_json_body` (status sama).

Catatan G4c:

- `internal/question/schema.go`: 13 bentuk validator untuk 28 tipe soal; teks galat sama persis dengan Rust (termasuk awalan lama `type=mcq` / `type=fill_blank` dan daftar field tak dikenal yang terurut). Satu beda yang disengaja: bila beberapa penugasan `assignments` salah sekaligus, Rust melaporkan salah satunya secara acak (iterasi `HashSet`), Go selalu melaporkan yang pertama menurut urutan `items`/`passages`.
- `question.go`: bank, buat soal (selalu draf), baca detail vs baca aman-pelajar (`/stem`), daftar berhalaman, alur review (QA tidak pernah menghalangi transisi), `check` satu soal (event `question_answered`, XP per kategori keterampilan, streak), draf OCR untuk G10 (`InsertOCRDraft`), `ConceptIDsForQuestions` untuk G6.
- **Kait untuk domain yang belum diport**: `RescueStatus` (Rescue Mode, ADR-0012) dan `OnConceptReviewed` (mastery + FRSS) → G5; `OnActivity` (pencapaian + misi harian) → G6. Sampai tersambung, `check` tetap menilai, mencatat event, dan membayar XP, tetapi `rescue_triggered` selalu `false` dan mastery tidak dihitung ulang.
- Test: 39 kasus validator (semua bentuk, jalur lolos dan gagal) + satu test integrasi alur penuh (izin, 422 field wajib yang boleh `null` tapi tidak boleh absen, draf tersembunyi dari pelajar, halaman + filter status, review → tolak → review dengan laporan QA bermasalah → terbit, stem tanpa kunci, `check` salah memicu rescue lewat kait, `check` benar, XP dan event).
- `paritydiff` `parity/g4-questions.txt` sebagai pengembang kurikulum dan sebagai pelajar: 27 permintaan, 22 identik (termasuk empat 422 skema dengan teks galat yang sama). Lima beda semuanya teks galat parameter/body yang sudah dikenal. Database dev hanya punya 15 soal, semuanya `published`, jadi jalur draf/review dan `check` yang berhasil hanya diuji lewat test Go.
- Bug paginasi daftar soal semula ikut diport, lalu **diperbaiki** — lihat "Bug Rust yang diperbaiki di Go" #2.

Catatan G4b:

- `internal/learning`: registri tipe event (13 tipe, kanal server/klien, validasi payload, gerbang consent, idempotensi `client_event_id`), `ItemCompleted` (sekarang tersambung ke kait `module.Service.OnItemCompleted`, jadi setiap penyelesaian item menulis `module_item_completed` seperti di Rust), `RecordFacts`, serta jaring pengaman partisi bulanan + retensi 24 bulan yang dipanggil saat API Go menyala (sama seperti `main.rs`).
- `internal/assessment`: mulai attempt (asesmen biasa dan item kuis dengan kertasnya), lanjutkan attempt yang sedang berjalan dengan kertas yang sama, pintu pratinjau terpisah dari pintu pelajar, batas `max_attempts`, bank sumber `question_pool`, submit asesmen (snapshot soal, event per soal, jawaban wajib), submit kuis (terjemahan jawaban dari huruf yang tampil, kunci + pembahasan dalam huruf kertas, event, fakta jawaban, penyelesaian item, tutup sesi proctor), antrean dan penilaian manual, sesi ujian berwaktu.
- **Tiga kait untuk domain yang belum diport** — sampai itu tersambung, perilaku Go berbeda dari Rust di titik ini saja:
  - `EvaluateRubric` (G10, AI): soal `ai_rubric` (esai, rekaman suara) belum dinilai, jadi dihitung 0 dari 1 — sama seperti cabang "penyedia gagal" di Rust.
  - `OnConceptAnswers` (G5): `mastery::recompute_for_concept` + `frss::record_review` setelah submit asesmen.
  - `OnActivity` (G6): `achievement::check_and_award` + `daily_mission::record_progress`. XP dan streak **sudah** berjalan sungguhan.
- Test integrasi (5): attempt kuis dimulai/dilanjutkan/dinilai/dibayar (acak pilihan aktif, hasil dalam urutan dan huruf kertas, submit kedua 409, event + fakta + skor gerbang + XP sekali, retake lebih buruk tidak dibayar, retake lebih baik dibayar kecil); penjagaan mulai + pratinjau tidak meninggalkan jejak + batas percobaan; kuis berbank (undian 5 dari 12, fakta menunjuk bank pemilik soal, retake tanpa soal berulang, bank hilang → 422); soal manual menunggu guru lalu dilebur ke skor (33,3 → 48,0), satu vonis tidak menghapus saudaranya, event `question_graded` atas nama siswa; asesmen biasa + sesi ujian (409 membawa `attempt_id`, jawaban kurang, kait konsep, XP 20, sesi `submitted`, `level_assessment` → galat jujur). Test `internal/learning` (4): registri, consent + idempotensi, penyelesaian + partisi + retensi, fakta jawaban.
- `paritydiff` `parity/g4-attempts.txt` sebagai dua pengguna: 24 permintaan, 20 identik — termasuk **melanjutkan tiga attempt yang sedang berjalan, yang kertasnya dibuat Rust dan dibaca Go apa adanya**. Empat beda semuanya teks `detail` galat (posisi baris/kolom, pesan UUID).
- **Penilaian dibandingkan ujung-ke-ujung lewat sesi pratinjau** (tidak menulis XP/event): tiga kuis dev (5, 16, 12 soal; pilihan ganda + true/false/not given) disidangkan dan disubmit dengan jawaban yang sama di Rust lalu di Go. Kertas identik, hasil penilaian identik (kecuali `1.0` vs `1`), dan baris `attempts` yang tersimpan identik (jawaban, skor, snapshot, versi konten, kertas). Enam sesi pratinjau uji itu dihapus lagi; jumlah baris `attempts` dev kembali seperti semula.
- Yang **belum** terbanding dengan Rust: submit oleh pelajar sungguhan (menulis XP/event ke akun dev), kuis dengan acak/undian (generator berbeda dengan sengaja, lihat G4a), penilaian manual, dan submit asesmen bank soal lama — semuanya hanya lewat test Go.
- Izin antrean penilaian manual semula diport apa adanya (`attempt:submit`), lalu **diperbaiki** — lihat "Bug Rust yang diperbaiki di Go" #5. Submit + efek sampingnya bukan satu transaksi.

Catatan G3f:

- `internal/canon`: `questions.go` (pemilihan soal per langkah, penilaian, hitungan bank → langkah), `path.go` (mapel, tangga Tahap, unit per level, jalur belajar, simpul, unit topik, ringkasan bank), `session.go` (mulai/baca/jawab/selesai), `routes.go`. Route `/catalog` milik registri tetap di `internal/catalog`.
- **XP dan streak diport sungguhan**, bukan lewat kait: `internal/gamification/xp.go` (`AwardXP` idempoten per `reference`, `RecordActivity` + aturan freeze, `SkillXP`, `QuizXP`) beserta unit test `xp.rs`/`streak.rs`. Route gamifikasi dan sisanya tetap di G6.
- Generator acak xorshift dan pengocokan Fisher-Yates diport bit demi bit (`seed` = uuid bab), semua pengurutan stabil seperti `sort_by_key` Rust. **Dibuktikan langsung**: tiga sesi latihan (`latihan_2`, `transfer`, `pemanasan`) dimulai di Rust dan Go untuk bab yang sama — isi `canon_sessions.questions` identik (urutan dan payload). Enam baris sesi uji itu (belum dijawab) dihapus lagi dari database dev. Ujian akhir memang acak tiap kali, jadi hanya diuji lewat sifatnya (12 soal, lintas fungsi).
- Soal disimpan ke sesi dengan angka apa adanya (`json.Number`), jadi salinan soal di sesi sama dengan yang di bank.
- Test: 15 unit test Rust diport (langkah, soal ulangan, bank tanpa tag, isi ulang pemanasan/transfer, tiga jenis soal, kunci tidak bocor) + pin aliran RNG; test integrasi: tangga mapel + jendela unit, penjagaan mulai sesi (langkah tak dikenal, unit `soon`/`locked`, konteks asing, sesi orang lain), latihan (umpan balik sekali, XP sekali per soal, soal salah kembali bertanda di langkah berikut, main ulang tidak membayar dua kali, streak tercatat), ujian (tanpa bocoran selama berjalan, gagal lalu lulus, 120 XP sekali, unit berikutnya terbuka dan unit tanpa bank dilewati), bundel jalur belajar (alias, judul yang ditahan `canon_held_titles`, jejak, konteks sesi).
- `paritydiff` `parity/g3-canon.txt` sebagai pelajar yang punya progres sungguhan (5 unit, 18 sesi): 34 permintaan, 31 identik — termasuk `POST .../finish` pada sesi yang sudah selesai (jalur "laporkan ulang tanpa membayar"). Tiga beda semuanya bentuk pesan galat: id path bukan UUID (400 teks polos, sudah dikenal) dan **body JSON tidak lengkap pada `POST /catalog/units/{id}/sessions` dan `.../answer`** — handler Rust ini memakai `Json` biasa (bukan `ValidatedJson`), jadi membalas 422 teks polos; Go membalas 422 dengan amplop `invalid_json_body` seperti route lain. Status sama.
- Yang **tidak** terbanding dengan Rust: jawab + selesai pada sesi baru (menulis XP/progres ke akun dev sungguhan) — hanya lewat test Go.
- Catatan perilaku yang ikut diport: `GET` jalur bisa menulis (`bab_bank_stats` dihitung saat pertama dibaca); `answer` + `finish` bukan satu transaksi.

Catatan G3e:

- `internal/module/label.go`, `learningpath.go`, `heatmap.go`, `report.go`; route heatmap kelas di `internal/class` lewat kait `class.Service.Heatmap`.
- Test baru: label idempoten + rollup + pencarian balik + pratinjau publik; **sinkron jalur belajar** (sinkron pertama, sinkron kedua tanpa perubahan, lalu topik diganti nama/ditambah/kehilangan label — baris referensi topik yang diganti nama dipertahankan, bukan dibuat ulang); landing publik dangkal dengan `has_more` dan label lewat referensi; cache landing segar seketika setelah kurikulum diedit; 11 pemeriksaan kurikulum; laporan konten yang jatuh ke bank pemilik soal (bukan ke kuis pengundi); heatmap dengan fakta jawaban sungguhan. Unit test `settle`/`child_of` Rust diport.
- `paritydiff`: `parity/g3-labels.txt` (30 permintaan; payload landing 423 KB identik byte-ukurannya) dan `parity/g3-heatmap.txt` + heatmap kelas sebagai guru — sama dengan Rust kecuali body 400. **Catatan jujur:** database dev tidak punya baris `question_answer_facts`, jadi heatmap hanya terbanding dalam keadaan kosong; isi heatmap diuji lewat test Go dengan data buatan, belum dibandingkan dengan Rust.
- Disiapkan untuk G11: `module.Service.HeatmapForPlatform` (heatmap Admin Pusat dari rollup harian), `ResolveItemContext`, `FindQuestion`/`FindCheckpointQuestion`, `Excerpt` — dipakai tiket konten admin (`/admin/content-tickets*`, 3 route) dan `/admin/learning/heatmap`.
- `sync_all` di Rust tidak memeriksa izin bila tidak ada jalur berspesifikasi (izin dicek di dalam `sync_path`); perilaku itu ikut diport.

Catatan G3d:

- `internal/module/proctor.go`, `rules.go`; `class.Service.GateStatus`. 4 unit test proctor Rust diport; test integrasi baru untuk gerbang "dinilai tutor" (kunci → selesai → setujui → terbuka → tarik persetujuan → terkunci lagi), checkpoint yang menahan tombol "Selesai", serta alur proctor lengkap (jenjang konfigurasi, kunci otomatis setelah 2x pindah tab, tidak bisa diakali dengan membuka ulang, buka kunci oleh tutor, kartu identitas, geofence).
- `paritydiff` (`parity/g3-rules.txt`, 30 permintaan, sebagai penyusun dan sebagai siswa): **0 beda**.
- Dipindahkan: 5 route checkpoint bagian (`section_checkpoint`: state, submit, reread, preview, preview/grade) → **G4**, karena memakai penyusun kertas soal dan penilai (`quiz_paper`, `quiz_score`, `answer_match`). Aturan "checkpoint harus lulus sebelum artikel bisa ditandai selesai" sudah aktif di Go (`CompletionAllowed`). Route progres blok interaktif → **G6**, karena memberi XP/streak/pencapaian.
- Kait untuk G4: `module.Service.ProctorSessionForSubmit` dan `CloseProctorSession` (menolak pengumpulan kuis berpengawas yang tidak lewat halaman kuis) sudah ada, dipanggil saat pengumpulan attempt diport.
- Lebih longgar dari Rust: `after_count`/`max_violations` bernilai `3.0` diterima sebagai 3 (serde menganggapnya bukan bilangan bulat dan mengabaikan aturannya).

Catatan G3b–G3c:

- Paket baru: `internal/quiz` (`subtype.go`, `config.go`, `schema.go`, `flatten.go`), `internal/lessonplan`, `internal/content/canonical.go`; `internal/module` bertambah `item.go`, `share.go`, `version.go`. Tabel 40 subtipe dibangkitkan dari tabel Rust, bukan diketik ulang.
- Test: unit test Rust untuk `quiz_config` (13), `quiz_config_schema` (20), `quiz_subtype` (5), `lesson_plan` (11), guard (5) diport dengan kasus yang sama. Rust tidak punya test integrasi untuk item modul; test Go ditulis baru, termasuk **siswa tidak pernah menerima kunci jawaban** (kuis dan checkpoint), kunci guard di pohon dan saat item dibuka lewat URL, versi beku saat terbit, duplikat subpohon, berbagi editor.
- `paritydiff` (`parity/g3-items.txt`, 47 permintaan data dev, dijalankan sebagai penyusun kurikulum **dan sebagai siswa**): detail item dengan `quiz_config` dan `lesson_plan` sungguhan identik dengan Rust untuk kedua peran.
- Route `module.rs` yang belum: `speaking-prompt-audio` (butuh TTS, G10), `completion-status` / `skip-completion` (`module_completion`, butuh kredit, G6), `pending-reviews` (G4), `quiz-taxonomy` / `quiz-templates*` (G4), sisanya G3d–G3e.
- Kait baru yang disambungkan nanti: `module.Service.OnQuizConfigSaved` → penyegaran ringkasan bank bab (`canon_path::refresh_stats_for_quiz_item`) — **tersambung di G3f** (`cmd/api/main.go`).
- `quiz_config` yang disimpan lewat Go bisa berbeda **bentuk teks** dari Rust untuk nilai yang sama: angka pecahan bulat ditulis `1` (bukan `1.0`). Nilainya sama; hash konten versi dihitung dari bentuk kanonik yang meniru Rust (`CanonicalJSON`), dengan celah yang dicatat di komentarnya (bilangan sangat besar/kecil berbentuk eksponen).
- Lebih longgar dari Rust: field string ber-`default` yang dikirim `null` diterima sebagai kosong (serde menolaknya).
- **Bug Rust yang ikut diport**: `POST /modules/{id}/items` dengan `content` yang gagal diparse membalas 422 **setelah** baris item dibuat, jadi item kosong tertinggal. Dicatat di Pasca-cutover.

Catatan G3a:

- `internal/module` (pohon, `progress.go`, `guard.go`) dan `internal/content` (`paste.go`, `alm.go`, `schema.go`). Unit test Rust untuk parser ALM (11) dan guard (5) diport dengan kasus yang sama; test skema blok dan test integrasi pohon modul ditulis baru.
- **Attendance Guard dari G2 kini tersambung** (`cmd/api/main.go`): check-in QR lewat Go memeriksa materi berpenjaga, teruji dengan data sungguhan di test.
- `item_progress::record_completion` di Rust juga menulis event `module_item_completed`. Di Go tersedia kait `module.Service.OnItemCompleted`, **disambungkan di G5** (jejak belajar).
- `purge_preview_attempts` (milik `assessment.rs`) diport lebih awal ke `module.PurgePreviewAttempts` karena hapus modul membutuhkannya; G4 memakainya dari sana.
- sqlc tidak bisa menganalisis CTE rekursif yang memfilter kolom hasil (`where id != $1`); query leluhur modul ditulis langsung dengan pgx.
- Penormal tempelan HTML di Rust memakai offset **byte** sebagai offset **karakter** saat mencari tag penutup (keliru untuk teks non-ASCII). Diport apa adanya supaya hasilnya identik; dicatat di Pasca-cutover.
- `paritydiff` (`parity/g3-modules.txt`, 25 permintaan data dev): sama dengan Rust kecuali dua beda yang sudah dikenal.

### G2 — Katalog & kelas ✅ (2026-10-05)

`internal/catalog` (registri kanonik, mapel, prasyarat konsep), `internal/program`, `internal/org/period.go`, `internal/class` (roster, sesi, kehadiran, kartu QR, sinkron Meet), `internal/platform/meeting` (stub + Google Meet + aturan status verifikasi), `internal/platform/dbtype.Date` (kolom `date` ditulis `YYYY-MM-DD`). 26 route.

Test: Rust tidak punya test integrasi untuk domain ini, jadi test Go ditulis baru terhadap perilaku Rust (kelas & visibilitas, sesi, kehadiran manual idempoten, QR pindai guru + check-in mandiri, sinkron Meet, program + urutan modul, periode, mapel, siklus prasyarat). `paritydiff` (`parity/g2.txt`, 35 permintaan terhadap data dev, dijalankan sebagai penyusun kurikulum dan sebagai guru pemilik kelas): sama dengan Rust kecuali body 400 untuk query wajib yang hilang (Rust teks polos) dan teks `detail` 422.

Dipindahkan ke tiket lain karena bergantung pada domain modul/kuis:

- 10 route `canon_path.rs` di bawah `/catalog` (penjelajah jalur belajar + sesi latihan) → G3/G4.
- `GET /classes/{id}/learning-heatmap` dan `GET /org-class-sessions/{id}/gate-status` → G3.
- **Attendance Guard**: check-in QR di Rust ditolak bila materi berpenjaga belum selesai (`item_guard::attendance_blockers`). Di Go lewat kait `class.Service.AttendanceBlockers` — **sudah tersambung sejak G3a**.

Beda kecil: `POST /subjects` di Rust memakai extractor JSON bawaan axum (body rusak → teks polos); di Go memakai `httpx.DecodeJSON` seperti route lain (422 `invalid_json_body`).

### G1 — Identitas & organisasi ✅ (2026-10-05)

`internal/identity` (auth, sesi, profil, avatar, persetujuan data, profil belajar) dan `internal/org` (organisasi & anggota). 18 route. Test: 8 test `auth_test.rs` + 3 test `user_data_consent_test.rs` + 2 test anggota `organization_test.rs` diport, ditambah test rotasi/penggunaan ulang token, akun terhapus, wali untuk jenjang SD/SMP, profil belajar, buat/gabung organisasi, dan kontrak body tak valid. `paritydiff` (`parity/identity.txt`, `parity/org.txt`): 24 permintaan, sama dengan Rust kecuali teks `detail` di atas.

Tertunda:

- `DELETE /users/me`: di Rust menghapus data suara dan foto profil Pare lebih dulu (`pare_voice::purge_user`, `pare_avatar::remove`). Di Go disediakan kait `identity.Service.OnAccountDelete`; kedua kait itu (`PurgeUser`, `RemoveAvatar`) sudah didaftarkan di `cmd/api/main.go` (G14).
- 4 test tutor di `organization_test.rs` (`/organizations/{id}/tutors`, `/tutors/me`) ikut G7, karena route itu milik domain tutor.

Bug Rust yang ikut diport apa adanya (dicatat untuk diperbaiki setelah cutover):

- `GET /organizations/{id}/members` berpaginasi: `next_cursor` diisi id baris pertama halaman berikutnya, lalu halaman berikutnya meminta id yang **lebih besar** darinya, sehingga satu anggota terlewat di tiap batas halaman.

## Bug Rust yang diperbaiki di Go (beda yang disengaja)

Untuk route di bawah ini Go **tidak** lagi sama dengan Rust, dan itu benar. Rust tidak diubah (akan dipensiunkan di G15).

| # | Di mana | Perilaku Rust | Perilaku Go | Test |
|---|---|---|---|---|
| 1 | `GET /organizations/{id}/members` | `next_cursor` menunjuk baris pertama halaman berikutnya, sehingga baris itu terlewat | `next_cursor` = baris terakhir halaman ini; tidak ada yang terlewat | `internal/org` |
| 2 | `GET /question-banks/{id}/questions` | sama seperti #1 | sama seperti #1; test menelusuri semua halaman | `internal/question` |
| 3 | `POST /modules/{id}/items` | konsep tak dikenal atau konten gagal diparse → 422, tetapi baris item kosong tertinggal | baris yang baru dibuat dihapus lagi bila langkah berikutnya gagal | `internal/module` |
| 4 | Penormal tempelan HTML (`format: "html"`) | offset **byte** tag penutup dipakai sebagai offset **karakter**; tempelan non-ASCII (Arab, CJK, huruf beraksen) terpotong di tempat yang salah | pencarian per karakter, tidak peka huruf besar ASCII | `internal/content` |
| 5 | `GET /module-items/{id}/pending-reviews`, `POST /attempts/{id}/grade` | izin `attempt:submit`: siswa boleh, guru ditolak | aturan yang sama dengan daftar "perlu approve tutor": penulis kurikulum + guru kelas yang mempelajari modul itu; siswa dan guru kelas lain 403. Urutan galat `grade` kini: skor tidak sah 422 → attempt tak ada 404 → bukan penilai 403 | `internal/assessment` |
| 6 | `POST /subscriptions/checkout` saat pesanan lama masih `pending` | 500 (status `cancelled` ditolak `orders_status_check`) | pesanan lama ditutup sebagai `failed` (status yang sudah ada, tanpa migrasi); pembayaran lama yang datang terlambat tidak mengaktifkan apa pun | `internal/economy` |
| 7 | Skema soal: beberapa `assignments` salah sekaligus | melaporkan salah satunya secara acak | selalu yang pertama menurut urutan `items` / `passages` | `internal/question` |
| 8 | `GET /products` | `next_cursor` = baris pertama halaman berikutnya, jadi produk itu terlewat | `next_cursor` = baris terakhir halaman ini | `internal/marketplace` |
| 9 | `POST /submissions/{id}/grade` | skor berapa pun diterima, padahal rapor merata-ratakannya dengan persentase kehadiran sehingga skor di luar 0–100 merusak nilai akhir | 422 `invalid_score` di luar 0–100 | `internal/marketplace` |
| 10 | `POST /tutors/{id}/reviews` | tutor di URL tidak pernah dicocokkan dengan tutor kelas itu, sehingga ulasan bisa ditempelkan ke tutor mana pun | 422 `tutor_mismatch` bila enrolmen itu bukan kelas tutor tersebut | `internal/marketplace` |
| 11 | `POST /cohorts/{id}/sessions/{date}/attendance` | menulis entri satu per satu; entri tak sah di tengah daftar → 422 setelah entri sebelumnya tersimpan dan jatah paketnya terpotong | semua status dan enrolmen divalidasi dulu; daftar yang ditolak tidak menyimpan apa pun | `internal/marketplace` |
| 12 | `GET /drive`, `GET /assets` di akar | semua aset tanpa folder milik **siapa pun** tampil ke setiap pengguna | akar hanya menampilkan milik pemanggil (folder: `owner_id`); isi folder tetap lewat izin | `internal/drive` |
| 13 | `DELETE /{assets,folders}/{id}/shares/{share_id}` | `share_id` tidak dicocokkan dengan sumber daya di URL, jadi pemilik A bisa mencabut berbagi milik B | `delete … where id, resource_type, resource_id` cocok semua; selain itu 404 | `internal/drive` |
| 14 | `GET /drive`, `/drive/trash`, `/assets` | `next_cursor` = baris pertama halaman berikutnya (terlewat); `null` bukan `[]` bila kosong | kursor = baris terakhir halaman ini; daftar selalu `[]` | `internal/drive` |
| 15 | `DELETE /folders/{id}/permanent` | 500 bila folder masih berisi aset (FK `assets_folder_id_folders_id_fk`) | aset di dalamnya tetap di sampah pemiliknya tetapi lepas dari folder, lalu folder dihapus | `internal/drive` |
| 16 | Admin atas id yang tidak ada; nama kosong | rename/pindah/pulihkan → 500, hapus → 204 diam-diam, buat folder dengan induk fiktif → 500; nama `"   "` untuk folder/aset diterima | 404 `resource_not_found` bila sumber daya tidak ada (juga untuk admin); 422 `invalid_name` untuk nama kosong | `internal/drive` |
| 17 | Aliran Vertex (`generate_stream`) | tiap bacaan jaringan didekode UTF-8 sendiri-sendiri: karakter multibyte yang terbelah antar-bacaan menjadi U+FFFD | menyangga byte, memecah hanya di batas event SSE | `internal/ai` |
| 18 | `POST /ai/generate-lesson`, `/ai/generate-questions` saat keluaran gagal validasi | alasan dicetak dengan `{e}` pada `AppError`, yang hanya menampilkan nama varian: penulis menerima `detail: "unprocessable_entity"` | `detail` berisi alasan sebenarnya (mis. bagian Konstitusi yang hilang, blok yang ditolak skema) | `internal/ai` |
| 19 | Prompt soal AI dan OCR | contoh bentuk soal dan daftar tipe memakai nama lama `mcq` / `fill_blank` (diganti Phase 37), sehingga tipe yang dipakai sekarang tidak diberi contoh sama sekali, dan tiap butir OCR ditandai "tidak dikenali" lalu disimpan dengan tipe yang tak dipahami bagian lain | contoh dan daftar memakai `multiple_choice` / `gap_fill`; nama lama dari model dinormalkan | `internal/ai` |
| 20 | `ai_tasks.provider` untuk lesson plan / edit / terjemahan / fragmen ALM / generator kuis / usulan tipe / kode web + QA / Live Chat | `"routing"` (nama pengarah) atau `"openrouter"` yang ditulis mati, walau Vertex yang melayani | penyedia yang benar-benar melayani model itu (`vertex` / `openrouter`) | `internal/ai` |
| 21 | Juri QA kode web (`parse_score`) | mengiris dari `{` pertama sampai `}` terakhir tanpa memeriksa urutan: balasan `} {` membuat panik | galat "penilai tidak mengembalikan JSON"; QA menjadi `null` | `internal/ai` |
| 22 | `POST /ai/live-chat-turn/stream` saat klien menutup koneksi di tengah balasan | aliran dibuang tanpa menulis baris `ai_tasks` sama sekali: token terpakai tanpa jejak audit | tetap dicatat (`done` bila sudah ada balasan, `failed` bila belum) | `internal/ai` |
| 23 | `POST /speaking-room/transcribe` dengan `audio_base64` bukan base64 | 500 `internal_error` (kesalahan pemanggil dilaporkan sebagai galat server) | 422 `invalid_audio` | `internal/ai` |
| 24 | `POST /ai/tutor-chat` dengan badan yang salah bentuk | penolakan teks polos bawaan axum, satu-satunya route AI tanpa amplop `{error, detail}` | amplop `invalid_json_body` seperti route lain | `internal/ai` |
| 25 | Daftar isi tutor bebas modul (`parse_outline`) | mengiris `{`…`}` tanpa memeriksa urutan: balasan `} {` membuat panik; peta batas laju per pengguna tak pernah dibersihkan | jatuh ke daftar isi bawaan; jendela batas laju yang kosong dibuang | `internal/ai` |
| 26 | `GET /admin/participants/search?q=` | `%` dan `_` dipakai sebagai wildcard LIKE: mencari `_` atau `%` menampilkan semua pengguna | karakter itu literal | `internal/admin` |
| 27 | Pabrik Konten: panggilan model | `ai_tasks.provider` selalu `"vertex"`, juga untuk model OpenRouter | penyedia katalog model yang menjawab | `internal/contentfactory` |
| 28 | `POST /admin/content-factory/tasks/{id}/review` pada tugas `bab_content` | dibaca sebagai rencana bab: 500 `internal_error` (35 tugas `needs_review` di dev tak bisa ditindak dari dasbor) | setujui = `applied`, tolak = `rejected`, regenerasi = antre ulang (prioritas 60) | `internal/contentfactory/content_test.go` |
| 29 | `POST /pare/premium/checkout` kedua kali (percobaan ulang) | pesanan `pending` lama ditutup dengan status `cancelled`, yang tidak diizinkan `orders_status_check`: 500 | ditutup sebagai `failed` | `internal/economy` |

Diperiksa dan **tidak** diubah karena bukan bug: `POST /learning-paths/sync` tanpa jalur berspesifikasi tidak memeriksa izin (tidak melakukan apa-apa); `answer` + `finish` sesi kanonik dan submit kuis bukan satu transaksi (desain; dicatat di Pasca-cutover).

## Pasca-cutover (tidak dikerjakan selama port)

- Bungkus submit kuis / sesi kanonik beserta efek sampingnya dalam satu transaksi.
- Hapus objek R2 saat aset dihapus permanen (Rust juga tidak pernah menghapusnya) dan beri `/drive` kursor terpisah untuk folder dan aset (satu `next_cursor` bersama masih bisa menggandakan item di halaman berikutnya).
- Posisi umpan balik evaluasi esai/berbicara adalah offset byte (Rust dan Go); bila klien kelak menandai teks, ubah ke unit kode UTF-16 supaya cocok dengan indeks string JavaScript.
- Pertimbangkan status pesanan `cancelled` yang sesungguhnya (migrasi) menggantikan `failed` untuk pesanan yang digantikan.

- **G16** Leaderboard & liga dengan Redis `ZSET` + reset mingguan lewat job, Postgres tetap sumber kebenaran.
- `LISTEN/NOTIFY` untuk worker agar tidak polling 5 detik.
- Pisahkan hub `/ws/pare` jadi service sendiri bila jumlah pemain serentak menuntut.
- Metrik Prometheus (belum ada di Rust juga).
