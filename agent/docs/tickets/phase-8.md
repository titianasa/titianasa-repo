# Phase 8 — Gamification (roadmap-Fase-6, learner-facing engagement core)

Depends on: `learning_events`/`masteries`/`frss_schedule` (Phase 1), `question_service.checkAnswer` (P3-001), `assessment_service.submitAttempt` (Phase 1), `ai_writing_evaluation_service`/`ai_speaking_evaluation_service` (P3-004/P6-002), `level_assessment_scoring_service` (P7-003), `questions.skill_category` (P7-002, reused here to map an answered question to its XP-earning category).

Sumber utama breakdown ini: `agent/ALR_Phase_Detail_Breakdown.md`'s `## PHASE 6 — Gamification & Economy` (§6.1-§6.16), dan `agent/ALR_Build_Roadmap.md`'s `## FASE 6 — Gamification & Economy`.

## Keputusan scope (baca duluan)

Setelah Phase 7 (Assessment/Exam Engine) ditutup, user diminta lanjut ke kandidat berikutnya di roadmap artifact — **Gamification & Economy (roadmap-Fase 6)**. Beda dari transisi Phase 5→6→7 sebelumnya, tidak ada keputusan arsitektur yang menurut dokumen sumbernya sendiri **wajib** ADR dulu (beda dari P7's bobot skor) — jadi ticket-phase ini langsung ditulis dari riset, tanpa `AskUserQuestion` tambahan, konsisten pola "kalau tidak ada gerbang eksplisit di sumber, riset + tulis ticket file dulu" yang dipakai Phase 4.

**§6.1-§6.8 (mekanik engagement inti) masuk scope ticket-phase ini. §6.9-§6.16 (model bisnis: subscription tier, Diamond framing UI, funnel iklan, wallet tutor marketplace) SENGAJA TIDAK TERMASUK** — alasan konkret per item, bukan cuma "nanti":
- **§6.9-§6.11 (Diamond framing, free-tier ad-gating)** — mekanisme charge-kredit-nya SUDAH ADA sejak P1-011 (`ai_gateway_service.ts` cek+charge kredit sebelum panggil provider). Yang belum ada murni *framing produk* (copy UI "💎 5 Diamonds" vs "5 credits") dan integrasi SDK iklan (`🎬 Watch Ad`) — bukan pekerjaan backend, dan iklan butuh keputusan vendor yang belum diambil.
- **§6.12-§6.13 (pricing table, subscription tier)** — draft di §6.12 sendiri sudah ditandai sumbernya sebagai **disuperseded ADR-0005**; §6.13 (tier Free/Plus/Pro, allowance bulanan) butuh integrasi payment yang belum ada dan keputusan harga bisnis yang bukan keputusan teknis sesi ini.
- **§6.9 wallet tutor / marketplace split 30/70** — depends langsung ke roadmap-Fase-8 (Organization/LMS/Marketplace), yang belum ada satu baris kode pun (tidak ada entitas tutor/booking sama sekali). ADR-0005 sendiri sudah mencatat "Wallet tutor (Phase 7 [lama]/marketplace)" sebagai depends-on terpisah — bukan sesuatu yang bisa dibangun sekarang tanpa entitas yang jadi sandarannya.
- **§6.6 (Kids Gamification reskin — "English Island")** — eksplisit di dokumen sumbernya sendiri "hanya presentation layer" (FE murni, tidak ada backend baru sama sekali) — dan `ALR_Phase_Detail_Breakdown.md` sendiri belum eksplisit dari user bahwa Kids Mode adalah target sekarang (poin yang sama juga dicatat sebagai alasan penundaan §4.4 di Phase 6/ticket-phase lama). Ditunda, bukan dianggap bagian dari "gamification core".
- **§6.16 (cron expiry credit)** — ini follow-up ADR-0005 (Economy, bukan Gamification), dan backend ini belum punya infrastruktur job/cron sama sekali (P0-010 CI juga belum jalan) — 1 baris di "Item lepas" `STATE.md`, bukan ticket Phase 8.

**Prinsip keras dari §6.1, ditegakkan eksplisit di tiap ticket di bawah**: XP/Streak/Achievement/League **tidak pernah** masuk formula `mastery.compute` (ADR-0002) atau `frss.apply` (ADR-0003) — read-only terhadap `learning_events`/`masteries`, tidak pernah menulis ke tabel itu. Pelanggaran ini butuh ADR baru yang men-supersede ADR-0002/0003 secara eksplisit — dicatat juga sebagai guard baru di `docs/STATE.md`.

**1 temuan nyata dari riset** (pola sama tiap ticket-phase — cek kode dulu, bukan asumsi dari dokumen): `POST /questions/{id}/check` (inline, dalam lesson), `POST /attempts/{id}/submit` (assessment/level_assessment), **dan** jalur lesson-attempt writing/speaking (`submitWritingAttempt`/`submitSpeakingAttempt`) — nol dari 3 jalur "submit" ini punya satu titik kait bersama; malah writing/speaking lesson attempt **tidak pernah menulis `learning_events` sama sekali** (beda dari checkAnswer/submitAttempt/level_assessment yang selalu menulis). Ini bukan bug yang perlu diperbaiki di ticket-phase ini (mastery/FRSS untuk writing/speaking lesson attempt memang sengaja tidak granular per-concept, karena tidak ada `question_concepts` link untuk prompt lesson penuh) — tapi berarti XP-awarding **tidak bisa** cukup hook ke `learning_events` saja; perlu hook eksplisit ke SEMUA 5 titik submit (P8-001 detail).

## Ticket

### P8-001 — XP system: ledger + earning triggers (§6.1, §6.2)
**Status:** done (2026-09-02, `titian-backend-bun`)
**Depends on:** -
**Endpoint baru:** `GET /me/xp` (total + riwayat ringkas).
**Deskripsi:** Metrik ke-2 yang terpisah total dari Mastery (§6.1) — reward loop, bukan kemampuan. Mirror arsitektur `credits`(agregat)/`transactions`(ledger) ADR-0005 persis: `xp_events` (ledger append-only, 1 baris per aksi) + `user_xp` (agregat cache, 1 baris per user, `balance` = SUM cepat tanpa scan ledger tiap baca).
**Acceptance Criteria:**
- [x] Migrasi baru: `xp_events` (`id`, `user_id`, `amount`, `reason` text, `reference` text nullable UNIQUE, `created_at`) + `user_xp` (`user_id` PK, `total` bigint, `updated_at`) — additive, tidak menyentuh `masteries`/`learning_events`
- [x] `xp_service.awardXp(db, userId, amount, reason, reference)` — insert `xp_events` + upsert `user_xp.total` dalam 1 transaksi DB, idempotent terhadap `reference` yang sama (dipanggil 2x dengan `reference` sama = no-op ke-2, mencegah double-award kalau caller retry)
- [x] Hook di **kelima** titik submit (bukan cuma yang nulis `learning_events`): `question_handler.postCheck` (setelah `checkAnswer` sukses — amount dari `question.skillCategory` kalau ada, fallback jumlah generik kalau NULL), `assessment_handler.postSubmit`'s 3 cabang (`assessmentService.submitAttempt` biasa, `levelAssessmentScoringService.submitLevelAssessmentAttempt`, DAN cabang lesson writing/speaking) — semua di level HANDLER (pola sama P7-001/P7-003), nol perubahan ke service scoring manapun
- [x] Tabel jumlah XP (§6.2, didokumentasikan eksplisit sebagai default yang bisa di-tuning, bukan final bisnis — sesuai catatan dokumen sumber sendiri "final angka lewat tuning"): vocabulary 5, grammar/reading/listening 10, speaking/pronunciation 15, writing 20, soal tanpa `skill_category` 5, `unit_test` 20, `mock_exam`/`level_assessment` 30
- [x] `GET /me/xp` balikin `{total, recent: [{amount, reason, created_at}]}`
**DoD:** test backend baru — jawab soal lewat `/check` → `user_xp.total` naik sesuai `skill_category`; submit assessment → XP sesuai jenis assessment; submit writing/speaking lesson attempt → XP sesuai (menutup gap "tidak ada `learning_events`" di atas, XP tetap jalan lewat hook handler); panggilan `awardXp` dengan `reference` sama 2x → cuma 1 XP masuk. Regression: `assessment.test.ts`/`ai-writing-evaluation.test.ts`/`ai-speaking-evaluation.test.ts`/`level-assessment-scoring.test.ts` tetap lulus tanpa modifikasi (nol service scoring disentuh).

**Catatan implementasi:** `xp_repository.award` (bukan `xp_service`) yang pegang transaksi DB-nya — persis pola `economy_repository.charge`, dipilih setelah `tsc` menolak meneruskan `tx` (tipe `PgTransaction`) ke fungsi repository lain yang menerima `Db` biasa (2 tipe tidak compatible di driver `bun-sql`). Idempotency pakai `ON CONFLICT DO NOTHING` di kolom `reference` (UNIQUE) — NULL tidak pernah collide (semantik SQL standar), jadi caller yang sengaja tidak kasih `reference` (jalur `/check`, karena praktik berulang atas soal yang sama itu SAH dan memang harus dapat XP lagi tiap kali) otomatis tidak pernah di-dedupe, tanpa butuh logic tambahan. Caller yang PUNYA kunci alami 1x-submit (assessment/level_assessment/writing/speaking — semua dijaga `loadSubmittableAttempt`'s status check supaya tidak bisa disubmit ulang) pakai `reference = "attempt:{attemptId}"`.

`question_service.checkAnswer`'s `CheckAnswerResult` dapat field baru `skillCategory` (dari `Question` row yang sudah di-load, bukan query kedua) — dipakai handler buat pilih jumlah XP tanpa round-trip DB tambahan; tidak diekspos ke response publik `/check` (field internal antara service→handler saja). XP diberikan untuk writing/speaking lesson attempt SEGERA setelah submission sukses, **TIDAK digantung ke keberhasilan evaluasi AI** — konsisten prinsip "submission selalu diterima, evaluasi terpisah" yang sudah berlaku di P3-004/P6-002 (dibuktikan test: `testAiProvider`'s fake response gagal di-parse sebagai writing rubric, evaluasi gagal, tapi XP tetap masuk).

8 test baru (`xp.test.ts`) mencakup semua skenario DoD plus 1 test eksplisit "repeated /check tidak di-dedupe" (membuktikan keputusan desain `reference: null` buat jalur itu, bukan cuma diasumsikan). Route-coverage 75 route (naik dari 74, `GET /me/xp` baru), 0 gap. Total sekarang **286/286 test lulus**. Tidak ada verifikasi browser — endpoint XP murni backend, belum ada FE consumer (di luar scope Phase 8 yang murni backend).

### P8-002 — Streak tracking (non-punitive, streak freeze) (§6.5)
**Status:** todo
**Depends on:** P8-001 (dipicu dari titik hook yang sama — 1 aksi = 1 "hari aktif")
**Endpoint baru:** `GET /me/streak`.
**Deskripsi:** §6.5 eksplisit: jangan bikin anak merasa gagal cuma karena lupa 1 hari — Streak Freeze melindungi dari 1x kealpaan.
**Acceptance Criteria:**
- [ ] Migrasi baru: `user_streaks` (`user_id` PK, `current_streak` int, `longest_streak` int, `freezes_available` int default 1, `last_active_date` date nullable)
- [ ] `streak_service.recordActivity(db, userId, today)` dipanggil dari titik hook YANG SAMA persis dengan P8-001 (1 pemanggilan gabungan di handler, bukan hook terpisah lagi) — logic: `last_active_date == today` → no-op (sudah dihitung hari ini); `== yesterday` → `current_streak += 1`; lebih lama dari kemarin DAN `freezes_available > 0` → pakai 1 freeze, `current_streak` tetap (tidak putus), `freezes_available -= 1`; lebih lama dari kemarin DAN tidak ada freeze → `current_streak` reset ke 1 (bukan 0 — hari ini sendiri tetap dihitung aktif)
- [ ] `freezes_available` bertambah 1 tiap kelipatan 7-day streak tercapai (§6.5's semangat "reward konsistensi", bukan dijual — beli-freeze itu §6.9-13 yang di luar scope)
- [ ] `GET /me/streak` balikin `{current_streak, longest_streak, freezes_available}`
**DoD:** test backend baru — aktivitas hari berurutan → streak naik; lompat 1 hari dengan freeze tersedia → streak tidak putus, freeze berkurang; lompat 1 hari tanpa freeze → streak reset ke 1; aktivitas 2x di hari yang sama → tidak dihitung dobel; 7 hari berurutan → dapat 1 freeze baru.

### P8-003 — Achievements: 3 kategori (§6.7)
**Status:** todo
**Depends on:** P8-001 (XP/aktivitas), P8-002 (streak), `masteries` (Phase 1, buat Improvement Achievement)
**Endpoint baru:** `GET /me/achievements`.
**Deskripsi:** `Learning Achievement` (First Lesson, 100 Vocabulary Words, 7/30 Day Streak, Level Completed), `Skill Achievement` (per-skill milestone dari `skill_category`), `Improvement Achievement` (delta mastery, bukan nilai absolut — menghargai progress).
**Acceptance Criteria:**
- [ ] Migrasi baru: `achievements` (katalog — `id`, `code` unique, `category` CHECK IN (`learning`,`skill`,`improvement`), `name`, `description`, `criteria` jsonb) + `user_achievements` (`user_id`, `achievement_id`, `earned_at`, PK gabungan — 1 baris = 1x didapat, tidak berulang)
- [ ] Katalog awal di-seed lewat kode (pola sama `rubricRepository.ensure`, id tetap, idempotent) — minimal 3 per kategori sesuai contoh §6.7: Learning (First Lesson, 7-Day Streak, 30-Day Streak), Skill (per `skill_category` yang punya XP >= threshold), Improvement (mastery 1 concept naik >= 20 poin dibanding snapshot sebelumnya)
- [ ] `achievement_service.checkAndAward(db, userId)` dipanggil dari titik hook yang sama (gabung 1 pemanggilan lagi di handler) — cek semua kriteria yang BELUM didapat user itu, award yang terpenuhi, idempotent (kriteria yang sudah pernah dicapai tidak dicek ulang tak perlu — short-circuit di query `user_achievements` yang belum ada)
- [ ] `GET /me/achievements` balikin daftar yang sudah didapat + progress kasar ke yang belum (opsional, kalau kriteria-nya gampang dihitung progress-nya — kalau tidak, cukup daftar yang sudah didapat, jangan dipaksakan)
**DoD:** test backend baru — First Lesson achievement ke-trigger setelah submit lesson attempt pertama; 7-Day Streak achievement ke-trigger tepat di hari ke-7; Improvement Achievement ke-trigger saat mastery 1 concept naik >=20 poin; achievement yang sudah didapat tidak muncul dobel di `user_achievements`.

### P8-004 — Personal Mission: daily quest (§6.8)
**Status:** todo
**Depends on:** P8-001 (reward XP saat selesai)
**Endpoint baru:** `GET /me/daily-mission`.
**Deskripsi:** §6.8: misi harian sederhana (bukan leaderboard) — dianggap dokumen sumber lebih penting buat retention daripada kompetisi. Target harian tetap (bukan dipersonalisasi dari weakness detection — itu perluasan terpisah, di luar scope, biar tidak nyampur dengan `learning_queue_service` P4-002 yang sudah kompleks sendiri).
**Acceptance Criteria:**
- [ ] Migrasi baru: `user_daily_missions` (`user_id`, `mission_date` date, `progress` jsonb — `{vocab: 0, grammar: 0, listening: 0, speaking: 0}` vs target tetap `{vocab: 5, grammar: 1, listening: 1, speaking: 1}`, `reward_claimed` bool default false, PK gabungan `user_id`+`mission_date`)
- [ ] `daily_mission_service.recordProgress(db, userId, skillCategory)` dipanggil dari titik hook yang sama (gabung lagi) — increment counter yang sesuai `skill_category` untuk row hari ini (buat row baru kalau belum ada, target tetap hardcoded konstanta seperti di atas)
- [ ] Semua target tercapai DAN `reward_claimed = false` → auto-award +80 XP (lewat `xp_service.awardXp`, `reference = 'daily_mission:{user_id}:{date}'`, idempotent otomatis dari P8-001) + set `reward_claimed = true`
- [ ] `GET /me/daily-mission` balikin progress hari ini + target + status reward
**DoD:** test backend baru — progress bertambah sesuai `skill_category` tiap aktivitas; semua target tercapai → +80 XP otomatis sekali; mission hari kemarin tidak ikut ke-update aktivitas hari ini (row baru per tanggal).

### P8-005 — Leaderboard (Weekly + Personal) & League tier (§6.3 scope minimal, §6.4)
**Status:** todo
**Depends on:** P8-001 (`xp_events` — sumber data leaderboard), P8-002 (streak, salah satu input formula league)
**Endpoint baru:** `GET /leaderboard/weekly`, `GET /me/league`.
**Deskripsi:** §6.3 penuh (Global/Country/Region/Friends/Class/Course + Personal) **dipersempit ke Weekly (global) + Personal saja** — Country/Region butuh field profil yang belum ada di `users`, Friends/Class/Course butuh entitas social-graph/enrollment yang belum ada (roadmap-Fase-8, belum dibangun). §6.4 (League) dihitung on-read dari formula, BUKAN disimpan/di-refresh lewat cron (backend ini belum punya infrastruktur job berkala sama sekali — dicatat eksplisit, bukan diam-diam disederhanakan).
**Acceptance Criteria:**
- [ ] `GET /leaderboard/weekly?limit=20` — agregasi `xp_events` 7 hari terakhir per user, `ORDER BY SUM(amount) DESC`, TIDAK butuh tabel baru (query langsung ke `xp_events`, bukan materialized view — skala dev/early-user saat ini tidak butuh itu; catat di kode kalau nanti user banyak, ini kandidat butuh index/cache)
- [ ] Personal leaderboard: field tambahan di response yang sama, `{ percentile: number }` — posisi user yang minta dibanding seluruh user yang punya XP minggu ini ("kamu lebih baik dari X% pengguna"), dihitung dari hasil agregasi yang sama, bukan query kedua
- [ ] `GET /me/league` — tier `Bronze`/`Silver`/`Gold`/`Platinum`/`Diamond`/`Master` dihitung dari formula gabungan (bobot: `current_streak` + rata-rata `masteries.score` user itu + jumlah `xp_events` 7 hari terakhir — bobot eksplisit didokumentasikan di kode sebagai default yang bisa di-tuning, sama semangat §6.2), bukan XP mentah (§6.4's syarat eksplisit "bukan cuma XP, supaya tidak bisa dibeli")
- [ ] User tanpa aktivitas sama sekali: tidak muncul di leaderboard (bukan skor 0 di posisi terakhir), league tier default `Bronze`
**DoD:** test backend baru — 3 user dengan XP minggu ini beda-beda → urutan leaderboard benar, percentile masuk akal; user tanpa aktivitas minggu ini tidak muncul; league tier berubah sesuai formula (bukan cuma XP — user XP tinggi tapi streak 0 dan mastery rendah TIDAK otomatis tier tinggi, dites eksplisit sebagai regression terhadap "tidak bisa dibeli").

### P8-006 — Integration test suite + exit checkpoint
**Status:** todo
**Depends on:** P8-001 s/d P8-005
**Deskripsi:** Pola sama tiap ticket-phase sebelumnya — route-coverage audit, checkpoint end-to-end yang menyatukan XP→Streak→Achievement→Mission dalam 1 alur aktivitas nyata.
**Acceptance Criteria:**
- [ ] Route-coverage audit (`grep`-based, pola P2-017/.../P7-004)
- [ ] Checkpoint baru: 1 user menjawab beberapa soal lintas skill (vocab/grammar/listening/speaking/writing) dalam 1 hari via jalur asli (`/check` + `/attempts/{id}/submit`) — assert: `user_xp.total` sesuai akumulasi tabel XP, `user_streaks.current_streak = 1`, minimal 1 achievement (First Lesson) ter-award, `user_daily_missions` progress sesuai. Skenario ke-2: ulangi besoknya (disimulasikan lewat override tanggal, bukan nunggu wall-clock — pola sama P5-001/P7-001) → streak jadi 2, `GET /leaderboard/weekly` menampilkan user itu.
- [ ] Verifikasi eksplisit: `mastery.compute`/`frss.apply` (ADR-0002/0003) tidak pernah menerima input dari `xp_events`/`user_streaks`/`achievements` — grep langsung ke kode, bukan cuma percaya desain (menegakkan prinsip §6.1 "3 metrik tidak boleh dicampur")
**DoD:** `bun test` hijau penuh di `titian-backend-bun` (lokal — CI masih P0-010 yang tertunda).

---

## Checkpoint keluar Phase 8 (harus bisa didemo, bukan asumsi)
1. [ ] XP bertambah dari SEMUA jenis aktivitas belajar (inline check, assessment, level assessment, writing, speaking) — bukan cuma sebagian, dibuktikan lewat test per jalur.
2. [ ] Streak non-punitive: 1 hari kealpaan dengan freeze tersedia tidak memutus streak, dibuktikan lewat test, bukan cuma dibaca dari kode.
3. [ ] Minimal 1 achievement dari tiap 3 kategori (Learning/Skill/Improvement) benar-benar bisa didapat lewat alur nyata.
4. [ ] League tier terbukti BUKAN fungsi XP semata — 2 user dengan XP sama tapi streak/mastery beda, tier-nya beda.
5. [ ] `mastery.compute`/`frss.apply` terbukti tidak pernah tersentuh field gamification manapun — grep eksplisit, bukan janji desain.

Kalau salah satu poin di atas belum jalan end-to-end, jangan lanjut ke prioritas berikutnya (§6.9-16, item lepas, atau roadmap-Fase lain) walau ticket lain kelihatan sudah "done" — sama semangatnya dengan aturan checkpoint di Phase 1-7.

---

## Strategi eksekusi (urutan sesi yang disarankan)

| Sesi | Ticket | Fokus | Kenapa dikelompokkan begini |
|---|---|---|---|
| 1 | P8-001 | XP ledger + hook ke 5 titik submit | Fondasi murni — semua ticket lain (streak/achievement/mission/leaderboard) numpang di titik hook dan/atau data yang sama. |
| 2 | P8-002 | Streak + freeze | Numpang titik hook P8-001 — 1 pemanggilan gabungan, bukan hook terpisah lagi. |
| 3 | P8-003 | Achievement 3 kategori | Butuh XP+streak (P8-001/002) DAN mastery (Phase 1) sudah ada buat kriteria Improvement. |
| 4 | P8-004 | Personal Mission harian | Independen dari achievement, tapi sama-sama numpang titik hook — dikelompokkan setelah biar tidak nambah kompleksitas di 1 sesi yang sama dengan achievement. |
| 5 | P8-005 | Leaderboard + League | Butuh data XP+streak+mastery yang sudah lengkap dari 4 ticket sebelumnya buat formula league yang bermakna. |
| 6 | P8-006 | Test suite + checkpoint | Pola sama P1-013/.../P7-004 — penutup fase. |

**Total 6 sesi** — lebih besar dari Phase 5/7 (3-4 sesi) karena scope genuinely lebih luas (5 subsistem baru: XP/Streak/Achievement/Mission/Leaderboard, dibanding Phase 5-7 yang masing-masing 1 subsistem inti) — bukan under-scoping yang dipaksa kecil. §6.9-6.16 (model bisnis) sengaja tidak termasuk — lihat "Keputusan scope".
