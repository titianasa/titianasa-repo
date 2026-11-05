# Tiket Pare-10: Kampung Bahasa 3D di `/start`

📋 **RENCANA (2026-10-13)**: belum ada kode `/start`. Acuan yang sudah jalan: `/3d-concepts` (`alr/game/src/components/concepts3d/`).

- **Keputusan:** [ADR-0023](../adr/0023-kampung-bahasa-3d.md), Accepted.
- **Perencana dan peninjau:** Opus.
- **Pembangun:** **Sonnet, effort medium, satu tiket per sesi, berurutan.** Dokumen ini ditulis supaya bisa dikerjakan tanpa ikut merancangnya.

## Baca dulu, berurutan

1. [ADR-0023](../adr/0023-kampung-bahasa-3d.md): apa yang diputuskan dan apa yang dilarang.
2. [`kampung-3d/README.md`](../kampung-3d/README.md), lalu [`panduan-gaya.md`](../kampung-3d/panduan-gaya.md) (angka-angka kontrak), [`arsitektur.md`](../kampung-3d/arsitektur.md), [`resep.md`](../kampung-3d/resep.md), [`qa.md`](../kampung-3d/qa.md).
3. Kode acuan: `alr/game/src/components/concepts3d/` (`catalog.ts`, `textures.ts`, `world.ts`, `avatar.ts`, `merge.ts`, `engine.ts`, `Studio.tsx`, `studio.module.css`).

   Buka `/3d-concepts` di browser lokal (`http://localhost:4700/3d-concepts`) dan coba semuanya sebelum mulai.
4. Game pixel yang dibungkus: `src/components/game/Game.tsx`, `src/game/engine/engine.ts`, `src/game/world/map.ts`, `kota.ts`, `zones.ts`, `src/game/protocol.ts`, `src/game/net.ts`.

## Aturan main

- **`/play` tidak boleh berubah perilakunya.** Setiap perubahan di `src/components/game`, `src/game`, atau `src/lib` diuji ulang di `/play` (arsitektur §7).
- **`/3d-concepts` dan `src/components/concepts3d/` dibekukan.** Salin, jangan ubah.
- **Angka di panduan gaya adalah kontrak.** Jangan mengganti warna, proporsi, cahaya, kecepatan, atau kamera "supaya lebih bagus". Bila benar-benar perlu, tulis alasannya, perbarui panduan dan `golden/`, dan sebutkan di laporan.
- **Tidak ada pustaka baru**, file gambar atau model yang diunduh, atau versi three.js lain.
- **Akibat ekonomi dan progres selalu lewat server** dan alur Game.tsx yang ada.
- **Kerumunan dummy tidak pernah membalas** apa pun.
- **Tidak commit dan tidak deploy tanpa diminta.** User yang push (repo `titianasa/kampung-bahasa`).
- **Bila tiket butuh keputusan yang tidak ada di dokumen:** berhenti dan tanya user. Jangan menebak.
- **Di akhir sesi:** status tiket ini, `STATE.md`, dan hasil QA ditulis di bagian "Catatan" tiketnya.

---

## P10-001: Mesin 3D jadi pustaka `src/game3d/`

**Status:** ✅ selesai (2026-10-13, Sonnet 5.5) · **Repo:** `alr/game`

**Tujuan:** modul acuan tersedia sebagai pustaka yang bisa dipakai `/start`, dengan hasil gambar identik.

**Kerjakan:**
1. Salin `textures.ts`, `merge.ts`, `catalog.ts`, dan `avatar.ts` dari `src/components/concepts3d/` ke `src/game3d/` **tanpa perubahan isi**, kecuali path import.
2. Pecah `world.ts` acuan menjadi:
   - `game3d/scene.ts`: renderer, langit, cahaya, `setTime`, `setQuality`, `update` untuk matahari, awan, dan bayangan.
   - `game3d/kit/`: `building-course.ts` (gedung kursus acuan), `warung.ts`, `bike.ts`, `bench.ts`, `flag.ts`, `pond.ts`, `fence.ts`, `pole.ts`, `house.ts`, `nature.ts` (pohon peneduh, kelapa, pisang, gumpalan daun, rumput tinggi).

   Pembantu `block`, `rod`, `boxUV`, `faceUV`, `hipRoof`, dan `gableSlopes` masuk `game3d/kit/build.ts`.
3. Pecah `engine.ts` acuan menjadi `people.ts`, `camera.ts`, `input.ts`, `interact.ts`, `bubbles.ts`, dan `engine3d.ts` (sementara masih kelas mandiri seperti acuan).
4. Buat `game3d/demo.ts` yang menyusun halaman konsep dari pustaka baru: tata letak yang sama dengan `buildWorld` acuan.
5. Salin `Studio.tsx` dan `studio.module.css` acuan ke `src/game3d/ui/ConceptStudio.tsx` dan `src/game3d/ui/studio.module.css`, import diarahkan ke pustaka `game3d`. Tambahkan route sementara `src/app/(game)/3d-concepts/v2/` (layout seperti `3d-concepts/layout.tsx`, page dengan loader dinamis ke `ConceptStudio`). **Jangan** ubah `components/concepts3d`. `ConceptStudio` juga harus memasang `window.__kb3d` di development dengan anggota yang sama, supaya `scripts/qa/3d.ts` bisa menjalankannya.

**Selesai bila:**
- `bun scripts/qa/3d.ts --url /3d-concepts/v2` menghasilkan gambar yang sama dengan `golden/` untuk semua adegan.
- `--perf` memberi angka draw call dan segitiga dalam ±3% dari acuan.
- `tsc` dan `eslint` bersih.
- `git diff --stat src/components/concepts3d` kosong.

---

## P10-002: Antarmuka mesin bersama `GameEngine`

**Status:** ✅ selesai (2026-10-13, Sonnet 5.5) · **Repo:** `alr/game`

**Tujuan:** Game.tsx bisa memakai mesin pixel atau 3D.

**Kerjakan:**
1. Daftar semua anggota `Engine` (pixel) yang dipakai di luar `engine.ts`. Pakai `grep` di `src/components` dan `src/game`; titik awalnya tabel arsitektur §3.
2. Tulis `src/game/engine/types.ts` → `export interface GameEngine` beserta `EngineCallbacks` yang sudah ada, dan `kind: "pixel" | "3d"`.
3. `Engine` pixel `implements GameEngine`, `kind = "pixel"`. Tidak ada perubahan perilaku.
4. Game.tsx:
   - `useRef<GameEngine>`;
   - prop baru `engine?: "pixel" | "3d"` (bawaan `"pixel"`);
   - pembuatan mesin lewat pabrik `createEngine(kind, …)`.

   Untuk sementara `"3d"` melempar `Error("belum ada")`.
5. `CAMERA_MODES` dan tombol kamera di HUD dibaca dari mesinnya, misalnya `engine.cameraModes`.

**Selesai bila:**
- `/play` lolos uji ulang (arsitektur §7.1): splash, tur pertama, satu pelajaran, satu warung, chat.
- `tsc` dan `eslint` bersih.
- Diff Game.tsx kecil dan hanya mengganti tipe dan pembuatan mesin.

---

## P10-003: Route `/start` dan Engine3D berjalan di Kampung Bahasa (tanah saja)

**Status:** ✅ selesai (2026-10-13, Sonnet 5.5) · **Repo:** `alr/game`

**Tujuan:** pemain bisa login di `/start`, berjalan di Kampung Bahasa 3D, dan terlihat oleh pemain `/play`.

**Kerjakan:**
1. Route:
   - `src/app/(game)/start/layout.tsx`: salin dari `play/layout.tsx`, tambah huruf Fredoka dan Nunito seperti `3d-concepts/layout.tsx`, `robots: { index: false }` sampai rilis.
   - `page.tsx`: cek maintenance seperti `play/page.tsx`, lalu `Start3DLoader` (dynamic, `ssr: false`) yang merender `<Game engine="3d" />`.
2. `game3d/engine3d.ts`: `class Engine3D implements GameEngine`, `kind = "3d"`.
   - **`loadZone(id, at)`:** `buildZone(id)` → `zone.ts` (P10-004 mengisi tanahnya; di tiket ini cukup tanah rata per kode `ground` dengan warna sementara dan collider dari `isSolid`) + `scene.ts` (langit, cahaya, waktu dari jam game).
   - **Pemain:** `buildAvatar(fromPixelLook(look))`. Gerak dan kamera orang ke-3 dari acuan; joystick sentuh dan keyboard.
   - **`onStep`** setiap ganti ubin (arsitektur §5); **`onWarp`** di ubin warp.
   - **`remotes`:** pemain lain digambar dan diinterpolasi.
   - **`interact()`** dan `onPrompt`: aksi utama untuk `MapObject` di depan pemain (jari-jari 1,6 m) memanggil `onInteract` dengan `Interaction` yang sama seperti pixel.
3. `game3d/look.ts`: `fromPixelLook(look: pixel Look): Look3d` dan `toPixelLook`.
   - Pemetaan: `hairStyle` hijab/peci → `head`, `outfit` → `top`/`dress`, `acc` → `bag`/`acc`.
   - Selalu tambahkan `lanyard`. Tulis tabelnya di komentar.
4. HUD 3D di atas kanvas, dengan gaya stiker dari `studio.module.css`: joystick, tombol kamera 1/2/3, zoom, dan Grafik di menu pengaturan.

   HUD pixel yang sudah ada (`Hud.tsx`: nyawa, uang, jam, tombol BELAJAR/MISI/CHAT/AKU) tetap dipakai. Sesuaikan posisi bila bertabrakan.

**Selesai bila:**
- Login di `/start` lewat layar judul yang sama dengan `/play`.
- Muncul di Kampung Bahasa sesuai posisi tersimpan, bisa berjalan, dan pindah zona lewat warp (zona lain boleh tampil tanah rata dulu).
- Buka `/play` dengan akun kedua: keduanya saling terlihat bergerak, dan chat dua arah. Minta izin user sebelum membuat akun uji; hapus setelahnya.
- `/play` lolos uji ulang.

---

## P10-004: Tanah, alam, langit, dan grafik Kampung Bahasa

**Status:** ✅ selesai (2026-10-13, Sonnet 5.5); menunggu persetujuan user untuk tampilan hujan · **Repo:** `alr/game`

**Tujuan:** Kampung Bahasa terasa seperti acuan, kecuali bangunannya.

**Kerjakan:**
1. **`zone.ts` → tanah per kode:**
   - Tabel di arsitektur §4: rumput, taman bunga, paving, aspal dengan marka, sungai (air turun 0,25 m, tepi batu), jembatan kayu, dan kode lain sesuai `terrain.ts`.
   - Gabungkan per kawasan sekitar 40 × 40 m.
2. **Feature:**
   - `T` pohon: peneduh, kelapa, atau pisang, dipilih tetap per posisi.
   - `F` pagar: tembok rendah + jeruji besi seperti acuan.
   - `X` dekor sesuai `decor`: bangku, lampu, tiang listrik di sepanjang jalan utama dengan kabelnya, papan.
3. **`scene.ts`:**
   - Waktu mengikuti jam WIB game (`src/game/time.ts`); interpolasi Pagi → Siang → Senja → Malam (panduan §4).
   - **Cuaca:** hujan memakai partikel garis + langit lebih kelabu bila `weather` hujan. Tetap dalam gaya realistis; tidak ada di acuan, jadi kirim tangkapan layarnya ke user untuk persetujuan.
4. **Tingkat grafik** persis panduan §5, termasuk pemilihan awal otomatis (Hemat bila < 24 fps).
5. **Kabut dan jarak gambar:** kawasan di luar 150 m tidak digambar.

**Selesai bila:**
- QA `01-overview`, `15-senja`, dan `16-malam` sama kesannya dengan acuan.
- `--perf` di empat tingkat dalam anggaran.

---

## P10-005: Bangunan Kampung Bahasa

**Status:** ✅ selesai (2026-10-13, Sonnet 5.5); menunggu tinjauan user atas tangkapan layar bangunan · **Repo:** `alr/game` · **Boleh dipecah:** 005a arketipe umum, 005b landmark.

**Tujuan:** setiap bangunan di `buildZone("umum").buildings` berdiri di petaknya dalam gaya acuan.

**Daftar** (periksa ulang dengan `bun scripts/check-map.ts umum --ascii` dan `buildZone("umum").buildings`):

| Kelompok | Bangunan |
|---|---|
| Arketipe umum | Camp Putra, Camp Putri (rumah dua lantai bergaya kos), Sewa Sepeda ×2 (ruko dengan sepeda di depan), Warung Pecel, Warkop (warung acuan, varian kopi), Minimarket (ruko kaca), Perpustakaan, Puskesmas, Balai Desa, Speaking Club (tenda merah, `kind` sesuai peta), Language Challenge, Kantor Imigrasi, Bank Kampung, Sekolah Dasar, Kerja Paruh Waktu, kios pasar |
| Landmark | lima gerbang kampung (bentuk khas tiap negara: pagoda Mandarin, kubah Arab, gaya Inggris, torii Jepang, gerbang Korea), huruf bunga KAMPUNG BAHASA PARE, Candi Bahasa, Museum Bahasa, masjid, Gereja Protestan, Gereja Katolik, klenteng (bila ada), Terminal Bus, Stasiun Kereta, halte kereta kelinci, papan reklame dan poster (`umum-poster-*`, `umum-gates-*`, `umum-west-*`) |

**Kerjakan:** ikuti resep "Menambah bangunan".
- Papan reklame dan poster menampilkan gambar dari `loadBillboards` yang sudah ada. Ini konten iklan, bukan aset seni, jadi boleh dimuat sebagai tekstur (ADR-0023 §2.3).
- Gerbang tetap memicu `onWarp` ke kampungnya.

**Selesai bila:**
- Setiap bangunan ada, pintunya tepat di ubin pintu, dan `MapObject`-nya bisa dipakai.
- Tangkapan layar tiap bangunan dari depan disimpan di `outputs/kampung-3d/bangunan/` dan dikirim ke user untuk ditinjau.
- `--perf` dalam anggaran.

---

## P10-006: Orang: warga, pemain lain, kerumunan, Nadia

**Status:** ✅ selesai (2026-10-13, Sonnet 5.5) · **Repo:** `alr/game` (+ `titian-backend-go` untuk flag `dummy`)

**Kerjakan:**
1. **Warga** dari `map.npcs`:
   - Penampilan 3D (resep "Menambah warga"); 23 warga Kampung Bahasa beserta pedagang kelilingnya: gerobak bakso, siomay, es degan, es krim; pikulan jamu.
   - Label nama, ruang gerak, tanda tugas ("!" dan cahaya untuk langkah misi, `npcHasTask`).
2. **Pemain lain:** `look3d` bila ada (P10-008), selain itu `fromPixelLook`. Gerak diinterpolasi. Ketuk dari kepala ke atas memanggil `onPlayerTap`.
3. **Kerumunan dummy:**
   - Tambahkan flag `dummy: true` pada data pemain di snapshot dan `join` hub (`titian-backend-go/internal/pare/hub.go`, `crowd.go`), plus tes Go.
   - Di `/start`, dummy tidak punya tombol aksi sosial dan tidak pernah membalas.
   - Di `/play` tidak ada perubahan.
4. **Balon:** pesan chat pemain lain di saluran zona tampil sebagai balon di atas kepalanya (seperti `sayBubble` pixel), dua baris bila ada terjemahan. Pemain komputer tur (Nadia) mengikuti `src/game/tour.ts`.
5. **Hemat:** orang di luar 16 m tidak digambar dan tidak dianimasikan.

**Selesai bila:**
- Semua warga tampil dengan peran yang jelas.
- Kerumunan 8–12 orang berjalan alami dan diam saat disapa.
- Anggaran per orang ≤ 25 draw call.

---

## P10-007: Interaksi, kamera, kendaraan

**Status:** ✅ selesai (2026-10-13, Sonnet 5.5); beberapa butir menunggu keputusan (lihat Catatan) · **Repo:** `alr/game`

**Kerjakan:**
1. **Kamera** 1/2/3 persis acuan (panduan §6): tangan orang pertama, orang kedua dari lawan bicara atau warga terdekat, zoom, seret.
2. **Aksi tampilan:**
   - duduk di bangku (deco `bench` dan `park`);
   - ambil dan baca buku (di bangku perpustakaan dan taman);
   - hormat bendera (di tiang bendera bila ada di peta; tambahkan di Balai Desa bila belum ada);
   - lempar koin ke kolam/sungai, Rp500 lewat endpoint uang yang ada. Bila tidak ada endpoint yang pas, jadikan gratis dan tanyakan user.
3. **Warung dan kios:**
   - Tombol utama membuka jendela menu yang sudah ada (`VenueModal`).
   - Setelah server mengonfirmasi pembelian, pemain memegang piring atau gelas dan memutar animasi makan atau minum (acuan).
4. **Sepeda sewa** (`rentBike`, `bikeActive`): saat aktif, pemain naik sepeda onthel 3D dengan kecepatan 5,6 m/s. Turun dan naik dengan tombol.
5. **Kereta kelinci:**
   - Model 3D odong-odong (kepala kelinci, gerbong terbuka, lampu warna).
   - Mengikuti rute dan jadwal yang sama dengan pixel (`world/trains.ts`, `world/tour.ts`, `engine.train`, `boardTrain`, `requestAlight`).
   - Pemain duduk di dalamnya.
6. **Emote** delapan bawaan, menu Emote seperti acuan.
7. **Interaksi dengan warga:** sapa, ngobrol, salaman, tos, foto bareng. Kalimat dalam bahasa fokus pemain + arti, dari daftar kalimat per bahasa di `game3d/talk.ts` (lima bahasa, dibuat dengan pola `src/game/tour.ts`). Foto menghasilkan polaroid yang bisa disimpan.

**Selesai bila:**
- QA `02`–`09` sama dengan acuan.
- Semua interaksi ekonomi memakai endpoint yang ada.
- Tidak ada aturan baru di klien.

---

## P10-008: Lemari, `look3d`, dan kepemilikan barang

**Status:** ✅ selesai (2026-10-13, Sonnet 5.5); uji bayar toko dengan BuatQris sandbox menunggu user · **Repo:** `titian-backend-go` + `alr/game` + `agent/docs`

**Kerjakan:**
1. **Backend:**
   - Migrasi `pare_players.look3d jsonb` dan tabel `pare_wardrobe` (arsitektur §6).
   - Katalog di `data/pare/content.json → wardrobe`, diekspor dari `game3d/catalog.ts` dengan `bun scripts/wardrobe.ts --write`.
   - Endpoint `GET /pare/wardrobe`, `POST /pare/wardrobe/buy`, `PUT /pare/me/look3d`.
   - Snapshot hub membawa `look3d`.
   - Tes Go untuk: beli dengan uang game, menolak barang yang tidak dimiliki, barang Plus/Pro mengikuti status langganan.
2. **Toko (uang sungguhan):** lewat `economy.PaymentProvider` yang ada (BuatQris), pesanan baru jenis `pare_wardrobe`. **Jangan** menempelkan gateway langsung; harus tetap bisa diganti.
3. **`/start`:** menu AKU → Lemari dengan UI acuan (tab Lemari `Studio.tsx`). Isinya:
   - coba gratis;
   - label harga;
   - tombol Simpan, yang menyimpan `look3d`; bila ada barang yang belum dimiliki, dibuka jendela beli dulu.
4. **`/play`:** pemain yang punya `look3d` digambar dengan `toPixelLook(look3d)`.
5. Perbarui `api-contract.md` dan `domain-model.md`.

**Selesai bila:**
- QA `10`–`14` sama dengan acuan.
- Uji beli dengan uang game berhasil, dan uji beli toko di sandbox BuatQris berhasil. Minta user mengaktifkan sandbox; produksi saat ini LIVE.

---

## P10-009: Aksi berdua dengan pemain sungguhan

**Status:** kode selesai, uji dua pemain di peramban belum (butuh akun uji kedua) · **Dikerjakan:** 2026-10-13 · **Repo:** `titian-backend-go` + `alr/game`

**Kerjakan:**
1. **Protokol hub:**
   - `social_invite {with, act}` dengan `act` ∈ `ngobrol | salaman | tos | foto`;
   - `social_answer {with, ok}`;
   - `social_play {a, b, act}`, dikirim ke semua di saluran zona.
   - **Aturan server:** hanya antar pemain di zona dan saluran yang sama, jarak ≤ 3 ubin, satu ajakan aktif per pemain, kedaluwarsa 15 detik, dibatasi laju.
   - **Tidak pernah ke atau dari dummy.**
   - Tes Go.
2. **`/start`:**
   - Tombol aksi untuk pemain sungguhan mengirim ajakan.
   - Penerima melihat kartu ajakan (Terima / Tolak).
   - Setelah `social_play`, kedua klien (dan penonton) memutar animasi berdua yang sama.
   - Foto: masing-masing klien membuat polaroidnya sendiri.
3. **`/play`:** ajakan dari pemain 3D tampil sebagai pesan kecil "X mengajak salaman (buka di /start untuk melihatnya)" atau diabaikan. Tanyakan user mana yang dipilih.

---

## P10-010: Lulus uji Kampung Bahasa 3D

**Status:** todo · **Repo:** semua

**Kerjakan:**
1. QA lengkap (`qa.md`) di `/start` dan uji perangkat sungguhan oleh user di HP biasa dan PC; catat FPS per tingkat grafik.
2. Daftar kekurangan, diperbaiki atau dijadikan tiket.
3. Usulan urutan peta berikutnya: lima kampung, Camp, kota, negara (ADR-0023 "Keputusan terbuka" no. 1) untuk diputuskan user.
4. Perbarui `STATE.md` dan memori proyek.

---

## Catatan

(Diisi per tiket: tanggal, model, ringkasan, hasil QA visual per gambar, angka `--perf`, uji `/play`, deviasi.)

### P10-001 (2026-10-13, Sonnet 5.5)

**Yang dibuat** (`alr/game/src/game3d/`):
- Salinan apa adanya: `textures.ts`, `merge.ts`, `catalog.ts`, `avatar.ts`.
- `scene.ts`: langit, cahaya, `setTime`, `setQuality`, `update`, `wander`, dan `buildWorld` yang menyusun dunia. Tipe `World`, `Quality`, dan `TimeOfDay` ada di sini.
- `kit/`: `build.ts` (pembantu geometri, material, konteks bersama, `R` berbiji, `blocked`), `ground.ts`, `nature.ts` (daun, pohon, kelapa, pisang, pagar tanaman, pohon, rumput tinggi), `building-course.ts`, `pole.ts` (lampu dan tiang listrik), `bench.ts`, `flag.ts`, `pond.ts`, `bike.ts`, `warung.ts`, `fence.ts`, `house.ts`.
- Mesin: `engine3d.ts` (kelas `Engine3D`: renderer, loop, status bersama, dan metode satu baris yang memanggil modul), `people.ts`, `camera.ts`, `input.ts`, `interact.ts`, `bubbles.ts`.
- `ui/ConceptStudio.tsx` dan `ui/studio.module.css` (salinan Studio acuan di atas mesin baru), `ui/ConceptV2Loader.tsx`, route `src/app/(game)/3d-concepts/v2/`.

**Cara memecah:**
- Angka dan urutan **tidak diubah**. Pemecahan dilakukan dengan skrip yang memotong berkas acuan per bagian, jadi isinya identik.
- Urutan pemanggilan pembangun dipertahankan karena `R` (acak berbiji) dipakai bersama.
- Fungsi mesin menerima mesin sebagai `eng`, dan `Engine3D` menyimpan metode satu baris yang memanggilnya. Dengan begitu pemanggil di tempat lain tidak berubah.

**Deviasi dari tiket:**
- `demo.ts` tidak dibuat. `buildWorld` di `scene.ts` sudah menyusun tata letak halaman konsep, jadi `demo.ts` tidak punya isi.
- Kelas dinamai `Engine3D` (bukan `Engine`). Antarmuka `GameEngine` datang di P10-002.
- Penghitung gerak bendera dan riak dipindah ke `flag.update` dan `pond.update`. Rumusnya sama.

**QA:**
- `tsc` dan `eslint src/game3d` bersih. `src/components/concepts3d` tidak disentuh.
- Semua aksi QA berjalan di `/3d-concepts/v2` (`bun scripts/qa/3d.ts --url /3d-concepts/v2`): salaman, foto, orang ke-1, pecel, orang ke-2, naik sepeda, ambil buku, duduk, joget, Lemari (tiga gaya), Konsep, Senja, Malam, dan 3 gambar HP. Total 19 gambar.
- **Perbandingan visual dengan `golden/`** (sembilan pasang dibandingkan berdampingan: 01, 05, 07, 09, 10, 12, 13, 14, 16): **sama**. Cahaya, material, proporsi tiga gaya, pakaian lokal, wajah, kartu peserta, UI, dan kamera sama. Yang beda hanya letak orang di keramaian, karena acak.
- **Angka kinerja**, diukur deterministik (2 orang, kamera tetap, halaman konsep vs `/v2`):

| Tingkat | Konsep (draw call / segitiga) | `/v2` |
|---|---|---|
| Tinggi | 583 / 202.446 | 582 / 202.426 |
| Rendah | 301 / 97.927 | 300 / 97.907 |

  Selisih 1 draw call dan 20 segitiga, di bawah 0,2% (batas tiket ±3%).
- `/play` tidak disentuh, jadi tidak diuji ulang (tiket ini hanya menambah `src/game3d` dan satu route).

**Berikutnya:** P10-002 (antarmuka `GameEngine` bersama).

### P10-002 (2026-10-13, Sonnet 5.5)

**Yang dibuat/diubah** (`alr/game/src`):
- `game/engine/types.ts`: `GameEngine`, `EngineCallbacks`, `Interaction`, `CameraModeInfo`, `EngineKind`. Isinya persis anggota yang dipakai di luar `engine.ts`, hasil `grep` di `Game.tsx`, `Minimap`, `TourGuide`, dan `EarnModals`, dan dikunci oleh `tsc`.
- `game/engine/create.ts`: `createEngine(kind, canvas, overlay, callbacks, options)`. `"pixel"` membuat `Engine`; `"3d"` melempar galat sampai P10-003.
- `game/engine/engine.ts`:
  - `Engine implements GameEngine`.
  - Menambah `kind = "pixel"` dan `cameraModes = CAMERA_MODES`.
  - Tipe `EngineCallbacks` dan `Interaction` dipindah ke `types.ts`, dan engine mengekspor ulang.
  - Perilaku tidak berubah.
- `components/game/Game.tsx`:
  - Prop `engine?: "pixel" | "3d"` (bawaan `"pixel"`), diteruskan ke `World`.
  - Mesin dibuat lewat `createEngine`; `useRef` dan `useState` bertipe `GameEngine`.
  - Menu kamera membaca `engine.cameraModes` dan `engine.camera` (tidak lagi `CAMERA_MODES` yang tertulis mati).
- `Minimap.tsx`, `TourGuide.tsx`, `EarnModals.tsx`: tipe `Engine` → `GameEngine`.

**Daftar anggota antarmuka:**
- **Hidup:** `start`, `destroy`, `paused`, `typing`.
- **Zona dan tujuan:** `zone`, `map`, `npcs`, `loadZone`, `setGoalTile`, `setGoalZone`, `setExtraNpcs`, `setCompanion`.
- **Pemain:** `player`, `playerTitle`, `playerAvatar`, `virtualDir`, `riding`, `train`, `boardTrain`, `requestAlight`, `interact`, `setLook`, `sayBubble`.
- **Pemain lain:** `remotes`.
- **Dunia:** `weather`, `clockSkew`, `adFree`.
- **Kamera:** `cameraModes`, `camera`, `setCamera`, `recenter`, `zoomBy`, `canZoomIn`, `canZoomOut`.

Tabel di `arsitektur.md` §3 belum memuat `boardTrain`, `setLook`, `sayBubble`, dan `kind`, sehingga ketiganya ditambahkan ke antarmuka setelah `tsc` menunjukkan Game.tsx memakainya.

**Catatan untuk P10-003:**
- `overlay` di `createEngine` bertipe `HTMLCanvasElement` (pixel). Mesin 3D memakai `div`, jadi tipenya dilebarkan di tiket itu.
- Bentuk data (`Actor`, `Remote`, `Npc`, `WorldMap`) tetap milik mesin pixel. Mesin 3D harus mengisi `player.x/y/dir` dalam ubin, karena Minimap dan EarnModals membacanya.

**QA:**
- `tsc` dan `eslint` bersih untuk berkas yang disentuh.
- **`/play` diuji ulang** (backend lokal + `scripts/video/rec.ts` sebagai pemain uji `view@example.com`):
  - masuk dan muncul di Kampung Bahasa;
  - menu Warung Pecel terbuka dengan `E`;
  - beli nasi pecel menghasilkan "Makan ke-1 hari ini · stamina +15" dan uang berkurang Rp5.000;
  - panel Chat terbuka;
  - BELAJAR membuka jendela Jalur, dan kartu Materi bisa dibuka.
  - Tangkapan layar: `/tmp/pare-video/regress-*.jpg`.
- `/3d-concepts` dan `/3d-concepts/v2` tidak terpengaruh. Keduanya memakai `src/game3d` dan `components/concepts3d`, yang tidak disentuh.

**Berikutnya:** P10-003 (route `/start` dan `Engine3D` berjalan di Kampung Bahasa, tanah saja).

### P10-003 (2026-10-13, Sonnet 5.5)

**Yang dibuat/diubah** (`alr/game/src`):
- **Route:**
  - `app/(game)/start/layout.tsx` (salinan layout `/play`, judul "Kampung Bahasa 3D", tidak diindeks).
  - `app/(game)/start/page.tsx` (cek maintenance seperti `/play`).
  - `components/game/Start3DLoader.tsx`: memuat `Game` dengan `engine="3d"` dan pabrik mesin 3D lewat `import()` dinamis, jadi three.js hanya dimuat halaman ini.
- **Antarmuka:**
  - `Game` menerima prop `factory?: EngineFactory`; `createEngine(kind, …, factory?)`.
  - `create.ts` tidak mengimpor mesin 3D, supaya bundel `/play` tidak ikut membesar.
- **`game3d/atmosphere.ts`:**
  - Langit, cahaya, waktu, dan efek tingkat grafik yang dikeluarkan dari `scene.ts`.
  - Dipakai bersama konsep dan game. Angkanya sama dan `scene.ts` memanggilnya.
- **`game3d/start/look.ts`:** `fromPixelLook` dan `toPixelLook`. Tabel pemetaannya ada di komentar berkas.
- **`game3d/start/zone.ts`:**
  - `WorldMap` menjadi denah 3D (1 ubin = 2 m, utara = −z).
  - Tanah satu mesh berwarna per kode dengan variasi kecil.
  - Ubin padat jadi balok sementara (pohon, bangunan, pagar, dekor).
  - Objek interaksi jadi tiang kuning, dan gerbang jadi bantalan biru.
  - Tabrakan lingkaran terhadap ubin padat.
- **`game3d/start/engine.ts`: kelas `Start3D implements GameEngine`.**
  - Berjalan dengan WASD/panah, joystick Game (`virtualDir`), Shift lari. Gerak halus, tabrakan, dan sentuhan ke ubin lain memanggil `onStep`.
  - Ubin gerbang memanggil `onWarp`, pindah zona lewat Game seperti di pixel.
  - `interact()` memilih yang terdekat dalam 2,6 m (orang di depan sedikit diutamakan) dan memanggil `onInteract` dengan `Interaction` yang sama. `onPrompt` memakai teks yang sama dengan pixel.
  - Pemain lain (`remotes`) digambar dengan interpolasi, dan `px/py` diperbarui untuk Minimap.
  - Warga berdiri di ubinnya, dengan label nama dan tanda ❗/🎯 dari `npcHasTask`.
  - Pendamping misi mengikuti pemain, dan `sayBubble` menampilkan balon.
  - Waktu mengikuti jam WIB game (+ `clockSkew`): pagi sampai 16:30, senja sampai 18:30, lalu malam.
  - Kamera orang ketiga (orbit) dan orang pertama dengan zoom, seret, dan pinch.
  - Sinar tiang di `goalTile` untuk tur.
  - Tombol "⚙ Grafik" (Hemat → Rendah → Sedang → Tinggi), pilihan disimpan di `kb3d-grafik`. Awalnya Rendah di layar sentuh, Sedang di PC.
  - Badan orang hanya dibuat dalam 42 m dari pemain dan dibuang di atas 56 m.
- `scripts/video/rec.ts`: `openGame` menerima `path`.

**Deviasi dari tiket:**
- Kelasnya bernama `Start3D` di `game3d/start/engine.ts`, bukan `Engine3D` di `engine3d.ts`. `Engine3D` sudah dipakai mesin konsep yang dibekukan sebagai acuan QA.
- HUD 3D sendiri tidak dibuat. Joystick, zoom, dan menu kamera Game.tsx dipakai ulang, dan hanya tombol Grafik yang ditambah.
- Jangkauan interaksi 2,6 m, bukan 1,6 m. Ubin bersebelahan berjarak 2 m dari pusat ke pusat, jadi 1,6 m tidak pernah mengenai objek di depan.
- Kamera orang kedua, tangan orang pertama, kereta kelinci (`boardTrain`, `requestAlight` kosong), dan sepeda 3D menunggu P10-007.
- Cuaca (`weather`) disimpan tetapi belum digambar (P10-004).

**QA (`/start`, backend lokal, pemain uji `view@example.com`, Chrome tanpa GPU):**
- Halaman termuat dan HUD Game muncul (nyawa, uang, jam, lokasi) tanpa galat konsol.
- Karakter Dinda tampil dengan nama dan bisa berjalan: ubin (40,50) → (39,47). Posisi sampai ke server.
- 10–11 pemain keramaian server tampil sebagai karakter 3D (16 badan dari 52 punya rig dalam jangkauan).
- Tekan `E` di depan warung membuka jendela Warung Pecel yang sama dengan `/play`.
- Kamera orang pertama dan zoom bekerja.
- `/play` diuji ulang: warung, makan, chat, dan jendela Jalur masih normal.
- `tsc` dan `eslint` bersih.
- **Belum diuji:** dua akun serentak (`/play` melihat pemain `/start`). Akun uji kedua butuh izin user. Lintasan datanya sama, yaitu `onStep` → `Net.move`, dan keramaian server sudah terbukti terlihat di `/start`.

**Catatan untuk P10-004:** tanah dan balok sementara ada di `game3d/start/zone.ts`; ganti dengan tanah bertekstur, alam, dan bangunan yang dibaca dari `WorldMap` yang sama. Hook QA dev: `window.__kbStart` (hanya di development).

**Berikutnya:** P10-004 (tanah, alam, langit, dan grafik Kampung Bahasa).

### P10-004 (2026-10-13, Sonnet 5.5)

**Yang dibuat/diubah** (`alr/game/src/game3d`):
- **`atmosphere.ts`:**
  - Parameter hari dijadikan satu struktur (`Params`).
  - `setTime(tm)` (konsep) menghasilkan angka yang persis sama.
  - `setClock(jam, hujan)` baru memadukan kunci pada 04:30 malam, 05:30 fajar, 07:30 pagi, 12:00 siang (matahari 70°), 16:00 sore, 17:15 senja, dan 18:30 malam.
  - Hujan menurunkan matahari dan memucatkan langit dan kabut.
  - Pantulan langit (PMREM) hanya dibangun ulang bila gambar berubah cukup jauh.
- **`start/zone.ts` ditulis ulang:**
  - Peta dipotong menjadi **kepingan 30 × 30 ubin (60 m)**. Tiap kepingan dibangun sekali, bagian diamnya digabung per material, dan ditampilkan atau disembunyikan menurut jarak.
  - **Tanah** bertekstur per kode:
    - Rumput (dengan pita rumput `l`), jalan tanah (`dirt()` baru di `textures.ts`), paving, dan aspal dengan marka putus-putus di garis tengah jalan dua jalur.
    - Air turun 0,12 m dengan tepi batu, sawah, jembatan kayu berpagar, lantai papan, tikar, dan karpet.
  - **Bunga** di ubin `f`, **rumput tinggi** (hanya Sedang dan Tinggi), dan **pohon** di ubin `T`: pohon peneduh, kelapa, atau pisang, dipilih tetap per ubin.
  - **Pagar** `F`: tembok rendah dengan jeruji besi.
  - **Dekor** yang sudah punya model: lampu (menyala saat senja), bangku, tiang bendera, tiang rambu, pagar tanaman, petak bunga.
  - **Tiang listrik dengan kabel** sepanjang jalan lurus ≥ 30 ubin.
  - **Masih balok sementara:** bangunan (`B`) dan dekor tanpa model (`X`), sampai P10-005.
- **`start/engine.ts`:**
  - Waktu mengikuti jam game secara mulus.
  - **Hujan:** garis hujan di sekitar kamera untuk `drizzle`, `rain`, dan `storm`, dengan langit dan kabut lebih kelabu.
  - **Empat tingkat grafik** sesuai panduan §5, ditambah:
    - Jarak gambar per tingkat: Hemat 80 m, Rendah 105 m, Sedang dan Tinggi 150 m.
    - Kabut mengikuti jarak itu.
    - Hemat dan Rendah memakai daun pohon lebih kasar dan 60% pohon (zona dibangun ulang bila melewati batas itu).
    - Bayangan bulat di bawah orang pada Hemat dan Rendah.
    - Orang jauh tidak dibuat: Hemat 16 m, Rendah 40 m, Sedang 42 m, Tinggi 46 m.
  - **Pemilihan awal otomatis:** tingkat yang belum dipilih pemain diturunkan ke Hemat bila 10 detik pertama di bawah 24 fps, dengan pemberitahuan.

**Deviasi dari tiket/panduan:**
- Kepingan 60 m, bukan 40 m. Tiap kepingan memakai satu draw call per material, sehingga kepingan lebih besar memangkas draw call hampir setengah.
- Kabut 55–190 m (Sedang dan Tinggi), bukan 70–330 m, supaya batas jarak gambar tidak terlihat. Panduan gaya §4 dan §5 diperbarui.
- Siang tidak punya warna sendiri: Pagi dengan matahari di 70°, seperti tertulis di panduan.
- Air sedalam 0,12 m, bukan 0,25 m. Tepi batu 0,22 m menutup celahnya.

**Angka kinerja** (`renderer.info`, kamera tetap di (40,50), ±11 pemain keramaian):

| Tingkat | Draw call | Segitiga | Batas |
|---|---|---|---|
| Hemat | 316 | 124 rb | ≤ 350 / 200 rb (Rendah) |
| Rendah | 317 | 124 rb | ≤ 350 / 200 rb |
| Sedang | 615 | 334 rb | – |
| Tinggi | 671 | 364 rb | ≤ 1.000 / 450 rb |

Sempat 454 draw call / 269 rb segitiga di Rendah. Sumber terbesarnya, bunga (±170 rb segitiga), tiang penanda objek, dan kelapa, diperkecil, lalu kepingan diperbesar dan 60% pohon dipakai di Rendah. Konsep `/3d-concepts/v2` tetap 583 draw call / 202.446 segitiga, sama dengan acuan.

**QA:**
- `tsc` dan `eslint` bersih. `/start` tanpa galat konsol.
- Gambar fajar (06:00), siang (12:00), senja (17:24), dan malam (20:00) diambil di (40,50): warna bergerak mulus, lampu menyala saat senja dan malam.
- **Perlu persetujuan user:** tampilan hujan (garis hujan 0,8 opak, langit kelabu). Tidak ada di konsep, jadi tangkapan layarnya perlu dilihat user.
- **Belum dibandingkan** dengan `golden/` untuk 01 (gedung kursus), karena bangunan baru datang di P10-005. Perbandingan itu dikerjakan di tiket tersebut.
- Perangkat sungguhan (HP biasa) belum diuji; itu oleh user di P10-010.

**Berikutnya:** P10-005 (bangunan Kampung Bahasa).

### P10-005 (2026-10-13, Sonnet 5.5)

**Yang dibuat** (`alr/game/src/game3d/start/buildings.ts`, dipanggil dari `zone.ts`):
- **`buildBuilding`:**
  - Dibaca dari `map.buildings`: `x, y, w, roof+wall` jadi petak (lebar × kedalaman), `door` jadi pintu di sisi selatan, `label` jadi papan nama.
  - **Satu bentuk dasar per `style`:**
    - `house` (Camp, Balai Desa): dua lantai, atap limas, jendela berteralis, teras bertiang, unit AC.
    - `shop`: etalase kaca, kanopi dengan warna atap, papan nama.
    - `hall`: balairung dengan serambi.
    - `stall`: lapak terbuka dengan terpal belang, meja, dan dagangan.
    - `tent`: tenda kanvas.
  - **Atap:** genteng tanah liat untuk warna merah, oranye, atau cokelat; seng berwarna untuk warna lain.
  - **Satu model per `form`:** masjid (kubah + dua menara), gereja (menara + puncak), katedral (dua menara + jendela mawar), pura (gapura belah + meru bertingkat), klenteng (atap kuning ganda, lampion), candi (piramida berundak + puncak), terminal bus (kanopi bertiang), stasiun (atap lengkung + menara jam), klasik/museum/bank/imigrasi (serambi berpilar + atap pelana), sekolah (bendera), puskesmas (palang merah), dan bioskop (marquee berlampu).
- **`buildDecor`:**
  - **Lima gerbang kampung** berbeda bentuk: paifang Mandarin, gerbang putih berkubah Arab, gerbang batu Inggris, torii Jepang, hongsalmun Korea. Semuanya dengan papan nama.
  - **Papan KAMPUNG BAHASA PARE**.
  - **Reklame dan poster:** isi dari `panelFor` dan `frameAt/posterCanvas` yang sama dengan `/play`, digambar ulang bila panelnya berganti.
  - **Lainnya:** halte, air mancur, gerobak berlabel, patung, ayunan, perosotan, monumen (gapura dan stupa), bus, orang-orangan sawah, dan sepeda parkir.
- **`zone.ts`:**
  - Ubin bangunan dan dekor yang sudah bermodel tidak lagi berupa balok sementara.
  - `ads(now, adFree)` dipanggil `Start3D` tiap detik.
  - Tiang penanda objek (kuning) dan bantalan gerbang (biru) tetap sebagai penanda.

**Deviasi dari tiket:**
- Tangkapan layar per bangunan tidak satu-satu (33 bangunan). Yang tersimpan: 12 sudut (`outputs/kampung-3d/bangunan/`) yang mewakili semua bentuk:
  - camp, museum, masjid, candi, terminal, stasiun, gerbang, huruf, gereja, toko, pasar, klenteng;
  - gerbang, huruf, dan pasar masing-masing memperlihatkan beberapa model sekaligus.
- Papan reklame tetap papan teks dan poster pixel art dari game, bukan foto.
- Bentuk `tower`, `mall`, `airport`, `control`, `palace`, `pagoda`, `souk`, `madrasa` (kota dan luar negeri) belum punya model sendiri. Sementara memakai balairung biasa. Masuk pekerjaan peta berikutnya.
- Objek interaksi tetap tiang kuning di depan pintu, belum papan atau meja sungguhan.

**QA:**
- `tsc` dan `eslint` bersih; `/start` tanpa galat konsol.
- Pintu setiap bangunan berada di kolom `door` pada sisi selatan. Objek pintu (`MapObject`) di ubin di depannya tetap memanggil jendela yang sama dengan `/play` (diuji untuk warung, stasiun, terminal, masjid, museum, candi: tulisan prompt benar).
- Perbandingan visual dengan acuan `01-overview`/`golden`: kesan material sama (plester, genteng, batu alam, jendela berteralis, papan nama). Susunan gedung kursus konsep sendiri tidak ada di peta game, jadi tidak dibandingkan satu-satu.
- Kinerja (kamera awal di (40,50), 11 orang):

| Tingkat | Draw call | Segitiga | Batas |
|---|---|---|---|
| Hemat / Rendah | 289 / 271 | 91 rb / 81 rb | ≤ 350 / 200 rb |
| Sedang / Tinggi | 536 | 259 rb | ≤ 1.000 / 450 rb |

  Dengan kamera yang jauh lebih tinggi dan lebar (pitch 0,55, jarak 14 m) Rendah mencapai 409 draw call, sedikit di atas batas 350, dan Tinggi 833 / 372 rb. Itu yang dipakai untuk menentukan jarak gambar Hemat (60 m) dan Rendah (80 m).

**Berikutnya:** P10-006 (orang: warga, pemain lain, keramaian, Nadia).

### P10-006 (2026-10-13, Sonnet 5.5)

**Backend** (`titian-backend-go/internal/pare`):
- `PlayerInfo.Dummy` (`json:"dummy,omitempty"`) diisi `true` oleh `walker.info()` di `crowd.go`, jadi snapshot dan `join` hub menandai warga keramaian.
- Tes `TestCrowdIsSeenButNeverSpeaksOrCounts` memeriksa tanda itu (lulus). Binari dibangun ulang dan flag sampai ke klien (8 dari 8 `remotes` bertanda `dummy`). Tidak ada perubahan skema.

**Game** (`alr/game/src`):
- `PlayerInfo.dummy` di `protocol.ts` dan `Remote.dummy` di `engine.ts`. `/play` tidak memakainya.
- `Start3D`:
  - Keramaian dummy tidak mendapat aksi ngobrol dan tidak bisa menjadi target `E`.
  - **Warga berjalan** seperti di pixel: radius `wander` di sekitar tempatnya, atau rute titik untuk pedagang keliling (1,1 m/s, berhenti 2–8 detik, tidak menabrak dinding atau pemain). Ubin `npcs[]` ikut diperbarui untuk Minimap.
  - **Pedagang** membawa gerobak, nampan, atau bakul gendong.
  - Label nama, tanda ❗/🎯 (`npcHasTask`), dan balon chat (`sayBubble`) sudah ada dari P10-003.

**Deviasi:** penampilan warga memakai `fromPixelLook` (gaya Kartun), bukan tabel `NPC_LOOK3D` per warga; tabel itu menunggu keputusan seni user. Pendamping misi dan Nadia memakai jalur warga ekstra tanpa perilaku khusus.

**QA:** 42 warga, 7 bergerak dalam 12 detik, 4 pedagang bergerobak, tanpa galat konsol. `tsc`, `eslint`, dan tes Go lulus.

**Berikutnya:** P10-007 (interaksi, kamera, kendaraan).

### P10-007 (2026-10-13, Sonnet 5.5)

**Yang dibuat** (`alr/game/src/game3d`):
- `kit/bike.ts`: `makeBicycle` dikeluarkan dari `buildBikes` (isi sama).
- `start/actions.ts`: kalimat warga dalam lima bahasa (`TALK`, bahasa fokus pemain dari `store`), model **kereta kelinci** (lokomotif berkepala kelinci + tiga gerbong terbuka), panel aksi, dan polaroid.
- `start/engine.ts`:
  - **Kamera:** orang ketiga, **orang pertama dengan tangan** (`buildHands`/`animateHands` dari avatar, ikut pose dan barang yang dipegang), dan **orang kedua** (mata warga atau pemain nyata terdekat dalam 10 m yang menatap pemain; arah jalan menjauh dari pengamat). Zoom bekerja di ketiganya.
  - **Aksi:**
    - Panel kiri bawah: Sapa, Salaman, Tos, Foto bareng (untuk warga terdekat; keramaian dummy tidak pernah), Duduk/Berdiri di bangku dekor, Baca/Taruh buku saat duduk, Hormat bendera di tiang bendera, Lempar koin ke air (koin melengkung dan riak), dan menu Emote (8 emote).
    - Warga membalas: menoleh, memutar pose yang sama, dan berbicara dengan bahasa yang dipelajari plus artinya di bawahnya (balon dua baris).
    - Foto bareng menghasilkan polaroid (Simpan/Tutup).
  - **Sepeda:** saat `engine.riding` (disewa lewat game), sepeda onthel 3D dengan pose mengayuh dan roda berputar, 5,6 m/s.
  - **Kereta kelinci:** empat kereta mengikuti rute dan jam game yang sama dengan pixel (`trains.ts`). `boardTrain`, `requestAlight`, pindah zona (`onRideZone`), dan turun di halte (`onAlight`) bekerja seperti di pixel.

**Deviasi dari tiket:**
- **Makan/minum setelah membeli** di warung belum ada: kontrak `GameEngine` tidak memberi tahu mesin bahwa pembelian berhasil. Butuh satu callback baru di Game.tsx (usulan: `engine.onPurchased(kind)`), jadi menunggu persetujuan user karena menyentuh `/play`.
- **Lempar koin gratis**, belum Rp500, karena belum ada endpoint uang yang pas (sesuai tiket: tanyakan user).
- **Hormat bendera:** peta Kampung Bahasa punya tiang bendera, jadi tidak perlu menambah di Balai Desa.
- **Aksi tanpa perlu server:** duduk, baca, koin, foto, dan emote. Aksi dengan pemain nyata ada di P10-009.
- Kualitas foto bareng masih sederhana (kamera dari belakang pemain), belum dibandingkan dengan acuan `04-foto`.

**QA** (`/start`, backend lokal, kamera di Kampung Bahasa):
- Sapa, Salaman, Foto bareng: balon dua baris dan polaroid tampil. Duduk di bangku lalu Baca buku: pose duduk dan buku di tangan. Orang kedua dan orang pertama dengan tangan: tampil. Sepeda: tampil dengan pose kayuh.
- Naik kereta: pemain ikut berjalan di rute, berpindah zona dari Kampung Bahasa ke Kampung Arab (`zone: "ar"`) dan terus bergerak, tanpa galat.
- `tsc` dan `eslint` bersih; tanpa galat konsol.
- Perbandingan dengan `golden/02`–`09` baru bisa dilakukan penuh di P10-010, karena acuan memakai gedung kursus dan keramaian tersendiri.

**Berikutnya:** P10-008 (Lemari, `look3d`, kepemilikan barang).

### P10-008 (2026-10-13, Sonnet 5.5)

**Backend** (`titian-backend-go`):
- Migrasi `0104_pare_wardrobe.sql`: `pare_players.look3d`, tabel `pare_wardrobe`, jenis pesanan `pare_wardrobe`.
- `data/pare/wardrobe.json` (45 barang) diekspor dari `catalog.ts` oleh `game/scripts/wardrobe.ts --write`. Server memegang harga dan hak pakai.
- `internal/pare/wardrobe.go` dengan tiga endpoint (lihat `api-contract.md`):
  - **Beli dengan uang game:** `Apply` ke buku besar dan insert dalam satu transaksi.
  - **Toko:** pesanan QRIS lewat `economy.Service.CheckoutPareItem`. Gerbang pembayarannya tetap `PaymentProvider`, tidak ditempel ke satu penyedia. `settle` memanggil `GrantPareItem`.
  - **Simpan penampilan:** `PUT /pare/me/look3d` memvalidasi gaya, warna, ukuran tubuh, dan bahwa tiap barang yang dipakai dimiliki. Barang Plus/Pro dihitung dari paket yang berjalan.
- Hub: `PlayerInfo.Look3D` (snapshot, `join`, dan frame `profile`). `GET /pare/me` membawa `look3d`. Dashboard admin menghitung pesanan `pare_wardrobe` sebagai pendapatan game.
- Tes `TestWardrobe` (baru) menutup: barang gratis, ditolak sebelum dimiliki, uang kurang, beli uang game (harga Rp12.000), beli dua kali, pesanan toko dan pelunasan lewat webhook stub, barang paket Plus (dan Pro ditolak), dan `look3d` di `PlayerInfo`. Tes `./internal/pare`, `./internal/economy`, `./internal/admin` lulus semua.

**Game** (`alr/game/src`):
- `lib/api.ts`: `pareWardrobe` (get, buy, setLook), tipe, dan `look3d`.
- `game3d/start/Wardrobe.tsx` + `wardrobe.module.css`: tombol "👗 Lemari" dan panel (Gaya, Tubuh, slot pakaian, warna). Mencoba apa saja gratis dan langsung terlihat di karakter; barang yang belum dimiliki dicantumkan dengan tombol Beli (uang game langsung, toko lewat QR dan polling pesanan) dan tombol Simpan hanya terbuka bila semuanya dimiliki. Panel menggulir di HP dan tombol Simpan tetap terlihat.
- `Start3D`: `dress(look)`, `setWardrobe(on)` (kamera depan dengan karakter diam, geser untuk memutar), `look3d` dipakai untuk diri sendiri (diambil dari server) dan pemain lain (`remotes[].look3d`). Registry `start/registry.ts` mempertemukan mesin dengan panel, jadi `Game.tsx` tidak berisi kode Lemari.
- `Game.tsx` (dibagi dengan `/play`): satu baris menyalin `look3d` dari frame `profile`. `PlayerInfo`, `Remote`, `PlayerProfile` mendapat `look3d?`.

**Deviasi dari tiket:**
- Tombol Lemari melayang di layar 3D (di bawah tombol grafik), bukan di dalam menu AKU. Dengan begitu menu AKU yang dibagi dengan `/play` tidak disentuh. Bila kamu mau di menu AKU, itu perubahan kecil di `AkuModal`.
- `/play` belum menampilkan pemain 3D lewat `toPixelLook(look3d)`: pemain tetap digambar dari `look` pixel mereka. Pemetaan balik sudah ada (`look.ts`) dan butuh satu baris di engine pixel.
- Pemain 3D belum punya `look` pixel yang ikut berubah saat berdandan di 3D.

**QA** (`/start`, backend lokal dengan gerbang stub):
- Buka Lemari, ganti ke Realis, pilih Batik kawung dan Kain jarik: terlihat langsung di karakter.
- Daftar "belum dimiliki" tampil dengan harga. Beli Batik dengan uang game: uang Rp50.000 → Rp38.000. Beli Jarik (toko): pesanan QRIS terbentuk (201), setelah pembayaran stub barang bisa dipakai. Simpan: `look3d` tersimpan di server.
- `/play` diuji ulang (warung, makan, chat): normal. `tsc` dan `eslint` bersih.
- **Belum diuji:** pembelian toko dengan BuatQris sandbox (produksi saat ini LIVE). Minta user mengaktifkan mode sandbox di server lokal.

**Berikutnya:** P10-009 (aksi berdua dengan pemain sungguhan).

### P10-009 (2026-10-13, Sonnet 5.5)

**Backend:** `internal/pare/social.go` (`onSocial`), field `With, Act, Ok` di `ClientMsg`. Server menolak yang jauh (> 3 ubin), beda saluran, terlalu cepat (2 dtk), dan kedaluwarsa (15 dtk); dummy tidak pernah bisa diajak karena bukan koneksi. Tes `TestHubSocialInvite` lulus. **Backend belum di-deploy** (prod masih build Lemari); deploy hanya atas permintaan, cadangkan DB dulu.

**Klien:**
- `protocol.ts`/`net.ts`: `social_invite`, `social_answer` (kirim) dan `social_invite`, `social_no`, `social_play` (terima).
- `Game.tsx`: dua tambahan kecil: `onSocial` di callback dan `case` yang meneruskan frame ke `e.socialEvent?.()`. `Engine` piksel tidak punya `socialEvent`, jadi `/play` mengabaikan frame itu.
- `Start3D`: chip "Ngobrol / Ajak salaman / Ajak tos / Ajak foto" bila pemain sungguhan lebih dekat dari warga (≤ 3,2 m); kartu ajakan Terima/Tolak (hilang sendiri setelah 15 dtk); `social_play` memutar pose dan balon yang sama seperti dengan warga di kedua pemain, penonton melihat keduanya beraksi; foto: tiap klien membuat polaroidnya sendiri.

**QA (2026-10-13, backend lokal `pare_view`, izin user):** pemain tiruan `view@example.com` (dinda, di peramban `/start`) dan `qa0001` (andi10, soket dari skrip) berdiri 2 m satu sama lain.
- Andi mengajak salaman: kartu "Andi mengajak salaman" tampil, Terima ditekan, kedua pihak menerima `social_play`; Dinda memutar salaman dan balon "Nice to meet you!".
- Dinda menekan "Ajak tos": Andi menerima `social_invite {act: tos}`, menjawab ok, `social_play` kembali. Chip Ngobrol/Ajak salaman/Ajak tos/Ajak foto tampil saat Andi dalam 3,2 m.
- Perbaikan dari QA: kartu dan pemberitahuan tertutup HUD, diturunkan ke `top:104px`.
- Tanpa galat konsol. Belum diuji: foto berdua, penonton ketiga, tombol Tolak, kedaluwarsa.

### Perbaikan lanjutan (2026-10-13, Sonnet 5.5)

- **Badan tenggelam di bangunan:** lingkaran tabrakan pemain kini menjauh 0,45 m ekstra dari ubin bangunan (`B`), karena tangga, tiang, dan teras gedung menjorok keluar dari ubinnya (`zone.ts`, `blocked`). Pagar (`X`) dan air tidak berubah. Pintu tetap bisa dimasuki (jarak dari tepi ubin ke tengah pintu 1 m, lebih dari 0,75 m yang dipakai).
- **Ganti skin di camp tidak terlihat:** kamera Lemari berada di luar tembok kamar. Kini kamera tidak masuk ke dinding: mendekat dan memilih sisi yang lebih lapang (jarak lensa dilebarkan agar bingkainya tetap).
- **Joystick HP:** jari boleh melewati tepi lingkaran (tarikan 1 = tepi, sampai 1,7; knob tetap di tepi). Sampai 125% berjalan (0,8 → 4 m/s, landai); lewat 125% naik ke lari 7 m/s dalam 15% berikutnya; kecepatan naik pelan (7 m/s²) dan turun lebih cepat (14 m/s²). Terukur: 50% = 1,9; 100% = 3,3; 125% = 4,0; 150% = 7,0 m/s. Zona mati 5 px.
- **Sisi joystick (HP dan tablet):** menu ⚙ punya baris "Joystick di sisi: Kiri / Kanan", hanya di layar sentuh (`pointer: coarse`). Bawaan: kanan. Pilihan disimpan di `localStorage` (`pare-control-side`, `src/lib/controlSide.ts`) dan berlaku juga di `/play`. Tombol A pindah ke sisi lain, begitu juga BELAJAR/MISI/CHAT. Dilihat di emulasi HP: joystick kanan, A kiri, tanpa tumpang tindih.
- **Tombol grafik ⚙:** membuka pilihan Hemat/Rendah/Sedang/Tinggi dengan tanda ✓ pada yang dipakai dan teks "Grafik sekarang: …".

### Perbaikan dari uji di pare.titianasa.com (2026-10-13, Sonnet 5.5)

Pemilik mengirim dua tangkapan layar dari `/start` yang sudah di-push:
- **Tiang listrik di tengah jalan:** jalan dua ubin lebar membuat tiang diletakkan di tiap baris jalan, sehingga baris kedua jatuh di garis tengah. Kini hanya di tepi atas jalan (`zone.ts`).
- **Pose Lemari di desktop tertutup:** kamera terlalu dekat (kepala terpotong) dan bergeser terlalu jauh ke kiri. Kini jarak 3,3 × tinggi badan, pusat pandang 0,88, dan bergeser setengah lebar panel (maks 400 px), jadi tubuh utuh dan berada di tengah ruang kiri panel. Diuji di 1280×720 (`QA_DESKTOP=1280x720` di `scripts/video/rec.ts`).
- **Sepeda tidak pas di sadel:** sadel 0,24 m di belakang tengah rangka dan pose mencondongkan pinggul 0,22 m ke depan; sepeda kini digeser 0,46 m ke depan, sehingga pinggul tepat di atas sadel.
- **Odong-odong (kereta kelinci) tidak pas di tempat duduk:** pemain dulu didudukkan di tengah gerbong (antara dua bangku). Kini di atas bangku (z ±0,8 gerbong, x ±0,38), menghadap depan, setinggi bangku (0,43). Dilihat dari samping: duduk di atas papan bangku.

### Perbaikan dari uji pemilik (2026-10-13, Sonnet 5.5)

Lima keluhan pemilik setelah mencoba `/start`:
1. **Interior camp seperti balok mentah.** Zona dalam ruangan kini punya pembangun sendiri, `start/room.ts` (dipakai `buildZoneScene` bila `map.indoor`). Satu ubin = 1 m di dalam ruangan (`setTileSize`, `M` kini `let` yang dibaca langsung), 2 m di luar. Isinya: lantai papan, karpet batik, dinding plester dengan list lantai dan plafon, plafon yang hanya terlihat dari dalam (dari atas kamera menembusnya), dua lampu gantung berlampu sungguhan, jendela bertirai, kasur (kepala kasur, bantal, selimut batik), lemari berpintu dua, meja belajar dengan buku, lampu, dan kursi, rak buku lima tingkat, papan info gabus, tanaman, keset, kusen pintu. Dinding di sisi kamera disembunyikan (`cull`). Kamera di ruangan lebih tinggi (pitch 0,62, jarak 7).
2. **Sisi belakang banner hitam.** `withBack()` memasang bidang kedua dengan bahan yang sama menghadap ke belakang untuk papan iklan, poster, tanda gerbang kampung, huruf toko, tanda halte, dan tanda gerobak.
3. **Kamera seperti Roblox/GTA.** Kamera berputar ke belakang pemain saat berjalan maju (tidak bila baru saja digeser jari; tidak bila mundur); kamera tidak menembus dinding (mendekat ke pemain, lalu naik sedikit, kembali pelan bila jalan bebas); di dalam ruangan kamera melihat dari atas. Keluar dari camp mendarat di Kampung Bahasa dengan pohon di depan, bukan dinding.
4. **Jalan di HP lambat.** Joystick hanya mengirim empat arah dengan 2,5 m/s. Kini analog (`setStick`): kecepatan 2,6 m/s di tarikan kecil sampai 6,6 m/s di tarikan penuh; keyboard 4,4 m/s, Shift 7 m/s.
5. **Tombol penuh di HP.** Tombol aksi pindah ke kiri atas (di bawah status), lebih kecil; Grafik jadi ikon ⚙ dan Lemari ikon 👗 (di kolom kanan); ajakan dua pemain tidak lagi ditimpa HUD.

**Belum diuji:** joystick sungguhan di HP (hanya `setStick` dari skrip), interior camp di grafik Hemat/Rendah, FPS ruangan, tombol Tolak/kedaluwarsa. Tidak ada galat konsol di uji skrip.

### Perbandingan dengan `golden/` (2026-10-13, Sonnet 5.5)

Diambil di Kampung Inggris pada layar HP (kerangka beda dari acuan desktop), grafik Sedang.
- `01-overview`: **sama** dalam hal bahan (paving bata, batu alam gerbang, genteng, rumput, palem), arah cahaya, dan bayangan lembut. Bedanya sengaja: peta `/start` dari `WorldMap`, bukan halaman konsep.
- `05-fp-pecel`: **sama** untuk tangan di bawah layar dan eye-level; barang di tangan belum diuji di sini.
- `10-lemari`: **sama** (panel Lemari, Gaya Kartun/Blok/Realis, Simpan/Batal), karakter Realis berbaju batik terlihat.
- `15-senja`, `16-malam`: **rusak, lalu diperbaiki.** Malam jauh lebih gelap daripada acuan karena `Start3D` memberi atmosfer daftar lampu kosong, jadi tiang lampu tidak menerangi tanah. Kini ada empat `PointLight` (dua di Hemat) yang berpindah ke tiang lampu terdekat tiap 0,4 detik; `ZoneScene.lamps` mendaftar posisi tiang. Malam kini tampil dengan kolam cahaya hangat. Kecerahan malam masih lebih redup daripada acuan (acuan tidak memakai kabut malam seberat ini); angka di `atmosphere.ts` tidak diubah.
- `03-salaman`: **sama** (balon dua baris "Nice to meet you! / Senang berkenalan!", kedua karakter berhadapan dengan tangan terulur).
- `04-foto`: **diperbaiki dua kali (2026-10-13).** (1) Kamera dulu di belakang pemain; (2) lalu di samping 3,6 m, dua orang kecil dan miring, tidak seperti acuan. Kini sama dengan konsep: kedua orang berdiri berdampingan menghadap kamera (`selfieSpot`: pemain melangkah 0,62 m di samping lawan, `meYaw`/`yaw` ke kamera), foto diambil 0,95 m di depan titik tengah kepala, setinggi telepon (`snap`). Penyebab foto salah di percobaan pertama: `both()` memutar keduanya saling berhadapan sehingga arah foto menyamping; untuk selfie `both()` tidak dipakai. Hasil: dua wajah besar berdampingan dan telepon di tengah. Wajah pemain masih agak miring ke samping.
- `09-joget`: **sama** (tangan terangkat, goyang); keramaian ikut joget belum diuji.
- `12-blok-koko`, `13-kartun-batik`: **beda lalu diperbaiki.** Pemain tampil membelakangi kamera di Lemari (`meYaw = yaw + π`); di konsep pemain menghadap kamera yang diam (`meYaw = yaw`). Kini wajah dan kartu peserta terlihat. Selebihnya **sama.** Blok berpeci, baju koko, sarung kotak-kotak; Kartun berblangkon dan batik kawung (jarik terlihat). Tombol simpan berubah menjadi "Beli dulu" (dinonaktifkan) selama ada barang yang belum dimiliki, sesuai aturan server.
- `control` (menara kontrol, Kota): batang menara putih menjulang di belakang gedung, tampil. Belum difoto utuh dari depan.
- `souk` (Kairo): **tidak terbukti.** Kamera uji berada di depan atap sehingga layar penuh genteng merah berukuran besar (kotak genteng ± 1 m, jauh lebih besar dari genteng gedung kursus). Skala `roofMat` pada `souk` dan `airport` perlu dicek ulang dari sudut jalan. Ulangi dengan kamera lebih jauh.
- Belum dibandingkan: `02`, `06`–`08`, `11`, `14`, `phone-*`.

### Kinerja `/start` (2026-10-13, Sonnet 5.5)

`renderer.info` di titik awal, dengan keramaian lokal (8–12 orang), GPU Intel HD 4000:

| Lokasi | Tinggi | Sedang | Rendah | Hemat |
|---|---|---|---|---|
| Kampung Bahasa (`en`), draw call | 570 | 631 | 324 | 323 |
| segitiga | 359 rb | 392 rb | 185 rb | 185 rb |
| Kota, draw call | 341 | 341 | 147 | 146 |
| segitiga | 212 rb | 212 rb | 101 rb | 101 rb |

Semua di bawah batas (Rendah ≤ 350 / 200 rb, Tinggi ≤ 1.000 / 450 rb). Dua hal yang perlu dicek: Hemat hampir sama dengan Rendah (bedanya hanya jarak gambar orang dan bayangan, bukan geometri), dan di Kota Sedang sama dengan Tinggi. Keduanya mungkin disengaja; konfirmasi di P10-010. FPS di HP sungguhan belum diukur.

### Delapan bentuk gedung (2026-10-13, Sonnet 5.5)

`start/buildings.ts` kini punya model untuk `tower` (17 gedung), `palace` (11), `mall`, `airport`, `control`, `pagoda` (2), `souk`, dan `madrasa` (2); tidak ada lagi bentuk yang jatuh ke aula polos. `tsc` dan `eslint` bersih. **Dilihat di peramban (2026-10-13, Hemat):** `palace` di Kampung Mandarin (dinding merah, atap emas) dan `madrasa` di Kampung Arab (serambi lengkung, kubah hijau) tampil benar, tanpa galat. Di Kota dan Beijing: `pagoda` (tingkat merah, atap emas), `tower` (kotak abu dengan pita kaca, di belakang kerumunan), `mall` (papan "MAL KOTA") dan `airport` tampil, tanpa galat. Atap bandara dan mal dari sudut tinggi tampak seperti hamparan genteng merah yang sangat luas; skala genteng belum dibandingkan dengan acuan. **Belum dilihat:** `control` (menara kontrol) dan `souk`. Varian (`variant`: cn, jp, kr, gb, glass, hotel, flats) belum dibedakan, semua memakai model dasar yang sama dengan warna dari `roofColor` dan `wallColor`. Cek tampilan, draw call, dan varian masuk P10-010.

**Keputusan terbuka (butir 3):** `/play` kini mengabaikan ajakan dari pemain 3D (pengirim melihat "Belum mau" setelah 15 dtk?). Sebenarnya pengirim tidak mendapat `social_no` saat kedaluwarsa kecuali penerima menjawab; perlu dipilih: pesan kecil di `/play` atau diabaikan.
