# Phase 17 (ticket-numbering) — Tutor Dashboard + Reputation/Reviews Frontend

## Keputusan scope (baca duluan)

Item ke-4 dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap di
`docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan semuanya'".

**1 gap backend KRITIS ditemukan sebelum sempat menyelesaikan FE ini**
(pola sama Phase 15/16 — ketiga kalinya berturut-turut backend
marketplace dibangun terhadap AC sempit, bukan alur pemakaian nyata):
**`learning_products.create` SELALU insert `status='draft'`
(default kolom), dan TIDAK ADA function/endpoint MANAPUN yang pernah
mengubahnya ke `published`** (dikonfirmasi grep repository — nol
fungsi update/publish sama sekali sejak P9-003). Tanpa ini, "Buat
Produk" yang jadi tugas ticket ini akan jadi JALAN BUNTU MUTLAK: produk
yang dibuat tutor tidak akan PERNAH muncul di `GET /products` (Phase
15's marketplace browse, published-only tanpa syarat). Ditutup sebagai
**P17-001**: `POST /products/{id}/publish` baru, ownership-only,
idempotent — SEBELUM UI "Buat Produk" ditulis, bukan sesudah ketemu
buntu di FE.

**Keputusan lingkup "My Teaching"**: satu halaman `/mengajar` (bukan
beberapa) menggabungkan SEMUA yang Phase 15/16 sengaja deferred:
wallet (`GET /tutors/me/wallet`), buat produk (`POST /tutors/me/products`
+ publish baru), buat batch (`POST /products/{id}/cohorts` — sudah ada
sejak P9-004, TIDAK PERNAH punya UI sampai sekarang), link "Kelola" ke
`/marketplace/kelas/{cohortId}` (reuse penuh Phase 16, nol kode baru
di situ). Entry point: item menu baru "Mengajar" di dropdown TopBar,
muncul HANYA untuk `role === 'tutor'` (mengikuti pola `canAccessStudio`
yang sudah ada untuk Content Studio).

**Keputusan "Tandai Selesai" sebagai bagian ticket ini, bukan
di-skip**: alur review (P12-004) SECARA STRUKTURAL butuh
`enrollment.status === 'completed'`, tapi TIDAK ADA UI manapun yang
bisa mencapai status itu — `POST /cohorts/{id}/enrollments/{id}/complete`
(P9-008) exist di backend sejak lama tapi baru dipakai lewat test/API
langsung. Kalau tombol ini tidak ditambahkan sekarang, seluruh
P17-003 (review) TIDAK BISA DIVERIFIKASI sama sekali lewat UI nyata —
jadi ditambahkan ke `AttendancePanel` (Phase 16's tutor view) sebagai
prasyarat, bukan scope creep.

**Dieksplisit DIDEFER**: withdraw/pencairan wallet (`payout_withdrawn`
belum pernah punya writer di backend manapun, dicatat sejak P9-007),
edit/arsip produk setelah publish, upload gambar produk (tidak ada
kolom `image_url` di skema), balas ulasan (tutor merespons review
siswa — bukan bagian P12-004's AC).

## Ticket

### P17-001 — Backend: endpoint publish produk yang hilang
**Status:** done
**Depends on:** P9-003 (`learning_products`)
**Endpoint baru:** `POST /products/{id}/publish`.
**Acceptance Criteria:**
- [x] Ownership-only (`product.tutorId === ctx.userId`), 404 (bukan 403) buat yang lain — pola sama `getProduct`'s "jangan bocorkan keberadaan produk draft orang lain"
- [x] Idempotent — publish produk yang sudah `published` no-op, bukan error
**DoD:** 3 test baru (`tests/learning-product.test.ts`), 472/472 total, route-coverage 121/121.

### P17-002 — "Mengajar": wallet, buat produk, buat batch
**Status:** done
**Depends on:** P17-001, P9-004 (`cohorts`), P9-007 (`wallet`)
**Deskripsi:** `/mengajar` — saldo wallet, form buat produk (draft) + tombol terbitkan, daftar produk sendiri dengan cohort per produk + form buat batch baru, link "Kelola" ke halaman Phase 16.
**Acceptance Criteria:**
- [x] Entry point dari dropdown TopBar, muncul cuma untuk role `tutor`/`platform_admin`
- [x] "Tandai Selesai" ditambahkan ke `AttendancePanel` (Phase 16) — prasyarat P17-003
**DoD:** Diverifikasi end-to-end: buat produk → terbitkan → MUNCUL di `GET /products` asli (bukan diasumsikan) → buat batch → link Kelola berfungsi.

### P17-003 — Ulasan + Reputasi
**Status:** done
**Depends on:** P12-004 (`tutor_reviews`), P17-002 ("Tandai Selesai")
**Deskripsi:** Form ulasan (1-5 bintang + komentar) muncul di "Kelas Saya" untuk enrollment `completed`; badge reputasi (rating+jumlah siswa) di halaman detail produk.
**Acceptance Criteria:**
- [x] Ulasan ganda (409 `already_reviewed`) ditangani jadi pesan "sudah pernah", bukan error mentah
- [x] Badge reputasi tersembunyi kalau `review_count: 0` (bukan tampilkan "0.0 dari 0 ulasan" yang terlihat seperti tutor jelek)
**DoD:** Diverifikasi end-to-end: siswa beri ulasan 5 bintang → `GET /tutors/{id}/reputation` asli balikin `average_rating: 5, review_count: 1` → badge muncul di halaman produk.

### P17-004 — Integration check + exit checkpoint
**Status:** done
**Depends on:** P17-001 s/d P17-003
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit`/`lint`/`build` bersih di `titian-web`
- [x] `bun test` bersih di `titian-backend-bun` (472/472, tidak ada regresi)
**DoD:** Skrip seed sekali-pakai (tutor+siswa+produk terbit+enrollment completed+wallet payout, tidak dicommit) dipakai buat verifikasi, dihapus + data dibersihkan dari dev DB setelahnya.

---

## Checkpoint keluar Phase 17
1. [x] Tutor bisa membuat produk BARU dari nol lewat UI dan produk itu benar-benar bisa ditemukan siswa lain (bukan cuma tersimpan sebagai draft selamanya).
2. [x] Saldo wallet yang ditampilkan cocok PERSIS dengan split 70% P9-007 (dibuktikan dengan angka nyata dari data seed, Rp84.000 dari harga Rp120.000).
3. [x] Siswa bisa memberi ulasan setelah kelasnya selesai, dan reputasi tutor ter-update DAN terlihat di halaman produk — alur penuh, bukan potongan terpisah.

Phase 17 tertutup. Lanjut Phase 18 — Organization Admin Frontend.
