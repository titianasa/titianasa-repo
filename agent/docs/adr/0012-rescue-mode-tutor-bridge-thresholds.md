# ADR-0012: Rescue Mode trigger threshold + Tutor Bridge scope

Status: Accepted
Date: 2026-09-03
Supersedes: -
Superseded by: -

## Context

`ALR_Phase_Detail_Breakdown.md` line 821 explicitly flags this as a
decision that needs a new ADR before implementation: "threshold
rescue-mode/tutor-bridge (3.9)" — grouped with 2 other decisions this
project already resolved via ADR (level-assessment scoring weights,
ADR-0011; attempt-vs-lesson-version, still open). §3.8/§3.9 of
roadmap-Fase-3 were deferred all the way back in `docs/tickets/phase-4.md`
("terhubung Phase 4/8" — needed a working tutor marketplace to bridge
*to*), which only became real in this session's Phase 15/17
(`titian-web`'s `/marketplace`, tutor booking, reputation).
`docs/STATE.md`'s Phase 21 entry ("item ke-8 dari 14", part of the
2026-09-03 "kerjakan semuanya" authorization) is what finally unblocks
this — this ADR is written now, before P21 code, per the source
document's own instruction.

`lms full.md` §35-36 (its own numbering, distinct from the
roadmap-Fase-3 "§3.9" numbering used elsewhere in this project's docs)
describes "Rescue Mode" with an illustrative, not prescriptive,
example:

> Misalnya learner sudah tiga kali gagal: Present Perfect. Attempt 1 →
> 42%, Attempt 2 → 48%, Attempt 3 → 51%. ALR jangan terus memberikan
> soal yang sama. AI berkata: "Let's slow down... Let's learn it
> another way."

It does **not** specify: what counts as one "attempt" at code level,
what score counts as a failure, or what the AI should concretely do
beyond re-teach (the doc's own 8-step remediation — visual
explanation, Indonesian analogy, contrast, graduated exercises,
speaking, retest — is itself a content-authoring pipeline this project
hasn't built; see `docs/STATE.md`'s Phase 24 "AI Content Generation
Pipeline", explicitly a separate, much later phase). "Tutor bridge"
itself is not a named section anywhere in the source docs — it is this
project's own shorthand (first appearing in `phase-4.md`'s "Keputusan
scope") for the pitch line in `lms full.md`'s own executive summary:
"menghubungkan learner dengan AI maupun human tutor ketika membutuhkan
bantuan lebih lanjut."

Code-level grounding, confirmed by direct reads before writing this ADR:
- **No "attempt round" exists at concept granularity.** `masteries`/
  `frss_schedule` are upserted-in-place, current-value-only (no
  history table — noted as a known limitation since Phase 4). The only
  per-answer history available is `learning_events` (`entityType:
  "question"`, `payload.correct`, `payload.concept_ids`), joined
  through `question_concepts` — `masteryRepository.findEventsForConcept`
  already does exactly this join, just unordered/unlimited.
- **No concept↔tutor mapping exists anywhere.** `tutor_profiles.specializations`
  is a free-form `jsonb` array, not FK'd to `subjects` or `concepts`.
  A "book a tutor for Present Perfect specifically" filter would be
  fabricated precision the data model doesn't support.
- `lesson_concepts` (concept → lesson, many-to-many, `ADR-0007`-era
  table) is real and queryable — "here's a lesson that re-teaches this
  concept" is a genuine, already-supported recommendation, unlike a
  concept-matched tutor search.

## Decision

**1. Rescue Mode trigger — reinterpreted at question-answer granularity,
not assessment-round granularity.** The doc's "3 failed attempts" is
operationalized as: **the learner's last 3 answered questions tagged
to this concept (`learning_events`, newest first) were all incorrect**.
This is a deliberate simplification of the doc's illustrative example
(3 full assessment attempts) down to what the data model actually
supports (per-question correctness, already recorded on every
`POST /questions/{id}/check` and `submitAttempt` call) — pedagogically
equivalent as a struggle signal (3 consecutive wrong answers on the
same concept, regardless of which screen they came from), and requires
zero new tracking infrastructure. Threshold is a new config field,
`rescueModeConsecutiveFailures`, default **3** (matches the doc's own
example number), env-overridable (`RESCUE_MODE_CONSECUTIVE_FAILURES`),
same pattern as `weaknessScoreThreshold`/`masteryConfidenceThreshold`.

**2. Rescue Mode remediation content — NOT built.** The doc's 8-step
sequence (visual explanation → Indonesian analogy → simple example →
contrast → easy exercise → medium exercise → speaking → retest) is a
full adaptive micro-curriculum per concept — that is content-authoring
work belonging to Phase 24 (AI Content Generation Pipeline) and Phase
25 (actual curriculum content), not this "quick win" ticket-phase. What
P21 actually ships when rescue mode triggers: a plain-language nudge
("Sepertinya ini masih sulit — coba pelan-pelan dulu.") plus links to
any **existing, already-published** lessons that teach the concept
(via `lesson_concepts`, reusing real content instead of synthesizing
new content this project can't yet generate).

**3. Tutor Bridge — a general marketplace link, not a concept-matched
search.** Because no concept↔tutor relation exists in the schema (and
inventing one now would be a much larger, separate scope — "which
tutors teach which concepts" implies tutor-side curriculum tagging
that doesn't exist), the bridge is a plain CTA to `/marketplace`
(browse all tutors/products) shown alongside the rescue-mode nudge —
honest about what the platform can actually target today, not a fake
"tutors for Present Perfect" filter.

## Consequences

- `masteryRepository` gets one new additive read function
  (`findRecentEventsForConcept`, ordered + limited) — no changes to
  the existing `findEventsForConcept` used by mastery recompute.
- New `GET /concepts/{id}/rescue-status` endpoint (own-data-only, same
  "milik sendiri" framing as `GET /mastery/{concept_id}`) plus an
  additive `rescue_triggered: boolean` field on
  `POST /questions/{id}/check`'s response, computed at the same
  per-concept loop site that already calls `recomputeForConcept`/
  `frssService.recordReview` — no new hook site, no second DB
  round-trip needed for the common case (answering a question is
  exactly when rescue mode needs to be known).
- If `rescueModeConsecutiveFailures` needs retuning later (e.g. product
  data shows 3 is too aggressive/lenient), it's a config change, not a
  schema or ADR change — this ADR fixes the *mechanism* (question-level
  streak, not assessment-round), not the number itself as permanent.
- Does **not** touch or supersede ADR-0002 (mastery formula) or
  ADR-0003 (FRSS) — rescue mode reads their outputs (`learning_events`,
  indirectly `masteries`) but does not change either algorithm.
