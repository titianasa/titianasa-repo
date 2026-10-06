#!/usr/bin/env python3
"""
Generator dan validator Bab 57 Matematika Kelas 2 SD:
"Membilang Loncat 2, 5, dan 10" (Fase A)
bab_id: 6e1d1fef-46ee-4537-93e5-47369d84dbd6
article_id: 9e3b6250-80c2-49e9-8a35-d4fc9a3b2918
quiz_id: 063186f5-6da7-4d86-b2db-7057ebfcdbf5
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "b1d2f3h4j501"  # Membilang Loncat 2
S2 = "c2e3g4i5k602"  # Membilang Loncat 5
S3 = "d3f4h5j6l703"  # Membilang Loncat 10
S4 = "e4g5i6k7m804"  # Membilang Loncat Mundur

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Membilang tidak harus satu-satu.
Kita bisa membilang lompat dua.
Setiap langkah bertambah dua angka.
Mulai dari dua: 2, 4, 6, 8, 10.
Semua bilangan itu genap.
Kita juga bisa mulai dari satu.
1, 3, 5, 7, 9.
Semua bilangan itu ganjil.
Loncat dua sangat menghemat waktu!

:::definition
title: Membilang Loncat 2
Membilang loncat 2 adalah menghitung urutan dengan menambahkan 2 pada setiap langkah berikutnya.
:::"""

s2_content = """Sekarang perhatikan loncat lima.
Setiap langkah bertambah lima angka.
Mari berhitung bersama-sama:
5, 10, 15, 20, 25, 30.
Perhatikan angka satuannya yang unik.
Satuannya selalu bergantian lima dan nol!
5 lalu 0, 5 lalu 0.
Pola ini sangat indah dan teratur.
Hitunglah kelipatan lima dengan riang!

:::steps
title: Langkah Membilang Loncat 5
1. Mulai dari angka 5.
2. Tambahkan 5 pada angka sebelumnya.
3. Periksa angka satuan: bergantian 5 dan 0.
:::"""

s3_content = """Loncat sepuluh adalah yang tercepat.
Setiap langkah bertambah sepuluh angka.
10, 20, 30, 40, 50, 60.
Angka satuannya selalu tetap nol!
Hanya angka puluhannya yang naik satu.
Satu, dua, tiga, empat, lima.
Jika mulai dari 4: 14, 24, 34, 44.
Satuannya tetap angka empat!"""

s4_content = """Kita bisa loncat mundur.
Loncat mundur berarti mengurang teratur.
Mundur 2: 10, 8, 6.
Mundur 5: 25, 20, 15.
Mundur 10: 50, 40, 30.
Nilai angka semakin mengecil.
Hitunglah mundur dengan teliti!

:::common_trap
title: Tertukar Antara Loncat Maju dan Mundur
Jika angka makin besar, itu loncat maju.
Jika angka makin kecil, itu loncat mundur.
Jangan sampai salah operasi!
:::

:::callout
variant: summary
title: Ringkasan
text: Loncat 2 ditambah 2. Loncat 5 ditambah 5. Loncat 10 ditambah 10. Loncat mundur berarti dikurang.
:::"""

sections = [
    {
        "id": S1,
        "title": "Membilang Loncat 2",
        "minutes": 6,
        "goal": "Siswa mampu membilang loncat 2 maju secara lisan maupun tertulis hingga 100.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Membilang Loncat 5",
        "minutes": 6,
        "goal": "Siswa mampu membilang loncat 5 maju dan mengenali pola satuan bergantian 5 dan 0.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membilang Loncat 10",
        "minutes": 6,
        "goal": "Siswa mampu membilang loncat 10 maju dengan melihat pertambahan angka puluhan.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Membilang Loncat Mundur",
        "minutes": 6,
        "goal": "Siswa mampu melakukan pembilangan loncat mundur 2, 5, dan 10 secara teratur.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membilang Loncat 2, 5, dan 10",
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
# 2. DEFINISI BANK 50 SOAL BAB 57
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
mc("c1", "mudah", D, F, S1, "Membilang loncat 2 artinya setiap langkah bertambah bilangan ....", ["2", "1", "3", "5"], "A", "Loncat 2 bertambah 2 tiap langkah.", verifikasi={"ekspresi": "2 / 1", "hasil": "2"})
tf("c1", "mudah", D, F, S2, "Pada loncat 5, angka satuannya bergantian antara 5 dan 0.", "Benar", "Akhiran loncat 5 selalu bergantian 5 dan 0.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Lanjutan dari 5, 10, 15 adalah bilangan ....", ["20", "18", "25", "16"], "A", "15 + 5 = 20.", verifikasi={"ekspresi": "15 + 5", "hasil": "20"})
mc("c1", "mudah", T, F, S3, "Lanjutan dari 10, 20, 30 adalah bilangan ....", ["40", "35", "50", "45"], "A", "30 + 10 = 40.", verifikasi={"ekspresi": "30 + 10", "hasil": "40"})
sa("c1", "mudah", T, F, S1, "Berapakah bilangan setelah 6 pada loncat 2?", "8", "6 + 2 = 8.", verifikasi={"ekspresi": "6 + 2", "hasil": "8"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Pola 20, 18, 16, 14 merupakan pola loncat ....", ["mundur 2", "maju 2", "mundur 5", "maju 5"], "A", "Angka berkurang 2 setiap langkah, yaitu loncat mundur 2.")
tf("c2", "mudah", D, Kn, S3, "Pada loncat 10 mulai dari 10, angka satuan selalu berubah-ubah.", "Salah", "Pada loncat 10 mulai dari 10, angka satuannya selalu tetap nol.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Lanjutan dari 25 pada loncat 5 maju adalah ....", ["30", "35", "26", "28"], "A", "25 + 5 = 30.", "Salah menambahkan loncat 5", verifikasi={"ekspresi": "25 + 5", "hasil": "30"})
mc("c2", "mudah", R, Kn, S1, "Lanjutan dari 7 pada loncat 2 maju adalah ....", ["9", "8", "10", "11"], "A", "7 + 2 = 9.", "Tertukar loncat 1 dengan loncat 2", verifikasi={"ekspresi": "7 + 2", "hasil": "9"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Mulai dari 12, sebutkan 2 angka berikutnya pada loncat 2!", ["14 dan 16", "13 dan 14", "15 dan 17", "14 dan 15"], "A", "12 + 2 = 14; 14 + 2 = 16.")
mc("c2", "mudah", T, Kn, S3, "Lanjutan dari 50 pada loncat 10 maju adalah ....", ["60", "55", "70", "65"], "A", "50 + 10 = 60.", verifikasi={"ekspresi": "50 + 10", "hasil": "60"})
tf("c2", "mudah", T, Kn, S4, "Urutan 40, 35, 30 adalah loncat mundur 5.", "Benar", "Setiap langkah berkurang 5.")
sa("c2", "mudah", T, Kn, S2, "Berapakah bilangan setelah 35 pada loncat 5 maju?", "40", "35 + 5 = 40.", verifikasi={"ekspresi": "35 + 5", "hasil": "40"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S4, "Lanjutan dari 50, 40, 30 adalah ....", ["20", "25", "10", "35"], "A", "30 - 10 = 20.", "Keliru loncat mundur 10", verifikasi={"ekspresi": "30 - 10", "hasil": "20"})
mc("c3", "sedang", R, Pr, S1, "Lengkapi titik-titik: 18, 20, ..., 24!", ["22", "21", "23", "25"], "A", "20 + 2 = 22.", "Salah melompati bilangan genap", verifikasi={"ekspresi": "20 + 2", "hasil": "22"})

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Lengkapi titik-titik: 14, 16, 18, ...!", ["20", "19", "21", "22"], "A", "18 + 2 = 20.", verifikasi={"ekspresi": "18 + 2", "hasil": "20"})
mc("c3", "mudah", T, Pr, S2, "Lengkapi titik-titik: 40, 45, 50, ...!", ["55", "60", "52", "54"], "A", "50 + 5 = 55.", verifikasi={"ekspresi": "50 + 5", "hasil": "55"})
tf("c3", "sedang", T, Pr, S3, "Urutan 17, 27, 37, 47 adalah loncat 10 maju.", "Benar", "Setiap langkah bertambah 10 dan satuannya tetap 7.")
mc("c3", "sedang", T, Pr, S4, "Lanjutan dari 24, 22, 20 adalah ....", ["18", "19", "16", "17"], "A", "20 - 2 = 18.", verifikasi={"ekspresi": "20 - 2", "hasil": "18"})
tf("c3", "sedang", T, Pr, S1, "Setelah angka 15 pada loncat 2 maju adalah 18.", "Salah", "15 + 2 = 17, bukan 18.")
sa("c3", "sedang", T, Pr, S3, "Berapakah bilangan setelah 63 pada loncat 10 maju?", "73", "63 + 10 = 73.", verifikasi={"ekspresi": "63 + 10", "hasil": "73"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Lengkapi titik-titik: 27, 29, 31, ...!", ["33", "32", "34", "35"], "A", "31 + 2 = 33.", verifikasi={"ekspresi": "31 + 2", "hasil": "33"})
mc("c3", "sedang", X, Pr, S2, "Berapakah bilangan setelah 65 pada loncat 5 maju?", ["70", "75", "68", "72"], "A", "65 + 5 = 70.", verifikasi={"ekspresi": "65 + 5", "hasil": "70"})
tf("c3", "sedang", X, Pr, S4, "Urutan 70, 60, 50, 30 adalah urutan yang benar.", "Salah", "Setelah 50 pada loncat mundur 10 adalah 40, bukan 30.")
sa("c3", "sedang", X, Pr, S4, "Berapakah bilangan setelah 45 pada loncat mundur 5?", "40", "45 - 5 = 40.", verifikasi={"ekspresi": "45 - 5", "hasil": "40"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Lengkapi titik-titik: 32, 42, 52, ...!", ["62", "60", "64", "58"], "A", "52 + 10 = 62.", verifikasi={"ekspresi": "52 + 10", "hasil": "62"})
mc("c3", "sedang", K, Pr, S4, "Berapakah bilangan setelah 16 pada loncat mundur 2?", ["14", "15", "12", "13"], "A", "16 - 2 = 14.", verifikasi={"ekspresi": "16 - 2", "hasil": "14"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa pola 2, 4, 6, 8 selalu menghasilkan bilangan genap?", ["karena bilangan genap ditambah 2 selalu menghasilkan genap", "karena angkanya kecil", "karena loncatnya 4", "karena tidak ada angka 0"], "A", "Genap + genap (2) selalu menghasilkan bilangan genap.")
mc("c4", "sedang", T, Kn, S2, "Manakah dari bilangan berikut yang BUKAN anggota loncat 5 dari 5?", ["27", "25", "30", "35"], "A", "27 bukan kelipatan 5 karena satuannya bukan 5 atau 0.")
tf("c4", "sedang", T, Kn, S3, "Jika mulai dari 8, loncat 10 kedua adalah bilangan 38.", "Salah", "Loncat 10 kedua dari 8 adalah 8 + 20 = 28, bukan 38.")
tf("c4", "sedang", T, Kn, S4, "Urutan 80, 75, 70, 65 adalah pola loncat maju 5.", "Salah", "Nilainya berkurang, jadi loncat mundur 5, bukan maju.")
sa("c4", "sedang", T, Kn, S4, "Berapakah bilangan setelah 60 pada loncat mundur 10?", "50", "60 - 10 = 50.", verifikasi={"ekspresi": "60 - 10", "hasil": "50"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Katak melompat 2 langkah sebanyak 5 kali dari 0. Di mana katak?", ["10", "8", "12", "7"], "A", "0 + (5 x 2) = 10.", verifikasi={"ekspresi": "5 * 2", "hasil": "10"})
mc("c4", "sedang", X, Kn, S3, "Ada pola: 23, 33, 43, ..., 63. Angka yang hilang adalah ....", ["53", "50", "55", "52"], "A", "43 + 10 = 53.", verifikasi={"ekspresi": "43 + 10", "hasil": "53"})
tf("c4", "sedang", X, Kn, S2, "Semua bilangan loncat 5 yang berakhiran 0 adalah bilangan genap.", "Benar", "Bilangan berakhiran 0 selalu genap.")
mc("c4", "sulit", X, Me, S4, "Lina mulai dari 50, mundur 5 sebanyak 4 kali. Di angka berapa Lina?", ["30", "35", "25", "40"], "A", "50 - (4 x 5) = 50 - 20 = 30.", verifikasi={"ekspresi": "50 - (4 * 5)", "hasil": "30"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Berapa banyak lompatan loncat 2 dari 10 untuk mencapai 20?", ["5 lompatan", "4 lompatan", "6 lompatan", "10 lompatan"], "A", "(20 - 10) : 2 = 10 : 2 = 5 lompatan.", verifikasi={"ekspresi": "(20 - 10) / 2", "hasil": "5"})
mc("c4", "sulit", K, Me, S2, "Berapa banyak lompatan loncat 5 dari 15 untuk mencapai 45?", ["6 lompatan", "5 lompatan", "7 lompatan", "8 lompatan"], "A", "(45 - 15) : 5 = 30 : 5 = 6 lompatan.", verifikasi={"ekspresi": "(45 - 15) / 5", "hasil": "6"})
tf("c4", "sulit", K, Me, S4, "Membilang mundur 10 dari 90 sebanyak 4 kali menghasilkan angka 50.", "Benar", "90 - (4 x 10) = 90 - 40 = 50.")
mc("c4", "sulit", K, Me, S3, "Mulai dari 15, loncat 10 maju sebanyak 5 kali. Berapakah hasilnya?", ["65", "55", "75", "60"], "A", "15 + (5 x 10) = 15 + 50 = 65.", verifikasi={"ekspresi": "15 + (5 * 10)", "hasil": "65"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Budi mulai dari 40 loncat maju 2 sebanyak 7 kali. Angka berapakah itu?", ["54", "52", "56", "50"], "A", "40 + (7 x 2) = 40 + 14 = 54.", verifikasi={"ekspresi": "40 + (7 * 2)", "hasil": "54"})
mc("c5", "sedang", T, Me, S2, "Siti loncat 5 dari 20 sampai 55. Berapa kali Siti melompat?", ["7 kali", "6 kali", "8 kali", "5 kali"], "A", "(55 - 20) : 5 = 35 : 5 = 7 kali.", verifikasi={"ekspresi": "(55 - 20) / 5", "hasil": "7"})
mc("c5", "sedang", T, Me, S3, "Doni mulai dari 85 loncat mundur 10 sebanyak 5 kali. Angka berapakah?", ["35", "45", "25", "30"], "A", "85 - (5 x 10) = 85 - 50 = 35.", verifikasi={"ekspresi": "85 - (5 * 10)", "hasil": "35"})
mc("c5", "sulit", T, Me, S4, "Berapakah hasil dari (loncat 5 ke-4 dari 0) + (loncat 10 ke-3 dari 0)?", ["50", "45", "55", "40"], "A", "(4 x 5) + (3 x 10) = 20 + 30 = 50.", verifikasi={"ekspresi": "(4 * 5) + (3 * 10)", "hasil": "50"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Pola: 10, 15, ..., 25, 30. Angka pada titik-titik adalah ....", ["20", "18", "22", "24"], "A", "15 + 5 = 20.", verifikasi={"ekspresi": "15 + 5", "hasil": "20"})
mc("c5", "sulit", K, Me, S4, "Berapa selisih mundur 10 kedua dari 100 dengan maju 5 ketiga dari 50?", ["15", "10", "20", "25"], "A", "(100 - 20) - (50 + 15) = 80 - 65 = 15.", verifikasi={"ekspresi": "(100 - 20) - (50 + 15)", "hasil": "15"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Mengapa membilang loncat 10 jauh lebih cepat daripada membilang satu-satu?", ["karena langsung melompati 10 bilangan dalam satu langkah", "karena angkanya lebih bagus", "karena tidak perlu berpikir", "karena semua bilangan sama"], "A", "Setiap langkah langsung merangkum sepuluh satuan sekaligus.")
mc("c6", "sulit", K, Me, S4, "Katak loncat maju 2 sebanyak 10 kali, lalu mundur 5 sebanyak 2 kali. Posisi?", ["10", "12", "8", "15"], "A", "(10 x 2) - (2 x 5) = 20 - 10 = 10.", verifikasi={"ekspresi": "(10 * 2) - (2 * 5)", "hasil": "10"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil dari (20 + 40) ditambah (45 - 15)!", ["90", "85", "95", "80"], "A", "(20 + 40) + (45 - 15) = 60 + 30 = 90.", verifikasi={"ekspresi": "(20 + 40) + (45 - 15)", "hasil": "90"})
mc("c6", "sulit", P, Me, S3, "Berapa banyak bilangan persekutuan antara loncat 2 dan loncat 5 dari 1 sampai 50?", ["5 bilangan", "4 bilangan", "6 bilangan", "10 bilangan"], "A", "Kelipatan 10 dari 1 sampai 50 adalah 10, 20, 30, 40, 50 (ada 5 bilangan).", verifikasi={"ekspresi": "50 // 10", "hasil": "5"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab57_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab57.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
