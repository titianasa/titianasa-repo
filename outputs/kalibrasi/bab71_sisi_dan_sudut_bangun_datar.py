#!/usr/bin/env python3
"""
Generator dan validator Bab 71 Matematika Kelas 2 SD:
"Sisi dan Sudut Bangun Datar" (Fase A)
bab_id: 796c7af5-e432-45a7-a171-72caab581f77
article_id: 44a8cc55-f165-4ee8-bba4-def6c5162947
quiz_id: 7e55aeb5-a87f-4687-94d7-bd2f389401dd
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "p1r2t3v4x501"  # Mengenal Sisi Bangun Datar
S2 = "q2s3u4w5y602"  # Mengenal Sudut dan Titik Sudut
S3 = "r3t4v5x6z703"  # Menghitung Jumlah Sisi dan Sudut
S4 = "s4u5w6y7a804"  # Mengelompokkan Berdasarkan Jumlah Sisi

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Bangun datar dibatasi garis lurus.
Garis pembatas itu disebut sisi.
Segitiga dibatasi tiga garis lurus.
Maka segitiga memiliki tiga sisi.
Segiempat dibatasi empat garis lurus.
Maka segiempat memiliki empat sisi.
Raba tepi meja atau buku.
Tepian lurus itulah sisinya!

:::definition
title: Sisi Bangun Datar
Ruas garis lurus yang membatasi suatu bidang bangun datar.
:::"""

s2_content = """Dua sisi bertemu pada pojok.
Pertemuan dua sisi membentuk sudut.
Pojok lancip disebut titik sudut.
Segitiga memiliki tiga titik sudut.
Segiempat memiliki empat titik sudut.
Perhatikan pojok papan tulis.
Pojok itu adalah titik sudut.
Setiap bangun datar memiliki sudut!

:::steps
title: Menemukan Titik Sudut
1. Cari garis-garis tepi bangun datar.
2. Temukan tempat dua garis bertemu.
3. Pojok pertemuan itulah titik sudutnya.
:::"""

s3_content = """Mari menghitung sisi dan sudut.
Segitiga memiliki 3 sisi.
Segitiga juga memiliki 3 sudut.
Persegi memiliki 4 sisi.
Persegi juga memiliki 4 sudut.
Segilima memiliki 5 sisi.
Segilima memiliki 5 sudut.
Jumlah sisi sama dengan sudut!

:::common_trap
title: Mengira Jumlah Sisi Berbeda dengan Sudut
Pada segi banyak beraturan dan sederhana.
Banyaknya sisi selalu sama dengan sudut.
Bila sisinya 4, sudutnya 4!
:::"""

s4_content = """Kita dapat mengelompokkan bangun datar.
Kelompok pertama adalah bangun segitiga.
Semua memiliki tepat 3 sisi.
Kelompok kedua adalah segiempat.
Persegi dan persegi panjang bersisi 4.
Kelompok ketiga adalah segi banyak.
Segilima punya 5 sisi.
Hitung sisinya untuk mengelompokkannya!

:::callout
variant: summary
title: Ringkasan
text: Sisi adalah garis pembatas. Titik sudut adalah pojok pertemuan dua sisi.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Sisi Bangun Datar",
        "minutes": 6,
        "goal": "Siswa mengenal konsep ruas garis pembatas sebagai sisi bangun datar.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengenal Sudut dan Titik Sudut",
        "minutes": 6,
        "goal": "Siswa memahami sudut dan titik sudut sebagai pojok pertemuan dua sisi.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Menghitung Jumlah Sisi dan Sudut",
        "minutes": 6,
        "goal": "Siswa mampu menghitung banyak sisi dan sudut pada segitiga, segiempat, dan segilima.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Mengelompokkan Berdasarkan Jumlah Sisi",
        "minutes": 6,
        "goal": "Siswa dapat mengelompokkan bangun datar berdasarkan banyak sisi dan sudutnya.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Sisi dan Sudut Bangun Datar",
    "topic": "Bangun Datar dan Bangun Ruang Sederhana",
    "level": "Kelas 2 SD · Fase A",
    "sections": sections
}

# Verifikasi teks materi sesuai kriteria validasi
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
# 2. DEFINISI BANK 50 SOAL BAB 71
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
mc("c1", "mudah", D, F, S1, "Ruas garis lurus pembatas bangun datar disebut ....", ["sisi", "sudut", "titik pusat", "isi"], "A", "Garis pembatas bangun datar dinamakan sisi.")
tf("c1", "mudah", D, F, S2, "Pojok tempat bertemunya dua sisi bangun datar disebut titik sudut.", "Benar", "Titik sudut adalah pojok pertemuan dua sisi.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Berapakah jumlah sisi yang dimiliki oleh bangun segitiga?", ["3 sisi", "4 sisi", "5 sisi", "2 sisi"], "A", "Segitiga memiliki 3 sisi.", verifikasi={"ekspresi": "1 * 3", "hasil": "3"})
mc("c1", "mudah", T, F, S2, "Berapakah banyak titik sudut pada bangun segiempat?", ["4 sudut", "3 sudut", "5 sudut", "6 sudut"], "A", "Segiempat memiliki 4 titik sudut.", verifikasi={"ekspresi": "2 * 2", "hasil": "4"})
sa("c1", "mudah", T, F, S3, "Bangun datar persegi memiliki ... sisi sama panjang.", "4", "Persegi memiliki 4 sisi.", verifikasi={"ekspresi": "4 * 1", "hasil": "4"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Bila sebuah bangun datar memiliki 5 sisi, bangun itu adalah ....", ["segilima", "segitiga", "segiempat", "segienam"], "A", "Bangun dengan 5 sisi disebut segilima.")
tf("c2", "mudah", D, Kn, S1, "Sisi sebuah bangun datar dapat berupa garis lengkung yang patah.", "Salah", "Sisi bangun datar poligon berupa garis lurus.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S3, "Berapa banyak sudut yang dimiliki oleh bangun segitiga?", ["3 sudut", "4 sudut", "2 sudut", "5 sudut"], "A", "Segitiga memiliki 3 sudut.", "Mengira segitiga memiliki 4 sudut", verifikasi={"ekspresi": "3 * 1", "hasil": "3"})
mc("c2", "mudah", R, Kn, S2, "Berapa banyak titik sudut yang dimiliki oleh bangun persegi panjang?", ["4 titik sudut", "3 titik sudut", "6 titik sudut", "5 titik sudut"], "A", "Persegi panjang memiliki 4 titik sudut.", "Salah menghitung titik sudut persegi panjang", verifikasi={"ekspresi": "2 + 2", "hasil": "4"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Permukaan buku tulis berbentuk segiempat. Berapa sisinya?", ["4 sisi", "3 sisi", "5 sisi", "2 sisi"], "A", "Buku segiempat memiliki 4 sisi.", verifikasi={"ekspresi": "4 * 1", "hasil": "4"})
mc("c2", "mudah", T, Kn, S4, "Manakah dari bangun berikut yang termasuk kelompok segiempat?", ["persegi", "segitiga sama sisi", "lingkaran", "segilima"], "A", "Persegi termasuk kelompok segiempat.")
tf("c2", "mudah", T, Kn, S3, "Bangun datar segienam memiliki tepat enam buah sisi dan enam sudut.", "Benar", "Segienam memiliki 6 sisi dan 6 sudut.")
sa("c2", "mudah", T, Kn, S3, "Jumlah sudut pada bangun segilima adalah ... buah.", "5", "Segilima memiliki 5 sudut.", verifikasi={"ekspresi": "5 * 1", "hasil": "5"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Berapakah jumlah gabungan sisi dari 2 buah segitiga?", ["6 sisi", "5 sisi", "7 sisi", "8 sisi"], "A", "2 x 3 = 6 sisi.", "Salah mengalikan jumlah sisi bangun", verifikasi={"ekspresi": "2 * 3", "hasil": "6"})
mc("c3", "sedang", R, Pr, S4, "Ada bangun dengan 4 sisi sama panjang. Bangun apakah itu?", ["persegi", "segitiga", "segilima", "trapesium"], "A", "Persegi memiliki 4 sisi sama panjang.", "Menyebut bangun lain yang sisinya tidak sama")

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S3, "Berapakah banyak sisi dari 3 buah bangun persegi digabungkan?", ["12 sisi", "10 sisi", "14 sisi", "8 sisi"], "A", "3 x 4 = 12 sisi.", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})
mc("c3", "mudah", T, Pr, S4, "Benda berikut yang memiliki 3 sisi dan 3 sudut adalah ....", ["penggaris segitiga", "papan tulis", "uang logam", "buku tulis"], "A", "Penggaris segitiga memiliki 3 sisi.")
tf("c3", "sedang", T, Pr, S1, "Sebuah segitiga memiliki 4 sisi garis lurus.", "Salah", "Segitiga selalu memiliki 3 sisi garis lurus.")
mc("c3", "sedang", T, Pr, S2, "Berapakah total titik sudut dari 2 segitiga dan 1 segiempat?", ["10 titik sudut", "9 titik sudut", "11 titik sudut", "12 titik sudut"], "A", "(2 x 3) + 4 = 6 + 4 = 10.", verifikasi={"ekspresi": "(2 * 3) + 4", "hasil": "10"})
tf("c3", "sedang", T, Pr, S4, "Uang kertas dan papan catur sama-sama termasuk bangun segiempat.", "Benar", "Keduanya memiliki 4 sisi dan 4 sudut.")
sa("c3", "sedang", T, Pr, S3, "Total sisi dari 4 buah bangun segitiga adalah ... sisi.", "12", "4 x 3 = 12 sisi.", verifikasi={"ekspresi": "4 * 3", "hasil": "12"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Berapakah jumlah sisi pada 5 buah bangun segiempat?", ["20 sisi", "15 sisi", "25 sisi", "16 sisi"], "A", "5 x 4 = 20 sisi.", verifikasi={"ekspresi": "5 * 4", "hasil": "20"})
mc("c3", "sedang", X, Pr, S3, "Budi punya 2 segilima. Berapa jumlah semua sudut bangun Budi?", ["10 sudut", "8 sudut", "12 sudut", "15 sudut"], "A", "2 x 5 = 10 sudut.", verifikasi={"ekspresi": "2 * 5", "hasil": "10"})
tf("c3", "sedang", X, Pr, S2, "Titik sudut segitiga selalu berjumlah lebih banyak daripada sisinya.", "Salah", "Jumlah sudut segitiga sama persis dengan sisinya (3 = 3).")
sa("c3", "sedang", X, Pr, S4, "Berapa banyak bangun bersisi empat pada kumpulan persegi dan persegi panjang?", "2", "Ada 2 jenis bangun bersisi 4.", verifikasi={"ekspresi": "1 + 1", "hasil": "2"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Berapakah selisih banyak sisi antara bangun segienam dan segitiga?", ["3 sisi", "2 sisi", "4 sisi", "1 sisi"], "A", "6 - 3 = 3 sisi.", verifikasi={"ekspresi": "6 - 3", "hasil": "3"})
mc("c3", "sedang", K, Pr, S4, "Kumpulan bangun: segitiga, persegi, persegi panjang, segilima. Berapa segiempat?", ["2 bangun", "1 bangun", "3 bangun", "4 bangun"], "A", "Persegi dan persegi panjang = 2 bangun segiempat.", verifikasi={"ekspresi": "1 + 1", "hasil": "2"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa sebuah bangun tertutup minimal harus memiliki 3 sisi lurus?", ["karena 2 garis lurus tidak dapat menutup menjadi bangun datar", "karena angka 3 angka ganjil", "supaya tidak bulat", "karena aturan sekolah"], "A", "Dua garis lurus hanya membentuk sudut dan tidak dapat menutup bidang.")
mc("c4", "sedang", T, Kn, S2, "Apa yang terjadi pada sudut jika dua garis lurus saling sejajar?", ["tidak membentuk sudut karena tidak pernah berpotongan", "membentuk 1 sudut", "membentuk sudut siku", "menjadi bulat"], "A", "Garis sejajar tidak bertemu sehingga tidak ada titik sudut.")
tf("c4", "sedang", T, Kn, S3, "Bangun datar bersisi 8 memiliki tepat 8 buah titik sudut.", "Benar", "Segidelapan memiliki 8 sisi dan 8 titik sudut.")
tf("c4", "sedang", T, Kn, S4, "Semua bangun datar yang memiliki 4 sisi pasti bentuknya persegi.", "Salah", "Ada persegi panjang, trapesium, jajargenjang, dan layang-layang.")
sa("c4", "sedang", T, Kn, S3, "Berapakah jumlah sudut dari 3 buah segiempat dan 2 buah segitiga?", "18", "(3 x 4) + (2 x 3) = 12 + 6 = 18.", verifikasi={"ekspresi": "(3 * 4) + (2 * 3)", "hasil": "18"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Sebuah kertas dipotong menjadi 2 bagian segitiga. Total sisi kedua potongan?", ["6 sisi", "5 sisi", "4 sisi", "7 sisi"], "A", "2 segitiga x 3 = 6 sisi.", verifikasi={"ekspresi": "2 * 3", "hasil": "6"})
mc("c4", "sedang", X, Kn, S2, "Jika salah satu pojok kertas persegi dipotong lurus, bersisa berapa sudut?", ["5 sudut", "4 sudut", "3 sudut", "6 sudut"], "A", "Memotong 1 pojok menambah 1 sisi dan 1 sudut baru = 5 sudut.", verifikasi={"ekspresi": "4 - 1 + 2", "hasil": "5"})
tf("c4", "sedang", X, Kn, S3, "Sebuah bangun datar dengan 7 sisi dinamakan bangun segitujuh.", "Benar", "Poligon 7 sisi dinamakan segitujuh (heptagon).")
mc("c4", "sulit", X, Me, S4, "Kumpulan potongan: 4 segitiga dan 3 segiempat. Berapa total titik sudutnya?", ["24 sudut", "22 sudut", "20 sudut", "26 sudut"], "A", "(4 x 3) + (3 x 4) = 12 + 12 = 24 sudut.", verifikasi={"ekspresi": "(4 * 3) + (3 * 4)", "hasil": "24"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Bila selembar kertas segitiga dipotong sejajar salah satu sisinya, terbentuk?", ["1 segitiga kecil dan 1 segiempat", "2 segitiga", "2 segiempat", "1 lingkaran"], "A", "Bagian atas segitiga kecil, bagian bawah trapesium (segiempat).")
mc("c4", "sulit", K, Me, S2, "Dua batang lidi dipasang bersilangan (+). Berapa sudut yang terbentuk di tengah?", ["4 sudut", "2 sudut", "3 sudut", "1 sudut"], "A", "Dua garis berpotongan membentuk 4 sudut di tengah.", verifikasi={"ekspresi": "2 * 2", "hasil": "4"})
tf("c4", "sulit", K, Me, S3, "Menempelkan 2 segitiga pada sisinya selalu menghasilkan bangun bersisi 6.", "Salah", "Dua sisi berimpit di dalam, sehingga hasilnya bangun bersisi 4 (segiempat).")
mc("c4", "sulit", K, Me, S4, "Ali memiliki 30 sedotan sama panjang untuk membuat segitiga. Berapa segitiga?", ["10 segitiga", "8 segitiga", "15 segitiga", "12 segitiga"], "A", "30 : 3 = 10 segitiga.", verifikasi={"ekspresi": "30 / 3", "hasil": "10"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Tersedia 20 sedotan. Berapa banyak segiempat yang dapat dibuat secara terpisah?", ["5 segiempat", "4 segiempat", "6 segiempat", "3 segiempat"], "A", "20 : 4 = 5 segiempat.", verifikasi={"ekspresi": "20 / 4", "hasil": "5"})
mc("c5", "sedang", T, Me, S2, "Bandingkan sudut tumpul dan sudut lancip. Manakah yang memiliki bukaan lebih besar?", ["sudut tumpul", "sudut lancip", "keduanya sama besar", "tidak dapat dibandingkan"], "A", "Sudut tumpul memiliki bukaan lebih besar daripada sudut siku dan lancip.")
mc("c5", "sedang", T, Me, S3, "Tiga segiempat dan empat segitiga disusun terpisah. Berapa total sisinya?", ["24 sisi", "22 sisi", "20 sisi", "26 sisi"], "A", "(3 x 4) + (4 x 3) = 12 + 12 = 24 sisi.", verifikasi={"ekspresi": "(3 * 4) + (4 * 3)", "hasil": "24"})
mc("c5", "sulit", T, Me, S4, "Sebuah pola hiasan terdiri dari 5 segienam terpisah. Berapa total sudutnya?", ["30 sudut", "24 sudut", "36 sudut", "25 sudut"], "A", "5 x 6 = 30 sudut.", verifikasi={"ekspresi": "5 * 6", "hasil": "30"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Rina menggambar 4 segilima dan 2 segienam. Berapa selisih total sisinya?", ["8 sisi", "6 sisi", "10 sisi", "4 sisi"], "A", "(4 x 5) - (2 x 6) = 20 - 12 = 8 sisi.", verifikasi={"ekspresi": "(4 * 5) - (2 * 6)", "hasil": "8"})
mc("c5", "sulit", K, Me, S4, "Tersedia 38 stik es krim. Dibuat 5 segiempat, sisanya dibuat segitiga. Berapa segitiga?", ["6 segitiga", "5 segitiga", "7 segitiga", "4 segitiga"], "A", "38 - (5 x 4) = 38 - 20 = 18 stik. 18 : 3 = 6 segitiga.", verifikasi={"ekspresi": "(38 - (5 * 4)) / 3", "hasil": "6"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Mengapa segitiga menjadi bentuk paling kokoh untuk jembatan dan atap rumah?", ["karena susunan 3 sisi segitiga tidak mudah berubah bentuk atau goyang", "karena warnanya bagus", "karena paling murah", "hanya tradisi"], "A", "Segitiga bersifat kaku dan stabil secara geometris.")
mc("c6", "sulit", K, Me, S4, "Diberikan selembar kertas persegi. Bagaimana cara membuat 2 segitiga sama besar?", ["melipat dan memotong kertas diagonal dari satu pojok ke pojok seberangnya", "memotong lurus di tengah", "meremas kertas", "membuat lingkaran"], "A", "Potongan diagonal membagi persegi menjadi 2 segitiga sama besar.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Hitung total sisi: (6 x 3 sisi) + (4 x 4 sisi) + (2 x 5 sisi)!", ["44 sisi", "40 sisi", "46 sisi", "42 sisi"], "A", "18 + 16 + 10 = 44 sisi.", verifikasi={"ekspresi": "(6 * 3) + (4 * 4) + (2 * 5)", "hasil": "44"})
mc("c6", "sulit", P, Me, S4, "Pak Made membuat pagar motif: 8 segiempat dan 6 segitiga. Berapa total sudutnya?", ["50 sudut", "48 sudut", "52 sudut", "46 sudut"], "A", "(8 x 4) + (6 x 3) = 32 + 18 = 50 sudut.", verifikasi={"ekspresi": "(8 * 4) + (6 * 3)", "hasil": "50"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab71_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab71.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")

