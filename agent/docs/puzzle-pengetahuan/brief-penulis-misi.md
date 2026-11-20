# Brief penulis misi Matematika

Brief ini untuk agen yang menulis misi dari deck kartu kanonik (ADR-0028). Satu agen menulis satu file di `titian-web/scripts/misi-level/`. File lain tidak disentuh, tidak ada commit, dan tidak ada tulis ke database.

## Baca dulu
- `agent/docs/puzzle-pengetahuan/temuan-misi.md`: masalah yang sudah pernah terjadi dan aturannya. Jangan ulangi.
- `agent/docs/adr/0028-misi-bertema-di-atas-kartu-kanonik.md`: apa itu misi.
- `titian-web/scripts/misi-aljabar.ts` dan `titian-web/scripts/misi-level/l04-*.ts`: contoh format BAB, SYARAT, TEMA yang sudah lolos.
- Interface `Tema` dan semua pemeriksaan di `titian-web/scripts/misi-bilangan-bulat.ts`.
- `titian-web/src/components/puzzle/math-pieces.ts` (`mathKey`) dan `math-soal.ts` (`planOf`): kalimat apa yang dimengerti mesin dan bentuk latihan yang didapatnya.
- Deck-nya sendiri, lewat `src/content/kartu/index.ts` (DECKS). Baca SETIAP kartu sampai habis. Daftar kartu materi beserta indeksnya:
  `cd titian-web && bun -e 'import { DECKS } from "./src/content/kartu/index.ts"; import { isExercise } from "./src/content/kartu/types.ts"; const d = DECKS["SLUG"]; d.cards.forEach((c, i) => { if (!isExercise(c)) console.log(i, c.t, (c as any).title) })'`

## Yang ditulis
- Bagi tiap deck menjadi tema mengikuti urutan mengajar deck itu. Satu tema = satu misi. Jumlah tema mengikuti kebutuhan materi: deck yang padat boleh 5 atau 6 tema, deck tipis cukup 2. Biasanya 3 sampai 9 kartu per tema. Setiap indeks kartu materi masuk tepat satu tema.
- Setiap tema: `level` (level file-mu), `id` unik global berawalan level (mis. `l5-akar-sederhana`), `deck`, `judul`, `sub`, `kartu`, `tokoh` [nama Indonesia, satu emoji], `cerita` (1–2 kalimat, situasi nyata di Indonesia yang diselesaikan matematika tema itu), `tujuan`, `pola` (aturan singkat), tepat 3 `tebak` [soal, benar, salah, salah, alasan], minimal 3 `isian` [teks dengan ___, jawaban, penjelasan], dan latihan.
- Kalimat latihan hanya boleh berisi bilangan bulat (boleh negatif), + − × : = < > ( ), ² ³, |x|, dan huruf kecil. Potongan dipisah satu spasi, memakai tanda minus "−" dan "×". TIDAK boleh ada desimal, pecahan, persen, derajat, akar, satuan, atau pasangan koordinat di dalam kalimat ("/" dibaca bagi). Jadi:
  - Arti kalimat latihan (teks di atas soal) tidak boleh menyebut hasil yang harus dicari siswa. Tulis "Lawan dari −4.", bukan "Lawan dari −4 adalah 4.". Pemain misi juga menutup angka jawaban, tapi jangan bergantung padanya.
  - Hitungan bilangan bulat atau identitas aljabar ditulis sebagai `latihan` [kalimat, artinya] (3 sampai 12 potongan), ditambah `pakai` (≥2) dan `target`. Generator menghitung semuanya.
  - Kalimat berhuruf harus berlaku untuk semua nilai huruf. Persamaan dan langkah penyelesaiannya (mis. `2x + 3 = 11`, `2x = 11 − 3`, `x = 4`) boleh, asal tema itu diberi `nilai: { x: 4 }`, dan semua kalimat berhuruf di tema itu benar untuk nilai tersebut. Pertidaksamaan berhuruf tidak didukung: pakai `pilih` atau `isian`.
  - Yang tidak bisa jadi kalimat (akar, pecahan, desimal, notasi ilmiah, membaca grafik, memilih metode, klasifikasi) ditulis sebagai `pilih` [soal, benar, salah, salah, alasan], minimal 4 per tema kalau tanpa latihan. Untuk tema yang hanya pilih: `latihan: []`, `pakai: []`, `target: ["", ""]`. Campuran latihan dan pilih boleh (total ≥ 4). Gambar atau grafik dijelaskan dengan kata di dalam soal.
  - Jawaban `isian` diketik siswa di papan ketik ponsel: pendek, tidak ambigu, dan hanya memakai angka, huruf, koma, minus, garis miring, atau tanda kurung (bilangan, `3/4`, `0,75`, `(2, −3)`, satu kata). Tanpa √, pangkat kecil, ×, atau π di jawaban: taruh simbolnya di teks soal, mis. `√48 = ___√3` dengan jawaban `4`.
- BAB: satu entri per deck {deck, key unik (mis. "l5-akar"), title (judul bab singkat), icon (satu emoji)}.
- KEMAMPUAN: ekspor `export const KEMAMPUAN: Kemampuan[] = [...]` (impor tipe `Kemampuan` dari `../misi-bilangan-bulat`). Satu sampai tiga kemampuan per deck: apa yang bisa dilakukan siswa setelah tema-temanya selesai, ditulis sebagai kegiatan nyata ("Menghitung volume tandon air"). Isi {id unik berawalan level, title, sentence (satu kalimat matematika yang menunjukkannya, aturan sama dengan latihan dan harus benar, atau "" kalau tidak bisa), needs (id tema yang harus selesai)}.
- SYARAT: id tema -> id tema yang langsung dibutuhkan. Jangan menambah prasyarat yang sudah tersirat lewat prasyarat lain di tema yang sama. Di dalam deck ikuti urutan mengajar. Boleh menunjuk tema level sebelumnya yang memang prasyarat (lihat id di `scripts/misi-bilangan-bulat.ts`, `scripts/misi-aljabar.ts`, dan file `misi-level` lain). Batas rantai 12 dihitung per level, jadi prasyarat ke level lain tidak menambah kedalaman.

## Mutu (pemilik ketat)
- Bahasa Indonesia alami seperti tutor yang baik bicara ke siswa level itu. Kalimat pendek. Tanpa basa-basi, tanpa "Yuk, mari kita…", tanpa bahasa Inggris kecuali istilah resminya.
- Matematika tepat. Pilihan salah adalah kekeliruan yang masuk akal (lihat kartu "Yang sering keliru"), tidak asal. Tepat satu jawaban benar; periksa setiap pilihan sendiri.
- Situasi konkret kehidupan Indonesia, bilangan realistis.

## Periksa sebelum selesai (semua harus lolos)
1. `cd titian-web && MISI_CEK=1 bun scripts/misi-bilangan-bulat.ts` mencetak ringkasan tanpa baris masalah. Mode ini hanya memeriksa dan tidak menulis file apa pun.
2. `../agent/tools/batas-ram.sh 3G bunx tsc --noEmit -p .` (dari folder titian-web; tsc memakan ±2 GB, jadi selalu lewat pembatas RAM ini) bersih untuk file-mu.
3. Uji kering importer dijalankan koordinator, bukan oleh agen penulis. Jangan mencoba menjalankannya atau menirunya dengan cara lain.
4. Baca ulang setiap tebak, pilih, dan isian sekali lagi.

Mesin punya RAM 15 GB yang dipakai bersama server dev: jangan menyalakan server atau browser.

## Batas kerja
Kerjakan sendiri. Jangan menjalankan agen atau subagen lain: pemilik membatasi dua agen sekaligus untuk seluruh pekerjaan.

## Laporan (singkat)
Tema per deck (id, judul, indeks kartu), jumlah tebak/pilih/latihan/isian, SYARAT yang dipilih, materi yang belum bisa dilatih dengan baik oleh bentuk yang ada (sebut bentuk latihan yang cocok), dan isi kartu yang menurutmu salah.
