# Phase 37 — Konten Artikel/Kuis, mereplikasi sistem kuis parelabs-backend

🟢 **SELESAI** — inti (backend penuh + authoring/learner UI) selesai dan teruji langsung (2026-09-08). Beberapa follow-up disebutkan eksplisit di bagian bawah.

Rencana lengkap (disetujui user lewat plan mode): `/home/john/.claude/plans/wild-brewing-hummingbird.md`.

---

## Keputusan scope (baca duluan)

Content Studio sebelumnya cuma punya 6 pilihan "Tipe" konten item: `learn/practice/speaking/writing/review/assessment` — semua bahasa-Inggris-spesifik, dipaksakan ke SEMUA modul termasuk yang bukan bahasa Inggris. User minta cuma 2: **Artikel** dan **Kuis**, dengan Kuis mendukung banyak variasi soal, referensi eksplisit ke sistem kuis umum di `parelabs-backend` (proyek saudara, stack sama: Rust/Axum/sqlx/Postgres).

Riset ke `parelabs-backend` menemukan sistem kuisnya BUKAN satu skema raksasa kaku — cuma segelintir "field primitive" bersama (`prompt`, `choices`, `pairs`, `passages/headings`, `media_url`, `rubric`, dst) yang dikomposisi beda-beda per **subtype**, lewat registry (`SubtypeId`, ~40 nilai, 6 family: reading/listening/grammar/vocabulary/production/interactive). Satu item kuis punya satu JSONB config berisi `sections[]` (media/passage bersama, timer opsional) dan `question_groups[]` (masing-masing ditandai subtype + section_id). Ini PERSIS idiom registry yang sudah 2x dipakai di Titian sendiri (`block_schema.rs`, `question_schema.rs` — `match r#type`, divalidasi di kode, TANPA DB CHECK) — jadi fase ini memperluas pola yang sudah terbukti, bukan bikin baru.

User secara eksplisit memilih opsi paling besar dari 2 pertanyaan scoping: **force-migrate** (6 tipe lama pensiun total, bukan dipertahankan paralel) dan **~40 subtype penuh dibangun sekarang** (bukan versi kecil ~6 subtype dulu).

## Pemetaan migrasi (6 lama → 2 baru)

- `learn`/`practice`/`review` → `article` (sudah cuma render content_blocks, rename tanpa kehilangan apa pun).
- `assessment` → `quiz` (config kosong — 0 baris nyata di DB dev saat migrasi jalan, jadi tidak perlu backfill kompleks dari `assessment_embed` block).
- `writing` → `quiz`, 1 section + 1 question_group subtype `essay`, prompt diambil dari content_block text/heading pertama item (fallback ke title).
- `speaking` → `quiz`, subtype `voice_record`, prompt dari block `speaking_prompt` (fallback ke title) — diverifikasi langsung: 1 baris nyata ("Listening Unit 1") ter-backfill benar.
- Grading `essay`/`voice_record` TETAP pakai jalur AI-rubric yang sudah ada (`ai_writing_evaluation`/`ai_speaking_evaluation`) — dipakai ulang, bukan ditulis ulang, cuma dialamatkan per-subtype sekarang bukan per-item-content_type.
- `questions.type`: `mcq`→`multiple_choice`, `fill_blank`→`gap_fill` (selaras kosakata registry baru).

## Backend

- Migrasi `0038_article_quiz_content_model.sql`: kolom `module_items.quiz_config jsonb`; drop `module_items_content_type_check` (kini `module_item.rs::CONTENT_TYPES` satu-satunya validator, sama idiom no-DB-CHECK seperti `content_blocks`/`questions`); backfill sesuai pemetaan di atas.
- `services/quiz_subtype.rs` (baru): registry 40 subtype, tiap entry punya family + `grading_mode` (`Auto | AiRubric | Manual | SelfCheck`).
- `services/question_schema.rs` & `services/grading.rs`: 28 subtype `Auto` divalidasi/dinilai lewat ~9 fungsi primitive bersama (single_index, multi_index, enum_value, text_match, pairs, matching_headings, assignment_map, ordered_list, span_selection) — bukan 28 arm bertumpuk sendiri-sendiri.
- `services/quiz_config_schema.rs` (baru): validasi 1 blob `quiz_config` utuh (section id unik, question_group.section_id valid, tiap group divalidasi sesuai registry).
- `services/quiz_attempt.rs` (baru) — mesin submit/nilai KHUSUS item kuis (`module_items.quiz_config`, bukan `assessments`/`questions`): tiap question_group dinilai sesuai grading_mode-nya sendiri dalam SATU submission (Auto+AiRubric+Manual+SelfCheck campur bebas), skor akhir dirata-rata proporsional per group yang benar-benar dinilai (SelfCheck tidak ikut menimbang). Plus antrian **review manual guru** (`GET /module-items/{id}/pending-reviews`, `POST /attempts/{id}/grade`) — pakai ulang tabel `evaluations`/`feedback` yang sudah ada (`evaluator_type` sudah izinkan `'human'` sejak awal, cuma belum pernah ada kode yang menulisnya).
- `PATCH /module-items/{id}/quiz-config` (baru) — endpoint save Quiz Builder, full-replace, divalidasi via `quiz_config_schema`.
- Endpoint `POST /organizations/{id}/teachers`-style lama untuk `writing`/`speaking` item-level (`ai_writing_evaluation::submit_speaking_attempt` dkk) dihapus total (dead code, tidak ada pemanggil lagi) — `essay`/`voice_record` sekarang cuma subtype di dalam kuis.

## Frontend

- `add-module-item-dialog.tsx`: picker "Tipe" → 2 opsi (Artikel/Kuis). Item Kuis dibuat kosong (1 section default), soal ditambah sesudahnya di Quiz Builder — bukan lewat ALM editor.
- `quiz-subtypes.ts` (baru) — mirror registry backend + label Bahasa Indonesia per subtype + pemetaan ke 9 "field primitive" (sama urutan seperti backend) supaya editor/renderer tidak perlu 40 komponen bespoke.
- `components/studio/quiz/quiz-builder.tsx` + `field-primitive-editor.tsx` (baru) — authoring: section list, "Tambah soal" dikelompokkan per family, editor generik per primitive, autosave ter-debounce 1.5s (sama pola `AUTO_SAVE_DEBOUNCE_MS` yang sudah dipakai ALM editor).
- `components/exercise/quiz-attempt.tsx` + `quiz-question-renderer.tsx` (baru) — sisi siswa: render tiap section/question_group, kumpul jawaban lokal, kirim 1x lewat `POST /lessons/{id}/attempts` → `POST /attempts/{id}/submit`, layar hasil per grading_mode (auto: benar/salah, ai_rubric: skor 0-100, manual: "Menunggu guru", self_check: tanpa skor).
- `writing-attempt.tsx`/`speaking-attempt.tsx` (lama) **dihapus** — sepenuhnya digantikan subtype `essay`/`voice_record` di dalam sistem kuis baru; `speaking-recorder.tsx` (perekam audio) dipakai ulang apa adanya oleh renderer baru.
- `item-editor-pane.tsx`/`belajar/[itemId]/page.tsx`: cabang lama `writing`/`speaking` diganti 1 cabang `quiz` yang render `QuizBuilder`/`QuizAttempt`; kolaborasi Yjs (ALM) sengaja dimatikan untuk item kuis (bukan teks bebas).

## Bug nyata ditemukan & diperbaiki selama build (bukan cuma dugaan — semua dikonfirmasi lewat compile/test/API langsung)

1. **`module_item.rs::duplicate()` diam-diam membuang `quiz_config`** — struct row-nya dari sebelum kolom ini ada; menduplikasi item kuis apa pun akan menghasilkan salinan dengan config kosong tanpa soal, tanpa ada error. Diperbaiki sebelum sempat kejadian nyata.
2. **`canvas.rs` (fitur sesi menulis kolaboratif live tutor↔siswa — ditemukan saat menelusuri dependensi, bukan dari riset awal) hard-check `content_type = 'writing'`** — nilai itu tidak akan pernah ada lagi setelah migrasi, jadi fitur Canvas akan 404 permanen di setiap item pasca-migrasi. Diperbaiki: sekarang cek item `quiz` yang punya question_group subtype `essay`.
3. **Bug agregasi skor di `grade_manual_group`** — ditemukan lewat pengujian API langsung (bukan cuma baca kode): saat menghitung ulang skor gabungan setelah guru menilai bagian manual, kode awalnya memakai `groups.len() - manual_count` sebagai pembagi, yang keliru ikut menghitung group `SelfCheck` (mis. flashcard) seakan-akan itu ikut menyumbang skor sebelumnya — hasilnya skor gabungan melenceng (contoh nyata: 85.0, seharusnya 80.9). Diperbaiki dengan menghitung ulang pembagi dari jumlah group yang BENAR-BENAR `Auto`/`AiRubric` saat submit awal, lalu diverifikasi ulang lewat API menghasilkan angka yang benar.
4. **Autosave Quiz Builder menolak SELURUH quiz_config gara-gara SATU soal belum lengkap** (dilaporkan user lewat screenshot error nyata, terjadi di item "tesse" saat sedang dipakai) — `PATCH /module-items/{id}/quiz-config` awalnya memanggil validasi PENUH per-subtype (field wajib lengkap) di jalur SAVE biasa, bukan cuma di submit-review. Karena PATCH itu full-replace, satu soal baru yang belum diisi (mis. `multiple_choice_multiple` tanpa `options`) membuat SELURUH config gagal tersimpan — termasuk soal lain yang sudah valid — persis bertentangan dengan prinsip yang sudah lama dianut `content_qa.rs` sendiri ("gerbang manusia": draft boleh belum lengkap, QA cuma melapor non-blocking di submit-review). Diperbaiki: `quiz_config_schema.rs` dipecah jadi `validate_structure` (blocking, dipakai PATCH — cuma cek bentuk/id/subtype valid, TIDAK cek kelengkapan field) dan `find_issues` (non-blocking, disambungkan ke `content_qa::run_item_qa`, muncul di `qa_report.issues` persis seperti temuan grammar constitution). Diverifikasi ulang lewat API: skenario yang sama (1 soal valid + 1 `multiple_choice_multiple` kosong) sekarang berhasil tersimpan, dan submit-review berhasil pindah status ke `in_review` sambil tetap melaporkan soal yang belum lengkap di `qa_report`.

## DoD

- `cargo check` bersih, `cargo test --lib` 24/24 lolos (termasuk test baru untuk `grading.rs`, `quiz_subtype.rs`, `quiz_config_schema.rs`).
- `npx tsc --noEmit` + `npx eslint src` bersih.
- **Smoke test end-to-end nyata lewat API + browser**: item kuis lama hasil migrasi ("Listening Unit 1", subtype `voice_record`) dibuka di Quiz Builder — render benar. Item kuis baru dibuat lewat UI, `quiz_config` di-PATCH langsung lewat API berisi 4 soal (1 tiap grading_mode: `multiple_choice`/auto, `essay`/ai_rubric, `file_upload`/manual, `flashcard`/self_check) → publish → attempt disubmit dengan jawaban asli → **evaluasi AI (LLM DeepSeek) benar-benar terpanggil dan berhasil** (skor essay 72.5), auto-grading benar (multiple_choice index=1 dinilai benar), manual masuk antrian pending, self_check dilewati — skor gabungan 86.3, status `submitted` (karena masih ada yang pending). Guru menilai bagian manual (70) lewat endpoint baru → status jadi `evaluated`, skor akhir 80.9 (dikonfirmasi manual sesuai rumus setelah bug #3 diperbaiki). Sisi siswa (`/belajar/{itemId}`) dikonfirmasi lewat screenshot: keempat tipe soal tampil dan bisa diisi, tanpa error console.
- Data uji (3 item "E2E Quiz Test", attempts, evaluations, feedback, refresh token) dibersihkan total setelah verifikasi.

## Follow-up yang belum digarap (scope eksplisit, bukan kelupaan)

- **Generate Kuis dengan AI**: tab "Generate dengan AI" di Content Studio saat ini cuma menghasilkan Artikel (prosa ALM); menghasilkan `quiz_config` utuh dari topik lewat LLM adalah pekerjaan terpisah.
- **Detail evaluasi AI per-kriteria di layar hasil siswa**: `QuizSubmitResponse` cuma balikin skor `overall` per group AI-rubric (bukan breakdown 4-5 kriteria + feedback berkutip seperti yang dulu ditampilkan `WritingAttempt`/`SpeakingAttempt`) — datanya tetap tersimpan lengkap di tabel `evaluations`/`feedback`, cuma belum ada endpoint/UI yang menariknya kembali secara detail.
- **TTS per-soal untuk prompt suara**: `GET /module-items/{id}/speaking-prompt-audio` masih baca dari content_block `speaking_prompt` lama, belum terhubung ke `quiz_config.question_groups[].prompt` milik soal baru — `ai-tutor-prompt.tsx` (komponen TTS lama) jadi tidak terpakai untuk sekarang, sengaja tidak dihapus karena masih relevan untuk penyambungan ini nanti.
- **h5p / widget_interact**: belum ada renderer sisi siswa sama sekali (pesan jujur "belum tersedia", sama pola `UnsupportedBlock` yang sudah ada) — memang butuh infrastruktur widget baru, bukan sekadar primitive lain.
