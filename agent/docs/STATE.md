# ALR — Current State
Last updated: 2026-08-23 by titian-web-google-login-wiring-session

## Fase aktif
Phase 1 — Backend Core sudah dimulai (P1-001 done) meski Phase 0 belum tertutup formal (P0-010 CI dan mobile scaffold masih terbuka) — ini disengaja atas instruksi eksplisit user, lihat "Deviasi".

## PENTING — baca sebelum mulai kerja
1. **Ada proyek lain di `/home/john/Dev/sanja-workspace/lms/`** (sejajar dengan `alr/`, di luar folder ini) berisi `alr-backend`/`alr-web`/`alr-mobile` versi lain yang jauh lebih maju (Phase 0-2 sudah banyak selesai di sana), dengan dokumentasi sendiri (`ALR_TECHNICAL_BLUEPRINT.md`, bukan `agent/docs/`). **User sudah eksplisit konfirmasi (2026-08-23): `lms/` tidak dipakai lagi, abaikan.** Proyek yang aktif adalah `alr/` ini. Jangan tanya ulang soal ini kecuali user membawanya lagi.
2. **Struktur bukan monorepo** — lihat bagian di bawah.

## Struktur repo (PENTING — beda dari `ALR_Build_Roadmap.md`)
`ALR_Build_Roadmap.md` menyebut monorepo sebagai bagian stack "terkunci". Itu sudah **tidak berlaku** —
atas instruksi eksplisit user (2026-08-23), proyek pindah ke **satu repo git independen per aplikasi**
supaya gampang dikerjakan tim terpisah:
- `alr/titian-web/` — Next.js 16, repo git sendiri. **Sudah di-scaffold, sudah di-commit.**
- `alr/titian-backend/` — Rust/Axum, repo git sendiri. **Sudah di-scaffold, migration jalan, sudah di-commit.**
- `alr/titian-mobile/` — Expo/React Native, repo git sendiri. **Belum dibuat — ditunda atas instruksi user ("mobile nanti aja").**
- `alr/agent/` — dokumentasi bersama (roadmap, ADR, ticket, file ini) — satu-satunya isi repo `alr/` itu sendiri.

Konsekuensi: tidak ada lagi `packages/shared` package. Kontrak tipe (zod schema dll) di-duplikasi
manual per-repo saat dibutuhkan — lihat `titian-web/src/lib/schemas.ts`. Setiap repo build & deploy
independen; yang menyatukan mereka cuma kontrak yang didokumentasikan di `docs/api-contract.md` dan
`docs/domain-model.md`, bukan tooling. Detail lengkap di catatan P0-009 (`docs/tickets/phase-0.md`).

## Ticket sedang dikerjakan
Tidak ada yang in-progress — P1-001 baru saja selesai. Next up: P1-002 (User & Profile) — lihat "Next action".

## Ticket selesai
- P0-001 s/d P0-006: ADR-0001 s/d ADR-0006 [done]
- P0-007: Migration SQL — 10 grup migration (`titian-backend/migrations/`, grup ke-10 ditambah di sesi P1-001), jalan + revert teruji, 34 tabel terverifikasi [done]
- P0-008: API contract cross-check — tidak ada mismatch field antara `api-contract.md` dan schema [done]
- P0-009: `titian-web` + `titian-backend` selesai di-scaffold, jalan, di-commit. `titian-mobile` masih belum (ditunda) — lihat status P0-009 di `docs/tickets/phase-0.md` untuk detail, ticket ini tetap tercatat in-progress di sana.
- P0-011: file protokol & STATE.md [done]
- **P1-001: Auth Google OAuth + JWT** — `POST /auth/google/callback` dan `POST /auth/refresh` jalan penuh di `titian-backend`, 11 integration test lulus. Detail lengkap di `docs/tickets/phase-1.md`.
- **`titian-web` disambungkan ke auth asli** — tombol login mock diganti Google Identity Services beneran (`src/components/auth/google-sign-in-button.tsx`), session di-persist via `auth-store.ts` (cuma refresh token yang disimpan, access token di-re-derive tiap boot lewat `/auth/refresh` — lihat `session-bootstrap.tsx`), route `(app)/*` di-gate lewat `require-auth.tsx` (redirect ke `/login` kalau belum login). CORS ditambah di backend (`FRONTEND_ORIGIN`) supaya browser boleh manggil API cross-origin.

## Blocker aktif
**Google Sign-In belum bisa dites end-to-end sampai origin di-whitelist.** Waktu dicoba di `http://localhost:3000`, Google nolak dengan `[GSI_LOGGER]: The given origin is not allowed for the given client ID` (403). Ini bukan bug kode — client ID di `Credential.md`/`google-auth.md` belum punya `http://localhost:3000` (dan domain produksi nanti) di daftar "Authorized JavaScript origins"-nya. **Cuma user yang bisa fix ini** (butuh akses Google Cloud Console project punya client ID `1029049482781-...`), bukan sesuatu yang bisa diperbaiki dari kode. Langkah: Google Cloud Console → APIs & Services → Credentials → pilih OAuth client itu → tambahkan `http://localhost:3000` ke "Authorized JavaScript origins" → save (biasanya langsung aktif, kadang perlu beberapa menit). Sisa alur (redirect kalau belum login, error handling, sesi persist, dsb) sudah diverifikasi jalan lewat Playwright — cuma langkah terakhir (klik tombol Google beneran) yang belum bisa dites dari sini.

## Lingkungan dev lokal (state mesin ini, bukan "keputusan" — dicatat biar next action tidak install ulang)
- Rust toolchain (rustup, stable) ter-install di `~/.cargo` — **tidak ada di PATH shell non-interaktif**, selalu `source "$HOME/.cargo/env"` dulu sebelum `cargo`/`sqlx` di sesi baru.
- `sqlx-cli` ter-install (`cargo install sqlx-cli --no-default-features --features rustls,postgres`).
- Postgres lokal jalan via Docker: `docker run -d --name titian-postgres -e POSTGRES_USER=titian -e POSTGRES_PASSWORD=titian_dev_password -e POSTGRES_DB=titian -p 5432:5432 postgres:16-alpine`. Kalau container ini mati/hilang, `titian-backend/.env`/`.env.example` sudah berisi `DATABASE_URL` yang cocok — tinggal jalankan ulang container dengan command yang sama.
- Git identity di-set **lokal per-repo saja** (bukan global) di `titian-web` dan `titian-backend`: `Sanja <ndsanja@gmail.com>`. `alr/` (root docs repo) belum di-set — set kalau mau commit di situ lagi dan belum ke-inherit.
- Dev server `titian-web` (`next dev --webpack`, port 3000) dan `titian-backend` (`cargo run`/binary langsung, port 8080) sempat dijalankan manual di background lintas sesi (termasuk sesi P1-001 ini) untuk verifikasi — kemungkinan sudah tidak jalan lagi begitu sesi berakhir (bukan proses yang di-daemonize, bukan systemd/supervisor).
- `titian-backend` sekarang struktur `lib.rs` + `main.rs` (dipecah di sesi P1-001 supaya `tests/*.rs` bisa import modul internal & build router asli). Kalau nambah module baru, daftarkan di `lib.rs`, bukan `main.rs`.

## Deviasi dari rencana
- `domain-model.md` (SQL migration siap pakai) dan `api-contract.md` ditulis lebih awal dari urutan ticket asli (harusnya P0-007/P0-008) karena isinya derivatif langsung dari ADR-0001 — bukan keputusan baru, jadi tidak perlu ADR terpisah.
- P0-009 dikerjakan sebelum P0-007/P0-008 pada sesi sebelumnya (bukan pelanggaran urutan — P0-009 "Depends on: -", user eksplisit minta mulai dari UI). P0-007/P0-008 lalu dikerjakan di sesi ini, setelah backend discaffold — urutan akhirnya: P0-009 (web) → P0-009 (backend scaffold kosong) → P0-007 → P0-008, bukan urutan linear dokumen asli, tapi semua acceptance criteria tetap terpenuhi.
- **Monorepo → repo terpisah per app** (lihat bagian "Struktur repo" di atas). Ini membatalkan satu poin yang disebut "locked" di `ALR_Build_Roadmap.md`. Keputusan datang langsung dari user.
- Next.js 16 default ke Turbopack, tapi PWA plugin (`@ducanh2912/next-pwa`) hanya support webpack → `titian-web` dev/build script dipaksa `--webpack`.
- shadcn/ui di `titian-web` di-init dengan library **Base UI** (bukan Radix, preset "Nova"/Lucide+Geist) — beda API polymorphism (`render` prop, bukan `asChild`).
- `titian-backend` pakai `docker run` manual untuk Postgres lokal, bukan `docker-compose` — tidak ada docker-compose.yml di repo ini. Kalau P0-010 (CI) atau kerja tim butuh compose file, itu belum dibuat.
- Belum ada ADR baru untuk keputusan stack/struktur repo di atas — dianggap keputusan tooling/proses, bukan keputusan yang mengunci data model, AI gateway, atau permission matrix (cakupan ADR 0001–0006).
- **Tabel `refresh_tokens` ditambahkan** (migrasi ke-10, `titian-backend/migrations/0010_auth_sessions.*`) untuk P1-001 — tidak ada di dump ERD asli ADR-0001. Ini additive (tabel baru, bukan ubah tabel lama), jadi menurut aturan "JANGAN lakukan ini tanpa ADR baru" di bawah tidak melanggar (yang dilarang cuma ubah `learning_events`/`masteries`/`frss_schedule`, dan mengunci struktur tanpa ADR — nambah tabel baru untuk kebutuhan ticket yang sudah disetujui itu normal). Sudah disinkronkan ke `docs/domain-model.md`.
- Google id_token diverifikasi dengan fetch JWKS asli Google (`https://www.googleapis.com/oauth2/v3/certs`) di runtime, di-cache in-memory (`Arc<RwLock<Vec<Jwk>>>`, refresh sekali kalau `kid` tidak ketemu). Belum ada TTL/refresh berkala terjadwal — kalau Google rotate key lebih sering dari yang diasumsikan ini masih aman (refresh-on-miss), tapi kalau butuh proactive refresh itu future work, bukan blocker sekarang.
- **Gotcha zustand-persist (kejadian di sesi ini, catat biar tidak keulang):** jangan panggil `useXStore.setState(...)` di dalam `onRehydrateStorage` milik store yang sama — itu bisa jalan **sinkron selama `create()` masih berjalan**, sebelum `const useXStore = ...` selesai di-assign, jadi referensinya belum ada (gagal diam-diam, hydration flag jadi macet, komponen yang nunggu hydration nge-hang selamanya tanpa error). Pola yang benar: taruh registrasi listener-nya **setelah** `const useXStore = create(...)` selesai, pakai `useXStore.persist.onFinishHydration(fn)` + cek `useXStore.persist.hasHydrated()` buat kasus udah kejadian duluan. Lihat `titian-web/src/store/auth-store.ts` buat contoh polanya.

## JANGAN lakukan ini tanpa ADR baru
- Jangan ubah struktur tabel di `domain-model.md` (khususnya `learning_events`, `masteries`, `frss_schedule` — dipakai lintas banyak fase) tanpa ADR baru yang menyatakan supersedes.
- Jangan panggil provider AI (DeepSeek/dst) langsung dari business logic — selalu lewat AI Gateway abstraction (ADR-0004).
- Jangan tambah role baru di luar daftar ADR-0006 tanpa update permission matrix.
- Jangan buat allowance subscription sebagai kolom terpisah dari `credits.balance` — semua saldo lewat agregasi `transactions` (ADR-0005).

## Next action
1. **User: whitelist `http://localhost:3000` di Google Cloud Console** (lihat "Blocker aktif") — begitu ini beres, login Google beneran siap dites end-to-end oleh user langsung di browser.
2. **P1-002 (User & Profile + user_organization_roles)** — ticket Phase 1 berikutnya, depends on P1-001 (done). Endpoint: `GET /users/me`, `GET /organizations/{id}/members`. Butuh middleware `AuthContext` (extract JWT dari `Authorization: Bearer`, decode pakai `JWT_ACCESS_SECRET`, resolve role dari `user_organization_roles`) — belum ada sama sekali, P1-001 cuma issue token, belum ada endpoint yang memvalidasinya. Pattern `google_oauth.rs`/`token_service.rs` (`titian-backend/src/service/`) bisa dipakai buat decode access token JWT-nya (`AccessTokenClaims` di `token_service.rs`). Begitu `/users/me` ada, `titian-web` bisa fetch role asli & profile lengkap (`api-client.ts` sudah punya pola `authApi`, tinggal tambah `usersApi`), gantikan role/streak/xp/credit yang masih mock di `user-store.ts`.
3. `titian-mobile` (Expo, repo git sendiri) — mulai kapan pun user siap, ditunda bukan dibatalkan.
4. P0-010 (CI) — sekarang berarti CI config per repo (`titian-web`, `titian-backend`, nanti `titian-mobile`), bukan satu CI monorepo. `titian-backend` sekarang punya test suite asli (`cargo test`, butuh `DATABASE_URL` ke Postgres yang bisa CREATEDB) yang layak masuk CI. Pertimbangkan juga `docker-compose.yml` untuk `titian-backend` supaya onboarding tim tidak perlu `docker run` manual.
