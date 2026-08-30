# ALR Detailed Development Blueprint v2
### Field-level, ticket-level, session-proof.

Dokumen ini melengkapi `ALR Development Roadmap` (fase besar) dengan level detail yang cukup supaya progres **tidak hilang** walau dikerjakan lintas puluhan sesi AI agent oleh solo developer.

> **Update (2026-08-30):** backend di-migrasi total dari Rust+Axum+sqlx ke
> Bun+ElysiaJS+Drizzle ORM (keputusan eksplisit user, lihat
> `docs/adr/0009-runtime-migration-bun-elysia.md`). Acceptance-criteria di
> bawah yang menyebut perintah spesifik Rust (`sqlx migrate run`,
> `cargo test`, dst) dibiarkan apa adanya sebagai catatan sejarah rencana
> asli — padanan Bun-nya (`bunx drizzle-kit migrate`, `bun test`) ada di
> `titian-backend-bun/`, bukan hasil edit ulang baris-baris di bawah ini.

---

# BAGIAN 1 — KENAPA PROJECT SEPERTI INI BIASANYA "HILANG DI TENGAH JALAN"

Tiga penyebab paling umum, dan solusinya:

| Penyebab | Kenapa terjadi | Solusi |
|---|---|---|
| **AI agent tidak punya memori antar sesi** | Tiap sesi baru = context kosong, agent bisa "menemukan ulang" arsitektur dengan cara berbeda dari sesi sebelumnya | 4 *living document* wajib dibaca di awal tiap sesi (lihat Bagian 2) |
| **Keputusan arsitektur tidak tercatat alasannya** | 2 bulan kemudian lupa kenapa milih pendekatan X, agent baru bisa "membetulkan" jadi Y tanpa sadar itu regresi | ADR (Architecture Decision Record) bernomor, immutable, isi alasan bukan cuma keputusan |
| **Task terlalu besar ("bangun backend")** | Tidak ada checkpoint, sulit tahu 30% atau 80% selesai, gampang scope creep | Semua kerjaan dipecah jadi **ticket** dengan ID, acceptance criteria, dan Definition of Done eksplisit |

**Prinsip inti:** kode adalah output yang bisa dibuang & dibangun ulang. **Dokumen keputusan (ADR + ticket log) tidak boleh hilang** — itu yang jadi "ingatan" proyek.

---

# BAGIAN 2 — SISTEM ANTI-HILANG (WAJIB DIBUAT DULUAN, SEBELUM KODE APAPUN)

## 2.1 Struktur folder dokumentasi

```
alr/
├── docs/
│   ├── STATE.md                  ← paling penting, dibaca tiap sesi
│   ├── adr/
│   │   ├── 0001-data-model.md
│   │   ├── 0002-mastery-formula.md
│   │   ├── 0003-frss-algorithm.md
│   │   └── ...
│   ├── tickets/
│   │   ├── phase-0.md
│   │   ├── phase-1.md
│   │   └── ...
│   ├── domain-model.md           ← ERD final (Bagian 3)
│   ├── api-contract.md           ← OpenAPI-style (Bagian 4)
│   └── ai-agent-protocol.md      ← Bagian 6
```

## 2.2 `docs/STATE.md` — file yang WAJIB dibaca AI agent di awal SETIAP sesi

Template isinya:

```markdown
# ALR — Current State
Last updated: 2026-08-22 by [nama/agent]

## Fase aktif
Phase 1 — Backend Core

## Ticket sedang dikerjakan
P1-004: Question Bank API (in-progress, 60%)

## Ticket selesai (5 terakhir)
- P1-003: Content API [done]
- P1-002: User & Profile API [done]
- P1-001: Auth Google OAuth + JWT [done]
- P0-010: Repository structure [done]
- P0-009: Database migration awal [done]

## Blocker aktif
- Belum ada, atau: "AI Gateway provider key belum di-provision di staging"

## Deviasi dari rencana (kalau ada)
- Contoh: "ERD di ADR-0001 field `difficulty` di questions diubah dari enum jadi float 0-1, lihat ADR-0007"

## JANGAN lakukan ini tanpa ADR baru
- Jangan ubah struktur `learning_events` (dipakai FRSS + mastery + recommendation, breaking change mahal)
- Jangan tambah provider AI baru tanpa lewat AI Gateway abstraction
```

**Aturan:** setiap AI agent WAJIB mengupdate file ini di akhir sesi sebelum berhenti — bukan opsional. Ini satu baris instruksi paling penting di seluruh dokumen ini.

## 2.3 Format ADR (Architecture Decision Record)

```markdown
# ADR-0001: Canonical Data Model
Status: Accepted
Date: 2026-08-22

## Context
Kita butuh data model yang generic (bisa dipakai English, Math, dst) tapi tidak over-engineered untuk MVP.

## Decision
[keputusan final]

## Alternatives considered
[opsi lain yang dipikirkan dan kenapa ditolak]

## Consequences
[apa yang jadi lebih mudah, apa yang jadi trade-off]

## Supersedes / Superseded by
-
```

ADR tidak boleh diedit setelah `Accepted` — kalau berubah, buat ADR baru yang menyatakan "supersedes ADR-000X".

## 2.4 Format Ticket

```markdown
### P0-005: Question & Assessment Schema
**Fase:** Phase 0
**Depends on:** P0-001 (Domain Model)
**Status:** todo | in-progress | blocked | done

**Deskripsi:**
Desain schema PostgreSQL untuk question_banks, questions, assessments, assessment_questions.

**Acceptance Criteria:**
- [ ] Support minimal 5 tipe soal: MCQ, fill-blank, matching, drag-drop, essay
- [ ] Question bisa dipakai ulang di banyak assessment (many-to-many)
- [ ] Question punya field difficulty & concept_ids untuk mastery engine
- [ ] Migration file jalan tanpa error di local Postgres

**Definition of Done:**
- [ ] Migration ditulis & diuji
- [ ] ERD diagram diupdate di domain-model.md
- [ ] ADR ditulis kalau ada keputusan baru
- [ ] STATE.md diupdate

**Prompt untuk AI Agent:**
"Baca docs/STATE.md, docs/adr/0001-data-model.md, dan docs/domain-model.md.
Buat migration PostgreSQL untuk question_banks, questions, assessments,
assessment_questions sesuai skema di Bagian 3.6 dokumen blueprint.
Setelah selesai, update docs/domain-model.md dan docs/STATE.md."
```

Semua ticket di bawah di dokumen ini sudah mengikuti format ringkas versi tabel — kalau dieksekusi, tulis ulang jadi format lengkap di atas per ticket di `docs/tickets/phase-X.md`.

---

# BAGIAN 3 — DOMAIN MODEL DETAIL (field-level)

Ini contoh isi ADR-0001. Tipe kolom pakai notasi PostgreSQL, `jsonb` dipakai untuk struktur fleksibel (biar tidak keseringan migration saat nambah field kecil).

## 3.1 Identity & Organization

```
organizations
  id              uuid pk
  name            text
  slug            text unique
  type            enum(platform, school, tutor_org)
  settings        jsonb
  created_at      timestamptz

users
  id              uuid pk
  email           text unique
  google_id       text unique
  name            text
  avatar_url      text
  locale          text default 'id'
  created_at      timestamptz

user_organization_roles
  id              uuid pk
  user_id         uuid fk -> users
  organization_id uuid fk -> organizations
  role            enum(platform_admin, org_owner, academic_director,
                       curriculum_developer, reviewer, teacher, tutor,
                       student, parent)
  created_at      timestamptz
  unique(user_id, organization_id, role)
```

**Kenapa role bukan kolom di `users`:** satu user bisa jadi student di satu org dan tutor di org lain (sudah jadi requirement eksplisit di dokumen awal kalian).

## 3.2 Curriculum Tree

```
subjects
  id       uuid pk
  code     text unique   -- 'english', 'math'
  name     text

curricula
  id           uuid pk
  subject_id   uuid fk -> subjects
  code         text        -- 'alr-english-general'
  name         text
  framework    enum(cefr, cambridge, kurikulum_id, custom)
  version      int default 1
  status       enum(draft, published, archived)

levels
  id             uuid pk
  curriculum_id  uuid fk -> curricula
  code           text     -- 'pre_basic','a1'...'c2'
  name           text
  order_index    int

units
  id          uuid pk
  level_id    uuid fk -> levels
  code        text
  title       text
  order_index int

lessons
  id          uuid pk
  unit_id     uuid fk -> units
  title       text
  type        enum(learn, practice, speaking, writing, review, assessment)
  order_index int
  status      enum(draft, in_review, published, archived)
  version     int default 1

content_blocks
  id          uuid pk
  lesson_id   uuid fk -> lessons
  type        text        -- 'text','image','audio','video','question_embed','flashcard',...
  order_index int
  data        jsonb        -- rendered content (ALM/AST hasil parsing)
  raw_source  text         -- ALR Learning Markdown asli, untuk re-parse kalau schema block berubah
```

## 3.3 Concept & Knowledge Graph

```
concepts
  id          uuid pk
  subject_id  uuid fk -> subjects
  code        text        -- 'present_simple', 'vocab_food_basic'
  name        text
  type        enum(grammar, vocabulary, skill, pronunciation)

lesson_concepts
  lesson_id   uuid fk -> lessons
  concept_id  uuid fk -> concepts
  weight      float default 1.0   -- seberapa dominan concept ini di lesson
  primary key(lesson_id, concept_id)

concept_prerequisites
  concept_id              uuid fk -> concepts
  prerequisite_concept_id uuid fk -> concepts
  primary key(concept_id, prerequisite_concept_id)
```

## 3.4 Question Bank

```
question_banks
  id          uuid pk
  subject_id  uuid fk -> subjects
  name        text

questions
  id            uuid pk
  bank_id       uuid fk -> question_banks
  type          text       -- 'mcq','fill_blank','matching','drag_drop','essay','speaking_prompt',...
  difficulty    float       -- 0.0 - 1.0, bukan enum, biar bisa dipakai algoritma
  data          jsonb       -- soal, opsi jawaban, media reference
  correct_answer jsonb
  explanation   jsonb
  status        enum(draft, in_review, published, archived)
  version       int default 1

question_concepts
  question_id  uuid fk -> questions
  concept_id   uuid fk -> concepts
  primary key(question_id, concept_id)
```

**Kenapa `data` jsonb bukan kolom per tipe soal:** 15+ tipe soal per skill (lihat daftar exercise di dokumen awal) — kalau tiap tipe punya tabel sendiri, migration akan meledak. Trade-off: validasi struktur `data` dilakukan di application layer via schema (Zod/serde) per `type`, bukan di level DB constraint.

## 3.5 Assessment & Attempt

```
assessments
  id          uuid pk
  type        enum(unit_test, level_assessment, mock_exam, ielts, toefl, pte)
  title       text
  config      jsonb    -- durasi, passing score, randomize, dst

assessment_questions
  assessment_id uuid fk -> assessments
  question_id   uuid fk -> questions
  order_index   int
  points        float
  primary key(assessment_id, question_id)

attempts
  id            uuid pk
  user_id       uuid fk -> users
  assessment_id uuid fk -> assessments  (nullable kalau attempt di lesson biasa)
  lesson_id     uuid fk -> lessons      (nullable)
  started_at    timestamptz
  submitted_at  timestamptz
  answers       jsonb   -- {question_id: answer}
  score         float
  status        enum(in_progress, submitted, evaluated)
```

## 3.6 Evaluation & Feedback (dipisah sesuai keputusan di dokumen awal)

```
evaluations
  id             uuid pk
  attempt_id     uuid fk -> attempts
  evaluator_type enum(ai, human)
  rubric_id      uuid fk -> rubrics (nullable)
  scores         jsonb   -- per-criteria score
  evidence       jsonb   -- untuk AI: raw model output / confidence
  created_at     timestamptz

feedback
  id             uuid pk
  evaluation_id  uuid fk -> evaluations
  type           enum(annotation, comment, voice_note)
  content        text
  position       jsonb   -- offset di writing canvas, timestamp di audio, dst
  created_by     uuid fk -> users (nullable kalau dari AI)
```

## 3.7 Learning Engine (Mastery, FRSS, Events)

```
learning_events
  id          uuid pk
  user_id     uuid fk -> users
  event_type  text     -- 'question_answered','lesson_completed','review_done',...
  entity_type text     -- 'question','lesson','assessment'
  entity_id   uuid
  payload     jsonb    -- correct/incorrect, time_spent, hint_used, dst
  created_at  timestamptz
  -- index wajib di (user_id, created_at) dan (entity_type, entity_id)

masteries
  id              uuid pk
  user_id         uuid fk -> users
  concept_id      uuid fk -> concepts
  score           float    -- 0-100, formula lihat ADR-0002
  confidence      float
  last_reviewed_at timestamptz
  updated_at      timestamptz
  unique(user_id, concept_id)

frss_schedule
  id             uuid pk
  user_id        uuid fk -> users
  concept_id     uuid fk -> concepts
  interval_days  float
  ease_factor    float default 2.5
  due_at         timestamptz
  last_result    enum(recalled, forgot, partial)
  unique(user_id, concept_id)
```

## 3.8 Economy

```
credits
  user_id      uuid pk fk -> users
  balance      bigint
  updated_at   timestamptz

transactions
  id           uuid pk
  user_id      uuid fk -> users
  type         enum(earn, spend, purchase, refund)
  amount       bigint
  reference    text    -- 'ai_task:{id}', 'subscription:{id}'
  created_at   timestamptz

ai_tasks
  id           uuid pk
  user_id      uuid fk -> users
  task_type    text    -- lihat enum AITask di roadmap
  provider     text
  model        text
  prompt_id    text
  tokens_used  int
  cost         numeric
  status       enum(queued, running, done, failed)
  created_at   timestamptz
```

## 3.9 Exam Runtime & Proctoring (dua engine terpisah, dihubungkan lewat FK)

```
exam_sessions
  id            uuid pk
  assessment_id uuid fk -> assessments
  user_id       uuid fk -> users
  status        enum(not_started, in_progress, submitted, timed_out)
  started_at    timestamptz
  submitted_at  timestamptz

proctoring_policies
  id                 uuid pk
  exam_type          text
  camera             enum(off, optional, on)
  microphone         enum(off, optional, on)
  screen             enum(off, optional, on)
  fullscreen_required boolean
  focus_monitoring   boolean

proctoring_sessions
  id              uuid pk
  exam_session_id uuid fk -> exam_sessions
  policy_id       uuid fk -> proctoring_policies
  device_info     jsonb

proctoring_events
  id                    uuid pk
  proctoring_session_id uuid fk -> proctoring_sessions
  type                  text     -- 'face_missing','multiple_faces','fullscreen_exit',...
  severity              enum(low, medium, high)
  timestamp             timestamptz
  metadata              jsonb
  evidence_id           uuid fk -> assets (nullable)
```

**Ticket untuk menuliskan ADR-0001 resmi + migration file dari semua tabel di atas: lihat P0-005 s/d P0-009 di Bagian 5.**

---

# BAGIAN 4 — API CONTRACT DETAIL (contoh, pola diulang untuk resource lain)

Format tiap endpoint: method, path, auth, request, response, error case. Ini contoh untuk 3 resource inti — pola yang sama dipakai AI agent untuk generate sisanya secara konsisten.

### `POST /api/v1/auth/google/callback`
```
Auth: none (ini endpoint yang menghasilkan auth)
Request:
  { "id_token": "string (dari Google OAuth)" }
Response 200:
  { "access_token": "jwt", "refresh_token": "jwt",
    "user": { "id": "uuid", "email": "string", "name": "string" } }
Error:
  401 { "error": "invalid_token" }
```

### `GET /api/v1/curricula/{curriculum_id}/tree`
```
Auth: Bearer JWT
Response 200:
  {
    "curriculum": { "id": "uuid", "code": "alr-english-general", "name": "..." },
    "levels": [
      {
        "id": "uuid", "code": "pre_basic", "name": "Pre-Basic",
        "units": [
          { "id": "uuid", "code": "unit-1", "title": "English Alphabet",
            "lessons": [
              { "id": "uuid", "title": "Learn", "type": "learn", "status": "published" }
            ]
          }
        ]
      }
    ]
  }
Error:
  404 { "error": "curriculum_not_found" }
```

### `POST /api/v1/attempts/{attempt_id}/submit`
```
Auth: Bearer JWT (harus attempt milik user ybs)
Request:
  { "answers": { "question_id_1": {...}, "question_id_2": {...} } }
Response 200:
  { "attempt_id": "uuid", "status": "submitted",
    "score": 85.0,
    "learning_events_created": 12 }
Error:
  409 { "error": "attempt_already_submitted" }
  422 { "error": "missing_required_answers", "missing": ["question_id_3"] }
```

**Aturan konsistensi wajib untuk semua endpoint (masukkan ke `docs/api-contract.md` sebagai header):**
- Semua error pakai bentuk `{ "error": "snake_case_code", "detail": "..." (optional) }`
- Semua list response wajib ada pagination: `{ "items": [...], "next_cursor": "..." }`
- Semua timestamp ISO 8601 UTC
- Semua endpoint yang mengubah data (`POST/PUT/PATCH/DELETE`) wajib idempotent-safe atau punya `Idempotency-Key` header untuk operasi finansial (transactions, credits)

---

# BAGIAN 5 — TICKET BREAKDOWN DETAIL: PHASE 0 & PHASE 1

## Phase 0 — Foundation (target 2–3 minggu)

| ID | Ticket | Depends on | DoD singkat |
|---|---|---|---|
| P0-001 | Tulis ADR-0001: Canonical Data Model (pakai Bagian 3 di atas sbg draft) | - | ADR status Accepted, direview manual |
| P0-002 | Tulis ADR-0002: Mastery formula awal (sederhana dulu, config-driven) | P0-001 | Formula tertulis + contoh perhitungan manual |
| P0-003 | Tulis ADR-0003: FRSS algorithm (SM-2 modifikasi) | P0-001 | Formula interval tertulis + tabel contoh 5 siklus review |
| P0-004 | Tulis ADR-0004: AI Gateway design (task→cost→model→prompt→validate→track) | - | Diagram + daftar AITask enum final |
| P0-005 | Tulis ADR-0005: Credit economy (unit, pricing, mapping ke AI cost) | P0-004 | Tabel konversi credit↔AI task |
| P0-006 | Tulis ADR-0006: RBAC (role list final + permission matrix) | P0-001 | Matrix role x action lengkap |
| P0-007 | Migration SQL untuk semua tabel Bagian 3.1–3.9 | P0-001 | `sqlx migrate run` sukses di local Postgres |
| P0-008 | Tulis `docs/api-contract.md` untuk 15 endpoint inti (auth, curriculum tree, lesson, question, attempt, mastery, credit) | P0-007 | Semua endpoint punya request/response/error seperti Bagian 4 |
| P0-009 | Scaffold monorepo (`apps/web`, `apps/mobile`, `apps/api`, `packages/shared`) | - | `pnpm install && pnpm build` sukses tanpa error di semua workspace |
| P0-010 | Setup CI (lint+test+build on PR) | P0-009 | PR dummy trigger pipeline hijau |
| P0-011 | Buat `docs/STATE.md`, `docs/ai-agent-protocol.md` awal | - | File ada dan diisi sesuai template Bagian 2 |

**Checkpoint keluar Phase 0:** semua ADR di atas Accepted, migration jalan, monorepo build sukses, CI hijau. Kalau salah satu belum, **jangan mulai Phase 1** — ini yang paling sering dilanggar dan jadi sumber "hilang arah".

## Phase 1 — Backend Core (target 4–6 minggu)

| ID | Ticket | Depends on | Endpoint terkait |
|---|---|---|---|
| P1-001 | Auth: Google OAuth + JWT issuing/refresh | P0-007, P0-008 | `/auth/google/callback`, `/auth/refresh` |
| P1-002 | User & Profile CRUD + `user_organization_roles` | P1-001 | `/users/me`, `/organizations/{id}/members` |
| P1-003 | Content API: curricula/levels/units/lessons read (admin write nanti di Phase 2) | P1-002 | `/curricula/{id}/tree`, `/lessons/{id}` |
| P1-004 | Question Bank API (CRUD internal, publish flow draft→review→published) | P1-002 | `/questions`, `/question-banks/{id}/questions` |
| P1-005 | Assessment API: create session, deliver question set | P1-003, P1-004 | `/assessments/{id}`, `/attempts` |
| P1-006 | Attempt submission + scoring dasar (auto-gradable types dulu: MCQ, fill-blank) | P1-005 | `/attempts/{id}/submit` |
| P1-007 | Learning Event writer (setiap attempt/submit memicu event) | P1-006 | internal, dipicu dari P1-006 |
| P1-008 | Mastery calculator v1 (implementasi formula ADR-0002) | P1-007 | `/mastery/{concept_id}` |
| P1-009 | FRSS scheduler v1 (implementasi ADR-0003) | P1-008 | `/review-queue` |
| P1-010 | Asset upload ke Cloudflare R2 + signed URL | P0-009 | `/assets/upload`, `/assets/{id}` |
| P1-011 | AI Gateway v1: abstraction + DeepSeek adapter + `ai_tasks` logging | P0-004 (ADR), P1-002 | `/ai/evaluate` (stub dulu, 1 task type) |
| P1-012 | Health check, structured logging (tracing), error handling standar (Bagian 4 aturan error) | P0-009 | `/health` |
| P1-013 | Integration test suite untuk semua endpoint di atas | semua di atas | `cargo test` hijau, coverage minimal untuk critical path (attempts, mastery) |

**Checkpoint keluar Phase 1 (definisi "backend core selesai" — bukan asumsi, harus bisa didemo):**
1. User bisa login via Google → dapat JWT.
2. User bisa lihat 1 curriculum tree (walau isinya masih data dummy/seed).
3. User bisa mengerjakan 1 assessment berisi 3 soal MCQ, submit, dapat score otomatis.
4. Submit tadi menghasilkan `learning_events`, yang memicu update `masteries` dan `frss_schedule` untuk concept terkait — **ini yang paling penting untuk dicek**, karena ini jalur yang menghubungkan semua engine (kalau ini gak konek, Phase 3 nanti stuck).
5. `ai_tasks` table terisi minimal 1 baris dari 1 pemanggilan AI Gateway percobaan.

Kalau checkpoint #4 belum jalan end-to-end, **jangan lanjut ke Phase 2/3** walau kelihatan "API-nya udah banyak" — itu justru tanda paling umum proyek kelihatan maju padahal core loop-nya belum pernah benar-benar dites nyambung.

---

# BAGIAN 6 — TEMPLATE TICKET UNTUK PHASE 2–9 (pakai pola yang sama)

Untuk fase-fase berikutnya, jangan generate semua ticket sekaligus di awal — itu sendiri jadi sumber "hilang", karena rencana detail untuk Phase 5 dibuat sebelum Phase 3 selesai dan realitanya pasti berubah. Polanya:

1. **Sebelum mulai fase baru**, buat `docs/tickets/phase-N.md` dengan level break down sama seperti Bagian 5 (tabel ID → ticket → depends on → target endpoint/deliverable), berdasarkan checkpoint keluar dari fase sebelumnya + bagian relevan dari `lms_full.md`.
2. Tiap ticket ikuti format lengkap di Bagian 2.4 (deskripsi, acceptance criteria, DoD, prompt agent).
3. Tiap fase punya **checkpoint keluar** eksplisit seperti contoh Phase 1 di atas — bukan daftar fitur, tapi **skenario end-to-end yang bisa didemo**.
4. `STATE.md` diupdate tiap ticket selesai, bukan tiap fase selesai.

Contoh checkpoint keluar untuk fase-fase lain (supaya kalian tahu target konkretnya, bukan cuma daftar fitur):

- **Phase 2 (Content & LMS):** admin bisa menulis 1 lesson penuh via WYSIWYG, publish, dan lesson itu langsung bisa diakses lewat `/lessons/{id}` yang dipakai Phase 1.
- **Phase 3 (Learning Engine):** setelah user mengerjakan 10 soal dari 3 concept berbeda, `/review-queue` mengembalikan urutan review yang masuk akal (concept lemah muncul duluan) — dites manual dengan skenario buatan, bukan cuma "kodenya ada".
- **Phase 4 (AI Engine):** 1 writing submission dari user menghasilkan evaluation dengan rubric scores + minimal 3 annotation feedback, tersimpan di tabel `evaluations`/`feedback`.
- **Phase 5 (Web App):** learner bisa: login → lihat dashboard → buka lesson → kerjakan soal → lihat mastery naik → dapat rekomendasi review — semua di 1 sesi browser, tanpa refresh manual data.

---

# BAGIAN 7 — PROTOKOL SESI AI AGENT (paste ini di awal SETIAP sesi baru)

```
Sebelum mengerjakan apapun:
1. Baca docs/STATE.md — pahami fase aktif, ticket aktif, blocker, dan larangan.
2. Baca semua file di docs/adr/ yang statusnya Accepted — jangan mengambil
   keputusan yang bertentangan dengan ADR tanpa membuat ADR baru yang
   eksplisit menyatakan supersedes.
3. Baca ticket aktif di docs/tickets/phase-N.md — kerjakan HANYA acceptance
   criteria ticket itu, jangan melebar ke ticket lain dalam sesi yang sama
   kecuali diminta eksplisit.
4. Kalau menemukan kebutuhan mengubah struktur yang sudah di-ADR
   (misal ubah kolom di tabel yang sudah dipakai fase lain) — STOP,
   laporkan ke user, jangan langsung eksekusi.
5. Di akhir sesi, WAJIB:
   - Update status ticket (todo/in-progress/blocked/done)
   - Update docs/STATE.md (ticket terakhir, next step, blocker baru kalau ada)
   - Kalau ada keputusan baru → tulis ADR baru
```

---

Kalau kalian mau, langkah paling produktif berikutnya: saya bantu tuliskan **ADR-0001 sampai ADR-0006 secara penuh** (bukan draft di Bagian 3, tapi versi final siap-Accept) berdasarkan ERD di atas, supaya Phase 0 bisa langsung ditutup minggu ini.
