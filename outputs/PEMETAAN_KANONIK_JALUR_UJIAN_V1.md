# Pemetaan Ulang ke Modul Kanonik — Jalur Ujian v1

Cakupan: **Ujian TKA · Persiapan Masuk Perguruan Tinggi · Ujian Bahasa Inggris · Padanan Kurikulum Cambridge · Ujian BUMN & CPNS**.
Acuan baru: `STANDAR_KURIKULUM_TITIAN_ASA.md`, `STANDAR_BLUEPRINT_MODUL_TITIAN_ASA_V1.md`, `PETA_KANONIK_KURIKULUM_TITIAN_ASA_V1.md`, `ARSITEKTUR_TAKSONOMI_DAN_LEARNING_PATH_V1.md`, pohon Matematika dan Domain Lain, `MATEMATIKA_DARI_POHON_KE_BLUEPRINT_MODUL_V1.md`.
Acuan lama: struktur path di database dev (salinan prod), `agent/tools/content-gen/` (bab plan dan `curriculum_standards.standar`).

Status: **lapis 1 selesai (otomatis, bisa dicek ulang); keputusan lingkup dan bank bertahap sudah ditetapkan (bagian 10)**. Pemetaan tingkat leaf untuk mapel selain Matematika dan Inggris **belum** dikerjakan. Tidak ada perubahan pada database.

Berkas pendukung ada di `outputs/pemetaan-jalur-ujian/`. Semua angka di bawah berasal dari sana.

## 1. Temuan utama

| Temuan | Angka |
|---|---:|
| Simpul referensi di 5 kelompok jalur (6 path lama) | 7.666 |
| Topik unik yang dirujuk | 3.384 |
| Topik yang dirujuk lebih dari satu kali | 1.684 (50%) |
| Bab di dalam topik-topik itu | 13.119 |
| Bab yang sudah punya materi | 683 (5%) |
| Topik yang dipakai bersama oleh TKA dan PTN | 856 |

1. **Path lama adalah daftar mapel yang dirujuk ulang, bukan blueprint ujian.** Contoh: "Ujian Mandiri PTN" merujuk 925 topik, dan itu gabungan seksi lain. "TKA Pilihan Saintek" merujuk 412 topik, yaitu hampir seluruh Fisika, Kimia, dan Biologi.
2. **Bahasa Inggris tercampur.** Seksi CEFR A2, Cambridge KET, dan YLE Flyers merujuk **himpunan topik yang identik**. Hal yang sama berlaku untuk B1/PET, B2/FCE, C1/CAE, dan C2/CPE. Ini bukti langsung bahwa Cambridge di sini hanyalah nama lain dari tingkat CEFR, bukan materi tersendiri.
3. **Ada rujukan yang tidak punya padanan wajar** (bagian 3): 939 dari 6.336 rujukan non-dump (15%) ditandai `OFF-SCOPE`. Contoh: PAI dan Khonghucu di Cambridge Primary/Lower Secondary, Akuntansi di TKA Soshum, PAI dan Sejarah di "Core Values AKHLAK".
4. **Sebagian "mapel" sebenarnya path**: "Wawasan ASN & Kepegawaian" (123 topik) dan "Wawasan BUMN & Dunia Kerja" (79 topik). Menurut peta kanonik, keduanya bukan mapel inti dan harus dirumahkan ulang ke kewargaan, kesiapan karier, dan penalaran.
5. **Satuan kanonik lebih dekat ke "topik" lama daripada ke "bab", tetapi timpang per konsep.** Pohon Matematika punya 46 konsep dan 253 leaf; Matematika lama punya 238 topik dan 1.070 bab. Secara agregat hampir setara: satu leaf (modul kanonik) kira-kira sebanding dengan satu topik lama, dan bab lama menjadi **bahan rujukan** untuk isi modul itu (bukan Bagian, lihat bagian 13). Bank soal dibuat **per modul**. Namun angka agregat menyembunyikan dua arah yang berlawanan (bagian 9): konsep dasar seperti bilangan bulat hanya punya 1 topik lama untuk 8 leaf, sedangkan 14 konsep lanjut punya lebih banyak topik lama daripada leaf. Karena itu klaim "bank turun ±4 kali" **belum boleh dipegang** sebelum pemetaan leaf Matematika selesai.

## 2. Aturan yang dipakai (ringkasan dari standar baru)

- Path **tidak memiliki materi**. Path hanya memiliki node yang **merujuk** modul kanonik.
- Yang boleh dimiliki path hanya `strategy` (strategi dan format tes) dan `assessment` (blueprint ujian, simulasi berwaktu).
- Bahasa Inggris fondasi/CEFR **dipisah** dari Cambridge dan dari persiapan tes.
- TKA dipetakan per jenjang dan mata uji resmi; **AKM bukan sinonim TKA**.
- CPNS/BUMN adalah path yang merujuk `career_readiness`, kewargaan, penalaran, dan kompetensi formasi.
- Satu leaf punya satu `module_id`, satu blueprint aktif, satu bank 50 soal. Path atau kurikulum lain hanya mengubah urutan, jumlah soal, dan aturan lulus.
- Pola `curriculum_standards.standar` dari kerja lama (satu bab plan dipakai banyak kurikulum, termasuk kode syllabus Cambridge yang sudah diverifikasi di `add_cambridge_references.py`) **dipertahankan** sebagai mekanisme rujukan Cambridge.

## 3. Aturan "kecocokan seksi" (asumsi saya, mohon ditinjau)

Untuk tiap seksi path saya tetapkan mapel yang wajar ada di dalamnya (tabel `FIT` di `build_pemetaan.py`). Rujukan di luar itu ditandai `OFF-SCOPE`. Tanda ini berarti **perlu keputusan**, bukan otomatis salah dan tidak ada yang dihapus.

| Jalur | Rujukan | OFF-SCOPE | Catatan |
|---|---:|---:|---|
| Belajar Bahasa Inggris | 959 | 0 | semua Inggris, tetapi duplikasi tinggi (bagian 1 poin 2) |
| Fokus Ujian TKA | 1.195 | 150 | Akuntansi 63 di Soshum; IPAS 53 di AKM; IPS 19 di Soshum |
| Persiapan Masuk PT | 2.817 | 70 (+1.330 dump/enrichment) | Akuntansi 63 di Soshum; Mandiri PTN dan OSN dipisah |
| Kurikulum Cambridge | 2.137 | 654 | PAI, Khonghucu, Hindu, Katolik, Seni, PJOK, Prakarya, Bahasa Arab di Primary/Lower Secondary |
| Fokus Ujian BUMN | 294 | 59 | PAI 22 dan Sejarah 22 di "Core Values AKHLAK" |
| Fokus Ujian CPNS | 264 | 6 | — |

Perlu dicek pada sumber resmi: apakah Akuntansi memang dilarang di TKA Soshum, dan mapel Cambridge Primary/Lower Secondary mana yang punya syllabus. Saya belum memverifikasinya di sini.

## 4. Arsitektur baru per jalur

Notasi: `REF` = merujuk modul kanonik, `OWN` = aset milik path (strategi atau blueprint ujian), `GATE` = aturan tanpa konten.

### 4.1 Ujian TKA

```text
path: tka-[jenjang]           (satu path per jenjang; AKM path terpisah)
├─ GATE  placement per konsep
├─ REF   Literasi membaca  → indonesian (membaca, kebahasaan, menulis)
├─ REF   Numerasi          → mathematics (number, algebra, geometry, data) + modeling.quantitative_reasoning (rumah utama)
│                            + OPSIONAL reasoning.quantitative_literacy, hanya leaf membaca angka/tabel/grafik/risiko (Keputusan D1)
├─ REF   Bahasa Inggris    → english.receptive_reading + grammar_vocabulary pada target CEFR jenjang itu
├─ REF   Pilihan Saintek   → science.physics / chemistry / biology, computing
├─ REF   Pilihan Soshum    → social_sciences.history / geography / economics / sociology
├─ OWN   blueprint komponen (jumlah item, waktu), strategi waktu, template EVALUATE/INTERPRET
└─ OWN   simulasi berwaktu
path: akm-[jenjang]           (Literasi dan Numerasi; tanpa mapel pilihan)
```

Yang perlu diverifikasi sebelum dibekukan: struktur resmi TKA per jenjang (mata uji wajib dan pilihan, jumlah item, waktu). Dokumen lama tidak memuatnya dan saya belum memeriksa sumber resmi.

### 4.2 Persiapan masuk perguruan tinggi

```text
path: utbk-snbt
├─ REF  Tes Potensi Skolastik  → reasoning (logic, problem_solving), indonesian, mathematics.quantitative
├─ REF  Literasi B. Indonesia  → indonesian
├─ REF  Literasi B. Inggris    → english (receptive_reading, grammar_vocabulary)
├─ REF  Penalaran Matematika   → mathematics + reasoning.quantitative_literacy
└─ OWN  blueprint subtes, strategi, simulasi adaptif berwaktu
path: pts-saintek / pts-soshum  → REF unit F2–F3 tiap mapel (hanya rujukan, tanpa daftar topik sendiri)
path: ujian-mandiri-ptn         → OWN aturan/format per PTN; REF ke path di atas (bukan 925 topik)
path: um-ptkin                  → REF religious_studies.islamic_madrasah + islamic_advanced + other_languages.arabic
path: osn-[mapel]               → REF unit F3–F4 (enrichment)
```

### 4.3 Ujian Bahasa Inggris

```text
fondasi CEFR: english (satu himpunan unit, ditag cefr:A1…C2)         ← satu-satunya rumah materi
Cambridge English (YLE, KET, PET, FCE, CAE, CPE): label + REF ke unit CEFR yang sama
                                  + OWN format ujian per level
IELTS / TOEFL iBT / TOEFL ITP / PTE / TOEIC / Duolingo: OWN strategi & format tes
                                  + REF ke unit skill (reading, listening, writing, speaking)
Linguistik S1–S3, TEFL/TESOL, penerjemahan, sastra: di luar pohon v1 → parkir (P2)
```

### 4.4 Padanan kurikulum Cambridge

```text
Cambridge bukan pohon materi. Ia adalah pemetaan (label + curriculum_standards.standar):
├─ Primary (Stage 1–6)      → peta fase A–C, hanya mapel yang punya syllabus Cambridge
├─ Lower Secondary (7–9)    → peta fase D, hanya mapel yang punya syllabus
├─ IGCSE                    → tag syllabus (0580, 0606, 0625, …) pada unit kanonik
├─ AS & A Level             → tag syllabus (9709, 9231, 9702, …) pada unit kanonik
└─ OWN  peta syllabus dan format paper; unit baru hanya bila ada gap nyata
```

### 4.5 Ujian BUMN dan CPNS

```text
path: bumn
├─ REF  TKD               → reasoning, indonesian, mathematics.quantitative
├─ OWN  Core Values AKHLAK  (kerangka nilai BUMN; bukan PAI atau Sejarah)
├─ REF  Learning Agility  → reasoning.problem_solving + career_readiness
├─ REF  Bahasa Inggris    → english
└─ OWN  format seleksi, etika proses, pembaruan sesuai pengumuman
path: cpns
├─ REF  TWK → social_sciences.civic_education (+ sejarah bila relevan)
├─ REF  TIU → reasoning, indonesian, mathematics.quantitative
├─ REF  TKP → career_readiness + reasoning
├─ OWN  strategi SKD
└─ OWN  SKB dipisah per rumpun/jabatan, dibuat hanya setelah formasi dipilih
```

## 5. Hasil pemetaan lapis 1

Skrip `build_pemetaan.py` memberi tiap topik lama: rumah kanonik, konsep kanonik (bila ada), template blueprint, jenis pemetaan, dan jumlah rujukan `OFF-SCOPE`.

| Jenis pemetaan | Topik | Arti |
|---|---:|---|
| CANONICAL | 448 | konsep kanonik sudah ditetapkan: Matematika 238 (semua), Inggris 210 |
| PATH-OWNED | 72 | aset strategi/format tes (IELTS, TOEFL, PTE, TOEIC, dst.) |
| EXTENSION | 136 | ESP dan linguistik/TEFL/terjemahan: di luar pohon v1 |
| REHOME | 425 | IPA, IPAS, IPS, Wawasan ASN, Wawasan BUMN: harus dirumahkan ulang per bab |
| HOME-ONLY | 2.310 | mapel sudah punya rumah kanonik, konsep/leaf belum dipetakan |

Cara kerja dan batasnya:

- Matematika: 39 kluster lama dipetakan ke 40 dari 46 konsep kanonik (6 konsep lanjut tidak punya topik lama), lalu 19 topik dikoreksi lewat kata kunci judul karena satu kluster kadang mencakup dua konsep. Cek sampel awal menemukan 1 salah dari 6; setelah aturan judul ditambahkan, kasus itu benar. **Akurasi belum diuji menyeluruh.** Ini pemetaan tingkat konsep, belum leaf.
- Inggris: 56 kluster lama dipetakan ke strand kanonik, aset milik path, atau ekstensi.
- Template blueprint diberikan per kluster/strand, bukan per leaf, dan merupakan tebakan awal: `MATH-*` untuk Matematika (dari dokumen Matematika), template generik `CONCEPT/INTERPRET/COMMUNICATE/PRACTICE/EVALUATE` untuk Inggris (dari standar blueprint bagian 4). Topik Inggris kanonik juga diberi label `cefr` dari seksi CEFR tempat ia dirujuk (203 dari 210 punya label).
- Mapel lain: baru sampai rumah kanonik. Pohonnya di `outputs/` masih setingkat konsep, jadi butuh pemecahan leaf oleh ahli mapel lebih dulu.

## 6. Ukuran pekerjaan (estimasi, bukan pengukuran)

Asumsi: Rp 100 juta untuk 100 ribu topik dengan workflow lama ≈ Rp 1.000/topik, dan workflow hemat ≈ 15% dari itu (belum dibenchmark).

| Skenario | Modul | Biaya perkiraan |
|---|---:|---:|
| P0 kanonik (Matematika 238 + Inggris 210), workflow lama, **hanya bank per modul** | 448 | ≈ Rp 450 ribu |
| P0 kanonik, workflow hemat | 448 | ≈ Rp 70 ribu |
| Semua 3.384 topik, workflow lama | 3.384 | ≈ Rp 3,4 juta (di atas anggaran Rp 2,5 juta) |
| Semua topik yang layak dipakai, workflow hemat | ≤ 3.384 | ≈ Rp 0,5 juta |

Angka di atas **belum** memuat bank dan blueprint ujian milik path (TKA, UTBK, CPNS, BUMN, IELTS, dll.). Standar mewajibkan bank itu terpisah dari bank unit (`STANDAR_KURIKULUM` bagian 9), jadi biayanya tambahan. Kalau angka Rp 1.000/topik meleset, semua angka ikut bergeser. Benchmark kecil (±20 modul) diperlukan sebelum ini dipakai untuk keputusan.

## 7. Keputusan yang dibutuhkan

1. **Daftar mapel per seksi** (bagian 3), terutama Cambridge Primary/Lower Secondary dan Akuntansi di TKA Soshum. Yang `OFF-SCOPE` mau dilepas dari path, dijadikan opsional, atau dipertahankan?
2. **Ujian Mandiri PTN dan OSN**: setuju diubah menjadi aturan/aset dan enrichment (bukan daftar topik)?
3. **Wawasan ASN/BUMN (202 topik)**: setuju dirumahkan ke kewargaan/karier/penalaran, dengan "Core Values AKHLAK" dan SKB sebagai aset milik path?
4. **Linguistik dan TEFL/terjemahan (136 topik)**: diparkir sebagai P2?
5. **Struktur resmi TKA, UTBK, dan format Cambridge**: siapa yang memverifikasi sumber resminya sebelum blueprint dibekukan?

## 8. Langkah berikut yang saya usulkan

1. Anda tinjau bagian 3 dan keputusan di bagian 7.
2. Pemetaan tingkat leaf untuk **Matematika** (238 topik → 253 leaf, dengan bab lama sebagai bahan rujukan modul). Ini pilot yang paling siap datanya dan cocok dengan jalur TKA/UTBK.
3. Pemetaan Inggris ke strand + CEFR, dan penyatuan duplikasi CEFR/Cambridge.
4. Benchmark ±20 modul dengan workflow hemat untuk memastikan angka bagian 6.
5. Gerbang sebelum produksi massal (`PETA_KANONIK` bagian 7, `STANDAR_KURIKULUM` bagian 12–13): unit emas Bilangan Bulat terpakai oleh tiga path (fondasi SMP, TKA, remedial adaptif) tanpa salinan.
6. Baru setelah itu menyentuh database (registry `module_id`, path node sebagai referensi).

## 9. Pemeriksaan terhadap lima standar dan koreksinya

Bagian ini menandai di mana pemetaan lapis 1 sejalan atau bertentangan dengan dokumen di `outputs/`.

**Sejalan**
- Path hanya merujuk; hanya `strategy` dan `assessment` yang milik path (`ARSITEKTUR` bagian 5 dan 8).
- "Bab" bukan objek kanonik (`STANDAR_KURIKULUM` bagian 2), sehingga bab lama diperlakukan sebagai Bagian atau bukti cakupan.
- CEFR dipisah dari Cambridge dan tes; AKM bukan sinonim TKA (`STANDAR_KURIKULUM` bagian 11 poin 5 dan 6).
- Wawasan ASN/BUMN diperlakukan sebagai path, bukan mapel (`PETA_KANONIK` bagian 3).

**Bertentangan atau perlu dikoreksi**
1. **Arah pemetaan.** `ARSITEKTUR` bagian 7 langkah 1 berkata "jangan mulai dari kelas, ujian, atau daftar topik lama". Pemetaan ini berangkat dari topik lama karena Anda meminta modul lama sebagai referensi. Konsekuensinya: **registry harus dibangun dari pohon (leaf → `module_id`), dan topik lama hanya bukti cakupan dan bahan yang bisa dipakai ulang.** Berkas `pemetaan_*.csv` bukan registry.
2. **Granularitas tidak seragam.** Lihat bagian 1 poin 5. Konsep dengan topik lama jauh lebih sedikit dari leaf: `number.integers` (1 vs 8), `number.whole_place_value` (1 vs 5), `number.factors_multiples` (1 vs 5), `number.fractions` (3 vs 7), `modeling.optimization_operations` (1 vs 5). Konsep dengan topik lama melebihi leaf (kandidat duplikat): `algebra.matrices_vectors` (12 vs 7), `geometry.plane_shapes` dan `solid_shapes` (10 vs 7 masing-masing), `geometry.measurement` (8 vs 4), `algebra.linear_equations` (9 vs 7), `statistics.inference` (9 vs 5), dan 8 konsep lain.
3. **Celah cakupan.** Enam konsep Matematika tidak punya topik lama: `geometry.differential`, `analysis.advanced`, `number_theory.algebraic`, `discrete.foundations`, `modeling.finance_games`, `modeling.stochastic_processes` (semuanya lanjut, jauh dari jalur ujian sekolah). Bahasa Inggris kanonik tipis di tingkat atas: A1 29, A2 43, B1 70, B2 44, **C1 14, C2 3** topik. Ini penting untuk Cambridge CAE/CPE dan IELTS skor tinggi.
4. **Bank ujian di luar bank unit.** Biaya di bagian 6 hanya menghitung bank 50 soal per modul. Standar mewajibkan tes format tertentu (IELTS, TKA, UTBK, CPNS, BUMN) punya bank dan blueprint sendiri.
5. **Prioritas.** `PETA_KANONIK` bagian 6 menaruh CPNS, BUMN, dan sertifikasi bahasa lengkap di **P2** karena bergantung pada format eksternal yang terus berubah, sedangkan path TKA/UTBK yang hanya merujuk inti ada di **P0**. Fokus Anda mencakup semuanya, jadi urutan kerjanya sebaiknya: TKA/UTBK dan fondasi Inggris dulu, BUMN/CPNS/sertifikasi belakangan.
6. **Kode belum seragam antar dokumen.** Pohon Matematika memakai kode konsep `algebra.patterns_expressions`, sedangkan `MATEMATIKA_DARI_POHON_KE_BLUEPRINT_MODUL` menyebut strand `algebra_functions` dengan konsep `patterns_expressions`. Domain Inggris juga `english` di `PETA_KANONIK` tetapi `english → bahasa_inggris` di `ARSITEKTUR`. CSV memakai kode dari berkas pohon. **Satu konvensi kode perlu diputuskan sebelum registry dibuat.**
7. **Template blueprint ganda.** Standar blueprint menetapkan tujuh kode generik; dokumen Matematika menambah enam varian `MATH-*`. Perlu diputuskan apakah `MATH-*` adalah sub-template resmi.
8. **Bank 50 soal.** Standar mewajibkan tepat 50 per modul sebagai Definition of Done. Usul bank bertahap (±20 soal saat rilis) yang saya ajukan sebelumnya **menyimpang** dari itu dan butuh persetujuan Anda.
9. **Web interaktif.** `STANDAR_KURIKULUM` bagian 8 dan Lampiran A menjadikan widget reusable sebagai jalur utama, dengan CodeWeb per modul hanya untuk kasus khusus. Alur generate HTML penuh per bab yang dipakai sebelumnya bertentangan dengan itu. Ini di luar pemetaan jalur, tetapi memengaruhi biaya produksi.

## 10. Keputusan dan lingkup P0

Keputusan Anda:

1. **Bank soal bertahap.** Modul dirilis dengan **20 soal** lebih dulu, lalu dilengkapi ke 50. Ini menyimpang dari Definition of Done "tepat 50" di `STANDAR_BLUEPRINT`, jadi standar itu perlu diubah menjadi dua tahap (bagian 10.1).
2. **Fokus kanonik hanya untuk yang dipakai di**: TKA, ujian masuk perguruan tinggi, tes Bahasa Inggris, dan konversi ke kurikulum Cambridge.
3. **BUMN dan CPNS ditunda.** Topiknya tidak disentuh, dan tidak masuk hitungan lingkup.

### 10.1 Bank tahap 1 (20 soal) dan tahap 2 (+30)

Komposisi tahap 1 diskalakan dari komposisi 50 di `STANDAR_BLUEPRINT` bagian 5 (×0,4, dibulatkan). Tiap Bagian tetap mendapat minimal 2 soal latihan.

| Fungsi bank | 50 (target akhir) | Tahap 1 | Tahap 2 |
|---|---:|---:|---:|
| Diagnostik prasyarat | 4 | 2 | +2 |
| Latihan per Bagian | 22 | 8 | +14 |
| Latihan mandiri/transfer | 8 | 3 | +5 |
| Checkpoint akhir | 10 | 6 | +4 |
| Remedial | 4 | 1 | +3 |
| Pengayaan | 2 | 0 | +2 |
| **Total** | **50** | **20** | **+30** |

| Sumbu | Tahap 1 |
|---|---|
| Kesulitan | 6 mudah, 10 menengah, 4 sulit (skala 15/25/10) |
| Bloom | C1 2, C2 3, C3 6, C4 5, C5 2, cadangan 2. **C6 ditunda ke tahap 2.** |

Catatan:
- Checkpoint tahap 1 = 6 soal, cukup untuk menampilkan 4 secara adaptif. Pool 10 baru lengkap di tahap 2.
- Kontrak item (`item_id`, `fungsi`, `bloom`, `miskonsepsi_target`, dst.) tetap sama; tahap 2 hanya menambah item ke bank yang sama, tidak membuat bank baru.
- Sesi latihan 10 dan 20 soal langsung bisa dipakai di tahap 1. Sesi 25 dan 50 baru penuh setelah tahap 2.
- **Pemicu tahap 2 belum ditetapkan.** Usulan: modul yang menjadi node `required` pada path aktif *dan* pool 20 sudah sering berulang bagi peserta. Ambang angkanya perlu data penggunaan; belum ada.

### 10.2 Lingkup P0

Aturan: sebuah topik lama masuk P0 bila dirujuk oleh seksi yang cocok (bukan `OFF-SCOPE`, bukan dump) di TKA, ujian masuk PT, atau Bahasa Inggris. **Cambridge tidak menggerakkan produksi**: konversi Cambridge hanya menempelkan label syllabus (`curriculum_standards.standar`) pada unit yang sudah ada, jadi topik yang hanya dirujuk Cambridge tidak diproduksi sekarang. Linguistik/ESP (136 topik) tetap diparkir. UM-PTKIN dipisah sebagai P1 karena standar mensyaratkan penelaah ahli keagamaan.

| Tier | Topik lama | Arti |
|---|---:|---|
| **P0a** | 852 | dipakai oleh ≥2 dari {TKA, ujian masuk PT, Inggris}: dikerjakan paling dulu |
| **P0b** | 561 | dipakai oleh satu di antaranya |
| P1-PTKIN | 326 | UM-PTKIN, butuh ahli keagamaan |
| MERGE | 25 | duplikat Matematika (bagian 11); tidak diproduksi |
| KONVERSI-SAJA | 546 | hanya dirujuk Cambridge: cukup diberi label bila unit kanoniknya kelak ada |
| Ditunda / diparkir | sisanya | BUMN, CPNS, linguistik/ESP, dump Mandiri PTN dan OSN |

**P0 = 1.413 topik lama** (dari 3.384). Angka ini batas atas jumlah modul: ada konsep Matematika yang topik lamanya melebihi leaf pohon (bagian 9 poin 2), sehingga hasil deduplikasi bisa lebih kecil.

| Mapel | P0 | P0a | P0b |
|---|---:|---:|---:|
| English | 275 | 73 | 202 |
| Matematika | 168 | 29 | 139 |
| Fisika | 140 | 140 | 0 |
| Kimia | 135 | 135 | 0 |
| Biologi | 122 | 122 | 0 |
| Bahasa Indonesia | 117 | 14 | 103 |
| Sejarah | 114 | 81 | 33 |
| Geografi | 90 | 90 | 0 |
| Ekonomi | 88 | 84 | 4 |
| Sosiologi | 84 | 84 | 0 |
| Penalaran & Logika | 32 | 0 | 32 |
| Filsafat | 25 | 0 | 25 |
| Sastra Indonesia | 23 | 0 | 23 |

Dari 1.413 topik itu, 387 sudah punya konsep kanonik (Matematika, Inggris, dan 16 topik penalaran), 77 adalah aset strategi tes, 11 dirumahkan ke Bahasa Indonesia, dan **938 baru punya rumah mapel** dan masih harus dipetakan ke konsep/leaf. 864 topik P0 juga membawa rujukan Cambridge, jadi konversinya nyaris gratis begitu unitnya ada.

Temuan yang perlu diperhatikan:
- 70 topik Matematika dan 120 topik IPA/84 IPAS/95 Informatika hanya muncul di Cambridge, sehingga tidak diproduksi sekarang. Artinya Cambridge A Level Further Math dan Primary/Lower Secondary Science belum tertutup.
- Topik lama Penalaran & Logika ternyata campuran dan sudah dirumahkan ulang (bagian 11, Keputusan D1).
- Pemisahan Bahasa Inggris: dari 282, hanya 73 dipakai lebih dari satu fokus. Sisanya khusus tes Inggris.

### 10.3 Perkiraan biaya P0 (asumsi, bukan pengukuran)

Dasar: bab Matematika yang saya generate hari ini memakai ±125 ribu token untuk 49 soal plus checkpoint, atau ±2,5 ribu token per soal, ditambah ±13 ribu untuk materi dan QA. Dengan Rp 1.000 per topik untuk workflow penuh ±207 ribu token (asumsi dari Anda, dengan Gemini 3.8 Flash):

| | Token per modul | Kira-kira |
|---|---:|---:|
| Workflow lama, bank 50, plus web interaktif | ±207 ribu | Rp 1.000 |
| Tahap 1: materi + QA + bank 20, tanpa web per modul | ±64 ribu | ±Rp 310 |

1.413 modul × ±Rp 310 ≈ **Rp 440 ribu** untuk seluruh P0 tahap 1, di bawah anggaran Rp 2,5 juta. Melengkapi ke 50 soal menambah sekitar 30 × 2,5 ribu = 75 ribu token per modul, jadi harus dipicu oleh penggunaan (bagian 10.1), bukan dijalankan massal.

Belum termasuk: bank dan blueprint ujian milik path, tinjauan manusia, dan ketidakpastian Rp 1.000/topik. Perkiraan token per soal juga berasal dari satu bab, jadi rentang sebenarnya lebih lebar. Benchmark ±20 modul tetap diperlukan.

### 10.4 Berkas

- `pemetaan-jalur-ujian/lingkup_p0_v1.csv`: satu baris per topik lama dalam lingkup, dengan tier, penanda fokus (TKA, PTN, ENG, PTKIN, CAMB), konsep kanonik, template, dan CEFR.

## 11. Keputusan D1: literasi kuantitatif dan Penalaran & Logika

Pertanyaan: apakah TKA Numerasi boleh merujuk `reasoning.quantitative_literacy`? **Keputusan: boleh, tetapi hanya sebagai referensi opsional ke satu leaf, dan rumah utama penalaran kuantitatif tetap Matematika.**

Dasar keputusan (dari pohon di `outputs/`):
- Pohon punya dua rumah untuk skill yang hampir sama. `modeling.quantitative_reasoning` (Matematika) memuat "mengestimasi dan memeriksa kewajaran hasil" dan "menjelaskan keputusan berbasis data atau perhitungan". `reasoning.quantitative_literacy` memuat "mengestimasi serta menilai kewajaran pernyataan kuantitatif" dan "membuat keputusan berbasis data". Kalau keduanya dijadikan unit, terjadi dua unit dan dua bank untuk skill yang sama, yang dilarang aturan satu konsep satu rumah (`ARSITEKTUR` bagian 4).
- TKA Numerasi di data lama sudah 100% berisi topik Matematika (72 topik); UTBK Pengetahuan Kuantitatif dan Penalaran Matematika juga Matematika.

Aturannya:
1. **Rumah utama: Matematika `modeling.quantitative_reasoning`** untuk estimasi, kewajaran hasil, soal cerita menjadi model, dan keputusan berbasis hitungan.
2. Di `reasoning.quantitative_literacy`, dua leaf yang tumpang tindih tidak dijadikan unit sendiri. Keduanya menjadi relasi `same_skill_as` ke leaf Matematika. Yang tetap menjadi unit di reasoning hanya leaf **membaca angka, tabel, grafik, dan risiko dalam konteks**.
3. TKA Numerasi dan UTBK merujuk Matematika (wajib) dan leaf reasoning itu (**opsional**). Statusnya naik menjadi wajib hanya bila blueprint resmi TKA yang diverifikasi memuatnya.
4. **Perubahan pada pohon yang diperlukan** (belum saya lakukan, karena pohon adalah dokumen otoritatif): dua bullet di `reasoning.quantitative_literacy` diberi catatan relasi `same_skill_as → modeling.quantitative_reasoning`.

Topik lama Penalaran & Logika (57 topik yang dipakai path lama) tidak satu jenis. Kluster-nya dirumahkan ulang:

| Kluster lama | Topik | Rumah baru | Jenis |
|---|---:|---|---|
| Aritmetika Dasar & Cepat, Deret & Pola Bilangan, Pengetahuan Kuantitatif, Soal Cerita & Pemodelan | 20 | Matematika | **MERGE** (duplikat; tidak diproduksi) |
| Logika Matematika Terapan | 5 | Matematika `discrete.logic_sets_proof` | **MERGE** |
| Logika Verbal, Pemecahan Masalah, Penalaran Analitis | 16 | `reasoning` (logic_argumentation, problem_solving) | kanonik |
| Kemampuan Verbal Dasar, Pemahaman Bacaan | 11 | Bahasa Indonesia | dirumahkan |
| Strategi Menghadapi Tes | 5 | aset strategi milik path | path-owned |

Ujian bahwa 25 topik MERGE memang duplikat: setelah dicocokkan ke leaf Matematika, mereka hanya menambah 2 leaf yang belum tercakup (dari 150 menjadi 152). Selebihnya jatuh ke leaf yang sudah tercakup oleh topik Matematika. Dampaknya: 25 topik keluar dari produksi (P0 1.445 menjadi 1.420, lalu 1.413 setelah 7 topik fonetik linguistik dipindah ke ekstensi, bagian 14).

## 12. Pemetaan leaf Matematika: hasil pertama

`match_leaf_matematika.py` mencocokkan 876 bab lama (168 topik P0 Matematika + 25 topik MERGE) ke 253 leaf pohon. Tanpa LLM: TF-IDF sederhana, dibatasi ke konsep topik, dan satu bab boleh mencakup sampai tiga leaf. **Hasilnya usulan yang harus ditinjau, bukan keputusan.**

| Status | Bab | Arti |
|---|---:|---|
| AUTO-KUAT | 494 | skor ≥ 0,45 dan di konsep yang sama |
| PERLU-TINJAU | 252 | skor 0,25-0,45, atau menyeberang konsep |
| LEMAH | 52 | skor rendah |
| TANPA-LEAF | 52 | tidak ada leaf yang cocok |
| BAGIAN-PENDUKUNG | 26 | "kesalahan umum", "rangkuman", "latihan", "strategi": jadi Bagian, bukan leaf |

Ketepatan yang saya periksa manual pada sampel acak: `AUTO-KUAT` benar ±85% (22 dari 26), `PERLU-TINJAU` ±60% (7 dari 12). Sampelnya kecil. Kesalahan yang saya temukan masih ada, contohnya bab "Penjumlahan & Pengurangan dengan Bantuan Garis Bilangan" masuk leaf garis bilangan padahal isinya operasi. Jadi angka cakupan di bawah adalah perkiraan.

Cakupan leaf: **152 dari 253 leaf tercakup** oleh minimal satu bab. Dari 101 yang belum:
- 79 adalah leaf lanjut/kuliah (analisis, aljabar abstrak, stokastik, dll.). Ini wajar tidak tercakup; klasifikasi "lanjut" adalah asumsi saya.
- **22 leaf tingkat sekolah/ujian belum tercakup**, dan ini yang penting untuk TKA dan UTBK:
  - `number.integers`: nilai mutlak, penjumlahan bilangan bulat bertanda sama, penjumlahan berbeda tanda, perkalian dan pembagian bertanda
  - `number.whole_place_value` dan `whole_operations`: pembulatan, pembagian dengan sisa
  - `number.fractions`: perkalian dan pembagian pecahan
  - `number.real_exponents_roots`: bilangan rasional dan irasional, estimasi bilangan real
  - `algebra`: pemodelan dengan variabel, perkalian dan pembagian bentuk aljabar, representasi fungsi
  - `geometry`: ketelitian dan satuan, pengukuran majemuk, simetri dan transformasi, parabola, elips, hiperbola
  - `data`: menilai representasi data yang menyesatkan
  - `calculus`: menafsirkan limit; `discrete`: himpunan, relasi, fungsi diskrit dan logika orde pertama

Untuk bilangan bulat, ini terbukti nyata: topik lama "Bilangan Bulat & Garis Bilangan" (7 bab) hanya mengajarkan garis bilangan, perbandingan, dan lawan bilangan. Operasi penjumlahan, nilai mutlak, dan perkalian tidak ada. Unit emas `Menjumlahkan Bilangan Bulat Berbeda Tanda` di `outputs/golden-module-bilangan-bulat/` sudah menutup satu dari leaf itu.

Dua kesimpulan:
1. **Jangan asumsikan materi lama menutup pohon.** Untuk prasyarat dasar, produksi baru diperlukan, tepatnya pada 22 leaf di atas. Ini pekerjaan tambahan di luar hitungan 1.420 modul.
2. Topik lama yang rujukannya melebihi leaf (bagian 9 poin 2) perlu ditinjau sebagai duplikat, terutama geometri bangun datar dan ruang.

Berkas: `pemetaan_leaf_matematika_v1.csv` (bab → leaf, skor, status), `status_leaf_matematika_v1.csv` (status per leaf), `ringkasan_leaf_matematika.json`, `build_lingkup.py`, `match_leaf_matematika.py`, serta `bab_math_semua.csv` dan `topik_math_semua.csv` (seluruh perpustakaan Matematika: 335 topik, 97 di antaranya tidak dirujuk path mana pun dan semuanya lanjut/kuliah).

## 13. Koreksi setelah membaca ulang dokumen blueprint Matematika

Membaca ulang `POHON_HIERARKI_MATEMATIKA_V1.md` dan `MATEMATIKA_DARI_POHON_KE_BLUEPRINT_MODUL_V1.md` bersama standar lain menunjukkan tiga hal yang salah atau kurang di dokumen ini:

1. **"Bab lama menjadi Bagian" salah.** Di dokumen blueprint, Bagian adalah tahap pedagogis yang ditentukan template, misalnya `MATH-PROCEDURE`: diagnosis prasyarat → strategi/langkah → variasi prosedur → aplikasi → checkpoint. Bagian tidak sama dengan bab lama. Yang benar: satu leaf adalah satu modul, dan beberapa bab lama (median 4, maksimum 18 per leaf yang tercakup) menjadi **sub-keterampilan yang dirujuk** saat menyusun Bagian strategi dan variasi. Contoh: bab "Metode Faktorisasi", "Melengkapkan Kuadrat", dan "Rumus ABC" adalah bahan untuk satu modul `Menentukan akar persamaan kuadrat`.
2. **Bab Matematika lama hampir tidak membawa isi.** Dari 1.070 bab Matematika di lingkup lama, hanya 17 yang bermateri. Jadi topik lama untuk Matematika terutama berguna sebagai **kerangka sub-keterampilan (spesifikasi pelajaran)**, bukan konten yang dipakai ulang. Semua modul tetap harus diproduksi. Ini menguntungkan biaya: bab lama memberi outline sehingga tahap penulisan tidak perlu merancang ulang dari nol, tetapi tidak menghemat penulisan materinya.
3. **Unit produksi Matematika adalah leaf, bukan topik lama.** Dengan asumsi klasifikasi saya, pohon punya 167 leaf tingkat sekolah/ujian dan 86 leaf lanjut/kuliah. Yang relevan untuk TKA dan UTBK adalah 167 leaf itu: 145 sudah punya bab lama sebagai kerangka, 22 belum punya sama sekali (bagian 12). Angka 168 topik P0 Matematika di bagian 10 sebaiknya dibaca sebagai sumber, bukan jumlah modul.

Satu implikasi untuk bank bertahap (bagian 10.1). Tabel kedalaman di pohon menetapkan tarikan bank: F0-F1 memakai sesi 10/20 soal, F2 memakai 25 soal, F3-F4 memakai 50 soal atau blueprint evaluasi khusus. Dengan bank tahap 1 berisi 20 soal:
- Sesi 10 dan 20 soal langsung tersedia (cukup untuk F0-F1).
- Sesi 25 soal (F2) tidak tersedia; ia dibatasi 20 sampai tahap 2.
- Sesi 50 soal dan blueprint evaluasi F3-F4 tidak tersedia sebelum tahap 2.

TKA dan UTBK banyak menguji penalaran (F2-F3). Karena itu leaf yang menjadi node `required` pada path ujian dan berkedalaman F2 ke atas sebaiknya naik ke tahap 2 lebih dulu, sedangkan leaf prasyarat dasar (F0-F1) cukup bertahan di 20 soal.

## 14. Pemetaan Bahasa Inggris (hasil pertama)

`build_inggris.py` memetakan 275 topik Inggris P0 ke 22 leaf pohon `english` (`POHON_HIERARKI_DOMAIN_LAIN_V1` bagian 2), memberi label CEFR, dan menilai apa yang sudah ada di perpustakaan. Aturannya berbasis kluster dan judul topik (judul lama berbahasa Inggris, leaf berbahasa Indonesia, sehingga TF-IDF tidak cocok). Hasilnya usulan.

**Koreksi kesalahan saya.** Kluster "Fonetik & Fonologi" (7 topik) sebelumnya saya anggap pelafalan dasar. Ternyata ia linguistik S1 dan dipindah ke ekstensi. Dampak: ekstensi 129 menjadi 136, P0 1.420 menjadi 1.413, unit Inggris kanonik 210 menjadi 203.

| Jenis | Topik | Arti |
|---|---:|---|
| Unit kanonik | 203 | dipetakan ke leaf dan CEFR |
| Strategi tes milik path | 72 | IELTS, TOEFL, PTE, TOEIC, Duolingo, dll. |

### 14.1 Aset lama: Inggris berbeda dari Matematika

Berbeda dengan Matematika, topik Inggris lama membawa isi: 799 bab, **471 bermateri**, dan **21.649 soal** (21.647 di antaranya sudah bertag Bloom dan kesulitan). Kesiapan tiap unit:

| Kesiapan | Unit | Arti |
|---|---:|---|
| SIAP-DIPAKAI | 115 | seluruh bab bermateri dan ≥20 soal |
| SEBAGIAN | 3 | ada sebagian materi atau soal |
| KOSONG | 85 | bab hanya kerangka, tanpa materi dan tanpa soal |

- **117 dari 203 unit punya ≥50 soal** (median 150 per unit). Bank tahap 1 (20 soal) dan bahkan tahap 2 (50 soal) untuk unit itu bisa **diseleksi dari soal yang ada tanpa generate baru**, memakai komposisi bagian 10.1.
- Semua materi dan soal itu berstatus **draf buatan AI** (1.089 artikel, 3.275 kuis; tidak satu pun terbit atau ditinjau). Jadi pakai ulang menghemat token generasi, tetapi tetap butuh QA otomatis (kunci jawaban, duplikasi, tag) dan tinjauan manusia. Saya sendiri menemukan satu soal dengan kunci yang bertentangan dengan pembahasannya di bank hasil pipeline yang sama.
- **85 unit KOSONG** semuanya tata bahasa/kosakata (77) dan menulis (8). Contoh: Present Continuous, Simple Present, Articles & Determiners, Modal "Can/Could". Ini butuh produksi penuh. **41 dari 61 topik TKA Bahasa Inggris kosong**, sedangkan untuk UTBK Literasi Inggris hanya 7 dari 26 yang kosong.
- Strategi tes: 72 topik, 290 bab, hanya 32 bermateri, 1.450 soal.

### 14.2 Cakupan leaf

Sebaran unit per strand: grammar_vocabulary 130, writing 28, speaking 21, pronunciation 9, **reading 8, listening 7**.
- **Tiga leaf tidak punya topik lama sama sekali:** `REA4` membaca teks akademik/fungsional/sastra, `SPK1` mengucapkan bunyi/tekanan kata/intonasi, `PRN3` memantau pelafalan mandiri.
- **Keterampilan reseptif sangat tipis**, padahal TKA Bahasa Inggris, UTBK Literasi Inggris, IELTS, dan TOEFL bergantung padanya. Path tes akan merujuk unit membaca dan menyimak yang hampir tidak ada. Ini kandidat produksi baru paling penting untuk Inggris.
- Sebaran CEFR unit: A1 29, A2 43, B1 70, B2 44, C1 14, C2 3. Tingkat atas tipis untuk Cambridge CAE/CPE.
- Judul topik lama berupa frasa benda ("Present Continuous"), sedangkan standar mewajibkan kata kerja + objek ("Menggunakan present continuous untuk kejadian sedang berlangsung"). Penamaan ulang diperlukan sebelum registry.
- Pohon `english` sendiri masih setingkat konsep (22 butir) dan menyatakan perlu dipecah ahli. Keputusan tentang unit sudah diambil pada bagian 15.

### 14.3 Dampak pada biaya (estimasi)

Yang perlu di-generate untuk Inggris P0: 85 unit kosong (+3 sebagian) dan sekitar 40 aset strategi tes yang belum bermateri, sekitar 128 dari 275. Yang lain butuh QA dan perakitan. Dengan asumsi bagian 10.3 (±Rp 310 per modul tahap 1), generate Inggris ≈ Rp 40 ribu, ditambah QA otomatis 115 unit (±Rp 60 per unit, perkiraan kasar dari biaya judge sebelumnya) ≈ Rp 7 ribu. Ini lebih murah daripada perkiraan awal ±Rp 87 ribu untuk 282 modul.

Berkas: `pemetaan_inggris_v1.csv`, `ringkasan_inggris.json`, `statistik_bank_inggris.csv`, `build_inggris.py`.

## 15. Bahasa Inggris dalam struktur baru

Permintaan: menyesuaikan Inggris dengan struktur baru. Tafsir saya: pohon `english` di `POHON_HIERARKI_DOMAIN_LAIN_V1` berhenti di 22 butir, sedangkan aturan bersamanya menyatakan `Domain → Mata Pelajaran → Strand → Konsep/cluster → Unit Belajar` dan meminta strand dipecah oleh ahli menjadi unit. Maka 22 butir itu saya perlakukan sebagai **konsep**, dan unit di bawahnya berasal dari topik lama. Dengan begitu topik lama tidak lagi menjadi unit produksi begitu saja: ia menjadi **sumber** unit yang dinamai ulang sesuai standar.

```text
english (domain)
└─ bahasa_inggris (mapel)
   └─ 6 strand → 22 konsep → 203 unit (kata kerja + objek, label CEFR)
```

Hasilnya dua berkas baru di `outputs/`:
- `POHON_HIERARKI_INGGRIS_V1.md`: pohon Inggris sampai tingkat unit, format sama dengan pohon Matematika.
- `pemetaan-jalur-ujian/registry_inggris_v1.csv` dan `aset_path_inggris_v1.csv`: satu baris per unit dan per aset milik path.

**Unit (203).** Tiap unit membawa: `module_id` (`english.<strand>.<konsep>.<unit>.v1`), nama kata kerja + objek, konsep utama dan sekunder, CEFR, template blueprint, label bernamespace, prioritas (P0a/P0b), kesiapan pakai ulang, dan asal bank tahap 1. Contoh: topik lama "Skimming & Scanning" menjadi `Menerapkan skimming dan scanning`, id `english.receptive_reading.main_idea_supporting_detail.skimming-scanning.v1`, label `cefr:A2` dan seterusnya.

Sebaran konsep: grammar_vocabulary 130, writing 28, speaking 21, pronunciation 9, reading 8, listening 7.

**Label bernamespace (`STANDAR_KURIKULUM` bagian 7).** Path tidak lagi menjadi daftar topik. Ia menjadi label pada unit yang sama:

| Label | Unit yang membawanya |
|---|---:|
| `cefr:A1`…`C2` | 203 (satu per unit) |
| `exam:tka` + `exam-component:bahasa-inggris` | 61 |
| `exam:utbk-snbt` + `exam-component:literasi-bahasa-inggris` | 26 |
| `cambridge:yle-starters` / `yle-movers` / `yle-flyers` | 17 / 12 / 43 |
| `cambridge:ket-a2` / `pet-b1` / `fce-b2` / `cae-c1` / `cpe-c2` | 43 / 70 / 44 / 14 / 3 |
| `exam:ielts` / `toefl-ibt` / `toefl-itp` / `toeic` | 66 / 62 / 49 / 29 |

Penyatuan duplikasi terlihat langsung: unit A2 yang dulu dirujuk tiga kali (CEFR A2, KET, YLE Flyers) sekarang satu unit dengan tiga label. YLE Starters dan Movers ternyata himpunan bagian dari A1, jadi cukup label tambahan. Label `cambridge:*` memakai kode dari dokumen katalog lama.

**Aset milik path (72).** Dipisah dari unit sesuai aturan bahwa hanya `strategy` dan `assessment` boleh dimiliki path:

| Ujian | Aset | Jenis |
|---|---:|---|
| IELTS (Academic dan General) | 18 | strategi; simulasi |
| PTE Academic | 12 | |
| TOEFL iBT | 12 | |
| TOEIC | 9 | |
| TOEFL ITP | 7 | |
| Duolingo dan tes lain | 6 | |
| Umum (lintas tes) | 8 | satu-satunya yang bermateri |

Totalnya 66 strategi dan 6 simulasi berwaktu (`assessment`). **64 dari 72 hanya kerangka bab tanpa materi**; 8 aset "umum" sudah bermateri. Kolom `merujuk_strand` mengaitkan tiap aset ke keterampilan yang dilatih (reading 13, speaking 10, listening 9, writing 9, grammar 5, 26 lainnya berupa format/penilaian/simulasi umum), sehingga path ujian tinggal merujuk unit keterampilan yang sesuai.

**Bank tahap 1:** 117 unit diisi dengan **seleksi dari soal lama**, dan 86 unit harus di-generate.

**Yang masih harus diputuskan penelaah Bahasa Inggris.** Semua ini usulan otomatis:
1. **Nama unit.** Unit tata bahasa dan kosakata (130) memakai pola `Menggunakan <istilah Inggris>` atau `Memperluas kosakata: <topik>`. Kata kerja + objeknya benar secara bentuk, tetapi belum spesifik ("Menggunakan Present Continuous" belum menyatakan kompetensi yang terukur seperti standar contoh). Penajaman nama dan tujuan belajar perlu penelaah.
2. **Penempatan konsep.** Judul lama berbahasa Inggris dipetakan ke konsep berbahasa Indonesia dengan aturan tangan, bukan pemeriksaan isi. Contoh yang ambigu: Conditionals & Wishes, Gerunds & Infinitives, dan Common Errors.
3. **Prasyarat.** Belum ada. Urutan CEFR hanya label, bukan graf prasyarat.
4. **Celah konsep.** `Membaca teks akademik, fungsional, dan sastra` hanya tercakup sekunder oleh 6 unit genre teks (Announcement, News Item, Report, Review, Explanation, Procedure). `Mengucapkan bunyi, tekanan kata, dan intonasi` dan `Memantau pelafalan mandiri` belum punya unit sama sekali.
5. ~~Unit genre teks~~ sudah diputuskan pada bagian 16.

## 16. Keputusan genre teks dan QA otomatis unit Inggris

### 16.1 Keputusan: unit genre teks menjadi unit kanonik

Pertanyaan: Recount, Narrative, Report, Procedure, dll. (12 topik) itu unit Inggris kanonik atau materi khusus kurikulum yang hanya dirujuk? **Keputusan: unit kanonik, dengan label kurikulum.**

Alasan:
- Kompetensinya, yaitu membaca dan menulis jenis teks, bukan milik kurikulum Indonesia saja. Jenis teks yang setara dituntut oleh path lain di sini: surat formal/informal di IELTS General Training, dan tulisan tipe laporan/ulasan/artikel di ujian Cambridge.
- `STANDAR_KURIKULUM` bagian 1 melarang menyalin materi per kerangka acuan ("kurikulum adalah kerangka acuan, bukan konten yang disalin"). Membuat unit khusus kurikulum akan menggandakan kompetensi yang sama dengan unit menulis dan membaca.
- Pengikat kurikulumnya cukup label: dua belas unit itu sekarang membawa `framework:kurikulum-merdeka`. Path Kurikulum Indonesia nanti memilihnya lewat label itu, tanpa salinan.

Yang tetap perlu ditinjau penelaah: sebagian namanya khas sekolah Indonesia (Hortatory Exposition, Analytical Exposition, News Item, Discussion Text). Nama unit sebaiknya memakai istilah internasional (argumentatif/persuasif, berita, diskusi), dengan istilah lama disimpan sebagai sinonim pencarian. Enam di antaranya juga melatih membaca teks fungsional (konsep `REA4`).

### 16.2 QA otomatis untuk 117 unit yang bank soalnya bisa diseleksi

`qa_bank_inggris.py` memeriksa 21.649 soal lama (tanpa LLM, tanpa biaya token), lalu memilih 20 soal per unit sesuai komposisi tahap 1 di bagian 10.1.

**Yang diperiksa (struktural dan tag):** stem kosong, kunci hilang atau bukan label, label ganda, pilihan kembar atau kosong, jumlah pilihan, kunci Benar/Salah tidak valid, pembahasan hilang, tag Bloom dan kesulitan hilang, bagian asal hilang, dan duplikasi soal (dalam satu unit dan lintas unit).

**Hasil:**

| Temuan | Soal | Catatan |
|---|---:|---|
| Cacat KRITIS (soal tidak boleh dipakai) | 31 | 15 di antaranya reparabel otomatis: opsi kelima kosong atau kembar dengan opsi keempat |
| Label ganda (mis. A B C D D) | 21 | |
| Pilihan kembar | 15 | |
| Pilihan kosong | 6 | |
| Kunci bukan label yang ada (mis. `"B"` atau `E` pada 4 opsi) | 3 | |
| Kunci hilang | 1 | |
| MAYOR: pembahasan hilang, tag Bloom/kesulitan hilang | 3 | |
| MINOR: kunci isian panjang (>80 karakter), pilihan bukan 4, bagian asal hilang | 114, 64, 14 | informasi |
| Duplikat soal (dalam unit atau lintas unit) | **0** | tidak ada pasangan mirip ≥0,8 |

Dari 21.649 soal, hanya 31 (0,14%) yang cacat struktural. Semua 117 unit tetap punya ≥50 soal layak (minimum tepat 50), sehingga bank tahap 2 juga secara struktur mungkin. Komposisi tahap 2 belum saya bangun.

**Seleksi tahap 1** (`seleksi_tahap1_inggris_v1.csv`, 117 unit × 20 = 2.340 soal):
- Kesulitan tepat 6 mudah / 10 sedang / 4 sulit di **semua** 117 unit.
- Fungsi usulan tepat di semua unit: 2 diagnostik, 8 latihan terarah, 3 latihan mandiri/transfer, 6 checkpoint akhir, 1 remedial.
- Tipe 10 pilihan ganda / 4 benar-salah / 6 isian di 116 unit; satu unit 12/4/4.
- Bloom **tidak** selalu sesuai target (C1 2, C2 3, C3 6, C4 5, C5 2). Bank lama hanya punya 1.308 soal C1 dari 21.649, dan tidak ada C6, sehingga 16 unit tanpa C1. Tahap 2 tidak bisa memenuhi C6 dari soal lama.
- Soal rata-rata tersebar dari 3,7 bab lama per unit, dan tidak ada soal terpilih yang punya temuan MAYOR.

**Batas yang harus diketahui:**
1. **Konsistensi kunci vs pembahasan tidak diperiksa.** Saya mencoba heuristik teks dan mengujinya dengan sampel manual: hasilnya nyaris semua salah alarm (0 dari 4 sampel tepat untuk kunci vs pilihan, dan pembahasan-TF terpicu frasa "salah satu"). Pembahasan wajar membahas pengecoh dan memparafrasa kunci, jadi aturan sederhana menyesatkan. Aturan itu saya buang. Cacat semacam soal Matematika #36 yang kunci dan pembahasannya bertentangan **tidak akan tertangkap** oleh QA ini.
2. **"LOLOS-QA-OTOMATIS" bukan "siap terbit".** Semua soal masih draf buatan AI dan belum ditinjau manusia. Kolom kesiapan sengaja tidak memakai kata "siap".
3. **`miskonsepsi_target`, `dimensi_pengetahuan`, `tujuan_id` tidak ada** pada soal lama, padahal kontrak item mewajibkannya. Bagian asal (`bagian_id`) di data lama adalah bagian dari artikel per bab, bukan Bagian modul baru, jadi harus dipetakan ulang saat modul disusun.
4. Kunci Benar/Salah tidak seimbang: 54% Salah, 46% Benar. Kecil dan tidak diperbaiki.

**Langkah yang saya usulkan untuk menutup batas 1** (belum dikerjakan): verifikasi semantik kunci vs pembahasan memakai LLM **hanya untuk 2.340 soal terpilih**. Volume masukan ±0,4 juta token (rata-rata 687 karakter per soal), atau ±0,7 juta dengan instruksi dan keluaran. Dengan kalibrasi biaya bagian 10.3 (yang kasar, dan sebenarnya terlalu mahal untuk token masukan), itu ±Rp 3 ribu. Untuk seluruh 21.649 soal ±4 juta token masukan, ±Rp 25-30 ribu. Selisihnya menunjukkan mengapa cukup memeriksa soal yang terpilih saja.

Berkas: `qa_bank_inggris.py`, `qa_unit_inggris_v1.csv` (ringkasan per unit), `qa_temuan_inggris_v1.csv` (241 temuan), `seleksi_tahap1_inggris_v1.csv`.
