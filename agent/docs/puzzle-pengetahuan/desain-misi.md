# Desain misi Puzzle Pengetahuan

Rancangan pengalaman belajar, 2026-11-01. Melengkapi [metode-belajar.md](metode-belajar.md). Dokumen itu menetapkan prinsip belajarnya; dokumen ini menetapkan bagaimana prinsip itu dirasakan siswa.

> **Inti yang tidak boleh hilang (arahan pemilik, 2026-11-01):** pengetahuan disusun dari kepingan kecil yang saling terhubung seperti saraf. Siswa harus selalu bisa melihat apa yang sudah diketahui, apa yang belum, dan apa kaitannya. Misi adalah cara menumbuhkan jaringan itu, bukan penggantinya. Lihat bagian "Jaringan pengetahuan".

> **Revisi alur (arahan pemilik, 2026-11-01):** siswa memilih sendiri di awal, *Lihat penjelasan dulu* atau *Langsung kerjakan*. Urutan wajib "aktivitas dulu" di bawah tidak lagi berlaku.
> - Penjelasan dulu: Misi → Penjelasan → Latihan → Uji akhir.
> - Langsung kerjakan: Misi → Tebak → hasil → Uji akhir atau Pelajari.
> - "Bos" diganti **Uji akhir** di tampilan.
> - Setiap akhir sesi punya tombol *Pelajari lagi*. Kalau banyak salah (2 atau lebih di uji akhir, 3 atau lebih di pelajaran, atau gagal ujian), tombol itu menjadi rekomendasi utama.
> - Pelajaran kata punya pilihan yang sama: *Pelajari katanya dulu* atau *Langsung kerjakan*.

## Ringkasan

Masukan pemilik: aktivitas harus datang lebih dulu, materi hadir sebagai animasi di tengah belajar, pemula Indonesia butuh konteks, yang sudah bisa tidak boleh merasa diremehkan, dan yang mudah bosan butuh semangat lewat misi.

Tahap A sudah benar pada prinsipnya, tetapi salah pada bentuknya. Lima tab Lihat–Coba–Buktikan–Pakai–Ingat terasa seperti formulir sekolah, dan masih dimulai dari membaca.

Usulan: satu puzzle menjadi **satu misi 5–7 menit**, satu layar penuh, tanpa tab. Urutannya:

> **Misi → Tebak → Aha! → Latihan → Bos → Hadiah**, lalu **Ingat** di hari-hari berikutnya

Empat aturan menjaga rancangan ini:
1. **Aktivitas dulu, tapi selalu bisa ditebak.** Tidak ada aktivitas tanpa konteks dan bantuan.
2. **Penjelasan datang setelah rasa ingin tahu muncul**, berupa animasi pendek yang membandingkan dengan bahasa Indonesia.
3. **Tebak juga berfungsi sebagai pintu lompat** bagi yang sudah bisa.
4. **Hadiah hanya untuk bukti belajar.** Dopamin tidak boleh bisa didapat dengan cara yang tidak melatih bahasa.

## 1. Apa yang berubah dari Tahap A

| Tahap A (sekarang) | Desain misi | Yang dipakai ulang |
|---|---|---|
| 5 tab yang dipilih sendiri | Satu alur layar penuh, satu kartu per layar, bilah progres | Logika status di server |
| Lihat: baca pola dulu | Misi (konteks) → Tebak (aktivitas) → Aha! (animasi) | Pola, contoh, `mistake` |
| Coba: tiga tingkat bantuan | Latihan: tingkat yang sama, ditambah format selang-seling dan kombo | Mesin fading dan Blockly |
| Buktikan: yakin/ragu | Bos: tanpa bantuan; yakin/ragu menjadi taruhan XP | `QuestionCard`, `confidence` |
| Pakai: tulis kalimat baru | Bagian penutup Bos, memakai tokoh misi; versi penuh di Kampung Bahasa (Tahap C) | Tugas `pakai` |
| Ingat: sesi ulangan | Tetap ada, ditambah soal lama yang diselipkan ke misi baru | `POST /puzzles/review`, syarat hari lain |
| Daftar 27 puzzle per level | Peta bab bertema | `chapters.ts`: A1 sudah punya 14 bab |

Definisi "dikuasai" tidak berubah: lolos bukti, bisa memakai, dan ingat di hari lain.

## 2. Satu misi, layar demi layar

Contoh: puzzle **have / has**, bab keluarga di level A1. Tokoh dan situasi diambil dari isi Kampung Bahasa.

| # | Layar | Yang terjadi | Tujuan | Durasi |
|---|---|---|---|---|
| 1 | **Misi** | "Emma, tetangga barumu, bertanya tentang keluargamu. Jawab supaya dia mengajakmu main ke rumah." Teks Indonesia, audio, dan 3 bintang target | Tahu *untuk apa* belajar ini | 10 detik |
| 2–4 | **Tebak** | Tiga aktivitas mudah: dengar lalu pilih gambar, lalu isi "He ___ a bike" dari dua pilihan. Kata bisa diketuk untuk melihat arti dan cara baca. **Salah tidak dihukum**: "Tebakan bagus, ayo lihat kenapa" | Otak mencari polanya sendiri | 1 menit |
| 5 | **Aha!** | Animasi 20–40 detik (bagian 3), dimulai dari tebakan siswa: "Tadi kamu pilih *have*. Coba lihat…" | Menjawab rasa ingin tahu | 30 detik |
| 6–10 | **Latihan** | Format berganti setiap 1–2 kartu: susun blok, dengar-susun, isi, ketik. Bantuan berkurang; kombo naik setiap benar | Membangun kemampuan tanpa bosan | 2–3 menit |
| 11–13 | **Bos** | Emma bertanya langsung, tanpa bantuan. Siswa memilih yakin atau ragu sebelum kirim. Satu kalimat terakhir ditulis sendiri tentang keluarganya | Bukti ingatan dan pemakaian | 1–2 menit |
| 14 | **Hadiah** | Keping puzzle terbang ke koleksi, bintang, XP, progres bab, dan satu kalimat lanjutan: "Besok Emma tanya lagi. Masih ingat?" | Rasa selesai dan alasan kembali | 10 detik |

Selipan: setiap misi berisi 1–2 soal dari puzzle lama yang sudah dimiliki, tanpa label "ulangan". Pengulangan terjadi di dalam cerita, sehingga tidak terasa seperti kewajiban.

## 3. Animasi Aha!: pembeda untuk pelajar Indonesia

**Isinya perbandingan dengan bahasa Indonesia**, bukan definisi tata bahasa:

> "Saya **punya**, dia **punya**: dalam bahasa Indonesia katanya sama. Dalam bahasa Inggris, begitu subjeknya *he/she/it*, *have* berubah jadi *has*."
> (Blok `She` masuk, blok `have` berputar menjadi `has`, lalu berhenti dan siswa diminta mengetuk.)

Prinsip:
- Maksimal 40 detik dan satu ide per animasi.
- **Berhenti di tengah untuk satu ketukan**, supaya siswa tetap aktif.
- Narasi bahasa Indonesia dengan teks, bisa diulang dan bisa dilewati.
- Kesalahan khas orang Indonesia diambil dari `mistake` dan ditunjukkan langsung.

**Cara produksinya: bukan video.** 164 video mahal dan sulit direvisi. Yang dibuat adalah satu pemutar animasi berbasis data:
- Naskah berupa JSON adegan: tampilkan kalimat, sorot kata, ubah kata, bandingkan, tanya.
- Dirender dengan React dan `framer-motion` (sudah ada di titian-web), memakai blok yang sama dengan editor.
- AI membuat draf naskah dari `pattern`, `explain`, dan `mistake`; manusia meninjau sebelum terbit.
- Narasi memakai TTS yang sudah ada di backend, lalu disimpan supaya tidak dibuat ulang.

Risikonya kualitas: animasi hasil templat bisa terasa kaku. Karena itu lima animasi pertama dibuat dan diuji dulu sebelum produksi massal.

## 4. Tiga tipe pelajar dalam satu misi

| | **Pemula total** | **Sudah bisa** | **Mudah bosan** |
|---|---|---|---|
| Masalah | Tidak paham ini tentang apa | Merasa diremehkan | Pergi sebelum selesai |
| Solusi | Konteks Indonesia di layar Misi, audio, cara baca, gambar, Tebak yang pasti bisa ditebak | Tebak menjadi pintu lompat: benar semua dan yakin → "Kamu sudah bisa" → langsung Tantangan | Misi 5–7 menit, kartu berganti format, progres selalu terlihat, tidak ada layar teks panjang |
| Rasa yang dituju | "Oh, ini buat ngobrol sama Emma" | "Ini menantang juga" | "Satu lagi deh" |

**Tantangan** membuat yang mahir tidak merasa receh. Isinya:
- mencari kesalahan di paragraf nyata;
- mengubah bentuk kalimat;
- soal bergaya TOEFL atau IELTS;
- menjawab "kenapa bukan yang satunya?".

Lulus memberi bintang emas. Soal jenis ini belum ada dan perlu dibuat. Tes penempatan (Tahap B) melengkapinya, supaya siswa mahir mulai dari levelnya, bukan dari Basic.

Nada juga disesuaikan: orang dewasa dan pencari skor ujian mendapat konteks kerja, kuliah, dan ujian, bukan maskot anak-anak.

## 5. Pola mengingat

Lima lapisan, dari yang paling terasa sampai yang paling sunyi:
1. **Selipan.** Soal lama muncul di misi baru.
2. **Ulangan harian 2 menit.** Soal campuran; nama aturannya baru muncul setelah dijawab.
3. **Puzzle retak.** Puzzle yang kekuatannya memudar tampak retak di koleksi. Ulangan memperbaikinya. Ini memberi alasan yang terlihat untuk mengulang.
4. **Kembalinya tokoh.** Emma bertanya lagi besok, jadi ulangan terasa sebagai kelanjutan cerita.
5. **Dipakai di Kampung Bahasa.** Puzzle dipakai dalam obrolan dan misi nyata (Tahap C).

## 6. Sistem semangat

Hadiah bekerja di beberapa jarak waktu. Banyak bagiannya sudah ada di backend.

| Jarak | Hadiah | Status |
|---|---|---|
| Detik | Suara, getar kecil, animasi benar, kombo | Baru |
| Menit | 3 bintang per misi, keping puzzle | Baru |
| Hari | Streak, 3 misi harian, peti setelah ulangan | Streak dan misi harian sudah ada; peti baru |
| Minggu | Liga | Sudah ada |
| Panjang | Bab selesai → membuka misi besar dan bagian baru di Kampung Bahasa | Misi per level sudah ada; penyambungannya baru |

**Taruhan yakin/ragu:** yakin dan benar +2 bonus, ragu dan benar +1, yakin dan salah 0, ragu dan salah 0. Ini mengubah penilaian diri menjadi permainan, sekaligus melatih kejujuran terhadap diri sendiri.

**Pagar supaya gamifikasi tidak merusak belajar:**
1. XP hanya dari menjawab, bukan dari menonton atau membaca. Ini sejalan dengan aturan yang sudah berlaku di Pare: hadiah harus datang dari kegiatan bahasa sungguhan.
2. Mengulang soal yang sama memberi XP makin kecil, supaya tidak bisa ditambang.
3. Nyawa hanya berlaku di Bos. Di Tebak dan Latihan, salah adalah bagian dari belajar.
4. Gagal Bos berarti latihan singkat lalu coba lagi. **Penguasaan tidak bisa dibeli.**
5. Streak bisa diselamatkan dengan satu ulangan 1 menit, dan ada jatah pelindung streak. Mode anak tidak memakai rasa takut kehilangan.
6. Tidak ada bonus kecepatan untuk pemula, karena kecepatan mengorbankan pemahaman.
7. Notifikasi dibatasi satu per hari.

## 7. Peta bab

Daftar datar diganti jalur bab yang diambil dari `chapters.ts`:
- Level → bab bertema → misi.
- Setiap bab ditutup dengan misi besar dan satu bagian Kampung Bahasa yang terbuka.
- Target pendek terlihat: "Bab Keluarga 3/5", bukan "3/164".

Graf prasyarat tetap bekerja di belakang layar untuk diagnosis, dan tab Peta tetap ada untuk yang ingin melihatnya.

## Jaringan pengetahuan

Dibangun setelah pemilik menilai prototipe M1 kehilangan gagasan utamanya: tidak ada visualisasi dan tidak ada label.

**Tiga lapis kepingan** (Basic: 48 kata, 6 konsep, 4 kemampuan):

| Lapis | Contoh | Isi |
|---|---|---|
| Kata | `I`, `am`, `hungry` | Arti, cara baca, audio, label peran |
| Konsep | Kata ganti orang, to be | Satu misi |
| Kemampuan | Memperkenalkan diri | Kalimat utuh, misalnya "I am {nama}."; tidak punya skor sendiri, hanya mengikuti kepingannya |

**Label:** dua bahasa dan detail (arahan pemilik). Warna menandai keluarga kata (Noun, Verb, Pronoun, dan seterusnya), sedangkan label menyebut *part of speech*-nya, misalnya *Concrete noun · Kata benda konkret*, *Uncountable noun · Kata benda tak terhitung*, *Proper noun · Nama diri*, *Linking verb (to be) · Kata kerja penghubung*, *Verb (V1) · Kata kerja bentuk 1*. Setiap kata ditetapkan di `jenis` pada `en-misi.json`, karena kategori game tidak bisa membedakannya. Bentuk V2 dan V3 muncul saat level yang mengajarkannya masuk jaringan.

**Tempat kemunculannya:**
- Jaringan menjadi layar utama level, dengan tab Misi di sampingnya. Tampil utuh sebentar, lalu zoom ke kepingan yang sedang dikerjakan.
- Ketuk kepingan: statusnya, arti dan cara baca, "Dibangun dari", dan "Dipakai di".
- Bedah kalimat di awal misi, setelah latihan benar, dan di Hadiah. Yang dimiliki menyala, yang belum berupa garis kosong.
- Kalimat misi memakai nama siswa dan menjadi soal terakhir Bos.
- Hadiah menyebut jumlah kepingan baru yang menyala.

**Menyala karena bukti:** soal Bos berlabel `assess_type = 'piece'` untuk setiap kata di dalamnya, jadi kalimat yang benar menguatkan kata-katanya tanpa menambah tugas konsep. Latihan berbantuan tidak menyalakan apa pun.

**Batasan saat ini:**
- Hanya level Basic. A1 ke atas belum punya kamus kepingan dan kemampuan.
- Kalimat salah menurunkan semua kata di dalamnya, walau hanya satu kata yang keliru.
- Kata yang tidak ada di kamus ditampilkan sebagai "Nama".

## Kartu penjelasan

Penjelasan berbentuk set kartu yang digeser seperti carousel Instagram, sekaligus bisa diunggah sebagai konten. Ada dua dimensi: 4:5 tampil di desktop, 9:16 tampil di HP. Tombol Bagikan membuka pilihan dimensi (4:5 atau 9:16), format (PNG atau MP4), dan isi (kartu ini atau semua), lalu Simpan atau Bagikan. Simpan "semua" mengunduh satu zip.

- **Isi set:** sampul, satu kartu per adegan naskah, kartu penutup. Naskah di `aha` pada `en-misi.json`.
- **Merek:** gaya stiker `panduan-konten-sosmed.md`, chip Titian Asa, dan `titianasa.com` di setiap kartu.
- **Warna punya arti:** di kartu perbandingan, kata dan padanannya satu warna, dan menyala bergantian. Kata tanpa padanan bergaris putus-putus. Di kartu lain, merah berarti salah, hijau berarti benar, emas berarti kata yang berpindah.
- **Istilah:** nama materi memakai istilah akademik Inggris (`materi` di naskah): `Part of Speech · Pronoun`, `Grammar · Simple Present`.
- **Berkas:** `outputs/konten-sosmed-puzzle/src/render.ts` merekam tiap kartu di kedua dimensi (1080×1350 dan 1080×1920) menjadi MP4 dan PNG, plus zip per set. Halaman sumbernya `/puzzle-kartu/[slug]?kartu=n&rasio=9x16`. Naskah untuk halaman itu ada di `titian-web/src/content/puzzle-kartu.json`, salinan dari `en-misi.json`, jadi perlu dibuat ulang setiap naskah berubah.

**Aturan teks:** tulis seperti guru les bicara ke murid. Kalimat pendek, pakai "kamu", boleh "nggak" dan "gampang". Hindari pembuka bergaya AI ("Kabar baik", "Mari kita"), pujian kosong ("Mantap", "Luar biasa"), dan kata buku ("merupakan", "memakai" kalau "pakai" cukup).

## Isi dari kurikulum game

Pemilik menilai materi Puzzle tipis dibanding game. Penyebabnya: impor awal hanya mengambil tata bahasa. Sumber materi Puzzle adalah konten Kampung Bahasa; jangan menulis ulang yang sudah ada di sana.

**Bentuk satu bab, sama dengan game:** pelajaran kata → misi konsep → praktik (situasi, bacaan, dialog) → ujian bab. Level ditutup ujian level.

| Bagian | Sumber | Status |
|---|---|---|
| Pelajaran kata | `vocab` game: ikon, cara baca, arti. Setiap kata mendapat kartu kenal, soal arti, dan soal dengar | Basic |
| Praktik | `situations`, `readings`, `dialogues`, `phrases` | Basic |
| Ujian bab | Soal bab itu, 10 soal acak, 3 nyawa | Basic |
| Ujian level | Pola ujian game: Kosakata 10, Tata bahasa 10, Membaca 8, Menyimak 8. Lulus 80% total dan 60% tiap bagian | Basic, tanpa Teori, Menulis, dan Berbicara |
| Audio bahasa Inggris | Klip rekaman game (`/pare/audio/clip/{key}`), tanpa biaya TTS. Kalimat yang tidak ada rekamannya memakai suara browser | Semua level siap dipakai |

Pelajaran dibuat otomatis oleh `import_puzzles` dari `data/puzzle/en-bahan.json`. Basic kini 28 langkah. Level lain tinggal `-lesson-levels`, setelah dicek pembagian kata per bab, peta kemampuan (`abilityOfChapter`), dan beban jaringan (A1 punya 561 kata).

Misi dunia game (pergi ke tempat, membeli, berbicara dengan warga) tidak dipindahkan: tempatnya tetap di Kampung Bahasa, dan disambungkan di tahap M4.

## 8. Tahapan

**Status 2026-11-01: M1 selesai di dev untuk seluruh level Basic, belum di-deploy.** Pemilik menyetujui kelima keputusan di bawah. Bab "Sapaan & perkenalan" hanya berisi 2 konsep, jadi cakupan M1 diperluas ke 6 misi dalam 4 bab.

Sudah ada:
- Pemutar misi layar penuh dan peta bab (`/puzzle`, `/puzzle/misi/[slug]`).
- Naskah 6 misi di `data/puzzle/en-misi.json`.
- Animasi Aha! berbasis naskah, Latihan 4 format dengan kombo, Bos 3 nyawa, Hadiah, pintu lompat, dan satu soal selipan.
- XP Puzzle hanya untuk jawaban benar, separuh saat diulang, lalu nol, dengan bonus yakin/ragu.

Belum ada di M1:
- Narasi TTS. `cmd/tools/narrate_puzzles` sudah siap, tetapi kredit OpenRouter habis (402). Sementara memakai suara browser dan teks.
- Arti kata saat diketuk, puzzle retak, peti ulangan, Tantangan, dan penulisan bebas tentang diri sendiri di Bos (butuh penilaian AI).
- Bintang dikirim dari browser, jadi belum tahan curang. Bintang tidak memengaruhi penguasaan.

| Tahap | Isi | Bukti yang dicari sebelum lanjut |
|---|---|---|
| **M1. Prototipe satu bab** | Pemutar misi layar penuh, Tebak, 5 animasi Aha!, Latihan dengan kombo, Bos, Hadiah, pada satu bab Basic | 5–10 pemula sungguhan menyelesaikan misi dan bisa menjelaskan isinya tanpa dibantu |
| **M2. Basic–A2** | Peta bab, selipan, puzzle retak, peti ulangan, naskah animasi AI + tinjauan | Tingkat selesai misi dan kembali di hari ke-2 |
| **M3. Yang sudah bisa** | Tantangan, pintu lompat, tes penempatan (bagian dari Tahap B) | Pengguna mahir tidak drop di menit pertama |
| **M4. Kampung Bahasa** | Bab membuka misi di game, jawaban Pare ikut menghitung (Tahap C) | Retensi hari ke-7 dan ke-30 |

Ukuran hasil belajar tetap yang ada di metode-belajar.md. Ukuran keterlibatan seperti streak tidak boleh menggantikannya.

## Keputusan yang perlu pemilik

1. **Urutan aktivitas dulu** untuk semua pelajar, dengan layar Misi sebelum Tebak. *Usul: ya.*
2. **Tab lima langkah diganti alur satu layar.** *Usul: ya*, sedangkan tab Materi tetap bisa dibuka sebagai rujukan setelah misi selesai.
3. **Nyawa hanya di Bos.** *Usul: ya.*
4. **Narasi animasi** memakai TTS dulu, bukan rekaman suara. *Usul: TTS.* Ini memakai kredit AI, jadi perlu izin sebelum dibuat massal.
5. **Bab prototipe** M1. *Usul: satu bab di Basic*, karena di sanalah pemula pertama kali menilai aplikasi ini.
