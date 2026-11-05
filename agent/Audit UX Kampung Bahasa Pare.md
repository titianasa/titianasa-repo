Audit UX · versi lokal 10 Oktober 2026 · HP Android 360×780

# Audit UX Kampung Bahasa Pare

Dunianya unik dan materinya kuat. Masalahnya ada di jalan menuju belajar: di HP, pemain baru harus melewati formulir panjang, panduan berparagraf, jalan kaki puluhan petak, dan sembilan ikon tanpa label sebelum menjawab satu soal. Laporan ini memetakan titik frustrasi itu dan cara memperbaikinya, dibandingkan dengan aplikasi yang sudah biasa dipakai orang Indonesia.

## Lima hal yang paling perlu diperbaiki

1. **Tombol Back Android menutup game.** Satu usapan balik untuk menutup jendela langsung meninggalkan halaman. Di aplikasi Android mana pun, Back menutup lapisan paling atas.
2. **Pelajaran pertama terlalu jauh.** Pemain baru muncul di kamar Camp dengan panduan panjang dan saldo Rp0, lalu harus jalan sekitar 80 petak ke Miss Kate tanpa penunjuk arah. Di Duolingo soal pertama muncul dalam satu menit.
3. **Latihan menilai jawaban begitu jari menyentuh pilihan.** Di HP, salah sentuh langsung dihitung salah. Tombol LANJUT ada di tengah layar, jauh dari jempol.
4. **Teks sulit dibaca.** Paragraf memakai huruf piksel 16–18 px dan judul 11 px, padahal isi pelajaran dan petunjuk misi banyak berupa paragraf panjang.
5. **Terlalu banyak tempat dan istilah untuk hal yang sama.** Jalur, Buku Perjalanan, panel Level, dan kartu misi sama-sama menjelaskan progres; ada empat jenis "misi"; tombol utama di HP hanya ikon.

## Angka dari pengujian

±80petak jalan kaki dari kamar Camp ke Miss Kate (48 di Kampung Bahasa, 33 di Kampung Inggris)

9tombol ikon tanpa label di layar utama HP; ikon 🎯 dipakai untuk dua fungsi

4jenis "misi": Misi Harian, Misi bab, Misi warga, Misi Besar

14tombol panah 29×29 px di layar buat tokoh, di bawah ukuran sentuh minimum 44 px

±1 MBmateri lima bahasa diunduh sekaligus saat game dibuka (build 6 Okt, sebelum B2–C2 ditambahkan)

[Perbandingan](#banding) [Pendaftaran](#onboarding) [Navigasi](#navigasi) [Belajar](#belajar) [Misi](#misi) [Progres](#progres) [Sosial](#sosial) [Teknis](#teknis) [Rencana](#rencana)

## Dibandingkan dengan aplikasi yang sudah familier

Pengguna datang dengan kebiasaan dari aplikasi belajar (Duolingo, Ruangguru), aplikasi chat (WhatsApp, HelloTalk), dan game HP populer (Mobile Legends, Free Fire, Pokémon GO). Pare menggabungkan ketiganya, jadi pola dari ketiganya berlaku.

| Pola | Yang biasa dialami pengguna | Pare sekarang | Arah perbaikan |
| --- | --- | --- | --- |
| Waktu ke soal pertama | Duolingo: pilih bahasa dan tujuan, langsung pelajaran pertama; akun dibuat sesudahnya. | Layar judul, ajakan install, masuk Google, formulir tokoh 7 baris, kamar Camp dengan panduan panjang, lalu jalan kaki. | Pilih bahasa, langsung pelajaran pertama di depan guru, tokoh dirapikan nanti. |
| Satu tombol "lanjut belajar" | Duolingo: simpul "MULAI" di jalur. Ruangguru: "Lanjutkan belajar" di beranda. | Tombol LANJUT ada, tetapi hanya di dalam Jalur, yang dibuka lewat Miss Kate atau tiga ketukan di Buku Perjalanan. | Tombol ▶ BELAJAR besar yang selalu ada di layar. |
| Mode fokus saat latihan | Duolingo, Babbel: layar penuh; pilih jawaban lalu PERIKSA di bawah; lembar umpan balik hijau/merah dengan suara. | Jendela kecil di atas peta; pilihan langsung dinilai; LANJUT di tengah layar. | Layar penuh di HP, pilih lalu periksa, tombol di zona jempol. |
| Navigasi | Duolingo: 5 tab berlabel di bawah. Lobi Mobile Legends/Free Fire: ikon besar dengan teks. | Joystick kiri dan tombol A kanan sudah sesuai kebiasaan game. Menu lain berupa 9 ikon tanpa label. | 4–5 tombol berlabel; sisanya masuk ke satu menu. |
| Menuju tujuan | Pokémon GO, Genshin: penanda di peta dan panah ke tujuan quest. | Tanda ❗ di atas kepala NPC (terlihat kalau sudah dekat) dan paragraf deskripsi lokasi. | Panah di tepi layar dengan jarak, tombol "tunjukkan di peta". |
| Ngobrol | WhatsApp: daftar percakapan, voice note. HelloTalk: ketuk untuk terjemah, koreksi. | Sudah mirip WhatsApp, ada voice note, telepon, frasa siap pakai, kamus, dan aturan bahasa. | Ketuk pesan untuk terjemah; balasan cepat untuk pemula. |
| Kebiasaan harian | Duolingo: streak dan target harian terlihat di setiap layar. | Streak tidak tampil di layar HP; Misi Harian tersembunyi di ikon 🎯. | Streak dan target harian di bar atas. |
| Tombol Back | Semua aplikasi Android: Back menutup jendela teratas. | Back meninggalkan game. | Back menutup jendela; dua kali di layar utama baru keluar. |

## Pendaftaran dan menit pertama

![Tiga layar HP: layar judul dengan ajakan install, formulir buat tokoh yang panjang, dan layar pertama di kamar Camp yang tertutup panduan berparagraf.](ev-onboarding.jpg)

Akun baru di HP 360×780: ajakan install muncul sebelum masuk; formulir tokoh perlu digulir; layar pertama tertutup panduan, saldo Rp0.

Kritis

### Jalan panjang ke pelajaran pertama

usaha: sedang

Yang terjadi

Pemain baru muncul di kamar Camp, tertutup panduan "Informasi & Panduan" berparagraf, dengan saldo Rp0. Untuk belajar, ia harus keluar Camp, menemukan gerbang Kampung Inggris (sekitar 48 petak), lalu mencari Miss Kate (33 petak lagi). Tidak ada panah penunjuk arah.

Kenapa membuat frustrasi

Orang membuka aplikasi untuk belajar bahasa. Kalau setelah dua menit belum menjawab satu soal, banyak yang menutup aplikasi dan tidak kembali.

Saran

Di akhir pendaftaran tanyakan "Mau belajar bahasa apa?", lalu munculkan pemain di depan guru bahasa itu dan buka Materi pertama otomatis. Ganti panduan panjang dengan tiga kartu pendek saat dibutuhkan: geser joystick, ketuk A di depan orang, ketuk ▶ BELAJAR kapan saja. Beri saldo awal (misalnya Rp10.000) supaya hari pertama tidak buntu.

Tinggi

### Formulir tokoh panjang dan penuh keputusan permanen

usaha: sedang

Yang terjadi

Tujuh baris pengatur penampilan dengan 14 tombol panah 29×29 px, lalu username "tidak bisa diganti", foto profil, dan jenis kelamin "tidak bisa diganti", semuanya sebelum belajar. Padahal Papan Info punya tombol "Ganti nama / username", jadi keterangan "tidak bisa diganti" juga tidak akurat.

Saran

Di awal cukup nama panggilan dan jenis kelamin, dengan tokoh acak (tombol 🎲) yang bisa diganti di lemari. Username dibuat otomatis dari nama, bisa diubah nanti. Duolingo meminta profil setelah pelajaran pertama.

Tinggi

### Ajakan install muncul di layar judul

usaha: kecil

Yang terjadi

Kotak "Install Kampung Bahasa Pare" menutupi layar judul sebelum pemain tahu gamenya seperti apa.

Saran

Tampilkan setelah pelajaran pertama selesai, atau di kunjungan hari kedua, dengan alasan yang terasa ("supaya streak-mu tidak putus").

## Navigasi dan layar utama

![Tiga layar HP: layar utama dengan deretan ikon di atas dan kanan, pelacak misi di atas, dan Buku Perjalanan dengan tab ikon tanpa label.](ev-hud.jpg)

Layar utama: 9 ikon tanpa label. Di Buku Perjalanan, tab di HP hanya ikon (🗺️ 🎓 ⭐ 🏘️ 🏅), padahal di desktop berlabel.

Kritis

### Tombol Back Android keluar dari game

usaha: kecil

Yang terjadi

Dengan kartu misi terbuka, perintah "kembali" browser meninggalkan halaman. Kode game tidak menangani riwayat (`popstate`). Di aplikasi yang dipasang ke layar utama, ini berarti aplikasi tertutup.

Kenapa membuat frustrasi

Usapan Back adalah cara paling umum menutup jendela di Android. Satu usapan bisa membuang sesi latihan yang sedang berjalan.

Saran

Setiap jendela yang dibuka menambah satu entri riwayat; Back menutup jendela teratas. Di layar utama, Back pertama memunculkan "Tekan sekali lagi untuk keluar".

Tinggi

### Sembilan ikon tanpa label

usaha: sedang

Yang terjadi

Di atas: 🎯 (Misi Harian), 📋 (Papan Info), 🧭 (Buku Perjalanan), 📖 (Kamus), ?. Di kanan: 🗺️, ＋, －, 🎯 (kembali ke karakter). Arti ikon hanya diketahui lewat coba-coba, dan 🎯 dipakai untuk dua hal. Pintasan keyboard (Q, P, J, K, L) tidak ada di HP.

Saran

Sisakan 4 tombol berlabel teks pendek: ▶ Belajar, ⭐ Misi, 💬 Chat, 👤 Aku (Kamus, Info, Bantuan masuk ke sini). Zoom sudah bisa dengan cubit, jadi ＋ dan － bisa dilipat ke Peta. Joystick dan tombol A tetap di tempatnya, karena sudah sesuai kebiasaan game HP.

Tinggi

### Tab Buku Perjalanan hanya ikon di HP

usaha: kecil

Yang terjadi

Label "Peta, Level ini, Misi, Warga, Stempel" hilang di layar kecil. Tab bahasa makan tiga baris sebelum isi terlihat. Hal yang sama terjadi di Kamus.

Saran

Tampilkan label pendek di bawah ikon; tab bahasa jadi satu baris yang bisa digeser, atau satu tombol "🇬🇧 Inggris ▾".

Sedang

### Target sentuh terlalu kecil dan label aksi yang keliru

usaha: kecil

Yang terjadi

Panah tokoh 29 px, tab ikon 36×33, tab bahasa tinggi 29, tombol 🔊 40×37, tombol ⭐ MISI tinggi 33. Saat menghadap Miss Kate di tengah misi, ajakan tetap berbunyi "Ketuk untuk masuk kelas" padahal tombol A membuka misi.

Saran

Minimal 44×44 px untuk semua yang bisa disentuh. Teks ajakan mengikuti aksi sebenarnya ("Ketuk untuk lanjutkan misi").

## Belajar: jalur, materi, latihan

![Empat layar HP: Jalur Inggris dengan tombol LANJUT hijau, soal pilihan ganda di jendela kecil, umpan balik salah dengan tombol LANJUT di tengah, dan layar hasil sederhana.](ev-lesson.jpg)

Latihan · Kata 1: soal tampil sebagai jendela kecil di atas peta; satu sentuhan langsung dinilai; layar hasil hanya persentase, XP, dan uang.

Tinggi

### Pilihan langsung dinilai saat disentuh

usaha: kecil

Yang terjadi

Begitu satu pilihan disentuh, jawaban dikunci dan "Kurang tepat" muncul. Tombol LANJUT ada di dalam kotak umpan balik, sekitar tengah layar.

Kenapa membuat frustrasi

Di layar sentuh, salah sentuh sering terjadi, terutama saat menggulir. Dinilai salah karena jari meleset terasa tidak adil.

Saran

Pola Duolingo: pilih dulu (bisa ganti), lalu tombol PERIKSA lebar di bawah layar. Umpan balik muncul sebagai lembar dari bawah, hijau atau merah, dengan suara dan getar singkat; tombol LANJUT di posisi yang sama dengan PERIKSA, supaya jempol tidak berpindah.

Tinggi

### Jalur hanya bisa dibuka dari guru

usaha: kecil

Yang terjadi

Jalur belajar dibuka dengan mendatangi Miss Kate atau gedung kelas, atau lewat Buku Perjalanan, tab 🎓, lalu "Buka Jalur". Pemain yang sedang di kota atau luar negeri harus pulang atau tahu jalan pintas itu.

Saran

Tombol ▶ BELAJAR yang selalu ada dan membuka jalur bahasa fokus dari mana saja. Kalau ingin tetap mendorong pemain datang ke kelas, beri bonus kecil saat belajar di kelas, jangan jadikan syarat.

Tinggi

### Teks sulit dibaca di HP

usaha: sedang

Yang terjadi

Paragraf memakai huruf piksel VT323 16–18 px; judul jendela memakai Press Start 2P 11 px. VT323 punya tinggi huruf kecil yang pendek, sehingga 16 px terbaca seperti 11–12 px huruf biasa. Banyak isi berupa paragraf panjang (petunjuk misi, panduan, keterangan jalur).

Saran

Huruf piksel cukup untuk judul dan merek. Isi pelajaran, petunjuk, dan paragraf memakai sans yang jelas, minimal 16 px; kata yang sedang dipelajari minimal 28 px. Sekalian pangkas teks: satu kalimat per petunjuk.

Tinggi

### Latihan tidak dalam mode fokus

usaha: sedang

Yang terjadi

Soal tampil sebagai jendela kecil; bar status, ikon, dan peta tetap terlihat di sekelilingnya. Bilah kemajuan tipis dan ✕ berdempetan dengannya.

Saran

Di HP, latihan memenuhi layar: ✕ dan bilah kemajuan tebal di atas, soal di tengah, tombol di bawah. Konfirmasi "Yakin berhenti? Kemajuanmu tersimpan" saat ✕ disentuh.

Sedang

### Layar hasil terlalu tipis

usaha: kecil

Yang terjadi

"Benar pada percobaan pertama: 87%", XP, uang, dan satu tombol LANJUT. Tidak ada kata yang perlu diulang, streak, atau target harian.

Saran

Tampilkan akurasi, kata yang tadi salah (ketuk untuk dengar lagi), kemajuan target harian dan streak, lalu tombol utama yang menyebut langkah berikutnya ("Lanjut: Materi · Kata 2").

Sedang

### Materi pasif dan jalur yang panjang

usaha: sedang

Yang terjadi

Materi berupa daftar kata dengan tombol 🔊 yang harus disentuh satu per satu. Jalur memakai satu kartu besar per langkah (10 per bab), dengan bab terkunci di bawahnya.

Saran

Materi sebagai kartu satu per satu: gambar besar, audio otomatis, geser untuk lanjut. Jalur sebagai simpul ringkas yang otomatis menggulir ke langkah aktif, dengan detail saat simpul diketuk.

## Misi

![Tiga layar HP: bagian bawah kartu misi dengan rumus nilai dan tiga tombol, layar misi berjalan dengan deskripsi lokasi panjang, dan layar saat pemain berdiri di depan Miss Kate dengan tombol Bicara.](ev-mission.jpg)

Kenalan dengan tetangga: rumus penilaian di kartu misi, deskripsi lokasi berparagraf yang muncul dua kali, tombol "Bicara dengan Miss Kate" saat sudah di depannya.

Tinggi

### Menemukan target misi bergantung pada paragraf

usaha: sedang

Yang terjadi

Lokasi ditulis sebagai paragraf ("Miss Kate, guru berjaket biru berambut pirang panjang, berdiri di halaman depan ENGLISH ACADEMY, kampus besar beratap biru tua…") dan muncul dua kali di layar yang sama. Perintahnya: "Tutup jendela ini, cari orangnya di peta".

Saran

Panah di tepi layar yang menunjuk target, dengan jarak ("Miss Kate · 24 langkah"); tombol "Tunjukkan di peta" yang membuka peta dengan penanda. Untuk target jauh, opsi jalan otomatis atau ojek berbayar kecil. Deskripsi teks tetap ada, cukup satu kalimat.

Tinggi

### Kartu misi panjang dan teknis

usaha: kecil

Yang terjadi

Kartu menampilkan rumus nilai ("Hasil 40 · Bahasa 40 · Mandiri 20, petunjuk 2: −2, petunjuk 3: −5"), syarat, hasil nyata, kalimat kunci, lalu tiga tombol sama besar (NANTI, LATIHAN DULU, MULAI) di ujung bawah setelah digulir.

Saran

Kartu ringkas: judul, satu kalimat cerita, hadiah, durasi. Tombol MULAI besar menempel di bawah layar; LATIHAN DULU sebagai tautan kecil. Rumus nilai masuk ke lipatan "Cara dinilai".

Sedang

### Istilah dan urutan daftar misi

usaha: kecil

Yang terjadi

Ada Misi Harian, Misi bab, Misi warga, Misi Besar, ditambah Praktik, Cek bab, Tantangan, dan Latihan bebas. Di daftar misi, Misi Besar yang masih terkunci tampil paling atas.

Saran

Ganti "Misi Harian" menjadi "Target harian". Urutkan misi: yang bisa dimainkan sekarang di atas, yang terkunci di bawah dengan satu baris alasan.

Bagus

### Tombol aksi saat sudah di depan NPC

Yang terjadi

Saat pemain berdiri di depan Miss Kate, kartu misi menampilkan tombol "Bicara dengan Miss Kate". Pola ini bisa diperluas: saat dekat target, tombol aksi besar langsung muncul di bawah layar tanpa membuka kartu.

## Progres dan level

![Tiga layar HP: Buku Perjalanan dengan daftar syarat naik level, panel Level dengan daftar syarat yang sama dan ujian lompat level, serta jendela Misi Harian.](ev-progress.jpg)

Syarat naik level yang sama muncul di Buku Perjalanan dan panel Level; Misi Harian adalah jenis "misi" keempat.

Sedang

### Informasi yang sama di banyak tempat

usaha: sedang

Yang terjadi

Syarat naik level ("Bab lulus 1/5, Misi bab 0/5, Misi warga 0/2, Misi Besar 0/1") ada di Buku Perjalanan dan di panel Level. Jalur dan kartu Misi Besar juga menjelaskan apa yang masih terkunci.

Saran

Satu layar per bahasa: tangga level di atas, jalur bab di tengah (misi bab tampil sebagai simpul di jalur), syarat naik level sebagai satu bilah kemajuan. Buku Perjalanan cukup untuk koleksi: warga, stempel, peta.

Sedang

### Sistem hidup aktif sejak menit pertama

usaha: sedang

Yang terjadi

Lapar, stamina, tidur 5 jam, pingsan, nyawa, dan uang sudah berjalan sejak pemain baru masuk, padahal ia belum tahu cara belajar.

Saran

Aktifkan bertahap: misalnya lapar dan pingsan baru berlaku setelah Bab 1 selesai, atau sesudah hari pertama. Cara ini dipakai banyak game: sistem dibuka satu per satu bersama penjelasannya.

## Chat, voice note, dan English area

![Dua layar HP: daftar percakapan bergaya WhatsApp dan chat umum Kampung Inggris dengan banner aturan bahasa.](ev-chat.jpg)

Chat terasa seperti WhatsApp. Banner "Hanya bahasa Inggris" selalu terlihat di Kampung Inggris.

Bagus

### Bagian yang paling siap

Yang terjadi

Daftar percakapan, voice note, telepon, frasa siap pakai (💡), kamus (🔤), dan peringatan aturan bahasa sebelum pesan terkirim. Ini keunggulan nyata dibanding Duolingo, yang tidak punya percakapan dengan orang sungguhan.

Saran

Tambahkan ketuk pesan untuk melihat terjemahan (seperti HelloTalk) dan balasan cepat sesuai level untuk pemain Basic, supaya pemula berani menulis pesan pertama.

## Teknis di HP

Tinggi

### Semua materi diunduh saat game dibuka

usaha: besar

Yang terjadi

Build produksi 6 Oktober memuat materi lima bahasa dalam satu berkas JavaScript 3,2 MB (sekitar 1,0 MB setelah dikompresi). Sejak itu materi Inggris B2–C2 ditambahkan (sumber materi Inggris kini 1,4 MB, bahasa lain 1,8 MB), jadi build berikutnya lebih besar.

Kenapa membuat frustrasi

Di paket data dan sinyal 4G yang lemah, pembukaan pertama terasa lama, dan HP murah lebih lambat memproses berkas sebesar itu.

Saran

Muat materi per bahasa dan per level saat dibutuhkan (server sudah punya `/pare/content`), lalu simpan di cache perangkat.

Sedang

### Iklan sela saat pindah zona

usaha: kecil

Yang terjadi

Iklan sela muncul saat masuk zona baru, paling sering tiap 3 menit. Langkah misi sering meminta pemain pindah zona, jadi iklan bisa memotong misi.

Saran

Tidak ada iklan sela di sesi pertama dan pekan pertama; tidak ada iklan sela saat misi sedang berjalan. Iklan berhadiah (pilihan pemain) tetap boleh.

## Yang sudah bagus dan perlu dipertahankan

- Dunia kampung yang hidup: alasan orang memilih Pare dibanding aplikasi kuis biasa.
- Urutan Materi, Latihan, Praktik, Cek bab, dengan XP yang tidak pernah berkurang di jalur.
- Soal yang salah muncul lagi dalam latihan yang sama.
- Misi yang menerapkan bahasa ke warga kampung, dengan petunjuk bertingkat dan tombol "Lanjut nanti".
- Joystick di kiri dan tombol A di kanan, sesuai kebiasaan game HP.
- Chat, voice note, telepon, dan aturan bahasa per kampung.
- Jendela naik level yang baru (animasi, fanfare, tangga level).

## Rencana perbaikan

Diurutkan menurut dampak terhadap pemain baru dibanding besar pekerjaannya.

Tahap 1 · 1–3 hari

### Hilangkan penyebab keluar

- Back Android menutup jendela, bukan game.
- Latihan: pilih lalu PERIKSA, tombol di bawah layar.
- Tombol ▶ BELAJAR yang selalu ada.
- Label teks di tab ikon (Buku Perjalanan, Kamus).
- Ajakan install dipindah ke setelah pelajaran pertama.
- Saldo awal, target sentuh 44 px, teks ajakan NPC yang benar.

Tahap 2 · 1–2 minggu

### Satu menit ke soal pertama

- Pendaftaran baru: pilih bahasa, pelajaran pertama, baru tokoh.
- Mode fokus latihan di HP dan layar hasil yang lengkap.
- Huruf isi yang mudah dibaca; teks dipangkas.
- Kartu misi ringkas dan panah penunjuk target.
- Streak dan target harian di bar atas; "Target harian" menggantikan "Misi Harian".

Tahap 3 · 2–4 minggu

### Rapikan strukturnya

- Navigasi 4 tombol berlabel.
- Satu layar progres per bahasa (jalur, misi, syarat naik level).
- Jalur bentuk simpul dan materi bentuk kartu.
- Sistem hidup dibuka bertahap.
- Materi dimuat per bahasa dan level.
- Chat: ketuk untuk terjemah, balasan cepat.

## Cara mengukur hasilnya

- **Waktu ke soal pertama:** dari aplikasi dibuka sampai soal pertama dijawab. Target di bawah 60 detik untuk akun baru.
- **Pelajaran pertama selesai:** persentase akun baru yang menyelesaikan Latihan · Kata 1 di sesi pertama.
- **Retensi hari ke-1 dan ke-7.**
- **Latihan yang ditinggalkan di tengah,** dipisah antara ✕ dan keluar aplikasi.
- **Jawaban salah dalam 0,4 detik setelah soal muncul,** sebagai tanda salah sentuh (seharusnya turun setelah pola pilih-lalu-periksa).

**Cara audit dilakukan.** Game versi lokal (localhost, 10 Oktober 2026) dibuka di browser HP tersimulasi 360×780 dengan mode sentuh. Satu akun baru dibuat untuk alur pendaftaran; pemain uji di level Basic dipakai untuk jalur, latihan, misi, Buku Perjalanan, Kamus, Peta, dan chat. Ukuran tombol, ukuran huruf, dan jarak jalan kaki diukur dari halaman dan peta.

**Yang belum diuji.** HP fisik (kecepatan di HP murah, keyboard virtual yang menutupi kolom ketik), tombol masuk Google (tidak tampil di versi lokal), soal berbicara dengan mikrofon, menerima telepon, dan Safari di iPhone. Perbandingan dengan aplikasi lain berdasarkan pola umum aplikasi tersebut, bukan riset pengguna. Langkah berikutnya yang paling berguna: minta 5 orang pemula memakai HP-nya sendiri untuk "mempelajari kata pertama" tanpa dibantu, lalu catat di mana mereka berhenti.
## Status pengerjaan (2026-10-10)

Semua butir Tahap 1, 2, dan 3 serta temuan di luar rencana sudah dikerjakan di kode dan diuji di emulasi layar HP 360×780 (rincian di `docs/STATE.md`). Yang masih di luar kode: uji di HP sungguhan, deploy backend (saldo awal Rp10.000, perlindungan pemain baru), dan push game. Angka hasil bisa dihitung dengan `titian-backend-go/db/reports/ux_metrics.sql`.
