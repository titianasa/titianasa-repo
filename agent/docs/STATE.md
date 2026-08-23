# ALR — Current State
Last updated: 2026-08-23 by backend-scaffold-session

## Fase aktif
Phase 0 — Foundation. P0-001 s/d P0-008 done. P0-009 in-progress (mobile ditunda). P0-010/P0-011 masih terbuka (P0-011 done).

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
**P0-009 (scaffold aplikasi)** — in-progress, cuma `titian-mobile` yang tersisa (ditunda). `titian-web` dan `titian-backend` selesai, jalan, dan sudah di-commit di repo masing-masing.

## Ticket selesai
- P0-001 s/d P0-006: ADR-0001 s/d ADR-0006 [done]
- P0-007: Migration SQL — 9 grup migration (`titian-backend/migrations/`), jalan + revert teruji, 33 tabel terverifikasi [done]
- P0-008: API contract cross-check — tidak ada mismatch field antara `api-contract.md` dan schema [done]
- P0-011: file protokol & STATE.md [done]

## Blocker aktif
Tidak ada.

## Lingkungan dev lokal (state mesin ini, bukan "keputusan" — dicatat biar next action tidak install ulang)
- Rust toolchain (rustup, stable) ter-install di `~/.cargo` — **tidak ada di PATH shell non-interaktif**, selalu `source "$HOME/.cargo/env"` dulu sebelum `cargo`/`sqlx` di sesi baru.
- `sqlx-cli` ter-install (`cargo install sqlx-cli --no-default-features --features rustls,postgres`).
- Postgres lokal jalan via Docker: `docker run -d --name titian-postgres -e POSTGRES_USER=titian -e POSTGRES_PASSWORD=titian_dev_password -e POSTGRES_DB=titian -p 5432:5432 postgres:16-alpine`. Kalau container ini mati/hilang, `titian-backend/.env`/`.env.example` sudah berisi `DATABASE_URL` yang cocok — tinggal jalankan ulang container dengan command yang sama.
- Git identity di-set **lokal per-repo saja** (bukan global) di `titian-web` dan `titian-backend`: `Sanja <ndsanja@gmail.com>`. `alr/` (root docs repo) belum di-set — set kalau mau commit di situ lagi dan belum ke-inherit.
- Dev server `titian-web` (`next dev --webpack`, port 3000) dan `titian-backend` (`cargo run`, port 8080) sempat dijalankan manual di background sesi ini untuk verifikasi — kemungkinan sudah tidak jalan lagi begitu sesi berakhir (bukan proses yang di-daemonize).

## Deviasi dari rencana
- `domain-model.md` (SQL migration siap pakai) dan `api-contract.md` ditulis lebih awal dari urutan ticket asli (harusnya P0-007/P0-008) karena isinya derivatif langsung dari ADR-0001 — bukan keputusan baru, jadi tidak perlu ADR terpisah.
- P0-009 dikerjakan sebelum P0-007/P0-008 pada sesi sebelumnya (bukan pelanggaran urutan — P0-009 "Depends on: -", user eksplisit minta mulai dari UI). P0-007/P0-008 lalu dikerjakan di sesi ini, setelah backend discaffold — urutan akhirnya: P0-009 (web) → P0-009 (backend scaffold kosong) → P0-007 → P0-008, bukan urutan linear dokumen asli, tapi semua acceptance criteria tetap terpenuhi.
- **Monorepo → repo terpisah per app** (lihat bagian "Struktur repo" di atas). Ini membatalkan satu poin yang disebut "locked" di `ALR_Build_Roadmap.md`. Keputusan datang langsung dari user.
- Next.js 16 default ke Turbopack, tapi PWA plugin (`@ducanh2912/next-pwa`) hanya support webpack → `titian-web` dev/build script dipaksa `--webpack`.
- shadcn/ui di `titian-web` di-init dengan library **Base UI** (bukan Radix, preset "Nova"/Lucide+Geist) — beda API polymorphism (`render` prop, bukan `asChild`).
- `titian-backend` pakai `docker run` manual untuk Postgres lokal, bukan `docker-compose` — tidak ada docker-compose.yml di repo ini. Kalau P0-010 (CI) atau kerja tim butuh compose file, itu belum dibuat.
- Belum ada ADR baru untuk keputusan stack/struktur repo di atas — dianggap keputusan tooling/proses, bukan keputusan yang mengunci data model, AI gateway, atau permission matrix (cakupan ADR 0001–0006).

## JANGAN lakukan ini tanpa ADR baru
- Jangan ubah struktur tabel di `domain-model.md` (khususnya `learning_events`, `masteries`, `frss_schedule` — dipakai lintas banyak fase) tanpa ADR baru yang menyatakan supersedes.
- Jangan panggil provider AI (DeepSeek/dst) langsung dari business logic — selalu lewat AI Gateway abstraction (ADR-0004).
- Jangan tambah role baru di luar daftar ADR-0006 tanpa update permission matrix.
- Jangan buat allowance subscription sebagai kolom terpisah dari `credits.balance` — semua saldo lewat agregasi `transactions` (ADR-0005).

## Next action
1. Mulai Phase 1 backend (P1-001 Auth Google OAuth+JWT) di `titian-backend` — folder `src/{models,repository,service,handler,routes}` dan pattern contoh (`health_*`) sudah siap dipakai sebagai template.
2. Begitu P1-001/P1-002/P1-003/P1-008/P1-009 ada endpoint asli, sambungkan `titian-web` (`src/store/user-store.ts`, `src/lib/mock-data.ts` masih mock) via TanStack Query + `src/lib/schemas.ts`, jaga bentuk field supaya cocok `docs/api-contract.md`.
3. `titian-mobile` (Expo, repo git sendiri) — mulai kapan pun user siap, ditunda bukan dibatalkan.
4. P0-010 (CI) — sekarang berarti CI config per repo (`titian-web`, `titian-backend`, nanti `titian-mobile`), bukan satu CI monorepo. Pertimbangkan juga `docker-compose.yml` untuk `titian-backend` supaya onboarding tim tidak perlu `docker run` manual.
