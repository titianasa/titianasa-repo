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
  - Minimal 3 contoh kerja dan 8 latihan bertingkat. Latihan pertama diletakkan sesudah contoh kerja pertama.
  - Soal `multi` (PG kompleks) dan `bs` (benar/salah) boleh dipakai bila cocok dengan materinya, tetapi tidak wajib.
- **Gambar dan lab.** Gambar harus sesuai skala angkanya. Topik geometri, grafik, data, dan peluang wajib bergambar atau memakai lab.
  - Lab yang cocok untuk deck kanonik: `statistik`, `peluang`, `vektor`, `turunan`, `integral`, `pythagoras`, `bukti-pythagoras`, `garis`, `parabola`, `sudut`, `gelombang`, `timbangan`, `preposisi`, juga `bingkai`, `potong`, `puluhan`, `jam`, `ukur`, `piktogram`, `bentuk`, dan `pola` bila memang menjelaskan konsepnya.
  - Parameternya ada di `src/content/kartu/types.ts` (`LabSpec`).
  - Warna gambar memakai indeks palet 0 biru, 1 merah muda, 2 hijau, 3 ungu, dan 4 kuning. Kalau teks menyebut warna, warnanya harus sesuai.
- **Animasi dan interaksi.** Lihat bagian "Animasi dan interaksi" di bawah. Setiap lab wajib punya `petunjuk`.
- **Bahasa Inggris.**
  - Pakai British English, dengan urutan dan isi sesuai CEFR dan rujukan standarnya.
  - Utamakan kalimat dari daftar berekaman di spesifikasi.
  - Panjang kalimat contoh mengikuti level CEFR (E4). Jenis latihan dan panjang kalimat latihan (E12) bebas di deck kanonik: pilih latihan yang paling melatih konsepnya, termasuk `fix` dan `arrange` di level awal. Pembatasan E12 hanya berlaku di deck jalur (kemasan).
  - Kesalahan khas pembelajar Indonesia ditulis beserta sebabnya (E16–E17).
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
- `dari: [dx, dy]` membuat bentuk bergeser masuk dari posisi itu ke tempatnya, misalnya benda masuk ke kelompok.
- `sorot: [n, ...]` membuat bentuk berdenyut di tahap itu. Pakai untuk bagian yang sedang dibicarakan keterangan.
- `coret: n` mencoret teks di tahap n. `hilang: n` membuat bentuk memudar keluar.
- `coretBagian: [a, b]` bersama `coret` mencoret hanya huruf ke-a sampai sebelum ke-b dalam satu teks, misalnya "which" di tengah kalimat. Hitung a dan b dari posisi huruf di string (`s.indexOf("which")`), jangan ditebak. Lebarnya ditaksir dari jumlah huruf, jadi pakai untuk kata utuh, bukan satu huruf.
- `langkah: [...]` di kartu berisi keterangan untuk setiap tahap, satu untuk tiap tahap mulai dari 0. Setiap tahap punya satu tugas, dan keterangannya menyebut tugas itu.
- `ketuk: true` membuat pembelajar memajukan tahap sendiri. Pakai ini kalau pembelajar sebaiknya menebak dulu sebelum melihat tahap berikutnya. Tanpa `ketuk`, gambar berjalan sendiri. `tempo` mengatur milidetik per tahap (bawaan 1400).
- `putar: { pada, sudut, pusat }` membuat bentuk berputar ke tempatnya di tahap `pada`. Sebelum tahap itu, bentuk terputar `sudut` derajat searah jarum jam di sekitar `pusat`. Contohnya lengan timbangan yang miring lalu datar, atau sudut segitiga yang disobek lalu diputar ke samping sudut lain.
- `lipat: { pada, sumbu, di }` membuat bentuk melipat ke tempatnya. Sebelum tahap `pada`, bentuk berupa bayangan cerminnya terhadap garis x = `di` (`sumbu: "tegak"`) atau y = `di` (`"datar"`). Pakai untuk jaring-jaring yang dilipat atau pencerminan.
- `tumbuh: { dari, arah }` membuat bentuk tumbuh dari titik `dari` saat muncul, menurut sumbu y, x, atau keduanya. Contohnya batang diagram yang naik dari sumbu.
- `pindah: { pada, ke: [dx, dy] }` menggeser bentuk yang sudah tampil sejauh `ke` di tahap `pada`. Bentuknya sama, bukan diganti salinan. Contohnya koma desimal yang bergeser dua tempat atau ubin aljabar yang dikumpulkan.
- `tebal: 2` mempertebal garis, misalnya jarum jam pendek.
- `arrow: true` memberi ujung panah pada `line`, dan juga pada `curve`: panahnya mengikuti arah dua titik terakhir kurva. Pakai untuk lompatan di garis bilangan, busur langkah, atau arah gerak "over".
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
