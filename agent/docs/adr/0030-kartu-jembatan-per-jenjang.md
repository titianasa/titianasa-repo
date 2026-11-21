# ADR-0030: Kartu jembatan per jenjang

Status: diterima (pemilik, 2026-11-19)

## Masalah
Audit misi dan gambaran menemukan deck kanonik yang lebih dalam daripada level tempat sebuah jalur mengajarkannya. Contohnya `ukur-jam` di Level 1 yang memuat zona waktu, dan `fungsi-domain-range` di Level 5 yang memuat notasi interval. Sebaliknya, deck perguruan tinggi masih bergaya sekolah. Daftar lengkapnya ada di `agent/docs/puzzle-pengetahuan/temuan-misi.md`.

## Keputusan
- **Materi kanonik tidak diubah.** Deck kanonik tetap mengikuti standar ilmunya dan menjadi bacaan lengkap (ADR-0026). Kesalahan fakta atau kesalahan kartu tetap diperbaiki di deck kanonik.
- **Kartu jembatan per jenjang.** Kalau deck kanonik tidak cocok dengan level, kelas, atau jalur tempat unitnya diajarkan, ditambahkan deck jembatan (`kind: "kemasan"`). Deck ini menyampaikan unit yang sama dengan kedalaman, bahasa, dan contoh jenjang itu. Untuk perguruan tinggi (Level 12–14), deck jembatan adalah versi akademik yang lengkap: unit itu ditulis ulang dalam bahasa Indonesia akademik baku dan sedalam perguruan tinggi. Misi Level 12–14 mengambil kartu dari versi itu. Deck kanonik yang sudah akademik tidak perlu dibuatkan versi baru.
- **Satu tulisan, banyak jalur.** Deck jembatan ditulis sekali di `titian-web/src/content/kartu/jembatan/<jenjang>.ts`. Lewat `untukJalur(deck, [jalur…])`, deck itu didaftarkan ke setiap jalur yang mengajarkan unitnya di jenjang yang sama. Satu salinan dibuat per jalur, karena satu deck milik satu jalur. Jalur pertama (biasanya `matematika-berurutan`) memakai slug asli `jb-<deck-kanonik>`, sedangkan jalur lain diberi akhiran (`-ki`, `-tka-sd`, …).
- **Misi tetap milik deck kanonik.** Bab misi boleh menyebut `kartu: "jb-…"`. Tema-temanya lalu mengambil kartu materi dari deck jembatan, dan pemeriksaan cakupan kartu berlaku pada deck jembatan itu. Misi tetap tercatat di deck kanonik, jadi muncul di semua jalur. Bacaan lanjut tetap deck kanonik.
- **Batas baca deck jembatan** ditentukan oleh jalurnya (`scripts/tingkat-kartu.ts`):
  - Berurutan Level 1 = k2
  - Level 2 = k34
  - Level 3 = k56
  - Level 4–6 = SMP
  - Level 7–11 = SMA
  - Level 12–14 = standar kanonik

- **Satu unit, beberapa jenjang dalam satu jalur:** lihat ADR-0032. Deck jembatan diberi `jenjang` (k34, k56, smp, sma), dan unit itu boleh punya set misi per jenjang di samping misi umum.

## Akibat
- Jumlah deck bertambah, tetapi deck kanonik tidak dikejar mengikuti setiap kurikulum.
- Gambaran bab memakai deck kanonik sebagai sumber fakta. Kedalamannya tetap mengikuti versi jenjang (ADR-0029).
