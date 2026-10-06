#!/usr/bin/env python3
"""
Generator dan validator Bab 43 Matematika Kelas 2 SD:
"Soal Cerita Penjumlahan dan Pengurangan: Menentukan Operasi yang Tepat" (Fase A)
bab_id: ae44139c-9144-4e05-b74f-0d8ee0710283
article_id: fd2b88ad-ed8d-4fae-a881-2da744d5768e
quiz_id: 119ca960-cad0-492a-a83f-89eae4cd31ba
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "e8f9a0b1c201"  # Kata Kunci Penjumlahan
S2 = "f9a0b1c2d302"  # Kata Kunci Pengurangan
S3 = "a0b1c2d3e403"  # Langkah Memecahkan Soal Cerita
S4 = "b1c2d3e4f504"  # Soal Cerita Dua Langkah

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Soal cerita bercerita tentang kejadian nyata.
Kita perlu mencari kata kunci penjumlahan.
Kata kunci seperti diberi lagi dan membeli.
Kata seluruhnya juga tanda penjumlahan.
Benda bertambah banyak jika dijumlahkan.
Gabungkan bilangan menjadi satu jumlah.
Perhatikan kata ceritanya dengan cermat!

:::definition
title: Kata Kunci Penjumlahan
Kata kunci penjumlahan menandakan jumlah benda bertambah banyak.
:::"""

s2_content = """Kadang benda berkurang atau hilang.
Ini adalah tanda operasi pengurangan.
Kata kuncinya adalah sisa atau pecah.
Diberikan kepada teman juga pengurangan.
Kata selisih mencari perbedaan dua bilangan.
Benda menjadi lebih sedikit jumlahnya.
Pilihlah tanda kurang dengan tepat!

:::steps
title: Menemukan Kata Pengurangan
1. Cari kata seperti sisa, hilang, atau rusak.
2. Periksa apakah benda bertambah sedikit.
3. Gunakan tanda kurang untuk menghitung.
:::"""

s3_content = """Memecahkan soal cerita sangat mudah.
Pertama, baca soal sampai selesai.
Kedua, temukan apa yang diketahui.
Ketiga, tentukan apa yang ditanyakan.
Keempat, tuliskan kalimat matematikanya.
Kelima, hitung jawabannya dengan teliti.
Keenam, periksa kembali hasil hitunganmu.
Jawabanmu pasti benar dan tepat!"""

s4_content = """Beberapa soal cerita membutuhkan dua langkah.
Mula-mula Beni punya 35 kelereng.
Paman memberi Beni 20 kelereng lagi.
Lalu 12 kelereng diberikan adik.
Pertama, jumlahkan 35 tambah 20 jadi 55.
Kedua, kurangkan 55 kurang 12 jadi 43.
Sisa kelereng Beni ada 43 butir.

:::common_trap
title: Terburu-buru Memilih Operasi
Jangan langsung menjumlahkan semua angka.
Pahami alur kejadian pada cerita.
Pastikan kapan bertambah dan kapan berkurang!
:::

:::callout
variant: summary
title: Ringkasan
text: Baca cerita sampai selesai. Cari kata kunci bertambah atau berkurang. Selesaikan soal dua langkah secara berurutan.
:::"""

sections = [
    {
        "id": S1,
        "title": "Kata Kunci Penjumlahan",
        "minutes": 6,
        "goal": "Siswa mampu mengidentifikasi kata kunci yang menandakan operasi penjumlahan dalam soal cerita.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Kata Kunci Pengurangan",
        "minutes": 6,
        "goal": "Siswa mampu mengidentifikasi kata kunci yang menandakan operasi pengurangan dalam soal cerita.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Langkah Memecahkan Soal Cerita",
        "minutes": 6,
        "goal": "Siswa mampu menerapkan tahapan pemecahan masalah soal cerita secara runut dari membaca hingga memeriksa hasil.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Soal Cerita Dua Langkah",
        "minutes": 6,
        "goal": "Siswa mampu memecahkan soal cerita kontekstual yang melibatkan kombinasi penjumlahan dan pengurangan dua langkah.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Soal Cerita Penjumlahan dan Pengurangan",
    "topic": "Penjumlahan dan Pengurangan sampai 100",
    "level": "Kelas 2 SD · Fase A",
    "sections": sections
}

# Verifikasi teks materi
for idx, s in enumerate(sections):
    clean = re.sub(r':::[a-z_]+.*?(?:\n.*?)*?:::', '', s['content'], flags=re.DOTALL)
    sents = [sent.strip() for sent in re.split(r'[.!?\n]+', clean) if sent.strip()]
    slens = [len(sent.split()) for sent in sents]
    avg_s = sum(slens) / len(slens) if slens else 0
    max_s = max(slens) if slens else 0
    word_count = len(s['content'].split())
    assert word_count <= 120, f"Section {idx+1} word count > 120 ({word_count})"
    assert avg_s <= 6.0, f"Section {idx+1} avg sentence len > 6 ({avg_s:.2f})"
    assert max_s <= 10, f"Section {idx+1} max sentence len > 10 ({max_s})"

# ==========================================
# 2. DEFINISI BANK 50 SOAL BAB 43
# ==========================================
D, T, X = "diagnostik", "latihan_terarah", "latihan_mandiri"
K, R, P = "checkpoint_akhir", "remedial", "pengayaan"
F, Kn, Pr, Me = "faktual", "konseptual", "prosedural", "metakognitif"

Q = []

def mc(b, d, f, dim, s, stem, opts, ans, ex, m=None, verifikasi=None):
    Q.append(dict(t="mc", b=b, d=d, f=f, dim=dim, s=s, stem=stem, opts=opts, ans=ans, ex=ex, m=m, verifikasi=verifikasi))

def tf(b, d, f, dim, s, text, ans, ex):
    Q.append(dict(t="tf", b=b, d=d, f=f, dim=dim, s=s, stem=text, ans=ans, ex=ex))

def sa(b, d, f, dim, s, stem, ans, ex, verifikasi=None):
    Q.append(dict(t="sa", b=b, d=d, f=f, dim=dim, s=s, stem=stem, ans=ans, ex=ex, verifikasi=verifikasi))

# ── C1 MUDAH (5 soal: 2 diagnostik, 3 terarah) ─────────────────────────────
# Diagnostik (2)
mc("c1", "mudah", D, F, S1, "Kata 'membeli lagi' dalam soal cerita menandakan operasi ....", ["penjumlahan", "pengurangan", "perkalian", "pembagian"], "A", "Membeli lagi berarti jumlah benda bertambah (penjumlahan).")
tf("c1", "mudah", D, F, S2, "Kata 'sisa' dalam soal cerita biasanya diselesaikan dengan pengurangan.", "Benar", "Mencari sisa diselesaikan dengan operasi pengurangan.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Kata berikut yang menandakan operasi pengurangan adalah ....", ["pecah", "datang lagi", "seluruhnya", "diberi"], "A", "Pecah berarti benda berkurang jumlahnya.")
mc("c1", "mudah", T, F, S3, "Langkah pertama dalam menyelesaikan soal cerita adalah ....", ["membaca soal dengan teliti", "langsung menghitung", "menulis jawaban acak", "menebak operasi"], "A", "Membaca soal dengan teliti adalah langkah pertama pemecahan masalah.")
sa("c1", "mudah", T, F, S1, "Siti punya 12 pensil, dibelikan 5 pensil lagi. Berapa total pensil?", "17", "12 + 5 = 17 pensil.", verifikasi={"ekspresi": "12 + 5", "hasil": "17"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Ani punya 24 pita, Lani punya 15 pita. Kalimat untuk mencari total pita adalah ....", ["24 + 15", "24 - 15", "24 + 24", "15 - 24"], "A", "Total seluruh pita dihitung dengan 24 + 15.", "Salah memilih operasi saat mencari total")
tf("c2", "mudah", D, Kn, S4, "Soal cerita dua langkah selalu diselesaikan dalam satu kali hitungan.", "Salah", "Soal dua langkah diselesaikan bertahap dalam dua operasi hitung.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Pak Tani panen 45 semangka, terjual 20 semangka. Kalimat matematika yang benar adalah ....", ["45 - 20", "45 + 20", "20 + 20", "45 - 45"], "A", "Terjual berarti berkurang: 45 - 20.", "Tertukar antara penjumlahan dan pengurangan pada kata terjual")
mc("c2", "mudah", R, Kn, S3, "Mengapa kita perlu menuliskan kalimat matematika dari soal cerita?", ["agar langkah perhitungannya jelas dan teratur", "agar terlihat panjang", "hanya hiasan buku", "karena disuruh teman"], "A", "Kalimat matematika mengubah cerita menjadi bentuk hitungan yang jelas.", "Mengabaikan penulisan kalimat matematika")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Kata 'digabungkan' pada soal cerita menandakan benda dihitung dengan cara ....", ["dijumlahkan", "dikurangkan", "dihilangkan", "dihitung mundur"], "A", "Menggabungkan dua kumpulan berarti menjumlahkannya.")
mc("c2", "mudah", T, Kn, S4, "Dono punya 30 stiker, diberi 10, lalu hilang 5. Langkah pertamanya adalah ....", ["menjumlahkan 30 + 10", "mengurangkan 30 - 5", "mengurangkan 10 - 5", "menjumlahkan 10 + 5"], "A", "Hitung dahulu stiker awal ditambah pemberian paman.")
tf("c2", "mudah", T, Kn, S2, "Menghitung selisih usia kakak dan adik menggunakan operasi penjumlahan.", "Salah", "Selisih selalu dihitung menggunakan operasi pengurangan.")
sa("c2", "mudah", T, Kn, S2, "Ibu membuat 38 kue, dimakan 15 kue. Berapa sisa kue ibu?", "23", "38 - 15 = 23 kue.", verifikasi={"ekspresi": "38 - 15", "hasil": "23"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Di kolam ada 36 ikan mas dan 27 ikan nila. Berapa banyak ikan seluruhnya?", ["63 ekor", "53 ekor", "64 ekor", "62 ekor"], "A", "36 + 27 = 63 ekor.", "Salah menjumlahkan dengan menyimpan", verifikasi={"ekspresi": "36 + 27", "hasil": "63"})
mc("c3", "sedang", R, Pr, S2, "Paman membawa 72 jeruk, diberikan tetangga 38 jeruk. Berapa sisa jeruk paman?", ["34 jeruk", "44 jeruk", "35 jeruk", "33 jeruk"], "A", "72 - 38 = 34 jeruk.", "Keliru saat meminjam pada soal pengurangan", verifikasi={"ekspresi": "72 - 38", "hasil": "34"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Riko punya 42 kelereng, menang 16 kelereng lagi. Berapa kelereng Riko sekarang?", ["58 kelereng", "48 kelereng", "59 kelereng", "57 kelereng"], "A", "42 + 16 = 58 kelereng.", verifikasi={"ekspresi": "42 + 16", "hasil": "58"})
mc("c3", "mudah", T, Pr, S2, "Di perpustakaan ada 65 buku, dipinjam 23 buku. Berapa sisa buku di rak?", ["42 buku", "32 buku", "43 buku", "41 buku"], "A", "65 - 23 = 42 buku.", verifikasi={"ekspresi": "65 - 23", "hasil": "42"})
tf("c3", "sedang", T, Pr, S3, "Menjawab soal cerita harus menyertakan satuan seperti butir atau buah.", "Benar", "Satuan benda penting agar jawaban jelas dan lengkap.")
mc("c3", "sedang", T, Pr, S4, "Lina punya 40 pita, membeli 25 pita, lalu dipakai 18 pita. Sisa pita Lina?", ["47 pita", "37 pita", "48 pita", "46 pita"], "A", "40 + 25 = 65; 65 - 18 = 47 pita.", verifikasi={"ekspresi": "40 + 25 - 18", "hasil": "47"})
tf("c3", "sedang", T, Pr, S1, "Budi punya 50 permen dan memberi adik 20 permen. Permen Budi bertambah.", "Salah", "Memberi orang lain berarti permen Budi berkurang.")
sa("c3", "sedang", T, Pr, S4, "Ada 55 ayam di kandang. Dijual 20 ekor, menetas 15 ekor. Berapa ayam sekarang?", "50", "55 - 20 = 35; 35 + 15 = 50 ekor.", verifikasi={"ekspresi": "55 - 20 + 15", "hasil": "50"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Toko roti menjual 48 roti abon dan 35 roti cokelat. Berapa roti terjual?", ["83 roti", "73 roti", "84 roti", "82 roti"], "A", "48 + 35 = 83 roti.", verifikasi={"ekspresi": "48 + 35", "hasil": "83"})
mc("c3", "sedang", X, Pr, S2, "Sebuah bus berisi 54 penumpang. Di halte turun 28 penumpang. Berapa sisa penumpang?", ["26 penumpang", "36 penumpang", "25 penumpang", "27 penumpang"], "A", "54 - 28 = 26 penumpang.", verifikasi={"ekspresi": "54 - 28", "hasil": "26"})
tf("c3", "sedang", X, Pr, S3, "Untuk mengetahui selisih 60 dan 25, kita lakukan hitungan 60 - 25.", "Benar", "Selisih dicari dengan mengurangkan bilangan besar dengan bilangan kecil.")
sa("c3", "sedang", X, Pr, S4, "Edo punya 60 balon. Meletus 15 balon, ditiup lagi 10 balon. Berapa balon sekarang?", "55", "60 - 15 = 45; 45 + 10 = 55 balon.", verifikasi={"ekspresi": "60 - 15 + 10", "hasil": "55"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Di keranjang ada 80 apel. Sebanyak 34 apel dibagikan. Berapa sisa apel di keranjang?", ["46 apel", "56 apel", "45 apel", "47 apel"], "A", "80 - 34 = 46 apel.", verifikasi={"ekspresi": "80 - 34", "hasil": "46"})
mc("c3", "sedang", K, Pr, S4, "Pak Dani punya 50 mangga, memetik 35 mangga, dijual 48 mangga. Sisa mangga?", ["37 mangga", "47 mangga", "38 mangga", "36 mangga"], "A", "50 + 35 = 85; 85 - 48 = 37 mangga.", verifikasi={"ekspresi": "50 + 35 - 48", "hasil": "37"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Siti punya 38 perangko dan Lani punya 45 perangko. Kalimat untuk mencari selisihnya adalah ....", ["45 - 38", "45 + 38", "38 - 45", "45 + 45"], "A", "Selisih dihitung dengan mengurangkan bilangan besar dengan kecil: 45 - 38.")
mc("c4", "sedang", T, Kn, S2, "Sebuah bioskop punya 90 kursi. Terisi 58 kursi. Berapa kursi yang masih kosong?", ["32 kursi", "42 kursi", "33 kursi", "31 kursi"], "A", "90 - 58 = 32 kursi.", verifikasi={"ekspresi": "90 - 58", "hasil": "32"})
tf("c4", "sedang", T, Kn, S3, "Jika kalimat matematikanya 40 + N = 75, maka cerita yang cocok adalah benda berkurang.", "Salah", "40 + N = 75 menunjukkan penambahan benda hingga menjadi 75.")
tf("c4", "sedang", T, Kn, S4, "Membeli lagi lalu memberikan ke teman berarti urutannya tambah lalu kurang.", "Benar", "Membeli lagi (+) kemudian memberikan (-).")
sa("c4", "sedang", T, Kn, S4, "Di rak ada 70 buku. Dipinjam 25 buku, dikembalikan 18 buku. Berapa buku di rak?", "63", "70 - 25 = 45; 45 + 18 = 63 buku.", verifikasi={"ekspresi": "70 - 25 + 18", "hasil": "63"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Budi punya 28 kelereng. Dono punya 15 butir lebih banyak. Berapa kelereng Dono?", ["43 butir", "33 butir", "44 butir", "42 butir"], "A", "28 + 15 = 43 butir.", verifikasi={"ekspresi": "28 + 15", "hasil": "43"})
mc("c4", "sedang", X, Kn, S4, "Ada 85 bibit pohon. Ditanam 46 dan 24 bibit. Berapa sisa bibit pohon?", ["15 bibit", "25 bibit", "14 bibit", "16 bibit"], "A", "46 + 24 = 70; 85 - 70 = 15 bibit.", verifikasi={"ekspresi": "85 - (46 + 24)", "hasil": "15"})
tf("c4", "sedang", X, Kn, S2, "Pernyataan 'Ali lebih tinggi 8 cm dari Bayu' diselesaikan dengan mencari selisih tinggi.", "Benar", "Perbedaan tinggi adalah selisih antara tinggi Ali dan Bayu.")
mc("c4", "sulit", X, Me, S4, "Ibu punya 95 ribu rupiah. Dibelanjakan 48 ribu dan 27 ribu. Berapa sisa uang ibu?", ["20 ribu rupiah", "30 ribu rupiah", "15 ribu rupiah", "25 ribu rupiah"], "A", "48 + 27 = 75 ribu; 95 - 75 = 20 ribu rupiah.", verifikasi={"ekspresi": "95 - (48 + 27)", "hasil": "20"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Di kelas ada 18 siswa laki-laki dan 19 siswa perempuan. Berapa total seluruh siswa?", ["37 siswa", "27 siswa", "38 siswa", "36 siswa"], "A", "18 + 19 = 37 siswa.", verifikasi={"ekspresi": "18 + 19", "hasil": "37"})
mc("c4", "sulit", K, Me, S2, "Kandang A ada 74 ayam, kandang B ada 38 ayam. Berapa selisih ayam kedua kandang?", ["36 ekor", "46 ekor", "35 ekor", "37 ekor"], "A", "74 - 38 = 36 ekor.", verifikasi={"ekspresi": "74 - 38", "hasil": "36"})
tf("c4", "sulit", K, Me, S4, "Mula-mula 80 buah, diambil 45 lalu ditambah 20 buah, hasilnya lebih dari 60.", "Salah", "80 - 45 = 35; 35 + 20 = 55. 55 kurang dari 60.")
mc("c4", "sulit", K, Me, S4, "Ada 92 buku cerita. Dipinjam 35 buku lalu dipinjam lagi 28 buku. Berapa sisa buku?", ["29 buku", "39 buku", "28 buku", "30 buku"], "A", "35 + 28 = 63; 92 - 63 = 29 buku.", verifikasi={"ekspresi": "92 - (35 + 28)", "hasil": "29"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Soal cerita berikut yang penyelesaiannya menggunakan kalimat matematika 35 + 47 adalah ....", ["Lina punya 35 buku dan dibelikan 47 buku lagi", "Lina punya 47 buku lalu hilang 35 buku", "Lina punya 47 buku dibagikan 35 buku", "Lina mencari selisih 47 dan 35"], "A", "Membeli lagi berarti dijumlahkan: 35 + 47.")
mc("c5", "sedang", T, Me, S2, "Soal cerita berikut yang penyelesaiannya menggunakan kalimat matematika 80 - 36 adalah ....", ["Paman punya 80 mangga lalu terjual 36 mangga", "Paman punya 80 mangga memetik lagi 36 mangga", "Paman mengumpulkan 80 dan 36 mangga", "Paman diberi 80 dan 36 mangga"], "A", "Terjual berarti dikurangkan: 80 - 36.")
mc("c5", "sedang", T, Me, S3, "Rani ingin mengecek apakah 84 - 37 = 47 benar melalui cerita. Cara mengeceknya?", ["jumlahkan 47 mangga sisa dengan 37 mangga yang dibagikan harus 84", "kurangkan lagi 47 dengan 37", "hitung mundur 37 kali", "buat cerita baru"], "A", "Jumlahkan sisa dengan pengurang: 47 + 37 = 84.")
mc("c5", "sulit", T, Me, S4, "Bus berisi 45 orang. Naik 18 orang, lalu turun 24 orang. Berapa orang di bus sekarang?", ["39 orang", "49 orang", "38 orang", "40 orang"], "A", "45 + 18 = 63; 63 - 24 = 39 orang.", verifikasi={"ekspresi": "45 + 18 - 24", "hasil": "39"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Doni menghitung 73 - 28 = 55. Temannya berkata salah. Bukti kesalahan Doni adalah ....", ["55 + 28 = 83 bukan 73", "55 - 28 = 27", "73 + 28 = 101", "73 - 55 = 28"], "A", "Jika diperiksa 55 + 28 = 83, bukan 73. Maka jawaban Doni salah.")
mc("c5", "sulit", K, Me, S4, "Ada 100 masker. Dibagikan 38 masker dan 45 masker. Berapa sisa masker sekarang?", ["17 masker", "27 masker", "16 masker", "18 masker"], "A", "38 + 45 = 83; 100 - 83 = 17 masker.", verifikasi={"ekspresi": "100 - (38 + 45)", "hasil": "17"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S3, "Sebuah soal cerita memiliki kata 'membeli' dan 'hilang'. Bagaimana rencana penyelesaian terbaik?", ["tambahkan pembelian ke jumlah awal lalu kurangkan barang yang hilang", "jumlahkan semua angka yang ada", "kurangkan semua angka yang ada", "abaikan kata hilang"], "A", "Operasi bertahap: awal + beli - hilang.")
mc("c6", "sulit", K, Me, S4, "Susunlah kalimat matematika dari cerita: 'Ada 65 apel, busuk 18, datang kiriman baru 25'!", ["65 - 18 + 25", "65 + 18 + 25", "65 - 18 - 25", "65 + 18 - 25"], "A", "Busuk berarti (-), kiriman baru berarti (+): 65 - 18 + 25.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Ada 88 pengunjung. Keluar 29, masuk 34, lalu keluar 18 orang. Berapa pengunjung sekarang?", ["75 orang", "65 orang", "76 orang", "74 orang"], "A", "88 - 29 = 59; 59 + 34 = 93; 93 - 18 = 75 orang.", verifikasi={"ekspresi": "88 - 29 + 34 - 18", "hasil": "75"})
mc("c6", "sulit", P, Me, S4, "Panen 94 jagung. Terjual 38 dan 29 buah, dibagikan 12 buah. Berapa sisa jagung sekarang?", ["15 jagung", "25 jagung", "14 jagung", "16 jagung"], "A", "38 + 29 + 12 = 79; 94 - 79 = 15 jagung.", verifikasi={"ekspresi": "94 - (38 + 29 + 12)", "hasil": "15"})

# ==========================================
# 3. PROSES & SHUFFLE PILIHAN GANDA (DISTRIBUSI KUNCI SEIMBANG)
# ==========================================
LETTERS = ["A", "B", "C", "D"]
mc_list = []
tf_list = []
sa_list = []

# Target sebaran kunci MC (35 soal): 9 A, 9 B, 9 C, 8 D
mc_targets = ["A"] * 9 + ["B"] * 9 + ["C"] * 9 + ["D"] * 8
random.shuffle(mc_targets)
target_idx = 0

for idx, q in enumerate(Q):
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab43_soal_{idx+1}"))
    tax = {
        "bloom": q["b"],
        "difficulty": q["d"],
        "fungsi": q["f"],
        "knowledge_dimension": q["dim"]
    }
    if q.get("m"):
        tax["miskonsepsi_target"] = q["m"]
        
    base = {
        "uid": uid,
        "source_section_id": q["s"],
        "taxonomy": tax,
        "explanation": q["ex"]
    }
    if q.get("verifikasi"):
        base["verifikasi"] = q["verifikasi"]

    if q["t"] == "mc":
        base["stem"] = q["stem"]
        correct_text = q["opts"][0]
        distractors = q["opts"][1:]
        random.shuffle(distractors)
        
        target_letter = mc_targets[target_idx]
        target_idx += 1
        pos = LETTERS.index(target_letter)
        
        final_opts = list(distractors)
        final_opts.insert(pos, correct_text)
        
        base["choices"] = [{"label": LETTERS[i], "text": final_opts[i]} for i in range(4)]
        base["answer"] = target_letter
        mc_list.append(base)
    elif q["t"] == "tf":
        base["text"] = q["stem"]
        base["answer"] = q["ans"]
        tf_list.append(base)
    elif q["t"] == "sa":
        base["stem"] = q["stem"]
        base["answer"] = q["ans"]
        sa_list.append(base)

# Assert TF balance
tf_answers = Counter(q["answer"] for q in tf_list)
assert tf_answers["Benar"] == 5 and tf_answers["Salah"] == 5, f"TF balance error: {tf_answers}"

question_groups = [
    {
        "type": "multiple_choice",
        "group_id": "mc",
        "instruction": "Pilih jawaban yang paling tepat.",
        "questions": mc_list,
        "ai_meta": {"draft": True}
    },
    {
        "type": "true_false",
        "group_id": "tf",
        "instruction": "Tentukan benar atau salah.",
        "options": ["Benar", "Salah"],
        "questions": tf_list,
        "ai_meta": {"draft": True}
    },
    {
        "type": "short_answer",
        "group_id": "sa",
        "instruction": "Jawab singkat dengan satu angka atau satu kata.",
        "questions": sa_list,
        "ai_meta": {"draft": True}
    }
]

quiz_config = {
    "level": "Fase A - Kelas 2 SD",
    "sections": [{"title": s["title"], "section_id": s["id"]} for s in sections],
    "passing_score": 70.0,
    "shuffle_choices": True,
    "shuffle_question_order": True,
    "question_groups": question_groups
}

# Verifikasi kuota dan aturan taksonomi
all_q = mc_list + tf_list + sa_list
diff = Counter(q["taxonomy"]["difficulty"] for q in all_q)
bloom = Counter(q["taxonomy"]["bloom"] for q in all_q)
fungsi = Counter(q["taxonomy"]["fungsi"] for q in all_q)
dimensi = Counter(q["taxonomy"]["knowledge_dimension"] for q in all_q)

print("Bloom:", dict(bloom))
print("Difficulty:", dict(diff))
print("Fungsi:", dict(fungsi))
print("Dimensi:", dict(dimensi))
print("Tipe:", {"mc": len(mc_list), "tf": len(tf_list), "sa": len(sa_list)})

sec_latihan = Counter(q["source_section_id"] for q in all_q if q["taxonomy"]["fungsi"] in ("latihan_terarah", "checkpoint_bagian"))
print("Latihan per section (min 4):", dict(sec_latihan))
for s in sections:
    assert sec_latihan[s["id"]] >= 4, f"Section {s['id']} kurang latihan ({sec_latihan[s['id']]})"

output_data = {
    "lesson_plan": lesson_plan,
    "quiz_config": quiz_config
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab43.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
