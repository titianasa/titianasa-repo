# Struktur repo dan deploy

Dibuat 2026-10-07. Menjelaskan di mana kode dan dokumentasi tinggal, dan bagaimana tiap bagian dideploy.

## Empat repo

```
alr/                         ← repo utama "titianasa-repo": dokumentasi saja
├── agent/                   ADR, tiket, STATE.md, kontrak API, model domain, alat QA
├── outputs/                 rancangan kurikulum, pemetaan jalur ujian, kalibrasi
├── *.md                     catatan di root
├── titian-web/     (repo sendiri: titianasa-web)      ← tidak di-commit di sini
├── game/           (repo sendiri: kampung-bahasa)     ← tidak di-commit di sini
└── titian-backend-go/ (repo backend)                  ← tidak di-commit di sini
    ├── cmd/ internal/ db/ data/pare/   API + worker Go, migrasi, konten Pare
    └── livekit/                        server media suara (hetzner/ dipakai; railway-legacy/ arsip)
```

Repo-repo itu sengaja terpisah: tiap layanan punya jalur deploy sendiri, dan platform deploy (Vercel) mengenali project
berdasarkan repo + folder root + branch. Memisahkan repo membuat jalur deploy yang ada tidak perlu diubah.

Identitas git semua repo: `user.name titianasa`, `user.email app.titianasa@gmail.com` (diset lokal per repo; identitas
global mesin ini bukan untuk proyek ini).

## Deploy per bagian

**Web (`titian-web`) dan game (`game`)** — Vercel, otomatis tiap push ke branch produksi di GitHub. Tidak ada pipeline
lain. Catatan dari 2026-10-06: Vercel menjalankan `next build`, yang ikut me-type-check `scripts/`; script di `game/scripts`
tidak boleh merujuk folder tetangga (`../../titian-backend-go/...`) karena di Vercel hanya repo itu yang di-clone. Karena
itu `scripts/` dikeluarkan dari `tsconfig.json` (cek lokal: `bun run typecheck:scripts`).
`NEXT_PUBLIC_API_URL` di Vercel = `https://api.titianasa.com`; origin web harus ada di `FRONTEND_ORIGIN` backend
(`https://titianasa.com`, `https://pare.titianasa.com`).

**Backend (`titian-backend-go`) dan LiveKit** — VPS Hetzner `ubuntu-4gb-nbg1-1` (`ssh hetzner`), dibagi dengan proyek lain
(parelabs, nanyang) lewat Caddy bersama `parelabs_caddy` dan jaringan Docker `proxy`.

```
cd titian-backend-go
./deploy.sh sync          # salin docker-compose.prod.yml ke /home/debian/titian-backend
./deploy.sh local-build   # bangun image di sini, kirim ke VPS (docker save | ssh docker load)
./deploy.sh restart       # up -d api + worker, lalu cek /health
./deploy.sh status | health
```

Jangan pakai `./deploy.sh full` kecuali memang perlu: ia juga menyentuh Caddy milik parelabs.
Migrasi database dijalankan otomatis oleh biner saat boot (tabel `_sqlx_migrations`).
`ADMIN_EMAILS` (email dipisah koma) menentukan akun `platform_admin` untuk Admin Pusat; tanpa itu produksi tidak punya admin. Rahasia produksi hanya ada di `/home/debian/titian-backend/.env` di server (contoh nama variabel: `.env.prod.example`).
Rollback: simpan `docker-compose.prod.yml` sebelumnya, lalu `docker compose up -d --pull never` dengan image sebelumnya
(image lama tetap ada di server sampai dihapus).
LiveKit: `titian-backend-go/livekit/hetzner/docker-compose.yml`, `livekit.yaml` dibuat dari `livekit.yaml.example` di server.

## Bekerja dari Claude Cloud / mesin lain

Hubungkan GitHub ke repo yang akan dikerjakan; sesi cloud meng-clone satu repo per sesi. Untuk pekerjaan lintas repo
(mis. fitur Pare yang menyentuh game dan backend), clone repo-repo itu berdampingan dalam satu folder seperti di mesin
pengembangan, dengan repo utama sebagai induknya — script `game/scripts/*` dan dokumen mengandalkan susunan sejajar
itu (`../titian-backend-go/data/pare/...`). Kunci dan `.env` tidak ikut repo; berikan lewat variabel lingkungan sesi.

## Di mana dokumentasi ditulis

Semua dokumentasi (ADR, tiket, STATE, catatan rancangan) ditulis di **repo utama**, termasuk dokumentasi untuk backend dan
game. README di tiap repo hanya menjelaskan cara menjalankan repo itu.
