# Phase 12 (ticket-numbering) — Marketplace Lanjutan (roadmap-Fase 8 sisa)

## Keputusan scope (baca duluan)

Item ke-3 dari 4 roadmap-Fase yang diminta user berurutan (2026-09-02):
5.3 (Phase 10) → 6.9-16 (Phase 11) → **8 sisa (ini)** → 9.

`docs/tickets/phase-9.md`'s "Keputusan scope" sudah mendaftar §8.1/8.2/
8.6/8.7/8.9-11 sebagai di luar scope Phase 9 dengan alasan masing-masing
— ticket-phase ini mengambil sisa itu, dipotong MVP lagi (sama disiplin
tiap fase sebelumnya), bukan dibangun sekaligus penuh.

**Riset kunci sebelum motong scope**:
- **§8.14 (Cancellation Policy) TERNYATA CUMA SETENGAH selesai di Phase
  9** — `POST /enrollments/{id}/cancel` (P9-007) HANYA jalur SISWA yang
  cancel (`ctx.userId === enrollment.studentId`, dicek langsung di
  kode). Separuh lain sumbernya sendiri ("Tutor cancellation: siswa
  full refund; repeated cancellation → tutor kena penalty") **tidak
  pernah dibangun, dan tidak eksplisit dicatat sebagai deferred** di
  `phase-9.md` — gap nyata, bukan exclusion sadar. Ditambal di sini.
- **§8.9 (Tutor Reputation) sebagian besar sudah computable dari data
  yang ADA** (jumlah siswa/lesson dari `enrollments`, completion% dari
  `enrollments.status`, cancellation% dari P12-001 di atas) — cuma
  "Rating" yang butuh input BARU (review/rating dari siswa, belum ada
  jalur sama sekali). "Response time <1 jam" butuh sistem messaging
  yang TIDAK ADA di proyek ini — didefer eksplisit, bukan dipaksa jadi
  angka palsu.
- **§8.6 (Assignment) "AI Evaluation" TIDAK di-reuse literal dari
  `ai_writing_evaluation_service.runWritingEvaluation`** — fungsi itu
  terikat erat ke `attempts.id` (FK NOT NULL ke tabel `attempts`,
  bagian alur lesson/assessment formal), Assignment adalah entitas
  beda (tutor-created, cohort-scoped, deadline) yang tidak alami masuk
  ke situ tanpa memaksakan skema. **Keputusan: MVP ticket ini scope ke
  submission + tutor grading manual (skor+feedback) dulu** — evaluasi
  AI otomatis didefer eksplisit sebagai peningkatan terpisah, BUKAN
  fitur setengah-jadi yang diklaim selesai (submission tanpa skor sama
  sekali TIDAK berguna, jadi manual grading yang dipastikan solid
  duluan, bukan AI yang setengah-jalan).
- **§8.1 (marketplace 8 kategori) sebagian besar butuh infra yang
  tidak ada**: Live Class (video-conference integration), Bootcamp
  (aturan jadwal intensif), Kids Course (Kids Mode, sudah eksplisit di
  luar scope beberapa fase). Self-paced Course lebih dekat — tapi tetap
  butuh keputusan desain baru (materi self-paced tanpa cohort/jadwal)
  yang belum ada precedent-nya. **Didefer penuh** ticket-phase ini,
  bukan dipaksa jadi 1 tipe baru yang tanggung.
- **§8.2 (tutor dashboard lengkap) sebagian besar kerja agregasi
  FRONTEND** (`titian-web`) di atas endpoint yang SUDAH ADA — "Messages"
  butuh sistem messaging yang tidak ada. Sesi ini backend-focused sejak
  Phase 7 (FE cuma disentuh untuk gap nyata/rebrand kecil) — didefer,
  dicatat sebagai kandidat FE terpisah.
- **§8.10 (Student Diagnosis) SENGAJA TIDAK DIKERJAKAN — bukan cuma
  discope, tapi TIDAK DITANYAKAN ke user juga di sesi ini**. Sumbernya
  sendiri eksplisit: *"Perlu aturan privasi/consent eksplisit siapa
  yang boleh lihat data ini — bukan default semua tutor lihat semua
  data student."* Ini keputusan kebijakan privasi, bukan keputusan
  arsitektur — di luar kewenangan dipotong MVP begitu saja. Didefer
  eksplisit dengan alasan ini dicatat tebal di `docs/STATE.md`, bukan
  ditanyakan sekarang supaya tidak menghentikan urutan 4 item yang
  sudah diminta user — tapi TIDAK BOLEH dibangun tanpa keputusan
  eksplisit user kapan pun nanti dikerjakan.
- **§8.11 (Learning Package) mekanisme "N sesi, redeem satu-satu di
  masa depan" genuinely rumit** (butuh tracking sesi terpakai per
  enrollment, beda dari 1 produk = 1 booking yang ada sekarang) —
  didefer penuh sebagai ticket tersendiri nanti, bukan MVP yang
  setengah-jadi (paket yang dijual tapi sesinya tidak bisa di-track
  worse daripada tidak ada fitur sama sekali).

**Keputusan pemotongan MVP (scope ticket-phase ini)**:
- **P12-001 — Tutor-initiated cancellation (§8.14, nutup gap Phase 9)**
- **P12-002 — Assignment (§8.6, MVP: submission + tutor grading manual, AI eval didefer eksplisit)**
- **P12-003 — Gradebook (§8.7)**
- **P12-004 — Tutor Reputation Score (§8.9, minus response-time)**
- **P12-005 — Integration test suite + exit checkpoint**

**Dieksplisit DIDEFER, bukan didiamkan**: §8.1 (marketplace 8 kategori
penuh — Live Class/Bootcamp/Kids Course butuh infra tidak ada), §8.2
(tutor dashboard FE lengkap), §8.10 (Student Diagnosis — **butuh
keputusan privasi/consent eksplisit dari user SEBELUM dikerjakan sama
sekali, bukan cuma dipotong MVP**), §8.11 (Learning Package — mekanisme
redeem-sesi genuinely rumit, ticket tersendiri).

Tidak ada ADR baru — ADR-0005/0006 sudah cukup buat semua ticket di
atas (wallet/RBAC pattern reuse, bukan desain baru).

## Ticket

### P12-001 — Tutor-initiated cancellation (§8.14)
**Status:** done
**Depends on:** P9-007 (`order_service`, `POST /enrollments/{id}/cancel` yang sudah ada — jalur siswa)
**Endpoint baru:** `POST /cohorts/{id}/enrollments/{enrollment_id}/tutor-cancel`.
**Deskripsi:** Separuh §8.14 yang belum ada — tutor batalkan enrollment siswa (bukan siswa batalkan sendiri). Beda kebijakan dari cancel siswa: SELALU full refund ke siswa (tidak peduli waktu, siswa tidak salah), dan setiap tutor-cancel dicatat buat P12-004's cancellation-rate metric.
**Acceptance Criteria:**
- [x] `POST /cohorts/{id}/enrollments/{enrollment_id}/tutor-cancel` — auth reuse `canManageCohorts` (pola sama semua endpoint cohort-management P9-004/005/006/008)
- [x] Kalau `orders.status = paid`: SELALU full refund (100%, tidak ada tingkat waktu seperti cancel siswa) — `transactions.type=refund` ke siswa, `orders.status=refunded`. Kalau `pending`: `orders.status=failed`. Kalau belum ada order: langsung `cancelled`
- [x] `enrollments.status = cancelled`, DAN ditandai `cancelled_by = 'tutor'` (kolom baru, beda dari cancel siswa yang `cancelled_by = 'student'` — dibutuhkan P12-004 buat hitung cancellation rate KHUSUS tutor, bukan gabung sama pembatalan siswa)
- [x] TIDAK reverse `payout_earned` tutor yang sudah dibayarkan (sama keterbatasan eksplisit P9-007, bukan baru)
**DoD:** test backend baru — tutor cancel enrollment yang sudah paid <6 jam sebelum mulai → TETAP full refund (beda dari cancel siswa yang di titik ini dapat 0%); siswa TIDAK BISA memanggil endpoint ini (403); `enrollments.cancelled_by` benar buat kedua jalur (siswa vs tutor).

**Catatan implementasi:** `enrollment_repository.cancel(db, id, cancelledBy)` set `status` dan `cancelled_by` dalam 1 UPDATE. `order_service.tutorCancelEnrollment` validasi `enrollment.cohortId === cohortId` (defense-in-depth, pola sama `completeEnrollment` P9-008) sebelum auth `canManageCohorts`. 3 test baru di `tests/order.test.ts` (always-full-refund-even-<6h, student-cannot-call → 403, `cancelled_by` benar buat kedua jalur).

### P12-002 — Assignment (§8.6, MVP: submission + tutor grading manual)
**Status:** done
**Depends on:** P9-004 (`cohorts`), P9-001 (`canManageCohorts`)
**Endpoint baru:** `POST /cohorts/{id}/assignments`, `GET /cohorts/{id}/assignments`, `POST /assignments/{id}/submissions`, `POST /submissions/{id}/grade`.
**Deskripsi:** Tutor bikin assignment (title/description/deadline) per cohort, siswa submit teks, tutor kasih skor+feedback manual. Evaluasi AI otomatis DIDEFER eksplisit (lihat "Keputusan scope") — submission tanpa skor sama sekali tidak berguna, jadi manual grading yang solid dulu.
**Acceptance Criteria:**
- [x] Migrasi: `assignments` (`id`, `cohort_id` FK, `title`, `description`, `deadline` nullable) + `assignment_submissions` (`id`, `assignment_id` FK, `student_id` FK, `content` text, `submitted_at`, `score` nullable, `feedback` nullable, `graded_at` nullable, `graded_by` nullable FK users)
- [x] `POST /cohorts/{id}/assignments` — auth `canManageCohorts`
- [x] `GET /cohorts/{id}/assignments` — auth: tutor/org-admin lihat semua, siswa yang terenroll lihat daftar assignment (bukan gerbang seketat manage)
- [x] `POST /assignments/{id}/submissions` — auth: siswa yang terenroll di cohort assignment itu; idempotent kalau submit ulang (update `content`+`submitted_at`, bukan baris baru) SELAMA belum di-grade; submit setelah `deadline` tetap diterima tapi ditandai (`late: boolean` computed dari `submitted_at > deadline`, bukan kolom tersimpan)
- [x] `POST /submissions/{id}/grade` — auth `canManageCohorts`; `{score, feedback}`, set `graded_at`/`graded_by`
**DoD:** test backend baru — tutor bikin assignment, siswa submit, submit ulang sebelum deadline update bukan duplikat; submit setelah deadline diterima tapi `late: true`; tutor grade → skor tersimpan; siswa lain (tidak terenroll) tidak bisa submit (403); siswa tidak bisa grade punya sendiri.

**Catatan implementasi:** `submitAssignment` throw `AppError.conflict("submission_already_graded")` kalau `existing.gradedAt !== null` — upsert-before-grading, bukan upsert selamanya. `computeLate` murni fungsi (bandingkan `submittedAt`/`deadline`), tidak ada kolom `late` tersimpan. 9 test baru di `tests/assignment.test.ts`.

### P12-003 — Gradebook (§8.7)
**Status:** done
**Depends on:** P12-002 (assignment scores), P9-005 (attendance), Assessment Engine (Phase 1/7, skor assessment)
**Endpoint baru:** `GET /cohorts/{id}/gradebook`.
**Deskripsi:** Rekap per siswa: attendance%, rata-rata skor assignment, overall — agregasi murni, TIDAK menyentuh mastery engine (sengaja terpisah, sumbernya sendiri eksplisit: "nilai akademik dan mastery engine disimpan terpisah, keduanya mengukur hal beda").
**Acceptance Criteria:**
- [x] `GET /cohorts/{id}/gradebook` — auth `canManageCohorts` (rekap PENUH, bukan per-siswa sendiri — beda dari pola "siswa lihat baris sendiri" endpoint lain, karena gradebook memang tutor-facing per definisi §8.7)
- [x] Per siswa: `attendance_percent` (present / total sesi tercatat × 100, dari `attendance_records` P9-005), `assignment_average` (rata-rata `score` dari submission yang sudah di-grade, null kalau belum ada yang di-grade), `overall` (rata-rata sederhana dari attendance% + assignment_average, null-aware — kalau salah satu null, overall dihitung dari yang ada saja, bukan dianggap 0)
**DoD:** test backend baru — cohort dengan 2 siswa, attendance+assignment berbeda, `GET /gradebook` balikin angka yang benar per siswa; siswa yang belum pernah di-grade assignment apapun → `assignment_average: null`, bukan 0; non-tutor/non-admin ditolak 403.

**Catatan implementasi:** Roster gradebook = `ACTIVE_ROSTER_STATUSES = {active, completed}` — enrollment `pending`/`cancelled` tidak muncul sama sekali (bukan baris dengan nilai 0). 2 test baru di `tests/gradebook.test.ts`.

### P12-004 — Tutor Reputation Score (§8.9, minus response-time)
**Status:** done
**Depends on:** P9-004 (`enrollments`), P12-001 (`cancelled_by` buat cancellation rate akurat)
**Endpoint baru:** `POST /tutors/{id}/reviews`, `GET /tutors/{id}/reputation`.
**Deskripsi:** Rating (baru, dari siswa) + statistik yang sudah computable dari data existing. "Response time" (butuh sistem messaging) DIDEFER eksplisit — tidak dipaksa jadi angka palsu.
**Acceptance Criteria:**
- [x] Migrasi: `tutor_reviews` (`id`, `tutor_id` FK, `student_id` FK, `enrollment_id` FK unique — 1 review per enrollment yang SUDAH `completed`, cegah review sebelum benar-benar belajar, `rating` CHECK 1-5, `comment` nullable)
- [x] `POST /tutors/{id}/reviews` — auth: siswa yang enrollment-nya (`enrollment_id` di body) `status=completed` DAN `student_id=ctx.userId`; 1x per enrollment (re-submit sebelum ini ditolak 409, bukan update — beda dari assignment yang boleh update sebelum grade, karena review medium orang lain bergantung ke situ begitu terbit)
- [x] `GET /tutors/{id}/reputation` — publik (siapa saja authenticated, pola sama `GET /tutors/{id}/products`): `average_rating` (null kalau 0 review), `review_count`, `student_count` (distinct `student_id` dari `enrollments` yang pernah `active`/`completed` di cohort tutor itu), `lesson_count` (COUNT `attendance_records.status='present'` di seluruh cohort tutor itu), `completion_rate` (`completed` / (`completed`+`cancelled`) enrollment), `cancellation_rate` (enrollment `cancelled_by='tutor'` / total enrollment tutor itu, dari P12-001)
**DoD:** test backend baru — siswa review setelah enrollment completed → masuk hitungan `average_rating`; review 2x buat enrollment sama → 409; siswa yang enrollment-nya belum completed tidak bisa review; tutor dengan beberapa tutor-cancel (P12-001) → `cancellation_rate` mencerminkan itu, BUKAN tercampur dengan cancel siswa.

**Catatan implementasi:** `reputation_repository.getStats` — semua angka dihitung on-read (join `enrollments`→`cohorts`→`learning_products` filter `tutor_id`), tidak ada tabel agregat baru selain `tutor_reviews` sendiri. `completion_rate` denominator = `completed+cancelled` saja (enrollment `pending`/`active` belum resolve, tidak dihitung understate). `cancellation_rate` denominator = SEMUA enrollment tutor itu (bukan cuma yang sudah final), numerator cuma `cancelled_by='tutor'`. 3 test baru di `tests/tutor-reputation.test.ts`.

### P12-005 — Integration test suite + exit checkpoint
**Status:** done
**Depends on:** P12-001 s/d P12-004
**Deskripsi:** Pola sama tiap ticket-phase sebelumnya — route-coverage audit, checkpoint end-to-end yang menyatukan tutor-cancel → assignment+grading → gradebook → review+reputation dalam 1 alur nyata.
**Acceptance Criteria:**
- [x] Route-coverage audit (`grep`-based, pola P2-017/.../P11-005)
- [x] Checkpoint baru: 1 cohort dengan 2 siswa — siswa A diselesaikan penuh (attendance+assignment+completed+review), siswa B di-tutor-cancel sebelum selesai; assert `GET /cohorts/{id}/gradebook` benar buat siswa A, `GET /tutors/{id}/reputation` mencerminkan 1 review DAN 1 tutor-cancellation (cancellation_rate > 0)
**DoD:** `bun test` hijau penuh di `titian-backend-bun` (lokal — CI masih P0-010 yang tertunda).

**Catatan implementasi:** Route-coverage audit: 110/110 routes, 0 gap. `tests/phase12-checkpoint.test.ts` — B (tutor-cancelled) hilang total dari gradebook roster (bukan baris bernilai 0), reputation A tercermin (`average_rating: 5`, `review_count: 1`) berdampingan dengan `cancellation_rate > 0` dari B tanpa saling mencampur. Final: 447/447 test lulus (naik dari 443 sebelum Phase 12).

---

## Checkpoint keluar Phase 12 (harus bisa didemo, bukan asumsi)
1. [x] Tutor-cancel terbukti SELALU full refund (beda dari cancel siswa yang tingkatan waktu) — dites eksplisit di skenario <6 jam yang buat siswa 0% tapi buat tutor tetap 100%.
2. [x] Assignment: submission → grading manual → skor tersimpan, jalur late-submission dites eksplisit.
3. [x] Gradebook menggabungkan attendance+assignment dengan benar, null-aware (bukan 0 palsu buat data yang belum ada).
4. [x] Tutor Reputation: rating cuma bisa dari enrollment completed (bukan sembarangan), cancellation_rate KHUSUS tutor-initiated (tidak tercampur cancel siswa) — dites eksplisit.
5. [x] Semua yang dideferred (§8.1/8.2/8.10/8.11) tercatat eksplisit di sini dan `docs/STATE.md`, **§8.10 secara khusus dicatat butuh keputusan privasi/consent user SEBELUM dikerjakan, bukan cuma "nanti"**.

Phase 12 tertutup: 447/447 test, 110/110 routes/0 gap. Lanjut ke roadmap-Fase 9 (Proctoring — item terakhir yang diminta user).
