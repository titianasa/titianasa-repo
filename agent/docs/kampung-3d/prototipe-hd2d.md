# Prototipe Pixel 3D di /play-art

Pemilik, 2026-10-21: game pixel dipertahankan, tapi harus terasa 3D ("masih 1 sisi 2D, aku ingin seperti 3D"). Prototipe pertama (sprite gambar ulang, 2026-10-20) diganti: sekarang memakai seni pixel game yang sudah ada.

- Halaman: `/play-art` (`game/src/app/(game)/play-art/`), kode di `game/src/game-art/pixel3d.ts` dan `ArtGame.tsx`. Tidak diindeks; game `/play` dan `/play-pixel` tidak berubah oleh halaman ini.
- Cara: peta asli (`buildZone`) dan gambar asli (`renderWorld`: tanah, bangunan, pohon, papan; `characterSprite`: orang) menjadi tekstur di adegan three.js.
  - Rumah biasa jadi balok: fasad di depan, potongan fasad di samping dan belakang, atap pelana dari gambar atapnya. Bangunan berbentuk khusus (masjid, menara, kios, tenda) dan semua benda lain berdiri sebagai kartu yang menghadap kamera.
  - Kamera miring dan bisa diputar (Q/E, seret, tombol putar), zoom dengan scroll. WASD mengikuti arah kamera.
  - Dirender pada tinggi internal rendah (240–400 px) lalu diperbesar tanpa penghalusan.
  - Semua kartu satu atlas dan satu draw call; semua rumah satu mesh. Hasil: 5 draw call, 58–60 fps di Intel HD 4000.
- Belum: papan iklan (di game pixel digambar di lapisan overlay, di sini hitam), NPC hanya berdiri, tanpa pemain lain, misi, chat, bayangan, malam dengan lampu. Bentuk khusus masih kartu datar.
