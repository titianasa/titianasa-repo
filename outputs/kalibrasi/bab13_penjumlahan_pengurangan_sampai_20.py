#!/usr/bin/env python3
"""
Generator dan validator Bab 13 Matematika Kelas 1 SD:
"Penjumlahan dan Pengurangan sampai 20" (Fase A)
bab_id: 6d8939a2-4df6-44ed-b18a-dca7a04726e6
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "c9d8e77f0a89"  # Menjumlahkan dengan Menyimpan Puluhan (11-20)
S2 = "d0e9f88a1b90"  # Mengurangkan dari Bilangan Belasan
S3 = "e1f0a99b2c01"  # Hubungan Penjumlahan dan Pengurangan (Keluarga Fakta)
S4 = "f2a1b00c3d12"  # Menghitung Maju dan Menghitung Mundur

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Kita menjumlahkan bilangan sampai 20.
Jadikan kelompok sepuluh terlebih dahulu.
Contohnya delapan ditambah lima.
Ambil 2 dari 5 untuk angka 8.
Delapan dan dua menjadi 10.
Sisa 3 digabung dengan 10.
Sepuluh dan tiga menjadi 13.
Maka $8 + 5 = 13$.

:::steps
title: Menjumlahkan Lewat Sepuluh
1. Lengkapi bilangan pertama jadi 10.
2. Ambil sisanya dari bilangan kedua.
3. Gabungkan 10 dengan bilangan sisa.
:::"""

s2_content = """Mengurangkan bilangan belasan juga mudah.
Contohnya 15 dikurang 4.
Kurangkan dulu angka satuannya.
Lima dikurang empat sama dengan 1.
Lalu gabungkan dengan satu puluhan.
Sepuluh dan satu menjadi 11.
Maka $15 - 4 = 11$.
Berlatihlah teliti melihat nilai tempat.

:::definition
title: Pengurangan Belasan
Pengurangan belasan dapat dilakukan dengan mengurangkan satuannya terlebih dahulu.
:::"""

s3_content = """Penjumlahan dan pengurangan saling berhubungan.
Mereka adalah keluarga fakta hitung.
Jika $7 + 5 = 12$,
maka $12 - 5 = 7$,
dan $12 - 7 = 5$.
Tiga bilangan ini saling bersahabat.
Mengetahui penjumlahan membantu menghitung pengurangan.
Satu fakta memberi banyak jawaban."""

s4_content = """Gunakan garis bilangan untuk berhitung.
Menjumlahkan artinya melompat maju ke kanan.
Mengurangkan artinya melompat mundur ke kiri.
Mulai dari 12 melompat maju 3.
Tiba pada bilangan 15.
Mulai dari 16 melompat mundur 4.
Tiba pada bilangan 12.

:::common_trap
title: Salah Arah Lompatan pada Garis Bilangan
Menambah harus melompat maju ke kanan.
Mengurang harus melompat mundur ke kiri.
Jangan sampai terbalik arah lompatan.
:::

:::callout
variant: summary
title: Ringkasan
text: Hitung sampai 20 dengan kelompok 10. Tambah melompat maju, kurang melompat mundur.
:::"""

sections = [
    {
        "id": S1,
        "title": "Menjumlahkan sampai 20 lewat Sepuluh",
        "minutes": 6,
        "goal": "Siswa dapat menjumlahkan dua bilangan dengan hasil 11 sampai 20 menggunakan strategi membuat sepuluh.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengurangkan Bilangan Belasan",
        "minutes": 6,
        "goal": "Siswa dapat mengurangkan bilangan satu angka dari bilangan belasan tanpa atau dengan meminjam.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Hubungan Penjumlahan dan Pengurangan",
        "minutes": 6,
        "goal": "Siswa dapat memahami keterkaitan timbal balik antara penjumlahan dan pengurangan (keluarga fakta).",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menghitung Maju dan Mundur sampai 20",
        "minutes": 6,
        "goal": "Siswa dapat menggunakan strategi hitung maju untuk penjumlahan dan hitung mundur untuk pengurangan.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Penjumlahan dan Pengurangan sampai 20",
    "topic": "Penjumlahan dan Pengurangan sampai 20",
    "level": "Kelas 1 SD · Fase A",
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
# 2. DEFINISI BANK 50 SOAL BAB 13
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
mc("c1", "mudah", D, F, S4, "Pada garis bilangan, menjumlahkan artinya melompat ke arah ....", ["kanan", "kiri", "bawah", "atas"], "A", "Menjumlahkan artinya melompat maju ke arah kanan.")
tf("c1", "mudah", D, F, S4, "Melompat mundur ke kiri digunakan untuk operasi pengurangan.", "Benar", "Mengurang artinya melompat mundur ke kiri pada garis bilangan.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Sepuluh ditambah empat menghasilkan bilangan ....", ["14", "13", "15", "12"], "A", "10 + 4 = 14.", verifikasi={"ekspresi": "10 + 4", "hasil": "14"})
mc("c1", "mudah", T, F, S2, "Angka satuan dari bilangan 17 adalah ....", ["7", "1", "10", "17"], "A", "Pada 17, angka 1 puluhan dan 7 satuan.")
sa("c1", "mudah", T, F, S3, "Berapakah hasil dari 10 ditambah 8?", "18", "10 + 8 = 18.", verifikasi={"ekspresi": "10 + 8", "hasil": "18"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Berapakah hasil dari $9 + 3$?", ["12", "11", "13", "14"], "A", "9 + 3 = 12.", verifikasi={"ekspresi": "9 + 3", "hasil": "12"})
tf("c2", "mudah", D, Kn, S3, "Jika $6 + 4 = 10$, maka $10 - 4 = 6$.", "Benar", "Penjumlahan dan pengurangan berhubungan erat sebagai keluarga fakta.")

# Remedial (2)
mc("c2", "mudah", R, F, S4, "Dari angka 12 melompat maju 3 langkah tiba di ....", ["15", "14", "16", "9"], "A", "12 + 3 = 15.", "Salah menentukan langkah hitung maju", verifikasi={"ekspresi": "12 + 3", "hasil": "15"})
mc("c2", "mudah", R, Kn, S2, "Berapakah hasil dari $16 - 4$?", ["12", "11", "13", "10"], "A", "6 - 4 = 2, sehingga 16 - 4 = 12.", "Salah mengurangkan satuan pada belasan", verifikasi={"ekspresi": "16 - 4", "hasil": "12"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Berapakah hasil dari $8 + 4$?", ["12", "11", "13", "14"], "A", "8 + 4 = 12.", verifikasi={"ekspresi": "8 + 4", "hasil": "12"})
mc("c2", "mudah", T, Kn, S2, "Berapakah hasil dari $14 - 3$?", ["11", "10", "12", "13"], "A", "14 - 3 = 11.", verifikasi={"ekspresi": "14 - 3", "hasil": "11"})
tf("c2", "mudah", T, Kn, S3, "Operasi $15 - 5$ menghasilkan bilangan 11.", "Salah", "15 - 5 = 10, bukan 11.")
sa("c2", "mudah", T, Kn, S4, "Dari 18 melompat mundur 2 langkah tiba di angka?", "16", "18 - 2 = 16.", verifikasi={"ekspresi": "18 - 2", "hasil": "16"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Berapakah hasil penjumlahan dari $7 + 6$?", ["13", "12", "14", "11"], "A", "7 + 6 = 13.", "Salah menjumlahkan bilangan melewati 10", verifikasi={"ekspresi": "7 + 6", "hasil": "13"})
mc("c3", "sedang", R, Pr, S2, "Hasil pengurangan dari $13 - 5$ adalah ....", ["8", "7", "9", "6"], "A", "13 - 5 = 8.", "Salah menghitung pengurangan belasan", verifikasi={"ekspresi": "13 - 5", "hasil": "8"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berapakah hasil dari $11 + 5$?", ["16", "15", "17", "14"], "A", "11 + 5 = 16.", verifikasi={"ekspresi": "11 + 5", "hasil": "16"})
mc("c3", "sedang", T, Pr, S2, "Berapakah hasil dari $17 - 5$?", ["12", "11", "13", "10"], "A", "17 - 5 = 12.", verifikasi={"ekspresi": "17 - 5", "hasil": "12"})
tf("c3", "sedang", T, Pr, S3, "Jika $8 + 7 = 15$, maka $15 - 8 = 7$.", "Benar", "15 - 8 = 7 adalah pasangan fakta.")
mc("c3", "sedang", T, Pr, S4, "Mulai dari 11, melompat maju 4 langkah tiba di ....", ["15", "14", "16", "13"], "A", "11 + 4 = 15.", verifikasi={"ekspresi": "11 + 4", "hasil": "15"})
tf("c3", "sedang", T, Pr, S1, "Hasil penjumlahan dari $9 + 5$ adalah 15.", "Salah", "9 + 5 = 14, bukan 15.")
sa("c3", "mudah", T, Pr, S2, "Berapakah sisa dari $19 - 7$?", "12", "19 - 7 = 12.", verifikasi={"ekspresi": "19 - 7", "hasil": "12"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Berapakah hasil dari $8 + 6$?", ["14", "13", "15", "12"], "A", "8 + 6 = 14.", verifikasi={"ekspresi": "8 + 6", "hasil": "14"})
mc("c3", "sedang", X, Pr, S2, "Berapakah hasil dari $18 - 6$?", ["12", "11", "13", "14"], "A", "18 - 6 = 12.", verifikasi={"ekspresi": "18 - 6", "hasil": "12"})
tf("c3", "sedang", X, Pr, S3, "Keluarga fakta dari 9, 4, 13 memiliki $13 - 9 = 5$.", "Salah", "13 - 9 = 4, bukan 5.")
sa("c3", "sedang", X, Pr, S4, "Dari angka 20 melompat mundur 5 langkah tiba di angka?", "15", "20 - 5 = 15.", verifikasi={"ekspresi": "20 - 5", "hasil": "15"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Berapakah hasil dari $9 + 7$?", ["16", "15", "17", "14"], "A", "9 + 7 = 16.", verifikasi={"ekspresi": "9 + 7", "hasil": "16"})
mc("c3", "sedang", K, Pr, S2, "Hasil dari $16 - 7$ adalah ....", ["9", "8", "10", "7"], "A", "16 - 7 = 9.", verifikasi={"ekspresi": "16 - 7", "hasil": "9"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Penjumlahan manakah yang hasilnya sama dengan $8 + 7$?", ["$9 + 6$", "$8 + 6$", "$7 + 7$", "$9 + 5$"], "A", "8 + 7 = 15 dan 9 + 6 = 15.")
mc("c4", "sedang", T, Kn, S2, "Pengurangan manakah yang hasilnya sama dengan $15 - 6$?", ["$16 - 7$", "$14 - 6$", "$13 - 5$", "$15 - 5$"], "A", "15 - 6 = 9 dan 16 - 7 = 9.")
tf("c4", "sedang", T, Kn, S3, "Bilangan 6, 8, dan 14 membentuk keluarga fakta penjumlahan.", "Benar", "6 + 8 = 14 dan 14 - 6 = 8.")
tf("c4", "sedang", T, Kn, S4, "Melompat maju 5 lalu mundur 2 sama dengan melompat maju 3.", "Benar", "5 - 2 = 3 langkah maju.")
sa("c4", "sedang", T, Kn, S4, "Berapa langkah mundur dari 17 agar tiba di 11?", "6", "17 - 11 = 6.", verifikasi={"ekspresi": "17 - 11", "hasil": "6"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Manakah yang menghasilkan jumlah paling besar?", ["$9 + 9$", "$8 + 9$", "$7 + 9$", "$6 + 9$"], "A", "9 + 9 = 18, paling besar.")
mc("c4", "sedang", X, Kn, S2, "Operasi $17 - 8$ dan $18 - 9$ memiliki ....", ["hasil yang sama", "hasil berbeda", "angka sama", "simbol berbeda"], "A", "Keduanya menghasilkan 9.")
tf("c4", "sedang", X, Kn, S4, "Dari angka 14 melompat mundur 4 langkah tiba di angka 11.", "Salah", "14 - 4 = 10, bukan 11.")
mc("c4", "sulit", X, Me, S1, "Bila $A + A = 16$, berapakah nilai A?", ["8", "7", "9", "6"], "A", "8 + 8 = 16.", verifikasi={"ekspresi": "16 // 2", "hasil": "8"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Operasi $12 + 6$ memiliki hasil yang sama dengan ....", ["$10 + 8$", "$11 + 6$", "$9 + 8$", "$13 + 4$"], "A", "12 + 6 = 18 dan 10 + 8 = 18.")
mc("c4", "sulit", K, Me, S2, "Jika $20 - C = 13$, berapakah nilai C?", ["7", "6", "8", "5"], "A", "20 - 7 = 13.", verifikasi={"ekspresi": "20 - 13", "hasil": "7"})
tf("c4", "sulit", K, Me, S3, "Pengurangan $14 - 8$ menghasilkan bilangan yang sama dengan $15 - 8$.", "Salah", "14 - 8 = 6 sedangkan 15 - 8 = 7.")
mc("c4", "sulit", K, Me, S4, "Dari 13 melompat maju berapa langkah agar tiba di 19?", ["6", "5", "7", "8"], "A", "19 - 13 = 6 langkah.", verifikasi={"ekspresi": "19 - 13", "hasil": "6"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Dina punya 8 pita. Ibu memberi beberapa hingga jadi 15. Berapa diberi?", ["7 pita", "6 pita", "8 pita", "5 pita"], "A", "15 - 8 = 7 pita.", verifikasi={"ekspresi": "15 - 8", "hasil": "7"})
mc("c5", "sedang", T, Me, S2, "Toko punya 16 roti terjual hingga sisa 9 roti. Berapa terjual?", ["7 roti", "6 roti", "8 roti", "5 roti"], "A", "16 - 9 = 7 roti.", verifikasi={"ekspresi": "16 - 9", "hasil": "7"})
mc("c5", "sedang", T, Me, S3, "Bagaimana cara memeriksa apakah $13 - 6 = 7$ sudah benar?", ["menghitung $7 + 6 = 13$", "menghitung $13 + 6$", "menghitung $13 - 7$", "menghitung $7 - 6$"], "A", "Penjumlahan 7 + 6 = 13 membuktikan kebenaran 13 - 6 = 7.")
mc("c5", "sulit", T, Me, S4, "Katak di titik 9 ingin ke titik 17. Apa lompatan katak?", ["maju 8 langkah", "mundur 8 langkah", "maju 7 langkah", "maju 9 langkah"], "A", "17 - 9 = 8 langkah maju.", verifikasi={"ekspresi": "17 - 9", "hasil": "8"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Di bus ada 12 penumpang lalu naik 7 orang. Berapa total penumpang?", ["19 orang", "18 orang", "20 orang", "17 orang"], "A", "12 + 7 = 19 orang.", verifikasi={"ekspresi": "12 + 7", "hasil": "19"})
mc("c5", "sulit", K, Me, S4, "Bila dari angka 18 melompat mundur 5 lalu mundur 3, tiba di?", ["10", "11", "9", "12"], "A", "18 - 5 - 3 = 10.", verifikasi={"ekspresi": "18 - 5 - 3", "hasil": "10"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Susunlah penjumlahan dua bilangan satu angka yang menghasilkan 17!", ["$9 + 8$", "$9 + 7$", "$8 + 8$", "$9 + 9$"], "A", "9 + 8 = 17.")
mc("c6", "sulit", K, Me, S3, "Buatlah keluarga fakta dari bilangan 7, 9, dan 16 yang benar!", ["$16 - 9 = 7$", "$16 - 8 = 8$", "$16 - 7 = 8$", "$9 - 7 = 2$"], "A", "16 - 9 = 7 adalah fakta yang tepat.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Rancanglah tiga bilangan berbeda yang jika dijumlahkan menghasilkan 18!", ["$5 + 6 + 7$", "$4 + 6 + 7$", "$5 + 5 + 8$", "$6 + 6 + 6$"], "A", "5 + 6 + 7 = 18 dan ketiganya berbeda.")
mc("c6", "sulit", P, Me, S4, "Susunlah lompatan dari 20 mundur ke 12 dengan dua langkah sama!", ["mundur 4 langkah dua kali", "mundur 3 langkah dua kali", "mundur 5 langkah dua kali", "mundur 2 langkah dua kali"], "A", "20 - 4 - 4 = 12.")

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab13_soal_{idx+1}"))
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
    "level": "Fase A - Kelas 1 SD",
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab13.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
