# QA visual dan kinerja Kampung Bahasa 3D

Cara memastikan hasil pembangunan tetap sama dengan konsep yang disetujui pemilik produk pada 2026-10-13.

## 1. Gambar acuan

`golden/` berisi tangkapan layar `/3d-concepts`, diambil dengan `bun scripts/qa/3d.ts --url /3d-concepts` pada 2026-10-13. Ukurannya 1100 × 650, kecuali yang bernama `phone-*` (390 × 844, HP).

| Berkas | Isi | Yang harus sama di `/start` |
|---|---|---|
| `01-overview` | gedung kursus, warung, halaman, kolam, sepeda, dari atas | kesan material (genteng, plester, batu alam, paving, rumput), terang pagi, bayangan lembut |
| `02-nadia` | pemain dekat Nadia, tombol aksi | wajah, kartu peserta, jilbab, tombol aksi kuning dengan `E` |
| `03-salaman` | salaman dengan balon kalimat | pose tangan, balon dua baris (Inggris + arti) |
| `04-foto` | foto bareng dan polaroid | pose selfie dan peace, kilat, polaroid |
| `05-fp-pecel` | orang pertama di warung memegang piring pecel | tangan di bawah layar, barang di tangan |
| `06-cam2` | kamera orang kedua | sudut dari mata lawan bicara |
| `07-ride` | naik sepeda | pose kayuh, sepeda ikut |
| `08-baca` | duduk di bangku membaca buku | pose duduk dan baca |
| `09-joget` | joget bersama keramaian | gerak joget, orang lain ikut |
| `10-lemari` … `13-kartun-batik` | Lemari: Kartun, Realis bergamis-jilbab, Blok berpeci-koko-sarung, Kartun berblangkon-batik-jarik | proporsi tiga gaya dan pakaian lokal |
| `14-konsep` | barisan tiga gaya | ciri khas di ketiga gaya |
| `15-senja`, `16-malam` | waktu | warna langit, lampu menyala, jendela berpendar |
| `phone-20` … `phone-22` | HP: Jelajah, Lemari, Konsep | tata letak HP |

## 2. Cara membandingkan

1. Jalankan:
   ```
   cd alr/game
   bun scripts/qa/3d.ts --url /start --out /tmp/kb3d-qa
   ```
   Butuh server dev di `:4700`. Supaya cepat, skrip menyesuaikan diri dengan perangkat:
   - **GPU:** Chrome dijalankan memakai GPU mesin lewat `scripts/qa/chrome-gpu.sh`. Bun menjalankan Chrome dengan `--disable-gpu`, sehingga tanpa ini WebGL jatuh ke CPU, sekitar 0,4 fps bahkan di Hemat. `--no-gpu` untuk tetap di CPU.
   - **Tingkat grafik adegan** (`--quality auto`): tingkat tertinggi yang masih ≥ 15 fps. Di mesin dev (Intel HD 4000) itu Hemat atau Rendah.
   - **Tingkat grafik gambar** (`--shot-quality`, bawaan Sedang): dinaikkan hanya saat mengambil gambar, dengan waktu game dihentikan. Gambar tetap sebanding dengan `golden/`.
   - Skrip menunggu menurut **waktu game**, bukan waktu nyata.

   Seluruh adegan selesai dalam beberapa menit.
2. Untuk setiap pasangan gambar, periksa dengan mata (baca keduanya dengan alat Read) dan tulis hasilnya di tiket: **sama**, **beda tapi disengaja (alasan)**, atau **rusak**.
3. **Tidak harus sama piksel demi piksel** (letak orang acak), tetapi lima hal ini wajib sama:
   1. Arah dan warna cahaya, serta kecerahan keseluruhan per waktu.
   2. Bentuk dan proporsi karakter tiap gaya, termasuk wajah dan kartu peserta.
   3. Material dan ukuran tekstur pada ukuran nyatanya (bata paving, genteng, plester).
   4. Gaya UI (garis tinta, kuning, huruf Fredoka/Nunito, balon dua baris).
   5. Kamera: jarak dan sudut awal tiap mode.
4. Untuk adegan yang belum ada di `/start` (misalnya Lemari sebelum P10-008), tulis "belum ada", jangan dilewati diam-diam.
5. **Bila tampilan berubah dengan sengaja:** perbarui gambar di `golden/` dan panduan gaya dalam tiket yang sama, dengan alasan.

## 3. Kinerja

```
bun scripts/qa/3d.ts --url /start --perf
```
Skrip mencetak `renderer.info` (draw call, segitiga, geometri) di keempat tingkat grafik, dengan 12 orang, di titik awal Kampung Bahasa.

| Ukuran | Batas | Acuan 2026-10-13 (halaman konsep) |
|---|---|---|
| Rendah: draw call | ≤ 350 | 329 |
| Rendah: segitiga | ≤ 200 rb | 156 rb |
| Tinggi: draw call | ≤ 1.000 | 967 |
| Tinggi: segitiga | ≤ 550 rb (dinaikkan dari 450 rb oleh pemilik 2026-10-14, setelah perombakan visual; Tinggi hanya di layar besar dan turun sendiri di bawah 26 fps) | 434 rb |
| Satu orang | ≤ 25 draw call | ± 20 |

**Peta Kampung Bahasa jauh lebih besar dari halaman konsep.** Untuk tetap di bawah batas:
- bagian yang diam digabung per material, per kawasan sekitar 40 × 40 m;
- kawasan di luar kabut tidak digambar;
- orang dan properti kecil di luar 40 m disembunyikan (Hemat: 16 m).

**Uji di perangkat sungguhan** sebelum tiket ditutup: minta pemilik produk membuka `/start` di HP biasa dan di PC, lalu catat FPS tiap tingkat grafik.

## 4. Daftar periksa per tiket

- [ ] `npx tsc --noEmit` dan `npx eslint src/game3d src/app/(game)/start` bersih
- [ ] QA visual §2 tercatat di tiket
- [ ] Kinerja §3 tercatat di tiket bila tiket menambah isi dunia atau karakter
- [ ] `/play` diuji ulang bila tiket menyentuh `src/components/game`, `src/game`, atau `src/lib` (arsitektur §7)
- [ ] `/3d-concepts` tidak berubah (`git diff --stat src/components/concepts3d src/app/(game)/3d-concepts` kosong)
- [ ] Panduan gaya dan gambar acuan diperbarui bila ada angka yang sengaja diubah
- [ ] `STATE.md` dan status tiket diperbarui
