# ALR — Roadmap Pembangunan + Pembagian AI Agent

Disusun dari `lms_full.md`. Prinsip yang dipegang: **MVP kecil, arsitektur besar** — data model harus generic sejak awal walau yang di-build duluan cuma English Pre-Basic → C2.

Stack yang sudah locked di dokumen: Next.js (web) + React Native (mobile) di atas satu ALR API, Rust + Axum (backend), PostgreSQL, Redis, Cloudflare R2, Google Auth, AI Gateway (provider-agnostic, DeepSeek sebagai daily driver), monorepo.

> **Update (2026-08-30, lihat ADR-0009 dan `docs/STATE.md`):** backend di-migrasi total dari Rust+Axum ke **Bun+ElysiaJS** (Drizzle ORM) — keputusan eksplisit user, bukan deviasi diam-diam. Struktur repo juga sudah berubah dari monorepo jadi repo terpisah per app sejak sesi P0-009 (lihat `docs/STATE.md`'s "Struktur repo"). Baris "locked" di atas dibiarkan apa adanya sebagai catatan sejarah rencana awal — jangan dianggap masih berlaku begitu saja, cek `docs/STATE.md` untuk stack yang sungguhan berjalan sekarang.

---

## FASE 0 — Kunci Arsitektur Sebelum Coding (1–3 minggu)

Ini bagian yang menurut dokumen **belum boleh di-lock tapi wajib selesai sebelum baris kode pertama**, karena semua fase berikutnya bergantung padanya:

1. **Canonical Data Model / ERD** — Organization, User, Role, Curriculum, Level, Unit, Lesson, Concept, Skill, Content, Block, Question, Question Bank, Assessment, Attempt, Mastery, Learning Event, Class, Cohort, Enrollment, Credit, Transaction, dst.
2. **Mastery Algorithm** — formula awal (boleh sederhana, tapi harus config-driven supaya gampang diubah tanpa migrasi besar).
3. **FRSS/SRS Algorithm** — interval, decay, recall probability, scheduling.
4. **AI Gateway design** — Task → Cost estimation → Model selection → Prompt → Context retrieval → Generation → Validation → Usage tracking.
5. **Credit Economy** — unit, pricing, mapping ke cost AI, subscription allowance, anti-abuse.
6. **RBAC** — Platform Admin → Org Owner → Academic Director → Curriculum Developer → Reviewer → Teacher/Tutor → Student → Parent.
7. **Content Versioning** — version → publish → attempt → migration.
8. **Mobile architecture** — Expo vs bare RN, offline mode, sync, local DB.

**Output fase ini:** kumpulan ADR (Architecture Decision Record) + ERD final, bukan kode.

**Agent:** *Architecture Agent* — diberi seluruh `lms_full.md` sebagai konteks, tugasnya menuliskan ADR per topik di atas dan draft ERD (SQL DDL). Manusia me-review dan menyetujui tiap ADR sebelum lanjut — jangan biarkan agent men-generate skema lalu langsung dipakai backend agent tanpa review, karena keputusan di fase ini mengunci semua fase berikutnya.

---

## FASE 1 — Fondasi Platform (skeleton yang bisa jalan end-to-end)

Tujuan: bukan fitur lengkap, tapi *satu jalur tipis* dari login sampai "user mengerjakan 1 soal" berjalan nyata.

1. Monorepo scaffold: `apps/web` (Next.js), `apps/mobile` (React Native), `apps/api` (Rust/Axum), `packages/shared` (types, schemas, API client).
2. Google Auth + entity User/Organization/Role minimal.
3. PostgreSQL schema v1 dari ERD Fase 0 (migration tooling — misal `sqlx` migrate).
4. Redis untuk session/cache.
5. Cloudflare R2 untuk asset (audio, gambar).
6. AI Gateway v1: abstraction layer + DeepSeek adapter, dengan logging Credit/Task supaya tidak hardcode ke satu provider.
7. CI/CD (lint, test, build, deploy), observability dasar (logging, error tracking).

**Agents:**
- *Backend/Infra Agent* (Rust/Axum) — implementasi API, migration, auth middleware.
- *DevOps Agent* — CI/CD, container, deployment pipeline ke staging.
- *Frontend Skeleton Agent* — Next.js shell (routing, auth flow, API client dari `packages/shared`).

Fase ini selesai kalau: user bisa login, hit satu endpoint terproteksi, dan dapat response dari AI Gateway (misal generate 1 kalimat contoh).

---

## FASE 2 — Content Engine & Curriculum Pipeline

Ini fase kunci karena isi silabus Pre-Basic→C2 yang sudah kalian tulis di file ini akan jadi **bahan input**, bukan ditulis manual satu-satu.

1. Content schema: ALR Learning Markdown (ALM) + Semantic AST.
2. Question Bank + Question Schema yang extensible (MCQ, fill-blank, matching, drag-drop, dst — semua tipe yang sudah dilist di bagian "Sistem Latihan ALR").
3. Content Block SDK (kontrak agar Next.js & React Native sama-sama bisa render block interaktif tanpa masing-masing ngerti Markdown).
4. Curriculum Blueprint + Curriculum Constitution (aturan konsistensi yang jadi "rel" untuk AI generator).
5. Content Memory / RAG — supaya AI generator tidak perlu dikirimi semua modul sekaligus.
6. AI Content Generation pipeline: **Blueprint → Generate → Validate → QA Agent → Human Review → Publish.**

**Agents:**
- *Content Pipeline Agent* — membangun editor WYSIWYG, paste normalizer, parser ALM→AST.
- *Curriculum Generation Agent* — pakai isi silabus di `lms_full.md` (Pre-Basic s/d C2, tiap modul: vocab/grammar/pronunciation/listening/speaking/reading/writing) sebagai blueprint, generate materi + soal per unit secara batch, unit demi unit, bukan sekaligus.
- *Content QA Agent* — cek konsistensi (grammar terminology, level CEFR, format soal sesuai schema) sebelum masuk ke antrean review manusia.
- *Human reviewer* (tutor/curriculum developer) tetap wajib approve sebelum publish — jangan auto-publish.

**Validasi:** jangan generate seluruh silabus sekaligus. Mulai dari 1 modul Pre-Basic penuh (Learn→Practice→Speaking→Writing→Review→Assessment) untuk memvalidasi pipeline, baru scale ke modul berikutnya secara paralel.

---

## FASE 3 — Core Learning Loop

1. Learning Event (setiap interaksi tercatat sebagai event).
2. Mastery engine (implementasi formula dari ADR Fase 0).
3. FRSS/SRS engine (jadwal review otomatis).
4. Knowledge Graph + Prerequisite Graph (concept-level, bukan cuma unit-level).
5. Personal Recommendation / weakness detection dasar.

**Agents:** *Learning Engine Agent* (Rust) untuk implementasi mastery/FRSS sebagai service terpisah dari content engine; *Algorithm Tuning Agent* (boleh Python untuk eksperimen offline sebelum diporting ke Rust).

---

## FASE 4 — Exercise Engine & 4 Skills

1. Exercise engine generik yang men-drive semua tipe latihan (vocab, grammar, listening, speaking, reading, writing) dari Question Bank Fase 2.
2. Speaking/pronunciation AI scoring (lewat AI Gateway).
3. Writing evaluation: Evaluation sebagai entity terpisah dari Feedback/Annotation (sesuai desain di dokumen), berbasis rubric.

**Agents:** *Frontend Interactive Agent* (render Content Block SDK jadi UI nyata di web+mobile), *AI Evaluation Agent* (prompt + rubric untuk scoring writing/speaking).

---

## FASE 5 — Assessment / Exam Engine

1. Exam Runtime Engine (session, delivery, timer, submission) — dipisah total dari Proctoring Engine sejak awal skema DB.
2. Level Assessment per CEFR.
3. (Setelah MVP English stabil) baru masuk IELTS/TOEFL/PTE-specific generators — ini masuk **Phase 2 roadmap fitur** di dokumen, jangan digabung ke MVP awal.

---

## FASE 6 — Gamification & Economy

XP/Mastery/Coin dipisah, Diamond/credit ledger, leaderboard bertingkat (bukan satu leaderboard global), streak, achievement, personal mission, wallet ledger untuk tutor.

**Agent:** *Product/Growth Agent* untuk implementasi ini — relatif independen, bisa jalan paralel dengan Fase 4–5.

---

## FASE 7 — Mobile (React Native)

Baru serius digarap setelah web MVP jalan dan `packages/shared` stabil: offline mode, local DB + sync, audio recording untuk speaking, push notification.

---

## FASE 8 — Organization / LMS / Marketplace

RBAC penuh, class management (cohort, enrollment, attendance, sertifikat), tutor marketplace (kelas privat/grup, split revenue 30/70), payment (QRIS).

---

## FASE 9 — Proctoring (paling akhir, paling sensitif)

Proctoring Policy per tier exam, Event Collector (camera/mic/screen/fullscreen/focus), Risk Engine (signal → score, **bukan** auto-decision), dashboard human review, Evidence storage. Privacy/consent/retention/encryption/audit **wajib** didesain bersamaan, bukan ditambahkan belakangan — ini sudah eksplisit di dokumen kalian sendiri.

---

## FASE 10+ — Scale ke domain lain

Bahasa lain (Jepang, Mandarin), mata pelajaran lain (Matematika, Sains), jenjang sekolah (SD/SMP/SMA, Cambridge). Kalau data model Fase 0 memang generic, fase ini seharusnya jadi **isi konten baru**, bukan **rombak arsitektur**.

---

## Cara mengorganisir AI Agent untuk development (ringkas)

| Peran Agent | Tanggung jawab | Kapan aktif |
|---|---|---|
| Orchestrator/Planning Agent | Pecah tiap fase jadi ticket, urutkan dependency | Terus-menerus |
| Architecture Agent | ADR, ERD, review desain sebelum implementasi | Fase 0, & tiap kali ada perubahan skema besar |
| Backend Agent (Rust/Axum) | Implementasi API, service layer | Fase 1–5 |
| Frontend Web Agent (Next.js) | UI web, integrasi Content Block SDK | Fase 1, 2, 4 |
| Mobile Agent (React Native) | Port UI ke mobile, offline/sync | Fase 7 |
| Curriculum Generation Agent | Generate materi & soal dari blueprint silabus | Fase 2, jalan terus paralel dgn fase lain |
| Content QA Agent | Validasi konsistensi konten sebelum human review | Setiap batch konten baru |
| AI Evaluation Agent | Prompt+rubric untuk scoring writing/speaking | Fase 4 |
| DevOps Agent | CI/CD, infra, observability | Fase 1, terus berjalan |
| QA/Test Agent | Test otomatis tiap PR, regression pada schema | Terus-menerus mulai Fase 1 |

**Prinsip kunci:** agent boleh generate cepat, tapi ada **gerbang manusia** di 3 titik yang tidak boleh dilewati otomatis — approve ADR (Fase 0), publish konten kurikulum (Fase 2), dan keputusan proctoring/risk (Fase 9). Semua titik itu memang sudah kalian tandai eksplisit di dokumen sebagai "jangan auto-*".

---

## Saran titik mulai paling praktis (kalau mau langsung jalan minggu ini)

1. Selesaikan ADR Fase 0 (bisa dibantu Architecture Agent, tapi kalian yang approve).
2. Scaffold monorepo + auth + 1 endpoint AI Gateway.
3. Generate & publish **1 modul penuh** Pre-Basic (Module 1 — Alphabet) lewat pipeline Fase 2, end-to-end sampai bisa dikerjakan user di web.
4. Baru dari situ pipeline di-scale ke modul-modul berikutnya secara paralel sambil Fase 3 (learning loop) dan Fase 4 (exercise engine) dibangun.

Ini memvalidasi seluruh arsitektur (data model, content pipeline, learning engine, AI gateway) dengan risiko kecil sebelum kalian commit generate ratusan unit sampai C2.
