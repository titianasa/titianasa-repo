# Phase 40 — Admin Pusat v1 & Pengaturan AI (ADR-0014, ADR-0013 §3.5)

📋 **RENCANA — belum dieksekusi.** Dianalisis & disetujui user 2026-09-13 (Opus), untuk dieksekusi tiket demi tiket (**Sonnet**). Dasar keputusan: [ADR-0014](../adr/0014-admin-pusat.md), [ADR-0013 §3.5](../adr/0013-ai-learning-engine.md).

Cara eksekusi: kerjakan tiket berurutan sampai DoD-nya lolos. Fase ini **paralel** dengan Phase 39. Halaman yang butuh event (Peserta aktif, Pembelajaran, Kelas & Guru) sengaja ditunda ke setelah Phase 39.

---

## 1. Tujuan

- Pengelola platform punya satu tempat (`/admin`) untuk melihat peserta, penjualan, kurikulum, dan biaya AI.
- **Semua peran AI memakai model yang diatur dari Admin Pusat**, tanpa deploy ulang. Default sekarang: Vertex AI `gemini-3.8-flash` untuk teks & vision; STT/TTS OpenRouter yang sedang dipakai.
- Antrean job generik tersedia, dipakai dulu untuk agregasi dashboard, lalu untuk agen AI di Phase 42.

## 2. Yang WAJIB dipertahankan

- `/organisasi` tetap konsol satu organisasi. Admin Pusat adalah area terpisah dan **lintas organisasi**.
- Kredensial provider AI tetap di env/secret. Tidak pernah masuk database atau tampil di UI.
- Variabel lingkungan model yang ada (`AI_*_MODEL` di `config.rs`) tetap berfungsi sebagai **fallback**, jadi deploy tanpa baris pengaturan di DB tetap jalan persis seperti sekarang.
- Setiap panggilan AI tetap tercatat di `ai_tasks`.
- Desain Titian: token `primary` emas, komponen `@/components/ui/*`, dark mode, teks Bahasa Indonesia.

## 3. Aturan main eksekusi

Sama dengan Phase 39 §3 (migrasi aditif mulai setelah nomor terakhir Phase 39, sinkron `domain-model.md` & `api-contract.md`, verifikasi terarah, cek browser dengan `Bun.WebView`, izin user untuk token QA, jangan commit tanpa diminta). Semua angka rupiah & tanggal dilaporkan dalam **WIB (Asia/Jakarta)**.

---

## P40-001 — Kerangka `/admin`, izin, log audit (S)

✅ **SELESAI (2026-09-13, Sonnet).** `permissions.rs`: `Resource::AdminPusat` + `Action::Manage` baru, digerbang lewat satu fungsi `is_admin_pusat_role()` (hanya `platform_admin` sekarang) — persis seperti diminta tiket, supaya `pusat_kurikulum`/`pusat_ai`/`pusat_bisnis`/`pusat_viewer` (ADR-0014 §1) nanti cukup ditambah di satu tempat. Migrasi `0049_admin_audit_log.sql`: `actor_id` sengaja `on delete set null` (bukan `cascade` seperti kebanyakan FK `user_id` lain di basis kode ini) — menghapus akun aktor tidak boleh menghapus jejak tindakannya. `services/admin_audit.rs::record()` (dipakai tiket Manage berikutnya) dan `::list()` (keyset `(created_at, id)` terbaru-dulu, cursor buram `"{rfc3339}_{uuid}"` — bukan disandikan, ini endpoint admin internal, tidak ada yang sensitif untuk disembunyikan dari query string). `GET /admin/audit-log`.

Frontend: `app/admin/layout.tsx` (`RequireAuth` → `RequireAdminAccess` → `AdminShell`), sidebar berisi **semua 11 halaman ADR-0014 §2** (bukan cuma yang sudah ada isinya) dengan badge "Fase 39"/"Fase 42" untuk yang ditunda, `PeriodSelector` (hari ini/7/30 hari/rentang custom lewat dialog tanggal, state di `store/admin-period-store.ts` — belum dipakai halaman manapun, disiapkan untuk P40-005), dan halaman `Log Audit` (`app/admin/audit-log`) yang benar-benar fungsional (bukan placeholder) karena itu yang tiket ini bangun di backend. 9 halaman lain (Ringkasan, Peserta, Pembelajaran, Kurikulum & Konten, Usulan AI, Kelas & Guru, Penjualan, Operasional AI, Pengaturan AI, Organisasi) adalah rute nyata dengan `AdminPlaceholderPage` yang menjelaskan tiket mana yang akan mengisinya — bukan 404, sesuai instruksi "pesan jelas, bukan layar kosong" (yang sebetulnya ditulis untuk gerbang peran, tapi prinsip yang sama dipakai di sini).

**`RequireAdminAccess` sengaja BEDA polanya dari `RequireStudioAccess`**: peran yang ditolak melihat layar "Akses ditolak" penuh dengan penjelasan + tombol kembali, bukan `router.replace` diam-diam — DoD tiket eksplisit minta "diarahkan keluar dengan pesan jelas, bukan layar kosong". Error loading/auth tetap redirect otomatis (tidak ada yang perlu dijelaskan di situ).

**2 bug nyata ditemukan lewat verifikasi browser sungguhan** (bukan cuma dari test yang lulus):
1. Server yang jalan di :8090 masih binary LAMA (predate P40-001) — `curl /admin/audit-log` sempat balas `404 not_found` bukan data asli. Ini pola yang sama yang sudah beberapa kali kejadian sesi ini ("stale binary problem") — di-rebuild+restart, langsung benar.
2. **Item sidebar "Ringkasan" (href `/admin`) selalu ter-highlight di SEMUA halaman** — karena `/admin` adalah prefix dari setiap href lain (`pathname.startsWith(item.href + "/")` cocok untuk `/admin/audit-log` dkk juga). Studio tidak kena bug yang sama karena tak satu pun item nav-nya adalah root section itu sendiri. Diperbaiki: item `/admin` dicek exact-match saja.

Diverifikasi via `Bun.WebView` (izin diminta & diberikan user sebelum insert baris QA): platform_admin bisa buka `/admin` dan `/admin/audit-log`, menulis 1 baris `admin_audit_log` langsung ke DB lalu reload → baris itu benar-benar muncul di layar (nama aktor, waktu WIB, before/after, alasan); role `student` yang buka `/admin` melihat layar "Akses ditolak" (bukan redirect diam-diam, bukan layar kosong). Baris `refresh_tokens`, user QA, dan baris audit uji coba semuanya dihapus setelah selesai.

`cargo test --lib` 222 lulus (+2 dari 220 — 2 unit test cursor). `cargo test --test integration` penuh: **113 lulus, 26 gagal — daftar sama persis**, tidak bertambah (113 = 109 sebelumnya + 4 test `admin_audit_test.rs` baru: `platform_admin_can_list_the_audit_log`, `other_roles_get_403`, `recording_an_action_is_what_list_later_reads_back...`, `pagination_walks_older_rows_via_next_cursor...`). `npx tsc --noEmit` dan `npx eslint` bersih.

Backend:
- `permissions.rs`: `Resource::AdminPusat` dengan aksi `View` dan `Manage`. Awalnya hanya `platform_admin`. Peran `pusat_*` belum dibuat, tetapi pengecekan sudah lewat satu fungsi supaya menambahkannya nanti cukup di satu tempat.
- Migrasi `admin_audit_log (id, actor_id, action, target_type, target_id, before, after, reason, created_at)` + `services/admin_audit.rs::record`.
- `GET /admin/audit-log` (paginasi).

Frontend:
- Route group `app/admin/` dengan layout sendiri: sidebar halaman sesuai ADR-0014 §2, pemilih periode (hari ini / 7 / 30 hari / rentang), dan gerbang peran lewat `lib/roles.ts`.
- Pengguna tanpa peran diarahkan keluar dengan pesan jelas, bukan layar kosong.

DoD: `platform_admin` bisa membuka `/admin`; peran lain mendapat 403 dari API dan diarahkan dari UI; setiap aksi `Manage` tercatat di log audit.

## P40-002 — Antrean job generik + scheduler (M)

✅ **SELESAI (2026-09-13, Sonnet).** Migrasi `0050_jobs.sql`: `priority` konvensi nice(1) — angka LEBIH KECIL diklaim lebih dulu. `services/job_queue.rs`: `enqueue`, `ensure_scheduled` (idempoten — hanya menulis kalau belum ada baris `pending`/`running` untuk `job_type` itu, dites eksplisit termasuk saat baris yang ada sedang `running` bukan cuma `pending`), `claim` (CTE `FOR UPDATE SKIP LOCKED` + `limit 1`, menaikkan `attempt` SAAT diklaim — mengklaim itu sendiri "menghabiskan" satu percobaan), `complete`, `fail` (backoff bertahap 30s→...→32min dibatasi 6 kali lipat, lalu `status='failed'` permanen begitu `attempt >= max_attempts`), `reap` (job `running` yang terkunci >`stuck_after` dikembalikan ke `pending` **tanpa** menghitung `attempt` — pekerjanya mati, bukan pekerjaannya gagal). Registry `HANDLERS`/`SCHEDULED_JOBS` sengaja **kosong** sekarang (pola yang sama dipakai berulang di Phase 39: infrastruktur teruji penuh, konsumen pertama—`metrics_rollup`—menyusul di P40-004, cukup 1 baris tambahan di sana, tidak ada perubahan di file ini).

Binary kedua `src/bin/titian-worker.rs` — **sengaja hanya connect ke Postgres** (`db::connect`), bukan `AppState::init` penuh (yang mewajibkan kredensial OpenRouter/GCP/R2 yang tidak relevan selama `HANDLERS` masih kosong; YAGNI, diperlebar nanti oleh tiket yang benar-benar butuh AI provider di dalam job). 3 loop independen lewat `tokio::join!`: klaim (poll 5 detik), scheduler (`run_scheduled` tiap 60 detik), reaper (tiap 60 detik, ambang macet 15 menit).

**Dibuktikan lewat 9 test integrasi baru** (`job_queue_test.rs`, langsung ke `job_queue::*`, tanpa lapisan HTTP — tiket ini memang tidak menambah endpoint): klaim mengembalikan job & menaikkan `attempt`; tipe job yang tidak diminta tidak pernah diklaim; prioritas lebih kecil diklaim lebih dulu; **4 "pekerja" mengklaim 20 job bersamaan — setiap job diklaim TEPAT SEKALI, tidak ada yang diklaim dobel** (bukti nyata `SKIP LOCKED` bekerja, bukan asumsi); `complete` melepas kunci; `fail` dites penuh 3 percobaan berturut sampai `status='failed'` (menegaskan `run_after` didorong maju tiap gagal, dan job yang sudah `failed` permanen tidak pernah bisa diklaim lagi); `reap` memulihkan job yang terkunci lama **tanpa** menaikkan `attempt`, dan sebaliknya TIDAK menyentuh job yang baru saja dikunci; `ensure_scheduled` dites 4 skenario (belum ada→tulis, sudah `pending`→lewati, sedang `running`→lewati juga, sudah `done`→boleh tulis lagi).

Binary worker juga dijalankan sungguhan (`cargo run --bin titian-worker`, terpisah dari proses API) selama proses API (`titian-backend-rust`) tetap hidup di port 8090 — keduanya jalan bersamaan tanpa saling ganggu, membuktikan DoD "worker berjalan terpisah dari API" secara nyata, bukan cuma dari bacaan kode.

`cargo test --lib` 223 lulus (+1, unit test `backoff_doubles_then_caps`). `cargo test --test integration` penuh: **122 lulus, 26 gagal — daftar sama persis**, tidak bertambah (122 = 113 sebelumnya + 9 baru).

- Migrasi `jobs (id, job_type, payload, priority, status, attempt, max_attempts, run_after, locked_by, locked_at, last_error, cost_tokens, created_at, finished_at)` + indeks `(status, run_after, priority)`.
- `services/job_queue.rs`: `enqueue`, `claim` (`FOR UPDATE SKIP LOCKED`), `complete`, `fail` (retry dengan jeda bertahap sampai `max_attempts`), dan `reap` untuk job yang terkunci terlalu lama.
- Binary kedua `src/bin/titian-worker.rs` di crate yang sama: loop klaim → jalankan handler sesuai `job_type` → selesai. Scheduler berkala (tokio interval) yang meng-enqueue job terjadwal secara idempoten.
- Registry `job_type` di kode (pola registry subtype soal).

DoD: unit test klaim bersamaan (dua worker tidak mengambil job yang sama), retry, dan reap; worker berjalan terpisah dari API.

## P40-003 — Pengaturan AI: katalog, peran, resolver (M–L) ⭐

✅ **SELESAI (2026-09-13, Sonnet).** Tiket terbesar Phase 40 — ringkasan lengkap dulu, rincian teknis di bawahnya (masih relevan sebagai spesifikasi asli).

Migrasi `0051_ai_settings.sql`: `ai_model_catalog` (unique `(provider, model_id)`, seed 3 baris persis seperti yang sudah hidup hari ini — `vertex/gemini-3.8-flash` teks+vision+json maks 65.536, `openrouter/openai/whisper-1` stt, `openrouter/hexgrad/kokoro-82m` tts) dan `ai_role_settings` (PK `role`, teks bebas seperti `jobs.job_type`/`learning_events.event_type` — bukan FK/enum, karena peran valid didefinisikan di kode lewat `AI_ROLES`, bukan di DB).

`services/ai_settings.rs` — **16 peran terdaftar** (12 diminta tiket + 4 peran agen ADR-0013 untuk Fase 42): `lesson_generation`, `question_generation`, `quiz_generation`, `ocr`, `live_chat`, `writing_evaluation`, `speaking_evaluation`, `grammar_evaluation`, `speaking_room_text`, `speaking_room_tts`, `stt`, `tts`, `agent_diagnosis`, `agent_editor`, `agent_qa`, `agent_reporter`. Tiap peran punya `required_capabilities` dan `env_fallback` — closure yang menunjuk PERSIS field `Config` yang dulu dibaca call site itu (bukan tebakan baru), termasuk kasus menarik: **`quiz_generation` tidak pernah punya field `Config` sendiri**, jadi `env_fallback`-nya sengaja menunjuk `ai_lesson_generation_model` — persis perilaku asli `handlers/ai.rs`'s `resolve_ai_model(body.model, &config.ai_lesson_generation_model)` sebelum tiket ini, dibuktikan lewat test khusus. `resolve(pool, config, role)`: baris `ai_role_settings` yang `enabled` → kalau tidak ada, `env_fallback(config)` — TIDAK PERNAH jatuh ke literal `"gemini-3.8-flash"` yang di-hardcode di resolver (kecuali untuk 4 peran agen yang memang belum punya pemanggil/field `Config` sama sekali) — inilah yang membuat DoD pertama benar **by construction**: tabel kosong = perilaku identik dengan sebelum tiket ini.

**Cache di memori dikunci per NAMA DATABASE pool** (`pool.connect_options().get_database()`), bukan satu slot global tanpa kunci — ditemukan lewat kegagalan test nyata: `#[sqlx::test]` memberi tiap test database terpisah tapi SEMUA test jalan di proses yang sama, jadi cache tanpa kunci membuat satu test yang menonaktifkan model membocorkan state ke test lain yang jalan bersamaan di database berbeda. Di produksi ini setara satu slot biasa (cuma ada satu pool sepanjang hidup proses) — nol biaya tambahan, tapi baru benar utuh untuk suite test yang paralel.

**Migrasi 26 titik kode** (`grep -rn "config.ai_.*_model" src` sekarang HANYA nongol di `ai_settings.rs` sebagai komentar prosa, bukan kode aktif — persis DoD) + **16 titik `resolve_max_tokens`** (sekarang butuh `pool` untuk baca `max_output_tokens` dari katalog, bukan `VERTEX_MODEL_MAX_TOKENS` const yang dihapus) + **6 titik `resolve_ai_model`** (jadi `async`, tervalidasi lewat `ai_settings::text_capable_models`, bukan `AI_MODEL_OPTIONS` const yang dihapus). `speaking_room.rs`'s 3 fungsi (murni stateless sebelumnya) dilebarkan menerima `pool: &PgPool` karena `resolve_max_tokens` butuhnya sekarang. `GET /ai/models` (pemilih model Studio) sekarang baca katalog live.

Endpoint admin: `GET /admin/ai/catalog`, `PATCH /admin/ai/catalog/{id}` (aktif/nonaktif + harga), `GET /admin/ai/roles`, `PUT /admin/ai/roles/{role}` (full-replace, tervalidasi model ada-di-katalog **dan** punya kemampuan yang dibutuhkan peran — 422 kalau tidak), `POST /admin/ai/roles/{role}/test` (prompt nyata ke `text_ai_provider`, kembalikan latensi+token+contoh balasan; ditolak jelas untuk peran `stt`/`tts` yang bukan berbasis teks). Semua tulisan lewat `admin_audit::record` dengan `reason` opsional dari body request.

**`generate_with_fallback`** (infrastruktur baru di `ai_provider.rs`, 4 test unit) — coba model utama, kalau gagal DAN `fallback_model_id` diisi, coba sekali lagi ke cadangan, kembalikan model mana yang BENAR-BENAR menjawab. **Belum disambungkan ke satu pun dari ~16 titik generate call** — keputusan cakupan sadar: DoD tiket ini sendiri hanya minta resolusi model yang BENAR (dibuktikan penuh), bukan pembuktian ujung-ke-ujung jalur kegagalan; menyambungkannya ke jalur retry-lalu-validasi yang sudah ada di tiap generator (yang bentuknya beda-beda per file) adalah pekerjaan tiket terpisah, satu titik pada satu waktu.

**1 bug nyata ditemukan+diperbaiki lewat verifikasi browser sungguhan** (bukan cuma test lulus): tombol **Uji** awalnya memakai `max_tokens: 128` — Vertex Gemini (model reasoning) bisa menghabiskan SELURUH anggaran untuk pemikiran tersembunyi sebelum menulis jawaban terlihat, gagal `MAX_TOKENS` tanpa apa pun untuk ditampilkan (kelas bug yang sama yang sudah didokumentasikan di komentar `resolve_max_tokens` untuk jalur generate sungguhan). Diperbaiki: `test_role` sekarang pakai `resolve_max_tokens` sendiri dengan fallback 1024, dibuktikan lewat panggilan Vertex sungguhan di browser (5174ms, 280 token, berhasil).

Frontend: `app/admin/pengaturan-ai` — tabel 16 peran (label bahasa sehari-hari, badge model/"Bawaan sistem", tombol Uji yang otomatis disembunyikan untuk peran non-teks), dialog edit (`components/admin/ai-role-edit-dialog.tsx`, pilihan model difilter ke yang aktif+mampu lewat `lib/ai-roles.ts` — mirror FE dari registry Rust, pola yang sama dengan `lib/roles.ts`), tabel katalog dengan toggle aktif/nonaktif langsung, dan bagian Riwayat Perubahan yang menyaring `admin_audit_log` ke aksi `ai_role_settings.*`/`ai_model_catalog.*`. Diverifikasi penuh lewat `Bun.WebView` (izin diminta & diberikan): ganti model peran "Membuat & Mengedit Modul Belajar" ke Gemini lewat UI → badge berubah SEKETIKA tanpa reload → baris muncul di Riwayat Perubahan dengan alasan yang diketik. Semua baris QA (user, org, token, baris `ai_role_settings`, baris audit uji coba) dihapus setelah selesai.

`cargo test --lib` 229 lulus (+6 dari 223: 3 test `ai_settings` registry, 4 test `generate_with_fallback` — koreksi: total bertambah bersih +6 setelah 1 test lama Vertex-ceiling dihapus karena fungsi yang diuji sudah tidak ada). `cargo test --test integration` penuh: **131 lulus, 26 gagal — daftar sama persis**, tidak bertambah (131 = 122 sebelumnya + 9 test baru `ai_settings_test.rs`). `npx tsc --noEmit` dan `npx eslint` bersih.

Backend:
- Migrasi `ai_model_catalog (id, provider, model_id, label, capabilities text[], max_output_tokens, price_input_per_mtok_idr, price_output_per_mtok_idr, enabled, created_at)` dan `ai_role_settings (role, model_id, fallback_model_id, temperature, max_tokens, daily_token_budget, enabled, updated_by, updated_at)`.
- Seed katalog: `vertex/gemini-3.8-flash` (`text`, `vision`, `json`; max output 65.536), `openrouter/openai/whisper-1` (`stt`), `openrouter/hexgrad/kokoro-82m` (`tts`).
- `services/ai_settings.rs`:
  - Registry `AiRole` beserta kemampuan yang dibutuhkan setiap peran. Awal: `lesson_generation`, `question_generation`, `quiz_generation`, `ocr`, `live_chat`, `writing_evaluation`, `speaking_evaluation`, `grammar_evaluation`, `speaking_room_text`, `speaking_room_tts`, `stt`, `tts`. Peran agen ADR-0013 (`agent_diagnosis`, `agent_editor`, `agent_qa`, `agent_reporter`) didaftarkan sekarang, dipakai di Phase 42.
  - `resolve(role) -> ResolvedModel { provider, model_id, fallback, temperature, max_tokens }`. Urutan: `ai_role_settings` → env `AI_*_MODEL` yang ada → `gemini-3.8-flash`. Cache di memori, dibuang saat pengaturan disimpan.
  - Validasi saat simpan: model harus aktif di katalog **dan** punya kemampuan yang dibutuhkan peran.
- **Pindahkan ke-26 titik kode** yang membaca `state.config.ai_*_model` ke `ai_settings::resolve(role)`: `ai_lesson_generation_model` ×9, `ai_stt_model` ×3, `ai_live_chat_model` ×2, `ai_ocr_model` ×2, `ai_speaking_evaluation_model` ×2, `ai_speaking_room_text_model` ×2, `ai_writing_evaluation_model` ×2, dan satu masing-masing untuk grammar, question generation, speaking room TTS, dan TTS.
- `AI_MODEL_OPTIONS` dan `VERTEX_MODEL_MAX_TOKENS` di `ai_provider.rs` dibaca dari katalog. `GET /ai/models` (pemilih model penulis di Studio) mengembalikan model aktif ber-`text` dari katalog.
- Bila model utama gagal karena gangguan sesaat setelah retry provider habis, pakai `fallback_model_id`. `ai_tasks.model` mencatat model yang **benar-benar** dipakai.
- Endpoint: `GET /admin/ai/catalog`, `PATCH /admin/ai/catalog/{id}` (aktif/nonaktif, harga), `GET /admin/ai/roles`, `PUT /admin/ai/roles/{role}`, `POST /admin/ai/roles/{role}/test` (prompt uji kecil, mengembalikan latensi & token). Semua perubahan tercatat di log audit.

Frontend (`app/admin/pengaturan-ai`):
- Tabel peran: nama peran dalam bahasa sehari-hari (misal "Membuat Modul Belajar"), model, cadangan, temperatur, batas token, anggaran harian, dan tombol **Uji**.
- Pilihan model per peran hanya menampilkan model yang mampu (OCR tidak menawarkan model tanpa vision).
- Katalog: daftar model, kemampuan, harga, aktif/nonaktif.
- Riwayat perubahan (dari log audit).

DoD:
- Tanpa baris di `ai_role_settings`, semua fitur AI berjalan persis seperti sekarang (lewat fallback env).
- Mengganti model satu peran di Admin Pusat langsung berlaku di panggilan berikutnya tanpa restart. Buktikan dengan satu generate soal sungguhan dan cek `ai_tasks.model`.
- Memilih model tanpa `vision` untuk `ocr` ditolak (422).
- `grep -rn "config.ai_.*_model" src` hanya tersisa di `config.rs` dan resolver.

## P40-004 — Agregat harian (M)

✅ **SELESAI (2026-09-13, Sonnet).** Migrasi `0052_metrics_daily.sql`: 5 tabel, PK = seluruh dimensi pengelompokan (upsert-lah yang membuat "jalankan dua kali" aman) — setiap dimensi yang bisa kosong (subscription_tier, org_id, jenjang) di-COALESCE ke sentinel tetap ('none', UUID nil, 'belum_diisi') alih-alih NULL mentah, karena NULL di dalam PRIMARY KEY tidak pernah dianggap sama dengan NULL lain oleh Postgres — akan diam-diam merusak jaminan anti-duplikat itu sendiri.

`services/metrics_rollup.rs`: `rollup_sales`/`rollup_subscriptions`/`rollup_users`/`rollup_ai` menghitung ulang satu `day` (dipanggil untuk 3 hari terakhir tiap giliran job, DAN dipakai backfill untuk setiap hari sejak data pertama). `rollup_content` **sengaja hanya untuk HARI INI**, tidak di-backfill mundur — keputusan desain sadar: `subscriptions`/`modules` tidak punya log perubahan, jadi "cakupan kurikulum minggu lalu" tidak bisa direkonstruksi secara jujur; tabel ini jadi riwayat berjalan mulai dari hari job pertama kali berjalan, bukan sejarah penuh.

**`metrics_daily_subscriptions`** — `subscriptions` tidak punya tabel riwayat (bahkan fitur "batalkan langganan" belum ada di produk sama sekali, dicek langsung ke kode), jadi `new` dihitung dari `orders` (order langganan BERBAYAR PERTAMA per pengguna — bukan `current_period_start`, yang ditimpa `activate()` setiap kali perpanjang juga), dan `churned` dari `current_period_end` yang sudah lewat tanpa perpanjangan — satu-satunya sinyal jujur yang ada di skema sekarang. Granularitas per HARI (bukan timestamp) berarti satu baris bisa `active=1` DAN `churned=1` pada hari yang sama (berlangganan sebagian hari itu, lalu kedaluwarsa) — bukan kontradiksi, dites eksplisit.

**`metrics_daily_content`** menjawab pertanyaan "cakupan kurikulum" lewat CTE rekursif yang berjalan NAIK dari tiap topik (modul daun, `is_folder=false`) mencari folder leluhur terdekat berjudul "Tahap N" — terbukti cepat (0.25 detik untuk 17.646 modul topik) dan berhasil menemukan 4.477 topik dengan tahap yang bisa diselesaikan di database dev sungguhan.

**1 bug nyata serius ditemukan & diperbaiki** oleh test dengan angka yang SUDAH DIKETAHUI benar (bukan cuma "lulus"): `jsonb_path_query(quiz_config, '$.**.taxonomy')` mode **lax** (default) **melipatgandakan dua kali** setiap hasil — ditemukan karena test dengan 2 soal buatan mengharapkan `questions_total=2` tapi dapat `4`. Root cause: operator rekursif `**` mode lax Postgres mengunjungi sebuah array SEBAGAI array DAN SEBAGAI tiap elemen yang dibongkar, menghasilkan kecocokan ganda untuk struktur bersarang seperti punya kita. Diperbaiki jadi `strict $.**.taxonomy` (terverifikasi lewat `psql` langsung: lax=4, strict=2, untuk data yang sama). **Bug ini sudah SEMPAT tertulis ke database dev sungguhan** lewat backfill pertama (`questions_total=70` untuk Topik 1 Matematika, seharusnya 35) — dikoreksi dengan menjalankan ulang job setelah fix, diverifikasi cocok PERSIS dengan hitungan manual (7 item kuis × 5 soal = 35).

**Dibuktikan lewat 8 test integrasi baru** (`metrics_rollup_test.rs`) dengan data seed terkendali (bukan cuma dibandingkan ke dirinya sendiri): sales/ai/users semuanya dites `assert_eq!` terhadap angka yang SECARA MANUAL dihitung dari skenario seed, bukan cuma "cocok dengan query sumber yang sama" (yang bisa lulus meski keduanya salah dengan cara yang sama); subscriptions menguji new/active/churned termasuk kasus "aktif dan churn di hari yang sama"; content menguji has_module/has_quiz membedakan konten ASLI dari placeholder kosong, dan taksonomi bloom/difficulty; `run_scheduled` diuji TIDAK mengantre ulang dalam jendela `min_interval` (1 jam) meski job sebelumnya sudah `done` (bukan cuma `pending`/`running`) — ini yang benar-benar menegakkan kadensi "setiap jam", bukan `ensure_scheduled`'s sendiri yang hanya mencegah duplikat SAAT BERSAMAAN; backfill diuji mencakup rentang penuh dari baris sumber tertua dan idempoten.

**Juga dijalankan sungguhan** lewat `cargo run --bin backfill_metrics` (14 hari diproses, sejak 2026-08-31) dan `titian-worker` sungguhan (scheduler benar-benar mengantre & menjalankan `metrics_rollup`, status `done` di tabel `jobs`) — setiap angka sales/ai/users dicek manual dengan `SUM`/`COUNT` langsung ke `orders`/`ai_tasks`/`users` di database dev dan **cocok persis**, bukan cuma di test.

`job_queue.rs` diperluas sesuai yang direncanakan di P40-002: `ScheduledJob` dapat field `min_interval`, `run_scheduled` sekarang mengecek baris `jobs` mana pun (bukan cuma pending/running) yang lebih baru dari `min_interval` sebelum mengantre lagi — satu-satunya perubahan mekanisme di file itu. `HANDLERS`/`SCHEDULED_JOBS` yang tadinya kosong sekarang masing-masing berisi 1 baris (`metrics_rollup::HANDLER`/`::SCHEDULE`), persis seperti yang dijanjikan.

`cargo test --lib` 229 lulus (tidak berubah — semua test baru integrasi). `cargo test --test integration` penuh: **139 lulus, 26 gagal — daftar sama persis**, tidak bertambah (139 = 131 sebelumnya + 8 baru).

- Migrasi tabel agregat dengan kolom `day date` (WIB), dimensi, dan nilai:
  - `metrics_daily_sales (day, kind, subscription_tier, orders, paid_orders, revenue_idr)`
  - `metrics_daily_subscriptions (day, tier, active, new, churned)`
  - `metrics_daily_users (day, org_id, jenjang, signups)`
  - `metrics_daily_content (day, subject_id, tahap, topics_total, topics_with_module, topics_with_quiz, questions_total, questions_by_bloom jsonb, questions_by_difficulty jsonb)`
  - `metrics_daily_ai (day, task_type, model, calls, failed, tokens, cost_idr)`
- Job `metrics_rollup` (P40-002) menghitung ulang **3 hari terakhir** setiap putaran (setiap jam) dan idempoten (upsert).
- Backfill sejak data pertama.

DoD: angka agregat cocok dengan query langsung ke tabel sumber untuk 3 hari sampel (test integrasi); memicu job dua kali tidak menggandakan angka.

## P40-005 — Halaman Ringkasan, Penjualan, Kurikulum & Konten, Operasional AI, Organisasi (L)

✅ **SELESAI (2026-09-13, Sonnet).** Tiket terakhir Phase 40. `services/admin_metrics.rs` (backend) + 5 halaman `app/admin/*` (frontend), semuanya baca dari agregat P40-004 kecuali dua pengecualian sadar: `pendapatan_hari_ini_idr`/`pendapatan_bulan_ini_idr` di Ringkasan baca LANGSUNG ke `orders` (job per jam bisa basi sampai 1 jam, terlalu lambat untuk angka uang hari ini — dibuktikan lewat test yang insert order lalu langsung cek API tanpa menjalankan rollup); `Organisasi` juga baca langsung (daftar organisasi kecil & murah, ADR-0014 §2 sendiri tidak mendaftarkannya sebagai butuh tabel agregat harian).

**Perbandingan periode sebelumnya** (`Comparison { current, previous: Option<i64> }`) — `previous: null` HANYA saat tidak ada baris sumber SAMA SEKALI sebelum jendela periode itu ("belum cukup data" jujur), berbeda dari `previous: 0` yang berarti ada riwayat tapi memang sepi (angka nyata, bisa dibandingkan) — dites eksplisit dengan 2 skenario terpisah, bukan cuma satu arah.

**Peringatan ADR-0014 §4** (deterministik, bukan AI) — 3 aturan aktif: pendapatan hari ini turun >40% dari rata-rata 7 hari sebelumnya, tingkat gagal AI >10% (7 hari), job pending lebih tua dari 1 jam. Semua 3 dites lewat skenario yang benar-benar memicu setiap aturan.

**Kurikulum & Konten** memakai `quiz_taxonomy::target_spread(&format!("Tahap {tahap}"), questions_total)` — resolver taksonomi yang SAMA yang dipakai generator soal (Fase sebelumnya) — jadi target yang ditampilkan di dashboard adalah target yang SAMA yang dipakai AI saat generate, tidak ada tabel target terpisah yang bisa berdrift. Halaman FE memakai `<details>` per mapel (36 mapel — terlalu banyak untuk ditampilkan penuh sekaligus) dengan badge amber untuk sel bloom/kesukaran yang menyimpang >30% dari target.

**1 perluasan kecil di luar 5 halaman sendiri, tapi diperlukan agar DoD-nya benar-benar terpenuhi**: `app/(app)/organisasi/page.tsx` (konsol organisasi lama, Phase 18/33/36) sebelumnya SELALU menampilkan org milik viewer sendiri (`me.roles[0].organization_id`), tidak menerima id dari luar — sehingga tautan "tautan ke /organisasi-nya" dari halaman Organisasi Admin Pusat tidak mungkin benar-benar berfungsi untuk `platform_admin` yang membuka konsol organisasi ORANG LAIN. Ditambahkan dukungan `?org=<id>` (hanya dihormati untuk `platform_admin`, memakai gerbang backend yang sudah ada — `require_permission_in_org` sudah melewati `platform_admin` tanpa cek keanggotaan). Diverifikasi hidup: klik "Buka konsol" dari daftar organisasi Admin Pusat → benar-benar membuka konsol organisasi ITU (kode organisasi & anggota yang cocok), bukan organisasi viewer sendiri.

**Dibuktikan lewat 10 test integrasi baru** (`admin_metrics_test.rs`) + verifikasi browser penuh ke SEMUA 5 halaman dengan data dev sungguhan: gerbang izin (403 untuk peran lain di kelima endpoint), pendapatan hari ini terbaca seketika tanpa menunggu rollup, ketiga aturan peringatan, perbandingan periode (kedua kasus null vs nol), MRR = langganan aktif × harga tier, target taksonomi Bloom/kesukaran, kesehatan antrean job, dan penghitungan anggota organisasi (mengecualikan organisasi semu `type='platform'`). Verifikasi browser: kelima halaman menampilkan data nyata dari database dev (23 pendaftar 7 hari, Rp100.000 pendapatan bulan ini, 481 panggilan AI dengan 10,4% gagal, 36 mapel dengan cakupan sungguhan termasuk Matematika Tahap 1 yang memang punya konten asli, daftar organisasi QA sungguhan) — termasuk tampilan ponsel (390px, tanpa terpotong) dan mode gelap (sudah demikian sejak dibangun).

`cargo test --lib` 229 lulus (tidak berubah). `cargo test --test integration` penuh: **149 lulus, 26 gagal — daftar sama persis**, tidak bertambah (149 = 139 sebelumnya + 10 baru). `npx tsc --noEmit` dan `npx eslint` bersih.

- API baca `GET /admin/metrics/{halaman}?from&to` dari agregat, ditambah "hari ini" dari query ringan berindeks.
- **Ringkasan**: pendaftar baru, pendapatan hari ini/bulan ini, langganan aktif, cakupan kurikulum, biaya AI 7 hari, dan peringatan aturan dasar (ADR-0014 §4: pendapatan turun >40% vs rata-rata 7 hari, tingkat gagal AI >10%, antrean job macet >1 jam).
- **Penjualan**: pendapatan per `orders.kind`, MRR, langganan baru/berhenti, GMV marketplace, diamond masuk/terpakai (`transactions`), iklan ditonton.
- **Kurikulum & Konten**: cakupan per mapel → tahap (topik berisi Modul Belajar + latihan dari total), sebaran Bloom & kesukaran per tahap **dibanding target** `quiz_taxonomy::target_spread`, dan progres generate.
- **Operasional AI**: panggilan/token/biaya per peran & model, tingkat gagal, dan kesehatan antrean `jobs`.
- **Organisasi**: daftar organisasi + jumlah anggota & aktivitas, tautan ke `/organisasi`.
- Setiap angka punya pembanding periode sebelumnya. Data yang belum cukup ditampilkan "belum cukup data", bukan nol.
- Halaman **Peserta aktif, Pembelajaran, Kelas & Guru** tampil di sidebar dengan status "tersedia setelah Phase 39".

DoD: cek di browser setiap halaman dengan data dev sungguhan (angka cocok dengan query SQL manual); tampilan ponsel tidak terpotong; dark mode terbaca.

---

## Urutan & ukuran

| Tiket | Ukuran | Bergantung |
|---|---|---|
| P40-001 kerangka, izin, audit | S | — |
| P40-002 antrean job + worker | M | — |
| P40-003 Pengaturan AI | M–L | 001 |
| P40-004 agregat harian | M | 002 |
| P40-005 halaman dashboard | L | 001, 003, 004 |

Setelah Phase 39 selesai: halaman Peserta aktif & retensi, Pembelajaran, Kelas & Guru (ADR-0014 §6 langkah 5). Phase 42: halaman Usulan AI.
