# Phase 16 (ticket-numbering) — LMS/Class Management Frontend

## Keputusan scope (baca duluan)

Item ke-3 dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap di
`docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan semuanya'".

**3 gap backend nyata ditemukan saat menulis FE ini** (pola sama
Phase 15 — backend LMS P9-004/005 + P12-002/003 dibangun ticket-demi-
ticket terhadap AC sempit, belum pernah terhadap "apa yang tutor/siswa
benar-benar butuhkan untuk pakai fitur ini"):
1. **Roster/gradebook cuma balikin `student_id` mentah** —
   `GET /cohorts/{id}/students` dan `GET /cohorts/{id}/gradebook`
   tidak pernah JOIN ke `users`, jadi tutor cuma lihat deretan UUID,
   bukan nama. Ditutup: `enrollment_repository.listByCohortWithStudent`
   baru, `student_name`/`student_email` ditambah ke kedua response
   (aditif, tidak menghapus field lama).
2. **`GET /assignments/{id}/submissions` TIDAK PERNAH ADA** —
   `assignment_submission_repository.listByAssignment` sudah ada sejak
   P12-002 tapi TIDAK PERNAH dipanggil endpoint/service manapun
   (dikonfirmasi grep) — dead code. Akibatnya `POST /submissions/{id}/grade`
   ada tapi tutor tidak punya cara TAHU `submission_id` apa yang mau
   dinilai. Ditutup dengan endpoint baru.
3. **Endpoint baru itu awalnya manager-only, lalu ketauan gap KEDUA
   pas testing FE**: siswa juga butuh cara BACA status submission-nya
   sendiri (nilai/feedback) yang BERTAHAN lintas reload — versi
   pertama FE cuma nyimpen status itu di state React lokal
   (`mutation.data`), hilang begitu halaman di-refresh. Diperbaiki
   dengan memperlebar endpoint yang SAMA: manager lihat semua, siswa
   terenroll lihat baris miliknya sendiri saja (pola persis
   `GET /cohorts/{id}/students`/`GET /cohorts/{id}/attendance`), bukan
   endpoint kedua.

**Keputusan navigasi**: 1 route `/marketplace/kelas/{cohortId}`
melayani DUA tampilan berbeda (tutor vs siswa) — dibedakan dari sinyal
`GET /cohorts/{id}/gradebook` yang 403 buat siapa pun BUKAN manager
(satu-satunya endpoint cohort-scoped yang MENOLAK bukan bercabang),
bukan duplikasi logic `canManageCohorts` di frontend. Siswa masuk dari
"Kelas Saya" (Phase 15), tutor masuk dari halaman detail produknya
sendiri (`/marketplace/{id}` mendeteksi `product.tutor_id === me.id`
lalu menukar alur booking dengan tombol "Kelola" per batch).

**Dieksplisit DIDEFER**: "My Teaching" — daftar produk/cohort tutor
sebagai TITIK MASUK tersendiri (bukan cuma via URL produk yang sudah
diketahui) — itu Phase 17 (Tutor Dashboard)'s tanggung jawab eksplisit.
Messaging/komentar per submission (butuh sistem pesan yang tidak ada,
Phase 22). QR/Geolocation attendance (§8.5, cuma manual method yang
backend-nya ada).

## Ticket

### P16-001 — Backend: nama siswa di roster & gradebook
**Status:** done
**Depends on:** P9-004 (`enrollments`), P12-003 (`gradebook`)
**Acceptance Criteria:**
- [x] `enrollment_repository.listByCohortWithStudent` baru (JOIN `users`)
- [x] `GET /cohorts/{id}/students` dan `GET /cohorts/{id}/gradebook` dapat `student_name`/`student_email` — aditif, field lama tidak berubah
**DoD:** Test lama tetap hijau (assert `.student_id`/`.length`, bukan deep-equal objek utuh — aman ditambah field), 2 assert baru (`student_name` truthy).

### P16-002 — Backend: discovery submission untuk dinilai + dibaca siswa sendiri
**Status:** done
**Depends on:** P12-002 (`assignment_submissions`)
**Endpoint baru:** `GET /assignments/{id}/submissions`.
**Acceptance Criteria:**
- [x] Manager (tutor/org-admin) lihat SEMUA submission + nama siswa
- [x] Siswa terenroll lihat SATU baris (miliknya sendiri) atau list kosong (belum submit) — BUKAN 403
- [x] Bukan siswa terenroll & bukan manager → 403
**DoD:** 4 test baru (`tests/assignment.test.ts`), 469/469 total, route-coverage 120/120.

### P16-003 — Cohort Detail: tampilan siswa + tutor
**Status:** done
**Depends on:** P16-001, P16-002
**Deskripsi:** `/marketplace/kelas/{cohortId}` — 1 route, `GET /cohorts/{id}/gradebook`'s 403 jadi sinyal tutor-vs-siswa. Siswa: kehadiran% + daftar tugas (submit/lihat nilai). Tutor: tab Kehadiran (tandai hari ini)/Tugas (buat+lihat jawaban+nilai)/Nilai (gradebook).
**Acceptance Criteria:**
- [x] Siswa: status submission (belum kirim/menunggu dinilai/sudah dinilai+feedback) BERTAHAN lintas reload, bukan cuma state lokal setelah submit
- [x] Tutor: tandai kehadiran, buat tugas, lihat+nilai jawaban per siswa (dengan nama, bukan UUID), lihat gradebook
- [x] Product detail page (`/marketplace/{id}`) menukar alur booking jadi tombol "Kelola" per batch kalau `product.tutor_id === me.id`
**DoD:** Diverifikasi end-to-end lewat `Bun.WebView`: tutor tandai hadir → buat tugas → siswa submit → tutor nilai → siswa lihat nilai (reload) → gradebook tutor menggabungkan attendance+tugas dengan benar (94 = rata2 100+88).

**Catatan implementasi:** **1 bug test-script ditemukan & diperbaiki saat verifikasi (bukan bug aplikasi)**: tombol grade "Nilai" di dalam baris submission punya teks PERSIS SAMA dengan tab trigger "Nilai" di atasnya — skrip verifikasi awal yang cuma cari `button` by exact text grab elemen pertama (tab trigger), bukan tombol grade, sehingga klik pertama gagal diam-diam (menavigasi ke tab lain, bukan submit nilai). Diperbaiki dengan scoping pencarian tombol ke dalam baris submission itu sendiri — tidak relevan buat pengguna asli (dua elemen itu terlihat jelas beda posisi/style di layar), murni artefak otomasi klik-by-text. **1 bug REAL ditemukan** (dijelaskan di P16-002 di atas): versi awal `StudentClassView` cuma nyimpen hasil submit di state mutation lokal, ketauan lewat reload manual di skrip verifikasi (bukan diasumsikan) — ditutup sebelum ticket ini ditandai selesai, bukan dicatat sebagai keterbatasan. Server backend juga sempat perlu di-restart manual pas verifikasi karena `bun run src/index.ts` tanpa `--watch` tidak hot-reload perubahan source — dicatat sebagai pengingat proses, bukan bug.

### P16-004 — Integration check + exit checkpoint
**Status:** done
**Depends on:** P16-001 s/d P16-003
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit`/`lint`/`build` bersih di `titian-web`
- [x] `bun test` bersih di `titian-backend-bun` (469/469, tidak ada regresi)
**DoD:** Skrip seed sekali-pakai (tutor+siswa+cohort+assignment, tidak dicommit) dipakai buat verifikasi, dihapus + data dibersihkan dari dev DB setelahnya.

---

## Checkpoint keluar Phase 16
1. [x] Tutor bisa menjalankan siklus penuh 1 kelas (tandai hadir → buat tugas → nilai jawaban) tanpa pernah melihat UUID mentah di UI.
2. [x] Siswa bisa lihat kehadiran% dan status tugasnya (termasuk nilai) yang BERTAHAN setelah reload halaman.
3. [x] Gradebook tutor menggabungkan attendance+tugas dengan benar, diverifikasi dengan angka nyata (bukan diasumsikan dari kode).

Phase 16 tertutup. Lanjut Phase 17 — Tutor Dashboard + Reputation/Reviews Frontend.
