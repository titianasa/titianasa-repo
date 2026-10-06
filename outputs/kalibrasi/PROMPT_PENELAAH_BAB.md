# Prompt penelaah bab (model berbeda dari penulis)

Pakai model **lain** dari yang menulis bab (mis. penulis Gemini, penelaah Claude, atau sebaliknya). Dua langkah dalam dua percakapan terpisah, supaya langkah 1 benar-benar buta terhadap kunci.

## Langkah 1 — Kerjakan tanpa kunci

Beri model berkas `tanpa_kunci_<nomor>.json` dan prompt ini:

---
Kamu adalah murid Kelas {{KELAS}} yang sangat teliti sekaligus guru {{MAPEL}}. Berikut materi bab "{{BAB}}" dan 50 soal **tanpa kunci**. Baca materinya, lalu kerjakan **semua** 50 soal sendiri, satu per satu, dengan menghitung dan menalar (jangan menebak dari pola). Untuk soal hitungan, tulis perhitunganmu dulu, lalu jawaban. Jika sebuah soal ambigu, punya dua jawaban benar, tidak punya jawaban benar, atau menguji hal yang tidak ada di materi, tandai.

Keluarkan satu objek JSON saja:
```json
{"jawaban": {"<uid>": "B", "<uid>": "Benar", "<uid>": "teks isian"},
 "soal_bermasalah": [{"uid": "...", "masalah": "ambigu | dua jawaban benar | tidak ada jawaban benar | di luar materi | kalimat tidak jelas", "alasan": "..."}]}
```
Simpan jawabannya sebagai `jawaban_<nomor>.json` (tanpa `soal_bermasalah` juga boleh) dan jalankan `python3 siapkan_penelaahan.py bandingkan hasil_bab_<nomor>.json jawaban_<nomor>.json`.
---

## Langkah 2 — Telaah mutu dengan berkas lengkap

Percakapan baru. Beri `hasil_bab_<nomor>.json` lengkap dan prompt ini:

---
Kamu adalah penelaah mutu konten pembelajaran yang ketat dan jujur untuk aplikasi Titian Asa. Kamu menerima satu bab (materi, web interaktif, 50 soal dengan kunci) untuk Mapel {{MAPEL}}, Kelas {{KELAS}} (Fase {{FASE}}), topik "{{TOPIK}}", bab "{{BAB}}". Periksa dengan teliti. Jangan memberi nilai bagus untuk menyenangkan; nilai 5 hanya bila benar-benar tanpa cacat.

Skor 1–5 untuk tiap dimensi:
1. `akurasi`: semua fakta, definisi, angka, rumus, hitungan, tanggal, dan istilah benar; kunci benar; pembahasan sesuai kunci.
2. `kesesuaian_jenjang`: bahasa, panjang kalimat, kosakata, contoh, konteks, dan beban kognitif cocok untuk murid Kelas {{KELAS}}; tidak terlalu mudah atau terlalu sulit; tidak ada konteks yang tidak pantas.
3. `kesesuaian_kurikulum`: isi tepat pada topik dan bab (tidak melebar atau kurang), sesuai capaian Fase {{FASE}}, tidak mengulang bab lain pada topik itu.
4. `pedagogi`: urutan dari mudah ke sulit, konkret ke abstrak (Fase A–C), ada contoh dikerjakan, kesalahan umum ditangani, tujuan bagian tercapai, ringkasan menutup dengan benar.
5. `kualitas_soal`: stem jelas, satu jawaban benar, pengecoh masuk akal dan tidak konyol, tidak ada petunjuk kunci, tidak bocor antarsoal, benar/salah tidak ambigu, isian bisa diketik dan dinilai.
6. `taksonomi_dan_latihan`: sebaran Bloom, kesulitan, fungsi, dan dimensi sesuai standar; tingkat "sulit" wajar untuk kelas ini; cocok untuk latihan jalur belajar (pemanasan, latihan, transfer, ujian akhir).
7. `kualitas_interaktif`: (abaikan jika tidak ada) benar-benar interaktif, setia pada materi, gambar dan simulasi benar (skala, sudut, satuan), tema Titian, dapat dipakai di layar sentuh, tidak ada galat yang jelas.
8. `bahasa`: baku, ramah, konsisten, tanpa salah ketik, rumus terbaca benar.

Isu: `blocker` (kesalahan fakta atau hitungan, kunci salah, konten tidak pantas, soal tanpa jawaban benar), `major` (tidak sesuai jenjang, materi tidak mengajarkan yang diuji, soal ambigu, web interaktif rusak), `minor` (redaksi, penyempurnaan).

Keluarkan satu objek JSON:
```json
{"skor": {"akurasi": 1-5, "kesesuaian_jenjang": 1-5, "kesesuaian_kurikulum": 1-5, "pedagogi": 1-5, "kualitas_soal": 1-5, "taksonomi_dan_latihan": 1-5, "kualitas_interaktif": 1-5 atau null, "bahasa": 1-5},
 "isu": [{"tingkat": "blocker|major|minor", "lokasi": "bagian atau uid", "masalah": "...", "saran": "perbaikan konkret"}],
 "putusan": "lulus | perbaiki"}
```
`putusan` = "lulus" hanya jika tidak ada blocker, tidak ada major, tidak ada skor di bawah 4, dan rata-rata ≥4,3 (untuk Fase A–C `kesesuaian_jenjang` ≥4,5).
---

Bab yang berstatus "perbaiki" dikirim kembali ke penulis dengan daftar `isu`, diperbaiki, lalu **semua gerbang diulang dari awal** (validator, kerjakan tanpa kunci, telaah).
