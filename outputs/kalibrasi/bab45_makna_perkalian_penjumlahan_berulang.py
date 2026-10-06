#!/usr/bin/env python3
"""
Generator dan validator Bab 45 Matematika Kelas 2 SD:
"Makna Perkalian sebagai Penjumlahan Berulang" (Fase A)
bab_id: 04d2ac28-0afa-4fde-b5fe-8beb6cf4576f
article_id: 7b3d6c98-963b-4fd6-9840-0f4317a146a8
quiz_id: 8246afcd-374d-437c-917e-183bb8e04c4e
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "c4d5e6f7a801"  # Kelompok Sama Banyak
S2 = "d5e6f7a8b902"  # Bentuk Penjumlahan Berulang
S3 = "e6f7a8b9c003"  # Menulis Kalimat Perkalian
S4 = "f7a8b9c0d104"  # Menghitung Hasil Perkalian Dasar

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Perkalian berawal dari kelompok benda.
Tiap kelompok harus sama banyak.
Ada tiga piring buah apel.
Tiap piring berisi empat apel.
Semua kelompok memiliki isi sama.
Jika tidak sama, bukan perkalian.
Kelompok sama banyak kunci perkalian.

:::definition
title: Kelompok Sama Banyak
Kelompok sama banyak adalah kumpulan benda dengan jumlah isi yang sama.
:::"""

s2_content = """Mari kita hitung seluruh apel.
Gunakan cara penjumlahan berulang.
Jumlahkan isi dari setiap piring.
Empat tambah empat tambah empat.
Empat ditambah sebanyak tiga kali.
Empat tambah empat jadi delapan.
Delapan tambah empat jadi dua belas.
Jumlah seluruh apel dua belas.

:::steps
title: Menulis Penjumlahan Berulang
1. Hitung isi tiap kelompok.
2. Tulis angka isi berulang-ulang.
3. Jumlahkan angka tersebut berurutan.
:::"""

s3_content = """Penjumlahan berulang ditulis lebih singkat.
Kita menggunakan tanda silang perkalian.
Tiga piring berisi empat apel.
Kita tulis tiga kali empat.
Angka depan adalah banyak kelompok.
Angka belakang adalah isi kelompok.
Tiga kali empat adalah dua belas.
Sangat singkat dan mudah dibaca!"""

s4_content = """Bagaimana menghitung hasil kali?
Hitunglah melalui penjumlahan berulang tadi.
Dua kali lima artinya lima tambah lima.
Hasil dua kali lima adalah sepuluh.
Empat kali tiga artinya tiga dijumlahkan empat kali.
Hasil empat kali tiga adalah dua belas.
Latihan terus membuatmu semakin mahir!

:::common_trap
title: Tertukar Makna Kali
Tiga kali empat artinya empat tambah empat tambah empat.
Bukan tiga tambah tiga tambah tiga tambah tiga!
Angka belakang yang dijumlahkan berulang.
:::

:::callout
variant: summary
title: Ringkasan
text: Perkalian adalah penjumlahan berulang dari kelompok benda yang sama banyak.
:::"""

sections = [
    {
        "id": S1,
        "title": "Kelompok Sama Banyak",
        "minutes": 6,
        "goal": "Siswa memahami konsep kelompok benda dengan jumlah isi yang sama sebagai dasar perkalian.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Bentuk Penjumlahan Berulang",
        "minutes": 6,
        "goal": "Siswa mampu menuliskan dan menghitung penjumlahan berulang dari beberapa kelompok sama banyak.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Menulis Kalimat Perkalian",
        "minutes": 6,
        "goal": "Siswa mampu merepresentasikan penjumlahan berulang ke dalam bentuk notasi perkalian (banyak kelompok x isi kelompok).",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menghitung Hasil Perkalian Dasar",
        "minutes": 6,
        "goal": "Siswa mampu menentukan hasil perkalian bilangan sederhana menggunakan strategi penjumlahan berulang.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Makna Perkalian sebagai Penjumlahan Berulang",
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
# 2. DEFINISI BANK 50 SOAL BAB 45
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
mc("c1", "mudah", D, F, S1, "Perkalian dapat diartikan sebagai bentuk penjumlahan ....", ["berulang", "satu kali", "pengurangan", "pembagian"], "A", "Perkalian adalah penjumlahan berulang kelompok sama banyak.")
tf("c1", "mudah", D, F, S3, "Pada bentuk 4 x 3, angka 4 menyatakan banyak kelompok.", "Benar", "Angka depan menyatakan banyak kelompok.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Bentuk penjumlahan berulang dari 3 x 2 adalah ....", ["2 + 2 + 2", "3 + 3", "3 + 2", "2 + 3"], "A", "3 x 2 berarti 2 dijumlahkan sebanyak 3 kali: 2 + 2 + 2.")
mc("c1", "mudah", T, F, S3, "Bentuk perkalian dari 5 + 5 + 5 + 5 adalah ....", ["4 x 5", "5 x 4", "4 + 5", "5 x 5"], "A", "Ada 4 kali angka 5, jadi ditulis 4 x 5.")
sa("c1", "mudah", T, F, S4, "Berapakah hasil dari 2 x 3?", "6", "2 x 3 = 3 + 3 = 6.", verifikasi={"ekspresi": "2 * 3", "hasil": "6"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Kumpulan benda dapat dihitung dengan perkalian jika setiap kelompok bernilai ....", ["sama banyak", "berbeda-beda", "selalu ganjil", "selalu genap"], "A", "Perkalian mewajibkan tiap kelompok memiliki isi sama banyak.", "Mengira perkalian berlaku untuk kelompok acak")
tf("c2", "mudah", D, Kn, S2, "Penjumlahan 3 + 3 + 4 dapat diubah menjadi perkalian.", "Salah", "Isinya berbeda (ada 4), jadi bukan penjumlahan berulang.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S3, "Arti yang tepat dari perkalian 5 x 2 adalah ....", ["2 + 2 + 2 + 2 + 2", "5 + 5", "5 + 2", "2 x 2"], "A", "5 kelompok masing-masing berisi 2, jadi 2 + 2 + 2 + 2 + 2.", "Tertukar antara banyak kelompok dan isi kelompok")
mc("c2", "mudah", R, Kn, S4, "Berapakah hasil dari 3 x 4?", ["12", "7", "10", "14"], "A", "3 x 4 = 4 + 4 + 4 = 12.", "Menjumlahkan 3 + 4 bukan mengalikan", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Ada 4 kantong, tiap kantong ada 3 kelereng. Banyak kelereng dapat ditulis ....", ["4 x 3", "3 x 3", "4 + 3", "4 x 4"], "A", "4 kelompok masing-masing 3 kelereng ditulis 4 x 3.")
mc("c2", "mudah", T, Kn, S2, "Bentuk 6 + 6 + 6 menyatakan penjumlahan angka 6 sebanyak ....", ["3 kali", "2 kali", "4 kali", "6 kali"], "A", "Angka 6 dijumlahkan sebanyak 3 kali.")
tf("c2", "mudah", T, Kn, S3, "Bentuk 2 x 7 sama artinya dengan 7 + 7.", "Benar", "2 kali angka 7 dijumlahkan.")
sa("c2", "mudah", T, Kn, S4, "Berapakah hasil dari 4 x 2?", "8", "4 x 2 = 2 + 2 + 2 + 2 = 8.", verifikasi={"ekspresi": "4 * 2", "hasil": "8"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Berapakah hasil penjumlahan 7 + 7 + 7?", ["21", "20", "22", "14"], "A", "7 + 7 + 7 = 21.", "Salah menjumlahkan tiga bilangan", verifikasi={"ekspresi": "7 + 7 + 7", "hasil": "21"})
mc("c3", "sedang", R, Pr, S3, "Penjumlahan 8 + 8 + 8 + 8 jika ditulis dalam bentuk perkalian menjadi ....", ["4 x 8", "8 x 4", "4 + 8", "8 x 8"], "A", "Ada 4 suku angka 8, ditulis 4 x 8.", "Menulis perkalian terbalik")

# Terarah (6): S1, S2, S3, S4, S2, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Ada 5 piring buah. Tiap piring berisi 3 jeruk. Berapa total jeruk seluruhnya?", ["15 jeruk", "12 jeruk", "18 jeruk", "16 jeruk"], "A", "5 kelompok berisi 3 jeruk = 5 x 3 = 15 jeruk.", verifikasi={"ekspresi": "5 * 3", "hasil": "15"})
mc("c3", "mudah", T, Pr, S4, "Berapakah hasil dari 3 x 6?", ["18", "15", "21", "16"], "A", "3 x 6 = 6 + 6 + 6 = 18.", verifikasi={"ekspresi": "3 * 6", "hasil": "18"})
tf("c3", "sedang", T, Pr, S2, "Bentuk perkalian dari 9 + 9 adalah 9 x 9.", "Salah", "9 + 9 artinya 2 kali angka 9, jadi ditulis 2 x 9 bukan 9 x 9.")
mc("c3", "sedang", T, Pr, S3, "Ada 5 piring, tiap piring berisi 4 kue. Berapa banyak kue seluruhnya?", ["20 kue", "16 kue", "24 kue", "18 kue"], "A", "5 x 4 = 20 kue.", verifikasi={"ekspresi": "5 * 4", "hasil": "20"})
tf("c3", "sedang", T, Pr, S4, "Hasil dari 4 x 5 sama dengan hasil dari 5 x 4 yaitu 20.", "Benar", "Keduanya bernilai 20 karena sifat pertukaran perkalian.")
sa("c3", "sedang", T, Pr, S4, "Berapakah hasil perkalian dari 6 x 3?", "18", "6 x 3 = 3 + 3 + 3 + 3 + 3 + 3 = 18.", verifikasi={"ekspresi": "6 * 3", "hasil": "18"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Tiga kotak masing-masing berisi 6 pensil warna. Berapa pensil seluruhnya?", ["18 pensil", "15 pensil", "21 pensil", "16 pensil"], "A", "3 x 6 = 6 + 6 + 6 = 18 pensil.", verifikasi={"ekspresi": "3 * 6", "hasil": "18"})
mc("c3", "sedang", X, Pr, S2, "Bentuk penjumlahan berulang dari 4 x 6 adalah ....", ["6 + 6 + 6 + 6", "4 + 4 + 4 + 4 + 4 + 4", "4 + 6", "6 x 4"], "A", "4 x 6 berarti 6 dijumlahkan 4 kali.")
tf("c3", "sedang", X, Pr, S3, "Perkalian 3 x 5 artinya 3 ditambah 3 sebanyak lima kali.", "Salah", "3 x 5 artinya 5 ditambah 5 ditambah 5 (angka 5 sebanyak 3 kali).")
sa("c3", "sedang", X, Pr, S4, "Berapakah hasil dari 7 x 2?", "14", "7 x 2 = 2 + 2 + 2 + 2 + 2 + 2 + 2 = 14.", verifikasi={"ekspresi": "7 * 2", "hasil": "14"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Berapakah hasil dari penjumlahan 9 + 9 + 9?", ["27", "26", "28", "18"], "A", "9 + 9 + 9 = 27.", verifikasi={"ekspresi": "9 + 9 + 9", "hasil": "27"})
mc("c3", "sedang", K, Pr, S4, "Berapakah hasil dari 4 x 7?", ["28", "24", "32", "26"], "A", "4 x 7 = 7 + 7 + 7 + 7 = 28.", verifikasi={"ekspresi": "4 * 7", "hasil": "28"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S3
mc("c4", "sedang", T, Kn, S1, "Kotak A isi 4, B isi 5, C isi 4. Bisakah dihitung dengan 3 x 4?", ["tidak bisa karena isi kotak B berbeda", "bisa langsung dihitung", "bisa jika kotak A dikurangi", "tidak tahu"], "A", "Semua kelompok harus persis sama banyak.")
mc("c4", "sedang", T, Kn, S2, "Manakah dari pilihan berikut yang bernilai sama dengan 6 + 6 + 6 + 6?", ["4 x 6", "6 x 6", "4 + 6", "6 + 4"], "A", "Penjumlahan 6 sebanyak 4 kali adalah 4 x 6.")
tf("c4", "sedang", T, Kn, S3, "Secara arti konsep benda, 3 piring isi 2 kue berbeda dari 2 piring isi 3 kue.", "Benar", "Kelompok dan isinya berbeda, meski hasil total kuenya sama-sama 6.")
tf("c4", "sedang", T, Kn, S4, "Hasil dari 3 x 8 lebih kecil daripada hasil 4 x 6.", "Salah", "3 x 8 = 24 dan 4 x 6 = 24. Hasil keduanya sama besar.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari 5 x 6?", "30", "5 x 6 = 6 + 6 + 6 + 6 + 6 = 30.", verifikasi={"ekspresi": "5 * 6", "hasil": "30"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Di meja ada 6 vas bunga. Tiap vas ada 4 mawar. Berapa seluruh mawar di meja?", ["24 mawar", "20 mawar", "28 mawar", "22 mawar"], "A", "6 x 4 = 24 mawar.", verifikasi={"ekspresi": "6 * 4", "hasil": "24"})
mc("c4", "sedang", X, Kn, S3, "Budi punya 4 kandang ayam, tiap kandang 5 ayam. Berapa jumlah ayam seluruhnya?", ["20 ekor", "16 ekor", "24 ekor", "18 ekor"], "A", "4 x 5 = 20 ekor.", verifikasi={"ekspresi": "4 * 5", "hasil": "20"})
tf("c4", "sedang", X, Kn, S2, "Bentuk 5 x 1 artinya angka 5 dijumlahkan berulang sebanyak lima kali.", "Salah", "5 x 1 artinya angka 1 yang dijumlahkan sebanyak 5 kali.")
mc("c4", "sulit", X, Me, S4, "Manakah pernyataan perkalian di bawah ini yang hasilnya PALING BESAR?", ["4 x 8", "5 x 6", "3 x 9", "6 x 4"], "A", "4 x 8 = 32, 5 x 6 = 30, 3 x 9 = 27, 6 x 4 = 24. Paling besar 32.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Jika N = 7 + 7 + 7 + 7 + 7, maka nilai N sama dengan perkalian ....", ["5 x 7", "7 x 5", "7 + 5", "5 + 7"], "A", "Ada 5 kali penjumlahan angka 7: 5 x 7.")
mc("c4", "sulit", K, Me, S3, "Dono menulis 2 x 6 = 6 + 6. Apakah Dono tepat secara konsep?", ["tepat", "salah", "ragu-ragu", "kurang angka"], "A", "2 x 6 artinya 2 kelompok berisi 6, jadi 6 + 6 (Dono tepat).")
tf("c4", "sulit", K, Me, S4, "Jika sebuah bilangan dikalikan 1, hasilnya selalu bilangan itu sendiri.", "Benar", "Unsur identitas perkalian: N x 1 = N.")
mc("c4", "sulit", K, Me, S4, "Pak RT membeli 4 kotak kue. Tiap kotak isi 8 kue. Berapa total kue Pak RT?", ["32 kue", "28 kue", "36 kue", "30 kue"], "A", "4 x 8 = 32 kue.", verifikasi={"ekspresi": "4 * 8", "hasil": "32"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Ada 5 rak buku, tiap rak ada 8 buku. Kalimat perkalian total buku adalah ....", ["5 x 8 = 40", "8 + 5 = 13", "8 - 5 = 3", "5 + 8 = 40"], "A", "5 kelompok masing-masing 8 buku: 5 x 8 = 40 buku.")
mc("c5", "sedang", T, Me, S2, "Berapakah nilai titik-titik pada kalimat: 4 x 5 = 5 + 5 + ... + 5?", ["5", "4", "10", "20"], "A", "Penjumlahan angka 5 sebanyak 4 suku: 5 + 5 + 5 + 5.", verifikasi={"ekspresi": "5", "hasil": "5"})
mc("c5", "sedang", T, Me, S3, "Manakah pasangan bentuk penjumlahan berulang dan perkalian yang BENAR?", ["3 x 7 = 7 + 7 + 7", "4 x 2 = 4 + 4", "2 x 5 = 2 + 2 + 2 + 2 + 2", "5 x 3 = 5 + 5 + 5"], "A", "3 x 7 = 7 + 7 + 7 adalah pasangan yang tepat.")
mc("c5", "sulit", T, Me, S4, "Berapakah hasil dari (3 x 4) + (2 x 4)?", ["20", "16", "24", "18"], "A", "3 x 4 = 12; 2 x 4 = 8; 12 + 8 = 20.", verifikasi={"ekspresi": "(3 * 4) + (2 * 4)", "hasil": "20"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Siti ingin menghitung 6 x 5 tetapi lupa. Cara termudah membantu Siti adalah ....", ["menjumlahkan angka 5 sebanyak enam kali", "menghitung mundur dari 30", "menebak angka", "mengurangi 6 dengan 5"], "A", "Menghitung 5 + 5 + 5 + 5 + 5 + 5 = 30.")
mc("c5", "sulit", K, Me, S4, "Berapakah hasil dari (4 x 5) + 15?", ["35", "30", "40", "25"], "A", "4 x 5 = 20; 20 + 15 = 35.", verifikasi={"ekspresi": "(4 * 5) + 15", "hasil": "35"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Mengapa manusia menciptakan operasi perkalian daripada terus menggunakan penjumlahan?", ["karena perkalian membuat perhitungan kelompok banyak menjadi jauh lebih cepat", "karena penjumlahan dilarang", "agar angka menjadi kecil", "karena hanya ada satu cara"], "A", "Perkalian adalah cara cepat dan ringkas menghitung kelompok sama banyak.")
mc("c6", "sulit", K, Me, S3, "Buatlah kesimpulan: jika ada A kelompok masing-masing berisi B benda, total benda adalah ....", ["A x B", "A + B", "A - B", "B - A"], "A", "Total benda dinyatakan dengan A x B.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil dari (3 x 6) + (4 x 5)!", ["38", "28", "48", "36"], "A", "3 x 6 = 18; 4 x 5 = 20; 18 + 20 = 38.", verifikasi={"ekspresi": "(3 * 6) + (4 * 5)", "hasil": "38"})
mc("c6", "sulit", P, Me, S4, "Ada 5 meja, tiap meja 4 kursi. Datang lagi 8 kursi. Berapa total kursi sekarang?", ["28 kursi", "24 kursi", "26 kursi", "30 kursi"], "A", "5 x 4 = 20; 20 + 8 = 28 kursi.", verifikasi={"ekspresi": "(5 * 4) + 8", "hasil": "28"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab45_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab45.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
