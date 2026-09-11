# Phase 32 — Landing Page Persona, Indikator Role, & Kelas Milik Guru

🟢 **SELESAI** — P32-001 s/d P32-005 selesai dan teruji (2026-09-07).

Rencana lengkap (disetujui user lewat plan mode sebelum eksekusi dimulai): `/home/john/.claude/plans/wild-brewing-hummingbird.md`.

---

## Keputusan scope (baca duluan)

User meminta (dikte, Bahasa Indonesia informal) landing page berhenti spesifik-Bahasa-Inggris dan menampilkan 3 pintu masuk — "masuk sebagai siswa", "masuk sebagai guru", "masuk sebagai pengelola organisasi" — masing-masing dengan contoh singkat. Dashboard juga diminta menampilkan "kamu di sini sebagai apa", dan seorang guru harus bisa langsung membuat kelas dari dashboard, dengan kelas itu sudah punya fitur di dalamnya. Organisasi sengaja dangkal dulu ("nanti harus lebih lanjut" — kata user sendiri).

Riset sebelum planning membongkar 2 hal yang mengubah baca naif permintaan ini:

1. **`teacher` adalah role mati.** Ada di CHECK constraint `user_organization_roles` dan sudah punya label Bahasa Indonesia di `member-list.tsx`'s `ROLE_LABEL`, tapi grep mengonfirmasi (dan komentar kode sendiri bilang) tidak ada satu endpoint pun yang pernah meng-assign-nya — satu-satunya aksi "promote member" yang ada cuma assignment tutor (`POST /organizations/{id}/tutors`, P9-001). `lib/roles.ts`'s `canTeach()` sengaja mengecualikan `teacher` justru karena ini. Jadi "masuk sebagai guru" tidak punya role sungguhan di baliknya — P32-001 akhirnya menyambungkan `teacher` jadi role pertama yang bisa di-assign.
2. **Sistem "kelas" yang sudah ada (`cohorts`/`class_sessions`/`enrollments`/`attendance`/`gradebook`) TIDAK bisa dipakai ulang untuk ini.** Sistem itu ada, tapi setiap layer resolve permission dengan menelusuri `cohort.product_id → learning_products.tutor_id` (dikonfirmasi lewat baca `cohort.rs`, `class_session.rs`'s `assert_can_manage_cohort`) — satu cohort ADALAH batch dari produk marketplace berbayar. Merombaknya untuk "guru org me-roster siswa org sendiri terhadap sebuah modul, tanpa pembelian" berarti bikin `product_id` nullable dan audit setiap consumer di 6 file service — risiko tinggi ke fitur live yang berhubungan dengan uang, demi manfaat yang belum pasti. **Keputusan: domain `classes`/`class_members` baru yang minimal dan lepas**, bukan retrofit. Penjadwalan sesi/attendance untuk kelas ini adalah fast-follow yang sengaja ditunda.

Juga dikonfirmasi: auth cuma Google OAuth, tidak ada registrasi self-serve atau pembuatan organisasi self-serve (`find_or_create_platform_org`/`assign_default_student_role` otomatis mendaftarkan setiap login baru sebagai `student` di satu org platform "Titian Asa" yang dibagi bersama). Jadi **ketiga CTA landing page mengarah ke `/login` yang sama** — cards-nya adalah copy marketing yang menyiapkan ekspektasi, bukan flow signup berbeda-beda; perubahan role sungguhan terjadi lewat promosi admin org (P32-001), sama seperti assignment tutor yang sudah jalan.

---

### P32-001 — Aktifkan role `teacher` sebagai role yang bisa di-assign
**Status:** ✅ selesai dan teruji (2026-09-07)
**Depends on:** tidak ada

**Deskripsi**: Mirror `assign_tutor`/`POST /organizations/{id}/tutors` persis, tapi lebih sederhana (tanpa tabel profile — `teacher` cuma baris role biasa, sama seperti `student`/`academic_director`). `permissions.rs`: `Resource::TeacherRole`, `(TeacherRole, Create) => platform_admin | org_owner | academic_director` (tier sama dengan `TutorProfile, Create`). `services/organization.rs::assign_teacher` — insert `user_organization_roles` dengan `on conflict do nothing`. `POST /organizations/{id}/teachers` (handler+route baru, mirror `handlers/tutor.rs::post_tutor` tanpa body bio/specializations). Frontend: `useAssignTeacherMutation` (mirror `useAssignTutorMutation`), `member-list.tsx` dapat tombol kedua "Jadikan Guru" di samping "Jadikan Tutor" yang sudah ada (member bisa punya lebih dari 1 role, sesuai comment composite-key yang sudah ada di file itu). `lib/roles.ts`: `canTeachOrgClasses()` (helper baru, bukan reuse `canTeach` — itu berarti tutor marketplace, konsep beda) dan `ROLE_LABEL` dipindah ke sini jadi shared export (dipakai `member-list.tsx` + dashboard role badge P32-004).

**DoD**: `cargo check` bersih. Server live di-restart di `:8090`. Smoke test lewat browser asli (Playwright, token JWT `ndsanja@gmail.com`/`platform_admin`): buka `/organisasi`, klik "Jadikan Guru" pada baris member `student` — badge "Guru" baru muncul di daftar member tanpa error, dikonfirmasi lewat screenshot sebelum/sesudah.

---

### P32-002 — Backend domain "Kelas" baru (roster guru, lepas dari marketplace)
**Status:** ✅ selesai dan teruji (2026-09-07)
**Depends on:** tidak ada (bisa paralel dengan P32-001)

**Deskripsi**: Migrasi baru `0029_classes.sql` — `classes(id, organization_id, teacher_id, module_id nullable, program_id nullable, name, description nullable, status default 'active', created_at, updated_at)` + `class_members(class_id, student_id, joined_at, PK(class_id, student_id))`. Sengaja TIDAK ada kolom sesi/jadwal di v1 — cuma roster + tautan konten (lihat header migrasi untuk alasan penuh kenapa ini bukan reuse `cohorts`).

`permissions.rs`: `Resource::Class`; `(Class, Create) | (Class, View) => platform_admin | org_owner | academic_director | teacher`. `services/org_class.rs` (baru, sengaja dinamai `org_class` bukan `class` — nama `classApi`/`class_session.rs` sudah dipakai domain marketplace, kata sama, fitur beda sengaja): `create` (teacher role bikin untuk diri sendiri; org-admin tier bisa assign `teacher_id` ke orang lain), `list_for_caller` (teacher cuma lihat kelas sendiri; org-admin tier lihat semua kelas di org-nya), `get_detail`/`add_member`/`remove_member` digerbang lewat `assert_can_manage_class` (org-admin tier selalu lolos; `teacher` tambahan harus `class.teacher_id == ctx.user_id` — mirror shape `module_item.rs`'s `can_edit_item`). Pencarian member reuse `driveApi.searchShareCandidates`/`GET /drive/share-candidates` apa adanya — sudah org-scoped, tidak perlu endpoint baru. `handlers/org_class.rs` + `routes/org_class.rs`: `GET/POST /classes`, `GET /classes/{id}`, `POST /classes/{id}/members`, `DELETE /classes/{id}/members/{student_id}`.

**Bug nyata ditemukan lewat smoke test, bukan cuma compile**: `sqlx::query_as!` gagal infer nullability lewat `LEFT JOIN` untuk `module_title`/`program_title` — karena kolom asalnya (`modules.title`/`programs.name`) sendiri `NOT NULL`, macro mengira hasil join juga selalu non-null, padahal `LEFT JOIN` bisa menghasilkan `NULL` saat `module_id`/`program_id` kosong. Manifest sebagai `ColumnDecode { index: "7", source: UnexpectedNullError }` — 500 nyata saat membuat kelas TANPA module/program (kasus paling umum). Fix: override eksplisit `as "module_title?"` / `as "program_title?"` di kedua query (`get_summary` dan `list_for_caller`) supaya macro menghormati nullability sungguhan dari LEFT JOIN, bukan kolom asalnya.

**DoD**: `cargo check` bersih setelah fix. Server live di-restart. Smoke test browser asli: `POST /classes` tanpa `module_id`/`program_id` (kasus yang tadinya 500) sekarang 201 dan langsung terlihat di daftar; `POST /classes/{id}/members` menambah "dwi dwi" ke roster lewat search-as-you-type, terverifikasi tampil di `GET /classes/{id}`.

---

### P32-003 — Frontend "Kelas": halaman daftar + roster
**Status:** ✅ selesai dan teruji (2026-09-07)
**Depends on:** P32-002

**Deskripsi**: `lib/api-client.ts`'s `orgClassApi` (nama `classApi` sudah dipakai marketplace, sama alasan dengan backend), `hooks/use-classes.ts`. `app/(app)/kelas/page.tsx` — daftar kelas org (scope sesuai role, cuma-milik-sendiri untuk `teacher`, semua untuk org-admin tier) + dialog "Buat kelas" (`components/kelas/create-class-dialog.tsx`: nama, deskripsi opsional, module ID/program ID opsional via paste-ID sederhana, sama pola dengan "Tempel module ID prasyarat" yang sudah ada di module detail page — bukan picker baru). `app/(app)/kelas/[classId]/page.tsx` — roster: cari-dan-tambah siswa (reuse UX type-to-search dari `share-item-dialog.tsx`, data member sudah lengkap nama/email dari backend jadi tidak perlu cache `knownCandidates` seperti punya share dialog), tombol hapus per siswa. Nav: `top-bar.tsx` dapat entry "Kelas" digerbang `canTeachOrgClasses`, terpisah dari entry "Mengajar" (tutor marketplace) yang sudah ada.

**DoD**: `npx tsc --noEmit` + `npx eslint src` bersih. Smoke test browser end-to-end (satu alur, screenshot tiap langkah): buat kelas → buka detail → cari "dwi" → tambah ke roster → roster menampilkan nama+email real-time tanpa reload.

---

### P32-004 — Indikator role & aksi cepat di dashboard
**Status:** ✅ selesai dan teruji (2026-09-07)
**Depends on:** P32-001 (role `teacher` harus bisa di-assign dulu supaya badge-nya berarti)

**Deskripsi**: `components/dashboard/role-status-card.tsx` (baru) — menampilkan SEMUA role distinct dari `useMe().roles` (bukan cuma satu, karena ADR-0006 membolehkan lebih dari satu role per user) via badge `ROLE_LABEL`, plus tombol "Buat kelas" kalau salah satu role lolos `canTeachOrgClasses`. Dipasang di `beranda/page.tsx` tepat di bawah salam pembuka.

**DoD**: `npx tsc --noEmit` + `npx eslint src` bersih. Smoke test: dashboard `platform_admin`+`tutor` menampilkan kedua badge ("Admin Platform", "Tutor") dan tombol "Buat kelas" (karena `platform_admin` lolos tier), dikonfirmasi lewat screenshot.

---

### P32-005 — Redesign landing page: copy subject-agnostic + 3 kartu persona
**Status:** ✅ selesai dan teruji (2026-09-07)
**Depends on:** tidak ada (dikerjakan terakhir supaya copy-nya bisa merujuk fitur yang sudah nyata ada)

**Deskripsi**: `components/landing/landing-hero.tsx` — headline+badge CEFR/Bahasa-Inggris-spesifik ("Pre-Basic → C2", "menuju bahasa Inggris yang lancar") diganti copy subject-agnostic selaras pivot Phase 31. `app/page.tsx` — section baru "Pilih jalanmu" (3 kartu: Siswa/Guru/Organisasi, masing-masing dengan contoh dari user: siswa → kurikulum Indonesia/Cambridge/apa pun; guru → kelola kelas/waktu/sesi/bank soal; organisasi → kelola siswa/guru/lainnya), ketiganya link ke `/login` yang sama (lihat Keputusan scope §akhir). `HIGHLIGHTS` grid yang sudah ada juga dibersihkan dari sisa referensi "Pre-Basic sampai C2".

**DoD**: `npx tsc --noEmit` + `npx eslint src` bersih. Smoke test browser: screenshot pertama (setelah cold-compile Next dev) sempat menangkap hero kosong — false alarm murni timing Framer Motion pre-hydration pada compile pertama route `/`, bukan bug; screenshot ulang setelah warm-compile menunjukkan hero + 3 kartu persona + highlights render penuh dan benar.
