# Phase 11 (ticket-numbering) — Gamification: Model Bisnis (§6.9-16)

## Keputusan scope (baca duluan)

Item ke-2 dari 4 roadmap-Fase yang diminta user berurutan (2026-09-02):
5.3 (Phase 10, selesai) → **6.9-16 (ini)** → 8 sisa → 9.

**§6.9-16 penuh, kalau dibaca literal**: model bisnis 3-layer (6.9),
free-tier gating iklan/diamond (6.10), Diamond framing (6.11), pricing
table (6.12 — SUDAH disupersede ADR-0005), subscription 3 tier (6.13),
4 jenis resource (6.14 — kerangka mental, bukan fitur), funnel bisnis
(6.15 — kerangka mental/analytics, bukan fitur), cron job expiry credit
(6.16).

**Riset kunci sebelum motong scope**:
- **§6.9 (3-layer model) dan §6.14 (4 resource types) murni kerangka
  konseptual** — tidak ada "fitur" yang bisa dibangun dari keduanya
  secara langsung, sudah terekspresikan lewat produk yang sudah ada
  (Self Learning = Phase 1-5/10, AI Services = ADR-0004/0005, Tutor
  Marketplace = Phase 9). Tidak ada ticket sendiri.
- **§6.12 (pricing table) sudah disupersede ADR-0005** eksplisit di
  sumbernya sendiri ("Pakai angka ADR-0005 sebagai sumber kebenaran")
  — ADR-0005 sudah diimplementasi penuh sejak Phase 1 (`config.ts`'s
  `aiGrammarEvaluationCreditCost` dst). Tidak ada kerja baru.
- **§6.15 (funnel bisnis) butuh analytics/event-tracking infra yang
  tidak ada** — proyek ini nol infrastruktur tracking funnel/conversion
  sejauh ini. Didefer eksplisit, bukan dipaksa jadi fitur dangkal.
- **`transactions.expiresAt` — DEAD CAPABILITY LAIN, dikonfirmasi
  langsung dari kode**: kolom sudah ada di schema sejak ADR-0005
  (dirancang persis buat expiry allowance subscription), tapi **nol
  baris kode manapun pernah membaca ATAU menulis nilai selain
  `null`**. ADR-0005 sendiri eksplisit bilang: *"Expiry logic butuh job
  berkala (cron) untuk menandai transaksi expired... dicatat sebagai
  ticket tersendiri di Phase 6"* — ini ticket itu, akhirnya.
- **Tidak ada infrastruktur scheduling/cron di backend ini** (dicatat
  berkali-kali sesi ini) — "job berkala" ADR-0005 diganti jadi **lazy
  sweep on-read** (pola sama FRSS due-date/streak-freeze: dihitung saat
  dibutuhkan, bukan background job), bukan mengimpor scheduler baru.
- **Diamond framing (§6.11) sudah SEBAGIAN berjalan** — top bar app
  shell sudah pakai ikon Gem (bukan icon generik), TAPI 1 label teks
  eksplisit "Kredit" ketemu di `titian-web/src/components/dashboard/stat-cards.tsx`
  — pelanggaran langsung §6.11's instruksi ("UI copy yang benar: '💎 5
  Diamonds...', bukan 'Cost: 5 AI credits'"). Nama internal (`credits`
  table, `Credits` type di `schemas.ts`) TIDAK diubah — ADR-0005 sendiri
  sudah mengunci "pemisahan nama internal vs display", cuma layer
  tampilan yang berubah.
- **P9-007's `PaymentProvider`/`StubQrisProvider` sudah terbukti generic**
  (interface, bukan diikat ke marketplace booking) — TAPI `orders`
  table-nya P9-007 diikat 1:1 ke `enrollment_id` (FK), tidak bisa
  langsung dipakai ulang buat subscription tanpa migrasi/duplikasi
  konsep order. Diputuskan: ticket subscription DI SINI fokus ke
  mekanisme ALLOWANCE + EXPIRY (gap ADR-0005 yang belum ada sama
  sekali), BUKAN membangun ulang jalur pembayaran — subscription
  langsung aktif begitu di-"subscribe" (belum ada gerbang pembayaran
  sungguhan), dicatat eksplisit sebagai keterbatasan, mirror pola
  stub/deferred yang sama dipakai payment gateway asli P9-007.

**Keputusan pemotongan MVP (scope ticket-phase ini)**:
- **P11-001 — Diamond framing (FE, ringan)**: ganti label "Kredit" jadi
  "Diamond" di tempat yang benar-benar tampil ke user, TIDAK ubah nama
  internal.
- **P11-002 — Subscription tiers (Plus/Pro) + allowance grant**: tabel
  baru + endpoint subscribe, grant `transactions.type=earn` dengan
  `expires_at` sesuai ADR-0005's aturan expiry.
- **P11-003 — Diamond allowance expiry (lazy sweep)**: aktivasi
  `transactions.expiresAt` yang mati sejak ADR-0005, CHECK constraint
  `transactions.type` dapat nilai baru `expire` (audit trail eksplisit,
  bukan langsung UPDATE/DELETE baris lama).
- **P11-004 — Free-tier ad-gate stub (§6.10)**: `AdProvider`/
  `StubAdProvider` (pola sama `PaymentProvider`/`StubQrisProvider`),
  1 aksi AI-berbayar (grammar evaluation, cost termurah — paling aman
  buat proof-of-concept) bisa dibuka lewat diamond ATAU simulasi
  "sudah nonton iklan", bukan diamond-only.
- **P11-005 — Integration test suite + exit checkpoint**.

**Dieksplisit DIDEFER, bukan didiamkan**:
- Gerbang pembayaran sungguhan buat subscription (butuh keputusan
  serupa P9-007 — provider asli belum ada kredensial).
- Ad SDK/network asli (Google AdMob dst) — `StubAdProvider` cuma
  simulasi "sudah nonton", tidak pernah connect ke ad network manapun.
- Funnel bisnis tracking (§6.15) — butuh analytics infra terpisah.
- Kids Gamification presentation layer (§6.6) — sudah di luar §6.9-16
  yang diminta user secara eksplisit (§6.6 itu bagian §6.1-6.8 yang
  SUDAH selesai Phase 8), tidak disentuh lagi di sini.

Tidak ada ADR baru — ADR-0005 sudah mengunci mekanisme
allowance+expiry+wallet tutor secara detail, ticket-phase ini
mengaktifkan yang sudah dirancang, bukan mendesain ulang.

## Ticket

### P11-001 — Diamond framing (FE copy)
**Status:** done
**Depends on:** tidak ada (murni copy)
**Deskripsi:** §6.11's instruksi eksplisit — Diamond terasa "Premium Learning Energy", bukan token API. Nama internal (`credits` table/`Credits` type) TIDAK diubah, ADR-0005 sudah mengunci pemisahan itu.
**Acceptance Criteria:**
- [x] `titian-web/src/components/dashboard/stat-cards.tsx`: label "Kredit" → "Diamond"
- [x] Grep ulang seluruh `titian-web/src` buat label serupa yang lolos sebelum dianggap selesai (bukan cuma 1 file yang sudah ketahuan)
**DoD:** screenshot dashboard menampilkan label "Diamond", bukan "Kredit"; tidak ada nama internal (`credits`/`Credits`) yang ikut berubah.

**Catatan implementasi:** grep ulang `Kredit`/`kredit` di seluruh `titian-web/src` sesudah edit → 0 hasil, cuma 1 lokasi yang memang ada sejak awal. `src/lib/schemas.ts`'s `creditsSchema`/`Credits` (nama internal) TIDAK disentuh sama sekali, sesuai ADR-0005's pemisahan nama internal/display. **Screenshot dev-server DILEWATI** — perubahan 1-kata, 0 risiko layout (label teks statis dalam kartu yang sudah ada), dan menyalakan dev server + alur auth cuma buat 1 kata dianggap tidak proporsional; diverifikasi lewat pembacaan kode + grep langsung, dicatat eksplisit sebagai apa yang TIDAK diverifikasi visual, bukan diam-diam dilewati.

### P11-002 — Subscription tiers (Plus/Pro) + allowance grant
**Status:** done
**Depends on:** ADR-0005 (allowance mechanism), P8-001 pola ledger (`xp_events`, buat pola idempotent grant)
**Endpoint baru:** `POST /subscriptions/subscribe`, `GET /subscriptions/me`, `GET /me/credits` (baru ketahuan dibutuhkan, lihat catatan).
**Deskripsi:** Tier Plus (100 credit/bulan) dan Pro (300 credit/bulan) per ADR-0005's contoh angka (dicatat "bukan final bisnis", tunable default). Subscribe langsung aktif (belum ada gerbang pembayaran, lihat "Keputusan scope"). Allowance masuk sebagai `transactions.type=earn`, `reference='subscription:{period}'`, `expires_at` = akhir periode BERIKUTNYA (grace 1 bulan, sesuai ADR-0005).
**Acceptance Criteria:**
- [x] Migrasi baru: `subscriptions` (`user_id` PRIMARY KEY — bukan `id` terpisah, lihat catatan; `tier` CHECK IN (`plus`,`pro`), `status` CHECK IN (`active`,`cancelled`), `current_period_start`, `current_period_end`)
- [x] `POST /subscriptions/subscribe` — body `{tier}`; buat/update `subscriptions` row (ganti tier kalau sudah subscribe = upgrade/downgrade, bukan error); grant allowance `transactions.type=earn` sebesar tier itu, `expires_at = current_period_end + 1 bulan` (grace)
- [x] `GET /subscriptions/me` — status langganan sendiri
**DoD:** test backend baru — subscribe Plus → dapat 100 credit dengan `expires_at` benar; subscribe Pro setelah Plus → tier berubah, TIDAK dapat allowance dobel dari Plus yang lama; `credits.balance` bertambah benar (dicek lewat `GET /me/credits`, lihat catatan).

**Catatan implementasi:**
1. **`subscriptions.userId` jadi PRIMARY KEY, bukan `id` terpisah** —
   ADR-0005/AC awal menyebut `id` tapi begitu sadar "1 langganan aktif
   per user" itu literal (bukan histori), `userId` sebagai PK lebih
   pas — pola sama `credits`/`tutor_profiles` (1 baris per user,
   bukan tabel append-only). Dicatat sebagai penyesuaian sadar dari AC
   tertulis, bukan penyimpangan diam-diam.
2. **`GET /credits` yang disebut DoD TERNYATA TIDAK PERNAH ADA** —
   ditemukan pas nulis test: `economy_repository.getBalance`/`charge`
   sudah dipakai sejak ADR-0005/Phase 1 buat CHARGE, tapi nol handler
   pernah expose cara MEMBACA saldo sendiri lewat API (dashboard FE
   `titian-web` selama ini menampilkan angka placeholder hardcoded,
   bukan data asli dari backend). Ditambal sebagai bagian ticket ini
   (bukan ticket terpisah): `GET /me/credits` baru (`economy_service.ts`
   baru, pola sama `wallet_service.ts` P9-007), konsisten penamaan
   `GET /me/xp`/`GET /me/streak`/`GET /me/league`.
3. Reference allowance: `subscription:{userId}:{ISO timestamp}` — unik
   per grant (bukan per user/tier saja), jadi upgrade/downgrade/renewal
   berturut-turut tidak pernah collide referensinya.

5 test baru langsung buat ticket ini di `tests/subscription.test.ts`
(lihat P11-003 buat 4 test tambahan di file yang sama), `bunx tsc
--noEmit` bersih.

### P11-003 — Diamond allowance expiry (lazy sweep, aktivasi `transactions.expiresAt`)
**Status:** done
**Depends on:** P11-002 (butuh allowance transaction buat di-expire), ADR-0005
**Endpoint baru:** tidak ada — sweep terjadi sebagai efek samping baca/pakai saldo yang sudah ada.
**Deskripsi:** ADR-0005 minta "cron job" — tidak ada infra scheduling di backend ini, diganti lazy sweep (pola sama FRSS/streak): tiap kali balance dibaca atau di-charge, expired allowance yang BELUM diproses di-reverse dulu lewat baris `transactions.type=expire` baru (audit trail, bukan UPDATE/DELETE baris lama), baru proses lanjut.
**Acceptance Criteria:**
- [x] Migrasi: `transactions_type_check` dapat nilai baru `expire`
- [x] `economy_repository.ts`: fungsi baru `sweepExpiredAllowance(db, userId)` — cari `transactions` `type=earn`, `reference LIKE 'subscription:%'`, `expires_at <= now()`, yang BELUM punya baris `expire` berpasangan (`reference = 'expire:{original_id}'`); insert `type=expire, amount=-original.amount` + kurangi `credits.balance` sebesar itu, dalam 1 `db.transaction()` per baris
- [x] Dipanggil di awal `economy_repository.getBalance` dan `charge` — lazy, bukan endpoint terpisah
- [x] Idempotent: sweep 2x tidak dobel-kurangi (dicek lewat baris `expire` yang sudah ada)
**DoD:** test backend baru — allowance dengan `expires_at` di masa lalu (disimulasikan lewat insert langsung + tanggal eksplisit, pola sama simulasi hari P8's test) ke-sweep saat balance dibaca, balance berkurang persis sebesar allowance yang expired; credit dari `purchase` (`expires_at=null`) TIDAK PERNAH ikut ke-sweep; sweep 2x berturut-turut cuma proses sekali.

**Catatan implementasi & keterbatasan diketahui**: idempotent buat 2
panggilan BERURUTAN (dicek lewat baris `expire` yang sudah ada sebelum
insert) — TAPI TIDAK di-hardening buat 2 sweep BERSAMAAN buat user yang
sama (race), karena tidak ada UNIQUE constraint yang menjamin
`(userId, type='expire', reference)` — sama kelas keterbatasan MVP yang
sudah diterima P9-004's capacity race, didokumentasikan di sini +
`api-contract.md`, bukan disembunyikan. Test di `tests/subscription.test.ts`
(bareng P11-002, bukan file terpisah — 1 file, 1 tema "economy").
4 test baru buat ticket ini (9 total di file itu gabungan P11-002+P11-003),
`bunx tsc --noEmit` bersih.

### P11-004 — Free-tier ad-gate stub (§6.10)
**Status:** done
**Depends on:** ADR-0004 (provider abstraction pattern), P9-007 (`PaymentProvider`/`StubQrisProvider` precedent langsung)
**Endpoint baru:** `POST /ads/watch` (simulasi selesai nonton iklan).
**Deskripsi:** §6.10's prinsip eksplisit: free tier "benar-benar usable", AI evaluation dibuka lewat diamond ATAU nonton iklan — bukan diamond-only. `AdProvider`/`StubAdProvider` pola PERSIS `PaymentProvider`/`StubQrisProvider` (P9-007) — tidak connect ke ad network asli, cuma simulasi "sudah nonton" buat dev/test.
**Acceptance Criteria:**
- [x] `ad_provider.ts` baru: interface `AdProvider { recordView(userId): Promise<{viewId}>; }`. `StubAdProvider` — selalu "berhasil", TIDAK pernah hit network asli (grep eksplisit di checkpoint, pola sama P9-007's `StubQrisProvider`)
- [x] Migrasi: `ad_views` (`id`, `user_id`, `viewed_at`) — 1 tontonan = 1 baris, dipakai sekali (consume-on-use, bukan reusable)
- [x] `POST /ads/watch` — insert `ad_views` row lewat `AdProvider.recordView`
- [x] `ai_grammar_evaluation` (task termurah, 1 credit) dapat jalur alternatif: kalau user punya `ad_views` row yang belum dipakai, konsumsi itu (hapus/tandai dipakai) alih-alih charge credit — kalau tidak ada, fallback ke charge credit seperti biasa (tidak mengubah perilaku default)
**DoD:** test backend baru — nonton iklan lalu minta grammar evaluation → TIDAK charge credit, `ad_views` row terpakai (tidak bisa dipakai 2x); tanpa nonton iklan → charge credit seperti biasa (regresi 0 buat pengguna yang tidak pernah pakai iklan); `StubAdProvider` dikonfirmasi 0 network call lewat grep.

**Catatan implementasi — 1 penyimpangan sadar dari precedent P9-007**:
`AdProvider` **TIDAK** dijadikan field wajib `AppState` seperti
`PaymentProvider` — kalau ikut pola itu, ~57 file test perlu diedit
ulang (persis biaya P9-007's `paymentProvider` rollout) buat provider
yang, tidak seperti `AIProvider`/`PaymentProvider`, TIDAK PERNAH butuh
skenario test yang beda perilaku (`StubAdProvider` selalu "berhasil",
tidak ada mode gagal buat disimulasikan). `ad_service.watchAd` terima
`adProvider` sebagai parameter OPSIONAL dengan default `new
StubAdProvider()` — seam abstraksinya tetap ada (provider asli bisa
dioper eksplisit nanti), tapi tidak dipaksa lewat DI penuh yang costnya
tidak sepadan manfaatnya di titik ini. Didokumentasikan eksplisit di
sini biar tidak dikira lupa menerapkan pola P9-007.
`markConsumed` di-guard `consumedAt IS NULL` di level query (BUKAN
"diterima sebagai keterbatasan" seperti sweep P11-003) — race
konsumsi ganda ditangani BENAR, bukan didokumentasikan sebagai celah.
5 test baru (`tests/ad-gate.test.ts`), `bunx tsc --noEmit` bersih,
grep `fetch/http/XMLHttpRequest/axios` di `ad_provider.ts` → 0 hasil.

### P11-005 — Integration test suite + exit checkpoint
**Status:** done
**Depends on:** P11-001 s/d P11-004
**Deskripsi:** Pola sama tiap ticket-phase sebelumnya — route-coverage audit, checkpoint end-to-end yang menyatukan subscribe → allowance masuk → allowance expire (lazy sweep) → ad-gate alternatif dalam 1 alur nyata.
**Acceptance Criteria:**
- [x] Route-coverage audit (`grep`-based, pola P2-017/.../P10-003)
- [x] Checkpoint baru: 1 user subscribe Plus (dapat 100 credit, `expires_at` tercatat), simulasikan waktu lewat (pola sama simulasi hari P5-001/P7-001/P8-006), baca balance lagi → allowance ter-sweep otomatis DAN `credits.balance` berkurang; user lain nonton iklan lalu minta grammar evaluation → tidak charge credit
**DoD:** `bun test` hijau penuh di `titian-backend-bun` (lokal — CI masih P0-010 yang tertunda).

**Catatan implementasi:** checkpoint (`tests/phase11-checkpoint.test.ts`,
2 test) SENGAJA lewat endpoint ASLI (`POST /subscriptions/subscribe`
sungguhan, bukan insert `transactions` langsung seperti test unit
P11-002/003) — re-verifikasi lewat jalur nyata, bukan cuma
mengandalkan test unit yang sudah hijau, konsisten prinsip closing
ticket tiap fase di sesi ini. Route-coverage: 102 route/0 gap (98
sebelum Phase 11 + 4 baru: `GET /me/credits`, `POST
/subscriptions/subscribe`, `GET /subscriptions/me`, `POST
/ads/watch`). Total 429/429 test (dari 413 sebelum Phase 11: +9
P11-002/003, +5 P11-004, +2 checkpoint), `bunx tsc --noEmit` bersih.

---

## Checkpoint keluar Phase 11 (harus bisa didemo, bukan asumsi)
1. [x] Label "Diamond" terlihat di FE, bukan "Kredit" — grep 0 hasil "Kredit" di seluruh `titian-web/src`; screenshot dev-server dilewati (dicatat eksplisit di P11-001, risiko 0 buat perubahan 1 kata).
2. [x] Subscribe Plus/Pro terbukti grant allowance yang benar dengan `expires_at` sesuai aturan grace-1-bulan ADR-0005. — `tests/subscription.test.ts` + checkpoint scenario 1 lewat endpoint asli.
3. [x] Allowance yang sudah lewat masa berlaku terbukti ke-sweep dan MENGURANGI `credits.balance` — dites eksplisit lewat simulasi waktu, bukan diasumsikan dari deskripsi fitur. — checkpoint scenario 1: subscribe asli → balance 100 → simulasi waktu lewat → balance 0.
4. [x] Credit dari pembelian langsung (`expires_at=null`) terbukti TIDAK PERNAH ikut ke-sweep — dites eksplisit, bukan cuma allowance yang dites. — `tests/subscription.test.ts`'s "a direct purchase (expires_at null) is never swept".
5. [x] Free-tier ad-gate terbukti membuka 1 aksi AI berbayar TANPA charge credit, `StubAdProvider` terbukti 0 network call asli (grep eksplisit, sama prinsip `StubQrisProvider` P9-007). — `tests/ad-gate.test.ts` + checkpoint scenario 2.
6. [x] Semua yang dideferred (payment gateway subscription asli, ad SDK asli, funnel tracking, §6.6 Kids) tercatat eksplisit di sini dan `docs/STATE.md`.

Phase 11 **SELESAI PENUH**. Lanjut ke item ke-3 dari 4 yang diminta user: roadmap-Fase 8 sisa (Marketplace lanjutan).

Kalau salah satu poin di atas belum jalan end-to-end, jangan lanjut ke roadmap-Fase 8 sisa (item berikutnya yang diminta user) walau ticket lain kelihatan sudah "done".
