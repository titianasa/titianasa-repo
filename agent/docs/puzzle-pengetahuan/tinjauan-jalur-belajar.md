# Jalur belajar Matematika dan Bahasa Inggris: acuan resmi 2026

Status: acuan ditetapkan 2026-11-02. Isinya dipakai untuk menyusun ulang jalur ujian dan daftar kartu kanonik.

Fokus pemilik: Kurikulum Indonesia, TKA, dan UTBK-SNBT, ditambah CEFR untuk Bahasa Inggris. Cambridge, IELTS, TOEFL, TOEIC, dan AKM disembunyikan dulu (status `draft`). Datanya tetap ada dan bisa dikembalikan.

## Dokumen acuan

Semua dokumen di bawah dibaca dari berkas resminya, bukan dari ringkasan.

| Untuk | Dokumen | Status 2026 |
|---|---|---|
| Kurikulum Indonesia | Kep. Kepala BSKAP 046/H/KR/2025 tentang Capaian Pembelajaran ([Ruang GTK](https://guru.kemendikdasmen.go.id/dokumen/74r6Yln0zK)) | Berlaku. Kep. Kepala BKPDM 020/2026 hanya mengubah CP Pendidikan Agama dan Budi Pekerti ([siaran pers](https://bkpdm.kemendikdasmen.go.id/publikasi/capaian-pembelajaran-baru-telah-terbit-yang-berubah-hanya-mata-pelajaran-agama-dan-budi-pekerti)) |
| Penyelenggaraan TKA | Kepmendikdasmen 56/2026 tentang Pedoman Penyelenggaraan TKA dan AN ([PDF](https://pusmendik.kemendikdasmen.go.id/pdf/file-201)) | Berlaku sejak 6 Maret 2026, menggantikan Kepmendikdasmen 95/M/2025 |
| Isi TKA SD dan SMP | Perka BSKAP 047/H/AN/2025 ([PDF](https://pusmendik.kemendikdasmen.go.id/pdf/file-204)) | Masih menjadi kerangka yang diunggah Pusmendik untuk TKA 2026 |
| Isi TKA SMA dan SMK | Perka BSKAP 045/H/AN/2025 ([PDF](https://pusmendik.kemendikdasmen.go.id/pdf/file-202)) | Sama |
| UTBK-SNBT | Framework UTBK-SNBT 2026 ([snpmb.id/fr](https://snpmb.id/fr/)) | Untuk ujian April 2026. Framework 2027 belum terbit, jadi dicek lagi saat terbit |

## Yang berubah di 2026

1. **Soal AKM masuk ke TKA.** Soal numerasi AN digabung ke mata uji Matematika (SD, SMP, dan Matematika wajib SMA). Soal literasi membaca digabung ke Bahasa Indonesia. Jadi tidak perlu jalur AKM terpisah, tapi kemasan TKA Matematika harus memuat soal numerasi berkonteks.
2. **TKA dan AN diselenggarakan bersama** untuk kelas 6, kelas 9, dan kelas 12.
3. **Bentuk soal TKA dan AN:** pilihan ganda, dan pilihan ganda kompleks dalam dua model, yaitu lebih dari satu jawaban benar dan kategori.

## Kurikulum Indonesia (CP 2025)

### Matematika

Elemen konten: Bilangan, Aljabar, Pengukuran, Geometri, Analisis Data dan Peluang. Elemen proses: penalaran dan pembuktian, pemecahan masalah, komunikasi, koneksi, representasi.

| Fase | Kelas | Isi pokok per elemen |
|---|---|---|
| A | 1–2 | Cacah sampai 100, nilai tempat, tambah dan kurang sampai 20, pecahan ½ dan ¼. Makna "=", pola bukan bilangan. Ukur tak baku. Bangun datar dan ruang, posisi. Turus dan piktogram |
| B | 3–4 | Cacah sampai 10.000, kali dan bagi sampai 100, kelipatan dan faktor, pecahan senilai, desimal, persen. Nilai yang tidak diketahui, pola bilangan. Satuan baku cm, m, g, kg, luas dan volume. Ciri bangun datar. Tabel, piktogram, diagram batang |
| C | 5–6 | Cacah sampai 1.000.000, uang, KPK dan FPB, operasi pecahan, desimal. Pola, rasio satuan, proporsi. Keliling, luas, waktu, sudut. Kubus, balok, tampak depan/atas/samping, peta berpetak. Tabel frekuensi, kemungkinan kejadian |
| D | 7–9 | Bilangan bulat, rasional, berpangkat, akar, notasi ilmiah, rasio, literasi finansial. Bentuk aljabar, relasi dan fungsi, PLSV, PtLSV, SPLDV. Lingkaran, luas permukaan dan volume. Jaring-jaring, sudut garis sejajar, kongruen dan sebangun, Pythagoras, transformasi. Data dan peluang |
| E | 10 | Pangkat pecahan. SPtLDV, persamaan dan fungsi kuadrat termasuk akar imajiner, eksponen. Trigonometri sudut lancip. Kuartil, box plot, histogram, diagram pencar |
| F | 11–12 | Barisan dan deret, bunga, anuitas. Fungsi invers, komposisi, transformasi fungsi. Lingkaran. Asosiasi dua variabel, regresi linear, peluang majemuk dan bersyarat, permutasi dan kombinasi |

Matematika Tingkat Lanjut (Fase F) adalah mata pelajaran tersendiri. Elemennya dirangkum ringkas dari CP: aljabar dan fungsi lanjut, geometri, kalkulus, dan seterusnya.

**Catatan:** CP mengatur per fase, bukan per kelas. Jadi pembagian kelas di dalam satu fase adalah susunan kita sendiri, idealnya mengikuti urutan buku teks resmi. Konsekuensinya:
- Bilangan bulat memang Fase D, sesuai TKA SD yang tidak memuatnya. Penempatannya di Kelas 7 sudah benar.
- `canon_units.level` yang menaruhnya di Level 6 perlu dikoreksi.

### Bahasa Inggris

| Fase | Kelas | Setara CEFR | Kosakata |
|---|---|---|---|
| A | 1–2 | Tidak diwajibkan | |
| B–C | 3–6 | A1 | 1.000 kata frekuensi tinggi |
| D | 7–9 | A2 | 2.000 kata |
| E | 10 | B1 | 3.000 kata |
| F | 11–12 | B2 | 4.000 kata |
| Tingkat Lanjut | 11–12 | B2. Teks narasi, eksposisi, dan diskusi | |

Elemennya ada tiga: Menyimak–Berbicara, Membaca–Memirsa, Menulis–Mempresentasikan. Jadi jalur Kurikulum Indonesia harus berbasis keterampilan dan jenis teks, bukan grammar saja.

Sudah diterapkan di dev: jalur `inggris-kurikulum-indonesia` sekarang dimulai Kelas 3 dan memakai tabel di atas. Kelas 10 berisi 70 unit B1, sedangkan kelas lain 7–22 unit. Ketimpangan ini akibat bank unit kanonik, bukan akibat CP.

## TKA 2026

Peserta TKA adalah kelas 6, kelas 9, dan kelas 12. Jadi jalur TKA dibagi per jenjang, lalu per mata uji.

| Jenjang | Mata uji | Isi dari kerangka resmi |
|---|---|---|
| SD (kelas 6) | Matematika | Bilangan (pecahan, operasi cacah, KPK, FPB), Geometri dan Pengukuran (satuan, waktu, kecepatan, keliling, luas, volume, sudut), Data. Tidak ada aljabar dan bilangan bulat |
| SMP (kelas 9) | Matematika | Bilangan real, Aljabar (PLSV, PtLSV, SPLDV, bentuk aljabar, fungsi, barisan dan deret), Geometri dan Pengukuran, Data dan Peluang |
| SMA (kelas 12), wajib | Matematika | Bilangan real, Aljabar (SPL tiga variabel, program linear, fungsi, invers, komposisi, barisan dan deret), Geometri dan Pengukuran, Trigonometri, Data dan Peluang |
| SMA, wajib | Bahasa Inggris | Membaca saja. Teks descriptive, recount, narrative, procedure, dan analytical exposition. Teks B1 250–350 kata, sebagian A2. Tiga level: tekstual, inferensial, evaluasi dan apresiasi |
| SMA, pilihan | Matematika Lanjutan | Matriks, polinomial, fungsi lanjut, vektor, lingkaran, transformasi dengan matriks, limit |
| SMA, pilihan | Bahasa Inggris Lanjutan | Membaca teks yang lebih kompleks |

SD dan SMP tidak punya mata uji Bahasa Inggris. Mata uji pilihan SMA ada 19, dan SMK menambah Teori Kompetensi Kejuruan.

Level kognitifnya Pengetahuan dan Pemahaman, Aplikasi, dan Penalaran. Soal bisa tunggal, atau grup dengan satu stimulus.

## UTBK-SNBT 2026

Total 160 soal dalam 195 menit.

| Kelompok | Subtes | Soal | Menit | Relevan untuk |
|---|---|---|---|---|
| TPS | Penalaran Umum: induktif, deduktif, kuantitatif | 30 | 30 | Matematika, untuk bagian kuantitatif |
| TPS | Pengetahuan dan Pemahaman Umum | 20 | 15 | |
| TPS | Pemahaman Bacaan dan Menulis | 20 | 25 | |
| TPS | Pengetahuan Kuantitatif: bilangan, aljabar, geometri dan pengukuran, analisis data, peluang. Kedalaman sesuai kurikulum SMA | 20 | 20 | Matematika |
| Literasi | Literasi dalam Bahasa Indonesia | 30 | 42,5 | |
| Literasi | Literasi dalam Bahasa Inggris: menemukan, memahami, menilai, merefleksi. Teks berkonteks saintek, soshum, dan personal | 20 | 20 | Bahasa Inggris |
| Literasi | Penalaran Matematika: merumuskan, menggunakan, menafsirkan. Konteks pribadi, pekerjaan, sosial, ilmiah | 20 | 42,5 | Matematika |

## Selisih dengan jalur di dev dan rencana perbaikan

| Jalur di dev | Selisih | Perbaikan |
|---|---|---|
| `tka-numerasi` | Satu jalur untuk semua jenjang. Ada Analisis Real, Variabel Acak, dan Logaritma, yang tidak diujikan di Matematika wajib | Ganti dengan TKA SD · Matematika, TKA SMP · Matematika, TKA SMA · Matematika, dan TKA SMA · Matematika Lanjutan. Kelompoknya mengikuti elemen dan sub-elemen kerangka |
| `tka-bahasa-inggris` | 41 unit grammar dan 12 writing, padahal TKA hanya membaca | Ganti dengan TKA SMA · Bahasa Inggris dan TKA SMA · Bahasa Inggris Lanjutan. Isinya membaca per jenis teks dan level |
| `utbk-pengetahuan-kuantitatif`, `utbk-penalaran-matematika` | Isinya pemetaan otomatis | Susun ulang per cakupan framework. Penalaran Matematika diisi soal berkonteks per siklus merumuskan, menggunakan, dan menafsirkan |
| `utbk-literasi-bahasa-inggris` | 11 kelompok hasil pemetaan otomatis | Susun ulang: membaca teks saintek, soshum, dan personal |
| Tidak ada | Penalaran Umum, bagian kuantitatif | Tambah sebagai jalur UTBK-SNBT · Penalaran Umum (kuantitatif), atau gabungkan ke Pengetahuan Kuantitatif |
| `matematika-kurikulum-indonesia` | Kelompok sudah diberi label fase. Level unit masih draf | Koreksi `canon_units.level` mengikuti tabel CP di atas |
| `cefr-inggris` | 64% grammar, reading dan listening hanya 15 unit | Tetap dipakai. Ditambah unit keterampilan per level |

## Akibatnya untuk kartu kanonik

1. **Kumpulan reading Bahasa Inggris paling mendesak.** Satu kumpulan dipakai bersama oleh empat jalur: TKA SMA, UTBK Literasi Bahasa Inggris, Kurikulum Indonesia (Membaca–Memirsa), dan CEFR. Isinya jenis teks descriptive, recount, narrative, procedure, dan analytical exposition, ditambah teks saintek dan soshum untuk UTBK. Tiap jenis teks di level A2 dan B1, dengan soal tekstual, inferensial, dan evaluatif.
2. **Model soal baru untuk kemasan ujian:**
   - PGK lebih dari satu jawaban benar.
   - PGK kategori dalam bentuk tabel benar/salah.
   - Soal grup dengan satu stimulus berupa teks, tabel, atau grafik.
   - Kartu bacaan 200–350 kata, yang digulir di website dan dipecah saat dirender.
3. **Kemasan TKA Matematika harus memuat soal numerasi berkonteks**, karena soal AKM sekarang ada di dalamnya.
4. **Kemasan "Nouns, Gaya Soal TKA" harus diganti.** Isinya isian grammar, sedangkan TKA Bahasa Inggris hanya membaca.
5. **Urutan kumpulan Matematika** mengikuti Fase A sampai F di atas. Sub-elemen TKA dan cakupan SNBT dipakai sebagai daftar periksa: setiap sub-elemen harus punya minimal satu deck.
