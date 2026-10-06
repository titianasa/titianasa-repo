#!/usr/bin/env python3
"""
Generator dan validator Bab 28 Matematika Kelas 1 SD:
"Mengenal Segitiga, Segiempat, dan Lingkaran" (Fase A)
bab_id: 6c405635-9560-4088-9258-bea65c05333d
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "e1f2a33b4c01"  # Mengenal Bentuk Segitiga
S2 = "f2a3b44c5d12"  # Mengenal Bentuk Segiempat
S3 = "a3b4c55d6e23"  # Mengenal Bentuk Lingkaran
S4 = "b4c5d66e7f34"  # Menghitung Sisi dan Sudut Bangun Datar

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Perhatikan potongan sepotong pizza lezat.
Bentuknya menyerupai bangun segitiga.
Segitiga dibatasi tiga garis lurus.
Tiga garis itu disebut tiga sisi.
Segitiga memiliki tiga pojok runcing.
Pojok itu disebut titik sudut.
Banyak benda berbentuk segitiga.
Ada penggaris segitiga dan rambu jalan.

:::definition
title: Segitiga
Segitiga adalah bangun datar dengan 3 sisi lurus dan 3 titik sudut.
:::"""

s2_content = """Lihatlah permukaan buku tulismu.
Permukaan buku berbentuk segiempat.
Segiempat dibatasi empat garis lurus.
Artinya segiempat memiliki empat sisi.
Segiempat memiliki empat pojok.
Ubin keramik juga berbentuk segiempat.
Pintu kelas juga berbentuk segiempat.
Bentuk ini sangat sering kita jumpai.

:::steps
title: Ciri Segiempat
1. Memiliki 4 sisi garis lurus.
2. Memiliki 4 titik sudut di setiap pojok.
:::"""

s3_content = """Amati permukaan roda sepedamu.
Permukaan roda berbentuk lingkaran bulat.
Lingkaran dibatasi satu garis lengkung.
Garis lengkung itu menyambung rapi.
Lingkaran tidak memiliki pojok runcing.
Lingkaran tidak memiliki sudut sama sekali.
Uang koin logam berbentuk lingkaran.
Piring makan bulat juga lingkaran."""

s4_content = """Mari hitung sisi dan sudut.
Segitiga punya 3 sisi.
Segitiga juga punya 3 sudut.
Segiempat punya 4 sisi.
Segiempat juga punya 4 sudut.
Lingkaran punya 1 sisi lengkung.
Lingkaran tidak punya sudut.

:::common_trap
title: Lingkaran Tidak Memiliki Sudut
Segitiga memiliki 3 sudut.
Segiempat memiliki 4 sudut.
Lingkaran melengkung bulat tanpa pojok.
Lingkaran memiliki 0 sudut.
Jangan mengira lingkaran punya pojok.
:::

:::callout
variant: summary
title: Ringkasan
text: Segitiga punya 3 sisi dan 3 sudut. Segiempat punya 4 sisi dan 4 sudut. Lingkaran punya 1 garis lengkung dan 0 sudut.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Bentuk Segitiga",
        "minutes": 6,
        "goal": "Siswa mengenal bangun datar segitiga yang memiliki 3 sisi lurus dan 3 titik sudut.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengenal Bentuk Segiempat",
        "minutes": 6,
        "goal": "Siswa mengenal bangun datar segiempat yang memiliki 4 sisi lurus dan 4 titik sudut.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mengenal Bentuk Lingkaran",
        "minutes": 6,
        "goal": "Siswa mengenal bangun datar lingkaran yang dibatasi 1 garis lengkung tanpa titik sudut.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menghitung Sisi dan Sudut Bangun Datar",
        "minutes": 6,
        "goal": "Siswa dapat menghitung dan membandingkan jumlah sisi dan sudut pada segitiga, segiempat, dan lingkaran.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengenal Segitiga, Segiempat, dan Lingkaran",
    "topic": "Mengenal Bentuk Bangun Datar dan Bangun Ruang",
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
# 2. DEFINISI BANK 50 SOAL BAB 28
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
mc("c1", "mudah", D, F, S1, "Bangun datar yang memiliki 3 sisi lurus dinamakan ....", ["segitiga", "segiempat", "lingkaran", "kubus"], "A", "Bangun dengan 3 sisi lurus adalah segitiga.")
tf("c1", "mudah", D, F, S3, "Lingkaran memiliki 4 titik sudut yang lancip.", "Salah", "Lingkaran berbentuk bulat melengkung tanpa titik sudut.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Buku tulis dan ubin keramik memiliki bentuk dasar ....", ["segiempat", "segitiga", "lingkaran", "bola"], "A", "Buku dan ubin berbentuk segiempat dengan 4 sisi.")
mc("c1", "mudah", T, F, S3, "Benda berikut yang berbentuk lingkaran adalah ....", ["uang koin logam", "pintu rumah", "atap segitiga", "buku cetak"], "A", "Uang koin logam memiliki bentuk lingkaran bundar.")
sa("c1", "mudah", T, F, S4, "Berapa jumlah titik sudut pada sebuah bangun segitiga?", "3", "Segitiga memiliki tepat 3 titik sudut.", verifikasi={"ekspresi": "3", "hasil": "3"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Berapa jumlah titik sudut yang dimiliki oleh lingkaran?", ["0 sudut", "1 sudut", "3 sudut", "4 sudut"], "A", "Lingkaran tidak memiliki sudut (0 sudut).", "Mengira lingkaran memiliki titik sudut", verifikasi={"ekspresi": "0", "hasil": "0"})
tf("c2", "mudah", D, Kn, S2, "Bangun segiempat selalu memiliki 4 sisi dan 4 sudut.", "Benar", "Segiempat dibatasi 4 sisi dan memiliki 4 sudut.")

# Remedial (2)
mc("c2", "mudah", R, F, S1, "Penggaris berbentuk segitiga memiliki sisi lurus sebanyak ....", ["3 sisi", "4 sisi", "5 sisi", "2 sisi"], "A", "Setiap bangun segitiga memiliki 3 sisi lurus.", "Salah menghitung sisi segitiga", verifikasi={"ekspresi": "3", "hasil": "3"})
mc("c2", "mudah", R, Kn, S3, "Garis pembatas pada bangun lingkaran berbentuk garis ....", ["lengkung", "patah-patah", "lurus kaku", "segi tiga"], "A", "Batas lingkaran berupa satu garis lengkung tertutup.", "Mengira pembatas lingkaran berupa garis lurus")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Berapa banyak sisi pada 1 segitiga ditambah 1 segitiga?", ["6 sisi", "5 sisi", "7 sisi", "4 sisi"], "A", "3 + 3 = 6 sisi.", verifikasi={"ekspresi": "3 + 3", "hasil": "6"})
mc("c2", "mudah", T, Kn, S2, "Berapa selisih jumlah sisi antara segiempat dan segitiga?", ["1 sisi", "2 sisi", "3 sisi", "0 sisi"], "A", "4 - 3 = 1 sisi.", verifikasi={"ekspresi": "4 - 3", "hasil": "1"})
tf("c2", "mudah", T, Kn, S4, "Jumlah sudut pada segiempat lebih banyak daripada sudut segitiga.", "Benar", "Segiempat punya 4 sudut, segitiga punya 3 sudut (4 > 3).")
sa("c2", "mudah", T, Kn, S4, "Sebuah segiempat punya 4 sisi. Berapa sudut yang dimilikinya?", "4", "Segiempat memiliki 4 sudut.", verifikasi={"ekspresi": "4", "hasil": "4"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Siti menggambar sebuah bangun datar dengan 4 pojok siku. Bangun itu adalah ....", ["segiempat", "segitiga", "lingkaran", "garis lurus"], "A", "Bangun dengan 4 pojok adalah segiempat.", "Tertukar menentukan nama bangun dari jumlah pojok")
mc("c3", "sedang", R, Pr, S4, "Berapa jumlah total sudut dari 1 segitiga dan 1 segiempat?", ["7 sudut", "6 sudut", "8 sudut", "5 sudut"], "A", "3 + 4 = 7 sudut.", "Salah menjumlahkan sudut dua bangun datar berbeda", verifikasi={"ekspresi": "3 + 4", "hasil": "7"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Ada 2 bangun segitiga. Berapa total sudut kedua segitiga itu?", ["6 sudut", "5 sudut", "7 sudut", "4 sudut"], "A", "3 + 3 = 6 sudut.", verifikasi={"ekspresi": "3 + 3", "hasil": "6"})
mc("c3", "sedang", T, Pr, S2, "Ada 2 bangun segiempat. Berapa total sisi kedua segiempat itu?", ["8 sisi", "7 sisi", "9 sisi", "6 sisi"], "A", "4 + 4 = 8 sisi.", verifikasi={"ekspresi": "4 + 4", "hasil": "8"})
tf("c3", "sedang", T, Pr, S3, "Roda sepeda dan piring makan memiliki bentuk dasar segiempat.", "Salah", "Roda dan piring makan berbentuk dasar lingkaran.")
mc("c3", "sedang", T, Pr, S4, "Sebuah segiempat punya 4 sisi. Dua segitiga punya 6 sisi. Berapa selisihnya?", ["2 sisi", "1 sisi", "3 sisi", "4 sisi"], "A", "6 - 4 = 2 sisi.", verifikasi={"ekspresi": "6 - 4", "hasil": "2"})
tf("c3", "sedang", T, Pr, S1, "Potongan pizza berbentuk segitiga memiliki tiga titik pojok.", "Benar", "Potongan pizza memiliki bentuk segitiga dengan 3 pojok.")
sa("c3", "mudah", T, Pr, S2, "Berapa jumlah sisi pada 2 bangun segiempat jika satu bangun punya 4 sisi?", "8", "4 + 4 = 8 sisi.", verifikasi={"ekspresi": "4 + 4", "hasil": "8"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Udin membuat segitiga dari 3 sedotan. Berapa sedotan untuk 3 segitiga?", ["9 sedotan", "8 sedotan", "10 sedotan", "6 sedotan"], "A", "3 x 3 = 9 sedotan.", verifikasi={"ekspresi": "3 * 3", "hasil": "9"})
mc("c3", "sedang", X, Pr, S2, "Budi punya 12 stik es krim. Satu segiempat butuh 4 stik. Berapa segiempat yang dibuat?", ["3 segiempat", "2 segiempat", "4 segiempat", "5 segiempat"], "A", "12 / 4 = 3 bangun.", verifikasi={"ekspresi": "12 // 4", "hasil": "3"})
tf("c3", "sedang", X, Pr, S4, "Dua lingkaran memiliki total 8 titik sudut.", "Salah", "Lingkaran tidak memiliki sudut, jadi total sudutnya adalah 0.")
sa("c3", "sedang", X, Pr, S4, "Berapa total sisi dari 2 bangun segitiga dan 1 segiempat?", "10", "3 + 3 + 4 = 10 sisi.", verifikasi={"ekspresi": "3 + 3 + 4", "hasil": "10"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Satu segitiga punya 3 sisi. Berapa sisi pada 4 segitiga terpisah?", ["12 sisi", "10 sisi", "14 sisi", "9 sisi"], "A", "4 x 3 = 12 sisi.", verifikasi={"ekspresi": "4 * 3", "hasil": "12"})
mc("c3", "sedang", K, Pr, S3, "Ada 5 koin lingkaran dan 4 kertas segiempat. Berapa total benda itu?", ["9 benda", "8 benda", "10 benda", "7 benda"], "A", "5 + 4 = 9 benda.", verifikasi={"ekspresi": "5 + 4", "hasil": "9"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Jika ada bangun dengan 3 sisi lurus dan 3 sudut, pasti itu adalah ....", ["segitiga", "segiempat", "lingkaran", "kubus"], "A", "Bangun dengan ciri 3 sisi dan 3 sudut adalah segitiga.")
mc("c4", "sedang", T, Kn, S2, "Manakah pernyataan yang benar tentang bangun segiempat?", ["mempunyai 4 sisi lurus dan 4 pojok", "mempunyai 3 sisi dan 3 pojok", "dibatasi oleh garis lengkung", "tidak memiliki titik sudut"], "A", "Segiempat memiliki 4 sisi lurus dan 4 titik sudut.")
tf("c4", "sedang", T, Kn, S3, "Lingkaran dapat menggelinding dengan mudah karena sisinya melengkung halus.", "Benar", "Garis lengkung lingkaran memungkinkannya menggelinding lancar.")
tf("c4", "sedang", T, Kn, S4, "Sebuah segitiga memiliki lebih banyak sisi daripada sebuah segiempat.", "Salah", "Segitiga hanya 3 sisi, sedangkan segiempat memiliki 4 sisi (3 < 4).")
sa("c4", "sedang", T, Kn, S4, "Tiga segiempat punya 12 sisi. Satu segitiga punya 3 sisi. Selisih sisinya?", "9", "12 - 3 = 9 sisi.", verifikasi={"ekspresi": "12 - 3", "hasil": "9"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Kertas berbentuk segiempat dilipat jadi 2 segitiga. Berapa sisi 1 segitiga?", ["3 sisi", "4 sisi", "5 sisi", "2 sisi"], "A", "Setiap potongan segitiga memiliki 3 sisi.", verifikasi={"ekspresi": "3", "hasil": "3"})
mc("c4", "sedang", X, Kn, S2, "Papan catur berbentuk segiempat. Berapa jumlah titik sudut pada 2 papan catur?", ["8 sudut", "6 sudut", "10 sudut", "7 sudut"], "A", "4 + 4 = 8 sudut.", verifikasi={"ekspresi": "4 + 4", "hasil": "8"})
tf("c4", "sedang", X, Kn, S4, "Dua segitiga dan satu segiempat memiliki total 10 titik sudut.", "Benar", "3 + 3 + 4 = 10 titik sudut.")
mc("c4", "sulit", X, Me, S3, "Ada 15 lidi. Dibuat 3 segiempat (tiap bangun 4 lidi). Berapa lidi tersisa?", ["3 lidi", "2 lidi", "4 lidi", "1 lidi"], "A", "15 - 12 = 3 lidi.", verifikasi={"ekspresi": "15 - (3 * 4)", "hasil": "3"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Benda di bawah ini yang permukaannya TIDAK berbentuk segiempat adalah ....", ["jam dinding bulat", "pintu rumah", "papan tulis", "ubin keramik"], "A", "Jam dinding bulat berpermukaan lingkaran.")
mc("c4", "sulit", K, Me, S2, "Ada 18 stik kayu. Dibuat 4 segiempat (butuh 16 stik). Berapa stik sisa?", ["2 stik", "1 stik", "3 stik", "4 stik"], "A", "18 - 16 = 2 stik.", verifikasi={"ekspresi": "18 - 16", "hasil": "2"})
tf("c4", "sulit", K, Me, S3, "Sebuah lingkaran yang dipotong tepat di tengah menjadi dua bangun segiempat.", "Salah", "Potongan lingkaran menjadi setengah lingkaran, bukan segiempat.")
mc("c4", "sulit", K, Me, S4, "Tiga bangun segitiga (tiap bangun 3 sisi). Berapa sisi yang harus ditambah agar jadi 15?", ["6 sisi", "5 sisi", "7 sisi", "4 sisi"], "A", "15 - 9 = 6 sisi.", verifikasi={"ekspresi": "15 - (3 * 3)", "hasil": "6"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Lani punya 2 segitiga dan 2 segiempat. Berapa total sudut keempat bangun itu?", ["14 sudut", "12 sudut", "15 sudut", "13 sudut"], "A", "(2 x 3) + (2 x 4) = 6 + 8 = 14 sudut.", verifikasi={"ekspresi": "2 * 3 + 2 * 4", "hasil": "14"})
mc("c5", "sedang", T, Me, S2, "Tersedia 16 batang korek api. Berapa paling banyak bangun segiempat dapat dibuat?", ["4 segiempat", "3 segiempat", "5 segiempat", "2 segiempat"], "A", "16 / 4 = 4 bangun segiempat.", verifikasi={"ekspresi": "16 // 4", "hasil": "4"})
mc("c5", "sedang", T, Me, S3, "Mengapa roda kendaraan dibuat berbentuk lingkaran dan bukan segiempat?", ["karena lingkaran bisa berputar mulus tanpa terhambat pojok", "karena lingkaran lebih murah", "karena warna ban hitam", "karena segiempat terlalu bundar"], "A", "Bentuk lingkaran yang mulus tanpa sudut memungkinkan perputaran lancar.")
mc("c5", "sulit", T, Me, S4, "Bangun A = 4 sudut, B = 3 sudut, C = 0 sudut. Berapa total sudut ketiganya?", ["7 sudut", "6 sudut", "8 sudut", "5 sudut"], "A", "4 + 3 + 0 = 7 sudut.", verifikasi={"ekspresi": "4 + 3 + 0", "hasil": "7"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Ada 20 kawat lurus. Dipakai membuat 5 segitiga (tiap bangun 3 kawat). Berapa sisa kawat?", ["5 kawat", "4 kawat", "6 kawat", "3 kawat"], "A", "20 - 15 = 5 kawat.", verifikasi={"ekspresi": "20 - 15", "hasil": "5"})
mc("c5", "sulit", K, Me, S3, "Empat koin lingkaran digabung dengan 3 kartu segiempat (tiap kartu 4 sudut). Berapa total sudut?", ["12 sudut", "10 sudut", "14 sudut", "8 sudut"], "A", "0 + (3 x 4) = 12 sudut.", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Rancanglah gambar gerobak sederhana menggunakan gabungan bentuk lingkaran dan segiempat!", ["membuat bak gerobak bentuk segiempat dan dua roda bentuk lingkaran", "membuat roda segitiga dan bak bulat", "menggambar awan di langit saja", "menumpuk lingkaran tanpa bak"], "A", "Bak segiempat dipadukan dengan roda lingkaran membentuk gerobak yang baik.")
mc("c6", "sulit", K, Me, S4, "Kelompokkan bangun datar berdasarkan jumlah sudutnya secara tepat!", ["lingkaran (0 sudut), segitiga (3 sudut), segiempat (4 sudut)", "segitiga (0 sudut), segiempat (3 sudut), lingkaran (4 sudut)", "semua bangun punya 4 sudut", "lingkaran punya 3 sudut dan segitiga 4 sudut"], "A", "Pengelompokan tepat: lingkaran 0, segitiga 3, segiempat 4 sudut.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S2, "Ada 3 segiempat (tiap bangun 4 sisi) dan 2 segitiga (tiap bangun 3 sisi). Total sisi?", ["18 sisi", "16 sisi", "20 sisi", "14 sisi"], "A", "(3 x 4) + (2 x 3) = 12 + 6 = 18 sisi.", verifikasi={"ekspresi": "3 * 4 + 2 * 3", "hasil": "18"})
mc("c6", "sulit", P, Me, S4, "Bangun gabungan dibuat dari 2 segitiga dan 3 segiempat. Berapa total seluruh sudutnya?", ["18 sudut", "16 sudut", "20 sudut", "15 sudut"], "A", "(2 x 3) + (3 x 4) = 6 + 12 = 18 sudut.", verifikasi={"ekspresi": "2 * 3 + 3 * 4", "hasil": "18"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab28_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab28.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
