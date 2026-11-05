# ADR-0023 — Kampung Bahasa 3D di `/start`

Status: **Accepted (2026-10-13)**. Keputusan pemilik produk: "fix saya akan bikin versi 3D-nya". Konsep yang menjadi acuan sudah jalan di `alr/game` pada `/3d-concepts`. Perencanaan dan peninjauan dikerjakan Opus; pembangunan tiket demi tiket dikerjakan Sonnet (effort medium) mengikuti [`kampung-3d/`](../kampung-3d/README.md) dan [`tickets/pare-10-kampung-3d.md`](../tickets/pare-10-kampung-3d.md).

## Konteks

- Kampung Bahasa Pare saat ini adalah game pixel art di `pare.titianasa.com/play` (`alr/game`, mesin kanvas 2D sendiri, peta di `src/game/world/`).
- Pemilik produk ingin versi 3D. Tiga uji di browser pada 2026-10-12 dan 2026-10-13:
  1. **Low-poly** dengan 50 pemain dan bayangan penuh: lancar di PC. Di HP biasa jalan bila bayangan dimatikan.
  2. **Gaya halus/kartun:** disetujui ("oke sih, bisa jalan").
  3. **Konsep lengkap di `/3d-concepts`:**
     - Tiga gaya karakter (Kartun Pare, Blok, Realis) di atas satu rangka.
     - Lemari kustomisasi dengan pakaian lokal.
     - Kamera orang ke-1, ke-2, dan ke-3.
     - Interaksi dengan pemain, barang, dan bangunan.
     - Dunia realistis bergaya The Sims.
- WebAssembly dan engine besar (Unity/Godot) sudah dibahas dan **tidak dipilih**. Penghambat 3D di HP adalah GPU, bukan CPU. Engine Wasm menambah unduhan puluhan MB dan memaksa UI teks (pelajaran, chat, misi, papan ketik bahasa) dibuat ulang di luar React.

## Keputusan

### 1. Tempat dan hidup berdampingan

1. **Game 3D tinggal di `/start`** (`alr/game`, route `src/app/(game)/start/`). **`/play` (pixel art) tidak dihapus dan tidak diubah perilakunya.** Keduanya dirawat sampai ada ADR baru yang memutuskan lain.
2. **Satu dunia, dua tampilan.** `/start` memakai backend, akun, data pemain, zona, ekonomi, pelajaran, misi, chat, suara, dan hub realtime (`/ws/pare`) yang sama dengan `/play`.
   - Pemain `/play` dan `/start` saling melihat di zona yang sama: pemain pixel tampil sebagai karakter 3D di `/start`, dan pemain 3D tampil sebagai sprite di `/play`.
   - Server tidak tahu dan tidak perlu tahu klien mana yang dipakai.
3. **UI tetap React** dan dipakai bersama sebanyak mungkin: jendela pelajaran, misi, chat, premium, profil, papan ketik bahasa (`src/components/game/*`). Yang baru di `/start` hanya kanvas 3D dan kontrolnya.
4. **`/3d-concepts` adalah implementasi acuan yang dibekukan.** Kodenya (`src/components/concepts3d/`) tidak diubah lagi kecuali untuk memperbaiki bug yang juga ada di `/start`. `/start` dibangun dari salinan modul-modulnya di `src/game3d/`.

### 2. Teknologi

1. **three.js `0.186.1` (r186), dikunci persis** di `package.json`, beserta `@types/three` `0.186.0`, `WebGLRenderer`, dan modul addon dari `three/addons/*`. Naik versi harus lewat tiket tersendiri dengan uji visual ulang.
2. **Tidak ada engine game, Wasm, atau pustaka 3D lain** (react-three-fiber, cannon, dan sejenisnya) tanpa ADR baru.
3. **Tidak ada file gambar atau model yang diunduh** untuk dunia dan karakter.
   - Semua tekstur dilukis di kanvas browser (`textures.ts`).
   - Semua bentuk dibuat dari geometri three.js.
   - Pengecualian, bila kelak diperlukan, harus lewat ADR. Alasannya: unduhan pertama `/start` tetap kecil, dan aset bertambah tanpa pipeline seni terpisah.
4. three.js hanya dimuat oleh `/start` dan `/3d-concepts` (dynamic import, `ssr: false`). Bundel `/play` tidak boleh ikut membesar.

### 3. Arah seni

1. **Karakter: tiga gaya pada satu rangka** yang dipilih pemain.
   - **Kartun Pare:** bawaan, kepala besar.
   - **Blok:** mirip Roblox.
   - **Realis:** proporsi mirip The Sims.
   - Satu pakaian dibuat sekali dan pas di ketiganya. Proporsi persisnya ada di [`kampung-3d/panduan-gaya.md`](../kampung-3d/panduan-gaya.md) §2 dan tidak boleh diubah tanpa memperbarui dokumen itu.
2. **Ciri khas karakter, berlaku di semua gaya:**
   - Kartu peserta kursus di leher: warna tali = level, kartu = bahasa.
   - Wajah yang sama: mata oval dengan titik kilau, alis tipis, pipi merona.
   - Kepala sedikit lebih besar dari aslinya.
   - Tangan bulat tanpa jari.
   - Gerakan khas Indonesia: salam tangan di dada, salaman, hormat bendera, angkat tangan, joget.
3. **Dunia: realistis gaya The Sims.**
   - Ukuran nyata dalam meter.
   - Material PBR (`MeshStandardMaterial`), dengan tekstur pada ukuran nyatanya (genteng, paving, plester, batu alam, kayu).
   - Langit fisik (`Sky`) yang juga menjadi environment map.
   - Tone mapping ACES dengan eksposur per waktu (lihat panduan §4).
   - **Tidak low-poly** dan tidak flat-shading.
4. **Detail khas Indonesia/Pare adalah wajib, bukan hiasan:**
   - Genteng tanah liat, teralis jendela, unit AC di dinding, sandal di depan pintu.
   - Warung dengan atap seng, terpal belang, dan etalase.
   - Sepeda onthel berkeranjang, tiang listrik dengan kabelnya.
   - Pohon kelapa dan pisang, bendera merah putih.

### 4. Skala dan peta

1. **1 ubin peta pixel = 2 meter.** Peta pixel (`WorldMap`: `ground`, `feature`, `buildings`, `objects`, `npcs`, `places`, `warps`) adalah **denah** dunia 3D.
   - Peta 3D dibangkitkan dari data peta yang sama, jadi setiap perubahan peta pixel ikut ke 3D.
   - Bangunan 3D berdiri di petak bangunannya dengan ukuran nyata dan menghadap ke arah pintunya. Bentuknya tidak harus mengisi seluruh petak.
2. **Posisi ke server tetap dalam satuan ubin**, dibulatkan seperti yang diharapkan hub sekarang.
   - Gerak 3D yang mulus dikirim sebagai ubin terdekat.
   - Pemain lain digambar dengan interpolasi di antara laporan.
3. **Titik interaksi tetap `MapObject`.** Semua yang bisa dipakai di pixel (warung, kasur Camp, perpustakaan, halte, gerbang, bus/kereta/pesawat, warga) bisa dipakai di 3D dengan aturan server yang sama. 3D menambah interaksi tampilan (duduk, salaman, foto), bukan aturan ekonomi baru.

### 5. Kustomisasi dan monetisasi

1. **Slot:**
   - Tubuh: gaya, kulit, tinggi, badan, bahu.
   - Mata dan rambut beserta warnanya.
   - Penutup kepala, atasan, terusan, bawahan, alas kaki, tas, aksesori.
2. **Empat cara mendapat barang:**
   - **Gratis.**
   - **Uang game:** hasil belajar. Sesuai aturan produk, penghasilan di Pare hanya dari tugas bahasa sungguhan, jadi uang game tetap hanya dari belajar.
   - **Plus/Pro:** ikut langganan.
   - **Toko:** beli satuan dengan uang sungguhan lewat gateway pembayaran yang sudah ada.
   - Semua barang **bisa dicoba gratis**; yang dibayar hanya yang disimpan.
3. **Koleksi lokal adalah jualan utama:** jilbab, pashmina, jilbab instan, peci, blangkon, caping, baju koko, batik, kebaya, gamis, daster, sarung, kain jarik, sandal jepit. Edisi musiman (Ramadan, 17 Agustus, Hari Batik) menyusul sebagai barang toko.
4. **Harga adalah data**, bukan kode: katalog dan harganya dipindah ke data konten backend (seperti `menus` dan `prices` di `content.json`). Angka di konsep hanyalah contoh.
5. **Tampilan tersimpan di server.**
   - Kolom baru `pare_players.look3d` (JSON) dan tabel kepemilikan barang (`pare_wardrobe`).
   - Pemain lama yang belum punya `look3d` mendapat tampilan yang diturunkan dari `look` pixel-nya.
   - Pemain 3D tampil di `/play` lewat pemetaan balik ke `look` pixel terdekat.

### 6. Kamera dan kontrol

- **Orang ke-1:** kedua tangan terlihat di bawah layar seperti Minecraft, ikut berayun saat berjalan, memegang barang, dan lengan bajunya mengikuti pakaian.
- **Orang ke-2:** pemain melihat dirinya dari mata orang yang diajak bicara (atau warga terdekat).
- **Orang ke-3:** kamera orbit di belakang pemain.
- **Mode Lemari:** kamera di depan pemain seperti meja putar.
- **Zoom** di semua mode.
- **Kontrol:** joystick layar sentuh, WASD/panah, Shift lari, Spasi lompat, E untuk aksi utama, seret untuk memutar kamera, cubit/gulir untuk zoom.

### 7. Interaksi

1. **Dengan warga (NPC berlabel) dan pemain komputer seperti Nadia:** sapa, ngobrol, salaman, tos, foto bareng.
   - Balasan mereka dalam bahasa yang sedang dipelajari pemain, dengan arti bahasa Indonesia di bawahnya.
2. **Dengan pemain sungguhan:** aksi berdua (ngobrol, salaman, tos, foto bareng) dikirim sebagai **ajakan** yang harus diterima pemain lain. Emote sendirian tidak perlu persetujuan.
3. **Kerumunan dummy (server, `@dummy.pare.invalid`) tidak pernah menjawab, menyapa balik, mengirim pesan, atau membalas gerakan**, sama seperti di `/play`. Di `/start` mereka tidak menampilkan tombol interaksi sosial. Ini menggantikan perilaku `/3d-concepts`, yang membuat orang di keramaian membalas karena belum ada server.
4. **Dengan barang:** ambil dan baca buku, makan, minum, naik sepeda, lempar koin ke kolam.
   **Dengan bangunan:** buka pintu, masuk, duduk di bangku, beli di warung, hormat bendera.
   - Aksi yang punya akibat ekonomi (beli, sewa, tiket) **selalu lewat endpoint server yang sudah ada**.
5. **Emote:** delapan bawaan gratis (lambai, salam, angkat tangan, mikir, tepuk tangan, hormat, joget, peace). Emote tambahan bisa menjadi barang toko.

### 8. Grafik dan anggaran kinerja

1. **Empat tingkat grafik: Hemat, Rendah, Sedang (bawaan), Tinggi.** Isinya persis seperti panduan §5. Pilihan disimpan di perangkat.
2. **Anggaran wajib** (diukur dengan `renderer.info` pada 12 orang di halaman Kampung Bahasa):
   - **Rendah:** ≤ 350 draw call, ≤ 200 ribu segitiga.
   - **Tinggi:** ≤ 1.000 draw call, ≤ 450 ribu segitiga.
   - **Satu orang:** ≤ 25 draw call.
   - Diukur di konsep pada 2026-10-13 (`scripts/qa/3d.ts --perf`): Rendah 329 draw call / 156 ribu segitiga, Tinggi 967 / 434 ribu.
3. **Bagian yang diam digabung per material (`merge.ts`).** Tiap bagian yang bergerak sendiri adalah `Group` sendiri.

### 9. Proses kerja

1. **Opus merencanakan dan meninjau; Sonnet (effort medium) membangun** satu tiket per sesi.
2. **Hasil harus sama dengan konsep.** Setiap tiket yang mengubah tampilan:
   - menjalankan `game/scripts/qa/3d.ts`,
   - membandingkan tangkapan layarnya dengan gambar acuan di `kampung-3d/golden/`,
   - dan mencatat hasilnya di tiket.
3. **Angka di panduan gaya adalah kontrak.** Mengubahnya (warna, proporsi, cahaya, kecepatan) berarti memperbarui panduan dan gambar acuan dalam tiket yang sama, dengan alasan tertulis.

## Konsekuensi

- **Dua klien dirawat bersamaan.** Fitur gameplay baru masuk ke server, lalu ditampilkan di kedua klien. Tiket fitur harus menyebut kedua tampilan, atau menyebut bahwa `/start` menyusul.
- **Kerumunan, NPC, dan warga harus dibangkitkan dari data yang sama** dengan `/play` (`map.ts`, `kota.ts`, dan data warga), bukan diketik ulang di 3D.
- **Pemain dengan HP lemah** memakai Hemat. `/play` tetap ada untuk perangkat yang tidak punya WebGL2.
- **Skala 1 ubin = 2 m membuat peta besar** (Kampung Bahasa ≈ 222 × 152 m). Sepeda, kereta kelinci, dan lari menjadi penting; kecepatan jalan ada di panduan §6.

## Keputusan yang masih terbuka

1. **Peta mana yang menyusul setelah Kampung Bahasa:** lima kampung, Camp, kota, negara tujuan. Urutannya diputuskan setelah Kampung Bahasa 3D lulus uji (tiket P10-010).
2. **Kapan `/start` menjadi pintu utama** dan landing page mengarah ke sana. Butuh ADR terpisah.
3. **Interior bangunan** (kelas, warung, kamar Camp) sebagai ruang 3D sendiri atau jendela UI seperti sekarang. Usulan: jendela UI dulu, interior menyusul.
4. **Harga sungguhan katalog toko dan edisi musiman.**
