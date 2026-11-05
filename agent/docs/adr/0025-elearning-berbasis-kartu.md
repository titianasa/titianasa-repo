# ADR-0025: E-learning berbasis kartu

Status: Diterima (2026-11-02, keputusan pemilik)

## Ringkasan

Semua materi Titian Asa berbentuk kumpulan kartu, bukan halaman materi panjang. Satu kumpulan kartu dipakai untuk dua hal sekaligus: belajar interaktif di website, dan konten media sosial.

## Konteks

Orang sekarang sulit belajar dari materi panjang. Kartu penjelasan Puzzle (ADR-0024) terbukti bisa dipakai untuk belajar dan bisa langsung diunggah sebagai konten. Pemilik memutuskan pola ini menjadi bentuk utama seluruh e-learning.

## Keputusan

1. **Satuan materi adalah kumpulan kartu (deck).** Materi dipecah sedetail mungkin. Contoh: Part of Speech → Noun → deck *Common and Proper Nouns*.
2. **Isi tetap lengkap.** Pendek per kartu, bukan dangkal. Satu kumpulan harus mencakup materinya secara utuh sesuai standar pembelajaran bahasa Inggris pada umumnya (jenjang CEFR, istilah akademik Inggris).
3. **Satu sumber, dua keluaran.**
   - Di website: soal dikerjakan langsung di dalam kartu, bukan di layar terpisah, dan animasinya merespons jawaban. Audio bisa diputar kalau tersedia.
   - Saat dirender (MP4, PNG, dalam 4:5 dan 9:16): hanya visualnya. Soal tampil lebih dulu, lalu jawabannya.
4. **Teks** natural seperti guru les berbicara. Istilah tata bahasa tetap bahasa Inggris. Aturan teksnya ada di `puzzle-pengetahuan/desain-misi.md`.
5. **Label part of speech di jaringan pengetahuan mengarah ke kartu materinya.** Mengetuk *Concrete noun* membuka deck yang membahasnya.

## Model soal di dalam kartu

| Model | Di website | Saat dirender |
|---|---|---|
| Pilihan ganda (A–E) | Ketuk jawaban | Jawaban benar menyala |
| Isian | Ketik di bagian yang kosong | Jawaban mengisi yang kosong |
| Susun kalimat | Ketuk kata, kata terbang ke tempatnya | Kata acak, lalu kalimat utuh |
| Pasangkan | Ketuk dua sisi, pasangan terkunci satu warna | Sisi kanan muncul berpasangan |
| Kelompokkan | Ketuk kelompok, kata terbang masuk | Kata acak, lalu dua kelompok |
| Ketuk kata | Ketuk kata yang diminta, misalnya semua noun | Kata yang dicari menyala |
| Menyimak | Putar audio, ketik yang didengar | Arti, lalu kalimat Inggrisnya |
| Perbaiki kalimat | Sunting kalimat yang salah | Kalimat salah, lalu yang benar |
| Ketuk garis bilangan | Ketuk titiknya, token melompat ke sana | Token muncul di jawaban |

Kartu menyimak teks panjang (`audio`) memutar dialog atau pengumuman kalimat demi kalimat. Di website teksnya tersembunyi sampai pelajar memintanya. Saat dirender, teksnya langsung tampil.

Percobaan pertama yang dihitung. Salah sekali boleh coba lagi, salah dua kali jawabannya ditampilkan bersama alasannya. Jawaban benar disusul audio kalimat utuhnya. Warna kartu punya arti: krem mengajar, kuning bertanya, biru tua menutup.

## Susunan materi inti: Part of Speech

Sembilan kelas kata (daftar yang umum dipakai kamus pembelajar) plus tenses:

| Kumpulan | Isi deck |
|---|---|
| **Noun** | Pengertian; Common & Proper; Concrete & Abstract; Countable & Uncountable; Plural beraturan; Plural tak beraturan; Collective; Compound; Possessive; Fungsi noun dalam kalimat |
| **Pronoun** | Subject; Object; Possessive; Reflexive; Demonstrative; Indefinite; Relative; Interrogative |
| **Verb** | Pengertian; Action & State; Linking; Auxiliary; Modal; Regular & Irregular (V1, V2, V3); Transitive & Intransitive; Phrasal verb; Gerund & Infinitive |
| **Tenses** | Present, Past, Future masing-masing Simple, Continuous, Perfect, Perfect Continuous; Future in the Past; perbandingan antar-tense |
| **Adjective** | Pengertian; Urutan; Comparative; Superlative; -ed & -ing |
| **Adverb** | Manner; Time; Place; Frequency; Degree; posisi dalam kalimat |
| **Determiner** | Article; Demonstrative; Possessive; Quantifier; Number |
| **Preposition** | Time; Place; Movement; Dependent preposition |
| **Conjunction** | Coordinating; Subordinating; Correlative |
| **Interjection** | Ungkapan dan pemakaiannya |

## Tahapan

1. Kumpulan **Noun** sebagai contoh lengkap, beserta pemutar kartu dan tautan dari jaringan pengetahuan. **Selesai di dev (2026-11-02):** 10 deck, 148 kartu, 68 soal di 8 model.
   Kumpulan **Bilangan Bulat** Matematika sebagai pilot mapel kedua (2026-11-02): 10 deck, 133 kartu, 68 soal, ditambah model ketuk garis bilangan dan contoh langkah demi langkah. Jalurnya di `puzzle-pengetahuan/jalur-belajar-matematika.md`.
2. Pemilik meninjau bentuk dan kedalaman isinya.
3. Kumpulan lain mengikuti pola yang sudah disetujui, dimulai dari Verb dan Tenses.
4. Misi, pelajaran kata, dan praktik berangsur memakai kartu yang sama.

## Implementasi

- Isi: `titian-web/src/content/kartu/` (`types.ts`, `noun.ts`, `bilangan-bulat.ts`, `index.ts`). Kalimat contoh diambil dari rekaman game bila ada: 82 dari 93 kalimat, termasuk semua soal menyimak.
- Tampilan: `src/components/puzzle/kartu/` (`deck-card.tsx`, `exercises.tsx`, `deck-player.tsx`, `card-library.tsx`) dan `mission/card-viewer.tsx`, yang dipakai bersama kartu misi.
- Rute: `/puzzle/kartu` (daftar), `/puzzle/kartu/[slug]` (belajar), `/puzzle-kartu/[slug]?kartu=n&rasio=9x16` (halaman publik yang direkam; tambah `&web` untuk versi interaktif).
- Render: `outputs/konten-sosmed-puzzle/src/render.ts [slug...]`. Tombol Bagikan hanya muncul untuk set yang sudah dirender.
- Belum: skor kartu masih di browser (`localStorage`), belum di akun, dan belum masuk ke jaringan pengetahuan.

## Konsekuensi

- Halaman lima tab (ADR-0024) akan hilang begitu semua level punya misi dan kartu.
- Setiap kartu baru perlu dirender di dua dimensi, jadi proses render harus tetap otomatis.
- Audio hanya tersedia kalau kalimatnya ada di rekaman game. Kalimat baru memakai suara browser sampai narasi TTS bisa dibuat.

## Tambahan 2026-11-03: kartu lab dan rasio 9:16

- **Kartu deck tersedia 9:16 dan 16:9** (keputusan pemilik, 2026-11-03, menggantikan kunci 9:16 di hari yang sama). 9:16 untuk ponsel dan video, 16:9 untuk layar kelas. Pengguna memilih lewat tombol Tegak/Mendatar di pemutar deck. Di 16:9, bingkai ukur tetap seukuran kartu tegak, sehingga semua ukuran cqw sebanding dengan tinggi kartu. Gambar atau lab (`.pz-visual`) mengisi kolom kiri, sisanya di kolom kanan. Kartu tanpa gambar tetap satu kolom di tengah. Halaman ekspor menerima `rasio=16x9`. Narasi suara ditunda atas keputusan pemilik.
- ~~Semua kartu deck dikunci 9:16.~~ Keluaran utamanya video, dan kartu interaktif butuh ruang. Pilihan 4:5 dihapus dari pemutar deck dan halaman ekspor `/puzzle-kartu/[slug]` (kartu misi Puzzle tidak berubah).
- **Kartu ajar baru `lab`:** model yang dicoba sendiri. Deck hanya menyimpan nama model dan nilai awal (`LabSpec` di `content/kartu/types.ts`). Semua bentuk dan angka dihitung kode dari rumus, sehingga gambar dan hitungan tidak mungkin saling bertentangan. Di web: slider, ketuk, dan suara. Di video (`film`): nilai berganti sendiri dalam putaran.
- Model pertama (`components/puzzle/kartu/lab.tsx`): `pythagoras` (persegi berkisi di ketiga sisi), `gelombang` (lingkaran satuan terhubung ke y = A sin Bx + C), `preposisi` (bola di sekitar kotak dan meja, kalimat Inggris dan artinya).
- Aturan: setiap model baru harus diuji dengan menggerakkan kontrolnya dan membaca angka yang tampil, bukan hanya dilihat.
- **Kartu ingat** (`t: "ingat"`): memanggil kartu ajar dari deck prasyarat berdasarkan judulnya. Di web, kartunya dibuka utuh di lapisan atas deck. Pemeriksa: `check-ingat.ts` di folder QA.
