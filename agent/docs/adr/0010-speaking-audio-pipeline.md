# ADR-0010: Speaking / Audio Pipeline — STT (Whisper) + TTS (Kokoro), both via OpenRouter

Status: Accepted
Date: 2026-09-02
Supersedes: -
Superseded by: -

## Context

Roadmap-Fase-4 §4.1 (AI Tutor, 3 mode) / §4.2 (AI Speaking Engine, 5-dimensi scoring) — the "Speaking" skill of ALR's "4 Skills" promise — has never been built. Confirmed by direct code search before this ADR: zero code anywhere in `titian-backend-bun`/`titian-web` handles audio recording, upload-for-transcription, speech-to-text, or text-to-speech. The only audio-adjacent thing that exists is `block_schema.ts`'s `audio` **content block** (P2-xxx) — a playback embed for a pre-uploaded audio asset in lesson content, unrelated to recording/transcribing a learner's spoken answer.

ADR-0004 (AI Gateway Design) already anticipated this gap — its routing table has a `SpeakingEvaluation` row noting "deepseek (dgn audio transcript dulu)" — but never specified *how* the transcript gets produced, and no code ever implemented that task type (`ai_gateway_service.ts`'s `POST /ai/evaluate` only supports `task === "grammar_evaluation"` today; writing evaluation was built as its own dedicated service outside this generic gateway, and speaking follows that same precedent — see Decision below).

User explicitly directed the provider choice rather than leaving it open: **STT via Whisper, TTS via Kokoro, both through OpenRouter** (the same provider this codebase already routes all AI Gateway/text-generation traffic through, `OPENROUTER_API_KEY` already configured).

## Decision

### Providers, confirmed by live smoke test against the real OpenRouter API (not docs alone)

- **STT: `openai/whisper-1`** via `POST https://openrouter.ai/api/v1/audio/transcriptions` (multipart form-data: `file`, `model`, optional `language`/`response_format`). **`openai/whisper-large-v3` was tried first and rejected** — a live test against a real ~3.7s Kokoro-generated clip had `whisper-large-v3` report `duration: 1.125` and transcribe only `"Hello."` (truncating the rest of the sentence silently, no error), while `whisper-1` transcribed the same file completely and correctly (`"Hello. Welcome to our restaurant. What would you like to order?"`). This is a live-provider defect, not a hypothetical — `whisper-large-v3` must not be used until re-verified.
- **TTS: `hexgrad/kokoro-82m`** via `POST https://openrouter.ai/api/v1/audio/speech` (JSON body: `model`, `input`, `voice`, `response_format: "mp3"`). Confirmed live: returns real `audio/mpeg` bytes, playable MP3. Voice roster (54 voices, confirmed via `GET /api/v1/models?output_modalities=speech`'s `supported_voices` field) is `{af,am}_*` (American female/male), `{bf,bm}_*` (British female/male), plus other languages — default voice for the AI Tutor is `af_bella` (confirmed working in the smoke test), overridable via config like every other model choice in this codebase.

### `AIProvider` interface gets 2 new methods, additive (ADR-0004's abstraction, not a new one)
```typescript
interface AIProvider {
  generate(req: GenerationRequest): Promise<GenerationResponse>;   // unchanged
  transcribe(audio: Uint8Array, mimeType: string): Promise<string>;             // NEW
  synthesizeSpeech(text: string, voice: string): Promise<{ bytes: Uint8Array; contentType: string }>; // NEW
}
```
`DeepSeekProvider` (the name stays — it's "the OpenRouter-backed provider", not literally DeepSeek-only; see ADR-0004's own routing table already sending different task types to different models under this one provider) implements both against the endpoints above. `FakeAIProvider` (test double) gets fake implementations returning canned transcripts/silent audio bytes — same pattern as its existing `generate()` fake.

### Audio storage — reuses the existing Drive/asset pipeline, no new subsystem
A learner's recorded answer is uploaded exactly like any other asset (`POST /assets/presigned-upload` → direct-to-R2 PUT → `POST /assets/confirm`, P1-010/P2-010's existing flow) and referenced by `asset_id`. No new storage code, no new bucket, no new upload endpoint.

### Evaluation flow mirrors P3-004's writing evaluation exactly, not the generic `/ai/evaluate` stub
`POST /attempts/{id}/submit`'s body gets one more optional field, `answer_audio_asset_id` (alongside the existing `answers`/`answer_text`), for `lessons.type = 'speaking'` attempts — reusing the same lesson-attempt dispatch P3-004 built (handler branches on `lesson_id`/`assessment_id` + lesson type), not a new attempt type. A new `ai_speaking_evaluation_service.ts` (sibling to `ai_writing_evaluation_service.ts`, not a modification of it): resolve the asset via `drivePermissions` (same access-check as `ai_ocr_service.ts`) → `aiProvider.transcribe()` → feed the transcript into a rubric-based text evaluation using the **same `rubrics`/`evaluations`/`feedback` tables** P3-004 already uses (ADR-0001's Evaluation/Feedback separation already anticipated this — no schema change). Rubric criteria: `grammar`, `vocabulary`, `fluency`, `naturalness`, `pronunciation` — 5 dimensions per §4.2, each a separate field (never one blended score), matching the roadmap's own explicit requirement.

### Pronunciation — an honest MVP limitation, not faked
§4.2 describes real phoneme-level scoring (per-word % + target IPA, e.g. `word: comfortable, score: 68%, target: /ˈkʌmf.tə.bəl/`). **A text transcript cannot produce that** — phoneme comparison needs acoustic analysis, which is out of scope for a transcript-based pipeline. MVP approximates pronunciation using Whisper's own per-segment confidence (`avg_logprob`/`no_speech_prob`, available via `response_format: verbose_json`) as a *weak proxy* for "how clearly the model heard each word" — explicitly documented in the rubric/prompt and to the learner as an approximation, never presented as true phoneme-target scoring. If real acoustic pronunciation scoring is wanted later, that's a separate ADR (a dedicated pronunciation-scoring provider/model, not Whisper).

### AI Tutor conversational mode (§4.1) — text-authored prompts, TTS-voiced, not live-generated dialogue
The "AI mulai percakapan kontekstual" opening line is authored content (a lesson's `speaking` block data, same authoring pattern as every other block type), synthesized to audio via Kokoro at request time (not pre-rendered/stored — cheap and always fresh, per Kokoro's per-character pricing). The learner's spoken reply goes through the same transcribe+evaluate path above; "Correction" and "Try Again" are the evaluation's own feedback replayed to the UI, optionally also voiced via a second TTS call. This is a scripted single-turn AI Tutor exchange, not an open-ended live conversation engine (that's out of scope here — no such requirement was made this session).

### Config — new fields, same pattern as every existing AI model config field
`aiSttModel` (default `openai/whisper-1`), `aiTtsModel` (default `hexgrad/kokoro-82m`), `aiTtsDefaultVoice` (default `af_bella`) — env-overridable, live in `config.ts` next to `aiWritingEvaluationModel` etc.

## Consequences

- Speaking becomes the 4th of the "4 Skills" to have a real evaluation pipeline (after MCQ/fill_blank/matching auto-grading, and writing) — closes roadmap-Fase-4's last substantive gap besides Kids Mode/Micro Learning (both explicitly lower-priority per the roadmap's own MVP-first ordering).
- New per-attempt cost: 1 STT call (`$0.006/min` for `whisper-1`) + 1 text-evaluation call (existing deepseek pricing) + (AI Tutor mode only) 1-2 TTS calls (`$0.62/M chars`, a spoken sentence is pennies) — all platform cost, **not charged to the learner's credits**, following `ai_writing_evaluation_service.ts`'s own precedent exactly (confirmed by reading it: zero `economyRepository`/credit references anywhere in that file — evaluating a submission is core learning-loop cost, not a discretionary AI action like lesson/question generation, which is the category ADR-0005's credit charges actually target).
- Pronunciation scoring is explicitly approximate (confidence-proxy, not phoneme-target) until a dedicated acoustic-analysis ADR supersedes this one — must stay visible in the UI/rubric text, not silently upgraded to look like real phoneme scoring later without re-deciding.
- `whisper-large-v3`'s truncation defect (found live, not assumed) means it must not be swapped in as a "better" default without re-verifying against a real multi-sentence clip first — noted here so a future session doesn't "upgrade" back into the same bug.
