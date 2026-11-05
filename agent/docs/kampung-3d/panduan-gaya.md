# Panduan gaya Kampung Bahasa 3D

Kontrak visual dan rasa main untuk `/start` ([ADR-0023](../adr/0023-kampung-bahasa-3d.md)).

- **Sumber angka:** implementasi acuan di `alr/game/src/components/concepts3d/` (halaman `/3d-concepts`). Setiap angka di sini ada di kode itu.
- **Bila keduanya berbeda:** kode acuan yang benar, dan dokumen ini diperbaiki.
- **Mengubah angka:** perbarui dokumen ini dan gambar acuan (`golden/`) dalam tiket yang sama, dengan alasan tertulis.

Satuan: meter, detik, radian. Kecuali disebut lain, karakter menghadap **+z**, atas adalah **+y**, dan sisi kanan karakter ada di **−x**.

## 1. Arah besar

| | Karakter | Dunia |
|---|---|---|
| Rasa | ramah, ekspresif, mainan yang halus | realistis seperti The Sims: bersih, terang, ukuran nyata |
| Bentuk | bulat dan halus, tanpa sudut tajam | proporsi bangunan nyata, tepi dibulatkan hanya pada perabot kecil |
| Shading | halus (`MeshStandardMaterial`, tanpa `flatShading`) | sama, ditambah bump map dari tekstur yang sama |
| Tekstur | warna polos; motif hanya pada kain bermotif | tekstur lukisan kanvas pada ukuran nyatanya (§3) |
| Larangan | low-poly bersudut, wajah tanpa kilau mata, jari terpisah | low-poly, warna polos tanpa tekstur pada dinding, lantai, atap, jalan, rumput |

## 2. Karakter

### 2.1 Tiga gaya pada satu rangka (`avatar.ts`, `SPECS`)

Semua angka dalam meter sebelum `look.height`, yang menskalakan seluruh tubuh, 0,9–1,1.

| Ukuran | Kartun Pare | Blok | Realis |
|---|---|---|---|
| Tinggi pinggul `hipY` | 0,64 | 0,72 | 0,88 |
| Paha / betis | 0,27 / 0,28 | 0,33 / 0,30 | 0,42 / 0,41 |
| Jari-jari paha / betis | 0,092 / 0,080 | 0,105 / 0,100 (balok) | 0,074 / 0,056 |
| Pusat torso / jari-jari (x, y, z) | 0,93 / 0,225 · 0,29 · 0,17 | 1,02 / 0,25 · 0,27 · 0,135 | 1,15 / 0,175 · 0,27 · 0,115 |
| Bahu y / jarak x | 1,10 / 0,262 | 1,22 / 0,335 | 1,40 / 0,19 |
| Lengan atas / bawah | 0,21 / 0,24 | 0,28 / 0,27 | 0,28 / 0,26 |
| Kepala y / jari-jari | 1,45 / 0,26 bulat | 1,45 / 0,175 · 0,165 kaleng | 1,58 / 0,093 · 0,118 · 0,106 lonjong |
| Bentuk torso | telur | kotak membulat | profil tubuh (pinggul, pinggang, dada, bahu) |
| Bentuk tungkai | kapsul meruncing | balok membulat | kapsul meruncing |
| Skala mata `eye` | 1 | 0,8 | 0,62 |
| Tinggi total ± | 1,71 | 1,62 | 1,69 |

**Tubuh:**
- `build` (0,85–1,2) mengalikan lebar dan tebal torso, panggul, dan paha.
- `shoulders` (0,85–1,2) mengalikan jarak bahu.
- Rangka: `body`, kemudian `hip[2]` ke `knee[2]`, `sh[2]` ke `el[2]` ke `hand[2]`, `head` ke `unit`. Indeks 0 = kanan (−x), 1 = kiri.

### 2.2 Wajah: sama di tiga gaya

Wajah digambar dalam satuan kepala (bola jari-jari 1, menghadap +z).

- **Mata:** di (±0,36, 0,04).
  - `bulat`: putih mata 0,17 × 0,21, pupil 0,11 × 0,14, titik kilau putih 0,035.
  - `senyum`: busur torus (mata tertutup tersenyum).
  - `tajam`: tinggi mata 72% dengan garis kelopak.
  - Gaya **Blok** tanpa putih mata (oval hitam saja), tetapi **tetap dengan titik kilau**.
- **Alis:** di y +0,27, miring 0,12. Warnanya sama dengan rambut, atau cokelat tua bila rambut tertutup.
- **Pipi merona:** `#f29b9b`, opasitas 0,75, di (±0,56, −0,22). Realis tanpa pipi merona.
- **Mulut:**
  - Kartun dan Blok: busur senyum `#8a3a2e`.
  - Realis: hidung dan bibir `#c06a6a`.
- **Telinga:** Kartun dan Realis; Blok tanpa telinga.

### 2.3 Ciri khas yang wajib ada pada setiap karakter

1. **Kartu peserta di leher (aksesori `lanyard`).** Tali berwarna level dan kartu putih bertuliskan PESERTA, nama, dan `BAHASA · LEVEL` (`idCard()`). Warna level:

   | Basic | A1 | A2 | B1 | B2 | C1 | C2 |
   |---|---|---|---|---|---|---|
   | `#58c46a` | `#3b82c4` | `#2f8f83` | `#9b6bd1` | `#e5534b` | `#f39c3d` | `#d4af37` |

   Konsep masih memakai A1 untuk semua orang; `/start` memakai level bahasa fokus pemain. Bahasa: `EN`, `ZH`, `AR`, `JA`, `KO`.
2. Wajah §2.2.
3. **Kepala lebih besar dari aslinya**, kira-kira kepala : tinggi = 1 : 3 (Kartun), 1 : 4,5 (Blok), 1 : 7 (Realis).
4. **Tangan bulat tanpa jari**, ditambah satu ibu jari bulat untuk Kartun dan Realis.
5. **Gerakan khas** (§2.6).

### 2.4 Pakaian: satu barang pas di tiga gaya

Aturan menutup tubuh:
- **Atasan** mewarnai torso dan lengan atas. Bila `longSleeves`, lengan bawah juga; bila tidak, lengan bawah berwarna kulit.
- **Bawahan** mewarnai panggul, paha, dan betis. `pendek`: betis berwarna kulit.
- **Rok, sarung, jarik, gamis, daster:**
  - Digambar sebagai rok lathe dari pinggang sampai pergelangan kaki (daster sampai tengah betis).
  - Kaki di dalamnya berwarna kulit, kecuali gamis dan rok yang memakai legging `#2b2b33`.
  - Saat duduk, rok miring mengikuti paha (×0,55).
- **Terusan** menggantikan atasan dan bawahan.
- **Penutup kepala `coversHair`** (jilbab, pashmina, jilbab instan, blangkon) menyembunyikan rambut.
- **Jilbab:** bola kain 1,16 digeser ke belakang, bingkai wajah torus, kain jatuh menutup bahu dan dada.
  - Jilbab segi empat menambah ujung lancip di dada.
  - Pashmina menambah juntai di dada.
  - Jilbab instan menambah pet di dahi.

Detail atasan:

| Atasan | Detail |
|---|---|
| kemeja | dua kerah, empat kancing |
| batik kawung | motif kawung dari warna kain, kerah cokelat tua |
| baju koko | kerah bulat putih, list tengah emas `#d4af37` |
| kebaya | motif renda, bros tiga butir emas |
| hoodie | tudung di tengkuk, saku depan, dua tali |
| jaket almamater | kemeja putih di dalam, kerah jas lebih gelap, badge kuning |

Alas kaki:
- **Sneakers:** sol putih.
- **Sepatu lari:** garis samping putih.
- **Pantofel:** mengilap (roughness 0,22) dengan hak.
- **Sandal jepit:** telapak kaki terlihat, sol tipis, tali V.

Tas:
- **Ransel:** di punggung, dengan tali di dada.
- **Selempang:** tali diagonal, tas kecil di pinggang kanan.
- **Tote:** tergantung dari bahu kanan, bertulisan PARE.

Aksesori:
- **Kacamata:** bingkai hitam.
- **Jam tangan:** di pergelangan kiri.
- **Headphone:** bando dengan dua mangkuk merah.

Material karakter:

| Bagian | Nilai |
|---|---|
| Kulit | roughness 0,55. Pilihan: `#f6d6b6` `#ecbd90` `#dcaa7c` `#c68e5e` `#a8714a` `#7c5034` |
| Rambut | roughness 0,5. Pilihan: `#1a1a1a` `#2b1d14` `#4a2f1c` `#7a4a2a` `#a0522d` `#8a8a8a` |
| Kain | roughness 0,82; jeans 0,95 |
| Warna kain | `#e5534b` `#f6c945` `#3b82c4` `#58c46a` `#2f4a7a` `#f4f4f4` `#262626` `#9b6bd1` `#ff8fab` `#2f8f83` `#b5651d` `#d9c7a7` |
| Mata | putih roughness 0,3; gelap `#20150f` 0,35; iris Realis `#4a2c1a` |

### 2.5 Kerumunan

Penampilan acak (`randomLook`):
- Sekitar 55% perempuan; 65% di antaranya berjilbab (segi empat, instan, atau pashmina).
- Sebagian kecil memakai gamis atau daster.
- Laki-laki kadang memakai peci atau topi.
- Gaya campuran: Kartun 40%, Blok 20%, Realis 40%.
- **Semua memakai kartu peserta.**

### 2.6 Gerak dan pose (`poseFor`, `applyPose`)

**Konvensi sudut:**
- Bahu x negatif mengangkat lengan ke depan; bahu z negatif mengangkat lengan kanan (−x) ke samping, z positif untuk lengan kiri.
- Siku x negatif menekuk ke depan.
- Pinggul x negatif mengayun paha ke depan; lutut x positif menekuk ke belakang.

**Gerak dasar:**
- **Penghalusan:** setiap sendi bergerak ke target dengan `1 − e^(−dt·10)` (barisan Konsep 8). Inilah yang membuat gerak terasa mulus. **Jangan menyetel sudut langsung tanpa penghalusan.**
- **Jalan:** ayunan pinggul ±0,55, lutut sampai 0,9, lengan berlawanan ±0,45, badan memantul `|cos|·0,03`, condong 0,05.
- **Langkah:** 1,15 m × tinggi; Realis × 1,25.
- **Duduk:** pinggul −1,52, lutut 1,5, panggul di 0,47 m.
- **Naik sepeda:** sadel 0,86 m, kayuh ±0,4, condong 0,22, tangan ke setang.
- **Diam:** napas 1,8 Hz, kepala menoleh pelan.

**Aksi** (nama kode → arti):
- **Emote:** `lambai`, `salam` (tangan di dada sambil mengangguk), `tanya` (angkat tangan), `mikir`, `tepuk`, `hormat`, `joget`, `peace`.
- **Lainnya:** `selfie`, `salaman` (tangan memompa), `tos`, `talk` (gerak tangan saat bicara), `toss` (lempar), `hold` (memegang barang), `read`, `eat`, `drink`.

**Lama aksi:**
- Emote 2,4–3 detik; joget sampai pemain bergerak.
- Salaman 2,4; tos 1,5; foto 3,2; makan dan minum 7.

**Lompat:** kecepatan awal 4,2 m/s, gravitasi 13 m/s². Di udara lutut 0,7 dan lengan terbuka.

### 2.7 Tangan orang pertama (`buildHands`, `animateHands`)

- Dua lengan tergantung dari kamera:
  - Lengan bawah silinder 0,46 m.
  - Ujung lengan baju bila atasan berlengan pendek.
  - Telapak bulat berwarna kulit.
  - Jam tangan bila dipakai.
- **Posisi diam:** (±0,27, −0,33, −0,42), condong 0,25.
- **Ayunan jalan:** ±0,018 bergantian.
- **Penghalusan:** `1 − e^(−dt·12)`.
- Setiap aksi punya pose tangan sendiri. Contoh: `read` dua tangan memegang buku di tengah; `ride` kedua tangan di setang; `lambai` tangan kanan naik dan berayun.
- Barang yang dipegang digambar ulang di tangan kanan kamera.
- `renderOrder` 10 dan `frustumCulled = false`.

## 3. Dunia: permukaan

Tekstur dilukis di kanvas (`textures.ts`), berulang tanpa sambungan, dan dipetakan per meter: `boxUV` untuk balok, `faceUV` untuk atap miring. Kolom "m/ubin" = berapa meter satu ulangan tekstur.

| Permukaan | Tekstur | m/ubin | Material |
|---|---|---|---|
| Rumput | `grass()` | 2 | roughness 1, bump 0,8 |
| Paving halaman | `paving()` blok 20 × 10 cm, running bond | 1,6 | 0,95, bump 2 |
| Lantai teras | `ceramic()` 40 × 40 cm | 1,6 | 0,25, bump 0,2 |
| Dinding | `plaster("#f3e6c9")` | 2 | 0,95, bump 0,4 |
| Kusen, kolom, list | `plaster("#f7f5ef")` | 2 | 0,8, bump 0,3 |
| Batu alam (plint, dinding bawah) | `stone()` | 1,2 | 0,95, bump 2,5 |
| Atap | `roofTiles()` genteng | 1,6 | 0,75, bump 3, dua sisi |
| Bubungan | warna `#9a3f22` | — | 0,7 |
| Pintu | `wood("#7a4527")` | 1 | 0,55, bump 1,2 |
| Bangku | `wood("#9a6a3c")` | 1 | 0,7 |
| Dinding warung | `planks("#a77b4f")` | 1,6 | 0,9, bump 1,5 |
| Atap seng | `zinc()` | 1 | metalness 0,55, roughness 0,45 |
| Aspal | `asphalt()` | 3 | 0,95, bump 1,5 |
| Kaca jendela | `#20384a` | — | roughness 0,06, metalness 0,25; emissive `#ffc46b` |
| Air kolam | `#2b6a7d` | — | roughness 0,04, opasitas 0,88 |
| Teralis | `grill()` alpha | per jendela | alphaTest 0,5 |
| Pohon | gumpalan daun ikosahedron detail 3, digoyang derau, warna per titik hijau | — | roughness 0,85 |
| Kelapa / pisang | pelepah bidang melengkung dengan `frond()` / `bananaLeaf()` | — | alphaTest 0,45, dua sisi |
| Rumput tinggi | `tuft()` silang dua bidang, instanced 1.400 | — | hanya Sedang dan Tinggi |

**Detail Indonesia/Pare yang harus ada di setiap kawasan permukiman:**
- Genteng dan teralis.
- Plint batu alam.
- Unit AC di dinding samping.
- Sandal di depan pintu.
- Pot tanaman.
- Pagar tembok rendah dengan jeruji besi.
- Tiang listrik beton dengan tiga kabel melengkung.
- Rumah warna pastel (`#cfe8d6` `#f4d9c2` `#f6ecb5` `#dfe3ef` `#f2d0d0` `#e6dcc8`) dengan teras keramik.
- Sepeda onthel berkeranjang.
- Warung dengan atap seng, terpal belang merah putih, papan menu, dan etalase.

## 4. Cahaya dan langit (`world.ts`, `setTime`)

Renderer:
- `ACESFilmicToneMapping`.
- Bayangan `PCFShadowMap` dengan `radius` 3, bias −0,0004, normalBias 0,03.
- Kotak bayangan ±22 m yang mengikuti pemain dan dibulatkan ke meter penuh (supaya bayangan tidak bergetar).

| | Pagi | Senja | Malam |
|---|---|---|---|
| Elevasi / azimut matahari | 38° / 130° | 3,5° / 245° | bulan 50° / 200° |
| Sky: turbidity, rayleigh | 2,5, 1,2 | 6, 2,6 | 2,5, 0,6 |
| Sky: mie, mieG | 0,004, 0,8 | 0,008, 0,93 | 0,004, 0,8 |
| Awan (cloudCoverage) | 0,3 | 0,3 | 0,2 (langit diganti `#0b1020`) |
| Matahari: warna / intensitas | `#fff3df` / 3,8 | `#ffa25c` / 2,6 | `#a9bfff` / 0,45 |
| Hemisfer: langit / tanah / intensitas | `#cfe3ff` / `#6d7f4a` / 0,55 | `#ffc9a8` / `#5a4a4a` / 0,5 | `#3a4a7a` / `#1a1a26` / 0,35 |
| `environmentIntensity` (env dari Sky lewat PMREM) | 0,75 | 0,6 | 0,25 |
| Eksposur | 0,46 | 0,55 | 0,9 |
| Kabut (konsep: 70–330 m; di game: 0,37–1,27 × jarak gambar, lihat §5) | `#c4d8e8` | `#e3a77d` | `#141a2c` |
| Kaca jendela dan lampu (emissive) | 0 | 0,8 | 1,4 |
| Lampu taman (PointLight, jarak 16, decay 2) | mati | 14 | 22 |

**Waktu di `/start`:** mengikuti jam WIB game, yaitu waktu yang sama dengan `/play` (`src/game/time.ts`), ditambah selisih jam server. `atmosphere.setClock` memadukan kunci: 04:30 malam, 05:30 fajar (Senja, matahari 4° di timur), 07:30 Pagi, 12:00 siang (Pagi, matahari 70°), 16:00 sore (Pagi, 38° di barat), 17:15 Senja, 18:30 malam. Cuaca `cloudy`/`fog`/`drizzle`/`rain`/`storm` menurunkan matahari dan memucatkan langit (0,3 / 0,4 / 0,5 / 0,8 / 1); hujan menambah garis hujan di sekitar kamera.

## 5. Tingkat grafik

| | Hemat | Rendah | Sedang (bawaan) | Tinggi |
|---|---|---|---|---|
| Pixel ratio | min(dpr, 0,7) | min(dpr, 1) | min(dpr, 1,5) | min(dpr, 2) |
| Bayangan matahari | — | — | 2048 | 4096 |
| Bayangan bulat di bawah orang | ya | ya | — | — |
| Rumput tinggi | — | — | ya | ya |
| Langit | warna polos | Sky tanpa awan | Sky + awan | Sky + awan |
| Pantulan lingkungan | — (hemisfer ×2,2) | ya | ya | ya |
| Orang jauh (> 16 m) | tidak digambar dan tidak dianimasikan | digambar | digambar | digambar |

Pilihan disimpan di perangkat (`localStorage` `kb3d-grafik`).

**Tambahan di game (`/start`):**

| | Hemat | Rendah | Sedang | Tinggi |
|---|---|---|---|---|
| Jarak gambar zona | 80 m | 105 m | 150 m | 150 m |
| Kabut (dekat–jauh) | 30–100 m | 39–133 m | 55–190 m | 55–190 m |
| Daun pohon | kasar, 60% pohon | kasar, 60% pohon | halus, semua | halus, semua |
| Orang dibuat dalam / dibuang di atas | 16 / 22 m | 40 / 52 m | 42 / 56 m | 46 / 60 m |

Peta dipotong menjadi kepingan 30 × 30 ubin (60 m), satu draw call per material tiap kepingan.

**Tingkat awal di `/start`:**
- **Sedang** bila perangkat bukan HP.
- **Rendah** di HP.
- **Hemat** bila 10 detik pertama rata-rata di bawah 24 fps. Pemain diberi tahu lewat toast, dan pilihannya tetap bisa diubah.

## 6. Gerak pemain dan kamera

**Gerak:**

| | Nilai |
|---|---|
| Jalan / lari (Shift) / sepeda | 2,5 / 4,4 / 5,6 m/s |
| Percepatan | `lerp` 9 (sepeda 3) |
| Belok | 12 (sepeda 4) |
| Jari-jari tabrakan | 0,28 m (sepeda 0,5) |
| Kecepatan warga | 1,05–1,45 m/s; diam 1–5 detik; 30% beraksi saat diam |

**Kamera:**

| Kamera | Nilai |
|---|---|
| Orang ke-3 | jarak 5,2 (1,6–26); pitch 0,32 (−0,05–1,35); titik pandang 1,15 × tinggi (sepeda ×1,2); fov 52 mendatar, 62 tegak; ikut `lerp` 12 (titik) dan 10 (posisi); seret 0,008 rad/px mendatar, 0,005 tegak |
| Orang ke-1 | mata = kepala + 0,1 × tinggi ke depan; fov 72 (25–95); menengadah dan menunduk ±1,1; tubuh pemain disembunyikan, tangan §2.7 tampil |
| Orang ke-2 | dari kepala lawan bicara (atau warga terdekat dalam 9 m, kalau tidak ada Nadia/warga terdekat) ke kepala pemain −0,15 × tinggi; fov 50 (12–80); orang yang matanya dipinjam disembunyikan |
| Lemari | kamera diam di depan pemain; jarak 2,6 × tinggi (1,1–5); titik 0,95 × tinggi; fov 40; seret memutar pemain. **Layar lebar (> 900 px):** kamera dan titiknya digeser ke kanan 0,42 × jarak, sehingga pemain tampil di kiri panel. **Layar tegak:** jarak × 3, titik 0,05 × tinggi, kamera 1,0 × tinggi, sehingga seluruh tubuh tampil di atas panel bawah. Orang lain dalam 4,5 m tidak digambar selama di Lemari |
| Konsep (barisan tiga gaya) | titik (0, 0,95, barisan); jarak 5,6; kamera 1,25 m; fov 40. Layar lebar: titik x +1,35. Layar tegak: jarak × 2,1, titik y −0,25, kamera 1,6 m |
| Zoom | tombol ×1,2 / ×0,83, gulir ±8%, cubit |

## 7. Antarmuka (`studio.module.css`)

**Gaya stiker** (bahasa desain Titian): garis tinta 3 px, sudut 14 px, bayangan keras 4 px 4 px tinta, latar kertas, kuning untuk yang terpilih dan aksi utama.

**Token:**

| Token | Nilai |
|---|---|
| ink | `#1d2a1f` |
| paper | `#fffaf0` |
| paper-2 | `#f3ead6` |
| sun | `#f6c945` |
| leaf | `#3f9b57` |
| coral | `#e5534b` |
| sky | `#3b82c4` |
| muted | `#5d6b5f` |
| Huruf tampilan | Fredoka 500/600 |
| Huruf isi | Nunito 600–800 |
| Tombol | minimal 44 px |

**Aturan:**
- **Tombol aksi kontekstual** di kanan bawah. Aksi pertama berwarna kuning dengan tanda `E`; tombol Emote selalu ada (menu 4 × 2).
- **Joystick** di kiri bawah: 126 px (HP 112 px), tuas kuning.
- **Balon percakapan:** kalimat dalam bahasa yang dipelajari (tebal), artinya dalam bahasa Indonesia di bawahnya (abu-abu). **Selalu dua baris** karena ini game belajar.
- **Panel samping** di desktop; **panel bawah** di HP (≤ 640 px, tinggi maksimal 46%).
- Ukuran barang di Lemari dinyatakan dengan **label harga** berwarna:

  | Label | Latar | Teks |
  |---|---|---|
  | gratis | `#dff1e3` | `#24633a` |
  | uang game | `#fdf0c2` | `#7a5a00` |
  | Plus | `#dbeafb` | `#1f4f86` |
  | Pro | `#ece2fb` | `#5a2f99` |
  | toko | `#fde2df` | `#9a2a22` |

  Barang lokal diberi label merah `LOKAL`.
- `prefers-reduced-motion`: tanpa animasi muncul.

## 8. Bangunan di game (P10-005, `game3d/start/buildings.ts`)

- **Denah:** petak bangunan = `w` ubin × (`roof` + `wall`) ubin, dikurangi 0,5 m; pintu di sisi selatan, kolom `door`; 1 ubin = 2 m.
- **Tinggi:** rumah dua lantai 6,3 m; ruko 3,6 m; balairung 4,8 m; sekolah 3,8 m; puskesmas 6,4 m; masjid 6 m (menara 13 m); gereja 5,5 m (menara 10 m); katedral 7,5 m; stasiun 5 m (menara jam 10 m).
- **Dinding:** plester dengan warna `wallColor`, atau satu dari `#f3e6c9 #cfe8d6 #f4d9c2 #f6ecb5 #dfe3ef #f2d0d0 #e6dcc8` menurut posisi; plint batu alam 0,3–0,6 m.
- **Atap:** limas dengan tepi 0,6 m. Genteng tanah liat bila `roofColor` merah, oranye, atau cokelat; seng berwarna bila lain.
- **Wajib di tiap bangunan:** papan nama dari `label`, pintu dua daun, jendela dengan bingkai putih, kaca yang menyala saat senja dan malam, dan teralis pada rumah dan balairung.
- **Gerbang:**
  - Lebar `w` ubin, lorong 4,2 m. Papan nama bernama kampung.
  - Mandarin: paifang, tiang merah, atap kuning dua tingkat.
  - Arab: gerbang putih berkubah hijau dengan bulan sabit.
  - Inggris: tiang batu dengan balok silang putih.
  - Jepang: torii merah dengan balok atas hitam.
  - Korea: tiang merah, balok hijau, atap abu dengan sudut terangkat.
- **Reklame:** papan di atas dua tiang (bawah 2,2 m), lebar `w` ubin × 0,85 (maks. 12 m), tinggi lebar/3,2; poster berbingkai 0,6 m dari tanah. Isi dari `panelFor` dan `frameAt/posterCanvas` yang sama dengan `/play`.

