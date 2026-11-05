# Acuan buku teks Matematika per kelas

Status: dikumpulkan 2026-11-03 untuk menyusun ulang jalur `matematika-kurikulum-indonesia` per kelas. Sumber: buku siswa resmi Kurikulum Merdeka dari Pusat Perbukuan (SIBI). Server resmi `static.buku.kemdikbud.go.id` tidak terjangkau dari mesin dev, jadi PDF diunduh dari salinan dengan jalur file yang sama, `static-sc.cloudapp.web.id/content/pdf/bukuteks/kurikulum21/`. Daftar isi Kelas III, VIII, dan IX cocok dengan ringkasan katalog resmi di hasil pencarian. PDF dan daftar isi lengkap ada di `~/.cache/titian-qa-tmp/bse/`.

**Catatan penting.** CP menetapkan capaian per fase, sedangkan pembagian per kelas di bawah ini berasal dari buku teks. Buku SD dan SMP masih terbitan 2022, jadi disusun sebelum CP 046/2025. Buku SMA Kelas X dan XI sudah direvisi (2023 dan 2024), dan Kelas XII revisi 2025. Kalau buku revisi SD/SMP terbit, susunan di bawah perlu dicek ulang.

| Kelas | Fase | Berkas (tahun) | Bab |
|---|---|---|---|
| I | A | `Matematika-BS-KLS-I` (2022) | Membilang sampai 10; penjumlahan sampai 10; pengurangan sampai 10; mengenal bentuk; membilang sampai 20; penjumlahan dan pengurangan sampai 20; mengukur panjang benda; mengenal diagram |
| II | A | `Matematika-BS-KLS-II` (2022) | Membilang sampai 50 dan nilai tempat; penjumlahan dan pengurangan; bentuk di sekitar kita (bangun datar, mengurai-menyusun, bangun ruang); posisi benda dan pola; setengah dan seperempat; pengukuran berat dan waktu; bilangan sampai 100; diagram turus dan diagram gambar |
| III | B | `Matematika_BS_KLS_III` (2022) | Bilangan cacah sampai 1.000 (nilai tempat, keempat operasi sampai 100); kalimat matematika; pengukuran panjang dan berat dengan satuan baku; unsur bangun datar (sisi, sudut, garis tegak lurus dan sejajar); penyajian data dalam tabel |
| IV | B | `Matematika-BS-KLS-IV` (2022) | Bilangan cacah sampai 10.000, faktor dan kelipatan; pecahan (pembilang satu, senilai, desimal persepuluhan dan perseratusan, konsep persen); pola gambar dan pola bilangan; pengukuran luas dan volume; bangun datar (ciri, komposisi, dekomposisi); piktogram dan diagram batang |
| V | C | `Matematika-BS-KLS-V` (2022) | Bilangan cacah sampai 100.000; KPK dan FPB (faktor prima); pecahan (membandingkan, menjumlah, mengurang); keliling bangun datar; luas daerah bangun datar; sudut; ciri-ciri segitiga dan segi empat; data (piktogram, diagram batang); bilangan cacah sampai 1.000.000 |
| VI | C | `Matematika_BS_KLS_VI` (2022) | Pecahan dan desimal (kali, bagi, mengubah ke desimal, membandingkan desimal); rasio (kesamaan rasio, rasio satuan); kubus dan balok (jaring, visualisasi spasial, lokasi); peluang (skala peluang, membandingkan peluang) |
| VII | D | `Matematika-BS-KLS-VII` (2022) | Bilangan bulat; bilangan rasional; rasio (skala, laju perubahan); bentuk aljabar; kesebangunan (hubungan antarsudut, kesebangunan segitiga); data dan diagram (batang, lingkaran) |
| VIII | D | `Matematika-BS-KLS-VIII-Baru` (2022, Tohir dkk.) | Bilangan berpangkat dan bentuk akar; teorema Pythagoras (tripel, segitiga istimewa, rumus jarak sebagai pengayaan); persamaan dan pertidaksamaan linear satu variabel; relasi dan fungsi; persamaan garis lurus (grafik, kemiringan); statistika (pemusatan dan penyebaran data) |
| IX | D | `Matematika_BS_KLS_IX` (2022, Kristanto dkk.) | Sistem persamaan linear dua variabel; bangun ruang (jaring, luas permukaan dan volume sisi datar dan lengkung, keliling dan luas lingkaran, busur, juring); transformasi geometri (translasi, refleksi, rotasi, kekongruenan, dilatasi); peluang dan pemilihan sampel |
| X | E | `Matematika_BS_KLS_X_Rev` (2023) | Eksponen dan bentuk akar, fungsi eksponensial; barisan, deret, dan bunga; perbandingan trigonometri; sistem persamaan dan pertidaksamaan linear; persamaan dan fungsi kuadrat; representasi dan interpretasi data; peluang (distribusi, aturan penjumlahan dan perkalian) |
| XI | F | `Matematika_BS_KLS_XI_Rev` (2024) | Statistika data bivariat (kategorikal, numerikal, hubungan dua variabel); komposisi fungsi dan fungsi invers; transformasi fungsi (geser, cermin, regang); lingkaran (busur, garis singgung, tali busur) |
| XI lanjut | F | `Matematika-Tingkat-Lanjut-BS-KLS-XI` (2022) | Bilangan kompleks; polinomial (pembagian, faktor, identitas); matriks (determinan, invers); transformasi geometri dengan matriks; fungsi trigonometri, logaritma, dan aljabar beserta pemodelannya |
| XII | F | `Matematika_BS_KLS_XII_Rev` (2025) | Barisan dan deret, bunga tunggal; investasi dan pinjaman (bunga majemuk, anuitas); kaidah pencacahan (permutasi, kombinasi); peluang (kejadian majemuk) |
| XII lanjut | F | `Matematika_Lanjut_BS_KLS_XII` (2022) | Geometri analitik (lingkaran, garis singgung, irisan kerucut: parabola, elips, hiperbola); limit fungsi aljabar dan trigonometri; turunan dan aplikasinya; integral dan teorema dasar kalkulus; distribusi seragam, binomial, dan normal |

Edisi 2021 adaptasi Gakko Tosho untuk Kelas VII–IX punya urutan berbeda, misalnya faktorisasi, akar kuadrat, dan persamaan kuadrat di Kelas IX. Edisi itu tidak dipakai.

## Tiga sumber, satu pemeriksa

Semua pemetaan ada di `titian-backend-go/data/kanonik/sumber/` dan diperiksa oleh `python3 sumber/cek_cakupan.py`:

| Berkas | Isi | Dipakai untuk |
|---|---|---|
| `buku-teks-matematika.json` | 270 subbab buku siswa I–XII dan Tingkat Lanjut XI–XII, masing-masing ke unit kanonik | Kelas tempat sebuah unit diajarkan |
| `cp-matematika-2025.json` | Butir CP 046/H/KR/2025 Fase A–F dan Matematika Tingkat Lanjut | Fase untuk unit yang tidak dibahas buku (buku SD/SMP terbit sebelum CP 2025) |
| `tka-matematika-2025.json` | Muatan TKA Matematika dan Tingkat Lanjut SMA, Peraturan BSKAP 045/H/AN/2025 | Jalur TKA dan materi ujian di luar buku dan CP |

Hasil pemeriksaan 2026-11-03:

- Semua kunci unit di ketiga berkas valid.
- 150 dari 274 unit dibahas buku. CP menempatkan 22 unit lagi, misalnya urutan operasi campuran dan keterbagian di Fase C, bilangan irasional dan koordinat Kartesius di Fase D, serta aturan sinus-cosinus dan identitas trigonometri di Tingkat Lanjut.
- Ada 14 unit baru yang perlu dibuat. Satu di antaranya hanya disebut CP, yaitu fungsi tangga dan fungsi sepotong-sepotong. Selain itu ada 22 catatan pecah unit.
- TKA SMA menguji lima unit yang tidak ada di buku maupun CP: program linear (dua unit), kedudukan titik-garis-bidang, jarak dan sudut dalam ruang, serta proyeksi vektor. Unit ini masuk jalur TKA, tidak masuk jalur kelas.
- Unit sekolah lama yang tidak ada di buku, CP, maupun TKA tetap dipertahankan di kanonik untuk jalur ujian lain (SNBT, ujian mandiri) dan untuk jalur berurutan: pecahan aljabar, pertidaksamaan kuadrat, persamaan logaritma, notasi sigma, induksi, rumus jumlah dan selisih sudut, logika, limit di ketakhinggaan, serta penalaran kuantitatif. Sisanya, sekitar 80 unit, adalah materi kuliah.
