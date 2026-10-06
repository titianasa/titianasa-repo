#!/usr/bin/env python3
"""
Generator dan validator Bab 47 Matematika Kelas 2 SD:
"Makna Pembagian sebagai Pembagian Rata" (Fase A)
bab_id: 743d95a7-c293-4491-af96-6eedbd1fe595
article_id: a8596730-7c2e-413b-9f83-fd93d4b144b1
quiz_id: 500f2235-0fb4-4906-981b-ffa0a2350b58
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "e7f8a9b0c101"  # Berbagi Sama Banyak
S2 = "f8a9b0c1d202"  # Pengurangan Berulang sampai Habis
S3 = "a9b0c1d2e303"  # Menulis Kalimat Pembagian
S4 = "b0c1d2e3f404"  # Menghitung Hasil Bagi Sederhana

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Pernahkah kamu berbagi kue dengan teman?
Berbagi harus dilakukan secara adil.
Semua orang mendapat bagian sama banyak.
Inilah inti dari pembagian.
Misalnya ada enam butir permen.
Dibagikan kepada dua orang anak.
Tiap anak mendapat tiga butir.
Tidak ada yang merasa dirugikan.

:::definition
title: Pembagian Rata
Pembagian rata adalah membagi benda sama banyak tanpa tersisa.
:::"""

s2_content = """Pembagian dihitung dengan pengurangan berulang.
Kurangi bilangan awal sampai bernilai nol.
Misalnya dua belas permen dibagi tiga.
Dua belas kurang tiga jadi sembilan.
Sembilan kurang tiga jadi enam.
Enam kurang tiga jadi tiga.
Tiga kurang tiga jadi nol.
Kita mengurangi sebanyak empat kali.
Maka dua belas bagi tiga empat.

:::steps
title: Menghitung dengan Pengurangan Berulang
1. Kurangkan bilangan awal dengan pembagi.
2. Ulangi terus sampai habis nol.
3. Hitung berapa kali kamu mengurang.
:::"""

s3_content = """Kita menggunakan tanda titik dua.
Tanda ini dibaca dibagi.
Dua belas dibagi tiga ditulis singkat.
Dua belas tanda titik dua tiga.
Hasilnya ditulis sama dengan empat.
Angka depan adalah jumlah awal benda.
Angka tengah adalah pembaginya.
Angka hasil adalah banyaknya pengurangan."""

s4_content = """Mari kita coba hitung bersama.
Sepuluh jeruk dibagikan kepada dua piring.
Sepuluh kurang dua terus sampai habis.
Tiap piring berisi lima jeruk.
Sepuluh bagi dua adalah lima.
Delapan bagi empat adalah dua.
Pembagian kebalikan dari perkalian.
Semakin banyak berlatih kamu semakin pintar!

:::common_trap
title: Mengira Hasil adalah Sisa Nol
Hasil pembagian bukan angka nol di akhir.
Hasil pembagian adalah berapa kali pengurangan dilakukan!
Dua belas bagi tiga adalah empat, bukan nol.
:::

:::callout
variant: summary
title: Ringkasan
text: Pembagian adalah pengurangan berulang dari kumpulan benda sampai habis bernilai nol.
:::"""

sections = [
    {
        "id": S1,
        "title": "Berbagi Sama Banyak",
        "minutes": 6,
        "goal": "Siswa memahami makna pembagian sebagai proses membagi benda secara rata dan adil kepada kelompok.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Pengurangan Berulang sampai Habis",
        "minutes": 6,
        "goal": "Siswa mampu menghitung hasil pembagian melalui proses pengurangan berulang sampai bersisa nol.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Menulis Kalimat Pembagian",
        "minutes": 6,
        "goal": "Siswa mampu menuliskan notasi pembagian dengan tanda titik dua beserta artinya secara tepat.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menghitung Hasil Bagi Sederhana",
        "minutes": 6,
        "goal": "Siswa mampu menentukan hasil pembagian bilangan sederhana sampai 20 dengan teliti.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Makna Pembagian sebagai Pembagian Rata",
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
# 2. DEFINISI BANK 50 SOAL BAB 47
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
mc("c1", "mudah", D, F, S1, "Pembagian dapat diartikan sebagai bentuk pengurangan ....", ["berulang", "satu kali", "penjumlahan", "perkalian"], "A", "Pembagian adalah pengurangan berulang bilangan yang sama sampai habis.")
tf("c1", "mudah", D, F, S3, "Tanda titik dua dalam matematika digunakan untuk menyatakan pembagian.", "Benar", "Tanda : melambangkan operasi pembagian.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Bentuk pengurangan berulang dari 8 : 2 adalah ....", ["8 - 2 - 2 - 2 - 2 = 0", "8 - 2 = 6", "8 + 2 + 2 = 12", "8 - 4 = 4"], "A", "8 dikurang 2 berulang kali sampai habis nol: 8 - 2 - 2 - 2 - 2 = 0.")
mc("c1", "mudah", T, F, S3, "Berapakah hasil dari 6 : 2?", ["3", "2", "4", "5"], "A", "6 : 2 = 3.", verifikasi={"ekspresi": "6 / 2", "hasil": "3"})
sa("c1", "mudah", T, F, S4, "Berapakah hasil dari 8 : 4?", "2", "8 : 4 = 2.", verifikasi={"ekspresi": "8 / 4", "hasil": "2"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Membagi rata 10 apel ke 2 keranjang artinya tiap keranjang berisi ....", ["5 apel", "4 apel", "6 apel", "2 apel"], "A", "10 : 2 = 5 apel tiap keranjang.", verifikasi={"ekspresi": "10 / 2", "hasil": "5"})
tf("c2", "mudah", D, Kn, S2, "Pada pembagian 15 : 5, angka 15 dikurangi 5 sebanyak tiga kali.", "Benar", "15 - 5 - 5 - 5 = 0, dikurangi 3 kali.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S3, "Berapakah hasil dari 12 : 3?", ["4", "3", "5", "6"], "A", "12 : 3 = 4.", "Menjawab angka sisa nol bukan banyak pengurangan", verifikasi={"ekspresi": "12 / 3", "hasil": "4"})
mc("c2", "mudah", R, Kn, S4, "Berapakah hasil dari 14 : 2?", ["7", "6", "8", "5"], "A", "14 : 2 = 7.", "Keliru menghitung bagi dua", verifikasi={"ekspresi": "14 / 2", "hasil": "7"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Ada 12 kue dibagi sama rata ke 4 piring. Kalimat pembagiannya adalah ....", ["12 : 4 = 3", "12 : 3 = 4", "12 - 4 = 8", "12 + 4 = 16"], "A", "12 kue dibagi ke 4 piring: 12 : 4 = 3 kue.")
mc("c2", "mudah", T, Kn, S2, "Pengurangan 9 - 3 - 3 - 3 = 0 menunjukkan kalimat pembagian ....", ["9 : 3 = 3", "9 : 3 = 0", "9 - 3 = 6", "3 x 3 = 0"], "A", "Pengurangan 3 sebanyak 3 kali: 9 : 3 = 3.")
tf("c2", "mudah", T, Kn, S3, "Hasil dari pembagian 10 : 2 adalah angka nol.", "Salah", "Hasilnya adalah 5 (banyaknya pengurangan), bukan sisa nol.")
sa("c2", "mudah", T, Kn, S4, "Berapakah hasil dari 16 : 4?", "4", "16 : 4 = 4.", verifikasi={"ekspresi": "16 / 4", "hasil": "4"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Berapa kalikah angka 4 mengurangkan 16 sampai habis menjadi nol?", ["4 kali", "3 kali", "5 kali", "2 kali"], "A", "16 - 4 - 4 - 4 - 4 = 0, yaitu 4 kali.", "Keliru menghitung langkah pengurangan")
mc("c3", "sedang", R, Pr, S4, "Berapakah hasil dari 18 : 3?", ["6", "5", "7", "8"], "A", "18 : 3 = 6.", "Salah fakta dasar pembagian 3", verifikasi={"ekspresi": "18 / 3", "hasil": "6"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Ada 15 mangga dibagikan kepada 3 anak sama banyak. Berapa mangga tiap anak?", ["5 buah", "4 buah", "6 buah", "3 buah"], "A", "15 : 3 = 5 buah.", verifikasi={"ekspresi": "15 / 3", "hasil": "5"})
mc("c3", "mudah", T, Pr, S4, "Berapakah hasil dari 18 : 2?", ["9", "8", "7", "6"], "A", "18 : 2 = 9.", verifikasi={"ekspresi": "18 / 2", "hasil": "9"})
tf("c3", "sedang", T, Pr, S2, "Bentuk pengurangan 20 - 5 - 5 - 5 - 5 = 0 sama artinya dengan 20 : 5 = 5.", "Salah", "Angka 5 dikurangkan sebanyak 4 kali, jadi hasilnya 4 bukan 5.")
mc("c3", "sedang", T, Pr, S3, "Berapakah hasil dari 20 : 4?", ["5", "4", "6", "3"], "A", "20 : 4 = 5.", verifikasi={"ekspresi": "20 / 4", "hasil": "5"})
tf("c3", "sedang", T, Pr, S4, "Hasil dari 12 : 2 lebih kecil daripada hasil 12 : 3.", "Salah", "12 : 2 = 6 dan 12 : 3 = 4. 6 lebih besar dari 4.")
sa("c3", "sedang", T, Pr, S4, "Berapakah hasil dari 20 : 5?", "4", "20 : 5 = 4.", verifikasi={"ekspresi": "20 / 5", "hasil": "4"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Ibu membagikan 16 roti ke dalam 2 kotak sama banyak. Berapa isi tiap kotak?", ["8 roti", "6 roti", "7 roti", "9 roti"], "A", "16 : 2 = 8 roti.", verifikasi={"ekspresi": "16 / 2", "hasil": "8"})
mc("c3", "sedang", X, Pr, S2, "Pengurangan berulang 15 - 5 - 5 - 5 = 0 bernilai sama dengan pembagian ....", ["15 : 5 = 3", "15 : 3 = 5", "15 - 5 = 10", "5 : 5 = 1"], "A", "15 dikurangi 5 sebanyak 3 kali: 15 : 5 = 3.")
tf("c3", "sedang", X, Pr, S3, "Sebuah bilangan jika dibagi dengan bilangan itu sendiri hasilnya selalu 1.", "Benar", "Contoh: 5 : 5 = 1, 8 : 8 = 1.")
sa("c3", "sedang", X, Pr, S4, "Berapakah hasil dari 24 : 4?", "6", "24 : 4 = 6.", verifikasi={"ekspresi": "24 / 4", "hasil": "6"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Berapakah hasil dari 21 : 3?", ["7", "6", "8", "9"], "A", "21 : 3 = 7.", verifikasi={"ekspresi": "21 / 3", "hasil": "7"})
mc("c3", "sedang", K, Pr, S4, "Berapakah hasil dari 25 : 5?", ["5", "4", "6", "7"], "A", "25 : 5 = 5.", verifikasi={"ekspresi": "25 / 5", "hasil": "5"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Ada 18 kelereng dibagikan ke 3 anak. Mengapa tiap anak tidak boleh dapat 7 kelereng?", ["karena 3 x 7 = 21 melebihi kelereng yang ada", "karena 7 bilangan ganjil", "karena harus dapat 5", "karena 18 bilangan genap"], "A", "18 : 3 = 6. Jika 7, butuh 21 kelereng sehingga kelereng kurang.")
mc("c4", "sedang", T, Kn, S2, "Manakah dari pengurangan berulang berikut yang menyatakan 14 : 2 = 7?", ["14 dikurang 2 sebanyak 7 kali hingga nol", "14 dikurang 7 sebanyak 2 kali", "14 dikurang 2 satu kali", "7 dikurang 2"], "A", "14 : 2 = 7 artinya 14 dikurangi 2 sebanyak 7 kali.")
tf("c4", "sedang", T, Kn, S3, "Makin besar bilangan pembagi, hasil bagi dari jumlah benda yang sama makin kecil.", "Benar", "Makin banyak anak yang berbagi, tiap anak dapat makin sedikit.")
tf("c4", "sedang", T, Kn, S4, "Hasil dari 18 : 3 sama dengan hasil dari 24 : 6.", "Salah", "18 : 3 = 6, sedangkan 24 : 6 = 4. Keduanya tidak sama.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari (16 : 2) + 5?", "13", "16 : 2 = 8; 8 + 5 = 13.", verifikasi={"ekspresi": "(16 / 2) + 5", "hasil": "13"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Pak Guru punya 24 buku, dibagikan ke 4 meja sama rata. Berapa buku tiap meja?", ["6 buku", "5 buku", "7 buku", "8 buku"], "A", "24 : 4 = 6 buku.", verifikasi={"ekspresi": "24 / 4", "hasil": "6"})
mc("c4", "sedang", X, Kn, S3, "Sebuah bilangan jika dibagi 1 hasilnya adalah ....", ["bilangan itu sendiri", "nol", "satu", "dua"], "A", "N : 1 = N (tidak dibagi ke siapapun selain satu bagian utuh).")
tf("c4", "sedang", X, Kn, S2, "Hasil pembagian 18 : 6 adalah 6 karena angkanya dikurangkan satu kali.", "Salah", "18 : 6 = 3 karena 18 dikurangi 6 sebanyak 3 kali.")
mc("c4", "sulit", X, Me, S4, "Di antara pembagian berikut, manakah yang hasilnya PALING BESAR?", ["18 : 2", "20 : 4", "16 : 4", "15 : 3"], "A", "18 : 2 = 9; 20 : 4 = 5; 16 : 4 = 4; 15 : 3 = 5. Paling besar 9.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Dono membagikan 20 jeruk ke 5 piring. Tiap piring mendapat ....", ["4 jeruk", "5 jeruk", "3 jeruk", "6 jeruk"], "A", "20 : 5 = 4 jeruk.", verifikasi={"ekspresi": "20 / 5", "hasil": "4"})
mc("c4", "sulit", K, Me, S2, "Ali menghitung 16 : 4 dan menjawab 0. Apa yang perlu diperbaiki dari pemahaman Ali?", ["Ali menjawab sisa akhir bukan banyaknya langkah pengurangan", "Ali salah mengurangkan", "Ali harusnya menjumlahkan", "jawaban Ali sudah tepat"], "A", "Hasil bagi adalah frekuensi pengurangannya (4 kali), bukan sisa nol.")
tf("c4", "sulit", K, Me, S4, "Hasil dari 20 : 2 dua kali lebih besar daripada 20 : 4.", "Benar", "20 : 2 = 10 dan 20 : 4 = 5. 10 adalah dua kali dari 5.")
mc("c4", "sulit", K, Me, S4, "Berapakah hasil dari (30 : 5) + (12 : 3)?", ["10", "8", "12", "9"], "A", "30 : 5 = 6; 12 : 3 = 4; 6 + 4 = 10.", verifikasi={"ekspresi": "(30 / 5) + (12 / 3)", "hasil": "10"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Rani ingin membagi 18 bunga ke dalam beberapa vas agar tiap vas isi 6. Berapa vas?", ["3 vas", "2 vas", "4 vas", "5 vas"], "A", "18 : 6 = 3 vas bunga.", verifikasi={"ekspresi": "18 / 6", "hasil": "3"})
mc("c5", "sedang", T, Me, S2, "Berapakah nilai titik-titik pada pengurangan: 12 - 4 - 4 - ... = 0?", ["4", "3", "2", "0"], "A", "12 - 4 - 4 - 4 = 0. Jadi titik-titik bernilai 4.")
mc("c5", "sedang", T, Me, S3, "Berapakah nilai M pada kalimat matematika: M : 3 = 6?", ["18", "15", "21", "12"], "A", "18 : 3 = 6, jadi M = 18.", verifikasi={"ekspresi": "3 * 6", "hasil": "18"})
mc("c5", "sulit", T, Me, S4, "Berapakah hasil dari (24 : 3) - (10 : 2)?", ["3", "2", "4", "5"], "A", "24 : 3 = 8; 10 : 2 = 5; 8 - 5 = 3.", verifikasi={"ekspresi": "(24 / 3) - (10 / 2)", "hasil": "3"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Berapakah nilai K pada kalimat matematika: 28 : K = 7?", ["4", "3", "5", "6"], "A", "28 : 4 = 7, jadi K = 4.", verifikasi={"ekspresi": "28 / 7", "hasil": "4"})
mc("c5", "sulit", K, Me, S4, "Berapakah hasil dari (20 : 2) - (15 : 5)?", ["7", "6", "8", "5"], "A", "20 : 2 = 10; 15 : 5 = 3; 10 - 3 = 7.", verifikasi={"ekspresi": "(20 / 2) - (15 / 5)", "hasil": "7"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Mengapa syarat pembagian matematika adalah membagi rata, bukan membagi sembarang?", ["karena pembagian menghasilkan kelompok yang bernilai sama persis", "karena lebih mudah", "karena sudah peraturan", "agar tidak lelah"], "A", "Pembagian adalah operasi partisi adil menghasilkan kelompok bernilai sama.")
mc("c6", "sulit", K, Me, S3, "Hubungan apa yang terjadi jika 4 x 5 = 20 diubah menjadi pembagian?", ["20 : 5 = 4 atau 20 : 4 = 5", "20 : 2 = 10", "20 - 4 = 16", "5 : 4 = 1"], "A", "Perkalian dan pembagian saling berkebalikan: 20 : 5 = 4.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi campuran: (30 : 3) + (16 : 4) - (12 : 2)!", ["8", "6", "10", "7"], "A", "30 : 3 = 10; 16 : 4 = 4; 12 : 2 = 6; 10 + 4 - 6 = 8.", verifikasi={"ekspresi": "(30 / 3) + (16 / 4) - (12 / 2)", "hasil": "8"})
mc("c6", "sulit", P, Me, S4, "Ada 24 pensil dibagikan ke 4 anak. Seorang anak memberi 2 ke adiknya. Berapa sisanya?", ["4 pensil", "5 pensil", "3 pensil", "6 pensil"], "A", "24 : 4 = 6 pensil; 6 - 2 = 4 pensil.", verifikasi={"ekspresi": "(24 / 4) - 2", "hasil": "4"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab47_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab47.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
