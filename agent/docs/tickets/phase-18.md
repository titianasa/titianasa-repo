# Phase 18 (ticket-numbering) — Organization Admin Frontend

## Keputusan scope (baca duluan)

Item ke-5 dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap di
`docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan semuanya'".

**1 bug backend nyata ditemukan** — bukan gap fitur kali ini, tapi
response shape yang salah sejak awal: `GET /organizations/{id}/members`
BALIKIN `userId` (camelCase, langsung dari `MemberRow` repository tanpa
mapping) padahal `api-contract.md` SUDAH sejak awal mendokumentasikan
`user_id` (snake_case, konsisten SEMUA endpoint lain di proyek ini).
Tidak pernah ketauan karena nol test yang assert nama field di
endpoint ini (`{items: unknown[]}`), dan Phase 18 FE ini adalah
CONSUMER PERTAMA yang benar-benar pakai response-nya. Ditutup di
`organization_handler.ts` (tambah `toMemberRowResponse`), dikunci lewat
assertion field-shape eksplisit di test.

**Riset scope**: cuma ADA 3 endpoint organization-related di seluruh
backend — `GET /organizations/{id}/members`, `POST/GET /organizations/{id}/tutors`.
**TIDAK ADA endpoint generik "ubah role jadi X"** untuk role manapun
selain `tutor` — `teacher`/`curriculum_developer`/`reviewer`/dst tidak
pernah punya jalur assign (dikonfirmasi grep, konsisten dengan
ADR-0006's addendum yang sudah dicatat: `teacher` sengaja tidak pernah
di-assign endpoint manapun). Jadi UI "Kelola Anggota" ini SECARA JUJUR
cuma menawarkan 1 aksi (Jadikan Tutor) — bukan UI promosi role umum
yang berpura-pura lengkap.

**Temuan React nyata (bukan backend) pas verifikasi**: 1 user bisa
punya LEBIH dari 1 role di org yang sama (`user_organization_roles`'s
unique key `(user, org, role)`, BUKAN `(user, org)`) — daftar anggota
awalnya pakai `key={member.userId}` yang collide begitu seseorang
dipromosikan (muncul 2 baris, key sama) → React key warning nyata,
diperbaiki jadi `key={user_id}-{role}` (dites ulang, warning hilang).

**Dieksplisit DIDEFER**: undang anggota baru via email (tidak ada
endpoint "invite" — org membership cuma lewat auto-join siswa atau
assign tutor terhadap user_id yang SUDAH ada), hapus/turunkan role,
edit organisasi (nama/pengaturan), org switcher (akun dengan lebih
dari 1 org — UI ini pakai `roles[0]` seperti semua tempat lain).

## Ticket

### P18-001 — Backend fix: response shape member list
**Status:** done
**Depends on:** ADR-0006 (`organization_members:view`)
**Acceptance Criteria:**
- [x] `GET /organizations/{id}/members` balikin `user_id` (bukan `userId`), sesuai `api-contract.md` yang sudah lama
- [x] Field-shape dikunci lewat assertion test eksplisit
**DoD:** Test lama tetap hijau + assertion baru, 472/472 total, route-coverage 121/121 (tidak ada route baru — perbaikan shape).

### P18-002 — Halaman Organisasi: daftar anggota + jadikan tutor
**Status:** done
**Depends on:** P18-001, P9-001 (`POST /organizations/{id}/tutors`)
**Deskripsi:** `/organisasi` — daftar anggota dengan badge role, aksi "Jadikan Tutor" untuk anggota berrole `student`.
**Acceptance Criteria:**
- [x] Entry point dari dropdown TopBar, muncul cuma untuk `org_owner`/`academic_director`/`platform_admin`
- [x] UI jujur soal keterbatasan cakupan role (cuma tutor) — bukan berpura-pura "kelola role apa saja"
**DoD:** Diverifikasi end-to-end: promosi 1 anggota siswa jadi tutor, baris baru "Tutor" muncul berdampingan dengan baris "Pelajar" lama (bukan menggantikan — 2 role sekaligus itu valid).

### P18-003 — Integration check + exit checkpoint
**Status:** done
**Depends on:** P18-001 s/d P18-002
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit`/`lint`/`build` bersih di `titian-web`
- [x] `bun test` bersih di `titian-backend-bun` (472/472, tidak ada regresi)
**DoD:** Skrip seed sekali-pakai (1 owner + 2 siswa dalam 1 org sekolah, tidak dicommit) dipakai buat verifikasi, dihapus + data dibersihkan dari dev DB setelahnya.

---

## Checkpoint keluar Phase 18
1. [x] Admin organisasi bisa melihat semua anggotanya dengan nama asli (bukan lagi bug `userId` yang belum pernah kepakai FE mana pun).
2. [x] Admin bisa mempromosikan siswa jadi tutor lewat UI, dan hasilnya benar-benar tercermin (baris role baru muncul) tanpa reload manual.
3. [x] Non-admin (siswa) sama sekali tidak melihat entry point "Organisasi" di menu.

Phase 18 tertutup. Lanjut Phase 19 — Certificates Frontend.
