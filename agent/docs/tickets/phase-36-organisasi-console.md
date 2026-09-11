# Phase 36 — Organisasi Admin Console: Anggota / Periode / Kelas

🟢 **SELESAI** — selesai dan teruji (2026-09-08).

Rencana lengkap (disetujui user lewat plan mode sebelum eksekusi dimulai): `/home/john/.claude/plans/wild-brewing-hummingbird.md`.

---

## Keputusan scope (baca duluan)

Halaman Organisasi sebelumnya cuma daftar anggota datar dengan tombol promosi — fungsional tapi polos. User minta konsol admin sungguhan dengan 3 bagian: (1) manajemen anggota (sudah ada, tinggal dipoles), (2) manajemen "batch atau semester" — konsep baru, (3) manajemen kelas ditampilkan di sini juga, dengan fitur "assign program ke kelas" yang sungguhan (bukan field paste-UUID mentah yang sudah ada).

**"Batch atau semester"** — user pakai kata "atau", memperlakukan keduanya sebagai bisa dipertukarkan, padahal secara struktur keduanya tidak persis sama (batch/angkatan biasanya properti siswa — tahun masuk; semester biasanya properti kelas — periode berjalan). Daripada memaksakan satu model kalender akademik, dibuat SATU entitas **Periode** yang fleksibel namanya (cuma nama + tanggal mulai/selesai opsional) yang ditautkan ke **kelas**. Organisasi bebas menamai "Semester Ganjil 2026/2027" atau "Angkatan 2026" — skema-nya tidak peduli mana yang dipakai.

**"Assign program"** — `classes.program_id` sudah ada sejak Phase 32 dan sudah bisa diisi, tapi cuma sekali, saat pembuatan kelas, lewat field teks mentah "paste UUID program". Tidak ada picker, tidak bisa diubah setelahnya. Diperbaiki jadi picker `Select` sungguhan (dari `GET /programs` yang sudah ada) plus endpoint `PATCH /classes/{id}` baru supaya bisa diubah kapan pun, bukan cuma saat pembuatan.

Kelas sendiri (roster/sesi/kehadiran/QR, Phase 32+35) **tidak dibangun ulang** — cuma ditampilkan sebagai daftar navigasi di dalam konsol Organisasi, tautan langsung ke `/kelas/{id}` yang sudah lengkap fiturnya.

---

## Backend

Migrasi baru `0036_periods.sql` — tabel `periods(id, organization_id, name, start_date, end_date, status)`, `classes` dapat kolom `period_id` (nullable FK). `permissions.rs`: `Resource::Period`, tier admin-org murni (`platform_admin|org_owner|academic_director` — guru bikin kelas, bukan periode akademik). `services/period.rs` (baru): create/list/set_status. `services/org_class.rs`: `get_summary`/`list_for_caller` diperluas LEFT JOIN `periods` (dengan fix nullable `as "period_name?"` — pola yang sama yang sudah 2x ditemukan sebelumnya di sesi ini untuk LEFT JOIN kolom NOT NULL), fungsi baru `update_links` (PATCH, full-replace semantics — form edit selalu kirim state lengkap ketiga field sekaligus, jadi tidak perlu double-Option JSON yang rumit).

**Bug nyata ditemukan lewat smoke test lain lagi** (di luar scope Phase 36 langsung, ditemukan saat user menguji fitur baru): `services/organization.rs::search_share_candidates` (dipakai semua dialog "cari anggota" — Kelas, share module item, dll) join `user_organization_roles` ke `users` tanpa `distinct` — anggota dengan lebih dari 1 role di org yang sama (misal admin platform yang juga tutor) muncul 2x, bikin React key duplikat di frontend. Fix: tambah `distinct`.

## Frontend

`lib/api-client.ts`/`hooks/use-periods.ts` (baru): `periodApi`, `orgClassApi.updateLinks`. `create-class-dialog.tsx` — 2 field paste-ID diganti 3 `Select` picker sungguhan (Modul/Program/Periode, dari `useModuleChildren`/`usePrograms`/`usePeriods` yang sudah ada). `assign-class-links-card.tsx` (baru) — kartu di halaman detail kelas, tombol "Ubah" membuka dialog 3 picker yang sama, panggil `PATCH /classes/{id}`. `organisasi/page.tsx` — dirombak jadi `Tabs` 3 bagian: Anggota (tidak berubah, cuma dipindah ke tab), Periode (`period-list.tsx` baru — buat/arsipkan), Kelas (`org-class-list.tsx` baru — daftar navigasi, tautan ke `/kelas/{id}`).

**Bug nyata ditemukan lewat smoke test browser**: ketiga `Select` (Modul/Program/Periode) menampilkan value mentah ("none", UUID) alih-alih label ("Tidak ada", nama program) pada render pertama — Base UI's `<Select.Value>` cuma resolve label dari `<Select.Item>` kalau popup-nya sudah pernah dibuka sekali; tanpa itu ia fallback ke value mentah. Fix: tambah prop `items` (Record value→label) di setiap `<Select>` root, sesuai dokumentasi Base UI sendiri — dikonfirmasi lewat baca source `node_modules/@base-ui/react` langsung, bukan tebakan.

**DoD**: `cargo check` bersih. `npx tsc --noEmit` + `npx eslint src` bersih. Smoke test browser end-to-end asli: buat periode "Semester Ganjil 2026/2027" di tab Periode → tab Kelas menampilkan "Kelas A" dengan tautan ke detail → buka kelas, klik "Ubah" di kartu Tautan kelas → pilih periode yang baru dibuat (dropdown menampilkan nama asli, bukan UUID) → simpan → reload halaman → periode tetap tersimpan (dikonfirmasi bukan cuma state React yang hilang saat refresh). Data uji dibersihkan setelah verifikasi.
