# Standar Blueprint Modul Titian Asa v1

Status: lapisan produksi yang melengkapi pohon kurikulum kanonik. Berlaku untuk Matematika, Bahasa Inggris, Bahasa Indonesia, Sains, dan domain berikutnya.

## 1. Dua artefak yang wajib terpisah tetapi terhubung

```text
Pohon kurikulum
Domain → Mata pelajaran → Strand → Konsep → Modul kanonik

Blueprint modul
Modul kanonik → Bagian → konten/media → grup latihan → item → checkpoint → aturan kelulusan
```

Pohon menjawab **materi apa, urutan prasyaratnya apa, dan modul mana yang reusable**. Blueprint menjawab **bagaimana satu modul dibangun dalam mesin Modul**. Satu leaf/modul pada pohon harus memiliki tepat satu blueprint aktif per versi; path sekolah atau ujian hanya memilih konfigurasi penyajian dan item, tanpa membuat modul baru.

## 2. Struktur data wajib

```text
ModuleBlueprint
├─ identitas
│  ├─ module_id
│  ├─ nama modul
│  ├─ domain / mapel / strand / konsep
│  └─ versi dan status review
├─ rancangan belajar
│  ├─ tujuan pembelajaran terukur
│  ├─ prasyarat
│  ├─ kedalaman target
│  ├─ durasi dan profil peserta
│  └─ miskonsepsi/risiko utama
├─ bagian[]
│  ├─ tujuan bagian
│  ├─ durasi
│  ├─ konten dan media
│  ├─ aktivitas
│  ├─ grup latihan (query ke bank soal modul)
│  └─ checkpoint bagian (bila perlu)
├─ bank_soal_kanonik[50]
│  ├─ latihan per bagian
│  ├─ latihan mandiri/transfer
│  ├─ checkpoint akhir
│  ├─ remedial
│  └─ pengayaan
├─ checkpoint_akhir
│  ├─ blueprint item
│  ├─ ambang kelulusan
│  └─ bukti performa
└─ tindak_lanjut
   ├─ remedial
   ├─ lanjut
   └─ pengayaan
```

## 3. Pemetaan ke mesin Modul yang ada

| Blueprint | Mesin Modul |
|---|---|
| `nama modul`, durasi, peserta, bahasa | header modul dan generator otomatis |
| `bagian[]` | tombol **Tambah Bagian** dan struktur di panel kiri |
| konten | paragraf, definisi, contoh, langkah, tabel, catatan, kesalahan umum, perbandingan, rumus, dan blok lain |
| media | audio, video, gambar, sematan web, berkas, atau tautan |
| grup latihan | grup soal di bawah bagian; menampilkan pilihan dari bank soal modul, bukan membuat bank baru |
| item | satu kartu soal kanonik dengan tipe, kunci, pembahasan, kesulitan, Bloom, dan tag |
| checkpoint | grup soal penutup yang menentukan status penguasaan |
| remedial/pengayaan | tautan ke modul prasyarat/lanjutan atau variasi latihan yang dipilih sistem |

## 4. Template blueprint menurut jenis modul

Template dipilih berdasarkan tujuan modul; ia bukan batas jumlah bagian. Konten dan soal harus mengikuti tujuan, bukan memenuhi kuota.

| Kode | Cocok untuk | Bagian minimum |
|---|---|---|
| `CONCEPT` | menjelaskan, mengenali, membedakan | fenomena/pemantik → konsep inti → contoh-kontras → latihan → checkpoint |
| `PROCEDURE` | menghitung, menentukan, menyelesaikan | diagnosis prasyarat → model/langkah → contoh bertahap → latihan terarah → transfer/checkpoint |
| `INTERPRET` | membaca, menafsirkan, menganalisis teks/data/grafik | orientasi sumber → strategi → contoh anotasi → latihan → evaluasi/checkpoint |
| `INVESTIGATE` | mengamati, merancang, menyelidiki | pertanyaan → rancangan/keamanan → data/bukti → kesimpulan → refleksi/checkpoint |
| `COMMUNICATE` | menulis, berbicara, mempresentasikan | model → perencanaan → produksi terbimbing → revisi/umpan balik → performa/rubrik |
| `PRACTICE` | pelafalan, keterampilan motorik, penggunaan alat | model/posisi → latihan terisolasi → latihan terarah → penggunaan bermakna → rekam/umpan balik |
| `EVALUATE` | mengevaluasi klaim, sumber, risiko, etika | kriteria → analisis contoh → perbandingan bukti → keputusan beralasan → checkpoint |

## 5. Bank soal kanonik: tepat 50 item per modul

Setiap modul memiliki **satu bank kanonik berisi tepat 50 item**. Bank tersebut adalah aset modul yang dapat dipakai ulang oleh sesi latihan, checkpoint, remedial, pengayaan, dan learning path. Satu item tidak disalin ketika muncul pada Bagian modul, kuis mandiri, atau path; sistem hanya membuat referensi/penyajian item yang sama.

```text
Modul
├─ Bagian 1 → grup latihan → menarik item bank yang ditag bagian_1
├─ Bagian 2 → grup latihan → menarik item bank yang ditag bagian_2
├─ Bagian 3 → grup latihan → menarik item bank yang ditag bagian_3
├─ Checkpoint akhir → menarik blueprint checkpoint dari bank yang sama
└─ Sesi 10/20, 25, atau 50 soal → menarik komposisi adaptif dari bank yang sama
```

Komposisi awal yang wajib dipenuhi oleh 50 item:

| Fungsi bank | Jumlah | Aturan |
|---|---:|---|
| Diagnostik prasyarat | 4 | muncul sebelum/awal modul; fokus C1–C2 dan miskonsepsi prasyarat |
| Latihan per Bagian | 22 | setiap Bagian berisi minimal 4 item; distribusi mengikuti bobot tujuan Bagian |
| Latihan mandiri dan transfer | 8 | menggabungkan tujuan dari dua/lebih Bagian atau konteks baru |
| Checkpoint akhir | 10 | mencakup seluruh tujuan inti dan tidak memakai item diagnosis sebagai satu-satunya bukti |
| Remedial | 4 | bertag miskonsepsi spesifik dan memberi umpan balik lebih terarah |
| Pengayaan | 2 | tugas bernalar, mengevaluasi, atau mencipta sesuai sifat kompetensi |
| **Total** | **50** | satu bank aktif per versi modul |

Jika modul memiliki lebih dari lima Bagian, kuota 22 latihan per Bagian disusun proporsional; jika hanya tiga Bagian, setiap Bagian tetap harus mendapat minimal empat item dan sisa dialokasikan ke tujuan yang paling berat. `Checkpoint bagian` dapat memakai item latihan yang bertag `checkpoint_bagian`; ia tidak boleh membuat salinan item ke bank lain.

### Kesulitan dan Bloom

Kesulitan dan Bloom adalah dua sumbu berbeda. Komposisi awal bank 50 harus memiliki cakupan berikut, kecuali ada alasan akademik yang disetujui penelaah untuk kompetensi yang memang tidak dapat dibuktikan dengan format tertentu.

| Kesulitan | Jumlah | Fokus umum |
|---|---:|---|
| Mudah | 15 | pengenalan, pemahaman, serta prosedur satu langkah |
| Menengah | 25 | penerapan, koneksi representasi, dan analisis terbimbing |
| Sulit | 10 | transfer, analisis multi-langkah, evaluasi, atau kreasi/performa |

| Bloom | Jumlah minimum | Bukti yang diharapkan |
|---|---:|---|
| C1 — Mengingat | 5 | mengenali istilah, fakta, simbol, atau langkah dasar |
| C2 — Memahami | 8 | menjelaskan, mengelompokkan, atau menafsirkan sederhana |
| C3 — Menerapkan | 14 | menggunakan prosedur/strategi pada situasi lazim |
| C4 — Menganalisis | 12 | membedakan pola, kesalahan, struktur, atau hubungan |
| C5 — Mengevaluasi | 6 | menilai bukti, strategi, kualitas, atau keputusan dengan kriteria |
| C6 — Mencipta | 2 | menyusun solusi, penjelasan, produk, atau performa baru |
| Cadangan terkalibrasi | 3 | dialokasikan ke Bloom yang paling relevan dengan tujuan modul |

Setiap bank juga menandai dimensi pengetahuan: `faktual`, `konseptual`, `prosedural`, atau `metakognitif`. C6 tidak berarti selalu esai panjang: untuk pelafalan dapat berupa rekaman produksi; untuk matematika berupa penyusunan model/strategi; untuk sains berupa rancangan penyelidikan; untuk bahasa berupa teks atau presentasi.

### Sesi yang ditarik dari bank

| Sesi | Jumlah item | Fungsi |
|---|---:|---|
| Latihan cepat | 10 atau 20 | diagnosis, penguatan Bagian, atau remedial; bukan pengganti cakupan penuh |
| Latihan standar | 25 | campuran terkalibrasi lintas Bagian dan tingkat kesulitan |
| Penguasaan lengkap | 50 | seluruh bank aktif atau blueprint ekuivalen yang tidak mengulang item yang sama |
| Checkpoint modul | 4–6 ditampilkan dari 10 item checkpoint | bukti lanjut; pemilihan dapat adaptif tetapi harus mencakup tujuan inti |

## 6. Kontrak item asesmen

Setiap item soal, termasuk item yang dibuat melalui AI, wajib menyimpan:

```text
item_id, module_id, bagian_id, tujuan_id, fungsi,
tipe_soal, kesulitan, bloom, dimensi_pengetahuan,
kunci/rubrik, pembahasan, miskonsepsi_target, versi, status_review
```

`fungsi` hanya salah satu dari: `diagnostik`, `latihan_terarah`, `latihan_mandiri`, `checkpoint_bagian`, `checkpoint_akhir`, `remedial`, atau `pengayaan`.

Pemilihan tipe soal mengikuti bukti yang diinginkan:

| Bukti | Tipe mesin yang diprioritaskan |
|---|---|
| mengenali konsep atau miskonsepsi | pilihan ganda, benar/salah, pilihan ganda kompleks |
| menghitung atau melengkapi relasi | isian, gap fill, table completion |
| mengurutkan proses | susun, flow chart |
| memberi label pada representasi | diagram labeling, matching |
| menghasilkan penjelasan atau karya | produksi, jawaban singkat, rekaman/performa bila tersedia |
| memahami teks/sumber | heading matching, true/false/not given, pilihan, cloze |

## 7. Contoh blueprint ringkas

```text
module_id: physics.electricity_magnetism.current_voltage_resistance_ohm.v1
template: PROCEDURE
tujuan:
  - Menjelaskan beda arus, tegangan, dan hambatan.
  - Menggunakan V = I × R untuk menentukan besaran yang tidak diketahui.
  - Menafsirkan hubungan V dan I dari tabel atau grafik.
prasyarat:
  - Besaran dan satuan dasar.
  - Muatan listrik dasar.
bagian:
  1. Arus, tegangan, dan hambatan — definisi, ilustrasi, latihan membedakan.
  2. Hukum Ohm — rumus, contoh bertahap, isian numerik.
  3. Data rangkaian — tabel/grafik, aktivitas simulasi, table completion.
  4. Checkpoint — 4–6 item yang ditarik dari 10 item checkpoint bank.
bank_soal:
  - 50 item: 4 diagnostik, 22 latihan per Bagian, 8 transfer,
    10 checkpoint, 4 remedial, 2 pengayaan.
  - Kesulitan: 15 mudah, 25 menengah, 10 sulit.
  - Bloom: C1–C6 seluruhnya terwakili sesuai kontrak bank.
kelulusan:
  - ≥80% checkpoint dan benar pada minimal satu item transfer.
tindak_lanjut:
  - remedial: modul besaran/satuan atau latihan Hukum Ohm visual.
  - lanjut: modul rangkaian seri, paralel, daya, dan energi listrik.
```

## 8. Aturan revisi pohon yang sudah ada

Setiap baris leaf pada pohon—misalnya `Menentukan ...`, `Menganalisis ...`, atau `Menulis ...`—harus diperlakukan sebagai **modul kanonik** dan diberi `module_id`. Pemetaan berikut wajib tersedia di registry:

```text
leaf pohon → module_id → blueprint_id → bagian[] → item blueprint[]
```

Tree tidak perlu memuat seluruh naskah dan soal; itu akan membuat navigasi dan perubahan versi sulit dikelola. Pohon cukup menunjukkan leaf/modul serta ID blueprint-nya. Detail Bagian dan Item disimpan dalam registry blueprint per mata pelajaran, agar mesin Modul dapat membuat, meninjau, menerbitkan, dan memperbaruinya tanpa mengubah pohon kurikulum.
