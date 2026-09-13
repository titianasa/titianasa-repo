# Migrasi ke GCP — Titian Content Studio

Panduan step-by-step memindahkan Google OAuth, generasi AI (OpenRouter/DeepSeek → Vertex AI Gemini), dan hosting ke Compute Engine — dipakai selama free trial $300.

## Ringkasan — 3 permintaan awal dipetakan ke 9 fase

| Layanan | Yang terjadi | Fase |
|---|---|---|
| **Compute Engine** | VM `e2-standard-2` jadi rumah baru backend, frontend, Postgres, dan Redis | 1, 2, 3, 7 |
| **Google OAuth** | Login GSI yang sudah jalan sekarang tinggal disambungkan ke project GCP baru — tidak ada client secret yang berubah | 4 |
| **Vertex AI Gemini** | Ganti 7 slot model teks (bukan OCR/STT/TTS) dari OpenRouter/DeepSeek ke Gemini 3.8 Flash lewat Vertex | 5, 6 |

Urutannya penting: Fase 4–7 bergantung pada VM dari Fase 1–2 sudah berjalan.

---

## Fase 0 — Prasyarat

- [ ] Akun GCP dengan trial $300 aktif, billing sudah terpasang (trial GCP tetap butuh kartu untuk verifikasi, walau tidak ditagih selama masa trial).
- [ ] `gcloud` CLI ter-install di mesin dev (`brew install google-cloud-sdk` atau installer resmi), lalu `gcloud init` dan `gcloud auth login`.
- [ ] Nama domain yang mau dipakai (mis. `app.titianasa.com` + `api.titianasa.com`) dan akses ke DNS-nya untuk menambah record A nanti (Fase 7).
- [ ] Backup database sudah ada — dari sesi sebelumnya: `/home/john/backups/titian-bun-full-backup-20260911-154932.sql`. Kalau sudah ada perubahan data sejak itu, ambil backup baru sebelum Fase 3.

> **Info** — Buat project GCP baru khusus untuk ini (jangan pakai project lama kalau ada) — memudahkan pelacakan biaya dan quota terpisah dari eksperimen lain:
> ```bash
> gcloud projects create titianasa-prod --name="Titian Asa"
> gcloud config set project titianasa-prod
> ```
> Lalu hubungkan billing account trial-nya lewat Console (Billing → Link a billing account).

---

## Fase 1 — VM Compute Engine

Satu VM `e2-standard-2` (2 vCPU, 8 GB RAM) menampung backend Rust, frontend Next.js, Postgres, dan Redis — cukup untuk beban saat ini, dan gampang di-resize kalau kurang nanti.

### 1.1 — Aktifkan API & siapkan service account

```bash
# Aktifkan Compute Engine API
gcloud services enable compute.googleapis.com

# Service account untuk VM — dipakai VM utk otentikasi ke Vertex AI
# TANPA perlu file key (lihat Fase 5)
gcloud iam service-accounts create titianasa-vm \
  --display-name="Titian Asa VM"
```

### 1.2 — Pesan IP statis

- [ ] Reserve external static IP supaya alamat VM tidak berubah tiap restart (penting untuk DNS di Fase 7).

```bash
gcloud compute addresses create titianasa-ip \
  --region=asia-southeast2
```

> **Info** — `asia-southeast2` (Jakarta) — region terdekat untuk latensi ke pengguna Indonesia. Pastikan region yang sama dipakai konsisten di semua perintah di fase ini.

### 1.3 — Buat VM

```bash
gcloud compute instances create titianasa-app \
  --zone=asia-southeast2-a \
  --machine-type=e2-standard-2 \
  --image-family=ubuntu-2404-lts-amd64 \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB \
  --boot-disk-type=pd-ssd \
  --address=titianasa-ip \
  --service-account=titianasa-vm@$(gcloud config get-value project).iam.gserviceaccount.com \
  --scopes=cloud-platform \
  --tags=http-server,https-server
```

- [ ] VM dibuat dengan disk 50 GB SSD — cukup untuk OS + toolchain Rust/Bun + kode + Postgres data untuk beberapa waktu ke depan.
- [ ] `--scopes=cloud-platform` dipasang supaya service account VM bisa dipakai library Rust (`gcp_auth`) mengambil token Vertex AI otomatis lewat metadata server — tidak perlu file key JSON sama sekali.

### 1.4 — Firewall

```bash
# HTTP/HTTPS publik — dipakai reverse proxy (Fase 7)
gcloud compute firewall-rules create allow-http-https \
  --allow=tcp:80,tcp:443 \
  --target-tags=http-server,https-server

# SSH — batasi ke IP kamu sendiri, bukan 0.0.0.0/0
# cek IP kamu dulu: curl ifconfig.me
gcloud compute firewall-rules create allow-ssh-mine \
  --allow=tcp:22 \
  --source-ranges=GANTI.DENGAN.IP.KAMU/32
```

> **Perhatikan** — Jangan biarkan port 8090 (backend) atau 3000 (frontend) terbuka ke publik — keduanya cukup diakses `localhost` di VM, karena Caddy (Fase 7) yang jadi satu-satunya pintu masuk dari luar lewat 80/443.

### 1.5 — SSH masuk & update dasar

```bash
gcloud compute ssh titianasa-app --zone=asia-southeast2-a

# di dalam VM:
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl build-essential pkg-config libssl-dev
```

- [ ] Masuk ke VM lewat SSH berhasil dan paket dasar ter-update.

---

## Fase 2 — Software di VM

Menyamai stack dev yang sudah jalan: Docker untuk Postgres/Redis, Rust untuk backend, Bun untuk frontend.

### 2.1 — Docker (Postgres + Redis)

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
# logout/login lagi supaya grup docker aktif, lalu:

docker run -d --name titian-postgres \
  --restart unless-stopped \
  -e POSTGRES_USER=titian \
  -e POSTGRES_PASSWORD=GANTI-PASSWORD-KUAT \
  -e POSTGRES_DB=titian_bun \
  -p 127.0.0.1:5432:5432 \
  -v titian-postgres-data:/var/lib/postgresql/data \
  postgres:16-alpine

docker run -d --name titian-redis \
  --restart unless-stopped \
  -p 127.0.0.1:6379:6379 \
  -v titian-redis-data:/data \
  redis:7-alpine redis-server --appendonly yes
```

> **Info** — Diikat ke `127.0.0.1`, bukan `0.0.0.0` — Postgres dan Redis hanya bisa diakses dari dalam VM itu sendiri, tidak dari internet, walau tanpa firewall rule tambahan.

### 2.2 — Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
rustc --version
```

### 2.3 — Bun

```bash
curl -fsSL https://bun.sh/install | bash
source ~/.bashrc
bun --version
```

### 2.4 — Clone repo

Kedua repo sudah punya remote GitHub (di-setup sesi sebelumnya) — tinggal clone langsung di VM:

```bash
mkdir -p ~/app && cd ~/app
git clone https://github.com/titianasa/titianasa-be-rust.git backend
git clone https://github.com/titianasa/titianasa-web.git frontend
```

> **Perhatikan** — Kalau repo GitHub masih *private*, clone lewat HTTPS di atas akan minta autentikasi — pakai `gh auth login` (GitHub CLI) atau setup deploy key/PAT di VM dulu.

- [ ] Docker, Rust, dan Bun semua ter-install dan versinya bisa dicek (`docker --version`, `rustc --version`, `bun --version`).
- [ ] Kedua repo ter-clone ke `~/app/backend` dan `~/app/frontend`.

---

## Fase 3 — Migrasi data Postgres

Restore dump lokal ke Postgres yang baru dijalankan di VM.

### 3.1 — Kirim backup ke VM

```bash
# dari mesin lokal (bukan di dalam VM)
gcloud compute scp \
  /home/john/backups/titian-bun-full-backup-20260911-154932.sql \
  titianasa-app:~/ \
  --zone=asia-southeast2-a
```

### 3.2 — Restore ke container Postgres di VM

```bash
# di dalam VM
docker cp ~/titian-bun-full-backup-20260911-154932.sql titian-postgres:/tmp/restore.sql
docker exec titian-postgres psql -U titian -d titian_bun -f /tmp/restore.sql
docker exec titian-postgres rm /tmp/restore.sql
```

### 3.3 — Verifikasi

```bash
docker exec titian-postgres psql -U titian -d titian_bun -c \
  "select count(*) from module_items; select count(*) from users;"
```

- [ ] Jumlah baris di `module_items`/`users` di VM cocok dengan angka di database lokal (bandingkan manual).

> **Awas** — Backend akan menjalankan migrasi SQL otomatis tiap boot (`db::run_migrations()` di `main.rs`) — pastikan restore ini dilakukan **sebelum** backend pertama kali dijalankan di VM (Fase 7), supaya migrasi jalan di atas data yang benar, bukan database kosong yang lalu ketimpa restore.

---

## Fase 4 — Google OAuth

Login yang jalan sekarang pakai Google Identity Services (GSI) — browser dapat `id_token` langsung dari Google, backend cuma *verifikasi* JWT-nya sendiri (lihat `google_oauth.rs`). Tidak ada client secret atau redirect URI yang perlu dipindah.

> **Keputusan** — **Client ID yang ada sekarang bisa dipakai terus** — Google Identity tidak terikat ke project GCP tertentu untuk soal billing/quota, jadi tidak wajib bikin baru. Kalau mau konsistensi (semua resource di satu project GCP), bikin Client ID baru di project `titianasa-prod` — langkah di bawah untuk opsi itu.

### 4.1 — (Opsional) OAuth consent screen di project baru

Console → *APIs & Services → OAuth consent screen*. Pilih *External*, isi nama app "Titian Asa", email support, logo (opsional). Scope default (`email`, `profile`, `openid`) sudah cukup — GSI tidak minta scope tambahan.

### 4.2 — Buat OAuth Client ID

Console → *APIs & Services → Credentials → Create Credentials → OAuth client ID* → tipe **Web application**.

| Field | Isi |
|---|---|
| Name | Titian Asa — Web |
| Authorized JavaScript origins | `https://app.titianasa.com`, `http://localhost:3000` |
| Authorized redirect URIs | Kosongkan — GSI tidak pakai redirect, hanya *origins*. |

- [ ] Client ID baru tersalin (bentuknya `xxxxx.apps.googleusercontent.com`).

### 4.3 — Pasang di env vars

| File (di VM) | Var | Catatan |
|---|---|---|
| `~/app/backend/.env` | `GOOGLE_CLIENT_ID` | Dibaca saat runtime — cukup restart service (Fase 7). |
| `~/app/frontend/.env.local` | `NEXT_PUBLIC_GOOGLE_CLIENT_ID` | **Di-bake saat build** — ganti value butuh `rm -rf .next/cache` lalu build ulang, restart saja tidak cukup. |

> **Perhatikan** — Kedua nilai ini harus **sama persis** — backend memvalidasi `aud` pada JWT terhadap `GOOGLE_CLIENT_ID`-nya sendiri; kalau beda, semua login gagal dengan `invalid_token`.

- [ ] Login Google dicoba di `https://app.titianasa.com` setelah deploy (Fase 8) dan berhasil.

---

## Fase 5 — Setup Vertex AI

Sisi GCP-nya dulu, sebelum menyentuh kode (Fase 6).

### 5.1 — Aktifkan API & beri izin service account VM

```bash
gcloud services enable aiplatform.googleapis.com

gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
  --member="serviceAccount:titianasa-vm@$(gcloud config get-value project).iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

> **Kenapa gampang** — Karena backend jalan di VM Compute Engine yang service account-nya sudah dipasang di Fase 1 (`--scopes=cloud-platform`), kode Rust cukup minta token ke metadata server VM — **tidak perlu** download file key JSON, simpan secret tambahan, atau urus rotasi key sama sekali.

### 5.2 — Cari ID model persis di Model Garden

- [x] ~~Buka Console → Vertex AI → Model Garden, cari ID model persis~~ — **dikonfirmasi langsung lewat API**: `gemini-3.8-flash` itu sendiri sudah ID yang benar, tidak ada akhiran versi.
- [x] ~~Cek region mana saja yang menyediakannya~~ — **`gemini-3.8-flash` HANYA tersedia di location `global`**, bukan region biasa seperti `asia-southeast1`/`us-central1` (dites langsung: keduanya balas 404 "Publisher model ... was not found"). Model preview/terbaru sering begini — belum di-roll-out ke regional endpoint.

> **Perhatikan — endpoint `global` beda bentuk URL-nya.** Region biasa pakai subdomain `{region}-aiplatform.googleapis.com`; location `global` **tidak pakai prefix region sama sekali** — host-nya `aiplatform.googleapis.com` polos, tapi path-nya tetap `.../locations/global/...`. Kalau kode provider Vertex kamu (Fase 6.3) selalu menempel `{region}-` di depan host, panggilan ke `global` akan gagal DNS lookup. Providernya harus punya cabang khusus: `region == "global"` → host tanpa prefix, selain itu → host dengan prefix `{region}-`.

### 5.3 — Catat nilai untuk Fase 6

| Kunci | Nilai |
|---|---|
| Project ID | `titianasa-prod` (`gcloud config get-value project`) |
| Region/Location | `global` — **wajib**, bukan `asia-southeast1`/`us-central1` |
| Model ID | `gemini-3.8-flash` (sudah dikonfirmasi persis) |

---

## Fase 6 — Kode: provider Vertex AI Gemini

Bagian coding sungguhan. Cuma jalur generasi TEKS yang pindah — OCR (vision), STT, dan TTS tetap lewat OpenRouter/DeepSeek karena scope permintaan awal cuma "ganti OpenRouter DeepSeek" untuk teks.

> **Yang pindah vs tidak**
> - **Pindah ke Gemini** (7 field teks murni di `config.rs`): `ai_speaking_room_text_model`, `ai_writing_evaluation_model`, `ai_speaking_evaluation_model`, `ai_grammar_evaluation_model`, `ai_lesson_generation_model`, `ai_question_generation_model`, `ai_live_chat_model` — plus `AI_MODEL_OPTIONS` di `ai_provider.rs` (allowlist model yang boleh dipilih penulis).
> - **Tetap di OpenRouter**: `ai_ocr_model` (vision, butuh `image_url`), `ai_stt_model` (Whisper), `ai_tts_model` + `ai_speaking_room_tts_model` (text-to-speech).

### 6.1 — Tambah dependency

`Cargo.toml` — `gcp_auth` mengambil access token dari metadata server VM secara otomatis (Application Default Credentials), tanpa file key:

```bash
cargo add gcp_auth
```

### 6.2 — Config baru

`src/config.rs` — dua field baru, mengikuti pola field lain di struct yang sama:

```rust
// tambahkan ke struct Config
pub gcp_project_id: String,
pub gcp_region: String,

// tambahkan ke Config::from_env(), pola sama seperti google_client_id
gcp_project_id: std::env::var("GCP_PROJECT_ID")
    .context("GCP_PROJECT_ID is required")?,
gcp_region: std::env::var("GCP_REGION")
    .unwrap_or_else(|_| "global".to_string()),
```

- [x] Update `AI_MODEL_OPTIONS` di `ai_provider.rs` ke `gemini-3.8-flash`, dan ubah default 7 field `_model` teks di atas ke ID Gemini yang sama. — **sudah dikerjakan & dites langsung lewat API sungguhan**, bukan cuma dibaca dari dokumentasi.

### 6.3 — Provider baru

File baru `src/services/vertex_ai_provider.rs`, implementasi `AIProvider::generate()` saja — `transcribe()`/`synthesize_speech()` mengembalikan `Err` (bukan `unimplemented!()` — supaya salah pakai gagal rapi lewat error biasa, bukan panic) karena tidak pernah dipanggil untuk provider ini (lihat 6.4). Endpoint-nya WAJIB punya percabangan `global` vs region biasa (lihat catatan di 5.2) — fungsi murni `build_endpoint(project_id, region, model)` yang dites langsung tanpa perlu kredensial GCP sungguhan mempermudah ini. Bedanya dari `DeepSeekProvider` (bentuk request Gemini beda dari format OpenAI):

| | OpenRouter (sekarang) | Vertex Gemini (baru) |
|---|---|---|
| Endpoint | `POST openrouter.ai/api/v1/chat/completions` | `POST {region}-aiplatform.googleapis.com/v1/projects/{project}/locations/{region}/publishers/google/models/{model}:generateContent` |
| Auth | Header `authorization: Bearer OPENROUTER_API_KEY` | Header `authorization: Bearer {token dari gcp_auth}` |
| Percakapan | `messages: [{role, content}]` | `contents: [{role, parts: [{text}]}]` |
| System prompt | Pesan pertama `role: "system"` | `systemInstruction: {parts: [{text}]}` |
| Temperature/max tokens | Top-level `temperature`, `max_tokens` | Di dalam `generationConfig: {temperature, maxOutputTokens}` |
| Mode JSON | `response_format: {type: "json_object"}` | `generationConfig.responseMimeType: "application/json"` |
| Respons | `choices[0].message.content` | `candidates[0].content.parts[0].text` |

```rust
// kerangka — sesuaikan dengan struct AppError/GenerationRequest yang ada
pub struct VertexGeminiProvider {
    project_id: String,
    region: String,
    auth: gcp_auth::AuthenticationManager,
}

impl VertexGeminiProvider {
    pub async fn new(project_id: String, region: String) -> Result<Self> {
        let auth = gcp_auth::AuthenticationManager::new().await?;
        Ok(Self { project_id, region, auth })
    }
}

// generate(): bangun body {systemInstruction, contents, generationConfig}
// di atas, POST dgn header Authorization dari auth.get_token(&["https://www.googleapis.com/auth/cloud-platform"]),
// parse candidates[0].content.parts[0].text
```

### 6.4 — Pasang provider kedua di `state.rs`

Jangan ganti `ai_provider` yang ada (dipakai OCR/STT/TTS) — tambah field baru `text_ai_provider`, lalu alihkan 7 pemanggil teks (grep `state.ai_provider.as_ref()` di `quiz_generation.rs`, `lesson_plan_ai.rs`, `live_chat.rs`, dan file evaluasi writing/speaking/grammar) ke `state.text_ai_provider.as_ref()` — bukan mengganti satu provider untuk semua, karena OCR/STT/TTS masih butuh OpenRouter.

- [ ] `AppState` punya field baru `text_ai_provider: Arc<dyn AIProvider>`, diisi `VertexGeminiProvider` di `main.rs`.
- [ ] 7 call-site teks (bukan OCR/STT/TTS) sudah dialihkan — grep ulang `state.ai_provider` setelah selesai untuk pastikan sisanya memang cuma OCR/STT/TTS.
- [ ] `FakeAIProvider` di test suite TIDAK berubah — provider asli cuma dipasang di `main.rs`, jadi semua test integrasi yang sudah ada tetap pakai fake seperti biasa.
- [ ] `cargo check` dan `cargo test --lib` lolos setelah semua perubahan di atas.

> **Perhatikan** — `resolve_max_tokens()` di `ai_provider.rs` saat ini memanggil `GET openrouter.ai/api/v1/models` untuk membatasi `max_tokens` per model — logika ini spesifik OpenRouter dan tidak berlaku untuk Gemini. Untuk provider Vertex, pakai batas tetap (hardcoded) berdasar limit resmi Gemini 3.8 Flash, jangan panggil fungsi ini.

---

## Fase 7 — Deploy aplikasi

Build kedua aplikasi, jalankan sebagai systemd service (belum ada sama sekali sebelumnya — semua di bawah baru), lalu satu reverse proxy (Caddy) yang otomatis urus TLS.

### 7.1 — `.env` produksi backend

`~/app/backend/.env` di VM:

```bash
DATABASE_URL=postgres://titian:PASSWORD-DARI-2.1@localhost:5432/titian_bun
REDIS_URL=redis://localhost:6379
JWT_ACCESS_SECRET=generate-baru-openssl-rand-hex-32
GOOGLE_CLIENT_ID=dari-Fase-4
BIND_ADDR=127.0.0.1:8090
FRONTEND_ORIGIN=https://app.titianasa.com
OPENROUTER_API_KEY=tetap-dipakai-untuk-OCR-STT-TTS
GCP_PROJECT_ID=dari-Fase-5.3
GCP_REGION=dari-Fase-5.3
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET=...
```

> **Awas** — `BIND_ADDR` diikat ke `127.0.0.1`, bukan `0.0.0.0` — backend hanya boleh diakses lewat Caddy di localhost, tidak langsung dari internet. `JWT_ACCESS_SECRET` WAJIB baru untuk produksi, jangan pakai punya dev lokal.

### 7.2 — Build & systemd untuk backend

```bash
cd ~/app/backend
cargo build --release
```

`/etc/systemd/system/titian-backend.service`:

```ini
[Unit]
Description=Titian Backend
After=network.target docker.service

[Service]
Type=simple
User=USER-VM-KAMU
WorkingDirectory=/home/USER-VM-KAMU/app/backend
EnvironmentFile=/home/USER-VM-KAMU/app/backend/.env
ExecStart=/home/USER-VM-KAMU/app/backend/target/release/titian-backend-rust
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now titian-backend
journalctl -u titian-backend -f
```

- [ ] Backend jalan lewat systemd, log terlihat bersih di `journalctl` (migrasi SQL jalan otomatis di boot pertama — pastikan tidak error di sini).

### 7.3 — Build & systemd untuk frontend

`~/app/frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=https://api.titianasa.com
NEXT_PUBLIC_GOOGLE_CLIENT_ID=dari-Fase-4
```

```bash
cd ~/app/frontend
bun install
bun --bun next build --webpack
```

> **Ingat dari sesi migrasi sebelumnya** — Kalau nanti ganti nilai `NEXT_PUBLIC_*` dan build ulang, `next build` saja kadang tidak cukup — hapus cache dulu: `rm -rf .next/cache`, baru build lagi. Ini sempat bikin login gagal saat migrasi backend Bun→Rust karena origin lama ke-cache.

`/etc/systemd/system/titian-frontend.service` — sama pola dengan backend, `ExecStart`-nya beda:

```ini
ExecStart=/home/USER-VM-KAMU/.bun/bin/bun --bun next start
WorkingDirectory=/home/USER-VM-KAMU/app/frontend
Environment=PORT=3000
```

- [ ] Frontend jalan lewat systemd di port 3000 (localhost saja).

### 7.4 — Caddy (reverse proxy + TLS otomatis)

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | \
  sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | \
  sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update && sudo apt install -y caddy
```

`/etc/caddy/Caddyfile` — TLS Let's Encrypt otomatis, tidak perlu setup manual:

```
app.titianasa.com {
    reverse_proxy localhost:3000
}

api.titianasa.com {
    reverse_proxy localhost:8090
}
```

```bash
sudo systemctl reload caddy
```

- [ ] DNS: A record `app.titianasa.com` dan `api.titianasa.com` mengarah ke IP statis dari Fase 1.2 — propagasi bisa beberapa menit sampai jam.
- [ ] Caddy berhasil menerbitkan sertifikat TLS otomatis (cek `https://app.titianasa.com` tanpa warning browser).

---

## Fase 8 — Verifikasi & cutover

Uji asap sebelum benar-benar mengalihkan trafik.

- [ ] Buka `https://app.titianasa.com`, login pakai Google — berhasil dan data lama (modul, kelas, dsb.) muncul.
- [ ] Coba satu "Generate soal dengan AI" di Quiz Builder — respons datang dari Gemini (cek log backend: `journalctl -u titian-backend -f` saat generate, tidak ada error `aiplatform.googleapis.com`).
- [ ] Coba fitur yang masih pakai OpenRouter — OCR foto soal, dan salah satu fitur audio (speaking room / TTS) — pastikan keduanya tetap jalan (tidak ikut kepindah tanpa sengaja).
- [ ] Cek tabel `ai_tasks` di Postgres — baris baru dengan model Gemini muncul dan berstatus `done`.
- [ ] Dev lokal (`.env`/`.env.local` di mesin sendiri) sudah diputuskan: tetap ke OpenRouter untuk dev sehari-hari, atau ikut pindah ke Vertex juga (butuh `gcloud auth application-default login` di mesin lokal kalau iya).

```bash
# tail cepat kalau ada yang aneh
journalctl -u titian-backend -f
journalctl -u titian-frontend -f
sudo journalctl -u caddy -f
```

---

## Fase 9 — Kontrol biaya trial $300

Supaya trial tidak habis diam-diam sebelum sempat dipakai sungguhan.

- [ ] Pasang budget alert: Console → *Billing → Budgets & alerts → Create budget* — set threshold mis. 50%/90%/100% dari $300, email notifikasi ke akun kamu.
- [ ] Catat tanggal kedaluwarsa trial (biasanya 90 hari dari aktivasi, dicek di Console → Billing) — pasang reminder kalender beberapa hari sebelumnya supaya tidak kaget kalau otomatis nonaktif/upgrade.
- [ ] Cek [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator) untuk estimasi biaya `e2-standard-2` di `asia-southeast2` jalan 24/7 sebulan, dan biaya per-token Gemini 3.8 Flash saat ini — angka resmi berubah dari waktu ke waktu, jangan andalkan angka lama.

> **Info** — Dua pengeluaran terbesar biasanya: (1) VM jalan 24/7 — kalau mau hemat saat belum ada trafik nyata, VM bisa di-stop di luar jam kerja (`gcloud compute instances stop titianasa-app`) karena disk tetap tersimpan walau instance berhenti; (2) volume panggilan Gemini — pantau lewat Console → *Vertex AI → Dashboard* untuk lihat jumlah request/token harian.

---

*Titian Asa · Panduan migrasi GCP*
