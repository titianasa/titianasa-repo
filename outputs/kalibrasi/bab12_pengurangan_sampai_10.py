#!/usr/bin/env python3
"""
Generator dan validator Bab 12 Matematika Kelas 1 SD:
"Pengurangan sampai 10 dengan Benda dan Gambar" (Fase A)
bab_id: 1cf0d73f-1ff9-4ff1-a9f1-2c46fed74304
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "e5f4a33b6c45"  # Mengambil atau Memisahkan Kumpulan Benda
S2 = "f6a5b44c7d56"  # Mengenal Simbol Kurang (-)
S3 = "a7b6c55d8e67"  # Mengurangkan dengan Bilangan Nol atau Bilangan Sama
S4 = "b8c7d66e9f78"  # Pasangan Pengurangan Bilangan 10

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Pengurangan artinya mengambil sebagian benda.
Benda yang diambil menjadi berkurang.
Ada 5 kue di piring.
Adik memakan 2 kue.
Kue di piring tersisa 3 buah.
Satu, dua, tiga kue tersisa.
Jumlah benda menjadi lebih sedikit.
Menghitung sisa benda sangat mudah.

:::definition
title: Arti Pengurangan
Pengurangan adalah mengambil sejumlah benda dari kumpulan sehingga sisanya lebih sedikit.
:::"""

s2_content = """Simbol pengurangan adalah tanda minus (-).
Tanda hasil adalah sama dengan (=).
Lima kue diambil dua kue.
Ditulis: $5 - 2 = 3$.
Dibaca lima dikurang dua sama dengan tiga.
Angka 3 adalah sisa kue.
Perhatikan posisi tanda kurang (-).
Tanda kurang memisahkan dua bilangan.

:::steps
title: Cara Menulis Pengurangan
1. Tulis banyak benda mula-mula.
2. Tulis tanda kurang (-).
3. Tulis banyak benda yang diambil.
4. Tulis tanda sama dengan (=) dan sisanya.
:::"""

s3_content = """Bagaimana jika dikurang dengan nol?
Ada 6 permen di toples.
Kamu mengambil 0 permen.
Artinya tidak ada permen yang diambil.
Permen tetap berjumlah 6 butir.
Jika 6 permen diambil semua?
Maka tersisa 0 permen.
Bilangan dikurang bilangan sama hasilnya nol."""

s4_content = """Ayo berlatih pengurangan dari bilangan 10.
Sepuluh jari tangan kita buka.
Tutup 3 jari tanganmu.
Tersisa 7 jari yang tegak.
Maka $10 - 3 = 7$.
Tutup 5 jari tanganmu.
Tersisa 5 jari tangan tegak.

:::common_trap
title: Terbalik Meletakkan Bilangan Saat Mengurang
Pada pengurangan bilangan cacah, bilangan mula-mula harus lebih besar.
Jangan menulis $3 - 5$ bila memiliki 5 benda dan diambil 3 benda.
Tulis selalu bilangan besar di depan: $5 - 3 = 2$.
:::

:::callout
variant: summary
title: Ringkasan
text: Pengurangan mengambil benda dengan tanda kurang (-). Dikurang nol tetap, dikurang sama habis.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengambil atau Memisahkan Kumpulan Benda",
        "minutes": 6,
        "goal": "Siswa dapat memahami konsep pengurangan sebagai proses mengambil atau memisahkan benda konkret.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengenal Simbol Kurang (-)",
        "minutes": 6,
        "goal": "Siswa dapat membaca dan menuliskan kalimat matematika pengurangan menggunakan simbol - dan =.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mengurangkan dengan Nol atau Bilangan Sama",
        "minutes": 6,
        "goal": "Siswa dapat memahami hasil pengurangan dengan nol dan hasil pengurangan dua bilangan yang sama.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Pasangan Pengurangan Bilangan 10",
        "minutes": 6,
        "goal": "Siswa dapat menentukan hasil pengurangan dari bilangan 10 dengan bilangan lain sampai 10.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Pengurangan sampai 10 dengan Benda dan Gambar",
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
# 2. DEFINISI BANK 50 SOAL BAB 12
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
mc("c1", "mudah", D, F, S2, "Simbol untuk operasi pengurangan adalah ....", ["-", "+", "=", "x"], "A", "Simbol pengurangan adalah tanda minus (-).")
tf("c1", "mudah", D, F, S1, "Mengambil sebagian benda membuat sisa benda berkurang.", "Benar", "Pengurangan memang membuat benda tersisa lebih sedikit.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Kegiatan pengurangan membuat kumpulan benda menjadi ....", ["lebih sedikit", "lebih banyak", "tetap sama", "berganda"], "A", "Pengurangan mengurangi jumlah benda.")
mc("c1", "mudah", T, F, S2, "Tanda minus (-) dibaca sebagai ....", ["dikurang", "ditambah", "sama dengan", "dikali"], "A", "Tanda - dibaca dikurang.")
sa("c1", "mudah", T, F, S3, "Berapakah hasil dari 7 dikurang 0?", "7", "Bilangan dikurang nol hasilnya tetap.", verifikasi={"ekspresi": "7 - 0", "hasil": "7"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Ada 6 apel diambil 2 apel. Sisanya?", ["4 apel", "5 apel", "3 apel", "2 apel"], "A", "6 - 2 = 4 apel.", verifikasi={"ekspresi": "6 - 2", "hasil": "4"})
tf("c2", "mudah", D, Kn, S3, "Bilangan 5 dikurang 5 hasilnya nol.", "Benar", "5 - 5 = 0.", verifikasi={"ekspresi": "5 - 5", "hasil": "0"})

# Remedial (2)
mc("c2", "mudah", R, F, S2, "Bentuk matematika dari lima dikurang dua adalah ....", ["$5 - 2$", "$5 + 2$", "$2 - 5$", "$5 = 2$"], "A", "Lima dikurang dua ditulis 5 - 2.", "Tertukar urutan atau simbol pengurangan")
mc("c2", "mudah", R, Kn, S3, "Hasil dari $8 - 0$ adalah ....", ["8", "0", "7", "9"], "A", "8 - 0 = 8.", "Mengira dikurang nol hasilnya selalu nol", verifikasi={"ekspresi": "8 - 0", "hasil": "8"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Ada 4 balon meletus 1 balon. Sisanya?", ["3 balon", "2 balon", "4 balon", "1 balon"], "A", "4 - 1 = 3 balon.", verifikasi={"ekspresi": "4 - 1", "hasil": "3"})
mc("c2", "mudah", T, Kn, S2, "Kalimat $7 - 3 = 4$ dibaca ....", ["tujuh dikurang tiga sama dengan empat", "tujuh ditambah tiga sama dengan empat", "tiga dikurang tujuh sama dengan empat", "tujuh sama dengan tiga dikurang empat"], "A", "Kalimat matematika dibaca secara urut.")
tf("c2", "mudah", T, Kn, S3, "Hasil dari sembilan dikurang sembilan adalah sembilan.", "Salah", "9 - 9 = 0, bukan 9.")
sa("c2", "mudah", T, Kn, S4, "Sepuluh dikurang berapa agar bersisa 8?", "2", "10 - 2 = 8.", verifikasi={"ekspresi": "10 - 8", "hasil": "2"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Di piring ada 7 biskuit dimakan 3 biskuit. Sisanya?", ["4 biskuit", "5 biskuit", "3 biskuit", "2 biskuit"], "A", "7 - 3 = 4 biskuit.", "Salah menghitung hasil pengurangan", verifikasi={"ekspresi": "7 - 3", "hasil": "4"})
mc("c3", "sedang", R, Pr, S4, "Berapakah hasil dari $10 - 4$?", ["6", "5", "7", "4"], "A", "10 - 4 = 6.", "Salah menghitung pengurangan dari 10", verifikasi={"ekspresi": "10 - 4", "hasil": "6"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Ada 8 burung terbang 2 ekor. Berapa sisa burung?", ["6 ekor", "5 ekor", "7 ekor", "4 ekor"], "A", "8 - 2 = 6 ekor.", verifikasi={"ekspresi": "8 - 2", "hasil": "6"})
mc("c3", "sedang", T, Pr, S2, "Hasil pengurangan dari $6 - 3$ adalah ....", ["3", "2", "4", "1"], "A", "6 - 3 = 3.", verifikasi={"ekspresi": "6 - 3", "hasil": "3"})
tf("c3", "sedang", T, Pr, S3, "Hasil dari $4 - 4$ adalah 0.", "Benar", "4 - 4 = 0.", verifikasi={"ekspresi": "4 - 4", "hasil": "0"})
mc("c3", "sedang", T, Pr, S4, "Berapakah sisa dari $10 - 7$?", ["3", "2", "4", "5"], "A", "10 - 7 = 3.", verifikasi={"ekspresi": "10 - 7", "hasil": "3"})
tf("c3", "sedang", T, Pr, S1, "Tujuh kue diambil 2 kue tersisa 4 kue.", "Salah", "7 - 2 = 5 kue, bukan 4 kue.")
sa("c3", "mudah", T, Pr, S2, "Berapakah hasil dari $9 - 5$?", "4", "9 - 5 = 4.", verifikasi={"ekspresi": "9 - 5", "hasil": "4"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Beni punya 9 kelereng hilang 3 kelereng. Sisanya?", ["6 kelereng", "5 kelereng", "7 kelereng", "4 kelereng"], "A", "9 - 3 = 6 kelereng.", verifikasi={"ekspresi": "9 - 3", "hasil": "6"})
mc("c3", "sedang", X, Pr, S2, "Hasil dari $8 - 5$ adalah ....", ["3", "2", "4", "5"], "A", "8 - 5 = 3.", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})
tf("c3", "sedang", X, Pr, S3, "Pengurangan $10 - 0$ bernilai 0.", "Salah", "10 - 0 = 10.")
sa("c3", "sedang", X, Pr, S4, "Sepuluh dikurang berapa sama dengan 5?", "5", "10 - 5 = 5.", verifikasi={"ekspresi": "10 - 5", "hasil": "5"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Ada 8 mangga busuk 4 mangga. Sisanya?", ["4 mangga", "3 mangga", "5 mangga", "2 mangga"], "A", "8 - 4 = 4 mangga.", verifikasi={"ekspresi": "8 - 4", "hasil": "4"})
mc("c3", "sedang", K, Pr, S2, "Hasil dari pengurangan $7 - 4$ adalah ....", ["3", "2", "4", "5"], "A", "7 - 4 = 3.", verifikasi={"ekspresi": "7 - 4", "hasil": "3"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Manakah pengurangan yang hasilnya sama dengan $8 - 4$?", ["$5 - 1$", "$6 - 1$", "$7 - 2$", "$9 - 4$"], "A", "8 - 4 = 4 dan 5 - 1 = 4.")
mc("c4", "sedang", T, Kn, S2, "Pengurangan $6 - 2$ menghasilkan nilai yang sama dengan ....", ["$7 - 3$", "$5 - 2$", "$8 - 3$", "$4 - 1$"], "A", "6 - 2 = 4 dan 7 - 3 = 4.")
tf("c4", "sedang", T, Kn, S3, "Mengurangkan dengan nol tidak mengubah nilai bilangan.", "Benar", "Bilangan dikurang nol hasilnya tetap bilangan itu.")
tf("c4", "sedang", T, Kn, S4, "Hasil dari $10 - 6$ adalah 4.", "Benar", "10 - 6 = 4.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari $10 - 1$?", "9", "10 - 1 = 9.", verifikasi={"ekspresi": "10 - 1", "hasil": "9"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Manakah pengurangan yang menghasilkan sisa paling sedikit?", ["$9 - 8$", "$8 - 5$", "$7 - 2$", "$6 - 1$"], "A", "9 - 8 = 1, paling kecil.")
mc("c4", "sedang", X, Kn, S2, "Operasi $9 - 5$ dan $8 - 4$ memiliki ....", ["hasil yang sama", "hasil berbeda", "simbol berbeda", "angka mula-mula sama"], "A", "Keduanya menghasilkan 4.")
tf("c4", "sedang", X, Kn, S4, "Operasi $10 - 3$ menghasilkan bilangan 6.", "Salah", "10 - 3 = 7, bukan 6.")
mc("c4", "sulit", X, Me, S4, "Bilangan 10 dikurang bilangan berapa yang hasilnya kembar?", ["5", "4", "3", "2"], "A", "10 - 5 = 5 (pengurang dan hasilnya kembar).", verifikasi={"ekspresi": "10 - 5", "hasil": "5"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Bila 8 permen diambil 3 permen, sisanya sama dengan ....", ["$9 - 4$", "$7 - 3$", "$6 - 2$", "$8 - 2$"], "A", "8 - 3 = 5 dan 9 - 4 = 5.")
mc("c4", "sulit", K, Me, S2, "Jika $9 - B = 6$, berapakah nilai B?", ["3", "2", "4", "5"], "A", "9 - 3 = 6.", verifikasi={"ekspresi": "9 - 6", "hasil": "3"})
tf("c4", "sulit", K, Me, S3, "Jika dua bilangan sama dikurangkan hasilnya selalu 1.", "Salah", "Hasilnya selalu 0, bukan 1.")
mc("c4", "sulit", K, Me, S4, "Dari bilangan 10, dikurang berapa agar bersisa 1?", ["9", "8", "7", "6"], "A", "10 - 9 = 1.", verifikasi={"ekspresi": "10 - 1", "hasil": "9"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Edo punya 8 kelereng. Agar sisa 5 kelereng, Edo harus ....", ["memberikan 3 kelereng", "memberikan 2 kelereng", "meminta 3 kelereng", "memberikan 4 kelereng"], "A", "8 - 5 = 3, jadi memberikan 3 kelereng.")
mc("c5", "sedang", T, Me, S2, "Mengapa $5 - 2$ tidak sama dengan $2 - 5$?", ["pengurangan tidak boleh dibalik urutannya", "karena angkanya berbeda", "karena hasilnya nol", "karena ada tanda tambah"], "A", "Urutan pengurangan bilangan cacah tidak boleh dibalik.")
mc("c5", "sedang", T, Me, S3, "Bila kotak berisi 7 donat dimakan habis, apa yang tersisa?", ["0 donat", "1 donat", "7 donat", "2 donat"], "A", "7 - 7 = 0 donat.", verifikasi={"ekspresi": "7 - 7", "hasil": "0"})
mc("c5", "sulit", T, Me, S4, "Ada 10 kursi. Dipakai 6 orang. Berapa kursi kosong?", ["4 kursi", "3 kursi", "5 kursi", "2 kursi"], "A", "10 - 6 = 4 kursi.", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Ibu punya 9 telur. Pecah 4 telur. Berapa telur utuh?", ["5 telur", "4 telur", "6 telur", "3 telur"], "A", "9 - 4 = 5 telur.", verifikasi={"ekspresi": "9 - 4", "hasil": "5"})
mc("c5", "sulit", K, Me, S4, "Lani punya 10 pita. Diberikan ke adik hingga sisa 3. Berapa diberikan?", ["7 pita", "6 pita", "8 pita", "5 pita"], "A", "10 - 3 = 7 pita.", verifikasi={"ekspresi": "10 - 3", "hasil": "7"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Susunlah bentuk pengurangan benda yang bersisa 5!", ["9 jeruk diambil 4 jeruk", "8 jeruk diambil 2 jeruk", "7 jeruk diambil 1 jeruk", "6 jeruk diambil 2 jeruk"], "A", "9 - 4 = 5 jeruk.")
mc("c6", "sulit", K, Me, S4, "Buatlah dua pengurangan dari 10 yang hasilnya berurutan!", ["$10 - 6$ dan $10 - 5$", "$10 - 4$ dan $10 - 2$", "$10 - 7$ dan $10 - 4$", "$10 - 8$ dan $10 - 5$"], "A", "10 - 6 = 4 dan 10 - 5 = 5 (berurutan 4 dan 5).")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Rancanglah pengurangan bertingkat $10 - 2 - 3$!", ["5", "6", "4", "7"], "A", "10 - 2 = 8, lalu 8 - 3 = 5.", verifikasi={"ekspresi": "10 - 2 - 3", "hasil": "5"})
mc("c6", "sulit", P, Me, S4, "Susunlah kalimat matematika pengurangan dari 10 bersisa 2!", ["$10 - 8 = 2$", "$10 - 7 = 3$", "$10 - 6 = 4$", "$10 - 5 = 5$"], "A", "10 - 8 = 2.")

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab12_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab12.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
