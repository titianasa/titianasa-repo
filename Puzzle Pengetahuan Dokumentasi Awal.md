# Puzzle Pengetahuan: Dokumentasi Awal

Draf 0.1, 31 Oktober 2026, PareLabs AI

## Visi

Platform belajar yang memvisualisasikan pengetahuan siswa sebagai jaringan puzzle yang saling terhubung, seperti neuron. Siswa bisa melihat apa yang sudah dikuasai, apa yang belum, dan apa yang harus dipelajari dulu sebelum mengerjakan suatu tugas. Ia berfungsi sebagai “second brain” belajar: bukan catatan tentang apa yang pernah dibaca, melainkan peta pengetahuan yang sudah terbukti dikuasai.

## Masalah yang ingin diselesaikan

- Siswa tidak tahu persis kenapa gagal pada suatu soal: kurang vocab, kurang konsep, atau lupa prasyarat.
- Materi disajikan berurutan, padahal pengetahuan saling bergantung dan berbentuk jaringan.
- Hafalan cepat hilang tanpa pengulangan yang terjadwal.
- Belajar bahasa jarang bersifat “merangkai sambil mencoba”, padahal pendekatan blok seperti Scratch membuat pemula bisa belajar lewat percobaan.

## Konsep inti

Tiga bagian yang saling mengunci:

1. **Puzzle:** unit pengetahuan terkecil. Jenisnya vocab, konsep, simbol atau aturan pakai, dan prosedur. Tiap puzzle punya materi singkat, bank soal, dan daftar prasyarat.
2. **Peta pengetahuan (graf):** puzzle sebagai titik, prasyarat sebagai garis. Terang atau redupnya titik menunjukkan tingkat penguasaan saat ini.
3. **Mesin blok:** tempat siswa merangkai puzzle yang sudah dimiliki menjadi hasil, seperti kalimat, persamaan reaksi, atau rumus. Aturan sambung ditulis sebagai data, sehingga satu mesin dipakai lintas pelajaran.

## Siklus belajar

1. Tugas muncul, misalnya “ubah kalimat ini ke passive voice”.
2. Sistem membaca puzzle yang dibutuhkan dan mengecek koleksi siswa.
3. Puzzle yang belum dikuasai ditandai terkunci, lengkap dengan prasyaratnya.
4. Siswa mencari puzzle itu, membaca materi, lalu mengikuti uji.
5. Jika lulus, puzzle disimpan ke koleksi dan titiknya menyala di peta.
6. Setelah semua puzzle yang dibutuhkan lengkap, tugas terbuka dan siswa merangkai jawabannya dengan blok.
7. Hasil tugas memperbarui penguasaan semua puzzle yang terlibat.

## Mengukur penguasaan

Tiga tingkat: dilihat, bisa recall, bisa menerapkan. Cara mengecek berbeda per jenis puzzle:

- **Vocab dan simbol:** recall aktif (mengetik jawaban, bukan memilih) dengan pengulangan berjarak.
- **Konsep:** soal transfer yang belum pernah dilihat, yaitu menerapkan di konteks lain, mencari kesalahan, atau menjelaskan dengan kata sendiri.
- **Prosedur:** soal bertingkat tanpa petunjuk, dengan langkah yang makin banyak.

Setiap puzzle punya skor 0–100%. Skor naik jika jawaban benar, turun jika salah, dan memudar saat lama tidak dipakai (waktu paruh makin panjang tiap pengulangan berhasil). Puzzle dianggap “dimiliki” pada skor 50% ke atas dan “dikuasai” pada 90% ke atas. Ambang ini perlu dikalibrasi dengan data siswa nyata.

## Model data awal

- **Puzzle:** id, mata pelajaran, jenis, judul, materi, prasyarat (daftar id), bank soal recall, bank soal terapan.
- **Penguasaan siswa:** id siswa, id puzzle, skor, waktu pembaruan terakhir, jumlah pengulangan berhasil.
- **Paket aturan:** jenis blok, tabel boleh menyambung, pesan kesalahan, dan level tantangan, disimpan sebagai JSON.
- **Tugas:** id, perintah, daftar puzzle yang dibutuhkan, dan fungsi pemeriksa.

## Arsitektur yang disarankan

Modul dipisah supaya tiap bagian bisa diganti: mesin blok, graf pengetahuan, mesin penilaian (skor dan pemudaran), paket konten per pelajaran, dan lapisan AI. Dengan stack PareLabs AI (Next.js dan Supabase), puzzle, prasyarat, dan penguasaan cocok disimpan di Postgres sebagai tiga tabel, sedangkan paket aturan disimpan di kolom JSON.

## Peta jalan

- **Fase 1, bukti konsep:** mesin blok untuk Inggris, Mandarin, matematika, kimia, dan fisika; prototipe peta pengetahuan untuk passive voice.
- **Fase 2, satu mata pelajaran utuh:** bahasa Inggris dengan sekitar 100–200 puzzle, akun siswa, penyimpanan penguasaan, pemudaran, dan antrean ulang harian.
- **Fase 3, lapisan AI:** pembuatan soal otomatis, penjelasan kesalahan, dan pemetaan puzzle dari materi yang diunggah guru.
- **Fase 4, lintas pelajaran dan sosial:** Mandarin, matematika, STEM, tampilan guru, dan berbagi peta.

## Potensi pengembangan dan fitur

**Belajar dan penilaian**

- Antrean ulang harian berdasarkan puzzle yang mulai memudar.
- Soal adaptif: kesulitan naik saat jawaban benar beruntun.
- Diagnosis akar masalah: saat gagal, sistem menelusuri prasyarat yang lemah.
- Belajar mundur dari target (misalnya skor IELTS Writing tertentu) yang menghasilkan jalur puzzle.
- Penilaian jawaban terbuka oleh AI dengan rubrik.

**Peta pengetahuan**

- Siswa menambah garis hubungan dan catatan pribadi sendiri.
- Zoom bertingkat (area, topik, puzzle), pencarian, dan filter berdasarkan kelemahan.
- Hubungan lintas pelajaran, misalnya satuan di fisika dengan aljabar di matematika.
- Riwayat peta berupa animasi pertumbuhan dari waktu ke waktu.

**Mesin blok**

- Seret-dan-lepas, level tantangan, dan pemeriksa makna dengan bantuan AI.
- Pembuat paket aturan tanpa kode untuk guru.
- Pelajaran baru: Jepang, Arab, akuntansi, logika, dan SQL.

**Guru dan lembaga**

- Dasbor kelas berisi peta gabungan dan puzzle yang paling sering gagal.
- Penugasan berbasis puzzle dan pelacakan kemajuan.
- Bank puzzle bersama antar guru atau antar lembaga.

**Motivasi**

- Streak, lencana, dan target mingguan, serta tantangan antar teman.
- Area peta yang terbuka bertahap seperti peta game.

**Integrasi PareLabs**

- Jalur khusus IELTS, TOEFL, dan beasiswa (LPDP, Chevening, DAAD, AAS), serta tautan ke simulasi UjiLab.

## Risiko dan pertanyaan terbuka

- Membuat puzzle dan prasyaratnya butuh kurasi manual yang besar. AI bisa membantu, tetapi hasilnya perlu ditinjau guru.
- Ambang “dimiliki” dan laju pemudaran perlu dikalibrasi dengan data nyata.
- Graf yang terlalu besar membingungkan, jadi perlu tampilan bertingkat.
- Makna jawaban terbuka tidak bisa dicek dengan aturan saja.
- Pertanyaan terbuka: apakah penguasaan dibagikan antar mata pelajaran, siapa pemilik konten (guru atau platform), dan apakah siswa boleh melewati prasyarat.

## Ukuran keberhasilan

- Persentase siswa yang berhasil mengerjakan tugas setelah melengkapi prasyarat, dibanding yang melewatinya.
- Retensi puzzle setelah 7 dan 30 hari.
- Kecepatan menemukan akar masalah ketika siswa gagal.
- Seberapa sering siswa kembali membuka peta.

## Kontrak data (revisi)

Kontrak ini bersifat umum untuk semua domain. Hal khusus tiap pelajaran tidak ditaruh di sini, tetapi di paket aturan yang dirujuk puzzle.

- **Identifier:** slug bernamespace dengan format `domain.area.topik`, misalnya `eng.grammar.passive-voice` atau `phys.units.newton`. Identifier permanen, tidak pernah dipakai ulang, dan tidak berubah saat judul diganti (gunakan alias). Ditulis dalam bahasa Inggris, sedangkan judul dan materi per bahasa disimpan terpisah.
- **Puzzle:** id, version, kind, title (per bahasa), content (rujukan materi), requires, partOf, related, assessments, dan builder (rujukan paket aturan).
- **kind:** daftar tertutup, yaitu vocab, concept, symbol, procedure, dan fact. Cara menguji penguasaan mengikuti kind ini.
- **requires:** daftar objek berisi id, min (skor minimal prasyarat, bawaan 50%), source (human, ai, atau data), dan confidence (0–1). Hanya garis dengan kepercayaan cukup yang dipakai di tampilan siswa.
- **partOf:** hubungan hierarki. Bilangan real berisi puzzle-puzzle kecil, dan puzzle lain bisa meminta kelompoknya (misalnya “bilangan real minimal 70%”) tanpa menyambung ke tiap anggotanya.
- **Soal:** id, puzzle yang diuji, tipe (recall, transfer, procedure), dan cara memeriksa (exact, set, numeric, rules dari mesin blok, atau ai-rubric).

Tiga aturan yang dikunci dari awal:

1. requires tidak boleh membentuk lingkaran, dan validator otomatis menolaknya.
2. Perubahan kecil pada materi tidak menghapus penguasaan siswa, sedangkan perubahan besar mereset sebagian. Aturan kenaikan versi harus jelas.
3. Normalisasi jawaban (huruf besar, tanda baca, spasi) didefinisikan di kontrak, sehingga semua domain memeriksa dengan cara yang sama.

## Diagnosis bertingkat

Prasyarat berfungsi sebagai persyaratan yang bisa diuji. Saat siswa gagal pada suatu puzzle atau tugas, sistem menelusuri ke bawah sampai menemukan akar masalahnya.

1. Siswa gagal pada puzzle atau tugas X.
2. Sistem menguji prasyarat terdekat X dengan soal singkat (1–2 soal per puzzle). Prasyarat yang skornya masih segar dan kuat boleh dilewati karena buktinya sudah ada.
3. Prasyarat yang gagal dibuka: tampil isi puzzle-nya dan titik gagalnya, yaitu soal yang salah, jawaban siswa, jawaban benar, dan penjelasannya.
4. Langkah 2 dan 3 diulang untuk prasyarat dari puzzle yang gagal, dan seterusnya. Puzzle terdalam yang gagal, dengan semua prasyaratnya lulus, adalah akar masalah.
5. Siswa belajar dari akar masalah, lalu naik kembali tingkat demi tingkat sampai ke tugas awal.

Agar tidak menjadi panjang dan membingungkan:

- **Layar teratas hanya menampilkan puzzle yang sedang diuji.** Jejak ringkas di atasnya menunjukkan posisi, misalnya Tugas > Passive voice > Verb 3.
- Tingkat yang sudah lulus otomatis tertutup. Siswa atau guru bisa membukanya untuk melihat isi dan hasil ujinya.
- Ada batas kedalaman dan batas jumlah soal per tingkat. Diagnosis berhenti begitu akar masalah ditemukan.
- Hasil setiap uji memperbarui skor puzzle terkait. Pola gagal dan lulus juga menjadi data untuk memperkuat atau melemahkan garis prasyarat.

Keluarannya adalah laporan “di mana pemahaman siswa putus”, yang berguna bagi siswa maupun guru.

## Pembangunan graf otomatis

Graf yang besar (misalnya bilangan real hingga aljabar) tidak mungkin dibuat manual, jadi dibangun oleh mesin dan ditinjau manusia.

**Pipeline**

1. **Sumber:** silabus, bab buku, materi guru, atau bank soal yang sudah ada.
2. **Usulan AI:** puzzle (dengan kind dan id sesuai kontrak) dan garis prasyaratnya.
3. **Validator otomatis:** menolak lingkaran, menggabungkan duplikat, membatasi kedalaman, dan menandai puzzle yatim.
4. **Tinjauan guru** hanya untuk usulan yang kepercayaannya rendah, bukan membuat dari nol.
5. **Kalibrasi dari data siswa:** jika siswa yang gagal di X sering lemah di Y, garis Y ke X diperkuat. Garis yang tidak membantu memprediksi dipangkas, dan garis baru bisa ditemukan dari pola kesalahan. Dengan begitu graf tumbuh seiring pengetahuan dan data.
6. **Pertumbuhan:** materi baru dianalisis, lalu puzzle barunya disambungkan ke graf yang ada.

**Mengendalikan ukuran graf**

- Tampilan siswa memakai hierarki partOf dan hanya menampilkan batas terdepan: puzzle lemah yang paling dekat dengan tugas.
- Garis berlebihan dibuang (jika A ke B ke C sudah ada, garis A ke C tidak digambar).
- Penguasaan di puzzle yang lebih tinggi menjadi bukti tidak langsung bagi prasyaratnya, sehingga siswa tidak dipaksa turun satu per satu.
- Satu puzzle harus bisa diuji dengan 3–5 soal. Jika tidak bisa, dipecah. Jika terlalu kecil, digabung.

**Risiko:** prasyarat usulan AI sering masuk akal tetapi tidak selalu benar. Karena itu tinjauan guru dan kalibrasi data tidak boleh dilewati. Mulai dari satu domain, misalnya tata bahasa Inggris, untuk mengukur akurasi usulan mesin sebelum melebar.
