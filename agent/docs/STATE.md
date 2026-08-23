# ALR — Current State
Last updated: 2026-08-23 by frontend-scaffold-session

## Fase aktif
Phase 0 — Foundation (mengerjakan P0-009 duluan, paralel dengan P0-007/008 karena tidak saling depends-on)

## Struktur repo (PENTING — beda dari `ALR_Build_Roadmap.md`)
`ALR_Build_Roadmap.md` menyebut monorepo sebagai bagian stack "terkunci". Itu sudah **tidak berlaku** —
atas instruksi eksplisit user (2026-08-23), proyek pindah ke **satu repo git independen per aplikasi**
supaya gampang dikerjakan tim terpisah:
- `alr/titian-web/` — Next.js 16, repo git sendiri. **Sudah di-scaffold.**
- `alr/titian-backend/` — Rust/Axum, repo git sendiri. **Belum dibuat.**
- `alr/titian-mobile/` — Expo/React Native, repo git sendiri. **Belum dibuat.**
- `alr/agent/` — dokumentasi bersama (roadmap, ADR, ticket, file ini) — satu-satunya isi repo `alr/` itu sendiri.

Konsekuensi: tidak ada lagi `packages/shared` package. Kontrak tipe (zod schema dll) di-duplikasi
manual per-repo saat dibutuhkan — lihat `titian-web/src/lib/schemas.ts`. Setiap repo build & deploy
independen; yang menyatukan mereka cuma kontrak yang didokumentasikan di `docs/api-contract.md` dan
`docs/domain-model.md`, bukan tooling. Detail lengkap di catatan P0-009 (`docs/tickets/phase-0.md`).

## Ticket sedang dikerjakan
**P0-009 (scaffold aplikasi)** — in-progress. `titian-web` (Next.js 16 + brand "TITIAN") sudah selesai dan lulus `build`/`lint`/verifikasi visual browser, git repo sendiri sudah di-init (belum ada commit — menunggu konfirmasi user). `titian-backend` (Rust/Axum) dan `titian-mobile` (Expo) belum digarap.
Ticket lain yang masih menunggu: **P0-007 (migration SQL)**, **P0-008 (api-contract cross-check)** — belum tersentuh sesi ini.

## Ticket selesai
- P0-001: ADR-0001 Canonical Data Model [done]
- P0-002: ADR-0002 Mastery Formula [done]
- P0-003: ADR-0003 FRSS Algorithm [done]
- P0-004: ADR-0004 AI Gateway Design [done]
- P0-005: ADR-0005 Credit Economy [done]
- P0-006: ADR-0006 RBAC [done]
- (domain-model.md dan api-contract.md sudah ditulis mendahului P0-007/P0-008 sebagai referensi teknis dari ADR di atas — lihat catatan)

## Blocker aktif
Tidak ada.

## Deviasi dari rencana
- `domain-model.md` (SQL migration siap pakai) dan `api-contract.md` ditulis lebih awal dari urutan ticket asli (harusnya P0-007/P0-008) karena isinya derivatif langsung dari ADR-0001 — bukan keputusan baru, jadi tidak perlu ADR terpisah. Saat P0-007 dieksekusi, tinggal jalankan SQL yang sudah ada di `domain-model.md`, tidak perlu didesain ulang.
- P0-009 dikerjakan sebelum P0-007/P0-008 (bukan pelanggaran urutan — P0-009 di ticket asli memang "Depends on: -", dan user secara eksplisit minta mulai dari UI).
- **Monorepo → repo terpisah per app** (lihat bagian "Struktur repo" di atas). Ini membatalkan satu poin yang disebut "locked" di `ALR_Build_Roadmap.md`. Keputusan datang langsung dari user, bukan inisiatif agent — dicatat di sini supaya sesi berikutnya tidak bingung kenapa strukturnya beda dari dokumen roadmap awal.
- Next.js 16 default ke Turbopack, tapi PWA plugin (`@ducanh2912/next-pwa`, untuk service worker/offline) hanya support webpack → `titian-web` dev/build script dipaksa `--webpack`. Kalau nanti ada alternatif PWA yang Turbopack-native (mis. Serwist), ini bisa dicabut — bukan keputusan permanen, murni kompatibilitas library saat ini.
- shadcn/ui di `titian-web` di-init dengan library **Base UI** (bukan Radix, preset "Nova"/Lucide+Geist) — beda API polymorphism (`render` prop, bukan `asChild`). Perlu diketahui agent berikutnya yang menambah komponen shadcn baru.
- Belum ada ADR baru untuk keputusan stack/struktur repo di atas — dianggap keputusan tooling/proses, bukan keputusan yang mengunci data model, AI gateway, atau permission matrix (cakupan ADR 0001–0006).

## JANGAN lakukan ini tanpa ADR baru
- Jangan ubah struktur tabel di `domain-model.md` (khususnya `learning_events`, `masteries`, `frss_schedule` — dipakai lintas banyak fase) tanpa ADR baru yang menyatakan supersedes.
- Jangan panggil provider AI (DeepSeek/dst) langsung dari business logic — selalu lewat AI Gateway abstraction (ADR-0004).
- Jangan tambah role baru di luar daftar ADR-0006 tanpa update permission matrix.
- Jangan buat allowance subscription sebagai kolom terpisah dari `credits.balance` — semua saldo lewat agregasi `transactions` (ADR-0005).

## Next action
1. Konfirmasi ke user: apakah initial commit `titian-web` (dan `alr/` docs) mau dibuat sekarang, atau mereka yang urus sendiri. Belum ada commit di kedua repo per akhir sesi ini.
2. `titian-web` masih pakai data & auth mock (`src/store/user-store.ts`, `src/lib/mock-data.ts`) — begitu P1-001/P1-002/P1-003/P1-008/P1-009 (auth, curriculum, mastery, FRSS) tersedia di `titian-backend`, ganti dengan fetch asli via TanStack Query + schema di `src/lib/schemas.ts`, jaga bentuk field supaya cocok `docs/api-contract.md`.
3. Jalankan P0-007: eksekusi migration SQL dari `docs/domain-model.md` di database lokal (di dalam `titian-backend` begitu repo itu dibuat), pecah jadi beberapa file migration bertahap per grup entity.
4. Lanjut P0-008: cross-check `docs/api-contract.md` terhadap schema hasil migration, sesuaikan kalau ada mismatch nama field.
5. Buat `titian-backend` (Rust/Axum, struktur folder `src/models|repository|service|handler|routes`, repo git sendiri) dan `titian-mobile` (Expo, repo git sendiri), lalu P0-010 (CI — sekarang berarti CI config per repo, bukan satu CI monorepo).
