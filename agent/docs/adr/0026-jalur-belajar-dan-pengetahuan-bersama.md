# ADR-0026: Banyak jalur belajar, satu catatan pengetahuan

Status: Diterima arahnya oleh pemilik (2026-11-02), berjalan di dev.

## Ringkasan

Satu mata pelajaran punya banyak jalur belajar, tapi seorang siswa hanya punya satu catatan pengetahuan. Unit yang dikuasai di satu jalur otomatis terhitung di semua jalur lain yang memuat unit itu. Yang berbeda antarjalur hanya urutan dan kemasannya.

## Konteks

Pemilik ingin siswa yang sudah belajar Kurikulum Indonesia Kelas 7 sampai 9 melihat apa yang sudah dan belum dikuasai saat masuk jalur TKA. Materinya sama, yang berubah soal latihan dan pendekatannya.

Pemetaan kanonik (`outputs/PEMETAAN_KANONIK_JALUR_UJIAN_V1.md`) sudah menetapkan bahwa path tidak memiliki materi, dan `canon_paths`, `canon_path_nodes`, serta `canon_units` sudah terisi di dev. Keputusan ini membangun di atasnya.

Keputusan ini menggantikan keputusan 2026-09-20 untuk kartu: jalur berjalan di atas unit kanonik, bukan di atas bab perpustakaan. Alur latihan bab yang lama di `/jalur` tidak berubah.

## Keputusan

Tiga lapis dengan tugas yang berbeda:

| Lapis | Isi | Milik |
|---|---|---|
| Pengetahuan | Status tiap unit: belum, dilihat, dimiliki, dikuasai | Siswa, satu per akun |
| Jalur | Urutan unit dan pengelompokannya | Jalur, tidak punya progres |
| Kemasan | Deck latihan khusus satu jalur, misalnya gaya soal TKA | Jalur, tidak mengubah pengetahuan |

Aturannya:

1. Deck `materi` menentukan status unit. Unit dimiliki kalau semua deck materinya lulus 80% sekali coba.
2. Unit dikuasai kalau semua deck itu lulus lagi di hari lain, dari jalur mana pun.
3. Deck `tambahan`, `cek`, dan `kemasan` tidak mengubah status unit.
4. Jalur tidak mengunci. Unit yang sudah dimiliki tampil dengan asalnya dan langsung menawarkan kemasan jalur itu.
5. Jaringan pengetahuan milik siswa. Memilih jalur hanya menyorot bagian yang dicakup jalur itu.

## Palet jalur (fokus sejak 2026-11-02)

| Rak | Matematika | Bahasa Inggris |
|---|---|---|
| Belajar dari awal | Kurikulum Indonesia (Fase A–F), Belajar Berurutan | Kurikulum Indonesia (Fase B–F, CP 2025), CEFR |
| Persiapan ujian | TKA SD, TKA SMP, TKA SMA, TKA SMA Lanjutan, UTBK Pengetahuan Kuantitatif, UTBK Penalaran Matematika, UTBK Penalaran Umum | TKA SMA, TKA SMA Lanjutan, UTBK Literasi dalam Bahasa Inggris |

- Semua unit dan jalur ditulis di `titian-backend-go/data/kanonik/`. Jalur ujian ada di `ujian.py`, mengikuti kisi-kisi resmi di `puzzle-pengetahuan/tinjauan-jalur-belajar.md`.
- Jalur di luar fokus dan jalur turunan otomatis lama sudah dihapus, karena belum produksi dan tidak ada data lama yang dibawa.
- Materi kanonik tidak memuat kelas. Rancangan kanoniknya ada di `puzzle-pengetahuan/rangkaian-kanonik.md`.

## Implementasi

- Skema: `db/migrations/0113_jalur_kartu.sql` (`card_decks`, `card_progress`, `card_active_paths`, `canon_paths.subject_code`).
- Data: `internal/kartu/seed.sql` dibangun oleh `data/kanonik/build.py` dari berkas kanonik, lalu dimuat lewat `cmd/tools/seed_jalur`. Bisa diulang, dan tabel kanonik hanya berisi isi berkas.
- API: `internal/kartu`, rute `/kartu/jalur`, `/kartu/jalur/{slug}`, `/kartu/jalur/{slug}/aktif`, `/kartu/jaringan`, `/kartu/decks/{slug}/hasil`.
- Web: `/puzzle/kartu` (palet), `/puzzle/kartu/jalur/[slug]`, `/puzzle/kartu/jaringan`, `/puzzle/kartu/semua`. Kemasan ada di `src/content/kartu/kemasan.ts`.
- Tes: `internal/kartu/kartu_test.go` membuktikan pengetahuan terbawa antarjalur.

Kelas di Kurikulum Indonesia Bahasa Inggris diturunkan dari CEFR: A1 di Kelas 1–5, A2 di Kelas 6–9, B1 di Kelas 9–12, enam unit B2 pertama di Kelas 12.

## Konsekuensi dan utang

- Pemetaan unit ke jalur ujian masih otomatis dan perlu ditinjau. Contoh: TKA hanya memuat 4 dari 8 unit bilangan bulat (sudah ditambah), dan TKA memuat Analisis Real serta IGCSE memuat Limit.
- `canon_units.level` masih draf. Bilangan bulat tercatat Level 6, sedangkan Kurikulum Indonesia menaruhnya di Kelas 7. Jalur Kurikulum Indonesia sudah mengoreksinya, jalur Berurutan belum.
- TKA belum dipisah per jenjang SD, SMP, dan SMA, dan struktur resminya belum diverifikasi.
- Jaringan kartu (`card_progress`) masih terpisah dari jaringan misi Basic (`masteries`). Keduanya perlu disatukan lewat pemetaan unit ke konsep.
- Skor dikirim oleh browser dan belum terhubung ke XP.
- Status unit belum memudar seiring waktu seperti kekuatan di `masteries`.
- Tiap penambahan deck perlu baris baru di `data/kanonik/kartu.py`, lalu `build.py` dijalankan ulang.

## Tambahan 2026-11-03: kanonik sedetail mungkin

Keputusan pemilik: unit kanonik dibuat selengkap dan sedetail mungkin, sehingga jalur mana pun (Kurikulum Indonesia per kelas, TKA, SNBT, CEFR) cukup memilih dan mengurutkan unit tanpa mengubah kanonik.

- **Ukuran unit:** satu kemampuan yang bisa dikuasai dalam satu kali belajar, kira-kira satu deck berisi 15–25 kartu. Unit dipecah kalau ada sumber yang mengajarkan bagian-bagiannya di waktu berbeda. Unit tidak dipecah kalau yang berbeda hanya besar bilangannya, sedangkan caranya sama.
- **Sumber cakupan Matematika:** buku teks resmi Kelas I–XII per subbab (lihat `puzzle-pengetahuan/acuan-buku-teks-matematika.md`), CP 046/2025, TKA, dan UTBK-SNBT. **Bahasa Inggris:** buku teks, CP, deskriptor CEFR, dan TKA. Setiap butir sumber harus terpetakan ke paling sedikit satu unit, dan ini diperiksa otomatis.
- **Prasyarat** dicatat per unit di kanonik. Jalur diperiksa supaya tidak menempatkan unit sebelum prasyaratnya. Kartu "ingat" diambil dari prasyarat ini.
- **Jalur Kurikulum Indonesia** dikelompokkan per kelas mengikuti buku teks resmi, dengan label fasenya. Unit yang tidak ada di buku ditempatkan menurut fase CP. Daftarnya dicetak oleh pemeriksa cakupan.
- Satu unit boleh muncul di beberapa kelas dalam satu jalur sebagai pengulangan. Database sudah mengizinkan ini.

### Hasil penerapan Matematika (2026-11-03)

- **Sumber:** ada tiga berkas pemetaan di `titian-backend-go/data/kanonik/sumber/`, yaitu `buku-teks-matematika.json` (270 subbab), `cp-matematika-2025.json`, dan `tka-matematika-2025.json`. Ketiganya diperiksa oleh `cek_cakupan.py`. Hasilnya: tidak ada kunci salah, tidak ada unit yang belum dibuat, dan tidak ada catatan pecah yang tersisa.
- **Kanonik:** unit Matematika bertambah dari 274 menjadi 314.
  - Ada 20 unit lama yang dipecah dan diganti id-nya, misalnya `keliling-luas-bangun-datar` menjadi petak satuan, keliling, dan luas dengan rumus.
  - Ada 14 unit yang benar-benar baru, misalnya pangkat pecahan, fungsi tangga, tabel kontingensi, dan garis singgung kurva.
  - Deck lama tetap di setengah unit yang memang diajarkannya. Dua deck dipindah: `inferensi-regresi` (isinya korelasi SMA) dan `datar-lingkaran` (isinya keliling dan luas lingkaran).
- **Prasyarat:** setiap unit menyimpan prasyarat langsung (`prasyarat`, kunci pendek) di `matematika.json`. `build.py` menolak prasyarat yang tidak dikenal atau membentuk siklus. Build juga melaporkan jalur yang menaruh unit sebelum prasyaratnya. Jalur ujian boleh mengikuti urutan kisi-kisinya, jadi laporan ini tidak menggagalkan build.
- **Jalur:** `sumber/susun_jalur.py` menulis kedua jalur Matematika dari sumber, jadi jalur tidak lagi disunting tangan.
  - **Kurikulum Indonesia:** 14 kelompok, terdiri dari Kelas 1–12 ditambah Tingkat Lanjut Kelas 11 dan 12. Unit spiral muncul di setiap kelas yang mengajarkannya.
  - **Berurutan:** 14 level. Setiap unit muncul sekali dan selalu sesudah prasyaratnya. Unit perguruan tinggi berada di Level 12–14.
  - Kedua jalur tidak melanggar prasyarat.
- **Unit sekolah di luar buku dan CP** ditempatkan menurut kisi-kisi ujian yang mengujinya atau menurut kelas Kurikulum 2013 (`EXTRA` di `susun_jalur.py`). Contohnya program linear, dimensi tiga, notasi sigma, logika, dan penalaran kuantitatif. Unit ini ada di jalur Berurutan dan jalur ujian, tetapi tidak di jalur Kurikulum Indonesia.
- **Utang:** 36 unit sekolah belum punya deck. Sebagian isinya sudah ada di deck lama dan tinggal dipisahkan, misalnya soal sudut keliling di `datar-busur-juring`. Seed baru belum dipasang ke database dev maupun prod.

### Hasil penerapan Bahasa Inggris (2026-11-03)

- **Sumber:**
  - `sumber/buku-teks-inggris.json` memetakan 242 subbab dari 12 buku siswa, yaitu Kelas III–XII ditambah Tingkat Lanjut XI–XII, dan setiap subbab punya bukti halaman.
  - `sumber/cp-inggris-2025.json` memetakan CP per fase. CP mewajibkan Bahasa Inggris mulai Fase B dan hanya menetapkan keterampilan serta target CEFR.
  - Keduanya diperiksa oleh `cek_cakupan.py`. Lihat `puzzle-pengetahuan/acuan-buku-teks-inggris.md`.
- **Kanonik:** unit Inggris bertambah dari 227 menjadi 261.
  - **Dua id diganti:** `vocab.numbers-time` menjadi `vocab.numbers`, dan `vocab.clothes-colours` menjadi `vocab.colours`.
  - **Lima pecahan** karena diajarkan di waktu berbeda:
    - hari dan tanggal dipisah dari angka;
    - pakaian dipisah dari warna;
    - sifat dipisah dari perasaan;
    - izin dan permintaan dengan *can* dipisah dari *can* untuk kemampuan;
    - kata urutan dipisah dari penghubung logis.
  - **Unit baru dari buku**, setelah usulan yang tumpang tindih digabung. Contohnya bahasa kelas, ciri fisik, memuji, terkejut dan kecewa, kalimat langsung, kalimat majemuk setara dan bertingkat, frasa nomina, poster dan infografik, unggahan media sosial, puisi sederhana, esai sebab-akibat, serta mendeskripsikan grafik.
  - **Deck tetap di bagian utama unit.** Deck lama mencakup kedua bagian, misalnya "Feelings and Personality", jadi deck itu perlu dipecah saat ditulis ulang.
- **Prasyarat:** 225 unit Inggris kini punya prasyarat langsung (`PRASYARAT` di `bahasa_inggris.py`). `build.py` memeriksa prasyarat kedua mapel.
- **Jalur:** `sumber/susun_jalur_inggris.py` kini menulis kedua jalur Inggris. Pembagian mekanis per CEFR di `build.py` dihapus.
  - **Kurikulum Indonesia:** Kelas 3–12 ditambah Tingkat Lanjut 11 dan 12, mengikuti buku. Unit setingkat target CP yang tidak diajarkan buku wajib diisi menurut CEFR dan disebar ke kelas-kelas dalam fasenya. Ada 67 unit seperti ini, misalnya future, present perfect, dan conditional. Prasyarat yang dipakai buku tetapi tidak diajarkannya ditarik ke kelas yang membutuhkannya.
  - **CEFR:** Pre-A1 sampai C2, diurutkan menurut prasyarat.
  - Kedua jalur tidak melanggar prasyarat.
- **Utang:** 34 unit Inggris belum punya deck. Lima deck lama perlu dipecah. Seed belum dipasang.


## Tambahan 2026-11-03: kanonik sebagai sumber pengetahuan

Keputusan pemilik, yang mempertajam tambahan "kanonik sedetail mungkin" di atas:

- **Isi kanonik.** Kanonik berisi materi dasar yang sudah mapan secara keilmuan. Bahasa Inggris mengikuti CEFR dan rujukan standarnya, misalnya Cambridge dan Oxford. Matematika mengikuti struktur dan prasyarat ilmunya sendiri. Kanonik adalah "induk pengetahuan" dan tidak dipaksa mengikuti jalur mana pun. Kurikulum, TKA, dan SNBT akan berubah, sedangkan isi kanonik tidak ikut berubah.
- **Pembaca.** Deck kanonik ditulis menurut standar mutu materi pembelajaran, untuk pembelajar mana pun. Penulis tidak mengandaikan pembacanya anak Kelas 1 atau siswa SMA. Tingkat deck kanonik Matematika adalah satu standar (`mtk`). Tingkat deck kanonik Inggris adalah level CEFR bahasanya.
- **Kelengkapan.** Kanonik dikejar tuntas menurut ilmunya, bukan menurut setiap butir kurikulum. Peta buku, CP, TKA, dan SNBT di `sumber/` tetap dipakai sebagai data jalur dan untuk menemukan celah. Data itu bukan syarat kanonik.
- **Penyesuaian ada di jalur.** Jalur menyesuaikan materi dengan deck miliknya sendiri (`kind: "kemasan"`, `path: <jalur>`) yang menempel pada unit kanonik. Bentuknya bisa berupa:
  - kartu jembatan sebelum unit yang sulit;
  - kartu penjelas tambahan;
  - versi untuk pembaca muda, misalnya prabaca Kelas 1–2 dengan suara, papan angka, dan catatan pendamping;
  - latihan bergaya TKA;
  - pembagian satu unit ke dua kelas.

  Kemajuan tetap dicatat per unit kanonik. Riset batas per jenjang (`riset-kelas-awal.md`, `riset-sd-sma.md`, dan aturan Kelas 3–4 di `riset-inggris.md`) dipakai untuk deck jalur ini.
- **Penerapan.**
  - `tingkat-kartu.ts` menentukan tingkat per deck: kanonik menurut ilmunya, kemasan menurut jalurnya.
  - Gerbang menolak deck kanonik yang ditandai `prabaca`.
  - Antrean produksi hanya memuat kanonik dan mengurutkannya menurut kedalaman prasyarat, bukan kelas.
  - Tiga deck pilot prabaca menjadi kemasan jalur Kurikulum Indonesia: `ki-k1-pasangan-10`, `ki-k1-tambah-kurang-20`, dan `ki-k2-setengah-seperempat`. Unit kanoniknya kembali ke versi standar umum.
- **Belum ada:** node jalur yang menunjuk sebagian kartu dari satu deck, untuk membagi satu unit ke dua kelas. Fitur ini dibuat saat jalur pertama membutuhkannya. Untuk sementara, pembagian dilakukan dengan deck kemasan per kelas.
