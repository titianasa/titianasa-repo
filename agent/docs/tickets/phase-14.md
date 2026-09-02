# Phase 14 (ticket-numbering) — Gamification & Economy Frontend

## Keputusan scope (baca duluan)

Item pertama dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap dan alasannya
dicatat di `docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan
semuanya'". Fase ini dipilih pertama karena backend-nya SUDAH ADA
PENUH (P8-001..006, P11-001..005) — murni kerja frontend, tidak ada
endpoint baru, jadi paling cepat memberi nilai nyata.

**Temuan mengejutkan sebelum mulai coding** (dikonfirmasi baca kode
langsung, bukan asumsi): `user-store.ts`'s `streakDays`/`xp`/
`creditBalance` — yang ditampilkan di `TopBar` DAN `StatCards` di
SETIAP halaman — adalah **angka hardcode** (`4`/`1280`/`35`) sejak
awal proyek, comment di kode sendiri bilang "mocked until gamification
tickets exist". Endpoint aslinya (`GET /me/xp`, `GET /me/streak`,
`GET /me/credits`) sudah ada sejak Phase 8/11 tapi TIDAK PERNAH
disambungkan — dashboard paling sering dilihat user justru yang
paling lama menampilkan data palsu. Ini prioritas #1 ticket-phase ini,
bukan cuma "nice to have".

**Keputusan penempatan UI** (tidak ada spek eksplisit dari roadmap
soal tata letak, jadi diputuskan sendiri mengikuti struktur nav yang
ADA — bottom nav sudah penuh 5 slot, TIDAK ditambah item baru):
- Leaderboard/League/Achievements masuk sebagai **tab baru di
  `/progres`** (halaman yang sudah tentang "posisi belajarmu"),
  bukan route/nav item terpisah.
- Daily Mission jadi **card baru di `/beranda`** (pola sama card
  "review due" yang sudah ada di situ).
- Diamond balance + subscribe + watch-ad jadi **halaman baru
  `/profil/diamond`**, dijangkau dari 1 baris baru di
  `SettingsList` (`/profil`) — uang/langganan itu "pengaturan akun",
  bukan "progres belajar".

**Dieksplisit DIDEFER**: notifikasi push (switch di `SettingsList`
sudah ada tapi murni state lokal, tidak ada backend — itu Phase 7
Mobile yang ditunda), pembelian Diamond langsung dengan uang (belum
ada payment gateway asli, cuma alur subscribe yang sudah distub P11
yang disentuh), dan funnel/analytics tracking (§6.15, butuh infra
terpisah, bukan scope FE).

## Ticket

### P14-001 — Wire real XP/Streak/Diamond ke chrome global
**Status:** done
**Depends on:** P8-001 (`GET /me/xp`), P8-002 (`GET /me/streak`), P11-002 (`GET /me/credits`)
**Deskripsi:** Ganti angka hardcode di `user-store.ts` dengan data asli via react-query, dipakai `TopBar` dan `StatCards`.
**Acceptance Criteria:**
- [x] `gamificationApi`/`economyApi` baru di `api-client.ts` (xp/streak/credits)
- [x] Hook `useXp`/`useStreak`/`useCredits` (react-query, pola sama `use-learning-queue.ts`)
- [x] `streakDays`/`xp`/`creditBalance` DIHAPUS dari `user-store.ts` (bukan sekadar tidak dipakai — data server, bukan client state, jangan di-persist zustand)
- [x] `TopBar`+`StatCards` pakai hook baru, loading state (skeleton/dash) saat belum resolve
**DoD:** `bun run build` sukses, verifikasi visual via `Bun.WebView` — angka di top bar cocok dengan row asli di DB (bukan 4/1280/35 lagi).

### P14-002 — Achievements tab
**Status:** done
**Depends on:** P8-003 (`GET /me/achievements`)
**Deskripsi:** Daftar achievement yang sudah didapat, dikelompokkan per `category` (Learning/Skill/Improvement, P8-003).
**Acceptance Criteria:**
- [x] Tab "Pencapaian" baru di `/progres` (pakai `Tabs` primitive yang sudah ada)
- [x] Kosong (belum ada achievement) → empty state, bukan list kosong senyap
**DoD:** Terverifikasi visual, achievement asli dari seed/test data muncul dengan nama+deskripsi+tanggal benar.

### P14-003 — Daily Mission card
**Status:** done
**Depends on:** P8-004 (`GET /me/daily-mission`)
**Deskripsi:** Card di Beranda menampilkan progress vs target per skill (vocabulary/grammar/listening/speaking, P8-004) + status reward.
**Acceptance Criteria:**
- [x] Card baru di `/beranda`, di bawah `StatCards` — pola visual sama card "review due"
- [x] `reward_claimed: true` ditampilkan beda (badge "Selesai") dari yang belum
**DoD:** Terverifikasi visual, progress bar per skill sesuai response asli.

### P14-004 — Leaderboard tab
**Status:** done
**Depends on:** P8-005 (`GET /leaderboard/weekly`)
**Deskripsi:** Tab "Peringkat" — daftar top-N + baris "posisi saya" (`me`, bisa di luar daftar top-N yang ditampilkan).
**Acceptance Criteria:**
- [x] `me: null` (belum ada XP minggu ini) → pesan eksplisit, bukan baris kosong/error
- [x] Baris "saya" disorot visual beda dari baris lain
**DoD:** Terverifikasi visual dengan ≥2 user berbeda XP di data test/seed.

### P14-005 — League tab
**Status:** done
**Depends on:** P8-005 (`GET /me/league`)
**Deskripsi:** Tab "Liga" — tier saat ini (`bronze`→`master`) + breakdown 3 input (`current_streak`/`average_mastery`/`weekly_activity_count`) supaya user paham KENAPA di tier itu, bukan cuma angka.
**Acceptance Criteria:**
- [x] 6 tier divisualisasikan berbeda (warna/badge per tier, bukan teks polos)
- [x] 3 input breakdown ditampilkan eksplisit (transparansi formula, sesuai §6.4 "supaya user tidak merasa dibeli lewat XP doang")
**DoD:** Terverifikasi visual.

### P14-006 — Diamond & Langganan page
**Status:** done
**Depends on:** P11-002 (`GET/POST /subscriptions/*`, `GET /me/credits`), P11-004 (`POST /ads/watch`)
**Deskripsi:** `/profil/diamond` — saldo Diamond, status langganan (`subscribed:false` → tawaran subscribe Plus/Pro; `subscribed:true` → detail periode aktif), tombol "Tonton iklan" (demo `StubAdProvider`, jelaskan di UI ini simulasi).
**Acceptance Criteria:**
- [x] Baris baru "Diamond & Langganan" di `SettingsList` (`/profil`), navigasi ke halaman baru
- [x] Subscribe Plus/Pro → `useMutation` + invalidate query saldo+status setelahnya (saldo naik terlihat tanpa refresh manual)
- [x] Watch-ad button → invalidate saldo setelah sukses (walau `StubAdProvider` tidak benar-benar menambah diamond, cuma buka 1x aksi AI gratis — UI harus jujur soal ini, bukan menjanjikan diamond bertambah)
**DoD:** Terverifikasi visual, subscribe asli mengubah tampilan status+saldo tanpa reload.

### P14-007 — Integration check + exit checkpoint
**Status:** done
**Depends on:** P14-001 s/d P14-006
**Deskripsi:** Verifikasi visual end-to-end via `Bun.WebView` (pola P6-005/P4-005) — bukan cuma "kodenya ada".
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit` bersih di `titian-web`
- [x] Semua 6 permukaan baru (chrome global, achievements, daily mission, leaderboard, league, diamond page) di-screenshot lewat browser asli dengan data asli dari backend yang jalan
**DoD:** Tidak ada halaman yang nampilkan data placeholder/hardcode yang tersisa dari sebelum ticket-phase ini.

**Catatan implementasi:** Verifikasi lewat `Bun.WebView` (backend `chrome`) nyata terhadap `titian-backend-bun` yang jalan asli, bukan mock — skrip seed sekali-pakai (dihapus lagi setelah dipakai, tidak dicommit) bikin 2 user demo (Sani/Budi) dengan xp_events/user_streaks/credits/achievements/daily_mission asli, plus refresh token diinsert langsung ke `refresh_tokens` supaya `SessionBootstrap` (`POST /auth/refresh`) bisa dites lewat alur asli, bukan token editan tangan. **1 race condition nyata ditemukan pas verifikasi** (murni bug test-harness, BUKAN bug aplikasi): `localStorage.setItem()` dari luar via `evaluate()` bisa "distomp" balik ke `null` oleh `SessionBootstrap`'s `clear()` yang masih in-flight dari page load SEBELUMNYA (React effect async, localStorage-nya ditulis ulang oleh persist middleware) — fix-nya di script verifikasi (tunggu ~1.5s setelah navigasi pertama sebelum inject token), BUKAN di kode aplikasi (dikonfirmasi lewat instrumentasi console.log sementara di `session-bootstrap.tsx`, di-revert lagi setelah kelar debug, `git diff` bersih). Semua data demo dihapus dari dev DB sesudahnya (dikonfirmasi via query ulang). Subscribe Plus→saldo 42→142, upgrade ke Pro→442, watch-ad→saldo tetap 442 (cuma buka 1x AI gratis, TIDAK menambah saldo) — semua diverifikasi via klik tombol asli + screenshot, bukan diasumsikan dari kode. Total **461/461 backend test tetap hijau** (tidak ada perubahan backend di fase ini), `bunx tsc --noEmit` + `bun run lint` + `bun run build` bersih di `titian-web`.

---

## Checkpoint keluar Phase 14
1. [x] Top bar & dashboard tidak lagi menampilkan angka hardcode — dibuktikan dengan mengubah data di DB lalu reload, angka di UI ikut berubah.
2. [x] Keempat tab baru di `/progres` (Penguasaan/Peringkat/Liga/Pencapaian) semuanya menampilkan data asli, bukan placeholder.
3. [x] Diamond page: subscribe dan watch-ad keduanya terbukti mengubah saldo/status yang terlihat di UI secara real-time (invalidate query), tidak butuh reload manual.

Phase 14 tertutup. Lanjut Phase 15 — Marketplace Frontend.
