#!/usr/bin/env python3
"""
Generator dan validator Bab 11 Matematika Kelas 1 SD:
"Penjumlahan sampai 10 dengan Benda dan Gambar" (Fase A)
bab_id: 9b187106-abc3-4e26-b561-f8e81bc723c0
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a1b0c99d2e01"  # Menggabungkan Dua Kumpulan Benda
S2 = "b2c1d00e3f12"  # Mengenal Simbol Tambah dan Sama Dengan
S3 = "c3d2e11f4a23"  # Menambah dengan Bilangan Nol
S4 = "d4e3f22a5b34"  # Pasangan Bilangan Menuju 10

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Menjumlahkan artinya menggabungkan benda.
Dua kumpulan benda disatukan.
Ada 3 apel di piring.
Ibu menambah 2 apel lagi.
Semua apel dihitung bersama.
Satu, dua, tiga, empat, lima.
Banyak apel sekarang lima buah.
Kumpulan benda menjadi bertambah banyak.

:::definition
title: Arti Penjumlahan
Penjumlahan adalah menggabungkan dua kumpulan benda menjadi satu.
:::"""

s2_content = """Kita memakai simbol untuk menjumlahkan.
Tanda tambah ditulis plus (+).
Tanda hasil ditulis sama dengan (=).
Tiga apel ditambah dua apel.
Ditulis: $3 + 2 = 5$.
Dibaca tiga ditambah dua sama dengan lima.
Simbol matematika mempermudah kita berhitung.
Berlatihlah menulis tanda tambah dengan rapi.

:::steps
title: Cara Menulis Penjumlahan
1. Tulis bilangan kumpulan pertama.
2. Tulis tanda tambah (+).
3. Tulis bilangan kumpulan kedua.
4. Tulis tanda sama dengan (=) dan hasilnya.
:::"""

s3_content = """Bilangan nol artinya tidak ada benda.
Apa yang terjadi jika ditambah nol?
Ada 4 pensil di kotak.
Kamu menambah 0 pensil baru.
Artinya tidak ada pensil bertambah.
Jumlah pensil tetap 4 buah.
Sembarang bilangan ditambah nol nilainya tetap.
Contohnya $4 + 0 = 4$."""

s4_content = """Pasangan bilangan bisa menghasilkan sepuluh.
Berapa ditambah berapa jadi 10?
Satu ditambah sembilan sama dengan 10.
Dua ditambah delapan sama dengan 10.
Lima ditambah lima juga 10.
Ingat pasangan menuju bilangan 10.

:::common_trap
title: Salah Membaca Simbol Kurang dan Tambah
Tanda tambah (+) artinya digabungkan.
Jangan tertukar dengan tanda kurang (-).
Tanda kurang artinya diambil atau dibuang.
:::

:::callout
variant: summary
title: Ringkasan
text: Penjumlahan menggabungkan benda memakai tanda tambah (+). Ditambah nol nilainya tetap.
:::"""

sections = [
    {
        "id": S1,
        "title": "Menggabungkan Dua Kumpulan Benda",
        "minutes": 6,
        "goal": "Siswa dapat memahami arti penjumlahan sebagai menggabungkan dua kelompok benda konkret atau gambar.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengenal Simbol Tambah dan Sama Dengan",
        "minutes": 6,
        "goal": "Siswa dapat membaca dan menuliskan kalimat matematika dengan simbol + dan =.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Menambah dengan Bilangan Nol",
        "minutes": 6,
        "goal": "Siswa dapat memahami sifat penambahan dengan nol yang menghasilkan bilangan itu sendiri.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Pasangan Bilangan Menuju 10",
        "minutes": 6,
        "goal": "Siswa dapat menemukan pasangan bilangan yang bila dijumlahkan menghasilkan nilai 10.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Penjumlahan sampai 10 dengan Benda dan Gambar",
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
# 2. DEFINISI BANK 50 SOAL BAB 11
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
mc("c1", "mudah", D, F, S2, "Simbol untuk operasi penjumlahan adalah ....", ["+", "-", "=", "x"], "A", "Simbol penjumlahan adalah tanda tambah (+).")
tf("c1", "mudah", D, F, S1, "Menjumlahkan benda artinya menggabungkan benda.", "Benar", "Menjumlahkan memang berarti menggabungkan dua kumpulan benda.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Arti kegiatan menjumlahkan adalah ....", ["menggabungkan benda", "mengambil benda", "membuang benda", "membelah benda"], "A", "Menjumlahkan berarti menyatukan kumpulan benda.")
mc("c1", "mudah", T, F, S2, "Simbol tanda sama dengan ditulis ....", ["=", "+", "-", "<"], "A", "Tanda sama dengan ditulis =.")
sa("c1", "mudah", T, F, S3, "Berapakah hasil dari 5 ditambah 0?", "5", "Bilangan ditambah nol hasilnya bilangan itu sendiri.", verifikasi={"ekspresi": "5 + 0", "hasil": "5"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Ada 2 bola digabung 3 bola. Jumlahnya?", ["5 bola", "4 bola", "6 bola", "3 bola"], "A", "2 ditambah 3 adalah 5 bola.", verifikasi={"ekspresi": "2 + 3", "hasil": "5"})
tf("c2", "mudah", D, Kn, S3, "Bilangan 7 ditambah 0 hasilnya tetap 7.", "Benar", "Menambah nol tidak mengubah jumlah benda.", verifikasi={"ekspresi": "7 + 0", "hasil": "7"})

# Remedial (2)
mc("c2", "mudah", R, F, S2, "Bentuk penjumlahan dua ditambah tiga adalah ....", ["2 + 3", "2 - 3", "2 = 3", "3 - 2"], "A", "Dua ditambah tiga ditulis 2 + 3.", "Tertukar simbol tambah dan kurang")
mc("c2", "mudah", R, Kn, S4, "Pasangan bilangan yang menghasilkan 10 adalah ....", ["6 dan 4", "6 dan 3", "7 dan 2", "5 dan 4"], "A", "6 + 4 = 10.", "Salah menghitung pasangan menuju 10")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Tiga pensil digabung dua pensil menjadi ....", ["5 pensil", "4 pensil", "6 pensil", "7 pensil"], "A", "3 + 2 = 5 pensil.", verifikasi={"ekspresi": "3 + 2", "hasil": "5"})
mc("c2", "mudah", T, Kn, S2, "Kalimat $1 + 4 = 5$ dibaca ....", ["satu ditambah empat sama dengan lima", "satu dikurang empat sama dengan lima", "satu ditambah lima sama dengan empat", "empat dikurang satu sama dengan lima"], "A", "Tanda + dibaca ditambah, = dibaca sama dengan.")
tf("c2", "mudah", T, Kn, S3, "Nol ditambah delapan hasilnya adalah nol.", "Salah", "0 + 8 hasilnya tetap 8, bukan 0.", verifikasi={"ekspresi": "0 + 8", "hasil": "8"})
sa("c2", "mudah", T, Kn, S4, "Sembilan ditambah berapa agar menjadi 10?", "1", "9 + 1 = 10.", verifikasi={"ekspresi": "10 - 9", "hasil": "1"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Di meja ada 4 buku. Ditambah 3 buku. Jumlahnya?", ["7 buku", "6 buku", "8 buku", "5 buku"], "A", "4 + 3 = 7 buku.", "Salah hitung penjumlahan benda", verifikasi={"ekspresi": "4 + 3", "hasil": "7"})
mc("c3", "sedang", R, Pr, S2, "Berapakah hasil dari $4 + 4$?", ["8", "7", "9", "6"], "A", "4 + 4 = 8.", "Salah menjumlahkan angka kembar", verifikasi={"ekspresi": "4 + 4", "hasil": "8"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Ada 5 permen ditambah 2 permen. Berapa jumlahnya?", ["7 permen", "6 permen", "8 permen", "9 permen"], "A", "5 + 2 = 7 permen.", verifikasi={"ekspresi": "5 + 2", "hasil": "7"})
mc("c3", "sedang", T, Pr, S2, "Hasil dari penjumlahan $3 + 4$ adalah ....", ["7", "6", "8", "5"], "A", "3 + 4 = 7.", verifikasi={"ekspresi": "3 + 4", "hasil": "7"})
tf("c3", "sedang", T, Pr, S3, "Hasil dari $0 + 6$ adalah 6.", "Benar", "0 + 6 = 6.", verifikasi={"ekspresi": "0 + 6", "hasil": "6"})
mc("c3", "sedang", T, Pr, S4, "Pasangan 10 dari angka 7 adalah ....", ["3", "2", "4", "5"], "A", "7 + 3 = 10.", verifikasi={"ekspresi": "10 - 7", "hasil": "3"})
tf("c3", "sedang", T, Pr, S1, "Hasil penjumlahan $4 + 2$ sama dengan 7.", "Salah", "4 + 2 = 6, bukan 7.")
sa("c3", "mudah", T, Pr, S2, "Berapakah hasil dari $2 + 6$?", "8", "2 + 6 = 8.", verifikasi={"ekspresi": "2 + 6", "hasil": "8"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Ibu membawa 6 apel lalu membeli 3 apel lagi. Totalnya?", ["9 apel", "8 apel", "10 apel", "7 apel"], "A", "6 + 3 = 9 apel.", verifikasi={"ekspresi": "6 + 3", "hasil": "9"})
mc("c3", "sedang", X, Pr, S2, "Hasil dari penjumlahan $5 + 3$ adalah ....", ["8", "7", "9", "6"], "A", "5 + 3 = 8.", verifikasi={"ekspresi": "5 + 3", "hasil": "8"})
tf("c3", "sedang", X, Pr, S3, "Bilangan 9 ditambah 0 menghasilkan 10.", "Salah", "9 + 0 hasilnya tetap 9.")
sa("c3", "sedang", X, Pr, S4, "Delapan ditambah berapa sama dengan 10?", "2", "8 + 2 = 10.", verifikasi={"ekspresi": "10 - 8", "hasil": "2"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Di kolam ada 4 ikan. Masuk lagi 5 ikan. Jumlahnya?", ["9 ikan", "8 ikan", "10 ikan", "7 ikan"], "A", "4 + 5 = 9 ikan.", verifikasi={"ekspresi": "4 + 5", "hasil": "9"})
mc("c3", "sedang", K, Pr, S2, "Hasil dari penjumlahan $2 + 7$ adalah ....", ["9", "8", "10", "7"], "A", "2 + 7 = 9.", verifikasi={"ekspresi": "2 + 7", "hasil": "9"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Manakah pasangan yang jumlahnya sama dengan $4 + 2$?", ["3 + 3", "4 + 1", "5 + 2", "2 + 3"], "A", "4 + 2 = 6, dan 3 + 3 = 6.")
mc("c4", "sedang", T, Kn, S2, "Penjumlahan $3 + 5$ menghasilkan bilangan yang sama dengan ....", ["5 + 3", "5 - 3", "3 + 6", "4 + 3"], "A", "Penjumlahan bersifat komutatif: 3 + 5 = 5 + 3.")
tf("c4", "sedang", T, Kn, S3, "Menjumlahkan dengan nol membuat bilangan lebih besar.", "Salah", "Menjumlahkan dengan nol tidak mengubah nilai bilangan sama sekali.")
tf("c4", "sedang", T, Kn, S4, "Pasangan 5 dan 5 menghasilkan bilangan 10.", "Benar", "5 + 5 = 10.")
sa("c4", "sedang", T, Kn, S4, "Berapa pasangan angka 3 agar menjadi 10?", "7", "3 + 7 = 10.", verifikasi={"ekspresi": "10 - 3", "hasil": "7"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Manakah yang menghasilkan jumlah paling banyak?", ["6 + 3", "5 + 3", "4 + 4", "2 + 6"], "A", "6 + 3 = 9, paling besar dibanding yang lain.")
mc("c4", "sedang", X, Kn, S2, "Operasi $2 + 4$ dan $1 + 5$ memiliki ....", ["hasil yang sama", "hasil berbeda", "simbol berbeda", "angka sama"], "A", "Keduanya menghasilkan nilai 6.")
tf("c4", "sedang", X, Kn, S4, "Pasangan 6 dan 3 menghasilkan bilangan 10.", "Salah", "6 + 3 = 9, bukan 10.")
mc("c4", "sulit", X, Me, S4, "Manakah pasangan 10 yang angkanya kembar?", ["5 dan 5", "4 dan 6", "3 dan 7", "2 dan 8"], "A", "5 + 5 = 10 dan kedua angkanya kembar.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Bila 3 kelereng ditambah 4 kelereng, hasilnya sama dengan ....", ["2 + 5", "3 + 3", "4 + 4", "1 + 5"], "A", "3 + 4 = 7 dan 2 + 5 = 7.")
mc("c4", "sulit", K, Me, S2, "Jika $A + 3 = 8$, berapakah nilai A?", ["5", "4", "6", "3"], "A", "5 + 3 = 8.", verifikasi={"ekspresi": "8 - 3", "hasil": "5"})
tf("c4", "sulit", K, Me, S3, "Menambah nol tidak mengubah urutan bilangan.", "Benar", "Nilai bilangan tetap sehingga urutannya tidak berubah.")
mc("c4", "sulit", K, Me, S4, "Manakah pasangan 10 yang selisihnya dua?", ["6 dan 4", "7 dan 3", "8 dan 2", "5 dan 5"], "A", "6 + 4 = 10 dan 6 dikurang 4 adalah 2.")

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Beni punya 3 kelereng. Agar jadi 7, Beni harus ....", ["menambah 4 kelereng", "mengambil 4 kelereng", "menambah 3 kelereng", "menambah 5 kelereng"], "A", "3 + 4 = 7 kelereng.")
mc("c5", "sedang", T, Me, S2, "Mengapa $2 + 5$ sama hasilnya dengan $5 + 2$?", ["urutan penambahan tidak mengubah jumlah", "karena angkanya sama persis", "karena ditambah bilangan nol", "karena hasilnya selalu sepuluh"], "A", "Menukar urutan dua bilangan tidak mengubah hasil penjumlahan.")
mc("c5", "sedang", T, Me, S3, "Apakah hasil dari $7 + 0$ sama dengan $0 + 7$?", ["sama", "berbeda", "kurang", "lebih"], "A", "Keduanya bernilai 7 sehingga hasilnya sama.")
mc("c5", "sulit", T, Me, S4, "Siti butuh 10 bunga. Sudah ada 6. Apa langkah Siti?", ["memetik 4 bunga lagi", "memetik 3 bunga lagi", "membuang 4 bunga", "memetik 5 bunga lagi"], "A", "6 + 4 = 10, jadi memetik 4 lagi.")

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Ada 2 kotak pensil. Jumlah pensil 9. Kotak pertama isi 5. Kotak kedua?", ["4 pensil", "3 pensil", "5 pensil", "6 pensil"], "A", "5 + 4 = 9 pensil.", verifikasi={"ekspresi": "9 - 5", "hasil": "4"})
mc("c5", "sulit", K, Me, S4, "Manakah cara paling cepat membuat 10 dari angka 8?", ["menambah 2", "menambah 3", "menambah 1", "menambah 4"], "A", "8 + 2 = 10.")

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Susunlah penjumlahan benda yang hasilnya 8!", ["5 apel ditambah 3 apel", "4 apel ditambah 2 apel", "6 apel ditambah 1 apel", "3 apel ditambah 4 apel"], "A", "5 + 3 = 8 apel.")
mc("c6", "sulit", K, Me, S4, "Buatlah dua pasangan berbeda yang hasilnya 9!", ["$5 + 4$ dan $6 + 3$", "$5 + 3$ dan $6 + 2$", "$4 + 4$ dan $5 + 3$", "$7 + 1$ dan $6 + 1$"], "A", "5 + 4 = 9 dan 6 + 3 = 9.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Rancanglah tiga bilangan yang jika dijumlahkan menghasilkan 10!", ["$2 + 3 + 5$", "$2 + 4 + 5$", "$1 + 3 + 5$", "$3 + 3 + 5$"], "A", "2 + 3 + 5 = 10.")
mc("c6", "sulit", P, Me, S4, "Susunlah bentuk penjumlahan dua bilangan sama yang menghasilkan 10!", ["$5 + 5 = 10$", "$4 + 4 = 10$", "$6 + 6 = 10$", "$3 + 3 = 10$"], "A", "5 + 5 = 10 adalah penjumlahan dua bilangan kembar.")

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab11_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab11.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
