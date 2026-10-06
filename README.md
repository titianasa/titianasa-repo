# Titian Asa — repo utama (dokumentasi)

Repo ini memuat **dokumentasi dan bahan rancangan** seluruh produk. Kode tiap aplikasi ada di repo masing-masing
(folder-folder itu ada di samping repo ini di mesin pengembangan, tetapi tidak di-commit di sini).

| Repo | Isi | Deploy |
|---|---|---|
| **`titianasa-repo`** (ini) | `agent/` (ADR, tiket, STATE, kontrak API, model domain), `outputs/` (rancangan kurikulum), `*.md` di root | — |
| `titianasa-web` (`titian-web/`) | Web Titian (Next.js) | Vercel, otomatis dari GitHub |
| `kampung-bahasa` (`game/`) | Game Kampung Bahasa Pare (Next.js) | Vercel, otomatis dari GitHub |
| repo backend (`titian-backend-go/`) | API + worker Go, migrasi, konten Pare ter-embed, konfigurasi LiveKit | VPS Hetzner, `./deploy.sh` |

Mulai dari sini:
- Status terkini proyek: [`agent/docs/STATE.md`](agent/docs/STATE.md)
- Cara repo disusun dan dideploy: [`agent/docs/struktur-repo-dan-deploy.md`](agent/docs/struktur-repo-dan-deploy.md)
- Keputusan arsitektur: [`agent/docs/adr/`](agent/docs/adr/) · tiket: [`agent/docs/tickets/`](agent/docs/tickets/)
- Kontrak API: [`agent/docs/api-contract.md`](agent/docs/api-contract.md) · model domain: [`agent/docs/domain-model.md`](agent/docs/domain-model.md)

Rahasia (`.env`, kunci API, `Credential.md`) tidak pernah di-commit; lihat `.gitignore` tiap repo.
