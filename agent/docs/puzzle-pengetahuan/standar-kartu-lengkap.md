# Standar kartu lengkap

Status: disusun 2026-11-02 setelah pemilik menilai kartu kanonik masih tipis. Berlaku untuk semua deck kanonik.

## Ukuran keberhasilan

Satu deck menjelaskan satu bab sampai tuntas. Orang yang belum pernah belajar bab itu, setelah melihat semua kartunya, paham konsepnya, bisa memakainya pada contoh, dan tahu kapan dipakai dalam kehidupan nyata. Dia tidak perlu sumber lain untuk memahami bab itu.

**Untuk siapa (2026-11-03):** semua kalangan, yaitu orang awam, orang yang pernah belajar lalu lupa, siswa, guru, dan akademisi. Bahasanya harus bisa diikuti orang awam: kata sehari-hari dulu, setiap istilah diberi arti, dan setiap langkah diberi alasan. Isinya tetap utuh. Kedalaman, kasus khusus, istilah resmi, dan alasan keilmuannya nggak dikurangi demi kemudahan. Yang dibuat mudah adalah jalan masuknya, bukan ilmunya.

## Hasil audit (502 deck, 2026-11-02)

- Rata-rata hanya 102 kata penjelasan per deck, setara satu paragraf pendek.
- 110 deck di bawah 60 kata. 19 deck Language Functions rata-rata 30 kata: satu tabel, lalu kuis.
- 183 deck tanpa bagian kesalahan umum. 165 deck tanpa contoh kerja.
- 1.398 dari 2.458 penjelasan jawaban hanya lima kata atau kurang, sering hanya hitungan.
- Geometri, grafik, dan diagram belum punya gambar.
- Deck hasil generator memuat isi yang tidak layak, misalnya dikte "Tea — 5" yang diambil dari baris menu.
- Banyak deck langsung masuk rumus atau tabel tanpa menjelaskan kenapa bab itu ada dan apa artinya.

## Isi wajib tiap deck

| Bagian | Isi |
|---|---|
| Pintu masuk | Masalah nyata yang dipecahkan bab ini, dari kehidupan pembelajar Indonesia, dan yang akan bisa dilakukan setelahnya |
| Bekal | Pengetahuan sebelumnya yang dibutuhkan, diingatkan singkat, bukan diasumsikan |
| Konsep | Dijelaskan dengan bahasa sehari-hari dulu, baru istilah resminya. Setiap istilah diberi arti |
| Alasan | Kenapa aturannya begitu, bukan hanya aturannya |
| Semua sub-bagian | Setiap kasus dalam bab punya kartu sendiri, termasuk kasus khusus |
| Contoh kerja | Paling sedikit tiga: mudah, sedang, dan konteks nyata, langkah demi langkah dengan alasan tiap langkah |
| Gambar | Wajib untuk geometri, grafik, data, dan garis waktu |
| Penerapan | Kapan dipakai: sehari-hari, pekerjaan, sekolah, ujian |
| Kesalahan khas | Kesalahan yang memang dibuat pembelajar Indonesia dan penyebabnya, termasuk pengaruh bahasa Indonesia |
| Latihan bertingkat | Dari mudah ke sulit, setelah bagian yang diujikan diajarkan |
| Penjelasan jawaban | Menjelaskan cara berpikir, bukan hanya hasil. Paling sedikit satu kalimat utuh |
| Rangkuman | Poin yang benar-benar dibutuhkan |

## Kanonik dan jalur (ADR-0026, 2026-11-03)

- **Deck kanonik** ditulis menurut standar mutu materi dan standar keilmuannya, untuk pembelajar mana pun. Penulis tidak mengandaikan usia atau kelas pembacanya.
- **Deck jalur** (`kind: "kemasan"`, `path`) menyesuaikan unit yang sama untuk pembaca atau ujian tertentu. Contohnya prabaca Kelas 1–2, kalimat lebih pendek untuk SD, kartu jembatan, atau soal bergaya TKA.

| Deck | Tingkat di gerbang | Batas |
|---|---|---|
| Kanonik Matematika | `mtk` | Kalimat ≤22 kata. Kartu ajar ≤90 kata, kartu padat ≤110. Kartu ajar bergambar ≥25%. Minimal 3 contoh kerja dan 8 latihan bertanda level dan konteks. Level 1 ≤40%, level 2 ≥40%, level 3 ≥15%. Konteks sehari-hari ≥30%. |
| Kanonik Inggris | level CEFR unit | Panjang kalimat contoh per level (E4). Jenis latihan bebas; batas E12 hanya untuk deck jalur. Penjelasan Indonesia per kartu: ≤60 kata sampai A1, ≤80 kata di A2, ≤100 kata mulai B1. |
| Kemasan Kurikulum Indonesia Matematika | kelas unit di jalur: `k1`, `k2`, `k34`, `k56`, `smp`, `sma` | Kelas 1–2 prabaca (A1–A19). Kelas 3–SMA mengikuti M1–M24 per jenjang. |
| Kemasan Kurikulum Indonesia Inggris | CEFR, ditambah aturan Kelas 3–4 | Penjelasan Indonesia pendek. Kelas 3 prabaca (E6–E8). |
| Kemasan ujian (TKA, UTBK) | `tka` | PG kompleks MCMA dan benar/salah, soal kelompok, campuran level SMA (M25, M26). |

Semua deck tetap memerlukan isi wajib, akurasi, gambar sesuai skala, dan bahasa yang bukan AI slop.

## Bahasa: bukan AI slop

Tulis seperti guru les Indonesia yang sedang menjelaskan di depan satu murid.

- Sapaan "kamu". Penjelasan memakai "nggak", kalimat aturan yang dikutip boleh "tidak". Satu kartu tidak mencampur keduanya.
- Dilarang: pembuka kosong ("Tahukah kamu", "Mari kita", "Pada kartu ini kita akan"), pujian kosong, "sangat penting", "dunia X", "kunci sukses", pola "bukan hanya X, tetapi juga Y", dan penutup yang mengulang isi.
- Dilarang kalimat umum yang bisa ditempel di bab apa pun. Setiap kalimat harus memuat isi bab itu.
- Contoh harus masuk akal dan terasa Indonesia: warung, angkot, rupiah, sekolah, Kediri, bukan nama dan situasi acak.
- Satu bab tidak memakai kerangka yang sama persis dengan bab lain kalau materinya tidak menuntut.
- Tanpa tanda pisah panjang di kalimat penjelasan. Istilah tata bahasa tetap bahasa Inggris dan selalu diberi arti.

## Animasi, interaksi, dan alur (2026-11-03)

Semua kartu deck berukuran 9:16. Keluaran utamanya video, dan ruang tambahannya dipakai untuk gambar, animasi, dan interaksi.

- **Kartu lab** (`t: "lab"`): model yang dihitung kode dari nilai awalnya, jadi gambar dan angka nggak bisa saling bertentangan. Setiap lab memutar peragaan berlangkah dengan keterangan sampai pengguna menyentuh kontrol. Setelah itu kendali di tangan pengguna, dan ada tombol untuk memutar peragaan lagi. Di video, peragaan berjalan sendiri.
- **Kapan lab dipakai:** saat gerakan atau perubahan nilai adalah inti pemahamannya, misalnya bukti, pengaruh parameter, atau proses langkah demi langkah. Bukan hiasan. Setiap bab punya paling sedikit satu gambar atau lab yang menjadi pusat penjelasan.
- **Kartu ingat** (`t: "ingat"`): memanggil kartu ajar dari deck prasyarat berdasarkan judulnya, lalu menjelaskan kaitannya dengan bab ini. Dipakai menggantikan kartu "Bekal" yang hanya berupa teks, setiap kali kartu prasyaratnya ada. Di web, kartunya bisa dibuka utuh tanpa meninggalkan deck.
- **Gambar sesuai skala:** panjang dan sudut di gambar harus sesuai angka yang tertulis. Segitiga 3-4-5 digambar 3 : 4 : 5.
- **Alur:** masalah nyata, lalu ingat bekal, lalu konsep dengan gambar atau lab, lalu alasan atau bukti, lalu contoh kerja, lalu latihan bertingkat, lalu kesalahan khas, lalu rangkuman.

## Deck jalur Kelas 1–2: prabaca (2026-11-03)

Bagian ini berlaku untuk deck kemasan jalur Kurikulum Indonesia Kelas 1–2, bukan untuk deck kanonik. Anak Kelas 1 dianggap belum bisa membaca. Anak Kelas 2 sudah bisa mengeja, tetapi belum lancar dan belum paham dari teks saja. Bukti dan aturan lengkapnya (A1–A19) ada di `riset-kelas-awal.md`.

- **Deck ditandai `prabaca: true`.** Kartu yang tampil dibacakan otomatis, dan penjelasan jawaban juga dibacakan. Soal dibacakan ulang setelah 8 detik tanpa sentuhan. Jawaban angka memakai papan angka besar. Teks penjelasan berukuran sekitar 24 px.
- **Teks untuk anak.** Kelas 1 paling banyak 5 kata per kalimat, 3 kalimat, dan 15 kata per kartu. Kelas 2 paling banyak 7 kata per kalimat, 5 kalimat, dan 30 kata per kartu. Angka dan tanda hitung tidak dihitung sebagai kata.
- **Penjelasan untuk orang dewasa** ditulis di field `dampingi`. Isinya muncul di tombol "Pendamping" dan tidak dihitung sebagai bacaan anak. Isinya sama lengkapnya dengan penjelasan tingkat lain: alasan, cara memeragakan dengan benda di rumah, dan kesalahan khas.
- **Urutan:** benda atau alat peraga, lalu gambar, lalu simbol. Kartu simbol untuk satu konsep tidak muncul sebelum kartu benda dan gambarnya.
- **Gambar dan praktik dulu.** Minimal 25% kartu bergambar atau berupa lab, dan minimal 65% kartu bergambar atau berupa latihan. Kartu teks saja paling banyak 3 per deck.
- **Latihan.** Hanya ketuk: pilihan bergambar, garis bilangan, pasangkan, dan papan angka. Tidak ada latihan menyusun kalimat, memperbaiki, atau menandai. Benda dalam pilihan jawaban dikelompokkan per tiga, misalnya "🍎🍎🍎 🍎🍎", supaya bisa dilihat tanpa menghitung satu-satu.
- **Bilangan.** Operasi dengan benda konkret sampai 20.
- **Alat peraga yang tersedia** (`lab-awal.tsx`): `hitung`, `bingkai`, `bandingkan`, `jam`, `potong`, dan `puluhan`.

## Batas dari riset (2026-11-03)

Batas per tingkat berasal dari riset, bukan perkiraan. Batas per jenjang sekolah berlaku untuk deck jalur. Deck kanonik memakai baris `mtk` dan CEFR di tabel atas.

- **Kelas 3–SMA (`riset-sd-sma.md`, M1–M28).**
  - Batas kalimat dan kata per kartu diturunkan dari buku siswa Kurikulum Merdeka dan Pedoman Perjenjangan Buku.
  - Porsi kartu ajar bergambar: 50% di Kelas 3–4, 40% di Kelas 5–6, 35% di SMP, dan 30% di SMA. Kartu ingat tidak dihitung.
  - Minimal 3 contoh kerja, dan latihan pertama diletakkan sesudah contoh kerja pertama.
  - Minimal 8 latihan, masing-masing bertanda `level` dan `konteks`. Campuran level mengikuti desain AKM numerasi.
  - SMP dan SMA wajib punya soal TKA `multi` dan `bs`, serta soal kelompok (`grup`).
- **Bahasa Inggris (`riset-inggris.md`, E1–E21).**
  - Panjang kalimat contoh dan jenis latihan mengikuti level CEFR.
  - Penjelasan Indonesia pendek untuk Kelas 3–4, dan deck Kelas 3 ditandai `prabaca`.
  - Soal dengar wajib memakai rekaman.
  - Kesalahan khas pembelajar Indonesia wajib ada beserta sebabnya.
  - Pre-A1 dan A1 memakai ubin huruf.

## Gerbang otomatis

`bun scripts/periksa-kartu.ts [awalan-slug ...]` di `titian-web` memeriksa:

- isi wajib;
- beban baca per tingkat, dengan Kelas 1 dan 2 dibedakan;
- porsi gambar dan praktik;
- jenis latihan;
- kartu ingat;
- hitungan;
- frasa terlarang;
- campuran "nggak" dan "tidak" dalam satu kartu.

Tanpa argumen, gerbang memeriksa semua deck yang sudah memenuhi standar. Deck baru didaftarkan di `src/content/kartu/mtk/baru.ts`. Deck baru boleh dikirim hanya jika gerbang lolos, tidak ada kartu yang meluber (`fit.ts`), dan sudah diuji sebagai pengguna.

## Uji sebagai pengguna

Setiap deck yang selesai dijalani kartu demi kartu di mode web, 9:16, seperti pemula:

1. Baca setiap kartu dan catat bagian yang membingungkan, terlalu padat, atau kosong.
2. Jalankan setiap lab: tonton peragaannya, lalu geser kontrolnya dan baca angka yang tampil.
3. Buka setiap kartu ingat.
4. Kerjakan latihan, termasuk jawaban salah, dan baca penjelasannya.
5. Perbaiki temuannya, lalu ulangi pemeriksaan otomatis.

## Akurasi

Salah materi lebih buruk daripada tipis. Setiap deck melewati:

1. **Hitungan:** semua persamaan bilangan dihitung ulang otomatis (`check-math-answers.ts`).
2. **Aljabar:** identitas dan jawaban yang memuat variabel diuji dengan mengganti variabel memakai beberapa bilangan.
3. **Pilihan ganda:** tepat satu jawaban benar, pengecoh benar-benar salah, dan penjelasan menyebut alasan jawaban itu.
4. **Bahasa Inggris:** setiap contoh diperiksa tata bahasa dan kewajarannya, memakai British English seperti Kampung Bahasa. Kalimat salah hanya boleh muncul sebagai contoh salah.
5. **Fakta dan acuan:** istilah Indonesia mengikuti buku sekolah, cakupan mengikuti CP 046/2025, kisi-kisi TKA, dan SNPMB. Fakta dunia nyata yang bisa berubah tidak ditulis sebagai angka pasti.
6. **Pembacaan ulang:** setiap deck dibaca utuh dari kartu pertama sampai terakhir, sebagai orang yang belum tahu babnya.

## Kemajuan

Disetujui pemilik pada 2026-11-02 setelah meninjau enam deck contoh.

| Bagian | Deck | Status |
|---|---|---|
| Contoh standar | 6 | Selesai |
| Language Functions | 19 | Selesai, 284–497 kata per deck |
| Kosakata tema | 30 | Selesai, 230–428 kata per deck |
| Kosakata cara kerja kata | 6 | Diperkaya, 196–277 kata per deck |
| Matematika: bilangan cacah, faktor, pecahan | 22 | Selesai, dengan gambar |
| Matematika: bilangan bulat | 9 | Selesai, 343–402 kata per deck, garis bilangan interaktif |
| Matematika: desimal, persen, perbandingan | 7 | Selesai, 421–569 kata per deck, dengan gambar |
| Matematika: bilangan real, pangkat, akar | 6 | Selesai, 434–589 kata per deck |
| Matematika: pola dan bentuk aljabar | 9 | Selesai, 313–534 kata per deck, ubin aljabar dan model luas |
| Matematika: persamaan dan pertidaksamaan linear | 7 | Selesai, 434–537 kata per deck, grafik bidang koordinat |
| Matematika: transformasi dan koordinat | 7 | Selesai, 419–528 kata per deck, peta berpetak dan bidang koordinat |
| Matematika: trigonometri | 7 | Selesai, 468–561 kata per deck, lingkaran satuan dan grafik gelombang |
| Matematika: persamaan dan fungsi kuadrat, polinomial | 10 | Selesai, 402–546 kata per deck, parabola dan kurva kubik |
| Matematika: relasi dan fungsi | 9 | Selesai, 385–513 kata per deck, diagram panah, asimtot, invers |
| Matematika sekolah lainnya | sekitar 100 | Belum |
| Matematika: unit baru dari pemecahan kanonik (ADR-0026) | 40 | 13 selesai (SD; 3 di antaranya prabaca Kelas 1–2), 27 belum. Lihat `produksi-massal-kartu.md` |
| Bahasa Inggris: unit baru dari buku siswa (ADR-0026) | 34 | Belum; lima deck lama perlu dipecah |
| Grammar, Reading, Listening, Writing, Sounds | sekitar 170 | Belum |
| Tingkat kuliah | 70 | Belum |

Kosakata A2 ke atas sebagian masih di bawah batas angka standar, karena isinya daftar kata dan pemakaian, bukan penjelasan panjang. Penilaiannya memakai isi wajib, bukan hanya jumlah kata.

## Cara kerja

Deck yang ditulis ulang disimpan di `titian-web/src/content/kartu/lengkap/` dan menggantikan versi lama menurut slug. Setelah semua selesai, versi lama dan generatornya dihapus.
