# Phase 22 (ticket-numbering) — Messaging System

## Keputusan scope (baca duluan)

Item ke-9 dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap di
`docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan semuanya'".
Digambarkan di sana sebagai "fondasi buat response-time reputation
P12-004, LMS messaging, nanti dipakai Collaborative Canvas juga".

**Tidak ada spesifikasi konkret di manapun** — `lms full.md` cuma
menyebut "messaging" 2 kali sebagai satu bullet dalam daftar fitur LMS
(baris 8772, 13852), tanpa skema, tanpa alur, tanpa detail apa pun.
Berbeda dari fase-fase lain yang punya contoh ilustratif eksplisit
(§37, §35-36), messaging di sini murni didesain dari nol memakai pola
yang sudah ada di proyek ini — bukan menerjemahkan spek yang hilang.

**Keputusan desain inti: 1 conversation per (cohort, student)**, bukan
DM bebas antar sembarang 2 user. Alasan: `enrollments`/`cohorts` sudah
jadi model relasi tutor↔siswa yang ADA dan punya otorisasi jelas
(`canManageCohorts`, `enrollmentRepository.findByCohortAndStudent`) —
dipakai ulang persis, bukan model relasi baru yang lepas dari LMS.
`conversations.tutor_id` diambil dari `learning_products.tutor_id`
saat dibuat (tidak berubah lagi — tidak ada fitur reassign tutor).
Konsekuensi jujur: **messaging fase ini SELALU dalam konteks 1 cohort
tertentu** — tidak ada "pesan umum ke platform admin" atau semacamnya,
itu di luar cakupan (LMS messaging, bukan support ticket system).

**Response-time reputation (P12-004's bagian yang didefer eksplisit,
lihat `docs/tickets/phase-12.md`) DITUTUP di ticket-phase ini juga**
(bukan sekadar "infra dibangun, dipakai nanti") — begitu ada data
message sungguhan, menghitungnya adalah pekerjaan kecil di atas yang
sudah dibangun, dan membiarkannya menganggur sampai fase entah kapan
di masa depan cuma menunda closure yang sudah bisa diselesaikan
sekarang.

**Privasi/visibilitas pesan SENGAJA lebih sempit dari
`canManageCohorts`'s cakupan biasa**: org_owner/academic_director
TIDAK otomatis bisa baca isi percakapan tutor↔siswa (beda dari
attendance/gradebook/assignment yang memang operasional dan boleh
dilihat admin org). Hanya `conversations.tutor_id`/`student_id` yang
bisa baca/kirim pesan di 1 conversation. `canManageCohorts` cuma
dipakai untuk 1 hal: staff MEMBUKA conversation ATAS NAMA seorang
siswa (skenario "tutor mulai chat duluan") — bukan untuk membaca isi
percakapan siapa pun. Visibilitas org-wide (misal admin audit pesan)
**dieksplisit DIDEFER**, dicatat di sini supaya tidak diasumsikan ada.

**Dieksplisit DIDEFER**: real-time delivery (WebSocket/SSE) — polling
biasa via React Query (interval refetch), sama seperti pola lain di
proyek ini yang tidak punya infra real-time. Read receipts UI granular
(centang 1/2) — cuma unread count sederhana. Attachment/gambar dalam
pesan — teks saja.

## Ticket

### P22-001 — Backend: Messaging core
**Status:** done
**Depends on:** P9-004 (`cohorts`), P9-003 (`learning_products`), P9-004 enrollments
**Tabel baru (additive):** `conversations`, `messages`.
**Endpoint baru:** `POST /cohorts/{id}/conversations`, `GET /conversations`, `GET /conversations/{id}/messages`, `POST /conversations/{id}/messages`, `POST /conversations/{id}/read`.
**Acceptance Criteria:**
- [x] Siswa buka conversation untuk cohort-nya sendiri (harus enrolled) — idempotent, tidak duplikat kalau dipanggil ulang
- [x] Tutor/manager buka conversation ATAS NAMA siswa tertentu (harus siswa itu enrolled di cohort tsb)
- [x] Kirim/baca pesan HANYA untuk peserta conversation (`tutor_id`/`student_id`) — bukan `canManageCohorts` yang lebih luas
- [x] `GET /conversations` balikin `unread_count` per conversation
**DoD:** test baru di `tests/messaging.test.ts`.

### P22-002 — Backend: response-time masuk ke Tutor Reputation
**Status:** done
**Depends on:** P22-001, P12-004 (`reputation_repository`)
**Deskripsi:** `GET /tutors/{id}/reputation` dapat 2 field baru: `avg_response_minutes`, `response_under_1h_rate` — dihitung dari jeda waktu pesan siswa pertama yang belum dijawab sampai balasan tutor berikutnya, di semua conversation tutor itu.
**Acceptance Criteria:**
- [x] Tutor belum punya conversation sama sekali → kedua field `null` (bukan `0`, beda makna dari "responnya selalu instan")
- [x] Beberapa balasan cepat + 1 lambat → rata-rata dan rate dihitung benar dari data nyata
**DoD:** test tambahan di `tests/messaging.test.ts` (bukan file terpisah — logic-nya nempel ke reputation yang sudah ada testnya sendiri).

### P22-003 — Frontend: inbox + thread + entry points
**Status:** done
**Depends on:** P22-001
**Deskripsi:** `/pesan` (daftar conversation, badge unread), `/pesan/[conversationId]` (thread + kirim pesan, polling). Entry point "Pesan" di dropdown TopBar. Tombol "Kirim Pesan" di roster siswa tutor (`tutor-class-view.tsx`) dan di sisi siswa (`student-class-view.tsx`).
**Acceptance Criteria:**
- [x] Badge unread di TopBar dan di daftar conversation cocok dengan data nyata (bukan hardcode)
- [x] Polling otomatis me-refresh thread yang sedang dibuka (interval React Query, bukan WebSocket)
**DoD:** Diverifikasi lewat `Bun.WebView` — lihat P22-004.

### P22-004 — Integration check + exit checkpoint
**Status:** done
**Depends on:** P22-001 s/d P22-003
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit`/`lint`/`build` bersih di `titian-web`
- [x] `bun test` bersih di `titian-backend-bun`, tidak ada regresi
**DoD:** Diverifikasi end-to-end lewat `Bun.WebView` — tutor buka percakapan dengan siswa, kirim pesan, siswa balas dari sisi lain, `GET /tutors/{id}/reputation` menunjukkan angka response-time nyata (bukan `null` lagi). Skrip seed sekali-pakai, dihapus + data dibersihkan setelah.

---

## Checkpoint keluar Phase 22
1. [x] Tutor dan siswa yang sama-sama terdaftar di 1 cohort bisa saling kirim pesan, dan pesan itu TIDAK bisa dibaca oleh siapa pun di luar keduanya (termasuk org admin — didokumentasikan sebagai batasan sengaja, bukan lupa).
2. [x] `GET /tutors/{id}/reputation` sekarang benar-benar menghitung response-time dari data pesan nyata, menutup gap yang eksplisit dicatat "didefer" sejak Phase 12.
3. [x] Unread count di UI (TopBar + daftar conversation) mencerminkan data nyata dari `read_at`, bukan simulasi.
4. [x] Keterbatasan (bukan real-time, bukan DM bebas, tidak ada visibilitas admin org atas isi pesan) didokumentasikan eksplisit.

Phase 22 tertutup. Lanjut Phase 23 — Marketplace kategori penuh + Learning Package.
