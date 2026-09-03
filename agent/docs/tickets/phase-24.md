# Phase 24 (ticket-numbering) — AI Content Generation Pipeline + Content Factory

## Keputusan scope (baca duluan)

Item ke-11 dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap di
`docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan semuanya'".

**Temuan utama SEBELUM menulis kode apa pun: sebagian besar fase ini
SUDAH SELESAI sejak Phase 2**, bukan gap yang perlu dibangun ulang.
Riset (agent Explore + verifikasi manual langsung baca kode) menemukan:

- **"Blueprint → Generate → Validate → QA Agent → Human Review →
  Publish"** (roadmap-Fase-2 poin 6, alasan utama fase ini ada di
  daftar) **SUDAH ADA PENUH** sejak P2-013 (`ai_content_service.ts`:
  `generateLesson`/`generateQuestions`, blueprint typed struct bukan
  free-text) + P2-014 (`content_qa_service.ts`, QA Agent otomatis di
  `submit-review`) + P2-005 (publish flow draft→in_review→published).
  Backend-nya LIVE, dipakai nyata sejak P2-016's validasi 1 modul
  penuh.
- **UI trigger-nya JUGA SUDAH ADA** — awalnya dikira belum (laporan
  riset pertama keliru bilang "Studio pure manual-authoring CRUD"),
  ternyata SALAH setelah dibaca langsung:
  `titian-web/src/components/studio/add-lesson-dialog.tsx` dan
  `add-question-dialog.tsx` SUDAH punya tab "Generate dengan AI" yang
  lengkap (form blueprint → `aiApi.generateLesson`/`generateQuestions`
  → hasil masuk sebagai draft). QA report (`qa_report.passed`/`issues`)
  SUDAH ditampilkan di `studio/lessons/[id]/page.tsx` dan
  `studio/question-banks/[id]/page.tsx`. **Pelajaran untuk sesi ini
  sendiri**: jangan percaya laporan riset generik tanpa verifikasi
  langsung baca file — grep yang salah scope (cuma cek
  `src/app/(app)/studio/`, padahal Studio ada di `src/app/studio/`,
  DAN dialog komponennya di `src/components/studio/`, bukan di
  halaman) nyaris membuat fase ini membangun ulang sesuatu yang sudah
  jadi.

**Yang genuinely masih kosong, setelah verifikasi ulang manual**:
1. **OCR-to-Question (P2-015) TIDAK PUNYA FRONTEND SAMA SEKALI** —
   dikonfirmasi grep `ocr` di seluruh `titian-web/src`: nol hasil.
   Backend-nya (`ai_ocr_service.ts`) sudah lengkap dan teruji
   (7 unit test) tapi tidak ada jalan manapun di UI untuk memicunya.
2. **Tidak ada provenance** — tidak ada kolom apa pun di `lessons`/
   `questions` yang mencatat "ini dibuat AI atau manusia". Satu-satunya
   jejak ada di tabel audit `ai_tasks` yang terpisah, tidak pernah
   di-JOIN balik ke `lessons`/`questions`. Reviewer yang membuka detail
   lesson/soal tidak tahu itu hasil generate atau tulisan manual tanpa
   buka tabel lain.
3. **OCR belum pernah diverifikasi sukses lewat model vision ASLI** —
   dicatat sejak `docs/tickets/phase-2.md`: 1 percobaan live sempat
   gagal `HTTP 404` (guardrail privasi akun OpenRouter, bukan bug
   kode). Belum pernah dicoba ulang.

**Scope fase ini jadi jauh lebih kecil dari nama "Content Factory"
yang terdengar besar** — cuma menutup 3 gap konkret di atas, BUKAN
membangun ulang pipeline yang sudah ada.

## Ticket

### P24-001 — Backend: provenance `generated_by` di lessons & questions
**Status:** done
**Depends on:** P2-013, P2-015
**Kolom baru (additive):** `lessons.generated_by`, `questions.generated_by` — CHECK IN ('human','ai'), default 'human'.
**Acceptance Criteria:**
- [x] Baris lama (dibuat sebelum ticket ini) otomatis 'human' — tidak ada perubahan makna
- [x] `generateLesson`/`generateQuestions`/`ocrToQuestion` set `generated_by='ai'` saat insert
- [x] Endpoint baca lesson/question yang sudah ada balikin field ini (tanpa endpoint baru)
**DoD:** test tambahan di file test AI yang sudah ada (bukan file baru — nempel ke suite yang relevan).

### P24-002 — Frontend: OCR-to-Question UI
**Status:** done
**Depends on:** P24-001, P2-015, P2-010 (`driveApi.uploadAsset`)
**Deskripsi:** Tab ke-3 "OCR dari gambar" di `AddQuestionDialog` (sejajar "Tulis manual"/"Generate dengan AI" yang sudah ada) — upload gambar (reuse `driveApi.uploadAsset` langsung, tidak perlu ke halaman Media dulu) → `POST /ai/ocr-to-question` → hasil (draft, dengan flag `ocr_verification`/`ocr_uncertain_type` di `qa_report`) masuk daftar soal yang sudah ada, direview lewat alur submit-review/publish yang SUDAH ADA (tidak ada UI review baru dibangun).
**Acceptance Criteria:**
- [x] Badge "AI" (dari `generated_by`) tampil di baris soal hasil OCR, sama seperti hasil generate teks
- [x] `qa_report.issues` OCR (verifikasi terhadap gambar sumber) tetap tampil lewat komponen QA report yang sudah ada, tidak diduplikasi
**DoD:** Diverifikasi lewat `Bun.WebView` — lihat P24-004.

### P24-003 — Percobaan ulang verifikasi OCR lewat model vision asli
**Status:** done — **BERHASIL, gap lama akhirnya tertutup**
**Depends on:** P2-015
**Deskripsi:** Coba ulang panggilan live ke `AI_OCR_MODEL` (default `deepseek/deepseek-v4-flash-vision-exp` via OpenRouter) dengan gambar sungguhan (dibuat sintetis via PIL: "1. I ___ a student. a) am b) is c) are" — bukan hasil scan asli, tapi gambar nyata dikirim ke model vision nyata, bukan simulasi).
**Catatan hasil:** **SUKSES** — beda dari kegagalan `HTTP 404` yang dicatat di `phase-2.md`. Model membaca gambar dengan benar: `ocr_raw_text` "1. I ___ a student\na) am b) is c) are" persis sama dengan isi gambar, diklasifikasi `type=mcq` dengan confidence (TIDAK ada `ocr_uncertain_type`), `data.options` `["am","is","are"]` terekstrak benar, `qa_report.issues` cuma `ocr_verification` (wajib review manual) seperti didesain — bukan uncertain-type. Kemungkinan guardrail privasi akun OpenRouter yang tercatat sebelumnya sudah tidak berlaku lagi (user mungkin sudah mengubah setting-nya di luar sesi ini, atau endpoint model sudah berubah ketersediaan) — **penyebab pastinya tidak diketahui, cuma hasilnya yang dikonfirmasi: real, sukses, end-to-end**. Item ini DIHAPUS dari `docs/STATE.md`'s "Item lepas" (sebelumnya poin 3), bukan didiamkan sebagai masih terbuka.

### P24-004 — Integration check + exit checkpoint
**Status:** done
**Depends on:** P24-001 s/d P24-003
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit`/`lint`/`build` bersih di `titian-web`
- [x] `bun test` bersih di `titian-backend-bun`, tidak ada regresi
**DoD:** Diverifikasi end-to-end lewat `Bun.WebView` — curriculum_developer upload gambar soal sintetis ("1. I ___ a student. a) am b) is c) are") → trigger OCR → **model vision ASLI berhasil membaca dan mengekstrak soal MCQ dengan benar** (lihat P24-003) → soal draft muncul di daftar dengan badge AI + badge status QA (icon X karena `qa_report.passed=false`, sesuai desain "selalu wajib verifikasi manual") → alur review yang sudah ada (submit-review/publish) tetap jalan tanpa perubahan. Skrip seed sekali-pakai, dihapus + data dibersihkan setelah.

---

## Checkpoint keluar Phase 24
1. [x] Ditemukan lebih dulu, sebelum menulis kode: pipeline generate→QA→review→publish (roadmap-Fase-2 poin 6) sudah lengkap sejak Phase 2 — fase ini TIDAK membangun ulang, cuma menutup 2 gap frontend nyata (OCR UI) + 1 gap data (provenance).
2. [x] OCR-to-Question sekarang punya jalan UI penuh, DAN untuk pertama kalinya berhasil diverifikasi sukses lewat model vision ASLI (gap yang tercatat terbuka sejak Phase 2 — akhirnya tertutup, bukan cuma didokumentasikan ulang sebagai gagal).
3. [x] Setiap lesson/soal sekarang bisa dibedakan asalnya (AI vs manusia) tanpa perlu buka tabel `ai_tasks` terpisah.

Phase 24 tertutup. Lanjut Phase 25 — Generate konten kurikulum asli (mulai 1 modul Pre-Basic penuh).
