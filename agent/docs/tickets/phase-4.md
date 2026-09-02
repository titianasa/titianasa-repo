# Phase 4 — Core Learning Loop (roadmap-Fase-3 remainder)

🟢 **SELESAI (2026-09-02)** — semua 5 ticket (P4-001 s/d P4-005) done, semua 5 checkpoint keluar tercentang, 224/224 test lulus di `titian-backend-bun`.

Target: belum diestimasi. Depends on: Phase 3 checkpoint terpenuhi penuh (lihat `docs/tickets/phase-3.md` — semua 5 ticket + 4 checkpoint done, 201 test lulus di `titian-backend-bun`, 2026-08-31).

Sumber utama breakdown ini: `agent/ALR_Phase_Detail_Breakdown.md`'s `## PHASE 3 — Core Learning Loop` (§3.1–§3.9). **Ini bukan ticket-Phase-3** — lihat "Keputusan scope" di bawah untuk penjelasan penomoran yang membingungkan ini.

---

## Keputusan scope (baca duluan)

Roadmap (`agent/ALR_Build_Roadmap.md`) dan file ticket ini (`docs/tickets/phase-N.md`) punya 2 skema penomoran fase yang **berbeda dan tidak sinkron** — ini sudah kejadian 2 kali sekarang, dicatat lagi di sini biar tidak bingung untuk ketiga kalinya:
- Roadmap-**Fase 3** ("Core Learning Loop") item 1-3 (Learning Event, Mastery engine, FRSS/SRS engine) **sudah selesai duluan**, dibangun di dalam ticket-**Phase 1** (P1-007/P1-008/P1-009), karena checkpoint keluar Phase 1 sendiri butuh jalur itu.
- Ticket-**Phase 3** (`docs/tickets/phase-3.md`, baru selesai) sebenarnya adalah **roadmap-Fase 4** ("Exercise Engine & 4 Skills") — bukan roadmap-Fase 3.
- File ini, ticket-**Phase 4**, isinya **sisa roadmap-Fase 3** (item 4-9: Knowledge Graph, weakness detection, dst) — **bukan** roadmap-Fase 4 ronde kedua.

Singkatnya: nomor "Phase N" di nama file ticket cuma urutan sesi kerja, **tidak** sama dengan nomor "Fase N" di roadmap. Selalu cek isi/sumbernya, jangan asumsi dari angkanya.

`ALR_Phase_Detail_Breakdown.md`'s `## PHASE 3` (§3.1–§3.9) sendiri sudah punya urutan MVP-first eksplisit (pola sama seperti yang dipakai `phase-2.md`/`phase-3.md`):

> "Urutan MVP-first Phase 3: **3.1** (weakness detection dasar dengan drill-down 2 level) → **3.6** (queue gabungan sederhana) → **3.2** (knowledge graph minimal, prerequisite untuk 1 level) → **3.5** (lesson packet, bisa versi sederhana dulu) → 3.3+3.4+3.7 (forgetfulness/retrieval variation/mistake bank — butuh cukup data historis untuk berguna, bisa menyusul) → 3.8+3.9 (rescue mode & tutor bridge, terhubung Phase 4/8)."

File ini mengambil persis 4 item pertama urutan itu — **§3.1, §3.6, §3.2, §3.5** — dan berhenti di situ. Yang **sengaja ditunda**, bukan bagian ticket-Phase-4 ini:
- **§3.3 (Forgetfulness Score) + §3.4 (Retrieval Variation) + §3.7 (Mistake Bank)** — breakdown-nya sendiri bilang "butuh cukup data historis untuk berguna". `masteries`/`frss_schedule` saat ini cuma simpan nilai terkini (upsert in-place, bukan history) — Forgetfulness Score yang nyata butuh entah tabel snapshot baru atau nge-mining `learning_events` langsung, belum ada datanya untuk berguna sekarang.
- **§3.8 (5 Jenis AI Intervention) + §3.9 (AI vs Human Recommendation Trigger)** — terhubung ke Phase marketplace/tutor (jauh di luar scope ini). §3.9 juga **satu-satunya item Phase 3 yang ditandai eksplisit butuh ADR baru sebelum implementasi** (`ALR_Phase_Detail_Breakdown.md`'s "Cara pakai dokumen ini": "threshold rescue-mode/tutor-bridge (3.9)") — ditunda berarti gerbang ADR itu belum perlu dilewati sekarang.

## Temuan riset (jadi dasar desain ticket di bawah — dicatat supaya tidak diulang trial-error)

- **`GET /review-queue` saat ini flat dan diurutkan tanggal, bukan berdasar kelemahan** — `frss_repository.findDue` sort utama `dueAt` ascending, `masteries.score` cuma tiebreaker kalau `dueAt`-nya sama persis. Tidak ada drill-down atau granularitas sub-concept sama sekali.
- **Tombol "Review" di halaman Latihan (`titian-web`) tidak punya `onClick` sama sekali** — dikonfirmasi masih benar. Juga **tidak ada alur "submit review" khusus** sisi backend — review FRSS saat ini numpang di alur submit attempt biasa (`assessment_service.submitAttempt`, deviasi ADR-0003 yang sudah tercatat). `POST /questions/{id}/check` (P3-001 — sudah manggil `frssService.recordReview` per concept) adalah handler asli yang pas buat "learner lagi ngerjain review", bukan endpoint baru.
- **`concept_prerequisites` ada di schema, tapi benar-benar mati** — nol referensi di luar `schema.ts`. `concept_repository.ts`'s `findAncestors`/`findDescendants` (pola `WITH RECURSIVE` buat containment hierarchy `parent_concept_id`, P2-001/ADR-0007) adalah template yang pas buat ditiru untuk traversal edge prerequisite — graph **terpisah dan additive**, bukan reinterpretasi `parent_concept_id`. `docs/STATE.md` punya guard aktif: jangan campur semantik keduanya tanpa ADR baru yang men-supersede ADR-0007 — ticket-ticket di bawah **tidak** menyentuh semantik `parent_concept_id` sama sekali, jadi tidak butuh ADR baru, tapi harus ditulis eksplisit di ticket-nya supaya guard itu tidak disalahartikan sebagai penghalang kerjaan ini.
- **Tidak ada tabel history untuk mastery atau FRSS** — `masteries` dan `frss_schedule` dua-duanya upsert in-place, cuma simpan nilai terkini. Ini alasan §3.3/§3.4/§3.7 ditunda (lihat "Keputusan scope").
- **Nol kode di mana pun** (backend maupun frontend) untuk Mistake Bank, Personal Learning Queue, Lesson Packet, Forgetfulness Score, atau Retrieval Variation — dikonfirmasi lewat grep menyeluruh. Clean slate, tidak ada risiko duplikasi.
- **Checkpoint keluar bagian ini sudah tertulis persis di 2 dokumen sumber** (`ALR_Phase_Detail_Breakdown.md` baris 424, `ALR_Detailed_Blueprint.md` baris 551-556) — dipakai apa adanya sebagai skenario checkpoint utama ticket-Phase-4 ini.

---

### P4-001 — Weakness detection: concept mastery drill-down (§3.1)
**Status:** done (2026-08-31, `titian-backend-bun`)
**Depends on:** P2-001 (concept hierarchy, `parent_concept_id`), P1-008 (mastery engine) — semua sudah done
**Endpoint baru:** `GET /concepts/{id}/mastery-breakdown`
**Deskripsi:** §3.1 — bukan cuma skor per skill top-level, tapi drill-down sampai sub-concept ("Present Simple 61% ← weak" lalu turun lagi "Questions 49% ← very weak"). MVP: drill-down 2 level, bukan mendalam tak terbatas.
**Acceptance Criteria:**
- [ ] Walk `parent_concept_id` containment 2 level ke bawah dari 1 concept root (reuse pola `WITH RECURSIVE` dari `concept_repository.findDescendants`, batasi depth), attach skor `masteries` (score/confidence) caller di tiap node yang ada datanya
- [ ] Node dengan score di bawah threshold ditandai eksplisit `weak: true` di response — threshold baru di `config.ts` (`weaknessScoreThreshold`, pola sama `masteryConfidenceThreshold`), bukan hardcode di kode
- [ ] Node tanpa data mastery sama sekali (belum pernah dikerjakan) TIDAK ditandai `weak` — beda kondisi ("belum ada data" vs "sudah dikerjakan, hasilnya lemah"), sama disiplinnya dengan `insufficient_data` di `GET /mastery/{id}` yang sudah ada
- [ ] Auth: sama seperti `GET /mastery/{id}` yang sudah ada (`mastery`/`view`) — cuma data milik caller sendiri, tidak ada parameter target-user
**DoD:** test backend baru (`concept-mastery-breakdown.test.ts`) — tree 2 level dengan mastery campuran (kosong/lemah/kuat) di beberapa node, assert struktur+flag `weak` benar; test node tanpa data tidak ke-flag weak.

**Catatan implementasi:** `concept_repository.findDescendantsUpTo(db, id, maxDepth)` — varian depth-bounded dari `findDescendants` yang sudah ada (`WITH RECURSIVE ... WHERE d.depth < maxDepth`), mengembalikan tiap row dengan `depth`-nya supaya service bisa susun tree tanpa query tambahan per level. `mastery_repository.findMany` — batch lookup 1 query buat semua concept id di tree (root+descendants) sekaligus, hindari N+1. Logic tree-building + flag `weak` ada di `mastery_service.getMasteryBreakdown` (bukan file/service baru — domainnya tetap "mastery", cuma sekarang dikomposisi dengan `concept_repository`), reuse persis aturan `insufficient_data` yang sudah ada di `getMastery` (mastery di bawah `masteryConfidenceThreshold` → tidak pernah ditampilkan skornya, dan di sini juga tidak pernah di-flag `weak` — sinyal yang belum ada tidak bisa diklaim "lemah"). Threshold baru `weaknessScoreThreshold` (config `WEAKNESS_SCORE_THRESHOLD`, default 60.0) mengikuti pola persis `masteryConfidenceThreshold`. Route `GET /concepts/{id}/mastery-breakdown`, permission tier sama seperti `/mastery/{id}` yang sudah ada (`mastery`/`view`), 404 `concept_not_found` kalau root concept tidak ada. 6 test baru (`tests/concept-mastery-breakdown.test.ts`) — tree 2 level dengan skor campuran (termasuk assert eksplisit drill-down berhenti di level 2, bukan turun ke level 3), node tanpa data sama sekali, node dengan skor rendah tapi confidence rendah (harus tetap `insufficient_data`, bukan `weak: true`), 404, dan 401 tanpa token. Total sekarang **207/207 test lulus**. Dites juga lewat `curl` server asli: `GET /concepts/{id}/mastery-breakdown` tanpa token → 401, sesuai kontrak semua route lain. **Tidak ada API authoring concept sama sekali di codebase ini** (dikonfirmasi — nol route `POST /concepts` di manapun, concept cuma pernah dibuat lewat migration/seed atau `concept_ids` di question authoring) — jadi verifikasi live 2-level tree lewat browser/curl asli dengan data nyata tidak praktis dilakukan sesi ini tanpa bikin data throwaway; coverage-nya penuh lewat 6 integration test HTTP-level (lewat `buildApp`+`withTx`, bukan cuma unit test pure-logic), konsisten dengan standar verifikasi ticket backend-only lain di proyek ini (mis. P2-015's OCR endpoint).

### P4-002 — Personal Learning Queue (§3.6)
**Status:** done (2026-08-31, `titian-backend-bun` + `titian-web`)
**Depends on:** P4-001 (definisi "weak" dipakai ulang di sini), P3-001/P3-002 (`POST /questions/{id}/check`, `QuestionCheck`/`QuestionRenderer` dipakai ulang di FE)
**Endpoint baru:** `GET /learning-queue`
**Deskripsi:** §3.6 — bukan cuma daftar due-review, tapi gabungan concept yang due DAN yang lemah tapi belum due, dikelompokkan prioritas. MVP eksplisit "queue gabungan sederhana" — jangan over-scope ke estimasi menit presisi atau algoritma ranking rumit.
**Acceptance Criteria:**
- [ ] Gabungkan `frss_repository.findDue` (due review, sudah ada) dengan concept lemah (`masteries.score` di bawah `weaknessScoreThreshold`) yang belum due — bucket sederhana: "due & lemah" > "due" > "lemah, belum due", bukan skor gabungan rumit
- [ ] Tiap item bawa cukup info buat FE render sesi review: `concept_id`, `concept_name`, kategori prioritas, `suggested_question_ids` (reuse `frss_repository.findSuggestedQuestionIds` yang sudah ada)
- [ ] FE: tombol "Review" di halaman Latihan (`review-queue-list.tsx`, **saat ini tidak punya `onClick` sama sekali**) akhirnya benar-benar jalan — klik buka sesi review mini yang render `suggested_question_ids` lewat `QuestionRenderer`/`QuestionCheck` (P3-001/P3-002) yang sudah ada, dijawab lewat `POST /questions/{id}/check` yang sudah ada — **tidak ada grading/attempt machinery baru**, murni pakai ulang yang sudah terbukti jalan di Phase 3
**DoD:** test backend baru (`learning-queue.test.ts`) — user dengan 1 concept due + 1 concept lemah-belum-due + 1 concept kuat, assert urutan/kategori response benar (concept kuat tidak muncul). Verifikasi manual browser: tombol Review di Latihan benar-benar membuka & bisa dikerjakan, bukan cuma dekoratif.

**Catatan implementasi:** `mastery_repository.findWeak` — query baru (join `concepts`, filter `confidence >= masteryConfidenceThreshold AND score < weaknessScoreThreshold`, sort skor termiskin dulu) reuse persis aturan "confidence gate dulu sebelum nge-klaim lemah" dari P4-001. Logic merge ada di file service baru `learning_queue_service.ts` (bukan ditumpuk ke `frss_service.ts` — ini komposisi 2 subsistem, bukan FRSS scheduling itu sendiri): due-set dari `frss_repository.findDue` (sudah ada) + weak-set dari `findWeak` digabung ke 1 `Map<conceptId, entry>` (concept yang due DAN lemah otomatis jadi `critical`, tidak pernah muncul dobel), lalu di-sort bucket (`critical` > `due` > `weak`) dan tiebreak dalam masing-masing bucket (due-soonest / skor-terlemah). `limit`/cap pakai config yang sama persis dengan `/review-queue` (`reviewQueueDefaultLimit`) — sengaja tidak nambah config baru buat ini, sesuai instruksi "queue gabungan sederhana". Route `GET /learning-queue`, permission tier sama (`mastery`/`view`).

FE: `ReviewQueueList` (`review-queue-list.tsx`) sekarang terima prop `onReview` — tombol "Review" yang dari awal proyek **tidak pernah punya `onClick`** akhirnya benar-benar buka sesuatu; disabled kalau concept itu belum ada soal published (`questionIds.length === 0`). Komponen baru `ReviewSessionDialog` (`review-session-dialog.tsx`) — dialog yang render tiap `suggested_question_ids` lewat `QuestionCheck` yang sudah ada dari P3-002, **tidak ada grading/attempt machinery baru sama sekali**, submit-nya tetap lewat `POST /questions/{id}/check` yang sudah ada. Hook baru `useLearningQueue` — lebih simpel dari `useReviewQueue` yang lama (yang masih dipakai Beranda/Progres, sengaja tidak diubah — di luar scope ticket ini): `/learning-queue` sudah bawa `score` langsung di response-nya, jadi tidak perlu N+1 `GET /mastery/{concept_id}` per item kayak `useReviewQueue` masih lakukan. Latihan page (`(app)/latihan/page.tsx`) diganti dari `useReviewQueue` ke `useLearningQueue`.

5 test baru (`tests/learning-queue.test.ts`) — kategorisasi 3-bucket, urutan sort, concept dengan confidence rendah dikecualikan total (bukan cuma disembunyikan skornya), suggested_question_ids, 401 tanpa token. Total sekarang **212/212 test lulus**. **Diverifikasi end-to-end lewat Playwright ke server asli** (bukan cuma test): seed 2 concept demo (1 due+lemah → `critical`, 1 lemah-belum-due → `weak`) + 1 soal published per concept, lihat kartu Latihan menampilkan label prioritas ("Prioritas tinggi"/"Perlu latihan") + skor penguasaan yang benar, klik "Review" pada concept `critical` — dialog terbuka, jawab soal MCQ dengan benar, dapat feedback "Benar!" (mengonfirmasi grading + efek samping learning_event/mastery/FRSS beneran jalan lewat endpoint yang sudah ada), klik "Selesai" menutup dialog. Nol console error. Data demo dihapus setelah verifikasi (bukan bagian deliverable, murni throwaway seperti verifikasi Fase 7 migrasi Bun).

### P4-003 — Knowledge Graph: prerequisite graph (§3.2, "minimal, prerequisite untuk 1 level")
**Status:** done (2026-09-02, `titian-backend-bun`)
**Depends on:** P2-001 (concept hierarchy — `concept_prerequisites` tabelnya sudah ada dari situ, sekarang dipakai)
**Endpoint baru:** `POST`/`GET /concepts/{id}/prerequisites`, `DELETE /concepts/{id}/prerequisites/{prerequisite_concept_id}`
**Deskripsi:** §3.2 — concept saling terhubung sebagai prasyarat (bukan cuma containment tree yang sudah ada). MVP eksplisit "minimal, prerequisite untuk 1 level" — edge langsung saja, tidak perlu traversal rekursif mendalam kayak containment tree.
**Acceptance Criteria:**
- [ ] `concept_repository` dapat `findPrerequisites`/`findDependents` (query langsung ke tabel `concept_prerequisites`, edge 1 level — bukan `WITH RECURSIVE`, beda dari `findAncestors`/`findDescendants`)
- [ ] `concept_service` dapat `addPrerequisite`/`removePrerequisite` dengan disiplin cek-siklus yang sama seperti `setParent` (containment) — 1 concept tidak boleh jadi prasyarat dirinya sendiri baik langsung maupun tidak langsung
- [ ] **Eksplisit didokumentasikan di kode & PR**: ini mengisi `concept_prerequisites` persis sesuai desain ADR-0007 (graph terpisah dari `parent_concept_id`) — bukan mengubah semantik containment, jadi **tidak butuh ADR baru** (guard di `docs/STATE.md` soal ini tetap utuh, tidak dilanggar)
- [ ] Auth: tier sama seperti authoring concept lain (`curriculum`/`create`)
**DoD:** test backend baru (`concept-prerequisites.test.ts`) — tambah/hapus prerequisite, cek siklus ditolak (langsung dan 2-hop), `findPrerequisites`/`findDependents` balikin edge yang benar.

**Catatan implementasi:** `concept_repository` dapat 5 fungsi baru: `findPrerequisites`/`findDependents` (edge 1-level, dipakai route GET), `findTransitivePrerequisiteIds` (satu-satunya yang pakai `WITH RECURSIVE`, padanan `findAncestors` tapi jalan di tabel `concept_prerequisites` bukan `parent_concept_id` — dipakai HANYA untuk cek siklus, bukan diekspos ke route manapun), `insertPrerequisite` (idempotent lewat `onConflictDoNothing` — POST edge yang sudah ada bukan error, tetap 201), `deletePrerequisite`. Cek siklus di `concept_service.addPrerequisite` persis pola `setParent`: tolak self-loop dulu, lalu hitung `findTransitivePrerequisiteIds` dari concept yang DIUSULKAN jadi prerequisite — kalau concept asal sudah ada di situ, berarti nambah edge ini bakal nutup loop (ditolak `422 concept_prerequisite_cycle`). Kedua concept id (concept asal DAN prerequisite yang diusulkan) divalidasi ada dulu (`404 concept_not_found`) sebelum insert — supaya FK violation mentah dari DB tidak pernah bocor ke caller sebagai 500. Handler baru `concept_handler.ts` (**HTTP surface pertama untuk `concepts` di seluruh sejarah proyek ini** — `setParent`/`findAncestors` dari P2-001 juga belum pernah punya route, cuma dipanggil test langsung; P4-001's `mastery-breakdown` adalah GET pertama, ini WRITE pertama). Permission tier `curriculum`/`create` (sama seperti authoring lesson/curriculum lain) untuk ketiga route, termasuk GET-nya. 11 test baru (`tests/concept-prerequisites.test.ts`) — tambah edge, self-loop, siklus langsung (A→B lalu B→A ditolak), siklus transitif (A→B→C lalu C→A ditolak), 404 concept tidak ada, idempotent, 403 role student, GET cuma balikin edge langsung (bukan transitif), GET 404, DELETE edge, DELETE edge yang tidak ada (no-op, bukan error). Total sekarang **223/223 test lulus**. Dites juga lewat `curl` server asli: `GET /concepts/{id}/prerequisites` tanpa token → 401.

### P4-004 — Lesson Packet (§3.5, "versi sederhana dulu")
**Status:** done (2026-09-02, `titian-web`)
**Depends on:** P4-002 (`GET /learning-queue` dipakai sebagai sumber data)
**Endpoint baru:** tidak ada — murni FE, memakai `GET /learning-queue` yang sudah ada
**Deskripsi:** §3.5 — bukan "course", tapi paket review personal lintas-skill yang dirangkai otomatis dari beberapa concept lemah sekaligus (`PERSONAL REVIEW — Target: X` diikuti beberapa langkah 1 menitan). MVP eksplisit "versi sederhana dulu" — breakdown-nya sendiri bilang Personal Learning Queue (3.6) yang "bisa merangkai jadi paket", jadi ticket ini murni cara PRESENTASI dari data yang P4-002 sudah punya.
**Acceptance Criteria:**
- [ ] Layar baru "Personal Review" (`titian-web`) — ambil beberapa item teratas `GET /learning-queue`, render sebagai 1 sesi terarah (bukan daftar terpisah-pisah) yang dikerjakan berurutan lewat `QuestionCheck` yang sudah ada, concept demi concept
- [ ] Selesai 1 packet → ringkasan singkat (berapa concept dikerjakan, berapa benar) — bukan skor formal (ini bukan assessment/attempt, sama seperti P3-001's inline check tidak ada attempt row)
**DoD:** verifikasi manual browser — buka Personal Review dari Latihan, kerjakan sampai selesai, lihat ringkasan. Tidak perlu test backend baru (tidak ada endpoint baru ticket ini).

**Catatan implementasi:** Halaman baru `/latihan/personal-review` — ambil top-3 item `GET /learning-queue` (`PACKET_CONCEPT_COUNT`, tidak ada perhitungan estimasi menit, sesuai instruksi "sederhana dulu"), flatten `suggested_question_ids` tiap concept jadi 1 urutan step linear, render step aktif lewat `QuestionCheck` (P3-002) yang sudah ada — **tidak ada grading/attempt machinery baru**. `QuestionCheck` dapat 1 prop opsional baru `onResult` (backward-compatible, dipanggil tiap kali check berhasil termasuk saat "Coba lagi") supaya halaman ini bisa lacak benar/salah per step tanpa `QuestionCheck` sendiri perlu tahu dia ada di dalam sesi multi-soal. Tombol "Lanjut"/"Lihat ringkasan" baru muncul setelah step berjalan dijawab. Ringkasan akhir: jumlah concept unik + rasio soal benar (bukan attempt row, bukan skor formal — sama persis prinsip P3-001). Entry point: kartu CTA baru "Personal Review" di atas daftar Latihan yang sudah ada (P4-002), tautan `Link` ke halaman baru.

**1 bug nyata ditemukan lewat verifikasi browser** (bukan cuma "kelihatannya jalan"): 2 tombol baru (`render={<Link>...}`) memicu warning base-ui `nativeButton` di console ("expected a native <button>... Rendering a non-<button> removes native button semantics") — pola `render={<Link/>}` sudah dipakai di 4 tempat lain proyek ini (`app/page.tsx`, `beranda/page.tsx`), semuanya SUDAH benar pakai `nativeButton={false}`, cuma 2 pemakaian baru ticket ini yang kelewatan. Diperbaiki, diverifikasi ulang lewat log dev server (`grep nativeButton` — 0 match setelah fix, ada sebelum fix).

**Diverifikasi end-to-end 2x lewat `Bun.WebView`** (Bun 1.4's browser-automation baru, native — bukan paket `playwright` eksternal yang dipakai sesi-sesi FE sebelumnya, lihat catatan di bawah): seed 3 concept demo lemah + 1 soal per concept, buka Latihan, klik CTA "Personal Review", jawab ketiga soal berurutan (dapat "Benar!" tiap step), sampai ringkasan "3 konsep dikerjakan · 3 dari 3 soal benar". Nol JS error. **Temuan menarik selama verifikasi**: run kedua (ulang persis skenario yang sama tanpa reseed) balik "Belum ada yang perlu direview" — BUKAN bug, ini bukti efek samping asli: `/questions/{id}/check` run pertama benar-benar memicu `masteryService.recomputeForConcept` lewat learning_event baru, mastery concept-concept demo itu jadi `score:100, confidence:0.2` (baru 1 dari `N_min=5` attempt) — di bawah `masteryConfidenceThreshold`, jadi tidak lagi lolos gate `findWeak` P4-002. Reseed data lalu ulang → lulus lagi. Data demo dihapus total setelah selesai (subject/concept/question/masteries/frss_schedule/learning_events/refresh_token, throwaway murni).

**Catatan tooling (di luar ticket ini, permintaan eksplisit user)**: mulai sesi ini, verifikasi browser FE pakai `Bun.WebView` (`new Bun.WebView({headless:true})`, `navigate`/`click`/`evaluate`/`screenshot`/`cdp`) — bawaan Bun 1.4, bukan lagi `npm install playwright` di scratchpad. LocalStorage auth-token injection (dipakai tiap verifikasi FE sejak P3-002) sekarang lewat CDP `Page.addScriptToEvaluateOnNewDocument` (butuh 1x `navigate("about:blank")` dulu buat buka sesi CDP, baru daftar script-nya, baru navigate ke URL asli — beda dari Playwright's `addInitScript` yang tidak butuh langkah pemanasan itu). Tidak ada dependency baru ditambahkan ke `package.json` manapun — murni skrip verifikasi scratchpad, jadi tidak ada perubahan repo untuk ini.

### P4-005 — Integration test suite + exit checkpoint
**Status:** done (2026-09-02, `titian-backend-bun` + `titian-web`) — **Phase 4 CLOSED, semua 5 ticket done, semua 5 checkpoint tercentang**
**Depends on:** semua di atas
**Deskripsi:** Sama pola seperti P1-013/P2-017/P3-005 — cross-check semua endpoint baru Phase 4 punya test, plus checkpoint yang sudah tertulis persis di dokumen sumber.
**Acceptance Criteria:**
- [x] Semua route baru P4-001 s/d P4-003 punya minimal 1 integration test HTTP-level — cross-check `grep`-based (persis pola P2-017/P3-005), jangan asumsi "kodenya ada pasti sudah dites"
- [x] Checkpoint end-to-end (dari sumber, dipakai apa adanya): "setelah user mengerjakan 10 soal dari 3 concept berbeda, `/learning-queue` (pengganti `/review-queue` buat kasus ini) mengembalikan urutan yang masuk akal (concept lemah muncul duluan)" — dites dengan skenario buatan (3 concept, skor sengaja dibuat beda-beda lewat `/questions/{id}/check`), bukan cuma cek "kodenya ada"
**DoD:** `bun test` hijau di `titian-backend-bun` (lokal — CI masih P0-010 yang tertunda).

**Catatan implementasi:** Route-coverage audit (skrip Python, pola persis P2-017/P3-005) atas semua 71 route di `app.ts` vs `tests/*.test.ts` — **0 gap ditemukan**, masuk akal karena tiap route baru P4-001 s/d P4-004 memang sudah dites langsung sewaktu ticket-nya sendiri dikerjakan (pola sama seperti P3-005, beda dari P2-017 yang nemu 20+ gap nyata sisa migrasi). Checkpoint end-to-end baru (`tests/phase4-checkpoint.test.ts`) — skenario persis dari sumber: 3 concept (4+3+3=10 soal), dijawab lewat `POST /questions/{id}/check` asli dengan rasio benar berbeda (0/4, 1/3, 3/3), `GET /learning-queue` dicek balikin urutan `[concept paling lemah, concept agak lemah]` dengan concept kuat (100% benar) tidak muncul sama sekali. Total sekarang **224/224 test lulus**.

**1 gap checkpoint nyata ditemukan saat menutup fase ini** (bukan diasumsikan beres): checkpoint poin 1 ("drill-down mastery ... lewat UI") ternyata belum bisa didemo — P4-001 sendiri cuma dibangun backend+test, tidak ada FE yang pernah memanggil `GET /concepts/{id}/mastery-breakdown`. Ditutup sekarang, bukan ditunda: halaman Progres (`titian-web`) dapat `MasteryBreakdownDialog` baru — tiap baris `MasteryBars` sekarang bisa diklik, buka dialog yang render tree drill-down 2 level dengan flag lemah (ikon+warna merah), reuse `GET /concepts/{id}/mastery-breakdown` yang sudah ada dari P4-001. Tidak ada endpoint backend baru untuk ini.

**Semua 5 poin checkpoint diverifikasi ulang, bukan diasumsikan dari ticket sebelumnya:**
1. **Drill-down mastery lewat UI** — diverifikasi lewat `Bun.WebView`: seed hierarchy 3 level nyata (Grammar 71% → Present Simple 61% → Questions 49%, persis contoh dari roadmap sendiri), buka Progres, klik baris "Grammar", dialog terbuka nampilin ketiga level dengan "Questions" ditandai merah+ikon peringatan. Screenshot dicek visual, bukan cuma teks.
2. **Tombol Review di Latihan** — sudah diverifikasi penuh di P4-002's sesi sendiri (lihat "Catatan implementasi" P4-002).
3. **Prerequisite API + cycle rejection** — sudah diverifikasi penuh lewat 11 test HTTP-level di P4-003 (self-loop, siklus langsung, siklus transitif, semuanya ditolak `422`).
4. **Personal Review packet end-to-end** — sudah diverifikasi penuh lewat `Bun.WebView` di P4-004's sesi sendiri (3 concept, ringkasan akhir benar).
5. **Checkpoint asli roadmap** — `tests/phase4-checkpoint.test.ts` baru (lihat atas), plus dikonfirmasi manual lewat skenario yang sama persis di sesi verifikasi P4-002 (concept `critical` muncul sebelum `weak`).

Semua 5 poin tercentang — **Phase 4 resmi ditutup**.

---

## Checkpoint keluar Phase 4 (harus bisa didemo, bukan asumsi) — 🟢 SEMUA TERCENTANG (2026-09-02)
1. [x] Siswa buka drill-down mastery 1 concept (misal "Grammar"), lihat sub-concept yang ditandai lemah — lewat UI, bukan cuma response JSON mentah. **Bukti**: `MasteryBreakdownDialog` baru (P4-005), diverifikasi lewat `Bun.WebView` — lihat P4-005's "Catatan implementasi".
2. [x] Siswa buka Latihan, tombol "Review" **benar-benar jalan** (bukan dekoratif seperti sekarang) — klik buka sesi review, jawab, dapat feedback benar/salah — lewat `QuestionCheck` yang sudah ada. **Bukti**: P4-002's "Catatan implementasi".
3. [x] Admin/curriculum_developer bisa menautkan 1 concept sebagai prasyarat concept lain lewat API, siklus (langsung maupun 2-hop) ditolak jelas. **Bukti**: P4-003's "Catatan implementasi", 11 test HTTP-level.
4. [x] Siswa kerjakan 1 "Personal Review" packet dari awal sampai ringkasan akhir, lintas beberapa concept dalam 1 sesi. **Bukti**: P4-004's "Catatan implementasi".
5. [x] Checkpoint asli dari roadmap: 10 soal dikerjakan lintas 3 concept berbeda → `/learning-queue` menunjukkan concept lemah duluan. **Bukti**: `tests/phase4-checkpoint.test.ts` (P4-005).

Kalau salah satu poin di atas belum jalan end-to-end, jangan lanjut ke ticket berikutnya (§3.3/3.4/3.7 atau roadmap-Fase-4 lanjutan) walau ticket lain kelihatan sudah "done" — sama semangatnya dengan aturan yang sama di checkpoint Phase 1/2/3.

---

## Strategi eksekusi (urutan sesi yang disarankan)

| Sesi | Ticket | Fokus | Kenapa dikelompokkan begini |
|---|---|---|---|
| 1 | P4-001 | Weakness detection drill-down (backend) | Fondasi — P4-002's definisi "lemah" dipakai ulang dari sini, bukan didefinisikan dua kali. |
| 2 | P4-002 | Personal Learning Queue + wire tombol Review (backend+FE) | Baru masuk akal setelah P4-001 ada. Ini juga yang pertama kali bikin Latihan benar-benar interaktif, bukan cuma daftar. |
| 3 | P4-003 | Knowledge Graph / prerequisite (backend) | Independen dari P4-002/004 — bisa duluan atau belakangan, ditaruh sesi 3 karena breakdown sumber menaruhnya setelah 3.6. |
| 4 | P4-004 | Lesson Packet (FE) | Reuse `GET /learning-queue` dari sesi 2 — murni cara presentasi baru, bukan data baru. |
| 5 | P4-005 | Test suite + checkpoint | Sama pola P1-013/P2-017/P3-005 — penutup fase. |

**Total 5 sesi** — sama ukurannya dengan ticket-Phase-3, scope-nya sengaja dipersempit ke 4 item MVP-first pertama roadmap-Fase-3 (bukan semua 9 item §3.1-3.9) lewat alasan yang sudah dijelaskan di "Keputusan scope".
