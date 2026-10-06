# Standar Gate Bagian V1

Berlaku untuk semua modul kanonik (Matematika, Inggris, dan domain berikutnya), lama maupun baru.

## Aturan

1. **Setiap Bagian modul diakhiri gate.** Pembelajar membaca Bagian, menjawab tarikan soal gate, dan baru boleh membuka Bagian berikutnya. Bagian berurutan ketat: hanya Bagian pertama yang belum lulus yang bisa dijawab, sisanya "terkunci".
2. **Gate bukan produksi AI terpisah.** Soal gate diambil dari **bank 50 soal modul itu sendiri**, dengan `uid` yang sama, diutamakan soal `latihan_terarah` Bagian itu, lalu ditandai `checkpoint_bagian`. Satu item tetap satu bukti penguasaan, tidak menjadi soal baru di bank lain (sesuai `STANDAR_BLUEPRINT_MODUL`, bagian bank kanonik). Biaya token tambahan: nol.
3. **Ukuran.** Pool gate = 4 soal pilihan ganda jawaban tunggal per Bagian; satu tarikan = 2 soal (`CHECKPOINT_DRAW`). Minimum agar Bagian bergate = 2 soal; kurang dari itu Bagian dilaporkan *tanpa gate* (tidak digate dengan satu soal).
4. **Pemilihan.** Soal dicocokkan ke Bagian yang diujinya lewat kemiripan teks (bobot idf; judul Bagian berbobot 3x). Bila soal membawa `source_section_id` yang valid, tag itu dipakai. Dalam satu Bagian, tingkat Bloom yang berbeda didahulukan sebelum mengulang satu tingkat. Satu soal hanya melayani satu gate.
5. **Tidak menimpa.** Bagian yang sudah punya checkpoint tidak disentuh.
6. **Kelulusan artikel.** Artikel bergate memakai `guard_config = {"completion_rule": "required"}`: Latihan baru terbuka setelah semua gate lulus. Jawaban salah mengunci Bagian; pembelajar membaca ulang minimal 30 detik (15 detik per menit Bagian) sebelum tarikan baru, yang mengutamakan soal yang belum pernah dilihat.
7. **Pembelajar tidak pernah menerima kunci.** Penilaian di server.

## Penerapan

| Situasi | Cara |
|---|---|
| Modul baru | `generate_bab_lean` memanggil `gates::apply_gates` setelah bank terisi; tidak ada langkah manual. |
| Modul lama tanpa gate | `cargo run --bin backfill_section_gates` (dry run) lalu `-- --apply`. Aman diulang; hanya Bagian tanpa gate yang berubah; tanpa AI. |
| Artikel terbit | Tidak diedit di tempat (ADR-0008); dilaporkan, bukan dipaksa. |
| Bank belum terisi | Belum bisa bergate. Gate terpasang otomatis begitu bank digenerate lewat pipeline atau backfill dijalankan ulang. |

Kode: `titian-backend-rust/src/services/content_factory/gates.rs` (perencanaan murni + tes), pembaca gate: `services/section_checkpoint.rs`.

## Keadaan saat standar ditetapkan (2026-09-19, DB dev)

- 721 artikel bermateri; 592 sudah bergate dari pipeline lama.
- Backfill: 42 artikel diberi gate (152 Bagian), termasuk modul "Membulatkan bilangan sesuai ketelitian yang diminta".
- Hasil: 616 artikel bergate penuh, 18 sebagian, 87 tanpa gate. 83 dari 87 itu belum punya bank soal sama sekali.
- 47 Bagian pada artikel yang bank-nya ada tetap tanpa gate karena soal pilihan ganda yang relevan kurang dari 2.

## Celah yang diketahui

- Pencocokan soal ke Bagian berbasis kata, bukan makna; Bagian yang kosakatanya tumpang tindih bisa tertukar. Kualitas gate belum dinilai hakim.
- Bank lean menghasilkan sekitar separuh pilihan ganda; modul dengan bank kecil atau dominan isian tidak cukup untuk 4 soal per Bagian. Jalan keluar bila perlu: naikkan porsi pilihan ganda di campuran bank, bukan menurunkan minimum.
