# Phase 0 — Foundation
Target: 2–3 minggu. Checkpoint keluar fase di bagian bawah file ini.

---

### P0-001 — ADR-0001: Canonical Data Model
**Status:** done
**Depends on:** -
**Acceptance Criteria:**
- [x] ERD mencakup semua entity dari roadmap (identity, content, concept, question, assessment, evaluation, learning engine, economy, exam/proctoring)
- [x] Prinsip generic content-agnostic dijelaskan eksplisit
**DoD:** ADR status Accepted, ada di `docs/adr/0001-canonical-data-model.md`.

### P0-002 — ADR-0002: Mastery Formula v1
**Status:** done
**Depends on:** P0-001
**Acceptance Criteria:**
- [x] Formula tertulis lengkap dengan parameter config-driven
- [x] Ada contoh perhitungan manual
**DoD:** ADR status Accepted, ada di `docs/adr/0002-mastery-formula.md`.

### P0-003 — ADR-0003: FRSS Algorithm v1
**Status:** done
**Depends on:** P0-001
**Acceptance Criteria:**
- [x] Update rule untuk 3 hasil (recalled/partial/forgot)
- [x] Ada contoh 5 siklus
- [x] Ada aturan anti-punitive (floor interval, cap per sesi, min gap)
**DoD:** ADR status Accepted, ada di `docs/adr/0003-frss-algorithm.md`.

### P0-004 — ADR-0004: AI Gateway Design
**Status:** done
**Depends on:** -
**Acceptance Criteria:**
- [x] Alur Task→Cost→Model→Prompt→Context→Generate→Validate→Track dijelaskan
- [x] AITask enum final untuk MVP
- [x] Provider abstraction (trait) didefinisikan
**DoD:** ADR status Accepted, ada di `docs/adr/0004-ai-gateway-design.md`.

### P0-005 — ADR-0005: Credit Economy
**Status:** done
**Depends on:** P0-004
**Acceptance Criteria:**
- [x] Unit credit didefinisikan
- [x] Pricing table AI task → credit charge
- [x] Aturan expiry & anti-abuse
**DoD:** ADR status Accepted, ada di `docs/adr/0005-credit-economy.md`.

### P0-006 — ADR-0006: RBAC
**Status:** done
**Depends on:** P0-001
**Acceptance Criteria:**
- [x] Daftar role final
- [x] Permission matrix per resource utama
**DoD:** ADR status Accepted, ada di `docs/adr/0006-rbac.md`.

---

### P0-007 — Migration SQL untuk semua tabel
**Status:** todo
**Depends on:** P0-001
**Deskripsi:** Eksekusi migration SQL dari `docs/domain-model.md` di database lokal (Postgres). Pecah jadi file migration bertahap per grup: (1) identity & organization, (2) curriculum tree, (3) concept graph, (4) question bank, (5) assessment & attempt, (6) evaluation & feedback, (7) learning engine, (8) economy, (9) exam & proctoring.
**Acceptance Criteria:**
- [ ] Semua migration jalan berurutan tanpa error (`sqlx migrate run`)
- [ ] Rollback (`migrate revert`) tiap file berfungsi
- [ ] Semua foreign key & check constraint sesuai `docs/domain-model.md`
- [ ] Index yang disebut eksplisit (`idx_attempts_user`, `idx_learning_events_user_time`, `idx_frss_due`, dll) ada
**DoD:** migration jalan di CI, `docs/domain-model.md` dicek konsisten dengan hasil `\d` di psql.
**Prompt untuk AI Agent:**
"Baca docs/STATE.md dan docs/domain-model.md. Buat migration sqlx (Rust) terpisah per grup entity sesuai urutan di deskripsi ticket P0-007. Jalankan migration di database lokal, verifikasi dengan \\dt dan \\d untuk tiap tabel. Update docs/STATE.md setelah selesai."

### P0-008 — API Contract v1 (cross-check final)
**Status:** todo (draft sudah ada di `docs/api-contract.md`, tinggal cross-check terhadap hasil P0-007)
**Depends on:** P0-007
**Acceptance Criteria:**
- [ ] Semua nama field di request/response `api-contract.md` cocok dengan nama kolom hasil migration
- [ ] Semua error code terdaftar konsisten
**DoD:** tidak ada mismatch antara `api-contract.md` dan schema DB aktual.

### P0-009 — Scaffold aplikasi (revisi: repo terpisah, bukan monorepo)
**Status:** in-progress (titian-web selesai; titian-backend dan titian-mobile belum digarap)
**Depends on:** -
**Deskripsi (direvisi 2026-08-23 atas instruksi eksplisit user):** semula didesain sebagai monorepo pnpm (`apps/web`, `apps/mobile`, `apps/api`, `packages/shared`) — lihat `ALR_Build_Roadmap.md` yang menyebut "monorepo" sebagai bagian stack terkunci. User memutuskan sebaliknya: **satu repo git independen per aplikasi**, supaya lebih gampang dikerjakan tim terpisah. Struktur baru, semua sejajar langsung di dalam `alr/`:
- `alr/titian-web/` — Next.js 16, git repo sendiri. **Selesai di-scaffold.**
- `alr/titian-backend/` — Rust/Axum, git repo sendiri. **Belum dibuat.**
- `alr/titian-mobile/` — Expo/React Native, git repo sendiri. **Belum dibuat.**
- `alr/agent/` — dokumentasi bersama (roadmap, ADR, ticket) — tetap satu-satunya isi repo `alr/` itu sendiri (bukan bagian dari repo aplikasi manapun).

Tidak ada lagi `packages/shared` — karena tiap app repo-nya independen, kontrak tipe (zod schema dsb) di-duplikasi per-repo saat dibutuhkan alih-alih di-share lewat package. Lihat `titian-web/src/lib/schemas.ts` (isinya identik dengan bekas `packages/shared/src/schemas.ts`) — copy file itu ke `titian-backend`/`titian-mobile` nanti kalau perlu skema yang sama, bukan reference ke package.

**Acceptance Criteria:**
- [x] `titian-web` (Next.js 16) scaffold sukses build standalone (`next build --webpack`, tanpa workspace apa pun) — shadcn/ui (Base UI), Tailwind v4 dark mode + tema kuning, TanStack Query, Zustand, React Hook Form + Zod, Framer Motion, PWA manifest+service worker (`@ducanh2912/next-pwa`), bottom nav mobile-first
- [x] `titian-web` git repo sendiri (`git init` di dalam foldernya, terpisah dari `alr/`)
- [ ] `titian-backend` (Rust/Axum) — repo + struktur folder standar (`src/models`, `src/repository`, `src/service`, `src/handler`, `src/routes`) — belum digarap
- [ ] `titian-mobile` (Expo) — belum digarap
**DoD:** tiap repo build hijau independen, tidak saling depends secara tooling (boleh saling depends secara kontrak API/schema yang didokumentasikan di `docs/api-contract.md` dan `docs/domain-model.md`).
**Catatan implementasi (lihat juga Deviasi di STATE.md):**
- Next.js 16 default ke Turbopack; `@ducanh2912/next-pwa` (untuk service worker/offline) hanya kompatibel webpack. `dev`/`build` script di `titian-web/package.json` di-set eksplisit `--webpack`.
- shadcn/ui di-init dengan library **Base UI** (preset "Nova", bukan Radix) — pola polymorphism-nya pakai prop `render`, bukan `asChild`. Untuk tombol yang me-render elemen non-button (mis. `<Link>`), wajib tambah `nativeButton={false}` supaya tidak muncul warning aksesibilitas Base UI.
- UI/auth masih mock: `src/store/user-store.ts` (Zustand, persisted) menyimpan user+role dummy sampai P1-001/P1-002 (Google OAuth, `/users/me`) tersedia. Halaman `/belajar`, `/latihan`, `/progres` pakai data dummy di `src/lib/mock-data.ts`, bentuknya mengikuti `docs/domain-model.md` supaya gampang diganti fetch asli nanti.

### P0-010 — Setup CI
**Status:** todo
**Depends on:** P0-009
**Acceptance Criteria:**
- [ ] PR trigger: lint + test + build untuk semua workspace
- [ ] PR dummy (perubahan trivial) menghasilkan pipeline hijau
**DoD:** CI config ada di repo, minimal 1 PR percobaan lulus pipeline.

### P0-011 — File protokol & state awal
**Status:** done (dokumen ini + STATE.md + ai-agent-protocol.md sudah dibuat)
**Depends on:** -
**DoD:** `docs/STATE.md` dan `docs/ai-agent-protocol.md` ada dan terisi.

---

## Checkpoint keluar Phase 0 (WAJIB terpenuhi sebelum mulai Phase 1)
- [ ] Semua ADR (0001–0006) status Accepted
- [ ] Migration jalan sukses di local Postgres, semua tabel & index sesuai domain-model.md
- [ ] `pnpm build` sukses di seluruh monorepo
- [ ] CI hijau untuk minimal 1 PR
- [ ] `docs/STATE.md` menunjukkan semua ticket P0-001 s/d P0-011 berstatus done

Kalau salah satu belum tercentang, **jangan mulai ticket Phase 1**.
