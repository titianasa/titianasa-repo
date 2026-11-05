# Kampung Bahasa 3D

Versi 3D Kampung Bahasa Pare di `pare.titianasa.com/start`, berdampingan dengan game pixel art di `/play`, yang tetap ada.

| Dokumen | Isi |
|---|---|
| [ADR-0023](../adr/0023-kampung-bahasa-3d.md) | keputusan: tempat, teknologi, arah seni, skala, monetisasi, interaksi, grafik, proses |
| [`panduan-gaya.md`](panduan-gaya.md) | kontrak visual: proporsi tiga gaya karakter, wajah, pakaian, material, tekstur, cahaya per waktu, tingkat grafik, kamera, kecepatan, UI |
| [`arsitektur.md`](arsitektur.md) | susunan kode `src/game3d/`, antarmuka `GameEngine`, peta pixel sebagai denah 3D, jaringan, data server baru |
| [`resep.md`](resep.md) | langkah baku: menambah pakaian, bangunan, warga, emote, interaksi, tingkat grafik |
| [`qa.md`](qa.md) | gambar acuan, cara membandingkan, anggaran kinerja, daftar periksa |
| [`golden/`](golden/) | tangkapan layar acuan dari `/3d-concepts` (2026-10-13) |
| [Tiket Pare-10](../tickets/pare-10-kampung-3d.md) | urutan pembangunan P10-001 … P10-010, mulai dari Kampung Bahasa |

## Status (2026-10-13)

- **Konsep disetujui** dan jalan di `alr/game` pada `/3d-concepts`. Ini **implementasi acuan yang dibekukan**: kodenya ada di `src/components/concepts3d/`, dan pengujinya di `scripts/qa/3d.ts`.
- **Isi konsep:**
  - tiga gaya karakter dan Lemari dengan pakaian lokal dan label harga;
  - kamera orang ke-1/2/3 dengan tangan orang pertama;
  - interaksi dengan warga, barang, dan bangunan; foto bareng;
  - emote;
  - empat tingkat grafik;
  - dunia realistis gaya The Sims di sekitar gedung kursus.
- **Belum ada kode `/start`.** Pembangunan dimulai dari P10-001.

## Cara kerja

1. **Opus** merencanakan dan meninjau. **Sonnet (effort medium)** membangun satu tiket per sesi, berurutan.
2. **Hasil harus sama dengan acuan.** Angka di panduan gaya adalah kontrak, dan tiap tiket membandingkan tangkapan layarnya dengan `golden/`.
3. **Bila ragu, berhenti dan tanya user**, bukan mengarang.
