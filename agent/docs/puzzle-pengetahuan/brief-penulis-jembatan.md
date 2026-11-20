# Brief penulis kartu jembatan

Brief ini untuk agen yang menulis deck jembatan (ADR-0030). Satu agen menulis satu file di `titian-web/src/content/kartu/jembatan/`, lalu mendaftarkannya di `jembatan/index.ts`. Agen hanya boleh mengubah file misi level yang disebut di tugasnya. Tidak ada commit, dan tidak ada tulis ke database.

## Baca dulu
- `agent/docs/adr/0030-kartu-jembatan-per-jenjang.md` dan `agent/docs/adr/0026-*.md` (kanonik versus jalur).
- `agent/docs/puzzle-pengetahuan/temuan-misi.md`: temuan yang menjadi dasar tugasmu dan aturan yang tidak boleh diulang.
- `agent/docs/puzzle-pengetahuan/standar-kartu-lengkap.md` dan `brief-penulis.md`: bentuk kartu, jenis soal, dan larangan gaya.
- Untuk Kelas 1–2: `riset-kelas-awal.md`. Untuk Kelas 3 sampai SMA: `riset-sd-sma.md`. Contoh deck prabaca ada di `src/content/kartu/mtk/cacah-dasar.ts`.
- Tipe `Deck` dan semua jenis kartu di `src/content/kartu/types.ts`. Contoh deck jalur ada di `src/content/kartu/kemasan.ts`.
- Deck kanoniknya sendiri. Baca setiap kartu sampai habis.

## Yang ditulis
- Untuk setiap deck kanonik di tugasmu, tulis satu deck jembatan dengan slug `jb-<slug-kanonik>`, `unit` yang sama, dan `kategori` yang sama. `title` dan `sub` ditulis untuk jenjang itu.
  - Daftarkan dengan `untukJalur(deck, jalur)` dari `./jalur`.
  - `jalur` berisi jalur yang mengajarkan unit itu di jenjang yang sama. Lihat `titian-backend-go/data/kanonik/jalur/*.json` dan grup kelas atau levelnya.
  - `matematika-berurutan` selalu ditaruh pertama kalau unitnya ada di sana.
- **Jenjang lebih rendah dari deck kanonik** (SD awal, SD, SMP):
  - Ajarkan inti unit sedalam yang diminta jenjang itu, lengkap: konsep, contoh, kekeliruan umum, latihan, dan ringkasan.
  - Materi yang melampaui jenjang tidak diajarkan. Cukup satu kartu penutup yang menyebut bahwa kelanjutannya ada di deck lengkap.
  - Kelas 1–2 memakai `prabaca: true` dengan aturan riset kelas awal: kalimat sangat pendek, `say` di setiap kartu, dan catatan pendamping.
- **Perguruan tinggi:**
  - Deck jembatan menjadi pendalaman akademik: definisi formal, teorema dengan syaratnya, bukti atau sketsa bukti, contoh penyangkal, dan penerapan di bidang ilmu.
  - Bahasanya Indonesia akademik baku. Tanpa "nggak", tanpa contoh warung atau Pramuka.
  - Jangan mengulang kartu kanonik. Rujuk saja.
- **Misi:** kalau tugasmu menyebut file misi level, tambahkan `kartu: "jb-…"` pada entri BAB deck itu. Lalu susun ulang `kartu` di setiap tema deck itu sehingga menunjuk indeks kartu materi deck jembatan.
  - Setiap kartu materi deck jembatan masuk tepat satu tema.
  - Id tema tetap. Isi tebak, latihan, dan isian disesuaikan kalau ternyata memakai materi yang sekarang tidak diajarkan.
  - Ikuti juga `brief-penulis-misi.md`.

## Mutu
- Bahasa Indonesia alami seperti tutor yang baik bicara ke siswa di jenjang itu.
- Matematika tepat.
- Contoh berasal dari kehidupan Indonesia yang dikenal siswa di jenjang itu.
- Soal hanya punya satu jawaban benar, dan bisa dijawab dari isi kartu yang tampil.

## Periksa sebelum selesai
1. `cd titian-web && bun scripts/periksa-kartu.ts jb-` lolos untuk deck-mu.
2. `bun scripts/daftar-deck.ts`, lalu `MISI_CEK=1 bun scripts/misi-bilangan-bulat.ts`. Keduanya tanpa baris masalah.
3. `../agent/tools/batas-ram.sh 3G bunx tsc --noEmit -p .` (dari folder titian-web; tsc memakan ±2 GB, jadi selalu lewat pembatas RAM ini) bersih untuk file-mu.
4. Jangan menyalakan server atau browser (RAM 15 GB). Jangan menjalankan importer.

## Batas kerja
Kerjakan sendiri. Jangan menjalankan agen atau subagen lain.

## Laporan (singkat)
Laporkan per deck:
- slug, jalur, dan jumlah kartu;
- apa yang ditinggalkan untuk deck lengkap;
- perubahan tema misi;
- isi kanonik yang menurutmu salah fakta, untuk diperbaiki koordinator.
