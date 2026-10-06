# Tiket Pare-8 — Iklan & Premium

> **Catatan migrasi backend (2026-10-05, ADR-0020):** backend sedang dipindah ke Go. Tiket ini ditulis untuk `titian-backend-rust`, dan kode Rust tetap yang aktif sampai domain ini diport (G14, lihat `phase-51-go-migration.md`). Pekerjaan yang belum dieksekusi: bila G14 sudah selesai saat tiket ini dikerjakan, kerjakan di `titian-backend-go` (`#[sqlx::test]` → test Go dengan `testdb.New`, `services/x.rs` → `internal/<domain>/`); bila belum, kerjakan di Rust dan catat endpoint/migrasi barunya di daftar paritas fase 51.

📋 **P8-001…004 SELESAI KODE (2026-09-25; dilanjutkan sesi lain setelah sesi awal dihentikan), P8-005 menunggu provider.** — [ADR-0018](../adr/0018-iklan-premium-pare.md) Accepted. Keputusan user: Premium **Rp10.000/30 hari** = tanpa iklan sama sekali + **voucher Rp20.000** untuk kebutuhan hidup (bukan ujian, hangus tiap periode) + `heart`/`rescue` tanpa iklan. Pembayaran **QRIS menyusul**: infrastruktur dulu dengan `StubQrisProvider`. Asumsi ADR-0018 §9 menunggu konfirmasi.

Repo yang disentuh: `titian-backend-rust` (migrasi **0084**, `/pare/premium*`, `/pare/boosts*`, cabang `pare_premium` di `orders`), `alr/game` (seam iklan, layar Premium, tombol rewarded). `titian-web` tidak disentuh.

> Migrasi 0084 dipakai Pare-8, 0085 dipakai Pare-5 (push). Rencana Pare-7 (suara, belum ada kode) bergeser ke **0086**.

## Aturan main eksekusi
Sama seperti Pare-1…4: migrasi aditif & idempoten, test integrasi `#[sqlx::test]` per tiket, angka ekonomi hanya di server, jangan commit tanpa diminta, hari dihitung WIB.

## Yang WAJIB dipertahankan
- Rewarded tidak pernah memberi uang langsung dan tidak melewati ujian.
- Voucher tidak bisa dipakai untuk ujian dan tidak menumpuk.
- Semua hadiah dan pemakaian voucher tercatat di `pare_ledger`.
- **Premium tidak dibuka di produksi sebelum P8-005** (webhook publik tanpa tanda tangan).

---

## P8-001 — Skema, Premium, checkout (M)

✅ **SELESAI.** Test `tests/integration/pare_premium_test.rs`: checkout → webhook → aktif + voucher Rp20.000, webhook diulang tidak memperpanjang, perpanjangan saat aktif = +30 hari, habis = tanpa voucher.
Migrasi `0084_pare_premium.sql`: `orders.kind` + `'pare_premium'` (butuh `user_id`); `pare_premium(user_id, period_start, period_end, voucher, voucher_until, last_order_id)`; `pare_players.fainted_at/faint_zone/faint_pos`; `pare_ledger.delta_voucher`; `pare_boosts(id, user_id, kind, via, ref, day, started_at, claimed_at)`.
`services/pare_premium.rs`: `activate` (baru = 30 hari + voucher; aktif = +30 hari; idempoten per order), isi ulang voucher per blok 30 hari saat dibaca, `status`/`ad_free`. `POST /pare/premium/checkout` (order + QRIS stub, batalkan pending lama), `GET /pare/premium`. Webhook `orders` mengaktifkan Premium; `GET /orders/{id}` untuk pemilik.
**DoD:** test checkout → webhook → aktif + voucher Rp20.000; webhook kedua tidak memperpanjang lagi; perpanjangan saat aktif = +30 hari; voucher terisi ulang di blok berikutnya dan hangus setelah Premium habis.

## P8-002 — Belanja memakai voucher (S)

✅ **SELESAI.** Test: voucher penuh, campuran voucher + uang (sepeda Rp2.500 = voucher 1.500 + uang 1.000), kurang → `insufficient_money`, ujian tetap hanya uang.
`buy`, `laundry`, `bike` membayar lewat `pare_premium::pay`: voucher dulu, baru uang; kurang = `insufficient_money`. Ledger `kind='spend'` mencatat `delta_money` dan `delta_voucher`. Ujian tetap hanya uang. `PlayerView.premium {active, until, voucher, ad_free}`.
**DoD:** test voucher penuh, campuran voucher + uang, voucher habis, voucher tidak dipakai di ujian, Premium habis → voucher tidak terpakai.

## P8-003 — Boosts (rewarded) (M)

✅ **SELESAI.** Tambahan: lokasi pingsan juga dicatat bila pingsan karena lapar/kurang tidur (bukan hanya karena berjalan). Test: `heart` (tidak perlu saat nyawa 5, klaim terlalu cepat, klaim dua kali, batas 3×), `rescue` (kembali ke zona/posisi pingsan, lewat 10 menit ditolak), `double_pay` (belum selesai ditolak, ×2 sekali, Premium ditolak), pelanggan Titian tanpa iklan.
`POST /pare/boosts {kind: heart|rescue|double_pay, ref?}` → `{id, needs_ad}`; `POST /pare/boosts/{id}/claim`. Syarat & batas sesuai ADR-0018 §2 (3×/hari/jenis WIB, iklan ≥ 15 dtk, token 10 menit, `rescue` ≤ 10 menit setelah pingsan, `double_pay` sekali per kertas & tidak untuk Premium Pare). Pingsan di `tick` menyimpan zona & posisi.
**DoD:** test tiap jenis (berhasil, syarat gagal, batas harian, klaim terlalu cepat, token kedaluwarsa, klaim dua kali), Premium tanpa iklan, ledger `kind='boost'`.

## P8-004 — FE: seam iklan & layar Premium (M)

✅ **SELESAI kode.** `src/game/ads.ts` (`H5AdProvider` via `adBreak()` bila `NEXT_PUBLIC_ADSENSE_CLIENT`; `StubAdProvider` 15 dtk di dev; tanpa iklan di produksi tanpa klien), `src/game/boosts.ts` (mulai → iklan bila `needs_ad` → tunggu `min_seconds` → klaim), tombol ❤️ di HUD saat nyawa ≤ 1 dan di modal "nyawa habis", modal pingsan dengan 🚑 kembali (memindahkan pemain ke zona/posisi dari server), 💰 bayaran ×2 di hasil pelajaran, interstitial saat naik level/pindah zona (≥ 3 menit, tidak untuk `ad_free`), `PremiumModal` (QR dari `qris_payload` dengan paket `qrcode`, polling `GET /orders/{id}`, tombol simulasi bayar khusus dev), HUD 💰 + 🎟️ voucher ⭐.
`src/game/ads.ts` (`AdProvider`, `StubAdProvider`, `H5AdProvider` via `adBreak()`, env `NEXT_PUBLIC_ADSENSE_CLIENT`); tombol rewarded di modal nyawa ≤ 1, modal pingsan, hasil pelajaran; interstitial saat naik level/pindah zona (≥ 3 menit); layar Premium (harga, isi, QR dari `qris_payload`, polling `GET /orders/{id}`); HUD voucher. Semua keputusan dari `ad_free`/`needs_ad` server.
**DoD:** browser: pemain gratis melihat tombol rewarded → klaim → hadiah; Premium via stub webhook → iklan hilang, voucher tampil & terpakai saat makan.

## P8-005 — Gateway QRIS asli (L) — ⛔ menunggu pilihan provider
Implementasi `PaymentProvider` kedua (mis. Midtrans/Xendit/Duitku QRIS), verifikasi tanda tangan webhook, kedaluwarsa QR, pencocokan nominal. Berlaku untuk Titian dan Pare sekaligus.
**DoD:** webhook tanpa tanda tangan valid ditolak; uji sandbox provider end-to-end.
