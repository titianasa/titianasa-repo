# Produksi massal kartu

Status per 2026-11-03: semua persiapan selesai, termasuk riset, aturan, alat, alat peraga, dan orkestrasi. Produksi menunggu persetujuan pemilik (lihat "Keputusan pemilik"). Dokumen ini menjelaskan apa yang diproduksi, cara menjalankannya dengan 5 agen sekaligus, dan alat yang dipakai.

Acuan isinya:

| Berkas | Isi |
|---|---|
| `standar-kartu-lengkap.md` | Standar semua deck |
| `riset-kelas-awal.md` | Kelas 1–2, aturan A1–A19 |
| `riset-sd-sma.md` | Kelas 3–SMA, aturan M1–M28 |
| `riset-inggris.md` | Bahasa Inggris, aturan E1–E21 |
| `brief-penulis.md`, `brief-pemeriksa.md` | Instruksi untuk agen |
| ADR-0026 | Kanonik dan jalur |

## Yang harus diproduksi

Produksi massal hanya mengerjakan **kanonik**. Kanonik ditulis menurut standar keilmuan untuk pembelajar mana pun (ADR-0026, "kanonik sebagai sumber pengetahuan"). Penyesuaian untuk kelas, pembaca muda, atau ujian dibuat sesudahnya, sebagai deck jalur (`kemasan`), oleh jalur yang membutuhkannya.

Hitungan ini tidak disimpan di berkas mana pun. Setiap kali dijalankan, `bun scripts/antrian-produksi.ts` (di `titian-web`) menghitung ulang langsung dari kode. Hitungan 2026-11-03:

| Tingkat | Baru | Tulis ulang | Perbaiki |
|---|---|---|---|
| Matematika (`mtk`) | 27 | 180 | 107 |
| Inggris Pre-A1 / A1 / A2 | 4 / 6 / 14 | 8 / 38 / 49 | 6 / 13 / 4 |
| Inggris B1 / B2 / C1 / C2 | 8 / 2 / 0 / 0 | 41 / 27 / 12 / 2 | 0 / 3 / 1 / 0 |

Totalnya 552 deck dalam 142 tugas agen, atau sekitar 28 putaran berisi 5 agen. Matematika diurutkan menurut kedalaman prasyarat kanonik, jadi yang paling mendasar dikerjakan dulu. Inggris diurutkan dari Pre-A1.

Deck jalur yang sudah ada:
- **Kurikulum Indonesia Kelas 1–2 (prabaca):** `ki-k1-pasangan-10`, `ki-k1-tambah-kurang-20`, `ki-k2-setengah-seperempat`.
- **TKA:** `tka-bulat-tambah-beda`.

Pembuatan deck jalur berikutnya menunggu putusan per jalur.

## Menjalankan produksi

Produksi dan audit adalah dua jalur terpisah. Penulisan tidak menunggu pemeriksaan, jadi produksi berjalan cepat. Mutu dijaga oleh gerbang, catatan penulis, dan audit bertahap.

**Kenapa tidak memakai Workflow.** Workflow Claude Code membatasi agen yang berjalan bersamaan menjadi jumlah inti CPU dikurangi 2. Mesin dev hanya punya 4 inti, jadi batasnya 2 agen. Putaran 1 (3 November 2026) berjalan dengan Workflow dan memakan sekitar 1 jam 15 menit untuk 6 tugas. Agen yang dipanggil langsung dari sesi utama tidak terkena batas itu. Pemeriksaan bukan penghambat: gerbang setengah detik dan pemeriksaan tipe sekitar 10 detik. Waktunya habis untuk menulis, sekitar 10 menit per tugas. `.claude/workflows/produksi-kartu.js` disimpan untuk mesin yang intinya banyak.

### Putaran tulis

1. **Antrean.** Jalankan `bun scripts/antrian-produksi.ts --putaran --json --agen 5`. Hasilnya 5 tugas. Setiap tugas berisi beberapa deck berurutan dari satu tingkat dan satu berkas tujuan `produksi/<id>.ts`.
2. **Tulis.** Sesi utama menjalankan 5 agen penulis sekaligus di latar belakang, masing-masing dengan `brief-penulis.md` dan satu tugas.
   - Setiap penulis hanya menulis berkasnya sendiri.
   - `produksi/index.ts` dibuat ulang oleh `susun-produksi.ts`, dan hasilnya selalu sama siapa pun yang menjalankannya.
   - Deck baru disisipkan ke koleksi lewat `setelah`, dan tulis ulang menimpa deck lama berdasarkan slug.
   - Penulis menjalankan gerbang sampai lolos dan mencatat yang belum bisa dipastikan di `catatan`.
3. **Gabung**, sekali setelah kelima penulis selesai. Sesi utama menjalankan berurutan:
   - indeks;
   - pemeriksaan tipe;
   - gerbang;
   - uji muat (`fit.ts`);
   - audit tumpang tindih dan lebar landscape (`tumpang.ts`);
   - uji galat browser (`isu.ts`);
   - ekspor deck dan build seed.

   Temuan tampilan masuk ke `catatan` jenis `tata-letak`.

Sesudah setiap putaran, baca laporan penulis, terutama catatan `fitur`. Lihat beberapa kartu bergambar dengan mata sendiri, lalu commit. Gerbang hanya mengukur yang bisa diukur. Kejelasan tetap perlu dinilai manusia.

### Putaran audit

Audit berjalan setelah beberapa putaran tulis, juga dengan 5 agen sekaligus.

- Antreannya: `bun scripts/antrian-audit.ts --json`. Isinya berkas yang decknya belum punya entri `audit`, dimulai dari yang paling lama, beserta catatan penulis dan pelanggaran gerbangnya.
- Satu auditor memegang satu berkas dan mengikuti `brief-pemeriksa.md`.
- Auditor membetulkan berkas itu, menulis `audit[slug]`, dan menghapus catatan yang sudah beres.
- Temuan yang muncul di banyak berkas dicatat di "Temuan berulang" di bawah. Bila bisa diperiksa mesin, temuan itu dijadikan aturan gerbang atau brief, supaya putaran tulis berikutnya tidak mengulanginya.

### Temuan berulang

Dari pemeriksaan putaran 1:
- Istilah atau lambang dipakai sebelum diberi arti, misalnya tanda + dan =, atau "pasangan sepuluh".
- Pengecoh setara dengan kunci, misalnya "3 dan 1" melawan "1 dan 3" setelah sifat tukar diajarkan.
- Rujukan "kartu berikut" menunjuk kartu yang salah.
- Gambar proses ditampilkan diam. Kosakata animasi baru tersedia sesudah putaran 1.

### Kebutuhan fitur dari penulis

Dikumpulkan dari laporan penulis. Setelah sebuah fitur dibangun, pindahkan barisnya ke "Komponen yang tersedia untuk penulis".

| Fitur | Diminta untuk | Putaran |
|---|---|---|
| Pilihan jawaban berupa gambar | Tampak dan jaring-jaring | 2 |
| Lipat dan putar 3D | Jaring kubus, bangun ruang | 2 |
| Lab balok dasar sepuluh dengan tukar 1 ratusan = 10 puluhan | Nilai tempat | 1 |
| Lab neraca dua sisi | Membandingkan berat | 1 |
| Lab tumpukan kubus | Tampak depan, atas, samping | 2 |
| Lab piktogram berskala, tabel frekuensi, diagram batang, pengambilan sampel | Penyajian data | 2 |
| Lab diagram Euler dan tabel kebenaran | Logika | 2 |
| Lab rentang taksiran, model luas dan perkalian bersusun, bagi rata ke piring | Operasi bilangan cacah | 2 |
| Lab ukur dalam milimeter (resmikan satuan dasar) | Ketelitian | 2 |
| `bantu` menerima `level` dan `konteks`; helper bersama garis bilangan, kotak sepuluh, turus | Semua deck | 1 |
| Lab `statistik`: baris jangkauan, ragam, simpangan baku, pita x̄ ± s; dua kumpulan data pada satu skala | Ukuran sebaran, keputusan statistik | 5 |
| Kartu tabel dengan sel yang disorot per tahap (atau diagram mosaik) | Tabel kontingensi | 5 |
| Matriks bertumpuk di teks langkah, soal, dan pilihan (sekarang ditulis `[a b; c d]`) | Matriks | 5 |
| Lab sudut keliling, lab radian | Lingkaran, trigonometri | 5 |
| Lab grafik eksponen | Pangkat pecahan | 5 |
| Lab persegi peluang, pohon peluang, distribusi, binomial | Peluang SMA, variabel acak | 5 |
| Notasi bertumpuk di teks: sigma dengan batas, pecahan bertingkat, matriks dan vektor kolom, panah vektor, basis log pecahan | Deret, aljabar, matriks, vektor, logaritma | 5–6 |
| Lab fungsi eksponen dan fungsi logaritma (geser basis, h, k; asimtot ikut), lab pertidaksamaan eksponen | Eksponen, logaritma | 6 |
| Lab ubin aljabar (faktor, melengkapkan kuadrat) | Aljabar, kuadrat | 6 |
| Lab transformasi linear (persegi satuan → jajargenjang, luas = det), lab ruang 3D dan kubus yang bisa diputar, irisan kubus dan kerucut | Matriks, vektor, geometri ruang | 6 |
| Lab mistar hitung | Sifat logaritma | 6 |
| Lab `vektor`: sembunyikan a·b dan a+b, tampilkan bayangan a pada b; lab `garis`: titik potong sumbu x dan arsir y > 0 | Vektor, pertidaksamaan linear | 6 |
| Lab `parabola` memutar peragaan dari nilai awal deck, bukan lima langkah tetap | Kuadrat, polinom | 6 |
| Poligon tanpa garis tepi atau arsiran | Daerah solusi | 6 |
| Lab Poisson, normal, nilai harapan, distribusi sampling, interval kepercayaan, limit numerik | Peluang dan statistik SMA, limit | 7 |
| Lab program linear (garis selidik digeser), lab anuitas, lab simulasi risiko dengan distribusi sendiri | Terapan | 7 |
| Lab bidang kompleks (a + bi, kali i, sekawan) | Bilangan kompleks | 7 |
| Lab `sudut`: batasi peragaan ke 0°–90°; teks menyebut warna sinus sesuai palet | Trigonometri | 7 |
| Gerak titik bertahap dengan angka berubah (0,9 → 0,99 → 0,999) | Limit | 7 |
| Gerak: `lipat` terhadap garis miring (y = x), ubah bentuk poligon, gerak 3D (membuka selimut, menggeser garis singgung) | Fungsi invers, matriks, bangun ruang | 6 |
## Alat

| Alat (`titian-web/scripts/`) | Kegunaan |
|---|---|
| `antrian-produksi.ts` | Antrean dan pembagian tugas per putaran tulis |
| `antrian-audit.ts` | Antrean audit: deck produksi yang belum diaudit, dengan catatan penulis dan pelanggaran gerbang |
| `spek-deck.ts <slug>` atau `--unit <kunci>` | Semua yang dibutuhkan penulis: tingkat dan batas, prasyarat beserta judul kartu untuk `ingat`, bukti buku/CP/TKA/acuan kuliah, kalimat Inggris berekaman, deck lama, deck contoh, posisi `setelah` |
| `periksa-kartu.ts` (`aturan-kartu.ts`, `tingkat-kartu.ts`) | Gerbang: aturan A, M, dan E yang bisa diperiksa mesin |
| `susun-produksi.ts` | Indeks berkas produksi |
| `suara-inggris.ts` | Kalimat Inggris yang belum berekaman, untuk antrean TTS |
| `export-decks.ts` | Peta deck ke backend |

Alat uji browser ada di `agent/tools/qa/kartu/`: `fit.ts`, `tumpang.ts`, `shot1.ts`, `ketuk.ts`, `jalan-deck.ts`, dan `isu.ts`. Penjelasannya ada di README folder itu.

Data sumber di `titian-backend-go/data/kanonik/sumber/`:

| Berkas | Isi |
|---|---|
| `buku-teks-matematika.json`, `buku-teks-inggris.json` | Peta subbab buku siswa ke unit kanonik |
| `cp-*-2025.json`, `tka-matematika-2025.json` | Butir CP dan muatan TKA |
| `acuan-kuliah-matematika.json` | 109 unit di luar sekolah, dengan sumber terbuka per bab |
| `klip-inggris.json` (dibuat `bank_klip.py`) | Kalimat Inggris berekaman per unit dan per level |

## Komponen yang tersedia untuk penulis

- **Lab Kelas 1–2:** `hitung`, `bingkai`, `bandingkan`, `jam`, `potong`, `puluhan`, `posisi`, `ukur`, `piktogram`, `bentuk`, `pola`.
- **Lab SMP–SMA:** `statistik`, `peluang`, `vektor`, `turunan`, `integral`, `pythagoras`, `bukti-pythagoras`, `garis`, `parabola`, `sudut`, `gelombang`, `timbangan`.
- **Lab Inggris:** `preposisi`.
- **Semua lab sudah diuji di browser:** peragaan berjalan, ketukan direspons, dan tidak ada galat hidrasi.
- **Soal TKA:** `multi` (PG kompleks MCMA) dan `bs` (PG kompleks benar/salah). Setiap latihan bisa diberi `level` 1–3, `konteks`, dan `grup` untuk soal kelompok.
- **Kelas 1–2 (`prabaca`):** suara otomatis, papan angka, catatan `dampingi`, dan teks besar.
- **Inggris Pre-A1–A1:** ubin huruf untuk jawaban satu kata.
- **Gambar beranimasi (sejak 4 November 2026):** `muncul`, `dari`, `sorot`, `coret`, `hilang`, `putar`, `lipat`, `tumbuh`, `pindah`, `tebal`, keterangan `langkah`, dan `ketuk` (lihat `brief-penulis.md`).
- **Lingkaran `kosong`** (sejak putaran 7): titik terbuka dan lubang di grafik. Gambar tegak dibatasi tingginya 90% lebar kartu.
- **Contoh memudar (M16):** langkah dengan `jawab`. **Latihan campuran (M20):** latihan dengan `dari`. **Soal bergambar:** latihan dengan `gambar`. Gerbang menagih M16 dan M20 pada deck produksi.

## Keputusan pemilik

1. **Produksi.** Disetujui 3 November 2026 ("oke kerjakan"). Sekitar 28 putaran tulis berisi 5 penulis, ditambah putaran audit. Biaya tokennya besar, jadi tetap dilaporkan per putaran.
2. **Suara Inggris.** 694 kalimat unik di deck yang ada belum berekaman, dan deck baru akan menambah lagi. Riset E1–E2 meminta rekaman atau TTS neural yang dicek manusia, dengan satu suara British, bukan suara perangkat. Ini memerlukan biaya TTS. Antreannya ada di `bun scripts/suara-inggris.ts --json`.
3. **Narasi Indonesia Kelas 1–3.** Sekarang memakai suara perangkat, yang gratis. Rekaman berkualitas memerlukan biaya TTS.
4. **Daftar kosakata CP** (1.000, 2.000, 3.000, dan 4.000 kata, aturan E14). Lampirannya tidak ada di teks CP yang kita punya. Daftar resminya perlu dicari, atau sementara memakai CEFR-J/EVP.
5. **Uji dengan pengguna sungguhan.** Ambang yang masih adaptasi perlu dicoba dengan anak Kelas 1–2, Kelas 3–4, Kelas 8, dan Kelas 11: batas teks Kelas 1–2 (A5, A7, A8), kata per kartu SD–SMA (M3–M5), dan batas Inggris bertanda [A].

## Masih terbuka (teknis)

- **A12:** bantuan tiga tingkat saat jawaban salah. Saat ini baru dua tingkat.
- **A16:** sorotan kata saat narasi.
- **Pemeriksaan otomatis yang belum ada:**
  - E3: kata yang diuji harus sudah pernah didengar;
  - E10: istilah tata bahasa per level;
  - E14: kosakata di luar daftar level;
  - M15: soal serupa paling jauh 2 kartu sesudah contoh kerja.

  Untuk sementara, keempatnya diperiksa pemeriksa.
