# Phase 21 (ticket-numbering) — Module Completion Rule + Rescue Mode/Tutor Bridge

## Keputusan scope (baca duluan)

Item ke-8 dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap di
`docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan semuanya'".
Digabung jadi 1 ticket-phase karena keduanya kecil ("ticket engine
kecil, quick win" per urutan eksekusi yang sudah dicatat) dan
sama-sama murni mekanisme gating/rekomendasi di atas data yang sudah
ada — tidak ada tabel besar baru, tidak ada UI besar baru.

**§3.9 (rescue-mode/tutor-bridge) BUTUH ADR BARU** — ditandai eksplisit
di `ALR_Phase_Detail_Breakdown.md` line 821 sebagai salah satu dari 3
titik yang "butuh ADR baru sebelum implementasi". Ditulis duluan:
`docs/adr/0012-rescue-mode-tutor-bridge-thresholds.md`. Ringkasan
keputusan (detail lengkap + alasan ada di ADR-nya sendiri):
1. **Threshold rescue mode diinterpretasi ulang ke granularitas
   per-jawaban, bukan per-attempt formal** — "3 kali gagal" jadi "3
   jawaban terakhir untuk concept ini, berurutan, semua salah" (dari
   `learning_events`, yang SUDAH tercatat tiap kali jawab soal) —
   karena tidak ada tabel history mastery/attempt-per-concept di
   manapun (cuma current-value, sudah dicatat sebagai limitation sejak
   Phase 4).
2. **Konten remediasi 8-langkah dari dokumen (visual explanation →
   analogi Indonesia → ... → retest) TIDAK dibangun** — itu pipeline
   AI Content Generation (Phase 24) + konten kurikulum asli (Phase 25),
   di luar cakupan ticket "quick win" ini. Yang benar-benar dikirim:
   pesan sederhana + link ke lesson YANG SUDAH ADA DAN TERBIT yang
   mengajarkan concept itu (lewat `lesson_concepts`, bukan sintesis
   konten baru).
3. **Tutor Bridge = link umum ke `/marketplace`, BUKAN pencarian tutor
   yang cocok dengan concept tertentu** — `tutor_profiles.specializations`
   itu `jsonb` bebas, tidak terhubung FK ke `concepts`/`subjects`
   manapun. Memfilter "tutor untuk Present Perfect" akan jadi presisi
   palsu yang model datanya tidak dukung.

**Module Completion Rule (§37 `lms full.md`) — "module" dipetakan ke
`lessons` (bukan tabel baru).** Tidak ada tabel "modules" di manapun
di skema — hierarki yang ada `curricula → levels → units → lessons`,
dan embedded question (`content_blocks` tipe `question_embed`) di
dalam lesson persis contoh §37 ("module dengan 10 embedded
questions"). **3 syarat AND dari dokumen, dipetakan ke data yang
benar-benar ada:**
1. **Accuracy ≥ 80%** — dari jawaban TERAKHIR tiap embedded question
   di lesson itu (`learning_events`, `entityType='question'`, filter
   ke `question_id` yang benar-benar embed di lesson ini).
2. **"Required activities completed"** — TIDAK ADA entity "activity"
   terpisah di skema manapun, jadi diinterpretasi sebagai "SEMUA
   embedded question di lesson ini sudah pernah dijawab minimal
   sekali" — makna nyata (tidak bisa lewati soal dan tetap dianggap
   selesai), bukan re-labeling accuracy yang sama.
3. **Minimum mastery reached** — mastery SETIAP concept yang terhubung
   ke lesson ini (`lesson_concepts`) harus ≥ `weaknessScoreThreshold`
   YANG SUDAH ADA (Phase 4, `P4-001`) — direuse, bukan bikin threshold
   duplikat baru dengan nama beda tapi makna sama.

**Skip pakai Learning Credits** — direuse LANGSUNG dari
`economy_repository.charge`/`getBalance`/`AppError.insufficientCredit`
yang sudah ada sejak P11 (dipakai `ai_gateway_service` untuk charge AI
task) — bukan mekanisme charge baru. 1 tabel baru additive
(`lesson_completion_overrides`, PK `(user_id, lesson_id)`) untuk
menyimpan hasil skip, karena status completion dihitung on-the-fly
(pola sama `getMasteryBreakdown`) dan butuh 1 tempat menyimpan
"pengguna ini sudah skip lesson ini" yang bertahan lintas request.

**Dieksplisit DIDEFER**: penguncian navigasi (lesson berikutnya
terkunci sampai yang sekarang selesai) — accordion `/belajar` yang ada
sekarang tidak mendukung locking sama sekali (murni daftar), dan
membangun itu adalah desain ulang navigasi yang jauh lebih besar dari
"quick win". Completion Rule fase ini murni **indikator status +
gerbang informasional** (badge selesai/belum + rincian kenapa, tombol
skip) di halaman lesson itu sendiri — bukan penguncian keras.

## Ticket

### P21-001 — ADR-0012 + Backend: Rescue Mode
**Status:** done
**Depends on:** P4-001 (`concept_repository`, mastery), `learning_events`
**Endpoint baru:** `GET /concepts/{id}/rescue-status`. Field baru:
`POST /questions/{id}/check` respons dapat `rescue_triggered: boolean`.
**Acceptance Criteria:**
- [x] 3 jawaban berurutan salah (default, `RESCUE_MODE_CONSECUTIVE_FAILURES`) → `triggered: true`, balikin `suggested_lesson_ids` dari `lesson_concepts` (published only)
- [x] Kurang dari 3 event, atau ada 1 yang benar di antara 3 terakhir → `triggered: false`
- [x] `rescue_triggered` di respons `check` cuma true kalau salah satu concept soal itu BARU SAJA memicu (bukan re-check status lama berulang-ulang di setiap jawaban benar)
**DoD:** test baru di `tests/rescue.test.ts` + assertion tambahan di `question.test.ts`.

### P21-002 — Backend: Module Completion Rule
**Status:** done
**Depends on:** P4-001 (`weaknessScoreThreshold`), `lesson_concepts`, `economy_repository`
**Endpoint baru:** `GET /lessons/{id}/completion-status`, `POST /lessons/{id}/skip-completion`.
**Tabel baru (additive):** `lesson_completion_overrides`.
**Acceptance Criteria:**
- [x] Lesson tanpa embedded question ATAU tanpa concept terhubung → `eligible_for_gate: false` (tidak ada yang bisa digerbang)
- [x] Ketiga syarat (accuracy/activities/mastery) dihitung benar dari data nyata, bukan hardcode
- [x] Skip: saldo cukup → charge + override tersimpan + `completed: true` seterusnya; saldo kurang → `insufficient_credit` (402-style), tidak charge sebagian
- [x] Skip dua kali tidak charge dua kali (idempotent kalau override sudah ada)
**DoD:** test baru di `tests/module-completion.test.ts`.

### P21-003 — Frontend: rescue banner + tutor bridge + completion status card
**Status:** done
**Depends on:** P21-001, P21-002
**Deskripsi:** `QuestionCheck` (dipakai di mana pun — lesson viewer, review, personal review) dapat banner rescue mode kalau `rescue_triggered`. Halaman lesson (`belajar/[lessonId]`) dapat card status completion (kalau `eligible_for_gate`) dengan tombol skip.
**Acceptance Criteria:**
- [x] Banner rescue tampilkan link ke lesson yang disarankan (kalau ada) + CTA umum ke `/marketplace` (bukan pencarian tutor per-concept — sesuai ADR-0012)
- [x] Card completion tampilkan 3 syarat secara terpisah (bukan cuma 1 boolean gabungan), supaya learner tahu bagian mana yang kurang
- [x] Tombol skip nonaktif/pesan jelas kalau saldo Diamond tidak cukup
**DoD:** Diverifikasi lewat `Bun.WebView` — lihat P21-004.

### P21-004 — Integration check + exit checkpoint
**Status:** done
**Depends on:** P21-001 s/d P21-003
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit`/`lint`/`build` bersih di `titian-web`
- [x] `bun test` bersih di `titian-backend-bun`, tidak ada regresi
**DoD:** Diverifikasi end-to-end lewat `Bun.WebView` dan/atau test integrasi backend langsung — skrip seed sekali-pakai, dihapus + data dibersihkan setelah.

---

## Checkpoint keluar Phase 21
1. [x] Menjawab 3 soal beruntun salah pada concept yang sama memicu rescue mode dengan saran lesson nyata yang sudah terbit (bukan konten sintetis baru).
2. [x] Rescue banner menyediakan jalan ke tutor marketplace secara jujur (link umum), tidak berpura-pura mencocokkan tutor ke concept tertentu.
3. [x] Lesson dengan embedded question bisa dicek status completion-nya (accuracy/activities/mastery terpisah), dan bisa dilewati pakai Diamond kalau saldo cukup — charge nyata terjadi di `transactions`, bukan simulasi.
4. [x] Keterbatasan (navigasi tidak dikunci, remediasi 8-langkah tidak dibangun) didokumentasikan eksplisit, bukan diam-diam discope-creep atau dijanjikan lebih dari yang benar-benar dikirim.

Phase 21 tertutup. Lanjut Phase 22 — Messaging system.
