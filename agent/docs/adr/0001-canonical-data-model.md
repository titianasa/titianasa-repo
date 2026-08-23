# ADR-0001: Canonical Data Model
Status: Accepted
Date: 2026-08-22
Supersedes: -
Superseded by: -

## Context
ALR harus jadi adaptive learning platform yang **content-agnostic** (English dulu, tapi arsitektur harus tahan dipakai Math/Bahasa Indonesia/dll tanpa migrasi ulang) dan **multi-curriculum** (CEFR, Cambridge, Kurikulum Indonesia). Kita juga butuh satu user bisa punya role berbeda di organization berbeda (student di satu tempat, tutor di tempat lain).

## Decision
Struktur entity final (lihat `docs/domain-model.md` untuk field lengkap):

```
Organization ──< UserOrganizationRole >── User
                                             │
Subject ──< Curriculum ──< Level ──< Unit ──< Lesson ──< ContentBlock
   │                                            │
   └──< Concept >── ConceptPrerequisite         └──< LessonConcept >── Concept
   │
   └──< QuestionBank ──< Question >── QuestionConcept >── Concept

Assessment ──< AssessmentQuestion >── Question
Attempt ── (assessment_id | lesson_id) ── User
Attempt ──< Evaluation ──< Feedback

User ──< LearningEvent
User ──< Mastery >── Concept
User ──< FrssSchedule >── Concept

User ──< Credit
User ──< Transaction
User ──< AiTask

Assessment ──< ExamSession ── User
ExamSession ──< ProctoringSession ── ProctoringPolicy
ProctoringSession ──< ProctoringEvent
```

Prinsip desain:
1. **Role tidak melekat di `users`** — disimpan di `user_organization_roles` (user_id, org_id, role) supaya satu user bisa multi-role lintas organisasi.
2. **Content tree generic**: `Subject → Curriculum → Level → Unit → Lesson → ContentBlock`. Tidak ada tabel khusus "English lesson" — perbedaan domain ada di `subject_id` dan isi `content_blocks.data` (jsonb), bukan di struktur tabel.
3. **Question terpisah dari Content**: question hidup di `question_banks`/`questions`, dipakai ulang lintas lesson & assessment lewat tabel relasi, bukan disalin.
4. **Concept sebagai jembatan** antara content, question, dan learning engine — baik lesson maupun question terhubung ke `concepts`, sehingga mastery/FRSS bisa dihitung di level concept, bukan di level lesson/question saja.
5. **Evaluation ≠ Feedback**: evaluation adalah skor terstruktur (AI atau human), feedback adalah anotasi/komentar individual yang menempel ke satu evaluation. Ini supaya UI bisa render banyak anotasi tanpa mem-parse blob teks.
6. **Exam Runtime terpisah dari Proctoring Engine**, dihubungkan lewat `exam_session_id`. Proctoring event tidak pernah langsung memutuskan `attempts.status` — hanya lewat manusia (lihat ADR terkait proctoring di fase lanjut).
7. Semua kolom fleksibel (soal, config assessment, payload event) pakai `jsonb`, divalidasi di application layer per `type`, bukan di level DB constraint — supaya nambah 1 tipe soal baru tidak butuh migration.

## Alternatives considered
- **Tabel terpisah per subject (English_Lesson, Math_Lesson, dst)** — ditolak, tidak scalable ke Phase 4-6 (bahasa lain, mata pelajaran lain) dan melanggar prinsip "arsitektur besar, MVP kecil".
- **Role sebagai kolom enum di `users`** — ditolak, tidak mendukung multi-role lintas organisasi.
- **Tabel terpisah per tipe soal (McqQuestion, MatchingQuestion, dst)** — ditolak, dengan 15+ tipe soal per skill akan meledak jadi puluhan tabel; dipilih `jsonb` + validasi aplikasi.

## Consequences
- (+) Menambah subject/curriculum/tipe soal baru tidak butuh perubahan skema besar.
- (+) Satu learning engine (mastery/FRSS) otomatis jalan untuk semua domain karena semuanya menempel ke `concepts`.
- (−) Validasi struktur `data` jsonb sepenuhnya tanggung jawab application layer — butuh disiplin schema versioning per tipe soal (lihat P1-004).
- (−) Query yang butuh filter berdasarkan isi `data` jsonb lebih lambat dari kolom biasa — mitigasi: index GIN di kolom jsonb yang sering difilter kalau ada masalah performa nyata (jangan premature-optimize).
