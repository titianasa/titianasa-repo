# Menerapkan perjalanan ke Mandarin, Jepang, Korea, dan Arab

Skenario bahasa Inggris (`en-*.md`) adalah acuan. Dokumen ini menjelaskan apa yang disalin apa adanya, apa yang harus diganti, dan untuk tiap bahasa: cara belajar yang cocok, latar budaya, dan misi mana yang ditukar. Ini **panduan**, bukan skenario jadi: skenario tiap bahasa masih harus ditulis sebagai data (`journey/zh.ts` dan seterusnya) dan ditinjau penutur asli. Saya bukan penutur asli keempat bahasa ini; contoh kalimat dan butir budaya di bawah perlu diperiksa sebelum dipakai.

## 1. Yang tetap sama di semua bahasa

- Susunan: Level → Bab → Pelajaran (Materi → Latihan) → Praktik → Cek → Misi bab → Misi Besar (ADR-0019 §2).
- Aturan: XP tidak berkurang di jalur, syarat lulus bab dan naik level, skor misi dan bintang, Buku Perjalanan (ADR-0019 §3, §16).
- Lima belas jenis langkah, sembilan belas pola misi, lima mode multipemain (ADR-0019 §6, §7, §17).
- Kerangka cerita: pendatang baru → warga → perantau di kota → magang → ke negeri asal bahasanya → profesional → pulang sebagai mentor.
- Sepuluh warga inti dengan satu misi per level, yang ceritanya tumbuh bersama pemain.
- Tujuh blok komputer dan cara dunia terbuka bertingkat.

## 2. Yang disesuaikan

| Hal | Bahasa Inggris | Yang berubah di bahasa lain |
|---|---|---|
| Aksara | Tidak ada bab aksara | Bab pertama Basic adalah aksara dan bunyi (sudah ada di isi Basic: nada & pinyin, kana, Hangeul, hijaiyah) |
| Bantuan baca | Tidak perlu | Pinyin, furigana, romanisasi, dan harakat ditampilkan penuh di awal lalu dikurangi bertahap per level |
| Urutan tata bahasa | Kala dan modal | Mengikuti silabus bahasa itu: partikel dan urutan kata (zh), partikel dan bentuk kata kerja (ja, ko), jenis kata dan pola akar (ar) |
| Kesopanan | Ragam resmi baru penting di B2 | Tingkat tutur adalah inti sejak awal (ko, ja) dan menjadi mekanik misi: pemain memilih tingkat tutur menurut lawan bicara |
| Satuan panjang tulisan | Kata | Aksara untuk zh, ja, ko (sudah begitu di kontrak benchmark) |
| Latar luar negeri | London | Beijing, Tokyo, Seoul (sudah ada di data `COUNTRIES`); Arab belum punya (§6.4) |
| Jumlah level | 7 | zh 7, ko 7, ja 6, ar 6 (§3) |
| Budaya misi | Kafe, pub, debat, West End | Ditukar dengan padanan setempat (tabel per bahasa) |
| Mengetik | Papan ketik biasa | Papan aksara di game sudah ada (pinyin dan romaji dengan kandidat, jamo, hijaiyah) |
| Audio | Aksen Inggris Britania | Petunjuk bahasa wajib di pipeline audio supaya aksara Han tidak dibaca dalam bahasa yang salah |

## 3. Tahap hidup → level tiap bahasa

| Tahap hidup | Inggris | Mandarin | Jepang | Korea | Arab |
|---|---|---|---|---|---|
| Pendatang baru | Basic | Pra-HSK 1 | Pra-N5 | Pra-TOPIK | Pra-Mubtadi' |
| Menjadi warga | A1 | HSK 1 | N5 | TOPIK 1 | Mubtadi' 1 |
| Merantau ke kota | A2 | HSK 2 | N4 | TOPIK 2 | Mubtadi' 2 |
| Magang | B1 | HSK 3 | N3 | TOPIK 3 | Mutawassith 1 |
| Ke negeri asal bahasa | B2 | HSK 4 | N2 | TOPIK 4 | Mutawassith 2 |
| Profesional | C1 | HSK 5 | N1 (babak 1–2 Misi Besar) | TOPIK 5 | Mutaqaddim (babak 1–2 Misi Besar) |
| Duta & mentor | C2 | HSK 6 | N1 (babak 3: pulang sebagai mentor) | TOPIK 6 | Mutaqaddim (babak 3: pulang sebagai mentor) |

Jepang dan Arab punya enam level, jadi dua tahap terakhir digabung: level terakhir memuat kehidupan profesional, dan babak ketiga Misi Besarnya adalah pulang ke Pare sebagai mentor. Isi B2-setara ke atas untuk keempat bahasa belum ditulis (kontraknya ada di `benchmark-plan.ts`).

## 4. Aturan menukar misi

1. **Pertahankan tugasnya, ganti latarnya.** "Memesan makan siang" tetap memesan; yang berubah tempat, menu, dan tata kramanya.
2. **Ikuti konsep babnya.** Misi dipasang pada konsep tata bahasa bab itu. Kalau urutan konsep berbeda, urutan misi ikut berubah. Contoh: misi Rutinitas dipasang di bab *simple present* untuk bahasa Inggris; di Jepang ia dipasang di bab ～ます, di Korea di bab -아요/-어요.
3. **Tambahkan misi yang hanya ada di bahasa itu**, terutama untuk aksara dan tingkat tutur.
4. **Jangan menerjemahkan lelucon dan idiom.** Bab humor, idiom, dan retorika ditulis dari budaya bahasa itu (chengyu, yojijukugo, peribahasa Korea, balaghah).
5. **Papan antarpemain dan sesi bersama** berlaku sama; pemain bertemu pemain lain yang belajar bahasa yang sama.

## 5. Per bahasa

### 5.1 Mandarin

**Cara belajar yang cocok**

| Prinsip | Wujud di game |
|---|---|
| Nada dan pinyin dulu, sebelum kata | Bab 1 Basic: empat nada, pasangan minimal, lalu perubahan nada (nada ketiga, 不, 一). Tiap butir menyimak di level awal menanyakan nada |
| Hanzi lewat komponen dan frekuensi; mengenali dulu, menulis kemudian | Pelajaran "aksara" tersendiri: komponen, lalu kata yang memakainya. Kontrak: 300 aksara di HSK 1 sampai 1.800 di HSK 6 |
| Pinyin dikurangi bertahap | Pra-HSK–HSK 1: selalu tampil. HSK 2: hanya untuk kata baru. HSK 3: saat diketuk. HSK 4 ke atas: tidak tampil |
| Tata bahasa = urutan kata dan partikel, bukan perubahan bentuk | Butir "susun kalimat" menjadi jenis utama; kata bantu bilangan, 了 / 过 / 着, komplemen hasil dan arah, 把 dan 被 |
| Kata bantu bilangan dipelajari bersama bendanya | Misi belanja selalu meminta jumlah + kata bantu bilangan + benda |
| Ungkapan empat aksara di level atas | Bab chengyu di HSK 5–6 menggantikan bab idiom dan alusi |

**Latar dan tokoh.** Kampung Mandarin (tokoh yang sudah ada: 林老师, 小王 di 茶馆, 陈师傅, 李阿姨, 张叔叔). Luar negeri: Beijing. Panggilan kekerabatan untuk orang yang bukan keluarga (阿姨, 叔叔, 师傅, 老师) dipakai sejak Basic.

**Misi yang ditukar**

| Misi bahasa Inggris | Padanan Mandarin |
|---|---|
| Makan siang pertama (kafe) | Memesan teh dan 饺子 di 茶馆 dan 饭馆; menu tanpa gambar |
| Belanja pertama | Menawar di pasar; membayar dengan memindai kode di ponsel tiruan |
| Kenalan dengan tetangga | Bertukar nama dan marga; menanyakan 您贵姓 kepada orang yang lebih tua |
| Pesta kampung (A1) | Malam Tahun Baru Imlek: makan bersama, 红包, ucapan selamat |
| Janji temu | Janji lewat pesan singkat ala aplikasi obrolan; tanggal dan jam dengan urutan besar ke kecil |
| Liburan pertama (A2) | Membeli tiket kereta cepat; Festival Pertengahan Musim Gugur |
| Reporter Kampung (B1) | Sama; ditambah mengutip dengan 说 dan 表示 |
| Rapat balai kota | Rapat warga 居委会; menolak secara tidak langsung demi menjaga muka |
| Kontrak flat (HSK 4) | Menyewa kamar di Beijing; pendaftaran tempat tinggal |
| Debat, salon, retorika | Diskusi dengan chengyu dan kutipan klasik; pidato perjamuan dan bersulang |
| Penerjemah (tahap akhir) | Menerjemahkan Indonesia ↔ Mandarin; juru bahasa untuk rombongan dagang |

**Yang khas dan perlu ditambah:** pelajaran nada di tiap bab Basic–HSK 1; langkah "pilih aksara yang benar di antara yang mirip"; langkah mengetik dengan pinyin lalu memilih hanzi; tata krama meja makan dan bersulang sebagai dialog.

### 5.2 Jepang

**Cara belajar yang cocok**

| Prinsip | Wujud di game |
|---|---|
| Kana dulu, sampai lancar | Bab 1 Basic: hiragana lalu katakana (92 huruf sudah ada di isi Basic). Tidak ada romaji setelah Basic |
| Kanji lewat kata, dengan furigana yang dikurangi | N5: furigana selalu. N4: hanya kanji baru. N3: saat diketuk. N2–N1: tidak ada. Kontrak: 100 kanji di N5 sampai 2.000 di N1 |
| Partikel dan bentuk kata kerja adalah tulang punggung | Butir "pilih partikel" dan "ubah bentuk" (ます, て, ない, bentuk biasa) di tiap bab N5–N4 |
| Sopan dulu, biasa kemudian, lalu keigo | です/ます sejak Basic; bentuk biasa di N4; 尊敬語 dan 謙譲語 di N3–N2, dipakai di misi kantor dan layanan |
| Mendengar dengan aizuchi | Di dialog, pemain memilih tanggapan pendengar (はい, そうですか, へえ) pada saat yang tepat |
| Kata bantu bilangan | Misi belanja dan pesan makanan selalu memakainya |

**Latar dan tokoh.** Kampung Jepang (ゆきせんせい, けんた di カフェ, けんじ, たなかさん di コンビニ, やまださん). Luar negeri: Tokyo. Hubungan senpai–kōhai dan uchi–soto menentukan tingkat tutur di tiap dialog.

**Misi yang ditukar**

| Misi bahasa Inggris | Padanan Jepang |
|---|---|
| Makan siang pertama | Membeli tiket makan di mesin kedai ramen; いただきます dan ごちそうさま |
| Belanja pertama | Belanja di コンビニ: menjawab pertanyaan kasir yang cepat (kantong, dipanaskan, kartu poin) |
| Kenalan dengan tetangga | Salam pindahan dengan buah tangan; よろしくお願いします |
| Pesta kampung (N5) | Hanami atau festival musim panas: membagi tugas, yukata, kedai |
| Kartu pos untuk rumah | Menulis 年賀状 (kartu tahun baru) dengan ungkapan baku |
| Hari pertama kerja (N4) | Kerja paruh waktu di コンビニ; bahasa layanan いらっしゃいませ, 少々お待ちください |
| Kolom konsumen (N3) | Meminta maaf dan menyampaikan keluhan dengan sangat halus |
| Lamaran magang | エントリーシート dan wawancara dengan keigo |
| Dunia kerja (N2) | 報告・連絡・相談: melapor, mengabari, berkonsultasi kepada atasan; email bisnis dengan salam musim |
| Negosiasi, konferensi pers (N1) | Rapat dengan nemawashi; menolak tanpa berkata "tidak" |
| Humor & ironi | Rakugo, permainan kata, dan apa yang tidak diucapkan |

**Yang khas dan perlu ditambah:** mekanik **pilih tingkat tutur** (teman, pelanggan, atasan) di tiap dialog mulai N4; pelajaran kanji per bab; membaca tegak (vertikal) di N2–N1; bertukar kartu nama sebagai langkah `dialog`.

### 5.3 Korea

**Cara belajar yang cocok**

| Prinsip | Wujud di game |
|---|---|
| Hangeul dalam beberapa hari pertama | Bab 1 Basic (24 huruf sudah ada); menyusun suku kata dari jamo; tidak ada romanisasi setelah Basic |
| Ejaan tidak sama dengan bunyi | Jalur pelafalan berisi aturan perubahan bunyi: 받침, penyambungan, nasalisasi, pengerasan |
| Tingkat tutur dan honorifik sejak awal | 해요체 dulu; 합쇼체 untuk pengumuman dan kantor; 반말 di TOPIK 3; honorifik -(으)시- dan kosakata hormat (드시다, 계시다) di TOPIK 2–3 |
| Dua sistem angka | Angka Sino-Korea untuk uang, tanggal, menit (sudah di Basic); angka asli Korea untuk jumlah, umur, jam (TOPIK 1). Misi janji memakai keduanya sekaligus: 세 시 삼십 분 |
| Akhiran kata kerja dan partikel | Butir "pilih akhiran" (-고, -아서, -(으)니까, -는데) dan "susun" dengan urutan SOV |

**Latar dan tokoh.** Kampung Korea (박쌤, 민수 di 카페, 이 셰프, 김 씨 di 편의점, 이 씨; 포장마차 sudah ada). Luar negeri: Seoul. Umur dan kedudukan menentukan tingkat tutur, jadi menanyakan umur adalah bagian dari perkenalan.

**Misi yang ditukar**

| Misi bahasa Inggris | Padanan Korea |
|---|---|
| Kenalan dengan tetangga | Perkenalan dengan menanyakan umur, lalu menentukan cara memanggil (언니, 오빠, 선배, 씨) |
| Makan siang pertama | Memesan di 식당 dan 포장마차; lauk pendamping, air ambil sendiri |
| Makan bersama | Tata krama makan: yang tua mulai dulu, menuang minum dengan dua tangan |
| Pesta kampung (TOPIK 1) | 추석 atau 설날: 세배, makanan hari raya, ucapan selamat |
| Janji temu | Janji lewat pesan ala aplikasi obrolan; dua sistem angka |
| Baju untuk pesta | Sama, ditambah 한복 untuk hari raya |
| Hari pertama kerja (TOPIK 2) | Kerja paruh waktu di 편의점 atau kafe; bahasa layanan |
| Malam Cerita | 노래방 atau malam cerita; lirik lagu sebagai bahan simakan |
| Reporter (TOPIK 3) | Sama; kalimat tak langsung -다고 하다 |
| Dunia kerja (TOPIK 4–5) | Jenjang jabatan, 회식, laporan kepada atasan dengan 합쇼체 |
| Surat untuk rumah, tulisan tamu | Surat penggemar atau ulasan drama, karena budaya pop adalah alasan belajar bagi banyak pemain |
| Debat, pidato (TOPIK 6) | Debat dan presentasi dengan ragam tulis resmi (-ㄴ다 / -는다) |

**Yang khas dan perlu ditambah:** mekanik **pilih tingkat tutur** di tiap dialog sejak TOPIK 1; butir "sebutkan angka dengan sistem yang benar"; butir perubahan bunyi (dengar lalu pilih ejaan).

### 5.4 Arab

**Cara belajar yang cocok**

| Prinsip | Wujud di game |
|---|---|
| Aksara dan arah tulis dulu | Bab 1 Basic: 28 huruf hijaiyah (sudah ada), bentuk huruf di awal, tengah, dan akhir, arah kanan ke kiri |
| Harakat dikurangi bertahap | Pra-Mubtadi'–Mubtadi' 2: harakat penuh. Mutawassith 1: hanya pada kata baru dan kata yang rawan salah baca. Mutawassith 2 ke atas: tanpa harakat |
| Kosakata lewat akar dan pola | Pelajaran "keluarga akar": ك ت ب → كِتَاب, كَاتِب, مَكْتَب, مَكْتَبَة. Wazan sudah ada di silabus Mutawassith 1 |
| Fusha sebagai dasar, ragam sehari-hari dikenalkan | Membaca, menulis, berita, dan pidato dalam fusha. Mulai Mutawassith 1, misi di luar negeri menyertakan salam dan ungkapan ragam setempat sebagai simakan, tidak sebagai bahan ujian |
| Kesesuaian jenis dan jumlah | Butir "sesuaikan": mudzakkar dan muannats, mutsanna, jamak taksir, idhafah |
| Jembatan dari bahasa Indonesia | Banyak kata serapan (kursi, kitab, waktu, kabar) dan, bagi banyak pemain, bacaan Al-Qur'an. Materi menandai kata yang sudah dikenal dan yang maknanya bergeser |

**Latar dan tokoh.** Kampung Arab (الأستاذ أحمد, عمر di مقهى, عم سعيد, أم سارة, أبو علي; masjid sudah ada sebagai penanda kampung). Kunyah (أبو …, أم …) dipakai sebagai panggilan hormat sejak Basic.

**Negeri tujuan belum ditentukan** (`LANG_COUNTRY` tidak punya entri Arab). Usul: **Kairo**. Alasannya: banyak pelajar Indonesia belajar di sana, jadi ceritanya dekat dengan pemain; ragam Mesir luas dipahami lewat film dan lagu; dan kota itu memberi latar kampus, penerbit, dan media untuk tahap akhir. Pilihan lain: Madinah atau Makkah sebagai bab perjalanan (umrah) di Mutawassith, yang bisa digabung dengan pilihan mana pun. Ini keputusan user (ADR-0019 §15.15).

**Misi yang ditukar**

| Misi bahasa Inggris | Padanan Arab |
|---|---|
| Kenalan dengan tetangga | Salam berlapis dan jawabannya (السلام عليكم, كيف الحال, الحمد لله); menanyakan kabar keluarga |
| Makan siang pertama | Jamuan: ditawari teh atau kopi dan kurma; cara menerima dan menolak dengan sopan |
| Belanja pertama | Menawar di سوق; angka Arab-Hindi (٠–٩) pada harga |
| Pesta kampung (Mubtadi' 1) | Undangan buka puasa atau Idulfitri: ucapan, hidangan, tamu |
| Janji temu | Janji dengan إن شاء الله; hari dan tanggal, termasuk kalender hijriah |
| Baju untuk pesta | Pakaian untuk hari raya; kesesuaian jenis kata sifat warna |
| Liburan pertama (Mubtadi' 2) | Perjalanan umrah atau ke Kairo: bandara, hotel, petunjuk arah |
| Reporter (Mutawassith 1) | Berita pendek gaya siaran; قال إنّ |
| Rapat balai kota | Musyawarah di majelis; menyampaikan keberatan dengan hormat |
| Debat, retorika (Mutaqaddim) | Khutbah dan pidato; balaghah (tasybih, isti'arah, saj') menggantikan retorika Yunani-Latin |
| Membaca sastra | Syair klasik dan modern; kutipan yang sudah dikenal pembaca |
| Penerjemah | Menerjemahkan Indonesia ↔ Arab; juru bahasa untuk rombongan |

**Yang khas dan perlu ditambah:** antarmuka kanan-ke-kiri untuk kartu misi dan jendela komputer; butir "beri harakat pada kata ini" sebagai latihan baca; langkah "kenali akar" di tiap bab mulai Mubtadi' 2; kaligrafi sebagai kegiatan kosmetik.

## 6. Urutan kerja untuk tiap bahasa

1. Salin bentuk data dari `journey/en.ts`; pakai `types.ts` yang sama.
2. Tulis daftar tokoh, tempat, dan aplikasi (`<bahasa>/world.ts`): pertahankan lima tokoh kampung yang sudah ada di `zones.ts`, tambahkan lima warga inti lain dan tokoh tiap tingkat.
3. Untuk tiap level yang isinya sudah ada (Basic sampai B1-setara): bagi konsep silabus ke bab menurut urutan belajar bahasa itu, bagi anggaran kata per kategori, bagi bahan Praktik. Jalankan `bun scripts/journey.ts` (skrip perlu diperluas supaya memeriksa lebih dari satu bahasa) sampai lolos.
4. Pasang satu misi per bab dengan aturan di §4; tulis sepuluh misi warga per level.
5. Tambahkan bab aksara dan jalur bantuan baca (§2).
6. Tinjauan penutur asli untuk kalimat kunci, tata krama, dan nama.
7. Baru setelah itu misi dibangun dan audio direkam.

## 7. Yang belum pasti

- Kecocokan pola misi dengan tiap bahasa belum diuji; beberapa pola (Negosiator, Kritikus) mungkin perlu aturan budaya tambahan.
- Mekanik "pilih tingkat tutur" untuk Jepang dan Korea belum dirancang rinci: bagaimana pilihan yang salah dinilai dan bagaimana NPC bereaksi.
- Pengenalan ragam sehari-hari untuk bahasa Arab adalah pilihan rancangan saya; apakah ragam Mesir, Syam, atau tidak sama sekali, bergantung pada negeri tujuan yang dipilih.
- Jadwal pengurangan pinyin, furigana, dan harakat di atas adalah usul; ladder game sekarang hanya menyebut "membaca teks tanpa pinyin" di HSK 4 dan "membaca teks tanpa harakat" di Mutawassith 1.
