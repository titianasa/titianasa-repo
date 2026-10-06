# ADR-0016: Kampung Bahasa Pare di atas arsitektur Titian

Status: Accepted (disetujui user 2026-09-24, termasuk asumsi §10; tambahan username di §1)
Date: 2026-09-24
Supersedes: -
Superseded by: -
Related: ADR-0005 (credit economy), ADR-0006 (RBAC), ADR-0014 (Admin Pusat), ADR-0015 (grup & liga)

> **Catatan migrasi (2026-10-05, ADR-0020):** backend sedang dipindah dari Rust ke Go. Keputusan di ADR ini tidak berubah; setiap "Rust" / `titian-backend-rust` / `services/pare_*.rs` di bawah berpadanan dengan `titian-backend-go/internal/pare/` setelah tiket G14. Sampai G14 selesai, kode Pare yang aktif tetap yang Rust.

## Context

**Kampung Bahasa Pare** adalah game pixel-art belajar 5 bahasa (Inggris, Mandarin, Arab, Jepang, Korea) yang hidup di simulasi Kampung Inggris Pare. Kode sekarang ada di `alr/game` (dipindah dari `nanyang-workspace/game` pada 2026-09-24) dan akan tayang di **`pare.titianasa.com`**.

Kondisi saat ini (prototipe yang sudah bisa dimainkan):
- **Frontend**: Next.js 16 + canvas engine sendiri (peta prosedural, sprite, cahaya, cuaca nyata Pare lewat `/api/weather`).
- **Realtime**: server WebSocket Bun (`server/realtime.ts`) — zona → saluran maks. 50, batch posisi 10 Hz, chat Umum / Personal / Grup, sudah diuji beban 2000 klien.
- **Semua data pemain di `localStorage`** (`store` di `src/game/progress.ts`): XP, uang, nyawa, stamina, level per bahasa, statistik kata, misi harian, riwayat chat personal/grup. Artinya: tidak lintas perangkat, dan **bisa dicurangi** (uang/XP/nyawa diubah dari DevTools).
- **Konten bahasa hard-code di bundle** (`src/game/content/*.ts`, `levels/*.ts`), termasuk kunci jawaban. Penilaian jawaban terjadi di browser.
- Aturan ekonomi (2026-09-24): mulai dari nol, XP hanya untuk level (salah = −5 XP), uang hanya dari belajar (Rp200/jawaban benar di Basic, naik per level; lulus level Rp1.000 × level; misi Rp500), nyawa 5 dalam satuan ½ yang terikat stamina (makan/minum/tidur menambah, berjalan & lapar mengurangi), ujian lompat level 20 soal Rp50.000 untuk 2 percobaan.

Keputusan user (2026-09-24): game adalah **aplikasi mandiri** (folder `alr/game`, repo & deployment sendiri — **bukan bagian dari `titian-web`**), tetapi server memakai **backend Titian yang sama** (`titian-backend-rust`) dengan arsitektur Titian (**Rust/Axum + Redis + Postgres**), frontend di **Vercel**, **tidak ada data dinamis hard-code di FE**, aset & data statis di-cache CDN, dan game dijadikan **PWA dengan push notification**. Data yang dipakai bersama hanya **user**; pemain game dan pengguna web Titian tetap dibedakan dan masing-masing wajib onboarding sendiri.

## Decision

### 1. Satu identitas, dua profil, dua onboarding

- **`users` dipakai bersama.** Login Pare memakai alur Google OAuth Titian yang sudah ada (`POST /auth/google/callback`, access JWT + refresh token). Akun Google yang sama = baris `users` yang sama.
- **Profil terpisah:**
  - Titian: `user_learning_profiles` (ADR/migrasi 0040) — onboarding web Titian.
  - Pare: tabel baru **`pare_players`** (username, nama panggilan, penampilan, posisi, zona, statistik hidup, uang, XP game). Onboarding Pare = layar pembuatan tokoh: **username unik (min. 3 karakter, permanen)** + **nama panggilan** + penampilan. Keduanya tampil di atas karakter sebagai `Nama @username` (keputusan user 2026-09-24).
- **Aturan masuk:**
  - Masuk lewat Pare → `users` dibuat bila belum ada → belum punya `pare_players` → onboarding tokoh.
  - Buka web Titian dengan akun itu → belum punya `user_learning_profiles.onboarding_completed_at` → wizard onboarding Titian. Begitu juga sebaliknya.
- `GET /pare/me` mengembalikan `404 pare_player_not_found` bila belum onboarding; FE mengarahkan ke pembuatan tokoh. Tidak ada `if user is game user` di kode Titian lain.

### 2. Data game milik Titian Postgres, di tabel `pare_*`

Semua data dinamis game disimpan di database Titian dengan awalan **`pare_`**, terpisah dari ekonomi Titian:
- **XP & uang game ≠ XP global Titian ≠ diamond/wallet Titian** (ADR-0005). Tidak ada konversi di fase ini (§10).
- Rancangan tabel (nama final diverifikasi saat tiket):

| Tabel | Isi |
|---|---|
| `pare_players` | user_id (PK), nama tokoh, look (jsonb), zona, posisi, xp, money, hearts (numeric langkah ½), stamina, fullness, focus, violations, streak, timestamps hidup (last_seen, sleeping_since, bike/laundry date, meal/snack counter harian) |
| `pare_lang_progress` | (player, bahasa): level, lang_xp, level_start_xp, exam_tries |
| `pare_word_stats` | (player, bahasa, word_uid): seen, correct |
| `pare_rest_log` | periode istirahat (offline ≥ 1 jam & tidur) untuk aturan 5 jam/24 jam |
| `pare_daily` | (player, tanggal WIB): counters jsonb, misi yang sudah diklaim, pelajaran selesai hari ini, cooldown |
| `pare_ledger` | **setiap** perubahan uang/XP/nyawa: jenis, delta, alasan, ref — audit & anti-curang |
| `pare_conversations` / `pare_conversation_members` / `pare_messages` | chat Personal & Grup (dan Umum per saluran, §5) |
| `pare_content_*` | konten bahasa & kurikulum (§3) |
| `push_subscriptions` | langganan Web Push (generik, bisa dipakai Titian juga) |

### 3. Konten bahasa pindah ke server; penilaian di server

- Kosakata, frasa, situasi, pola kalimat, konsep, dan tangga level (CEFR/HSK/JLPT/TOPIK/Mubtadi') disimpan di **`pare_content_*`** dan di-seed dari berkas yang sekarang ada di `src/game/content`. Kelak bisa dikelola lewat Admin Pusat (di luar ADR ini).
- **Kunci jawaban tidak pernah dikirim ke klien** (pola sama dengan checkpoint & bank soal Titian 2026-09-14): server menyusun "kertas" pelajaran/tantangan/ujian (`paper_id`, soal tanpa kunci), klien mengirim jawaban, **server menilai** dan menerapkan XP/uang lewat `pare_ledger`.
- Konten yang aman ditampilkan (kamus, frasa cepat, konsep) disajikan lewat endpoint baca yang **bisa di-cache CDN** (`Cache-Control` + `ETag` berbasis versi konten).
- Deteksi bahasa chat (`langrule.ts`) di-port ke Rust dan dijalankan **di server**; klien tetap boleh menampilkan pratinjau, tapi penalti ½ nyawa diputuskan server.

### 4. Simulasi hidup otoritatif di server

- Stamina, kenyang, istirahat, nyawa dihitung **malas (lazy) dari timestamp** saat dibaca/diubah, bukan tick per menit dari klien. Rumus di satu modul `services/pare_life.rs` (port `src/game/life.ts`).
- Stamina dari langkah dihitung server dari pesan `move` di WebSocket (jalan 0,04/petak, sepeda 0,015/petak — diturunkan setengah 2026-09-25).
- Semua aksi yang menyentuh uang/nyawa lewat API: beli makanan (`POST /pare/shop/buy`, harga & menu dari server), laundry, sewa sepeda, tidur/bangun, taman, bayar ujian, klaim misi.

### 5. Realtime dipindah ke Rust

- WebSocket **`GET /ws/pare?token=…`** di backend Rust, auth lewat `resolve_auth_context` dengan token di query (pola `canvas_ws.rs`).
- `services/pare_hub.rs` membawa logika Bun yang sudah teruji: saluran maks. 50 per zona, batch `moves` 10 Hz, rate limit gerakan, backpressure, satu koneksi per pemain.
- **Chat:** pesan Personal & Grup disimpan di `pare_messages` dan dikirim ke anggota di zona mana pun; pesan Umum disimpan per saluran dengan retensi (§10). Riwayat dimuat dari API (`GET /pare/conversations`, `/messages`), bukan `localStorage`.
- **Skala horizontal:** instance tunggal dulu (sesuai uji beban). Saat butuh >1 instance, saluran di-*shard* per zona dan pesan lintas instance lewat **Redis pub/sub**. Presence online di Redis.

### 6. Frontend mandiri (self-host): hanya statis & tampilan

- `alr/game` di-deploy sendiri ke `pare.titianasa.com` (rencana Vercel), terpisah dari `titian-web`; `NEXT_PUBLIC_API_URL` & `NEXT_PUBLIC_WS_URL` dari env, tidak ada URL/angka ekonomi di kode.
- **Boleh tetap di bundle/CDN (statis):** geometri peta, sprite, tile, UI copy, font, suara. **Wajib dari server (dinamis):** profil, ekonomi, progres, konten soal, harga menu, misi, chat, level.
- Backend menambah `https://pare.titianasa.com` (dan domain preview Vercel) ke `allowed_origins`; Google OAuth client menambah origin yang sama.

### 7. PWA & push notification

- `manifest.webmanifest`, ikon, service worker (cache aset statis, halaman offline), prompt pasang.
- **Web Push (VAPID)**: tabel `push_subscriptions`, endpoint `POST/DELETE /me/push-subscriptions`, pengiriman lewat **`titian-worker`/job_queue** (tidak dari request handler).
- Pemicu awal: pesan Personal/Grup saat pemain offline, misi harian baru, pengingat stamina/lapar, tidur cukup (bangun). Semua bisa dimatikan per jenis di pengaturan pemain.

### 8. Cuaca nyata Pare

Tetap di route handler Next (`/api/weather`, ISR 30 menit) — sudah server-side dan satu panggilan per 30 menit untuk semua pemain. Boleh dipindah ke Rust + Redis kelak tanpa mengubah kontrak.

### 9. Yang tidak berubah

- Tidak ada perubahan kontrak endpoint Titian yang ada; semua endpoint game di bawah **`/pare/*`**.
- XP/streak/liga Titian tidak membaca data `pare_*` (dan sebaliknya) sampai ada keputusan terpisah.
- Aturan main dan angka ekonomi game (Context) dipertahankan, dipindah apa adanya ke server.

### 10. Asumsi (dikonfirmasi user 2026-09-24)

1. **Login wajib sebelum bermain** (layar judul → Google login → pembuatan tokoh). Mode tamu tanpa login **tidak ada** (data tamu tidak bisa otoritatif).
2. **Login terpisah per domain** di awal (login sekali di Pare, sekali di Titian — akun sama). SSO lintas subdomain (cookie `.titianasa.com`) ditunda.
3. **Ekonomi terpisah**: uang & XP game tidak bisa ditukar ke diamond/XP Titian.
4. **Konten bahasa di DB** (seed dari berkas sekarang), bukan berkas JSON di CDN — supaya penilaian di server dan kelak bisa diedit dari Admin Pusat.
5. **Retensi chat Umum 30 hari**; Personal & Grup disimpan tanpa batas waktu (bisa dihapus pemain).
6. **Data localStorage lama tidak dimigrasi** (aplikasi belum live); semua pemain mulai baru di server.
7. Nomor fase **Pare-1 … Pare-6** (tiket `P1-…`) supaya tidak bertabrakan dengan Phase 41–50 Titian.

## Consequences

- (+) Anti-curang: uang, XP, nyawa, kunci jawaban tidak lagi di tangan klien; semua perubahan tercatat di `pare_ledger`.
- (+) Lintas perangkat, chat & progres awet, PWA + push, satu backend & satu database untuk dioperasikan.
- (+) Realtime ikut infrastruktur Titian (Caddy, deploy, monitoring) dan bisa diskalakan dengan Redis.
- (−) Setiap jawaban & pembelian butuh round-trip ke server; UI harus optimistis dengan rollback, dan offline hanya untuk aset statis.
- (−) Porting logika TypeScript (life, langrule, lesson builder, hub realtime) ke Rust perlu test paritas agar angka tidak bergeser.
- (−) Backend Titian bertambah beban WebSocket jangka panjang; diawasi lewat uji beban `scripts/loadtest.ts` yang diarahkan ke endpoint Rust.
