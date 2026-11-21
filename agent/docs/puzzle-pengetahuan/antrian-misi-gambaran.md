# Antrean penyelesaian misi, gambaran, dan kartu jembatan

Disusun 2026-11-19 atas permintaan pemilik: "selesaikan semuanya". Batasnya dua agen sekaligus. Koordinator menjalankan generator penuh, importer lokal, dan `bun scripts/gambaran.ts`. Status: `[ ]` belum, `[~]` jalan, `[x]` selesai dan terimpor ke DB lokal.

Urutan: kartu jembatan SMA dan PT dikerjakan sebelum misi yang memakai deck itu.

## Gambaran bab (brief-penulis-gambaran.md)
- [x] G1 probability.random_variables, modeling.optimization_operations
- [x] G2 algebra.linear_algebra, calculus.multivariable
- [x] G3 discrete.combinatorics_graphs, modeling.mechanics
- [x] G4 modeling.numerical_computation, statistics.inference
- [x] G5 analysis.differential_equations, analysis.real
- [x] G6 number_theory.elementary, analysis.advanced
- [x] G7 discrete.foundations, geometry.differential
- [x] G8 modeling.stochastic_processes, number_theory.algebraic

## Kartu jembatan (brief-penulis-jembatan.md, ADR-0030)
- [x] J1a `sd-awal-a` SD awal, bilangan (misi `l01-bilangan.ts`): cacah-banyak-benda, cacah-nilai-tempat, cacah-tambah, cacah-kurang
- [x] J1b `sd-awal-b` SD awal, ukur dan bentuk (`l01-ukur-bentuk.ts`): ukur-jam, ukur-tidak-baku, datar-posisi-arah, datar-kenal-bangun, datar-susun-urai
- [x] J1c `sd-awal-c` SD awal, data dan pola (`l01-ukur-bentuk.ts` atau `l01-bilangan.ts`, sesuai letak BAB-nya): data-mengumpulkan, data-turus-piktogram, pola-bukan-bilangan
- [x] J2a `sd-a` SD, ukur dan bangun (`l02-*`, `l03-*`): datar-garis-sudut, ukur-konversi, ukur-satuan-baku, ruang-volume-kubus-satuan, ruang-jaring-unsur
- [x] J2b `sd-b` SD, bilangan dan data (`l02-*`, `l03-*`): data-tabel-frekuensi, peluang-kemungkinan, faktor-prima, pecahan-tambah-kurang, pecahan-sederhana-banding, desimal-ubah-bentuk, dan deck pengukuran Level 2–3 yang mengalikan desimal
- [x] J3a `smp-a` SMP, fungsi dan persamaan (`l05-*`, `l06-*`): fungsi-domain-range, fungsi-representasi, linear-spldv
- [x] J3b `smp-b` SMP, data dan penalaran (`l05-*`, `l06-*`): statistik-kuartil, nalar-model, nalar-informasi, datar-busur-juring
- [x] J4 `sma` SMA (`l07-kuadrat.ts`; deck lain sebelum misinya ditulis): kuadrat-akar, kuadrat-susun, deret-induksi, peluang-saling-bebas, limit-makna, limit-kontinuitas, keuangan-npv

## Misi (brief-penulis-misi.md)
- [x] M7a `l07-eksponen-logika`: eksponen-fungsi, eksponen-persamaan, eksponen-pertumbuhan, pertidaksamaan-eksponen, terapan-bunga, logika-pernyataan, logika-penghubung, logika-kesimpulan
- [x] M7b `l07-barisan-trigono`: barisan-aritmetika, barisan-geometri, deret-aritmetika, deret-geometri, deret-tak-hingga, trigono-perbandingan, trigono-sudut-istimewa
- [x] M7c `l07-data-peluang`: data-box-plot, data-histogram, statistik-berkelompok, statistik-keputusan, statistik-sebaran, peluang-bersyarat, peluang-majemuk, peluang-saling-bebas (setelah J4)
- [x] M8a `l08-fungsi-deret`: fungsi-invers, fungsi-komposisi, fungsi-transformasi, deret-induksi (setelah J4), deret-sigma, datar-singgung-tali-busur, datar-sudut-keliling
- [x] M8b `l08-data-optimasi`: data-diagram-pencar, inferensi-regresi, statistik-kontingensi, optimasi-objektif, terapan-program-linear
- [x] M9a `l09-fungsi-logaritma`: fungsi-akar, fungsi-logaritma-grafiknya, fungsi-nilai-mutlak, fungsi-rasional, fungsi-tangga, logaritma-makna, logaritma-persamaan, logaritma-sifat
- [x] M9b `l09-polinom-matriks`: identitas-polinomial, polinom-faktor, polinom-operasi, polinom-teorema-sisa, matriks-determinan, matriks-jenis, matriks-operasi, matriks-sistem-linear
- [x] M9c `l09-trigono`: relasi-sudut-empat-kuadran, trigono-aturan, trigono-grafik, trigono-identitas, trigono-persamaan, trigono-radian
- [x] M9d `l09-vektor-kompleks`: kompleks-imajiner, kompleks-operasi, koordinat-komposisi, transformasi-geometri-matriks, vektor-dasar, vektor-dot-cross, vektor-proyeksi
- [x] M10a `l10-ruang-peluang`: ruang-jarak-sudut, ruang-kedudukan, ruang-proyeksi-irisan, vektor-di-ruang, peluang-aturan-cacah, peluang-permutasi-kombinasi
- [x] M10b `l10-keuangan-nalar`: keuangan-npv (setelah J4), terapan-anuitas, nalar-keputusan, nalar-strategi
- [x] M11a `l11-limit-turunan`: limit-makna, limit-aljabar-trigono, limit-trigonometri, limit-tak-hingga, limit-kontinuitas (setelah J4), turunan-makna, turunan-aturan
- [x] M11b `l11-turunan-integral`: turunan-garis-singgung, turunan-kemonotonan, turunan-optimasi, turunan-trigono, integral-tak-tentu, integral-tentu, integral-luas
- [x] M11c `l11-kerucut-acak`: kerucut-parabola, kerucut-elips, kerucut-hiperbola, kerucut-umum, koordinat-lingkaran, acak-variabel, acak-harapan, acak-binomial, acak-normal

## Perguruan tinggi: deck akademik jembatan dan misi sekaligus (Level 12–14)
Hampir semua deck Level 12–14 bergaya sekolah ("nggak", "kamu", contoh sehari-hari). Satu agen per batch membaca deck kanonik, menulis deck jembatan akademik `jb-*` di `jembatan/pt-<batch>.ts` untuk jalur `matematika-berurutan` (ditulis ulang lengkap dalam bahasa akademik dan sedalam perguruan tinggi; boleh dilewati kalau deck kanonik sudah akademik, dengan alasan di laporan), lalu menulis misinya di `misi-level/l<batch>.ts` dengan `kartu: "jb-…"`.
- [x] P12a distribusi-poisson, inferensi-sampling, keuangan-risiko, keuangan-permainan
- [x] P12b integral-teknik, integral-volume-putar, turunan-implisit, multi-fungsi
- [x] P12c numerik-akar, numerik-interpolasi, mekanika-kinematika, optimasi-transportasi, graf-rekurensi
- [x] P12d kompleks-polar, vektor-hasil-kali-silang, linalg-ruang-vektor, logika-himpunan, logika-pembuktian
- [x] P13a inferensi-estimasi, mekanika-dinamika, multi-gradien, numerik-galat
- [x] P13b pd-model-orde-satu, real-supremum, teori-euklid, kompleks-de-moivre
- [x] P13c graf-lintasan, graf-pencacahan, linalg-basis, logika-orde-pertama
- [x] P14a abstrak-grup, abstrak-ring, abstrak-modul, abstrak-galois, abstrak-homologi
- [x] P14b teori-prima, teori-kongruensi, teori-fermat-euler, teori-modular
- [x] P14c fondasi-zfc, fondasi-kardinal, fondasi-pilihan, fondasi-godel
- [x] P14d graf-pohon, graf-keterhitungan, kompleks-akar, lanjut-kompleks
- [x] P14e real-epsilon-delta, real-konvergen, real-nilai-rata-rata, real-riemann
- [x] P14f lanjut-konvergensi, lanjut-lebesgue, lanjut-banach-hilbert, lanjut-pdp
- [x] P14g difgeo-kurva, difgeo-kelengkungan, difgeo-manifold, difgeo-riemann, difgeo-stokes
- [x] P14h multi-garis-permukaan, multi-lipat, linalg-transformasi, linalg-eigen
- [x] P14i linalg-diagonal, linalg-ortogonal, numerik-dekomposisi, numerik-sistem-besar, numerik-beda-hingga
- [x] P14j inferensi-hipotesis, inferensi-anova, inferensi-korelasi, stokastik-markov
- [x] P14k stokastik-poisson, stokastik-martingale, stokastik-ito, stokastik-keuangan
- [x] P14l mekanika-harmonik, mekanika-momentum, optimasi-nonlinear, optimasi-dualitas
- [x] P14m pd-terpisah-linear, pd-orde-dua, pd-sains-teknik

## Bahasa Inggris sampai A2 (brief-penulis-misi-inggris.md)
Generator `titian-web/scripts/misi-inggris.ts`, satu file batch per agen di `scripts/misi-inggris/`, didaftarkan di `index.ts`. Impor ke subject `english` dengan berkas `data/puzzle/en-kanonik*.json` (bukan `en.json`, yang milik ekspor game). Level CEFR: Pre-A1 = 0, A1 = 1, A2 = 2. Batch disusun urut prasyarat kanonik; yang bertanda "setelah" menunggu batch itu selesai. Dua batch tanpa tanda saling bergantung boleh jalan bersamaan.

Pre-A1 (pilot, 18 deck, 47 misi; lolos `MISI_CEK` dan uji kering importer 2026-11-21, menunggu `-apply`):
- [x] E0a `pre-a1-a`: sounds-alphabet, pronoun-subject, verb-be, det-articles, det-demonstrative, sent-word-order, sent-questions, vocab-greetings
- [x] E0b `pre-a1-b`: vocab-numbers-time, vocab-classroom-language, vocab-clothes-colours, vocab-toys, vocab-shapes, vocab-food-drink, speak-introducing, speak-requests, speak-wants, listen-numbers-spelling

A1 (57 deck):
- [x] E1a `a1-a` bunyi dan tulisan: sounds-vowels, sounds-consonants, sounds-phonics, sounds-numbers, write-capitals-punctuation
- [x] E1b `a1-b` noun: noun-pengertian, noun-common-proper, noun-plural-regular, noun-countable-uncountable, noun-plural-irregular
- [x] E1c `a1-c` pronoun dan determiner: pronoun-object, pronoun-demonstrative, pronoun-interrogative, det-possessive, noun-possessive
- [x] E1d `a1-d` kelas kata (setelah E1b): verb-definition, adj-definition, adv-time-place, det-quantifiers, det-numbers
- [x] E1e `a1-e` Present Simple: tense-present-simple, verb-auxiliary, sent-negatives, adv-frequency, vocab-daily-routine
- [x] E1f `a1-f` tense dan modal (setelah E1e): tense-present-continuous, tense-past-simple, modal-ability, modal-permission, sent-imperative
- [x] E1g `a1-g` tempat, waktu, sambung (setelah E1b): prep-place, conj-coordinating, sent-there-is, sent-linkers-sequence, vocab-calendar, prep-time
- [x] E1h `a1-h` kosakata 1: vocab-family, vocab-home, vocab-school, vocab-body-health, vocab-clothes
- [x] E1i `a1-i` kosakata 2 (setelah E1d): vocab-appearance, vocab-weather-nature, vocab-animals, vocab-feelings, vocab-synonyms-antonyms
- [x] E1j `a1-j` berbicara (setelah E1e, E1f, E1g): speak-personal-info, speak-ordering-shopping, speak-directions, speak-likes, speak-suggestions
- [x] E1k `a1-k` membaca, menyimak, menulis (setelah E1a, E1d, E1f): read-short-functional, read-descriptive, listen-instructions, write-sentences, write-forms-messages, write-descriptive

A2 (74 deck, semua setelah A1):
- [ ] E2a `a2-a` bunyi dan kata: sounds-minimal-pairs, sounds-silent-letters, sounds-word-stress, interjection, noun-compound
- [ ] E2b `a2-b` noun dan pronoun: noun-concrete-abstract, noun-collective, noun-functions, pronoun-possessive, pronoun-reflexive, pronoun-indefinite
- [ ] E2c `a2-c` adjective dan adverb: adj-order, adj-comparative, adj-superlative, adj-ed-ing, adv-manner, adv-degree
- [ ] E2d `a2-d` verb: verb-action-state, verb-modal-overview, verb-forms, verb-gerund-infinitive, prep-movement
- [ ] E2e `a2-e` lampau dan perfect (setelah E2d): tense-past-continuous, tense-used-to-would, tense-present-perfect, speak-experiences, read-recount
- [ ] E2f `a2-f` future: tense-future-will, tense-future-going-to, tense-future-present-forms, tense-compare-present, speak-arrangements
- [ ] E2g `a2-g` modal: modal-obligation, modal-advice, modal-possibility, speak-advice, sent-so-neither
- [ ] E2h `a2-h` klausa: conj-subordinating, pronoun-relative, sent-compound-sentences, sent-time-clauses, sent-relative-defining
- [ ] E2i `a2-i` kalimat lanjut (setelah E2d, E2f): sent-purpose-result, sent-conditional-0-1, sent-direct-speech, read-procedure, read-narrative
- [ ] E2j `a2-j` kosakata 1: vocab-town-directions, vocab-shopping-money, vocab-travel-transport, vocab-jobs-work, vocab-hobbies-sport
- [ ] E2k `a2-k` kosakata 2 dan pendapat: vocab-personality, vocab-plants, vocab-measurement, speak-opinions, speak-compliments, speak-certainty
- [ ] E2l `a2-l` berbicara (setelah E2a, E2i): speak-reactions, speak-clarification, speak-sympathy-apology, speak-retelling, listen-announcements
- [ ] E2m `a2-m` membaca dan menyimak: read-scanning, read-skimming, read-multimodal, listen-conversations, listen-main-idea
- [ ] E2n `a2-n` menulis (setelah E2e, E2h, E2i): write-paragraph, write-social-media, write-multimodal, write-email-informal, write-recount, write-procedure

Sesudah tiap level: peninjau dengan `brief-peninjau-misi.md` (bagian Bahasa Inggris di `temuan-misi.md`), lalu koordinator menjalankan generator penuh dan importer.

## Bahasa Inggris per jenjang (ADR-0032, brief-penulis-jenjang-inggris.md)
Audit: `jenjang-inggris.md`. Satu agen per batch menulis deck jembatan di `src/content/kartu/jembatan/en-<jenjang>-<batch>.ts` (jalur `inggris-kurikulum-indonesia`, slug `jb-<deck>-<jenjang>`) dan misi varian di `scripts/misi-inggris/<level>-<jenjang>-<batch>.ts`. Satu file misi boleh memuat deck Pre-A1 dan A1. Batch disusun mengikuti urutan kelas dan prasyarat kanonik. Kelas 5–6 dan SMP tidak dikerjakan sebelum Kelas 3–4 selesai.

Kelas 3–4 (`k34`, 56 deck; Kelas 3 lebih dulu):
- [x] EK34a pilot: vocab-greetings, sounds-alphabet, speak-introducing, det-articles, vocab-numbers-time (11 misi, terimpor ke DB lokal 2026-11-21)
- [x] EK34b kata ganti dan be: pronoun-subject, verb-be, det-demonstrative, pronoun-demonstrative, det-possessive
- [x] EK34c benda (setelah EK34a): noun-common-proper, noun-plural-regular, noun-plural-irregular, noun-possessive, adj-definition
- [x] EK34d kalimat dan tanya (setelah EK34b): sent-word-order, sent-questions, pronoun-interrogative, sent-there-is, prep-place
- [x] EK34e kosakata rumah dan sekolah: vocab-clothes-colours, vocab-family, vocab-home, vocab-school, vocab-appearance
- [x] EK34f kegiatan (setelah EK34b): tense-present-simple, tense-present-continuous, vocab-daily-routine, speak-likes
- [x] EK34g bicara dan menulis Kelas 3 (setelah EK34d): speak-personal-info, write-capitals-punctuation, write-sentences, write-descriptive
- [x] EK34h Kelas 4 kosakata 1: vocab-toys, vocab-shapes, vocab-food-drink, vocab-clothes, vocab-body-health
- [x] EK34i Kelas 4 kosakata 2 dan waktu: vocab-weather-nature, vocab-feelings, vocab-calendar, prep-time, det-numbers
- [x] EK34j Kelas 4 bunyi (setelah EK34a): sounds-vowels, sounds-consonants, sounds-phonics, sounds-numbers
- [x] EK34k Kelas 4 kalimat (setelah EK34f): pronoun-object, verb-auxiliary, sent-negatives, sent-imperative, modal-ability
- [x] EK34l Kelas 4 bicara (setelah EK34k): adv-frequency, sent-linkers-sequence, speak-requests, speak-suggestions

Kelas 5–6 (`k56`, 6 deck):
- [x] EK56a tense dan jumlah: det-quantifiers, tense-present-simple, tense-past-simple
- [x] EK56b fungsi bahasa: speak-ordering-shopping, speak-directions, write-forms-messages

SMP dan SMA: tidak ada batch. Keduanya memakai misi umum.

Sesudah tiap batch, koordinator menjalankan `bun scripts/periksa-kartu.ts jb-`, `MISI_CEK=1 bun scripts/misi-inggris.ts`, generator penuh, `bun scripts/daftar-deck.ts`, uji kering importer, `-apply`, dan `bun test src/components/puzzle/belajar/varian.test.ts`.

## Lain-lain
- [x] K56 KEMAMPUAN untuk keenam file Level 5–6
- [ ] Tinjauan akhir: peninjau (brief-peninjau-misi.md) per level yang baru, setelah semua misinya masuk
- [ ] Impor lokal per level, uji kering importer, lalu uji main sungguhan dengan akun login (perlu izin pemilik untuk token QA)

### Catatan koordinator Bahasa Inggris
- Prasyarat lintas batch dari E1c sudah ditambahkan koordinator (a1-punya-apostrof ← a1-jamak-s, a1-tanyaganti-pelaku ← a1-present-s).
- Temuan kartu kanonik A1 dari penulis (bentuk lampau sebelum Past Simple, comparative/continuous sebelum waktunya) dikumpulkan untuk ditinjau setelah A1 selesai; kartu kanonik tidak diubah oleh penulis.
- Temuan kanonik dari penulis jenjang (untuk satu putaran perbaikan setelah k34 selesai): vocab-body-health #2/#7 foot ≠ "telapak kaki"; cara baca memakai "ö" (circle, shirt, skirt, T-shirt) bukan ejaan Indonesia.
- Tautan EK34c ke EK34b sudah ditambahkan koordinator.
- en/sounds.ts (deck sounds-consonants lama, sudah ditimpa produksi): kartu pasangan bersuara menaruh /ʃ/–/tʃ/ sebagai pasangan; keduanya tak bersuara. Bersihkan saat putaran kanonik.
- vocab-feelings di DECKS ber-level A2, padahal kanonik/audit A1 — seragamkan. Kartu sort hanya dua kelompok (penulis k34 terpaksa memindah pemilahan tiga kelompok ke misi).
- Generator belum menegakkan aturan isi per jenjang (k34 latihan: [], k56 rangkai ≤6 kata, ≤2 istilah per deck) — tambahkan pemeriksaan.
- Gerbang kartu E12 tidak mengizinkan latihan formulir/ubin di A1 (dilaporkan EK56b); generator menolak pertanyaan gema dan butir dua kalimat.
