# Standar Mutu Bab v1

Berlaku untuk semua mapel dan semua Fase. Sebuah bab boleh berstatus `siap` (tampil ke pengguna) hanya jika **semua gerbang** di bawah lolos. Tidak ada jalan pintas, termasuk untuk bab yang "kelihatannya bagus".

## Yang dijamin dan yang tidak

Proses ini menjamin bahwa tidak ada bab yang tampil sebelum lolos pemeriksaan berlapis: struktur dan taksonomi diperiksa mesin, hitungan diperiksa kode, kunci diperiksa oleh penjawab kedua yang buta kunci, mutu diperiksa penelaah dari model berbeda, dan sebagian dibaca manusia. Proses ini **tidak** menjamin nol kesalahan: model bisa salah pada fakta yang tidak bisa diperiksa mesin (sejarah, biologi, hukum ekonomi), dan kesesuaian dengan anak nyata baru terlihat pada pemakaian. Karena itu ada gerbang manusia dan mekanisme laporan setelah rilis (bagian 4).

## 1. Gerbang otomatis (tanpa token, wajib)

`validasi_bab.py` harus **LOLOS**:

| Pemeriksaan | Ambang |
|---|---|
| Struktur | tepat 50 soal, skema aplikasi, uid unik, kunci ada di pilihan, 4 pilihan, tidak ada "semua benar" |
| Taksonomi | sel Bloom × kesulitan × fungsi persis; mudah 15, sedang 25, sulit 10; tiap dimensi pengetahuan ≥3 (metakognitif ≥2); tipe hanya PG, B/S, isian |
| Materi | jumlah bagian, kata per bagian, kalimat rata-rata dan terpanjang sesuai Fase; ada blok kesalahan umum dan blok terstruktur |
| Rumus | setiap `$...$` dirender KaTeX aplikasi tanpa galat; tidak ada `$` liar; kunci isian tanpa LaTeX |
| Hitungan | soal berkunci bilangan diverifikasi kode (minimal 20 soal untuk mapel hitungan); kunci = hasil ekspresi |
| Web interaktif | HTML lengkap ≤120 ribu karakter; tanpa iframe/handler inline/sumber luar di luar CDN yang diizinkan; JavaScript lolos pemeriksaan sintaks; memakai token warna dan mode gelap Titian; memanggil `window.Titian.complete()` atau `submitScore()` |

## 2. Gerbang penjawab kedua (buta kunci, wajib)

Model berbeda mengerjakan 50 soal **tanpa kunci** (`siapkan_penelaahan.py`). Kecocokan harus **100% setelah penyelesaian**: setiap ketidakcocokan diselesaikan (kunci salah diperbaiki, soal ambigu ditulis ulang, atau terbukti jawaban penelaah yang salah) dan ditulis singkat di catatan bab. Kecocokan awal <90% berarti penulisnya bermasalah; ulangi generate bab, jangan ditambal.

## 3. Gerbang penelaah mutu (wajib)

`PROMPT_PENELAAH_BAB.md` langkah 2 oleh model berbeda dari penulis.

| Kriteria | Ambang |
|---|---|
| Blocker | 0 |
| Major | 0 |
| Skor tiap dimensi | ≥4,0 |
| Rata-rata | ≥4,3 |
| `kesesuaian_jenjang` pada Fase A–C | ≥4,5 |

Gagal → kembali ke penulis dengan daftar isu → semua gerbang diulang dari awal. Maksimal 3 putaran; bab yang masih gagal masuk antrean manusia dan tidak dipaksa lolos.

## 4. Gerbang manusia (sampel, wajib)

| Kapan | Berapa banyak |
|---|---|
| Setiap mapel dan Fase baru | 5 bab pertama dibaca guru mapel sebelum generate massal Fase itu |
| Tiap topik | bab pertama pada topik dibaca |
| Selain itu | sampel acak 1 dari 10 bab |
| Web interaktif | dicoba manual di peramban (sentuh dan desktop, terang dan gelap) untuk semua yang pertama kali memakai pola baru |

Daftar 10 poin bagi pembaca manusia: (1) fakta benar, (2) hitungan benar, (3) bahasa sesuai usia, (4) contoh sesuai usia, (5) tidak ada yang bikin bingung, (6) soal jelas, (7) kunci benar, (8) pengecoh masuk akal, (9) web interaktif jalan dan setia materi, (10) bab layak dipakai murid tanpa perbaikan.

## 5. Sesudah tayang (fitur laporan konten sudah ada; penarikan otomatis dan penandaan soal di bawah **belum dibangun**)

- Tombol "laporkan soal/materi" pada pengguna (tabel `content_reports` dan halaman admin Laporan Konten sudah ada). Usulan: bab yang dilaporkan ≥2 kali otomatis ditarik ke status `perlu tinjau` dan hilang dari jalur sampai ditinjau.
- Usulan: soal dengan tingkat benar yang sangat rendah atau sangat tinggi secara konsisten (data `canon_question_facts`) ditandai untuk ditinjau: soal yang hampir tidak ada yang menjawab benar sering kuncinya salah.
- Bab dengan tingkat berhenti tinggi di satu unit ditinjau materinya.

## 6. Kalibrasi awal

Sebelum generate massal per Fase, buat 5 bab, lewatkan semua gerbang, dan catat: berapa yang gagal di gerbang mana, berapa biaya token, dan apa yang dikoreksi manusia. Angka ambang di dokumen ini (panjang kalimat per Fase, 0,4 kunci per huruf, dan sebagainya) diubah dengan bukti dari kalibrasi ini, bukan berdasarkan perasaan.
