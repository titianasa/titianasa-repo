# ADR-0011: Level Assessment Scoring — Knowledge 40% / Communication 60%

Status: Accepted
Date: 2026-09-02
Supersedes: -
Superseded by: -

## Context

Roadmap-Fase-5 (`ALR_Build_Roadmap.md`, `## FASE 5 — Assessment / Exam Engine`) covers §5.1 (Exam Runtime Engine) and §5.2 (Level Assessment). `ALR_Phase_Detail_Breakdown.md` §2.11 documents 2 candidate scoring-weight schemes for a CEFR-level gate test and is explicit that this decision **must** be made before Assessment Engine is built, not left as an implicit default — "berdampak langsung ke kelulusan naik level":

1. **7-category generic**: `Vocabulary 20% / Grammar 20% / Reading 15% / Listening 15% / Writing 10% / Speaking 15% / Pronunciation 5%`.
2. **Knowledge/Communication** (the document's own recommended deviation, because ALR's product positioning is speaking-first): `Knowledge 40% / Communication 60%`, where Knowledge = Vocabulary+Grammar+Reading+Listening and Communication = Writing+Speaking+Pronunciation.

This ADR was written after Phase 1–6 (`docs/tickets/phase-1.md` through `phase-6.md`) closed and the user picked "Assessment / Exam Engine" as the next priority from `docs/STATE.md`'s "Kandidat scope berikutnya" (2026-09-02), then was asked this exact question directly (matching the source document's own instruction to decide explicitly, not default silently). **User picked Knowledge 40% / Communication 60%.**

Code-level grounding, confirmed by direct reads before writing this ADR:
- `assessments`/`attempts`/`evaluations`/`feedback`/`rubrics` already exist per ADR-0001's canonical model — `assessments.type` already allows `'level_assessment'` in its CHECK constraint, unused by any code today.
- `exam_sessions`/`proctoring_policies`/`proctoring_sessions`/`proctoring_events` also already exist in `titian-backend-bun/src/db/schema.ts` — **zero repository/service/handler code touches any of them**, the same "table exists since ADR-0001 but was never wired up" pattern `concept_prerequisites` was in before P4-003.
- `assessment_service.submitAttempt` (the assessment-attempt scoring path, distinct from the lesson-attempt path P3-004/P6-002 built) computes `score = pointsEarned / pointsPossible` **over auto-gradable questions only** — a writing/speaking question inside an assessment today contributes to neither `pointsPossible` nor any AI evaluation call; it is silently excluded from the score entirely. This is the concrete gap a Communication-weighted composite score needs to close.
- `concepts.type` CHECK constraint is only `('grammar', 'vocabulary', 'skill', 'pronunciation')` — too coarse to separate Reading/Listening/Writing/Speaking (all would fall under the catch-all `'skill'`). `questions.cefr_tag` (added migration 0015, P2-014) is the closest precedent for a nullable, additive per-question classification column.

## Decision

**Knowledge 40% / Communication 60%**, composed as:
- **Knowledge** = Vocabulary + Grammar + Reading + Listening, scored the existing way (`pointsEarned / pointsPossible` over auto-gradable mcq/fill_blank/matching questions — no change to that math).
- **Communication** = Writing + Speaking + Pronunciation, scored via AI evaluation (reusing the rubric-based pipeline P3-004/P6-002 already built for lesson attempts, adapted to run per-question inside an assessment rather than once per attempt — see `docs/tickets/phase-7.md` P7-003 for the mechanics).

This is a **fixed platform-wide default weighting for `assessments.type = 'level_assessment'`**, not a per-assessment configurable value in this ADR's scope — `assessments.config jsonb` could carry an override later, but that is a separate, smaller decision (doesn't touch scoring semantics, additive), not part of what needed a human call here.

Within each bucket, the underlying skill-category proportions are **not** independently re-litigated here — Knowledge's 4 sub-skills split their 40% evenly by default (10% each: Vocabulary/Grammar/Reading/Listening) and Communication's 3 sub-skills split their 60% evenly by default (20% each: Writing/Speaking/Pronunciation), unless a specific blueprint's `assessments.config` lists explicit per-skill weights. This keeps the MVP scoring formula simple (2 numbers decided here, not 7) while leaving room for a blueprint author to be more specific later without a schema change.

## Consequences

- `assessment_service.submitAttempt` needs a new branch for `level_assessment`-typed assessments: auto-gradable questions feed the Knowledge composite exactly as today; writing/speaking questions need a real AI evaluation call per question (new: `evaluations.question_id`, nullable, additive column — today's `evaluations` row is always 1:1 with an attempt, which breaks for an assessment with more than one non-auto-gradable question). A `unit_test`/`mock_exam`-typed assessment (the only types any code has ever exercised) is **unaffected** — this branch only activates for `level_assessment`, so P1/P3's existing assessment-taking behavior has zero regression risk from this ADR. See `docs/tickets/phase-7.md` for the full ticket breakdown.
- `questions` needs a new nullable `skill_category` column (`vocabulary`/`grammar`/`reading`/`listening`/`writing`/`speaking`/`pronunciation`) to know which bucket a given question's points belong to — additive, same precedent as `cefr_tag` (P2-014), no ADR needed for that column itself (doesn't change existing structural meaning of any table per the "JANGAN ubah struktur tabel tanpa ADR" guard in `docs/STATE.md`).
- §5.3 (IELTS/TOEFL/PTE-specific generators) stays explicitly deferred per the source document's own MVP-first ordering ("ditunda eksplisit sampai English Core CEFR stabil") — this ADR's weighting is for ALR's own CEFR Level Assessment, not an IELTS band-score formula; a later IELTS/TOEFL/PTE ADR would need its own scoring decision entirely (those exams have their own published weighting rules, not ALR's to invent).
- Proctoring (roadmap-Fase-9, `proctoring_policies`/`proctoring_sessions`/`proctoring_events`) is explicitly **not** in scope for this ADR or `docs/tickets/phase-7.md` — the source roadmap itself orders Proctoring last and separately ("paling akhir, paling sensitif... privacy/consent/retention wajib didesain bersamaan, bukan ditambahkan belakangan"), and `exam_sessions` (this ADR's concern) was deliberately schema-separated from proctoring since ADR-0001 for exactly this reason. `docs/tickets/phase-7.md` activates `exam_sessions` only.
