# ADR-0007: Concept Hierarchy
Status: Accepted
Date: 2026-08-23
Supersedes: -
Superseded by: -

## Context
`concepts` (ADR-0001) is flat today: `(id, subject_id, code, name, type)`. `ALR_Phase_Detail_Breakdown.md` 3.1 requires drill-down weakness detection at sub-concept granularity — not "Grammar 71%" but:
```
Grammar 71%
  Present Simple 61%  ← weak
    Affirmative  85%
    Negative     64%
    Questions    49%  ← weak
    3rd Person   42%  ← very weak
```
That section says explicitly this needs "concept hierarchy, bukan flat list" and needs to exist **starting from Phase 2** — Phase 2 is where hundreds of concepts get created as content is authored, and retrofitting a hierarchy onto an already-large flat set later means reclassifying every row instead of authoring them correctly the first time.

A separate, easily-confused concern already exists: `concept_prerequisites` (ADR-0001, unchanged by this ADR) — "must know X before Y", a prerequisite graph between *unrelated* concepts (e.g. `present_simple` requires `subject_pronouns` first). That is not containment. This ADR is about **IS-A/PART-OF hierarchy** (a concept *is a sub-topic of* another), which is a different relationship.

3.2 (Knowledge Graph) additionally describes cross-skill *associative* links (vocabulary "food" relates to grammar "like/don't like" relates to speaking "food conversation") — this is neither containment nor prerequisite, it's a general graph edge. That is explicitly a Phase 3 concern (weakness detection / recommendation), not required for Phase 2 content authoring itself. Building it now would be speculative — deferred, see Consequences.

## Decision

### Schema (additive)
```sql
ALTER TABLE concepts ADD COLUMN parent_concept_id UUID NULL REFERENCES concepts(id);
CREATE INDEX idx_concepts_parent ON concepts(parent_concept_id);
```
- `NULL` = top-level concept (e.g. `present_simple` itself has no parent; `present_simple_questions` has `parent_concept_id = present_simple.id`).
- Self-referencing FK, one parent per concept (a tree, not a DAG) — matches every example in the source doc (`Present Simple → Questions → 3rd Person` is a strict path, never a concept with two parents). If a genuine need for multi-parent membership shows up later, that is a new decision (new ADR), not a silent extension of this one.
- No hard-coded max depth in the schema. Typical depth from the examples is 2–3 levels (`Grammar → Present Simple → Questions`); this is a convention for content authors, not a DB constraint.

### Cycle prevention
Postgres doesn't enforce "no cycles in a self-referencing FK" declaratively. Enforced at the application layer: before setting/changing `parent_concept_id`, the service walks the *proposed* parent's ancestor chain and rejects the write if the concept being edited appears in it (would create a cycle) or if `parent_concept_id == id` (self-loop). This mirrors how this codebase already validates other invariants in the service layer rather than the DB layer (e.g. `question_schema.rs`).

### Query pattern
Ancestor chain and descendant subtree are both implemented as `WITH RECURSIVE` queries in `concept_repository.rs` — the standard Postgres approach, no ORM-level tree library needed. Both directions get at least one real caller in Phase 2 (not just migration-with-no-use): the drill-down UI (later) walks descendants of a concept; a "which top-level skill does this belong to" breadcrumb walks ancestors. Phase 2 exercises the descendant query specifically via P2-001's own test suite even before Phase 3 needs it live.

### `question_concepts` / `lesson_concepts` still link at any level
No change to those junction tables. A question can link to `present_simple_questions_3rd_person` directly (leaf-level, preferred — most precise) or to `present_simple` (coarser) — both are valid, the hierarchy doesn't force re-tagging existing links. Mastery/FRSS (ADR-0002/0003) continue to operate on whatever `concept_id` a `learning_event` actually references; aggregating a parent's mastery from its children's mastery (e.g. "Grammar 71%" as a roll-up of its sub-concepts) is a Phase 3 read-time computation, not something this ADR needs to solve now.

## Alternatives considered
- **Materialized path (`ltree` extension or a `path` text column like `'grammar.present_simple.questions'`)** — faster subtree queries at scale, but adds a Postgres extension dependency (`ltree`) and a denormalized field that must stay in sync with `parent_concept_id` on every move. Rejected for now: Phase 2's concept count is nowhere near the scale where `WITH RECURSIVE` becomes a real bottleneck. Revisit as a *performance* migration later if it ever is, not an architecture decision now.
- **Separate `concept_hierarchy` closure table (ancestor, descendant, depth)** — avoids recursive queries entirely, common at large scale. Rejected for the same reason as `ltree`: solves a scale problem Phase 2 doesn't have yet, at the cost of a second table that must stay consistent with `concepts` on every insert/move.
- **Cross-skill associative graph (`concept_relations`) built now alongside containment** — considered because 3.2 describes it, but 3.2 is scoped to Phase 3 explicitly in the source doc, and no Phase 2 ticket actually needs it to author content. Building it speculatively risks guessing the wrong edge semantics (directed? weighted? typed by relation-kind?) before Phase 3's actual recommendation engine defines what it needs from it. Deferred — flagged here so Phase 3 planning starts from this note instead of rediscovering the gap.

## Consequences
- (+) Phase 2 content authoring can immediately organize concepts correctly (`Present Simple` → `Questions` → `3rd Person`) instead of a flat tag soup that needs manual reclassification before Phase 3 can use it.
- (+) Additive only — no existing table's meaning changes, `concept_prerequisites` is untouched and keeps its distinct (prerequisite, not containment) semantics.
- (−) Cycle prevention is application-layer, not database-enforced — a direct SQL `UPDATE` bypassing the service could theoretically introduce a cycle. Accepted risk (same trust boundary as every other jsonb-validated-in-app-layer decision in ADR-0001).
- (−) Cross-skill associative relations (3.2) remain undesigned — explicitly deferred, not forgotten. Phase 3 planning must address this before weakness-detection recommendation logic is built, not assume it already exists.
