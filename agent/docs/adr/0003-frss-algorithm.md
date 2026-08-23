# ADR-0003: FRSS (Forgetting-Resistant Spaced Scheduling) Algorithm v1
Status: Accepted
Date: 2026-08-22
Supersedes: -
Superseded by: -

## Context
`frss_schedule` menentukan kapan sebuah concept harus direview lagi oleh user (mengisi `/review-queue`). Butuh algoritma yang terbukti (SM-2 base) tapi disesuaikan supaya tidak menghukum user terlalu keras (sesuai prinsip di dokumen awal: "review tidak harus 1 jam", micro-learning, jangan punitive untuk Kids).

## Decision

Modifikasi SM-2, per (user, concept):

### State
```
ease_factor   float, default 2.5, range [1.3, 2.8]
interval_days float, default 1.0
due_at        timestamptz
last_result   enum(recalled, partial, forgot)
```

### Update rule setiap kali concept direview (dipicu dari learning_event hasil review, bukan attempt biasa)
```
IF result == recalled:
    interval_days = interval_days * ease_factor
    ease_factor   = min(2.8, ease_factor + 0.1)

IF result == partial:
    interval_days = interval_days * 1.2
    ease_factor   = max(1.3, ease_factor - 0.15)

IF result == forgot:
    interval_days = 1.0
    ease_factor   = max(1.3, ease_factor - 0.3)

due_at = now() + interval_days (dalam hari, dibulatkan ke jam terdekat)
```

`result` ditentukan dari correctness attempt terkait: `c_i >= 0.8 → recalled`, `0.4 <= c_i < 0.8 → partial`, `c_i < 0.4 → forgot` (threshold config-driven).

### Contoh 5 siklus (mulai ease=2.5, interval=1)
| Siklus | Result | Interval baru | Ease baru | Due dalam |
|---|---|---|---|---|
| 1 | recalled | 1 * 2.5 = 2.5 hari | 2.6 | 2.5 hari |
| 2 | recalled | 2.5 * 2.6 = 6.5 hari | 2.7 | 6.5 hari |
| 3 | forgot   | 1 hari (reset)       | 2.4 | 1 hari |
| 4 | recalled | 1 * 2.4 = 2.4 hari   | 2.5 | 2.4 hari |
| 5 | partial  | 2.4 * 1.2 = 2.9 hari | 2.35| 2.9 hari |

### Anti-punitive rules (khusus supaya tidak terasa menghukum)
1. **Minimum interval floor** = 1 hari, walau `forgot` berkali-kali — tidak ada "review lagi 5 menit lagi" yang bikin frustrasi.
2. **Batch, bukan per-concept popup**: `/review-queue` mengembalikan maks N item per sesi (default 10, config), diprioritaskan berdasarkan `due_at` terlama + `mastery.score` terendah — bukan seluruh backlog sekaligus (selaras dengan konsep "Micro Learning" di dokumen awal).
3. Concept yang sama tidak boleh direview >1x dalam periode `min_gap_hours` (default 4 jam), walau sistem lain memicu — mencegah spam review dari beberapa modul sekaligus.

## Alternatives considered
- **SM-2 murni tanpa floor/batasan** — ditolak, terlalu punitive untuk retensi harian (risiko user drop karena kebanjiran review).
- **FSRS (algoritma modern berbasis ML)** — dicatat sebagai kandidat upgrade jangka panjang setelah cukup data review historis untuk melatih parameternya; SM-2 modifikasi dipilih untuk MVP karena predictable & mudah didebug.

## Consequences
- (+) Semua threshold config-driven, gampang dituning per hasil A/B test retention.
- (+) `min_gap_hours` dan cap per sesi mencegah UX yang terasa seperti hukuman.
- (−) Ease factor per concept, bukan per user global — artinya `frss_schedule` bisa jadi tabel besar (1 baris per user x concept). Perlu index `(user_id, due_at)` sejak awal.
