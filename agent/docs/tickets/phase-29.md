# Phase 29 (ticket-numbering) — Speaking Room (porting `speaking-main`)

## Keputusan scope (baca duluan)

Fitur baru di luar 14 item "kerjakan semuanya" dan di luar Phase 28 —
diminta eksplisit user: port aplikasi standalone di
`speaking-main/` (React SPA + Express, `@google/genai` langsung ke
Gemini) jadi fitur "Speaking Room" di Titian Asa, sesuaikan tema, dan
ganti TTS ke Gemini Flash TTS preview via OpenRouter.

**Apa itu `speaking-main`** (dikonfirmasi baca langsung, bukan asumsi):
ruang praktik percakapan AI bebas-topik — pilih bahasa → skenario →
tutor persona (nama/aksen/suara) → ngobrol via suara (Web Speech API,
fallback `MediaRecorder`+server-transcribe) atau teks → tiap giliran
dapat balasan tutor DALAM bahasa target + feedback analitis (koreksi
tata bahasa, kosakata, pelafalan, skor fluency, estimasi CEFR) → 2 mode
("Percakapan" langsung, atau "Belajar" yang muter feedback lisan
Bahasa Indonesia dulu baru balasan) → ringkasan skor sesi di akhir.
**Nol persistensi/auth** di app aslinya — murni React state + 4
endpoint Express stateless yang jadi proxy ke Gemini
(`/api/chat`, `/api/tts`, `/api/transcribe`, `/api/session-summary`).

**Keputusan bahasa — DITANYAKAN eksplisit ke user, dijawab: porting
semua 8 bahasa** (Inggris, Mandarin, Korea, Arab, Jepang, Prancis,
Spanyol, Jerman) — bukan cuma Inggris seperti fokus Titian Asa selama
ini. **Ini keputusan scope-platform yang nyata**: Titian Asa mulai
jadi platform multi-bahasa lewat fitur ini, bukan cuma "belajar Bahasa
Inggris". Konten (18 skenario, 15 tutor persona) + sistem prompt
lengkap dengan aturan skrip/transliterasi per-bahasa (Hanzi+Pinyin,
Hangul+Romanisasi, Hijaiyah+Latin, Kanji/Kana+Romaji, dst) di-porting
verbatim dari `speaking-main/src/data/`.

**Keputusan reuse infrastruktur AI — jangan bikin provider baru**:
- **TTS**: `AIProvider.synthesizeSpeech(text, voice, model)` yang SUDAH
  ADA (ADR-0010, endpoint OpenRouter `/audio/speech`) dipakai apa
  adanya — dikonfirmasi `google/gemini-3.1-flash-tts-preview` tersedia
  di endpoint OpenAI-Audio-Speech-compatible YANG SAMA yang sudah kita
  panggil untuk Kokoro. Cuma ganti `model`+`voice` (voice = nama voice
  Gemini per tutor persona: Kore/Puck/Zephyr/Fenrir/Charon), TIDAK ADA
  kode provider baru.
- **Transkripsi**: reuse `AIProvider.transcribe()` (Whisper via
  OpenRouter, ADR-0010) — TIDAK porting model transcribe Gemini
  terpisah dari app asli, Whisper sudah multi-bahasa.
- **Generate teks (giliran percakapan + ringkasan sesi)**: reuse
  `AIProvider.generate()` yang sudah ada. App asli pakai
  `responseSchema` native Gemini (constraint JSON di level API) — kita
  TIDAK punya itu di `generate()`, jadi pakai pola yang SUDAH established
  di seluruh codebase ini (`ai_content_service.ts` dst): instruksikan
  JSON di prompt, parse+`stripCodeFence`+validasi manual sesudahnya.
  Model default mengikuti config routing yang sudah ada (`~deepseek/...`)
  — BUKAN dipaksa Gemini (user cuma minta Gemini untuk AUDIO secara
  eksplisit) — bisa disetel lewat config kalau kualitas linguistik
  DeepSeek untuk 7 bahasa non-Inggris ternyata kurang, ini akan
  divalidasi lewat verifikasi live, bukan diasumsikan sempurna duluan.

**Keputusan arsitektur — TIDAK reuse `SpeakingRecorder`/`SpeakingAttempt`
(Phase 6)**: itu untuk lesson berstruktur 1-attempt-lalu-dinilai
(tertanam kurikulum). Speaking Room ini genuinely beda: percakapan
bebas multi-giliran tanpa kurikulum, jadi komponen rekam-audio
di-porting terpisah (mirror `speaking-main`'s Web-Speech-API-first,
`MediaRecorder`-fallback punya sendiri) — TIDAK ada tumpang tindih
penamaan/nol konflik dengan Phase 6.

**Keputusan persistensi — SENGAJA TIDAK ADA, sama seperti app asli**:
Speaking Room ini murni alat latihan bebas, TIDAK disimpan ke DB
(tidak ada tabel percakapan/attempt baru), TIDAK charge Diamond/credit,
TIDAK hook ke XP/streak/learning_events. Ini DIPUTUSKAN eksplisit di
sini (bukan lupa) — kalau nanti mau diintegrasikan ke progress
tracking/gamification, itu keputusan terpisah yang butuh didiskusikan
(skill_category mana, charge berapa credit, dst), bukan diam-diam
ditambahkan sekarang.

**Navigasi**: bottom nav sudah penuh (5 slot, pola berulang sejak
banyak fase sebelumnya) — entry point baru sebagai card di `/beranda`
atau `/latihan`, bukan slot bottom-nav baru. Route baru: `/speaking-room`.

## Ticket

### P29-001 — Backend: endpoint generate + TTS + summary
**Depends on:** ADR-0010 (`AIProvider`), P1-011 (OpenRouter)
**Endpoint baru** (auth wajib, tanpa charge credit — lihat "Keputusan
scope"): `POST /speaking-room/turn`, `POST /speaking-room/tts`,
`POST /speaking-room/summary`. Transkripsi audio reuse endpoint upload
asset yang sudah ada + `AIProvider.transcribe()` langsung (tidak perlu
endpoint baru — cek dulu apakah butuh endpoint transcribe generik baru
atau bisa reuse existing).
**Config baru**: `AI_SPEAKING_ROOM_TTS_MODEL` (default
`google/gemini-3.1-flash-tts-preview`), `AI_SPEAKING_ROOM_TEXT_MODEL`
(default ikut model default yang sudah ada).

### P29-002 — Frontend: porting UI + tema Titian Asa
**Depends on:** P29-001
Porting seluruh komponen (`ConversationView`, `AudioInputControls`,
`FeedbackPanel`, `Header`, 4 modal selector) + data (`languages`,
`scenarios`, `tutors`) dari `speaking-main/src/` ke
`titian-web/src/components/speaking-room/` + `src/app/(app)/speaking-room/`,
disesuaikan ke palet warna/tipografi/komponen `ui/` Titian Asa yang
sudah ada (bukan style Tailwind mentah dari app asli).

### P29-003 — Integration check + exit checkpoint
`bunx tsc --noEmit`/`lint`/`build` bersih, `bun test` bersih, diverifikasi
lewat `Bun.WebView`: pilih bahasa → percakapan 1 giliran (suara ATAU
teks) → balasan+feedback muncul → audio TTS Gemini benar terdengar →
ringkasan sesi tergenerate.

---

## Checkpoint keluar Phase 29
1. [x] Semua 8 bahasa bisa dipilih dan menghasilkan percakapan yang
   masuk akal (skrip/transliterasi benar per bahasa).
2. [x] TTS pakai `google/gemini-3.1-flash-tts-preview` via OpenRouter,
   bukan Kokoro/browser-fallback (kecuali API gagal, fallback tetap ada).
3. [x] Nol perubahan ke `SpeakingRecorder`/`SpeakingAttempt`/`ai_speaking_evaluation_service`
   (Phase 6) — Speaking Room genuinely terpisah.
4. [x] Nol persistensi DB ditambahkan (sesuai keputusan sengaja di atas).

## Temuan live-testing pasca-port (P29-004)

Setelah porting selesai dan dites manual, 3 bug nyata ditemukan lewat
smoke test langsung ke provider (bukan diasumsikan) — dua di antaranya
berdampak ke SELURUH aplikasi, bukan cuma Speaking Room:

**1. `maxTokens` hardcoded terlalu kecil (2048, lalu 4096)** —
`deepseek/deepseek-v4-flash-latest` adalah model reasoning yang bisa
menghabiskan SELURUH budget `max_tokens` untuk reasoning tersembunyi
sebelum sempat menulis jawaban terlihat, muncul sebagai error "empty or
null completion content". OpenRouter's `/api/v1/models` melaporkan
limit asli model ini: 131072. Instruksi eksplisit user: jangan tebak
angka baru, buat otomatis menyesuaikan model — jadi ini dijadikan
`resolveMaxTokens(model, fallback)` di `ai_provider.ts` (fetch
`/api/v1/models` sekali, di-cache in-process, fallback kalau gagal).
Instruksi eksplisit user kedua: jadikan default untuk SEMUA pemanggilan
AI di aplikasi — diterapkan ke 7 titik: `speaking_room_service.ts` (x2),
`ai_gateway_service.ts`, `ai_writing_evaluation_service.ts`,
`ai_speaking_evaluation_service.ts`, `ai_content_service.ts` (x2),
`ai_ocr_service.ts`.

**2. Reasoning model membocorkan chain-of-thought ke `content`** — bug
BERBEDA dari #1, ditemukan lewat smoke test bahasa Arab: bahkan dengan
`maxTokens` besar, model kadang menulis narasi
deliberasi/draft-ulang berbahasa Inggris LANGSUNG ke field `content`
(bercampur dengan JSON duplikat/rusak), bukan ke field `reasoning`
terpisah yang sudah disediakan OpenRouter — gagal parse ("Expected
'}'"). Dikonfirmasi lewat A/B test langsung: menambahkan
`response_format: {type: "json_object"}` (grammar-constrained decoding
di sisi OpenRouter) membuat prompt Arab yang SAMA persis berhasil
parse bersih. **Batasan penting yang juga dikonfirmasi lewat tes**:
mode ini memaksa top-level JSON jadi OBJECT — sebuah array yang diminta
di prompt akan DIAM-DIAM diubah jadi object oleh model. Jadi
`jsonMode: true` (field baru di `GenerationRequest`, `ai_provider.ts`)
HANYA dipasang di 5 titik yang outputnya object
(`ai_gateway_service.ts`, `ai_writing_evaluation_service.ts`,
`ai_speaking_evaluation_service.ts`, `speaking_room_service.ts` x2) —
SENGAJA TIDAK dipasang di `ai_content_service.ts`'s question
generation atau `ai_ocr_service.ts`, keduanya butuh top-level array.

**3. Latensi turn generation 50-170+ detik, independen dari
`maxTokens`** — dites langsung lewat `Bun.WebView` (`resource timings`
browser mencatat 165102ms untuk satu turn bahasa Inggris) dan lewat
perbandingan `max_tokens` 131072 vs 8192 vs 4096 (50s/58s/117s — tidak
berkorelasi rapi dengan besarnya ceiling, jadi BUKAN efek dari
`resolveMaxTokens`). Ini karakteristik inheren model `~deepseek/...`
lewat OpenRouter, bukan bug kode. **Ini akar penyebab laporan user
"audio masih pakai browser TTS, belum Gemini"**: request TTS baru
jalan SETELAH turn text selesai — dengan jeda 50-170+ detik dari klik
awal user, Chrome tidak lagi menganggap `audio.play()` terprogram itu
dipicu oleh user gesture yang masih segar, jadi promise-nya ditolak dan
kode fallback ke `speakWithBrowserSynthesis`. Perbaikan kode terkait:
`requestGeminiTts` sebelumnya diam-diam menelan SEMUA `ApiError` tanpa
log — sekarang semua jalur gagal (network DAN backend 4xx/5xx) di-log
lewat `console.warn`, plus deteksi respons non-audio (size 0 atau
content-type bukan `audio/*`). Backend TTS endpoint sendiri sudah
diverifikasi 100% berfungsi lewat curl langsung (WAV valid, 24kHz/16-bit/
mono). **Belum diputuskan**: apakah ganti model default Speaking Room
ke sesuatu yang lebih cepat (trade-off kualitas linguistik 7 bahasa
non-Inggris vs latensi) — dilaporkan ke user sebagai temuan, bukan
diputuskan sepihak.

**4. Feedback Bahasa Indonesia sekarang muncul di chat, bukan cuma
audio** — di app sumber (`speaking-main`), `spokenFeedbackIndonesian`
ditempel ke pesan asisten itu sendiri dan dirender sebagai panel
ber-highlight DI DALAM bubble percakapan (bukan cuma diputar sebagai
audio atau disembunyikan di feedback sheet). Diporting persis ke
`message-bubble.tsx` (panel amber dengan tombol putar terpisah) +
`page.tsx` (field baru `spokenFeedbackIndonesian` pada
`SpeakingRoomMessage`, hanya diisi saat `mode === "study"`).
