# ALR API Contract v1
Base URL: `/api/v1`. Auth: `Authorization: Bearer <jwt>` kecuali disebutkan lain.

> **Backend sedang dimigrasi dari Rust ke Go (ADR-0020).** Kontrak di dokumen ini berlaku sama untuk kedua backend; port tidak boleh mengubahnya. Rujukan berkas sumber Rust (`services/x.rs`, `cargo run --bin …`) berpadanan dengan `titian-backend-go` menurut tabel di `tickets/phase-51-go-migration.md`. Dua beda bentuk yang diterima di Go, keduanya tetap sah menurut aturan di bawah: angka pecahan bulat ditulis `1` (bukan `1.0`), dan pecahan detik pada timestamp tanpa nol di belakang. Method yang salah pada path yang ada dijawab `405 {"error":"method_not_allowed"}` (Rust: 405 tanpa body).

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
Response 200: { "items": [{ "user_id": "uuid", "name": "string", "bio": "string", "specializations": ["string"] }] }
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

### `POST /cohorts/{id}/enrollments/{enrollment_id}/complete`
P9-008 (bukan dari §8.1-8.15 sumber asli — gap ditemukan pas menutup
Phase 9: P9-006's penerbitan sertifikat SUDAH mengecek
`enrollment.status = 'completed'` sejak awal, tapi tidak ada jalur
manapun yang PERNAH menulis nilai itu — tidak ada infrastruktur
scheduling di backend ini buat auto-complete berdasarkan
`cohorts.ends_at`. Endpoint manual ini menutupnya, pola sama attendance
manual P9-005: tidak ada otomasi, jadi manusia (tutor) yang menandai.
Auth sama `canManageCohorts` yang dipakai di semua endpoint
cohort-management lain. Idempotent kalau sudah `completed`
(no-op, balikin state saat ini) — tapi enrollment yang belum pernah
`active` (belum bayar) ditolak 422.
```
Response 200: { "id": "uuid", "cohort_id": "uuid", "student_id": "uuid", "status": "completed", "enrolled_at": "ISO string" }
Error: 403 { "error": "forbidden" }, 404 { "error": "cohort_not_found"|"enrollment_not_found" }, 422 { "error": "enrollment_not_active", "detail": "string" }
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

### `POST /enrollments/{id}/checkout`
P9-007 (roadmap-Fase-8 §8.12+§8.13+§8.14). Auth: HANYA siswa yang
enrollment itu miliknya (`ctx.userId === enrollment.studentId`) — bukan
role-matrix, "milik sendiri" murni, sama pola `enrollSelf`. `amount_idr`
selalu dari `learning_products.price_idr` (server-side), TIDAK PERNAH
dari body. 1 order per enrollment (UNIQUE) — checkout ke-2 kali = 409,
bukan retry.
```
Response 201: { "id": "uuid", "enrollment_id": "uuid", "amount_idr": number, "status": "pending", "payment_id": "string", "qris_payload": "string" }
Error: 403 { "error": "forbidden" }, 404 { "error": "enrollment_not_found" }, 409 { "error": "order_already_exists" }
```

### `POST /payments/{payment_id}/webhook`
P9-007. **PUBLIK, tanpa auth sama sekali** — simulasi callback yang
biasanya dikirim provider asli (mode stub: dipanggil manual test/dev).
Provider asli akan diverifikasi lewat signature khusus provider itu,
bukan bearer token user — signature itu belum ada buat diverifikasi
karena belum ada provider asli (keputusan scope eksplisit, lihat
`docs/tickets/phase-9.md`). Idempotent: order yang statusnya sudah
bukan `pending` (sudah `paid`/dst) balikin state saat ini apa adanya,
TIDAK insert payout ke-2 — webhook di dunia nyata bisa terkirim lebih
dari sekali. Sukses → `orders.status → paid`, `enrollments.status →
active`, split 30/70: `transactions` baru (`type: payout_earned`,
`user_id`: tutor, `amount`: 70% `amount_idr` — **Rupiah mentah, bukan
credit**) dengan fee platform 30% dicatat di `reference` baris yang
sama (bukan baris ledger ke-2 — platform tidak punya `users` row
sendiri).
```
Response 200: { "id": "uuid", "enrollment_id": "uuid", "amount_idr": number, "status": "paid", "payment_id": "string" }
Error: 404 { "error": "order_not_found" }
```

### `POST /enrollments/{id}/cancel`
P9-007. Auth sama `checkout` — siswa pemilik enrollment itu sendiri.
Kebijakan refund §8.14 (default tunable dari sumber, bukan kebijakan
final yang direview legal): >24 jam sebelum `cohorts.starts_at` → 100%
refund; 6-24 jam → 50%; <6 jam → 0% (tidak ada refund, tapi enrollment
tetap `cancelled`). `cohorts.starts_at` kosong (belum dijadwalkan) →
default 100% refund. Refund → `transactions` baru (`type: refund`) ke
SISWA, `orders.status → refunded` — HANYA kalau ada uang benar-benar
dikembalikan (tingkat 0% tidak mengubah `orders.status`, tetap `paid`).
**TIDAK reverse `payout_earned` tutor** kalau webhook sudah jalan
sebelumnya — kompleksitas clawback eksplisit di luar scope ticket ini,
dicatat sebagai keterbatasan, bukan lupa.
```
Response 200: { "enrollment_id": "uuid", "status": "cancelled", "refund_amount_idr": number }
Error: 403 { "error": "forbidden" }, 404 { "error": "enrollment_not_found" }
```

### `GET /tutors/me/wallet`
P9-007. Selalu "wallet milik sendiri" (`ctx.userId`), tanpa gerbang
role — pola sama `GET /me/xp`/`GET /me/streak`. `balance_idr` = SUM
`transactions.payout_earned` dikurangi SUM `payout_withdrawn` (`type:
payout_withdrawn` belum ada jalur penulisannya di ticket manapun —
selalu 0 untuk sekarang). Agregasi on-read, bukan kolom cache (pola
sama leaderboard P8-005).
```
Response 200: { "balance_idr": number }
```

### `GET /me/credits`
P11-002 (roadmap-Fase-6.9-16). Selalu "saldo milik sendiri" — pola sama
`GET /tutors/me/wallet`. **Baru ditambahkan** — sebelum ini, nol
endpoint pernah mengekspos cara membaca saldo `credits.balance` sendiri
walau `charge` sudah dipakai sejak ADR-0005/Phase 1 (dashboard FE
selama ini menampilkan angka placeholder, bukan data asli). Men-sweep
allowance subscription yang sudah expired dulu (P11-003) sebelum
membalikkan saldo, jadi angkanya selalu akurat meski tidak ada cron job
yang jalan di background.
```
Response 200: { "balance": number }
```

### `POST /subscriptions/subscribe`
P11-002. Body `{ "tier": "plus"|"pro" }`. **Belum ada gerbang
pembayaran sungguhan** — subscribe langsung aktif (keputusan scope
eksplisit, lihat `docs/tickets/phase-11.md`). Upsert — subscribe ulang
(renewal/upgrade/downgrade) selalu mengganti tier+periode yang aktif,
bukan error. Selalu grant PERSIS 1 allowance baru sebesar tier yang
diminta (Plus 100/Pro 300, contoh angka ADR-0005 — tunable default,
bukan final bisnis) — upgrade dari Plus ke Pro TIDAK menggandakan
allowance Plus yang lama. `expires_at` allowance = akhir periode +
grace 1 bulan (ADR-0005).
```
Response 201: { "subscribed": true, "tier": "string", "status": "active", "current_period_start": "ISO string", "current_period_end": "ISO string" }
Error: 422 { "error": "invalid_tier", "detail": "string" }
```

### `GET /subscriptions/me`
P11-002. `{"subscribed": false}` (BUKAN 404) kalau belum pernah
subscribe — bukan bare `null`, konsisten pola "jangan balikin null
telanjang di top-level response" (`GET /mastery/{id}`'s `message`
field).
```
Response 200: { "subscribed": true, "tier": "string", "status": "string", "current_period_start": "ISO string", "current_period_end": "ISO string" } | { "subscribed": false }
```

### `POST /ads/watch`
P11-004 (roadmap-Fase-6.9-16 §6.10, "free tier benar-benar usable").
Simulasi "selesai nonton iklan" — `StubAdProvider` TIDAK PERNAH connect
ke ad network asli (grep `fetch`/`http` di `ad_provider.ts` → 0 hasil).
Hasilnya 1 baris `ad_views` yang bisa dikonsumsi SEKALI oleh
`POST /ai/evaluate` (task `grammar_evaluation`) sebagai pengganti
charge diamond — kalau tidak ada `ad_views` yang belum dipakai, jalur
charge diamond biasa tetap berlaku (0 perubahan perilaku default).
```
Response 201: { "view_id": "string" }
```

### `POST /cohorts/{id}/enrollments/{enrollment_id}/tutor-cancel`
P12-004 (roadmap-Fase-8 §8.14, separuh yang belum ada sampai Phase 12).
Auth `canManageCohorts` (bukan siswa) — beda arah dari `POST
/enrollments/{id}/cancel`. Kebijakan beda total: SELALU 100% refund
(tidak ada tingkat waktu seperti cancel siswa, karena siswa tidak
salah). `enrollments.cancelled_by = 'tutor'` (beda dari cancel siswa
yang `'student'`) — dipakai `GET /tutors/{id}/reputation`'s
`cancellation_rate` supaya tidak tercampur pembatalan siswa sendiri.
**TIDAK reverse `payout_earned` tutor** — sama keterbatasan eksplisit
`POST /enrollments/{id}/cancel`.
```
Response 200: { "enrollment_id": "uuid", "status": "cancelled", "cancelled_by": "tutor", "refund_amount_idr": number }
Error: 403 { "error": "forbidden" }, 404 { "error": "enrollment_not_found" }
```

### `POST /cohorts/{id}/assignments`, `GET /cohorts/{id}/assignments`
P12-002 (roadmap-Fase-8 §8.6, MVP: manual grading, AI eval didefer
eksplisit — lihat `docs/tickets/phase-12.md`). POST: auth
`canManageCohorts`. GET: tutor/org-admin lihat semua assignment cohort
itu; siswa yang terenroll lihat daftar assignment cohort itu (gerbang
lebih longgar dari manage, tapi tetap butuh keterkaitan ke cohort).
```
Request (POST): { "title": "string", "description": "string"?, "deadline": "ISO string"|null? }
Response 201 (POST): { "id": "uuid", "cohort_id": "uuid", "title": "string", "description": "string", "deadline": "ISO string"|null }
Response 200 (GET): { "items": [{ "id": "uuid", "cohort_id": "uuid", "title": "string", "description": "string", "deadline": "ISO string"|null }] }
Error: 403 { "error": "forbidden" }, 404 { "error": "cohort_not_found" }
```

### `POST /assignments/{id}/submissions`
P12-002. Auth: siswa terenroll di cohort assignment itu. Upsert-sampai-
digrade: submit ulang SEBELUM `graded_at` terisi mengganti `content`+
`submitted_at` (bukan baris baru); submit setelah sudah digrade → 409
`submission_already_graded` (nilai yang sudah keluar tidak bisa diubah
diam-diam lewat submit ulang). `late` dihitung on-read
(`submitted_at > deadline`), BUKAN kolom tersimpan — submit setelah
deadline tetap diterima, cuma ditandai.
```
Request: { "content": "string" }
Response 201: { "id": "uuid", "assignment_id": "uuid", "student_id": "uuid", "content": "string", "submitted_at": "ISO string", "late": boolean, "score": number|null, "feedback": "string"|null, "graded_at": "ISO string"|null }
Error: 403 { "error": "forbidden" }, 409 { "error": "submission_already_graded" }
```

### `POST /submissions/{id}/grade`
P12-002. Auth `canManageCohorts`. Set `score`+`feedback`+`graded_at`+
`graded_by`; sesudah ini `POST /assignments/{id}/submissions` untuk
siswa yang sama akan 409, bukan menimpa nilai.
```
Request: { "score": number, "feedback": "string"|null? }
Response 200: { "id": "uuid", "assignment_id": "uuid", "student_id": "uuid", "content": "string", "submitted_at": "ISO string", "late": boolean, "score": number, "feedback": "string"|null, "graded_at": "ISO string" }
Error: 403 { "error": "forbidden" }, 404 { "error": "submission_not_found" }
```

### `GET /cohorts/{id}/gradebook`
P12-003 (roadmap-Fase-8 §8.7). Auth `canManageCohorts` — rekap PENUH
tutor-facing, bukan pola "siswa lihat baris sendiri" seperti
`GET /cohorts/{id}/students`. Roster = enrollment `active`/`completed`
SAJA (`pending`/`cancelled` tidak muncul sama sekali, bukan baris
bernilai 0). `assignment_average`/`overall` null-aware: siswa yang
belum pernah digrade → `assignment_average: null` (bukan 0), `overall`
dihitung dari komponen yang ADA saja. Sengaja TIDAK menyentuh mastery
engine (`masteries`) — nilai akademik dan mastery mengukur hal beda
(keputusan eksplisit sumber dokumen).
```
Response 200: { "items": [{ "student_id": "uuid", "attendance_percent": number|null, "assignment_average": number|null, "overall": number|null }] }
Error: 403 { "error": "forbidden" }, 404 { "error": "cohort_not_found" }
```

### `POST /tutors/{id}/reviews`
P12-004 (roadmap-Fase-8 §8.9, minus response-time — butuh sistem
messaging yang tidak ada, didefer eksplisit). Auth: siswa yang
`enrollment_id` di body miliknya sendiri DAN `status = completed` (cegah
review sebelum benar-benar selesai belajar). 1x per enrollment — review
ulang untuk enrollment yang sama → 409 `already_reviewed` (BUKAN
update; beda dari assignment submission yang boleh diedit sebelum
digrade, karena rating publik orang lain bergantung padanya begitu
terbit).
```
Request: { "enrollment_id": "uuid", "rating": number, "comment": "string"|null? }
Response 201: { "id": "uuid", "tutor_id": "uuid", "student_id": "uuid", "enrollment_id": "uuid", "rating": number, "comment": "string"|null, "created_at": "ISO string" }
Error: 403 { "error": "forbidden" }, 409 { "error": "already_reviewed" }, 422 { "error": "invalid_rating"|"enrollment_not_completed", "detail": "string" }
```

### `GET /tutors/{id}/reputation`
P12-004. Publik (siapa saja authenticated), pola sama
`GET /tutors/{id}/products` — tidak ada gerbang kepemilikan. Semua
angka dihitung on-read dari `enrollments`/`attendance_records`/
`tutor_reviews`, tidak ada tabel agregat cache. `completion_rate`
denominator = `completed+cancelled` saja (enrollment yang belum
resolve tidak dihitung, supaya tidak understate). `cancellation_rate`
numerator HANYA `cancelled_by = 'tutor'` (P12-001), denominator SEMUA
enrollment tutor itu — tidak tercampur pembatalan siswa sendiri.
```
Response 200: { "average_rating": number|null, "review_count": number, "student_count": number, "lesson_count": number, "completion_rate": number|null, "cancellation_rate": number|null }
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

## Proctoring

P13-001..005 (roadmap-Fase-9, the LAST of 4 roadmap-Fase requested in
sequence). Activates `proctoring_policies`/`proctoring_sessions`/
`proctoring_events`, unused in the schema since ADR-0001. "Risk Engine
gives a score, never a decision" — `risk_score` is read-only and never
writes `review_status`; only `POST /proctoring-sessions/{id}/review`
(a human) ever does.

### `POST /proctoring-policies`
P13-001. Role `platform_admin`/`org_owner`/`academic_director` (`proctoring_policy:create`,
same tier as `tutor_profile:create`).
```
Request: { "exam_type": "string", "camera": "off"|"optional"|"on"?, "microphone": "off"|"optional"|"on"?, "screen": "off"|"optional"|"on"?, "fullscreen_required": boolean?, "focus_monitoring": boolean?, "retention_days": number? }
Response 201: { "id": "uuid", "exam_type": "string", "camera": "string", "microphone": "string", "screen": "string", "fullscreen_required": boolean, "focus_monitoring": boolean, "retention_days": number }
Error: 403 { "error": "forbidden" }, 422 { "error": "invalid_camera_level"|"invalid_microphone_level"|"invalid_screen_level"|"invalid_retention_days", "detail": "string" }
```

### `GET /proctoring-policies`
P13-001. Any authenticated user (config read-only, pola sama `GET /curricula`).
```
Response 200: { "items": [{ "id": "uuid", "exam_type": "string", "camera": "string", "microphone": "string", "screen": "string", "fullscreen_required": boolean, "focus_monitoring": boolean, "retention_days": number }] }
```

### `POST /exam-sessions/{id}/proctoring-session`
P13-001. Auth "milik sendiri" (`exam_session.user_id === ctx.userId`).
**Consent-first, non-negotiable**: `consent !== true` → 422
`consent_required`, and the session is NEVER inserted — there is no
"created but unconsented" row to ever clean up, because that state
can't exist.
```
Request: { "policy_id": "uuid", "consent": boolean, "device_info": object? }
Response 201: { "id": "uuid", "exam_session_id": "uuid", "policy_id": "uuid", "consent_given_at": "ISO string", "review_status": "pending" }
Error: 403 { "error": "forbidden" }, 404 { "error": "exam_session_not_found"|"proctoring_policy_not_found" }, 422 { "error": "consent_required", "detail": "string" }
```

### `POST /proctoring-sessions/{id}/events`
P13-002. Auth "milik sendiri" (via `proctoring_session -> exam_session.user_id`).
The client reports something it already detected — this endpoint never
performs detection itself. `evidence_id`, if given, must be an asset
the reporting student actually owns (already uploaded via the existing
`POST /assets`, no new upload mechanism).
```
Request: { "type": "string", "severity": "low"|"medium"|"high", "metadata": object?, "evidence_id": "uuid"|null? }
Response 201: { "id": "uuid", "proctoring_session_id": "uuid", "type": "string", "severity": "string", "timestamp": "ISO string", "evidence_id": "uuid"|null }
Error: 403 { "error": "forbidden" }, 422 { "error": "invalid_severity"|"invalid_evidence", "detail": "string" }
```

### `GET /proctoring-sessions/{id}`
P13-002/003/004/005. Branches on caller: the owning student sees a
LIMITED view (consent/policy/review status only — never the raw event
list or `risk_score`, a deliberate privacy-by-design choice so a
student can't learn exactly what triggers detection and route around
it next time); staff with `proctoring_session:review` permission
(`platform_admin`/`org_owner`/`academic_director`) see the FULL human-review
packet. A lazy retention sweep (P13-005, no scheduler exists in this
backend) runs at the top of every call in both branches, before events
are read.
```
Response 200 (owner): { "id": "uuid", "exam_session_id": "uuid", "policy_id": "uuid", "consent_given_at": "ISO string", "review_status": "string", "reviewed_at": "ISO string"|null }
Response 200 (staff): { "id": "uuid", "exam_session_id": "uuid", "policy_id": "uuid", "consent_given_at": "ISO string", "review_status": "string", "reviewed_by": "uuid"|null, "reviewed_at": "ISO string"|null, "review_notes": "string"|null, "risk_score": number, "events": [{ "id": "uuid", "type": "string", "severity": "string", "timestamp": "ISO string", "metadata": object, "evidence_id": "uuid"|null }] }
Error: 403 { "error": "forbidden" }, 404 { "error": "proctoring_session_not_found" }
```

### `POST /proctoring-sessions/{id}/review`
P13-004. `requirePermission(ctx, "proctoring_session", "review")` —
`platform_admin`/`org_owner`/`academic_director` only (the ADR-0006 matrix's
`teacher/tutor` "kelas sendiri" cell needs an exam_session<->cohort
linkage that doesn't exist yet, deferred explicitly — see
`docs/tickets/phase-13.md`). The ONLY endpoint that ever moves
`review_status` away from `pending` — `risk_score` never does.
`decision` must be a real outcome (`pending` itself is rejected, a
human must actually decide). Re-review is ALLOWED (overwrites the
previous decision) — deliberately different from `tutor_reviews`'s
409-on-repeat (P12-004): this is an internal moderation call that may
need correction, not a public rating.
```
Request: { "decision": "cleared"|"flagged"|"violation_confirmed", "notes": "string"|null? }
Response 200: { "id": "uuid", "exam_session_id": "uuid", "policy_id": "uuid", "consent_given_at": "ISO string", "review_status": "string" }
Error: 403 { "error": "forbidden" }, 404 { "error": "proctoring_session_not_found" }, 422 { "error": "invalid_decision", "detail": "string" }
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
**P11-004 update**: kalau caller punya `ad_views` row yang belum
dipakai (`POST /ads/watch`), dikonsumsi sebagai pengganti charge
diamond — `credit_charged: 0` di response, TIDAK menyentuh
`credits.balance` sama sekali. Tanpa `ad_views`, perilaku sama persis
seperti sebelum P11-004 (charge diamond seperti biasa).
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

## Grup Belajar (P45, ADR-0015)

Semua endpoint butuh login. Kuota, kapasitas, dan izin **diputuskan server** (`subscription::group_limits`,
`group_capacity`, peran per-grup di `study_group_members`); klien tidak dipercaya. Grup Global
(`id 00000000-0000-0000-0000-00000000c0de`, `kind:"global"`) berisi semua pengguna secara implisit: tidak ada
baris anggota, tidak menghabiskan kuota join, tidak bisa di-join/keluar/diubah (`422 global_group_implicit`).

Bentuk grup (`GroupResponse`):
```
{ id, kind: "belajar"|"kelas"|"global", name, description, avatar_emoji, jenjang, subject,
  visibility: "public"|"private", join_mode: "open"|"approval", owner_id, cohort_id,
  max_members, status: "active"|"archived"|"suspended", created_at, member_count,
  my_role: "owner"|"admin"|"member"|null, my_status: "active"|"pending"|"left"|"removed"|"banned"|null }
```
Kapasitas mengikuti **jenis** grup: `belajar` 100, `kelas` 1000 (bukan tier pemilik).
Grup privat yang bukan milik pemanggil → **404** (bukan 403) supaya keberadaannya tidak bocor; grup terarsip hanya terlihat oleh anggotanya.

Kuota per tier (`GET /me/entitlements` → blok `groups`):

| | gratis | Plus | Pro |
|---|---|---|---|
| `max_groups_joined` | 3 | 1000 | 1000 |
| `max_groups_created` | 0 | 50 | 100 |
| `max_active_leagues_per_group` | 0 | 3 | null (tak terbatas) |
| `can_create_classroom` / `can_convert_to_class_group` / `can_use_circuits` / `can_monetize` | false | false | true |

### `POST /groups`  (Plus/Pro)
```
Request: { "name": "1-80", "description"?: "<=500", "avatar_emoji"?, "jenjang"?, "subject"?,
           "visibility"?: "private"(default)|"public", "join_mode"?: "open"(default)|"approval" }
Response 201: GroupResponse    -- pembuat otomatis owner; grup privat langsung dibuatkan 1 kode undangan
Error: 403 group_creation_requires_plus | group_create_quota_reached | group_join_quota_reached
       422 invalid_group_name | invalid_visibility | invalid_join_mode | invalid_group_description
```
### `GET /me/groups`
```
Response 200: { "items": [GroupResponse],  -- Grup Global selalu pertama
                "quota": { "tier", "joined", "max_joined", "created", "max_created" } }
```
### `GET /groups/explore?q=&jenjang=&subject=&cursor=&limit=`
Hanya grup `public` + `active`, terbaru dulu, keyset `(created_at, id)`. `limit` 1-50 (default 20).
```
Response 200: { "items": [GroupResponse], "next_cursor": "..."|null }
```
### `GET /groups/{id}` · `PATCH /groups/{id}` (owner/admin) · `DELETE /groups/{id}` (owner, mengarsipkan; 204)
`PATCH` menerima subset field `POST /groups`.
### `POST /groups/{id}/join`
Grup publik saja (privat → 404). `join_mode:"approval"` menghasilkan `status:"pending"` (tidak memakai slot join/kapasitas sampai disetujui).
```
Response 200: { "group_id", "status": "active"|"pending", "already_member": bool }   -- idempoten
Error: 403 group_join_quota_reached | group_banned   409 group_full
       422 global_group_implicit | class_group_join_unavailable   404 group_not_found
```
### `POST /groups/join-by-code`  (dibatasi laju: 10/menit/pengguna → 429 `group_join_rate_limited`)
```
Request: { "code": "XXXXX-XXXXX" }   -- huruf besar/kecil, tanda hubung/spasi diabaikan
Response 200: sama dengan /join     -- kode = pre-approved, boleh masuk grup privat; join ulang tidak memakai 1 pemakaian lagi
Error: 404 invite_not_found   422 invite_expired | invite_revoked | invite_exhausted   + error /join
```
### `POST /groups/{id}/leave`  (204)
Owner → `422 owner_must_transfer`. Permintaan `pending` yang ditarik dihapus.
### Kode undangan (owner/admin)
```
POST   /groups/{id}/invites  { "expires_in_days"?: 1-365, "max_uses"?: 1-10000 } -> 201 { id, code, expires_at, max_uses, use_count, revoked_at, created_at, usable }
GET    /groups/{id}/invites  -> [invite]
DELETE /groups/{id}/invites/{invite_id}  -> 204   (dicatat di audit log)
```
Kode 10 karakter acak kriptografis, alfabet tanpa `0/O/1/I/L`.
### Anggota
```
GET    /groups/{id}/members?status=active|pending|left|removed|banned&cursor=&limit=   -- active: semua anggota; selain itu: owner/admin
         -> { items: [{ user_id, name, avatar_url, role, status, joined_at }], next_cursor }
PATCH  /groups/{id}/members/{user_id}        { "role": "admin"|"member" }   -- owner saja
DELETE /groups/{id}/members/{user_id}                                        -- keluarkan (status removed; boleh bergabung lagi)
POST   /groups/{id}/members/{user_id}/ban | /unban                          -- ban: tidak bisa bergabung lagi
POST   /groups/{id}/members/{user_id}/approve | /reject                     -- antrean pending; approve mengecek ulang kuota & kapasitas
POST   /groups/{id}/transfer-ownership       { "user_id" }                  -- pemilik lama jadi admin
```
Aturan: owner tak tersentuh; admin hanya bisa bertindak pada `member`; tidak ada yang bisa menargetkan dirinya sendiri (`422 cannot_target_self`).
Pemilik baru harus bisa membuat grup (`403 new_owner_requires_plus | new_owner_quota_reached`).
Setiap aksi moderasi dicatat di `admin_audit_log` (`target_type:"study_group"`).

### Materi grup (P46) — referensi ke perpustakaan Titian, bukan salinan
```
GET    /groups/{id}/content                       -- anggota aktif -> [{ id, kind, ref_id, title|null, available, position, due_at, created_at }]
POST   /groups/{id}/content   { kind, ref_id, due_at? }   -- owner/admin; kind = "learning_path"|"module_item"|"assessment"
PATCH  /groups/{id}/content/{content_id}  { due_at?: iso|null, position? }   -- due_at:null menghapus tenggat, tanpa field = tidak berubah
DELETE /groups/{id}/content/{content_id}  -> 204
GET    /groups/attachable/assessments?q=  -> [{ id, title, type }]   -- daftar untuk pemilih tryout (maks 50, cari judul)
Error: 404 content_not_found (tidak ada / belum terbit / jenis salah — draf tak bisa diintip)  409 content_already_attached | group_content_limit_reached (maks 50)
       422 invalid_content_kind (mis. "question_bank" — belum didukung, lihat migrasi 0074)  403 (bukan owner/admin / bukan anggota)  422 global_group_implicit
```
`learning_path` = sebuah `modules` terbit beserta seluruh sub-modulnya; unitnya = `module_items` (`node_type='item'`) terbit di subtree itu.
Materi yang kemudian di-unpublish/dihapus tetap terdaftar dengan `available:false` dan `title:null` (grup tidak rusak; owner bisa melepasnya).
```
GET /groups/{id}/progress  -> { items: [{ content, total_units,
        aggregate: { members, completed_members, avg_pct },
        mine: { user_id, name, completed_units, total_units, pct, best_score } | null,
        members?: [ ... ]    -- HANYA owner/admin }] }
```
Sumber: `module_item_progress.completed_at` (item/path) dan `attempts` berstatus `submitted|evaluated` bukan `is_preview` (assessment; `best_score` = skor tertinggi).
Hanya anggota aktif yang dihitung (yang keluar/dikeluarkan/diblokir tidak). Butir draf tidak dihitung sebagai unit.

### Target grup (P46)
```
GET    /groups/{id}/targets   -> [{ id, title, metric, target_value, per_member, period_start, period_end,
                                    status: "upcoming"|"active"|"finished",
                                    progress: { current, goal, pct, reached, mine } }]
POST   /groups/{id}/targets   { title(1-120), metric, target_value(1-100000), per_member?, period_start, period_end }   -- owner/admin
DELETE /groups/{id}/targets/{target_id}  -> 204
```
`metric`: `items_completed` (module_item_progress.completed_at di periode), `questions_answered` (learning_events `question_answered`), `activity_days` (hari kalender WIB berbeda yang punya event belajar).
Progres **tidak disimpan**: dihitung saat dibaca dari aktivitas anggota aktif di `[period_start, period_end)`.
`per_member:false` → `current` = total grup, `goal` = target_value. `per_member:true` → `current` = anggota yang masing-masing mencapai target_value, `goal` = jumlah anggota.
Batas: periode ≤ 366 hari, `activity_days` ≤ panjang periode, maks 20 target aktif per grup (`409 group_target_limit_reached`).
Error: 422 invalid_target_title | invalid_target_metric | invalid_target_value | invalid_target_period.

### Liga grup (P47) — poin dihitung dari hasil belajar, tidak pernah dikirim klien
Semua anggota aktif grup otomatis peserta semua liga grup itu. **Tamu** (di luar grup) ikut lewat kode liga dan tidak menjadi anggota grup.
```
POST /groups/{id}/leagues   -- owner/admin
  { title(1-120), description?, format, source?, scoring?, xp_policy?, cadence, season_days?, starts_at?, ends_at?, allow_guests?, guest_cap? }
  Response 201: League { id, group_id, title, description, format, source, scoring, xp_policy, integrity:"casual", cadence, season_days,
                         allow_guests, guest_cap, share_code (HANYA owner/admin), status:"active"|"finished"|"archived",
                         current_season: { id, number, starts_at, ends_at, status:"upcoming"|"active"|"ended"|"closed" } }
GET  /groups/{id}/leagues   -- anggota -> [League]  (yang diarsipkan disembunyikan)
GET  /leagues/{id}?season=N -- anggota grup ATAU tamu liga itu; selain itu 404
  -> { league, season, frozen, items: [{ rank|null, user_id, name, role:"member"|"guest", points, participated }], me, seasons:[N,...] }
DELETE /leagues/{id}        -- owner/admin, mengarsipkan (hasil musim tetap ada) -> 204
POST /leagues/join-by-code  { code }  -- jadi tamu; dibatasi 10/menit/pengguna (429 league_join_rate_limited)
  -> { league_id, group_id, already_joined }
PUT  /leagues/{id}/manual-scores  { scores: [{ user_id, points 0-1000, note? }] }  -- owner/admin, HANYA liga format "manual" -> 204
```
| `format` | `source` | `scoring` (default pertama) | Poin |
|---|---|---|---|
| `tryout` | `{assessment_id}` | `best_attempt` \| `first_attempt` | nilai attempt submitted/evaluated, bukan preview, di jendela musim |
| `ujian` | `{assessment_id}` | `first_attempt` saja | attempt pertama; retry diabaikan |
| `olimpiade` | `{assessment_ids: [2..10]}` | `sum_of_rounds` | jumlah nilai terbaik tiap babak |
| `learning_path` | `{module_id}` (modul terbit) | `path_progress` | butir yang diselesaikan di subtree pada jendela musim |
| `latihan` | `{module_id}?` | `count_correct` \| `accuracy` | jawaban benar (learning_events); akurasi butuh ≥10 jawaban, kurang dari itu = belum ikut |
| `aktivitas` | - | `activity_count` | JUMLAH aksi belajar (bukan XP) |
| `manual` | - | `manual` | nilai yang diinput guru; `xp_policy` selalu `none` |

Peringkat: poin ↓, lalu yang mencapainya lebih dulu, lalu `user_id` — total dan identik di tiap baca. Yang belum ikut tidak diberi peringkat (`rank:null`) dan ditampilkan setelahnya.
`xp_policy:"normal"`: saat musim ditutup, **3 ANGGOTA teratas** mendapat bonus XP 150/100/50 (`xp_events.reason="league_bonus"`, `reference="league:{season}:{user}"` → tepat sekali) — hanya bila ≥3 orang ikut, tamu tidak pernah dibayar, dan tak ada yang menerima >500 XP bonus liga per 7 hari.
`integrity:"proctored"` belum didukung (`422 integrity_not_supported_yet`).
Kuota liga aktif per grup mengikuti paket **pemilik grup**: Plus 3, Pro tanpa batas (`403 group_league_quota_reached`).
Error tambahan: 422 invalid_league_title|format|scoring|source|period|guest_cap, invalid_season_days, invalid_xp_policy, not_a_manual_league, not_a_participant, invalid_points, already_participant; 404 league_not_found, content_not_found; 409 league_guest_cap_reached, season_over.
**Penutupan musim** dijalankan job `league_season_close` (worker, tiap ≤5 menit): membekukan `final_points/final_rank`, membayar bonus, lalu membuka musim berikutnya (liga berulang; tamu ikut terbawa, poin mulai dari nol) atau menandai liga `finished` (sekali jalan). Idempoten & aman diulang. **`titian-worker` harus berjalan** agar musim tertutup otomatis; status `ended` = jendela sudah lewat, hasil belum dibekukan.

### Ruang Kelas & Grup Kelas (P48) — hanya Pro
Ruang Kelas = baris `cohorts` ber-`owner_id`, sehingga pendaftaran, sesi, absensi terverifikasi, sertifikat, dan tugas memakai layanan kelas yang sudah ada. Tiap Ruang Kelas punya **produk pendukung tersembunyi** (`learning_products`: draft, harga 0, milik pengajar) — inilah yang membuat semua pengecekan `can_manage_cohorts` tetap berlaku, dan harga produk itulah yang menentukan apakah pendaftaran baru `active` (harga 0) atau `pending` (berbayar; alur bayar di P49).
```
POST   /classrooms { name(1-100), description?(<=500) }   -- Pro; 403 classroom_requires_pro; pengajar otomatis diberi profil tutor + role teacher
GET    /me/classrooms   -> { items: [Classroom] }          -- yang dimiliki + yang diikuti (terdaftar)
GET    /classrooms/{id} -- pemilik / siswa terdaftar / platform_admin; selain itu 404
PATCH  /classrooms/{id} { name?, description? }            -- pemilik
DELETE /classrooms/{id}                                     -- pemilik, mengarsipkan (grup & riwayat tetap)
  Classroom: { id, name, description, owner_id, status:"active"|"archived", product_id, price_idr, group_count, student_count, my_role:"owner"|"student", created_at }
GET    /classrooms/{id}/groups  -> [Group]                  -- pemilik & siswa terdaftar
POST   /classrooms/{id}/groups  { ...body POST /groups }    -- pemilik; kind:"kelas", kapasitas 1000, menghabiskan kuota buat (100 untuk Pro)
POST   /groups/{id}/convert { classroom_id }                -- owner grup Belajar + pemilik Ruang Kelas tujuan (Pro); anggota TIDAK dikeluarkan, semua didaftarkan
POST   /groups/{id}/unlink                                   -- kembali ke Grup Belajar; 409 group_has_class_records bila sudah ada sesi
GET    /groups/{id}/sessions -> [{ id, session_date, scheduled_start, scheduled_end, join_url, status }]   -- anggota grup itu
GET    /groups/{id}/class    -> { group_id, cohort_id, total_sessions, roster: [{ user_id, name, role, enrollment_id, enrollment_status, attended, certificate_code }] }  -- owner/admin
POST   /cohorts/{id}/class-sessions { session_date, scheduled_start, scheduled_end, group_id? }   -- endpoint lama + group_id opsional
```
- **Bergabung ke Grup Kelas = mendaftar di Ruang Kelas** (`enrollments`): `active` bila gratis, `pending` bila berbayar; idempoten, pendaftaran yang pernah dibatalkan dihidupkan lagi. Permintaan `pending` (grup ber-approval) baru didaftarkan saat disetujui. Keluar dari grup tidak membatalkan pendaftaran.
- **Sesi per grup**: `group_id` harus grup aktif milik Ruang Kelas itu (`422 group_not_in_classroom`). Roster verifikasi kehadiran sesi itu = anggota grup ∩ terdaftar; sesi tanpa `group_id` = seluruh Ruang Kelas.
- **Beku (downgrade)**: bila pemilik tak lagi Pro, sesi baru, sertifikat baru, Grup Kelas baru, dan convert ditolak `403 classroom_frozen`; semua data tetap terbaca dan pendaftaran tidak berubah. Berlangganan lagi membuka bekuan. Ruang Kelas yang diarsipkan menolak siswa/grup baru (`409 classroom_archived`).
- Error lain: 403 classroom_quota_reached (maks 50 Ruang Kelas per pengajar), 409 group_already_class_group | group_not_class_group, 422 not_a_class_group.

### Liga berjenjang, harga kelas & moderasi (P49)
```
POST   /groups/{id}/circuits { name, cadence:"weekly"|"monthly"|"custom", season_days?, starts_at?, tiers:[{ title, format, source?, scoring?, xp_policy?, allow_guests?, promotion_slots?, relegation_slots? }] }
       -- pemilik/admin grup, pemilik grup HARUS Pro (403 circuits_require_pro); 2–8 divisi, teratas dulu; 422 invalid_circuit_tiers | invalid_cadence (one_off ditolak); Grup Global 422
GET    /groups/{id}/circuits -> [{ id, group_id, name, created_at }]
GET    /circuits/{id}        -> { circuit, tiers: [{ league (League + circuit_id, tier, promotion_slots, relegation_slots), items: [LeaderRow] }] }   -- anggota grup; selain itu 404
GET    /circuits/{id}/movements?season=N -> [{ user_id, name, from_tier, from_title, to_tier, to_title, kind:"promoted"|"relegated"|"placed", created_at }]   -- default: musim tertutup terakhir
DELETE /circuits/{id}        -- arsipkan seluruh sirkuit; DELETE /leagues/{divisi} -> 422 archive_whole_circuit_instead
```
Tier 1 = teratas (promotion_slots dipaksa 0), tier terbawah relegation_slots dipaksa 0. Anggota (lama & baru) mulai di divisi terbawah. Penutupan musim menutup semua divisi serentak dari snapshot beku: naik = anggota dengan poin > 0 teratas sebanyak `promotion_slots`; turun = ekor klasemen anggota (yang tidak naik) sebanyak `relegation_slots`; tamu tidak pindah. `GET /groups/{id}/leagues` tidak memuat divisi sirkuit.
```
PATCH  /classrooms/{id} { price_idr?: 0..10000000 }  -- di atas 0 wajib Pro (403 monetization_requires_pro); 422 invalid_price
GET    /groups/{id}/sessions -> 403 classroom_payment_required bagi siswa berstatus pending (pemilik/admin tidak digerbang)
  Classroom kini juga: my_enrollment_id, my_enrollment_status  -- untuk POST /enrollments/{id}/checkout (alur marketplace yang ada)
POST   /groups/{id}/report { reason:"spam"|"inappropriate"|"harassment"|"fraud"|"other", detail?(<=1000) } -> 201 { id, already_reported }   -- 409 cannot_report_own_group; 429 report_rate_limited
GET    /admin/groups/reports?status=open|actioned|dismissed|all -> [{ id, group_id, group_name, group_kind, group_status, owner_name, member_count, reporter_id, reporter_name, reason, detail, status, resolution, created_at, resolved_at }]   -- AdminPusat View
POST   /admin/groups/reports/{id}/resolve { resolution:"actioned"|"dismissed" }   -- 204; 409 report_already_resolved
POST   /admin/groups/{id}/suspend { reason }   -- 204, AdminPusat Manage; 409 group_already_suspended; Grup Global 422
POST   /admin/groups/{id}/unsuspend            -- 204; 409 group_not_suspended
```

### Liga Global (P47-005)
Grup Global (`00000000-0000-0000-0000-00000000c0de`) punya satu liga sintetis, id `00000000-0000-0000-0000-00000000c0df`: papan bergulir **7 hari terakhir**, dihitung saat dibaca — tanpa musim, tanpa penutupan, tanpa bonus XP (`xp_policy:"none"`, `scoring:"weekly_composite"`, `cadence:"weekly"`).
```
GET /groups/{global}/leagues  -> [League]                 -- selalu tepat satu
GET /leagues/{global_league}  -> { league, season (jendela 7 hari, number 1), frozen:false, items: [50 teratas], me (baris pemanggil, selalu ada bila ia aktif), seasons: [] }
```
Peringkat = `league::composite_score` (rumus SAMA dengan `GET /me/league`): rata-rata tiga komponen 0–100 — streak (maks 30 hari), rata-rata penguasaan (yang yakin saja), dan JUMLAH XP event (maks 50; hitungan, bukan penjumlahan XP). Skor lalu jumlah aktivitas lalu `user_id` menentukan urutan. Peserta = pengguna dengan ≥1 XP event dalam 7 hari; yang dinilai hanya 5.000 paling aktif. `PUT /leagues/{global}/manual-scores`, `DELETE`, dan pembuatan liga di Grup Global tidak berlaku (404/422).
**Alias**: consent kind `global_leaderboard_alias` (`POST /me/consents {kind, granted}`); `granted:true` → nama tampil "Pelajar #A1B2" bagi semua orang selain diri sendiri, di papan ini **dan** di `GET /leaderboard/weekly`. Default (tanpa baris) = nama asli. Tidak butuh konfirmasi wali (mengurangi data yang dibagikan). `GET /me/consents` kini mengembalikan 3 kind.

---

## Kampung Bahasa Pare (ADR-0016)

Game mandiri `alr/game` (`pare.titianasa.com`) memakai backend ini dan alur login yang sama (`POST /auth/google/callback`, access + refresh token). Semua endpoint game di bawah `/pare/*`, wajib `Authorization: Bearer`. Hanya `users` yang dipakai bersama; profil game terpisah dari onboarding Titian.

### Soal & ujian (benchmark level, 2026-09-25)
```
Question.kind: choice | arrange | speak | write
choice.passage?: [{speaker?, text, reading}]   -- teks bacaan (arti hanya di reveal)
choice.passageHidden: bool                     -- dialog menyimak: teks disembunyikan, `audio` = dialog
*.section?: kosakata | membaca | menyimak       -- ujian
write: {instruction, prompt, icon?, audio?}     -- kunci (answers) tidak dikirim
POST /pare/papers/{id}/answers  {index, written}  -- untuk write; dibandingkan tanpa huruf besar, spasi, tanda nada, harakat
reveal.passage?: [{speaker?, text, reading, meaning}] · reveal.line (write)
FinishResult.sections?: [{id, name, correct, total, passed}]   -- ujian
Ujian: 40 soal (16/12/12), lulus ≥ 70% total dan ≥ 50% tiap bagian. GET /pare/levels → exam {questions: 40, pass: 28, section_min: 0.5}
content.json per level: vocab[].value? (angka), cloze[], readings[], dialogues[]; Basic: letters[]
```

### Profil pemain (P1-002)
```
GET   /pare/me                      -> PlayerView | 404 {error:"pare_player_not_found"}   -- 404 = tampilkan onboarding game
POST  /pare/me  {username, nickname, look, gender: "m"|"f", focus?}  -> 201 PlayerView   -- focus: bahasa pilihan onboarding (salah satu dari 5; default "en")
        409 pare_player_exists | 409 username_taken | 422 invalid_username | 422 invalid_nickname | 422 invalid_gender
PATCH /pare/me  {nickname?, look?, gender?, focus?}  -> PlayerView   -- focus: bahasa yang sedang dipelajari (422 invalid_lang bila bukan salah satu dari 5)   -- username permanen (field lain diabaikan);
        gender hanya bisa diisi sekali (pemain lama yang gender-nya null), mengganti = 422 gender_locked
-- PlayerView.gender: "m" (Camp Putra, barat) | "f" (Camp Putri, timur) | null (belum memilih — game menampilkan pilihan sekali)
GET   /pare/usernames/{username}    -> { username (dinormalkan), available, reason|null }
```
- `username`: disimpan huruf kecil, unik tanpa peduli kapital, 3–20 karakter `a-z 0-9 _ .`, tidak diawali/diakhiri titik, tanpa `..`, nama cadangan (admin, titian, pare, npc, …) ditolak sebagai `username_taken`.
- `nickname` ("nama panggilan"): 1–16 karakter, spasi dirapikan. Di game tampil `Nickname @username` di atas karakter.
- `look`: `{skin, hair, hairStyle, shirt, outfit, pants, shoes, acc}` — nilai tak dikenal diganti default, kunci lain dibuang.
- `PlayerView`: `{user_id, username, nickname, look, zone, pos, xp, level (1 + xp/100, turunan), money, hearts (0–5 langkah 0,5), stamina, fullness, focus, violations, streak, languages: [{lang, level, lang_xp, level_start_xp, exam_tries}] × 5, created_at}`. Pemain baru: Rp0, XP 0, nyawa 5, stamina 100, di `camp`.

### Konten, kertas soal, misi (Pare-2 / P2-001…005)
Soal dibangun dan dinilai **di server**; kunci jawaban tidak pernah dikirim sebelum soal dijawab.
```
GET  /pare/content                     -- PUBLIK, tanpa token. {version, ladder, languages[5]} (kosakata, frasa, percakapan, tata bahasa,
                                          konsep, tangga level). ETag + Cache-Control: public, max-age=300, stale-while-revalidate=86400;
                                          If-None-Match -> 304. Tidak ada kunci soal (soal dibuat server).
GET  /pare/billboards                  -- PUBLIK, tanpa token, cacheable (ETag konten). {note, rotate_seconds, slots: {slot: [{title, subtitle?, bg, fg, accent?}]}, ad_free}
                                          Isi slot iklan pada papan billboard (spanduk di bangunan DINONAKTIFKAN 2026-09-26): `umum-west-1|umum-west-2|umum-garden-left|umum-garden-right|umum-gates-1..3|umum-library-board|umum-minimarket-board|umum-park-left|umum-park-right`,
                                          per kampung `<lang>-main`. Panel `house` ("Space ini Bisa Digunakan" + nomor WA besar; `emphasis: "subtitle"`) bergilir di semua slot dan jadi default slot kosong. Konten diisi di `data/pare/content.json` → `billboards.slots` lalu backend dideploy ulang (belum ada UI admin). Pemain `ad_free` melihat panel `ad_free`.
                                          Empat papan potret 4:5 rapat jalan raya Kampung Bahasa (barat→timur): `umum-poster-1` (kecil, 2 petak, area iklan 28×35 px), `umum-poster-2` & `umum-poster-3` (lebar, 4 petak, 60×75 px),
                                          `umum-poster-4` (kecil). Selama slot belum punya sponsor (dan untuk pemain `ad_free`) game menampilkan pixel art bawaan yang bergantian tiap 6 dtk, tanpa label IKLAN:
                                          papan kecil memutar Kampung Inggris, Arab, Mandarin, Korea, Jepang (urutan papan timur digeser agar tak sama dengan yang barat); papan lebar memutar
                                          "Kampung Bahasa Pare" dan himbauan "Chat dan ngobrol hanya boleh pakai bahasa Inggris, Mandarin, Arab, Korea, Jepang — bukan Indonesia".
                                          Begitu server mengisi slotnya, sponsor tampil bertumpuk (logo, judul, subjudul).
GET  /pare/state                       -> {words{lang{id:[seen,correct]}}, lessons{key:n}, done_today[], photos[], daily{date,quests[],counts}, exam_cooldown_min{lang}}
GET  /pare/levels                      -> {languages:[{readiness{level,mastered,words_need,points,points_need,ready,has_next}, exam{fee,tries,tries_per_fee,cooldown_min,questions,pass}}]}
GET  /pare/daily                       -> {date, quests:[{id,icon,text,event,target,count,done}], counts}   -- 3 misi/hari WIB, sama untuk semua pemain
POST /pare/events {event}              -> {missions[], level_up|null, xp, player}
        event: park | meal | visit:<lang> | buy:<lang> | chat:<lang> | photo:<lang> | violation ; lainnya 422 invalid_event
        (sementara: game melapor sampai Pare-3/4 mensimulasikan di server. Hadiah tetap di server: batas XP chat 15 pesan/hari +5/level,
         foto sekali per kampung, misi dibayar sekali.)

POST /pare/papers {kind, lang, role?, challenge?, can_speak?}  -> 201 {paper_id, kind, lang, key, level, graded, scored, assist, time_limit, challenge, pay_share (1 kelas / 0,5 mandiri / 0,25 challenge), questions[], exam_fee, exam_tries_left}
        kind: class(role) | market | library | desk | club | fish | challenge(challenge) | exam | lastchance
        kind: job  -- satu giliran Kerja Paruh Waktu: 10 soal di level pemain; 422 job_limit bila 4 giliran berbayar hari itu sudah habis.
        finish untuk job menambah {wage (0 = tidak lulus), shifts_left, need_correct, passed}; upah = 200 × (level+1) × 10 × 1,25, hanya bila benar ≥ 80% dan tidak ditinggalkan. pay_share job = 0 (tidak ada bayaran per jawaban).
        403 no_hearts (kelas/club saat nyawa 0) | 409 lastchance_not_needed | 409 no_next_level | 429 exam_cooldown | 422 insufficient_money (ujian)
        Ujian: bayar examFee (Rp25.000 + 10.000/level) untuk 2 percobaan; jeda 60 menit setelah gagal; 20 soal, lulus >= 17.
POST /pare/papers/{id}/help {index, kind: hint|translate}  -> {hide[]|first|translation|optionNotes}   -- hanya challenge; bantuan = hadiah soal itu separuh
POST /pare/papers/{id}/answers {index, choice? | arrange? | heard?[] | skipped?}
        -> {final, ok, skipped, xp, money, score, tries_left, reveal{answer,explain,...}, word_key, xp_total, money_total, lang, lang_xp, level_start_xp}
        benar: +10 XP, bayaran per level (kelas/club: Basic Rp200, +200/level; belajar mandiri, perpustakaan, pasar, memancing: separuhnya; Balai Tantangan: seperempatnya; separuh lagi dengan bantuan; kegiatan di luar kelas maks 5 jawaban penuh per sesi, mis. Basic Rp1.000 — di bawah satu kelas 6 soal = Rp1.200; dibulatkan Rp5); salah: -5 XP (tidak turun di bawah awal level); soal bicara
        dinilai kemiripan >= 0,7 dengan 3 percobaan (final=false selama masih boleh coba) dan tidak pernah mengurangi XP.
        409 already_answered | 409 time_up (ronde berwaktu) | 409 paper_finished | 404 paper_not_found (kertas milik pemain lain)
POST /pare/papers/{id}/finish {aborted?} -> {kind,lang,correct,total,answered,earned_xp,earned_money,perfect,bonus_xp,passed,exam_tries_left,recovered,level_up{lang,level,pay},missions[],club_bonus,player}

Pare-9 — jalur belajar (ADR-0019, tiket P9-002..004; kode `services/pare_path.rs`):
GET  /pare/path/{lang}                     -> {lang, level, level_name, available, chapters[{id,key,title,label,icon,status(done|open|locked),done,total,words,concepts,nodes[{id,kind(materi|latihan|practice|check|mission),title,lesson,status(done|open|locked|soon),auto,score,attempts}]}], next{node,kind,chapter,title,chapter_title}|null}   -- available=false: level tanpa bab, game memakai kelas lama; simpul misi: done bila misinya selesai, selain itu soon
GET  /pare/path/{lang}/lessons/{chapter}:{lesson}        -> {node, chapter, chapter_title, title, kind(words|letters|concept), cards[]}   -- kartu Materi tanpa kunci; 409 node_locked
POST /pare/path/{lang}/lessons/{chapter}:{lesson}/done   -> path (seperti di atas)   -- Materi dibaca: Latihan terbuka, kata tercatat "pernah dilihat" (bukan "benar")
POST /pare/papers {kind:"path", lang, node}  -> paper biasa; 409 node_locked|node_not_ready (Materi dan Misi tidak punya soal), 404 node_not_found. Jawaban salah di Latihan/Praktik diulang sekali (respons jawaban memuat `retry` = butir yang ditambahkan di akhir); XP tidak pernah berkurang
POST /pare/papers/{id}/finish -> untuk kind=path memuat `path {node, kind, score (benar pada percobaan pertama, 0–100), passed, reward [xp, money] | null (hanya penyelesaian pertama), suggest_review, chapter_done}`; Cek bab lulus ≥ 80%

Pare-9 — misi (ADR-0019 §6, §16; tiket P9-006; kode `services/pare_mission.rs`, data `data/pare/missions.json`):
GET  /pare/missions?lang=en                -> {lang, missions[{id,title,tier(chapter|villager|big),chapter,level,giver,place,minutes,status(locked|new|active|review|done),stars,best_score,step,steps,locked_reason}]}
GET  /pare/missions/{id}                   -> kartu misi: {identity{lang,lang_name,level,level_name,cefr,stage,tier,chapter_no,chapter_count,chapter_title,giver} (juga ada di tiap baris /pare/missions; dipakai agar misi tidak hanya berupa judul), cost (perkiraan biaya pembelian di levelmu, dihitung dari harga menu), money (uangmu sekarang), earn{per_answer,daily_mission,path_node,level_up} (cara mendapat uang), steps[].at / current.at (di mana tempatnya, dalam kata), id,title,en,story,result,prep[],key[],giver,place,mode,minutes,proof,reward{xp,money,refund (belanjaan misi yang diganti saat selesai pertama kali)},scoring{hasil:40,bahasa:40,mandiri:20,stars:[60,80,90]},status,locked_reason,stars,best_score,attempts,step,steps[{n,type,text,npc,zone,state(done|current|todo)}],current{n,type,text,npc,zone,turn,turns,say,question | event}|null   (`event` = yang boleh dilaporkan game untuk langkah pergi/bicara/temukan/do:*; null untuk langkah yang dihitung server),score{hasil,bahasa,mandiri,total,stars,weak[]}|null}   -- `current.question` = butir milik pemain ini (opsi diacak per pemain), tanpa kunci
     `requires` (di baris /pare/missions: id bab yang harus selesai, misi warga) dan `requirement` (di kartu: {kind chapter|missions, chapter, chapter_no, chapter_count, chapter_title, lang, lang_name, level_name, done, progress{done,total}, next{title}, order[{icon,name,what}] (Materi→Latihan→Praktik→Cek bab), pass}) menjelaskan syarat buka misi; game menampilkannya dan tombol "KE JALUR · BAB N" membuka Jalur bahasa itu dengan bab tsb terbuka.
POST /pare/missions/{id}/start             -> kartu (status active)   -- mulai, lanjut (bila active), atau main lagi (run baru, varian baru; skor terbaik, bintang, dan hadiah tetap); 422 mission_locked (bab belum lulus Cek)
POST /pare/missions/{id}/steps/{n}  {event? | choice? | arrange? | written? | hint? (1|2|3) | redo?}  -> {ok, reaction?, hint?, reveal?, tries?, finished, level_up{lang,level,pay}|null (misi ini syarat terakhir level: pemain naik), mission}
    langkah pergi dengan `tile` {x,y,r}: server juga memeriksa posisi tersinkron pemain (|dx|+|dy| ≤ r), 422 not_there_yet; game melaporkan otomatis saat pemain sampai (current.tile). Langkah pergi/bicara/temukan/sosial: {event:"goto:en"|"talk:kate"|"find:…"}; zona pemain di server harus cocok (422 wrong_place; 422 wrong_event)
    langkah beli/lakukan: selesai sendiri dari kejadian server (klien tidak boleh mengirimnya: 422 event_from_server; hanya `do:*` untuk lakukan yang boleh dilaporkan klien) (`pare_daily::bump` memanggil `pare_mission::on_events`: `meal`, `buy:{zona}`, `item:{id}`, `park`, `class:{lang}` …); mengirim kejadian dari klien → 422 event_from_server untuk beli. `miss` = kejadian yang dihitung kesalahan Hasil tanpa menyelesaikan langkah
    langkah sosial: kirim {event:"talk:<warga>"} untuk tiap orang yang disapa; selesai setelah `need` orang berbeda (current.options[{event,met}], current.need/have; respons memuat progress [sudah, perlu]; orang yang sama dua kali tidak dihitung; 422 wrong_event untuk orang di luar daftar)
    langkah dialog/baca/dengar: jawaban butir giliran ini (zona pemain harus cocok: 422 wrong_place); salah → {ok:false, reaction, hint(tingkat 1), tries} tanpa kunci; benar → {ok:true, reveal}. hint 1 gratis; hint 2 = kata pertama + terjemahan (−2 Mandiri); hint 3 = jawaban ditunjukkan lalu butir serupa sekali lagi (−5 Mandiri, 0 poin bahasa giliran itu)
    urutan dipaksa: 409 not_current_step · mission_not_started · mission_not_active
    skor di bawah 60 → status `review` dengan `score.weak` (tiga langkah paling mahal); `{redo:true}` pada langkah n membuka langkah itu lagi (varian baru). Hadiah dan stempel hanya saat ≥ ⭐ dan hanya sekali
GET  /pare/journey/{lang}   -> Buku Perjalanan (P9-009), hanya baca, SATU bahasa: {lang, lang_name, has_missions, levels[{level,name,cefr,state,missions,has_path}] (tangga level bahasa itu, jumlah misi per level), villagers kosong bila bahasa belum punya misi warga, level, level_name, stages[{level,name,place,level_name,cefr,state(done|current|ahead)}] | null (hanya bahasa Inggris), stage_percent, path_available, requirements[{key(chapters|chapter_missions|side_missions|big_mission),label,have,need,done,soon?}], can_level_up, journey_level (level dilalui lewat jalur, bukan kata+poin), next{…}|null, missions[…seperti /pare/missions], collection[{key,kind(stamp|title|card|region|friend),label,earned,level,from}], villagers[{key,name,role,friend,friendship (0–7),missions[{id,title,status,stars}]}]}   -- syarat naik level mengikuti ADR-0019 §16.6 (Basic: 2 misi warga, lain: 3); Misi Besar `soon` sampai P9-013
WS /ws/pare menerima {t:"mission", id, status, step} saat misi pemain bergerak (setelah POST start/steps).
        idempoten (panggilan kedua mengembalikan hasil yang sama). Bonus sempurna +20 XP (kelas), bonus Speaking Club +20 XP sekali/hari, streak harian,
        naik level otomatis bila 80% kata level dikuasai & poin >= 150 x (level+1), lulus dibayar Rp1.000 x level baru.
```

### Hidup harian (Pare-3 / P3-001…003)
Nyawa, stamina, kenyang, tidur, makan, dan pembelian dihitung & dihargai **di server**, dihitung malas dari `last_seen` (tanpa proses latar). Browser hanya meminta.
```
POST /pare/tick {zone?, pos?, walked?, rode?, boot?}  -> LifeResult
        Panggilan berkala (game: tiap 20 dtk saat tab terlihat, dan setelah pindah zona). Menyusul waktu nyata: jeda >= 60 mnt = istirahat
        (kembali ke Camp, kenyang >= 70, stamina >= 85); jeda lebih pendek = waktu bermain (kenyang turun 10/jam, lapar = stamina -1/mnt,
        kurang tidur < 5 jam/24 jam = -0,5/mnt). Langkah: 0,04 stamina/petak jalan kaki, 0,015 dengan sepeda yang disewa hari ini (bukan di Camp).
        Stamina habis = -1/2 nyawa, stamina 30, kembali ke Camp (event "fainted"). boot=true (game baru dibuka): pemain yang tidur dibangunkan,
        zone/pos tidak dikirim (server yang menjawab posisi terakhir).
GET  /pare/menus/{zone}/{venue}       -> [{item, id, icon, name[3], kind, base_price, price}]   -- price sudah diskon level kampung (5%/level, maks 25%, dibulatkan ke Rp100)
POST /pare/shop/buy {zone, venue, item} -> LifeResult   -- 422 insufficient_money | invalid_item | invalid_zone
POST /pare/travel {to}                -> LifeResult   -- ADR-0022: beli tiket di terminal/stasiun/bandara zona pemain dan pindah ke titik `to` ("kota-terminal", "kota-stasiun", "kota-bandara", "umum-terminal", "umum-stasiun", "<gb|cn|eg|jp|kr>-bandara"); 422 invalid_destination | no_route | insufficient_money | fainted. Tarif di `player.life.fares` {bus, rail, air}. Terbang ke negara butuh level bahasa negara itu ≥ `player.life.flight_min_level[zona]` (422 level_too_low); pulang tidak.
POST /pare/hotel                      -> LifeResult   -- ADR-0022 §3a: menginap di kota atau luar negeri (`player.life.hotel_price`), tertidur di tempat; 422 no_hotel (di Pare) | insufficient_money. `POST /pare/sleep` dari kota/luar negeri: 422 far_from_camp.
POST /pare/flat                       -> LifeResult   -- flat mahasiswa di luar negeri (B2): tidur di tempat seharga `player.life.flat_price` (Rp5.000); 422 no_flat (bukan di luar negeri) | insufficient_money. Venue `gb-flat`.
POST /pare/laundry | /pare/bike | /pare/park | /pare/sleep | /pare/wake  -> LifeResult
        422 laundry_done (sekali sehari) | insufficient_money | park_cooldown (30 mnt, detail memuat menit tersisa)
LifeResult = {message, events[starving|exhausted|fainted], catch_up{idle_hours, slept_hours}, gained (stamina penuh -> +1/2 nyawa), missions[], player}
PlayerView.life = {sleeping_since(ms), rest_minutes_24h, sleep_deprived, meals_today, snacks_today, meals_per_day, max_snacks, min_rest_hours,
                   bike_active, laundry_today, bike_price, laundry_price}
```
Efek makan: makan berat +35 kenyang & stamina +15 (kekenyangan >= 105 atau > 4×/hari: stamina -10), jajan +12 & +5 (> 3×/hari: -5), minuman +5 & +4 (kopi +8); stamina penuh -> +1/2 nyawa dan turun ke 70. Makan menghitung misi `meal`, beli di kampung menghitung `buy:<lang>`, taman `park` — dihitung server. Tidur: stamina +20/jam; bangun dari tidur >= 1 jam menambah kenyang >= 60.
Perubahan uang tercatat di `pare_ledger` (`spend`), perubahan nyawa (`life`). `zone`/`pos` masih dilaporkan game lewat tick sampai Pare-4 (server mengetahui zona dari realtime). Endpoint sementara `POST /pare/spend` (Pare-2) sudah dihapus.

### Realtime & chat (Pare-4 / P4-001…002)
```
GET  /ws/pare?token=<access token>     -- WebSocket. Tanpa/token salah: close 1008. Token sah tapi belum onboarding game: close 4404 `pare_player_not_found`.
        Satu koneksi per pemain (yang baru menendang yang lama: pesan `kicked`). Pesan klien maks 4 KB.
        Identitas (nama panggilan, @username, look, gelar level) SELALU dari server; klien hanya mengirim posisi.
client -> server (JSON, field `t`):
  hello {room, channel?, x, y, dir} | room {room, x, y, dir} | channel {n} | channels | move {x, y, dir} | typing {on} | social_invite {with, act: ngobrol|salaman|tos|foto} | social_answer {with, ok} | profile {}   -- profile: server memuat ulang look/gelar
  chat {text, scope?: all|near|private, to?: [@username], group?: {id, name}}
server -> client:
  welcome {id, uid}  (uid = @username, id kanonik koneksi) | snapshot {room, channel, channels[], players[], chat[]} | channels | join {p} | leave {id}
  moves {m: [[id, x, y, dirCode]]}  (satu batch per saluran, 100 ms setelah langkah pertama)  | chat {msg} | notice {text} | typing {id, on} | social_invite {from, name, act} | social_no {why: far|wait|declined|expired} | social_play {a, b, act} | profile {id, look, title} | kicked {text}
  violation {reason, hearts, violations}     -- aturan bahasa dilanggar: -1/2 nyawa sudah diambil server
  reward {xp, lang, reward{xp, missions[], level_up}, player}   -- pesan berbahasa target: +3 poin (batas harian 15 pesan + 5/level), misi chat
```
- **Saluran:** tiap zona dibagi saluran maks 50 pemain (yang paling terisi tapi masih muat dulu); pemain hanya menerima data salurannya. Kamar Camp privat. Antrean keluar per koneksi dibatasi 256 pesan (klien lambat kehilangan batch lama); gerakan dibatasi 16/dtk.
- **Aturan bahasa (`services/pare_langrule.rs`, port `langrule.ts`, 588 kasus paritas), ketat sejak 2026-09-25:** di kampung hanya bahasanya; di **Kampung Bahasa dan Camp hanya Inggris, Korea, Mandarin, Jepang, Arab** — bahasa Indonesia dan bahasa lain (Prancis, Rusia, Thai, …) melanggar; kalimat Latin ≥ 3 kata yang tidak terbaca sebagai bahasa yang diizinkan = pelanggaran, 1–2 kata dimaafkan. Berlaku untuk semua jenis pesan. Pesan tetap terkirim (game memperingatkan dulu) tapi pelanggaran memotong 1/2 nyawa (ledger `life`, `violations` +1).
- **Chat tersimpan:** `all` -> `pare_channel_messages` (retensi 30 hari, dipangkas tiap jam); `near` tidak disimpan; `private` -> `pare_conversations` (`dm:<uuid kecil>:<uuid besar>` atau `g:<id>`) + `pare_messages`, dikirim ke anggota online di zona mana pun. Grup: id 6-24 huruf/angka dari klien, nama <= 24, butuh >= 2 teman (maks 5); anggota grup yang sudah ada saja yang boleh menulis.
- **Langkah & posisi:** selama socket terbuka, server menghitung petak yang dilalui dan tahu zona/posisi; `POST /pare/tick` memakai itu (laporan klien hanya dipakai bila offline, dan tidak pernah menurunkan hitungan server).
```
PUT  /pare/me/avatar                    -> 200 {avatar: token}   (foto profil: body = gambar itu sendiri, JPEG/PNG/WebP ≤ 300 KB, jenis dicek dari byte; game mengirim 256×256 JPEG; mengganti menghapus yang lama; 422 invalid_avatar, 429 avatar_rate_limited bila < 3 dtk dari unggahan sebelumnya)
DELETE /pare/me/avatar                  -> 204
GET  /pare/avatars/{token}              -> gambar   (PUBLIK tanpa login; token acak berganti tiap unggah, cache `immutable` setahun; 404 avatar_not_found)
GET  /pare/inbox                        -> ChatMsg[]  (50 pesan terakhir dari 30 percakapan terbaru, lama -> baru; format sama dengan pesan realtime)
POST /pare/conversations/{id}/leave     -> 204        (grup; id tanpa awalan `g:`; anggota terakhir keluar = grup & pesannya dihapus) | 404 conversation_not_found
GET  /pare/conversations/state          -> [{conversation, last_read_at: ms|null, request: bool}]   (per percakapan pemain: kapan terakhir dibaca & apakah masih PERMINTAAN PESAN)
POST /pare/conversations/{id}/read      -> 204        (percakapan dibuka: semua sampai sekarang terbaca; id lengkap seperti `dm:<uuid>:<uuid>` / `g:<id>`) | 404 conversation_not_found (bukan anggota)
POST /pare/conversations/{id}/accept    -> 204        (terima permintaan pesan; membalas juga menerima)
POST /pare/conversations/{id}/clear     -> 204        ("hapus chat": riwayat sampai sekarang disembunyikan untuk pemain ini saja; pesan baru muncul lagi)
GET  /pare/stats                        -> {online, cap, zones{zone:[{n, count}]}}   (perlu login)
```
Endpoint `POST /pare/events` kini hanya menerima `visit:<lang>` dan `photo:<lang>` (chat & pelanggaran dinilai hub).

**Zona (ADR-0022, 2026-10-07):** `zone` kini juga `kota` dan `gb|cn|eg|jp|kr`. `kota` mengikuti aturan, menu, dan harga `umum`; negara mengikuti kampung bahasanya (`gb`→`en`, `cn`→`zh`, `eg`→`ar`, `jp`→`ja`, `kr`→`ko`). Laporan posisi (`/pare/tick`, soket) tidak bisa memindahkan pemain antara Pare, kota, dan negara: hanya `POST /pare/travel`. `POST /pare/events` juga menerima `venue:<id>` (id = jenis tempat di Kampung Bahasa, `kota-<jenis>` atau `<negara>-<jenis>` di tempat lain; 12 XP + Rp600 sekali sehari per id) dan `photo:<negara>` (foto landmark pertama di negara itu, terpisah dari `photo:<lang>` kampungnya).

### Push notification (Pare-5 / P5-002…003)
```
GET    /pare/notify                      -> {enabled, public_key (VAPID, base64url), devices, kinds: {messages, missions, streak, sleep}}
PATCH  /pare/notify {kind: bool, …}      -> sama   -- 422 invalid_notify untuk kunci tak dikenal
POST   /pare/push/subscriptions {endpoint, keys: {p256dh, auth}}   -> 204   (PushSubscription.toJSON(); endpoint https; browser yang ganti akun ikut pindah)
DELETE /pare/push/subscriptions {endpoint}                         -> 204
POST   /pare/push/test                    -> {devices}   (notifikasi percobaan ke semua perangkat pemain)
```
- Dikirim langsung dari server (Web Push RFC 8291 `aes128gcm` + VAPID RFC 8292, `services/web_push.rs`, crypto `ring`) — tanpa layanan pihak ketiga. Kunci: env `PUSH_VAPID_PUBLIC_KEY` / `PUSH_VAPID_PRIVATE_KEY` / `PUSH_VAPID_SUBJECT` (buat dengan `cargo run --bin pare_vapid_keys`); tanpa kunci push nonaktif (`enabled: false`).
- Pemicu: **messages** (pesan personal/grup saat penerima tidak membuka game; maks 1 per percakapan per 2 menit), **missions** (misi hari ini, sekali sehari mulai 07:00 WIB), **streak** (streak > 0 dan belum belajar hari ini, mulai 19:00 WIB), **sleep** (stamina penuh lagi saat tidur, sekali per tidur). Tiga yang terakhir dari job `pare_push_reminders` di `titian-worker` (tiap 5 menit). Maks **12 notifikasi/hari** per pemain. Langganan yang dijawab 404/410 oleh layanan push dihapus.
- Payload yang diterima service worker: `{title, body, tag, url}` (`url` `/?chat=1` membuka daftar chat, `/?quests=1` membuka misi).

### Percakapan suara (Pare-7a, ADR-0017)

> **Evaluasi bahasa dari transkrip DILEPAS SEMENTARA (2026-09-26).** Voice note dan panggilan live tidak lagi ditranskrip, dinilai, atau dihukum: tidak ada STT server, `judge_speech`, strike/penalti, pesan hub `voice_transcript` / `voice_result`, maupun penandaan sistem "mikrofon tanpa transkrip". Yang tetap ada: rekam/unggah/putar/hapus otomatis 3 hari, panggilan live LiveKit, blokir, lapor & antrean moderasi, ekspor/hapus data. Tabel `pare_voice_transcripts`/`pare_voice_strikes` dibiarkan (data lama). Kode lama diarsipkan di `titian-backend-rust/attic/pare-voice-evaluation/`.
```
GET  /pare/voice/eligibility?lang=&conversation=   -> {consent, note_max_seconds, note: {allowed, reason, needs_plan}, live: {allowed, reason, needs_plan, min_level, levels: {username: level}, remaining_seconds, daily_limit_seconds}}
POST /pare/voice/consent {version}                 -> 204   (menyetujui/menyetujui ulang; satu baris per pemain)
POST /pare/voice/notes {conversation, lang, duration_ms, mime}   -> 201 {id, upload_url, expires_in}   (P7-003)
POST /pare/voice/notes/{id}/finish                   -> 204   (klien sudah unggah; jadi pesan kind="voice" lewat hub/inbox; body apa pun diabaikan — dulu `{transcript}`)
GET  /pare/voice/notes/{id}/audio                  -> {url}   (URL putar bertanda tangan; hanya anggota percakapan)
GET  /pare/blocks                                  -> [{username, nickname}]   (P7-007; pemain yang kamu blokir untuk suara)
POST /pare/blocks {username}                       -> 204   (idempoten; 422 cannot_block_self, 404 pare_player_not_found)
DELETE /pare/blocks/{username}                     -> 204
POST /pare/voice/reports {ref: "note:<id>", reason}   -> 201 {id, muted_until}   (422 invalid_ref/invalid_reason/cannot_report_self, 404 voice_note_not_found, 403 not_a_conversation_member, 409 already_reported, 429 report_rate_limited)
POST /pare/voice/rooms {conversation, lang}       -> 201 {room, livekit_url, livekit_room, token, token_expires_in, invited: [username], remaining_seconds}   (P7-009; 422 live_not_eligible + detail per peserta, 409 already_in_call, 503 live_not_configured)
POST /pare/voice/rooms/{id}/join                   -> {room, livekit_url, livekit_room, token, …}   (yang diundang menjawab / penelepon minta token baru; 404 call_expired, 403 not_invited, 409 already_in_call, 422 live_not_eligible)
POST /pare/voice/rooms/{id}/decline                -> 204   (bila tak ada lagi yang bisa menjawab: panggilan batal, penelepon dapat `voice_cancelled`)
POST /pare/voice/rooms/{id}/leave                  -> 204   (menutup telepon, atau membatalkan panggilan yang masih berdering)
POST /webhooks/livekit                             -> 200   (PUBLIK; hanya dari LiveKit: header `Authorization` = JWT HS256 ber-`sha256` = base64 SHA-256 dari body; 401 selainnya)
GET  /admin/voice/reports?status=open|actioned|dismissed   -> [{id, reference, reporter, reported, reason, excerpt, flagged, status, action, action_note, created_at, reviewed_at, reporters_7d, strikes}]   (Admin Pusat, izin View; yang `flagged` dulu, lalu terlama)
POST /admin/voice/reports/{id}/action {action: dismiss|warn|lock, days?: 1-30, note?}   -> laporan terbarui   (izin Manage; 422 invalid_action/invalid_days, 409 report_already_reviewed)
GET  /pare/voice/data                              -> {consent: {version, accepted_at}|null, notes: [{id, conversation, lang, zone, duration_ms, status, created_at, expires_at, transcript: [{text, confidence, verdict}]}], strikes}   (P7-006, akses data UU PDP)
DELETE /pare/voice/data                            -> {notes: n}   (hapus audio semua voice note pemain (+ sisa transkrip lama) & cabut persetujuan)
```
- **Lapor panggilan live:** `POST /pare/voice/reports {"ref": "live:<sesi>", "username": "<terlapor>", "reason"}` — `username` wajib (panggilan punya banyak peserta; 422 `username_required`), pelapor dan terlapor harus peserta sesi (403 `not_in_session` / 422), sesi tak ada = 404 `voice_session_not_found`. Tak ada kutipan (`excerpt` null): ucapan live tak pernah disimpan.
- `lang` salah satu dari 5 bahasa Pare (422 `invalid_lang` selainnya); `conversation` id percakapan Personal/Grup yang sudah ada (404 `conversation_not_found`; 403 `not_a_conversation_member` bila pemain bukan anggotanya).
- **Suara untuk Plus/Pro (2026-10-11):** mengirim voice note dan menelepon butuh paket aktif (`needs_plan: true` bila pemain belum punya; `POST /pare/voice/notes` dan `POST /pare/voice/rooms` → 403 `plan_required`); panggilan butuh paket untuk setiap peserta (422 `live_not_eligible`, "@user: belum Plus atau Pro"). Mendengarkan (`GET …/audio`) tidak butuh paket.
- Gerbang `note` (voice note, semua level): persetujuan → kunci suara aktif (`pare_voice_locks`) → blokir (`pare_blocks`, dua arah) → hubungan "sudah saling membalas chat teks" (Personal: kedua pihak; Grup: pengirim + minimal satu anggota lain), urut dari yang dicek lebih dulu; `reason` berbahasa Indonesia untuk UI. `POST /pare/voice/notes` menegakkan gerbang yang sama (422 `voice_not_eligible` + alasan sebagai `detail` bila gagal).
- Gerbang `live` (panggilan langsung) = semua gerbang `note` (persetujuan, kunci, blokir, sudah saling membalas). **Level tidak lagi menjadi syarat (2026-09-26): `content.json` → `voice.liveMinLevel` = 0 untuk semua bahasa**, sehingga semua level boleh menelepon; mekanismenya (`live.min_level`, alasan "level") tetap ada dan bisa dinaikkan lagi lewat konten. Setiap anggota percakapan diperiksa, bukan hanya penelepon.
- **Batas waktu telepon per hari (2026-09-26, migrasi 0093):** tiap pemain punya jatah bicara live per hari WIB (semua panggilan digabung) menurut **level di bahasa panggilan**: `content.json` → `voice.liveDailyMinutes` = `[10, 15, 20, 30, 30, 30, 30]` menit untuk level 0.. (Basic 10 · A1-setara 15 · A2-setara 20 · B1-setara ke atas 30; tangga level kelima bahasa sejajar: A1 = HSK 1 = JLPT N5 = TOPIK 1 = Mubtadi' 1, dst). Waktu dihitung per segmen dari webhook `participant_joined` → `participant_left`/`room_finished` (`pare_voice_participants.seg_started_at`, `talk_seconds`); tidak ada isi percakapan yang disimpan. Semua anggota harus punya sisa ≥ 60 dtk agar panggilan bisa dimulai/dijawab (422 `live_not_eligible` "@user: batas waktu telepon hari ini sudah habis"). `eligibility.live.remaining_seconds/daily_limit_seconds` = milik penanya; `RoomJoin.remaining_seconds` = sisa waktu si pemegang token. Saat waktu habis server mengirim hub `{"t":"voice_limit","room"}` lalu mengeluarkan pemain lewat LiveKit `RemoveParticipant` (env `LIVEKIT_API_URL`, mis. `http://livekit:7880`; bila kosong dipakai `LIVEKIT_URL` dengan ws→http). Klien menghitung mundur dan menutup telepon sendiri di angka nol.
- Belum ada gerbang batas laju di endpoint ini (baru relevan saat undangan live ada, P7-009).
- `POST /pare/voice/notes` cuma menyimpan metadata + mengembalikan URL unggah langsung ke storage (klien PUT bytes-nya sendiri, backend tidak menyentuhnya) — 422 `invalid_duration`/`invalid_mime` bila melebihi batas (`content.json` → `voice.noteMaxSeconds`) atau bukan audio.
- `POST /pare/voice/notes/{id}/finish` memverifikasi objeknya benar-benar ada di storage (422 `voice_note_not_uploaded` bila belum), lalu mengirim lewat hub sekali saja (409 `voice_note_already_sent` bila dipanggil dua kali; 403 `not_your_voice_note` bila bukan pengunggahnya). Pengiriman pesan **tidak menunggu** penilaian transkrip — keduanya terjadi di request yang sama tapi hasil transkrip tidak menahan pesan.
- Batas laju: 10 voice note / menit / pemain (`create_note` → 429 `voice_rate_limited`) — pembatas spam unggahan.
- `ChatMsg` privat (hub & inbox) juga membawa `conversation` (id percakapan server: `dm:<uuid>:<uuid>` / `g:<id>`) — satu-satunya cara game tahu id itu untuk memanggil endpoint voice; selalu ada karena voice baru boleh setelah kedua pihak saling chat (P7-008). `eligibility.note_max_seconds` = batas rekaman dari server, agar FE tidak meng-hardcode 60 dtk.
- **Permintaan pesan & blokir chat (2026-09-26, migrasi 0092):** chat personal pertama dari orang yang belum kamu terima adalah *permintaan*: salinan untuk penerima membawa `request: true`, TANPA push notifikasi, toast, gelembung, atau badge belum-dibaca; game menaruhnya di bagian "Permintaan pesan". Penerima memilih **Terima** / **Hapus** ("hapus chat") / **Blokir**; membalas = menerima. Yang memulai otomatis diterima. **Blokir** (`POST /pare/blocks`) kini juga memblokir chat dua arah: pesan dari yang diblokir dibuang diam-diam (tidak disimpan, ia tidak diberi tahu), dan si pemblokir yang menulis ke yang diblokir dapat notice "Kamu memblokir pemain ini…". Daftar blokir & buka blokir: `GET /pare/blocks`, `DELETE /pare/blocks/{username}`. Status baca disimpan di server (`last_read_at`), jadi tidak reset saat aplikasi ditutup/dibuka atau ganti perangkat.
- **Foto profil (2026-10-02, migrasi 0094):** `PlayerView.avatar` (token atau null) dan hub `PlayerInfo.avatar` / `{"t":"profile", ..., avatar}` membawa token; URL gambar = `/pare/avatars/{token}`. Game menggambarnya di atas nama sebagai lingkaran: milik sendiri bercincin biru, milik pemain lain tanpa cincin; tanpa foto tampil inisial berwarna. Ukuran label & foto mengikuti zoom. Foto ikut dihapus saat akun dihapus.
- `ChatMsg` (hub & `GET /pare/inbox`) punya `kind: "text"|"voice"` dan, untuk voice, `voice: {id, duration_ms}`; `text` tetap terisi caption pendek ("🎙 Voice note") untuk klien lama.
- Retensi (ADR-0017 §5): audio + transkrip voice note dihapus persis 3 hari setelah dibuat (`content.json` → `voice.retentionDays`), lalu `status` jadi `expired` dan `GET .../audio` membalas 404 `voice_note_expired`. `services/pare_voice::purge_expired` melakukan ini per note (dipanggil manual/tes di P7-003; job berjadwal & hapus akun menyusul di P7-006).
- Blokir & laporan (P7-007, ADR-0017 §7): **blokir** menutup gerbang voice di dua arah (dicek `eligibility` dan `create_note`; undangan live P7-009 memakai gerbang yang sama, jadi pemain yang diblokir tak bisa mengundang). **Lapor** hanya untuk voice note (`live:<id>` menyusul P7-009): kutipan transkrip disalin ke laporan saat itu juga (transkrip aslinya hilang setelah 3 hari), pelapor otomatis **tidak bisa memutar** voice note terlapor 24 jam (403 `voice_muted` di `GET .../audio`), dan ≥ 3 pelapor berbeda terhadap pemain yang sama dalam 7 hari menandai (`flagged`) semua laporan terbukanya. Maks 20 laporan / 24 jam / pelapor.
- **Panggilan live (P7-009, ADR-0017 §2/§4):** media TIDAK lewat backend — backend hanya penjaga pintu dan penanda tangan token LiveKit. `POST /pare/voice/rooms` memeriksa **setiap anggota** percakapan, bukan hanya penelepon: persetujuan, kunci, blokir, sudah pernah menulis di percakapan, level ≥ `voice.liveMinLevel[lang]`, dan tidak menyenyapkan penelepon; satu saja gagal → 422 `live_not_eligible` dengan `detail` "@user: alasan; …". Token LiveKit: HS256 dengan API secret, **5 menit**, hanya untuk satu room (`pare-<session>`), izin `canPublish`/`canSubscribe` dan `canPublishSources: ["microphone"]`, **tanpa** data channel, kamera, atau hak admin room; `sub` = user id pemain. Maks 6 peserta (1 + `MAX_PRIVATE`).
- Undangan: pesan hub `{"t":"voice_invite","room","conversation","lang","from":{uid,name},"group","expires_in"}` ke yang online, Web Push (`pare_push::call`) ke yang offline; berdering 45 dtk. Habis waktu tanpa jawaban → sesi `missed` dan semua dapat `{"t":"voice_cancelled","room","reason":"missed"}`; ditolak semua → `reason:"declined"`; penelepon menutup saat berdering → `reason:"cancelled"`. **Satu panggilan per pemain**: penelepon yang masih di panggilan lain → 409 `already_in_call`; menjawab juga mengambil kunci itu.
- Webhook LiveKit → sesi: `participant_joined` (mengisi `joined_at`, sesi `active`), `participant_left` (`left_at`, kunci pemain lepas), `room_finished` (sesi `ended`, semua kunci & room di Redis dibersihkan); room di luar `pare-<uuid>` diabaikan. Konfigurasi lewat env `LIVEKIT_URL` (yang dipakai browser), `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`; tanpa itu live nonaktif (503). Verifikasi tanda tangan diuji terhadap LiveKit sungguhan (semua webhook dijawab 200).
- Tindakan moderator: `dismiss` (abaikan), `warn` (notice ke pemain bila online + tercatat), `lock` N hari (1–30; mengisi `pare_voice_locks`, gerbang `eligibility` langsung menolak). Kunci **tidak pernah dipendekkan**: kunci otomatis 24 jam dari penalti (P7-005) tidak menimpa kunci moderator yang lebih panjang. Setiap tindakan masuk `admin_audit_log`. Halaman: Admin Pusat → **Moderasi Suara** (`/admin/moderasi-suara` di titian-web).
- Job `pare_voice_purge` di `titian-worker` (tiap jam, P7-006) memanggil `purge_expired`; worker kini butuh env R2 yang sama dengan API (`JobContext.storage`). **Hapus akun (`DELETE /users/me`) adalah soft delete** (`users.deleted_at`), jadi `on delete cascade` ADR-0017 §5 tidak pernah jalan — `delete_me` memanggil `pare_voice::purge_user` secara eksplisit (audio di R2 + transkrip; baris note tetap sebagai `expired` karena `pare_messages` menunjuknya; strike/kunci tetap karena tak berisi suara). Bila storage gagal saat itu, akun tetap tertutup dan job per jam yang membersihkan sisanya (≤ 3 hari). Log sesi live > 1 tahun: belum ada tabelnya (P7-009 menambah pemangkasan ke job yang sama).

### Premium & iklan berhadiah (Pare-8, ADR-0018)
```
GET  /pare/premium            -> {active, tier: ""|"plus"|"pro", plan: ""|"plus"|"pro"|"plus_year"|"pro_year", until, unlimited_hearts, all_levels, free_exams, ad_free, voucher, plans: [{id, tier, name, period: "month"|"year", price_idr, list_price_idr, bonus_idr, saving_idr, period_days, benefits[], quote: {kind: "new"|"renew"|"upgrade"|"unavailable", pay_idr, credit_idr, reason?}}], voucher_until, price_idr, voucher_idr, period_days, boosts}   (2026-10-11: Plus Rp10.000 coret Rp40.000, Pro Rp30.000 coret Rp120.000, 30 hari; Plus Tahunan Rp99.000, Pro Tahunan Rp299.000, 365 hari. POST /pare/premium/checkout {plan} memakai quote.pay_idr: naik paket = harga baru − nilai sisa paket lama, paket baru mulai saat dibayar)
GET  /pare/wardrobe            -> {items: [{id: "slot:key", slot, key, name, tier: gratis|koin|plus|pro|toko, price?, lokal?, owned}], look3d: {...}|null, plan: ""|"plus"|"pro", money}   (Lemari 3D, ADR-0023/P10-008; katalog dari data/pare/wardrobe.json, diekspor `game/scripts/wardrobe.ts`)
POST /pare/wardrobe/buy        {item: "top:batik"} -> tier koin: 200 + seluruh view (uang game berkurang, barang jadi milik); tier toko: 201 + pesanan {kind: "pare_wardrobe", subscription_tier: item, ... , qris_payload} (dipantau lewat GET /orders/{id}; barang jadi milik saat lunas); tier lain 422 not_for_game_money; sudah punya 422 already_owned; uang kurang 422 insufficient_money
PUT  /pare/me/look3d           {style: kartun|blok|realis, skin, height 0.9-1.1, build, shoulders 0.85-1.2, eyes, hair, hairColor, head, headColor, top, topColor, dress, dressColor, bottom, bottomColor, shoes, shoesColor, bag, bagColor, acc[]} -> view; 422 item_not_owned bila ada barang yang belum dimiliki (gratis, dibeli, atau tercakup paket Plus/Pro yang berjalan); disiarkan ke pemain lain lewat frame `profile` (`look3d`) dan `PlayerInfo.look3d`
GET  /pare/me                  juga membawa `look3d` (null sampai pemain berdandan di 3D); `PlayerInfo.dummy` menandai keramaian server (P10-006)
PUT  /pare/me/engine           {engine: "pixel"|"3d"} -> PlayerView; 422 invalid_engine untuk nilai lain. Cara pemain memilih bermain (P11-002, migrasi 0105); `GET /pare/me` membawa `engine` (bawaan `pixel`). Dunia dan progres sama di keduanya.
POST /pare/pond/coin           {} -> {money, price: 500}; 422 insufficient_money bila uang < Rp500 (P11, 3D: lempar koin ke kolam, ledger kind `coin`). Akun baru dibuat dengan `engine = "3d"` (keputusan pemilik 2026-10-14); pemain lama tetap `pixel`.
POST /pare/reports             {kind: perf|error|context_lost, engine: pixel|3d, detail: {...≤2 KB}} -> 204; 422 invalid_report (jenis, tampilan, atau isi tidak valid/terlalu besar). Laporan diri game (P11-008): kecepatan per tingkat grafik, jenis layar dan kartu grafis, galat 3D. Batas 40 per pemain per jam; kelebihannya dibuang tanpa galat. Tanpa chat, posisi, atau teks pemain.
POST /pare/premium/checkout   {tier: "plus"|"pro"} -> {id, kind: "pare_premium", subscription_tier, amount_idr, status: "pending", payment_id, payment_total_idr, payment_meta: {qr_url, qr_image, payment_url, expires_at}, qris_payload}
                               (order paket pending lama ditutup 'failed'; 422 already_pro untuk Plus saat Pro aktif; 503 payments_unavailable tanpa gateway)
GET  /orders/{id}             -> order; saat pending dan webhook belum datang, server menanyakan BuatQris (maks. 1×/20 dtk) lalu melunasi/menutup
POST /payments/{provider}/webhook  (publik; hanya untuk gateway yang sedang dipakai, diverifikasi tanda tangan gateway itu. BuatQris: X-BuatQris-Signature: sha256=HMAC body mentah; is_test harus cocok; total_amount >= yang ditagih; idempoten)
POST /payments/{payment_id}/webhook  (hanya untuk stub dev: payment_id "stub_…" dan PAYMENT_PROVIDER=stub)
GET  /pare/info               -> {items: [{id, kind: progres|sistem|promo|nyawa, icon, title, body, action: {label, target: path|plans|missions|profile|earn}|null, at, read}], unread}
POST /pare/info/read          {ids: [...]} -> papan Info terbaru
GET  /pare/path/{lang}?level=N  -> jalur level lain (hanya Pro; selain itu 403 level_locked); respons + own_level, all_levels. Pro: tidak ada langkah atau misi berstatus `locked`. Respons memuat `complete` (false selama jalur dan misi bahasa itu belum lengkap: semua selain `en`, `CompleteLanguages`).
Nyawa (2026-10-11): /pare/me dan setiap jawaban (papers/answers, missions/{id}/steps) membawa hearts, hearts_refill_at; papers/answers + out_of_hearts. Sesi (kecuali ujian) dan misi menolak 403 no_hearts saat nyawa 0 (Plus/Pro tidak pernah habis).
GET  /orders/{id}             -> order milik sendiri (FE memantau sampai "paid")
POST /payments/{payment_id}/webhook   -> mengaktifkan Premium (idempoten per order; aktif = +30 hari)  ⚠️ publik tanpa tanda tangan — P8-005 wajib sebelum produksi
POST /pare/boosts {kind: heart|rescue|double_pay, ref?}   -> {id, kind, needs_ad, min_seconds, expires_at}
POST /pare/boosts/{id}/claim  -> {message, player}
        422 boost_not_needed | boost_limit (3×/hari WIB per jenis) | ad_not_finished (< 15 dtk) | boost_expired (> 10 mnt) | invalid_kind | invalid_ref | premium_no_double_pay ; 409 boost_claimed
```
- `PlayerView.premium = {active, until, voucher, ad_free}`. `ad_free` = Premium Pare aktif **atau** langganan Titian aktif (Titian: tanpa voucher).
- Belanja hidup (`/pare/shop/buy`, `/laundry`, `/bike`) memakai **voucher dulu, lalu uang**; ledger `spend` mencatat `delta_money` dan `delta_voucher`. Ujian hanya uang.
- `heart`: nyawa ≤ 1 → +½. `rescue`: ≤ 10 menit setelah pingsan & masih di Camp → kembali ke zona/posisi pingsan (FE harus memindahkan pemain ke sana). `double_pay`: kertas milik sendiri yang selesai ≤ 10 menit lalu, uang > 0, sekali per kertas, bukan untuk Premium Pare → +uang yang sama. Semua hadiah di ledger `boost`.

---

## Health

### `GET /health`
```
Response 200: { "status": "ok", "db": "ok", "redis": "ok" }
```
