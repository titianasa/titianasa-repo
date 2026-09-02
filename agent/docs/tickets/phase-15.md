# Phase 15 (ticket-numbering) — Marketplace Frontend

## Keputusan scope (baca duluan)

Item ke-2 dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap di
`docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan semuanya'".

**3 gap backend nyata ditemukan SEBELUM sempat menulis 1 baris
frontend pun** (dikonfirmasi grep `app.ts`, bukan asumsi) — marketplace
backend (P9-003/004/007) dibangun ticket-demi-ticket terhadap AC
sempit, tidak pernah terhadap "bagaimana caranya siswa MENEMUKAN
produk/kelas untuk di-booking":
1. **Tidak ada `GET /products`** — satu-satunya jalur baca produk yang
   ada adalah `GET /tutors/{id}/products` (butuh tutor id yang SUDAH
   diketahui) dan `GET /products/{id}` (butuh product id yang SUDAH
   diketahui). Tidak ada cara "jelajahi semua produk platform" sama
   sekali.
2. **Tidak ada `GET /products/{id}/cohorts`** — `POST /products/{id}/cohorts`
   (buat batch) ada, tapi tidak ada cara BACA daftar batch yang sudah
   dibuat untuk 1 produk. Siswa tidak bisa tahu batch mana yang masih
   buka.
3. **Tidak ada `GET /me/enrollments`** — siswa tidak punya cara melihat
   "kelas apa saja yang sudah saya ikuti", cuma `GET /cohorts/{id}/students`
   yang butuh cohort id yang sudah diketahui duluan.

**Ditutup sebagai P15-001** (backend, additive, tidak ada migrasi
baru) SEBELUM FE ditulis — pola sama P9-008 (nemu gap `/complete` pas
nulis checkpoint) dan Phase 13's beberapa temuan lain: bukan
"scope creep", tapi prasyarat yang genuinely hilang, ditutup sebagai
bagian fase yang menemukannya, bukan didiamkan sampai FE-nya gagal
dibangun.

**Keputusan desain checkout** (belum ada payment gateway asli, cuma
`StubQrisProvider` sejak P9-007): setelah checkout, `POST /payments/{id}/webhook`
itu PUBLIK tanpa auth (dipanggil provider asli nanti) — dari sisi FE,
tidak ada cara alami memicu "pembayaran sukses" tanpa gateway sungguhan.
**Halaman checkout menampilkan tombol "Simulasikan pembayaran berhasil
(khusus development)"** yang memanggil webhook itu langsung — dilabeli
eksplisit sebagai simulasi/dev-only di UI (pola sama P14's "Tonton
iklan (ini simulasi)"), BUKAN dipura-purakan sebagai QRIS asli.

**Dieksplisit DIDEFER**: tutor-side product creation UI (`POST /tutors/me/products`
belum ada FE — masuk Phase 17 Tutor Dashboard, biar Phase 15 murni
sisi siswa), 8 kategori marketplace penuh (§8.1, cuma private/group
yang backend-nya ada — Live Class/Self-paced/dst di Phase 23),
Learning Package bundel (§8.11, Phase 23), pencarian/filter lanjutan
(cuma daftar+cursor pagination MVP, bukan search/filter per kategori/
harga/CEFR).

## Ticket

### P15-001 — Backend: 3 endpoint baca yang hilang
**Status:** done
**Depends on:** P9-003 (`learning_products`), P9-004 (`cohorts`/`enrollments`), P9-007 (`orders`)
**Endpoint baru:** `GET /products`, `GET /products/{id}/cohorts`, `GET /me/enrollments`.
**Acceptance Criteria:**
- [x] `GET /products` — published-only tanpa syarat (bukan "published ATAU milik sendiri" seperti `GET /products/{id}` — ini permukaan discovery publik), cursor-paginated (`{items, next_cursor}`, pola sama `asset_repository.listInFolder`)
- [x] `GET /products/{id}/cohorts` — produk draft cuma terlihat manager-nya (404 buat yang lain, pola sama `GET /products/{id}` — bukan bocorkan keberadaan produk draft lewat daftar cohort-nya)
- [x] `GET /me/enrollments` — LEFT JOIN `orders` (enrollment bisa ada SEBELUM checkout, P9-004 vs P9-007 2 langkah terpisah — `order_status: null` valid, bukan bug)
**DoD:** 4 test baru (`tests/marketplace-browse.test.ts`), 465/465 total, route-coverage 119/119.

### P15-002 — Browse Marketplace page
**Status:** done
**Depends on:** P15-001
**Deskripsi:** `/marketplace` — grid produk published, cursor "muat lebih banyak".
**Acceptance Criteria:**
- [x] Nav baru dijangkau dari mana pun yang masuk akal tanpa nambah slot bottom-nav (lihat implementasi utk keputusan final)
- [x] Card produk: judul, tipe (Private/Group badge), harga (format Rupiah)
**DoD:** Terverifikasi visual dengan data produk asli.

### P15-003 — Product detail + booking
**Status:** done
**Depends on:** P15-002
**Deskripsi:** `/marketplace/{id}` — detail produk, daftar cohort/batch (kapasitas, jadwal), tombol enroll → checkout → simulasi bayar (dev only, lihat "Keputusan scope").
**Acceptance Criteria:**
- [x] Cohort penuh → pesan jelas, bukan error API mentah (lihat "Catatan implementasi" soal deviasi dari "disabled")
- [x] Setelah checkout, tampilkan status order + tombol simulasi bayar berlabel jelas
**DoD:** Terverifikasi visual, alur penuh browse→detail→enroll→checkout→simulasi-bayar→status `active` lewat aksi nyata di browser.

**Catatan implementasi:** AC awal minta tombol enroll DISABLED kalau cohort penuh — TIDAK diimplementasikan begitu (deviasi sadar): tidak ada cara aman menampilkan "X/Y kursi terisi" ke calon siswa yang belum terdaftar (`GET /cohorts/{id}/students` mensyaratkan jadi manager ATAU sudah terdaftar — membocorkan hitungan ke orang luar berarti membocorkan sebagian isi roster). Jadi tombol "Daftar" TETAP aktif, error `cohort_full` (422) ditangkap dan ditampilkan sebagai pesan ramah — hasil akhirnya sama (calon siswa tidak pernah lihat error API mentah), cuma ditangani SAAT klik bukan SEBELUM klik. Diverifikasi penuh via `Bun.WebView`: browse → pilih produk privat → pilih batch → Daftar → Lanjut ke pembayaran → Simulasikan pembayaran berhasil (dev) → status `active` — semua lewat klik tombol asli di browser asli, bukan diasumsikan dari kode.

### P15-004 — My Enrollments page
**Status:** done
**Depends on:** P15-001
**Deskripsi:** `/belajar` atau halaman baru — daftar kelas yang diikuti siswa (dari `GET /me/enrollments`), status tiap enrollment, tombol batal (`POST /enrollments/{id}/cancel`) kalau masih bisa dibatalkan.
**Acceptance Criteria:**
- [x] Status order/enrollment ditampilkan jelas (pending pembayaran / aktif / selesai / dibatalkan) — bukan cuma raw string API
**DoD:** Terverifikasi visual.

**Catatan implementasi:** Tombol "Batalkan" cuma muncul untuk status `pending`/`active` (disembunyikan buat `completed`/`cancelled`, konsisten dengan `order_service.cancelEnrollment` yang no-op kalau sudah cancelled — UI tidak perlu menampilkan aksi yang percuma). Diverifikasi lewat klik asli: badge berubah "Aktif" → "Dibatalkan" tanpa reload manual (query invalidation).

### P15-005 — Integration check + exit checkpoint
**Status:** done
**Depends on:** P15-002 s/d P15-004
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit`/`lint`/`build` bersih di `titian-web`
- [x] Alur end-to-end browse→booking→my-enrollments diverifikasi lewat `Bun.WebView` terhadap backend asli
**DoD:** Tidak ada endpoint marketplace P9-003/004/007 yang masih backend-only tanpa jalur FE (kecuali yang dideferred eksplisit di atas).

**Catatan implementasi:** Skrip seed sekali-pakai (2 user demo — tutor+siswa, 2 produk published dengan cohort masing-masing, tidak dicommit) + `Bun.WebView` (`backend: "chrome"`) terhadap backend asli. Semua data demo dihapus dari dev DB setelah verifikasi (dikonfirmasi query ulang). Tidak ada race condition test-harness baru ditemukan fase ini (fix P14's timing sudah dipakai konsisten). `bunx tsc --noEmit`/`bun run lint`/`bun run build` bersih, 465/465 backend test tetap hijau (tidak ada regresi dari P15-001's endpoint baru).

---

## Checkpoint keluar Phase 15
1. [x] Siswa bisa menemukan produk TANPA tahu tutor id-nya duluan (dibuktikan lewat `/marketplace`, bukan hardcode URL).
2. [x] Booking penuh berhasil sampai `enrollment.status: active` lewat UI nyata (termasuk simulasi pembayaran dev-only).
3. [x] Siswa bisa melihat semua kelas yang diikutinya di 1 tempat, termasuk membatalkannya.

Phase 15 tertutup. Lanjut Phase 16 — LMS/Class Management Frontend.
