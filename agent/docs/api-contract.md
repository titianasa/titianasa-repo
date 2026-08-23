# ALR API Contract v1
Base URL: `/api/v1`. Auth: `Authorization: Bearer <jwt>` kecuali disebutkan lain.

## Aturan konsisten (wajib di semua endpoint)
- Error selalu: `{ "error": "snake_case_code", "detail": "optional string" }`
- List selalu dipaginasi: `{ "items": [...], "next_cursor": "string|null" }`
- Timestamp selalu ISO 8601 UTC.
- Endpoint yang mengubah data finansial (`credits`, `transactions`) wajib menerima header `Idempotency-Key`.
- Semua list query difilter `organization_id` dari JWT claim (ADR-0006), tidak pernah dari query param mentah.

---

## Auth

### `POST /auth/google/callback`
Auth: none
```
Request:  { "id_token": "string" }
Response 200:
  { "access_token": "jwt", "refresh_token": "jwt",
    "user": { "id": "uuid", "email": "string", "name": "string" } }
Error: 401 { "error": "invalid_token" }
```

### `POST /auth/refresh`
```
Request:  { "refresh_token": "jwt" }
Response 200: { "access_token": "jwt" }
Error: 401 { "error": "invalid_refresh_token" }
```

---

## Users & Organization

### `GET /users/me`
```
Response 200:
  { "id": "uuid", "email": "string", "name": "string",
    "roles": [{ "organization_id": "uuid", "role": "student" }] }
```

### `GET /organizations/{id}/members?cursor=&limit=`
Auth: role org_owner/academic_director di org tsb.
```
Response 200: { "items": [{ "user_id": "uuid", "name": "string", "role": "string" }], "next_cursor": null }
Error: 403 { "error": "forbidden" }
```

---

## Content

### `GET /curricula/{curriculum_id}/tree`
```
Response 200:
  { "curriculum": { "id": "uuid", "code": "string", "name": "string", "status": "published" },
    "levels": [
      { "id": "uuid", "code": "pre_basic", "name": "Pre-Basic",
        "units": [
          { "id": "uuid", "code": "unit-1", "title": "English Alphabet",
            "lessons": [{ "id": "uuid", "title": "Learn", "type": "learn", "status": "published" }] } ] } ] }
Error: 404 { "error": "curriculum_not_found" }
```

### `POST /curricula`, `POST /curricula/{id}/levels`, `POST /levels/{id}/units` (P2-009)
Auth: curriculum_developer+ (hasil selalu `status: draft` untuk curriculum; level/unit tidak punya status sendiri)
```
POST /curricula
Request: { "subject_id": "uuid", "code": "string", "name": "string", "framework": "cefr" }
Response 201: { "id": "uuid", "status": "draft" }

POST /curricula/{id}/levels
Request: { "code": "string", "name": "string", "order_index": 0 }
Response 201: { "id": "uuid" }

POST /levels/{id}/units
Request: { "code": "string", "title": "string", "order_index": 0 }
Response 201: { "id": "uuid" }

Error: 403 { "error": "forbidden" }
```

### `POST /lessons` (P2-008)
Auth: curriculum_developer+ (hasil selalu `status: draft`)
```
Request:
  { "unit_id": "uuid", "title": "string", "type": "learn",
    "order_index": 0, "content": "# Present Simple\n\n...", "format": "markdown",
    "concept_ids": ["uuid"] }  -- opsional, default [] (P2-011: lesson yang tertaut ke
                                  -- concept type="grammar" wajib lolos Grammar Constitution
                                  -- (agent/docs/curriculum-constitution.md) sebelum submit-review)
Response 201: { "id": "uuid", "status": "draft" }
Error: 422 { "error": "invalid_lesson_type", "detail": "..." }
422 { "error": "invalid_source_format", "detail": "..." }
422 { "error": "invalid_alm_source", "detail": "..." }       -- directive tidak ditutup, dst (P2-006)
422 { "error": "invalid_block_schema", "detail": "..." }     -- hasil parse tidak lolos validasi block (P2-003)
422 { "error": "question_embed_not_found", "detail": "..." } -- question_embed merujuk question_id yang tidak ada
```
`content` diproses lewat Paste Normalizer (P2-007, kalau `format: "html"`) lalu ALM Parser (P2-006) sebelum ditulis jadi `content_blocks` — respons ini tidak mengembalikan block list, `GET /lessons/{id}` (sudah ada) yang menampilkannya.

### `PUT /lessons/{id}` (P2-008)
Auth: curriculum_developer+ — **hanya untuk lesson berstatus `draft`/`in_review`**, `published` selalu ditolak (ADR-0008)
```
Request: { "content": "...", "format": "markdown" }
Response 200: { "id": "uuid", "status": "draft" }
Error: 404 { "error": "lesson_not_found" }
422 { "error": "cannot_edit_published_content" }
```

### `GET /lessons/{id}`
```
Response 200:
  { "id": "uuid", "title": "string", "type": "learn", "status": "published",
    "blocks": [{ "id": "uuid", "type": "text", "order_index": 0, "data": {} }],
    "qa_report": { "passed": true, "issues": [] } | null }
Error: 404 { "error": "lesson_not_found" }
403 { "error": "lesson_not_published" }  -- kecuali role curriculum_developer/reviewer/admin
```
`qa_report` (P2-014) is `null` until `submit-review` has run at least once.

### `POST /lessons/{id}/submit-review` (P2-005)
Auth: curriculum_developer+ (own draft → in_review)
```
Response 200: { "id": "uuid", "status": "in_review", "qa_report": { "passed": bool, "issues": [{"category": "grammar_constitution"|"cefr_mismatch", "message": "string"}] } }
Error: 404 { "error": "lesson_not_found" }
422 { "error": "invalid_status_transition", "detail": "cannot submit for review from status \"published\" — must be \"draft\"" }
422 { "error": "grammar_constitution_incomplete", "detail": "missing required section(s): 07 — Signal words" }
  -- P2-011: only for a lesson linked (lesson_concepts) to a concepts.type="grammar" row — hard
  -- block, distinct from the same category possibly appearing (non-blocking) in qa_report above
```
P2-014: the Content QA Agent always runs here (once the P2-011 hard gate above passes) and its
report is written to `qa_report` — a QA finding (`passed: false`) never blocks this transition
(response is still `200`/`in_review`), it's only surfaced for the human reviewer.

### `POST /lessons/{id}/publish` (P2-005)
Auth: reviewer+ (academic_director/org_owner/platform_admin/reviewer — NOT curriculum_developer)
```
Response 200: { "id": "uuid", "status": "published", "qa_report": {...} | null }
Error: 404 { "error": "lesson_not_found" }
422 { "error": "invalid_status_transition", "detail": "cannot publish from status \"draft\" — must be \"in_review\"" }
```

### `POST /lessons/{id}/reject` (P2-005)
Auth: reviewer+ (same as publish) — sends `in_review` back to `draft`
```
Response 200: { "id": "uuid", "status": "draft", "qa_report": {...} | null }
Error: 404 { "error": "lesson_not_found" }
422 { "error": "invalid_status_transition", "detail": "cannot reject from status \"draft\" — must be \"in_review\"" }
```

---

## Question Bank

### `POST /question-banks/{id}/questions`
Auth: curriculum_developer+ (status hasil selalu `draft`)
```
Request:
  { "type": "mcq", "difficulty": 0.4,
    "data": { "prompt": "I ___ a student.", "options": ["am","is","are"] },
    "correct_answer": { "index": 0 },
    "explanation": { "text": "..." },
    "concept_ids": ["uuid"] }
Response 201: { "id": "uuid", "status": "draft" }
Error: 422 { "error": "invalid_question_schema", "detail": "unknown field for type=mcq" }
```

### `GET /question-banks/{id}/questions?status=&cursor=&limit=`
```
Response 200: { "items": [{ "id": "uuid", "type": "mcq", "difficulty": 0.4, "status": "draft", "qa_report": {...} | null }], "next_cursor": null }
```

### `POST /questions/{id}/submit-review`, `POST /questions/{id}/publish`, `POST /questions/{id}/reject` (P2-005)
Sama pola persis seperti `/lessons/{id}/submit-review`/`/publish`/`/reject` di atas (auth, response shape, error shape identik, `qa_report` P2-014 juga sama — QA Agent jalan di `submit-review`, findingnya (kategori `question_schema`) tidak pernah memblokir transisi) — `questions` dan `lessons` berbagi state machine yang sama (`service/publish_flow.rs`).
```
Response 200: { "id": "uuid", "status": "in_review" | "published" | "draft", "qa_report": {...} | null }
Error: 404 { "error": "question_not_found" }
422 { "error": "invalid_status_transition", "detail": "..." }
```

---

## Assessment & Attempt

### `GET /assessments/{id}`
```
Response 200:
  { "id": "uuid", "type": "unit_test", "title": "string", "config": { "duration_minutes": 15 },
    "question_count": 10 }
```

### `POST /assessments/{id}/attempts`
Membuat attempt baru untuk user saat ini.
```
Response 201:
  { "attempt_id": "uuid", "status": "in_progress",
    "questions": [{ "id": "uuid", "type": "mcq", "data": { "prompt": "...", "options": [...] } }] }
Error: 409 { "error": "attempt_already_in_progress", "attempt_id": "uuid" }
```

### `POST /attempts/{attempt_id}/submit`
```
Request:  { "answers": { "<question_id>": { "index": 0 }, "<question_id_2>": { "text": "..." } } }
Response 200:
  { "attempt_id": "uuid", "status": "submitted", "score": 85.0, "learning_events_created": 12 }
Error:
  409 { "error": "attempt_already_submitted" }
  422 { "error": "missing_required_answers", "missing": ["question_id_3"] }
```

---

## Learning Engine

### `GET /mastery/{concept_id}`
```
Response 200: { "concept_id": "uuid", "score": 72, "confidence": 0.6, "last_reviewed_at": "iso8601" }
Error: 200 { "concept_id": "uuid", "score": null, "confidence": 0, "message": "insufficient_data" }
```

### `GET /review-queue?limit=10`
```
Response 200:
  { "items": [
      { "concept_id": "uuid", "concept_name": "present_simple", "due_at": "iso8601",
        "suggested_question_ids": ["uuid"] } ] }
```

---

## Assets

### `POST /assets/upload`
```
Request: multipart/form-data (file)
Response 201: { "id": "uuid", "url": "https://r2.../signed-url", "type": "audio/mpeg" }
Error: 413 { "error": "file_too_large" }
```
Always writes `visibility: "private"` — no visibility choice on this endpoint (P1-010 predates P2-010).

### `POST /assets/presigned-upload` (P2-010)
Auth: any authenticated user (same as `/assets/upload`). No DB row is created by this call.
```
Request: { "content_type": "image/png" }
Response 201: { "asset_id": "uuid", "upload_url": "https://r2.../presigned-put-url" }
```
Client uploads the file bytes directly to `upload_url` via `PUT` (bypasses this backend entirely — 2.14), then calls `/assets/confirm`.

### `POST /assets/confirm` (P2-010)
Auth: any authenticated user.
```
Request: { "asset_id": "uuid", "content_type": "image/png", "visibility": "public" }
Response 201: { "id": "uuid", "url": "https://r2.../signed-url", "type": "image/png" }
Error: 422 { "error": "asset_not_uploaded", "detail": "..." }   -- no object found at this key yet (HEAD check failed)
422 { "error": "invalid_visibility", "detail": "..." }          -- must be "public" or "private"
```
`visibility` picks the returned signed GET URL's TTL — longer for `"public"` (`asset_public_signed_url_ttl_seconds`, default 7 days) than `"private"` (`asset_signed_url_ttl_seconds`, default 1 hour, same as `/assets/upload`).

---

## AI Gateway (stub Phase 1, penuh di Phase 4)

### `POST /ai/evaluate`
```
Request: { "task": "grammar_evaluation", "input": { "text": "I is a student." } }
Response 200:
  { "ai_task_id": "uuid", "status": "done",
    "result": { "errors": [{ "span": [2,4], "issue": "subject_verb_agreement", "suggestion": "am" }] },
    "credit_charged": 1 }
Error:
  402 { "error": "insufficient_credit", "required": 1, "balance": 0 }
  422 { "error": "ai_output_validation_failed" }   -- tidak charge credit (ADR-0005)
```

### `POST /ai/generate-lesson` (P2-013)
Auth: curriculum_developer+ (same gate as `POST /lessons`). 0 credit charged either way (ADR-0005 —
platform cost, not user cost). AI output is validated (ALM parse → block schema → Grammar
Constitution if applicable) **before** any `lessons` row is written — a failed generation never
leaves an orphan draft lesson behind.
```
Request:
  { "unit_id": "uuid", "lesson_type": "learn", "order_index": 0, "topic": "Present Perfect",
    "grammar_target": "present_perfect", "vocab_target": ["already", "yet"], "concept_ids": ["uuid"] }
  -- grammar_target/vocab_target/concept_ids all optional, default null/[]/[]
Response 201: { "ai_task_id": "uuid", "status": "done", "lesson_id": "uuid" }
  -- lesson_id's status is always "draft" — never auto-published (2.6/ADR-0004)
Error:
  422 { "error": "ai_output_validation_failed" }      -- provider call itself failed
  422 { "error": "invalid_alm_source", "detail": "..." }             -- AI output didn't parse as ALM
  422 { "error": "invalid_block_schema", "detail": "..." }           -- a block's data failed P2-003 schema
  422 { "error": "grammar_constitution_incomplete", "detail": "..." } -- grammar_target set, missing section(s)
  403 { "error": "forbidden" }
```

### `POST /ai/generate-questions` (P2-013)
Auth: curriculum_developer+ (same gate as `POST /question-banks/{id}/questions`). 0 credit charged.
Unlike lesson generation, the model outputs Semantic JSON directly (P2-004 schema), not ALM — a
deliberately separate prompt/parsing path. Every item is validated **before** any `questions` rows
are written — one invalid item fails the whole batch, no partial set is ever created.
```
Request:
  { "bank_id": "uuid", "question_type": "mcq", "topic": "to be", "count": 5, "difficulty": 0.4,
    "concept_ids": ["uuid"] }
  -- concept_ids optional, default []
Response 201: { "ai_task_id": "uuid", "status": "done", "question_ids": ["uuid", ...] }
  -- all created questions are always "draft"
Error:
  422 { "error": "ai_output_validation_failed" }        -- provider call failed, or output wasn't a JSON array
  422 { "error": "invalid_ai_output_count", "detail": "expected 5 question(s), got 3" }
  422 { "error": "invalid_question_schema", "detail": "..." }  -- an item failed P2-004 schema
  403 { "error": "forbidden" }
```

---

## Health

### `GET /health`
```
Response 200: { "status": "ok", "db": "ok", "redis": "ok" }
```
