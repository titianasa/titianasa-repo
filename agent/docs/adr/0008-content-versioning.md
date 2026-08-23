# ADR-0008: Content Versioning & Attempt Snapshot
Status: Accepted
Date: 2026-08-23
Supersedes: -
Superseded by: -

## Context
`lessons.version`/`questions.version` (ADR-0001) exist as columns but the rules around them were never decided: if a `published` question or lesson gets edited, what happens to `attempts` that already reference it? `ALR_Phase_Detail_Breakdown.md` 2.15 is explicit this must be a real ADR, not "diputuskan diam-diam di kode" (decided silently in code) — publish flow (P2-005) cannot start without this settled, since publishing an edit *is* the moment versioning rules apply.

Two things are at stake, and they don't need the same answer:
1. **Scored history (`attempts`)** — fairness-critical. A student's `attempts.score` was computed against a specific `correct_answer` at submit time. If that question's content is edited afterward, the historical attempt must never appear to have been graded against something different than what the student actually saw.
2. **Informational content (`lessons`/`content_blocks`)** — not scored, no "correct answer" to protect. Revisiting a lesson later and seeing the latest published version (like any CMS page) is normal and expected, not a fairness problem.

One thing already works correctly and doesn't need fixing: `learning_events.payload` (P1-007) already snapshots `correct`/`difficulty`/`concept_ids` at submit time — it never re-derives from the live `questions` row. Mastery (ADR-0002) already reads only from that snapshot. This ADR extends the same snapshot principle to `attempts` itself, where it's currently missing.

## Decision

### 1. `attempts` gets a full question snapshot (additive)
```sql
ALTER TABLE attempts ADD COLUMN question_snapshot JSONB NULL;
```
Populated at submit time (`assessment_service::submit_attempt`, same place `learning_events` already get written) with `{ "<question_id>": { "data": ..., "correct_answer": ..., "explanation": ..., "version": N }, ... }` for every question in that attempt — captured from whatever `questions` rows looked like *at that exact moment*, not re-fetched later. `NULL` for attempts submitted before this ADR (nothing retroactive; those attempts' scores remain valid, they just can't be "replayed" with full original question content).

This makes `attempts` fully self-contained: reviewing a past attempt never depends on the live state of `questions`, no matter how many times the question gets edited or archived afterward.

### 2. Lessons/content_blocks are NOT snapshotted
Revisiting a lesson shows the current `published` version. No per-user snapshot, no history table for lesson content. This is a deliberate asymmetry, not an oversight — lessons aren't scored, so there's no fairness property to protect, and adding snapshot machinery here would be speculative complexity with no ticket that needs it.

### 3. Editing rule: draft vs. published
- **Editing a `draft` or `in_review` question/lesson**: in-place, same row, no version bump. It hasn't gone live yet — free to iterate.
- **Editing a `published` question/lesson**: the row is never mutated in place. A new row is created (`version = old.version + 1`, `status = 'draft'`), and:
  ```sql
  ALTER TABLE questions ADD COLUMN superseded_by UUID NULL REFERENCES questions(id);
  ALTER TABLE lessons   ADD COLUMN superseded_by UUID NULL REFERENCES lessons(id);
  ```
  The **old row stays `published` and keeps serving live traffic** untouched while the new draft goes through the normal review flow (P2-005). Only when the new version is itself published does the old row's `superseded_by` get set to the new row's id and its `status` flip to `archived`.

  **Phase 2 MVP scope, stated explicitly so it isn't assumed to be more than it is:** the API simply refuses to edit a `published` row (`422`/`403` per existing error-envelope conventions) — the *columns* above exist and are schema-ready, but the "auto-create a draft revision" convenience flow is not built this phase. To update published content in Phase 2, an author archives the old row and creates a new `draft` from scratch, then manually re-links whatever `assessment_questions`/`content_blocks.question_embed` references should point at it. This is deliberately conservative: an assessment's question set never changes under a student's feet without an explicit, visible re-link action by a human. Building the automatic "supersede and relink" UX is real future work, tracked here rather than half-built now.

### Why not full immutable-row-per-version for everything (Option A taken further)
Wrapping *every* edit (even pre-publish drafts) in a new-row-per-version model was considered and rejected for MVP: it would mean `assessment_questions`/`content_blocks` need to resolve "current version of this question" through a chain on every read, adding a join and a resolution step to the hot path (every attempt creation, every lesson view) for a problem (draft churn) that doesn't need historical preservation at all — nobody needs to see "draft edit #4 of a question that was never published."

## Alternatives considered
- **No snapshot, `attempts` just re-reads live `questions` on demand** — rejected outright, this is the "decided silently" failure mode the source doc warned against; a `correct_answer` edit would retroactively change what a graded historical attempt "was graded against."
- **Version everything (lessons AND questions AND attempts) via a full audit-log table** — rejected as over-engineering for Phase 2's actual need; `question_snapshot` on `attempts` solves the one place where losing history has real fairness consequences, without building generic content history nobody asked for yet.
- **Bump version + flip to draft on the *same row* when editing published content** — rejected: makes a live lesson/assessment disappear out from under active users mid-edit, which is a worse failure mode than the extra row.

## Consequences
- (+) Fairness/audit property is real from Phase 2 onward: no attempt can silently change meaning after the fact.
- (+) Additive only (`question_snapshot`, two `superseded_by` columns) — no existing column semantics change, `learning_events`'s existing snapshot pattern is extended rather than replaced with something different.
- (+) Published content is never mutated in place — no risk of a typo-fix accidentally rewriting graded history.
- (−) Editing published content in Phase 2 is manual (archive + new draft + manual re-link) rather than a smooth "revise and republish" flow — explicitly deferred, tracked here so it isn't quietly forgotten once Phase 2 ships.
- (−) `attempts.question_snapshot` duplicates data already in `questions` at submit time — accepted, standard trade-off for point-in-time correctness (same trade-off `learning_events.payload` already made in P1-007, this is not a new pattern).
