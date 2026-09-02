# Phase 13 (ticket-numbering) — Proctoring (roadmap-Fase 9)

## Keputusan scope (baca duluan)

Item ke-4/TERAKHIR dari 4 roadmap-Fase yang diminta user berurutan
(2026-09-02): 5.3 (Phase 10) → 6.9-16 (Phase 11) → 8 sisa (Phase 12) →
**9 (ini)**. Sumbernya sendiri (`ALR_Build_Roadmap.md` §Fase 9) memberi
peringatan eksplisit yang tidak dipakai fase manapun sebelumnya:
*"paling akhir, paling sensitif... Privacy/consent/retention/
encryption/audit **wajib** didesain bersamaan, bukan ditambahkan
belakangan."* Ticket-phase ini memperlakukan itu sebagai gerbang
desain, bukan slogan — tiap ticket di bawah punya bagian consent/
retention eksplisit, bukan ditambal di ticket terakhir.

**Breakdown resmi** (`ALR_Phase_Detail_Breakdown.md` PHASE 9, merujuk
balik ke ADR-0001/`ALR_Detailed_Blueprint.md` §3.9): Policy → Event
Collector → Risk Engine → Human Review → Privacy/Compliance, **gerbang
manusia wajib, jangan auto-decision**.

**Riset kunci sebelum motong scope**:
- **`proctoring_policies`/`proctoring_sessions`/`proctoring_events`
  sudah ada di schema sejak ADR-0001, NOL kode pernah menyentuhnya**
  (dikonfirmasi grep) — pola dead-capability yang sama seperti
  `exam_sessions` sebelum P7-001, `concept_prerequisites` sebelum
  P4-003, `transactions.payout_earned` sebelum P9-007. Ticket-phase ini
  MENGAKTIFKAN 3 tabel itu, bukan mendesain ulang.
- **`exam_sessions` (P7-001) punya `user_id` langsung** — proctoring
  session menempel di exam session yang sudah ada (`exam_session_id`
  FK), jadi ownership check ("punya sesi ujian ini") gratis dari kerja
  P7-001, tidak perlu tabel/kolom baru buat itu.
- **Evidence upload REUSE `POST /assets` yang sudah ada** (P1-010/
  P2-010) — `proctoring_events.evidence_id` sudah FK ke `assets` sejak
  ADR-0001. Tidak ada mekanisme upload baru, evidence Cuma referensi
  asset yang sudah di-upload lewat jalur yang ada.
- **ADR-0006's role matrix SUDAH punya baris "Proctoring event:
  review"**: `platform_admin`/`org_owner`/`academic_director` (✅
  unconditional) + `teacher/tutor` (✅ "kelas sendiri"). **MVP ini CUMA
  implementasi 3 role pertama** — "kelas sendiri" butuh
  `exam_sessions` terhubung ke `cohort`/kelas, yang TIDAK ADA (exam
  session dibangun di atas `assessments`, assessment bukan entitas
  cohort-scoped — Level Assessment/IELTS/dst semua standalone).
  **Didefer eksplisit sebagai gap, bukan diimplementasi setengah
  salah** — dicatat juga di `docs/STATE.md`.
- **Encryption-at-rest DI LUAR SCOPE kode aplikasi** — itu keputusan
  infra (disk/object-storage encryption di provider hosting DB/R2),
  bukan sesuatu yang ticket backend bisa "implementasikan" tanpa
  kredensial/provider produksi nyata — kelas keterbatasan yang sama
  dengan payment gateway asli (P9-007) yang di-stub karena tidak ada
  kredensial. Dicatat eksplisit sebagai infra decision tertunda, bukan
  diam-diam dilewati.
- **Audit sistem-lebar (generic audit log utk SEMUA endpoint) DI LUAR
  SCOPE** — terlalu besar utk 1 ticket-phase dan tidak diminta spesifik
  di luar konteks proctoring. Yang DIBANGUN: jejak audit utk **1
  tindakan sensitif yang ticket ini tambahkan sendiri** — keputusan
  human review (`reviewed_by`/`reviewed_at`/`decision`/`notes` di baris
  `proctoring_sessions`, immutable-append-semantics kecuali revisi
  eksplisit — lihat P13-004) — bukan audit umum.
- **Capture kamera/mikrofon/layar sungguhan (browser API) adalah kerja
  FRONTEND** — sesi ini backend-focused sejak Phase 7 (FE cuma
  disentuh utk gap nyata/rebrand kecil, konsisten seluruh sesi).
  Backend cuma memodelkan EVENT yang sudah terdeteksi client (`type`,
  `severity`, `metadata`) — tidak membangun deteksi wajah/gerak
  sungguhan (itu computer-vision, jauh di luar scope apa pun sesi ini).
  **Didefer eksplisit** sebagai kandidat FE terpisah, sama seperti
  Phase 9's §8.2 (tutor dashboard) di Phase 12.

**Keputusan pemotongan MVP (scope ticket-phase ini)**:
- **P13-001 — Proctoring Policy + consent-first gate**
- **P13-002 — Event Collector (student-reported events + evidence link)**
- **P13-003 — Risk Engine (signal → score, murni fungsi, BUKAN keputusan)**
- **P13-004 — Human Review (gerbang manusia wajib + audit trail keputusan)**
- **P13-005 — Retention (lazy purge evidence, pola sama P11-003 — tidak ada scheduler)**
- **P13-006 — Integration test suite + exit checkpoint**

**Dieksplisit DIDEFER, bukan didiamkan**: capture kamera/mic/screen
sungguhan (FE + computer vision, di luar scope backend manapun sesi
ini), encryption-at-rest (keputusan infra/provider, butuh kredensial
produksi nyata), audit sistem-lebar (di luar konteks proctoring),
`teacher/tutor` "kelas sendiri" review scope (butuh linkage
exam_session↔cohort yang tidak ada), dashboard FE human-review
(backend-only, pola sama semua fase sejak Phase 7).

Tidak ada ADR baru — ADR-0001 sudah mengunci skema 3 tabel proctoring,
ADR-0006 sudah mengunci role matrix "Proctoring event: review". Kolom
tambahan di bawah (consent/retention/review) murni migrasi aditif,
bukan desain ulang.

## Ticket

### P13-001 — Proctoring Policy + consent-first gate
**Status:** done
**Depends on:** ADR-0001 (`proctoring_policies`/`proctoring_sessions` sudah ada di schema), P7-001 (`exam_sessions`)
**Endpoint baru:** `POST /proctoring-policies`, `GET /proctoring-policies`, `POST /exam-sessions/{id}/proctoring-session`.
**Deskripsi:** Policy (camera/mic/screen level + fullscreen/focus flag, SUDAH ada kolomnya) dibuat staff dulu; siswa memulai proctoring session dari exam session miliknya SENDIRI, WAJIB consent eksplisit — tanpa consent, sesi tidak pernah dibuat sama sekali (bukan dibuat lalu ditandai "belum consent").
**Acceptance Criteria:**
- [x] Migrasi: `proctoring_policies` dapat kolom baru `retention_days` (integer NOT NULL default 30 — dasar P13-005's purge window, per policy karena tiap tipe ujian bisa punya kebijakan retensi beda)
- [x] `POST /proctoring-policies` — resource baru `proctoring_policy:create` di `permissions.ts`'s matrix, role `platform_admin`/`org_owner`/`academic_director` (pola sama `tutor_profile:create`)
- [x] `GET /proctoring-policies` — siapa saja authenticated (config read-only, pola sama `GET /curricula`)
- [x] `POST /exam-sessions/{id}/proctoring-session` — auth "milik sendiri" (`exam_session.user_id === ctx.userId`, exam session ORANG LAIN → 403); body wajib `{policy_id, consent: true, device_info}` — `consent !== true` → **422 `consent_required`, sesi TIDAK PERNAH di-insert** (bukan insert dulu baru gerbang); `consent_given_at = now()` direkam di baris yang sama saat insert (bukti eksplisit, bukan diasumsikan dari keberadaan baris)
**DoD:** test backend baru — consent `false`/absen → 422, nol baris `proctoring_sessions` tersisa; consent `true` → sesi dibuat dengan `consent_given_at` terisi; siswa lain (bukan pemilik exam session) → 403; non-staff mencoba `POST /proctoring-policies` → 403.

**Catatan implementasi:** `proctoring_service.startProctoringSession` cek consent SEBELUM query policy sekalipun (gerbang paling awal). 4 test baru di `tests/proctoring.test.ts`.

### P13-002 — Event Collector
**Status:** done
**Depends on:** P13-001
**Endpoint baru:** `POST /proctoring-sessions/{id}/events`, `GET /proctoring-sessions/{id}` (draft awal, diperluas P13-003/004).
**Deskripsi:** Client (siswa) melaporkan event yang SUDAH terdeteksi di sisi client (`face_missing`/`multiple_faces`/`fullscreen_exit`/dst, sesuai contoh ADR-0001) — backend cuma menerima+menyimpan, TIDAK melakukan deteksi computer-vision apa pun (di luar scope, lihat "Keputusan scope"). `evidence_id` opsional, referensi ke asset yang SUDAH di-upload lewat `POST /assets` yang ada (bukan mekanisme upload baru).
**Acceptance Criteria:**
- [x] `POST /proctoring-sessions/{id}/events` — auth "milik sendiri" (via `proctoring_session → exam_session.user_id`); `{type, severity, metadata?, evidence_id?}`; `severity` harus salah satu `low`/`medium`/`high` (CHECK constraint sudah ada di DB, validasi service dulu biar 422 rapi, pola sama tiap CHECK-constraint lain di proyek ini)
- [x] `evidence_id` (kalau diisi) harus asset yang benar-benar ada DAN milik siswa yang sama (422 kalau tidak — mencegah siswa mereferensikan asset orang lain sebagai "bukti")
- [x] `GET /proctoring-sessions/{id}` — DRAFT: cabang kepemilikan (siswa pemilik lihat versi TERBATAS: status/consent/policy saja, BUKAN daftar event mentah — keputusan privasi-by-design sadar, supaya siswa tidak bisa "belajar" persis apa yang memicu deteksi lalu menghindarinya di ujian berikutnya; staff lihat versi PENUH termasuk daftar event, diperluas P13-003/004 dengan risk score+review state)
**DoD:** test backend baru — siswa post event ke sesi miliknya sendiri berhasil; siswa lain (bukan pemilik) → 403; `evidence_id` milik orang lain → 422; `GET` versi siswa TIDAK mengandung field `events`/daftar mentah, versi staff MENGANDUNG.

**Catatan implementasi:** `getSession` balikin union type `OwnerSessionView | StaffSessionView` — versi owner SECARA STRUKTURAL tidak punya field `events`/`risk_score` sama sekali (bukan cuma disembunyikan di response mapping), jadi tidak ada risiko field itu bocor lewat perubahan serialisasi nanti. 3 test baru.

### P13-003 — Risk Engine (signal → score, bukan keputusan)
**Status:** done
**Depends on:** P13-002
**Endpoint baru:** tidak ada endpoint baru — `risk_score` jadi field tambahan di `GET /proctoring-sessions/{id}` (versi staff).
**Deskripsi:** Fungsi MURNI (`computeRiskScore(events)`), memetakan severity event ke skor 0-100 (bobot `low=1`/`medium=3`/`high=7`, konstanta lokal tunable — bukan tabel config, sama kelas keputusan `weaknessScoreThreshold` dst). **Skor ini TIDAK PERNAH menulis apa pun** — tidak set status, tidak block submission, tidak trigger notifikasi otomatis. Murni angka yang disurfacekan ke manusia lewat `GET`, manusia yang memutuskan (P13-004). Ini penegakan literal "Risk Engine cuma kasih skor, bukan auto-decision" dari kata-kata user sendiri.
**Acceptance Criteria:**
- [x] `computeRiskScore(events: {severity}[]): number` — fungsi murni di `proctoring_service.ts`, di-`export` biar dites langsung tanpa lewat HTTP (pola sama `gradebook_service.average`/`assignment_service.computeLate`)
- [x] Sesi tanpa event sama sekali → skor `0`, BUKAN `null` (beda dari `mastery`/`gradebook` yang null-aware — di sini "belum ada sinyal" secara semantik SAMA dengan "belum ada indikasi risiko", bukan "tidak diketahui")
- [x] Skor di-cap maksimal 100 (event bertumpuk banyak tidak overflow ke angka aneh)
- [x] `GET /proctoring-sessions/{id}` versi staff dapat field baru `risk_score`, dihitung ON-READ dari event yang ada (tidak ada kolom cache `proctoring_sessions.risk_score` — konsisten pola agregasi on-read leaderboard P8-005/reputation P12-004, dan sengaja: kalau di-cache, ada risiko nyata skor "membeku" salah kalau event baru masuk setelah cache ditulis)
- [x] **Dites eksplisit: skor risk TIDAK PERNAH mengubah `review_status`** — sesi dengan skor tinggi (banyak event `high`) tetap `review_status: 'pending'` sampai manusia benar-benar memanggil endpoint review (P13-004)
**DoD:** test backend baru — kombinasi event severity campuran menghasilkan skor sesuai formula; sesi kosong → `risk_score: 0`; skor tinggi TIDAK mengubah `review_status` secara otomatis (assert eksplisit, ini poin paling penting ticket ini).

**Catatan implementasi:** 5 event `high` (5×7=35, dites eksplisit) menghasilkan `risk_score: 35` dan `review_status` tetap `pending` — assert langsung di test yang sama, bukan 2 test terpisah yang bisa "kebetulan" tidak saling bertentangan. 2 test baru.

### P13-004 — Human Review (gerbang manusia wajib)
**Status:** done
**Depends on:** P13-001 (role matrix), P13-003 (risk score disurfacekan ke reviewer)
**Endpoint baru:** `POST /proctoring-sessions/{id}/review`.
**Deskripsi:** SATU-SATUNYA jalur `review_status` pernah berubah dari `pending` — dipanggil manusia (staff), bukan otomatis oleh sistem manapun. Keputusan+catatan reviewer sekaligus JADI jejak audit tindakan sensitif ini (lihat "Keputusan scope" soal audit sistem-lebar yang di luar scope).
**Acceptance Criteria:**
- [x] Migrasi: `proctoring_sessions` dapat 4 kolom baru — `review_status` (text NOT NULL default `'pending'`, CHECK `pending`/`cleared`/`flagged`/`violation_confirmed`), `reviewed_by` (nullable FK users), `reviewed_at` (nullable timestamptz), `review_notes` (nullable text)
- [x] `POST /proctoring-sessions/{id}/review` — `requirePermission(ctx, "proctoring_session", "review")`, resource/action baru di `permissions.ts`, role `platform_admin`/`org_owner`/`academic_director` (persis 3 role ADR-0006 matrix yang di-scope MVP ini — lihat "Keputusan scope" soal `teacher/tutor` yang didefer)
- [x] Body `{decision, notes?}` — `decision` HARUS salah satu `cleared`/`flagged`/`violation_confirmed` (BUKAN `pending` — manusia wajib memilih hasil nyata, tidak bisa "reset" lewat endpoint ini)
- [x] Review ULANG untuk sesi yang sama DIPERBOLEHKAN (menimpa `review_status`/`reviewed_by`/`reviewed_at`/`review_notes`) — SENGAJA beda dari `tutor_reviews` (P12-004) yang menolak re-review 409: keputusan moderasi internal butuh bisa dikoreksi (salah pencet, banding), bukan rating publik yang reputasinya bergantung pada 1x submit
- [x] `GET /proctoring-sessions/{id}` versi staff (P13-002/003) diperluas: `review_status`/`reviewed_by`/`reviewed_at`/`review_notes` ikut tampil — 1 "paket review" lengkap dalam 1 GET (setara dashboard human-review yang diminta sumber, backend-only)
**DoD:** test backend baru — non-staff (termasuk siswa pemilik sesi sendiri) mencoba review → 403; staff review dengan `decision: flagged` → `review_status`/`reviewed_by`/`reviewed_at` terisi benar; `decision: pending` → 422 (bukan diterima diam-diam); review ulang oleh staff lain menimpa (bukan ditolak).

**Catatan implementasi:** `proctoring_session_repository.setReview` adalah SATU-SATUNYA tempat `review_status`/`reviewed_by`/`reviewed_at`/`review_notes` pernah ditulis di seluruh codebase (dikonfirmasi grep) — satu fungsi, satu jalur, tidak ada cabang lain yang bisa menulisnya diam-diam. 3 test baru.

### P13-005 — Retention (lazy purge evidence)
**Status:** done
**Depends on:** P13-001 (`retention_days` per policy), P13-002 (`evidence_id`)
**Endpoint baru:** tidak ada — sweep terjadi lazy di dalam `GET /proctoring-sessions/{id}`, pola PERSIS P11-003's subscription-allowance expiry (tidak ada infra scheduling/cron di backend ini, sudah dikonfirmasi berulang kali tiap fase yang butuh "expiry").
**Deskripsi:** Event yang lebih tua dari `policy.retention_days` sejak `timestamp`-nya kehilangan link evidence — `evidence_id` di-null-kan + `purged_at` dicatat. **TIDAK menghapus baris `assets` itu sendiri** (siklus hidup asset itu domain fitur Drive yang terpisah, P2-010 dst — proctoring cuma memutus REFERENSI-nya sendiri ke situ, keterbatasan MVP jujur, bukan diklaim "data sungguhan terhapus permanen").
**Acceptance Criteria:**
- [x] Migrasi: `proctoring_events` dapat kolom baru `purged_at` (nullable timestamptz)
- [x] `proctoring_event_repository.purgeExpired(db, proctoringSessionId)` — untuk tiap event sesi itu yang `evidence_id IS NOT NULL AND purged_at IS NULL AND timestamp <= now() - policy.retention_days hari`: `UPDATE ... SET evidence_id = NULL, purged_at = now()`
- [x] Dipanggil di AWAL `GET /proctoring-sessions/{id}` (kedua cabang, staff maupun siswa — data hygiene, bukan cuma buat yang lihat versi staff) sebelum baca event/hitung risk score — pola PERSIS `economy_repository.sweepExpiredAllowance` dipanggil di awal `getBalance`/`charge`
- [x] Idempotent (event yang sudah `purged_at` terisi tidak diproses ulang) — TAPI belum di-hardening race 2 sweep bersamaan (keterbatasan MVP diketahui, kelas sama P9-004/P11-003, didokumentasikan bukan disembunyikan)
**DoD:** test backend baru — policy `retention_days: 0`, event lama (timestamp dimundurkan manual di DB, pola sama simulasi waktu P5-001/P11-005) → `GET` memicu purge, `evidence_id` jadi `null`+`purged_at` terisi; event BARU (dalam window retensi) TIDAK ikut ter-purge; baris `assets` yang direferensikan TETAP ADA di DB setelah purge (dites eksplisit — cuma link yang putus, bukan asset-nya).

**Catatan implementasi:** Test final pakai `retention_days: 2` + 1 event dimundurkan 3 hari (purged) berdampingan dengan 1 event baru yang TIDAK disentuh (tidak purged) di sesi yang SAMA — membuktikan sweep-nya selektif per-event, bukan "semua evidence di sesi ini hilang begitu 1 saja kedaluwarsa". 1 test baru.

### P13-006 — Integration test suite + exit checkpoint
**Status:** done
**Depends on:** P13-001 s/d P13-005
**Deskripsi:** Pola sama tiap ticket-phase sebelumnya — route-coverage audit, checkpoint end-to-end yang menyatukan Policy → Consent → Event Collector → Risk Engine → Human Review → Retention dalam 1 alur nyata lewat request HTTP asli.
**Acceptance Criteria:**
- [x] Route-coverage audit (`grep`-based, pola P2-017/.../P12-005)
- [x] Checkpoint baru: staff bikin policy (`retention_days` pendek) → siswa mulai exam session (P7-001) → siswa mulai proctoring session DENGAN consent → siswa lapor beberapa event campuran severity (termasuk 1 dengan `evidence_id` dari asset asli) → staff `GET` packet PENUH lihat `risk_score` terhitung benar dan `review_status` MASIH `pending` (belum ada keputusan otomatis) → staff `POST /review` dengan `decision: flagged` → `GET` ulang menunjukkan `review_status: flagged`+`reviewed_by`+`reviewed_at` benar → simulasi waktu lewat retention window → `GET` ulang menunjukkan `evidence_id` event lama ter-purge sementara `review_status`/`risk_score` tidak berubah (purge cuma sentuh evidence, bukan keputusan review)
**DoD:** `bun test` hijau penuh di `titian-backend-bun` (lokal — CI masih P0-010 yang tertunda).

**Catatan implementasi:** Route-coverage audit: 116/116 route, 0 gap (110 sebelum Phase 13 + 6 baru). `tests/phase13-checkpoint.test.ts` — 1 skenario penuh persis urutan AC: policy `retention_days: 2` → exam session (P7-001) → proctoring session dengan consent → 3 event campuran (low/medium+evidence/high) → staff lihat `risk_score: 11` (1+3+7) DAN `review_status: pending` tetap (belum ada keputusan otomatis) → staff review `decision: flagged` → `reviewed_by`/`reviewed_at` benar → event bukti dimundurkan 3 hari (lewat window 2 hari) → purge lewat `GET` berikutnya, `evidence_id` event itu `null`, TAPI `review_status`/`risk_score` TIDAK berubah (purge dan review 2 concern independen, dibuktikan bukan cuma diasumsikan dari desain kode). Total **461/461 test lulus** (dari 447 sebelum Phase 13).

---

## Checkpoint keluar Phase 13 (harus bisa didemo, bukan asumsi)
1. [x] Consent-first terbukti keras: tanpa `consent: true`, proctoring session TIDAK PERNAH dibuat (bukan dibuat lalu ditandai belum-consent) — dites eksplisit lewat percobaan tanpa consent yang menghasilkan nol baris baru.
2. [x] Event Collector: siswa cuma bisa lapor event ke sesi miliknya sendiri, evidence cuma bisa referensi asset miliknya sendiri.
3. [x] Risk Engine terbukti MURNI SKOR: skor tinggi dari banyak event severity `high` TIDAK PERNAH mengubah `review_status` dengan sendirinya — cuma `POST /review` (manusia) yang bisa mengubahnya, dites eksplisit sebagai 1 skenario terpisah, bukan cuma disimpulkan dari desain endpoint.
4. [x] Human Review: role gate benar (siswa pemilik sesi sendiri TETAP tidak bisa me-review sesinya sendiri — bukan cuma "orang lain" yang ditolak), keputusan+catatan tersimpan sebagai jejak audit (`reviewed_by`/`reviewed_at`).
5. [x] Retention: evidence event lama ter-purge (link diputus) tanpa menyentuh baris `assets` itu sendiri maupun `review_status`/skor sesi manapun.
6. [x] Semua yang dideferred (capture client sungguhan, encryption-at-rest, audit sistem-lebar, `teacher/tutor` "kelas sendiri" review scope) tercatat eksplisit di sini dan `docs/STATE.md`.

Phase 13 tertutup: 461/461 test, 116/116 routes/0 gap. **Ini item TERAKHIR dari 4 roadmap-Fase yang diminta user secara eksplisit berurutan** (5.3 → 6.9-16 → 8 sisa → 9) — semuanya sekarang selesai. Tidak ada fase berikutnya yang menunggu kecuali user memberi instruksi baru.
