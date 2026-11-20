# ADR-0029: Gambaran bab dan sub-bab

Status: Dirancang dan dipilot di dev (2026-11-19), permintaan pemilik. Melanjutkan ADR-0026 dan ADR-0028.

## Masalah

Siswa membuka bab tanpa tahu apa yang akan dipelajari, untuk apa, dan bagaimana bab itu tersambung dengan pelajaran sebelum dan sesudahnya. Target modul bukan hanya paham, tetapi juga bisa menerapkan, dan menaikkan skor literasi dan numerasi PISA.

## Keputusan

Gambaran punya dua lapis.

1. **Gambaran kanonik.** Ditulis sekali per bab (konsep kanonik) dan per sub-bab (unit). Berlaku di semua jalur.
2. **Bingkai jalur.** Dihitung dari susunan tiap jalur, tanpa ditulis. Satu bab bisa terpecah ke beberapa kelas atau level, jadi tiap jalur menampilkan bagian bab yang ada di kelas itu, kelas sebelumnya yang sudah membahas bab ini, dan kelas sesudahnya yang melanjutkannya.

### Ditulis per jenjang

Keputusan pemilik: gaya bahasa, contoh, dan kedalaman mengikuti pembaca di tiap kelas atau jalur. Bab ditulis satu versi per jenjang tempat bab itu diajarkan: `sd-awal` (Kelas 1–2, Level 1), `sd` (Kelas 3–6, Level 2–3, TKA SD), `smp` (Kelas 7–9, Level 4–6, TKA SMP), `sma` (Kelas 10–12, Level 7–11, TKA SMA, UTBK), dan `pt` (Level 12–14). Matematika butuh 82 versi bab untuk 47 bab. Sub-bab ditulis untuk jenjang levelnya. Aplikasi memilih versi dari kelas atau level yang dibuka (`jenjangOf`), atau versi terdekat. Panduan gaya ada di `agent/docs/puzzle-pengetahuan/brief-penulis-gambaran.md`.

### Isi gambaran bab

| Bagian | Isi | Alasan |
|---|---|---|
| Ringkas | "Di bab ini kamu …", dua sampai tiga kalimat | Selalu tampil |
| Pertanyaan bab | Satu pertanyaan nyata yang bisa dijawab setelah bab ini | Memberi alasan belajar sejak awal |
| Kenapa perlu dipelajari | Apa yang bisa dilakukan setelahnya | |
| Sebelum dan sesudah di jalur ini | Dihitung dari jalur | Kaitan dengan pelajaran sebelum dan sesudahnya |
| Posisi di Matematika | Ide besar tempat bab ini berada dan ke mana ia tumbuh, dengan kategori konten PISA (kuantitas, perubahan dan hubungan, ruang dan bentuk, ketidakpastian dan data) | |
| Di dunia nyata | Tiga sampai empat penerapan dari konteks PISA yang berbeda: sehari-hari, pekerjaan, masyarakat, sains | Penerapan |
| Dipakai juga di | Dua sampai tiga bidang ilmu lain | Kaitan lintas bidang |
| Istilah | Kata yang harus dibaca dengan tepat di soal | Literasi membaca soal |
| Tantangan | Satu unit bergaya PISA: situasi dengan data, lalu tiga pertanyaan yang meminta merumuskan, menghitung, dan mengartikan hasil, dengan pembahasan yang dibuka sendiri | Numerasi PISA |

### Isi gambaran sub-bab

Ringkas, kenapa, dan satu contoh nyata ditulis. Bekal (topik prasyarat) dan "membuka jalan ke" (topik yang memakainya) dihitung dari graf prasyarat kanonik, termasuk lintas bab.

## Teknis

- Sumber: `titian-web/scripts/gambaran/<mapel>/<kode-bab>.ts` (tipe di `scripts/gambaran/tipe.ts`).
- `bun scripts/gambaran.ts` memeriksa kelengkapan dan menulis `public/gambaran/<mapel>/<kode-bab>.json`, ditambah bekal dan tautan dari `titian-backend-go/data/kanonik/<mapel>.json`. `GAMBARAN_CEK=1` hanya memeriksa.
- Pemeriksaan: semua bagian bab terisi, minimal 3 penerapan dari 3 konteks berbeda, minimal 2 bidang dan 3 istilah, tantangan memuat tiga proses, dan setiap unit bab punya gambaran sub-bab.
- Beranda (`belajar/gambaran.tsx`) memuat file satu bab saat bab itu dibuka. Ringkasan selalu tampil. Bagian lain ada di balik "Gambaran bab ini". Gambaran sub-bab dibuka dari judul topik.
- File statis, jadi tidak perlu deploy backend.

## Pilot dan sisa pekerjaan

- Pilot: `number.real_exponents_roots`, versi SMP dan SMA, dengan 7 sub-bab.
- Sisa Matematika: 80 versi bab untuk 46 bab, dan 307 sub-bab. Bahasa Inggris memakai format yang sama nanti.
- Jalur ujian (TKA, UTBK) bisa mendapat catatan khusus per bab (yang sering diuji, bentuk soalnya) sebagai lapis ketiga.
