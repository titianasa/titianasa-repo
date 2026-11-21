# Keputusan teknis pindahan engine Parilabs

Keputusan produk ada di ADR-0031. Berkas ini mencatat keputusan teknis per batch, supaya batch berikutnya tidak memutuskannya ulang.

## B1.1: skema inti (commit `85b2459`, branch `latihan`)
- `org_id` mengacu ke `organizations`. `NULL` berarti jalur pribadi.
- Pengguna mengacu ke `users`, kelas ke `classes`, dan `semester_id` diganti `period_id` → `periods`. Berkas mengacu ke `assets`.
- Grant produk memakai `subscription_tier` ('plus'/'pro') dan dibaca dari langganan aktif Titian. Pro mencakup plus.
- Setiap user Titian otomatis menjadi `student` di org platform "Titian Asa". Karena itu peran `student`/`parent` di org bertipe `platform` **tidak** memberi akses. Isi platform dibuka lewat `public` atau grant produk.
- Peta peran:
  - Admin org adalah `org_owner` dan `academic_director`.
  - `teacher` dan `tutor` dipetakan ke peran akses `tutor`, bukan `editor` seperti di Parilabs. Guru menjadi editor lewat posisi pembuat atau grant.
- Bug Parilabs yang diperbaiki:
  - Grant user tidak lagi memotong peran lebih tinggi; yang dipakai peran tertinggi dari semua langkah.
  - Grant produk tidak lagi terbaca sebagai grant `public`.

## B1.2: diputuskan koordinator (2026-11-19)
- Aturan org platform di atas tetap dipakai. Penetapan peran bawaan Titian tidak diubah.
- Guru tetap `tutor`.
- Grant dan aturan yatim dibersihkan: tambahkan trigger yang menghapus `resource_grants` dan `org_learning_rules` (scope `class`/`program`/`module`) saat modul, program, atau kelas dihapus.
- Satu grant produk per resource sudah cukup (pro mencakup plus). Unique index tidak diubah.
- `fn_has_class_role` dan `fn_scoped_role_covers` masuk B1.2, berbasis `classes.teacher_id` dan `class_members` Titian.
- Grant lewat email tidak dipakai, jadi `resolve_pending_email_grants` tidak disalin.
- Percobaan pelajar mandiri: `org_assignment_submissions.org_id` boleh `NULL`.
- Share (K5) ditunda ke fase opsional, jadi `share_link_id` belum dibuat.
- `org_proctor_frames` ditambatkan ke draft atau submission (salah satu, dengan CHECK xor).
- Semua FK ke `assets` memakai `on delete set null`.
- Tes integrasi memakai `TEST_DATABASE_URL` dari `.cache/api-local.env`, diteruskan lewat `GO_DOCKER_ARGS="-e TEST_DATABASE_URL"`. Tanpa itu `testdb` diam-diam SKIP.

## B1.2: hasil (branch `latihan`)
- Migrasi `0118_latihan_percobaan_proktor.sql`: tabel 11–19 (`org_assignments`, `org_assignment_drafts`, `org_assignment_submissions`, `org_submission_annotations`, `org_proctor_events`, `org_proctor_locks`, `org_proctor_frames`, `org_class_module_proctors`, `org_question_bank_items`), `fn_has_class_role`, `fn_scoped_role_covers`, dan `fn_delete_latihan_orphans` beserta triggernya. `0119` tidak dibuat: taksonomi skill hanya dipakai `labs/skills.go` (opsional).
- Submission di Parilabs tidak punya `org_id`. Di Titian kolom itu ditambahkan: org tempat percobaan dibuat (sekolah siswa), `NULL` untuk pelajar mandiri, `on delete set null` (percobaan tetap ada walau sekolahnya dihapus). Pemilik isi tetap `org_assignments.org_id`. Runner P tidak mengisinya, jadi B2.3 harus mengisi dari tenant.
- Anchor event, kunci, dan frame: `draft_id` xor `submission_id`. `share_attempt_id` dan `elv2_session_id` dibuang. Kalau share (K5) dipasang, kolom dan CHECK-nya ditambah lagi. Kode `proctor`/`share` P yang menyebut `share_attempt_id` (±15 tempat) harus dipangkas di B2.4.
- Saat kumpul, B2.3 memindahkan `org_proctor_frames` ke submission bersama event dan kunci. Di P, frame ikut terhapus bersama draft.
- `fn_has_class_role`: hanya `classes.teacher_id`. Peran `teacher` di org tidak otomatis menjadi tutor semua kelas. Admin org diperiksa terpisah (`IsOrgStaff`), sama seperti P.
- `fn_scoped_role_covers`: guru kelas × anggota `class_members` × `org_class_programs` (program induk ikut). Cabang batch P (`org_semester_members`) tidak punya padanan, karena `periods` tidak punya anggota.
- Pembersih yatim juga berjalan untuk `organizations` (aturan scope `org`, grant ke org) dan `users` (grant ke user), selain modul, item, program, dan kelas.
- FK ke `users` yang di P tanpa aksi (`edited_by`, `unlocked_by`) dan `triggered_by_event_id` memakai `on delete set null`. `annotator_id` tetap cascade karena CHECK anotasi tutor mewajibkannya.
- `org_question_bank_items.source_module_id` tetap tanpa FK, sama seperti P: snapshot berdiri sendiri.
- Indeks dari migrasi P yang hilang di `schema.sql` P (`idx_org_assignments_*`, `idx_assignment_submissions_*`) dan trigger `updated_at` untuk assignment dan submission ikut dipasang.
- Cara memperbarui `db/schema.sql`: dump template tes sebelum dan sesudah migrasi baru, lalu sisipkan blok yang baru ke `schema.sql` di posisi urutan dump. Ini dilakukan dengan skrip kecil, bukan `make schema`, karena DB dev berisi objek lain. `TEST_DATABASE_URL` diisi dari `DATABASE_URL` di `.cache/api-local.env`, karena berkas itu tidak punya `TEST_DATABASE_URL` sendiri.

## B2.1: hasil (branch `latihan`)
- **Disalin ke `internal/platform/`** (API sama dengan P): `dbx`, `jsonx` (+`F64`), `reqbody`, `idem`, `bg`, `useragent`. Titian tidak punya padanan yang setara. `useragent` P (jenis perangkat, OS, browser, touch points untuk dinding proktor) berbeda dari label woothee di `auth/requestmeta.go`, jadi keduanya tetap ada.
- **Disesuaikan saat disalin:**
  - `reqbody` dan `lx.DecodeJSON` memakai kontrak Titian: setiap body yang tidak cocok adalah 422 `invalid_json_body`. P memakai 415/400/413/422.
  - `idem` membaca `auth.From(ctx).UserID` Titian. Galat 409-nya `idempotency_in_progress`. Tesnya memakai Redis lokal DB 15 (`TEST_REDIS_ADDR`, default `127.0.0.1:6379`, SKIP bila tidak ada) karena Titian tidak memakai miniredis.
  - `bg.Wait(10s)` dipasang di shutdown `cmd/api`.
  - CORS mengizinkan header `Idempotency-Key`.
- **Dipetakan ke padanan Titian** (tidak disalin):
  - `httpx` P → `httpx` T lewat `lx`.
  - `auth` P → `auth.Context` lewat `lx.From`.
  - `tenant` P → `lx.TenantFrom`.
  - `apitest` dan `testdb` P → milik T.
- **`internal/latihan/lx`:**
  - `User{ID, GlobalRole, OrgRole}` dengan `IsAdmin`/`IsSuperAdmin`, serta `From`, `With`, `Tenant{OrgID}.RequireOrgID`, `TenantFrom`, `Resolve`, dan `Middleware(db)`.
  - Galat: `BadRequest`, `Unauthorized`, `Forbidden`, `NotFound`, `Conflict`, `Validation`, dan `PaymentRequired`, semuanya menerima pesan. Bentuknya `{"error": "not_found", "detail": pesan}`, dan pesan P menjadi `detail` yang ditampilkan `ApiError` web.
  - Ada juga `Message(err)`, `Data` (amplop `{"data": ...}` P dipertahankan agar layanan web P di B3.1 tidak berubah), serta alias `Error`, `HandlerFunc`, `Handle`, `OK`, `Status`, `WriteError`, `DecodeJSON`, `PathUUID`, `QueryUUID`, dan `QueryInt`.
  - Kode P cukup diganti impornya: `auth.From` → `lx.From`, `auth.User` → `lx.User`, `tenant.From` → `lx.TenantFrom`, `httpx.` → `lx.`, `access.` → `akses.`.
- **Aturan tenant:**
  - Tenant adalah org aktif dari `auth` T, yaitu header `X-Organization-Id` (atau `?organization_id=` di rute SSE) atau peran bawaan.
  - Peran `student`/`parent` di org `platform` berarti jalur pribadi (`OrgID` nil). Karena itu pelajar mandiri tanpa org, dan siswa sekolah dengan header sekolahnya memakai tenant sekolah.
  - `GlobalRole` = `platform_admin` bila ada baris `platform_admin` di org mana pun. Nilainya dibaca dari DB sekali per request, karena token T tidak membawa peran.
- **`internal/latihan/akses`:**
  - Fungsi yang diport: `IsGlobalAdmin`, `IsAdminFromClaims`, `RequireGlobalAdmin`, `OrgRoles`, `IsOrgAdmin`, `IsOrgStaff` (`org_owner`/`academic_director`), `IsStaff`, `ValidRole`, `ResolveAccess`, `CanPerform`, `CanViewModule`, `CanEditModule`, `CanGradeSubmission`, `TutorScope`, `AssignmentScope`/`AssignmentScopeFor`, `CanProctorModule`, `IsClassTutor` (`fn_has_class_role`), `TutorCoversStudent` (`fn_scoped_role_covers`), dan `CanAuthorInClass` (`classes.organization_id`).
  - Perubahan dari P:
    - Cabang kolaborator program dibuang, karena T tidak punya `org_program_collaborators`.
    - Cabang batch diganti admin org dari `org_assignment_submissions.org_id`: sekolah menilai percobaan siswanya pada isi platform.
    - Kolaborator modul `owner` juga boleh menilai dan masuk `TutorScope`.
    - `AssignmentScopeFor` penuh juga untuk admin org pemilik modul.
    - `CanProctorModule` mengambil org terdekat di rantai folder dengan urutan pasti dan batas kedalaman.
    - Galat kueri admin global di `IsStaff` tidak lagi ditelan.
- **SSE:**
  - `auth.Resolver.SSEMiddleware` menerima `?access_token=` dan `?organization_id=` hanya pada GET, dan hanya pada rute yang memasangnya. Header selalu menang.
  - Parameter dihapus dari URL sebelum handler berjalan. `Middleware` biasa tetap menolak token di query.
  - Alasan keamanan dicatat di komentar fungsi: token di URL bisa bocor lewat log. Log T hanya mencatat path, Caddy tanpa access log, dan token berumur 15 menit. Tiket sekali pakai bisa ditambahkan bila API menjadi banyak instance atau log akses dinyalakan.
- **Tes:**
  - Unit `dbx`, `jsonx`, `reqbody`, `idem`, `bg`, dan `useragent`.
  - `auth/sse_test.go`.
  - `lx_test.go`: kontrak galat dan resolusi tenant untuk admin global, admin org, guru, siswa sekolah, pelajar mandiri, orang tua, dan user tanpa peran.
  - `akses_test.go`: admin global, `org_owner`/`academic_director`, guru kelas vs guru org saja, siswa sekolah, pelajar mandiri, dan langganan plus/pro/kedaluwarsa.
- **Untuk B2.2:**
  - Rute dipasang di `Protected` dengan `r.Route("/latihan", ...)` + `r.Use(lx.Middleware(a.DB))`.
  - Rute SSE dipasang di `Public` dengan `r.With(a.Auth.SSEMiddleware, lx.Middleware(a.DB))`.
  - `labs.IsStaff` P sekarang `akses.IsStaff`.
  - Rujukan `org_classes`/`org_class_members` di kode P (mis. `proctor.getItemConfig`, `labs/rules_db.go` StudentContexts) harus ditulis ulang ke `classes`/`class_members`, dan `semester_id` ke `period_id`.

## B2.2: hasil (branch `latihan`)
- **Berkas** `internal/latihan/`: `latihan.go` (Service, rute, `RequireProgramEditor`, `GrantProgramModules`, `ExpandProgramIDs`, `SyncProgramIntoLinkedContexts`), `modules.go`, `items.go`, `programs.go`, `grants.go`, `pickers.go`, `bank.go`, `my_assessments.go`, `enroll.go` (pendaftaran mandiri, kelas Titian), `gate.go` (akses program dan isi berbayar), `rahasia.go` (penyaring kunci jawaban). `rules.go` dan `rules_db.go` ikut disalin sekarang, karena `listModules`/`getModule` membutuhkannya.
- **Rute** di `Protected`, `r.Route("/latihan")` + `lx.Middleware`. Akhiran sama dengan `/labs` P. Rute baru: `POST /latihan/programs/{id}/enroll`, `GET /latihan/me/programs`, `GET|POST /latihan/classes/{id}/programs`, `DELETE /latihan/classes/{class_id}/programs/{program_id}`, `GET|POST /latihan/{modules|programs}/{id}/product-grants`, `DELETE .../product-grants/{tier}`.
- **Tidak disalin:** semesters/classes/enrollment P (formulir gabung, undangan), produk P (`/products/*`), kolaborator program lintas org, token akses (`resource_access_tokens`, ikut K5), grant email, bentuk lama `module_assignments`, media collection, skill, usage, kunci `phase/open_mode/requires/materi` di aturan (e-learning v2, K9).
- **Kelas Titian:**
  - Siswa = `class_members`, tutor = `classes.teacher_id`, org = `classes.organization_id`, `semester_id` → `classes.period_id`.
  - Pengelola program kelas = admin org atau guru kelas itu.
  - Menautkan program ke kelas mendaftarkan anggota (dengan `class_id` dan `period_id`).
  - Anggota baru didaftarkan lewat `class.Service.OnMemberAdded` → `latihan.Service.ClassMemberAdded` (dipasang di `cmd/api`).
- **Pelajar mandiri:**
  - `POST /programs/{id}/enroll` butuh peran `taker` pada program (public, org, grant, atau langganan).
  - Program yang dijual tanpa langganan yang cukup → 402 `payment_required` dengan tier. Draf hanya untuk editornya.
  - Pendaftaran tanpa `class_id`/`period_id`.
- **`GrantProgramModules` (berubah dari P):** hanya memberi grant ke modul milik org program itu sendiri, dan tidak pernah ke org `platform`. Isi platform tetap di balik visibilitas dan grant produknya. Akibatnya isi berbayar tertutup lagi saat langganan habis, dan sekolah yang menautkan program berbayar ke kelasnya tidak membukanya untuk siswa.
- **Isi berbayar:**
  - `listModules` menampilkan kerangka modul tanpa akses dengan `access_role: ""`, `subscription_tier`, dan item `content_withheld`.
  - `getModule` tanpa akses → 402 bila dijual, 403 bila tidak.
  - `listPrograms` ikut menampilkan program yang dijual (dengan `subscription_tier`, `access_role`, `enrolled`).
  - Hanya admin platform yang boleh memasang grant produk. Role grant produk viewer/taker.
- **Penyaring rahasia (`rahasia.go`):** P (labs) ternyata masih mengirim kunci `kuis_umum` ke browser. Hanya e-learning v2 P yang menyaringnya (`content/secrets.go`), jadi aturannya diambil dari sana dan diterapkan ke semua item Latihan.
  - Per soal dibuang: `answer`, `answers`, `explanation`, `ai_grading_instructions`, `model_answer`, `sample_answer`, `errors`.
  - Per grup/section/deck dibuang `transcript` (kecuali `audio_show_transcript: "always"`) dan `explanation` grup.
  - Di mana saja dibuang: `widget.grading`, `answer_key`, `bank_source`. Pada mock juga `bank`, `book`, `test`.
  - `complete_the_words` dipotong ke huruf awal + `missing_len`.
  - Berlaku untuk non-editor di `getModule`, untuk tampilan siswa di `listModules`, dan untuk snapshot Bank Soal yang tidak ditulis oleh pembacanya. Editor dan guru kelas yang sedang menyusun lapisan kelas (`?class_id=`) tetap menerima config utuh.
- **Bank Soal:**
  - Baca: item tenant (atau milik sendiri di jalur pribadi), ditambah item org platform yang modul sumbernya bisa diakses pembaca. Dengan begitu grup dari test berbayar tidak bisa dilatih tanpa langganan.
  - Tulis: peran pembuat isi di tenant (`org_owner`, `academic_director`, `curriculum_developer`, `teacher`, `tutor`, `platform_admin`), atau milik sendiri di jalur pribadi.
- **Bug P yang diperbaiki** (tanpa cek akses atau terlalu longgar di P):
  - `getProgram`, daftar modul program, tautkan/lepas modul, prasyarat, urutkan modul dan sub-program kini butuh akses.
  - Duplikasi modul kini butuh hak edit sumber, karena salinannya membawa semua kunci.
  - Membuat modul di org butuh peran pembuat isi. Pindah ke folder butuh hak edit folder, dan dicek sebelum ada yang ditulis.
  - Memberi peran `owner` butuh `manage_access`.
  - Kolaborator dikelola pemilik modul (termasuk admin org), dan perannya divalidasi (400, bukan 500).
  - `public_role` hanya `viewer`/`taker`.
  - `listPrograms` tidak lagi membocorkan semua program org ke siapa pun yang menyebut `org_id`.
  - Revoke grant biasa tidak bisa mematikan grant produk.
  - Daftar modul (`listAllModules`, `my-modules`) memakai `resolve_resource_access`, sehingga `can_edit` = editor/owner (P menghitung tutor juga).
- **`lx.Resolve` (B2.1) diperbaiki:**
  - Admin platform juga memegang peran `student` bawaan di org platform. Dengan header `X-Organization-Id` platform, `auth` memilih satu baris tanpa urutan, sehingga admin bisa terbaca sebagai pelajar mandiri.
  - Sekarang peran selain `student`/`parent` di org itu yang menentukan. Kasus ini ditambahkan di `lx_test.go`.
- **Tes:**
  - `api_test.go`:
    - CRUD modul, item, program, grant, dan kolaborator.
    - Rahasia: siswa dan tutor tanpa kunci, editor/admin org/guru kelas utuh.
    - Admin org, guru kelas, dan siswa sekolah lain.
    - Pelajar mandiri mendaftar program publik.
    - Isi berbayar: plus, pro, dan langganan kedaluwarsa.
    - Bank Soal, picker.
  - `rules_db_test.go`: aturan kelas pada `class_members`, siswa tidak bisa memilih kelas lain, gerbang item, progres per konteks.
  - `rules_test.go`: salinan P. `rahasia_test.go`.
  - `cmd/api/latihan_routes_test.go`: rute terpasang, tanpa token 401.
- **Untuk B2.3:**
  - Runner menambah rute ke grup `/latihan` di `latihan.go`. `EnsureItemOpenForStudent`, `RecordProgressContexts`, `MarkModuleCompletions`, `StudentClassForItem`, `ProctorOverlayForStudent`, dan `requireScopeEditor` sudah ada di `rules_db.go`. `learning_rules.go` (editor aturan, `PUT /learning-rules`) belum.
  - Submit harus memeriksa akses modul (`CanPerform submit`, 402 lewat `denyResource` untuk isi berbayar) selain `EnsureItemOpenForStudent`, karena pendaftaran tidak lagi membuka modul platform.
  - Karena config yang dikirim ke siswa tanpa kunci, `scoring_detail` buatan klien tidak bisa dipercaya untuk benar/salah. Server menilai ulang dengan `grading.Verify` dari config DB, dan respons submit (atau endpoint review setelah kumpul, bila `result_show_key` tidak `false`) harus membawa kunci dan pembahasan per soal untuk layar hasil. Ini perlu dicek di player B3.2.
  - Draw (`question_draw`): deck yang dikirim ke siswa juga harus lewat `StripConfigSecrets`.
  - `org_assignment_submissions.org_id` diisi dari `lx.TenantFrom` (catatan B1.2).
- **Untuk B4.1 (impor bank):**
  - Test gratis diberi `visibility = 'public'` + `public_role = 'taker'` di modulnya.
  - Test berbayar diberi grant produk per modul. Grant produk pada program saja tidak membuka modulnya.
  - Program dibuat `public` agar kerangkanya tampil.
- **Kinerja:** daftar modul/program memanggil `resolve_resource_access` per baris setelah prasaring murah (`moduleCandidates`). Ini cukup untuk ribuan modul. Bila bank sudah besar, ukur ulang.

## B2.3: hasil (branch `latihan`)
- **Berkas:** `internal/latihan/runner.go` (runner), `learning_rules.go` (editor aturan), `internal/latihan/grading/` (salinan `internal/grading` P + `complete.go`), tes `runner_test.go` dan `grading/complete_test.go`. `internal/grading` T tidak disentuh (tetap untuk Belajar). `ItemGuardForStudent` ditambahkan di `rules_db.go` (`EnsureItemOpenForStudent` kini membungkusnya), dan `countsTowardCompletion` di `rules.go` tidak menghitung item `practice`.
- **Rute** (grup `/latihan`):
  - Runner: `POST /items/{item_id}/progress`, `GET|PUT|DELETE /items/{item_id}/draft`, `POST /items/{item_id}/clock`, `POST /items/{item_id}/submit` (dibungkus `idem.Wrap`), serta dua rute baru `GET /items/{item_id}/deck` dan `GET /items/{item_id}/review?submission_id=`.
  - Aturan: `GET /learning-rules/editor`, `PUT /learning-rules`, `GET /classes/{id}/item-progress`, `GET /programs/{id}/my-authoring`, `GET /my-classes`. Di respons, `batch_name` P menjadi `period_name` (`periods`).
- **Akses runner (`requireTaker`):**
  - Submit, simpan draf, jam ujian, deck, dan tandai selesai di `/progress` butuh `CanPerform(module, submit)`. Isi berbayar tanpa langganan mendapat 402 lewat `denyResource`.
  - Item yang belum terbit (atau berada di bawah section yang belum terbit) → 404, kecuali bagi editor modul. Section → 400.
  - P tidak memeriksa apa pun di sini, dan draf P menerima id apa saja.
- **Penilaian di server:**
  - `grading.Complete` (baru) membuat `scoring_detail` berisi tepat satu entri per soal config. Soal yang tidak dikirim klien dihitung kosong, dan nomor yang tidak ada di config dibuang. Bug P: `Verify` hanya menilai entri yang dikirim, jadi siswa bisa menaikkan persentase dengan membuang soal yang salah. Deck acak tetap lewat `ApplyDraw`.
  - Full mock (`sections[].config`) kini dinilai per section. Section yang tidak dikirim dihitung kosong. `score`/`max_score` section ditulis server. Di P, full mock tidak dinilai ulang sama sekali.
  - Klaim klien (`score`, `percentage`, `ai_score`, `ai_feedback`, `ai_eval_results`, serta `band`/`itp_counts`/`overall_*`/`toefl_itp` full mock) tidak dipakai sebagai nilai, tetapi disimpan di `metadata.client_reported`. `final_score` = persentase terverifikasi, atau NULL bila tidak ada yang bisa dinilai otomatis (writing, speaking, unggahan).
  - `ai_eval_results` dari klien dibuang sebelum `Verify`. Di P, isian itu memberi poin esai sesuai band yang diklaim klien.
- **Submission:**
  - `org_id` = `lx.TenantFrom` (sekolah siswa; NULL untuk pelajar mandiri), dan `module_item_id` ikut diisi.
  - `org_assignments.org_id` tetap org pemilik isi. `assignment_type` diambil dari `content` item, bukan dari klien.
  - Satu transaksi mencakup kunci advisory per (siswa, item), cek `max_attempts`, insert, pindah `org_proctor_events`/`locks`/`frames` ke `submission_id`, hapus draf, dan progres item. Dengan begitu kiriman serentak berkunci berbeda tidak bisa melewati batas, dan assignment item tidak terbuat dua kali.
  - Setelah commit, `RecordProgressContexts` dan `MarkModuleCompletions` dijalankan; di P keduanya hanya lewat `/progress`. `cascadeProgress` berjalan di `bg`. `Service.HandedIn` sudah ada dan menunggu dipasang di B2.4.
- **Practice** (`completion_rule` efektif `practice`, dari `guard_config` item atau aturan org/program/kelas):
  - Tetap dinilai dan disimpan dengan `metadata.practice = true`.
  - `max_attempts` tidak berlaku, dan percobaan practice tidak mengurangi jatah percobaan biasa. Respons membawa `practice: true` dengan `max_attempts: null`.
  - Item practice tidak dihitung untuk kelulusan modul (`countsTowardCompletion`) dan progres modul/program (`cascadeProgress`, berdasarkan `guard_config` item sendiri).
- **Kunci jawaban:**
  - Respons submit dan `GET /review` membawa `review` (`scoring_detail` terverifikasi + `question_groups` dengan kunci dan pembahasan; untuk deck acak dipakai deck tersimpan; untuk full mock per section) hanya bila `result_show_key` tidak `false`. Bila `false`, benar/salah per soal juga tidak dikirim.
  - `final_score` hanya dikirim bila `result_show_score` tidak `false`.
  - `GET /deck` membangun deck di server (`DrawDeck`, seed sama dengan penilaian) dan mengirimnya lewat `StripConfigSecrets`, kecuali kepada editor.
- **Tes** (`runner_test.go`):
  - Jawaban palsu `is_correct: true` + soal dibuang + nomor palsu → 33,33.
  - Siswa sekolah mendapat `org_id` sekolah. Hand-in tanpa jawaban → 0. Writing → tanpa skor, klaim tersimpan.
  - Flag `result_show_key`/`result_show_score`. Deck acak.
  - `close_at`, `open_at`, `daily_*`, aturan kelas oleh guru kelas (guru lain 403), dan editor aturan.
  - Practice ×3 tanpa kelulusan modul, lalu kuis wajib menyelesaikan modul.
  - `max_attempts` dan 4 kiriman serentak → 1 baris.
  - Kunci idempotensi sama → 1 baris (Redis lokal DB 15, SKIP tanpa Redis).
  - 402 untuk submit/draft/clock/deck. Modul privat 403, item draf 404, section 400.
  - Draf dibatasi 300 dtk, simpan kosong tidak menghapus jawaban, event/kunci/frame pindah ke submission, draf terhapus.
  - Tes ini lulus bersama seluruh `internal/latihan/...`, `cmd/api`, `internal/platform/...`, `internal/grading`, `go vet ./...`, dan `go build ./...`.
- **Untuk B2.4 (proktor):**
  - Pasang `latihan.Service.HandedIn` di `cmd/api`.
  - Event/kunci/frame sudah dipindah di transaksi submit, jadi proktor tidak perlu memindahnya lagi.
  - `PUT /items/{id}/draft` (anchor proktor) kini butuh peran submit.
  - `ProctorOverlayForStudent` ada di `rules_db.go`, dan `proctor_config` lewat `PUT /learning-rules`.
- **Untuk B2.5 (penilaian):**
  - Setiap tampilan submission untuk siswa harus memakai aturan `result_show_key`/`result_show_score` yang sama (`resultFor` di `runner.go`). `answers_data` tersimpan berisi deck lengkap dengan kunci untuk config acak.
  - Penilaian AI Writing/Speaking harus dijalankan di server. Klaim klien ada di `metadata.client_reported` dan tidak boleh dipakai sebagai nilai.
  - Submission `metadata.practice = true` jangan masuk antrean penilaian wajib, rekap nilai, atau bukti unit (B2.7).
  - Band IELTS/ITP full mock tidak disimpan server; web (B3.2) menghitungnya dari `score`/`max_score` section terverifikasi. Bila server perlu band, port tabel `ieltsBands`/`toefl-itp-score`.
  - `vocab_mastery` (dinilai klien di P) kini tanpa skor sampai ada penilai server.
- **Untuk B3.2 (player):** pakai `GET /items/{id}/deck` atau `drawDeck` web dengan seed `user:item` (full mock: seed yang sama untuk setiap section). Layar hasil membaca kunci dari `review`, bukan dari config.

## B2.4: hasil (branch `latihan`)
- **Berkas** `internal/latihan/proktor/`: `proktor.go` (Service, rute, akses, config bertingkat, event, kunci, log, ringkasan), `autolock.go`, `freeze.go`, `reentry.go`, `resolver.go`, `hub.go`, `sse.go`, `live.go`, `live_audio.go`, `collab.go`, `handin.go`, `wall.go`, `wall_feed.go`, `wall_cache.go`, `wall_org.go`. Tes: `proktor_test.go`, `api_test.go`, `pipe_test.go`, `wall_feed_test.go`.
- **Pemasangan:**
  - `latihan.Service.Mounts` (baru) memasang `proktor.Service.Routes` di grup `/latihan` yang sama, di belakang `lx.Middleware`. Grup itu tidak bisa dipasang dua kali di chi.
  - `proktor.Service.Module()` memasang tiga rute SSE di Public dengan `a.Auth.SSEMiddleware` + `lx.Middleware`: `GET /latihan/modules/{id}/proctor-stream`, `GET /latihan/drafts/{draft_id}/live-stream`, `GET /latihan/drafts/{draft_id}/collab-stream`. Rute statis itu tidak menutupi rute grup berawalan sama (dicek di `cmd/api/latihan_routes_test.go`).
  - `latihan.Service.HandedIn` = `proktor.Service.SubmissionHandedIn` di `cmd/api`. Skor `nil` (writing, speaking, unggahan) dikirim sebagai `pending`.
- **Rute lain** (akhiran sama dengan `/labs` P): `GET|PUT /items/{id}/proctor-config`, `GET /items/{id}/effective-proctor-config`, `GET|PUT /modules/{id}/proctor-config`; `/drafts/{draft_id}/` + `proctor-events`, `lock-status`, `send-unlock-code`, `lock`, `unlock`, `lock-history`, `unlock-by-code`, `events`, `proctor-summary`, `live`, `audio`, `collab/start|stop|update`; `GET /modules/{id}/proctor-wall|proctor-feed|proctor-identity-fields`, `GET /orgs/{org_id}/proctor-wall`, `GET|POST /modules/{id}/proctors`, `DELETE /modules/{id}/proctors/{user_id}`, `GET|POST /modules/{id}/class-proctors?class_id=`, `DELETE /modules/{id}/class-proctors/{user_id}?class_id=`.
- **Tidak disalin atau ditunda:**
  - Share (K5) dan e-learning v2: semua event, kunci, dan frame hanya menempel ke draft atau ke submission. `OverlayShareLink`, `SummaryFor`, `VerifyLegacyOrCreator`, `ResolveForAttempt` (`org_exam_packages`), baris wall share/elv2, dan jam `elv2_lesson_state` dibuang.
  - Identitas pendaftaran: T tidak punya formulir pendaftaran batch/kelas (`enrollment_data`). `GET .../proctor-identity-fields` tetap ada dan menjawab `[]`, dan baris wall tanpa `identity`. Pelajar dibedakan lewat email.
  - Audio live tidak butuh LiveKit/TURN. Potongan suara direlai lewat hub SSE yang sama, jadi ikut disalin. Kolaborasi Yjs juga disalin, karena `live.go` memakainya dan servernya hanya relai di memori.
  - Hub, keadaan live, ruang kolaborasi, dan hand-in tersimpan di memori satu instance API, sama seperti P.
- **Akses (berubah dari P):**
  - Config proktor modul diubah oleh yang boleh mengedit modul (`CanEditModule`), dan item kelas juga oleh penulis kelas itu (`CanAuthorInClass`), sama seperti bagian modul lainnya. P hanya mengizinkan admin org. Fallback P "konten tanpa org boleh diatur admin tenant mana pun" dibuang.
  - Guru kelas yang kelasnya memuat modul boleh membaca config (hanya baca), lewat `classes.teacher_id`.
  - Menambah atau mencabut pengawas modul butuh `manage_access`, sama seperti kolaborator lain. Pengawas yang sudah editor/owner tidak diturunkan menjadi `proctor` (bug P), dan viewer dinaikkan.
  - Draft boleh diawasi oleh:
    - `CanProctorModule` (editor, kolaborator `proctor`/`tutor`, admin org pemilik, admin platform);
    - guru kelas lewat `TutorCoversStudent`;
    - pengawas kelas dari `org_class_module_proctors` × `class_members`;
    - **baru:** admin sekolah untuk siswa di kelas sekolahnya yang memuat modul. Ini agar sekolah bisa mengawasi siswanya pada isi platform.
  - Pelajar mandiri tidak punya kelas, jadi hanya pengawas modul (admin platform, kolaborator) yang melihat draftnya, dan tidak ada overlay aturan kelas.
  - Wall organisasi memuat modul milik org ditambah modul org lain yang dimuat kelas org itu. Untuk modul org lain, barisnya diambil per kelas (scope kelas). `batch_*` P menjadi `period_id`/`period_name`.
- **Perbaikan lain dari P:**
  - Config item di `hello` live-stream dikirim tanpa kunci jawaban (`StripConfigSecrets`) bila pengawas bukan editor modul.
  - Hand-in menutup ruang kolaborasi draft itu; di P ruang itu tertinggal di memori.
  - `submission_status` di baris draft hanya menghitung kiriman setelah draft dimulai. Di P, draft percobaan ulang terbaca "submitted".
  - Kunci otomatis hanya dibuat bila belum ada kunci aktif, sehingga dua batch serentak tidak membuat dua kunci.
  - `module_item_id` event di luar modul draft diganti item draft. Satu kiriman paling banyak 500 event. `reason` kunci manual paling panjang 60 karakter (422, bukan 500).
  - `config` proktor harus objek atau `null` (422).
  - Overlay aturan kelas dipakai juga untuk `freeze_timer_on_lock` lewat `effectiveFor`.
- **Tidak memindah ulang:** proktor tidak pernah memindahkan event/kunci/frame. Pemindahan tetap di transaksi submit B2.3, dan `HandedIn` hanya memberi tahu penonton, mencatat hand-in di memori 6 jam, serta membuang keadaan live dan ruang kolaborasi.
- **Tes:**
  - Unit dari P: merge, overlay, aturan kunci, aturan `violation`, kode buka, hub, feed (satu kepergian sekali, offline di jam halaman), dan cache wall.
  - Integrasi di sekolah Titian:
    - Config bertingkat dan siapa boleh membaca/menulis.
    - Kunci otomatis setelah 2 tempel, kode buka (tidak terlihat sebelum dikirim, huruf kecil berspasi diterima), kunci manual, dan jam dibekukan ±60 dtk.
    - Wall, ringkasan, log, serta pengawas modul diberi dan dicabut (editor tidak turun).
  - Guru kelas lain ditolak (wall, feed, kunci, log), pengawas per kelas, dan wall organisasi dua kelas.
  - Pelajar mandiri tanpa overlay kelas dan tanpa pengawas kelas/sekolah, sementara siswa sekolah pada isi platform mendapat aturan kelas yang lebih ketat dan diawasi sekolahnya.
  - SSE dengan `?access_token=`: event modul lain dan detak tidak terkirim, langganan berakhir saat klien pergi, 401/403.
  - Hand-in saat ditonton: SSE `handin` di live-stream dan stream modul, log pindah sekali, wall dan feed membaca log di submission, live-stream yang dibuka sesudahnya tetap menerima `handin`, siswa 403, ruang kolaborasi tertutup.
  - Mutasi (klausul admin sekolah dan autolock dimatikan) membuat tes gagal seperti seharusnya. Lulus juga dengan `-race`.
- **Untuk B2.5:** `proktor.Summary(ctx, q, "submission_id", id)` siap untuk log pengerjaan di halaman hasil. Frame putar ulang ada di `org_proctor_frames.submission_id`, tetapi endpoint pembacanya belum ada (P: `/elearning-v2/attempts/{id}/frames`). Siapa boleh membaca: pemilik submission atau `canProctorDraft`-setara. `proctor_config_snapshot`/`proctor_summary` di submission belum diisi siapa pun.
- **Untuk B3.3:**
  - Klien SSE memakai `?access_token=` (+ `?organization_id=` untuk tenant sekolah).
  - Pesan modul membawa `student_id` dan `draft_id` (kunci otomatis juga `anchor_column`/`anchor_id` seperti P).
  - `hello` live membawa `item.content` tambahan.
  - Wall organisasi memakai `period_*`, bukan `batch_*`.
  - Kolom identitas selalu kosong.

## B2.5: hasil (branch `latihan`)
- **Berkas** `internal/latihan/nilai/`: `nilai.go` (Service, rute, `Evaluator`, `graderSQL`), `submissions.go` (tampilan siswa, detail, PATCH, nilai tutor, edit jawaban, antrean, log pengerjaan), `evaluate.go` (penilaian AI di server, ringkasan proktor saat kumpul, re-evaluate, rencana belajar), `annotations.go`, `tutor.go`, `export.go` (xlsx/csv, `excelize` v2.9.0 ditambahkan ke `go.mod`), `titian_ai.go` (adapter). AI: `internal/ai/latihan_nilai.go` dan `internal/ai/prompts_latihan.go`. `prompts_gen.go` tidak disentuh karena berkas hasil generator.
- **Rute** (grup `/latihan`, lewat `latihan.Service.Mounts`): `GET /items/{id}/submissions/my`, `GET /submissions/queue`, `GET|PATCH /submissions/{id}`, `POST /submissions/{id}/grade|re-evaluate|generate-learning-plan|mark-reviewed`, `PATCH /submissions/{id}/answers`, `GET|POST /submissions/{id}/annotations`, `PATCH|DELETE /submissions/annotations/{annotation_id}`, `GET /submissions/{id}/proctor-log` (baru), `GET /tutor/scope|submissions|tree`, `GET /tutor/assignment/{id}/analytics|raw-submissions|export.csv|export.xlsx`, `GET /modules/{id}/results`, `GET /modules/{id}/results/export.xlsx`, `GET /modules/{id}/speaking-queue`.
- **Peran AI:** memakai peran yang sudah ada, tanpa peran baru. `writing_evaluation` untuk esai dan rencana belajar, `stt` untuk transkrip rekaman, `speaking_evaluation` untuk penilaian rekaman. Setiap panggilan dicatat di `ai_tasks` (prompt_id `latihan_*_v1`). Kredit tidak dipotong, karena Latihan dibuka lewat langganan.
- **Prompt:**
  - Writing memakai `evaluation.writing.general` P (versi migrasi 0192+0208). Rubrik guru (`ai_grading_instructions`, termasuk rubrik IELTS/PTE di config item) menjadi rubrik utama, dan rubrik IELTS empat kriteria jadi bawaan.
  - Speaking memakai `tutor_eval_system.txt`/`tutor_eval_ielts.txt` P. Bagian Praat dibuang karena T hanya punya transkrip, dan pelafalan disebut perkiraan.
  - Rencana belajar memakai bagian `learning_plan` dari `evaluation.writing.enriched`. Panggilan "enriched" kedua (jalur CEFR, contoh band) tidak dijalankan.
  - Band dihitung server dari kriteria (rata-rata, dibulatkan ke 0,5). Band dan CEFR dari model tidak dipercaya.
- **Alur kumpul:** runner memanggil `latihan.Service.Submitted` (= `nilai.Service.Submitted`) setelah commit.
  1. `proctor_config_snapshot` diisi dengan config efektif (`proktor.EffectiveFor`, termasuk overlay kelas) bila ada config. `proctor_summary` (`proktor.Summary` pada submission) diisi bila ada config atau event. Snapshot diambil saat kumpul, bukan saat mulai.
  2. Penilaian AI berjalan di `bg` untuk: `writing`/`ielts_writing`; soal grup `essay`/`freeform_eval` di kuis (hasil ke `ai_eval_results`, lalu `grading.Verify`, sehingga poin esai mengikuti band); section full mock (soal esai di section berkuis; section writing tanpa `question_groups` → `ai_band` di section, skor otomatis mock tidak berubah); dan `speaking_record`. Untuk `speaking_record`, rekaman harus `assets.user_id` milik siswa, transkrip disimpan di `responses[].transcript` dan `ai_transcription`, dan skor = band IELTS/9, atau rata-rata lima skor ×10. IELTS dipakai bila `rubric_ids` memuat "ielts", `theme: ielts`, atau `ielts: true`.
  3. `ai_evaluate: false` di config item mematikan penilaian otomatis, tetapi re-evaluate manual tetap bisa.
  4. Bila AI gagal, submission tetap `submitted` untuk tutor. Re-evaluate yang gagal menjawab 502 `ai_unavailable` (`lx.AIUnavailable`, baru).
  5. Practice tetap dinilai AI agar siswa melihat umpan balik.
- **Nilai tutor menimpa AI:** `final_score` = `tutor_score` begitu ada. Penilaian AI, PATCH, dan edit jawaban sesudahnya hanya mengubah `ai_score`, sedangkan `final_score` tetap nilai tutor. Tanpa nilai tutor, skor AI menjadi final. `tutor_score` harus 0–100 (422).
- **`vocab_mastery`:** dinilai server tanpa AI (`grading.VocabMastery`, dipanggil di `gradeHandIn`). Skornya = kata di `word_list` config yang punya `mastered_at` untuk setiap `target_aspects` (bawaan recall/meaning/spelling), lalu `passed` dihitung terhadap `pass_threshold_pct` (bawaan 85). Matriksnya tetap catatan latihan klien: server menghitung dari matriks, bukan memutar ulang latihannya. Ringkasan AI P (`/labs/ai/vocab-mastery-summary`) tidak disalin.
- **Tampilan siswa** (`learnerView`, dipakai di `GET /submissions/{id}` untuk pemilik dan di `/items/{id}/submissions/my`):
  - Mengikuti `latihan.ResultFor` (diekspor dari `runner.go`, bersama `ShowFlag`).
  - Tanpa `answers_data`, config, atau deck. Jawaban sendiri dikirim di `my_answers`.
  - `ai_score`, `tutor_score`, `rubric_scores`, dan `evaluation` (hasil AI) hanya dikirim bila `result_show_score` tidak `false`.
  - Grader mendapat baris utuh dengan config gabungan.
- **Akses:**
  - Antrean, riwayat (`/tutor/submissions`), dan hitungan di pohon memakai `graderSQL`, yaitu predikat yang sama dengan `akses.CanGradeSubmission`: kolaborator modul tutor/editor/owner, admin org pemilik isi atau sekolah tempat percobaan dibuat, dan guru kelas lewat `fn_scoped_role_covers`. Admin platform melihat semua.
  - Bug P yang diperbaiki:
    - `/tutor/tree` dulu menampilkan seluruh pustaka ke siapa saja.
    - Siswa dulu boleh PATCH `ai_score`/`status`/`ai_feedback` submission-nya; kini PATCH hanya untuk grader, `ai_score` tidak pernah diambil dari request, dan status divalidasi.
    - `GET /submissions/{id}` dulu mengirim config gabungan (kunci dan `grading_criteria`) ke siswa.
  - `assignmentScope` (analitik, raw, ekspor per assignment) menambah siswa dari sekolah yang dipimpin admin (`s.org_id`).
  - Hasil modul: `view_analytics` modul, atau `class_id` dengan `CanAuthorInClass` (filter `class_members`).
  - `proctor-log` boleh dibaca pemilik, grader, atau `proktor.CanProctorStudent` (diekspor dari `canProctorDraft`).
- **Practice** (`metadata.practice`) dikeluarkan dari antrean, riwayat tutor, pohon, hasil modul, ringkasan, ekspor xlsx/csv, analitik, raw, dan speaking-queue.
- **Tidak disalin:**
  - `POST /assignments` dan `/assignments/{id}/submit` (diganti submit item; P membiarkan siapa saja membuat assignment).
  - Backfill anotasi AI (T belum punya submission lama), hasil e-learning v2, dan nama dari `enrollment_data` (T memakai `users.name`).
- **speaking-queue:** roster = pendaftar aktif program yang memuat modul (termasuk program induk), ditambah yang sudah mengumpulkan. Pengganti `module_assignments` P.
- **Tes:**
  - `nilai/api_test.go` dengan AI palsu `fakeAI`, tanpa model sungguhan:
    - Antrean guru A hanya siswa A, guru B hanya siswa B, admin sekolah keduanya, admin sekolah lain dan siswa kosong. Practice tidak masuk. Akses silang 403. Hitungan pohon.
    - Nilai tutor menimpa AI, termasuk setelah re-evaluate dan PATCH. Klaim `ai_score` klien diabaikan. AI gagal → `submitted`, lalu 502.
    - Esai di kuis.
    - Anotasi: AI → anotasi, edit anotasi AI jadi milik tutor, hanya penulis yang boleh mengubah, re-evaluate tidak menghapus anotasi tutor.
    - Kunci tersembunyi tidak bocor di tiga endpoint, dan `grading_criteria` speaking tidak terlihat siswa.
    - Transkrip dan penilaian rekaman. Rekaman milik orang lain tidak dibaca.
    - Hasil, xlsx modul, xlsx/csv per assignment per kelas, tanpa practice.
    - Snapshot proktor dan log.
  - `nilai/unit_test.go`, `nilai/export_test.go` (salinan P), `grading/vocab_test.go`, dan `ai/latihan_nilai_test.go` (`ai.Fake`: band dari server, baris `ai_tasks`, rubrik empat kriteria yang dijawab satu ditolak, skala guru 0–4).
  - Lulus bersama `internal/latihan/...`, `cmd/api`, `internal/ai`, `internal/platform/...`, `go vet ./...`, dan `go build ./...`.
- **Untuk B2.7 (bukti unit):**
  - Skor final ada di `final_score`. Bukti sebaiknya ditulis saat status final: `submitted` dengan skor otomatis, `ai_graded`, atau `graded`.
  - Bukti perlu diperbarui saat `grade`, penilaian AI (`storeMarking`), atau edit jawaban mengubah `final_score`. Titik kaitnya ada di `nilai`.
  - Practice dikecualikan (`notPractice`).
- **Untuk B3:**
  - Player tidak lagi memanggil `/ai/*/evaluate` atau PATCH skor. Layar hasil membaca `GET /submissions/{id}` (`evaluation`, `my_answers`, `review`) dan menunggu status `ai_graded` (polling).
  - Kunci anotasi esai kuis adalah nomor soal. Di full mock kuncinya `sectionId:nomor`, dan writing section memakai `sectionId`.
  - Endpoint frame putar ulang (`org_proctor_frames.submission_id`) belum dibuat. `proctor-log` sudah ada.

## B2.7: hasil (commit `6590187`, branch `latihan`)
- **Berkas:** `db/migrations/0120_latihan_bukti_unit.sql`, paket baru `internal/latihan/bukti/` (`bukti.go`: penanda, `Check`, `Sync`; `routes.go`: endpoint baca; `bukti_test.go`), hook di `runner.go` dan `nilai/{nilai,evaluate,submissions}.go`, cek penanda di `items.go`, `grading.NumberKey` (ekspor), `cmd/api` memasang `bukti.Service.Routes` di `Mounts`. Tes integrasi `nilai/bukti_test.go`.
- **Penanda (`config.titian`):** `{unit: [...], jalur: [...], peran: "kemasan"|"cek"|"ujian"}` di item. Unit boleh juga ditulis di section full mock (`section.titian` atau `section.config.titian`), grup soal (`group.titian`), dan soal (`question.titian`). Tingkat paling dalam yang menang (soal menggantikan grup, grup menggantikan section/item), dan `unit: []` berarti "tidak menguji unit". Unit = `canon_units.module_id` (atau `id`). `jalur` disimpan apa adanya dan belum dipakai server.
- **Cek saat simpan:** create/PATCH item menolak (422) bentuk `titian.unit` yang bukan teks/daftar teks, `peran` lain, dan unit yang tidak ada di `canon_units`.
- **Tabel `latihan_bukti_unit`:** PK (`submission_id`, `unit_id`), `user_id`, `module_item_id`, `org_id` (sekolah tempat percobaan; NULL untuk pelajar mandiri), `peran`, `benar`/`total` (poin terverifikasi soal unit itu; NULL bila tidak ada soal bernilai per soal), `skor` 0–100, `sumber` (`otomatis`/`ai`/`tutor`), `submitted_at`. FK cascade ke submission, unit, dan user; set null ke item dan org.
- **`bukti.Sync(ctx, q, submission)`** menghitung ulang bukti satu submission dari DB dan dipanggil di **transaksi yang sama** dengan setiap perubahan skor/status: kumpul di runner (sebelum commit), `storeMarking` (AI), `grade`, `PATCH /answers`, dan `PATCH /submissions/{id}` (lewat `nilai.Service.changeScore`). Proktor, anotasi, `mark-reviewed`, dan rencana belajar tidak mengubah skor, jadi tidak memanggilnya.
- **Kapan ada bukti:** `final_score` tidak NULL **dan** status `submitted`/`ai_graded`/`graded`/`returned` **dan** bukan practice. Selain itu baris submission dihapus (mis. PATCH ke `pending_review`), dan muncul lagi bila kembali final.
- **Skor per unit (keputusan sendiri):**
  - Ada soal bernilai di unit itu → `benar/total × 100`.
  - Tanpa soal bernilai (writing, speaking, unggahan, section writing full mock) → `final_score`.
  - Unit yang semua soalnya masih menunggu penilaian (esai di kuis sebelum AI menilai) → **belum ada baris**, agar skor bagian lain tidak dipinjam. Baris muncul saat penilaian menyimpan skornya.
  - Ada `tutor_score` → semua unit memakai skor tutor (`sumber: tutor`), sama seperti `final_score`. `benar`/`total` tetap disimpan untuk rincian.
- **Status unit tidak berubah:** tidak ada yang ditulis ke `card_progress`, dan status unit tetap dibaca `kartu.standings` dari deck materi (ADR-0026 aturan 3). Tes memeriksanya di setiap skenario.
- **Endpoint** (grup `/latihan`):
  - `GET /me/bukti?subject=` → per unit: `unit_id`, `unit` (module_id), `name`, `subject_code`, `attempts`, `best_skor`, `last_skor`, `last_at`, urut terbaru.
  - `GET /me/bukti/{unit}` (module_id atau id) → `{unit, bukti: [...]}`, paling banyak 100 percobaan terbaru: `submission_id`, `module_item_id`, `item_title`, `module_id`, `module_title`, `org_id`, `peran`, `benar`, `total`, `skor`, `sumber`, `submitted_at`, `skor_hidden`. 404 bila unit tidak dikenal.
  - Bukti milik akun, lintas org (satu catatan pengetahuan per akun), jadi tenant tidak menyaring.
  - Item dengan `result_show_score: false` tetap menjadi bukti, tetapi `skor`/`benar`/`total` dikirim NULL dan tidak masuk `best_skor`/`last_skor`. `result_show_key: false` menyembunyikan `benar`/`total`.
- **Tidak dibuat:** node jalur `latihan` (`canon_path_nodes`). Bukti sudah menempel ke unit, jadi tampil di semua jalur yang memuat unit itu tanpa node baru. Node baru mengubah CHECK `node_type` dan pembaca jalur (`catalog`, `kartu`) yang butuh tes sendiri. Usulan: dibuat di B4.2 saat try out TKA/SNBT pertama perlu ditautkan dari jalur. Belum ada pula tampilan bukti untuk guru/orang tua.
- **Tes:**
  - `nilai/bukti_test.go`: kuis bertanda (A 1/2, B 1/1, C 0/1, org sekolah, peran `ujian`), edit jawaban tutor menaikkan A, nilai tutor menjadi skor semua unit, `pending_review` menghapus bukti lalu `graded` mengembalikannya, ringkasan dan daftar per unit (module_id dan id), unit tak dikenal 404, teman sekelas tidak melihat; practice (juga setelah dinilai tutor) tanpa bukti; skor tersembunyi; 422 untuk unit tak dikenal, peran salah, dan unit bukan teks; esai (sumber `ai`, lalu `tutor`, re-evaluate tidak menggeser skor tutor); esai di kuis saat AI gagal tidak membuat baris unit esai, lalu re-evaluate membuatnya; pelajar mandiri (`org_id` NULL) dan siswa sekolah pada item platform yang sama.
  - `bukti/bukti_test.go`: pewarisan unit di full mock (section, config section, grup `unit: []`, soal), entri `needs_eval`, deck acak dibaca dari jawaban.
  - Mutasi (cek practice dibuang, `Sync` di `changeScore` dimatikan) membuat tes gagal. Lulus bersama `internal/latihan/...`, `cmd/api`, `internal/kartu`, `internal/platform/...`, `go vet ./...`, dan `go build ./...`.
- **Untuk B3 (web):**
  - Profil/Peta membaca `GET /latihan/me/bukti` (ringkasan, bisa per `subject`) dan `GET /latihan/me/bukti/{unit}` (rincian). Tampilkan sebagai "bukti latihan" di samping status unit dari `/kartu/*`, bukan sebagai status. `skor_hidden` berarti item menyembunyikan skor.
  - Editor item (B3.4) perlu pemilih unit kanonik untuk `config.titian.unit` di item, grup, dan soal, serta `peran`. Server menolak unit yang tidak dikenal (422, `detail` berisi daftarnya).
  - Bukti esai muncul setelah AI selesai menilai, jadi layar hasil yang menunggu `ai_graded` juga menunggu buktinya.
- **Untuk B4.2:** konversi kuis bab mengisi `config.titian.unit` (dan per soal bila satu bab mencakup beberapa unit). Unit yang id-nya diganti oleh seed kanonik membuat buktinya ikut terhapus (cascade); seed kanonik memakai `on conflict (module_id)`, jadi id unit yang tetap tidak berubah.

## B3.1: hasil (commit `b5087b7`, branch `vite` di `titian-web-vite`)
- **Berkas:** `src/lib/latihan/quiz/**` (salinan `lib/quiz` P, 85 berkas), `src/lib/latihan/{api,types,org-store,answer-match,speech,media-compat,markdown-math,draft-store}.ts`, `src/hooks/use-latihan.ts`, `src/components/latihan/markdown-viewer.tsx`, `src/components/latihan/editor/quiz-rich-text-modal.tsx`, `src/components/ui/{alert-dialog,retry-dialog}.tsx`, `vitest.config.ts`.
- **Klien API (`api.ts`):** di atas `authedRequest` T (kini diekspor, bersama `authedBlobRequest` dan `freshAccessToken` baru di `api-client.ts`). Amplop `{data}` dibuka di klien; rute yang menjawab dengan tambahan (`question-bank` `total`, `submissions/my` `attempts`, `submissions/queue` paging, wall `can_manage`) dikembalikan utuh. Galat tidak ditelan (P sering mengembalikan `[]`/`null`), jadi 402/403 sampai ke layar.
- **Org aktif:** store baru `useLatihanOrgStore` (persist `titian-latihan-org`) mengirim `X-Organization-Id`; `null` = tanpa header (peran bawaan, pelajar mandiri jalur pribadi). Per panggilan bisa ditimpa (`orgId`). Kunci query di `use-latihan.ts` diawali `["latihan", org]`.
- **Runner:** `submitItem` memakai `Idempotency-Key` dan salinan tertunda di `localStorage` (`latihan-pending-submit:v1:`, beserta user dan org), dicoba ulang 3× untuk galat koneksi/5xx/`idempotency_in_progress`; `flushPendingSubmits` mengirimnya lagi. `itemClock` dari `POST /items/{id}/clock`, cadangan offline hanya bila koneksi putus (galat server dilempar). `saveItemDraft` mendukung `keepalive`. Hasil dari respons submit, `GET /items/{id}/review`, dan `GET /submissions/{id}` (`useLatihanSubmission(..., {pollWhilePending})` poll 5 dtk sampai ada skor).
- **SSE:** `latihanStreamUrl(stream, id)` membangun URL `proctor-stream`/`live-stream`/`collab-stream` dengan `?access_token=` (+ `organization_id`).
- **Disesuaikan saat menyalin `lib/quiz`:**
  - PCF tidak dibawa. `QuizRichContent` menggambar `::image{url width align}` dan `::divider` sendiri (bank IELTS memakai `::image` untuk gambar Writing Task 1); node PCF lain tampil sebagai teks.
  - `resolveAudioUrl` tidak lagi memakai proksi P (`/labs/audio-proxy`, `/files/proxy-r2`, `/files/{id}/proxy`); URL dipakai apa adanya. URL bank `.../api/v1/files/<id>/proxy` harus ditulis ulang ke R2 T di B4.1.
  - `widget_interact` tidak disalin (WidgetHost dan `lib/widgets` opsional). Meta tetap ada, tetapi tanpa renderer ia tidak masuk registri dan pemilih.
  - `QuizRichTextModal` (TipTap + PCF) diganti sementara dengan textarea Markdown + pratinjau, props sama; diganti TipTap di B3.4.
  - `<style jsx>` (Next) di `word_match` menjadi `<style>` biasa dengan keyframes `latihan-word-match-shake`.
  - `MarkdownViewer` P disalin (react-markdown + GFM + KaTeX), karena `lib/markdown.tsx` T terlalu kecil untuk tabel dan rumus bank.
- **npm:** `react-markdown`, `remark-gfm`, `remark-breaks`, `remark-math`, `rehype-katex`, `sonner` (Toaster dipasang di `AppProviders`), `@dnd-kit/{core,sortable,utilities}`, `react-resizable-panels`; dev `vitest` 5.1. Ekstensi TipTap (table, image, link, highlight, text-align, underline, bubble-menu) ditunda ke B3.4 agar versi `@tiptap/core` tidak bergeser sekarang. `framer-motion`, `zod`, Radix: tidak dipakai di folder yang disalin.
- **Tes:** `bun run test` (Vitest, `vitest.config.ts` terpisah dari `vite.config.ts`). Tes P `answer-match`, `draw`, `toefl-itp-score`, dan `full-mock/elearning` diubah ke Vitest; tiga cek `primaryAnswerText` yang di P hanya dicetak kini menjadi assertion. P tidak punya tes `score`, jadi `quiz/score.test.ts` ditulis baru. 74 tes lulus. `tsc --noEmit -p .` bersih.
- **ESLint:** berkas baru bersih. Kode salinan P masih punya ±58 galat aturan ketat (`no-explicit-any`, `react-hooks/*`, `error-boundaries` di `ChartBlock`, `no-img-element`); tidak diubah agar tetap sama dengan P.
- **Untuk B3.2:**
  - Hook `use-draft-autosave` P belum disalin; pakai `saveItemDraft`/`getItemDraft`/`deleteItemDraft` dan `DraftStore` di `lib/latihan/draft-store.ts`.
  - Deck: pakai `useItemDeck` (server) atau `drawDeck` web dengan seed `user:item`. Config item untuk siswa tanpa kunci, jadi skor di klien (`score.ts`) hanya untuk indikator; layar hasil membaca `review`.
  - Pemilih org Latihan (mengisi `useLatihanOrgStore`) belum ada; tanpa itu header tidak dikirim.
  - Panggil `flushPendingSubmits` saat aplikasi dibuka dan saat `online`.
  - `src/lib/quiz-*.ts` lama T belum dihapus (fase 5).

## B3.2: hasil (branch `vite` di `titian-web-vite`)
- **Berkas:**
  - Player salinan P di `src/components/latihan/runner/`: `kuis-umum/player.tsx` (+ `themes/{ielts,pte,toefl_itp}`), `full-mock/{FullMockRunner,FullMockResult}.tsx`, `writing/player.tsx` (+ `_components`, termasuk `ProctorWrapper` dan `CountdownTimer` dari ujilab P), `speaking-record/{player,Recorder,types}`, `vocab-mastery/{player,exercises,orchestrator,types}`, `uploads/{GenericUploadLayout,InBrowserAudioRecorder,InBrowserVideoRecorder}.tsx`, `_shared/{use-hand-in,SubmitFailed,RefreshGuard,SubmitConfirmModal,DeviceCheckGate}`.
  - Baru (Titian): `latihan-runner.tsx` (pengganti AssignmentDispatcher: layar awal + riwayat, player, hasil), `hasil-latihan.tsx`, `players.tsx` (lazy), `_shared/{upload,net,use-draft-autosave,EssayAnnotationSection,types}`; `src/lib/latihan/{autosave,band,hasil,links,drive-url}.ts`; `src/lib/latihan/proktor/{progress,live,live-ui,collab,input-guard}.ts` (salinan utuh P, tanpa klien server); `components/latihan/{latihan-org-picker,latihan-submit-sync}.tsx`.
  - Rute: `/latihan/kerjakan/$itemId?modul=&program=` (`src/routes/latihan/kerjakan/$itemId.tsx`, di luar `_app`: layar penuh tanpa bottom nav, `RequireAuth`) dan `/_app/latihan/program/$id/`.
- **Tidak ikut:** player lama P (reading, listening, grammar, vocabulary, cbt), ruang bicara AI/SpeakingPro/SID/kelas live, `widget`, editor (GroupCard, ConfigEditor, AudioSupportWidget → B3.4), annotator tutor (→ B3.6). Section `speaking` di full mock menampilkan catatan dan tombol lanjut (SpeakingRoomLayout tidak disalin).
- **Item diambil dari modulnya:** backend tidak punya `GET /latihan/items/{id}`, jadi rute kerjakan membawa `?modul=` (dan `?program=` untuk kembali). Tanpa `modul` layar meminta membuka dari program.
- **Kumpul dan hasil:**
  - Semua player memakai `submitItem` (Idempotency-Key + salinan di browser; writing dan speaking P sebelumnya POST langsung). `onComplete` membawa `id`/`result` dari respons submit, lalu runner membuka `HasilLatihan`.
  - Fase hasil lokal kuis P tidak dipakai setelah kumpul sungguhan (config siswa tanpa kunci). Hasil selalu dari `GET /submissions/{id}`: kuis memakai player P dalam `reviewMode` dengan `review.question_groups` + jawaban dari `my_answers`/`review.scoring_detail`, esai lewat prop `serverEssays` (hasil `evaluation`). Writing membaca `evaluation`, speaking membaca `evaluation` + `responses[].transcript`, full mock dibangun ulang oleh `fullMockFromLearner`.
  - Semua panggilan AI klien P dibuang: `/ai/writing/evaluate`, `/ai/writing/model-answer` (UI contoh band disembunyikan, `MODEL_ANSWER = false`), `/ai/speaking/saved-eval|tutor-eval`, `/labs/ai/vocab-mastery-summary`, `/ai/tts` (vocab memakai suara peramban), PATCH skor. Rencana belajar writing memakai `POST /submissions/{id}/generate-learning-plan`.
  - Polling: `useLatihanSubmission(..., {pollWhile})` + `awaitingAi`: hanya item yang dinilai AI (`expectsAiMarking`: writing, speaking_record, kuis berisi essay/freeform_eval, full mock dengan writing/esai; `ai_evaluate: false` mematikan) selama status `submitted`, paling lama 10 menit (AI gagal → "tutor akan menilai"). Bug yang dihindari: `pollWhilePending` B3.1 akan memuat ulang selamanya untuk kuis otomatis dengan `result_show_score: false`.
- **Band:** `lib/latihan/band.ts`. IELTS Reading/Listening = skor section terverifikasi diskalakan ke 40 → tabel `ieltsBands` (skill dari `skill` atau judul section, sama seperti runner P); writing = `overall_band` AI; overall = rata-rata dibulatkan ke 0,5. ITP = benar per bagian dari `review` → `itpScoresFromCounts` → total hanya bila ketiga bagian ada.
- **Full mock:**
  - Section tidak lagi diberi id palsu `item__section` (di P itu membuat kuis/writing section mengirim submit dan draf ke id yang tidak ada). Section memakai `assignmentId` kosong; deck acaknya memakai prop baru `drawSeedItemId` = item mock (seed `user:item`, sama dengan server).
  - Draf: satu draf server per item mock (`fullMockDraftStores`, `{sections: {id: snapshot}}`), tanpa jam per section. Progres section yang sudah selesai tetap hanya di `sessionStorage` seperti P.
- **Autosave:** `DraftSaver` (hanya kirim bila berubah, `time_increment_seconds` dibatasi 300, gagal dicoba lagi di tick berikutnya dengan waktunya, tidak pernah menyimpan setelah `clear`) + `useDraftAutosave` dengan API P (dipakai kuis dan vocab) + `itemDraftStore`/`fullMockDraftStores` sebagai `DraftStore`.
- **Kumpul tertahan:** `LatihanSubmitSync` (di layout `(app)` dan layout kerjakan) memanggil `flushPendingSubmits` saat akun dikenal dan setiap `online`. Layar awal item menampilkan "belum terkirim" + Kirim sekarang.
- **Org:** `LatihanOrgPicker` (select biasa, di halaman program) dari `GET /my-orgs` (kini dikirim tanpa header org), "Pribadi" = tanpa header; org tersimpan yang tidak lagi dimiliki kembali ke Pribadi.
- **Unggahan:** `POST /assets/upload` (`driveApi.uploadAsset`); id aset menjadi `file_ids`/`responses[].file_id`, URL putar dari `GET /assets/{id}`.
- **Tampilan:** chrome baru (runner, hasil, program, pemilih org) memakai komponen dan token Titian dan mode gelap. Isi player P belum diubah warnanya (masih kelas slate/putih P dan tema ujian resmi); merapikannya sekaligus akan mengubah 13 ribu baris tanpa QA.
- **Tes:** `autosave.test.ts`, `band.test.ts`, `hasil.test.ts`, `submit-queue.test.ts` (Idempotency-Key, org, kunci sama untuk jawaban sama, flush hanya milik akun, 4xx dibuang/5xx disimpan, offline). `bun run test` 100 lulus, `tsc --noEmit` bersih, ESLint berkas baru bersih. Salinan P masih punya ±121 galat aturan ketat (any, refs, deps), tidak diubah, sama seperti B3.1.
- **Untuk B3.3 (proktor):**
  - `lib/latihan/proktor/{progress,live,live-ui,collab,input-guard}` sudah ada dan dipanggil player (`setProctorProgress`, `setLiveState`, `setLiveConfig`, `useCollab`, `useLiveField`, `SYNCED_EVENT`); yang belum: `regular-client`, `enforcement`, `block-clipboard`, `live-audio`, dan pembungkus runner.
  - Pasang di `LatihanRunner` saat `view.kind === "work"` (config dari `useEffectiveProctorConfig`, sudah dipakai untuk `disable_spellcheck`). Jangkar draf = `DraftSaver.state.draftId` (`useDraftAutosave` mengembalikan `draftId`) atau `PUT /draft` tanpa `answers_data`. Prop P `clockPaused` dan `mirror` di kuis tetap ada.
  - `ProctorWrapper` writing (blokir salin/tempel tetap, peringatan pindah tab) masih statis seperti P; sebaiknya diganti config proktor.
- **Untuk QA koordinator:** item hanya bisa dibuka dari `/latihan/program/$id` (atau URL dengan `?modul=`). Beranda `/latihan` belum menautkan program (B3.5).

## B3.3: hasil (commit `5cbee93`, branch `vite` di `titian-web-vite`)
- **Berkas:**
  - `src/lib/latihan/proktor/`: `regular-client.ts`, `antrean.ts`, `enforcement.ts`, `block-clipboard.ts`, `live-audio.ts`, `live-audio-player.ts`, `audio-mime.ts`, `grow.ts` (salinan P), serta `pesan.ts` (parser SSE, baris log live, `lockLimit`, `WarningCounter`, `throttle`), `wall.ts` (keadaan, label, saringan, urutan), `stream.ts` (EventSource yang tersambung lagi). `live.ts` ditambah `WritingLiveState` dan `PresenceLiveState`.
  - `src/components/latihan/proktor/`: `use-proktor-latihan.ts`, `proktor-siswa.tsx` (`ProktorAturan`, `ProktorLapisan`), `konteks.ts`, `collab-cursors.tsx`, `wall-modul.tsx` (+ `BarisSiswa`), `detail-siswa.tsx`, `live-exam-view.tsx`, `org-wall.tsx`, `daftar-pengawas.tsx`, `bagian.tsx` (chip, log event, dialog hasil).
  - `src/hooks/use-proktor.ts`; fungsi baru di `api.ts` (lock-history, events, summary, feed, proctors/class-proctors, collab start/stop/update, audio); `latihanStreamUrl` menerima query tambahan (`class_id`).
- **Rute:** `/pengawasan` (organisasi yang dipimpin → semua kelas; kelas yang diajar → modul dari programnya dengan `?kelas=`; modul dengan peran owner/editor/tutor/proctor), `/pengawasan/modul/$moduleId?kelas=` (tab Peserta dan Pengawas, layar "tidak punya akses" untuk 403), `/pengawasan/organisasi/$orgId`. Rute dan layar lama `/pengawasan/$sessionId` dihapus; `components/proctoring/*` tetap ada (dipakai `latihan/ujian`), dihapus fase 5.
- **Siswa:** `useProktorLatihan(item, content, view.kind === "work", attemptKey)` di `LatihanRunner`: `PUT /items/{id}/draft` tanpa jawaban sebagai jangkar, lalu klien proktor, enforcement (`guardTyping`), peringatan, kunci + kode, kolaborasi (`collab-stream`). Peraturan tampil di layar awal item yang diawasi. Kuis menerima `clockPaused` saat terkunci dengan `freeze_timer_on_lock`.
- **Keputusan sendiri:**
  - Klien proktor memanggil `api.ts` (refresh token), bukan `fetch` dengan token yang diberikan sekali seperti P: token Titian 15 menit, jadi di P versi Titian event akan 401 di tengah ujian.
  - Antrean: 4xx selain 408/429 dibuang (draf sudah dikumpulkan/dihapus), batas 2000 event saat offline dengan detak dibuang lebih dulu, kiriman dipotong per 500.
  - Bug P diperbaiki: `session_end` tidak pernah terkirim (`destroyed` diset sebelum `enqueue`).
  - `ProctorWrapper` Writing: bila diawasi, semuanya dari config proktor (peringatan dan kunci dari `ProktorLapisan`); bila tidak, copy/paste tetap diblokir (`mountClipboardBlock`, aturan sesi menulis P) tanpa peringatan pindah tab yang tidak tercatat. `beforeunload` sudah ada di player.
  - Writing mengirim `{player: "writing", answer, words}`; Tonton live menampilkan soal + esai (hanya baca), bukan player Writing dalam mode cermin. Speaking record dan unggahan mengirim tanda hadir (`PresenceLiveState`) agar halaman tahu ada yang menonton; perekam audio mengirim potongan suara (`startLiveAudio`) dan siswa melihat "Pengawas sedang mendengarkan langsung". Mode video tidak dikirim.
  - Jenis runner di live = `state.player`, lalu `item.content` (Titian), lalu `item.player`.
  - "Lihat hasil" membuka dialog kecil (status, skor `GET /submissions/{id}`, kunci dan log `proctor-log`); penilaian lengkap menunggu B3.6.
  - Kunci dari baris dinding langsung tanpa catatan; kunci dengan catatan di laci rincian (P memakai `prompt()`).
  - Pilihan identitas pendaftaran P tidak dibuat (backend selalu `[]`); nama + email.
- **Tes:** `antrean.test.ts`, `regular-client.test.ts` (jsdom: sesi, detak, satu kepergian satu pelanggaran, kedip < 800 ms, paste/bulk, kunci hanya saat berubah, live + penonton + kolaborasi, `session_end`), `pesan.test.ts`, `wall.test.ts`. `bun run test` 134 lulus, `tsc --noEmit` bersih, ESLint berkas baru bersih (galat lama di `writing/player.tsx` dan `Recorder.tsx` salinan P tidak bertambah).
- **Untuk B3.4:**
  - `ProctorConfigSection` (editor) menulis `PUT /items/{id}/proctor-config` dan `/modules/{id}/proctor-config`; kunci yang dibaca siswa: `enabled`, `block_paste`, `force_fullscreen`, `disable_spellcheck`, `freeze_timer_on_lock`, `auto_lock_rules[{type, after_count}]` (`violation`/`tab_switch`/`paste`).
  - Tautan "Pemantauan" dari editor modul ke `/pengawasan/modul/$id`; `DaftarPengawas` bisa dipakai lagi di laci pengaturan modul.
  - Full mock dan Writing belum membekukan jam saat terkunci (hanya kuis lewat `clockPaused`).
- **QA dua sesi (butuh izin pemilik; belum dilakukan):**
  1. Siapkan item kuis berisi soal esai/Writing dengan `proctor_config` `{enabled: true, block_paste: true, auto_lock_rules: [{type: "violation", after_count: 3}]}` di modul yang dimuat program sebuah kelas; siswa anggota kelas, guru = `classes.teacher_id`.
  2. Sesi A (siswa, HP atau jendela privat): buka `/latihan/program/$id` → item → layar awal menampilkan "Latihan ini diawasi" → Mulai.
  3. Sesi B (guru): `/pengawasan` → kelas → modul → baris siswa "Mengerjakan", badge Live hijau.
  4. A pindah tab ±2 dtk lalu kembali → A melihat "Pelanggaran 1 dari 3"; B melihat "Keluar halaman" lalu kembali, dan "Kejadian terbaru" mencatatnya dalam ±3 dtk.
  5. A mencoba paste → ditolak dengan toast, peringatan ke-2. Pelanggaran ke-3 → A melihat layar "Pengerjaan dikunci"; B melihat "Terkunci" dengan alasan otomatis.
  6. B buka rincian siswa → Riwayat kunci → "Kirim ke siswa" → kode muncul di layar kunci A → A tekan Buka → lanjut dengan jawaban utuh. Ulangi dengan kunci manual dan "Buka kunci" dari B.
  7. B "Tonton live" → A mengetik di soal esai → teks muncul di B ±1 dtk per kata, "Aktivitas jawaban" bertambah. B "Bantu menulis" → keduanya mengetik, kursor terlihat, A tidak mendapat pelanggaran dari teks B; "Selesai membantu".
  8. A kumpulkan → B melihat kartu "Siswa sudah mengumpulkan" dengan skor dan "Lihat hasil" (log berisi pelanggaran dan kunci). Baris pindah ke "Selesai".
  9. Admin sekolah: `/pengawasan/organisasi/$orgId` menampilkan siswa dengan kelas/periode; saringan dan "Tonton live" bekerja. Uji juga item Writing (esai tampil di live) dan speaking_record (Dengarkan suara siswa).

## B3.4: hasil (commit `aa61d11`, branch `vite` di `titian-web-vite`)
- **Rute:** `/studio/latihan` (daftar modul yang bisa disunting, buat modul, duplikat, pemilih org) dan `/studio/latihan/modul/$id` (tab Isi, Aturan, Akses, Pengawasan, Modul). Menu "Latihan" di StudioShell; editor modul memakai lebar penuh. Studio lama (modules/programs/question-banks) tidak disentuh.
- **Berkas:**
  - Layar: `src/screens/studio/latihan/{page.tsx,modul/[id]/page.tsx}`, rute `src/routes/studio/latihan/{index.tsx,modul/$id.tsx}`.
  - Komponen baru `src/components/latihan/editor/`: `item-editor.tsx`, `pemilih-unit.tsx`, `proctor-config-section.tsx`, `aturan-belajar.tsx`, `akses-modul.tsx`, `editor-lain.tsx` (Writing, Kosakata, unggahan), `kuis-umum/{config-editor,group-card,media,ubah-tipe-dialog}.tsx`.
  - Salinan P (impor dan warna token Titian): `kuis-umum/{SubtypeLibraryPicker,TemplateBrowser,TableStructureEditor,FlowStructureEditor,GapFillSectionsEditor,CellLinesEditor,ConversationCardsEditor,structureSync,AddToQuestionBankModal}`, `full-mock/{FullMockConfigEditor,SectionImportModal}`, `speaking-record/ConfigEditor` (tanpa AIGenerateModal), `lib/latihan/rubrics.ts`.
  - Logika teruji `src/lib/latihan/editor/`: `unit-kanonik`, `kuis-struktur`, `konversi`, `validasi`, `pohon`, `proktor-config`, `aturan`, `kata`.
  - `api.ts`: `get/putItemProctorConfig`, `get/putModuleProctorConfig`; tipe `ItemProctorConfig`; `titian?` di `KuisUmumConfig`, `QuizQuestionGroup`, `QuizQuestion`, `FullMockSection`.
- **Dipangkas dari P:** semua AI (buat/tambah/sunting soal, parse teks, impor PDF/Word, transkrip/TTS/Whisper, passage AI, petunjuk AI, pemilih model, ModuleAiPanel, GenerateFromPdf, SectionBulkGenerate, varian domain), staging draf impor, `ConvertGroupTypeModal` (AI), ModuleItemRefPicker, IeltsPromptHelper, editor Listening/Reading/Grammar/Vocabulary/SpeakingLab/Widget/SID lama, artikel/video/tautan/presentasi, LessonPlan, ShareLinks (K5), SettingsAudit, analitik, pilih banyak + aturan massal, clipboard antar tab, seret-lepas (diganti naik/turun dan "pindah ke folder"), mode lapisan kelas `?class=`, kamera/kartu identitas/geofence di proktor.
- **Keputusan sendiri:**
  - ConfigEditor dan GroupCard ditulis ulang (bukan disalin) karena ±60% isinya AI; struktur (urutan saudara, duplikat subtree, hapus section menaikkan isi) dipindah ke `kuis-struktur.ts` dengan perilaku P.
  - Ubah tipe grup tanpa AI (`konversi.ts`): hanya perpindahan pasti (bentuk sama, antarvarian Benar/Salah, PG ↔ PG kompleks, PG → isian, Benar/Salah → PG), dengan peringatan per soal.
  - Validasi sebelum terbit (`validasi.ts`): galat menahan "Terbitkan" (grup tanpa soal, kunci kosong/tidak cocok, pilihan < 2, nomor ganda, map tanpa gambar, bentuk `titian` salah); tombol "Nomori ulang" memberi nomor 1..N mengikuti urutan tampil. Server tetap menilai ulang.
  - Pemilih unit: pohon `GET /catalog` → `GET /catalog/concepts/{code}/units`, atau ketik module_id; nama unit dari `GET /catalog/units/{id}`. Tingkat sesi/grup/soal punya "Ikut atas / Atur / Tanpa unit" (`unit` tidak ada / daftar / `[]`). Pesan 422 "Unit kanonik tidak dikenal: …" ditampilkan di editor item dan unitnya ditandai merah di semua pemilih (context). `peran` hanya di tingkat item. Unit di section kuis umum tidak ditawarkan karena server tidak membacanya.
  - ProctorConfigSection hanya kunci catatan B3.3 (`enabled`, `block_paste`, `force_fullscreen`, `disable_spellcheck`, `freeze_timer_on_lock`, `auto_lock_rules` violation/tab_switch/paste); aturan kunci disalin dari warisan saat item mulai mengatur sendiri (server mengganti seluruh array). Ada juga di tingkat modul (tab Pengawasan) bersama `DaftarPengawas` dan tautan Pemantauan.
  - Aturan belajar diatur dari editor modul per program yang memuat modul (`GET /modules/{id}/programs`) atau per kelas yang diajar (`my-authoring`).
  - Grant langganan hanya tampil untuk `platform_admin`; grant org memilih dari `my-orgs`; kolaborator lewat email.
  - TipTap tambahan tidak dipasang: konten pendukung disimpan sebagai Markdown/PCF (`::image{…}`), dan editor WYSIWYG butuh konversi dua arah yang berisiko merusak bank. `QuizRichTextModal` Markdown + pratinjau B3.1 tetap; `@tiptap/*` tidak bergeser.
  - Audio diunggah ke aset Titian (`POST /assets/upload`) dan URL-nya ditulis ke `audio_url`; gambar sama.
- **Tes:** `src/lib/latihan/editor/*.test.ts` (unit kanonik, struktur kuis, konversi, validasi, pohon, proktor, aturan, kata). `bun run test` 175 lulus, `tsc --noEmit` bersih, ESLint berkas baru Titian bersih. Salinan P masih punya 4 galat `set-state-in-effect` (SubtypeLibraryPicker, SectionImportModal) dan 3 peringatan, tidak diubah (kebijakan B3.1–B3.3).
- **QA browser (butuh izin pemilik; belum dilakukan):**
  1. Akun guru/pembuat isi: `/studio/latihan` → "Modul baru" (pemilik Pribadi atau org sekolah) → terbuka di editor.
  2. Tab Isi → Tambah → Kuis. Di editor item: "Grup soal" → Multiple Choice → buka grup → "Edit soal" → tambah 3 soal dengan pilihan A–D dan kunci. Pastikan daftar "Periksa sebelum terbit" kosong.
  3. "Kaitan ke pengetahuan" → Pilih unit → pilih satu unit Matematika → Pakai; peran Cek. Simpan. Uji juga: ketik `unit.palsu` lalu Simpan → muncul pesan 422 dan chip merah; hapus lalu Simpan lagi.
  4. Terbitkan item (tombol di editor), lalu tab Modul → "Terbitkan modul". Tab Akses → Publik + mengerjakan → Simpan visibilitas (atau muat modul ke program kelas).
  5. "Coba sebagai siswa" atau akun siswa di `/latihan/kerjakan/{itemId}?modul={moduleId}` → kerjakan → kumpul → hasil dan kunci tampil; skor sama dengan server.
  6. Profil siswa: `GET /latihan/me/bukti` memuat unit dari langkah 3.
  7. Tambahan: urutkan item naik/turun, pindah ke folder, duplikat item/modul, tab Pengawasan (aktifkan + kunci setelah 3 pelanggaran, lalu "Buka Pemantauan"), tab Aturan (program yang memuat modul).
- **Untuk B3.5:**
  - Memuat modul ke program dan admin program belum ada di Studio Latihan (tab Modul hanya menampilkan program yang memuat). Pakai `linkModuleToProgram`/`useLinkModuleToProgram`.
  - Bank Soal: "Tambah ke Bank Soal" di grup sudah memakai `AddToQuestionBankModal` + `POST /latihan/question-bank`; halaman admin Bank Soal dan latihan per tipe soal bisa memakai ulang `SubtypeLibraryPicker` dan renderer pratinjau `group-card`.
  - Generator AI (K6, `ai/quizgen`) bisa dipasang di `kuis-umum/config-editor.tsx` (grup kosong) tanpa mengubah struktur.
  - Mode lapisan kelas (`?class=`, item milik kelas, override proktor kelas lewat aturan) belum dibuat; `gabungCfg` di `proktor-config.ts` sudah menyamai penggabungan server.

## B3.5: hasil (branch `vite` di `titian-web-vite`)
- **Rute:** `/latihan` (beranda data asli), `/latihan/ujian?ujian=` (Ujilab), `/latihan/tipe-soal` (pilih tipe) dan `/latihan/tipe-soal/kerjakan?subject=&family=&subtype=&part=&test_type=&count=&item_id=` (layar penuh, di luar `_app`), `/studio/latihan/bank`, `/studio/latihan/program`, `/studio/latihan/program/$id`. Navigasi Modul/Program/Bank Soal di atas halaman Studio Latihan (`StudioLatihanNav`). Tab Modul editor modul kini bisa memuat/melepas modul ke program.
- **Berkas:** layar `src/screens/(app)/latihan/{page,ujian/page,tipe-soal/page}.tsx`, `src/screens/latihan-kerjakan/tipe-soal.tsx`, `src/screens/studio/latihan/{bank/page,program/page,program/[id]/page}.tsx`; komponen `components/latihan/akses-latihan.tsx` (lencana akses, ajakan berlangganan ke `/langganan`), `components/latihan/editor/studio-latihan-nav.tsx`; logika teruji `src/lib/latihan/{ujian,bank-latihan,beranda,program-admin}.ts`. `Pratinjau` di `group-card.tsx` kini diekspor.
- **Keputusan sendiri:**
  - Jenis ujian program dibaca dari `subject`, lalu tag, lalu nama (`jenisUjian`). B4.1/B4.2 sebaiknya mengisi `subject` program dengan `ielts`/`pte`/`toefl_itp`/`tka`/`snbt`; editor program menawarkan nilai itu.
  - Label akses modul: `access_role: ""` = "Langganan Plus/Pro" (terkunci, ajakan berlangganan); punya akses tanpa langganan aktif = "Gratis"; dengan langganan = "Terbuka". `GET /programs/{id}/modules` tidak membawa `visibility`, jadi pelanggan tidak bisa dibedakan antara test gratis dan berbayar. 402 saat membuka modul juga menampilkan ajakan.
  - Latihan per tipe soal memutar player kuis umum `standalone` tanpa kiriman ke server (seperti P). Karena `hideBankKeys` menyaring kunci untuk yang bukan penulis bank, skor lokal hanya dipakai bila setiap grup bernilai otomatis masih membawa kunci (`kunciLengkap`); selain itu (siswa) layar selesai menampilkan jumlah terjawab tanpa skor dan menunjuk ke halaman Ujian. Grup acak diambil sekali per sesi (tanpa refetch saat fokus).
  - Riwayat beranda disusun dari `/me/assessments` (kiriman, skor terbaik) dan `/my-learning-modules` (aktivitas terakhir), karena belum ada endpoint daftar semua submission siswa.
  - Admin program dipangkas: tanpa sub-program, prasyarat antarmodul, sampul, kolaborator, visibilitas program (backend tidak punya PATCH visibilitas program; B4.1 menulisnya langsung). Kelas yang ditawarkan = `/my-classes` + `GET /classes?organization_id=` org program (admin org); status tertaut per kelas dari `GET /classes/{id}/programs`.
  - Bank Soal admin: aksi massal (tambah tag, hapus) memanggil endpoint per item (sama dengan P), galat sebagian dilaporkan. "Pustaka tipe soal" (`SubtypeLibraryPicker`) memilih saringan tipe; pratinjau memakai renderer siswa `Pratinjau` + daftar kunci (kosong bila disaring server). Tombol "Coba" membuka sesi satu item.
  - Beranda lama (kartu TKA/SNBT/tryout tiruan dan simulator showcase) diganti. Personal Review (dengan jumlah konsep jatuh tempo), Latihan Gemini, Speaking Room, dan Grup & Liga tetap sebagai tautan. Layar lama `/latihan/{tka,snbt,ielts,toefl,pte}` dan `ujian/$assessmentId` tidak dihapus (fase 5), hanya tidak ditautkan.
- **Tes:** `ujian.test.ts`, `bank-latihan.test.ts`, `beranda.test.ts`, `program-admin.test.ts` (25 tes). `bun run test` 200 lulus, `tsc --noEmit` bersih, ESLint berkas baru/diubah bersih.
- **QA browser (butuh izin pemilik; belum dilakukan):**
  1. Tanpa data bank: `/latihan` tampil dengan kartu ujian "Segera hadir", riwayat kosong; `/latihan/ujian` menampilkan "Bank ujian sedang disiapkan"; `/latihan/tipe-soal` menampilkan tipe soal IELTS/TOEFL ITP/PTE dengan "Belum ada soal".
  2. Akun guru: buat modul kuis (B3.4) → di grup "Tambah ke Bank Soal" (IELTS, Reading, Passage 1) → `/studio/latihan/bank` menampilkan grup itu; Pratinjau (renderer + kunci), Ubah metadata, Tambah tag massal, Hapus, Pustaka tipe soal menyaring.
  3. "Coba" di baris bank → sesi layar penuh, kumpulkan → hasil dinilai (penulis melihat kunci). Ulangi sebagai siswa di `/latihan/tipe-soal` → Mulai → kumpulkan → layar "belum dinilai" dengan jumlah terjawab.
  4. `/studio/latihan/program` → Program baru (Ujian: IELTS) → Muat modul → urutkan → Terbitkan → Tautkan ke kelas yang diajar (anggota terdaftar). Dari editor modul tab Modul: "Muat ke program" dan "Lepas".
  5. Siswa kelas itu: `/latihan` → Lanjutkan menampilkan program; `/latihan/ujian?ujian=ielts` menampilkan program dan test; buka test → item → kerjakan → kembali, Riwayat memuat percobaan dengan skor.
  6. Isi berbayar: sebagai admin platform beri grant langganan Plus pada satu modul (tab Akses), modul platform publik untuk yang lain. Pelajar mandiri tanpa langganan: test berlabel "Gratis" terbuka, yang lain "Langganan Plus" dengan ajakan → `/langganan`. Dengan langganan aktif: semua "Terbuka". Mode gelap di semua layar baru.
- **Untuk B3.6:** riwayat lengkap butuh `GET /latihan/me/submissions` (semua submission siswa, dengan item/modul/skor/status); beranda dan halaman hasil bisa memakainya. Antrean penilaian dan detail submission belum ada di web.
- **Untuk B4 / backend:**
  - Penilaian sesi Bank Soal di server, mis. `POST /latihan/question-bank/periksa {ids, answers}` → `grading.Complete` atas snapshot utuh + `review` (kunci, pembahasan), tanpa submission atau dengan `metadata.practice`. Tanpa itu siswa tidak mendapat skor latihan per tipe soal.
  - `GET /programs/{id}/modules` sebaiknya membawa `visibility` (dan `subscription_tier` juga saat ada akses) agar label Gratis/Langganan benar bagi pelanggan.
  - B4.1: isi `subject` program bank (`ielts`, `pte`, `toefl_itp`), satu modul per test di bawah program publik, dan `org_question_bank_items` dengan `source_module_id` ke modul test agar bank berbayar ikut tertutup. B4.2: program try out TKA/SNBT dengan `subject` `tka`/`snbt`.

## B4.1: hasil (branch `latihan`)
- **Alat:** `cmd/tools/impor_bank_parilabs/` di `titian-backend-latihan`. `ekspor.sh` mengekspor subtree bank dari DB Parilabs ke JSONL (setiap query `default_transaction_read_only=on`; repo Parilabs tidak diubah). Ekspor B4.1 ada di scratchpad sesi; jalankan ulang `ekspor.sh` bila bank Parilabs berubah. Pengimpor membaca JSONL itu; tanpa `-apply` hanya melapor, `-periksa` membaca ulang DB.
  ```
  docker start parelabs_db && cmd/tools/impor_bank_parilabs/ekspor.sh DIR && docker stop parelabs_db
  GO_DOCKER_ARGS="-e DATABASE_URL -v DIR:DIR -v /home/john/Dev/parelabs-workspace:/home/john/Dev/parelabs-workspace:ro -v MEDIA:MEDIA" \
    ./go.sh run ./cmd/tools/impor_bank_parilabs -ekspor DIR -audio-dir ".../AUDIO IELTS" -img-dir .../parelabs-backend-go/scripts/ielts_bank \
    -public-dir .../app-parelabs-v2/public -media-dir MEDIA -media-cek http://localhost:3000 [-apply] [-periksa]
  ```
- **Target:** DB dev `titian_bun`. Migrasi 0117, 0118, 0120 diterapkan ke sana dengan psql (aditif), dan dicatat di `_sqlx_migrations` dengan checksum yang sama seperti `RunMigrations`, jadi API branch `latihan` tidak menjalankannya lagi. Catatan: API dev yang sedang jalan di :8091 (dari `titian-backend-go`, branch main) dan `.cache/api-local.env` kedua worktree memakai DB `pare_view`, bukan `titian_bun`. Untuk QA web, API `latihan` harus diarahkan ke `titian_bun`, atau impor diulang ke `pare_view` (setelah migrasi 0117–0120 diterapkan di sana).
- **Pemilik dan id:** semua baris milik org platform "Titian Asa". `created_by`/`granted_by` = akun `app.titianasa@gmail.com` (`-pembuat`). Id = UUID v5 dari id Parilabs (namespace tetap di `peta.go`). Upsert per id, jadi pengimpor bisa diulang tanpa duplikat (diuji di DB dev: jumlah baris sama setelah run kedua). Item yang hilang di ekspor baru tidak dihapus. Suntingan di Titian ditimpa saat impor diulang (belum ada pola `build_hash`).
- **Struktur:**
  - Satu program per ujian: `IELTS Academic` (`subject` `ielts`, 48 modul), `PTE Academic` (`pte`, 8 modul), `TOEFL ITP` (`toefl_itp`, 4 modul). Ketiganya `public`/`taker` dan terbit, `metadata.sumber = parilabs`.
  - Pohon folder Parilabs ikut (`BANK SOAL › … › buku › TEST n`). Setiap test punya dua modul seperti di Parilabs: modul part/tipe soal dan modul `MOCK TEST`. Urutan di program: buku, test, lalu part sebelum mock.
  - Gratis: Test 1 setiap buku (TOEFL ITP: Practice Test A), dua modulnya `public`/`taker`. Modul test lainnya `private` dengan grant produk `plus`/`taker` (`-tier`). Folder `private`. Semua modul terbit, `target_tests` diisi ujiannya bila kosong.
- **Yang dilewati (36 modul):** folder lama `CAMBRIDGE 17–21` (salinan lama IELTS 17–21 yang dipakai kelas Parilabs, gambar Writing di bucket prod Parilabs), `IELTS GT › IELTS-GT-WRITING` (satu modul dengan tautan Google Drive), dan `TEST 1 - C20 - AC (Salinan)`. Karena itu 48 baris bank IELTS Parilabs (semuanya dari CAMBRIDGE 17) tidak ikut. Penggantinya 389 baris bank IELTS **turunan** dari part Listening/Reading keenam buku, dibuat seperti "Tambah ke Bank Soal" di editor: grup + passage/transcript/audio/speakers dari section, `family` listening/reading, `part_number`/`passage_number` dari judul item, `test_type` academic, `taxonomy = {series, test, asal: "turunan"}`, `source_module_id` = modul test.
- **Catatan:** inventaris §7.2 menyebut IELTS 15 dan 16, tetapi DB Parilabs tidak punya modulnya (hanya MP3 di `AUDIO IELTS/15` dan `/16`).
- **Media:** tidak ada yang diunggah ke cloud. Dev Titian memakai R2 sungguhan (`storage.NewR2`, tanpa storage lokal), jadi media disimpan di `/home/john/Dev/sanja-workspace/alr/titian-backend-go/.cache/latihan-media/<buku>/<nama>` (gitignored, 678 MB, 162 berkas). Web dev menyajikannya lewat symlink `titian-web-vite/public/latihan-media` → direktori itu (dikecualikan di `.git/info/exclude` repo `titian-web`, tidak di-commit). URL di config menjadi relatif: `/latihan-media/<buku>/<nama>`.
  - Asal: R2 publik Parilabs (76 klip, diunduh lewat DNS-over-HTTPS karena DNS ISP memblokir `*.r2.dev`), MinIO dev (20 MP3, diambil dari `AUDIO IELTS/` menurut nama berkas di baris `files`), `/files/<id>/proxy` (29 gambar, dari `scripts/ielts_bank/ieltsNN_img/`), `/bank-soal/pte/pte-2/*` (37 webp, dari `app-parelabs-v2/public`).
  - **Untuk B5.2:** `vite build` ikut menyalin symlink `public/latihan-media` (678 MB) ke `dist`. Hapus symlink sebelum build prod, unggah media ke R2 prod dengan kunci `latihan/bank/<buku>/<nama>`, lalu tulis ulang awalan `/latihan-media/` (jalankan pengimpor dengan `-media-base` URL R2).
- **Jumlah (sumber = rencana = DB, diperiksa `-periksa`):**

  | Buku | Modul (gratis) | Item | Grup / soal (part) | Grup / soal (mock) | Bank | Audio | Gambar |
  |---|---|---|---|---|---|---|---|
  | IELTS 14 | 8 (2) | 108 | 70 / 361 | 70 / 361 | 62 turunan | 16 | 5 |
  | IELTS 17 | 8 (2) | 108 | 72 / 360 | 72 / 360 | 64 turunan | 16 | 4 |
  | IELTS 18 | 8 (2) | 108 | 76 / 359 | 76 / 359 | 68 turunan | 16 | 5 |
  | IELTS 19 | 8 (2) | 108 | 75 / 360 | 75 / 360 | 67 turunan | 16 | 5 |
  | IELTS 20 | 8 (2) | 108 | 71 / 359 | 71 / 359 | 63 turunan | 16 | 5 |
  | IELTS 21 | 8 (2) | 108 | 73 / 358 | 73 / 358 | 65 turunan | 16 | 5 |
  | PTE 2 | 8 (2) | 128 | 241 / 457 | 482 / 914 | 241 | 0 | 37 |
  | TOEFL ITP L1 V3 | 4 (2) | 44 | 84 / 280 | 168 / 560 | 84 | 0 | 0 |
  | **Jumlah** | 60 (16) + 44 folder | 820 | 762 / 2.894 | 1.087 / 3.631 | 325 + 389 turunan | 96 | 66 |

  "Soal" menghitung pertanyaan di config, termasuk pertanyaan Speaking dan Writing. Mock PTE dan ITP menghitung grup dua kali karena mock penuh dan mock per section sama-sama memuat grupnya. DB: 3 program, 104 modul, 820 item, 60 modul program, 44 grant produk, 714 baris bank.
- **Periksa (§7.3 butir 4):** 13.687 jawaban kunci (setiap alternatif `a|b`) dinilai benar oleh `internal/latihan/grading.Verify`, baik di item, di setiap section mock, maupun di bank. 752 soal dinilai AI/tutor (essay, voice_record), jadi tidak punya kunci. Tidak ada soal otomatis tanpa kunci. Tidak tersisa URL `r2.dev`, `/files/<id>/proxy`, `localhost:9000/3001`, `sekolahterbuka.com`, atau `/bank-soal/`. Setiap URL media menjawab 200/206 dengan tipe media dari `http://localhost:3000` (bukan fallback HTML).
- **Kosong:** audio PTE (160 grup listening) dan TOEFL ITP (70 grup) tidak punya audio, hanya audioscript dan transkrip (B4.3, TTS perlu izin biaya). Audio IELTS lengkap di keenam buku, termasuk IELTS 18 Test 4 dan IELTS 14 (dari MinIO → `AUDIO IELTS`).
- **Tes:** `impor_test.go`: pemetaan (yang dilewati, gratis/berbayar, urutan program, parent item, empat jenis URL media ditulis ulang, termasuk `::image` di markdown, baris bank turunan), id deterministik, cek kunci, salin media (kedua kali dilewati), dan tulis dua kali ke `testdb` (jumlah tetap, modul orang lain dengan slug sama tidak tersentuh, akses, `source_module_id`, `periksaDB` bersih).
- **Untuk B3.5/QA:** beranda Latihan dan Ujilab bisa diuji dengan data asli setelah API `latihan` diarahkan ke `titian_bun`. Label Gratis/Langganan butuh `visibility` di `GET /programs/{id}/modules` (catatan B3.5).

## B3.6: hasil (backend `4975d55` branch `latihan`, web `5303dd2` branch `vite`)
- **Backend:**
  - `GET /latihan/me/submissions?page=&per_page=&module_id=&module_item_id=&practice=` (`nilai/riwayat.go`): semua kiriman akun (lintas org, tenant tidak menyaring, sama seperti bukti), terbaru dulu, `{data, total, page, per_page}`. Per baris: item, jenis, modul, org, status, percobaan, waktu, `practice`, `score_hidden`; `final_score`/`tutor_graded` NULL bila item `result_show_score: false`. Tanpa jawaban, kunci, atau hasil AI.
  - `POST /latihan/question-bank/periksa {ids, answers}` (`bank_periksa.go`): snapshot utuh dirakit seperti `rakitLatihan` web (satu item = nomor asli; beberapa = 1..N lewat `remapGroupNumbers`, port `remapGroupQuestionNumbers` termasuk flow/rows/sections/passage_sections), lalu `grading.Complete` + `Verify`. Klaim klien dan `ai_eval_results` dibuang. Akses = `bankScope` (sama dengan baca bank; id di luar cakupan → 404), paling banyak 50 id, id ganda 422. Jawaban `{score, max_score, percentage, review: {scoring_detail, question_groups}}`; esai `needs_eval` di luar skor. **Tidak disimpan** (bukan item: tanpa submission dan tanpa bukti unit).
  - `GET /programs/{id}/modules` membawa `visibility` dan `subscription_tier` untuk semua pembaca (`requiredTiers`, satu kueri).
  - Tes: `bank_periksa_test.go` (vektor penomoran ulang, penilaian, klaim palsu, satu grup, esai, tanpa jawaban, 404/422, bank platform berbayar + langganan), `nilai/riwayat_test.go`, tambahan di `TestPelajarMandiriAndPaidContent`, rute di `cmd/api`. Lulus bersama `internal/latihan/...`, `cmd/api`, `go vet ./...`, `go build ./...`.
- **Web:**
  - Rute: `/latihan/tutor` (tab Perlu dinilai = `submissions/queue`, Sudah dinilai = `tutor/submissions?status=graded,returned`, Hasil per modul = `tutor/tree`), `/latihan/tutor/kiriman/$id` (layar penuh, di luar `_app`), `/latihan/tutor/hasil/$moduleId?kelas=`, `/latihan/riwayat`. Tautan "Penilaian Latihan" di menu akun (admin org atau akses Studio).
  - Detail kiriman: player siswa dalam mode review dengan config utuh penilai (`ulasan-kiriman.tsx`) + panel nilai (nilai tutor 0–100, catatan, nilai ulang AI bila `bisaNilaiUlangAI`, rencana belajar writing, tandai sudah dicek). Pemilik yang bukan penilai menerima tampilan siswa → layar "tidak bisa menilai".
  - Anotasi: `components/latihan/tutor/essay-annotator.tsx` (salinan EssayAnnotator P) dipakai `EssayAnnotationSection` untuk siswa (baca) dan tutor (ubah). Kunci di `lib/latihan/anotasi.ts` = backend: writing `main`, soal kuis = nomor (bukan `question_id`), full mock `sectionId:nomor`, writing section `sectionId`. Writing player dulu memakai `section:{id}:main` dan kuis section tanpa awalan; keduanya diperbaiki.
  - Hasil modul: ringkasan, saringan status/item/jenis/nama/tanggal, urutan, halaman; Excel dari `results/export.xlsx`, CSV dibangun di web dari semua halaman saringan (`csvHasilModul`, BOM UTF-8).
  - Riwayat beranda dan `/latihan/riwayat` dari endpoint baru; baris membuka `/latihan/kerjakan/{item}?modul=&hasil={submission}` (runner langsung ke hasil; item tertutup tetap bisa dibaca hasilnya). `susunRiwayat` dihapus.
  - Latihan per tipe soal: setelah Kumpulkan, `periksaBank(ids, answers_data)` lalu player mode review dengan kunci dari server; galat → "Periksa lagi" tanpa kehilangan jawaban. `kunciLengkap` dihapus.
  - `labelAkses`: `access_role ""` = terkunci; ada tier = "Langganan Plus/Pro" (terbuka bagi pelanggan); `public` = Gratis; lainnya Terbuka. Lencana juga di judul modul halaman program (hanya untuk modul gratis/berbayar).
- **Keputusan sendiri:**
  - Catatan suara anotasi tidak dibuat: aset Titian hanya terbaca pemiliknya, jadi siswa tidak bisa memutar rekaman tutor. Butuh aturan akses aset (mis. aset anotasi terbaca pemilik submission) sebelum dipasang.
  - Tidak disalin dari P: editor jawaban/kunci (AnswersEditorPanel; endpoint `PATCH /answers` sudah ada), "Kembalikan ke siswa" (PATCH Titian tidak menyimpan `return_note`/`returned_at`), layar penuh terpisah, sinkron skor hitung ulang klien, ekspor per assignment (endpoint `exportAssignment` ada di `api.ts`, belum ada tombol), Analytics modal.
  - Periksa bank tanpa submission: tidak ada item atau assignment untuk ditempeli; siswa bisa melihat kunci grup yang memang boleh ia baca, sama seperti practice.
- **Tes web:** `anotasi.test.ts`, `tutor.test.ts`, tambahan `beranda`, `bank-latihan` (`ringkasPeriksa`), `ujian` (`labelAkses`). `bun run test` 217 lulus, `tsc --noEmit` bersih, ESLint berkas baru bersih.
- **QA browser (butuh izin pemilik; belum dilakukan):**
  1. Siswa kelas mengumpulkan item Writing dan kuis berisi soal esai (B3.4/B3.5). Tunggu status `ai_graded`.
  2. Guru kelas: menu akun → Penilaian Latihan → Perlu dinilai menampilkan kedua kiriman (siswa kelas lain tidak). Cari nama; ubah urutan.
  3. Buka kiriman Writing: esai dengan sorotan AI putus-putus. Sorot satu kata → kategori + komentar → Simpan; klik sorotan AI → ubah komentar (menjadi tutor, garis penuh); Ubah rentang; tandai selesai; hapus.
  4. Nilai ulang dengan AI → skor AI berubah. Isi nilai 85 + catatan → Simpan nilai → kembali ke antrean; kiriman pindah ke Sudah dinilai. Isian 120 ditolak.
  5. Siswa: `/latihan` Riwayat → kiriman itu 85, "Dinilai tutor"; buka → hasil dengan catatan tutor dan sorotan (klik untuk membaca). "Lihat semua" → `/latihan/riwayat`, saringan Latihan bebas.
  6. Kuis esai: anotasi di soal esai muncul di hasil siswa pada soal yang sama. Ulangi di full mock (section kuis dan section writing).
  7. Hasil per modul → modul → pilih kelas → ringkasan dan daftar; saring status/item/tanggal; Excel dan CSV terunduh dan terbuka benar di Excel (huruf Indonesia utuh).
  8. Siswa `/latihan/tipe-soal` → Mulai → jawab sebagian → Kumpulkan → "x dari y soal benar", kunci dan pembahasan tampil, Latihan lagi memberi set baru. Matikan jaringan sebelum Kumpulkan → "Periksa lagi" bekerja setelah online.
  9. Pelanggan Plus di program bank: test gratis berlabel "Gratis", test berbayar "Langganan Plus" (tanpa gembok); tanpa langganan berbayar bergembok. Mode gelap di semua layar baru.

## B4.2: ruang ujian TKA + impor bank TKA (branch `vite` di `titian-web-vite`, `latihan` di `titian-backend-latihan`)
- **Permintaan pemilik (2026-11-21):** isi folder `TKA BANK` dijadikan paket ujian, dengan exam runner khusus TKA yang tampilan dan fiturnya semirip mungkin dengan TKA berbasis komputer, ditambah semua fitur runner Parilabs (termasuk pengawasan live). Builder (Studio Latihan, B3.4) sudah ada, jadi yang dibuat: tema runner, opsi di builder, dan impor isi.
- **Runner (tema `tka`, `config.theme = "tka"`):** `components/latihan/runner/kuis-umum/themes/tka/{TkaHeader,TkaIntro,TkaRoomView,steps}`; dipasang di `player.tsx` seperti tema PTE, jadi timer, autosave, kunci proktor, pengawasan live, kolaborasi, kumpul tertunda, dan hasil/tinjauan memakai jalur yang sama dengan tema lain (pembungkus proktor ada di `LatihanRunner`, tidak bergantung tema).
  - Layar pembuka: konfirmasi data peserta, petunjuk, tata tertib + centang, "Mulai Mengerjakan".
  - Ruang: satu nomor soal per layar; kepala (peserta, ukuran huruf 90–150%, jam hitung mundur); kotak "Hierarki Indikator" (bisa dilipat); kode soal + label "Bentuk Soal"; stimulus; panel "Daftar Soal" (terjawab hijau, ragu-ragu kuning, sedang dibuka bercincin; lembar dari bawah di layar kecil); bilah bawah Sebelumnya, Ragu-ragu, Berikutnya/Selesai; panah kiri/kanan; konfirmasi Selesai dengan ringkasan (terjawab, belum lengkap, ragu-ragu). Ragu-ragu dan ukuran huruf disimpan di peramban (`tka-ragu:<item>`, `tka-font-scale`).
  - Satu nomor TKA = satu langkah: tabel pernyataan Benar/Salah, PG kompleks, dan menjodohkan memakai satu layar; grup pilihan ganda berisi beberapa soal dipecah per soal.
  - `true_false` tampil sebagai tabel Pernyataan | Benar | Salah (kunci tetap `True`/`False`); label Benar/Salah juga di tinjauan. `TkaModeContext` menyederhanakan `GroupHeader` (hanya instruksi biru) dan nomor soal di dalam renderer disembunyikan.
  - Tanpa logo atau merek resmi pemerintah: label teks "Simulasi TKA" dan identitas Titian Asa.
- **Builder:** pilihan tema "TKA" di editor kuis; per grup, bagian "Data soal TKA" (kode, bentuk, elemen, subelemen, kompetensi, indikator) disimpan di `group.tka`. Tipe `QuizQuestionGroup.tka` baru di `lib/latihan/quiz/types.ts`.
- **Isi:** 22 paket dari 36 PDF (23 unik, sisanya salinan `(1)`/`(2)` byte-identik). Ekstraksi ke JSON (`TKA BANK/_hasil/<slug>/paket.json` + `img/`, kontrak di `KONTRAK.md`, validator `validasi.py`) lewat 12 agen; 635 nomor soal, 260 gambar. Empat PDF berlapis teks (30 soal variasi Matematika SMP, 30 soal Bahasa Indonesia, dua soal latihan SMP) memuat kunci → `kunci_dari: "pdf"`. **18 PDF tangkapan layar tidak memuat kunci: kuncinya disusun AI dan ditandai `ragu` bila kurang yakin** (`kunci_dari: "disusun_ai"`, deskripsi modul mencantumkannya). Perlu ditinjau guru/pakar sebelum dipakai sebagai nilai resmi.
  - Soal yang memang kosong di PDF ("OTW") dilewati: Bahasa Indonesia SMA Pilihan no. 1–4 dan 27–30, Fisika no. 6, Biologi no. 25–27, PPKn no. 21. Beberapa soal terpotong di tangkapan layar; daftar lengkap ada di field `catatan` tiap `paket.json`.
  - Duplikat soal dalam satu PDF (kode soal sama) dihitung sekali.
- **Impor:** `cmd/tools/impor_tka` (backend `latihan`). Program publik "Try Out TKA" (`subject: tka`, slug `bank-tka`), tiga folder (TKA SD/SMP/SMA), satu modul + satu item `kuis_umum` per paket, semua publik/taker (gratis; belum ada keputusan pemilik soal langganan untuk TKA). Waktu = 2 menit × jumlah nomor soal (perkiraan, `-menit-per-soal`), `max_attempts 1000`. Id UUID v5 dari slug, jadi bisa diulang. Sebelum menulis, tiap kunci dijalankan lewat `grading.Verify` server: 848 kunci diperiksa, 0 bermasalah. Gambar disalin ke `…/titian-backend-go/.cache/latihan-media/tka/<slug>/` (URL `/latihan-media/tka/<slug>/<berkas>`). Hanya DB dev `titian_bun`; sama seperti B4.1, media perlu diunggah ke R2 dan awalan URL ditulis ulang sebelum prod.
  ```
  DATABASE_URL=… GO_DOCKER_ARGS="-v <TKA BANK/_hasil tanpa spasi>:/tka:ro -v <MEDIA>:/media" ./go.sh run ./cmd/tools/impor_tka -hasil /tka -media-dir /media [-apply]
  ```
  (`go.sh` tidak bisa memuat jalur ber-spasi di `GO_DOCKER_ARGS`; pasang lewat symlink atau salin ke jalur tanpa spasi.)
- **Tes:** `themes/tka/steps.test.ts` (pemecahan langkah, status, ringkasan, bentuk soal). Web: `tsc --noEmit` bersih, `bun run test` 224 lulus. Go: `go vet ./cmd/tools/impor_tka` bersih. Pratinjau visual (Chrome headless, data nyata dari DB: Matematika SD, Fisika SMA, termasuk gambar, kunci rumus, Hierarki Indikator, tabel Benar/Salah, daftar soal) sudah dicek; rute pratinjau sementara dihapus.
- **QA browser penuh (butuh izin pemilik; belum dilakukan):** login siswa → `/latihan/ujian?ujian=tka` → buka modul → kerjakan sampai Selesai → hasil dan kunci; aktifkan pengawasan di tab Pengawasan modul TKA, kerjakan sebagai siswa, pantau di `/pengawasan`; builder: ubah tema modul lain ke TKA dan isi "Data soal TKA". Tampilan terang (hanya mode gelap yang dipratinjau) dan layar ponsel juga belum dilihat.
- **Belum dilakukan:** hasil akhir bergaya TKA (layar skor setelah kumpul memakai tampilan hasil umum); soal Menjodohkan/Isian TKA tidak ada di bank ini sehingga belum diuji di tema TKA; durasi resmi per mata uji belum diketahui.
- **B4.2, perbaikan keterbacaan (2026-11-21):** (1) `normaliseMathDelimiters` tidak lagi membungkus ulang kurung di dalam `$…$`/`$$…$$`, dan `$$x$$` satu baris diberi pagar `$$` di baris sendiri supaya menjadi blok display (sebelumnya dibaca math inline: kecil dan rapat); berlaku untuk semua tampilan markdown Latihan. (2) `lib/latihan/tka-mode.ts` (`TkaModeContext`) menyala di seluruh kartu soal TKA: `\frac` dipaksa `\dfrac` (pembilang/penyebut ukuran penuh, termasuk di pilihan), `QNum` dan kepala grup disembunyikan, kartu pilihan tidak lagi bersarang. (3) CSS `.tka-room` di `screens/globals.css`: KaTeX 1,3×, jarak rumus, pilihan rata tengah. (4) `QMD` menggambar baris `::image` (pilihan bergambar). (5) Ukuran huruf bawaan ruang TKA 115%; footer muat di layar ≤ 375 px; hierarki indikator terlipat di layar kecil. Tes: `markdown-math.test.ts`.
- **B4.2, pengelompokan test TKA di `/latihan/ujian?ujian=tka`:** test dikelompokkan seperti katalog beranda: TKA SD/MI, TKA SMP/MTs, Latihan tambahan SMP/MTs, SMA/MA — mata uji wajib, Saintek (Matematika Tingkat Lanjut, Fisika, Kimia, Biologi), Soshum (Ekonomi, Geografi, Sejarah, Sosiologi, PPKn), dan Bahasa pilihan; tiap kelompok bisa dilipat dan menampilkan jumlah test. Logika di `lib/latihan/ujian.ts` (`kelompokTka`, `kelompokkanTestTka`, `tagDariJudul`; tes `ujian-tka.test.ts`) memakai tag modul hasil impor (`tka, jenjang, mapel, kategori`). `GET /latihan/programs/{id}/modules` kini juga mengirim `tags` dan `is_folder` (`internal/latihan/modules.go`); sebelum API di-restart, web membaca jenjang dan mapel dari judul modul.
- **B4.2, tata letak TKA di Ujilab (revisi):** `/latihan/ujian?ujian=tka` menampilkan kartu per jenjang dulu (gaya katalog beranda: ikon, lencana, fase dan kelas, deskripsi, chip mata uji, jumlah test, tombol "Latihan …"); memilih kartu membuka daftar test jenjang itu dengan tombol "Semua jenjang" untuk kembali. Data kartu di `KELOMPOK_TKA` (`lib/latihan/ujian.ts`).
- **B4.2, siap production (2026-11-21, backend `16fd3a1`, web `442d546`):** `impor_tka` kini berjalan di server seperti `impor_bank_parilabs`: `-tanpa-media` (gambar sudah disajikan API di `/latihan-media/tka/…`), `-media-base https://api.titianasa.com/latihan-media`, `-media-cek url` (260 URL gambar production terbaca), `-periksa` (baca ulang akses, folder, tautan program, dan config). Server hanya butuh berkas `paket.json` (tanpa `img/`).
  - **Kunci:** paket `kunci_dari: "disusun_ai"` hanya ditulis bila punya `kunci_diperiksa` (hasil pemeriksaan ulang); `-izinkan-belum-diperiksa` untuk sengaja melewati. Deskripsi modul: "Kunci jawaban disusun dan diperiksa ulang tim Titian; bukan kunci resmi." (sudah diperiksa), "… disusun AI dan belum diverifikasi pakar." (belum), "… dari sumber soal; bukan kunci resmi." (`pdf`).
  - **Soal `ragu`:** tetap dinilai (penilai tidak punya soal tanpa nilai, dan membuangnya merusak tabel Benar/Salah), pembahasannya diberi "Catatan Titian: kunci soal ini belum dapat dipastikan. Jadikan bahan diskusi, bukan acuan.", dan deskripsi modul menyebut jumlah butirnya. Tanda `ragu` tidak dikirim.
  - Web: tautan sumber dan kata panjang di stimulus dipatahkan di ruang TKA (sebelumnya melebar di layar 375 px). Pratinjau 375 px dan desktop, terang dan gelap, sudah dicek.
