# Uji kartu di browser

Alat untuk menguji deck kartu seperti pengguna. Semuanya memakai `../webview.ts` (Bun.WebView) dan server web dev (`WEB`, bawaan `http://localhost:3010`). Gambar disimpan di `OUT`.

| Skrip | Kegunaan |
|---|---|
| `bun fit.ts awalan1,awalan2` | Setiap kartu di mode video dan web harus muat di dalam kartu 9:16. |
| `bun shot1.ts slug n` | Tangkapan layar satu kartu (n = 1 untuk sampul, kartu pertama = 2). `MODE=web` menampilkan tombol web. |
| `bun ketuk.ts slug n selektor i ...` | Mengetuk elemen SVG ke-i di dalam lab (misalnya `g`, `polygon`), lalu mengambil gambarnya. |
| `bun jalan-deck.ts slug` | Menjalani seluruh deck di mode web, termasuk membuka kartu ingat. |
| `bun isu.ts slug:n slug:n ...` | Menghitung galat konsol dan ketidakcocokan hidrasi yang ditandai Next.js dev di setiap kartu. Hasil yang diharapkan: `0 issue`. |

Gerbang isinya ada di `titian-web/scripts/periksa-kartu.ts`. Urutannya: gerbang, `fit.ts`, lalu lihat setiap kartu bergambar dan setiap lab.

Bun.WebView membuat profil browser di folder kerja, dengan nama berawalan titik dan berakhiran `.bun-chrome`, setiap kali dijalankan. Hapus profil yang sudah tidak dipakai setelah selesai. Kalau dibiarkan, 89 profil pernah memakan 17 GB.
