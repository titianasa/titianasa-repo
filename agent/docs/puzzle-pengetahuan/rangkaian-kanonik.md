# Rangkaian kanonik kartu: Matematika dan Bahasa Inggris

Status: struktur kanonik diterapkan di dev (2026-11-02). Kartu lengkap: Bahasa Inggris 227 dari 227 unit, Matematika 274 dari 274 unit.

**Sumber kebenaran:** `titian-backend-go/data/kanonik/`.
- Bahasa Inggris: `bahasa_inggris.py`, 227 unit.
- Matematika: `matematika.json`, 274 unit.
- Jalur: `jalur/*.json`, `ujian.py`, dan jalur sekolah serta CEFR Bahasa Inggris yang dibangun di `build.py`.
- Peta deck: `kartu.py`.

`build.py` memeriksa semuanya lalu menulis `internal/kartu/seed.sql`, yang dimuat oleh `cmd/tools/seed_jalur`.

**Aturan pemilik:** karena belum produksi, data lama tidak dibawa. Tabel kanonik hanya berisi apa yang tertulis di berkas, tanpa alias, tanpa label otomatis, tanpa tautan ke bab lama, dan tanpa level draf. Backup sebelum pembersihan ada di `/home/john/backups/dev_canon_sebelum_kanonik_baru_20261102.dump`.

## Prinsip

1. **Kanonik adalah materinya sendiri, tanpa kelas dan tanpa ujian.** Satu unit kanonik adalah satu kemampuan, misalnya "Menjumlahkan bilangan bulat berbeda tanda". Kelas, fase, TKA, dan SNBT hanyalah jalur yang menunjuk ke unit itu (ADR-0026).
2. **Satu unit, satu rumah.** Topik yang sama tidak boleh punya dua unit, walau muncul di dua sumber. Contohnya plural noun dari game dan dari Part of Speech harus menjadi satu unit.
3. **Menyeluruh.** Setiap sub-elemen CP 2025, kisi-kisi TKA, dan cakupan SNBT harus punya minimal satu unit. Daftar periksanya ada di `tinjauan-jalur-belajar.md`.
4. **Bentuknya deck kartu** (ADR-0025). Satu unit berisi 1–3 deck materi, ditambah deck latihan bila perlu. Satu kumpulan (konsep) dibuka dengan Cek Awal.
5. **Standar selesai per kumpulan:**
   - Semua unit punya deck.
   - Hitungan dicek otomatis.
   - Teks natural.
   - Kartu tidak meluap di 4:5 dan 9:16.
   - Audio tersambung bila ada.
   - Sudah dirender.

## Matematika

Kanonik Matematika memakai pohon yang sudah ada (`outputs/POHON_HIERARKI_MATEMATIKA_V1.md`, sama dengan `canon_units` di DB): 7 strand, 46 konsep, 253 unit. Strukturnya sudah sesuai elemen CP, jadi tinggal ditambal.

### Celah terhadap CP 2025, TKA, dan SNBT

| Asal | Yang belum punya unit |
|---|---|
| CP Fase A–C | Pola bukan bilangan dan makna "=", pengukuran tak baku, posisi dan arah, mengenal bangun ruang, turus dan piktogram, uang, durasi waktu, tampak depan/atas/samping, peta berpetak, kemungkinan lebih besar atau lebih kecil |
| CP Fase D dan TKA SD/SMP | Kecepatan dan laju perubahan, literasi finansial dasar, frekuensi relatif |
| CP Fase E–F | Box plot, dot plot, diagram pencar, asosiasi dua variabel dan garis terbaik, frekuensi harapan |
| TKA Matematika Lanjutan | Polinomial (operasi, pemfaktoran, teorema sisa), fungsi mutlak, fungsi akar |

Sudah ditambahkan: 21 unit, termasuk konsep baru Polinomial. Matematika sekarang 47 konsep dan 274 unit.

### Level unit yang perlu dikoreksi

Kolom `level` di registry masih draf, contohnya:
- bilangan bulat tercatat Level 6, padahal CP-nya Fase D;
- program linear tercatat Level 14, padahal masuk TKA SMA wajib;
- bunga tunggal dan majemuk tercatat Level 14, padahal masuk CP Fase F dan TKA SMA.

Kolom `level` sekarang dikosongkan, karena kanonik tidak memuat kelas. Penempatan level dan kelas pindah ke berkas jalur (`jalur/matematika-berurutan.json`, `jalur/matematika-kurikulum-indonesia.json`). Penempatan di Kurikulum Indonesia masih turunan dari level lama, kecuali bilangan bulat yang sudah dipindah ke Fase D. Pemeriksaan per unit terhadap CP masih perlu dilakukan.

### Dua lapis produksi

| Lapis | Isi | Unit | Perkiraan deck |
|---|---|---|---|
| Sekolah | Semua yang dipakai Kurikulum Indonesia, TKA, dan SNBT | sekitar 190 (termasuk 25 tambalan) | sekitar 250 deck, ±3.500 kartu |
| Lanjut | Kalkulus lanjut, aljabar linear, analisis, teori bilangan aljabar, dan seterusnya | sekitar 85 | menyusul |

Urutan produksi lapis sekolah mengikuti strand dan prasyarat:
1. Bilangan: cacah, bulat (sudah), faktor, pecahan, desimal-persen-rasio, real.
2. Aljabar.
3. Geometri dan Pengukuran.
4. Data dan Peluang.
5. Trigonometri, Kalkulus dasar, dan Pemodelan.

## Bahasa Inggris

### Tiga sumber yang bertabrakan

| Sumber | Isi | Kekuatan | Kelemahan |
|---|---|---|---|
| Game Kampung Bahasa (`game/src/game/content/en`) | 7 level Basic–C2, 164 konsep grammar, sekitar 10.000 kata berlevel, 81 bab bertema, 455 situasi, bacaan, dialog, tugas menulis, 17.840 rekaman audio | Lengkap empat keterampilan, berlevel CEFR, sudah dimainkan, ada audio | Disusun per bab cerita. Belum ada pembagian jenis teks seperti CP dan TKA |
| Registry `canon_units` (203 unit) dan `POHON_HIERARKI_INGGRIS_V1.md` | Turunan otomatis dari topik perpustakaan lama | Sudah punya ID, label ujian, dan sambungan ke bank soal lama | 64% grammar, reading 8 unit, listening 7, status usulan dan belum ditinjau |
| Kartu Part of Speech (ADR-0025) | Kumpulan Noun, 10 deck | Rapi per kelas kata, standar istilah akademik | Baru satu dari sepuluh kumpulan |

### Keputusan

1. **Tulang punggung grammar** adalah kartu Part of Speech, Tenses, dan Modal.
2. **Keterampilan dan isi diambil dari game:** contoh, audio, kosakata, situasi, bacaan, dan dialog. Ke-164 konsep grammar game masing-masing masuk ke tepat satu unit kanonik (`game=` di `bahasa_inggris.py`, diperiksa otomatis).
3. **Registry lama (203 unit) dan `POHON_HIERARKI_INGGRIS_V1.md` tidak dipakai lagi.** Isinya sudah dihapus dari database dev.

### Strand

| Strand | Unit |
|---|---|
| Sounds and Spelling | 11 |
| Parts of Speech | 51 |
| Tenses | 18 |
| Modal Verbs in Use | 7 |
| Sentence Grammar | 35 |
| Vocabulary | 36 |
| Speaking and Interaction | 19 |
| Reading (keterampilan dan jenis teks) | 21 |
| Listening | 9 |
| Writing | 20 |

Per level: Pre-A1 13, A1 51, A2 61, B1 50, B2 34, C1 15, C2 3. Level C1–C2 masih tipis, karena sebagian isinya berupa keterampilan lanjut, bukan unit grammar.

### Aturan supaya tidak dobel

- **Kelas kata adalah rumah topik bentuk kata:** plural, countable, possessive, pronoun, article, comparative, adverb -ly. Konsep game yang sama dipetakan ke sana.
- **Tata bahasa dalam pemakaian adalah rumah topik kalimat:** tenses, passive, conditional, reported speech, relative clause.
- Satu tabel pemetaan menyimpan konsep game, unit kanonik, dan unit registry lama.

### Kartu Bahasa Inggris (selesai di dev, 2026-11-02)

Ditulis langsung di sesi (pilihan a), tanpa biaya AI. Satu unit, satu deck: 227 deck, 2.555 kartu, 1.144 soal (pilihan 491, menyimak 184, perbaiki 130, isian 118, pasangkan 101, kelompokkan 66, susun 40, ketuk kata 14). Semuanya berjenis materi.

| Strand | Berkas di `titian-web/src/content/kartu` | Asal isi |
|---|---|---|
| Sounds and Spelling | `en/sounds.ts` | Ditulis tangan, menyimak memakai rekaman kata dari game |
| Parts of Speech, Tenses, Modal, Sentence Grammar | `noun.ts`, `en/pronoun.ts` … `en/sentences-b.ts` | Ditulis tangan |
| Vocabulary (tema) | `en/vocabulary.ts` dari `scripts/vocab-decks.py` | Kosakata dan kalimat rekaman game |
| Vocabulary (cara kerja kata) | `en/vocabulary-words.ts` | Ditulis tangan |
| Speaking and Interaction | `en/speaking.ts` dari `scripts/speaking-decks.py` | Situasi game, pengantar ditulis di generator |
| Reading | `en/reading.ts` dari `scripts/reading-decks.py` | Bacaan dan soal game, catatan jenis teks ditulis di generator |
| Listening | `en/listening.ts` dari `scripts/listening-decks.py` | Dialog dan pengumuman game (kartu audio baru), strategi ditulis di generator |
| Writing | `en/writing.ts` dari `scripts/writing-decks.py` | Dasar menulis ditulis tangan; jenis teks memakai contoh dan tugas menulis game |

Berkas hasil generator jangan disunting langsung; ubah generatornya. Semua deck lolos pemeriksaan struktur (`check-en.ts`): jawaban, duplikat, dan setiap soal menyimak punya rekaman.

Yang masih kurang:

- Contoh tulisan, kalimat contoh Writing, dan sebagian kalimat grammar belum punya rekaman. Tombol putarnya memakai suara browser. Merekamnya butuh biaya TTS.
- Menulis bebas pada kartu *Giliranmu* belum dinilai. Penilaiannya butuh AI.

## Kartu Matematika (selesai di dev, 2026-11-02)

Ditulis langsung di sesi, tanpa biaya AI. 277 deck, 2.745 kartu, 1.328 soal, satu deck untuk tiap unit dari 274 unit, ditambah cek awal dan deck tambahan Bilangan Bulat. Berkasnya di `titian-web/src/content/kartu/mtk/` dan `bilangan-bulat.ts`.

| Kelompok | Berkas | Kedalaman |
|---|---|---|
| Bilangan cacah, faktor, pecahan, desimal, pangkat | `bilangan-cacah.ts`, `faktor-pecahan.ts`, `desimal-eksponen.ts` | Deck sekolah penuh |
| Aljabar, fungsi, kompleks, matriks | `aljabar-linear.ts`, `aljabar-fungsi.ts`, `aljabar-lanjut.ts` | Deck sekolah penuh |
| Geometri, trigonometri | `geometri-dasar.ts`, `geometri-analitik.ts` | Deck sekolah penuh |
| Data, peluang, statistika | `data-peluang.ts` | Deck sekolah penuh |
| Kalkulus, logika, numerasi, program linear, bunga | `kalkulus-logika.ts` | Deck sekolah penuh |
| 70 unit tingkat kuliah | `kuliah-analisis.ts`, `kuliah-diskrit.ts`, `kuliah-terapan.ts` | Deck ringkas, 6 sampai 8 kartu |

Unit tingkat kuliah hanya masuk jalur Matematika Berurutan, bukan jalur Kurikulum Indonesia, TKA, atau SNBT.

Perbaikan jalur saat menulis: CP 046/2025 Matematika Tingkat Lanjut Fase F mewajibkan turunan dan integral, sedangkan jalur Kurikulum Indonesia hanya memuat limit. Delapan unit turunan dan integral ditambahkan ke Fase F · Kelas 12. Kisi-kisi TKA Matematika Lanjutan memang hanya limit, tanpa L'Hôpital, jadi jalur TKA tidak diubah.

Yang masih kurang:

- Hitungan bilangan diperiksa otomatis (`check-math-answers.ts`), tetapi jawaban aljabar, geometri, dan soal cerita hanya diperiksa manual.
- Deck geometri belum punya gambar bangun. Kartu perlu model gambar supaya segitiga, jaring-jaring, dan grafik tampil.
- Penempatan unit per kelas di jalur Kurikulum Indonesia masih turunan dari level lama dan belum sesuai CP. Contohnya, Teorema Pythagoras masih di Fase B · Kelas 3.

## Yang perlu diputuskan

1. **Fitur lama di luar kanonik:** pohon perpustakaan (`modules` dan `module_items`) beserta halaman `/belajar`, `/jalur`, dan `/katalog` masih ada. Perlu diputuskan apakah ikut dipensiunkan saat kanonik baru siap.
