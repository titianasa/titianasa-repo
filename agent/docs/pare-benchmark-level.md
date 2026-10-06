# Benchmark Level Bahasa — Kampung Bahasa Pare (Basic · A1 · A2)

Status: **Berlaku (2026-09-25)**. Audit Basic–A2 sudah ditindaklanjuti: isi kelima bahasa ditulis ulang sesuai benchmark ini (lihat §8), dan benchmark ini menjadi patokan untuk B1 ke atas. Tes `pare_content::tests::every_language_meets_the_level_benchmark` memeriksanya setiap build.

Sumber isi yang diaudit: `titian-backend-rust/data/pare/content.json` (diekspor dari `alr/game/src/game/content/`) dan pembangun soal `services/pare_lesson.rs` / `pare_paper.rs`.

---

## 1. Kesimpulan singkat

Isi Basic–A2 saat ini **belum merepresentasikan level yang sebenarnya**. Tiga masalah utama:

1. **Jumlahnya jauh di bawah standar.** Basic 42 kata, level 1 dan level 2 masing-masing 24 kata, jadi total 90 kata sampai A2. Standar terkecil (HSK 2.0) meminta 300 kata sampai HSK 2; bahasa lain di kisaran 1.000–2.000 kata. Tata bahasanya hanya 4 pola kalimat dan 4 konsep per level; standar A1 atau A2 punya belasan sampai puluhan butir tata bahasa per level.
2. **Beberapa materi tidak berada di levelnya.** Ada materi yang terlalu sulit untuk levelnya (present perfect di Basic Inggris, 渋滞 di N4, kata HSK 3–4 di Basic dan HSK 2). Ada juga yang terlalu mudah: tata bahasa N4 dan TOPIK 2 hampir semuanya materi N5/TOPIK 1.
3. **Latihan dan ujian belum mengikuti level.** Kelas memilih kata menurut kategori yang hanya cocok untuk Basic dan level 1. Pasar selalu memakai angka 1–10. Ujian hanya 20 soal pilihan ganda dan susun kalimat, tanpa bagian menyimak dan membaca seperti ujian resmi.

Selain itu, **tangga level bahasa Arab tidak sejajar**: level 2 Arab (Mutawassith) dicap B1–B2, padahal level 2 bahasa lain adalah A2. Bahasa Arab tidak punya level A2.

---

## 2. Standar acuan

| Level game | CEFR | Inggris | Mandarin | Jepang | Korea | Arab |
|---|---|---|---|---|---|---|
| Basic (sebelum level) | Pra-A1 | Pre-A1 (Cambridge Starters) | — | — | — | — |
| Level 1 | A1 | A1 | HSK 1 | JLPT N5 | TOPIK 1 | Mubtadi' 1 (usulan) |
| Level 2 | A2 | A2 | HSK 2 | JLPT N4 | TOPIK 2 | Mubtadi' 2 (usulan) |

**Jumlah kosakata kumulatif** (angka yang lazim dipakai; hanya HSK yang punya daftar resmi):

| | Inggris | Mandarin | Jepang | Korea | Arab |
|---|---|---|---|---|---|
| A1 | ±500–700 | HSK 1: 150 (2.0) · 500 (3.0) | N5: ±800 · ±100 kanji | TOPIK 1: ±800 | ±500 |
| A2 | ±1.000–1.500 | HSK 2: 300 (2.0) · 1.272 (3.0) | N4: ±1.500 · ±300 kanji | TOPIK 2: ±1.500–2.000 | ±1.000 |

Catatan:
- **HSK**: standar 2.0 (daftar 150/300 kata) adalah yang lama; standar 3.0 (GF0025-2021) jauh lebih besar. Status peralihan ujian ke 3.0 perlu dicek saat penulisan ulang, karena menentukan daftar mana yang dipakai.
- **JLPT**: sejak 2010 tidak menerbitkan daftar resmi; angka di atas adalah perkiraan umum dari materi persiapan.
- **TOPIK**: tidak punya daftar resmi per level; angka berasal dari materi persiapan.
- **Arab**: tidak ada ujian standar tunggal. Acuan yang dipakai: deskriptor CEFR/ACTFL dan urutan buku ajar yang lazim (mis. *Al-ʿArabiyyah Bayna Yadayk*).

**Ujian resmi sebagai pembanding bentuk ujian:**

| Ujian | Isi | Batas lulus |
|---|---|---|
| HSK 1 | 40 soal: menyimak 20, membaca 20 | 120/200 (60%) |
| HSK 2 | 60 soal: menyimak 35, membaca 25 | 120/200 (60%) |
| JLPT N5 / N4 | kosakata-tata bahasa-membaca + menyimak | 80/180 · 90/180, dengan nilai minimum per bagian |
| TOPIK I (level 1–2) | 70 soal: menyimak 30, membaca 40 | level 1 ≥ 80/200 · level 2 ≥ 140/200 |
| Cambridge A1 Movers / A2 Key | membaca, menulis, menyimak, berbicara | — |

Ujian game saat ini: 20 soal, lulus 17 (85%), tanpa bagian menyimak atau membaca teks.

---

## 3. Temuan per bahasa

### Inggris

| Level | Isi sekarang | Masalah |
|---|---|---|
| Basic | 42 kata survival; 7 pola | "I have eaten breakfast" adalah present perfect (A2/B1), terlalu sulit untuk Basic. Simple present sudah diajarkan di Basic, lalu diulang di A1. |
| A1 | keluarga, waktu, tempat, kata kerja, sifat; present & past simple | Belum ada materi inti A1: present continuous, can/can't, there is/are, have got, imperatif, this/that, jamak, kata ganti objek, hari/bulan, warna, angka 11–100, pakaian, pekerjaan, cuaca. |
| A2 | belanja, kesehatan, kerja, liburan; comparative, going to, have to/must, some/any | some/any sebenarnya materi A1. Yang belum ada: past continuous, present perfect (ever/never), will, superlative, should, much/many, adverb of frequency. |

### Mandarin

| Level | Masalah |
|---|---|
| Basic | Banyak kata yang di atas HSK 1–2 (daftar 2.0): 护照, 地铁, 洗澡, 刷牙 (HSK 3); 饺子 (HSK 4); 酒店 dan 鸡肉 tidak ada di HSK 1–2. |
| HSK 1 | Kosakata sebagian besar sesuai, kecuali 银行 (HSK 3); 哥哥 dan 姐姐 adalah kata HSK 2. Tata bahasanya (很, 个, 了, 的, posisi waktu) sesuai. |
| HSK 2 | Tata bahasanya sesuai (比, 正在, 过, 一点儿/一下), tapi kosakatanya bercampur: 超市, 自行车, 船, 换, 试 (HSK 3); 逛街, 打折 (HSK 4); 堵车 dan 药店 di luar daftar. Tata bahasa HSK 2 yang belum ada: 要…了, 已经, 就/还, 因为…所以, 虽然…但是, 得 (komplemen derajat), 从…到, 离, 着, 别. |

### Jepang

| Level | Masalah |
|---|---|
| Basic | Sesuai untuk pra-N5. |
| N5 | Kosakata dan tata bahasanya sesuai N5 (を/に/で, ました, kata sifat い, います/あります), tapi baru sebagian kecil. Belum ada: kata sifat な, ～たい, ～ましょう, ～ています, ～てください, kata penunjuk, angka dan kata bantu bilangan, hari/tanggal. |
| N4 | **Terlalu mudah.** ～てください, ～てもいいです, ～てはいけません, ～ています adalah materi N5; hanya bentuk biasa + と思う yang benar N4. Kosakatanya hampir semua N5 (天気, 雨, 駅, バス, 切符, 安い…), sementara 渋滞 kira-kira N2–N3. Materi N4 yang belum ada: bentuk potensial, bentuk ajakan (～よう), ～たら/～ば, ～ながら, ～つもり, ～たことがある, ～ことができる, memberi-menerima (あげる/くれる/もらう), ～そう, pasif. |

### Korea

| Level | Masalah |
|---|---|
| Basic | Sesuai; angka Sino-Korea 1–10 sudah ada. |
| TOPIK 1 | Sesuai tapi baru sebagian kecil. Belum ada: -고 싶다, -지만, -(으)러 가다, -고, -(으)세요, 안/못, kata penunjuk, hari/tanggal. |
| TOPIK 2 | **Terlalu mudah.** -고 싶다 dan -(으)ㄹ 거예요 biasanya diajarkan di TOPIK 1. Tata bahasa TOPIK 2 yang belum ada: -아서/어서, -(으)니까, -(으)면, -는데, -(으)ㄹ 수 있다/없다, -아야/어야 하다, -아/어 보다, -기 전에/-(으)ㄴ 후에, -(으)ㄹ게요, bentuk pewatas -는/-(으)ㄴ/-(으)ㄹ. Kosakatanya sesuai. |

### Arab

| Level | Masalah |
|---|---|
| Tangga level | Basic → Mubtadi' (A1–A2) → Mutawassith (B1–B2) → Mutaqaddim (C1). **Tidak ada A2 tersendiri, dan level 2 melompat ke B1.** |
| Basic | Sesuai. Kosakata daily-nya berupa frasa (أَذْهَبُ إِلَى الْمَدْرَسَةِ), bukan kata. |
| Level 1 | Sesuai A1 (dhamir muttashil, madhi, mudhari', kata tanya). |
| Level 2 | Isinya B1 (wazan, لِأَنَّ, عِنْدَمَا, قَدْ, لَمْ + majzum, surat/berita). Kalau level 2 harus A2, materi A2 Arab belum ada: mutsanna & jamak (salim dan taksir), idhafah, kesesuaian sifat–benda, bilangan 11–100, سَـ/سَوْفَ, لَنْ + manshub, كَانَ, preposisi dan kata penunjuk lengkap. |

**Usulan tangga Arab** (sejajar dengan bahasa lain):

| Level | Nama | CEFR |
|---|---|---|
| 0 | Basic | Pra-A1 |
| 1 | Mubtadi' 1 | A1 |
| 2 | Mubtadi' 2 | A2 |
| 3 | Mutawassith 1 | B1 |
| 4 | Mutawassith 2 | B2 |
| 5 | Mutaqaddim | C1 |

Isi level 2 Arab yang sekarang (B1) dipindah ke level 3.

---

## 4. Temuan lintas bahasa: struktur dan latihan

| # | Temuan | Dampak |
|---|---|---|
| 1 | **Basic (42 kata) lebih besar dari level 1 dan level 2 (24 kata).** Di standar, jumlah kata bertambah tiap naik level (HSK: 150 → +150 → +300). | Progres terasa terbalik. |
| 2 | **Kelas memilih kata berdasarkan kategori tetap** (`class_lesson`): kelas Kosakata = greet/number/family/time/adj, kelas Makanan = food/adj. Di level 2 kategorinya berbeda, jadi kelas Makanan Mandarin/Arab/Korea tidak berisi kata makanan dan kelas Kosakata Mandarin hanya mendapat 4 kata sifat. Sisanya diambil acak. | Nama kelas tidak sesuai isinya. `ROLE_INFO_HIGHER` di game menulis "Keluarga, waktu & kata sifat" untuk semua level. |
| 3 | **Pasar selalu memakai angka 1–10** (`market_lesson`) di semua level. | A1 seharusnya sudah memakai 11–100, A2 harga ribuan (dan topik "uang" TOPIK 2). |
| 4 | **Jenis latihan terbatas**: pilih arti, pilih kata, dengar kata, pilih balasan, susun kalimat, tirukan. | Belum ada **membaca teks pendek** (papan, pesan, menu), **menyimak dialog** + pertanyaan, **isian tata bahasa** (cloze, konjugasi), **menulis/mengetik**, dan latihan **huruf** (hanzi, kana/kanji, hangeul, hijaiyah). Semua itu keterampilan inti A1–A2. |
| 5 | **Bahasa Indonesia selalu ditampilkan** di semua level. | Di A2 bantuan bahasa ibu seharusnya mulai dikurangi (instruksi dan pilihan dalam bahasa target). |
| 6 | **Ujian**: 20 soal, lulus 85%, hanya dari kata dan kalimat level itu. | Belum berbentuk ujian resmi (bagian menyimak dan membaca, nilai minimum per bagian). |
| 7 | **Konsep di Kamus** hanya berisi judul, pola, penjelasan dan 2 contoh. | Konstitusi kurikulum Titian (`curriculum-constitution.md`) memakai 11 bagian. Versi ringkas untuk game sebaiknya juga punya bentuk negatif, bentuk tanya, dan kesalahan umum. |
| 8 | **24 kata sudah cukup untuk naik level** (dikuasai 80% + poin). | Level bisa dilewati dalam hitungan jam, padahal A1 standar butuh ±90–100 jam belajar terbimbing. |

---

## 5. Benchmark yang diusulkan

Benchmark ini berlaku untuk setiap bahasa di setiap level, mulai Basic–A2 dan seterusnya.

### 5.1 Jumlah isi per level

| | Basic (Pra-A1) | A1 | A2 |
|---|---|---|---|
| Kosakata **baru** — minimum game | ≥ 60 | ≥ 90 (kumulatif ≥ 150) | ≥ 150 (kumulatif ≥ 300) |
| Kosakata — standar penuh (kumulatif) | — | lihat tabel §2 | lihat tabel §2 |
| Butir tata bahasa (konsep Kamus) | 5–8 | 12–20 | 12–20 |
| Kalimat susun (grammar) | 2 per konsep | 2 per konsep | 2 per konsep |
| Frasa siap pakai | 15–20 | 20–30 | 20–30 |
| Situasi percakapan | 3 per topik | 3 per topik | 3 per topik |
| Teks bacaan pendek | 3–5 (papan, label) | 8–10 (pesan, menu, jadwal) | 10–15 (email pendek, pengumuman, cerita pendek) |
| Dialog menyimak + soal | 3–5 | 8–10 | 10–15 |
| Huruf | hijaiyah, kana, hangeul lengkap; ±20 hanzi | ±100 hanzi / ±100 kanji | ±300 hanzi / ±300 kanji |

Minimum game mengikuti daftar resmi terkecil, HSK 2.0: kumulatif 150 kata sampai A1 (= seluruh HSK 1) dan 300 kata sampai A2 (= HSK 1 + HSK 2). "Standar penuh" adalah target jangka panjang.

### 5.2 Syarat kualitas setiap butir

- **Kosakata**: setiap kata tercatat di daftar acuan levelnya (HSK/JLPT/TOPIK/English Vocabulary Profile/buku ajar Arab). Kata yang di atas level tidak boleh masuk; kata dari level di bawah tidak diulang sebagai kata baru.
- **Tata bahasa**: setiap pola kalimat hanya memakai tata bahasa level itu atau di bawahnya, dan kosakata level itu atau di bawahnya.
- **Konsep**: judul, pola, penjelasan, bentuk positif/negatif/tanya, kapan dipakai, kesalahan umum, minimal 2 contoh.
- **Situasi**: jawaban benar dan jawaban salah memakai tata bahasa yang sama levelnya. Jawaban salah harus masuk akal secara bahasa tapi tidak cocok dengan konteks.
- **Topik**: setiap topik di `LADDER` punya kosakata, minimal satu konsep, dan situasi.

### 5.3 Latihan per level

| Jenis latihan | Basic | A1 | A2 |
|---|---|---|---|
| Kosakata (arti ↔ kata, gambar, dengar) | ✔ | ✔ | ✔ |
| Susun kalimat | ✔ | ✔ | ✔ |
| Isian tata bahasa / konjugasi | — | ✔ | ✔ |
| Pilih balasan percakapan | ✔ | ✔ | ✔ |
| Membaca teks pendek + soal | ✔ (papan) | ✔ | ✔ |
| Menyimak dialog + soal | — | ✔ | ✔ |
| Berbicara (tirukan → jawab bebas) | tirukan | tirukan | jawab pendek |
| Menulis (ketik kata → kalimat) | — | kata | kalimat |
| Huruf | ✔ | ✔ | ✔ |
| Bantuan bahasa Indonesia | penuh | penuh | berkurang (instruksi & pilihan dalam bahasa target) |

Kelas mengikuti **topik level** (dari `LADDER`), bukan kategori kata tetap. Pasar memakai angka sesuai level: Basic 1–10, A1 1–100, A2 ratusan dan ribuan.

### 5.4 Ujian lompat level

| | A1 | A2 |
|---|---|---|
| Jumlah soal | 30–40 | 40–50 |
| Bagian | kosakata-tata bahasa · membaca · menyimak | kosakata-tata bahasa · membaca · menyimak |
| Batas lulus | ±70% total **dan** nilai minimum tiap bagian | sama |

Batas 70% lebih ketat dari ujian resmi (60%), karena ujian game melompati level tanpa belajar. Itu sengaja, tapi sebaiknya tetap diputuskan.

---

## 6. Keputusan yang perlu diambil

1. **Target jumlah kosakata**: minimum game (≥150 kata baru per level) atau langsung standar penuh (A2 kumulatif ±1.000–1.500)?
2. **Daftar HSK**: 2.0 (150/300 kata) atau 3.0 (500/1.272 kata)?
3. **Tangga Arab**: setuju dipecah menjadi Mubtadi' 1 / Mubtadi' 2 / Mutawassith 1 / … seperti usulan §3?
4. **Batas lulus ujian**: 70% + minimum per bagian, atau mengikuti ujian resmi (60%)?
5. **Pemeriksa bahasa**: siapa penutur asli/guru yang meninjau tiap bahasa sebelum rilis (terutama Arab, Jepang, Korea)?

## 7. Urutan perbaikan yang diusulkan

1. Putuskan §6.
2. Sesuaikan tangga Arab dan skema data isi. Tambahkan jenis isi baru (teks bacaan, dialog menyimak, isian, huruf) ke `content.json` dan ke pembangun soal.
3. Tulis ulang Basic–A2 per bahasa sesuai §5. Validasi otomatis setiap kata dan tata bahasa terhadap daftar acuannya.
4. Ubah kelas agar mengikuti topik level, pasar mengikuti angka level, dan ujian mengikuti §5.4.
5. Perluas tes isi (`pare_content.rs` → `every_language_has_complete_packs…`) menjadi pemeriksa benchmark ini.
6. Tinjauan penutur asli, lalu B1 ke atas dengan benchmark yang sama.

---

## 8. Keputusan yang dipakai & status penulisan ulang (2026-09-25)

Keputusan §6 yang dipakai (bisa diubah):
1. **Target kosakata**: minimum game — Basic ≥ 60, A1 ≥ 90 baru (kumulatif ≥ 150), A2 ≥ 150 baru (kumulatif ≥ 300).
2. **Mandarin**: HSK 2.0 — Basic + A1 = daftar HSK 1, A2 = daftar HSK 2. Partikel murni (的, 了, 吗, 呢, 吧, 得, 着) diajarkan lewat konsep, bukan sebagai kosakata.
3. **Tangga Arab**: Basic → Mubtadi' 1 (A1) → Mubtadi' 2 (A2) → Mutawassith 1 (B1) → Mutawassith 2 (B2) → Mutaqaddim (C1). Isi B1 lama (wazan, قَدْ, surat/berita) dikeluarkan; akan dipakai lagi saat B1 ditulis.
4. **Ujian lompat level**: 40 soal (kosakata & tata bahasa 16, membaca 12, menyimak 12), lulus ≥ 70% dan tiap bagian ≥ 50%.
5. **Tinjauan penutur asli**: belum. Wajib sebelum rilis publik, terutama Arab, Jepang, dan Korea.

Isi yang sekarang ada (per bahasa: kosakata Basic + A1 + A2):

| Bahasa | Kosakata | Konsep | Kalimat susun | Isian | Frasa | Situasi | Bacaan | Dialog | Huruf |
|---|---|---|---|---|---|---|---|---|---|
| Inggris | 60 + 97 + 150 | 6 · 12 · 12 | 12 · 24 · 24 | 0 · 24 · 24 | 15 · 20 · 20 | 9 · 15 · 15 | 3 · 8 · 10 | 3 · 8 · 10 | — |
| Mandarin | 60 + 90 + 151 | 6 · 12 · 12 | 12 · 24 · 24 | 0 · 24 · 24 | 15 · 20 · 20 | 9 · 15 · 15 | 3 · 8 · 10 | 3 · 8 · 10 | (hanzi lewat kosakata) |
| Jepang | 60 + 100 + 150 | 6 · 12 · 12 | 12 · 24 · 24 | 0 · 24 · 24 | 15 · 20 · 20 | 9 · 15 · 15 | 3 · 8 · 10 | 3 · 8 · 10 | 92 kana |
| Korea | 60 + 91 + 151 | 6 · 12 · 12 | 12 · 24 · 24 | 0 · 24 · 24 | 15 · 20 · 20 | 9 · 15 · 15 | 3 · 8 · 10 | 3 · 8 · 10 | 24 jamo |
| Arab | 61 + 94 + 150 | 6 · 12 · 12 | 12 · 24 · 24 | 0 · 24 · 24 | 15 · 20 · 20 | 9 · 15 · 15 | 3 · 8 · 10 | 3 · 8 · 10 | 28 hijaiyah |

Latihan dan ujian yang sudah mengikuti §5.3–5.4:
- **Jenis soal baru**: membaca teks (teks tampil), menyimak dialog (hanya diputar, teks + arti muncul setelah menjawab), isian tata bahasa, menulis kata (huruf asli atau romanisasi tanpa nada/harakat), membaca huruf (Basic), dan "cara membaca" kata (Mandarin, Jepang, Korea, Arab).
- **Kelas** mengikuti topik: Kosakata (kata + menulis; di Basic: huruf), Makanan / Rutinitas / Perjalanan (kata + situasi + bacaan + dialog + menulis mulai A1), Tata Bahasa (susun kalimat + isian), Pelafalan.
- **Pasar** memakai angka sesuai level (1–10, sampai 100, lalu ratusan dan ribuan).
- **Konsep di Kamus**: pola, penjelasan, kapan dipakai, contoh, bentuk negatif, bentuk tanya, kesalahan umum.

Belum dikerjakan: target "standar penuh" (§2), latihan menulis kalimat (A2 baru menulis kata), dan tinjauan penutur asli.

---

## 9. Kontrak level di atas A2 (rencana, 2026-10-02)

Basic, A1, dan A2 sudah lulus `bun scripts/check-benchmark.ts` dan tes backend `every_language_meets_the_level_benchmark`. Level di atas A2 **belum punya isi**; kontraknya (target kata, huruf, silabus tata bahasa, jumlah bacaan/dialog/tugas menulis) ditulis lebih dulu di `alr/game/src/game/content/benchmark-plan.ts` (`PLANNED_BENCHMARK`) dan divalidasi dengan `bun scripts/check-benchmark-plan.ts` (id tata bahasa unik di semua bahasa & level, kata dan hanzi hanya naik, rentang menulis masuk akal, jumlah materi tidak menyusut). Entri ini sengaja TIDAK ada di `BENCHMARK`, jadi tes yang berjalan tidak terpengaruh. Saat isi sebuah level selesai, pindahkan entrinya ke `BENCHMARK` di `benchmark.ts` — sejak itu skrip dan tes backend menegakkannya.

| Bahasa | Level (CEFR) | Kata kumulatif | Hanzi/kanji kumulatif | Butir tata bahasa |
|---|---|---|---|---|
| Inggris | B1 · B2 · C1 · C2 | 3.000 · 5.000 · 8.000 · 10.000 | — | 28 · 28 · 24 · 20 |
| Mandarin (HSK 3.0, resmi) | HSK 3 · 4 · 5 · 6 (B1 · B2 · C1 · C1+) | 2.245 · 3.245 · 4.316 · 5.456 | 900 · 1.200 · 1.500 · 1.800 | 28 · 28 · 20 · 20 |
| Jepang | N3 · N2 · N1 (B1 · B2 · C1) | 3.750 · 6.000 · 10.000 | 650 · 1.000 · 2.000 | 28 · 26 · 26 |
| Korea | TOPIK 3 · 4 · 5 · 6 (B1 · B2 · C1 · C2) | 3.000 · 5.000 · 7.500 · 10.000 | — | 25 · 25 · 22 · 20 |
| Arab | Mutawassith 1 · 2 · Mutaqaddim (B1 · B2 · C1) | 2.000 · 3.500 · 6.000 | — | 28 · 25 · 22 |

Total: **18 level, ±34.600 kata baru, 443 butir tata bahasa.** Hanya HSK 3.0 yang punya daftar resmi; angka lainnya perkiraan lazim (JLPT dan TOPIK tidak menerbitkan daftar), jadi ubah di `benchmark-plan.ts` bila ingin lain. Bahan per tingkat (A2 = 40/24/14/14/6): B1 50/30/18/16/8 · B2 60/36/22/18/10 · C1 70/40/26/20/12 · C2 80/44/30/22/14 (frasa/situasi/bacaan/dialog/tugas menulis). Tangga Arab kini disejajarkan: Mutawassith 1 = B1, Mutawassith 2 = B2, Mutaqaddim = C1 (tidak ada C2).

**Catatan mutu:** silabus tata bahasa ditulis dari pengetahuan umum tentang tiap kerangka, bukan disalin dari daftar resmi; tinjau terutama silabus Arab, Jepang, dan Korea (dan HSK 5–6 klasik) bersama penutur asli atau pengajar sebelum isi ditulis.

**Audit Basic · A1 · A2 (2026-10-02):** skrip validator yang sama kini juga memeriksa level yang sudah ada. Hasil: semua lulus — id tata bahasa unik dan berawalan kode bahasanya, kata dan hanzi/kanji hanya naik, jumlah bahan dan panjang tulisan tidak menyusut dari satu level ke berikutnya, can-do dan topik terisi. Satu catatan ketebalan ditemukan dan sudah diperbaiki (2026-10-02): silabus Arab A1 dan A2 hanya 20 butir, lebih tipis daripada bahasa lain (Inggris 24/27, Mandarin 32/28, Jepang 28/36, Korea 24/28). Ditambah menjadi **26 (A1)** dan **28 (A2)**: A1 — feminin ـَة, هٰؤُلَاءِ/أُولٰئِكَ, bilangan urut, larangan لَا تَـ, keterangan waktu, كَمْ; A2 — كَانَ + يَفْعَلُ, قَدْ, ism fa'il, عِنْدَمَا/بَعْدَ أَنْ/بَيْنَمَا, أَوْ/أَمْ, أَيّ, غَيْر/بِدُونِ/مِثْل, tujuan (لِـ/كَيْ/حَتَّى). Tiap butir punya konsep, dua contoh, dua kalimat susun, dan dua soal isian (`content/ar/a1-grammar3.ts`, `a2-grammar3.ts`), terdaftar di `benchmark.ts`, `ar.ts`, dan diekspor ke `content.json`; `check-benchmark.ts` dan tes backend lulus. Teks Arab ditulis dengan harakat tetapi **belum ditinjau penutur asli**.

**Audit lanjutan: silabus Inggris, Mandarin, Jepang, Korea (2026-10-02).** Setiap bahasa dibandingkan dengan kerangkanya dan dilengkapi pada bagian yang terlihat kurang. Tiap butir baru punya konsep, dua contoh, dua kalimat susun, dan dua soal isian (`content/<bahasa>/…grammar2.ts` / `a2-grammar4.ts` untuk Jepang), terdaftar di `benchmark.ts` dan paket bahasa, dan diekspor ke `content.json`:

| Bahasa | A1 | A2 |
|---|---|---|
| Inggris | 24 → **27**: countable/uncountable (a/an · some), want/need/like + to + V, yesterday · last · ago | 27 → **31**: possessive pronouns (mine · yours …), reflexive pronouns, Present Perfect for/since, preposisi gerak |
| Mandarin | 32 → **34**: kata arah & tempat (上面 · 里面 · 旁边), 为什么 / 因为 | 28 → **32**: 多 + sifat, 好/难 + kata kerja, 的时候 / 以前 / 以后, kata bantu bilangan lanjut (张 · 件 · 条 · 只 · 双) |
| Jepang | 28 → **30**: とても · あまり · ぜんぜん, いい tak beraturan (よくない · よかった) | 36 → **40**: 〜んです, 〜ことにする / 〜ことになる, 〜くなる / 〜になる, 〜と言う / 〜という |
| Korea | 24 → **27**: -ㅂ니다/-습니다 (formal), 이·그·저, -(으)ㅂ시다 | 28 → **32**: -(으)ㄴ/는 것 같다, -아/어도 되다, -아/어 있다, -기 위해서 |

Hasil: `check-benchmark.ts`, `check-benchmark-plan.ts`, dan tes backend patokan lulus. Isinya ditulis dari pengetahuan umum tentang kerangka masing-masing dan **belum ditinjau penutur asli atau pengajar**. Sebagian bahan yang disebut kerangka resmi mungkin masih ada yang kurang (mis. beberapa pola N4 dan TOPIK 2); silabus ini patokan kerja, bukan daftar resmi lengkap.

