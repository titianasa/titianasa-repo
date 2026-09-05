# Phase 28 (ticket-numbering) — Attendance Verification (Meeting Provider)

## Keputusan scope (baca duluan)

Fitur baru di luar 14 item "kerjakan semuanya" (yang sudah tuntas semua,
lihat `docs/STATE.md`) — diminta user secara eksplisit setelah membahas
kelayakan integrasi Google Meet/Zoom API untuk mencegah tutor mengklaim
mengajar padahal tidak, dan siswa mengklaim hadir padahal tidak.

**2 keputusan diminta eksplisit ke user dulu lewat `AskUserQuestion`**
(pola sama Phase 6/9's provider decision) sebelum kode ditulis:
1. **Kredensial belum ada** — user pilih **bangun dulu sebagai stub**
   (pola persis `PaymentProvider`/`StubQrisProvider` P9-007), bukan
   menunggu kredensial nyata dulu.
2. **Provider target**: user pilih **Google Meet** sebagai target utama
   integrasi asli nantinya (selaras dengan Google OAuth login yang
   sudah ada, `users.google_id` sudah tersedia buat identity-matching).

**Temuan riset sebelum desain** (lewat agent Explore, dikonfirmasi baca
langsung):
- `attendance_records` (P9-004/005) murni manual — tutor klik hadir/
  tidak, **nol field join-time/leave-time/duration**. Kolom `method`
  sengaja punya CHECK 1-nilai (`'manual'`) dari awal supaya nanti bisa
  ditambah nilai baru secara ADDITIVE — persis slot yang fitur ini isi.
- `cohorts.meeting_url` (P23-001) cuma link eksternal yang tutor
  tempel sendiri — **tidak ada** pembuatan meeting lewat API, tidak
  ada baca data peserta.
- Google OAuth sekarang cuma verifikasi `id_token` (Sign in with
  Google) — BUKAN OAuth2 authorization-code flow. Meet REST API
  (`conferenceRecords`/`participants`) butuh flow yang sama sekali
  beda + biasanya akun Google Workspace (bukan Gmail biasa) sebagai
  organizer. Nol `googleapis`/`google-auth-library` di dependencies,
  nol `GOOGLE_CLIENT_SECRET` di `.env`.
- **`cohorts.schedule` (jsonb) TERNYATA cuma passthrough** — dikonfirmasi
  grep, cuma dibaca-tulis apa adanya di `cohort_handler.ts`, tidak
  pernah di-parse jadi apa pun. Tidak ada konsep "1 sesi kelas konkret
  dengan jadwal mulai/selesai" di mana pun di skema — `attendance_records`
  cuma punya `session_date` (text tanggal) yang dipilih bebas saat
  tutor menandai, bukan sesi yang direncanakan duluan. **Gap struktural
  ini harus ditutup dulu** sebelum verifikasi jadwal (join maks 10
  menit setelah mulai, dst) bisa dihitung — makanya P28-001 menambah
  tabel `class_sessions` baru, bukan menambal `cohorts.schedule`.
- `users.google_id` (unique) sudah ada sejak awal — inilah yang jadi
  kunci identity-matching Layer 2 (Platform Account ↔ Google Account
  ↔ Meet Participant) dari desain 3-lapis yang didiskusikan dengan
  user, TANPA perlu kolom baru untuk itu.

**Keputusan arsitektur — reuse, bukan sistem paralel**:
- `attendance_records` (siswa) TETAP jadi tabel keputusan akhir — hasil
  verifikasi MENULIS ke situ dengan `method = 'online'` (slot yang
  sudah disiapkan sejak P9-004), bukan tabel attendance kedua yang
  terpisah. `markedBy` diubah jadi nullable (migrasi aditif) — `NULL`
  berarti "diverifikasi sistem", BUKAN mengatasnamakan tutor secara
  keliru seolah tutor yang menandai (justru itu yang mau dicegah).
  CHECK `status` ditambah 1 nilai baru `'partial'` (hadir tapi durasi
  kurang dari ambang batas) — additive, bukan breaking.
- **Attendance TUTOR tidak pernah ada tabelnya sebelumnya** (masuk akal
  — tutor yang menandai attendance siswa, jadi tidak masuk akal tutor
  menandai attendance dirinya sendiri, itu justru celah kecurangan yang
  ingin ditutup). Baris partisipan tutor cukup hidup di
  `session_participant_records` (tabel evidence baru) — jadi basis buat
  Tutor Performance/KPI, TIDAK butuh entri paralel di `attendance_records`.
- **Identity matching HANYA lewat `google_id`, TIDAK PERNAH fuzzy-match
  nama** — persis kekhawatiran user sendiri ("John" vs "John Smith" vs
  "John - iPhone") — peserta yang tidak cocok `google_id`-nya ke user
  manapun di roster TETAP TERSIMPAN sebagai evidence (`user_id: null`)
  tapi TIDAK PERNAH otomatis diasumsikan siapa dia.
- **`GoogleMeetProvider` TIDAK ditulis di fase ini** — sama persis
  preseden `PaymentProvider`/P9-007 (Midtrans/Xendit belum ditulis
  sampai kredensial ada): menulis integrasi asli tanpa cara mengetesnya
  sama sekali (nol kredensial, nol `googleapis` package) cuma
  menghasilkan kode yang tidak pernah diverifikasi jalan. Interface
  `MeetingProvider` didesain supaya implementasi asli tinggal
  "implement interface ini", persis seperti komentar `payment_provider.ts`
  sendiri soal `DeepSeekProvider` yang "slot in next to FakeAIProvider".
- **Dieksplisit DIDEFER**: dispute/appeal workflow (status `DISPUTED`
  dari diskusi awal — butuh alur banding sendiri, bukan quick add);
  Zoom provider (user pilih Google Meet sebagai target utama, interface
  tetap provider-agnostic jadi Zoom bisa nyusul tanpa ubah service);
  webhook real-time dari Google (`sync-attendance` di-trigger manual/
  polling, bukan event push — webhook Google Meet butuh setup admin
  Workspace terpisah, di luar scope stub); differentiasi ambang batas
  tutor vs siswa (1 rasio durasi dipakai untuk keduanya di config, bisa
  dipisah nanti tanpa migrasi karena ini env config bukan kolom DB);
  concurrency/capacity planning 1 akun organizer (pertanyaan operasional
  yang baru relevan begitu kredensial nyata ada).

## Ticket

### P28-001 — Skema + MeetingProvider abstraction
**Depends on:** P9-004 (`attendance_records`), P9-002 (`google_id`)
**Tabel baru (additive):** `class_sessions` (cohort_id, session_date,
scheduled_start, scheduled_end, meeting_provider, external_meeting_id,
join_url, status), `session_participant_records` (class_session_id,
user_id nullable, role, external_participant_name,
external_google_account_id nullable, first_joined_at, last_left_at,
duration_seconds, join_session_count, verification_status).
**Migrasi additive ke `attendance_records`:** `markedBy` jadi nullable,
`class_session_id` FK nullable baru, CHECK `status` tambah `'partial'`,
CHECK `method` tambah `'online'`.
**Kode baru:** `meeting_provider.ts` (interface `MeetingProvider` +
`StubMeetingProvider` — `createMeeting` generate id+url palsu jelas
recognizable, `getParticipantReport` baca dari
`session_participant_records` yang sudah disimulasikan, tidak ada
network call).

### P28-002 — Verification engine + REST endpoints
**Status:** done
**Depends on:** P28-001
**Endpoint baru:**
- `POST /cohorts/:id/class-sessions` — buat sesi terjadwal, panggil
  `MeetingProvider.createMeeting`.
- `GET /cohorts/:id/class-sessions` — discovery (dibangun dari awal,
  bukan ditambal belakangan — pola berulang di sesi ini).
- `GET /class-sessions/:id` — detail + `join_url`.
- `POST /class-sessions/:id/simulate-participant` — DEV-ONLY, ditolak
  403 kalau `meeting_provider !== 'stub'` (tidak bisa dipakai "curang"
  di sesi yang seharusnya pakai provider asli).
- `POST /class-sessions/:id/sync-attendance` — idempotent, jalankan
  verification engine, tulis ke `attendance_records` (method='online').
- `GET /class-sessions/:id/attendance` — laporan evidence penuh (roster
  × partisipan × status), bentuk persis mockup yang didiskusikan user.
**Acceptance Criteria:**
- [x] Partisipan tanpa `google_id` yang cocok TETAP tersimpan sebagai
  evidence, TIDAK PERNAH otomatis diasumsikan sebagai user tertentu.
- [x] `sync-attendance` dipanggil 2x berturut-turut menghasilkan hasil
  identik (idempotent), bukan baris dobel — dites otomatis DAN
  diverifikasi manual lewat curl terhadap dev DB nyata.
- [x] `simulate-participant` ditolak (422) kalau `role='tutor'` dengan
  `user_id` yang bukan tutor asli cohort itu, dan ditolak (403) kalau
  bukan manager yang memanggil.
- [x] Status dihitung dari rasio durasi (`attendanceMinDurationRatio`)
  + keterlambatan join (`attendanceLateJoinMinutes`), bukan boolean
  hadir/tidak sederhana — dibuktikan lewat 3 skenario nyata (present/
  late/partial) di 1 sesi yang sama, plus 4 unit test batas nilai murni.
- [~] `simulate-participant` ditolak di sesi `meeting_provider!='stub'`
  — logic-nya ada (`class_session_service.ts`), TAPI tidak ada cara
  membuat sesi `google_meet` di sistem ini sama sekali sejak
  `GoogleMeetProvider` sengaja belum ditulis (lihat "Keputusan scope")
  — jadi cabang ini genuinely tidak bisa dites end-to-end sampai
  provider asli ada. Bukan gap yang terlewat, murni konsekuensi logis
  dari keputusan stub-first.

**1 bug nyata ditemukan+diperbaiki saat menulis test**: draf pertama
memfilter roster ke `enrollments.status === 'active'` — tapi alur
manual attendance yang sudah ada (`attendance_service.markAttendance`)
TIDAK PERNAH membuat pembedaan itu (cuma cek baris enrollment ada,
apapun status-nya), dan `POST /cohorts/{id}/enrollments` (self-enroll)
membuat baris berstatus `'pending'` sampai pembayaran — bukan
`'active'`. Filter yang salah ini bikin siswa yang belum bayar TIDAK
PERNAH muncul di verifikasi kehadiran sama sekali, padahal manual
marking selalu bisa. Diperbaiki jadi `status !== 'cancelled'`, sesuai
perilaku jalur manual yang sudah ada — ditemukan lewat test otomatis
(3 test gagal), bukan lewat produksi.

**Diverifikasi lewat REST langsung terhadap dev server nyata** (skrip
seed sekali-pakai, dihapus + data dibersihkan setelah): tutor buat
sesi → simulasi tutor (on-time, 65 menit) → `present`; siswa A
(terlambat 20 menit, 55 menit) → `late`; siswa B (on-time, cuma 20
menit) → `partial`; `sync-attendance` menulis 2 baris
`attendance_records` dengan `method='online'`/`marked_by=NULL` persis
sesuai desain; re-run `sync-attendance` tidak menambah baris; siswa A
lewat `GET /class-sessions/{id}/attendance` cuma lihat baris tutor +
dirinya sendiri, TIDAK lihat baris siswa B. 13 test otomatis baru
(`tests/attendance-verification.test.ts`) semuanya lulus, plus 526
test lama tetap hijau (2 kegagalan pre-existing di
`leaderboard-league.test.ts` dikonfirmasi TIDAK terkait — reproduce
identik di kode SEBELUM Phase 28 lewat `git stash`, disebabkan data XP
asli akun user sendiri yang bocor ke agregat test karena test itu
query platform-wide tanpa scoping, bukan sesuatu yang disentuh Phase 28).

### P28-003 — Frontend: buat sesi + simulasi + laporan attendance
**Status:** done
**Depends on:** P28-002
**Deskripsi:** Panel "Sesi Kelas Terverifikasi" di halaman kelola kelas
tutor (Phase 16/17's `/marketplace/kelas/{id}`) — buat sesi baru, lihat
`join_url`, kontrol simulasi (cuma tampil kalau provider stub, dilabeli
eksplisit "simulasi" — pola sama Phase 14/15's simulate button), tabel
laporan attendance per sesi (join/leave/duration/status, evidence
penuh) buat tutor DAN admin/org.

### P28-004 — Test suite + exit checkpoint
**Status:** done
**Depends on:** P28-001 s/d P28-003
**DoD:** `bun test` 537/539 (2 kegagalan pre-existing tidak terkait, lihat
P28-002's catatan), `bunx tsc --noEmit`/`lint`/`build` bersih di
`titian-web`, diverifikasi PENUH lewat `Bun.WebView` end-to-end.

**1 bug FE nyata ditemukan+diperbaiki saat verifikasi browser**: Select
peserta simulasi awalnya menampilkan raw UUID (`2eb7bacd-24ad-...`)
alih-alih nama — Radix `SelectValue` cuma tahu label sebuah opsi
SETELAH `SelectContent` sempat mount (dropdown pernah dibuka sekali);
sebelum itu dia fallback ke `value` mentah. Diperbaiki dengan render
label secara eksplisit (`{participantOptions.find(...)?.name}`)
sebagai children `SelectValue`, bukan mengandalkan auto-derivation
Radix. Ditemukan dari screenshot asli, bukan cuma baca kode.

**1 karakteristik harness yang sudah dikenal, dicatat ulang**: klik
tombol "Kelola" kadang tidak ter-registrasi pada percobaan PERTAMA
kalau `Next.js dev` sedang di tengah Fast Refresh rebuild — sama
persis pola flaky yang sudah didokumentasikan di `docs/tickets/phase-26.md`.
Bukan bug aplikasi (skrip verifikasi dengan retry-loop selalu berhasil
di percobaan ke-2), jadi tidak diperbaiki di kode — dicatat di sini
supaya tidak disalahpahami sebagai regresi di sesi berikutnya.

**Diverifikasi PENUH lewat `Bun.WebView` browser asli** (skrip
sekali-pakai, dihapus + data dibersihkan setelah): tutor buka
`/marketplace/kelas/{id}` → tab "Sesi Live" → buat sesi baru (dapat
`join_url` stub) → buka panel "Kelola" → simulasikan diri sendiri
sebagai tutor (on-time, 65 menit) → ganti pilihan ke siswa → simulasikan
siswa (terlambat 20 menit, cuma 20 menit durasi) → klik "Sinkronkan
Kehadiran" → laporan LANGSUNG menunjukkan **Pak Guntur · Tutor —
present (65 menit)** dan **Nadia · Siswa — partial (20 menit)**, badge
sesi berubah jadi "completed", Select menampilkan nama asli (bukan
UUID). Screenshot asli disimpan sebagai bukti selama sesi, dihapus
bersama data demo setelah verifikasi selesai.

**Bonus temuan operasional (bukan bagian scope Phase 28, ditemukan
kebetulan saat user mencoba `/mengajar` secara manual)**: `platform_admin`
yang belum pernah jadi tutor mendapat `internal_error` (500 mentah,
FK violation) saat mencoba "Buat Produk", karena
`learning_product_service.createProduct` mengizinkan role `platform_admin`
(sesuai matrix permission) tapi langsung insert `tutor_id = ctx.userId`
tanpa cek `tutor_profiles` ada dulu. Diperbaiki: provisioning lazy
`tutor_profiles` untuk caller yang lolos permission tapi belum punya
profile, pola sama `assignDefaultStudentRole` (P9-002). Di luar scope
ticket ini tapi dicatat di sini karena ditemukan+ditutup di sesi yang
sama — lihat commit terpisah di `titian-backend-bun`.

### P28-005 — GoogleMeetProvider: integrasi Meet asli
**Status:** done
**Depends on:** P28-001

**Eligibility test nyata dilakukan bersama user (2026-09-05)**, di luar
kode aplikasi (skrip sekali-pakai `~/secrets`/scratchpad), sebelum
menulis 1 baris kode produksi: user bikin OAuth Client ID terpisah
(Desktop app/`installed` type, bukan reuse client login) di Google
Cloud Console project `titian-asa`, dengan scope
`meetings.space.readonly` + `meetings.space.created`. Hasil tes
terhadap akun **Google personal `@gmail.com` dengan Google One 2TB**
(BUKAN Workspace):
- `conferenceRecords.list` — **berhasil**, 200 OK.
- `conferenceRecords/{id}/participants` — **berhasil**, data peserta
  penuh (nama, `signedinUser.user` = `users/{id}` yang FORMATNYA SAMA
  dengan `users.google_id` yang sudah ada sejak login, join/leave time)
  setelah dites dengan meeting nyata 3 peserta.
- `spaces.create` dengan `artifactConfig.recordingConfig.autoRecordingGeneration: "ON"`
  — **berhasil**, recording nyala otomatis tanpa klik manual.
- `attendanceReportGenerationType: "GENERATE_REPORT"` (fitur laporan
  kehadiran bawaan Google, Developer Preview) — **TIDAK berhasil**
  diakses lewat REST langsung (404 "Method not found" di v2beta) —
  DIDEFER, tidak menghalangi karena `participants` mentah sudah cukup.

**Kesimpulan penting: klaim "harus Google Workspace" dari sumber
sekunder yang dibaca sebelum ticket ini ditulis TERBUKTI SALAH/
ketinggalan zaman** untuk kasus penggunaan ini — dikonfirmasi empiris,
bukan cuma dari dokumentasi resmi Google (yang sendiri tidak eksplisit
menyebut syarat ini di halaman manapun yang dicek).

**Implementasi**: `google_meet_provider.ts` (`GoogleMeetProvider`
implements `MeetingProvider`) — `createMeeting` bikin space asli +
auto-recording ON; `getParticipantReport` filter `conferenceRecords`
by `space.name`, ambil yang paling baru, map `signedinUser.user` (strip
prefix `users/`) langsung ke `users.google_id` tanpa transformasi
tambahan. `index.ts` pilih `GoogleMeetProvider` kalau
`GOOGLE_MEET_CLIENT_ID`/`_SECRET`/`_REFRESH_TOKEN` (organizer tunggal,
akun personal user sendiri) ketiganya di-set, fallback
`StubMeetingProvider` kalau tidak (dev/CI). `attendance_verification_service.syncAttendance`
sekarang benar-benar panggil `getParticipantReport` untuk sesi
non-stub (sebelumnya cuma jalur stub yang terisi, diisi manual lewat
`simulate-participant`).

**1 bug nyata ditemukan+diperbaiki dari smoke test end-to-end pertama**:
`class_session_service.createSession` HARDCODE `meeting_provider: 'stub'`
ke row `class_sessions`, apa pun provider yang benar-benar dipakai —
tidak masalah selama cuma stub yang ada, tapi begitu `GoogleMeetProvider`
nyata dipakai, ini berarti sesi ASLI tetap tercatat `'stub'`, yang berarti
`simulate-participant` (seharusnya DITOLAK di sesi non-stub) masih akan
diterima di sesi yang seharusnya sudah diverifikasi asli — celah
kecurangan yang justru mau dicegah fitur ini. Diperbaiki: `MeetingProvider`
dapat field `name` (`'stub'` | `'google_meet'`), ditulis ke DB apa
adanya, bukan literal hardcode.

**Diverifikasi lewat smoke test kode produksi asli** (skrip sekali-pakai,
dihapus setelah): panggil `class_session_service.createSession` LANGSUNG
(bukan skrip terpisah) terhadap cohort nyata milik user sendiri →
`meeting_provider: "google_meet"`, `join_url` link Meet asli yang bisa
diklik. Row test dihapus lagi setelah verifikasi.

**Dieksplisit DIDEFER**: `attendanceReportGenerationType` (laporan
kehadiran bawaan Google, belum bisa diakses lewat cara yang dicoba);
`participantSessions` sub-resource (rejoin count presisi — MVP pakai
`earliestStartTime`/`latestEndTime` saja, cukup untuk kebutuhan
verifikasi); test otomatis `bun:test` untuk `GoogleMeetProvider`
sendiri (network call asli ke Google, diverifikasi lewat smoke test
manual seperti `DeepSeekProvider` di Phase 6, bukan unit test).

---

## Checkpoint keluar Phase 28
1. [x] `class_sessions`+`session_participant_records` menyimpan evidence
   mentah, `attendance_records` tetap jadi 1 sumber kebenaran status
   akhir (method='online' vs 'manual' hidup berdampingan, bukan sistem
   paralel) — dibuktikan lewat query langsung ke dev DB.
2. [x] Identity matching murni `google_id`, nol fuzzy-name-matching —
   `simulate-participant` cuma terima `user_id` platform asli, tidak
   pernah menebak dari nama string.
3. [x] Ambang batas (durasi/keterlambatan) benar-benar menentukan status
   berbeda (present/late/partial/absent), dibuktikan lewat skenario
   nyata (curl DAN browser asli), bukan cuma dites logic terisolasi.
4. [x] **Update 2026-09-05 (P28-005)**: `GoogleMeetProvider` SEKARANG
   SUDAH DITULIS DAN LIVE — awalnya sengaja ditunda (checkpoint asli
   di bawah ini disimpan sebagai catatan sejarah keputusan, bukan
   dihapus), tapi eligibility test nyata bersama user membuktikan akun
   Google personal 2TB (Google One, BUKAN Workspace) BISA akses
   `conferenceRecords`/`participants` DAN `autoRecordingGeneration` —
   lihat P28-005 di atas untuk detail lengkap tes+implementasi+bug yang
   ditemukan. Model arsitektur **1 akun organizer terpusat** terpakai
   persis seperti dirancang, `MeetingProvider` interface tidak perlu
   diubah sama sekali untuk menampung provider asli ini.

   *(Catatan asli sebelum P28-005, disimpan untuk konteks keputusan):*
   `GoogleMeetProvider` SENGAJA belum ditulis (didokumentasikan,
   bukan diam-diam skip) — `MeetingProvider` interface siap disambung
   begitu kredensial Workspace ada.
