# Pohon Hierarki Matematika Kanonik v1

Status: rancangan registry materi inti. Mengikuti `STANDAR_KURIKULUM_TITIAN_ASA.md` dan `PETA_MATEMATIKA_DAN_GOLDEN_MODULE_V1.md`.

## Aturan pakai

```text
Domain → Mata Pelajaran → Strand → Konsep/cluster → Unit Belajar
```

- **Unit Belajar** adalah aset terkecil yang dapat dituntaskan dan satu-satunya pemilik bank soal. Setiap unit memiliki bank kanonik **50 soal**, ditag konsep, kesulitan, Bloom, format respons, dan versi.
- Sesi latihan 10/20, 25, dan 50 soal hanya menarik komposisi dari bank unit yang sama; tidak membuat bank baru atau salinan soal.
- Fase, kelas, TKA/UTBK, dan kuliah adalah label/pemetaan pada unit; bukan cabang materi yang menggandakan unit.
- Kode di bawah bersifat stabil. Nama unit memakai kata kerja + objek kompetensi.

```text
mathematics
└─ matematika
   ├─ number
   ├─ algebra_functions
   ├─ geometry_measurement
   ├─ data_probability_statistics
   ├─ calculus_analysis
   ├─ discrete_logic_number_theory
   └─ modeling_applied
```

---

## 1. Strand `number` — Bilangan

```text
number
├─ number.whole_place_value — Bilangan cacah dan nilai tempat
│  ├─ Menentukan banyak benda dan lambang bilangan
│  ├─ Membandingkan dan mengurutkan bilangan cacah
│  ├─ Menguraikan bilangan berdasarkan nilai tempat
│  ├─ Membulatkan bilangan sesuai ketelitian yang diminta
│  └─ Mengestimasi hasil operasi bilangan cacah
├─ number.whole_operations — Operasi bilangan cacah
│  ├─ Menjumlahkan bilangan cacah
│  ├─ Mengurangkan bilangan cacah
│  ├─ Mengalikan bilangan cacah
│  ├─ Membagi bilangan cacah dan menafsirkan sisa
│  └─ Menyelesaikan operasi campuran dengan urutan yang benar
├─ number.integers — Bilangan bulat
│  ├─ Menempatkan bilangan bulat pada garis bilangan
│  ├─ Membandingkan dan mengurutkan bilangan bulat
│  ├─ Menentukan nilai mutlak bilangan bulat
│  ├─ Menjumlahkan bilangan bulat bertanda sama
│  ├─ Menjumlahkan bilangan bulat berbeda tanda
│  ├─ Mengurangkan bilangan bulat sebagai penjumlahan lawan
│  ├─ Mengalikan dan membagi bilangan bulat bertanda
│  └─ Menyelesaikan operasi campuran bilangan bulat
├─ number.factors_multiples — Faktor, kelipatan, dan keterbagian
│  ├─ Menentukan faktor dan kelipatan suatu bilangan
│  ├─ Menguji keterbagian bilangan
│  ├─ Menentukan faktorisasi prima
│  ├─ Menentukan FPB dengan faktorisasi atau algoritma Euklid
│  └─ Menentukan KPK dan menerapkannya pada masalah periodik
├─ number.fractions — Pecahan dan bilangan rasional
│  ├─ Memodelkan pecahan sebagai bagian, ukuran, dan hasil bagi
│  ├─ Menentukan pecahan senilai
│  ├─ Menyederhanakan dan membandingkan pecahan
│  ├─ Menjumlahkan dan mengurangkan pecahan
│  ├─ Mengalikan dan membagi pecahan
│  ├─ Mengubah pecahan campuran dan pecahan biasa
│  └─ Menyelesaikan operasi campuran bilangan rasional
├─ number.decimal_percent_ratio — Desimal, persen, rasio, dan proporsi
│  ├─ Menentukan nilai tempat pada bilangan desimal
│  ├─ Mengubah pecahan, desimal, dan persen
│  ├─ Menghitung operasi bilangan desimal
│  ├─ Menentukan rasio dan perbandingan senilai
│  ├─ Menentukan perbandingan berbalik nilai
│  ├─ Menggunakan skala pada peta dan model
│  └─ Menyelesaikan masalah persen, diskon, untung-rugi, bruto-neto-tara
├─ number.real_exponents_roots — Bilangan real, eksponen, dan akar
│  ├─ Mengklasifikasikan bilangan rasional dan irasional
│  ├─ Menggunakan sifat perpangkatan bilangan bulat
│  ├─ Menentukan bentuk akar dan menyederhanakannya
│  ├─ Merasionalkan penyebut bentuk akar
│  ├─ Menggunakan notasi ilmiah
│  └─ Mengestimasi dan membandingkan bilangan real
└─ number.complex — Bilangan kompleks
   ├─ Memodelkan satuan imajiner dan bidang kompleks
   ├─ Menjalankan operasi bilangan kompleks
   ├─ Mengubah bentuk kartesius dan polar
   ├─ Menerapkan teorema De Moivre
   └─ Menentukan akar bilangan kompleks
```

## 2. Strand `algebra_functions` — Aljabar dan Fungsi

```text
algebra_functions
├─ algebra.patterns_expressions — Pola dan ekspresi aljabar
│  ├─ Mengidentifikasi pola bilangan dan aturan suku ke-n
│  ├─ Memodelkan situasi dengan variabel
│  ├─ Mengidentifikasi koefisien, konstanta, dan suku sejenis
│  ├─ Menjumlahkan dan mengurangkan bentuk aljabar
│  ├─ Mengalikan serta membagi bentuk aljabar
│  ├─ Memfaktorkan bentuk aljabar
│  └─ Menyederhanakan pecahan aljabar
├─ algebra.linear_equations — Persamaan dan pertidaksamaan linear
│  ├─ Menyelesaikan persamaan linear satu variabel
│  ├─ Menyelesaikan pertidaksamaan linear satu variabel
│  ├─ Memodelkan masalah dengan persamaan linear
│  ├─ Menentukan grafik persamaan linear dua variabel
│  ├─ Menyelesaikan SPLDV secara grafik, substitusi, dan eliminasi
│  ├─ Menyelesaikan SPLTV
│  └─ Menentukan daerah solusi pertidaksamaan linear dua variabel
├─ algebra.quadratic — Fungsi, persamaan, dan pertidaksamaan kuadrat
│  ├─ Memfaktorkan dan melengkapkan kuadrat sempurna
│  ├─ Menentukan akar persamaan kuadrat
│  ├─ Menafsirkan diskriminan dan sifat akar
│  ├─ Menyusun persamaan kuadrat dari akar atau konteks
│  ├─ Menentukan grafik fungsi kuadrat
│  ├─ Menyelesaikan pertidaksamaan kuadrat
│  └─ Memodelkan masalah maksimum-minimum dengan fungsi kuadrat
├─ algebra.relations_functions — Relasi dan fungsi
│  ├─ Membedakan relasi dan fungsi
│  ├─ Menentukan domain, kodomain, dan range
│  ├─ Menentukan representasi fungsi (tabel, grafik, rumus, konteks)
│  ├─ Menentukan fungsi linear dan transformasi grafiknya
│  ├─ Menentukan fungsi rasional dan asimtotnya
│  ├─ Menentukan komposisi fungsi
│  └─ Menentukan fungsi invers
├─ algebra.exponential_logarithmic — Eksponen dan logaritma
│  ├─ Menentukan fungsi eksponen dan grafiknya
│  ├─ Menyelesaikan persamaan serta pertidaksamaan eksponen
│  ├─ Menentukan makna dan bentuk logaritma
│  ├─ Menggunakan sifat logaritma
│  ├─ Menyelesaikan persamaan serta pertidaksamaan logaritma
│  └─ Memodelkan pertumbuhan dan peluruhan eksponensial
├─ algebra.sequences_series — Barisan dan deret
│  ├─ Menentukan barisan aritmetika
│  ├─ Menentukan jumlah deret aritmetika
│  ├─ Menentukan barisan geometri
│  ├─ Menentukan jumlah deret geometri
│  ├─ Menentukan jumlah deret geometri tak hingga
│  ├─ Menggunakan notasi sigma
│  └─ Membuktikan pola dengan induksi matematika
├─ algebra.matrices_vectors — Matriks dan vektor
│  ├─ Mengklasifikasikan jenis dan ukuran matriks
│  ├─ Menjalankan operasi matriks
│  ├─ Menentukan determinan dan invers matriks
│  ├─ Menyelesaikan sistem linear dengan matriks
│  ├─ Memodelkan vektor di R² dan R³
│  ├─ Menjalankan operasi, dot product, dan cross product vektor
│  └─ Menentukan proyeksi vektor
└─ algebra.linear_algebra — Aljabar linear lanjut
   ├─ Menentukan ruang vektor dan subruang
   ├─ Menentukan basis, dimensi, dan kebebasan linear
   ├─ Menentukan transformasi linear dan matriks representasinya
   ├─ Menentukan nilai eigen dan vektor eigen
   ├─ Mendiagonalkan matriks
   └─ Menggunakan hasil kali dalam dan ortogonalitas
```

## 3. Strand `geometry_measurement` — Geometri dan Pengukuran

```text
geometry_measurement
├─ geometry.measurement — Besaran dan pengukuran
│  ├─ Mengukur dan mengonversi panjang, massa, waktu, dan kuantitas
│  ├─ Mengonversi satuan luas, volume, dan debit
│  ├─ Menentukan ketelitian, estimasi, dan satuan yang sesuai
│  └─ Menyelesaikan masalah pengukuran majemuk
├─ geometry.plane_shapes — Bangun datar dan relasi bidang
│  ├─ Mengklasifikasikan bangun datar berdasarkan sifatnya
│  ├─ Menentukan keliling dan luas bangun datar
│  ├─ Menentukan hubungan garis dan sudut
│  ├─ Menganalisis segitiga dan teorema Pythagoras
│  ├─ Menganalisis segiempat serta lingkaran
│  ├─ Menentukan busur, juring, dan sudut pusat
│  └─ Membuktikan kesebangunan dan kekongruenan
├─ geometry.solid_shapes — Bangun ruang dan dimensi tiga
│  ├─ Mengidentifikasi jaring-jaring dan unsur bangun ruang
│  ├─ Menentukan luas permukaan kubus, balok, prisma, dan limas
│  ├─ Menentukan volume prisma, limas, tabung, kerucut, dan bola
│  ├─ Menentukan volume bangun gabungan
│  ├─ Menentukan kedudukan titik, garis, dan bidang
│  ├─ Menentukan jarak dan sudut dalam ruang
│  └─ Menentukan proyeksi dan irisan bidang
├─ geometry.transformations_coordinates — Transformasi dan koordinat
│  ├─ Mengenali simetri, pencerminan, translasi, rotasi, dan dilatasi
│  ├─ Menentukan hasil komposisi transformasi
│  ├─ Menempatkan titik pada koordinat Kartesius
│  ├─ Menentukan jarak, titik tengah, dan gradien
│  ├─ Menentukan persamaan garis
│  └─ Menentukan persamaan lingkaran dan garis singgung
├─ geometry.trigonometry — Trigonometri
│  ├─ Mengubah ukuran sudut derajat dan radian
│  ├─ Menentukan perbandingan trigonometri segitiga siku-siku
│  ├─ Menentukan nilai sudut istimewa dan relasi sudut
│  ├─ Membuktikan dan menggunakan identitas trigonometri
│  ├─ Menerapkan aturan sinus, cosinus, dan luas segitiga
│  ├─ Menentukan grafik fungsi trigonometri
│  └─ Menyelesaikan persamaan serta rumus jumlah-selisih sudut
├─ geometry.analytic_conics — Geometri analitik dan irisan kerucut
│  ├─ Menentukan parabola
│  ├─ Menentukan elips
│  ├─ Menentukan hiperbola
│  └─ Mengubah dan menafsirkan persamaan umum irisan kerucut
└─ geometry.differential — Geometri diferensial
   ├─ Menganalisis kurva dan permukaan di R³
   ├─ Memodelkan manifold diferensiabel dan ruang tangen
   ├─ Menggunakan bentuk diferensial dan teorema Stokes
   ├─ Menentukan metrik Riemann, koneksi, dan geodesik
   └─ Menafsirkan kelengkungan
```

## 4. Strand `data_probability_statistics` — Data, Peluang, dan Statistika

```text
data_probability_statistics
├─ data.representation — Pengumpulan dan representasi data
│  ├─ Mengumpulkan dan mengklasifikasikan data
│  ├─ Membaca serta membuat tabel frekuensi
│  ├─ Membaca serta membuat diagram batang, garis, dan lingkaran
│  ├─ Membuat histogram dan distribusi frekuensi
│  └─ Menilai representasi data yang menyesatkan
├─ data.descriptive_statistics — Statistika deskriptif
│  ├─ Menentukan mean, median, dan modus data tunggal
│  ├─ Menentukan mean, median, dan modus data berkelompok
│  ├─ Menentukan kuartil, desil, dan persentil
│  ├─ Menentukan jangkauan, ragam, dan simpangan baku
│  └─ Menafsirkan ringkasan data untuk mengambil keputusan
├─ probability.foundations_counting — Peluang dan pencacahan dasar
│  ├─ Menentukan ruang sampel dan kejadian
│  ├─ Menghitung peluang kejadian sederhana
│  ├─ Menggunakan aturan penjumlahan dan perkalian
│  ├─ Menentukan permutasi dan kombinasi
│  ├─ Menentukan peluang kejadian majemuk
│  └─ Menentukan peluang bersyarat dan independensi
├─ probability.random_variables — Variabel acak dan distribusi
│  ├─ Memodelkan variabel acak diskrit dan kontinu
│  ├─ Menentukan distribusi binomial dan Poisson
│  ├─ Menentukan distribusi normal dan standardisasi
│  └─ Menggunakan nilai harapan dan varians
└─ statistics.inference — Statistika inferensial
   ├─ Menentukan distribusi sampling dan teorema limit pusat
   ├─ Menentukan estimasi titik dan interval kepercayaan
   ├─ Melakukan serta menafsirkan uji hipotesis
   ├─ Menentukan korelasi dan regresi
   └─ Melakukan serta menafsirkan ANOVA
```

## 5. Strand `calculus_analysis` — Kalkulus dan Analisis

```text
calculus_analysis
├─ calculus.limits_continuity — Limit dan kontinuitas
│  ├─ Menafsirkan limit secara grafis, numerik, dan aljabar
│  ├─ Menentukan limit fungsi aljabar dan trigonometri
│  ├─ Menentukan limit di ketakhinggaan
│  └─ Menguji kekontinuan fungsi
├─ calculus.differentiation — Turunan
│  ├─ Menafsirkan turunan sebagai laju perubahan
│  ├─ Menggunakan aturan turunan dasar dan aturan rantai
│  ├─ Menentukan turunan fungsi trigonometri dan implisit
│  ├─ Menganalisis kemonotonan, titik stasioner, dan titik belok
│  └─ Memodelkan optimasi dengan turunan
├─ calculus.integration — Integral
│  ├─ Menentukan integral tak tentu
│  ├─ Menggunakan integral tentu dan teorema dasar kalkulus
│  ├─ Menentukan integral substitusi, parsial, dan trigonometri
│  ├─ Menentukan luas daerah di bawah/antara kurva
│  └─ Menentukan volume benda putar
├─ calculus.multivariable — Kalkulus multivariabel
│  ├─ Memodelkan fungsi multivariabel
│  ├─ Menentukan turunan parsial, gradien, dan turunan berarah
│  ├─ Menentukan integral lipat dua dan tiga
│  └─ Menentukan integral garis dan permukaan
├─ analysis.real — Analisis real
│  ├─ Menentukan supremum dan infimum pada bilangan real
│  ├─ Membuktikan kekonvergenan barisan dan deret
│  ├─ Menggunakan definisi epsilon-delta untuk limit dan kontinuitas
│  ├─ Membuktikan teorema nilai rata-rata
│  └─ Mengonstruksi integral Riemann
├─ analysis.differential_equations — Persamaan diferensial
│  ├─ Memodelkan persamaan diferensial orde satu
│  ├─ Menyelesaikan PD terpisah dan PD linear orde satu
│  ├─ Menyelesaikan PD orde dua homogen/nonhomogen
│  └─ Memodelkan fenomena sains dan teknik dengan PD
└─ analysis.advanced — Analisis lanjut
   ├─ Menggunakan ukuran dan integral Lebesgue
   ├─ Menerapkan teorema konvergensi dan ruang Lp
   ├─ Menganalisis ruang Banach, Hilbert, dan operator linear
   ├─ Menggunakan analisis kompleks, integral kontur, dan residu
   └─ Memodelkan PDP: panas, gelombang, Laplace, dan Fourier
```

## 6. Strand `discrete_logic_number_theory` — Diskrit, Logika, dan Teori Bilangan

```text
discrete_logic_number_theory
├─ discrete.logic_sets_proof — Logika, himpunan, dan pembuktian
│  ├─ Menentukan nilai kebenaran pernyataan
│  ├─ Menggunakan negasi, konjungsi, disjungsi, implikasi, dan biimplikasi
│  ├─ Menggunakan kuantor serta menarik kesimpulan yang valid
│  ├─ Mengoperasikan himpunan, relasi, dan fungsi diskrit
│  ├─ Menulis pembuktian langsung, kontraposisi, kontradiksi, dan induksi
│  └─ Menggunakan logika orde pertama dan sistem formal
├─ discrete.combinatorics_graphs — Kombinatorika, graf, dan rekursi
│  ├─ Menggunakan prinsip pencacahan lanjut
│  ├─ Memodelkan graf, lintasan, dan jaringan
│  ├─ Menganalisis pohon dan aplikasinya
│  ├─ Menyusun relasi rekurensi
│  └─ Menilai keterhitungan dan masalah henti
├─ number_theory.elementary — Teori bilangan elementer
│  ├─ Menggunakan keterbagian dan algoritma Euklid
│  ├─ Menentukan prima, faktorisasi, dan fungsi aritmetika dasar
│  ├─ Menghitung dalam aritmetika modular
│  ├─ Menyelesaikan kongruensi linear
│  └─ Menerapkan teorema Fermat kecil dan Euler
├─ number_theory.algebraic — Aljabar abstrak
│  ├─ Menganalisis grup dan teorema Sylow
│  ├─ Menganalisis ring, ideal, daerah integral, dan lapangan
│  ├─ Menggunakan modul dan perluasan lapangan
│  ├─ Menerapkan teori Galois
│  └─ Menggunakan dasar aljabar homologis dan representasi grup
└─ discrete.foundations — Fondasi formal matematika
   ├─ Menggunakan teori himpunan aksiomatik (ZFC)
   ├─ Membandingkan ordinal dan kardinal
   ├─ Menilai aksioma pilihan dan hipotesis kontinum
   └─ Menerapkan teori model serta teorema Gödel
```

## 7. Strand `modeling_applied` — Pemodelan dan Matematika Terapan

```text
modeling_applied
├─ modeling.quantitative_reasoning — Penalaran kuantitatif lintas-strand
│  ├─ Memilih informasi kuantitatif yang relevan
│  ├─ Mengestimasi dan memeriksa kewajaran hasil
│  ├─ Menerjemahkan soal cerita menjadi model matematika
│  ├─ Membandingkan strategi penyelesaian
│  └─ Menjelaskan keputusan berbasis data atau perhitungan
├─ modeling.optimization_operations — Optimisasi dan riset operasi
│  ├─ Memodelkan program linear
│  ├─ Menentukan nilai optimum fungsi objektif
│  ├─ Menyelesaikan masalah transportasi dan penugasan
│  ├─ Menggunakan dualitas dan syarat KKT
│  └─ Menggunakan optimisasi nonlinear, stokastik, dan kombinatorial
├─ modeling.numerical_computation — Metode numerik dan komputasi
│  ├─ Menentukan akar persamaan secara numerik
│  ├─ Menginterpolasi data serta mengintegralkan secara numerik
│  ├─ Menganalisis galat, kondisi, dan stabilitas
│  ├─ Mendekomposisi matriks (LU, QR, SVD)
│  ├─ Menyelesaikan sistem linear besar dan nilai eigen secara numerik
│  └─ Menerapkan beda hingga, elemen hingga, spektral, dan Monte Carlo
├─ modeling.finance_games — Keuangan dan teori permainan
│  ├─ Memodelkan bunga tunggal, majemuk, dan anuitas
│  ├─ Menentukan nilai kini, NPV, dan arus kas
│  ├─ Memodelkan strategi dalam teori permainan
│  └─ Menilai risiko melalui peluang dan simulasi
├─ modeling.mechanics — Mekanika matematis
│  ├─ Memodelkan kinematika dengan vektor
│  ├─ Memodelkan dinamika dan hukum Newton
│  ├─ Menganalisis momentum, impuls, dan kesetimbangan
│  └─ Memodelkan gerak harmonik sederhana
└─ modeling.stochastic_processes — Proses stokastik
   ├─ Memodelkan rantai Markov waktu diskrit dan kontinu
   ├─ Menggunakan proses Poisson dan proses titik
   ├─ Menggunakan martingale dan gerak Brown
   ├─ Menerapkan kalkulus Itô dan PDS stokastik
   └─ Memodelkan aplikasi stokastik pada keuangan
```

## Pemetaan kedalaman dan latihan unit

| Kedalaman | Tujuan latihan | Tarikan bank soal 50 unit |
|---|---|---|
| F0–F1 | pengenalan dan prosedur | 10/20 soal, dominan mudah–menengah |
| F2 | koneksi konsep dan representasi | 25 soal, komposisi seimbang |
| F3–F4 | penalaran, transfer, pembuktian/formal | 50 soal atau blueprint evaluasi khusus |

Contoh unit: `number.integers → Menjumlahkan bilangan bulat berbeda tanda`. Unit itu memiliki satu bank 50 soal; path Fondasi SMP, remedial, dan TKA hanya menarik sesi serta aturan XP berbeda dari bank tersebut.
