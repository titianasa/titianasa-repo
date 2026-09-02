# Phase 5 — Core Learning Loop, roadmap-Fase-3's last loose ends

Depends on: Phase 4 checkpoint terpenuhi penuh (lihat `docs/tickets/phase-4.md` — semua 5 ticket + 5 checkpoint done, 224 test lulus di `titian-backend-bun`, 2026-09-02).

Sumber utama breakdown ini: `agent/ALR_Phase_Detail_Breakdown.md`'s `## PHASE 3 — Core Learning Loop` (§3.4, §3.2's sisa). Angka "Phase 5" di nama file ini **tetap murni urutan sesi kerja** (lihat pola yang sama di `phase-4.md`'s "Keputusan scope") — bukan roadmap-Fase-5 ("Assessment / Exam Engine", dokumen sendiri di `ALR_Phase_Detail_Breakdown.md` baris 482+), yang **tidak disentuh sama sekali** di ticket ini.

## Keputusan scope (baca duluan)

Setelah Phase 4 ditutup, user ditanya prioritas berikutnya lewat riset + `AskUserQuestion` (3 opsi: selesaikan sisa roadmap-Fase-3 / Speaking+AI Tutor roadmap-Fase-4 / Assessment-Exam-Engine roadmap-Fase-5). **User pilih opsi pertama** — sengaja yang paling kecil dan aman, murni pakai infra yang sudah ada, tidak butuh ADR baru atau keputusan provider AI baru.

Isi ticket ini persis 2 item nyata yang tersisa dari `docs/tickets/phase-4.md`'s "Keputusan scope" sendiri (yang sebelumnya ditunda ke sesi berikutnya):
- **§3.4 Retrieval Variation** — review tidak boleh selalu bentuk soal yang sama.
- **Integrasi nyata `concept_prerequisites`** (P4-003) ke `/learning-queue` — API-nya sudah ada sejak P4-003, tapi **belum pernah dipakai oleh kode manapun** sejak dibangun (dikonfirmasi: 0 baris di tabel `concept_prerequisites` di database dev, dan tidak ada satu pun pemanggil `findPrerequisites`/`findDependents` di luar test-nya sendiri).

**§3.3 (Forgetfulness Score) dan §3.7 (Mistake Bank) TETAP ditunda** — dicek ulang langsung ke database dev sesi ini (bukan diasumsikan dari sesi lalu): `learning_events` cuma 15 baris, dan **0 pasang (user, concept)** yang tembus `masteryNMin=5` (maksimum baru 1 event per pasang). Kedua fitur itu secara desain butuh data historis riil buat berguna ("rate of decay per user-concept", "frekuensi kesalahan per jenis") — belum ada sinyal apa pun buat dibangun sekarang, bukan soal effort implementasi.

**§3.8 (5 Jenis AI Intervention) dan §3.9 (AI vs Human Trigger) TETAP ditunda** — alasan sama seperti keputusan `phase-4.md`: §3.9 eksplisit butuh ADR baru, keduanya terhubung ke fase lain (marketplace/tutor, roadmap-Fase-8) yang belum dibangun.

Dengan ini, **seluruh roadmap-Fase-3 (§3.1-§3.9) akan selesai** setelah ticket ini ditutup, kecuali 4 item yang eksplisit ditunda di atas (§3.3/3.7/3.8/3.9) — semuanya karena alasan struktural (data historis belum ada / butuh ADR / terhubung fase belum dibangun), bukan diabaikan begitu saja.

## Temuan riset

- **`frss_repository.findSuggestedQuestionIds(db, conceptId, limit)`** (`src/repository/frss_repository.ts`) — dipakai `frss_service.getReviewQueue` DAN `learning_queue_service.getLearningQueue` (P4-002) — saat ini murni `ORDER BY questions.id LIMIT n`, **tidak tahu tipe soal apa yang barusan dijawab user untuk concept itu**. Tidak ada state/riwayat tipe apa pun yang dibaca — persis masalah yang §3.4 gambarkan ("review berikutnya tidak boleh selalu bentuk yang sama").
- **`learning_events`** (schema `src/db/schema.ts:392-409`) sudah punya semua yang dibutuhkan buat tahu "tipe soal apa yang terakhir dijawab user untuk concept X": `entityType='question'` + `entityId` (question id, join ke `questions.type`) + `eventType='question_answered'`, filter concept lewat `question_concepts`. Query-nya mirror persis `mastery_repository.findEventsForConcept`'s join pattern yang sudah ada — tidak perlu tabel baru.
- **`concept_repository.findPrerequisites`/`findDependents`** (P4-003) sudah ada dan sudah teruji (11 test), tapi **nol pemanggil produksi** — dikonfirmasi lewat grep, cuma dipanggil dari `concept_service.listPrerequisites`/`addPrerequisite`, yang cuma dipanggil dari `concept_handler.ts`'s 3 route CRUD-nya sendiri. Tidak ada satu pun service lain (termasuk `learning_queue_service.ts`) yang membaca prerequisite graph ini buat pengambilan keputusan apa pun.
- **`learning_queue_service.getLearningQueue`** (P4-002, `src/service/learning_queue_service.ts`) menggabung due (`frssRepository.findDue`) + lemah (`masteryRepository.findWeak`) jadi 3 bucket (`critical`/`due`/`weak`), tapi **buta terhadap prerequisite** — concept yang lemah bisa saja punya prerequisite yang JAUH lebih lemah (atau belum pernah disentuh sama sekali), dan queue saat ini tidak pernah mempertimbangkan itu. Secara pedagogis, merekomendasikan review ke concept yang prasyaratnya sendiri belum kuat itu kontraproduktif — user akan terus gagal di concept lanjutan sampai prasyaratnya dibereskan duluan.
- **ADR-0007 guard tetap berlaku** (`docs/STATE.md`): kedua ticket di bawah ini **tidak mengubah semantik** `parent_concept_id` (containment) ataupun `concept_prerequisites` (prerequisite graph) — cuma membaca graph yang sudah ada buat keputusan ranking/seleksi. Tidak butuh ADR baru.

## Ticket

### P5-001 — Retrieval Variation: FRSS scheduler pilih tipe soal berbeda tiap due-review (§3.4)
**Status:** done (2026-09-02, `titian-backend-bun`)
**Depends on:** P3-001 (grading/learning_events), P4-002 (`findSuggestedQuestionIds` dipakai `/learning-queue`)
**Endpoint baru:** tidak ada — mengubah behavior internal `frss_repository.findSuggestedQuestionIds` yang dipakai `GET /review-queue` dan `GET /learning-queue` yang sudah ada.
**Deskripsi:** §3.4 — kalau sebuah concept punya lebih dari 1 tipe soal terdaftar (mcq/fill_blank/matching), urutan/pilihan soal yang disarankan untuk direview tidak boleh selalu didominasi tipe yang sama dengan review user itu yang paling akhir untuk concept tersebut.
**Acceptance Criteria:**
- [x] `frss_repository` dapat fungsi baru `findLastAnsweredQuestionType(db, userId, conceptId)` — query `learning_events` (`event_type='question_answered'`, `entity_type='question'`) join `questions`+`question_concepts`, `ORDER BY created_at DESC LIMIT 1`, balikin `type` (atau `undefined` kalau belum pernah ada riwayat)
- [x] `findSuggestedQuestionIds` dapat parameter `userId` baru (dipakai kedua caller-nya) — kalau concept itu punya soal dengan tipe LAIN dari `findLastAnsweredQuestionType`'s hasil, prioritaskan tipe yang berbeda itu duluan di hasil; kalau cuma ada 1 tipe soal terdaftar untuk concept itu (atau belum ada riwayat sama sekali), behavior lama (`ORDER BY id`) tetap berlaku apa adanya — **tidak ada regresi buat concept single-type**
- [x] `frss_service.getReviewQueue` dan `learning_queue_service.getLearningQueue` (P4-002) diupdate meneruskan `userId` ke pemanggilan baru ini
**DoD:** test backend baru (`retrieval-variation.test.ts`) — concept dengan 2 soal tipe berbeda (mcq + fill_blank), user jawab tipe mcq duluan, assert saran berikutnya memprioritaskan fill_blank; concept single-type tidak berubah behavior-nya (regression check eksplisit); concept tanpa riwayat sama sekali tidak error.

**Catatan implementasi:** `findLastAnsweredQuestionType` mirror persis join pattern `mastery_repository.findEventsForConcept` (`learning_events` → `question_concepts` on `entity_id`), ditambah join `questions` buat ambil `type`. `findSuggestedQuestionIds` sekarang ambil SEMUA soal published buat concept itu dulu (bukan `LIMIT` di query SQL), cek `distinctTypes.size <= 1` (short-circuit ke behavior lama persis kalau cuma 1 tipe — regresi nol buat kasus mayoritas saat ini), baru kalau >1 tipe DAN ada riwayat, partition jadi "beda tipe" (duluan) + "tipe sama" (belakangan), masing-masing tetap `ORDER BY id` di dalam partisinya, baru `slice(0, limit)`. `frss_service.getReviewQueue` dan `learning_queue_service.getLearningQueue` (P4-002) diupdate meneruskan `userId` — perubahan sinyal minimal, tidak ada endpoint/response shape yang berubah.

**1 isu test-environment nyata ditemukan+diperbaiki**: test awal buat "urutan berdasar waktu terbaru" pakai 2 panggilan `/questions/{id}/check` berurutan + `Bun.sleep()` di antaranya, tapi GAGAL — ternyata Postgres's `now()` (yang dipakai `defaultNow()`) **dibekukan di awal transaksi**, bukan per-statement, dan `withTx` (isolasi test standar proyek ini) membungkus 1 test dalam 1 transaksi — jadi 2 event yang "berurutan" secara kode tetap dapat `created_at` yang identik. Di produksi ini tidak masalah (2 request nyata = 2 transaksi terpisah = timestamp beda beneran) — murni keterbatasan harness test. Diperbaiki: test itu insert 2 `learning_events` langsung lewat drizzle dengan `createdAt` eksplisit berbeda, bukan lewat 2 panggilan API berurutan.

Diverifikasi lewat 5 test baru (`retrieval-variation.test.ts`) — semua terhadap Postgres asli lewat `withTx` (bukan mock), termasuk skenario nyata lewat `POST /questions/{id}/check` asli (bukan cuma unit test pure-logic). Total sekarang **255/255 test lulus**. Tidak ada endpoint baru yang butuh verifikasi browser — perubahan internal murni ke behavior `/review-queue`/`/learning-queue` yang sudah ada.

### P5-002 — Concept prerequisite dipakai nyata: `/learning-queue` jadi prerequisite-aware (menutup gap P4-003)
**Status:** done (2026-09-02, `titian-backend-bun`)
**Depends on:** P4-002 (`learning_queue_service.ts`), P4-003 (`concept_repository.findPrerequisites`)
**Endpoint baru:** tidak ada — mengubah behavior `GET /learning-queue` yang sudah ada (field baru ditambahkan ke tiap item, bukan endpoint baru).
**Deskripsi:** Concept yang masuk kategori `weak`/`critical` di `/learning-queue`, kalau salah satu prerequisite langsungnya (1 level, sesuai desain P4-003) juga lemah atau belum pernah disentuh, prasyaratnya itu yang harus diprioritaskan direview duluan — bukan concept lanjutannya. Ini bukan fitur baru dari nol, ini menyambungkan 2 hal yang sudah ada (`concept_prerequisites` API dari P4-003, ranking `/learning-queue` dari P4-002) yang sejak awal memang dirancang saling berkaitan tapi belum pernah benar-benar disambung.
**Acceptance Criteria:**
- [x] `learning_queue_service.getLearningQueue` — untuk tiap concept kandidat (due/weak), cek `concept_repository.findPrerequisites` (1 level, bukan rekursif — konsisten sama batas MVP P4-003)
- [x] Kalau ada prerequisite yang mastery-nya juga di bawah `weaknessScoreThreshold` (atau belum ada data sama sekali), prerequisite itu ditambahkan/dinaikkan ke prioritas `critical` (sinyal "harus dibereskan duluan"), dan item asalnya dapat penanda baru `blocked_by_concept_id` di response — **bukan disembunyikan**, cuma diberi sinyal urutan yang benar (siswa tetap bisa lihat kedua-duanya)
- [x] Concept tanpa prerequisite (kasus mayoritas saat ini, karena `concept_prerequisites` masih kosong di data manapun) — behavior `/learning-queue` **identik** dengan sebelum ticket ini, dikonfirmasi lewat regresi eksplisit di test (semua test P4-002 yang sudah ada tetap lulus tanpa ubah)
- [x] Tidak ada rekursi tak terbatas — 1 level saja, sama sekali tidak mencoba jalan sampai prerequisite-of-prerequisite (kalau nanti dibutuhkan, itu perluasan terpisah, bukan bagian ticket ini)
**DoD:** test backend baru (`learning-queue-prerequisites.test.ts`) — concept lemah dengan prerequisite yang juga lemah → prerequisite naik jadi `critical` + `blocked_by_concept_id` muncul di item asalnya; concept lemah dengan prerequisite yang SUDAH kuat → tidak ada perubahan prioritas; concept tanpa prerequisite sama sekali → identik P4-002. Semua test `learning-queue.test.ts` (P4-002) yang sudah ada tetap lulus tanpa modifikasi.

**Catatan implementasi:** ditambah 1 pass baru di `getLearningQueue`, setelah `due`+`weak` digabung tapi sebelum sort+slice — ambil snapshot entry yang priority-nya `weak`/`critical`, buat tiap satu cek `findPrerequisites` (1 level), lalu cek mastery prerequisite itu lewat `masteryRepository.find` (bukan `findWeak`, karena butuh single-lookup termasuk kasus "belum ada row sama sekali" — `findWeak` cuma balikin yang confidence-nya sudah cukup, tidak membedakan "belum ada data" dari "confidence rendah"). Snapshot diambil SEBELUM pass ini memodifikasi map — jadi entry prerequisite yang baru ditambahkan tidak pernah ikut di-walk buat prerequisite-nya sendiri, menegakkan batas 1-level tanpa perlu guard eksplisit. Kalau prerequisite punya >1 (jarang di MVP ini), cuma prerequisite pertama yang qualify yang dipakai buat `blocked_by_concept_id` (field-nya singular, sesuai AC) — `break` setelah match pertama. Tidak ada perubahan skema DB atau endpoint baru, cuma 1 field opsional baru (`blocked_by_concept_id`) di response `/learning-queue` yang sudah ada.

4 test baru (`learning-queue-prerequisites.test.ts`): weak+weak prerequisite → escalate+marker; weak+strong prerequisite → tidak ada perubahan; weak+prerequisite tanpa data mastery sama sekali → escalate juga (kasus "atau belum ada data" di AC); concept tanpa prerequisite edge sama sekali → tidak ada `blocked_by_concept_id`. `learning-queue.test.ts` (P4-002) dan `concept-prerequisites.test.ts` (P4-003) dijalankan ulang tanpa modifikasi — tetap lulus, regresi nol dikonfirmasi bukan diasumsikan. Total sekarang **259/259 test lulus**. Tidak ada endpoint baru yang butuh verifikasi browser — perubahan internal murni ke `GET /learning-queue` yang sudah ada, sama alasannya dengan P5-001.

### P5-003 — Integration test suite + exit checkpoint
**Status:** todo
**Depends on:** P5-001, P5-002
**Deskripsi:** Pola sama seperti P1-013/P2-017/P3-005/P4-005 — cross-check semua behavior baru punya test, plus 1 checkpoint end-to-end yang menyatukan kedua ticket di atas dalam 1 skenario nyata (tidak ada checkpoint eksplisit dari sumber untuk kombinasi §3.4+prerequisite-integration ini, jadi ditulis sendiri berdasarkan behavior yang benar-benar dibangun, bukan diasumsikan).
**Acceptance Criteria:**
- [ ] Route-coverage audit (`grep`-based, pola P2-017/P3-005/P4-005) — pastikan tidak ada route yang berubah behavior-nya tanpa test yang benar-benar meng-cover perubahan itu
- [ ] Checkpoint baru: user seed 2 concept — "Verb To Be" (prerequisite) dan "Present Simple" (dependent, prerequisite-nya "Verb To Be"). Jawab beberapa soal Present Simple sampai lemah, TANPA pernah menyentuh Verb To Be sama sekali. `GET /learning-queue` harus menunjukkan Verb To Be dengan prioritas `critical` dan `blocked_by_concept_id` muncul di item Present Simple, menunjuk ke Verb To Be. Lalu jawab beberapa soal Verb To Be dengan tipe yang sama berulang-ulang — assert soal yang disarankan berikutnya untuk concept itu bervariasi tipe-nya, bukan tipe yang sama terus (retrieval variation nyata jalan di alur yang sama).
**DoD:** `bun test` hijau penuh di `titian-backend-bun` (lokal — CI masih P0-010 yang tertunda).

---

## Checkpoint keluar Phase 5 (harus bisa didemo, bukan asumsi)
1. [ ] Concept dengan >1 tipe soal terdaftar, direview berkali-kali oleh user yang sama — tipe soal yang disarankan bervariasi, tidak macet di 1 tipe terus, dibuktikan lewat test bukan cuma baca kode.
2. [ ] Concept dengan prerequisite yang lemah/belum disentuh — `/learning-queue` menaikkan prioritas prerequisite itu di atas concept lanjutannya, dan item lanjutannya dapat penanda `blocked_by_concept_id`.
3. [ ] Concept tanpa prerequisite sama sekali (mayoritas data saat ini) — `/learning-queue` behave identik seperti sebelum Phase 5, dikonfirmasi lewat regresi test P4-002 yang tidak diubah sama sekali.
4. [ ] Seluruh roadmap-Fase-3 (§3.1-§3.9) resmi ditutup, kecuali §3.3/3.7 (butuh data historis, belum ada sinyal) dan §3.8/3.9 (butuh ADR baru + fase lain yang belum dibangun) — didokumentasikan eksplisit sebagai deferred, bukan didiamkan.

Kalau salah satu poin di atas belum jalan end-to-end, jangan lanjut ke prioritas berikutnya (Speaking+AI Tutor atau Assessment/Exam Engine, dua opsi yang tidak dipilih user di sesi ini) walau ticket lain kelihatan sudah "done" — sama semangatnya dengan aturan checkpoint di Phase 1-4.

---

## Strategi eksekusi (urutan sesi yang disarankan)

| Sesi | Ticket | Fokus | Kenapa dikelompokkan begini |
|---|---|---|---|
| 1 | P5-001 | Retrieval Variation (backend) | Independen dari P5-002 — bisa duluan atau belakangan, tapi ditaruh duluan karena scope-nya lebih sempit (1 fungsi repository + 1 perubahan kecil di 2 caller). |
| 2 | P5-002 | Prerequisite-aware `/learning-queue` (backend) | Menyambungkan P4-002+P4-003 — baru masuk akal setelah keduanya (sudah done sejak Phase 4). |
| 3 | P5-003 | Test suite + checkpoint | Sama pola P1-013/P2-017/P3-005/P4-005 — penutup fase, sekaligus menutup seluruh roadmap-Fase-3. |

**Total 3 sesi** — scope paling kecil dari semua ticket-Phase sejauh ini, sesuai keputusan eksplisit user memilih opsi paling kecil dan aman setelah ditawari 3 pilihan (yang lain: Speaking+AI Tutor, Assessment/Exam Engine — keduanya butuh keputusan arsitektur besar/ADR baru, sengaja ditunda).
