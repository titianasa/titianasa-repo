# Phase 2 — Content Engine & Curriculum Pipeline
Target: 6–10 minggu (lebih panjang dari Phase 1 — ini fase paling padat keputusan arsitektur di seluruh roadmap). Depends on: Phase 1 checkpoint terpenuhi penuh (lihat `docs/tickets/phase-1.md` — **terverifikasi ulang 2026-08-23, semua 13 ticket + 5 checkpoint done, 79 test lulus, working tree bersih di 3 repo**).

Sumber utama breakdown ini: `agent/ALR_Phase_Detail_Breakdown.md` bagian "PHASE 2" (2.0–2.15, sudah berisi spesifikasi konkret — format ALM, contoh JSON, urutan MVP-first). Ticket di bawah adalah konversi bagian itu jadi format ticket lengkap sesuai `ai-agent-protocol.md`. **ADR yang sudah Accepted selalu menang** kalau ada angka yang beda dari draft `lms_full.md`.

---

## Keputusan yang WAJIB diambil sebelum/selama Phase 2 (baca duluan)

Ditemukan saat re-audit dokumentasi penuh (2026-08-23), sebelum ticket pertama Phase 2 ditulis:

1. **Concept hierarchy — schema saat ini FLAT, Phase 3 butuh hierarki "sejak Phase 2"** (`ALR_Phase_Detail_Breakdown.md` 3.1: drill-down `Grammar → Present Simple → Questions → Do/Does`). Tabel `concepts` di `domain-model.md` cuma punya `(id, subject_id, code, name, type)` — tidak ada `parent_concept_id`. `concept_prerequisites` yang sudah ada itu edge "harus tahu X dulu sebelum Y" (prerequisite graph), **bukan** hierarki containment "sub-concept dari". Kalau Phase 2 mulai bikin banyak concept dalam bentuk flat lalu Phase 3 baru sadar butuh hierarki, itu migration + reklasifikasi ratusan row — jauh lebih mahal daripada menambah 1 kolom nullable sekarang. → **P2-001**.
2. **Content versioning — butuh ADR baru sebelum publish flow dieksekusi** (`ALR_Phase_Detail_Breakdown.md` 2.15, eksplisit ditulis "jangan diputuskan diam-diam di kode"): `lessons.version`/`questions.version` sudah ada di kolom, tapi aturan snapshot attempt vs versi lesson/question saat sudah `submitted`/`evaluated` belum didefinisikan. → **P2-002**.
3. **P1-004b (publish flow question) yang dulu ditunda di Phase 1 kini WAJIB masuk Phase 2** — `docs/tickets/phase-1.md` P1-004 mencatat alur draft→in_review→published belum dikerjakan. Kolom `status` di `questions` DAN `lessons` sama-sama sudah punya CHECK constraint yang benar (`draft/in_review/published/archived`), jadi ini murni kerjaan application-layer (service+handler+permission), tidak butuh migration baru. Digabung jadi 1 ticket generik untuk kedua entity (bukan 2 ticket terpisah) karena state machine-nya identik. → **P2-005**.
4. **Asset upload saat ini proxy lewat Rust API (P1-010), tapi 2.14 eksplisit bilang "jangan proxy file besar lewat Rust API — presigned URL langsung dari client ke R2"** — P1-010 valid untuk file kecil (smoke-test-nya cuma beberapa KB), tapi Phase 2 akan mulai upload audio/video lesson yang lebih besar. Bukan bug P1-010 (kontraknya memang minta backend generate signed URL, dan itu sudah benar untuk kasus kecil), tapi perlu jalur tambahan (bukan ganti yang lama) untuk upload besar. → **P2-010**.
5. **Bobot Level Assessment (Knowledge 40%/Communication 60% vs 7-skill rata) butuh ADR sebelum Phase 5**, dicatat di sini supaya tidak lupa — TIDAK memblokir Phase 2 (itu domain Phase 5 Assessment Engine), tapi kalau Phase 2 mulai attach metadata `weight` per concept/skill ke content, sebaiknya sadar keputusan ini masih terbuka.

**Poin 1 dan 2 adalah blocker beneran untuk P2-001/P2-002 — keduanya di urutan pertama secara sengaja.** Poin 3 dan 4 tidak memblokir ticket lain untuk *mulai*, tapi harus selesai sebelum ticket yang depends on state publish/asset besar (P2-006 dst, P2-015).

**Update 2026-08-23: poin 1, 2, dan 3 selesai** (ADR-0007/0008 Accepted, P2-005 publish flow done — lihat detail masing-masing ticket di bawah). Poin 4 (presigned direct upload, P2-010) dan poin 5 (bobot Level Assessment, belum ada ticket — domain Phase 5) masih terbuka.

**Temuan tambahan 2026-08-23 (sesi 3, P2-006):** contoh ALM di `ALR_Phase_Detail_Breakdown.md` 2.1 sendiri **kontradiktif** — contoh kode menunjukkan `:::question id="q_123" type="multiple_choice" ...:::` dengan isi soal ditulis penuh inline, padahal 2 paragraf di bawahnya dokumen yang sama eksplisit bilang "question **tidak** ditulis penuh di dalam ALM... embed question q_123". `alm_parser.rs` mengikuti aturan tertulis (by-reference only, `:::question_embed\nquestion_id: <uuid>\n:::`), bukan contoh kode yang kontradiktif — dicatat di sini + komentar kode supaya sesi berikutnya (atau user) tidak bingung kalau menemukan ketidaksesuaian ini sendiri.

---

## Reorganisasi dari breakdown asli

`ALR_Phase_Detail_Breakdown.md` 2.15 memberi urutan MVP-first: *2.7 → 2.4 → 2.1+2.3 → 2.14 → 2.9 → 2.13+AI pipeline → 2.6 → 2.10 → 2.15*. Beberapa dari itu **sudah selesai duluan di Phase 1** karena checkpoint Phase 1 butuh assessment/asset/mastery yang saling terhubung:
- **2.4 (question type MVP: MCQ + fill-blank)** — sudah jalan penuh sejak P1-004 (`service/question_schema.rs`). Yang **belum**: pola *registry* extensible (2.4 eksplisit minta `question_type` bukan enum mati) dan publish flow-nya (lihat poin 3 di atas). → jadi **P2-004** (refactor ke registry) bukan ticket "buat MCQ dari nol".
- **2.14 (asset upload)** — sudah jalan sejak P1-010, tapi model proxy bukan presigned-direct (lihat poin 4). → **P2-010** jadi ticket tambahan (direct upload), bukan pengganti.
- **2.15 (versioning)** — dipindah ke urutan **pertama** (bukan terakhir seperti breakdown asli) karena publish flow (P2-005) butuh aturan ini dulu supaya tidak "diputuskan diam-diam di kode" seperti larangan eksplisit di dokumen sumber.

Urutan final ticket di bawah: **schema/ADR dulu → block & question infra → authoring pipeline (ALM/normalizer/API) → media & pattern → AI generation pipeline → OCR → validasi 1 modul penuh → test suite**.

---

### P2-001 — ADR-0007: Concept Hierarchy
**Status:** done
**Depends on:** -
**Deskripsi:** Tambah dukungan hierarki concept (containment, bukan prerequisite) supaya drill-down granular ala `ALR_Phase_Detail_Breakdown.md` 3.1 (`Grammar → Present Simple → Questions → Do/Does`) bisa dipakai mulai Phase 2, tidak menunggu Phase 3 lalu migration ulang ratusan row.
**Acceptance Criteria:**
- [x] ADR baru (`docs/adr/0007-concept-hierarchy.md`) menjelaskan keputusan: kolom `parent_concept_id UUID NULL REFERENCES concepts(id)` ditambah ke `concepts` (additive, tidak mengubah kolom yang sudah ada) — bedakan eksplisit dari `concept_prerequisites` (itu tetap dipakai untuk "harus tahu X dulu", bukan diganti) — **Accepted**.
- [x] Migration baru (bukan edit migration lama) menambah kolom + index `(parent_concept_id)` — `migrations/0011_concept_hierarchy.{up,down}.sql`.
- [x] Query helper untuk ambil full ancestor chain / descendant subtree — `repository/concept_repository.rs::find_ancestors`/`find_descendants`, `WITH RECURSIVE` (bukan `ltree`/closure table — lihat ADR, alasan skala).
- [x] `docs/domain-model.md` disinkronkan.
**DoD:** ADR status Accepted, migration jalan + revert teruji (`sqlx migrate revert` x2 lalu `run` lagi, kolom/index/FK diverifikasi lewat `\d concepts`), 6 test di `tests/concept_hierarchy_test.rs`.
**Catatan implementasi:**
- Cycle prevention di `service/concept_service.rs::set_parent` (bukan DB constraint — Postgres tidak bisa enforce acyclicity di self-referencing FK): cek `concept_id` tidak sama dengan `new_parent_id`, dan `concept_id` tidak muncul di ancestor chain `new_parent_id`. 2 test khusus (self-loop, cycle 3-node A→B→C dicoba dibalik jadi C→A).
- `set_parent` adalah **satu-satunya** jalur tulis `parent_concept_id` — tidak ada endpoint HTTP untuk ini di P2-001 (itu nanti nyambung ke concept-authoring UI, belum ada ticket-nya eksplisit; P2-011/2-013 akan jadi konsumen pertama lewat konten yang benar-benar dibuat).

### P2-002 — ADR-0008: Content Versioning & Attempt Snapshot
**Status:** done
**Depends on:** -
**Deskripsi:** Kunci aturan: kalau `lessons.version`/`questions.version` naik (edit setelah publish), apa yang terjadi ke `attempts` yang sudah `submitted`/`evaluated` mereferensikan versi lama? (`ALR_Phase_Detail_Breakdown.md` 2.15, eksplisit "butuh ADR baru sebelum eksekusi P2").
**Acceptance Criteria:**
- [x] ADR baru (`docs/adr/0008-content-versioning.md`) — **Accepted**. Keputusan: `attempts` dapat kolom `question_snapshot jsonb` (captured di submit time, immutable sesudahnya) — bukan lesson/content_blocks (tidak scored, tidak butuh snapshot).
- [x] Aturan publish: edit ke row `published` **tidak pernah** mutate in-place — row baru dibuat (`version+1`, status `draft`), row lama tetap `published` sampai versi baru itu sendiri di-publish (baru `superseded_by` di-set + row lama `archived`). MVP Phase 2 scope: API menolak edit langsung ke row `published` (kolom `superseded_by` sudah siap, tapi alur auto-supersede belum dibangun — lihat ADR untuk alasan).
- [x] Konsekuensi ke `assessment_questions`/`attempts` didokumentasikan eksplisit di ADR.
**DoD:** ADR status Accepted, migration `0012_content_versioning.{up,down}.sql` (`attempts.question_snapshot`, `questions.superseded_by`, `lessons.superseded_by`) jalan + revert teruji, `docs/domain-model.md` disinkronkan.
**Catatan implementasi:**
- `question_snapshot` di-populate di `assessment_service::submit_attempt` (map `question_id → {data, correct_answer, explanation, version}`) di tempat yang sama `learning_events` sudah ditulis (P1-007) — pola snapshot yang sama, bukan pola baru.
- 1 test end-to-end (`submit_writes_question_snapshot_matching_content_at_submit_time` di `tests/assessment_test.rs`): submit, lalu edit `questions.correct_answer` langsung lewat SQL, verifikasi snapshot attempt **tidak berubah** — bukti properti fairness-nya benar-benar jalan, bukan cuma kolom kosong.
- `superseded_by` ditambah ke model (`Question`, `Lesson`) tapi **belum ada consumer** — itu memang scope P2-005 (publish flow) dan seterusnya, ticket ini cuma menyiapkan schema + ADR-nya.

### P2-003 — Content Block SDK v1
**Status:** done
**Depends on:** -
**Deskripsi:** Registry tipe block (2.7) + validasi schema `content_blocks.data` per `type` di application layer — pola yang sama seperti `question_schema.rs` (P1-004), bukan didesain ulang.
**Acceptance Criteria:**
- [x] Block type MVP didukung: `text`, `heading`, `example`, `audio`, `video`, `image` (referensi `asset://`), `flashcard`, `question_embed` (by-reference ke `question_id`, **bukan** isi soal ditulis ulang — aturan keras dari 2.1, dienforce struktural: validator cuma terima field `question_id`).
- [x] Tiap type punya schema validasi sendiri (`service/block_schema.rs`, trait `BlockTypeValidator` + registry — pola sama seperti `QuestionTypeValidator` P2-004), tipe tak dikenal ditolak eksplisit (`invalid_block_schema`).
- [x] `question_embed` block memvalidasi `question_id` yang direferensikan benar-benar ada — `content_block_service.rs::validate_and_replace_blocks`, dicek batched (1 query `= ANY($1)` lewat `question_repository::find_existing_ids`, bukan N+1).
**DoD:** unit test validasi tiap block type (`service/block_schema.rs`, valid+invalid tiap type) + 4 integration test di `tests/content_block_test.rs` (mixed valid types, unregistered type rejected tanpa partial write, `question_embed` ke id tidak ada ditolak, `replace_content_blocks` transaksional — old blocks selamat kalau replace berikutnya gagal validasi).
**Catatan implementasi:**
- `content_repository::replace_content_blocks` (baru): delete-then-insert 1 transaction — lesson selalu replace *seluruh* set block sekaligus (parser P2-006 re-parse semua ALM tiap edit), bukan patch block-by-block.
- `content_block_service::validate_and_replace_blocks` adalah **satu-satunya** jalur tulis `content_blocks` yang dimaksudkan dipakai P2-006 (ALM parser) dan P2-008 (lesson authoring API) — belum ada HTTP endpoint di ticket ini sendiri (itu scope P2-008), P2-003 cuma menyiapkan SDK-nya siap pakai + teruji.

### P2-004 — Question Type Registry v1 (refactor dari fixed match)
**Status:** done
**Depends on:** -
**Deskripsi:** `service/question_schema.rs` saat ini `match type { "mcq" => ..., "fill_blank" => ... }` — cukup untuk 2 tipe, tapi 2.4 eksplisit minta arsitektur *registered component type* (nambah tipe = daftar validator baru, bukan migration/redeploy besar). Refactor ke pola yang sama dipakai `AIProvider`/`AssetStorage` trait (P1-010/011) — trait `QuestionTypeValidator` + registry map.
**Acceptance Criteria:**
- [x] `mcq` dan `fill_blank` tetap jalan identik — semua test P1-004 lama hijau tanpa diubah setelah refactor (regression check: `tests/content_and_question_test.rs` tidak disentuh sama sekali).
- [x] 1 tipe baru ditambah lewat registry murni (bukan match baru) — `matching` (`{"pairs": [["a","b"], ...]}`, min 2 pasang, tiap pasang persis 2 string).
- [x] Tipe belum diregister tetap ditolak eksplisit (`invalid_question_schema`).
**DoD:** unit test registry (`mcq_and_fill_blank_still_validate_identically_after_registry_refactor`, 3 test `matching`, `unregistered_type_is_rejected`) — semua di `service/question_schema.rs`, tidak ada regression di test P1-004 (diverifikasi: full suite tetap hijau).
**Catatan implementasi:** `QuestionTypeRegistry::new()` dibangun ulang tiap panggilan `validate()` (bukan lazy-static) — validasi terjadi per-request (create question), bukan hot-loop, jadi overhead alokasi registry kecil ini diabaikan sengaja daripada nambah dependency lazy-static untuk beberapa entry saja.

### P2-005 — Content & Question Publish Flow (draft → in_review → published)
**Status:** done
**Depends on:** P2-002 (ADR versioning harus ada dulu)
**Endpoint:** `POST /questions/{id}/submit-review`, `POST /questions/{id}/publish`, `POST /questions/{id}/reject`, `POST /lessons/{id}/submit-review`, `POST /lessons/{id}/publish`, `POST /lessons/{id}/reject`
**Deskripsi:** State machine `draft → in_review → published` untuk `questions` DAN `lessons` — kolom `status` sudah punya CHECK constraint benar di kedua tabel sejak P0-007, ini murni service+handler+permission layer yang belum ditulis (P1-004 dulu sengaja menunda ini sebagai "P1-004b" — sekarang ditutup lewat ticket ini, digeneralisasi ke lesson juga).
**Acceptance Criteria:**
- [x] `curriculum_developer` bisa submit draft → `in_review`, **tidak bisa** langsung publish (matrix ADR-0006: "Question bank: publish" cuma ✅ untuk platform_admin/org_owner/academic_director/reviewer) — diverifikasi test DAN smoke test manual (curl) ke server asli.
- [x] `reviewer`/`academic_director`/`org_owner`/`platform_admin` bisa `in_review → published` atau reject balik ke `draft`.
- [x] Transisi tidak valid (`draft→published` langsung, publish oleh role tanpa izin, publish ulang item yang sudah `published`) ditolak dengan error code jelas (`invalid_status_transition` / `forbidden`).
**DoD:** 9 integration test di `tests/publish_flow_test.rs` (questions + lessons berdampingan — state machine sama persis via `service/publish_flow.rs`) + 3 unit test murni transisi + **smoke test manual end-to-end ke server asli**: curriculum_developer submit → reviewer publish → publish ulang ditolak 422 — persis skenario DoD, dijalankan lewat curl bukan cuma test.
**Catatan implementasi:**
- `service/publish_flow.rs`: 1 modul pure-function dipakai `question_service.rs` DAN `content_service.rs` (lesson) — `questions`/`lessons` punya state machine identik, jadi 1 sumber kebenaran, bukan aturan yang diketik ulang 2x yang bisa divergen.
- Permission baru di `service/permissions.rs`: `Action::SubmitReview` (role sama seperti `Create` — curriculum_developer+) dan `Action::Publish` (role sama seperti matrix ADR-0006 "publish" row — reviewer+, **tanpa** curriculum_developer, sesuai prinsip "tidak approve pekerjaan sendiri").
- Aturan versioning ADR-0008 (row `published` tidak boleh diedit in-place, `superseded_by`) **belum** ada endpoint edit-setelah-publish di ticket ini — publish flow cuma menangani transisi status (`draft→in_review→published`/`reject`), bukan re-edit konten yang sudah live. Itu tetap scope P2-006/P2-008 (authoring API) nanti, bukan diam-diam diimplementasikan di sini.

### P2-006 — ALM (ALR Learning Markdown) Parser v1
**Status:** done
**Depends on:** P2-003 (Block SDK harus ada dulu, parser nulis ke situ)
**Deskripsi:** Parser `ALM → Semantic AST → content_blocks` rows, sesuai spesifikasi 2.1 (directive block `:::type ... :::`, contoh persis ada di breakdown doc).
**Acceptance Criteria:**
- [x] Markdown standar (`#`-`######`, `>`) ter-parse jadi heading/example block — `service/alm_parser.rs::parse`, pure function.
- [x] Directive `:::example`, `:::audio`, `:::video`, `:::flashcard` ter-parse sesuai contoh persis di `ALR_Phase_Detail_Breakdown.md` 2.1 — diverifikasi test yang meniru contoh persis dari dokumen (`parses_audio_video_flashcard_directives_as_key_value`).
- [x] `question_embed` ter-parse dari `:::question_embed\nquestion_id: <uuid>\n:::`, **tidak** menerima isi soal ditulis inline (2.1 aturan keras) — **catatan penting**: contoh ALM di dokumen sumber sendiri (`:::question id="q_123" type="multiple_choice"...`) berisi soal inline, KONTRADIKTIF dengan aturan kerasnya sendiri 2 paragraf di bawahnya ("Lesson cukup bilang `embed question q_123`"). Parser mengikuti **aturan**, bukan contoh yang salah — didokumentasikan eksplisit di komentar kode, bukan diam-diam dipilih salah satu.
- [x] `raw_source` (ALM asli persis) disimpan bareng `data` (AST) per block.
- [x] Input ALM malformed (directive tidak ditutup, tipe directive kosong) ditolak dengan error jelas (`invalid_alm_source`), bukan parse-partial diam-diam.
**DoD:** 11 unit test murni (`service/alm_parser.rs`, tidak butuh DB) — termasuk 1 test yang menjalankan CONTOH LENGKAP dari `ALR_Phase_Detail_Breakdown.md` 2.1 persis dan mencocokkan urutan tipe block yang dihasilkan.
**Catatan implementasi:**
- Parser tidak hardcode daftar tipe directive yang "sah" — cuma tahu 2 pola parsing body (`example` = free text, selainnya = key:value pairs). Validitas tipe (apakah `foo` di `:::foo:::` benar-benar terdaftar) adalah tanggung jawab `block_schema` (P2-003) di layer berikutnya — parser dan registry sengaja dipisah supaya nambah tipe block baru tidak pernah butuh sentuh parser ini.
- `image` cuma via sintaks Markdown `![alt](asset://...)`, **tidak** ada `:::image:::` directive — sesuai contoh persis di dokumen sumber (image beda pola dari audio/video/flashcard).

### P2-007 — Paste Normalizer v1
**Status:** done
**Depends on:** P2-006
**Deskripsi:** HTML/plain-text/Markdown-dari-sumber-lain → ALM ternormalisasi (2.3) — supaya hasil akhirnya identik terlepas sumbernya Word/Google Docs/website/ChatGPT.
**Acceptance Criteria:**
- [x] `<h2>X</h2>` (HTML) dan `## X` (Markdown murni) menghasilkan AST Heading block yang identik setelah lewat normalizer + parser (P2-006) — test `html_heading_produces_identical_ast_to_markdown_heading` membandingkan `Value` hasil parse langsung (bukan cuma "kelihatan mirip").
- [x] Minimal 2 sumber input didukung eksplisit: HTML dan plain Markdown (PDF/OCR ditangani terpisah di P2-015, bukan di sini). Markdown lewat tanpa perubahan (sudah ALM-compatible by definition).
**DoD:** 5 unit test (`service/paste_normalizer.rs`) termasuk golden-test heading HTML vs Markdown, paragraf+blockquote, image, dan strip inline formatting tags (`<strong>` dst dibuang dari teks).
**Catatan implementasi:** Scanner tag-level sederhana (cari `<tag>...</tag>` berurutan), **bukan** parser HTML5 penuh — cukup untuk paste dari editor (Word/Google Docs/website) yang HTML block-level-nya relatif flat sesuai scope 2.3. Tidak menangani HTML bersarang dalam yang aneh; itu bukan kasus yang disebut di AC.

### P2-008 — Lesson Authoring API
**Status:** done
**Depends on:** P2-006, P2-005
**Endpoint:** `POST /lessons`, `PUT /lessons/{id}` (isi: ALM/HTML raw text), terhubung ke publish flow P2-005
**Deskripsi:** Endpoint admin/curriculum_developer untuk menulis lesson via ALM (bukan WYSIWYG penuh dulu — sesuai keputusan MVP-first "WYSIWYG boleh belakangan"), tersimpan lewat parser P2-006 jadi `content_blocks`.
**Acceptance Criteria:**
- [x] `POST /lessons` bikin lesson baru status `draft`, `PUT /lessons/{id}` re-parse ALM dan replace `content_blocks` (transaksional lewat `content_block_service::validate_and_replace_blocks` yang sudah ada dari P2-003 — tidak ditulis ulang).
- [x] Ditolak kalau role tidak berhak (matrix ADR-0006, sama role dengan question bank create).
- [x] Lesson yang sudah `published` tidak bisa diedit langsung — ADR-0008 dienforce persis (`cannot_edit_published_content`, bukan cuma didokumentasikan tapi tidak dicek).
**DoD:** 6 integration test (`tests/content_authoring_test.rs`): create dari markdown, create dari HTML (normalizer terpakai beneran), tolak tipe lesson invalid, tolak ALM malformed tanpa membuat lesson yatim, tolak role tanpa izin, update replace blocks, tolak edit lesson published. Plus **smoke test manual end-to-end ke server asli**: bikin lesson via ALM multi-baris (persis contoh "Present Simple" dari `ALR_Phase_Detail_Breakdown.md`), verifikasi lewat `GET /lessons/{id}` hasil block-nya persis (heading→text→example→example).
**Catatan implementasi:** `content` + `format` (`"markdown"`/`"html"`) dikirim 1 request — server yang jalankan normalizer→parser→validate→write, client tidak perlu tahu pipeline internalnya.

### P2-009 — Curriculum/Level/Unit Authoring API
**Status:** done
**Depends on:** -
**Endpoint:** `POST /curricula`, `POST /curricula/{id}/levels`, `POST /levels/{id}/units`
**Deskripsi:** Saat ini struktur curriculum→level→unit cuma bisa dibuat lewat `seed.sql` manual (P1-003 cuma READ). Phase 2 butuh jalur admin resmi supaya modul baru tidak perlu SQL tangan.
**Acceptance Criteria:**
- [x] Create untuk `curricula`/`levels`/`units` dengan permission sesuai matrix ADR-0006 ("Curriculum: create/edit" row — `Resource::Curriculum` baru di `permissions.rs`, role sama dengan question bank create).
- [x] `order_index` diterima langsung dari caller (bukan auto-increment) — insert di posisi manapun tidak merusak urutan existing karena tidak ada asumsi "selalu di akhir".
**DoD:** 2 integration test langsung (permission ditolak untuk role salah) + **1 test rantai penuh** (`full_authoring_chain_shows_up_in_curriculum_tree`): curriculum→level→unit→lesson dibuat murni lewat API P2-008/P2-009, lalu dibuktikan muncul persis di `GET /curricula/{id}/tree` — endpoint Phase 1 yang **tidak diubah sama sekali** oleh Phase 2. Ini bukti hidup bahwa Phase 1 dan Phase 2 satu sistem, bukan 2 sistem paralel. Plus smoke test manual end-to-end ke server asli (curl, bukan cuma test).
**Catatan implementasi:** Tidak ada pre-check "parent exists" sebelum insert (misal cek `curriculum_id` valid sebelum bikin level) — mengikuti preseden `question_service::create_question` (P1-004) yang juga tidak precheck `bank_id`, mengandalkan FK constraint. Konsisten dengan pola yang sudah ada, bukan pola baru.

### P2-010 — Direct-to-R2 Presigned Upload (media besar)
**Status:** done
**Depends on:** -
**Endpoint:** `POST /assets/presigned-upload` (baru), `POST /assets/confirm` (baru) — di samping `POST /assets/upload` P1-010 yang tetap ada untuk file kecil.
**Deskripsi:** 2.14 eksplisit: "jangan proxy file besar lewat Rust API". P1-010 (proxy) tetap valid untuk file kecil, tapi audio/video lesson Phase 2 butuh jalur upload langsung client→R2.
**Acceptance Criteria:**
- [x] Endpoint mengembalikan presigned PUT URL (pakai `AssetStorage` trait yang sudah ada, `service/storage.rs` — tambah method baru `presigned_put_url`/`exists`, bukan bikin abstraksi kedua)
- [x] Client upload langsung ke R2 pakai URL itu, lalu konfirmasi ke backend (`POST /assets/confirm`) supaya row `assets` tercatat setelah upload sukses — `exists()` (HEAD request) dicek sebelum menulis row, tidak percaya klaim klien begitu saja
- [x] Access control per asset (public vs org-scoped vs user-scoped, 2.14) — dibedakan `public`/`private` dulu (kolom `assets.visibility`, migration 0013), org/user-scoped ditunda ke fase berikutnya
**DoD:** test generate presigned URL (offline, `InMemoryStorage` fake) — 2 test baru di `tests/asset_test.rs`; **smoke test manual ke R2 asli** dilakukan (presigned PUT → upload file beneran → confirm → GET signed URL berhasil ambil isi file → confirm sebelum upload ditolak `422 asset_not_uploaded`).
**Catatan implementasi:**
- Desain stateless: tidak ada row "pending" di DB antara `presigned-upload` dan `confirm` — key adalah UUID server-generated, hanya bisa ditulis lewat presigned URL yang sah, jadi tidak perlu disimpan di server antara dua request.
- `visibility` menentukan TTL signed GET URL yang dikembalikan `confirm`: `private` pakai `Config::asset_signed_url_ttl_seconds` (default 3600s, sama seperti P1-010), `public` pakai `Config::asset_public_signed_url_ttl_seconds` (default 604800s/7 hari — batas maksimum SigV4 presigned URL).
- `Config` dapat 2 field baru: `asset_presigned_put_ttl_seconds` (default 900s), `asset_public_signed_url_ttl_seconds`. Semua 11 file test yang construct `Config` langsung di-update (field non-optional).

### P2-011 — Curriculum Constitution: Grammar 11-Section Pattern
**Status:** done
**Depends on:** P2-006
**Deskripsi:** 2.9 — pola wajib 11-bagian untuk **setiap** materi grammar (What is it/Form/Positive/Negative/Question/When to use/Signal words/Common mistakes/Practice/Speaking/Writing). Ini "Constitution rule" yang jadi rel untuk generator AI (P2-013) DAN human author.
**Acceptance Criteria:**
- [x] Constitution didokumentasikan sebagai file config yang direview manusia (bukan hidup cuma di kepala/prompt) — `agent/docs/curriculum-constitution.md`, isi pola 11-bagian persis
- [x] Validator (`service/curriculum_constitution.rs::validate_grammar_lesson`) mengecek 1 lesson grammar type sudah mengandung 11 section itu sebelum bisa submit-for-review
**DoD:** constitution file ada + direview user, validator punya test (lesson lengkap 11 section lolos, lesson kurang 1 section ditolak dengan pesan jelas bagian mana yang hilang) — 4 unit test di `curriculum_constitution.rs` + 3 integration test di `tests/curriculum_constitution_test.rs` lewat endpoint `POST /lessons/{id}/submit-review` beneran, bukan cuma validator murni.
**Catatan implementasi:**
- "Lesson grammar type" dideteksi lewat `lesson_concepts` → `concepts.type = 'grammar'` (bukan `lessons.type`, yang enum-nya `learn/practice/speaking/writing/review/assessment` — tidak ada nilai "grammar" di sana). `content_repository::lesson_has_grammar_concept` baru, dipanggil dari `content_service::submit_lesson_for_review` sebelum transisi status.
- `NewLesson`/`POST /lessons` dapat field baru `concept_ids: Vec<Uuid>` (opsional, default kosong) — `content_repository::link_lesson_concepts` baru untuk menulis `lesson_concepts` saat lesson dibuat.
- Matching pakai numeric-prefix ("teks heading mulai dengan '05'"), bukan keyword — dipilih eksplisit untuk hindari false positive (mis. heading "Formal greetings" mengandung kata "Form" tapi bukan section "02 — Form"). Dijelaskan di `curriculum-constitution.md`.
- Gate ini di **submit-review**, bukan di save-draft — penulis bebas menyimpan draft belum lengkap, Constitution baru dipaksakan saat lesson mau masuk antrean review.
- Smoke test manual: lesson grammar dengan ALM asli (termasuk 3 block type baru dari P2-012) lewat `POST /lessons` → `submit-review` ditolak `422 grammar_constitution_incomplete` (kurang "07 — Signal words") → `PUT /lessons/{id}` lengkapi section → `submit-review` sukses `in_review`.

### P2-012 — Indonesian Learner Support Blocks
**Status:** done
**Depends on:** P2-003
**Deskripsi:** 2.10 — block khusus untuk learner Indonesia: `indonesian_learner_alert`, `common_trap`/`false_friends`, comparison "Think in English vs Pola Indonesia". Metadata `indonesian_difficulty_tag` di `concepts`/`questions` (dipakai weakness detection Phase 3 nanti, tapi field-nya perlu ada dari sekarang supaya konten yang ditulis Phase 2 sudah punya tag-nya, tidak perlu backfill).
**Acceptance Criteria:**
- [x] 3 block type baru terdaftar di registry P2-003 dengan schema masing-masing (`indonesian_learner_alert`, `common_trap`, `think_in_english`)
- [x] Kolom `indonesian_difficulty_tag` (nullable, additive) ditambah ke `concepts` — dipilih `concepts` (bukan `questions`) karena weakness detection/drill-down (Phase 3) beroperasi di level concept, migration 0014
**DoD:** unit test block validasi (6 test baru di `block_schema.rs`, 2 per tipe), migration `0014_indonesian_difficulty_tag` jalan + revert teruji + sync `domain-model.md`.
**Catatan implementasi:**
- 3 validator baru mengikuti pola `BlockTypeValidator` yang sama seperti `flashcard`/`example` — tidak perlu perubahan di `alm_parser.rs` sama sekali, directive generik `:::type\nkey: value\n:::`-nya sudah otomatis mendukung tipe baru begitu terdaftar di registry (dibuktikan smoke test manual: ketiga block type ini ditulis lewat ALM asli dan berhasil di-parse+tervalidasi lewat `POST /lessons`).
- `indonesian_learner_alert`: `{text}`. `common_trap`: `{term, explanation}`. `think_in_english`: `{indonesian_pattern, english_pattern}` — semua field wajib non-empty string, field tak dikenal ditolak (pola `reject_unknown_fields` yang sama seperti tipe lain).
- Kolom `indonesian_difficulty_tag` di `concepts` sudah selesai dari kerja migrasi P2-010/012 gabungan sebelumnya (migration 0014) — ticket ini hanya menambah 3 block type-nya.

### P2-013 — AI Content Generation Pipeline v1 (Lesson + Question)
**Status:** todo
**Depends on:** P2-006, P2-011, P2-005
**Endpoint:** internal (dipicu admin action, bukan endpoint publik student) — kemungkinan `POST /ai/generate-lesson`, `POST /ai/generate-questions`, lewat AI Gateway yang sama (P1-011)
**Deskripsi:** Blueprint → Generate → Validate → QA Agent → Human Review → Publish (roadmap Fase 2 poin 6). AITask baru: `LessonGeneration`, `QuestionGeneration` (sudah terdaftar di enum ADR-0004, belum diimplementasi provider call-nya). Sesuai ADR-0005: task ini **0 credit ke user** ("cost platform bukan cost user, task admin/content").
**Acceptance Criteria:**
- [ ] `LessonGeneration`: AI keluarkan ALM (bukan Block JSON — aturan 2.2), lewat parser P2-006, hasilnya masuk status `draft` (**tidak pernah** auto-publish — aturan keras 2.6/ADR-0004)
- [ ] `QuestionGeneration`: AI **wajib** keluarkan Semantic JSON langsung sesuai schema P2-004 (bukan ALM) — 2 jalur output berbeda ini harus benar-benar terpisah di prompt/parsing, jangan digabung satu template
- [ ] Blueprint input (topik, grammar target, vocab target, jumlah soal per skill) sebagai struct/schema eksplisit, bukan free-text prompt tak terstruktur
- [ ] `ai_tasks.status=failed` (gagal validasi schema/constitution P2-011) tidak charge credit ke platform account manapun tanpa audit trail — tetap tercatat di `ai_tasks`, cuma tidak lanjut ke publish
**DoD:** test generate lesson (mock provider, output valid → draft tersimpan lewat P2-006 parser), test generate question (mock provider, output tervalidasi P2-004), test output gagal validasi → `ai_tasks.status=failed`, tidak ada content_blocks/questions row yang setengah jadi.

### P2-014 — Content QA Agent v1
**Status:** todo
**Depends on:** P2-011, P2-013
**Deskripsi:** Cek otomatis sebelum konten (hasil AI generation ATAU human authoring) masuk antrean review manusia — konsistensi terminologi grammar, kelengkapan pola 11-bagian (P2-011), format soal sesuai schema (P2-004), CEFR level tag konsisten dengan level curriculum-nya.
**Acceptance Criteria:**
- [ ] Berjalan otomatis saat `submit-review` dipanggil (P2-005) — bukan proses terpisah yang harus dipicu manual
- [ ] Hasil QA (pass/fail + daftar issue) tersimpan/terlampir ke item yang direview, supaya human reviewer lihat langsung apa yang sudah dicek, bukan review dari nol
- [ ] QA fail **tidak** memblokir masuk `in_review` (manusia tetap harus bisa lihat & putuskan), tapi flag-nya harus jelas terlihat — jangan auto-reject tanpa manusia (prinsip "gerbang manusia" dari roadmap)
**DoD:** test tiap kategori pengecekan (constitution incomplete, question schema invalid, CEFR mismatch) menghasilkan flag yang benar, test QA pass tidak menghasilkan false-positive flag.

### P2-015 — OCR-to-Question Pipeline v1
**Status:** todo
**Depends on:** P2-010 (asset upload gambar/PDF), P2-004, P2-005, P2-014
**Endpoint:** `POST /ai/ocr-to-question` (atau setara)
**Deskripsi:** 2.6 — admin foto/scan halaman soal, sistem ekstrak jadi draft question. Alur wajib: `SCANNED → EXTRACTED → AI STRUCTURED → DRAFT → REVIEW → APPROVED → PUBLISHED` — **tidak pernah** AI→langsung published (aturan keras, kesalahan OCR pada TKA/Olimpiade bisa fatal).
**Acceptance Criteria:**
- [ ] AITask baru `OCRToQuestion` lewat AI Gateway yang sama (provider trait sudah ada, tinggal tambah task type + prompt vision)
- [ ] Output OCR selalu masuk sebagai `questions` status `draft`, wajib lewat P2-005 (submit-review→publish) — tidak ada shortcut
- [ ] Question Type Classification (2.6 diagram) minimal bisa bedakan `mcq` vs tipe lain, dan tipe yang tidak dikenali/tidak yakin ditandai eksplisit untuk perhatian ekstra reviewer, bukan dipaksa masuk salah satu kategori
**DoD:** test dengan gambar soal contoh (mock provider response terstruktur), verifikasi hasil selalu `draft` tidak pernah `published` langsung, test tipe tak dikenal ditandai bukan silently mis-classified.

### P2-016 — Validasi Pipeline: Generate & Publish Module 1 Penuh (Pre-Basic — Alphabet)
**Status:** todo
**Depends on:** P2-001 s/d P2-015 (semua di atas — ini ticket validasi integrasi, bukan fitur baru)
**Deskripsi:** Sesuai instruksi eksplisit roadmap ("jangan generate seluruh silabus sekaligus... mulai dari 1 modul Pre-Basic penuh untuk memvalidasi pipeline"). Pakai pipeline P2-006 s/d P2-015 buat menghasilkan **1 modul nyata** lengkap: Learn → Practice → Speaking → Writing → Review → Assessment, untuk topik Pre-Basic "Alphabet" (contoh eksplisit dari `ALR_Build_Roadmap.md`).
**Acceptance Criteria:**
- [ ] Modul lengkap (semua tipe lesson: `learn`, `practice`, `speaking`, `writing`, `review`, `assessment`) untuk 1 unit nyata, bukan data seed dummy
- [ ] Minimal sebagian kontennya lewat AI generation pipeline (P2-013), bukan 100% ditulis manual — supaya pipeline itu benar-benar tervalidasi ada yang lewat situ, bukan cuma "kodenya ada, belum pernah dipanggil sungguhan"
- [ ] Modul sudah `published`, bisa diakses lewat endpoint Phase 1 yang sudah ada tanpa perubahan (`GET /curricula/{id}/tree`, `GET /lessons/{id}`) — bukti bahwa Phase 1 dan Phase 2 memang tersambung, bukan 2 sistem paralel
- [ ] Minimal 1 assessment di modul ini benar-benar bisa dikerjakan end-to-end (attempt → submit → score) memakai soal yang dihasilkan pipeline Phase 2, bukan soal seed lama
**DoD:** didemo manual (curl atau browser) end-to-end: buka curriculum tree → modul Alphabet ada → buka tiap lesson → kerjakan assessment → dapat score. Ini bukti hidup, dicatat di `docs/tickets/phase-2.md` dan `docs/STATE.md` seperti smoke test manual di Phase 1.

### P2-017 — Integration Test Suite Phase 2 + Exit Checkpoint
**Status:** todo
**Depends on:** semua di atas
**Deskripsi:** Sama pola seperti P1-013 — cross-check semua endpoint baru Phase 2 punya test, plus 1 test end-to-end untuk checkpoint keluar Phase 2.
**Acceptance Criteria:**
- [ ] Semua endpoint P2-001 s/d P2-016 punya minimal 1 integration test (cross-check via `grep` pola sama seperti P1-013)
- [ ] 1 test end-to-end: admin authoring 1 lesson via ALM lewat API (P2-008) → submit-review → publish (P2-005) → lesson itu langsung bisa diakses lewat `/lessons/{id}` (endpoint Phase 1 yang tidak berubah) — ini persis contoh checkpoint Phase 2 di `ALR_Detailed_Blueprint.md` Bagian 6
**DoD:** `cargo test` hijau (lokal — CI masih P0-010 yang tertunda).

---

## Checkpoint keluar Phase 2 (harus bisa didemo, bukan asumsi)
1. [ ] Admin/curriculum_developer bisa menulis 1 lesson penuh via ALM lewat API, submit review, di-publish oleh reviewer — dan lesson itu langsung muncul di `GET /lessons/{id}` (endpoint Phase 1, tidak diubah) tanpa langkah manual tambahan.
2. [ ] Minimal 1 soal berhasil dihasilkan lewat AI Content Generation pipeline (P2-013), lolos QA Agent (P2-014), direview manusia, dan dipublish — bukan cuma soal seed manual.
3. [ ] Minimal 1 soal berhasil masuk lewat OCR-to-Question pipeline (P2-015) sampai status `draft` — membuktikan jalur ini benar-benar tersambung ke AI Gateway & Question Bank, walau belum di-scale.
4. [ ] **1 modul Pre-Basic penuh ("Alphabet")** — Learn/Practice/Speaking/Writing/Review/Assessment — live dan bisa dikerjakan end-to-end oleh 1 user percobaan, assessment-nya menghasilkan score seperti biasa (P2-016).
5. [ ] Concept hierarchy (P2-001) dipakai minimal 1 kali nyata di konten Phase 2 (bukan cuma migration kosong tanpa data) — supaya Phase 3 nanti punya sesuatu untuk drill-down.

Kalau poin 4 belum jalan end-to-end, jangan lanjut ke Phase 3 walau ticket lain kelihatan sudah "done" — sama semangatnya dengan aturan poin 4 di checkpoint Phase 1.

---

## Strategi eksekusi (urutan sesi yang disarankan)

Pengelompokan di bawah mengikuti dependency graph di atas, bukan urutan nomor ticket semata. Tiap sesi diakhiri dengan: build, test, `cargo fmt`, update ticket file + `docs/STATE.md`, commit di `titian-backend` + `alr` — pola yang sama persis dipakai sepanjang Phase 1.

| Sesi | Ticket | Fokus | Kenapa dikelompokkan begini |
|---|---|---|---|
| 1 ✅ | P2-001 + P2-002 | 2 ADR (concept hierarchy, content versioning) | **Selesai 2026-08-23** — ADR-0007/0008 Accepted, migration 0011/0012 jalan + revert teruji, 7 test. Keduanya sudah lewat "gerbang manusia" (user eksplisit minta arsitektur terbaik dibangun sekaligus, konfirmasi diberikan di percakapan). |
| 2 ✅ | P2-003 + P2-004 + P2-005 | Block SDK, question type registry, publish flow | **Selesai 2026-08-23** — 3 registry/flow baru, 20 test (unit+integration), smoke test manual publish flow ke server asli. |
| 3 ✅ | P2-006 + P2-007 + P2-008 + P2-009 | Parser ALM, normalizer, lesson + curriculum authoring API | **Selesai 2026-08-23** — 24 test baru, smoke test manual end-to-end ke server asli (bikin curriculum→level→unit→lesson via ALM, muncul persis di `GET /curricula/{id}/tree` dan `GET /lessons/{id}` — endpoint Phase 1 yang tidak diubah sama sekali). |
| 4 | P2-010 + P2-011 + P2-012 | Presigned upload, grammar constitution, Indonesian learner blocks | Independen satu sama lain, bisa paralel kalau ada lebih dari 1 agent; digabung 1 sesi karena masing-masing kecil. |
| 5 | P2-013 + P2-014 | AI generation pipeline + QA Agent | Baru masuk akal setelah authoring manual (sesi 3) terbukti jalan — AI generation menulis lewat jalur yang sama, QA Agent butuh constitution (sesi 4) sudah ada. |
| 6 | P2-015 | OCR-to-Question | Depends langsung ke hampir semua sesi sebelumnya (asset upload, question registry, publish flow, QA Agent) — sengaja ditaruh sendirian karena paling kompleks & paling banyak dependency. |
| 7 | P2-016 | Validasi: generate & publish Module 1 penuh | Ticket integrasi murni, tidak ada kode baru signifikan — ini pembuktian bahwa sesi 1–6 benar-benar tersambung, bukan 6 subsistem paralel yang kebetulan lulus test masing-masing. |
| 8 | P2-017 | Test suite penuh + checkpoint | Sama pola P1-013 — penutup fase. |

**Total 8 sesi** (vs 6 sesi di Phase 1) — Phase 2 memang lebih besar sesuai catatan roadmap sendiri ("6–10 minggu", fase paling padat keputusan). Kalau user mau mempercepat, sesi 4 adalah kandidat paling aman untuk diparalel/diskip-sementara (paling independen, paling tidak memblokir sesi lain) — sesi 1, 2, 3 tidak bisa dipercepat urutannya karena rantai dependency-nya lurus.

**Perbedaan penting dari strategi Phase 1:** Phase 1 semua ticket bisa langsung dieksekusi tanpa menunggu keputusan user (ADR-nya sudah selesai duluan di Phase 0). Phase 2 **tidak** — sesi 1 (P2-001, P2-002) wajib berhenti dan menunggu approval user sebelum sesi 2 dimulai, karena isinya adalah 2 ADR baru yang mengunci struktur data. Jangan lanjut ke sesi 2 di sesi yang sama dengan sesi 1 kecuali user eksplisit approve ADR-nya dulu.
