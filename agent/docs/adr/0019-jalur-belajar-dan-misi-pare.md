# ADR-0019: Jalur belajar & misi dunia terbuka di Kampung Bahasa Pare

Status: **Accepted** (2026-10-04; keputusan di §15). Pelaksanaan: `tickets/pare-9-jalur-misi.md`.
Date: 2026-10-04 (revisi kedua pada hari yang sama)
Supersedes: -
Superseded by: -
Related: ADR-0016 (Kampung Bahasa Pare, §3 penilaian di server, §4 simulasi hidup, §5 hub realtime), ADR-0017 (suara), ADR-0018 (iklan & premium), `pare-benchmark-level.md` (kontrak isi per level), skenario lengkap `pare-perjalanan/`, tiket `tickets/pare-9-jalur-misi.md`

**Yang berubah di revisi kedua.** (1) Misi dirinci dari sisi pemain: cara menyelesaikan, cara dinilai, tempat melihat kemajuan, syarat lulus bab dan naik level (§16). (2) Skenario bahasa Inggris ditulis penuh dari Basic sampai C2, termasuk silabus B2–C2 yang isinya belum ada (§9 dan folder `pare-perjalanan/`). (3) Rancangan memperhitungkan bahwa game ini multipemain dan berjalan di waktu nyata (§17). (4) Angka di §2, §8, §10, §14 disesuaikan dengan skenario itu. Contoh pemetaan bab → misi di revisi pertama dihapus karena sudah digantikan skenario lengkap.

> **Catatan migrasi (2026-10-05, ADR-0020):** backend sedang dipindah dari Rust ke Go. Keputusan di ADR ini tidak berubah; setiap "Rust" / `titian-backend-rust` / `services/pare_*.rs` di bawah berpadanan dengan `titian-backend-go/internal/pare/` setelah tiket G14. Sampai G14 selesai, kode Pare yang aktif tetap yang Rust.

## Context

Pare adalah pembelajaran berbasis game, tetapi bagian belajarnya sekarang belum berjalan seperti game:

- **Tidak ada urutan.** Kelas punya enam tombol sejajar (Kosakata, Tata Bahasa, Pelafalan, Rutinitas, Makanan, Perjalanan). Pemain baru tidak tahu harus mulai dari mana atau apa berikutnya.
- **Tidak ada pengajaran.** Satu kelas = 6 soal acak (`class_lesson`). Kata dipilih acak dari kategori, jadi pemain sering ditanya kata yang belum pernah dilihat. Konsep tata bahasa hanya dijelaskan di Kamus, bukan di kelas.
- **Materi dan latihan tidak dibedakan**, dan setiap jawaban salah memotong 5 XP, termasuk untuk hal yang baru pertama kali dilihat.
- **Dunia dan pelajaran terpisah.** Warung, pasar, laundry, klinik, taman, jam WIB, dan cuaca nyata sudah ada, tetapi tidak dipakai untuk mempraktikkan bahasa. Misi yang ada hanya tiga Misi Harian generik ("makan 3×", "ikut 1 kelas").

Yang diminta user (2026-10-04):

1. Pembelajaran **berurutan**, dengan pemisahan jelas antara materi/konsep dan latihan/praktik, bertahap supaya pemain tidak terus-menerus salah lalu jenuh.
2. **Misi seperti kehidupan nyata** yang terikat pada apa yang dipelajari. Contoh dari user: bab *simple present* → misi menjalani kegiatan rutin; *reported speech* → mencari berita lalu melaporkannya. Misi bisa per bab, per topik, atau per level.
3. **Dunia yang berkembang**: wilayah, bangunan, dan aktivitas baru (termasuk yang interaktif atau berupa komputer) terbuka lewat misi, dan tingkat tantangan naik tiap level.
4. **Misi yang jelas bagi pemain**: ia tahu cara menyelesaikannya, tahu ukuran penilaiannya, punya tempat untuk melihat kemajuannya, dan tahu apa saja yang harus dikerjakan untuk menamatkan satu bab atau satu level, sehingga tahu apa yang harus disiapkan.
5. **Skenario perjalanan hidup yang lengkap** dari Basic sampai C2 untuk bahasa Inggris (apa yang dipelajari, misi wajib, misi per level, misi per warga di tiap level), yang nanti diterapkan ke bahasa lain menurut budaya dan cara belajar yang efektif untuk bahasa itu.
6. **Multipemain dan waktu nyata** harus diperhitungkan: satu warga bisa diwawancarai banyak siswa pada saat yang sama, kelas bisa diikuti banyak siswa, dan sifat multipemain itu sebaiknya dimanfaatkan sebagai variasi permainan.

Yang sudah ada dan dipakai ulang (sudah dicek di kode):

- Mesin soal otoritatif di server (`pare_paper.rs`, `pare_lesson.rs`): pilihan ganda, susun kalimat, ketik, ucap, dan menulis terbimbing yang dinilai AI dengan empat kriteria (`pare_compose.rs`; kalau AI tidak tersedia, tulisan tetap dicek dengan aturan).
- Kemajuan per kata (`pare_words`), buku besar hadiah (`pare_ledger`), dan aliran kejadian harian (`pare_daily::bump`: makan, beli, kunjungan, chat, kelas, tantangan).
- Endpoint kehidupan (beli, laundry, sewa sepeda, tidur, bangun), jam WIB dan cuaca nyata Pare, aturan bahasa chat (`pare_langrule`).
- Hub realtime (`pare_hub.rs`): tiap zona dibagi menjadi kanal berisi paling banyak 50 pemain; satu koneksi per pemain; chat seluruh kanal, sekitar, dan pribadi atau grup (paling banyak 5 orang lain) yang sampai ke anggotanya di zona mana pun; voice note dan panggilan langsung. State hub ada di satu proses (pembagian lintas instance lewat Redis ditunda).
- Dialog NPC adalah jendela di klien, dan soalnya adalah kertas per pemain di server. Artinya percakapan dengan NPC sudah bersifat pribadi: NPC tidak pernah "terpakai" oleh satu pemain.
- Tanda "!" di atas NPC, titik emas di minimap, gelar di papan nama, lemari pakaian.
- Konten per level yang lolos benchmark untuk Basic sampai B1-setara di lima bahasa; kontrak B2 ke atas di `benchmark-plan.ts`.
- Audio rekaman per teks (pipeline `game/scripts/audio`).

## Decision

### 1. Prinsip: ajarkan dulu, latih bertahap, lalu pakai di dunia

Jawaban untuk "materi dulu atau dicampur?": **berurutan di dalam satu pelajaran, bercampur antar pelajaran, dan ditutup dengan tugas nyata.**

| Prinsip | Wujudnya di game |
|---|---|
| Presentasi → latihan → produksi ("saya contohkan, kita kerjakan, kamu kerjakan") | Tiap pelajaran: Materi → Latihan. Tiap bab: Praktik → Cek → Misi |
| Belajar berbasis tugas dan *can-do* CEFR | Misi = tugas dengan hasil nyata ("memesan makan siang"), bukan soal |
| Paparan pertama tanpa salah | Kata dan konsep baru selalu muncul dulu sebagai kartu Materi, baru kemudian sebagai soal |
| Bantuan yang dikurangi sedikit demi sedikit | Mengenali → memilih → menyusun → mengetik → menulis dan berbicara bebas |
| Mengingat ulang berjarak | Tiap Latihan menyisipkan 2 butir dari pelajaran lama; misi warga dan kelas bersama memakai materi lama |
| Tantangan pas | Sasaran tingkat benar 80–90% per sesi; di bawah 60% game menurunkan beban, di atas 95% menawarkan loncat |

Angka 80–90% adalah patokan praktis, bukan hasil ukur di game ini. Ia harus dikalibrasi dari data pemain (§13.6).

### 2. Susunan kurikulum

```
Level (Basic, A1, A2, B1, B2, C1, C2)  =  satu tahap hidup (§9)
└─ Bab (satu tema, mis. "Makan bersama")
   ├─ Pembukaan bab: peta bab + kartu misi bab (pemain tahu sejak awal apa tujuannya)
   ├─ Pelajaran 1…n   → 📖 Materi → 🧩 Latihan
   ├─ 🎯 Praktik bab  → situasi, dialog, bacaan, menulis terbimbing; disisipkan tiap 2–3 pelajaran
   ├─ 🏁 Cek bab      → lulus ≥ 80% (boleh diulang)
   └─ ⭐ Misi bab     → dikerjakan di dunia game
├─ Misi warga         → 10 per level, pilih beberapa
└─ 🏆 Misi Besar level → membuka wilayah baru + naik level
```

- Pemain selalu punya **satu langkah berikutnya** yang jelas: tombol "Lanjut" di kelas, pelacak di HUD, dan tanda di atas NPC.
- **Bab ditulis eksplisit** per bahasa dan level: tiap konsep silabus masuk tepat satu bab, dan anggaran kata per bab habis terbagi. Untuk bahasa Inggris ini sudah ditulis dan diperiksa mesin (§9).
- Ukuran bahasa Inggris:

| | Basic | A1 | A2 | B1 | B2 | C1 | C2 |
|---|---|---|---|---|---|---|---|
| Bab | 5 | 14 | 14 | 14 | 12 | 12 | 10 |
| Kata baru | 60 | 561 | 1.005 | 1.399 | 2.000 | 3.000 | 2.000 |
| Konsep tata bahasa | 6 | 27 | 31 | 28 | 28 | 24 | 20 |
| Kata per pelajaran | 6 | 6 | 8 | 10 | 12 | 15 | 15 |
| Pelajaran (±) | 18 | 128 | 162 | 169 | 196 | 228 | 160 |

- **Bentuk Materi berubah menurut level.** Basic–A1: kartu gambar (kata, arti, audio). A2–B1: kartu kata dengan kalimat contoh dan kolokasi. B2 ke atas: satu paket kata dipelajari dari satu teks pendek atau rekaman (keluarga kata, kolokasi, ragam), karena di level itu kata tidak lagi efektif dipelajari satu per satu.
- Praktik ditaruh **per bab** dan disisipkan di antara pelajaran, karena jumlah situasi, dialog, dan bacaan memang seukuran bab.

### 3. Tahap pelajaran dan aturan hadiah

| Tahap | Isi | Salah | Hadiah |
|---|---|---|---|
| 📖 Materi | Kartu kata atau satu konsep dengan pola, kapan dipakai, contoh, dan kesalahan umum | Tidak ada soal | Membuka Latihan |
| 🧩 Latihan | Hanya isi Materi itu + 2 ulangan lama. Urutan: kenali → dengar → susun → ketik. Petunjuk 💡 gratis | Tidak memotong XP. Butir yang salah muncul lagi sebelum sesi selesai | XP + uang, sekali per pelajaran |
| 🎯 Praktik | Situasi, dialog (didengar), bacaan, menulis terbimbing. Terjemahan bisa dibuka | Tidak memotong XP | XP + uang, sekali |
| 🏁 Cek bab | Campuran seluruh bab. Lulus ≥ 80% | Tidak memotong XP; gagal menunjukkan pelajaran yang perlu diulang | XP + membuka Misi bab |
| ⭐ Misi bab | Tugas di dunia (§5–§8, §16) | Tidak memotong XP; mengurangi skor misi | Hadiah besar, stempel, pembukaan |

- **Di jalur belajar, XP tidak pernah berkurang.** Taruhannya adalah gerbang 80% dan bintang, bukan denda. Potongan XP untuk jawaban salah tetap berlaku di aktivitas kompetitif (Language Challenge) saja.
- **Hadiah hanya pada penyelesaian pertama** tiap simpul. Mengulang selalu boleh, tanpa hadiah, supaya XP tidak bisa diternak.
- Nyawa tidak tersentuh oleh belajar (sekarang pun nyawa hanya berkurang karena pelanggaran aturan bahasa).

### 4. Aturan anti-jenuh

1. Kata atau konsep baru tidak pernah menjadi soal sebelum Materinya dibuka.
2. Sesi pendek: Materi ± 2 menit, Latihan ± 4 menit di level awal; satu pelajaran paling lama ± 10 menit di C1–C2.
3. Salah → penjelasan singkat langsung, lalu butir itu diulang di sesi yang sama, sehingga sesi berakhir dengan benar.
4. Dua kali salah pada butir yang sama → kartu Materinya ditampilkan lagi.
5. Latihan di bawah 60% → tawarkan ulang Materi dan varian soal yang lebih mudah, tanpa label "gagal".
6. Selang-seling: setelah 2–3 pelajaran selalu ada Praktik, Cek, atau Misi.
7. **Tes loncat bab**: pemain yang sudah bisa boleh langsung Cek bab; lulus ≥ 90% menandai semua pelajaran bab itu selesai.
8. Target harian kecil (1 pelajaran + 1 langkah misi) lewat Misi Harian yang sudah ada.
9. Misi tidak punya keadaan "gagal" (§16.3), dan tidak pernah menunggu pemain lain (§17.1).

### 5. Tiga tingkat misi

| Tingkat | Kapan | Ukuran | Wajib? | Hasil |
|---|---|---|---|---|
| **Misi bab** | Setelah Cek bab lulus | 5–7 langkah; 6–8 menit di Basic sampai 30–40 menit di C2 | Ya | Stempel, hadiah, bab berikutnya terbuka |
| **Misi warga** | Kapan saja, dari sepuluh warga inti; satu per warga per level | 2–4 langkah | Pilih 3 dari 10 per level (Basic: 2) | Uang, kosmetik, keakraban dengan warga itu; memakai materi lama |
| **Misi Besar** | Setelah semua bab satu level | 3 babak, 9–10 langkah, menggabungkan semua bab; 15 menit di Basic sampai 75 menit di C2 | Ya | Wilayah baru, naik level, gelar |

Misi Harian (Balai Desa) tetap ada sebagai kebiasaan harian. Jumlah untuk bahasa Inggris: 81 misi bab + 70 misi warga + 7 Misi Besar = **158 misi**.

Sepuluh warga inti (Miss Kate, Tom, Chef Oliver, Mrs. Brown, Mr. Green, Mrs. Hughes, Mr. Smith, Prof. Grey, Lily, Officer Jones) menemani pemain dari Basic sampai C2: cerita tiap warga berkembang bersama kemampuan pemain (Tom: mengantar teh → membuka cabang → rencana bisnis → memoar). Tabel alur tiap warga ada di `pare-perjalanan/en-ringkasan.md`.

### 6. Mesin misi: langkah yang diverifikasi server

Misi = daftar langkah berurutan. Status misi disimpan di server; klien hanya menampilkan. Ada lima belas jenis langkah:

| Jenis langkah | Contoh | Verifikasi |
|---|---|---|
| `pergi` | Pergi ke kafe | Zona dan posisi pemain di hub realtime |
| `bicara` | Temui Tom | Interaksi NPC (endpoint baru) |
| `dialog` | NPC berbicara, pemain membalas dengan memilih, menyusun, mengetik, atau (kalau peramban mendukung) mengucapkan | Mesin soal yang ada; satu giliran = satu butir |
| `beli` / `lakukan` | Beli teh; makan; menata benda; mengganti pakaian | Endpoint kehidupan yang ada, atau interaksi objek |
| `waktu` | Datang pada jam janji | Jam server (WIB), selalu jendela relatif (§17.1) |
| `temukan` / `baca` | Cari kunci; baca papan pengumuman; cocokkan informasi | Interaksi objek; butir pemahaman |
| `dengar` | Dengar pengumuman, lalu bertindak | Klip audio + butir pemahaman |
| `telepon` | Panggilan tiruan: hanya suara, transkrip tertutup secara default | Klip audio + butir; membuka transkrip mengurangi skor Mandiri |
| `komputer(aplikasi)` | Isi formulir, pesan tiket, susun rekaman, sunting naskah | Aturan (isi dan urutan yang benar) |
| `tulis` / `tulis(aplikasi)` | Email, berita, ulasan, laporan | Aturan + rubrik AI (§16.3) |
| `presentasi` | Paparan, pidato, laporan langsung | Naskah yang diketik dinilai dengan rubrik; membacakannya sebagai voice note bersifat pilihan |
| `ucap` | Ucapkan kalimat tetap | Pengenal suara peramban (hanya Chrome); selalu ada jalur ketik. Hanya dipakai di misi warga |
| `sosial` | Rapat, debat, wawancara, juru bahasa | Sesi dengan pemain lain atau NPC pengganti (§17) |

Tidak ada keadaan "gagal": balasan salah membuat NPC bereaksi dan memberi petunjuk, langkah bisa diulang, dan yang berkurang hanya skor. Misi bisa ditinggal dan dilanjutkan dari langkah terakhir, di perangkat mana pun.

### 7. Pola misi, supaya bisa dibuat banyak

Misi dibuat dari **pola** yang diisi konten bab. Sembilan belas pola dipakai di skenario bahasa Inggris (angka = jumlah misi bab yang memakainya):

| Pola | Mekanik | Dipakai |
|---|---|---|
| Kenalan / wawancara | Tanyai orang, isi formulir atau tabel | 7 |
| Reporter | Kumpulkan pernyataan, lalu laporkan | 7 |
| Juru tulis | Email, formulir, petisi, brief | 6 |
| Kritikus | Mengulas dan membela penilaian | 6 |
| Balai desa | Sampaikan dan bela pendapat; debat | 6 |
| Perencana | Susun rencana dengan batasan | 5 |
| Penolong | Beri saran, tengahi | 5 |
| Peneliti | Cari sumber, timbang bukti, tulis | 5 |
| Belanja | Daftar, harga, kembalian, anggaran | 4 |
| Pemandu arah | Antar atau arahkan orang | 4 |
| Detektif | Kumpulkan petunjuk, simpulkan | 4 |
| Pesan & layani | Memesan; lalu tukar peran menjadi pelayan | 3 |
| Rutinitas | Jalani kegiatan di game, lalu ceritakan | 3 |
| Pengamat | Lihat adegan, lalu deskripsikan | 3 |
| Dengar & catat | Pengumuman, telepon, kuliah | 3 |
| Negosiator | Berunding dengan lembar posisi rahasia | 3 |
| Pembicara | Presentasi, pidato, konferensi pers | 3 |
| Penyunting | Memperbaiki naskah sendiri atau orang lain | 3 |
| Penerjemah | Menerjemahkan dan menjadi juru bahasa | 1 |

Pola "Rutinitas" dan "Pengamat" memanfaatkan sesuatu yang hanya dimiliki game ini: server mencatat kegiatan, pakaian, dan cuaca yang sebenarnya, sehingga misi bisa meminta kalimat tentang hari si pemain sendiri, pakaian avatar yang sedang dipakainya, atau cuaca Pare saat itu.

### 8. Tangga kesulitan

Jumlah langkah tetap 5–7 di semua level. Yang naik adalah bobot tiap langkah:

| | Basic | A1 | A2 | B1 | B2 | C1 | C2 |
|---|---|---|---|---|---|---|---|
| Lama misi bab | 6–8 mnt | 7–10 | 10–12 | 12–18 | 15–25 | 25–35 | 30–40 |
| Instruksi | Indonesia | Dwibahasa | Inggris + tombol terjemah | Inggris | Inggris | Inggris | Inggris |
| Cara menjawab | Pilih, susun | Susun, ketik kalimat | Ketik kalimat | Ketik bebas | Ketik bebas | Ketik bebas | Ketik bebas |
| Tulisan per misi | — | 25–50 kata | 60–100 | 100–150 | 150–250 | 250–350 | 350–500 |
| Sumber informasi | Diberikan | Diberikan | Dicari di 1–2 tempat | Dikumpulkan dari beberapa orang | Beberapa teks + data | Pangkalan data, arsip | Teks sastra, hukum, ilmiah |
| Penanda di peta | Titik tujuan persis | Titik tujuan | Hanya zona | Petunjuk dari NPC | Tidak ada | Tidak ada | Tidak ada |
| Penilaian | Aturan | Aturan + rubrik untuk tulisan | Aturan + rubrik | Rubrik + aturan struktur | Rubrik | Rubrik (ragam, kohesi) | Rubrik (gaya, dampak) |
| Bintang ketiga | Skor | Skor | Skor + tantangan | Skor + tantangan | Skor + tantangan | Skor + tantangan | Skor + tantangan |
| Peran pemain lain | Berkenalan | Tukar peran sederhana | Info-gap, cerita berantai | Tim redaksi, rapat | Debat, panel | Telaah sejawat, negosiasi | Sidang, juru bahasa, mentor |

"Border" pada permintaan user saya artikan sebagai gerbang wilayah (§10). Kalau maksudnya lain, bagian ini perlu disesuaikan.

### 9. Perjalanan hidup: tujuh tahap

Tiap level adalah satu tahap hidup seseorang yang datang ke Kampung Inggris tanpa bisa apa-apa dan berakhir sebagai penulis, juru bahasa, dan mentor.

| Level | Tahap hidup | Di mana | Yang dialami | Misi Besar | Membuka |
|---|---|---|---|---|---|
| Basic | Pendatang baru | Kampung Inggris | Minggu pertama: menyapa, menghitung, memesan, tidak tersesat | Minggu pertamaku di Kampung | Permukiman |
| A1 | Menjadi warga | Permukiman | Tinggal di rumah keluarga Brown; sekolah, pasar, janji, cuaca | Pesta kampung | Pusat kota |
| A2 | Merantau ke kota | Pusat kota | Kerja paruh waktu, klinik, tiket, liburan pertama | Gaji pertama, liburan pertama | Distrik media & kampus |
| B1 | Magang jadi reporter | Distrik media & kampus | Kampung Post, radio, rapat warga | Edisi khusus Kampung Post | London (beasiswa) |
| B2 | Mahasiswa pertukaran | London, kawasan mahasiswa | Flat bersama, kuliah, magang, klub debat | Konferensi Mahasiswa Internasional | London, City & Westminster |
| C1 | Profesional & peneliti | London, City & Westminster | Analis di lembaga kebijakan; riset, negosiasi, konferensi pers | Proyek unggulan | London, South Bank |
| C2 | Duta & mentor | South Bank, lalu Pare | Penulis, kritikus, juru bahasa; pulang membimbing pendatang baru | Karya besar & pulang kampung | Balai Mentor (kegiatan setelah tamat) |

Skenario lengkapnya, satu halaman per level, ada di `agent/docs/pare-perjalanan/`:

- `README.md` — cara membaca dan indeks.
- `en-0-basic.md` … `en-6-c2.md` — per level: yang perlu disiapkan, syarat naik level, dunia yang terbuka, peta bab, lalu tiap bab (yang dipelajari + misi bab langkah demi langkah), Misi Besar, sepuluh misi warga, dan acara dunia.
- `en-ringkasan.md` — angka, alur tiap warga, dan daftar kebutuhan pembangunan (tokoh, tempat, aplikasi komputer, jenis langkah, isi yang belum ditulis).
- `adaptasi-bahasa-lain.md` — cara menerapkannya ke Mandarin, Jepang, Korea, dan Arab.

Halaman `en-*.md` **dihasilkan** dari data di `alr/game/src/game/content/journey/` oleh `bun scripts/journey.ts --write`. Skrip yang sama memeriksa data itu terhadap benchmark dan isi yang ada: tiap konsep silabus ada di tepat satu bab; anggaran kata per bab cocok dengan jumlah kata per kategori (level yang sudah ditulis) atau dengan jumlah kata baru di kontrak (B2–C2); situasi, bacaan, dialog, dan tugas menulis habis terbagi; tiap misi hanya memakai tokoh, tempat, dan aplikasi yang sudah terbuka di level itu; tiap warga inti punya tepat satu misi per level. Saat ini pemeriksaan itu lolos untuk ketujuh level.

**Silabus B2, C1, dan C2** bahasa Inggris sekarang lengkap sebagai kontrak per bab (tata bahasa dari `benchmark-plan.ts`, ranah kosakata dengan jumlah kata, fungsi bahasa, pelafalan, judul bacaan dan simakan, jenis tulisan). **Isi pelajarannya sendiri belum ditulis**: 7.000 kata, 72 konsep, dan bahan Praktiknya (rincian di `en-ringkasan.md`).

### 10. Dunia yang berkembang

Tiap kampung bahasa tumbuh bertingkat; tingkat terbuka lewat Misi Besar:

| Tingkat | Terbuka setelah | Wilayah | Isi baru (bahasa Inggris) |
|---|---|---|---|
| 0 | — | Kampung (ada) | Kelas, kafe, diner, minimart, laundry, taman, gerbang |
| 1 | Misi Besar Basic | Permukiman | Rumah keluarga Brown, sekolah, kantor pos, taman bermain, wisma, perpustakaan |
| 2 | Misi Besar A1 | Pusat kota | Stasiun, klinik, pusat belanja, bank, agen perjalanan, warnet, museum, pos polisi |
| 3 | Misi Besar A2 | Distrik media & kampus | Kantor berita, radio, kampus, balai kota, informasi wisata |
| 4 | Misi Besar B1 | Luar negeri: kawasan mahasiswa | Bandara, flat, universitas, students' union, lembaga amal, pasar, teater |
| 5 | Misi Besar B2 | Luar negeri: pusat kota | Kantor, lembaga riset, perpustakaan nasional, ruang komite, ruang pers, koran nasional |
| 6 | Misi Besar C1 | Luar negeri: kawasan budaya; lalu pulang | Penerbit, aula kuliah umum, klub komedi, sidang semu, KBRI, studio; Balai Mentor di Pare |

Cara membangunnya, dari yang termurah:

1. **Bangunan terkunci dan adegan.** Pintu bertanda 🔒 "terbuka setelah Misi …". Isi bangunan berupa adegan (jendela seperti toko), bukan peta baru. Dari 45 tempat baru di skenario bahasa Inggris, 40 berupa adegan.
2. **Area peta.** Hanya lima yang perlu area berjalan: taman bermain, stasiun, kampus universitas, Borough Market, Speakers' Corner. Dibuat sebagai templat distrik per tingkat yang diberi tema per bahasa, seperti `buildVillage` sekarang.
3. **Luar negeri.** Kode kota luar negeri (`buildTown`, data `COUNTRIES`) masih ada dari versi awal dan tidak dipakai; dihidupkan lagi untuk tingkat 4–6.

**Komputer dalam game**: satu jendela terminal. Dua puluh aplikasi di skenario (formulir, email, tiket, peta, situs ulasan, meja redaksi, forum, portal lamaran, perekam, obrolan kerja, penyunting dokumen, salindia, portal kampus, pangkalan data, tinjauan dokumen, meja penerjemah, …) semuanya adalah tampilan di atas **tujuh blok dasar**: formulir, utas pesan, penyunting teks, peramban dokumen, pemesanan, audio, dan tinjauan (menandai dan memperbaiki naskah). Yang dibangun tujuh komponen.

**Benda dan tokoh pribadi.** NPC tetap (Tom, Miss Kate) terlihat oleh semua pemain. Tokoh dan benda yang hanya ada karena misi seorang pemain (turis yang diantar, kunci yang dicari, rombongan tur) hanya terlihat oleh pemiliknya, sehingga dua puluh pemain bisa menjalankan misi yang sama tanpa dua puluh turis berdesakan.

### 11. Lapisan game

| Unsur | Rancangan |
|---|---|
| Buku Perjalanan | Satu tempat untuk semua kemajuan: peta hidup, syarat level, bab ini, misi, warga, rapor (§16.5) |
| Kartu misi | Sebelum mulai, pemain melihat tujuan, bekal, langkah, dan cara dinilai (§16.1) |
| Pelacak HUD | Satu baris: "Langkah berikutnya: …" |
| Penanda | "!" misi tersedia, "…" sedang berjalan, "?" siap dilaporkan; titik di minimap; 🔒 di pintu; "💬 n" jumlah pemain yang sedang berbicara dengan NPC itu |
| Bintang 1–3 | Dari skor misi (§16.3). Boleh diulang demi bintang |
| Stempel paspor | Satu per bab, tampil di Buku Perjalanan dan Papan Info |
| Gelar | Satu per Misi Besar ("Warga Baru" … "Duta Bahasa"), ditambah gelar khusus ("Reporter") di papan nama |
| Keakraban warga | Tiap misi warga menaikkan keakraban dengan warga itu (0–7); membuka sapaan dan diskon kecil |
| Barang | Kosmetik (lemari sudah ada), kartu pembuka wilayah (Kartu Warga, Kartu Kota, Kartu Pers, visa pelajar) |
| Papan antarpemain | Tulisan pemain yang lulus terbit dan dipakai misi pemain lain (§17.6) |
| Acara dunia | Kegiatan bersama pada jam tertentu; selalu opsional (§17.5) |

Hadiah misi lebih besar daripada satu kelas dan naik per level, tetap sesuai prinsip ADR-0016 bahwa uang hanya datang dari belajar. Angkanya ditala di tahap 9c.

### 12. Naik level dan nasib fitur lama

- **Naik level** = semua bab lulus + misi warga secukupnya + Misi Besar (§16.6). Ini menggantikan aturan otomatis sekarang (80% kata dikuasai + poin cukup).
- **Ujian lompat level** tetap ada sebagai jalur cepat. Lulus ujian menandai semua bab level itu lulus tanpa bintang; misinya tetap boleh dimainkan demi bintang dan hadiah.
- **Enam kelas lama** pindah ke tab "Latihan bebas" (tetap berhadiah kecil, tidak menggerakkan jalur).
- **Pemain lama**: bab yang katanya sudah dikuasai (≥ 3 kali benar) ditandai selesai otomatis; levelnya tidak diturunkan.
- Pasar, perpustakaan, memancing, Speaking Club, dan Language Challenge tetap sebagai latihan bebas dan hiburan.

### 13. Arsitektur teknis

1. **Konten.** Rencana perjalanan sudah ada sebagai data bertipe di `game/src/game/content/journey/` (`types.ts`, `en.ts`, `en/world.ts`, `en/l0.ts` … `en/l6.ts`). Saat dibangun, data ini menjadi bibit dua bagian baru DSL konten yang diekspor ke `content.json`:
   - `chapters`: `{ id, title, lessons: [{ id, kind: letters|words|concept, words[] | concept }], practice: { situations[], readings[], dialogues[], compose[] }, mission }` — penugasan kata per bab dibuat saat itu, mengikuti anggaran per kategori.
   - `missions`: `{ id, level, chapter, tier, title, story, giver, place, mode, steps: [{ type, app?, … butir dan kunci }], bonus, rewards, unlocks }`.
2. **Basis data** (migrasi baru, aditif, mulai 0095):
   - `pare_path_nodes(user_id, lang, node_id, best_score, attempts, done_at)`
   - `pare_missions(user_id, lang, mission_id, status, step, state jsonb, score jsonb, stars, started_at, done_at)`
   - `pare_unlocks(user_id, key, unlocked_at)` untuk wilayah, bangunan, barang, gelar
   - `pare_sessions(id, kind, lang, mission_id, step, state jsonb, created_at, expires_at)` dan `pare_session_members(session_id, user_id, role, joined_at, left_at)` untuk sesi bersama (§17.9)
   - `pare_posts(id, user_id, lang, board, mission_id, body, score, status, created_at)` dan `pare_post_marks(post_id, user_id, mark)` untuk papan antarpemain
   - `pare_papers`: jenis baru `path` dan `mission`, kolom `node`, `wrong_scale`, `reward`
3. **Backend.** `pare_path.rs` (susunan bab, status simpul, kartu Materi, soal per tahap), `pare_mission.rs` (mulai, maju saat kejadian masuk, verifikasi langkah, skor, hadiah, pembukaan), `pare_session.rs` (pencocokan, giliran, pengganti NPC), `pare_board.rs` (terbit, baca, tandai, moderasi). Mesin misi mendengarkan kejadian di titik yang sama dengan `pare_daily::bump`.
4. **API.** `GET /pare/path/{lang}`, `GET|POST /pare/path/{lang}/lessons/{id}`, `POST /pare/papers {kind: path|mission}`, `GET /pare/journey/{lang}` (isi Buku Perjalanan), `GET /pare/missions`, `GET /pare/missions/{id}` (kartu misi), `POST /pare/missions/{id}/start`, `POST /pare/missions/{id}/steps/{n}`, `GET /pare/boards/{board}`, `POST /pare/posts/{id}/marks`; pesan hub di §17.9.
5. **Game.** Jendela Jalur (pengganti menu kelas), kartu Materi, Buku Perjalanan, kartu dan rapor misi, pelacak HUD, dialog NPC bergilir, jendela komputer (tujuh blok dasar), adegan bangunan, penanda dan pintu terkunci di engine, tokoh dan benda pribadi, jendela sesi bersama.
6. **Pengukuran.** Per simpul dan langkah: percobaan, ketepatan, waktu, berhenti di mana; per sesi bersama: waktu tunggu, berapa kali pengganti NPC dipakai. Dipakai untuk menala §1, §4, dan batas tunggu §17.
7. **Audio.** Semua kalimat NPC misi masuk pipeline audio yang ada (anotasi suara → rekam → cek dengar).
8. **Validasi.** `scripts/journey.ts` (sudah ada, untuk rencana) dan `check-benchmark.ts` (diperluas saat dibangun: tiap kata ada di tepat satu bab; tiap langkah menunjuk NPC, tempat, dan barang yang ada; semua teks punya audio).

### 14. Tahapan

| Tahap | Isi | Hasil yang bisa dicoba |
|---|---|---|
| 9a Jalur Basic | Bab Basic lima bahasa; Materi, Latihan, Praktik, Cek; aturan hadiah; jendela Jalur | Pemain baru belajar berurutan tanpa denda |
| 9b Mesin misi | Mesin langkah dan skor, kartu dan rapor misi, Buku Perjalanan, pelacak, penanda; 5 misi bab + 10 misi warga Basic bahasa Inggris | Bab 1–5 Inggris lengkap dengan misi dan kemajuan yang terlihat |
| 9c Dunia tahap 1 | Pintu terkunci, adegan, `pare_unlocks`, tokoh pribadi, Misi Besar Basic, bintang/stempel/gelar, aturan naik level | Satu level utuh dari awal sampai naik level |
| 9d Multipemain inti | Kehadiran di NPC, sesi bersama (ramai, pasangan, kelompok), papan antarpemain, kelas bersama | Misi Basic–A1 yang bisa dimainkan bersama |
| 9e A1 Inggris | 14 bab dan misinya; Permukiman; komputer (formulir, pesan, kalender) | — |
| 9f A2 Inggris | Pusat kota; email, tiket, peta, ulasan; telepon; skor rubrik | — |
| 9g B1 Inggris | Distrik media & kampus; meja redaksi, forum, perekam; presentasi | Perjalanan Basic → B1 utuh |
| 9h Bahasa lain | Basic → B1 untuk zh, ja, ko, ar menurut `adaptasi-bahasa-lain.md` | — |
| 9i B2 Inggris | Menulis isi B2 (2.000 kata, 28 konsep), misi, London tingkat 4 | — |
| 9j C1 Inggris | Isi C1 (3.000 kata), misi, tingkat 5, telaah sejawat | — |
| 9k C2 Inggris | Isi C2 (2.000 kata), misi, tingkat 6, Balai Mentor | Perjalanan Basic → C2 utuh |

Perkiraan kasar (belum diukur): 9a–9d masing-masing 2–4 sesi kerja; 9e–9g masing-masing lebih besar karena 14 misi bab, adegan, dan audio; 9i–9k didominasi penulisan isi. Rincian tiket: `tickets/pare-9-jalur-misi.md`.

### 15. Keputusan (2026-10-04)

User menyerahkan semua pilihan kepada saya ("pilihkan yang terbaik"); berikut yang diputuskan, dengan alasannya. Semuanya bisa diubah lewat revisi ADR ini.

**Aturan belajar**
1. **XP tidak pernah berkurang di jalur belajar.** Salah terus adalah sumber jenuh yang diminta dihindari; taruhannya cukup gerbang 80% dan bintang.
2. **Aturan naik level baru** (§12, §16.6) menggantikan aturan poin; ujian lompat level tetap jalur cepat.
3. **Misi warga wajib "pilih 3 dari 10"** per level (Basic: 2). Membuat pemain menjalani ulangan berjarak tanpa memaksa satu misi tertentu.
4. **Kelas lama menjadi "Latihan bebas"**, bukan dihapus: pemain lama kehilangan paling sedikit.

**Urutan kerja**
5. **Bahasa Inggris sampai B1 dulu**, baru empat bahasa lain: mesin misi terbukti pada satu bahasa sebelum isinya digandakan lima kali.
6. **Isi B2–C2 ditulis setelah mesin terbukti** di Basic–B1.

**Dunia dan cerita**
7. **Bangunan terkunci dan adegan dulu**; hanya lima area peta baru.
8. **Latar dan tokoh di skenario disetujui** sebagai bahan kerja; nama fiktif boleh diganti kapan saja karena hanya data.
9. **"Border" = gerbang wilayah** (§10).

**Penilaian**
10. **Rubrik AI untuk semua langkah `tulis` dan `presentasi`**, batas tiga penilaian per langkah per hari, dengan cadangan aturan bila AI tidak tersedia. Biaya diukur di P9-016 sebelum dibuka luas.
11. **Berbicara dinilai dari naskah yang diketik**; bicara dengan pemain lain tidak dinilai (konsisten dengan ADR-0017, 2026-09-26).

**Multipemain**
12. **Urutan: kehadiran di NPC + sesi "ramai" + papan antarpemain dulu**, lalu pasangan dan kelompok (tahap 9d).
13. **Tulisan yang lulus tampil ke pemain lain dengan nama panggilan secara default**, dengan pilihan "sembunyikan tulisanku" dan tombol lapor.
14. **Jadwal acara dunia hanya tebakan**: dibuat sebagai konfigurasi yang bisa diubah tanpa deploy dan ditala setelah ada data jam ramai.

**Bahasa lain**
15. **Negeri tujuan bahasa Arab: Kairo** (alasan di `adaptasi-bahasa-lain.md`).

### 16. Misi dari sisi pemain: tahu caranya, tahu ukurannya, tahu posisinya

#### 16.1 Kartu misi (sebelum mulai)

Tiap misi dibuka dengan satu kartu. Tidak ada informasi penilaian yang disembunyikan.

| Bagian kartu | Isi | Contoh ("Makan siang pertama", Basic) |
|---|---|---|
| Judul dan cerita | Satu atau dua kalimat | Miss Kate menyuruhmu makan siang sendiri di kafe |
| Hasil nyata | Apa yang harus ada di akhir | Pesanan datang sesuai yang kamu minta |
| Bekal | Pelajaran yang harus sudah selesai (dengan tanda ✓ dan tautan ke Materinya), uang atau barang, perangkat | Bab 3 ✓ · uang ± Rp3.000 · pengeras suara |
| Kalimat kunci | 3–4 kalimat sasaran, bisa didengar | "Can I have a tea, please?" |
| Langkah | Daftar langkah dengan jenisnya; langkah berikutnya ditandai | 1 pergi · 2 dialog · 3 beli · 4 dengar · 5 dialog · 6 bicara |
| Cara dinilai | Tiga komponen skor dan syarat tiap bintang | lihat §16.3 |
| Tantangan bintang ketiga | Mulai A2 | — |
| Waktu, tempat, mode | Perkiraan menit; di mana mulai; sendiri atau bisa bersama | ± 6 menit · CAFÉ · solo |
| Tombol | **Mulai** · **Latihan dulu** (pemanasan 5 butir dari kalimat kunci, tanpa hadiah dan tanpa pengaruh ke skor) · **Nanti** | |

#### 16.2 Selama misi

- **Pelacak** di HUD menunjukkan langkah sekarang; Buku Perjalanan menunjukkan semua langkah dan catatan yang terkumpul (kutipan saksi, daftar belanja, jadwal).
- **Petunjuk tiga tingkat.** Tingkat 1 gratis: NPC mengulang pelan atau menyederhanakan kalimatnya. Tingkat 2: kata pertama jawaban atau terjemahan pertanyaan. Tingkat 3: jawaban ditunjukkan, lalu butir serupa muncul sekali lagi. Tingkat 2 dan 3 mengurangi skor Mandiri.
- **Salah** tidak menghentikan misi: NPC bereaksi wajar ("Sorry?"), pemain mencoba lagi.
- **Tinggal dan lanjut** kapan saja; status tersimpan di server.

#### 16.3 Penilaian

Skor misi 0–100 dari tiga komponen, semuanya terlihat di kartu misi:

| Komponen | Bobot | Dihitung dari |
|---|---|---|
| **Hasil** | 40 | Apakah hasil nyata tercapai dengan benar: barang yang dibeli cocok, alamat benar, formulir lengkap, pesanan memenuhi anggaran, tulisan memenuhi tugasnya. Butirnya tertulis di baris "Dinilai dari" tiap misi |
| **Bahasa** | 40 | Butir bahasa: penuh kalau benar pada percobaan pertama, separuh pada percobaan kedua, nol setelahnya. Tulisan dan presentasi: rata-rata rubrik |
| **Mandiri** | 20 | Mulai dari 20. Petunjuk tingkat 2: −2. Petunjuk tingkat 3: −5. Membuka transkrip simakan atau telepon: −3. Tidak pernah di bawah 0 |

| Bintang | Syarat |
|---|---|
| ⭐ | Semua langkah wajib selesai dan skor ≥ 60. Ini yang dibutuhkan untuk lulus bab |
| ⭐⭐ | Skor ≥ 80 |
| ⭐⭐⭐ | Skor ≥ 90, tanpa petunjuk tingkat 3, dan (mulai A2) tantangan tambahan di kartu misi tercapai. Tantangan itu selalu bisa dicapai sendirian |

**Rubrik untuk tulisan dan presentasi** (langkah `tulis` dan `presentasi`): empat kriteria, masing-masing 0–5, sama dengan penilai menulis yang sudah ada (`ComposeGrade`), dengan tuntutan yang naik per level.

| Kriteria | Yang dilihat | Naik per level |
|---|---|---|
| Isi & tugas | Semua bagian tugas dijawab; panjang dalam rentang | B2+: argumen dan bukti; C1+: sesuai jenis teks |
| Struktur sasaran | Struktur bab dipakai dengan benar; ada aturan minimum yang tertulis di kartu (mis. "minimal tiga kalimat tak langsung yang cocok dengan kutipan") | Dicek aturan dulu, baru AI |
| Kosakata & ketepatan | Pilihan kata, ejaan, kolokasi | B2+: ragam; C1+: kolokasi dan nuansa; C2: konotasi |
| Keterpaduan (tulisan) / Penyampaian (presentasi) | Urutan, penghubung; untuk presentasi: susunan dan kejelasan naskah | C1+: kohesi; C2: gaya dan dampak |

- Langkah lulus kalau jumlahnya ≥ 12 dari 20 dan tidak ada kriteria di bawah 2.
- Sebelum AI, tulisan dicek dengan aturan: panjang, bahasa yang dipakai, dan aturan struktur. Kalau AI tidak tersedia, pengecekan aturan saja yang berlaku dan pemain tidak tertahan (perilaku `pare_compose.rs` sekarang).
- Tiap penilaian memberi catatan per kriteria dalam bahasa Indonesia dan versi yang sudah diperbaiki.
- Mengulang selalu boleh. Skor terbaik per langkah yang dihitung. Usul batas: tiga penilaian AI per langkah per hari (§15.10).
- **Bersama pemain lain tidak pernah menurunkan skor.** Skor tiap pemain hanya dari jawabannya sendiri; kesalahan atau kepergian pasangan tidak berpengaruh (§17.8).
- Kalau misi selesai dengan skor di bawah 60, pemain mendapat daftar langkah yang paling menurunkan skor dan tombol "Perbaiki" untuk mengulang langkah itu saja.

#### 16.4 Rapor misi (setelah selesai)

Satu layar: skor per komponen; bintang; butir yang salah beserta jawaban benarnya; untuk tulisan, catatan per kriteria dan versi perbaikan; "Yang perlu diulang" dengan tautan ke pelajaran yang bersangkutan; hadiah dan apa yang terbuka. Rapor tersimpan dan bisa dibuka lagi dari Buku Perjalanan.

#### 16.5 Buku Perjalanan: tempat melihat kemajuan

Dibuka dari tombol 📖 di HUD (selalu ada), dari Papan Info di kamar, dan dari pintu kelas. Enam halaman:

| Halaman | Isi |
|---|---|
| **Peta hidup** | Tujuh tahap sebagai satu jalan: tahap yang sudah lewat (gelar dan tanggal), posisi sekarang dengan persentase, tahap berikutnya dengan apa yang akan terbuka |
| **Level ini** | Daftar centang syarat naik level (§16.6) dengan angka: bab lulus 6/14, misi bab 5/14, misi warga 1/3, Misi Besar 🔒; perkiraan sisa waktu; "Yang perlu kamu siapkan" untuk level ini |
| **Bab ini** | Peta bab: tiap simpul (📖 🧩 🎯 🏁 ⭐) dengan statusnya; apa saja isi bab; kartu misi bab yang bisa dibaca sejak bab dibuka |
| **Misi** | Aktif (langkah dan catatan), tersedia (kartu misi), selesai (bintang, rapor, tombol ulang) |
| **Warga** | Sepuluh warga inti: keakraban, misi yang tersedia di level ini, misi yang sudah selesai |
| **Rapor** | Enam batang kemampuan (kosakata, tata bahasa, menyimak, membaca, menulis, berbicara) yang dihitung dari hasil simpul dan misi; kata yang dikuasai; butir yang paling sering salah; stempel dan gelar |

#### 16.6 Syarat lulus bab dan naik level

**Satu bab lulus kalau:**
1. semua pelajarannya selesai (Materi dibuka, Latihan tuntas);
2. semua Praktik bab dikerjakan;
3. Cek bab ≥ 80%;
4. Misi bab mendapat minimal ⭐.

**Naik level kalau:**
1. semua bab level itu lulus;
2. misi warga yang selesai ≥ 3 dari 10 (Basic: 2), bebas pilih;
3. Misi Besar mendapat minimal ⭐.

Jalur cepat: lulus ujian lompat level (§12).

**Supaya pemain tahu apa yang harus disiapkan**, tiga tempat menyebutkannya sebelum ia memulai: halaman "Level ini" (bekal untuk satu level: panjang tulisan, perangkat, perkiraan jam), pembukaan bab (peta bab dan kartu misi bab), dan kartu misi (bekal untuk satu misi). Isi ketiganya untuk bahasa Inggris sudah tertulis di halaman tiap level di `pare-perjalanan/`.

### 17. Multipemain dan waktu nyata

#### 17.1 Prinsip

1. **Jalur wajib selalu bisa diselesaikan sendirian, kapan saja.** Jam tiga pagi, kampung kosong, misi tetap jalan. Pemain lain adalah nilai tambah, bukan syarat.
2. **NPC tidak pernah terpakai.** NPC adalah tokoh bersama di peta, tetapi percakapannya adalah jendela pribadi dengan state di server per pemain. Tidak ada antrean dan tidak ada kunci.
3. **Isi misi diacak per pemain.** Daftar belanja, harga, alamat, keterangan saksi, dan kutipan diambil dari kumpulan varian dengan benih (pemain, misi). Pemain bisa saling membantu dalam bahasa sasaran, tetapi tidak bisa menyalin jawaban.
4. **Benda dan tokoh misi bersifat pribadi** (§10).
5. **Waktu nyata tidak pernah mengunci.** Langkah `waktu` selalu memakai jendela relatif ("10–20 menit dari sekarang") atau acara yang berulang, tidak pernah satu jam tertentu per hari. NPC misi melayani 24 jam. Cuaca nyata dipakai apa adanya; tidak ada misi yang menunggu hujan. Tidur di game memakan jam sungguhan, jadi tidak pernah menjadi langkah wajib.
6. **Status misi ada di basis data**, bukan di memori hub, sehingga sambungan putus, pindah perangkat, atau server dimulai ulang tidak menghilangkan kemajuan.

#### 17.2 Banyak pemain di satu warga

Kasus "satu warga diwawancarai banyak siswa sekaligus":

| Jumlah pemain di NPC yang sama | Yang terjadi |
|---|---|
| 1 | Dialog pribadi biasa |
| 2–5 | Masing-masing tetap punya dialog pribadi. Di atas NPC tampil "💬 n". Kalau mereka berada di langkah misi yang sama dalam 60 detik, muncul tawaran **tanya-jawab bersama**: tiap pemain mengajukan satu pertanyaan (butirnya sendiri, dinilai sendiri), semua mendengar semua jawaban, catatan dibagi. Menolak tidak merugikan |
| 6–50 | Sama, dengan beberapa sesi bersama berjalan sejajar (paling banyak 5 pemain per sesi). Avatar pemain lain diredupkan selama dialog supaya layar tidak penuh |
| > 50 | Zona otomatis terbagi ke kanal berisi paling banyak 50 pemain (perilaku hub sekarang); tiap kanal punya tampilan NPC yang sama |

Beban server untuk n pemain di satu NPC adalah n kertas soal biasa; tidak ada state bersama kecuali sesi yang mereka pilih.

Kasus sebaliknya juga dipakai: di misi "Konferensi pers krisis" (C1) **pemainlah yang ditanyai** banyak pemain lain yang berperan sebagai wartawan.

#### 17.3 Lima mode

Tiap misi di skenario menyebut modenya dan apa yang terjadi kalau tidak ada pemain lain.

| Mode | Apa | Ukuran | Cara bertemu | Pengganti | Contoh |
|---|---|---|---|---|---|
| **solo** | Pribadi; pemain lain hanya terlihat | 1 | — | — | Belanja pertama; Tinjauan bukti |
| **ramai** | Dialog pribadi, dengan tawaran sesi bersama, atau pemain lain boleh menggantikan seorang warga (menjawab lewat tombol jawab cepat) | 2–5 | Berada di tempat dan langkah yang sama | Warga NPC menjawab setelah 30 detik | Survei kelas; Bingo pengalaman; Reporter Kampung |
| **pasangan** | Main peran berdua dengan tukar peran: pelanggan–pelayan, petugas–turis, analis–klien, penulis–penerbit | 2 | Antrean pencocokan per (bahasa, misi, peran), lintas kanal dan zona | NPC setelah 45 detik | Pelayan sehari; Pemandu wisata (peta dipegang satu pemain); Negosiasi; Sidang semu |
| **kelompok** | Sesi berperan 3–5 orang: rapat, debat, tim redaksi, komite, cerita berantai, Simon says | 3–5 | Mulai begitu cukup orang, atau pada jadwal | NPC mengisi kursi kosong; mulai sendiri setelah 60 detik | Rapat balai kota; Debat; Edisi khusus |
| **asinkron** | Hasil pemain terbit di papan dan dipakai misi pemain lain: dibaca, ditandai, dibalas, ditelaah | — | Tidak perlu bersamaan | Tulisan contoh kalau papan kosong | Laporan cuaca; Ulasan; Kolom opini; Telaah sejawat |

Jumlah misi bab per mode dan per level ada di `en-ringkasan.md`. Di Basic hampir semuanya solo; di B2–C2 hampir semuanya melibatkan pemain lain bila ada.

Cara sesi dinilai tanpa bergantung pada lawan main: di A1–A2 tiap giliran adalah butir terpandu (pilih, susun, ketik) yang dicek server; mulai B1 giliran berupa teks bebas yang dicek aturan bahasa chat yang sudah ada dan, untuk sumbangan utama, rubrik. Panggilan suara langsung (fitur yang ada) boleh dibuka di dalam sesi, tetapi tidak dinilai.

#### 17.4 Kelas bersama

- **Jalur tetap pribadi.** Materi dan Latihan dibuka kapan saja dari meja belajar atau pintu kelas, tanpa menunggu siapa pun. Seratus pemain bisa belajar di kelas yang sama pada saat yang sama.
- **Sesi kelas bersama**, per level, tiap jam pada menit 00 dan 30, 10 menit, dipimpin guru NPC: delapan butir ulangan dari bab yang sudah dilulusi sebagian besar peserta. Tiap pemain menjawab sendiri (tanpa denda); setelah tiap butir, papan menunjukkan persentase benar kelas dan penjelasannya. Kalau kelas mencapai 80%, semua peserta mendapat bonus kecil. Satu butir dikerjakan dengan teman sebangku (pemain lain, atau murid NPC).
- Paling banyak 20 pemain per sesi; kelebihannya membuka sesi sejajar.
- **Papan tanya kelas**: pemain menulis pertanyaan; pemain di level lebih tinggi menjawabnya lewat misi mentor (§17.7).
- Kelas bersama tidak wajib dan tidak menggerakkan jalur; ia berfungsi sebagai ulangan berjarak.

#### 17.5 Acara dunia

Kegiatan bersama pada jam WIB tertentu atau begitu cukup pemain menunggu. Semuanya opsional dan berulang: Hitung bersama dan Sapa pagi (Basic), Pesta kampung dan Simon says (A1), Malam Cerita dan Jam sibuk toko (A2), Konferensi pers dan Rapat balai kota (B1), Kuliah langsung, Debat klub, Konferensi mahasiswa (B2), Dengar pendapat publik dan Salon filsafat (C1), Malam satire, Debat gaya Oxford, Speakers' Corner (C2). Babak yang memakai acara dunia di Misi Besar selalu punya versi NPC di luar jadwal.

#### 17.6 Papan antarpemain dan moderasi

Papan: papan cuaca wisma, keterangan foto museum, situs ulasan, papan berita, forum warga, kamus kampung, aula poster, papan petisi, koran mahasiswa, halaman opini, lampiran sastra.

- Hanya tulisan yang **lulus penilaian** yang terbit, dan lolos saringan kata kasar yang sudah ada serta tanda moderasi dari penilai.
- Pembaca hanya bisa memberi tanda berlabel tetap ("membantu", "setuju", "tidak setuju", tanda tangan) atau balasan terstruktur di dalam misinya sendiri. Tidak ada kolom komentar bebas di luar misi.
- Tiap tulisan punya tombol lapor; penulis bisa menarik tulisannya; pemain bisa memilih agar tulisannya tidak pernah ditampilkan (§15.13).
- Papan tidak pernah kosong: tulisan contoh mengisi sampai ada tulisan pemain.
- Papan menampilkan sejumlah terbatas tulisan terbaru per papan; tulisan lama diarsipkan.

#### 17.7 Mentor

Mulai A2, misi warga Miss Kate meminta pemain membantu pemain di bawahnya: memeriksa kalimat, menjawab papan tanya kelas. Di akhir C2 ini menjadi kegiatan setelah tamat (Balai Mentor): menjawab pertanyaan, memberi masukan atas tulisan pemain Basic–A2, menjadi juri debat atau penelaah. Penerima menilai apakah bantuan itu membantu; mentor mendapat poin mentor, bukan XP bahasa. Kalau tidak ada pemain yang menunggu, murid NPC yang bertanya.

#### 17.8 Keadilan dan penyalahgunaan

- Skor pribadi; lawan main tidak bisa menurunkannya (§16.3).
- Pasangan yang diam 60 detik atau keluar digantikan NPC tanpa mengulang langkah.
- Blokir dan lapor yang sudah ada berlaku di sesi; pemain yang diblokir tidak dipasangkan.
- Hadiah sosial hanya sekali per misi; menjawab pertanyaan pemain lain memberi poin kecil dengan batas harian.
- Aturan bahasa chat tetap berlaku di sesi (hanya bahasa sasaran), dengan satu pengecualian yang disengaja: sesi juru bahasa di C2 memakai bahasa Indonesia sebagai bahasa sumber, dan hanya di dalam sesi itu.
- Jawaban cepat untuk survei ("Yes, I have.") adalah tombol, bukan teks bebas, sehingga tidak bisa disalahgunakan.

#### 17.9 Teknis

- **Kehadiran di NPC.** Klien mengirim "sedang berbicara dengan NPC x"; hub menyiarkan jumlah per NPC ke kanal, paling sering sekali per detik.
- **Pencocokan.** Antrean di memori hub per (bahasa, misi, langkah, peran). Kalau hub dimulai ulang, antrean hilang dan klien mengantre lagi; tidak ada kemajuan yang hilang.
- **Sesi.** State tiap sesi disimpan di `pare_sessions` pada tiap giliran. Pesan sesi dikirim ke tiap anggota lewat jalur yang sama dengan chat pribadi (`send_to_user`), sehingga anggota boleh berada di kanal atau zona berbeda. Sesi misi paling banyak 6 anggota, sama dengan batas percakapan grup yang ada. Sesi kelas bersama (paling banyak 20) tidak memakai chat grup: tiap pemain menjawab sendiri dan hub hanya menyiarkan hasil gabungan.
- **Pesan hub baru:** `npc_presence`, `session_offer`, `session_join`, `session_state`, `session_turn`, `session_end`, `mission_update`, `board_new`.
- **Batas skala.** Hub berjalan di satu proses. Sesi lintas instance baru mungkin setelah pembagian lewat Redis (P4-003 di tiket Pare-4) dikerjakan. Untuk satu instance rancangan ini cukup.
- **Jam.** Semua langkah `waktu` dan jadwal acara dihitung server dalam WIB.

### 18. Bahasa lain

Struktur (§2–§8, §16, §17) sama untuk semua bahasa. Yang berbeda adalah isi bab, urutan, tokoh, latar, dan beberapa jenis pelajaran (aksara, nada, kanji, tingkat tutur, akar kata). Panduannya di `pare-perjalanan/adaptasi-bahasa-lain.md`. Skenario bahasa lain ditulis sebagai data dengan bentuk yang sama (`journey/zh.ts`, …) dan diperiksa skrip yang sama.

## Consequences

- **Volume adalah biaya terbesar.** Untuk bahasa Inggris saja: 158 misi, 36 tokoh yang belum ada di peta (5 di antaranya sudah punya nama dan sapaan di data), 45 tempat baru (40 adegan), tujuh blok komputer, audio untuk semua kalimat NPC, dan isi pelajaran B2–C2 yang belum ada (7.000 kata, 72 konsep). Pola misi (§7) dan blok komputer (§10) menekan biaya, tetapi tidak menghilangkannya.
- **Waktu belajar.** Hitungan dari data: jalur wajib ± 4 jam (Basic), 18 (A1), 27 (A2), 35 (B1), 45 (B2), 60 (C1), 52 (C2); jumlahnya ± 240 jam. Ini perkiraan dari jumlah pelajaran dan misi, belum diukur. Jam belajar yang biasa dikutip untuk mencapai C2 beberapa kali lebih besar, jadi game ini pelengkap, bukan pengganti penuh; label level jangan dijanjikan setara sertifikat.
- **Penilaian AI** dipakai di 87 langkah jalur wajib (6 di A1 sampai 22 di C1). Keandalannya untuk tulisan C1–C2 (gaya, ironi, terjemahan) belum teruji, dan biayanya belum diukur. Aturan struktur sebelum AI dan pengecekan aturan saat AI tidak tersedia mengurangi risiko, tetapi rubrik C2 kemungkinan perlu model yang lebih kuat atau telaah sejawat sebagai penyeimbang.
- **Berbicara** tetap titik lemah: yang dinilai adalah naskah, bukan suara. Pelafalan hanya dilatih lewat langkah `ucap` (kalimat tetap, hanya Chrome) dan lewat bicara dengan pemain lain yang tidak dinilai.
- **Multipemain** bergantung pada adanya pemain di level yang sama pada saat yang sama. Di level tinggi pemain akan sedikit, sehingga pengganti NPC akan sering terpakai dan harus sama baiknya dengan versi bersama. Papan asinkron lebih tahan terhadap jumlah pemain yang kecil daripada sesi langsung; karena itu ia dibangun lebih dulu.
- **Moderasi** menjadi kewajiban begitu tulisan pemain tampil ke pemain lain.
- **Hub satu proses** membatasi sesi lintas instance (§17.9).
- **Ekonomi** perlu ditala ulang (hadiah misi, kelas, tantangan) supaya jalur tidak membuat uang terlalu mudah.
- Aturan naik level berubah; pemain lama perlu pemetaan otomatis (§12) supaya tidak kehilangan kemajuan.
- **Isi level yang sudah ditulis punya celah Praktik**: enam bab A1–A2 belum punya cukup situasi dan dialog untuk temanya (daftar di `en-ringkasan.md`).
