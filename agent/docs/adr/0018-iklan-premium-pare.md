# ADR-0018: Iklan & Premium di Kampung Bahasa Pare

Status: **Accepted** — disetujui user 2026-09-25 (harga, isi paket, penempatan iklan). Pembayaran QRIS asli menyusul; infrastruktur disiapkan dulu dengan `StubQrisProvider`. Asumsi §9 menunggu konfirmasi.
Date: 2026-09-25
Supersedes: -
Superseded by: -
Related: ADR-0016 (Kampung Bahasa Pare, §10.3 ekonomi terpisah), ADR-0005 (credit economy & langganan Titian), P9-007 (`PaymentProvider`/`StubQrisProvider`), P11-004 (`ad_views`)

> **Catatan migrasi (2026-10-05, ADR-0020):** backend sedang dipindah dari Rust ke Go. Keputusan di ADR ini tidak berubah; setiap "Rust" / `titian-backend-rust` / `services/pare_*.rs` di bawah berpadanan dengan `titian-backend-go/internal/pare/` setelah tiket G14. Sampai G14 selesai, kode Pare yang aktif tetap yang Rust.

## Context

Pare belum punya pemasukan uang sungguhan. Ekonomi game (Rupiah game, XP, nyawa, stamina) sengaja kecil: **uang hanya dari belajar** (ADR-0016). User ingin dua sumber pemasukan:

1. **Iklan Google** untuk pemain gratis.
2. **Premium Rp10.000/bulan** untuk menghapus iklan, dibayar lewat **QRIS**.

Perkiraan pendapatan iklan untuk pemain berat (2 jam/hari) di Indonesia adalah ± Rp4.500–15.000/bulan, dengan titik tengah ± Rp9.000. Jadi harga Rp10.000 kira-kira impas dengan iklan yang hilang. Angka ini perkiraan pasar, bukan data game, dan harus diukur ulang 2–4 minggu setelah iklan berjalan.

Yang sudah ada di backend dan dipakai ulang:
- `orders` + `PaymentProvider` (satu-satunya implementasi: `StubQrisProvider`) + `POST /payments/{payment_id}/webhook`. Alur ini sudah melayani pendaftaran kelas dan langganan Titian.
- `subscriptions` Titian (Plus Rp29rb, Pro Rp59rb), yang sudah menjanjikan "Belajar tanpa iklan".
- `pare_ledger` untuk semua perubahan uang, XP, dan nyawa.

## Decision

### 1. Jenis iklan: Google H5 Games Ads (Ad Placement API)

- Hanya **interstitial** dan **rewarded**. Banner AdSense biasa tidak ditempel di atas canvas game, karena rawan klik tak sengaja dan melanggar kebijakan.
- Penempatan:

| Posisi | Jenis |
|---|---|
| Nyawa tinggal ≤ 1 → "tonton iklan = +½ nyawa" | Rewarded (`heart`) |
| Pingsan → "tonton iklan = kembali ke tempat pingsan, tidak dikirim ke Camp" | Rewarded (`rescue`) |
| Hasil pelajaran → "tonton iklan = bayaran pelajaran ×2" | Rewarded (`double_pay`) |
| Setelah naik level / pindah zona | Interstitial, paling cepat 3 menit sekali |
| Layar judul / loader | Interstitial ringan |

- **Tidak boleh** ada iklan di tengah soal, ujian, chat, atau di dekat tombol sentuh.
- Rewarded **tidak pernah** memberi uang langsung dan tidak pernah melewati ujian. `double_pay` hanya melipatgandakan uang yang sudah didapat dari belajar.

### 2. Hadiah rewarded ditentukan dan diberikan server

H5 Games Ads tidak punya verifikasi server-side (tidak seperti AdMob SSV). Karena itu:

- Alurnya dua langkah. `POST /pare/boosts {kind, ref?}` mengecek syarat dan batas, lalu mengembalikan `{id, needs_ad}`. Klien memutar iklan bila `needs_ad`. Setelah itu `POST /pare/boosts/{id}/claim` menerapkan hadiah.
- Klaim lewat iklan ditolak bila kurang dari **15 detik** sejak dimulai. Token kedaluwarsa setelah **10 menit**.
- **Batas harian (WIB) per jenis: 3 kali.**
- Syarat per jenis:
  - `heart`: nyawa ≤ 1. Hadiahnya +½ nyawa.
  - `rescue`: paling lama 10 menit setelah pingsan dan masih di Camp. Pemain dikembalikan ke zona dan posisi saat pingsan.
  - `double_pay`: `ref` = kertas pelajaran milik sendiri yang sudah selesai, paling lama 10 menit setelah selesai, dan uang pelajaran itu > 0. Satu kertas hanya bisa digandakan sekali.
- Semua hadiah tercatat di `pare_ledger` (`kind = 'boost'`) dan di `pare_boosts`.

### 3. Premium Pare — Rp10.000 / 30 hari

| Isi | Keterangan |
|---|---|
| Tanpa iklan sama sekali | Interstitial dan rewarded tidak diputar |
| **Voucher Rp20.000 per periode 30 hari** | Hanya untuk kebutuhan hidup: makan, minum, laundry, sewa sepeda. **Tidak bisa untuk ujian.** Hangus di akhir periode, tidak menumpuk. |
| `heart` & `rescue` tanpa iklan | Batas harian sama (3×/hari) |
| `double_pay` **tidak ada** | Sudah digantikan voucher |

- Rp20.000 kira-kira setara 2–3 hari makan di Pare. Ini membuat hidup lebih santai tanpa menggantikan belajar.
- **Belanja memakai voucher dulu, baru uang.** Bila voucher + uang kurang, pembelian ditolak (`insufficient_money`).
- Premium adalah produk **terpisah** dari langganan Titian. Tabelnya `pare_premium`, bukan `subscriptions`, karena `subscriptions` hanya menyimpan satu tier per user. Dengan begitu pemain bisa punya Titian Plus dan Premium Pare sekaligus.
- **Perpanjangan saat masih aktif menambah 30 hari** ke akhir periode (tidak memotong sisa hari). Voucher diisi ulang ke Rp20.000 di awal setiap blok 30 hari. Isi ulang ini dihitung malas saat dibaca, tanpa cron.
- Harga, nilai voucher, dan batas harian adalah konstanta di `services/pare_premium.rs`, seperti angka ekonomi lain di `pare_economy.rs`.

### 4. Pembayaran: QRIS lewat alur `orders` yang sudah ada

- `orders.kind` ditambah `'pare_premium'` (butuh `user_id`, tanpa tier). `POST /pare/premium/checkout` membuat order, meminta payload QRIS ke `PaymentProvider`, dan membatalkan order Premium lama yang masih `pending`. Nominal selalu dari server.
- Klien memantau `GET /orders/{id}` sampai `paid`. Webhook yang sama (`/payments/{payment_id}/webhook`) mengaktifkan Premium lewat `pare_premium::activate`. Aktivasi ini idempoten per order.
- **Sampai gateway QRIS asli terpasang, yang dipakai tetap `StubQrisProvider`.** Webhook saat ini **publik tanpa tanda tangan**, jadi siapa pun yang tahu `payment_id` bisa menandai order lunas. Ini boleh untuk dev, tapi **wajib ditutup (verifikasi tanda tangan provider) sebelum Premium atau langganan Titian dibuka di produksi**. Pekerjaan ini masuk tiket P8-005.

### 5. Hak akses: satu tempat

`GET /pare/premium` → `{active, until, voucher, voucher_until, ad_free, price_idr, voucher_idr, boosts: {heart, rescue, double_pay: {used, cap}}}`.
- `ad_free` = Premium Pare aktif **atau** langganan Titian aktif (§9.1).
- `PlayerView` (`/pare/me`, dan setiap hasil aksi hidup) menyertakan `premium: {active, until, voucher, ad_free}` supaya HUD selalu sinkron.
- FE tidak memutuskan hak; FE hanya membaca `ad_free` / `needs_ad`.

### 6. Frontend: satu seam iklan

`alr/game` mendapat `src/game/ads.ts` dengan antarmuka `AdProvider { interstitial(placement), rewarded(placement): Promise<'viewed'|'skipped'|'unavailable'> }`. Implementasi awalnya `StubAdProvider` (dev), lalu `H5AdProvider` (`adBreak()` dari Ad Placement API) setelah akun AdSense for Games disetujui. ID klien AdSense disimpan di env (`NEXT_PUBLIC_ADSENSE_CLIENT`). Bila env kosong, iklan mati dan rewarded dianggap `unavailable`.

## Consequences

- (+) Pemasukan pertama Pare tanpa mengubah aturan "uang hanya dari belajar". Hadiah rewarded hanya menyelamatkan nyawa, posisi, atau menggandakan hasil belajar.
- (+) Memakai ulang `orders`/`PaymentProvider`/webhook, jadi gateway QRIS asli cukup dipasang di satu tempat untuk Titian dan Pare sekaligus.
- (+) Semua hadiah dan pemakaian voucher tercatat di ledger, sehingga bisa diaudit.
- (−) Tanpa SSV, klaim rewarded bisa dipalsukan oleh klien yang dimodifikasi. Dampaknya dibatasi ke 3×/hari per jenis dengan jeda minimal 15 detik.
- (−) Webhook publik tanpa tanda tangan adalah lubang yang sudah ada. Premium **tidak boleh** dibuka di produksi sebelum P8-005.
- (−) Voucher adalah saldo kedua di samping uang. UI perlu jelas menunjukkan mana yang dipakai.

## 9. Asumsi (menunggu konfirmasi user)

1. **Pelanggan Titian Plus/Pro juga bebas iklan di Pare** (sesuai janji "Belajar tanpa iklan"), tapi **tidak** mendapat voucher. `heart`/`rescue` mereka tanpa iklan, dan `double_pay` juga tanpa iklan.
2. Batas rewarded 3×/hari per jenis, jeda iklan 15 detik, jendela `rescue`/`double_pay` 10 menit.
3. Premium tidak otomatis diperpanjang. QRIS dibayar manual setiap bulan, dan game mengingatkan 3 hari sebelum habis (lewat push setelah Pare-5).
4. Target pemain bukan anak di bawah 13 tahun. Bila ada, iklan harus diset *child-directed* (pendapatan turun).


## 10. Pembaruan 2026-10-11: Plus, Pro, nyawa, BuatQris (keputusan user)

- **Dua paket 30 hari** menggantikan Premium: **Plus** Rp10.000 (harga coret Rp40.000) = bebas iklan, nyawa tak terbatas, bonus Rp20.000 uang game; **Pro** Rp30.000 (coret Rp120.000) = semua Plus + semua level terbuka (`GET /pare/path/{lang}?level=N`) + gratis ujian loncat level + bonus Rp100.000. Bonus (uang game) dibayar per pembelian, tidak hangus, dan menumpuk; voucher bulanan tidak lagi diberikan. Membeli Pro saat Plus aktif langsung beralih ke Pro; membeli Plus saat Pro aktif ditolak.
- **Nyawa**: 5; setiap jawaban salah (semua sesi kecuali ujian, dan misi) dan setiap pelanggaran aturan bahasa = −1; semua terisi penuh 24 jam setelah nyawa pertama hilang (`pare_players.hearts_lost_at`). Nyawa 0 = sesi dan misi ditolak (`no_hearts`); Materi, Kamus, chat, jalan-jalan tetap bisa. Challenge kesempatan terakhir dan bonus nyawa lewat iklan tidak ditawarkan lagi (iklan belum berjalan).
- **Ujian loncat** Rp20.000 uang game di semua level (gratis untuk Pro).
- **Pembayaran**: gateway bersifat pluggable (`economy.PaymentProvider`; tiap order mencatat `payment_provider`; webhook `/payments/{provider}/webhook`). BuatQris (`internal/economy/buatqris.go`) adalah provider pertama, dipilih lewat `PAYMENT_PROVIDER=buatqris` + `BUATQRIS_*` di `.env` server; menggantinya nanti tidak mengubah alur order. Webhook ditandatangani HMAC dan diverifikasi; webhook tanpa tanda tangan hanya untuk stub dev. Tanpa gateway, checkout ditolak (menutup lubang §4: webhook stub publik di produksi).
- **Paywall** dengan copy manfaat (bukan ajakan): muncul saat nyawa habis (selalu), saat nyawa berkurang (maks. sekali per 3 jam), dan saat stamina habis.
- **Papan iklan** menampilkan pesan sendiri (ajakan belajar, aturan bahasa, promo Plus/Pro, titianasa.com, @titianasa.app, @pare.titianasa); sponsor dimatikan sementara (`SPONSORS_ON` di `game/src/game/billboards.ts`).
- **Suara (tambahan 2026-10-11)**: mengirim voice note dan panggilan langsung, termasuk kuota telepon harian, adalah manfaat Plus/Pro; panggilan butuh paket aktif untuk semua peserta; mendengarkan voice note tetap terbuka untuk semua. Gerbang ADR-0017 lainnya (persetujuan, level, blokir, saling membalas) tetap berlaku.
- **Paywall menurut paket**: tanpa paket tampil Plus dan Pro; Plus aktif hanya Pro; Pro aktif hanya masa berlaku. Perpanjangan paket yang sama ditawarkan 7 hari sebelum habis.
