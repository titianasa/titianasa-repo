# ADR-0021 — Kereta kelinci beneran, jalan keliling di semua zona, dan Zona Umum sebagai kota

Status: **K1 dan C1 dikerjakan (2026-10-07)**; K2 (jalan keliling empat kampung kecil) dan C2 (isi fasilitas) belum. Menggantikan kereta kelinci "satu tiket, jalan otomatis" yang dibuat sebelumnya.

## 1. Permintaan

1. Kereta kelinci harus berupa kereta yang benar-benar ditumpangi orang (bukan ditarik satu orang), ada **beberapa** kereta, dan rutenya **mengelilingi semua peta**: Zona Umum dan kelima kampung.
2. Penumpang melihat seluruh pemandangan; di dalam kereta mereka **duduk** (stamina tidak turun) dan kereta **tidak berhenti** karena NPC atau pemain lain di jalan. Kereta hanya berhenti di **halte**.
3. Penumpang pasti banyak: kereta harus konsisten untuk banyak pemain sekaligus.
4. Halte di titik strategis tiap zona (bukan di tengah lapangan). Penumpang naik/turun di halte.
5. Jalan di semua zona didesain ulang supaya ada jalur keliling yang memperlihatkan semua pemandangan.
6. Zona Umum diperlebar: pusat lapangan/taman lebih luas, area belakang gapura lebih luas, dan diisi fasilitas kota yang menyebar dan tertata: terminal, bandara, stasiun, sekolah, rumah ibadah lima agama, bioskop, beberapa taman dan taman bermain, danau, museum, candi, serta fasilitas umum (barber, salon, imigrasi, dan lainnya).

Sudah dikerjakan sebagai langkah awal (2026-10-07): tiket Rp5.000 dari server, `world/tour.ts` + autopilot klien, stasiun di tiap zona, tombol TURUN, penumpang tidak menguras stamina (pesan `seat` di hub realtime), kereta tidak berhenti karena orang. Yang di bawah adalah rancangan penggantinya.

## 2. Kereta: simulasi berbasis jam (tanpa status di server)

Posisi tiap kereta adalah **fungsi murni dari jam**: `trainAt(trainId, nowMs) → { zone, x, y, dir, atStop }` pada satu rute lingkar global. Setiap klien menghitung hasil yang sama dari jam server (sinkron lewat offset waktu yang sudah ada di tick), jadi:

- semua pemain di satu zona melihat kereta yang sama di tempat yang sama, tanpa lalu lintas jaringan;
- N kereta = N fase (`offset = i × T / N`); rute lingkar `T` ≈ 12 menit, 4 kereta → satu kereta lewat tiap halte setiap ~3 menit;
- kereta berhenti di halte `dwell` 15 detik (jam yang sama menentukan kapan berangkat);
- melintasi zona memakai gerbang yang sudah ada (Zona Umum ↔ kampung); kereta "pindah zona" di jam yang sama, jadi pemain di zona tujuan sudah melihatnya muncul dari gerbang.

Rute global: Zona Umum (sisi kota) → gerbang Mandarin → kampung → kembali → Arab → … → Korea → Zona Umum (sisi sungai/bandara) dan seterusnya. Tiap zona punya **jalur keliling** (lihat §4); kereta tidak berbelok masuk gang.

### Penumpang
- Naik: di halte pemain menekan "Naik"; bila ada kereta berhenti di halte itu ia langsung naik, bila tidak ia menunggu ("Kereta berikutnya ± 70 detik") dengan hitung mundur dari jam yang sama. Tiket Rp5.000 dibayar saat naik (satu tiket = sampai turun di halte mana pun, maksimal satu putaran penuh).
- Selama di kereta: karakter duduk (sprite duduk di gerbong), posisinya mengikuti `trainAt` (klien memancarkan `move` seperti biasa supaya pemain lain melihat penumpang di gerbong), pesan `seat` mencegah penghitungan langkah (sudah ada).
- Turun: tombol TURUN ("Turun di halte berikutnya") → di halte karakter diturunkan di petak jalan kaki terdekat.
- Gerbong: lokomotif + 3 gerbong terbuka, tiap gerbong 4 kursi; pemain yang duduk digambar kecil (kepala/badan) di kursi, NPC penumpang pengisi di kursi kosong agar kereta tidak tampak kosong. Bila penumpang > kursi, sisanya berdiri di gerbang (tetap digambar).
- Server hanya: menjual tiket (`POST /pare/train`), mencatat `seat`, dan (opsional) satu event misi "naik kereta kelinci".

## 3. Halte
Tiap zona: 3–5 halte strategis di tepi jalur keliling, ditandai bangunan kecil "HALTE · nama tempat" dan papan jadwal. Kampung (40×30 lama, diperbesar §4): halte Gerbang, Kelas, Taman, Pasar. Kampung Inggris: Gerbang, Kampus (depan), Dermaga/Sawah, Pasar, Stasiun/halte bus. Zona Umum: lihat §5.

## 4. Jalan keliling di semua zona
- **Kampung Inggris (79×60)**: jalur keliling mengikuti jalan raya utara (boulevard), jalan selatan, dan dua lorong barat–timur yang dilebarkan, ditambah ruas sungai/sawah di belakang kampus; halaman kampus dan plaza tetap area pejalan kaki.
- **Kampung Mandarin/Arab/Jepang/Korea (40×30)**: peta diperluas (≈ 64×44) dengan jalan lingkar di tepi, jalan raya tengah, dan satu "pemandangan besar" tiap kampung di sisi lingkar (kuil/masjid-tempat-landmark, taman, pasar); NPC dan bangunan lama dipertahankan di tengah.
- **Zona Umum**: jalan raya utara/selatan (sudah ada) disambung jalan barat/timur menjadi lingkar kota.
Aturan teknis: jalur kereta = rangkaian petak "jalan" (`r`) khusus yang tidak boleh dihalangi dekor; kereta melewati NPC dan pemain, pemain/NPC tidak terblokir (kereta digambar di atas, tidak punya tabrakan).

## 5. Zona Umum sebagai kota (±120×84)
Diperlebar dari 80×46. Pembagian (utara → selatan), simetris di sumbu tengah x = 60:
1. **Gerbang & plaza belakang gapura** (y 0–30): kelima gapura tetap di jalan raya, di belakangnya plaza gerbang yang luas (3× sekarang) dengan alun-alun, patung, dua danau kecil, **museum**, **candi/candi bentar**, taman bunga, amfiteater.
2. **Lapangan & taman pusat** (y 30–52): lapangan dilebarkan (≈ 50×18), taman kota dengan air mancur besar, jogging track, dua **taman bermain**, kolam.
3. **Distrik layanan** (y 52–70), menyebar kiri–kanan: **sekolah** dan **kampus kecil**, **bioskop**, **terminal bus**, **stasiun kereta**, **puskesmas**, **kantor imigrasi**, **kantor pos**, **barber**, **salon**, **bank/ATM**, **toko**.
4. **Rumah ibadah** (lima agama di Indonesia) tersebar di sudut yang berbeda dengan halaman masing-masing: masjid, gereja (Protestan), gereja Katolik, pura, vihara (+ klenteng) — Konghucu mengikuti vihara/klenteng di sudut yang sama.
5. **Bandara & tepi sungai** (y 70–84): bandara kecil di timur laut, danau/sungai membentang di selatan, dermaga memancing (sudah ada), Camp Putra/Putri dan penyewaan sepeda tetap di tepi barat/timur.
Setiap bangunan punya `kind`, label, NPC penjaga (fasilitas yang punya fungsi: imigrasi/bandara/terminal membuka layar tiket atau info; bioskop/museum/candi membuka cerita pendek + soal bahasa) dan titik misi yang bisa dipakai misi level berikutnya (ADR-0019 P9-012).

## 6. Bertahap
1. **Fase K1 (kereta v2, Kampung Inggris + Zona Umum lama)**: `trainAt`, gerbong dengan penumpang, 2–4 kereta, halte, jalur keliling di dua zona itu; hapus autopilot.
2. **Fase K2 (empat kampung)**: perbesar peta, jalur keliling, halte.
3. **Fase C1 (Zona Umum kota)**: lebarkan peta, tambah fasilitas bertahap per distrik, NPC, billboard slot, minimap.
4. **Fase C2**: konten fasilitas (museum, candi, bioskop, imigrasi) dan misi.

## 7. Risiko
- Sinkron jam klien–server: pakai `offset` dari respons tick (±2 detik cukup; kereta bergerak 7 petak/detik jadi selisih 2 detik ≈ 14 petak; perlu offset akurat, kereta digambar dengan interpolasi dari jam sinkron).
- Ukuran peta dan `clampCoord` (sudah 127) serta jumlah titik di minimap.
- Banyak penumpang: batasi gambar penumpang ke 12 per kereta (sisanya angka "+n").

## 8. Yang sudah dibangun (2026-10-07)
- `world/trains.ts`: rute global, 4 kereta berbasis jam (`trainState`), 20 perhentian per putaran, halte (`HALTE`) di Zona Umum, Kampung Inggris, dan empat kampung; `scripts/check-trains.ts` memeriksa rute terhadap peta nyata.
- Mesin: kereta digambar dengan lokomotif + 3 gerbong terbuka, penumpang duduk (pemain sendiri, pemain lain di petak gerbong, dan penumpang pengisi); penumpang mengikuti kereta lintas zona (`engine.boardTrain`, `onRideZone`); kereta menembus orang (tidak berhenti); `seat` ke hub membuat langkah tidak dihitung.
- Game: halte (`kind: "train"`) membuka modal jadwal ("kereta berikutnya ± n detik"), tunggu di halte, tiket Rp5.000 dipotong saat naik, TURUN di halte berikutnya.
- Kampung Inggris: jalan lingkar (belakang kampus, sisi barat dan timur, jalan selatan) dan 4 halte.
- Zona Umum 111×76 (`world/kota.ts`): lapangan diperdalam, area belakang gapura (danau + dermaga, candi dengan kolam, museum, taman bermain, taman bunga), jalan belakang dengan barber, salon, bioskop, kantor imigrasi, bank, kantor pos, jalur barat (sekolah, masjid, gereja Protestan, gereja Katolik, pura) dan timur (bandara, terminal bus, stasiun kereta, vihara & klenteng). Tempat-tempat itu objek `venue` (modal info + frasa) dengan penjaga.
Belum: jalan lingkar dan peta lebih luas untuk Mandarin/Arab/Jepang/Korea (K2), sinkron jam server untuk kereta (sekarang jam perangkat), isi interaktif fasilitas (C2), billboard di distrik baru.

### Pembaruan (2026-10-07, setelah permintaan lanjutan)
- Museum Bahasa sekarang di tengah (tempat candi), candi dihapus; kolam pantul dan patung tetap. Bandara besar di timur laut (terminal, menara kontrol, apron dengan tiga pesawat, landasan), bandara kecil di lajur timur diganti taman bermain timur. Kantor imigrasi ada di jalan pelayanan.
- K2 selesai dengan cara lain: keempat kampung (Mandarin, Arab, Jepang, Korea) memakai tata letak yang sama dengan Kampung Inggris (`buildGrandVillage` di `world/english.ts`, 79×60): kampus besar bertuliskan nama kampung di atap (menyala malam), perpustakaan, wisma, kantor pos, rumah warga, sekolah, info wisata, taman bermain, pasar, halte bus, sawah dan taman bunga di belakang kampus, sungai dengan dermaga, jalan lingkar dan 4 halte. Label bangunan memakai kosakata bahasa tiap kampung, bendera tiap negara, dan landmark kampung di plaza.

### Pembaruan 2 (2026-10-07): jam server dan isi fasilitas
- **Jam server:** `GET /pare/time` (publik, `{now_ms}`); `serverClockSkew()` (game/src/game/server.ts) mengambil tiga sampel dan memakai yang round trip-nya terpendek; dipasang ke `engine.clockSkew` saat buka game dan tiap 5 menit. Diuji: dengan jam halaman sengaja maju 40 detik, selisih terukur −40.001 ms.
- **Isi fasilitas:** 16 tempat di Zona Umum (museum, sekolah, masjid, gereja, katedral, pura, vihara, bioskop, barber, salon, imigrasi, bank, kantor pos, bandara, terminal, stasiun) masing-masing punya kunjungan singkat (`VENUES[id].quiz` di `world/kota.ts`, 2–3 butir: orang di sana berkata, pemain memilih jawaban; salah tidak mengurangi apa pun dan jawaban benar ditampilkan). `VenueModal.tsx` menjalankannya dan melaporkan `venue:<id>`; server (`RecordEvent` di daily.go) memberi 12 XP + Rp600 sekali sehari per tempat dan menghitung event untuk misi harian. Tes: `TestVenueVisitPaysOncePerDay`; e2e: `scripts/e2e/venue.ts`.
