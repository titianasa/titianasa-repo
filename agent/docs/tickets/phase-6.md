# Phase 6 — Speaking / AI Tutor (roadmap-Fase-4's last skill)

Depends on: Phase 4 checkpoint terpenuhi penuh (`docs/tickets/phase-4.md`, 224 test lulus, 2026-09-02). **Bukan tergantung Phase 5** (`docs/tickets/phase-5.md`, Retrieval Variation + prerequisite integration) — Phase 5 sudah ditulis lebih dulu tapi belum dikerjakan; ticket ini **menyalip** karena keputusan eksplisit user (lihat "Keputusan scope"). Phase 5 tetap valid, tinggal dikerjakan setelah ini.

Sumber utama breakdown ini: `agent/ALR_Phase_Detail_Breakdown.md`'s `## PHASE 4 — Exercise Engine & 4 Skills` §4.1 (AI Tutor) + §4.2 (AI Speaking Engine). Keputusan provider ada di **ADR-0010** (`agent/docs/adr/0010-speaking-audio-pipeline.md`) — baca itu dulu sebelum baca ticket ini, semua detail teknis STT/TTS ada di sana, tidak diulang di sini.

## Keputusan scope (baca duluan)

Sesi sebelumnya menutup Phase 4 lalu menulis `docs/tickets/phase-5.md` (Retrieval Variation + prerequisite integration — scope paling kecil dari 3 opsi yang ditawarkan). **User langsung membalas dengan keputusan provider eksplisit** untuk salah satu dari 2 opsi yang sebelumnya ditunda (Speaking + AI Tutor): "stt pakai whisper, tts pakai kokoro, semua pakai openrouter" — lalu instruksi eksplisit "kerjakan". Ini keputusan langsung dari user, bukan hasil riset+tanya seperti transisi fase sebelumnya — tapi tetap didahului riset (ADR-0010) buat memverifikasi provider itu benar-benar bisa dipakai (bukan asumsi), termasuk 1 temuan nyata: `openai/whisper-large-v3` ternyata cacat (transkrip terpotong diam-diam di clip nyata yang dites), jadi default yang dipakai adalah `openai/whisper-1`.

**Kenapa file ini `phase-6.md`, bukan menimpa `phase-5.md`:** `phase-5.md` sudah ditulis lengkap dan sudah dikomunikasikan ke user dengan nomor ticket P5-001/002/003 di sesi sebelumnya — mengubahnya sekarang akan bikin riwayat dokumen membingungkan. Ticket ini nomornya lanjut (`phase-6.md`), isinya menyalip di urutan pengerjaan (dikerjakan sebelum P5-00X), bukan menggantikan.

**§4.4 (Kids Mode) dan §4.5 (Micro Learning) TETAP tidak termasuk** — §4.4 eksplisit ditunda roadmap-nya sendiri ("tunda kalau target awal bukan Kids", belum dikonfirmasi user itu targetnya). §4.5 depends ke Personal Learning Queue (P4-002, sudah ada) tapi murni soal slotting jadwal, tidak terkait audio pipeline — kandidat terpisah, bukan bagian "Speaking" secara substansi.

## Ringkasan teknis (detail lengkap di ADR-0010)

- **STT**: `openai/whisper-1` lewat OpenRouter, `POST /api/v1/audio/transcriptions`, multipart form-data.
- **TTS**: `hexgrad/kokoro-82m` lewat OpenRouter, `POST /api/v1/audio/speech`, JSON body, balikin `audio/mpeg` mentah. Voice default `af_bella` (dari 54 voice yang ada, dikonfirmasi lewat `/api/v1/models?output_modalities=speech`).
- **Storage**: reuse pipeline asset/Drive yang sudah ada (`POST /assets/presigned-upload` → `POST /assets/confirm`) — tidak ada storage baru.
- **Evaluasi**: mirror `ai_writing_evaluation_service.ts` (P3-004) persis — service baru terpisah (bukan modifikasi file itu), rubric baru 5 kriteria (`grammar`/`vocabulary`/`fluency`/`naturalness`/`pronunciation`), reuse tabel `rubrics`/`evaluations`/`feedback` yang sudah ada sejak Phase 0. Tidak charge kredit — mengikuti persis precedent `ai_writing_evaluation_service.ts` (dikonfirmasi baca kodenya: nol referensi `economyRepository` di situ).
- **Pronunciation**: **keterbatasan MVP yang jujur, bukan dipalsukan** — skor phoneme-level asli (target IPA per kata) butuh analisis akustik yang di luar scope transcript-based pipeline ini. MVP approksimasi lewat confidence Whisper sendiri (`avg_logprob`/`no_speech_prob` dari `response_format: verbose_json`) — didokumentasikan eksplisit di rubric/prompt/UI sebagai approksimasi, tidak pernah diklaim sebagai scoring fonem asli.

## Ticket

### P6-001 — AIProvider audio capabilities: `transcribe` + `synthesizeSpeech`
**Status:** todo
**Depends on:** ADR-0010
**Endpoint baru:** tidak ada — perluasan interface `AIProvider` (`src/service/ai_provider.ts`), dipakai internal oleh ticket berikutnya.
**Deskripsi:** Fondasi murni — belum ada fitur produk yang kelihatan di sini, cuma kemampuan provider baru yang dites langsung (bukan diasumsikan jalan dari dokumentasi OpenRouter saja).
**Acceptance Criteria:**
- [ ] `AIProvider` interface (`ai_provider.ts`) dapat 2 method baru: `transcribe(audio: Uint8Array, mimeType: string): Promise<string>` dan `synthesizeSpeech(text: string, voice: string): Promise<{bytes: Uint8Array, contentType: string}>` — additive, `generate()` tidak berubah
- [ ] `DeepSeekProvider` implementasi `transcribe` — POST multipart ke `https://openrouter.ai/api/v1/audio/transcriptions`, `model: config.aiSttModel`, balikin `response.text`
- [ ] `DeepSeekProvider` implementasi `synthesizeSpeech` — POST JSON ke `https://openrouter.ai/api/v1/audio/speech`, `model: config.aiTtsModel`, `response_format: "mp3"`, balikin bytes mentah + `content-type` dari response header
- [ ] `FakeAIProvider` (test double) dapat implementasi fake buat keduanya — `transcribe` balikin string yang bisa diset per-test (pola sama seperti `generate`'s fake response queue yang sudah ada), `synthesizeSpeech` balikin byte array kecil apa adanya (tidak perlu MP3 asli buat test)
- [ ] Config baru: `aiSttModel` (default `openai/whisper-1`), `aiTtsModel` (default `hexgrad/kokoro-82m`), `aiTtsDefaultVoice` (default `af_bella`) — pola persis field AI model lain yang sudah ada
**DoD:** test backend baru (`ai-provider-audio.test.ts`) via `FakeAIProvider`. **Verifikasi manual sekali lewat provider ASLI** (curl/script, bukan bagian test suite yang di-commit — sama precedent P2-013/P3-004): `synthesizeSpeech` balikin MP3 yang valid (dicek `file` command), `transcribe` atas hasil `synthesizeSpeech` itu balikin teks yang cocok.

### P6-002 — Speaking attempt: submission + rubric-based AI evaluation (Practice mode)
**Status:** todo
**Depends on:** P6-001, P3-004 (`loadSubmittableAttempt`, pola `ai_writing_evaluation_service.ts` yang di-mirror persis)
**Endpoint baru:** tidak ada endpoint baru — perluasan `POST /attempts/{id}/submit` yang sudah ada (P3-004), body dapat 1 field opsional baru.
**Deskripsi:** Mode "Practice" §4.1 — siswa rekam jawaban audio buat 1 lesson bertipe `speaking`, dievaluasi 5 dimensi. Belum termasuk mode "AI Conversation" penuh (itu P6-003) — ini fondasi evaluasi-nya duluan, sama urutan P3-004 (submission+evaluation) mendahului P3-005 (integrasi UI penuh).
**Acceptance Criteria:**
- [ ] `assessment_repository` dapat `submitSpeakingLessonAttempt(db, id, audioAssetId, submittedAt)` — sibling function baru dari `submitLessonAttempt` yang sudah ada (bukan modifikasi), simpan `answers: {audio_asset_id: audioAssetId}`
- [ ] `POST /attempts/{id}/submit`'s body schema dapat field opsional baru `answer_audio_asset_id: t.Optional(t.String())`, di samping `answers`/`answer_text` yang sudah ada
- [ ] Handler dispatch (`assessment_handler.ts`'s `postSubmit`, sudah bercabang lesson_id/assessment_id sejak P3-004) diperluas: lesson bertipe `speaking` + `answer_audio_asset_id` ada → panggil service baru
- [ ] Service baru `ai_speaking_evaluation_service.ts` (bukan modifikasi `ai_writing_evaluation_service.ts`): resolve asset lewat `drivePermissions` (pola sama `ai_ocr_service.ts`) → `aiProvider.transcribe()` → prompt evaluasi 5 kriteria (`grammar`/`vocabulary`/`fluency`/`naturalness`/`pronunciation`, pronunciation eksplisit disebut approksimasi di system prompt) → tulis `evaluations`+`feedback` (rubric baru `SPEAKING_RUBRIC_ID`, `ensure`-idempotent pola sama `WRITING_RUBRIC_ID`)
- [ ] **Gerbang manusia sama persis P3-004**: attempt selalu `submitted` dulu (audio asset id tersimpan) sebelum evaluasi dicoba; kalau STT atau evaluasi gagal, attempt TETAP `submitted` (bukan hilang), `evaluation: null` di response, bukan error ke caller
- [ ] Tidak charge kredit — konsisten P3-004
**DoD:** test backend baru (`ai-speaking-evaluation.test.ts`, `FakeAIProvider`) — submit sukses → transcript+scores+feedback tersimpan; STT gagal → attempt tetap `submitted`, `evaluation: null`; parse output AI gagal → sama; asset bukan milik caller → 403/404 (pola akses `ai_ocr_service.ts`). **Verifikasi manual lewat provider ASLI**: rekam/upload 1 audio nyata (bisa pakai `synthesizeSpeech` dari P6-001 buat generate audio uji kalau tidak ada mic asli), submit lewat endpoint asli, cek transcript+scores masuk akal.

### P6-003 — AI Tutor: percakapan kontekstual + Correction + Try Again (§4.1's 3 mode)
**Status:** todo
**Depends on:** P6-001 (TTS), P6-002 (evaluasi)
**Endpoint baru:** tidak ada — komposisi dari yang sudah ada (P6-001's `synthesizeSpeech` + P6-002's evaluasi), dipanggil via handler yang sama.
**Deskripsi:** §4.1 — AI mulai percakapan kontekstual (teks yang sudah diautorisasi sebagai bagian content lesson, disuarakan lewat TTS saat diminta, **bukan digenerate live**), siswa jawab lewat rekaman, AI kasih skor + koreksi ("Better: ...") + opsi "Try Again".
**Acceptance Criteria:**
- [ ] Endpoint baru `GET /lessons/{id}/speaking-prompt-audio` (atau serupa) — ambil teks prompt dari `content_blocks` lesson itu (block type baru atau field yang sudah ada, DIPUTUSKAN saat implementasi berdasar struktur block yang paling pas), sintesis lewat `synthesizeSpeech`, balikin audio (atau URL asset kalau di-cache — keputusan implementasi, bukan didesain ulang di ticket ini)
- [ ] Response evaluasi P6-002 diperluas menyertakan 1 kalimat "Correction" yang jelas kalau skor grammar/naturalness di bawah threshold (reuse feedback yang sudah dihasilkan evaluasi, bukan pemanggilan AI kedua)
- [ ] "Try Again" bukan endpoint baru — cuma alur FE: submit attempt baru untuk lesson yang sama (pola sama seperti "Coba lagi" `QuestionCheck` P3-002 sudah punya)
**DoD:** test backend baru untuk endpoint prompt-audio. Verifikasi manual: buka 1 lesson speaking, dengar prompt (lewat browser), rekam jawaban sengaja salah tata bahasa, dapat correction yang masuk akal.

### P6-004 — FE: rekam audio + layar Speaking Attempt + AI Tutor
**Status:** todo
**Depends on:** P6-002, P6-003
**Deskripsi:** Sisi learner — `titian-web` belum punya cara merekam audio sama sekali. Mirror `WritingAttempt` (P3-004) tapi input-nya rekaman, bukan textarea.
**Acceptance Criteria:**
- [ ] Komponen baru `SpeakingRecorder` — `MediaRecorder` browser API, rekam → preview playback → "Kirim" (upload lewat presigned-upload flow yang sudah ada, submit attempt)
- [ ] Komponen baru `SpeakingAttempt` (mirror `WritingAttempt`) — pakai `SpeakingRecorder`, tampilkan hasil 5 skor terpisah + feedback + catatan approksimasi pronunciation
- [ ] Halaman lesson viewer (`(app)/belajar/[lessonId]/page.tsx`, sudah render `WritingAttempt` untuk `type==='writing'`) diperluas render `SpeakingAttempt` untuk `type==='speaking'`
- [ ] AI Tutor: tombol "Dengarkan" memutar audio prompt (P6-003), lalu alur rekam-jawab-koreksi-coba lagi yang sama
**DoD:** verifikasi browser lewat `Bun.WebView` — TIDAK bisa merekam mic asli di headless browser, jadi verifikasi upload-path pakai file audio yang sudah disiapkan (mis. hasil `synthesizeSpeech`) di-inject lewat `evaluate()`/CDP file-input simulation, bukan `getUserMedia` sungguhan (dicatat sebagai keterbatasan verifikasi headless, bukan bug produk) — atau, kalau itu tidak praktis, verifikasi manual sekali oleh user sendiri di browser asli dengan mic (dicatat eksplisit di STATE.md kalau ini rutenya).

### P6-005 — Integration test suite + exit checkpoint
**Status:** todo
**Depends on:** semua di atas
**Deskripsi:** Pola sama seperti tiap ticket-phase sebelumnya — cross-check route coverage, checkpoint end-to-end. Tidak ada checkpoint eksplisit dari sumber untuk §4.1/§4.2 (beda dari §3.x yang punya teks checkpoint tertulis) — ditulis sendiri berdasar apa yang benar-benar dibangun.
**Acceptance Criteria:**
- [ ] Route-coverage audit (`grep`-based, pola sama semua ticket-phase sebelumnya)
- [ ] Checkpoint baru (lihat di bawah)
**DoD:** `bun test` hijau penuh.

---

## Checkpoint keluar Phase 6 (harus bisa didemo, bukan asumsi)
1. [ ] Siswa buka 1 lesson `speaking`, kirim jawaban lewat audio (rekaman asli atau upload), dapat kembali 5 skor terpisah (grammar/vocabulary/fluency/naturalness/pronunciation) — bukan 1 angka gabungan.
2. [ ] Skor pronunciation secara eksplisit ditandai approksimasi di UI, bukan diklaim scoring fonem asli.
3. [ ] AI Tutor: siswa dengar prompt AI (audio nyata, bukan cuma teks), jawab, dapat correction yang relevan, bisa "Try Again".
4. [ ] Kegagalan STT/evaluasi AI tidak pernah menghilangkan submission siswa — attempt tetap `submitted`, sama persis gerbang manusia P3-004.
5. [ ] `openai/whisper-1` dipakai (bukan `whisper-large-v3`, yang dikonfirmasi cacat lewat smoke test ADR-0010) — dicek langsung dari config, bukan diasumsikan.

Kalau salah satu poin di atas belum jalan end-to-end, jangan lanjut ke P5-00X (Retrieval Variation + prerequisite integration, sudah ditulis tapi ditunda) walau ticket lain kelihatan sudah "done".

---

## Strategi eksekusi (urutan sesi yang disarankan)

| Sesi | Ticket | Fokus | Kenapa dikelompokkan begini |
|---|---|---|---|
| 1 | P6-001 | AIProvider audio capabilities (backend, fondasi) | Semua ticket lain butuh ini duluan — tidak ada fitur produk yang bisa dites tanpa `transcribe`/`synthesizeSpeech` jalan. |
| 2 | P6-002 | Speaking attempt submission + evaluasi (backend) | Baru masuk akal setelah P6-001. Mirror P3-004 persis, jadi risiko desain rendah. |
| 3 | P6-003 | AI Tutor: prompt audio + correction + try again (backend) | Komposisi P6-001+P6-002, bukan infra baru. |
| 4 | P6-004 | FE: rekam audio + layar Speaking + AI Tutor | Baru masuk akal setelah backend-nya lengkap (P6-002+P6-003). |
| 5 | P6-005 | Test suite + checkpoint | Penutup fase, pola sama semua ticket-phase sebelumnya. |

**Total 5 sesi.** Setelah ini selesai, lanjut ke `docs/tickets/phase-5.md` (P5-001/002/003, sudah ditulis, ditunda karena user menyalip prioritas ke Speaking) kecuali user reprioritas lagi.
