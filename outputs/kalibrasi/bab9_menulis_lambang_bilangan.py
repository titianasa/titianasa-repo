#!/usr/bin/env python3
"""
Generator dan validator Bab 9 Matematika Kelas 1 SD:
"Menulis Lambang Bilangan sampai 100" (Fase A)
bab_id: e24feefc-bd12-4545-8318-e46aa9dc010d
article_id: ef60751c-40f7-4060-80f1-28118ef54444
quiz_id: 5c891089-1ec6-46c9-9b27-561eb9714e2c
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a9b8c79d0e01"  # Dari Kata ke Lambang Angka
S2 = "b0c9d80e1f12"  # Menulis Puluhan Utuh
S3 = "c1d0e91f2a23"  # Menulis Bilangan Campuran
S4 = "d2e1f02a3b34"  # Menulis Angka Seratus

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Kita sering mendengar nama bilangan.
Sekarang kita tulis lambang angkanya.
Dengar kata puluhannya terlebih dahulu.
Lalu dengar kata satuannya.
Dua puluh tiga ditulis 23.
Angka 2 di depan.
Angka 3 di belakang.
Menulis angka itu sangat mudah.

:::definition
title: Lambang Angka
Lambang angka adalah tanda bertulis untuk menyatakan bilangan.
:::"""

s2_content = """Ayo tulis puluhan utuh.
Puluhan utuh berakhiran angka nol.
Empat puluh ditulis 40.
Enam puluh ditulis 60.
Delapan puluh ditulis 80.
Sembilan puluh ditulis 90.
Hanya ada satu angka nol.
Jangan buat nol berlebih."""

s3_content = """Hati-hati menulis bilangan campuran.
Tiga puluh lima ditulis 35.
Bukan ditulis 305.
Angka 5 menggantikan nol.
Tujuh puluh dua ditulis 72.
Ada dua angka saja.
Tulis puluhan lalu satuan.
Hasil tulisanmu rapi sekali."""

s4_content = """Sekarang kita tulis angka 100.
Seratus memiliki tiga angka.
Tulis angka satu di depan.
Lalu tulis dua angka nol.
Lambangnya adalah 100.

:::common_trap
title: Menulis Nol Tambahan pada Bilangan Dua Angka
Tiga puluh lima ditulis 35 bukan 305.
Angka satuan menggantikan angka nol puluhan.
Jangan sisipkan angka nol di tengah.
Bilangan dua angka hanya punya dua digit.
:::

:::callout
variant: summary
title: Ringkasan
text: Tulis puluhan lalu satuan. Jangan sisipkan nol di tengah. Seratus ditulis 100.
:::"""

sections = [
    {
        "id": S1,
        "title": "Dari Kata ke Lambang Angka",
        "minutes": 6,
        "goal": "Siswa dapat menulis lambang angka dari nama bilangan yang didengar atau dibaca.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Menulis Puluhan Utuh",
        "minutes": 6,
        "goal": "Siswa dapat menuliskan bilangan puluhan utuh yang berakhiran satu angka nol.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Menulis Bilangan Campuran",
        "minutes": 6,
        "goal": "Siswa dapat menulis bilangan dua angka tanpa menyelipkan angka nol tambahan di tengah.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menulis Angka Seratus",
        "minutes": 6,
        "goal": "Siswa dapat menuliskan lambang bilangan seratus (100) dengan tepat.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Menulis Lambang Bilangan sampai 100",
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
# 2. DEFINISI BANK 50 SOAL BAB 9
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
mc("c1", "mudah", D, F, S1, "Lambang angka untuk dua puluh tiga adalah ....", ["23", "32", "203", "20"], "A", "Dua puluh tiga ditulis 23.", verifikasi={"ekspresi": "20 + 3", "hasil": "23"})
tf("c1", "mudah", D, F, S2, "Empat puluh ditulis dengan lambang angka 40.", "Benar", "Empat puluh memang ditulis 40.")

# Terarah (3): S1, S2, S4
mc("c1", "mudah", T, F, S1, "Lambang angka untuk tiga puluh delapan adalah ....", ["38", "83", "308", "30"], "A", "Tiga puluh delapan ditulis 38.", verifikasi={"ekspresi": "30 + 8", "hasil": "38"})
mc("c1", "mudah", T, F, S2, "Lambang angka untuk enam puluh adalah ....", ["60", "16", "600", "6"], "A", "Enam puluh ditulis 60.", verifikasi={"ekspresi": "6 * 10", "hasil": "60"})
sa("c1", "mudah", T, F, S4, "Tulis lambang angka untuk seratus!", "100|seratus", "Seratus ditulis dengan angka 100.", verifikasi={"ekspresi": "100", "hasil": "100"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Tiga puluh lima ditulis ....", ["35", "305", "53", "350"], "A", "Tiga puluh lima ditulis 35.", verifikasi={"ekspresi": "30 + 5", "hasil": "35"})
tf("c2", "mudah", D, Kn, S4, "Seratus ditulis dengan dua angka penyusun.", "Salah", "Seratus memiliki tiga angka yaitu 1, 0, 0.")

# Remedial (2)
mc("c2", "mudah", R, Pr, S3, "Budi menulis empat puluh dua sebagai 402. Cara yang benar adalah ....", ["tulis 42 tanpa menyelipkan nol", "tulis 24", "tulis 4002", "sudah benar"], "A", "Angka satuan 2 menggantikan nol, jadi ditulis 42.", "Menyelipkan angka nol di tengah bilangan campuran", verifikasi={"ekspresi": "40 + 2", "hasil": "42"})
mc("c2", "mudah", R, F, S1, "Lambang angka untuk lima puluh empat adalah ....", ["54", "45", "504", "50"], "A", "Lima puluh empat ditulis 54.", "Tertukar urutan menulis angka puluhan dan satuan", verifikasi={"ekspresi": "50 + 4", "hasil": "54"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S2, "Lambang angka untuk delapan puluh adalah ....", ["80", "18", "800", "88"], "A", "Delapan puluh ditulis 80.", verifikasi={"ekspresi": "8 * 10", "hasil": "80"})
mc("c2", "mudah", T, Kn, S3, "Lambang angka untuk tujuh puluh dua adalah ....", ["72", "27", "702", "70"], "A", "Tujuh puluh dua ditulis 72.", verifikasi={"ekspresi": "70 + 2", "hasil": "72"})
tf("c2", "mudah", T, Kn, S1, "Menulis lambang bilangan dimulai dari angka kanan.", "Salah", "Menulis lambang bilangan dua angka dimulai dari angka kiri (puluhan).")
sa("c2", "mudah", T, F, S4, "Berapa banyak angka nol pada penulisan seratus?", "2|dua", "Pada 100 ada dua angka nol.", verifikasi={"ekspresi": "2", "hasil": "2"})

# ── C3 MUDAH (2 soal: 2 terarah) ──────────────────────────────────────────
# Terarah (2): S1, S3
mc("c3", "mudah", T, Pr, S1, "Lambang angka untuk empat puluh tujuh adalah ....", ["47", "74", "407", "40"], "A", "Empat puluh tujuh ditulis 47.", verifikasi={"ekspresi": "40 + 7", "hasil": "47"})
sa("c3", "mudah", T, Pr, S3, "Tulis lambang angka untuk lima puluh!", "50|lima puluh", "Lima puluh ditulis 50.", verifikasi={"ekspresi": "5 * 10", "hasil": "50"})

# ── C3 SEDANG (12 soal: 4 checkpoint, 2 remedial, 6 terarah) ──────────────
# Checkpoint akhir (4)
mc("c3", "sedang", K, Pr, S2, "Lambang angka untuk sembilan puluh adalah ....", ["90", "19", "900", "99"], "A", "Sembilan puluh ditulis 90.", verifikasi={"ekspresi": "9 * 10", "hasil": "90"})
mc("c3", "sedang", K, Pr, S3, "Lambang angka untuk delapan puluh sembilan adalah ....", ["89", "98", "809", "80"], "A", "Delapan puluh sembilan ditulis 89.", verifikasi={"ekspresi": "80 + 9", "hasil": "89"})
tf("c3", "sedang", K, Kn, S3, "Enam puluh satu ditulis 601.", "Salah", "Enam puluh satu ditulis 61.")
tf("c3", "sedang", K, Pr, S4, "Lambang angka seratus adalah 100.", "Benar", "Seratus ditulis 100.")

# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Ani menulis tujuh puluh enam sebagai 706. Ani harus ....", ["menghapus angka nol di tengah", "menambah angka nol di depan", "menulis 67", "menebak saja"], "A", "Bilangan dua angka tidak memiliki angka nol di tengah.", "Menyisipkan nol di antara puluhan dan satuan")
mc("c3", "sedang", R, Kn, S1, "Lambang bilangan enam puluh tiga ditulis ....", ["63", "36", "603", "16"], "A", "Enam puluh tiga ditulis 63.", "Menulis angka terbalik dari satuan ke puluhan", verifikasi={"ekspresi": "60 + 3", "hasil": "63"})

# Terarah (6): S1, S2, S2, S3, S3, S4
mc("c3", "sedang", T, Pr, S1, "Lambang angka untuk dua puluh delapan adalah ....", ["28", "82", "208", "20"], "A", "Dua puluh delapan ditulis 28.", verifikasi={"ekspresi": "20 + 8", "hasil": "28"})
mc("c3", "sedang", T, Pr, S2, "Puluhan utuh setelah delapan puluh ditulis ....", ["90", "81", "100", "89"], "A", "Puluhan utuh setelah 80 adalah 90.", verifikasi={"ekspresi": "80 + 10", "hasil": "90"})
mc("c3", "sedang", T, Pr, S2, "Lambang bilangan untuk tujuh puluh adalah ....", ["70", "17", "700", "77"], "A", "Tujuh puluh ditulis 70.", verifikasi={"ekspresi": "7 * 10", "hasil": "70"})
mc("c3", "sedang", T, Pr, S3, "Lambang angka untuk sembilan puluh delapan adalah ....", ["98", "89", "908", "90"], "A", "Sembilan puluh delapan ditulis 98.", verifikasi={"ekspresi": "90 + 8", "hasil": "98"})
tf("c3", "sedang", T, Kn, S3, "Bilangan dua angka campuran terdiri dari dua angka.", "Benar", "Bilangan dua angka terdiri dari angka puluhan dan satuan.")
sa("c3", "sedang", T, Pr, S4, "Tulis angka sebelum seratus dalam bentuk lambang angka!", "99|sembilan puluh sembilan", "Sebelum 100 adalah angka 99.", verifikasi={"ekspresi": "100 - 1", "hasil": "99"})

# ── C4 SEDANG (13 soal: 2 checkpoint, 4 mandiri, 7 terarah) ──────────────
# Checkpoint akhir (2)
mc("c4", "sedang", K, Kn, S3, "Manakah lambang angka yang paling tepat untuk sembilan puluh sembilan?", ["99", "909", "109", "990"], "A", "Sembilan puluh sembilan ditulis 99.", verifikasi={"ekspresi": "90 + 9", "hasil": "99"})
tf("c4", "sedang", K, Kn, S2, "Semua puluhan utuh di bawah 100 ditulis dengan dua angka.", "Benar", "Puluhan utuh (10, 20, 30, dst.) memiliki 2 digit.")

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Lambang angka untuk tiga puluh satu adalah ....", ["31", "13", "301", "30"], "A", "Tiga puluh satu ditulis 31.", verifikasi={"ekspresi": "30 + 1", "hasil": "31"})
mc("c4", "sedang", X, Kn, S2, "Berapa banyak angka nol pada penulisan lima puluh?", ["1", "2", "0", "3"], "A", "Pada angka 50 hanya ada satu angka nol.", verifikasi={"ekspresi": "1", "hasil": "1"})
mc("c4", "sedang", X, Kn, S3, "Lambang bilangan untuk delapan puluh empat adalah ....", ["84", "48", "804", "80"], "A", "Delapan puluh empat ditulis 84.", verifikasi={"ekspresi": "80 + 4", "hasil": "84"})
sa("c4", "sedang", X, Pr, S4, "Berapa jumlah digit penyusun pada lambang angka 100?", "3|tiga", "100 memiliki tiga digit: 1, 0, 0.", verifikasi={"ekspresi": "3", "hasil": "3"})

# Terarah (7): S1, S1, S2, S2, S3, S3, S4
mc("c4", "sedang", T, Kn, S1, "Dina mendengar kata enam puluh enam. Dina menulis ....", ["66", "606", "60", "16"], "A", "Enam puluh enam ditulis 66.", verifikasi={"ekspresi": "60 + 6", "hasil": "66"})
tf("c4", "sedang", T, Kn, S1, "Dua puluh satu ditulis 12.", "Salah", "Dua puluh satu ditulis 21.")
mc("c4", "sedang", T, Kn, S2, "Pola lambang bilangan: 40, 50, .... Angka berikutnya adalah?", ["60", "70", "51", "65"], "A", "Lanjutan pola puluhan berikutnya adalah 60.", verifikasi={"ekspresi": "50 + 10", "hasil": "60"})
tf("c4", "sedang", T, Kn, S2, "Penulisan 30 memiliki dua angka nol.", "Salah", "Penulisan 30 hanya memiliki satu angka nol.")
mc("c4", "sedang", T, Kn, S3, "Lambang angka untuk tujuh puluh tujuh adalah ....", ["77", "707", "70", "17"], "A", "Tujuh puluh tujuh ditulis 77.", verifikasi={"ekspresi": "70 + 7", "hasil": "77"})
tf("c4", "sedang", T, Me, S3, "Menuliskan angka puluhan lebih dahulu memudahkan kita.", "Benar", "Menulis dari kiri (puluhan) menjaga urutan tetap benar.")
mc("c4", "sedang", T, Me, S4, "Mengapa lambang seratus memiliki dua angka nol?", ["karena nilainya sepuluh puluhan", "agar terlihat panjang", "karena tidak ada angka lain", "hanya hiasan"], "A", "Seratus tersusun dari sepuluh puluhan sehingga bernilai 100.")

# ── C5 SULIT (6 soal: 2 checkpoint, 4 mandiri) ───────────────────────────
# Checkpoint akhir (2)
mc("c5", "sulit", K, Me, S3, "Riko menulis bilangan lima puluh dua sebagai 502. Mengapa salah?", ["karena angka 502 adalah bilangan tiga digit", "karena seharusnya 25", "karena tidak ada angka nol", "sudah benar"], "A", "Lima puluh dua hanya memiliki dua digit yaitu 52.")
mc("c5", "sulit", K, Me, S4, "Bagaimana membedakan lambang angka sepuluh dan seratus saat menulis?", ["sepuluh satu nol, seratus dua nol", "sepuluh dua nol, seratus satu nol", "keduanya sama", "tidak ada perbedaan"], "A", "Sepuluh ditulis 10, sedangkan seratus ditulis 100.")

# Mandiri (4)
mc("c5", "sulit", X, Kn, S1, "Lambang angka yang tepat untuk bilangan setelah 79 adalah ....", ["80", "710", "89", "70"], "A", "Setelah 79 adalah 80.", verifikasi={"ekspresi": "79 + 1", "hasil": "80"})
mc("c5", "sulit", X, Me, S3, "Mengapa penulisan 405 salah untuk empat puluh lima?", ["angka nol tidak boleh disisipkan di tengah", "angka 5 seharusnya ditulis di paling depan", "empat puluh lima adalah bilangan tiga angka", "angka 4 seharusnya tidak ditulis"], "A", "Angka satuan 5 langsung ditulis di belakang 4 menjadi 45.")
mc("c5", "sulit", X, Kn, S2, "Bilangan puluhan utuh terkecil yang lebih dari 50 ditulis ....", ["60", "51", "70", "50"], "A", "Puluhan utuh berikutnya adalah 60.", verifikasi={"ekspresi": "50 + 10", "hasil": "60"})
mc("c5", "sulit", X, Kn, S4, "Lambang bilangan tepat sebelum 100 yang berakhiran angka nol adalah ....", ["90", "99", "80", "10"], "A", "Puluhan utuh tepat sebelum 100 adalah 90.", verifikasi={"ekspresi": "100 - 10", "hasil": "90"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ──────────────────────────
# Checkpoint akhir (2)
mc("c6", "sulit", K, Me, S2, "Susunlah aturan menulis bilangan puluhan utuh!", ["tulis angka puluhannya lalu akhiri dengan satu nol", "tulis angka nol di depan", "tulis dua angka nol", "tulis tanpa angka nol"], "A", "Puluhan utuh ditulis dengan angka puluhan diikuti angka 0.")
mc("c6", "sulit", K, Kn, S3, "Temukan pasangan lambang bilangan yang jika dibalik tetap dua angka yang sama!", ["88", "80", "18", "81"], "A", "Pada 88, kedua angkanya sama.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Rancanglah cara termudah mengingat penulisan angka 100!", ["ingat angka 1 diikuti dua buah angka 0", "ingat angka sepuluh ditambah satu", "tulis angka nol tiga kali", "tulis angka 1 saja"], "A", "Seratus selalu ditulis angka 1 dengan dua nol (100).")
mc("c6", "sulit", P, Pr, S1, "Urutkan penulisan lambang angka dari terkecil: 42, 24, 40!", ["24, 40, 42", "42, 40, 24", "40, 24, 42", "24, 42, 40"], "A", "Urutan dari yang terkecil adalah 24, lalu 40, kemudian 42.")

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
    u = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab9_soal_{i}"))

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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab9.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
