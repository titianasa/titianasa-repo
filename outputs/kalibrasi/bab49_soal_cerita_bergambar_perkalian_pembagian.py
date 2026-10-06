#!/usr/bin/env python3
"""
Generator dan validator Bab 49 Matematika Kelas 2 SD:
"Soal Cerita Bergambar: Perkalian dan Pembagian" (Fase A)
bab_id: 5eac71e9-158e-4e06-a32e-00a83f5f2828
article_id: e4f5a6b7-8c9d-4e0f-1a2b-3c4d5e6f7a8b
quiz_id: 9c0d1e2f-3a4b-5c6d-7e8f-9a0b1c2d3e4f
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a1b2c3d4e501"  # Mengenal Cerita Perkalian vs Pembagian
S2 = "b2c3d4e5f602"  # Cerita Bergambar Perkalian
S3 = "c3d4e5f6a703"  # Cerita Bergambar Pembagian
S4 = "d4e5f6a7b804"  # Masalah Gabungan Bertingkat

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Cerita matematika sangat dekat dengan kita.
Kuncinya ada pada kata cerita.
Kata 'tiap kelompok berisi' menandakan perkalian.
Perkalian menggabungkan bagian-bagian kecil.
Kata 'dibagi rata' menandakan pembagian.
Pembagian memecah kumpulan besar.
Kenali ceritanya dengan teliti!

:::definition
title: Soal Cerita Operasi Hitung
Soal cerita adalah masalah sehari-hari yang diselesaikan dengan kalimat matematika.
:::"""

s2_content = """Lihatlah gambar kelompok benda berikut.
Ada tiga piring buah segar.
Tiap piring berisi empat apel.
Kita ingin mencari total semua apel.
Tiga kelompok apel dikalikan empat.
Tiga kali empat sama dengan dua belas.
Total ada dua belas apel.
Gambar membantu kita berhitung cepat!

:::steps
title: Menyelesaikan Cerita Perkalian
1. Hitung banyaknya wadah atau kelompok.
2. Hitung banyak benda tiap wadah.
3. Kalikan banyak kelompok dengan isi.
:::"""

s3_content = """Sekarang kita membagikan benda.
Ibu membawa sepuluh donat cokelat.
Donat dibagikan kepada dua anak.
Tiap anak mendapat bagian sama banyak.
Sepuluh dibagi dua adalah lima.
Masing-masing anak mendapat lima donat.
Gambar memudahkan kita melihat pembagian!"""

s4_content = """Kadang cerita menggabungkan keduanya.
Kalian bisa mengalikan lalu membagi.
Atau membagi lalu mengalikan.
Kerjakan satu per satu secara runut.
Jangan terburu-buru saat menghitung.
Pasti kamu bisa menyelesaikannya!

:::common_trap
title: Tertukar Operasi Hitung
Jangan menggunakan pembagian saat mencari total!
Jika mencari total kumpulan, gunakan perkalian.
Jika memecah kumpulan, gunakan pembagian.
:::

:::callout
variant: summary
title: Ringkasan
text: Perkalian menggabungkan kelompok sama banyak, sedangkan pembagian membagikan total benda sama rata.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Cerita Perkalian vs Pembagian",
        "minutes": 6,
        "goal": "Siswa mampu mengidentifikasi operasi yang tepat (perkalian atau pembagian) berdasarkan kata kunci dalam cerita.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Cerita Bergambar Perkalian",
        "minutes": 6,
        "goal": "Siswa mampu menuliskan kalimat perkalian dan menghitung total benda dari stimulus cerita bergambar.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Cerita Bergambar Pembagian",
        "minutes": 6,
        "goal": "Siswa mampu menuliskan kalimat pembagian dan menentukan hasil bagi dari stimulus cerita bergambar.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Masalah Gabungan Bertingkat",
        "minutes": 6,
        "goal": "Siswa mampu menyelesaikan soal cerita dua langkah yang melibatkan perkalian dan pembagian sederhana.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Soal Cerita Bergambar: Perkalian dan Pembagian",
    "topic": "Mengenal Perkalian dan Pembagian",
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
# 2. DEFINISI BANK 50 SOAL BAB 49
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
mc("c1", "mudah", D, F, S1, "Kata 'dibagikan sama banyak kepada teman' menunjukkan operasi ....", ["pembagian", "perkalian", "penjumlahan", "pengurangan satu"], "A", "Dibagikan sama banyak adalah ciri operasi pembagian.")
tf("c1", "mudah", D, F, S2, "Ada 3 piring berisi 2 jeruk, total jeruk dihitung dengan 3 x 2.", "Benar", "3 piring masing-masing 2 jeruk: 3 x 2 = 6 jeruk.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Ada 4 sarang burung. Tiap sarang ada 2 anak burung. Total anak burung?", ["8 ekor", "6 ekor", "10 ekor", "4 ekor"], "A", "4 x 2 = 8 ekor.", verifikasi={"ekspresi": "4 * 2", "hasil": "8"})
mc("c1", "mudah", T, F, S3, "Ada 10 permen dibagikan ke 2 anak sama banyak. Berapa permen tiap anak?", ["5 butir", "4 butir", "6 butir", "2 butir"], "A", "10 : 2 = 5 butir.", verifikasi={"ekspresi": "10 / 2", "hasil": "5"})
sa("c1", "mudah", T, F, S1, "Berapakah hasil dari 2 x 4?", "8", "2 x 4 = 8.", verifikasi={"ekspresi": "2 * 4", "hasil": "8"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Ibu memotong kue jadi 12 potong, dibagikan ke 4 anak. Berapa potong tiap anak?", ["3 potong", "4 potong", "2 potong", "5 potong"], "A", "12 : 4 = 3 potong.", verifikasi={"ekspresi": "12 / 4", "hasil": "3"})
tf("c2", "mudah", D, Kn, S1, "Mencari total seluruh benda dari beberapa kelompok menggunakan operasi pembagian.", "Salah", "Mencari total seluruh benda dari kelompok yang sama menggunakan perkalian.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Ada 5 kotak pensil. Tiap kotak isi 4 pensil. Berapa seluruh pensil?", ["20 batang", "15 batang", "25 batang", "9 batang"], "A", "5 x 4 = 20 batang pensil.", "Menjumlahkan 5 + 4 bukan mengalikan", verifikasi={"ekspresi": "5 * 4", "hasil": "20"})
mc("c2", "mudah", R, Kn, S3, "Ada 15 mangga dibagi ke 3 keranjang sama rata. Berapa isi keranjang?", ["5 mangga", "3 mangga", "6 mangga", "4 mangga"], "A", "15 : 3 = 5 mangga.", "Tertukar pembagi dengan isi", verifikasi={"ekspresi": "15 / 3", "hasil": "5"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Budi punya 4 kandang ayam. Tiap kandang isi 5 ayam. Operasi yang tepat?", ["4 x 5", "4 : 5", "5 - 4", "4 + 5"], "A", "Ada 4 kelompok masing-masing 5 ayam, jadi dikalikan: 4 x 5.")
mc("c2", "mudah", T, Kn, S2, "Toko punya 3 rak buku. Tiap rak ada 6 buku dongeng. Berapa total buku?", ["18 buku", "15 buku", "21 buku", "12 buku"], "A", "3 x 6 = 18 buku.", verifikasi={"ekspresi": "3 * 6", "hasil": "18"})
tf("c2", "mudah", T, Kn, S3, "Ada 16 kelereng dibagi rata ke 4 anak. Tiap anak mendapat 8 kelereng.", "Salah", "16 : 4 = 4 kelereng, bukan 8 kelereng.")
sa("c2", "mudah", T, Kn, S4, "Berapakah hasil dari 14 : 2?", "7", "14 : 2 = 7.", verifikasi={"ekspresi": "14 / 2", "hasil": "7"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Ada 6 baris tanaman bunga. Tiap baris ada 4 bunga mawar. Berapa mawar?", ["24 tangkai", "20 tangkai", "28 tangkai", "18 tangkai"], "A", "6 x 4 = 24 tangkai mawar.", "Salah tabel perkalian 4", verifikasi={"ekspresi": "6 * 4", "hasil": "24"})
mc("c3", "sedang", R, Pr, S3, "Ada 18 bola dimasukkan ke 3 keranjang sama banyak. Berapa bola per keranjang?", ["6 bola", "5 bola", "7 bola", "8 bola"], "A", "18 : 3 = 6 bola.", "Keliru pembagian 18 dengan 3", verifikasi={"ekspresi": "18 / 3", "hasil": "6"})

# Terarah (6): S1, S2, S3, S4, S2, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S2, "Ada 4 kantong jeruk. Tiap kantong ada 5 jeruk. Berapa total jeruk?", ["20 jeruk", "18 jeruk", "24 jeruk", "15 jeruk"], "A", "4 x 5 = 20 jeruk.", verifikasi={"ekspresi": "4 * 5", "hasil": "20"})
mc("c3", "mudah", T, Pr, S3, "Ada 20 kue dibagikan kepada 5 anak sama rata. Berapa kue per anak?", ["4 kue", "3 kue", "5 kue", "6 kue"], "A", "20 : 5 = 4 kue.", verifikasi={"ekspresi": "20 / 5", "hasil": "4"})
tf("c3", "sedang", T, Pr, S1, "Cerita 'Doni membagikan 12 kelereng ke 3 toples' diselesaikan dengan perkalian.", "Salah", "Membagikan sejumlah kelereng ke wadah diselesaikan dengan pembagian.")
mc("c3", "sedang", T, Pr, S4, "Budi punya 2 kotak bola tenis isi 6. Lalu 4 bola hilang. Sisa bola?", ["8 bola", "7 bola", "9 bola", "6 bola"], "A", "2 x 6 = 12 bola; 12 - 4 = 8 bola.", verifikasi={"ekspresi": "(2 * 6) - 4", "hasil": "8"})
tf("c3", "sedang", T, Pr, S2, "Ada 5 baris meja, tiap baris 4 meja. Total meja adalah 20 buah.", "Benar", "5 x 4 = 20 meja.")
sa("c3", "sedang", T, Pr, S3, "Berapakah hasil dari 24 : 3?", "8", "24 : 3 = 8.", verifikasi={"ekspresi": "24 / 3", "hasil": "8"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Lina membeli 3 bungkus permen. Tiap bungkus isi 8 permen. Kalimat matematikanya?", ["3 x 8 = 24", "8 : 3 = 2", "3 + 8 = 11", "8 - 3 = 5"], "A", "3 kelompok masing-masing 8: 3 x 8 = 24.")
mc("c3", "sedang", X, Pr, S2, "Ada 7 vas bunga. Tiap vas ada 3 mawar putih. Berapa seluruh mawar?", ["21 mawar", "18 mawar", "24 mawar", "27 mawar"], "A", "7 x 3 = 21 mawar.", verifikasi={"ekspresi": "7 * 3", "hasil": "21"})
tf("c3", "sedang", X, Pr, S4, "Dua kelompok 6 kue sama banyak dengan tiga kelompok 4 kue.", "Benar", "2 x 6 = 12 dan 3 x 4 = 12, hasilnya sama banyak.")
sa("c3", "sedang", X, Pr, S3, "Berapakah hasil dari 28 : 7?", "4", "28 : 7 = 4.", verifikasi={"ekspresi": "28 / 7", "hasil": "4"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Pak Tani punya 5 kandang kelinci. Tiap kandang 4 kelinci. Berapa kelinci seluruhnya?", ["20 ekor", "18 ekor", "22 ekor", "16 ekor"], "A", "5 x 4 = 20 ekor kelinci.", verifikasi={"ekspresi": "5 * 4", "hasil": "20"})
mc("c3", "sedang", K, Pr, S3, "Ada 27 kelereng dibagi kepada 3 anak sama banyak. Berapa kelereng tiap anak?", ["9 butir", "8 butir", "7 butir", "6 butir"], "A", "27 : 3 = 9 butir.", verifikasi={"ekspresi": "27 / 3", "hasil": "9"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S1
mc("c4", "sedang", T, Kn, S1, "Mengapa kita mengalikan 4 dengan 5 untuk menghitung total 4 piring berisi 5 kue?", ["karena perkalian adalah penjumlahan berulang angka 5 sebanyak 4 kali", "karena 4 ditambah 5 hasilnya 9", "karena pembagian terlalu lambat", "karena angka 5 lebih besar"], "A", "Perkalian adalah representasi efisien dari penjumlahan berulang.")
mc("c4", "sedang", T, Kn, S2, "Di meja ada 6 piring kue. Tiap piring ada 5 kue donat. Berapa donat?", ["30 donat", "25 donat", "35 donat", "20 donat"], "A", "6 x 5 = 30 donat.", verifikasi={"ekspresi": "6 * 5", "hasil": "30"})
tf("c4", "sedang", T, Kn, S3, "Membagi 24 kue ke 4 piring menghasilkan isi yang lebih banyak daripada ke 6 piring.", "Benar", "24 : 4 = 6 kue, sedangkan 24 : 6 = 4 kue. 6 lebih banyak dari 4.")
tf("c4", "sedang", T, Kn, S4, "Hasil dari (2 x 10) bernilai sama besar dengan hasil (5 x 5).", "Salah", "2 x 10 = 20, sedangkan 5 x 5 = 25. Keduanya tidak sama besar.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari (4 x 6) - (15 : 3)?", "19", "4 x 6 = 24; 15 : 3 = 5; 24 - 5 = 19.", verifikasi={"ekspresi": "(4 * 6) - (15 / 3)", "hasil": "19"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S2, "Lina membawa 4 kotak susu. Tiap kotak isi 6 botol. Total botol susu?", ["24 botol", "20 botol", "28 botol", "22 botol"], "A", "4 x 6 = 24 botol susu.", verifikasi={"ekspresi": "4 * 6", "hasil": "24"})
mc("c4", "sedang", X, Kn, S3, "Sebanyak 32 buku dibagi rata kepada 4 meja belajar. Berapa buku per meja?", ["8 buku", "7 buku", "9 buku", "6 buku"], "A", "32 : 4 = 8 buku.", verifikasi={"ekspresi": "32 / 4", "hasil": "8"})
tf("c4", "sedang", X, Kn, S1, "Soal cerita bergambar tentang pembagian selalu melibatkan gambar benda yang bertambah banyak.", "Salah", "Pembagian memecah benda menjadi bagian-bagian lebih kecil, bukan bertambah.")
mc("c4", "sulit", X, Me, S4, "Manakah cerita yang menghasilkan jumlah benda PALING BANYAK?", ["5 kotak pensil masing-masing 6 pensil", "4 kantong buah masing-masing 7 buah", "3 ikat bunga masing-masing 9 bunga", "7 bungkus permen masing-masing 4 permen"], "A", "5 x 6 = 30 pensil; 4 x 7 = 28 buah; 3 x 9 = 27 bunga; 7 x 4 = 28 permen. Paling banyak 30.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Budi punya 3 kantong isi 6. Siti membagi 18 permen ke 3 piring. Siapakah lebih banyak?", ["Budi dan Siti sama-sama 6", "Budi lebih banyak", "Siti lebih banyak", "tidak dapat dihitung"], "A", "Budi: 6 permen/kantong. Siti: 18 : 3 = 6 permen/piring. Keduanya bernilai sama.")
mc("c4", "sulit", K, Me, S2, "Ada 5 rak sepatu, tiap rak muat 4 pasang. Berapa pasang sepatu yang muat?", ["20 pasang", "18 pasang", "22 pasang", "16 pasang"], "A", "5 x 4 = 20 pasang sepatu.", verifikasi={"ekspresi": "5 * 4", "hasil": "20"})
tf("c4", "sulit", K, Me, S4, "Tiga kotak donat isi 4 donat bernilai sama dengan dua kotak donat isi 6 donat.", "Benar", "3 x 4 = 12 dan 2 x 6 = 12.")
mc("c4", "sulit", K, Me, S4, "Budi punya 4 kotak isi 5 apel. Dimakan bersama teman 8 apel. Sisa apel?", ["12 apel", "10 apel", "14 apel", "8 apel"], "A", "4 x 5 = 20 apel; 20 - 8 = 12 apel tersisa.", verifikasi={"ekspresi": "(4 * 5) - 8", "hasil": "12"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Lina punya 24 permen. Ia ingin membagikan ke 4 temannya. Berapa permen tiap teman?", ["6 permen", "5 permen", "7 permen", "8 permen"], "A", "24 : 4 = 6 permen tiap teman.", verifikasi={"ekspresi": "24 / 4", "hasil": "6"})
mc("c5", "sedang", T, Me, S2, "Berapakah nilai A pada kalimat: 4 x A = 32 apel?", ["8", "7", "9", "6"], "A", "4 x 8 = 32, jadi A = 8 apel.", verifikasi={"ekspresi": "32 / 4", "hasil": "8"})
mc("c5", "sedang", T, Me, S3, "Berapakah nilai B pada kalimat: B : 5 = 6 kue?", ["30", "25", "35", "20"], "A", "30 : 5 = 6, jadi B = 30 kue.", verifikasi={"ekspresi": "5 * 6", "hasil": "30"})
mc("c5", "sulit", T, Me, S4, "Ibu beli 3 kantong jeruk isi 8. Dibagikan ke 4 anak sama rata. Tiap anak?", ["6 jeruk", "5 jeruk", "7 jeruk", "4 jeruk"], "A", "3 x 8 = 24 jeruk; 24 : 4 = 6 jeruk.", verifikasi={"ekspresi": "(3 * 8) / 4", "hasil": "6"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Manakah dari kalimat matematika berikut yang nilainya PALING TEPAT untuk 35 jeruk?", ["7 x 5 = 35", "6 x 6 = 35", "8 x 4 = 35", "9 x 3 = 35"], "A", "7 x 5 = 35.")
mc("c5", "sulit", K, Me, S4, "Pak Guru punya 30 pensil. Dimasukkan ke 5 kotak sama banyak. Tiap kotak isi pensil?", ["6 batang", "5 batang", "7 batang", "4 batang"], "A", "30 : 5 = 6 batang pensil.", verifikasi={"ekspresi": "30 / 5", "hasil": "6"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Budi punya 4 kandang isi 5 ayam. Siti punya 2 kandang isi 10. Siapa lebih banyak?", ["ayam Budi dan Siti sama banyak", "Budi punya lebih banyak", "Siti punya lebih banyak", "tidak dapat dibandingkan"], "A", "Budi: 4 x 5 = 20 ayam. Siti: 2 x 10 = 20 ayam. Keduanya sama banyak.")
mc("c6", "sulit", K, Me, S4, "Ada 2 kotak donat isi 8 donat. Ditambah 1 kotak isi 4 donat. Total donat?", ["20 donat", "18 donat", "22 donat", "24 donat"], "A", "(2 x 8) + 4 = 16 + 4 = 20 donat.", verifikasi={"ekspresi": "(2 * 8) + 4", "hasil": "20"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi gabungan: (6 x 5) - (20 : 4) + (2 x 7)!", ["39", "37", "41", "35"], "A", "6 x 5 = 30; 20 : 4 = 5; 2 x 7 = 14; 30 - 5 + 14 = 39.", verifikasi={"ekspresi": "(6 * 5) - (20 / 4) + (2 * 7)", "hasil": "39"})
mc("c6", "sulit", P, Me, S4, "Ada 4 rak piring isi 6. Sebanyak 2 pecah. Sisanya dibagi 2 orang. Tiap orang?", ["11 piring", "10 piring", "12 piring", "9 piring"], "A", "4 x 6 = 24; 24 - 2 = 22; 22 : 2 = 11 piring.", verifikasi={"ekspresi": "( (4 * 6) - 2 ) / 2", "hasil": "11"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab49_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab49.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
