# ALR — Detail Pembangunan per Phase (Phase 2–10+)

Pelengkap `ALR_Build_Roadmap.md`. Phase 0 dan Phase 1 **sudah** dipecah jadi ticket level (lihat `docs/tickets/phase-0.md` dan `docs/tickets/phase-1.md`) — tidak diulang di sini.

**Revisi v2**: dokumen ini sekarang menyertakan keputusan-keputusan konkret yang sudah dibahas & disepakati di `lms_full.md` — bukan cuma daftar nama subsistem, tapi **bentuk aslinya seperti apa** (format, contoh, angka, struktur) supaya tidak hilang ketika ditulis ulang jadi ticket nanti. Tiap keputusan konkret saya beri sumber baris `lms_full.md` biar gampang ditelusuri balik kalau perlu detail lebih lanjut.

Untuk Phase 2 ke atas, dokumen ini **bukan** ticket final siap-eksekusi (aturan `ai-agent-protocol.md`: jangan generate ticket detail untuk fase yang belum mulai). Tapi bedanya dengan v1: sekarang **spesifikasi konkret sudah ada** — begitu satu fase mulai, tinggal dikonversi jadi ticket format lengkap, bukan didesain ulang dari nol.

Catatan penting soal status keputusan: beberapa angka di `lms_full.md` (misal harga Diamond, pricing AI task) adalah **diskusi awal**, sebagian sudah di-lock ulang di ADR resmi (ADR-0004, ADR-0005) dengan angka sedikit berbeda. Saya tandai eksplisit setiap kali ada perbedaan — **ADR yang sudah Accepted selalu menang**, `lms_full.md` dipakai untuk detail yang belum di-ADR-kan.

---

## PHASE 2 — Content Engine & Curriculum Pipeline

### 2.0 Keputusan arsitektur konten yang sudah dikunci (WAJIB dibaca duluan)

Ini keputusan paling penting di seluruh Phase 2 — salah paham di sini bikin rework besar (`lms_full.md` baris 10340–10346):

> **Markdown sebagai authoring/AI interchange format + Semantic AST/Block sebagai canonical runtime format.**

Artinya **tiga hal berbeda**, jangan dicampur:
1. **ALM (ALR Learning Markdown)** — yang ditulis/dilihat admin & AI, format *authoring*.
2. **Semantic AST** — hasil parse ALM, yang benar-benar disimpan & dipakai runtime (jadi `content_blocks` rows).
3. **Question JSON** — **terpisah total dari ALM**, bukan salah satu block type di dalamnya (lihat 2.4).

Alasan kenapa bukan pure Block JSON (baris 10416–10470): bukan karena "block bikin token AI mahal" (itu mitos — token bisa dihemat lewat context builder terlepas dari format simpan), tapi karena Block JSON nested (`lesson → quiz → question → options → explanation`) makin berat buat AI *generate* dan bikin prompt/output-schema makin kompleks begitu strukturnya dalam.

Diagram alur resminya (baris 10582–10626):
```
AUTHORING
  Google Docs-like Editor (WYSIWYG)
       │
  ALR Learning Markdown (ALM)
       │
     Parser
       │
  Semantic AST / Content Model
       │
   ┌───┼───┐
  WEB MOBILE AI
  Renderer Renderer Context
   └───┼───┘
       │
  LEARNING ENGINE
```
Markdown **bukan runtime utama** — hanya bahasa pertukaran/authoring. Admin sendiri tidak perlu melihat markdown mentahnya (bisa full WYSIWYG), tapi di belakang layar tetap lewat jalur ALM → AST.

### 2.1 ALM (ALR Learning Markdown) — spesifikasi konkret

Markdown standar (`#`, `##`, `>`) diperluas dengan **directive block** pakai `:::`. Contoh persis dari dokumen (baris 10480–10572):

```markdown
# Present Simple

We use the present simple to talk about habits and routines.

For example:

> I study English every day.

:::example
She works at a school.
:::

## Practice

:::question id="q_123" type="multiple_choice"
She ___ to school every day.
- go
- goes
- going
- gone
answer: goes
:::
```

Media juga jadi directive (baris 10532–10572):
```markdown
![A family having dinner](asset://abc123)

:::audio
asset: asset://audio123
title: Listening Practice
:::

:::video
asset: asset://video123
:::

:::flashcard
front: "What is the past tense of go?"
back: "went"
:::
```

**Aturan kritis** (baris 10988–10992): question **tidak** ditulis penuh di dalam ALM. Lesson cukup bilang `embed question q_123` — isi soal sesungguhnya hidup di Question Bank (2.4), diambil by-reference. Ini supaya satu soal bisa dipakai ulang di banyak lesson/exam tanpa duplikasi.

### 2.2 Question Generation — jalur BEDA dari lesson generation

Ini pengecualian yang eksplisit ditegaskan (baris 10869–10905): untuk **lesson generation**, AI boleh keluarkan ALM/Markdown. Tapi untuk **question generation**, AI **wajib** keluarkan Semantic JSON langsung — bukan ALM:
```json
{
  "type": "multiple_choice",
  "stem": "She ___ to school every day.",
  "options": [
    {"id": "a", "text": "go"},
    {"id": "b", "text": "goes"},
    {"id": "c", "text": "going"},
    {"id": "d", "text": "gone"}
  ],
  "correct_answer": "b",
  "explanation": "..."
}
```
Alasan (baris 10901–10934): question adalah *structured data*, bukan tulisan bebas. Jadi ada dua dunia terpisah:
- **Content** → ALM/Rich Text — untuk lesson, explanation, article, theory, examples, instructions.
- **Assessment** → Question Schema — untuk question, options, answer, rubric, scoring, explanation, metadata.

### 2.3 Paste Normalizer (wajib, bukan nice-to-have)

Alur (baris 10702–10774):
```
Paste dari: Word / Google Docs / website / PDF / buku / ChatGPT / Markdown
        ↓
  HTML / Plain Text / Markdown (raw)
        ↓
     Normalizer
        ↓
       ALM
        ↓
   Semantic AST
```
Prinsip: apapun sumbernya, hasil akhirnya harus sama persis (`<h2>Present Simple</h2>` dari HTML dan `## Present Simple` dari Markdown murni harus jadi Heading block yang identik). Ini yang bikin copy-paste **tidak merusak struktur internal ALR**.

### 2.4 Question Bank & Question Type System

**Kenapa dipisah dari lesson** (baris 9356–9424): satu soal ("She ___ to school every day.") bisa dipakai di A1 Grammar → Present Simple, School Exam → Grade 7, TOEFL Preparation → Grammar Practice sekaligus — question-nya cuma satu, lesson/quiz/exam tinggal *mereferensikan*.

**Metadata wajib per question** (baris 9428–9487):
```
id, type, subject, topic, concept, skill, difficulty, CEFR, grade, curriculum, exam, tags
```
Contoh: `type: multiple_choice, subject: English, concept: Present Simple, skill: Grammar, difficulty: Easy, CEFR: A1, exam: General Practice`.

**`question_type` BUKAN enum mati** (baris 9560–9609) — ini keputusan arsitektur eksplisit. Desainnya adalah *registered component type*, bukan hardcode `type = MCQ | TRUE_FALSE | ESSAY`:
```
question_type registry: multiple_choice, true_false, matching, ordering,
                         numeric_input, essay, speaking, audio_response, ...

Frontend:
QuestionRenderer
 ├── MultipleChoiceRenderer
 ├── MatchingRenderer
 ├── NumericRenderer
 ├── EssayRenderer
 ├── SpeakingRenderer
 └── ... (nambah tipe = nambah 1 renderer, bukan migration)
```

**Daftar tipe soal MVP English** (baris 9490–9524, dikelompokkan):
- *Objective*: Multiple Choice, Multiple Response, True/False, Yes/No/Not Given, True/False/Not Given, Matching, Matching Headings, Matching Information, Matching Sentence Endings, Fill in the Blank, Gap Fill, Sentence Completion, Summary Completion.
- *Interactive*: Drag & Drop, Ordering, Categorization, Hotspot, Click the Answer.
- *Language*: Speaking, Writing, Listening, Pronunciation.

**Tipe soal untuk sekolah/TKA/Olimpiade** (baris 9527–9553, ditunda ke Phase 10+ kecuali ada kebutuhan mendesak): Mathematics (Numeric Answer, Equation Input, Fraction, Matrix, Graph, Geometry interaction), Science (Label Diagram, Sequence, Data Interpretation, Graph Interpretation), Olympiad (Multi-step solution, Proof, Structured answer, Free response).

**Kenapa arsitektur ini bisa menampung TKA, Olimpiade, IELTS, dan sekolah sekaligus** (baris 9612–9650): semua pakai **Question Bank + Assessment Engine yang sama**, yang beda cuma **blueprint** dan **scoring rules**.

### 2.5 Exam Blueprint (contoh konkret, baris 9654–9716)

```
IELTS Reading
  Section: Reading | Passage: 3 | Questions: 40
  Question Types: Multiple Choice, Matching, True/False/Not Given,
                  Sentence Completion, Summary Completion

Ujian Akhir Semester
  Grade: 8 | Subject: Mathematics
  Blueprint: 20 MCQ, 5 Multiple Response, 5 Essay

TKA
  Domain, Difficulty, Competency, Question distribution
```
Semua disimpan lewat `assessments.config jsonb` yang sama (sudah sesuai ADR-0001) — beda blueprint, satu engine.

### 2.6 OCR-to-Question Pipeline (subsistem yang belum ada di breakdown v1 — WAJIB ditambah)

Kasus konkret: admin foto halaman soal IELTS dari buku, upload, sistem harus bisa ekstrak jadi draft soal (baris 10778–10864):
```
Image/PDF
   ↓
OCR / Vision
   ↓
Document Structure Detection
   ↓
Question Detection
   ↓
Question Type Classification
   ↓
Content Extraction
   ↓
Draft Question
   ↓
Human Review
   ↓
Question Bank
```
**Aturan keras** (baris 10824–10866): jangan pernah AI → langsung published. Alurnya wajib `SCANNED → EXTRACTED → AI STRUCTURED → DRAFT → REVIEW → APPROVED → PUBLISHED`. Alasan eksplisit: AI bisa salah baca angka, simbol, pilihan jawaban, gambar, tabel, superscript, audio reference, diagram — untuk TKA/Olimpiade kesalahan satu simbol saja fatal.

### 2.7 Content Block SDK — daftar block type konkret

Dari ALM (2.1) + kebutuhan lesson kaya (`lms_full.md` bagian "Format Materi Grammar"): `text/heading/paragraph`, `example` (directive), `audio`, `video`, `image` (via `asset://` reference), `flashcard`, `question_embed` (by-reference only, bukan isi soal), `indonesian_learner_note` (lihat 2.10).

### 2.8 Struktur Konten — Level → Module → Unit → Section

Struktur final yang disepakati (baris 2209–2296):
```
Level → Module → Unit
              ├── Vocabulary
              ├── Grammar
              ├── Pronunciation
              ├── Reading
              ├── Listening
              ├── Speaking
              ├── Writing
              ├── AI Practice
              ├── Quiz
              └── Assessment
```
Contoh konkret: `B1 → Unit 04 → Present Perfect → (Lesson, Examples, Vocabulary, Grammar Practice, Listening Practice, Speaking Practice, Writing Practice, AI Conversation, Review, Unit Test)`.

Di dalam **satu grammar topic**, dipecah jadi section berurutan (baris 2244–2293) — "satu grammar topic bisa jadi satu mini-course":
```
Overview → S1 Introduction → S2 Form & Structure → S3 Affirmative →
S4 Negative → S5 Questions → S6 Usage → S7 Examples → S8 Practice →
S9 Speaking → [Mark as Completed]
```

### 2.9 Format Materi Grammar — pola wajib 11-bagian (baris 2297–2345)

**Setiap** materi grammar, tanpa kecuali, ikuti pola persis ini (Constitution rule untuk Curriculum Generation Agent):
```
01 — What is it?      (penjelasan sederhana)
02 — Form              (contoh: Subject + have/has + V3)
03 — Positive          (contoh: I have finished my homework.)
04 — Negative          (contoh: I haven't finished my homework.)
05 — Question          (contoh: Have you finished your homework?)
06 — When to use it?   (penjelasan penggunaan)
07 — Signal words      (contoh: already, yet, just, ever, never, since, for)
08 — Common mistakes   (contoh: ❌ I have went there. → ✅ I have gone there.)
09 — Practice
10 — Speaking
11 — Writing
```
Ini persis apa yang harus masuk ke Curriculum Constitution (2.13) sebagai aturan generator, bukan aturan longgar.

### 2.10 Indonesian Learner Support Layer

Block khusus yang harus ada di Content Block SDK (2.7): `Indonesian Learner Alert`, `Think in English` vs `Pola Indonesia` comparison, `Common Trap`/`False Friends`, `Indonesian Error Corpus` (data referensi kesalahan umum, dipakai juga oleh AI evaluator writing/speaking di Phase 4), `Indonesian Difficulty Tag` di metadata concept/question (dipakai weakness detection Phase 3).

### 2.11 Level Assessment — bobot skor (baris 2349–2372)

Contoh gate test A2:
```
Vocabulary 20% | Grammar 20% | Reading 15% | Listening 15% |
Writing 10% | Speaking 15% | Pronunciation 5%
```
**Tapi ada rekomendasi eksplisit untuk deviasi** dari bobot rata seperti di atas — karena ALR fokus kuat di speaking, disarankan skema alternatif: `Knowledge 40% / Communication 60%` (bukan speaking cuma 15%). **Ini perlu diputuskan eksplisit sebagai ADR** sebelum Assessment Engine (Phase 5) dibangun — jangan pakai bobot generik tanpa keputusan sadar, karena berdampak langsung ke kelulusan naik level.

### 2.12 English Core vs Exam Preparation — pemisahan arsitektur wajib (baris 2459–2478)

```
                ALR
                 │
    ┌────────────┴────────────┐
ENGLISH CORE              EXAM PREPARATION
Pre-Basic → C2         ┌─────┼─────┐
                      IELTS TOEFL  PTE
                     Academic iBT  Academic
                     General  ITP
```
**Kurikulum 7-level CEFR TIDAK dicampur ke IELTS/TOEFL/PTE** — dijadikan layer terpisah *di atas* English Core. Alasan eksplisit: orang bisa punya kemampuan B2/C1 tapi belum siap hadapi IELTS, dan sebaliknya orang hafal "teknik tes" belum tentu English-nya kuat.

### 2.13 Curriculum Blueprint & Constitution — isi konkret

- **Blueprint** = input generator per modul (topik, grammar target, vocab target, jumlah soal per skill, section wajib sesuai 2.9).
- **Constitution** = aturan konsistensi wajib (2.9 pattern, terminology grammar konsisten, urutan section standar, format soal sesuai 2.4). Ini file config yang direview manusia sekali, dipakai berulang.
- **Master Curriculum / Knowledge Map** (baris 6279): setiap node di knowledge map (bukan cuma "daftar chapter") harus punya: `skill, prerequisite, exercise types, mastery criteria, Indonesian difficulty tag, FRSS/review rules`. Ini "otak" yang dipakai app + AI personalization — desainnya harus selesai sebelum generate silabus besar-besaran (Phase 2 lanjut), bukan sesudahnya.

### 2.14 Asset Management

- Upload langsung client → Cloudflare R2 pakai presigned URL, **jangan** proxy file besar lewat Rust API (baris 10000–10032).
- Access control per asset (public vs org-scoped vs user-scoped) (baris 10032–10056).

### 2.15 Content Versioning

`lessons.version`/`questions.version` sudah ada di skema — **butuh ADR baru** sebelum eksekusi P2: aturan snapshot attempt vs version lesson/question saat sudah `submitted`/`evaluated` (supaya publish versi baru tidak mengubah histori attempt lama). Jangan diputuskan diam-diam di kode.

**Urutan MVP-first Phase 2:** 2.7 (Block SDK minimal) → 2.4 (question type MVP: MCQ+fill-blank dulu) → 2.1+2.3 (ALM + normalizer, WYSIWYG penuh boleh belakangan) → 2.14 (asset upload) → 2.9 (pola grammar 11-bagian, karena ini menentukan bentuk konten pertama yang ditulis) → 2.13+AI pipeline (setelah alur manual terbukti untuk 1 modul, ikuti prinsip "generate 1 modul penuh Module 1 — Alphabet dulu") → 2.6 (OCR pipeline, boleh menyusul setelah Question Bank stabil) → 2.10 (Indonesian layer) → 2.15 (versioning, desainnya disiapkan dari awal tapi eksekusi bisa menyusul).

---

## PHASE 3 — Core Learning Loop

### 3.1 Weakness Detection — drill-down bertingkat (baris 4467–4527)

Bukan cuma skor per skill, tapi drill-down sampai sub-concept:
```
SANI — A1
├── Vocabulary       84%
├── Grammar          71%
│   ├── be           92%
│   ├── have         88%
│   ├── Present Simple 61%  ← weak
│   └── can          90%
├── Listening        76%
├── Speaking         59%
└── Pronunciation    68%

Drill-down Present Simple:
├── Affirmative  85%
├── Negative     64%
├── Questions    49%  ← weak
└── 3rd Person   42%  ← very weak
```
Konsekuensi desain: rekomendasi review **bukan** "ulangi seluruh Present Simple", tapi presisi ke `Present Simple → Questions → Do/Does`. Ini artinya `masteries` harus bisa dihitung di level sub-concept, bukan cuma concept top-level — perlu granularitas concept graph yang cukup dalam sejak Phase 2 (concept hierarchy, bukan flat list).

### 3.2 Knowledge Graph — concept saling terhubung lintas skill (baris 4529–4611)

```
Vocabulary
  └── Food
       ├── rice, bread, vegetable
       └── Grammar
            └── Like/Don't like
                 └── Speaking
                      └── Food conversation
```
Satu vocabulary bukan cuma kartu — "rice" terhubung ke banyak knowledge node. Contoh lengkap 1 kata "vegetable" (baris 4567–4611): satu concept punya field `Meaning, Pronunciation, Spelling, Example, Plural, Countability, Collocations, Grammar, Listening, Speaking, Reading, Writing` — dari 1 kalimat "I eat vegetables every day." learner belajar vegetable, vegetables (plural), eat, every day (collocation), Present Simple sekaligus. Ini prinsip desain: **satu micro lesson bisa mengajarkan banyak concept sekaligus**, bukan 1 concept per lesson.

### 3.3 Forgetfulness Score (baris 4687–4725) — beda dari accuracy biasa

```
Concept: Present Simple
Initial mastery: 82% → After 7 days: 61% → After review: 89%
→ sistem belajar "learner ini cepat lupa" → interval FRSS dipendekkan

Vocabulary: apple
82% → 91% → 96% → 98% → interval bisa diperpanjang
```
Ini bukan cuma modifier ke FRSS interval biasa (ADR-0003) — butuh tracking terpisah *rate of decay per (user, concept)*, bukan cuma `last_result`. Scheduling jadi berbasis **actual learner behavior**, bukan fixed `1 day → 3 days → 7 days → 14 days`.

### 3.4 Retrieval Variation (baris 4727–4765) — review tidak boleh identik

Kalau learner gagal di "vegetable", review berikutnya **tidak boleh** selalu bentuk yang sama:
```
Hari 1: "What is this?" (recall)
Hari 2: Choose the word (recognize)
Hari 3: Listen (listening)
Hari 4: Fill in the blank
Hari 5: Speak
Hari 6: Use it in a sentence
```
Konsekuensi desain: FRSS scheduler (Phase 3) perlu tahu variasi exercise-type yang tersedia per concept, bukan cuma jadwal `due_at` — perlu link ke Question Bank (2.4) untuk pilih tipe soal berbeda tiap kali due.

### 3.5 Lesson Packet — output personal review otomatis (baris 4615–4685)

Contoh konkret ketika AI deteksi Sani lemah di "Food vocabulary + Present Simple questions + speaking fluency":
```
PERSONAL REVIEW — Target: Food + Present Simple Questions
1 MIN — Flashcards (apple, vegetable, chicken, fish)
1 MIN — Grammar (Do you like...? / Does he like...?)
1 MIN — Example (Do you like chicken? / Yes, I do.)
1 MIN — Listening (Listen and choose.)
1 MIN — Speaking (AI: "Do you like vegetables?" → koreksi real-time → retry)
```
Ini bukan "course" — ini personal tutor. Jadi Personal Learning Queue (3.6) bukan cuma daftar item, tapi bisa merangkai jadi paket 5 menit lintas skill otomatis.

### 3.6 Personal Learning Queue (baris 4902–4977)

Format konkret di dashboard:
```
TODAY'S LEARNING
🔴 High Priority   — Present Simple Questions   3 min
🟠 Review          — Food Vocabulary            2 min
🟡 Practice        — Speaking: Daily Routine    5 min
🟢 Optional        — New Vocabulary             5 min
```
Prinsip: dashboard tidak menampilkan "Current Level: A1" statis, tapi kondisi personal — "Your weakest skill: Speaking", "Your current focus: Daily Activities" (baris 4944–4977). Learner tidak bertanya "hari ini belajar apa" — ALR yang menentukan.

### 3.7 Mistake Bank (baris 4802–4836)

```
MY MISTAKES
❌ She go to school.  → ✓ She goes to school.
Topic: Present Simple | Error: Third Person Singular | Frequency: 7 times
Status: Needs Review
```
Notifikasi personal setelah beberapa hari: "You made this mistake 7 times. Let's fix it." — perlu tabel/tracking terpisah dari `learning_events` biasa (agregasi per jenis kesalahan, bukan per attempt).

### 3.8 5 Jenis AI Intervention (dari roadmap #35, desain trigger)

`Learn` (materi baru) | `Practice` (latihan biasa) | `Correct` (koreksi kesalahan) | `Review` (FRSS-triggered) | `Rescue` (khusus struggling berulang — lihat 3.9).

### 3.9 AI vs Human Recommendation Trigger (baris 6126–6154) — jembatan ke Phase 8

```
Attempt 1 → 42%
Attempt 2 → 49%
Attempt 3 → 51%
→ "You're still struggling with this topic."
   🤖 Try another AI explanation — 2💎   atau   👩‍🏫 Learn with a tutor
```
Ini bukan fitur marketplace murni (Phase 8) — triggernya hidup di Learning Engine (Phase 3): kalau AI intervention berulang tidak menaikkan mastery signifikan, sistem menawarkan opsi tutor. Perlu threshold eksplisit (berapa kali attempt gagal → tawarkan tutor) sebagai config, bukan hardcode.

**Urutan MVP-first Phase 3:** 3.1 (weakness detection dasar dengan drill-down 2 level) → 3.6 (queue gabungan sederhana) → 3.2 (knowledge graph minimal, prerequisite untuk 1 level) → 3.5 (lesson packet, bisa versi sederhana dulu) → 3.3+3.4+3.7 (forgetfulness/retrieval variation/mistake bank — butuh cukup data historis untuk berguna, bisa menyusul) → 3.8+3.9 (rescue mode & tutor bridge, terhubung Phase 4/8).

**Checkpoint keluar (dari roadmap):** setelah user mengerjakan 10 soal dari 3 concept berbeda, `/review-queue` mengembalikan urutan yang masuk akal (concept lemah muncul duluan) — dites manual dengan skenario buatan.

---

## PHASE 4 — Exercise Engine & 4 Skills

### 4.1 AI Tutor — 3 mode konkret (baris 2043–2089)

**AI Conversation**: AI mulai percakapan kontekstual ("Hi! Welcome to our restaurant. What would you like to order?"), user jawab via suara, AI skor 5 dimensi (lihat 4.2) sekaligus. **Correction**: user salah ("I want eat fried rice.") → AI kasih versi lebih baik ("Better: 'I'd like to have fried rice.'"). **Try Again**: user mengulang dengan koreksi.

### 4.2 AI Speaking Engine — 5 dimensi scoring wajib terpisah (baris 2091–2138)

Setiap dimensi **field terpisah**, bukan 1 angka gabungan (`evaluations.scores` jsonb):
1. **Grammar** — contoh: "I go to Bali yesterday." → koreksi "I went to Bali yesterday." + reason ("Use Past Simple for completed past events.").
2. **Pronunciation** — per kata, dengan skor % + target IPA. Contoh: `word: comfortable, score: 68%, target: /ˈkʌmf.tə.bəl/`.
3. **Vocabulary** — saran kata lebih natural sesuai konteks (contoh: "very good" → "excellent").
4. **Fluency** — analisis pause, hesitation, repetition, speaking rate.
5. **Naturalness** — koreksi kalimat "textbook-correct tapi tidak natural" (contoh: "I very like this movie." → "I really like this movie.").

### 4.3 Exercise Engine — struktur generik (audit dulu sebelum generate, baris 3469–3570)

Prinsip: 1 engine generik dari Question Bank (2.4), bukan engine per skill terpisah. Render lewat `QuestionRenderer` registry (2.4).

### 4.4 Kids Mode — "Learn by Doing" 10-step (baris 4198–4270, contoh "FOOD")

Bukan "hafalkan 30 vocabulary", tapi sequence wajib:
```
Step 1 — See      (🍎 Apple, 🍌 Banana, 🍚 Rice...)
Step 2 — Hear     (audio "Apple.")
Step 3 — Repeat   (AI dengarkan pronunciation)
Step 4 — Recognize ("Which one is an apple?")
Step 5 — Recall   ("What is this?")
Step 6 — Use      ("I like apples.")
Step 7 — Speak    ("What food do you like?" → jawab bebas)
Step 8 — Grammar  (AI perkenalkan pola "I like + noun")
Step 9 — Practice ("I like ___.")
Step 10 — Review  (beberapa hari kemudian, recall ulang)
```
Ini "exercise sequence template" yang dipasang ke Content Block SDK (2.7) — bukan tipe soal baru, tapi urutan wajib pemakaian tipe-tipe soal yang sudah ada.

### 4.5 Micro Learning — pemecahan sesi (baris 4401–4436)

```
Morning (3 min)   → 🔔 Review 5 vocabulary
Afternoon (4 min) → 🎧 Listen & repeat
Evening (5 min)   → 🗣️ Speaking challenge
Weekend (15 min)  → 📊 Weekly review
```
Personal Learning Queue (3.6) harus bisa dipecah ke slot ini, bukan cuma "1 blok belajar" — dan notifikasi harus personal, bukan generik "Time to study English!" (baris 4439–4463; contoh baik: "Sani, you often forget 'vegetable'. Let's practice it for 2 minutes.").

### 4.6 Writing Evaluation

`Evaluation` entity terpisah dari `Feedback`/annotation (prinsip ADR-0001 #5) — rubric-based scoring (`rubrics.criteria`) + feedback per-posisi teks, sesuai skema yang sudah ada.

**Urutan MVP-first Phase 4:** 4.3 (MCQ/fill-blank/matching dulu, sudah auto-gradable dari Phase 1) → 4.6 (writing, infra lebih sederhana dari speaking) → 4.1+4.2 (speaking + AI Tutor, butuh transcript pipeline) → 4.5 (micro learning slotting) → 4.4 (Kids mode, tunda kalau target awal bukan Kids).

---

## PHASE 5 — Assessment / Exam Engine

### 5.1 Exam Runtime & Blueprint — sudah dirinci di 2.5 (Exam Blueprint), dipakai sebagai basis.

### 5.2 Level Assessment (unit-internal) — lihat 2.11, termasuk keputusan bobot Knowledge/Communication yang perlu ADR.

### 5.3 IELTS/TOEFL/PTE — Exam Preparation Layer (setelah English Core stabil, lihat 2.12)

**Pre-Exam Diagnostic + Exam Bridge**: sebelum masuk mock test penuh, ada IELTS Foundation dengan sub-modul: Orientation, Listening Foundation, Reading Foundation, Writing Foundation, Speaking Foundation.

**IELTS Academic vs General**: **tidak dibuat 2 course terpisah dari awal** — Listening/Speaking sama, Reading/Writing berbeda, di-branch dalam 1 struktur data yang sama (bukan duplikasi konten).

**IELTS Reading — 14 tipe soal eksplisit** (masing-masing perlu question schema sendiri di 2.4): Multiple Choice, True/False/Not Given, Yes/No/Not Given, Matching Information, Matching Headings, Matching Features, Matching Sentence Endings, Sentence Completion, Summary Completion, Note Completion, Table Completion, Flow-chart Completion, Diagram Label Completion, Short Answer Questions.

**IELTS Listening**: perlu "Word limit engine" — validasi jawaban sesuai batas kata yang diizinkan.

**IELTS Writing**: question generator sendiri untuk Task 1 Academic (beda dari Task 1 General) + Task 2.

**IELTS Speaking**: Part 1/2/3, masing-masing pola pertanyaan beda.

**TOEFL**: iBT dan **ITP benar-benar terpisah** (struktur & scoring beda total) — jangan disatukan di skema.

**PTE**: banyak tipe soal integrated-skill (Summarize Group Discussion, Respond to a Situation, dll) — cocok dengan Question Type registry yang extensible (2.4).

**Exam-specific weakness detection** — contoh konkret (baris 4840–4899):
```
IELTS Reading: Matching Headings 86% | T/F/NG 48% ← weak | Matching Info 72% | Summary Completion 81%
→ notifikasi: "Kamu masih sering tertukar antara False dan Not Given. Yuk latihan 5 soal."

PTE: Read Aloud 82% | Repeat Sentence 67% | Describe Image 88% |
     Retell Lecture 51% ← weak | Write from Dictation 59% ← weak
→ micro lesson 7 menit khusus 2 sub-skill terlemah
```
Ini bukan sistem terpisah dari weakness detection biasa (3.1) — persis engine yang sama, cuma diaplikasikan ke concept granularitas exam-skill.

**Urutan MVP-first Phase 5:** 5.1+5.2 dulu (exam internal, sudah dipakai sejak Phase 1). 5.3 (IELTS/TOEFL/PTE) **ditunda eksplisit** sampai English Core CEFR stabil.

---

## PHASE 6 — Gamification & Economy

### 6.1 Pemisahan 3 metrik — TIDAK BOLEH dicampur (baris 7821–7868)

```
🪙 Learning Credits — untuk ekonomi (AI evaluation, AI tutor, skip, generation)
⭐ XP               — untuk gamification (lesson selesai, streak, improvement)
🧠 Mastery          — kemampuan sebenarnya (formula ADR-0002)
```
Contoh: `Sani: XP 12,430 | Learning Coin 87 | English Mastery 72%`. **XP tinggi tidak berarti English-nya bagus** — prinsip ini harus terlihat di UI (jangan tampilkan XP sebagai proxy kemampuan) dan di formula (XP tidak pernah masuk kalkulasi mastery).

### 6.2 XP earning table (baris 7876–7899, contoh — final angka lewat tuning)

```
Daily review +10 | Vocabulary practice +5 | Grammar exercise +10 |
Listening +10 | Speaking +15 | Writing +20 | Complete lesson +20 |
Weekly assessment +30 | Mastery improvement +25 | 7-day streak +50
```
Bonus lebih besar untuk **improvement & consistency**, bukan volume — contoh: speaking naik 52%→68% dapat bonus khusus "+50 XP — Great Improvement!" (bukan cuma dari jumlah soal dikerjakan).

### 6.3 Leaderboard — banyak konteks, wajib ada Personal Leaderboard (baris 7903–7952)

`Global, Country, Region, Friends, Class, Course, Weekly, Monthly` + **Personal Leaderboard** (bukan "ranking 20.000" tapi "You improved more than 87% of learners this week" — jauh lebih sehat untuk retention daripada 1 leaderboard global yang bikin user baru merasa "ngapain saya coba?").

### 6.4 League (baris 7955–7985)

`Bronze → Silver → Gold → Platinum → Diamond → Master`, **berdasarkan learning consistency + mastery + activity**, bukan cuma XP — supaya user tidak bisa "beli" jalan ke ranking tinggi.

### 6.5 Streak — non-punitive by design (baris 7989–8007)

Streak Freeze (proteksi dari langganan) — "You missed yesterday. Your streak is safe." — jangan sampai anak merasa gagal cuma karena lupa buka app 1 hari.

### 6.6 Kids Gamification — presentation layer saja (baris 8011–8046)

Contoh: "English Island" dengan sub-island (Food Island, Home Island, Space Island, Animal Island) — tapi underlying learning tetap `vocabulary → grammar → listening → speaking` yang sama. Game **hanya presentation layer**, tidak boleh menggantikan struktur pembelajaran asli.

### 6.7 Achievement — 3 kategori (baris 8049–8078)

`Learning Achievement` (First Lesson, 100 Vocabulary Words, 7/30 Day Streak, A1/B1 Completed), `Skill Achievement` (Speaking Star, Listening Master, Reading Explorer, Writing Builder), `Improvement Achievement` (Biggest Improvement, Weakness Destroyer, Comeback Learner — menghargai progress, bukan cuma kemampuan awal).

### 6.8 Personal Mission (baris 8083–8107) — dianggap lebih penting dari leaderboard

```
Today's Mission: ✓5 vocab reviews ✓1 grammar exercise ✓1 listening ✓1 speaking
Reward: +80 XP, +2 Credits
```

### 6.9 Model Bisnis 3-layer (baris 5265–5295)

```
              ALR
    ┌──────────┼──────────┐
SELF LEARNING  AI SERVICES  TUTOR MARKETPLACE
Free/Premium   Diamond      Private Tutor
   Ads      AI Eval/Teacher  70% Tutor / 30% ALR
```

### 6.10 Free tier — bukan "unlimited tapi diselipi iklan di mana-mana" (baris 5297–5350)

Prinsip eksplisit: **free = benar-benar usable** untuk core learning, premium = lebih cepat/nyaman/powerful, bukan gerbang. Tabel fitur:
```
Materi/Vocabulary/Grammar/Basic exercises/Basic review/Progress → ✅ Free
AI evaluation / AI Speaking / AI Writing evaluation → 🎬 Watch Ad / 💎 Diamond
Skip assessment / Skip level / AI Live Teacher → 💎 Diamond only
```

### 6.11 Diamond ≠ token AI mentah — framing produk (baris 5434–5459)

Diamond harus terasa sebagai **"Premium Learning Energy"**, bukan "membayar token AI". UI copy yang benar: "💎 5 Diamonds — Get your IELTS Writing evaluated by AI", bukan "Cost: 5 AI credits."

### 6.12 Pricing draft awal (baris 5399–5430) — ⚠️ SUDAH DISUPERSEDE sebagian oleh ADR-0005

```
AI Grammar Evaluation 1 | AI Writing Evaluation 5 | IELTS Writing Eval 8 |
IELTS Speaking Eval 8 | PTE Speaking Eval 6 | Pronunciation Analysis 2 |
AI Answer Generation 2 | AI Tutor 5min 5 | AI Tutor 15min 12 | AI Tutor 30min 25 |
Skip Unit Assessment 5 | Skip Level Assessment 15
```
**Catatan penting**: tabel ini draft awal dari `lms_full.md`. ADR-0005 (Accepted) sudah punya tabel resmi yang sedikit beda (contoh: `LiveTutor = 10 credit/menit` di ADR-0005, vs draft `AI Tutor 5min = 5 credit` ≈ 1/menit di sini). **Pakai angka ADR-0005 sebagai sumber kebenaran**; draft ini hanya referensi kenapa angka itu dipilih/berubah.

### 6.13 Subscription — Diamond allowance, bukan unlimited AI (baris 5354–5491)

```
Monthly +100 Diamond | 3 Months +350 | 6 Months +750 | Yearly +1,600
```
(angka contoh, final di ADR-0005). Prinsip kunci: **Subscription ≠ Unlimited AI** — kalau unlimited, 1 user power-user (100 speaking eval + 100 writing eval + 20 live session + 500 pronunciation analysis) bisa bikin biaya AI melebihi harga subscription. Jadi **Subscription = Premium Access + Diamond Allocation**.

### 6.14 4 Jenis Resource — kerangka mental produk (baris 6072–6122)

```
Free Resource:         Time, Practice, Basic Learning, Ads
Subscription Resource: Premium Content, No Ads, Diamond Allocation, Advanced Analytics
Diamond Resource:      AI Evaluation, AI Generation, Skip, AI Tutor, Special Assessments
Human Resource:        Tutor, Private Class, Course
```

### 6.15 Funnel bisnis (baris 6158–6226)

```
NEW USER → FREE LEARNING → (Ads | Engaged → Need More AI →
(Watch Ads | Buy Diamond) → Heavy User → Subscribe → Advanced Learning →
Human Support? → Tutor Marketplace → Long-term Customer)
```
Ini rasional produk kenapa 4 revenue stream (ads, diamond, subscription, marketplace) harus saling terhubung, bukan berdiri sendiri.

### 6.16 Cron Job Expiry Credit

Konsekuensi ADR-0005: job berkala untuk expire `transactions` allowance subscription — perlu ticket eksplisit.

**Urutan MVP-first Phase 6:** 6.5 (streak) + 6.7 (achievement dasar) → 6.10+6.11 (framing free/diamond, karena berdampak langsung ke funnel monetisasi) → 6.3+6.4 (leaderboard/league, butuh user aktif cukup banyak) → 6.6+6.8 (Kids/personal mission, bisa paralel dengan Phase 4/5).

---

## PHASE 7 — Mobile (React Native)

### 7.1 Monorepo package breakdown — versi lebih rinci dari yang di-lock P0-009 (baris 8945–9018)

Diskusi awal mengusulkan struktur lebih granular daripada `packages/shared` tunggal:
```
apps/ → web (Next.js), mobile (React Native), admin (Next.js terpisah)
packages/ → ui, types, schemas, api-client, auth, learning, assessment, analytics, utils
services/ → api (Rust + Axum)
```
**Catatan**: P0-009 sudah dikunci lebih sederhana (`apps/web`, `apps/mobile`, `apps/api`, `packages/shared`). Struktur granular di atas **bukan keputusan final** — dicatat sebagai opsi refactor kalau `packages/shared` mulai terasa jadi satu package raksasa yang sulit di-maintain. Jangan pecah packages di awal sebelum benar-benar terasa perlu (over-engineering), tapi simpan sebagai referensi arah kalau saatnya tiba.

**Yang wajib shared** (baris 8995–9006): TypeScript types, Zod schemas, API client, authentication state, analytics events, content schemas, learning models, constants, validation, business contracts.

**Yang boleh platform-specific** (baris 9008–9017): Web → sidebar, table, rich editor, admin dashboard. Mobile → bottom navigation, mobile reader, gestures, push notification.

### 7.2 Content Renderer — bukti arsitektur platform-agnostic (baris 9020–9048)

```
Content JSON (dari Semantic AST, 2.0)
   ┌───────┴───────┐
Web Renderer    Mobile Renderer
Next.js         React Native
```
Content **tidak pernah** disimpan sebagai HTML sebagai sumber utama — kalau di titik Phase 7 ternyata renderer mobile butuh transformasi aneh dari data yang sama, itu tanda ada logic yang menyelinap ke Next.js dan perlu ditarik balik ke `packages/shared`.

### 7.3 Offline mode, audio recording, push notification personal

Sudah dibahas di v1 — ditambah detail: push notification **harus personal** (lihat 4.5), bukan broadcast generik ke semua user jam yang sama.

**Catatan:** mulai serius setelah web MVP + `packages/shared` stabil, sesuai roadmap.

---

## PHASE 8 — Organization / LMS / Marketplace

### 8.1 ALR Learning Marketplace — 8 kategori produk (baris 8119–8143)

```
Marketplace → Private Tutoring, Group Course, Live Class, Self-paced Course,
              Hybrid Course, Bootcamp, Exam Preparation, Kids Course
```

### 8.2 Tutor sebagai Course Creator — dashboard lengkap (baris 8145–8181)

```
My Teaching → Profile, Services, Courses, Classes, Students, Schedule,
              Attendance, Assignments, Assessments, Messages, Certificates, Earnings
```

### 8.3 4 Tipe Learning Product (baris 8183–8230)

```
1. Private — 1 tutor : 1 student (contoh: "IELTS Speaking Private — 60 menit")
2. Group   — 1 tutor : 5–20 student (contoh: "IELTS Preparation — Batch 12")
3. Course  — self-paced (contoh: "English Grammar Mastery A1")
4. Hybrid  — self-paced material + group class + private session digabung
```

### 8.4 Class Management (baris 8233–8276)

```
Course → Cohort/Batch → Class → Students
```
Contoh: "IELTS Academic Preparation" → Batch 01 (20 students), Batch 02 (15 students). Tiap batch punya: schedule, instructor, students, attendance, materials, assignments, exams, discussions, grades, certificates.

### 8.5 Attendance — 4 metode (baris 8278–8314)

```
QR Attendance   — tutor tampilkan QR, student scan
Geolocation     — verifikasi berada di lokasi kelas
Online          — otomatis dari join/leave time
Manual          — tutor override
```

### 8.6 Assignment (baris 8317–8349)

```
Assignment → Title, Description, Deadline, Attachments, Questions, Rubric, AI Evaluation
Flow: Student submit → AI evaluate → Tutor review/override
```

### 8.7 Gradebook (baris 8351–8374)

```
Sani → Attendance 95% | Assignment 88% | Quiz 82% | Speaking 76% | Final Exam 84% | Overall 84%
```
Nilai akademik (gradebook) dan mastery engine **disimpan terpisah** — cocok karena keduanya mengukur hal beda (kelulusan course vs kemampuan aktual).

### 8.8 Certificate Generator + verifikasi (baris 8377–8457)

```
Certificate → Student, Course, Instructor, Completion Date, Score,
              Certificate ID, Verification URL (QR code → verify.alr.../valid)
```
Terhubung ke mastery, bukan cuma "completed" (contoh: `Course: English Speaking B1 | Completion: 100% | Assessment: 84% | Estimated CEFR: B1 | Skills: Speaking/Listening/Vocabulary/Pronunciation`). **Wording harus hati-hati** — jangan menyamakan sertifikat kursus internal dengan sertifikasi resmi eksternal (legal/reputational risk).

### 8.9 Tutor Reputation Score — bukan cuma bintang (baris 5729–5761)

```
Rating 4.9 | Students 128 | Lessons 642 | Completion 98% |
Response time <1 hour | Cancellation 1% | Specialization tags (IELTS/Kids/Speaking)
```
Dipakai untuk "Recommended Tutor" berdasarkan kebutuhan learner spesifik.

### 8.10 Student Diagnosis untuk Tutor (baris 5811–5847) — value-add signifikan

Sebelum sesi pertama, tutor sudah lihat:
```
Student Profile: Current Level B1
Weakness: Speaking fluency, Past tense, Vocabulary recall
IELTS: Speaking 5.5 estimated
Recommended focus: 1. Fluency 2. Past experiences 3. Part 2 answers
```
Tutor tidak mulai dari "Hello, what is your name?" — langsung mengajar sesuai kebutuhan. **Perlu aturan privasi/consent eksplisit** siapa yang boleh lihat data ini (terhubung ke Phase 3 Personal Learning System) — bukan default semua tutor lihat semua data student.

### 8.11 Learning Package (baris 8511–8879, contoh)

```
Single Session Rp100.000 | 4 Sessions Rp360.000 | IELTS Speaking Package (8 sessions) |
IELTS Intensive (20 sessions) | Kids English (12 sessions)
```
Desain sebagai produk yang bisa dikonfigurasi tutor sendiri, bukan hardcode daftar paket.

### 8.12 Payment Abstraction (baris 5913–5945)

```
Payment → Order, Payment, Payment Status, Refund, Transaction,
          Revenue, Platform Fee, Tutor Earnings, Payout
```
QRIS jadi salah satu provider di dalam abstraksi ini, database ALR tidak bergantung implementasi provider tertentu.

### 8.13 Wallet Ledger — bukan `balance +=` langsung (baris 5980–6007)

```
Lesson Rp100.000 → Platform -Rp30.000 | Tutor +Rp70.000
Status: Pending → Completed → Available → Paid
```
Jangan langsung `tutor_balance += 70.000` — butuh accounting trail lengkap (sudah selaras dengan ADR-0005 `transactions.type = payout_earned/payout_withdrawn`).

### 8.14 Cancellation Policy — beda student vs tutor (baris 5703–5726)

```
Student cancellation: >24 jam full refund | 6–24 jam 50% | <6 jam no refund (contoh, bukan final)
Tutor cancellation: user full refund; repeated cancellation → tutor kena penalty
```

### 8.15 Organization/School Tier

RBAC penuh sudah didesain (ADR-0006) — implementasi UI/flow admin sekolah + private leaderboard per class/org (beda dari leaderboard publik Phase 6). 3 jenis user dibedakan eksplisit: `Learner`, `Tutor/Teacher`, `Organization` — permission & UI flow tidak boleh bercampur.

**Urutan MVP-first Phase 8:** 8.3+8.4 (Private + Group session dulu) → 8.12+8.13 (payment + wallet ledger, tanpa ini marketplace tidak jalan) → 8.14 (cancellation policy, wajib bareng payment) → 8.5+8.6+8.7 (attendance/assignment/gradebook) → 8.8 (certificate) → 8.9+8.10+8.11 (peningkatan value tutor) → 8.1 (Course/Bootcamp/Hybrid penuh) → 8.15 (organization tier, target market beda, bisa rilis terpisah).

---

## PHASE 9 — Proctoring

(tidak ada detail baru signifikan dari `lms_full.md` di luar yang sudah ada di ADR-0001 — breakdown v1 tetap berlaku: Policy → Event Collector → Risk Engine → Human Review → Privacy/Compliance, gerbang manusia wajib, jangan auto-decision.)

---

## PHASE 10+ — Scale ke Domain Lain

### 10.1 Domain Adapter Pattern — analoginya eksplisit "sistem kendaraan" (baris 7443–7525)

Arsitektur sama, "mesin" (adapter) beda per domain — kalau English/Math/Cambridge butuh migration skema besar untuk ditambahkan, berarti ada asumsi English-specific yang menyelinap di fase-fase sebelumnya (indikator kegagalan desain generic di Phase 0–2).

### 10.2 Empat Progression Type — kerangka Learner Profile lintas domain (baris 6010–6068)

```
LEVEL → CEFR (Pre-Basic → C2)
      → EXAM (IELTS, TOEFL, PTE)
      → SKILL (Vocabulary, Grammar, Listening, Reading, Speaking, Writing, Pronunciation)
      → MASTERY (Knowledge → Practice → Retention → Fluency)
```
Semua masuk 1 Learner Profile — kerangka ini yang harus tetap valid ketika domain baru (Math, Science, bahasa lain) masuk; kalau ternyata "EXAM" atau "SKILL" harus didefinisikan ulang total per domain, itu bukan scaling murni tapi rework.

### 10.3 Prinsip kunci — jangan kunci curriculum jadi daftar chapter statis (baris 6230–6279)

"ALR jangan dibangun sebagai course app" — curriculum adalah **knowledge map**, learner tidak harus jalan linear di dalamnya, AI yang menentukan bagian mana yang perlu dipelajari sekarang. Prinsip ini yang membuat scaling ke domain baru = isi node baru di knowledge map, bukan rombak alur aplikasi.

---

## Cara pakai dokumen ini

1. Jangan tulis ticket detail untuk Phase N+1 sebelum Phase N checkpoint keluar terpenuhi (aturan `ai-agent-protocol.md`).
2. Saat mulai Phase baru, ambil bagian relevan dari dokumen ini (sudah termasuk contoh/format konkret, tidak perlu buka ulang `lms_full.md` dari nol) + baris rujukan kalau butuh konteks percakapan aslinya, tulis ulang jadi `docs/tickets/phase-N.md` format lengkap.
3. Titik yang butuh **ADR baru sebelum implementasi** (ditandai eksplisit di teks): skema versioning attempt-vs-lesson-version (2.15), bobot Level Assessment Knowledge/Communication vs per-skill (2.11), formula reputation tutor (8.9), threshold rescue-mode/tutor-bridge (3.9).
4. Kalau ada angka/keputusan di `lms_full.md` yang beda dari ADR resmi (contoh paling jelas: pricing Diamond di 6.12) — **ADR Accepted selalu menang**. `lms_full.md` dipakai sebagai konteks "kenapa", bukan sumber kebenaran angka final.
5. Update `docs/STATE.md` seperti biasa tiap ticket selesai — dokumen ini tidak menggantikan STATE.md, hanya membantu menulis ticket-nya.
