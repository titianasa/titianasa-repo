# Misi Inggris dan peta baru (audit 2026-10-07)

> **Pembaruan 2026-10-07 (ADR-0022).** Keputusan §5.1 sudah diambil: warga Kampung Bahasa berbicara lima bahasa, tidak ada warga baru khusus Inggris. Kota dan lima negara tujuan kini peta sendiri (`kota`, `gb`, `cn`, `eg`, `jp`, `kr`), bandara pindah ke kota, dan bekas bandara di Kampung Bahasa menjadi Candi Bahasa. Bagian 1, 4 dan 5 di bawah sudah disesuaikan; bagian 2 dan 3 (misi Basic dan A1 di Kampung Inggris) tidak berubah.

Peta Kampung Inggris dan Kampung Bahasa sudah dibangun ulang (ADR-0021). Dokumen ini mencocokkan misi Basic dan A1 yang sudah ada, serta rencana A2–C2 (`journey/en/world.ts`), dengan tempat dan warga yang kini benar-benar ada di peta. Tidak ada kode misi yang diubah; ini daftar usulan untuk diputuskan.

## 1. Yang ada di peta sekarang

**Kampung Inggris (79×60)**: ENGLISH ACADEMY (kampus, patung singa kembar), LIBRARY, GUESTHOUSE, CAFÉ, MINIMART, LAUNDRY, POST OFFICE, DINER, THE BROWNS' HOUSE, PRIMARY SCHOOL, TOURIST INFO, MARKET (4 los), menara jam "Big Ben" dengan dua air mancur, taman bermain (ayunan, perosotan), halte bus, 2 gerobak (Fred: fish & chips, Molly: ice cream) dan Mas Eko si es krim keliling, 8 billboard, 4 halte kereta kelinci, dan di belakang kampus: sungai (memancing), sawah dengan orang-orangan sawah, taman bunga.
Warga: Kate, Tom, Oliver, Mrs. Brown, Green, Hughes, Smith, Grey, Lily, Jones, Anna, Mr. Brown, Emma, Jack, Patel, Fred, Molly, tiga warga umum.

**Kampung Bahasa (111×76)**: Candi Bahasa, cagar budaya (Pak Juru), Museum Bahasa (Bu Kurator), Kantor Imigrasi, Bank Kampung (Bu Teller), Kantor Pos, Bioskop, Barbershop, Salon, Sekolah Dasar, masjid, gereja Protestan, gereja Katolik, pura, vihara & klenteng, Terminal Bus, Stasiun Kereta, Perpustakaan, Minimarket, Pasar Pare, Speaking Club, Language Challenge, Balai Desa, Puskesmas, Sewa Sepeda, warung, warkop, camp putra dan putri, lapangan, taman, danau, 4 halte kereta kelinci. Terminal Bus dan Stasiun Kereta menjual tiket ke kota. Tempat yang punya kunjungan (venue) memberi 12 XP sekali sehari; orang di sana berbicara dalam bahasa yang sedang dipelajari pemain.

**Kota (zona `kota`, 120×90)**, bus atau kereta Rp7.000 dari Kampung Bahasa: Bandara Internasional + menara kontrol (Kapten Dedi) + Kantor Imigrasi, Universitas Kota (Bu Dosen), Menara Bahasa (perkantoran, Mbak Sekar), Bank Kota, Hotel Kota (Mas Reza), Balai Kota + alun-alun dan Tugu (Pak Wali), Mal Kota (Mbak Lala), Sekolah Kota, Perpustakaan Kota, Taman Kota + danau, Masjid Agung, Bioskop, Rumah Sakit (Dokter Rina), apartemen, Kantor Pos, Rumah Makan, Kedai Kopi, Minimarket, Pasar Kota, Katedral, Klenteng, Museum Kota, Sewa Sepeda, Stasiun Kota, Terminal Bus Kota, Speaking Club, Language Challenge. Semua warganya lima bahasa.

**Negara tujuan (72×56 masing-masing)**, pesawat Rp100.000 dari bandara kota: London `gb`, Beijing `cn`, Kairo `eg`, Tokyo `jp`, Seoul `kr`. Tiap negara: bandara, imigrasi, universitas (kelas), hotel, museum, restoran, kafe, toko, pasar, taman, dan landmark khas. Hanya bahasa negara itu yang dipakai.

## 2. Temuan pada misi yang sudah ada

Petunjuk lokasi di kartu misi (`EN_PLACES`) masih cocok dengan peta baru: posisi Kate, Tom, Brown, Green, Hughes, Smith, Grey (dekat air mancur), Jones, Anna, Lily, Emma, Jack, Mr. Brown dan Patel sudah dicek terhadap koordinat NPC. Dua hal kecil: Tom "di sebelah barat kampus" sebenarnya di ujung barat di luar LIBRARY, dan gerbang ke Kampung Bahasa kini di tengah selatan.

Yang belum dipakai misi sama sekali, padahal sekarang ada: THE BROWNS' HOUSE, PRIMARY SCHOOL, TOURIST INFO, MARKET, gerobak Fred/Molly, billboard, sungai/sawah/taman bunga, halte kereta kelinci, dan seluruh Kampung Bahasa.

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

Rencana A2–C2 memakai tempat yang belum ada di peta (status "baru"). Sejak ADR-0022 hampir semuanya punya padanan nyata: pusat kota A2 dan distrik B1 di zona `kota`, London di zona `gb`. Kolom kanan menyebut zonanya.

| Level | Tempat rencana | Padanan di peta |
|---|---|---|
| A2 Pusat kota | station | STASIUN KOTA (`kota`, Pak Masinis berperan sebagai Mr. Khan); naik kereta sungguhan dari Stasiun Pare |
| | clinic | RUMAH SAKIT KOTA (`kota`, Dokter Rina) atau PUSKESMAS (`umum`) |
| | bank | BANK KOTA (`kota`) |
| | travel agency | BANDARA INTERNASIONAL (`kota`): jendela tiket dan imigrasi nyata |
| | netcafe | PERPUSTAKAAN KOTA (`kota`) |
| | museum | MUSEUM KOTA (`kota`) |
| | police | BALAI KOTA (`kota`, Pak Wali) |
| | seaside hotel, bandara kecil | HOTEL KOTA dan BANDARA INTERNASIONAL (`kota`) |
| | mall (kerja paruh waktu) | MAL KOTA (`kota`, Mbak Lala) |
| | tambahan yang belum direncanakan | BIOSKOP KOTA (ulasan film), MENARA BAHASA (wawancara kerja), UNIVERSITAS KOTA; di `umum`: BARBERSHOP, SALON, SEWA SEPEDA, KANTOR POS, CANDI BAHASA (aturan cagar budaya) |
| B1 Media & kampus | townhall | BALAI KOTA (`kota`) |
| | infodesk | TOURIST INFO (Kampung Inggris, sudah ada) |
| | natpark | sungai, sawah, taman bunga di belakang kampus; CANDI BAHASA dan hutannya (`umum`) |
| | roastery | CAFÉ Tom atau KEDAI KOPI (`kota`) |
| | college | UNIVERSITAS KOTA (`kota`, Bu Dosen berperan sebagai Dr. Evans) |
| | newsroom, radio | belum ada gedungnya; MENARA BAHASA atau KANTOR di baris 4 (`kota`) bisa dipakai sebagai kantor Kampung Post |
| B1→B2 keberangkatan | bandara, imigrasi | BANDARA INTERNASIONAL (`kota`): penerbangan nyata ke London dengan pemeriksaan imigrasi |
| B2 | union, debate club | SPEAKING CLUB dan LANGUAGE CHALLENGE (`umum` atau `kota`) |
| B2–C2 budaya | tempat ibadah | lima rumah ibadah di `umum`; Masjid Agung, Katedral, Klenteng di `kota` |
| C2 | mentorhall (Balai Mentor di Pare) | bangunan di Kampung Inggris, usul LIBRARY sayap timur atau TOURIST INFO |
| London (tingkat 4–6) | campus | UNIVERSITY OF LONDON (`gb`, kelas) |
| | council, committee | HOUSES OF PARLIAMENT (`gb`, tempat kunjungan) |
| | southbank | tepi Thames dengan LONDON EYE dan TOWER BRIDGE (`gb`) |
| | embassy, publisher, office, flat, court… | belum ada gedungnya di `gb`; tetap adegan sampai ditambahkan (GRAND HOTEL dan BRITISH MUSEUM sudah ada) |

### 4a. A2 sudah ditulis (2026-10-09)

Ke-25 misi A2 (`missions/en2.ts`, `en2-villagers.ts`, `en2-big.ts`) memakai nama warga peta, bukan nama tokoh rencana: Pak Masinis, Mbak Lala, Dokter Rina, dan seterusnya. Warga Kampung Bahasa dan Kota bisa lima bahasa (ADR-0022), jadi di misi mereka berbahasa Inggris. Kunci warga kota berawalan `kota-` supaya tidak bertabrakan dengan warga Kampung Bahasa.

| Bab | Misi | Pemberi | Peta |
|---|---|---|---|
| 1 Pindah ke kota | Buku harian minggu pertama | Miss Kate | Kampung Inggris → naik bus/kereta → Kota (Terminal, Mbak Tia, Rumah Makan) |
| 2 Saat itu terjadi | Saksi mata | Pak Satpam | Kota: Mal Kota, Bioskop, Rumah Sakit |
| 3 Dulu & sekarang | Album lama kota | Bu Kurator | Kampung Bahasa: Museum Bahasa, Candi Bahasa (Pak Juru) |
| 4 Belanja pintar | Hadiah dengan anggaran | Mbak Lala | Kota: Mal Kota |
| 5 Kerja paruh waktu | Hari pertama kerja | Mbak Lala | Kota: Mal Kota |
| 6 Uang & jumlah | Kasir akhir pekan | Mbak Lala | Kota: Mal Kota → Bank Kota (Bu Teller) |
| 7 Sehat-sehat ya | Di klinik | Dokter Rina | Kota: Rumah Sakit, Bioskop (Mas Tiket) |
| 8 Makan di luar | Kritikus kuliner | Chef Oliver | Kampung Inggris (DINER) → Kampung Bahasa (Warung Pecel Bu Sri) |
| 9 Keliling kota | Pemandu wisata sehari | Pak Masinis | Kampung Bahasa: Stasiun → Museum Bahasa → Candi Bahasa |
| 10 Rencana liburan | Agen perjalanan | Kapten Dedi | Kota: Bandara Internasional |
| 11 Di perjalanan | Liburan yang kacau | Pak Masinis (Kota) | Kota: Stasiun Kota → Hotel Kota (Mas Reza) |
| 12 Pengalaman | Bingo pengalaman | Miss Kate | Kampung Inggris (kelas, tiga warga) |
| 13 Hobi & waktu luang | Klub baru | Mrs. Hughes | Kampung Inggris (wisma, Lily, Mr. Smith) |
| 14 Ceritakan! | Malam Cerita | Tom | Kampung Inggris (CAFÉ, tiga tamu) |
| Misi Besar | Gaji pertama, liburan pertama | Mrs. Brown | Kampung Inggris → Kota (stasiun, hotel, rumah makan, rumah sakit, mal) → Kampung Inggris |

Sepuluh misi warga A2 semuanya di Kampung Inggris. Langkah rencana yang belum bisa diperiksa mesin (`tulis`, `komputer`, `telepon`) diganti `dialog`, `baca`, atau `dengar` dengan butir ketik; `bun scripts/missions.ts` mencatat tiap penyimpangan.

### 4b. B1 sudah ditulis (2026-10-09)

Tempat yang dibutuhkan misi tetapi belum ada di peta dibangun baru (keputusan pemilik produk 2026-10-09: peta mengikuti kebutuhan misi). Untuk B1 dibangun **distrik media** di pojok barat daya Kota (`world/city.ts`): kantor **KAMPUNG POST** dengan editornya, Bu Laras (peran Ms. Reed), dan menara **RADIO KOTA** dengan DJ Max, berbagi satu pelataran di sebelah barat Stasiun Kota (menggantikan gedung KANTOR dan MENARA KOTA yang kosong). Dimas, mahasiswa Universitas Kota, menjadi fotografer magang (peran Sam). Kampus, balai kota, dan danau memakai Universitas Kota, Balai Kota, dan Danau Taman Kota yang sudah ada; kebun kopi memakai ladang Pak Tani di selatan Pasar Pare.

| Bab | Misi | Pemberi | Peta |
|---|---|---|---|
| 1 Lamaran magang | Wawancara magang | Bu Laras | Kota: kantor Kampung Post, Dimas di Universitas Kota |
| 2 Masa kecil & kebiasaan | Rubrik Pendatang | Bu Laras | Kota: Kak Lina (Balai Kota), Bu Yanti (Rumah Makan) |
| 3 Kasus barang hilang | Kasus kamera hilang | Dimas | Kota: Perpustakaan, Sekolah Kota, Kantor Pos |
| 4 Layanan & keluhan | Kolom konsumen | Mr. Green | Kampung Inggris: Laundry, Kantor Pos (Mr. Patel) |
| 5 Bertanya dengan sopan | Meja informasi wisata | Pak Sopir | Kampung Bahasa: Terminal Bus |
| 6 Bagaimana dibuat? | Dari kebun ke cangkir | Tom | Kampung Inggris (CAFÉ) → Kampung Bahasa (kebun Pak Tani) → CAFÉ |
| 7 Reporter Kampung | Reporter Kampung | Pak RT | Kampung Bahasa: Balai Desa, Pasar Pare (Mbak Ayu), Pak Joko |
| 8 Tokoh & ulasan | Halaman budaya | Lily | Kampung Inggris: taman, perpustakaan (Mr. Smith) |
| 9 Seandainya… | Rapat balai kota | Pak Wali | Kota: Balai Kota, Taman Kota (Mas Aji) |
| 10 Sehat & bugar | Siaran pagi sehat | DJ Max | Kota: Rumah Sakit (Dokter Rina) → Taman Kota (Mas Aji) → studio Radio Kota |
| 11 Makan & kebiasaan | Dapur sehat Chef Oliver | Chef Oliver | Kampung Inggris: DINER |
| 12 Teknologi & pendapat | Kolom opini | Bu Guru | Kota: Sekolah Kota, Perpustakaan (Mbak Nisa) |
| 13 Rencana & perjalanan | Ekspedisi ke danau | Kak Lina | Kota: Balai Kota, Sewa Sepeda (Mas Heru), dermaga Danau Taman Kota |
| 14 Obrolan sehari-hari | Hari sibuk di ruang redaksi | Bu Laras | Kota: kantor Kampung Post, Kantor Pos, Kedai Kopi |
| Misi Besar | Edisi khusus Kampung Post | Bu Laras | Kota → Kampung Bahasa (Balai Desa, Candi) → Kampung Inggris → Kota → London (Border Control, University of London) |

Sepuluh misi warga B1 semuanya di Kampung Inggris. Misi Besar sengaja berakhir di London: hadiahnya (Rp100.000) menutup tiket pulang, dan B2 "Mahasiswa pertukaran di London" bisa dimulai dari sana. Pedagang gerobak tidak dipakai sebagai tokoh misi karena menekan E di depan mereka selalu membuka toko.

### 4c. B2 sudah ditulis (2026-10-09)

B2 dijalani seluruhnya di London (zona `gb`). Peta London diperpanjang ke selatan dengan **kawasan mahasiswa** (`world/abroad.ts`, `studentQuarter`): 12 Camden Road (flat, tempat pemain tidur Rp5.000 semalam), Students' Union, Bright Pages (lembaga amal), Town Hall, Old Globe Theatre, Police Station, dan Camden Green. Tokoh baru: Mr. Doyle, Aisha, Luca (flat), Priya (Students' Union), Ms. Harris (Bright Pages), Councillor Shah (Town Hall), Dr. Bennett (University of London). Warga Kampung Inggris ada di London dengan kunci yang sama: Miss Kate, Mr. Smith, Prof. Grey di universitas; Mrs. Hughes di The Grand Hotel; Mr. Green di British Museum; Chef Oliver, Tom, Mrs. Brown di deretan toko; Lily di depan teater; Officer Jones di kantor polisi.

| Bab | Misi | Pemberi | Tempat di London |
|---|---|---|---|
| 1 Tiba di London | Kontrak flat | Mr. Doyle | 12 Camden Road (Aisha, Luca) |
| 2 Kuliah pertama | Catatan kuliah | Dr. Bennett | University of London (Mr. Smith) |
| 3 Teman serumah | Drama dapur | Aisha | Flat, Corner Shop |
| 4 Andai saja | Podcast Titik Balik | Priya | Students' Union, Tea Room (Tom), Grand Hotel (Mrs. Hughes), British Museum (Mr. Green) |
| 5 Kesehatan masyarakat | Investigasi kantin | Aisha | Flat, Students' Union |
| 6 Dunia kerja | Magang di lembaga amal | Ms. Harris | Bright Pages, Grand Hotel |
| 7 Sains & teknologi | Poster ilmiah | Luca | Flat, University of London |
| 8 Lingkungan & energi | Debat: kota tanpa mobil | Priya | Students' Union, tiga warga London |
| 9 Politik & hukum | Petisi mahasiswa | Aisha | Flat, tiga tanda tangan, Town Hall (Councillor Shah) |
| 10 Masyarakat & media | Artikel feature | Dr. Bennett | University, Corner Shop (Mrs. Brown), flat (Mr. Doyle) |
| 11 Seni & sastra | Malam di West End | Luca | Old Globe Theatre (Lily), flat |
| 12 Menuju konferensi | Proposal & presentasi | Dr. Bennett | University of London (Prof. Grey) |
| Misi Besar | Konferensi Mahasiswa Internasional | Dr. Bennett | University → Students' Union → Grand Hotel |

Sepuluh misi warga B2 dimainkan di London, di tempat tiap warga berada. Misi Besar berakhir dengan tawaran wawancara di Thames Policy Lab, pintu masuk ke C1.

### 4d. C1 sudah ditulis (2026-10-09)

C1 dijalani seluruhnya di London (zona `gb`). Peta London diperpanjang lagi ke selatan (72×100) dengan **kawasan City** di tepi sungai (`world/abroad.ts`, `cityQuarter`): Thames Policy Lab, Housing Research Institute, The British Library, Committee Rooms, The Thames Herald, dan Press Centre. Tokoh baru: Ms. Morgan (direktur) dan Mr. Chen (klien) di Thames Policy Lab, Dr. Okafor di Housing Research Institute, Ms. Wright di Committee Rooms, Nina Walsh di The Thames Herald. Pemain tetap tidur di flat 12 Camden Road.

| Bab | Misi | Pemberi | Tempat utama |
|---|---|---|---|
| 1 `office` | Orientasi di Thames Policy Lab | Ms. Morgan | Thames Policy Lab |
| 2 `proposal` | Proposal penelitian | Dr. Okafor | Housing Research Institute |
| 3 `evidence` | Tinjauan bukti | Dr. Okafor | The British Library |
| 4 `negotiation` | Negosiasi dengan klien | Mr. Chen | Thames Policy Lab |
| 5 `ethics` | Sidang komite etik | Ms. Wright | Committee Rooms |
| 6 `media` | Kolom opini nasional | Nina Walsh | The Thames Herald |
| 7 `policy` | Policy brief untuk dewan kota | Ms. Morgan | Thames Policy Lab |
| 8 `history` | Sejarah lisan | Dr. Okafor | The British Library |
| 9 `philosophy` | Salon filsafat | Ms. Wright | The British Library |
| 10 `crisis` | Konferensi pers krisis | Ms. Morgan | Press Centre |
| 11 `words` | Glosarium proyek | Dr. Okafor | Housing Research Institute |
| 12 `publication` | Artikel & telaah sejawat | Dr. Okafor | Housing Research Institute |
| Misi Besar | Proyek unggulan | Ms. Morgan | Thames Policy Lab → Housing Research Institute → Committee Rooms → The Thames Herald |

Sepuluh misi warga C1 dimainkan di London, di tempat tiap warga berada, dan isinya bantuan profesional (kursus Miss Kate, rencana bisnis Tom, buku masak Chef Oliver, pidato Mrs. Brown, kontrak sewa Mr. Green, undangan konferensi Mrs. Hughes, kolom bahasa Mr. Smith, metodologi Prof. Grey, wawancara radio Lily, juru bahasa untuk Officer Jones). Misi Besar berakhir dengan undangan dari penerbit di South Bank, pintu masuk ke C2.

### 4e. C2 sudah ditulis (2026-10-10)

C2 dijalani di London (zona `gb`) dan berakhir di Kampung Inggris Pare. Peta London diperpanjang lagi ke selatan (72×122) dengan **kawasan South Bank** (`world/abroad.ts`, `southBank`): Ward & Hale Publishers, Southbank Centre, The Laughing Gull (klub komedi), Moot Court, KBRI London, Broadcasting House, dan taman dengan Speakers' Corner. Tokoh baru: Ms. Ward (editor), Dr. Hale (direktur festival), Mr. Fox (barrister), Ibu Ratna (atase kebudayaan), Inés (produser radio). Di kelima kampung bahasa ditambahkan gedung **Balai Mentor** (`world/english.ts`), tempat Misi Besar berakhir.

| Bab | Misi | Pemberi | Tempat utama |
|---|---|---|---|
| 1 `literature` | Lingkar baca South Bank | Dr. Hale | Southbank Centre |
| 2 `critique` | Kritikus tamu | Ms. Ward | Ward & Hale Publishers |
| 3 `humour` | Malam satire | Dr. Hale | The Laughing Gull |
| 4 `rhetoric` | Pidato di Speakers' Corner | Dr. Hale | Speakers' Corner |
| 5 `debate` | Debat gaya Oxford | Mr. Fox | Southbank Centre |
| 6 `law` | Sidang semu | Mr. Fox | Moot Court |
| 7 `science` | Dari jurnal ke publik | Ms. Ward | Ward & Hale Publishers |
| 8 `translation` | Penerjemah & juru bahasa | Ibu Ratna | KBRI London |
| 9 `englishes` | Suara-suara Inggris | Inés | Broadcasting House |
| 10 `editing` | Menyunting buku | Ms. Ward | Ward & Hale Publishers |
| Misi Besar | Karya besar & pulang kampung | Ms. Ward | Ward & Hale Publishers → Southbank Centre → KBRI London → Balai Mentor, Kampung Inggris Pare |

Sepuluh misi warga C2 dimainkan di London (umpan balik untuk guru magang, memoar Tom, balasan atas ulasan pedas, pidato perpisahan Mrs. Brown, surat wasiat keluarga Green, protokol kunjungan resmi, Kamus Kampung, buku persembahan Prof. Grey, lirik dua bahasa, mediasi lintas budaya). Babak terakhir Misi Besar dimainkan di Kampung Inggris: pemain harus pulang (pesawat ke Kota, lalu kereta atau bus), menjawab pendatang baru sebagai mentor bersama Miss Kate, dan berpidato. Hadiahnya (Rp120.000) menutup ongkos pulang. Dengan ini jalur bahasa Inggris Basic–C2 lengkap.

## 5. Hal yang harus diputuskan sebelum menulis misi

1. ~~**Bahasa warga Kampung Bahasa.**~~ **Diputuskan (ADR-0022):** warga Kampung Bahasa dan kota berbicara lima bahasa dan menjawab dalam bahasa yang sedang dipelajari pemain. Tidak ada warga baru khusus Inggris. Semua warga punya `key` (= `id`), dan game membuka misi pada mereka untuk bahasa misi apa pun.
2. **Tokoh A2+ (Shaw, Clarke, Khan, Lee, Maya, Reed, Max, Evans, Wood, Sam)**: dengan keputusan no. 1, peran mereka bisa dimainkan warga yang sudah ada (lihat tabel §4). Yang harus diputuskan saat menulis misi: nama mana yang tampil, nama warga peta (Pak Masinis) atau nama tokoh cerita (Mr. Khan).
3. **Newsroom dan radio (B1)** belum punya gedung sendiri; usul memakai MENARA BAHASA di kota.
4. **Status tempat di `world.ts`**: tempat yang sudah ada di peta masih bertanda "baru" dan belum menyebut zonanya (`kota`, `gb`). Perlu diubah ke "ada" dengan zona, dengan penyesuaian pemeriksaan `bun scripts/journey.ts`.
5. ~~Isi pelajaran B2–C2 belum ditulis.~~ **Selesai:** B2, C1, dan C2 sudah ditulis berikut misinya (§4c, §4d, §4e).
6. Misi bisa memakai `zone: "umum"`, `"kota"`, atau kode negara (`"gb"` …); server memeriksa zona pemain, dan zona kota atau negara hanya bisa dicapai dengan tiket, jadi langkah "pergi ke kota" atau "terbang ke London" terverifikasi sendiri.
7. ~~Tidur dan syarat level di luar negeri.~~ **Diputuskan (ADR-0022 §3a):** hotel berbayar bisa dipakai tidur; terbang ke suatu negara butuh level B2 di bahasanya (sementara level 3 sampai isi B2 ada). Jadi misi London tetap baru terbuka di akhir B1.
