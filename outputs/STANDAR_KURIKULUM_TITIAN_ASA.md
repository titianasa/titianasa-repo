# Standar Kurikulum Titian Asa v0.1

Status: rancangan fondasi sebelum produksi massal atau otomasi AI.

## 1. Prinsip dasar

Titian Asa bukan kumpulan mata pelajaran dan bank soal. Titian Asa adalah perpustakaan kompetensi kanonik yang dapat dipakai ulang oleh banyak tujuan belajar.

1. **Satu konsep diajarkan sekali, digunakan berkali-kali.** Tidak boleh ada salinan materi “Pecahan” khusus SD, TKA, dan UTBK jika kompetensi dasarnya sama. Yang berbeda adalah kedalaman, konteks, urutan, dan asesmennya.
2. **Learning path hanya merujuk, tidak menggandakan.** Path menyusun unit inti menjadi pengalaman belajar untuk tujuan tertentu.
3. **Kompetensi lebih penting daripada jumlah konten.** Setiap unit harus punya hasil belajar terukur, prasyarat, dan bukti penguasaan.
4. **AI mengusulkan dan mengukur; manusia memegang akuntabilitas akademik.** Semua perubahan substansi dimulai sebagai proposal yang dapat ditinjau dan dibatalkan.
5. **Kurikulum nasional/internasional adalah kerangka acuan, bukan konten yang disalin.** Setiap pemetaan harus menyimpan sumber, versi, dan tanggal peninjauan.

## 2. Definisi objek kurikulum

| Objek | Makna | Contoh |
|---|---|---|
| Domain | rumpun pengetahuan/kemampuan tertinggi | Matematika |
| Mata pelajaran | wadah kurikulum dan navigasi pengguna | Matematika |
| Strand | untai kompetensi yang stabil | Bilangan; Aljabar; Geometri |
| Konsep | pengetahuan/keterampilan atomik yang reusable | operasi penjumlahan bilangan bulat |
| Unit Belajar | paket terkecil yang dapat dituntaskan | Menjumlahkan bilangan bulat berbeda tanda |
| Sumber Belajar | cara mempelajari unit | artikel, simulasi, audio, contoh |
| Aktivitas | interaksi di dalam sumber belajar | manipulasi garis bilangan, refleksi |
| Item Asesmen | alat mengukur satu/lebih konsep | soal pilihan ganda, isian, rekaman bicara |
| Learning Path | urutan dan aturan penggunaan unit | TKA Matematika SMA; IELTS 6.5 |

Aturan penting: **bab bukan objek kanonik.** “Bab” hanya nama tampilan untuk satu atau beberapa Unit Belajar. Unit dan konsep adalah aset yang dipakai ulang oleh sistem.

## 3. Hirarki materi inti

Struktur wajib:

```text
Domain → Mata pelajaran → Strand → Konsep → Unit Belajar
                                      ├─ sumber belajar (teks/media/interaktif)
                                      ├─ contoh dan miskonsepsi umum
                                      └─ asesmen + bukti penguasaan
```

Satu Unit Belajar wajib mengandung:

- tujuan belajar yang dapat diamati;
- prasyarat konsep;
- tingkat kedalaman: pengenalan, penerapan, penalaran, atau penguasaan;
- penjelasan utama, contoh bertahap, dan miskonsepsi umum;
- latihan diagnostik, latihan terarah, dan cek penguasaan;
- estimasi waktu serta versi/sumber akademik.

Jumlah aktivitas tidak boleh dipatok seragam. “20 aktivitas” hanya boleh muncul jika desain pembelajarannya memang membutuhkannya, bukan sebagai angka template.

## 4. Domain materi inti v1

Fokus awal harus pada domain yang paling reusable dan berpenduduk pengguna besar.

| Prioritas | Domain inti | Strand awal |
|---|---|---|
| P0 | Matematika | bilangan, aljabar, geometri-pengukuran, data-peluang, kalkulus, penalaran |
| P0 | Bahasa Indonesia | menyimak, membaca, berbicara, menulis, kebahasaan, apresiasi |
| P0 | Bahasa Inggris | receptive skills, productive skills, grammar, vocabulary, pronunciation |
| P0 | Sains | keterampilan ilmiah, fisika, kimia, biologi, bumi-antariksa |
| P1 | Literasi digital & Informatika | sistem komputer, data, pemrograman, jaringan, keamanan digital, AI literacy |
| P1 | Ilmu sosial & kewargaan | sejarah, geografi, ekonomi, sosiologi, pendidikan Pancasila |
| P1 | Kesehatan, seni, dan keterampilan hidup | PJOK, kesehatan mental, literasi finansial, seni, prakarya |
| P2 | Keagamaan dan bahasa lain | dibangun dengan ahli domain serta struktur setara |
| P2 | Kejuruan | berbasis kompetensi/jabatan, bukan satu mapel SMK generik |

Urutan di atas adalah prioritas produksi, bukan penilaian nilai suatu disiplin. Ia menjaga kualitas ketika tim dan data masih terbatas.

## 5. Standar topik dan unit

### Topik

Topik harus merupakan kelompok konsep yang koheren, bukan label kelas atau daftar ujian. Nama topik memakai kata benda/kemampuan yang spesifik.

- Baik: `Operasi Bilangan Bulat`, `Membaca Teks Informasi`, `Kinematika Satu Dimensi`.
- Tidak baik: `Matematika Kelas 7`, `Latihan TKA`, `Materi Lanjutan`.

### Unit Belajar

Nama unit menggunakan kata kerja + objek kompetensi.

- Baik: `Menentukan hasil penjumlahan bilangan bulat berbeda tanda`.
- Tidak baik: `Penjumlahan Bilangan Bulat`.

Setiap unit memiliki struktur minimum:

1. pemantik atau diagnosis singkat;
2. penjelasan konsep;
3. contoh dengan alasan langkah;
4. latihan bertahap;
5. checkpoint penguasaan;
6. tindak lanjut: lanjut, pengayaan, atau perbaikan.

## 6. Learning path

Learning path tidak membuat materi baru kecuali ada gap nyata. Ia terdiri dari node yang **mereferensikan** Unit Belajar, dengan metadata:

- tujuan akhir dan profil peserta;
- prasyarat masuk/placement test;
- node wajib, pilihan, remedial, dan pengayaan;
- aturan kelulusan per node;
- dependensi antarnode;
- estimasi waktu dan target tanggal bila relevan;
- versi path dan rujukan standar eksternal.

### Jenis path resmi

| Jenis | Contoh | Sifat |
|---|---|---|
| Fondasi | Matematika dari dasar sampai lanjut | panjang, lintas jenjang, reusable |
| Kurikulum | CP Matematika Fase D | dipetakan ke CP/fase, bukan digandakan per kelas |
| Ujian | TKA Matematika SMA; UTBK Penalaran Matematika | menggabungkan konsep inti + strategi format tes |
| Sertifikasi bahasa | IELTS 6.5; CEFR B1 | berbasis kemampuan dan bukti performa |
| Karier | Dasar Akuntansi untuk staf administrasi | berbasis kompetensi kerja dan proyek |
| Adaptif | Pemulihan Aljabar Dasar | dibuat dari gap mastery peserta |

Path ujian tidak boleh disebut sebagai kurikulum dasar. Konten strategi ujian dipisahkan dari konsep akademik agar tetap tidak mengontaminasi perpustakaan inti.

## 7. Label dan kode

Semua label memakai namespace. Satu label satu arti.

```text
domain:mathematics
subject:matematika
strand:bilangan
concept:integer-addition-opposite-sign
framework:kurikulum-merdeka
phase:D
grade:SMP-7
exam:tka-sma
exam-component:matematika-wajib
cefr:B1
audience:student
content-type:interactive
language:id
status:published
```

Larangan:

- jangan memakai `custom` sebagai kode mapel produksi;
- jangan memakai label kelas SMA untuk konten SMK;
- jangan membuat satu label mengandung dua konsep seperti `jenjang:SMA-10, kurikulum:merdeka-smk`;
- jangan mencampur taksonomi ujian, jenjang, dan kompetensi dalam satu label teks.

## 8. Bentuk konten dan interaktif yang scalable

Teks tetap penting sebagai penjelasan, rujukan, aksesibilitas, dan fallback. Namun, untuk konsep yang dapat dimanipulasi atau didemonstrasikan, **web interaktif adalah format utama yang reusable**: dapat dipakai peserta belajar mandiri, guru melalui layar sentuh/proyektor, dan kelas bersama.

Titian Asa boleh—dan memang perlu—mendukung dua jalur interaktif berikut. Keduanya tidak saling menggantikan.

| Jalur | Dipakai untuk | Bentuk produksi |
|---|---|---|
| Widget reusable | pola interaksi yang berulang | satu engine + konfigurasi tervalidasi |
| CodeWeb/website khusus | satu pengalaman belajar kaya yang tidak cocok dipaksa ke widget | HTML/CSS/JS mandiri yang dipaketkan dan diverifikasi |

Widget reusable adalah alat utama efisiensi. CodeWeb khusus tetap bernilai untuk materi seperti pelafalan alfabet, simulasi, permainan belajar, atau demonstrasi kelas yang punya alur pedagogis khas. Tujuannya bukan melarang web khusus, tetapi mencegahnya menjadi aset lepas yang tidak dapat diukur, dicari, diperbarui, atau dipakai ulang.

```text
Konsep kanonik
  └─ Lesson specification (tujuan, contoh, aturan pedagogis)
       ├─ artikel terstruktur
       ├─ konfigurasi interaktif (JSON tervalidasi)
       ├─ template latihan/variasi soal
       └─ mode guru dan mode peserta

Runtime interaktif bersama
  ├─ garis bilangan
  ├─ pecahan/manipulatif virtual
  ├─ grafik fungsi
  ├─ simulasi sains
  ├─ kartu kosakata/pasangan
  ├─ pronunciation/audio loop
  ├─ Hanzi/nada Mandarin
  └─ visualisasi algoritma
```

Setiap CodeWeb atau widget wajib memiliki manifest:

```text
id stabil · versi · konsep yang dilatih · tujuan · mode (peserta/guru)
input/aksi yang didukung · event standar · kondisi selesai · fallback aksesibel
```

Event minimum: `opened`, `section_viewed`, `interaction_completed`, `checkpoint_answered`, `completed`, dan `error`. Runtime Titian menyimpan event tersebut; web tidak menyimpan progres sebagai sumber kebenaran hanya di browser. Sematan memakai sandbox/iframe yang aman, komunikasi `postMessage` dengan allowlist origin, dan fallback teks/audio bila fitur browser tidak tersedia.

Contoh: Unit `Menjumlahkan Bilangan Bulat Berbeda Tanda` tidak memerlukan aplikasi baru. Ia memakai engine `number-line` dengan konfigurasi seperti rentang angka, contoh awal, soal parameter, petunjuk, dan konsep yang dilacak. Perbaikan engine akan otomatis meningkatkan semua unit yang menggunakannya.

| Bentuk | Dipakai ketika |
|---|---|
| Artikel terstruktur | penjelasan, contoh, rujukan, aksesibilitas, dan fallback |
| Checkpoint | perlu menguji pemahaman cepat sebelum lanjut |
| Latihan adaptif | perlu bukti mastery dan diagnosis kesalahan |
| Web interaktif | manipulasi/visualisasi memberi nilai belajar nyata atau menjadi media ajar guru |
| Audio/rekaman | kompetensi utamanya menyimak atau berbicara |
| Proyek/portofolio | hasil belajar tidak dapat dibuktikan lewat soal objektif |

Web interaktif diprioritaskan untuk garis bilangan, pecahan, geometri, grafik fungsi, simulasi sains, pronunciation, nada Mandarin, dan visualisasi algoritma. Ia harus memiliki tujuan konsep, event belajar, serta fallback teks yang aksesibel. Mode guru minimal memiliki layar bersih, kontrol langkah, reset, proyeksi layar penuh, dan kemampuan memunculkan/tutup petunjuk; mode peserta menyimpan progres serta memberi umpan balik personal.

## 9. Standar asesmen

Setiap soal harus punya identitas tetap, konsep yang ditag, tingkat kesulitan, target kognitif, jawaban dan alasan jawaban, serta versi.

Sistem kuis Titian yang mendukung banyak subtype adalah kekuatan inti. Subtype dipilih berdasarkan bukti yang hendak dikumpulkan—bukan hanya agar latihan tampak bervariasi. Satu kuis dapat memadukan penilaian otomatis, rubrik AI, penilaian guru, dan refleksi mandiri; blueprint harus menyatakan proporsi dan alasannya.

Tingkat kesulitan dan taksonomi adalah dua sumbu berbeda; keduanya tidak boleh digabung menjadi satu label.

| Dimensi | Nilai awal | Nilai setelah data cukup |
|---|---|---|
| Kesulitan | mudah, menengah, sulit berdasarkan kalibrasi ahli | indeks kesulitan/tingkat keberhasilan aktual per versi soal |
| Proses kognitif | mengingat, memahami, menerapkan, menganalisis, mengevaluasi, mencipta | tetap dipertahankan sebagai tujuan desain |
| Dimensi pengetahuan | faktual, konseptual, prosedural, metakognitif | tetap dipertahankan sebagai tujuan desain |
| Format respons | pilihan ganda, isian, pencocokan, esai, lisan, manipulasi interaktif | statistik kualitas per format |

Soal HOTS tidak otomatis sulit, dan soal mudah tidak otomatis hanya menguji ingatan. Keduanya perlu ditetapkan secara terpisah agar AI dapat mendeteksi kekosongan blueprint dengan benar.

Komposisi asesmen minimal per unit:

- 1 diagnosis prasyarat bila konsep berisiko tinggi;
- 2–5 latihan terarah dengan umpan balik;
- 1 checkpoint mastery;
- pengayaan atau remedial sesuai pola salah.

Tes format tertentu—IELTS, TKA, UTBK, CPNS, atau BUMN—memiliki bank dan blueprint terpisah, karena bentuk respons, waktu, dan rubriknya berbeda. Jangan menjadikan semua latihan sebagai pilihan ganda.

## 10. Standar mutu dan pemeliharaan AI

AI boleh memberi sinyal bila terjadi:

- banyak siswa salah pada konsep/pengecoh yang sama;
- waktu belajar jauh di atas atau di bawah ekspektasi;
- siswa berhenti berulang pada unit tertentu;
- ada kontradiksi terhadap sumber acuan yang lebih baru;
- ada laporan guru/siswa yang tervalidasi.

AI tidak boleh menyimpulkan “materi buruk” hanya dari skor rendah; ia harus mempertimbangkan prasyarat, karakter peserta, desain asesmen, dan versi konten.

Setiap perubahan substansi wajib melewati: `temuan → diagnosis → proposal → QA independen → persetujuan → publikasi bertahap → evaluasi → rollback bila perlu`.

## 11. Perbaikan langsung terhadap katalog lama

1. Ubah judul dokumen dari “katalog lengkap” menjadi “inventaris awal”; data totalnya belum konsisten.
2. Pisahkan 48 rumpun saat ini menjadi: materi inti, domain aplikasi, persiapan ujian, dan materi khusus. CPNS/BUMN bukan rumpun materi inti.
3. Hapus angka seragam “20 aktivitas” sebagai target desain.
4. Ubah mapel `custom` menjadi kode domain permanen sebelum diproduksi.
5. Pisahkan Bahasa Inggris fondasi/CEFR dari jalur Cambridge dan persiapan ujian bahasa.
6. TKA harus dipetakan per jenjang dan mata uji resmi; AKM tidak digabung sebagai sinonim TKA.
7. Gunakan fase CP sebagai kerangka Kurikulum Merdeka: A (kelas 1–2), B (3–4), C (5–6), D (7–9), E (10), F (11–12). Kelas tetap boleh menjadi tampilan/filter.
8. Bagi “Seni Budaya” ke seni rupa, musik, tari, dan teater jika materi akan benar-benar dibuat.
9. SMK dibangun per program keahlian/kompetensi kerja; Akuntansi dan Otomotif hanyalah dua jalur awal.
10. Koreksi nomenklatur menjadi `Al-Qur'an Hadis`; gunakan nama mata pelajaran resmi sebagai nama tampilan bila relevan.

## 12. Definition of Done sebelum produksi massal

Sebuah domain boleh diproduksi massal hanya jika:

- peta domain → strand → konsep telah disetujui ahli mapel;
- setiap konsep memiliki kode stabil, prasyarat, dan definisi singkat;
- unit contoh telah lulus review pedagogis, fakta, bahasa, dan aksesibilitas;
- blueprint asesmen tersedia untuk tiap tipe unit;
- path hanya memakai reference ke unit, tidak membuat salinan;
- sumber acuan, pemilik akademik, versi, dan tanggal tinjau tersimpan;
- data event dan versi konten siap dipakai untuk evaluasi AI.

## 13. Urutan kerja yang disarankan

1. Sahkan standar ini dan tetapkan peran pemilik akademik.
2. Audit serta normalisasi 48 rumpun menjadi peta domain/strand/konsep.
3. Pilih satu pilot: **Matematika → Bilangan → Bilangan Bulat**.
4. Bangun 10–15 unit inti pilot beserta teks, checkpoint, soal, dan 1–2 interaktif.
5. Turunkan tiga path dari unit yang sama: fondasi SMP, TKA, dan remedial adaptif.
6. Uji dengan pengguna nyata, lakukan review ahli, lalu tetapkan template produksi untuk domain berikutnya.

Langkah 3–5 adalah pembuktian bahwa arsitektur anti-duplikasi benar-benar bekerja sebelum katalog diperluas.

## Lampiran A — Strategi biaya produksi dan skala

Biaya token adalah biaya **produksi/peningkatan konten**, bukan biaya yang seharusnya dibayar ulang setiap peserta membuka materi. Semua hasil yang sudah lolos QA harus disimpan sebagai aset ber-versi dan dilayani secara statis dari CDN/cache; runtime belajar tidak memanggil model AI kecuali fitur tutor memang dipakai.

### Pola produksi hemat

1. Tulis satu `lesson specification` ringkas dan terstruktur lebih dulu, bukan meminta AI langsung menulis artikel panjang, soal, dan aplikasi yang saling tidak konsisten.
2. Gunakan specification yang sama untuk merender artikel, mengisi konfigurasi engine interaktif, dan membangun template variasi soal.
3. Bangun library engine interaktif secara bertahap. Engine yang baik dipakai oleh puluhan/ratusan unit; konten baru cukup membuat konfigurasi yang kecil dan tervalidasi.
4. Gunakan keluarga soal berparameter untuk latihan rutin. AI dipakai untuk membuat blueprint, contoh, pengecoh, dan QA—bukan membuat semua soal baru setiap kali siswa berlatih.
5. Jalankan AI mahal hanya pada pekerjaan bernilai tinggi: desain awal, review fakta, review pedagogis, dan diagnosis kualitas. Outline, normalisasi label, dan variasi terstruktur memakai model yang lebih hemat.
6. Cache berdasarkan `content_hash`; jangan menghasilkan ulang konten yang spesifikasinya tidak berubah.
7. Batasi output dengan skema JSON dan anggaran token per tahap. Output yang gagal validasi tidak boleh diteruskan ke tahap berikutnya.
8. Versi dan eksperimen dipakai untuk memperbaiki satu aset bersama, bukan membuat cabang permanen per pengguna.

Untuk CodeWeb khusus, gunakan paket starter yang sudah memuat shell responsif, navigasi bagian, progres, checkpoint, event Titian, mode guru, audio fallback, dan pemeriksaan aksesibilitas. AI hanya mengisi `lesson specification` dan aset/konfigurasi khususnya; ia tidak perlu berulang kali menulis boilerplate HTML/CSS/JS yang sama. Ini menjaga keunggulan biaya web interaktif tanpa mewariskan ratusan kode mandiri yang sukar dirawat.

### Pipeline produksi yang disarankan

```text
Peta konsep yang disetujui ahli
  → lesson specification terstruktur
  → artikel + konfigurasi interaktif + template soal
  → validasi otomatis (skema, tag, duplikasi, jawaban)
  → QA akademik/pedagogis
  → publish versi 1
  → data penggunaan dan hasil belajar
  → proposal perbaikan AI
```

Ukuran biaya harus dilacak per tahap: token input/output, model, keberhasilan validasi, lama QA manusia, dan jumlah unit yang kembali memakai engine yang sama. Dengan begitu keputusan “artikel vs interaktif” dibuat dari biaya total dan dampak belajar, bukan dari token generasi awal saja.
