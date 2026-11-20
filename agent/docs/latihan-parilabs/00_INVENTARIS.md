# Latihan Parilabs: inventaris fase 0

Dasar: ADR-0031. Disusun 2026-11-19 dari membaca kode dan dokumen (tanpa build, server, atau browser). Angka baris dari `wc -l`, tanpa berkas tes kecuali disebut. Jumlah baris DB Titian dari `titian-bun-postgres` / `titian_bun` (SELECT saja). DB Parilabs (`parelabs_db`) sedang mati, jadi ukuran bank diambil dari skrip pembangun dan dokumennya.

Singkatan: **P** = Parilabs, **T** = Titian.

## 0. Temuan yang mengubah rencana

1. **`modules` dan `module_items` Titian bukan milik Latihan.** Isinya pustaka Belajar: 19.951 modul, 95.157 item (54.997 kuis bab dengan `quiz_config`, 20.826 artikel, 19.334 section), 28.282 label, 54.536 `content_blocks`. Tabel `canon_*`, `bab_bank_stats`, `canon_question_facts`, `content_tickets`, `module_item_concepts` punya FK ke `module_items`. Sebelas paket Go T membacanya (`canon`, `contentfactory`, `ai`, `studygroup`, `catalog`, `collab`, `completion`, `learning`, `messaging`, `metrics`, `module`).
2. **`questions` Titian milik Puzzle.** Dari 11.354 soal, 11.339 ada di bank "Puzzle · Matematika/Bahasa Inggris", dirujuk `puzzle_tasks` (6.716 baris). Hanya 15 soal (IELTS Reading 6, Pre-Basic 9) yang benar-benar soal latihan.
3. **Tabel P berawalan `org_*`, jadi tidak bentrok nama dengan tabel T.** Engine P bisa dipasang berdampingan. Yang diganti cukup domain ujian lama T (assessment, attempt, exam, proctoring, program) dan layar Latihan, Pengawasan, serta Studio bank soal.
4. **Format kuis sudah sama.** `quiz_config` T disalin field demi field dari `lib/quiz/types.ts` P (lihat komentar `internal/quiz/config.go`). Kuis bab T bisa langsung dijalankan player `kuis_umum` P tanpa konversi bentuk.
5. **Layar Latihan T masih tiruan.** `/latihan/{tka,snbt,ielts,toefl,pte}` merender `mock-exam-room.tsx` dengan soal tertanam. Data ujian T di DB lokal hanya data uji: 4 assessment, 15 soal assessment, 10 attempt, 0 exam session, 0 proctoring, 1 program "Smoke Program".
6. **Web P sudah siap SPA.** Tidak ada satu pun impor `next/*` di kode yang akan disalin. Navigasi lewat `lib/router/{navigation,link,dynamic}`, padanan langsung `lib/next-compat` T. Komponen UI yang dipakai hanya button, sheet, dialog, input, alert-dialog, tabs, badge, dropdown-menu, label, retry-dialog, tanpa `asChild`.
7. **Bentrok rute.** P mendaftarkan rute tingkat atas `/skills`, `/questions/{id}/skills`, `/assignments`, `/submissions/*`, `/tutor/*`, `/files/*`. T sudah punya `/questions/{id}`, `/assignments/{id}/submissions`, `/submissions/{id}/grade` (marketplace). Semua rute engine harus dipasang di bawah satu awalan.
8. **Hak pakai bank.** Isi bank berasal dari buku Cambridge IELTS 14–21, Pearson PTE Practice Tests Plus, dan ETS ITP Volume 3. Catatan hak pakai di P berlaku untuk Parilabs. Untuk Titian sebagai produk terpisah, hak pakainya perlu dipastikan pemilik.

## 1. Gambaran engine P

### 1.1 Alur data

```
org_programs (parent_id: program induk) ──org_program_modules (urutan, wajib, syarat buka)──▶ org_modules (is_folder, parent_id = folder)
   ▲ org_class_programs / org_semester_programs / org_product_programs                         │
   │                                                                                          ▼
org_program_enrollments (siswa × program, progres, item terakhir)          org_module_items (section/item, parent_id,
                                                                              type = assignment|article|video|file,
                                                                              content = id player, config = config player,
                                                                              guard_config, proctor_config, scope_class_id)
Akses: resolve_resource_access(user, module|program) ← resource_grants (user/org/email/public/product), visibility, org_members
Aturan: org_learning_rules (scope org < program < class; target module|item): open_at/close_at, daily_from/until, hidden,
        completion_rule (required|optional|practice), gate_condition, proctor_config
        └─ labs/rules.go menggabungkan lapisan → Availability (open/locked/hidden) per item

Siswa:  GET item → EnsureItemOpenForStudent → player
        PUT /labs/items/{id}/draft (autosave) · POST …/clock (jam ujian) → org_assignment_drafts
        proktor: POST /labs/drafts/{draft}/proctor-events · lock · live (keadaan layar) · audio · collab → org_proctor_events/locks/frames (draft_id)
        POST /labs/items/{id}/submit (idempoten lewat Redis) →
          org_assignments (dibuat otomatis satu per item) + org_assignment_submissions
          grading.Verify menilai ulang setiap jawaban di server (+ DrawDeck untuk soal acak)
          event dan kunci proktor pindah dari draft_id ke submission_id, draft dihapus
          org_module_item_progress → cascade org_module_progress, org_program_enrollments.progress_pct
          proctor.HandedIn → pengawas yang menonton menerima event SSE "handin"
Nilai:  Writing/Speaking → assignment (AI re-evaluate, antrean tutor, anotasi esai) → final_score
Tutor:  dinding pantau per modul / per org (SSE), Tonton live (runner mode mirror), kunci/buka/kirim kode, kolaborasi Yjs
```

### 1.2 Tipe item dan player (`AssignmentDispatcher.tsx`)

| `content` | Isi | Penilaian | Untuk Latihan T |
|---|---|---|---|
| `kuis_umum` | Kuis bergrup, ±40 subtype (`lib/quiz/subtypes`), tema `ielts`/`pte`/`toefl_itp`, soal acak (draw) | Auto di server (`grading`), esai lewat AI | **Inti.** Semua bank IELTS/PTE/ITP dan kuis bab T |
| `full_mock`, `mock_exam` | Ujian penuh per section, timer per section, skor band/310–677 | Gabungan part | **Inti.** Mock IELTS/PTE/ITP, try out TKA/SNBT |
| `writing`, `ielts_writing` | Esai dengan rubrik dan gambar Task 1 | AI + tutor | **Ya** |
| `speaking_record` | Rekam jawaban per bagian | AI (transkrip + rubrik) + tutor | **Ya** (IELTS Speaking, PTE) |
| `vocab_mastery` | Daftar kata, latihan bertahap | Auto | Opsional |
| `audio_upload`, `video_upload`, `file_upload` | Unggah berkas | Tutor | Opsional (tugas kelas) |
| `widget` | Widget interaktif (`components/widgets`) | `grading/widget.go` | Opsional |
| `reading`, `listening`, `grammar`, `vocabulary`, `cbt` | Player lama sebelum kuis umum | Klien | Tidak (diganti `kuis_umum`) |
| `speaking`, `special_speaking`, `speaking_lab`, `sid`, `live_class` | Ruang bicara AI, SpeakingPro, kelas live | AI | Tidak (T punya Ruang Bicara, Kelas, latihan Gemini) |
| `article`, `video`, `file` (`type`) | Materi | – | Tidak untuk Latihan (materi ada di Belajar) |

E-learning v2 (`internal/elearning`, 26.533 baris, tabel `elv2_*`) adalah kursus SpeakingPro 2 dan IELTS berlevel, bukan engine latihan. Tidak disalin. Yang diambil hanya gagasannya: tabel konversi band (`band.go`) sudah ada di web (`lib/quiz/full-mock/ieltsBands`, `toefl-itp-score.ts`).

## 2. Backend yang disalin

### 2.1 Paket domain

| Paket P | Baris (src/tes) | Fungsi | Endpoint | Disalin |
|---|---|---|---|---|
| `internal/labs` | 10.167 / 1.673 | Program, modul, item, aturan belajar, runner, bank soal, akses, taksonomi skill | 127 | Sebagian, lihat 2.2 |
| `internal/grading` | 1.066 / 396 | Penilaian ulang di server: `Verify`, `DrawDeck`, widget | – | **Ya, utuh** |
| `internal/proctor` | 3.805 / 631 | Config efektif, event, kunci (autolock), freeze, re-entry, identitas, dinding pantau modul/org, feed, live (SSE), audio live, kolaborasi Yjs, hand-in | 32 | **Ya**, tanpa `elv2_*`; share opsional |
| `internal/assignment` | 4.103 / 562 | Submission, antrean tutor, nilai, anotasi esai, AI re-evaluate, rencana belajar, ekspor xlsx/csv, hasil modul | 26 | **Ya**, AI lewat adapter |
| `internal/quiz` | 1.784 / 65 | Prompt dan parser generator AI kuis umum (13 bentuk keluaran) | – | Opsional (lihat keputusan K6) |
| `internal/aiapi` (bagian) | `kuis.go` 609, `evaluate.go` 747, `tutoreval.go` 458 | `/labs/ai/kuis-umum/*`, `/ai/writing/evaluate`, `/ai/ielts/*/evaluate`, `/ai/speaking/*-eval` | 44 total | Hanya penilai Writing/Speaking dan, bila K6 = ya, generator kuis |
| `internal/share` | 1.614 / 303 | Tautan ujian publik tanpa login, share attempt, dinding share | 25 | Opsional (K5: try out publik) |
| `internal/observer` | 801 / 125 | Pemantau/orang tua: token, ringkasan, submission siswa | 17 | Opsional (T punya peran `parent`) |
| `internal/files` | 890 / 442 | Unggah presigned, proxy R2, `/labs/audio-proxy` | 16 | Tidak; diganti adapter ke `assets` + `storage` T |
| `internal/attendance` | 2.610 / 648 | Jadwal, sesi, presensi QR | 28 | Tidak; T punya `class_sessions`, `org_attendance_records` |
| `internal/elearning` | 26.533 | Kursus SP2/IELTS | – | Tidak |

### 2.2 Rincian `internal/labs`

| Berkas | Baris | Isi | Disalin |
|---|---|---|---|
| `modules.go` | 1.057 | CRUD modul, folder, duplikat, analitik, transfer pemilik | Ya (buang 5 rujukan `elv2`) |
| `items.go` | 483 | CRUD item, salin subtree, urutan, kedalaman | Ya |
| `programs.go` | 738 | CRUD program, program anak, modul program, progres | Ya, tanpa kolaborator lintas org |
| `runner.go` | 523 | Progres, draft, jam, submit, cascade progres | Ya |
| `rules.go`, `rules_db.go`, `learning_rules.go` | 611 + 693 + 363 | Validasi dan penggabungan aturan, overlay proktor per siswa, editor aturan | Ya |
| `grants.go` | 971 | Visibilitas, grant user/org/produk, token akses, kolaborator | Sebagian: visibilitas, grant user/org, kolaborator; token dan produk sesuai K2 |
| `bank.go` | 410 | Bank Soal (`org_question_bank_items`): daftar, statistik, CRUD | Ya |
| `pickers.go` | 410 | Dashboard, "modul saya", picker item | Ya |
| `my_assessments.go` | 88 | Daftar ujian siswa (Ujilab) | Ya |
| `skills.go` | 487 | Taksonomi skill, test family, tag soal | Opsional (berguna untuk tag `ielts.*`, `itp.*`) |
| `usage.go` | 310 | Di mana program dipakai | Opsional |
| `semesters.go`, `classes.go`, `enrollment.go` | 1.192 + 874 + 637 | Batch, kelas, formulir gabung | **Tidak.** Diganti adapter ke `periods`, `classes`, `class_members` T. Yang dibawa hanya `ExpandProgramIDs`, `GrantProgramModules`, `SyncProgramIntoLinkedContexts` (ditulis ulang untuk tabel T) |

Perkiraan Go yang disalin dan disesuaikan: ±19 ribu baris sumber + ±3,5 ribu baris tes (labs inti ±7,3 ribu, grading 1,1 ribu, proctor 3,8 ribu, assignment 4,1 ribu, AI ±1,8 ribu; tambah share/observer ±2,4 ribu bila dipilih).

### 2.3 Ketergantungan platform P

| P | Dipakai oleh | Padanan T | Tindakan |
|---|---|---|---|
| `platform/auth` (`auth.User{ID, GlobalRole}`, `?access_token=` untuk SSE) | semua | `auth.Context{UserID, OrganizationID, Role}`; token query hanya untuk WS | Adapter `auth.User` dari Context; tambahkan `?access_token=` di middleware T untuk rute SSE |
| `platform/tenant` (`x-tenant-id`, nil = jalur pribadi) | labs, proctor, share | header `X-Organization-Id` → `auth.Context.OrganizationID` | Adapter: `tenant.From(ctx)` membaca Context T |
| `platform/access` (317 baris: `IsGlobalAdmin`, `IsOrgStaff`, `ResolveAccess`, `CanGradeSubmission`, `TutorScope`, `CanProctorModule`) | semua | `rbac` (matriks peran), `user_organization_roles` | Salin, ganti `org_members`/`user_global_roles` dengan `user_organization_roles` |
| `platform/httpx` (`NotFound(pesan)`, galat `{code,message}`) | semua | `httpx` T (`NotFound(kode)`, galat berkode) | Shim kecil di paket engine (`lx.NotFound(pesan)` → galat T) |
| `dbx` 118, `jsonx` 131, `reqbody` 378, `idem` 155, `bg` 40, `useragent` 93 | semua | tidak ada | Salin apa adanya ke `internal/platform/` |
| Redis (`idem.Wrap` pada submit) | labs | `App.Redis` ada | Pakai |
| Storage R2/MinIO (`files`, `storage`) | assignment (audio tutor), proctor (foto identitas), files | `storage.Storage` (R2, `InMemory` di tes), tabel `assets` | Adapter: `file_id` → `assets.id` |
| SSE (ditulis langsung di `proctor/live.go`) + `Hub` di memori | proctor | belum ada SSE umum | Ikut paketnya; satu instance API (sama seperti P) |
| AI (`ai.Provider`, `prompts` di DB, Azure pronunciation, Praat) | assignment, aiapi | `ai.Service.Resolve(peran)`: `writing_evaluation`, `speaking_evaluation`, `quiz_generation`, `stt`, `tts` | Adapter `assignment.Evaluator` di atas resolver T; prompt rubrik IELTS dipindah ke `prompts_gen.go` |
| LiveKit | tidak dipakai engine (hanya jadwal P) | – | – |
| `apitest`, `testdb` | tes | `apitest`, `testdb` T | Tes disesuaikan ke harness T |

### 2.4 Awalan rute

Usulan: semua rute engine di bawah `/latihan/...` dengan akhiran yang sama seperti P (`/latihan/modules/{id}`, `/latihan/items/{id}/submit`, `/latihan/drafts/{id}/live-stream`, `/latihan/submissions/{id}`, ...). Di web cukup satu konstanta dasar di service. Daftar lengkap endpoint per paket ada di berkas `Module()` masing-masing (`labs/labs.go`, `proctor/proctor.go`, `assignment/assignment.go`).

## 3. Tabel database

DB P tidak bisa dibangun dari migrasinya (README P: skema ditambal manual). Migrasi T ditulis baru dari definisi di `db/schema.sql` P, bukan menyalin berkas migrasi. Migrasi T terakhir: `0116_pare_aktivitas.sql`.

### 3.1 Tipe dan fungsi SQL

| Nama | Isi | Penyesuaian T |
|---|---|---|
| `access_role` enum | viewer < taker < tutor < editor < owner | Sama |
| `resource_visibility` enum | private, org, public | Sama |
| `resolve_resource_access(user, type, id, global_role)` | 1 admin global → owner; 1.5 admin org → owner; 2 pembuat → owner; 3 grant user; 4 grant org; 5 visibilitas org × peran org; 6 public; 7 grant public; 8 grant produk (`org_user_product_access`) | `org_members` → `user_organization_roles`; langkah 8 → langganan T (`subscriptions.tier`) atau dibuang (K2) |
| `org_role_to_access_role` | admin/principal/teacher → editor, student → taker | Peran T: `org_owner`, `academic_director`, `curriculum_developer` → editor; `teacher`, `tutor` → tutor; `reviewer` → viewer; `student` → taker; `parent` → viewer |
| `role_can(role, action)` | view/submit/grade/edit/manage_access/delete | Sama |
| `fn_has_class_role`, `fn_scoped_role_covers` | Tutor kelas, cakupan tutor atas siswa lewat program kelas | Ditulis ulang di atas `classes.teacher_id` + `class_members` T |
| `fn_delete_item_learning_rules` + trigger | Hapus aturan item saat item dihapus | Sama |
| `resolve_pending_email_grants` | Grant via email jadi grant user saat daftar | Opsional |

### 3.2 Tabel

Urutan = urutan migrasi (FK).

| # | Tabel P | Fungsi | Kolom penting | FK | Migrasi T |
|---|---|---|---|---|---|
| 1 | `org_programs` | Program/kursus, pohon program | org_id, parent_id, slug, visibility, public_role, sequential_modules, metadata, created_by | organizations, self, users | 0117 |
| 2 | `org_modules` | Modul dan folder (bank) | org_id, parent_id, is_folder, program_id, proctor_config, target_tests[], tags[], visibility, public_role | organizations, self, org_programs, users | 0117 |
| 3 | `org_program_modules` | Modul dalam program | order_index, is_required, unlock_after_module_id, requires_previous, guard_config | org_programs, org_modules | 0117 |
| 4 | `org_module_items` | Section/item, config player | node_type, type, content, config, guard_config, proctor_config, assessment_kind, file_id, scope_class_id | org_modules, self, assets (ganti `files`), classes | 0117 |
| 5 | `org_learning_rules` | Aturan per org/program/kelas | scope_type, scope_id, target_type, target_id, module_id, rules | org_modules | 0117 |
| 6 | `resource_grants` | Grant akses | resource_type, grantee_type, grantee_id, role, source, product_id, expires_at | users, organizations | 0117 |
| 7 | `org_module_collaborators` | Editor/tutor/proktor per modul atau item | module_id xor module_item_id, role (owner…proctor) | org_modules, org_module_items, users | 0117 |
| 8 | `org_class_programs` | Program yang dipakai kelas | class_id, program_id | **classes T**, org_programs | 0117 |
| 9 | `org_program_enrollments` | Siswa × program | progress_pct, last_item_id, class_id, semester_id → `period_id` | org_programs, users, classes, periods | 0117 |
| 10 | `org_module_progress`, `org_module_item_progress` | Progres modul dan item | status, completed_items_count, is_completed, completion_type | enrollments, org_modules, org_module_items, users | 0117 |
| 11 | `org_assignments` | Satu per item yang dinilai | module_item_id, assignment_type, config, max_score, passing_score | org_module_items, org_programs | 0118 |
| 12 | `org_assignment_drafts` | Jawaban sementara + jam ujian | answers_data, duration_seconds, clock_started_at | org_module_items, users | 0118 |
| 13 | `org_assignment_submissions` | Hasil kumpul | answers_data, ai_score, ai_feedback, tutor_score, final_score, attempt_number, proctor_config_snapshot, proctor_summary, rubric_scores | org_assignments, org_module_items, users, assets | 0118 |
| 14 | `org_submission_annotations` | Anotasi esai tutor/AI | submission_id, start/end_offset, comment, source | submissions, users, assets | 0118 |
| 15 | `org_proctor_events` | Log proktor | draft_id / submission_id / share_attempt_id (xor), event_type, severity, payload, client_ts, geo | drafts, submissions, assets | 0118 (tanpa `elv2_session_id`) |
| 16 | `org_proctor_locks` | Kunci dan kode buka | reason, is_locked, unlock_code, unlocked_by | drafts, submissions, events | 0118 |
| 17 | `org_proctor_frames` | Cuplikan keadaan layar untuk putar ulang | draft_id, at, state | drafts | 0118 (anchor = draft atau submission) |
| 18 | `org_class_module_proctors` | Pengawas per kelas × modul | class_id, module_id, user_id | classes T, org_modules, users | 0118 |
| 19 | `org_question_bank_items` | Bank Soal: snapshot grup soal | subject (ielts/pte/toefl_itp/…), family, subtype, part/passage_number, test_type, tags[], taxonomy, group_snapshot, source_module_id | organizations, users | 0118 |
| 20 | `skills`, `test_families`, `skill_test_coverage`, `org_skill_overrides` | Taksonomi skill | – | – | 0119, opsional |
| 21 | `org_share_links`, `org_share_attempts`, `resource_access_tokens` | Tautan publik | – | – | 0119, opsional (K5) |
| 22 | `observer_tokens`, `user_relationships` | Pemantau | – | – | opsional |

Tidak dibawa: `org_organizations`, `org_members`, `users`, `files`, `org_semesters*`, `org_classes`, `org_class_members`, `org_class_sessions`, `org_class_attendance`, `org_product_*`, `org_user_product_access`, semua `elv2_*`, `cert_*`, `sid_*`, `org_speaking_*`.

## 4. Web yang disalin

Semua sumber di `app-parelabs-v2/src`. Angka baris tanpa berkas tes.

| Fitur | Berkas P | Baris | Tujuan T |
|---|---|---|---|
| **Pustaka kuis** | `lib/quiz/**` (subtypes 5.616, _helpers 2.771, templates 3.195, generation 1.165, full-mock 700, bank 323, inti 3.566) | 17.211 | `src/lib/latihan/quiz/`; menggantikan `lib/quiz-*.ts` T |
| **Runner dan player** | `components/labs/assignments/AssignmentDispatcher.tsx` 1.447 (dipangkas ke tipe di 1.2); `simulations/kuis-umum/page.tsx` 3.342 + `GroupCard` 1.077 + `themes/{ielts,pte,toefl_itp}` 860; `full-mock/` 2.466; `writing/` 1.707; `speaking-record/` 2.061; `vocab-mastery/` 1.971; `_shared/` 931; `submissions/` 1.513; `ExamTimer` 50; `lib/labs/{submit-item,item-clock,transcribe-audio}` 180; `hooks/use-draft-autosave` 161 | ±17.800 | `src/components/latihan/runner/`; menggantikan `components/exercise/*` dan `components/latihan/mock-exam-room.tsx` |
| **Pemutar program** | `app/[tenantSlug]/(fullscreen)/labs/elearning/page.tsx` 1.732 (navigasi program → modul → item); halaman program siswa `(main)/labs/programs/**` 1.969 | ±3.700 | rute `/latihan/program/$id`, `/latihan/kerjakan/$itemId` |
| **Proktor siswa** | `lib/proctor/**` (regular-client 500, input-guard 157, enforcement 95, live 115, collab 242, live-audio, block-clipboard, progress) 1.367; `lib/share/proctor-client.ts` 295 (opsional) | ±1.660 | `src/lib/latihan/proktor/` |
| **Dinding pantau tutor** | `components/labs/proctor/` (`ProctorWallPanel` 1.062, `LiveExamView` 585, `OrgProctorWall` 348, `ProctorGrantsPanel` 138, `CollabCursors` 117); halaman `labs/tutor/proctor/[moduleId]` 114; drawer `ProctorWallDrawer` 731 | ±3.100 | `/pengawasan`, `/pengawasan/modul/$moduleId`, `/admin/organisasi/$org/pengawasan`; menggantikan `components/proctoring/*` dan `screens/(app)/pengawasan/*` T |
| **Editor modul** | `(focus)/labs/modules/[mid]/page.tsx` 3.513 + `_components/` yang relevan: `ProctorConfigSection` 966, `ModuleProctorDrawer` 583, `ModuleAssignmentDrawer` 591, `ItemAccessPanel` 347, `SettingsAuditDrawer` 334, `ShareLinksDrawer` 915 (opsional). Dibuang: Listening/Reading/Grammar/Vocabulary/SpeakingLab ConfigSection, LessonPlanEditor, GenerateFromPdf, SectionDomainVariant | ±6.300 dari 20.149 | `/studio/latihan/modul/$id`; menggantikan `components/studio/modules` untuk kebutuhan Latihan |
| **Editor soal** | `kuis-umum/ConfigEditor` 2.667 + editor struktur (Table, Flow, GapFill, CellLines, ConversationCards), `SubtypeLibraryPicker`, `TemplateBrowser`, `ModuleItemRefPicker`, `ConvertGroupTypeModal`, `AddToQuestionBankModal`, Generate*Modal (AI, opsional) ; `full-mock/FullMockConfigEditor` 700 + `SectionImportModal` 527; `speaking-record/ConfigEditor`; `components/editor/**` (TipTap, QuizRichTextModal, extensions) 5.841 | ±16.000 | `src/components/latihan/editor/`; menggantikan `components/studio/quiz/*` T (5.031) |
| **Aturan belajar** | `components/admin/learning-rules-editor.tsx` 372; `components/labs/class-item-rules.tsx` 48 | 420 | tab "Aturan" di editor modul dan halaman kelas T |
| **Bank Soal dan Ujilab** | admin `labs/bank-soal/*` 1.229; `(fullscreen)/labs/practice/page.tsx` 179 (latihan per tipe soal); `(main)/labs/ujilab/page.tsx` 144; `services/question-bank.ts` 145; `hooks/useQuestionBank.ts` 93 | ±1.800 | `/studio/latihan/bank`, `/latihan/tipe-soal`, `/latihan/ujian`; menggantikan `screens/studio/question-banks/*` |
| **Admin program** | `admin/organizations/[id]/labs/programs/**` 1.211, `modules` 141 | ±1.350 | `/studio/latihan/program`; menggantikan `screens/studio/programs/*` |
| **Tutor: penilaian dan hasil** | `labs/tutor/review-queue/**` 1.075; `components/tutor/**` (EssayAnnotator, AnswersEditorPanel, SpeakingRecordReviewPanel, …) 3.997; `ModuleResultsPanel` 319; `hooks/useModuleResults` 116; `services/annotations` 110 | ±5.600 | `/guru/latihan/...`; menggantikan `components/latihan/review-*` |
| **Widget** (opsional) | `components/widgets/**` 2.858 + `lib/widgets` 1.047 | 3.900 | hanya bila subtype `widget_interact` dipakai |
| **Service, hook, tipe** | `services/labs.ts` 1.387; `hooks/use-labs.ts` 597; `types/index.ts` 448 (bagian labs) | ±2.400 | `src/lib/latihan/api.ts`, `hooks/use-latihan.ts` |

Total yang disalin: ±65–70 ribu baris (tanpa widget dan opsional ±60 ribu). Tidak disalin: `components/labs/elearning-v2` (22.898), `sid`, `slides`, `live-class`, `speaking`, `speaking-lab`, player lama.

### 4.1 Ketergantungan npm

| Paket | P | T | Tindakan |
|---|---|---|---|
| `@tiptap/*` (starter-kit, table, image, link, highlight, text-align, underline, placeholder, bubble-menu) | 3.33 | 3.31 (core, react, starter-kit, placeholder, collaboration) | Tambah ekstensi table, image, link, highlight, text-align, underline, bubble-menu |
| `yjs` | 13.6.27 | 13.6.32 | Sudah ada |
| `@dnd-kit/core`, `sortable`, `utilities` | ya | tidak | Tambah |
| `react-resizable-panels` | 4.21 | tidak | Tambah (layout passage/soal) |
| `katex`, `react-markdown`, `framer-motion`, `zustand`, `@tanstack/react-query` | ya | ya (versi lebih baru) | Cek API `framer-motion` 12 → 13 |
| `xlsx` | ya | tidak | Hanya bila ekspor dari web; ekspor xlsx ada di backend |
| `recharts`, `sonner` | ya | tidak | Ganti ke komponen grafik/toast T, atau tambah |
| `zod` 3 vs 4 | | | Periksa skema form |
| UI: Radix (P) vs `@base-ui/react` (T) | | | Tidak ada `asChild`; tambah `alert-dialog` dan `retry-dialog` di `components/ui` T |
| LiveKit | hanya jadwal P | – | Tidak perlu |

### 4.2 Yang harus diganti saat menyalin

| P | T |
|---|---|
| `@/lib/router/{navigation,link,dynamic}` | `@/lib/next-compat/{navigation,link,dynamic}` (API sama) |
| `tenantHref(path)` (13 berkas), `use-tenant`, `use-enforce-org-slug`, `stores/tenant-store` | Path langsung; organisasi aktif dari store auth T (`X-Organization-Id`) |
| `fetchApiWithAuth`, `fetchApi`, `API_BASE_URL` dari `@/lib/api-client` (88 berkas) | Satu modul `lib/latihan/api.ts` di atas `api-client.ts` T (token refresh T), awalan `/latihan` |
| `EventSource(url?access_token=…)` | Sama, setelah backend T menerima `?access_token=` |
| `@/stores/auth-store` | `@/store/auth-store` T |
| `@/lib/brand` (white-label) | Konstanta Titian |
| `@/components/ai/AiModelPicker`, `PromptOverrideDrawer` | Dibuang; model diatur Admin Pusat T (`ai_settings`) |
| `@/components/presentation/*`, `PCFPreview`, `lib/pcf` | Dibuang |
| `contexts/tutor-level`, `components/labs/elearning-v2/*` yang diimpor editor (`LessonPanel`, `SpeakingPracticeEditor`, `ClassPathPlanner`, `kit`) | Dibuang dari editor |
| Gaya: Tailwind P, palet P, tema ujian | Token desain T; tema `ielts`/`pte`/`toefl_itp` tetap meniru tampilan ujian resmi |
| Gambar bank `/bank-soal/pte/pte-2/*` di `public/` P (37 berkas, 1,1 MB) | Diunggah ke R2 T, URL ditulis ulang |

## 5. Pemetaan ke Titian

| P | T | Cara |
|---|---|---|
| `users` | `users` | Sama (UUID). FK langsung |
| `auth.User.GlobalRole` admin/super_admin | `user_organization_roles.role = 'platform_admin'` | `access.IsGlobalAdmin` membaca tabel T |
| `org_organizations` (tenant) | `organizations` (24 sekolah + 1 `platform`) | `org_id` → `organizations.id` |
| `org_members.role` | `user_organization_roles.role` | Peta peran di 3.1 |
| Batch `org_semesters` | `periods` | Hanya dibaca (enrollment.semester_id → period_id) |
| `org_classes`, `org_class_members` (role student/tutor/admin) | `classes` (`teacher_id` tunggal, `module_id`, `program_id`), `class_members` (tanpa peran) | Kelas tetap milik T. Engine membaca lewat adapter: tutor = `classes.teacher_id` atau peran `teacher`/`tutor` di org; siswa = `class_members`. `org_class_programs` dan `org_class_module_proctors` ber-FK ke `classes` |
| `files` | `assets` + `storage.Storage` | `file_id` → `assets.id`; audio unggahan siswa lewat presigned PUT T |
| AI per jenis (`aiapi`, `prompts`) | `ai.Service.Resolve(peran)` | `writing_evaluation`, `speaking_evaluation`, `stt`, `tts`, `quiz_generation` |
| Produk → program (`org_product_programs`, grant `source='product'`) | `subscriptions.tier`, ekonomi T | Lihat K2 |
| Kelas live, presensi | `class_sessions`, `org_attendance_records` | Tidak disentuh |

### 5.1 Pelajar mandiri tanpa organisasi

Usulan: **konten milik org platform Titian, percobaan siswa tanpa org.**
- Program, modul, dan bank Latihan resmi dimiliki `organizations` bertipe `platform` (Titian Asa). Pelajar mandiri tidak dimasukkan ke org itu.
- Akses lewat langkah `resolve_resource_access` yang sudah ada: `visibility = 'public'` + `public_role = 'taker'` untuk yang gratis, dan grant `source = 'product'` (langkah 8, dibaca dari langganan T) untuk yang berbayar.
- Pendaftaran program mandiri: endpoint baru kecil "Mulai program" yang membuat `org_program_enrollments` tanpa `class_id`.
- Progres, draft, dan submission tidak butuh `org_id` (kolomnya nullable). Siswa mandiri hanya kena `proctor_config` item. Aturan ketat tingkat program atau kelas tidak berlaku baginya, sama seperti perilaku P untuk siswa tanpa kelas.
- Alasan: tidak menambah keanggotaan palsu (kalau semua pengguna masuk org platform, langkah 5 `resolve_resource_access` memberi mereka akses ke semua isi ber-visibilitas `org`); jalur `org_id IS NULL` dan `public` sudah diuji di P; sekolah tetap bisa menautkan program resmi ke kelasnya lewat `org_class_programs`.

### 5.2 Kaitan ke unit kanonik dan jalur (ADR-0026)

- Penanda di item dan grup soal: `org_module_items.config.titian = {unit: ["slug-unit"], jalur: ["tka-sma", ...], peran: "kemasan" | "cek" | "ujian"}`, dan `question.titian.unit` per soal bila satu grup mencakup beberapa unit (pola `question.elv2` P).
- Modul ujian jalur (try out TKA, SNBT, mock IELTS) ditautkan dari node jalur: `canon_path_nodes` dengan `node_type = 'latihan'` dan `asset_id` = `org_modules.id` (atau tabel kecil `canon_path_latihan`).
- Setelah submit, hook di `runner.go` (setelah `grading.Verify`) menulis bukti per unit: benar/total per unit ke tabel baru `latihan_bukti_unit (user_id, unit_id, submission_id, benar, total, at)`, dan ringkasannya tampil di jaringan pengetahuan.
- Status unit (dimiliki/dikuasai) tetap dari deck materi, sesuai aturan 3 ADR-0026, kecuali pemilik memutuskan lain (K3).

## 6. Fitur Titian lama yang hilang atau perlu padanan

| Fitur T lama | Lokasi | Padanan P / tindakan |
|---|---|---|
| Assessment `unit_test`/`level_assessment`/`ielts` + `assessment_questions` | `internal/assessment` (3.506), `assessmentsApi` | `org_module_items` `kuis_umum`/`full_mock` |
| Attempt kuis per item (`POST /lessons/{id}/attempts`, `attempts`) | `assessment/quizsubmit.go`, `components/exercise/quiz-attempt.tsx`, **dipakai `kelas/materi/[itemId]` (kuis bab Belajar)** | Draft + submit P. Kuis bab tetap di alur lama sampai B4.2 memindahkannya; jangan dihapus di fase 5 sebelum itu |
| Checkpoint per section artikel, reread | `assessment/checkpoint.go`, `section_checkpoint_progress` | Milik Belajar (artikel), **tetap** |
| Exam session + proctoring policy/session/event | `assessment/exam.go`, `proctoring.go` (tabel kosong) | `proctor_config` + `org_proctor_*` |
| Quiz proctor session per item (foto KTP, unlock) | `module/proctor.go` (745), `quiz_proctor_*` (kosong) | `proctor/identity.go`, kunci + kode buka |
| Review manusia atas sesi ujian (`/pengawasan`) | `components/proctoring` | Dinding pantau + Tonton live + antrean tutor |
| Program + `program_modules` | `internal/program` (346), 1 program uji | `org_programs` |
| Question bank + soal + alur review (draft → in_review → published) | `internal/question` (1.422), `/studio/question-banks` | `org_question_bank_items` + editor kuis. **Alur review hilang**; P tidak punya status review per soal (K7). Bank Puzzle tetap di `questions` |
| Versi item, review/publish item, tiket konten, label modul, learning path publik, heatmap, lesson plan, guard/presensi item, Yjs kolaborasi editor | `internal/module` | Milik Belajar/Studio, **tetap**. Engine P punya `guard_config`/`attendance_guard` sendiri, tanpa versi dan review |
| FRSS personal review (`/latihan/personal-review`) | `learningApi.getLearningQueue` | Bukan bagian engine; **tetap**, pindah ke Belajar atau tetap di tab Latihan |
| Mock room statis TKA/SNBT/IELTS/TOEFL/PTE | `components/latihan/mock-exam-room.tsx` (673) | `full_mock` dengan isi nyata |
| Generator AI kuis (`ai/quizgen.go`) | `components/studio/quiz` | Editor P + generator T atau P (K6) |

### 6.1 Data lama di DB lokal (`titian_bun`, 2026-11-19)

| Tabel | Baris | Isi | Tindakan |
|---|---|---|---|
| `programs` | 1 | "Smoke Program" | Hapus setelah arsip |
| `program_modules` | 0 | | Hapus |
| `assessments` | 4 | IELTS Reading Practice Test 1, Alphabet Concept Check, Alphabet Quiz, Numbers Quiz | Pindah ke modul (B4.2) atau buang (data uji) |
| `assessment_questions` | 15 | | Ikut di atas |
| `attempts` | 10 | 5 per item (2 preview), 5 per assessment | Arsip, tidak dipindah |
| `exam_sessions`, `proctoring_sessions`, `proctoring_events`, `proctoring_policies` | 0 | | Hapus |
| `quiz_proctor_sessions`, `quiz_proctor_events` | 0 | | Hapus |
| `question_banks` | 6 | 2 Puzzle, IELTS Reading, Pre-Basic ×2, "Bank" | Puzzle tetap; sisanya pindah ke Bank Soal |
| `questions` | 11.354 | 11.339 Puzzle, 6 IELTS Reading, 9 Pre-Basic | 15 dipindah; Puzzle **tetap** |
| `module_items` kuis (`quiz_config`) | 54.997 (53.354 dengan `question_groups`, 51.531 grup) | Bank kuis bab di "Semua Mata Pelajaran" (Pabrik Konten) | Disalin ke format modul di B4.2 bila K1 memutuskan; sumber tetap untuk `canon`/`bab_bank_stats` |
| `modules` | 19.951 | Pustaka kurikulum dan ujian (Kurikulum Indonesia 5.397, Persiapan PT 3.136, Kurikulum Cambridge 1.893, TKA 1.600, BUMN 310, CPNS 277, Bahasa Inggris 1.252, Semua Mapel 6.082) | **Tetap** |
| `module_item_progress` | 2 | | Tetap (Belajar) |
| `classes` / `class_members` | 1 / 1 | | Tetap; dipakai engine lewat adapter |

## 7. Isi bank P

### 7.1 Tempat simpan

- **DB modul P** (`parelabs_db` dev; prod "hanya dengan persetujuan"): pohon folder `org_modules` (`IELTS BANK SOAL › IELTS ACADEMIC › IELTS nn › TEST n`, `PTE BANK SOAL › PTE ACADEMIC › PTE 2`, `TOEFL ITP BANK SOAL › ITP LEVEL 1 › VOLUME 3`), item `kuis_umum` per part/tipe soal dan `full_mock` per test, plus baris `org_question_bank_items` per grup soal.
- **Sumber yang bisa dibangun ulang (file):**
  - IELTS: `parelabs-backend-go/scripts/ielts_bank/` (21 MB, 77 berkas; soal, kunci, pembahasan, audioscript per test dalam Python), `build_ieltsNN.py` → SQL + dump JSON, cek `cmd/tools/bankcheck`.
  - PTE: `parelabs-workspace/PTE BANK/PTE 2/data/pte-2.sql` siap pakai (15 modul, 128 item, 241 grup bank) + `pte-2.json`, gambar webp di `public/bank-soal/pte/pte-2/`.
  - TOEFL ITP: `parelabs-workspace/TOEFL ITP BANK/ITP Level 1 - Volume 3/data/itp-l1-v3.sql` (9 modul, 44 item, 84 grup bank) + JSON.
  - Indeks per tipe soal: `content/ielts/bank_index.json`.
- **Audio:** R2 publik P (`pub-8bfe…r2.dev/uploads/…`) untuk klip yang dipakai ulang (44 URL di `ielts_old_audio.py` untuk IELTS 17–19, 16 di `ielts20_scripts.py`, 16 di `ielts21_scripts.py`); MinIO dev untuk yang diunggah `set_ielts_audio.py`; berkas lokal pemilik `parelabs-workspace/AUDIO IELTS/` (60 MP3, 550 MB: IELTS 14, 15, 16 masing-masing 16, IELTS 18 sebanyak 8, IELTS 20 sebanyak 4).
- **Gambar:** chart Writing Task 1 dan peta Listening di `scripts/ielts_bank/ieltsNN_img/` (42 berkas, ±17 MB), dirujuk `::image{url=".../files/<id>/proxy"}` dengan id per lingkungan (`ieltsNN_images.json`).

### 7.2 Ukuran

| Bank | Isi | Soal | Audio |
|---|---|---|---|
| IELTS 14–21 Academic | 8 buku × 4 test, reguler + MOCK TEST (Speaking AI + rekam) | ±2.460 (indeks: 14: 309, 15: 311, 16: 308, 17: 308, 18: 307, 19: 308, 20: 307, 21: 306) | 17, 19, 20, 21 lengkap (16 klip per buku); 18 tanpa Test 4; 14, 15, 16 kosong di DB tapi ada di `AUDIO IELTS/` |
| CAMBRIDGE 17–21 (bank lama) | Folder lama P, sebagian tidak lengkap | ±1.160 | Sumber audio untuk IELTS 17–21 |
| PTE 2 | 4 test, 20 tipe soal, tema `pte` | 4 test × ±65–75 tugas | Kosong (hanya audioscript; perlu TTS atau rekaman) |
| TOEFL ITP L1 V3 | Practice Test A dan B, 140 soal per test | 280 | Kosong (transkrip + speaker siap TTS) |

Angka pasti (baris modul, item, bank, audio terisi) dihitung di B4.1 dari DB P, dengan izin menyalakan `parelabs_db`.

### 7.3 Cara impor (B4.1)

1. Ekspor pohon bank dari DB P: `pg_dump --data-only` dibatasi lewat salinan sementara, atau skrip `cmd/tools/ekspor_bank` yang membaca subtree folder bank (modul, item, `org_question_bank_items`) ke JSON. Lebih aman daripada menjalankan ulang builder, karena hasil suntingan editor di DB ikut terbawa.
2. Pengimpor T `cmd/tools/impor_bank_parilabs`: id baru UUID v5 deterministik (bisa diulang), `org_id` = org platform T, `created_by` = akun sistem T, `visibility` sesuai K2.
3. Media: unduh setiap `audio_url` dan gambar (R2 publik P, MinIO dev, `AUDIO IELTS/`, `public/bank-soal`), unggah ke R2 T dengan kunci `latihan/bank/<buku>/<test>-<part>.mp3`, tulis ulang URL di `config`.
4. Periksa: setiap kunci dinilai benar oleh `grading` T (port `bankcheck`), jumlah modul/item/grup sama dengan sumber, setiap URL media menjawab 200, tidak ada URL `r2.dev` P atau `/files/<id>/proxy` yang tersisa.

## 8. Rencana fase 1–5

Aturan kerja: maksimal dua agen sekaligus, setiap batch satu agen, perintah berat lewat `agent/tools/batas-ram.sh`, hanya container yang dibutuhkan. Tes Go dengan `testdb` T.

### Fase 1: skema

| Batch | Berkas | Bukti selesai |
|---|---|---|
| **B1.1** Skema inti | `db/migrations/0117_latihan_inti.sql` (enum, tabel 1–10 di 3.2, fungsi `resolve_resource_access`, `role_can`, `org_role_to_access_role`, trigger aturan), `db/schema.sql` | Tes `internal/latihan/schema_test.go`: setiap langkah `resolve_resource_access` (admin global, admin org, pembuat, grant user/org/public/produk, visibilitas org/public, kedaluwarsa) memberi peran yang benar; hapus item menghapus aturannya |
| **B1.2** Skema percobaan dan proktor | `0118_latihan_percobaan_proktor.sql` (tabel 11–19), `0119` opsional (skill, share) | Tes constraint xor event/kunci, FK ke `classes` dan `assets`, cascade hapus draft |

### Fase 2: backend

| Batch | Berkas | Bukti selesai |
|---|---|---|
| **B2.1** Platform | `internal/platform/{dbx,jsonx,reqbody,idem,bg,useragent}` (salin), `internal/latihan/lx` (shim httpx, `auth.User`, `tenant`), `internal/latihan/akses` (port `platform/access` ke tabel T), `auth` menerima `?access_token=` untuk SSE | Tes unit paket yang disalin lulus; tes akses peran T |
| **B2.2** Modul, item, program, bank | `internal/latihan/{modules,items,programs,grants,pickers,bank,my_assessments,enroll}.go`, rute `/latihan/*`, adapter kelas T | Tes integrasi CRUD + akses (siswa tidak melihat `config` item rahasia, editor melihat), program mandiri bisa diikuti |
| **B2.3** Aturan, runner, grading | `internal/latihan/{rules,rules_db,learning_rules,runner}.go`, `internal/latihan/grading` (salinan `grading` P; `internal/grading` T tetap untuk Belajar) | Tes: jawaban palsu `is_correct: true` dinilai ulang; jendela `open_at`/`close_at` dan `daily_*`; `practice` tidak dihitung; submit ganda dengan kunci idempotensi sama hanya tersimpan sekali |
| **B2.4** Proktor | `internal/latihan/proktor/*` (dari `proctor`, tanpa `elv2_*`, share di belakang flag) | Port `proctor_test.go`, `pipe_test.go`, `wall_feed_test.go`: autolock setelah N pelanggaran, buka dengan kode, event pindah ke submission, feed membaca event setelah kumpul, SSE `handin` |
| **B2.5** Penilaian dan tutor | `internal/latihan/nilai/*` (dari `assignment`), adapter `Evaluator` ke `ai.Resolve("writing_evaluation")`/`speaking_evaluation`, prompt rubrik IELTS/PTE ke `ai/prompts_gen.go` | Tes: antrean tutor hanya berisi siswa yang dicakup, anotasi, nilai tutor menimpa AI, ekspor xlsx; AI dipalsukan di tes |
| **B2.6** (opsional) | Share link publik (K5), observer (orang tua), generator AI kuis (K6) | Tes paket masing-masing |
| **B2.7** Kaitan kanonik | `config.titian`, `latihan_bukti_unit` (migrasi 0120), hook setelah submit, node jalur `latihan` | Tes: submit kuis bertanda unit menulis bukti per unit; status unit tidak berubah (atau berubah sesuai K3) |

### Fase 3: web

| Batch | Berkas | Bukti selesai |
|---|---|---|
| **B3.1** Fondasi | `src/lib/latihan/quiz/**` (salin `lib/quiz`), `src/lib/latihan/api.ts` (dari `services/labs.ts`, `question-bank.ts`), `hooks/use-latihan.ts`, tipe, `components/ui/{alert-dialog,retry-dialog}`, dependensi npm 4.1 | Vitest: tes P yang ikut (`answer-match`, `draw`, `toefl-itp-score`, `score`) lulus; `tsc` untuk folder baru lewat `batas-ram.sh` |
| **B3.2** Runner dan player | `components/latihan/runner/**` (Dispatcher dipangkas, kuis umum + tema, full mock, writing, speaking record, vocab mastery, uploads), rute `/latihan/kerjakan/$itemId`, `/latihan/program/$id` | QA Bun.WebView (dengan izin pemilik): kerjakan satu part IELTS Reading, autosave, reload, kumpul, skor sama dengan server |
| **B3.3** Proktor | `lib/latihan/proktor/**`, `components/latihan/proktor/**` (Wall, LiveExamView, OrgWall, Cursors, Grants), rute `/pengawasan/**` | QA dua sesi: pindah tab tercatat, kunci, buka dengan kode, Tonton live melihat ketikan Writing |
| **B3.4** Editor | `screens/studio/latihan/**`: editor modul (dipangkas), ConfigEditor kuis umum, FullMockConfigEditor, speaking record, ProctorConfigSection, aturan belajar, TipTap tambahan | Buat modul baru dengan satu grup soal, terbitkan, kerjakan sebagai siswa |
| **B3.5** Bank, ujian, tipe soal, beranda Latihan | Bank Soal admin, `/latihan/tipe-soal`, `/latihan/ujian` (Ujilab), halaman `/latihan` memakai data asli, admin program | Beranda Latihan menampilkan bank IELTS/PTE/ITP dari API; latihan per tipe soal merakit grup dari bank |
| **B3.6** Tutor | Antrean penilaian, detail submission, anotasi esai, panel hasil modul | Tutor menilai Writing siswa dan siswa melihat nilai dan anotasi |

### Fase 4: isi

| Batch | Berkas | Bukti selesai |
|---|---|---|
| **B4.1** Bank IELTS, PTE, ITP | `cmd/tools/ekspor_bank` (di sisi P, baca saja), `cmd/tools/impor_bank_parilabs`, unggah media | Cek 7.3 butir 4 lulus; laporan jumlah per buku |
| **B4.2** Bank Titian ke modul | Konversi kuis bab (54.997 item) ke `org_modules` per bab dengan `config.titian.unit`; 4 assessment + 15 soal lama; peta jalur TKA/SNBT ke modul try out | Jumlah grup sama; satu bab dikerjakan lewat runner baru; `canon`/`bab_bank_stats` tetap benar |
| **B4.3** Audio yang kosong | IELTS 14–16 dan 18 Test 4 dari `AUDIO IELTS/`; PTE dan ITP lewat TTS Inggris (biaya, perlu izin) | Setiap grup Listening punya audio yang terputar |

### Fase 5: bersih-bersih

| Batch | Isi | Bukti selesai |
|---|---|---|
| **B5.1** Arsip dan hapus | `pg_dump` tabel lama + tar kode ke `/home/john/backups/`, commit dulu; hapus `internal/assessment`, `internal/program`, bagian `internal/question` yang bukan Puzzle, `module/proctor.go`; migrasi drop `assessments`, `assessment_questions`, `exam_sessions`, `proctoring_*`, `quiz_proctor_*`, `programs`, `program_modules` (dan `attempts` hanya setelah B4.2); web `components/exercise` (kecuali yang dipakai Belajar), `components/proctoring`, `components/latihan/mock-exam-room`, layar Studio bank dan program | `go test ./...` dan tes web lulus; tidak ada impor ke paket yang dihapus |
| **B5.2** Deploy | Backup DB prod, deploy `sync`/`local-build`/`restart`, unggah media ke R2 prod | Konfirmasi pemilik; cek kesehatan dan satu ujian ujung ke ujung di prod |

Jumlah: 19 batch wajib (2 + 6 + 6 + 3 + 2), ditambah 1–3 batch opsional (B2.6). Urutan kritis: B1.1 → B1.2 → B2.1 → B2.2 → B2.3 → (B2.4 ∥ B2.5) → B3.1 → B3.2 → (B3.3 ∥ B3.4) → B3.5 → B4.1. B2.7, B3.6, B4.2, B4.3 bisa berjalan setelah dependensinya.

### Risiko

| Risiko | Akibat | Mitigasi |
|---|---|---|
| Menghapus `modules`/`module_items`/`questions` T ikut "domain lama" | Belajar, kanonik, Puzzle rusak | Fase 5 hanya menghapus tabel di 6.1 yang bertanda hapus; daftar dicek ulang sebelum migrasi drop |
| Kuis bab Belajar memakai `attempts` + `components/exercise` | `/kelas/materi` rusak bila dihapus sebelum B4.2 | `attempts` dan komponen exercise dihapus paling akhir |
| Kontrak galat P vs T berbeda | Pesan galat web kosong | Shim `lx` + tes kontrak galat di B2.1 |
| Hub SSE dan ruang kolaborasi di memori | Tidak jalan di lebih dari satu instance | T berjalan satu instance di Hetzner; catat di ADR |
| Hak pakai bank komersial | Risiko hukum saat Titian launch | K4 sebelum B4.1 ke prod |
| Bank P terus diedit di P setelah disalin | Isi T tertinggal | Impor bisa diulang (UUID v5) dan hanya menimpa item yang belum diedit di T (pola `build_hash` P) |
| Ukuran web (±65 ribu baris) dan RAM 15 GB | Build berat, agen kehabisan konteks | Batch dipotong per fitur; `tsc` per folder lewat `batas-ram.sh` |
| `framer-motion` 12 → 13, `zod` 3 → 4, Radix → Base UI | Galat tipe dan perilaku | Diperiksa di B3.1 sebelum player disalin |
| Biaya TTS untuk audio PTE/ITP | Belanja AI | Izin pemilik di B4.3 |

## 9. Keputusan yang perlu pemilik

| # | Pertanyaan | Usulan |
|---|---|---|
| K1 | "Menggantikan domain lama" mencakup pustaka Belajar (`modules`, 55 ribu kuis bab) atau hanya domain ujian? | Hanya domain ujian sekarang. Kuis bab disalin ke format modul di B4.2, pustaka Belajar tidak dipindah |
| K2 | Latihan mana yang gratis dan mana yang berbayar (grant produk dari langganan)? | Satu test per buku gratis (`public`), sisanya lewat tier langganan |
| K3 | Apakah hasil latihan mengubah status unit (dimiliki/dikuasai)? ADR-0026 aturan 3 bilang kemasan dan cek tidak | Dicatat sebagai bukti dan ditampilkan, status tetap dari deck materi |
| K4 | Hak pakai bank Cambridge/Pearson/ETS untuk Titian | Konfirmasi sebelum naik ke prod |
| K5 | Perlu tautan ujian publik tanpa login (try out sekolah, `share`)? | Ya untuk try out TKA/SNBT sekolah, di fase opsional |
| K6 | Generator AI di editor kuis: pakai milik P (`/labs/ai/kuis-umum/*`) atau `ai/quizgen` T? | `ai/quizgen` T (sudah memakai bentuk config yang sama dan resolver T) |
| K7 | Alur review soal (draft → in_review → published) hilang di engine P. Perlu? | Cukup status terbit modul/item P untuk Latihan |
| K8 | Awalan rute `/latihan/*` dan nama paket `internal/latihan` | Ya |
| K9 | Kursus e-learning v2 IELTS (Foundation, Level 1) ikut? | Tidak, di luar ADR-0031 |
