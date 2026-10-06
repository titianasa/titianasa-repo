# Peta Matematika Kanonik & Golden Module v1

Status: standar produksi awal untuk Titian Asa. Dibuat dari audit struktur Matematika yang ada; belum merupakan silabus per kelas yang final.

## 1. Koreksi terhadap struktur Matematika lama

Struktur lama sudah luas, tetapi mencampur empat hal: konsep dasar, urutan jenjang, strategi ujian, dan matematika perguruan tinggi. “Tahap 1–5” terlalu besar untuk dipakai AI menentukan prasyarat, dan sejumlah konsep muncul dalam jalur yang berbeda tanpa identitas bersama.

Struktur baru memakai strand yang stabil. Fase/kelas, TKA/UTBK, Cambridge, dan kuliah hanya menjadi **pemetaan** terhadap konsep yang sama.

```text
Matematika
├─ Bilangan
├─ Aljabar & Fungsi
├─ Geometri & Pengukuran
├─ Data, Peluang & Statistika
├─ Kalkulus & Analisis
├─ Diskrit, Logika & Teori Bilangan
└─ Pemodelan & Matematika Terapan
```

`Penalaran kuantitatif` bukan strand yang mengulang seluruh Matematika. Ia adalah lapisan penggunaan lintas-strand: membaca informasi kuantitatif, memilih model, memperkirakan, dan menjelaskan alasan.

## 2. Registry strand dan konsep tingkat pertama

| Kode strand | Nama | Kelompok konsep utama |
|---|---|---|
| `number` | Bilangan | cacah, bulat, rasional, real, kompleks; nilai tempat; operasi; rasio; persen; eksponen; akar |
| `algebra_functions` | Aljabar & Fungsi | pola, ekspresi, persamaan/pertidaksamaan, sistem, relasi, fungsi, barisan-deret, matriks, vektor |
| `geometry_measurement` | Geometri & Pengukuran | objek/bangun, ruang, relasi spasial, transformasi, koordinat, ukuran, trigonometri, geometri analitik |
| `data_probability_statistics` | Data, Peluang & Statistika | representasi data, ukuran ringkasan, peluang, pencacahan, variabel acak, inferensi |
| `calculus_analysis` | Kalkulus & Analisis | limit, kontinuitas, turunan, integral, multivariabel, analisis real, persamaan diferensial |
| `discrete_logic_number_theory` | Diskrit, Logika & Teori Bilangan | himpunan, logika, pembuktian, kombinatorika, graf, rekursi, keterbagian, modularitas |
| `modeling_applied` | Pemodelan & Terapan | pemodelan, optimisasi, numerik, keuangan, riset operasi, mekanika matematis |

## 3. Tingkatan kedalaman yang independen dari kelas

| Kode | Kedalaman | Bukti penguasaan |
|---|---|---|
| `F0` | fondasi konkret | memodelkan dengan benda, gambar, atau interaksi |
| `F1` | prosedur dasar | menjalankan prosedur dan memeriksa hasil |
| `F2` | koneksi konsep | memilih representasi/operasi serta menjelaskan hubungan |
| `F3` | penalaran & pemecahan masalah | memodelkan konteks baru, memberi alasan, mengevaluasi strategi |
| `F4` | formal & lanjut | membuktikan, menggeneralisasi, atau memakai definisi formal |

Fase Kurikulum Merdeka dan kelas hanya menargetkan kombinasi konsep + kedalaman. Contoh: konsep bilangan bulat ada di F1 ketika prosedur dituju dan di F3 ketika dipakai dalam masalah multi-langkah.

## 4. Peta fase sekolah dan jalur lanjut

| Pemetaan | Fokus dominan |
|---|---|
| Fase A (kelas 1–2) | bilangan konkret, operasi dasar, pengukuran informal, bentuk, data sederhana |
| Fase B (kelas 3–4) | nilai tempat, pecahan awal, pengukuran baku, bangun, data tabel/diagram |
| Fase C (kelas 5–6) | bilangan rasional, rasio/persen awal, geometri-pengukuran, data dan peluang awal |
| Fase D (kelas 7–9) | bilangan real, aljabar dasar, persamaan, geometri, statistika-peluang, penalaran kontekstual |
| Fase E (kelas 10) | fungsi, trigonometri, statistika, peluang, pemodelan menurut pilihan kurikulum |
| Fase F (kelas 11–12) | fungsi lanjut, kalkulus/vektor/matriks/statistika sesuai mata pelajaran dan peminatan |
| Perguruan tinggi | fondasi formal dan spesialisasi: kalkulus lanjut, linear algebra, diskrit, analisis, terapan |

Peta ini harus disandingkan dengan dokumen Capaian Pembelajaran versi yang berlaku saat rincian unit tiap fase disahkan. CP menjadi acuan pemetaan, bukan alasan untuk menggandakan unit yang sama per kelas.

## 5. Normalisasi topik katalog lama

| Topik lama | Lokasi kanonik baru | Catatan |
|---|---|---|
| Bilangan & Operasi Dasar | `number` | pecah menjadi konsep nilai tempat, operasi, bilangan bulat, faktor/kelipatan |
| Pecahan, Desimal & Persen | `number` | rasio/perbandingan tersambung ke pemodelan dan aljabar |
| Pengukuran | `geometry_measurement` | unit dan konversi disusun sebagai konsep pengukuran, bukan daftar satuan |
| Geometri Dasar/Bidang/Ruang | `geometry_measurement` | konsep bangun, sifat, transformasi, dan ukuran dipisah |
| Pengenalan Data/Statistika/Peluang | `data_probability_statistics` | bukan tiga jalur terpisah; berkembang dari representasi ke inferensi |
| Aljabar Dasar/Persamaan/Program Linear | `algebra_functions` + `modeling_applied` | program linear adalah aplikasi pemodelan, bukan cabang persamaan saja |
| Aritmetika Sosial | `number` + `modeling_applied` | persentase, rasio, bunga, diskon adalah konteks; jangan salin operasi dasar |
| Numerasi & Penalaran Kuantitatif | lintas semua strand | kumpulan task kontekstual; bukan materi konsep kedua |
| Eksponen & Logaritma | `number` + `algebra_functions` | aturan eksponen adalah Bilangan, fungsi/persamaan eksponen adalah Aljabar |
| Fungsi, Kuadrat, Barisan & Deret | `algebra_functions` | urutkan lewat prasyarat fungsi dan pola |
| Trigonometri, Transformasi, Geometri Analitik, Dimensi Tiga, Irisan Kerucut | `geometry_measurement` | keterkaitan koordinat/fungsi ditandai sebagai relasi lintas-strand |
| Matriks & Vektor | `algebra_functions` | aplikasi geometri/fisika melalui relasi, bukan salinan materi |
| Limit, Turunan, Integral | `calculus_analysis` | urutan wajib: fungsi → limit → turunan → integral |
| Logika, Diskrit, Teori Bilangan | `discrete_logic_number_theory` | pembuktian menjadi skill lintas konsep |
| Kalkulus Lanjut, PD, Aljabar Linear, Analisis Real, Inferensial | spesialisasi perguruan tinggi | diproduksi setelah kurikulum fondasi stabil |
| Matematika Keuangan/Mekanika/Metode Numerik/Riset Operasi | `modeling_applied` | selalu mereferensikan konsep inti terlebih dahulu |

## 6. Aturan prasyarat inti

Contoh relasi yang harus ada di registry, bukan hanya tertulis di narasi:

```text
nilai_tempat
  → operasi_bilangan_cacah
  → bilangan_bulat_dan_garis_bilangan
  → penjumlahan_bilangan_bulat
  → operasi_campuran_bilangan_bulat

pecahan_senilai
  → operasi_pecahan
  → rasio_dan_proporsi
  → persamaan_linear_satu_variabel

pola_dan_relasi
  → ekspresi_aljabar
  → persamaan_linear
  → fungsi_linear
  → fungsi_kuadrat
  → limit_fungsi
```

Prasyarat tidak sama dengan urutan tampilan. Satu path boleh mempercepat atau menambah remedial, tetapi tidak boleh menyatakan siswa menguasai node yang prasyaratnya belum terbukti.

## 7. Golden Module: Bilangan Bulat

### 7.1 Identitas

| Field | Nilai |
|---|---|
| Unit ID | `math.number.integer.addition-opposite-signs.v1` |
| Nama | Menjumlahkan Bilangan Bulat Berbeda Tanda |
| Strand | `number` |
| Kedalaman target | F1 → F2 |
| Estimasi | 25–35 menit mandiri; 15–20 menit mode guru |
| Prasyarat | membandingkan bilangan bulat pada garis bilangan; memahami positif/negatif; nilai mutlak dasar |
| Bukti akhir | siswa dapat memodelkan, menghitung, dan menjelaskan penjumlahan dua bilangan bulat berbeda tanda |

### 7.2 Tujuan pembelajaran

Setelah menuntaskan unit, peserta dapat:

1. menentukan arah gerak pada garis bilangan ketika bilangan positif atau negatif ditambahkan;
2. menghitung hasil penjumlahan dua bilangan bulat berbeda tanda dengan strategi nilai mutlak;
3. menjelaskan mengapa tanda hasil mengikuti bilangan dengan nilai mutlak lebih besar;
4. memeriksa kewajaran hasil lewat estimasi/garis bilangan;
5. menyelesaikan masalah kontekstual sederhana dengan model bilangan bulat.

### 7.3 Struktur artikel di Content Studio

| Bagian | Blok Studio yang dipakai | Tujuan |
|---|---|---|
| Diagnosis cepat | sisipan soal: pilihan ganda/isian | cek prasyarat garis bilangan dan urutan bilangan |
| Makna tanda | paragraf, definisi, contoh | positif/negatif sebagai arah atau perubahan, bukan “angka dengan tanda” |
| Visualisasi | sematan CodeWeb `number-line` | peserta menggeser titik dan melihat hasil penjumlahan |
| Aturan ringkas | langkah, contoh dua kolom | bandingkan nilai mutlak lalu tentukan tanda hasil |
| Kesalahan umum | blok kesalahan umum | mencegah “selalu kurangi lalu gunakan tanda bilangan pertama” |
| Aplikasi | contoh, tabel, sisipan soal | suhu, saldo, atau elevasi dengan konteks yang tidak ambigu |
| Refleksi | catatan/pertanyaan singkat | siswa memilih strategi yang paling dipahaminya |

### 7.4 Spesifikasi CodeWeb

`number-line` merupakan widget reusable, bukan halaman unik. Konfigurasinya memuat:

```json
{
  "startRange": [-20, 20],
  "operations": [{"a": 7, "b": -10}, {"a": -4, "b": 9}],
  "showAbsoluteValueComparison": true,
  "teacherMode": true,
  "checkpointAfter": 3,
  "conceptIds": ["integer-number-line", "integer-addition-opposite-signs"]
}
```

Mode guru memiliki kontrol langkah, contoh acak/terkunci, layar penuh, reset, dan jawaban yang dapat disembunyikan. Mode peserta mengirim event standar Titian dan tidak menganggap interaksi sebagai mastery sampai checkpoint dinilai.

### 7.5 Blueprint latihan

| Tahap | Subtype kuis | Kesulitan | Bloom | Tujuan |
|---|---|---|---|---|
| Diagnostik | pilihan ganda tunggal | mudah | C1–C2 | urutan dan posisi bilangan bulat |
| Terarah | interaktif garis bilangan / gap fill | mudah | C2–C3 | menghubungkan arah gerak dengan operasi |
| Penguasaan prosedural | isian numerik | menengah | C3 | menghitung dengan nilai mutlak dan tanda hasil |
| Diagnosis miskonsepsi | pilihan ganda kompleks + pembahasan | menengah | C2–C4 | mengenali alasan yang salah/benar |
| Transfer | jawaban singkat atau uraian ringkas | sulit | C3–C4 | membuat model dari konteks suhu/saldo/elevasi |

Minimal 10 item/variasi tersedia; 4–6 dipilih adaptif untuk satu sesi. Kesulitan awal adalah editorial dan harus dikalibrasi ulang dari data jawaban per versi soal.

### 7.6 Aturan kelulusan dan tindak lanjut

- Jika diagnosis prasyarat gagal: arahkan ke `integer-number-line` atau `comparing-integers`.
- Jika checkpoint <80%: berikan latihan visual tambahan dan variasi konteks yang berbeda.
- Jika checkpoint ≥80% dan tidak ada miskonsepsi tanda: lanjut ke `integer-subtraction-as-addition`.
- Jika siswa cepat selesai: pengayaan `operasi-campuran-bilangan-bulat` dan masalah multi-langkah.

## 8. Reuse Golden Module dalam tiga path

| Path | Peran unit | Tambahan khusus path |
|---|---|---|
| Fondasi SMP | unit inti wajib setelah pengenalan bilangan bulat | latihan bertahap dan tugas kelas |
| Pemulihan adaptif | remedial saat gap pada operasi bilangan bulat terdeteksi | diagnosis lebih singkat, visual lebih banyak, pengulangan terjadwal |
| Numerasi/TKA sesuai jenjang | prasyarat konseptual bila blueprint tes memerlukannya | latihan konteks dan manajemen waktu ditempatkan di item path, bukan menduplikasi unit |

## 9. Definition of Done pilot Matematika

Pilot dianggap selesai hanya bila:

- registry strand/konsep/prasyarat tersimpan dengan kode stabil;
- unit dapat diterbitkan sebagai artikel + widget + kuis dari Studio saat ini;
- setiap soal ditag konsep, kesulitan, Bloom, serta versi;
- CodeWeb mengirim event yang dibaca Titian;
- tiga path mereferensikan unit yang sama, tanpa menyalin artikel atau soal inti;
- guru dapat memakai mode presentasi dan peserta dapat menyelesaikan mode mandiri;
- ahli Matematika meninjau ketepatan konsep, contoh, dan miskonsepsi.

## 10. Urutan setelah pilot

1. Lengkapi strand `number`: cacah → nilai tempat → operasi → bilangan bulat → pecahan → rasio/persen → eksponen/akar.
2. Bangun `algebra_functions`, dimulai dari pola → ekspresi → persamaan linear.
3. Tambahkan peta CP Fase A–F di atas registry yang sudah stabil.
4. Baru turunkan path Matematika sekolah, TKA, UTBK, Cambridge, dan lanjut.

Pendekatan ini memastikan satu peningkatan pada konsep bilangan bulat memperbaiki semua path yang menggunakannya.
