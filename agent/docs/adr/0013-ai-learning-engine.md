# ADR-0013: AI Learning Engine — Jejak Belajar & Pengelolaan Konten Semi-Otonom

Status: Accepted
Date: 2026-09-13 (diusulkan & disetujui user pada tanggal yang sama)
Supersedes: -
Superseded by: -
Related: ADR-0002 (mastery), ADR-0003 (FRSS), ADR-0004 (AI gateway), ADR-0007 (concept hierarchy), ADR-0008 (content versioning), ADR-0012 (rescue mode), ADR-0014 (Admin Pusat)

## Context

Titian sudah punya kurikulum induk yang besar (perpustakaan kanonik: 48 mapel, 4.949 topik, dipakai semua jalur belajar lewat reference row), pipeline AI yang membuat Modul Belajar dan latihan per bab, 40 tipe soal, dan taksonomi soal (tingkat kesukaran + Bloom C1–C6, dengan kesukaran didefinisikan lewat indeks p). Titian juga sudah punya mesin pemahaman siswa yang dirancang matang: penguasaan per konsep (ADR-0002), pengulangan berjadwal (ADR-0003), hierarki konsep (ADR-0007), dan rescue mode (ADR-0012).

Arah produk yang diputuskan (2026-09-13): **kurikulum berbasis AI**. AI mengumpulkan data dari seluruh perilaku belajar (belajar mandiri, kelas live, tryout, kebiasaan peserta kelas, aktivitas guru), lalu memakainya untuk **mengelola konten modul dan latihan secara semi-otonom**, dengan setiap tindakan dilaporkan dulu ke Admin Pusat.

Pemeriksaan kode dan data (2026-09-13) menunjukkan fondasinya ada, tetapi **tidak tersambung**:

1. **Dua model konten yang terpisah.** Mastery/FRSS/rescue hanya membaca bank soal lama (`questions` + `question_concepts`). Semua konten baru ada di `module_items.quiz_config`, dan `quiz_attempt.rs` menyatakan terang-terangan: *"no mastery/FRSS integration here"*.
2. **Soal tidak punya identitas tetap.** `QuizQuestion` hanya punya `number`, yang berubah saat soal dihapus dan penomoran disusun ulang. Statistik per soal akan menempel ke soal yang salah.
3. **Hampir tidak ada yang tercatat.** `learning_events` hanya berisi `question_answered` dari bank soal lama (16 baris). Mengerjakan kuis, membaca modul, dan tryout tidak menulis event apa pun.
4. **Sinyal terkaya dibuang.** Live AI Chat sengaja stateless: pertanyaan siswa ke tutor AI, per bagian modul, tidak disimpan. Kelas live (Google Meet) hanya menyimpan kehadiran.
5. **Konten `module_items` tidak berversi.** ADR-0008 hanya mengatur `questions`/`lessons`, dan MVP-nya sekadar menolak edit pada item yang sudah terbit. AI tidak bisa "membuat v1.1 dan membandingkannya dengan v1.0" tanpa versi.
6. **Belum ada data siswa** (5 attempt). Mekanisme yang butuh volume (A/B, statistik butir, IRT) harus dirancang sekarang, tetapi baru bisa dinyalakan setelah data terkumpul.

Keputusan "bangun ulang dari nol" dipertimbangkan dan ditolak (lihat *Alternatives considered*). Yang dibangun baru adalah **lapisan di atas fondasi yang ada**.

## Decision

Engine disusun dalam lima lapisan. Setiap lapisan hanya bergantung pada lapisan di bawahnya.

```
L4  PERBAIKAN    usulan perubahan · QA AI independen · versi · eksperimen
L3  KEPUTUSAN    agen AI via antrian job · jalur adaptif siswa
L2  PEMAHAMAN    statistik butir & bagian · penguasaan per bab · health score
L1  JEJAK        event dari seluruh aplikasi, ID konten tetap, versi konten
L0  KONTEN       perpustakaan → topik → bab → Modul Belajar + Latihan (sudah ada)
```

### L1 — Jejak Belajar

**1.1 Identitas tetap untuk setiap unit konten.**
- `QuizQuestion.uid` (UUID) diberikan server saat soal pertama kali ditulis, **tidak pernah berubah** saat soal diurutkan ulang, dinomori ulang, atau diedit. `number` tetap menjadi label tampilan dan kunci jawaban attempt. Soal lama di-backfill.
- Bagian Modul Belajar sudah punya `sections[].id`, jadi tidak perlu diubah.
- Satu soal hasil *rewrite* AI mendapat `uid` baru dengan `derived_from_uid` ke soal asal, supaya statistik versi lama tidak tercampur dengan soal yang isinya sudah berbeda.

**1.2 Versi konten untuk `module_items`** (memperluas ADR-0008 ke model konten baru).
- Tabel `module_item_versions (item_id, version, lesson_plan, quiz_config, content_hash, created_by, created_via, change_summary, published_at, superseded_at)`.
- Setiap *publish* membekukan satu versi. Draft tetap diedit di tempat (aturan ADR-0008 dipertahankan).
- `created_via` ∈ `human | ai_generation | ai_proposal`, supaya asal setiap versi selalu bisa ditelusuri.
- Setiap event dan attempt mencatat `content_version`, sehingga statistik selalu dihitung per versi.

**1.3 `learning_events` diperluas, bukan diganti.** ADR-0002 sudah membaca tabel ini, jadi kolom baru ditambahkan secara aditif:
`source` (konteks: `self_learning | live_class | tryout | assignment | practice | speaking_room | live_ai_chat | canvas | review`), `session_id`, `org_id`, `module_item_id`, `content_uid` (uid soal atau id bagian), `content_version`, `occurred_at` (waktu kejadian di klien, terpisah dari `created_at` di server), `client_event_id` (idempotensi untuk retry dan offline), dan `schema_version`.
- Tabel dipartisi per bulan, karena volume event jauh melampaui tabel lain.
- **Registry event di kode**, dengan pola yang sama seperti registry subtype soal: setiap `event_type` punya skema payload yang divalidasi. Event yang tidak dikenal ditolak, bukan disimpan diam-diam.

**1.4 Dua jalur pencatatan.**
- **Server (otoritatif)** untuk semua yang berdampak nilai atau uang: jawaban dinilai, attempt disubmit, item selesai, kehadiran, pembelian, dan langganan. Dicatat di service yang sama yang menjalankan aksinya.
- **Klien (telemetri)** lewat `POST /events` secara batch, untuk perilaku yang hanya terlihat di browser: waktu baca per bagian, kedalaman scroll, membuka petunjuk, mengganti jawaban sebelum submit, pindah tab, dan audio diputar. Endpoint ini dibatasi laju dan divalidasi registry. Data klien **tidak pernah** dipakai untuk menilai siswa.

**1.5 Sumber sinyal per konteks.**

| Konteks | Yang dicatat | Catatan |
|---|---|---|
| Belajar mandiri (Modul Belajar) | buka/selesai per bagian, waktu baca, scroll, kembali membaca | per `sections[].id` |
| Live AI Chat | **pertanyaan siswa per bagian** + ringkasan topiknya | berubah dari stateless menjadi disimpan (lihat Privasi) |
| Latihan & kuis | jawaban per `uid`, benar/salah, pilihan pengecoh, waktu, petunjuk, ganti jawaban | fondasi statistik butir |
| Tryout | sama dengan kuis + pacing antarsoal | sinyal integritas proctoring **tidak** dipakai untuk menilai konten |
| Kelas live (Meet) | kehadiran, durasi, bergabung ulang; tahap berikutnya: transkrip rekaman lewat STT yang sudah ada | isi kelas memerlukan persetujuan rekaman |
| Canvas & Speaking Room | event canvas yang sudah ada, hasil evaluasi speaking | sudah tercatat sebagian |
| Kebiasaan | streak, jam belajar, panjang sesi, misi harian | dari tabel yang sudah ada |
| Guru/tutor | jadwal vs pelaksanaan, kecepatan menilai, ulasan | untuk Admin Pusat, bukan untuk menilai konten |

### L2 — Pemahaman

**2.1 Bab sebagai konsep.** Setiap bab (section di bawah topik) otomatis menjadi `concept` dengan `parent_concept_id` ke konsep topiknya (ADR-0007), dan setiap item di dalam bab ditautkan lewat `module_item_concepts`, yang tabelnya sudah ada. Dengan begitu 4.949 topik mendapat peta konsep tanpa pemetaan manual. Mastery (ADR-0002), FRSS (ADR-0003), dan rescue mode (ADR-0012) disambungkan ke jawaban `quiz_config` melalui tautan ini, tanpa mengubah rumusnya.

**2.2 Statistik butir** per `(uid, content_version)`, dihitung ulang oleh job (bukan query langsung):
- `n`, indeks kesukaran **p**, daya beda (**korelasi point-biserial**; kelompok atas–bawah 27% sebagai cadangan saat n kecil), proporsi pemilih setiap pengecoh, median waktu, tingkat petunjuk, dan tingkat dilewati.
- **Kesukaran empiris vs label AI**: soal berlabel `mudah` tetapi p < 0,30 ditandai. Inilah alasan kesukaran didefinisikan lewat indeks p sejak awal.
- Teori tes klasik lebih dulu. Model Rasch/IRT ditambahkan setelah satu butir punya ≥200 jawaban.

**2.3 Statistik bagian modul:** tingkat selesai, titik berhenti (drop-off), waktu baca dibanding panjang teks, jumlah dan tema pertanyaan Live AI Chat per bagian, dan korelasi antara membaca suatu bagian dengan hasil latihan bab tersebut.

**2.4 Content Health Score** per item dan per bab. Skor (0–100) disusun dari komponen yang **masing-masing punya tingkat keyakinan berdasarkan jumlah data**. Skor dengan data tidak cukup ditampilkan sebagai "belum cukup data", tidak pernah sebagai angka palsu.
- Komponen kuis: kalibrasi kesukaran, daya beda, kualitas pengecoh (pengecoh yang tidak pernah dipilih), dan indikasi ambiguitas (siswa berkemampuan tinggi justru salah).
- Komponen modul: selesai, drop-off, beban pertanyaan chat, dan dampak ke latihan.
- Kebijakan: 90–100 dibiarkan · 80–89 dipantau · 70–79 dianalisis · <70 diprioritaskan. **Agen hanya bekerja pada item yang turun di bawah ambang**, dan inilah pengendali biaya utama.

### L3 — Keputusan

**3.1 Antrian job di Postgres** (tabel generik `jobs`, dibangun di Fase 40 karena agregasi Admin Pusat membutuhkannya lebih dulu: `job_type, entity, priority, status, attempt, run_after, locked_by, locked_at, error, cost_tokens`), diambil dengan `FOR UPDATE SKIP LOCKED`. Tidak ada infrastruktur baru (Redis/Kafka). Scheduler berjalan sebagai loop tokio. Worker berupa binary kedua di crate yang sama (`titian-worker`), jadi kodenya satu dan deploy-nya bisa terpisah dari API.

**3.2 Pemicu: event + jadwal, bukan polling AI terus-menerus.**
- **Real-time** (siswa menunggu): hanya logika deterministik dan model cepat, misalnya petunjuk dan remedial singkat. Tidak menulis konten induk.
- **Per sesi** (async, beberapa menit setelah kuis/modul selesai): diagnosis siswa dan rekomendasi langkah berikutnya.
- **Batch** (awal: setiap 6 jam; setelah data besar: harian): hitung ulang statistik → health score → cari temuan → buat usulan.

**3.3 Agen**, masing-masing punya satu tugas, input sempit, dan output terstruktur:

| Agen | Tugas | Model |
|---|---|---|
| Analis | statistik & temuan dari data agregat | **deterministik (SQL), tanpa LLM** |
| Diagnosa | menjelaskan *mengapa* suatu item buruk (soal ambigu? penjelasan sebelumnya kurang?), dari data agregat + teks konten + tema pertanyaan chat | diatur di Admin Pusat (§3.5) |
| Editor Konten | menyusun usulan perubahan tingkat bagian/soal memakai `lesson_plan_ai` & `quiz_generation` yang sudah ada (bukan generate ulang modul) | diatur di Admin Pusat (§3.5) |
| QA Independen | menilai usulan: kebenaran fakta, kesesuaian tujuan bab, taksonomi, konstitusi, dan tidak menduplikasi soal lain | diatur di Admin Pusat (§3.5); disarankan model berbeda dari Editor bila tersedia |
| Pelapor | ringkasan harian/mingguan ke Admin Pusat | diatur di Admin Pusat (§3.5) |

**Agen tidak pernah menerima data pribadi**: input berupa agregat, dan ID siswa (bila perlu) di-hash.

**3.5 Model AI diatur dari Admin Pusat, bukan dari kode atau variabel lingkungan.** Setiap peran AI di Titian, baik agen di atas maupun fitur yang sudah ada (pembuatan Modul Belajar, soal, OCR, Live AI Chat, evaluasi writing/speaking/grammar, Speaking Room, STT, TTS), memakai model yang dipilih admin. Model bisa diganti tanpa deploy ulang.

- **Katalog model** (`ai_model_catalog`): provider (`vertex`, `openrouter`, dan provider lain nanti), `model_id`, label, kemampuan (`text`, `vision`, `json`, `stt`, `tts`), batas token keluaran, harga per 1 juta token masuk/keluar, dan status aktif. Katalog ini menggantikan daftar yang sekarang ditanam di kode (`AI_MODEL_OPTIONS`, `VERTEX_MODEL_MAX_TOKENS`).
- **Pengaturan per peran** (`ai_role_settings`): `role` → `model_id`, model cadangan, temperatur, batas token, anggaran harian (token/rupiah), dan status aktif. Daftar peran didefinisikan di kode sebagai registry (pola yang sama dengan registry subtype soal), dan setiap peran menyatakan kemampuan yang dibutuhkannya. OCR butuh `vision`, transkripsi butuh `stt`, dan admin tidak bisa memilih model yang tidak mampu.
- **Urutan resolusi**: pengaturan peran di database → variabel lingkungan yang ada sekarang (menjadi fallback & nilai awal) → `gemini-3.8-flash`. Pengaturan di-cache di memori dan dibuang saat admin menyimpan perubahan.
- **Kredensial provider tetap di secret/env**, tidak pernah disimpan di database atau ditampilkan di Admin Pusat.
- **Setiap perubahan pengaturan masuk log audit**, dan setiap panggilan mencatat model yang benar-benar dipakai di `ai_tasks`, termasuk bila model cadangan yang dipakai.
- **Kondisi awal (2026-09-13)**: semua peran teks & vision memakai **Vertex AI `gemini-3.8-flash`**; STT (`openai/whisper-1`) dan TTS (`hexgrad/kokoro-82m`) lewat OpenRouter. QA Independen sementara memakai model yang sama dengan Editor; independensinya dijaga lewat prompt, temperatur, dan tugas yang berbeda, lalu dipindah ke model lain begitu katalog punya pilihan kedua.

**3.4 Jalur adaptif siswa** ("AI merekomendasikan, siswa memilih"). Setelah diagnosis bab, siswa ditawari **Lanjut Cepat / Standar / Penguatan / Tantangan**. Setiap pilihan disertai alasan singkat dan estimasi waktu yang dihitung dari median waktu nyata. Tantangan = soal C4 ke atas. Penguatan diambil **dari bank soal yang ada dulu**; generate soal baru hanya bila bank tidak punya soal yang sesuai untuk level itu. Pilihan siswa ikut dicatat sebagai event.

### L4 — Perbaikan (semi-otonom)

**4.1 Alur usulan.** Setiap perubahan AI melewati jalur yang sama, dan jalur ini tidak bisa dilewati oleh kode mana pun:

```
temuan → usulan (diff per bagian/soal + bukti data) → QA independen (skor)
      → Admin Pusat: setujui / tolak / minta revisi → versi baru (draft → publish)
      → pemantauan versi baru vs lama
```

Tabel `content_findings` (temuan dan buktinya) dan `content_proposals` (diff, alasan, skor QA, status, keputusan, siapa yang memutuskan). Setiap proposal menautkan statistik yang memicunya, supaya admin melihat *mengapa*, bukan hanya *apa*.

**4.2 Level otonomi per jenis perubahan**, bisa dikonfigurasi dari Admin Pusat. **Semua jenis dimulai dari L1.**

| Level | Artinya |
|---|---|
| L0 | hanya laporan, tanpa usulan |
| L1 | usulan dibuat, **wajib disetujui manusia** |
| L2 | diterapkan otomatis untuk perubahan berisiko rendah (misal typo, pengecoh yang tidak pernah dipilih), admin diberi tahu dan bisa membatalkan |
| L3 | dirilis sebagai eksperimen champion/challenger, dipromosikan otomatis bila menang menurut aturan |

Kenaikan level adalah keputusan admin, dan hanya boleh dilakukan bila rekam jejak usulan jenis itu terbukti baik (tingkat persetujuan tinggi, tidak ada rollback).

**4.3 Konstitusi Konten AI** (ditegakkan di kode, bukan hanya di prompt):
- **Boleh**: mengubah contoh, memperjelas penjelasan, mengubah urutan penjelasan dalam satu bab, menambah petunjuk, menambah soal remedial/pengayaan, menulis ulang soal buruk, mengganti pengecoh, dan mengoreksi label taksonomi.
- **Tidak boleh**: mengubah tujuan pembelajaran atau struktur kurikulum (topik/bab), menghapus konsep wajib bab, mengubah fakta tanpa verifikasi QA, menggeser level Bloom atau kesukaran lebih dari satu tingkat dalam satu usulan, menyentuh soal tryout yang sedang dipakai ujian aktif, dan mengubah konten berbayar milik pihak ketiga (marketplace).
- **Syarat bukti**: temuan berbasis data butuh n minimum (awal: 30 jawaban per butir, 50 pembaca per bagian). Di bawah itu hanya QA AI yang boleh mengusulkan, dengan label "tanpa data siswa".
- **Batas laju**: maksimal N usulan per item per minggu, supaya konten tidak terus bergoyang.
- **Audit**: setiap usulan, keputusan, versi, dan rollback tercatat permanen.

**4.4 Eksperimen champion vs challenger** (Fase 44, setelah volume cukup):
- Penempatan deterministik `hash(user_id, item_id)`, memakai pola seeded yang sama dengan pengacakan soal. Siswa selalu mendapat versi yang sama.
- **Hanya untuk latihan, tidak pernah untuk tryout atau penilaian yang berdampak nilai**, demi keadilan (sejalan dengan snapshot ADR-0008).
- Metrik: p & daya beda butir, penguasaan bab setelahnya, dan tingkat selesai. Promosi hanya bila selisihnya signifikan dan n minimum terpenuhi; bila tidak, champion tetap.

### Privasi & kepatuhan (UU No. 27/2022 tentang Pelindungan Data Pribadi)

Banyak pengguna adalah **anak di bawah umur** (jenjang SD–SMP). Karena itu:
- Persetujuan pencatatan perilaku, termasuk dari orang tua untuk anak, diminta saat onboarding. Tanpa persetujuan hanya event server otoritatif yang dicatat.
- Minimisasi data: telemetri tidak menyimpan isi ketikan bebas selain pertanyaan Live AI Chat. Pertanyaan chat disimpan **dengan ID ter-hash** dan dipakai hanya dalam bentuk ringkasan tema.
- Retensi: event mentah 24 bulan, lalu hanya agregat. Rekaman/transkrip kelas mengikuti kebijakan kelas.
- Hak hapus: menghapus akun menghapus event mentah milik pengguna; agregat anonim tetap.
- Agen AI hanya menerima agregat atau data ter-hash, tidak pernah nama, email, atau nomor telepon.

### Tahapan

| Fase | Isi | Prasyarat |
|---|---|---|
| **39 — Fondasi Jejak** | `uid` soal + backfill, `module_item_versions`, `learning_events` v2 + registry + partisi, event server untuk kuis/modul/tryout, `POST /events`, Live AI Chat disimpan, persetujuan data | — |
| **40 — Admin Pusat v1** | lihat ADR-0014, termasuk **Pengaturan AI** (katalog model + pengaturan per peran, §3.5) | bisa paralel dengan 39 |
| **41 — Mesin Pemahaman** | bab sebagai konsep, mastery/FRSS untuk konten baru, statistik butir & bagian, health score | 39 |
| **42 — Agen Konten Semi-Otonom** | jenis job agen di atas antrean `jobs` (dibangun di Fase 40), agen Analis/Diagnosa/Editor/QA/Pelapor, `content_findings`/`content_proposals`, konstitusi, antrean persetujuan di Admin Pusat | 40, 41 |
| **43 — Jalur Adaptif Siswa** | Lanjut Cepat/Standar/Penguatan/Tantangan + remedial | 41 |
| **44 — Eksperimen & Otonomi L2/L3** | champion/challenger, promosi berbasis kebijakan | 42 + volume data |

**Dampak pada generate konten massal:** generate 26 topik Tahap 1 berikutnya **ditunda sampai `uid` soal (bagian pertama Fase 39) selesai**, supaya ±34 ribu soal lahir dengan identitas tetap dan tidak perlu di-backfill.

## Alternatives considered

- **Bangun ulang LMS dari nol.** Ditolak. Perpustakaan kanonik, 40 tipe soal beserta penilaiannya, pipeline generasi, taksonomi, dan rumus mastery/FRSS sudah ada dan teruji. Masalahnya adalah sambungan antarbagian, bukan fondasinya. Membangun ulang akan menunda lapisan yang benar-benar baru (jejak, agen, versi) berbulan-bulan tanpa menghasilkan kemampuan baru.
- **Tabel event baru yang terpisah dari `learning_events`.** Ditolak. ADR-0002 sudah membaca `learning_events`, dan dua aliran event berarti dua sumber kebenaran untuk perilaku yang sama. Perluasan aditif menjaga pembaca lama tetap jalan.
- **Queue eksternal (Redis/Kafka/Pub/Sub) sejak awal.** Ditunda. Pada volume awal, Postgres `SKIP LOCKED` cukup, transaksional dengan data yang diubahnya, dan tidak menambah komponen yang harus dioperasikan. Pindah ke Pub/Sub dibuka setelah migrasi GCP, bila volume menuntut.
- **Analitik langsung di BigQuery sejak awal.** Ditunda ke setelah migrasi GCP. Tabel agregat di Postgres cukup untuk Admin Pusat v1, dan skema event dirancang agar bisa diekspor tanpa perubahan.
- **Agen otonom penuh sejak awal.** Ditolak. Tanpa data siswa, agen tidak punya dasar untuk memutuskan, dan kesalahan pada kurikulum anak berdampak nyata. Otonomi dinaikkan per jenis perubahan setelah rekam jejaknya terbukti (4.2).
- **Model dipilih lewat variabel lingkungan (seperti sekarang).** Ditolak. Mengganti model butuh deploy ulang, tidak ada jejak siapa mengubah apa, dan tidak ada pemeriksaan apakah model mampu menjalankan perannya (misalnya OCR ke model tanpa vision). Variabel lingkungan tetap dipakai sebagai fallback.
- **Satu model AI untuk semua peran.** Ditolak. Editor dan QA yang memakai model dan prompt yang sama cenderung menyetujui kesalahannya sendiri. Analisis statistik juga tidak butuh LLM sama sekali.

## Consequences

- Setiap soal dan bagian modul punya identitas dan versi. Statistik, usulan, dan eksperimen selalu merujuk ke konten yang tepat.
- Mastery, FRSS, dan rescue mode akhirnya bekerja pada konten yang benar-benar dipakai siswa.
- Volume tulis database naik tajam karena event. Partisi bulanan dan retensi wajib sejak Fase 39.
- Live AI Chat berubah dari stateless menjadi menyimpan pertanyaan. Ini perlu persetujuan data dan ditinjau dari sisi privasi.
- Semua perubahan konten oleh AI melewati Admin Pusat, sehingga ADR-0014 menjadi prasyarat agen konten (Fase 42).
- Biaya AI bisa dikendalikan: analisis tanpa LLM, agen hanya menyentuh item di bawah ambang health score, dan setiap job mencatat token.
- Keputusan yang butuh volume (A/B, IRT, otonomi L3) sengaja dijadwalkan terakhir. Sebelum data cukup, sistem jujur menampilkan "belum cukup data".
