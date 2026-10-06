# Algoritma Generate Hemat Token v1 ("lean")

Status: **diimplementasikan di backend dan diukur pada satu bab nyata**. Belum dipakai untuk produksi massal. Menjalankan generate bab dengan bank lebih kecil dan jumlah panggilan jauh lebih sedikit, tanpa mengubah kualitas prompt soal.

## 1. Sumber pemborosan di pipeline lama

Diukur dari bab Matematika pertama (Vertex Gemini): 125.233 token untuk 49 soal plus checkpoint, atau ±2.550 token per soal, dalam 26 panggilan yang tiap panggilannya menulis hanya 2-5 soal. Penyebab, dari membaca kode (`content.rs::fill_bank`, `quiz_generation.rs`):

| Penyebab | Rincian |
|---|---|
| Panggilan terlalu kecil | Bank dipecah per (subtipe × bagian), maksimal 5 soal per panggilan, jadi ±18 kelompok dan sering 2-3 soal per panggilan |
| Overhead yang dikirim ulang tiap panggilan | prompt sistem ±1,5 ribu token (aturan mutu, skema) + rujukan materi + blok "soal yang sudah ada di topik" sampai 80 potongan soal (`SIBLING_QUESTION_LIMIT`) |
| Blok soal saudara membesar | token per panggilan naik dari ±8 ribu ke ±19 ribu selama satu run |
| Checkpoint per bagian | satu panggilan AI tambahan per bagian (4 soal), di luar bank |
| Pengulangan | putaran lanjutan memakai potongan 2 soal dan rujukan diperlebar, jadi makin boros |

## 2. Yang diubah

Semua di `titian-backend-rust`, tanpa mengubah jalur standar (default tetap sama).

1. **Satu panggilan per subtipe.** `blueprint::bank_blueprint_sized` dan `chunks_by_group`: slot tidak lagi terikat bagian, dan seluruh slot suatu subtipe (pilihan ganda, benar/salah, isian) dikirim dalam satu panggilan, ditulis dari seluruh materi. Ukuran bank dapat diatur (20 untuk tahap 1, 50 untuk penuh).
2. **Tanpa blok soal saudara.** Flag `lean` pada `QuizGenerationBlueprint`. Duplikat dalam satu grup tetap dibuang setelahnya.
3. **Tanpa panggilan checkpoint per bagian.** Pada struktur kanonik, checkpoint adalah fungsi item bank, bukan proses AI terpisah.
4. **Putaran lanjutan hanya meminta yang masih kurang** (`deficit`), maksimal 3 putaran.
5. **Latihan berkedalaman menyesuaikan bank.** Bank 20 tidak bisa melayani draw 25, jadi Latihan yang ada dijepit ke ukuran bank.
6. **Materi dipakai ulang** bila artikel sudah punya bagian (0 token).

Kode: `content.rs` (`fill_bank_lean`, `generate_bab_lean`, `reorder_bab_items`, `ensure_pooled_latihan_with`), `blueprint.rs`, `quiz_generation.rs`.

**Cara memakai**
- Worker: kirim `lean_bank_size` di opsi run `bab_content`, misalnya `{"lean_bank_size": 20}` (`RunOptions`). Tanpa opsi itu, pipeline lama berjalan seperti biasa.
- CLI satu bab: `cargo run --bin lean_bab_content -- <bab_id> [ukuran_bank=20]`. Mencetak token nyata per jenis tugas dari `ai_tasks`.

## 3. Hasil ukur (satu bab, Vertex Gemini 3.8 Flash)

Bab "Nilai dan Letak Elemen Tengah pada Barisan Berukuran Ganjil", bank 20 soal:

| | Panggilan | Token |
|---|---:|---:|
| Materi (1 panggilan) | 1 | 7.149 |
| Bank 20 soal | 4 | 18.431 |
| **Total** | 5 | **25.580** |

| Per soal bank | Pipeline lama | Lean |
|---|---:|---:|
| Token per soal | ±2.550 | ±920 |
| Panggilan per bank | 26 | 4 |

Penghematan bank ±2,8× per soal. Untuk satu unit tahap 1 (materi + 20 soal) 25,6 ribu token, dibanding ±138 ribu untuk materi + 49 soal + checkpoint + QA di bab lama (±5×, tetapi bank dan struktur tidak sebanding, jadi angka 2,8× lebih jujur).

**Kualitas hasil** (diperiksa langsung): 20 soal (10 pilihan ganda, 6 isian, 4 benar/salah) semuanya punya kunci dan pembahasan, 20 stem unik, kesulitan tepat 6 mudah / 10 sedang / 4 sulit, Bloom c1 1, c2 4, c3 7, c4 5, c5 3. Tanda draf terpasang. Sampel enam soal terbaca tepat secara matematis. Ini pemeriksaan mata pada satu bab, **bukan perbandingan buta dengan pipeline lama**.

## 4. Bug yang ditemukan dan diperbaiki saat menguji

Bab yang dibuat lewat kerangka lama sudah punya Latihan berdraw 10 dan 25. Versi pertama jalur lean membuat Latihan kedua berdraw 20 di sampingnya, sehingga bab punya dua "Latihan 2". Kini Latihan yang ada dijepit ke ukuran bank sebelum memastikan Latihan lain. Duplikat pada bab uji sudah saya hapus dan draw 25 dijepit menjadi 20.

## 5. Batas dan yang belum dikerjakan

1. **Satu bab, satu kali jalan.** Variasi antar bab belum diketahui. Rentang biaya yang wajar butuh benchmark ±20 modul.
2. **Masih 4 panggilan, bukan 3.** Satu panggilan ulang (3,5 ribu token) dipakai untuk slot yang kurang setelah duplikat dibuang. Meminta 1-2 soal ekstra per grup bisa menghapusnya.
3. **Overhead per subtipe masih ada.** Grup benar/salah (4 soal) tetap menelan ±4 ribu token, hampir semuanya prompt sistem dan rujukan. **Satu panggilan campuran** (ketiga subtipe sekaligus) bisa memangkas kira-kira 30-45% lagi, tetapi butuh jalur parsing dan penyimpanan baru, jadi belum dibuat.
4. **Prompt sistem tidak dipangkas.** Aturan mutu tetap sama, sehingga kualitas tidak dikorbankan.
5. **Tahap 2 (+30 soal) belum diukur.** Perkiraan bahwa biaya per soal turun lagi pada panggilan lebih besar belum terbukti.
6. **Checkpoint per bagian dan `guard_config`** tidak lagi dihasilkan pada bab lean. Pembaca pelajaran lama yang memakai checkpoint per bagian tidak akan menampilkannya, dan artikel tidak lagi dikunci "wajib selesai" sebelum Latihan. Ini pilihan struktur kanonik yang perlu Anda setujui sebelum jalur lean dipakai pada bab yang sudah punya pembaca.
7. **QA tetap yang lama.** Hasil lean belum melalui hakim materi+soal (`agent_qa`) maupun QA struktural bagian 16 PEMETAAN. Konsistensi kunci vs pembahasan masih butuh LLM/manusia.
8. **Cache prompt tidak dimanfaatkan.** Awal prompt berbeda per subtipe, jadi awalan bersama tidak terbentuk. Menyusun ulang agar materi berada di awalan yang sama bisa menurunkan biaya masukan bila penyedia menyediakan diskon cache; belum diperiksa.

## 6. Koreksi estimasi biaya

Perkiraan saya di `PEMETAAN_KANONIK_JALUR_UJIAN_V1.md` bagian 10.3 memakai ±64 ribu token per unit tahap 1 (materi + QA + bank 20 dengan biaya per soal lama). Ukuran nyata jalur lean: **25,6 ribu token (materi + bank 20, tanpa QA judge)**, sekitar 40% dari perkiraan itu. Dengan kalibrasi yang sama (Rp 1.000 per 207 ribu token, asumsi Anda), itu ±Rp 120 per unit. Angka ini dari satu bab, jadi hanya patokan.

## 7. Benchmark 20 bab (Vertex Gemini 3.8 Flash saja)

Dijalankan setelah bagian 1-6, dengan `lean_benchmark` (3 worker paralel). Data mentah: `pemetaan-jalur-ujian/benchmark_hasil_v1.jsonl`; daftar bab: `benchmark_bab_dipilih.json`.

**Sampel.** 10 bab Inggris (dari unit KOSONG: 4 GRV1, 4 GRV2, 2 WRT1; CEFR A2-B2) dan 10 bab Matematika (10 konsep berbeda, dari pecahan sampai turunan). Semua bab masih kerangka kosong. Dua bab Matematika memakai bentuk lama (satu item Latihan). Tahap 2 dijalankan pada 10 dari 20 bab.

**Bukti hanya Vertex.**
- Alat hanya membuat `VertexGeminiProvider` (tidak ada instance OpenRouter di proses itu) dan berhenti bila peran `lesson_generation`, `quiz_generation`, atau `agent_qa` bukan provider `vertex` bermodel `gemini*` atau punya model fallback.
- `ai_tasks` (dicatat dengan `provider_name()` yang baru, bagian 8): 20 baris `lesson_plan_generation` dan 113 baris `quiz_group_generation`, semuanya `vertex` / `gemini-3.8-flash`, 1 gagal sementara (diulang otomatis).
- Panggilan hakim tidak dicatat di `ai_tasks` oleh alat ini; tokennya diambil dari responsnya.

### 7.1 Biaya (token nyata)

| | Inggris (10) | Matematika (10) | Semua (20) |
|---|---:|---:|---:|
| Materi | 6.149 | 7.391 | **6.770** |
| Bank tahap 1 (20 soal) | 12.782 | 16.626 | **14.704** (median 13.052) |
| **Total tahap 1** | 18.931 | 24.017 | **21.474** (median 19.369; 18.172-32.853) |
| Panggilan bank tahap 1 | 3 | rata 4 (3-5) | rata 3 |
| Hakim `agent_qa` (8 soal sampel) | 5.453 | 6.517 | **5.985** |
| **Tahap 1 + hakim** | 24.384 | 30.534 | **27.459** |

| Tahap 2 (+30 soal, 10 bab) | |
|---|---:|
| Token bank | rata **23.603** (median 20.400; 15.444-40.678) |
| Panggilan | rata 5 (3-7) |
| Bank akhir | 50 soal pada 7 bab; 43, 48, 49 pada 3 bab lain |
| Duplikat dibuang | 46 soal |

**Satu unit penuh (50 soal):** materi 6,8 ribu + bank tahap 1 14,7 ribu + tahap 2 23,6 ribu = **±45 ribu token**, atau ±51 ribu dengan hakim. Pipeline lama pada bab Matematika pertama: ±138 ribu (materi + checkpoint + 49 soal + hakim). Penghematan ±2,7× per unit penuh dan ±3,3× per soal (±735 token per soal tahap 1, ±790 tahap 2, dibanding ±2.550).

Kalibrasi Rp 1.000 per 207 ribu token (asumsi Anda; harga Vertex sebenarnya belum saya masukkan): tahap 1 + hakim ±Rp 130 per unit, unit penuh ±Rp 245. Per 100 unit tahap 1 + hakim: ±2,75 juta token.

**Waktu:** tahap 1 rata-rata 132 detik (Inggris 99, Matematika 164; 66-325), tahap 2 rata-rata 120 detik. Tiga worker paralel tidak menemui 429.

### 7.2 Yang tidak sesuai harapan

1. **Tahap 2 tidak lebih murah per soal.** Saya menduga panggilan lebih besar akan menurunkan biaya per soal. Ternyata ±790 token per soal, sedikit lebih tinggi daripada tahap 1, karena duplikat.
2. **Duplikat.** Tahap 1 Matematika membuang 15 soal (Inggris 0), tahap 2 membuang 46. Daftar soal yang sudah ada di grup (yang saya tambahkan untuk tahap 2) belum cukup mencegahnya. Perkiraan token terbuang: ±61 soal × ±750 ≈ 46 ribu dari ±530 ribu token bank, sekitar 9%. Akibatnya tiga bank berhenti di 43-49 soal, dan dua bank tahap 1 Matematika berhenti di 18.
3. **Matematika lebih mahal dan lebih lambat daripada Inggris** (24,0 ribu vs 18,9 ribu token; 164 vs 99 detik), lebih banyak panggilan, dan ekor kanannya panjang (maksimum 32,9 ribu).
4. **Masih perlu 1-2 putaran tambahan** pada bab yang slotnya kurang; jumlah panggilan bank rata-rata 3, tetapi maksimum 5 (tahap 1) dan 7 (tahap 2).

### 7.3 Kualitas

**Hakim `agent_qa`** (sampel 8 soal + seluruh materi, per bab): rata-rata **4,86/5**, minimum 4,5, **20 dari 20 bab lolos ambang 4,2**, tidak ada galat parse. Rata-rata per dimensi: kegunaan belajar 5,00, kejelasan contoh 5,00, akurasi 4,95, kesesuaian jenjang 4,90, cakupan 4,85, **kualitas soal 4,45** (terendah). Total 32 isu: 1 Blocker, 2 Major.

- **Blocker: salah alarm.** Pada bab "Metode Faktorisasi Aljabar", hakim menandai soal nomor 7 sebagai salah secara aljabar, tetapi dalam teks isunya sendiri ia menghitung ulang ("Tunggu, periksa kembali...") dan menyimpulkan perhitungan itu benar. Di pipeline produksi (`run_bab_content`), Blocker mengirim bab ke perbaikan, jadi salah alarm seperti ini akan menghabiskan token untuk memperbaiki sesuatu yang tidak rusak.
- **Major, nyata (2 dari 20 bab):** soal menguji hal di luar materi bab. Inggris: soal preposisi pengiring ("with three assistants") padahal materi hanya mengajarkan mencari subjek secara umum. Matematika: soal memakai aturan kelipatan konstanta padahal materi menyatakan aturan itu baru dibahas di bab berikutnya. Jalur lean menulis soal dari seluruh materi tanpa membatasi ke bagian, dan model kadang memakai pengetahuannya sendiri. Ini biaya kualitas jalur lean yang perlu diawasi: 10% bab pada sampel ini.
- Isu minor yang berulang: label Bloom yang terlalu tinggi (mis. C3 untuk identifikasi benar/salah sederhana), dan dua soal dengan konsep identik pada satu bab.

**QA struktural** (`qa_bank_inggris.py` diterapkan pada 688 soal dari 20 bank): 2 soal KRITIS (0,29%: satu dengan jumlah pilihan tidak valid, satu kunci bukan label), 3 pasangan soal mirip ≥0,8, dan 688 temuan minor `BAGIAN-ASAL-HILANG` yang memang disengaja (jalur lean tidak memberi `source_section_id`). Komposisi: kesulitan mudah 216 / sedang 332 / sulit 140; Bloom C1 54, C2 155, C3 223, C4 185, C5 67, C6 4.

**Batas:** pemeriksaan kunci vs pembahasan tetap tidak dilakukan (lihat PEMETAAN bagian 16). Sampel hanya Matematika dan Inggris, bukan acak dari seluruh 1.413 unit. Angka untuk sains atau bahasa lain belum diketahui.

### 7.4 Efek samping pada database dev

20 bab uji kini berisi materi dan bank draf AI (10 bab dengan 50 soal, 10 dengan 20 soal), dan Latihan pooled sudah dijepit ke ukuran bank. Semua berstatus draf.

## 8. Perbaikan pencatatan penyedia

Kolom `ai_tasks.provider` untuk `quiz_group_generation` dan `lesson_plan_*` dulu diisi konstanta usang `"openrouter"` meskipun pemanggilnya Vertex. Kini dicatat dari instance yang benar-benar dipanggil lewat `AIProvider::provider_name()` (`vertex` untuk `VertexGeminiProvider`, `openrouter` untuk `DeepSeekProvider`). Layanan lain yang masih memakai konstanta sendiri (`alm_generation`, `live_chat`, dst.) belum diubah.


## 9. Gate Bagian (ditetapkan 2026-09-19)

Pipeline lean sempat membuang checkpoint per Bagian untuk menghemat token. Gate dikembalikan **tanpa biaya token**: soalnya dipilih dari bank 50 soal modul (uid sama) dan dicocokkan ke Bagian secara deterministik. Aturan lengkap, penerapan ke modul lama dan baru: `STANDAR_GATE_BAGIAN_V1.md`.

## 10. Komposisi bank mengikuti standar (ditetapkan 2026-09-19)

Blueprint bank tidak lagi berbobot per jenjang. Tabel tetap untuk bank 50 (`blueprint::standard_cells`): kesulitan 15 mudah / 25 sedang / 10 sulit; Bloom C1 5, C2 8, C3 14, C4 12, C5 6, C6 2 + 3 cadangan (topik konsep: C2, C4, C5; lainnya: C3, C3, C4). Tiap tipe soal menjangkau semua tingkat; benar/salah tidak memegang C5/C6. Ukuran lain memakai proporsi yang sama.

Bank yang dibuat dengan rencana lama diperbaiki dengan `rebalance_bank <bab_id>`: membuang soal yang tidak diinginkan rencana (paling banyak sebanyak sel yang kurang), mengisi sel yang kurang lewat Vertex, lalu memasang ulang gate Bagian yang soalnya terbuang. Soal yang sudah sesuai tidak disentuh. Hasil uji pada bab "Membulatkan": 12 dibuang dan 9 dibuang pada putaran kedua, total sekitar 23.000 token; akhirnya tepat 15/25/10 dan C1–C6 = 5/8/16/13/6/2.

Audit 609 bank berisi ≥40 soal (DB dev): kesulitan sudah rata-rata 16/24/10, tetapi Bloom atas kurang (C5 rata-rata 4,1; C6 0,2; C1 3,0); hanya 33 bank yang memenuhi C4/C5/C6. Memperbaiki semuanya berarti generasi ulang sekitar 10–20 soal per bank dan belum dijalankan.

## 11. Tag item: fungsi, bagian, dimensi, miskonsepsi (ditetapkan 2026-09-19)

Setiap slot bank membawa `fungsi` (nilai resmi dokumen; "transfer" = `latihan_mandiri`). Tabel sel tetap di `blueprint::standard_cells`: 4 diagnostik (C1-C2), 22 latihan_terarah, 8 latihan_mandiri (C3-C5 sulit), 10 checkpoint_akhir (C3-C5 sedang), 4 remedial (hanya pilihan ganda, C2-C3), 2 pengayaan (C6). Soal yang dipakai gate Bagian ditandai `checkpoint_bagian` dan tetap dihitung dalam 22 latihan.

Tag per soal (`taxonomy` + `source_section_id`), modul `content_factory/tagging.rs`:

| Tag | Asal |
|---|---|
| `fungsi` | turunan deterministik dari pencocokan sel Bloom x kesulitan; nol token |
| `source_section_id` (bagian_id) | kemiripan teks ke Bagian; minimal 4 latihan per Bagian (sampai 5 Bagian, proporsional di atasnya) |
| `knowledge_dimension` | dari prompt generasi untuk soal baru; satu panggilan pelabel per bank untuk yang belum punya |
| `miskonsepsi_target` | idem, wajib pada soal remedial |

`tagging::audit` menilai satu bank terhadap standar (ukuran 50, kesulitan 15/25/10, minimum Bloom, jumlah tiap fungsi, bagian_id, dimensi, miskonsepsi remedial) dan menyebut masalahnya. `content::finish_bank` (dipanggil `generate_bab_lean` setelah bank terisi) melabeli, menandai, memasang gate, dan mengaudit. Bank lama diperbaiki massal dengan `conform_banks <ids.csv> <out.jsonl> [--audit-only]`: rebalance hingga 6 putaran, lalu `finish_bank`; dapat diulang, lapor sebelum/sesudah dan biaya USD per bank.

Uji tiga bank lama (50 soal, 49 soal, 18 soal): dua pertama sesuai penuh dengan $0,044 dan $0,069 per bank; yang 18 soal butuh lebih dari 3 putaran.
