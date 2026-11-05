# Pare-11: Kampung Bahasa 3D siap produksi

Dasar: [`../kampung-3d/audit-produksi.md`](../kampung-3d/audit-produksi.md) (temuan F1–F17, saran fitur, urutan). Pemilik produk (2026-10-14): halus, indah, kontrol standar industri, UI/UX siap produksi, misi dan semua bahasa tetap jalan, sinkron dengan pixel art, pemain memilih tampilan.

Aturan sama dengan Pare-10: satu tiket per sesi, `/play` tidak boleh berubah perilakunya, catat QA di bagian Catatan, uji di HP sungguhan oleh pemilik di akhir P11-003, P11-006, P11-008.

| Tiket | Isi | Status |
|---|---|---|
| P11-001 | Pengaman produksi: tanpa WebGL → `/play?px=1`; konteks grafis hilang → layar pemulihan | ✅ 2026-10-14 |
| P11-002 | Pilihan tampilan di akun (`engine`), pengalihan `/play`→`/start`, tombol di AKU dan Bantuan. Sisa: pemain 3D tampil bergaya Lemari di `/play`; aksi dua pemain di `/play` | 🔶 inti selesai |
| P11-003 | Kontrol dan kamera: joystick analog, kamera mengikuti, tabrakan kamera, sisi joystick. Sisa: ketuk untuk bergerak, orang pertama menembus dinding, sensitivitas, getar | 🔶 inti selesai |
| P11-004 | Dunia: tabrakan sungguhan per bentuk bangunan (ganti jarak ekstra), skala genteng, varian gedung (cn/jp/kr/gb), foto menara kontrol dan souk, efek hidup (kupu-kupu, kunang-kunang), cuaca, malam (F2: pemilik meninjau) | ⬜ |
| P11-005 | Karakter dan animasi: lari, interpolasi pemain lain, pose duduk/naik, animasi makan (`onPurchased`, butuh keputusan). Lempar koin berbayar ✅ | 🔶 |
| P11-006 | UI/UX produksi: HUD di 360×640 dan landscape, tombol 44 px, area aman, banner misi dapat dilipat, tur pertama, pengaturan terpadu, ukuran teks, kurangi gerakan. Selesai: daftar aksi ringkas 44 px di HP. Sisa: landscape, area aman, tur, pengaturan terpadu | 🔶 |
| P11-007 | Suara: langkah kaki, suasana, musik, tombol bisukan. Sisa: didengar dan disetel oleh pemilik; suara di pixel | 🔶 kode selesai |
| P11-008 | Kualitas otomatis berdasar FPS, ingat pilihan, telemetri FPS/perangkat/galat, sembunyikan "Tinggi" di layar sentuh sempit. Sisa: tampilan data di dashboard admin, uji FPS HP sungguhan | 🔶 kode selesai, backend sudah di prod |
| P11-009 | Paritas misi dan bahasa: titik uji stabil (`data-testid`) di Game, skrip e2e 3D untuk lima bahasa, jalur belajar, kota dan luar negeri. Selesai: tiga skrip e2e (`ui3d`, `parity3d`, `path3d`) hijau. Sisa: misi bahasa lain (belum ada misinya), misi dengan langkah kota/luar negeri | ✅ inti |
| P11-010 | Sosial: ketuk pemain → kartu (profil, pesan, ajak, blokir, lapor), `setGoalZone`, teman. Selesai: ketuk pemain membuka kartu. Sisa: panah ke pintu keluar, teman dan kehadiran | 🔶 |
| P11-011 | Rilis bertahap: label beta, persentase pengguna, `/3d-concepts` hanya pengembangan, rollback | ⬜ |
| P11-012 | Keamanan gerak: batas jarak per detik di hub, batas laju aksi sosial | ⬜ |

## Catatan

### Hari pertama (2026-10-14, Sonnet 5.5)

**Dikerjakan:**
- **P11-001:** `Start3DLoader` memeriksa WebGL (`lib/engine-pref.ts`, `webglOk`); tanpa WebGL pemain dialihkan ke `/play?px=1`. `Start3D` memasang `webglcontextlost` dan menampilkan layar dengan "Muat ulang" dan "Pakai pixel art".
- **P11-002:** migrasi `0105_pare_engine.sql`, `pare_players.engine`, `PUT /pare/me/engine`, `PlayerView.engine`. Klien: `PlayerProfile.engine`, `pareApi.setEngine`, `shouldOpen3D` di `Game.resolve`, `EngineSwitch` di AKU dan Bantuan. Tes Go `TestEnginePreference` lulus. Uji peramban lokal: pilih 3D → `/play` membuka `/start`; AKU → "Main dengan pixel art" → `/play?px=1` dan `engine = pixel` di server.
- **F2:** malam dinaikkan (`atmosphere.ts`: hemi 0,35→0,7, bulan 0,45→1,0, eksposur 0,9→1,0, langit hemi dan tanah lebih terang). Menyimpang dari panduan gaya karena malam hampir hitam tidak bisa dimainkan; pemilik meninjau.
- **Peluncur Lemari** kini di bawah jendela game (z-index 25 < 30), tidak lagi menimpa menu AKU.
- **Uji misi di 3D:** `scripts/e2e/ui3d.ts` (salinan `ui.ts` untuk `/start`). Misi `en-0-greet`, langkah 1 (Miss Kate) lolos. Langkah 2 (Tom) tidak terbukti: jawaban tersorot tapi tak terkirim, dan versi pixel `ui.ts` juga gagal di langkah itu (skrip bergantung teks petunjuk lama). Tidak disimpulkan sebagai regresi 3D; ditangani di P11-009.

**Build produksi:** `next build` lolos; `tsc` dan `eslint src` bersih.

**Belum diuji:** kamera Lemari di HP setelah perubahan terbaru (hanya emulasi), malam di jam lain, iOS Safari, dan perangkat sungguhan.

**Perlu keputusan pemilik:**
1. Bawaan tampilan untuk akun baru: tetap pixel (saran sekarang) atau 3D setelah beta.
2. `/play` menampilkan ajakan dari pemain 3D sebagai pesan kecil atau mengabaikan.
3. Lempar koin tetap gratis atau Rp500; animasi makan setelah membeli (menyentuh `/play`).
4. Dua gaya karakter saat peluncuran (Kartun + Blok) atau semuanya.

### Keputusan pemilik dan pekerjaan lanjutan (2026-10-14, Sonnet 5.5)

**Keputusan pemilik:** (1) akun baru bawaan 3D; (3) lempar koin berbayar Rp500; (4) saat peluncuran hanya satu gaya, Kartun khas Titian. Butir (2) (ajakan dari pemain 3D di `/play`) dikosongkan: tetap diabaikan sampai diputuskan.

**Dikerjakan:**
- **Akun baru bawaan 3D:** `CreatePlayerProfile` mengisi `engine = '3d'`; pemain lama tetap `pixel` (bawaan kolom). Setelah onboarding, `Game` menyimpan fokus dan tur hari pertama, lalu membuka `/start` (bila WebGL ada). Tes `TestEnginePreference` diperbarui.
- **Lempar koin Rp500:** `POST /pare/pond/coin` → `{money, price}` (`internal/pare/pond.go`, ledger kind `coin`); 422 `insufficient_money` bila uang kurang. Klien: `parePond.coin`, `Start3D` memotong uang dulu baru melempar, pesan galat sebagai pemberitahuan. Tes `TestTossCoin`.
- **Satu gaya:** `Wardrobe.tsx` `LAUNCH_STYLES = ["kartun"]`: tab Gaya disembunyikan, gaya lain tetap di kode. Look tersimpan bergaya lain ditampilkan sebagai Kartun saat Lemari dibuka.
- **HUD HP (P11-006):** daftar aksi mulai di bawah banner misi (top 200 px), tombol 44 px, hanya dua aksi pertama + 😊 + "⋯ n lagi"; dibuka: daftar bergulir, banner "Ketuk untuk…" menyingkir, tombol ✕ Tutup selalu terlihat. Banner "Ketuk untuk…" naik ke `bottom-[15rem]` (menyentuh `/play` hanya di layar sentuh). Dilihat di emulasi 360×640 dengan misi aktif.

**Uji:** tes Go `pare` (101 dtk), `economy`, `admin` lulus; `tsc` dan `eslint src` bersih.

**Deploy backend (2026-10-14 04:55 WIB):** migrasi `0105` dan `POST /pare/pond/coin` sudah di prod (cadangan `/home/john/backups/titian_pre_engine_20261013T215138Z.sql.gz`, `:prev` = image aksi dua pemain). 230 pemain yang ada tetap `pixel`; hanya akun baru yang masuk 3D. Terverifikasi: kesehatan, kolom, rute (401 tanpa token), tanpa WARN/ERROR. Frontend baru boleh di-push sekarang.

### P11-008 (2026-10-14, Sonnet 5.5)

**Kualitas otomatis** (`Start3D.watchSpeed`): kecepatan diukur per jendela empat detik waktu nyata (jendela pertama dilewati karena shader; jeda tab atau layar tidur tidak dihitung). Bila dua jendela berturut-turut di bawah 26 fps dan pemain belum memilih sendiri, grafik turun **satu** tingkat (tidak lompat ke Hemat), diumumkan, dan disimpan dengan tanda `kb3d-grafik-auto` supaya masih boleh turun lagi di kunjungan berikut. Memilih lewat ⚙ menghentikannya. Tidak pernah naik sendiri. Tingkat "Tinggi" tidak ditawarkan di layar sentuh lebih sempit dari 800 px.

**Laporan** (`POST /pare/reports`, migrasi `0106`): satu laporan `perf` setelah jendela stabil pertama dan satu tiap penurunan, berisi fps, tingkat, jumlah draw call dan segitiga, kelas layar (sentuh, lebar, tinggi, dpr), dan nama kartu grafis (`WEBGL_debug_renderer_info`); `error` (tiga pertama) dan `context_lost`. Tanpa chat atau posisi; batas 40 per pemain per jam; catatan privasi ditambahkan di Bantuan.

**Uji lokal** (GPU Intel HD 4000, grafik dipaksa Tinggi): setelah sekitar 100 detik turun ke Sedang (24,5 fps), tersimpan sebagai otomatis, dan dua laporan `perf` masuk ke tabel. Tes Go `TestClientReports` (jenis tak dikenal, tampilan tak dikenal, terlalu besar ditolak; banjir dibatasi 40) lulus.

**Deploy backend (2026-10-14 06:40 WIB):** migrasi `0106` dan `POST /pare/reports` sudah di prod (cadangan `/home/john/backups/titian_pre_reports_20261013T233659Z.sql.gz`, `:prev` = image 04:55). Tabel ada (0 baris), 401 tanpa token, tanpa WARN/ERROR. **Belum:** tampilan data di dashboard admin; FPS di HP sungguhan (data masuk setelah `game` di-push).

### P11-007 (2026-10-14, Sonnet 5.5)

**Dibuat** (`src/game3d/start/audio.ts`, `WorldAudio`): semua suara dibuat dari gelombang dan derau saat main (tanpa berkas, tanpa lisensi, tanpa unduhan).
- **Langkah kaki:** tiap setengah putaran fase kaki, suaranya menurut tanah di bawah pemain: batu (paving), aspal, kayu (lantai kamar, jembatan), tanah, rumput, karpet/tatami; lebih tegas bila lebih cepat.
- **Suasana:** angin lembut di luar, hujan menurut cuaca (juga teredam dari dalam ruangan), kicau burung acak di siang hari (05:30–17:30, tanpa hujan lebat), jangkrik di malam hari, dan dengung ruangan di dalam kamar.
- **Aksi:** cipratan koin, jepretan foto, tepuk tangan saat tos, nada kecil saat ada ajakan.
- **Musik:** jalan lambat melalui nada pentatonik (C mayor), akor lembut sesekali; lebih rendah dan lambat di malam hari dan di dalam ruangan.
- **Kontrol:** dua tombol di menu ⚙ ("🔊 Suara" dan "🎵 Musik", nyala/mati), tersimpan di perangkat (`kb3d-suara`); suara berhenti saat tab disembunyikan; mulai pada ketukan atau tombol pertama (atau segera bila halaman sudah pernah disentuh).

**Terukur (tanpa telinga, `AnalyserNode` di keluaran, lalu master dinaikkan ×2,2):** diam dengan semua nyala 0,031; berjalan 0,047; musik mati diam 0,008 (hanya angin); musik mati berjalan 0,023 (langkah jelas di atas suasana); semua mati 0,000; pilihan tersimpan.

**Belum:** saya tidak bisa mendengar; keseimbangan dan selera (terlalu keras, musik mengganggu, kicau terlalu sering) perlu didengar pemilik dan disetel. Musik bawaan nyala pelan; bila terasa mengganggu, ubah bawaan di `loadSoundPrefs`.

### P11-010, bagian pertama (2026-10-14, Sonnet 5.5)

**Ketuk pemain membuka kartunya** (`Start3D.tapAt`): ketukan pendek (< 500 ms, bergeser < 8 px) pada tubuh seseorang (garis kaki–kepala selebar jari) memanggil `onPlayerTap` yang sama dengan `/play`, jadi kartu, aksi, dan aturannya sama persis. Pemain lain membuka kartu mereka; karakter sendiri membuka kartu sendiri ("Ini kamu", Edit profil); warga dan keramaian server tidak membuka apa-apa. Tidak aktif saat jendela game terbuka atau Lemari terbuka. Uji lokal dengan pemain uji kedua (`qa0001`): ketukan pada tubuhnya membuka kartu "Andi @andi10" dengan "💬 Ngobrol". Blokir dan lapor ada di dalam chat personal, seperti di `/play`.

**Temuan saat menguji:** kamera ditarik terlalu dekat (1,4–1,6 m dari 6 m) oleh pagar rendah (`X`) dan oleh jarak aman bangunan, padahal kamera melihat dari atas pagar. Kini kamera tidak memakai jarak aman 0,45 m (khusus pemain), dan pagar yang lebih rendah dari kamera tidak menghalangi (`blocked(x, z, r, pad, above)`). Di titik uji jarak kamera kembali 6,0 m.

**Belum:** panah ke pintu keluar (`setGoalZone`), daftar teman dan kehadiran, dan ketuk di kamera orang pertama.

### P11-009 (2026-10-14, Sonnet 5.5)

**Tiga skrip uji** di `game/scripts/e2e/` (daftar di `README.md`), semuanya di game 3D, dengan data uji lokal:

1. **`parity3d.ts`, keterjangkauan tiap zona.** 13 zona (kamar camp, desa umum, lima kampung bahasa, kota, lima negara). Di tiap zona pemain ditempatkan di tempat bebas di samping tiap warga dan tiap *kelompok* objek (satu gedung kursus adalah ratusan ubin objek; yang dituntut: bisa dituju dari tepinya), lalu mesin ditanya apa yang dilakukan `E`. **Hasil: semua warga terjangkau** (camp 0, umum 42, en 21, zh/ar/ja/ko 11, kota 35, gb 31, cn 10, eg 11, jp 10, kr 10) **dan semua 13 zona lolos**: semua kelompok objek terjangkau, titik awal (home) bebas, tanpa galat halaman. Kelompok objek: camp 5, umum 69, tiap kampung 39, kota 77, gb 46, cn 24, eg 21, jp 24, kr 25. Satu kasus (bangku di sawah desa umum, hanya bisa dituju dari jalan setapak satu ubin) bergantung pada ada tidaknya petani di jalan itu: bila ada, warga dahulu yang dituju; dicatat sebagai "terhalang orang", bukan gagal. Draw call di titik awal pada grafik Rendah: kampung 313–369 (batas 350: **Kampung Korea 369 dan Kampung Inggris 366 menembus batas**), kota 48, luar negeri 73–79.
2. **`ui3d.ts`, misi penuh lewat UI 3D.** `en-0-greet` (6 langkah: bicara, dialog ×4, baca), `en-0-numbers` (bicara, dialog, dengar, beli, dengar, bicara), `en-0-food` (pergi, dialog, beli, dialog, lakukan, bicara), dan misi warga `en-0:villager:tom`: **semuanya selesai, nilai 100, tiga bintang.** Jenis langkah yang melalui UI: bicara, dialog, dengar, baca (jawab dan PERIKSA di jendela game yang sama), yang melalui API (seperti `ui.ts`): beli, lakukan, pergi.
3. **`path3d.ts`, jalur belajar tiap bahasa.** Inggris, Mandarin, Arab, Jepang, Korea: desa termuat, BELAJAR membuka jalur bahasanya, langkah berikutnya mulai dan isinya tampil (kartu "living room", 马 mǎ, harakat Arab, hiragana, hangul), tanpa galat halaman. **Hijau 5/5.**

**Temuan penting:** hanya bahasa Inggris yang punya misi (158); Mandarin, Arab, Jepang, dan Korea punya jalur belajar tetapi misinya belum ada (jalurnya sendiri memberi tahu: "misinya belum ada"). Jadi "semua misi, semua bahasa" yang bisa diuji sekarang sudah diuji; misi bahasa lain menunggu konten.

**Yang ditemukan lewat uji dan diperbaiki di skrip (bukan di game):** posisi pemain tertimpa bila token disetel lewat `/play`; id warga di misi adalah `spawn.key`; misi baru "hidup" bagi warga setelah tracker menampilkan langkahnya; pilihan jawaban butuh PERIKSA. Satu temuan di game: kamera terlalu dekat karena pagar rendah (sudah diperbaiki di P11-010).

**Belum:** misi dengan langkah di kota dan luar negeri (hanya ada bila ada misi bahasa lain / misi kota), `data-testid` stabil (skrip masih memakai teks tombol), dan jalankan otomatis di CI.

**Perlu diperbaiki di game (baru):** draw call kampung bahasa di grafik Rendah menembus 350 di Korea (369) dan Inggris (366): perlu dipangkas (P11-004), mis. gabung lebih banyak bangunan atau kurangi pohon di Rendah.

### F18, draw call kampung bahasa (2026-10-14, Sonnet 5.5)

`parity3d` menemukan titik awal Kampung Korea (369) dan Kampung Inggris (366) di grafik Rendah menembus batas 350. Pengukuran per mesh: 451 mesh dalam satu potongan wilayah memakai **satu** material, karena `mergeStatic` hanya menggabungkan mesh di bawah induk yang sama (satu bangunan), jadi material yang sama digambar sekali per bangunan.

**Perbaikan:** `mergeDeep` (`src/game3d/merge.ts`) menggabungkan semua mesh diam satu potongan wilayah menurut material, per sel 30 m (supaya kamera masih bisa membuang yang di luar pandangan); yang bergerak (`userData.keep`), bayangan semu (`blob`), terinstans, atau berinduk tidak disentuh. Dipanggil di `zone.ts` setelah `mergeStatic`.

**Hasil (Rendah, titik awal):** Inggris 366 → **241**, Korea 369 → **278**, Mandarin 315 → **255**, Kota 48 → 50. Segitiga naik karena potongan digambar utuh bila sebagian terlihat: Inggris 144 rb → 162 rb, Korea 141 → 163 rb, Mandarin 143 → 178 rb (batas 200 rb). `parity3d` masih hijau di keempat zona; tampilan dilihat (dinding, jendela berteralis, orang, paving utuh).

**Catatan:** batas segitiga kini lebih dekat (Mandarin 178 rb dari 200 rb); bila bangunan ditambah, ukur ulang dengan `parity3d` dan pertimbangkan sel 20 m.

### Perombakan visual, tahap 1 (2026-10-14, Opus 5.5)

Permintaan pemilik: karakter, bangunan, dan objek masih terlihat sangat low-poly dan seperti aplikasi belum jadi; ingin lebih "3D sungguhan". Digabung dengan P11-004/005/006.

**Alat:** `scripts/qa/look3d.ts`: sepuluh gambar tetap (tempat, jam, dan kamera yang sama) untuk membandingkan sebelum dan sesudah; `QA_DESKTOP=1280x720`. Gambar "sebelum" di `/tmp/pare-video/look-before`.

**Penyebab kesan low-poly (dari gambar "sebelum"), dan yang dikerjakan:**
1. **Warna pucat seperti pastel**: kurva ACES + cahaya isi (hemisfer, pantulan langit) terlalu kuat, sehingga hijau dan batik luntur dan bayangan hilang. Kini `NeutralToneMapping`, matahari lebih kuat, cahaya isi lebih rendah (`atmosphere.ts`: pagi env 0,75→0,4, hemi 0,55→0,3, matahari 3,8→4,3, eksposur 0,46→0,62; senja dan malam disetel ulang untuk kurva baru). **Menyimpang dari angka panduan gaya dengan sengaja.**
2. **Pohon dan pagar tanaman bersegi**: geometri daun tidak dilas, jadi tiap segitiga terlihat. Kini dilas (`mergeVertices`) sehingga cahaya menggulung halus, warna lebih gelap di bawah dan terang di atas, tajuk lebih penuh (9 gumpalan).
3. **Balok kuning** penanda objek (terlihat seperti aset sementara) diganti cincin lembut di tanah, dan tidak digambar di dalam bangunan.
4. **Bunga oktahedron** diganti kepala bunga bulat.
5. **Karakter**: akun uji tersimpan bergaya Realis (manekin kurus); sesuai keputusan satu gaya, semua orang kini digambar bergaya Kartun (`launchLook`), pakaian tetap.

**Dilihat (Tinggi, 1280×720):** karakter depan, warga, taman, senja, malam. Malam terbaca (jendela menyala, tanah terlihat); senja hangat tetapi dinding yang membelakangi matahari masih cokelat gelap. `parity3d` (en, ko) hijau; `tsc` dan `eslint src` bersih.

**Kinerja (Rendah, titik awal, `parity3d`):** percobaan pertama menembus anggaran segitiga (612 rb, karena kepala bunga bulat dan daun lebih rapat); setelah disesuaikan (di Rendah/Hemat: daun tetap kasar tetapi dilas, 6 gumpalan, bunga oktahedron dilas) Inggris **195 call / 162 rb**, Korea 198 / 192 rb, Mandarin 198 / 195 rb (batas 350 / 200 rb; Korea dan Mandarin dekat batas segitiga).

**Belum (tahap berikut, urut dampak):** bangunan (tepi tumpul, kusen, talang, variasi dinding, atap menjorok, AO di kaki dinding); kota (menara masih kotak putih polos); gerak karakter (ayunan lengan, condong saat lari, pemain lain meluncur); tanah (tepi jalan/trotoar, peralihan rumput–paving); air; lalu sisa P11-006 (landscape, area aman, tur, pengaturan terpadu). Kinerja Rendah/Hemat setelah perubahan cahaya belum diukur di HP.

### Perombakan visual, tahap 2: bangunan dan gerak (2026-10-14, Opus 5.5)

- **Menara kota (`form: "tower"`, 17 gedung):** dulu kotak plester putih dengan kaca hanya di depan dan belakang. Kini podium batu dengan bibir putih dan kanopi masuk bertiang, badan berkaca di **empat sisi** dengan bibir pelat lantai dan sirip antar-bidang, sudut berplester, parapet, ruang mesin dan tiang di atap. Varian: `glass` = dinding tirai kaca berwarna dari `wallColor`; `flats` = balkon berpagar; lainnya jendela pita. Kaca menara ikut menyala saat senja (`kit.dusk`).
- **Bayangan kontak:** pita gelap lembut di tanah sekeliling kaki tiap bangunan (memudar 1,5 m), supaya bangunan "menapak" dan tidak terlihat melayang.
- **Gerak:** makin cepat, badan makin condong dan siku makin menekuk, dengan sedikit naik-turun saat lari; jalan santai dan lari tidak lagi tampak sama. Berlaku untuk pemain dan orang lain.
- **Kecelakaan dan pemulihan:** saat menyunting, ekor `buildings.ts` (bagian dekor) terpotong; dipulihkan utuh dari commit terakhir (`git show HEAD:`), `tsc` bersih, diff berkas hanya perubahan yang dimaksud.

**Dilihat:** kota (Tinggi, 1280×720): podium batu, menara kaca, bangku, orang. **Belum dilihat:** bayangan kontak dari dekat, gerak lari (gambar diam tidak menunjukkannya), varian `flats`, bangunan kampung setelah perubahan ini.

**Kinerja (Rendah, `parity3d`):** Kampung Inggris 201 call / 163 rb; Kota 52 call / **126 rb** (naik dari 56 rb karena detail menara; masih di bawah 200 rb). `tsc` dan `eslint src` bersih.

### Perombakan visual, tahap 3: tanah dan cahaya (2026-10-14, Opus 5.5)

- **Trotoar (kerb):** bibir beton 14 cm di tempat jalan aspal bertemu rumput atau paving (tidak di tempat jalan setapak menyeberang), digabung per potongan wilayah. Tepi jalan tidak lagi berupa garis tekstur lurus.
- **Penanda pintu keluar zona:** cakram biru pejal diganti cincin biru lembut di tanah (seperti penanda objek).
- **Cahaya siang:** putih tampak kebiruan; langit hemisfer dihangatkan (`#cfe3ff` → `#eaf0fb`), tanah hemisfer `#8c8468`, pantulan langit 0,4 → 0,3, hemisfer 0,3 → 0,38. Putih masih sedikit dingin di bayangan (wajar di bawah langit biru).
- **Gambar 06** dipindah (titik lama berada di dalam gapura).

**Dilihat (Tinggi):** halaman kampus dan taman: kerb terlihat di tepi jalan, pohon dan pagar tanaman halus, warna pekat. **Kinerja (Rendah):** Kampung Inggris 202 call / 166 rb. `tsc` dan `eslint src/game3d` bersih.

### Perombakan visual, tahap 4: bangunan kampung (2026-10-14, Opus 5.5)

- **Tiga dinding lainnya:** dulu hanya dinding depan yang berjendela; samping dan belakang polos seperti kotak dicat. `dressSides` memasang jendela berkusen dan berambang di samping dan belakang (satu baris per lantai) dan pilaster putih di keempat sudut, untuk toko, rumah/camp, balai, sekolah, puskesmas, dan gedung klasik.
- **Toko:** etalase kaca di atas kaki batu dengan tiang-tiang pembagi; kanopi sungguhan (pelat miring bergaris warna atap, lis depan, dua penyangga besi), bukan bidang datar.
- **Pohon di grafik Tinggi** lebih halus (`leafDetail` 2); Sedang 1; Rendah/Hemat 0.
- `look3d` bertambah dua gambar: `11-toko-samping`, `12-rumah`.

**Dilihat (Tinggi):** toko dari samping (kanopi bergaris, etalase bertiang, kaki batu) dan Camp Putra (jendela dua lantai, pilaster, teras). **Kinerja (Rendah):** Kampung Inggris 210 call / 168 rb, desa umum 103 / 123 rb; `parity3d` hijau; `tsc` dan `eslint src/game3d` bersih. Anggaran grafik Tinggi (450 rb segitiga) belum diukur ulang setelah pohon lebih halus.

### Pemain lain dan layar mendatar (2026-10-14, Opus 5.5)

- **Pemain lain tidak lagi meluncur atau tersendat:** dulu badan mengejar ubin tujuan dengan kecepatan tetap 2,6 m/s, berhenti di tiap ubin, dan berputar dalam satu bingkai. Kini kecepatan mengikuti jarak ketinggalan (1,6–8,5 m/s, dilunakkan), ada histeresis mulai/berhenti, dan badan berputar bertahap; ayunan kaki mengikuti kecepatan itu. **Belum dilihat bergerak** (butuh dua pemain yang berjalan; hanya `tsc`).
- **HP mendatar (640×360, emulasi sentuh, `QA_LANDSCAPE=1`):** sebelumnya menu ⚙ terpotong di atas, ⚙ dan Lemari menimpa joystick dan tombol peta, dan banner "Ketuk untuk…" menimpa status. Kini: menu ⚙ dibatasi tinggi layar dan bisa digulir; ⚙ dan 👗 pindah ke samping tombol peta; tombol aksi jadi satu baris di bawah status; banner "Ketuk untuk…" di tengah bawah, di antara tombol A dan joystick (menyentuh `Game.tsx` hanya untuk layar sentuh setinggi ≤ 480 px). Dilihat: tidak ada yang bertumpuk kecuali label nama pemain lain yang lewat di atas tombol aksi.
- **Area aman (notch):** bukan masalah saat ini: halaman tidak memakai `viewport-fit=cover`, jadi peramban sendiri menjaga isi di dalam area aman. F6 bagian ini ditutup tanpa perubahan.

**Belum dari P11-006:** tur pertama untuk kontrol 3D, dan judul "Pengaturan" terpadu (menu ⚙ kini sudah memuat grafik, suara, dan sisi joystick; tampilan pixel/3D masih di AKU).

### Tur kontrol dan anggaran grafik Tinggi (2026-10-14, Opus 5.5)

- **Tur pertama (P11-006):** tiga kartu sekali per perangkat (`kb3d-tur`): putar kamera, jalan dan lari, orang dan menu ⚙; teks berbeda untuk layar sentuh dan keyboard; "Lewati" dan "Lanjut" 44 px. Tampil 2,5 detik setelah dunia terbuka, di bawah jendela game. Dilihat di emulasi HP. Skrip uji menandainya sudah dilihat.
- **Anggaran Tinggi diukur (`QA_QUALITY=high` di `parity3d`):** setelah perombakan visual, Kampung Inggris sempat **995 rb** segitiga (batas 450 rb; angka ini termasuk lintasan bayangan). Dipangkas: daun Tinggi kembali ke detail 1 dengan 7 gumpalan, kepala bunga ikosahedron dilas (20 segitiga), kerb dan kusen samping tidak melempar bayangan, sel gabung 20 m. **Hasil: Inggris 503 call / 513 rb, Mandarin ±400 / 484 rb**: masih **di atas batas 450 rb** (sebelum perombakan: 359 rb). Rendah tetap aman (223 call / 166 rb).

**Keputusan yang perlu:** naikkan batas Tinggi ke ±550 rb (Tinggi hanya ditawarkan di layar besar, dan grafik turun sendiri bila di bawah 26 fps), atau pangkas lagi (mis. jendela samping hanya di Sedang ke atas sudah berlaku; berikutnya: jarak gambar Tinggi 150 → 120 m). Belum diputuskan; FPS Tinggi di mesin kuat belum diukur.

### Keluhan pemilik: lari, gapura, bunga, tulisan Kampung Bahasa (2026-10-14, Opus 5.5)

Keluhan: lari masih aneh dan gerak seperti robot; gapura dan bunga rumput jelek; tulisan KAMPUNG BAHASA PARE di lapangan harus berupa bunga di rumput agar tidak menutupi gapura; batas Tinggi dinaikkan ke ±550 rb (disetujui).

- **Gerak (`avatar.ts` `poseFor(..., run)`, `engine.ts`):** dulu jalan dan lari memakai pose yang sama (langkah 0,55, lutut 0,9) yang ditekuk lambat (laju 10), jadi langkah terpipihkan menjadi seretan kaku. Kini pose jalan bergantung pada `run` 0–1: langkah 0,5 → 0,85, lutut 0,85 → 1,6 saat kaki diayun, siku menekuk dan memompa, badan rendah dan condong, bahu berputar melawan pinggul, pinggul bergoyang, kepala tetap datar menghadap depan; panjang langkah lari lebih jauh (kaki tidak berputar terlalu cepat); sendi mengikuti jalan dengan laju 22. Dilihat dari samping (jalan dan lari): langkah dan kaki terangkat terlihat. Pemain lain memakai pose yang sama (P11).
- **Gapura lima kampung (`gate()` ditulis ulang):** Mandarin: paifang empat tiang di atas alas batu, balok berlis emas, deret konsol, dua atap emas berujung melengkung (balok sapu `sweptBeam`), lampion merah. Arab: dinding putih utuh dengan lengkung lancip (bentuk ekstrusi, bukan kotak + silinder), pita ubin hijau, kerangka bergerigi, kubah hijau di atas drum, bulan sabit, lampu. Inggris: pilar batu berpita dengan bola di puncak dan lampu, lengkung besi berpapan nama. Jepang: torii merah-jingga dengan kaki hitam, nuki, kasagi hitam melengkung, plakat. Korea: hongsalmun (tiang merah, deret jeruji bermata tombak, taegeuk dalam lingkaran; tanpa atap).
- **Tulisan KAMPUNG BAHASA PARE:** bukan papan tinggi lagi, tetapi taman bunga di rumput: bedeng landai (miring 0,17 rad, tepi depan di rumput, belakang ±1 m) berbingkai batu; tiap huruf disusun bunga (sampel teks di kanvas, satu bunga per 13 cm), kata-kata berwarna lima kampung dengan bunga putih acak. Gapura di belakangnya tetap terlihat. Laporan pemilik "PARE terpotong" (bedeng terlalu miring, tepi depan masuk tanah) sudah diperbaiki dan dilihat.
- **Bunga rumput:** di Sedang/Tinggi tiap bunga kini bintang lima kelopak bertangkai tipis, enam per ubin, tinggi dan miring acak (bukan permen lolipop); Rendah/Hemat tetap kepala bulat murah.
- **Anggaran Tinggi 550 rb** dicatat di `qa.md`.

**Kinerja:** Rendah: Kampung Inggris 225 call / 167 rb, desa umum 99 / 120 rb. Tinggi: Kampung Inggris 465 / 483 rb, desa umum 323 / 350 rb (di bawah 550 rb). `parity3d` hijau; `tsc` dan `eslint src` bersih.

**Belum dilihat:** gapura Mandarin dan Korea dari dekat (gambar hanya dari lapangan dan dari gapura Jepang), lari pemain lain di layar orang lain.

### Suasana malam dan karakter lebih hidup (2026-10-14, Opus 5.5)

Permintaan pemilik: taman bunga Kampung Bahasa menyala di malam hari; semua peta punya dekorasi dan suasana malam yang syahdu dengan lampu, di dalam dan di luar ruangan; karakter lebih riil dan lebih hidup.

**Malam (`start/night.ts`, baru):** lapisan malam per zona, digambar dengan titik bercahaya aditif (beberapa draw call), muncul pelan saat senja (17:15–18:40) dan hilang saat fajar, tidak digambar di siang hari.
- Pendar hangat di setiap lampu jalan; untaian bola lampu warna-warni yang menjuntai di antara tiang lampu berjarak 6–16 m, dengan kabelnya.
- Kunang-kunang (70) di atas rumput dan pepohonan di sekitar pemain, masing-masing berkedip sendiri (tidak di Hemat).
- Langit: 900 bintang dan bulan dengan pendarnya.
- Taman bunga KAMPUNG BAHASA PARE: tiap bunga menyala dalam warnanya sendiri.
- Kamar camp: untaian lampu di sepanjang atas dinding; jendela berubah dari biru langit ke biru malam (`nightTint`).
- Jendela bangunan dan lampu jalan yang sudah menyala tetap seperti sebelumnya.

**Karakter (`avatar.ts`):**
- Mata berkedip (kadang dua kali), iris berwarna cokelat yang dipilih dari nama (tetap per orang), pupil, dua kilau, garis bulu mata; hidung kecil; kulit sedikit hangat dari dalam (tidak seperti plastik).
- Proporsi gaya Kartun sedikit lebih jenjang: kepala lebih kecil, kaki dan lengan lebih panjang.
- Berdiri tidak pernah diam: berat badan berpindah dari satu kaki ke kaki lain, napas, kepala melihat ke sekeliling.
- Orang yang berdiri dalam 6 m dari pemain menoleh ke arah pemain (sebatas lirikan, tidak memutar penuh).

**Dilihat:** taman bunga menyala di malam hari, kampus malam (pendar lampu, kunang-kunang, bintang), kamar malam (untaian lampu, jendela gelap), karakter dari depan (mata, hidung, proporsi), Miss Kate menoleh ke pemain. **Kinerja (Rendah):** Kampung Inggris 230 call / 168 rb, desa umum 105 / 121 rb; `parity3d` hijau; `tsc` dan `eslint src` bersih.

**Batas yang jujur:** karakter masih dibangun dari bentuk dasar (bola, kapsul) di dalam kode. "Riil" sesungguhnya (badan satu permukaan mulus, wajah berotot, jari, rambut berhelai, pakaian berlipat) butuh model 3D buatan seniman (glTF ber-rig) yang dimuat game; itu keputusan anggaran dan arah seni, bukan lagi soal kode.

### Karakter KayKit Adventurers (2026-10-14, Opus 5.5)

Pemilik sempat meminta karakter seperti The Sims (model The Sims milik EA, tidak boleh dipakai). Percobaan dengan Quaternius Universal Base Characters dihentikan pemilik ("aku mau pakai karakter lucu aja"). **Keputusan pemilik:** badan dasar dari **KayKit Adventurers 2.0 FREE** (Kay Lousberg, CC0); pakaian dan aksesori disesuaikan dengan Lemari kita. **Keputusan kedua (hari yang sama):** tidak ada ikon perang dan tidak ada aksesori atau baju bernuansa fantasi; yang dipakai baju dan aksesori yang umum di Indonesia dan di kalangan pelajar, ditambah pilihan wajah imut untuk anak dan remaja. Senjata, helm, perisai, tabung panah, tongkat, topi penyihir, dan topi beruang dari pack **tidak dipakai** (berkas prop dan Barbarian dihapus).

**Dibuat (`src/game3d/human.ts`, aset di `public/models/kaykit/`: Rogue, Rogue_Hooded, Mage, Ranger, Knight, dua berkas animasi, `LICENSE.txt`):**
- **Satu orang = satu mesh = satu draw call,** dengan satu atlas 512×256 per kombinasi warna: separuh kiri swatch Rogue (kepala, kaki, tunik Rogue), separuh kanan swatch milik potongan baju yang dipinjam.
- **Potongan baju menurut atasan:** kaos dan daster memakai tunik Rogue; kemeja, batik, seragam sekolah, dan pramuka memakai tunik Ranger (selendangnya menjadi kerah, atau hasduk merah untuk pramuka); koko, almamater, kebaya, dan gamis memakai jas berkancing Mage; hoodie memakai badan berkerudung.
- **Nuansa fantasi dihapus:** bantalan bahu, tali kulit, sabuk, gesper, dan kantong dicat dengan nada warna baju; pelindung lengan Rogue dipindah ke swatch sendiri (kulit untuk lengan pendek, kain untuk lengan panjang); pisau dan logam di lengan dilipat hilang; sarung tangan menjadi tangan; kumis dan janggut kepala Ranger dihapus; kepala Barbarian (berjanggut) tidak dipakai.
- **Wajah imut (pilihan `eyes` di Lemari):** Bulat berkilau (mata ×1,3 dengan kilau), Berbinar (×1,45, dua kilau, pipi merona), Bulu mata lentik, Tersenyum (mata ^^ dan pipi merona), Kedip (satu mata ^), dan Kalem (wajah asli pack). Alis ditipiskan, kecuali pada Kalem. Mata diperbesar langsung pada geometri kepala; kilau, rona, bulu mata, dan lengkung mata digambar tanpa cahaya di tulang kepala.
- **Badan:** tinggi, besar badan (build), dan lebar bahu dari Lemari mengubah geometri (disimpan per ukuran); rok mengikuti lebar badan.
- **Rok:** rok panjang, sarung, jarik, dan gamis menggantung sampai tanah tanpa kaki di dalamnya; daster dan rok sekolah selutut memperlihatkan kaki. Kain berayun saat berjalan dan terlipat saat duduk.
- **Barang baru di Lemari:** Kemeja seragam sekolah, Seragam pramuka (selalu khaki, hasduk merah), Rok sekolah selutut, Dasi sekolah (warna mengikuti bawahan, seperti seragam SD/SMP/SMA), Pita rambut, Bando, Botol minum, dan Pipi merona. Kartu peserta, kacamata, jam, headphone, ransel, selempang, dan tote kini tergambar pada karakter KayKit (sebelumnya hilang). Peci, topi, blangkon, dan caping tetap ada.
- Barang milik satu orang (rok, peci, tas, kartu) dibebaskan dari memori saat orang itu diganti (`disposeAvatar`).

**Dilihat:** `look3d` 02b–02m: gamis + jilbab, rok berjalan, enam atasan, badan ramping/besar, tas dan aksesori, dan enam gaya pelajar (SD dengan rok merah, dasi, pita, ransel; SMP; SMA berjilbab; pramuka dengan wajah kedip; santai dengan hoodie, bando, headphone; Kalem dengan batik dan kacamata). **Kinerja:** Tinggi: Kampung Inggris 351 call / 530 rb, desa umum 229 / 409 rb, kota 96 / 263 rb (di bawah 550 rb); Rendah: Kampung Inggris 215 / 204 rb, kota 30 / 144 rb. `parity3d` hijau; `tsc` dan `eslint` bersih; tes backend `internal/pare` lolos dengan `wardrobe.json` baru (56 barang).

**Belum:**
1. ~~Deploy backend untuk `wardrobe.json` baru~~: **sudah di-deploy 2026-10-14 14:59 WIB** (tanpa migrasi; backup DB `titian_pre_wardrobe_kaykit_20261014T075744Z.sql.gz`; `:prev` = image 06:40 WIB). Tinggal push `game`.
2. Motif kain (batik kawung, kebaya) masih warna polos.
3. Ujung tunik Ranger (seragam, kemeja) bergerigi bawaan pack; belum ada versi baju dimasukkan.
4. Harga barang baru masih contoh (sebagian besar gratis; botol Rp3.000, Berbinar Rp3.000, Kedip Rp4.000), menunggu keputusan pemilik.

### Audit Lemari: setiap barang terlihat dan sesuai namanya (2026-10-14, Opus 5.5)

Pemilik meminta semua isi Lemari benar-benar bisa dipakai dan tampak sesuai namanya. **Alat uji baru:** `scripts/qa/lemari3d.ts` memakaikan setiap barang di setiap slot (dan setiap wajah) di atas satu look tetap, memotret, lalu membandingkannya dengan barang lain di slot yang sama. Barang yang tidak mengubah apa pun dianggap gagal. Hasilnya berupa lembar kontak per slot (`/tmp/pare-video/lemari/lembar-*.jpg`) untuk dicek mata. **Hasil: 57/57 lolos.**

**Yang diperbaiki:**
- **Bug nama tulang:** GLTFLoader membuang titik dari nama tulang ("foot.l" menjadi "footl"). Akibatnya pegangan tangan, tekukan kaki saat duduk, lengan saat joget, jam tangan, dan semua yang menempel di kaki diam-diam tidak jalan. Sekarang kedua nama dikenali. Barang di tangan (buku, telepon) ditaruh di wadah yang membatalkan skala model, sehingga tampil seukuran tangan.
- **Rambut** sesuai namanya: pendek (kepala Knight), belah pinggir (Ranger, tanpa kumis), panjang (Mage), ikal (Rogue + ikal di ujung), kuncir kuda (Knight + kuncir dan ikat rambut), cepol (Knight + sanggul). Tidak lagi ditentukan oleh jenis kelamin.
- **Penutup kepala:** peci, topi (dengan pinggiran depan), blangkon (bermotif batik + mondolan), dan caping dibuat ulang agar pas di kepala KayKit; bergo diberi pinggiran depan, pashmina diberi juntaian di dada.
- **Atasan:** batik bermotif kawung dan kebaya bermotif renda (keduanya digambar shader dari posisi badan) + bros di kebaya; almamater berlambang; seragam putih berkerah dengan saku dan OSIS; koko berkerah tegak; kemeja berkerah lipat; pramuka khaki dengan hasduk.
- **Bawahan dan kaki:** betis punya swatch sendiri, jadi celana panjang menutup betis, sedangkan celana pendek dan rok selutut memperlihatkan kaki. Jeans diberi lipatan ujung, rok sekolah berlipit, sarung kotak-kotak, jarik batik parang, daster bermotif bunga (di baju dan rok).
- **Alas kaki:** sneakers (sol putih), sandal jepit (kaki telanjang, sol, tali V), pantofel (sol tipis, hak), sepatu lari (sol oranye, strip putih).
- **Detail menurut jarak:** sol, kartu, jam, lipatan jeans, serta kilau dan rona wajah disembunyikan pada orang yang lebih dari 14 m dari kamera (`humanDetail`). Tinggi: Kampung Inggris 294 call / 436 rb (sebelumnya 413 / 558 rb, melewati batas), desa umum 256 / 403 rb, kota 128 / 261 rb; Rendah: Kampung Inggris 218 / 186 rb, kota 33 / 132 rb.

Gerak yang dicek: duduk (kaki menekuk ke depan, rok terlipat), joget (goyangan dikurangi supaya tidak tampak jatuh), memegang buku dan telepon. Katalog tidak berubah (56 barang), jadi tidak perlu deploy backend.


### Karakter siap pakai di Lemari (2026-10-14, Opus 5.5)

Pemilik: tab Tubuh hanya berisi pengaturan; seharusnya ada pilihan karakter siap pakai yang beragam, khas Indonesia, dan sesuai pengguna Titian. **Dibuat:** tab **Karakter** (tab pertama, terbuka saat Lemari dibuka) dengan 15 karakter (`PRESETS` di `src/game3d/catalog.ts`):
- **Pelajar:** Dimas (siswa SD), Putri (siswi SD), Bagas (siswa SMP), Aisyah (siswi SMP berjilbab), Rizky (siswa SMA), Nadia (siswi SMA), Bayu (anggota pramuka), Ahmad (santri).
- **Kuliah dan kerja:** Sinta (mahasiswi), Raka (mahasiswa), Fajar (pekerja muda).
- **Orang tua dan guru:** Bu Ratna (guru), Pak Budi (bapak yang ikut belajar).
- **Anak dan remaja:** Ucok (anak main di kampung), Kezia (remaja santai).

Warna kulit, tinggi, badan, wajah, dan jilbab beragam.
- Satu ketukan memakaikan seluruh look (masih bisa diubah di tab lain).
- Kartu menunjukkan gambar mini, nama, keterangan, dan apa yang masih dibutuhkan: "Siap pakai", harga uang game, Toko, atau Plus/Pro. Barang berbayar dibeli lewat alur yang sudah ada sebelum bisa disimpan.
- Gambar mini dirender dari model asli dengan renderer kecil sementara (`portraits()` di `human.ts`), dibingkai menurut kotak pembatas tiap karakter, lalu disimpan di memori.

`lemari3d.ts` kini juga memeriksa slot karakter: 15/15 berbeda. Dicek di desktop (1280×800) dan HP (portrait). Tidak ada perubahan backend.

### URL, onboarding 3D, dan performa (2026-10-14, Opus 5.5)

**URL (pemilik):** `/play` kini game 3D, pixel art pindah ke `/play-pixel`, dan `/start` dialihkan ke `/play` (next.config). Pilihan pemain tetap dihormati (`engineRedirect` di `lib/engine-pref.ts`): pilihan pixel yang membuka `/play` dialihkan ke `/play-pixel`, pilihan 3D yang membuka `/play-pixel` dialihkan ke `/play`, dan `?px=1` berarti tetap di halaman itu. Perangkat tanpa WebGL dialihkan ke `/play-pixel?px=1`. Skrip uji sudah disesuaikan.

**Onboarding 3D:** langkah 3 di `/play` berisi karakter siap pakai 3D sesuai gender langkah 2 (`Preset3DPicker`), dalam versi gratisnya (`freeLook`: barang berbayar diganti padanan gratis), dengan gambar dari model asli. Look 3D disimpan begitu akun dibuat (`PUT /pare/me/look3d`, termasuk `gender`), dan look pixel diturunkan darinya. Kartu "Tur hari pertama" tidak lagi bertumpuk dengan tur kontrol 3D (engine menunggu kartu bertanda `data-tour-card` ditutup). Teks letak joystick mengikuti setelan sisi. Ditambah tiga karakter perempuan (Mei, Rara, Wulan): 9 + 9.
- **Uji:** `scripts/e2e/onboard3d.ts` (akun baru dibuat dan dihapus) **lulus** di build produksi lokal, HP (perempuan) dan desktop (laki-laki).

**Performa (diukur di Intel HD Graphics 4000, setara HP murah):**
- Zona dibangun bertahap (`pump` di `zone.ts`): petak tempat pemain berdiri langsung jadi, sisanya dicicil 4–6 ms per bingkai dari yang terdekat. Penggabungan geometri dipecah per material. Petak baru masuk scene setelah shader-nya dikompilasi (`compileAsync`). Masuk zona: 1,6–3,2 dtk beku → 0,4–1 dtk.
- Bayangan digambar ulang tiap 2 bingkai (Tinggi) atau 3 bingkai (Sedang), bukan tiap bingkai. Orang di atas 20/35 m dianimasikan tiap 2/4 bingkai, dan yang di belakang kamera tiap 6 bingkai. `checkShaderErrors` mati di produksi. Kampung Inggris Tinggi 11 → 17 fps, Rendah 21 → 25 fps; Hemat 41–45 fps. Penurunan grafik otomatis (FPS < 26 selama 8 dtk) membawa perangkat seperti ini ke Hemat.
- Model karakter dan alam mulai diunduh begitu `/play` dibuka (saat login/onboarding). Service worker menyimpan `/models/*` (stale-while-revalidate), dan `Cache-Control` untuk `/models` ditambahkan di next.config.
- Dicoba lalu dibatalkan: penggabungan per petak 60 m. Draw call turun, tapi segitiga naik dan FPS turun di GPU lemah.
- Uji akses engine di build produksi: hanya bila `localStorage["kb3d-qa"]="1"`.

**Uji di build produksi lokal (`next build` + `next start`):**
- onboarding HP/desktop lulus;
- `parity3d` 13 zona hijau (Rendah ≤ 269 call / 192 rb);
- pengalihan `/play` ↔ `/play-pixel` ↔ `/start` benar (5/5);
- tanpa error halaman.

**Deploy backend 2026-10-14 19:15 WIB:** kolom `gender`, Pro membuka semua barang, dan teks keuntungan Pro (tanpa migrasi; backup `titian_pre_gender_pro_20261014T121344Z.sql.gz`). Suara jangkrik malam dihapus (pemain merasa terganggu). Semua pemain lama dipindah ke 3D (228 baris, kini 231 pemain di 3D). **Belum:** push `game`.
