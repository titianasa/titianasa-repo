#!/usr/bin/env python3
"""
Generator dan validator Bab 53 Matematika Kelas 2 SD:
"Mengenal Seperempat" (Fase A)
bab_id: 7bab3312-a26e-42b3-a867-f023f815315e
article_id: 41baaef1-d85f-4293-950c-16b4198cc346
quiz_id: 8cc3ea47-d6cf-4760-b33c-29046926e58a
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a1c2e3g4i501"  # Arti Seperempat atau Satu per Empat
S2 = "b2d3f4h5j602"  # Lambang dan Penulisan Pecahan Seperempat
S3 = "c3e4g5i6k703"  # Seperempat dari Kumpulan Benda
S4 = "d4f5h6j7l804"  # Membuktikan Seperempat

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Bagaimana jika ada empat anak yang ingin berbagi?
Satu kue martabak dipotong menjadi empat.
Keempat potongan harus sama besar.
Satu bagian disebut seperempat.
Seperempat juga disebut satu per empat.
Ada empat bagian seperempat pada benda utuh.
Empat bagian seperempat bersatu menjadi utuh!

:::definition
title: Seperempat
Seperempat adalah satu dari empat bagian yang sama besar pada suatu benda.
:::"""

s2_content = """Lambang pecahan seperempat ditulis $1/4$.
Angka satu ditulis di atas.
Garis mendatar ada di tengah.
Angka empat ditulis di bawah.
Angka empat artinya empat bagian sama.
Angka satu adalah bagian yang diambil.
Kita membacanya satu per empat.

:::steps
title: Cara Menulis Lambang Seperempat
1. Tulis angka 1 di bagian atas.
2. Buat garis lurus mendatar di tengah.
3. Tulis angka 4 di bagian bawah.
:::"""

s3_content = """Kita juga bisa mencari seperempat kumpulan benda.
Ibu membawa delapan buah apel segar.
Seperempat bagian diberikan kepada adik.
Delapan dibagi empat sama rata.
Adik mendapat dua buah apel.
Jadi seperempat dari delapan adalah dua!
Seperempat dari dua belas adalah tiga.
Hitunglah dengan membagi empat sama banyak."""

s4_content = """Mari kita buktikan dengan selembar kertas.
Lipat kertas menjadi dua bagian.
Lalu lipat sekali lagi menjadi dua.
Buka lipatan kertas tersebut.
Ada empat petak yang sama besar!
Satu petak bernilai seperempat bagian.
Lipatan simetri membuktikan ukuran sama rata.

:::common_trap
title: Mengira Seperempat Lebih Besar dari Setengah
Angka 4 memang lebih besar dari 2.
Tetapi potongan seperempat lebih kecil dari setengah!
Makin banyak bagian, makin kecil potongannya.
:::

:::callout
variant: summary
title: Ringkasan
text: Seperempat ($1/4$) adalah satu dari empat bagian sama besar. Menghitung seperempat sama dengan membagi empat rata.
:::"""

sections = [
    {
        "id": S1,
        "title": "Arti Seperempat atau Satu per Empat",
        "minutes": 6,
        "goal": "Siswa memahami konsep seperempat sebagai salah satu dari empat bagian yang sama besar.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Lambang dan Penulisan Pecahan Seperempat",
        "minutes": 6,
        "goal": "Siswa mampu membaca dan menuliskan lambang pecahan $1/4$ dengan benar.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Seperempat dari Kumpulan Benda",
        "minutes": 6,
        "goal": "Siswa mampu menentukan banyaknya objek yang bernilai seperempat dari kumpulan benda kelipatan empat.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Membuktikan Seperempat",
        "minutes": 6,
        "goal": "Siswa mampu mengidentifikasi dan memvisualisasikan daerah seperempat melalui lipatan atau arsiran petak.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengenal Seperempat",
    "topic": "Mengenal Setengah dan Seperempat",
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
# 2. DEFINISI BANK 50 SOAL BAB 53
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
mc("c1", "mudah", D, F, S1, "Satu kue utuh dipotong menjadi 4 bagian sama besar. Tiap bagian disebut ....", ["seperempat", "setengah", "sepertiga", "satu utuh"], "A", "Satu dari empat bagian sama besar bernilai seperempat.")
tf("c1", "mudah", D, F, S2, "Lambang pecahan seperempat ditulis $1/4$.", "Benar", "Lambang bilangan seperempat adalah 1/4.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Pada lambang pecahan $1/4$, angka 4 di bawah menunjukkan ....", ["jumlah seluruh bagian sama besar", "bagian yang dimakan", "sisa kue", "angka pengurang"], "A", "Angka 4 di bawah (penyebut) menyatakan total 4 bagian sama besar.")
mc("c1", "mudah", T, F, S3, "Berapakah seperempat dari 8 butir kelereng?", ["2 kelereng", "3 kelereng", "4 kelereng", "1 kelereng"], "A", "8 : 4 = 2 kelereng.", verifikasi={"ekspresi": "8 / 4", "hasil": "2"})
sa("c1", "mudah", T, F, S3, "Berapakah seperempat dari 4 buah donat?", "1", "4 : 4 = 1 buah donat.", verifikasi={"ekspresi": "4 / 4", "hasil": "1"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Sebuah lingkaran dibagi 4 bagian berbeda ukuran. Mengapa bukan seperempat?", ["karena keempat bagian tidak sama besar", "karena berbentuk lingkaran", "karena terlalu banyak garis", "karena tidak diwarnai"], "A", "Syarat mutlak seperempat adalah keempat bagian harus sama besar.")
tf("c2", "mudah", D, Kn, S3, "Seperempat dari 12 apel adalah 5 apel.", "Salah", "Seperempat dari 12 adalah 12 : 4 = 3 apel, bukan 5.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Satu roti dipotong jadi 4 bagian sembarang. Apakah tiap potong seperempat?", ["bukan karena ukurannya tidak sama besar", "ya karena sudah dipotong empat", "pasti seperempat", "tergantung pisaunya"], "A", "Bukan seperempat karena ukurannya tidak sama besar.", "Mengira asal dipotong 4 selalu seperempat")
mc("c2", "mudah", R, Kn, S3, "Berapakah seperempat dari 16 jeruk manis?", ["4 jeruk", "3 jeruk", "5 jeruk", "2 jeruk"], "A", "16 : 4 = 4 jeruk.", "Salah membagi rata kumpulan objek ke 4", verifikasi={"ekspresi": "16 / 4", "hasil": "4"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Berapa banyak bagian seperempat yang diperlukan untuk membentuk satu benda utuh?", ["4 bagian", "2 bagian", "3 bagian", "5 bagian"], "A", "Empat potong seperempat membentuk satu keutuhan.", verifikasi={"ekspresi": "4 / 1", "hasil": "4"})
mc("c2", "mudah", T, Kn, S2, "Pecahan $1/4$ dibaca ....", ["satu per empat", "empat per satu", "satu bagi empat puluh", "empat bagi satu"], "A", "Lambang 1/4 dibaca satu per empat atau seperempat.")
tf("c2", "mudah", T, Kn, S4, "Melipat kertas dua kali berturut-turut menghasilkan 4 petak sama besar.", "Benar", "Lipatan dua kali membagi kertas menjadi 4 petak sama rata.")
sa("c2", "mudah", T, Kn, S3, "Berapakah seperempat dari 20 buku gambar?", "5", "20 : 4 = 5 buku.", verifikasi={"ekspresi": "20 / 4", "hasil": "5"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Ada 24 permen dibagikan rata ke 4 anak. Berapa permen tiap anak?", ["6 permen", "5 permen", "7 permen", "4 permen"], "A", "24 : 4 = 6 permen tiap anak.", "Salah menghitung pembagian 4", verifikasi={"ekspresi": "24 / 4", "hasil": "6"})
mc("c3", "sedang", R, Pr, S4, "Sebuah persegi dibagi 4 petak sama besar. Satu petak diarsir. Nilainya?", ["seperempat", "setengah", "tiga per empat", "satu utuh"], "A", "Satu dari empat petak sama bernilai seperempat ($1/4$).", "Salah menentukan pecahan arsiran seperempat")

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Empat anak membagi 1 semangka sama besar. Berapa bagian per anak?", ["seperempat bagian", "setengah bagian", "satu semangka utuh", "tiga bagian"], "A", "Dibagi ke 4 anak sama besar berarti masing-masing mendapat seperempat.")
mc("c3", "mudah", T, Pr, S3, "Berapakah seperempat dari 28 pensil warna?", ["7 pensil", "6 pensil", "8 pensil", "5 pensil"], "A", "28 : 4 = 7 pensil.", verifikasi={"ekspresi": "28 / 4", "hasil": "7"})
tf("c3", "sedang", T, Pr, S1, "Empat potong kue seperempat bernilai sama dengan satu kue utuh.", "Benar", "4 x 1/4 = 1 kue utuh.")
mc("c3", "sedang", T, Pr, S2, "Pecahan berikut yang bernilai seperempat adalah ....", ["$1/4$", "$1/2$", "$2/4$", "$4/1$"], "A", "Lambang seperempat adalah 1/4.")
tf("c3", "sedang", T, Pr, S4, "Potongan seperempat memiliki ukuran yang lebih besar daripada potongan setengah.", "Salah", "Seperempat lebih kecil daripada setengah.")
sa("c3", "sedang", T, Pr, S3, "Berapakah seperempat dari 32 kelereng?", "8", "32 : 4 = 8 kelereng.", verifikasi={"ekspresi": "32 / 4", "hasil": "8"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Ada 36 biskuit. Seperempatnya rasa cokelat. Berapa biskuit cokelat?", ["9 biskuit", "8 biskuit", "10 biskuit", "7 biskuit"], "A", "36 : 4 = 9 biskuit.", verifikasi={"ekspresi": "36 / 4", "hasil": "9"})
mc("c3", "sedang", X, Pr, S2, "Pada lambang pecahan $1/4$, angka 1 dinamakan ....", ["pembilang", "penyebut", "pembagi", "pengali"], "A", "Angka bagian atas pecahan disebut pembilang.")
tf("c3", "sedang", X, Pr, S3, "Seperempat dari 40 bola kasti adalah 12 bola.", "Salah", "40 : 4 = 10 bola, bukan 12.")
sa("c3", "sedang", X, Pr, S4, "Berapakah seperempat dari 40 butir telur?", "10", "40 : 4 = 10 butir telur.", verifikasi={"ekspresi": "40 / 4", "hasil": "10"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Peternak punya 44 bebek. Seperempatnya bertelur. Berapa bebek bertelur?", ["11 bebek", "10 bebek", "12 bebek", "9 bebek"], "A", "44 : 4 = 11 bebek.", verifikasi={"ekspresi": "44 / 4", "hasil": "11"})
mc("c3", "sedang", K, Pr, S4, "Sebuah lingkaran dibagi 4 bagian sama besar. Dua bagian diarsir. Berapa bagian?", ["setengah bagian", "seperempat bagian", "satu utuh", "sepertiga bagian"], "A", "Dua dari empat bagian sama besar bernilai dua per empat atau setengah.")

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa potongan seperempat lebih kecil ukurannya daripada potongan setengah?", ["karena satu benda dibagi menjadi lebih banyak bagian", "karena angka 4 lebih kecil dari 2", "karena pembagiannya tidak rata", "karena warnanya berbeda"], "A", "Makin banyak bagian pembagiannya (dibagi 4 vs dibagi 2), ukuran tiap potongannya makin kecil.")
mc("c4", "sedang", T, Kn, S2, "Dua potong kue seperempat jika disatukan nilainya sama dengan ....", ["setengah kue", "satu kue utuh", "seperempat kue", "tiga per empat kue"], "A", "1/4 + 1/4 = 2/4 = 1/2 kue.")
tf("c4", "sedang", T, Kn, S3, "Seperempat dari 48 buah mangga adalah 12 buah mangga.", "Benar", "48 : 4 = 12 buah mangga.")
tf("c4", "sedang", T, Kn, S4, "Memotong sembarang garis diagonal pada trapesium selalu menghasilkan seperempat.", "Salah", "Trapesium sembarang tidak memiliki simetri lipat menjadi 4 bagian sama besar.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari (seperempat dari 36) + 5?", "14", "36 : 4 = 9; 9 + 5 = 14.", verifikasi={"ekspresi": "(36 / 4) + 5", "hasil": "14"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Budi punya 4 potong roti seperempat. Siti punya 1 roti utuh. Siapa lebih banyak?", ["roti Budi dan Siti sama banyak", "Budi punya lebih banyak", "Siti punya lebih banyak", "tidak dapat dibandingkan"], "A", "4 potong seperempat sama dengan 1 roti utuh.")
mc("c4", "sedang", X, Kn, S3, "Sebuah toko punya 52 penggaris. Seperempatnya terjual. Berapa penggaris terjual?", ["13 penggaris", "12 penggaris", "14 penggaris", "11 penggaris"], "A", "52 : 4 = 13 penggaris.", verifikasi={"ekspresi": "52 / 4", "hasil": "13"})
tf("c4", "sedang", X, Kn, S2, "Pecahan $1/4$ nilainya lebih besar daripada pecahan $1/2$.", "Salah", "1/4 lebih kecil dari 1/2.")
mc("c4", "sulit", X, Me, S4, "Manakah pernyataan yang PALING TEPAT mengenai pecahan seperempat?", ["satu bagian utuh dipotong menjadi empat bagian sama besar", "benda dipotong menjadi empat sembarang", "empat benda utuh digabung menjadi satu", "setengah bagian ditambah satu"], "A", "Definisi tepat: 1 benda utuh dibagi menjadi 4 bagian sama besar.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Kakek punya tali 60 cm. Dipotong jadi 4 sama panjang. Panjang tiap tali?", ["15 cm", "14 cm", "16 cm", "12 cm"], "A", "60 : 4 = 15 cm.", verifikasi={"ekspresi": "60 / 4", "hasil": "15"})
mc("c4", "sulit", K, Me, S2, "Di perpustakaan ada 56 buku dongeng. Seperempatnya dipinjam. Berapa buku dipinjam?", ["14 buku", "12 buku", "15 buku", "13 buku"], "A", "56 : 4 = 14 buku.", verifikasi={"ekspresi": "56 / 4", "hasil": "14"})
tf("c4", "sulit", K, Me, S4, "Dua bagian seperempat sama besarnya dengan satu bagian setengah.", "Benar", "2/4 bernilai sama dengan 1/2.")
mc("c4", "sulit", K, Me, S3, "Berapakah hasil dari (seperempat dari 64) dikurangi 6?", ["10", "8", "12", "9"], "A", "64 : 4 = 16; 16 - 6 = 10.", verifikasi={"ekspresi": "(64 / 4) - 6", "hasil": "10"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Jika seperempat dari suatu bilangan adalah 9, berapakah bilangan utuh tersebut?", ["36", "32", "40", "28"], "A", "9 x 4 = 36.", verifikasi={"ekspresi": "9 * 4", "hasil": "36"})
mc("c5", "sedang", T, Me, S2, "Jika seperempat tabungan Doni adalah 10 rupiah, total tabungan Doni?", ["40 rupiah", "30 rupiah", "50 rupiah", "20 rupiah"], "A", "10 x 4 = 40 rupiah.", verifikasi={"ekspresi": "10 * 4", "hasil": "40"})
mc("c5", "sedang", T, Me, S3, "Ada 68 jeruk. Seperempatnya diberikan ke bibi. Berapa jeruk untuk bibi?", ["17 jeruk", "16 jeruk", "18 jeruk", "15 jeruk"], "A", "68 : 4 = 17 jeruk.", verifikasi={"ekspresi": "68 / 4", "hasil": "17"})
mc("c5", "sulit", T, Me, S4, "Berapakah hasil dari seperempat 80 ditambah seperempat 40?", ["30", "25", "35", "20"], "A", "(80 : 4) + (40 : 4) = 20 + 10 = 30.", verifikasi={"ekspresi": "(80 / 4) + (40 / 4)", "hasil": "30"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Seperempat dari Y adalah 15. Berapakah nilai Y?", ["60", "55", "65", "50"], "A", "15 x 4 = 60.", verifikasi={"ekspresi": "15 * 4", "hasil": "60"})
mc("c5", "sulit", K, Me, S4, "Berapakah hasil dari (seperempat dari 72) - (seperempat dari 32)?", ["10", "8", "12", "9"], "A", "(72 : 4) - (32 : 4) = 18 - 8 = 10.", verifikasi={"ekspresi": "(72 / 4) - (32 / 4)", "hasil": "10"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Bagaimana cara membuktikan pada teman bahwa satu kue dibagi 4 menghasilkan seperempat?", ["lipat dua lalu lipat dua lagi dan tunjukkan 4 bagian sama persis", "tunjukkan gambar acak di papan tulis", "hitung jumlah anak yang ada di ruangan", "tidak bisa dibuktikan"], "A", "Melipat dua kali simetris membuktikan terbentuk 4 bagian sama besar secara nyata.")
mc("c6", "sulit", K, Me, S4, "Sebuah batang kayu 80 cm dipotong jadi 4 sama panjang. Panjang 3 potong kayu?", ["60 cm", "50 cm", "70 cm", "40 cm"], "A", "80 : 4 = 20 cm; 3 x 20 cm = 60 cm.", verifikasi={"ekspresi": "3 * (80 / 4)", "hasil": "60"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi: (seperempat dari 96) - (seperempat dari 48) + 8!", ["20", "18", "22", "16"], "A", "(96 : 4) - (48 : 4) + 8 = 24 - 12 + 8 = 20.", verifikasi={"ekspresi": "(96 / 4) - (48 / 4) + 8", "hasil": "20"})
mc("c6", "sulit", P, Me, S3, "Pak Budi panen 88 jagung. Seperempat dibagikan, sisanya dimasukkan 3 karung. Isi karung?", ["22 jagung", "20 jagung", "24 jagung", "18 jagung"], "A", "88 - (88 : 4) = 88 - 22 = 66 jagung; 66 : 3 = 22 jagung per karung.", verifikasi={"ekspresi": "(88 - (88 / 4)) / 3", "hasil": "22"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab53_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab53.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")

