# Tiket Pare-7 — Percakapan suara (voice note & live)

> **Catatan migrasi backend (2026-10-05, ADR-0020):** backend sedang dipindah ke Go. Tiket ini ditulis untuk `titian-backend-rust`, dan kode Rust tetap yang aktif sampai domain ini diport (G14, lihat `phase-51-go-migration.md`). Pekerjaan yang belum dieksekusi: bila G14 sudah selesai saat tiket ini dikerjakan, kerjakan di `titian-backend-go` (`#[sqlx::test]` → test Go dengan `testdb.New`, `services/x.rs` → `internal/<domain>/`); bila belum, kerjakan di Rust dan catat endpoint/migrasi barunya di daftar paritas fase 51.

📋 **RENCANA (2026-09-25)** — keputusan user: gerbang hubungan = sudah saling membalas chat; STT = **bawaan browser** (server hanya menilai teks); bahasa mengikuti zona secara ketat (kampung = bahasanya; Kampung Bahasa & Camp = en/ko/zh/ja/ar saja); Google Chrome; voice note (audio + transkrip) disimpan 3 hari; live tidak disimpan sama sekali. Masih terbuka: [ADR-0017 §11](../adr/0017-percakapan-suara-pare.md) no. 1, 4, 6, 7. Belum ada kode. Urutan: setelah Pare-5 (PWA/push) dan Pare-6 (Vercel); **7a (voice note)** dulu, **7b (live)** kemudian.

Repo yang disentuh: `titian-backend-rust` (endpoint `/pare/voice/*`, pesan `voice_invite` di `/ws/pare`, penilaian transkrip, migrasi `pare_voice_*` dari **0087** (0084 dipakai Pare-8, 0085 push, 0086 gender pemain)), `alr/game` (UI rekam/panggil), infrastruktur baru hanya untuk 7b (LiveKit + TURN di VM GCP `pare-voice`). `titian-web` tidak disentuh, kecuali antrean tinjauan di Admin Pusat (P7-010).

## Aturan main eksekusi
Sama seperti Pare-1…4: migrasi aditif & idempoten, sinkron `domain-model.md` & `api-contract.md`, test integrasi `#[sqlx::test]` per tiket, verifikasi browser sungguhan (minta izin user sebelum membuat token QA / data uji, hapus setelahnya), jangan commit tanpa diminta, waktu harian WIB. Penalti suara **dinyalakan hanya setelah mode shadow** menghasilkan ambang yang dikalibrasi dengan data nyata.

## Yang WAJIB dipertahankan
- Suara hanya di percakapan **Personal & Grup** (tidak di Kampung Bahasa / saluran).
- **Live hanya bila semua peserta ≥ A2 pada bahasa percakapan**; level lebih rendah = voice note.
- Kunci/angka kelayakan dari server; FE tidak memutuskan gerbang.
- **Live: tidak ada audio maupun transkrip yang disimpan di backend.** Voice note: audio + transkrip dihapus setelah **3 hari**.
- Bahasa mengikuti zona pembicara (ketat): kampung = bahasanya; Kampung Bahasa dan Camp = Inggris/Korea/Mandarin/Jepang/Arab; Indonesia/bahasa lain = pelanggaran. Di Kampung Bahasa pemain memilih salah satu dari 5 bahasa sebelum bicara (pengenal suara browser butuh satu bahasa).

---

# Pare-7a — Voice note

> **2026-09-26 — evaluasi bahasa dari transkrip dilepas sementara (permintaan pemilik produk).** P7-004 (penilaian transkrip, STT di server), P7-005 (strike/penalti/kunci otomatis) dan P7-010 (pengawasan transkrip live) **tidak lagi berjalan**: voice note & panggilan tidak ditranskrip/dinilai; klien tidak lagi memakai SpeechRecognition (jadi rekam suara & telepon jalan di semua browser dengan mikrofon, bukan hanya Chrome); persetujuan tidak lagi menyebut penyedia AI. Kode lama diarsipkan di `titian-backend-rust/attic/pare-voice-evaluation/` (backend + tes + FE) untuk dipulihkan nanti. Yang tetap: P7-001…003, 006…009, 011 (dan tabel lama tidak dihapus). **Panggilan live dibuka untuk semua level** (`voice.liveMinLevel` = 0; gerbang level tetap ada di kode) **tetapi dibatasi waktu per hari menurut level**: Basic 10 mnt, A1-setara 15, A2-setara 20, B1-setara ke atas 30 (`voice.liveDailyMinutes`; angka B1+ adalah asumsi, ubah di konten bila perlu).

## P7-001 — Skema & konfigurasi gerbang (M)
Migrasi `0087_pare_voice.sql`: `pare_voice_consents(user_id, version, accepted_at)`, `pare_voice_notes(id, conversation_id, user_id, lang, object_key, mime, duration_ms, status[pending|transcribed|failed|expired], expires_at, created_at)`, `pare_voice_transcripts(id, note_id|segment_id, user_id, lang_target, text, detected_lang, confidence, verdict jsonb, created_at)`, `pare_voice_strikes(id, user_id, ref, kind, created_at)`, `pare_voice_locks(user_id, until, reason)`, `pare_blocks(user_id, blocked_id)`; `pare_messages.kind text not null default 'text'` + `voice_note_id`. `content.json` → `voice: {live_min_level: {en, zh, ar, ja, ko}, note_max_seconds, retention_days: 3}`.
**DoD:** migrasi idempoten di DB kosong; constraint diuji; konfigurasi dimuat & divalidasi saat start.

## P7-002 — Kelayakan & persetujuan (M)
`GET /pare/voice/eligibility?lang=&conversation=` → `{consent, note: {allowed, reason}, live: {allowed, reason, min_level, levels: {username: level}}}`; `POST /pare/voice/consent {version}`. Gerbang: persetujuan, kunci suara aktif, blokir, **hubungan = sudah saling membalas chat** (Personal: kedua pihak ≥ 1 pesan teks; Grup: pengirim pernah menulis & ≥ 1 anggota lain membalas; live grup: tiap peserta pernah menulis), batas laju.
**DoD:** test tiap alasan penolakan (level, persetujuan, blokir, kunci, hubungan); pesan alasan berbahasa Indonesia untuk UI.

## P7-003 — Unggah, kirim, putar voice note (L)
`POST /pare/voice/notes` (meta: conversation, lang, durasi ≤ 60 dtk) → URL unggah bertanda tangan (`storage`), `POST /pare/voice/notes/{id}/finish` → pesan bertipe `voice` masuk `pare_messages` dan dikirim lewat hub (`ChatMsg.kind = "voice"`, `voice: {id, duration_ms}`); `GET /pare/voice/notes/{id}/audio` → URL putar bertanda tangan (hanya anggota percakapan). Inbox memuat pesan voice. Pekerjaan pembersih menghapus audio **dan transkrip** > 3 hari (`status=expired`). Fitur suara hanya aktif di Google Chrome.
**DoD:** hanya anggota yang bisa memutar; batas ukuran/durasi ditolak; audio kedaluwarsa dihapus; test hub menerima pesan voice.

## P7-004 — Penilaian transkrip dari browser (M) — ⛔ DILEPAS SEMENTARA
Klien: `SpeechRecognition` (lang = bahasa zona / pilihan di Kampung Bahasa, `continuous`) berjalan selama merekam voice note / selama panggilan; hasil (teks + confidence per potongan) dikirim bersama voice note (`POST /pare/voice/notes/{id}/finish {transcript: [{text, confidence}]}`) atau per 15–30 dtk lewat hub (`voice_transcript {room, parts}`). Server: `judge_speech(zone, parts)` = `pare_langrule.judge` per potongan + aturan confidence (< 0,45 atau kosong berturut-turut = strike lemah; 2 lemah = 1 strike), toleransi potongan pendek/nama/angka. Tanpa dukungan browser (Firefox) → fitur suara nonaktif. Transkrip **voice note** disimpan 3 hari (`pare_voice_transcripts`); transkrip **live** hanya dinilai di memori lalu dibuang (yang disimpan hanya strike tanpa isi).
**DoD:** test server untuk: sesuai bahasa, Indonesia di kampung, Indonesia di Kampung Bahasa, bahasa lain yang diizinkan di Kampung Bahasa, confidence rendah beruntun, terlalu pendek, transkrip kosong; batas ukuran/laju `voice_transcript`.

## P7-005 — Strike, penalti, kunci, mode shadow (M) — ⛔ DILEPAS SEMENTARA
Aturan ADR-0017 §4 di `services/pare_voice_penalty.rs`: 2 strike = −½ nyawa (`pare_ledger` `voice_violation`, maks −1 per voice note/sesi), 3 penalti/24 jam = kunci 24 jam. Bendera `voice.penalties_enabled` (awal **false** = shadow: catat verdict & strike hipotetis, tanpa memotong). Pesan hasil ke pengirim lewat hub (`voice_result {note, verdict, hearts}`).
**DoD:** test ledger, batas per sesi, kunci & pembukaan otomatis, shadow tidak mengubah nyawa.

## P7-006 — Retensi & hapus akun (S)
Job tiap jam: hapus audio & transkrip voice note > 3 hari, log sesi > 1 tahun; jalur hapus akun memastikan cascade. Ekspor/hapus data suara atas permintaan pemain.
**DoD:** test pemangkasan per tanggal; tidak ada audio yatim di storage.

## P7-008 — FE voice note (M)
Tombol 🎙 di percakapan (tahan/ketuk untuk rekam, batal, kirim), pemutar di gelembung pesan (durasi, kecepatan), status "sedang dianalisis" lalu hasil (peringatan/penalti dijelaskan), layar persetujuan pertama kali, alasan nonaktif dari `eligibility`. Tanpa aturan di FE.
**DoD:** browser: rekam → kirim → penerima memutar → transkrip dinilai → hasil tampil; izin mikrofon ditolak ditangani.

---

# Pare-7b — Live conversation

## P7-007 — Blokir, laporan, moderasi (M)
`POST /pare/blocks`, `DELETE /pare/blocks/{username}`, `POST /pare/voice/reports {ref, reason}` (voice note: kutipan transkrip selama masih ada; live: keterangan pelapor saja), auto-mute pelapor→terlapor, penandaan otomatis ≥ 3 pelapor/7 hari. Antrean tinjauan & tindakan (peringatan, kunci N hari) di Admin Pusat dengan log tindakan.
**DoD:** test alur laporan → antrean → tindakan → kunci berlaku; pemain yang diblokir tidak bisa mengundang.

## P7-009 — LiveKit: ruang, token, undangan (L)
Infrastruktur: VM GCP baru `pare-voice` (asia-southeast2, e2-small/e2-standard-2 sesuai uji), IP statis, firewall tag `pare-voice`; LiveKit server + TURN + TLS, konfigurasi API key/secret via env. Rust: `POST /pare/voice/rooms {conversation, lang}` (cek gerbang semua peserta), `POST /pare/voice/rooms/{id}/join|decline|leave`, token akses HS256 berumur pendek (izin: hanya publish audio, tanpa data/video), status di Redis (undangan TTL 45 dtk, ruang aktif, satu panggilan per pemain), pesan hub `voice_invite / voice_cancelled`, webhook LiveKit (`participant_joined/left`, `room_finished`) → `pare_voice_sessions/participants`. Web Push untuk undangan saat offline (bergantung Pare-5).
**DoD:** test token (klaim, umur, ruang), izin per peserta, undangan kedaluwarsa, satu panggilan aktif, webhook memperbarui sesi; uji dengan 2 klien nyata.

### P7-009 — status (2026-09-26): dikerjakan untuk **dev lokal**

Backend selesai dan diuji (`pare_voice_live.rs`, `pare_livekit.rs`, migrasi 0090; 8 tes + uji interoperabilitas terhadap LiveKit sungguhan: token diterima, webhook bertanda tangan LiveKit lolos verifikasi, token rusak 401). **VM GCP `pare-voice` + TLS + TURN sengaja belum dibuat** — itu bagian infrastruktur P7-011 (perlu keputusan biaya). Menjalankan LiveKit lokal: `titian-backend-rust/dev/livekit/run.sh` (mengunduh server v1.13.7 ke `~/.local/share/pare-livekit`, membuat API key/secret, dan mengarahkan webhook ke `http://localhost:8090/webhooks/livekit`); tambahkan `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` yang dicetaknya ke `.env` backend. Yang BELUM diuji: media audio antar-browser (perlu FE `livekit-client`, P7-011) — uji "2 klien nyata" di sini baru setingkat signalling.

## P7-010 — Pengawasan transkrip live (M) — ⛔ DILEPAS SEMENTARA
Tanpa Egress: tiap klien mengirim transkrip mikrofonnya sendiri (P7-004). Server mengumpulkan verdict per peserta per sesi dan mengirim hasil setelah sesi (`voice_result`). Deteksi "bicara tanpa transkrip": webhook LiveKit *active speaker* / `track_published` dibandingkan dengan `voice_transcript` yang masuk — bicara > 30 dtk tanpa transkrip = "tak terbaca" (strike lemah) + penandaan untuk moderator. Shadow mode dulu.

**Status: backend selesai dan diuji** (`pare_voice_watch.rs`, migrasi 0091; 5 tes unit + 5 tes integrasi: verdict per peserta terkirim hanya ke pemilikinya, klien yang berhenti mengirim ketahuan & ditandai, hanya track mikrofon yang menjalankan jam, batch dari luar sesi diabaikan, lapor panggilan live). **Penyimpangan dari rencana:** LiveKit tidak punya webhook *active speaker*, jadi dasar deteksi adalah `track_published/unpublished` (mikrofon menyala) dibanding batch 30-dtk termasuk yang kosong sebagai detak; "bicara" tak bisa dibedakan dari "menyala hening" di sisi server — itu sebabnya batas ≥ 30 dtk tak tertutup dan hanya dinilai sebagai penandaan + strike lemah. Klien (mengirim batch/detak 30 dtk) dikerjakan di P7-011. Belum diuji dengan browser sungguhan.
**DoD:** verdict teralamat ke peserta yang benar; klien yang berhenti mengirim transkrip terdeteksi; tidak ada audio live di server kita.

## P7-011 — FE live call + uji beban & runbook (L)
`livekit-client`: overlay panggilan (mute, keluar, laporkan, indikator bicara, pemulihan koneksi), tombol 📞 dengan alasan nonaktif, notifikasi masuk (hub + push). Uji beban: N ruang × 2–6 peserta terhadap 1 VPS; ukur CPU/bandwidth per jam; runbook operasional (port UDP, TLS, TURN, skala node).
**DoD:** browser 2 akun: panggil → terima → bicara → hasil penilaian setelah sesi; angka kapasitas & biaya per 1.000 menit tercatat di `gcp-migration-runbook.md`.

**Uji di Railway (2026-09-26):** deploy sederhana dari repo GitHub — folder `alr/livekit-railway/` (Dockerfile + entrypoint + railway.json + README berisi prosedur). Jalur TCP-only ala Railway (proxy TCP → socat → LiveKit) sudah disimulasikan lokal dengan Docker (UDP diblokir, 2 Chrome, audio dua arah lewat TCP, webhook masuk ke backend); belum dicoba di Railway sungguhan. Uji berikutnya: dev dan prod dengan backend `api.titianasa.com` dan FE `pare.titianasa.com`.

**Status (2026-09-26): klien selesai & diuji end-to-end di localdev; VM/uji beban/runbook BELUM.** `livekit-client` di `alr/game` (`game/call.ts` sesi LiveKit + pengenal suara dengan batch 30 dtk termasuk kosong sebagai detak; `components/game/Call.tsx` tombol 📞 dengan alasan nonaktif dari `eligibility.live`, banner telepon masuk, overlay: mikrofon/bisu, tutup telepon, indikator bicara, lapor per peserta + senyapkan lokal, pemulihan koneksi, hasil penilaian; `Game.tsx` meneruskan `voice_invite/cancelled/result{room}`). **Uji 2 akun (Chrome sungguhan via Playwright + LiveKit lokal, mikrofon palsu, pengenal suara di-stub karena headless Chrome tak punya layanan Google):** 📞 → banner → Jawab → audio 2 arah tersambung (track audio `live` di kedua sisi) → batch tiap 30 dtk dinilai → tutup telepon → hasil di overlay: pemain berbahasa Indonesia di Kampung Bahasa 15 peringatan (shadow, nyawa tetap 5), pemain berbahasa Inggris 0; DB: strike `live:<sesi>` hanya untuk yang melanggar, 0 baris transkrip, 0 laporan sistem, kunci panggilan Redis terbebas. **Belum diuji:** suara manusia sungguhan/kualitas audio, pengenal suara Chrome asli, Firefox/Safari, jaringan di balik NAT (butuh TURN di VM), penolakan izin mikrofon di UI. Catatan: sesi tetap `active` di DB sampai LiveKit mengirim `room_finished` (mengikuti `empty_timeout` LiveKit).
