# Phase 38 — Quiz Builder setara parelabs (config, generate & integrasi AI, UI/UX)

📋 **RENCANA — belum dieksekusi.** Dianalisis 2026-09-11 (Opus), untuk dieksekusi fase demi fase (Sonnet).

Cara eksekusi: kerjakan **satu fase sampai DoD-nya lolos**, baru lanjut. Setiap fase bisa dirilis sendiri. Kalau menemui keputusan di bagian "Keputusan terbuka", pakai **default** yang tertulis kecuali user sudah menjawab lain.

---

## 1. Ringkasan temuan

Perbandingan langsung kode `parelabs` (`app-parelabs-v2` + `parelabs-backend/api`) dengan Titian (`titian-web` + `titian-backend-rust`):

1. **Model data sudah setara.** `QuizConfig` Titian (`titian-web/src/lib/api-client.ts` ±L1357–1476) sudah punya hampir semua field parelabs: `timer_mode` (global/section/question/audio), `max_duration_seconds`, `audio_auto_sequence(+_gap_seconds)`, `audio_timer_buffer_seconds`, `passing_score`, `shuffle_questions`, `show_guide`, `theme` (default/ielts/pte), section bersarang (`parent_section_id`, `duration_seconds`), dan di tiap group: `context_prompt`, `reference_module_item_ids`, `target_tests`, `module_skill_codes`, `display_mode`, `widget`, `codeweb_*`, `ai_meta`, pengaturan audio.
2. **Builder tidak mengekspos sebagian besar field itu.** Tidak ada panel Pengaturan Kuis sama sekali. Di level group/section, UI hanya ada untuk `audio_max_plays/audio_speed/audio_show_transcript` — `context_prompt`, `target_tests`, referensi item, skill, speakers/tts_context, durasi section tidak bisa diisi.
3. **Runtime siswa mengabaikan setting.** `shuffle_questions`, `show_guide`, `passing_score`, `audio_auto_sequence`, `duration_seconds` section: **0 referensi** di `components/exercise/*`. `quiz-attempt.tsx` tidak punya timer sama sekali. Tema IELTS/PTE belum ada. Parelabs (`kuis-umum/page.tsx` + `themes/ielts`, `themes/pte`) sudah punya semuanya.
4. **Endpoint AI kurang 5.** Titian: `POST /ai/generate-quiz-group` (mode replace/append/rewrite/answer_only + ekstraksi dari gambar). Parelabs tambahan: `generate_batch`, `edit_question` (instruksi bebas), `parse_raw` (Tempel & Parse), `suggest_group_types` (dokumen → manifest), `convert_group_type`, plus pemilih model per group dan potong kredit per panggilan.
5. **Template:** Titian 59 template / 19 folder — lebih kaya untuk Indonesia (AKM, CPNS, BUMN, OSN, UMPTKIN, Mandiri) dan bahasa (HSK, JLPT, Goethe, DELF, TOPIK), tapi tipis di IELTS (4 vs 30), TOEFL (2 vs 20), TOEIC (1 vs 12), PTE (1 vs 15), Psikotes (1 vs 6). Parelabs juga punya 13 full-mock. UI template Titian cuma daftar polos — tanpa cari, tanpa panel detail.
6. **Sudah ada fondasi yang tinggal dipakai:** `POST /documents/extract` (PDF/DOCX → teks, `handlers/document.rs`, batas 12 MB), `lesson_plan_ai::referenced_items_block` (menyuntik isi item lain ke prompt), `GenerationProgress` (`components/studio/lesson-plan/generation-progress.tsx`), `MentionTextarea`/`SiblingItem` untuk memilih item modul.
7. **"Maks. Percobaan" belum ada** di Titian (tidak di `item_guard`, tidak di runtime).

## 2. Matriks paritas

| Area | Parelabs | Titian sekarang | Fase |
|---|---|---|---|
| Panel Pengaturan Kuis (mapel, topik, tingkat, bahasa, tampilan, mode timer, durasi, buffer audio, nilai lulus, acak grup, halaman panduan, audio berurutan) | ✅ | ❌ (field ada, UI tidak) | 1 |
| Instruksi Tugas (rich) | ✅ | ❌ | 1 |
| Maks. Percobaan | ✅ | ❌ | 1 + 2 |
| Onboarding kosong 4 kartu (Template / Impor dokumen / Kosong / Section) | ✅ | ❌ | 1 |
| Runtime: timer 4 mode + auto-submit, halaman panduan, acak, nilai lulus | ✅ | ❌ | 2a |
| Runtime: mode ujian audio (berurutan, batas putar, jeda), tema IELTS/PTE | ✅ | ❌ | 2b |
| Section: urut, duplikat, sub-bagian, durasi, target tes, konteks AI | ✅ | sebagian (judul, bacaan, audio) | 3 |
| Group: nomor urut, judul, naik/turun, duplikat, pindah section, collapse, pratinjau, edit JSON | ✅ | ❌ (hanya hapus) | 3 |
| Soal: urut, duplikat, timer per soal | ✅ | ❌ | 3 |
| Library tipe soal: cari, chip kategori + jumlah, badge, **demo interaktif 3 keadaan** | ✅ | tab kategori saja | 4 |
| Template browser: pohon folder + subfolder, cari, panel detail struktur + konteks AI | ✅ | daftar polos | 4 |
| Katalog template setara (IELTS/TOEFL/TOEIC/PTE/Psikotes) | 98 + 13 full-mock | 59 | 4 |
| Petunjuk untuk AI per group (tersimpan), referensi item modul, target tes | ✅ | ❌ (brief tidak disimpan) | 5a |
| Pemilih model AI per group | ✅ | ❌ (1 model global) | 0 + 5a |
| Generate semua group kosong (batch) | ✅ | ❌ | 5b |
| Edit soal dengan instruksi bebas | ✅ | rewrite/answer_only tanpa instruksi | 5b |
| Tempel & Parse | ✅ | ❌ | 5b |
| Impor dari dokumen (flat + multi-section) & generate group dari dokumen | ✅ | ❌ (ekstraksi dari **gambar** sudah ada) | 5c |
| Ubah tipe group | ✅ | ❌ | 5b |
| Draft AI: Setujui/Tolak per group + massal | ✅ | ❌ | 5d |
| Simpan ke bank soal | ✅ | ❌ (bank soal Titian ada, terpisah) | 6 |
| Bantuan Prompt AI per format ujian | ✅ (IELTS) | ❌ | 6 |
| Kredit AI penulis | ✅ | ❌ (tidak dimeter) | Keputusan |

## 3. Yang WAJIB dipertahankan dari Titian

- Kategori subject-neutral & copy Bahasa Indonesia (penulis Matematika/Psikotes tidak disodori label "reading/vocabulary").
- Template Indonesia yang sudah ada (AKM, CPNS, BUMN, OSN, SNBT, TKA, UMPTKIN, Mandiri) dan bahasa (HSK, JLPT, Goethe, DELF, TOPIK, Duolingo).
- Ekstraksi soal dari foto (`asset_id` → `ai_ocr_model`), aksi per soal "Buatkan kunci & pembahasan" / "Tulis ulang".
- `validate_structure` (blocking, di PATCH) vs `find_issues` (non-blocking, di QA) — lihat bug #4 phase-37.
- ADR-0008 (item published read-only), izin `require_permission(ModuleItem, Create)` + `module_item::can_edit_item`, share grant `editor`.
- Aturan Akses & Guard, Attendance Guard, Proctor (`item_guard.rs`, `item_proctor.rs`, `proctored-quiz.tsx`) — runtime baru harus tetap lewat jalur ini.
- Konten kaya pakai **ALM** (`AlmField`), bukan PCF parelabs.
- Autosave (debounce 1.5 s, full-replace PATCH) di semua perubahan.
- Desain Titian: token `primary` emas, `Card`/`Badge`/`Button`, `rounded-2xl`, dark mode. **Jangan** bawa violet/gradient parelabs.
- Setiap panggilan AI tercatat di `ai_tasks`.

## 4. Keputusan terbuka (pakai default kalau user belum menjawab)

| # | Pertanyaan | Default |
|---|---|---|
| K1 | Generate AI oleh penulis dipotong kredit? | **Tidak** di fase ini; cukup catat token di `ai_tasks`. |
| K2 | Model apa saja di pemilih model? | Allowlist di config: `deepseek/deepseek-v4.1-flash` ("Cepat", default) dan `deepseek/deepseek-v4-pro` ("Kualitas tinggi"). Keduanya terverifikasi ada di OpenRouter. |
| K3 | Tema IELTS/PTE meniru tampilan ujian resmi? | **Ya**, tapi hanya di tampilan pengerjaan siswa (scoped), builder tetap gaya Titian. |
| K4 | Seberapa jauh katalog template diperluas? | Samakan IELTS/TOEFL iBT/ITP/TOEIC/PTE/Psikotes dengan parelabs; Olimpiade parelabs digabung ke folder OSN. Full-mock ditunda. |
| K5 | Draft AI boleh tampil ke siswa sebelum disetujui? | Boleh tersimpan, tapi **submit-review ditolak** selama masih ada draft (lewat `find_issues`). |

## 5. Aturan main eksekusi (jebakan yang sudah pernah terjadi)

- `PATCH /module-items/{id}/quiz-config` itu **full-replace**. Jangan pernah menambah validasi kelengkapan di jalur save.
- Nomor soal unik **se-dek** (lihat `nextQuestionNumber` di `quiz-builder.tsx`). Duplikat group/soal wajib me-remap nomor (port `lib/quiz/bank/remap-question-numbers.ts` parelabs).
- Endpoint yang **menulis ke DB** (generate-quiz-group) → builder memanggil `reloadFromServer`. Endpoint baru yang menghasilkan **draft** (batch, parse, dokumen, convert) sebaiknya **mengembalikan group** tanpa menulis, lalu diterapkan lewat autosave — sama seperti parelabs.
- Field baru di `quiz_config`: cek struct Rust `QuizConfig`/`QuizSection`/`QuizQuestionGroup` (dipakai `quiz_config_schema::parse`) — tambahkan field-nya, dan pastikan tidak ada `deny_unknown_fields` yang membuang data.
- Semua teks UI Bahasa Indonesia. Semua komponen dari `@/components/ui/*`.
- Verifikasi tiap fase: `cargo check`, `cargo test --lib`, `npx tsc --noEmit`, `npx eslint src`, lalu uji langsung di browser (resep sesi QA ada di memory `project_titian_dev_qa_access.md` — **minta izin user** sebelum insert refresh token, hapus setelahnya). Bersihkan data uji.
- Jangan commit kecuali user minta.

---

## Fase 0 — Fondasi AI (S)

Wajib duluan: batch generation (Fase 5) melipatgandakan dampak masalah ini.

Backend (`titian-backend-rust`):
- `services/ai_provider.rs::resolve_max_tokens` — sekarang mengembalikan batas maksimum model (384 000) dan **mengabaikan fallback**. Ubah jadi `min(fallback, model_max)`; kalau model tidak terdaftar, pakai fallback.
- `DeepSeekProvider::new` — `reqwest::Client::builder().connect_timeout(15s).timeout(240s)`.
- Retry 1× bila output gagal di-parse/divalidasi: `quiz_generation::generate_quiz_group`, `lesson_plan_ai::{generate_plan, edit_section}`. Buat helper kecil bersama; catat `ai_tasks` gagal hanya bila kedua percobaan gagal.
- Pemilih model: `config.rs` tambah `ai_generation_model_options` (daftar `id|label`, default K2). Endpoint `GET /ai/models` → daftar + default. Tambah field opsional `model` pada request generate kuis/modul; tolak (422 `model_not_allowed`) bila di luar allowlist.
- Catat `ai_tasks` untuk `alm_generation::generate_fragment` (`alm_fragment`) dan `live_chat` (`live_chat_turn`).

DoD: unit test untuk `resolve_max_tokens` (min) dan retry (pakai provider palsu yang gagal sekali lalu berhasil). Generate modul & kuis sungguhan tetap berhasil.

## Fase 1 — Pengaturan Kuis, Instruksi, Maks. Percobaan, onboarding (M)

Frontend (`titian-web/src/components/studio/quiz/`):
- `quiz-settings-panel.tsx` (baru), dirender di atas daftar soal di `quiz-builder.tsx`. Field → `QuizConfig`: Mata Pelajaran (`subject`), Topik (`topic`), Tingkat (`level`), Bahasa (`language`, pakai `PLAN_LANGUAGES`), Tampilan (`theme`), Mode Timer (`timer_mode` + penjelasan tiap mode), Durasi (`max_duration_seconds`, input menit ↔ detik), Waktu tambahan setelah audio (`audio_timer_buffer_seconds`, hanya bila mode `audio`), Nilai lulus (`passing_score`), checkbox `shuffle_questions`, `show_guide` (default true), `audio_auto_sequence` (+ jeda). Referensi: parelabs `ConfigEditor.tsx` L1700–1840.
- Instruksi Tugas: field baru `instructions` (ALM) di `QuizConfig`, editor `AlmField` yang bisa dilipat.
- Maks. Percobaan: field baru `max_attempts` (kosong = tak terbatas).
- Onboarding kosong (saat `question_groups` kosong): 4 kartu — Pakai Template, Impor dari PDF/Word (tampil setelah Fase 5c; sebelum itu sembunyikan), Mulai dari Kosong (buka library tipe soal), Buat Section. Referensi: `ConfigEditor.tsx` L2050–2100.
- Indikator simpan konsisten dengan `SaveStatus` di `lesson-plan-panel.tsx` (bukan teks "Menyimpan..." polos).

Backend: tambah `instructions`, `max_attempts` ke struct `QuizConfig`. `quiz_attempt.rs` (create attempt) tolak 422 `max_attempts_reached` bila jumlah attempt siswa ≥ `max_attempts`.

DoD: semua field tersimpan lewat autosave dan terbaca ulang setelah reload; percobaan ke-(N+1) ditolak server.

## Fase 2 — Runtime siswa menghormati setting (L)

File: `components/exercise/quiz-attempt.tsx`, `quiz-layouts.tsx`, `quiz-question-renderer.tsx`, `proctored-quiz.tsx`, `app/(app)/belajar/[itemId]/page.tsx`. Referensi: parelabs `kuis-umum/page.tsx` (timer ±22 titik, autoplay ±15).

**2a — inti**
- Halaman panduan sebelum mulai (`show_guide`, default true): judul, instruksi (ALM `instructions`), jumlah soal, durasi, nilai lulus, sisa percobaan, tombol Mulai.
- Timer: `global` (satu hitung mundur), `section` (per section, section habis → grupnya terkunci read-only, lanjut section berikut), `question` (per soal `max_duration_seconds`), `audio` (durasi = panjang audio + buffer). Habis waktu global → auto-submit. Simpan waktu mulai di attempt; server menolak submit melewati batas + 60 s toleransi.
- `shuffle_questions`: acak urutan group (seed per attempt supaya stabil saat reload).
- Layar hasil: lulus/tidak lulus terhadap `passing_score`.
- Proctor/guard tetap aktif di atas semua mode.

**2b — ujian audio & tema**
- Mode ujian audio: `audio_max_plays`, `audio_playback_mode: "exam"` (tanpa seek), `audio_auto_sequence` + jeda, `audio_show_transcript`.
- Tema `ielts` dan `pte` (header + navigasi bawah + tata letak per passage), port dari parelabs `themes/ielts/*`, `themes/pte/*`, tetap memakai renderer soal Titian. Tema hanya presentasi — skor & waktu identik.

DoD: tiap mode timer diuji di browser (termasuk auto-submit & kunci section), acak stabil setelah reload, tema IELTS/PTE tampil benar di desktop & mobile, proctor tetap memicu pelanggaran.

## Fase 3 — Struktur builder (M)

`quiz-builder.tsx`, `question-editor.tsx`:
- Section: naik/turun, duplikat (remap nomor), sub-bagian (`parent_section_id`), hapus, `duration_seconds` (tampil bila mode `section`), `target_tests` (select; menentukan bahasa generate — IELTS/TOEFL/PTE/TOEIC = English), `context_prompt` ("Konteks untuk AI Generate"), tombol "Tambah tipe soal ke bagian ini".
- Group: nomor urut `#N`, badge grading, `title`, `instruction` singkat, naik/turun, duplikat, pindah section (select), collapse ("Edit Manual" ↔ ringkas), **Pratinjau** (render `quiz-question-renderer` dalam mode siswa), "Opsi lanjutan" = edit JSON group (divalidasi `validate_structure` sebelum diterapkan). Referensi: parelabs `GroupCard.tsx`.
- Soal: naik/turun, duplikat, `max_duration_seconds` (tampil bila mode `question`).
- Port `remap-question-numbers.ts` → `titian-web/src/lib/quiz-numbering.ts`.

DoD: semua operasi lolos autosave tanpa 422; nomor soal tetap unik setelah duplikat/pindah.

## Fase 4 — Library tipe soal & Template browser v2 (M–L)

- `subtype-library-picker.tsx` (menggantikan `AddGroupDialog`): kolom cari, chip kategori dengan jumlah, badge `AUTO`/grading + tingkat kesulitan, panel kanan **demo interaktif** dengan 3 keadaan (Kosong / Sudah Dijawab / Hasil + Kunci) memakai renderer Titian. Data demo: `titian-web/src/lib/quiz-samples.ts` — satu contoh kecil per subtype (39), port dari parelabs `lib/quiz/samples.ts`, disesuaikan ke bentuk `QuizQuestionGroup` Titian. Tambah `difficulty` di registry `quiz_subtype.rs` + DTO.
- Backend template: `quiz_template.rs` tambah `difficulty`, `tags`, `duration_label`; endpoint baru `GET /quiz-templates/{id}` mengembalikan sections + groups (subtype, jumlah, instruksi, `context_prompt`).
- `template-browser.tsx` (menggantikan `TemplateDialog`): pohon folder + subfolder dengan jumlah, cari, kartu (jumlah soal, durasi, kategori, tag, tingkat), panel detail (stat group/soal/durasi, struktur group, "Konteks AI" yang bisa dibuka), tombol Terapkan (konfirmasi bila kuis sudah berisi). Referensi: parelabs `TemplateBrowser.tsx`.
- Katalog: port preset parelabs (`lib/quiz/templates/presets/{ielts,toefl_ibt,toefl_itp,toeic,pte,psikotes,olimpiade}.ts`) ke spec statis `quiz_template.rs` sesuai K4. Setiap template wajib lolos `validate_structure` — tambahkan unit test yang meng-apply semua template.

DoD: semua template ter-apply tanpa error (test), demo 39 subtype bisa diklik tanpa error console.

## Fase 5 — Paritas generate & integrasi AI (L)

**5a — field AI per group (UI + backend)**
- "Petunjuk untuk AI" = `group.context_prompt` tersimpan (dialog generate membaca & menulis field ini, bukan brief sekali pakai).
- Referensi item modul: pemilih `reference_module_item_ids` (pakai daftar sibling seperti `flattenItems` di `plan-utils.ts`). Backend `quiz_generation::build_prompt` menyuntik isinya — pakai ulang `lesson_plan_ai::referenced_items_block` (artikel → bacaan rujukan; kuis → ringkasan soal "jangan diulang").
- Pemilih model (dari `GET /ai/models`) di samping tombol "Buat Soal dengan AI".
- Tombol cepat "N soal AI" di bawah daftar soal (append tanpa buka dialog).

**5b — endpoint baru** (`handlers/ai.rs`, `services/quiz_generation.rs`; semua: izin, `ai_tasks`, retry Fase 0, model opsional). Referensi kontrak: parelabs `handlers/kuis_umum_ai.rs`.
- `POST /ai/quiz/generate-batch` — semua group yang masih kosong di satu item; konkurensi dibatasi 3; hasil per group (sukses/gagal) supaya satu kegagalan tidak membatalkan semua.
- `POST /ai/quiz/edit-question` — satu soal + instruksi bebas ("jadikan lebih sulit", "ganti konteks ke olahraga").
- `POST /ai/quiz/parse-raw` — teks mentah yang ditempel → soal sesuai subtype group ("Tempel & Parse").
- `POST /ai/quiz/suggest-group-types` — teks dokumen → manifest section + blok (subtype, jumlah, cuplikan sumber).
- `POST /ai/quiz/convert-group-type` — group → subtype lain, pertahankan konten/konteks; juga dipakai untuk membuat group dari blok dokumen.

**5c — Impor dari dokumen**
- `import-document-dialog.tsx`: unggah PDF/DOCX → `POST /documents/extract` → pilih mode **flat** (langsung jadi group) atau **multi-section** (manifest dari `suggest-group-types`, penulis meninjau/mengubah, lalu tiap blok di-`convert-group-type`, konkurensi 3). Hasil diterapkan sebagai **draft**. Referensi: parelabs `GenerateFromDocumentModal.tsx`.
- Per group: "Generate dari Dokumen" (`GenerateGroupFromDocumentModal.tsx`).

**5d — Draft AI**
- Output batch/dokumen/parse/convert diberi `ai_meta.draft = true`. Banner per group: Setujui / Edit / Tolak; aksi massal di header daftar soal: "Setujui semua draft", "Hapus semua draft", "Generate AI untuk semua group kosong".
- `quiz_config_schema::find_issues` melaporkan draft yang belum disetujui (K5).

**5e — UX progres**: pakai `GenerationProgress` untuk batch dan impor dokumen (dengan jumlah group selesai/total — ini progres nyata, bukan estimasi).

DoD: tiap endpoint diuji langsung dengan model sungguhan; impor PDF contoh (mis. `S01L-Spesimen-Dokumen-Akademik-SAMPLE.pdf` di `parelabs-workspace`) menghasilkan section + group draft yang valid; batch 5 group kosong berhasil dengan progres terlihat.

## Fase 6 — Bank soal & Bantuan Prompt (M, sebagian bergantung keputusan)

- Simpan soal group ke bank soal Titian (tabel `questions` / bank yang sudah ada — lihat `create-question-bank-dialog.tsx`, `add-question-dialog.tsx`), dan sebaliknya impor soal dari bank ke group (remap nomor). Referensi: parelabs `AddToQuestionBankModal.tsx`.
- Bantuan Prompt AI: kartu terpandu (Tes → Skill → Part → Topik/Band/Panjang) yang menyusun `context_prompt`. Data preset di `titian-web/src/lib/quiz-prompt-presets.ts`, mulai IELTS (port `ielts-prompt-presets.ts`, `ielts-question-prompt-presets.ts`), lalu SNBT, TKA, CPNS.
- (Bila K1 = ya) meter kredit penulis per panggilan AI + tampilan saldo di builder.

---

## Urutan & ukuran

0 (S) → 1 (M) → 3 (M) → 4 (M–L) → 5 (L) → 2 (L) → 6 (M).

Fase 2 sengaja setelah 5 kalau prioritasnya "siap generate"; kalau prioritasnya "siap dipakai siswa untuk ujian bertimer", kerjakan 2a tepat setelah 1.

## Peta referensi parelabs

| Fitur | File parelabs |
|---|---|
| Pengaturan, onboarding, aksi draft massal, kartu section | `app-parelabs-v2/src/components/labs/assignments/templates/simulations/kuis-umum/ConfigEditor.tsx` |
| Kartu group, pemilih model | `.../kuis-umum/GroupCard.tsx`, `src/components/ai/AiModelPicker.tsx` |
| Editor soal, Tempel & Parse | `src/lib/quiz/_helpers/QuestionsEditor.tsx` |
| Library tipe soal + demo | `.../kuis-umum/SubtypeLibraryPicker.tsx`, `src/lib/quiz/samples.ts` |
| Template | `.../kuis-umum/TemplateBrowser.tsx`, `src/lib/quiz/templates/{types.ts,presets/*.ts}` |
| Impor dokumen | `.../kuis-umum/GenerateFromDocumentModal.tsx`, `GenerateGroupFromDocumentModal.tsx` |
| Ubah tipe | `.../kuis-umum/ConvertGroupTypeModal.tsx` |
| Bantuan prompt | `.../kuis-umum/IeltsPromptHelper.tsx`, `src/lib/quiz/ielts-prompt-presets.ts` |
| Bank soal | `.../kuis-umum/AddToQuestionBankModal.tsx`, `src/lib/quiz/bank/*` |
| Runtime + tema | `.../kuis-umum/page.tsx`, `.../kuis-umum/themes/{ielts,pte}/*` |
| Endpoint AI | `parelabs-backend/api/src/handlers/kuis_umum_ai.rs` (generate L86, generate_batch L319, edit_question L496, parse_raw L578, suggest_group_types L669, convert_group_type L757), `handlers/regenerate_question.rs`, `services/quiz_prompts.rs` |
