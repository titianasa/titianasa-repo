# Pohon Hierarki Domain Lain Titian Asa v1

Status: registry kurikulum kanonik setelah Matematika. Acuan: `STANDAR_KURIKULUM_TITIAN_ASA.md` dan `PETA_KANONIK_KURIKULUM_TITIAN_ASA_V1.md`.

## Aturan bersama

```text
Domain → Mata Pelajaran → Strand → Konsep/cluster → Unit Belajar
```

- Unit memakai nama kerja + objek kompetensi dan menjadi pemilik bank asesmen/unit versioning.
- Bundel sekolah (IPA, IPAS, IPS, Kurikulum Indonesia, Cambridge) serta path ujian/karier hanya mereferensikan unit ini.
- Bahasa lain memakai template struktur yang setara agar kualitas, aksesibilitas, dan pelacakan mastery konsisten.

---

## 1. `indonesian` — Bahasa Indonesia

```text
indonesian
└─ Bahasa Indonesia
   ├─ menyimak
   │  ├─ Memahami gagasan dan informasi eksplisit dalam teks lisan
   │  ├─ Menyimpulkan informasi implisit dalam teks lisan
   │  ├─ Mengevaluasi tujuan, sudut pandang, dan keandalan pembicara
   │  └─ Menanggapi informasi lisan secara relevan
   ├─ membaca_memirsa
   │  ├─ Menemukan informasi eksplisit pada teks informasi
   │  ├─ Menyimpulkan makna kata, gagasan, dan hubungan antaride
   │  ├─ Menganalisis struktur, argumen, dan bias teks
   │  ├─ Membandingkan sumber serta mengevaluasi kredibilitasnya
   │  └─ Menafsirkan teks multimodal: tabel, infografik, dan video
   ├─ berbicara_mempresentasikan
   │  ├─ Menyampaikan gagasan dengan struktur yang jelas
   │  ├─ Berdiskusi, bertanya, dan menanggapi secara santun
   │  ├─ Menyampaikan argumen berbasis bukti
   │  └─ Mempresentasikan informasi untuk audiens dan tujuan tertentu
   ├─ menulis
   │  ├─ Menulis kalimat dan paragraf efektif
   │  ├─ Merencanakan, menyusun, serta merevisi teks informasi
   │  ├─ Menulis teks argumentasi dan eksposisi
   │  ├─ Menulis teks prosedur, laporan, ulasan, dan korespondensi
   │  └─ Menulis karya kreatif dan multimodal
   ├─ kebahasaan
   │  ├─ Menggunakan ejaan, tanda baca, dan kapitalisasi
   │  ├─ Memilih kata baku, makna kata, dan majas secara tepat
   │  ├─ Membentuk kalimat efektif dan kohesi paragraf
   │  └─ Menerapkan tata bahasa sesuai konteks formal/informal
   └─ sastra
      ├─ Mengapresiasi puisi, prosa, dan drama
      ├─ Menganalisis unsur intrinsik serta konteks karya
      └─ Mencipta dan mementaskan karya sastra
```

## 2. `english` — Bahasa Inggris

```text
english
└─ Bahasa Inggris
   ├─ receptive_listening
   │  ├─ Mengenali bunyi, kata, dan informasi eksplisit
   │  ├─ Memahami ide utama, detail, inferensi, dan sikap pembicara
   │  └─ Mengevaluasi tujuan serta keandalan teks lisan
   ├─ receptive_reading
   │  ├─ Memahami kosakata dalam konteks
   │  ├─ Menemukan gagasan utama dan detail pendukung
   │  ├─ Membuat inferensi dan menilai argumen
   │  └─ Membaca teks akademik, fungsional, dan sastra
   ├─ productive_speaking
   │  ├─ Mengucapkan bunyi, tekanan kata, dan intonasi
   │  ├─ Berinteraksi dalam percakapan transaksional/interpersonal
   │  ├─ Menyampaikan opini dan argumen
   │  └─ Mempresentasikan topik dengan kelancaran sesuai CEFR
   ├─ productive_writing
   │  ├─ Menulis kalimat, paragraf, dan teks koheren
   │  ├─ Menulis deskripsi, narasi, prosedur, dan laporan
   │  ├─ Menulis argumentasi serta tanggapan akademik
   │  └─ Merevisi tulisan berdasarkan rubrik
   ├─ grammar_vocabulary
   │  ├─ Menggunakan kelas kata, tenses, aspek, dan modalitas
   │  ├─ Menggunakan frasa, klausa, serta kalimat kompleks
   │  ├─ Mengembangkan kosakata umum, akademik, dan kolokasi
   │  └─ Menggunakan strategi pembentukan dan penebakan kata
   └─ pronunciation
      ├─ Membedakan fonem dan pasangan bunyi minimal
      ├─ Memproduksi bunyi sulit, ritme, serta intonasi
      └─ Memantau dan memperbaiki pelafalan mandiri
```

Catatan: CEFR, IELTS, TOEFL, TOEIC, dan Cambridge adalah path/pemetaan kemampuan. Mereka tidak memiliki salinan unit grammar atau vocabulary.

## 3. `other_languages` — Bahasa Arab, Mandarin, Jepang, Korea, Jerman, Prancis

```text
other_languages
├─ Arabic | Mandarin | Japanese | Korean | German | French
│  ├─ sistem_bunyi_tulisan
│  │  ├─ Mengenali dan memproduksi bunyi/fonem
│  │  ├─ Membaca serta menulis aksara/sistem ejaan
│  │  └─ Menggunakan nada, goresan, harakat, atau romanisasi bila relevan
│  ├─ kosakata_dan_tata_bahasa
│  │  ├─ Menggunakan kosakata berdasarkan tema dan fungsi komunikasi
│  │  ├─ Membentuk frasa serta kalimat dasar
│  │  ├─ Menggunakan struktur tata bahasa sesuai tingkat kemahiran
│  │  └─ Menggunakan register dan kesantunan bahasa
│  ├─ menyimak_membaca
│  │  ├─ Memahami teks lisan fungsional
│  │  ├─ Memahami teks tulis dari literal sampai inferensial
│  │  └─ Menafsirkan konteks budaya dalam teks
│  ├─ berbicara_menulis
│  │  ├─ Berinteraksi dalam situasi sehari-hari
│  │  ├─ Menyampaikan informasi dan opini
│  │  └─ Menulis teks fungsional serta kreatif
│  └─ budaya_dan_strategi
│     ├─ Membandingkan praktik budaya secara beretika
│     └─ Menerapkan strategi belajar bahasa mandiri
```

Setiap bahasa memiliki registry unit spesifiknya; template ini mencegah struktur bahasa dibangun dari nol, tetapi tidak memaksakan tata bahasa satu bahasa ke bahasa lain.

## 4. `science` — Sains

```text
science
├─ keterampilan_ilmiah
│  ├─ Mengamati, mengukur, dan mengajukan pertanyaan ilmiah
│  ├─ Merumuskan hipotesis serta merancang penyelidikan
│  ├─ Mengolah data, menyimpulkan, dan mengomunikasikan bukti
│  └─ Mengevaluasi risiko, etika, dan keterbatasan penyelidikan
├─ physics
│  ├─ mekanika: Memodelkan gerak, gaya, energi, momentum, dan fluida
│  ├─ gelombang_optik: Menganalisis getaran, gelombang, bunyi, cahaya, dan optik
│  ├─ listrik_magnet: Menganalisis muatan, rangkaian, medan, dan induksi
│  └─ fisika_modern: Menjelaskan atom, radioaktivitas, relativitas dasar, dan teknologi
├─ chemistry
│  ├─ materi: Mengklasifikasikan materi, perubahan, dan pemisahan campuran
│  ├─ atom_ikatan: Memodelkan struktur atom, periodisitas, serta ikatan
│  ├─ reaksi: Menyetarakan, menghitung stoikiometri, dan menginterpretasi energi reaksi
│  ├─ larutan: Menganalisis konsentrasi, asam-basa, redoks, dan kesetimbangan
│  └─ kimia_terapan: Menilai kimia karbon, material, lingkungan, dan keselamatan
├─ biology
│  ├─ organisme: Menganalisis sel, jaringan, sistem organ, dan homeostasis
│  ├─ kehidupan: Menjelaskan reproduksi, pertumbuhan, genetika, dan evolusi
│  ├─ ekologi: Memodelkan ekosistem, populasi, keanekaragaman, dan konservasi
│  └─ bioteknologi: Menilai aplikasi serta etika bioteknologi
└─ earth_space
   ├─ Menganalisis struktur bumi, cuaca, iklim, dan bencana
   ├─ Menjelaskan sumber daya serta perubahan lingkungan
   └─ Memodelkan tata surya, bintang, galaksi, dan eksplorasi antariksa
```

`IPA` dan `IPAS` adalah bundel fase yang menarik unit dari `science` (serta sosial untuk IPAS), bukan mapel kanonik baru.

## 5. `social_sciences` — Ilmu Sosial dan Kewargaan

```text
social_sciences
├─ history
│  ├─ Menggunakan kronologi, periodisasi, dan sumber sejarah
│  ├─ Menganalisis sejarah Indonesia dan sejarah dunia
│  ├─ Mengevaluasi sebab-akibat, perubahan-keberlanjutan, dan multiperspektif
│  └─ Menulis argumen sejarah berbasis sumber
├─ geography
│  ├─ Membaca peta, skala, citra, dan data geospasial
│  ├─ Menganalisis litosfer, atmosfer, hidrosfer, dan biosfer
│  ├─ Menganalisis penduduk, mobilitas, dan interaksi ruang
│  └─ Merancang respons terhadap risiko bencana dan isu lingkungan
├─ economics
│  ├─ Menjelaskan kelangkaan, pilihan, dan sistem ekonomi
│  ├─ Menganalisis pasar, harga, produksi, dan konsumsi
│  ├─ Menganalisis pendapatan nasional, inflasi, dan kebijakan ekonomi
│  └─ Menilai perdagangan, pembangunan, dan ekonomi global
├─ sociology_anthropology_psychology
│  ├─ Menganalisis interaksi sosial, kelompok, institusi, dan perubahan sosial
│  ├─ Menganalisis budaya, identitas, keberagaman, dan metode etnografi
│  └─ Memahami perilaku serta perkembangan psikologis tanpa membuat diagnosis klinis
└─ civic_education
   ├─ Memahami Pancasila, konstitusi, hukum, dan hak warga negara
   ├─ Berpartisipasi demokratis serta menyelesaikan konflik secara damai
   └─ Menilai isu publik, media, dan kewargaan digital secara kritis
```

`IPS` adalah bundel fase yang mereferensikan unit sosial ini.

## 6. `computing` — Informatika dan Literasi Digital

```text
computing
├─ systems_hardware
│  ├─ Menjelaskan perangkat keras, perangkat lunak, dan sistem operasi
│  └─ Mengelola berkas, perangkat, serta praktik penggunaan yang aman
├─ networks_internet
│  ├─ Menjelaskan jaringan, internet, web, dan layanan cloud
│  └─ Menerapkan keamanan akun, privasi, dan respons insiden dasar
├─ data_information
│  ├─ Mengumpulkan, membersihkan, menyimpan, dan memvisualisasikan data
│  ├─ Membaca spreadsheet serta membuat rumus dasar
│  └─ Menilai kualitas data, bias, lisensi, dan perlindungan data pribadi
├─ computational_thinking_programming
│  ├─ Mengurai masalah, membuat algoritma, dan memakai representasi data
│  ├─ Membuat program dengan urutan, percabangan, perulangan, dan fungsi
│  ├─ Menguji, men-debug, mendokumentasikan, dan berkolaborasi pada kode
│  └─ Membangun aplikasi/web sederhana sesuai tingkat kemampuan
├─ ai_literacy
│  ├─ Menjelaskan cara kerja, manfaat, serta keterbatasan AI
│  ├─ Menggunakan AI secara aman, kritis, dan beretika
│  └─ Mengevaluasi bias, privasi, halusinasi, dan atribusi AI
└─ digital_creation
   ├─ Membuat dokumen, presentasi, media visual, dan audio digital
   └─ Merencanakan proyek digital dengan aksesibilitas serta lisensi yang tepat
```

## 7. `arts_health_life` — Seni, Kesehatan, dan Keterampilan Hidup

```text
arts_health_life
├─ arts
│  ├─ seni_rupa: Mengamati, mencipta, mengkurasi, dan merefleksikan karya visual
│  ├─ musik: Mendengar, memainkan, mencipta, serta mementaskan musik
│  ├─ tari: Mengeksplorasi gerak, mencipta, dan menampilkan tari
│  └─ teater: Memerankan, menyutradarai, memproduksi, serta mengapresiasi teater
├─ physical_education_health
│  ├─ Mengembangkan gerak lokomotor, nonlokomotor, dan manipulatif
│  ├─ Menerapkan strategi permainan, kebugaran, dan keselamatan olahraga
│  ├─ Menerapkan gizi, kesehatan reproduksi sesuai usia, P3K, dan kebencanaan
│  └─ Mengembangkan kesehatan mental, relasi sehat, dan regulasi diri
├─ craft_entrepreneurship
│  ├─ Merancang serta membuat produk prakarya dengan aman
│  ├─ Mengelola bahan, proses, kualitas, dan keberlanjutan
│  └─ Memasarkan serta mengevaluasi produk/kegiatan wirausaha
└─ life_skills_financial
   ├─ Mengelola anggaran, tabungan, utang, risiko, dan perlindungan konsumen
   ├─ Berkomunikasi profesional, berkolaborasi, dan mengelola proyek
   └─ Menyusun CV, portofolio, dan rencana pendidikan/karier
```

## 8. `religious_studies` — Keagamaan

```text
religious_studies
├─ Islam_madrasah
│  ├─ Al-Qur'an_Hadis: Membaca, memahami, dan menerapkan nilai teks secara kontekstual
│  ├─ Akidah_Akhlak: Memahami keyakinan serta membangun akhlak dalam tindakan
│  ├─ Fikih: Menerapkan prinsip ibadah dan muamalah sesuai sumber serta konteks
│  └─ SKI: Menganalisis sejarah kebudayaan Islam melalui sumber dan multiperspektif
├─ Islam_lanjut
│  ├─ Menganalisis ushul fikih, tafsir, hadis, kalam, dan tasawuf dengan penelaah ahli
│  └─ Menerapkan metodologi studi teks serta etika perbedaan pandangan
├─ Buddha | Hindu | Katolik | Kristen | Khonghucu
│  ├─ Memahami ajaran, kitab/sumber, sejarah, dan praktik per tradisi
│  ├─ Mengembangkan budi pekerti serta refleksi moral
│  └─ Menghormati keberagaman keyakinan dan dialog antariman
└─ literasi_lintas_agama
   ├─ Membedakan pengetahuan agama, pengalaman pribadi, dan klaim faktual
   └─ Berdialog secara hormat tanpa menilai kebenaran iman peserta lain
```

Setiap tradisi memerlukan pemilik akademik dan penelaah ahli; struktur setara tidak berarti menyamakan isi teologisnya.

## 9. `career_vocational` — Karier dan Kejuruan

```text
career_vocational
├─ career_readiness
│  ├─ Memetakan minat, kekuatan, dan pilihan karier
│  ├─ Menyusun CV, surat lamaran, portofolio, dan profil profesional
│  ├─ Berlatih wawancara, komunikasi kerja, dan etika profesional
│  └─ Mengelola proyek, waktu, serta kolaborasi kerja
├─ accounting
│  ├─ Mencatat transaksi dan jurnal umum
│  ├─ Memposting buku besar dan menyusun neraca saldo
│  ├─ Menyusun laporan keuangan dasar
│  └─ Menganalisis biaya, perpajakan dasar, dan pengendalian internal
├─ business_management
│  ├─ Memodelkan pelanggan, nilai produk, dan model bisnis
│  ├─ Mengelola pemasaran, operasi, SDM, dan keuangan dasar
│  └─ Mengembangkan usaha secara etis dan berkelanjutan
└─ automotive
   ├─ Menerapkan K3 dan penggunaan alat bengkel
   ├─ Menganalisis mesin, pemindah tenaga, chassis, dan kelistrikan
   ├─ Mendiagnosis gangguan serta melakukan perawatan kendaraan
   └─ Mendokumentasikan pekerjaan dan layanan pelanggan
```

Program SMK lain ditambahkan per kompetensi kerja, bukan sebagai “mapel SMK” tunggal. CPNS/BUMN adalah **learning path** yang mereferensikan `career_readiness`, kewargaan, penalaran, dan kompetensi formasi.

## 10. `reasoning` — Penalaran Lintas-Domain

```text
reasoning
├─ logic_argumentation
│  ├─ Membedakan klaim, alasan, bukti, asumsi, dan kesimpulan
│  ├─ Menilai kesahihan penalaran serta sesat pikir
│  └─ Menyusun argumen tertulis dan lisan berbasis bukti
├─ problem_solving
│  ├─ Memahami masalah, memilih strategi, dan memeriksa solusi
│  ├─ Memecah masalah kompleks serta mengelola batasan
│  └─ Mengevaluasi solusi alternatif dan dampaknya
├─ media_information_literacy
│  ├─ Memverifikasi sumber, konteks, bukti, dan gambar/media
│  ├─ Mendeteksi misinformasi, manipulasi, serta bias
│  └─ Mengutip dan mengatribusi sumber secara bertanggung jawab
└─ quantitative_literacy
   ├─ Membaca angka, tabel, grafik, dan risiko dalam konteks
   ├─ Mengestimasi serta menilai kewajaran pernyataan kuantitatif
   └─ Membuat keputusan berbasis data tanpa menggandakan konsep Matematika
```

## Urutan produksi v1

1. P0: Bahasa Indonesia, Bahasa Inggris, lalu registry Sains dan Informatika.
2. P1: Sosial/Kewargaan, Seni-Kesehatan-Keterampilan Hidup, dan Madrasah bersama ahli.
3. P2: Bahasa lain, kejuruan, studi agama lanjut, dan spesialisasi sosial.

Sebelum produksi massal per mata pelajaran, tiap strand perlu dipecah lagi oleh ahli domain menjadi konsep atomik ber-ID stabil dan Unit Belajar yang memiliki tujuan, prasyarat, sumber, manifest interaktif bila diperlukan, serta bank 50 soal per unit.
