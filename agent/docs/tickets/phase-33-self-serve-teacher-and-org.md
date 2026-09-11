# Phase 33 — Self-Serve "Jadi Guru" & Pembuatan/Gabung Organisasi

🟢 **SELESAI** — P33-001 s/d P33-003 selesai dan teruji (2026-09-07).

Rencana lengkap (disetujui user lewat plan mode sebelum eksekusi dimulai): `/home/john/.claude/plans/wild-brewing-hummingbird.md`.

---

## Keputusan scope (baca duluan)

Lihat dashboard-nya sendiri (yang cuma menampilkan "Kamu di sini sebagai: Pelajar" dari Phase 32), user minta 2 card tambahan untuk akun yang baru siswa: (1) jadi guru — kelola kelas, modul, dll — pakai role `teacher` dan fitur `/kelas` yang baru dibangun Phase 32; (2) kelola organisasi (sekolah/kursus/pesantren) dengan absen/guru/siswa/report wali disebut sebagai contoh fitur masa depan, bukan permintaan literal untuk membangunnya sekarang — ATAU gabung ke organisasi yang sudah ada.

Kedua jalur ini belum ada sama sekali sebelum phase ini: auth cuma Google OAuth, setiap login baru otomatis terdaftar sebagai `student` di satu org platform bersama, dan jadi `teacher`/`org_owner` sebelumnya butuh admin yang SUDAH ADA mempromosikan (gated `require_permission_in_org`). Tidak ada `POST /organizations` sama sekali, tidak ada konsep kode undangan di mana pun. Dibuat self-serve TANPA antrian approval — konsisten dengan betapa ringannya setiap aksi "buat X" lain di platform ini (kelas, produk tutor, module item semuanya langsung create-and-go).

**Bug nyata ditemukan lewat smoke test, bukan cuma dari baca kode**: rencana awal cuma memperbaiki ordering `find_all_roles` (dipakai `/users/me`, yang di-treat frontend sebagai "org aktif" via `roles[0]`). Tapi ternyata ada FUNGSI KEDUA yang terpisah, `find_default_role`, yang dipakai `middleware/auth.rs`'s `resolve_auth_context` untuk resolve `ctx.organization_id` — org yang SUNGGUHAN dipakai untuk gerbang permission di setiap request — dan fungsi ini punya `ORDER BY created_at asc` sendiri yang TIDAK ikut diperbaiki di iterasi pertama. Akibatnya: user yang baru saja bikin org sendiri (jadi `org_owner` di situ) melihat org barunya sebagai "aktif" di frontend (karena `find_all_roles` sudah benar), tapi SETIAP permission check tetap diam-diam menggerbang ke org LAMA-nya (`find_default_role` belum diperbaiki) — 403 di organisasinya sendiri. Manifest sebagai `GET /organizations/{id}/members` dan `GET /organizations/{id}` 403 tepat setelah `POST /organizations` sukses. Fix: `find_default_role` disamakan ordering-nya persis dengan `find_all_roles` (case admin-tier dulu, lalu `created_at desc`) — 2 fungsi ini sekarang WAJIB tetap sinkron kalau salah satu diubah lagi nanti.

---

### P33-001 — Backend: self-serve teacher assignment + pembuatan/gabung organisasi
**Status:** ✅ selesai dan teruji (2026-09-07)
**Depends on:** Phase 32 (P32-001, role `teacher` sudah jadi assignable)

**Deskripsi**: `services/auth.rs::find_all_roles` DAN `find_default_role` (baru ditemukan saat smoke test — lihat di atas) sama-sama diberi `ORDER BY` eksplisit: role admin-tier (`platform_admin`/`org_owner`/`academic_director`) duluan, lalu `created_at desc` — supaya org yang baru dibuat/dipromosikan otomatis jadi "aktif" di seluruh app tanpa perlu org-switcher UI baru.

`services/organization.rs` dapat 3 fungsi baru, semuanya TANPA gerbang `require_permission_in_org` (ini aksi self-service ke membership sendiri, bukan aksi admin ke orang lain — beda sikap dengan `assign_teacher`/`assign_tutor` yang tetap admin-gated):
- `self_assign_teacher` — insert role `teacher` untuk caller di org default mereka saat ini (`find_all_roles(...).first()`).
- `create_organization` — validasi `type` (`school`/`tutor_org`, bukan `platform` — itu reserved buat org platform bersama), slugify nama (helper baru, lowercase+dash, retry sekali dengan suffix acak kalau slug bentrok — pola sama dengan `find_or_create_platform_org`'s retry-nya sendiri), insert org, lalu insert `org_owner` untuk creator.
- `join_organization_by_slug` — cari org by slug (404 kalau tidak ada), insert `student` untuk caller.

`GET /organizations/{id}` (baru, `get_organization`) — gerbang sama dengan `get_members` (admin-tier), dipakai untuk menampilkan slug org sebagai "kode organisasi" di halaman Organisasi. `POST /me/teacher-role`, `POST /organizations`, `POST /organizations/join` (route baru).

**DoD**: `cargo check` bersih. Server live di-restart. Smoke test browser asli, akun `student` murni (`ndsanja21@gmail.com`): `POST /me/teacher-role` → role `teacher` muncul; `POST /organizations` (nama "SD Uji Coba Nusantara") → 201, dan `GET /users/me` berikutnya menunjukkan `org_owner` di org baru sebagai `roles[0]` (bukti fix ordering bekerja); akun kedua (`p2016-student@example.com`) `POST /organizations/join` pakai slug org pertama → `student` baru muncul, `roles[0]`-nya berpindah ke org baru (kedua role sama-sama `student`, dibedakan lewat `created_at desc`).

---

### P33-002 — Frontend: 2 card baru di dashboard + dialog buat/gabung organisasi
**Status:** ✅ selesai dan teruji (2026-09-07)
**Depends on:** P33-001

**Deskripsi**: `role-status-card.tsx` (dari Phase 32) dapat 2 card tambahan, masing-masing sembunyi begitu tier terkait sudah dimiliki (tidak menawari user yang sudah guru untuk "jadi guru" lagi): "Jadi guru" (dialog konfirmasi 1 klik, `useSelfAssignTeacherMutation`, sukses → `/kelas`) dan "Kelola organisasi" (buka `components/organisasi/create-or-join-org-dialog.tsx`, baru — 2 tab: "Buat baru" nama+jenis, "Gabung dengan kode" input slug). Ketiga mutation (`selfAssignTeacher`/`create`/`join`) invalidate query `["me"]`, bukan key org-scoped — itu yang bikin `account-sync.tsx` (sudah ada) otomatis re-sync role/org aktif user-store dari refetch `me`, tanpa perlu perubahan frontend lain untuk switch-nya "langsung jalan". Halaman `organisasi/page.tsx` dapat baris "Kode organisasi" (cuma untuk viewer admin-tier, gerbang sama dengan backend) menampilkan slug buat dibagikan sebagai kode undangan.

**Bug nyata ditemukan lewat smoke test**: `JoinOrgForm` awalnya redirect ke `/organisasi` setelah sukses gabung — tapi org itu halaman admin-only (`MemberList` butuh tier admin buat lihat), jadi siswa yang baru gabung langsung kena 403 di `GET /organizations/{id}/members` begitu mendarat di situ. Fix: redirect join ke `/beranda` (dashboard), bukan `/organisasi` — cuma alur "buat organisasi" (creator jadi `org_owner`, benar-benar punya akses) yang tetap redirect ke `/organisasi`. Juga ditemukan: 2 dialog trigger baru (`Card` sebagai trigger, bukan `<button>` asli) memicu warning Base UI "`nativeButton` true tapi elemen bukan native button" — fix: `nativeButton={false}` eksplisit di kedua `DialogTrigger`.

**DoD**: `npx tsc --noEmit` + `npx eslint src` bersih. Smoke test browser end-to-end 2 akun: akun A klik "Jadi guru" → confirm → mendarat di `/kelas`, badge role bertambah "Guru"; akun A klik "Kelola organisasi" → buat org baru → `/organisasi` menampilkan badge "Pemilik" + kode organisasi tampil; akun B gabung pakai kode itu → mendarat di `/beranda` tanpa error, roster org A (kalau dicek lewat DB) berisi akun B sebagai `student`. Data uji (2 role row test + 1 organisasi test) dibersihkan setelah verifikasi.
