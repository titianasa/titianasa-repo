# Phase 39 — Fondasi Jejak Belajar (ADR-0013 L1)

📋 **RENCANA — belum dieksekusi.** Dianalisis & disetujui user 2026-09-13 (Opus), untuk dieksekusi tiket demi tiket (**Sonnet**). Dasar keputusan: [ADR-0013](../adr/0013-ai-learning-engine.md).

Cara eksekusi: kerjakan tiket **berurutan** sampai DoD-nya lolos. **P39-001 wajib duluan**, karena generate konten massal (26 topik Tahap 1, ±34 ribu soal) ditahan sampai soal punya `uid`. Fase ini bisa berjalan paralel dengan Phase 40 (Admin Pusat).

---

## 1. Tujuan

Setelah fase ini, setiap interaksi belajar yang penting meninggalkan jejak yang **merujuk konten yang tepat**:
- setiap soal punya identitas tetap,
- setiap modul yang terbit punya versi,
- mengerjakan kuis, membaca Modul Belajar, tryout, dan Live AI Chat menulis event ke `learning_events`,
- pencatatan perilaku mengikuti persetujuan pengguna (UU No. 27/2022).

Fase ini **tidak** membangun statistik, agen, atau dashboard. Itu Phase 40–42.

## 2. Yang WAJIB dipertahankan

- `learning_events` **diperluas, bukan diganti**. `mastery.rs` (ADR-0002) dan penulis lama di `assessment.rs` harus tetap jalan tanpa perubahan perilaku.
- `QuizQuestion.number` tetap label tampilan **dan** kunci jawaban attempt (`attempts.answers`). `uid` ditambahkan di sampingnya, bukan menggantikannya.
- `PATCH /module-items/{id}/quiz-config` tetap **full-replace** tanpa validasi kelengkapan (jebakan phase-38 §5).
- ADR-0008: item `published` tetap read-only di tempat. Snapshot `attempts.question_snapshot` tetap diisi.
- Event klien **tidak pernah** dipakai untuk menilai siswa.

## 3. Aturan main eksekusi

- Migrasi baru mulai `0046_*`. Semua aditif, tanpa `drop column`.
- Semua tabel/kolom baru disinkronkan ke `docs/domain-model.md`; endpoint baru ke `docs/api-contract.md` (protokol agen).
- Verifikasi setiap tiket: `cargo test --lib`, test integrasi yang relevan (`cargo test --test integration <modul>::`, **bukan** seluruh suite; disk pernah penuh karenanya), `npx tsc --noEmit`, `npx eslint`, lalu cek di browser dengan `Bun.WebView` (`agent/tools/qa/webview.ts`). **Minta izin user** sebelum membuat token QA, dan hapus setelahnya.
- Jangan commit kecuali user minta.

---

## P39-001 — `uid` tetap untuk setiap soal (S) ⚠️ prasyarat generate massal

Backend:
- `services/quiz_config.rs::QuizQuestion`: tambah `uid: Option<Uuid>` dan `derived_from_uid: Option<Uuid>` (`skip_serializing_if = None`).
- Satu fungsi `ensure_question_uids(config: &mut QuizConfig)`: memberi `uid` baru pada soal yang belum punya, dan **memberi `uid` baru pada kemunculan kedua** bila ada dua soal ber-`uid` sama dalam satu deck (hasil duplikat). Dipanggil di:
  - `module_item::update_quiz_config` (sebelum simpan),
  - `quiz_generation::merge_into_group` (soal hasil generate),
  - `quiz_template` apply.
- Mode `rewrite` di `quiz_generation`: soal hasil tulis ulang mendapat `uid` baru dengan `derived_from_uid` = `uid` lama. Mode `answer_only` mempertahankan `uid`.
- `quiz_attempt::submit_quiz_attempt`: `question_snapshot` ikut menyimpan `uid` per soal.
- Migrasi backfill: satu kali, beri `uid` ke semua soal di `module_items.quiz_config` yang ada (SQL `jsonb` atau job Rust kecil yang lewat `ensure_question_uids`).

Frontend (`titian-web`):
- `api-client.ts::QuizQuestion`: tambah `uid?`, `derived_from_uid?`.
- `quiz-builder.tsx::duplicateQuestion` dan duplikat grup: **hapus `uid`** dari salinan, supaya server memberi yang baru.

DoD:
- Unit test: soal tanpa uid mendapat uid; menata ulang/menomori ulang/mengedit **tidak** mengubah uid; duplikat mendapat uid baru; rewrite mengisi `derived_from_uid`.
- Backfill: 0 soal tanpa `uid` di DB.
- Hapus soal #1 di builder → nomor bergeser, tetapi `uid` soal lain **tetap sama** setelah reload.

## P39-002 — Versi konten `module_items` (M)

- Migrasi `module_item_versions (id, item_id, version, lesson_plan, quiz_config, content_hash, created_by, created_via, change_summary, published_at, superseded_at)` + unik `(item_id, version)`.
- `module_items.current_version int` (null = belum pernah terbit).
- `module_item::publish`: bekukan snapshot `lesson_plan`/`quiz_config` sebagai versi baru, isi `superseded_at` versi sebelumnya, dan naikkan `current_version`. `created_via` = `human | ai_generation | ai_proposal` (turunan dari `generated_by` untuk sekarang).
- Backfill: item yang sudah `published` mendapat versi 1.
- Endpoint baca: `GET /module-items/{id}/versions` (daftar) dan `GET /module-items/{id}/versions/{n}`.

DoD: publish dua kali menghasilkan versi 1 & 2 dengan snapshot yang benar; attempt yang dibuat di antara keduanya mencatat versi yang berlaku saat itu.

## P39-003 — `learning_events` v2 + registry event (M)

- Migrasi aditif ke `learning_events`: `source`, `session_id`, `org_id`, `module_item_id`, `content_uid`, `content_version`, `occurred_at`, `client_event_id` (unik per `user_id`), `schema_version`. Default untuk baris lama: `source='practice'`, `schema_version=1`.
- **Partisi bulanan** (`created_at`). Migrasi memindahkan 16 baris lama ke tabel terpartisi. Ada job/fungsi pembuat partisi bulan berikutnya.
- `services/learning_event.rs` (baru): registry `EventType` → skema payload yang divalidasi, sumber yang diizinkan (`server` / `client`), dan satu fungsi `record(pool, ctx, event)`. Event tak dikenal → error, tidak disimpan diam-diam.
- Penulis lama di `assessment.rs` dipindah ke `learning_event::record` **tanpa mengubah payload** yang dibaca `mastery.rs`.
- Indeks: `(user_id, created_at)`, `(module_item_id, content_uid)`, `(event_type, created_at)`.

DoD: unit test registry (payload valid/invalid, idempotensi `client_event_id`); test integrasi mastery yang ada tetap lulus.

## P39-004 — Event server: kuis, modul, tryout (M)

Semua lewat `learning_event::record`, di service yang sama yang menjalankan aksinya:
- `quiz_attempt::submit_quiz_attempt`: `quiz_attempt_submitted` (skor, durasi, `content_version`), dan **satu `question_answered` per soal** (`content_uid` = uid, benar/salah/parsial, jawaban terpilih termasuk label pengecoh, waktu per soal bila dikirim klien). `source` = `tryout` bila item di bawah sesi ujian/proctor, selain itu `practice`.
- `item_progress`: `module_item_completed`.
- `quiz_attempt::grade_manual_group`: `question_graded` untuk soal yang dinilai manual.
- Tryout: `exam_session` mulai/selesai.

DoD: satu attempt kuis 5 soal menghasilkan 1 `quiz_attempt_submitted` + 5 `question_answered` dengan `content_uid` & `content_version` benar; tryout ber-`source='tryout'`.

## P39-005 — Telemetri klien `POST /events` (M)

Backend:
- `POST /events` menerima batch ≤50 event. Hanya event berlabel `client` di registry. Divalidasi, dibatasi laju per pengguna, idempoten lewat `client_event_id`, dan `occurred_at` dibatasi ke rentang wajar (tidak di masa depan, tidak lebih dari 7 hari lalu).

Frontend:
- `lib/telemetry.ts`: antrean di memori, dikirim setiap 10 detik, saat `visibilitychange` → hidden (`navigator.sendBeacon`), dan saat navigasi. Tidak mengirim apa pun tanpa persetujuan (P39-007).
- Reader Modul Belajar (`components/belajar/lesson-plan/reader.tsx`): `section_viewed` (masuk viewport), `section_read` (waktu aktif per bagian, berhenti saat tab tidak aktif), `section_scroll_depth`.
- Kuis (`components/exercise/quiz-attempt.tsx`): `question_viewed`, `answer_changed`, `hint_opened`, dan waktu per soal (dikirim bersama submit untuk P39-004).

DoD: membaca satu Modul Belajar 5 bagian menghasilkan event per `section_id` dengan waktu aktif yang masuk akal (tab disembunyikan tidak dihitung); tanpa persetujuan tidak ada request `/events`.

## P39-006 — Live AI Chat disimpan (S)

- `services/live_chat.rs`: tetap stateless untuk percakapannya, tetapi setiap giliran siswa menulis `live_chat_question` (`module_item_id`, `section_id`, teks pertanyaan, `content_version`) ke `learning_events` dengan `source='live_ai_chat'`.
- Hanya bila pengguna memberi persetujuan (P39-007). Teks pertanyaan dibatasi panjangnya; tidak menyimpan jawaban AI.
- `chat-room.tsx` mengirim `section_id` yang sedang dibuka.

DoD: bertanya 3 kali di bagian 2 menghasilkan 3 event ber-`section_id` benar; tanpa persetujuan tidak ada yang tersimpan, tetapi chat tetap berfungsi.

## P39-007 — Persetujuan data & retensi (S–M)

- Migrasi `user_data_consents (user_id, kind, granted, granted_by, guardian_confirmed, granted_at, revoked_at)`. `kind`: `learning_analytics`, `ai_chat_storage`.
- Onboarding (`app/mulai`) & Profil: pilihan persetujuan dengan bahasa sederhana. Untuk jenjang SD/SMP (`user_learning_profiles.jenjang`) wajib konfirmasi orang tua/wali.
- `learning_event::record` memeriksa persetujuan untuk event non-otoritatif. Event server yang wajib (penilaian, pembelian) tetap dicatat.
- Retensi: job (atau `pg_cron` fallback) yang menghapus partisi event mentah >24 bulan. Hapus akun → hapus event mentah pengguna.

DoD: pengguna tanpa persetujuan hanya menghasilkan event server wajib; mencabut persetujuan menghentikan telemetri saat itu juga.

---

## Urutan & ukuran

| Tiket | Ukuran | Bergantung |
|---|---|---|
| P39-001 uid soal | S | — |
| P39-002 versi modul | M | — |
| P39-003 learning_events v2 | M | — |
| P39-004 event server | M | 001, 002, 003 |
| P39-005 telemetri klien | M | 003, 007 |
| P39-006 Live AI Chat disimpan | S | 003, 007 |
| P39-007 persetujuan & retensi | S–M | 003 |

Setelah **P39-001** selesai, generate 26 topik Tahap 1 boleh dilanjutkan (`agent/tools/content-gen/generate_bab_content.py`).
