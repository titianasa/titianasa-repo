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

### `GET /me/xp`
P8-001 (roadmap-Fase-6 §6.1/§6.2) — XP, deliberately separate from Mastery
(real ability) and Credits (economy): never used as a proxy for skill, never
fed into `mastery.compute`/`frss.apply`. Awarded automatically on every
learning submission (`POST /questions/{id}/check`, `POST /attempts/{id}/submit`
— assessment, level_assessment, lesson writing, lesson speaking); amount
depends on the question's `skill_category` (P7-002) or the assessment's
`type`. Default amounts (documented in source as tunable, not final):
vocabulary 5, grammar/reading/listening 10, speaking/pronunciation 15,
writing 20, untagged question 5, `unit_test` 20, `mock_exam`/`level_assessment` 30.
```
Response 200:
  { "total": 145, "recent": [{ "amount": 10, "reason": "question_answered",
      "created_at": "iso8601" }] }
```

### `GET /me/streak`
P8-002 (roadmap-Fase-6 §6.5) — non-punitive by design. Updated on the same
5 submission points as `GET /me/xp` above (1 activity per calendar day, UTC).
A gap of 1+ days is absorbed by `freezes_available` if one is available
(`current_streak` stays exactly where it was, doesn't increment or reset) —
without one, `current_streak` resets to 1, not 0 (today's activity still
counts). A new freeze is earned every 7-day streak milestone reached by
consecutive activity (not by using a freeze). A user with no activity yet
gets zeroed defaults, not a 404.
```
Response 200: { "current_streak": 4, "longest_streak": 12, "freezes_available": 1 }
```

### `GET /me/achievements`
P8-003 (roadmap-Fase-6 §6.7) — 3 categories, checked on the same 5 submission
points as `GET /me/xp`/`GET /me/streak`. Only earned achievements are
returned (no "locked" placeholders/progress-toward-next in this version).
`Learning`: First Lesson (first-ever XP-earning activity), 7-Day/30-Day
Streak. `Skill`: Speaking Star / Listening Master / Reading Explorer /
Writing Builder — cumulative XP tagged to that `skill_category` crosses a
threshold. `Improvement`: Improver / Weakness Destroyer / Master of Growth —
a concept's `masteries.score` grows 10/20/40+ points versus the first score
ever observed for that (user, concept) pair (a fixed baseline, not a moving
window). A user with no activity yet gets an empty list, not a 404.
```
Response 200:
  { "items": [{ "code": "first_lesson", "name": "First Lesson",
      "description": "Completed your first learning activity.",
      "category": "learning", "earned_at": "iso8601" }] }
```

### `GET /me/daily-mission`
P8-004 (roadmap-Fase-6 §6.8) — a fixed daily quest, deliberately NOT
personalized from weakness detection (that's `GET /learning-queue`, P4-002 —
a different mechanism). Updated on the same 5 submission points as the other
`GET /me/*` gamification endpoints; only `vocabulary`/`grammar`/`listening`/
`speaking` count toward it (matching §6.8's own example — `reading`/
`writing`/`pronunciation` don't). 1 row per calendar day (UTC) — resets
automatically the next day. All 4 targets met awards +80 XP exactly once
(`reason: "daily_mission_completed"`); progress still accumulates past a
met target, it just no longer re-triggers the reward. A user with no
activity yet today gets zeroed progress, not a 404.
```
Response 200:
  { "date": "2026-09-02",
    "progress": { "vocabulary": 3, "grammar": 1, "listening": 0, "speaking": 1 },
    "target": { "vocabulary": 5, "grammar": 1, "listening": 1, "speaking": 1 },
    "reward_claimed": false }
```

### `GET /leaderboard/weekly?limit=20`
P8-005 (roadmap-Fase-6 §6.3, scope narrowed to Weekly + Personal only —
Country/Region/Friends/Class/Course need a user profile field and social-
graph/enrollment entities that don't exist yet, roadmap-Fase-8 unbuilt).
`items`: top `limit` users by `xp_events.amount` summed over the last 7
days, ranked descending — a user with 0 XP this week simply never appears
(not a synthetic 0-XP row). `me`: the CALLER's own standing computed from
the same full ranking (not a second query), even when outside `items` —
`null` if the caller had no XP this week. `percentile` reads as "you're
better than X% of other users this week" (denominator excludes the caller;
the sole ranked user this week reads as 100).
```
Response 200:
  { "items": [{ "user_id": "uuid", "name": "Sani", "xp": 145, "rank": 1 }],
    "me": { "xp": 60, "rank": 4, "percentile": 72 } | null }
```

### `GET /me/league`
P8-005 (roadmap-Fase-6 §6.4) — tier is a WEIGHTED FORMULA, never raw XP
(§6.4's own requirement: "bukan cuma XP, supaya tidak bisa dibeli"). Inputs,
each capped and rescaled to 0-100 before averaging: `current_streak` (capped
at 30 days), average `masteries.score` across confident rows only (same
`masteryConfidenceThreshold` gate as `GET /concepts/{id}/mastery-breakdown`,
0 if no confident data), and a COUNT (not sum) of `xp_events` in the last 7
days — deliberately not XP amount, since per-event XP varies by skill.
Computed live on every call, never cached/refreshed by a job (this backend
has no scheduling infrastructure at all). Tiers: `bronze`/`silver`/`gold`/
`platinum`/`diamond`/`master`, thresholds documented as tunable defaults in
`league_service.ts`. No activity at all defaults to `bronze`.
```
Response 200:
  { "tier": "gold", "score": 54.2,
    "inputs": { "current_streak": 12, "average_mastery": 68.5, "weekly_activity_count": 22 } }
```

### `GET /organizations/{id}/members?cursor=&limit=`
Auth: role org_owner/academic_director di org tsb.
```
Response 200: { "items": [{ "user_id": "uuid", "name": "string", "role": "string" }], "next_cursor": null }
Error: 403 { "error": "forbidden" }
```

### `POST /organizations/{id}/tutors`
P9-001 (roadmap-Fase-8 §8.15 core). Auth: role org_owner/academic_director
di org tsb. Assign role `tutor` (ADR-0006, ada sejak Phase 0, baru dipakai
di sini) + buat `tutor_profiles` row dalam 1 transaksi — idempotent: assign
user yang sudah jadi tutor di org yang sama bukan error, bukan duplikat row,
cuma return profile yang sudah ada. Org platform-type = tutor marketplace-
wide; org school-type = tutor khusus sekolah itu — model org yang sama,
tidak ada konsep baru.
```
Request: { "user_id": "uuid", "bio": "string"?, "specializations": ["string"]? }
Response 201: { "user_id": "uuid", "organization_id": "uuid", "bio": "string", "specializations": ["string"] }
Error: 403 { "error": "forbidden" }
```

### `GET /organizations/{id}/tutors`
P9-001. Auth: user manapun yang login (lebih longgar dari `members:view`
di atas — sengaja, sama seperti calon murid browsing marketplace).
```
Response 200: { "items": [{ "userId": "uuid", "name": "string", "bio": "string", "specializations": ["string"] }] }
```

### `PATCH /tutors/me`
P9-001. Ownership check (bukan role-matrix) — target selalu caller sendiri.
Field yang di-omit di request = tidak diubah (PATCH semantics asli, fallback
ke value existing, bukan default kosong).
```
Request: { "bio": "string"?, "specializations": ["string"]? }
Response 200: { "user_id": "uuid", "organization_id": "uuid", "bio": "string", "specializations": ["string"] }
Error: 404 { "error": "tutor_profile_not_found" }
```

---

## Marketplace

### `POST /tutors/me/products`
P9-003 (roadmap-Fase-8 §8.3 minimal). Auth: role `tutor`. `tutor_id` selalu
dari `ctx.userId`, TIDAK PERNAH dari body — tutor tidak bisa bikin produk
atas nama tutor lain. `price_idr` dalam Rupiah mentah (bigint), BUKAN
credit — beda "dompet" dari ekonomi AI/Diamond (ADR-0005). `capacity`
wajib `null` untuk `type: "private"` (selalu 1 siswa), wajib `>0` untuk
`type: "group"` — dijaga di 2 lapis: validasi service (422 rapi) DAN
CHECK constraint DB (defense-in-depth kalau ada jalur insert lain).
Produk baru selalu `status: "draft"`.
```
Request: { "type": "private"|"group", "title": "string", "description": "string"?, "price_idr": number, "capacity": number|null? }
Response 201: { "id": "uuid", "tutor_id": "uuid", "type": "string", "title": "string", "description": "string", "price_idr": number, "capacity": number|null, "status": "draft" }
Error: 403 { "error": "forbidden" }, 422 { "error": "invalid_price"|"invalid_capacity"|"invalid_product_type", "detail": "string" }
```

### `GET /tutors/{id}/products`
P9-003. Publik (siapa saja authenticated). Cuma `status: "published"`,
KECUALI kalau caller adalah tutor pemilik produk itu sendiri — dia juga
lihat draft/archived miliknya.
```
Response 200: { "items": [{ "id": "uuid", "tutor_id": "uuid", "type": "string", "title": "string", "price_idr": number, "capacity": number|null, "status": "string" }] }
```

### `GET /products/{id}`
P9-003. Sama aturan visibilitas dengan listing di atas. Produk draft
milik orang lain balikin 404 (BUKAN 403) — caller tidak bisa bedakan
"tidak ada" dari "ada tapi belum publish".
```
Response 200: { "id": "uuid", "tutor_id": "uuid", "type": "string", "title": "string", "description": "string", "price_idr": number, "capacity": number|null, "status": "string" }
Error: 404 { "error": "learning_product_not_found" }
```

### `POST /products/{id}/cohorts`
P9-004 (roadmap-Fase-8 §8.4). Auth: HYBRID, bukan role-matrix murni —
tutor pemilik produk itu SENDIRI selalu boleh, ATAU `org_owner`/
`academic_director` dari org yang SAMA dengan `tutor_profiles.organization_id`
tutor itu (platform_admin selalu boleh). Dicek langsung di
`cohort_service.canManageCohorts`, bukan lewat `permissions.ts`'s matrix
(row-context, bukan cuma role) — pola sama `PATCH /tutors/me`'s
ownership check.
```
Request: { "name": "string", "schedule": object?, "starts_at": "ISO string"|null?, "ends_at": "ISO string"|null? }
Response 201: { "id": "uuid", "product_id": "uuid", "name": "string", "schedule": object, "starts_at": "ISO string"|null, "ends_at": "ISO string"|null }
Error: 403 { "error": "forbidden" }, 404 { "error": "learning_product_not_found" }
```

### `POST /cohorts/{id}/enrollments`
P9-004. Self-enroll SAJA — `student_id` selalu dari `ctx.userId`, tidak
ada field ini di body. BELUM terikat ke pembayaran sukses (itu P9-007) —
`status` awal selalu `pending`. Idempotent: enroll ulang oleh siswa yang
sama balikin row yang sudah ada (dicek SEBELUM gerbang kapasitas, supaya
siswa yang sudah terdaftar tidak pernah ditolak gara-gara cohort penuh
belakangan). Kapasitas: `group` pakai `learning_products.capacity`,
`private` selalu maks 1 total (bukan per-siswa).
**Keterbatasan diketahui:** gerbang kapasitas TIDAK di-lock row-level —
2 siswa berbeda yang enroll BENAR-BENAR bersamaan ke kursi terakhir bisa
race (sama seperti tiap capacity-check lain di proyek ini, belum ada
row-locking di manapun) — didokumentasikan eksplisit, bukan diklaim
aman dari race.
```
Response 201: { "id": "uuid", "cohort_id": "uuid", "student_id": "uuid", "status": "pending", "enrolled_at": "ISO string" }
Error: 404 { "error": "cohort_not_found" }, 422 { "error": "cohort_full", "detail": "string" }
```

### `GET /cohorts/{id}/students`
P9-004. 3 cabang visibilitas dari endpoint yang SAMA: tutor pemilik
cohort (atau org admin dari org yang sama, atau platform_admin) lihat
roster PENUH; siswa yang terdaftar di cohort itu lihat HANYA baris
miliknya sendiri (bukan 403, bukan daftar penuh); siapa pun yang tidak
terkait cohort itu sama sekali (bukan pengelola, bukan terdaftar) → 403.
```
Response 200: { "items": [{ "id": "uuid", "cohort_id": "uuid", "student_id": "uuid", "status": "string", "enrolled_at": "ISO string" }] }
Error: 403 { "error": "forbidden" }, 404 { "error": "cohort_not_found" }
```

### `POST /cohorts/{id}/sessions/{session_date}/attendance`
P9-005 (roadmap-Fase-8 §8.5, dipersempit ke Manual — QR/Geolocation/
Online-auto butuh infrastruktur yang belum ada, didefer eksplisit).
`session_date` di URL sebagai string `"YYYY-MM-DD"` (bukan ISO
datetime). Auth SAMA dengan `POST /products/{id}/cohorts` (dipakai
ulang `cohort_service.canManageCohorts`, bukan aturan baru) — tutor
pemilik cohort ATAU org admin dari org tutor itu ATAU platform_admin.
Upsert per `(cohort_id, student_id, session_date)` — tandai ulang
tanggal yang sama = update, bukan baris baru. Setiap `student_id` WAJIB
sudah terdaftar (enrolled) di cohort itu.
```
Request: { "records": [{ "student_id": "uuid", "status": "present"|"absent"|"late"|"excused" }] }
Response 200: { "items": [{ "id": "uuid", "cohort_id": "uuid", "student_id": "uuid", "session_date": "YYYY-MM-DD", "status": "string", "method": "manual", "marked_by": "uuid", "marked_at": "ISO string" }] }
Error: 403 { "error": "forbidden" }, 404 { "error": "cohort_not_found" }, 422 { "error": "invalid_attendance_status"|"student_not_enrolled", "detail": "string" }
```

### `GET /cohorts/{id}/attendance`
P9-005. Visibilitas SAMA dengan `GET /cohorts/{id}/students` (3 cabang):
tutor/org-admin/platform_admin lihat rekap penuh; siswa terdaftar lihat
rekap miliknya sendiri saja; siapa pun tidak terkait → 403.
```
Response 200: { "items": [{ "id": "uuid", "cohort_id": "uuid", "student_id": "uuid", "session_date": "YYYY-MM-DD", "status": "string", "method": "manual", "marked_by": "uuid", "marked_at": "ISO string" }] }
Error: 403 { "error": "forbidden" }, 404 { "error": "cohort_not_found" }
```

### `POST /cohorts/{id}/enrollments/{enrollment_id}/certificate`
P9-006 (roadmap-Fase-8 §8.8). Wording sengaja hati-hati — ini catatan
penyelesaian internal + estimasi CEFR kasar, BUKAN sertifikasi resmi
eksternal. Auth SAMA dengan cohort-management lain (`canManageCohorts`
— tutor pemilik ATAU org admin ATAU platform_admin). Syarat:
`enrollment.status = 'completed'`. `skill_summary`/`estimated_cefr`
adalah SNAPSHOT saat diterbitkan (bukan live-query saat verifikasi) —
rata-rata `masteries.score` confident-only (`config.masteryConfidenceThreshold`),
dikelompokkan per `questions.skill_category` lewat
`question_concepts`. Tanpa data mastery confident sama sekali →
`estimated_cefr: null`, `skill_summary: {}` — TIDAK PERNAH ditebak.
`completion_percent` selalu `100` (syaratnya sendiri sudah `completed`,
tidak ada tabel progress parsial buat hitung angka lebih halus). 1
sertifikat per enrollment — terbit ke-2 kali = 409, BUKAN idempotent
(beda dari pola "assign berulang = no-op" di ticket lain fase ini,
karena sertifikat itu peristiwa formal sekali-jadi dengan
timestamp+code sendiri).
```
Response 201: { "id": "uuid", "enrollment_id": "uuid", "certificate_code": "string", "issued_at": "ISO string", "completion_percent": 100, "estimated_cefr": "string"|null, "skill_summary": { "grammar": 82, "...": "..." } }
Error: 403 { "error": "forbidden" }, 404 { "error": "cohort_not_found"|"enrollment_not_found" }, 409 { "error": "certificate_already_issued" }, 422 { "error": "enrollment_not_completed", "detail": "string" }
```

### `GET /certificates/{code}/verify`
P9-006. PUBLIK, tanpa auth sama sekali. Balikin `{valid:false}` (status
200, BUKAN 404) untuk code yang tidak ketemu — endpoint verifikasi
publik tidak boleh bocorin lewat status code mana `certificate_code`
yang benar-benar exist.
```
Response 200: { "valid": true, "student_name": "string", "course_title": "string", "completion_date": "ISO string" } | { "valid": false }
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

### `GET /lessons/{id}/speaking-prompt-audio` (P6-003, ADR-0010)
The AI Tutor's authored opening line for a `speaking` lesson (a `speaking_prompt`
content block, `data: {"text": "..."}`), synthesized to audio on request via
Kokoro (`config.aiTtsModel`/`aiTtsDefaultVoice`) — **not** generated live, the
text itself is authored content like any other block. Returns raw audio bytes,
not JSON.
```
Response 200 (audio/mpeg body, raw bytes)
Error:
  404 { "error": "lesson_not_found" }
  404 { "error": "speaking_prompt_not_found" }  -- lesson has no speaking_prompt block
  403 { "error": "lesson_not_published" }  -- same rule as GET /lessons/{id}
```

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
    "qa_report": { "passed": true, "issues": [] } | null, "cefr_tag": "a1" | null,
    "skill_category": "grammar" | null }
Error: 404 { "error": "question_not_found" }
403 { "error": "question_not_published" }  -- kecuali role curriculum_developer/reviewer/admin, sama pola seperti GET /lessons/{id}
```

### `POST /question-banks/{id}/questions`
Auth: curriculum_developer+ (status hasil selalu `draft`)

`skill_category` (P7-002, roadmap-Fase-5 §5.2, ADR-0011) — opsional, salah satu
dari `vocabulary`/`grammar`/`reading`/`listening`/`writing`/`speaking`/`pronunciation`.
Dipakai P7-003's Level Assessment composite scoring buat tahu bucket
Knowledge/Communication mana soal ini masuk — tidak berpengaruh ke `unit_test`/
`mock_exam` biasa. Kosong (NULL) = belum ditag, tidak dihitung ke bucket manapun.
```
Request:
  { "type": "mcq", "difficulty": 0.4,
    "data": { "prompt": "I ___ a student.", "options": ["am","is","are"] },
    "correct_answer": { "index": 0 },
    "explanation": { "text": "..." },
    "concept_ids": ["uuid"],
    "skill_category": "grammar" }
Response 201: { "id": "uuid", "status": "draft" }
Error: 422 { "error": "invalid_question_schema", "detail": "unknown field for type=mcq" }
Error: 422 { "error": "invalid_skill_category", "detail": "skill_category must be one of: ..." }
```

### `GET /question-banks/{id}/questions?status=&cursor=&limit=`
```
Response 200: { "items": [{ "id": "uuid", "type": "mcq", "difficulty": 0.4, "status": "draft",
                             "qa_report": {...} | null, "data": { "prompt": "...", "options": [...] },
                             "skill_category": "grammar" | null }],
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
Body-nya bercabang tergantung jenis attempt-nya — `answers` untuk attempt assessment; untuk attempt lesson, dicek dari lesson-nya sendiri (`lesson.type`, bukan dari bentuk body): `answer_text` untuk `writing` (P3-004), `answer_audio_asset_id` untuk `speaking` (P6-002, ADR-0010).
```
Request (assessment):  { "answers": { "<question_id>": { "index": 0 }, "<question_id_2>": { "text": "..." } } }
Response 200:
  { "attempt_id": "uuid", "status": "submitted", "score": 85.0, "learning_events_created": 12 }
Error:
  409 { "error": "attempt_already_submitted" }
  422 { "error": "missing_required_answers", "missing": ["question_id_3"] }
```

**Level Assessment composite scoring (P7-003, roadmap-Fase-5 §5.2, ADR-0011)** — only for
`assessments.type = 'level_assessment'`; `unit_test`/`mock_exam` are unaffected, same
request/response shape as above. Each question's `answers[question_id]` shape depends on
its `skill_category` (P7-002): auto-gradable Knowledge questions (`vocabulary`/`grammar`/
`reading`/`listening`) use the normal per-type shape (`{"index": 0}` etc.); Communication
questions (`writing`/`pronunciation` use `{"text": "..."}`, `speaking` uses
`{"audio_asset_id": "uuid"}`) trigger 1 AI evaluation call PER QUESTION — reusing the same
rubric pipeline P3-004/P6-002 built, writing 1 `evaluations` row per question
(`question_id` set, unlike a lesson attempt's evaluation where it's always `NULL`).
`score = Knowledge*0.4 + Communication*0.6`; if one bucket has nothing scoreable in it, the
other bucket's score is used at 100% weight rather than losing half the score. A question
with no `skill_category` at all doesn't count toward either bucket — its id appears in the
response's `unscored_question_ids`. A Communication question whose evaluation fails
(missing/malformed answer, inaccessible asset, AI provider error, unparseable AI output) is
simply excluded from the Communication bucket's denominator — the submission never fails
because of it.
```
Response 200 (level_assessment):
  { "attempt_id": "uuid", "status": "submitted", "score": 68.0, "learning_events_created": 3,
    "unscored_question_ids": ["uuid-of-a-question-with-no-skill_category"] }
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
```
Request (lesson/speaking, P6-002): { "answer_audio_asset_id": "uuid" }
Response 200:
  { "attempt_id": "uuid", "status": "evaluated", "transcript": "I want to eat fried rice...",
    "evaluation": { "id": "uuid",
      "scores": { "grammar": 65, "vocabulary": 72, "fluency": 58, "naturalness": 60,
                   "pronunciation": 55, "overall": 62.0 },
      "feedback": [{ "content": "...", "position": { "start": 12, "end": 34 } | null }],
      "correction": "Better: \"I'd like to have fried rice.\"" | null } }
  -- Same "submission always succeeds, evaluation is a separate step" rule as writing
  -- above. `transcript` is the Whisper output the evaluation actually scored — surfaced so
  -- the learner can see what the system "heard" even if it misheard something.
  -- "pronunciation" is an ADR-0010 approximation (inferred from transcript artifacts only,
  -- no acoustic analysis) — never real phoneme/IPA-target scoring.
  -- "correction" (P6-003, §4.1) is `feedback[0]`'s content re-surfaced, only when grammar OR
  -- naturalness scores below 65 — null otherwise. Not a 2nd AI call, just a presentation pick.
Response 200 (transcription or evaluation failed):
  { "attempt_id": "uuid", "status": "submitted", "transcript": "..." | null, "evaluation": null }
  -- transcript is null only when transcription itself failed; if transcription succeeded but
  -- the text evaluation step failed, transcript is still returned.
Error:
  404 { "error": "asset_not_found" }  -- answer_audio_asset_id doesn't exist or caller can't
                                          access it; checked BEFORE the attempt is marked
                                          submitted (unlike writing's inline text, an asset
                                          reference is validated up front, not left to the
                                          "evaluation can fail gracefully" path)
  422 { "error": "missing_answer_audio_asset_id" }
  409 { "error": "attempt_already_submitted" }
```

---

## Concepts

P4-003 (roadmap §3.2) — the first HTTP surface `concepts`/`concept_prerequisites`
have ever had (concept containment via `parent_concept_id`, ADR-0007, has existed
since P2-001 but was never wired to a route either — `GET /concepts/{id}/mastery-breakdown`,
P4-001, was the first read; these are the first writes). `concept_prerequisites`
is a graph *separate* from `parent_concept_id` containment (ADR-0007's own
design) — edge `(concept_id, prerequisite_concept_id)` means "concept_id
requires prerequisite_concept_id", checked for cycles (direct or transitive)
the same way `setParent` checks containment. Auth: `curriculum:create` tier
(platform_admin/org_owner/academic_director/curriculum_developer) on all 3
routes.

### `POST /concepts/{concept_id}/prerequisites`
Idempotent — adding an edge that already exists returns 201 again, not a
conflict.
```
Request: { "prerequisite_concept_id": "uuid" }
Response 201: { "concept_id": "uuid", "prerequisite_concept_id": "uuid" }
Error:
  404 { "error": "concept_not_found" }  -- either id
  422 { "error": "concept_prerequisite_cycle" }  -- self, direct, or transitive cycle
```

### `GET /concepts/{concept_id}/prerequisites`
Direct (1-level) prerequisites only — no transitive walk, per the roadmap's
"minimal, prerequisite untuk 1 level" MVP scope.
```
Response 200: { "items": [ { "concept_id": "uuid", "name": "Verb To Be" } ] }
Error: 404 { "error": "concept_not_found" }
```

### `DELETE /concepts/{concept_id}/prerequisites/{prerequisite_concept_id}`
Removing an edge that doesn't exist is a no-op, not an error.
```
Response 204 (empty body)
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
`suggested_question_ids` (P5-001, §3.4 Retrieval Variation) avoids suggesting
the same question TYPE the caller most recently answered for that concept,
when the concept has more than 1 type registered — a concept reviewed with
`mcq` last time surfaces a `fill_blank`/`matching` question first next time,
if one exists. A concept with only 1 registered type, or no review history
yet, is unaffected (plain `ORDER BY id`).
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

`blocked_by_concept_id` (P5-002, closes the P4-003 dead-API gap) — for a
`weak`/`critical` item, if any of its direct (1-level, no recursion)
`concept_prerequisites` is itself below `WEAKNESS_SCORE_THRESHOLD` or has no
mastery data at all, that prerequisite is escalated to `critical` priority
(added to the queue if it wasn't already a candidate) and this field is set
to that prerequisite's `concept_id` — the dependent item is never hidden,
just given a correct ordering signal. Absent when the concept has no
prerequisite edge, or when its prerequisite(s) are already confidently
strong (the majority of data today, since `concept_prerequisites` is empty
outside curriculum that's explicitly wired one up).
```
Response 200:
  { "items": [
      { "concept_id": "uuid", "concept_name": "Verb To Be", "priority": "critical",
        "score": 30, "suggested_question_ids": ["uuid"] },
      { "concept_id": "uuid", "concept_name": "Present Simple Questions", "priority": "critical",
        "due_at": "iso8601", "score": 30, "blocked_by_concept_id": "uuid-of-verb-to-be",
        "suggested_question_ids": ["uuid"] },
      { "concept_id": "uuid", "concept_name": "Past Simple", "priority": "due",
        "due_at": "iso8601", "suggested_question_ids": ["uuid"] },
      { "concept_id": "uuid", "concept_name": "Articles", "priority": "weak",
        "score": 42, "suggested_question_ids": ["uuid"] } ] }
```

### `POST /assessments/{id}/exam-sessions`
P7-001 (roadmap-Fase-5 §5.1, Exam Runtime) — activates `exam_sessions`
(existed unused in the schema since ADR-0001). Composes the existing
`POST /assessments/{id}/attempts` (same permission, same in-progress
dedup — a 2nd call while one session is already in progress gets the
same `409 attempt_already_in_progress` that endpoint already returns)
with timer bookkeeping: `duration_minutes` inside `assessments.config`
(absent = untimed, `deadline: null`). Submitting via the normal
`POST /attempts/{attempt_id}/submit` after the deadline is still
accepted and graded exactly as answered (auto-submit-on-timeout, not a
rejection) — only `exam_sessions.status` reflects `timed_out` instead
of `submitted`.
```
Response 201:
  { "exam_session_id": "uuid", "attempt_id": "uuid", "status": "in_progress",
    "deadline": "iso8601 | null",
    "questions": [ { "id": "uuid", "type": "mcq", "data": {} } ] }
Error: 404 { "error": "assessment_not_found" }
Error: 409 { "error": "attempt_already_in_progress", "attempt_id": "uuid" }
```

### `GET /exam-sessions/{id}`
Ownership-only read (ADR-0006 "milik sendiri" pattern, no separate
permission tier) — `deadline` recomputed from `started_at` +
`assessments.config.duration_minutes` the same way the POST above does.
```
Response 200:
  { "id": "uuid", "assessment_id": "uuid", "status": "in_progress",
    "started_at": "iso8601", "submitted_at": "iso8601 | null",
    "deadline": "iso8601 | null" }
Error: 403 { "error": "forbidden" }
Error: 404 { "error": "exam_session_not_found" }
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
