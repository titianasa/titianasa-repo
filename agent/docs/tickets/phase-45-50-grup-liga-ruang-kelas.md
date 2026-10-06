# Phase 45–50 — Grup Belajar, Liga, Ruang Kelas & Grup Kelas (ADR-0015)

> **Catatan migrasi backend (2026-10-05, ADR-0020):** backend sedang dipindah ke Go. Tiket ini ditulis untuk `titian-backend-rust`, dan kode Rust tetap yang aktif sampai domain ini diport (G13, lihat `phase-51-go-migration.md`). Pekerjaan yang belum dieksekusi: bila G13 sudah selesai saat tiket ini dikerjakan, kerjakan di `titian-backend-go` (`#[sqlx::test]` → test Go dengan `testdb.New`, `services/x.rs` → `internal/<domain>/`); bila belum, kerjakan di Rust dan catat endpoint/migrasi barunya di daftar paritas fase 51.

📋 **Phase 45 SEDANG DIEKSEKUSI (2026-09-21)** — P45-001 s/d P45-004 (backend) dan P45-005 (frontend) selesai kode, verifikasi lihat catatan tiap tiket. Phase 46–50 masih rencana. Dasar keputusan: [ADR-0015](../adr/0015-grup-liga-ruang-kelas.md). Kapasitas anggota dikonfirmasi user 2026-09-21: **Grup Belajar 100, Grup Kelas 1000**.

Nomor fase 45–50 dipilih supaya **tidak bertabrakan** dengan Phase 41–44 (AI Learning Engine, ADR-0013). Kedua jalur boleh berjalan paralel; satu-satunya titik temu adalah `learning_events` (dibaca, tidak diubah).

---

## 1. Tujuan

- Pengguna Plus/Pro bisa membuat dan mengelola **Grup Belajar**; Pro bisa membuat **Ruang Kelas** berisi **Grup Kelas**.
- Konten Titian yang sudah ada (learning path, modul, tryout/assessment, bank soal) bisa **di-attach** ke grup.
- **Liga** bekerja di dalam grup, dengan poin yang **dihitung dari aktivitas belajar nyata**, mendukung: tryout bersama, ujian harian, latihan soal, liga learning path, olimpiade, ujian simulasi, dan ujian beneran (nilai manual).
- Prototipe mock di `titian-web` diganti data server, tanpa `user-me` hardcode.

## 2. Yang WAJIB dipertahankan

- **XP, streak, Poin Liga tidak pernah masuk `mastery.compute` / `frss.apply`** (ADR-0002/0003, guard di STATE.md). Liga hanya **membaca** `learning_events`, `attempts`, `xp_events`, `masteries`.
- `GET /me/league` dan `GET /leaderboard/weekly` **tidak berubah kontraknya**.
- `org_classes` / konsol `/organisasi` (LMS sekolah) **tidak disentuh**.
- Alur pembayaran (`orders`, QRIS stub, wallet 30/70) **dipakai ulang**, tidak dibuat ulang.
- Absensi, sertifikat, dan `class_sessions` tetap berjalan untuk cohort yang ada.
- Data belajar dan skor **tidak pernah dihitung/dipercaya dari klien**.
- Desain Titian: token `primary` emas, `@/components/ui/*`, dark mode, teks Bahasa Indonesia. Istilah UI: **Grup Belajar**, **Grup Kelas**, **Ruang Kelas**.

## 3. Aturan main eksekusi

Sama dengan Phase 39/40 §3: migrasi aditif mulai dari nomor setelah migrasi terakhir (**0073** saat ini), sinkron `domain-model.md` & `api-contract.md`, verifikasi terarah, cek browser dengan `Bun.WebView` (minta izin user sebelum membuat token QA, hapus setelahnya), jangan commit tanpa diminta. Waktu pelaporan dan batas musim **WIB (Asia/Jakarta)**.

Setiap phase berakhir dengan tiket **frontend** untuk potongan yang baru jadi, jadi mock dihapus bertahap, bukan sekaligus di akhir. Nama tabel/kolom eksternal (mis. `attempts`, `assessments`, learning path) **diverifikasi ke skema nyata saat mengerjakan tiket**; tabel di dokumen ini adalah rancangan.

Kuota tier hidup di satu fungsi `group_limits(tier)`; kapasitas anggota di `group_capacity(kind)` (belajar 100, kelas 1000, dikonfirmasi user 2026-09-21). Angka di §Asumsi ADR-0015 §9 bisa berubah tanpa menyentuh tiket lain.

---

# Phase 45 — Fondasi Grup & Entitlement

## P45-001 — Skema grup, anggota, undangan (M)

✅ **SELESAI (2026-09-21).** `migrations/0073_study_groups.sql`. Selisih dari rencana: (1) `study_groups.owner_id` nullable + CHECK `(kind='global') = (owner_id is null)` karena Grup Global tidak dimiliki siapa pun; (2) tambah `join_mode` ('open'|'approval') dan `updated_at`; (3) status anggota punya 5 nilai — `left` (keluar sendiri) dibedakan dari `removed` (dikeluarkan admin) dan `banned` (tidak boleh kembali); (4) `cohort_id` belum punya FK (baru jadi Ruang Kelas di P48), CHECK `kind='kelas' ⇔ cohort_id is not null` sudah menguncinya; (5) kapasitas dijaga CHECK `1..1000`, nilai defaultnya (100/1000) di kode (`subscription::group_capacity`). Grup Global di-seed dengan id tetap `00000000-0000-0000-0000-00000000c0de`. Diterapkan ke dev DB lewat `psql` (bukan `sqlx migrate run` — sqlx-cli menolak karena migrasi 53 pernah dimodifikasi; runner aplikasi mencatatnya saat start).


Migrasi `0073_study_groups.sql`:
- `study_groups(id, kind check in ('belajar','kelas','global'), name, description, avatar_emoji, jenjang, subject, visibility check in ('public','private'), owner_id, cohort_id null, max_members (default 100 untuk `belajar`, 1000 untuk `kelas`/`global`-tak-berlaku), status check in ('active','archived','suspended'), created_at)`. CHECK: `kind='kelas'` ⇔ `cohort_id is not null`.
- `study_group_members(group_id, user_id, role check in ('owner','admin','member'), status check in ('pending','active','removed','banned'), joined_at)`, UNIQUE `(group_id, user_id)`. `owner` selalu tepat satu (partial unique index).
- `study_group_invites(id, group_id, code unique, created_by, expires_at, max_uses, use_count, revoked_at)`. Kode: **acak kriptografis** (`rand`/`getrandom`), 10 karakter tanpa yang ambigu (0/O/1/I).
- Seed **satu** Grup Global (`kind='global'`), keanggotaan implisit (tidak ada baris anggota).

**DoD:** migrasi naik & turun bersih; constraint diuji lewat insert yang sengaja melanggar (pola P9-003).

## P45-002 — Entitlement & kuota grup (S)

✅ **SELESAI (2026-09-21).** `subscription::group_limits(tier)` (satu-satunya tempat angka kuota), `group_capacity(kind)`, `active_tier(pool, user)`; `Entitlements` mendapat blok `groups`, sehingga `GET /me/entitlements` ikut mengembalikannya. Kedaluwarsa langganan = batas gratis. `list_tiers()` menambah baris benefit Plus/Pro. Angka: gratis join 3/buat 0; Plus join 1000/buat 50/liga 3; Pro join 1000/buat 100/liga tak terbatas.


- Perluas `subscription::Entitlements` dengan `group_limits`: `max_groups_joined` (gratis 3 / Plus 1000 / Pro 1000), `max_groups_created` (0 / 50 / 100), kapasitas per jenis grup: `belajar`=100, `kelas`=1000 (bukan per tier), `max_active_leagues_per_group` (Plus 3), dan flag `can_create_classroom`, `can_convert_to_class_group`, `can_use_circuits`, `can_monetize` (semua hanya Pro).
- `GET /subscriptions/me` / endpoint entitlement yang ada ikut mengembalikan blok ini. **Satu fungsi** `group_limits(tier)`; tidak ada angka kuota lain di kode.
- `list_tiers()` menambah baris benefit Plus/Pro (buat grup, ikut banyak grup, kelas dan liga berjenjang untuk Pro).

**DoD:** test per tier (gratis/Plus/Pro/langganan kedaluwarsa); kedaluwarsa = kembali ke batas gratis.

## P45-003 — CRUD grup, join, keluar, kode undangan (L)

✅ **SELESAI (2026-09-21).** `services/study_group.rs`, `handlers/study_group.rs`, `routes/study_group.rs`. Keputusan penting: (1) **race quota**: setiap cek-lalu-insert berjalan dalam satu transaksi dengan `pg_advisory_xact_lock` per pengguna (`sg:create:`/`sg:join:`) + `for update` pada baris grup untuk kapasitas; urutan kunci selalu user → invite → grup supaya tidak deadlock — dibuktikan test balapan 6 pendaftar untuk 1 kursi terakhir; (2) membuat grup juga memakai 1 slot join (pembuat adalah anggota); (3) `explore` hanya grup `public`+`active`, keyset `(created_at, id)` presisi mikrodetik; (4) permintaan `pending` **tidak** memakai slot join maupun kapasitas sampai disetujui; (5) kode undangan yang dikenal tapi tidak layak pakai dibedakan (`invite_expired`/`invite_revoked`/`invite_exhausted`) sedangkan kode tak dikenal `404 invite_not_found` — ini tidak membuka oracle karena pembedaan hanya berlaku untuk kode yang sudah dipegang penanya; (6) join ulang lewat kode tidak menghabiskan 1 pemakaian; (7) `join-by-code` dibatasi 10/menit/pengguna (Redis, `rate_limit::check`); (8) Grup Kelas tidak bisa di-join langsung (`422 class_group_join_unavailable`) sampai P48. Kueri memakai `sqlx::query_as` runtime + `FromRow` (seperti `canon_path.rs`), bukan makro `query!`, jadi **tidak perlu regenerasi `.sqlx`**.


- `POST /groups` (Plus/Pro; cek `max_groups_created`), `GET /groups/{id}`, `PATCH /groups/{id}`, `DELETE`/arsip (owner).
- `GET /me/groups` (grup yang diikuti, termasuk Grup Global sebagai baris sintetis).
- `GET /groups/explore` (publik saja, keyset, filter jenjang/mapel).
- `POST /groups/{id}/join` (publik) dan `POST /groups/join-by-code {code}`. Cek: kuota join (gratis 3), `max_members`, tidak sedang `banned`. Kode tidak dikenal → **404**, bukan membuat grup baru (perilaku prototipe dihapus).
- `POST/DELETE /groups/{id}/invites`: buat/cabut kode, atur kedaluwarsa dan `max_uses`. Join lewat kode dibatasi laju (Redis, pola P39-005).
- `POST /groups/{id}/leave`. Owner tidak boleh keluar sebelum mengalihkan kepemilikan.

**DoD:** test kuota (tepat di batas, +1 ditolak), kode kedaluwarsa/dicabut/habis, join ganda idempoten, `explore` tidak membocorkan grup privat.

## P45-004 — Manajemen anggota & log audit (M)

✅ **SELESAI (2026-09-21).** Selisih dari rencana: **tidak ada `Resource::StudyGroup` di `permissions.rs`** — RBAC di file itu berbasis peran organisasi (`student`/`teacher`/...), sedangkan hak di grup berbasis peran **keanggotaan** (owner/admin/member) dan tier langganan; menambah Resource di sana tidak menegakkan apa pun. Izin ditegakkan di `study_group.rs` (`require_manager`/`require_owner`/`check_can_moderate`). Aksi tercatat di `admin_audit_log` dengan `target_type='study_group'`: `member_removed`, `member_banned`, `member_unbanned`, `member_role_changed`, `join_approved`, `join_rejected`, `ownership_transferred`, `invite_revoked`, `archived`. Transfer kepemilikan: pemilik lama didemosi dulu (indeks unik parsial 1 owner), pemilik baru harus bisa membuat grup (kuota buat berlaku baginya).


- `GET /groups/{id}/members` (paginasi), `PATCH .../members/{uid}` (ubah role: owner→admin/member; admin tidak boleh menyentuh owner atau admin lain), `DELETE` (keluarkan), `POST .../ban`, `POST .../transfer-ownership`.
- Persetujuan join untuk grup dengan `join_mode='approval'` (status `pending`): `POST .../members/{uid}/approve|reject`.
- Semua aksi admin memanggil `admin_audit::record` (tabel/pola P40-001, `resource='study_group'`).
- Izin: `Resource::StudyGroup` di `permissions.rs`, dicek per-grup lewat peran anggota (bukan hanya peran global).

**DoD:** matriks izin diuji (member/admin/owner/non-anggota/`platform_admin`), aksi tercatat di audit log.

## P45-005 — Frontend: daftar, buat, gabung, kelola (L)

✅ **SELESAI (2026-09-21), diverifikasi penuh lewat `Bun.WebView`** (izin user diberikan; server 8090 di-restart dengan binary baru; 3 user QA + refresh token dibuat lalu **dihapus semua** — users, credits, user_presence, subscriptions, roles, org, grup, audit; dev DB bersih). 11/11 pengecekan lulus: Plus melihat kuota `0 / 50` dan Grup Global di urutan pertama → membuat grup lewat dialog → mendarat di halaman grup dengan lencana Pemilik dan `1 / 100` → kode undangan muncul di Pengaturan; user gratis melihat `/ 3` + ajakan upgrade → kode salah menampilkan galat server asli → bergabung dengan kode huruf kecil → melihat grup privat, tab Anggota tanpa tab Pengaturan → dialog buat grup berupa ajakan upgrade, bukan formulir; pemilik lalu melihat anggota baru dengan aksi Jadikan admin/pemilik, Keluarkan, Blokir. **2 temuan harness (bukan bug aplikasi)**: (1) refresh token berotasi, jadi menanam ulang token mentah di tiap navigasi (perilaku `login()` di `webview.ts`) memutus sesi setelah muat pertama — skrip QA mencabut init-script setelah sesi terbentuk; (2) dua Chrome headless berbagi localStorage yang sama, sehingga login user kedua menimpa sesi user pertama — pemilik harus login ulang dengan token baru sebelum pengecekan berikutnya. `lib/api-client.ts` (`groupApi` + tipe), `hooks/use-groups.ts`, `lib/group-errors.ts`, `/grup` dan `/grup/[groupId]` ditulis ulang di atas API; `create-group-dialog.tsx` dan `join-group-dialog.tsx` diganti versi API (pengguna gratis melihat ajakan upgrade, bukan formulir); panel anggota & pengaturan baru (`group-members-panel.tsx`, `group-settings-panel.tsx`). **Selisih dari rencana**: prototipe untuk target/jadwal/liga/kelas **tidak dipertahankan di halaman detail** — tab-tab itu sekarang kartu "Segera hadir" (bukan data palsu), karena aksinya memanggil store mock yang tidak mengenal grup server. **Prototipe LENGKAP diarsipkan**: `titian-web/src/app/(app)/grup/_prototype/{list,detail}-page.tsx` (folder `_` = tidak dirute) + tar `/home/john/backups/titian-group-prototype-2026-09-21.tar.gz`. Alasan arsip: berkas-berkas itu **belum pernah di-commit** (untracked di repo `titian-web`), jadi tidak ada di git. `store/group-store.ts` + `lib/group-mock-data.ts` + `components/group/*` (dialog/tab mock) tetap ada untuk dipakai P46/P47/P48 dan `/kelas` (yang masih memakai mock sampai P48). `tsc --noEmit` bersih; `eslint` 0 error.


- Hook `use-groups.ts` (react-query): `useMyGroups`, `useExploreGroups`, `useGroup`, `useCreateGroup`, `useJoinGroup`, `useJoinByCode`, dst. `api-client.ts` mendapat `groupApi`.
- Halaman `/grup` dan `/grup/[groupId]` membaca API; **`user-me`/`Kamu (John)` dihapus dari alur ini** (pakai `useAuth().user.id`). Dialog buat/gabung memakai error nyata dari server (kuota, kode tidak valid).
- Tampilan kuota ("2 / 3 grup" untuk gratis) dan CTA upgrade ke `/langganan` saat mentok.
- Copy UI: **Grup Belajar**.
- Bagian yang belum punya backend (target, konten, liga) **tetap memakai mock** sementara, di-isolasi di satu modul yang jelas ditandai `// mock — dihapus di P46/P47`.

**DoD:** verifikasi `Bun.WebView`: buat grup, gabung lewat kode di sesi lain, mentok kuota gratis, keluarkan anggota; `tsc` + `eslint` bersih.

## P45-006 — Test suite & checkpoint (S)

✅ **Test lulus (2026-09-21):** `tests/integration/study_group_test.rs` **25/25** + 4 unit test di `study_group.rs`; `admin_audit_test` dan `gamification_test` tetap hijau (entitlements berubah bentuk, tidak ada regresi). Dijalankan dengan tambalan SEMENTARA di `0063` (dikembalikan otomatis, sha256 diverifikasi utuh). 2 kegagalan di `economy_test` (`subscribe_*`) **bukan dari fase ini**: test memanggil `POST /subscriptions/subscribe` yang sudah tidak ada (langganan kini lewat order/QRIS) → 404; test basi, perlu diperbarui terpisah. Lihat catatan verifikasi di STATE.md tentang **migrasi 0063/0064 yang merusak seluruh suite integrasi pada DB kosong**.


Test integrasi end-to-end fase 45; route-coverage audit; catat di STATE.md.

---

# Phase 46 — Konten & Target Grup

## P46-001 — Attach konten (M)

✅ **Backend SELESAI (2026-09-21).** `migrations/0074_group_content_targets.sql`, `services/study_group_content.rs`. Selisih dari rencana: (1) **`question_bank` DITUNDA** dari `kind` — bank soal adalah objek penulisan (soalnya membawa kunci jawaban) dan siswa hanya mengakses soal lewat assessment/item; menempelkannya butuh desain "soal yang disajikan", yang memang milik format liga `latihan` (P47). CHECK DB hanya mengizinkan `learning_path|module_item|assessment`; (2) `learning_path` = `modules` terbit + seluruh subtree-nya (tabel `modules` adalah pohon; tidak ada tabel `learning_paths`); (3) ditambah `GET /groups/attachable/assessments?q=` karena tidak ada endpoint daftar assessment untuk pemilih UI; (4) materi yang di-unpublish tetap terdaftar dengan `available:false`; (5) `PATCH` membedakan `due_at` absen vs `null` (hapus tenggat) lewat `Option<Option<_>>`; (6) batas 50 materi/grup, dijaga `for update` pada baris grup.


Migrasi `group_content(id, group_id, kind in ('learning_path','module_item','assessment','question_bank'), ref_id, position, due_at, added_by, created_at)`, UNIQUE `(group_id, kind, ref_id)`.
- `POST/GET/PATCH/DELETE /groups/{id}/content` (owner/admin).
- Validasi `ref_id` ada **dan boleh dilihat** pembuat (draft/privat milik orang lain → 404 "jangan bocorkan keberadaan").
- Anggota melihat konten grup; **entitlement konten tetap per anggota** (grup tidak membuka paywall). Respons menandai `locked` bila anggota tidak berhak.

## P46-002 — Progres anggota atas konten (M)

✅ **SELESAI (2026-09-21).** `GET /groups/{id}/progress`. Tanpa tabel progres baru. **Keputusan privasi**: anggota biasa hanya menerima progres dirinya + agregat (`members` tidak dikirim sama sekali, bukan disembunyikan di UI); owner/admin menerima tabel per anggota. Selisih dari rencana: progres dibaca dari `module_item_progress`/`attempts` (data inti, bukan event telemetri), jadi **tidak ada** status "tidak dilacak" akibat persetujuan `learning_analytics` — persetujuan itu hanya menyangkut event klien opsional, dan tidak ikut dipakai di sini. Jumlah selesai dipotong ke `total_units` (jalur yang menyusut tidak melaporkan >100%).


- `GET /groups/{id}/progress` (owner/admin: semua anggota; member: dirinya + agregat).
- Dihitung on-read dari `learning_events`/`item_progress`/`attempts`; **tanpa tabel progres baru**. Anggota tanpa persetujuan event (P39-007) ditandai "tidak dilacak", bukan nol.

## P46-003 — Target grup (M)

✅ **SELESAI (2026-09-21).** Metrik: `items_completed`, `questions_answered`, `activity_days` (hari kalender **WIB** berbeda). `study_minutes` dari rencana **dibuang** — belum ada sumber durasi yang andal di server. **`reward_xp` DITUNDA ke P47** — hadiah XP harus tunduk pada batas bonus mingguan yang sama dengan hadiah liga (ADR-0015 §9 no. 4, angkanya belum dikonfirmasi user), jadi dibangun sekali di sana. Kolom `reward_xp` sengaja tidak dibuat sekarang.


- Migrasi `group_targets(id, group_id, title, metric in ('items_completed','questions_answered','study_minutes','activity_days'), target_value, per_member bool, period_start, period_end, reward_xp)`.
- Progres dihitung on-read dalam periode target. `reward_xp` (opsional) diberikan sekali per pengguna via `xp_events` `reference = "gtarget:{id}:{user}"`, tunduk pada batas bonus mingguan (ADR-0015 §3).
- Target hanya bisa dibuat owner/admin.

## P46-004 — Frontend: tab Konten & Target, "tambah dari Titian" (L)

✅ **SELESAI (2026-09-21), diverifikasi penuh lewat `Bun.WebView`** (9/9; izin user diberikan; data QA — user, token, grup, modul/butir/tryout uji — dihapus semua). Alur: pemilik membuka tab Materi kosong → "Tambah dari Titian" → menjelajah perpustakaan dan memilih jalur → mencari dan memilih tryout → keduanya muncul dengan progres pemilik `0 / 3` (jalur = 3 butir terbit di modul + sub-modul; butir draf tidak dihitung) → membuat target "Tuntaskan 3 materi" yang langsung menampilkan `1 / 3 materi` dari penyelesaian anggota; anggota melihat progresnya sendiri `1 / 3` tanpa kontrol tambah/hapus maupun tabel per-anggota; pemilik membuka "Lihat progres tiap anggota" dan melihat daftar anggota. Tab **Materi** dan **Target** di `/grup/[groupId]` (`group-content-panel.tsx`, `group-targets-panel.tsx`), pemilih "Tambah dari Titian" (jelajah folder→modul terbit, dan pencarian tryout). Mock target/learningPath TIDAK lagi ada di halaman detail baru (sudah dihapus sejak P45). `tsc` bersih.


- Picker konten dari katalog/learning path/tryout/bank soal yang sudah ada.
- Tab Konten dan Target di `/grup/[groupId]` membaca API; mock target/learningPath dihapus.

## P46-005 — Test & checkpoint (S)

✅ **SELESAI (2026-09-21).** `tests/integration/study_group_content_test.rs` **17 test**: hanya owner/admin yang boleh attach; draf/tak-ada/jenis-salah semuanya `404 content_not_found`; urutan & posisi; materi yang di-unpublish → `available:false` tanpa merusak progres; batas 50 materi & 20 target aktif (target yang sudah selesai tidak dihitung); set/hapus tenggat lewat `null`; jejak audit; Grup Global menolak materi/target; progres jalur = butir terbit di seluruh subtree, hanya anggota aktif (bukan pihak luar, bukan yang keluar), butir draf tidak menggelembungkan; anggota tidak menerima tabel per-anggota; assessment hanya menghitung attempt `submitted|evaluated` non-preview + skor terbaik; target grup menjumlah hanya dalam periode; target per-anggota; `activity_days` menghitung hari berbeda bukan jumlah event; status upcoming/active/finished; validasi target; pemilih tryout (LIKE di-escape). Total bersama P45: **42/42** (+5 unit test) — dijalankan dengan tambalan sementara `0063` yang dikembalikan (sha256 terverifikasi).

---

# Phase 47 — Liga, Musim & Grup Global

## P47-001 — Skema liga & musim (M)

✅ **SELESAI (2026-09-21).** `migrations/0075_group_leagues.sql`. Selisih dari rencana: (1) `scoring_rule jsonb` menjadi kolom `scoring text` ber-CHECK + kombinasi format↔scoring divalidasi di service (`allowed_scoring`) — lebih ketat dari jsonb bebas; (2) `xp_policy` hanya `normal|none` (`bonus_only` dibuang: tak ada bedanya dengan `normal` di rancangan ini), dan CHECK DB memaksa `format='manual' ⇒ xp_policy='none'`; (3) `integrity` disimpan (`casual|proctored`) tetapi service menolak `proctored` (`422 integrity_not_supported_yet`) — menyimpan tanpa menegakkan akan menyesatkan; (4) `league_entries` hanya berisi **tamu** dan hasil beku; anggota grup implisit peserta semua liga grupnya (kelas tak perlu menekan "gabung" satu-satu); (5) ditambah `share_code` unik per liga dan `guest_cap`; (6) `promotion_slots`/`relegation_slots`/sirkuit **tidak dibuat** — milik P49.


Migrasi:
- `group_leagues(id, group_id, circuit_id null, tier null, title, description, format in ('tryout','ujian','latihan','learning_path','olimpiade','aktivitas','manual'), source jsonb, scoring_rule jsonb, integrity in ('casual','proctored'), xp_policy in ('normal','bonus_only','none'), cadence in ('one_off','weekly','monthly','custom'), season_days null, allow_guests bool, guest_cap null, promotion_slots default 0, relegation_slots default 0, status, created_by)`.
- `league_seasons(id, league_id, number, starts_at, ends_at, status in ('upcoming','active','closing','closed'), closed_at)`, UNIQUE `(league_id, number)`.
- `league_entries(id, season_id, user_id, role in ('member','guest'), joined_at, final_score null, final_rank null, zone null)`, UNIQUE `(season_id, user_id)`. **Skor sementara tidak disimpan**; `final_*` diisi saat musim ditutup.
- `league_manual_scores(season_id, user_id, score, entered_by, note, updated_at)`.
- `source` dan `scoring_rule` divalidasi di service per `format` (bukan jsonb bebas). `format='manual'` mewajibkan `xp_policy='none'`.

## P47-002 — Mesin skor `LeagueScorer` (L) — tiket terberat

✅ **SELESAI (2026-09-21)** sebagai `services/group_league.rs::score()` (satu `match` per `scoring`, bukan trait — tak ada implementasi lain yang perlu bertukar; ubah bila P49 membutuhkan). Semua pembacaan murni. Keputusan: (1) `learning_path` = jumlah butir terbit yang **diselesaikan dalam jendela musim** (bukan delta mastery — mastery tidak disentuh sama sekali, sesuai guard STATE.md); (2) `latihan` membaca `learning_events` `question_answered` (bukan bank soal, yang ditunda); `accuracy` butuh ≥10 jawaban — di bawah itu dianggap **belum ikut**, bukan "ikut dengan 0" (bug ini tertangkap oleh test, bukan oleh review); (3) `aktivitas` = COUNT aksi belajar server (`question_answered`, `module_item_completed`, `quiz_attempt_submitted`, `question_graded`, `exam_session_finished`) — bukan SUM XP; test membuktikan grant XP 1.000.000 tak menggeser klasemen; (4) tie-break total: poin ↓ → yang mencapai lebih dulu → `user_id`. Bagian "sumber skor bersama dengan `league.rs`" milik P47-005 (ditunda).


Trait `LeagueScorer { fn scores(season, participants) -> Vec<(user_id, points, tie_break)> }` dengan satu implementasi per `format`, semuanya **read-only**:
- `tryout` / `ujian`: dari `attempts`/`exam_sessions` assessment yang di-attach, dalam `[starts_at, ends_at]`; `best_attempt` / `first_attempt`.
- `latihan`: benar/akurasi berbobot atas soal bank yang di-attach.
- `learning_path`: kemajuan + delta mastery **baca-saja** pada concept path itu (memakai baseline P8-003, tidak menulis).
- `olimpiade`: jumlah beberapa babak, tie-break waktu.
- `aktivitas`: COUNT event dalam jendela (bukan SUM XP), memakai persetujuan P39-007.
- `manual`: dari `league_manual_scores`.
- Tie-break seragam: poin ↓, waktu pencapaian ↑, `user_id`.

**DoD:** test per format, termasuk: satu event XP raksasa **tidak** mengubah peringkat `aktivitas`; `first_attempt` mengabaikan percobaan ulang; attempt di luar jendela musim tidak dihitung; peserta tanpa data = 0, bukan error.

## P47-003 — API liga: buat, ikut, papan peringkat (L)

✅ **SELESAI (2026-09-21).** Endpoint di `api-contract.md` §"Liga grup (P47)". Keputusan: (1) papan peringkat dihitung on-read; `me` diambil dari hasil penuh yang sama; (2) tamu bergabung lewat `POST /leagues/join-by-code` (dibatasi laju), tidak pernah menjadi anggota grup, dan hanya bisa membaca **liga itu** (bukan konten grup) — diuji; (3) liga yang tidak menerima tamu **tak dapat dibedakan** dari kode tak dikenal (404); (4) anggota yang di-ban tidak bisa masuk sebagai tamu; (5) kuota liga aktif memakai paket **pemilik grup** (Plus 3, Pro tak terbatas); (6) semua nilai manual tercatat di audit log dan hanya bisa diisi untuk peserta.


- `POST /groups/{id}/leagues` (cek `max_active_leagues_per_group`, `can_use_circuits` untuk sirkuit), `GET /groups/{id}/leagues`, `GET /leagues/{id}` (musim aktif + papan peringkat), `POST /leagues/{id}/join` (anggota; tamu bila `allow_guests`, dibatasi `guest_cap`).
- Papan peringkat dihitung on-read lewat `LeagueScorer`; `me` dihitung dari hasil penuh yang sama (pola P8-005).
- `PUT /leagues/{id}/manual-scores` (owner/admin; tercatat audit).
- Kode bagikan liga (`share code`) dibuat kripto-acak; tautan publik hanya untuk liga `allow_guests`.

## P47-004 — Penutupan musim (job) (L)

✅ **SELESAI (2026-09-21).** `close_season`/`close_due_seasons` + job `league_season_close` (didaftarkan di `job_queue::HANDLERS` dan `SCHEDULED_JOBS`, tiap ≤5 menit). Satu transaksi dengan `for update skip locked` (dua worker tak pernah menutup musim yang sama); bonus XP idempoten lewat `reference` UNIQUE dan **dicek sebelum batas mingguan dihitung**, sehingga percobaan ulang setelah crash tak pernah membayar dua kali (diuji dengan mensimulasikan crash: status musim dikembalikan ke `active` lalu ditutup lagi → tetap 3 baris bonus). Bonus: hanya **anggota** (tamu tidak pernah dibayar, dan tidak menggeser anggota dari urutan bonus), top 3 = 150/100/50, hanya bila ≥3 orang ikut, tak lebih dari 500 XP/7 hari/orang. Liga berulang membuka musim berikutnya berurutan (`starts_at` = `ends_at` musim lalu) dan membawa tamu; sekali jalan → `finished`; liga yang diarsipkan menutup musimnya tetapi tidak bergulir. **`titian-worker` harus berjalan di produksi** — tanpa worker, musim tetap `ended` dan klasemen tetap live (tidak salah, hanya belum beku/berbonus). Konstanta bonus (`BONUS_BY_RANK`, `WEEKLY_BONUS_CAP`, `MIN_PARTICIPANTS_FOR_BONUS`) ada di satu tempat; angka 500 masih asumsi ADR-0015 §9 no. 4.


- Job terjadwal `league_season_close` di `job_queue` (`SCHEDULED_JOBS`), tiap jam: klaim musim `active` yang `ends_at <= now()` lewat `UPDATE ... SET status='closing' WHERE status='active'` (idempoten, aman untuk banyak worker).
- Bekukan `final_score`/`final_rank`, tulis bonus XP (`league:{season}:{user}`, batas mingguan), lalu:
  - `cadence='one_off'` → `closed`, selesai.
  - berulang → buat musim berikutnya (nomor +1, poin dari nol).
- Crash di tengah → job berikutnya melanjutkan tanpa dobel (klaim status + `reference` UNIQUE).

**DoD:** test idempotensi (job jalan dua kali), crash simulasi, musim tanpa peserta, batas WIB.

## P47-005 — Grup Global & liga global (M)

✅ **SELESAI (2026-09-21).** Liga Global = satu liga sintetis milik Grup Global (`GLOBAL_LEAGUE_ID = 00000000-0000-0000-0000-00000000c0df`): **tanpa baris `group_leagues`, tanpa musim, tanpa job penutupan, tanpa bonus XP** — papan bergulir 7 hari terakhir yang dihitung saat dibaca, sehingga tak ada yang perlu dibekukan atau dibayar. `GET /groups/{global}/leagues` mengembalikan liga itu; `GET /leagues/{global_league}` mengembalikan papan (50 teratas + baris pemanggil selalu ikut, walau di luar 50). Peserta = semua orang dengan ≥1 XP event dalam 7 hari (dibatasi 5.000 paling aktif yang dinilai — batas kerja, bukan batas pengguna; orang di bawah potongan itu tak tampil). **Satu rumus, satu implementasi**: `league::composite_score(streak, mastery, aktivitas)` diekstrak dan dipakai `get_league` (`/me/league`) DAN papan global; test membuktikan `points` di papan sama persis dengan `score` di `/me/league` untuk orang yang sama, dan bahwa satu grant XP 1.000.000 tidak mengalahkan orang yang lebih aktif. Kontrak `GET /me/league` **tidak berubah**. `GET /leaderboard/weekly` tetap peringkat XP (kontraknya memang begitu sejak P8-005) — **bukan** dibuat memakai rumus gabungan, karena itu mengubah arti papan yang sudah dipakai widget beranda; ini selisih sadar dari ADR-0015 §4. **Privasi (ADR-0015 §10)**: consent kind baru `global_leaderboard_alias` — `granted=true` berarti tampil sebagai "Pelajar #A1B2" bagi semua orang kecuali diri sendiri, **default tetap nama asli** (perilaku papan selama ini tak berubah); berlaku di papan global DAN di `/leaderboard/weekly` (opt-out tak bermakna bila papan lama tetap mencetak nama). Memberi alias **mengurangi** data yang dibagikan, sehingga dikecualikan dari aturan konfirmasi wali untuk anak SD/SMP (aturan itu ada untuk mencegah anak di-opt-in ke pengumpulan data). Frontend: tab "Liga Global" di halaman Grup Global (`/grup/00000000-…c0de`), tautan "Lihat klasemen Liga Global" di kartu Liga (Progres), toggle "Tampilkan namaku di Liga Global" di Profil › Pengaturan (mati = alias). Test: 6 di `group_league_test.rs`. **Dua bug tertangkap saat verifikasi (bukan saat menulis):** (1) tabel `user_data_consents` punya CHECK yang hanya mengizinkan dua kind, sehingga consent baru ditolak DB (500) — test alias gagal; diperbaiki migrasi `0077_global_leaderboard_alias_consent.sql`; (2) toggle di Profil masih mengirim nama consent versi awal (`global_leaderboard_name`, semantik terbalik dari backend) — tertangkap saat QA browser (galat "consent kind … is not recognised" tampil di UI); kini toggle = negasi dari consent alias dan dikunci sampai daftar consent termuat. **Browser diverifikasi** (izin user; data QA dihapus): mengaktifkan toggle menyimpan consent alias → tautan "Lihat klasemen Liga Global" di Progres › Liga → halaman Grup Global hanya berisi papan (tanpa tab Anggota/Pengaturan) → penjelasan "bukan XP / 7 hari terakhir" → urutan mengikuti aktivitas (6 > 4 > 2) → pengguna lain melihat yang beralias sebagai "Pelajar #EE42" sementara yang lain tetap bernama, dan pemilik alias tetap melihat namanya sendiri. Papan menampilkan pengguna dev nyata juga (data dev asli), sehingga peringkat tester bukan #1.


- Liga `aktivitas` mingguan milik Grup Global memakai rumus `services/league.rs` (satu kode, bukan salinan).
- `GET /me/league` & `GET /leaderboard/weekly` tetap; internalnya memakai kode bersama. Opt-out alias di papan global.

## P47-006 — Frontend: liga nyata (L)

✅ **SELESAI (2026-09-21), diverifikasi lewat `Bun.WebView`** (izin user diberikan; 3 user QA + data uji dihapus semua): tab **Liga** (daftar, pembuat liga dengan 7 jenis + pemilih tryout/modul + jadwal + opsi tamu/XP, klasemen dengan peringkat/poin/tanda "kamu"/lencana Tamu, pemilih musim, kode tamu bisa disalin, arsipkan, editor nilai manual), dialog **Ikut Liga dengan Kode** di `/grup`, dan halaman tamu `/grup/liga/[leagueId]`. Terbukti di browser: pemilik membuat liga tryout (tamu diizinkan) → klasemen menaruh anggota 90 di atas pemilik 80 dengan "Kamu peringkat #2" dan kode tamu; membuat liga Ujian Resmi (opsi bonus XP hilang) → mengisi nilai 88 dan 70 → klasemen mengikuti; tamu memasukkan kode salah (galat server asli) lalu kode benar (huruf kecil) → mendarat di halaman liga peringkat #1 dengan lencana Tamu tanpa kode tamu/arsipkan; anggota melihat kedua liga tanpa tombol buat dan peringkat #2 di belakang tamu. 2 pengecekan skrip "gagal" hanyalah artefak urutan `innerText` (nama pengguna di sidebar); tangkapan layar membuktikan urutan benar. **Tidak diverifikasi di browser: tampilan musim yang sudah beku dan bonus XP** (butuh menjalankan worker terhadap DB dev, yang juga akan memproses job konten AI yang mungkin menunggu — dihindari); keduanya diverifikasi di test backend. `tsc` bersih, `eslint` 0 error (2 pelanggaran `react-hooks/purity` — `Date.now()` saat render — diperbaiki dengan initializer lazy, termasuk di panel Target P46).


- Ganti `group-leagues-section`, `join-league-modal`, `share-league-dialog`, `create-group-league-dialog` ke API. Form buat liga memilih **jenis** (tryout, ujian, latihan, learning path, olimpiade, aktivitas, ujian beneran) yang otomatis menyesuaikan field sumber & aturan skor.
- Hapus `weekly_xp` mentah, `Kamu`-string matching, skor hardcode.
- `/progres` tab Liga tetap; menampilkan Grup Global.

## P47-007 — Test & checkpoint (S)

✅ **SELESAI (2026-09-21).** `tests/integration/group_league_test.rs` **22 test** + 4 unit test (`rank`, `bonus_for`, `allowed_scoring`). Cakupan: validasi pembuatan (format/scoring/xp/integrity/cadence/period/source/guest_cap, hanya manager), kuota Plus 3 vs Pro tak terbatas, arsip membebaskan slot; tiap format (tie-break tryout, ujian hanya percobaan pertama, olimpiade jumlah terbaik per babak, jalur dalam jendela, latihan benar/akurasi dengan sampel minimum, aktivitas tak bisa dibeli XP); nilai manual (manager saja, hanya peserta, 0–1000, diaudit); tamu (kode huruf kecil, batas tamu, idempoten, tak dapat membaca grup, banned tak bisa menyelinap, liga tertutup = 404); musim (upcoming); penutupan (klasemen beku & bonus 150/100/50 tepat sekali, buku besar = total cache, retry setelah crash tak membayar dua kali, batas mingguan 500, tanpa bonus bila <3 peserta atau `xp_policy=none`, tamu tak dibayar dan tak menggeser anggota, liga berulang membuka musim berikutnya berurutan & membawa tamu & musim lama tetap beku, liga terarsip tak bergulir); privasi (liga grup privat 404 bagi orang luar). Total bersama P45–P46: **64/64**, dijalankan dengan tambalan sementara `0063` yang dikembalikan (sha256 terverifikasi).


E2E: buat liga tryout → 3 pengguna mengerjakan assessment → papan peringkat benar → tutup musim → `final_rank` dan bonus XP tepat satu kali.

---

# Phase 48 — Ruang Kelas & Grup Kelas (Pro)

## P48-001 — Skema Ruang Kelas (S)

✅ **SELESAI (2026-09-21).** `migrations/0076_classrooms.sql`. **Selisih penting dari ADR-0015 §5: `cohorts.product_id` TETAP `NOT NULL`.** Alasan: sekitar 20 titik (`can_manage_cohorts`, `find_product_for_cohort_id`, kapasitas pendaftaran, sesi, absensi, sertifikat, tugas, gradebook) memberi otorisasi lewat produk kohor; membuatnya nullable berarti menyentuh semuanya. Sebagai gantinya **setiap Ruang Kelas mendapat produk pendukung tersembunyi** (`learning_products`: draft, harga 0, milik pengajar). Hasilnya semua layanan kohor lama bekerja tanpa diubah, dan produk itulah yang akan diberi harga di P49. Kolom baru: `cohorts.owner_id` (nullable — kohor marketplace lama tak berpemilik), `description`, `status`; `study_groups.cohort_id` mendapat FK (`on delete restrict`); `class_sessions.group_id` nullable.


Migrasi aditif atas `cohorts`: `product_id` → **nullable**, tambah `owner_id`, `description`, `status`. `class_sessions.group_id` nullable (FK `study_groups`). Backfill dev DB: cohort lama tanpa `owner_id` diisi dari tutor produknya (atau dihapus — aplikasi belum live).

## P48-002 — API Ruang Kelas (M)

✅ **SELESAI (2026-09-21).** `services/classroom.rs`. Pro saja (`403 classroom_requires_pro`); pengajar otomatis diberi profil tutor + role `teacher` (pola lazy-provisioning `create_product`). Terlihat oleh pemilik, siswa terdaftar, dan platform_admin — selain itu 404. Nama Ruang Kelas diikuti judul produk pendukungnya. Batas 50 Ruang Kelas/pengajar (batas kewajaran, bukan batas paket). Arsip menghentikan siswa/grup baru tetapi tidak menghapus apa pun. Alias `/cohorts` lama tetap; kontrak baru di `api-contract.md`.


- `POST /classrooms` (Pro), `GET /me/classrooms` (dimiliki & diikuti), `GET/PATCH /classrooms/{id}`, arsip.
- Memakai `cohort.rs`/`enrollment.rs` yang ada; hanya lapisan izin & bentuk respons baru.
- Kontrak `api-contract.md`: section "Ruang Kelas" (alias `/cohorts` dipertahankan bila FE lama masih memanggilnya).

## P48-003 — Grup Kelas: buat di dalam & convert (L)

✅ **SELESAI (2026-09-21).** (1) `create_group_of_kind` dipakai bersama Grup Belajar dan Grup Kelas (kuota buat tetap berlaku); (2) **bergabung ke Grup Kelas = mendaftar di Ruang Kelas** dalam transaksi yang sama (`ensure_enrollment`: `active` bila gratis, `pending` bila berbayar; idempoten; pendaftaran yang dibatalkan dihidupkan lagi); permintaan `pending` baru didaftarkan saat disetujui; (3) **convert tidak mengeluarkan siapa pun** dan tidak menghapus liga/target/materi yang sudah ada — diuji; pemilik grup tidak didaftarkan sebagai siswa; (4) unlink ditolak (`group_has_class_records`) bila sudah ada sesi (yang membawa absensi & sertifikat); kapasitas kembali 100 tetapi tidak di bawah jumlah anggota; (5) keluar dari grup tidak membatalkan pendaftaran.


- `POST /classrooms/{id}/groups` membuat Grup Kelas baru.
- `POST /groups/{id}/convert {classroom_id | new_classroom}` (Pro, owner): set `kind='kelas'`, `cohort_id`; anggota **tidak dikeluarkan**; buat `enrollments` (status `active` bila Ruang Kelas gratis, `pending` bila berbayar; ADR-0015 §7).
- `POST /groups/{id}/unlink`: hanya bila belum ada absensi/sertifikat; jika ada → arsip.
- Join Grup Kelas otomatis membuat enrollment.

**DoD:** test convert ke ruang gratis & berbayar, anggota lama tidak hilang, unlink diblokir bila ada absensi.

## P48-004 — Sesi, absensi, sertifikat per Grup Kelas (M)

✅ **SELESAI (2026-09-21).** `POST /cohorts/{id}/class-sessions` menerima `group_id` opsional (harus grup aktif milik Ruang Kelas itu). Roster verifikasi kehadiran sesi berbasis grup = anggota grup ∩ terdaftar (`restrict_roster_to_group`, dipakai di sinkronisasi dan laporan); sesi tanpa grup = seluruh kelas. `GET /groups/{id}/sessions` (anggota grup itu saja) dan `GET /groups/{id}/class` (owner/admin: roster + status pendaftaran + jumlah hadir + kode sertifikat). Sertifikat tetap per pendaftaran lewat mekanisme lama. **Bug ditemukan lewat browser (bukan test):** absensi manual (endpoint per-tanggal lama) tidak menyimpan `class_session_id`, sehingga jumlah "hadir" di ikhtisar tetap 0; query kini menghitung sesi sebagai hadir bila `class_session_id` **atau** tanggal cocok, satu kali per sesi — test diperbarui (catatan verifikasi + manual sama-sama dihitung).


- `class_sessions.group_id`: roster absensi = anggota grup ∩ enrollment aktif. Verifikasi Google Meet (Phase 28) tetap dipakai apa adanya.
- Sertifikat: mekanisme per enrollment tidak berubah; hanya tombol terbit tersedia dari konteks Grup Kelas.
- Fitur ini **digerbang** `can_convert_to_class_group`/Pro di backend.

## P48-005 — Downgrade & langganan habis (S)

✅ **SELESAI (2026-09-21).** `assert_class_features_active`: bila pemilik bukan Pro, sesi baru, sertifikat baru, Grup Kelas baru, dan convert ditolak `403 classroom_frozen`. Semua tetap terbaca (Ruang Kelas, grup, sesi, ikhtisar), pendaftaran tidak berubah, dan berlangganan lagi membuka bekuan — diuji. Kohor marketplace tanpa pemilik tidak terpengaruh.


Grup Kelas & Ruang Kelas milik pengguna yang turun tier menjadi **beku**: baca-saja, tidak bisa buat sesi/absensi/sertifikat/liga baru; tidak ada data dihapus. Test kedaluwarsa langganan.

## P48-006 — Frontend: Ruang Kelas & Grup Kelas (L)

✅ **SELESAI (2026-09-21), diverifikasi penuh lewat `Bun.WebView`** (izin user diberikan; user/data QA dihapus semua): halaman baru `/ruang-kelas` (daftar + buat) dan `/ruang-kelas/[id]` (Grup Kelas di dalamnya + buat Grup Kelas + arsip), tab **Kelas** di Grup Kelas (jadwalkan sesi, daftar sesi dengan tautan, absensi manual, roster dengan status pendaftaran/hadir, terbitkan sertifikat), bagian **Jadikan Grup Kelas / Kembalikan** di Pengaturan, dan tombol Ruang Kelas di hub `/grup`. 14/14 pengecekan: pengajar Pro membuat Ruang Kelas → Kelas A (badge Grup Kelas, kapasitas 1000, tab Kelas) → menjadwalkan sesi (tautan Ikuti) → mengonversi grup lama (anggota lama otomatis terdaftar Aktif) → roster "0 / 1 hadir" → absensi manual → "1 / 1 hadir" → sertifikat terbit (kode tampil, status Selesai, tercatat di DB) → siswa baru bergabung Kelas A (terdaftar Aktif, melihat sesi + tautan tanpa roster/tombol jadwal, Ruang Kelas muncul di "Kelas yang saya ikuti") → roster pengajar menampilkan siswa baru. **Temuan**: (1) bug hitungan hadir (di atas); (2) di dev, token Google Meet di `.env` sudah `invalid_grant`, sehingga jadwal sesi gagal dengan JSON mentah Google — pesan dipetakan ke teks yang layak (`meeting_provider_auth_failed`/`_request_failed`) dan **QA dijalankan dengan penyedia pertemuan stub** (server QA dijalankan dari direktori sementara tanpa variabel `GOOGLE_MEET_*`, lalu dipulihkan). **Token Google Meet dev perlu diperbarui** agar sesi asli bisa dibuat. Tidak diverifikasi di browser: tampilan beku (`classroom_frozen`) — diuji di backend.


- `/mengajar` → konsol Ruang Kelas (daftar Grup Kelas, jadwal, absensi, sertifikat); `/kelas` → Ruang Kelas yang diikuti siswa.
- Dialog `convert-to-class`, `link-to-class`, `create-group-in-class` disambungkan ke API; tab absensi/sertifikat/laporan akademik memakai data server, bukan mock.
- Copy: **Ruang Kelas** (payung) dan **Grup Kelas**.

## P48-007 — Test & checkpoint (S)

✅ **SELESAI (2026-09-21).** `tests/integration/classroom_test.rs` **15 test**: hanya Pro yang membuat, produk pendukung (draft, harga 0, milik pengajar) + provisioning role teacher; visibilitas (pemilik/siswa terdaftar saja, orang lain 404); edit/arsip hanya pemilik dan Ruang Kelas terarsip menolak siswa/grup baru; Grup Kelas berkapasitas 1000 terikat ke Ruang Kelasnya dan tidak bisa ditambahkan oleh pengajar lain; bergabung = mendaftar (aktif/pending menurut harga, idempoten, keluar tidak membatalkan); kode undangan dan persetujuan; convert (tak ada yang keluar, anggota terdaftar, liga lama selamat, tak bisa dua kali; ke Ruang Kelas berbayar → pending); hanya owner + Pro + Ruang Kelas sendiri; unlink diblokir setelah ada sesi; sesi per grup hanya terlihat anggotanya dan menolak grup dari Ruang Kelas lain; roster sesi berbasis grup vs seluruh kelas; ikhtisar kelas (manager saja, hadir verifikasi + manual); beku saat langganan habis (sesi, sertifikat, grup baru ditolak; semua tetap terbaca; pulih saat berlangganan lagi). Regresi: test lama `attendance_test` dan `marketplace_test` (sesi/absensi/sertifikat/kohor) tetap lulus bersama 17 test materi P46 (31/31). Dijalankan dengan tambalan sementara `0063` yang dikembalikan (sha256 terverifikasi).


---

# Phase 49 — Liga Berjenjang, Monetisasi & Moderasi

## P49-001 — Sirkuit & perpindahan divisi (L)

- Migrasi `league_circuits(id, group_id, name)` dan `league_movements(id, season_id, user_id, from_league_id, to_league_id, kind in ('promoted','relegated','placed'), created_at)`.
- Penutupan musim untuk liga bersirkuit menutup **semua divisi sekaligus**: hitung dari snapshot beku, baru pindahkan (ADR-0015 §8). Aturan: poin 0 tidak dipromosikan, tidak beririsan, tamu tidak pindah, tier 1 tanpa promosi & tier terbawah tanpa degradasi. Anggota baru masuk tier terbawah.

**DoD:** test kasus tepi: peserta < jumlah slot, seri di batas zona, satu divisi kosong, crash di tengah tanpa dobel-pindah.

✅ **SELESAI (2026-09-24).** `migrations/0078_league_circuits.sql`, `services/league_circuit.rs`, job `league_circuit_close`. Keputusan: (1) **satu divisi = satu baris `group_leagues`** (kolom baru `circuit_id`, `tier`, `promotion_slots`, `relegation_slots`, semua-null atau semua-terisi); peserta divisi = `league_entries` eksplisit, bukan "semua anggota grup" seperti liga biasa, karena satu orang hanya di satu divisi; (2) semua divisi satu sirkuit **berbagi cadence & panjang musim** dan ditutup **serentak** — sirkuit yang divisinya tak sinkron dilewati utuh, tidak pernah ditutup separuh; (3) urutan tutup: kunci semua musim (`for update skip locked`) → bekukan semua klasemen dari snapshot langsung → bayar bonus → hitung naik/turun → tutup musim & buka musim berikut → pindahkan. Idempoten: musim baru belum jatuh tempo, jadi run kedua tidak melakukan apa pun (dibuktikan test); (4) **naik** hanya untuk anggota yang benar-benar mencetak poin (>0), maks `promotion_slots`; **turun** = ekor klasemen (boleh yang tidak aktif, kalau tidak kursi divisi atas tak pernah kosong) setelah yang naik dikeluarkan, jadi dua daftar tak pernah beririsan; tamu tidak pindah dan tidak dicatat di `league_movements`; anggota pasif tetap ikut musim berikut, tidak dibuang dari sirkuit; (5) sirkuit menolak cadence `one_off` (`invalid_cadence`) dan hanya bisa dibuat pemilik Pro (`circuits_require_pro`); (6) anggota baru (join/approve) ditempatkan di divisi terbawah dalam transaksi yang sama; (7) sebuah divisi tidak bisa diarsipkan sendiri (`archive_whole_circuit_instead`). Endpoint: `POST/GET /groups/{id}/circuits`, `GET /circuits/{id}` (tangga), `GET /circuits/{id}/movements?season=`, `DELETE /circuits/{id}`. 7 test (`league_circuit_test.rs`): bentuk & hak, penempatan anggota baru, perpindahan dari snapshot beku, slot > peserta, seri di batas zona, sirkuit tak sinkron, tamu.

## P49-002 — Monetisasi Ruang Kelas (M)

Ruang Kelas dijual lewat `learning_products` + `orders` + wallet 30/70 yang ada. Gerbang akses: `enrollments.status='active'`. Alur `pending` setelah convert (P48-003) selesai setelah pembayaran. **Grup Belajar tidak bisa dijual** (ditolak backend).

✅ **SELESAI (2026-09-24).** Tidak ada tabel baru: `PATCH /classrooms/{id} { price_idr }` (0–10.000.000; di atas 0 wajib Pro `can_monetize` → `403 monetization_requires_pro`; kembali ke 0 selalu boleh; perubahan harga masuk audit `classroom.price_changed`) menulis ke produk pendukung tersembunyi. Pendaftaran baru mengikuti harga saat ini (`pending` bila berbayar); **siswa yang sudah aktif tidak dikunci** saat harga dinaikkan. `GET /groups/{id}/sessions` mengembalikan `403 classroom_payment_required` bagi siswa berstatus `pending` (pemilik/admin tidak pernah digerbang). `ClassroomResponse` mendapat `my_enrollment_id` / `my_enrollment_status`, sehingga paywall bisa langsung memakai `POST /enrollments/{id}/checkout` → webhook QRIS → bagi hasil 70/30 yang sudah ada (diuji utuh: bayar → aktif → sesi terbuka → payout 70.000 dari 100.000). Grup Belajar memang tak punya harga (harga hanya di Ruang Kelas).

## P49-003 — Moderasi & laporan (M)

`POST /groups/{id}/report`, `GET /admin/groups/reports`, aksi admin platform (suspend grup) tercatat di audit; halaman ringkas di Admin Pusat "Grup".

✅ **SELESAI (2026-09-24).** `migrations/0079_group_reports.sql`, `services/group_moderation.rs`. `POST /groups/{id}/report { reason: spam|inappropriate|harassment|fraud|other, detail? }` (anggota/pengunjung yang bisa melihat grup; bukan pemilik sendiri → `409 cannot_report_own_group`; Grup Global tak bisa dilaporkan; satu laporan terbuka per orang per grup — klik ulang mengembalikan laporan yang sama; maks 20 laporan/hari/orang → `429 report_rate_limited`). Admin Pusat: `GET /admin/groups/reports?status=open|actioned|dismissed|all`, `POST /admin/groups/reports/{id}/resolve { resolution }`, `POST /admin/groups/{id}/suspend { reason }`, `POST /admin/groups/{id}/unsuspend` (izin `AdminPusat` View/Manage; pemilik grup **tidak** bisa menangguhkan grupnya sendiri). Suspend: `study_groups.status='suspended'` → hilang dari explore, tidak menerima anggota/tulis baru (semua jalur tulis sudah mensyaratkan `active`), tetap terbaca oleh anggota; semua laporan terbuka grup itu otomatis `actioned`; grup Global tak bisa ditangguhkan. Semua keputusan masuk `admin_audit_log` (suspend menyimpan alasannya). 6 test di `group_moderation_test.rs` (bersama 3 test monetisasi).

## P49-004 — Frontend: sirkuit, tangga divisi, evaluasi musim, checkout kelas (L)

`division-ladder-modal` dan `season-evaluation-modal` membaca `league_movements` asli (tidak lagi simulasi); checkout Ruang Kelas berbayar; layar "Fitur ini untuk Pro" dengan CTA.

✅ **KODE SELESAI (2026-09-24)**, verifikasi browser menunggu izin. `components/group/circuit-section.tsx` (daftar sirkuit di tab Liga, dialog buat sirkuit — format seragam untuk semua divisi: keaktifan/latihan/jalur belajar, divisi 2–8 dengan slot naik/turun; tangga divisi dengan zona naik/turun; "Evaluasi musim terakhir" dari `league_movements` asli; CTA "Fitur ini untuk Pro" bagi pemilik non-Pro), `classroom-paywall.tsx` (bayar via checkout marketplace + polling + tombol simulasi dev), editor harga di `/ruang-kelas/[id]`, `report-group-dialog.tsx` di header grup, halaman `/admin/grup` + menu "Moderasi Grup". Format tryout/ujian/olimpiade untuk divisi belum ada pemilih sumber di dialog sirkuit (API-nya sudah mendukung).

## P49-005 — Test & checkpoint (S)

✅ **SELESAI (2026-09-24).** Suite grup/liga/kelas/sirkuit/moderasi: **93 lulus, 0 gagal** (`-- study_group group_league classroom league_circuit`; `group_moderation_test` 6 lulus terpisah, sudah termasuk). Front-end: `tsc --noEmit` bersih, eslint bersih di berkas baru. Baseline 27 kegagalan lama di luar suite ini tidak disentuh.

---

# Phase 50 — Pembersihan & Verifikasi Akhir

## P50-001 — Hapus mock (S)
Hapus `lib/group-mock-data.ts` dan `store/group-store.ts` (persist localStorage), sisa `user-me`/`Kamu (John)`. Seed dev (bukan bundel produksi) untuk data demo bila perlu.

## P50-002 — Verifikasi menyeluruh (M)
Skenario `Bun.WebView` penuh, satu alur per persona: siswa gratis (mentok 3 grup), Plus (buat grup + liga tryout), Pro (Ruang Kelas → convert → sesi → absensi → sertifikat → liga berjenjang → tutup musim).

## P50-003 — Dokumentasi (S)
Sinkron `domain-model.md`, `api-contract.md`, STATE.md; catat asumsi ADR-0015 §9 yang sudah dikonfirmasi.

---

## Pertanyaan yang masih terbuka (tidak memblokir P45–P46)
Lihat ADR-0015 §9. Yang paling perlu dijawab sebelum **P47**: batas bonus XP liga per minggu dan jumlah liga aktif per grup Plus.
