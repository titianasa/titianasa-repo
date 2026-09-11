# Phase 35 — Sesi Kelas & Kehadiran 4-Metode

🟢 **SELESAI** — M1 s/d M7 selesai dan teruji (2026-09-07).

Rencana lengkap (disetujui user lewat plan mode sebelum eksekusi dimulai): `/home/john/.claude/plans/wild-brewing-hummingbird.md`.

---

## Keputusan scope (baca duluan)

Lihat fitur "Kelas" org (Phase 32 — cuma roster: tambah/hapus siswa, tautan modul/program, tidak ada lagi), user minta (1) fitur sesi/kehadiran ala tutor marketplace nanti juga ada di Kelas, dan (2) — bagian konkret dari permintaan — sistem kehadiran nyata dengan 4 metode: manual (hadir/alpha/sakit/izin/telat/belum diabsen), guru scan QR tiap siswa, siswa scan QR sesi hari itu, dan deteksi otomatis dari gabung Google Meet.

Riset sebelum planning (2 Explore paralel) menemukan sisi marketplace SUDAH punya hampir semua ini untuk **cohort** (produk tutor berbayar), cuma belum pernah untuk kelas org, dan belum pernah pakai QR:

- **Manual**: nyata, jalan (`services/attendance.rs::mark_attendance`).
- **Deteksi Google Meet otomatis**: nyata, jalan, BUKAN stub — `GoogleMeetProvider` (`services/meeting_provider.rs`) benar-benar panggil OAuth + Meet API. **Polling, bukan webhook live** — tutor klik "Sinkronkan Kehadiran" secara eksplisit setelah sesi selesai.
- **QR (kedua arah)**: tidak ada sama sekali di codebase manapun.
- **Manajemen sesi**: nyata (`services/class_session.rs`).

Semuanya digerbang lewat `cohort.product_id → learning_products.tutor_id` — coupling marketplace yang sama persis yang sudah ditemukan dan sengaja dihindari Phase 32 saat bikin Kelas org. **Keputusan, konsisten dengan preseden itu: tabel baru yang scope ke `classes.id`, reuse LOGIKA YANG SUDAH JALAN** (trait `MeetingProvider`/`GoogleMeetProvider`, fungsi `compute_verification_status`, bentuk manual-marking) **bukan tabel marketplace-nya**. QR genuinely baru di kedua arah.

Perbedaan produk yang disengaja dari marketplace: status pakai kosakata absensi sekolah Indonesia yang user minta sendiri — `hadir/alpha/sakit/izin/telat` — bukan `present/absent/late/excused` marketplace. "Belum diabsen" tidak butuh nilai status — cukup ketiadaan baris untuk siswa+tanggal itu.

---

### M1-M4 — Backend: sesi, kehadiran manual, QR (2 arah), sinkronisasi Google Meet
**Status:** ✅ selesai dan teruji (2026-09-07)

**Deskripsi**: Migrasi baru `0035_org_class_sessions_attendance.sql` — `org_class_sessions` (mirror `class_sessions`, tapi `session_date` beneran `date` bukan `text` marketplace), `org_session_participant_records`, `org_attendance_records` (status Indonesia + method `manual|qr_teacher|qr_student|google_meet`).

`services/org_class.rs` diperluas jadi `pub(crate)`: `assert_can_manage_class` (dipakai semua write), plus `assert_is_member_or_manager` BARU (gerbang lebih sempit — siswa boleh baca jadwal/self-check-in tanpa butuh tier `Resource::Class,Create`).

`services/org_class_session.rs` — create/list/get sesi, pakai `dyn MeetingProvider` yang sama dari `AppState` (jadi kalau lagi dev, real `GoogleMeetProvider` beneran dipanggil — dikonfirmasi lewat smoke test, bukan stub). `services/org_attendance.rs` — manual marking (`mark_attendance`), roster-per-tanggal via LEFT JOIN (`get_roster_for_date`), tanpa logika billing package-session marketplace (kelas org bukan produk berbayar). `services/attendance_qr.rs` — token QR siswa pakai `jsonwebtoken` (sudah ada, bukan crate `hmac` baru) dengan domain separation via klaim `purpose` (bukan reuse literal secret JWT auth), masa berlaku 5 tahun (kartu ID durable, bukan token sesi). `services/org_attendance_verification.rs` — port `sync_attendance` marketplace, reuse `compute_verification_status` LANGSUNG (bukan ditulis ulang), pemetaan status verifikasi ke kosakata Indonesia (`present→hadir`, `late→telat`, `partial→izin`, `absent/lainnya→alpha`) didokumentasikan eksplisit sebagai keputusan, bukan mapping 1:1.

**Bug nyata ditemukan lewat smoke test (2 kali, pola yang sama)**: `sqlx::query_as!` gagal infer nullability lewat `LEFT JOIN` untuk kolom yang di tabel asalnya `NOT NULL` — pertama di `get_roster_for_date`'s `ar.status`/`ar.method` (500 di percobaan pertama load tab Kehadiran), fix sama seperti bug serupa yang sudah ditemukan sebelumnya di sesi ini (`org_class.rs`'s `module_title`): override eksplisit `as "status?"`/`as "method?"`.

**DoD**: `cargo check` bersih. Server live di-restart. Smoke test end-to-end lewat curl dengan token JWT asli (guru + siswa, `Kelas A`): buat sesi (Google Meet asli, bukan stub — `join_url` beneran `meet.google.com/...`) → mark manual (`telat`) → siswa ambil QR token sendiri → guru scan token itu (`qr_teacher`, jadi `hadir`) → siswa self-check-in pakai session id (`qr_student`, tetap `hadir`) → sync-attendance dari Google Meet asli (0 peserta beneran gabung → status turun jadi `alpha`, MEMBUKTIKAN sync membaca data real, bukan fake). Batas permission dikonfirmasi: siswa coba mark attendance orang lain → 403; token QR sampah → 422; endpoint tanpa auth → 401.

---

### M5-M7 — Frontend: tab Sesi & Kehadiran, QR (kartu siswa + scan guru + check-in URL), tombol sinkron
**Status:** ✅ selesai dan teruji (2026-09-07)
**Depends on:** M1-M4

**Deskripsi**: `lib/api-client.ts` (`orgClassSessionApi`, `orgAttendanceApi`), `hooks/use-class-sessions.ts`. Halaman `kelas/[classId]/page.tsx` sekarang 3 tab (Siswa/Sesi/Kehadiran, komponen `Tabs` yang sudah ada): **Sesi** (`components/kelas/session-list.tsx` — buat sesi, link Google Meet, tombol "QR sesi", "Scan siswa", "Sinkronkan Kehadiran"), **Kehadiran** (`components/kelas/attendance-panel.tsx` — 1 tanggal per waktu mirip `AttendancePanel` marketplace, bukan grid multi-tanggal, 5 tombol status per baris siswa).

**QR, 2 library baru** (`qrcode` generasi, `qr-scanner` versi 1.4.2 — TIDAK perlu setup `WORKER_PATH` manual lagi, sudah pakai `import()` dinamis + `BarcodeDetector` native kalau browser dukung): `components/kelas/qr-code-display.tsx` (wrapper canvas tipis dipakai di 2 tempat), `components/profil/attendance-card.tsx` (kartu QR durable siswa di halaman Profil), `components/kelas/scan-student-dialog.tsx` (mode kamera guru, scan bergantian tanpa tutup dialog, dedup 3 detik biar 1 kartu tidak ke-mark berkali-kali).

**Keputusan desain penting**: arah "siswa scan QR sesi" TIDAK pakai library scanner sama sekali — payload QR-nya adalah URL langsung (`/kelas/{id}/checkin/{sessionId}`, halaman baru), jadi kamera native HP mana pun yang sudah bisa buka URL hasil scan otomatis bisa dipakai, cukup halaman itu yang otomatis panggil self-check-in saat dimuat. `qr-scanner` cuma benar-benar dibutuhkan untuk arah SEBALIKNYA (guru scan banyak siswa berturut-turut tanpa pindah halaman tiap scan).

**DoD**: `npx tsc --noEmit` + `npx eslint src` bersih. Smoke test browser end-to-end (Playwright, 2 akun asli): guru buka tab Sesi → buat sesi → buka dialog "QR sesi" (kode render nyata) → tab Kehadiran → klik "Sakit" pada baris siswa → reload halaman → baris tetap menunjukkan "Sakit"/"Manual" (bukan cuma state optimistic yang hilang saat refresh — DIBUKTIKAN lewat reload penuh, bukan cuma cek state React). Halaman Profil siswa menampilkan "Kartu Absen" dengan QR code render nyata. Data uji dibersihkan setelah verifikasi.
