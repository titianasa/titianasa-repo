# ADR-0002: Mastery Formula v1
Status: Accepted
Date: 2026-08-22
Supersedes: -
Superseded by: -

## Context
`masteries.score` (0-100) harus merefleksikan seberapa kuat user menguasai satu concept, dipakai oleh: dashboard progress, weakness detection, recommendation engine, dan FRSS trigger. Formula harus **config-driven** (parameter bisa di-tune tanpa migrasi) karena di dokumen awal disebutkan eksplisit ini belum final dan akan dikalibrasi dengan data nyata.

## Decision

### Input per concept per user
Semua `learning_events` dengan `event_type = 'question_answered'` yang terhubung (lewat `question_concepts`) ke concept tersebut, diurutkan dari terbaru.

Untuk tiap attempt *i*:
- `c_i` = correctness, 0.0–1.0 (1.0 untuk benar penuh, partial score untuk tipe soal seperti writing/speaking)
- `d_i` = difficulty soal, 0.0–1.0 (dari `questions.difficulty`)
- `age_i` = umur attempt dalam hari sejak `created_at`

### Recency weight (exponential decay)
```
w_i = exp(-λ * age_i)          λ = 0.05 (default, config-driven)
```
λ = 0.05 berarti attempt 14 hari lalu masih berbobot ~0.5, attempt 60 hari lalu turun ke ~0.05 — cukup lama untuk stabil, cukup cepat untuk menangkap perubahan kemampuan.

### Weighted score
```
raw = Σ(w_i * (0.5 + 0.5*d_i) * c_i) / Σ(w_i * (0.5 + 0.5*d_i))
```
Faktor `(0.5 + 0.5*d_i)` membuat soal sulit dijawab benar berkontribusi lebih besar (maks 2x bobot soal termudah), tapi soal termudah tetap punya bobot minimum 0.5 — supaya concept dengan soal mudah saja tidak dianggap 0.

### Mastery score final
```
mastery_score = round(raw * 100)   -- 0-100
```

### Confidence
```
confidence = min(1.0, jumlah_attempt_unik / N_min)   N_min = 5 (default)
```
Dashboard/recommendation **tidak menampilkan mastery sebagai final** kalau `confidence < 0.6` — ditampilkan sebagai "Belum cukup data", supaya tidak menyesatkan user baru dengan 1 attempt kebetulan benar.

### Contoh perhitungan manual
User A, concept "present_simple", 3 attempt:
| # | hari lalu | correct (c) | difficulty (d) | w = e^(-0.05*age) | bobot = w*(0.5+0.5d) |
|---|---|---|---|---|---|
| 1 | 1  | 1.0 | 0.6 | 0.951 | 0.741 |
| 2 | 10 | 0.0 | 0.4 | 0.607 | 0.425 |
| 3 | 20 | 1.0 | 0.8 | 0.368 | 0.331 |

```
raw = (0.741*1.0 + 0.425*0.0 + 0.331*1.0) / (0.741+0.425+0.331)
    = 1.072 / 1.497 = 0.716
mastery_score = 72
confidence = min(1, 3/5) = 0.6  → ditampilkan tapi dekat batas
```

### Trigger perhitungan ulang
`masteries` di-*upsert* async setiap ada `learning_event` baru untuk concept terkait (bukan cron batch) — supaya dashboard & recommendation selalu real-time.

## Alternatives considered
- **Simple moving average tanpa decay** — ditolak, tidak menangkap "lupa" / perbaikan terbaru user.
- **Bayesian Knowledge Tracing (BKT) penuh** — ditunda, lebih akurat tapi butuh kalibrasi parameter per concept dengan data historis yang belum ada di MVP. Dicatat sebagai kandidat ADR lanjutan setelah cukup data.

## Consequences
- (+) Semua parameter (`λ`, faktor difficulty, `N_min`) hidup di config, bisa dituning tanpa migration.
- (+) Formula sederhana, mudah dijelaskan ke user ("kenapa mastery saya turun") — penting untuk trust.
- (−) Belum menangani forgetting curve secara eksplisit di skor mastery itu sendiri (itu tugas FRSS di ADR-0003, dipisahkan sengaja).
- Rencana revisit: setelah 3 bulan data attempt real, evaluasi apakah upgrade ke BKT/IRT diperlukan.
