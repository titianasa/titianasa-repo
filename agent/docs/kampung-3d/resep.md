# Resep Kampung Bahasa 3D

Langkah baku untuk pekerjaan yang berulang. Ikuti urutannya.

- **Kalau resep tidak cukup:** berhenti dan tanyakan, jangan mengarang gaya baru.
- **Semua angka:** [`panduan-gaya.md`](panduan-gaya.md).
- **Tempat berkas:** [`arsitektur.md`](arsitektur.md) §2.

## Aturan umum (berlaku di setiap resep)

1. **Ukuran nyata dalam meter.** Pintu 0,9–1,0 × 2,1 m, jendela 1,0 × 1,25 m, dinding satu lantai 3 m, plint 0,4 m, bangku 0,45 m, meja 0,75 m.
2. **Material:**
   - Pakai `MeshStandardMaterial` lewat pembantu yang ada (`paint`, `tex`, `mat`, `cloth`).
   - **Jangan** `MeshBasicMaterial`, kecuali untuk bayangan bulat dan riak.
   - **Jangan** `flatShading`.
   - Dinding, lantai, atap, jalan, dan rumput **selalu** bertekstur (`textures.ts`), pada ukuran per meter yang ada di panduan §3.
3. **Tekstur baru:** tambahkan fungsi pelukis di `textures.ts`, pola yang sama dengan yang ada:
   - `painted(key, w, h, paint)`, berulang tanpa sambungan (pakai `wrapped`).
   - Sebutkan ukurannya dalam meter di komentar.
   - **Tidak boleh memuat file gambar.**
4. **Geometri:**
   - Balok dengan `block(w, h, d, …)` (`boxUV`), bukan `BoxGeometry` yang diskalakan.
   - Atap dengan `hipRoof` atau `gableSlopes` + `faceUV`.
   - Batang dengan `rod`.
   - Kurva dengan `LatheGeometry` atau `TubeGeometry`.
5. **Bagian yang bergerak** (pintu, roda, bendera, kipas, tuas) adalah `Group` tersendiri. Mesh yang berubah bentuk sendiri diberi `userData.keep = true`. Sisanya biarkan digabung `mergeStatic`.
6. **Bayangan:**
   - Benda di atas tanah `castShadow = true`.
   - Bidang tanah, papan nama, dan kaca `castShadow = false`.
   - Semuanya `receiveShadow = true`.
7. **Detail Indonesia/Pare** (panduan §3, daftar bawah): pakai sebanyak yang masuk akal untuk bangunan itu.
8. **Selesai berarti:**
   - `npx tsc --noEmit` dan `npx eslint` bersih;
   - QA visual sesuai [`qa.md`](qa.md);
   - anggaran draw call tidak terlampaui.

## Menambah barang pakaian atau aksesori

1. **`game3d/catalog.ts`:** tambahkan `Item` di slot yang benar.
   - `id` huruf kecil tanpa spasi; `name` bahasa Indonesia.
   - `tier` dan `price`; `lokal: true` bila pakaian Indonesia.
   - Penanda: `coversHair`, `skirt`, `longSleeves` sesuai jenisnya.
2. **`game3d/avatar.ts` → `buildAvatar`:** tambahkan cabang di bagian slot itu. Ketentuan bentuk:
   - Ukur dari `s` (spec gaya), **bukan dari angka tetap**, supaya pas di Kartun, Blok, dan Realis.
     - Tinggi pakai `s.torsoY`, `s.torso`, `s.chestY`.
     - Permukaan depan dada pakai `front(y)`.
     - Bahu pakai `s.shX`, `s.armR`.
     - Kepala pakai satuan `unit` dan `surf(x, y)`.
     - Bila gayanya kaleng (Blok), kalikan `hw`.
   - Kain bermotif lewat `cloth(hex, kind)`; tambah motif baru di `textures.ts`.
   - Bagian yang menempel pada tungkai atau lengan dimasukkan ke `Group` sendi itu (`hip`, `knee`, `sh`, `el`, `hand`), supaya ikut bergerak.
3. Bila memengaruhi bagian lain (menutup rambut, mengganti kaki dengan rok), pakai penanda di `Item`. Jangan memeriksa `id` di banyak tempat.
4. **`toPixelLook`:** tambahkan padanan pixel terdekat untuk barang itu.
5. **Ekspor katalog ke server** (setelah P10-008): `bun scripts/wardrobe.ts --write`.
6. **QA:**
   - Di Lemari, pakai barang itu di **ketiga gaya**, dengan dua warna, dan bersama jilbab maupun tanpa.
   - Simpan tangkapan layar di tiket.
   - Periksa tidak ada yang menembus badan saat jalan, duduk, dan joget.

## Menambah bangunan berdasarkan denah pixel

1. Cari bangunannya di `buildZone(id).buildings` (`kind`, `style`, `label`, posisi, lebar, pintu) dan lihat dari atas dengan `bun scripts/check-map.ts <zona> --ascii`.
2. **Pilih arketipe** di `game3d/kit/`. Bila belum ada yang cocok:
   - buat fungsi baru `kit/<nama>.ts` dengan tanda tangan `(g: Group, plot: Plot, opts) => Collider[]`;
   - `Plot` = kotak petak dalam meter, arah pintu, ubin pintu.
3. **Bentuk:**
   - Ukuran nyata di dalam petak, pintu tepat di ubin `door`.
   - Plint batu alam 0,4 m, dinding plester, kolom sudut putih, ring balok putih, atap genteng (`roofColor` sebagai rona), papan nama dari `label` dengan `T.board`, jendela dengan teralis.
   - Ruko memakai rolling door dan kanopi.
   - Warung memakai atap seng dan terpal.
4. **Interaksi:** jangan buat aturan baru. Objek di depan pintu (`MapObject`) sudah membawa `kind` yang dibuka Game.tsx.
5. **Kembalikan collider** sesuai bentuk dinding (bukan seluruh petak), supaya teras dan halaman bisa diinjak.
6. **QA:**
   - Tangkapan layar dari depan pada jarak kamera 6 m dan dari atas (pitch 0,55, jarak 17).
   - Bandingkan dengan gambar acuan gedung kursus (`golden/01-overview.jpg`) untuk kesan material dan cahaya.
   - Catat draw call sebelum dan sesudah. Satu bangunan biasa sebaiknya **≤ 12 draw call** setelah digabung.

## Menambah warga (NPC berlabel)

1. Warga berasal dari `map.npcs` (pixel), jadi tambahkan di sana dulu. Pixel dan 3D sama-sama mendapatkannya.
2. **Penampilan 3D:** `fromPixelLook(npc.look)` lalu ditimpa bila perlu, di tabel `NPC_LOOK3D[npc.id]` di `game3d/people.ts`.
   - Penjual memakai celemek (aksesori baru bila belum ada).
   - Pedagang keliling membawa gerobak atau pikulan (properti di `kit/`).
3. Label nama melayang memakai teks `npc.label`.
4. Dialog dan tugas tetap dari pixel (`npcHasTask`, `NpcDialog`).

## Menambah emote

1. `catalog.ts → EMOTES`: `{ id, name, icon }`.
2. `avatar.ts → poseFor`: tambahkan `case` dengan sudut target. Ikuti konvensi panduan §2.6. Ubah hanya sendi yang perlu; bagian lain tetap dari gerak dasar.
3. `avatar.ts → animateHands`: pose tangan orang pertama untuk emote itu.
4. Lamanya dicatat di `ACT_SECONDS` (engine).
5. Bila emote menjadi barang toko, tambahkan ke katalog di slot `emote` (P10-008) dan periksa kepemilikan sebelum dipakai.
6. **QA:** tangkapan layar orang ke-3 dan orang ke-1 di tengah gerakan.

## Menambah interaksi

Tentukan jenisnya dulu:

| Jenis | Contoh | Di mana aturannya |
|---|---|---|
| Ada akibat ekonomi atau progres | beli, sewa, tidur, tiket, belajar | **server dan Game.tsx yang sudah ada.** 3D hanya memanggil `onInteract` di `MapObject` terkait, lalu memutar animasi saat jendela dibuka atau setelah server berhasil |
| Tampilan saja | duduk, baca, lempar koin, hormat bendera | `game3d/interact.ts`, tanpa server |
| Dengan pemain sungguhan | salaman, tos, ngobrol, foto | **ajakan lewat hub** (P10-009): kirim ajakan, tunggu terima, lalu kedua klien memutar animasi yang sama |
| Dengan warga dan pemain komputer | sapa, ngobrol, salaman, tos, foto | `interact.ts`, warga membalas otomatis |
| Dengan kerumunan dummy | — | **tidak ada** (ADR-0023 §7.3) |

Langkah:
1. Tambahkan pemeriksaan di `findPrompts` (jarak dan syarat) dengan `{ id, label, icon }`. Label pendek bahasa Indonesia; harga ditulis `· Rp5.000`.
2. Tambahkan `case` di `act(id)`. Bila butuh pose, pakai aksi yang ada atau tambahkan seperti emote.
3. Balon kalimat dari warga: bahasa yang dipelajari + arti Indonesia (`say(who, en, idn, detik)`).
4. **QA:** dekati, pastikan tombolnya muncul sebagai aksi utama atau tambahan, tekan, lalu ambil tangkapan layar di tengah aksi.

## Menambah atau mengubah tingkat grafik

1. Ubah tabel panduan §5 dulu.
2. Terapkan di `scene.setQuality`, `engine.setQuality`, dan `people.cull`.
3. Ukur keempat tingkat (`bun scripts/qa/3d.ts --perf`) dan tulis angkanya di tiket.
