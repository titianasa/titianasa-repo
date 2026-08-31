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

### `GET /curricula` (Content Studio)
Auth: any authenticated user (no permission row for Curriculum "View" — same precedent as the tree endpoint below). No filter/pagination — admin-sized dataset.
```
Response 200: { "items": [{ "id": "uuid", "code": "string", "name": "string", "status": "draft" }] }
```
Ordered by `code`.

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
422 { "error": "assessment_embed_not_found", "detail": "..." } -- assessment_embed (P3-003) merujuk assessment_id yang tidak ada
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
    "blocks": [{ "id": "uuid", "type": "text", "order_index": 0, "data": {},
                 "raw_source": "She works at a school." | null }],
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

### `GET /question-banks` (Question Bank UI)
Auth: any authenticated user (no permission row for QuestionBank "View" on banks themselves — same precedent as `GET /curricula`). No filter/pagination — admin-sized dataset.
```
Response 200: { "items": [{ "id": "uuid", "name": "string" }] }
```
Ordered by `name`.

### `POST /question-banks` (Question Bank UI)
Auth: curriculum_developer+ (same permission row as creating a question within a bank — `Resource::QuestionBank, Action::Create` covers both).
```
Request: { "subject_id": "uuid", "name": "string" }
Response 201: { "id": "uuid", "name": "string" }
Error: 403 { "error": "forbidden" }
```

### `GET /questions/{id}` (Question Bank UI)
Full single-question detail, including `correct_answer` — this is the authoring/review surface (Studio), never a student-facing response, so unlike `POST /attempts/{id}` the answer key is not withheld.
```
Response 200:
  { "id": "uuid", "bank_id": "uuid", "type": "mcq", "difficulty": 0.4,
    "data": { "prompt": "...", "options": [...] }, "correct_answer": { "index": 0 },
    "explanation": { "text": "..." } | null, "status": "draft",
    "qa_report": { "passed": true, "issues": [] } | null, "cefr_tag": "a1" | null }
Error: 404 { "error": "question_not_found" }
403 { "error": "question_not_published" }  -- kecuali role curriculum_developer/reviewer/admin, sama pola seperti GET /lessons/{id}
```

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
Response 200: { "items": [{ "id": "uuid", "type": "mcq", "difficulty": 0.4, "status": "draft",
                             "qa_report": {...} | null, "data": { "prompt": "...", "options": [...] } }],
                 "next_cursor": null }
```
`data` is included for list-row preview purposes (Question Bank UI) — `correct_answer` deliberately isn't, use `GET /questions/{id}` for the full review surface.

### `POST /questions/{id}/submit-review`, `POST /questions/{id}/publish`, `POST /questions/{id}/reject` (P2-005)
Sama pola persis seperti `/lessons/{id}/submit-review`/`/publish`/`/reject` di atas (auth, response shape, error shape identik, `qa_report` P2-014 juga sama — QA Agent jalan di `submit-review`, findingnya (kategori `question_schema`) tidak pernah memblokir transisi) — `questions` dan `lessons` berbagi state machine yang sama (`service/publish_flow.rs`).
```
Response 200: { "id": "uuid", "status": "in_review" | "published" | "draft", "qa_report": {...} | null }
Error: 404 { "error": "question_not_found" }
422 { "error": "invalid_status_transition", "detail": "..." }
```

### `GET /questions/{id}/stem` (P3-001/P3-002)
Auth: any authenticated user, sama pola akses seperti `GET /questions/{id}` (published = open read, kecuali role curriculum_developer/reviewer/admin). **Learner-safe** — beda dari `GET /questions/{id}` yang eksplisit surface authoring/review (selalu include `correct_answer`), endpoint ini cuma balikin cukup buat *merender* soal. Dipakai `QuestionRenderer` (P3-002) buat ambil `data` sebuah `question_embed` block.
```
Response 200: { "id": "uuid", "type": "mcq", "data": { "prompt": "...", "options": [...] } }
Error:
  404 { "error": "question_not_found" }
  403 { "error": "question_not_published" }
```

### `POST /questions/{id}/check` (P3-001)
Auth: any authenticated user (bukan role-gated seperti authoring endpoint lain di section ini). Menjawab 1 soal *inline* — dipakai buat `question_embed` di dalam konten lesson — **independen dari alur `attempts`/`assessments`** di bawah: tidak ada row `attempts` yang ditulis. Grading 100% server-side (`correct_answer` tidak pernah ada di request, cuma di response setelah grading). Mendukung ketiga tipe soal terdaftar (`mcq`/`fill_blank`/`matching`). Efek sampingnya sama seperti attempt formal: 1 `learning_events` row + recompute `masteries`/`frss_schedule` untuk tiap concept yang ditaut ke soal itu — supaya latihan inline juga memberi sinyal ke learning engine, bukan cuma assessment formal.
```
Request: { "submitted_answer": { "index": 0 } }   -- bentuk sama seperti correct_answer question itu sendiri (per tipe)
Response 200: { "correct": true, "correct_answer": { "index": 0 }, "explanation": { "text": "..." } | null }
Error:
  404 { "error": "question_not_found" }
  403 { "error": "question_not_published" }  -- kecuali role curriculum_developer/reviewer/admin, sama pola seperti GET /questions/{id}
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

### `POST /lessons/{id}/attempts` (P3-004)
Sama pola persis seperti `POST /assessments/{id}/attempts` di atas, untuk lesson `type: "writing"` — tapi tidak ada "questions" yang dibalikin (prompt-nya cuma konten lesson itu sendiri, yang learner sudah baca di lesson viewer).
```
Response 201: { "attempt_id": "uuid", "status": "in_progress" }
Error:
  404 { "error": "lesson_not_found" }
  422 { "error": "invalid_lesson_type", "detail": "..." }  -- lesson.type bukan "writing"
  403 { "error": "lesson_not_published" }
  409 { "error": "attempt_already_in_progress", "attempt_id": "uuid" }
```

### `POST /attempts/{attempt_id}/submit`
Body-nya bercabang tergantung jenis attempt-nya (dicek dari `assessment_id`/`lesson_id` si attempt, bukan dari bentuk body) — `answers` untuk attempt assessment, `answer_text` untuk attempt lesson/writing (P3-004).
```
Request (assessment):  { "answers": { "<question_id>": { "index": 0 }, "<question_id_2>": { "text": "..." } } }
Response 200:
  { "attempt_id": "uuid", "status": "submitted", "score": 85.0, "learning_events_created": 12 }
Error:
  409 { "error": "attempt_already_submitted" }
  422 { "error": "missing_required_answers", "missing": ["question_id_3"] }
```
```
Request (lesson/writing, P3-004): { "answer_text": "My essay text..." }
Response 200:
  { "attempt_id": "uuid", "status": "evaluated",
    "evaluation": { "id": "uuid",
      "scores": { "task_achievement": 78, "coherence_cohesion": 82, "lexical_resource": 70,
                   "grammar_accuracy": 75, "overall": 76.3 },
      "feedback": [{ "content": "...", "position": { "start": 12, "end": 34 } | null }] } }
  -- "position" is null when the AI's quoted span couldn't be located verbatim in the
  -- submitted text — the feedback comment itself is still kept, just unpositioned.
Response 200 (AI evaluation failed — provider error or unparseable output):
  { "attempt_id": "uuid", "status": "submitted", "evaluation": null }
  -- NOT an error response: the submission itself always succeeds (the text is safely
  -- turned in, same as a real exam) even when scoring fails. `status` stays "submitted"
  -- (not "evaluated") until an evaluation actually succeeds — retriable later, including
  -- via a human evaluator (evaluator_type: "human"), not just automatic retry.
Error:
  422 { "error": "empty_writing_submission" }
  422 { "error": "missing_answer_text" }  -- attempt is lesson-based but no answer_text sent
  409 { "error": "attempt_already_submitted" }
```

---

## Learning Engine

### `GET /mastery/{concept_id}`
```
Response 200: { "concept_id": "uuid", "score": 72, "confidence": 0.6, "last_reviewed_at": "iso8601" }
Error: 200 { "concept_id": "uuid", "score": null, "confidence": 0, "message": "insufficient_data" }
```

### `GET /concepts/{concept_id}/mastery-breakdown`
P4-001 (roadmap §3.1) — 2-level drill-down over the concept containment
tree (ADR-0007, `parent_concept_id`), each node annotated with the
caller's own mastery. `weak` is only ever `true` when the node has a
scored, confident mastery record below `WEAKNESS_SCORE_THRESHOLD`
(default 60) — a node with no data yet or below-threshold confidence
reports `insufficient_data` instead and is never flagged weak (no
signal to call "weak" yet, distinct from "confirmed weak").
```
Response 200:
  { "concept_id": "uuid", "name": "Grammar", "score": 71, "confidence": 1.0, "weak": false,
    "children": [
      { "concept_id": "uuid", "name": "Present Simple", "score": 61, "confidence": 1.0, "weak": false,
        "children": [
          { "concept_id": "uuid", "name": "Questions", "score": 49, "confidence": 1.0, "weak": true,
            "children": [] } ] } ] }
Node with no/low-confidence mastery: { "concept_id": "uuid", "name": "...", "score": null,
  "confidence": 0, "weak": false, "message": "insufficient_data", "children": [...] }
Error: 404 { "error": "concept_not_found" }
```

### `GET /review-queue?limit=10`
```
Response 200:
  { "items": [
      { "concept_id": "uuid", "concept_name": "present_simple", "due_at": "iso8601",
        "suggested_question_ids": ["uuid"] } ] }
```

### `GET /learning-queue?limit=10`
P4-002 (roadmap §3.6) — a "queue gabungan sederhana" merging `/review-queue`'s
FRSS-due concepts with confident-but-weak concepts (below
`WEAKNESS_SCORE_THRESHOLD`, same rule P4-001 uses) that aren't due yet, into
one prioritized list. Same `limit`/cap semantics as `/review-queue`
(`REVIEW_QUEUE_DEFAULT_LIMIT`, no separate config). `priority`: `critical`
(due AND weak) > `due` (due, not confidently weak) > `weak` (weak, not due
yet) — sorted in that bucket order, soonest-due-first within `critical`/`due`,
weakest-score-first within `weak`. `due_at` only present when the concept is
actually due; `score` only present when a weak-signal contributed the item.
A concept that's neither due nor confidently weak doesn't appear at all.
```
Response 200:
  { "items": [
      { "concept_id": "uuid", "concept_name": "Present Simple Questions", "priority": "critical",
        "due_at": "iso8601", "score": 30, "suggested_question_ids": ["uuid"] },
      { "concept_id": "uuid", "concept_name": "Past Simple", "priority": "due",
        "due_at": "iso8601", "suggested_question_ids": ["uuid"] },
      { "concept_id": "uuid", "concept_name": "Articles", "priority": "weak",
        "score": 42, "suggested_question_ids": ["uuid"] } ] }
```

---

## Assets & Drive (file/media management)

Drive-style file management on top of P1-010/P2-010's asset upload — folders,
per-user/role sharing (Viewer/Editor), ownership + activity trail, trash. See
`service/drive_permissions.rs` for the access model: `platform_admin` or the
resource's owner always has Editor; otherwise the highest permission found
across `resource_shares` rows matching the resource itself, its ancestor
folders (a folder share cascades to everything inside it), the caller's user
id, or the caller's role. Sharing/trash-restore/permanent-delete are
owner/platform_admin-only — an Editor share doesn't grant re-sharing rights.
Every mutation writes one `resource_activity` row (`create`, `upload`,
`rename`, `move`, `delete`, `restore`, `share`, `unshare`).

`GET /assets`/`GET /assets/{id}`/`GET /drive*` all re-sign each asset's `url`
fresh on every read (`storage.signed_url`, a local HMAC — no network call) —
the value stored at upload time has a TTL (1h private / 7d public) and would
go stale otherwise. **This is why ALM content embeds `asset://<id>`, never a
raw URL** — `block_schema.rs` rejects anything else in `data.asset`.

### `POST /assets/upload`
```
Request: multipart/form-data (file, folder_id? — which folder to upload into, root if absent)
Response 201: { "id": "uuid", "url": "https://r2.../signed-url", "type": "audio/mpeg", "filename": "clip.mp3" | null }
Error: 413 { "error": "file_too_large" }
```
Always writes `visibility: "private"` — no visibility choice on this endpoint (P1-010 predates P2-010). `filename` is captured from the multipart field's own filename.

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
Request: { "asset_id": "uuid", "content_type": "image/png", "visibility": "public", "filename": "diagram.png"?, "folder_id": "uuid"? }
Response 201: { "id": "uuid", "url": "https://r2.../signed-url", "type": "image/png", "filename": "diagram.png" | null }
Error: 422 { "error": "asset_not_uploaded", "detail": "..." }   -- no object found at this key yet (HEAD check failed)
422 { "error": "invalid_visibility", "detail": "..." }          -- must be "public" or "private"
```
`visibility` picks the returned signed GET URL's TTL — longer for `"public"` (`asset_public_signed_url_ttl_seconds`, default 7 days) than `"private"` (`asset_signed_url_ttl_seconds`, default 1 hour, same as `/assets/upload`).

### `GET /assets?folder_id=&type=&cursor=&limit=`, `GET /assets/{id}`
List assets at one folder level (root if `folder_id` omitted), optionally filtered by MIME `type` prefix (`"image"`, `"audio"`, ...) — used by the ALM editor's media picker. Both re-sign fresh, see above.
```
Response 200 (list): { "items": [{ "id", "url", "type", "filename", "folder_id", "owner_id", "visibility", "created_at", "updated_at" }], "next_cursor": null }
Response 200 (single): the same item shape directly.
Error: 404 { "error": "asset_not_found" }  -- doesn't exist, or exists but caller has no access
```

### `POST /assets/{id}/rename` `{ "filename": "string" }`, `POST /assets/{id}/move` `{ "folder_id": "uuid"? }`
Both require Editor access, return the updated asset (same shape as `GET /assets/{id}`).

### `DELETE /assets/{id}` (trash), `POST /assets/{id}/restore`, `DELETE /assets/{id}/permanent`
Soft-delete (Editor access), restore/permanent-delete (owner/platform_admin only — trash is scoped to its owner). `DELETE` responses are `204`.

### `GET/POST /assets/{id}/shares`, `DELETE /assets/{id}/shares/{share_id}`
```
GET  Response 200: [{ "id", "principal_type": "user"|"role", "principal_id", "permission": "viewer"|"editor" }]
POST Request: { "principal_type": "user"|"role", "principal_id": "uuid-or-role-name", "permission": "viewer"|"editor" }
     Response 201: the created share.
DELETE Response 204.
Error: 403 { "error": "owner_only" }             -- POST/DELETE, caller isn't the owner or platform_admin
422 { "error": "invalid_principal_type" | "invalid_permission" }
```
Identical shape for folders at `GET/POST /folders/{id}/shares`, `DELETE /folders/{id}/shares/{share_id}`.

### `GET /assets/{id}/activity` (and `GET /folders/{id}/activity`)
```
Response 200: [{ "id", "actor_id", "action", "detail": {...}|null, "created_at" }], newest first
```

## Folders

### `POST /folders` `{ "name": "string", "parent_folder_id": "uuid"? }`
### `POST /folders/{id}/rename` `{ "name": "string" }`, `POST /folders/{id}/move` `{ "parent_folder_id": "uuid"? }`
```
Error: 422 { "error": "invalid_move", "detail": "a folder cannot be moved into itself" | "...into its own descendant" }
```
### `DELETE /folders/{id}`, `POST /folders/{id}/restore`, `DELETE /folders/{id}/permanent`
`DELETE` cascades — every descendant folder and asset is soft-deleted (or, for `/permanent`, hard-deleted) in the same transaction, matching "trashing a folder empties it from view too".

All return/require the same shapes as the asset endpoints above (`FolderResponse`: `id`, `name`, `parent_folder_id`, `owner_id`, `created_at`, `updated_at`).

## Drive (cross-cutting views)

### `GET /drive?folder_id=&cursor=&limit=`
The main listing: folders + assets at one level (root if `folder_id` omitted), plus a `breadcrumb` (root-to-here) so the FE doesn't need a second round-trip.
```
Response 200: { "folders": [...], "assets": [...], "breadcrumb": [FolderResponse, ...], "next_cursor": null }
Error: 404 { "error": "folder_not_found" }  -- doesn't exist, or caller has no access to it
```

### `GET /drive/trash?cursor=&limit=`
Same shape, the caller's own trashed folders/assets only (no sharing concept for trash).

### `GET /drive/shared-with-me`
Same shape (no pagination — expected to stay small), everything shared directly with the caller's user id or role, any folder depth, flat (not a tree walk from here).

### `GET /drive/share-candidates?query=&limit=`
```
Response 200: [{ "user_id": "uuid", "name": "string" }]
```
Who the share dialog can offer — members of the caller's own organization, optionally filtered by name. **Deliberately not `GET /organizations/{id}/members`** — that endpoint is gated to org_owner/academic_director (ADR-0006), which would 403 exactly the curriculum_developer/reviewer accounts that actually use Drive sharing day to day.

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

### `POST /ai/ocr-to-question` (P2-015, built in titian-backend-bun)
Auth: curriculum_developer+ (same gate as `POST /question-banks/{id}/questions`). 0 credit charged.
`asset_id` references an existing Drive asset (`POST /assets/upload`/`confirm`) — a photographed or
scanned page of exam/exercise questions; **images only for v1**, PDF input deferred as a follow-up.
Real Drive permission check on `asset_id` (same as `GET /assets/{id}`), not a bypass.

Every extracted question is created as `status: "draft"` — **never auto-published**
(ALR_Phase_Detail_Breakdown.md 2.6: an OCR misread on a real exam can be fatal). Nothing is silently
dropped: an item the model can't confidently classify still lands as a draft with `type: "unknown"`
rather than being forced into `mcq`/`fill_blank` or discarded. **Every** created question — confidently
classified or not — carries an `ocr_verification` entry in `qa_report.issues` telling a reviewer to
check it against the source image before it goes through the normal submit-review → publish flow
(P2-005); an item that couldn't be validated against its claimed type also gets an `ocr_uncertain_type`
entry. `qa_report` additionally carries `ocr_raw_text` — the model's raw reading of that question, for
comparison against the source image.
```
Request: { "bank_id": "uuid", "asset_id": "uuid", "concept_ids": ["uuid"] }
  -- concept_ids optional, default []; applied to every question extracted from the page
Response 201: { "ai_task_id": "uuid", "status": "done", "question_ids": ["uuid", ...] }
  -- all created questions are always "draft"; question_ids may include type="unknown" entries
Error:
  422 { "error": "ai_output_validation_failed" }  -- provider call failed, or output wasn't a JSON array
  404 { "error": "asset_not_found" }               -- asset doesn't exist, or caller has no Drive access to it
  403 { "error": "forbidden" }
```

---

## Health

### `GET /health`
```
Response 200: { "status": "ok", "db": "ok", "redis": "ok" }
```
