# ADR-0022 — Kota, lima negara tujuan, warga lima bahasa, dan bangunan berbentuk asli

Status: **Dikerjakan (2026-10-07)**: peta, perjalanan berbayar, warga lima bahasa, dan gambar bangunan sudah jalan dan diuji di game lokal. Belum: misi yang memakai tempat-tempat baru, klip audio untuk kalimat baru, deploy. Melanjutkan [ADR-0021](0021-kereta-kelinci-dan-kota-zona-umum.md) dan menjawab keputusan terbuka di [`pare-perjalanan/penyesuaian-peta-baru.md`](../pare-perjalanan/penyesuaian-peta-baru.md) §5.

> **Nama zona (2026-10-07):** zona pusat Pare yang dulu bernama "Zona Umum" kini bernama **Kampung Bahasa**, di game, di pesan server, dan di semua dokumen. Kode zonanya tetap `umum`, jadi data pemain, misi, dan API tidak berubah. Di dokumen, "Kampung Bahasa" berarti zona pusat itu; kelima kampung disebut "kampung" atau dengan namanya (Kampung Inggris, dan seterusnya).

## 1. Keputusan

1. **Warga Kampung Bahasa berbicara lima bahasa.** Tidak ada warga baru khusus bahasa Inggris. Warga yang sama menjawab dalam bahasa yang sedang dipelajari pemain (`focus`), sehingga misi bahasa apa pun bisa memakai mereka.
2. **Kota adalah peta sendiri** (zona `kota`, 120×90): lebih besar dan lebih modern daripada Kampung Bahasa, dengan semua fasilitas Kampung Bahasa ditambah bandara internasional, stasiun dan terminal besar, universitas, sekolah, gedung bertingkat, mal, bioskop, rumah sakit, museum, masjid agung, katedral, klenteng. Warganya juga lima bahasa, jadi semua misi berlatar kota bisa ditaruh di sini untuk bahasa apa pun.
3. **Pergi ke kota naik bus atau kereta, berbayar.** Bandara pindah ke kota. **Bekas bandara di Kampung Bahasa menjadi Candi Bahasa**, cagar budaya di taman berhutan dengan dua kolam teratai.
4. **Tiap bahasa punya satu negara tujuan** dengan peta sendiri dan landmark khasnya: London (`gb`), Beijing (`cn`), Kairo (`eg`), Tokyo (`jp`), Seoul (`kr`). Setiap negara punya bandara dan imigrasi untuk pulang-pergi.
5. **Bangunan digambar menurut bentuk aslinya** dan gaya daerahnya, di semua zona.

## 2. Zona dan aturan

| Zona | Isi | Bahasa chat | Menu dan harga |
|---|---|---|---|
| `umum` | pusat Pare | lima bahasa, bukan Indonesia | menu `umum` |
| `kota` | kota | sama dengan `umum` | menu `umum` |
| `gb` `cn` `eg` `jp` `kr` | negara tujuan | bahasa negara itu saja | menu dan diskon level kampung bahasanya |

Di server, `ZoneBase(zone)` memetakan `kota → umum` dan negara → kampung bahasanya; aturan bahasa chat, menu, harga, dan diskon level memakai hasilnya. Di game, `isOpenZone()` dan `ABROAD_LANG` (`src/game/types.ts`) melakukan hal yang sama.

**Kelompok zona.** Pare (`camp`, `umum`, lima kampung), `kota`, dan tiap negara adalah kelompok terpisah. Laporan posisi dari game (tick atau soket) **tidak bisa** memindahkan pemain ke kelompok lain; hanya pembelian tiket yang bisa. Jadi gerbang dan kereta kelinci tetap gratis seperti dulu, tetapi kota dan luar negeri tidak bisa dimasuki tanpa membayar. Pengecualian: pingsan tetap memulangkan pemain ke kamar Camp dari mana pun.

## 3. Perjalanan dan tarif

`POST /pare/travel {to}` (`internal/pare/travel.go`). Server memeriksa bahwa di zona pemain ada titik berangkat menuju `to`, memotong tarif (uang sendiri atau voucher Premium), lalu memindahkan zona. Game memuat peta tujuan dan menaruh pemain di depan bangunannya.

| Rute | Titik | Tarif sekali jalan |
|---|---|---|
| Kampung Bahasa ↔ Kota, bus | `umum-terminal` ↔ `kota-terminal` | Rp7.000 |
| Kampung Bahasa ↔ Kota, kereta | `umum-stasiun` ↔ `kota-stasiun` | Rp7.000 |
| Kota ↔ negara, pesawat | `kota-bandara` ↔ `gb-bandara`, `cn-`, `eg-`, `jp-`, `kr-` | Rp50.000 |

Angka ini ditetapkan pemilik produk pada 2026-10-09 (sebelumnya Rp20.000, Rp25.000, Rp500.000, lalu pesawat Rp100.000; rancangan awal Rp3.000, Rp5.000, Rp45.000), supaya misi A2 bisa memakai Kampung Inggris, Kampung Bahasa, dan kota bergantian tanpa memberatkan. Catatan ekonomi: jawaban benar di kelas Basic dibayar Rp200 dan di level 3 Rp800, jadi tiket pesawat setara sekitar 63 jawaban benar di level 3. Tarif bisa diubah tanpa deploy kode lewat `prices.busTicket`, `railTicket`, `flightTicket` di `data/pare/content.json`; game membaca tarif dari `life.fares`.

**Imigrasi.** Jendela tiket pesawat ke luar negeri menampilkan petugas imigrasi yang bertanya dalam bahasa negara tujuan ("How long will you stay?"), dan pemain memilih jawabannya. Jawaban salah hanya menampilkan jawaban yang benar; tidak ada yang ditolak masuk. Saat pulang, pemain cukup menyerahkan paspor. Tiap bandara juga punya gedung imigrasi yang bisa dikunjungi (latihan singkat).

Tidak ada penerbangan langsung antarnegara atau dari Kampung Bahasa: semua lewat bandara kota.

### 3b. Adegan perjalanan dan harga di kota dan luar negeri (2026-10-07)

- **Adegan perjalanan.** Setelah tiket dibayar, pemain melihat ± 7 detik suasana di dalam kendaraan (`TravelScene.tsx`): bus yang berguncang dengan pegangan tangan berayun, kereta dengan rak bagasi dan jendela panjang, atau kabin pesawat yang lepas landas lalu terbang di atas awan. Pemandangan sawah bergeser di jendela dan gedung kota makin tampak menjelang tiba. Peta tujuan dimuat di baliknya; jeda iklan pindah zona tidak ditampilkan pada perjalanan bertiket.
- **Harga makanan dan sewa (diturunkan 2026-10-09).** Seluruh harga diturunkan supaya terjangkau dari hasil belajar: di Kampung Bahasa makan termurah Rp5.000 (nasi pecel) dan es teh Rp1.000; nasi ayam Rp8.000, bakso Rp6.000, sate ayam Rp9.000. Di Kampung Inggris nasi goreng Rp7.000 dan es teh Rp2.000. Sewa sepeda Rp1.500 sehari, kereta wisata Rp3.000, laundry Rp6.000. Kota mengenakan **150%** dari harga Kampung Bahasa (nasi pecel Rp7.500, nasi ayam Rp12.000, es teh Rp1.500), luar negeri **200%** dari harga kampung bahasanya; dibulatkan ke Rp500. Jadi luar negeri selalu lebih mahal daripada dalam negeri. Diskon level kampung tetap berlaku di negaranya. Bisa diubah lewat `menus` dan `prices.cityPercent`, `prices.abroadPercent` di `data/pare/content.json`.
- **Hotel.** Rp25.000 semalam di kota, Rp40.000 di luar negeri (`prices.hotelNight`, `prices.hotelNightAbroad`).
- **Flat mahasiswa (2026-10-09).** Di London, pemain yang tinggal setahun (B2) tidur di flat 12 Camden Road seharga Rp5.000 semalam (`POST /pare/flat`, `prices.flatNight`), karena hotel terlalu mahal untuk ditinggali. London diperpanjang ke selatan (72×78) dengan kawasan mahasiswa; negara lain tetap 72×56.
- **Kawasan City (2026-10-09).** Untuk C1, London diperpanjang lagi ke selatan (72×100) dengan kawasan City di tepi sungai: Thames Policy Lab, Housing Research Institute, The British Library, Committee Rooms, The Thames Herald, Press Centre. Tempat kerja C1 dibangun di peta, bukan dipinjam dari gedung lain (aturan: tempat yang dibutuhkan misi dibuat).
- **Kawasan South Bank dan Balai Mentor (2026-10-10).** Untuk C2, London diperpanjang ke selatan sekali lagi (72×122): penerbit, Southbank Centre, klub komedi, Moot Court, KBRI London, Broadcasting House, dan Speakers' Corner. Gedung Balai Mentor ditambahkan di barat daya tiap kampung bahasa; saat ini ia hanya papan keterangan dan tujuan langkah terakhir Misi Besar C2 (misi mentor harian belum dibuat).
- **Biaya ujian lompat level.** Rp25.000 + Rp10.000 per level (sebelumnya Rp50.000 + Rp25.000).

### 3a. Syarat level, hotel, dan pemain yang diam (diputuskan 2026-10-07)

- **Syarat level terbang.** Tiket ke suatu negara hanya dijual bila level pemain di bahasa negara itu sudah mencapai **B2 (level 4)**, sesuai ADR-0019. Selama isi pelajaran B2 belum ada, syaratnya level tertinggi yang punya isi: sekarang **level 3** di kelima bahasa (B1, HSK 3, Mutawassith 1, JLPT N3, TOPIK 3). Tanpa aturan ini tidak seorang pun bisa terbang, karena level 4 belum bisa dicapai. Begitu isi B2 masuk, syarat naik sendiri ke B2. Terbang pulang tidak pernah butuh level. Jendela tiket menandai tujuan yang masih terkunci beserta level yang diminta (`life.flight_min_level`). **Diubah 2026-10-09:** syaratnya kini **B1 (level 3)** secara tetap (`FlightLevel = 3`), karena Misi Besar B1 memuat penerbangan ke London; lihat Catatan no. 4.
- **Hotel.** Di kota dan di luar negeri, pintu hotel punya tombol **Menginap** (`POST /pare/hotel`; harga di §3b). Pemain tertidur di tempat itu dan bangun di sana. Kasur kamar Camp tetap gratis, tetapi tidak bisa dipakai dari kota atau luar negeri (`/pare/sleep` menolak dengan `far_from_camp`).
- **Pemain yang diam lebih dari satu jam** di kota atau luar negeri tetap di sana (di Pare tetap dianggap pulang ke kamar). Sebelumnya aturan itu memulangkan pemain dari London ke Camp tanpa tiket.
- **Pingsan** tetap memulangkan pemain ke Camp dari mana pun. Itu juga jalan pulang terakhir bagi pemain yang kehabisan uang di luar negeri; jalan biasanya adalah belajar di universitas negara itu sampai uangnya cukup untuk tiket.

## 4. Warga lima bahasa

- `src/game/world/poly.ts` menyimpan tiap kalimat dalam lima bahasa (teks + cara baca) dengan arti Indonesianya: 8 sapaan umum dan 2–3 kalimat untuk tiap dari 20 jenis tempat.
- Petugas di pintu tiap tempat (`talk: "poly"`) mengucapkan kalimatnya dalam bahasa `focus` pemain. Pemandu lama Kampung Bahasa (Mas Doni, Bu Sri, dan lain-lain) tetap menjelaskan cara bermain dalam bahasa Indonesia, tetapi membuka dengan sapaan dalam bahasa `focus`.
- **Kunjungan tempat** (`VenueModal`): orang di sana berbicara dalam bahasa `focus` (di luar negeri: bahasa negara itu), pemain memilih artinya. Hadiah tetap 12 XP + Rp600 sekali sehari per tempat. ID tempat: jenisnya saja di Kampung Bahasa (`museum`), `kota-<jenis>` di kota, `<negara>-<jenis>` di luar negeri; masing-masing dihitung sendiri.
- Semua warga Kampung Bahasa dan kota kini punya `key` (sama dengan `id`-nya), sehingga data misi bisa menunjuk mereka. Game membuka misi pada warga zona terbuka untuk bahasa misi apa pun; di kampung dan negara tetap hanya bahasa zona itu.

## 5. Peta

**Kota** (`world/city.ts`). Empat jalan raya barat–timur dan lima utara–selatan membentuk blok:

| | Barat | Tengah-barat | Tengah-timur | Timur |
|---|---|---|---|---|
| Utara | Bandara internasional: landasan, apron, terminal, menara kontrol, kantor imigrasi, hangar (selebar peta) | | | |
| Baris 1 | Universitas Kota | Menara Bahasa (perkantoran), Bank Kota, Hotel Kota | Balai Kota (papan misi) dan alun-alun dengan Tugu Kota | Mal Kota (belanja) |
| Baris 2 | Sekolah Kota, Perpustakaan Kota | Taman Kota dan danau (memancing) | Masjid Agung | Bioskop, Rumah Sakit (nyawa) |
| Baris 3 | Apartemen, Kantor Pos | Rumah Makan, Kedai Kopi, Minimarket, Pasar Kota, gerobak | Katedral, Klenteng | Museum Kota, Sewa Sepeda |
| Baris 4 | Menara dan apartemen | Stasiun Kota (rel di tepi selatan) | Terminal Bus Kota | Speaking Club, Language Challenge |

**Negara** (`world/abroad.ts`, 72×56). Tata jalannya sama di kelima negara supaya bandara dan jalan pulang selalu di tempat yang sama: bandara dan imigrasi di utara, universitas (kelas bahasa itu) di barat laut, hotel dan museum di timur laut, jalan makanan, pasar dan taman di barat daya, landmark di tenggara. Papan nama memakai bahasa setempat diikuti kata Indonesianya.

| Negara | Landmark dan bangunan khas |
|---|---|
| London | Big Ben dan Houses of Parliament, London Eye, Tower Bridge di atas Thames, Buckingham Palace, British Museum, bus tingkat merah, taksi hitam, kotak telepon merah |
| Beijing | Kuil Surga (天坛), Tembok Besar, gapura paifang, pagoda, aula Kota Terlarang (故宫), rumah hutong |
| Kairo | tiga piramida Giza dan Sfinks, obelisk, Sungai Nil, Masjid dan Universitas Al-Azhar, pasar Khan el-Khalili (arkade), rumah beratap datar; tema gurun |
| Tokyo | Tokyo Tower, Gunung Fuji di cakrawala, kastel, pagoda lima tingkat dan gerbang torii, Stasiun Tokyo bata merah, sakura |
| Seoul | gerbang Gwanghwamun dan balairung Gyeongbokgung, N Seoul Tower di Namsan, rumah hanok |

**Kampung Bahasa**: bandara diganti Candi Bahasa (tiga menara batu bergaya Prambanan di atas teras, gapura bata, dua stupa, dua kolam, papan cagar budaya). Terminal Bus dan Stasiun Kereta kini menjual tiket ke kota.

## 6. Bangunan berbentuk asli

`src/game/engine/architecture.ts`. Bangunan meminta bentuk lewat `form` (dan `variant`), boleh menjulang di atas tapaknya (`rise`, dalam petak) sehingga pemain bisa berjalan di belakang bagian yang tinggi. Landmark adalah dekor `monument`; kendaraan dekor `vehicle`.

- **Bentuk bangunan (20):** `tower` (kaca, kantor, apartemen, hotel), `mall`, `airport`, `control`, `station` (kolonial atau `grand` beratap kaca), `busterminal`, `classic` (museum, bank, balai kota; `college` = kampus Gotik), `school`, `hospital`, `cinema`, `mosque` (Nusantara atau Mamluk Mesir), `church`, `cathedral`, `pura` (candi bentar dan meru), `klenteng`, `candi`, `palace` (Beijing, Seoul, kastel Jepang, Buckingham, aula kayu Jepang), `pagoda`, `souk`, `madrasa`.
- **Landmark (16):** Big Ben, Tower Bridge, London Eye, piramida, Sfinks, obelisk, Kuil Surga, Tembok Besar, paifang, torii, Tokyo Tower, Fuji, N Seoul Tower, tugu kota, stupa, gapura.
- **Yang diubah di zona lama:** rumah ibadah, sekolah, bioskop, museum, imigrasi, bank, terminal, stasiun, dan puskesmas di Kampung Bahasa kini berbentuk asli. Kampus tiap kampung mengikuti negaranya: kampus Gotik (Inggris), aula istana beratap kuning (Mandarin), madrasah dengan menara (Arab), aula kayu beratap gelap (Jepang), gerbang istana (Korea). Toko dan rumah di Kampung Arab beratap datar dengan tembok pembatas, bukan atap genting miring. Bendera Mesir ditambahkan.

`bun scripts/e2e/art.ts <zona> [x y w h] [skala] [nama]` merender gambar sebuah zona ke PNG tanpa backend dan tanpa login; dipakai untuk memeriksa semua bentuk di atas.

## 7. Yang berubah di kode

| Tempat | Perubahan |
|---|---|
| `game/src/game/world/` | baru: `city.ts`, `abroad.ts`, `travel.ts`, `poly.ts`, `kit.ts`; `kota.ts` (distrik Kampung Bahasa) ditulis ulang; `zones.ts`, `countries.ts` (Mesir), `english.ts` (kampus) |
| `game/src/game/engine/` | baru: `architecture.ts`; `props.ts` (rumah Arab beratap datar, kanvas untuk bagian yang menjulang) |
| `game/src/components/game/` | baru: `TransitModal.tsx`; `VenueModal.tsx` (lima bahasa), `NpcDialog.tsx`, `Game.tsx` |
| `game/scripts/e2e/` | baru: `art.ts`, `travel.ts` |
| `titian-backend-go/internal/pare/` | baru: `travel.go`; `life.go`, `content.go`, `hub.go`, `daily.go`, `mission.go`, `routes.go` |
| `titian-backend-go/db/migrations/` | `0098_pare_zones_city_abroad.sql`: batasan `pare_players.zone` menerima zona baru |

Foto landmark: di kampung tetap dicatat per bahasa (`photo:en`); di luar negeri per negara (`photo:gb`), jadi London dihitung terpisah dari Kampung Inggris.

## 8. Diuji

- Server: `TestTravelNeedsATicket` (tanpa rute atau tanpa uang ditolak, tarif terpotong, zona pindah, laporan posisi tidak bisa memulangkan pemain dari London, menu London = menu Inggris, kunjungan dan foto di London dibayar) dan `TestZoneBase`; seluruh paket `internal/pare` lulus.
- Game: `tsc` bersih; `check-map.ts` lulus untuk `kota` dan kelima negara; `check-trains.ts` lulus.
- UI sungguhan (`scripts/e2e/travel.ts`, backend uji lokal): bus ke kota, kereta pulang, lalu imigrasi dan terbang ke London, masing-masing dengan adegan perjalanannya (Rp2.000.000 → Rp1.980.000 → Rp1.955.000 → Rp1.455.000).
- UI sungguhan (`scripts/e2e/abroad.ts`): dengan level 0 semua penerbangan terkunci dan menyebut level yang diminta; menginap di hotel London memotong harga semalam dan pemain tertidur di London.

## 9. Belum dikerjakan dan risiko

1. **Misi A2 dan B1 sudah memakai tempat baru (2026-10-09); B2–C2 belum.** B1 memakai Kota, Kampung Bahasa, Kampung Inggris, dan London (`penyesuaian-peta-baru.md` §4b). Ke-25 misi A2 bahasa Inggris dimainkan di Kampung Inggris, Kampung Bahasa (Museum Bahasa, Candi Bahasa, Warung Pecel, stasiun) dan Kota (terminal, mal, bank, hotel, rumah sakit, bioskop, stasiun, bandara); lihat `penyesuaian-peta-baru.md` §4a. Tempat B1–C2 di `journey/en/world.ts` masih "baru" dan belum menunjuk zona `kota` atau `gb`.
2. **Audio (dibuat dan diunggah 2026-10-07).** 255 klip suara untuk kalimat `poly.ts` (sapaan, kalimat di 20 jenis tempat, pengumuman bus/kereta/pesawat) di lima bahasa dan warga Kairo sudah dibuat, lulus cek dengar, dan diunggah ke bucket R2 (`audio/manifest/<bahasa>-0.json`, ref `poly:*`); produksi sudah menyajikannya. 30 klip yang terdengar berlawanan gender dibuat ulang dengan `scripts/audio/fix-gender.ts`, dan suaranya dikunci di `audio/voices/`. Suara perjalanan (mesin bus, sambungan rel, kabin pesawat, nada tiba) disintesis di peramban (`sfx.ts`), tanpa berkas. Kalimat baru di `poly.ts` butuh `annotate.ts`, `generate.ts`, lalu `upload.ts` lagi.
3. **Kehabisan uang di luar negeri.** Pemain yang tidak punya Rp50.000 untuk pulang harus belajar di sana sampai cukup, atau pingsan (dipulangkan ke Camp). Jendela tiket belum memperingatkan sebelum berangkat bahwa uang yang tersisa tidak cukup untuk pulang.
4. **Syarat level terbang ditetapkan di B1 (level 3) sejak 2026-10-09**, bukan B2: Misi Besar B1 bahasa Inggris berakhir dengan penerbangan beasiswa ke London, dan hidup di luar negeri adalah cerita B2 (§3a tetap berlaku untuk bahasa yang isinya berhenti di bawah B1).
5. **Kereta kelinci** tidak masuk kota atau luar negeri. Billboard iklan belum dipasang di zona baru.
6. **Deploy.** Migrasi 0098 dan backend harus naik lebih dulu daripada game; game lama tidak terpengaruh oleh backend baru.
