# Brief peninjau misi: soal yang mustahil dijawab benar

Tugasmu mencari dan memperbaiki soal misi Matematika yang tidak bisa dijawab benar oleh siswa yang sudah paham materinya, hanya dari apa yang ia lihat (atau dengar di Level 1). Ubah seminimal mungkin. Jangan mengganti id, deck, kartu, level, SYARAT, atau KEMAMPUAN.

Baca dulu `agent/docs/puzzle-pengetahuan/temuan-misi.md`: masalah yang sudah pernah terjadi dan aturannya.

## Yang dilihat siswa
- **tebak** dan **pilih**: teks soal dan tiga pilihan. Tidak ada gambar, tabel, atau kartu di layar.
- **isian** (uji akhir): hanya teks soal dengan `___`. Penjelasannya baru muncul setelah menjawab. Jawaban diketik di ponsel. Server menerima variasi ketikan (spasi, titik atau koma desimal, `-` untuk `−`, satuan atau Rp di sekitar angka, "nggak" untuk "tidak"), tapi bentuk lain tetap ditolak: 0,5 untuk 1/2, 3/6 untuk 1/2, kata untuk angka.
- **latihan**: arti kalimat sebagai petunjuk, lalu kalimat matematika dikerjakan lewat berbagai bentuk (isi angka, susun blok, ketik). Bilangan atau huruf yang tidak disebut di petunjuk otomatis ditampilkan sebagai "Pakai bilangan: …".
- **pakai** (uji akhir): teks situasi, siswa mengetik kalimat matematikanya. Kalimat yang dibaca dari sisi lain (`1 > −3` untuk `−3 < 1`) diterima.

## Yang termasuk mustahil atau ambigu
1. Lebih dari satu pilihan yang benar, atau pilihan yang ditandai benar ternyata salah.
2. Soal butuh gambar, diagram, tabel, atau data yang tidak ada di teks.
3. Isian yang punya lebih dari satu jawaban benar, atau tidak menyebut bentuk yang diminta (pecahan atau desimal, satuan apa, sederhanakan atau tidak, jam berapa dalam format apa).
4. Isian yang jawabannya berupa kata yang bisa ditulis beberapa cara (sinonim, singkatan) tanpa diarahkan teks soalnya.
5. Situasi pakai yang bisa ditulis sebagai kalimat lain yang sama benarnya (urutan bilangan berbeda, cara lain menghitung), padahal hanya satu yang diterima. Perbaiki situasinya supaya urutannya jelas, misalnya "Mula-mula …, lalu …".
6. Hitungan atau fakta yang salah.

Bukan masalah: soal sulit, pilihan salah yang bernilai sama tapi bukan bentuk yang diminta (4/6 untuk "bentuk paling sederhana"), atau tebak sebelum materi yang memang menguji tebakan awal.

## Cara memperbaiki
- Ubah teks soal, pilihan, atau jawaban supaya tepat satu jawaban benar dan bentuknya jelas.
- Tetap bahasa Indonesia alami untuk level itu. Level 1 untuk didengar: kalimat pendek.
- Setelah selesai, jalankan `cd titian-web && MISI_CEK=1 bun scripts/misi-bilangan-bulat.ts` (hanya memeriksa, tidak menulis) dan `../agent/tools/batas-ram.sh 3G bunx tsc --noEmit -p .` (dari folder titian-web; tsc memakan ±2 GB, jadi selalu lewat pembatas RAM ini). Keduanya harus bersih. Jangan menjalankan generator tanpa `MISI_CEK=1`. Kalau ada perintah yang ditolak sistem izin, jangan coba cara lain; laporkan.

## Batas kerja
Kerjakan sendiri. Jangan menjalankan agen atau subagen lain: pemilik membatasi dua agen sekaligus untuk seluruh pekerjaan.

## Laporan
Jumlah soal yang diperiksa dan yang diubah, per jenis masalah di atas, dengan beberapa contoh sebelum dan sesudah.
