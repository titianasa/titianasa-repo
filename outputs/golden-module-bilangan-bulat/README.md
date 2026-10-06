# Golden module — Bilangan Bulat

Paket ini adalah aset produksi pertama untuk konsep `MAT.NUM.INT.OPPOSITE_SIGN_ADD` — **menjumlahkan bilangan bulat dengan tanda berbeda**. Ia sengaja memisahkan tiga aset yang dipakai ulang oleh banyak learning path:

- `article-lesson-plan.json`: isi artikel dan checkpoint per bagian untuk item `article`.
- `quiz-config.json`: kuis latihan mandiri untuk item `quiz`.
- `number-line-codeweb.html`: item `code_web` berupa garis bilangan interaktif.
- `concept-map.json`: metadata kanonik; UUID konsep diisi setelah konsep dibuat pada Admin Pusat.

## Cara memasukkan ke Studio

1. Buat modul perpustakaan (bukan modul referensi/path) bernama **Operasi Bilangan Bulat**.
2. Buat tiga item sesuai urutan: artikel, Web Interaktif, lalu kuis. Kaitkan masing-masing dengan konsep pada `concept-map.json` setelah UUID tersedia.
3. Pada item artikel, simpan isi `article-lesson-plan.json` melalui editor Modul Belajar. Pada item kuis, simpan `quiz-config.json` melalui Quiz Builder. Tempel seluruh HTML CodeWeb ke item Web Interaktif.
4. Tinjau akademik, uji di ponsel dan layar sentuh, lalu publish. UUID soal akan diberikan server saat kuis disimpan; jangan menuliskannya manual.

## Batas integrasi saat ini

HTML sudah memanggil `window.Titian.submitScore` dan `window.Titian.complete` **jika** bridge tersedia. Viewer CodeWeb saat ini belum menyuntikkan bridge tersebut, sehingga panggilan bersifat aman tetapi progres/skor belum tersimpan otomatis. Jangan memakai skor CodeWeb sebagai syarat kelulusan sebelum bridge `postMessage` atau `window.Titian` benar-benar dihubungkan di runtime.

## Penggunaan ulang

Gunakan modul sumber yang sama untuk fondasi SMP, remedial, dan path TKA; path hanya mengatur urutan, target mastery, dan pemilihan latihan. Jangan menyalin artikel atau HTML ini ke tiap path.
