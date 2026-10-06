# Dokumentasi Matematika: Pohon Hierarki sampai Blueprint Modul v1

Status: dokumen produksi utuh Matematika Titian Asa. Urutannya sengaja mengikuti alur kerja tim: dokumentasi sistem → pohon kurikulum → Blueprint modul → Bagian mesin Modul → latihan dan bank soal → checkpoint → tindak lanjut.

## 1. Dokumentasi sistem dan aturan pakai

### Tujuan dokumen

Dokumen ini adalah spesifikasi sebelum materi dibuat di Studio. Ia tidak langsung berisi artikel dan 50 soal per modul; ia memberi identitas, struktur, aturan produksi, serta kontrak asesmen agar AI dan editor membuat aset yang konsisten. Konten dan item aktual diterbitkan ke mesin Modul berdasarkan Blueprint ini.

### Istilah yang dipakai

| Istilah | Arti operasional di Titian Asa |
|---|---|
| Domain | payung katalog, misalnya `mathematics` |
| Mata pelajaran | rumah akademik permanen: `matematika` |
| Strand | untai kompetensi stabil, misalnya `number` atau `algebra_functions` |
| Konsep | kelompok kemampuan reusable, misalnya `number.integers` |
| Modul kanonik | setiap leaf pada pohon; satu paket belajar yang dapat dituntaskan |
| Blueprint Modul | rancangan satu modul untuk mesin Studio: Bagian, konten, media, latihan, checkpoint, dan aturan lulus |
| Bagian | tahap belajar yang tampil di panel kiri mesin Modul |
| Item | satu blok konten/media atau satu soal; item soal selalu punya tag dan versi |
| Bank soal | tepat 50 item asesmen kanonik milik satu modul |
| Learning path | urutan referensi modul untuk fase, kelas, ujian, atau remedial; tidak memiliki salinan modul |

### Pemetaan ke mesin Modul

| Blueprint | Implementasi di mesin Anda |
|---|---|
| `module_id`, judul, durasi, target peserta | header Modul dan input generator otomatis |
| `Bagian[]` | struktur dan tombol **Tambah Bagian** |
| konten | pembahasan, definisi, contoh, langkah, rumus, tabel, catatan, perbandingan, kesalahan umum |
| media | gambar, audio, video, sematan web, berkas, atau tautan |
| grup latihan | kelompok latihan di bawah Bagian yang menarik item bertag dari bank modul |
| item soal | kartu soal berisi tipe, kunci/rubrik, pembahasan, kesulitan, Bloom, dan tag |
| checkpoint | grup soal penutup yang memilih item checkpoint dari bank |
| tindak lanjut | aturan sistem menuju remedial, modul berikutnya, atau pengayaan |

### Prinsip non-duplikasi

Satu leaf pohon memiliki satu modul, satu Blueprint aktif per versi, dan satu bank 50 soal. Jika modul yang sama muncul di Fase D, remedial, TKA, atau kelas guru, sistem mengubah urutan, jumlah soal, dan aturan kelulusan—bukan membuat artikel atau bank baru.

## 2. Pohon kurikulum dan kontrak arsitektur

```text
mathematics
└─ matematika
   └─ strand
      └─ konsep
         └─ modul kanonik (setiap leaf pohon)
            ├─ blueprint modul
            │  └─ Bagian → konten/media → grup latihan → item
            └─ bank kanonik 50 soal
```

- Pohon `POHON_HIERARKI_MATEMATIKA_V1.md` adalah daftar leaf/modul Matematika yang otoritatif.
- Setiap leaf—misalnya **Menentukan hasil penjumlahan bilangan bulat berbeda tanda**—menjadi satu modul kanonik, bukan satu Bagian atau satu soal.
- Setiap modul memiliki satu `module_id`, satu Blueprint aktif per versi, dan **satu bank kanonik tepat 50 soal**.
- Bagian modul, kuis mandiri, sesi latihan 10/20, 25, 50, remedial, pengayaan, dan path hanya mereferensikan item dari bank modul itu. Tidak ada duplikasi item.
- Fase/kelas, TKA/UTBK, Cambridge, dan kuliah adalah label atau path. Mereka tidak membuat salinan modul Matematika.

## 3. Pohon kanonik dan rumah blueprint

| Strand | Konsep | Bentuk modul dominan | Blueprint |
|---|---|---|---|
| `number` | `whole_place_value`, `whole_operations`, `integers`, `factors_multiples`, `fractions`, `decimal_percent_ratio`, `real_exponents_roots`, `complex` | representasi, prosedur, transfer kontekstual | `MATH-CONCEPT`, `MATH-PROCEDURE`, `MATH-MODEL` |
| `algebra_functions` | `patterns_expressions`, `linear_equations`, `quadratic`, `relations_functions`, `exponential_logarithmic`, `sequences_series`, `matrices_vectors`, `linear_algebra` | simbol, transformasi, pembuktian, pemodelan | `MATH-PROCEDURE`, `MATH-INTERPRET`, `MATH-PROOF` |
| `geometry_measurement` | `measurement`, `plane_shapes`, `solid_shapes`, `transformations_coordinates`, `trigonometry`, `analytic_conics`, `differential` | visual-spasial, pengukuran, pembuktian | `MATH-VISUAL`, `MATH-PROCEDURE`, `MATH-PROOF` |
| `data_probability_statistics` | `representation`, `descriptive_statistics`, `foundations_counting`, `random_variables`, `inference` | data, peluang, keputusan berbukti | `MATH-INTERPRET`, `MATH-PROCEDURE`, `MATH-MODEL` |
| `calculus_analysis` | `limits_continuity`, `differentiation`, `integration`, `multivariable`, `real`, `differential_equations`, `advanced` | representasi perubahan, prosedur, pembuktian | `MATH-INTERPRET`, `MATH-PROCEDURE`, `MATH-PROOF`, `MATH-MODEL` |
| `discrete_logic_number_theory` | `logic_sets_proof`, `combinatorics_graphs`, `elementary`, `algebraic`, `foundations` | logika, struktur diskrit, pembuktian | `MATH-CONCEPT`, `MATH-PROOF`, `MATH-PROCEDURE` |
| `modeling_applied` | `quantitative_reasoning`, `optimization_operations`, `numerical_computation`, `finance_games`, `mechanics`, `stochastic_processes` | masalah kontekstual, keputusan, simulasi | `MATH-MODEL`, `MATH-INTERPRET`, `MATH-PROCEDURE` |

Nama leaf di pohon menentukan nama modul dan tujuan utama. Kode konsep menentukan rumah, relasi prasyarat, template Blueprint, dan bank soal. Contoh aturan ID:

```text
Konsep: number.integers
Leaf: Menjumlahkan bilangan bulat berbeda tanda
Module ID: math.number.integers.addition-opposite-signs.v1
Blueprint ID: math.number.integers.addition-opposite-signs.blueprint.v1
Question bank ID: math.number.integers.addition-opposite-signs.bank.v1
```

## 4. Blueprint yang tersedia untuk modul Matematika

### `MATH-CONCEPT` — Memahami representasi dan hubungan

Digunakan untuk leaf seperti menempatkan bilangan pada garis bilangan, mengklasifikasikan bangun, membedakan relasi dan fungsi, atau menentukan nilai kebenaran pernyataan.

```text
Bagian 1 — Fenomena/representasi awal
Bagian 2 — Konsep, definisi, dan contoh-kontras
Bagian 3 — Menghubungkan beberapa representasi
Bagian 4 — Latihan dan checkpoint
```

Blok utama: definisi, contoh, perbandingan, kesalahan umum, tabel/diagram, dan widget bila representasi dapat dimanipulasi. Item utama: pilihan, matching, diagram labeling, gap fill, dan produksi penjelasan singkat.

### `MATH-PROCEDURE` — Menjalankan dan menjelaskan prosedur

Digunakan untuk leaf seperti operasi bilangan, persamaan, faktorisasi, turunan, integral, peluang, atau metode numerik.

```text
Bagian 1 — Diagnosis prasyarat dan makna operasi
Bagian 2 — Strategi/langkah dengan contoh beralasan
Bagian 3 — Variasi prosedur dan pengecekan hasil
Bagian 4 — Aplikasi atau transfer
Bagian 5 — Checkpoint penguasaan
```

Blok utama: contoh dua kolom, langkah, rumus, kesalahan umum, tabel, serta simulasi/peraga jika membantu. Item utama: isian numerik, gap fill, susun langkah, pilihan diagnostik, dan jawaban singkat.

### `MATH-VISUAL` — Menalar melalui bentuk, ruang, dan transformasi

Digunakan untuk leaf Geometri, koordinat, transformasi, trigonometri, serta visualisasi kalkulus.

```text
Bagian 1 — Mengamati objek dan sifat
Bagian 2 — Membangun konstruksi/representasi
Bagian 3 — Mengukur, menghitung, atau mentransformasi
Bagian 4 — Menjelaskan hubungan dan pembuktian ringan
Bagian 5 — Checkpoint
```

Blok utama: gambar beranotasi, langkah konstruksi, perbandingan, widget geometri/grafik, dan catatan strategi. Item utama: diagram labeling, matching, isian, pilihan kompleks, dan produksi penjelasan.

### `MATH-INTERPRET` — Membaca data, grafik, atau struktur matematis

Digunakan untuk leaf representasi data, fungsi, limit, distribusi, statistika, dan penalaran kuantitatif.

```text
Bagian 1 — Orientasi stimulus dan pertanyaan
Bagian 2 — Strategi membaca representasi
Bagian 3 — Anotasi/contoh interpretasi
Bagian 4 — Analisis kesalahan atau keputusan
Bagian 5 — Checkpoint transfer
```

Blok utama: tabel, grafik, infografik, contoh anotasi, perbandingan, dan kesalahan umum. Item utama: table completion, pilihan kompleks, matching, jawaban singkat, dan produksi argumentasi data.

### `MATH-PROOF` — Menyusun alasan dan pembuktian

Digunakan untuk leaf kesebangunan, identitas, induksi, logika, analisis real, aljabar linear, dan teori bilangan lanjut.

```text
Bagian 1 — Klaim, definisi, dan kondisi yang digunakan
Bagian 2 — Membaca contoh pembuktian beranotasi
Bagian 3 — Melengkapi atau menyusun langkah bukti
Bagian 4 — Memeriksa kesahihan dan memperbaiki bukti
Bagian 5 — Bukti/performa akhir dengan rubrik
```

Blok utama: definisi, teorema, langkah, contoh-kontras, kesalahan umum, dan rubrik. Item utama: susun, gap fill, pilihan kompleks untuk kesalahan logika, serta produksi jawaban dengan rubrik.

### `MATH-MODEL` — Memodelkan konteks dan mengambil keputusan

Digunakan untuk leaf persamaan cerita, optimasi, keuangan, mekanika matematis, peluang terapan, dan proses stokastik.

```text
Bagian 1 — Memahami konteks, kuantitas, dan batasan
Bagian 2 — Membuat asumsi serta model
Bagian 3 — Menyelesaikan dan memeriksa model
Bagian 4 — Menafsirkan hasil, risiko, dan alternatif
Bagian 5 — Tugas transfer/checkpoint
```

Blok utama: stimulus kontekstual, tabel, grafik, langkah pemodelan, catatan asumsi, dan perbandingan strategi. Item utama: pilihan data relevan, isian, flow chart, table completion, dan produksi model/penjelasan.

## 5. Pembedahan Blueprint hingga Bagian modul

Setiap leaf memakai satu blueprint di atas lalu menyesuaikan tujuan, contoh, media, dan miskonsepsi. Setiap Bagian pada mesin Modul wajib menyimpan: judul, tujuan Bagian, durasi, konten/blok media, serta referensi grup latihan dari bank modul.

```text
Bagian Blueprint
├─ bagian_id dan judul
├─ tujuan Bagian
├─ durasi
├─ konten[]
│  ├─ tipe blok
│  └─ tujuan pedagogis
├─ media/aktivitas[]
│  ├─ jenis media atau widget
│  └─ fallback aksesibel
├─ grup_latihan[]
│  └─ query tag: module_id + bagian_id + fungsi
└─ checkpoint_bagian opsional
   └─ query tag: checkpoint_bagian
```

| Elemen mesin | Aturan Matematika |
|---|---|
| Pembahasan | menjelaskan alasan, bukan hanya rumus; selalu menyertakan contoh dan pengecekan hasil bila prosedural |
| Definisi/rumus | memuat syarat penggunaan dan contoh noncontoh bila ada risiko salah pakai |
| Langkah | setiap langkah menyebut alasan atau aturan yang digunakan |
| Kesalahan umum | memetakan kesalahan ke tag `miskonsepsi_target` pada bank soal |
| Media/interaktif | dipakai bila visualisasi/manipulasi lebih bermakna daripada teks; misalnya garis bilangan, pecahan, grafik fungsi, geometri, atau simulasi peluang |
| Latihan Bagian | menampilkan item bank yang ditag `bagian_id`; bukan soal lokal yang disalin |
| Checkpoint | menarik 4–6 item dari 10 item checkpoint bank dan mencakup tujuan inti |

## 6. Latihan dan bank kanonik 50 soal per modul

Setiap modul Matematika memakai struktur bank yang sama; substansi, tipe soal, dan proporsi Bloom disesuaikan dengan target kompetensi.

| Fungsi | Jumlah | Penempatan di mesin Modul |
|---|---:|---|
| Diagnostik prasyarat | 4 | awal modul atau sebelum Bagian 1 |
| Latihan per Bagian | 22 | ditarik oleh grup latihan di setiap Bagian; minimal 4 item per Bagian |
| Latihan mandiri/transfer | 8 | sesi latihan mandiri atau akhir Bagian aplikasi |
| Checkpoint akhir | 10 | bank khusus checkpoint; 4–6 ditampilkan adaptif pada satu percobaan |
| Remedial | 4 | muncul saat pola salah tertentu terdeteksi |
| Pengayaan | 2 | muncul saat kompetensi inti telah tuntas |
| **Total** | **50** | bank kanonik tunggal per versi modul |

### Matriks kesulitan dan Bloom

| Sumbu | Target bank 50 |
|---|---|
| Kesulitan | 15 mudah, 25 menengah, 10 sulit |
| Bloom | minimal C1: 5; C2: 8; C3: 14; C4: 12; C5: 6; C6: 2; tiga item cadangan pada Bloom paling relevan |
| Dimensi pengetahuan | faktual, konseptual, prosedural, metakognitif—dipilih sesuai leaf |
| Format respons | kombinasi pilihan, isian, susun, matching/diagram, table completion, dan produksi/rubrik bila kompetensi memerlukannya |

Untuk modul prosedural, C3–C4 biasanya dominan. Untuk pembuktian dan pemodelan, porsi C4–C6 lebih besar tetapi kesulitan tetap dijaga pada 15–25–10. Kesulitan tidak boleh dipakai sebagai pengganti tag Bloom.

## 7. Checkpoint, kelulusan, dan adaptasi

```text
Diagnosis prasyarat gagal
  → modul prasyarat atau latihan visual dasar

Checkpoint <80% atau pola miskonsepsi terdeteksi
  → item remedial dari bank yang sama + ulang checkpoint ekuivalen

Checkpoint ≥80% dan seluruh tujuan inti terwakili
  → modul leaf berikutnya pada relasi prasyarat

Checkpoint ≥90% serta item transfer benar
  → dua item pengayaan atau node pemodelan/pembuktian lanjut
```

Aturan spesifik per leaf dapat menambah syarat performa. Contoh modul pembuktian tidak cukup dengan skor objektif: satu item produksi harus mencapai kategori minimum pada rubrik alasan matematis.

## 8. Golden blueprint: Menjumlahkan Bilangan Bulat Berbeda Tanda

```text
module_id: math.number.integers.addition-opposite-signs.v1
konsep: number.integers
template: MATH-PROCEDURE
durasi: 25–35 menit mandiri; 15–20 menit mode guru
prasyarat:
  - Menempatkan dan membandingkan bilangan bulat pada garis bilangan.
  - Menentukan nilai mutlak dasar.
tujuan:
  - Memodelkan arah penjumlahan pada garis bilangan.
  - Menghitung jumlah dua bilangan bertanda berbeda.
  - Menjelaskan tanda hasil dengan nilai mutlak.
  - Memeriksa kewajaran hasil dan menggunakan konteks sederhana.
```

| Bagian | Konten/media | Latihan bank yang ditarik |
|---|---|---|
| 1. Makna tanda | definisi arah positif/negatif, contoh garis bilangan | diagnosis + latihan membedakan arah dan posisi |
| 2. Aturan selisih | langkah nilai mutlak, contoh dua kolom, kesalahan “selalu menjumlah” | isian/gap fill dan pilihan miskonsepsi |
| 3. Strategi dan verifikasi | perbandingan garis bilangan–aturan selisih, konteks suhu/saldo/skor | table/cerita pendek dan transfer |
| 4. Checkpoint | 4–6 item adaptif dari bank checkpoint | konsep, prosedur, diagnosis tanda, dan transfer |

Media utama: widget `number-line` dengan konfigurasi contoh, kontrol guru, reset, dan event Titian. Widget tidak menyatakan mastery sendiri; checkpoint menentukan kelulusan.

Bank 50 mengikuti matriks di atas. Contoh tag item:

```text
item_id: math.number.integers.addition-opposite-signs.q27.v1
bagian_id: aturan-selisih
fungsi: latihan_terarah
tipe_soal: isian_numerik
kesulitan: menengah
bloom: C3
dimensi_pengetahuan: prosedural
miskonsepsi_target: menjumlahkan_nilai_mutlak_pada_tanda_berbeda
```

Kelulusan: checkpoint minimal 80%, tanpa gagal pada dua item tanda berbeda berturut-turut. Remedial mengarahkan ke garis bilangan atau latihan nilai mutlak; lanjut mengarah ke pengurangan sebagai penjumlahan lawan; pengayaan mengarah ke operasi campuran dan masalah multi-langkah.

## 9. Pemetaan jenis leaf ke Blueprint

| Ciri leaf | Blueprint utama | Contoh leaf |
|---|---|---|
| mengenali, membandingkan, mengklasifikasikan, menentukan representasi | `MATH-CONCEPT` | membedakan relasi dan fungsi; mengklasifikasikan bangun datar |
| menghitung, menyelesaikan, mengubah bentuk, menjalankan operasi | `MATH-PROCEDURE` | menyelesaikan SPLDV; menentukan integral tentu |
| mengukur, mengonstruksi, mentransformasi, memvisualkan | `MATH-VISUAL` | menentukan hasil komposisi transformasi; menentukan jarak dan sudut dalam ruang |
| membaca, menafsirkan, menganalisis grafik/data | `MATH-INTERPRET` | menilai diagram menyesatkan; menafsirkan diskriminan |
| membuktikan, menguji kesahihan, menggeneralisasi | `MATH-PROOF` | membuktikan kesebangunan; menggunakan induksi matematika |
| memodelkan, memilih strategi, mengambil keputusan | `MATH-MODEL` | memodelkan pertumbuhan eksponensial; menentukan nilai optimum fungsi objektif |

Jika satu leaf memiliki dua karakter, pilih satu blueprint utama dan tambahkan Bagian dari blueprint kedua. Contoh `Memodelkan masalah maksimum-minimum dengan fungsi kuadrat` memakai `MATH-MODEL` dengan Bagian prosedur turunan/fungsi kuadrat dari `MATH-PROCEDURE`.

## 10. Definition of Done modul Matematika

Sebuah leaf pohon Matematika siap terbit hanya jika:

1. memiliki `module_id`, konsep rumah, prasyarat, versi, dan Blueprint;
2. setiap Bagian dapat dirender pada mesin Modul dengan konten/media yang sesuai;
3. bank berisi tepat 50 item, terdistribusi lintas Bagian, kesulitan, Bloom, dan fungsi;
4. semua item memiliki kunci atau rubrik, pembahasan, tag miskonsepsi, dan status review;
5. checkpoint mengukur semua tujuan inti serta menjalankan remedial/lanjut/pengayaan;
6. media interaktif, bila digunakan, memiliki manifest, fallback aksesibel, dan event yang dapat dilacak;
7. ahli Matematika menyetujui ketepatan konsep, contoh, pengecoh, dan aturan kelulusan.
