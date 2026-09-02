# Phase 9 — Organization / LMS / Marketplace (roadmap-Fase-8)

Depends on: ADR-0006 (role matrix — `teacher`/`tutor`/`org_owner`/`academic_director` sudah ada sejak Phase 0, belum pernah dipakai gate resource di luar `organization_members`/content authoring), ADR-0005 (Credit Economy — `transactions.type` sudah punya `payout_earned`/`payout_withdrawn` sejak migrasi awal, belum pernah dipakai kode apa pun), `organizations`/`user_organization_roles` (Phase 1).

Sumber utama breakdown ini: `agent/ALR_Phase_Detail_Breakdown.md`'s `## PHASE 8 — Organization / LMS / Marketplace` (§8.1-§8.15), `agent/ALR_Build_Roadmap.md`'s `## FASE 8`.

## Keputusan scope (baca duluan)

Setelah Phase 8 (Gamification) ditutup, user diminta update roadmap artifact lalu **eksplisit memilih Organization/LMS/Marketplace** sebagai prioritas berikutnya, dengan scope yang disebutkan sendiri: "RBAC penuh, class management (cohort, enrollment, attendance, sertifikat), marketplace tutor split revenue 30/70, pembayaran QRIS." Ini fase PERTAMA di seluruh proyek yang menyentuh **uang sungguhan** (payout tutor, refund, split revenue) — beda kategori risiko dari fase manapun sebelumnya (Diamond/credit di ADR-0005 itu sendiri bukan uang sungguhan, "1 credit ≈ Rp 10" cuma rate internal buat hitung margin, tidak pernah charge kartu/QRIS sungguhan).

**1 keputusan eksplisit ditanyakan ke user sebelum riset lanjut** (pola sama Phase 7's bobot skor): tidak ada kredensial payment gateway apa pun (`Midtrans`/`Xendit`/dst) tersimpan di `.env` — bagaimana scope pembayarannya? **User pilih: bangun abstraksi + alur lengkap, provider QRIS-nya DI-STUB dulu** (tidak charge uang sungguhan sampai ada akun bisnis+kredensial nyata) — pola persis `AIProvider`/`FakeAIProvider` yang sudah terbukti di proyek ini sejak P1-011/ADR-0004.

**Scope ticket-phase ini, dipetakan dari §8.1-§8.15 ke permintaan user:**
- "RBAC penuh" → §8.15 — matrix-nya SUDAH ADA sejak ADR-0006 (`teacher`/`tutor`/`org_owner`/`academic_director` semua sudah terdaftar), yang belum ada baru API/UI buat org admin kelola tutor+kelas. Ticket ini nambah `Resource`/`Action` baru ke `permissions.ts` buat resource yang baru dibuat di ticket-phase ini — bukan mendesain ulang matrix yang sudah ada.
- "class management (cohort, enrollment, attendance, sertifikat)" → §8.4 (cohort/enrollment) + §8.5 (attendance, DIPERSEMPIT ke Manual saja — QR/Geolocation/Online-auto butuh infrastruktur yang belum ada: scan UI, client geolocation, integrasi video-conference) + §8.8 (certificate).
- "marketplace tutor split revenue 30/70" → §8.3 (DIPERSEMPIT ke Private + Group session saja, sesuai urutan MVP-first sumbernya sendiri) + §8.13 (wallet ledger, REUSE `transactions.payout_earned`/`payout_withdrawn` — ADR-0005 SUDAH mengunci desain ini secara eksplisit: "dipakai tabel transactions yang sama... supaya audit trail konsisten satu tempat", bukan tabel ledger terpisah, jadi TIDAK butuh ADR baru).
- "pembayaran QRIS" → §8.12 (Payment Abstraction, provider di-stub sesuai keputusan user di atas) + §8.14 (Cancellation Policy — logic refund-nya bisa dites penuh meski provider di-stub, karena kebijakannya murni business-rule, bukan tergantung provider asli).

**SENGAJA TIDAK TERMASUK, dengan alasan konkret:**
- **§8.1 (8 kategori marketplace penuh: Course/Bootcamp/Hybrid/Exam Prep/Kids)** — urutan MVP-first sumbernya sendiri eksplisit "8.3+8.4 dulu (Private + Group)", 8.1 penuh menyusul belakangan.
- **§8.2 (tutor dashboard lengkap: Schedule/Messages/dst)** — di luar apa yang user sebutkan eksplisit; ticket ini cuma bikin `tutor_profiles` (data minimal buat listing produk), bukan dashboard penuh.
- **§8.6 (Assignment) + §8.7 (Gradebook)** — TIDAK disebutkan user di scope eksplisitnya (beda dari attendance/certificate yang disebut). Assignment butuh AI-evaluation flow baru (mirip P3-004/P6-002 tapi buat tugas kelas, bukan lesson), Gradebook butuh agregasi nilai lintas assignment/quiz/exam — keduanya cukup besar buat ticket-phase terpisah, bukan diselipkan diam-diam di sini.
- **§8.9 (Tutor Reputation Score) + §8.11 (Learning Package fleksibel)** — value-add di atas marketplace dasar yang ticket ini bangun, bukan prasyaratnya. Bisa jadi perluasan Phase 9 lanjutan.
- **§8.10 (Student Diagnosis untuk Tutor)** — sumbernya SENDIRI eksplisit minta "aturan privasi/consent eksplisit siapa yang boleh lihat data ini" sebelum dibangun — itu keputusan produk/privasi tersendiri yang belum diminta user, bukan default "tutor lihat semua data student".
- **Payment gateway ASLI (Midtrans/Xendit/dst)** — keputusan eksplisit user di atas: stub dulu, provider asli menyusul begitu ada kredensial.

**3 temuan nyata dari riset** (pola sama tiap ticket-phase — cek kode dulu sebelum nulis ticket):
1. **`transactions.type` CHECK constraint sudah punya `payout_earned`/`payout_withdrawn` sejak migrasi awal (ADR-0001), tapi ZERO baris kode manapun pernah menulis nilai itu** — persis pola `exam_sessions` sebelum P7-001 dan `concept_prerequisites` sebelum P4-003: kolom/enum yang "disiapkan" arsitektur tapi baru diaktifkan sesi ini.
2. **Unit `transactions.amount` ambigu antar-`type`**: untuk `earn`/`spend`/`purchase`/`refund` (ekonomi AI/Diamond), `amount` dalam satuan credit (ADR-0005: "1 credit ≈ Rp 10"). Untuk `payout_earned`/`payout_withdrawn` (marketplace tutor), tidak ada rate konversi yang masuk akal — ini uang Rupiah SUNGGUHAN dari transaksi booking siswa, bukan Diamond yang bisa dibelanjakan buat AI. **Keputusan ticket ini: `amount` untuk 2 type payout itu dalam Rupiah mentah (bigint, bukan credit)** — didokumentasikan eksplisit di kode (komentar di `wallet_repository.ts`), BUKAN silent reinterpretation kolom yang sama — kalau nanti perlu dipisah tabel biar tidak ambigu, itu keputusan terpisah (dicatat sebagai risiko di "Item lepas" `STATE.md` setelah ticket-phase ini, bukan diselesaikan diam-diam sekarang).
3. **Ditemukan setelah P9-001 selesai, saat user bertanya soal perbedaan role**: alur registrasi asli (`auth_service.ts`) TIDAK PERNAH insert row `user_organization_roles` — nol user asli (bukan test-seed) pernah bisa dapat role apa pun sejak Phase 0. Gap ini lintas-fase (bukan cuma marketplace), ditambal di **P9-002** (baru, lihat di bawah) karena RBAC bootstrap paling pas dikerjakan sekelompok P9-001, sebelum produk/enrollment dibangun di atasnya.

## Ticket

### P9-001 — Tutor & Organization RBAC surface (§8.15 core)
**Status:** done
**Depends on:** ADR-0006 (role matrix)
**Endpoint baru:** `POST /organizations/{id}/tutors` (assign role `tutor` + buat profil), `GET /organizations/{id}/tutors`, `PATCH /tutors/me` (edit profil sendiri).
**Deskripsi:** Data model tutor minimal (bio, spesialisasi) + permission baru buat resource marketplace yang ticket-phase ini bangun — matrix role-nya sendiri sudah lengkap sejak ADR-0006, ini nambah `Resource`/`Action` baru ke `permissions.ts` (pola additive yang sudah dipakai tiap fase: `organization_members`→`lesson`→`question_bank`→...→sekarang `tutor_profile`/`learning_product`/`cohort`/dst).
**Acceptance Criteria:**
- [x] Migrasi baru: `tutor_profiles` (`user_id` PK+FK, `organization_id` FK, `bio` text, `specializations` jsonb array, `created_at`)
- [x] `permissions.ts` dapat `Resource` baru: `tutor_profile`. Matrix: `org_owner`/`academic_director` bisa `create` (assign tutor) di org mereka; `tutor` bisa `view`/edit profil sendiri (`PATCH /tutors/me` cek `ctx.userId` = profile owner, bukan role matrix — pola sama endpoint "milik sendiri" lain di proyek ini)
- [x] `POST /organizations/{id}/tutors` — insert `user_organization_roles` (role `tutor`) + `tutor_profiles` row dalam 1 transaksi, idempotent kalau user itu sudah jadi tutor di org itu (ON CONFLICT DO NOTHING, bukan error)
- [x] `GET /organizations/{id}/tutors` — daftar tutor 1 org + profil masing-masing, auth: siapa saja yang authenticated boleh lihat (buat calon murid browsing tutor nanti) — bukan org-scoped seperti `organization_members`
**DoD:** test backend baru — `org_owner` assign tutor baru sukses; role selain `org_owner`/`academic_director` ditolak 403; assign tutor yang sudah jadi tutor di org sama → tidak error, tidak duplikat row; tutor edit profil sendiri sukses, tutor lain tidak bisa edit punya orang lain (403).

**Catatan implementasi:** `permissions.ts` cuma butuh 1 case baru
(`tutor_profile:create` → `platform_admin`/`org_owner`/`academic_director`,
sama persis role list `organization_members:view`) — `PATCH /tutors/me`
sengaja TIDAK lewat matrix sama sekali, itu ownership check murni di
`tutor_service.updateOwnProfile` (404 kalau caller belum punya profile,
bukan 403 — karena bukan soal izin, tapi soal "kamu belum jadi tutor").
`tutor_repository.assign` gabung insert role + insert profile dalam 1
`db.transaction()`, dua-duanya `onConflictDoNothing`, fallback SELECT
kalau insert profile-nya no-op — replay call yang sama 2x terbukti aman
(test "idempotent, not a duplicate"). Ketemu 1 bug PATCH-semantics pas
nulis kode (bukan pas testing): draft pertama default-in field yang
di-omit ke `""`/`[]` SEBELUM masuk service layer, yang artinya PATCH
`{bio: "x"}` doang bakal diam-diam ngosongin `specializations` yang
sudah ada. Fix: service nerima `string | undefined` dan fallback ke
`existing.bio`/`existing.specializations` (row yang sudah di-fetch),
bukan default kosong — ada test regresi eksplisit buat ini
("a partial update (bio only) does not blank out specializations").
Insight desain: tutor marketplace-wide vs tutor sekolah-spesifik TIDAK
butuh konsep baru — tutor yang di-assign di org bertipe `platform`
otomatis marketplace-wide, di org bertipe `school` otomatis khusus
sekolah itu, karena keduanya numpang `organization_id` yang sama di
`tutor_profiles`. Test baru: 8 (3 assign, 1 list, 4 PATCH — termasuk 1
isolation test yang mastiin edit profil sendiri tidak pernah menyentuh
profil tutor lain). Suite: 331 pass / 0 fail (dari 323), `bunx tsc
--noEmit` bersih, ketiga route baru dikonfirmasi dipakai di
`tests/tutor.test.ts` (audit manual, bukan script — tidak ada script
coverage terpisah di repo ini).

### P9-002 — Default Role Bootstrap: auto-join platform org sebagai student
**Status:** todo
**Depends on:** ADR-0006 (addendum `teacher`/`tutor` di bawah), P9-001 (pola idempotent assign yang dipakai ulang)
**Endpoint baru:** tidak ada — perubahan di alur registrasi (`auth_service.ts`) yang sudah ada.
**Deskripsi:** Ditemukan lewat riset sebelum P9-002 ditulis, di luar §8.1-8.15 sumber asli: **ZERO baris kode manapun pernah insert row ke `user_organization_roles`** untuk alur registrasi asli (`auth_service.ts` cuma insert ke `users`) — artinya user asli (bukan lewat test-seed helper) TIDAK PERNAH bisa dapat role apa pun, `AuthContext.organizationId`/`role` permanen `null`, dan endpoint apa pun yang butuh role (`attempt:submit`, `mastery:view`, dst — bukan cuma marketplace) tidak bisa diakses sama sekali. Ini bukan gap khusus Phase 9 — gap ini ada SEJAK Phase 0/ADR-0006, baru ketahuan sekarang karena semua ticket-phase sebelumnya diuji lewat `seedUserWithRole` (insert DB langsung, bypass alur asli). Belum ada user asli di produksi (masih pre-launch) jadi tidak perlu migrasi backfill.

**Keputusan (ditanya ke user, dipilih eksplisit):** user baru auto-join 1 organisasi singleton bertipe `platform` sebagai `student` saat registrasi — bukan wajib diundang/join eksplisit dulu. Org sekolah/tutor tambahan menyusul lewat undangan terpisah (di luar scope ticket ini — belum ada alur invite sekolah sama sekali; dicatat sebagai item lepas berikutnya di `docs/STATE.md`).
**Acceptance Criteria:**
- [ ] `organization_repository.findOrCreatePlatformOrg(db)` — cari org `type='platform'` (slug tetap, mis. `alr-platform`), insert kalau belum ada (`onConflictDoNothing` di `slug` UNIQUE + fallback SELECT, pola sama `tutor_repository.assign`) — idempotent, aman dipanggil concurrent tanpa duplikat org
- [ ] `auth_service.ts`'s alur registrasi (bukan login user yang sudah ada) — setelah `userRepository.insert`, panggil `findOrCreatePlatformOrg` lalu insert `user_organization_roles` (role=`student`) buat user baru itu
- [ ] User yang SUDAH PERNAH login sebelumnya (row `users` sudah ada) TIDAK di-auto-assign ulang kalau sudah punya role manapun — cuma path registrasi user BENAR-BENAR baru yang dapat role default ini
**DoD:** test backend baru — user baru pertama kali login (Google OAuth) langsung dapat `organizationId`+`role=student` terisi (dicek lewat endpoint yang butuh `AuthContext`, mis. `GET /me/xp` langsung setelah registrasi tanpa seed manual apa pun); login kedua kalinya (user sudah ada) tidak menambah role kedua/duplikat; 2 user baru berbeda tidak collide (org platform-nya SATU, dua row role beda user).

**Catatan (addendum ADR-0006, `teacher` vs `tutor`):** ditinjau ulang di sesi yang sama — matrix ADR-0006 sudah menganggap `teacher`/`tutor` setara persis di tiap baris permission sejak awal (1 kolom gabungan), jadi TIDAK ada penggabungan/pemisahan baru yang dibutuhkan sekarang. `tutor_profiles` (P9-001) dipakai bersama utk keduanya, dibedakan di UI murni lewat `organizations.type` (`school`→label "Guru", `platform`/`tutor_org`→label "Tutor"). Role value `teacher` tetap ada di CHECK constraint tapi sengaja tidak pernah di-assign endpoint manapun sampai ada kebutuhan konkret yang benar-benar beda dari tutor. Detail lengkap: `agent/docs/adr/0006-rbac.md`'s addendum 2026-09-02.

### P9-003 — Learning Products: Private & Group sessions (§8.3 minimal)
**Status:** todo
**Depends on:** P9-001 (`tutor_profiles`)
**Endpoint baru:** `POST /tutors/me/products`, `GET /tutors/{id}/products`, `GET /products/{id}`.
**Deskripsi:** Listing yang bisa di-booking siswa — dipersempit ke 2 tipe (`private`, `group`) sesuai urutan MVP-first sumbernya. Harga dalam Rupiah (bukan credit — ini transaksi marketplace, beda "dompet" dari Diamond).
**Acceptance Criteria:**
- [ ] Migrasi baru: `learning_products` (`id`, `tutor_id` FK `tutor_profiles`, `type` CHECK IN (`private`,`group`), `title`, `description`, `price_idr` bigint, `capacity` int nullable — null buat private (selalu 1), diisi buat group, `status` CHECK IN (`draft`,`published`,`archived`) default `draft`)
- [ ] `POST /tutors/me/products` — auth: role `tutor`, harus milik tutor itu sendiri (`tutor_id` dari `ctx.userId`, bukan dari body — cegah tutor bikin produk atas nama tutor lain)
- [ ] `GET /tutors/{id}/products`/`GET /products/{id}` — publik (siapa saja authenticated), cuma tampilkan `status=published`, kecuali kalau pemanggil adalah tutor pemilik produk itu sendiri (lihat draft miliknya)
**DoD:** test backend baru — tutor bikin produk private/group sukses; non-tutor ditolak; draft produk tidak muncul di listing publik tapi muncul buat pemiliknya sendiri; harga negatif/capacity invalid ditolak validasi.

### P9-004 — Class Management: Cohort + Enrollment (§8.4)
**Status:** todo
**Depends on:** P9-003 (`learning_products`)
**Endpoint baru:** `POST /products/{id}/cohorts`, `POST /cohorts/{id}/enrollments`, `GET /cohorts/{id}/students`.
**Deskripsi:** `Product → Cohort/Batch → Enrollment` sesuai struktur sumbernya persis. Enrollment di ticket ini TIDAK terikat ke pembayaran sukses (itu P9-006) — enrollment dulu bisa berdiri sendiri (dites pakai status manual), disambungkan ke payment flow beneran di P9-006 supaya tiap ticket tetap fokus 1 lapisan.
**Acceptance Criteria:**
- [ ] Migrasi baru: `cohorts` (`id`, `product_id` FK, `name`, `schedule` jsonb, `starts_at`, `ends_at` nullable) + `enrollments` (`id`, `cohort_id` FK, `student_id` FK users, `status` CHECK IN (`pending`,`active`,`completed`,`cancelled`) default `pending`, `enrolled_at`)
- [ ] `POST /products/{id}/cohorts` — auth: tutor pemilik produk itu (atau `org_owner`/`academic_director` kalau produk itu milik org)
- [ ] `POST /cohorts/{id}/enrollments` — untuk `group`: cek `capacity` belum penuh (COUNT enrollment `status IN (pending,active)` < capacity) sebelum insert, kalau penuh 422; untuk `private`: max 1 enrollment per cohort
- [ ] `GET /cohorts/{id}/students` — auth: tutor pemilik cohort itu, atau siswa lihat enrollment-nya sendiri saja (bukan daftar penuh)
**DoD:** test backend baru — enroll ke group sampai capacity penuh → enrollment ke-N+1 ditolak 422; enroll ke private ke-2 kali → ditolak; tutor lihat semua siswa cohort miliknya; siswa cuma lihat status enrollment sendiri, bukan daftar siswa lain (403 kalau minta daftar penuh).

### P9-005 — Attendance: Manual (§8.5, dipersempit)
**Status:** todo
**Depends on:** P9-004 (`cohorts`/`enrollments`)
**Endpoint baru:** `POST /cohorts/{id}/sessions/{session_date}/attendance`, `GET /cohorts/{id}/attendance`.
**Deskripsi:** Cuma metode Manual (tutor tandai langsung) — QR/Geolocation/Online-auto butuh infrastruktur yang belum ada di proyek ini (scan UI kamera, geolocation client, integrasi video-conference), didefer eksplisit, bukan disederhanakan diam-diam jadi "auto selalu hadir".
**Acceptance Criteria:**
- [ ] Migrasi baru: `attendance_records` (`id`, `cohort_id` FK, `student_id` FK, `session_date` date, `status` CHECK IN (`present`,`absent`,`late`,`excused`), `method` CHECK IN (`manual`) — kolom `method` sengaja ada dari awal walau cuma 1 nilai valid sekarang, biar QR/Geolocation/Online nanti additive bukan migrasi ubah kolom, `marked_by` FK users, `marked_at`)
- [ ] `POST /cohorts/{id}/sessions/{session_date}/attendance` — body: daftar `{student_id, status}[]`, auth: tutor pemilik cohort; upsert per (cohort, student, session_date) — tandai ulang di tanggal sama = update, bukan baris baru
- [ ] `GET /cohorts/{id}/attendance` — rekap per siswa per tanggal, auth: tutor pemilik cohort, atau siswa lihat attendance sendiri
**DoD:** test backend baru — tandai attendance beberapa siswa sekaligus; tandai ulang tanggal yang sama → update bukan duplikat; siswa yang tidak terenroll di cohort itu ditolak; non-tutor pemilik cohort ditolak.

### P9-006 — Certificates (§8.8)
**Status:** todo
**Depends on:** P9-005 (attendance, salah satu syarat penerbitan), `masteries` (Phase 1)
**Endpoint baru:** `POST /cohorts/{id}/enrollments/{enrollment_id}/certificate`, `GET /certificates/{code}/verify` (publik, tanpa auth).
**Deskripsi:** Terhubung ke mastery asli (skor CEFR estimasi), bukan cuma status "completed" — sesuai contoh sumbernya. Wording sengaja hati-hati (bukan sertifikasi resmi eksternal).
**Acceptance Criteria:**
- [ ] Migrasi baru: `certificates` (`id`, `enrollment_id` FK unique — 1 sertifikat per enrollment, `certificate_code` text unique (buat URL verifikasi publik), `issued_at`, `completion_percent`, `estimated_cefr` nullable text, `skill_summary` jsonb — snapshot ringkas mastery per skill saat diterbitkan, BUKAN live-query tiap verifikasi, biar sertifikat tidak "berubah" setelah diterbitkan)
- [ ] `POST /cohorts/{id}/enrollments/{enrollment_id}/certificate` — auth: tutor pemilik cohort; syarat `enrollment.status = 'completed'`; snapshot mastery concept yang ter-link ke produk/cohort itu (kalau ada) jadi `skill_summary`+`estimated_cefr` kasar (rata-rata mastery confident-only, pola sama `league_service.getLeague`'s `average_mastery`, P8-005) — kalau tidak ada data mastery sama sekali, `estimated_cefr: null`, bukan ditebak
- [ ] `GET /certificates/{code}/verify` — publik, balikin `{valid: true, student_name, course_title, completion_date}` kalau ketemu, `{valid: false}` (bukan 404 — endpoint verifikasi publik tidak boleh bocorin "certificate_code mana yang exist" lewat status code beda)
**DoD:** test backend baru — terbitkan sertifikat buat enrollment `completed` sukses, snapshot mastery benar; terbitkan buat enrollment belum `completed` ditolak; terbitkan 2x buat enrollment sama ditolak (unique); verifikasi code valid balikin data benar; verifikasi code sembarangan balikin `valid:false` bukan 404/500.

### P9-007 — Payment Abstraction (QRIS stub) + Wallet Ledger 30/70 + Cancellation Policy (§8.12+§8.13+§8.14)
**Status:** todo
**Depends on:** P9-004 (enrollment jadi target order), ADR-0005 (`transactions.payout_earned`/`payout_withdrawn`)
**Endpoint baru:** `POST /enrollments/{id}/checkout`, `POST /payments/{id}/webhook` (simulasi callback provider — dipanggil manual/test di mode stub), `POST /enrollments/{id}/cancel`, `GET /tutors/me/wallet`.
**Deskripsi:** Inti finansial ticket-phase ini. `PaymentProvider` interface (pola persis `AIProvider`/ADR-0004) + `StubQrisProvider` (tidak charge uang sungguhan, generate `payment_id` palsu + auto-berhasil setelah dipanggil, konsisten `FakeAIProvider`). Wallet tutor REUSE `transactions` (ADR-0005), bukan tabel baru.
**Acceptance Criteria:**
- [ ] `payment_provider.ts` baru: interface `PaymentProvider { createPayment(orderId, amountIdr): Promise<{paymentId, qrisPayload}>; }`. `StubQrisProvider` — balikin `payment_id` acak + `qris_payload` dummy, TIDAK pernah hit network asli. Provider asli (Midtrans/dst) TIDAK diimplementasi ticket ini — placeholder yang jelas ditandai di kode + `docs/STATE.md` sebagai keputusan eksplisit user, bukan lupa
- [ ] Migrasi baru: `orders` (`id`, `enrollment_id` FK unique, `amount_idr` bigint, `status` CHECK IN (`pending`,`paid`,`failed`,`refunded`), `payment_id` text nullable, `created_at`)
- [ ] `POST /enrollments/{id}/checkout` — buat `orders` row (`status=pending`) + panggil `PaymentProvider.createPayment`, balikin `qris_payload` ke client
- [ ] `POST /payments/{id}/webhook` — simulasi callback sukses (mode stub: endpoint ini yang biasanya provider asli panggil, di sini dipanggil manual test/dev) — `orders.status → paid`, `enrollments.status → active`, DAN split 30/70: insert `transactions` (`type: payout_earned`, `user_id`: tutor, `amount`: 70% `amount_idr`, **satuan Rupiah mentah, bukan credit** — lihat "Keputusan scope" soal ambiguitas unit) + platform fee 30% dicatat sebagai `reference` di baris yang sama (bukan baris terpisah — platform tidak punya `users` row buat jadi `transactions.user_id`-nya sendiri, jadi fee dicatat sebagai metadata bukan baris ledger kedua)
- [ ] `POST /enrollments/{id}/cancel` — kebijakan §8.14 (contoh dari sumber, didokumentasikan sebagai default tunable): student cancel >24 jam sebelum `cohorts.starts_at` → full refund; 6-24 jam → 50%; <6 jam → no refund. Refund → `orders.status = refunded` + `transactions` baru `type: refund` ke SISWA (bukan tutor) — TIDAK reverse `payout_earned` tutor kalau sudah dibayarkan (kompleksitas clawback di luar scope ticket ini, dicatat eksplisit sebagai keterbatasan, bukan silently ignored)
- [ ] `GET /tutors/me/wallet` — SUM `transactions` (`payout_earned` - `payout_withdrawn`) buat tutor itu, pola sama `credits.balance`/`user_xp.total` (cached read, bukan scan tiap kali — TAPI karena ini tabel baru dipakai, agregasi on-read dulu, cache belakangan kalau perlu, sama pola P8-005's leaderboard)
**DoD:** test backend baru (`FakeAIProvider`-style test double buat `PaymentProvider`) — checkout → order pending + qris_payload; webhook sukses → order paid, enrollment active, tutor dapat 70% di wallet (dicek lewat `transactions` langsung DAN `GET /tutors/me/wallet`); cancel >24 jam → full refund; cancel <6 jam → no refund; refund tidak menyentuh `transactions` tutor yang sudah ada.

### P9-008 — Integration test suite + exit checkpoint
**Status:** todo
**Depends on:** P9-001 s/d P9-007
**Deskripsi:** Pola sama tiap ticket-phase sebelumnya — route-coverage audit, checkpoint end-to-end yang menyatukan tutor→produk→cohort→enrollment→payment→attendance→certificate dalam 1 alur marketplace nyata.
**Acceptance Criteria:**
- [ ] Route-coverage audit (`grep`-based, pola P2-017/.../P8-006)
- [ ] Checkpoint baru: 1 tutor bikin 1 produk group, 1 siswa enroll+checkout+webhook-sukses (dites lewat `StubQrisProvider`, bukan network asli — TIDAK ada verifikasi provider asli di checkpoint ini, beda dari Phase 6/7 yang punya provider AI asli buat dites, karena payment gateway asli memang belum ada per keputusan scope), tutor tandai attendance, cohort selesai → enrollment `completed`, tutor terbitkan sertifikat, verifikasi publik sertifikat itu sukses. Assert tiap langkah state benar DAN wallet tutor bertambah 70% dari harga produk.
- [ ] Skenario ke-2: siswa lain enroll lalu cancel <6 jam sebelum mulai → no refund, wallet tutor TIDAK berkurang (tutor sudah terlanjur dibayar dari transaksi pertama, transaksi kedua yang di-cancel beda enrollment).
**DoD:** `bun test` hijau penuh di `titian-backend-bun` (lokal — CI masih P0-010 yang tertunda).

---

## Checkpoint keluar Phase 9 (harus bisa didemo, bukan asumsi)
1. [ ] Alur marketplace penuh (tutor→produk→cohort→enrollment→payment→attendance→certificate) bisa didemo end-to-end lewat request asli, bukan potongan-potongan terpisah.
2. [ ] Wallet tutor terbukti benar-benar 70% dari harga produk (bukan 100% atau angka sembarangan) — dites eksplisit dari row `transactions` yang tersimpan.
3. [ ] Cancellation policy 3 tingkat (>24 jam/6-24 jam/<6 jam) terbukti menghasilkan refund yang berbeda sesuai kebijakan, bukan cuma 1 skenario yang dites.
4. [ ] `StubQrisProvider` terbukti TIDAK PERNAH melakukan panggilan network asli — grep eksplisit, konsisten prinsip "gerbang keputusan user" soal payment yang di-stub.
5. [ ] Sertifikat yang diterbitkan terhubung ke mastery asli (bukan cuma status completed) dan bisa diverifikasi publik tanpa auth.

Kalau salah satu poin di atas belum jalan end-to-end, jangan lanjut ke prioritas berikutnya (§8.1/8.2/8.6/8.7/8.9-11 penuh, payment gateway asli, atau roadmap-Fase lain) walau ticket lain kelihatan sudah "done" — sama semangatnya dengan aturan checkpoint di Phase 1-8.

---

## Strategi eksekusi (urutan sesi yang disarankan)

| Sesi | Ticket | Fokus | Kenapa dikelompokkan begini |
|---|---|---|---|
| 1 | P9-001 | Tutor & Org RBAC surface | Fondasi — semua ticket lain butuh `tutor_profiles` ada duluan. |
| 2 | P9-002 | Default Role Bootstrap (auto-join student) | Gap ditemukan lewat riset (tidak ada di §8.1-8.15 asli) — foundational RBAC, sekelompok sama P9-001, dikerjakan sebelum produk/enrollment dibangun. |
| 3 | P9-003 | Learning Products (Private/Group) | Produk yang di-booking — numpang tutor profile P9-001. |
| 4 | P9-004 | Cohort + Enrollment | Numpang produk P9-003 — "siapa ikut kelas yang mana". |
| 5 | P9-005 | Attendance (Manual) | Numpang cohort+enrollment P9-004. |
| 6 | P9-006 | Certificates | Numpang attendance/enrollment (`completed` jadi syarat) + `masteries` yang sudah ada sejak Phase 1. |
| 7 | P9-007 | Payment (stub) + Wallet + Cancellation | Ticket paling besar & paling sensitif finansial — dikerjakan setelah struktur produk/enrollment stabil, supaya payment cuma perlu nyambung ke entitas yang sudah teruji, bukan dibangun bareng entitas yang belum stabil. |
| 8 | P9-008 | Test suite + checkpoint | Pola sama P1-013/.../P8-006 — penutup fase. |

**Total 8 sesi** — lebih besar dari Phase 5/7 (3-4 sesi) dan Phase 8 (6 sesi) — scope genuinely luas (marketplace + payment + class management + RBAC bootstrap sekaligus, domain yang seluruhnya baru, nol tabel dead yang bisa diaktifkan kecuali `transactions.payout_earned`/`payout_withdrawn`). §8.1/8.2/8.6/8.7/8.9-11 penuh dan payment gateway asli sengaja tidak termasuk — lihat "Keputusan scope".
