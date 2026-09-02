# Phase 19 (ticket-numbering) — Certificates Frontend

## Keputusan scope (baca duluan)

Item ke-6 dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap di
`docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan semuanya'".

**1 gap backend + 2 bug backend nyata ditemukan** — pola sama fase-fase
sebelumnya, kali ini campuran gap fitur DAN bug response-shape:

1. **Gap: sertifikat TIDAK BISA DIBACA ULANG setelah diterbitkan.**
   `certificate_repository.findByEnrollmentId` (P9-006) cuma pernah
   dipakai INTERNAL untuk cek konflik re-issue — tidak pernah jadi
   endpoint baca. Siswa pemilik sertifikat tidak punya cara melihatnya
   lagi setelah respons POST issue yang cuma sekali itu, kecuali sudah
   tahu kodenya duluan buat lewat verify publik. Ditutup: `GET /enrollments/{id}/certificate`
   baru (`{issued: false}` kalau belum terbit — bukan bare `null`, pola
   sama `GET /subscriptions/me`).
2. **Bug: `GET /organizations/{id}/tutors` JUGA balikin `userId` (camelCase)**,
   bug KELAS SAMA persis dengan yang ditemukan P18-001 di
   `GET /organizations/{id}/members` — ditemukan sambil cek endpoint
   terkait sebelum membangun FE ini, BUKAN reaktif setelah gagal.
   Ditutup dengan cara sama: tambah mapping snake_case, `api-contract.md`
   juga diperbaiki (dokumennya sendiri salah sejak awal, ikut
   camelCase yang salah, bukan cuma kodenya).

**Keputusan arsitektur penting: halaman verifikasi HARUS di luar
`(app)` route group.** Seluruh app dibungkus `RequireAuth` — kalau
halaman verifikasi ditaruh di dalam grup itu, orang tanpa akun Titian
Asa (siapa pun yang scan QR code sertifikat) akan dilempar ke halaman
login duluan, PADAHAL `GET /certificates/{code}/verify` backend-nya
sendiri sengaja publik tanpa auth sejak P9-006. Ditaruh di
`src/app/verifikasi/[code]/page.tsx` (setingkat dengan `/login`, bukan
di dalam `(app)`).

**Keputusan "Terbitkan Sertifikat" ditambahkan ke Phase 16's tutor
view, bukan halaman baru**: satu-satunya jalan mencapai
`enrollment.status='completed'` sudah ada di `AttendancePanel`
(P17-002's "Tandai kelas selesai") — aksi terbitkan sertifikat
ditaruh persis di situ, konteksnya sudah pas (per-siswa, per-baris).

**Dieksplisit DIDEFER**: unduh sertifikat sebagai PDF/gambar (tidak
ada generator PDF di backend manapun), custom desain sertifikat
visual (halaman verifikasi cukup teks terstruktur, bukan render
sertifikat bergambar).

## Ticket

### P19-001 — Backend: baca sertifikat + 2 perbaikan response shape
**Status:** done
**Depends on:** P9-006 (`certificates`)
**Endpoint baru:** `GET /enrollments/{id}/certificate`.
**Acceptance Criteria:**
- [x] Pemilik (siswa) ATAU manager cohort (tutor/org-admin) bisa baca; yang lain 403
- [x] `{issued: false}` untuk enrollment completed yang belum diterbitkan sertifikatnya — bukan error, bukan `null`
- [x] `GET /organizations/{id}/tutors` diperbaiki jadi `user_id` (snake_case), `api-contract.md` ikut diperbaiki
**DoD:** 8 test baru (`tests/certificate.test.ts` + `tests/tutor.test.ts`), 476/476 total, route-coverage 122/122.

### P19-002 — Terbitkan + lihat sertifikat (tutor & siswa)
**Status:** done
**Depends on:** P19-001, P17-002 ("Tandai kelas selesai")
**Deskripsi:** Tombol "Terbitkan Sertifikat" di `AttendancePanel` (tutor) untuk enrollment `completed`; card sertifikat di `StudentClassView` (siswa) begitu terbit, dengan link ke halaman verifikasi publik.
**Acceptance Criteria:**
- [x] Tutor tidak melihat tombol terbit lagi begitu sudah diterbitkan (cek `GET /enrollments/{id}/certificate` duluan) — mencegah percobaan re-issue yang 409
- [x] Card sertifikat siswa cuma muncul kalau BENAR sudah terbit, bukan placeholder "belum terbit" yang mengotori tampilan
**DoD:** Diverifikasi end-to-end: tutor terbitkan → siswa lihat di kelasnya (termasuk estimasi CEFR asli dari data mastery, bukan hardcode) → link ke halaman verifikasi.

### P19-003 — Halaman verifikasi publik
**Status:** done
**Depends on:** P19-001
**Deskripsi:** `/verifikasi/{code}` — di luar `(app)`, tanpa auth, tanpa bottom-nav/top-bar.
**Acceptance Criteria:**
- [x] Kode valid → nama siswa, judul kursus, tanggal selesai
- [x] Kode tidak valid/tidak ada → pesan jelas, bukan crash/blank page
**DoD:** Diverifikasi lewat browser TANPA localStorage/sesi login sama sekali (persis pengunjung asing yang scan QR code) — dites eksplisit kode valid dan kode palsu.

### P19-004 — Integration check + exit checkpoint
**Status:** done
**Depends on:** P19-001 s/d P19-003
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit`/`lint`/`build` bersih di `titian-web`
- [x] `bun test` bersih di `titian-backend-bun` (476/476, tidak ada regresi)
**DoD:** Skrip seed sekali-pakai (tutor+siswa+enrollment completed+mastery utk CEFR asli, tidak dicommit) dipakai buat verifikasi, dihapus + data dibersihkan dari dev DB setelahnya.

---

## Checkpoint keluar Phase 19
1. [x] Tutor bisa menerbitkan sertifikat lewat UI, dan sistem mencegah penerbitan ganda secara visual (bukan cuma backend 409).
2. [x] Siswa bisa melihat sertifikatnya SETELAH RELOAD (bukan cuma state sesaat setelah aksi tutor), termasuk estimasi CEFR nyata dari mastery data.
3. [x] Siapa pun (TANPA login) bisa memverifikasi sertifikat lewat kode — dibuktikan lewat sesi browser yang benar-benar tidak punya sesi Titian Asa sama sekali.

Phase 19 tertutup. Lanjut Phase 20 — Proctoring Frontend.
