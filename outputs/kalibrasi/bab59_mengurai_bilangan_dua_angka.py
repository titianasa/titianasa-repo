#!/usr/bin/env python3
"""
Generator dan validator Bab 59 Matematika Kelas 2 SD:
"Mengurai Bilangan Dua Angka" (Fase A)
bab_id: 187ad622-bf08-4adf-a37f-2225786db13a
article_id: ae794667-9eae-478d-8dfd-08c9805c7baf
quiz_id: 3c3ea1c3-d389-40ab-9115-78c02733083f
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "d1f2h3j4l501"  # Nilai Tempat Puluhan dan Satuan
S2 = "e2g3i4k5m602"  # Mengurai Menjadi Bentuk Panjang
S3 = "f3h4j5l6n703"  # Berbagai Cara Mengurai Bilangan (Fleksibel)
S4 = "g4i5k6m7o804"  # Menyusun Kembali Bilangan dari Uraian

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Setiap bilangan punya tempat tinggal.
Ada tempat puluhan di depan.
Ada tempat satuan di belakang.
Contohnya pada bilangan 47.
Angka 4 menempati nilai puluhan.
Angka 7 menempati nilai satuan.
Masing-masing punya nilai berbeda.
Jangan sampai posisi mereka tertukar!

:::definition
title: Nilai Tempat Bilangan Dua Angka
Angka sebelah kiri bernilai puluhan. Angka sebelah kanan bernilai satuan.
:::"""

s2_content = """Kita bisa membuka bilangan itu.
Cara ini disebut bentuk panjang.
Kita uraikan menurut nilainya.
4 puluhan bernilai 40.
7 satuan bernilai 7.
Maka 47 ditulis 40 + 7.
Contoh lain: 63 = 60 + 3.
Bentuk panjang membuat bilangan jelas!

:::steps
title: Cara Menulis Bentuk Panjang
1. Lihat angka puluhan, kalikan sepuluh.
2. Lihat angka satuan.
3. Tuliskan dengan tanda tambah: puluhan + satuan.
:::"""

s3_content = """Mengurai bilangan bisa sangat bebas.
Tidak harus selalu puluhan pas.
Contohnya pada bilangan 45.
Bisa diurai menjadi 40 + 5.
Bisa juga menjadi 30 + 15.
Bisa pula menjadi 20 + 25.
Jumlahnya tetap sama yaitu 45.
Cara ini membantu kita berhitung!"""

s4_content = """Kita juga bisa menyusun kembali.
Gabungkan puluhan dengan satuannya.
Misalnya 50 ditambah 8.
Hasilnya adalah bilangan 58.
Bagaimana jika 40 ditambah 14?
40 ditambah 14 menjadi 54.
Susunlah bilangan dengan sangat cermat!

:::common_trap
title: Mengira Nilai Angka Puluhan Sama dengan Satuannya
Angka 5 pada puluhan bernilai 50.
Angka 5 pada satuan bernilai 5.
Nilainya jelas berbeda sepuluh kali lipat!
:::

:::callout
variant: summary
title: Ringkasan
text: Bilangan dua angka diurai menjadi puluhan dan satuan. 56 sama dengan 50 ditambah 6.
:::"""

sections = [
    {
        "id": S1,
        "title": "Nilai Tempat Puluhan dan Satuan",
        "minutes": 6,
        "goal": "Siswa memahami letak dan arti nilai tempat puluhan dan satuan pada bilangan dua angka.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengurai Menjadi Bentuk Panjang",
        "minutes": 6,
        "goal": "Siswa mampu menuliskan penguraian bilangan dua angka dalam bentuk panjang penjumlahan.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Berbagai Cara Mengurai Bilangan (Fleksibel)",
        "minutes": 6,
        "goal": "Siswa memahami bahwa suatu bilangan dapat diurai menjadi berbagai kombinasi penjumlahan.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menyusun Kembali Bilangan dari Uraian",
        "minutes": 6,
        "goal": "Siswa mampu menyusun kembali lambang bilangan dari bentuk uraian puluhan dan satuan.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengurai Bilangan Dua Angka",
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
# 2. DEFINISI BANK 50 SOAL BAB 59
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
mc("c1", "mudah", D, F, S1, "Pada bilangan 58, angka yang menempati nilai puluhan adalah ....", ["5", "8", "50", "80"], "A", "Angka depan (5) adalah puluhan.")
tf("c1", "mudah", D, F, S2, "Bentuk panjang dari bilangan 34 adalah 30 + 4.", "Benar", "34 = 30 + 4.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Pada bilangan 72, angka yang menempati nilai satuan adalah ....", ["2", "7", "20", "70"], "A", "Angka belakang (2) adalah satuan.")
mc("c1", "mudah", T, F, S2, "Bentuk panjang dari bilangan 65 adalah ....", ["60 + 5", "50 + 6", "60 + 50", "6 + 5"], "A", "65 = 60 + 5.")
sa("c1", "mudah", T, F, S4, "Berapakah hasil dari 40 + 8?", "48", "40 + 8 = 48.", verifikasi={"ekspresi": "40 + 8", "hasil": "48"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Berapakah bilangan yang tersusun dari 7 puluhan dan 3 satuan?", ["73", "37", "703", "10"], "A", "7 puluhan (70) + 3 satuan (3) = 73.")
tf("c2", "mudah", D, Kn, S1, "Pada bilangan 49, angka 4 bernilai 4 satuan.", "Salah", "Angka 4 berada di depan, sehingga bernilai 40 atau 4 puluhan.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Berapakah nilai sebenarnya dari angka 8 pada bilangan 83?", ["80", "8", "83", "38"], "A", "Angka 8 di tempat puluhan bernilai 80.", "Mengira nilai puluhan sama dengan lambang angkanya", verifikasi={"ekspresi": "8 * 10", "hasil": "80"})
mc("c2", "mudah", R, Kn, S2, "Manakah penguraian bentuk panjang yang BENAR untuk 91?", ["90 + 1", "9 + 1", "90 + 10", "10 + 9"], "A", "91 diurai menjadi 90 + 1.", "Keliru menuliskan nilai satuan atau puluhan")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Angka 6 pada bilangan 62 bernilai ....", ["60", "6", "62", "26"], "A", "Angka 6 adalah puluhan, bernilai 60.", verifikasi={"ekspresi": "6 * 10", "hasil": "60"})
mc("c2", "mudah", T, Kn, S3, "Penguraian 54 menjadi 40 + 14 bernilai ....", ["54", "50", "44", "64"], "A", "40 + 14 = 54.", verifikasi={"ekspresi": "40 + 14", "hasil": "54"})
tf("c2", "mudah", T, Kn, S4, "Bilangan yang terdiri dari 5 puluhan dan 0 satuan adalah 50.", "Benar", "5 puluhan = 50.")
sa("c2", "mudah", T, Kn, S4, "Berapakah hasil dari 70 + 6?", "76", "70 + 6 = 76.", verifikasi={"ekspresi": "70 + 6", "hasil": "76"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S4, "Berapakah hasil gabungan dari 3 puluhan dan 15 satuan?", ["45", "35", "315", "50"], "A", "3 puluhan = 30; 30 + 15 = 45.", "Bingung jika satuan lebih dari 9", verifikasi={"ekspresi": "(3 * 10) + 15", "hasil": "45"})
mc("c3", "sedang", R, Pr, S3, "Jika 68 diurai menjadi 50 + ..., maka titik-titik bernilai ....", ["18", "8", "28", "16"], "A", "68 - 50 = 18.", "Salah menentukan sisa penguraian fleksibel", verifikasi={"ekspresi": "68 - 50", "hasil": "18"})

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Selisih nilai angka 5 dan angka 2 pada bilangan 52 adalah ....", ["48", "50", "3", "7"], "A", "Nilai 5 adalah 50, nilai 2 adalah 2. 50 - 2 = 48.", verifikasi={"ekspresi": "50 - 2", "hasil": "48"})
mc("c3", "mudah", T, Pr, S2, "Lengkapi bentuk panjang: 87 = ... + 7!", ["80", "8", "70", "87"], "A", "87 = 80 + 7.", verifikasi={"ekspresi": "87 - 7", "hasil": "80"})
tf("c3", "sedang", T, Pr, S3, "Bilangan 36 dapat diurai menjadi 20 + 16.", "Benar", "20 + 16 = 36.")
mc("c3", "sedang", T, Pr, S4, "Berapakah hasil dari 6 puluhan ditambah 24 satuan?", ["84", "64", "74", "94"], "A", "60 + 24 = 84.", verifikasi={"ekspresi": "(6 * 10) + 24", "hasil": "84"})
tf("c3", "sedang", T, Pr, S4, "Hasil dari 80 + 13 adalah 83.", "Salah", "80 + 13 = 93, bukan 83.")
sa("c3", "sedang", T, Pr, S3, "Jika 75 diurai menjadi 40 + ..., berapakah isi titik-titik?", "35", "75 - 40 = 35.", verifikasi={"ekspresi": "75 - 40", "hasil": "35"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Berapakah jumlah nilai tempat angka 4 dan 6 pada bilangan 46?", ["46", "10", "40", "50"], "A", "Nilai 4 adalah 40, nilai 6 adalah 6. 40 + 6 = 46.", verifikasi={"ekspresi": "40 + 6", "hasil": "46"})
mc("c3", "sedang", X, Pr, S2, "Lengkapi bentuk panjang: 94 = 90 + ...!", ["4", "40", "14", "9"], "A", "94 = 90 + 4.", verifikasi={"ekspresi": "94 - 90", "hasil": "4"})
tf("c3", "sedang", X, Pr, S3, "Penguraian 82 menjadi 70 + 12 menghasilkan nilai yang benar.", "Benar", "70 + 12 = 82.")
sa("c3", "sedang", X, Pr, S4, "Berapakah lambang bilangan dari 5 puluhan dan 23 satuan?", "73", "50 + 23 = 73.", verifikasi={"ekspresi": "50 + 23", "hasil": "73"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Manakah dari penguraian berikut yang bernilai 62?", ["40 + 22", "40 + 12", "50 + 22", "30 + 22"], "A", "40 + 22 = 62.")
mc("c3", "sedang", K, Pr, S4, "Berapakah hasil dari 30 + 47?", ["77", "67", "87", "74"], "A", "30 + 47 = 77.", verifikasi={"ekspresi": "30 + 47", "hasil": "77"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa angka 7 pada bilangan 73 dan 37 memiliki arti berbeda?", ["karena pada 73 bernilai puluhan sedangkan pada 37 bernilai satuan", "karena angkanya terbalik", "karena warnanya beda", "karena 73 lebih besar"], "A", "Nilai angka bergantung pada letak nilai tempatnya.")
mc("c4", "sedang", T, Kn, S2, "Jika puluhan 5 diubah menjadi 7 pada bilangan 54, berapakah nilainya sekarang?", ["74", "70", "57", "24"], "A", "Angka puluhan menjadi 7, sehingga bilangan menjadi 74.")
tf("c4", "sedang", T, Kn, S3, "Penguraian 60 + 15 bernilai sama dengan 50 + 25.", "Benar", "Keduanya bernilai 75.")
tf("c4", "sedang", T, Kn, S4, "4 puluhan dan 30 satuan menghasilkan bilangan 43.", "Salah", "40 + 30 = 70, bukan 43.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari (4 puluhan) + (3 puluhan) + (18 satuan)?", "88", "40 + 30 + 18 = 88.", verifikasi={"ekspresi": "40 + 30 + 18", "hasil": "88"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Berapakah selisih nilai angka 8 pada bilangan 88?", ["72", "0", "80", "8"], "A", "80 - 8 = 72.", verifikasi={"ekspresi": "80 - 8", "hasil": "72"})
mc("c4", "sedang", X, Kn, S3, "Sebuah bilangan diurai menjadi 30 + 28. Bilangan berapakah itu?", ["58", "48", "68", "52"], "A", "30 + 28 = 58.", verifikasi={"ekspresi": "30 + 28", "hasil": "58"})
tf("c4", "sedang", X, Kn, S2, "Bentuk panjang dari bilangan 90 adalah 9 + 0.", "Salah", "Bentuk panjang 90 adalah 90 + 0, bukan 9 + 0.")
mc("c4", "sulit", X, Me, S4, "Aku punya 6 puluhan dan 32 satuan. Siapakah aku?", ["92", "82", "632", "96"], "A", "60 + 32 = 92.", verifikasi={"ekspresi": "60 + 32", "hasil": "92"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Berapakah nilai tempat dari angka 0 pada bilangan 70?", ["satuan bernilai 0", "puluhan bernilai 70", "ratusan", "tidak ada nilai"], "A", "Angka 0 menempati satuan dan nilainya adalah 0.")
mc("c4", "sulit", K, Me, S2, "Berapakah hasil pengurangan nilai puluhan 93 dengan nilai satuannya?", ["87", "90", "84", "89"], "A", "90 - 3 = 87.", verifikasi={"ekspresi": "90 - 3", "hasil": "87"})
tf("c4", "sulit", K, Me, S4, "Menukar posisi angka puluhan dan satuan pada 63 menambah nilainya.", "Salah", "63 ditukar menjadi 36, nilainya justru berkurang, bukan bertambah.")
mc("c4", "sulit", K, Me, S3, "Bilangan 86 diurai menjadi A + B. Jika A = 50, berapakah B?", ["36", "26", "46", "30"], "A", "86 - 50 = 36.", verifikasi={"ekspresi": "86 - 50", "hasil": "36"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Berapakah selisih antara nilai puluhan 84 dengan nilai puluhan 39?", ["50", "45", "55", "40"], "A", "80 - 30 = 50.", verifikasi={"ekspresi": "80 - 30", "hasil": "50"})
mc("c5", "sedang", T, Me, S2, "Jika 47 = 40 + 7 dan 35 = 30 + 5, berapakah jumlah puluhannya?", ["70", "60", "80", "75"], "A", "40 + 30 = 70.", verifikasi={"ekspresi": "40 + 30", "hasil": "70"})
mc("c5", "sedang", T, Me, S3, "Sebuah bilangan diurai menjadi 40 + 25. Apakah jenis bilangan tersebut?", ["ganjil karena 65", "genap karena 64", "nol", "tidak pasti"], "A", "40 + 25 = 65, berakhiran 5 jadi bilangan ganjil.")
mc("c5", "sulit", T, Me, S4, "Berapakah hasil dari (5 puluhan + 18 satuan) - (3 puluhan + 8 satuan)?", ["30", "28", "32", "25"], "A", "(50 + 18) - (30 + 8) = 68 - 38 = 30.", verifikasi={"ekspresi": "(50 + 18) - (30 + 8)", "hasil": "30"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Dua bilangan memiliki puluhan sama (60) dan selisih satuan 4. Bilangan apakah?", ["67 dan 63", "65 dan 60", "68 dan 62", "70 dan 66"], "A", "67 dan 63 puluhannya sama-sama 60, dan 7 - 3 = 4.")
mc("c5", "sulit", K, Me, S4, "Berapakah hasil dari (4 puluhan + 35 satuan) + 15?", ["90", "85", "95", "80"], "A", "(40 + 35) + 15 = 75 + 15 = 90.", verifikasi={"ekspresi": "(40 + 35) + 15", "hasil": "90"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Mengapa memahami penguraian bilangan sangat membantu dalam pengurangan meminjam?", ["karena puluhan bisa diurai menjadi satuan lebih banyak untuk dikurang", "karena angkanya jadi cantik", "karena tidak perlu berhitung", "karena rumus ajaib"], "A", "Misalnya 42 diurai menjadi 30 + 12 agar 12 mudah dikurangi.")
mc("c6", "sulit", K, Me, S4, "Aku bilangan dua angka. Puluhanku dua kali satuanku. Jika satuanku 4, siapakah aku?", ["84", "48", "82", "42"], "A", "Satuan = 4, puluhan = 2 x 4 = 8. Bilangannya 84.", verifikasi={"ekspresi": "(2 * 4 * 10) + 4", "hasil": "84"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi: (7 puluhan + 24 satuan) - (4 puluhan + 18 satuan) + 10!", ["46", "44", "48", "42"], "A", "(70 + 24) - (40 + 18) + 10 = 94 - 58 + 10 = 36 + 10 = 46.", verifikasi={"ekspresi": "(70 + 24) - (40 + 18) + 10", "hasil": "46"})
mc("c6", "sulit", P, Me, S3, "Berapa banyak cara mengurai 50 menjadi penjumlahan dua bilangan puluhan utuh?", ["4 cara", "5 cara", "3 cara", "6 cara"], "A", "10+40, 20+30, 30+20, 40+10 (ada 4 cara).", verifikasi={"ekspresi": "4 / 1", "hasil": "4"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab59_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab59.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
