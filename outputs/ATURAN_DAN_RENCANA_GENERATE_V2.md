# Aturan Generate dan Rencana v2

Status: **usulan, belum ada generate yang dijalankan.** Dibuat 2026-09-21. Menggantikan `RENCANA_URUTAN_GENERATE_V1.md` di bagian aturan, biaya, dan operasi. Urutan gelombang dan antrean bab (`kurikulum/antrean_generate_v1.csv`) tetap dipakai.

Kurs: **Rp 18.000 per dolar.** Harga Vertex Gemini $0,75 masuk dan $3,75 keluar per 1 juta token.

## 1. Aturan: satu bab dianggap selesai jika

Satu perintah generate untuk satu bab selalu menghasilkan **dua hal sekaligus: materi dan bank 50 soal.** Bab yang hanya punya salah satunya tidak dihitung selesai dan tidak dibuka di jalur belajar.

### 1.1 Materi

Materi mengikuti topik, bab, dan jenjang. Profil di bawah dikirim ke prompt sebagai bagian aturan tetap, dan diperiksa lagi sesudahnya tanpa token (bagian 1.3).

| Fase (Kelas) | Kalimat rata-rata / maks (kata) | Isi per bagian | Konteks dan cara mengajar |
|---|---|---|---|
| A (1–2) | 6 / 10 | ≤120 kata, 3–4 bagian, satu gagasan per kalimat | Rumah, sekolah, mainan, makanan, hewan. Konkret dulu (benda, gambar, permainan), simbol sesudahnya. Bilangan ≤100. Tanpa istilah abstrak. |
| B (3–4) | 10 / 16 | ≤180 kata, 4 bagian | Pasar, keluarga, lingkungan sekitar. Maksimal 3 istilah baru per bagian, masing-masing dengan definisi satu kalimat. |
| C (5–6) | 14 / 22 | ≤250 kata, 4–5 bagian | Kehidupan nyata anak. Abstraksi awal boleh muncul setelah contoh konkret. |
| D (7–9) | 18 / 28 | ≤300 kata, 5 bagian | Konteks remaja (olahraga, gawai, uang saku). Pemodelan dan alasan "mengapa". |
| E–F (10–12) | 22 / 34 | ≤400 kata, 5 bagian | Konteks akademik, kerja, gaya soal TKA dan UTBK. Notasi dan istilah baku. |

Berlaku untuk semua Fase: contoh dikerjakan langkah demi langkah, satu blok "kesalahan umum" (diambil dari judul bab Kesalahan Umum topik itu), dan ringkasan akhir. Bahasa pengantar Indonesia. Untuk Bahasa Inggris, contoh berbahasa Inggris mengikuti CEFR bab (A1 ≤6 kata per kalimat, A2 ≤10, B1 ≤15) dan diberi terjemahan atau penjelasan Indonesia.

Angka di tabel adalah usulan awal. Batasnya harus dikalibrasi pada gelombang 0 dengan membaca hasilnya, bukan diterima begitu saja.

### 1.2 Bank 50 soal

Sebagian besar sudah diatur di kode (`content_factory/blueprint.rs`, `tagging.rs`). Yang saya tambahkan ditandai (baru).

| Sumbu taksonomi di aplikasi | Aturan |
|---|---|
| Jumlah | Tepat 50, stem unik, kunci valid, pembahasan ada. |
| Kesulitan | 15 mudah / 25 sedang / 10 sulit. |
| Bloom | C1 5 / C2 8 / C3 14 / C4 12 / C5 6 / C6 2 (minimum), semua enam level terwakili. Tingkat berpikir LOTS, MOTS, HOTS diturunkan dari Bloom. |
| Fungsi (untuk jalur belajar) | 4 diagnostik, 22 latihan terarah, 8 latihan mandiri, 10 checkpoint akhir, 4 remedial, 2 pengayaan. Itu yang memasok Pemanasan 4, Latihan 1 (6), Latihan 2 (8), Transfer (8), dan Ujian akhir (12) tanpa soal berulang. |
| Dimensi pengetahuan | (baru) Faktual, Konseptual, Prosedural, Metakognitif semuanya terwakili, minimal 3 soal per dimensi (Metakognitif minimal 2). |
| Miskonsepsi | 4 soal remedial, masing-masing menargetkan satu miskonsepsi. (baru) Miskonsepsinya diambil dari bab "Kesalahan Umum" topik itu, jadi 966 judul yang baru ditulis benar-benar dipakai. |
| Tipe soal | (baru) Hanya pilihan ganda, benar/salah, dan isian singkat, karena hanya tiga itu yang bisa dinilai server di sesi jalur belajar. Tipe "pilihan ganda banyak jawaban" **dikeluarkan** dari bank untuk jalur, karena kuncinya tidak lolos penilai (`canon_path::gradable`) dan soalnya tidak akan pernah muncul. Campuran bawaan "konsep" saat ini memakainya 25%, jadi ia perlu diganti. |
| Komposisi tipe per mapel | (baru, usulan) Hitungan (Matematika, Fisika, Kimia, Akuntansi): 50% pilihan ganda, 20% benar/salah, 30% isian. Konsep (Biologi, Sejarah, Sosiologi, Geografi, Ekonomi, IPA, IPAS, IPS): 60 / 25 / 15. Bahasa Indonesia dan Inggris: 55 / 15 / 30 (isian berupa bentuk kata yang benar). Penalaran: 75 / 15 / 10. |
| Jenjang | (baru) Fase A–B: stem ≤12 kata, isian hanya satu kata atau angka dan tidak lebih dari 10%, pilihan 3–4. Bobot Bloom bergeser ke C1–C3 tetapi C4–C6 tetap ada. Kalibrasi kesulitan relatif terhadap jenjang, bukan mutlak. |

Catatan: standar di kode memakai tabel Bloom yang sama untuk semua jenjang. Itu berarti bank Kelas 1 saat ini akan dapat 8 soal C5 dan C6. Bobot per Fase di baris terakhir perlu diputuskan sebelum gelombang 1.

### 1.3 Gerbang mutu (tanpa token dulu)

Urutan pemeriksaan sebelum bab dianggap selesai:

1. **Struktur:** 50 soal, distribusi Bloom, kesulitan, fungsi, dimensi, tipe sesuai bagian 1.2. Sudah ada di `tagging::audit`.
2. **Keterbacaan materi (baru):** rata-rata dan maksimum kata per kalimat, panjang per bagian, jumlah istilah baru, sesuai tabel 1.1. Murni hitungan.
3. **Kesesuaian konteks (baru):** daftar kata dan konteks yang tidak pantas per Fase (misalnya pajak, kartu kredit, dan istilah teknis pada Fase A–B). Murni pencocokan.
4. **Hakim `agent_qa`:** pada sampel 1 dari 5 bab, dan wajib pada 3 bab pertama tiap topik dan tiap mapel baru. Ambang rata-rata ≥4,2, dimensi "kesesuaian jenjang" ≥4,5 untuk Fase A–C. Pada gelombang 0 semua bab dinilai.
5. Yang gagal masuk antrean tinjauan admin dengan alasannya. Yang lolos berstatus `siap`.

Bab yang sudah ada (324 Bahasa Inggris dan 14 Matematika yang punya bank ≥50 dan materi) harus diperiksa ulang dengan gerbang yang sama sebelum dianggap selesai.

## 2. Biaya Matematika dan Bahasa Inggris (materi + 50 soal)

Kondisi sekarang (jalur Kurikulum Indonesia):

| | Bab | Materi belum ada | Bank belum ada | Bank kurang dari 50 | Sudah lengkap |
|---|---:|---:|---:|---:|---:|
| Bahasa Inggris | 750 | 388 | 418 | 8 | 324 |
| Matematika | 1.107 | 1.072 | 1.079 | 14 | 14 |

Basis token: hasil ukur benchmark 20 bab (materi Inggris 6,1 ribu, Matematika 7,4 ribu; bank 50 soal Inggris 36,4 ribu, Matematika 40,2 ribu), ditambah hakim pada 20% bab dan 15% untuk putaran ulang.

| | Token | Dolar | Rupiah (Rp 18.000) | Rentang |
|---|---:|---:|---:|---|
| Bahasa Inggris (426 bab perlu diisi) | ±21 juta | ±$41 | **±Rp 0,74 juta** | Rp 0,57–0,96 juta |
| Matematika (1.093 bab perlu diisi) | ±61 juta | ±$119 | **±Rp 2,1 juta** | Rp 1,6–2,8 juta |
| **Keduanya** | ±82 juta | **±$159** | **±Rp 2,9 juta** | **Rp 2,2–3,8 juta** |

Waktu: Matematika ±29 jam, Bahasa Inggris ±9 jam, dengan 3 worker (waktu benchmark: materi + bank 50 ≈ 284 dan 219 detik per bab). Dengan 6 worker separuhnya jika batas laju Vertex mengizinkan (belum diuji).

Rentang mengikuti pembagian token masuk:keluar yang belum terukur (saya pakai 60:40; rentang 75:25 sampai 40:60). Jika token keluar lebih besar, biaya naik.

Seluruh 15 mapel (materi + bank 50 untuk 8.673 bab): ±$880, **±Rp 15,8 juta** (rentang Rp 12,2–20,7 juta). Per gelombang: Matematika Rp 2,1 juta, gelombang 2 Rp 2,9 juta, gelombang 3 Rp 6,0 juta, gelombang 4 Rp 4,7 juta.

Perbandingan dengan v1: v1 hanya menghitung bank dan memakai kurs Rp 16.500, sehingga totalnya Rp 4,8–12 juta. Angka v2 lebih besar karena materi wajib ikut dan kurs naik.

## 3. Generate langsung di aplikasi, dan pemantauan di dashboard

### 3.1 Sudah ada

- Antrean Postgres `jobs` dan `titian-worker` (jalan terpisah dari API), dengan claim aman, coba ulang, dan pemulihan job yang macet.
- Kerangka `generation_runs` dan `generation_tasks` dengan aksi jeda, lanjut, batal, dan ulang yang gagal, batas token per run, dan pencatatan token di `ai_tasks`.
- Halaman admin **Pabrik Konten** (Cakupan, Proses, Tinjau, Standar, Contoh Emas).

Halaman itu berorientasi tahap dan run, bukan bab dan gelombang, dan tidak menampilkan rupiah, sisa anggaran, atau kesehatan worker.

### 3.2 Yang dibersihkan hari ini

Sesuai izinmu, daftar tunggu lama sudah dibersihkan (dengan cadangan `db_titian_bun_20260921_sebelum_bersih_antrean.dump`):

| | Sebelum | Sesudah |
|---|---|---|
| Job `content_generation` menunggu, berjalan, gagal | 737 + 6 + 5 | dihapus (748 baris) |
| Tugas generasi antre atau sedang jalan | 600 + 137 | dibatalkan (737) |
| Run dijeda | 7 | dibatalkan |

Yang tetap: riwayat job selesai, tugas yang sudah diterapkan (1.205), dan 35 tugas menunggu tinjauan. Worker tidak sedang berjalan sehingga tidak ada token yang terpakai oleh antrean lama.

### 3.3 Yang perlu dibangun

**Antrean bab (backend)**
1. Satu perintah generate = satu job per bab yang mengerjakan materi lalu bank 50 lalu gerbang, dengan kunci unik per bab agar tidak dobel.
2. Prioritas: permintaan langsung dari pengguna (10), admin (30), gelombang massal (100).
3. Antrean gelombang dari `antrean_generate_v1.csv`: admin memilih gelombang atau mapel, sistem membuat run.
4. Batas anggaran dalam rupiah per run dan per hari. Berhenti otomatis jika gagal >5%, hakim <4,0 dua kali berturut-turut, atau biaya lebih dari 1,4× estimasi.
5. Detak jantung worker (siapa hidup, sedang apa, kapan terakhir terlihat) dan pengaturan jumlah worker.
6. Tombol henti darurat: jeda semua, dan hapus antrean menunggu.

**Generate langsung di aplikasi**
1. Admin dan kurator: tombol "Isi bab ini" pada bab kosong (di pustaka dan di tampilan jalur) yang membuat job prioritas 30.
2. Pengguna belajar: unit berstatus `soon` menampilkan "sedang disiapkan" dan, bila diizinkan, mengantre satu job prioritas 10 dengan pembatasan (satu per bab, batas harian total, batas per pengguna). Bab yang sedang dibuat tidak dibuat lagi.
3. Endpoint status per bab sehingga tampilan bisa menampilkan kemajuan dan pengguna dikabari saat siap.
4. Pengguna belajar hanya melihat bab berstatus `siap`. Draf tidak pernah tampil.

**Dashboard admin** (perluasan Pabrik Konten, atau tab baru "Antrean")
- Ringkasan: bab selesai, dalam antrean, sedang jalan, gagal, perlu tinjauan, per gelombang dan per mapel.
- Uang: biaya terpakai hari ini dan total (Rp), sisa anggaran, biaya rata-rata per bab, perkiraan sisa biaya dan waktu (ETA).
- Papan bab: per bab, ikon materi, bank n/50, status gerbang, skor hakim, token dan biaya, waktu, percobaan.
- Antrean: daftar menunggu dan berjalan, ubah prioritas, batalkan, coba ulang, hapus semua.
- Kesehatan: worker hidup atau mati, laju per menit, kegagalan berulang per penyebab (429, parse, mutu).
- Tinjauan: bab gagal gerbang dengan alasannya, setujui, generate ulang, atau tolak.
- Jejak audit: siapa memulai, menjeda, atau menghapus apa.

## 4. Urutan pengerjaan

| Langkah | Isi | Bergantung pada |
|---|---|---|
| 0 | Bersihkan antrean lama. **Sudah dikerjakan.** | – |
| 1 | Keputusan aturan (bagian 5) dan penulisan profil Fase menjadi konfigurasi kode. | Persetujuanmu |
| 2 | Gerbang baru (keterbacaan, konteks, dimensi, tipe soal) dan penggantian campuran "konsep". | 1 |
| 3 | Antrean bab, anggaran rupiah, detak worker, henti darurat. | – |
| 4 | Dashboard antrean dan papan bab. | 3 |
| 5 | Gelombang 0: 2 bab × 13 mapel, semua dinilai hakim. Kalibrasi profil Fase dan batas. | 2, 3, 4 |
| 6 | Gelombang 1 (Matematika) dan Bahasa Inggris, Rp ±2,9 juta. Periksa ulang 338 bab lama. | 5 lolos |
| 7 | Generate langsung di aplikasi (admin, lalu pengguna). | 3, 4 |
| 8 | Gelombang 2–4, per gelombang menunggu persetujuanmu. | 6 |

Tidak ada generate massal yang berjalan sebelum langkah 5 selesai dan kamu menyetujuinya.

## 5. Keputusan yang saya butuhkan

1. **Tipe "pilihan ganda banyak jawaban":** dikeluarkan dari bank (usulan saya), atau kita bangun dulu penilaiannya di sesi jalur? Mengeluarkannya lebih murah dan cepat.
2. **Bobot Bloom per Fase** (bagian 1.2, baris terakhir): geser ke C1–C3 untuk Fase A–B (usulan saya), atau pakai tabel yang sama untuk semua jenjang?
3. **Generate langsung oleh pengguna belajar:** diizinkan (dengan pembatas), atau hanya admin dan kurator pada tahap awal? Usulan saya admin dahulu.

## 6. Yang belum diketahui

- Pembagian token masuk:keluar. Biaya bisa meleset ke atas jika token keluar lebih besar.
- Apakah profil Fase pada bagian 1.1 membuat materi lebih panjang atau lebih mahal (prompt lebih besar, kemungkinan lebih banyak putaran ulang).
- Biaya sains dan sosial (gelombang 0 menjawabnya), dan laju maksimum Vertex di atas 3 worker.
- Mutu 324 + 14 bab lama terhadap aturan baru. Belum diperiksa.
