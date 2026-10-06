# Pohon Hierarki Keagamaan v1

Status: materi inti kanonik untuk domain `religious_studies`. Dibuat dengan struktur yang sama seperti Matematika: `mata pelajaran → strand → konsep/cluster → unit belajar`.

## Keputusan struktur

```text
religious_studies
├─ pai_budi_pekerti            ← PAI untuk sekolah umum
├─ islam_madrasah              ← struktur mata pelajaran madrasah
├─ islam_lanjut
├─ agama_buddha
├─ agama_hindu
├─ agama_katolik
├─ agama_kristen
└─ agama_khonghucu
```

`pai_budi_pekerti` berbeda dari `islam_madrasah` pada **bundel kurikulum, kedalaman, dan konteks institusi**, bukan karena semua pengetahuan Islam harus dibuat dua kali. Unit yang kompetensinya setara dapat memakai sumber belajar dan bank soal kanonik bersama, lalu dua mata pelajaran tersebut memasukkannya ke path/bundel berbeda.

Setiap unit di bawah wajib memiliki tujuan terukur, prasyarat, sumber acuan, penelaah akademik/keagamaan, versioning, serta bank soal unit. Untuk mata pelajaran keagamaan, perubahan substansi selalu memerlukan peninjauan ahli tradisi terkait.

---

## 1. `pai_budi_pekerti` — Pendidikan Agama Islam dan Budi Pekerti (sekolah umum)

```text
pai_budi_pekerti
├─ quran_hadis
│  ├─ konsep: literasi Al-Qur'an
│  │  ├─ Unit: Mengenali huruf dan tanda baca Al-Qur'an sesuai tahap belajar
│  │  ├─ Unit: Membaca potongan ayat dengan kaidah tajwid dasar
│  │  ├─ Unit: Menghafal dan melafalkan surah/ayat pilihan dengan benar
│  │  └─ Unit: Memeriksa bacaan melalui umpan balik guru atau audio
│  ├─ konsep: memahami pesan ayat dan hadis
│  │  ├─ Unit: Menjelaskan makna umum ayat atau hadis pilihan
│  │  ├─ Unit: Menghubungkan pesan ayat/hadis dengan situasi sehari-hari
│  │  ├─ Unit: Membedakan pesan utama, konteks, dan penerapan yang bertanggung jawab
│  │  └─ Unit: Menyampaikan refleksi nilai secara santun
│  └─ konsep: tajwid terapan
│     ├─ Unit: Mengidentifikasi hukum nun mati dan tanwin
│     ├─ Unit: Mengidentifikasi hukum mim mati dan mad dasar
│     └─ Unit: Menerapkan tajwid pada bacaan ayat pilihan
├─ akidah
│  ├─ konsep: iman dan sumber ajaran
│  │  ├─ Unit: Menjelaskan rukun iman sesuai tahap perkembangan
│  │  ├─ Unit: Menjelaskan sifat-sifat Allah dalam bahasa yang tepat dan beradab
│  │  ├─ Unit: Meneladani iman kepada malaikat, kitab, rasul, hari akhir, serta qada-qadar
│  │  └─ Unit: Menghubungkan keyakinan dengan sikap tanggung jawab sehari-hari
│  └─ konsep: identitas dan keberagamaan
│     ├─ Unit: Menunjukkan adab beragama di lingkungan sekolah
│     └─ Unit: Menghormati pemeluk agama dan keyakinan lain secara damai
├─ akhlak
│  ├─ konsep: akhlak pribadi
│  │  ├─ Unit: Mempraktikkan jujur, amanah, disiplin, dan tanggung jawab
│  │  ├─ Unit: Mengelola emosi dan menghindari perilaku merugikan
│  │  └─ Unit: Membiasakan evaluasi diri dan perbaikan perilaku
│  ├─ konsep: akhlak sosial
│  │  ├─ Unit: Berempati, tolong-menolong, dan menghargai perbedaan
│  │  ├─ Unit: Menerapkan adab kepada keluarga, guru, teman, dan tetangga
│  │  └─ Unit: Menyelesaikan konflik secara adil dan damai
│  └─ konsep: akhlak lingkungan dan digital
│     ├─ Unit: Menjaga lingkungan sebagai tanggung jawab bersama
│     └─ Unit: Menerapkan etika bermedia dan komunikasi digital
├─ fikih
│  ├─ konsep: bersuci dan ibadah
│  │  ├─ Unit: Mempraktikkan kebersihan dan bersuci sesuai tuntunan dasar
│  │  ├─ Unit: Menjelaskan dan mempraktikkan salat sesuai tahap belajar
│  │  ├─ Unit: Menjelaskan puasa, zakat, dan ibadah sosial dalam konteksnya
│  │  └─ Unit: Mengidentifikasi hikmah ibadah bagi diri dan masyarakat
│  └─ konsep: muamalah dan halal-haram
│     ├─ Unit: Menerapkan kejujuran dalam jual beli dan pergaulan
│     ├─ Unit: Menilai pilihan konsumsi yang halal, aman, dan bertanggung jawab
│     └─ Unit: Menerapkan prinsip keadilan serta kepedulian sosial
└─ sejarah_peradaban_islam
   ├─ konsep: nabi dan keteladanan
   │  ├─ Unit: Menceritakan peristiwa kehidupan Nabi Muhammad secara runtut
   │  └─ Unit: Meneladani kepemimpinan, kejujuran, dan kasih sayang Nabi
   ├─ konsep: perkembangan peradaban Islam
   │  ├─ Unit: Menjelaskan perkembangan masyarakat Islam awal
   │  ├─ Unit: Mengidentifikasi kontribusi peradaban Islam bagi ilmu dan budaya
   │  └─ Unit: Menganalisis keragaman sejarah Islam secara kontekstual
   └─ konsep: Islam di Indonesia
      ├─ Unit: Menjelaskan proses penyebaran Islam di Indonesia secara multiperspektif
      └─ Unit: Menghargai tradisi lokal yang selaras dengan nilai kemaslahatan
```

## 2. `islam_madrasah` — Mata pelajaran keislaman Madrasah

```text
islam_madrasah
├─ quran_hadis
│  ├─ konsep: qiraah dan tajwid
│  │  ├─ Unit: Membaca Al-Qur'an dengan makhraj dan tajwid bertahap
│  │  ├─ Unit: Menganalisis hukum tajwid dalam ayat pilihan
│  │  └─ Unit: Mempraktikkan tilawah dengan adab yang tepat
│  ├─ konsep: ulumul_quran_dasar
│  │  ├─ Unit: Menjelaskan fungsi Al-Qur'an sebagai sumber ajaran
│  │  └─ Unit: Menafsirkan pesan ayat pilihan dengan rujukan yang sesuai tingkat belajar
│  └─ konsep: hadis
│     ├─ Unit: Menjelaskan kedudukan hadis sebagai sumber ajaran
│     ├─ Unit: Memahami pesan hadis tematik pilihan
│     └─ Unit: Menerapkan nilai hadis dalam proyek sosial sederhana
├─ akidah_akhlak
│  ├─ konsep: tauhid dan keimanan
│  │  ├─ Unit: Menjelaskan konsep tauhid sesuai tingkat dan sumber yang ditetapkan
│  │  ├─ Unit: Menghubungkan rukun iman dengan perilaku bertanggung jawab
│  │  └─ Unit: Menganalisis tantangan akidah secara proporsional dan beradab
│  ├─ konsep: akhlak_mahmudah
│  │  ├─ Unit: Mempraktikkan ikhlas, sabar, syukur, tawakal, dan adil
│  │  └─ Unit: Merancang kebiasaan akhlak baik di sekolah dan masyarakat
│  └─ konsep: akhlak_madzmumah
│     ├─ Unit: Mengenali dampak perilaku tercela pada diri dan lingkungan
│     └─ Unit: Menentukan strategi perbaikan perilaku secara reflektif
├─ fikih
│  ├─ konsep: thaharah_dan_ibadah
│  │  ├─ Unit: Menerapkan ketentuan bersuci dalam situasi sehari-hari
│  │  ├─ Unit: Menjelaskan rukun, syarat, dan hikmah salat
│  │  ├─ Unit: Menjelaskan ketentuan puasa, zakat, haji/umrah sesuai tahap
│  │  └─ Unit: Menilai praktik ibadah dengan adab terhadap perbedaan yang diakui
│  └─ konsep: muamalah
│     ├─ Unit: Menerapkan prinsip akad dan kejujuran dalam transaksi sederhana
│     ├─ Unit: Menilai isu makanan, keuangan, dan pergaulan dari prinsip fikih dasar
│     └─ Unit: Menganalisis kemaslahatan pada persoalan sosial sesuai tingkat belajar
├─ sejarah_kebudayaan_islam
│  ├─ konsep: sirah
│  │  ├─ Unit: Menyusun kronologi sirah Nabi Muhammad
│  │  └─ Unit: Menilai keteladanan sirah untuk persoalan masa kini
│  ├─ konsep: peradaban_islam
│  │  ├─ Unit: Menjelaskan perkembangan dinasti dan pusat peradaban secara kontekstual
│  │  ├─ Unit: Menganalisis kontribusi tokoh ilmuwan dan cendekiawan Muslim
│  │  └─ Unit: Membandingkan sumber sejarah dan perspektifnya
│  └─ konsep: islam_nusantara
│     ├─ Unit: Menelusuri perkembangan Islam di Nusantara
│     └─ Unit: Menilai peran ulama dan institusi Islam dalam masyarakat Indonesia
└─ bahasa_arab_keagamaan
   ├─ Unit: Membaca kosakata dan frasa Arab yang relevan dengan teks pembelajaran
   ├─ Unit: Memahami struktur kalimat Arab dasar
   └─ Unit: Memahami teks Arab sederhana dengan strategi membaca
```

`bahasa_arab_keagamaan` mereferensikan unit inti dari mata pelajaran `bahasa_arab`; ia hanya memiliki konteks/kurasi madrasah, bukan bank tata bahasa kedua.

## 3. `islam_lanjut` — Studi Islam Lanjut

```text
islam_lanjut
├─ ulumul_quran_tafsir
│  ├─ Unit: Mengenali prinsip dasar ulumul Qur'an dan tafsir
│  ├─ Unit: Membandingkan pendekatan tafsir dalam batas sumber yang ditetapkan
│  └─ Unit: Menyusun analisis ayat tematik dengan rujukan serta adab ilmiah
├─ ulumul_hadis
│  ├─ Unit: Menjelaskan unsur dan klasifikasi hadis tingkat dasar
│  ├─ Unit: Mengenali prinsip verifikasi sanad/matan secara pengantar
│  └─ Unit: Menilai penggunaan hadis populer dengan rujukan yang tepat
├─ ushul_fikih_fikih_lanjut
│  ├─ Unit: Menjelaskan sumber dan metode penetapan hukum tingkat pengantar
│  ├─ Unit: Membedakan ruang kesepakatan dan perbedaan pendapat fikih
│  └─ Unit: Menganalisis kasus kontemporer dengan kerangka yang ditetapkan ahli
├─ kalam_filsafat_islam
│  ├─ Unit: Mengenali sejarah persoalan dan aliran pemikiran Islam
│  ├─ Unit: Menganalisis argumen secara logis dan beradab
│  └─ Unit: Menulis kajian pengantar berbasis sumber akademik
└─ tasawuf_etika
   ├─ Unit: Menjelaskan istilah dan sejarah tasawuf secara proporsional
   ├─ Unit: Merefleksikan akhlak, pengendalian diri, dan tanggung jawab sosial
   └─ Unit: Membandingkan sumber secara kritis dengan pendampingan ahli
```

## 4. `agama_buddha` — Pendidikan Agama Buddha dan Budi Pekerti

```text
agama_buddha
├─ keyakinan_dan_ajaran
│  ├─ Unit: Menjelaskan nilai inti ajaran Buddha sesuai tahap belajar
│  ├─ Unit: Menghubungkan ajaran dengan perilaku penuh kesadaran
│  └─ Unit: Merefleksikan sebab-akibat tindakan secara bertanggung jawab
├─ kitab_sejarah_teladan
│  ├─ Unit: Mengenal kisah Buddha dan tokoh teladan
│  ├─ Unit: Menjelaskan peristiwa penting dalam sejarah Buddhis
│  └─ Unit: Meneladani kebijaksanaan dan welas asih dalam kehidupan
├─ etika_dan_meditasi
│  ├─ Unit: Mempraktikkan perilaku tidak menyakiti dan kepedulian
│  ├─ Unit: Melatih perhatian penuh sesuai panduan yang aman dan sesuai usia
│  └─ Unit: Menyelesaikan konflik dengan welas asih serta kebijaksanaan
└─ komunitas_dan_keberagaman
   ├─ Unit: Menjelaskan peran komunitas keagamaan dalam kehidupan sosial
   └─ Unit: Menghormati keragaman agama dan budaya
```

## 5. `agama_hindu` — Pendidikan Agama Hindu dan Budi Pekerti

```text
agama_hindu
├─ tattwa
│  ├─ Unit: Menjelaskan konsep ketuhanan dan keyakinan Hindu sesuai tahap belajar
│  ├─ Unit: Menghubungkan ajaran tattwa dengan tanggung jawab pribadi
│  └─ Unit: Menjelaskan nilai keseimbangan manusia, alam, dan ketuhanan
├─ susila
│  ├─ Unit: Menerapkan kejujuran, pengendalian diri, dan kepedulian
│  ├─ Unit: Menganalisis akibat tindakan bagi diri serta lingkungan
│  └─ Unit: Membangun relasi yang damai dan menghormati perbedaan
├─ acara_dan_praktik
│  ├─ Unit: Mengenal makna ibadah dan hari suci sesuai tradisi
│  └─ Unit: Menerapkan adab dalam praktik keagamaan dan lingkungan
└─ sejarah_dan_kitab
   ├─ Unit: Mengenal sumber ajaran, cerita suci, dan tokoh teladan
   └─ Unit: Menafsirkan pesan moral cerita secara kontekstual
```

## 6. `agama_katolik` — Pendidikan Agama Katolik dan Budi Pekerti

```text
agama_katolik
├─ kitab_suci_dan_tradisi
│  ├─ Unit: Mengenal Kitab Suci dan tradisi Gereja sesuai tahap belajar
│  ├─ Unit: Menafsirkan pesan teks dengan bimbingan konteks yang tepat
│  └─ Unit: Menghubungkan pesan iman dengan kehidupan sehari-hari
├─ iman_dan_perayaan
│  ├─ Unit: Menjelaskan pokok iman dan perayaan liturgi sesuai tahap belajar
│  └─ Unit: Menghayati perayaan iman dengan sikap hormat dan aktif
├─ moral_dan_pelayanan
│  ├─ Unit: Menerapkan kasih, keadilan, pengampunan, dan kepedulian
│  ├─ Unit: Menilai pilihan moral dengan hati nurani yang dibentuk
│  └─ Unit: Merancang aksi pelayanan bagi sesama dan lingkungan
└─ gereja_dan_masyarakat
   ├─ Unit: Menjelaskan peran Gereja dalam masyarakat
   └─ Unit: Membangun dialog serta persaudaraan lintas iman
```

## 7. `agama_kristen` — Pendidikan Agama Kristen dan Budi Pekerti

```text
agama_kristen
├─ alkitab_dan_teologi_dasar
│  ├─ Unit: Mengenal Alkitab dan narasi iman sesuai tahap belajar
│  ├─ Unit: Memahami pesan teks dalam konteks pembelajaran yang sesuai
│  └─ Unit: Menghubungkan iman dengan identitas serta tanggung jawab pribadi
├─ yesus_dan_teladan
│  ├─ Unit: Menjelaskan teladan Yesus dalam kasih dan pelayanan
│  └─ Unit: Menerapkan nilai kasih dalam keluarga, sekolah, dan masyarakat
├─ etika_dan_spiritualitas
│  ├─ Unit: Mengembangkan kejujuran, pengampunan, dan keadilan
│  ├─ Unit: Mempraktikkan refleksi serta disiplin spiritual sesuai tradisi
│  └─ Unit: Menilai tantangan kehidupan dengan pertimbangan iman dan etika
└─ gereja_dan_keberagaman
   ├─ Unit: Menjelaskan peran gereja dan warga dalam kehidupan bersama
   └─ Unit: Membangun perdamaian serta penghormatan lintas iman
```

## 8. `agama_khonghucu` — Pendidikan Agama Khonghucu dan Budi Pekerti

```text
agama_khonghucu
├─ keyakinan_dan_kitab
│  ├─ Unit: Mengenal keyakinan dan kitab suci Khonghucu sesuai tahap belajar
│  ├─ Unit: Memahami nilai kebajikan serta hubungan manusia dengan Tian
│  └─ Unit: Menafsirkan pesan ajaran dengan bimbingan sumber yang tepat
├─ etika_kebajikan
│  ├─ Unit: Menerapkan ren, yi, li, zhi, dan xin dalam perilaku sehari-hari
│  ├─ Unit: Mengembangkan bakti, hormat, dan tanggung jawab keluarga
│  └─ Unit: Menyelesaikan masalah secara bijaksana serta harmonis
├─ ibadah_dan_tradisi
│  ├─ Unit: Mengenal makna ibadah, upacara, dan hari besar
│  └─ Unit: Menerapkan adab dalam praktik tradisi keagamaan
└─ sejarah_dan_masyarakat
   ├─ Unit: Mengenal Nabi Kongzi dan tokoh teladan
   └─ Unit: Menghargai peran umat Khonghucu dalam masyarakat majemuk
```

## Relasi PAI sekolah umum dan Madrasah

| Kompetensi inti | Rumah utama | Penggunaan PAI umum | Penggunaan Madrasah |
|---|---|---|---|
| Membaca Al-Qur'an bertajwid dasar | `islam_madrasah.quran_hadis` | direferensikan dengan kedalaman/target PAI | unit inti mapel Al-Qur'an Hadis |
| Menjelaskan pesan ayat/hadis pilihan | `islam_madrasah.quran_hadis` | direferensikan dan dikontekstualkan sebagai PAI | unit inti mapel Al-Qur'an Hadis |
| Mempraktikkan akhlak baik | `pai_budi_pekerti.akhlak` | unit inti PAI | direferensikan oleh Akidah Akhlak |
| Menerapkan ibadah dasar | `pai_budi_pekerti.fikih` | unit inti PAI | direferensikan/diperdalam oleh Fikih |
| Menganalisis sejarah peradaban Islam | `islam_madrasah.sejarah_kebudayaan_islam` | unit pilihan/pengayaan PAI | unit inti SKI |

Relasi ini adalah awal registry, bukan putusan teologis final. Pemilik akademik dan penelaah dari tiap tradisi wajib meninjau batas materi, istilah, sumber, serta pemetaan fase sebelum produksi/publikasi.
