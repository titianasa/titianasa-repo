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

Backend:
- `permissions.rs`: `Resource::AdminPusat` dengan aksi `View` dan `Manage`. Awalnya hanya `platform_admin`. Peran `pusat_*` belum dibuat, tetapi pengecekan sudah lewat satu fungsi supaya menambahkannya nanti cukup di satu tempat.
- Migrasi `admin_audit_log (id, actor_id, action, target_type, target_id, before, after, reason, created_at)` + `services/admin_audit.rs::record`.
- `GET /admin/audit-log` (paginasi).

Frontend:
- Route group `app/admin/` dengan layout sendiri: sidebar halaman sesuai ADR-0014 §2, pemilih periode (hari ini / 7 / 30 hari / rentang), dan gerbang peran lewat `lib/roles.ts`.
- Pengguna tanpa peran diarahkan keluar dengan pesan jelas, bukan layar kosong.

DoD: `platform_admin` bisa membuka `/admin`; peran lain mendapat 403 dari API dan diarahkan dari UI; setiap aksi `Manage` tercatat di log audit.

## P40-002 — Antrean job generik + scheduler (M)

- Migrasi `jobs (id, job_type, payload, priority, status, attempt, max_attempts, run_after, locked_by, locked_at, last_error, cost_tokens, created_at, finished_at)` + indeks `(status, run_after, priority)`.
- `services/job_queue.rs`: `enqueue`, `claim` (`FOR UPDATE SKIP LOCKED`), `complete`, `fail` (retry dengan jeda bertahap sampai `max_attempts`), dan `reap` untuk job yang terkunci terlalu lama.
- Binary kedua `src/bin/titian-worker.rs` di crate yang sama: loop klaim → jalankan handler sesuai `job_type` → selesai. Scheduler berkala (tokio interval) yang meng-enqueue job terjadwal secara idempoten.
- Registry `job_type` di kode (pola registry subtype soal).

DoD: unit test klaim bersamaan (dua worker tidak mengambil job yang sama), retry, dan reap; worker berjalan terpisah dari API.

## P40-003 — Pengaturan AI: katalog, peran, resolver (M–L) ⭐

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
