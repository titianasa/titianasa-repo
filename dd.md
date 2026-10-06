# Review project Titian Asa

> aku ingin kamu mereview ini, lihat apakah ada yang kliru, apa yang perlu diperbaiki , dikrangi atau ditambahkan untuk project titian asa, ekosistem pembelajran terlengkap di indonesia
>
> User context
>
> Attachments:
> - DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md: `~/Dev/sanja-workspace/alr/DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md`

<details><summary>6 previous messages</summary>

> Saya akan menilai dokumen ini sebagai rancangan kurikulum dan learning path untuk Titian Asa—fokus pada ketepatan isi, celah penting, prioritas, serta apa yang sebaiknya dipangkas atau ditambahkan.
>
> <details><summary>Explored a file, a search</summary>
>
> - Read `~/Dev/sanja-workspace/alr/DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md`
> - Searched for `^## |^### ` in `DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md`
>
> </details>
>
> Saya sudah menemukan ketidakkonsistenan struktural yang jelas pada hitungan rumpun mapel. Berikutnya saya cek pola duplikasi, kelengkapan jenjang, dan kesesuaian jalur ujian dengan rujukan resmi yang berlaku.
>
> <details><summary>Explored a file, 3 searches, searched the web</summary>
>
> <details><summary>Explored a file, a search</summary>
>
> - Read `~/Dev/sanja-workspace/alr/DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md`
> - Searched for `^(\*\*)?Total (Modul|Bab)|Jumlah (Data|Materi|Modul)|TODO|TBD|unspecified|SMK|PAUD|TK|SLB|P5|Fase [A-F]` in `DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md`
>
> </details>
>
> Searched the web for `site:pusmendik.kemdikbud.go.id TKA mata pelajaran Bahasa Indonesia Matematika pilihan 2025 ...`
>
> <details><summary>Explored 4 files, 2 searches</summary>
>
> - Read `~/Dev/sanja-workspace/alr/DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md`
> - Searched for `Kurikulum 2013|K13|Kurikulum Merdeka|Capaian Pembelajaran|CP |Fase|Pendidikan Khusus|disabilitas|aksesibil|orang tua|guru|portofolio|proyek|project|rubrik|diagnostik|prasyarat|remedial|microcredential|sertifikat|literasi finansial|keamanan digital|AI |kecerdasan buatan|kesehatan mental|karier` in `DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md`
> - Read `~/Dev/sanja-workspace/alr/DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md`
> - Searched for `Kode Mapel|Total Modul|Total Bab` in `DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md`
> - Read `~/Dev/sanja-workspace/alr/DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md`
> - Read `~/Dev/sanja-workspace/alr/DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md`
>
> </details>
>
> </details>
>
> Audit angkanya memperkuat temuan awal: dokumen ini memuat 48 rumpun, bukan 45 atau 46; total aktivitas yang benar-benar tertera di tabel berjumlah 89.070, bukan 89.088. Saya juga menemukan beberapa rumpun berstatus `custom` tetapi tercatat 0 modul/0 materi walau isi kurikulumnya panjang—ini akan menurunkan kepercayaan pengguna bila dipublikasikan.
>
> Permission request
>
> Status: completed
> Reason: Saya perlu membaca dokumen yang Anda minta untuk direview.
> Response: granted
</details>

Secara arah, dokumen ini kuat: cakupannya luas, jenjangnya ambisius, dan sudah mencakup sekolah, ujian, Cambridge, agama, hingga karier. Namun untuk menjadi “ekosistem pembelajaran terlengkap”, saya rasa dokumen ini belum siap dipublikasikan sebagai katalog resmi tanpa perapihan besar pada data, struktur, dan positioning.

Prioritas perbaikan tertinggi:

1. Perbaiki konsistensi data terlebih dahulu.

   - Ringkasan menyebut **45 mapel**, judul Bagian 2 menyebut **46**, tetapi daftar aktual berisi **48 rumpun**.
   - Ringkasan menyebut **20.018 modul** dan **89.088 materi**. Akumulasi angka per-rumpun yang tertulis hanya **13.636 modul** dan **71.830 materi**, sedangkan penjumlahan aktivitas pada tabel menghasilkan **89.070**. Tiga angka ini tidak bisa hidup berdampingan.
   - Sejumlah mapel berisi kurikulum panjang namun statistiknya `0 modul / 0 materi`, misalnya Akidah Akhlak, Al-Qur’an Hadis, Bahasa Inggris, lima bahasa asing, Fiqih, dan SKI. Ini perlu dianggap sebagai bug sinkronisasi, bukan sekadar kosmetik.
   - `unspecified` sebanyak 17.281 item terlalu besar. Setiap item harus punya tipe yang jelas: materi, video, latihan, asesmen diagnostik, proyek, flashcard, simulasi, atau checkpoint.

2. Jangan menyebut ini “learning path” jika baru berupa daftar topik.

   Saat ini yang tersedia lebih mirip katalog/outline. Learning path yang sebenarnya perlu memiliki:

   - sasaran peserta dan prasyarat;
   - kompetensi akhir yang terukur;
   - urutan wajib vs pilihan;
   - estimasi waktu;
   - asesmen diagnostik awal;
   - aturan kelulusan/mastery;
   - remedial dan pengayaan;
   - proyek/portofolio;
   - rekomendasi jalur berikutnya.

   Misalnya, “Persiapan IELTS” seharusnya bukan hanya bagian dalam daftar Bahasa Inggris, tetapi jalur dengan target skor, placement test, latihan listening/speaking/writing, mock test, dan umpan balik rubrik.

3. Pisahkan “kurikulum”, “persiapan ujian”, dan “keahlian hidup/karier”.

   Saat ini ketiganya bercampur sebagai mapel sejajar. Lebih mudah dipahami jika navigasinya menjadi:

   | Area | Contoh |
   |---|---|
   | Kurikulum sekolah | SD–SMA/MA/SMK, Madrasah, Cambridge |
   | Persiapan ujian | TKA, UTBK-SNBT, CPNS, BUMN, OSN |
   | Keahlian dan karier | Bahasa, coding, bisnis, komunikasi, CV, wawancara |
   | Pengembangan diri | Penalaran, literasi finansial, kesehatan mental, etika digital |

4. Koreksi beberapa rujukan kurikulum dan ujian yang berisiko menyesatkan.

   - TKA tidak tepat diposisikan terutama sebagai “literasi membaca, numerasi, Bahasa Inggris, Saintek, Soshum”. Untuk SD/SMP, mata uji wajib adalah Bahasa Indonesia dan Matematika; pada SMA/SMK ada Bahasa Indonesia, Matematika, Bahasa Inggris, serta mata pelajaran pilihan. Struktur TKA sebaiknya dipisahkan menurut jenjang dan mapel, bukan memakai kerangka AKM lama. [Pusat Asesmen Pendidikan](https://pusmendik.kemdikbud.go.id/tka/)
   - Frasa “AKM & TKA” sebaiknya tidak digabung tanpa penjelasan karena tujuan dan bentuk asesmennya berbeda.
   - Kurikulum Indonesia sebaiknya bertumpu pada **Capaian Pembelajaran (CP) Fase A–F**, lalu baru dipetakan ke kelas. Ini membuat konten lebih tahan terhadap perubahan kebijakan. [Contoh struktur CP Bahasa Indonesia](https://kurikulum.kemdikbud.go.id/file/cp/dasmen/8.%20CP%20Bahasa%20Indonesia.pdf)
   - SKB CPNS sangat bergantung pada jabatan/formasi; jangan disajikan sebagai satu silabus universal.
   - Rekrutmen BUMN berubah per periode. Materinya lebih aman diberi label “persiapan umum” dan diberi tanggal pembaruan, bukan diklaim sebagai format tetap.
   - Untuk Cambridge, gunakan istilah “selaras dengan” hanya bila ada pemetaan eksplisit terhadap syllabus/kode ujian dan proses peninjauan akademik.

5. Tambahkan cakupan yang masih kosong bila klaimnya “terlengkap di Indonesia”.

   Yang paling penting:

   - PAUD/TK;
   - Paket A, B, C dan homeschooling;
   - pendidikan khusus/aksesibilitas disabilitas;
   - jalur madrasah yang benar-benar dipetakan per jenjang, bukan hanya tambahan mapel agama;
   - kompetensi kejuruan SMK yang jauh lebih luas dari Akuntansi dan Teknik Otomotif;
   - literasi finansial, hukum warga digital, keamanan siber, media literacy, AI literacy, dan keselamatan daring;
   - kesehatan mental, relasi sehat, pertolongan pertama, serta pendidikan kebencanaan;
   - keterampilan kerja: spreadsheet, komunikasi profesional, presentasi, manajemen proyek, dan portofolio;
   - proyek lintas-mapel yang kontekstual Indonesia.

6. Kurangi pola “20 aktivitas” yang terlalu mekanis.

   Hampir semua bab memiliki 20 aktivitas. Ini membuat katalog tampak dihasilkan dari template dan belum menunjukkan desain pembelajaran. Lebih baik tiap bab memiliki komposisi yang bermakna, misalnya:

   `konsep → contoh → latihan bertahap → aplikasi → refleksi → asesmen`

   Kualitas tidak diukur dari banyaknya aktivitas. Untuk konsep sederhana, 4–6 aktivitas yang tepat lebih baik daripada 20 checkpoint.

7. Tambahkan standar mutu konten.

   Dokumen perlu satu bagian “Governance Kurikulum” yang menjelaskan:

   - sumber resmi dan versi kurikulum;
   - pemilik/editor akademik per mapel;
   - tanggal terakhir diperbarui;
   - standar editorial dan sensitivitas agama/budaya;
   - sistem review guru/ahli;
   - mekanisme koreksi pengguna;
   - lisensi dan atribusi, terutama untuk Cambridge dan materi ujian.

Catatan kecil nomenklatur: gunakan “Al-Qur’an Hadis” (bukan “Hadist”) dan pertimbangkan mengikuti nama mapel resmi seperti “Pendidikan Agama … dan Budi Pekerti” serta “Pendidikan Pancasila” agar konsisten dengan dokumen pemerintah.

Rekomendasi saya: jangan menambah ribuan materi dulu. Rapikan data dan arsitektur, jadikan 7 jalur unggulan benar-benar adaptif dan selesai dari awal sampai outcome, lalu perluas secara bertahap. Titian Asa akan lebih meyakinkan bila dikenal sebagai platform dengan jalur belajar yang jelas, terukur, dan terus diperbarui—bukan hanya katalog yang sangat besar.

> Ide dari aplikasi ini adalah nanti ini akan menjadi aplikasi yang pembelajarannya, kurikulumnya itu sepenuhnya otonom, akan di-upgrade dan di-maintain oleh AI. Jadi sistemnya nanti kita menyediakan template seperti ini. Lalu dari user akan berinteraksi dengan materi kita, dengan latihan soal kita. Lalu dari data itu nanti AI akan meng-upgrade apakah ini relevan, apakah ini masih bisa digunakan, apakah penjelasannya sudah sesuai atau belum. Untuk membuat skeleton-nya, di sini itu kita bedakan antara learning path dan materi inti. Materi inti adalah materi yang mencakup fundamental seperti matematika, itu dari tingkat dasar sampai advance. Itu nanti di learning path dipecah-pecah. Nah itu berlaku untuk mengajari materi yang lain juga. Jadi learning path itu adalah memetakan dari materi inti biar apa, biar tidak double produksi dan ketika mereka sudah mempelajari materi ini, mereka merasa tidak double belajar dari awal. Ide-nya sih seperti itu. Nah untuk latihannya memang di situ nanti rencana kita akan fokus ke teks dulu semuanya. Teks dan juga nanti ada checkpoint latihan. Nah untuk latihannya pun di situ nanti ada berbagai macam materi atau bentuk soal menyesuaikan dari bentuk latihannya sendiri. Contohnya IELTS itu kan ada macam-macam bentuk soal, mungkin TKA juga. Nah berikutnya di sini nanti saya juga akan menambahkan yang namanya materi dari web interaktif, di mana beberapa materi itu akan berbentuk website interaktif seperti bilangan bulat dan sebagitu, mereka akan menggunakan website interaktif untuk belajar. Seperti bahasa Inggris, nanti pronunciation-nya, soal alfabet, itu nanti menggunakan web interaktif. Seperti bahasa Mandarin, mereka juga akan mendapatkan web interaktif. Jadi semuanya itu nanti akan ada web interaktifnya. Nah tolong bantu saya itu bisa merealisasikan.

<details><summary>3 previous messages</summary>

> Saya paham modelnya sekarang: **materi inti adalah aset kanonik**, sedangkan learning path adalah susunan/pemetaan aset itu untuk tujuan pengguna tertentu. Itu keputusan yang tepat—dan mengubah beberapa kritik saya sebelumnya: angka `custom` dan aktivitas teks bukan masalah jika memang merupakan template awal, asalkan model datanya siap untuk diisi dan dievaluasi AI. Saya akan mulai dengan menyusun blueprint yang bisa langsung menjadi fondasi implementasinya.
>
> <details><summary>Explored 5 files, a search, 2 lists</summary>
>
> - Listed files
> - Listed files
> - Read `./agent/docs/adr/0007-concept-hierarchy.md`
> - Read `./agent/docs/adr/0008-content-versioning.md`
> - Read `./agent/docs/adr/0013-ai-learning-engine.md`
> - Read `./agent/docs/curriculum-constitution.md`
> - Read `./agent/docs/STATE.md`
> - Searched for `^## |^### |^#### |Status:|Phase|Fase|Next|Berikut|Acceptance|Milestone|L[0-4]` in `0013-ai-learning-engine.md`
>
> </details>
>
> Permission request
>
> Status: completed
> Reason: Untuk menerjemahkan blueprint ini menjadi implementasi yang cocok, saya perlu memeriksa struktur proyek aplikasi yang terkait.
> Response: granted
</details>

Ide dasarnya sangat tepat. Kunci arsitekturnya adalah:

> **Materi inti = perpustakaan kanonik yang reusable.**
> **Learning path = komposisi materi inti untuk tujuan tertentu, tanpa menduplikasi konten.**

Contoh: konsep “bilangan bulat” cukup dibuat sekali, tetapi dapat dipakai ulang di jalur SD, TKA, UTBK dasar, remedial, atau jalur adaptif siswa. Yang berbeda adalah urutan, kedalaman, latihan, dan syarat kelulusannya—bukan materi dasarnya.

Setelah saya cek fondasi proyeknya, arah ini ternyata sudah cukup matang secara desain. Bahkan sudah ada keputusan tentang jejak belajar, versi konten, identitas soal tetap, analisis kualitas konten, dan agen AI semi-otonom. Fase fondasi pencatatan data serta Admin Pusat juga sudah selesai. Langkah realisasinya sekarang sebaiknya:

1. **Phase 41 — Mesin pemahaman**
   - Hubungkan setiap aktivitas teks, checkpoint, kuis, dan web interaktif ke konsep inti.
   - Hitung penguasaan konsep, kesulitan soal, waktu belajar, pola salah, dan “health score” per materi.
   - Jangan gunakan engagement semata sebagai ukuran mutu; banyak scroll bukan berarti paham.

2. **Phase 42 — Agen konten semi-otonom**
   - AI Analis mendeteksi materi/soal bermasalah.
   - AI Diagnosa mencari penyebab: penjelasan membingungkan, prasyarat kurang, soal ambigu, atau tingkat kesulitan salah.
   - AI Editor membuat revisi sebagai proposal.
   - AI QA memeriksa revisi secara independen.
   - Admin Pusat menyetujui, menolak, atau meminta revisi.

   Mulai dari level otonomi **L1: AI hanya mengusulkan, manusia menyetujui**. Koreksi typo atau metadata bisa naik ke L2 nanti, tetapi perubahan substansi akademik jangan otomatis diterbitkan di awal.

3. **Phase 43 — Learning path adaptif**
   - Placement test saat masuk jalur.
   - Sistem menentukan materi yang boleh dilewati, harus dipelajari, atau perlu remedial.
   - Jalur IELTS, TKA, UTBK, dan sekolah memakai materi inti yang sama, lalu memiliki aturan urutan dan target berbeda.
   - Siswa tidak dipaksa mengulang materi yang sudah terbukti dikuasai.

4. **Phase 44 — Eksperimen**
   - Bandingkan versi materi lama vs revisi AI secara aman.
   - Promosikan versi baru hanya jika bukti menunjukkan pemahaman siswa membaik.
   - Wajib ada rollback dan versi historis; hasil ujian siswa tidak boleh berubah akibat konten direvisi setelahnya.

Untuk model data, hubungan utamanya kira-kira seperti ini:

```text
Konsep inti
  └─ Materi / artikel / web interaktif / checkpoint / soal
       └─ versi konten + bukti kualitas

Learning path
  └─ node materi inti (referensi, bukan salinan)
       └─ prasyarat, urutan, target, aturan adaptasi
            └─ progres dan mastery tiap siswa
```

Fokus teks lebih dulu juga keputusan yang bagus. Teks + checkpoint adalah format paling cepat untuk memvalidasi struktur kurikulum dan menghasilkan data belajar. Web interaktif sebaiknya ditambahkan selektif pada konsep yang memang mendapat manfaat besar dari visualisasi atau manipulasi langsung—bilangan, geometri, grafik, simulasi fisika/kimia, pronunciation, Hanzi, dan sejenisnya—bukan sekadar agar semua materi “punya web interaktif”.

Satu penyesuaian penting: saya akan menyebut visinya **“AI-maintained, human-governed curriculum”**, bukan sepenuhnya otonom sejak awal. Itu lebih aman secara akademik, lebih mudah dipercaya sekolah/orang tua, dan tetap menuju otonomi bertahap setelah datanya cukup.

Fondasi proyek saat ini sudah berada tepat sebelum Phase 41–44. Jadi pekerjaan paling bernilai berikutnya bukan menambah katalog materi dulu, melainkan merinci dan membangun **Mesin Pemahaman** agar semua materi yang nanti diproduksi benar-benar bisa belajar dari perilaku pengguna.

> Masalahnya sekarang itu kita belum punya standar materi yang menurut saya benar. Makanya di sini tadi saya berikan ke kamu untuk kamu koreksi dan kamu benarkan. Mulai dari materinya, topiknya, babnya, terus learning path-nya, label-labelnya, gitu. Jadi kita benahi itu dulu

<details><summary>2 previous messages</summary>

> Setuju—AI tidak boleh dibiarkan memelihara kurikulum yang standarnya belum tegas. Kita perlu membangun **konstitusi kurikulum Titian Asa** lebih dulu, lalu katalog lama dipetakan ulang terhadap standar itu. Saya akan membuat rancangan standar yang memisahkan materi inti, materi turunan, dan learning path; sekaligus menetapkan struktur topik, bab, label, serta aturan mutu konten.
>
> <details><summary>Created a file, ran a command</summary>
>
> - Ran `mkdir -p outputs && ls -ld outputs`
> - Wrote `./outputs/STANDAR_KURIKULUM_TITIAN_ASA.md` (+225 -0)
>
> </details>
</details>

Betul. Sebelum AI mengelola konten, kita harus menetapkan standar akademik dan struktur data yang benar dulu.

Saya sudah membuat rancangan fondasi: [STANDAR_KURIKULUM_TITIAN_ASA.md](./outputs/STANDAR_KURIKULUM_TITIAN_ASA.md).

Inti koreksinya:

- Materi inti disusun sebagai `domain → mapel → strand → konsep → unit belajar`.
- Learning path hanya mereferensikan unit inti; tidak boleh membuat duplikat.
- “Bab” bukan aset utama, hanya tampilan. Aset yang stabil adalah konsep dan unit belajar.
- Setiap unit wajib punya tujuan, prasyarat, penjelasan, contoh, latihan, checkpoint, dan aturan lanjut/remedial.
- Label distandardkan dan dipisah: `subject:`, `concept:`, `phase:`, `exam:`, `cefr:`, dan seterusnya.
- TKA, UTBK, IELTS, CPNS, dan BUMN diposisikan sebagai path ujian/tujuan, bukan materi inti.
- Angka template seperti “20 aktivitas” dihapus sebagai standar desain.
- Web interaktif digunakan pada konsep yang memang terbantu visualisasi atau manipulasi, bukan sebagai hiasan wajib.
- AI bekerja dengan alur temuan → diagnosis → proposal → QA → persetujuan → evaluasi, bukan langsung mengubah kurikulum.

Saya juga menetapkan pilot yang paling tepat: **Matematika → Bilangan → Bilangan Bulat**. Dari materi inti itu kita bisa membuktikan satu sumber yang sama dapat dipakai untuk jalur fondasi SMP, TKA, dan remedial adaptif tanpa produksi ganda.

Berikutnya, saya sarankan kita mengaudit dan menulis ulang katalog lama berdasarkan standar ini—mulai dari pemetaan seluruh rumpun menjadi domain, strand, konsep, dan path yang benar.

> Mungkin sebelum lanjut saya sampaikan lagi. Di sini untuk latihannya atau soalnya itu sudah saya set juga untuk tingkat kesulitan ya, dari mudah, menengah, dan sulit. Lalu di situ juga ada taksonomi, tingkat taksonomi, belum pemahaman sampai higher order thinking kalau nggak salah ya. Lalu sebenarnya untuk kenapa kok saya pakai pembelajaran interaktif itu, biar itu nanti bisa digunakan untuk guru di kelas juga, karena sekarang banyak sekolah yang menggunakan media layar sentuh dan lain sebagainya. Jadi saya buatkan itu dan juga untuk mengatasi mahalnya token itu. Karena kemarin itu di sini saya hitung itu ketika full menggunakan artikel itu, satu bab itu sudah tiga sama latihan soal itu mengeluarkan sekitar 150 ribu token habisnya. Tapi kalau dengan satu website interaktif itu, itu hanya menghabiskan 20 ribu token. Nah mungkin itu berisaran saya juga gimana untuk biar tidak membengkak dalam penyiapan materinya ini. Apakah bisa dibikin yang lebih simpel, terus nanti pengembangannya gimana, gitu ya. Jadi saya ingin ini benar-benar nanti bisa dikembangkan, digunakan, dan scalable.

<details><summary>2 previous messages</summary>

> Penjelasan ini mengubah penekanannya: web interaktif bukan sekadar pelengkap visual, melainkan **format konten utama yang reusable** untuk belajar mandiri sekaligus media guru di kelas—dan berpotensi jauh lebih hemat dalam produksi. Saya akan menambahkan pola arsitektur “engine + konfigurasi” agar interaktifnya tidak berubah menjadi ribuan website unik yang mahal dirawat.
>
> <details><summary>Edited a file</summary>
>
> - Wrote `./outputs/STANDAR_KURIKULUM_TITIAN_ASA.md` (+69 -5)
>
> </details>
</details>

Pendekatan Anda masuk akal, terutama bila interaktif dipakai sebagai media guru sekaligus materi peserta. Saya sudah memperbarui standar menjadi [versi terbaru](./outputs/STANDAR_KURIKULUM_TITIAN_ASA.md).

Perubahan terpenting: jangan membuat “website per bab”. Buat:

```text
Engine interaktif reusable + konfigurasi materi kecil
```

Contohnya, engine garis bilangan dibuat sekali. Materi penjumlahan, pengurangan, perbandingan, dan operasi campuran cukup mengirim konfigurasi: rentang angka, skenario, petunjuk, konsep, dan checkpoint. Satu perbaikan pada engine otomatis meningkatkan banyak materi.

Ini cocok untuk target biaya dan skala Anda:

- Artikel panjang tidak perlu dibuat ulang per path atau per siswa.
- Web interaktif yang sudah dibuat tidak menggunakan token setiap kali dibuka.
- Satu spesifikasi materi dapat menghasilkan artikel, konfigurasi interaktif, dan keluarga soal yang konsisten.
- Guru memiliki mode presentasi/layar sentuh; peserta memiliki mode latihan dan progres personal.
- Latihan bisa memakai soal berparameter, bukan AI membuat soal baru penuh setiap kali siswa mengerjakan.

Soal Anda yang sudah memiliki tingkat mudah–menengah–sulit dan taksonomi itu fondasi yang benar. Yang perlu dipastikan: keduanya disimpan sebagai dua dimensi terpisah.

- Kesulitan: mudah, menengah, sulit—awalnya dari kalibrasi ahli, lalu diperbaiki dari data keberhasilan nyata.
- Taksonomi: mengingat sampai HOTS—menjelaskan jenis berpikir yang diuji.
- Tambahkan format respons dan konsep yang diukur.

Soal HOTS tidak selalu sulit, dan soal sulit tidak selalu HOTS. Pemisahan ini penting agar AI nantinya tidak keliru menyimpulkan kualitas latihan.

Urutan pengembangan paling hemat menurut saya:

1. Buat 5–8 engine interaktif yang paling banyak dipakai: garis bilangan, pecahan, geometri/grafik, matching/flashcard, pronunciation, visualisasi algoritma.
2. Tetapkan format `lesson specification` terstruktur sebagai sumber tunggal.
3. Pilot pada Bilangan Bulat: satu materi inti, artikel ringkas, engine garis bilangan, checkpoint, dan soal tiga tingkat kesulitan.
4. Turunkan materi yang sama ke mode guru, jalur SMP, jalur TKA, dan remedial—tanpa menggandakan konten.
5. Setelah terbukti, baru produksi domain besar lain.

Catatan penting: perbandingan 150 ribu vs 20 ribu token bagus sebagai hipotesis biaya, tetapi tetap ukur biaya totalnya: generasi, validasi, QA, pengujian interaktif, serta berapa banyak unit yang bisa memakai ulang engine tersebut. Engine interaktif memang paling hemat ketika dipakai puluhan hingga ratusan unit, bukan hanya satu bab.

> contoh konten website
>
> dan contoh beberapa fitur konten studio, elearning, kuis engie, tipe soal.
>
> untuk dokumentasi bisa dilihat di folder alr/agen/docs/tickets disitu ada full dokumentasi pembuatan aplikasi sampai saat ini
>
> User context
>
> Attachments:
> - <!DOCTYPE html> <html lang="id"> <head> <meta charset="UTF-8"> <meta name="view…: `~/.codex/attachments/0d265505-850c-42a7-93cc-17dda4bcd0e6/pasted-text.txt`
> Images:
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-58-03.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-57-56.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-57-45.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-57-34.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-56-40.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-56-30.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-56-08.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-55-57.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-55-36.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-55-29.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-55-22.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-55-05.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-54-57.png`
> - `~/Pictures/Screenshots/Screenshot From 2026-09-17 04-54-48.png`

<details><summary>5 previous messages</summary>

> Contoh ini penting—fitur yang Anda miliki ternyata jauh lebih matang daripada yang terlihat dari katalog: studio sudah mendukung blok pedagogis, media/sematan web, checkpoint, bank soal, tingkat kesulitan, Bloom, serta review AI. Saya akan meninjau contoh website dan dokumentasi tiketnya agar standar kurikulum yang kita buat benar-benar mengikuti kemampuan sistem yang sudah ada, bukan mendesain ulang secara abstrak.
>
> <details><summary>Explored 3 files, 2 searches</summary>
>
> - Read `~/.codex/attachments/0d265505-850c-42a7-93cc-17dda4bcd0e6/pasted-text.txt`
> - Searched for `question type|tipe soal|content block|blok|interactive|interaktif|embed|web|taxonomy|bloom|difficulty|kesulitan|checkpoint|module item|article|quiz` in `phase-3*.md`
> - Searched for `<h[1-3]|function |addEventListener|localStorage|audio|quiz|check|score|progress` in `pasted-text.txt`
> - Read `./agent/docs/tickets/phase-37-article-quiz-content-model.md`
> - Read `./agent/docs/tickets/phase-38-quiz-builder-parity.md`
>
> </details>
>
> Saya sudah mengonfirmasi tiga hal: sistem saat ini memang sudah memiliki artikel/kuis sebagai dua jenis konten utama, sekitar 40 subtype soal lintas format, dan tingkat kesulitan serta Bloom per soal. Contoh web Anda juga menunjukkan format yang tepat untuk materi kaya—namun agar dapat dipakai AI dan diskalakan, web tersebut perlu kontrak integrasi yang jelas untuk progres, konsep, versi, aksesibilitas, dan mode guru.
>
> <details><summary>Edited a file</summary>
>
> - Wrote `./outputs/STANDAR_KURIKULUM_TITIAN_ASA.md` (+21 -1)
>
> </details>
>
> Permission request
>
> Status: completed
> Reason: Saya perlu meninjau contoh website interaktif dan tampilan studio/kuis untuk menyelaraskan standar kurikulum dengan fitur nyata aplikasi.
> Response: granted
</details>

Contoh-contoh ini mengubah kesimpulan saya: fondasi produk Anda sudah sangat kuat. Kita tidak perlu merancang ulang Content Studio atau Quiz Engine; kita perlu menjadikan kemampuan yang sudah ada sebagai **standar produksi kurikulum**.

Saya sudah menyesuaikan standar di [STANDAR_KURIKULUM_TITIAN_ASA.md](./outputs/STANDAR_KURIKULUM_TITIAN_ASA.md).

Yang sudah benar dan perlu dipertahankan:

- Studio artikel sudah mendukung blok pedagogis yang kaya: definisi, contoh, langkah, catatan, kesalahan umum, media, sematan web, dan soal di dalam materi.
- Kuis memiliki banyak subtype lintas pilihan, isian, susun, media, produksi, interaktif, dan skala.
- Setiap soal sudah dapat diberi tingkat kesulitan dan Bloom; ini persis fondasi untuk pelacakan kualitas AI.
- Ada pemisahan draft, QA/review, dan persetujuan AI.
- Contoh pelafalan `TH` sangat baik sebagai format materi: penjelasan, definisi, langkah praktis, kesalahan umum, checkpoint, lalu tampilan peserta yang rapi.

Koreksi pentingnya hanya satu: website interaktif seperti contoh Alphabet tidak boleh menjadi aset terpisah yang “hidup sendiri”. Dari kode contoh, progres dan skor masih berada di JavaScript browser; belum terlihat pengiriman event ke platform. Jadi perlu kontrak standar:

```text
Website interaktif
→ memberi tahu Titian saat dibuka, menyelesaikan bagian,
  menjawab checkpoint, dan selesai
→ Titian menyimpan progres, mastery, dan versi kontennya
```

Setiap web interaktif wajib punya metadata: ID stabil, versi, konsep yang dilatih, tujuan, mode guru/peserta, event belajar, kondisi selesai, serta fallback teks/audio. Ini membuat AI bisa mengevaluasi apakah web tersebut benar-benar membantu pemahaman.

Untuk skala, gunakan dua jalur sekaligus:

- **Widget reusable** untuk pola berulang: garis bilangan, grafik, flashcard, matching, pronunciation, visualisasi algoritma.
- **CodeWeb khusus** untuk pengalaman lengkap seperti Alphabet & Letter Sounds, simulasi, permainan, atau materi presentasi guru.

Jangan memaksa web khusus menjadi widget generik. Tetapi untuk CodeWeb, gunakan starter/template yang sudah menyediakan layout responsif, navigasi, progres, checkpoint, event Titian, mode guru, dan aksesibilitas. AI cukup mengisi spesifikasi pembelajaran serta konfigurasi/aset khusus—bukan menulis ulang ribuan baris boilerplate setiap bab.

Satu catatan tentang tingkat kesulitan: badge “mudah/menengah/sulit” pada library tipe soal sebaiknya diperlakukan sebagai **rekomendasi default subtype**, bukan kebenaran untuk seluruh soal. Soal Gap Fill bisa mudah atau sulit tergantung teks dan jawaban. Nilai kesulitan final harus disimpan per soal, lalu nanti dikalibrasi dari data nyata.

Dokumentasi juga menegaskan bahwa Content Studio telah matang pada model Artikel + Kuis. Rencana Quiz Builder berikutnya sudah mencakup pengaturan ujian, timer, template, bank soal, generation batch, dan draft AI. Jadi standar kurikulum nanti harus langsung memanfaatkan struktur tersebut, terutama menambahkan pemetaan `konsep → item artikel → bagian artikel → grup soal → soal` agar seluruh data pembelajaran dapat dibaca oleh AI.

> sekarang apa yang bisa kita lakukan

Sekarang kita bisa berhenti menambah materi massal dan membangun fondasinya dalam urutan ini:

1. Buat **Peta Kurikulum Kanonik v1** dari katalog 48 rumpun yang ada.

   Hasilnya bukan daftar bab panjang, tetapi peta:
   `domain → mapel → strand → konsep inti → unit belajar`

   Sekaligus kita tandai mana yang:
   - materi inti;
   - path ujian;
   - path karier;
   - materi khusus;
   - belum layak diproduksi karena belum punya standar.

2. Buat **template produksi resmi** yang langsung cocok dengan Studio Anda.

   Template satu unit harus menentukan:
   - tujuan dan prasyarat;
   - struktur artikel dan blok pedagogis;
   - konsep yang ditag;
   - checkpoint;
   - blueprint latihan: subtype soal, kesulitan, Bloom, jawaban/pembahasan;
   - kebutuhan web interaktif dan mode guru;
   - sumber akademik serta status review.

3. Jadikan satu materi sebagai “golden module”.

   Rekomendasi saya:
   `Matematika → Bilangan → Bilangan Bulat`

   Satu konsep ini dibuat benar-benar lengkap: artikel, blok visual, web interaktif garis bilangan, checkpoint, soal mudah–sulit, Bloom, mode guru, dan jalur remedial. Setelah selesai, template tersebut menjadi cetakan seluruh produksi berikutnya.

4. Hubungkan konsep ke fitur yang sudah ada.

   Yang perlu ditambahkan bukan mesin baru, melainkan tag konseptual yang konsisten pada:
   - item artikel;
   - bagian artikel;
   - grup soal;
   - soal individual;
   - CodeWeb/web interaktif.

   Dengan itu AI nanti dapat menjawab: “siswa gagal pada konsep apa?”, bukan hanya “siswa salah di kuis mana?”.

5. Standarkan CodeWeb.

   Pertahankan format website interaktif seperti contoh Alphabet, tetapi beri manifest dan event standar agar progresnya masuk ke Titian—bukan hanya tampil di browser.

Urutan paling efektif: **peta kanonik → template resmi → golden module → migrasi katalog lama → produksi massal**.

Saya sarankan kita mulai dari nomor 1 sekarang: memetakan dan membetulkan seluruh katalog lama menjadi struktur kanonik yang tidak duplikatif.

> ya

<details><summary>2 previous messages</summary>

> Saya mulai dari peta kanoniknya. Saya akan mempertahankan seluruh cakupan yang sudah Anda rencanakan, tetapi mengubah posisinya: mana yang benar-benar materi inti, mana yang menjadi bundel kurikulum, dan mana yang seharusnya menjadi learning path/tujuan—supaya produksi tidak berulang.
>
> <details><summary>Created a file</summary>
>
> - Wrote `./outputs/PETA_KANONIK_KURIKULUM_TITIAN_ASA_V1.md` (+142 -0)
>
> </details>
</details>

Peta kanonik v1 sudah dibuat: [PETA_KANONIK_KURIKULUM_TITIAN_ASA_V1.md](./outputs/PETA_KANONIK_KURIKULUM_TITIAN_ASA_V1.md).

Hasil utamanya:

- Seluruh 48 rumpun tetap dipertahankan, tetapi diposisikan ulang secara benar.
- IPA, IPAS, dan IPS menjadi bundel kurikulum yang mereferensikan konsep Sains/Sosial—bukan tiga perpustakaan konsep baru.
- Sastra Indonesia menjadi strand Bahasa Indonesia.
- Penalaran & Logika menjadi layanan lintas-domain.
- CPNS dan BUMN menjadi learning path karier/ujian, bukan mata pelajaran inti.
- Semua `custom` diberi daftar kode permanen yang harus dimigrasikan.
- Produksi diprioritaskan: Matematika, Bahasa Indonesia, Bahasa Inggris, lalu path CP/TKA/UTBK yang memakai ulang materi tersebut.

Langkah berikutnya sudah sangat jelas: kita pecah **Matematika** menjadi peta `strand → konsep → unit belajar`, lalu membangun satu “golden module” Bilangan Bulat sebagai standar produksi nyata.

> ya

<details><summary>2 previous messages</summary>

> Saya lanjutkan dengan peta Matematika. Saya akan memakai struktur konsep yang reusable lintas jenjang, lalu memetakan fase sekolah dan path ujian sebagai referensi di atasnya—bukan sebagai materi duplikat.
>
> <details><summary>Created a file, explored a file, a search, searched the web</summary>
>
> <details><summary>Explored a file, a search</summary>
>
> - Read `./DAFTAR_PELAJARAN_DAN_LEARNING_PATH.md`
> - Searched for `^####|^#####|^\| [^|]+ \|`
>
> </details>
>
> Searched the web for `site:kurikulum.kemdikbud.go.id/file/cp/dasmen CP Matematika Fase A F PDF ...`
>
> - Wrote `./outputs/PETA_MATEMATIKA_DAN_GOLDEN_MODULE_V1.md` (+208 -0)
>
> </details>
</details>

Peta Matematika dan satu golden module sudah dibuat: [PETA_MATEMATIKA_DAN_GOLDEN_MODULE_V1.md](./outputs/PETA_MATEMATIKA_DAN_GOLDEN_MODULE_V1.md).

Isinya mencakup:

- 7 strand Matematika kanonik, dari Bilangan hingga Matematika Terapan.
- Pemetaan seluruh topik Matematika lama agar tidak tumpang tindih.
- Aturan prasyarat antarkonsep.
- Desain lengkap golden module: **Menjumlahkan Bilangan Bulat Berbeda Tanda**.
- Struktur artikel Studio, widget garis bilangan, latihan adaptif, Bloom, kesulitan, remedial, mode guru, dan pemakaian ulang di tiga learning path.

Langkah paling tepat berikutnya adalah mengubah golden module ini menjadi **template produksi nyata di Content Studio**, lalu mengisi konten Bilangan Bulat pertama berdasarkan spesifikasi tersebut.

> kerjakan

<details><summary>6 previous messages</summary>

> Saya akan menerjemahkan golden module Bilangan Bulat menjadi aset nyata: template artikel, konfigurasi widget garis bilangan, dan blueprint kuis yang dapat diimpor/dimasukkan lewat Studio. Saya akan terlebih dahulu mencocokkan formatnya dengan struktur proyek aktif agar tidak membuat artefak yang tidak dapat dipakai.
>
> <details><summary>Explored 14 files, 5 searches, 2 lists, ran a command</summary>
>
> <details><summary>Explored 16 files, 5 searches, 2 lists</summary>
>
> - Listed files in `sanja-workspace`
> - Searched for `codeweb|widget_interact|Sematan Web|iframe|external.*web|concept_ids|concept_id` in `titian-backend-rust`
> - Searched for `codeweb|widget_interact|Sematan Web|iframe|external.*web|concept_ids|concept_id` in `titian-backend-rust`
> - Listed files in `titian-backend-rust`
> - Searched for `seed|content|module|quiz|interactive|codeweb`
> - Read `./titian-backend-rust/src/bin/seed_content_factory.rs`
> - Read `./titian-backend-rust/src/models/requests/module.rs`
> - Read `./titian-backend-rust/src/services/code_web_ai.rs`
> - Read `./titian-backend-rust/src/services/quiz_config.rs`
> - Read `./titian-web/src/components/studio/modules/code-web-editor.tsx`
> - Read `./titian-backend-rust/src/services/content_factory/blueprint.rs`
> - Read `./titian-backend-rust/src/services/content_factory/apply.rs`
> - Read `./titian-backend-rust/src/services/module_item.rs`
> - Searched for `code_web|CodeWeb|window.Titian|submitScore|complete\(` in `titian-backend-rust`
> - Read `./titian-web/src/components/belajar/lesson-content.tsx`
> - Read `./titian-web/src/app/(app)/belajar/[itemId]/page.tsx`
> - Read `./titian-backend-rust/src/services/module_item.rs`
> - Read `./titian-backend-rust/src/models/responses/module.rs`
> - Read `./titian-backend-rust/src/services/quiz_attempt.rs`
> - Read `./titian-web/src/components/belajar/lesson-content.tsx`
> - Searched for `post_complete|completeItem|mark.*complete|complete.*item|titian-score-submit|titian-module-complete` in `api-client.ts`
> - Read `./titian-backend-rust/src/handlers/item_rules.rs`
> - Read `./titian-backend-rust/src/routes/module.rs`
>
> </details>
>
> - Ran `sed -n '1,120p' titian-web/src/components/belajar/lesson-content.tsx
> rg -n "function .*Web|export function .*Web|const .*Web" titian-web/src/components/belajar/lesson-content.tsx
> git -C titian-web status --short
> git -C titian-backend-rust status --short`
>
> </details>
>
> Saya menemukan fondasi yang relevan sudah ada: item memang dapat ditag konsep, item `code_web` sudah didukung, dan kuis sudah punya taksonomi. Namun workspace aplikasi sedang berisi banyak perubahan belum di-commit, termasuk berkas CodeWeb baru; saya tidak akan mengubah berkas tersebut agar pekerjaan yang ada tidak tertimpa. Saya akan membuat paket golden module yang mandiri dan siap dimasukkan ke Studio, sambil mendokumentasikan satu celah integrasi CodeWeb yang perlu ditutup sebelum dipublikasikan.
>
> <details><summary>Created 4 files, edited a file, explored 2 files, 3 searches, ran a command</summary>
>
> <details><summary>Explored a file, 2 searches</summary>
>
> - Searched for `^::|^:::|\[\[|@example|common_trap|checkpoint|lesson_plan` in `agent`
> - Searched for `*.alm` in `agent`
> - Read `./titian-backend-rust/src/services/alm_parser.rs`
>
> </details>
>
> - Ran `sed -n '115,160p' titian-backend-rust/tests/integration/section_checkpoint_test.rs
> sed -n '1,160p' titian-backend-rust/src/services/lesson_plan.rs 2>/dev/null || true
> rg -n "pub struct .*LessonPlan|struct LessonPlan|checkpoint.*Question|LessonPlanSection" titian-backend-rust/src -g '*.rs' | sed -n '1,200p'`
>
> - Wrote `./outputs/golden-module-bilangan-bulat/README.md` (+31 -0)
> - Wrote `./outputs/golden-module-bilangan-bulat/concept-map.json` (+49 -0)
>
> - Wrote `./outputs/golden-module-bilangan-bulat/article-lesson-plan.json` (+134 -0)
>
> <details><summary>Explored a file, a search</summary>
>
> - Searched for `"two_column"|"note"|"steps"|"definition"|"common_trap"` in `block_schema.rs`
> - Read `./titian-backend-rust/src/services/block_schema.rs`
>
> </details>
>
> - Wrote `./outputs/golden-module-bilangan-bulat/article-lesson-plan.json` (+2 -2)
>
> - Wrote `./outputs/golden-module-bilangan-bulat/number-line-codeweb.html` (+29 -0)
>
> </details>
>

>
> Permission request
>
> Status: completed
> Reason: Anda meminta saya mengerjakan golden module di proyek Titian Asa. Saya perlu memeriksa dan menulis aset/template pada workspace aplikasi yang aktif.
> Response: granted
</details>
