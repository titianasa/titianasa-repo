# Standar Pengembangan Kurikulum: Mapel → Topik → Bab (V1)

Dipakai sebelum materi dan bank soal ditulis. Tujuannya satu: pohon **Mapel → Topik → Bab** benar, lengkap, urut, dan pantas dipakai semua learning path. Materi dan soal yang ditulis di atas pohon yang keliru hanya membuang token.

## 1. Sumber acuan

| Kebutuhan | Acuan |
|---|---|
| Cakupan dan jenjang | Capaian Pembelajaran Kurikulum Merdeka per Fase (A: Kelas 1–2, B: 3–4, C: 5–6, D: 7–9, E: 10, F: 11–12) dan elemennya |
| Ujian | Kerangka TKA (SD, SMP, SMA), subtes UTBK-SNBT, Cambridge Primary/Lower Secondary/IGCSE/A Level |
| Urutan | Prasyarat konsep (siapa harus dipahami lebih dulu) |
| Perkembangan | Tahap kognitif dan bahasa pembelajar pada usianya |

## 2. Aturan pedagogi

1. **Satu topik = satu kelas.** Topik yang isinya melintasi kelas dipecah. Label `jenjang:SD-3` harus benar untuk seluruh bab di dalamnya.
2. **Batas atas per Fase.** Isi topik tidak boleh melampaui capaian Fase-nya (contoh: Fase A membilang sampai 100, Fase B sampai 10.000, Fase C sampai 1.000.000).
3. **Kurikulum spiral.** Konsep yang sama muncul lagi di kelas berikutnya sebagai topik terpisah dengan rentang lebih luas ("Bilangan sampai 20", "sampai 100", "sampai 1.000", ...). Tidak ada satu topik yang dipakai untuk seluruh SD.
4. **Lengkap per elemen.** Setiap kelas menutup semua elemen mapelnya. Matematika: Bilangan, Aljabar/Pola, Pengukuran, Geometri, Data dan Peluang.
5. **Urutan prasyarat.** Di dalam kelas, topik disusun dari prasyarat ke turunan. Tidak ada topik yang memakai konsep yang baru diajarkan sesudahnya.
6. **Konkret → Gambar → Simbol (Bruner) untuk Fase A–C.** Bab awal sebuah konsep memakai benda dan gambar; simbol menyusul.
7. **Satu bab = satu tujuan belajar** yang dapat diperiksa, kira-kira 15–25 menit di SD, 25–40 menit di SMP dan SMA.
8. **Bentuk topik: 5–7 bab** dengan urutan Konsep → Prosedur atau Representasi → Penerapan (soal cerita) → **Kesalahan Umum** (miskonsepsi yang paling sering).
9. **Bloom menurut Fase.** A: C1–C2, B: C1–C3, C: C1–C4 ringan, D: C1–C4, E–F: C1–C5.
10. **Bahasa dan konteks** sesuai usia; judul bab menyebut tujuan belajar, bukan merek ujian.

## 3. Netral terhadap learning path

Kurikulum Indonesia adalah **tulang punggung**. Jalur lain **diturunkan dari tulang punggung dengan aturan**, tidak ditulis ulang:

| Jalur | Diturunkan dari |
|---|---|
| Kurikulum Cambridge Stage N | Kelas N (nama mapel Cambridge) |
| TKA SD | topik Kelas 5–6 (Fase C) |
| TKA SMP | topik Kelas 8–9 |
| TKA SMA | topik Kelas 10–12 (wajib, Saintek, Soshum) |
| UTBK-SNBT | topik Kelas 10–12 ditambah subtes penalaran |

Topik khusus ujian (misalnya strategi tes) hidup hanya di jalur ujian dan diberi label `ujian`.

## 4. Mekanisme perubahan (alat)

Perubahan dibuat sebagai **rencana** (`rencana/*.json`) lalu diterapkan oleh `terapkan_rencana.sql`:
- memindahkan bab antar-topik **dengan id yang sama**, sehingga materi, bank soal, gate, dan progres pembelajar ikut;
- membuat topik dan bab baru (bab baru hanya kerangka: judul, artikel, dan bank kosong);
- bab duplikat diarsipkan (`status = archived`); bab dan topik yang memang tidak sesuai boleh diubah judulnya atau dihapus (`hapus`, `hapus_topik`) karena aplikasi belum diluncurkan;
- label `jenjang`/`cambridge` diperbarui;
- folder turunan (Kurikulum Indonesia, Cambridge, TKA) dibangun ulang dari rencana;
- satu transaksi, aman diulang.
