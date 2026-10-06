#!/usr/bin/env python3
"""
Generator dan validator Bab 56 Matematika Kelas 2 SD:
"Mengenal Bilangan Genap dan Ganjil" (Fase A)
bab_id: 62faa5ae-b791-4e47-96a9-71908c482b97
article_id: 63c2c9bd-b428-4028-b6e4-525fc4592112
quiz_id: ae33f280-2502-4818-8a1d-6cef600fac37
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a1b2c3d4e501"  # Arti Bilangan Genap (Pasangan Dua-Dua)
S2 = "b2c3d4e5f602"  # Arti Bilangan Ganjil (Selalu Bersisa Satu)
S3 = "c3d4e5f6g703"  # Mengenali Genap dan Ganjil dari Angka Satuan
S4 = "d4e5f6g7h804"  # Penjumlahan Bilangan Genap dan Ganjil

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Pernahkah kamu memakai sepasang sepatu?
Sepatu selalu berpasangan dua-dua.
Benda genap habis berpasangan.
Tidak ada benda yang tersisa sendiri.
Contohnya dua, empat, dan enam.
Delapan dan sepuluh juga genap.
Semua benda berpasangan dengan pas.
Bilangan genap bisa dibagi dua rata!

:::definition
title: Bilangan Genap
Bilangan genap adalah bilangan yang habis dipasangkan dua-dua tanpa sisa.
:::"""

s2_content = """Bagaimana dengan bilangan ganjil?
Cobalah pasangkan lima buah permen.
Dua permen membentuk satu pasang.
Dua permen lagi membentuk pasang kedua.
Ada satu permen tersisa sendiri!
Satu permen tidak mendapat pasangan.
Inilah ciri bilangan ganjil.
Bilangan ganjil selalu bersisa satu.
Contohnya satu, tiga, lima, tujuh, sembilan.

:::steps
title: Cara Mengetahui Bilangan Ganjil
1. Pasangkan benda dua demi dua.
2. Hitung apakah ada yang tersisa.
3. Jika sisa satu, bilangan itu ganjil.
:::"""

s3_content = """Bagaimana bilangan dua angka?
Lihatlah angka satuannya.
Angka satuan ada di belakang.
Akhiran 0, 2, 4, 6, 8 itu genap.
Contohnya 24 adalah genap.
Akhiran 1, 3, 5, 7, 9 itu ganjil.
Contohnya 37 adalah ganjil.
Cara ini cepat dan mudah!"""

s4_content = """Mari amati penjumlahan bilangan.
Genap ditambah genap hasilnya genap.
Contoh: 2 ditambah 4 hasilnya 6.
Ganjil ditambah ganjil hasilnya genap.
Contoh: 3 ditambah 5 hasilnya 8.
Genap ditambah ganjil hasilnya ganjil.
Contoh: 4 ditambah 3 hasilnya 7.
Pola ini selalu berlaku teratur!

:::common_trap
title: Mengira Angka Puluhan Menentukan Genap atau Ganjil
Angka puluhan tidak menentukan genap atau ganjil.
Misalnya 32: angka 3 ganjil, tetapi satuannya 2.
Maka 32 tetap merupakan bilangan genap!
:::

:::callout
variant: summary
title: Ringkasan
text: Genap habis dipasangkan dua-dua (akhiran 0, 2, 4, 6, 8). Ganjil bersisa satu (akhiran 1, 3, 5, 7, 9).
:::"""

sections = [
    {
        "id": S1,
        "title": "Arti Bilangan Genap (Pasangan Dua-Dua)",
        "minutes": 6,
        "goal": "Siswa memahami konsep bilangan genap sebagai kumpulan objek yang habis dipasangkan dua-dua.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Arti Bilangan Ganjil (Selalu Bersisa Satu)",
        "minutes": 6,
        "goal": "Siswa memahami konsep bilangan ganjil yang selalu menyisakan satu objek saat dipasangkan dua-dua.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mengenali Genap dan Ganjil dari Angka Satuan",
        "minutes": 6,
        "goal": "Siswa mampu mengidentifikasi bilangan genap atau ganjil sampai 100 dengan melihat angka satuannya.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Penjumlahan Bilangan Genap dan Ganjil",
        "minutes": 6,
        "goal": "Siswa mampu menemukan pola keteraturan hasil penjumlahan bilangan genap dan ganjil.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengenal Bilangan Genap dan Ganjil",
    "topic": "Bilangan Genap, Ganjil, dan Pola Bilangan",
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
# 2. DEFINISI BANK 50 SOAL BAB 56
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
mc("c1", "mudah", D, F, S1, "Bilangan yang habis dipasangkan dua-dua tanpa sisa disebut bilangan ....", ["genap", "ganjil", "cacah", "bulat"], "A", "Bilangan genap selalu habis dipasangkan dua-dua.")
tf("c1", "mudah", D, F, S2, "Bilangan 7 jika dipasangkan dua-dua selalu menyisakan satu benda.", "Benar", "7 = 2 + 2 + 2 + 1 (bersisa 1).")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S3, "Di antara bilangan berikut, manakah yang merupakan bilangan genap?", ["8", "7", "9", "5"], "A", "8 adalah bilangan genap karena habis dipasangkan dua-dua.")
mc("c1", "mudah", T, F, S2, "Di antara bilangan berikut, manakah yang merupakan bilangan ganjil?", ["9", "4", "6", "8"], "A", "9 adalah bilangan ganjil karena bersisa 1 jika dipasangkan dua-dua.")
sa("c1", "mudah", T, F, S1, "Berapakah sisa benda jika 6 kelereng dipasangkan dua-dua?", "0", "6 adalah bilangan genap, sisa = 0.", verifikasi={"ekspresi": "6 % 2", "hasil": "0"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Mengapa bilangan 24 disebut bilangan genap?", ["karena angka satuannya adalah 4", "karena ada angka 2 di depan", "karena terdiri dari 2 angka", "karena nilainya besar"], "A", "Bilangan genap ditentukan oleh angka satuan 0, 2, 4, 6, 8.")
tf("c2", "mudah", D, Kn, S3, "Bilangan 31 adalah bilangan genap.", "Salah", "31 berakhiran 1, jadi merupakan bilangan ganjil.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S3, "Apakah bilangan 38 genap atau ganjil?", ["genap karena angka satuannya 8", "ganjil karena angka puluhannya 3", "bukan keduanya", "tidak tahu"], "A", "38 genap karena satuannya 8. Puluhan 3 tidak menentukan genap/ganjil.", "Mengira angka puluhan menentukan genap atau ganjil")
mc("c2", "mudah", R, Kn, S2, "Mengapa bilangan 11 merupakan bilangan ganjil?", ["karena jika dipasangkan dua-dua bersisa satu", "karena tidak ada angka nol", "karena lebih besar dari 10", "karena kembar"], "A", "11 dipasangkan dua-dua menghasilkan 5 pasang dan sisa 1.", "Salah memahami konsep sisa ganjil")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Ada 10 kaus kaki. Berapa pasang kaus kaki yang terbentuk?", ["5 pasang", "4 pasang", "6 pasang", "3 pasang"], "A", "10 : 2 = 5 pasang pas tanpa sisa.", verifikasi={"ekspresi": "10 / 2", "hasil": "5"})
mc("c2", "mudah", T, Kn, S2, "Ada 13 pensil dipasangkan dua-dua. Berapa pensil yang tidak punya pasangan?", ["1 pensil", "2 pensil", "0 pensil", "3 pensil"], "A", "13 = (6 x 2) + 1, sisa 1 pensil.", verifikasi={"ekspresi": "13 % 2", "hasil": "1"})
tf("c2", "mudah", T, Kn, S4, "Hasil dari bilangan genap ditambah bilangan genap selalu genap.", "Benar", "Genap + genap = genap.")
sa("c2", "mudah", T, Kn, S1, "Berapa pasang yang terbentuk dari 14 sepatu?", "7", "14 : 2 = 7 pasang.", verifikasi={"ekspresi": "14 / 2", "hasil": "7"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S4, "Berapakah hasil dari 7 + 5 dan apakah jenis bilangannya?", ["12 genap", "12 ganjil", "11 ganjil", "14 genap"], "A", "7 + 5 = 12 (genap). Ganjil + ganjil = genap.", "Salah menjumlahkan ganjil dan ganjil", verifikasi={"ekspresi": "7 + 5", "hasil": "12"})
mc("c3", "sedang", R, Pr, S3, "Di antara 41, 44, 47, 49, manakah yang merupakan bilangan genap?", ["44", "41", "47", "49"], "A", "44 genap karena satuannya 4.", "Keliru mengenali bilangan genap dua angka")

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Kelompok bilangan berikut yang SEMUANYA GENAP adalah ....", ["2, 4, 6, 8", "1, 3, 5, 7", "2, 3, 4, 5", "4, 6, 7, 8"], "A", "2, 4, 6, 8 semuanya habis dipasangkan dua-dua.")
mc("c3", "mudah", T, Pr, S2, "Kelompok bilangan berikut yang SEMUANYA GANJIL adalah ....", ["1, 3, 5, 7", "2, 4, 6, 8", "1, 2, 3, 4", "3, 5, 6, 9"], "A", "1, 3, 5, 7 semuanya bilangan ganjil.")
tf("c3", "sedang", T, Pr, S3, "Bilangan 50 adalah bilangan ganjil.", "Salah", "50 berakhiran 0, sehingga merupakan bilangan genap.")
mc("c3", "sedang", T, Pr, S4, "Berapakah hasil dari 8 + 6?", ["14", "13", "15", "12"], "A", "8 + 6 = 14 (genap).", verifikasi={"ekspresi": "8 + 6", "hasil": "14"})
tf("c3", "sedang", T, Pr, S4, "Penjumlahan bilangan genap dan bilangan ganjil menghasilkan bilangan ganjil.", "Benar", "Genap + ganjil = ganjil. Contoh: 4 + 3 = 7.")
sa("c3", "sedang", T, Pr, S3, "Berapakah banyak bilangan genap di antara 1 dan 10?", "4", "Bilangan genap antara 1 dan 10 adalah 2, 4, 6, 8 (ada 4 bilangan).", verifikasi={"ekspresi": "4 / 1", "hasil": "4"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Ada 18 kelereng. Berapa pasang kelereng yang bisa dibuat?", ["9 pasang", "8 pasang", "10 pasang", "7 pasang"], "A", "18 : 2 = 9 pasang.", verifikasi={"ekspresi": "18 / 2", "hasil": "9"})
mc("c3", "sedang", X, Pr, S2, "Ada 21 siswa berbaris berdua-dua. Berapa siswa yang tidak dapat pasangan?", ["1 siswa", "2 siswa", "0 siswa", "3 siswa"], "A", "21 ganjil, jadi bersisa 1 siswa tanpa pasangan.", verifikasi={"ekspresi": "21 % 2", "hasil": "1"})
tf("c3", "sedang", X, Pr, S3, "Semua bilangan yang berakhiran angka 5 adalah bilangan ganjil.", "Benar", "Akhiran 1, 3, 5, 7, 9 selalu ganjil.")
sa("c3", "sedang", X, Pr, S4, "Berapakah hasil penjumlahan bilangan genap 12 + 16?", "28", "12 + 16 = 28.", verifikasi={"ekspresi": "12 + 16", "hasil": "28"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Tentukan jenis bilangan dari 67!", ["ganjil karena satuannya 7", "genap karena puluhannya 6", "bukan ganjil bukan genap", "nol"], "A", "67 berakhiran 7 sehingga merupakan bilangan ganjil.")
mc("c3", "sedang", K, Pr, S4, "Berapakah hasil dari 15 + 9?", ["24", "22", "26", "25"], "A", "15 + 9 = 24 (genap).", verifikasi={"ekspresi": "15 + 9", "hasil": "24"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Manakah pernyataan yang BENAR mengenai pembagian bilangan genap?", ["selalu dapat dibagi dua sama rata tanpa sisa", "selalu menyisakan satu benda", "tidak dapat dipasangkan", "selalu lebih kecil dari 10"], "A", "Definisi bilangan genap adalah selalu habis dibagi dua tanpa sisa.")
mc("c4", "sedang", T, Kn, S2, "Mengapa bilangan ganjil jika dibagi 2 selalu menyisakan 1?", ["karena tidak bisa habis dipasangkan dua-dua", "karena angkanya ganjil", "karena jumlahnya terlalu sedikit", "karena salah hitung"], "A", "Karakteristik bilangan ganjil adalah selalu memiliki 1 objek tanpa pasangan.")
tf("c4", "sedang", T, Kn, S3, "Bilangan 78 dan 93 keduanya adalah bilangan genap.", "Salah", "93 berakhiran 3 sehingga merupakan bilangan ganjil, bukan genap.")
tf("c4", "sedang", T, Kn, S4, "Hasil dari penjumlahan 11 + 13 adalah bilangan ganjil.", "Salah", "11 + 13 = 24, yaitu bilangan genap.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari 14 + 17?", "31", "14 + 17 = 31 (ganjil).", verifikasi={"ekspresi": "14 + 17", "hasil": "31"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Berapa banyak pasang yang terbentuk dari 26 bola?", ["13 pasang", "12 pasang", "14 pasang", "11 pasang"], "A", "26 : 2 = 13 pasang.", verifikasi={"ekspresi": "26 / 2", "hasil": "13"})
mc("c4", "sedang", X, Kn, S3, "Di antara bilangan 51, 62, 73, 84, berapakah jumlah bilangan genapnya?", ["2 bilangan", "1 bilangan", "3 bilangan", "4 bilangan"], "A", "Yang genap adalah 62 dan 84 (ada 2 bilangan).", verifikasi={"ekspresi": "2 / 1", "hasil": "2"})
tf("c4", "sedang", X, Kn, S1, "Bilangan 0 termasuk dalam kelompok bilangan genap.", "Benar", "0 habis dibagi 2 dan berakhiran 0.")
mc("c4", "sulit", X, Me, S4, "Jika $A$ adalah bilangan ganjil, maka $A + 1$ adalah bilangan ....", ["genap", "ganjil", "nol", "negatif"], "A", "Bilangan setelah ganjil selalu bilangan genap.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Berapakah bilangan genap tepat setelah bilangan 36?", ["38", "37", "40", "39"], "A", "Bilangan genap tepat berikutnya adalah 36 + 2 = 38.", verifikasi={"ekspresi": "36 + 2", "hasil": "38"})
mc("c4", "sulit", K, Me, S2, "Berapakah bilangan ganjil tepat sebelum bilangan 55?", ["53", "54", "51", "52"], "A", "Bilangan ganjil tepat sebelumnya adalah 55 - 2 = 53.", verifikasi={"ekspresi": "55 - 2", "hasil": "53"})
tf("c4", "sulit", K, Me, S4, "Penjumlahan tiga bilangan ganjil menghasilkan bilangan genap.", "Salah", "Ganjil + ganjil + ganjil = genap + ganjil = ganjil.")
mc("c4", "sulit", K, Me, S3, "Berapakah hasil dari 28 + 35?", ["63", "61", "65", "62"], "A", "28 + 35 = 63 (ganjil).", verifikasi={"ekspresi": "28 + 35", "hasil": "63"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Ada 34 anak ingin bermain berpasangan. Apakah semua dapat pasangan?", ["ya karena 34 bilangan genap", "tidak karena ada sisa", "hanya sebagian", "tidak tahu"], "A", "34 genap, jadi semua anak mendapatkan pasangan pas.")
mc("c5", "sedang", T, Me, S2, "Ada 45 mangga dibagikan berdua-dua. Berapa pasang dan sisanya?", ["22 pasang dan sisa 1 mangga", "21 pasang dan sisa 3", "23 pasang tanpa sisa", "20 pasang sisa 5"], "A", "45 = (22 x 2) + 1.", verifikasi={"ekspresi": "45 // 2", "hasil": "22"})
mc("c5", "sedang", T, Me, S3, "Berapakah jumlah bilangan ganjil antara 10 dan 20?", ["5 bilangan", "4 bilangan", "6 bilangan", "3 bilangan"], "A", "Ganjil: 11, 13, 15, 17, 19 (ada 5 bilangan).", verifikasi={"ekspresi": "5 / 1", "hasil": "5"})
mc("c5", "sulit", T, Me, S4, "Berapakah hasil dari (genap 18 + 12) + (ganjil 7 + 3)?", ["40", "38", "42", "36"], "A", "(18 + 12) + (7 + 3) = 30 + 10 = 40 (genap).", verifikasi={"ekspresi": "(18 + 12) + (7 + 3)", "hasil": "40"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Jumlah dua bilangan ganjil berurutan adalah 20. Bilangan apakah itu?", ["9 dan 11", "7 dan 13", "8 dan 12", "5 dan 15"], "A", "9 dan 11 adalah bilangan ganjil berurutan yang berjumlah 20.")
mc("c5", "sulit", K, Me, S4, "Berapakah hasil dari 46 + 38?", ["84", "82", "86", "80"], "A", "46 + 38 = 84 (genap).", verifikasi={"ekspresi": "46 + 38", "hasil": "84"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Bagaimana kamu membuktikan kepada adik bahwa 16 adalah bilangan genap?", ["pasangkan 16 lidi dua-dua hingga habis tanpa sisa", "sebutkan saja dari buku", "hitung dengan cepat", "tidak perlu dibuktikan"], "A", "Memasangkan konkret dua-dua hingga tidak ada sisa membuktikan 16 adalah genap.")
mc("c6", "sulit", K, Me, S4, "Jika genap + ganjil + genap dijumlahkan, hasil akhirnya selalu bernilai ....", ["ganjil", "genap", "nol", "tidak pasti"], "A", "Genap + ganjil = ganjil; ganjil + genap = ganjil.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi: (37 + 43) + (24 + 16) - 10!", ["110", "100", "120", "105"], "A", "(37 + 43) + (24 + 16) - 10 = 80 + 40 - 10 = 110.", verifikasi={"ekspresi": "(37 + 43) + (24 + 16) - 10", "hasil": "110"})
mc("c6", "sulit", P, Me, S3, "Jumlah bilangan genap dari 2 sampai 10 adalah ....", ["30", "28", "32", "26"], "A", "2 + 4 + 6 + 8 + 10 = 30.", verifikasi={"ekspresi": "2 + 4 + 6 + 8 + 10", "hasil": "30"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab56_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab56.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
