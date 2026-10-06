# Audit Kurikulum pada Learning Path yang Tampil (2026-09-21)

Cakupan: lima jalur yang tampil (Belajar Bahasa Inggris, Kurikulum Indonesia, Kurikulum Cambridge, Fokus Ujian TKA, Persiapan Ujian Masuk PT), tanpa cabang yang ditahan. Data: DB dev. Berkas pendukung: `topik_dalam_jalur.csv` (2.192 topik), `kebutuhan_per_mapel.csv`, `topik_tanpa_bab.csv`, `topik_bab_sedikit.csv`. Kueri: `audit.sql`, `q2..q5.sql`.

Definisi "bab lengkap": punya materi (artikel dengan bagian) **dan** bank soal ≥ 15 (semua yang lengkap kini berisi ±50 soal bertag fungsi).

## 1. Ringkasan (topik unik, tanpa hitung ganda antar jalur)

| Ukuran | Jumlah |
|---|---:|
| Topik | 2.192 |
| Bab | 9.032 |
| Bab bermateri | 719 |
| Bab berbank soal | 624 |
| **Bab lengkap** | **624** |
| **Bab yang perlu dibuat** | **8.408** |
| — perlu materi + bank | 8.313 |
| — sudah bermateri, hanya perlu bank | 95 |

Per jalur (dihitung per alias, jadi ada yang sama antar jalur): Inggris 1.944 lengkap dari 3.815 bab; Cambridge 935 dari 6.436; Kurikulum Indonesia 497 dari 7.107; TKA 249 dari 5.548; PTN 95 dari 4.513.

## 2. Apakah tiap jalur/folder punya bab yang sesuai?

- **Mapel vs isi folder: sesuai.** Tidak ada satu pun alias yang tersasar ke mapel lain (0 dari 2.192).
- **Topik tanpa bab: 10.** Tiga di Belajar Bahasa Inggris (Present Perfect Continuous, Future Perfect Continuous, Third Conditional), satu di TKA (Teks Sastra), enam di Cambridge Science Stage 5–6 (Benda Hidup & Tak Hidup, Bermain & Bergerak, Provinsi & Ibu Kota, Hidup Rukun di Lingkungan, Perubahan Wujud Benda, Merawat Diri & Kebersihan).
- **Cambridge Science memuat topik IPS.** IPAS menggabungkan alam dan sosial; "Provinsi & Ibu Kota" dan "Hidup Rukun di Lingkungan" bukan sains. Perlu dikurasi bila Science Cambridge harus murni sains.
- **Tingkat (level): hampir sesuai.** Jenjang SD/SMP/SMA mengambil Tahap pustaka yang wajar. Yang patut ditinjau hanya Bahasa Inggris: SMP memuat 28 topik dari Tahap 4–6 (Empat Keterampilan, Jenis Teks, Lanjutan & Profesional), SMA memuat 43 topik Tahap 9 (Persiapan Tes Internasional) dan 16 topik Tahap 5–6, SD memuat 3 topik Tahap 3.
- **Kelas vs kanonik (Matematika).** Cakupan bab tidak tipis: SD 186 bab, SMP 177, SMA 446 dibanding 67, 44, dan 60 unit kanonik pada level padanan. Bab di pustaka lebih halus daripada unit kanonik.

## 3. Apakah tiap topik punya bab yang lengkap dan sesuai?

- **Jumlah bab per topik konsisten:** 2.101 topik berisi 4–5 bab, 39 topik hanya 3 bab, 42 topik 6–9 bab, 10 topik kosong. Tidak ada topik dengan 1–2 bab. Daftar topik ≤3 bab: `topik_bab_sedikit.csv`.
- **Judul bab kembar: 25 judul (51 bab)**, misalnya "Prinsip Dasar Bioteknologi Konvensional" muncul di 3 topik. Ini duplikasi kecil, bukan pola.
- **Kelengkapan isi (inilah celah utamanya):** hanya 114 topik yang semua babnya lengkap, 81 sebagian, dan **1.987 topik belum punya satu pun bab lengkap**.
- **Kelengkapan per mapel:** hanya Bahasa Inggris (595 dari 1.639) dan Matematika (29 dari 1.071) yang punya bab lengkap. Fisika, Kimia, Biologi, Ekonomi, Bahasa Indonesia, IPA, Sejarah, Geografi, Akuntansi, Sosiologi, IPAS, Penalaran, Informatika, dan IPS semuanya nol.
- **Kesesuaian isi bab terhadap topik (kualitas materi)** tidak dinilai otomatis di audit ini; itu butuh hakim/kurator.

## 4. Kebutuhan pembuatan bab per mapel (topik unik seluruh jalur)

Lihat `kebutuhan_per_mapel.csv`. Ringkas: Bahasa Inggris 1.044, Matematika 1.042, Fisika 732, Kimia 698, Biologi 659, Ekonomi 652, Bahasa Indonesia 632, IPA 491, Sejarah 474, Geografi 364, Akuntansi 351, Sosiologi 337, IPAS 321, Penalaran & Logika 275, Informatika 258, IPS 78.

## 5. Catatan

- ICT dan Computer Science Cambridge sudah dikeluarkan dari daftar tahan, sehingga 258 bab Informatika kembali terjangkau lewat Cambridge, walau mapel Informatika sendiri tetap ditahan di daftar mata pelajaran.
- Kurikulum Indonesia 497 unit lengkap (turun dari 624) karena ±127 bab Inggris lanjutan hanya terdaftar lewat Perguruan Tinggi yang kini ditahan; bab itu tetap ada di Belajar Bahasa Inggris.
