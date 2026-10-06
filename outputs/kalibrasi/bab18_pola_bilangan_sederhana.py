#!/usr/bin/env python3
"""
Generator dan validator Bab 18 Matematika Kelas 1 SD:
"Pola Bilangan Sederhana" (Fase A)
bab_id: 625b9305-0863-40ac-ad55-92bc62aebe0b
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a8b7c69d9e01"  # Membilang Maju Bertambah Satu (+1)
S2 = "b9c8d70e0f12"  # Pola Loncatan Dua Bilangan (+2)
S3 = "c0d9e81f1a23"  # Pola Loncatan Lima dan Sepuluh
S4 = "d1e0f92a2b34"  # Pola Bilangan Berkurang (Membilang Mundur)

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Bilangan juga bisa membentuk pola.
Paling mudah adalah bertambah satu.
Contohnya: 1, 2, 3, 4, 5.
Setiap langkah ditambah satu angka.
Kita membilang maju secara urut.
Berapa angka setelah 5?
Tentu saja angka 6.
Aturan polanya adalah tambah 1.

:::definition
title: Pola Tambah Satu
Pola tambah satu berarti bilangan selalu bertambah 1 langkah.
Bilangan berurutan dari kecil ke besar.
:::"""

s2_content = """Ayo melompat dua angka.
Ini disebut pola bertambah dua.
Contohnya: 2, 4, 6, 8.
Dua ditambah dua jadi empat.
Empat ditambah dua jadi enam.
Berapa angka setelah 8?
Delapan ditambah dua adalah 10.
Lompatannya selalu dua angka.

:::steps
title: Melanjutkan Pola Tambah Dua
1. Ambil bilangan terakhir pada barisan.
2. Tambahkan 2 pada bilangan itu.
3. Tuliskan hasilnya sebagai bilangan berikutnya.
:::"""

s3_content = """Bisa juga loncat lebih jauh.
Misalnya pola bertambah lima.
Contohnya: 5, 10, 15, 20.
Atau pola bertambah sepuluh.
Contohnya: 10, 20, 30, 40.
Semua bertambah secara teratur.
Hitunglah loncatannya dengan teliti.
Setiap angka berjarak sama."""

s4_content = """Pola juga bisa berkurang.
Angkanya menjadi semakin kecil.
Contohnya: 10, 9, 8, 7.
Setiap langkah dikurangi satu.
Bisa juga mundur dua: 10, 8, 6.

:::common_trap
title: Mengira Pola Selalu Bertambah
Perhatikan urutan bilangan dengan cermat.
Bila angka mengecil, berarti polanya berkurang.
Kurangkan dengan selisih yang tetap.
Jangan menambahkan saat angka mengecil.
:::

:::callout
variant: summary
title: Ringkasan
text: Pola bilangan punya loncatan tetap. Tambah jika membesar, kurang jika mengecil.
:::"""

sections = [
    {
        "id": S1,
        "title": "Membilang Maju Bertambah Satu (+1)",
        "minutes": 6,
        "goal": "Siswa dapat mengenali dan melanjutkan pola bilangan bertambah satu secara teratur.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Pola Loncatan Dua Bilangan (+2)",
        "minutes": 6,
        "goal": "Siswa dapat mengenali dan melanjutkan pola bilangan loncat dua (genap/ganjil).",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Pola Loncatan Lima dan Sepuluh",
        "minutes": 6,
        "goal": "Siswa dapat mengenali dan melanjutkan pola bilangan bertambah lima dan sepuluh.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Pola Bilangan Berkurang (Membilang Mundur)",
        "minutes": 6,
        "goal": "Siswa dapat mengenali dan melanjutkan pola bilangan berkurang teratur.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Pola Bilangan Sederhana",
    "topic": "Pola dan Urutan",
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
# 2. DEFINISI BANK 50 SOAL BAB 18
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
mc("c1", "mudah", D, F, S1, "Pada barisan 1, 2, 3, 4, bilangan bertambah berapa tiap langkah?", ["1", "2", "3", "4"], "A", "Tiap langkah bertambah 1.", verifikasi={"ekspresi": "1", "hasil": "1"})
tf("c1", "mudah", D, F, S2, "Barisan 2, 4, 6, 8 adalah pola bilangan loncat dua.", "Benar", "Tiap bilangan bertambah 2.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Lanjutan dari barisan 5, 6, 7, .... adalah angka ....", ["8", "9", "7", "10"], "A", "7 + 1 = 8.", verifikasi={"ekspresi": "7 + 1", "hasil": "8"})
mc("c1", "mudah", T, F, S2, "Berapa selisih antarangka pada pola loncat dua?", ["2", "1", "3", "4"], "A", "Selisihnya selalu 2.", verifikasi={"ekspresi": "2", "hasil": "2"})
sa("c1", "mudah", T, F, S3, "Berapa loncatan antarangka pada barisan 5, 10, 15, 20?", "5", "Loncatan antarangka bernilai 5.", verifikasi={"ekspresi": "5", "hasil": "5"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Pola: 1, 3, 5, 7, .... Angka berikutnya adalah ....", ["9", "8", "10", "11"], "A", "7 + 2 = 9.", verifikasi={"ekspresi": "7 + 2", "hasil": "9"})
tf("c2", "mudah", D, Kn, S4, "Barisan 10, 9, 8, 7 adalah pola bilangan bertambah satu.", "Salah", "Nilainya mengecil, jadi pola berkurang satu.")

# Remedial (2)
mc("c2", "mudah", R, F, S4, "Bila angka pada barisan semakin kecil, maka aturannya adalah ....", ["berkurang", "bertambah", "dikalikan", "tetap"], "A", "Angka yang mengecil menunjukkan aturan berkurang.", "Mengira pola bilangan selalu bertambah")
mc("c2", "mudah", R, Kn, S2, "Pola: 2, 4, 6, .... Angka berikutnya adalah ....", ["8", "7", "9", "10"], "A", "6 + 2 = 8.", "Salah menjumlahkan loncatan dua", verifikasi={"ekspresi": "6 + 2", "hasil": "8"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Barisan: 8, 9, 10, 11, .... Angka berikutnya adalah ....", ["12", "13", "11", "14"], "A", "11 + 1 = 12.", verifikasi={"ekspresi": "11 + 1", "hasil": "12"})
mc("c2", "mudah", T, Kn, S2, "Pola loncat dua mulai dari 1: 1, 3, 5, .... Angka selanjutnya?", ["7", "6", "8", "9"], "A", "5 + 2 = 7.", verifikasi={"ekspresi": "5 + 2", "hasil": "7"})
tf("c2", "mudah", T, Kn, S3, "Barisan 10, 20, 30 bertambah sepuluh pada setiap langkah.", "Benar", "10 + 10 = 20, 20 + 10 = 30.")
sa("c2", "mudah", T, Kn, S4, "Pola mundur: 6, 5, 4, .... Angka berikutnya adalah?", "3", "4 - 1 = 3.", verifikasi={"ekspresi": "4 - 1", "hasil": "3"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Pola loncat lima: 5, 10, 15, .... Angka berikutnya adalah ....", ["20", "25", "18", "16"], "A", "15 + 5 = 20.", "Salah menghitung loncatan lima", verifikasi={"ekspresi": "15 + 5", "hasil": "20"})
mc("c3", "sedang", R, Pr, S4, "Pola mundur: 10, 8, 6, .... Angka selanjutnya adalah ....", ["4", "5", "3", "2"], "A", "6 - 2 = 4.", "Salah menghitung pola mundur loncat dua", verifikasi={"ekspresi": "6 - 2", "hasil": "4"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Lengkapi barisan bertambah satu: 14, 15, ..., 17.", ["16", "18", "13", "15"], "A", "15 + 1 = 16.", verifikasi={"ekspresi": "15 + 1", "hasil": "16"})
mc("c3", "sedang", T, Pr, S2, "Pola: 10, 12, 14, 16, .... Berapakah angka berikutnya?", ["18", "17", "19", "20"], "A", "16 + 2 = 18.", verifikasi={"ekspresi": "16 + 2", "hasil": "18"})
tf("c3", "sedang", T, Pr, S3, "Pada barisan 5, 10, 15, 20, angka ke-5 adalah 25.", "Benar", "20 + 5 = 25.", verifikasi={"ekspresi": "20 + 5", "hasil": "25"})
mc("c3", "sedang", T, Pr, S4, "Barisan: 15, 14, 13, 12, .... Bilangan selanjutnya adalah ....", ["11", "10", "13", "9"], "A", "12 - 1 = 11.", verifikasi={"ekspresi": "12 - 1", "hasil": "11"})
tf("c3", "sedang", T, Pr, S1, "Barisan 3, 5, 7 memiliki aturan bertambah satu.", "Salah", "Selisihnya 2, jadi bertambah dua.")
sa("c3", "mudah", T, Pr, S2, "Pola: 9, 11, 13, .... Angka berikutnya adalah?", "15", "13 + 2 = 15.", verifikasi={"ekspresi": "13 + 2", "hasil": "15"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Barisan: 7, 8, 9, 10, 11. Berapa banyak angka pada barisan itu?", ["5", "4", "6", "3"], "A", "Ada 5 angka tertulis.", verifikasi={"ekspresi": "5", "hasil": "5"})
mc("c3", "sedang", X, Pr, S2, "Pola loncat dua: 8, 10, 12, .... Angka setelah 12 adalah ....", ["14", "13", "15", "16"], "A", "12 + 2 = 14.", verifikasi={"ekspresi": "12 + 2", "hasil": "14"})
tf("c3", "sedang", X, Pr, S3, "Barisan 10, 20, 30, 40 memiliki aturan tambah lima.", "Salah", "Aturannya adalah tambah 10, bukan tambah 5.")
sa("c3", "sedang", X, Pr, S4, "Membilang mundur: 20, 19, 18, .... Angka berikutnya adalah?", "17", "18 - 1 = 17.", verifikasi={"ekspresi": "18 - 1", "hasil": "17"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Lengkapi barisan: 12, 13, 14, .... Angka berikutnya adalah ....", ["15", "16", "17", "14"], "A", "14 + 1 = 15.", verifikasi={"ekspresi": "14 + 1", "hasil": "15"})
mc("c3", "sedang", K, Pr, S3, "Pola loncat sepuluh: 20, 30, 40, .... Angka berikutnya adalah ....", ["50", "60", "45", "70"], "A", "40 + 10 = 50.", verifikasi={"ekspresi": "40 + 10", "hasil": "50"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Barisan: 2, 4, 6, 8 dan barisan 1, 3, 5, 7 sama-sama memiliki aturan ....", ["bertambah 2", "bertambah 1", "berkurang 2", "bertambah 3"], "A", "Keduanya memiliki selisih loncatan yang sama yaitu +2.")
mc("c4", "sedang", T, Kn, S2, "Ada angka hilang: 4, 6, ..., 10, 12. Angka berapakah itu?", ["8", "7", "9", "11"], "A", "6 + 2 = 8.", verifikasi={"ekspresi": "6 + 2", "hasil": "8"})
tf("c4", "sedang", T, Kn, S3, "Barisan 5, 10, 15, 20 semua bilangannya berakhiran 0 atau 5.", "Benar", "Kelipatan 5 selalu berakhiran 0 atau 5.")
tf("c4", "sedang", T, Kn, S4, "Barisan 20, 18, 16, 14 bertambah dua setiap langkah.", "Salah", "Barisan tersebut angkanya mengecil, jadi berkurang dua bukan bertambah.")
sa("c4", "sedang", T, Kn, S4, "Barisan mundur: 14, 12, 10, .... Angka selanjutnya adalah?", "8", "10 - 2 = 8.", verifikasi={"ekspresi": "10 - 2", "hasil": "8"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Lengkapi dua angka: 3, 4, 5, ..., .... Angka yang tepat adalah ....", ["6 dan 7", "7 dan 8", "5 dan 6", "6 dan 8"], "A", "Lanjutan dari 5 adalah 6 lalu 7.")
mc("c4", "sedang", X, Kn, S2, "Manakah barisan yang bertambah dua setiap langkah?", ["5, 7, 9, 11", "5, 6, 7, 8", "5, 10, 15, 20", "5, 8, 11, 14"], "A", "7 - 5 = 2, 9 - 7 = 2, 11 - 9 = 2.")
tf("c4", "sedang", X, Kn, S4, "Barisan 12, 10, 8, 7 memiliki aturan loncatan yang teratur.", "Salah", "Dari 8 ke 7 berkurang 1, tidak teratur loncat dua.")
mc("c4", "sulit", X, Me, S3, "Barisan 10, 20, 30, 40, 50. Berapa jumlah dua angka pertama?", ["30", "20", "40", "25"], "A", "10 + 20 = 30.", verifikasi={"ekspresi": "10 + 20", "hasil": "30"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Bandingkan barisan A (1, 2, 3) dan B (10, 9, 8). Perbedaannya adalah ....", ["A bertambah sedangkan B berkurang", "A berkurang sedangkan B bertambah", "keduanya bertambah", "keduanya berkurang"], "A", "A membilang maju (+1) sedangkan B membilang mundur (-1).")
mc("c4", "sulit", K, Me, S2, "Ada barisan: 3, 6, 9, 12. Berapakah loncatan pada barisan tersebut?", ["3", "2", "4", "5"], "A", "6 - 3 = 3.", verifikasi={"ekspresi": "6 - 3", "hasil": "3"})
tf("c4", "sulit", K, Me, S3, "Loncatan sepuluh dari angka 5 adalah 15 lalu 25.", "Benar", "5 + 10 = 15, 15 + 10 = 25.")
mc("c4", "sulit", K, Me, S4, "Membilang mundur loncat dua mulai dari 16. Angka ke-3 adalah ....", ["12", "14", "10", "8"], "A", "16(1), 14(2), 12(3).", verifikasi={"ekspresi": "16 - 4", "hasil": "12"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Dito menulis barisan: 4, 5, 7, 8. Angka mana yang terlewat?", ["6", "5", "9", "3"], "A", "Setelah 5 seharusnya 6 sebelum 7.")
mc("c5", "sedang", T, Me, S2, "Katak melompat di batu 2, 4, 6. Jika melompat 3 kali lagi, tiba di batu?", ["12", "10", "14", "8"], "A", "6 + 2 + 2 + 2 = 12.", verifikasi={"ekspresi": "6 + 6", "hasil": "12"})
mc("c5", "sedang", T, Me, S3, "Tabungan Siti: 10, 20, 30. Berapa rupiah tabungan pada hari ke-5?", ["50", "40", "60", "70"], "A", "Hari ke-5 adalah 50.", verifikasi={"ekspresi": "50", "hasil": "50"})
mc("c5", "sulit", T, Me, S4, "Hitung mundur dari 18 loncat dua sampai angka 10. Berapa kali loncatan?", ["4 kali", "3 kali", "5 kali", "2 kali"], "A", "(18 - 10) / 2 = 4 kali.", verifikasi={"ekspresi": "(18 - 10) // 2", "hasil": "4"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Barisan 11, 13, ..., 17, 19. Angka berapa yang melengkapi barisan?", ["15", "14", "16", "12"], "A", "13 + 2 = 15.", verifikasi={"ekspresi": "13 + 2", "hasil": "15"})
mc("c5", "sulit", K, Me, S4, "Dari angka 20 mundur loncat 5. Berapakah angka setelah dua kali loncatan?", ["10", "15", "5", "0"], "A", "20 - 5 = 15, 15 - 5 = 10.", verifikasi={"ekspresi": "20 - 10", "hasil": "10"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Susunlah barisan loncat dua yang dimulai dari angka 7!", ["7, 9, 11, 13", "7, 8, 9, 10", "7, 10, 13, 16", "7, 12, 17, 22"], "A", "7 + 2 = 9, 9 + 2 = 11, 11 + 2 = 13.")
mc("c6", "sulit", K, Me, S4, "Rancanglah barisan bilangan berkurang empat angka mulai dari 16 loncat dua!", ["16, 14, 12, 10", "16, 15, 14, 13", "16, 12, 8, 4", "16, 14, 11, 9"], "A", "16 - 2 = 14, 14 - 2 = 12, 12 - 2 = 10.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S2, "Susunlah barisan loncat dua dari 2 sampai 12! Berapa banyak angka genap?", ["6", "5", "7", "4"], "A", "2, 4, 6, 8, 10, 12 ada 6 angka.", verifikasi={"ekspresi": "12 // 2", "hasil": "6"})
mc("c6", "sulit", P, Me, S3, "Rancanglah pola loncat sepuluh mulai 5 sampai melebihi 30! Angka terakhirnya?", ["35", "30", "40", "25"], "A", "5, 15, 25, 35 melebihi 30.", verifikasi={"ekspresi": "35", "hasil": "35"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab18_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab18.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
