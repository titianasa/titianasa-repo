# Tiket Pare-9 — Jalur belajar & misi dunia terbuka

> **Peta Kampung Inggris besar (2026-10-07):** `game/src/game/world/english.ts` (79×60, ditulis dalam koordinat desa lalu digeser `EN_OY`=14; `backCountry()` = sungai + dermaga pancing, sawah, taman bunga di belakang kampus). Kampus ENGLISH ACADEMY dengan tulisan atap menyala malam, gerbang selatan lebar, interaksi di seluruh sisi depan gedung (`frontage`), patung singa/pagar tanaman/bendera/ayunan/halte bus (`engine/scenery.ts`). Kereta kelinci nyata: stasiun (objek `train`) di Zona Umum dan kelima kampung, `POST /pare/train` (Rp5.000), rencana rute `world/tour.ts`, autopilot `engine.driveAlong`, tombol TURUN. Perbaikan server: `clampCoord` di hub memotong koordinat ke 64 (pemain di timur Zona Umum/Kampung Inggris tampak bergeser) → 127. Alat: `bun scripts/check-map.ts <zona> [--ascii|--approach]`.
>
> **A1 Inggris (2026-10-07):** 14 bab (`chapters.ts` level 1, sama persis dengan rencana `journey/en/l1.ts`), 14 misi bab (`missions/en1.ts`), 10 misi warga (`en1-villagers.ts`), Misi Besar "Pesta kampung" (`en1-big.ts`), 25 perayaan (`celebrations.ts`), 4 warga baru di peta (Mr. Brown, Emma, Jack, Mr. Patel). Tidak ada gedung baru: rumah Brown = lantai atas MINIMART, sekolah = ENGLISH CLASS, taman bermain = PARK, kantor pos/wisma = Mr. Patel/Mrs. Hughes di plaza dan gerbang (adegan interior tetap menunggu P9-012). Langkah `tulis/ucap/komputer/waktu/temukan` dari rencana diganti dialog berketik/pilihan karena mesin belum memverifikasinya. Lolos: `bun scripts/check-chapters.ts`, `bun scripts/missions.ts`, `bun scripts/journey.ts`, tes Go, 14 bab (284 node) + 25 misi dimainkan via API sampai naik ke A2, dan tiga misi dimainkan lewat UI berhadapan dengan NPC.
>
> **Pembaruan 2026-10-06:** cutover ke Go selesai; kerjakan semua di `titian-backend-go` (data misi: `titian-backend-go/data/pare/missions.json`, diekspor `bun scripts/missions.ts --write`). Selesai di Go: syarat bab per misi warga (`requires` → `requirement` di kartu, tombol KE JALUR membuka bab itu), scene perayaan misi + gambar bagikan (`MissionCelebration.tsx`, dibuat di perangkat), tombol KEMBALI di jendela yang dibuka dari jendela lain, middleware `decodedPath` (id misi `a:b` terkirim `%3A`). 16 misi Basic Inggris dimainkan penuh via API di Go.
>
> **Catatan migrasi backend (2026-10-05, ADR-0020):** backend sedang dipindah ke Go. Tiket ini ditulis untuk `titian-backend-rust`, dan kode Rust tetap yang aktif sampai domain ini diport (G14, lihat `phase-51-go-migration.md`). Pekerjaan yang belum dieksekusi: bila G14 sudah selesai saat tiket ini dikerjakan, kerjakan di `titian-backend-go` (`#[sqlx::test]` → test Go dengan `testdb.New`, `services/x.rs` → `internal/<domain>/`); bila belum, kerjakan di Rust dan catat endpoint/migrasi barunya di daftar paritas fase 51.

📋 **RENCANA (2026-10-04, revisi kedua)** — **belum ada kode jalur maupun misi.** ADR-0019 sudah Accepted (keputusan §15 diambil 2026-10-04); tiket boleh dikerjakan berurutan. Dokumen ini ditulis supaya bisa dikerjakan oleh pengembang (atau model) yang tidak ikut merancangnya.

## Baca dulu, berurutan

1. [ADR-0019](../adr/0019-jalur-belajar-dan-misi-pare.md) — aturan: susunan kurikulum (§2–§4), misi (§5–§8), dunia (§10), arsitektur (§13), misi dari sisi pemain (§16), multipemain (§17).
2. [`pare-perjalanan/README.md`](../pare-perjalanan/README.md) lalu [`en-ringkasan.md`](../pare-perjalanan/en-ringkasan.md) — isi: tujuh level, 81 bab, 158 misi, daftar kebutuhan.
3. Halaman level yang sedang dikerjakan (`pare-perjalanan/en-0-basic.md`, …).
4. Data sumbernya: `alr/game/src/game/content/journey/` (`types.ts`, `en.ts`, `en/world.ts`, `en/l0.ts` … `l6.ts`) dan pemeriksanya `alr/game/scripts/journey.ts`.
5. `pare-benchmark-level.md` dan `game/src/game/content/benchmark.ts` — kontrak isi tiap level.

## Yang sudah ada

- Isi pelajaran Basic sampai B1-setara di lima bahasa (lolos `check-benchmark.ts` dan tes backend `every_language_meets_the_level_benchmark`).
- Audio rekaman Basic lima bahasa (pipeline `game/scripts/audio`; cakupan 100%).
- Rencana perjalanan bahasa Inggris sebagai data bertipe + pemeriksa + halaman baca (butir 4 di atas). **Data itu rencana**: belum diimpor game, belum diekspor ke `content.json`.
- Mesin soal, penilai menulis (`pare_compose.rs`), kehidupan, hub realtime, chat, suara: lihat ADR-0019 Context.

## Repo yang disentuh

`titian-backend-rust` (migrasi `pare_*` mulai **0095**; `services/pare_path.rs`, `pare_mission.rs`, `pare_session.rs`, `pare_board.rs`; perluasan `pare_paper.rs`, `pare_lesson.rs`, `pare_hub.rs`), `alr/game` (DSL `chapters` dan `missions`, jendela Jalur, Buku Perjalanan, kartu dan rapor misi, komputer, engine), `agent/docs` (`domain-model.md`, `api-contract.md`, `STATE.md`).

## Aturan main eksekusi

Sama seperti Pare-1…8: migrasi aditif dan idempoten; `domain-model.md` dan `api-contract.md` ikut diperbarui; tes integrasi `#[sqlx::test]` per tiket; verifikasi di browser sungguhan (minta izin user sebelum membuat akun uji, hapus setelahnya); tidak commit dan tidak deploy tanpa diminta; waktu harian WIB. Kunci OpenRouter ada di `.env` backend (`OPENROUTER_KEY_PARE`) dan tidak pernah dicetak.

## Yang WAJIB dipertahankan

- Server satu-satunya penilai: kunci jawaban, status dan skor misi, hadiah, dan pembukaan wilayah tidak pernah diputuskan klien.
- Kata atau konsep baru tidak pernah muncul sebagai soal sebelum Materinya dibuka.
- Di jalur belajar XP tidak berkurang; hadiah hanya pada penyelesaian pertama tiap simpul (§15.1).
- **Tiap misi wajib selesai sendirian, kapan saja**: tiap langkah `sosial` dan tiap mode bersama punya pengganti NPC dengan batas tunggu; tiap langkah `ucap` punya jalur ketik; tidak ada langkah yang menunggu jam atau cuaca tertentu.
- Percakapan NPC selalu pribadi per pemain; NPC tidak pernah dikunci.
- Skor pemain hanya dari jawabannya sendiri; pemain lain tidak bisa menurunkannya.
- Isi misi diacak per pemain dengan benih (pemain, misi), supaya jawaban tidak bisa disalin.
- Semua teks yang diucapkan punya klip audio (tes `every_spoken_text_…` diperluas ke bab dan misi).
- Tulisan pemain hanya tampil ke pemain lain setelah lulus penilaian dan saringan moderasi.
- Pemain lama tidak kehilangan level maupun kata yang sudah dikuasai.
- `bun scripts/journey.ts` harus tetap lolos; halaman `pare-perjalanan/en-*.md` dihasilkan ulang (`--write`) kalau data berubah.

Ukuran tiket: S (kecil), M (sedang), L (besar).

---

# Pare-9a — Jalur Basic (lima bahasa)

## P9-001 — Kontrak konten bab (M) ✅ (bab ada di `content.json`, dibaca `pare_path::layout`)
DSL `chapters` di `game/src/game/content/dsl.ts`. Peta bab Basic untuk en (dari `journey/en/l0.ts`), zh, ja, ko, ar (bab = topik Basic di benchmark, dengan bab aksara di depan untuk bahasa beraksara). Tiap kata ditugaskan ke satu bab. Ekspor ke `content.json`. `check-benchmark.ts`: tiap kata dan konsep ada di tepat satu bab; tiap bab punya ≥ 1 pelajaran dan bahan Praktik (atau `extra`).
**DoD:** pemeriksa gagal bila ada kata atau konsep yatim atau ganda; tes backend membaca `chapters`.

## P9-002 — Skema & status jalur (M) ✅ (`0095`, `pare_path.rs`, tes `pare_path_test`)
Migrasi `0095_pare_path.sql`: `pare_path_nodes`; kolom `pare_papers.node`, `wrong_scale`, `reward`; jenis kertas `path`. `pare_path.rs`: susunan simpul per bab, status (selesai, terbuka, terkunci), selesai otomatis untuk bab yang katanya sudah dikuasai. `GET /pare/path/{lang}`.
**DoD:** tes urutan pembukaan, pemetaan pemain lama, bahasa tanpa aksara (en) dan beraksara.

## P9-003 — Materi (M) ✅ (API + pembaca kartu di `PathModal.tsx`)
`GET /pare/path/{lang}/lessons/{id}` (kartu kata, konsep, huruf) dan `POST …/done` (menandai selesai, mencatat kata sebagai "pernah dilihat" tanpa menambah "benar"). Komponen kartu di game dengan audio rekaman.
**DoD:** Materi tidak pernah memberi XP; kata yang belum di-Materi tidak muncul di soal jalur (tes).

## P9-004 — Latihan, Praktik, Cek (L) ✅ (butir salah diulang, hadiah sekali, tanpa potongan XP; tes loncat bab belum)
Penyusun soal per simpul di `pare_lesson.rs`: Latihan (hanya isi pelajaran + 2 ulangan lemah; urutan kenali → dengar → susun → ketik; butir salah diulang), Praktik (situasi, dialog, bacaan bab; disisipkan tiap 2–3 pelajaran), Cek (campuran, lulus ≥ 80%, daftar pelajaran yang perlu diulang). Tanpa potongan XP; hadiah sekali. Tes loncat bab (≥ 90%).
**DoD:** tes hadiah-sekali, tanpa potongan XP, ambang lulus, pengulangan butir salah, tes loncat.

## P9-005 — Jendela Jalur (M) ✅ (`PathModal.tsx`, uji di browser headless `Bun.WebView`: ponsel; Cek bab, pemain lama dan Praktik belum diuji di browser)
Pengganti menu kelas: kepala level, tombol besar "Lanjut", daftar bab dengan simpul berlabel 📖 🧩 🎯 🏁 ⭐, tab "Latihan bebas" berisi enam kelas lama. Judul sesi menyebut tahapnya.
**DoD:** diuji di browser untuk pemain baru dan pemain lama; layar ponsel.

---

# Pare-9b — Mesin misi + misi Basic bahasa Inggris

## P9-006 — Skema, mesin langkah, dan skor (L) ✅ backend (`0096`, `pare_mission.rs`, `data/pare/missions.json` berisi 2 misi Basic; `pare_mission_test` 7 tes). Jenis langkah: pergi, bicara, dialog, beli, lakukan, baca, dengar, temukan; `tulis`/`presentasi`/`sosial`/`ucap`/`telepon`/`komputer` belum. Zona dicek dari `pare_players.zone`, bukan posisi
Migrasi `pare_missions`, `pare_unlocks`. `pare_mission.rs`: mulai, status, maju saat kejadian masuk (dipasang di titik `pare_daily::bump` dan interaksi NPC atau objek); jenis langkah Basic: `pergi`, `bicara`, `dialog`, `beli`, `lakukan`, `baca`, `dengar`, `temukan`. Skor tiga komponen (Hasil 40, Bahasa 40, Mandiri 20), petunjuk tiga tingkat, bintang, "Perbaiki" (ADR-0019 §16.2–§16.3). Isi misi diacak dengan benih (pemain, misi). `GET /pare/missions`, `GET /pare/missions/{id}`, `POST …/start`, `POST …/steps/{n}`, pesan hub `mission_update`.
**DoD:** tes tiap jenis langkah, urutan paksa, lanjut setelah keluar, skor per komponen, pengaruh petunjuk, hadiah sekali, dua pemain mendapat varian berbeda.

## P9-007 — DSL misi dari data perjalanan (M) ✅ (2026-10-04): misi ditulis di `game/src/game/content/missions/` (`dsl.ts` helper + `en0.ts`), diperiksa dan diekspor oleh `bun scripts/missions.ts [--write]` ke `titian-backend-rust/data/pare/missions.json` — **jangan sunting JSON itu langsung**. Pemeriksa menolak: id/tokoh/tempat/zona/barang menu yang tidak ada, tokoh yang belum di peta, jenis langkah yang belum bisa diverifikasi mesin, butir yang tak bisa dijawab, langkah dengar tanpa audio. Selisih terhadap daftar langkah di `journey/en/l0.ts` dicetak sebagai catatan (misi boleh menyesuaikan rencana), bukan galat. Pola Basic (Kenalan, Belanja, Pesan, Rutinitas, Pemandu) belum dijadikan helper tersendiri
DSL `missions` yang memuat butir dan kunci tiap langkah (data `journey/` hanya memuat deskripsi langkah; butir konkret ditulis di sini). Validasi rujukan tokoh, tempat, barang, aplikasi. Pola Basic: Kenalan, Belanja, Pesan & layani, Rutinitas, Pemandu arah.
**DoD:** pemeriksa menolak rujukan yang tidak ada; tiap langkah di `journey/en/l0.ts` punya padanan di DSL.

## P9-008 — Kartu misi, pelacak, rapor (M) ✅ (`MissionModal.tsx`: kartu → jalannya misi → rapor; pelacak HUD; node misi di Jendela Jalur; kejadian `goto`/`talk` dilaporkan game dan dicek server; dimainkan sampai rapor di browser headless, ponsel). Belum: tombol "Latihan dulu", penanda "!" di engine dan minimap, dialog langsung di NPC selain Miss Kate (warga lain belum ada di peta, P9-010) — langkah dialog sementara dijawab dari jendela misi di zona yang benar
Kartu misi (ADR-0019 §16.1) dengan tombol Mulai, Latihan dulu, Nanti; pelacak HUD; rapor misi (§16.4); dialog NPC bergilir memakai komponen soal yang ada; penanda "!", "…", "?" di engine dan minimap (ganti `npcHasTask`).
**DoD:** satu misi dimainkan dari kartu sampai rapor di browser, termasuk ditinggal lalu dilanjutkan.

## P9-009 — Buku Perjalanan (M) ✅ sebagian (2026-10-04): `services/pare_journey.rs` + `GET /pare/journey/{lang}`; `JourneyModal.tsx` (tombol 🧭 / tombol J) dengan halaman Peta (tujuh tahap, hanya Inggris), Level ini (syarat dengan angka server), Misi, Warga. Tes `the_journey_book_counts_…`; dicoba di browser headless. Belum: halaman Bab ini (sementara lewat Jendela Jalur), Rapor enam batang kemampuan, "yang perlu disiapkan", perkiraan sisa waktu, tombol dari Papan Info kamar, gelar/stempel (P9-014)
`GET /pare/journey/{lang}` dan jendela enam halaman (ADR-0019 §16.5): Peta hidup, Level ini (syarat naik level dengan angka), Bab ini, Misi, Warga, Rapor. Tombol 📖 di HUD; juga dari Papan Info kamar.
**DoD:** angka di halaman "Level ini" cocok dengan status di server untuk pemain baru, pemain di tengah bab, dan pemain yang siap Misi Besar.

## P9-010 — Lima misi bab Basic + audio (M) ✅ sebagian: 5 misi bab (`missions.json`), enam warga di peta Kampung Inggris (`ZoneMeta.villagers`, `NpcSpawn.key`), audio en-0 202/202 direkam dan diunggah ke R2 (2026-10-04). Belum: uji main misi 2–5 sampai rapor di browser (hanya misi 1 dan pembukaan misi 5 dengan Anna yang dicoba), langkah "antar ke tempat" (butuh posisi, P9-012), Anna sebagai tokoh pribadi (P9-012), tinjauan penutur asli
Misi bab 1–5 dari `pare-perjalanan/en-0-basic.md`; lima warga inti yang belum ada di peta kampung (Mrs. Hughes, Mr. Smith, Prof. Grey, Lily, Officer Jones) dan Anna ditambahkan; kalimat NPC lewat pipeline audio.
**DoD:** kelima misi selesai dimainkan; cakupan audio 100%.

## P9-011 — Sepuluh misi warga Basic (M) ✅ [diuji penuh di browser 2026-10-04: lihat catatan uji di P9-013] (2026-10-04): `missions/en0-villagers.ts`, id `en-0:villager:<who>`, terbuka kapan saja, hadiah 40 XP + Rp1.200 sekali + `friend:<who>`; bicara dengan warga yang punya misi belum dimainkan membuka kartunya (Game.tsx). Kejadian `laundry` ditambahkan di `pare_life::laundry`. Tes: `villager_side_missions_are_open_any_time_and_pay_once` (delapan misi tanpa kejadian server dimainkan sempurna, plus Tom dengan pembelian dan Mr. Green dengan cucian). Belum: keakraban sebagai angka dan tampilannya (P9-014), "dua misi cukup untuk syarat level" (P9-015), uji main di browser, klip audio baru belum diunggah ke R2. Versi sederhana: tidak ada langkah `temukan`/`waktu`/`ucap` (mesin belum ada); misi Smith, Hughes dan Brown memakai butir pilihan sebagai pengganti
Dari tabel "Misi warga" Basic; keakraban warga.
**DoD:** tiap misi selesai dimainkan; dua misi cukup untuk syarat level.

---

# Pare-9c — Dunia tahap 1 & naik level

## P9-012 [sebagian 2026-10-05: langkah `pergi` dengan `tile` diverifikasi posisi server dan dilaporkan otomatis saat pemain berjalan sampai; misi Turis tersesat memakainya (kafe, taman). Belum: pintu terkunci/adegan, Anna pribadi yang mengikuti] — Pintu terkunci, adegan, tokoh pribadi (M)
Pintu 🔒 dengan alasannya; adegan bangunan (jendela); `pare_unlocks` dipakai engine; tokoh dan benda misi yang hanya terlihat pemiliknya (Anna mengikuti pemain).
**DoD:** dua pemain menjalankan "Turis tersesat" bersamaan, masing-masing hanya melihat Anna miliknya.

## P9-013 — Misi Besar Basic (M) [UJI PENUH 2026-10-04, browser headless: seluruh 16 misi Basic (5 bab, 10 warga, 1 besar) dimainkan sampai rapor dalam satu run, skor 100, naik level ke A1 dan jendela NAIK LEVEL tampil setelah rapor; 62/62 ketukan 🔊 meminta klip rekaman; 11 NPC di peta diuji (E membuka misi, ditawarkan sekali; Anna ada; misi berjalan dilanjutkan); pintu Camp sungguhan menyelesaikan langkah "pergi". Pembelian, laundry, dan kelas dikerjakan lewat API (efek server yang sama), bukan lewat jendela toko] ✅ (2026-10-04): `missions/en0-big.ts` (`en-0:big`, 10 langkah dalam tiga babak: pagi, siang, sore), terkunci sampai kelima misi bab selesai; langkah baru `sosial` (`need` orang berbeda dari daftar `events`, orang yang sama dua kali tidak dihitung; pengganti NPC selalu ada, pemain lain belum dihitung); hadiah 150 XP + Rp5.000 sekali, membuka `title:warga-baru`, `card:kartu-warga`, `region:permukiman` (tanda saja: pintu Permukiman belum ada, P9-012/024). Syarat Misi Besar di Buku Perjalanan sekarang nyata. Tes `the_big_mission_waits_…`. Belum: pintu dan adegan Permukiman, naik level otomatis (P9-015), pesta bersama pemain lain (P9-018), sambutan di taman sebagai peristiwa dunia, 10 klip audio baru belum diunggah ke R2
Tiga babak "Minggu pertamaku di Kampung"; langkah `sosial` pertama (berkenalan dengan pemain atau warga); membuka Permukiman sebagai pintu dan adegan.

## P9-014 — Bintang, stempel, gelar, keakraban, hadiah (M) ✅ (2026-10-04): koleksi (stempel, gelar, kartu, wilayah, teman) di tab 🏅 Stempel Buku Perjalanan (`collection` di `GET /pare/journey`, label di `pare_journey::label`); keakraban 0–7 per warga (satu langkah tiap misi warga selesai) di halaman Warga; gelar hasil Misi Besar di papan nama ("Warga Baru · EN A1", `pare_hub::load_player`, profil disegarkan saat misi selesai). Penalaan hadiah: belanjaan yang diminta misi **diganti penuh** pada penyelesaian pertama (`reward.refund` = `cost`), XP misi bab 120 / warga 60 / besar 300 (dulu 60/40/150) supaya lebih menarik dari kelas biasa. Tes `a_mission_pays_back_…`. Belum: stempel di Papan Info kamar, sapaan dan diskon dari keakraban (ADR §11), bintang di papan nama
Stempel di Buku Perjalanan dan Papan Info; gelar di papan nama; penalaan hadiah misi terhadap kelas dan tantangan.

## P9-015 — Aturan naik level baru (M) ✅ (2026-10-04): level yang punya Misi Besar (kini hanya Basic bahasa Inggris; `pare_mission::has_big`) naik otomatis saat bab lulus + misi bab + misi warga (Basic: 2, lain: 3) + Misi Besar selesai (`pare_journey::try_level_up`, dipanggil saat misi selesai; bayaran Rp1.000 × level baru, sekali) dan aturan otomatis lama (80% kata + poin) dimatikan di level itu (`eco::check_level`). Level tanpa Misi Besar tetap memakai aturan lama sampai jalurnya ditulis. Ujian lompat level tetap jalur cepat. Respons langkah misi memuat `level_up`; Panel Level menampilkan syarat jalur. Tes: `the_big_mission_…` (diperluas), `english_basic_is_not_promoted_…`; dua tes pendakian lama dipindah ke zh / mulai A1. Belum: ujian menandai bab lulus (tidak perlu: level berikutnya punya jalurnya sendiri), pemetaan khusus pemain lama selain bab auto-selesai (pemain di Basic yang dulu hampir naik harus mengerjakan misi)
Semua bab lulus + misi warga secukupnya + Misi Besar (ADR-0019 §16.6); ujian tetap jalur cepat; pemetaan pemain lama. Sesuai §15.2 dan §15.3.

## P9-016 — Pengukuran (S)
Percobaan, ketepatan, waktu, dan titik berhenti per simpul dan langkah; ringkasan untuk menala ambang dan perkiraan waktu di `scripts/journey.ts`.

---

# Pare-9d — Multipemain inti (ADR-0019 §17)

## P9-017 — Kehadiran di NPC (S)
Klien melapor saat membuka dan menutup dialog NPC; hub menyiarkan jumlah per NPC ke kanal (≤ 1 per detik); gelembung "💬 n"; avatar lain diredupkan saat dialog.
**DoD:** uji dengan `scripts/bots.ts`: 50 klien di satu NPC, tidak ada yang tertahan.

## P9-018 — Sesi bersama: ramai (M)
Migrasi `pare_sessions`, `pare_session_members`. `pare_session.rs`: tawaran sesi untuk pemain di langkah yang sama dalam 60 detik; giliran; catatan bersama; keluar tanpa merugikan yang lain. Tombol jawab cepat untuk survei (pemain menggantikan warga; NPC menjawab setelah 30 detik). Pesan hub `session_*`.
**DoD:** tes dua sampai lima pemain; pemain keluar di tengah; skor tiap pemain tidak terpengaruh pemain lain.

## P9-019 — Pencocokan pasangan dan kelompok (L)
Antrean per (bahasa, misi, langkah, peran), lintas kanal dan zona; pengganti NPC setelah 45 detik (pasangan) atau 60 detik (kelompok); tukar peran; kartu peran dan lembar posisi rahasia; blokir dihormati.
**DoD:** tes pencocokan, batas tunggu, pasangan diam 60 detik digantikan NPC, restart hub tidak menghilangkan kemajuan misi.

## P9-020 — Papan antarpemain & moderasi (M)
Migrasi `pare_posts`, `pare_post_marks`. `pare_board.rs`: terbit setelah lulus penilaian dan saringan; baca; tanda berlabel tetap; lapor; tarik; pilihan "sembunyikan tulisanku"; tulisan contoh saat kosong.
**DoD:** tulisan yang tidak lulus atau terkena saringan tidak pernah tampil ke pemain lain (tes).

## P9-021 — Kelas bersama (M)
Sesi per level tiap menit 00 dan 30: delapan butir ulangan, persentase benar kelas, bonus 80%, satu butir teman sebangku; paling banyak 20 per sesi; papan tanya kelas.

## P9-022 — Penjadwal acara dunia (S)
Acara berulang menurut jam WIB atau begitu cukup pemain menunggu; daftar acara di Buku Perjalanan.

---

# Pare-9e — A1 bahasa Inggris

## P9-023 — Bab A1 dan bahan Praktik yang kurang (M)
Penugasan 561 kata ke 14 bab mengikuti anggaran `journey/en/l1.ts`; tambah satu situasi dan satu dialog untuk Bab 9, 12, 13, 14 (lihat "Catatan isi" di `en-1-a1.md`).
## P9-024 — Permukiman (M)
Enam tempat (lima adegan + taman bermain sebagai area), empat tokoh (keluarga Brown, Mr. Patel).
## P9-025 — Komputer: blok formulir, utas, pemesanan (M)
Jendela terminal; aplikasi Formulir, Pesan singkat, Kalender; langkah `komputer(aplikasi)` dan `waktu` (janji relatif).
## P9-026 — Misi A1 (L)
14 misi bab, Misi Besar "Pesta kampung", 10 misi warga; langkah `tulis` memakai penilai menulis yang ada; Simon says sebagai sesi kelompok; pakaian dan kegiatan avatar sebagai kunci jawaban (Bab 9 dan 10); audio.

# Pare-9f — A2 bahasa Inggris
P9-027 bab A2 (1.005 kata, 14 bab; bahan Praktik untuk Bab 13 dan 14) · P9-028 Pusat kota (sembilan tempat, lima tokoh) · P9-029 blok peramban dan penyunting; aplikasi Email, Tiket, Peta, Situs ulasan; langkah `telepon` · P9-030 skor rubrik untuk `tulis` di dalam skor misi; batas penilaian per hari · P9-031 14 misi bab, Misi Besar, 10 misi warga, audio.

# Pare-9g — B1 bahasa Inggris
P9-032 bab B1 (1.399 kata, 14 bab) · P9-033 Distrik media & kampus (tujuh tempat, lima tokoh) · P9-034 blok audio; aplikasi Meja redaksi, Forum, Portal lamaran, Perekam, Obrolan kerja; langkah `presentasi` · P9-035 14 misi bab, Misi Besar "Edisi khusus", 10 misi warga, audio; papan berita.

# Pare-9h — Bahasa lain, Basic → B1
Untuk zh, ja, ko, ar, menurut [`adaptasi-bahasa-lain.md`](../pare-perjalanan/adaptasi-bahasa-lain.md): tulis `journey/<bahasa>.ts` (perluas `scripts/journey.ts` supaya memeriksa semua bahasa), tinjauan penutur asli, misi, audio. Mekanik tambahan: bantuan baca yang dikurangi bertahap; pilih tingkat tutur (ja, ko); antarmuka kanan-ke-kiri (ar).

# Pare-9i, 9j, 9k — B2, C1, C2 bahasa Inggris
Tiap tahap: (1) tulis isi level menurut silabus per bab di `journey/en/l4.ts`, `l5.ts`, `l6.ts` sampai lolos benchmark, lalu pindahkan entri dari `benchmark-plan.ts` ke `benchmark.ts`; (2) audio; (3) wilayah London tingkat 4, 5, 6 (hidupkan `buildTown`); (4) aplikasi baru (B2: Penyunting dokumen, Salindia, Portal kampus; C1: Pangkalan data, Tinjauan dokumen dengan blok tinjauan, Rapat daring; C2: Meja penerjemah, Penyunting naskah); (5) misi. C1 menambah telaah sejawat antarpemain; C2 menambah Balai Mentor dan misi mentor setelah tamat.
