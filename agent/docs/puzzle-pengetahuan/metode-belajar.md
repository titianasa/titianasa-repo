# Metode belajar Puzzle Pengetahuan

Rancangan kurikulum, 2026-11-01. Melengkapi [ADR-0024](../adr/0024-puzzle-pengetahuan.md): ADR itu mengatur *wadah*-nya (graf, mastery, editor), dokumen ini mengatur *cara mengajarnya*.

Bentuk pengalaman siswanya (aktivitas dulu, animasi, misi, sistem semangat) dirancang di [desain-misi.md](desain-misi.md). Prinsip di dokumen ini tetap berlaku.

## Ringkasan

Puzzle Pengetahuan sekarang punya wadah yang bagus tetapi metodenya masih "baca → kuis pilihan ganda → susun kata → selesai". Pola itu terasa rapi, namun efek belajarnya lemah:
- pilihan ganda hanya melatih *mengenali*, bukan *mengingat*;
- menyusun kata acak bukan transfer;
- "selesai" setelah sekali benar menciptakan ilusi menguasai, padahal besok sudah lupa.

Usulan: setiap puzzle, di mata pelajaran apa pun dan untuk usia berapa pun, melewati satu siklus yang sama:

> **Lihat → Coba → Buktikan → Pakai → Ingat**

Mesinnya satu, tetapi tiga hal disesuaikan:
1. **Jenis pengetahuan**: fakta, konsep, prosedur, prinsip, atau strategi. Jenisnya menentukan bentuk latihan.
2. **Lapisan pelajar**: anak, remaja, atau dewasa, dan pemula atau mahir. Lapisannya menentukan takaran bantuan dan cara penyajian.
3. **Graf lintas pelajaran**: puzzle dari mata pelajaran berbeda bisa disambung dalam satu proyek.

Efeknya dibuktikan dengan ukuran yang dikunci dari awal: retensi hari ke-7 dan ke-30, keberhasilan transfer, dan uji coba terkontrol.

## 1. Apa yang terbukti berhasil, dan apa yang kurang di versi sekarang

| Prinsip (riset) | Artinya untuk kita | Versi sekarang |
|---|---|---|
| **Retrieval practice**: menguji diri lebih efektif daripada membaca ulang (Roediger & Karpicke; Dunlosky dkk. menilainya "utilitas tinggi") | Siswa harus *mengeluarkan* jawaban dari ingatan | Uji = pilihan ganda (mengenali). Perlu isian dan produksi |
| **Spacing**: latihan yang dijeda jauh lebih awet daripada sekaligus | Puzzle baru dianggap kuat setelah lolos ulangan di hari lain | "Selesai" diberikan di hari yang sama |
| **Interleaving**: ulangan campuran melatih memilih aturan yang tepat | Ulangan harian mencampur beberapa puzzle | Ulang hanya per puzzle |
| **Worked example dan fading** untuk pemula (Sweller), dibalik untuk yang mahir (*expertise reversal*, Kalyuga) | Pemula diberi contoh terurai lalu bantuan dikurangi bertahap; yang sudah bisa langsung diuji | Semua orang dapat materi panjang yang sama |
| **Contoh dan bukan-contoh** untuk konsep | Tunjukkan yang salah di samping yang benar, lalu siswa memilah | Sudah ada satu "kesalahan umum" per konsep, belum dijadikan latihan |
| **Umpan balik spesifik per miskonsepsi** | Jawaban salah dipetakan ke penyebabnya, lalu diarahkan ke puzzle prasyarat | Hanya "benar/salah", plus kata merah di Rangkai |
| **Mastery learning** (Bloom): lanjut setelah menguasai, dengan koreksi | Graf prasyarat dipakai untuk diagnosis dan remedi | Graf baru dipakai sebagai peta |
| **Transfer** butuh variasi konteks | "Pakai" = situasi baru yang nyata: misi Kampung Bahasa, soal cerita, proyek | Rangkai = menyusun ulang kalimat contoh |
| **Kalibrasi metakognitif** | Siswa menilai "yakin atau ragu" sebelum melihat jawaban. Salah tapi yakin menandai miskonsepsi | Belum ada |
| **Concreteness fading (CRA)** untuk anak dan matematika | Konkret (gambar, benda) → representasi (diagram, blok) → abstrak (simbol) | Langsung ke bentuk abstrak |
| **4C/ID** (van Merriënboer): belajar lewat tugas utuh, dengan info pendukung dan latihan bagian | Tugas utuh (Pakai, Proyek) menjadi tulang punggung, sedangkan puzzle adalah bagian-bagiannya | Tugas utuh belum ada |

## 2. Siklus satu puzzle: Lihat → Coba → Buktikan → Pakai → Ingat

| Langkah | Tujuan | Isi | Durasi |
|---|---|---|---|
| **1. Lihat** | Membangun gambaran yang benar | Satu contoh terurai (langkah demi langkah), satu bukan-contoh, pola dalam satu kalimat. Untuk anak: gambar dan audio. **Bukan teks panjang.** | 1–2 menit |
| **2. Coba** (dibimbing) | Membangun kemampuan dengan bantuan | Latihan berbantuan yang **memudar** dalam 3 tingkat. Tingkat 1: susun blok dengan petunjuk dan sebagian sudah terpasang (Parsons problem). Tingkat 2: susun blok tanpa petunjuk. Tingkat 3: isian bebas. Naik tingkat setelah 2 benar berturut-turut; turun satu tingkat setelah salah. | 3–5 menit |
| **3. Buktikan** | Bukti ingatan tanpa bantuan | 3 soal **produksi** (isian, ketik, susun tanpa blok bantu) dengan penilaian "yakin/ragu" sebelum jawaban dibuka. Lulus = puzzle **dimiliki**. | 2 menit |
| **4. Pakai** | Transfer ke situasi baru | Satu tugas dalam konteks nyata, contohnya:<ul><li>bahasa: misi di Kampung Bahasa, menulis atau berbicara dengan warga, dinilai AI dengan rubrik yang menyasar puzzle ini;</li><li>matematika: soal cerita;</li><li>sains: menjelaskan fenomena.</li></ul> | 3–5 menit |
| **5. Ingat** | Memindahkan ke ingatan jangka panjang | Ulangan terjadwal (±1, 3, 7, 21 hari; jadwal FRSS yang sudah ada), **dicampur** dengan puzzle lain. Satu soal per puzzle sudah cukup. | 1 menit/hari |

**Status puzzle, untuk siswa:**
- **Dimiliki 🧩**: lulus Buktikan.
- **Dikuasai ✨**: lulus Pakai **dan** lulus satu ulangan Ingat di hari lain (≥ 1 hari kemudian). Inilah definisi "tamat" yang jujur.
- **Memudar**: kekuatan turun di bawah 50. Puzzle kembali ke antrean Ulang; pencapaian lamanya tidak hilang.

**Jalan pintas untuk yang sudah bisa (*test-out*).** Setiap puzzle punya tombol "Sudah tahu? Langsung buktikan". Kalau lulus, Lihat dan Coba dilewati. Orang dewasa dan siswa mahir tidak dipaksa membaca ulang.

**Remedi otomatis (akar masalah).**
- Gagal Buktikan dua kali → sistem menguji 1–2 soal dari setiap prasyarat langsung (yang sudah kuat dilewati), sampai kedalaman 4, lalu mengarahkan ke puzzle akar.
- Jawaban salah yang dijawab "yakin" langsung dibaca sebagai miskonsepsi.
- Pilihan salah di setiap soal diberi label miskonsepsi, misalnya `he have` → kesesuaian subjek dan kata kerja → puzzle `en-present`.

## 3. Jenis pengetahuan → bentuk latihan (kunci lintas pelajaran)

Setiap mata pelajaran tersusun dari lima jenis pengetahuan yang sama (Anderson & Krathwohl; Merrill). Yang berbeda hanya isinya. Jenis menentukan bentuk blok di editor (sudah ada di ADR §10) dan resep latihan:

| Jenis (`kind`) | Contoh lintas pelajaran | Lihat | Coba (blok) | Buktikan | Pakai |
|---|---|---|---|---|---|
| **Fakta / kosakata** (`vocab`, `fact`) | kosakata Inggris, lambang unsur, tahun peristiwa, nama organ | kartu bergambar dan audio | pasangkan, pilih dari gambar | ingat bebas (ketik atau ucap) | dipakai di kalimat atau soal |
| **Konsep** (`concept`) | passive voice, pecahan senilai, fotosintesis, majas | contoh dan bukan-contoh | pilah: masuk kategori atau tidak | buat contoh baru sendiri, kenali di teks | jelaskan atau terapkan di situasi baru |
| **Prosedur** (`procedure`) | ubah ke passive, penjumlahan pecahan, setarakan reaksi | contoh terurai, langkah bernomor | blok-C bertahap, dengan langkah yang dikosongkan bertahap | kerjakan tanpa bantuan | soal cerita, data nyata |
| **Simbol / notasi** (`symbol`) | `→`, `=`, rumus, IPA (pelafalan) | baca simbol + arti | susun ekspresi dari blok heksagon | tulis atau baca notasi | pakai dalam prosedur |
| **Prinsip / strategi** (jenis baru `principle`) | argumen *claim–evidence–reasoning*, strategi membaca, sebab-akibat sejarah | contoh analisis | susun kerangka argumen dari blok | analisis kasus baru | proyek atau esai pendek dinilai rubrik AI |

Paket aturan (*builder pack*) per disiplin menjadi "papan" Scratch-nya:

| Paket | Isi |
|---|---|
| `kalimat` (sudah ada) | susun kata |
| `ekspresi` (matematika) | blok angka, operasi, dan kurung; diperiksa secara numerik atau aljabar |
| `reaksi` (kimia) | blok rumus dan koefisien; diperiksa setara atau tidak |
| `argumen` (lintas pelajaran) | blok Klaim, Bukti, dan Alasan; diperiksa dengan rubrik AI |
| `garis-waktu` (sejarah) | urutkan peristiwa beserta sebab-akibatnya |

## 4. Lapisan pelajar: satu mesin, empat cara penyajian

Mesinnya sama: graf, mastery, dan siklus 5 langkah. Yang berubah adalah **profil penyajian**, yang dipilih dari usia di profil akun dan bisa diganti guru atau orang tua.

| | **Anak awal** (6–9) | **Anak** (10–12) | **Remaja** (13–18) | **Dewasa** |
|---|---|---|---|---|
| Lihat | audio-dulu, gambar, maskot, tanpa istilah tata bahasa | cerita pendek + gambar | contoh terurai + pola | ringkas, langsung pola dan contoh |
| Coba | blok bergambar, ketuk-dengar, banyak bantuan | blok + teks pendek | blok, fading normal | boleh dilewati (test-out) |
| Buktikan | ucap atau pilih gambar | isian pendek | isian + "yakin/ragu" | produksi bebas |
| Pakai | permainan peran di Kampung Bahasa | misi + cerita | misi, soal ujian (TKA, SNBT) | tujuan nyata: TOEFL, kerja, perjalanan |
| Sesi | 5 menit, 2–3 puzzle | 10 menit | 15–20 menit | bebas, ditentukan sendiri |
| Motivasi | stiker, maskot, laporan ke orang tua | lencana, koleksi | liga, streak, target ujian | progres menuju tujuan, tanpa gimmick |
| Bahasa antarmuka | "Ayo susun!" | "Susun kalimatnya" | biasa | ringkas |

**Pemula vs mahir** tidak ditentukan usia:
- Tes penempatan 10–15 soal memakai graf: soal dipilih dari puzzle tengah, lalu naik atau turun cabang ala *Knowledge Space Theory*.
- Hasilnya memberi titik mulai per orang. Puzzle yang sudah dikuasai langsung dimiliki, dengan jadwal Ingat tetap jalan untuk memastikan.

**Isi per lapisan:**
- Setiap puzzle menyimpan `content.variants.{anak,remaja,dewasa}`. AI membuat variannya lewat pipeline konten yang sudah ada, lalu ditinjau manusia sebelum terbit.
- Yang diubah AI hanya penyajiannya (contoh, panjang, media). Pola dan soal intinya tetap satu.

## 5. Lintas pelajaran (interdisipliner)

1. **Jembatan antar-graf.** `concept_relations` dengan jenis baru `bridge` menyambung puzzle yang memakai ide yang sama di pelajaran berbeda. Contohnya:
   - perbandingan (Matematika) ↔ konsentrasi larutan (Kimia) ↔ skala peta (Geografi);
   - passive voice (Inggris) ↔ penulisan laporan praktikum (IPA).

   Menguasai satu sisi jembatan menurunkan biaya tes-out di sisi lain.
2. **Proyek lintas puzzle**, yaitu tugas utuh ala 4C/ID dengan `required` dari dua pelajaran atau lebih. Contoh:

   | Proyek | Puzzle yang dipakai |
   |---|---|
   | *Laporan praktikum singkat dalam bahasa Inggris* | passive voice + past simple + pengukuran dan satuan (Fisika) |
   | *Belanja di pasar Kampung Bahasa* | angka + harga + persen diskon (Matematika) + would like / how much (Inggris) |
   | *Garis waktu kemerdekaan* | fakta sejarah + sebab-akibat + past tense |

   Puzzle yang kurang ditampilkan sebelum mulai, dengan tombol "Kumpulkan dulu".
3. **Guru sebagai perancang.** Mulai tahap 6 ADR, guru menyusun proyek dari puzzle yang ada di Ruang Kelas tanpa membuat soal dari nol. Mesin memeriksa prasyarat kelas dan menunjukkan "puzzle yang paling sering membuat kelas gagal".

## 6. Membuktikan efeknya

**Ukuran utama**, dikunci sebelum uji coba dan dibaca dari `learning_events`:
1. **Retensi hari ke-7 dan ke-30**: persen benar pada soal Ingat yang belum pernah dilihat.
2. **Transfer**: keberhasilan langkah Pakai dan proyek, dibanding kelompok yang hanya membaca dan mengerjakan kuis.
3. **Waktu sampai dikuasai** per puzzle, dan berapa yang terselamatkan oleh test-out dan diagnosis.
4. **Kalibrasi**: selisih antara keyakinan dan kebenaran. Yang baik menurun seiring waktu.

**Uji coba** selama 6 minggu:

| Kelompok | Peserta | Pembanding |
|---|---|---|
| A | pemain Pare level A1, sekitar 60 orang | sebagian diacak ke alur lama (Materi → Kuis) |
| B | satu kelas SMP mitra, bahasa Inggris | pre-test, post-test, dan tes tunda 30 hari |

- Target efek: d ≥ 0,3 pada retensi hari ke-30.
- Eksperimen kecil dijalankan permanen lewat flag: contoh-dulu vs uji-dulu, dan fading 3 tingkat vs 2 tingkat.

**Gerbang mutu konten.** Puzzle baru terbit kalau memenuhi semua ini:
- 1 contoh terurai dan 1 bukan-contoh;
- ≥ 6 soal ingat (minimal setengahnya produksi);
- ≥ 2 tugas Pakai;
- setiap pengecoh berlabel miskonsepsi;
- varian penyajian untuk lapisan yang dituju.

Validator importer memeriksa semua ini, seperti validator graf yang sudah ada.

## 7. Dari yang sudah ada ke metode ini

Bahan yang sudah tersedia untuk bahasa Inggris (164 konsep):

| Langkah | Bahan |
|---|---|
| Lihat | pola, penjelasan, 2–4 contoh, 1 kesalahan umum (menjadi bukan-contoh) |
| Coba | 2 kalimat susun per konsep → Parsons tingkat 1–2 |
| Buktikan | 2 isian per konsep → diubah dari pilihan ganda menjadi **ketik jawaban** (`gap_fill`, penilaiannya sudah ada) |
| Pakai | misi dan NPC Kampung Bahasa, plus evaluasi tata bahasa AI yang sudah ada (perlu rubrik per puzzle) |
| Ingat | FRSS dan antrean ulang yang sudah ada; tinggal dicampur dan diberi syarat "hari lain" |

**Status 2026-11-01: Tahap A selesai di dev, belum di-deploy.** Keputusan 1 di bawah diambil sesuai usul: Dikuasai wajib lolos satu ulangan di hari lain. Catatan pelaksanaannya:
- Langkah Pakai untuk sementara berupa menulis kalimat baru dari artinya. Konteks nyata di Kampung Bahasa menyusul di Tahap C.
- Level Basic memakai soal pilihan (bukan ketik) di Buktikan, karena game tidak punya soal isian untuk Basic.
- `en-article` dan `en-plural` tidak punya latihan Coba, karena contohnya frasa dua kata. Siswa langsung diarahkan ke Buktikan.
- Status "Coba selesai" dan "Lihat selesai" disimpan di browser (localStorage). Status lainnya disimpan di server.

**Urutan pengerjaan:**

| Tahap | Isi | Perkiraan |
|---|---|---|
| **A. Siklus inti, bahasa Inggris** | 5 langkah menggantikan 3 tab; Coba dengan fading; Buktikan berupa isian ketik + "yakin/ragu"; syarat Dikuasai = Pakai + satu Ingat di hari lain; Ulang dicampur; tombol test-out | 1–2 minggu |
| **B. Diagnosis dan miskonsepsi** | Label miskonsepsi pada pengecoh (AI mengusulkan, manusia meninjau); remedi akar masalah lewat graf; tes penempatan | 1–2 minggu |
| **C. Pakai di Kampung Bahasa** | Misi bertarget puzzle, rubrik AI per puzzle, jawaban Pare ikut menghitung (keputusan 5 di ADR) | 1–2 minggu |
| **D. Lapisan usia** | Profil penyajian; varian konten via pipeline AI + tinjauan; mode Anak (audio, gambar, sesi 5 menit); laporan orang tua dan guru | 2–3 minggu |
| **E. Pelajaran kedua: Matematika** | Paket blok `ekspresi`, 253 unit kanonik sebagai puzzle, CRA untuk SD. Membuktikan mesinnya lintas pelajaran | 3–4 minggu |
| **F. Jembatan dan proyek lintas pelajaran** | Relasi `bridge`, proyek ala 4C/ID, guru menyusun proyek | 2 minggu |
| **Sepanjang jalan** | Uji coba terkontrol dan dasbor ukuran efek | — |

Tahap A sudah bisa diuji coba di Pare (kelompok A) begitu selesai. Tahap B–C memperkuat efeknya, dan tahap D–F memperluas cakupannya.

## Keputusan yang perlu pemilik

1. **Definisi tamat.** "Dikuasai" harus melewati satu ulangan di hari lain? *Usul: ya.* Ini yang membuat efeknya nyata. Kompensasinya, "Dimiliki" langsung memberi rasa berhasil di hari yang sama.
2. **Pelajaran kedua.** Matematika (unit kanonik sudah ada) atau IPA? *Usul: Matematika.*
3. **Mitra uji coba** untuk kelompok B: sekolah, kelas, atau tutor mana.
4. **Usia di profil akun.** Wajib saat mendaftar, atau ditanya saat pertama membuka Puzzle? *Usul: ditanya saat pertama membuka Puzzle*, satu pertanyaan saja, bisa diubah.
