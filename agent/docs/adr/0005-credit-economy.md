# ADR-0005: Credit Economy v1
Status: Accepted
Date: 2026-08-22
Supersedes: -
Superseded by: -

## Context
Dokumen awal menegaskan: Diamond/Credit bukan sekadar "uang untuk beli AI", tapi juga reward loop dan revenue stream tidak langsung. Perlu unit yang konsisten menghubungkan `ai_tasks.cost` (biaya nyata ke provider) dengan `credits.balance` (yang dilihat/dipakai user).

## Decision

### Unit
1 **Credit** = satuan internal, **tidak dipatok 1:1 ke Rupiah** secara publik (nama yang dilihat user boleh "Diamond" — pemisahan nama internal vs display sudah diputuskan di dokumen awal). Secara internal: `1 credit ≈ Rp 10` (rate ini hidup di config `credit_to_idr_rate`, dipakai untuk menghitung margin, bukan ditampilkan ke user).

### Pricing table AI task → credit cost (default, config-driven)
| AITask | Estimasi cost provider (token) | Credit charge ke user |
|---|---|---|
| GrammarEvaluation | rendah | 1 credit |
| WritingEvaluation | sedang | 5 credit |
| SpeakingEvaluation | sedang-tinggi (audio) | 8 credit |
| ExplanationGeneration | rendah | 1 credit |
| LiveTutor (per menit) | tinggi | 10 credit/menit |
| LessonGeneration / QuestionGeneration / CurriculumGeneration | tinggi, tapi ini cost platform bukan cost user | 0 credit (dibebankan ke platform, bukan wallet user — ini task admin/content, bukan task learner) |

Margin minimum default: charge ke user ≥ 1.5x estimasi cost provider (config `margin_multiplier`), dicek otomatis saat routing table diupdate — bukan hardcode di kode, supaya bisa direspons cepat kalau harga provider berubah.

### Subscription allowance
Tiap tier subscription dapat **alokasi credit periodik** (bukan "unlimited AI" — sudah diputuskan eksplisit di dokumen awal):
```
Free        : 0 credit/bulan gratis, hanya bisa beli/dapat dari gamification
Plus        : 100 credit/bulan
Pro         : 300 credit/bulan
```
(Angka ini contoh awal, bukan final bisnis — tapi mekanismenya yang dikunci: allowance masuk sebagai `transactions.type = earn`, `reference = 'subscription:{period}'`, bukan langsung menambah "allowance" terpisah dari `credits.balance`. Satu sumber kebenaran saldo.)

### Expiry
Credit dari subscription allowance **expire di akhir periode berikutnya** (grace 1 bulan) supaya tidak menumpuk tak terbatas; credit dari pembelian langsung **tidak expire**. Field tambahan di `transactions`: `expires_at` (nullable — null berarti tidak expire).

### Anti-abuse
- Rate limit: maksimum N credit spend per jam per user (default 50), dicek sebelum request AI dieksekusi, bukan sesudah — supaya tidak ada task jalan lalu ditolak setelah biaya sudah keluar.
- Setiap `ai_tasks.status = failed` (gagal validasi output, lihat ADR-0004) **tidak** memicu `transactions.type = spend` — user tidak dibebankan untuk hasil AI yang gagal validasi.
- Refund manual (`transactions.type = refund`) selalu butuh `reference` yang jelas (misal `refund:ai_task:{id}`) untuk audit.

### Wallet tutor (dua sisi ledger)
Untuk marketplace tutor (Phase 7), dipakai tabel `transactions` yang sama dengan `type` tambahan `payout_earned`/`payout_withdrawn`, split 30/70 dihitung saat `type = payout_earned` dibuat dari transaksi booking siswa — bukan tabel ledger terpisah, supaya audit trail konsisten satu tempat.

## Alternatives considered
- **Credit 1:1 dengan Rupiah dan ditampilkan sebagai harga** — ditolak, dokumen awal eksplisit ingin credit terasa seperti currency game (Diamond), bukan harga API mentah.
- **"Unlimited AI" untuk semua tier subscription** — ditolak eksplisit di dokumen awal (risiko biaya tak terkendali).
- **Allowance disimpan sebagai kolom terpisah dari balance** — ditolak, memecah sumber kebenaran saldo jadi 2 tempat; dipilih semua lewat `transactions` yang di-agregasi jadi `credits.balance`.

## Consequences
- (+) Satu sumber kebenaran saldo (`transactions` → agregat `credits.balance`), audit gampang.
- (+) Margin kelihatan eksplisit di config, gampang direview kalau biaya provider naik.
- (−) Expiry logic butuh job berkala (cron) untuk menandai transaksi expired dan mengurangi balance — dicatat sebagai ticket tersendiri di Phase 6 (Gamification & Economy).
