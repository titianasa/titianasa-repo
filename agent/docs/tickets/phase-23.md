# Phase 23 (ticket-numbering) — Marketplace Delivery Modes + Learning Package

## Keputusan scope (baca duluan)

Item ke-10 dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap di
`docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan semuanya'".
`docs/tickets/phase-12.md` sudah mendefer §8.1 (8 kategori marketplace)
dan §8.11 (Learning Package) penuh dengan alasan eksplisit — fase ini
membuka lagi keduanya dan memutuskan berapa banyak yang SEKARANG bisa
dibangun jujur, bukan menerima defer lama begitu saja.

**Kesalahpahaman yang diperbaiki dulu**: `learning_products.type`
(`private`/`group`) BUKAN dimensi yang sama dengan "8 kategori
marketplace" roadmap (Live Class/Self-paced/Bootcamp/Hybrid/Kids
Course) — `type` itu soal KAPASITAS (1-on-1 vs grup), kategori roadmap
itu soal MODE PENGIRIMAN (terjadwal vs mandiri vs intensif dst). Dua
dimensi ORTOGONAL, bukan pengganti satu sama lain — makanya kolom baru
(`delivery_mode`), bukan mengubah makna `type` yang sudah ada
(`type` menyentuh CHECK constraint + capacity-by-type logic, mengubah
maknanya butuh ADR; menambah kolom baru additive tidak).

**Temuan kunci: "Live Class" sebenarnya SUDAH ada** — cohort + jadwal +
attendance (P9-004/P9-005) itu SENDIRINYA sudah persis "kelas
langsung/terjadwal". Yang genuinely hilang cuma cara link ke platform
video eksternal (Zoom/Meet/dst) — bukan "integrasi video-conference"
(WebRTC tertanam, yang memang butuh infra besar tidak ada), tapi
sesederhana `cohorts.meeting_url` (link yang tutor tempel sendiri).
Ini jujur soal apa yang bisa dibangun sekarang vs yang genuinely
butuh SDK/kredensial pihak ketiga (sama kelas keputusan dengan
payment gateway/ad SDK: stub sampai user sediakan kredensial produksi
— bedanya di sini TIDAK BUTUH stub sama sekali, link eksternal cukup).

**4 dari 5 kategori dibangun, 1 TETAP didefer**:
1. **Live Class** — sudah ada (cohort+jadwal+attendance), ditambah
   `meeting_url` opsional di cohort.
2. **Self-paced** — `delivery_mode='self_paced'`, reuse 100% mesin
   enrollment/payment/certificate yang ada. Bedanya cuma di FE: cohort
   tunggal yang tidak perlu dipilih manual, attendance tidak relevan
   ditampilkan.
3. **Bootcamp** — cuma label (`delivery_mode='bootcamp'`) di atas
   mekanisme cohort/jadwal yang SUDAH ADA. Sumbernya sendiri cuma
   bilang "aturan jadwal intensif" tanpa aturan konkret apa pun — jadi
   tutor sudah bisa membuat jadwal intensif lewat `cohorts.schedule`
   (jsonb bebas) yang ada sejak P9-004; label ini murni penanda
   kategori, BUKAN mesin validasi jadwal baru yang dipaksakan dari
   spek yang tidak ada.
4. **Hybrid** — sama, cuma label (`delivery_mode='hybrid'`) — sumbernya
   juga tidak kasih perilaku beda apa pun untuk hybrid selain "gabungan
   online+offline", yang mesin cohort+attendance yang ada sudah cukup
   general untuk itu.
5. **Kids Course — TETAP DIDEFER**, bukan infra blocker seperti 3 yang
   di atas tadinya dikira — ini keputusan POSISI PRODUK yang sudah
   ditunda BERULANG KALI sejak Phase 3/6/8 dengan alasan SAMA PERSIS:
   *"tunda kalau target awal bukan Kids"* (kata roadmap sendiri) dan
   belum ada konfirmasi eksplisit dari user bahwa Kids adalah target
   awal. Kelas keputusan sama dengan §8.10 (Student Diagnosis) — di
   luar kewenangan dipotong MVP begitu saja, TIDAK ditanyakan sekarang
   supaya tidak menghentikan urutan 14 item yang sudah diminta, dicatat
   di sini + `docs/STATE.md` supaya tidak diasumsikan selesai.

**Learning Package (§8.11) — DIBANGUN, scope dipersempit dari
deskripsi asli.** Mekanisme "N sesi, redeem satu-satu" diimplementasi
dengan REUSE PENUH `attendance_records` yang sudah ada sebagai
mekanisme "redeem": `delivery_mode='package'` + `session_count` di
produk, `enrollments.sessions_remaining` diisi dari `session_count`
saat enrollment dibuat, lalu **setiap kali attendance MENJADI
'present'** (transisi, bukan setiap panggilan — re-mark tanggal yang
sama tidak dobel-kurangi, batal-present balikin sesi) untuk enrollment
package, `sessions_remaining` berkurang 1 lewat endpoint attendance
YANG SUDAH ADA (`POST /cohorts/{id}/sessions/{date}/attendance`) —
BUKAN endpoint booking-per-sesi baru yang terpisah. Ini secara jujur
lebih sempit dari deskripsi asli §8.11 (yang membayangkan booking slot
waktu fleksibel di masa depan) — MVP ini mengasumsikan sesi package
tetap dijadwal via cohort (sama seperti kelas biasa), cuma jumlah
sesinya terbatas & terlacak. Booking-slot-fleksibel (siswa pilih sendiri
tanggal per sesi tanpa cohort tetap) **dieksplisit DIDEFER** sebagai
peningkatan terpisah — precedent-nya belum ada di skema manapun dan
akan butuh keputusan desain sendiri.

## Ticket

### P23-001 — Backend: delivery_mode + meeting_url
**Status:** done
**Depends on:** P9-003 (`learning_products`), P9-004 (`cohorts`)
**Tabel diubah (additive, tanpa ADR — kolom baru, bukan ubah makna kolom lama):** `learning_products.delivery_mode`, `cohorts.meeting_url`.
**Acceptance Criteria:**
- [x] Produk lama (dibuat sebelum ticket ini) otomatis `delivery_mode='live_class'` — tidak ada perubahan perilaku
- [x] `POST /tutors/me/products` terima `delivery_mode` opsional (default `live_class`), validasi 5 nilai yang diizinkan
- [x] `POST /products/{id}/cohorts` terima `meeting_url` opsional
**DoD:** test baru di `tests/marketplace-delivery-mode.test.ts`.

### P23-002 — Backend: Learning Package (redeem lewat attendance)
**Status:** done
**Depends on:** P23-001, P9-005 (`attendance_records`)
**Kolom baru (additive):** `enrollments.sessions_remaining`.
**Acceptance Criteria:**
- [x] `session_count` wajib diisi (>0) kalau `delivery_mode='package'`, harus kosong untuk mode lain (validasi sama pola capacity-by-type)
- [x] Enroll ke produk package → `sessions_remaining` = `session_count` produk
- [x] Attendance jadi 'present' pertama kali → `sessions_remaining` -1; jadi 'present' LAGI di tanggal yang sama (re-mark) → TIDAK dikurangi lagi; berubah dari 'present' ke status lain → `sessions_remaining` +1 (dikembalikan)
- [x] `sessions_remaining` tidak pernah negatif (diclamp di 0)
- [x] `sessions_remaining` muncul di `GET /me/enrollments` dan `GET /cohorts/{id}/students`
**DoD:** test baru di `tests/marketplace-delivery-mode.test.ts` (file sama, 1 ticket-phase).

### P23-003 — Frontend: buat produk dengan delivery mode + package, tampilan sesi tersisa
**Status:** done
**Depends on:** P23-001, P23-002
**Acceptance Criteria:**
- [x] Form "Buat Produk" (`/mengajar`) punya pilihan delivery mode, field `session_count` cuma muncul kalau pilih Paket
- [x] Form buat batch/cohort punya field opsional "Link Meeting" (untuk Live Class)
- [x] Badge delivery mode tampil di kartu produk marketplace dan halaman detail
- [x] "Kelas Saya" (`GET /me/enrollments`) tampilkan progress sesi tersisa untuk enrollment package
- [x] Roster tutor (`AttendancePanel`) tampilkan sisa sesi per siswa package
**DoD:** Diverifikasi lewat `Bun.WebView` — lihat P23-004.

### P23-004 — Integration check + exit checkpoint
**Status:** done
**Depends on:** P23-001 s/d P23-003
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit`/`lint`/`build` bersih di `titian-web`
- [x] `bun test` bersih di `titian-backend-bun`, tidak ada regresi
**DoD:** Diverifikasi end-to-end lewat `Bun.WebView` — tutor buat produk Paket 3 sesi → siswa enroll & bayar → sesi tersisa 3 → tutor tandai hadir 1x → sesi tersisa 2 (real, bukan simulasi) → tandai hadir tanggal SAMA lagi → tetap 2 (tidak dobel kurang). Skrip seed sekali-pakai, dihapus + data dibersihkan setelah.

---

## Checkpoint keluar Phase 23
1. [x] Tutor bisa membuat produk dengan 5 kategori delivery mode (4 dibangun jujur di atas mesin yang ada, 1 murni label baru untuk Live Class yang sudah ada).
2. [x] Learning Package benar-benar melacak sesi terpakai dari data attendance NYATA, bukan angka statis atau simulasi — dikonfirmasi lewat siklus tandai-hadir-berkurang, re-mark-tidak-dobel, batal-kembali.
3. [x] Kids Course TETAP didefer dengan alasan tercatat eksplisit (keputusan posisi produk, bukan potongan MVP) — bukan diam-diam dilewati.
4. [x] Booking-slot-fleksibel untuk package (versi penuh §8.11) didokumentasikan sebagai scope yang sengaja dipersempit, bukan diklaim selesai.

Phase 23 tertutup. Lanjut Phase 24 — AI Content Generation Pipeline + Content Factory.
