# AI Agent Protocol — ALR Development

Paste ini (atau reference file ini) di awal SETIAP sesi AI coding agent (Claude Code, atau lainnya) yang mengerjakan proyek ALR.

## Sebelum mengerjakan apapun
1. Baca `docs/STATE.md` — pahami fase aktif, ticket aktif, blocker, dan daftar larangan.
2. Baca semua file di `docs/adr/` berstatus `Accepted` — jangan mengambil keputusan yang bertentangan dengan ADR manapun tanpa membuat ADR baru yang eksplisit menyatakan `Supersedes: ADR-000X`.
3. Baca ticket aktif di `docs/tickets/phase-N.md` — kerjakan **hanya** acceptance criteria ticket itu. Jangan melebar ke ticket lain dalam sesi yang sama kecuali diminta eksplisit oleh user.
4. Kalau menemukan kebutuhan mengubah struktur yang sudah di-ADR (misal ubah kolom tabel yang sudah dipakai fase lain, ubah routing AI Gateway, ubah permission matrix) — **STOP**, laporkan ke user, jangan langsung eksekusi.
5. Kalau ticket aktif ternyata butuh keputusan yang belum ada ADR-nya — usulkan draft ADR baru dulu, minta konfirmasi user, baru implementasi.

## Selama mengerjakan
- Ikuti alur standar: migration → model → repository → service → handler → route → test (untuk backend); schema → component → integration test (untuk frontend).
- **Backend sedang dimigrasi dari Rust ke Go (ADR-0020, `docs/tickets/phase-51-go-migration.md`).** Sebelum menyentuh backend, cek di tiket itu apakah domain yang dikerjakan sudah diport:
  - Domain **belum diport** → kerjakan di `titian-backend-rust` (masih melayani klien), lalu catat endpoint/migrasi barunya di daftar paritas tiket fase 51.
  - Domain **sudah diport** → kerjakan di `titian-backend-go`. Alurnya: migrasi SQL (`db/migrations/`, salin juga ke repo Rust selama Rust masih aktif) → query (`db/queries/<domain>.sql`, `make sqlc`) → service → handler → `Module()` → test (`testdb.New`) → `make parity`.
  - Tiket port (G0–G15) adalah **port 1:1**: jangan mengubah kontrak, skema, atau aturan bisnis sambil memport.
- Di Go, kontrak galat/JSON hanya lewat `internal/platform/httpx` (`httpx.Error`, `httpx.DecodeJSON`); slice respons selalu diinisialisasi supaya keluar `[]`, bukan `null` (ADR-0020 §4).
- Semua endpoint baru wajib ditambahkan ke `docs/api-contract.md` dengan format yang sama seperti contoh yang sudah ada (request/response/error).
- Semua tabel baru/perubahan tabel wajib disinkronkan ke `docs/domain-model.md`.
- Ikuti aturan konsistensi error/pagination/timestamp yang sudah didefinisikan di `docs/api-contract.md` — jangan buat pola baru per endpoint.

## Di akhir sesi (WAJIB, bukan opsional)
1. Update status ticket terkait di `docs/tickets/phase-N.md` (todo → in-progress → blocked/done).
2. Update `docs/STATE.md`:
   - Ticket terakhir dikerjakan + progres persentase kasar
   - Next action yang jelas untuk sesi berikutnya
   - Blocker baru kalau ada
   - Deviasi dari rencana kalau ada penyimpangan dari ADR/ticket asli
3. Kalau ada keputusan arsitektur baru diambil selama sesi → tulis sebagai ADR baru bernomor urut berikutnya, status `Accepted` setelah dikonfirmasi user.
4. Jangan tinggalkan kode yang tidak lulus test di branch utama — kalau ticket belum selesai, tandai `in-progress` dan jelaskan sisa kerjaan di `docs/STATE.md`, bukan commit kode setengah jadi tanpa catatan.

## Definition of Done (berlaku untuk semua ticket, tambahan di luar acceptance criteria spesifik tiap ticket)
- [ ] Kode terimplementasi sesuai acceptance criteria ticket
- [ ] Unit test untuk logic inti (khususnya mastery/FRSS/scoring) lulus
- [ ] Integration test untuk endpoint baru lulus
- [ ] `docs/api-contract.md` dan/atau `docs/domain-model.md` diupdate kalau relevan
- [ ] `docs/STATE.md` diupdate
- [ ] Tidak ada breaking change ke tabel/endpoint yang dipakai fase lain tanpa ADR baru
