# ADR-0028: Misi bertema di atas kartu kanonik

Status: Berjalan di dev untuk seluruh Level 4 jalur Berurutan: 25 deck, 83 misi (2026-11-19), keputusan pemilik. Melanjutkan ADR-0024, ADR-0025, dan ADR-0026.

## Ringkasan

Bentuk utama e-learning Titian Asa adalah **misi** seperti puzzle klasik. Kartu kanonik menjadi materi di dalam misi dan pendalaman yang tersambung dari tiap kepingan. Satu deck tidak dipelajari sekaligus, melainkan dipecah menjadi beberapa **tema**, dan setiap tema adalah satu misi.

## Keputusan

| Lapis | Isi |
|---|---|
| Unit kanonik | Satu deck kartu, satu bab di peta misi |
| Tema | Sebagian kartu dari deck itu, dengan latihan dan uji sendiri. Satu tema = satu misi |
| Kepingan | Bagian terkecil yang diberi label, misalnya bilangan negatif atau tanda tambah. Menyala di jaringan pengetahuan |
| Kemampuan | Yang bisa dilakukan dari gabungan kepingan, misalnya menghitung untung dan rugi |

Alur satu misi:

> **Misi → Materi (kartu tema) → Latihan → Uji akhir → Kepingan menyala → Ingat di hari lain**

- Materi wajib sebelum latihan. Siswa yang merasa sudah paham boleh memilih "Uji dulu". Kalau semua tebakannya benar, ia boleh langsung ke uji akhir. Kalau ada yang salah, ia harus mempelajari kartunya dulu.
- Latihan dan penilaian memakai mesin yang sama dengan puzzle klasik: bantuan memudar, uji tanpa bantuan dengan yakin/ragu, tiga nyawa, bintang, dan ulangan di hari lain.
- Tiap kepingan dan konsep punya tautan ke deck-nya untuk penjelasan lengkap.
- Satu deck dianggap lulus saat semua temanya selesai, sehingga unitnya ikut menyala di semua jalur belajar (ADR-0026).

## Pilot: Bilangan Bulat

- 8 deck kanonik dipecah menjadi 8 bab dan 23 misi. Semua kartu materi di 8 deck itu masuk tepat satu tema.
- Jenis latihan baru: **melompat di garis bilangan**. Format mendengar diganti format ini kalau kalimatnya berupa satu lompatan yang muat di layar.
- Kalimat matematika dibaca sebagai kepingan menurut bentuknya: −3 dan −8 sama-sama "Negative integer · Bilangan negatif".

## Aljabar Kelas 7

- 4 deck kanonik dipecah menjadi 4 bab dan 12 misi, dengan aturan cakupan kartu yang sama.
- Suku seperti `3x` dan `x²` dibaca sebagai kepingan **Variabel** dan **Suku aljabar**.
- Generator memeriksa setiap kesamaan aljabar pada beberapa nilai huruf. Tema pemodelan cerita ditandai `model`, karena kalimatnya hanya benar untuk situasinya.

## Level dan produksi

- Misi memakai level jalur Berurutan (1 sampai 14), karena satu misi dipakai di semua jalur. Bilangan Bulat dan Aljabar ada di Level 4.
- Beranda hanya mengambil misi dari level yang dipakai kelas yang sedang dibuka. Peta `deck → level` dibuat generator di `src/content/kartu/misi-level.ts`.
- Kepingan Matematika (bilangan, tanda, variabel) ditandai `lintas_level`, jadi muncul di jaringan setiap level.
- Tema ditulis per file di `titian-web/scripts/misi-level/` dan didaftarkan di `index.ts`. Satu generator memeriksa semuanya.
- Materi yang tidak bisa ditulis sebagai kalimat hitung (pecahan, desimal, persen, sifat bangun, membaca diagram) dilatih dengan **latihan pilihan** (`pilih`). Misi yang hanya berisi pilihan tidak punya kalimat target.
- Setiap bentuk latihan memeriksa kalimatnya sendiri. Kalau tidak cocok, latihan kembali ke susun blok.

## Beranda belajar

Beranda mengikuti jalur yang dipilih siswa, jadi satu tampilan berlaku untuk Kurikulum Indonesia, Belajar Berurutan, TKA, UTBK, dan CEFR.

- Navigasi kelas atau level ada di bagian atas, dengan tanda "Kamu di sini". Siswa bisa melihat kelas lain kapan saja.
- Isi tiap kelas adalah **bab besar** (konsep kanonik) yang bisa dibuka-tutup. Di dalamnya ada yang dipelajari, misi, misi yang sudah selesai, dan kemampuan yang didapat.
- Topik yang sudah punya misi tampil sebagai misi di jalur mana pun yang memuatnya. Topik lain sementara ditandai "Belajar lewat kartu" sampai misinya dibuat.

## Bentuk latihan mengikuti jenis soal

| Jenis kalimat | Bentuk latihan |
|---|---|
| Membandingkan dua bilangan | Pilih tanda, dengan garis bilangan |
| Mengurutkan | Ketuk bilangan sesuai urutan |
| Nilai mutlak dan jarak | Hitung langkah di garis bilangan |
| Penjumlahan beda tanda | Pasangkan keping + dan − |
| Penjumlahan lain | Melompat di garis bilangan |
| Perkalian, pembagian, pangkat | Tentukan tanda dulu, baru angka |
| Operasi campuran | Ketuk operasi yang dikerjakan lebih dulu |
| Penjumlahan bentuk aljabar | Ketuk suku sejenis, lalu jumlahkan koefisiennya |
| Bentuk aljabar lain | Lengkapi koefisien atau konstanta di ruas kanan |
| Pecahan, desimal, persen, geometri, data | Pilih jawabannya |
| Semua jenis | Lengkapi bilangan, susun blok, ketik sendiri |

## Cara menambah bab baru

1. Tulis tema di file data seperti `titian-web/scripts/misi-aljabar.ts`, lalu daftarkan di `titian-web/scripts/misi-bilangan-bulat.ts`. Generator berhenti kalau ada hitungan salah, kartu yang tidak ada, atau kartu materi yang belum masuk tema.
2. Jalankan generatornya, lalu impor dengan `cmd/tools/import_puzzles` memakai `-subject matematika`.
3. Daftarkan deck-nya di `MISI_DECKS` (`components/puzzle/belajar/lib.ts`).

## Catatan temuan

Semua temuan audit, penyebabnya, dan pengamannya ada di `agent/docs/puzzle-pengetahuan/temuan-misi.md`. Brief penulis dan peninjau merujuk ke sana.

## Konsekuensi dan utang

- Baru Level 4 (25 dari 314 topik Berurutan) yang punya misi. Topik lain masih dipelajari lewat kartu.
- Level 1 (Kelas 1 sampai 2, belum lancar membaca) menunggu fitur bacakan soal dalam bahasa Indonesia.
- Batas rantai prasyarat 12 (ADR-0024 §7) berlaku untuk seluruh graf. Di Level 4 rantai terdalam sudah 10, jadi level atas butuh batas per level atau prasyarat antarlevel yang diwakili urutan level.
- Bentuk latihan yang masih kurang menurut penulis misi: titik di bidang koordinat, bilangan pecahan dan desimal dalam kalimat, hitung bersusun, membaca grafik, durasi waktu, dan memilah dua kelompok.
- Hasil latihan garis bilangan diputuskan di browser, lalu dikirim sebagai jawaban biasa ke server.
- Status misi (`masteries`) dan status unit (`card_progress`) masih dua catatan. Jembatannya hanya saat semua tema satu deck selesai.
- Bahasa Inggris kanonik belum dipindahkan ke pola ini. Misi Kampung Bahasa lama ada di `/puzzle/klasik`.
