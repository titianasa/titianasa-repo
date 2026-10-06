#!/usr/bin/env python3
"""
Generator dan validator Bab 42 Matematika Kelas 2 SD:
"Hubungan Penjumlahan dengan Pengurangan" (Fase A)
bab_id: 3d547525-6c6e-48b2-9131-cdf609bda8d6
article_id: 474d8283-7bdd-49c4-9e36-3b9e020e3e76
quiz_id: fa866331-bba5-493f-a6be-8849c13c4d7e
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "d7e8f9a0b101"  # Penjumlahan dan Pengurangan Operasi Kebalikan
S2 = "e8f9a0b1c202"  # Keluarga Fakta (Fact Families)
S3 = "f9a0b1c2d303"  # Memeriksa Pengurangan dengan Penjumlahan
S4 = "a0b1c2d3e404"  # Mencari Bilangan yang Belum Diketahui

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Penjumlahan dan pengurangan saling berhubungan.
Keduanya operasi yang berkebalikan.
Dua puluh lima tambah lima belas jadi empat puluh.
Empat puluh kurang lima belas jadi dua puluh lima.
Pengurangan membatalkan penjumlahan.
Penjumlahan membatalkan pengurangan.
Mereka sahabat karib matematika.

:::definition
title: Operasi Kebalikan
Operasi kebalikan adalah hubungan saling membalikkan operasi hitung.
:::"""

s2_content = """Tiga bilangan membentuk keluarga fakta.
Lihatlah angka 20, 30, dan 50.
20 tambah 30 jadi 50.
30 tambah 20 jadi 50.
50 kurang 20 jadi 30.
50 kurang 30 jadi 20.
Ada empat kalimat matematika.
Belajar keluarga fakta sangat asyik!

:::steps
title: Membuat Keluarga Fakta
1. Tulis dua kalimat penjumlahan bolak-balik.
2. Tulis dua kalimat pengurangan dari hasil jumlah.
3. Gunakan selalu tiga bilangan yang sama.
:::"""

s3_content = """Periksalah hasil pengurangan dengan penjumlahan.
Enam puluh empat kurang dua puluh delapan.
Hasil hitungan kita tiga puluh enam.
Ayo kita jumlahkan kembali.
Tiga puluh enam tambah dua puluh delapan.
Hasilnya adalah enam puluh empat.
Bilangan kembali seperti semula.
Jawaban pengurangan kita pasti benar!"""

s4_content = """Hubungan ini mencari bilangan rahasia.
Berapa ditambah 17 jadi 45?
Baliklah operasi hitung ini.
Kurangkan 45 dengan 17.
45 kurang 17 jadi 28.
Bilangan rahasianya adalah 28.
Sangat cerdas dan cepat!

:::common_trap
title: Salah Menentukan Operasi Pembalik
Jika mencari pengurang, gunakan pengurangan tepat.
Tujuh puluh kurang berapa jadi empat puluh dua?
Hitunglah tujuh puluh dikurang empat puluh dua.
Bukan tujuh puluh ditambah empat puluh dua!
:::

:::callout
variant: summary
title: Ringkasan
text: Penjumlahan adalah kebalikan dari pengurangan. Periksa pengurangan dengan penjumlahan. Cari bilangan rahasia dengan operasi kebalikan.
:::"""

sections = [
    {
        "id": S1,
        "title": "Penjumlahan dan Pengurangan Operasi Kebalikan",
        "minutes": 6,
        "goal": "Siswa memahami bahwa penjumlahan dan pengurangan merupakan operasi matematika yang saling berkebalikan.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Keluarga Fakta (Fact Families)",
        "minutes": 6,
        "goal": "Siswa mampu menyusun 4 kalimat matematika (2 penjumlahan dan 2 pengurangan) dari 3 bilangan terkait.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Memeriksa Pengurangan dengan Penjumlahan",
        "minutes": 6,
        "goal": "Siswa mampu mengecek kebenaran hasil pengurangan dengan menjumlahkan hasil sisa dengan pengurang.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Mencari Bilangan yang Belum Diketahui",
        "minutes": 6,
        "goal": "Siswa mampu menemukan nilai suku yang hilang pada kalimat penjumlahan atau pengurangan menggunakan operasi kebalikan.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Hubungan Penjumlahan dengan Pengurangan",
    "topic": "Penjumlahan dan Pengurangan sampai 100",
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
# 2. DEFINISI BANK 50 SOAL BAB 42
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
mc("c1", "mudah", D, F, S1, "Operasi hitung yang merupakan kebalikan dari penjumlahan adalah ....", ["pengurangan", "perkalian", "pembagian", "pengukuran"], "A", "Pengurangan adalah kebalikan dari operasi penjumlahan.")
tf("c1", "mudah", D, F, S2, "Tiga bilangan dapat membentuk empat kalimat matematika keluarga fakta.", "Benar", "2 kalimat penjumlahan dan 2 kalimat pengurangan.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Jika 30 + 20 = 50, maka 50 dikurang 20 menghasilkan ....", ["30", "20", "50", "10"], "A", "50 - 20 = 30.", verifikasi={"ekspresi": "50 - 20", "hasil": "30"})
mc("c1", "mudah", T, F, S3, "Cara memeriksa kebenaran hasil pengurangan adalah dengan operasi ....", ["penjumlahan", "pengurangan lagi", "perkalian", "pembagian"], "A", "Menjumlahkan hasil sisa dengan pengurang untuk menguji kebenaran.")
sa("c1", "mudah", T, F, S1, "Jika 40 + 15 = 55, berapakah hasil dari 55 - 40?", "15", "55 - 40 = 15.", verifikasi={"ekspresi": "55 - 40", "hasil": "15"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Manakah pasangan pengurangan dari kalimat 24 + 16 = 40?", ["40 - 16 = 24", "40 + 16 = 56", "24 - 16 = 8", "40 - 40 = 0"], "A", "Keluarga fakta pengurangan dari 24 + 16 = 40 adalah 40 - 16 = 24.", "Keliru menyusun kalimat pengurangan dari penjumlahan")
tf("c2", "mudah", D, Kn, S4, "Untuk mencari titik-titik pada ... + 20 = 60, kita kurangkan 60 dengan 20.", "Benar", "60 - 20 = 40.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Mengapa penjumlahan dan pengurangan disebut operasi kebalikan?", ["karena satu operasi membatalkan efek operasi lainnya", "karena lambangnya mirip", "karena selalu menghasilkan nol", "karena dihitung bersama"], "A", "Penjumlahan menambah nilai, sedangkan pengurangan mengurangi kembali nilai tersebut.", "Belum memahami konsep invers operasi")
mc("c2", "mudah", R, Kn, S4, "Jika titik-titik ditambah 15 sama dengan 35, berapakah titik-titik itu?", ["20", "50", "15", "30"], "A", "35 - 15 = 20.", "Salah memilih operasi untuk mencari suku hilang", verifikasi={"ekspresi": "35 - 15", "hasil": "20"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S2, "Bilangan 18, 12, dan 30 adalah satu keluarga fakta karena ....", ["18 + 12 = 30", "18 - 12 = 30", "18 + 30 = 12", "30 + 18 = 12"], "A", "18 + 12 = 30 menghubungkan ketiga bilangan tersebut.")
mc("c2", "mudah", T, Kn, S3, "Jika Doni menghitung 48 - 16 = 32, cara mengecek jawabannya adalah ....", ["menjumlahkan 32 + 16", "mengurangkan 32 - 16", "menjumlahkan 48 + 32", "mengurangkan 48 - 32"], "A", "Cek apakah 32 + 16 = 48.")
tf("c2", "mudah", T, Kn, S1, "Jika 25 + 35 = 60, maka 60 - 35 sama dengan 30.", "Salah", "60 - 35 = 25, bukan 30.")
sa("c2", "mudah", T, Kn, S4, "Berapakah bilangan pengganti N jika N + 25 = 75?", "50", "75 - 25 = 50.", verifikasi={"ekspresi": "75 - 25", "hasil": "50"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Siti menghitung 72 - 28 = 44. Apakah hitungan Siti benar?", ["benar karena 44 + 28 = 72", "salah karena 44 + 28 = 70", "salah karena 44 - 28 = 16", "tidak tahu"], "A", "44 + 28 = 72, jadi hitungan Siti benar.", "Tidak dapat membuktikan pengurangan lewat penjumlahan")
mc("c3", "sedang", R, Pr, S4, "Berapakah nilai titik-titik pada kalimat 65 - ... = 28?", ["37", "47", "36", "38"], "A", "65 - 28 = 37.", "Menjumlahkan bukan mengurangkan pada pengurang hilang", verifikasi={"ekspresi": "65 - 28", "hasil": "37"})

# Terarah (6): S1, S2, S3, S4, S2, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Jika 34 + 28 = 62, maka 62 - 34 bernilai ....", ["28", "38", "27", "29"], "A", "62 - 34 = 28.", verifikasi={"ekspresi": "62 - 34", "hasil": "28"})
mc("c3", "mudah", T, Pr, S4, "Berapakah nilai A jika 50 + A = 85?", ["35", "25", "45", "30"], "A", "85 - 50 = 35.", verifikasi={"ekspresi": "85 - 50", "hasil": "35"})
tf("c3", "sedang", T, Pr, S2, "Kalimat 58 - 23 = 35 sekeluarga dengan 35 + 23 = 58.", "Benar", "Keduanya memakai bilangan 23, 35, dan 58.")
mc("c3", "sedang", T, Pr, S3, "Lina menghitung 81 - 36 = 45. Pemeriksaan yang benar adalah ....", ["45 + 36 = 81", "81 + 36 = 117", "45 - 36 = 9", "81 - 45 = 30"], "A", "Jumlahkan sisa (45) dengan pengurang (36) menghasilkan 81.")
tf("c3", "sedang", T, Pr, S1, "Jika 46 + 18 = 64, maka 64 - 18 bernilai 56.", "Salah", "64 - 18 = 46, bukan 56.")
sa("c3", "sedang", T, Pr, S4, "Berapakah nilai B jika B + 37 = 72?", "35", "72 - 37 = 35.", verifikasi={"ekspresi": "72 - 37", "hasil": "35"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Jika 57 + 29 = 86, maka 86 dikurang 29 sama dengan ....", ["57", "47", "58", "56"], "A", "86 - 29 = 57.", verifikasi={"ekspresi": "86 - 29", "hasil": "57"})
mc("c3", "sedang", X, Pr, S2, "Manakah yang BUKAN anggota keluarga fakta dari 27, 35, dan 62?", ["62 + 35 = 97", "27 + 35 = 62", "62 - 27 = 35", "62 - 35 = 27"], "A", "62 + 35 = 97 tidak berada dalam keluarga fakta ketiga bilangan tersebut.")
tf("c3", "sedang", X, Pr, S3, "Pengurangan 90 - 45 = 45 benar karena 45 + 45 = 90.", "Benar", "Pemeriksaan dengan penjumlahan terbukti tepat.")
sa("c3", "sedang", X, Pr, S4, "Berapakah nilai K jika 84 - K = 38?", "46", "84 - 38 = 46.", verifikasi={"ekspresi": "84 - 38", "hasil": "46"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Budi menghitung 85 - 47 = 38. Buktikan dengan penjumlahan!", ["38 + 47 = 85", "85 + 47 = 132", "47 + 47 = 94", "38 + 38 = 76"], "A", "38 + 47 = 85 membuktikan kebenaran pengurangannya.")
mc("c3", "sedang", K, Pr, S4, "Berapakah nilai P jika P + 48 = 91?", ["43", "33", "44", "42"], "A", "91 - 48 = 43.", verifikasi={"ekspresi": "91 - 48", "hasil": "43"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Edo punya 60 kelereng. Diberi adik A, sekarang jadi 85. Berapa A?", ["25 kelereng", "35 kelereng", "20 kelereng", "15 kelereng"], "A", "85 - 60 = 25 kelereng.", verifikasi={"ekspresi": "85 - 60", "hasil": "25"})
mc("c4", "sedang", T, Kn, S2, "Tiga bilangan adalah 34, 48, dan 82. Kalimat pengurangan yang benar adalah ....", ["82 - 34 = 48", "82 - 48 = 30", "48 - 34 = 82", "34 - 82 = 48"], "A", "82 - 34 = 48 adalah kalimat pengurangan yang valid.")
tf("c4", "sedang", T, Kn, S3, "Jika hasil pengurangan 73 - 29 adalah 44, maka 73 - 44 pasti 29.", "Benar", "Ini adalah sifat keluarga fakta dari tiga bilangan.")
tf("c4", "sedang", T, Kn, S4, "Untuk menyelesaikan 80 - ... = 35, kita harus menghitung 80 + 35.", "Salah", "Seharusnya menghitung 80 - 35 = 45.")
sa("c4", "sedang", T, Kn, S4, "Sebuah toko punya 93 roti, tersisa 46 roti. Berapa roti yang terjual?", "47", "93 - 46 = 47 roti.", verifikasi={"ekspresi": "93 - 46", "hasil": "47"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Andi memikirkan sebuah bilangan. Jika ditambah 36 hasilnya 82. Berapa bilangan itu?", ["46", "56", "45", "47"], "A", "82 - 36 = 46.", verifikasi={"ekspresi": "82 - 36", "hasil": "46"})
mc("c4", "sedang", X, Kn, S3, "Rani menghitung 95 - 48 = 57. Saat diperiksa 57 + 48 = 105. Apa kesimpulannya?", ["hitungan Rani salah seharusnya 47", "hitungan Rani sudah benar", "pemeriksaannya yang salah", "angka 95 salah"], "A", "Karena 57 + 48 = 105 (bukan 95), hitungan Rani salah, harusnya 47.")
tf("c4", "sedang", X, Kn, S2, "Kalimat 70 - 25 = 45 dan 70 - 20 = 50 berasal dari keluarga yang sama.", "Salah", "Keluarga fakta harus memakai tiga bilangan yang sama.")
mc("c4", "sulit", X, Me, S4, "Pak Dani punya bibit pohon. Ditanam 38 bibit, sisa 47 bibit. Berapa bibit awal?", ["85 bibit", "75 bibit", "86 bibit", "84 bibit"], "A", "Operasi kebalikan: 47 + 38 = 85 bibit awal.", verifikasi={"ekspresi": "47 + 38", "hasil": "85"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Diberikan angka 26, 47, dan 73. Manakah kalimat matematika yang tepat?", ["73 - 47 = 26", "26 + 73 = 47", "73 - 26 = 57", "47 - 26 = 73"], "A", "73 - 47 = 26 adalah kalimat fakta yang benar.")
mc("c4", "sulit", K, Me, S3, "Beni menghitung 94 - 58 = 36. Bagaimana cara memeriksa yang paling meyakinkan?", ["menjumlahkan 36 + 58 dan melihat apakah hasilnya 94", "menghitung ulang dari awal", "menebak-nebak", "mengurangi lagi dengan 10"], "A", "Menjumlahkan hasil sisa dengan pengurang: 36 + 58 = 94 membuktikan kebenarannya.")
tf("c4", "sulit", K, Me, S4, "Jika M - 45 = 35, maka nilai M lebih kecil daripada 50.", "Salah", "M = 35 + 45 = 80. 80 jauh lebih besar dari 50.")
mc("c4", "sulit", K, Me, S4, "Di perpustakaan ada buku cerita. Dipinjam 49 buku, sisa 38 buku. Berapa buku awal?", ["87 buku", "77 buku", "88 buku", "86 buku"], "A", "38 + 49 = 87 buku.", verifikasi={"ekspresi": "38 + 49", "hasil": "87"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Jika 43 + 39 = 82, maka nilai dari 82 - 39 - 20 adalah ....", ["23", "13", "33", "43"], "A", "82 - 39 = 43; 43 - 20 = 23.", verifikasi={"ekspresi": "82 - 39 - 20", "hasil": "23"})
mc("c5", "sedang", T, Me, S2, "Jika segitiga bilangan berisi 38, ..., dan 90, bilangan yang tepat adalah ....", ["52", "42", "62", "50"], "A", "90 - 38 = 52.", verifikasi={"ekspresi": "90 - 38", "hasil": "52"})
mc("c5", "sedang", T, Me, S3, "Untuk membuktikan 91 - 46 = 45, operasi penjumlahan manakah yang tepat?", ["45 + 46 = 91", "91 + 46 = 137", "45 + 45 = 90", "46 + 46 = 92"], "A", "45 + 46 = 91.")
mc("c5", "sulit", T, Me, S4, "Sebuah bus membawa penumpang. Turun 28 orang, naik 15 orang, sekarang ada 50. Berapa orang semula?", ["63 orang", "53 orang", "73 orang", "43 orang"], "A", "Operasi kebalikan: 50 - 15 = 35; 35 + 28 = 63 orang.", verifikasi={"ekspresi": "50 - 15 + 28", "hasil": "63"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Berapakah hasil dari (96 - 48) + 48?", ["96", "48", "0", "94"], "A", "Penjumlahan membatalkan pengurangan, hasilnya kembali ke 96.", verifikasi={"ekspresi": "(96 - 48) + 48", "hasil": "96"})
mc("c5", "sulit", K, Me, S4, "Jika (X + 27) - 15 = 60, berapakah nilai bilangan X?", ["48", "38", "58", "45"], "A", "X + 27 = 60 + 15 = 75; X = 75 - 27 = 48.", verifikasi={"ekspresi": "60 + 15 - 27", "hasil": "48"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Mengapa hubungan keluarga fakta sangat bermanfaat dalam matematika?", ["karena jika kita hafal satu fakta kita tahu tiga fakta lainnya secara otomatis", "karena membuat angka jadi lebih besar", "karena hanya ada satu operasi", "tidak ada gunanya"], "A", "Keluarga fakta mengaitkan 4 operasi (2 tambah dan 2 kurang) dari 3 bilangan sekaligus.")
mc("c6", "sulit", K, Me, S4, "Lina membuat teka-teki: 'Aku dikurang 36 jadi 45'. Bagaimana cara temannya memecahkan teka-teki?", ["menjumlahkan 45 dengan 36 menggunakan operasi kebalikan untuk menemukan 81", "mengurangkan 45 dengan 36", "menebak angka 10", "mengalikan angkanya"], "A", "Menggunakan operasi kebalikan: 45 + 36 = 81.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Berapakah hasil dari (87 - 39) + (75 - 39) jika diselesaikan bertahap?", ["84", "74", "85", "83"], "A", "87 - 39 = 48; 75 - 39 = 36; 48 + 36 = 84.", verifikasi={"ekspresi": "(87 - 39) + (75 - 39)", "hasil": "84"})
mc("c6", "sulit", P, Me, S4, "Suatu bilangan ditambah 28 lalu dikurang 19 menghasilkan 65. Berapa bilangan awal?", ["56", "46", "66", "54"], "A", "Operasi kebalikan: 65 + 19 = 84; 84 - 28 = 56.", verifikasi={"ekspresi": "65 + 19 - 28", "hasil": "56"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab42_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab42.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
