# Phase 10 (ticket-numbering) — IELTS/TOEFL/PTE: Exam Preparation Layer

## Keputusan scope (baca duluan)

User eksplisit minta 4 roadmap-Fase dikerjakan berurutan (2026-09-02):
**roadmap-Fase 5.3 (ini) → roadmap-Fase 6.9-16 → roadmap-Fase 8 sisa →
roadmap-Fase 9**. Ini yang pertama.

Sumbernya sendiri (`ALR_Phase_Detail_Breakdown.md` §5.3) secara eksplisit
menunda seluruh scope ini ("5.3 ditunda eksplisit sampai English Core
CEFR stabil") TANPA memberi urutan MVP-first untuk isinya — beda dari
tiap §-lain yang selalu punya kalimat "Urutan MVP-first Phase N: ...".
Jadi ticket-phase ini yang pertama kali harus memutuskan sendiri
pemotongan MVP untuk §5.3, mengikuti disiplin yang sama dipakai tiap
fase sebelumnya di proyek ini.

**§5.3 penuh, kalau dibaca literal, mencakup**: Pre-Exam Diagnostic +
IELTS Foundation (5 sub-modul), IELTS Academic vs General branching,
14 tipe soal Reading eksplisit (masing-masing butuh schema sendiri),
Listening word-limit engine, Writing Task 1/2 generator terpisah,
Speaking Part 1/2/3, TOEFL iBT DAN ITP (struktur+scoring beda total,
sumbernya sendiri bilang "jangan disatukan"), PTE dengan banyak tipe
soal integrated-skill. Ini besarnya setara beberapa fase sebelumnya
digabung — tidak realistis 1 ticket-phase.

**Riset kunci sebelum motong scope** (baca kode langsung, bukan asumsi):
- `questions.type` di schema **genuinely extensible** — `text` biasa,
  TANPA CHECK constraint (beda dari `status`/`difficulty` yang punya
  CHECK) — konfirmasi §2.4's klaim "registered component type, bukan
  hardcode enum" itu nyata di level DB, bukan cuma niat desain.
- Tapi yang BENAR-BENAR terdaftar & jalan cuma 3 tipe:
  `question_schema.ts`'s `validators` dan `grading.ts`'s
  `isAutoGradable`/`isCorrect` cuma punya `mcq`/`fill_blank`/`matching`.
  Dari 14 tipe IELTS Reading eksplisit di sumber, **cuma 0 yang sudah
  ada** (`matching` generik ADA tapi bukan `matching_headings`/
  `matching_information`/dst yang punya semantik beda: heading dipilih
  dari daftar dengan distractor, bukan pasangan 1:1 polos).
- **P4-001's `GET /concepts/{id}/mastery-breakdown` subject-agnostic
  sepenuhnya** — jalan generik atas `concepts`/`masteries`, tidak peduli
  domain. Ini artinya "exam-specific weakness detection" yang diminta
  §5.3 (baris 506-515: "bukan sistem terpisah dari weakness detection
  biasa — persis engine yang sama, cuma diaplikasikan ke concept
  granularitas exam-skill") **TIDAK BUTUH KODE BARU SAMA SEKALI** — cukup
  seed data: subject/curriculum/concept IELTS + question baru yang
  ditag ke concept itu, mastery breakdown otomatis kerja begitu ada
  attempt data. §2.5's klaim serupa ("beda blueprint, satu engine")
  juga terbukti murni via `assessments.config jsonb` yang sudah ada
  sejak ADR-0001 — tidak perlu tabel baru buat "IELTS Reading Practice
  Test" sebagai assessment.
- §2.12 (pemisahan wajib English Core vs Exam Prep) juga tidak butuh
  skema baru — `subjects` sudah generik, "IELTS" jadi subject terpisah
  dari "English" (yang dipakai CEFR core), keduanya numpang tabel yang
  sama.

**Keputusan pemotongan MVP (scope ticket-phase ini)**: **IELTS SAJA**
(bukan TOEFL/PTE — masing-masing produk ujian terpisah dengan scope
sendiri sebesar ini, dicatat sebagai kandidat lanjutan terpisah, bukan
digabung diam-diam), dan dari IELTS SENDIRI cuma:
- **3 tipe soal baru** yang paling eksplisit disebut sumber (True/False/
  Not Given, Matching Headings, Short Answer — yang terakhir sekalian
  jadi kendaraan buat "Listening word-limit engine" karena keduanya
  butuh mekanisme yang sama: validasi jumlah kata jawaban).
- **Bukti reuse arsitektur** (bukan tabel/endpoint baru): seed 1 subject
  IELTS + 1 concept tree + question bank kecil + 1 assessment blueprint
  "IELTS Reading Practice Test", lalu buktikan weakness detection JALAN
  lewat `GET /concepts/{id}/mastery-breakdown` yang sudah ada (P4-001),
  BUKAN endpoint baru.

**Dieksplisit DIDEFER, bukan didiamkan** (kandidat lanjutan terpisah):
- TOEFL (iBT+ITP terpisah) dan PTE — produk ujian sendiri-sendiri,
  scope sebesar IELTS ini per produk.
- 11 dari 14 tipe soal IELTS Reading lainnya (Multiple Choice sudah
  ke-cover oleh `mcq` yang ada; Yes/No/Not Given bentuknya identik
  `true_false_not_given` cuma label beda — trivial follow-up; Matching
  Information/Features/Sentence Endings bentuknya sama pola
  "assignment dari daftar" seperti `matching_headings` — trivial
  follow-up; Sentence/Summary/Note/Table/Flow-chart/Diagram Label
  Completion semua varian "isi bagian kosong dalam struktur" —
  follow-up, bukan pola rekayasa baru).
- IELTS Writing Task 1/2 generator, IELTS Speaking Part 1/2/3 — butuh
  kerja sebesar Phase 6 (AI generation + evaluation audio/teks) per
  skill, di luar scope ticket-phase ini.
- Pre-Exam Diagnostic + IELTS Foundation (Orientation/Listening
  Foundation/Reading Foundation/Writing Foundation/Speaking
  Foundation) — ini kerja *authoring konten* (nulis modul lesson),
  bukan ticket engineering; menyusul setelah tipe soal+concept tree
  IELTS ini ada.
- Frontend `QuestionRenderer` buat 3 tipe soal baru — ticket-phase ini
  backend-only (pola sama Phase 7/8/9), FE renderer dicatat sebagai gap
  terbuka, bukan diklaim selesai.

Tidak ada ADR baru yang dibutuhkan — §2.12's pemisahan sudah didesain
sejak ADR-0001 (`subjects` generik), P2-004/ADR yang sama sudah
mengunci `question_type` sebagai registry.

## Ticket

### P10-001 — 3 tipe soal baru: True/False/Not Given, Matching Headings, Short Answer (word-limit engine)
**Status:** done
**Depends on:** P2-004 (`question_schema.ts` registry), P3-001 (`grading.ts`)
**Endpoint baru:** tidak ada — ini nambah entry ke registry yang sudah dipakai `POST /questions/{id}/check` dan submit attempt yang ada.
**Deskripsi:** Bukti nyata klaim "registered type, add 1 entry, bukan migration" (§2.4) — 3 tipe soal paling eksplisit disebut sumber. `short_answer` sekalian implementasi "Listening word-limit engine" (§5.3 baris 496): jawaban yang melebihi jumlah kata yang diizinkan otomatis salah, terlepas dari isi teksnya.
**Acceptance Criteria:**
- [x] `question_schema.ts`: validator `true_false_not_given` (`data: {statement}`, `correct_answer: {value: "true"|"false"|"not_given"}`)
- [x] `question_schema.ts`: validator `matching_headings` (`data: {passages: [{id, text}], headings: string[]}` — `headings.length` boleh lebih banyak dari `passages.length`, distractor asli seperti IELTS; `correct_answer: {assignments: Record<passage_id, heading_index>}`)
- [x] `question_schema.ts`: validator `short_answer` (`data: {prompt, max_words}`, `correct_answer: {text}`)
- [x] `grading.ts`: `isAutoGradable` + `isCorrect` buat ketiga tipe. `short_answer` WAJIB reject kalau `submitted.text` jumlah kata > `max_words`, sebelum cek kecocokan teks — ini yang jadi "word limit engine"-nya, bukan validasi kosmetik di FE
- [x] `matching_headings` scoring: benar HANYA kalau SEMUA `passage_id` di `data.passages` match persis assignment yang disubmit (biner, sama seperti `matching` yang sudah ada — bukan partial credit)
**DoD:** test backend baru — tiap tipe: schema validasi tolak data/correct_answer yang salah bentuk; grading benar untuk correct/incorrect; `short_answer` PENTING dites eksplisit dengan jawaban yang textually benar TAPI melebihi `max_words` → tetap salah; dites lewat KEDUA jalur (`/check` inline DAN submit attempt formal) — pelajaran dari gap `matching` P3-001 yang cuma ke-cover 1 jalur dulu.

**Catatan implementasi:** `grading.isCorrect` butuh parameter ke-4 baru
`data?: unknown` — `short_answer`'s `max_words` hidup di kolom `data`
milik SOAL (bukan `correct_answer`), yang sebelumnya tidak pernah perlu
diteruskan ke fungsi ini sama sekali. Parameter opsional (bukan
mengubah 5 call site lama) — cuma 2 call site (`question_service.check`,
`assessment_service.submitAttempt`) yang diupdate meneruskan
`question.data`/`q.data`. **1 bug nyata ketemu pas nulis test**: fungsi
`normalize()` yang dipakai bersama `fill_blank`/`short_answer` cuma
`.trim().toLowerCase()` — TIDAK collapse whitespace INTERNAL (cuma
surrounding) — test awal pakai `"Carbon  Dioxide "` (double-space
tengah) gagal karena mismatch murni whitespace, bukan bug logic.
Diperbaiki di level test (bukan ubah `normalize()` yang dipakai
`fill_blank` juga — di luar scope ticket ini, `fill_blank` selama ini
tidak pernah exercise kasus double-space). Kedua jalur (`/check` di
`tests/question-check.test.ts` + submit attempt formal di
`tests/assessment.test.ts`, seeding sendiri — TIDAK reuse
`seedAssessment` yang di-hardcode ke `mcq`) dites eksplisit buat
ketiga tipe, termasuk `short_answer` yang textually superset (3 kata)
tapi `max_words: 2` tetap salah di KEDUA jalur. 13 test baru (412/412
total, dari 399), `bunx tsc --noEmit` bersih.

### P10-002 — Seed IELTS Reading: subject terpisah + concept tree + practice test, bukti reuse engine
**Status:** done
**Depends on:** P10-001 (3 tipe soal), P4-001 (`GET /concepts/{id}/mastery-breakdown`), P7-001 (Exam Session Runtime)
**Endpoint baru:** tidak ada — ticket ini murni data (migration seed script atau service function 1-kali-panggil), membuktikan §2.12/§2.5's klaim reuse tanpa kode baru.
**Deskripsi:** IELTS sebagai layer terpisah dari English Core CEFR (§2.12) — `subjects` row baru "IELTS" (bukan menambah ke subject "English" yang dipakai CEFR core). 1 concept tree kecil + question bank + 1 assessment blueprint, cukup buat membuktikan weakness detection exam-specific (§5.3 baris 506-515) jalan lewat engine yang SAMA PERSIS dengan §3.1, bukan sistem baru.
**Acceptance Criteria:**
- [x] Subject baru "IELTS" (`subjects` row terpisah dari "English")
- [x] Concept tree: 1 parent concept "IELTS Reading" + 3 child concept (1 per tipe soal baru P10-001: "True/False/Not Given", "Matching Headings", "Short Answer Questions") via `parent_concept_id` (pola sama containment tree ADR-0007/P2-001)
- [x] Question bank "IELTS Reading" + minimal 2 soal per tipe baru (6 soal total), masing-masing ditag ke concept-nya lewat `question_concepts`
- [x] 1 `assessments` row "IELTS Reading Practice Test 1" (`config` blueprint mereferensikan ke-6 soal itu) — reuse `assessments.config jsonb` yang sudah ada sejak ADR-0001, TIDAK ada kolom/tabel baru
**DoD:** test backend baru — siswa kerjakan practice test itu lewat Exam Session Runtime yang sudah ada (P7-001, timer+auto-submit), jawab benar sebagian salah sebagian per tipe soal, submit; `GET /concepts/{ielts-reading-concept-id}/mastery-breakdown` (endpoint P4-001 yang TIDAK disentuh sama sekali) balikin breakdown per sub-skill yang benar, sub-skill yang dijawab salah muncul `weak: true` — membuktikan reuse, bukan endpoint baru yang menduplikasi logic.

**Catatan implementasi:**
1. **`assessments.type = 'ielts'` — dead capability lain ketemu**: CHECK constraint `assessments_type_check` sudah punya nilai `'ielts'`/`'toefl'`/`'pte'` sejak ADR-0001, TAPI nol kode pernah pakai — ticket ini yang pertama kali beneran insert `type: "ielts"`. Pola sama persis `exam_sessions` (sebelum P7-001)/`concept_prerequisites` (sebelum P4-003)/`assessments.type payout_earned` (sebelum P9-007) — ditemukan lagi, bukan kebetulan pertama kali.
2. **Seed script persisten** (`scripts/seed-ielts-reading.ts`, pola sama `scripts/migrate.ts`) — idempotent (skip total kalau subject "ielts" sudah ada, bukan partial re-run, karena `question_banks`/`questions` tidak punya unique key buat conflict-guard per baris). Dijalankan against dev DB, dikonfirmasi idempotent lewat 2x run.
3. **AC "minimal 2 soal per tipe" cukup buat seed persisten (demo), TAPI TIDAK cukup buat test yang menuntut sinyal `weak` yang bisa dipercaya** — ketemu pas nulis test: `config.masteryNMin` (default 5) berarti confidence cuma `n/5`, dan `weak` di P4-001 SENGAJA `false` kalau `confidence < masteryConfidenceThreshold` (0.6) — 2 event cuma confidence 0.4, di bawah threshold. Test (`tests/ielts-reading.test.ts`) pakai fixture terpisah dengan 3 soal per sub-skill (confidence tepat 0.6), BUKAN reuse seed script — 2 artefak beda tujuan (demo vs bukti-lewat-assert), didokumentasikan eksplisit di sini biar tidak dikira inkonsistensi.
4. Test membuktikan full stack asli: `POST /assessments/{id}/exam-sessions` (P7-001) → `POST /attempts/{id}/submit` (jalur formal, bukan `/check`) → `GET /concepts/{id}/mastery-breakdown` (P4-001, 0 baris diubah) — 3 soal `short_answer` sengaja salah, 1 di antaranya lewat word-limit engine P10-001 (bukan cuma teks salah), 3 soal `true_false_not_given` sengaja benar semua — breakdown balikin `weak: true`/`score: 0` utk Short Answer, `weak: false`/`score: 100` utk TFNG, keduanya `confidence >= 0.6`. 1 test baru (413/413 total, dari 412), `bunx tsc --noEmit` bersih, route-coverage TETAP 98 route/0 gap (tidak bertambah — bukti langsung nol endpoint baru).

### P10-003 — Integration test suite + exit checkpoint
**Status:** done
**Depends on:** P10-001, P10-002
**Deskripsi:** Pola sama tiap ticket-phase sebelumnya — route-coverage audit (kemungkinan 0 route baru karena P10-001/002 murni registry+data, bukan endpoint — itu sendiri bagian dari pembuktian "reuse", dicek eksplisit bukan diasumsikan), checkpoint end-to-end yang menyatukan tipe soal baru → seed IELTS → exam session → weakness detection dalam 1 alur nyata.
**Acceptance Criteria:**
- [x] Route-coverage audit (`grep`-based, pola P2-017/.../P9-008)
- [x] Checkpoint baru: 1 siswa kerjakan "IELTS Reading Practice Test 1" penuh (P10-002) lewat Exam Session Runtime asli, sengaja salah di 1 sub-skill (termasuk kasus `short_answer` melebihi word limit — untuk membuktikan word-limit engine ikut kena di checkpoint, bukan cuma unit test terisolasi), assert skor benar DAN `GET /concepts/{id}/mastery-breakdown` menandai sub-skill yang salah sebagai weak
**DoD:** `bun test` hijau penuh di `titian-backend-bun` (lokal — CI masih P0-010 yang tertunda).

**Catatan implementasi:** checkpoint scenario-nya SUDAH persis `tests/ielts-reading.test.ts` yang ditulis di P10-002 (bukan diduplikasi jadi file terpisah) — test itu SENDIRI sudah memenuhi seluruh AC checkpoint ini kata per kata (Exam Session Runtime asli, submit formal, breakdown weak yang benar, TERMASUK kasus word-limit). Tidak ada test baru ditulis khusus P10-003 — dicatat eksplisit di sini supaya jelas ini keputusan sadar (checkpoint = re-verifikasi apa yang sudah ada, bukan kewajiban selalu menulis file baru), bukan langkah yang terlewat. Route-coverage audit dijalankan ulang: 98 route/0 gap, sama seperti setelah P10-002 (mengonfirmasi P10-001-003 kolektif menambah 0 endpoint). `bun test` penuh: 413/413.

---

## Checkpoint keluar Phase 10 (harus bisa didemo, bukan asumsi)
1. [x] 3 tipe soal baru (`true_false_not_given`, `matching_headings`, `short_answer`) tervalidasi DAN ternilai benar lewat kedua jalur (`/check` + submit attempt formal), bukan cuma salah satu. — `tests/question-check.test.ts` (jalur `/check`) + `tests/assessment.test.ts` (jalur submit formal, seed sendiri bukan reuse fixture `mcq`) + `tests/ielts-reading.test.ts` (jalur submit formal lewat Exam Session Runtime asli).
2. [x] Word-limit engine terbukti menolak jawaban yang textually benar tapi kepanjangan — dites eksplisit, bukan diasumsikan dari deskripsi fitur. — `grading.test.ts`: `correct_answer` yang textually identik tapi `max_words` lebih ketat dari jumlah katanya sendiri tetap salah, di 2 jalur HTTP + di checkpoint `ielts-reading.test.ts`.
3. [x] IELTS terbukti sebagai layer terpisah dari English Core CEFR (subject beda), bukan dicampur ke subject "English" yang ada. — subject baru `code: "ielts"` (persisten di `scripts/seed-ielts-reading.ts`), tidak pernah insert ke subject "English" manapun.
4. [x] Weakness detection exam-specific terbukti JALAN lewat `GET /concepts/{id}/mastery-breakdown` yang SUDAH ADA (P4-001) — nol endpoint baru buat fitur ini, dibuktikan lewat route-coverage audit yang tidak bertambah untuk kebutuhan ini. — 98 route sebelum dan sesudah P10-001/002/003.
5. [x] Semua yang dideferred (TOEFL/PTE, 11 tipe soal Reading sisanya, Writing/Speaking generator, Pre-Exam Diagnostic, FE renderer) tercatat eksplisit di sini dan `docs/STATE.md`, bukan hilang begitu saja dari radar. — lihat "Keputusan scope" di atas + `docs/STATE.md`'s entri Phase 10.

Phase 10 **SELESAI PENUH**. Lanjut ke item berikutnya yang diminta user: roadmap-Fase 6.9-16 (Gamification: model bisnis).
