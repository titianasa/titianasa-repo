# ADR-0017: Percakapan suara di Kampung Bahasa Pare (voice note & live audio)

Status: **Proposed** — diputuskan user 2026-09-25: §11.2 (sudah saling membalas chat), §11.3 (STT bawaan browser), §11.5 (retensi 3 hari; live tidak disimpan), §11.8 (Camp = aturan Kampung Bahasa), aturan bahasa ketat per zona, dan anjuran Google Chrome. Masih terbuka: §11.1, §11.4, §11.6, §11.7. Belum ada kode.
Date: 2026-09-25
Supersedes: -
Superseded by: -
Related: ADR-0016 (Kampung Bahasa Pare), ADR-0014 (Admin Pusat), ADR-0005 (credit economy), P39-007 (`user_data_consent`)


> **Status 2026-09-26:** bagian evaluasi bahasa dari transkrip (§3, §3a, §3b, §4 penalti, dan pengawasan live) **dilepas sementara** dan tidak berjalan; kode arsip di `titian-backend-rust/attic/pare-voice-evaluation/`. Bagian lain (voice note, panggilan live, privasi, moderasi) tetap berlaku. Keputusan hukum soal audio ke penyedia AI tidak lagi relevan selama STT dimatikan.

> **Catatan migrasi (2026-10-05, ADR-0020):** backend sedang dipindah dari Rust ke Go. Keputusan di ADR ini tidak berubah; setiap "Rust" / `titian-backend-rust` / `services/pare_*.rs` di bawah berpadanan dengan `titian-backend-go/internal/pare/` setelah tiket G14. Sampai G14 selesai, kode Pare yang aktif tetap yang Rust.

## Context

Setelah Pare-4, chat Personal & Grup sudah tersimpan di server dan aturan bahasa (teks) dinilai server. User ingin **percakapan bersuara** untuk melatih *speaking*, dengan batasan yang sudah diputuskan:

- **Hanya 1-on-1 dan grup kecil** (chat Personal & Grup yang sudah ada). **Tidak** di Kampung Bahasa / saluran (puluhan orang: berat secara teknis dan kacau secara UX).
- **Gerbang level per bahasa**: percakapan **live (real-time)** hanya untuk level **A2 ke atas**; level **Basic dan A1** boleh bersuara tetapi **tidak real-time** — berupa **voice note**.
- **Penegakan bahasa lewat transkrip**: semua suara ditranskrip (STT); bahasa dideteksi dari transkrip; bila bukan bahasa yang ditentukan → peringatan/penalti (kurangi poin/nyawa). Berlaku sama untuk voice note dan live (untuk live, penilaian **tertunda** — percakapan tidak terganggu, hasilnya keluar setelahnya).
- Backend Rust, Redis, Postgres (arsitektur Titian). Game tetap aplikasi mandiri di Vercel; audio real-time tidak bisa lewat Vercel.

Yang sudah ada dan dipakai ulang: `AIProvider::transcribe(audio, mime, model)` (Whisper, konfigurasi `AI_STT_MODEL`), `services/storage.rs` (objek + URL bertanda tangan), `services/job_queue.rs` + `titian-worker`, Redis, `user_data_consent` (termasuk konfirmasi wali untuk jenjang SD/SMP), hub realtime Pare (`/ws/pare`), `pare_langrule.rs`, ledger `pare_ledger`, Admin Pusat (ADR-0014).

## Decision

### 1. Dua mode, dipilih otomatis oleh level

| Mode | Syarat | Cara kerja |
|---|---|---|
| **Voice note** (async) | Semua level (Basic, A1, dst.), 1-on-1 & grup | Rekam di browser → unggah → dikirim sebagai pesan bertipe `voice` → penerima memutar kapan saja. Transkrip & penilaian bahasa berjalan di belakang. |
| **Live** (real-time) | **Semua peserta** ≥ A2 **pada bahasa percakapan** | Panggilan lewat SFU. Audio mengalir real-time; transkrip & penilaian berjalan paralel dan tertunda. |

- **Bahasa yang boleh dipakai mengikuti zona tempat pembicara berada** (keputusan user 2026-09-25), sama seperti chat teks:
  - **Kampung bahasa** (en/zh/ar/ja/ko): hanya bahasa kampung itu.
  - **Kampung Bahasa**: salah satu dari **Inggris, Korea, Mandarin, Jepang, Arab**; bahasa Indonesia dan bahasa lain tidak boleh.
  - **Camp** (kamar pribadi): **ikut aturan Kampung Bahasa** (diputuskan 2026-09-25) — berlaku juga untuk chat teks sejak 2026-09-25.
  - **Ketat** (diputuskan 2026-09-25): selain bahasa yang diizinkan, bahasa lain (Prancis, Spanyol, Rusia, Thai, …) juga pelanggaran; kalimat Latin ≥ 3 kata yang tidak terbaca sebagai bahasa yang diizinkan = pelanggaran, 1–2 kata dimaafkan. Sudah berlaku untuk chat teks (`pare_langrule.rs` & `langrule.ts`, 588 kasus paritas).
  - Di Kampung Bahasa/Camp pembicara **memilih bahasa yang akan dipakai** sebelum merekam/menelepon (default: `focus`) — pengenal suara browser butuh satu bahasa (§3a).
  - Gerbang level: voice note memakai level *pengirim* pada bahasa yang dipakai; live memakai level *semua* peserta pada bahasa yang dipilih pemrakarsa.
- **Pemetaan A2** memakai tangga level yang sudah ada (`ladder[lang][level].cefr`), disimpan sebagai konfigurasi server (`voice.live_min_level` per bahasa di `content.json`), bukan hard-code FE. Usulan awal: **en = 2 (A2)**, **ja = 2 (N4)**, **ko = 2 (TOPIK 2)**, **zh = 3 (HSK 3; HSK 2 masih A1+)**, **ar = 1 (Mubtadi' A1–A2)** — lihat pertanyaan §11.
- Pemetaan ini konsisten dengan standar internasional (CEFR / HSK / JLPT / TOPIK); tidak membuat standar sendiri.

### 2. Live audio: SFU **LiveKit** self-hosted; backend Rust hanya "penjaga pintu"

- **LiveKit server** (Apache-2.0, tanpa batas lisensi; batasnya kapasitas hardware). **1-on-1 = ruang berisi 2 orang** sehingga satu jalur untuk semua kasus. Maks. peserta live: **6** (sama dengan grup chat: 1 + `MAX_PRIVATE` 5).
- **TURN**: pakai TURN bawaan LiveKit (UDP 3478 / TLS 5349) atau `coturn`; wajib untuk jaringan seluler/kampus yang ketat.
- Media **tidak** lewat backend Rust. Rust hanya: memeriksa izin (§4), membuat **token akses LiveKit berumur pendek** (JWT HS256 dengan API key/secret LiveKit — `jsonwebtoken` sudah ada di dependensi), dan mengelola undangan/ruang.
- **Alur**: A menekan 📞 di percakapan → `POST /pare/voice/rooms` (Rust cek gerbang level, persetujuan, blokir, batas laju) → ruang dibuat, status `ringing` di **Redis** (TTL 45 dtk) → undangan dikirim ke peserta lewat `/ws/pare` (`voice_invite`) **dan Web Push** (Pare-5) bila offline → B menerima → `POST /pare/voice/rooms/{id}/join` → Rust mengeluarkan token per peserta → klien memakai `livekit-client` → audio via SFU. Webhook LiveKit (`participant_joined/left`, `room_finished`) memperbarui Redis dan Postgres.
- **Redis** (sementara, sering berubah): undangan tertunda, ruang aktif, siapa di ruang mana, penanda "sedang bicara", batas laju, satu-panggilan-aktif-per-pemain. **Postgres** (permanen): sesi, peserta, durasi, strike, laporan (§5, §7).
- Enkripsi transport: DTLS-SRTP bawaan WebRTC (jangan dimatikan). End-to-end **tidak** wajib (dan menghalangi penilaian bahasa di server).

### 3. Transkripsi & penilaian bahasa (inti aturan permainan)

Satu jalur untuk voice note dan live — **pengenalan suara di browser pembicara, penilaian di server**:

```
mikrofon pembicara
  → SpeechRecognition bawaan browser (lang = bahasa zona / bahasa yang dipilih, continuous, interim off)
  → hasil: teks + confidence per potongan kalimat
  → dikirim ke server (voice note: bersama audio; live: lewat /ws/pare `voice_transcript` per 15–30 dtk)
  → server: pare_langrule.judge(zona, teks) + aturan confidence (§3a)
  → verdict per potongan → strike → penalti (§4)
Server TIDAK menerima/menyimpan audio live, dan tidak menjalankan STT sama sekali.
```

- **Live tidak butuh LiveKit Egress lagi**: tiap klien mentranskrip mikrofonnya sendiri, sehingga pelanggaran otomatis teralamat ke orang yang benar.
- **Toleransi**: ucapan < 4 kata, kosong, nama/angka/salam pendek = netral. *Catatan implementasi (2026-09-26, dari data uji nyata):* SpeechRecognition Chrome mengeluarkan satu hasil final **per jeda**, sehingga satu tarikan napas datang sebagai beberapa potongan 1–3 kata; potongan berurutan karena itu digabung menjadi satu ucapan sampai ≥ 4 kata sebelum dinilai (`pare_speech::judge_speech`), kalau tidak, tak ada yang pernah dinilai dan jeda tiap beberapa kata bisa dipakai menghindari aturan. Uji nyata juga menunjukkan pengenal yang dikunci ke Inggris mengubah ucapan Indonesia/Jawa menjadi kata mirip-Inggris ber-*confidence* tinggi (0,76–0,92) — sinyal confidence di §3a tidak seandal asumsinya; itulah gunanya mode shadow. Ambang dikalibrasi di **mode shadow** (catat, belum menghukum) sebelum penalti dinyalakan.
- Hasil live tampil **setelah sesi** ("Percakapanmu selesai dianalisis: 1 peringatan"); UI memberi tahu sejak awal bahwa percakapan dianalisis.

### 3b. Pembaruan 2026-09-26 — STT di server untuk voice note (menggantikan §3a sebagai sumber utama)

Uji nyata (rekaman pengguna + klip TTS lewat 11 model OpenRouter) membuktikan Web Speech tak bisa dijadikan penegak bahasa: pengenal yang dikunci ke Inggris mengubah ucapan Indonesia/Jawa menjadi kata mirip-Inggris ber-confidence tinggi. Maka voice note **ditranskrip di server** dengan model STT yang tidak mengunci bahasa; teksnya dinilai `pare_langrule` per zona seperti biasa, transkrip browser hanya cadangan. Model dipilih dari hasil uji, bukan dari harga: `qwen/qwen3-asr-flash-2026-02-10` (±US$0,002/menit) — model termurah (`qwen3-asr-0.6b`) memotong isi ("你好。" saja dari satu kalimat Mandarin), `whisper-large-v3-turbo` menjawab dengan aksara Mandarin untuk ucapan Jawa (di Kampung Bahasa itu justru dianggap sah), `whisper-large-v3` menyebut ucapan Inggris sebagai "Halo, apa kabar?", dan `nemotron`/`parakeet` tak mengerti Indonesia. Korea dan Arab belum terverifikasi empiris (belum ada audionya). **Konsekuensi privasi (§6):** audio kini dikirim ke penyedia AI pihak ketiga (OpenRouter → penyedia model), bukan hanya ke Google via Chrome — teks persetujuan diperbarui (versi 2026-09-26) dan perlu ditinjau hukum sebelum rilis publik. Live (§2) tetap tanpa STT server sampai P7-010.

### 3a. Mesin STT: **bawaan browser (Web Speech API)** — keputusan user 2026-09-25 (menggantikan whisper.cpp)

- **Gratis, tanpa server STT, tanpa GPU/VM tambahan untuk STT.** Game sudah memakai `SpeechRecognition` untuk soal "Ucapkan" (`src/game/speech.ts`), jadi pola & izin mikrofon sudah ada.
- **Browser tidak mendeteksi bahasa** — ia mengenali **satu bahasa yang ditentukan** (`lang`). Maka:
  - bila pemain berbicara bahasa Indonesia dengan pengenal **Inggris**, hasilnya biasanya berupa kata-kata Indonesia/campur → tertangkap `pare_langrule` (sudah teruji 518 kasus);
  - dengan pengenal **Mandarin/Jepang/Korea/Arab**, bahasa lain sering menjadi teks acak ber-*confidence* rendah atau kosong → aturan tambahan: potongan dengan confidence < ambang (awal 0,45) atau "tak terbaca" berturut-turut dihitung **strike lemah** (2 strike lemah = 1 strike). Ini lebih lemah daripada deteksi bahasa sungguhan — dikalibrasi di mode shadow.
- **Transkrip dibuat di perangkat pemain → bisa dipalsukan** oleh klien yang dimodifikasi (mengirim teks "benar" walau berbicara bahasa lain). Mitigasi: (1) **laporan & blokir** (§7) sebagai lapisan utama untuk kecurangan disengaja; (2) untuk live, server membandingkan aktivitas bicara dari LiveKit (webhook *active speaker*) dengan transkrip yang masuk — bicara tanpa transkrip = ditandai dan dihitung "tak terbaca"; (3) voice note tetap menyimpan audio selama 3 hari (penerima perlu memutarnya), sehingga laporan dalam 3 hari bisa ditinjau manusia dengan mendengarkan.
- **Browser: Google Chrome** (diputuskan 2026-09-25). Game menganjurkan Chrome sejak layar login (sudah dipasang: `src/lib/browser.ts`, pemberitahuan + tautan unduh di luar Chrome) dan di Bantuan. Fitur suara hanya diaktifkan di Chrome (desktop, Android, iOS/CriOS); browser lain: tombol nonaktif dengan alasan "Fitur suara butuh Google Chrome".
- **Privasi**: di Chrome, pengenalan suara standar mengirim audio ke layanan Google (bukan server kita); Safari/Chrome terbaru bisa memproses di perangkat. Disebut jelas di layar persetujuan (§6).
- Opsi cadangan bila kecurangan/akurasi bermasalah: whisper.cpp self-host di VM terpisah (rancangan sebelumnya) — tidak dikerjakan sekarang.

### 4. Penalti & gerbang (anti-penyalahgunaan)

- **Strike bertingkat** (tidak langsung berat): segmen melanggar → +1 strike sesi; tiap **2 strike = −½ nyawa** lewat `pare_ledger` (`kind='voice_violation'`), **maks −1 nyawa per sesi/voice note**. Berulang: **3 penalti dalam 24 jam → fitur suara dikunci 24 jam**; pelanggar kambuhan naik ke 72 jam / tinjauan moderator.
- **Gerbang memulai voice** (bukan sembarang akun): level ≥ syarat bahasa, sudah **persetujuan suara** (§6), tidak diblokir oleh/memblokir lawan, dan **hubungan: sudah saling membalas chat** (keputusan user 2026-09-25) — Personal: masing-masing pihak sudah mengirim minimal 1 pesan teks di percakapan itu; Grup: pengirim voice note sudah mengirim teks di grup itu dan minimal satu anggota lain sudah membalas; panggilan live grup: setiap peserta yang diundang sudah pernah mengirim teks di grup itu. Mengurangi undangan suara dari orang asing/akun spam. Tidak perlu fitur teman.
- Batas laju: undangan 5/menit, 30/jam per pemain; 1 panggilan aktif per pemain; voice note maks 60 dtk & 10/menit.

### 5. Penyimpanan & retensi (minimal, terukur)

| Data | Disimpan | Retensi |
|---|---|---|
| Audio **voice note** | Cloudflare R2 (penerima perlu memutarnya) | **3 hari**, lalu dihapus (tautan bertanda tangan pendek) |
| **Transkrip voice note** + verdict | Postgres | **3 hari**, lalu dihapus |
| **Live** — audio | **tidak pernah** sampai ke server kita (hanya lewat SFU) | — |
| **Live** — transkrip | **tidak disimpan sama sekali**: teks dinilai di memori saat masuk lalu dibuang | — |
| Strike / penalti (tanpa isi percakapan) | Postgres (`pare_ledger`, `pare_voice_strikes`) | seperti ledger lain |
| Log sesi live (siapa, kapan, durasi — tanpa isi) | Postgres | 1 tahun |
| Laporan | Postgres (kutipan transkrip voice note bila ada; untuk live hanya keterangan pelapor) | sampai ditinjau + 1 tahun |

Semua terhapus bila akun game dihapus (`on delete cascade`). Diputuskan user 2026-09-25: voice tidak perlu disimpan lama; live tidak disimpan di backend sama sekali. Konsekuensi: laporan atas panggilan live tidak punya bukti isi — tinjauan memakai keterangan pelapor, pola strike, dan jumlah pelapor berbeda.

### 6. Persetujuan, privasi, dan hukum

- **Persetujuan eksplisit sebelum suara pertama** (versi teks disimpan: `pare_voice_consents(user_id, version, accepted_at)`): "suaramu diubah menjadi teks oleh browser untuk memeriksa bahasa sesuai zona; voice note (audio + teks) disimpan 3 hari; panggilan live tidak disimpan". Tanpa persetujuan: tombol suara nonaktif.
- Suara = data pribadi (UU PDP). Wajib: kebijakan privasi/ToS diperbarui **sebelum fitur live**, dasar persetujuan, hak hapus, dan tidak ada perekaman permanen. Untuk pemain di bawah umur, ikuti alur konfirmasi wali `user_data_consent` yang sudah ada (`consent_guardian_confirmation_required`). *Ini bukan nasihat hukum — perlu ditinjau oleh user/penasihat hukum sebelum rilis publik.*
- Pengenalan suara berjalan di **browser pemain** (§3a); pada Chrome audio diproses layanan Google — disebut di persetujuan. Server hanya menerima teks transkrip (dan audio voice note untuk diputar penerima).

### 7. Moderasi & keselamatan

- **Laporkan** & **blokir** (`pare_blocks`, `pare_voice_reports`): tombol di panggilan/voice note; laporan menyimpan kutipan transkrip (bukti tanpa audio) dan sesi terkait.
- **Auto-mute sementara** untuk pelapor→terlapor di ruang itu, dan penandaan otomatis bila terlapor dilaporkan ≥ 3 orang berbeda dalam 7 hari (masuk antrean tinjauan).
- **Tinjauan manusia** lewat Admin Pusat (ADR-0014): antrean laporan, tindakan (peringatan, kunci suara N hari, kunci akun) tercatat di ledger moderasi. Mulai dengan tim kecil; moderasi suara berbasis AI ditunda.
- Pemain dapat **mematikan penerimaan undangan suara** (pengaturan privasi) dan **melarang undangan dari non-teman**.

### 8. Skala & biaya (perkiraan kasar, untuk keputusan)

- **LiveKit**: audio-saja, ruang kecil → satu VPS 4 vCPU/8 GB menampung puluhan ruang serentak; skala keluar dengan node tambahan. Biaya awal: 1 VPS media (± US$40–80/bln) + TURN (bawaan) — jauh di bawah angka "US$400–1.200/bln" yang berlaku untuk skala menengah-besar.
- **STT**: bawaan browser (§3a) — **Rp0**, tanpa server. Voice note (7a) tidak menambah infrastruktur sama sekali (audio di Cloudflare R2 yang sudah dipakai backend).
- **Hosting (GCP, dicek 2026-09-25)**: satu-satunya VM `titian-prod-vm` (e2-medium, 2 vCPU shared, 4 GB, Jakarta) sudah memuat backend + Postgres + Redis — **LiveKit jangan di sana**. Untuk 7b: VM baru `pare-voice` (e2-standard-2, ±US$55–65/bln, `asia-southeast2`), IP statis, firewall tag `pare-voice` (UDP 3478 & 7882, TCP 7881, TLS 5349, 443). Tanpa Egress & tanpa whisper, e2-small (±US$15–20/bln) mungkin cukup di awal — diukur di P7-011.
- Diukur di tiket P7-011 sebelum rilis.

### 9. Frontend

- `livekit-client` (JS) untuk live; `MediaRecorder` (opus/webm) untuk voice note; tombol **🎙 voice note** dan **📞 panggil** di tiap percakapan Personal/Grup (aktif sesuai gerbang, dengan alasan bila nonaktif: "Live mulai level A2 di bahasa ini"). Overlay panggilan (mute, keluar, laporkan, indikator bicara). Notifikasi panggilan masuk lewat `/ws/pare` dan Web Push (bergantung Pare-5).
- Tidak ada aturan/angka di FE: kelayakan, batas, dan hasil penilaian dari server (`GET /pare/voice/eligibility`).

### 10. Urutan pengerjaan yang diusulkan

1. **Pare-5** PWA + push (dibutuhkan untuk panggilan masuk saat tab tidak terbuka) → **Pare-6** Vercel.
2. **Pare-7a — voice note** (R2 + STT browser; tanpa infrastruktur baru): P7-001…P7-006, P7-008.
3. **Pare-7b — live**: LiveKit + TURN di VM GCP baru + moderasi lanjutan: P7-007, P7-009, P7-010, P7-011.
Voice note dulu karena murah, sudah memenuhi kebutuhan level Basic/A1, dan menghasilkan data nyata untuk mengkalibrasi ambang penilaian bahasa sebelum live.

### 11. Pertanyaan terbuka (butuh keputusan user)

1. **Pemetaan A2 per bahasa** (usulan di §1: en 2, ja 2, ko 2, zh 3, ar 1). Khusus Arab: Mubtadi' mencakup A1–A2 — cukup, atau live baru mulai Mutawassith (level 2)?
2. ~~Hubungan sebelum voice~~ — **diputuskan 2026-09-25: cukup sudah saling membalas chat** (§4).
3. ~~STT~~ — **diputuskan 2026-09-25 (revisi): STT bawaan browser**; server hanya menilai teks sesuai aturan zona (§3a).
4. **Penalti**: setuju "2 strike = −½ nyawa, maks −1 per sesi, 3 penalti/24 jam = kunci suara 24 jam", dan **mode shadow** (catat tanpa menghukum) selama beberapa minggu awal untuk kalibrasi?
5. ~~Retensi~~ — **diputuskan 2026-09-25: voice note (audio + transkrip) 3 hari; live tidak disimpan sama sekali** (§5).
6. **Hosting LiveKit**: GCP (satu-satunya penyedia saat ini) — setuju VM baru `pare-voice` di Jakarta (§8), dibuat saat 7b?
7. **Dampak ekonomi**: apakah voice memberi hadiah (mis. poin/uang kecil untuk sesi berbahasa target) atau murni fitur sosial/latihan? Usulan: **tanpa hadiah uang** (mudah dieksploitasi dua akun), boleh XP bahasa kecil dengan batas harian.
8. ~~Aturan suara di Camp~~ — **diputuskan 2026-09-25: ikut Kampung Bahasa** (juga chat teks).

## Consequences

- Voice note (7a) tidak menambah komponen operasional; live (7b) menambah **LiveKit + TURN** di satu VM GCP. Tidak ada biaya STT.
- Penegakan bahasa lebih lemah daripada STT server (transkrip bisa dipalsukan, bahasa non-Latin dinilai lewat confidence) — ditutup dengan laporan/moderasi dan kalibrasi shadow.
- Penilaian tertunda berarti pelanggaran terlihat beberapa menit kemudian — dijelaskan di UI; ambang salah-positif harus dikalibrasi (shadow mode).
- Data suara membawa kewajiban hukum/privasi; rilis publik bergantung pada persetujuan, kebijakan privasi, dan moderasi yang siap.
- Hub realtime (`/ws/pare`) dan `pare_messages` diperluas (pesan bertipe `voice`, pesan `voice_invite`), tanpa mengubah kontrak yang ada.
