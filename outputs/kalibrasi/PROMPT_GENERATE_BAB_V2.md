# Prompt generate bab v2 (semua mapel, semua level)

Satu prompt untuk satu bab. Isi placeholder `{{...}}` di blok di bawah garis, tempel ke model (Gemini atau Claude), simpan keluarannya sebagai `hasil_bab_{{NOMOR}}.json`. Jangan mengubah isi prompt selain placeholder; semua aturan per mapel dan per Fase sudah ada di dalamnya, model memilih baris yang sesuai.

Alur wajib sesudahnya (tanpa langkah ini bab tidak dianggap selesai):

```
python3 validasi_bab.py hasil_bab_{{NOMOR}}.json {{FASE}} {{JENIS_SOAL}}
python3 siapkan_penelaahan.py buat hasil_bab_{{NOMOR}}.json          # membuat tanpa_kunci_{{NOMOR}}.json dan berkas penelaah
#   -> beri PROMPT_PENELAAH_BAB.md + berkas itu ke model LAIN (bukan yang menulis)
python3 siapkan_penelaahan.py bandingkan hasil_bab_{{NOMOR}}.json jawaban_{{NOMOR}}.json
python3 impor_bab.py hasil_bab_{{NOMOR}}.json {{BAB_ID}} {{FASE}} {{JENIS_SOAL}}
```

Standar mutu dan ambang lulus ada di `STANDAR_MUTU_BAB_V1.md`.

Cara mengisi: `antrean_generate_v1.csv` memuat mapel, kelas, topik, bab, bab_id. Fase dari kelas (1–2 A, 3–4 B, 5–6 C, 7–9 D, 10–12 E). `{{KESALAHAN_UMUM}}` adalah judul bab "Kesalahan Umum" pada topik yang sama. `{{BAB_LAIN}}` adalah judul bab lain pada topik yang sama.

---

Kamu adalah tim tiga orang dalam satu peran: (1) guru {{MAPEL}} berpengalaman untuk murid Kelas {{KELAS}}, (2) penulis soal bersertifikat yang paham taksonomi Bloom, dan (3) perancang media interaktif. Tugas: menulis **satu bab lengkap** untuk aplikasi belajar Titian Asa, yaitu **materi (termasuk web interaktif bila perlu) dan bank 50 soal**. Mutu adalah prioritas utama. Lebih baik sedikit tetapi benar daripada banyak tetapi meragukan. Jika kamu tidak yakin sebuah fakta, angka, atau hasil hitungan, jangan menulisnya; ganti dengan yang kamu yakini.

## 0. Bab yang ditulis

- Mapel: {{MAPEL}}
- Kelas / Fase: {{KELAS}} / {{FASE}}
- Topik: {{TOPIK}}
- Bab: **{{BAB}}**
- Bab lain pada topik ini (jangan diulang, boleh dirujuk): {{BAB_LAIN}}
- Kesalahan umum topik ini: {{KESALAHAN_UMUM}}
- Jenis soal: {{JENIS_SOAL}}  (hitungan | konsep | bahasa | penalaran)
- Jika judul bab diawali "Kesalahan Umum:", bab ini membahas **satu miskonsepsi**. Susun materi menjadi: kesalahan yang terjadi, mengapa terasa masuk akal, mengapa keliru, cara yang benar, latihan membedakan. Semua soal, termasuk yang remedial, berputar di miskonsepsi itu dan variasinya.

## 1. Profil Fase (pilih baris Fase {{FASE}})

| Fase | Kalimat rata-rata / terpanjang (kata) | Kata per bagian | Bagian | Cara mengajar dan konteks |
|---|---|---|---|---|
| A (1–2) | 6 / 10 | 120 | 3–4 | Konkret dulu (benda, gambar, permainan), simbol sesudahnya. Satu gagasan per kalimat. Rumah, sekolah, mainan, makanan, hewan. Tanpa istilah abstrak. Bilangan ≤100. |
| B (3–4) | 10 / 16 | 180 | 4 | Konkret lalu semi-konkret. Maksimal 3 istilah baru per bagian, masing-masing didefinisikan satu kalimat. Pasar, keluarga, lingkungan. |
| C (5–6) | 14 / 22 | 250 | 4–5 | Contoh kehidupan nyata anak. Abstraksi awal setelah contoh konkret. |
| D (7–9) | 18 / 28 | 300 | 5 | Konteks remaja (olahraga, gawai, uang saku). Pemodelan, alasan "mengapa". |
| E (10–12) | 22 / 34 | 400 | 5 | Konteks akademik, kerja, gaya soal TKA dan UTBK. Istilah dan notasi baku, argumentasi. |

Aturan untuk semua Fase: tiap bagian punya satu `goal` satu kalimat; ada contoh yang dikerjakan langkah demi langkah; ada minimal satu blok `:::common_trap`; bagian terakhir berisi ringkasan; bahasa Indonesia baku yang ramah pembaca (sapaan "kamu"); tidak ada konteks, kosakata, atau contoh yang tidak sesuai usia; tidak ada konten SARA, kekerasan, atau promosi.

## 2. Profil mapel (pilih baris {{MAPEL}})

| Mapel | Jenis soal / komposisi (PG : B-S : isian) | Gaya materi | Rumus | Web interaktif **wajib** bila |
|---|---|---|---|---|
| Matematika | hitungan 35:10:5 | Konkret→gambar→simbol (Fase A–C). Contoh dikerjakan bertahap. | Ya, dari Kelas 7 | ada geometri, grafik, transformasi, statistik, garis bilangan, pola, atau ruang |
| Fisika | hitungan 35:10:5 | Fenomena dulu, lalu konsep, lalu rumus, lalu hitungan bersatuan. | Ya | ada gerak, gelombang, listrik, optik, fluida, termal (simulasi dengan slider) |
| Kimia | hitungan 35:10:5 (konsep 30:12:8 untuk bab teori) | Fenomena, partikel, simbol, hitungan stoikiometri. | Ya (`\mathrm{}`) | ada struktur atom, ikatan, bentuk molekul, kurva titrasi, reaksi |
| Biologi, IPA, IPAS | konsep 30:12:8 | Amati, jelaskan, hubungkan, terapkan. | Sedikit | ada struktur (sel, organ, sistem), siklus, klasifikasi, ekosistem |
| Geografi | konsep 30:12:8 | Fenomena ruang, data, peta, analisis. | Sedikit | ada peta, kontur, diagram iklim, piramida penduduk, proses geologis |
| Sejarah | konsep 30:12:8 | Kronologi, sebab-akibat, sumber, makna. | Tidak | ada linimasa, peta persebaran, perbandingan peristiwa |
| Sosiologi, IPS | konsep 30:12:8 | Konsep, contoh sosial nyata, analisis kasus. | Tidak | ada bagan struktur, stratifikasi, alur interaksi |
| Ekonomi | konsep 30:12:8 (hitungan 35:10:5 untuk bab hitung) | Konsep, contoh pasar nyata, kurva, hitungan. | Ya untuk hitung | ada kurva permintaan-penawaran, aliran uang, tabel hitung |
| Akuntansi | hitungan 35:10:5 | Transaksi, akun, jurnal, laporan, langkah bertahap. | Tidak (pakai `:::table`) | ada jurnal, buku besar, neraca, siklus akuntansi |
| Bahasa Indonesia | bahasa 28:8:14 | Teks contoh dulu, ciri, kaidah, latihan menulis dan membaca. | Tidak | ada susun kalimat, klasifikasi teks, pengucapan |
| Bahasa Inggris | bahasa 28:8:14 | Penjelasan berbahasa Indonesia, contoh Inggris sesuai CEFR (A1 ≤6 kata per kalimat, A2 ≤10, B1 ≤15), disertai arti. Stem dan pilihan berbahasa Inggris, pembahasan berbahasa Indonesia. | Tidak | ada pelafalan (`speechSynthesis`), susun kalimat, mencocokkan kosakata |
| Penalaran & Logika | penalaran 38:7:5 | Semua informasi ada di soal; tidak butuh pengetahuan luar. Strategi dan contoh bertahap. | Sedikit | ada pola gambar, tabel kebenaran, penjadwalan, diagram Venn |

Web interaktif **opsional tetapi dianjurkan** pada bab lain jika ia membuat konsep lebih jelas. Jangan membuat web interaktif yang hanya menghias teks.

## 3. Materi

Struktur satu bagian: `id` (12 karakter hex acak, unik), `title`, `goal`, `minutes`, `content` (markdown). Blok terstruktur yang dikenali aplikasi, ditutup `:::` pada baris sendiri:

- `:::definition` (`term:`, `definition:`)
- `:::steps` (`title:`, `items: ["...", "..."]`)
- `:::table` (`headers: [...]`, `rows: [[...]]`, `caption:`)
- `:::common_trap` (`term:`, `explanation:`)
- `:::callout` (`variant: tip|warning|important`, `title:`, `text:`)

Larangan: jangan menulis tautan luar, jangan "perhatikan gambar" (tidak ada gambar; pakai web interaktif atau deskripsi kata), jangan mengarang data statistik atau kutipan.

Emoji hanya sebagai objek hitung pada Fase A–B.

## 4. Rumus dan simbol (KaTeX)

- Rumus baris `$x^2+3x$`, blok `$$\frac{a}{b}$$`. Hanya dua pembatas itu. Jangan memakai `\(...\)`, `\[...\]`, `\begin{equation}`.
- Berlaku di materi, stem, pilihan, pembahasan. Jangan di judul bagian atau `label`.
- Di JSON, setiap garis miring terbalik ditulis dua kali: `"$\\frac{1}{2}$"`.
- Dolar untuk uang ditulis `\$` (di JSON `\\$`) atau, lebih baik, "Rp5.000". Tanda `$` tunggal dilarang.
- **Kunci isian ditulis polos tanpa LaTeX**, semua penulisan wajar dipisah `|` (`2x+3|2x + 3`, `1/2|0,5`). Murid mengetik jawabannya, jadi soal isian harus meminta jawaban yang bisa diketik. Untuk ekspresi aljabar yang penulisannya banyak ragam, pakai pilihan ganda.
- Kimia: `\ce{}` tidak ada. Tulis `$\mathrm{H_2O}$`, reaksi `\rightarrow` atau `\rightleftharpoons`.
- Fisika dan Kimia: besaran selalu bersatuan, mis. `$5\,\mathrm{m/s}$`.
- Fase A–C: rumus hanya bila perlu (pecahan sederhana boleh).
- Panjang kalimat tidak menghitung isi rumus.

## 5. Web interaktif (untuk gambar, geometri, simulasi, dan penjelasan yang tidak cukup dengan teks)

Web interaktif disisipkan ke dalam materi. Kamu tidak menulisnya di dalam `content`; kamu menaruhnya di daftar `interaktif` pada keluaran (bagian 8) dan menandai posisinya dengan `[[interaktif:1]]`, `[[interaktif:2]]` di dalam `content` bagian yang bersangkutan. Jumlah: 0–3 per bab.

Syarat setiap web interaktif:
1. **Satu dokumen HTML lengkap**, dimulai `<!DOCTYPE html>`, CSS di `<style>`, JavaScript di `<script>`. Maksimal 120.000 karakter.
2. **Setia pada materi bab ini.** Isinya hanya yang diajarkan di bagian materi tempat ia berada. Dilarang menambah fakta, istilah, atau contoh baru. Jika memuat kuis mini, gunakan **persis** soal dari bank 50 (stem, pilihan, kunci tidak diubah).
3. **Benar-benar interaktif**: slider, seret-dan-lepas, klik untuk mengungkap, input yang mengubah gambar. Bukan teks statis dibungkus kartu. Ada tombol reset. Berfungsi di layar sentuh dan desktop. Target sentuh ≥44 px.
4. **Tema Titian Asa.** Salin token warna di bawah **persis** ke `:root` dan `html.dark`, dan pakai hanya token ini untuk warna (`var(--primary)` dst). Jangan membuat toggle tema. Kontras tinggi di kedua mode.

```
:root {
  --background: oklch(0.978 0.007 245); --foreground: oklch(0.18 0.02 260);
  --card: oklch(1 0 0); --card-foreground: oklch(0.18 0.02 260);
  --primary: oklch(0.82 0.17 86); --primary-foreground: oklch(0.16 0.04 60);
  --secondary: oklch(0.95 0.012 245); --secondary-foreground: oklch(0.25 0.02 260);
  --muted: oklch(0.95 0.008 245); --muted-foreground: oklch(0.50 0.02 250);
  --accent: oklch(0.94 0.05 86); --accent-foreground: oklch(0.25 0.05 70);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.925 0.008 245); --ring: oklch(0.82 0.17 86);
  --chart-1: oklch(0.82 0.17 86); --chart-2: oklch(0.65 0.15 60);
  --chart-3: oklch(0.5 0.12 40); --chart-4: oklch(0.7 0.14 130); --chart-5: oklch(0.6 0.1 250);
  --radius: 1rem;
}
html.dark, [data-theme="dark"] {
  --background: oklch(0.15 0.015 250); --foreground: oklch(0.96 0.01 90);
  --card: oklch(0.20 0.018 250); --card-foreground: oklch(0.96 0.01 90);
  --primary: oklch(0.85 0.18 86); --primary-foreground: oklch(0.14 0.04 60);
  --secondary: oklch(0.25 0.015 250); --secondary-foreground: oklch(0.96 0.01 90);
  --muted: oklch(0.25 0.015 250); --muted-foreground: oklch(0.68 0.02 250);
  --accent: oklch(0.30 0.05 86); --accent-foreground: oklch(0.94 0.03 90);
  --destructive: oklch(0.704 0.191 22.216);
  --border: oklch(1 0 0 / 9%); --ring: oklch(0.85 0.18 86);
  --chart-1: oklch(0.85 0.18 86); --chart-2: oklch(0.72 0.15 60);
  --chart-3: oklch(0.6 0.12 40); --chart-4: oklch(0.75 0.14 130); --chart-5: oklch(0.65 0.1 250);
}
```
5. **Jembatan penilaian.** Panggil `window.Titian.complete()` saat seluruh penjelajahan selesai, dan `window.Titian.submitScore(skor, skorMaksimal)` (dua bilangan, bukan persen) **tepat sekali** per penyelesaian bila ada kuis mini. `window.Titian.celebrate()` untuk momen berhasil. Jangan memanggil tiap ketukan.
6. **Keselamatan:** tanpa `<iframe>`, `<object>`, `<embed>`, tanpa handler inline (`onclick=`), tanpa tautan atau sumber luar kecuali CDN `cdn.jsdelivr.net` dan `cdnjs.cloudflare.com`. Pakai `addEventListener`. Jangan `height: 100vh`; tinggi mengikuti isi.
7. **Library yang boleh** (bila perlu): KaTeX (`https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js` dan `.css`), Chart.js, Three.js r128, Matter.js, canvas-confetti, HanziWriter. Untuk geometri dan diagram, **SVG murni atau Canvas** sudah cukup dan lebih andal.
8. **Aksesibilitas dan bahasa:** teks antarmuka bahasa Indonesia yang ramah (Bahasa Inggris untuk konten Inggris), label tombol jelas, informasi tidak hanya lewat warna, dapat dipakai dengan keyboard bila memungkinkan.
9. **Kebenaran:** angka, rumus, dan gambar dalam simulasi harus benar (skala, sudut, satuan). Jika ragu, sederhanakan.

Panduan pilihan: geometri dan grafik (SVG dengan titik yang bisa digeser), simulasi gerak dan gelombang (slider), struktur (klik bagian untuk melihat nama dan fungsi), linimasa (klik peristiwa), peta (klik wilayah), jurnal dan neraca (isi lalu periksa), susun kalimat (seret kata), pelafalan (`speechSynthesis`).

Pada Fase A–B, web interaktif berupa permainan sentuh sederhana (hitung dengan mengetuk, seret benda ke kotak). Teks di dalamnya mengikuti batas kalimat Fase.

## 6. Bank 50 soal

Tepat 50 soal. Sebaran per sel harus persis:

| Bloom | Kesulitan | Fungsi | Jumlah |
|---|---|---|---:|
| c1 | mudah | diagnostik | 2 |
| c1 | mudah | latihan_terarah | 3 |
| c2 | mudah | diagnostik | 2 |
| c2 | mudah | remedial | 2 |
| c2 | mudah | latihan_terarah | 4 |
| c3 | mudah | latihan_terarah | 2 |
| c3 | sedang | checkpoint_akhir | 4 |
| c3 | sedang | remedial | 2 |
| c3 | sedang | latihan_terarah | 6 |
| c4 | sedang | checkpoint_akhir | 3 |
| c4 | sedang | latihan_terarah | 7 |
| c5 | sedang | checkpoint_akhir | 3 |
| c3 | sulit | latihan_mandiri | 2 |
| c4 | sulit | latihan_mandiri | 3 |
| c5 | sulit | latihan_mandiri | 3 |
| c6 | sulit | pengayaan | 2 |

Total: mudah 15, sedang 25, sulit 10. Bloom: c1 5, c2 8, c3 16, c4 13, c5 6, c6 2.

Aturan:
- **Tipe hanya tiga:** `multiple_choice`, `true_false`, `short_answer`. Komposisi mengikuti baris mapel di bagian 2. Fase A–B: isian maksimal 5, jawaban satu kata atau satu angka.
- **Pilihan ganda: tepat 4 pilihan** berlabel A–D, satu kunci, tiga pengecoh masuk akal yang mewakili kesalahan nyata murid. Dilarang "semua benar", "semua salah", "tidak ada yang benar". Panjang pilihan seimbang. Kunci tersebar: tidak ada huruf yang jadi kunci >40%.
- **Benar/salah:** pernyataan yang jelas dan tidak ambigu; tidak untuk c5 dan c6; kunci Benar dan Salah kira-kira seimbang.
- **Isian:** jawaban tunggal tak ambigu; ragam penulisan dipisah `|`.
- **Remedial (4):** pilihan ganda; masing-masing menarget satu miskonsepsi nyata di `miskonsepsi_target`, dan pengecoh utamanya adalah miskonsepsi itu. Ambil dari {{KESALAHAN_UMUM}} dan dari kesalahan yang lazim pada bab ini.
- **Pengayaan (2):** c6, pilihan ganda.
- **Dimensi pengetahuan:** tiap soal diberi `knowledge_dimension` (`faktual`, `konseptual`, `prosedural`, `metakognitif`). Minimal 3 soal per dimensi, metakognitif minimal 2.
- **Tingkat kesulitan relatif terhadap kelas.** "Sulit" berarti sulit untuk murid Kelas {{KELAS}}, bukan mutlak. Fase A–B: stem ≤12 kata; C4–C6 tetap ada tetapi disesuaikan usia.
- **Setia pada materi:** setiap soal menunjuk satu bagian materi lewat `source_section_id` dan hanya menguji yang diajarkan di materi bab ini.
- **Tidak berbasis gambar.** Bank soal tidak punya gambar. Jika soal membutuhkan bangun, grafik, atau tabel, deskripsikan dengan kata dan angka pada stem ("Segitiga siku-siku dengan sisi tegak 3 cm dan 4 cm ...") atau tabel teks; penjelajahan visual diberikan lewat web interaktif di materi.
- **Pembahasan** wajib, 1–3 kalimat: mengapa kunci benar dan, untuk pilihan ganda, mengapa pengecoh utama keliru. Soal C3 ke atas pada mapel hitungan memuat langkah singkat.
- **Verifikasi hitungan.** Untuk mapel hitungan, isi bidang `verifikasi` pada soal yang kuncinya berupa bilangan: `{"ekspresi": "3*4+2", "hasil": "14"}`. `ekspresi` adalah ekspresi Python yang boleh memakai `sqrt, sin, cos, tan, log, log10, exp, pi, e, factorial, comb, perm, gcd, radians, degrees, floor, ceil, abs, round, min, max, sum, Fraction, pow`. Komputer akan menghitung ekspresi itu dan membandingkannya dengan kuncimu. **Hitung kuncinya dari ekspresi ini, jangan dari kepalamu.** Minimal 20 soal untuk jenis hitungan.
- Tidak ada stem kembar dan tidak ada soal yang jawabannya bocor dari soal lain.

## 7. Periksa sendiri sebelum menjawab

1. Jumlah soal per sel persis. 2. Tiap kalimat materi sesuai batas Fase. 3. Tiap `source_section_id` ada; tiap kunci ada di pilihannya. 4. **Kerjakan ulang semua soal dari awal seolah kamu murid**, lalu cocokkan dengan kunci; perbaiki yang tidak cocok. 5. Setiap web interaktif diuji dalam kepala: tombol berfungsi, tidak ada variabel yang tidak terdefinisi, `window.Titian` dipanggil. 6. Jika bisa menjalankan kode: `python3 validasi_bab.py hasil_bab_{{NOMOR}}.json {{FASE}} {{JENIS_SOAL}}` harus mencetak **LOLOS**; jika GAGAL perbaiki sampai lolos.

## 8. Format keluaran (satu objek JSON, tanpa teks lain)

```json
{
  "lesson_plan": {
    "title": "{{BAB}}", "topic": "{{TOPIK}}", "level": "Kelas {{KELAS}} — Fase {{FASE}}", "language": "id",
    "sections": [
      {"id": "12hexacak", "title": "...", "goal": "...", "minutes": 5, "content": "markdown, boleh berisi [[interaktif:1]]"}
    ]
  },
  "interaktif": [
    {"section_id": "id bagian tempat ia berada", "title": "judul singkat", "html": "<!DOCTYPE html>..."}
  ],
  "quiz_config": {
    "level": "Kelas {{KELAS}} — Fase {{FASE}}",
    "sections": [{"title": "judul bagian", "section_id": "id bagian"}],
    "passing_score": 70.0, "shuffle_choices": true, "shuffle_question_order": true,
    "question_groups": [
      {"type": "multiple_choice", "group_id": "mc", "instruction": "Pilih jawaban yang paling tepat.", "ai_meta": {"draft": true},
       "questions": [{"uid": "uuid v4 unik", "number": 1, "stem": "...",
         "choices": [{"label": "A", "text": "..."}, {"label": "B", "text": "..."}, {"label": "C", "text": "..."}, {"label": "D", "text": "..."}],
         "answer": "B", "explanation": "...",
         "taxonomy": {"bloom": "c1", "difficulty": "mudah", "fungsi": "diagnostik", "knowledge_dimension": "faktual", "miskonsepsi_target": "hanya untuk remedial"},
         "source_section_id": "id bagian", "verifikasi": {"ekspresi": "...", "hasil": "..."}}]},
      {"type": "true_false", "group_id": "tf", "instruction": "Tentukan benar atau salah.", "options": ["Benar", "Salah"], "ai_meta": {"draft": true},
       "questions": [{"uid": "...", "number": 36, "text": "pernyataan", "answer": "Benar", "explanation": "...", "taxonomy": {}, "source_section_id": "..."}]},
      {"type": "short_answer", "group_id": "sa", "instruction": "Jawab singkat dengan satu angka atau satu kata.", "ai_meta": {"draft": true},
       "questions": [{"uid": "...", "number": 46, "stem": "...", "answer": "10|sepuluh", "explanation": "...", "taxonomy": {}, "source_section_id": "..."}]}
    ]
  }
}
```

Kesalahan format yang sering terjadi (jangan diulang): kunci pilihan ganda adalah **huruf pada `answer` di tingkat soal** (bukan `answer: true` per pilihan; pilihan hanya `label` dan `text`); benar/salah memakai `text` bukan `stem`; `uid` UUID unik (bukan "q01"); `number` berurutan 1–50; pilihan ganda selalu 4; tidak ada properti `t`, `subtype`, `key`; `verifikasi` hanya di soal hitungan.
