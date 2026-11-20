# Brief penulis gambaran bab

Gambaran bab dan sub-bab menjelaskan apa yang dipelajari, kenapa, posisinya di Matematika, penerapannya, dan kaitannya dengan bidang lain (ADR-0029). Satu agen menulis satu file `titian-web/scripts/gambaran/matematika/<kode-bab>.ts`. Contoh lengkap: `number.real_exponents_roots.ts`. Format dan pemeriksaannya ada di `scripts/gambaran/tipe.ts` dan `scripts/gambaran.ts`.

## Ditulis untuk siapa

Tulis satu versi bab untuk setiap jenjang tempat bab itu diajarkan. Pemeriksa menyebut jenjang mana saja yang wajib ada. Sub-bab ditulis sekali, untuk jenjang levelnya sendiri (kolom `jenjang` di keluaran). Gaya, contoh, dan kedalaman mengikuti pembacanya.

| Jenjang | Pembaca | Bahasa | Contoh dan tantangan |
|---|---|---|---|
| `sd-awal` | Kelas 1–2, belum lancar membaca. Teks akan dibacakan | Kalimat sangat pendek, kata sehari-hari, tanpa istilah asing | Benda di rumah dan sekolah: kue, kelereng, jam dinding. Tantangan dengan bilangan kecil |
| `sd` | Kelas 3–6 | Kalimat pendek dan jelas. Istilah dikenalkan dengan contoh | Belanja di warung, kebun sekolah, jadwal, peta kampung |
| `smp` | Kelas 7–9 | Istilah matematika yang tepat dengan penjelasan singkat | Ponsel, kuota, ojek, berita, olahraga, IPA SMP |
| `sma` | Kelas 10–12, TKA SMA, UTBK | Lebih abstrak: model, fungsi, alasan | Ekonomi, sains, teknologi, keputusan berbasis data, persiapan kuliah |
| `pt` | Perguruan tinggi | Bahasa akademik yang tetap jernih | Riset, industri, rekayasa, ilmu data, keuangan |

## Mutu

- Fakta dan angka harus benar dan bisa dicek. Angka dunia nyata diberi kata "sekitar" bila dibulatkan. Hitung ulang setiap tantangan.
- Tidak ada basa-basi, ajakan kosong, atau kalimat promosi. Setiap kalimat memberi informasi.
- Pertanyaan bab adalah pertanyaan nyata yang benar-benar bisa dijawab setelah bab selesai.
- Penerapan nyata datang dari konteks PISA yang berbeda (pribadi, pekerjaan, masyarakat, ilmiah) dan cocok untuk umur pembacanya.
- Tantangan bergaya PISA: situasi dengan data yang cukup, lalu tiga pertanyaan berurutan untuk merumuskan, menerapkan, dan menafsirkan. Pertanyaan menafsirkan meminta siswa menilai sebuah klaim atau hasil dalam situasinya.
- Istilah adalah kata yang harus dibaca dengan tepat di soal bab ini.
- Baca deck kartu bab itu (`src/content/kartu`) supaya gambaran sejalan dengan materinya. Jangan menjanjikan materi yang tidak ada.

## Penulisan

- Halaman gambaran menampilkan teks polos. Tulis matematika dengan karakter Unicode biasa (², ³, √, ²log, ≤, π), bukan markup deck seperti `@log{a}`.
- Angka rekaan ditandai "rekaan". Peraturan yang dikutip harus benar, dan disebut nomornya hanya kalau penulis yakin.
- Cocokkan dengan deck yang benar-benar dimuat aplikasi lewat `src/content/kartu/index.ts`. Deck produksi dan lengkap bisa berbeda dari deck dasar.

## Periksa

`cd titian-web && GAMBARAN_CEK=1 bun scripts/gambaran.ts` harus lolos (hanya memeriksa, tidak menulis), lalu `../agent/tools/batas-ram.sh 3G bunx tsc --noEmit -p .` (dari folder titian-web; tsc memakan ±2 GB, jadi selalu lewat pembatas RAM ini). Kalau ada perintah yang ditolak sistem izin, jangan coba cara lain; laporkan.

## Batas kerja

Kerjakan sendiri. Jangan menjalankan agen atau subagen lain: pemilik membatasi dua agen sekaligus.
