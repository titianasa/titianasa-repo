# Brief penulis deck jembatan dan misi varian Bahasa Inggris

Brief ini untuk agen yang menulis satu batch "Bahasa Inggris per jenjang" (ADR-0032) dari `antrian-misi-gambaran.md`. Untuk setiap deck kanonik di tugasmu, kamu menulis satu deck jembatan untuk jenjang itu dan misi variannya. Satu agen mengerjakan dua file baru:
- `titian-web/src/content/kartu/jembatan/en-<jenjang>-<batch>.ts`, didaftarkan di `jembatan/index.ts`;
- `titian-web/scripts/misi-inggris/<level>-<jenjang>-<batch>.ts`, didaftarkan di `scripts/misi-inggris/index.ts` sesudah file umum.

File lain tidak disentuh. Tidak ada commit dan tidak ada tulis ke database. Deck kanonik juga tidak diubah; kesalahan isinya dilaporkan.

## Baca dulu
- `agent/docs/adr/0032-misi-varian-per-jenjang.md`, `0030` (kartu jembatan), dan `0026` (satu catatan pengetahuan).
- `jenjang-inggris.md`: baris deck-mu menyebut apa yang dibuang dan inti yang tetap diajarkan.
- `brief-penulis-jembatan.md` dan `brief-penulis-misi-inggris.md`. Semua aturannya tetap berlaku, kecuali yang diubah di bawah.
- `riset-inggris.md` §1 (Kelas 3–4) dan §5 (E1–E21).
- Contoh yang sudah lolos: `jembatan/en-k34-a.ts` dan `scripts/misi-inggris/pre-a1-k34-a.ts`.
- Deck kanoniknya sendiri, setiap kartu sampai habis, serta misi umumnya di `scripts/misi-inggris/pre-a1-*.ts` atau `a1-*.ts`.

## Deck jembatan
- **Bentuk:** `slug: "jb-<deck-kanonik>-<jenjang>"`, dengan `unit` dan `kategori` sama dengan deck kanonik, serta `jenjang: "k34"` (atau `"k56"`). Daftarkan lewat `untukJalur(deck, ["inggris-kurikulum-indonesia"])`. `title` boleh lebih sederhana, tetapi tetap dalam bahasa Inggris ("The Alphabet", "A, An, The").
- **Kelas 3–4 (`k34`):** `prabaca: true`, karena penjelasan Indonesia dibacakan.
  - **Dengar dulu, lalu tirukan.** Setiap kata atau ungkapan sudah terdengar di kartu `examples`, `audio`, atau `figure` sebelum ditanyakan. Mulai kartu contoh dengan "Dengarkan, lalu tirukan" bila perlu.
  - **Gambar untuk benda konkret.** Pakai emoji di `figure` (gambar dan nama, muncul bertahap), di `table`, di `match`, atau di `gambar` soal.
  - **Konteks yang dikenal anak:** rumah, kelas, kantin, UKS, halaman sekolah, kampung, pasar bersama orang tua. Tokohnya Bu/Pak guru, teman sekelas, dan keluarga. Tanpa hotel, bandara, kantor, bank, kos, gaji, status menikah, atau menawar.
  - **Tanpa istilah tata bahasa** (subject, auxiliary, article, plural) dan tanpa kartu aturan. Pola diajarkan lewat ungkapan utuh dan contoh: "Satu benda diberi a", bukan "article tak tentu".
  - **Tanpa lambang fonetik.** Cara baca ditulis dengan ejaan Indonesia seperti di deck kanonik (`ei`, `SE-ven`).
  - **Tanpa materi yang belum diajarkan:** bentuk lampau, can/could/may yang bertumpuk, would like, kalimat tanya tidak langsung, ribuan, dan jam past/to. Materi di atas jenjang ditutup dengan satu kartu `idea` "Lanjutannya nanti".
  - **Batas gerbang Kelas 3:** penjelasan Indonesia ≤25 kata per kartu dan ≤9 kata per kalimat. Kalimat Inggris ≤7 kata, dan ≤3 kalimat Inggris per kartu. Untuk unit yang pertama diajarkan di Kelas 4, batasnya ≤40 dan ≤12. Yang dihitung adalah `say`, `q`, arti contoh, `why` di kartu kesalahan, dan catatan `compare`. Isi tabel dan `langkah` tidak dihitung.
  - **Latihan:** `choice` (kalimat ≤7 kata), `match`, `sort`, `listen` (satu kata yang sudah berekaman; cek dengan `berklip`), dan `type` satu kata (`sentence: "___"` atau `"___ 🍊"`). `choice` boleh memakai `klip` untuk kalimat berekaman. Minimal 5 latihan, dan `why` minimal 6 kata.
  - `dampingi` di kartu pertama berisi saran singkat untuk orang tua atau guru.
  - Wajib ada `mistakes` (kekeliruan khas anak Indonesia, tanpa istilah) dan `recap`.
- **Kelas 5–6 (`k56`):** tanpa prabaca. Batasnya A1 (≤60 kata, ≤12 kata per kalimat), dengan paling banyak 2 istilah per deck dan selalu disertai artinya. Konteksnya sekolah, keluarga, kampung, liburan, dan kantin. Ajarkan inti yang disebut `jenjang-inggris.md`.
- Pilih ungkapan yang wajar dan British English seperti deck kanonik. Bahasa Indonesia ditulis seperti guru SD bicara: kalimat pendek, "kamu", dan "tidak" secara konsisten di satu kartu.

## Misi varian
- **BAB:** `{ deck: "<deck kanonik>", key: "<key umum>-<jenjang>", title, icon, kartu: "jb-<deck>-<jenjang>", varian: "<jenjang>" }`. Deck kanoniknya harus sudah punya bab umum.
- **TEMA:** setiap tema diberi `varian`, dan id-nya berawalan level lalu jenjang: `pre-k34-…` atau `a1-k34-…`. `kartu` menunjuk indeks kartu materi deck jembatan, dan setiap kartu materi masuk tepat satu tema. Biasanya ada 2–3 tema per deck.
- **Kelas 3–4: hanya dengar lalu pilih.** Isi `latihan: []`, `pakai: []`, `target: ["", ""]`, minimal 4 `pilih`, 3 `tebak`, dan ≥3 `isian`. Pakai soal dengar (elemen keenam) sebanyak mungkin: "Dengarkan. Huruf apa yang disebut?" Jawaban isian satu kata ≤8 huruf, dan kurungnya memberi artinya ("Good ___! (selamat pagi)"). Kelas 3 belum menyusun kalimat, jadi jangan menulis latihan rangkai.
- **Isian ubin huruf (Kelas 3–4).** Isian tema `varian: "k34"` otomatis dijawab dengan menyusun ubin huruf, bukan papan ketik. Penulis tidak perlu mengubah apa pun. Importer membuat ubinnya (huruf jawaban utama diacak, ditambah 2–4 pengecoh: huruf mirip seperti b/d, versi kapital/kecil lain di tema `kapital`, tanda . ? ! lain bila jawaban bertanda), dan server tetap menilai seperti isian biasa. Jawaban yang bisa diubinkan hanya berisi huruf, apostrof, tanda hubung, spasi, dan . , ? ! dengan panjang ≤12. Jawaban lain (angka, jawaban panjang) otomatis tetap diketik. Ubin hanya cukup untuk jawaban utama, jadi bentuk lain (`do not` untuk `don't`) tetap dinilai benar, tetapi anak menyusun bentuk utamanya. Jadi tulis bentuk yang ingin disusun anak sebagai jawaban utama.
  - Matikan untuk satu isian dengan elemen kelima: `["Ada ___ buku.", "12", "…", [], { ubin: false }]`, atau untuk satu tema dengan `ubin: false`.
  - Tema non-k34 (misalnya k56 atau tema umum yang ramah anak) boleh memakai ubin dengan `ubin: true` di tema atau `{ ubin: true }` di isian. Jawabannya wajib bisa diubinkan, kalau tidak `MISI_CEK` menolak.
- **Kelas 5–6:** rangkai boleh, dengan kalimat ≤6 kata dan uji akhir ≤6 kata. Ikuti semua aturan "ketik harus bisa benar" di brief misi Inggris.
- **Cerita** diperankan di dunia anak: menjawab salam Bu guru, mengeja nama untuk papan tulis, menghitung buku di meja guru, atau berkenalan dengan murid baru.
- **SYARAT:** di dalam bab, tema berikutnya bersandar pada tema sebelumnya. Tema pertama bersandar pada tema bab varian yang sama dari unit prasyarat kanonik, bila bab itu sudah ada. Jangan bersandar pada tema varian jenjang lain. Tema umum boleh dipakai sebagai sandaran bila memang dibutuhkan.
- **KEMAMPUAN:** satu per deck boleh ditulis, dengan id `…-k34-…` dan `needs` tema terakhir varian. Kalimatnya hanya memakai kata di KATA.
- **KATA** hanya perlu diisi kalau ada latihan rangkai (k56). Kata yang sudah ada di file lain tidak ditulis ulang.

## Periksa sebelum selesai
1. `cd titian-web && bun scripts/periksa-kartu.ts jb-` lolos untuk semua deck-mu.
2. `MISI_CEK=1 bun scripts/misi-inggris.ts` tanpa baris masalah.
3. `NODE_OPTIONS=--max-old-space-size=2800 ../agent/tools/batas-ram.sh 3G bunx tsc --noEmit -p .` bersih.
4. Baca ulang setiap soal dengan bertanya: "Bisakah anak Kelas 3 menjawab ini hanya dari mendengar dan kartu yang tadi tampil?"

Jangan menyalakan server atau browser, jangan membuat audio, jangan memanggil AI berbayar, dan jangan menjalankan agen lain. Generator penuh dan importer dijalankan koordinator.

## Laporan (singkat)
Per deck: slug jembatan, jumlah kartu, apa yang ditinggalkan untuk deck lengkap, tema (id, judul, indeks kartu), dan isi kanonik yang menurutmu salah.
