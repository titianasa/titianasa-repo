# Arsitektur Taksonomi dan Relasi Learning Path v1

Status: penyempurnaan dari pohon domain sebelumnya. Dokumen ini menjadi aturan utama bila domain memiliki lebih dari satu mata pelajaran.

## Keputusan inti

**Domain adalah payung katalog, bukan simpul kurikulum.** Domain tidak memiliki strand, konsep, atau unit secara langsung.

Pohon akademik selalu dimulai dari **mata pelajaran**:

```text
Domain
└─ Mata Pelajaran
   └─ Strand
      └─ Konsep
         └─ Unit Belajar
            ├─ sumber belajar dan interaktif
            ├─ bank soal unit
            └─ bukti penguasaan
```

Dengan aturan ini, domain dengan satu mapel dan banyak mapel menggunakan struktur yang sama. Yang berbeda hanya jumlah mapelnya.

## 1. Mengapa domain tidak boleh punya strand sendiri

Contoh `mathematics` berisi satu mata pelajaran, yaitu Matematika. Maka tampak wajar bila pohonnya adalah `Matematika → Bilangan → Bilangan Bulat → Unit`.

Namun `science` berisi Fisika, Kimia, Biologi, dan Bumi-Antariksa. Membuat strand bersama seperti `mekanika`, `atom`, atau `ekologi` langsung di bawah Sains akan membuat pohon tidak konsisten: strand itu sebenarnya milik satu mapel, bukan Sains secara keseluruhan.

Struktur yang benar:

```text
science
├─ physics
│  └─ mechanics → motion → Memodelkan gerak lurus
├─ chemistry
│  └─ atomic_structure → atoms → Menjelaskan struktur atom
├─ biology
│  └─ ecology → ecosystems → Menganalisis interaksi ekosistem
└─ earth_space
   └─ earth_systems → weather → Menafsirkan data cuaca
```

`science` boleh memiliki metadata, pemilik akademik, filter, dan bundel pembelajaran. Namun ia tidak memiliki pohon konsep sendiri.

## 2. Fungsi masing-masing objek

| Objek | Fungsi | Wajib? | Boleh dimiliki oleh |
|---|---|---:|---|
| Domain | pengelompokan produk dan navigasi tingkat atas | Ya | satu atau banyak mata pelajaran |
| Mata pelajaran | rumah akademik permanen sebuah disiplin | Ya | tepat satu domain utama |
| Strand | untai kompetensi stabil dalam satu mapel | Ya | satu mata pelajaran |
| Konsep | pengetahuan/keterampilan reusable yang dapat dilacak | Ya | satu strand utama; dapat memiliki relasi lintas-mapel |
| Unit Belajar | paket pembelajaran dan asesmen yang dapat dituntaskan | Ya | satu konsep utama; dapat melatih konsep sekunder |
| Cluster/Topik | grup tampilan atau kurasi beberapa konsep/unit | Tidak | satu mapel, satu path, atau konteks khusus |
| Learning path | urutan node untuk tujuan peserta | Ya bila ada tujuan belajar | mereferensikan unit, tidak memilikinya |

### Cluster bukan tingkat wajib

`Cluster` hanya digunakan jika membantu navigasi, misalnya `Operasi Bilangan Bulat` untuk menampilkan beberapa konsep yang berdekatan. Ia tidak boleh menjadi satu-satunya cara menyimpan prasyarat atau mastery.

```text
Matematika
└─ Strand Bilangan
   ├─ Konsep: bilangan bulat
   │  ├─ Unit: Menempatkan bilangan bulat pada garis bilangan
   │  ├─ Unit: Membandingkan bilangan bulat
   │  └─ Unit: Menentukan nilai mutlak
   ├─ Konsep: penjumlahan bilangan bulat
   │  ├─ Unit: Menjumlahkan bilangan bertanda sama
   │  └─ Unit: Menjumlahkan bilangan berbeda tanda
   └─ [Cluster tampilan opsional: Operasi Bilangan Bulat]
```

Jadi hubungan akademik tetap bisa berjalan walaupun cluster diganti, dihapus, atau ditampilkan berbeda untuk kelas tertentu.

## 3. Pemetaan domain → mata pelajaran

```text
mathematics
└─ matematika

indonesian
└─ bahasa_indonesia

english
└─ bahasa_inggris

other_languages
├─ bahasa_arab
├─ bahasa_mandarin
├─ bahasa_jepang
├─ bahasa_korea
├─ bahasa_jerman
└─ bahasa_prancis

science
├─ fisika
├─ kimia
├─ biologi
└─ bumi_antariksa

social_sciences
├─ sejarah
├─ geografi
├─ ekonomi
├─ sosiologi
├─ antropologi
├─ psikologi
└─ pendidikan_pancasila

computing
└─ informatika

arts_health_life
├─ seni_rupa
├─ seni_musik
├─ seni_tari
├─ seni_teater
├─ pjok_kesehatan
├─ prakarya_kewirausahaan
└─ keterampilan_hidup_keuangan

religious_studies
├─ islam_madrasah
├─ islam_lanjut
├─ agama_buddha
├─ agama_hindu
├─ agama_katolik
├─ agama_kristen
└─ agama_khonghucu

career_vocational
├─ kesiapan_karier
├─ akuntansi
├─ bisnis_manajemen
└─ teknik_otomotif

reasoning
├─ penalaran_logika
├─ literasi_media_informasi
└─ literasi_kuantitatif
```

Contoh yang membedakan dua tipe domain:

| Tipe domain | Contoh | Bentuk pohon |
|---|---|---|
| Satu mapel | `mathematics` | domain → matematika → strand → konsep → unit |
| Banyak mapel | `science` | domain → fisika/kimia/biologi/... → strand masing-masing → konsep → unit |

## 4. Relasi lintas-mapel tanpa merusak pohon

Satu konsep harus memiliki **satu rumah utama**, tetapi dapat membangun relasi ke konsep lain tanpa dipindahkan atau disalin.

| Relasi | Contoh | Makna sistem |
|---|---|---|
| `prerequisite_of` | pecahan → rasio | wajib dikuasai sebelum unit target |
| `reinforces` | grafik fungsi ↔ gerak lurus | memperkuat, tetapi tidak selalu wajib |
| `applies` | persamaan linear → hukum Ohm | konsep inti diterapkan pada mapel lain |
| `same_skill_as` | membaca grafik Matematika ↔ membaca grafik Geografi | kompetensi serupa, rumah konsep tetap berbeda |
| `assesses` | soal → konsep | item mengukur satu atau lebih konsep |
| `uses` | unit → interaktif/widget | unit memakai aset sumber belajar reusable |

Contoh: `Menggunakan persamaan linear` tetap tinggal di Matematika. Unit Fisika `Menganalisis hukum Ohm` memberi relasi `applies` ke konsep itu, sehingga siswa bisa mendapat remedial Matematika tanpa Fisika menggandakan persamaan linear.

## 5. Struktur learning path

Learning path bukan pohon mata pelajaran kedua. Path adalah **graf urutan** yang memuat node referensi.

```text
Learning Path
├─ metadata tujuan: target peserta, outcome, versi, pemilik, sumber acuan
├─ entry rule: placement test atau bukti prasyarat
└─ path node
   ├─ reference: unit / assessment / aktivitas-strategi-path
   ├─ role: required | optional | remedial | enrichment | assessment
   ├─ prerequisite rule
   ├─ completion rule
   ├─ depth target dan estimasi waktu
   └─ urutan/dependensi node
```

`reference` normalnya adalah unit yang sudah ada. Path hanya boleh memiliki konten sendiri untuk hal yang benar-benar khusus pada tujuan itu, misalnya strategi waktu TKA, format IELTS speaking, atau instruksi proyek karier.

### Jenis node path

| Jenis node | Referensi | Contoh |
|---|---|---|
| `unit` | satu Unit Belajar kanonik | Menjumlahkan bilangan bulat berbeda tanda |
| `assessment` | bank/blueprint khusus path | simulasi waktu TKA Matematika |
| `strategy` | aset khusus path | strategi membaca soal IELTS |
| `choice` | satu dari beberapa node | pilih bahasa asing sesuai tujuan |
| `gate` | aturan tanpa konten | placement test atau mastery minimum |

## 6. Pemetaan contoh path

### A. Path Fondasi SMP: Operasi Bilangan Bulat

```text
path: fondasi-smp-operasi-bilangan-bulat
├─ gate: cek prasyarat garis bilangan
├─ required unit: Menempatkan bilangan bulat pada garis bilangan
├─ required unit: Membandingkan bilangan bulat
├─ required unit: Menentukan nilai mutlak
├─ required unit: Menjumlahkan bilangan bertanda sama
├─ required unit: Menjumlahkan bilangan berbeda tanda
├─ conditional remedial: Memvisualkan penjumlahan pada garis bilangan
├─ required unit: Mengurangkan bilangan bulat sebagai penjumlahan lawan
└─ assessment: cek penguasaan operasi bilangan bulat
```

### B. Path Kurikulum: CP Matematika Fase D

```text
path: cp-matematika-fase-d
├─ references: unit Bilangan yang bertag phase:D
├─ references: unit Aljabar yang bertag phase:D
├─ references: unit Geometri/Pengukuran yang bertag phase:D
├─ references: unit Data/Peluang yang bertag phase:D
└─ assessment: bukti capaian per elemen CP
```

Path ini menyimpan relasi ke dokumen CP dan bukti capaian, bukan menyalin Unit Matematika Fase D.

### C. Path Ujian: TKA Matematika

```text
path: tka-matematika-[jenjang]
├─ gate: placement per konsep
├─ references: unit Matematika yang diperlukan blueprint ujian
├─ conditional remedial: unit dengan mastery rendah
├─ strategy: manajemen waktu dan pembacaan stimulus TKA
├─ assessment: latihan format TKA per komponen resmi
└─ assessment: simulasi adaptif berwaktu
```

TKA menyimpan blueprint dan strategi ujian sebagai aset sendiri; materi Bilangan, Aljabar, Geometri, dan Data tetap memakai unit kanonik.

### D. Path lintas-mapel: Sains Fase D

```text
path: sains-fase-d
├─ required unit: Merancang penyelidikan ilmiah
├─ physics unit: Memodelkan gerak dan gaya
├─ chemistry unit: Menjelaskan perubahan materi
├─ biology unit: Menganalisis ekosistem
├─ earth_space unit: Menjelaskan cuaca dan iklim
├─ reinforces: Membaca tabel/grafik dari Matematika
└─ project: Menyajikan bukti ilmiah pada isu lingkungan lokal
```

## 7. Metode pembuatan registry dan path

### Langkah 1 — Tetapkan rumah akademik

Untuk setiap materi, pilih satu mata pelajaran dan satu strand utama. Jangan mulai dari kelas, ujian, atau daftar topik lama.

### Langkah 2 — Pecah menjadi konsep

Konsep harus dapat memiliki definisi singkat, prasyarat, dan indikator penguasaan. Jika dua hal dapat dikuasai atau diremediasi secara terpisah, jadikan dua konsep.

### Langkah 3 — Bentuk unit

Satu unit mengajarkan satu kemampuan yang dapat dibuktikan. Unit diberi tujuan, prasyarat, kedalaman F0–F4, sumber, interaktif bila perlu, dan bank 50 soal.

### Langkah 4 — Tambahkan relasi

Hubungkan konsep dengan `prerequisite_of`, `applies`, dan `reinforces`. Hubungan ini menggantikan kebutuhan menaruh konsep yang sama di banyak pohon.

### Langkah 5 — Bentuk cluster hanya untuk pengalaman pengguna

Cluster digunakan pada halaman katalog atau path untuk membuat navigasi nyaman. Menghapus cluster tidak boleh merusak kode, prasyarat, mastery, atau bank soal.

### Langkah 6 — Susun learning path terakhir

Path memilih unit dan menambahkan tujuan, urutan, aturan adaptif, serta asesmen format khusus. Ia tidak boleh membuat `unit versi path` kecuali kontennya memang strategi/format khusus path.

## 8. Fungsi sistem minimum

```text
createSubject(domainId, subject)
createStrand(subjectId, strand)
createConcept(strandId, concept)
createUnit(primaryConceptId, unit)
linkConcept(fromConceptId, relationType, toConceptId)
attachAssessment(unitId, questionBankId)
createLearningPath(path)
addPathNode(pathId, referenceType, referenceId, rules)
```

Aturan validasi:

1. `createStrand` wajib menerima `subjectId`, bukan `domainId`.
2. `createConcept` memiliki satu `primaryStrandId`; relasi lintas-mapel dibuat dengan `linkConcept`, bukan membuat salinan.
3. `createUnit` memiliki satu `primaryConceptId`; konsep sekunder hanya ditag sebagai konsep yang diperkuat/diukur.
4. `attachAssessment` menghubungkan bank soal unit yang sama ke sesi latihan 10/20, 25, atau 50.
5. `addPathNode` mereferensikan aset existing; hanya `strategy` dan blueprint `assessment` yang boleh menjadi aset khusus path.

## Definition of Done

Sebuah domain siap diproduksi bila semua mata pelajaran di dalamnya telah memiliki strand sendiri, setiap unit memiliki rumah konsep yang jelas, dan path dapat ditulis sepenuhnya dengan referensi—tanpa membuat salinan materi atau bank soal.
