# Bahasa Inggris per jenjang: audit deck Pre-A1 dan A1

Disusun 2026-11-21 untuk ADR-0032. Untuk setiap deck kanonik Pre-A1 dan A1 (75 deck), dicek apakah deck itu cocok apa adanya di setiap tingkat tempat jalur `inggris-kurikulum-indonesia` mengajarkannya, atau perlu deck jembatan dan misi varian sendiri.

## Ukuran yang dipakai

| Jenjang | Kelas | Batas (riset-inggris.md, scripts/aturan-kartu.ts) | Bentuk misi |
|---|---|---|---|
| `k34` | 3–4 | Penjelasan Indonesia ≤25 kata per kartu dan ≤9 kata per kalimat di Kelas 3 (≤40 dan ≤12 di Kelas 4), dibacakan (prabaca). Tanpa istilah tata bahasa dan kartu aturan (E10, E11). Kalimat Inggris ≤7 kata. Latihan hanya pilih, pasangkan, pilah, dengar satu kata, ketik satu kata. Konteks rumah, sekolah, UKS, kampung. | Dengar lalu pilih, isian satu kata. Tanpa rangkai kalimat |
| `k56` | 5–6 | Sama dengan batas A1 deck kanonik (≤60 kata, ≤12 kata per kalimat, ≤2 istilah). | Rangkai kalimat ≤6 kata boleh |
| `smp` | 7–9 | Target CP A2. Deck kanonik Pre-A1 dan A1 sudah di bawah level baca ini. | Misi umum |
| `sma` | 10–12 | Target B1–B2. | Misi umum |

**Kesimpulan:**
- **Kelas 3–4: semua 56 deck yang diajarkan di sana perlu jembatan.** Deck kanonik ditulis untuk pembelajar umum: kartu bisa sampai 60 kata, memakai istilah (subject, auxiliary), kartu aturan, lambang fonetik, dan konteks dewasa (hotel, bandara, kantor, status menikah, menawar). Deck itu juga tidak prabaca. Semua hal ini dilarang gerbang Kelas 3–4 (E6–E11). Pilot EK34a sudah menulis 5 deck.
- **Kelas 5–6: 6 dari 30 deck perlu jembatan**, yaitu deck yang memuat materi di atas Fase C atau konteks dewasa sebagai inti (bukan sekadar contoh). Sisanya cocok. Contoh dewasa di sebuah kartu (bank, bandara) tidak cukup alasan untuk jembatan.
- **SMP: tidak perlu varian sendiri.** Semua 51 deck cocok. Bacaannya di bawah level A2, dan konteks dewasa masih wajar untuk remaja. Siswa SMP yang sudah lulus unitnya di SD tetap lulus (ADR-0026), dan misi umum menjadi pengulangan yang lebih dalam.
- **SMA: cocok** untuk 21 deck.

## Tabel per deck

Kolom kelas: kelas jalur KI yang memuat unitnya (TL = Tingkat Lanjut). "Jembatan" diikuti hal yang dibuang dan inti yang tetap diajarkan.

| Deck | CEFR | Kelas KI | Kelas 3–4 | Kelas 5–6 | SMP | SMA |
|---|---|---|---|---|---|---|
| `sounds-alphabet` | Pre-A1 | K3 K7 | **jembatan**: pilot EK34a. Buang lambang fonetik, Great Vowel Shift, email, telepon hotel; cukup nama huruf dan mengeja nama | – | cocok | – |
| `pronoun-subject` | Pre-A1 | K3 K7 | **jembatan**: istilah subjek, it untuk cuaca/jarak, they untuk benda; cukup I, you, he, she, we, they dengan gambar orang | – | cocok | – |
| `verb-be` | Pre-A1 | K3 K4 K7 K8 K9 | **jembatan**: tabel bentuk dan aturan; cukup I am, you are, he/she is lewat ungkapan (I'm happy, She's my sister) | – | cocok | – |
| `det-articles` | Pre-A1 | K3 K7 | **jembatan**: pilot EK34a. Buang uniform/hour, tanpa article, empat pertanyaan; cukup a/an bergambar dan the door | – | cocok | – |
| `det-demonstrative` | Pre-A1 | K3 | **jembatan**: lambang fonetik, paspor, this morning; cukup this/that + benda di kelas | – | – | – |
| `sent-word-order` | Pre-A1 | K3 K8 K11 TL | **jembatan**: istilah S-V-O, bought; cukup susun 3 kata dari ungkapan yang sudah didengar | – | cocok | cocok |
| `sent-questions` | Pre-A1 | K3 K4 K5 K6 K7 K8 K9 K11 | **jembatan**: do-support, WH lengkap; cukup What's this? Is it…? Can you…? sebagai ungkapan | cocok | cocok | cocok |
| `vocab-greetings` | Pre-A1 | K3 K7 | **jembatan**: pilot EK34a. Buang Mrs/Miss/Ms (status menikah), pardon, kantor; konteks sekolah | – | cocok | – |
| `vocab-numbers-time` | Pre-A1 | K3 K7 | **jembatan**: pilot EK34a. Buang ratusan-jutaan, desimal, nomor telepon, harga, jam; cukup 0–100 | – | cocok | – |
| `vocab-classroom-language` | Pre-A1 | K7 K8 K9 | – | – | cocok | – |
| `vocab-clothes-colours` | Pre-A1 | K3 K4 K5 K6 K7 | **jembatan**: ejaan British-Amerika, mencampur cat dalam kalimat; cukup warna + benda | cocok | cocok | – |
| `vocab-toys` | Pre-A1 | K4 | **jembatan**: play with/fly, meminjam sopan (may I borrow); cukup nama mainan, Let's play | – | – | – |
| `vocab-shapes` | Pre-A1 | K4 | **jembatan**: pentagon-octagon, bangun ruang; cukup circle, square, triangle, rectangle, star, heart | – | – | – |
| `vocab-food-drink` | Pre-A1 | K4 K5 K6 K7 K10 | **jembatan**: tabel rasa lengkap, memesan; cukup nama makanan, buah, minuman, I'm hungry | cocok | cocok | cocok |
| `speak-introducing` | Pre-A1 | K3 K7 | **jembatan**: pilot EK34a. Buang pekerjaan, bandara/kantor, resmi-santai; cukup nama, umur, tinggal, This is | – | cocok | – |
| `speak-requests` | Pre-A1 | K4 K5 K7 K8 K9 | **jembatan**: could/may/would you mind; cukup …, please dan Can I have…? | cocok (Would you mind cukup dikenali) | cocok | – |
| `speak-wants` | Pre-A1 | K5 | – | cocok | – | – |
| `listen-numbers-spelling` | Pre-A1 | K7 | – | – | cocok | – |
| `sounds-vowels` | A1 | K4 | **jembatan**: lambang fonetik, peta vokal, schwa, diftong; cukup dengar-tirukan pasangan ship/sheep bergambar | – | – | – |
| `sounds-consonants` | A1 | K4 K11 | **jembatan**: bersuara/tak bersuara, aspirasi, th dua bunyi; cukup f/v, s/sh dengar-tirukan | – | – | cocok |
| `sounds-phonics` | A1 | K4 | **jembatan**: aturan magic e, -tion, vokal+r; cukup bunyi huruf awal dan kata CVC (cat, dog, bus) | – | – | – |
| `sounds-numbers` | A1 | K4 K5 K7 | **jembatan**: tanggal, tahun, past/to, bank/bandara; cukup thirteen/thirty dan jam bulat | cocok (contoh bank/bandara) | cocok | – |
| `noun-pengertian` | A1 | K10 | – | – | – | cocok |
| `noun-common-proper` | A1 | K3 | **jembatan**: istilah common/proper, the dengan nama; cukup nama orang/kota berhuruf besar | – | – | – |
| `noun-plural-regular` | A1 | K3 | **jembatan**: -ves, -o, tiga bunyi -s; cukup -s dan -es bergambar (books, boxes) | – | – | – |
| `noun-countable-uncountable` | A1 | K5 | – | cocok | – | – |
| `noun-plural-irregular` | A1 | K3 | **jembatan**: kata Latin-Yunani, selalu jamak; cukup children, men, women, feet, teeth | – | – | – |
| `pronoun-object` | A1 | K4 | **jembatan**: istilah objek, her dua tugas; cukup me, you, him, her dalam ungkapan (Help me!) | – | – | – |
| `pronoun-demonstrative` | A1 | K3 | **jembatan**: paspor, this di telepon, that untuk ucapan; cukup This is…/That is…/These are… | – | – | – |
| `pronoun-interrogative` | A1 | K3 | **jembatan**: whose/who's, pelaku tanpa do, did/was; cukup who, what dengan gambar | – | – | – |
| `verb-definition` | A1 | K10 | – | – | – | cocok |
| `adj-definition` | A1 | K3 K4 K5 K6 K8 K10 | **jembatan**: istilah, look/feel; cukup warna/ukuran + benda (a big cat, The cat is big) | cocok | cocok | cocok |
| `adv-time-place` | A1 | K7 K10 K11 TL | – | – | cocok | cocok |
| `det-possessive` | A1 | K3 K7 K9 | **jembatan**: husband, its/it's; cukup my, your, his, her + barang sekolah | – | cocok | – |
| `noun-possessive` | A1 | K3 K9 | **jembatan**: s' jamak, 's atau of, lambang fonetik; cukup Rina's bag | – | cocok | – |
| `det-quantifiers` | A1 | K5 | – | **jembatan**: 11 quantifier sekaligus; Kelas 5 cukup some/any, many/much, a lot of | – | – |
| `det-numbers` | A1 | K4 K7 | **jembatan**: lantai hotel, tanggal; cukup first, second, third di antrean/lomba | – | cocok | – |
| `prep-place` | A1 | K3 K4 K5 K7 | **jembatan**: above/opposite, bank/rapat; cukup in, on, under, next to dengan gambar kamar | cocok | cocok | – |
| `conj-coordinating` | A1 | K8 | – | – | cocok | – |
| `tense-present-simple` | A1 | K3 K4 K6 K7 K8 K9 K10 K11 K11 TL K12 | **jembatan**: empat kegunaan, ejaan dan bunyi -s, does; cukup I/you/we + kegiatan harian (I go to school) | **jembatan**: empat kegunaan, tabel ejaan dan bunyi -s; cukup kebiasaan, he/she -s, do/does | cocok | cocok |
| `verb-auxiliary` | A1 | K4 | **jembatan**: did, have got, tabel bentuk sesudah kata bantu; Kelas 4 cukup do/don't dalam ungkapan | – | – | – |
| `adv-frequency` | A1 | K4 K6 K7 K9 K10 | **jembatan**: posisi sesudah be, how often, kantor; cukup always/sometimes/never + kegiatan | cocok | cocok | cocok |
| `tense-present-continuous` | A1 | K3 K4 | **jembatan**: ejaan -ing, keadaan, masa sekitar sekarang; cukup What are you doing? I'm reading. | – | – | – |
| `tense-past-simple` | A1 | K5 K6 K8 K9 K10 K11 K11 TL K12 | – | **jembatan**: bunyi -ed dan daftar V2 panjang; Kelas 5–6 cukup was/were, -ed, 15 V2 umum, recount liburan | cocok | cocok |
| `modal-ability` | A1 | K4 K8 K12 TL | **jembatan**: could, was able to; cukup I can swim. Can you…? Yes, I can. | – | cocok | cocok |
| `modal-permission` | A1 | K5 K7 | – | cocok (contoh kantor) | cocok | – |
| `sent-negatives` | A1 | K4 K5 K6 | **jembatan**: didn't, was/were, satu negatif; cukup I don't like…, I'm not…, I can't… | cocok | – | – |
| `sent-imperative` | A1 | K4 K5 K6 K7 K8 K9 K10 K11 | **jembatan**: ke orang asing, bank; cukup perintah kelas (Sit down, Stand up, Don't run) | cocok | cocok | cocok |
| `sent-there-is` | A1 | K3 K7 K9 | **jembatan**: bank, there was/were, there/it; cukup There is a…/There are… di kamar dan kelas | – | cocok | – |
| `sent-linkers-sequence` | A1 | K4 K6 K7 K8 K9 K11 K11 TL | **jembatan**: firstly/secondly, cerita kemarin; cukup first, then, finally pada cuci tangan | cocok | cocok | cocok |
| `vocab-calendar` | A1 | K4 K7 | **jembatan**: tahun, tanggal 20–31; cukup hari dan bulan, today/tomorrow | – | cocok | – |
| `prep-time` | A1 | K4 K7 | **jembatan**: bagian hari bersama, next/last; cukup on Monday, in the morning, at seven | – | cocok | – |
| `vocab-family` | A1 | K3 K7 | **jembatan**: suami/istri, menikah; cukup keluarga inti dan kakek-nenek | – | cocok | – |
| `vocab-home` | A1 | K3 K5 K7 | **jembatan**: house/flat/floor, apartment, alat makan lengkap; cukup ruang dan perabot rumah | cocok | cocok | – |
| `vocab-daily-routine` | A1 | K3 K4 K6 K7 | **jembatan**: tabel present simple, he/she -s; cukup I wake up, I take a bath (versi I) | cocok | cocok | – |
| `vocab-school` | A1 | K3 K4 K7 | **jembatan**: denah dan kedatangan tamu, mata pelajaran lengkap; cukup benda di tas dan di kelas | – | cocok | – |
| `vocab-body-health` | A1 | K4 K6 K8 | **jembatan**: di dokter, keluhan; cukup bagian tubuh + I have a headache di UKS | cocok | cocok | – |
| `vocab-clothes` | A1 | K4 | **jembatan**: ukuran, membeli kemeja di pasar; cukup pakaian sekolah, a pair of | – | – | – |
| `vocab-appearance` | A1 | K3 K7 K10 | **jembatan**: kesan pretty/handsome, menjemput di stasiun; cukup tall/short, long/short hair | – | cocok | cocok |
| `vocab-weather-nature` | A1 | K4 | **jembatan**: empat musim, hujan sekarang/biasanya; cukup sunny, rainy, hot, cold, alam dekat rumah | – | – | – |
| `vocab-animals` | A1 | K6 K8 K9 | – | cocok | cocok | – |
| `vocab-feelings` | A1 | K4 K5 K6 K8 | **jembatan**: was/were, bosan/membosankan, sebelum ujian di Pare; cukup happy, sad, angry, scared, tired | cocok | cocok | – |
| `vocab-synonyms-antonyms` | A1 | K8 | – | – | cocok | – |
| `speak-personal-info` | A1 | K3 K7 | **jembatan**: kebangsaan, status menikah, pekerjaan, email; cukup nama, umur, alamat, kelas | – | cocok | – |
| `speak-ordering-shopping` | A1 | K5 K9 | – | **jembatan**: menawar, restoran dan tagihan, mencoba baju; cukup kantin/warung, how much/many | cocok | – |
| `speak-directions` | A1 | K5 K7 | – | **jembatan**: indirect question (Can you tell me where…), bank/kantor pos; cukup kiri-kanan-lurus di kampung | cocok | – |
| `speak-likes` | A1 | K3 K4 K6 K7 K8 K10 | **jembatan**: would like, really/very much, alasan; cukup I like…/I don't like…/Do you like…? | cocok | cocok | cocok |
| `speak-suggestions` | A1 | K4 | **jembatan**: shall we/why don't we, menolak tiga langkah, undangan; cukup Let's…! OK! | – | – | – |
| `read-short-functional` | A1 | K5 K6 K7 K8 K9 | – | cocok (contoh bandara/paspor) | cocok | – |
| `read-descriptive` | A1 | K7 K9 K10 K11 | – | – | cocok | cocok |
| `listen-instructions` | A1 | K5 K6 K8 K9 K11 | – | cocok (contoh bandara/bank) | cocok | cocok |
| `write-capitals-punctuation` | A1 | K3 K7 K11 | **jembatan**: koma, apostrof, its/it's, angka; cukup huruf besar awal kalimat, nama, I, titik | – | cocok | cocok |
| `write-sentences` | A1 | K3 K4 K5 K6 K9 | **jembatan**: menyambung kalimat, kalimat terpotong; cukup menyalin dan melengkapi kalimat pendek | cocok | cocok | – |
| `write-forms-messages` | A1 | K5 K11 | – | **jembatan**: kartu kedatangan, kewarganegaraan, status menikah; cukup formulir klub sekolah, pesan ke orang tua | – | cocok |
| `write-descriptive` | A1 | K3 K6 K7 K9 K10 K11 | **jembatan**: kamar kos, peta pikiran ke paragraf; cukup 3 kalimat tentang benda/hewan kesayangan | cocok (contoh kamar kos) | cocok | cocok |

## Catatan kanonik (tidak diubah, dilaporkan)
- `vocab-greetings` #9 mengajarkan Mrs/Miss/Ms menurut status menikah. Untuk SD, versi jembatan memakai Miss sebagai sapaan guru perempuan saja.
- `speak-introducing` #0 menyebut bandara dan kantor sebagai tempat berkenalan, dan `speak-personal-info` menanyakan status menikah. Ini wajar untuk dewasa, tetapi menjadi alasan utama jembatan SD.
- `det-articles` #10 dan `sent-negatives` memakai bentuk lampau (saw, was, didn't) sebelum Past Simple. Ini sudah tercatat koordinator untuk tinjauan A1.
- `sounds-alphabet` #25 menulis lambang fonetik di kartu "yang sering keliru". Kartu jembatan SD menggantinya dengan cara baca ala ejaan Indonesia.
