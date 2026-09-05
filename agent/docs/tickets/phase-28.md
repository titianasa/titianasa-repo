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

### P28-006 — Lihat hasil rekaman dari dalam app
**Status:** done
**Depends on:** P28-005

Ditanyakan user langsung setelah P28-005 selesai: "management, meeting,
attendance, dan melihat hasil rekaman ada dimana di aplikasi kita" —
jawaban jujurnya saat itu: rekaman TIDAK ADA di mana pun di app,
cuma bisa dicari manual di Google Drive organizer. Ditutup:
`MeetingProvider.getRecordingStatus` baru (state `not_found`/
`in_progress`/`ready` — Meet API's `recordings.state` beneran punya
3 nilai ini, bukan disederhanakan jadi boolean, supaya UI bisa bedakan
"belum ada" dari "lagi diproses Google"), resolve
`driveDestination.exportUri` dari `conferenceRecords/{id}/recordings`.
`GET /class-sessions/:id/recording` baru (audiens sama `getSession` —
manager atau siswa terdaftar). FE: tombol "Lihat Rekaman" di panel
Sesi Live, cuma tampil untuk sesi non-stub, poll tiap 15 detik selama
`in_progress`. 2 test baru (stub selalu `not_found`, siswa terdaftar
bisa akses).

### P28-007 — Organizer dipindah ke akun terpisah + temuan kunci soal recording
**Status:** done untuk MVP (pemindahan organizer selesai+live; bot
auto-join DICOBA lalu DIHENTIKAN — lihat "Keputusan akhir" di bawah)
**Depends on:** P28-005

**Konteks**: user minta 2 peningkatan fitur — (1) tutor bisa batasi
siapa yang boleh join meeting (cuma siswa terdaftar), (2) perbaiki bug
recording yang cuma nyala kalau `ndsanja@gmail.com` (pemilik akun 2TB)
ikut join — kalau tutor lain + siswa lain jalan meeting tanpa
`ndsanja@gmail.com`, recording SAMA SEKALI tidak nyala.

**Riset empiris untuk #1 (pembatasan peserta) — GAGAL, dikonfirmasi
langsung ke akun**: `spaces.config.accessType` ganti ke `RESTRICTED` →
`403 PERMISSION_DENIED "updateAccessType is not available to the
user"`; `spaces.members.create` (untuk invite spesifik + kasih role
`COHOST`) → `404 Method not found` di v2 MAUPUN v2beta. **Kontrol akses
berbasis member/whitelist genuinely tidak tersedia untuk akun Google
personal** — beda dari `attendanceReportGenerationType` kemarin yang
"sekadar" salah versi API, ini benar-benar gerbang fitur Workspace-only
(`FEATURE_UNAVAILABLE_TO_USER`). **Diputuskan bersama user**: TIDAK
upgrade ke Workspace untuk ini — cukup andalkan yang sudah ada
(siapa pun bisa join link, tapi sistem attendance verification
Titian Asa sendiri cuma mengakui siswa terdaftar sebagai "hadir" —
orang asing yang ikut join tetap tersimpan sebagai evidence tapi
tidak pernah dianggap hadir resmi).

**Riset empiris untuk #2 (bug recording) — temuan penting yang
mengubah arah desain**: awalnya dihipotesiskan mungkin SIAPA PUN
peserta yang punya entitlement rekam sendiri (Google One 2TB/Workspace)
bisa memicu recording, terlepas dari siapa PEMBUAT space-nya lewat API
— kalau benar, solusinya cukup "setiap tutor pakai akun 2TB sendiri",
TANPA bot. **User menolak arah ini secara eksplisit** ("itu bukan
solusi... saya mau peserta/tutor memang gak perlu langganan Google
2TB"), jadi dites langsung: buat 1 space via API `ndsanja@gmail.com`
(dengan `autoRecordingGeneration: ON`), lalu **`pedasnyabumbu@gmail.com`
join SENDIRIAN** (device Playwright headful nyata di layar user,
sesi login asli, BUKAN simulasi) tanpa `ndsanja@gmail.com` ikut sama
sekali. Hasil: `conferenceRecords` mengonfirmasi `pedasnyabumbu` BENAR
join (conference record + participant row nyata) — tapi
`conferenceRecords/{id}/recordings` balik **KOSONG total** (`{}`), tidak
ada recording apa pun. **Kesimpulan terkonfirmasi**: hak rekam terikat
ke akun yang MEMBUAT space via API (space owner), bukan sekadar
"siapa saja yang hadir dan punya paket 2TB sendiri" — jadi bot
auto-join (kalau dibangun nanti) harus login+join SEBAGAI akun yang
SAMA dengan yang dipakai `GoogleMeetProvider` untuk `createMeeting`,
bukan akun "tamu perekam" yang berbeda.

**Keputusan user berikutnya**: daripada bot join meeting `ndsanja`'s
punya, **`pedasnyabumbu@gmail.com` jadi organizer TUNGGAL** yang
menggantikan `ndsanja@gmail.com` sepenuhnya untuk fitur Meet —
memisahkan risiko otomasi (kalau bot auto-join dibangun nanti dan
kena flag Google) dari akun pribadi founder. **Penting, dan sudah
dikonfirmasi user secara eksplisit**: ini TIDAK terikat ke `ndsanja@gmail.com`-
nya-sebagai-akun-platform sama sekali — siapa pun user Titian Asa
(tutor mana pun, termasuk `ndsanja@gmail.com` sendiri sebagai
platform_admin/tutor) yang memicu "Buat sesi" tetap menghasilkan room
milik `pedasnyabumbu@gmail.com` — persis arsitektur `MeetingProvider`
yang sudah dirancang sejak awal (1 instance dipakai semua caller,
terlepas `ctx.userId` siapa). **Nol perubahan kode dibutuhkan** — cuma
ganti `GOOGLE_MEET_CLIENT_ID`/`_SECRET`/`_REFRESH_TOKEN` di `.env`.
Kredensial baru: project Google Cloud terpisah (`crucial-cycling-507703-e4`),
OAuth Client ID Desktop-app baru, refresh token dimint ulang untuk
`pedasnyabumbu@gmail.com`. Diverifikasi lewat smoke test kode produksi
asli (`class_session_service.createSession` langsung) — `join_url`
Google Meet baru berhasil dibuat, row test dihapus lagi.

**Belum dikerjakan (di luar scope P28-007 ini)**: bot auto-join
sungguhan (Playwright + sesi login persisten + scheduler mengikuti
`class_sessions.scheduled_start`/`scheduled_end`) — baru tahap
eligibility test manual (1 kali login+join manual lewat browser
Playwright headful, bukan otomasi terjadwal). Risiko yang sudah
didiskusikan eksplisit dengan user sebelum lanjut: ceiling konkurensi
keras (1 akun = 1 call bersamaan, kelas yang tumpang tindih waktu
cuma 1 yang kebagian rekaman), risiko akun kena flag/suspend Google
karena pola login+join otomatis berulang, bot akan TERLIHAT sebagai
peserta asli di setiap kelas (nama "Bumbu Pedas" kecuali profil
diganti), dan otomasi browser rapuh terhadap perubahan UI Meet
(beda dari REST API yang stabil).

**Bot auto-join DICOBA (2026-09-05) — DIBLOKIR Google, dihentikan.**
Proof-of-concept dijalankan: sesi login `pedasnyabumbu@gmail.com` yang
sudah tervalidasi (dari tes join manual sebelumnya) dipakai ulang oleh
skrip Playwright (headful, di layar user) untuk membuat meeting lewat
API `pedasnyabumbu` SENDIRI (bukan lagi join punya akun lain — pola
yang benar sesuai temuan di atas), lalu bot MENCOBA join sepenuhnya
otomatis (klik "Join now" via skrip, tanpa bantuan manusia). **Hasil:
Google MENOLAK join-nya sama sekali** — layar "You can't join this
video call" / "No one can join a meeting unless invited or admitted by
the host", padahal akun ini adalah host/pembuat space itu sendiri.
Dibandingkan dengan tes join MANUAL sebelumnya (berhasil, sesi login
yang SAMA) — satu-satunya beda adalah klik "Join" dilakukan skrip,
bukan manusia. **Kesimpulan: Google mendeteksi pola join terprogram
sebagai mencurigakan dan memblokirnya secara aktif** — bukan risiko
teoretis lagi, sudah terjadi nyata di percobaan pertama. Percobaan
DIHENTIKAN saat itu juga (tidak diulang-ulang) untuk menghindari akun
`pedasnyabumbu@gmail.com` makin ter-flag, karena akun yang sama juga
dipakai untuk seluruh fitur Meet yang SUDAH JALAN (attendance
verification, dst).

**Keputusan akhir untuk MVP (2026-09-05, eksplisit dari user)**:
**bot auto-join DIBATALKAN**, bukan ditunda-untuk-nanti. Recording
tetap seperti sudah dibangun sejak P28-005 — cuma aktif kalau
`pedasnyabumbu@gmail.com` (organizer) benar-benar join SECARA MANUAL
oleh manusia (admin/operator Titian Asa). Ini keterbatasan yang
DITERIMA secara sadar untuk MVP, bukan bug yang masih dikejar. Fitur
attendance verification (P28-001..004) TIDAK terpengaruh sama sekali
— itu bekerja dari data `conferenceRecords`/`participants` yang selalu
ada begitu ADA peserta yang join meeting-nya (terlepas apakah
recording nyala atau tidak), jadi tetap berfungsi penuh untuk semua
kelas, dengan atau tanpa admin ikut merekam.

**Alternatif yang dicatat untuk PERTIMBANGAN NANTI, belum dikerjakan**
(tidak ada yang dipilih untuk dieksekusi sekarang):
1. **Per-tutor OAuth linking** — tiap tutor hubungkan akun Google
   sendiri, mereka join kelas sendiri secara natural (tanpa bot),
   recording jalan kalau akun mereka punya entitlement 2TB/Workspace.
   Butuh: alur OAuth web penuh di app, tabel kredensial per-tutor
   (perlu ENKRIPSI, bukan cuma 1 baris `.env` seperti sekarang), refactor
   `MeetingProvider` dari 1 instance bersama jadi per-tutor, DAN verifikasi
   app Google (proses resmi, berminggu-minggu) sebelum bisa dipakai
   tutor mana pun secara mandiri di luar daftar test-user manual.
2. **Zoom** (`auto_recording: cloud` + `join_before_host: true`) —
   secara arsitektur recording-nya server-side, TIDAK butuh siapa pun
   "hadir" sama sekali (beda fundamental dari Meet) — jadi TIDAK
   berisiko kena deteksi anti-bot seperti di atas, karena memang tidak
   ada bot yang join. Belum dites empiris. Trade-off diketahui: storage
   cuma 10GB/akun (vs 2TB Google One), konsep "Concurrent Meeting
   License" add-on (sampai 20 meeting bersamaan/akun) ada tapi harga
   dan kompatibilitas API-nya belum dikonfirmasi (perlu kontak sales
   Zoom atau tes langsung).
3. **Bridge Google Drive** (ide user, bagian PERTAMA dari 2 permintaan
   di sesi ini, BELUM DIBANGUN) — pakai kredensial `pedasnyabumbu@gmail.com`
   untuk otomatis kasih izin akses (Drive `permissions.create`) ke
   tutor+siswa yang benar-benar ikut kelas, supaya "Lihat Rekaman"
   (P28-006) benar-benar bisa dibuka (bukan cuma link yang valid API
   tapi mentok "perlu izin" di Drive). Butuh scope Drive baru + re-consent
   `pedasnyabumbu@gmail.com`. Independen dari keputusan bot — bisa
   dikerjakan kapan saja tanpa terikat pertimbangan di atas.

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
