# Jalur belajar Matematika berbasis kartu

Status: pilot Bilangan Bulat jalan di dev (2026-11-02). Keputusan dasarnya ADR-0025. Banyak jalur dengan satu catatan pengetahuan diputuskan di ADR-0026.

## Inti

Satu konsep cukup punya satu kumpulan kartu. Jalur seperti Kelas 7, TKA, dan remedial hanya mengatur urutan dan memilih kartu yang sama, tidak menyalin isinya. Kalau satu kartu diperbaiki, semua jalur ikut membaik.

## Susunan

| Tingkat | Contoh | Jumlah di pohon kanonik |
|---|---|---|
| Mata pelajaran | Matematika | 1 |
| Strand | Bilangan | 7 |
| Kumpulan (konsep) | Bilangan Bulat | 46 |
| Deck (unit belajar) | Menjumlahkan Beda Tanda | 253 |
| Bank soal | 50 soal per unit, untuk latihan dan ujian | 253 |

Kelas, fase, TKA, dan UTBK adalah label di atas unit, bukan cabang materi. Sumbernya `outputs/POHON_HIERARKI_MATEMATIKA_V1.md`.

## Perjalanan satu topik: pilot Bilangan Bulat

```text
Cek Awal (9 soal)
   │  soal pertama yang salah menentukan titik mulai
   ▼
1 Garis Bilangan → 2 Membandingkan → 3 Lawan & Nilai Mutlak
   → 4 Tambah Tanda Sama → 5 Tambah Beda Tanda → 6 Mengurangkan
   → 7 Mengalikan & Membagi → 8 Operasi Campuran → 9 Soal Cerita
   │
   ▼
Ujian topik dari bank soal → masuk ke ulangan berjarak → lanjut ke Faktor & Kelipatan
```

Rantai prasyarat sebelumnya: bilangan cacah → nilai tempat → operasi bilangan cacah → bilangan bulat. Rantai sesudahnya: persamaan linear → fungsi linear → fungsi kuadrat → limit.

## Perjalanan satu deck

| Langkah | Bentuk kartu | Contoh |
|---|---|---|
| Lihat | Ide, tabel, garis bilangan yang bergerak | Token melompat dari −3 ke 2 |
| Coba | Contoh langkah demi langkah, ketuk garis bilangan | −8 + 3 diuraikan satu per satu |
| Buktikan | Soal hitung di dalam kartu | −15 + 6 = ___ |
| Pakai | Soal konteks | Suhu, saldo, lift, skor |
| Waspada | Kartu kesalahan umum | −4 + 9 = −5 |
| Ingat | Kartu ringkasan, lalu diulang di hari lain | Mengikuti `metode-belajar.md` |

## Aturan lanjut

Mengikuti `mastery_rule` golden module.

| Hasil | Yang terjadi |
|---|---|
| Benar sekali coba ≥ 80% | Tombol langsung mengarah ke deck berikutnya |
| Di bawah 80% | Tombol "Ulangi dulu" disorot, deck berikutnya tetap bisa dibuka |
| Cek Awal ada yang salah | Mulai dari deck soal pertama yang salah |
| Salah dua soal bertanda berbeda | Diarahkan ke latihan visual tambahan (belum dibuat) |
| Benar lagi di hari berikutnya | Status jadi dikuasai |

Urutan bersifat anjuran, bukan kunci. Tapi sistem tidak boleh menyatakan seseorang menguasai suatu konsep kalau prasyaratnya belum terbukti.

## Satu kartu, banyak jalur

| Jalur | Peran kumpulan Bilangan Bulat | Tambahannya |
|---|---|---|
| Kurikulum Merdeka Kelas 7 | Inti, wajib berurutan | Mengikuti urutan sekolah |
| Remedial | Dibuka saat kesalahan tanda terdeteksi | Hanya deck yang lemah |
| TKA SMP | Fondasi, lalu deck 9 | Latihan bertimer dari bank soal |
| UTBK-SNBT | Fondasi pengetahuan kuantitatif | Cek Awal dulu, lewati yang sudah bisa |
| Cambridge Stage 7 | Inti | Istilah bahasa Inggris menyusul |

Pemetaan ke bab Kurikulum Merdeka Kelas 7 (topik "Bilangan Bulat dan Operasinya"):

| Bab | Deck |
|---|---|
| Mengenal Bilangan Bulat dan Garis Bilangan | 1, 2, 3 |
| Penjumlahan dan Pengurangan | 4, 5, 6 |
| Perkalian dan Pembagian | 7 |
| Operasi Hitung Campuran | 8 |
| Soal Cerita | 9 |
| Kesalahan Umum: Tanda Negatif Hilang | Ada di kartu kesalahan tiap deck, utamanya deck 6 |

## Urutan membangun Matematika

| Tahap | Kumpulan | Unit | Sasaran |
|---|---|---|---|
| Sudah | Bilangan Bulat | 8 + Soal Cerita + Cek Awal | Pilot |
| 1 | Sisa strand Bilangan kecuali Kompleks | 35 | Pondasi SD–SMP, TKA |
| 2 | Aljabar dan Fungsi | 54 | SMP–SMA, UTBK |
| 3 | Geometri dan Pengukuran | 40 | SD–SMA |
| 4 | Data, Peluang, dan Statistika | 25 | SD–SMA, UTBK |
| 5 | Kalkulus, Diskrit, Pemodelan, Bilangan Kompleks | 91 | SMA akhir–kuliah |

## Beda dengan bahasa Inggris

- Kartu Matematika punya garis bilangan interaktif dan contoh langkah demi langkah.
- Tanda minus memakai karakter − supaya terbaca. Mengetik `-` tetap diterima.
- Belum ada audio, karena narasi Indonesia masih menunggu TTS.
- Hitungan di kartu dicek otomatis sebelum terbit. Pilot ini: 122 hitungan.
- Istilah memakai bahasa Indonesia sekolah. Istilah akademik Inggris hanya untuk materi bahasa Inggris.

## Keputusan yang dibutuhkan

1. **Satuan deck** sudah diputuskan: per unit kanonik, lihat ADR-0026.
2. **Asal soal ujian topik.** Bank 50 soal Kelas 7 ini masih kosong, dan menghasilkannya memakai Gemini, jadi perlu persetujuan biaya.
3. **Kartu masuk jaringan pengetahuan** sudah dibuat: skor tersimpan di akun per unit. Yang tersisa menyatukannya dengan `masteries`, lihat ADR-0026.
