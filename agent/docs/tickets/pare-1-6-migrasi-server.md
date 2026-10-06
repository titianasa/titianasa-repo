# Pare-1 … Pare-6 — Kampung Bahasa Pare ke arsitektur Titian (ADR-0016)

> **Catatan migrasi backend (2026-10-05, ADR-0020):** backend sedang dipindah ke Go. Tiket ini ditulis untuk `titian-backend-rust`, dan kode Rust tetap yang aktif sampai domain ini diport (G14, lihat `phase-51-go-migration.md`). Pekerjaan yang belum dieksekusi: bila G14 sudah selesai saat tiket ini dikerjakan, kerjakan di `titian-backend-go` (`#[sqlx::test]` → test Go dengan `testdb.New`, `services/x.rs` → `internal/<domain>/`); bila belum, kerjakan di Rust dan catat endpoint/migrasi barunya di daftar paritas fase 51.

📋 **Pare-1 SELESAI (diverifikasi dengan backend dev sungguhan), Pare-2, Pare-3, Pare-4 (kecuali P4-003 dan uji beban) & Pare-5 SELESAI KODE (2026-09-25)** — backend + frontend; verifikasi end-to-end dengan backend dev sungguhan menunggu izin (restart backend 8090 + origin `localhost:4700`). Pare-2 … Pare-6 masih rencana. Dasar keputusan: [ADR-0016](../adr/0016-kampung-bahasa-pare.md) (Accepted, termasuk username).

Repo yang disentuh: `titian-backend-rust` (endpoint `/pare/*`, `/ws/pare`, migrasi `pare_*`, worker push) dan `alr/game` (FE Next.js **mandiri**, di-host sendiri — bukan bagian dari `titian-web`; login Google lewat backend yang sama). `titian-web` hanya disentuh di Pare-6 (tautan & onboarding silang). Nomor fase `Pare-n` / tiket `P<n>-xxx` sengaja tidak memakai 41–50 agar tidak bertabrakan dengan jalur ADR-0013/0015.

---

## 1. Tujuan

- Pemain login dengan akun Google Titian, punya profil game sendiri (onboarding tokoh), dan progresnya awet lintas perangkat.
- **Tidak ada data dinamis & aturan ekonomi di FE**: uang, XP, nyawa, stamina, level, konten soal, harga, misi, chat — semuanya dari server.
- Realtime (saluran, gerakan, chat Umum/Personal/Grup) berjalan di backend Rust dengan perilaku yang sama seperti server Bun sekarang.
- FE tayang di `pare.titianasa.com` (Vercel) sebagai **PWA** dengan **push notification**.

## 2. Yang WAJIB dipertahankan

- Perilaku & angka game saat ini (lihat Context ADR-0016 dan README `game`): saluran 50, batch 10 Hz, aturan bahasa chat (½ nyawa), ekonomi (Rp200/jawaban benar Basic, −5 XP salah, ujian 20 soal Rp50.000/2 percobaan, stamina penuh = +½ nyawa, dll.).
- Kontrak endpoint Titian yang ada tidak berubah. Semua endpoint baru di bawah `/pare/*` dan `/ws/pare`.
- `users` satu-satunya tabel bersama; `pare_*` tidak dibaca oleh XP/liga/mastery Titian, dan sebaliknya.
- Kunci jawaban tidak pernah terkirim ke klien; semua perubahan uang/XP/nyawa lewat `pare_ledger`.
- Teks UI Bahasa Indonesia, gaya pixel-art game tetap (bukan komponen UI Titian).

## 3. Aturan main eksekusi

Sama seperti fase Titian: migrasi aditif dari nomor setelah migrasi terakhir (**0080** saat ini), sinkron `domain-model.md` & `api-contract.md`, test integrasi `#[sqlx::test]` per tiket, verifikasi browser sungguhan (minta izin user sebelum membuat token QA, hapus setelahnya), jangan commit tanpa diminta, waktu harian **WIB**. Port logika TS → Rust wajib disertai **test paritas** (kasus nyata dari test yang sudah dipakai di prototipe: deteksi bahasa, rumus stamina/nyawa, bayaran per level).

---

# Pare-1 — Identitas & profil pemain

## P1-001 — Skema `pare_players` + `pare_lang_progress` + `pare_ledger` (M)

✅ **SELESAI (2026-09-24).** `migrations/0080_pare_players.sql` (idempoten, `if not exists`). Tambahan dari rencana: kolom **`username`** (CHECK `^[a-z0-9_.]{3,20}$`, UNIQUE `lower(username)`) dan **`nickname`** (1–16), CHECK zona/fokus/nyawa kelipatan ½/stamina/kenyang. Diverifikasi: seluruh 81 migrasi berjalan di DB kosong lewat `#[sqlx::test]`. Belum diterapkan ke DB dev (akan dijalankan runner saat backend dev direstart).

Migrasi `0080_pare_players.sql`. `pare_players(user_id PK FK users, display_name, look jsonb, zone, pos jsonb, xp int, money int, hearts numeric(3,1), stamina real, fullness real, focus, violations, streak, last_study, last_seen, sleeping_since, bike_date, laundry_date, created_at, updated_at)`, CHECK hearts 0..5 kelipatan 0,5, money ≥ 0. `pare_lang_progress(player_id, lang, level, lang_xp, level_start_xp, exam_tries)`. `pare_ledger(id, player_id, kind, delta_money, delta_xp, delta_hearts, reason, ref, created_at)`.
**DoD:** constraint diuji lewat insert pelanggar; indeks ledger per pemain+waktu.

## P1-002 — `services/pare_player.rs` + `GET/POST /pare/me` (M)

✅ **SELESAI (2026-09-24).** `services/pare_player.rs`, `handlers/pare.rs`, `routes/pare.rs` (+1 baris registrasi di tiap `mod.rs`). Endpoint: `GET/POST/PATCH /pare/me`, `GET /pare/usernames/{u}` (cek ketersediaan live). Username permanen (PATCH hanya nickname/look). `tests/integration/pare_player_test.rs`: **8/8 lulus** (404 sebelum onboarding, mulai dari nol, onboarding ganda 409, username unik case-insensitive, validasi username/nickname + nama cadangan, cek ketersediaan, PATCH tidak mengubah username, tanpa token 401, onboarding game tidak membuat `user_learning_profiles`).

`GET /pare/me` → profil lengkap atau `404 pare_player_not_found`. `POST /pare/me` (onboarding tokoh: nama 2–16, look tervalidasi sama seperti `cleanLook` server Bun). `PATCH /pare/me/look` (lemari). Pemain baru: Rp0, XP 0, nyawa 5, stamina 100, istirahat 6 jam awal.
**DoD:** test onboarding ganda (409), validasi look, user Titian tanpa profil Pare → 404.

## P1-003 — Origin & OAuth untuk Pare (S)

✅ **SELESAI dokumentasi (2026-09-24).** Tidak perlu kode: CORS sudah dari env `FRONTEND_ORIGIN` (dipisah koma). Langkah backend/Google Console/Vercel dicatat di `gcp-migration-runbook.md` § "Tambahan — Kampung Bahasa Pare". Nilai dev `http://localhost:4700` belum ditambahkan ke `.env` backend (menunggu izin user).

Tambah `pare.titianasa.com`, `localhost:4700`, dan pola preview Vercel ke `allowed_origins` lewat config (bukan hard-code). Catat langkah Google Cloud Console (authorized JS origins) di `gcp-migration-runbook.md`.

## P1-004 — FE: login Google + onboarding tokoh (M)

✅ **SELESAI KODE (2026-09-24).** `alr/game`: `src/lib/api.ts` (access token di memori, refresh token di `localStorage` dan dirotasi, satu refresh bersama untuk 401 serentak), `AccountScreens.tsx` (layar login Google Identity Services + layar muat/galat), `TitleScreen.tsx` jadi onboarding server (username dengan cek live, nama panggilan, penampilan), gerbang di `Game()` (splash → login → onboarding → dunia), papan nama `Nama @username` (juga untuk pemain lain lewat realtime), lemari menyimpan look ke server, tombol "Keluar akun" menggantikan RESET. Env: `.env.example`. Diverifikasi di browser sungguhan dengan API disimulasikan di level jaringan (login → onboarding → cek username terpakai/min 3/tersedia → dunia → muat ulang langsung masuk). Belum: uji dengan backend dev sungguhan + akun Google asli.

`game`: klien API (`NEXT_PUBLIC_API_URL`), store token (akses di memori, refresh di storage aman), alur Layar judul → Login Google → `GET /pare/me` → 404 ⇒ pembuatan tokoh (`POST /pare/me`). Hapus `created/name/look` dari `localStorage`.
**DoD:** browser: akun baru → onboarding → masuk Camp; login ulang di perangkat lain → tokoh sama.

---

# Pare-2 — Konten ke server & penilaian di server

## P2-001 — Skema & seed konten bahasa (L)

✅ **SELESAI dengan penyimpangan yang disengaja (2026-09-24).** Konten TIDAK dijadikan tabel `pare_content_*`: diekspor sekali dari game (`alr/game/scripts/export-content.ts`) ke `titian-backend-rust/data/pare/content.json` (157 KB, 32 KB gzip; 5 bahasa × Basic + Level 1 + tangga level) dan dikompilasi ke binary (`services/pare_content.rs`, `include_str!`). Alasan: konten statis, ikut deploy backend, tanpa migrasi/seed, ETag otomatis dari hash berkas, tanpa DB per permintaan. Editor konten berbasis DB bisa menggantikannya kelak tanpa mengubah API.
`pare_content_vocab`, `pare_content_phrases`, `pare_content_situations`, `pare_content_grammar`, `pare_content_concepts`, `pare_levels` (tangga per bahasa, topik, can-do), semua dengan `uid` stabil & `level`. Binary `seed_pare_content` membaca berkas yang sekarang di `game/src/game/content` (diekspor ke JSON sekali) dan meng-upsert. `content_version` untuk ETag.

## P2-002 — Endpoint konten baca (cacheable) (S)

✅ **SELESAI.** `GET /pare/content` publik (satu berkas untuk semua bahasa + tangga level), ETag + `Cache-Control: public, max-age=300, stale-while-revalidate=86400`, `If-None-Match` → 304. (Tidak dipecah per bahasa/level: 32 KB gzip cukup kecil; CDN menyimpannya.)
`GET /pare/content/{lang}/dictionary?level=` (kata/frasa/konsep **tanpa** data kunci soal), `GET /pare/levels/{lang}`. Header `Cache-Control: public, max-age=300, stale-while-revalidate` + `ETag`.

## P2-003 — Kertas soal & penilaian (L)

✅ **SELESAI.** `services/pare_lesson.rs` (port `lesson.ts`: kelas 6 peran, pasar, perpustakaan/meja belajar, club, memancing, 6 tantangan, ujian 20 soal, kesempatan terakhir), `services/pare_paper.rs` (buat/jawab/bantuan/selesai), `pare_economy.rs` (aturan uang/XP, ledger, promosi). Kunci tersimpan di `pare_papers.questions`, tidak pernah dikirim sebelum dijawab; jawaban ganda 409, kertas orang lain 404, ronde berwaktu ditutup di server. Test integrasi `tests/integration/pare_learning_test.rs` (11 test) + unit test builder.
Port `lesson.ts` (buildLesson, marketLesson, reviewLesson, clubLesson, buildChallenge, buildExam, fishQuestion) ke `services/pare_lesson.rs`. `POST /pare/papers` (jenis: class/role, activity, challenge, exam, lastchance) → `paper_id` + soal tanpa kunci; `POST /pare/papers/{id}/answers` → nilai, delta XP/uang (bayaran per level bahasa, bantuan = ½, salah −5 XP dengan lantai level) lewat ledger; `POST /pare/papers/{id}/finish` → bonus sempurna, `pare_daily`, kenaikan level otomatis (readiness) atau hasil ujian.
**DoD:** paritas angka dengan prototipe; kunci tak ada di respons; jawaban ganda/replay ditolak.

## P2-004 — Level & ujian lompat level (M)

✅ **SELESAI.** Kesiapan (`pare_economy::readiness`), promosi otomatis di akhir kertas & event chat, ujian: biaya + 2 percobaan + jeda 60 menit + lulus ≥ 17/20 (diuji), `GET /pare/levels`.
Readiness (80% kata dikuasai + poin ≥ 150×(level+1)), `promote` (+Rp1.000 × level baru), ujian: bayar `examFee(level)` = 50.000 + 25.000×level untuk 2 percobaan, jeda 60 menit, 20 soal lulus ≥ 17, tanpa XP/uang per soal.

## P2-005 — Misi harian (S)

✅ **SELESAI.** `services/pare_daily.rs`: hash & templat identik dengan game (tes paritas 4 tanggal nyata), `GET /pare/daily`, `POST /pare/events` untuk kejadian yang masih dilaporkan game (park, meal, visit, buy, chat, photo, violation). ⚠️ Sementara: kejadian ini masih dilaporkan klien; server hanya menjaga batas & hadiah. Pare-3 (hidup) dan Pare-4 (chat) memindahkannya ke server.
Port `quests.ts`: misi sama untuk semua per tanggal WIB (hash tanggal), counter di `pare_daily`, klaim otomatis +30 XP & Rp500.

## P2-006 — FE: semua pelajaran lewat API (M)

✅ **SELESAI kode (2026-09-24)** — `LessonModal`, memancing, tantangan, ujian, kelas, misi, level & foto lewat API; `recordAnswer`/`completeLesson`/`promotePatch`/`buildLesson`… dihapus dari FE; HUD hanya menampilkan angka dari server (`src/game/server.ts`). Diverifikasi di browser (API disimulasikan) untuk alur ujian penuh. **Belum**: (1) `src/game/content/*` masih di bundle karena Kamus & aturan bahasa chat memakainya — pindah ke `GET /pare/content` bersama Pare-4 (aturan bahasa server-side); (2) angka aturan untuk tampilan ("+10 XP · Rp200") masih konstanta FE (server yang membayar); (3) hidup (nyawa/stamina) & pembelian masih simulasi lokal (Pare-3), pembelian dilaporkan lewat `POST /pare/spend`.
LessonModal/Challenge/Exam/Fishing/Kamus/LevelPanel memakai endpoint Pare-2. Hapus `recordAnswer`, konten `src/game/content/*` dari bundle (kecuali data tampilan statis), dan angka ekonomi dari FE.

---

# Pare-3 — Simulasi hidup otoritatif

## P3-001 — `services/pare_life.rs` (M)

✅ **SELESAI (2026-09-24).** `services/pare_life.rs`: port `life.ts` (kenyang, lapar, kurang tidur, langkah, stamina penuh = +½ nyawa, pingsan, idle ≥ 1 jam, tidur), dihitung malas dari `last_seen`. 8 unit test paritas (angka sama dengan game) + test integrasi jam-demi-jam (`tests/integration/pare_life_test.rs`, 8 test). Penyesuaian: absen < 1 jam kini tetap dihitung sebagai waktu bermain (game lama mengabaikannya) — konsekuensi perhitungan malas.
Port `life.ts`: kenyang turun per waktu, lapar/kurang tidur menguras stamina, stamina penuh = +½ nyawa (turun ke 70), stamina habis = −½ nyawa & pingsan ke Camp, idle ≥ 1 jam = istirahat di Camp. Dihitung **malas** dari `last_seen` saat setiap baca/aksi. Test paritas jam demi jam.

## P3-002 — Aksi kehidupan (M)

✅ **SELESAI.** `POST /pare/tick`, `GET /pare/menus/{zone}/{venue}`, `POST /pare/shop/buy`, `/laundry`, `/bike`, `/park`, `/sleep`, `/wake`. Menu & harga di `content.json` (`menus`, `prices`), diskon level dihitung server, semua lewat ledger; endpoint sementara `/pare/spend` dihapus. Bedanya dengan rencana: `tick` menggantikan `/pare/steps`; `zone`/`pos` masih dilaporkan game sampai Pare-4.
`GET /pare/menus/{zone}` (menu & harga dari server), `POST /pare/shop/buy`, `/pare/laundry`, `/pare/bike`, `/pare/park`, `/pare/sleep`, `/pare/wake`. Diskon level kampung dihitung server. Semua lewat ledger.

## P3-003 — FE: HUD & modal hidup dari server (S)

✅ **SELESAI kode.** `life.ts` kini hanya klien API; `tickLife`/`spendSteps`/`startSession`/konsumsi lokal dihapus. HUD, toko (menu dari server), laundry, sepeda, taman, tidur/bangun, papan info memakai `PlayerView.life`; game memanggil `tick` tiap 20 dtk (langkah dihitung server), saat pindah zona dan saat tab kembali terlihat; boot memakai posisi dari server. Menu & harga dihapus dari `zones.ts`. Diverifikasi di browser (API disimulasikan): boot tick → menu → beli → pesan & uang dari server → tick membawa langkah.
HUD membaca `GET /pare/me` + event WS; hapus `tickLife`/`spendSteps` lokal (stamina langkah dari server, Pare-4).

---

# Pare-4 — Realtime di Rust

## P4-001 — `services/pare_hub.rs` + `/ws/pare` (L)

✅ **SELESAI kode (2026-09-24), uji beban BELUM.** `services/pare_hub.rs` (hub mandiri-transport, dites tanpa socket) + `handlers/pare_ws.rs` (WebSocket tipis, token di query seperti `canvas_ws.rs`). Sama dengan server Bun: saluran maks 50 terisi-dulu, batch `moves` per saluran, 16 gerakan/dtk, antrean keluar 256 (backpressure), satu koneksi per pemain, `/pare/stats` (perlu login, bukan admin). Beda: identitas & gelar dari DB (bukan dari klien), batch dikirim 100 ms setelah langkah pertama (bukan ticker global), langkah dihitung server (`take_steps` dipakai `tick`). 10 test integrasi lewat socket sungguhan (`tokio-tungstenite`) + hub langsung. DoD "1000 & 2000 klien, p95 ≤ 200 ms" menunggu `bin/pare_qa_tokens` + database scratch (butuh izin user).
Port `server/realtime.ts`: auth token query (pola `canvas_ws.rs`), zona → saluran maks. 50 (pilih yang paling ramai), batch `moves` 10 Hz, rate limit 16 gerakan/detik, backpressure, satu koneksi per pemain (tab baru menendang yang lama), `/pare/stats` (admin). Stamina langkah (jalan 0,04, sepeda 0,015 — diturunkan setengah 2026-09-25) dicatat per batch.
**DoD:** `scripts/loadtest.ts` diarahkan ke Rust: 1000 & 2000 klien, latensi p95 ≤ 200 ms.

## P4-002 — Chat tersimpan & aturan bahasa di server (L)

✅ **SELESAI (2026-09-24).** Migrasi `0083_pare_chat.sql`; `pare_langrule.rs` (port `langrule.ts`, **518 kasus nyata dari `judgeMessage` TS lolos** — `scripts/gen-langrule-cases.ts`); pelanggaran −½ nyawa lewat ledger, poin chat dengan batas harian; personal & grup tersimpan dan sampai lintas zona; Umum tersimpan 30 hari (dipangkas tiap jam). `GET /pare/inbox`, `POST /pare/conversations/{id}/leave`. Penyimpangan: pembuatan grup terjadi pada pesan pertama (id dari klien, divalidasi) — bukan `POST /pare/conversations`; tanda baca (`read`) masih lokal di FE; riwayat Umum yang diputar ulang saat masuk saluran berasal dari memori hub (tersimpan di DB, belum dibaca ulang setelah restart).
Tabel `pare_conversations(kind: channel|dm|group)`, `pare_conversation_members`, `pare_messages`. Personal & Grup tersimpan dan terkirim lintas zona; Umum per saluran dengan retensi 30 hari (job worker). Port `langrule.ts` ke Rust (test paritas dengan kasus prototipe) → pelanggaran −½ nyawa lewat ledger. `GET /pare/conversations`, `GET /pare/conversations/{id}/messages`, tanda baca, buat grup (2–5 anggota), keluar grup.

## P4-003 — Skala: Redis pub/sub & presence (M)

⏸ **DITUNDA sesuai tiket** sampai uji beban P4-001 memutuskan satu instance cukup atau tidak. State hub per-proses (saluran, presence, langkah); `Hub` sudah memisahkan transport, sehingga pub/sub bisa ditambahkan tanpa mengubah protokol.
Presence online di Redis; saluran di-shard per zona antar instance; pesan lintas instance lewat pub/sub. Boleh ditunda bila satu instance cukup (keputusan berdasar hasil P4-001).

## P4-004 — FE: WS Rust + chat dari API (M)

✅ **SELESAI kode.** `net.ts` ke `/ws/pare?token=` (turunan `NEXT_PUBLIC_API_URL`, atau `NEXT_PUBLIC_WS_URL`), `hello` hanya membawa posisi, token kedaluwarsa (1008) → refresh & sambung ulang, 4404 tidak diulang; riwayat personal/grup dari `GET /pare/inbox` (localStorage `nanyang-chats-v1` dihapus); pesan `violation`/`reward` dari server; `server/realtime.ts` (Bun) dihapus; `scripts/bots.ts` & `loadtest.ts` memakai token QA (`cargo run --bin pare_qa_tokens`, database scratch). Diverifikasi di browser dengan socket disimulasikan (`page.routeWebSocket`).
`net.ts` ke `NEXT_PUBLIC_WS_URL`, riwayat chat dari API (hapus `nanyang-chats-v1` localStorage), bot demo `scripts/bots.ts` diarahkan ke `/ws/pare` dengan akun QA.

---

# Pare-5 — PWA & push notification

## P5-001 — PWA (S)

✅ **SELESAI kode (2026-09-25).** `src/app/manifest.ts` (fullscreen, ikon pixel-art 192/512 + maskable + apple-touch di `public/icons`), `public/sw.js` (cache-first `/_next/static`, ikon, font; navigasi selalu dari jaringan, offline → `offline.html` (game butuh server); API & socket tidak pernah di-cache; `push` & `notificationclick`), `public/offline.html`, registrasi hanya di build produksi (`src/lib/pwa.ts`), tombol "Pasang aplikasi" (`beforeinstallprompt`, instruksi iOS) di Bantuan → 🔔 Notifikasi & Aplikasi. `sw.js` dikirim `no-cache`.
`manifest.webmanifest`, ikon, service worker (cache-first aset statis & font, network-first API), halaman offline, prompt pasang.

## P5-002 — Web Push backend (M)

✅ **SELESAI (2026-09-25), dengan penyimpangan.** Migrasi `0085_push.sql`; `services/web_push.rs` (RFC 8291 + VAPID RFC 8292 dengan `ring`, diuji terhadap nilai antara RFC 8291 §5 + dekripsi ala browser + verifikasi tanda tangan ES256); VAPID dari env (bukan `Config`, supaya test yang menyalin Config tidak berubah), `bin/pare_vapid_keys`. Endpoint `GET/PATCH /pare/notify`, `POST/DELETE /pare/push/subscriptions`, `POST /pare/push/test` (di bawah `/pare`, bukan `/me/push-subscriptions`; tabelnya tetap generik). Pengiriman pesan langsung dari API (tokio task + 1 kali coba ulang), pengingat terjadwal lewat `job_queue`/`titian-worker`. Langganan 404/410 dihapus. Test: `tests/integration/pare_push_test.rs` (3, dengan layanan push palsu yang mendekripsi) + 3 unit test.
`push_subscriptions(user_id, endpoint, p256dh, auth, app, created_at)`, VAPID di config, `POST/DELETE /me/push-subscriptions`, pengiriman lewat `job_queue` di `titian-worker` (retry, hapus langganan 404/410).

## P5-003 — Pemicu & pengaturan notifikasi (M)

✅ **SELESAI.** `services/pare_push.rs`: pesan personal/grup saat offline (throttle 2 menit/percakapan), misi harian (07:00 WIB), streak hampir putus (19:00 WIB), stamina pulih saat tidur; saklar per jenis; maks 12/hari. Penyimpangan: "pengingat lapar/stamina" diganti **streak** — saat offline ≥ 1 jam pemain dianggap istirahat (Pare-3), jadi lapar tidak terjadi ketika game tertutup. Pengingat Premium habis (ADR-0018 §9.3) belum.
Pesan Personal/Grup saat offline, misi harian baru, pengingat lapar/stamina, bangun setelah tidur cukup; toggle per jenis di pengaturan pemain; batas frekuensi.

---

# Pare-6 — Deploy & integrasi

## P6-001 — Vercel & domain (S)
Proyek Vercel `game`, env, `pare.titianasa.com`, header cache aset, tanpa URL hard-code.

## P6-002 — Backend produksi (S)
Caddy: rute `/pare/*` & `/ws/pare` (WebSocket upgrade), batas koneksi, observabilitas (metrik koneksi WS, pesan/detik).

## P6-003 — Titian ↔ Pare (S)
Tautan dari web Titian ke Pare dan sebaliknya; onboarding masing-masing tetap wajib (ADR-0016 §1). Admin Pusat: kartu ringkas pemain Pare (jumlah pemain, online).

## P6-004 — Uji beban & QA akhir (M)
Uji beban produksi-mirip, uji browser end-to-end (login → onboarding → kelas → makan → chat → push), pembersihan data QA.
