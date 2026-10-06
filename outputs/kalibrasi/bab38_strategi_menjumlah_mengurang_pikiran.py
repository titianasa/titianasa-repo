#!/usr/bin/env python3
"""
Generator dan validator Bab 38 Matematika Kelas 2 SD:
"Strategi Menjumlah dan Mengurang dalam Pikiran" (Fase A)
bab_id: 5cdea310-4aab-4492-8456-0bda5494d775
article_id: 973bd586-8ff3-44ba-8bd0-8074cbe2466e
quiz_id: 3cf02c4b-108f-4511-a786-43bc93c36935
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a1b2c3d4e501"  # Menjumlah Puluhan Utuh dalam Pikiran
S2 = "b2c3d4e5f602"  # Strategi Menjadikan Puluhan (Make a Ten)
S3 = "c3d4e5f6a703"  # Mengurang Puluhan Utuh dalam Pikiran
S4 = "d4e5f6a7b804"  # Strategi Mengurai Bilangan

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Menjumlah dalam pikiran sangat mudah.
Mari kita lihat puluhan utuh.
Tiga puluh tambah dua puluh.
Tiga tambah dua jadi lima.
Hasilnya adalah lima puluh.
Hitunglah angka puluhannya saja.
Tambahkan angka nol di belakang.
Berhitung cepat jadi sangat mudah.

:::definition
title: Puluhan Utuh
Puluhan utuh berakhiran angka nol.
Contohnya sepuluh dan dua puluh.
:::"""

s2_content = """Bagaimana menjumlahkan bilangan acak?
Gunakan trik menjadikan puluhan.
Misalnya dua puluh delapan tambah lima.
Ambil dua dari lima.
Dua puluh delapan tambah dua jadi tiga puluh.
Sisa lima masih ada tiga.
Tiga puluh tambah tiga jadi tiga puluh tiga.
Pikiran kita bekerja sangat rapi.

:::steps
title: Trik Menjadikan Puluhan
1. Cari angka untuk melengkapi puluhan terdekat.
2. Pecah bilangan penambah.
3. Jumlahkan puluhan dengan sisanya.
:::"""

s3_content = """Kini mari belajar mengurang puluhan.
Tujuh puluh kurang tiga puluh.
Tujuh kurang tiga sama dengan empat.
Jadi hasilnya empat puluh.
Cukup kurangkan angka depannya saja.
Tuliskan angka nol di belakang.
Mudah sekali berhitung dalam kepala!"""

s4_content = """Untuk pengurangan bilangan lain, uraikanlah.
Empat puluh lima kurang tujuh.
Kurangkan lima terlebih dahulu.
Empat puluh lima kurang lima jadi empat puluh.
Lalu kurangkan sisa dua.
Empat puluh kurang dua jadi tiga puluh delapan.
Hebat, kamu pintar berhitung!

:::common_trap
title: Salah Mengurai Pengurangan
Jangan kurangkan angka sembarangan.
Uraikan pengurang agar mencapai puluhan utuh.
Kurangkan sisanya dari puluhan tersebut.
:::

:::callout
variant: summary
title: Ringkasan
text: Hitunglah angka puluhan terlebih dahulu. Jadikan bilangan ke puluhan terdekat. Berhitung dalam pikiran menjadi cepat.
:::"""

sections = [
    {
        "id": S1,
        "title": "Menjumlah Puluhan Utuh dalam Pikiran",
        "minutes": 6,
        "goal": "Siswa mampu menjumlahkan dua bilangan puluhan utuh dalam pikiran secara cepat dan tepat.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Strategi Menjadikan Puluhan Terdekat",
        "minutes": 6,
        "goal": "Siswa mampu menggunakan strategi make-a-ten untuk menyelesaikan penjumlahan mental.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mengurang Puluhan Utuh dalam Pikiran",
        "minutes": 6,
        "goal": "Siswa mampu mengurangkan bilangan puluhan utuh dalam kepala dengan mengurangkan nilai puluhannya.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Strategi Mengurai Bilangan pada Pengurangan",
        "minutes": 6,
        "goal": "Siswa mampu mengurai bilangan pengurang untuk memudahkan pengurangan mental secara terstruktur.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Strategi Menjumlah dan Mengurang dalam Pikiran",
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
# 2. DEFINISI BANK 50 SOAL BAB 38
# ==========================================
D, T, X = "diagnostik", "latihan_terarah", "latihan_mandiri"
K, R, P = "checkpoint_akhir", "remedial", "pengayaan"
F, Kn, Pr, Me = "faktual", "konseptual", "prosedural", "metakognitif"

Q = []

def mc(b, d, f, dim, s, stem, opts, ans, ex, m=None, verifikasi=None):
    Q.append(dict(t="mc", b=b, d=d, f=f, dim=dim, s=s, stem=stem, opts=opts, ans=ans, ex=ex, m=m, verifikasi=verifikasi))

def tf(b, d, f, dim, s, text, ans, ex, verifikasi=None):
    Q.append(dict(t="tf", b=b, d=d, f=f, dim=dim, s=s, stem=text, ans=ans, ex=ex, verifikasi=verifikasi))

def sa(b, d, f, dim, s, stem, ans, ex, verifikasi=None):
    Q.append(dict(t="sa", b=b, d=d, f=f, dim=dim, s=s, stem=stem, ans=ans, ex=ex, verifikasi=verifikasi))

# ── C1 MUDAH (5 soal: 2 diagnostik, 3 terarah) ─────────────────────────────
# Diagnostik (2)
mc("c1", "mudah", D, F, S1, "Berapakah hasil dari 20 ditambah 30?", ["50", "40", "60", "70"], "A", "2 puluhan + 3 puluhan = 5 puluhan (50).", verifikasi={"ekspresi": "20 + 30", "hasil": "50"})
tf("c1", "mudah", D, F, S3, "Hasil dari 50 dikurang 20 adalah 40.", "Salah", "50 - 20 = 30, bukan 40.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Berapakah hasil penjumlahan 40 ditambah 10?", ["50", "40", "60", "30"], "A", "40 + 10 = 50.", verifikasi={"ekspresi": "40 + 10", "hasil": "50"})
mc("c1", "mudah", T, F, S3, "Berapakah hasil dari 60 dikurang 20?", ["40", "30", "50", "20"], "A", "6 puluhan - 2 puluhan = 4 puluhan (40).", verifikasi={"ekspresi": "60 - 20", "hasil": "40"})
sa("c1", "mudah", T, F, S1, "Berapakah hasil dari 10 ditambah 70?", "80", "10 + 70 = 80.", verifikasi={"ekspresi": "10 + 70", "hasil": "80"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Agar 27 menjadi 30, kita perlu menambahkan angka ....", ["3", "2", "4", "5"], "A", "30 - 27 = 3.", "Keliru menentukan pelengkap ke puluhan terdekat", verifikasi={"ekspresi": "30 - 27", "hasil": "3"})
tf("c2", "mudah", D, Kn, S4, "Mengurangkan 42 dengan 5 lebih mudah jika 5 diurai menjadi 2 dan 3.", "Benar", "42 - 2 = 40, lalu 40 - 3 = 37.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Mengapa 30 + 50 hasilnya 80?", ["karena 3 puluhan ditambah 5 puluhan adalah 8 puluhan", "karena 3 + 5 = 7", "karena angka nol dijumlahkan", "karena ada puluhan"], "A", "Nilai tempat puluhan: 3 + 5 = 8 puluhan (80).", "Lupa konsep nilai tempat puluhan")
mc("c2", "mudah", R, Kn, S3, "Berapakah hasil dari 80 dikurang 30?", ["50", "40", "60", "30"], "A", "8 puluhan - 3 puluhan = 5 puluhan (50).", "Salah mengurangkan puluhan utuh", verifikasi={"ekspresi": "80 - 30", "hasil": "50"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S2, "Bilangan 38 paling dekat menuju puluhan utuh ....", ["40", "30", "50", "20"], "A", "38 hanya butuh 2 angka menuju 40.")
mc("c2", "mudah", T, Kn, S4, "Untuk menghitung 53 - 6, kita kurangkan 53 dengan angka berapa dulu?", ["3", "4", "5", "6"], "A", "Kurangkan 3 dulu agar menjadi 50, baru kurangkan sisa 3.")
tf("c2", "mudah", T, Kn, S1, "Menjumlahkan 40 + 40 dalam pikiran menghasilkan 70.", "Salah", "40 + 40 = 80, bukan 70.")
sa("c2", "mudah", T, Kn, S3, "Berapakah hasil dari 90 dikurang 40?", "50", "90 - 40 = 50.", verifikasi={"ekspresi": "90 - 40", "hasil": "50"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Berapakah hasil dari 29 ditambah 6 dengan strategi puluhan?", ["35", "34", "36", "33"], "A", "29 + 1 = 30; 30 + 5 = 35.", "Keliru memecah bilangan penambah", verifikasi={"ekspresi": "29 + 6", "hasil": "35"})
mc("c3", "sedang", R, Pr, S4, "Berapakah hasil dari 34 dikurang 7?", ["27", "26", "28", "25"], "A", "34 - 4 = 30; 30 - 3 = 27.", "Salah mengurai bilangan pengurang", verifikasi={"ekspresi": "34 - 7", "hasil": "27"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berapakah hasil dari 50 ditambah 40?", ["90", "80", "100", "70"], "A", "50 + 40 = 90.", verifikasi={"ekspresi": "50 + 40", "hasil": "90"})
mc("c3", "mudah", T, Pr, S3, "Berapakah hasil dari 70 dikurang 50?", ["20", "30", "10", "40"], "A", "70 - 50 = 20.", verifikasi={"ekspresi": "70 - 50", "hasil": "20"})
tf("c3", "sedang", T, Pr, S2, "Hasil dari 18 ditambah 7 adalah 25.", "Benar", "18 + 2 = 20; 20 + 5 = 25.")
mc("c3", "sedang", T, Pr, S4, "Berapakah hasil dari 52 dikurang 6?", ["46", "47", "45", "48"], "A", "52 - 2 = 50; 50 - 4 = 46.", verifikasi={"ekspresi": "52 - 6", "hasil": "46"})
tf("c3", "sedang", T, Pr, S1, "Hasil dari 30 ditambah 60 sama dengan 80.", "Salah", "30 + 60 = 90, bukan 80.")
sa("c3", "sedang", T, Pr, S2, "Berapakah hasil dari 48 ditambah 5?", "53", "48 + 2 = 50; 50 + 3 = 53.", verifikasi={"ekspresi": "48 + 5", "hasil": "53"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Berapakah hasil dari 20 ditambah 60?", ["80", "70", "90", "60"], "A", "20 + 60 = 80.", verifikasi={"ekspresi": "20 + 60", "hasil": "80"})
mc("c3", "sedang", X, Pr, S2, "Berapakah hasil dari 37 ditambah 8?", ["45", "44", "46", "43"], "A", "37 + 3 = 40; 40 + 5 = 45.", verifikasi={"ekspresi": "37 + 8", "hasil": "45"})
tf("c3", "sedang", X, Pr, S3, "Hasil dari 80 dikurang 60 sama dengan 20.", "Benar", "80 - 60 = 20.")
sa("c3", "sedang", X, Pr, S4, "Berapakah hasil dari 63 dikurang 5?", "58", "63 - 3 = 60; 60 - 2 = 58.", verifikasi={"ekspresi": "63 - 5", "hasil": "58"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Berapakah hasil dari 50 ditambah 50?", ["100", "90", "80", "70"], "A", "50 + 50 = 100.", verifikasi={"ekspresi": "50 + 50", "hasil": "100"})
mc("c3", "sedang", K, Pr, S3, "Berapakah hasil dari 100 dikurang 40?", ["60", "50", "70", "40"], "A", "100 - 40 = 60.", verifikasi={"ekspresi": "100 - 40", "hasil": "60"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Jika 40 + A = 90, maka berapakah nilai A?", ["50", "40", "60", "30"], "A", "90 - 40 = 50.", verifikasi={"ekspresi": "90 - 40", "hasil": "50"})
mc("c4", "sedang", T, Kn, S2, "Untuk menjumlahkan 57 + 8, langkah pertama yang paling efisien adalah ....", ["memecah 8 menjadi 3 dan 5", "menghitung jari dari 1", "menggambar 57 lingkaran", "mengurangi 57"], "A", "57 + 3 = 60, lalu 60 + 5 = 65.")
tf("c4", "sedang", T, Kn, S3, "Selisih antara 90 dan 30 sama dengan hasil 40 + 20.", "Benar", "90 - 30 = 60, dan 40 + 20 = 60. Keduanya sama.")
tf("c4", "sedang", T, Kn, S4, "Hasil dari 71 dikurang 4 sama dengan 68.", "Salah", "71 - 1 = 70; 70 - 3 = 67, bukan 68.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari 82 dikurang 6?", "76", "82 - 2 = 80; 80 - 4 = 76.", verifikasi={"ekspresi": "82 - 6", "hasil": "76"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Sebuah bus membawa 30 penumpang, lalu naik 40 orang lagi. Jumlah seluruhnya?", ["70 orang", "60 orang", "80 orang", "50 orang"], "A", "30 + 40 = 70 orang.", verifikasi={"ekspresi": "30 + 40", "hasil": "70"})
mc("c4", "sedang", X, Kn, S2, "Siti punya 46 pita, diberi ibu 7 pita. Berapa pita Siti sekarang?", ["53 pita", "52 pita", "54 pita", "51 pita"], "A", "46 + 4 = 50; 50 + 3 = 53 pita.", verifikasi={"ekspresi": "46 + 7", "hasil": "53"})
tf("c4", "sedang", X, Kn, S3, "Pengurangan 90 - 70 bernilai lebih besar daripada 80 - 50.", "Salah", "90 - 70 = 20, sedangkan 80 - 50 = 30. 20 lebih kecil dari 30.")
mc("c4", "sulit", X, Me, S4, "Beni punya 65 kelereng, hilang 8 butir. Berapa sisa kelereng Beni?", ["57 butir", "56 butir", "58 butir", "55 butir"], "A", "65 - 5 = 60; 60 - 3 = 57 butir.", verifikasi={"ekspresi": "65 - 8", "hasil": "57"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Edo punya 50 kelereng merah dan 30 kelereng biru. Berapa total kelereng Edo?", ["80 kelereng", "70 kelereng", "90 kelereng", "60 kelereng"], "A", "50 + 30 = 80 kelereng.", verifikasi={"ekspresi": "50 + 30", "hasil": "80"})
mc("c4", "sulit", K, Me, S2, "Berapakah hasil dari 68 ditambah 7?", ["75", "74", "76", "73"], "A", "68 + 2 = 70; 70 + 5 = 75.", verifikasi={"ekspresi": "68 + 7", "hasil": "75"})
tf("c4", "sulit", K, Me, S3, "Nilai dari 100 - 30 lebih banyak 20 daripada 50.", "Benar", "100 - 30 = 70; 70 - 50 = 20.")
mc("c4", "sulit", K, Me, S4, "Toko punya 73 roti, terjual 9 roti. Berapa sisa roti di toko?", ["64 roti", "63 roti", "65 roti", "62 roti"], "A", "73 - 3 = 70; 70 - 6 = 64 roti.", verifikasi={"ekspresi": "73 - 9", "hasil": "64"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Manakah dari pasangan penjumlahan berikut yang menghasilkan 90?", ["30 + 60", "40 + 40", "20 + 50", "10 + 70"], "A", "30 + 60 = 90.")
mc("c5", "sedang", T, Me, S2, "Jika 56 + N = 63, berapakah nilai bilangan N?", ["7", "6", "8", "9"], "A", "63 - 56 = 7.", verifikasi={"ekspresi": "63 - 56", "hasil": "7"})
mc("c5", "sedang", T, Me, S3, "Budi punya uang 80 rupiah, dibelikan permen 30 rupiah. Berapa sisa uang Budi?", ["50 rupiah", "40 rupiah", "60 rupiah", "30 rupiah"], "A", "80 - 30 = 50 rupiah.", verifikasi={"ekspresi": "80 - 30", "hasil": "50"})
mc("c5", "sulit", T, Me, S4, "Jika 84 - M = 77, berapakah nilai bilangan M?", ["7", "8", "6", "9"], "A", "84 - 77 = 7.", verifikasi={"ekspresi": "84 - 77", "hasil": "7"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Berapakah hasil dari 78 ditambah 8?", ["86", "85", "87", "84"], "A", "78 + 2 = 80; 80 + 6 = 86.", verifikasi={"ekspresi": "78 + 8", "hasil": "86"})
mc("c5", "sulit", K, Me, S3, "Ada 90 buku: 40 komik, sisanya dongeng. Berapa banyak buku dongeng?", ["50 buku", "40 buku", "60 buku", "30 buku"], "A", "90 - 40 = 50 buku dongeng.", verifikasi={"ekspresi": "90 - 40", "hasil": "50"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Dodi menghitung 47 + 6 dengan cara 47 + 3 + 3. Bagaimana penilaianmu?", ["sangat tepat karena memecah 6 untuk melengkapi 50", "salah total", "terlalu rumit", "hasilnya salah"], "A", "47 + 3 = 50; 50 + 3 = 53 adalah strategi mental math yang sangat baik.")
mc("c6", "sulit", K, Me, S4, "Lina menghitung 62 - 5 dengan 62 - 2 - 3. Mengapa cara Lina benar?", ["karena 62 dikurang 2 jadi puluhan utuh 60 lalu dikurang 3 jadi 57", "karena 2 + 3 = 6", "karena hasilnya selalu nol", "karena tidak perlu berhitung"], "A", "Mengurai pengurang menuju puluhan utuh memudahkan perhitungan mental.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Berapakah hasil dari 20 + 30 + 40 dalam pikiran?", ["90", "80", "100", "70"], "A", "20 + 30 = 50; 50 + 40 = 90.", verifikasi={"ekspresi": "20 + 30 + 40", "hasil": "90"})
mc("c6", "sulit", P, Me, S4, "Berapakah hasil dari 95 dikurang 7 dikurang 5?", ["83", "82", "84", "81"], "A", "95 - 5 = 90; 90 - 7 = 83.", verifikasi={"ekspresi": "95 - 7 - 5", "hasil": "83"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab38_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab38.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
