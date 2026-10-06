#!/usr/bin/env python3
"""
Generator dan validator Bab 7 Matematika Kelas 1 SD:
"Membilang dan Membaca Bilangan sampai 100" (Fase A)
bab_id: 2cde690d-76dc-4571-b3da-eb5b75824eb0
article_id: 1d6424bc-6dfe-43d2-bb88-89d89944586e
quiz_id: c7479808-c2e1-4282-b149-ec3067a08a01
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a7b6c59d8e01"  # Membilang 21 sampai 40
S2 = "b8c7d60e9f12"  # Membilang 41 sampai 70
S3 = "c9d8e71f0a23"  # Membilang 71 sampai 100
S4 = "d0e9f82a1b34"  # Membaca Nama Bilangan dengan Jelas

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Setelah angka 20 kita membilang 21.
Dua puluh satu, lalu dua puluh dua.
Begitu seterusnya sampai angka 30.
Tiga puluh lalu tiga puluh satu.
Membilang teratur sangat mudah.
Pola angka selalu berulang.
Angka bertambah satu demi satu.
Kini kita bisa sampai 40."""

s2_content = """Ayo lanjut membilang lebih banyak.
Setelah 40 ada empat puluh satu.
Kelompok 50 disebut lima puluh.
Kelompok 60 disebut enam puluh.
Kelompok 70 disebut tujuh puluh.
Ucapkan nama puluhan dengan jelas.
Lalu sebut angka satuannya.

:::definition
title: Bilangan Puluhan Utuh
Puluhan utuh berakhiran angka nol.
:::"""

s3_content = """Ayo melangkah menuju seratus.
Tujuh puluh, delapan puluh, sembilan puluh.
Setelah 99 ada angka 100.
Angka 100 dibaca seratus.
Seratus memiliki tiga angka.
Ada satu dan dua nol.
Kita sudah membilang sampai seratus.
Luar biasa, kamu makin hebat."""

s4_content = """Membaca bilangan harus teliti.
Jangan tertukar belasan dan puluhan.
Angka 15 dibaca lima belas.
Angka 50 dibaca lima puluh.
Dengarkan bunyi akhir katanya.

:::common_trap
title: Tertukar Belasan dan Puluhan Saat Membaca
Angka 14 dibaca empat belas.
Angka 40 dibaca empat puluh.
Belasan memiliki angka satu di depan.
Puluhan diakhiri kata puluh.
:::

:::callout
variant: summary
title: Ringkasan
text: Bilangan sampai 100 dibaca teratur. Bedakan kata belasan dan puluhan.
:::"""

sections = [
    {
        "id": S1,
        "title": "Membilang 21 sampai 40",
        "minutes": 6,
        "goal": "Siswa dapat membilang secara teratur bilangan 21 sampai 40.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Membilang 41 sampai 70",
        "minutes": 6,
        "goal": "Siswa dapat membilang secara teratur bilangan 41 sampai 70 dan mengenali nama puluhannya.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membilang 71 sampai 100",
        "minutes": 6,
        "goal": "Siswa dapat membilang bilangan 71 sampai 100 dan mengenal bilangan seratus.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Membaca Nama Bilangan dengan Jelas",
        "minutes": 6,
        "goal": "Siswa dapat membaca nama bilangan dua angka dengan tepat tanpa tertukar belasan dan puluhan.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membilang dan Membaca Bilangan sampai 100",
    "topic": "Bilangan sampai 100 dan Nilai Tempat",
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
# 2. DEFINISI BANK 50 SOAL BAB 7
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
mc("c1", "mudah", D, F, S1, "Angka setelah 20 adalah ....", ["21", "22", "19", "25"], "A", "Setelah angka 20 adalah 21.", verifikasi={"ekspresi": "20 + 1", "hasil": "21"})
tf("c1", "mudah", D, F, S4, "Angka 14 dibaca empat puluh.", "Salah", "Angka 14 dibaca empat belas, bukan empat puluh.")

# Terarah (3): S1, S2, S4
mc("c1", "mudah", T, F, S1, "Angka 25 dibaca ....", ["dua puluh lima", "lima puluh dua", "dua puluh", "dua lima"], "A", "Angka 25 dibaca dua puluh lima.")
mc("c1", "mudah", T, F, S2, "Angka 60 dibaca ....", ["enam puluh", "enam belas", "enam ratus", "enam"], "A", "Angka 60 dibaca enam puluh.")
sa("c1", "mudah", T, F, S4, "Tulis angka untuk tiga puluh!", "30|tiga puluh", "Tiga puluh ditulis dengan angka 30.", verifikasi={"ekspresi": "30", "hasil": "30"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Bilangan tepat setelah 99 adalah ....", ["100", "98", "90", "89"], "A", "Setelah angka 99 adalah 100.", verifikasi={"ekspresi": "99 + 1", "hasil": "100"})
tf("c2", "mudah", D, Kn, S2, "Angka 50 dibaca lima puluh.", "Benar", "Angka 50 memang dibaca lima puluh.")

# Remedial (2)
mc("c2", "mudah", R, F, S4, "Manakah lambang angka untuk empat puluh?", ["40", "14", "4", "44"], "A", "Empat puluh ditulis 40, bukan 14.", "Tertukar belasan 14 dengan puluhan 40", verifikasi={"ekspresi": "40", "hasil": "40"})
mc("c2", "mudah", R, Kn, S1, "Angka 31 dibaca ....", ["tiga puluh satu", "tiga belas", "tiga puluh", "tiga puluh tiga"], "A", "31 dibaca tiga puluh satu.", "Salah membaca angka satuan pada puluhan")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S2, "Angka 47 dibaca ....", ["empat puluh tujuh", "tujuh puluh empat", "empat belas", "empat puluh"], "A", "Angka 47 dibaca empat puluh tujuh.")
mc("c2", "mudah", T, Kn, S3, "Angka 100 dibaca ....", ["seratus", "sepuluh", "seribu", "satu ratus"], "A", "Angka 100 dibaca seratus.")
tf("c2", "mudah", T, Kn, S4, "Angka 17 dan 70 dibaca sama.", "Salah", "17 dibaca tujuh belas, sedangkan 70 dibaca tujuh puluh.")
sa("c2", "mudah", T, F, S1, "Tulis angka untuk dua puluh delapan!", "28|dua puluh delapan", "Dua puluh delapan ditulis 28.", verifikasi={"ekspresi": "28", "hasil": "28"})

# ── C3 MUDAH (2 soal: 2 terarah) ──────────────────────────────────────────
# Terarah (2): S1, S3
mc("c3", "mudah", T, Pr, S1, "Lanjutan urutan: 21, 22, 23, ....", ["24", "25", "20", "22"], "A", "Setelah 23 adalah 24.", verifikasi={"ekspresi": "23 + 1", "hasil": "24"})
sa("c3", "mudah", T, Pr, S3, "Lanjutan urutan: 71, 72, 73, ....", "74|tujuh puluh empat", "Setelah 73 adalah 74.", verifikasi={"ekspresi": "73 + 1", "hasil": "74"})

# ── C3 SEDANG (12 soal: 4 checkpoint, 2 remedial, 6 terarah) ──────────────
# Checkpoint akhir (4)
mc("c3", "sedang", K, Pr, S1, "Urutan mundur: 40, 39, 38, ....", ["37", "36", "41", "35"], "A", "Mundur satu langkah setelah 38 adalah 37.", verifikasi={"ekspresi": "38 - 1", "hasil": "37"})
mc("c3", "sedang", K, Pr, S2, "Lanjutan urutan maju: 68, 69, ....", ["70", "67", "80", "71"], "A", "Setelah 69 adalah 70.", verifikasi={"ekspresi": "69 + 1", "hasil": "70"})
tf("c3", "sedang", K, Kn, S3, "Angka 100 tersusun dari 3 angka.", "Benar", "Angka 100 tersusun dari angka 1, 0, dan 0.")
tf("c3", "sedang", K, Pr, S4, "Angka 80 dibaca delapan belas.", "Salah", "Angka 80 dibaca delapan puluh.")

# Remedial (2)
mc("c3", "sedang", R, Pr, S4, "Budi membaca 23 menjadi tiga puluh dua. Budi harus ....", ["membaca angka puluhan kiri dulu", "membaca dari kanan", "menambahkan kata belas", "menebak saja"], "A", "Baca angka 2 di depan (dua puluh) baru angka 3.", "Membaca angka puluhan terbalik dari kanan ke kiri")
mc("c3", "sedang", R, Kn, S4, "Angka lima puluh delapan ditulis ....", ["58", "85", "508", "15"], "A", "Lima puluh delapan ditulis 58.", "Menulis angka terbalik puluhan dan satuan", verifikasi={"ekspresi": "58", "hasil": "58"})

# Terarah (6): S1, S2, S2, S3, S3, S4
mc("c3", "sedang", T, Pr, S1, "Urutan maju: 31, 32, ..., 34.", ["33", "35", "30", "36"], "A", "Angka di antara 32 dan 34 adalah 33.", verifikasi={"ekspresi": "32 + 1", "hasil": "33"})
mc("c3", "sedang", T, Pr, S2, "Lanjutan urutan puluhan: 40, 50, ....", ["60", "70", "45", "55"], "A", "Lompat sepuluh setelah 50 adalah 60.", verifikasi={"ekspresi": "50 + 10", "hasil": "60"})
mc("c3", "sedang", T, Pr, S2, "Lanjutan urutan: 58, 59, ....", ["60", "57", "70", "61"], "A", "Setelah 59 adalah 60.", verifikasi={"ekspresi": "59 + 1", "hasil": "60"})
mc("c3", "sedang", T, Pr, S3, "Urutan angka maju: 87, 88, 89, ....", ["90", "91", "80", "92"], "A", "Setelah 89 adalah 90.", verifikasi={"ekspresi": "89 + 1", "hasil": "90"})
tf("c3", "sedang", T, Kn, S3, "Bilangan 99 adalah bilangan 2 angka terbesar.", "Benar", "Setelah 99 adalah 100 yang memiliki 3 angka.")
sa("c3", "sedang", T, Pr, S4, "Tulis lambang angka untuk enam puluh empat!", "64|enam puluh empat", "Enam puluh empat ditulis 64.", verifikasi={"ekspresi": "64", "hasil": "64"})

# ── C4 SEDANG (13 soal: 2 checkpoint, 4 mandiri, 7 terarah) ──────────────
# Checkpoint akhir (2)
mc("c4", "sedang", K, Kn, S2, "Ada 6 ikat permen. Tiap ikat isi 10. Berapa permen?", ["60", "16", "6", "26"], "A", "6 puluhan bernilai 60 permen.", verifikasi={"ekspresi": "6 * 10", "hasil": "60"})
tf("c4", "sedang", K, Kn, S4, "Angka 15 dan 51 memiliki nilai yang sama.", "Salah", "15 bernilai lima belas, sedangkan 51 bernilai lima puluh satu.")

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Bilangan tepat di antara 35 dan 37 adalah ....", ["36", "38", "34", "39"], "A", "Di antara 35 dan 37 adalah 36.", verifikasi={"ekspresi": "35 + 1", "hasil": "36"})
mc("c4", "sedang", X, Kn, S2, "Bilangan di antara 50 dan 53 adalah ....", ["51 dan 52", "49 dan 50", "53 dan 54", "54 dan 55"], "A", "Di antara 50 dan 53 adalah 51 dan 52.")
mc("c4", "sedang", X, Kn, S3, "Lengkapi urutan puluhan: 70, 80, ..., 100.", ["90", "85", "95", "89"], "A", "Pola puluhan melompat sepuluh: 70, 80, 90, 100.", verifikasi={"ekspresi": "80 + 10", "hasil": "90"})
sa("c4", "sedang", X, Pr, S1, "Berapa hasil hitungan mundur satu langkah dari 30?", "29|dua puluh sembilan", "Mundur satu langkah dari 30 adalah 29.", verifikasi={"ekspresi": "30 - 1", "hasil": "29"})

# Terarah (7): S1, S1, S2, S2, S3, S3, S4
mc("c4", "sedang", T, Kn, S1, "Bilangan tepat di antara 38 dan 40 adalah ....", ["39", "37", "41", "36"], "A", "Di antara 38 dan 40 adalah 39.", verifikasi={"ekspresi": "38 + 1", "hasil": "39"})
tf("c4", "sedang", T, Kn, S1, "Urutan membilang maju nilainya bertambah.", "Benar", "Setiap maju satu langkah, bilangan bertambah 1.")
mc("c4", "sedang", T, Kn, S2, "Pola puluhan: 30, 40, 50, .... Angka berikutnya?", ["60", "70", "51", "55"], "A", "Pola lompat 10 berikutnya adalah 60.", verifikasi={"ekspresi": "50 + 10", "hasil": "60"})
tf("c4", "sedang", T, Kn, S2, "Angka 45 lebih kecil daripada 40.", "Salah", "45 lebih besar daripada 40.")
mc("c4", "sedang", T, Kn, S3, "Urutan bilangan yang benar dari kecil ke besar adalah ....", ["78, 79, 80", "80, 79, 78", "79, 78, 80", "78, 80, 79"], "A", "Urutan yang benar dari kecil adalah 78, 79, lalu 80.")
tf("c4", "sedang", T, Me, S3, "Menghitung puluhan lebih cepat daripada satu demi satu.", "Benar", "Mengelompokkan sepuluh-sepuluh membuat hitungan lebih cepat.")
mc("c4", "sedang", T, Me, S4, "Mengapa kita menyebut empat belas bukan empat puluh?", ["ada angka 1 di depan bernilai sepuluh", "karena angkanya lebih besar", "karena ada angka nol di belakang", "karena sama bunyinya"], "A", "Empat belas diawali angka 1 yang bernilai sepuluh.")

# ── C5 SULIT (6 soal: 2 checkpoint, 4 mandiri) ───────────────────────────
# Checkpoint akhir (2)
mc("c5", "sulit", K, Me, S2, "Budi membilang: 48, 49, 60. Apa kesalahan Budi?", ["setelah 49 seharusnya 50", "setelah 49 seharusnya 40", "seharusnya membilang mundur", "Budi sudah benar"], "A", "Setelah kelompok empat puluhan berakhir di 49, masuk ke 50.")
mc("c5", "sulit", K, Me, S4, "Temanmu ragu membaca angka 90. Cara membantunya?", ["sebut angka 9 lalu beri kata puluh", "sebut sembilan belas", "sebut sembilan nol", "sebut seratus"], "A", "Angka 9 dengan 0 di belakang dibaca sembilan puluh.")

# Mandiri (4)
mc("c5", "sulit", X, Kn, S1, "Manakah yang bernilai lebih banyak: 34 atau 43?", ["43", "34", "sama banyak", "tidak tahu"], "A", "43 memiliki 4 puluhan sehingga lebih banyak dari 34.", verifikasi={"ekspresi": "40 + 3", "hasil": "43"})
mc("c5", "sulit", X, Me, S4, "Siti membaca 16 sebagai enam puluh. Apa sarannya?", ["ingat angka 1 di depan adalah belasan", "sudah benar", "baca dari belakang", "ganti angkanya"], "A", "Angka 1 di depan dibaca belasan, jadi 16 adalah enam belas.")
mc("c5", "sulit", X, Kn, S3, "Bilangan yang tepat sebelum seratus adalah ....", ["99", "90", "101", "98"], "A", "Tepat sebelum 100 adalah 99.", verifikasi={"ekspresi": "100 - 1", "hasil": "99"})
mc("c5", "sulit", X, Kn, S4, "Perbedaan angka 27 dan 72 adalah ....", ["27 dua puluhan, 72 tujuh puluhan", "hanya beda warna", "nilainya persis sama", "tidak ada perbedaan"], "A", "27 bernilai dua puluh tujuh, 72 bernilai tujuh puluh dua.")

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ──────────────────────────
# Checkpoint akhir (2)
mc("c6", "sulit", K, Me, S3, "Cara membilang 100 biji jagung paling cepat adalah ....", ["kelompokkan tiap 10 biji lalu hitung puluhannya", "hitung satu per satu pelan-pelan", "tebak saja tanpa dihitung", "hitung dua per dua"], "A", "Mengelompokkan tiap 10 biji membuat hitungan cepat dan rapi.")
mc("c6", "sulit", K, Kn, S4, "Buatlah kesimpulan tentang bilangan puluhan utuh!", ["selalu berakhiran angka nol", "selalu berakhiran angka lima", "selalu memiliki tiga angka", "tidak ada aturannya"], "A", "Puluhan utuh (10, 20, 30, dst.) selalu berakhiran angka 0.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Mengapa bilangan seratus disebut bilangan 3 angka?", ["karena ada satu angka 1 dan dua angka 0", "karena nilainya paling sedikit", "hanya kebetulan saja", "karena dibaca seratus"], "A", "100 memiliki tiga digit penyusun yaitu 1, 0, dan 0.")
mc("c6", "sulit", P, Pr, S2, "Urutan lompat 10 dari 10 sampai 100 adalah ....", ["10, 20, 30, 40, 50, 60, 70, 80, 90, 100", "10, 15, 20, 25, 30", "10, 30, 50, 70, 90", "10, 100"], "A", "Pola lompat 10 dari 10 berlanjut 20, 30, sampai 100.")

# ==========================================
# 3. VERIFIKASI & GENERASI STRUKTUR APLIKASI
# ==========================================
assert len(Q) == 50, f"Total soal: {len(Q)} != 50"

mc_list, tf_list, sa_list = [], [], []

for i, q in enumerate(Q, 1):
    tax = {
        "bloom": q["b"],
        "difficulty": q["d"],
        "fungsi": q["f"],
        "knowledge_dimension": q["dim"]
    }
    if q.get("m"):
        tax["miskonsepsi_target"] = q["m"]

    # Deterministic UUID5
    u = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab7_soal_{i}"))

    base = {
        "uid": u,
        "number": i,
        "taxonomy": tax,
        "source_section_id": q["s"],
        "explanation": q["ex"]
    }
    if q.get("verifikasi"):
        base["verifikasi"] = q["verifikasi"]

    if q["t"] == "mc":
        opts = list(q["opts"])
        correct_text = opts[0]
        random.shuffle(opts)
        choices = [{"label": L, "text": opt} for L, opt in zip(["A", "B", "C", "D"], opts)]
        ans_label = next(c["label"] for c in choices if c["text"] == correct_text)
        base["stem"] = q["stem"]
        base["choices"] = choices
        base["answer"] = ans_label
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
types = Counter(q["taxonomy"]["fungsi"] for q in all_q)

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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab7.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
