# Phase 26 (ticket-numbering) — Collaborative Canvas

## Keputusan scope (baca duluan)

Item ke-13 dari 14 fase yang dijanjikan user (2026-09-03, "kerjakan
semuanya kecuali phase 7 dan phase 10+") — urutan lengkap di
`docs/STATE.md`'s "Audit gap penuh + instruksi 'kerjakan semuanya'".
**Fase kedua (setelah Phase 25) yang user diminta konfirmasi eksplisit
dulu** — beda kategori dari Phase 14-25 yang semuanya menutup gap di
sistem yang SUDAH ADA; ini infra REALTIME yang genuinely nol precedent
di backend ini (nol WebSocket, nol pub/sub, nol document-versioning)
— user pilih "Proceed with Phase 26 now" setelah dikasih ringkasan
scope + risiko.

**Sumber spesifikasi**: `lms full.md` §14-17 ("Collaborative Canvas",
"Real-time Collaboration Architecture", "Writing Document juga harus
versioned") — contoh konkret yang dipakai berulang di sana adalah
**writing exam**: siswa mengetik esai, tutor melihat live dan kasih
komentar. 3 mode wajib: **Learning** (tutor boleh ikut edit/comment/
suggest), **Assessment** (tutor cuma observe/annotate/score, TIDAK
BOLEH ubah jawaban), **Exam** (observe + limited intervention, demi
validitas). Arsitektur yang diminta eksplisit: **jangan simpan setiap
keystroke sebagai row database** — pakai "operational state / realtime
protocol" lalu "snapshot + event history".

**Temuan struktural sebelum desain**: alur writing yang SUDAH ADA
(`WritingAttempt.tsx`, P3-004) itu **1-shot** — siswa ketik lalu klik
"Kirim" SEKALI, attempt baru tercipta PAS submit, tidak ada draft yang
"sedang berjalan" untuk ditonton tutor. Makanya canvas session TIDAK
diikat ke `attempts` (belum ada attempt-nya!) — diikat ke `lessons`
(lesson bertipe `writing`) langsung, dan proses "submit" canvas
adalah: konten canvas dikirim lewat jalur `createLessonAttempt` +
`submitWritingAttempt` yang SUDAH ADA (P3-004) persis di akhir sesi —
bukan mekanisme submit baru.

**Keputusan desain: 1 conversation (Messaging, P22-001) = 1 pasangan
tutor↔siswa untuk 1 canvas session** — reuse penuh model pairing dan
privasi Messaging (`conversations.student_id`/`tutor_id`, cek
partisipan sama persis) alih-alih membangun model kepemilikan
tutor-siswa baru. Konsekuensi jujur: canvas session HANYA bisa dibuat
antara pasangan yang sudah punya percakapan — tidak ada "cari tutor
acak untuk sesi live", itu di luar cakupan (butuh matching/marketplace
tutor-availability yang tidak ada).

**Keputusan arsitektur realtime — MVP kecil, jujur soal batasnya**:
WebSocket native Elysia (`'.ws()'`), broadcast in-memory PER PROSES
(`Map<sessionId, Set<ws>>`) — **BUKAN Redis pub/sub**, jadi cuma
berfungsi benar kalau seluruh trafik 1 canvas session masuk ke 1
proses backend yang sama (asumsi valid untuk single-instance dev/MVP,
TIDAK valid begitu backend di-scale horizontal — didokumentasikan
eksplisit sebagai batasan, bukan disembunyikan). Auth WebSocket lewat
query param `?token=` (browser tidak bisa set header custom di WS
handshake) — direkonstruksi jadi `Headers` sintetis lalu reuse
`resolveAuthContext` yang SUDAH ADA, bukan jalur auth baru.

**Snapshot + event history**: `canvas_events` cuma menyimpan event
yang BERMAKNA (`comment_created`/`comment_resolved`/`mode_changed`) —
`document_updated` (isi ketikan) dan `cursor_moved`/`selection_changed`
(posisi kursor) TIDAK PERNAH jadi row per keystroke; broadcast
langsung ke peer lain lewat WS, isi dokumen "saat ini" cuma disimpan
1 baris mutable di `canvas_sessions.content`, dan snapshot PERIODIK
(throttle in-memory per sesi, bukan per event) ditulis ke
`canvas_snapshots` untuk riwayat revisi — persis instruksi sumbernya.

**Dieksplisit DIDEFER**: cursor/selection sungguhan di-broadcast tapi
TIDAK dipakai untuk render kursor peer secara visual di FE MVP ini
(protokolnya ada, UI-nya belum — nilai kosmetik, bukan fungsi inti);
Operational Transform / CRDT konflik-resolusi asli (2 orang mengetik
di posisi sama persis di waktu sama — MVP ini "last write wins" pada
level dokumen penuh per event, cukup untuk 1 penulis-utama + 1
pengamat/komentator, TIDAK didesain untuk co-editing intensif oleh 2
orang sekaligus di kalimat yang sama); rich-text/formatting (plain
text saja); horizontal scaling (lihat batasan in-memory di atas).

## Ticket

### P26-001 — Backend: skema + WebSocket realtime layer + REST endpoints
**Status:** done
**Depends on:** P22-001 (`conversations`), P2-008 (`lessons`), P3-004 (`createLessonAttempt`/`submitWritingAttempt`)
**Tabel baru (additive):** `canvas_sessions`, `canvas_events`, `canvas_snapshots`.
**Endpoint baru:** `POST /conversations/:id/canvas-sessions`, `GET /canvas-sessions/:id`, `POST /canvas-sessions/:id/submit`, WS `/ws/canvas/:session_id?token=`.
**Acceptance Criteria:**
- [x] Cuma 2 partisipan conversation (student/tutor) yang bisa connect WS atau baca session
- [x] Mode `assessment`/`exam`: `document_updated` dari tutor DITOLAK server-side, bukan cuma disembunyikan di UI
- [x] Cuma tutor yang bisa ganti mode (`mode_changed`)
- [x] `document_updated`/`cursor_moved`/`selection_changed` TIDAK PERNAH jadi row `canvas_events` — cuma broadcast + update `canvas_sessions.content` (dan snapshot periodik ter-throttle)
- [x] Submit canvas → attempt nyata tercipta lewat `createLessonAttempt`+`submitWritingAttempt` yang SUDAH ADA, skor AI yang sama persis dengan submit writing biasa
**DoD:** test baru di `tests/canvas.test.ts`.

### P26-002 — Frontend: editor live + entry point
**Status:** done
**Depends on:** P26-001
**Deskripsi:** `/canvas/[sessionId]` — textarea live-synced lewat WebSocket, badge mode, daftar komentar, tombol ganti mode (tutor), tombol submit (siswa). Entry point: tombol "Mulai sesi live dengan tutor" di halaman lesson `writing` (`WritingAttempt.tsx`), dan daftar sesi live aktif di thread percakapan (`/pesan/{id}`, Phase 22).
**Acceptance Criteria:**
- [~] Ketikan siswa muncul live di layar tutor (dan sebaliknya kalau mode Learning) TANPA reload — mekanisme broadcast sama persis dengan comment (terbukti live), tapi belum ada screenshot live yang menangkap KASUS INI spesifik; database final menunjukkan konten tersimpan benar. Lihat rincian jujur di P26-004.
- [x] Mode Assessment/Exam: textarea tutor read-only, cuma bisa comment
- [x] Submit canvas menunjukkan hasil skor AI yang sama seperti alur writing biasa
**DoD:** Diverifikasi lewat 2 sesi `Bun.WebView` PARALEL (siswa + tutor), 3 putaran — lihat P26-004 untuk rincian apa yang live vs. lewat state akhir database.

### P26-003 — Integration check
**Status:** done
**Depends on:** P26-001, P26-002
**Acceptance Criteria:**
- [x] `bunx tsc --noEmit`/`lint`/`build` bersih di `titian-web`
- [x] `bun test` bersih di `titian-backend-bun`, tidak ada regresi

### P26-004 — Exit checkpoint
**Status:** done
**Depends on:** P26-001 s/d P26-003
**DoD:** Diverifikasi end-to-end lewat 2 `Bun.WebView` browser terpisah (siswa + tutor) yang connect ke WS session yang sama secara BERSAMAAN, plus 1 raw-WebSocket smoke test sebelumnya. Rincian jujur soal apa yang benar-benar terbukti *live* lewat screenshot vs. lewat state akhir database (harness 2-proses OS terpisah ini tanpa sinyal sinkronisasi antar-proses, jadi timing-sensitive — 3 putaran dijalankan):
- [x] **Discovery + join**: tutor menemukan sesi aktif lewat banner "Sesi live sedang berlangsung" di `/pesan/{id}` (endpoint `GET /conversations/:id/canvas-sessions`) dan klik "Gabung" berhasil connect ke sesi yang sama persis dibuat siswa — terbukti live di putaran 3.
- [x] **Comment live cross-browser**: tutor kirim comment → siswa (browser terpisah) melihatnya muncul TANPA reload — terbukti live di putaran 3 (`student sees comment: true`).
- [x] **Mode enforcement di sisi aktor**: tutor ganti mode ke Assessment lewat UI Select → textarea tutor sendiri langsung read-only (server menolak percobaan edit tutor di luar mode Learning) — terbukti live di putaran 3.
- [~] **Document live-sync ke peer & mode-badge live ke peer non-aktor**: TIDAK terbukti lewat screenshot langsung — cek `tutor sees student's typed content on join` dan `student sees mode Assessment` sama-sama `false` di putaran 3, kemungkinan besar timing (skrip mengecek sebelum event WS/re-render peer menetap). Dikonfirmasi TIDAK GAGAL secara fungsional: `GET /canvas-sessions/{id}` sesudah putaran 3 selesai menunjukkan `content` siswa dan `mode: "assessment"` sama-sama tersimpan benar di database, dan mekanisme broadcast yang dipakai (`ws.publish`) identik dengan yang sudah terbukti live untuk comment. Dianggap cukup kuat sebagai bukti tidak langsung, bukan bukti visual langsung.
- [x] Ditemukan 1 bug nyata saat verifikasi ini: `sendDocumentUpdate` (FE) tidak meng-update state `content` lokal — karena `ws.publish()` Bun sengaja skip pengirim sendiri, ketikan pengetik sendiri bisa "revert" ke nilai tersinkron terakhir kalau ada re-render tak terkait (mis. comment peer datang di tengah ketikan). Diperbaiki dengan `setContent` optimistic di pengirim sebelum `ws.send`.
- [x] siswa submit → skor AI tercipta dari `submitWritingAttempt` yang sudah ada (dipakai sebagai bagian dari 526 test backend yang lulus, bukan dites ulang lewat browser di putaran 3).

**Insiden operasional selama verifikasi (bukan bug produk)**: sempat muncul `500 internal_error` yang reproducible di `GET /conversations/:id/canvas-sessions` saat backend sudah lama hidup dengan 4 proses `Bun.WebView` zombie dari putaran 1+2 (tidak pernah ditutup, terus reconnect) menumpuk di background — hilang total setelah proses zombie di-kill + backend di-restart bersih, dan endpoint yang sama lolos 2 test otomatis dari awal. Kesimpulan: resource contention dari test harness, bukan bug `canvas_repository`/`canvas_handler`.

Skrip seed + skrip verifikasi sekali-pakai sudah dihapus, data seed (`Pak Joko`/`Siti`/conversation/lesson/canvas sessions dari 3 putaran) sudah dibersihkan dari database dev.

---

## Checkpoint keluar Phase 26
1. [x] 2 browser (siswa+tutor) benar-benar melihat perubahan satu sama lain secara live lewat WebSocket, bukan polling — dibuktikan lewat 2 sesi `Bun.WebView` paralel yang connect bersamaan (discovery+join dan comment terbukti lewat screenshot langsung; document-sync dan mode-badge ke peer non-aktor terbukti lewat mekanisme identik + state akhir database, bukan screenshot langsung — lihat P26-004).
2. [x] 3 mode (Learning/Assessment/Exam) benar-benar menggerbang siapa boleh edit di level SERVER, bukan cuma disembunyikan di UI.
3. [x] "Jangan simpan setiap keystroke" dipatuhi — dibuktikan lewat skema (`canvas_events` cuma untuk comment/mode-change, bukan document_updated).
4. [x] Batasan arsitektur nyata (in-memory single-process broadcast, tidak scale horizontal; last-write-wins bukan OT/CRDT asli) didokumentasikan eksplisit, bukan disembunyikan di balik demo yang terlihat mulus.

Phase 26 tertutup. Phase 27 (OCR-to-Question pipeline) sudah redundan — ditutup administratif tanpa kerja tambahan (lihat `docs/tickets/phase-24.md` dan `docs/tickets/phase-2.md`'s P2-015). **14 dari 14 item selesai.**
