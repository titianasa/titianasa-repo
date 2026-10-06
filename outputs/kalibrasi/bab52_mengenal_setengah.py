#!/usr/bin/env python3
"""
Generator dan validator Bab 52 Matematika Kelas 2 SD:
"Mengenal Setengah" (Fase A)
bab_id: 99d812e9-139b-4f0f-a5a8-b1ddee6f8cf9
article_id: 7a4aa31f-26ef-4b31-bd76-4a99f9ab3bf2
quiz_id: 4f951c01-9da5-43f4-9e60-f9316c0528fc
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "f1a2b3c4d501"  # Arti Setengah atau Seperdua
S2 = "a2b3c4d5e602"  # Lambang dan Penulisan Pecahan Setengah
S3 = "b3c4d5e6f703"  # Setengah dari Kumpulan Benda
S4 = "c4d5e6f7a804"  # Membuktikan Setengah

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Pernahkah kamu membagi apel dengan teman?
Satu apel dipotong menjadi dua bagian.
Kedua bagian itu harus sama besar.
Satu bagian disebut setengah.
Setengah juga disebut seperdua.
Ada dua bagian setengah pada benda utuh.
Dua setengah bersatu menjadi utuh kembali!

:::definition
title: Setengah
Setengah adalah satu dari dua bagian yang sama besar pada suatu benda.
:::"""

s2_content = """Setengah dapat ditulis dengan lambang bilangan.
Lambang pecahan setengah ditulis $1/2$.
Angka satu ditulis di atas.
Garis pembatas berada di tengah.
Angka dua ditulis di bawah.
Angka dua artinya ada dua bagian.
Angka satu adalah bagian yang diambil.
Kita membacanya satu per dua.

:::steps
title: Cara Menulis Lambang Setengah
1. Tulis angka 1 untuk bagian yang diambil.
2. Buat garis lurus mendatar di bawahnya.
3. Tulis angka 2 di bawah garis.
:::"""

s3_content = """Setengah juga berlaku untuk kumpulan benda.
Budi mempunyai enam buah permen manis.
Budi memberikan setengahnya kepada Siti.
Enam dibagi dua sama rata.
Tiap anak mendapat tiga permen.
Jadi setengah dari enam adalah tiga!
Setengah dari sepuluh adalah lima.
Hitunglah dengan membagi dua rata."""

s4_content = """Bagaimana membuktikan pecahan setengah pada kertas?
Lipatlah kertas tepat di tengah.
Kedua bagian saling menutupi rapat.
Daerah yang diarsir bernilai setengah.
Jika tidak sama besar, bukan setengah!
Perhatikan selalu garis lipatannya.
Pastikan ukurannya benar-benar adil dan pas.

:::common_trap
title: Mengira Setiap Potongan Dua adalah Setengah
Jika memotong roti jadi dua tapi satu besar dan satu kecil.
Potongan itu bukan pecahan setengah!
Syarat mutlak setengah adalah ukurannya wajib sama besar.
:::

:::callout
variant: summary
title: Ringkasan
text: Setengah ($1/2$) adalah satu bagian dari dua bagian sama besar. Menghitung setengah sama dengan membagi dua sama banyak.
:::"""

sections = [
    {
        "id": S1,
        "title": "Arti Setengah atau Seperdua",
        "minutes": 6,
        "goal": "Siswa memahami konsep setengah sebagai salah satu dari dua bagian yang berukuran sama besar.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Lambang dan Penulisan Pecahan Setengah",
        "minutes": 6,
        "goal": "Siswa mampu membaca dan menuliskan lambang pecahan $1/2$ secara benar.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Setengah dari Kumpulan Benda",
        "minutes": 6,
        "goal": "Siswa mampu menentukan banyaknya objek yang bernilai setengah dari sekumpulan benda genap.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Membuktikan Setengah",
        "minutes": 6,
        "goal": "Siswa mampu mengidentifikasi daerah setengah pada gambar arsiran bangun datar melalui simetri lipat.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengenal Setengah",
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
# 2. DEFINISI BANK 50 SOAL BAB 52
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
mc("c1", "mudah", D, F, S1, "Satu benda utuh dibagi dua sama besar. Tiap bagian disebut ....", ["setengah", "seperempat", "utuh", "sepertiga"], "A", "Satu dari dua bagian sama besar disebut setengah atau seperdua.")
tf("c1", "mudah", D, F, S2, "Pecahan setengah dapat dituliskan dengan lambang $1/2$.", "Benar", "Lambang bilangan setengah ditulis 1/2.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Pada lambang pecahan $1/2$, angka 2 di bawah menunjukkan ....", ["jumlah seluruh bagian sama", "bagian yang dimakan", "benda yang tersisa", "angka tambahan"], "A", "Angka 2 di bawah menunjukkan jumlah seluruh bagian sama besar.")
mc("c1", "mudah", T, F, S3, "Berapakah setengah dari 4 buah apel?", ["2 apel", "1 apel", "3 apel", "4 apel"], "A", "4 : 2 = 2 apel.", verifikasi={"ekspresi": "4 / 2", "hasil": "2"})
sa("c1", "mudah", T, F, S3, "Berapakah setengah dari 6 permen?", "3", "6 : 2 = 3 permen.", verifikasi={"ekspresi": "6 / 2", "hasil": "3"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Kapan potongan sebuah roti TIDAK DAPAT disebut setengah?", ["jika kedua bagian tidak sama besar", "jika rotinya berbentuk bulat", "jika rotinya dipotong pisau", "jika rotinya manis"], "A", "Syarat mutlak setengah adalah kedua bagian harus sama besar.")
tf("c2", "mudah", D, Kn, S3, "Setengah dari 8 kelereng adalah 5 kelereng.", "Salah", "Setengah dari 8 adalah 8 : 2 = 4 kelereng, bukan 5.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Ibu memotong kue jadi dua. Satu potong sangat kecil. Apakah itu setengah?", ["bukan karena ukurannya tidak sama besar", "ya karena sudah dipotong dua", "selalu setengah", "tergantung siapa yang makan"], "A", "Bukan setengah karena tidak sama besar.", "Mengira asal dipotong dua sudah setengah")
mc("c2", "mudah", R, Kn, S3, "Berapakah setengah dari 10 jeruk?", ["5 jeruk", "4 jeruk", "6 jeruk", "2 jeruk"], "A", "10 : 2 = 5 jeruk.", "Salah membagi rata kumpulan objek", verifikasi={"ekspresi": "10 / 2", "hasil": "5"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Berapa banyak bagian setengah yang dibutuhkan untuk membentuk satu benda utuh?", ["2 bagian", "1 bagian", "3 bagian", "4 bagian"], "A", "Dua potong setengah membentuk satu keutuhan.", verifikasi={"ekspresi": "2 / 1", "hasil": "2"})
mc("c2", "mudah", T, Kn, S2, "Pecahan $1/2$ dibaca ....", ["satu per dua", "dua per satu", "satu bagi nol", "dua bagi dua"], "A", "Lambang 1/2 dibaca satu per dua atau setengah.")
tf("c2", "mudah", T, Kn, S4, "Lipatan kertas yang saling menutupi rapat menunjukkan dua bagian yang sama besar.", "Benar", "Lipatan simetri yang menutupi rapat menunjukkan ukuran sama besar.")
sa("c2", "mudah", T, Kn, S3, "Berapakah setengah dari 12 butir telur?", "6", "12 : 2 = 6 butir telur.", verifikasi={"ekspresi": "12 / 2", "hasil": "6"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Dono punya 14 kelereng. Dono memberikan setengahnya. Berapa kelereng yang diberikan?", ["7 kelereng", "6 kelereng", "8 kelereng", "5 kelereng"], "A", "14 : 2 = 7 kelereng.", "Keliru pembagian setengah", verifikasi={"ekspresi": "14 / 2", "hasil": "7"})
mc("c3", "sedang", R, Pr, S4, "Sebuah lingkaran dibagi dua sama besar. Satu bagian diarsir. Nilai bagian diarsir?", ["setengah", "seperempat", "satu utuh", "dua"], "A", "Satu dari dua bagian sama besar bernilai setengah ($1/2$).", "Salah menentukan pecahan arsiran")

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Dua anak membagi 1 melon sama besar. Berapa bagian per anak?", ["setengah melon", "satu melon utuh", "seperempat melon", "dua melon"], "A", "Satu melon dibagi 2 sama besar bernilai setengah per anak.")
mc("c3", "mudah", T, Pr, S3, "Berapakah setengah dari 16 buku tulis?", ["8 buku", "6 buku", "10 buku", "7 buku"], "A", "16 : 2 = 8 buku.", verifikasi={"ekspresi": "16 / 2", "hasil": "8"})
tf("c3", "sedang", T, Pr, S1, "Dua bagian setengah jika digabungkan akan menjadi satu benda utuh.", "Benar", "1/2 + 1/2 = 1 benda utuh.")
mc("c3", "sedang", T, Pr, S2, "Manakah lambang pecahan yang bernilai setengah?", ["$1/2$", "$1/4$", "$2/1$", "$1/3$"], "A", "Lambang setengah adalah 1/2.")
tf("c3", "sedang", T, Pr, S4, "Memotong sembarang kertas dari pojok selalu menghasilkan setengah.", "Salah", "Memotong sembarang tidak menjamin ukuran kedua bagian sama besar.")
sa("c3", "sedang", T, Pr, S3, "Berapakah setengah dari 18 bola?", "9", "18 : 2 = 9 bola.", verifikasi={"ekspresi": "18 / 2", "hasil": "9"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Ada 20 kancing baju. Setengahnya berwarna merah. Berapa kancing merah?", ["10 kancing", "8 kancing", "12 kancing", "5 kancing"], "A", "20 : 2 = 10 kancing.", verifikasi={"ekspresi": "20 / 2", "hasil": "10"})
mc("c3", "sedang", X, Pr, S2, "Pada pecahan $1/2$, angka 1 disebut pembilang dan angka 2 disebut ....", ["penyebut", "pembagi", "penjumlah", "pengurang"], "A", "Angka di bawah pada pecahan disebut penyebut.")
tf("c3", "sedang", X, Pr, S3, "Setengah dari 22 donat adalah 12 donat.", "Salah", "22 : 2 = 11 donat, bukan 12.")
sa("c3", "sedang", X, Pr, S4, "Berapakah setengah dari 24 kotak pensil?", "12", "24 : 2 = 12 kotak pensil.", verifikasi={"ekspresi": "24 / 2", "hasil": "12"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Paman memanen 26 semangka. Setengahnya dijual ke pasar. Berapa semangka dijual?", ["13 semangka", "12 semangka", "14 semangka", "15 semangka"], "A", "26 : 2 = 13 semangka.", verifikasi={"ekspresi": "26 / 2", "hasil": "13"})
mc("c3", "sedang", K, Pr, S4, "Sebuah persegi panjang diarsir setengah bagiannya. Berapa bagian yang tidak diarsir?", ["setengah bagian", "satu bagian utuh", "seperempat bagian", "tiga bagian"], "A", "Jika setengah diarsir, maka bagian yang tidak diarsir juga bernilai setengah.")

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa kita tidak boleh menyebut potongan sembarang sebagai pecahan setengah?", ["karena pecahan setengah harus berukuran tepat sama besar", "karena potongan sembarang kotor", "karena angkanya terlalu besar", "karena harus memakai rumus sulit"], "A", "Pecahan setengah mewajibkan kesamaan ukuran pada kedua bagian.")
mc("c4", "sedang", T, Kn, S2, "Jika satu kue dibagi rata kepada 2 anak, bagian tiap anak bernilai ....", ["$1/2$ kue", "$1/4$ kue", "1 kue utuh", "2 kue"], "A", "Tiap anak mendapat 1 bagian dari 2 bagian sama (1/2 kue).")
tf("c4", "sedang", T, Kn, S3, "Setengah dari 30 buku adalah 15 buku.", "Benar", "30 : 2 = 15 buku.")
tf("c4", "sedang", T, Kn, S4, "Membagi lingkaran menjadi dua bagian dengan garis di pinggir menghasilkan setengah.", "Salah", "Garis harus melewati titik pusat lingkaran agar terbagi dua sama besar.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari setengah 28 ditambah 6?", "20", "28 : 2 = 14; 14 + 6 = 20.", verifikasi={"ekspresi": "(28 / 2) + 6", "hasil": "20"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Lina punya 2 potong roti setengah. Edo punya 1 roti utuh. Siapa lebih banyak?", ["roti Lina dan Edo sama banyak", "Lina punya lebih banyak", "Edo punya lebih banyak", "tidak dapat dibandingkan"], "A", "Dua potong setengah bernilai sama dengan satu roti utuh.")
mc("c4", "sedang", X, Kn, S3, "Toko punya 32 pensil. Setengahnya dimasukkan kotak. Berapa pensil di kotak?", ["16 pensil", "14 pensil", "18 pensil", "12 pensil"], "A", "32 : 2 = 16 pensil.", verifikasi={"ekspresi": "32 / 2", "hasil": "16"})
tf("c4", "sedang", X, Kn, S2, "Pecahan $1/2$ nilainya lebih besar daripada satu benda utuh.", "Salah", "Satu benda utuh selalu lebih besar daripada setengahnya.")
mc("c4", "sulit", X, Me, S4, "Manakah dari bangun berikut yang jika dilipat diagonal menghasilkan 2 segitiga sama besar?", ["persegi", "trapesium sembarang", "jajar genjang miring", "layang-layang sembarang"], "A", "Persegi dilipat menurut garis diagonalnya menghasilkan dua segitiga siku-siku yang sama persis.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Budi punya tali 40 cm. Budi memotongnya jadi 2 sama panjang. Panjang tiap tali?", ["20 cm", "15 cm", "25 cm", "10 cm"], "A", "40 : 2 = 20 cm.", verifikasi={"ekspresi": "40 / 2", "hasil": "20"})
mc("c4", "sulit", K, Me, S2, "Di sebuah kotak ada 36 kelereng. Setengahnya berwarna biru. Berapa kelereng biru?", ["18 kelereng", "16 kelereng", "20 kelereng", "14 kelereng"], "A", "36 : 2 = 18 kelereng.", verifikasi={"ekspresi": "36 / 2", "hasil": "18"})
tf("c4", "sulit", K, Me, S4, "Dua buah bangun datar kongruen yang disatukan dapat membentuk bangun utuh semula.", "Benar", "Dua bangun identik sama besar membentuk keutuhan semula.")
mc("c4", "sulit", K, Me, S3, "Berapakah hasil dari (setengah dari 50) dikurangi 10?", ["15", "10", "20", "25"], "A", "50 : 2 = 25; 25 - 10 = 15.", verifikasi={"ekspresi": "(50 / 2) - 10", "hasil": "15"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Jika setengah dari sebuah bilangan adalah 15, berapakah bilangan utuh tersebut?", ["30", "25", "35", "20"], "A", "15 x 2 = 30.", verifikasi={"ekspresi": "15 * 2", "hasil": "30"})
mc("c5", "sedang", T, Me, S2, "Jika setengah dari tabungan Siti adalah 20 rupiah, total tabungan Siti?", ["40 rupiah", "30 rupiah", "50 rupiah", "60 rupiah"], "A", "20 x 2 = 40 rupiah.", verifikasi={"ekspresi": "20 * 2", "hasil": "40"})
mc("c5", "sedang", T, Me, S3, "Ada 44 jeruk. Setengah dibagikan. Sisanya dibagi lagi ke 2 piring. Tiap piring?", ["11 jeruk", "10 jeruk", "12 jeruk", "9 jeruk"], "A", "44 : 2 = 22; 22 : 2 = 11 jeruk.", verifikasi={"ekspresi": "(44 / 2) / 2", "hasil": "11"})
mc("c5", "sulit", T, Me, S4, "Berapakah hasil dari setengah 60 ditambah setengah 40?", ["50", "45", "55", "40"], "A", "(60 : 2) + (40 : 2) = 30 + 20 = 50.", verifikasi={"ekspresi": "(60 / 2) + (40 / 2)", "hasil": "50"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Setengah dari X adalah 18. Berapakah nilai X yang tepat?", ["36", "32", "40", "28"], "A", "18 x 2 = 36.", verifikasi={"ekspresi": "18 * 2", "hasil": "36"})
mc("c5", "sulit", K, Me, S4, "Berapakah hasil dari (setengah dari 48) - (setengah dari 16)?", ["16", "14", "18", "12"], "A", "(48 : 2) - (16 : 2) = 24 - 8 = 16.", verifikasi={"ekspresi": "(48 / 2) - (16 / 2)", "hasil": "16"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Bagaimana cara meyakinkan teman bahwa lipatan segitigamu bernilai setengah?", ["tunjukkan bahwa kedua sisi saling menutupi sempurna saat dilipat", "katakan bahwa kamu menebaknya", "pakai penggaris ukur sembarang", "tidak perlu diyakinkan"], "A", "Saling menutupi sempurna saat dilipat membuktikan luas kedua bagian sama besar.")
mc("c6", "sulit", K, Me, S4, "Sebuah pita 80 cm dipotong setengahnya. Setengah sisanya dipotong lagi setengahnya. Panjang sisa akhir?", ["20 cm", "40 cm", "10 cm", "30 cm"], "A", "80 : 2 = 40 cm; 40 : 2 = 20 cm.", verifikasi={"ekspresi": "(80 / 2) / 2", "hasil": "20"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi: (setengah dari 64) - (setengah dari 24) + 5!", ["25", "20", "30", "15"], "A", "(64 : 2) - (24 : 2) + 5 = 32 - 12 + 5 = 25.", verifikasi={"ekspresi": "(64 / 2) - (24 / 2) + 5", "hasil": "25"})
mc("c6", "sulit", P, Me, S3, "Pak Tani panen 72 jagung. Setengah dibagikan ke tetangga. Sisanya disimpan ke 4 karung. Isi karung?", ["9 jagung", "8 jagung", "10 jagung", "7 jagung"], "A", "72 : 2 = 36; 36 : 4 = 9 jagung per karung.", verifikasi={"ekspresi": "(72 / 2) / 4", "hasil": "9"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab52_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab52.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")

