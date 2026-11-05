# Kampung Bahasa Pare: 30 hari konten (1–30 November 2026)

Untuk akun **@pare.titianasa** (Instagram dan TikTok). Satu postingan per hari, pukul 19.00 WIB, melanjutkan batch Oktober yang berakhir 31 Oktober. Fokus **Kampung Inggris** dan bahasa Inggris. Kampung bahasa lain tidak dibahas sama sekali, karena belum siap.

- Gambar Instagram 1080×1350: `instagram/`. Gambar TikTok mode foto 1080×1920: `tiktok/`.
- Nomor file sama dengan nomor postingan. Carousel berupa folder, urut `-1`, `-2`, dan seterusnya.
- Isi slide ada di `src/posts.ts`. Ubah di sana, lalu `bun build.ts` dan `bun render.ts` di folder `src/`.
- Tangkapan layar 3D dibuat dengan `game/scripts/video/social-shots.ts` (cara pakainya di komentar skrip).

## Pilar konten

| Pilar | Isi | Postingan |
|---|---|---|
| Dunia 3D | Tur, Lemari, peta, Miss Kate, ngobrol dengan warga | 1, 2, 7, 14, 15, 21, 30 |
| Seri level | Topik dan kemampuan tiap level, dari `content.json` | 3, 9, 16, 23, 28 |
| Misi | Cerita misi tiap level, dari `missions.json` | 5, 11, 18, 25 |
| Kesalahan umum | Pasangan salah dan benar dari bab tata bahasa | 6, 12, 19, 26 |
| Bahasa Inggris praktis | Kalimat kerja paruh waktu (WHV) dan melayani tamu (kapal pesiar) | 13, 20 |
| Infografik tes | TOEFL iBT, TOEFL ITP, IELTS, PTE Academic, TOEIC | 4, 10, 17, 24, 27, 29 |
| Tebak-tebakan | Soal di slide 1, jawaban di slide 2 | 8, 22 |

## Sebelum tayang

| Syarat | Berlaku untuk |
|---|---|
| Fitur ngobrol langsung dengan warga sudah di-deploy (migrasi `0107_pare_npc_chat.sql`) dan sudah dicoba di pare.titianasa.com. | Postingan 14, juga slide 5 postingan 24 dan postingan 30 |
| Versi game yang difoto sudah tayang di pare.titianasa.com, termasuk perbaikan balon chat dan nama warga di kotak chat (belum di-commit). | Semua postingan bergambar 3D |
| Fakta tes dicek ulang ke situs resmi bila tayang lewat dari Desember 2026. | 4, 10, 17, 24, 27, 29 |

Bila fitur ngobrol dengan warga belum di-deploy pada 14 November, tukar postingan 14 dengan postingan 22, lalu geser postingan 14 ke tanggal 22.

## Kalender

| No | Tanggal | Hari | Format | Judul | File |
|---|---|---|---|---|---|
| 1 | 1 Nov | Minggu | Single | Kampung Bahasa sekarang 3D | `01-kampung-bahasa-sekarang-3d.png` |
| 2 | 2 Nov | Senin | Carousel 6 | Tur Kampung Bahasa versi 3D | `02-tur-kampung-bahasa-3d/` |
| 3 | 3 Nov | Selasa | Carousel 5 | Level Basic: mulai dari nol | `03-level-basic/` |
| 4 | 4 Nov | Rabu | Carousel 6 | TOEFL, IELTS, PTE, TOEIC: bedanya apa? | `04-toefl-ielts-pte-toeic-bedanya/` |
| 5 | 5 Nov | Kamis | Carousel 6 | Misi: minggu pertamamu di Kampung Inggris | `05-misi-minggu-pertama/` |
| 6 | 6 Nov | Jumat | Carousel 7 | 5 kesalahan A1 yang sering banget | `06-salah-kaprah-a1/` |
| 7 | 7 Nov | Sabtu | Carousel 4 | Pilih karakter di Lemari | `07-pilih-karakter-di-lemari/` |
| 8 | 8 Nov | Minggu | Carousel 2 | Tebak: a, an, atau some? | `08-tebak-a-atau-some/` |
| 9 | 9 Nov | Senin | Carousel 5 | Level A1: cerita sehari-hari | `09-level-a1/` |
| 10 | 10 Nov | Selasa | Carousel 5 | TOEFL iBT format baru | `10-toefl-ibt-format-baru/` |
| 11 | 11 Nov | Rabu | Carousel 6 | Misi A1: tinggal bareng keluarga Brown | `11-misi-a1-keluarga-brown/` |
| 12 | 12 Nov | Kamis | Carousel 7 | 5 kesalahan A2 yang bikin kebalik | `12-salah-kaprah-a2/` |
| 13 | 13 Nov | Jumat | Carousel 7 | 5 kalimat buat kerja paruh waktu | `13-kalimat-kerja-paruh-waktu/` |
| 14 | 14 Nov | Sabtu | Carousel 5 | Ngobrol langsung dengan warga | `14-ngobrol-langsung-dengan-warga/` |
| 15 | 15 Nov | Minggu | Carousel 4 | Peta Kampung Inggris | `15-peta-kampung-inggris/` |
| 16 | 16 Nov | Senin | Carousel 5 | Level A2: keluar dari zona nyaman | `16-level-a2/` |
| 17 | 17 Nov | Selasa | Carousel 5 | IELTS sekilas | `17-ielts-sekilas/` |
| 18 | 18 Nov | Rabu | Carousel 6 | Misi A2: gaji pertama, liburan pertama | `18-misi-a2-gaji-pertama/` |
| 19 | 19 Nov | Kamis | Carousel 7 | 5 kesalahan level menengah (B1) | `19-salah-kaprah-b1/` |
| 20 | 20 Nov | Jumat | Carousel 6 | Kalimat sopan buat melayani tamu | `20-kalimat-sopan-melayani-tamu/` |
| 21 | 21 Nov | Sabtu | Carousel 3 | Kenalan sama Miss Kate | `21-kenalan-sama-miss-kate/` |
| 22 | 22 Nov | Minggu | Carousel 2 | Tebak: interested on, in, atau at? | `22-tebak-preposisi/` |
| 23 | 23 Nov | Senin | Carousel 5 | B1 & B2: mulai berpendapat | `23-level-b1-dan-b2/` |
| 24 | 24 Nov | Selasa | Carousel 5 | PTE Academic sekilas | `24-pte-academic-sekilas/` |
| 25 | 25 Nov | Rabu | Carousel 6 | Misi B1 & B2: dari Pare ke London | `25-misi-b1-b2-dari-pare-ke-london/` |
| 26 | 26 Nov | Kamis | Carousel 7 | Kesalahan yang masih lolos di level atas | `26-salah-kaprah-b2-c1/` |
| 27 | 27 Nov | Jumat | Carousel 5 | TOEFL ITP sekilas | `27-toefl-itp-sekilas/` |
| 28 | 28 Nov | Sabtu | Carousel 6 | C1 & C2: puncaknya | `28-level-c1-c2-puncaknya/` |
| 29 | 29 Nov | Minggu | Carousel 5 | TOEIC sekilas | `29-toeic-sekilas/` |
| 30 | 30 Nov | Senin | Single | Basic sampai C2, di satu tempat | `30-basic-sampai-c2-satu-jalur.png` |

## Tagar

Tetap di setiap postingan: `#KampungBahasaPare #KampungInggrisPare #BelajarBahasaInggris #TitianAsa`

Tambahan per pilar (pilih 2–4):

| Pilar | Tagar |
|---|---|
| Dunia 3D | `#Game3D #BelajarSambilJalanJalan #KampungInggris` |
| Seri level dan misi | `#CEFR #BelajarDariNol #EnglishLevel` |
| Kesalahan umum dan tebak-tebakan | `#GrammarBahasaInggris #TipsBahasaInggris #EnglishGrammar` |
| Bahasa Inggris praktis | `#WorkingHolidayVisa #PejuangWHV #KapalPesiar #EnglishForWork` |
| Infografik tes | `#TOEFL #IELTS #PTEAcademic #TOEIC #PejuangBeasiswa` |

## Caption

Caption Instagram di bawah judul tiap postingan. Baris **TikTok** adalah versi pendeknya.

### 1. Kampung Bahasa sekarang 3D
Kampung Bahasa sekarang 3D! 🎉

Lapangan senja, Kampung Inggris, odong-odong, sepeda ontel, dan teman belajar yang lalu-lalang. Semuanya bisa kamu datangi sekarang.

Yang nggak berubah: jalur belajar bahasa Inggrisnya tetap lengkap, Basic sampai C2.

Coba sekarang, gratis, langsung dari browser 👉 pare.titianasa.com

**TikTok:** Kampung Bahasa sekarang 3D 🎉 Belajar bahasa Inggrisnya tetap Basic sampai C2. pare.titianasa.com

### 2. Tur Kampung Bahasa versi 3D
Jalan-jalan dulu sebelum belajar, yuk 🚶‍♀️

🏫 Kampung Inggris: semua warganya ngomong bahasa Inggris
🚲 Sepeda ontel buat keliling
🚃 Odong-odong, duduk bareng warga lain
🍜 Jajan pecel, bakso, es degan

Tapi ingat, belajarnya tetap serius 😄 Kamu paling penasaran ke mana dulu?

pare.titianasa.com

**TikTok:** Tur singkat Kampung Bahasa versi 3D. Kamu mau ke mana dulu? pare.titianasa.com

### 3. Level Basic: mulai dari nol
Seri level, bagian 1 dari 7: **Basic** (setara Pra-A1).

Di sini kamu belajar huruf dan bunyi, sapaan, angka, makanan, rutinitas, dan arah. Habis Basic, kamu sudah bisa menyapa, memesan makanan sederhana, dan menanyakan arah.

Kata pertama yang paling sering kepakai? **Excuse me.** 😉

Mulai dari nol di pare.titianasa.com

**TikTok:** Level Basic: 6 bab pertama buat yang mulai dari nol. pare.titianasa.com

### 4. TOEFL, IELTS, PTE, TOEIC: bedanya apa?
Bingung bedain tes bahasa Inggris? Ini rangkumannya 📊

✅ Skor dan lamanya
✅ Bagian yang diuji
✅ Biasanya dipakai untuk apa

Satu hal jujur: Kampung Bahasa bukan kelas persiapan tes. Tapi fondasinya sama, yaitu tata bahasa, kosakata, membaca, mendengar, dan menulis, dan itu yang kamu bangun dari Basic sampai C2.

Format tes bisa berubah. Selalu cek situs resminya sebelum daftar.

Simpan postingan ini buat nanti 📌 pare.titianasa.com

**TikTok:** TOEFL, IELTS, PTE, TOEIC: skor, lama, dan bedanya dalam satu geser. pare.titianasa.com

### 5. Misi: minggu pertamamu di Kampung Inggris
Minggu pertama di Kampung Inggris itu kayak gini 👇

1️⃣ Kenalan dengan tiga tetangga dan isi kartu nama mereka
2️⃣ Belanja pertama pakai uang saku sendiri
3️⃣ Pesan minuman di kafe, lalu makan di warung
4️⃣ Bantu Anna, turis yang tersesat

Penutupnya: sehari penuh tanpa bantuan Miss Kate, lalu pesta sambutan dari warga 🎉

Mulai misi pertamamu di pare.titianasa.com

**TikTok:** Minggu pertamamu di Kampung Inggris: kenalan, belanja, makan siang, bantu turis. pare.titianasa.com

### 6. 5 kesalahan A1 yang sering banget
Pernah nulis salah satu dari ini? Nggak apa-apa, semua orang pernah 😅

❌ She have a bike → ✅ She has a bike
❌ I like swim → ✅ I like swimming
❌ How old you are? → ✅ How old are you?
❌ Let's to go! → ✅ Let's go!
❌ I want a water → ✅ I want some water

Kamu paling sering salah yang nomor berapa? Tulis di komentar 👇

Latihan sampai terbiasa di pare.titianasa.com

**TikTok:** 5 kesalahan bahasa Inggris level A1 yang sering banget. Kamu yang mana? pare.titianasa.com

### 7. Pilih karakter di Lemari
Pilih karakter yang sesuai denganmu 👗

Ada karakter siap pakai, putra dan putri. Pilih satu, lalu atur rambut, penutup kepala, baju, sampai tas. Mau tampil kayak anak Pare? Ada batik, peci, jilbab, seragam sekolah, dan pramuka.

Coba apa saja gratis. Karaktermu nanti tampil di Kampung Bahasa, lengkap dengan nama dan levelmu.

pare.titianasa.com

**TikTok:** Pilih karakter yang sesuai denganmu, lalu atur gayanya sendiri. pare.titianasa.com

### 8. Tebak: a, an, atau some?
Tebak dulu sebelum geser 👀

**I want ___ water.**
A. a · B. an · C. some

Tulis jawabanmu di komentar, lalu geser ke slide 2 buat cek!

pare.titianasa.com

**TikTok:** I want ___ water. Isi apa? Jawab di komentar 👇

### 9. Level A1: cerita sehari-hari
Seri level, bagian 2 dari 7: **A1**.

Di A1 kamu mulai pakai kalimat utuh: cerita keluarga, rumah, sekolah, kerja, dan cuaca. Habis A1, kamu bisa bikin janji ketemu, tanya jam dan harga, dan baca pesan atau menu sederhana.

Contohnya: **I always get up at six.** (Saya selalu bangun jam enam.)

Sudah merasa bisa? Ikut ujian lompat level di pare.titianasa.com

**TikTok:** Level A1: mulai cerita sehari-hari dalam bahasa Inggris. pare.titianasa.com

### 10. TOEFL iBT format baru
Pejuang TOEFL, sudah tahu? 📢

Sejak Januari 2026, TOEFL iBT pakai skor **1 sampai 6**. Skor totalnya rata-rata empat bagian, dibulatkan ke setengah poin. Selama masa transisi dua tahun, kamu juga dapat skor setara skala lama 0–120.

Bagiannya tetap empat: Reading, Listening, Writing, Speaking. Sediakan sekitar 2 jam.

Sumber: ets.org (dicek Oktober 2026). Simpan dan bagikan ke temanmu yang lagi persiapan 📌

pare.titianasa.com

**TikTok:** TOEFL iBT sekarang pakai skor 1–6. Ini rinciannya. pare.titianasa.com

### 11. Misi A1: tinggal bareng keluarga Brown
Di level A1, kamu pindah ke rumah keluarga Brown 🏠

👨‍👩‍👧 Kenali semua anggota keluarganya
🍳 Gantikan pelayan diner Chef Oliver
👕 Pilihkan baju pesta buat Jack
🔍 Bantu Officer Jones mencari tas Emma yang hilang

Puncaknya: kamu jadi panitia pesta tahunan Kampung Inggris 🎉

pare.titianasa.com

**TikTok:** Level A1: tinggal bareng keluarga Brown di Kampung Inggris. pare.titianasa.com

### 12. 5 kesalahan A2 yang bikin kebalik
Sering lolos di chat, tapi bikin artinya beda 😬

❌ I didn't finish yet → ✅ I haven't finished yet
❌ If it will rain → ✅ If it rains
❌ for learn English → ✅ to learn English
❌ I enjoy to cook → ✅ I enjoy cooking
❌ mustn't (padahal maksudnya "tidak perlu") → ✅ don't have to

Yang terakhir paling sering bikin salah paham. Kamu baru tahu yang mana?

pare.titianasa.com

**TikTok:** 5 kesalahan bahasa Inggris level A2. Nomor 5 sering bikin salah paham. pare.titianasa.com

### 13. 5 kalimat buat kerja paruh waktu
Buat pejuang WHV dan yang mau kerja paruh waktu 💼

1. Could you do me a favour? (Bisa minta tolong?)
2. Would you mind waiting? (Keberatan menunggu?)
3. Let me check. (Saya cek dulu.)
4. It takes about twenty minutes. (Kira-kira dua puluh menit.)
5. Keep the change. (Ambil saja kembaliannya.) Yang ini biasanya dari pelanggan 😄

Semuanya dari level A2, tempat kamu kerja paruh waktu di toko pakaian Mal Kota.

Simpan dulu 📌 pare.titianasa.com

**TikTok:** 5 kalimat bahasa Inggris buat kerja paruh waktu. Simpan dulu! pare.titianasa.com

### 14. Ngobrol langsung dengan warga
Fitur baru: sekarang kamu bisa ngobrol langsung dengan warga Kampung Inggris 💬

Dekati warga, ketuk, lalu tulis dalam bahasa Inggris. Mr. Smith, Tom, Chef Oliver, dan warga lain membalas di atas kepalanya, lengkap dengan artinya. Jawabannya dibantu AI dan disesuaikan dengan levelmu.

Obrolanmu tersimpan di ruang chat, jadi bisa dilanjut kapan saja.

Latihan ngobrol tanpa malu di pare.titianasa.com

**TikTok:** Sekarang bisa ngobrol langsung dengan warga Kampung Inggris. Mereka membalas! pare.titianasa.com

### 15. Peta Kampung Inggris
Biar nggak nyasar di Kampung Inggris 🗺️

🏫 English Class Academy: Miss Kate
📚 Library: Mr. Smith
☕ Café: Tom
🍳 Diner: Chef Oliver
🛒 Minimart: Mrs. Brown
🧺 Laundry: Mr. Green
🏨 Guesthouse: Mrs. Hughes
✉️ Post Office: Mr. Patel

Hampir tiap warga punya misi sampingan sendiri. Sudah sapa siapa saja?

pare.titianasa.com

**TikTok:** Peta Kampung Inggris: siapa di mana. pare.titianasa.com

### 16. Level A2: keluar dari zona nyaman
Seri level, bagian 3 dari 7: **A2**.

Belanja, ke dokter, kerja, liburan. Di A2 bahasa Inggrismu dipakai buat urusan beneran. Kamu juga mulai menulis email dan cerita pendek, lalu dapat masukan dari penilai AI ✍️

Contohnya: **I'm flying to Jakarta on Friday.**

pare.titianasa.com

**TikTok:** Level A2: bahasa Inggris buat belanja, ke dokter, kerja, dan liburan. pare.titianasa.com

### 17. IELTS sekilas
IELTS dalam 5 slide 📊

⏱️ 2 jam 45 menit, empat bagian
🎧 Listening 40 soal · 📖 Reading 40 soal · ✍️ Writing 2 tugas · 🗣️ Speaking tatap muka
🎓 Academic untuk kuliah, 🧳 General Training untuk kerja, pelatihan, atau migrasi
🔢 Skor band 0–9, bisa setengah band

Sumber: ielts.org (dicek Oktober 2026). Cek lagi sebelum daftar ya.

Tag teman yang lagi berjuang IELTS 👇 pare.titianasa.com

**TikTok:** IELTS sekilas: bagian, waktu, dan cara menilainya. pare.titianasa.com

### 18. Misi A2: gaji pertama, liburan pertama
Di level A2, kamu keluar dari Kampung Inggris dan mengurus semuanya sendiri 🏙️

👀 Jadi saksi kejadian di depan Mal Kota
🎁 Pilih hadiah ulang tahun dengan anggaran Rp100.000
🩺 Jelaskan keluhanmu ke Dokter Rina
🧳 Selamatkan liburan yang kacau

Puncaknya: pakai gaji pertamamu untuk mengajak keluarga Brown berlibur ✈️

pare.titianasa.com

**TikTok:** Level A2: kerja, gaji pertama, lalu liburan pertama. pare.titianasa.com

### 19. 5 kesalahan level menengah (B1)
Sudah lancar ngobrol? Coba cek lima ini 👇

❌ I have seen him yesterday → ✅ I saw him yesterday
❌ If I would have money → ✅ If I had money
❌ He said me → ✅ He told me
❌ where is the station? (di pertanyaan tak langsung) → ✅ where the station is
❌ She made me to wait → ✅ She made me wait

Kalau kamu lolos semua, level B1 sudah dekat 😎

pare.titianasa.com

**TikTok:** 5 kesalahan bahasa Inggris yang masih sering muncul di level B1. pare.titianasa.com

### 20. Kalimat sopan buat melayani tamu
Buat calon kru kapal pesiar dan anak hospitality 🛳️

🍽️ Certainly. Would you like it mild or spicy?
📸 Would you mind taking a photo of us, please?
🙏 We apologise for any inconvenience this may have caused.
📧 I would be grateful if you could confirm the date.

Ingat polanya: **Would you mind + V-ing**, bukan "to + V".

Semuanya dari bab layanan dan bertanya dengan sopan di level B1 dan B2.

pare.titianasa.com

**TikTok:** Kalimat sopan bahasa Inggris buat melayani tamu. Calon kru kapal pesiar, simpan! pare.titianasa.com

### 21. Kenalan sama Miss Kate
Kenalan dulu sama Miss Kate 👩‍🏫

Dia gurumu di English Class Academy, Kampung Inggris. Datangi dia untuk membuka jalur belajar, dan dia juga yang memberi misi pertamamu.

Dari Pare sampai London, ceritamu dimulai dari dia. Dan di level tertinggi, surat darinya datang lagi 💌

pare.titianasa.com

**TikTok:** Kenalan sama Miss Kate, gurumu di Kampung Inggris. pare.titianasa.com

### 22. Tebak: interested on, in, atau at?
Tebak lagi, yuk 👀

**I am interested ___ music.**
A. on · B. in · C. at

Jawab di komentar dulu, baru geser!

pare.titianasa.com

**TikTok:** I am interested ___ music. Isi apa? 👇

### 23. B1 & B2: mulai berpendapat
Seri level, bagian 4 dan 5 dari 7: **B1 dan B2**.

B1: memberi pendapat dengan alasan, menulis email semi-formal, bercerita pengalaman.
B2: berdiskusi topik abstrak, presentasi singkat, memahami artikel panjang.

Di sini bahasa Inggrismu mulai terasa lancar 🚀

pare.titianasa.com

**TikTok:** B1 dan B2: dari bercerita ke berdiskusi. pare.titianasa.com

### 24. PTE Academic sekilas
PTE Academic dalam 5 slide 📊

💻 Tes di komputer, sekali duduk sekitar 2 jam
🎙️ Speaking & Writing, Reading, Listening
🔢 Skor 10–90 (Global Scale of English)
📬 Hasil biasanya dalam 2 hari kerja

Ciri khasnya: kamu bicara ke mikrofon, bukan ke penguji. Biasakan pakai bahasa Inggris setiap hari, termasuk ngobrol dengan warga di Kampung Inggris.

Sumber: pearsonpte.com (dicek Oktober 2026).

pare.titianasa.com

**TikTok:** PTE Academic sekilas: bagian, skor, dan hasilnya. pare.titianasa.com

### 25. Misi B1 & B2: dari Pare ke London
Ceritamu berlanjut sampai London 🇬🇧

B1: magang di Kampung Post, meliput banjir di Pasar Pare, menulis kolom opini, lalu menulis satu halaman edisi khusus.
B2: tinggal di flat Mr. Doyle, kuliah dengan Dr. Bennett, ikut debat, dan tampil di konferensi mahasiswa internasional.

Siapa sangka, semuanya dimulai dari kartu nama kosong di minggu pertama 😉

pare.titianasa.com

**TikTok:** Dari Pare ke London: cerita misi level B1 dan B2. pare.titianasa.com

### 26. Kesalahan yang masih lolos di level atas
Yang sudah lancar pun sering kepeleset di sini 😏

❌ If I would have known → ✅ If I had known
❌ must had been → ✅ must have been
❌ Unless you don't pay → ✅ Unless you pay
❌ very better → ✅ far better
❌ made a performance → ✅ gave a performance

Berapa yang kamu benar? Jujur di komentar 👇

pare.titianasa.com

**TikTok:** 5 kesalahan bahasa Inggris yang masih lolos di level B2 dan C1. pare.titianasa.com

### 27. TOEFL ITP sekilas
TOEFL ITP, yang sering diminta kampus dan instansi di Indonesia 📊

📝 140 soal, 115 menit
🎧 Listening 50 · ✏️ Structure & Written Expression 40 · 📖 Reading 50
🔢 Skor 310–677
🚫 ETS tidak menetapkan batas lulus. Tiap kampus atau instansi menentukan skor yang diminta.

Bagian Structure isinya tata bahasa, persis yang kamu latih bab demi bab di Kampung Bahasa.

Sumber: ets.org (dicek Oktober 2026).

pare.titianasa.com

**TikTok:** TOEFL ITP sekilas: 140 soal, 115 menit, skor 310–677. pare.titianasa.com

### 28. C1 & C2: puncaknya
Seri level, bagian 6 dan 7 dari 7: **C1 dan C2** 🏔️

C1: menulis esai terstruktur, bernegosiasi, memahami humor dan idiom. Di misinya kamu jadi analis muda di Thames Policy Lab, London.
C2: berkomunikasi hampir seperti penutur asli. Di misinya kamu berpidato di Speakers' Corner, debat gaya Oxford, sampai jadi juru bahasa untuk KBRI London.

Akhir ceritanya? Bukumu terbit 📖

pare.titianasa.com

**TikTok:** C1 dan C2: puncak jalur bahasa Inggris di Kampung Bahasa. pare.titianasa.com

### 29. TOEIC sekilas
TOEIC Listening & Reading, tes bahasa Inggris buat dunia kerja 💼

📝 200 soal, 2 jam
🎧 Listening 100 soal · 📖 Reading 100 soal
🔢 Skor 10–990

Soalnya seputar situasi kantor: percakapan kerja, pengumuman, email. Mirip misi kerja di Kampung Bahasa dari level A2 sampai C1.

Sumber: penyelenggara resmi (dicek Oktober 2026).

pare.titianasa.com

**TikTok:** TOEIC sekilas: 200 soal, skor 10–990, soal seputar kantor. pare.titianasa.com

### 30. Basic sampai C2, di satu tempat
Sebulan ini kita sudah keliling Kampung Inggris, dari Basic sampai C2 🙌

Materi bersuara, latihan, menulis tanpa autocorrect, misi bareng warga, dan sekarang ngobrol langsung dengan warga di Kampung Inggris 3D.

Mulai dari level mana pun, gratis, di pare.titianasa.com

**TikTok:** Basic sampai C2, di satu tempat. Mulai sekarang di pare.titianasa.com

## Sumber fakta tes (dicek 20 Oktober 2026)

| Tes | Sumber |
|---|---|
| TOEFL iBT | [ets.org: TOEFL iBT test content](https://www.ets.org/toefl/test-takers/ibt/about/content.html), [ets.org: score displays 2026](https://www.ets.org/toefl/blog/understanding-toefl-ibt-score-displays.html) |
| TOEFL ITP | [ets.org: TOEFL ITP test content](https://www.ets.org/toefl/itp/test-content.html) |
| IELTS | [ielts.org: IELTS Academic](https://ielts.org/take-a-test/test-types/ielts-academic-test), [ielts.org: scoring in detail](https://ielts.org/take-a-test/your-results/ielts-scoring-in-detail) |
| PTE Academic | [pearsonpte.com: PTE Academic](https://www.pearsonpte.com/pte-academic), [pearsonpte.com: test format](https://www.pearsonpte.com/pte-academic/test-format) |
| TOEIC L&R | [IIBC (perwakilan ETS di Jepang)](https://www.iibc-global.org/english/toeic/test/lr/about.html) |

Konversi skor tes ke level CEFR sengaja tidak dipakai. Tabel resmi IELTS sendiri tidak seragam antarhalaman, dan konversi TOEFL ITP dari pihak ketiga saling berbeda.
