# Riset Kelas 3–12 (SD atas, SMP, SMA): beban baca, visual, urutan latihan, dan kesiapan TKA

> **Pemakaian (ADR-0026, 2026-11-03):** batas per jenjang (Kelas 3–4, 5–6, SMP, SMA) dan bentuk soal TKA (M25, M26) berlaku untuk deck jalur. Deck kanonik memakai satu standar `mtk`, dengan prinsip contoh kerja, latihan, dan level soal dari riset ini (M8, M14–M24).

Disusun 2026-11-03 untuk deck Matematika Titian Asa (kartu 9:16). Lanjutan dari `riset-kelas-awal.md` (Kelas 1–2, aturan A1–A19). Aturan di sini diberi kode M1, M2, dan seterusnya. Gerbang yang dibandingkan: `titian-web/scripts/periksa-kartu.ts`, dengan batas di `scripts/tingkat-kartu.ts` (sekarang sd 75 kata/22 per kalimat, smp 90/28, sma 95/30; visual 15%/10%/10%; latihan ≥5).

## Kesimpulan singkat

- **Batas kata di gerbang sekarang terlalu longgar.** Buku siswa resmi berhenti di sekitar 10 kata per kalimat (SD atas) dan 11–12 (SMP, SMA). Batas 22–30 kata per kalimat jauh di atas persentil ke-90 buku. Kisi-kisi TKA juga menulis teks bacaan dengan **3–7 kata per kalimat untuk SD, 5–9 untuk SMP, dan 8–12 untuk SMA**. Usulan: maksimal 12/15/18/20 kata per kalimat (Kelas 3–4 / Kelas 5–6 / SMP / SMA). Untuk kata per kartu: maksimal 40/55/70/85.
- **Daya baca siswa rendah, jadi kesulitan bahasa tidak boleh ikut menjadi beban soal Matematika.** Hanya 17% siswa usia 15 tahun yang mencapai Level 2 matematika di PISA 2025, dan 27% di membaca. Sekitar sepertiga siswa SD–SMA masih di bawah kompetensi minimum numerasi AKM.
- **Visual:** gambar skematis yang menyatu dengan teks terbukti membantu. Gambar hiasan merugikan. Gambar wajib untuk geometri, grafik/fungsi, data, peluang, dan model batang. Untuk topik prosedural (aljabar, eksponen, turunan), contoh kerja lebih penting daripada gambar. Usulan porsi kartu ajar bergambar atau lab: ≥50% / ≥40% / ≥35% / ≥30%.
- **Urutan latihan:** contoh kerja, lalu soal serupa, lalu contoh yang dipudarkan (memudar), lalu latihan mandiri bertingkat, lalu latihan campuran, lalu pengulangan berjarak. Minimal 3 soal per sub-kasus, dan minimal 8 latihan per deck.
- **TKA:** tiga level kognitif (Pengetahuan & Pemahaman, Aplikasi, Penalaran). Ada tiga bentuk soal, semuanya objektif: PG, PGK MCMA (jawaban benar bisa lebih dari satu), dan PGK kategori (benar/salah per pernyataan). Konteksnya "permasalahan matematika" atau "sehari-hari". Kerangka TKA **tidak menyebut proporsi**. Proporsi resmi yang paling dekat adalah desain AKM numerasi (30/50/20 untuk kelas 5, 25/50/25 untuk kelas 8, 20/50/30 untuk kelas 11). Sejak 2026, soal numerasi AN digabung ke mata uji Matematika TKA.

---

## 1. Beban baca

### 1.1 Kemampuan membaca dan numerasi siswa

| Data | Tahun | Siapa | Angka |
|---|---|---|---|
| EGRA nasional | 2012 | 4.233 siswa kelas 3 | 68 kata/menit dalam teks bersambung; "tidak selalu memahami" ([ACDP 2014](https://repositori.kemendikdasmen.go.id/8564/1/Working-Paper-ACDP-EGRA-English-FINAL.pdf)) |
| AKSI/INAP | 2016 | kelas 4, nasional | 47% kategori "kurang" dalam membaca ([Devpolicy](https://devpolicy.org/using-data-to-drive-education-policy-in-indonesia-20211124/)) |
| INOVASI *Learning Gap* | 2021 | 18.370 siswa kelas 1–3 | hanya 55% siswa kelas 3 di standar minimum literasi ([INOVASI](https://www.inovasi.or.id/en/publication/the-learning-gap-series/)) |
| Rapor Pendidikan (AN 2024) | rilis Mar 2025 | nasional | **Mencapai kompetensi minimum numerasi: SD 69,51%, SMP 68,1%, SMA 63,71%, SMK 64,02%.** Literasi: SD 71,76%, SMP 70,34%, SMA 64,83%. Semua jenjang masih kategori "sedang" ([Puslapdik](https://puslapdik.kemendikdasmen.go.id/kemendikdasmen-terbitkan-raport-pendidikan-2022-2024/); [ntvnews](https://www.ntvnews.id/news/0140244/kemendikdasmen-rilis-rapor-pendidikan-2022-2024-capaian-literasi-dan-numerasi-meningkat-ketimpangan-masih-jadi-pr)) |
| Rapor Pendidikan rilis Jun 2026 (kemungkinan AN 2025; tahun data tidak disebut) | 2026 | nasional | Numerasi: SD 59,45%, SMP 70,81%, SMA 67,14%, SMK 60,22% ([Kompas](https://www.kompas.com/edu/read/2026/06/20/093927871/pemerintah-ungkap-capaian-literasi-numerasi-siswa-sd-hingga-smk)) |
| PISA 2022 | 2022 | usia 15 | Matematika 366 (OECD 472). **18%** mencapai Level 2+ (OECD 69%). Membaca 359, 25% di Level 2+ ([OECD](https://www.oecd.org/en/publications/pisa-2022-results-volume-i-and-ii-country-notes_ed6fbcc5-en/indonesia_c2e1ae0e-en.html)) |
| PISA 2025 | rilis Sep 2026 | usia 15 | **17%** Level 2+ matematika, **27%** Level 2+ membaca. Hasil "kurang lebih sama dengan 2022" ([OECD country note](https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/09/pisa-2025-results-volume-i-country-notes_88d1164e/indonesia_20c83120/9c880f8a-en.pdf)) |

**Bahasa adalah beban tambahan pada soal Matematika.** Penyederhanaan bahasa soal (tanpa mengubah matematikanya) menaikkan skor, terutama bagi siswa berbahasa kedua dan siswa dari kelompok sosial-ekonomi rendah (Abedi & Lord 2001, *Applied Measurement in Education* 14(3): 219–234, https://doi.org/10.1207/S15324818AME1403_2). Banyak siswa Indonesia berbahasa ibu daerah. Ditambah data di atas, ini berarti: **kalimat pendek dan kosakata sehari-hari, sedangkan istilah resmi diperkenalkan dan diberi arti.**

### 1.2 Standar resmi panjang kalimat

| Sumber | Jenjang | Kata/kalimat | Lainnya |
|---|---|---|---|
| Pedoman Perjenjangan Buku (Per. Ka. BSKAP 030/P/2022) | B3, 8–10 th | **≤12** | ≤3 paragraf × 3 kalimat per halaman |
| | C "Semenjana", 10–13 th | **≤12** | ≤4 paragraf × 5 kalimat per halaman; ilustrasi atau infografik "yang mendukung teks" |
| | D "Madya", 13–15 th; E "Mahir", >16 th | tidak dibatasi angka | kalimat tunggal dan majemuk; D: "diagram/grafik … yang mendukung teks" |
| Kerangka TKA, Bahasa Indonesia SD (047/H/AN/2025, `file-178.txt` baris 345–349) | kelas 6 | **3–7** | teks 150–200 kata |
| Kerangka TKA, Bahasa Indonesia SMP (`file-178.txt` 722–727) | kelas 9 | **5–9** | teks 200–250 kata |
| Kerangka TKA, Bahasa Indonesia SMA (045/H/AN/2025, `file-175.txt` 363–368) | kelas 12 | **8–12** | teks 250–300 kata; tingkat lanjut 300–350 kata |

Sumber Perjenjangan: https://www.ikapi.org/wp-content/uploads/2022/06/Pedoman-Perjenjangan-Buku-Pusat-Perbukuan-BSKAP.pdf

### 1.3 Hitungan buku siswa Matematika Kurikulum Merdeka (Pusat Perbukuan)

Metodenya sama dengan `riset-kelas-awal.md`. Teks diambil dengan `pdftotext -layout` dari PDF di `bse/` (berkas `.txt` lokal hanya memuat 16 halaman, jadi tidak dipakai). Hanya halaman isi yang dihitung (6–88% dari total halaman). Kata = token alfabet ≥2 huruf. Baris footer/judul berjalan dibuang. Kalimat = potongan di `.!?` yang diikuti huruf kapital, dengan panjang 3–80 kata. Hasil Kelas III dan IV sama dengan hitungan sebelumnya (53 dan 79), jadi metodenya konsisten.

| Buku | Hal. isi | Kata/hal. median | P25 | P75 | P90 | Kata/kalimat median | P75 | P90 |
|---|---|---|---|---|---|---|---|---|
| III | 196 | **53** | 38 | 76 | 99 | **8** | 12 | 16 |
| IV | 185 | **79** | 55 | 109 | 142 | **9** | 14 | 21 |
| V | 269 | **84** | 61 | 109 | 131 | **10** | 15 | 22 |
| VI | 132 | **110** | 86 | 135 | 170 | **10** | 15 | 23 |
| VII | 224 | **108** | 79 | 139 | 177 | **11** | 16 | 24 |
| VIII | 283 | **109** | 73 | 147 | 175 | **12** | 18 | 26 |
| IX | 263 | **128** | 98 | 154 | 181 | **12** | 18 | 25 |
| X (Rev 2023) | 257 | **130** | 100 | 164 | 195 | **11** | 17 | 25 |
| XI (Rev 2024) | 218 | **125** | 80 | 168 | 203 | **12** | 18 | 25 |
| XII (Rev 2025) | 176 | **148** | 123 | 186 | 221 | **12** | 17 | 25 |
| XI Tingkat Lanjut | 288 | 120 | 100 | 147 | 173 | 11 | 17 | 24 |
| XII Tingkat Lanjut | 185 | 135 | 108 | 168 | 200 | 12 | 17 | 26 |

Pola:
- **Kata per kalimat naik dari 8 ke 12, lalu mendatar sejak SMP.**
- **Kata per halaman naik hampir tiga kali**, dari 53 (III) ke 148 (XII).
- **Batas gerbang sekarang (22/28/30 kata per kalimat) berada di sekitar P90 buku atau lebih.** Akibatnya satu kalimat terpanjang di setiap kartu boleh sepanjang kalimat terpanjang 10% di buku.

### 1.4 Dari halaman buku ke kartu 9:16

- **Luas halaman dibanding layar.** Halaman B5 (≈17,6 × 25 cm ≈ 440 cm²) sekitar 4–5 kali luas layar ponsel (≈6,5 × 14 cm). Teks di ponsel (16 px ≈ 2,5 mm tinggi huruf kecil) sedikit lebih kecil dari teks buku 11–12 pt. Jadi kepadatan yang setara kira-kira **kata per halaman ÷ 2,5–3**. Ini perkiraan berbasis luas dan ukuran huruf, bukan standar resmi.
- **Hasil konversi (median ÷ 2,5 → P90 ÷ 2,5):** SD atas 21–44 → 40–68 kata; SMP 43–51 → 70–72; SMA 50–59 → 78–88.
- **Waktu baca.** Siswa kelas 3 membaca sekitar 68 kata/menit (EGRA 2012), jadi 40 kata ≈ 35 detik per kartu. Prinsip *segmenting* menyarankan satu ide per potongan yang tempo bacanya diatur pelajar (Mayer 2024, *Educational Psychology Review* 36:8, https://doi.org/10.1007/s10648-023-09842-1).
- **Batas yang diusulkan (M1–M4):** batas keras ≈ P90 buku ÷ 2,5, dan median deck ≈ median buku ÷ 2,5.
  - Kelas 3 diberi batas lebih ketat dari Kelas 5–6, karena kepadatan buku III kira-kira setengah dari buku VI.
  - Untuk SMA tingkat lanjut, batas SMA dipakai dengan kelonggaran kecil.

Catatan cara hitung: gerbang menghitung setiap token yang berisi huruf, termasuk variabel satu huruf seperti "x". Hitungan buku di atas hanya token ≥2 huruf. Karena itu ambang di bawah sudah diberi kelonggaran sekitar 10%.

---

## 2. Porsi visual

### 2.1 Bukti

| Prinsip | Temuan | Sumber |
|---|---|---|
| Multimedia, *dual coding* | Kata + gambar lebih baik daripada kata saja, karena sistem verbal dan sistem gambar saling menguatkan | Mayer 2024 (di atas); Clark & Paivio 1991, *Educ. Psych. Review* 3: 149–210, https://doi.org/10.1007/BF01320076 |
| Panduan IES | "Combine graphics with verbal descriptions" dan "Connect abstract and concrete representations": bukti **sedang** | Pashler dkk. 2007, NCER 2007-2004, https://ies.ed.gov/ncee/wwc/Docs/PracticeGuide/20072004.pdf |
| Panduan IES kelas 4–8 | "Teach students how to use visual representations": bukti **kuat** | Woodward dkk. 2012, NCEE 2012-4055, https://ies.ed.gov/ncee/wwc/Docs/PracticeGuide/MPS_PG_043012.pdf |
| Panduan IES SD (intervensi) | Representasi visual dan manipulatif, serta garis bilangan: bukti sedang | Fuchs dkk. 2021, WWC 2021006, https://ies.ed.gov/ncee/wwc/Docs/PracticeGuide/WWC2021006-Math-PG.pdf |
| Gambar skematis vs gambar pemandangan | Representasi **skematis** (relasi ruang, ukuran) berkorelasi positif dengan kemampuan memecahkan soal. Representasi **piktorial** (penampilan benda) berkorelasi negatif | Hegarty & Kozhevnikov 1999, *J. Educ. Psych.* 91(4): 684–689, https://doi.org/10.1037/0022-0663.91.4.684 |
| Detail menarik yang tak relevan | Detail menarik yang tidak relevan **menurunkan** hasil belajar (g ≈ −0,33) | Sundararajan & Adesope 2020, *Educ. Psych. Review* 32: 707–734, https://doi.org/10.1007/s10648-020-09522-4 |
| Kontiguitas | Teks yang diletakkan di dalam atau di samping gambar lebih baik daripada teks yang terpisah (d ≈ 0,7) | Ginns 2006, *Learning and Instruction* 16: 511–525, https://doi.org/10.1016/j.learninstruc.2006.10.001 |
| Modalitas (anak) | Pada siswa kelas 4, teks yang dibacakan lebih baik daripada teks tertulis di samping gambar | Herrlinger dkk. 2017, https://doi.org/10.1007/s11165-016-9525-y ; meta-analisis Ginns 2005, https://doi.org/10.1016/j.learninstruc.2005.07.001 |
| CPA Singapura (SD atas) | Konkret–Piktorial–Abstrak, berakar pada Bruner, menjadi inti pengajaran SD Singapura. **Model batang** adalah tahap piktorial untuk soal cerita, pecahan, dan perbandingan | Leong, Ho & Cheng 2015, *The Mathematics Educator* 16(1): 1–18, https://repository.nie.edu.sg/server/api/core/bitstreams/700a4f49-3cdd-4365-9802-92b8634b39eb/content ; Ng & Lee 2009, *JRME* 40(3): 282–313, https://doi.org/10.5951/jresematheduc.40.3.0282 |
| *Concreteness fading* | Mulai dari yang konkret, lalu dipudarkan bertahap ke abstrak. Cara ini lebih baik untuk transfer | Fyfe dkk. 2014, https://doi.org/10.1007/s10648-014-9249-3 |
| *Expertise reversal* | Bantuan (gambar penjelas, contoh terurai) yang menolong pemula bisa menjadi beban bagi pelajar yang sudah mahir | Kalyuga dkk. 2003, *Educ. Psychologist* 38(1): 23–31, https://doi.org/10.1207/S15326985EP3801_4 |

### 2.2 Buku siswa sebagai pembanding (batas bawah)

Persentase halaman isi yang memuat gambar raster (>60 px) atau label "Gambar n":

| Buku | III | IV | V | VI | VII | VIII | IX | X | XI | XII |
|---|---|---|---|---|---|---|---|---|---|---|
| % halaman | 77 | 79 | 71 | 27* | 48 | 25* | 73 | 30 | 28 | 29 |

*Buku VI dan VIII memakai banyak gambar vektor tanpa label, jadi angkanya pasti di bawah angka sebenarnya. Pola umumnya: **SD atas sekitar ¾ halaman bergambar, SMA sekitar ⅓.**

### 2.3 Kapan gambar wajib, kapan contoh kerja lebih penting

- **Gambar atau lab wajib** (semua jenjang):
  - geometri dan pengukuran (bangun, sudut, luas, volume, Pythagoras, kesebangunan, transformasi, vektor);
  - grafik dan fungsi (garis, parabola, eksponen, trigonometri);
  - data dan statistika (tabel, diagram, histogram, *box plot*);
  - peluang (diagram pohon, ruang sampel);
  - garis bilangan bulat dan pecahan;
  - di SD atas juga **model batang** untuk soal cerita, pecahan, perbandingan, dan persen.

  Alasannya: TKA level 1 secara eksplisit mengukur "memahami informasi dari grafik fungsi, tabel, diagram, infografis, atau bentuk visual lainnya" (`file-178.txt` baris 456–470).
- **Contoh kerja lebih penting daripada gambar** untuk topik prosedural-simbolik: manipulasi aljabar, persamaan, eksponen dan logaritma, barisan dan deret, turunan, serta integral. Gambar di sini hanya perlu bila memberi makna, misalnya model luas untuk (a+b)² atau gradien sebagai kemiringan. Pada pelajar SMA yang sudah menguasai prasyarat, gambar yang berlebihan bisa menjadi beban (*expertise reversal*).
- **Gambar harus skematis dan sesuai skala**, tanpa ilustrasi hiasan. Ini sudah ada di `standar-kartu-lengkap.md`. Buktinya Hegarty & Kozhevnikov 1999 dan Sundararajan & Adesope 2020.
- **Kartu `ingat` sebaiknya tidak dihitung sebagai visual.** Gerbang sekarang memasukkan `ingat` ke himpunan `VISUAL`, padahal isinya bisa teks saja.

---

## 3. Urutan dan latihan

| Prinsip | Temuan | Sumber |
|---|---|---|
| *Worked example effect* | Meta-analisis 55 studi Matematika (SD sampai perguruan tinggi): contoh kerja dibanding pemecahan soal saja, **g = 0,48**. Contoh benar saja memberi efek terbesar. Ajakan menjelaskan diri sendiri (*self-explanation*) yang ditambahkan malah menurunkan efek | Barbieri dkk. 2023, *Educ. Psych. Review* 35:11, https://doi.org/10.1007/s10648-023-09745-1 |
| Asal temuan | Siswa yang mempelajari contoh aljabar lebih cepat dan lebih akurat daripada yang langsung memecahkan soal | Sweller & Cooper 1985, *Cognition and Instruction* 2(1): 59–89, https://doi.org/10.1207/s1532690xci0201_3 |
| Ciri contoh yang baik | ≥2 contoh per jenis soal dengan permukaan berbeda; langkah diberi label sub-tujuan; teks menyatu dengan gambar | Atkinson, Derry, Renkl & Wortham 2000, *RER* 70(2): 181–214, https://doi.org/10.3102/00346543070002181 |
| Pasangan contoh–soal | Selang-seling contoh kerja dengan soal latihan: bukti **sedang** (IES). Pasangan contoh lalu soal lebih efektif dan efisien daripada soal saja atau soal lalu contoh | Pashler dkk. 2007 rek. 2; van Gog, Kester & Paas 2011, *Contemp. Educ. Psych.* 36(3): 212–218, https://doi.org/10.1016/j.cedpsych.2010.10.004 |
| Memudar (*fading*) | Langkah dihilangkan satu per satu, dari belakang, sampai pelajar memecahkan soal sendiri. Cara ini lebih baik daripada pasangan contoh–soal biasa untuk transfer dekat | Renkl, Atkinson, Maier & Staley 2002, *J. Exp. Educ.* 70(4): 293–315, https://doi.org/10.1080/00220970209599510 ; Renkl & Atkinson 2003, *Educ. Psychologist* 38(1): 15–22, https://doi.org/10.1207/S15326985EP3801_3 |
| Contoh salah | Contoh benar ditambah contoh salah membantu konsep aljabar | Booth dkk. 2013, *Learning and Instruction* 25: 24–34, https://doi.org/10.1016/j.learninstruc.2012.11.002 |
| Membandingkan cara | Membandingkan dua cara penyelesaian berdampingan meningkatkan fleksibilitas prosedural | Rittle-Johnson & Star 2007, *J. Educ. Psych.* 99(3): 561–574, https://doi.org/10.1037/0022-0663.99.3.561 |
| Pertanyaan "kenapa" | Ajukan pertanyaan penjelasan mendalam: bukti **kuat** (IES) | Pashler dkk. 2007 rek. 7 |
| *Retrieval practice* | Kuis untuk memunculkan ulang isi: bukti **kuat** (IES). Meta-analisis 217 studi: g ≈ 0,61 | Pashler dkk. 2007 rek. 5b; Adesope dkk. 2017, *RER* 87(3): 659–701, https://doi.org/10.3102/0034654316689306 ; Roediger & Karpicke 2006, https://doi.org/10.1111/j.1467-9280.2006.01693.x |
| Interleaving | RCT 54 kelas, kelas 7: latihan campuran dibanding latihan berkelompok, pada tes sebulan kemudian 61% vs 38%, **d = 0,83** | Rohrer, Dedrick, Hartwig & Cheung 2020, *J. Educ. Psych.* 112(1): 40–52, https://doi.org/10.1037/edu0000367 |
| Jarak (*spacing*) | Ulang isi minimal dua kali dengan selang beberapa minggu atau bulan: bukti sedang. Selang optimal sekitar 10–20% dari lama ingatan yang dituju | Pashler dkk. 2007 rek. 1; Cepeda dkk. 2008, *Psych. Science* 19(11): 1095–1102, https://doi.org/10.1111/j.1467-9280.2008.02209.x ; Dunlosky dkk. 2013, https://doi.org/10.1177/1529100612453266 |
| Berapa latihan | Menambah soal dalam satu sesi (*overlearning*, 9 vs 3 soal) **tidak** menambah ingatan jangka panjang. Menyebar latihan ke beberapa sesi yang menambah | Rohrer & Taylor 2006, *Applied Cognitive Psych.* 20: 1209–1224, https://doi.org/10.1002/acp.1266 |
| Kriteria penguasaan | *Successive relearning*: target 3 jawaban benar di sesi awal, lalu 3 sesi ulang berjarak. Hasilnya efisien dan tahan lama | Rawson & Dunlosky 2011, *J. Exp. Psych.: General* 140(3): 283–302, https://doi.org/10.1037/a0023956 |
| Kerangka beban kognitif | Pemula butuh bimbingan penuh. Bimbingan dikurangi seiring keahlian | Sweller, van Merriënboer & Paas 2019, https://doi.org/10.1007/s10648-019-09465-5 ; Kalyuga dkk. 2001, https://doi.org/10.1037/0022-0663.93.3.579 |

**Turunannya untuk deck:**
1. Urutan dalam deck: contoh kerja (benar) → soal serupa → contoh dipudarkan → latihan mandiri bertingkat → kesalahan khas (setelah contoh benar) → latihan campuran → ringkasan.
2. Minimal 3 soal per sub-kasus di dalam deck. Lebih dari itu sebaiknya masuk antrean ulang berjarak, bukan ditambah di sesi yang sama.
3. Latihan campuran di akhir deck dan soal dari deck sebelumnya.
4. Penjelasan jawaban berupa kalimat alasan. Ajakan menjelaskan diri sendiri tidak diwajibkan, karena buktinya bercampur (Barbieri 2023).

---

## 4. TKA Matematika (047/H/AN/2025 SD/SMP, 045/H/AN/2025 SMA)

### 4.1 Isi kerangka

- **Level kognitif** (sama di SD, SMP, SMA; `file-178.txt` 447–520 dan 828–915; `file-175.txt` 479–560):
  1. **Pengetahuan dan Pemahaman**: menghitung; memahami informasi dari grafik, tabel, diagram, atau infografis; mengelompokkan; mengidentifikasi.
  2. **Aplikasi**: memodelkan soal kontekstual menjadi kalimat matematika; menerapkan rumus atau strategi pada masalah yang "familiar dan rutin"; menginterpretasikan.
  3. **Penalaran**: menganalisis hubungan antarkonsep; memecahkan masalah di "situasi baru atau konteks yang tidak rutin"; mengevaluasi strategi dan solusi; menyimpulkan. SMP dan SMA ditambah **melakukan generalisasi**.
- **Proporsi per level: tidak disebut** di kedua kerangka.
- **Bentuk soal** (`file-178.txt` 294–313; `file-175.txt` 316–335):
  - pilihan ganda sederhana (satu jawaban benar; contoh SD/SMP memakai 4 opsi, SMA 5 opsi);
  - **PGK MCMA**: lebih dari satu jawaban benar;
  - **PGK kategori**: setiap pernyataan dijawab benar/salah atau sesuai/tidak sesuai.

  Ada soal tunggal dan **soal grup** (beberapa soal dengan satu stimulus). Tidak ada isian, menjodohkan, atau uraian.
- **Konteks:**
  - "permasalahan dalam konteks matematika dan … konteks keseharian".
  - SD: lingkup personal, keluarga, lingkungan sekitar.
  - SMP: ditambah "yang bersifat lokal".
  - SMA: "baik lokal maupun global".
  - Contoh soal SMA diberi label konteks "Permasalahan Matematika" atau "Permasalahan Sehari-hari".
- **Elemen:**
  - SD: bilangan, geometri dan pengukuran, data.
  - SMP: bilangan, aljabar, geometri dan pengukuran, data dan peluang. Logika diintegrasikan.
  - SMA: bilangan, aljabar, geometri dan pengukuran, data dan peluang, trigonometri.
  - Tingkat lanjut: aljabar, geometri dan pengukuran, kalkulus.
- **Contoh soal resmi** (24 butir Matematika: SD 6, SMP 6, SMA 6, Lanjut 6):

  | | L1 | L2 | L3 | PG | PGK kategori | PGK MCMA |
  |---|---|---|---|---|---|---|
  | SD | 1 | 4 | 1 | 3 | 2 | 1 |
  | SMP | 0 | 4 | 2 | 3 | 2 | 1 |
  | SMA | 1 | 3 | 2 | 3 | 2 | 1 |
  | Lanjut | 0 | 5 | 1 | 2 | 2 | 2 |
  | Total | 2 (8%) | 16 (67%) | 6 (25%) | 11 (46%) | 8 (33%) | 5 (21%) |

  - Konteks SMA: 3 matematika, 3 sehari-hari. Lanjut: 5 matematika, 1 sehari-hari.
  - Soal SMA no. 4 (penalaran) berbentuk **kecukupan data**: "Pernyataan (1) SAJA cukup …".
  - Soal SD/SMP sehari-hari memakai rupiah, diskon, telur, dan cat dengan tabel. Batangnya 40–60 kata.
  - Ini contoh, bukan cetak biru.
- **Penggabungan dengan AN (Kepmendikdasmen 56/2026, `k56.txt` 1780–1790, 2535–2620):**
  - Soal numerasi AN digabung ke mata uji "Matematika dan Numerasi".
  - Durasi: 75 menit untuk SD dan SMP, 70 menit untuk SMA/SMK.
  - TKA kelas 6 dan 9 = soal pusat + soal daerah. Penulis soal daerah menulis indikator "berdasarkan kompetensi, materi, level kognitif, bentuk soal".
  - Jumlah butir tidak disebut di sana. Media menyebut 30 butir untuk SD/SMP 2026 dan 25 butir Matematika SMA 2026 ([Medcom](https://www.medcom.id/pendidikan/news-pendidikan/yNLZOO2k-lengkap-ini-3-ketentuan-baru-tka-sma-smk-2026-mapel-jumlah-soal-hingga-timeline); [Detik](https://www.detik.com/edu/sekolah/d-8719505/3-perbedaan-tka-2025-dan-2026-butir-soal-matematika-hingga-skor)). Angka ini belum dicek ke POS resmi.

### 4.2 Proporsi resmi terdekat: desain AKM numerasi (Pusmenjar 2020)

Sumber: *Desain Pengembangan Soal AKM 2020*, https://ppkn.unpkediri.ac.id/wp-content/uploads/2021/03/desain-pengembangan-soal-akm.pdf (salinan dokumen Pusmenjar).

| | Kelas 5 | Kelas 8 | Kelas 11 |
|---|---|---|---|
| Pemahaman / Penerapan / Penalaran | 30 / 50 / 20 % | 25 / 50 / 25 % | 20 / 50 / 30 % |
| Konteks personal / sosial-budaya / saintifik | 60 / 30 / 10 % | 40 / 40 / 20 % | 30 / 40 / 30 % |
| Saintifik intra-matematika | 3% | 7% | 10% |
| Bilangan / Geometri-pengukuran / Data / Aljabar | 40 / 25 / 25 / 10 % | 30 / 30 / 30 / 10 % | 20 / 20 / 35 / 25 % |
| Bentuk soal (survei nasional) | PG 20%, PG kompleks 60%, menjodohkan 10%, isian 5%, uraian 5% | | |

Proporsi ini cocok dengan contoh TKA (sekitar ⅔ soal Aplikasi), dan numerasi kini menjadi bagian dari mata uji Matematika TKA. Karena itu proporsi AKM dipakai sebagai acuan target. Untuk deck *belajar*, porsi L1 boleh lebih besar dari porsi ujian, karena latihan awal memang membangun kelancaran. Jadi ambang di bawah adalah batas bawah untuk L2–L3, bukan salinan persis.

### 4.3 Usulan penandaan

Setiap latihan diberi field:
- `level: 1 | 2 | 3` (1 = Pengetahuan dan Pemahaman, 2 = Aplikasi, 3 = Penalaran);
- `proses`, opsional: menghitung, membaca-visual, memodelkan, menerapkan, menginterpretasikan, menganalisis, memecahkan, mengevaluasi, menyimpulkan, generalisasi;
- `konteks: "matematika" | "personal" | "sosial-budaya" | "saintifik"` (tiga yang terakhir = "sehari-hari" dalam istilah TKA);
- `bentuk`, diturunkan dari jenis kartu:
  - `choice` → PG;
  - jenis baru `multi` → PGK MCMA;
  - jenis baru `bs` (tabel pernyataan benar/salah) → PGK kategori;
  - `sort` dengan dua keranjang boleh dianggap PGK kategori;
  - `type`, `line`, `match` → bentuk latihan non-TKA. Bentuk ini tetap dipakai karena AKM memakai isian dan menjodohkan, dan karena bagus untuk latihan.

Untuk soal grup, satu kartu `stimulus` (teks, tabel, atau gambar) dirujuk oleh beberapa latihan lewat `stimulus: id`.

---

## Usulan aturan

Jenjang: **K3–4** = Kelas 3–4 (Fase B), **K5–6** = Kelas 5–6 (Fase C), **SMP** = Kelas 7–9, **SMA** = Kelas 10–12 (tingkat lanjut memakai SMA kecuali disebut lain).
- "Kata" mengikuti gerbang (token yang mengandung huruf).
- "Kartu ajar" = kartu yang bukan latihan.
- "Visual" = `figure`, `lab`, `line`, `jump` (tanpa `ingat`).
- Kolom "Sekarang" = nilai di `tingkat-kartu.ts` hari ini (kelas 3–6 = `sd`).

| # | Aturan | K3–4 | K5–6 | SMP | SMA | Sekarang | Dasar |
|---|---|---|---|---|---|---|---|
| M1 | Kata per kalimat, maksimal | 12 | 15 | 18 | 20 (lanjut 22) | 22 / 28 / 30 | Buku P75: 12–15 (SD), 16–18 (SMP), 17–18 (SMA); Perjenjangan B3/C ≤12; teks TKA 3–7 / 5–9 / 8–12 |
| M2 | Median kata per kalimat dalam satu deck, maksimal | 9 | 10 | 12 | 13 | – | Median buku 8–10 / 11–12 / 11–12 |
| M3 | Kata per kartu ajar, maksimal | 40 | 55 | 70 | 85 | 75 / 90 / 95 | Buku P90 per halaman ÷ 2,5 (§1.4) |
| M4 | Median kata per kartu ajar dalam satu deck, maksimal | 30 | 35 | 45 | 55 | – | Buku median per halaman ÷ 2,5 |
| M5 | Kartu `steps`, `table`, `mistakes`: kata maksimal (sekarang dikecualikan) dan langkah per `steps` | 52; ≤5 langkah | 72; ≤6 | 90; ≤6 | 110; ≤7 | tanpa batas | 1,3 × M3; *segmenting* (Mayer 2024) |
| M6 | Kata batang soal tunggal (`q` + `sentence`), maksimal | 25 | 35 | 45 | 55 | 25 / 35 / 40 | Batang contoh TKA 40–60 kata; Abedi & Lord 2001 |
| M7 | Kartu `stimulus` untuk soal grup: kata maksimal, wajib memuat tabel atau gambar bila berisi data | 60 | 80 | 100 | 120 | belum ada | Soal grup TKA; teks TKA BI 150–300 kata dikurangi untuk Matematika |
| M8 | Penjelasan jawaban: minimal 1 kalimat alasan ≥8 kata; soal level 3 minimal 2 kalimat; tiap kalimat mematuhi M1 | wajib | wajib | wajib | wajib | ≥6 kata | IES rek. 7 (pertanyaan penjelasan, bukti kuat) |
| M9 | Tombol dengar (narasi) di kartu ajar dan soal | wajib | disarankan | opsional | opsional | – | AKSI 2016: 47% kelas 4 "kurang" membaca; Herrlinger 2017 (kelas 4) |
| M10 | Porsi kartu ajar yang visual, minimal | 50% | 40% | 35% | 30% | 15% / 10% / 10% dari semua kartu | Buku: ≈¾ halaman SD atas, ≈⅓ SMA bergambar; IES (visual: bukti kuat untuk kelas 4–8) |
| M11 | Topik visual wajib (geometri, pengukuran, grafik/fungsi, trigonometri, data, peluang, transformasi, vektor, garis bilangan; di SD juga pecahan, perbandingan, persen): setiap kartu konsep punya `figure` atau `lab`, dan ≥30% latihan menyajikan gambar, tabel, atau grafik | wajib | wajib | wajib | wajib | – | TKA L1 "memahami informasi dari grafik … diagram"; Woodward 2012 |
| M12 | Urutan CPA: lab/manipulatif atau model batang muncul sebelum kartu simbol-saja pertama (pecahan, desimal, perkalian/pembagian, luas/volume, perbandingan, soal cerita; di SMP: bentuk aljabar dan persamaan) | wajib, ≥1 lab | wajib, ≥1 lab atau model batang | ≥1 lab untuk aljabar/fungsi/geometri | disarankan | A14 (hanya K1–2) | Fyfe 2014; Leong dkk. 2015; Ng & Lee 2009 |
| M13 | Visual skematis dan sesuai skala; tanpa ilustrasi hiasan (tag `hias: false` diperiksa saat review) | wajib | wajib | wajib | wajib | aturan penulisan | Hegarty & Kozhevnikov 1999; Sundararajan & Adesope 2020 |
| M14 | Contoh kerja (`steps`): minimal per deck, plus ≥1 per sub-kasus; setiap langkah punya alasan (`note`) | 3 | 3 | 3 | 3 (lanjut 2 bila prasyarat diingat lewat `ingat`) | 3 di standar, tidak dicek | Barbieri 2023; Atkinson 2000; Kalyuga 2003 |
| M15 | Pasangan contoh–soal: setiap contoh kerja diikuti soal serupa dalam ≤2 kartu berikutnya | wajib | wajib | wajib | wajib | – | Pashler rek. 2; van Gog dkk. 2011 |
| M16 | Contoh memudar: kartu langkah dengan 1–2 langkah terakhir dikosongkan untuk diisi pembelajar, minimal per deck | 1 | 1 | 2 | 2 | – | Renkl dkk. 2002; Renkl & Atkinson 2003 |
| M17 | Urutan: latihan pertama setelah contoh kerja pertama; latihan sub-kasus X tidak muncul sebelum kartu ajar X; kartu `mistakes` setelah ≥2 contoh kerja benar | wajib | wajib | wajib | wajib | aturan penulisan | Barbieri 2023 (contoh benar dulu); Booth 2013 |
| M18 | Jumlah latihan per deck: minimal max(8, 3 × sub-kasus); maksimal sekitar 16 (sisanya masuk antrean ulang) | 8 | 8 | 8 | 8 (lanjut 6) | 5 (lanjut 4) | Rawson & Dunlosky 2011 (3 benar); Rohrer & Taylor 2006 |
| M19 | Bertingkat: setiap latihan diberi `tingkat` 1–3; dua latihan pertama tingkat 1; latihan tingkat 3 ada di sepertiga akhir; urutan tingkat tidak turun lebih dari sekali | wajib | wajib | wajib | wajib | – | Standar "latihan bertingkat"; Sweller dkk. 2019 |
| M20 | Latihan campuran di akhir deck: minimal sekian soal berurutan dari sub-kasus berbeda, ditambah soal dari deck sebelumnya di jalur yang sama (`dari: slug`) | 2 + 1 | 3 + 1 | 3 + 2 | 3 + 2 | – | Rohrer dkk. 2020; Pashler rek. 1, 5b |
| M21 | Ulang berjarak (aplikasi, bukan isi deck): soal yang dijawab masuk antrean sekitar 1 hari, 1 minggu, dan 1 bulan; dianggap kuasai setelah 3 jawaban benar di sesi berbeda | wajib | wajib | wajib | wajib | – | Cepeda 2008; Rawson & Dunlosky 2011 |
| M22 | Setiap latihan punya `level` (1/2/3) dan `konteks` (matematika / personal / sosial-budaya / saintifik) | wajib | wajib | wajib | wajib | – | Kerangka TKA; Kepmendikdasmen 56/2026 (indikator per level kognitif) |
| M23 | Proporsi level per deck: L1 maksimal, L2 minimal, L3 minimal (dengan jumlah mutlak minimal) | L1 ≤50%, L2 ≥35%, L3 ≥10% (≥1) | L1 ≤40%, L2 ≥40%, L3 ≥15% (≥1) | L1 ≤35%, L2 ≥40%, L3 ≥20% (≥2) | L1 ≤30%, L2 ≥40%, L3 ≥25% (≥2) | – | AKM 30/50/20 (kls 5), 25/50/25 (kls 8), 20/50/30 (kls 11); contoh TKA 8/67/25% |
| M24 | Porsi latihan berkonteks sehari-hari (personal, sosial-budaya, saintifik), minimal | 40% | 40% | 40% | 35% (lanjut 20%) | – | AKM: konteks nyata dominan; contoh TKA SMA 3/6, Lanjut 1/6 |
| M25 | Bentuk TKA per deck: PG minimal 2; PGK MCMA (`multi`) dan PGK kategori (`bs`/`sort`) minimal; opsi PG 4 (SD/SMP) atau 5 (SMA) | PGK opsional | ≥1 PGK | ≥1 MCMA + ≥1 kategori | ≥1 MCMA + ≥1 kategori | belum ada jenis `multi`/`bs` | Kerangka TKA §II; AKM: PG kompleks 60% |
| M26 | Soal grup: minimal 1 kartu `stimulus` dengan ≥2 soal per deck | – | disarankan | wajib | wajib | – | Jenis soal grup TKA |
| M27 | Soal level 3 mencakup ≥2 proses penalaran berbeda per 3 deck berurutan (menganalisis, memecahkan masalah non-rutin, mengevaluasi strategi/jawaban, menyimpulkan dari data, generalisasi, kecukupan data di SMA) | – | disarankan | wajib | wajib | – | Proses berpikir Penalaran TKA; contoh soal SMA no. 4 |
| M28 | Pengecoh PG/MCMA berasal dari kesalahan khas deck (kartu `mistakes`); tepat satu jawaban benar di PG | wajib | wajib | wajib | wajib | hanya cek indeks dan duplikat | Standar "Akurasi" butir 3; Booth 2013 |

**Yang bisa langsung diperiksa gerbang:** M1–M8, M10, M14, M17 (sebagian, lewat urutan jenis kartu), M18, M19, M22–M26, dan M28 (indeks dan duplikat).

**Yang perlu jenis kartu atau field baru:** M7 dan M26 (`stimulus`), M16 (`steps` dengan `kosong`), M20 (`dari`), M22–M24 (`level`, `konteks`), M25 (`multi`, `bs`).

**Yang tetap butuh review manusia:** M11–M13 (apakah gambarnya skematis dan benar) dan M27.

**Catatan keandalan:**
- M3–M5 adalah konversi luas halaman ke layar, jadi perkiraan, bukan standar resmi. Ambang ini perlu dicek ulang dengan uji pengguna Kelas 4, 8, dan 11.
- Proporsi M23–M24 diambil dari desain AKM 2020, bukan dari kerangka TKA, karena kerangka TKA tidak menyebut proporsi. Perbarui ambang ini kalau Pusmendik menerbitkan kisi-kisi berproporsi.
- Data Rapor Pendidikan rilis Juni 2026 belum jelas tahun AN-nya.
