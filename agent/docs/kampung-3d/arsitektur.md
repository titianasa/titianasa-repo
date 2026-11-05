# Arsitektur Kampung Bahasa 3D (`/start`)

Bagaimana klien 3D dibangun di atas game yang sudah ada tanpa mengubah `/play`. Keputusan: [ADR-0023](../adr/0023-kampung-bahasa-3d.md). Rasa dan angka visual: [`panduan-gaya.md`](panduan-gaya.md).

## 1. Prinsip

1. **Satu dunia, dua mesin gambar.** Logika game sudah ada di `src/components/game/Game.tsx`:
   - pelajaran, misi, kehidupan, ekonomi, perjalanan, chat, panggilan, premium, tur, iklan, sinkron server.
   - Game.tsx memegang satu objek `Engine` (pixel, `src/game/engine/engine.ts`).

   `/start` **memakai Game.tsx yang sama** dengan mesin 3D yang memenuhi antarmuka yang sama. Jadi semua aturan, jendela, dan alur tidak disalin dan tidak bercabang.
2. **`/play` tidak boleh berubah perilakunya.** Perubahan di Game.tsx hanya:
   - prop pemilih mesin (bawaan: pixel);
   - jalan keluar kecil (`if (engine.kind === "3d")`) untuk hal yang memang beda, misalnya tombol kamera.

   Setiap tiket yang menyentuh Game.tsx harus menjalankan ulang alur `/play` (§7).
3. **Peta pixel adalah denah peta 3D.** Mesin 3D memanggil `buildZone(id)` yang sama (`src/game/world/zones.ts`) dan mengubah `WorldMap` menjadi adegan 3D. Tidak ada peta 3D yang diketik ulang dengan tangan.
4. **Server tidak tahu klien.** Posisi, gerak, aksi, dan pesan memakai protokol yang sama (`src/game/protocol.ts`).

## 2. Susunan kode

```
alr/game/src/
├── app/(game)/start/          layout.tsx (huruf Fredoka/Nunito, viewport tanpa zoom, noindex sampai rilis)
│                              page.tsx   (cek maintenance seperti /play, lalu <Start3DLoader/>)
├── app/(game)/3d-concepts/    acuan beku: JANGAN diubah (ADR-0023 §1.4)
├── components/concepts3d/     acuan beku: kode yang menjadi sumber salinan
├── components/game/           UI bersama (Game.tsx, LessonModal, MissionModal, ChatPanel, …)
│   └── Start3DLoader.tsx      dynamic import Game dengan engine="3d", ssr: false
└── game3d/                    MESIN 3D (baru, salinan dari concepts3d lalu dikembangkan)
    ├── catalog.ts             gaya, slot, barang (data katalog pindah ke server di P10-008)
    ├── textures.ts            sama persis dengan acuan
    ├── merge.ts               sama persis dengan acuan
    ├── avatar.ts              rig, pakaian, pose, tangan, barang dipegang (dari acuan)
    ├── look.ts                look3d ⇄ look pixel (fromPixelLook, toPixelLook)
    ├── scene.ts               renderer, langit, cahaya, waktu, tingkat grafik (dari world.ts acuan)
    ├── kit/                   arketipe bangunan & properti: shop.ts, house.ts, camp.ts, food.ts,
    │                          gate.ts, landmark/*.ts, street.ts (tiang listrik, pagar), nature.ts
    ├── zone.ts                buildZone3D(map: WorldMap): tanah, bangunan, objek, dekor, collider
    ├── people.ts              pemain sendiri, pemain lain (interpolasi), warga, kerumunan
    ├── camera.ts              orang ke-1/2/3, Lemari, zoom, seret
    ├── input.ts               keyboard, joystick, sentuh
    ├── interact.ts            aksi kontekstual → Interaction milik Game.tsx atau aksi tampilan
    ├── bubbles.ts             balon percakapan & label (HTML di atas kanvas)
    ├── engine3d.ts            Engine3D: mesin konsep yang dibekukan (acuan QA, tidak dipakai game)
    └── start/                 MESIN GAME: engine.ts (class Start3D implements GameEngine), zone.ts, look.ts
```

**Aturan salinan:**
- `textures.ts`, `merge.ts`, dan isi `avatar.ts` disalin **apa adanya** dari `components/concepts3d/`.
- Isi `world.ts` dan `engine.ts` dipecah ke berkas di atas **tanpa mengubah angka**. Setiap angka yang dipindah tetap sama dengan panduan gaya.

## 3. Antarmuka mesin bersama

Langkah pertama (P10-002):
1. Tulis `src/game/engine/types.ts` berisi `interface GameEngine`. Isinya **semua** method, getter, dan properti `Engine` pixel yang dipakai di luar `engine.ts`. Cari dengan `grep` di `src/components` dan `src/game`.
2. Engine pixel menyatakan `implements GameEngine` tanpa perubahan perilaku.
3. Game.tsx menyimpan `GameEngine`, bukan `Engine`.

Yang sekarang dipakai Game.tsx (diperiksa 2026-10-13; pastikan ulang saat mengerjakan):

| Kelompok | Anggota |
|---|---|
| Hidup-mati | `constructor(canvas, overlay, callbacks, …)`, `start()`, `destroy()`, `paused`, `typing` |
| Zona & tujuan | `loadZone(id, at)`, `setGoalTile`, `setGoalZone`, `setExtraNpcs`, `setCompanion` |
| Pemain | `player`, `setLook`, `playerAvatar`, `playerTitle`, `sayBubble`, `interact()`, `virtualDir`, `riding` (definisi: `src/game/engine/types.ts`, P10-002) |
| Pemain lain | `remotes` (peta uid → posisi, look, nama) |
| Kendaraan | `train`, `boardTrain`, `requestAlight` |
| Kamera | `cameraModes`, `camera`, `setCamera`, `recenter`, `zoomBy`, `canZoomIn`, `canZoomOut`; mesin juga punya `kind` (`"pixel"` atau `"3d"`) |
| Dunia | `weather`, `clock`, `clockSkew`, `adFree` |
| Callback ke Game.tsx (`EngineCallbacks`) | `onInteract`, `onStep`, `onHotkey`, `npcHasTask`, `onPrompt`, `onZoom`, `onPan`, `onWarp`, `onRideZone`, `onAlight`, `onPlayerTap` |

**Engine3D** memenuhi antarmuka ini:
- **`onStep(x, y, dir)`:** dipanggil saat pemain masuk ubin baru (§5). Game.tsx tetap yang mengirim ke server.
- **`onInteract`:** dipanggil saat aksi utama di depan `MapObject`, warga, atau warp. `Interaction` sama dengan pixel; Game.tsx yang membuka jendelanya.
- **`onPrompt`:** dipanggil dengan teks aksi utama. Daftar aksi tambahan 3D (duduk, salaman, emote) ditampilkan oleh HUD 3D sendiri.
- **Kamera:** `camera` / `setCamera` memakai mode 3D (`"1" | "2" | "3"`). Tombol kamera di HUD menampilkan pilihan sesuai `engine.kind`.

## 4. Peta: `WorldMap` → adegan 3D (`zone.ts`)

**Skala:** `M = 2` (meter per ubin).
- Titik tengah ubin (x, y) ada di dunia `((x + 0.5)·M, 0, (y + 0.5)·M)`.
- **Utara peta = −z**, jadi "atas" peta pixel menjauh dari kamera awal.

**Ground** (`map.ground[y][x]`): bangun satu mesh per jenis tanah dari persegi-persegi ubin yang digabung, lalu `boxUV` per meter. Arti kodenya ada di komentar `Ground` di `map.ts`. Kode yang belum jelas maknanya: lihat cara `engine/terrain.ts` menggambarnya.

| Kode | Permukaan 3D |
|---|---|
| `g` | rumput |
| `f` | taman bunga (rumput + bunga instanced) |
| `p` | paving |
| `r` | aspal + marka |
| `w` | air (turun 0,25 m, tepi batu) |
| `d` | jembatan kayu |
| lainnya | ikuti `terrain.ts` |

**Feature** (`map.feature`):
- `T` pohon: pilih pohon peneduh, kelapa, atau pisang secara acak tetap per posisi.
- `F` pagar.
- `X` dekor padat.
- `B` adalah bagian bangunan, digambar oleh bangunan dan bukan per ubin.

**Bangunan** (`map.buildings`, lihat tipe `Building` di `map.ts`):
- Petak bangunan = kotak ubinnya × M. Pintu menghadap jalan masuk (ubin `door`).
- Arketipe dipilih dari `kind` dan `style`: `shop`, `house`, `camp`, `food`, `coffee`, `bike`, `library`, …
- Nama di papan memakai `label`; warna atap memakai `roofColor` dengan tekstur genteng atau seng menurut arketipe.
- Bangunan khusus (gerbang lima kampung, huruf bunga KAMPUNG BAHASA PARE, Candi Bahasa, Museum, masjid, gereja, klenteng, stasiun, terminal, Puskesmas, Balai Desa) punya model sendiri di `kit/landmark/`. Daftar lengkapnya ada di tiket P10-005.

**Objek** (`map.objects`, `MapObject`) adalah titik interaksi. Di 3D tiap objek mendapat:
- penanda fisik (pintu, papan, meja, kasur, halte, gerobak);
- jari-jari aksi 1,6 m.

Aksi utamanya memanggil `onInteract` persis seperti pixel.

**Warga** (`map.npcs`, `NpcSpawn`):
- Dibangun dengan `buildAvatar`. Penampilan diturunkan dari `look` pixel-nya lewat `fromPixelLook`, dengan gaya **Realis** untuk warga dewasa dan Kartun untuk anak.
- Ruang gerak warga (`wander`) dan dialognya sama dengan pixel.

**Collider:** ubin yang `isSolid(map, x, y)` menjadi kotak padat M × M. Bangunan menambah collider sesuai bentuk 3D-nya. Tabrakan memakai `blocked(x, z, r)` seperti acuan.

**Warp** (`map.warps`): saat pemain masuk ubin warp, panggil `onWarp` seperti pixel.

## 5. Posisi dan jaringan

**Pemain sendiri:**
- Bergerak mulus dalam meter.
- Setiap kali `floor(x / M), floor(z / M)` berubah, panggil `callbacks.onStep(tx, ty, dir)`. `dir` adalah arah hadap terdekat (`up`/`down`/`left`/`right`).
- Ubin yang dilaporkan **tidak boleh solid**. Bila ubin di bawah pemain solid karena collider 3D lebih kecil dari ubin, laporkan ubin terakhir yang tidak solid.

**Pemain lain** (`remotes`, pesan `moves`): posisi ubin dijadikan titik tujuan di tengah ubin, lalu didekati dengan `lerp` pada kecepatan jalan 3D. Arah hadap dari `dir`.

**Look pemain lain:**
- `look3d` dari server bila ada.
- Bila tidak ada, `fromPixelLook(look)`, dengan gaya Kartun dan kartu peserta di level bahasa fokusnya.

**Kerumunan dummy** dari server tampil seperti pemain lain. **Tidak ada aksi sosial untuk mereka** (ADR-0023 §7.3). Kenali dari data pemain yang dikirim hub; bila belum ada penanda, tambahkan flag `dummy` di snapshot hub (P10-006).

**Pemain komputer tur (Nadia, `BUDDY_ID`) dan warga** boleh membalas gerakan dan berbicara. Kalimatnya dari data yang sama dengan pixel (`src/game/tour.ts`, dialog warga).

## 6. Data baru di server (P10-008)

| Apa | Bentuk |
|---|---|
| `pare_players.look3d` | `jsonb null` dengan isi persis `Look` di `game3d/catalog.ts` (gaya, kulit, tinggi, badan, bahu, mata, rambut + warna, penutup kepala + warna, atasan + warna, terusan + warna, bawahan + warna, alas kaki + warna, tas + warna, aksesori[]) |
| `pare_wardrobe` | `(user_id, item_id, acquired_at, source)`; `source` ∈ `gratis \| koin \| plus \| pro \| toko` |
| Katalog | `data/pare/content.json` → `wardrobe: [{ id, slot, name, tier, price, lokal, … }]`, diekspor dari `game3d/catalog.ts` dengan skrip (seperti `scripts/missions.ts --write`) |
| Endpoint | `GET /pare/wardrobe`, `POST /pare/wardrobe/buy {item}` (uang game atau toko lewat `PaymentProvider`), `PUT /pare/me/look3d` (server menolak barang yang tidak dimiliki kecuali gratis, atau Plus/Pro yang aktif) |
| Hub | snapshot dan `join` membawa `look3d` dan flag `dummy` |

Tulis semuanya di `api-contract.md` dan `domain-model.md`. Barang langganan tidak dimasukkan ke `pare_wardrobe`; aksesnya dihitung dari status Plus/Pro.

## 7. Pengujian

1. **`/play` tetap sama.** Setelah tiket yang menyentuh `src/components/game`, `src/game`, atau `src/lib`:
   - jalankan `bun scripts/e2e/splash.ts` dan alur tur pertama;
   - lakukan satu pelajaran dan satu interaksi warung di `/play`.

   Cara kerjanya ada di skrip `scripts/e2e/` dan `scripts/video/rec.ts`.
2. **`/start` sama dengan acuan.** Jalankan `bun scripts/qa/3d.ts --url /start`, lalu bandingkan dengan `kampung-3d/golden/` sesuai [`qa.md`](qa.md).
3. **Anggaran kinerja:** catat `renderer.info` di tiket (ADR-0023 §8).
4. **Uji jaringan:**
   - Buka `/play` dan `/start` bersamaan dengan dua akun uji. Minta izin user dulu. Token uji dibuat seperti `freshToken` di `scripts/e2e/lib.ts`, browser dikendalikan dengan `Bun.WebView` (`agent/tools/qa/webview.ts`), dan akun uji dihapus setelahnya.
   - Pastikan keduanya saling terlihat, bergerak, dan chat.
