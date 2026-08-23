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
**Status:** todo
**Depends on:** P1-001
**Endpoint:** `GET /users/me`, `GET /organizations/{id}/members`
**Acceptance Criteria:**
- [ ] `/users/me` mengembalikan semua role user lintas organisasi
- [ ] `/organizations/{id}/members` hanya bisa diakses role sesuai matrix ADR-0006
- [ ] Middleware `AuthContext` (user_id, organization_id, role) terpasang dan dipakai endpoint ini sebagai referensi untuk endpoint berikutnya
**DoD:** test mencakup akses ditolak (403) untuk role yang tidak berhak.

### P1-003 — Content API (read)
**Status:** todo
**Depends on:** P1-002
**Endpoint:** `GET /curricula/{id}/tree`, `GET /lessons/{id}`
**Acceptance Criteria:**
- [ ] Tree mengembalikan struktur level→unit→lesson sesuai `api-contract.md`
- [ ] Lesson yang belum published tidak bisa diakses student (403), tapi bisa oleh curriculum_developer/reviewer/admin
- [ ] Perlu data seed minimal (1 curriculum, 1 level, 1 unit, 2 lesson) untuk testing manual
**DoD:** endpoint tervalidasi dengan seed data, test permission per role.

### P1-004 — Question Bank API
**Status:** todo
**Depends on:** P1-002
**Endpoint:** `POST /question-banks/{id}/questions`, `GET /question-banks/{id}/questions`
**Acceptance Criteria:**
- [ ] Validasi schema `data`/`correct_answer` per `type` di application layer (minimal untuk `mcq` dan `fill_blank` dulu)
- [ ] Question baru selalu `status = draft`
- [ ] Alur publish (draft → in_review → published) mengikuti role reviewer sesuai ADR-0006 (endpoint publish bisa ticket terpisah kalau perlu: P1-004b)
**DoD:** test create MCQ valid, create dengan schema salah (422), publish oleh role salah (403).

### P1-005 — Assessment API
**Status:** todo
**Depends on:** P1-003, P1-004
**Endpoint:** `GET /assessments/{id}`, `POST /assessments/{id}/attempts`
**Acceptance Criteria:**
- [ ] `POST attempts` membuat attempt baru dan mengirim daftar soal (tanpa `correct_answer` di response!)
- [ ] Kalau user sudah punya attempt `in_progress` untuk assessment yang sama → 409 dengan `attempt_id` existing, bukan bikin baru
**DoD:** test memastikan `correct_answer` tidak pernah bocor di response manapun sebelum submit.

### P1-006 — Attempt Submission + Scoring Dasar
**Status:** todo
**Depends on:** P1-005
**Endpoint:** `POST /attempts/{id}/submit`
**Acceptance Criteria:**
- [ ] Auto-grading untuk tipe `mcq` dan `fill_blank` (exact/normalized match)
- [ ] Tipe soal yang butuh AI evaluation (writing/speaking) di-skip dari auto-score, status attempt tetap `submitted` menunggu evaluasi (bukan `evaluated`)
- [ ] Submit kedua untuk attempt yang sama → 409
- [ ] Jawaban kurang dari total soal wajib → 422 dengan daftar `missing`
**DoD:** test mencakup submit lengkap, submit sebagian, submit ganda.

### P1-007 — Learning Event Writer
**Status:** todo
**Depends on:** P1-006
**Deskripsi:** Setiap submit attempt memicu 1 `learning_event` per question (event_type=`question_answered`) — bukan 1 event per attempt, supaya mastery per-concept bisa dihitung granular.
**Acceptance Criteria:**
- [ ] Event tercatat dengan payload minimal `{ correct: bool|float, difficulty: float, question_id, concept_ids }`
- [ ] Jumlah event yang dibuat = jumlah soal dijawab (dicek lewat `learning_events_created` di response submit)
**DoD:** test memverifikasi jumlah row `learning_events` setelah submit sesuai jumlah soal.

### P1-008 — Mastery Calculator v1
**Status:** todo
**Depends on:** P1-007
**Endpoint:** `GET /mastery/{concept_id}`
**Deskripsi:** Implementasi formula ADR-0002 persis, termasuk parameter `λ=0.05`, faktor difficulty, `N_min=5` sebagai config (bukan hardcode literal tersebar di kode).
**Acceptance Criteria:**
- [ ] Hasil perhitungan cocok dengan contoh manual di ADR-0002 (dites sebagai unit test dengan data yang sama persis)
- [ ] `masteries` di-upsert async setiap ada learning_event baru untuk concept terkait
- [ ] `confidence < 0.6` → response `score: null, message: "insufficient_data"` sesuai kontrak
**DoD:** unit test dengan angka dari contoh ADR-0002 harus menghasilkan `mastery_score = 72` persis.

### P1-009 — FRSS Scheduler v1
**Status:** todo
**Depends on:** P1-008
**Endpoint:** `GET /review-queue`
**Deskripsi:** Implementasi ADR-0003 persis, termasuk floor interval, cap per sesi (default 10), dan `min_gap_hours` (default 4).
**Acceptance Criteria:**
- [ ] Hasil update `ease_factor`/`interval_days` cocok dengan tabel 5 siklus di ADR-0003 (unit test)
- [ ] `/review-queue` tidak pernah mengembalikan >`limit` item
- [ ] Concept yang direview <4 jam lalu tidak muncul lagi di queue
**DoD:** unit test siklus + test cap/gap.

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
