# Misi Inggris dan peta baru (audit 2026-10-07)

Peta Kampung Inggris dan Zona Umum sudah dibangun ulang (ADR-0021). Dokumen ini mencocokkan misi Basic dan A1 yang sudah ada, serta rencana A2–C2 (`journey/en/world.ts`), dengan tempat dan warga yang kini benar-benar ada di peta. Tidak ada kode misi yang diubah; ini daftar usulan untuk diputuskan.

## 1. Yang ada di peta sekarang

**Kampung Inggris (79×60)**: ENGLISH ACADEMY (kampus, patung singa kembar), LIBRARY, GUESTHOUSE, CAFÉ, MINIMART, LAUNDRY, POST OFFICE, DINER, THE BROWNS' HOUSE, PRIMARY SCHOOL, TOURIST INFO, MARKET (4 los), menara jam "Big Ben" dengan dua air mancur, taman bermain (ayunan, perosotan), halte bus, 2 gerobak (Fred: fish & chips, Molly: ice cream) dan Mas Eko si es krim keliling, 8 billboard, 4 halte kereta kelinci, dan di belakang kampus: sungai (memancing), sawah dengan orang-orangan sawah, taman bunga.
Warga: Kate, Tom, Oliver, Mrs. Brown, Green, Hughes, Smith, Grey, Lily, Jones, Anna, Mr. Brown, Emma, Jack, Patel, Fred, Molly, tiga warga umum.

**Zona Umum (111×76)**: Bandara besar + menara kontrol (Kapten Dedi), Museum Bahasa (Bu Kurator), Kantor Imigrasi, Bank Kampung (Bu Teller), Kantor Pos, Bioskop, Barbershop, Salon, Sekolah Dasar, masjid, gereja Protestan, gereja Katolik, pura, vihara & klenteng, Terminal Bus, Stasiun Kereta, Perpustakaan, Minimarket, Pasar Pare, Speaking Club, Language Challenge, Balai Desa, Puskesmas, Sewa Sepeda, warung, warkop, camp putra dan putri, lapangan, taman, danau, 4 halte kereta kelinci. Tempat yang punya kuis (venue) memberi 12 XP sekali sehari.

## 2. Temuan pada misi yang sudah ada

Petunjuk lokasi di kartu misi (`EN_PLACES`) masih cocok dengan peta baru: posisi Kate, Tom, Brown, Green, Hughes, Smith, Grey (dekat air mancur), Jones, Anna, Lily, Emma, Jack, Mr. Brown dan Patel sudah dicek terhadap koordinat NPC. Dua hal kecil: Tom "di sebelah barat kampus" sebenarnya di ujung barat di luar LIBRARY, dan gerbang ke Zona Umum kini di tengah selatan.

Yang belum dipakai misi sama sekali, padahal sekarang ada: THE BROWNS' HOUSE, PRIMARY SCHOOL, TOURIST INFO, MARKET, gerobak Fred/Molly, billboard, sungai/sawah/taman bunga, halte kereta kelinci, dan seluruh Zona Umum.

## 3. Usulan penyesuaian Basic dan A1 (peta Kampung Inggris)

| Misi | Sekarang | Usulan dengan tempat baru |
|---|---|---|
| en-0-numbers Belanja pertama | beli di kafe/minimart | tambah satu langkah menanyakan harga ke Fred (fish & chips) atau Molly (ice cream); angka dan harga yang nyata |
| en-0-food Makan siang pertama | kafe + diner | tambah MARKET: sebut buah/sayur di los pasar (kata makanan Basic) |
| en-0-travel Turis tersesat | antar Anna ke kafe dan taman | tambah TOURIST INFO sebagai tujuan ketiga, dan baca satu billboard bersama Anna |
| en-0:villager:jones Papan petunjuk | papan petunjuk | pakai signpost dan billboard yang nyata di plaza |
| en-1-family Pohon keluarga | bicara di minimart/taman | langkah `pergi` ke THE BROWNS' HOUSE untuk menerima foto; keluarga bertemu di rumahnya |
| en-1-school Survei kelas | di perpustakaan dan taman | pindahkan survei Emma dan Jack ke PRIMARY SCHOOL (ada bangunannya; `place: school` sudah dipakai) |
| en-1-city Kurir Mr. Patel | antar surat ke laundry | rute tiga alamat: GUESTHOUSE, PRIMARY SCHOOL, TOURIST INFO; kata depan tempat (next to, opposite, between) dan satu langkah naik kereta kelinci dari halte |
| en-1-market Belanja untuk pesta | diner lalu minimart | belanja di MARKET (los buah, los sayur): how much / how many, countable dan uncountable |
| en-1-doing Fotografer taman | foto taman dan Emma/Jack | foto-foto dari belakang kampus: orang memancing di sungai, petani di sawah, tukang es krim; kalimat present continuous dari adegan nyata |
| en-1-yesterday Tas Emma hilang | tanya Smith dan Lily | garis waktu kemarin mencakup sungai atau taman bunga (tas ditemukan di tepi sungai) |
| en-1-calendar Janji temu | kalender wisma | tambah papan jadwal halte kereta kelinci (jam kereta, at/on/in) |
| en-1-weather Laporan cuaca | kartu pos dan Lily | pengamat cuaca di sawah atau sungai |

Catatan: setiap langkah baru berarti klip audio baru (`generate.ts en 0/1`, lalu `upload.ts`); unggah ke bucket R2 bersama perlu persetujuan.

## 4. A2–C2: tempat rencana → tempat nyata

Rencana A2–C2 memakai tempat yang belum ada di peta (status "baru"). Sebagian besar sudah punya padanan di Zona Umum, sehingga A2 bisa langsung berjalan di peta nyata, bukan adegan terpisah.

| Level | Tempat rencana | Padanan di peta |
|---|---|---|
| A2 Pusat kota | station | STASIUN KERETA (Zona Umum, Mr. Khan menggantikan Pak Masinis) |
| | clinic | PUSKESMAS |
| | bank | BANK KAMPUNG |
| | travel agency | TERMINAL BUS atau BANDARA |
| | netcafe | PERPUSTAKAAN Zona Umum atau SPEAKING CLUB |
| | museum | MUSEUM BAHASA (dan kuis venue) |
| | police | BALAI DESA (Pak RT) |
| | seaside hotel, bandara kecil | BANDARA besar, tiket perjalanan nyata |
| | mall (kerja paruh waktu) | PASAR PARE / MINIMARKET; belum ada toko pakaian |
| | tambahan yang belum direncanakan | BIOSKOP (ulasan film), BARBERSHOP dan SALON (mendeskripsikan penampilan), SEWA SEPEDA (harga, deposit), KANTOR POS |
| B1 Media & kampus | townhall | BALAI DESA |
| | infodesk | TOURIST INFO (Kampung Inggris, sudah ada) |
| | natpark | sungai, sawah, taman bunga di belakang kampus |
| | roastery | CAFÉ Tom |
| | newsroom, radio | belum ada: perlu gedung baru di Zona Umum (usul dekat BIOSKOP) |
| B1→B2 keberangkatan | bandara, imigrasi | BANDARA dan KANTOR IMIGRASI sebagai adegan berangkat ke London |
| B2 | union, debate club | SPEAKING CLUB dan LANGUAGE CHALLENGE |
| B2–C2 budaya | tempat ibadah | lima rumah ibadah untuk topik antaragama dan tradisi |
| C2 | mentorhall (Balai Mentor di Pare) | bangunan di Kampung Inggris, usul LIBRARY sayap timur atau TOURIST INFO |
| London (tingkat 4–6) | flat, campus, council, office… | tetap adegan; tidak ada padanan di peta |

## 5. Hal yang harus diputuskan sebelum menulis misi

1. **Bahasa warga Zona Umum.** Warga di sana berbahasa Indonesia (Mas Doni, Bu Sri…). Misi Inggris di Zona Umum memerlukan warga berbahasa Inggris. Pilihan: warga baru berbahasa Inggris di tempat yang dipakai misi (Dr. Shaw di PUSKESMAS, Mr. Khan di STASIUN, dan seterusnya), atau memakai SPEAKING CLUB sebagai tempat berbahasa Inggris saja.
2. **Warga A2+ belum ada sebagai NPC peta**: Shaw, Clarke, Khan, Lee, Maya, Reed, Max, Evans, Wood, Sam. Perlu ditempatkan di bangunan yang ada.
3. **Newsroom dan radio (B1)** belum punya gedung.
4. **Status tempat di `world.ts`**: tempat yang sudah ada di peta (school, post, guesthouse, library, playground, station, clinic, bank, museum, infodesk) masih bertanda "baru". Perlu diubah ke "ada", dengan penyesuaian pemeriksaan `bun scripts/journey.ts`.
5. **B2–C2 isi pelajarannya belum ditulis** (7.000 kata, 72 konsep); misi mengikuti setelah isinya ada.
6. Misi di Zona Umum bisa memakai `zone: "umum"`; server memeriksa zona pemain, jadi tidak perlu perubahan mesin.
