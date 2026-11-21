# Temuan audit misi Matematika

Catatan ini mengumpulkan masalah yang ditemukan saat membuat dan menguji misi (ADR-0028), sejak pilot Bilangan Bulat sampai produksi Level 1–7 (2026-11-19). Setiap temuan berisi gejalanya, penyebabnya, dan aturan atau pengaman yang sekarang mencegahnya. Baca catatan ini sebelum menulis misi, menambah bentuk latihan, atau mengubah penilaian.

## Soal yang tidak bisa dijawab benar

| Temuan | Penyebab | Perbaikan dan pengaman |
|---|---|---|
| Soal ketik "Negatif selalu kurang dari positif" hanya menerima `−3 < 1` | Petunjuk tidak menyebut bilangannya | Generator menambahkan "Pakai bilangan: …" ke petunjuk latihan dan uji akhir untuk bilangan dan huruf yang tidak disebut (`denganPetunjuk`). Hasil hitungan tidak ikut disebut kalau bisa dihitung |
| Daftar "Pakai bilangan: 3, 15" ikut menyebut hasil 15 | Daftar dihitung di aplikasi dari potongan yang sudah diacak | Daftar dihitung di generator dari kalimat aslinya, bukan di aplikasi |
| `1 > −3`, `7 = 3 + 4`, `5 × 3 = 15` ditolak | Kunci hanya satu urutan | Server menerima `accept`: kalimat dibaca dari sisi lain, dan dua bilangan penjumlahan atau perkalian ditukar (`sameSentences` di importer). Aplikasi membalik `>`/`<` yang tidak ada di potongan (`typedToOrderLoose`). Pengurangan dan pembagian tidak ditukar |
| `−3 + 5 = 2` ditolak untuk `(−3) + 5 = 2` | Kurung dianggap bagian bilangan | `typedToOrder` menyamakan `(−3)` dan `−3` |
| `250.000` ditolak untuk `250000`, `·` tidak dibaca kali | Ketikan ponsel | `mathTokens` membuang titik ribuan dan membaca `·` sebagai × |
| Isian `0.75` untuk `0,75`, `17 / 12`, `(2,-3)`, `15 cm`, `Rp80`, `1.200`, "nggak" ditolak | Server membandingkan teks persis | `sameTypedAnswer` di `internal/grading/typed.go`. Yang memang salah tetap ditolak (`375` untuk `0,375`, `34/24` untuk `17/12`) |
| `x = □` dengan petunjuk "Bagi kedua ruas dengan 2" | Langkah persamaan atau model cerita tidak bisa dihitung dari kalimatnya sendiri | Bentuk isi angka dan lengkapi koefisien hanya untuk kalimat bilangan atau identitas aljabar (`fits` dan `isIdentity` di `math-soal.ts`). Selain itu memakai susun blok |
| Lengkapi koefisien error pada `n(n + 1) = n² + n` | Ruas kanan tidak punya koefisien tertulis | `fits` mengganti bentuk yang tidak cocok dengan susun blok |
| Kerjakan satu per satu gagal pada `−(2 × 3 + 1)` dan `= 4²` | Minus di depan kurung dan hasil berpangkat | Sama, lewat `fits` |
| Jawaban isian `4√3`, `2√2` | Simbol tidak ada di keyboard ponsel | Simbol ditaruh di teks soal: `√48 = ___√3`, jawaban `4`. Diperiksa di audit |

## Kunci jawaban yang bocor

| Temuan | Penyebab | Perbaikan dan pengaman |
|---|---|---|
| Isian uji akhir menampilkan "−1 + 5 = 4" di bawah soal | Penjelasan jawaban masuk ke kolom arti, dan importer menampilkan arti sebagai baris kedua | Penjelasan dikirim lewat `explain` dan baru muncul setelah menjawab. Audit: 0 dari 1.792 isian Matematika menampilkan jawaban |
| 966 dari 2.301 petunjuk latihan menyebut jawabannya ("Lawan dari −4 adalah 4") | Penulis menulis arti lengkap | Aplikasi menutup angka jawaban dengan "…" pada bentuk yang meminta angka (`hideAnswer`), kecuali model cerita. Brief: arti tidak boleh menyebut hasil |

- **Bentuk dengar dengan suara browser** (pasangan minimal, dikte, urutkan dengar): teks `say` harus ikut ke pemain supaya bisa dibacakan, jadi kunci bisa dibaca dari jaringan. Bentuk lain (pilah, urutkan, geser, ketuk) tidak mengirim kunci: ketuk mengirim area tanpa id-nya. Saat audio rekaman ada, `say` diganti id klip (2026-11-21).
- **Ketuk dengan area berlabel**: area jawaban yang tulisannya disebut soal menjawab dirinya sendiri. Generator menolaknya; yang ditanya diberi ikon atau dikosongkan dan dicari lewat patokan.

## Isi soal yang ambigu (peninjauan 2026-11-19)

Peninjau Level 4–7 memeriksa 275 misi dan mengubah 371 soal:
- 274 situasi uji akhir bisa ditulis sebagai kalimat lain yang sama benar. Situasinya sekarang menyebut urutan.
- 49 soal butuh angka, huruf, tabel, atau gambar yang tidak ada di teks.
- 25 isian tidak menyebut bentuk jawaban (pecahan atau desimal, campuran atau biasa, paling sederhana).
- 18 isian berupa kata yang punya sinonim. Sekarang pilihannya disebut.
- 5 soal punya dua pilihan benar. Contohnya √200 memang terletak di antara 10 dan 20.
- 1 penjelasan salah.

Peninjau Level 1–3, pilot Bilangan Bulat, dan Aljabar memeriksa 253 misi dan mengubah 223 soal:
- 158 situasi uji akhir bisa ditulis dengan cara lain. Contohnya "Tulis sisanya" dengan kunci `40 + (−15) = 25`, sekarang "… sebagai penjumlahan".
- 30 isian berupa kata yang punya sinonim, misalnya peubah dan variabel, separuh dan setengah, bulat dan lingkaran.
- 25 isian tidak menyebut bentuknya. Contohnya 21/35 yang juga bisa ditulis 3/5, dan "kurang dari ___" yang bisa diisi 1, 2, atau 4.
- 8 soal kehilangan angka atau huruf, misalnya "Rapikan notanya" tanpa menyebut huruf k dan s.
- 2 fakta salah. Salah satunya kedipan keempat lampu bisa 27 atau 36, tergantung detik 0 dihitung atau tidak.

Aturan untuk penulis ada di `brief-peninjau-misi.md` dan `brief-penulis-misi.md`.

## Mesin dan generator

| Temuan | Perbaikan dan pengaman |
|---|---|
| Importer diam-diam membuang latihan di luar 3–12 potongan | Generator menolak latihan seperti itu. Kalimat panjang dipindah ke uji akhir |
| Isian dengan satuan (`1 m = ___ cm`) membuat pemeriksa crash | `holdsLoosely` melewati isian yang tidak bisa dihitung |
| Batas rantai prasyarat 12 berlaku untuk seluruh graf, sehingga Level 5 ke atas pasti gagal | Keputusan pemilik: batas dihitung per level (`ValidateByLevel`). Loop tetap dicari lintas level |
| Prasyarat redundan memunculkan peringatan importer | Brief: jangan tambah prasyarat yang sudah tersirat. Koordinator menghapus sisanya sebelum impor |
| Level Matematika tampil sebagai "B2" | `levelLabel(level, subject)` |
| Misi geometri dan data berlabel "Bilangan Bulat", semua di area bilangan | Kategori dari judul bab, area dari keluarga deck (`areaOf`) |
| Bentuk "tanda dulu, baru angka" muncul di 71 soal tanpa bilangan negatif | Hanya untuk kalimat yang memuat bilangan negatif |
| Kepingan (bilangan, tanda, variabel) hanya ada di jaringan satu level | Ditandai `lintas_level` |
| `−(x − 4)²` membuat pemeriksa identitas error | `algebraJs` membungkus minus sebelum pangkat |
| Mode periksa generator memanggil dirinya sendiri, sehingga run biasa macet | Diperbaiki. Pelajaran: uji kedua mode setiap kali mengubah generator |
| Impor bisa membawa level yang masih ditulis | `MISI_LEVELS=2,4,5` hanya menulis level itu |
| Importer tidak menghapus misi yang id-nya diganti | Jangan ganti id setelah diimpor. Kalau terpaksa, hapus misi lama secara sadar |

## Cara kerja agen

- Agen penulis ditolak sistem izin saat menjalankan generator penuh (menulis file bersama) dan importer. Agen memakai `MISI_CEK=1`. Generator penuh dan importer dijalankan koordinator.
- Satu agen peninjau membagi tugasnya ke 9 subagen, padahal pemilik membatasi dua agen sekaligus. Kedua brief sekarang melarang subagen.
- RAM habis pada 2026-11-19 pukul 20.02. Sebuah proses `bun` membengkak sampai 7 GB, lalu OOM killer mematikan seluruh terminal, termasuk sesi Claude dan kedua agennya. Penyebabnya:
  - `tsc -p .` memakan ±1,9 GB dan butuh 82 detik;
  - dua agen menjalankannya bersamaan;
  - server dev Next (4–7 GB) masih hidup.
  Aturannya sekarang:
  - Perintah berat dijalankan lewat `agent/tools/batas-ram.sh <batas> <perintah>`, yang menaruh proses di scope systemd sendiri dengan MemoryMax. Proses yang melewati batas mati sendirian.
  - Server dev hanya dinyalakan untuk uji browser, dengan batas 5G, lalu dimatikan.
- Prettier pernah dijalankan pada file yang tidak berformat Prettier. Repo `titian-web` tidak memakai Prettier: jangan menjalankannya.

## Kecepatan pengujian

- Halaman `/puzzle` memuat seluruh pustaka kartu (15 MB), sehingga kompilasi pertama butuh 63 detik. Beranda sekarang memakai `src/content/kartu/daftar.ts` (judul saja) dan turun ke 15 detik. Halaman misi masih memuat semua kartu (64 detik). Ini utang.
- Server dev memakai sekitar 4 GB, dan swap hampir penuh. Mulai ulang server dev kalau pengujian melambat.
- Skrip uji browser memakai jeda tetap dan membuka kartu satu per satu. Cukup uji bentuk yang berubah.

## Bahasa Inggris (pilot Pre-A1, 2026-11-21)

| Temuan | Perbaikan dan pengaman |
|---|---|
| Latihan diketik tanpa blok dan uji akhir diketik bebas, jadi kalimat lain yang sama benar ditolak (It's/That's untuk "Itu", I'm nine/I'm nine years old, can/could/may untuk "Boleh/Bisa", eat/have untuk "makan") | Arti dan situasi menunjuk pilihannya: "Bentuknya …", "(tanpa years old)", "(pakai may)". Generator menolak he/she tanpa (laki-laki)/(perempuan) atau nama |
| Urutan lain dari kata yang sama juga benar ("Could you please spell that?") | Uji akhir boleh menulis urutan lain sebagai elemen keempat `pakai`; importer menaruhnya di `accept` (`placeLoose`). Generator memastikan katanya sama persis |
| that's, what's, where's diketik panjang ditolak | Ditambahkan ke daftar bentuk pendek di `sentence.ts` (aplikasi) dan `contractions` (importer, untuk isian) |
| "Budi and I are" dianggap I + are | Pemeriksa subjek-be melewati pronoun sesudah "and" |
| Soal dengar di latihan tidak punya suara | Pilih dengan elemen keenam membawa `say` (`pilihPrompt` di importer); aplikasi memutar suaranya dan menyediakan "Lihat teksnya" |
| Kartu dipilih pemain menurut judul | Generator menolak judul kartu kembar di satu deck |
| Isian yang jawabannya tertulis di teksnya sendiri | Generator menolak |
| Pilihan yang hanya beda kapital/tanda baca ditolak sebagai kembar (2026-11-21, penulis A1) | `checkChoice` membandingkan persis setelah trim (`twinOptions`, `scripts/misi-inggris-aturan.ts`) |
| Tema yang menguji kapital dan tanda baca tidak bisa dinilai | Bendera tema `kapital: true` → misi `kapital` → importer menulis `strict` dan `texts` di kunci soal, `kapital` di prompt/data → `grading` (`sentence.go`) membandingkan teks peka kapital, koma, dan tanda akhir; pemain mengirim teks ketikan dan menampilkan "Perhatikan huruf besar dan tanda baca." |
| NAMA menelan kata biasa (May/may, March/march) | Nama hanya berlaku dengan kapital di tengah kalimat; di awal kalimat kata menang ("May I borrow your kite?" = modal). Sama di generator (`pieceOf`), importer (`wordsIn`), dan pemain (`isNameAt`) |
| "Rina's" harus ditulis di NAMA | `Nama's` dibaca nama + 's otomatis; pemain melabelinya Possessive noun · milik Rina |
| "five five", "very very" ditolak sebagai kata ganda | Hanya salah ketik kata tugas (the the, a a, is is…) yang ditolak; pemain sudah memberi dua blok |
| Satu kata = satu arti (there di sana / there is ada; one, cook, so, next, no) | `KATA` boleh punya elemen keenam `[[frase, arti, pos, keluarga]]`; kepingan tetap satu, isinya membawa `arti`, jaringan mengirimnya, pemain memilih arti menurut frase di kalimat |
| BENTUK leaves→leaf membuat verba "leaves" salah keping | `BENTUK_FRASE: [bentuk, kata, frase]`, juga di importer (`bentuk_frase`) |
| Varian benar ditolak (Have you got/Do you have, on Sundays, adverb di awal) | `accept` berlaku juga untuk latihan ketik (elemen ketiga) dan isian (elemen keempat), dan boleh memuat kata lain: importer menulis `texts`, server menerima teks yang cocok. Keterangan waktu di awal/akhir pernyataan dipindah otomatis (`timeMoves`) |
| "Don't cross the road." / "Have a nice weekend!" ditolak sebagai tanya tanpa "?" | do/don't/have dianggap tanya hanya bila diikuti subjek (`asksByStart`) |
| "T-shirt" di tengah kalimat ditolak pemeriksa kapital | Pola huruf kapital + tanda hubung adalah kata biasa |
| Pemain tidak memakai BENTUK: bentuk tak beraturan (children, men) tampil sebagai nama di label blok | Belum diperbaiki: jaringan belum mengirim peta bentuk ke pemain |
| Deck dan misi kanonik ditulis untuk pelajar umum (hotel, kantor, status menikah, lambang fonetik, kalimat diketik), padahal jalur KI mengajarkan unitnya di Kelas 3 (2026-11-21) | Misi varian per jenjang (ADR-0032) dengan deck jembatan `jb-<deck>-k34`. Audit per deck di `jenjang-inggris.md`. Generator menolak bab varian tanpa deck jembatan jenjangnya, tema varian yang bersandar pada varian lain, dan id tanpa awalan `pre-k34-` |
| Gerbang kartu mengambil batas Kelas 3 dari kelas pertama unit, sehingga deck SMP untuk unit yang juga ada di Kelas 3 dinilai sebagai deck Kelas 3 | `Deck.jenjang` menentukan batasnya (`aturan-kartu.ts`) |
| Misi Kelas 3–4 dengan rangkai kalimat dan uji diketik melampaui riset (Kelas 3 baru menyusun huruf, kalimat mulai Kelas 5) | Tema k34 hanya dengar lalu pilih dan isian satu kata (`latihan: []`). Isian ubin huruf di pemain misi masih kurang |
| A2 (2026-11-22): "When I get home, I'll call you." dan "What a beautiful view!" / "How brave!" ditolak sebagai tanya tanpa "?" | `asksByStart` menerima tanda akhir: kata tanya tanpa auxiliary sesudahnya bukan tanya bila seruan (What a/an …!, What/How + adjective/adverb …!) atau When/Where + anak kalimat dengan koma. Tanpa koma tetap dianggap tanya |
| A2: butir dua kalimat ("Oh no. Is there…?", "Phew! The bus…") dan titik koma ditolak | Potongan boleh berakhir `;` dan satu `.`/`!`/`?` di tengah (maks dua kalimat per butir, kalimat kedua kapital); aturan tanya dicek per kalimat (`sentenceParts`). Penilai longgar mengabaikan tanda di tengah seperti koma; tema `kapital` menilainya |
| A2: bentuk pendek we'll/you'd/he's (= has)/I'd better ditolak atau diterima salah (`I would better`) | Satu aturan di server (`grading/contract.go`) dan pemain (`contractions.ts`): 's dan 'd dibaca dari kata sesudahnya (been/got/V3 → has, V3 sebelum by/of/in… atau di akhir → has/is, tired/worried… → is; better/been/V3 → had, rather/lainnya → would). Isian memakai kata sesudah ___ |
| A2 (E2l): "…, right?" / "…, OK?" dan "And what does … mean?" ditolak sebagai tanda tanya tanpa kata tanya; titik dua di tengah ditolak | Tag right/OK/okay/yes/yeah sesudah koma di akhir, dan and/so/but/or + kata tanya di awal, dihitung tanya. Potongan boleh berakhir `:`; penilai longgar mengabaikannya, dan kalimat kata dengan tahun atau titik dua tidak lagi dibaca sebagai kalimat bilangan (`numberSentence`) |
| A2: tahun (2019) bukan potongan | Tahun 1000–2099 boleh jadi potongan, bukan kepingan (seperti nama) |
| A2 (E2i): kalimat langsung dengan petik tidak bisa dipakai | Petik lurus `"` di awal/akhir potongan, berpasangan; kalimat boleh berakhir `."`; aturan tanya dicek di dalam petik. Penilai longgar membuang petik, petik lengkung = lurus; tema `kapital` menilai petik dan tanda di dalamnya. Petik tunggal sebagai kutipan tidak didukung (bentrok dengan apostrof) |
| `timeMoves` memindah keterangan waktu keluar dari anak kalimat ("Last year, he has worked here since.", "Yesterday, this is the bag which I bought.") | Tidak memindah bila sisa kalimat memuat pembuka anak kalimat (when, if, because, since, that + subjek, who, which…), dua kalimat, `;`, atau petik |

## Belum diselesaikan

- **Deck terlalu berat untuk levelnya:**
  - Level 1: `data-mengumpulkan` (populasi dan sampel), `ukur-jam` (zona waktu), `datar-posisi-arah` (derajat), `datar-kenal-bangun` (rumus Euler), `datar-susun-urai` (luas trapesium), bilangan ribuan sampai jutaan.
  - Level 2: `datar-garis-sudut` (garis sejajar, sudut luar), `ukur-konversi` (desimal).
  - Kartu negatif di `pecahan-sederhana-banding` #31 dan faktor prima di `desimal-ubah-bentuk` #10–11.
- **Deck kanonik Level 1 yang melampaui "bilangan sampai 100"** (temuan penulis gambaran):
  - "Nilai Tempat" sampai 36.408 dan "Banyak Benda" sampai 4.060.
  - "Penjumlahan" dan "Pengurangan" memakai hitung bersusun empat angka.
  - Hanya deck Kelas 1–2 (`ki-k1-*`, `ki-k2-*`) yang bergaya SD awal.
  - "Menjumlah dan Mengurang Pecahan" (Level 3) sudah memakai pecahan campuran, padahal topik mengubah pecahan campuran baru ada di Level 4.
- **Deck pengukuran dan bilangan yang melampaui levelnya:**
  - `ukur-jam` (Level 1) memuat sistem 24 jam, perjalanan lewat tengah malam, jam desimal, dan zona waktu.
  - `ukur-tidak-baku` (Level 1) sudah memakai perkalian dan pembagian.
  - `ukur-satuan-baku` (Level 2) membahas konstanta Planck dan newton.
  - Deck pengukuran Level 2–3 sudah mengalikan desimal (3,5 × 1.000), padahal perkalian desimal baru diajarkan di Level 4.
  - `faktor-prima` (Level 3) memakai notasi √36.
- **Deck geometri yang melampaui levelnya:**
  - `datar-posisi-arah` (Level 1) memakai arah dalam derajat.
  - `datar-kenal-bangun` (Level 1) memuat rumus Euler.
  - `datar-susun-urai` (Level 1) memakai rumus luas segitiga.
  - `datar-garis-sudut` (Level 2) sebenarnya materi Kelas 7.
  - `datar-busur-juring` (Level 6) memuat radian, yang biasanya materi SMA.
- **Deck pola dan data Level 1:**
  - Tidak ada deck baca-dengar untuk Kelas 1–2.
  - `pola-bukan-bilangan` memakai pembagian bersisa.
  - `data-mengumpulkan` berlatar SMP.
  - `data-turus-piktogram` memakai simbol yang mewakili beberapa benda, yang baru cocok untuk Kelas 3.
  - `data-tabel-frekuensi` (Level 2) memakai persen.
- **Deck bangun ruang dan peluang yang melampaui levelnya:**
  - `ruang-jaring-unsur` (Level 3) memakai π dan juring, padahal keliling lingkaran baru diajarkan di Level 6.
  - `ruang-volume-kubus-satuan` (Level 2) memakai s³.
  - `peluang-kemungkinan` (Level 3) memakai peluang sebagai pecahan, komplemen, dan kekeliruan penjudi. Padahal CP Fase C hanya meminta kemungkinan dinyatakan dengan kata-kata.
  - `peluang-saling-bebas` (SMA) membahas kebebasan berpasangan dan bersama, yang setara materi kuliah.
- **Deck fungsi dan persamaan Level 5–6 yang melampaui SMP:**
  - `fungsi-domain-range` memakai notasi interval, daerah asal fungsi akar dan pecahan, dan istilah surjektif.
  - `fungsi-representasi` memuat fungsi kuadrat dan eksponen.
  - `linear-spldv` memuat variabel di penyebut.
- **Deck statistik dan penalaran Level 5–6 yang melampaui SMP:**
  - `statistik-kuartil` memuat desil, persentil, dan rumus letak interpolasi.
  - `nalar-model` memuat model eksponen dan optimasi kuadrat.
  - `nalar-informasi` memakai format kecukupan data A–E ala UTBK.
  - Topik korelasi dan regresi diajarkan oleh deck `inferensi-regresi` dari koleksi Statistika Inferensial.
- **Deck SMA yang memakai materi sebelum waktunya:**
  - Deck akar dan menyusun persamaan kuadrat memakai akar kompleks sebelum bab bilangan kompleks. Keduanya sudah punya deck jembatan (J4). `kuadrat-diskriminan` (kartu "Jumlah dan hasil kali akar") juga menyebut akar kompleks di Level 7, dan belum dijembatani.
  - Deck induksi memuat induksi kuat dan prinsip urutan baik, yang setara materi kuliah.
- **Deck perguruan tinggi yang bahasanya masih gaya sekolah:**
  - Daftar deck: himpunan, bukti, logika orde satu, teori permainan, risiko, bentuk polar, De Moivre, akar kompleks, dan perkalian silang.
  - Bahasanya masih santai ("nggak"), dengan contoh warung dan Pramuka.
  - Kedalamannya juga di bawah gambaran versi perguruan tinggi.
  - Deck NPV (Level 10) memuat IRR dan anuitas abadi, yang melampaui silabus SMA.
- **Deck PT yang tipis untuk Level 12–14** (penulis gambaran, 2026-11-19). Ini dasar untuk deck jembatan PT dan batch P:
  - Mekanika pada dasarnya Fisika SMA (g = 10, lift, bidang miring licin). Impuls tidak memakai ∫F dt. Gerak harmonik tanpa redaman dan resonansi.
  - Kombinatorika: rekurensi tanpa akar kembar, nonhomogen, dan bagi-dan-taklukkan.
  - Unit "keterhitungan dan masalah henti" janggal di bab kombinatorika.
  - Semua deck `inferensi-*` (Level 12–14) setara statistika pengantar SMA. Konteksnya sekolah, dan tidak ada MLE, uji khi-kuadrat, uji t dua sampel, atau Bayes.
  - Soal di `numerik-galat` terlalu ringan.
  - `pd-orde-dua` dan `pd-sains-teknik` banyak tumpang tindih: redaman, resonansi, RLC, bahkan kartu pembukanya.
  - Dua prasyarat belum punya kartu kanonik: rumus Euler e^(iθ) di `pd-orde-dua` dan pecahan parsial di `pd-terpisah-linear`.
  - `numerik-akar` #0 menyebut polinomial berderajat 12. Yang benar 13, dan sudah diperbaiki.
- **Deck kalkulus SMA:**
  - `limit-makna` memuat definisi ε-δ, yang setara materi kuliah. `limit-kontinuitas` memuat diskontinuitas berayun dan aturan ujung selang tertutup. Keduanya sudah punya deck jembatan SMA (J4).
  - `limit-aljabar-trigono` hampir mengulang isi `limit-trigonometri`.
  - Integral substitusi dan volume benda putar ada di Level 12. Sudah dicek 2026-11-19: keduanya tidak termasuk TKA. TKA Matematika Lanjutan (045/H/AN/2025) berhenti di limit tanpa L'Hôpital, tanpa turunan dan tanpa integral. CP 2025 Fase F lanjut hanya meminta integral sebagai antiturunan dan luas, serta teorema dasar kalkulus. Level 12 dipertahankan dan tidak perlu kemasan TKA.

**Keputusan pemilik 2026-11-19 untuk semua temuan "deck melampaui level" di bagian ini (ADR-0030):**
- Deck kanonik tidak diubah.
- Untuk setiap level, kelas, atau jalur yang tidak cocok, ditambahkan deck jembatan `jb-*` di `src/content/kartu/jembatan/`.
- Misi level itu mengambil kartu dari deck jembatan lewat `kartu` di BAB.
- Kesalahan kartu (bagian "Kartu bermasalah") tetap diperbaiki di deck kanonik.
- **Kartu bermasalah** (ditangani 2026-11-19; sumbernya di `src/content/kartu/produksi/`, bukan `mtk/`):
  - `datar-luas-petak` #0: judulnya diganti menjadi "Ubin di lantai kamar", sesuai isinya.
  - `data-diagram-batang` #3: sumbu sampai 16 memang disengaja. Lab memberi ruang 1,5 kali data terbesar untuk menarik batang. Kalimatnya sekarang menjelaskan hal itu.
  - `statistik-kuartil` #22: penjelasannya sekarang menyebut syarat rumus letak, sama dengan #10.
  - `ruang-tampak` #2: dihitung ulang dari koordinat gambarnya. Ada 8 kubus, tampak depan 3-1-1, 5 petak atas, dan tampak kanan 2-3. Semuanya sesuai teks, jadi tidak ada yang diubah.
  - Pemakaian "÷" dan ":" tidak seragam. Masih terbuka.
- **Bentuk latihan yang diminta penulis:**
  - pecahan, desimal, dan akar di dalam kalimat
  - titik di bidang koordinat
  - hitung bersusun
  - membaca grafik
  - memilah dua kelompok
  - jam dan durasi
  - pangkat di atas 3 dan pangkat berhuruf (2⁵, 2^(x − 1)), karena mathKey hanya mengenal ² dan ³
  - tabel kebenaran B/S dan memilah argumen valid atau cacat
  - suku berindeks Uₙ dan Sₙ (supaya U₅ = S₅ − S₄ bisa ditulis)
  - sin, cos, tan dengan nilai pasti, dan membaca titik di lingkaran satuan
  - garis bilangan 0–20
  - mengikat puluhan
  - hasil bagi dan sisa
  - tabel tanda pertidaksamaan
  - dua akar sekaligus
- Setelah J3b, tema `l5-letak-persentil` ("Membaca Kuartil") mengajarkan JAK, sehingga beririsan dengan tema `l5-sebaran-*` di Level 5. Irisan ini dibiarkan. Unit kuartil juga ada di KI Kelas 8 dan 10; lihat "Unit yang sama di beberapa kelas".
- Setelah J3a, tiga prasyarat dibiarkan sebagai bekal umum: `l5-dr-syarat` ← `l5-ptlsv-negatif`, `l7-feks-arti`/`l7-parabola-bentuk` ← `l5-rep-tabel` (kini tanpa tabel kuadrat dan eksponen), dan `l7-maksmin-batas` ← `l5-dr-range` (kini tanpa puncak). Id `l5-dr-alami` dan `l5-dr-syarat` tidak lagi cocok dengan isinya ("Empat Cara Menyajikan", "Range dari Rumus").
- `pecahan-sederhana-banding` dan `desimal-ubah-bentuk` (Level 2) memakai FPB dan KPK yang baru diajarkan di Level 3. Kini dijembatani (J2b).
- Deck pengukuran Level 3 masih mengalikan desimal di satu-dua kartu: `ukur-luas-volume-debit` #16 dan #28, `ukur-majemuk` #25 dan #28, `datar-keliling-luas` #34. Tema misinya hanya menggeser koma, jadi tidak dibuatkan jembatan.
- Tema Level 2 `l2-frek-relatif` dan `l2-frek-kumulatif` sekarang berisi "Membaca Tabel" dan "Menjawab dari Beberapa Baris". Prasyarat Level 7 dialihkan ke `l2-frek-tabel`. Frekuensi relatif dan kumulatif diajarkan di deck Level 7 sendiri.
- Misi `l2-baku-penggaris` dulu menyebut "mulai dari tepi membuat hasilnya terlalu besar"; yang benar terlalu kecil. Diperbaiki di J2a.
- **Celah materi setelah jembatan SD.** Sejak J2a, jembatan `datar-garis-sudut` (Level 2) tidak lagi mengajarkan sudut pelurus, penyiku, bertolak belakang, sudut pada garis sejajar, sudut luar segitiga, dan jumlah sudut segitiga. Akibatnya tidak ada misi Level 1–7 yang mengajarkannya, padahal `datar-sudut-keliling` (Level 8) membutuhkan sudut luar segitiga. Perlu misi SMP (Kelas 7) dari bagian deck kanonik itu. Masalah ini masuk keputusan "unit di beberapa kelas".
- **Unit yang sama di beberapa kelas (keputusan terbuka).** Di jalur Kurikulum Indonesia, unit seperti banyak-benda, nilai-tempat (Kelas 1–5), hubungan-garis-sudut (Kelas 3 dan 7), dan jaring-unsur (Kelas 6 dan 9) muncul di lebih dari satu kelas. Masalahnya:
  - Deck jembatan didaftarkan per jalur dan per unit, sehingga salinan `-ki` versi SD ikut tampil di kelas SMP.
  - Misi terikat ke deck kanonik, sehingga misi Level 2 juga muncul di Kelas 7.
  - Pilihan solusi: tandai deck jembatan dengan jenjangnya lalu saring per kelas di web, atau buat misi per jenjang untuk unit yang diajarkan ulang.
  - **Diputuskan untuk Bahasa Inggris (ADR-0032, 2026-11-21):** misi per jenjang. `Deck.jenjang`, `Bab.varian`/`Tema.varian` di generator Inggris, saringan `misiUntuk` di beranda. Matematika belum memakainya.
- `susun.ts` (kartu hitung bersusun) menulis "koma di bawah koma" juga untuk bilangan cacah. Sudah diperbaiki 2026-11-19: tanpa desimal, teksnya "satuan di bawah satuan, puluhan di bawah puluhan".
- Di jalur Kurikulum Indonesia, unit banyak-benda dan nilai-tempat juga ada di Kelas 3–5. Deck jembatan J1a hanya untuk Kelas 1–2, jadi kelas di atasnya memakai deck kanonik. Ini belum diputuskan.
- `data-histogram` #12–13 memakai aturan Sturges (log) di Level 7, tetapi tidak ada prasyarat ke tema logaritma `l7-peks-log`. Siswa bisa bertemu log sebelum diajarkan. Prasyarat tidak ditambah karena rantai Level 7 sudah 11 dari batas 12.
- Generator membuang kemampuan yang `needs`-nya tidak ada tanpa memberi tahu, dan kalimat kemampuan tidak dihitung (temuan K56, 2026-11-19). Sekarang keduanya menjadi galat. Dua kalimat Level 7 yang memakai huruf tanpa nilai (`g = 47 − 32` dan `4a + 2b + c = 3`) ditulis ulang dengan bilangan. Kalimat kemampuan berhuruf hanya boleh berupa identitas.
- `inferensi-regresi` (Level 8) #26 "Regresi menuju rata-rata" (ŷ = r·x dalam satuan baku) adalah pengayaan di atas SMA. Kartu ini belum dijembatani, tetapi tetap dipakai di pilih `l8-regresi-hati`.
- Jembatan `jb-fungsi-domain-range` (J3a) membuang domain alami fungsi akar dan pecahan, padahal `fungsi-akar` #2 dan `fungsi-rasional` #1 (Level 9) merujuknya. Tema Level 9 mengajarkannya ulang.
- Nilai mutlak berhuruf (`|x − 3| = 5`) belum didukung `holds`/`algebraJs`, karena `|` tidak diubah menjadi `Math.abs`.
- Kalimat kompleks: identitas berhuruf dengan i belum memakai i² = −1, dan `(a + bi)(c + di)` tanpa × ditolak mathKey. Slug `vektor-dot-cross` menyesatkan, karena isinya hanya hasil kali titik.
- `limit-aljabar-trigono` #19 merujuk "lim sin x/x dari bab makna limit", padahal jembatan `jb-limit-makna` tidak memuatnya. Rujukan bekal itu tidak cocok untuk jalur yang memakai jembatan.
- Catatan kartu Level 11:
  - `kerucut-hiperbola` #16 melebih-lebihkan: pada e = 3 kemiringan asimtot baru 2,83, belum tegak.
  - `koordinat-lingkaran` #36 berjudul "Enam kedudukan", padahal tabel #35 hanya punya lima baris.
  - `acak-harapan` #23 dan `acak-binomial` saling merujuk silang.
- Pecahan parsial tidak diajarkan unit kanonik mana pun (`integral-teknik` #40, `pd-terpisah-linear`). Jembatan `jb-integral-teknik` memberi satu kartu ringkas. `multi-fungsi` #29 dulu menjanjikan bab optimisasi yang tidak ada; kalimatnya diperbaiki 2026-11-20.
- Istilah belum seragam: "terbilang" dan "terhitung" untuk *countable*; "teorema sisa Tiongkok" di kanonik, "teorema sisa Cina" di deck jembatan.
- Impor: generator dengan `MISI_LEVELS=<satu level>` gagal kalau prasyaratnya menunjuk level lain. Selalu tulis semua level, lalu impor.
- **Pertidaksamaan dengan operasi di satu ruas** (mis. `3 × 3 × 3 × 3 × 3 > 27`) jangan dipakai sebagai latihan. Bentuk "isi" bisa mengosongkan ruas kanan, padahal banyak bilangan memenuhi. Pakai perbandingan dua bilangan saja (temuan penulis Level 7).
- `eksponen-fungsi` #28 menyebut y = 2ˣ dan y = x² berpotongan di (2, 4) dan (4, 16). Ada titik potong ketiga di x ≈ −0,77, di luar gambar. Kartunya masih benar untuk x positif, tetapi kalimatnya sebaiknya menyebut syarat itu.
- `multi-fungsi` Contoh 7 menjanjikan optimisasi multivariabel (Hessian, Lagrange), padahal tidak ada unit kanonik yang mengajarkannya. Ini celah di kanonik.
- **Level 7 sisa dan Level 8–14** belum dibuat.
