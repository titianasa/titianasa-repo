# Pare-12 — Chat langsung dengan pemain dan warga (NPC)

Keputusan pemilik 2026-10-15: saat berhadapan dengan pemain atau warga, chat langsung terbuka; balon muncul di atas kepala
kedua pihak; percakapan tetap tercatat di ruang chat.

## Yang dibangun
- **Kotak chat cepat** (`game/src/components/game/QuickChat.tsx`): muncul ketika pemain mengetuk pemain lain, atau warga biasa
  (guide, poly, local). Tombol ℹ membuka dialog lama warga; 📜 membuka ruang chat. Menutup sendiri jika pemain menjauh > 6 petak.
- **Pemain ↔ pemain**: lewat chat pribadi yang sudah ada (`net.chat(text, "private", [uid])`), jadi balon dan riwayat otomatis.
- **Warga ↔ pemain**: `POST /pare/npc/chat` (backend `internal/pare/npcchat.go`). Persona dibuat server dari nama + jenis
  warga + bahasa + level pemain di bahasa itu. Model: `PARE_NPC_CHAT_MODEL` (bawaan `anthropic/claude-haiku-5.5` lewat
  OpenRouter, sekitar Rp0,5 per 100 pesan). Jawaban singkat dalam bahasa yang dipelajari + arti Indonesia di balon.
- **Riwayat**: tabel `pare_npc_messages` (migrasi 0107). `GET /pare/npc-chats` mengembalikan bentuk `ChatMsg` dengan
  percakapan `npc:<id>`, jadi ChatPanel menampilkannya sebagai chat pribadi (tanpa blokir, suara, panggilan, dan aturan bahasa
  zona). `DELETE /pare/npc-chats/{id}` = "Hapus chat".
- **Kuota harian** (WIB, pesan pemain): gratis 30, Plus 100, Pro 300. Jawaban gagal tidak disimpan dan tidak dihitung.
- Engine: `sayNpcBubble` dan `npcTile` di kedua engine (3D dan pixel).

## Belum
- Tutor (membuka jalur belajar) dan penjual (toko) masih membuka dialognya sendiri; belum ada tombol ngobrol di sana.
- Warga yang punya misi tetap membuka misi lebih dulu.
- Chat pemain ↔ pemain belum diuji otomatis dengan dua klien.
- Belum di-deploy: migrasi 0107 dan env `PARE_NPC_CHAT_MODEL` (opsional) di Hetzner.

Tes: `./go.sh test ./internal/pare -run TestNPCChat`, `QA_BASE=http://localhost:4700 bun game/scripts/e2e/quickchat3d.ts gb`.

## Pemain komputer (crowd) ikut ngobrol (2026-10-20)

Pemilik: pemain komputer ditambahkan di area lapangan, dan bisa berinteraksi dengan pemain asli di chat pribadi dan grup.

- **Lapangan**: `game/scripts/export-nav.ts` membuat 54 titik berkelompok tiga (saling berhadapan) di tanah `l` zona umum, jenis `field`. Crowd punya kegiatan baru `hangout` (bobot 45, sore hari 15–18 WIB dua kali lipat), dan 55% orang yang sudah ada saat server mulai langsung berdiri di lapangan. Sekitar 40% crowd Kampung Bahasa ada di lapangan. `nav.json` dibuat ulang (hanya zona umum yang berubah).
- **Balasan**: `internal/pare/crowdchat.go`. Pesan pribadi ke pemain komputer selalu dibalas; di grup, yang disebut namanya membalas, dan bila tak ada yang disebut satu anggota ikut menjawab (peluang 75%). Jeda 2–6 detik. Persona: teman belajar komputer pada bahasa dan level yang sedang dipelajarinya, membalas dalam bahasa pesan terakhir (Inggris, Mandarin, Arab, Jepang, Korea), singkat, dan mengaku bila ditanya tulus apakah ia bot. Model: `PARE_NPC_CHAT_MODEL` (Haiku). Satu percobaan ulang bila panggilan AI macet (juga dipakai warga).
- **Jatah**: jatah harian yang sama dengan ngobrol dengan warga (gratis 30, Plus 100, Pro 300), dihitung dari semua balasan pemain komputer di percakapan pemain itu. Lewat jatah: pemain diberi tahu, tidak ada balasan.
- **Tanda**: `bot` pada pesan dan peserta chat; di game tampil "🤖 Pemain komputer · teman belajar" (kotak chat cepat, judul ruang chat, daftar chat, nama pengirim di grup). Suara dan telepon tidak ditawarkan di chat dengan pemain komputer.
- **Game 3D**: pemain komputer kini bisa diketuk (tombol aksi atau papan nama) dan membuka kotak chat cepat. Aksi sosial (tos, salaman) tetap tidak ditawarkan.
- Tes: `./go.sh test ./internal/pare -run TestCrowd`, `QA_BASE=http://localhost:4700 bun game/scripts/e2e/crowdchat3d.ts`.

Belum: chat umum (Umum) tidak dijawab pemain komputer, dan mereka belum memulai obrolan sendiri. Jumlah crowd per saluran diatur `PARE_CROWD_MIN` dan `PARE_CROWD_MAX` di server (belum dicek nilainya di Hetzner).
