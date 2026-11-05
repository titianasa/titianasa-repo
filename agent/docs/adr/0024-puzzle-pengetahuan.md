# ADR-0024: Puzzle Pengetahuan di E-learning Titian Asa

Status: Diterima (2026-11-01: keputusan terbuka dipilihkan atas delegasi pemilik; UI/UX mengikuti scratch.mit.edu)
Tanggal: 2026-11-01
Sumber: `Puzzle Pengetahuan Dokumentasi Awal.md` (draf 0.1, 31 Oktober 2026)
Terkait: ADR-0001 (model data kanonik), ADR-0002 (rumus penguasaan), ADR-0003 (FRSS), ADR-0007 (hierarki konsep), ADR-0008 (versi konten), ADR-0012 (rescue mode), ADR-0013 (AI Learning Engine), ADR-0014 (Admin Pusat)

## Ringkasan

Puzzle Pengetahuan masuk ke Titian Asa sebagai **fitur baru, bukan pengganti**. Siswa mendapat menu baru **Puzzle**, satu layar bergaya editor Scratch, yang menampilkan pengetahuannya sebagai jaringan puzzle, menguji puzzle yang belum dimiliki, menelusuri akar masalah saat gagal, dan merangkai jawaban dengan blok. Modul Belajar, Latihan, Jalur, Try Out, Ruang Kelas, Progres, dan Kampung Bahasa Pare tetap berjalan seperti sekarang.

Kuncinya: **hampir semua mesin yang dibutuhkan dokumen awal sudah ada di Titian**, hanya belum disambungkan dan belum diberi tampilan. Fitur ini dibangun sebagai lapisan di atasnya, dengan perubahan basis data yang semuanya aditif.

## Konteks: yang sudah ada dan cocok

| Kebutuhan di dokumen awal | Yang sudah ada di Titian | Status |
|---|---|---|
| Puzzle (unit pengetahuan) | Tabel `concepts`, jembatan antara konten, soal, dan mesin belajar (ADR-0001) | Ada, perlu kolom tambahan |
| Prasyarat (garis graf) | Tabel `concept_prerequisites` (ADR-0001) | Ada, kosong, belum dipakai |
| Hierarki `partOf` | `concepts.parent_concept_id` + penolakan lingkaran di aplikasi (ADR-0007) | Ada |
| Skor 0–100 dengan pemudaran | `masteries` (skor, keyakinan, bobot waktu λ, ADR-0002) | Ada, berjalan |
| Pengulangan berjarak, antrean harian | `frss_schedule` + `GET /review-queue` (ADR-0003) | Ada, berjalan |
| Deteksi gagal berulang | Rescue mode, `GET /concepts/{id}/rescue-status` (ADR-0012) | Ada, belum menelusuri prasyarat |
| Rincian penguasaan bertingkat | `GET /concepts/{id}/mastery-breakdown` | Ada |
| Bank soal dan uji singkat | Bank soal (50+ tipe soal), kuis Modul Belajar dengan `uid` tetap, sesi drill/ujian kanonik (`canon_sessions`) | Ada |
| Materi per puzzle | Modul Belajar dan unit kanonik (456 unit, termasuk 203 unit bahasa Inggris dan 253 unit matematika) | Ada |
| Jejak belajar | `learning_events` (dipartisi per bulan, registry event, ADR-0013) | Ada |
| Usulan AI + tinjauan manusia | Antrian job, agen AI per peran, model diatur di Admin Pusat (ADR-0013/0014) | Ada |
| Tipe soal mirip blok | `sentence_reorder`, `word_scramble`, `sentence_transform`, `gap_fill` | Ada, tanpa aturan sambung |
| Konsep tata bahasa Inggris siap pakai | 164 konsep di konten Kampung Bahasa (`game/src/game/content/en/*-grammar.ts`): pola, penjelasan, contoh, kesalahan umum | Ada, belum di basis data |

Yang **belum ada**: identitas puzzle bernamespace dan jenisnya, atribut garis prasyarat (ambang, sumber, keyakinan), hubungan non-hierarki (`related`), tugas yang membutuhkan beberapa puzzle, mesin blok dengan paket aturan, diagnosis yang menelusuri prasyarat, tampilan graf, dan daftar seluruh penguasaan siswa (halaman Progres sekarang hanya menebak dari antrean ulang).

## Keputusan

### 1. Tempat di aplikasi

```
titian-web (app)
├── Belajar        (tetap)
├── Latihan        (tetap)  ──► tombol baru "Cari akar masalah" saat gagal
├── Jalur          (tetap)  ──► simpul jalur menampilkan puzzle yang dibutuhkan
├── Progres        (tetap)  ──► tab Penguasaan memakai daftar penguasaan baru
└── Puzzle         (BARU, satu layar bergaya editor Scratch, lihat §10)
    ├── /puzzle                    editor: tab Rangkai · Peta · Materi
    ├── /puzzle?tugas=[id]         membuka tugas di panggung
    ├── /puzzle?p=[slug]           membuka satu puzzle (materi + uji)
    ├── /puzzle?diagnosis=[sesi]   diagnosis bertingkat di panggung, jejak di atasnya
    └── /puzzle?ulang=1            antrean ulang harian (memakai /review-queue yang ada)
```

Fitur dinyalakan per organisasi lewat flag (`features.puzzle_pengetahuan`), supaya bisa diuji di satu kelas dulu tanpa terlihat oleh pengguna lain.

### 2. Puzzle = konsep yang diperluas, bukan tabel baru

Setiap puzzle **adalah** satu baris `concepts`. Karena mastery, FRSS, rescue mode, dan statistik semuanya memakai `concept_id`, puzzle otomatis mendapat semuanya tanpa menulis ulang mesin.

Tambahan aditif:

```sql
-- identitas dan jenis puzzle (1:1 dengan concepts)
CREATE TABLE puzzle_meta (
  concept_id    uuid PRIMARY KEY REFERENCES concepts(id),
  slug          text UNIQUE NOT NULL,      -- eng.grammar.passive-voice (permanen, tidak dipakai ulang)
  kind          text NOT NULL CHECK (kind IN ('vocab','concept','symbol','procedure','fact')),
  version       int  NOT NULL DEFAULT 1,
  status        text NOT NULL DEFAULT 'draft',  -- draft | review | published | archived
  content_ref   jsonb NOT NULL DEFAULT '{}',    -- rujukan materi: module_item_id / canon unit / konsep Pare
  builder_pack  text,                           -- rujukan paket aturan blok (bila ada)
  title_i18n    jsonb NOT NULL DEFAULT '{}'     -- {"id": "...", "en": "..."}
);
CREATE TABLE puzzle_aliases (old_slug text PRIMARY KEY, concept_id uuid NOT NULL REFERENCES concepts(id));

-- garis prasyarat: kolom tambahan di tabel yang sudah ada
ALTER TABLE concept_prerequisites
  ADD COLUMN min_score  int    NOT NULL DEFAULT 50,
  ADD COLUMN source     text   NOT NULL DEFAULT 'human',  -- human | ai | data
  ADD COLUMN confidence real   NOT NULL DEFAULT 1,
  ADD COLUMN status     text   NOT NULL DEFAULT 'active'; -- proposed | active | pruned

-- hubungan non-hierarki (ditunda di ADR-0007, sekarang dibutuhkan)
CREATE TABLE concept_relations (
  a uuid NOT NULL REFERENCES concepts(id), b uuid NOT NULL REFERENCES concepts(id),
  kind text NOT NULL,  -- related | same_skill_as | contrasts_with
  PRIMARY KEY (a, b, kind)
);
```

`concepts.type` yang lama (`grammar`, `vocabulary`, `skill`, `pronunciation`) tetap dipakai fitur lama. `puzzle_meta.kind` adalah klasifikasi baru untuk menentukan cara menguji, sesuai kontrak di dokumen awal.

### 3. Penguasaan: memakai mesin yang ada, ditambah satu tampilan

Rumus skor (ADR-0002) dan jadwal ulang (ADR-0003) **tidak diubah**. Yang ditambahkan adalah **kekuatan tampilan** di peta:

```
kekuatan = mastery.score × retensi
retensi  = exp(− hari_sejak_review_terakhir / interval_frss)
```

Dengan begitu titik meredup saat lama tidak dipakai (pemudaran di dokumen awal), dan menyala lagi setelah ulang berhasil. Interval FRSS yang memanjang tiap keberhasilan sudah memberi "waktu paruh makin panjang".

Tiga tingkat penguasaan dibaca dari data yang ada:

| Tingkat | Bukti |
|---|---|
| Dilihat | event membuka materi puzzle (`learning_events`, sudah tercatat untuk Modul Belajar) |
| Bisa recall | kekuatan ≥ 50 dari soal bertipe recall (puzzle "dimiliki") |
| Bisa menerapkan | ada jawaban benar pada soal transfer atau prosedur, dan kekuatan ≥ 90 (puzzle "dikuasai") |

Ambang 50 dan 90 disimpan di konfigurasi (pola yang sama dengan ambang mastery yang ada), karena dokumen awal menyebut keduanya harus dikalibrasi. Penandaan tipe recall/transfer/procedure ditambahkan sebagai label pada soal (`question_concepts.assess_type` dan field yang sama pada kuis Modul Belajar), bukan tabel soal baru.

### 4. Tugas

Tugas adalah soal yang membutuhkan beberapa puzzle sekaligus, misalnya "ubah kalimat ini ke passive voice".

```sql
CREATE TABLE puzzle_tasks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  slug text UNIQUE NOT NULL,
  prompt jsonb NOT NULL,                -- perintah per bahasa
  required jsonb NOT NULL,              -- [{concept_id, min_score}]
  checker jsonb NOT NULL,               -- {type: exact|set|numeric|rules|ai-rubric, ...}
  builder_pack text,                    -- bila dijawab dengan blok
  question_id uuid REFERENCES questions(id)  -- bila memakai soal bank yang sudah ada
);
```

Alur siklus belajar di dokumen awal dijalankan oleh satu endpoint `GET /tasks/{id}/readiness`: daftar puzzle yang dibutuhkan, kekuatannya, dan mana yang terkunci beserta prasyaratnya.

### 5. Mesin blok

Dibangun sebagai **satu tipe soal baru** `block_build` di registry tipe soal yang ada (ADR-0001: soal berupa `jsonb` yang divalidasi registry). Dengan begitu blok bisa muncul di Latihan, Modul Belajar, dan Try Out juga, bukan hanya di menu Puzzle.

- **Paket aturan** (`builder_packs`: id, versi, JSON) berisi jenis blok, tabel boleh menyambung, pesan kesalahan, dan level tantangan. Satu mesin, banyak pelajaran.
- Pemeriksa `rules` jalan di server (Go) dan di peramban (TypeScript) dari JSON yang sama: peramban memberi umpan balik langsung saat merangkai, server yang menilai.
- Normalisasi jawaban (huruf besar, tanda baca, spasi) ditulis sekali di kontrak dan dipakai semua pemeriksa.
- Komponen web memakai Blockly dengan renderer bergaya Scratch (§10), termasuk ketuk-untuk-menambah di HP.
- Pelajaran pertama: bahasa Inggris (passive voice, tense, urutan kata). Matematika dan kimia menyusul setelah pola paket aturan teruji.

### 6. Diagnosis bertingkat = rescue mode yang diperdalam

Rescue mode yang ada (ADR-0012) hanya mendeteksi 3 jawaban salah berturut dan menawarkan materi. Diagnosis meneruskannya ke bawah graf:

1. Siswa gagal pada tugas atau puzzle X (atau rescue mode terpicu).
2. Server membuat sesi diagnosis (`canon_sessions` dengan `kind = 'diagnosis'`, memakai mekanisme sesi drill yang sudah ada).
3. Prasyarat aktif X diuji 1–2 soal per puzzle, diambil dari bank. **Prasyarat yang kekuatannya segar dan keyakinannya cukup dilewati**, karena buktinya sudah ada.
4. Prasyarat yang gagal dibuka (soal yang salah, jawaban siswa, jawaban benar, penjelasan), lalu prasyaratnya sendiri diuji. Berulang sampai menemukan puzzle terdalam yang gagal dengan semua prasyarat lulus: itulah akar masalah.
5. Siswa belajar dari akar, lalu naik kembali tingkat demi tingkat ke tugas awal.

Batas: kedalaman maksimal 4, soal maksimal 2 per puzzle dan 12 per sesi (konfigurasi). Layar hanya menampilkan puzzle yang sedang diuji, dengan jejak ringkas di atasnya. Setiap jawaban menulis `learning_events` biasa, jadi mastery, FRSS, dan statistik butir ikut terbarui tanpa jalur khusus. Hasilnya disimpan sebagai laporan "di mana pemahaman putus" yang bisa dilihat siswa dan guru.

Tombol **"Cari akar masalah"** juga ditambahkan di layar hasil Latihan yang sudah ada, sehingga diagnosis bisa dipakai tanpa siswa masuk ke menu Puzzle dulu.

### 7. Pembangunan graf: lewat agen AI dan Admin Pusat yang ada

Graf tidak dibuat manual. Pipeline di dokumen awal dijalankan oleh infrastruktur ADR-0013:

| Langkah | Diwujudkan dengan |
|---|---|
| Sumber | unit kanonik, Modul Belajar, bank soal, konsep tata bahasa Kampung Bahasa |
| Usulan AI | peran AI baru `graph_builder` (model dipilih di Admin Pusat, ADR-0014), lewat antrian job |
| Validator | kode Go deterministik: tolak lingkaran (pola ADR-0007), gabungkan duplikat slug, batasi kedalaman, tandai puzzle yatim, buang garis transitif dari tampilan |
| Tinjauan | halaman baru di Studio/Admin: hanya usulan dengan keyakinan rendah yang perlu ditinjau guru |
| Kalibrasi | job terjadwal membaca `learning_events`: jika siswa yang gagal di X sering lemah di Y, garis Y→X diperkuat; garis yang tidak membantu memprediksi turun keyakinannya lalu `pruned` |

Usulan AI selalu masuk dengan `status = 'proposed'`. Siswa hanya melihat garis `active` dengan keyakinan di atas ambang.

### 8. API baru (semua di modul Go baru `internal/puzzle`)

| Endpoint | Fungsi |
|---|---|
| `GET /puzzles/graph?root=&depth=&view=frontier` | potongan graf: titik, garis, kekuatan siswa; hierarki `partOf` untuk zoom |
| `GET /puzzles/{slug}` | puzzle: materi (rujukan), prasyarat, kekuatan, tingkat, riwayat |
| `POST /puzzles/{slug}/test` | mulai uji puzzle (sesi drill dengan soal recall/transfer sesuai `kind`) |
| `GET /me/knowledge` | daftar seluruh penguasaan siswa (sekaligus menutup celah di halaman Progres) |
| `GET /tasks/{id}/readiness` | puzzle yang dibutuhkan tugas, mana yang terkunci |
| `POST /tasks/{id}/answer` | kirim jawaban (termasuk susunan blok) |
| `POST /diagnosis` · `GET /diagnosis/{id}` · `POST /diagnosis/{id}/answer` | diagnosis bertingkat |
| Admin: `GET/POST /admin/puzzles/proposals` | tinjau usulan graf |

### 9. Tampilan peta (tab Peta di editor, §10)

- Pustaka graf di web: React Flow (xyflow); titik digambar sebagai keping puzzle berwarna kategori. Graf besar tidak pernah digambar sekaligus. Bawaannya **batas terdepan**: puzzle lemah yang paling dekat dengan tujuan siswa, ditambah satu tingkat prasyarat.
- Zoom bertingkat mengikuti `parent_concept_id`: mata pelajaran → topik → puzzle.
- Terang titik = kekuatan; gembok = belum dimiliki; cincin emas = dikuasai.
- Filter "kelemahanku" memakai data penguasaan, dan pencarian memakai slug serta judul.

### 10. UI/UX bergaya Scratch

Pemilik meminta tampilan seperti editor scratch.mit.edu. Seluruh fitur Puzzle berada di satu layar editor, dengan susunan dan bahasa visual Scratch 3, tetapi warna utama dan logo tetap Titian.

#### Susunan layar (laptop dan tablet)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Titian · Puzzle   [Bahasa Inggris ▾]   📂 Tugas   🔁 Ulang (6)   👤            │  bilah atas
├───────┬──────────────────┬──────────────────────────────┬────────────────────┤
│ ●Tata │ [Rangkai] [Peta] [Materi]                        │  ▶ Periksa  ■ Ulang │
│  bahasa│                  │                              │ ┌────────────────┐ │
│ ●Kosa │  PALET           │  AREA SUSUN                  │ │ PANGGUNG       │ │
│  kata │  ┌───────────┐   │   ╭──────────────────────╮   │ │ Tugas:         │ │
│ ●Tense│  │ the fish  │   │   │ ketika tugas dimulai │   │ │ "The cat ate   │ │
│ ●Kali-│  └───────────┘   │   ╰─┬────────────────────╯   │ │  the fish."    │ │
│  mat  │  ┌───────────┐   │   ┌─┴───────────┐            │ │ → passive      │ │
│ ●Sim- │  │ be (was) ▾│   │   │ the fish    │            │ │                │ │
│  bol  │  └───────────┘   │   ├─────────────┤            │ │ Hasil: ...     │ │
│ ●Pro- │  ┌───────────┐   │   │ was         │            │ └────────────────┘ │
│  ses  │  │🔒 V3      │   │   ├─────────────┤            │ ┌────────────────┐ │
│       │  └───────────┘   │   │ eaten       │            │ │ KOLEKSI        │ │
│       │   ketuk: uji     │   ├─────────────┤            │ │ 🧩 12/40        │ │
│       │   untuk membuka  │   │ by the cat  │            │ │ ✨ 3 dikuasai   │ │
│       │                  │   └─────────────┘  ⊕ ⊖ ⟲     │ └────────────────┘ │
└───────┴──────────────────┴──────────────────────────────┴────────────────────┘
 kolom    palet blok          area susun (seret, sambung)    panggung + koleksi
 kategori
```

| Bagian Scratch | Di Puzzle Titian |
|---|---|
| Kolom kategori (lingkaran berwarna: Motion, Looks, …) | Area pelajaran: Tata bahasa, Kosakata, Tense, Kalimat, Simbol, Prosedur. Satu warna tetap per area |
| Palet blok | Puzzle milik siswa sebagai blok yang bisa diseret. Puzzle yang belum dimiliki tampil abu-abu bergembok; diketuk membuka uji di panggung |
| Area susun dengan zoom ⊕ ⊖ ⟲ | Tempat merangkai jawaban tugas. Blok menempel lewat lekukan seperti Scratch, dan hanya bisa menempel kalau paket aturan mengizinkan. Blok yang salah posisi bergetar dan menampilkan pesan dari paket aturan |
| Panggung dengan bendera hijau dan tombol stop | Panggung tugas: perintah, hasil rangkaian dibaca sebagai kalimat utuh, **▶ Periksa** (bendera hijau) dan **■ Ulang**. Uji puzzle dan diagnosis juga tampil di sini |
| Panel sprite | Koleksi: jumlah puzzle dimiliki dan dikuasai, kartu puzzle yang baru menyala |
| Tab Code / Costumes / Sounds | Tab **Rangkai** (area susun) · **Peta** (graf pengetahuan) · **Materi** (penjelasan puzzle yang dipilih) |
| Menu File dan tutorial | 📂 Tugas (daftar tugas per level) dan 🔁 Ulang (antrean ulang harian) |

#### Bentuk blok mengikuti jenis puzzle

Seperti Scratch membedakan blok perintah, reporter, dan boolean dari bentuknya:

| `kind` | Bentuk blok | Contoh |
|---|---|---|
| vocab | reporter bulat (oval), mengisi lubang di blok lain | `eaten`, `the fish` |
| symbol | heksagon (seperti boolean) | `→`, `=`, `+`, `Fe²⁺` |
| concept | blok tumpuk (bertakik atas-bawah) dengan lubang isian | `[subjek] was/were [V3]` |
| procedure | blok-C yang membungkus langkah | `ubah ke passive { … }` |
| fact | blok topi (hat), pembuka rangkaian | `ketika tugas dimulai` |

#### Tab Peta

Graf tampil di atas latar bertitik seperti area susun Scratch, titiknya berupa keping puzzle berwarna kategori. Terang = kekuatan, gembok = belum dimiliki, kilau emas = dikuasai. Mengetuk titik membuka tab Materi untuk puzzle itu dan memunculkan tombol "Uji" di panggung. Zoom memakai tombol ⊕ ⊖ ⟲ yang sama dengan area susun.

#### Diagnosis di panggung

Panggung menampilkan satu puzzle yang sedang diuji. Di atasnya ada jejak berupa blok tumpuk kecil (`Tugas › Passive voice › Verb 3`). Tingkat yang lulus melipat menjadi blok kecil hijau, seperti blok Scratch yang diciutkan.

#### Di HP

Editor Scratch tidak dibuat untuk HP, jadi susunannya disesuaikan:
- Panggung di atas (sepertiga layar), area susun di tengah, palet sebagai laci geser di bawah dengan kategori sebagai tab bulat berwarna.
- **Ketuk untuk menambah** selain seret: mengetuk blok di palet menempelkannya ke posisi sah berikutnya, karena seret-dan-lepas di layar kecil melelahkan.
- Tab Rangkai, Peta, dan Materi pindah ke bilah bawah.

#### Teknologi

- **Blockly** dari Google (lisensi Apache 2.0) dengan renderer **zelos**, renderer yang meniru tampilan blok Scratch 3. `scratch-blocks` sendiri turunan Blockly. Blockly sudah menangani seret, sambung, zoom, sentuh, dan navigasi papan ketik.
- **Paket aturan → definisi blok Blockly.** "Tabel boleh menyambung" di paket aturan menjadi pemeriksaan tipe sambungan Blockly (`setCheck`), jadi blok yang tidak cocok memang tidak bisa menempel, bukan hanya ditolak saat diperiksa. Pemeriksa server (Go) membaca JSON paket yang sama.
- Blockly hanya dimuat di halaman Puzzle (dynamic import), supaya halaman lain tidak bertambah berat.
- Tab Peta memakai React Flow seperti di §9.
- Gaya: font Nunito, sudut bulat, bayangan lembut, warna kategori jenuh seperti Scratch; kuning Titian untuk tombol utama dan sorotan.

## Tahapan pengerjaan

Setiap tahap bisa dipakai sendiri dan tidak mengganggu fitur lama.

| Tahap | Isi | Hasil yang bisa dicoba |
|---|---|---|
| **0. Kontrak** | ADR ini disetujui, migrasi aditif, flag fitur, registry `kind` dan `assess_type` | Tidak ada perubahan yang terlihat |
| **1. Data dan API inti** | `puzzle_meta`, kolom prasyarat, `concept_relations`, validator, `GET /puzzles/graph`, `GET /me/knowledge`, kekuatan tampilan | Tab Penguasaan di Progres menampilkan seluruh konsep, bukan hanya yang jatuh tempo |
| **2. Satu pelajaran: tata bahasa Inggris** | Impor 164 konsep tata bahasa Kampung Bahasa sebagai puzzle (sudah ada pola, contoh, kesalahan umum), dikaitkan ke 203 unit kanonik bahasa Inggris; prasyarat diusulkan AI lalu ditinjau; label recall/transfer pada soal yang ada | Peta tata bahasa Inggris Basic–C2 |
| **3. Editor Puzzle dan uji** | layar editor bergaya Scratch (§10) dengan tab Peta dan Materi, palet blok, panggung untuk uji puzzle, antrean ulang | Siswa melihat, menguji, dan menyalakan puzzle |
| **4. Tugas, blok, diagnosis** | `puzzle_tasks`, area susun Blockly + tipe soal `block_build` + paket aturan bahasa Inggris, diagnosis bertingkat di panggung, tombol di Latihan | Contoh utuh di dokumen awal: tugas passive voice dari awal sampai akar masalah |
| **5. Graf otomatis dan kalibrasi** | peran `graph_builder`, halaman tinjauan, job kalibrasi | Graf tumbuh dari materi baru; garis lemah terpangkas |
| **6. Guru dan lintas pelajaran** | dasbor kelas (peta gabungan, puzzle paling sering gagal) di Ruang Kelas, penugasan berbasis puzzle, matematika (253 unit kanonik) | Guru memakai peta untuk kelasnya |

### Status pengerjaan (2026-11-01)

Metode mengajarnya (siklus Lihat → Coba → Buktikan → Pakai → Ingat, lapisan usia, lintas pelajaran, cara membuktikan efek) dirancang di [puzzle-pengetahuan/metode-belajar.md](../puzzle-pengetahuan/metode-belajar.md).

Tahap 0–3 selesai di dev, sebagian tahap 4 juga (tugas rangkai kalimat). Belum di-deploy ke produksi.

- **Backend** (`titian-backend-go`):
  - Migrasi `0108_puzzle_pengetahuan.sql`.
  - Paket `internal/puzzle`: validator graf, kekuatan dan status, API, beserta tes.
  - Alat `cmd/tools/import_puzzles` ditambah data di `data/puzzle/`.
  - Flag: env `PUZZLE_PENGETAHUAN` (bawaan `false`) atau `organizations.settings.features.puzzle_pengetahuan`.
- **Konten**:
  - 164 puzzle tata bahasa Inggris Basic–C2.
  - 316 soal isian (recall) untuk uji puzzle.
  - 328 tugas rangkai kalimat (transfer).
  - 227 prasyarat yang disusun tangan (`source=import`, confidence 0.8), lolos validator tanpa peringatan.
  - Ekspor dari game: `game/scripts/export-puzzles.ts`.
- **Web** (`titian-web`):
  - Rute layar penuh `/puzzle`, berisi editor Blockly zelos, tab Peta (React Flow), dan tab Materi.
  - Panggung dengan ▶ Periksa / ■ Ulang, uji puzzle, Koleksi, dan susunan khusus HP.
  - Menu "Puzzle" di sidebar, hanya tampil jika flag aktif.
  - Tab Penguasaan di Progres kini memakai `/me/knowledge`.

Penyesuaian terhadap rancangan di atas:
- **Isi puzzle**:
  - Kolomnya `puzzle_meta.content`, bukan `content_ref`. Isinya disimpan langsung, bukan rujukan.
  - Ditambah kolom `area` (kolom kategori editor: kata · tense · kalimat · modal · wacana), `level`, dan `position`.
- **Tugas memakai soal biasa**:
  - Setiap tugas rangkai juga disimpan sebagai soal `sentence_reorder` (`puzzle_tasks.question_id`, `assess_type=transfer`). Jawabannya lewat `POST /questions/{id}/check`, jadi mastery, FRSS, dan rescue ikut bergerak tanpa jalur baru.
  - Tipe `block_build` dengan pemeriksa aturan baru dibutuhkan untuk tugas yang lebih bebas dari susun kata.
- **Rumus kekuatan**: `skor × 0,9^(hari sejak review ÷ interval FRSS)`, bukan `exp(−hari/interval)`. Dengan rumus ini puzzle yang jatuh tempo baru turun 10%; rumus lama sudah memangkasnya ke 37%.
- **Status**:
  - "Dimiliki" berarti kekuatan ≥ 50.
  - "Dikuasai" (puzzle selesai) berarti kekuatan ≥ 50, semua kalimat Pakai pernah benar, dan ada jawaban ingatan benar di hari lain (tanggal WIB) setelah yang pertama. Konsep tanpa tugas memakai skor ≥ 90 plus syarat hari lain itu.
  - Revisi 2026-11-01 setelah tinjauan pemilik. Aturan lama (skor ≥ 90 plus satu soal transfer) membuat siswa tidak tahu kapan sebuah puzzle tamat, dan tamat di hari yang sama tidak membuktikan ingatan.
- **Alur belajar (revisi 2026-11-01, detail di metode-belajar.md)**:
  - Setiap puzzle punya 5 langkah tetap: Lihat, Coba, Buktikan, Pakai, Ingat.
  - Soal latihan Coba berlabel `assess_type = 'practice'`: tercatat sebagai jawaban, tetapi tidak menggerakkan mastery, FRSS, maupun Rescue Mode.
  - `POST /questions/{id}/check` menerima `confidence` ("yakin"/"ragu"), disimpan di payload event.
  - `POST /puzzles/review` menarik ulangan harian campuran, satu soal per puzzle. `/me/knowledge` menyertakan `review`.
  - Migrasi `0109_puzzle_siklus_belajar.sql` menambah `practice` dan `puzzle_tasks.stage`.
  - Tombol kuning "Lanjut" selalu menunjuk langkah berikutnya.
  - Level Basic–C2 tampil sebagai jalur dengan progres masing-masing. Level tamat kalau semua puzzle di dalamnya dikuasai.
  - Panduan "Cara belajar" muncul di kunjungan pertama dan bisa dibuka lagi lewat tombol "?".
  - Kolom kategori dan menu Tugas versi pertama dihapus, karena tugas melekat pada puzzle.
  - Level Basic (tanpa soal isian di game) diberi 3 soal uji per puzzle, dibuat dari contoh dan kesalahan umum.
  - `/me/knowledge` menyertakan `levels`. Tugas menyertakan `solved`.
- **Diagnosis (sisa tahap 4)**: akan memakai tabel sesi sendiri, bukan `canon_sessions`, karena `canon_sessions.bab_id` wajib merujuk ke sebuah bab.
- **API**:
  - `POST /tasks/{id}/answer` dan `GET /tasks/{id}/readiness` digantikan oleh `GET /puzzles/tasks?level=&puzzle=`, yang menyertakan kesiapan tiap tugas, ditambah jalur pemeriksaan soal yang sudah ada.
  - Ditambah `GET /puzzles/access`.
- **Misi (revisi 2026-11-01, detail di desain-misi.md)**:
  - Migrasi `0110_puzzle_misi.sql` menambah kolom bab di `puzzle_meta` dan tabel `puzzle_missions`.
  - `GET /puzzles/path` dan `POST /puzzles/{slug}/mission` melayani peta bab dan bintang.
  - `POST /questions/{id}/check` mengembalikan `xp_awarded`. Soal Puzzle hanya memberi XP untuk jawaban benar.
  - `gap_fill` menerima `correct_answer.accept` untuk bentuk lain yang sama benarnya.
  - Kalimat Pakai level Basic ditulis ulang di naskah misi, karena urutan aslinya tidak sejajar dengan konsepnya. A1–C2 sudah diperiksa dan sejajar.
- **Jaringan kepingan (revisi 2026-11-01)**: migrasi `0111_puzzle_kepingan.sql` menambah `assess_type = 'piece'` dan relasi `used_in`. Kata menjadi `puzzle_meta.kind = 'vocab'`, kemampuan `kind = 'fact'`; keduanya tidak dihitung sebagai puzzle (angka 164 tetap konsep). `GET /puzzles/network` mengembalikan kepingan dan sambungannya.
- **Pelajaran dari kurikulum game (revisi 2026-11-01)**: migrasi `0112_puzzle_pelajaran.sql` menambah `puzzle_lessons` dan `puzzle_lesson_runs`. `GET /puzzles/lessons/{slug}` dan `POST /puzzles/lessons/{slug}/complete` melayani pelajaran kata, praktik, dan ujian; `GET /puzzles/path` menyusun bab dalam urutan `before`, `missions`, `after`, ditambah `exam`.
- **Belum dikerjakan**:
  - Pemetaan puzzle ke 203 unit kanonik.
  - Jawaban tata bahasa di Kampung Bahasa yang ikut menghitung (keputusan 5).
  - Diagnosis bertingkat dan tombol "Cari akar masalah" di Latihan.
  - Tahap 5–6.

## Ukuran keberhasilan

Mengikuti dokumen awal, dibaca dari `learning_events`:
- Tingkat berhasil mengerjakan tugas setelah melengkapi prasyarat, dibanding yang melewatinya.
- Retensi puzzle pada hari ke-7 dan ke-30.
- Jumlah langkah diagnosis sampai akar masalah ditemukan.
- Seberapa sering siswa kembali membuka menu Puzzle per minggu.

## Keputusan terbuka (dipilihkan 2026-11-01)

Pemilik meminta dipilihkan yang terbaik. Pilihannya:

1. **Nama menu: "Puzzle".** Pendek, sesuai metafora keping yang disambung, dan tidak bentrok dengan "Jalur" maupun peta Kampung Bahasa. "Peta" menjadi salah satu tab di dalamnya.
2. **Prasyarat tidak mengunci mati.** Tugas boleh dibuka walau puzzle-nya belum lengkap, dengan peringatan "Kamu belum punya 2 puzzle untuk ini" dan tombol "Kumpulkan dulu". Alasannya: kunci mati membuat siswa frustrasi, dan ukuran keberhasilan pertama di dokumen awal justru membutuhkan perbandingan siswa yang melengkapi dengan yang melewati.
3. **Satu skor puzzle untuk semua tempat.** Latihan, Jalur, Try Out, Modul Belajar, Puzzle, dan Kampung Bahasa menulis ke penguasaan konsep yang sama. Ini sudah cara kerja mesin mastery sekarang, dan mencegah siswa terlihat "pintar" di satu menu tapi "nol" di menu lain.
4. **Konten oleh platform dulu, guru di tahap 6.** Graf yang dibuat banyak pihak sejak awal sulit dijaga bebas lingkaran dan duplikat. Guru sudah bisa meninjau usulan AI sejak tahap 5. Puzzle dan paket aturan buatan guru dibuka di tahap 6, terbatas untuk kelasnya dan ditinjau sebelum masuk bank bersama.
5. **Kampung Bahasa ikut menghitung, mulai tahap 2.** 164 konsep tata bahasa game diimpor dengan slug yang sama, jadi soal tata bahasa yang dijawab di Pare (latihan, misi bersama warga) ikut memperbarui puzzle bahasa Inggris. Pare punya jauh lebih banyak jawaban siswa daripada e-learning, jadi kalibrasi graf mendapat data lebih cepat. Ngobrol bebas dengan warga dan pemain komputer tidak dihitung, karena tidak dinilai.

## Alternatif yang dipertimbangkan

- **Aplikasi terpisah (Next.js + Supabase seperti di dokumen awal)**: ditolak. Titian sudah punya mesin penguasaan, pengulangan berjarak, bank soal, dan pipeline AI; membangun ulang di stack lain menggandakan data siswa dan kehilangan semua riwayat belajar yang ada.
- **Tabel `puzzles` sendiri yang terpisah dari `concepts`**: ditolak, karena mastery, FRSS, rescue mode, dan statistik harus ditulis ulang atau disinkronkan dua arah.
- **Mengganti rumus mastery dengan model pemudaran baru**: ditolak untuk sekarang. Kekuatan tampilan (skor × retensi FRSS) memberi efek yang sama tanpa mengubah angka yang sudah dipakai fitur lain. Model seperti BKT atau FSRS tetap kandidat setelah data cukup (catatan di ADR-0002 dan ADR-0003).

## Konsekuensi

- (+) Fitur lama tidak berubah; semua perubahan basis data aditif dan bisa dimatikan dengan flag.
- (+) Puzzle langsung mendapat mastery, FRSS, rescue, statistik butir, dan pipeline AI yang sudah ada.
- (+) Mesin blok menjadi tipe soal biasa, jadi bisa dipakai di luar menu Puzzle juga.
- (−) `concept_prerequisites` dan `concepts` yang sekarang hampir kosong harus diisi. Tahap 2 (tata bahasa Inggris dari Kampung Bahasa) dipilih karena bahannya paling siap.
- (−) Kualitas graf bergantung pada tinjauan guru dan data siswa. Tanpa keduanya, prasyarat usulan AI bisa masuk akal tetapi salah, sesuai risiko yang sudah dicatat di dokumen awal.
