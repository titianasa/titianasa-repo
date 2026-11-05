# Audit kesiapan produksi: Kampung Bahasa 3D dan permainan

Dibuat 2026-10-14 (Sonnet 5.5) atas permintaan pemilik produk: menyempurnakan peta, aset, kontrol, UI/UX, kesesuaian dengan semua misi dan bahasa, sinkronisasi dengan versi pixel art, dan saran fitur. Dasarnya adalah yang **benar-benar dijalankan dan dilihat**, bukan dugaan. Yang belum diuji ditulis sebagai "belum diuji".

Tiket pelaksanaan: [`../tickets/pare-11-produksi-3d.md`](../tickets/pare-11-produksi-3d.md).

## 1. Ringkasan

| Bidang | Keadaan |
|---|---|
| Dunia dan bangunan | Kampung Bahasa, kota, dan kota-kota luar negeri tampil; 8 bentuk gedung baru ada; interior camp jadi kamar. Masih ada ketidaksempurnaan skala dan tabrakan (§3). |
| Kontrol | Joystick analog, kamera ikut dari belakang, kamera tidak menembus dinding, sisi joystick bisa ditukar. Belum diuji di HP sungguhan. |
| Kemampuan game | Misi, jalur belajar, toko, chat, telepon dipakai bersama (kode `Game.tsx` yang sama). Langkah pertama misi terbukti lewat UI 3D; sisanya belum diuji otomatis. |
| Sinkronisasi pixel ↔ 3D | Satu akun, satu progres (sudah). **Pilihan tampilan di akun** dibuat hari ini. Pemain 3D belum terlihat bergaya 3D di `/play` (§4). |
| Produksi | `next build` lolos, `tsc` dan `eslint src` bersih, paket 3D ±270 KB terkompresi. Belum ada pengaman perangkat tanpa WebGL (dibuat hari ini), belum ada suara, telemetri, dan penyesuaian kualitas otomatis. |

**Keputusan pemilik 2026-10-14:** akun baru bawaan 3D, lempar koin Rp500, satu gaya (Kartun) saat peluncuran. Karena itu bagian "belum layak sebagai tampilan bawaan" di bawah kini berlaku hanya untuk pemain lama; tiket P11-001 sampai P11-003 dan P11-006 menjadi syarat sebelum akun baru dibuka ke 3D.

**Kesimpulan jujur:** layak diuji tertutup (beta berlabel) setelah tiket P11-001 sampai P11-003 selesai dan diuji di HP sungguhan. **Belum layak sebagai tampilan bawaan** untuk semua pemain; karena itu bawaan akun tetap pixel dan 3D dipilih pemain.

## 2. Yang sudah diverifikasi

- `tsc --noEmit` dan `eslint src` bersih. (`eslint` seluruh repo menemukan 74 galat, semuanya di `scripts/` dan `any` di skrip lama, bukan di `src/`.)
- `next build` (produksi) lolos: 13 halaman, `/start` statis. Paket yang memuat three.js ±952 KB mentah, ±271 KB gzip, hanya dimuat oleh `/start` (`/play` tidak bertambah berat).
- Kinerja (`renderer.info`, keramaian 8–12 orang, GPU Intel HD 4000): Kampung Bahasa Rendah **324 draw call / 185 rb segitiga** (batas 350 / 200 rb, tipis), Tinggi 570 / 359 rb, Kota Rendah 147 / 101 rb. FPS di HP sungguhan belum diukur.
- Aksi dua pemain: ajak, terima, tos, salaman, foto dua arah dengan pemain sungguhan (soket uji), tanpa galat konsol.
- Pilihan tampilan: memilih 3D lewat API lalu membuka `/play` membuka `/start`; menu AKU menampilkan tombol pindah; memilih "pixel art" menyimpan `engine = pixel` di server dan membuka `/play?px=1`.
- Misi `en-0-greet`, langkah 1 (bicara dengan Miss Kate): lolos lewat UI 3D (jalan ke posisi, petunjuk muncul, `E`, jendela dialog).

## 3. Temuan

Tingkat: **P0** harus sebelum pemain umum, **P1** sebelum beta luas, **P2** penyempurnaan. Status: ✅ selesai hari ini, 🔶 sebagian, ⬜ belum.

| # | Tingkat | Temuan (bukti) | Status | Tiket |
|---|---|---|---|---|
| F1 | P0 | Tidak ada pengaman bila perangkat tak punya WebGL atau konteks grafis hilang: layar kosong. | ✅ dialihkan ke `/play?px=1`; layar "Gambar 3D terhenti" dengan Muat ulang / pixel art | P11-001 |
| F2 | P0 | Malam hampir hitam di luar cahaya lampu (foto 02:58). | ✅ cahaya malam dinaikkan (hemi 0,35→0,7, bulan 0,45→1,0, eksposur 0,9→1,0). **Mohon dilihat pemilik**; angka ini menyimpang dari panduan gaya dengan sengaja | P11-004 |
| F3 | P1 | Badan tenggelam di bangunan: tabrakan hanya mengikuti ubin, sedangkan tangga, tiang, dan teras menjorok. | 🔶 jarak ekstra 0,45 m dari ubin bangunan; tabrakan sungguhan per bentuk belum | P11-004 |
| F4 | P1 | Kamera menghadap dinding saat keluar camp / gerbang / kereta. | ✅ kamera mengikuti dari belakang dan tidak menembus dinding. Orang pertama dan kamera di dalam kereta belum | P11-003 |
| F5 | P1 | HUD bertumpuk di 360×640: banner misi menutup tombol aksi kiri atas; petunjuk "Ketuk untuk…" menimpa tombol BELAJAR. | ✅ aksi di bawah banner, banner petunjuk naik dan menyingkir saat daftar dibuka (landscape belum) | P11-006 |
| F6 | P1 | Tombol sentuh 34 px (< 44 px yang dianjurkan); belum memakai area aman (notch); mode landscape HP belum diuji. | 🔶 tombol aksi kini 44 px; area aman dan landscape belum | P11-006 |
| F7 | P1 | Tidak ada suara sama sekali di dunia (hanya efek UI sintetis): tanpa langkah kaki, suasana, musik, tombol bisukan. Berlaku juga di pixel. | 🔶 3D punya suara dan tombol bisukan (belum didengar pemilik); pixel belum | P11-007 |
| F8 | P1 | Kualitas bawaan hanya ditentukan "layar sentuh = Rendah". Tidak menyesuaikan FPS, tidak ada telemetri FPS/perangkat. | 🔶 turun otomatis satu tingkat + laporan kinerja (menunggu deploy migrasi 0106) | P11-008 |
| F9 | P1 | `onPlayerTap` dan `onPan` tak ada di 3D: mengetuk pemain lain tidak membuka kartunya (profil, chat, blokir, lapor). `setGoalZone` (panah ke pintu keluar) hanya rintisan. | 🔶 ketuk pemain membuka kartu; panah pintu keluar belum | P11-010 |
| F10 | P1 | Pemain yang berpakaian 3D tampil di `/play` dengan gaya pixel lamanya (`toPixelLook` ada tapi belum dipasang). | ⬜ | P11-002 |
| F11 | P1 | Skrip uji e2e (`ui.ts`) rapuh: bergantung pada teks petunjuk; versi pixel pun gagal di langkah 2 misi. Tanpa uji otomatis, paritas misi tak terjaga. | ✅ `ui3d`, `parity3d`, `path3d` hijau (4 misi penuh, 13 zona, 5 bahasa); `data-testid` dan CI belum | P11-009 |
| F12 | P1 | Gerak di server hanya dibatasi laju (16 langkah/dtk), tidak jarak: klien bisa berpindah jauh sekaligus. Berlaku di pixel juga, lebih berbahaya saat gerak 3D bebas. | ⬜ | P11-012 |
| F18 | P1 | Draw call titik awal kampung bahasa di grafik Rendah menembus batas 350: Korea 369, Inggris 366 (diukur oleh `parity3d`). | ✅ `mergeDeep`: Inggris 241, Korea 278, Mandarin 255 | P11-004 |
| F13 | P2 | Atap bandara/souk/mal tampak terlalu besar dari dekat (skala genteng); menara kontrol dan souk belum difoto utuh; varian gedung (cn/jp/kr/gb/glass) sama bentuknya. | ⬜ | P11-004 |
| F14 | P2 | Efek hidup pixel (kupu-kupu, kunang-kunang, daun jatuh) tak ada di 3D; cuaca selain hujan hanya mengubah langit. | ⬜ | P11-004 |
| F15 | P2 | Animasi makan/minum setelah membeli (butuh callback `onPurchased`), uji beli Lemari lewat BuatQris sandbox. Lempar koin kini Rp500 (keputusan pemilik). | 🔶 | P11-005 |
| F16 | P2 | `/3d-concepts` (acuan beku) terbuka untuk umum dan terindeks. | ⬜ | P11-011 |
| F17 | P2 | Tablet, layar lipat, dan HP landscape belum diuji (bingkai Lemari dan tata letak HUD). | ⬜ | P11-006 |

## 4. Sinkronisasi dengan versi pixel art

**Sudah sama (satu sumber):** akun, progres, level, uang, misi, jalur belajar, chat, telepon, toko, premium, posisi pemain, zona dan peta (`WorldMap`), keramaian, kereta kelinci, dan iklan. Pemain di dua tampilan saling melihat dan bisa chat.

**Dibuat hari ini:** `pare_players.engine` (`pixel` | `3d`, migrasi `0105`), `PUT /pare/me/engine`, `GET /pare/me` memuat `engine`. Pemain yang memilih 3D lalu membuka `/play` (termasuk aplikasi terpasang) dialihkan ke `/start`; `?px=1` mencegah putaran tanpa akhir. Tombol pindah ada di menu 👤 AKU dan di jendela Bantuan. Perangkat tanpa WebGL tidak bisa memilih 3D.

**Belum sama:**
1. Pemain 3D di `/play`: gaya pixel lama, bukan hasil Lemari (F10).
2. Aksi dua pemain (salaman, tos, foto) hanya terlihat di 3D; `/play` mengabaikannya. Keputusan terbuka: pesan kecil atau diabaikan.
3. Hanya 3D yang memakai Lemari baru; pixel memakai pemilih avatar lamanya. Pakaian 3D tidak berubah bila pemain mengganti avatar pixel (dan sebaliknya) kecuali `toPixelLook` dipakai satu arah.

## 5. Audit UI/UX (apa yang dilihat, bukan pendapat)

Baik: bahasa antarmuka Indonesia konsisten; jendela game (misi, kamus, toko) dipakai ulang tanpa perubahan; tombol bantu berlabel; menu grafik menampilkan pilihan dan yang aktif.

Perlu diperbaiki:
- **Kepadatan HUD** (F5, F6): kiri atas memuat status, zona, lonceng, AKU, peta, zoom; lalu banner misi; lalu tombol aksi; bawah: BELAJAR/MISI/CHAT + joystick + A. Di 360 px tidak ada ruang kosong. Usulan: satu pita status, tombol aksi kontekstual satu baris, banner misi dapat dilipat.
- **Kesadaran kontrol**: tak ada petunjuk pertama kali untuk geser kamera, cubit zoom, joystick melewati tepi (lari), tombol grafik. Usulan: tur 3 langkah sekali.
- **Pengaturan tercecer**: grafik di ⚙, sisi joystick di ⚙, tampilan di AKU, notifikasi di Bantuan. Usulan: satu halaman "Pengaturan" (grafik, kontrol, suara, tampilan, notifikasi, akun).
- **Keterbacaan**: label nama 12 px, banner kecil di layar kecil; sediakan ukuran teks.
- **Kesalahan dan keadaan kosong**: pesan saat server tak terjangkau sudah ada; pesan saat grafik berhenti (baru); belum ada pesan "perangkat terlalu lemah, pakai Hemat".
- **Aksesibilitas**: tidak ada "kurangi gerakan"; tak ada penanda selain warna untuk NPC bertugas; tak ada getar (haptic).

## 6. Saran fitur (untuk standar aplikasi sejenis)

### Yang kurang dan sebaiknya ada sebelum peluncuran
1. **Suara**: langkah kaki per permukaan, suasana (burung, pasar, hujan, kereta), musik latar yang tenang, dan tombol bisukan; suara yang membantu belajar (sapaan warga dibacakan, sudah ada TTS di pelajaran).
2. **Ketuk untuk bergerak** (tap-to-move) dan **jalan otomatis** ke target misi (ikuti panah): standar game seluler dunia terbuka; menolong yang kesulitan memakai joystick.
3. **Kartu pemain saat diketuk** (profil, kirim pesan, ajak, blokir, lapor): standar permainan sosial dan wajib untuk keamanan (F9).
4. **Teman dan kehadiran**: daftar teman, siapa yang daring, "pergi ke teman" dan "ikuti".
5. **Pengaturan terpadu, tur pertama kali, dan layar "perangkat tidak didukung"**.
6. **Telemetri dan pelaporan galat** (FPS, tingkat grafik, perangkat, galat WebGL, jatuh/macet); tanpa ini kinerja di HP nyata tidak terlihat.
7. **Kualitas otomatis**: turunkan resolusi/efek bila FPS tertahan di bawah 30 dan beri tahu pemain; ingat pilihannya.
8. **Anti-curang gerak** di server (F12) dan batas laju aksi sosial (sebagian ada).

### Yang tidak perlu atau tunda
- **Tiga gaya karakter sekaligus saat peluncuran**: tiap gaya berarti uji tiap barang Lemari (45 barang × 3 gaya). Pertimbangkan meluncurkan dua dulu atau menandai Realis "segera".
- **Kamera orang kedua**: jarang dipakai, menambah uji dan beban kode; sembunyikan di pengaturan lanjut.
- **Tingkat "Tinggi" di HP**: disembunyikan pada layar sentuh sempit; cukup Hemat/Rendah/Sedang.
- **Kota-kota luar negeri dan kota 3D penuh pada rilis pertama**: poles Kampung Bahasa, camp, dan satu kota dulu; sisanya tetap bisa dimainkan lewat pixel sampai siap.
- **`/3d-concepts` publik** (F16): jadikan hanya untuk pengembangan.

### Yang menambah daya tarik (urut manfaat/biaya)
1. **Kamar camp yang bisa didekor** (kasur, rak, karpet, poster): pengeluaran uang game yang sehat dan identitas ala The Sims, memakai ruang yang baru dibuat.
2. **Papan misi harian dan tujuan di dunia** (panah dan cahaya ke warga bertugas), supaya alur belajar terasa sebagai bagian dunia.
3. **Ruang belajar bersuara** (LiveKit sudah ada) dengan suara berjarak di taman dan warung.
4. **Mode foto** (bingkai, stiker kampung, simpan/bagikan): sudah ada polaroid; murah dan viral untuk media sosial.
5. **Acara musiman** (17 Agustus, Imlek, Ramadan) dengan dekor dan pakaian terbatas di Lemari.
6. **Peliharaan dan kendaraan** (sepeda sudah ada; becak, motor listrik) sebagai barang toko.
7. **Liga/peringkat terlihat di dunia** (papan di alun-alun).

## 7. Rencana

Urutan yang disarankan, satu tiket per sesi, dengan pengujian di HP sungguhan oleh pemilik di akhir tiket P11-003, P11-006, dan P11-008:

1. **P11-001 Pengaman produksi** (selesai hari ini).
2. **P11-002 Pilihan tampilan dan sinkronisasi** (inti selesai; sisa: pemain 3D di pixel, aksi dua pemain di pixel).
3. **P11-003 Kontrol dan kamera** (inti selesai; sisa: ketuk untuk bergerak, orang pertama).
4. **P11-006 UI/UX produksi** (HUD, sentuhan 44 px, area aman, tur, pengaturan terpadu).
5. **P11-008 Kinerja, kualitas otomatis, telemetri**.
6. **P11-007 Suara**.
7. **P11-010 Sosial** (kartu pemain, teman, lapor/blokir).
8. **P11-004 / P11-005 Dunia dan karakter** (tabrakan, skala, varian, animasi).
9. **P11-009 Paritas misi dan bahasa** (uji otomatis stabil di 3D untuk lima bahasa).
10. **P11-012 Keamanan gerak**, lalu **P11-011 Rilis bertahap** (label beta, persentase pengguna, rollback).
