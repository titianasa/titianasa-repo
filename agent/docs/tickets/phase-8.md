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
**Status:** done (2026-09-02, `titian-backend-bun`)
**Depends on:** P8-001 (dipicu dari titik hook yang sama — 1 aksi = 1 "hari aktif")
**Endpoint baru:** `GET /me/streak`.
**Deskripsi:** §6.5 eksplisit: jangan bikin anak merasa gagal cuma karena lupa 1 hari — Streak Freeze melindungi dari 1x kealpaan.
**Acceptance Criteria:**
- [x] Migrasi baru: `user_streaks` (`user_id` PK, `current_streak` int, `longest_streak` int, `freezes_available` int default 1, `last_active_date` — TEXT "YYYY-MM-DD", bukan tipe `date` native, lihat catatan implementasi)
- [x] `streak_service.recordActivity(db, userId, today)` dipanggil dari titik hook YANG SAMA persis dengan P8-001 — logic: `last_active_date == today` → no-op (sudah dihitung hari ini); `== yesterday` → `current_streak += 1`; lebih lama dari kemarin DAN `freezes_available > 0` → pakai 1 freeze, `current_streak` tetap (tidak putus), `freezes_available -= 1`; lebih lama dari kemarin DAN tidak ada freeze → `current_streak` reset ke 1 (bukan 0 — hari ini sendiri tetap dihitung aktif)
- [x] `freezes_available` bertambah 1 tiap kelipatan 7-day streak tercapai (§6.5's semangat "reward konsistensi", bukan dijual — beli-freeze itu §6.9-13 yang di luar scope) — HANYA saat streak genuinely maju ke kelipatan baru (bukan saat freeze dipakai, lihat catatan implementasi soal bug yang dicegah)
- [x] `GET /me/streak` balikin `{current_streak, longest_streak, freezes_available}`
**DoD:** test backend baru — aktivitas hari berurutan → streak naik; lompat 1 hari dengan freeze tersedia → streak tidak putus, freeze berkurang; lompat 1 hari tanpa freeze → streak reset ke 1; aktivitas 2x di hari yang sama → tidak dihitung dobel; 7 hari berurutan → dapat 1 freeze baru.

**Catatan implementasi:** `last_active_date` disimpan sebagai `text` ("YYYY-MM-DD", UTC), BUKAN tipe Postgres `date` native seperti draft awal ticket ini — service ini cuma butuh perbandingan string lurus terhadap tanggal yang caller kasih (`today: Date` — parameter eksplisit, bukan dibaca `new Date()` internal, jadi test bisa simulasikan hari manapun tanpa manipulasi DB langsung seperti P5-001/P7-001), jadi tipe `date` native (dengan potensi konversi timezone di boundary driver) cuma nambah risiko tanpa nambah manfaat di sini. **1 bug nyata dicegah sebelum sempat jadi bug** (ketauan waktu menulis kode, dikonfirmasi lewat test eksplisit `streak-freeze-no-double-bonus`): kalau bonus 7-hari dicek dari `newCurrentStreak % 7 === 0` tanpa syarat tambahan, memakai freeze saat `currentStreak` kebetulan kelipatan 7 (yang nilainya TETAP, bukan naik) akan salah memicu bonus freeze kedua kalinya — diperbaiki dengan syarat `streakAdvanced = newCurrentStreak > existing.currentStreak` sebelum cek kelipatan 7, jadi bonus cuma pernah lewat jalur "hari berurutan", tidak pernah lewat jalur "pakai freeze". `recordActivity` dipanggil di titik hook yang PERSIS sama dengan `xpService.awardXp` (P8-001) — 2 pemanggilan berurutan di tiap handler, bukan 1 fungsi gabungan (streak-nya sendiri sudah idempotent per-hari, tidak butuh `reference` kayak XP). 9 test baru (`streak.test.ts`). Route-coverage 76 route (naik dari 75, `GET /me/streak` baru), 0 gap. Total sekarang **295/295 test lulus**. Tidak ada verifikasi browser — murni backend, sama alasan P8-001.

### P8-003 — Achievements: 3 kategori (§6.7)
**Status:** done (2026-09-02, `titian-backend-bun`)
**Depends on:** P8-001 (XP/aktivitas), P8-002 (streak), `masteries` (Phase 1, buat Improvement Achievement)
**Endpoint baru:** `GET /me/achievements`.
**Deskripsi:** `Learning Achievement` (First Lesson, 100 Vocabulary Words, 7/30 Day Streak, Level Completed), `Skill Achievement` (per-skill milestone dari `skill_category`), `Improvement Achievement` (delta mastery, bukan nilai absolut — menghargai progress).
**Acceptance Criteria:**
- [x] Migrasi baru: `achievements` (katalog — `id`, `code` unique, `category` CHECK IN (`learning`,`skill`,`improvement`), `name`, `description`, `criteria` jsonb) + `user_achievements` (`user_id`, `achievement_id`, `earned_at`, PK gabungan — 1 baris = 1x didapat, tidak berulang) + `user_concept_mastery_baselines` (tambahan, lihat catatan implementasi)
- [x] Katalog awal di-seed lewat kode (pola sama `rubricRepository.ensure`, id tetap, idempotent) — Learning (First Lesson, 7-Day Streak, 30-Day Streak — 3), Skill (Speaking Star/Listening Master/Reading Explorer/Writing Builder — 4), Improvement (Improver +10/Weakness Destroyer +20/Master of Growth +40, 3 tier dari 1 mekanisme — lihat catatan implementasi kenapa bukan 3 kriteria berbeda seperti 3 nama contoh §6.7)
- [x] `achievement_service.checkAndAward(db, userId, context)` dipanggil dari titik hook yang sama — cek semua kriteria yang BELUM didapat user itu, award yang terpenuhi, idempotent (`ON CONFLICT DO NOTHING` di composite PK `user_achievements`, bukan cuma short-circuit di kode)
- [x] `GET /me/achievements` balikin daftar yang sudah didapat (progress-ke-belum-didapat TIDAK diimplementasi — lihat catatan implementasi)
**DoD:** test backend baru — First Lesson achievement ke-trigger setelah aktivitas XP-earning pertama; 7-Day Streak achievement ke-trigger tepat di hari ke-7; Improvement Achievement ke-trigger saat mastery 1 concept naik >=20 poin; achievement yang sudah didapat tidak muncul dobel di `user_achievements`.

**Catatan implementasi:** `xp_events` dapat kolom baru `skill_category` (nullable, additive — revisit kecil ke P8-001) karena Skill Achievement butuh SUM XP per kategori, dan `user_xp` cuma nyimpen total gabungan. Diisi hanya oleh caller yang tahu 1 skill dominan buat event itu (`checkAnswer`'s `question.skill_category`, atau literal `"writing"`/`"speaking"` di 2 cabang lesson) — NULL buat submission assessment/level_assessment (mencakup banyak skill sekaligus).

**Improvement Achievement butuh baseline, bukan cuma skor sekarang** — `masteries` tetap current-value-only (tidak ada tabel histori, sesuai batasan yang sudah dicatat sejak riset Phase 4). Solusinya: `user_concept_mastery_baselines` baru, nyimpen skor PERTAMA yang pernah diobservasi buat 1 pasangan (user, concept) — direkam sekali (idempotent, `ON CONFLICT DO NOTHING`) saat `checkAndAward` pertama kali melihat concept itu, tidak pernah berubah lagi sesudahnya. Delta = skor sekarang - baseline itu, bukan jendela bergerak.

**Improvement cuma 1 mekanisme (bukan 3 kriteria beda) diimplementasi sebagai 3 tingkat threshold (+10/+20/+40) dari mekanisme yang sama** — 3 nama contoh §6.7 (Biggest Improvement/Weakness Destroyer/Comeback Learner) sebenarnya menyiratkan 3 kriteria BEDA (ranking relatif "terbesar" butuh bandingkan ke semua user lain; "Comeback Learner" butuh nyambungin ke logic streak-freeze P8-002) — di luar scope wajar buat 1 ticket ini, jadi didokumentasikan eksplisit sebagai simplifikasi sadar, bukan diam-diam disederhanakan.

`GET /me/achievements` **tidak** balikin progress ke achievement yang belum didapat — AC sendiri menandai ini opsional ("kalau kriteria-nya gampang dihitung... kalau tidak, cukup daftar yang sudah didapat"), dan kriteria Skill/Improvement (threshold XP per-kategori, delta mastery) butuh query tambahan per achievement yang belum didapat untuk tiap request — dianggap tidak "gampang" cukup buat versi ini, bisa jadi perluasan terpisah.

`checkAndAward`'s parameter `questionIds` (bukan `conceptIds` langsung) dipilih supaya handler tidak perlu query tambahan — `assessment_handler.postSubmit`'s cabang assessment biasa/level_assessment sudah punya `answers.keys()` (question id) gratis; `achievement_service` sendiri yang resolve concept id lewat `questionRepository.findConceptIdsForQuestions` yang sudah ada. Cabang lesson writing/speaking sengaja TIDAK kirim `questionIds` (tidak ada `question_concepts` link buat prompt 1-lesson-penuh — temuan yang sama persis dicatat di awal ticket-phase ini).

11 test baru (`achievement.test.ts`) mencakup semua skenario DoD plus Skill category (tidak diminta eksplisit di DoD tapi diimplementasi, jadi dites) dan isolasi antar-skill (XP writing tidak ikut menghitung ke Speaking Star). Route-coverage 77 route (naik dari 76, `GET /me/achievements` baru), 0 gap. Total sekarang **306/306 test lulus**. Tidak ada verifikasi browser — murni backend, sama alasan P8-001/P8-002.

### P8-004 — Personal Mission: daily quest (§6.8)
**Status:** done (2026-09-02, `titian-backend-bun`)
**Depends on:** P8-001 (reward XP saat selesai)
**Endpoint baru:** `GET /me/daily-mission`.
**Deskripsi:** §6.8: misi harian sederhana (bukan leaderboard) — dianggap dokumen sumber lebih penting buat retention daripada kompetisi. Target harian tetap (bukan dipersonalisasi dari weakness detection — itu perluasan terpisah, di luar scope, biar tidak nyampur dengan `learning_queue_service` P4-002 yang sudah kompleks sendiri).
**Acceptance Criteria:**
- [x] Migrasi baru: `user_daily_missions` (`user_id`, `mission_date` — TEXT "YYYY-MM-DD" pola sama `user_streaks.last_active_date` P8-002, bukan `date` native, `progress` jsonb — `{vocabulary: 0, grammar: 0, listening: 0, speaking: 0}` vs target tetap `{vocabulary: 5, grammar: 1, listening: 1, speaking: 1}`, `reward_claimed` bool default false, PK gabungan `user_id`+`mission_date`)
- [x] `daily_mission_service.recordProgress(db, userId, skillCategory, today)` dipanggil dari titik hook yang sama — increment counter yang sesuai `skill_category` untuk row hari ini (buat row baru kalau belum ada, target tetap hardcoded konstanta); no-op kalau `skillCategory` di luar 4 yang dilacak (termasuk `undefined` dari cabang assessment/level_assessment yang tidak punya 1 skill tunggal)
- [x] Semua target tercapai DAN `reward_claimed = false` → auto-award +80 XP (lewat `xp_service.awardXp`, `reference = 'daily_mission:{user_id}:{date}'`, idempotent otomatis dari P8-001) + set `reward_claimed = true`
- [x] `GET /me/daily-mission` balikin progress hari ini + target + status reward
**DoD:** test backend baru — progress bertambah sesuai `skill_category` tiap aktivitas; semua target tercapai → +80 XP otomatis sekali; mission hari kemarin tidak ikut ke-update aktivitas hari ini (row baru per tanggal).

**Catatan implementasi:** 4 skill yang dilacak — `vocabulary`/`grammar`/`listening`/`speaking` — dipilih PERSIS sesuai contoh §6.8 sendiri ("✓5 vocab reviews ✓1 grammar exercise ✓1 listening ✓1 speaking"), BUKAN 7 `skill_category` penuh dari P7-002 — `reading`/`writing`/`pronunciation` sengaja tidak dilacak. Konsekuensinya: cabang lesson WRITING (`skillCategory: "writing"`) memanggil `recordProgress` sama seperti cabang lain (konsisten "panggil di semua 5 titik, biarkan service yang no-op"), tapi tidak pernah menambah progress — dites eksplisit (`a skill_category outside the tracked set (writing) does not affect progress`), bukan cuma diasumsikan dari baca kode. Cabang assessment/level_assessment (tidak ada 1 skill tunggal, sama alasan persis Skill Achievement P8-003 skip di cabang itu) juga dipanggil dengan `skillCategory: undefined`, no-op juga.

`mission_date` disimpan sebagai `text` "YYYY-MM-DD" (bukan tipe `date` native) — keputusan yang sama persis P8-002's `last_active_date`, alasan yang sama (`today` selalu parameter eksplisit, cuma butuh perbandingan string lurus).

Reward XP (+80) dan `reward_claimed = true` ditulis lewat 2 panggilan terpisah (`xpService.awardXp` lalu `dailyMissionRepository.upsert`), bukan 1 transaksi DB gabungan — idempotency-nya tetap aman karena `reference = "daily_mission:{userId}:{date}"` di `xp_events` sudah UNIQUE (P8-001): kalaupun `recordProgress` somehow terpanggil 2x sebelum `reward_claimed` sempat ke-persist, `awardXp` panggilan ke-2 no-op sendiri di layer XP. Didokumentasikan eksplisit di kode kenapa tidak perlu transaksi DB tambahan di sini.

7 test baru (`daily-mission.test.ts`). Route-coverage 78 route (naik dari 77, `GET /me/daily-mission` baru), 0 gap. Total sekarang **313/313 test lulus**. Tidak ada verifikasi browser — murni backend, sama alasan tiket-tiket Phase 8 lainnya.

### P8-005 — Leaderboard (Weekly + Personal) & League tier (§6.3 scope minimal, §6.4)
**Status:** done (2026-09-02, `titian-backend-bun`)
**Depends on:** P8-001 (`xp_events` — sumber data leaderboard), P8-002 (streak, salah satu input formula league)
**Endpoint baru:** `GET /leaderboard/weekly`, `GET /me/league`.
**Deskripsi:** §6.3 penuh (Global/Country/Region/Friends/Class/Course + Personal) **dipersempit ke Weekly (global) + Personal saja** — Country/Region butuh field profil yang belum ada di `users`, Friends/Class/Course butuh entitas social-graph/enrollment yang belum ada (roadmap-Fase-8, belum dibangun). §6.4 (League) dihitung on-read dari formula, BUKAN disimpan/di-refresh lewat cron (backend ini belum punya infrastruktur job berkala sama sekali — dicatat eksplisit, bukan diam-diam disederhanakan).
**Acceptance Criteria:**
- [x] `GET /leaderboard/weekly?limit=20` — agregasi `xp_events` 7 hari terakhir per user, `ORDER BY SUM(amount) DESC`, TIDAK butuh tabel baru (query langsung ke `xp_events`, bukan materialized view — skala dev/early-user saat ini tidak butuh itu; dicatat eksplisit di kode kalau nanti user banyak, ini kandidat butuh index/cache)
- [x] Personal leaderboard: field tambahan di response yang sama, `{ percentile: number }` — posisi user yang minta dibanding seluruh user yang punya XP minggu ini ("kamu lebih baik dari X% pengguna"), dihitung dari hasil agregasi yang sama, bukan query kedua
- [x] `GET /me/league` — tier `bronze`/`silver`/`gold`/`platinum`/`diamond`/`master` dihitung dari formula gabungan (bobot: `current_streak` + rata-rata `masteries.score` user itu + JUMLAH (COUNT, bukan SUM XP) `xp_events` 7 hari terakhir — bobot eksplisit didokumentasikan di kode sebagai default yang bisa di-tuning, sama semangat §6.2), bukan XP mentah (§6.4's syarat eksplisit "bukan cuma XP, supaya tidak bisa dibeli")
- [x] User tanpa aktivitas sama sekali: tidak muncul di leaderboard (bukan skor 0 di posisi terakhir), league tier default `bronze`
**DoD:** test backend baru — 3 user dengan XP minggu ini beda-beda → urutan leaderboard benar, percentile masuk akal; user tanpa aktivitas minggu ini tidak muncul; league tier berubah sesuai formula (bukan cuma XP — user XP tinggi tapi streak 0 dan mastery rendah TIDAK otomatis tier tinggi, dites eksplisit sebagai regression terhadap "tidak bisa dibeli").

**Catatan implementasi:** Nol migrasi baru di ticket ini — leaderboard murni agregasi `xp_events` (JOIN `users` buat nama), league murni gabungan `user_streaks`+`masteries`+`xp_events` yang sudah ada, keduanya dihitung on-read tiap request, konsisten AC-nya sendiri.

League's "jumlah `xp_events`" sengaja **COUNT**, bukan SUM XP seperti leaderboard — kalau pakai SUM, tier league jadi proxy XP lagi lewat pintu belakang (soal writing 20 XP vs vocabulary 5 XP bikin user yang banyak nulis otomatis unggul di komponen ini juga), padahal §6.4 eksplisit minta league TIDAK jadi proxy XP mentah. Formula: 3 komponen (`current_streak` capped 30 hari, rata-rata `masteries.score` confident-only — gate sama `masteryConfidenceThreshold` yang `findWeak` sudah pakai, `weekly_activity_count` capped 50) masing-masing di-rescale ke 0-100 lalu dirata-rata — dites eksplisit (`high-raw-xp-alone`) bahwa 1 event XP raksasa (streak=0, mastery=0) TIDAK bisa mendorong tier ke Diamond/Master, membuktikan formula-nya beneran tahan "dibeli" pakai XP doang.

`leaderboard_service`'s "me" (standing personal si pemanggil) dihitung dari **hasil agregasi penuh yang sama** yang menghasilkan `items` (bukan query kedua terpisah) — bahkan kalau si pemanggil di luar `limit` yang diminta (dites eksplisit: user rank ke-3 dari 3, `limit=2`, tetap dapat `rank`/`percentile` yang benar meski tidak muncul di `items`). Percentile pakai `(totalUsers - rank) / (totalUsers - 1) * 100` (penyebut TIDAK termasuk diri sendiri) — "lebih baik dari X% pengguna LAIN", bukan termasuk diri sendiri di pembagi (yang secara matematis janggal, tidak mungkin lebih baik dari diri sendiri); satu-satunya user berperingkat minggu itu dapat 100 (tidak ada yang perlu dikalahkan).

9 test baru (`leaderboard-league.test.ts`). Route-coverage 80 route (naik dari 78, `GET /leaderboard/weekly` + `GET /me/league` baru), 0 gap. Total sekarang **322/322 test lulus**. Tidak ada verifikasi browser — murni backend, sama alasan tiket-tiket Phase 8 lainnya.

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
