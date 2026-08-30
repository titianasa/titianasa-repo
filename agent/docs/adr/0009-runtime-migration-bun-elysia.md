# ADR-0009: Runtime Migration — Rust/Axum/sqlx → Bun/ElysiaJS/Drizzle
Status: Accepted
Date: 2026-08-30
Supersedes: the "Rust + Axum (backend)" line in `ALR_Build_Roadmap.md`'s stack-lock paragraph
Superseded by: -

## Context
`titian-backend` (Rust/Axum/sqlx) had grown into a full production backend
across many sessions: 34 tables, ~30 endpoints, ~9,950 lines of source and
~7,150 lines of integration tests — auth, RBAC (ADR-0006), curriculum/
lesson/question authoring with a custom markdown-like parser (ALM) and an
11-section grammar validator, an assessment+grading engine, a mastery/
FRSS spaced-repetition learning engine (ADR-0002/0003) with formulas that
reproduce exact worked examples, an AI gateway (ADR-0004) with real
OpenRouter/DeepSeek integration, R2 asset storage, and a Drive-style
file/folder/sharing system.

The user made an explicit, direct decision to replace this entirely with
Bun + ElysiaJS — not a deviation discovered mid-ticket the way most other
entries in this ADR sequence are, but a deliberate runtime/framework
change requested outright. Per this project's own rule ("JANGAN lakukan
ini tanpa ADR baru", `docs/STATE.md`), a decision that reverses a stack
line explicitly called "locked" in `ALR_Build_Roadmap.md` gets a real ADR,
not a silent rewrite.

**This ADR is scoped narrowly on purpose**: it records a runtime/language
swap, not a product or data-model decision. It does not reopen ADR-0001
through ADR-0008 — the canonical data model, the mastery formula, the
FRSS algorithm, the AI gateway's task/provider/routing shape, the credit
economy, the RBAC matrix, and the concept hierarchy semantics all carry
over unchanged. Their Rust code-fence examples get updated to
TypeScript-flavored pseudocode where they showed implementation sketches
(e.g. ADR-0004's `AITask` enum, `AIProvider` trait), but the *decisions*
those ADRs record are untouched.

## Decision

### What changes
- Runtime: Rust (tokio) → Bun.
- HTTP framework: Axum → ElysiaJS.
- Database access: sqlx (raw parameterized SQL) → **Drizzle ORM**
  (`drizzle-orm` + `drizzle-kit`, via the `drizzle-orm/bun-sql` driver —
  built on Bun's native `Bun.sql`, no extra Postgres driver dependency
  underneath). Chosen over Prisma: TypeScript-native schema-as-code, a
  query-builder style close enough to raw SQL that porting the existing
  hand-written queries is close to mechanical, and it's the standard
  pairing with Bun+Elysia in practice.
- Schema authority: `titian-backend-bun/src/db/schema.ts` (Drizzle table
  definitions) becomes the new schema source, generating migrations via
  `drizzle-kit generate`/`migrate` — replaces sqlx-cli one-for-one.
  `agent/docs/domain-model.md` remains the human-readable source of
  truth both `schema.ts` and the original hand-written `.sql` migrations
  were kept in sync with; the 34-table shape itself does not change.
- Auth: `jose` for HS256 access tokens and Google `id_token` JWKS
  verification (replaces `jsonwebtoken` + the hand-rolled JWKS
  fetch-and-cache in `google_oauth.rs`). Refresh-token hashing via
  `Bun.CryptoHasher("sha256")` (replaces `sha2`).
- R2/S3: `@aws-sdk/client-s3` + `@aws-sdk/s3-request-presigner` (same AWS
  SDK family as the Rust side's `aws-sdk-s3`, JS SDK instead of the Rust
  one — same bucket, same credentials, same presigned-URL semantics).
- AI provider calls: plain `fetch` to OpenRouter (mirrors
  `DeepSeekProvider`'s `reqwest` calls, no SDK).
- Testing: `bun:test`, each test wrapped in a Postgres transaction that's
  rolled back afterward (closest practical equivalent to `#[sqlx::test]`'s
  per-test ephemeral database).
- New repo: `titian-backend-bun/` (sibling to `titian-backend/`, its own
  directory per the multi-repo-per-app structure already in place).

### What does not change
- The 34-table schema (column names, types, constraints, FKs, indexes) —
  `schema.ts` is written directly from `domain-model.md`.
- The HTTP contract — `agent/docs/api-contract.md` stays authoritative;
  same routes, same request/response shapes, same error codes.
- Every business rule and formula: ADR-0002's mastery formula, ADR-0003's
  FRSS/SM-2 scheduler, ADR-0004's AI task/provider/routing shape,
  ADR-0005's credit economy, ADR-0006's RBAC matrix, ADR-0007's concept
  hierarchy semantics, the ALM grammar, and the Grammar Constitution's 11
  sections — all ported with identical inputs/outputs, verified by
  porting the same test scenarios (including the exact worked-example
  assertions like `mastery_score = 72` and the 5-cycle SM-2 table).
- `titian-web` (frontend) — no changes beyond eventually repointing
  `NEXT_PUBLIC_API_URL` at the new server once verified equivalent.

### Transition, not a big-bang swap
`titian-backend` (Rust) is **not deleted or archived** as part of this
ADR. It stays on disk, untouched, as the reference implementation the
port is checked against, running side-by-side with
`titian-backend-bun` on a different port until the port is verified
equivalent end-to-end (including a real-browser pass, not just a green
test suite). Retiring the Rust backend is a separate, later decision —
this ADR authorizes building the replacement, not deleting the original.

## Alternatives considered
- **Incremental strangler-fig migration (route by route, both backends
  live in production simultaneously)** — rejected for this project's
  scale: with one solo developer and no live production traffic yet,
  running two backends against the same database in production would add
  operational complexity (which backend owns which route, dual
  deployment) with no user-facing benefit. A side-by-side dev-time
  comparison (this ADR's approach) gets the same verification safety
  without that overhead.
- **Prisma instead of Drizzle** — considered and explicitly rejected via
  a direct question back to the user; Drizzle's schema-as-TypeScript-code
  and SQL-adjacent query builder is a smaller conceptual jump from the
  existing raw-SQL-via-sqlx code than Prisma's separate schema DSL and
  generated-client build step.
- **Keep sqlx-style raw SQL in Bun (via `Bun.sql` directly, no ORM)** —
  this was the original draft plan; the user asked specifically "untuk
  orm nya pakai apa?" (what ORM are we using), making clear an ORM layer
  was wanted, not a bare SQL client port.

## Consequences
- (+) One runtime for the whole stack becomes closer (Bun already runs
  `titian-web`'s tooling in places) — not a full unification since
  Next.js still targets Node/Bun as a web framework runtime separately,
  but the backend and frontend now share a language.
- (+) Drizzle's TypeScript schema gives compile-time type-checking on
  every query, something sqlx's runtime-checked raw SQL strings only
  partially provided (query-shape errors now surface at build time, not
  first-request time).
- (−) Full re-implementation risk: ~17,000 lines of tested business logic
  need porting with equivalent behavior, not just equivalent-looking
  code — mitigated by porting test-by-test against the same real
  Postgres/R2/OpenRouter dependencies the Rust version already proved
  against, in the same dependency order the original was built in.
- (−) Two backend codebases exist simultaneously during the transition —
  accepted as the cost of verifying equivalence before retiring working
  code, not left open-ended (retirement is the explicit next decision
  once the port is done).
