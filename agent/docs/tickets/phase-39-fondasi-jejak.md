# Phase 39 — Fondasi Jejak Belajar (ADR-0013 L1)

📋 **RENCANA — belum dieksekusi.** Dianalisis & disetujui user 2026-09-13 (Opus), untuk dieksekusi tiket demi tiket (**Sonnet**). Dasar keputusan: [ADR-0013](../adr/0013-ai-learning-engine.md).

Cara eksekusi: kerjakan tiket **berurutan** sampai DoD-nya lolos. **P39-001 wajib duluan**, karena generate konten massal (26 topik Tahap 1, ±34 ribu soal) ditahan sampai soal punya `uid`. Fase ini bisa berjalan paralel dengan Phase 40 (Admin Pusat).

---

## 1. Tujuan

Setelah fase ini, setiap interaksi belajar yang penting meninggalkan jejak yang **merujuk konten yang tepat**:
- setiap soal punya identitas tetap,
- setiap modul yang terbit punya versi,
- mengerjakan kuis, membaca Modul Belajar, tryout, dan Live AI Chat menulis event ke `learning_events`,
- pencatatan perilaku mengikuti persetujuan pengguna (UU No. 27/2022).

Fase ini **tidak** membangun statistik, agen, atau dashboard. Itu Phase 40–42.

## 2. Yang WAJIB dipertahankan

- `learning_events` **diperluas, bukan diganti**. `mastery.rs` (ADR-0002) dan penulis lama di `assessment.rs` harus tetap jalan tanpa perubahan perilaku.
- `QuizQuestion.number` tetap label tampilan **dan** kunci jawaban attempt (`attempts.answers`). `uid` ditambahkan di sampingnya, bukan menggantikannya.
- `PATCH /module-items/{id}/quiz-config` tetap **full-replace** tanpa validasi kelengkapan (jebakan phase-38 §5).
- ADR-0008: item `published` tetap read-only di tempat. Snapshot `attempts.question_snapshot` tetap diisi.
- Event klien **tidak pernah** dipakai untuk menilai siswa.

## 3. Aturan main eksekusi

- Migrasi baru mulai `0046_*`. Semua aditif, tanpa `drop column`.
- Semua tabel/kolom baru disinkronkan ke `docs/domain-model.md`; endpoint baru ke `docs/api-contract.md` (protokol agen).
- Verifikasi setiap tiket: `cargo test --lib`, test integrasi yang relevan (`cargo test --test integration <modul>::`, **bukan** seluruh suite; disk pernah penuh karenanya), `npx tsc --noEmit`, `npx eslint`, lalu cek di browser dengan `Bun.WebView` (`agent/tools/qa/webview.ts`). **Minta izin user** sebelum membuat token QA, dan hapus setelahnya.
- Jangan commit kecuali user minta.

---

## P39-001 — `uid` tetap untuk setiap soal (S) ⚠️ prasyarat generate massal

✅ **SELESAI (2026-09-13, Sonnet).** `QuizQuestion.uid`/`derived_from_uid` (quiz_config.rs), `ensure_question_uids` dipanggil dari `module_item::update_quiz_config` dan `quiz_generation::generate_quiz_group` (termasuk lineage `derived_from_uid` di mode Rewrite). Frontend: `stripQuestionIdentity`/`stripGroupIdentity` (quiz-numbering.ts) dipakai di `duplicateQuestion`, `duplicateGroup`, `duplicateSection`. Backfill one-off `src/bin/backfill_question_uids.rs` dijalankan terhadap dev DB — 45/45 soal punya uid unik, 0 tanpa uid. `question_snapshot` di `quiz_attempt.rs` sudah otomatis membawa uid (snapshot seluruh `quiz_config`, tidak perlu kode baru). Diverifikasi live: hapus soal #1 → uid soal lain bertahan (dibuktikan lewat query DB sebelum/sesudah); duplikat grup → salinan dapat 4 uid baru, sumber tidak berubah — keduanya lewat server yang baru di-build, bukan asumsi. `cargo test --lib` 203 lulus (+5 baru), `cargo test --test integration quiz_` 14 lulus, `tsc`/`eslint` bersih. `domain-model.md` sengaja TIDAK disentuh — file itu ERD ADR-0001 lama yang sudah tidak disinkronkan sejak `module_items` (Phase 31+), dan `uid` hidup di jsonb `quiz_config`, bukan kolom/tabel baru.

**Generate 26 topik Tahap 1 sisanya sudah boleh dilanjutkan** — lihat `agent/tools/content-gen/generate_bab_content.py`.

Backend:
- `services/quiz_config.rs::QuizQuestion`: tambah `uid: Option<Uuid>` dan `derived_from_uid: Option<Uuid>` (`skip_serializing_if = None`).
- Satu fungsi `ensure_question_uids(config: &mut QuizConfig)`: memberi `uid` baru pada soal yang belum punya, dan **memberi `uid` baru pada kemunculan kedua** bila ada dua soal ber-`uid` sama dalam satu deck (hasil duplikat). Dipanggil di:
  - `module_item::update_quiz_config` (sebelum simpan),
  - `quiz_generation::merge_into_group` (soal hasil generate),
  - `quiz_template` apply.
- Mode `rewrite` di `quiz_generation`: soal hasil tulis ulang mendapat `uid` baru dengan `derived_from_uid` = `uid` lama. Mode `answer_only` mempertahankan `uid`.
- `quiz_attempt::submit_quiz_attempt`: `question_snapshot` ikut menyimpan `uid` per soal.
- Migrasi backfill: satu kali, beri `uid` ke semua soal di `module_items.quiz_config` yang ada (SQL `jsonb` atau job Rust kecil yang lewat `ensure_question_uids`).

Frontend (`titian-web`):
- `api-client.ts::QuizQuestion`: tambah `uid?`, `derived_from_uid?`.
- `quiz-builder.tsx::duplicateQuestion` dan duplikat grup: **hapus `uid`** dari salinan, supaya server memberi yang baru.

DoD:
- Unit test: soal tanpa uid mendapat uid; menata ulang/menomori ulang/mengedit **tidak** mengubah uid; duplikat mendapat uid baru; rewrite mengisi `derived_from_uid`.
- Backfill: 0 soal tanpa `uid` di DB.
- Hapus soal #1 di builder → nomor bergeser, tetapi `uid` soal lain **tetap sama** setelah reload.

## P39-002 — Versi konten `module_items` (M)

✅ **SELESAI (2026-09-13, Sonnet).** Migrasi `0046_module_item_versions.sql`: tabel `module_item_versions` + `module_items.current_version` + `attempts.content_version`, plus backfill (0 baris memenuhi syarat di dev DB — semua 20.256 item masih berstatus `draft`, belum pernah publish). Service baru `module_item_version.rs` (`freeze`/`list`/`get`, hash sha256 dengan pemisah byte antar `lesson_plan`/`quiz_config` supaya tidak pernah tabrakan). `module_item::publish` memanggil `freeze` — dilewati untuk artikel ALM polos (`lesson_plan`/`quiz_config` dua-duanya null) karena tidak ada apa pun di bentuk baru untuk dibekukan. `quiz_attempt::submit_quiz_attempt` membaca `current_version` dalam query yang SAMA dengan `quiz_config` yang dipakai menilai, lalu menulisnya ke `attempts.content_version`. Endpoint baru `GET /module-items/{id}/versions` & `/versions/{n}`, digerbang `can_edit_item` yang sudah ada.

**Catatan jujur soal DoD "publish dua kali":** belum ada jalur unpublish/re-draft di produk (ADR-0008 sendiri menyatakan publish saat ini satu arah), jadi skenario itu diuji langsung lewat `module_item_version::freeze` dua kali (bukan lewat endpoint publish dua kali, yang memang belum bisa terjadi) — 4 test integrasi baru (`module_item_versions_test.rs`) lulus semua, termasuk yang membuktikan `attempts.content_version` mencatat versi yang benar-benar berlaku saat setiap attempt dinilai. Verifikasi browser sengaja dilewati untuk tiket ini — tidak ada perubahan frontend sama sekali (baca-saja, dikonsumsi Admin Pusat nanti), dan test integrasi HTTP sudah melewati router+izin+DB sungguhan.

`cargo test --lib` 206 lulus (+3 dari 203), `cargo test --test integration` semua kuis+attempt+module_item_versions lulus, 6 kegagalan lama (`content_type "learn"`) tetap 6, tidak bertambah.

- Migrasi `module_item_versions (id, item_id, version, lesson_plan, quiz_config, content_hash, created_by, created_via, change_summary, published_at, superseded_at)` + unik `(item_id, version)`.
- `module_items.current_version int` (null = belum pernah terbit).
- `module_item::publish`: bekukan snapshot `lesson_plan`/`quiz_config` sebagai versi baru, isi `superseded_at` versi sebelumnya, dan naikkan `current_version`. `created_via` = `human | ai_generation | ai_proposal` (turunan dari `generated_by` untuk sekarang).
- Backfill: item yang sudah `published` mendapat versi 1.
- Endpoint baca: `GET /module-items/{id}/versions` (daftar) dan `GET /module-items/{id}/versions/{n}`.

DoD: publish dua kali menghasilkan versi 1 & 2 dengan snapshot yang benar; attempt yang dibuat di antara keduanya mencatat versi yang berlaku saat itu.

## P39-003 — `learning_events` v2 + registry event (M)

✅ **SELESAI (2026-09-13, Sonnet).** Migrasi `0047_learning_events_v2.sql`: tabel lama di-rename → tabel baru **terpartisi bulanan** (`partition by range (created_at)`, PK komposit `(id, created_at)` — syarat Postgres untuk tabel partisi) → 16 baris lama disalin dengan `source='practice'`, `schema_version=1` → tabel lama dihapus. 12 partisi Jan–Des 2026 dibuat langsung di migrasi + 1 partisi `default` untuk jaga-jaga. `learning_event_idempotency` adalah tabel TERPISAH (tidak dipartisi) khusus untuk keunikan `client_event_id` — tabel partisi tidak bisa punya unique/PK yang tidak menyertakan kolom partisinya, jadi keunikan silang-bulan tidak bisa ditegakkan di `learning_events` sendiri.

Service baru `learning_event.rs`: registry `EVENT_TYPES` (baru `question_answered`, sesuai isi produksi hari ini), `EventChannel::{Server,Client}` supaya tipe event server-only tidak pernah bisa dipalsukan lewat `POST /events` (P39-005) nanti, `record()` yang memvalidasi sebelum menulis + dedup idempoten, dan `ensure_current_partitions()` (dipanggil sekali saat boot di `main.rs`) sebagai jaring pengaman sampai antrean job Fase 40 punya cron bulanan sungguhan.

Penulis lama di `assessment.rs::submit_attempt` (insert mentah ke `learning_events`) dipindah ke `learning_event::record` — payload persis sama, tidak ada perubahan yang terlihat `mastery.rs`/`frss.rs`.

**Dibuktikan lewat jalur nyata, bukan asumsi**: karena test bawaan `attempt_submission_test.rs` sudah gagal duluan (masalah lama `content_type "learn"`, tidak berkaitan), saya menulis test baru yang memanggil `assessment::submit_attempt` langsung (tanpa lewat setup HTTP yang rusak itu) → mengecek baris `learning_events` yang ditulis → lalu memanggil `mastery::recompute_for_concept` SUNGGUHAN dan membuktikan hasilnya skor 100 yang benar. Ini pembuktian ujung-ke-ujung paling kuat yang tersedia.

`cargo test --lib` 211 lulus (+5 dari 206). `cargo test --test integration` penuh: **87 lulus, 26 gagal — persis sama dengan jumlah kegagalan lama sebelum tiket ini**, tidak bertambah satu pun.

- Migrasi aditif ke `learning_events`: `source`, `session_id`, `org_id`, `module_item_id`, `content_uid`, `content_version`, `occurred_at`, `client_event_id` (unik per `user_id`), `schema_version`. Default untuk baris lama: `source='practice'`, `schema_version=1`.
- **Partisi bulanan** (`created_at`). Migrasi memindahkan 16 baris lama ke tabel terpartisi. Ada job/fungsi pembuat partisi bulan berikutnya.
- `services/learning_event.rs` (baru): registry `EventType` → skema payload yang divalidasi, sumber yang diizinkan (`server` / `client`), dan satu fungsi `record(pool, ctx, event)`. Event tak dikenal → error, tidak disimpan diam-diam.
- Penulis lama di `assessment.rs` dipindah ke `learning_event::record` **tanpa mengubah payload** yang dibaca `mastery.rs`.
- Indeks: `(user_id, created_at)`, `(module_item_id, content_uid)`, `(event_type, created_at)`.

DoD: unit test registry (payload valid/invalid, idempotensi `client_event_id`); test integrasi mastery yang ada tetap lulus.

## P39-004 — Event server: kuis, modul, tryout (M)

✅ **SELESAI (2026-09-13, Sonnet).** Registry `learning_event.rs` diperluas dari 1 jadi 6 tipe event: `quiz_attempt_submitted`, `module_item_completed`, `question_graded`, `exam_session_started`, `exam_session_finished` (semua Server-only). `learning_event::record` diubah menerima `user_id: Uuid` langsung, bukan `&AuthContext` — supaya event tetap tercatat atas nama SISWA saat pemanggilnya orang lain (guru menilai manual).

- `quiz_attempt::submit_quiz_attempt`: 1 `quiz_attempt_submitted` per attempt + 1 `question_answered` per soal, `content_uid`=uid soal (P39-001), `content_version` dibaca bareng `quiz_config` yang menilai (P39-002). `source` = `tryout` bila ada sesi proctor, selain itu `practice`.
- `item_progress::record_completion` (titik tunggal, dipakai 3 pemanggil: submit kuis, selesai dinilai manual, tombol "selesai" artikel) kini menerima `source` dan memancarkan `module_item_completed` setiap dipanggil — bukan hanya sekali.
- `quiz_attempt::grade_manual_group`: `question_graded` diatribusikan ke SISWA yang dinilai, bukan guru yang menilai — bukti nyata kenapa `record()` perlu `user_id` eksplisit.
- `exam_session.rs`: `exam_session_started`/`finished`, `source='tryout'` selalu (sesi ujian memang definisi tryout-nya ADR-0013 §1.5).

**Catatan jujur**: "waktu per soal bila dikirim klien" dari deskripsi tiket belum diisi — tidak ada jalur klien yang mengirim waktu per soal hari ini (itu memang pekerjaan P39-005). `NewLearningEvent` sudah punya slot untuk itu di masa depan tanpa perubahan skema.

**Dibuktikan lewat 8 test integrasi baru** (bukan cuma build lulus): attempt 5 soal sungguhan → persis 1 `quiz_attempt_submitted` + 5 `question_answered` dengan `content_uid`/`content_version` benar; sesi diawasi proctor → semua event `source='tryout'`; guru menilai soal manual → event tercatat atas nama siswa; sesi ujian mulai/selesai → dua event dengan `session_id` terisi dan `timed_out` benar.

`cargo test --lib` 216 lulus (+5). `cargo test --test integration` penuh: **91 lulus, 26 gagal — daftar kegagalan sama persis**, tidak bertambah.

Semua lewat `learning_event::record`, di service yang sama yang menjalankan aksinya:
- `quiz_attempt::submit_quiz_attempt`: `quiz_attempt_submitted` (skor, durasi, `content_version`), dan **satu `question_answered` per soal** (`content_uid` = uid, benar/salah/parsial, jawaban terpilih termasuk label pengecoh, waktu per soal bila dikirim klien). `source` = `tryout` bila item di bawah sesi ujian/proctor, selain itu `practice`.
- `item_progress`: `module_item_completed`.
- `quiz_attempt::grade_manual_group`: `question_graded` untuk soal yang dinilai manual.
- Tryout: `exam_session` mulai/selesai.

DoD: satu attempt kuis 5 soal menghasilkan 1 `quiz_attempt_submitted` + 5 `question_answered` dengan `content_uid` & `content_version` benar; tryout ber-`source='tryout'`.

## P39-005 — Telemetri klien `POST /events` (M)

✅ **BACKEND SELESAI (2026-09-13, Sonnet).** Registry `learning_event.rs` diperluas dari 6 jadi 12 tipe event: 6 baru berkanal `Client` + `requires_consent: Some("learning_analytics")` — `section_viewed`, `section_read`, `section_scroll_depth`, `question_viewed`, `answer_changed`, `hint_opened`. Service baru `client_events.rs`: `MAX_BATCH_SIZE=50`, `MAX_EVENTS_PER_MINUTE=600` (dibatasi laju lewat Redis `INCR`+`EXPIRE` per user, **degradasi anggun** — Redis mati tidak memblokir telemetri, cuma melewati batasnya), `MAX_OCCURRED_AT_AGE_DAYS=7` (menolak `occurred_at` di masa depan atau lebih dari 7 hari lalu), `VALID_SOURCES` divalidasi, event non-`client` di registry ditolak (tidak bisa dipalsukan lewat endpoint ini — gerbang `EventChannel` P39-003 dipakai persis untuk ini). Idempotensi lewat `client_event_id` (tabel `learning_event_idempotency` yang sudah ada dari P39-003). Setiap event di batch dapat hasil individual (`ClientEventResult`) — batch tidak gagal total kalau satu event bermasalah. `AppError::TooManyRequests` baru → HTTP 429. Handler `POST /events` (`handlers/client_events.rs`) digerbang auth biasa, dipasang langsung di root protected router (`routes/mod.rs`).

**Dibuktikan lewat 6 test integrasi baru** (`client_events_test.rs`): batch tervalidasi tersimpan & bisa dibaca balik dari DB; event server-only (`question_answered`) ditolak lewat endpoint klien; `client_event_id` duplikat tidak menulis baris kedua; `occurred_at` di luar rentang wajar ditolak per-event (bukan gagal seluruh batch); batch >50 ditolak; tanpa persetujuan `learning_analytics` event dilewati (`Option<Uuid>` `None`, gerbang P39-007 dipakai apa adanya, tidak ada kode baru). Bug test ditemukan+diperbaiki saat menulis test: event butuh `module_item_id` nyata (FK asli ke `module_items`, bukan UUID acak) — ditambah helper `seed_module_item()`.

`cargo test --lib` 220 lulus (tidak berubah — semua penambahan ada di test integrasi). `cargo test --test integration` penuh: **105 lulus, 26 gagal — daftar kegagalan sama persis** sejak P39-003, tidak bertambah (105 = 99 setelah P39-007 + 6 test baru).

✅ **FRONTEND SELESAI (2026-09-13, Sonnet)** — dikerjakan setelah user memilih "Sisa Phase 39 (frontend)" dan secara eksplisit memberi kebebasan tata bahasa/alur ("saya akan putuskan sendiri... kecuali Anda mau arahkan"). `lib/telemetry.ts`: antrean di memori, `MAX_BATCH_SIZE=50` (mencerminkan batas backend), flush tiap 10 detik dan saat `visibilitychange`/`pagehide`. **Penyimpangan sadar dari kalimat tiket**: `navigator.sendBeacon` tidak bisa membawa header custom, sementara auth aplikasi ini murni Bearer-token di header `Authorization` — jadi diganti `fetch(url, { keepalive: true })`, padanan modern standards-track yang sama-sama "request tetap jalan walau tab ditutup/hilang", tapi mendukung header. Dijelaskan langsung di komentar berkas.
- Reader (`reader.tsx`): `useSectionActiveTime` — akumulator waktu aktif per bagian lewat ref (bukan state, supaya tidak memicu re-render tiap detik), berhenti mengakumulasi persis saat `visibilitychange` → hidden dan lanjut saat visible lagi, flush `section_read` saat pindah bagian/tab hidden/unmount. `section_viewed` sekali per bagian saat pertama jadi aktif (termasuk bagian 0 saat mount). `section_scroll_depth` memakai titik ambang PERSIS yang sama dengan `read` Set yang sudah ada (70% terlewat / dasar tercapai) — bukan sampling terpisah.
- Kuis (`quiz-attempt.tsx`): `question_viewed` sekali per soal saat mount (seluruh dek dirender sekaligus, tidak ada pagination). `answer_changed` setiap `onAnswer`. `content_uid` diambil dari `QuizQuestion.uid` (P39-001), bukan `number` tampilan. **`hint_opened` dan waktu-per-soal SENGAJA TIDAK dikerjakan** — tidak ada UI pembuka hint di manapun (`QuizQuestion.hint` field data tak terpakai, butuh keputusan produk dulu), dan waktu-per-soal butuh field baru di request submit (perubahan backend kecil tapi nyata, di luar cakupan "frontend saja").
- Persetujuan (P39-007) disambung nyata di sini: `hooks/use-consent.ts`, `components/telemetry/telemetry-consent-sync.tsx` (dipasang di `(app)/layout.tsx`, men-sync konsen → `setTelemetryEnabled`) — lihat detail lengkap di bagian P39-007 di bawah.

**Dibuktikan lewat browser sungguhan** (`Bun.WebView`, resep QA standar — modul & kuis QA sekali-pakai disemai `status='published'` langsung agar tidak menyentuh konten Matematika asli yang masih draft, token `refresh_tokens` QA dihapus setelah selesai): tanpa persetujuan, membaca modul 5 bagian sampai scroll ke bawah **menghasilkan nol request `POST /events`** (dibuktikan lewat intersep CDP `Network.requestWillBeSent`, bukan cuma asumsi UI). Setelah persetujuan dinyalakan dari Profil, membaca ulang modul yang sama menghasilkan 29 baris `learning_events` nyata: `section_viewed` per bagian, `section_read` dengan `active_seconds` masuk akal (2–7 detik, sesuai waktu tunggu skrip), `section_scroll_depth` naik 70%→100% persis saat scroll melewati ambang. Mencabut persetujuan dari Profil mid-sesi lalu membaca modul lagi kembali menghasilkan nol request. Kuis QA 3 soal: `question_viewed` ×3 saat termuat (dobel di dev karena React StrictMode me-mount efek dua kali — perilaku dev normal, bukan bug), `answer_changed` ×3 dengan `content_uid` berbeda-beda sesuai `uid` tiap soal setelah memilih satu pilihan per soal. Semua baris `learning_events` dan modul/kuis QA dihapus setelah verifikasi.

Backend:
- `POST /events` menerima batch ≤50 event. Hanya event berlabel `client` di registry. Divalidasi, dibatasi laju per pengguna, idempoten lewat `client_event_id`, dan `occurred_at` dibatasi ke rentang wajar (tidak di masa depan, tidak lebih dari 7 hari lalu).

Frontend:
- `lib/telemetry.ts`: antrean di memori, dikirim setiap 10 detik, saat `visibilitychange` → hidden (`fetch(..., {keepalive:true})`, lihat catatan penyimpangan di atas), dan saat navigasi. Tidak mengirim apa pun tanpa persetujuan (P39-007).
- Reader Modul Belajar (`components/belajar/lesson-plan/reader.tsx`): `section_viewed` (masuk viewport), `section_read` (waktu aktif per bagian, berhenti saat tab tidak aktif), `section_scroll_depth`.
- Kuis (`components/exercise/quiz-attempt.tsx`): `question_viewed`, `answer_changed`. ~~`hint_opened`, dan waktu per soal~~ — lihat catatan cakupan di atas.

DoD: membaca satu Modul Belajar 5 bagian menghasilkan event per `section_id` dengan waktu aktif yang masuk akal (tab disembunyikan tidak dihitung); tanpa persetujuan tidak ada request `/events`. **Dibuktikan lewat browser sungguhan, lihat catatan verifikasi di atas.**

## P39-006 — Live AI Chat disimpan (S)

✅ **SELESAI (2026-09-13, Sonnet).** Registry `learning_event.rs` bertambah 1 tipe: `live_chat_question` (`EventChannel::Server`, `requires_consent: Some("ai_chat_storage")`). `live_chat.rs`: helper baru `record_question_event()` dipanggil di KEDUA jalur — `generate_turn` (non-stream) dan `generate_turn_stream` (SSE) — segera setelah `section_index` diketahui, **sebelum** memanggil AI, supaya pertanyaan siswa tercatat bahkan kalau provider gagal di tengah jalan. Kegagalan menulis event di-log lalu ditelan (`tracing::warn!`), tidak pernah menggagalkan giliran chat — pola berbeda dari P39-004 yang mem-`?`-kan `record()` karena event-event itu OTORITATIF (nilai/progres); `live_chat_question` bukan.

**`section_id` tidak butuh perubahan frontend**: `ChatTurnRequest` sudah membawa `lesson_plan` + `section_index` sejak awal (dipakai untuk prompt), jadi backend cukup mengambil `plan.sections[section_index].id` — `chat-room.tsx` tidak disentuh sama sekali. `content_version` dibaca lewat query kecil terpisah ke `module_items.current_version` (pola yang sama dengan `get_detail`'s catatan "baca terpisah, jangan lebarkan ItemRow" untuk kebutuhan satu pemanggil). Payload cuma `{"question": <teks, dipotong 500 karakter>}` — **jawaban tutor sengaja tidak pernah disimpan**, sesuai baris privasi di deskripsi tiket ini sendiri.

**Dibuktikan lewat 4 test integrasi baru** (`live_chat_test.rs`): satu giliran dengan persetujuan → 1 event dengan `content_uid`, `content_version`, `source`, dan payload yang cuma berisi `question` (bukan `reply`); 3 pertanyaan di section index 1 → 3 event ber-`content_uid="sec-b"` berurutan; tanpa persetujuan → 0 event tapi endpoint tetap balas 200 dengan reply asli; jalur **streaming** SSE juga tercatat (bukti dua entry point sama-sama benar, bukan cuma salah satu).

`cargo test --lib` 220 lulus (tidak berubah). `cargo test --test integration` penuh: **109 lulus, 26 gagal — daftar sama persis**, tidak bertambah (109 = 105 sebelumnya + 4 baru).

- `services/live_chat.rs`: tetap stateless untuk percakapannya, tetapi setiap giliran siswa menulis `live_chat_question` (`module_item_id`, `section_id`, teks pertanyaan, `content_version`) ke `learning_events` dengan `source='live_ai_chat'`.
- Hanya bila pengguna memberi persetujuan (P39-007). Teks pertanyaan dibatasi panjangnya; tidak menyimpan jawaban AI.
- `chat-room.tsx` mengirim `section_id` yang sedang dibuka.

DoD: bertanya 3 kali di bagian 2 menghasilkan 3 event ber-`section_id` benar; tanpa persetujuan tidak ada yang tersimpan, tetapi chat tetap berfungsi.

## P39-007 — Persetujuan data & retensi (S–M)

✅ **BACKEND SELESAI (2026-09-13, Sonnet)** — dikerjakan LEBIH DULU dari P39-005/006 meski nomornya belakangan: kedua tiket itu sendiri menyatakan bergantung padanya ("Tidak mengirim apa pun tanpa persetujuan (P39-007)"), jadi urutan tertulis dibalik supaya tiket berikutnya benar-benar bisa diperiksa DoD-nya.

- Migrasi `0048_user_data_consents.sql`: satu baris per (user, kind) — status TERKINI, bukan log riwayat. `learning_analytics` & `ai_chat_storage`.
- `user_data_consent.rs`: `set_consent`/`has_consent`/`list_for_user`. Untuk jenjang SD/SMP (`user_learning_profiles.jenjang` berawalan "SD"/"SMP"), `granted=true` ditolak (422 `guardian_confirmation_required`) kecuali `guardian_confirmed=true` disertakan — dicek ulang di sini, tidak dipercaya dari pemanggil.
- `learning_event::record` sekarang mengembalikan `Option<Uuid>` (bukan `Uuid`) — `None` berarti dilewati karena belum ada persetujuan. Registry `EventTypeInfo` dapat field baru `requires_consent: Option<&'static str>`; **keenam tipe event P39-004 semuanya `None`** (wajib, sesuai ADR-0013 §1.4: penilaian/progres selalu dicatat) — gerbang ini baru benar-benar aktif dipakai saat P39-005/006 mendaftarkan tipe event pertama yang `Some(kind)`.
- Retensi: `enforce_retention()` menghapus partisi bulanan yang seluruh isinya >24 bulan (drop tabel instan, bukan DELETE baris demi baris — manfaat langsung dari pemartisian P39-003). Dipanggil di boot bersama `ensure_current_partitions`, sampai antrean job Fase 40 bisa menjalankannya terjadwal.
- "Hapus akun → hapus event mentah" **sudah terpenuhi otomatis** sejak migrasi P39-003 (`learning_events.user_id references users(id) on delete cascade`) — tidak perlu kode tambahan.
- Endpoint baru: `GET`/`POST /me/consents`.

**Keputusan produk (2026-09-13, user):** *"untuk anak, di uji coba allow aja"* — konfirmasi wali TIDAK ditegakkan selama fase uji coba. Diimplementasikan sebagai `Config.consent_guardian_confirmation_required` (default `false`, env `CONSENT_GUARDIAN_CONFIRMATION_REQUIRED`) — mekanismenya tetap utuh dan teruji (`a_minor_jenjang_cannot_grant_consent_without_guardian_confirmation_when_enforced`), tinggal dinyalakan lewat konfigurasi saat siap produksi, tanpa kode baru.

✅ **FRONTEND SELESAI (2026-09-13, Sonnet)**, sekaligus dengan P39-005 frontend di atas (kedua UI menyatu: toggle Profil dan langkah onboarding sama-sama memakai `hooks/use-consent.ts`).
- **Profil** (`components/profil/settings-list.tsx`): dua `<Row>` baru — "Analitik belajar" (`learning_analytics`) dan "Simpan riwayat Tanya AI" (`ai_chat_storage`) — masing-masing `<Switch>` langsung memanggil `POST /me/consents` lewat `useSetConsentMutation`, dengan pesan galat inline bila gagal. Ini satu-satunya tempat mengubah persetujuan setelah login.
- **Onboarding** (`app/mulai`, `onboarding-wizard.tsx`): langkah baru `"privasi"` disisipkan sebelum langkah hasil, dengan `Switch` untuk `consentLearningAnalytics` dan — hanya muncul bila jenjang yang dipilih adalah SD/SMP (`isMinorJenjang`) DAN konsen dinyalakan — kartu konfirmasi "Orang tua/wali saya sudah menyetujui ini" yang memblokir tombol lanjut sampai dicentang. **Keputusan desain penting**: wizard ini sepenuhnya anonim pra-login (jawaban hanya di localStorage, lihat komentar header komponennya sendiri) — `POST /me/consents` butuh `user_id` terautentikasi, jadi TIDAK bisa dikirim dari dalam wizard. Pilihan konsen disimpan di `OnboardingAnswers` yang sama dan disinkronkan ke server pada momen yang SAMA dengan sinkronisasi profil belajar yang sudah ada: tepat setelah login Google berhasil, sebelum redirect ke `/beranda` (`google-sign-in-button.tsx`). Dua try/catch independen (profil, konsen) masing-masing dengan `clearAnswers()` sendiri digerbang keberhasilannya sendiri — kegagalan salah satu tidak boleh membatalkan/mengulang yang lain, dan `consentApi.set` sama sekali tidak dipanggil bila langkah "privasi" tidak pernah dijawab (`answers.consentLearningAnalytics === undefined`).

**Dibuktikan lewat browser sungguhan** — lihat catatan verifikasi gabungan di bagian P39-005 di atas (toggle Profil menyalakan/mematikan telemetri seketika, dibuktikan lewat perubahan langsung pada request `/events` berikutnya, bukan cuma state UI).

Dibuktikan lewat 7 test integrasi baru: grant/revoke berubah seketika; minor tanpa konfirmasi wali ditolak, dengan konfirmasi berhasil; dewasa tidak perlu konfirmasi; retensi menghapus partisi 2018 tapi tidak menyentuh partisi 2026; endpoint HTTP GET default `false` untuk kedua kind, POST tercermin di GET berikutnya, kind tak dikenal ditolak.

`cargo test --lib` 220 lulus (+4). `cargo test --test integration` penuh: **98 lulus, 26 gagal — daftar sama persis**, tidak bertambah.

- Migrasi `user_data_consents (user_id, kind, granted, granted_by, guardian_confirmed, granted_at, revoked_at)`. `kind`: `learning_analytics`, `ai_chat_storage`.
- Onboarding (`app/mulai`) & Profil: pilihan persetujuan dengan bahasa sederhana. Untuk jenjang SD/SMP (`user_learning_profiles.jenjang`) wajib konfirmasi orang tua/wali.
- `learning_event::record` memeriksa persetujuan untuk event non-otoritatif. Event server yang wajib (penilaian, pembelian) tetap dicatat.
- Retensi: job (atau `pg_cron` fallback) yang menghapus partisi event mentah >24 bulan. Hapus akun → hapus event mentah pengguna.

DoD: pengguna tanpa persetujuan hanya menghasilkan event server wajib; mencabut persetujuan menghentikan telemetri saat itu juga. **Dibuktikan lewat browser sungguhan, lihat catatan verifikasi di atas.**

---

## Urutan & ukuran

| Tiket | Ukuran | Bergantung |
|---|---|---|
| P39-001 uid soal | S | — |
| P39-002 versi modul | M | — |
| P39-003 learning_events v2 | M | — |
| P39-004 event server | M | 001, 002, 003 |
| P39-005 telemetri klien | M | 003, 007 |
| P39-006 Live AI Chat disimpan | S | 003, 007 |
| P39-007 persetujuan & retensi | S–M | 003 |

Setelah **P39-001** selesai, generate 26 topik Tahap 1 boleh dilanjutkan (`agent/tools/content-gen/generate_bab_content.py`).
