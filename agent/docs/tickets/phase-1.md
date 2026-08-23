# Phase 1 — Backend Core
Target: 4–6 minggu. Depends on: Phase 0 checkpoint terpenuhi penuh.

---

### P1-001 — Auth: Google OAuth + JWT
**Status:** done
**Depends on:** P0-007, P0-008
**Endpoint:** `POST /auth/google/callback`, `POST /auth/refresh`
**Acceptance Criteria:**
- [x] Verifikasi `id_token` Google server-side (jangan percaya token dari client tanpa verifikasi) — `GoogleTokenVerifier` (titian-backend/src/service/google_oauth.rs) fetch JWKS Google, verifikasi signature RS256 + `aud` + `iss` + `exp` lewat `jsonwebtoken`, bukan cuma decode tanpa cek.
- [x] Buat/lookup `users` row berdasarkan `google_id`/`email` — `auth_service::google_callback`: cari by `google_id` dulu, fallback cari by `email` lalu link `google_id`-nya, baru insert baru kalau dua-duanya tidak ketemu.
- [x] Issue access token (short-lived, ~15 menit) + refresh token (long-lived) — access token JWT HS256 (`ACCESS_TOKEN_TTL_MINUTES=15`), refresh token opaque random 32-byte disimpan **hashed** (SHA-256) di tabel baru `refresh_tokens` (`REFRESH_TOKEN_TTL_DAYS=30`).
- [x] `/auth/refresh` menolak refresh token expired/revoked — `auth_repository::find_valid_by_hash` cuma return row kalau `revoked_at IS NULL AND expires_at > now()`.
**DoD:** integration test untuk happy path + token invalid + token expired — **11 test, semua lulus** (`titian-backend/tests/auth_test.rs`): verifikasi Google id_token (happy path, expired, wrong audience, malformed — pakai keypair RSA test lokal karena JWKS Google asli tidak bisa dites di CI), user upsert (create baru, link google_id ke email existing), refresh (issued token valid, expired, revoked, tidak pernah ada), plus 1 test HTTP end-to-end lewat route asli (`POST /auth/refresh`) yang mengecek response error match `api-contract.md`.
**Catatan implementasi:**
- Tabel baru `refresh_tokens` ditambahkan (tidak ada di ADR-0001 asli) — additive, tidak ubah tabel yang sudah ada, sinkron ke `docs/domain-model.md`. Lihat "Deviasi" di `docs/STATE.md`.
- `titian-backend` dipecah jadi `lib.rs` + `main.rs` tipis supaya `tests/*.rs` bisa import modul internal dan build router asli buat test HTTP-level — bukan scope creep, murni supaya "integration test" di DoD bisa benar-benar jalan.
- Kredensial Google OAuth ada di `google-auth.md` (root `alr/`, gitignored). Backend cuma butuh **client ID** (buat validasi `aud`), bukan client secret — flow ini nerima `id_token` yang sudah didapat frontend lewat Google Identity Services, bukan authorization-code exchange.

### P1-002 — User & Profile + user_organization_roles
**Status:** done
**Depends on:** P1-001
**Endpoint:** `GET /users/me`, `GET /organizations/{id}/members`
**Acceptance Criteria:**
- [x] `/users/me` mengembalikan semua role user lintas organisasi — `handler/user_handler.rs::get_me`, query `user_organization_roles` tanpa filter org.
- [x] `/organizations/{id}/members` hanya bisa diakses role sesuai matrix ADR-0006 — `service/permissions.rs::require_permission`, const map per `(Resource, Action)`, `platform_admin` bypass scoping org sesuai ADR-0006.
- [x] Middleware `AuthContext` (user_id, organization_id, role) terpasang dan dipakai endpoint ini sebagai referensi untuk endpoint berikutnya — `middleware/auth_context.rs`, sebagai axum extractor (`FromRequestParts<AppState>`) bukan tower layer, jadi handler baru tinggal ambil `ctx: AuthContext` sebagai parameter. Resolve org aktif dari header `X-Organization-Id`, fallback ke org pertama user kalau header tidak dikirim.
**DoD:** test mencakup akses ditolak (403) untuk role yang tidak berhak — **7 test, semua lulus** (`titian-backend/tests/user_organization_test.rs`): `/users/me` happy path (role lintas 2 org) + tanpa token + token rusak; `/organizations/{id}/members` untuk org_owner (200), role tanpa izin (403), org mismatch — role valid tapi di org lain (403), dan `platform_admin` yang boleh akses org manapun tanpa `X-Organization-Id` cocok (200).
**Catatan implementasi:**
- `organization_repository::list_members` pakai keyset pagination beneran (cursor = `user_id` terakhir), bukan cuma `next_cursor: null` palsu — sesuai aturan pagination di `api-contract.md`.
- Multi-role per org (constraint DB `UNIQUE(user_id, organization_id, role)` mengizinkan lebih dari 1 role per user per org) disederhanakan: `AuthContext.role` cuma ambil 1 row (yang paling awal dibuat). Kalau nanti ada kebutuhan union multi-role, itu perlu penyesuaian, dicatat sebagai simplifikasi yang disengaja, bukan bug.
- `service/permissions.rs` baru punya 1 entry (`OrganizationMembers::View`) — struktur const map disiapkan supaya tiket berikutnya (P1-003 dst) tinggal nambah varian `Resource`, bukan bikin pola baru.

### P1-003 — Content API (read)
**Status:** done
**Depends on:** P1-002
**Endpoint:** `GET /curricula/{id}/tree`, `GET /lessons/{id}`
**Acceptance Criteria:**
- [x] Tree mengembalikan struktur level→unit→lesson sesuai `api-contract.md` — `service/content_service.rs::get_curriculum_tree`, 3 query total (levels, lalu semua unit-nya, lalu semua lesson-nya), bukan N+1 per level/unit.
- [x] Lesson yang belum published tidak bisa diakses student (403), tapi bisa oleh curriculum_developer/reviewer/admin — error code spesifik `lesson_not_published` (bukan `forbidden` generik), lihat `permissions::is_allowed`.
- [x] Perlu data seed minimal (1 curriculum, 1 level, 1 unit, 2 lesson) untuk testing manual — `titian-backend/seed.sql` (idempotent, id tetap, aman dijalankan ulang). Dites manual lewat curl end-to-end sesi ini, hasilnya cocok kontrak persis.
**DoD:** endpoint tervalidasi dengan seed data, test permission per role — **6 test** di `tests/content_and_question_test.rs` (bagian tree+lesson): happy path tree, curriculum tidak ketemu (404), lesson published ke student (200), lesson draft ke student (403 `lesson_not_published`), lesson draft ke curriculum_developer (200), lesson tidak ketemu (404).
**Catatan:** endpoint tree sengaja tidak menyaring lesson draft dari struktur tree (semua lesson tetap muncul dengan field `status`-nya) — cuma akses langsung ke `/lessons/{id}` yang diblokir. AC tidak minta penyaringan di level tree, jadi ini bukan bug, cuma scope yang lebih sempit dari yang mungkin diasumsikan.

### P1-004 — Question Bank API
**Status:** done
**Depends on:** P1-002
**Endpoint:** `POST /question-banks/{id}/questions`, `GET /question-banks/{id}/questions`
**Acceptance Criteria:**
- [x] Validasi schema `data`/`correct_answer` per `type` di application layer (minimal untuk `mcq` dan `fill_blank` dulu) — `service/question_schema.rs`. Tipe lain ditolak eksplisit (`invalid_question_schema`), bukan diloloskan diam-diam.
- [x] Question baru selalu `status = draft` — di-hardcode di `question_repository::insert`, bukan diambil dari request.
- [ ] Alur publish (draft → in_review → published) — **belum dikerjakan, sesuai catatan asli tiket ini ("bisa ticket terpisah: P1-004b")**. Ticket P1-004b belum dibuat di file ini — tambahkan kalau mau digarap.
**DoD:** test create MCQ valid, create dengan schema salah (422), publish oleh role salah (403) — **5 test** di `tests/content_and_question_test.rs` (bagian question): create mcq valid (201, draft), create fill_blank valid, schema salah (422 `invalid_question_schema`), role tanpa izin (403) — **catatan: DoD asli minta test publish ditolak role salah, tapi endpoint publish belum ada (lihat AC di atas), jadi yang dites adalah create ditolak role salah sebagai padanan paling dekat** — dan list setelah create menunjukkan item yang baru dibuat.
**Catatan implementasi:**
- `question_repository::list_by_bank` pakai keyset pagination beneran (cursor = `id` terakhir), sama seperti pola `organization_repository::list_members`.
- `service/permissions.rs` dipecah jadi `require_permission` (role-only, buat resource yang tidak terikat 1 organisasi — `curricula`/`question_banks` memang tidak punya kolom `organization_id` di `domain-model.md`, jadi platform-wide) dan `require_permission_in_org` (tambah cek org match, dipakai `/organizations/{id}/members`). `is_allowed` jadi fungsi murni bool supaya bisa dipakai ulang buat kasus yang butuh kode error custom (`lesson_not_published`) tanpa duplikasi daftar role.

### P1-005 — Assessment API
**Status:** done
**Depends on:** P1-003, P1-004
**Endpoint:** `GET /assessments/{id}`, `POST /assessments/{id}/attempts`
**Acceptance Criteria:**
- [x] `POST attempts` membuat attempt baru dan mengirim daftar soal (tanpa `correct_answer` di response!) — `service/assessment_service.rs::CreateAttemptResponse`/`AttemptQuestion` struct-nya secara struktural tidak punya field `correct_answer` sama sekali (bukan cuma di-skip pas serialize), jadi tidak mungkin bocor.
- [x] Kalau user sudah punya attempt `in_progress` untuk assessment yang sama → 409 dengan `attempt_id` existing, bukan bikin baru — `AppError::AttemptAlreadyInProgress(Uuid)`, response shape custom `{error, attempt_id}` (beda dari envelope `{error, detail}` standar, sesuai kontrak).
**DoD:** test memastikan `correct_answer` tidak pernah bocor di response manapun sebelum submit — test `create_attempt_never_leaks_correct_answer` cek string mentah response HTTP-nya tidak mengandung kata "correct_answer" sama sekali, bukan cuma cek field per field.
**Catatan:** endpoint attempt (create & submit) dibatasi role `student`/`platform_admin` saja, sesuai matrix ADR-0006 ("Attempt: submit ✅ milik sendiri" — cuma student yang dicentang). `assessments`/`attempts` tidak punya kolom `organization_id` di `domain-model.md`, jadi pakai `require_permission` (role-only), bukan `require_permission_in_org`.

### P1-006 — Attempt Submission + Scoring Dasar
**Status:** done
**Depends on:** P1-005
**Endpoint:** `POST /attempts/{id}/submit`
**Acceptance Criteria:**
- [x] Auto-grading untuk tipe `mcq` dan `fill_blank` (exact/normalized match) — `service/grading.rs`, murni & sudah ada 4 unit test sendiri (`mcq` exact index, `fill_blank` trim+lowercase, tipe tak dikenal selalu salah).
- [x] Tipe soal yang butuh AI evaluation (writing/speaking) di-skip dari auto-score, status attempt tetap `submitted` menunggu evaluasi (bukan `evaluated`) — `grading::is_auto_gradable` cuma `true` untuk `mcq`/`fill_blank`; soal tipe lain tidak masuk hitungan `points_possible`/`points_earned` sama sekali, dan status yang di-set selalu `'submitted'`, tidak pernah `'evaluated'` (belum ada kode yang menulis `'evaluated'` di codebase ini).
- [x] Submit kedua untuk attempt yang sama → 409 — cek `attempt.status != "in_progress"` sebelum grading apapun.
- [x] Jawaban kurang dari total soal wajib → 422 dengan daftar `missing` — `AppError::MissingRequiredAnswers(Vec<String>)`, response shape custom `{error, missing}`.
**DoD:** test mencakup submit lengkap, submit sebagian, submit ganda — **10 test** di `tests/assessment_test.rs` (P1-005+P1-006 gabung, karena satu alur): GET assessment (found/404), create attempt (tidak bocor `correct_answer`, tolak duplikat in-progress, tolak role bukan student), submit (semua benar→100, sebagian salah→33.3, jawaban kurang→422 dengan `missing` yang benar, submit ganda→409, submit oleh yang bukan pemilik attempt→403). Plus verifikasi manual end-to-end lewat curl pakai `seed.sql` (assessment 3 soal MCQ) — hasil cocok kontrak persis, termasuk `missing` array-nya.
**Catatan implementasi:**
- Skor dihitung cuma dari soal yang auto-gradable (`mcq`/`fill_blank`) — kalau assessment punya soal writing/speaking, soal itu tidak masuk pembilang *maupun* penyebut skor. Ini disengaja buat "Scoring Dasar" (basic) — begitu AI evaluation beneran ada (Phase 4), kemungkinan skor perlu dihitung ulang/gabungan, bukan asumsi final.
- ~~`learning_events_created` di response submit di-hardcode `0`~~ — **selesai di P1-007**, sekarang diisi count asli. Jalur submit→learning_events→masteries→frss_schedule (checkpoint keluar Phase 1 poin 4) siap disambung P1-008/P1-009.
- Ownership check ("milik sendiri", ADR-0006) buat submit pakai `AppError::Forbidden` (403) generik, bukan `NotFound` — dipertimbangkan pakai 404 supaya tidak bocor keberadaan attempt orang lain, tapi dipilih konsisten sama pola `Forbidden` yang sudah dipakai di tempat lain di codebase ini.

### P1-007 — Learning Event Writer
**Status:** done
**Depends on:** P1-006
**Deskripsi:** Setiap submit attempt memicu 1 `learning_event` per question (event_type=`question_answered`) — bukan 1 event per attempt, supaya mastery per-concept bisa dihitung granular.
**Acceptance Criteria:**
- [x] Event tercatat dengan payload minimal `{ correct: bool|float, difficulty: float, question_id, concept_ids }` — `repository/learning_event_repository.rs::insert_many`, payload dibangun di `assessment_service::submit_attempt` di loop grading yang sama (tidak query ulang soal), `correct` bertipe `Option<bool>` (`None`/JSON `null` untuk tipe non-auto-gradable kayak writing/speaking — tetap tercatat sebagai event, cuma belum ada nilai benar/salah).
- [x] Jumlah event yang dibuat = jumlah soal dijawab (dicek lewat `learning_events_created` di response submit) — `learning_events_created` sekarang diisi count asli dari `insert_many` (bukan hardcode 0 lagi, lihat catatan P1-006 di bawah yang sudah diperbarui).
**DoD:** test memverifikasi jumlah row `learning_events` setelah submit sesuai jumlah soal — **2 test baru** di `tests/assessment_test.rs` (total assessment test jadi 12, total keseluruhan 45): `submit_writes_one_learning_event_per_question` (submit 3 jawaban, cek `learning_events_created == 3` di response DAN query langsung `SELECT COUNT(*)` di tabel `learning_events` juga 3 — dua sumber kebenaran independen), `submit_learning_event_payload_reflects_correctness_and_concepts` (seed 1 concept + link ke 1 soal lewat `question_concepts`, submit campuran benar/salah, cek `payload["correct"]` per soal dan `payload["concept_ids"]` isinya id concept yang benar).
**Catatan implementasi:**
- `question_repository::find_concept_ids_for_questions` (baru) ambil semua `question_concepts` buat sekumpulan `question_id` sekaligus (1 query pakai `= ANY($1)`), bukan N+1 per soal.
- Verifikasi manual end-to-end lewat curl pakai `seed.sql` (assessment 3 soal MCQ, "Unit 1 Quiz"): submit 2 benar + 1 salah → response `{"score":66.7,"learning_events_created":3}`, lalu query langsung ke tabel `learning_events` konfirmasi 3 row dengan `correct: true/false` yang cocok per soal dan `concept_ids: []` (soal seed belum di-link ke concept manapun — sesuai, karena `seed.sql` memang belum punya data `concepts`/`question_concepts`).
- Insert masih 1 row per `INSERT` di dalam loop (bukan multi-row `UNNEST`) — jumlah event per attempt dibatasi jumlah soal dalam 1 assessment (puluhan paling banyak), belum perlu optimasi batch.

### P1-008 — Mastery Calculator v1
**Status:** done
**Depends on:** P1-007
**Endpoint:** `GET /mastery/{concept_id}`
**Deskripsi:** Implementasi formula ADR-0002 persis, termasuk parameter `λ=0.05`, faktor difficulty, `N_min=5` sebagai config (bukan hardcode literal tersebar di kode).
**Acceptance Criteria:**
- [x] Hasil perhitungan cocok dengan contoh manual di ADR-0002 (dites sebagai unit test dengan data yang sama persis) — `service/mastery.rs::compute`, pure function, unit test `matches_adr_0002_worked_example` pakai angka persis dari ADR (age 1/10/20 hari, correct 1.0/0.0/1.0, difficulty 0.6/0.4/0.8) → `mastery_score = 72` persis, `confidence = 0.6` persis.
- [x] `masteries` di-upsert async setiap ada learning_event baru untuk concept terkait — `service/mastery_service.rs::recompute_for_concept`, dipanggil dari `assessment_service::submit_attempt` untuk tiap concept yang tersentuh submit (bukan cuma yang auto-gradable — lihat catatan di bawah soal interpretasi kata "async").
- [x] `confidence < 0.6` → response `score: null, message: "insufficient_data"` sesuai kontrak — `mastery_service::get_mastery`.
**DoD:** unit test dengan angka dari contoh ADR-0002 harus menghasilkan `mastery_score = 72` persis — **lulus**, lihat `service/mastery.rs` test di atas.
**Catatan implementasi:**
- Parameter `λ` (`mastery_lambda`), `N_min` (`mastery_n_min`), dan threshold `insufficient_data` (`mastery_confidence_threshold`) semua di `Config` (env-overridable, default 0.05/5.0/0.6) — bukan hardcode, sesuai penekanan ADR-0002 "semua parameter hidup di config".
- Kata "async" di AC diartikan **"dipicu tiap learning_event baru (bukan cron batch)"**, bukan literal `tokio::spawn` background — recompute jalan sinkron di dalam request `submit_attempt` yang sama. Dipilih supaya hasilnya deterministik & langsung testable lewat HTTP response, konsisten dengan cara P1-005/006/007 dibangun (semua sinkron, tidak ada background task di codebase ini).
- `correct` di payload `learning_events` sekarang cuma `bool|null` (dari P1-007) — ADR-0002 menyebut `c_i` bisa partial float (buat writing/speaking nanti), tapi belum ada mekanisme itu (Phase 4). Event dengan `correct: null` di-exclude total dari perhitungan (bukan dianggap salah) — lihat unit test `ungraded_events_are_excluded_not_treated_as_wrong`.
- `mastery_repository::find_events_for_concept` join ke `question_concepts` di query time (bukan pakai `concept_ids` yang sudah didup di payload JSON) — supaya concept yang di-link ke soal *setelah* soal itu pernah dijawab tetap ke-hitung retroactive. Diverifikasi manual lewat curl: link concept baru ke soal yang 2x pernah dijawab (1x sebelum link ada), GET /mastery langsung menunjukkan `confidence: 0.4` (2/5), bukan `0.2` (1/5) — konfirmasi retroactive linking jalan seperti didesain.
- `masteries.score` (kolom `NOT NULL FLOAT`) diisi `0.0` sebagai sentinel kalau belum ada event yang bisa dihitung — aman karena `confidence` juga 0 di kondisi itu, jadi selalu ke-mask jadi `insufficient_data` di response, tidak pernah bocor skor 0 palsu sebagai skor final.
- 4 unit test murni (`service/mastery.rs`) + 2 integration test wiring (`submit_upserts_mastery_and_get_mastery_reflects_it`, `mastery_reports_insufficient_data_before_any_attempt` di `tests/assessment_test.rs`) + 2 integration test kontrak endpoint (`mastery_masks_score_when_confidence_below_threshold`, `mastery_shows_score_when_confidence_meets_threshold` di `tests/learning_test.rs`, seed langsung ke tabel `masteries` biar presisi tanpa bergantung ke seluruh alur submit).

### P1-009 — FRSS Scheduler v1
**Status:** done
**Depends on:** P1-008
**Endpoint:** `GET /review-queue`
**Deskripsi:** Implementasi ADR-0003 persis, termasuk floor interval, cap per sesi (default 10), dan `min_gap_hours` (default 4).
**Acceptance Criteria:**
- [x] Hasil update `ease_factor`/`interval_days` cocok dengan tabel 5 siklus di ADR-0003 (unit test) — `service/frss.rs::apply`, pure function, unit test `matches_adr_0003_five_cycle_table` menjalankan persis urutan recalled→recalled→forgot→recalled→partial dari ADR dan cocok di tiap langkah (2.5/2.6 → 6.5/2.7 → 1.0/2.4 → 2.4/2.5 → 2.88/2.35).
- [x] `/review-queue` tidak pernah mengembalikan >`limit` item — `frss_service::get_review_queue`, `limit` diclamp ke `[1, review_queue_default_limit]` (default 10 dobel jadi cap keras, caller cuma bisa minta lebih kecil, bukan lebih besar).
- [x] Concept yang direview <4 jam lalu tidak muncul lagi di queue — lihat catatan desain di bawah soal `masteries.last_reviewed_at` dipakai sebagai gate, bukan kolom baru.
**DoD:** unit test siklus + test cap/gap — **lulus**, lihat `service/frss.rs` tests + `tests/learning_test.rs` (`review_queue_never_exceeds_requested_or_default_limit`, `review_queue_excludes_concept_reviewed_within_min_gap_hours`).
**Catatan implementasi (baca semua sebelum lanjut ke ticket berikutnya):**
- **Deviasi dari ADR-0003 yang sengaja, di-flag ke user (lihat `docs/STATE.md` "Deviasi"):** ADR-0003 bilang trigger update FRSS itu "dipicu dari learning_event hasil review, bukan attempt biasa" — implikasinya seharusnya ada alur "review" terpisah dari submit assessment biasa. Tapi checkpoint keluar Phase 1 poin 4 (`docs/tickets/phase-1.md` bagian bawah) eksplisit bilang submit attempt harus memicu update `masteries` **dan** `frss_schedule` sebagai satu jalur kritis, dan belum ada ticket/endpoint apapun di Phase 1 yang mendefinisikan alur "review" terpisah. Untuk MVP, `assessment_service::submit_attempt` memanggil `frss_service::record_review` untuk tiap concept yang punya jawaban auto-gradable di submit itu (rata-rata correctness kalau 1 concept muncul di >1 soal dalam 1 submit, supaya tidak dobel-update SM-2 dalam 1 request) — setiap latihan biasa dianggap juga "review" sampai ada alur review terpisah yang dibuat (kemungkinan tiket Phase 2, saat recommendation engine/UI review dibangun). **Ini keputusan yang disengaja & didokumentasikan, bukan penyimpangan diam-diam** — kalau nanti butuh dipisah (practice vs review), itu perlu ADR baru yang men-supersede bagian trigger di ADR-0003.
- **`min_gap_hours` diimplementasi tanpa kolom baru** — `frss_schedule` di `domain-model.md` tidak punya kolom `last_reviewed_at` sendiri (cuma `due_at`), dan aturan "JANGAN ubah struktur tabel `frss_schedule` tanpa ADR baru" di `STATE.md` berlaku. Solusinya: pakai `masteries.last_reviewed_at` (kolom yang sudah ada, di-touch P1-008 di *setiap* learning_event untuk concept itu, dari sistem manapun) sebagai gate bersama — persis semangat aturan ADR-0003 nomor 3 ("concept yang sama tidak boleh direview >1x dalam periode min_gap_hours, walau sistem lain memicu"). `repository/frss_repository.rs::find_due` join ke `masteries` buat cek ini, tidak nambah kolom.
- Threshold `frss_recalled_threshold` (0.8) dan `frss_partial_threshold` (0.4) di `Config` (env-overridable) sesuai ADR-0003 "threshold config-driven". Increment/decrement ease_factor (+0.1/-0.15/-0.3) dan multiplier partial (1.2) **tidak** dijadikan config — ADR-0003 cuma eksplisit sebut threshold sebagai config-driven, bukan angka-angka SM-2 itu sendiri.
- Verifikasi manual end-to-end lewat curl: link concept baru ke 1 soal, submit assessment (semua benar) → `frss_schedule` row baru dengan `interval_days=2.5, ease_factor=2.6, last_result='recalled'` (persis siklus 1 tabel ADR-0003 dari state default). `/review-queue` kosong selama `due_at` belum lewat (2.5 hari ke depan, sesuai desain — bukan bug), lalu setelah `due_at` dipaksa ke masa lalu manual, concept itu langsung muncul di `/review-queue` dengan `suggested_question_ids` yang benar.
- `suggested_question_ids` per concept dibatasi 3 soal published (`repository/frss_repository.rs::find_suggested_question_ids`) — kontrak (`api-contract.md`) tidak spesifikasi jumlahnya, 3 dipilih sebagai angka wajar buat 1 sesi micro-review.

### P1-010 — Asset Upload (Cloudflare R2)
**Status:** todo
**Depends on:** P0-009
**Endpoint:** `POST /assets/upload`
**Acceptance Criteria:**
- [ ] Upload sukses mengembalikan signed URL dengan expiry wajar (misal 1 jam untuk akses langsung, atau permanent kalau public asset)
- [ ] File > batas ukuran (config, default 25MB) → 413
**DoD:** test upload sukses + test file terlalu besar.

### P1-011 — AI Gateway v1 (stub, 1 task type)
**Status:** todo
**Depends on:** P0-004 (ADR), P1-002
**Endpoint:** `POST /ai/evaluate` (task: `grammar_evaluation` saja dulu)
**Acceptance Criteria:**
- [ ] Alur penuh sesuai ADR-0004 dijalankan (bukan panggil provider langsung): estimasi cost → cek saldo credit → panggil DeepSeek adapter → validasi output schema → tulis `ai_tasks` → charge credit (ADR-0005)
- [ ] Saldo tidak cukup → 402 sebelum request ke provider dieksekusi
- [ ] Output gagal validasi schema → `ai_tasks.status=failed`, tidak charge credit
**DoD:** test 3 skenario: sukses, saldo kurang, output invalid (mock provider response rusak).

### P1-012 — Health Check & Logging Standar
**Status:** todo
**Depends on:** P0-009
**Endpoint:** `GET /health`
**Acceptance Criteria:**
- [ ] Cek koneksi DB + Redis, bukan cuma "server nyala"
- [ ] Semua handler pakai `tracing` dengan request_id konsisten
- [ ] Format error di semua handler yang sudah dibuat sejauh ini konsisten dengan aturan di `api-contract.md`
**DoD:** `/health` return `db: down` kalau DB memang mati (dites dengan mematikan koneksi sengaja di test env).

### P1-013 — Integration Test Suite Penuh
**Status:** todo
**Depends on:** semua di atas
**Acceptance Criteria:**
- [ ] Semua endpoint P1-001 s/d P1-012 punya minimal 1 integration test
- [ ] Skenario checkpoint keluar Phase 1 (lihat bawah) dites sebagai 1 test end-to-end
**DoD:** `cargo test` hijau di CI.

---

## Checkpoint keluar Phase 1 (harus bisa didemo, bukan asumsi)
1. [ ] User bisa login via Google → dapat JWT.
2. [ ] User bisa lihat 1 curriculum tree (data seed).
3. [ ] User mengerjakan 1 assessment (3 soal MCQ), submit, dapat score otomatis.
4. [ ] Submit tadi menciptakan `learning_events`, yang memicu update `masteries` dan `frss_schedule` untuk concept terkait — **jalur paling kritis**, tes end-to-end eksplisit untuk ini.
5. [ ] `ai_tasks` terisi minimal 1 baris dari 1 pemanggilan `/ai/evaluate` percobaan, dengan credit ter-charge dengan benar di `transactions`.

Kalau poin 4 belum jalan end-to-end, jangan lanjut ke Phase 2/3 walau endpoint lain sudah banyak dibuat.
