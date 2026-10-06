# Kalibrasi 1 bab oleh Claude Code

Tujuan: mengukur berapa persen jatah Claude Pro yang dihabiskan satu bab lengkap (materi + 50 soal), supaya tabel di `ATURAN_DAN_RENCANA_GENERATE_V2.md` bagian 2 dan jawaban "berapa persen bab yang bisa tercover" memakai angka nyata.

## Cara menjalankan (pengguna)

1. Tunggu jatah sesi 5 jam reset. Jangan jalankan di percakapan panjang: 96% pemakaian di percakapan lama berada di konteks >150 ribu token, sehingga pengukurannya bias dan mahal.
2. Buka percakapan baru (atau `/clear`). Pilih model yang akan dipakai untuk produksi (Sonnet direkomendasikan; Opus menghabiskan jatah jauh lebih cepat).
3. Buka **Account & Usage**, catat (screenshot) persen Session dan Weekly **sebelum**.
4. Ketik: `kerjakan outputs/kalibrasi_1_bab.md`.
5. Setelah selesai, screenshot Account & Usage lagi (**sesudah**). Selisihnya adalah biaya satu bab.

## Tugas untuk Claude (percakapan baru)

Bab: **Matematika, Kelas 1, topik "Bilangan sampai 20", bab "Membilang dan Mencocokkan Benda dengan Bilangan"** (`bab_id` 173c2e4b-de0d-4c0f-b4ab-99e4a563f86d, Fase A). Dipilih karena pembacanya paling muda, jadi kesesuaian jenjang paling mudah dinilai.

Baca dulu, secukupnya saja:
- `outputs/ATURAN_DAN_RENCANA_GENERATE_V2.md` bagian 1 (aturan materi dan bank).
- Bentuk data: materi ada di `module_items.lesson_plan` pada item artikel anak bab (`sections[]` dengan `id`, `goal`, `title`, `content` markdown dengan blok `:::definition`, `:::steps`, `:::common_trap`, `:::callout`, `minutes`). Bank ada di `quiz_config.question_groups[]` pada item kuis anak bab (soal punya `uid`, `stem` atau `text`, `choices` dengan `label`, `answer`, `explanation`, `taxonomy` berisi `bloom`, `difficulty`, `fungsi`, `knowledge_dimension`, `miskonsepsi_target`). Contoh nyata: bab emas di Matematika Tahap 1 "Bilangan Cacah & Nilai Tempat".
- Standar taksonomi: `titian-backend-rust/src/services/content_factory/blueprint.rs` (`standard_cells`) dan `tagging.rs`.

Hasilkan:
1. **Materi** sesuai profil Fase A: kalimat rata-rata ≤6 kata (maks 10), 3–4 bagian, ≤120 kata per bagian, konteks rumah/sekolah/mainan, konkret dulu, satu blok kesalahan umum, ringkasan akhir.
2. **Bank 50 soal**: 15 mudah / 25 sedang / 10 sulit; Bloom C1 5, C2 8, C3 14, C4 12, C5 6, C6 2 (minimum); fungsi 4 diagnostik, 22 latihan terarah, 8 mandiri, 10 checkpoint akhir, 4 remedial, 2 pengayaan; keempat dimensi pengetahuan terwakili; hanya pilihan ganda, benar/salah, isian satu kata atau angka (isian ≤10%); stem ≤12 kata; C5–C6 disesuaikan dengan anak Kelas 1 (misalnya membandingkan dan memilih cara yang lebih tepat, bukan penalaran abstrak).
3. Simpan ke DB dev pada bab itu (draf, bukan terbit), lalu jalankan pemeriksaan struktur yang sudah ada (`tag_bank` / `tagging::audit`) dan laporkan hasilnya.
4. Laporkan apa adanya: apa yang terasa berat, apa yang tidak sesuai profil, berapa lama, dan apakah materi terbaca oleh anak 6–7 tahun.

Jangan generate bab lain. Jangan mengubah kode. Satu bab saja.

## Dicatat sesudahnya

| | Sebelum | Sesudah | Selisih |
|---|---|---|---|
| Session (5 jam) | | | |
| Weekly (7 hari) | | | |
| Model yang dipakai | | | |
