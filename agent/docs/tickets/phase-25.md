# Phase 25 (ticket-numbering) — Generate Konten Kurikulum Asli

## Keputusan scope (baca duluan)

Item ke-12 dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap di
`docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan semuanya'".
Berbeda dari fase 14-24 (semuanya membangun/menguji INFRASTRUKTUR):
fase ini **user secara eksplisit dikonfirmasi lewat pertanyaan
langsung** sebelum dikerjakan (2026-09-03) — karena isinya generate
konten kurikulum ASLI lewat panggilan AI sungguhan (biaya nyata,
keputusan kualitas konten nyata), bukan sekadar verifikasi pipeline
dengan data sintetis. User memilih "Proceed with Phase 25 now".

**Ditemukan SEBELUM sempat generate konten baru apa pun — 2 bug
KRITIS yang membuat SELURUH sisi belajar siswa tidak berfungsi sejak
cutover ADR-0009 (Rust→Bun), tidak berkaitan dengan konten baru:**

1. **`ACTIVE_CURRICULUM_ID` (frontend, `lib/curriculum.ts`) menunjuk
   ke UUID yang TIDAK PERNAH ADA di backend Bun ini** — nilai itu
   cuma pernah eksis di `titian-backend` (Rust) yang sudah diretire.
   Akibatnya: `/belajar` dan `/beranda` **SELALU** menampilkan "Belum
   ada materi" — termasuk Module 1 "Alphabet" yang sudah `published`
   penuh sejak P2-016 (2026-08-31)! Tidak ada satu pun siswa yang
   pernah bisa membuka kurikulum lewat UI sejak cutover, walau
   konten-nya sudah ada. Ditutup: `useCurriculumTree()` sekarang
   resolve curriculum aktif secara dinamis lewat `GET /curricula`
   (ambil yang pertama — cuma ada 1 curriculum nyata dalam praktiknya)
   alih-alih ID yang di-hardcode.
2. **`DEFAULT_SUBJECT_ID` (frontend, `lib/curriculum.ts`) — bug KELAS
   SAMA** — juga menunjuk UUID lama dari `titian-backend`'s seed yang
   tidak ada di backend ini. Akibatnya: "Buat curriculum baru" dan
   "Buat question bank baru" di Content Studio SELALU gagal (FK
   constraint ke `subject_id` yang tidak eksis). Ditutup: nilai
   diperbaiki ke subject asli yang benar-benar ada
   (`english-p2016`).

**Ditemukan SAAT generate konten Module 2 — 1 bug backend nyata:**

3. **`stripCodeFence` crash `TypeError: null is not an object` kalau
   provider AI balikin `message.content: null`** (bukan `undefined` —
   OpenRouter/model reasoning bisa balikin `content: null` kalau
   token budget habis dipakai untuk reasoning internal, bukan
   jawaban). Sebelumnya cuma dicek `text === undefined`, jadi kasus
   `null` lolos ke `stripCodeFence` dan crash jadi 500 mentah alih-alih
   jalur graceful yang sudah didesain (`ai_tasks` dicatat gagal, 422
   `ai_output_validation_failed`). Ditutup di `ai_provider.ts` — cek
   `undefined` DAN `null`, keduanya lempar `AIProviderError` yang sudah
   ditangkap caller.

**Ditemukan SAAT verifikasi student flow — 1 gap nyata, DIDOKUMENTASI
tapi TIDAK ditutup (di luar scope fase ini):** `POST
/assessments/{id}/attempts` yang gagal dengan `409
attempt_already_in_progress` SUDAH balikin `attempt_id` yang bisa
dipakai untuk resume (komentar di `error.ts` sendiri bilang begitu),
tapi TIDAK ADA `GET /attempts/{id}` untuk benar-benar mengambil ulang
soal-soalnya, dan `AssessmentAttempt` (FE) tidak pernah menangkap
`attempt_id` dari respons error itu untuk resume — cuma menampilkan
teks error mentah, siswa macet. Ditemukan murni karena skrip
verifikasi sesi ini sendiri membuat attempt yang tidak pernah
disubmit lalu retry. **Ini gap Phase 3 (`AssessmentAttempt`, P3-003),
bukan gap Phase 25** — memperbaikinya butuh endpoint backend baru +
alur resume FE, scope terpisah dari "generate 1 modul kurikulum".
Diverifikasi lewat panggilan API langsung ke attempt yang sama
(`POST /attempts/{attempt_id}/submit`) sebagai bukti scoring memang
bekerja, bukan didiamkan tanpa bukti.

**Modul 1 ("Alphabet") sudah ada sejak P2-016** — fase ini TIDAK
mengulang, tapi "scale ke modul berikutnya" (instruksi roadmap sendiri:
"mulai dari 1 modul Pre-Basic penuh untuk memvalidasi pipeline, baru
scale ke modul berikutnya") — **Modul 2 ("Numbers") dibangun penuh**
sebagai modul kedua yang membuktikan scaling benar-benar jalan.

**Dieksplisit DIDEFER**: generate seluruh 15 modul Pre-Basic + level
A1-C2 penuh — itu operasi konten berkelanjutan yang jauh melebihi 1
ticket-phase (setiap modul butuh biaya AI nyata + waktu kurasi
manusia nyata), persis sesuai instruksi roadmap sendiri ("jangan
generate seluruh silabus sekaligus"). `curricula.status` yang tetap
`'draft'` selamanya (tidak ada mekanisme publish untuk level
curriculum, cuma untuk lesson/question) — kosmetik saja, tidak
menggerbang apa pun secara fungsional (dikonfirmasi baca kode), tidak
ditutup karena butuh endpoint publish curriculum baru yang di luar
proporsi cuma untuk badge warna di Studio.

## Ticket

### P25-001 — Bugfix: `/belajar` & `/beranda` tidak pernah bisa menampilkan kurikulum
**Status:** done
**Depends on:** -
**Deskripsi:** `useCurriculumTree()` (titian-web) resolve curriculum aktif dinamis lewat `GET /curricula`, bukan ID hardcode basi dari backend Rust yang sudah retired. `DEFAULT_SUBJECT_ID` diperbaiki ke subject asli.
**Acceptance Criteria:**
- [x] `/belajar` menampilkan Module 1 (Alphabet) yang sudah lama published — dikonfirmasi lewat `Bun.WebView`, sebelumnya SELALU "Belum ada materi"
- [x] `/beranda` juga ikut pulih (pakai hook yang sama)
- [x] Content Studio's "Buat curriculum"/"Buat question bank" pakai subject id yang benar-benar ada
**DoD:** `bunx tsc --noEmit` bersih, diverifikasi lewat browser (before/after screenshot).

### P25-002 — Bugfix: crash saat provider AI balikin content null
**Status:** done
**Depends on:** -
**Deskripsi:** `ai_provider.ts`'s `stripCodeFence` caller sekarang dilindungi dari `content: null` (bukan cuma `undefined`) dari respons OpenRouter.
**Acceptance Criteria:**
- [x] `content: null` gagal lewat jalur graceful yang sudah ada (`AIProviderError` → `ai_tasks` gagal tercatat → 422), bukan crash 500 mentah
**DoD:** `bun test` 515/515, ditemukan+diverifikasi lewat panggilan generate-lesson ASLI (bukan test), bukan diasumsikan dari baca kode saja.

### P25-003 — Generate Module 2 Pre-Basic ("Numbers") penuh
**Status:** done
**Depends on:** P25-001, P25-002, P2-013 (AI generation), P2-005 (publish flow)
**Deskripsi:** Unit "Numbers" di bawah curriculum "Pre-Basic English" (P2-016) yang sudah ada — Learn/Practice/Speaking/Writing/Review/Assessment, 5 soal mcq, 1 assessment nyata. Campuran AI-generated (3 lesson + 5 soal — pipeline P2-013 dipakai sungguhan, bukan cuma dites) dan manual (3 lesson — writing/review/assessment-intro, pola sama persis P2-016 setelah 3x percobaan AI writing lesson gagal validasi berturut-turut).
**Acceptance Criteria:**
- [x] Semua 6 lesson + 5 soal + 1 assessment `published` lewat submit-review→publish ASLI (author terpisah dari reviewer)
- [x] Minimal sebagian lewat AI generation pipeline sungguhan (bukan 100% manual) — 3 lesson + semua 5 soal
- [x] Bisa diakses & dikerjakan end-to-end lewat endpoint yang sudah ada tanpa perubahan skema
**DoD:** Diverifikasi lewat `Bun.WebView` (browse `/belajar` → unit Numbers muncul, buka lesson quiz-intro, `assessment_embed` merender tombol "Mulai kuis") + panggilan API langsung untuk submit attempt (skor 100, 5 `learning_events` tercipta) — jalur resume browser terhalang gap P3-003 (lihat "Keputusan scope"), diverifikasi lewat API asli sebagai gantinya, bukan diasumsikan.

### P25-004 — Integration check + exit checkpoint
**Status:** done
**Depends on:** P25-001 s/d P25-003
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit`/`lint`/`build` bersih di `titian-web`
- [x] `bun test` bersih di `titian-backend-bun` (515/515, tidak ada regresi)
**DoD:** Akun author/reviewer/student sekali-pakai dibersihkan setelah verifikasi — KONTEN (unit/lesson/soal/assessment Numbers) SENGAJA TIDAK dibersihkan, itu konten produksi asli, bukan data demo. 1 lesson draft duplikat (akibat 1 panggilan curl saya sendiri yang timeout di sisi client tapi sukses di server) ditemukan+dihapus manual sebelum diverifikasi ulang.

---

## Checkpoint keluar Phase 25
1. [x] **Gap paling kritis fase ini bukan konten yang kurang, tapi konten yang sudah ada tidak pernah bisa dilihat siapa pun** — ditemukan dan ditutup sebelum melangkah lebih jauh, bukan diasumsikan "pasti sudah beres" karena backend-nya sudah published.
2. [x] Modul 2 ("Numbers") live, published, bisa dikerjakan end-to-end, skor tercatat nyata — bukti pipeline P2-013 scale ke modul kedua, bukan cuma modul pertama yang tervalidasi lalu didiamkan.
3. [x] 1 bug backend nyata (null-content crash) ditemukan lewat penggunaan sungguhan (bukan cuma dari membaca kode), ditutup dengan graceful-failure yang SUDAH didesain sejak awal, bukan mekanisme baru.
4. [x] Gap resume-attempt (P3-003) didokumentasikan eksplisit sebagai DI LUAR scope fase ini, bukan didiamkan atau disamarkan sebagai "sudah selesai".
5. [x] Generate seluruh silabus (15 modul Pre-Basic + A1-C2) DIDEFER eksplisit sesuai instruksi roadmap sendiri — dicatat sebagai operasi konten berkelanjutan, bukan 1 ticket-phase.

Phase 25 tertutup. Lanjut Phase 26 — Collaborative Canvas.
