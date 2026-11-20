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

## Lain-lain
- [x] K56 KEMAMPUAN untuk keenam file Level 5–6
- [ ] Tinjauan akhir: peninjau (brief-peninjau-misi.md) per level yang baru, setelah semua misinya masuk
- [ ] Impor lokal per level, uji kering importer, lalu uji main sungguhan dengan akun login (perlu izin pemilik untuk token QA)
