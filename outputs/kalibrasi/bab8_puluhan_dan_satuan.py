#!/usr/bin/env python3
"""
Generator dan validator Bab 8 Matematika Kelas 1 SD:
"Puluhan dan Satuan" (Fase A)
bab_id: c018cc02-7ddd-41af-a7d3-fcbe4ec43f61
article_id: feafc303-3677-407e-8aad-a0b02dada28f
quiz_id: d76ba572-00dc-4b90-b1bc-3149e12bf549
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a8b7c69d9e01"  # Mengenal Nilai Tempat
S2 = "b9c8d70e0f12"  # Mengurai Bilangan Dua Angka
S3 = "c0d9e81f1a23"  # Menyusun Puluhan dan Satuan
S4 = "d1e0f92a2b34"  # Makna Nilai Setiap Angka

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Bilangan dua angka punya dua kamar.
Kamar kiri untuk puluhan.
Kamar kanan untuk satuan.
Lihatlah angka 24.
Angka 2 menempati nilai puluhan.
Angka 4 menempati nilai satuan.
Kamar kiri selalu puluhan.
Kamar kanan selalu satuan.

:::definition
title: Nilai Tempat
Nilai tempat menunjukkan posisi puluhan dan satuan.
:::"""

s2_content = """Kita bisa mengurai bilangan.
Ambil contoh angka 35.
Ada tiga ikat puluhan.
Ada lima stik satuan.
Jadi 35 adalah 3 puluhan.
Ditambah dengan 5 satuan.
3 puluhan nilainya 30.
5 satuan nilainya 5."""

s3_content = """Sekarang kita susun bilangannya.
Ada 4 puluhan dan 2 satuan.
4 puluhan nilainya 40.
2 satuan nilainya 2.
Kita gabungkan menjadi 42.
Contoh lain 6 puluhan dan 7 satuan.
Bilangan itu adalah 67.
Sangat mudah dan seru."""

s4_content = """Perhatikan nilai setiap angka.
Tempat menentukan nilainya.
Pada 72 angka 7 bernilai 70.
Angka 2 bernilai 2.

:::common_trap
title: Menilai Angka Tanpa Memperhatikan Tempatnya
Pada angka 53, angka 5 bernilai 50 bukan 5.
Angka di depan selalu bernilai puluhan.
Angka di belakang bernilai satuan.
Tempat angka menentukan besar nilainya.
:::

:::callout
variant: summary
title: Ringkasan
text: Angka depan adalah puluhan. Angka belakang adalah satuan. Tempat menentukan nilainya.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Nilai Tempat",
        "minutes": 6,
        "goal": "Siswa dapat mengenali posisi puluhan (kiri) dan satuan (kanan) pada bilangan dua angka.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengurai Bilangan Dua Angka",
        "minutes": 6,
        "goal": "Siswa dapat menguraikan bilangan dua angka menjadi puluhan dan satuan.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Menyusun Puluhan dan Satuan",
        "minutes": 6,
        "goal": "Siswa dapat menyusun bilangan dua angka dari nilai puluhan dan satuan yang diketahui.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Makna Nilai Setiap Angka",
        "minutes": 6,
        "goal": "Siswa dapat menentukan nilai sebenarnya dari angka puluhan dan satuan sesuai posisinya.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Puluhan dan Satuan",
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
# 2. DEFINISI BANK 50 SOAL BAB 8
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
mc("c1", "mudah", D, F, S1, "Pada bilangan dua angka, angka di sebelah kiri adalah ....", ["puluhan", "satuan", "ratusan", "nol"], "A", "Angka sebelah kiri bernilai puluhan.")
tf("c1", "mudah", D, F, S1, "Angka sebelah kanan bernilai puluhan.", "Salah", "Angka sebelah kanan bernilai satuan.")

# Terarah (3): S1, S2, S4
mc("c1", "mudah", T, F, S1, "Nilai tempat angka 6 pada bilangan 62 adalah ....", ["puluhan", "satuan", "ratusan", "ribuan"], "A", "Angka 6 di sebelah kiri menempati nilai puluhan.")
mc("c1", "mudah", T, F, S2, "Bilangan 46 diurai menjadi 4 puluhan ditambah ....", ["6 satuan", "4 satuan", "60 satuan", "1 satuan"], "A", "46 adalah 4 puluhan ditambah 6 satuan.")
sa("c1", "mudah", T, F, S4, "Berapakah nilai angka 7 pada bilangan 70?", "70|tujuh puluh", "Angka 7 di tempat puluhan bernilai 70.", verifikasi={"ekspresi": "7 * 10", "hasil": "70"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Bilangan 37 terdiri dari ....", ["3 puluhan dan 7 satuan", "7 puluhan dan 3 satuan", "30 puluhan dan 7 satuan", "3 satuan dan 7 puluhan"], "A", "37 terdiri dari 3 puluhan dan 7 satuan.")
tf("c2", "mudah", D, Kn, S4, "Angka 4 pada bilangan 48 bernilai 40.", "Benar", "Angka 4 di posisi puluhan bernilai 40.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Pada angka 25, angka yang menempati puluhan adalah ....", ["2", "5", "20", "25"], "A", "Angka 2 di depan adalah angka puluhannya.", "Salah membedakan angka dengan nilainya pada puluhan", verifikasi={"ekspresi": "25 // 10", "hasil": "2"})
mc("c2", "mudah", R, F, S4, "Angka 5 pada bilangan 53 bernilai ....", ["50", "5", "30", "53"], "A", "Angka 5 menempati puluhan bernilai 50.", "Angka puluhan hanya bernilai satuannya saja", verifikasi={"ekspresi": "5 * 10", "hasil": "50"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S2, "Bilangan 20 dapat diurai menjadi ....", ["2 puluhan dan 0 satuan", "2 satuan dan 0 puluhan", "20 puluhan", "0 puluhan dan 2 satuan"], "A", "20 terdiri dari 2 puluhan dan 0 satuan.")
mc("c2", "mudah", T, Kn, S3, "Susunan dari 3 puluhan dan 5 satuan adalah ....", ["35", "53", "305", "8"], "A", "3 puluhan dan 5 satuan disusun menjadi 35.", verifikasi={"ekspresi": "30 + 5", "hasil": "35"})
tf("c2", "mudah", T, Kn, S1, "Nilai tempat angka 9 pada 59 adalah puluhan.", "Salah", "Angka 9 menempati posisi satuan di kanan.")
sa("c2", "mudah", T, F, S4, "Berapakah nilai angka satuan pada bilangan 83?", "3|tiga", "Nilai angka 3 di posisi satuan adalah 3.", verifikasi={"ekspresi": "83 % 10", "hasil": "3"})

# ── C3 MUDAH (2 soal: 2 terarah) ──────────────────────────────────────────
# Terarah (2): S1, S3
mc("c3", "mudah", T, Pr, S1, "Manakah bilangan yang angka satuannya 8?", ["28", "82", "80", "180"], "A", "Pada 28, angka 8 berada di posisi satuan.")
sa("c3", "mudah", T, Pr, S3, "Berapakah hasil gabungan 4 puluhan dan 2 satuan?", "42|empat puluh dua", "4 puluhan (40) dan 2 satuan (2) menjadi 42.", verifikasi={"ekspresi": "40 + 2", "hasil": "42"})

# ── C3 SEDANG (12 soal: 4 checkpoint, 2 remedial, 6 terarah) ──────────────
# Checkpoint akhir (4)
mc("c3", "sedang", K, Pr, S2, "Berapakah banyak puluhan pada bilangan 78?", ["7", "8", "70", "80"], "A", "Pada 78 ada 7 puluhan.", verifikasi={"ekspresi": "78 // 10", "hasil": "7"})
mc("c3", "sedang", K, Pr, S3, "Susunan dari 8 puluhan dan 0 satuan adalah ....", ["80", "8", "800", "18"], "A", "8 puluhan dan 0 satuan bernilai 80.", verifikasi={"ekspresi": "8 * 10", "hasil": "80"})
tf("c3", "sedang", K, Kn, S2, "Bilangan 65 terdiri dari 6 puluhan dan 5 satuan.", "Benar", "65 = 6 puluhan + 5 satuan.")
tf("c3", "sedang", K, Pr, S4, "Angka 3 pada bilangan 73 bernilai 30.", "Salah", "Angka 3 menempati posisi satuan bernilai 3.")

# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Ani menyusun 6 puluhan dan 7 satuan menjadi 76. Ani salah karena ....", ["menukar posisi puluhan dan satuan", "kurang satuannya", "satuannya terlalu besar", "sudah benar"], "A", "Puluhan harus di depan, jadi seharusnya 67 bukan 76.", "Tertukar urutan menulis puluhan dan satuan")
mc("c3", "sedang", R, Kn, S4, "Berapakah nilai sebenarnya dari angka 8 pada 81?", ["80", "8", "1", "18"], "A", "Angka 8 menempati puluhan sehingga bernilai 80.", "Menganggap angka puluhan bernilai satuan", verifikasi={"ekspresi": "8 * 10", "hasil": "80"})

# Terarah (6): S1, S2, S2, S3, S3, S4
mc("c3", "sedang", T, Pr, S1, "Manakah bilangan yang angka puluhannya 5?", ["54", "45", "15", "5"], "A", "Pada 54, angka 5 berada di sebelah kiri.")
mc("c3", "sedang", T, Pr, S2, "Berapa banyak satuan pada bilangan 94?", ["4", "9", "40", "90"], "A", "Angka satuan di kanan adalah 4.", verifikasi={"ekspresi": "94 % 10", "hasil": "4"})
mc("c3", "sedang", T, Pr, S2, "Bilangan 50 memiliki berapa puluhan?", ["5", "0", "50", "15"], "A", "Bilangan 50 memiliki 5 puluhan.", verifikasi={"ekspresi": "50 // 10", "hasil": "5"})
mc("c3", "sedang", T, Pr, S3, "Susunlah 6 puluhan dan 7 satuan!", ["67", "76", "607", "13"], "A", "6 puluhan dan 7 satuan menjadi 67.", verifikasi={"ekspresi": "60 + 7", "hasil": "67"})
tf("c3", "sedang", T, Kn, S3, "7 puluhan dan 1 satuan bernilai 71.", "Benar", "70 ditambah 1 menjadi 71.")
sa("c3", "sedang", T, Pr, S4, "Berapakah nilai angka 2 pada bilangan 92?", "2|dua", "Angka 2 di tempat satuan bernilai 2.", verifikasi={"ekspresi": "92 % 10", "hasil": "2"})

# ── C4 SEDANG (13 soal: 2 checkpoint, 4 mandiri, 7 terarah) ──────────────
# Checkpoint akhir (2)
mc("c4", "sedang", K, Kn, S4, "Berapakah selisih nilai angka 7 dan 2 pada 72?", ["68", "70", "2", "5"], "A", "Nilai 7 adalah 70 dan nilai 2 adalah 2. 70 - 2 = 68.", verifikasi={"ekspresi": "70 - 2", "hasil": "68"})
tf("c4", "sedang", K, Kn, S1, "Pada bilangan 33 kedua angka memiliki nilai yang sama.", "Salah", "Angka 3 kiri bernilai 30, angka 3 kanan bernilai 3.")

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Angka 7 pada 77 memiliki nilai tempat ....", ["puluhan dan satuan", "hanya puluhan", "hanya satuan", "ratusan"], "A", "7 di kiri puluhan, 7 di kanan satuan.")
mc("c4", "sedang", X, Kn, S2, "Jika 64 dikurangi 4 satuannya, sisanya adalah ....", ["60", "64", "4", "40"], "A", "64 dikurangi 4 satuan tersisa 6 puluhan bernilai 60.", verifikasi={"ekspresi": "64 - 4", "hasil": "60"})
mc("c4", "sedang", X, Kn, S3, "Bilangan yang terbentuk dari 9 puluhan dan 9 satuan adalah ....", ["99", "90", "18", "909"], "A", "9 puluhan dan 9 satuan disusun menjadi 99.", verifikasi={"ekspresi": "90 + 9", "hasil": "99"})
sa("c4", "sedang", X, Pr, S4, "Jika angka puluhan pada bilangan 56 dihilangkan, tersisa angka berapa?", "6|enam", "Tersisa satuannya yaitu 6.", verifikasi={"ekspresi": "56 - 50", "hasil": "6"})

# Terarah (7): S1, S1, S2, S2, S3, S3, S4
mc("c4", "sedang", T, Kn, S1, "Manakah bilangan yang memiliki angka puluhan lebih besar dari satuannya?", ["62", "26", "35", "18"], "A", "Pada 62, puluhannya 6 lebih besar dari satuannya 2.")
tf("c4", "sedang", T, Kn, S1, "Letak kamar menentukan besar nilai suatu angka.", "Benar", "Posisi puluhan bernilai sepuluh kali lipat dari satuan.")
mc("c4", "sedang", T, Kn, S2, "Bilangan 85 terdiri dari ....", ["8 puluhan dan 5 satuan", "5 puluhan dan 8 satuan", "80 puluhan dan 5 satuan", "85 puluhan"], "A", "85 terdiri dari 8 puluhan dan 5 satuan.")
tf("c4", "sedang", T, Kn, S2, "Bilangan 30 tidak memiliki nilai satuan sama sekali.", "Salah", "Bilangan 30 memiliki 0 satuan.")
mc("c4", "sedang", T, Kn, S3, "Ada 5 ikat lidi isi 10 dan 4 lidi lepas. Semua lidi ada ....", ["54", "45", "50", "9"], "A", "5 puluhan dan 4 satuan bernilai 54 lidi.", verifikasi={"ekspresi": "50 + 4", "hasil": "54"})
tf("c4", "sedang", T, Me, S3, "Menyusun bilangan dimulai dengan menulis puluhan di kiri.", "Benar", "Puluhan ditulis di kiri, satuan di kanan.")
mc("c4", "sedang", T, Me, S4, "Mengapa angka 5 pada 52 bernilai 50 bukan 5?", ["karena berada di kamar puluhan", "karena angkanya besar", "karena ditambah 2", "karena berwarna hitam"], "A", "Posisi di depan menentukan nilainya sebagai puluhan.")

# ── C5 SULIT (6 soal: 2 checkpoint, 4 mandiri) ───────────────────────────
# Checkpoint akhir (2)
mc("c5", "sulit", K, Me, S1, "Dito menulis bilangan tiga puluh empat menjadi 43. Apa kesalahan Dito?", ["menukar posisi puluhan dan satuan", "lupa menulis puluhan", "salah menghitung angka", "Dito sudah benar"], "A", "Dito menaruh 4 di depan, seharusnya 3 puluhan di depan.")
mc("c5", "sulit", K, Me, S4, "Mengapa nilai 8 pada 82 lebih besar daripada nilai 8 pada 28?", ["pada 82 bernilai 80, pada 28 bernilai 8", "karena 82 lebih panjang", "karena angka 8 di kanan", "tidak ada bedanya"], "A", "8 di posisi puluhan bernilai 80, sedangkan di posisi satuan bernilai 8.")

# Mandiri (4)
mc("c5", "sulit", X, Kn, S2, "Suatu bilangan memiliki 7 puluhan dan satuan 3 lebihnya dari 4. Bilangan itu adalah ....", ["77", "74", "73", "47"], "A", "Satuannya 4 + 3 = 7. Jadi bilangannya 77.", verifikasi={"ekspresi": "70 + 7", "hasil": "77"})
mc("c5", "sulit", X, Me, S4, "Ibu mengikat 5 ikat lidi isi sepuluh dan 3 lidi lepas. Berapakah nilai lidi yang diikat?", ["50", "5", "30", "3"], "A", "5 ikat lidi bernilai 50 buah lidi.", verifikasi={"ekspresi": "5 * 10", "hasil": "50"})
mc("c5", "sulit", X, Kn, S3, "Bilangan dua angka dengan puluhan 8 dan satuan terkecil adalah ....", ["80", "81", "89", "8"], "A", "Satuan terkecil adalah 0, jadi bilangannya 80.", verifikasi={"ekspresi": "80 + 0", "hasil": "80"})
mc("c5", "sulit", X, Kn, S4, "Jumlah nilai angka puluhan dan satuan pada 63 adalah ....", ["63", "9", "60", "36"], "A", "60 ditambah 3 menjadi 63.", verifikasi={"ekspresi": "60 + 3", "hasil": "63"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ──────────────────────────
# Checkpoint akhir (2)
mc("c6", "sulit", K, Me, S2, "Bagaimana cara membuktikan bilangan 45 lebih besar dari 39?", ["lihat puluhannya: 4 puluhan lebih besar dari 3 puluhan", "lihat satuannya saja", "karena 9 lebih besar dari 5", "tebak langsung"], "A", "Bandingkan nilai tempat tertinggi (puluhan) terlebih dahulu.")
mc("c6", "sulit", K, Kn, S3, "Rancanglah bilangan dua angka yang memiliki angka puluhan sama dengan satuannya!", ["55", "54", "50", "15"], "A", "Pada 55, puluhannya 5 dan satuannya juga 5.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Mengapa sistem nilai tempat sangat berguna dalam matematika?", ["agar nilai angka jelas berdasarkan posisinya", "agar angka terlihat indah", "agar lebih sulit dibaca", "hanya tradisi lama"], "A", "Nilai tempat memberi arti pasti pada setiap digit sesuai posisinya.")
mc("c6", "sulit", P, Pr, S4, "Temukan bilangan antara 60 dan 70 yang selisih nilai tempatnya adalah 56!", ["64", "62", "68", "66"], "A", "Pada 64, nilai puluhan 60 dan satuan 4. Selisihnya 60 - 4 = 56.")

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
    u = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab8_soal_{i}"))

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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab8.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
