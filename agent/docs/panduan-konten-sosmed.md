# Panduan membuat konten sosmed Titian Asa

Panduan ini untuk siapa pun (orang atau agen AI) yang membuat konten Instagram dan TikTok Titian Asa berikutnya. Isinya: aturan merek, cara membuat gambar, cara membuat video, dan daftar periksa sebelum tayang.

Semua alat ada di `outputs/konten-sosmed/`. Batch pertama (9 postingan dan 1 video perkenalan, Oktober 2026) dibuat dengan alat yang sama dan bisa dijadikan contoh.

## 1. Aturan yang tidak boleh dilanggar

| Aturan | Keterangan |
|---|---|
| Alamat web | **titianasa.com** wajib ada di setiap gambar dan setiap video. Di narasi diucapkan "Titian Asa dot com", bukan "titik kom". |
| Kata "belajar" | Untuk Kampung Bahasa Pare pakai **belajar**, jangan "main", "pemain", atau "game". Contoh: "Cara belajar di Kampung Bahasa Pare", "teman belajar". |
| Status fitur | Yang sudah bisa dipakai hanya Kampung Bahasa Pare. Program lain (Ruang Belajar, TKA, SNBT, Tryout, Mock Test, Study Group) wajib diberi tanda **Segera hadir** sampai benar-benar rilis. |
| Sumber materi | Ambil dari isi titianasa.com. Jangan mengarang angka, testimoni, atau harga. Testimoni dan harga sedang disembunyikan di web, jadi jangan dipakai di konten. |
| Warna utama | Kuning. Jangan diganti. |
| Sasaran | Gen Z dan milenial. Bahasa santai, kalimat pendek, tanpa bahasa brosur. |

## 2. Gaya visual

Gayanya sama dengan landing page titianasa.com (gaya "stiker", mengikuti nanyangmandarin.com).

| Unsur | Nilai |
|---|---|
| Font judul | Fredoka (tebal) |
| Font teks | Nunito |
| Font aksen tulisan tangan | Caveat |
| Kuning utama | `#f5b800` |
| Tinta (teks dan garis tepi) | `#1f2638` |
| Latar krem | `#fff8e8` |
| Latar kuning muda | `#ffeeb8` |
| Kertas (kartu) | `#fffdf8` |
| Aksen kata penting | `#d97c00` di latar terang, putih di latar kuning |
| Latar "dunia Pare" | gradasi biru malam ke hijau: `#1a1f4f` → `#183457` → `#1d5c3e` |

Ciri khasnya: garis tepi tebal, bayangan keras yang bergeser ke kanan bawah, sudut sangat bulat, label miring, latar bertitik, dan gambar kecil matahari serta bintang.

Tangkapan layar Kampung Bahasa Pare ada di `src/assets/` (dan `titian-web/public/pare/`). Jangan pakai frame yang memuat papan iklan contoh ("Kemendikbud", "ChatGPT") atau tulisan "Main sekarang".

## 3. Suara merek

- Sapaan "kamu", bukan "Anda".
- Slogan: "Semua Asa, Pasti Ada Jalannya!" dan "Belajar sampai bisa & terbiasa."
- Arti nama: Titian = jembatan, Asa = harapan.
- Boleh pakai kata sehari-hari (nggak, udah, yuk, bareng), tetapi jangan berlebihan.
- Setiap caption ditutup dengan ajakan dan `titianasa.com`.
- Visi dan misi di batch pertama dirumuskan dari teks web dan **belum disahkan pemilik**. Minta persetujuan sebelum dipakai ulang.

## 4. Membuat gambar (single dan carousel)

Semua slide didefinisikan sebagai data di satu file, lalu dirender jadi PNG dalam dua ukuran sekaligus.

| Ukuran | Dipakai untuk | Folder hasil |
|---|---|---|
| 1080×1350 (4:5) | Feed Instagram | `instagram/` |
| 1080×1920 (9:16) | TikTok mode foto, Reels, Story | `tiktok/` |

Versi 9:16 sudah memberi ruang kosong di atas, bawah, dan kanan supaya teks tidak tertutup tombol aplikasi.

### Langkah

1. Buka `outputs/konten-sosmed/src/build.ts`. Tambah atau ubah isi `POSTS`.
2. Jalankan di folder `src/`:

   ```bash
   bun build.ts     # membuat preview-ig.html dan preview-tiktok.html
   bun render.ts    # mengekspor semua slide ke PNG
   ```

3. Buka `preview-ig.html` di browser untuk melihat semua slide berdampingan.
4. Tulis caption dan jadwal di `kalender-dan-caption.md`.

`render.ts` butuh koneksi internet (font diambil dari Google Fonts) dan Google Chrome terpasang.

### Isi satu slide

| Kolom | Arti |
|---|---|
| `bg` | Latar: `cream`, `soft`, `yellow`, atau `navy` |
| `kicker` | Label kecil di atas judul |
| `title` | Judul. Kata di dalam `<a>…</a>` diberi warna aksen |
| `body` | Paragraf pendek. `<b>…</b>` untuk tebal |
| `note` | Catatan tulisan tangan, misalnya "geser →" |
| `phone` | Nama file tangkapan layar di `assets/` |
| `items` | Daftar butir: emoji, judul, keterangan |
| `big`, `sub` | Kalimat besar di kartu (dipakai untuk sapaan bahasa asing) dan terjemahannya |
| `tag` | Stiker merah miring di pojok, misalnya "Segera hadir" |
| `cta` | `true` untuk menampilkan alamat web ukuran besar |

Satu postingan dengan satu slide menjadi file tunggal. Lebih dari satu slide menjadi folder carousel berisi `NN-1.png`, `NN-2.png`, dan seterusnya.

### Saran isi

- Satu slide, satu pesan. Judul maksimal dua baris.
- Slide pertama carousel harus memancing orang menggeser. Slide terakhir berisi ajakan (`cta: true`).
- Carousel 5 sampai 7 slide.
- Selang-seling warna latar antar postingan supaya tampilan profil tidak monoton.

## 5. Membuat video motion (9:16, 60 detik)

Tekniknya sama dengan video promosi Kampung Bahasa Pare (`game/scripts/video/`): animasi tidak direkam, melainkan dirender frame demi frame, jadi hasilnya selalu tepat 1.800 frame pada 30 fps.

File ada di `outputs/konten-sosmed/video/`.

| File | Fungsi |
|---|---|
| `narr.ts` | Naskah narator dan pembuatan suaranya |
| `motion.html` | Adegan dan animasinya |
| `render.ts` | Render frame dan potong video dengan narasi |
| `music.ts` | Membuat musik latar |
| `mix.ts` | Mencampur musik di bawah narasi |

### Urutan kerja

```bash
bun narr.ts       # 1. suara narator, satu kalimat per adegan
bun render.ts     # 2. video dengan narasi, tanpa musik
bun music.ts      # 3. musik latar
bun mix.ts        # 4. video dengan musik
```

Narasi harus dibuat lebih dulu, karena lama tiap adegan dihitung dari panjang suaranya ditambah jeda yang dibagi rata.

### Narasi

- Layanan: ElevenLabs, model `eleven_v3`, suara **Citra** (id `RbNgJzKAV7jpYJNtCBpj`).
- Kunci API dibaca dari `game/.env.local` (`ELEVEN_LABS_API_KEY`).
- Tiap kalimat dibuat 3 take, lalu dicek oleh model pendengar (lewat OpenRouter, kunci `OPENROUTER_KEY_PARE` di `titian-backend-go/.env`). Take yang dipilih adalah yang panjangnya di tengah.
- Kolom `tag` berisi arahan gaya seperti `[excited]` atau `[warm]`. Arahan ini tidak dibacakan.
- Kolom `say` dipakai bila yang diucapkan berbeda dari teks di layar, misalnya singkatan dieja per huruf ("T K A") dan alamat web ("Titian Asa, dot com").
- Membuat ulang kalimat tertentu saja: `bun narr.ts 7` (nomor mulai dari 0).
- Total narasi sebaiknya 42 sampai 46 detik untuk video 60 detik.

Cek model pendengar hanya memastikan kata-katanya sesuai `say`. Ia tidak tahu apakah pilihan katanya benar. Pada batch pertama "titik kom" lolos cek padahal seharusnya "dot com". Jadi tetap dengarkan sendiri hasil akhirnya.

### Adegan

- Tiap adegan adalah satu `<section class="scene …">` di `motion.html`. Jumlah adegan harus sama dengan jumlah kalimat di `narr.ts`.
- Unsur yang muncul diberi kelas `a` dan `style="--d:1.5"`. Angka itu adalah detik sejak adegan dimulai, jadi cocokkan dengan saat kata itu diucapkan.
- Adegan penutup diberi atribut `data-end` supaya alamat web kecil di bawah diganti versi besar.
- Membuka `motion.html` langsung di browser memutar pratinjau (lama adegan disamaratakan).
- Melihat beberapa frame saja tanpa render penuh: `FRAMES=20,300,900 bun render.ts`.
- Versi dengan teks narasi di layar: `bun render.ts --subs`.

Render penuh memakan waktu sekitar 5 menit.

### Musik

- Layanan: `google/lyria-3-pro-preview` lewat OpenRouter. Deskripsi musik ada di `PROMPT` dalam `music.ts`.
- Selalu minta "instrumental only, no vocals" dan "about 60 seconds".
- `mix.ts` menurunkan musik otomatis saat narator bicara. Keras-pelan musik diatur di `volume=0.30`.
- `mix.ts` tidak merender ulang gambar, jadi cepat.

### Hasil

Video disimpan di `outputs/video/`. Pola nama: `titian-asa-<judul>-v1.mp4` (narasi saja) dan `-v2-musik.mp4` (dengan musik).

## 6. Daftar periksa sebelum tayang

- [ ] `titianasa.com` terlihat di setiap gambar dan video.
- [ ] Tidak ada kata "main" atau "pemain" untuk Kampung Bahasa Pare.
- [ ] Program yang belum rilis diberi tanda "Segera hadir".
- [ ] Tidak ada angka, testimoni, atau harga yang tidak bisa dibuktikan.
- [ ] Teks tidak terpotong dan tidak menabrak unsur lain di kedua ukuran.
- [ ] Huruf Mandarin, Arab, Jepang, dan Korea tampil benar (bukan kotak kosong).
- [ ] Video sudah ditonton dan didengarkan sampai habis, terutama ucapan nama dan alamat web.
- [ ] Caption ditutup dengan ajakan dan alamat web.

## 7. Jadwal dan caption

- Irama batch pertama: 3 kali seminggu (Senin, Rabu, Jumat) pukul 19.00 WIB, diunggah ke Instagram dan TikTok di hari yang sama.
- Caption Instagram lebih panjang dan boleh memakai daftar beremoji. Caption TikTok satu sampai dua kalimat.
- Tagar tetap: `#TitianAsa #PastiAdaJalannya #BelajarSampaiBisa`. Tambah `#KampungBahasaPare` bila membahas Pare, lalu 2 sampai 4 tagar sesuai topik.
- Contoh lengkap ada di `outputs/konten-sosmed/kalender-dan-caption.md`.

## 8. Yang perlu diketahui

- Bila judul postingan diganti, nama file hasil ikut berubah dan file lama tidak terhapus sendiri. Hapus file lama secara manual supaya tidak terunggah.
- Bila sebuah program rilis, cabut stiker "Segera hadir" di konten baru dan perbarui tabel aturan di bagian 1.
- Pembuatan suara dan musik memakai layanan berbayar. Buat ulang hanya bagian yang perlu.

## 9. Konten khusus Kampung Bahasa Pare (akun @pare.titianasa)

Akun Kampung Bahasa punya batch sendiri di `outputs/konten-sosmed-pare/` (9 postingan gambar, Oktober 2026). Alat dan gayanya sama dengan bagian 2 dan 4; yang berbeda:

| Hal | Aturan |
|---|---|
| Alamat web | **pare.titianasa.com** wajib ada di setiap gambar (bukan titianasa.com). |
| Merek di gambar | "Kampung Bahasa Pare" dengan ikon aplikasinya (`src/assets/pare.png`). |
| Sasaran | Orang yang mau belajar bahasa, dengan **Kampung Inggris Pare** sebagai ikon tempat belajarnya. Empat tipe: yang sedang di Pare, yang mager berangkat tapi ingin belajar dan merasakan suasananya, yang ingin ke Pare tapi belum ada waktu, dan alumni Pare yang ingin nostalgia sambil belajar lagi. Tujuan mereka: pejuang beasiswa, pejuang WHV, calon kru kapal pesiar, dan yang ingin jago speaking. |
| Fokus | Belajar **bahasa Inggris**. Mandarin, Arab, Jepang, dan Korea boleh disinggung, tetapi jarang (di batch pertama hanya postingan 9), dan selalu jujur bahwa jalur dan misinya masih disusun. |
| Kata "kampung" | Jangan berdiri sendiri. Tulis **Kampung Bahasa** atau **Kampung Inggris** (jangan "aturan kampung", "uang kampung", "kabar dari kampung"). |
| Kata lain | Tetap **belajar**, bukan "main", "pemain", atau "game". Pengguna lain disebut "teman belajar". Uang di dalam aplikasi disebut **uang saku**, dan ditegaskan bukan rupiah asli. |
| Istilah khas Pare | Pakai untuk copywriting, asal ada padanannya di aplikasi: English Area (chat wajib bahasa Inggris), punishment (nyawa berkurang), camp, jajan ke pakde dan budhe (Warung Pecel Bu Sri, Bakso Cak Mat, Es Degan Mbak Lis), healing atau hangout di lapangan senja, naik odong-odong (kereta kelinci), sepeda ontel, kenalan dengan teman baru, Speaking Club. Daftar lengkapnya ada di `kalender-dan-caption.md`. |
| Nyawa tanpa batas | Di paket, jangan berhenti di "nyawa tidak pernah habis". Tekankan artinya: **bisa belajar kapan saja dan lebih cepat**, tanpa menunggu 24 jam. |
| Harga | Harga paket Plus dan Pro boleh dipakai, karena tampil di aplikasinya. Cocokkan dulu dengan `internal/pare/premium.go`, dan jangan tayangkan sebelum pembayaran aktif. |
| Isi pelajaran | Kalimat, cara baca, dan arti diambil dari isi kursus (`game/src/game/content/en/`), kemampuan tiap level dari `data/pare/content.json` (`ladder`), cerita tiap level dari `data/pare/missions.json`. Jangan mengarang: untuk WHV dan kapal pesiar, sebut bab yang memang ada, bukan "kelas persiapan" yang tidak ada. |
| Jadwal | Selasa, Kamis, Sabtu pukul 19.00 WIB, supaya berselang dengan akun Titian Asa. |
| Tagar tetap | `#KampungBahasaPare #KampungInggrisPare #BelajarBahasaInggris #TitianAsa` |

Langkah membuatnya sama: ubah `POSTS` di `outputs/konten-sosmed-pare/src/build.ts`, lalu `bun build.ts` dan `bun render.ts` di folder itu. Kolom tambahan di batch ini: `small` (judul panjang, satu ukuran lebih kecil), `per` (baris kecil di bawah judul, dipakai untuk masa berlaku harga), `<s>…</s>` di judul untuk harga coret, dan `<span class='nb'>…</span>` supaya kata bertanda hubung tidak terpotong.

Tangkapan layar diambil dari aplikasi lokal pada ukuran HP 360×640 (skala 3, jadi tepat 1080×1920), dengan jam halaman digeser: pagi supaya gambarnya terang, sekitar 17.15 untuk warna senja. Suasana ramai (lapangan, chat) memakai akun uji lokal sebagai teman belajar lain (`game/scripts/video/bots.ts`). Ambil ulang setiap kali tampilan berubah, dan pastikan versi yang difoto sudah tayang di pare.titianasa.com sebelum kontennya diunggah.

## 10. Batch edukasi 30 hari (21 Okt – 19 Nov 2026)

Batch ketiga akun Titian Asa ada di `outputs/konten-sosmed-edu/` (30 postingan, 125 slide): tips dan infografis seputar TKA, SNBP/SNBT, beasiswa, TOEFL/IELTS, dan teknik belajar. Kalender, caption, dan **tabel sumber beserta status verifikasinya** ada di `kalender-dan-caption.md` di folder itu.

| Hal | Aturan |
|---|---|
| Alat | Sama dengan bagian 4, dengan tata letak infografis tambahan: `steps` (garis waktu dengan chip tanggal), `cmp` (perbandingan dua kolom), `stats` (angka besar), `checks` (daftar centang; `xs: true` untuk tanda silang), `src` (baris sumber kecil), `dense` dan `tight` (slide padat). Isi slide ada di `src/posts-a.ts`, `posts-b.ts`, `posts-c.ts`. |
| Cek otomatis | `bun check.ts` di folder `src/` melaporkan slide yang teksnya meluap. `ONLY=15 bun render.ts` merender satu postingan saja. Render penuh berat; kalau proses terhenti (kode 137), render per postingan. |
| Info yang berubah | Hanya pakai angka dan tanggal yang ada di tabel sumber. Jadwal 2027 (SNBP, SNBT, KIP Kuliah, LPDP) belum resmi per 20 Okt 2026, jadi selalu diberi label "perkiraan" atau "belum final" dan arahan cek situs resmi. Perbarui slide saat panitia mengumumkan. |
| Verifikasi | Fakta TOEFL diperiksa di ets.org. Jadwal TKA hanya terbaca dari repost di situs BBPMP, jadi cek ulang ke pengumuman Kemendikdasmen sebelum tayang. Mata pelajaran, durasi, dan jumlah soal TKA sengaja tidak dipakai karena belum ada sumber resmi. |
| Jam tayang | 12.00 WIB setiap hari (batch pertama tetap Senin, Rabu, Jumat 19.00). |

### Batch November 2026 (30 hari)

Batch kedua ada di `outputs/konten-sosmed-pare-nov/`: 30 postingan, satu per hari (1–30 November), 150 slide. Alatnya sama, dengan dua tambahan:

- Isi slide dipisah ke `src/posts.ts`. Kolom baru: `table` (tabel infografik, `head` dan `rows`) dan `src` (baris sumber kecil). Kalimat di kartu `big` yang panjang otomatis satu ukuran lebih kecil, dan `<b>…</b>` di `sub` tampil merah untuk contoh yang salah.
- Tangkapan layar 3D dibuat dengan `game/scripts/video/social-shots.ts`.

Fakta tes (TOEFL iBT, TOEFL ITP, IELTS, PTE Academic, TOEIC) diambil dari situs resmi pada Oktober 2026, dan sumbernya dicatat di `kalender-dan-caption.md`. Jangan memakai tabel konversi skor tes ke CEFR: sumber resminya tidak seragam. Tetap jujur bahwa Kampung Bahasa bukan kelas persiapan tes.
