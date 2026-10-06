# Prompt generate satu bab (materi + 50 soal)

Cara pakai: salin blok di bawah garis, isi semua `{{...}}`, tempel ke Gemini/Claude. Satu prompt = satu bab. Hasilnya satu berkas `hasil_bab_{{NOMOR}}.json`. Lalu:

```
python3 validasi_bab.py hasil_bab_{{NOMOR}}.json {{FASE}}
python3 impor_bab.py hasil_bab_{{NOMOR}}.json {{BAB_ID}} {{FASE}}
```

`validasi_bab.py` menolak hasil yang menyimpang dari aturan (jumlah soal, sebaran, panjang kalimat, skema). `impor_bab.py` menulis ke DB dev dan menyegarkan ringkasan bank sehingga bab langsung muncul di jalur belajar. Kalau validasi gagal, tempel pesan galatnya kembali ke model dan minta perbaikan, jangan diperbaiki manual.

Isi `{{...}}` yang bergantung pada bab bisa diambil dari `outputs/kurikulum/antrean_generate_v1.csv` (mapel, kelas, topik, bab, bab_id). `{{KESALAHAN_UMUM}}` adalah judul bab "Kesalahan Umum" pada topik yang sama di rencana kurikulum. `{{BAB_LAIN}}` adalah judul bab lain pada topik itu.

---

Kamu adalah guru {{MAPEL}} berpengalaman sekaligus penulis soal untuk aplikasi belajar Titian Asa. Tugasmu: menulis **satu bab lengkap**, yaitu **materi** dan **bank 50 soal**, untuk murid **Kelas {{KELAS}}** (Fase {{FASE}}).

## Bab yang ditulis

- Mapel: {{MAPEL}}
- Kelas / Fase: {{KELAS}} / {{FASE}}
- Topik: {{TOPIK}}
- Bab: **{{BAB}}**
- Bab lain pada topik ini (jangan diulang, boleh dirujuk): {{BAB_LAIN}}
- Kesalahan umum topik ini (jadikan bahan blok kesalahan umum dan soal remedial): {{KESALAHAN_UMUM}}
- Jenis soal mapel: {{JENIS_SOAL}}  (hitungan / konsep / bahasa / penalaran)

## Bagian 1 — Materi

Tulis untuk pembaca berusia sesuai kelasnya. Jangan memakai bahasa, contoh, atau isi yang tidak sesuai pembaca. Patuhi batas Fase {{FASE}} ini:

| Fase | Rata-rata kata per kalimat | Kalimat terpanjang | Kata per bagian | Jumlah bagian |
|---|---|---|---|---|
| A (Kelas 1–2) | 6 | 10 | 120 | 3–4 |
| B (Kelas 3–4) | 10 | 16 | 180 | 4 |
| C (Kelas 5–6) | 14 | 22 | 250 | 4–5 |
| D (Kelas 7–9) | 18 | 28 | 300 | 5 |
| E (Kelas 10–12) | 22 | 34 | 400 | 5 |

Aturan isi:
- Satu bagian membahas satu gagasan yang menuju tujuan bab. Setiap bagian punya `goal` satu kalimat ("Aku bisa ...", atau "Siswa dapat ...").
- Fase A–C: mulai dari yang **konkret** (benda, gambar, permainan, situasi sehari-hari), baru simbol dan istilah. Fase A: satu gagasan per kalimat, kosakata sederhana, tanpa istilah abstrak. Fase B: maksimal 3 istilah baru per bagian, masing-masing dengan definisi satu kalimat.
- Konteks contoh mengikuti usia: Fase A rumah, sekolah, mainan, makanan, hewan. Fase B pasar, keluarga, lingkungan. Fase C kehidupan anak sehari-hari. Fase D remaja (olahraga, gawai, uang saku). Fase E akademik, kerja, gaya soal TKA dan UTBK. Jangan memakai konteks yang tidak dipahami anak seusia itu.
- Sertakan contoh yang dikerjakan langkah demi langkah, minimal satu **`:::common_trap`** (kesalahan umum, berdasarkan {{KESALAHAN_UMUM}}), dan ringkasan di bagian akhir.
- Untuk Bahasa Inggris: penjelasan berbahasa Indonesia, contoh kalimat Inggris sesuai tingkat CEFR bab (A1 maksimal 6 kata per kalimat, A2 10, B1 15), disertai terjemahan atau penjelasan.
- Gunakan blok terstruktur yang dikenali aplikasi, di dalam teks `content` (markdown):
  - `:::definition` dengan baris `term:` dan `definition:`
  - `:::steps` dengan `title:` dan `items: ["...", "..."]`
  - `:::table` dengan `headers: [...]`, `rows: [[...]]`, `caption:`
  - `:::common_trap` dengan `term:` dan `explanation:`
  - `:::callout` dengan `variant: tip|warning|important`, `title:`, `text:`
  - Setiap blok ditutup `:::` pada baris sendiri.
- Bahasa Indonesia baku yang ramah anak. Sapaan "kamu". Tanpa emoji berlebihan; emoji hanya sebagai gambar hitungan atau benda pada Fase A–B.

## Bagian 2 — Bank 50 soal

Tepat 50 soal, dengan sebaran berikut. Isi tabel ini sel demi sel; jumlah per sel harus persis.

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

Ringkasan yang harus terpenuhi: mudah 15, sedang 25, sulit 10. Bloom: c1 5, c2 8, c3 16, c4 13, c5 6, c6 2.

Aturan soal:
- **Tipe hanya tiga:** `multiple_choice`, `true_false`, `short_answer`. Jangan membuat tipe lain.
- **Komposisi tipe:** {{KOMPOSISI_TIPE}}  (Hitungan: 35 pilihan ganda, 10 benar/salah, 5 isian. Konsep: 30 / 12 / 8. Bahasa: 28 / 8 / 14. Penalaran: 38 / 7 / 5.) Untuk Fase A–B isian tidak lebih dari 5, jawabannya satu kata atau satu angka.
- **Pilihan ganda: tepat 4 pilihan** berlabel A, B, C, D. Satu kunci. Tiga pengecoh masuk akal dan mewakili kesalahan nyata murid. **Dilarang** "semua benar", "semua salah", atau "tidak ada yang benar". Sebar posisi kunci: tidak ada huruf yang menjadi kunci lebih dari 40% soal pilihan ganda.
- **Benar/salah:** kalimat pernyataan yang jelas. Jangan dipakai untuk c5 dan c6. Sebar kunci Benar dan Salah kira-kira seimbang.
- **Isian singkat:** jawaban tunggal yang tidak ambigu. Jika ada beberapa penulisan yang benar, gabungkan dengan tanda `|` ("10|sepuluh").
- **Remedial (4 soal):** semuanya pilihan ganda. Masing-masing menargetkan satu miskonsepsi nyata, ditulis di `miskonsepsi_target`; pengecoh utamanya adalah miskonsepsi itu. Ambil dari {{KESALAHAN_UMUM}}.
- **Pengayaan (2 soal):** bloom c6 (mencipta atau merancang), pilihan ganda.
- **Dimensi pengetahuan:** setiap soal diberi `knowledge_dimension` salah satu dari `faktual`, `konseptual`, `prosedural`, `metakognitif`. Minimal 3 soal untuk tiap dimensi dan minimal 2 untuk metakognitif.
- **Jenjang:** Fase A–B: stem maksimal 12 kata, satu pertanyaan per soal. Bloom c4–c6 tetap ada tetapi disesuaikan usia (misalnya membandingkan dan memilih cara yang lebih tepat, bukan penalaran abstrak). Kesulitan "sulit" berarti sulit **untuk kelas ini**, bukan sulit secara mutlak.
- Setiap soal wajib punya pembahasan singkat (1–3 kalimat) yang menjelaskan mengapa kunci benar dan, untuk pilihan ganda, mengapa pengecoh utama keliru.
- Setiap soal menunjuk satu bagian materi lewat `source_section_id` (harus sama dengan `id` sebuah bagian di `lesson_plan.sections`). Soal tidak boleh menguji hal yang tidak diajarkan di materi.
- Tidak ada stem yang kembar. Tidak ada soal yang jawabannya bocor dari soal lain.

## Bagian 2b — Penulisan rumus dan simbol (semua mapel, wajib pada Matematika, Fisika, Kimia, Akuntansi)

Aplikasi menampilkan rumus dengan KaTeX. Aturannya:
- Rumus baris: `$x^2 + 3x$`. Rumus blok: `$$\frac{a}{b}$$`. **Hanya dua pembatas itu.** Jangan memakai `\(...\)`, `\[...\]`, atau `\begin{equation}`.
- Berlaku di materi, stem, teks pilihan, dan pembahasan. Jangan taruh rumus di judul bagian atau di `label`.
- Di dalam berkas JSON, setiap garis miring terbalik ditulis **dua kali**. Rumus `$\frac{1}{2}$` ditulis `"$\\frac{1}{2}$"` di JSON. Pastikan JSON tetap valid.
- Tanda dolar untuk uang ditulis `\$` (di JSON `\\$`); lebih baik tulis "Rp5.000" tanpa dolar. Tanda `$` tunggal tanpa pasangan dilarang.
- Kunci **isian singkat ditulis polos, tanpa LaTeX**, karena murid mengetik jawabannya: `2x+3|2x + 3`. Beri semua penulisan yang wajar dipisah `|` (pecahan `1/2|0,5`, satuan dengan dan tanpa spasi). Soal isian harus meminta jawaban yang bisa diketik.
- Kimia: `\ce{}` tidak tersedia. Tulis `$\mathrm{H_2O}$`, `$\mathrm{CO_2}$`, reaksi dengan `\rightarrow` atau `\rightleftharpoons`, muatan `$\mathrm{Na^+}$`.
- Fisika dan Kimia: tulis besaran dengan satuan, mis. `$5\,\mathrm{m/s}$`. Matematika Kelas 7 ke atas: ekspresi dan persamaan ditulis dengan rumus, bukan teks polos.
- Fase A–C: jangan memakai rumus kecuali perlu (pecahan sederhana `$\frac{1}{2}$` boleh). Bilangan dan operasi dasar ditulis biasa.
- Diagram dan gambar belum didukung di bank soal. Untuk geometri, gerak, atau rangkaian, **deskripsikan dengan kata dan angka pada stem** (mis. "Segitiga siku-siku dengan sisi tegak 3 cm dan 4 cm ...") atau pakai tabel. Jangan menulis "perhatikan gambar".
- Aturan panjang kalimat tidak menghitung isi rumus.

## Catatan khusus per mapel

- **Matematika dan sains hitungan:** soal hitungan harus bisa diselesaikan tanpa kalkulator kecuali disebut. Bilangan dipilih supaya hasilnya wajar. Setiap soal C3 ke atas menyertakan langkah singkat di pembahasan. Periksa sendiri hasil hitungannya sebelum menulis kunci.
- **Bahasa Inggris:** stem dan pilihan dalam bahasa Inggris, instruksi dan pembahasan dalam bahasa Indonesia. Kosakata dan struktur sesuai CEFR bab.
- **Sejarah, Sosiologi, Geografi, Ekonomi, Biologi (konsep):** soal isian hanya untuk istilah yang tunggal dan baku; selebihnya pilihan ganda dan benar/salah.
- **Penalaran dan logika:** semua informasi ada di soal; tidak boleh membutuhkan pengetahuan luar.

## Bagian 3 — Format keluaran (wajib persis)

Keluarkan **satu objek JSON saja** tanpa teks lain, disimpan sebagai `hasil_bab_{{NOMOR}}.json`:

```json
{
  "lesson_plan": {
    "title": "{{BAB}}",
    "topic": "{{TOPIK}}",
    "level": "Kelas {{KELAS}} — Fase {{FASE}}",
    "language": "id",
    "sections": [
      {"id": "12 karakter hex acak", "title": "...", "goal": "...", "minutes": 4, "content": "markdown dengan blok ::: ..."}
    ]
  },
  "quiz_config": {
    "level": "Kelas {{KELAS}} — Fase {{FASE}}",
    "sections": [{"title": "sama dengan judul bagian", "section_id": "sama dengan id bagian"}],
    "passing_score": 70.0,
    "shuffle_choices": true,
    "shuffle_question_order": true,
    "question_groups": [
      {"type": "multiple_choice", "group_id": "mc", "instruction": "Pilih jawaban yang paling tepat.", "ai_meta": {"draft": true},
       "questions": [
         {"uid": "uuid v4 unik", "number": 1, "stem": "...",
          "choices": [{"label": "A", "text": "..."}, {"label": "B", "text": "..."}, {"label": "C", "text": "..."}, {"label": "D", "text": "..."}],
          "answer": "B",
          "explanation": "...",
          "taxonomy": {"bloom": "c1", "difficulty": "mudah", "fungsi": "diagnostik", "knowledge_dimension": "faktual", "miskonsepsi_target": "hanya untuk remedial"},
          "source_section_id": "id bagian"}
       ]},
      {"type": "true_false", "group_id": "tf", "instruction": "Tentukan benar atau salah.", "options": ["Benar", "Salah"], "ai_meta": {"draft": true},
       "questions": [
         {"uid": "...", "number": 36, "text": "pernyataan", "answer": "Benar", "explanation": "...", "taxonomy": {...}, "source_section_id": "..."}
       ]},
      {"type": "short_answer", "group_id": "sa", "instruction": "Jawab singkat dengan satu angka atau satu kata.", "ai_meta": {"draft": true},
       "questions": [
         {"uid": "...", "number": 46, "stem": "...", "answer": "10|sepuluh", "explanation": "...", "taxonomy": {...}, "source_section_id": "..."}
       ]}
    ]
  }
}
```

Catatan format yang sering salah (jangan diulang):
- Kunci pilihan ganda adalah **huruf pada `answer` di tingkat soal**, bukan bendera `answer: true` pada tiap pilihan. Pilihan hanya punya `label` dan `text`.
- Pertanyaan benar/salah memakai `text` (bukan `stem`) dan `answer` berisi kata **Benar** atau **Salah**.
- `uid` harus **UUID unik** (bukan "q01"), `number` berurutan 1–50 lintas kelompok.
- Pilihan ganda selalu **4** pilihan.
- Tidak ada properti `t`, `subtype`, atau `key`.

## Bagian 4 — Periksa sendiri sebelum menjawab

1. Hitung jumlah soal per sel di tabel bagian 2. Harus persis.
2. Setiap kalimat materi sesuai batas Fase {{FASE}}. Kalau ada yang lebih panjang, pecah.
3. Setiap `source_section_id` ada di materi. Setiap kunci ada di pilihannya.
4. Posisi kunci pilihan ganda tersebar.
5. Jika kamu bisa menjalankan kode: `python3 validasi_bab.py hasil_bab_{{NOMOR}}.json {{FASE}}` harus mencetak **LOLOS**. Jika GAGAL, perbaiki dan jalankan lagi sampai lolos.
