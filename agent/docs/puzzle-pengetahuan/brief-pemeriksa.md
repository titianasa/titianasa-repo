# Brief auditor deck

Untuk agen yang mengaudit hasil produksi massal. Audit berjalan di putaran tersendiri, terpisah dari penulisan. Satu auditor memegang satu berkas produksi: `titian-web/src/content/kartu/produksi/<id-tugas>.ts`. Ambil dari antrean `bun scripts/antrian-audit.ts --json`, yang mendahulukan berkas paling lama.

Tugasmu menemukan kesalahan yang tidak tertangkap gerbang otomatis, lalu membetulkannya langsung di berkas itu. Jangan mengubah berkas lain.

Mulai dari tiga hal yang sudah ada di antrean:
- `catatan` penulis untuk deck itu;
- pelanggaran gerbang (`gerbang`), termasuk aturan yang lahir sesudah deck ditulis, misalnya lab tanpa petunjuk;
- temuan audit sebelumnya yang berulang (lihat "Temuan berulang" di `produksi-massal-kartu.md`).

Sesudah itu, baca deck tanpa memakai kesimpulan penulis. Anggap setiap kalimat bisa salah sampai kamu memeriksanya.

## Yang diperiksa per deck

1. **Kebenaran matematika.**
   - Hitung ulang setiap angka: di kartu, gambar, contoh kerja, soal, pilihan, dan penjelasan.
   - Untuk aljabar, uji dengan beberapa nilai pengganti.
   - Soal `choice` harus punya tepat satu jawaban benar. Soal `multi` harus tepat sesuai kunci. Setiap pernyataan `bs` harus benar-benar benar atau salah.
2. **Gambar.** Koordinat harus sesuai angka yang ditulis, label tidak boleh bertumpuk, dan warna yang disebut teks harus sesuai palet (0 biru, 1 merah muda, 2 hijau, 3 ungu, 4 kuning).
3. **Bahasa Inggris.**
   - Setiap kalimat contoh harus gramatikal dan wajar dalam British English, serta sesuai level CEFR deck.
   - Kalimat salah hanya boleh muncul di sisi "salah".
   - Terjemahan Indonesia harus tepat.
4. **Fakta dan acuan.**
   - Istilah harus sesuai buku sekolah Indonesia.
   - Istilah dan kebenaran dicek terhadap sumber di `bun scripts/spek-deck.ts <slug>`. Cakupan dinilai menurut kelengkapan ilmunya, bukan dibatasi satu buku.
   - Fakta yang bisa berubah, seperti harga atau aturan, tidak boleh ditulis sebagai angka pasti.
5. **Pedagogi.**
   - Urutannya: masalah, ingat, konsep, contoh kerja, latihan, kesalahan khas, ringkasan.
   - Kartu `ingat` harus benar-benar relevan.
   - Pengecoh harus berasal dari kesalahan khas, bukan angka acak.
   - Tanda `level` harus sesuai isi soal.
   - Deck kanonik tidak boleh mengandaikan usia atau kelas pembacanya, dan tidak boleh memuat penyesuaian jalur seperti prabaca, gaya TKA, atau kartu jembatan (ADR-0026).
   - Cakupannya harus tuntas menurut ilmunya.
   - Uji dua arah: apakah orang awam bisa mengikutinya tanpa sumber lain, dan apakah akademisi tetap menemukan isi yang utuh dan benar. Istilah yang belum dijelaskan atau kedalaman yang dipangkas sama-sama temuan.
6. **Animasi dan interaksi** (bagian "Animasi dan interaksi" di `brief-penulis.md`).
   - Kartu yang menjelaskan proses atau perubahan harus memperagakannya, bukan menampilkan hasil akhir saja. Tambahkan tahap bila perlu.
   - Setiap tahap punya satu tugas, dan keterangannya cocok dengan yang sedang bergerak atau disorot.
   - Gambar rujukan tetap diam. Gerak hiasan dibuang.
   - Setiap lab punya `petunjuk` yang menyebut apa yang disentuh dan apa yang diperhatikan.
7. **Tata letak.** Label gambar tidak boleh saling menimpa. Ukur jarak label dari koordinat dan ukuran hurufnya. Tampilan browser 9:16 dan 16:9 diuji penggabung dengan `fit.ts` dan audit tumpang tindih.
8. **Bahasa penjelasan.** Hindari AI slop: kalimat umum, pembuka kosong, pujian kosong, dan pengulangan. Pakai "kamu" dan "nggak" secara konsisten.

## Sesudah membetulkan

Jalankan `bun scripts/periksa-kartu.ts <slug> ...` sampai lolos, lalu `bunx tsc --noEmit -p .` sekali di akhir, keduanya di `titian-web`.

Isi `audit[slug]` di berkas itu untuk setiap deck yang kamu audit:
- `tanggal`: tanggal audit;
- `perbaikan`: satu baris per perbaikan;
- `terbuka`: yang belum bisa dibetulkan, misalnya fitur yang belum ada.

Hapus catatan penulis yang sudah beres. Deck tanpa entri `audit` tetap dianggap belum diaudit.

## Laporan

Kembalikan juga, untuk setiap temuan:
- deck dan kartunya;
- masalahnya;
- perbaikan yang kamu lakukan, atau alasan tidak diperbaiki.

Tandai juga apakah semua deck lolos gerbang.
