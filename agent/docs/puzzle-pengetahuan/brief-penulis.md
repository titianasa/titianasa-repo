# Brief penulis deck

Untuk agen yang menulis deck **kanonik** dalam produksi massal (`produksi-massal-kartu.md`). Setiap putaran menjalankan 5 penulis bersamaan. Setiap penulis memegang satu tugas: beberapa deck berurutan dari satu tingkat.

Tidak ada pemeriksa yang menunggu hasilmu dalam putaran yang sama. Audit berjalan belakangan, di putaran tersendiri, dan dimulai dari catatanmu. Jadi tulis deck sampai standar penuh, lalu catat dengan jujur apa yang belum bisa kamu pastikan.

## Aturan berkas

Kamu hanya boleh menulis **satu berkas**: `titian-web/src/content/kartu/produksi/<id-tugas>.ts`.

- Jangan mengubah berkas lain: komponen, deck lama, indeks, dokumen, data kanonik, dan git.
- Kalau kamu butuh jenis kartu, lab, atau helper yang belum ada, jangan membuatnya sendiri. Tulis deck dengan yang tersedia, lalu laporkan kebutuhannya.
- Jangan menyalakan server dan jangan membuka browser. Uji tampilan dikerjakan penggabung.

Bentuk berkas:

```ts
import type { Kiriman } from "./jenis";
import { idea, isi, keliru, langkah, pasang, pilih, ringkas, tabel } from "../lengkap/bantu";
import { bar, kisi, bidang, sumbu, koma } from "../lengkap/gambar";

export const KIRIMAN: Kiriman = {
  tulisUlang: {
    "slug-lama": { points: [...], cards: [...] },          // tulis ulang atau perbaiki deck yang ada
  },
  baru: [
    { slug: "slug-baru", unit: "mtk....", kategori: "...", title: "...", sub: "...", emoji: "...",
      points: [...], cards: [...], setelah: "slug-deck-sebelumnya" },  // unit yang belum punya deck
  ],
  catatan: {
    "slug-lama": [{ kartu: "judul kartu", jenis: "tata-letak", isi: "label 4.520 dan 4.530 rapat, cek di 9:16" }],
  },
};
```

Sesudah menulis, jalankan `bun scripts/susun-produksi.ts` di `titian-web`, supaya indeks memuat berkasmu. Penulis lain juga menjalankannya, dan hasilnya selalu sama.

## Langkah per deck

1. **Baca spesifikasi.** Jalankan `bun scripts/spek-deck.ts <slug>`, atau `bun scripts/spek-deck.ts --unit <kunci>` untuk deck baru. Isinya:
   - tingkat dan batas gerbang;
   - prasyarat beserta judul kartu untuk `ingat`;
   - sumber resmi beserta bukti halaman;
   - kalimat Inggris yang sudah berekaman;
   - deck lama;
   - deck contoh.
2. **Baca aturannya.**
   - `standar-kartu-lengkap.md`, terutama bagian "Kanonik dan jalur" dan baris tingkat deckmu.
   - Matematika: prinsip contoh kerja dan latihan di `riset-sd-sma.md` (M8, M14–M24).
   - Bahasa Inggris: aturan per CEFR di `riset-inggris.md` (E4, E5, E10–E21).
   - Batas per kelas dan prabaca di dokumen riset itu untuk deck jalur, bukan untukmu.
   - Baca juga satu deck contoh dari spesifikasi sampai habis untuk meniru bentuknya.
3. **Tulis deck lengkap.** Dari kartu pertama sampai ringkasan, menurut urutan di standar: masalah nyata, `ingat`, konsep dengan gambar atau lab, alasan, contoh kerja, latihan bertingkat, kesalahan khas, ringkasan.
4. **Periksa.**
   - Jalankan `bun scripts/periksa-kartu.ts <slug> ...` (setengah detik) setiap selesai satu deck, sampai lolos.
   - Jalankan `bunx tsc --noEmit -p .` (sekitar 10 detik) sekali di akhir, dan bereskan galat di berkasmu.
   - Hitung ulang sendiri setiap angka yang tidak tertangkap gerbang, misalnya angka di gambar dan di kalimat penjelasan.
5. **Catat.** Isi `catatan` untuk setiap hal yang belum bisa kamu pastikan (lihat "Catatan untuk audit").

## Kanonik, bukan jalur

Deck yang kamu tulis adalah deck **kanonik** (ADR-0026, "kanonik sebagai sumber pengetahuan"):

- **Untuk siapa.** Semua kalangan: orang awam, siswa, guru, dan akademisi. Tulis menurut standar keilmuan dan standar mutu materi. Bahasanya harus bisa diikuti orang awam (kata sehari-hari dulu, setiap istilah diberi arti, setiap langkah diberi alasan), tanpa mengurangi kedalaman dan esensi ilmunya. Jangan menulis untuk "anak Kelas 1" atau "siswa SMA", walaupun spesifikasi menyebut kelas tempat jalur memakai unit itu.
- **Jangan masukkan penyesuaian jalur.** Prabaca, kalimat ekstra pendek untuk anak, catatan pendamping, gaya soal TKA, dan kartu jembatan semuanya milik deck jalur (`kemasan`) dan bukan tugasmu. Jangan menandai deck dengan `prabaca`.
- **Cakupan.** Tuntas menurut ilmunya: semua sub-bagian konsep, kasus khusus, alasan, dan bukti bila ada. Ini lebih penting daripada mengikuti satu buku atau kurikulum. Sumber resmi di spesifikasi dipakai untuk mengecek istilah dan kebenaran, bukan untuk membatasi isi.

## Yang wajib

- **Matematika.**
  - Ikuti baris `mtk` di standar.
  - Setiap latihan diberi `level` (1 paham, 2 terapkan, 3 nalar) dan `konteks` (`matematika`, `personal`, `sosial`, `saintifik`).
  - Contoh kerja ditulis dengan `langkah(...)`, dan setiap langkah diberi alasan.
  - **Contoh memudar (M16):** minimal satu contoh kerja yang 1–2 langkah terakhirnya diisi pembelajar. Beri langkah itu `jawab`, yaitu bagian kunci yang diketik, misalnya `"68"`, dan `terima` untuk bentuk lain yang juga benar. Contoh memudar diletakkan sesudah contoh kerja utuh.
  - **Latihan campuran (M20):** kalau deck punya kartu `ingat`, minimal satu latihan melatih deck sebelumnya. Tandai dengan `dari: "slug-deck"`, dan latihan itu akan tampil dengan label "Ulang · judul deck".
  - **Soal bergambar:** `gambar: { shapes, view }` di latihan menampilkan gambar di atas pertanyaan. Pakai ini kalau soalnya tentang gambar, misalnya sudut atau bangun.
  - **Notasi matematika di teks** (`src/content/kartu/notasi.ts`). Berlaku di semua teks kartu: judul, `say`, langkah, tabel, contoh, soal, pilihan, `why`, `petunjuk`, dan teks gambar. Teks tanpa `@` tampil seperti biasa.
    - `@sigma{k=1}{5} (2k − 1)`: Σ bertumpuk, batas atas 5 dan batas bawah k=1; sukunya ditulis biasa sesudahnya.
    - `@mat[1 2; 3 4]`: matriks bertumpuk dalam kurung siku, baris dipisah `;`. `@mat(3; 4)` memakai kurung biasa (vektor kolom), `@mat|a b; c d|` garis tegak (determinan), `@mat[2 1 | 14; 1 1 | 9]` matriks diperbesar dengan garis pemisah. Sel dipisah spasi; operator berspasi menyatukan sel (`@mat[ad − bc 0; 0 ad − bc]`), dan sel yang berisi spasi lain dipisah `&` atau dua spasi (`@mat[cos θ & −sin θ]`).
    - `0,1@bar{6}`: garis atas di atas angka yang berulang. `@vec{AB}`: panah di atas AB (vektor, bukan ruas garis). `@log{2} 8`, `@log{1/2} x`: basis kecil di kiri atas, pecahan ditulis bersusun.
    - Jawaban isian dibandingkan dalam bentuk polosnya: matriks menjadi `[1 2; 3 4]`, panah vektor diabaikan. Teks gambar bernotasi nggak bisa memakai `stabilo`, `bagian`, `tanda`, `coretBagian`, `coretLagi`, atau `ganti`; gerbang memeriksanya, juga notasi yang salah tulis dan matriks yang barisnya nggak sama panjang. Selang ditulis tanpa notasi: [1; 2].
    - Di teks gambar, garis atas dan basis log tetap teks SVG biasa; sigma, matriks, dan panah vektor digambar sebagai HTML seukuran barisnya. Matriks bertumpuk lebih tinggi dari satu baris, jadi beri jarak tegak sekitar 1,3 × ukuran huruf per baris matriks.
  - **Kartu bersusun** `{ t: "susun", title, op: "tambah" | "kurang" | "kali" | "bagi", a, b, say }`: bilangan ditulis dengan koma, misalnya `{ t: "susun", title: "Bersusun: 5 − 2,36", op: "kurang", a: "5", b: "2,36" }`. Kolom nilai tempat, nol pelurus (pudar), simpanan (merah muda) yang naik, pinjaman (ungu) yang mencoret angka, baris parsial perkalian, porogapit dengan nol tambahan, dan keterangan tiap langkah dihitung kode (`src/content/kartu/susun.ts`). Maks 11 kolom dan 13 baris; pembagian harus habis dalam 3 angka tambahan. Letakkan sesudah contoh kerjanya.
  - **Garis bilangan.** Kartu `jump` dengan `tanpaLabel: true` nggak memberi +3 atau −3 di atas lompatan, tetapi menamai titik berhentinya; pakai untuk letak bilangan, bukan penjumlahan. Latihan `line` dengan `langkah: 0.1` (atau 0.01) menjadi garis desimal: `{ t: "line", q: "Ketuk 0,7 di garis ini", range: [0, 1], langkah: 0.1, start: 0, answer: 0.7, why }`. Tetap maks 13 titik.
  - Minimal 3 contoh kerja dan 8 latihan bertingkat. Latihan pertama diletakkan sesudah contoh kerja pertama.
  - Soal `multi` (PG kompleks) dan `bs` (benar/salah) boleh dipakai bila cocok dengan materinya, tetapi tidak wajib.
- **Gambar dan lab.** Gambar harus sesuai skala angkanya. Topik geometri, grafik, data, dan peluang wajib bergambar atau memakai lab.
  - Lab yang cocok untuk deck kanonik: `statistik`, `peluang`, `vektor`, `turunan`, `integral`, `transformasi`, `regresi`, `proyeksi`, `kerucut`, `luas-antara`, `garis-waktu`, `pasangan-minimal`, `pythagoras`, `bukti-pythagoras`, `garis`, `parabola`, `sudut`, `gelombang`, `timbangan`, `preposisi`, juga `bingkai`, `potong`, `puluhan`, `jam`, `ukur`, `piktogram`, `bentuk`, dan `pola` bila memang menjelaskan konsepnya.
  - Parameternya ada di `src/content/kartu/types.ts` (`LabSpec`).
  - Lab baru: `luas-antara` (luas di antara dua kurva, `{ f, g, a, b }` dengan koefisien polinom, suku tetap dulu).
  - **Peragaan mulai dari nilai deck.** Pythagoras, gelombang, garis, parabola, sudut, dan vektor memulai peragaan dari nilai di spec. `peragaan: [{}, { c: -3, teks: "c turun, parabola turun" }, ...]` memilih langkahnya sendiri. Langkah pertama `{}`, dan `teks` menjadi keterangan di bawah gambar. Tanpa `peragaan`, lab mengubah satu nilai saja.
  - **Opsi tampilan.** Isinya `tampil` (tambah baris atau tanda) dan `sembunyi` (buang angka yang belum diajarkan):
    - garis: `sembunyi: ["gradien"]`, `tampil: ["potong-x", "y-positif"]`.
    - parabola: `tampil: ["range", "akar-kompleks"]`, `sumbu: ["r", "y"]`.
    - sudut: `tampil: ["identitas", "garis-c"]`, `sembunyi: ["tan"]`, `batas: [0, 90]`, `c`.
    - vektor: `sembunyi: ["jumlah", "dot", "sudut"]`, `tampil: ["proyeksi"]`, `mode: "kombinasi"` (s·a + t·b dengan rentangnya).
    - statistik: `sembunyi: ["median", "kotak", "jak"]`, `tampil: ["jangkauan", "pencilan", "ragam"]`, `pembagi: "n-1"`, `banding: { data, nama }` (data kedua pada skala yang sama).
    - regresi: `tampil: ["uji", "residu"]` (SE, t, p, plot residu).
  - **Opsi lab lain.**
    - pythagoras: `tampil: ["akar-sederhana"]`.
    - gelombang: `h` (geser fase; A boleh negatif).
    - turunan: `sumbu: ["t", "x"]`.
    - integral: `aturan: "simpson"`, `mode: "akumulasi"`.
    - timbangan: `pilih: true` (pembelajar memilih operasinya sendiri).
    - bentuk: `bahasa: "en"` (nama bentuk circle, square, triangle, rectangle untuk deck kosakata Inggris; hitungan diucapkan dengan klip angka Inggris).
  - **Lab baru B3.**
    - `pohon-ekspresi` (lab-ekspresi.tsx): pohon kalimat matematika; pembelajar mengetuk operasi yang kedua angkanya siap dan cabangnya menjadi nilai, peragaan mengikuti urutan kurung, kali-bagi, tambah-kurang. `{ k: "pohon-ekspresi", ekspresi: "30 − (2 + 3) × 4 + 6 : 2" }`. Pakai bilangan cacah dan pembagian yang habis.
    - `batang-inggris` (lab-inggris.tsx): diagram batang yang batangnya diubah dengan + dan −, dan kalimat Inggris more, fewer, as many as, the most, the least yang ikut berubah. `{ k: "batang-inggris", judul: "How do students get to school?", satuan: "students", data: [{ nama: "walk", kerja: "walk", benda: "walking", nilai: 6, warna: 4 }, ...], maks: 20 }`. `kerja` mengisi More students ___ than ___, `benda` mengisi ___ is the most popular, `warna` sama dengan warna batang di gambar deck.
  - **Lab bilangan, pecahan, dan rasio** (`lab-bilangan`, `lab-hitung`, `lab-ubin`, `lab-pecahan`, `lab-ruang-satuan`). Semua mulai dari nilai spec; yang memakai `peragaan` ditandai.
    - `garis-bilangan`: titik yang melangkah di garis bilangan bulat. `mode` `tambah` (mulai a, langkah b), `kurang` (a + (−b) di atas garis dan langkah dari b ke a di bawahnya), `kali` (a lompatan b dari nol, dicerminkan di nol kalau a negatif), atau `mutlak` (tombol lawan, nilai mutlak, jarak). `batas` mengunci ujung garis; ada `peragaan`. Contoh: `{ k: "garis-bilangan", mode: "kurang", a: 5, b: -3, batas: [-12, 12] }`.
    - `rentang-taksiran`: a + b, a − b, atau a × b dibulatkan ke bawah dan ke atas menurut angka depannya; hasil tepat terjepit di pita kuning, taksiran terdekat ikut tampil; ada `peragaan`. Contoh: `{ k: "rentang-taksiran", op: "kali", a: 48, b: 21 }`.
    - `supremum`: A = {s − c/n} (`bentuk: "barisan"`) atau selang (s − c, s) (`"interval"`) dengan penggeser ε; anggota yang melewati s − ε hijau, strip bawah memperbesar sekitar s; ada `peragaan` untuk `eps`. Contoh: `{ k: "supremum", bentuk: "barisan", s: 1, c: 1, eps: 0.3 }`.
    - `keping`: keping +1 dan −1 untuk a + b; pasangan nol dipasangkan lalu dibuang; ada `peragaan`. Contoh: `{ k: "keping", a: -3, b: 5 }`.
    - `larik`: n benda dibagi ke banyak baris yang dipilih pembelajar; isi tiap baris, sisa, dan faktor yang ketemu. Contoh: `{ k: "larik", n: 12, baris: 5 }`.
    - `larik-sifat`: larik a baris × b kolom yang dipotong sesudah kolom `potong` (distributif) dan diputar seperempat putaran (komutatif). Contoh: `{ k: "larik-sifat", a: 4, b: 13, potong: 10 }`.
    - `model-luas`: a × b (sampai 999 × 99) sebagai luas yang dipotong menurut nilai tempat, diisi bagian demi bagian di samping perkalian bersusunnya. Contoh: `{ k: "model-luas", a: 47, b: 23 }`.
    - `petak`: bangun di atas petak, satu teks per baris: `#` petak utuh, `.` kosong, `◣ ◢ ◤ ◥` setengah petak (sudut tempat bagian yang terisi). Pembelajar mengetuk petak untuk menutupnya; setengah petak dipasangkan dua-dua. Contoh: `{ k: "petak", petak: ["◣...", "#◣..", "##◣.", "###◣"] }`.
    - `kotak-seratus`: n dari 100 kotak, tampil sebagai pecahan paling sederhana, desimal, dan persen sekaligus; ada `peragaan` untuk `n`. Contoh: `{ k: "kotak-seratus", n: 45 }`.
    - `bagi-balok`: a : b (a sampai 999, b dari 2 sampai 6) dengan balok ratusan, puluhan, satuan; dibagi per tempat, sisanya ditukar 1 = 10 tempat berikutnya. Contoh: `{ k: "bagi-balok", a: 72, b: 3 }`.
    - `porogapit`: pembagian bersusun a : b (b sampai 99); pembelajar mengetuk angka hasil bagi tiap tempat dan diberi alasan kalau terlalu besar atau terlalu kecil. Contoh: `{ k: "porogapit", a: 756, b: 6 }`.
    - `bagi-rata`: n benda (sampai 30) dibagikan satu per satu ke 2–6 piring; sisa yang nggak cukup satu putaran tetap di atas. Contoh: `{ k: "bagi-rata", n: 12, piring: 3, benda: "🍬" }`.
    - `ubin-faktor`: ax² + bx + c (a = 1 atau bilangan prima, b dan c positif) disusun menjadi persegi panjang (ax + p)(x + q); pembelajar memilih lajur kanan dan bawah. Contoh: `{ k: "ubin-faktor", a: 2, b: 7, c: 3 }`.
    - `ubin-lengkap`: x² + bx + c dilengkapkan: pita bx dibelah, satu diputar ke bawah, pojok (b/2)² diisi dari konstanta. Contoh: `{ k: "ubin-lengkap", b: 6, c: 5 }`.
    - `ubin-kurang`: (p) − (q), masing-masing [koefisien x, konstanta]; ubin kurung kedua berbalik warna, lalu pasangan nol dibuang. Contoh: `{ k: "ubin-kurang", p: [5, 2], q: [3, -4] }`.
    - `pecahan-batang`: dua batang pecahan dengan penggeser pembilang dan banyak potong, tombol samakan penyebut; ada `peragaan`. Contoh: `{ k: "pecahan-batang", a: [2, 3], b: [3, 5] }`.
    - `bagi-pecahan`: a ÷ b sebagai menakar: berapa kali takaran b muat di a, dan sisanya sebagai bagian dari satu takaran. `satuan` opsional. Contoh: `{ k: "bagi-pecahan", a: [2, 1], b: [3, 4], satuan: "m" }`.
    - `persen-batang`: batang 0–100% di atas garis 0–`total`, penggeser persen; `mode: "diskon"` mewarnai potongan dan yang dibayar, `rupiah: true` menulis Rp. Contoh: `{ k: "persen-batang", total: 80000, persen: 30, rupiah: true }`.
    - `rasio-ganda`: garis bilangan ganda rasio a : b dengan pengali 0 sampai `kali` (bawaan 5) berlangkah `langkah` (bawaan 0,5; pakai 1 untuk benda yang nggak bisa dibagi dua), dan grafik garis lurus lewat nol. Contoh: `{ k: "rasio-ganda", a: 1, b: 4000, nama: ["banyak buku", "harga (Rp)"], kali: 8, langkah: 1 }`.
    - `luas-tetap`: persegi panjang berluas `hasil`; lebar digeser, tinggi menyesuaikan, titik berjalan di kurva y = hasil/x. Contoh: `{ k: "luas-tetap", hasil: 24, lebar: 4, nama: ["tukang", "hari"] }`.
    - `peta-skala`: peta 1 : `skala` dengan A–B sejauh `cm`; penggaris digeser, peta diperbesar 2× dan skala garisnya ikut memanjang. Contoh: `{ k: "peta-skala", skala: 200000, cm: 5 }`.
    - `jarak-waktu`: grafik jarak terhadap waktu dengan penggeser kecepatan dan segitiga naik dalam 1 jam; `v2` garis pembanding. Contoh: `{ k: "jarak-waktu", v: 60, jam: 3, v2: 20 }`.
    - `piktogram-skala`: piktogram dengan 1 simbol = `skala`, tombol mengganti skala (`pilihan`, bawaan 2, 5, 10), sisa digambar sebagai potongan simbol. Contoh: `{ k: "piktogram-skala", kategori: [["Senin", "🥚"], ["Selasa", "🥚"]], data: [40, 25], skala: 10 }`.
    - `kubus-satuan`: tumpukan kubus dari denah angka (baris belakang dulu) di gambar miring tetap; petak denah diketuk untuk menambah atau mengambil kubus, volume dan tampak depan, kanan, atas dihitung. `maks` tinggi tumpukan (bawaan 4). Contoh: `{ k: "kubus-satuan", denah: [[1, 3, 2], [2, 1, 1]] }`.
  - **Lab peluang dan pencacahan** (`lab-peluang`). Semua mulai dari nilai spec dan nggak memakai angka acak.
    - `persegi-peluang`: persegi satuan; kolom A selebar P(A), B mengisi P(B | A) di dalam A dan P(B | Aᶜ) di luar A; luas ungu P(A ∩ B) dibandingkan dengan P(A) × P(B). `b` satu angka = saling bebas, `b: [P(B | A), P(B | Aᶜ)]` mulai di mode bergantung. Contoh: `{ k: "persegi-peluang", a: 0.6, b: 0.5 }`.
    - `pohon-kantong`: dua ambilan dari kantong `isi` = [warna pertama, warna kedua], dengan atau tanpa pengembalian (`kembali`); pecahan tepat di setiap cabang dan jalur, jumlah jalur 1. `nama` label pendek, `warna` indeks palet. Contoh: `{ k: "pohon-kantong", isi: [3, 2], nama: ["K", "B"], warna: [4, 0] }`.
    - `pohon-bayes`: pohon dua tahap P(A) = `p`, P(B | A) = `ya`, P(B | Aᶜ) = `tidak`; peluang total P(B) dan Bayes P(A | B); tombol mode frekuensi dengan `orang` kejadian (bawaan 1.000), `frekuensi: true` mulai di mode itu. `nama` [A, B, Aᶜ, Bᶜ]. Contoh: `{ k: "pohon-bayes", p: 0.3, ya: 0.4, tidak: 0.1, nama: ["H", "T", "Hᶜ", "Tᶜ"] }`.
    - `isi-tempat`: kotak pengisian tempat untuk bilangan 2–4 angka dari `angka`; `ulang` boleh berulang, `syarat` satuan genap atau ganjil; 0 nggak boleh di depan, kotak bersyarat diisi dulu (nomor urut), genap dengan 0 dipecah dua kasus; tombol mengganti pengulangan, syarat, dan angka 0. Contoh: `{ k: "isi-tempat", angka: [1, 2, 3, 4, 5], tempat: 3 }`.
    - `cacah-susunan`: semua susunan r huruf dari A… (n sampai 5, r sampai 3), lalu dikelompokkan menjadi kombinasi (setiap kelompok muncul r! kali); `mode: "melingkar"` menyusun n (sampai 4) orang di meja bundar dan mengelompokkan putarannya. Contoh: `{ k: "cacah-susunan", n: 4, r: 2 }`.
  - **Lab lingkaran** (`lab-lingkaran`). Semua mulai dari nilai spec; yang memakai `peragaan` ditandai.
    - `busur-juring`: juring bersudut `sudut`° dan berjari-jari `r` dengan penggeser θ dan r; bagian θ/360 dari keliling (busur, merah muda) dan dari luas (juring, biru), π = 22/7 kalau r kelipatan 7, selain itu 3,14. `radian: true` menulis θ dalam radian, busur r × θ dan juring ½r²θ dalam kelipatan π, dengan tanda 1–6 rad di tepi. `rMaks` (bawaan 21), `satuan` (bawaan cm); ada `peragaan`. Contoh: `{ k: "busur-juring", sudut: 90, r: 14 }`.
    - `sudut-keliling`: A, B, C pada lingkaran (sudut dalam derajat, berlawanan jarum jam dari kanan). C diseret atau digeser keliling lingkaran; busur yang dihadap hijau, sudut pusat biru (refleks kalau C di busur kecil), ∠ACB merah muda selalu setengahnya. Penggeser kedua mengubah busur AB. Contoh: `{ k: "sudut-keliling", a: 200, b: 340, c: 80 }`.
    - `potong-lingkaran`: lingkaran dipotong n juring (genap, 4–48); penggeser susun menggeser dan memutar juring ke susunan berselang di samping kotak πr × r, alas lurus n·sin(180°/n)·r ikut dihitung; ada `peragaan` untuk `n`. Contoh: `{ k: "potong-lingkaran", n: 12 }`.
    - `konstruksi-segitiga`: segitiga di atas alas AB = `ab` dari S-S-S (`ac`, `bc`), S-Sd-S (`sudut` di A, `ac`), atau S-S-Sd (`sudut`, `bc`: nol, satu, atau dua segitiga); `mode` adalah mode awal dan tombolnya bisa diganti; ada `peragaan` (boleh berganti `mode`). Contoh: `{ k: "konstruksi-segitiga", mode: "ssa", ab: 6, ac: 5, bc: 4, sudut: 30 }`.
  - Warna gambar memakai indeks palet 0 biru, 1 merah muda, 2 hijau, 3 ungu, dan 4 kuning. Kalau teks menyebut warna, warnanya harus sesuai.
- **Animasi dan interaksi.** Lihat bagian "Animasi dan interaksi" di bawah. Setiap lab wajib punya `petunjuk`.
- **Bahasa Inggris.**
  - Pakai British English, dengan urutan dan isi sesuai CEFR dan rujukan standarnya.
  - Utamakan kalimat dari daftar berekaman di spesifikasi.
  - Panjang kalimat contoh mengikuti level CEFR (E4). Jenis latihan dan panjang kalimat latihan (E12) bebas di deck kanonik: pilih latihan yang paling melatih konsepnya, termasuk `fix` dan `arrange` di level awal. Pembatasan E12 hanya berlaku di deck jalur (kemasan).
  - Kesalahan khas pembelajar Indonesia ditulis beserta sebabnya (E16–E17).
  - Soal tentang teks dengar atau teks bacaan: beri `dengar: [{ who, en }, ...]` (baris yang sama dengan kartu `audio`-nya) supaya soal bisa memutar ulang audionya, atau `bacaan: { judul, teks }` supaya teksnya bisa dibuka di atas soal. Soal seperti ini jangan bergantung pada ingatan dari kartu sebelumnya. Sebagian sudah otomatis (`lengkap/rapi.ts`): soal pilihan, isian, dan benar-salah dalam dua kartu sesudah kartu `audio` mendapat `dengar` dari kartu itu, kecuali soal yang membawa kalimatnya sendiri atau situasi baru (Temanmu bilang:). Soal yang menyebut teks bacaan dengan namanya (Menurut teks Bamboo, Di Email dari Lombok, Teks 1) mendapat `bacaan` dari kartu `examples` berjudul Teks: …, Teks N: …, Cerita: …, atau Email …. Jadi beri judul teks bacaan dengan pola itu, dan sebut nama teksnya di soal.
  - **Latihan dengar dan susun** (B3, 2026-11-08). Klip harus ada di rekaman game (gerbang memeriksa E2).
    - Dengar lalu pilih: `klip` di soal `choice` (atau `multi`) memutar satu baris berekaman lewat tombol besar; teksnya baru tampil di jawaban. `{ t: "choice", q: "Dengarkan, lalu ketuk angka yang kamu dengar", klip: "sixteen", options: ["60", "16"], answer: 1, why }`. Pilihan boleh angka, kata, atau panah nada ↘ ↗ ↘↗.
    - Ketuk kata bertekanan sambil mendengar: `klip` di soal `spot`, kata bertekanan ditandai `**`: `{ t: "spot", q: "Dengarkan, lalu ketuk kata yang ditekan", klip: "Yes, I can.", sentence: "**Yes**, I **can**.", why }`.
    - Ubin: `{ t: "ubin", q, ubin: ["n", "igh", "t", "i", "ie"], answer: ["n", "igh", "t"], klip: "night", why }`. Ubin bisa huruf (ejaan nama), angka (nomor telepon), atau pola ejaan; beri 1–3 ubin pengecoh. `sentence` dengan ___ menampilkan jawaban yang tersusun di celahnya. Yang dinilai ejaan yang tersusun, bukan urutan ubin.
    - Formulir: `{ t: "formulir", q, judul: "Evening English course", dengar: [{ who, en }, ...], isian: [{ label: "Classes", answer: "twice a week", accept: ["2x a week"] }, ...], why }`. Minimal dua kotak; isinya dari `dengar` (atau `bacaan`), dan tombol putarnya ada di atas formulir.
    - Bingkai frasa: `{ t: "frasa", q: "Bingkai frasa subjeknya", sentence: "**The rising price of cooking oil** worries many families.", why }`. Pembelajar mengetuk kata pertama lalu kata terakhir frasa yang ditandai `**`.
    - Sortir berisian: item `sort` boleh punya isian ketiga, kalimat lengkapnya, yang tampil di keranjang begitu item masuk: `["Seldom ___ (she / complain).", 0, "Seldom does she complain."]`.
    - Rekam suara: `{ t: "rekam", title, naskah: "FIRST, | I missed the BUS. ||", model: ["First, I missed the bus."], detik: 30, petunjuk, say }`. Naskah memakai `|` untuk jeda, `**kata**` atau KAPITAL untuk tekanan, dan ↗ ↘ untuk nada; `model` diputar sebagai contoh dan harus berekaman. Rekaman dibuat di peramban dan nggak diunggah; di film hanya naskah dan contohnya yang tampil.
  - Latihan `type` mengabaikan huruf besar dan kecil. Kalau yang dilatih justru huruf kapital (nama hari, nama orang, I), beri `kapital: true`: jawaban harus sama persis, dan ubin huruf memuat huruf kecilnya sebagai pengecoh.
- **Bahasa penjelasan.** Pakai "kamu" dan "nggak". Jangan memakai frasa terlarang di standar, jangan memakai tanda pisah panjang, dan jangan menulis kalimat umum yang bisa ditempel di bab apa pun. Contoh harus terasa Indonesia.
- **Kartu `ingat`.** Isinya harus merujuk judul kartu persis seperti tercantum di spesifikasi.
- **Penjelasan jawaban.** Jelaskan cara berpikirnya, minimal satu kalimat utuh. Jangan menyebut posisi pilihan, misalnya "pilihan pertama".

## Animasi dan interaksi

Animasi dirancang per kartu, sesuai konsep yang dijelaskan kartu itu. Tidak ada pola baku. Pertanyaannya selalu: apa yang harus dilihat pembelajar terjadi, dan dalam urutan apa?

**Kapan gambar bergerak.**
- Konsepnya proses atau perubahan: membilang satu per satu, mengelompokkan sepuluh, meminjam dan menyimpan, titik bergeser di garis bilangan, bangun diputar atau dicerminkan, grafik bergeser, sebelum dan sesudah.
- Ada kesalahan yang dibetulkan: langkah salah dicoret, lalu yang benar muncul.
- Ada bagian yang harus dikaitkan dengan kalimat: angka atau sisi yang sedang dibahas disorot.

**Kapan gambar diam.** Gambar dibaca sebagai rujukan dengan kecepatan sendiri, misalnya diagram berlabel, bangun dengan ukurannya, atau tabel. Gerak yang tidak menjelaskan apa pun hanya mengganggu.

**Cara menulisnya** (`FigureShape` dan kartu `figure` di `types.ts`):
- Gambar berjalan dalam tahap 0, 1, 2, dan seterusnya. Bentuk tanpa tanda tahap hadir sejak awal.
- `muncul: n` membuat bentuk masuk di tahap n. Garis, kurva, dan polyline terbuka menggambar dirinya sendiri, sedangkan bentuk lain memudar masuk.
- `dari: [dx, dy]` membuat bentuk bergeser masuk dari posisi itu ke tempatnya, misalnya benda masuk ke kelompok. Beri daftar, `dari: [[dx1, dy1], [dx2, dy2], ...]`, untuk beberapa sumber yang berkumpul menjadi satu: satu salinan meluncur dari setiap asal dan semuanya melebur menjadi bentuk itu. Contohnya kalimat utama yang terkumpul dari empat baris. Daftar `dari` butuh `muncul`.
- `sorot: [n, ...]` membuat bentuk berdenyut di tahap itu. Pakai untuk bagian yang sedang dibicarakan keterangan.
- `coret: n` mencoret teks di tahap n. `hilang: n` membuat bentuk memudar keluar.
- `coretBagian: [a, b]` bersama `coret` mencoret hanya huruf ke-a sampai sebelum ke-b dalam satu teks, misalnya "which" di tengah kalimat. Hitung a dan b dari posisi huruf di string (`s.indexOf("which")`), jangan ditebak. Lebarnya ditaksir dari jumlah huruf, jadi pakai untuk kata utuh, bukan satu huruf. Untuk mencoret beberapa bagian di tahap berbeda, tambahkan `coretLagi: [[tahap, a, b], ...]` pada teks yang sama; jangan menumpuk salinan teks.
- **Bagian dari satu teks.** Teks dengan salah satu tambahan berikut diukur dari huruf yang benar-benar tampil di layar, jadi posisinya tepat sampai satu huruf. Hitung indeks huruf dengan `s.indexOf(...)`, jangan ditebak.
  - `stabilo: [[tahap, a, b], ...]` memberi stabilo kuning di belakang huruf a sampai sebelum b mulai tahap itu. Angka keempat, `[tahap, a, b, sampai]`, mencabutnya di tahap `sampai`. Pakai untuk menyorot kata di tengah kalimat, misalnya hanya Monday, because, Tuesday, dan to 8 p.m. di pengumuman.
  - `ganti: [[tahap, "teks baru"], ...]` mengganti kata-kata teks di tempatnya pada tahap itu, dengan pudar silang. Contohnya murky menjadi keruh.
  - `bagian: [{ a, b, ...gerak }, ...]` menjadikan huruf a sampai sebelum b bentuk sendiri, sementara sisa barisnya tetap di tempat dan menyisakan celahnya. Potongan boleh diberi `pindah` (termasuk `tuju` dan `lengkung`), `muncul` (dengan `dari` supaya potongan meluncur masuk lalu mendarat tepat di tempatnya sendiri dalam baris), `hilang`, `sorot`, `coret`, `color`, dan `ganti`. Contohnya unforgettable yang terbelah menjadi un, forget, dan able, huruf -s yang pindah dari does ke leave, atau kata prosa yang pindah ke baris puisinya. Untuk mencoret satu huruf saja, jadikan huruf itu `bagian` dengan `coret`.
  - `tanda: [{ pada, jenis, a, b, c }, ...]` menggambar tanda koreksi BS 5261 berwarna merah di teks: `sisip` (caret di bawah celah sebelum huruf a), `hapus` (garis coret dengan tegak di kedua ujung, huruf a sampai sebelum b), `tukar` (garis di atas bagian a..b dan di bawah bagian b..c, menyilang di antaranya), dan `biarkan` (titik-titik di bawah huruf a sampai sebelum b, membatalkan koreksi).
- `langkah: [...]` di kartu berisi keterangan untuk setiap tahap, satu untuk tiap tahap mulai dari 0. Setiap tahap punya satu tugas, dan keterangannya menyebut tugas itu.
- `ketuk: true` membuat pembelajar memajukan tahap sendiri. Pakai ini kalau pembelajar sebaiknya menebak dulu sebelum melihat tahap berikutnya. Tanpa `ketuk`, gambar berjalan sendiri. `tempo` mengatur milidetik per tahap (bawaan 1400).
- `putar: { pada, sudut, pusat }` membuat bentuk berputar ke tempatnya di tahap `pada`. Sebelum tahap itu, bentuk terputar `sudut` derajat searah jarum jam di sekitar `pusat`. Contohnya lengan timbangan yang miring lalu datar, atau sudut segitiga yang disobek lalu diputar ke samping sudut lain. Untuk berputar bertahap, beri daftar: `putar: [{ pada: 2, sudut: -6, pusat }, { pada: 4, sudut: -6, pusat }]`. Gambarlah bentuknya di posisi **akhir**. Sebelum tahap pertama, bentuk terputar sebesar jumlah semua `sudut`, dan setiap tahap melepas sudutnya sendiri. Contohnya palang yang mula-mula datar lalu makin miring setiap kali argumen datang: gambar palang di kemiringan terakhir. Satu objek tetap berarti satu putaran ke tempatnya, sama seperti dulu.
- `lipat: { pada, sumbu, di }` membuat bentuk melipat ke tempatnya. Sebelum tahap `pada`, bentuk berupa bayangan cerminnya terhadap garis x = `di` (`sumbu: "tegak"`) atau y = `di` (`"datar"`). Pakai untuk jaring-jaring yang dilipat atau pencerminan. Untuk melipat di garis miring, tulis `lipat: { pada, garis: [[x1, y1], [x2, y2]] }`, misalnya jajargenjang dilipat di diagonalnya. `lipat` juga boleh berupa daftar, dibaca seperti daftar `putar`.
- `tumbuh: { dari, arah }` membuat bentuk tumbuh dari titik `dari` saat muncul, menurut sumbu y, x, atau keduanya. Contohnya batang diagram yang naik dari sumbu.
- `pindah: { pada, ke: [dx, dy] }` menggeser bentuk yang sudah tampil sejauh `ke` di tahap `pada`. Bentuknya sama, bukan diganti salinan. Contohnya koma desimal yang bergeser dua tempat atau ubin aljabar yang dikumpulkan. Untuk gerak berkali-kali, beri daftar: `pindah: [{ pada: 1, ke: [0, -10] }, { pada: 2, ke: [20, 0] }, { pada: 3, ke: [0, 10] }]`; tiap `ke` dihitung dari posisi sesudah gerak sebelumnya. Pakai untuk cakram Hanoi yang diangkat, digeser, lalu diturunkan, pejalan yang berbelok di peta, atau grafik yang digeser dua langkah. Jangan lagi memakai salinan yang menghilang dan muncul.
  - `lengkung: n` di satu langkah membuat geraknya melengkung sejauh n satuan ke kiri arah geraknya: ke atas untuk gerak ke kanan, ke bawah untuk gerak ke kiri. Jadi dua bentuk yang bertukar tempat dengan `lengkung` yang sama saling melewati, nggak bertabrakan di satu garis. Contoh: `pindah: { pada: 2, ke: [20, 0], lengkung: 6 }`.
  - `tuju: [x, y]` menggantikan `ke`: bentuk pergi ke titik itu, bukan sejauh itu. Yang mendarat di titik itu adalah titik acuan bentuk: `at` untuk teks dan titik, pusat untuk lingkaran, tengah kotak batas untuk poly, curve, dan line, dan ujung kiri untuk potongan teks (`bagian`). Pakai untuk kata yang pindah ke baris lain atau benda yang mendarat di tempat tertentu.
  - `kitar: { pusat: [x, y], sudut }` menggantikan `ke`: bentuk berkeliling `pusat` sejauh `sudut` derajat searah jarum jam dan tetap tegak. 360 berarti satu putaran penuh. Contohnya penanda yang mengelilingi tujuh hari, lalu langkah berikutnya `sudut: 5 * 360 / 7` untuk lima hari lagi.
  - `balik: true` membuat bentuk maju sejauh `ke` lalu kembali di tahap yang sama, seperti mencoba masuk lalu ditolak. Contohnya cooking yang mencoba masuk ke slot sesudah want lalu terpental.
  - Setiap langkah memakai tepat satu dari `ke`, `tuju`, atau `kitar`; gerbang memeriksanya.
- `jadi: [{ pada, pts }, ...]` mengubah bentuk poly, curve, atau line (`pts: [a, b]`) menjadi titik-titik `pts` di tahap `pada`, dengan banyak titik yang sama seperti bentuk asalnya. Bentuknya sama, berubah perlahan, bukan diganti salinan. Contohnya senar yang bergetar, pegas yang memanjang dan memendek (`pegas(a, b)` dari `lengkap/gambar` selalu memberi banyak titik yang sama), persegi yang menjadi jajargenjang, sisi jaring-jaring yang membuka dari balok, atau garis selidik yang bergeser sejajar dan tetap terpotong kotak bidang (hitung ujungnya di tepi kotak untuk setiap tahap).
- **Gambar ruang (3D).** Belum ada kamera 3D di kartu gambar. Gambar benda dalam proyeksi miring yang tetap, lalu pakai `jadi` untuk sisi yang membuka atau benda yang berputar, `pindah` untuk bagian yang keluar lalu kembali, dan `circle` dengan `ry` untuk lingkaran yang terlihat miring. Lab ruang yang bisa diputar adalah pekerjaan lab, bukan animasi.
- `tebal: 2` mempertebal garis, misalnya jarum jam pendek.
- `arrow: true` memberi ujung panah pada `line`, dan juga pada `curve`: panahnya mengikuti arah dua titik terakhir kurva. Pakai untuk lompatan di garis bilangan, busur langkah, atau arah gerak "over".
- `circle` dengan `ry` menjadi elips: `r` lebar mendatar, `ry` tinggi tegak. Pakai untuk tutup tabung atau lingkaran yang dilihat miring.
- `path` dengan `d` (data path SVG) dipakai helper `lengkap/gambar` untuk gambar yang nggak bisa dibuat rapi dari bentuk lain. `isi: true` mengisinya dengan warnanya. Penulis sebaiknya memakai helpernya, bukan menulis `d` sendiri. `tuju` dan `kitar` nggak berlaku untuk `path`.
- Helper gambar di `lengkap/gambar`. Yang menggambar mengembalikan `FigureShape[]` yang bisa diberi tahap; `busur` dan `pegas` mengembalikan titik:
  - `busur(c, r, dari, sampai)`: titik-titik busur lingkaran atau elips, untuk `curve` atau target `jadi`. `panahPutar(c, r)`: panah melingkar, misalnya siklus x ∈ y ∈ x.
  - `awanHujan(c, lebar, { awan, hujan })`: awan kelabu dengan tetes hujan, masing-masing bisa punya tahap sendiri.
  - `jendela(x, y, w, h, buka)`: jendela dengan dua daun yang terbuka ke luar di tahap `buka`.
  - `timbangan(poros, lengan, [{ pada, sudut }, ...])`: timbangan yang miring bertahap. Hasilnya `{ shapes, kiri, kanan, piringKiri, piringKanan }`: beri `pindah: kiri` (atau `kanan`) ke benda di atas piring supaya ikut naik turun.
  - `pai3d(c, rx, ry, tebal, [{ nilai, color }, ...])`: diagram lingkaran miring dengan dinding samping, untuk menunjukkan juring depan yang tampak lebih besar.
  - `pegas(a, b, lilitan)`: titik-titik pegas zigzag dengan banyak titik tetap.
  - `unggahan(x, y, w, { akun, foto, caption, hashtag, komentar }, gerak)`: tiruan unggahan media sosial (akun, foto, caption, hashtag, komentar, balasan menjorok), dengan tahap per bagian. Hasilnya juga memberi `baris` (y tiap bagian) untuk label di sampingnya.
- `circle` dengan `kosong: true` diisi warna kertas, sehingga garis di bawahnya tertutup. Pakai untuk titik terbuka di garis bilangan dan lubang di grafik. Letakkan setelah garis atau kurvanya. `kosong` milik bentuk `circle`, bukan `Gerak`: kalau kamu menyalin helper `bulatan(c, r, color, g: Gerak)` dari deck lain dan mengoper `kosong` lewat `g`, tsc gagal. Ketik parameternya `g: Gerak & { kosong?: boolean }`.
- `pada({ muncul: 2 }, bar(...))` dari `lengkap/gambar` memberi gerak yang sama ke satu kelompok bentuk.
- Contohnya ada di kartu "Membilang: satu benda, satu sebutan" di `produksi/cacah-banyak-benda.ts`.

**Lab.** Setiap lab wajib punya `petunjuk`, yaitu satu kalimat perintah yang menyebut tombol atau benda yang disentuh dan apa yang harus diperhatikan. Contoh: "Tekan +1 sampai lidi lepas genap sepuluh, lalu lihat angka puluhannya." Petunjuk tampil dengan tangan menunjuk sampai lab disentuh pertama kali.

**Tata letak.** Kartu tampil di 9:16 dan 16:9. Di 16:9, kartu bergambar atau ber-lab menjadi dua kolom, dan kartu teks diperbesar. Tinggi gambar dibatasi 90% lebar kartu, jadi gambar tegak mengecil; utamakan `view` mendatar atau persegi. Jaga label gambar supaya tidak saling menimpa: beri jarak sesuai ukuran huruf, dan catat label yang rapat.

## Catatan untuk audit

Isi `catatan[slug]` dengan hal yang belum bisa kamu pastikan saat menulis. Satu catatan untuk satu kartu (`kartu` berisi judul kartu, atau `"deck"`), dengan salah satu jenis berikut:

| Jenis | Contoh |
|---|---|
| `isi` | Fakta atau istilah yang kamu ragukan, rumusan yang bisa disalahpahami, atau angka rekaan yang perlu ditandai |
| `tata-letak` | Label gambar rapat, kartu padat yang mungkin melewati batas, atau tabel lebar |
| `animasi` | Gerak yang kamu inginkan tapi belum bisa ditulis dengan kosakata yang ada |
| `interaksi` | Lab atau soal yang caranya mungkin tidak jelas bagi pembelajar |
| `fitur` | Jenis kartu, lab, atau helper yang dibutuhkan tapi belum ada |
| `suara` | Kalimat yang butuh rekaman, atau pelafalan yang perlu dicek |

Catatan bukan tempat untuk menunda pekerjaan yang bisa kamu selesaikan sendiri. Kalau bisa dibetulkan sekarang, betulkan.

## Pelajaran dari putaran sebelumnya

Temuan yang berulang di putaran 1–4. Periksa deckmu terhadap daftar ini sebelum melapor.

- Istilah dan lambang diberi arti sebelum dipakai, termasuk +, =, ∀, n, dan nama sifat.
- Pengecoh tidak boleh setara dengan kunci, misalnya "3 dan 1" melawan "1 dan 3" setelah sifat tukar diajarkan.
- Kartu lain dirujuk dengan judulnya persis. Jangan menulis "kartu berikut".
- Konvensi buku sekolah ditulis sebagai kebiasaan, bukan disebut kesalahan. Contohnya urutan faktor 3 × 5, tepi kelas, atau penamaan ABCD.EFGH.
- Fakta yang bisa berubah, seperti tarif, harga, dan data penduduk, tidak ditulis sebagai angka pasti. Data rekaan ditandai rekaan.
- Kartu yang terlalu padat dipecah. Tabel panjang ditambah penjelasan panjang, atau kartu `ingat` yang sumbernya panjang, sering meluap di 9:16.
- **Judul kartu yang dirujuk deck lain jangan diganti.** Sebelum mengganti judul kartu lama, jalankan `grep -rn 'card: "' src/content/kartu`. Kalau deck sumber sedang ditulis ulang penulis lain di putaran yang sama, jangan merujuk judul kartunya. Jelaskan langsung di kartumu, lalu catat supaya kartu itu diganti `ingat` saat audit.
- Unit yang sengaja kamu keluarkan dari deck, karena punya unit sendiri, sebutkan di laporan.

## Laporan

Kembalikan untuk setiap deck:
- slug;
- jenis tugasnya;
- apakah lolos gerbang;
- jumlah catatan per jenis;
- kebutuhan fitur yang belum ada.
