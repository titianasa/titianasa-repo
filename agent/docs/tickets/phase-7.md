# Phase 7 — Assessment / Exam Engine (roadmap-Fase-5, §5.1 + §5.2)

Depends on: Phase 1 (`assessments`/`attempts`/`evaluations`/`feedback`/`rubrics`, `docs/tickets/phase-1.md`), P3-004 + P6-002 (rubric-based AI evaluation pipeline this phase reuses, not reinvents). **ADR-0011** (`agent/docs/adr/0011-level-assessment-scoring-weights.md`) — read that first, the scoring-weight decision behind P7-003 lives there, not repeated here.

Sumber utama breakdown ini: `agent/ALR_Build_Roadmap.md`'s `## FASE 5 — Assessment / Exam Engine`, dan `agent/ALR_Phase_Detail_Breakdown.md`'s `## PHASE 5 — Assessment / Exam Engine` (§5.1/§5.2/§5.3) + §2.5 (Exam Blueprint) + §2.11 (Level Assessment bobot skor) + §2.12 (English Core vs Exam Preparation).

## Keputusan scope (baca duluan)

Setelah Phase 6 (Speaking/AI Tutor) ditutup, roadmap artifact TITIAN diperbarui dan user diberi 4 opsi eksplisit lewat `AskUserQuestion` (Assessment/Exam Engine, Gamification & Economy, beresin item lepas, atau lainnya) — **user pilih Assessment/Exam Engine**. Riset ulang sumber lalu menemukan 1 keputusan arsitektur yang menurut dokumennya sendiri **wajib** diputuskan eksplisit sebelum mulai (§2.11's bobot skor Level Assessment) — ditanya langsung, **user pilih Knowledge 40% / Communication 60%** (opsi yang direkomendasikan dokumen sumber, karena ALR fokus speaking-first). Lihat ADR-0011 untuk detail lengkap keputusan itu.

**Scope ticket-phase ini = §5.1 (Exam Runtime) + §5.2 (Level Assessment) saja**, mengikuti urutan MVP-first yang eksplisit ditulis sumbernya sendiri: *"5.1+5.2 dulu (exam internal, sudah dipakai sejak Phase 1). 5.3 (IELTS/TOEFL/PTE) ditunda eksplisit sampai English Core CEFR stabil."*

**Yang SENGAJA tidak termasuk fase ini:**
- **§5.3 (IELTS/TOEFL/PTE Exam Preparation Layer)** — 14 tipe soal IELTS Reading, word-limit engine, generator Task 1/2 Writing terpisah, dll. Ditunda eksplisit oleh sumbernya sendiri, bukan keputusan sesi ini.
- **Proctoring (roadmap-Fase-9)** — `proctoring_policies`/`proctoring_sessions`/`proctoring_events` sudah ada di schema sejak ADR-0001 (migrasi awal), **tapi TIDAK disentuh sama sekali di ticket-phase ini**. Sumbernya sendiri eksplisit menaruh Proctoring paling akhir & terpisah ("privacy/consent/retention wajib didesain bersamaan, bukan ditambahkan belakangan") — dan `exam_sessions` (yang fase ini aktifkan) memang sengaja dipisah secara skema dari Proctoring sejak awal justru supaya bisa dibangun independen. Kalau nanti fase Proctoring dimulai, itu ticket-phase terpisah lagi, bukan lanjutan diam-diam dari ini.
- **Bobot per-skill granular yang bisa dikustom per-assessment** (mis. blueprint tertentu mau Vocabulary 15%/Grammar 25% dsb, bukan rata) — ADR-0011 sengaja membatasi keputusan ke 2 angka (Knowledge 40/Communication 60), pembagian di dalam tiap bucket rata dulu (lihat ADR-0011's "Decision"). Override per-assessment lewat `assessments.config` adalah perluasan additive terpisah, bukan bagian ticket ini.

**1 temuan nyata dari riset** (pola sama seperti `concept_prerequisites` sebelum P4-003): `exam_sessions`/`proctoring_*` sudah ada penuh di `src/db/schema.ts` sejak migrasi awal (ADR-0001), tapi **nol kode** (repository/service/handler) pernah menyentuhnya — dikonfirmasi lewat grep langsung sebelum ticket ini ditulis. P7-001 mengaktifkan `exam_sessions`; `proctoring_*` tetap dead sampai fase Proctoring beneran dimulai.

**1 gap arsitektur nyata lain**: `assessment_service.submitAttempt` (jalur assessment, BEDA dari jalur lesson-attempt yang P3-004/P6-002 bangun) hari ini menghitung skor cuma dari soal auto-gradable (`pointsEarned/pointsPossible`) — soal writing/speaking di dalam 1 assessment **sama sekali tidak berkontribusi ke skor maupun memicu evaluasi AI apa pun**, diam-diam diabaikan. Ini gap konkret yang bikin Communication-weighted scoring (§5.2) mustahil tanpa P7-003.

## Ticket

### P7-001 — Exam Session Runtime (§5.1)
**Status:** done (2026-09-02, `titian-backend-bun`)
**Depends on:** Phase 1 (`assessments`/`attempts`)
**Endpoint baru:** `POST /assessments/{id}/exam-sessions` (mulai sesi — bikin `exam_sessions` row + 1 `attempts` row lewat pemanggilan internal yang sama dengan `assessment_service.createAssessmentAttempt` yang sudah ada, bukan duplikasi logic), `GET /exam-sessions/{id}` (status + deadline).
**Deskripsi:** Mengaktifkan tabel `exam_sessions` yang sudah ada di schema sejak ADR-0001 tapi belum pernah dipakai kode apa pun. Menambahkan konsep "sesi ujian" (delivery/timer, terpisah dari Proctoring by design) di atas `attempts` yang sudah ada — bukan mekanisme grading baru, `POST /attempts/{id}/submit` yang sudah ada tetap 1 jalur submission yang sama.
**Acceptance Criteria:**
- [x] `exam_repository.ts` baru: `insert`/`findById`/`findActiveForAssessment`/`updateStatus` atas `exam_sessions` (Drizzle query builder, tidak ada join kompleks yang butuh raw SQL)
- [x] `exam_service.ts` baru: `startExamSession(db, ctx, assessmentId)` — baca `assessments.config.duration_minutes` (field baru di dalam jsonb yang sudah ada, tidak butuh migrasi kolom), kalau tidak ada berarti tanpa batas waktu; bikin `exam_sessions` row (`status: 'in_progress'`, `started_at: now()`) + panggil `assessment_service.createAttempt` yang sudah ada (nama asli fungsinya, bukan `createAssessmentAttempt` seperti draft awal ticket ini), attempt_id dikembalikan sekali di response `POST`
- [x] `POST /attempts/{id}/submit` yang sudah ada diperluas LEWAT HANDLER (`assessment_handler.postSubmit`), bukan `assessment_service.submitAttempt` itu sendiri — dipanggil `exam_service.recordSubmission` setelah submit assessment-path sukses, no-op kalau attempt itu bukan bagian exam_session manapun. `exam_sessions.status` di-set `'timed_out'` kalau submit lewat deadline, `'submitted'` kalau tidak — `attempts.score`/grading sama sekali tidak disentuh
- [x] Tanpa `duration_minutes` di config: behavior identik hari ini — dikonfirmasi lewat `assessment.test.ts` (Phase 1) yang tetap lulus tanpa modifikasi
**DoD:** 7 test baru (`exam-session.test.ts`) — start session tanpa duration → deadline null, submit sukses, session `submitted`; start session DENGAN duration → submit sebelum deadline `submitted`, submit setelah deadline (disimulasikan lewat update `started_at` langsung, bukan nunggu wall-clock — pola sama P5-001) tetap diterima tapi session `timed_out`; `GET /exam-sessions/{id}` balikin status+deadline benar; akses punya orang lain → 403; attempt biasa yang tidak pernah lewat exam-session → submit normal tanpa exam_sessions row terlibat; mulai sesi ke-2 saat 1 masih in-progress → 409 (sama seperti `createAttempt` biasa). Regression check eksplisit: `assessment.test.ts` (Phase 1) tetap lulus tanpa modifikasi.

**Catatan implementasi:** Korelasi attempt↔exam_session TIDAK pakai foreign key baru — `exam_sessions` tidak punya kolom `attempt_id` (schema ADR-0001 aslinya memang begitu). Sebagai gantinya `exam_repository.findActiveForAssessment` cari lewat `(assessment_id, user_id, status='in_progress')`, aman karena `assessment_service.createAttempt` sendiri sudah menolak attempt in-progress ke-2 untuk pasangan (user, assessment) yang sama — jadi maksimal 1 exam_session in-progress per pasangan itu kapan pun. `duration_minutes` dibaca dari `assessments.config` jsonb (bukan kolom baru), konsisten pola blueprint `assessments.config` yang sudah ada sejak ADR-0001. Tidak ada perubahan sama sekali ke `assessment_service.ts` — komposisi murni di level handler (`assessment_handler.postSubmit`), pola yang sama dengan alasan P3-004 memilih composition di handler (menghindari `assessment_service` bergantung ke konsep yang cuma dipakai sebagian kecil caller-nya). Route-coverage audit: 74 route (naik dari 72), 0 gap. Total sekarang **267/267 test lulus**. Tidak ada verifikasi browser — 2 endpoint baru murni backend, belum ada FE consumer (sesuai scope ticket ini, FE Exam Runtime bukan bagian Phase 7).

### P7-002 — Question skill-category tagging (§5.2 foundation)
**Status:** done (2026-09-02, `titian-backend-bun`)
**Depends on:** -
**Endpoint baru:** tidak ada — field baru di body `POST /question-banks/{id}/questions` yang sudah ada (P1-004), sama pola `cefr_tag` (P2-014).
**Deskripsi:** ADR-0011 butuh tahu bucket mana (Knowledge vs Communication) dan sub-skill mana (vocabulary/grammar/reading/listening/writing/speaking/pronunciation) tiap soal termasuk, buat menghitung skor komposit P7-003. `concepts.type` (`grammar`/`vocabulary`/`skill`/`pronunciation`) terlalu kasar — `'skill'` jadi tempat sampah buat reading/listening/writing/speaking sekaligus, tidak bisa dibedakan. Menambah kolom baru di `questions`, TIDAK mengubah `concepts.type` sama sekali (tidak menyentuh containment/prerequisite semantics yang dikunci ADR-0007).
**Acceptance Criteria:**
- [x] Migrasi baru: `questions.skill_category` (nullable text, `CHECK IN ('vocabulary','grammar','reading','listening','writing','speaking','pronunciation')`) — additive, pola persis `cefr_tag` (migration 0015, P2-014), tidak butuh ADR baru (bukan perubahan struktural ke tabel yang dikunci `docs/STATE.md`'s "JANGAN lakukan ini tanpa ADR baru")
- [x] `question_service.createQuestion` terima `skillCategory` opsional, tervalidasi terhadap daftar di atas kalau diisi (validasi konstanta lokal, bukan `question_schema.ts` — lihat catatan implementasi)
- [x] `GET /questions/{id}` (authoring) dan `GET /question-banks/{id}/questions` (list) menyertakan `skill_category` di response
- [x] Soal yang sudah ada (tanpa `skill_category`, NULL): tidak error di mana pun, cuma tidak ikut dihitung ke bucket manapun oleh P7-003 (dianggap "belum ditag", bukan default ke salah satu bucket secara diam-diam)
**DoD:** test backend baru — create question dengan `skill_category` valid tersimpan+kebaca balik; nilai di luar daftar ditolak `422`; soal lama (NULL) tetap kebaca normal di endpoint yang sudah ada, regresi nol terhadap `question-bank.test.ts` (Phase 1) yang sudah ada.

**Catatan implementasi:** Validasi `skill_category` ditaruh sebagai konstanta lokal `SKILL_CATEGORIES` + cek langsung di `question_service.createQuestion` — BUKAN di `question_schema.ts` seperti draft awal ticket ini, karena modul itu validator bentuk-jawaban per tipe soal (mcq/fill_blank/matching), bukan tempat buat 1 field enum lepas; pola ini konsisten cara input enum-ish lain divalidasi di codebase (`AppError.unprocessableEntity` langsung di service). `questionRepository.insert` dapat parameter baru `skillCategory: string | null = null` (default supaya caller lama tidak perlu berubah kalau memang tidak butuh field ini). 1 caller lain ditemukan lewat `tsc` (bukan digrep manual): `ai_content_service.ts`'s AI question generation — diteruskan `skillCategory: null` eksplisit (AI generation tidak menentukan skill category, di luar scope pipeline itu; tag manual lewat endpoint authoring kalau dibutuhkan). 4 test baru (`question-skill-category.test.ts`). Route-coverage tetap 74 route (field baru di body, bukan route baru). Total sekarang **271/271 test lulus**. Tidak ada verifikasi browser — field baru murni backend, Question Bank UI (`titian-web`) belum diperbarui buat mengekspos input ini (di luar scope Phase 7, yang murni backend).

### P7-003 — Level Assessment composite scoring: Knowledge 40% / Communication 60% (§5.2 core, ADR-0011)
**Status:** todo
**Depends on:** P7-002 (`skill_category`), P3-004 + P6-002 (rubric evaluation pipeline yang di-reuse)
**Endpoint baru:** tidak ada — mengubah behavior `POST /attempts/{id}/submit` untuk assessment ber-`type = 'level_assessment'` SAJA; `unit_test`/`mock_exam` tidak berubah sama sekali.
**Deskripsi:** Inti ADR-0011. Assessment ber-`type = 'level_assessment'` sekarang menghitung skor komposit: soal auto-gradable (vocabulary/grammar/reading/listening lewat `skill_category`) dihitung persis seperti sekarang (`pointsEarned/pointsPossible`) jadi skor **Knowledge**; soal writing/speaking (`skill_category` writing/speaking/pronunciation) memicu evaluasi AI per-soal (bukan per-attempt seperti jalur lesson) jadi skor **Communication**; `attempts.score` akhir = `Knowledge*0.4 + Communication*0.6` (ADR-0011).
**Acceptance Criteria:**
- [ ] `evaluations` dapat kolom baru `question_id` (nullable UUID, additive — precedent sama `cefr_tag`/`skill_category`, bukan perubahan struktural yang butuh ADR) — evaluasi lesson-attempt (P3-004/P6-002) tetap `question_id: NULL` (1 evaluation = 1 attempt, tidak berubah), evaluasi baru dari ticket ini SELALU mengisinya (1 evaluation per soal writing/speaking di dalam 1 assessment attempt)
- [ ] `assessment_service.submitAttempt` cabang baru, aktif HANYA kalau `assessments.type === 'level_assessment'`: soal dengan `skill_category` di `{vocabulary,grammar,reading,listening}` dihitung ke `knowledgePointsEarned`/`knowledgePointsPossible` (logic sama existing); soal dengan `skill_category` di `{writing,speaking,pronunciation}` — kalau ada `answer_text`/`answer_audio_asset_id` di jawaban submit — memanggil evaluasi AI per-soal (reuse prompt/rubric `ai_writing_evaluation_service`/`ai_speaking_evaluation_service` yang sudah ada, dipanggil per-soal bukan per-attempt, tulis 1 `evaluations` row per soal dengan `question_id` terisi) menghasilkan `communicationPointsEarned`/`communicationPointsPossible`
- [ ] Soal tanpa `skill_category` (NULL) di dalam sebuah `level_assessment`: **tidak dihitung ke bucket manapun** (dikeluarkan dari `pointsPossible` kedua bucket, bukan didefault ke salah satu) — dicatat sebagai warning di response (field baru `unscored_question_ids`, kalau ada), supaya penulis blueprint tahu soal itu perlu ditag, bukan diam-diam salah hitung
- [ ] `attempts.score` final = `(knowledgeScore * 0.4) + (communicationScore * 0.6)` kalau kedua bucket punya `pointsPossible > 0`; kalau salah satu bucket kosong (mis. assessment cuma auto-gradable, tidak ada soal writing/speaking sama sekali), fallback ke bucket yang ada 100% bobotnya (jangan kalikan 0.4/0.6 lalu kehilangan setengah skor gara-gara 1 bucket kosong)
- [ ] Evaluasi AI yang gagal (STT/parse gagal, pola sama P3-004/P6-002): soal itu dikeluarkan dari `communicationPointsPossible` (bukan dihitung salah/0), attempt tetap `submitted`/`evaluated`, tidak pernah gagal total gara-gara 1 evaluasi AI error — gerbang manusia yang sama persis prinsipnya dengan P3-004/P6-002
- [ ] `unit_test`/`mock_exam` (semua assessment yang sudah ada di data manapun hari ini): **behavior identik**, cabang baru ini tidak pernah tersentuh — regresi nol dikonfirmasi lewat test yang sudah ada, bukan diasumsikan
**DoD:** test backend baru (`level-assessment-scoring.test.ts`, `FakeAIProvider`) — assessment `level_assessment` campuran (2 soal grammar auto-graded + 1 soal writing) → skor komposit sesuai formula, `evaluations` row baru muncul dengan `question_id` terisi; assessment tanpa soal Communication sama sekali → skor 100% dari Knowledge (bukan dikali 0.4); soal tanpa `skill_category` → masuk `unscored_question_ids`, tidak mempengaruhi skor; evaluasi AI gagal 1 soal → attempt tetap sukses, soal itu dikeluarkan dari `communicationPointsPossible`. Regression check eksplisit: `assessment.test.ts` (Phase 1) dan test writing/speaking evaluation (P3-004/P6-002) tetap lulus tanpa modifikasi.

### P7-004 — Integration test suite + exit checkpoint
**Status:** todo
**Depends on:** P7-001, P7-002, P7-003
**Deskripsi:** Pola sama tiap ticket-phase sebelumnya — route-coverage audit, checkpoint end-to-end yang menyatukan §5.1 (sesi+timer) dan §5.2 (skor komposit) dalam 1 skenario nyata.
**Acceptance Criteria:**
- [ ] Route-coverage audit (`grep`-based, pola P2-017/P3-005/P4-005/P5-003/P6-005)
- [ ] Checkpoint baru: buat 1 `level_assessment` blueprint — 4 soal Knowledge (2 grammar, 1 reading, 1 listening, semua mcq/fill_blank) + 2 soal Communication (1 writing, 1 speaking) via `skill_category`. Mulai lewat `POST /assessments/{id}/exam-sessions` (P7-001), jawab semua soal lewat `POST /attempts/{id}/submit`, assert: `attempts.score` cocok formula `Knowledge*0.4 + Communication*0.6` (dihitung manual dari `evaluations` yang tersimpan, bukan ditebak), `exam_sessions.status = 'submitted'` (bukan `timed_out`, karena dijawab dalam waktu). Skenario ke-2: assessment yang sama tapi durasi 0 menit (deadline sudah lewat sejak start) → submit tetap diterima, `exam_sessions.status = 'timed_out'`.
**DoD:** `bun test` hijau penuh di `titian-backend-bun` (lokal — CI masih P0-010 yang tertunda).

---

## Checkpoint keluar Phase 7 (harus bisa didemo, bukan asumsi)
1. [ ] `exam_sessions` (dead sejak ADR-0001) sekarang benar-benar dipakai — sesi ujian bisa dimulai, disubmit, dan auto-timeout dideteksi dengan benar, dibuktikan lewat test.
2. [ ] `unit_test`/`mock_exam` (assessment biasa, dipakai sejak Phase 1/3) **behave identik** seperti sebelum Phase 7 — dikonfirmasi lewat regresi test `assessment.test.ts` yang tidak diubah sama sekali.
3. [ ] 1 `level_assessment` nyata dengan campuran soal Knowledge + Communication menghasilkan skor komposit yang cocok persis formula ADR-0011 (Knowledge 40% / Communication 60%), dibuktikan lewat evaluasi AI asli (bukan cuma `FakeAIProvider`) di setidaknya 1 verifikasi manual.
4. [ ] §5.3 (IELTS/TOEFL/PTE) dan Proctoring (roadmap-Fase-9) **tetap tidak tersentuh** — dikonfirmasi lewat route-coverage audit (tidak ada endpoint baru untuk keduanya) dan grep `proctoring_*` (masih nol referensi kode di luar `schema.ts`).

Kalau salah satu poin di atas belum jalan end-to-end, jangan lanjut ke prioritas berikutnya (Gamification & Economy, item lepas, atau §5.3/Proctoring) walau ticket lain kelihatan sudah "done" — sama semangatnya dengan aturan checkpoint di Phase 1-6.

---

## Strategi eksekusi (urutan sesi yang disarankan)

| Sesi | Ticket | Fokus | Kenapa dikelompokkan begini |
|---|---|---|---|
| 1 | P7-001 | Exam Session Runtime (backend) | Independen dari P7-002/003 — mengaktifkan tabel yang sudah ada, tidak butuh skema baru apa pun. Scope paling kecil dan paling aman, cocok dikerjakan duluan. |
| 2 | P7-002 | Question skill-category tagging (backend) | Fondasi murni buat P7-003 — kolom baru + validasi, tidak ada logic skor sama sekali di sini, sengaja dipisah dari P7-003 supaya tiap ticket tetap kecil dan gampang dites terpisah. |
| 3 | P7-003 | Composite scoring §5.2 (backend, ADR-0011) | Ticket paling besar & paling berisiko di fase ini (evaluasi AI per-soal, bukan per-attempt — pola baru) — dikerjakan setelah 2 fondasi di atas siap, supaya tidak nyampur beberapa hal belum stabil sekaligus. |
| 4 | P7-004 | Test suite + checkpoint | Pola sama P1-013/P2-017/.../P6-005 — penutup fase. |

**Total 4 sesi.** §5.3 (IELTS/TOEFL/PTE) dan Proctoring (roadmap-Fase-9) sengaja tidak termasuk — lihat "Keputusan scope".
