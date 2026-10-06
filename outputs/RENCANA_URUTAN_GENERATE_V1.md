# Rencana Urutan Generate dan Hemat Token v1

Status: **usulan, belum ada satu pun generate yang dijalankan.** Dibuat 2026-09-21 setelah tinjauan kurikulum 15 mapel selesai. Setiap gelombang menunggu persetujuan tersendiri.

Antrean lengkap: `outputs/kurikulum/antrean_generate_v1.csv` (8.313 baris, satu per bab, sudah berurutan).

## 1. Yang harus digenerate

Jalur Kurikulum Indonesia berisi 1.707 topik dan 8.673 bab (15 mapel). Semua jalur lain (Cambridge, TKA, UTBK, Ujian Mandiri) hanya merujuk bab yang sama, jadi **biaya dihitung per bab, bukan per jalur**. Rata-rata satu bab dipakai 2 sampai 8 jalur.

| | Bab |
|---|---:|
| Sudah punya bank soal (≥15) | 360 (hampir semuanya Bahasa Inggris) |
| **Belum punya bank soal** | **8.313** |

Strategi kita: soal latihan adalah inti, materi opsional. Jadi yang diantre hanya bank soal. Materi dibuat menurut permintaan (bagian 5).

## 2. Urutan

Aturan urut: gelombang, lalu Kelas naik, lalu mapel, lalu urutan topik pada rencana kurikulum, lalu urutan bab. Satu topik dikerjakan sampai habis sebelum topik berikutnya, karena rantai buka-kunci berjalan per bab dan tampilan topik baru terasa selesai kalau semua babnya siap.

| Gelombang | Isi | Bab | Alasan |
|---|---|---:|---|
| 0 | Uji coba 2 bab × 13 mapel yang belum pernah diukur | ±26 | Benchmark lama hanya Matematika dan Inggris. Sains dan sosial mungkin lebih mahal atau lebih sering gagal mutu. |
| 1 | Matematika (SD→SMP→SMA) | 1.079 | Keputusan awal "Matematika dulu". Satu jalur utuh Kelas 1 sampai 12 yang bisa dites penuh. |
| 2 | Bahasa Inggris (sisa), Penalaran & Logika, Bahasa Indonesia | 1.582 | Universal untuk TKA, UTBK, dan Cambridge. Inggris sudah 40% jadi. |
| 3 | IPAS, IPA, Fisika, Kimia, Biologi | 3.134 | Saintek dan Cambridge Science. |
| 4 | IPS, Ekonomi, Geografi, Sejarah, Sosiologi, Akuntansi | 2.518 | Soshum. Paling akhir karena rujukan per bab paling sedikit di IPS dan bobot ujiannya lebih kecil. |

Ambang untuk lanjut dari satu gelombang ke berikutnya (semua harus terpenuhi pada sampel):
- Skor hakim `agent_qa` rata-rata ≥4,2 dan tidak ada bab di bawah 4,0.
- Soal KRITIS pada QA struktural <0,5%.
- Soal duplikat yang dibuang <10% dari yang dihasilkan.
- Bab gagal tuntas (kurang dari 15 soal setelah 3 putaran) <3%.

## 3. Estimasi biaya

Dasar: token nyata dari benchmark 20 bab di `ALGORITMA_GENERATE_HEMAT_TOKEN_V1.md` bagian 7 (bank tahap 1 rata-rata 14,7 ribu token, tahap 2 23,6 ribu, materi 6,8 ribu). Harga Vertex Gemini $0,75 masuk dan $3,75 keluar per 1 juta token.

**Asumsi yang belum diukur:** pembagian token masuk:keluar saya taruh 60:40. Tokennya terukur, tetapi pembagiannya tidak, jadi rentang wajar ±40%. Kurs Rp 16.500 per dolar juga asumsi.

| Komponen per bab | Token | Biaya |
|---|---:|---:|
| Bank tahap 1 (20 soal, playable) | 14.700 | ±$0,029 |
| Bank tahap 2 (+30 soal, jadi 50) | 23.600 | ±$0,046 |
| Materi (opsional) | 6.800 | ±$0,013 |
| Hakim, sampel 1 dari 5 bab | 6.000 | ±$0,0015 rata-rata |

| Gelombang | Bab | Tahap 1 | Tahap 1 + 2 |
|---|---:|---:|---:|
| 1 Matematika (×1,27 karena lebih mahal dari Inggris) | 1.079 | $40 | $105 |
| 2 Inggris, Penalaran, Indonesia | 1.582 | $45 | $118 |
| 3 Sains | 3.134 | $90 | $234 |
| 4 Soshum | 2.518 | $72 | $188 |
| **Total** | **8.313** | **±$250** | **±$650** |

Tambah 15% untuk putaran ulang dan gagal: tahap 1 saja ±$290 (±Rp 4,8 juta), tahap 1+2 ±$750 (±Rp 12 juta). Materi untuk semua bab menambah ±$110.

Waktu, dengan 3 worker seperti di benchmark (132 detik per bab tahap 1): gelombang 1 ±13 jam, gelombang 2 ±19 jam, gelombang 3 ±38 jam, gelombang 4 ±31 jam. Total ±102 jam. Batas laju Vertex di atas 3 worker belum diuji.

## 4. Cara hemat token

Urut dari yang paling besar efeknya dan yang sudah pasti.

1. **Tahap 1 dulu, tahap 2 menurut permintaan.** Tahap 1 (20 soal) sudah melewati ambang 15 soal untuk bisa dimainkan dan menghabiskan ±40% biaya bank penuh. Tahap 2 hanya untuk bab yang benar-benar dimainkan (misalnya ≥30 sesi) atau yang dipakai jalur ujian. Menunda tahap 2 untuk sebagian besar bab menghemat hingga ±$400 sampai ada bukti permintaan. **Perlu dicek dulu** apakah unit dengan 20 soal terasa cukup pada enam langkah unit (Pemanasan, Latihan 1, Latihan 2, Transfer, Ujian akhir). Aturan pengisi soal sisa memakai ulang soal, jadi ujian akhir bisa terasa berulang. Uji di gelombang 1 sebelum melebar.
2. **Panggilan campuran** (pilihan ganda, benar/salah, isian dalam satu panggilan): diperkirakan memangkas 30 sampai 45% dari bank. Ini belum dibangun. Kalau terbukti, biaya tahap 1+2 turun ke ±$360 sampai $455. Layak dibangun sebelum gelombang 3, karena gelombang 3 dan 4 adalah 68% dari total.
3. **Materi hanya sesuai permintaan.** Sejalan dengan strategi materi opsional. Kalau nanti dipakai untuk semua bab, taruh sesudah bank.
4. **Bab "Kesalahan Umum" (±1.700 bab) dengan bank lebih kecil.** Usul: 12 sampai 15 soal yang dibangun dari judul miskonsepsinya. Belum diukur, tetapi menghemat ±20% bank di bab jenis ini.
5. **Hakim hanya pada sampel.** 1 dari 5 bab (dan semua bab yang skor struktural-nya rendah), bukan setiap bab.
6. **Cegah duplikat sebelum panggilan.** Benchmark membuang 61 soal (±46 ribu dari ±530 ribu token). Kirim ringkasan judul soal yang sudah ada per topik (bukan potongan penuh) untuk menekan ini.
7. **Cache prompt** belum dimanfaatkan. Kalau Vertex menawarkan diskon cache untuk awalan yang sama, susun awalan yang seragam per mapel. Belum diperiksa, jadi jangan dihitung di anggaran.

## 5. Sebelum gelombang 1

1. Bangun panggilan campuran (poin 2) atau putuskan berjalan tanpa itu.
2. Jalankan `lean_benchmark` untuk gelombang 0 (±26 bab, ±$1).
3. Pasang tutup anggaran per gelombang di `services/metered_ai.rs` dan hentikan otomatis jika: gagal >5%, hakim <4,0 pada 2 bab berturut-turut, atau biaya sebenarnya lebih dari 1,4× estimasi.
4. Setelah tiap gelombang: `tag_all_banks --apply`, segarkan `bab_bank_stats`, lalu cek sampel di tampilan jalur.
5. Simpan cadangan DB sebelum tiap gelombang (aturan tetap).

## 6. Yang belum diketahui

- Pembagian token masuk:keluar dan kurs, jadi angka dolar di atas ±40%.
- Biaya per bab untuk sains dan sosial (gelombang 0 menjawabnya).
- Apakah 20 soal cukup nyaman untuk satu unit penuh.
- Laju maksimum Vertex di atas 3 worker.
- Soal hitungan (Fisika, Kimia) mungkin butuh lebih banyak putaran ulang daripada Matematika dan Inggris.
- Deteksi "materi sudah ada" di DB saya tidak bisa dipastikan, jadi angka 360 bab yang sudah punya bank berasal dari `bab_bank_stats`, bukan dari pemeriksaan isi materi.
