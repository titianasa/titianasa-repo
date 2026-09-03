# Phase 20 (ticket-numbering) — Proctoring Frontend

## Keputusan scope (baca duluan)

Item ke-7 dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap di
`docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan semuanya'".

**1 gap discovery + 1 gap arsitektur jauh lebih besar ditemukan** —
polanya beda dari fase-fase sebelumnya (P9-003/P12-002/P16-003 dst.,
yang biasanya cukup 1 endpoint "list"/"discovery" baru):

1. **Gap kecil, ditutup di P20-001**: reviewer tidak punya cara
   menemukan sesi proctoring mana saja yang perlu ditinjau — endpoint
   yang ada semua per-ID (`GET /proctoring-sessions/{id}`). Ditutup
   dengan `GET /proctoring-sessions` (listing, reviewer-only,
   `risk_score` dihitung sama seperti detail view, urut terbaru
   duluan). Backend selesai lebih dulu, dikomit terpisah dari FE:
   `feat(P20-001)`.
2. **Gap besar, TIDAK ditutup di fase ini — didokumentasikan sebagai
   scope yang sengaja didefer**: Exam Runtime (P7-001) — satu-satunya
   hal yang proctoring sungguh-sungguh mengawasi — **tidak punya
   frontend sama sekali** sebelum ticket ini (dikonfirmasi lewat grep,
   nol referensi `exam-session` di manapun di `titian-web`). Tanpa
   itu, tidak ada alur nyata untuk mendemonstrasikan "siswa setuju
   diawasi lalu browser melaporkan kejadian sungguhan selama ujian" —
   jadi P20-003 TERPAKSA membangun halaman ambil-ujian minimal
   (`/latihan/ujian/[assessmentId]`) sebagai prasyarat, memakai ulang
   `questionRenderer`/`QUESTION_RENDERERS` (P3-002) dan
   `assessmentsApi.submit` yang sudah ada — bukan proyek Phase 7
   penuh, cuma cukup untuk proctoring punya sesuatu yang nyata untuk
   dipasangi.

**Keputusan arsitektur: konsen ditawarkan, TIDAK dipaksakan.** Tidak
ada kolom di skema manapun yang mengikat `proctoring_policy_id` sebagai
wajib untuk `assessment` tertentu — `policy_id` dipilih bebas saat
`POST /exam-sessions/{id}/proctoring-session` (lihat P13-001..003).
Jadi `ConsentGate` cuma bisa MENAWARKAN pengawasan (siswa pilih dari
semua policy yang ada lewat `GET /proctoring-policies`) dan SELALU
menyediakan tombol "Lanjut Tanpa Pengawasan" — keterbatasan ini
didokumentasikan secara eksplisit di komentar kode
(`consent-gate.tsx`), bukan disembunyikan di balik UI yang berpura-pura
mewajibkan sesuatu yang backend-nya sendiri tidak mewajibkan.

**Dieksplisit DIDEFER (bukan ditutup diam-diam)**: titik masuk untuk
siswa MENEMUKAN ujian yang bisa dikerjakan. `/latihan/ujian/{id}`
sekarang cuma bisa dicapai lewat URL langsung dengan `assessmentId`
yang sudah diketahui — tidak ada link dari `/latihan` atau manapun.
Alasannya bukan kelalaian: tabel `assessments` (ADR-0001) berdiri
sendiri, TIDAK punya relasi apa pun ke `cohort`/`learning_product` di
skema manapun (dikonfirmasi baca `schema.ts` — `assessments` cuma
punya `id`/`type`/`title`/`config`, tidak ada FK masuk dari cohort).
Membangun discovery yang benar butuh keputusan desain skema baru (tabel
relasi assessment↔cohort) yang di luar cakupan "Proctoring Frontend" —
kalau nanti mau dikerjakan, itu ticket-phase sendiri, bukan tambahan
kecil di sini.

Juga didefer: rekaman kamera/mikrofon sungguhan (`EventMonitor` cuma
melaporkan `document.visibilitychange`/`fullscreenchange`/`window
blur` — sinyal yang browser sudah expose sendiri, bukan capture media
baru), deteksi wajah/computer-vision apa pun (sudah didefer sejak
`docs/tickets/phase-13.md`'s "Keputusan scope", tidak diubah di sini).

## Ticket

### P20-001 — Backend: `GET /proctoring-sessions` (listing untuk reviewer)
**Status:** done
**Depends on:** P13-002/003/004 (`proctoring_sessions`, review, risk score)
**Endpoint baru:** `GET /proctoring-sessions`.
**Acceptance Criteria:**
- [x] Reviewer (`platform_admin`/`org_owner`/`academic_director`) lihat semua sesi, urut `consent_given_at` terbaru duluan, masing-masing bawa `student_name`/`assessment_title`/`risk_score`
- [x] Non-reviewer (termasuk siswa) 403
**DoD:** 2 test baru (`tests/proctoring.test.ts`), 478/478 total, route-coverage 123/123. Dikomit terpisah: `feat(P20-001): add GET /proctoring-sessions - a reviewer had no way to discover sessions`.

### P20-002 — Dashboard tinjauan staff (`/pengawasan`)
**Status:** done
**Depends on:** P20-001
**Deskripsi:** `/pengawasan` (list, `ProctoringSessionList`) → `/pengawasan/[sessionId]` (detail, `SessionDetail`) — risk score, riwayat event mentah, form keputusan (Bersih/Tandai/Pelanggaran Terkonfirmasi + catatan opsional) lewat `POST /proctoring-sessions/{id}/review`. Entry point ditambahkan ke dropdown `TopBar` ("Pengawasan"), digerbangi role sama persis dengan `canManageOrganization` (diverifikasi identik dengan `proctoring_session:review`'s role list di `permissions.ts` — direuse, bukan diduplikasi).
**Acceptance Criteria:**
- [x] `risk_score` ditampilkan sebagai skor, BUKAN keputusan otomatis — teks eksplisit "bukan keputusan otomatis" di UI, satu-satunya jalan mengubah `review_status` tetap lewat aksi manusia yang eksplisit
- [x] Badge status pakai label Indonesia (Menunggu/Bersih/Ditandai/Pelanggaran)
**DoD:** Diverifikasi lewat `Bun.WebView` — lihat P20-004.

### P20-003 — Exam Runtime minimal + consent gate + event monitor (siswa)
**Status:** done
**Depends on:** P7-001 (backend, sudah ada sejak sebelumnya — cuma FE-nya yang baru), P13-001..003
**Deskripsi:** `/latihan/ujian/[assessmentId]` — mulai sesi (`POST /assessments/{id}/exam-sessions`), `ConsentGate` (pilih policy dari `GET /proctoring-policies` atau skip), soal-soal lewat `questionRenderer` yang sudah ada, `EventMonitor` (listener browser asli) selama sesi berjalan, submit lewat `assessmentsApi.submit` yang sudah ada.
**Acceptance Criteria:**
- [x] Tipe soal yang belum punya renderer terdaftar tampil pesan jelas ("belum didukung"), bukan crash
- [x] Event browser asli (tab hidden/visible, fullscreen exit, window blur) benar-benar terkirim ke `POST /proctoring-sessions/{id}/events`, bukan simulasi tombol
- [x] Skip pengawasan tetap bisa menyelesaikan ujian normal (proctoring opsional, bukan wajib — lihat "Keputusan scope")
**DoD:** Diverifikasi lewat `Bun.WebView` — lihat P20-004.

### P20-004 — Integration check + exit checkpoint
**Status:** done
**Depends on:** P20-001 s/d P20-003
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit`/`lint`/`build` bersih di `titian-web` (satu lint error nyata ditemukan & diperbaiki: `EventMonitor` menulis `.current` sebuah ref di badan render, bukan di `useEffect` — `react-hooks/refs` menangkapnya sebelum production)
- [x] `bun test` bersih di `titian-backend-bun` (478/478, tidak ada regresi)
**DoD:** Skrip seed sekali-pakai (staff `org_owner` + siswa + 1 assessment mock_exam + 1 policy, refresh token di-mint langsung ke DB — tidak dicommit) dipakai untuk diverifikasi end-to-end lewat `Bun.WebView`: siswa mulai ujian → consent gate tampil pilihan policy → setuju & mulai → event `tab_hidden` sungguhan terpicu (`document.hidden`/`visibilitychange`) → jawab & kirim → skor 100/100 tampil → staff buka `/pengawasan` → sesi muncul dengan `risk_score: 4` dan status "Menunggu" → buka detail → riwayat 2 event (`tab_hidden` medium, `tab_visible` low) dengan timestamp asli → klik "Bersih" → status berubah jadi "Bersih" beserta jam tinjauan. Data demo dihapus dari dev DB setelahnya (termasuk FK tambahan yang belum pernah ditemukan cleanup sebelumnya: `learning_events`/`masteries`/`frss_schedule`/`user_xp`/`user_achievements`/`user_concept_mastery_baselines`/`user_daily_missions`/`ai_tasks`/`assets`/`resource_activity`/`tutor_profiles`/`subscriptions`/`ad_views` — attempt+submit ternyata menyentuh jauh lebih banyak tabel FK ke `users` daripada fase-fase sebelumnya yang cuma butuh `credits`/`transactions`/`xp_events`/`user_streaks`).
- [x] Bug operasional ditemukan & diperbaiki selama verifikasi (BUKAN bug app): backend `.env`'s `FRONTEND_ORIGIN=http://localhost:3001` tidak cocok dengan dev server yang sempat dijalankan di port 3000 (default) — CORS diam-diam menolak semua panggilan API dari browser, termasuk `/auth/refresh`, membuat sesi selalu ke-`clear()` lalu redirect ke `/login` walau token valid. Diperbaiki dengan menjalankan `next dev` di port 3001. Dicatat di sini karena polanya bisa berulang di fase berikutnya kalau dev server dijalankan tanpa cek `.env` dulu.

---

## Checkpoint keluar Phase 20
1. [x] Siswa bisa memulai ujian sungguhan, memilih setuju/tidak diawasi, dan kejadian pengawasan (tab tersembunyi, dll.) benar-benar terlapor lewat listener browser asli — bukan tombol simulasi.
2. [x] Staff (org_owner/academic_director/platform_admin) bisa menemukan semua sesi yang perlu ditinjau lewat satu dashboard (`/pengawasan`), bukan cuma lewat ID yang sudah diketahui.
3. [x] Keputusan tinjauan (Bersih/Tandai/Pelanggaran) selalu aksi manusia eksplisit — `risk_score` cuma sinyal, tidak pernah otomatis mengubah `review_status`.
4. [x] Keterbatasan arsitektur nyata (consent tidak bisa dipaksakan; tidak ada discovery ujian dari `/latihan`) didokumentasikan secara eksplisit, bukan disembunyikan atau diam-diam di-scope-creep jadi proyek skema baru.

Phase 20 tertutup. Lanjut Phase 21 — Module Completion Rule + §3.9 rescue-mode/tutor-bridge.
