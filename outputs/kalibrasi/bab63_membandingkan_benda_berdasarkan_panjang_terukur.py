#!/usr/bin/env python3
"""
Generator dan validator Bab 63 Matematika Kelas 2 SD:
"Membandingkan Benda Berdasarkan Panjang Terukur" (Fase A)
bab_id: 053f5dee-853a-455c-8359-7dff39b582f4
article_id: 16c6427d-27b3-434a-85bb-dc9060a184ed
quiz_id: c0ab520f-31af-4687-9c95-4a37c9e8b651
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "h1j2l3n4p501"  # Membandingkan Dua Nilai Ukur Sentimeter
S2 = "i2k3m4o5q602"  # Menghitung Selisih Panjang
S3 = "j3l4n5p6r703"  # Mengurutkan Benda Berdasarkan Panjang
S4 = "k4m5o6q7s804"  # Membandingkan Panjang Gabungan

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Kita sudah bisa mengukur benda.
Sekarang kita bandingkan ukurannya.
Ada pensil 12 cm.
Ada krayon 8 cm.
Angka 12 lebih besar dari 8.
Maka pensil lebih panjang dari krayon.
Krayon lebih pendek dari pensil.
Bandingkan angka sentimeter dengan cermat!

:::definition
title: Lebih Panjang dan Lebih Pendek
Benda berukuran sentimeter lebih besar berarti lebih panjang. Benda berukuran lebih kecil berarti lebih pendek.
:::"""

s2_content = """Berapa perbedaan panjang keduanya?
Kita bisa mencari selisihnya.
Gunakan operasi pengurangan.
Kurangi bilangan besar dengan kecil.
Pensil 12 cm dikurang krayon 8 cm.
12 dikurang 8 adalah 4.
Jadi pensil lebih panjang 4 cm.
Selisih dicari dengan cara dikurang!

:::steps
title: Cara Menghitung Selisih Panjang
1. Tentukan ukuran benda yang lebih panjang.
2. Tentukan ukuran benda yang lebih pendek.
3. Kurangkan: Ukuran panjang - Ukuran pendek.
:::"""

s3_content = """Jika ada tiga benda, urutkanlah!
Contoh tiga benda di meja:
Penghapus panjangnya 5 cm.
Spidol panjangnya 14 cm.
Penggaris panjangnya 30 cm.
Urutan dari paling pendek:
Penghapus, lalu spidol, lalu penggaris.
Urutan dari paling panjang:
Penggaris, lalu spidol, lalu penghapus.
Perhatikan kata perintah soalnya!"""

s4_content = """Terkadang benda digabungkan.
Misalnya dua tali disambung.
Tali merah panjangnya 10 cm.
Tali biru panjangnya 15 cm.
Panjang gabungan adalah 25 cm.
Sekarang bandingkan dengan tongkat 20 cm.
Tali gabungan lebih panjang 5 cm.
Hitung jumlahnya sebelum membandingkan!

:::common_trap
title: Mengira Selisih Dicari dengan Penjumlahan
Selisih adalah perbedaan jarak atau ukuran.
Gunakan pengurangan, bukan penjumlahan!
:::

:::callout
variant: summary
title: Ringkasan
text: Bandingkan angka cm. Cari selisih dengan pengurangan. Urutkan sesuai permintaan soal.
:::"""

sections = [
    {
        "id": S1,
        "title": "Membandingkan Dua Nilai Ukur Sentimeter",
        "minutes": 6,
        "goal": "Siswa mampu membandingkan panjang dua benda berdasarkan nilai sentimeter terukur.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Menghitung Selisih Panjang",
        "minutes": 6,
        "goal": "Siswa mampu menghitung selisih panjang dua benda menggunakan operasi pengurangan.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mengurutkan Benda Berdasarkan Panjang",
        "minutes": 6,
        "goal": "Siswa mampu mengurutkan beberapa benda dari terpendek atau terpanjang.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Membandingkan Panjang Gabungan",
        "minutes": 6,
        "goal": "Siswa mampu menghitung panjang gabungan lalu membandingkannya dengan benda lain.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membandingkan Benda Berdasarkan Panjang Terukur",
    "topic": "Mengukur Panjang dan Berat",
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
# 2. DEFINISI BANK 50 SOAL BAB 63
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
mc("c1", "mudah", D, F, S1, "Pensil A panjangnya 15 cm, pensil B 10 cm. Manakah yang lebih panjang?", ["pensil A", "pensil B", "keduanya sama", "tidak dapat diukur"], "A", "15 cm lebih panjang dari 10 cm.")
tf("c1", "mudah", D, F, S2, "Selisih panjang dua benda dicari dengan operasi pengurangan.", "Benar", "Selisih selalu dicari dengan cara mengurangkan.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Benda 7 cm dibanding benda 12 cm artinya benda 7 cm ....", ["lebih pendek", "lebih panjang", "sama panjang", "lebih berat"], "A", "7 cm lebih kecil, jadi lebih pendek.")
mc("c1", "mudah", T, F, S3, "Dari benda 4 cm, 9 cm, dan 15 cm, manakah yang paling pendek?", ["benda 4 cm", "benda 9 cm", "benda 15 cm", "semua sama"], "A", "4 cm adalah angka terkecil.")
sa("c1", "mudah", T, F, S2, "Berapakah selisih panjang antara pita 18 cm dan pita 10 cm?", "8", "18 - 10 = 8 cm.", verifikasi={"ekspresi": "18 - 10", "hasil": "8"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Urutan benda: buku 20 cm, pensil 12 cm, penghapus 4 cm dari terpendek?", ["penghapus, pensil, buku", "buku, pensil, penghapus", "pensil, penghapus, buku", "buku, penghapus, pensil"], "A", "4 cm < 12 cm < 20 cm.")
tf("c2", "mudah", D, Kn, S1, "Benda berukuran 25 cm lebih pendek daripada benda berukuran 20 cm.", "Salah", "25 cm lebih panjang dari 20 cm.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Tali A 14 cm dan tali B 9 cm. Berapa cm selisih panjang keduanya?", ["5 cm", "23 cm", "6 cm", "4 cm"], "A", "14 - 9 = 5 cm.", "Menjumlahkan bukan mengurangkan saat mencari selisih", verifikasi={"ekspresi": "14 - 9", "hasil": "5"})
mc("c2", "mudah", R, Kn, S3, "Ali mengurutkan 15 cm, 8 cm, 22 cm dari terpanjang. Urutan Ali seharusnya?", ["22 cm, 15 cm, 8 cm", "8 cm, 15 cm, 22 cm", "15 cm, 22 cm, 8 cm", "8 cm, 22 cm, 15 cm"], "A", "Dari terpanjang artinya dari angka terbesar.", "Tertukar urutan naik dan turun")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Benda A 17 cm dan Benda B 17 cm. Pernyataan yang benar adalah ....", ["kedua benda sama panjang", "benda A lebih panjang", "benda B lebih panjang", "benda A lebih pendek"], "A", "Ukuran keduanya sama persis yaitu 17 cm.")
mc("c2", "mudah", T, Kn, S4, "Dua sedotan masing-masing 6 cm disambung. Total panjangnya adalah ....", ["12 cm", "10 cm", "14 cm", "6 cm"], "A", "6 + 6 = 12 cm.", verifikasi={"ekspresi": "6 + 6", "hasil": "12"})
tf("c2", "mudah", T, Kn, S3, "Urutan 3 cm, 7 cm, 11 cm adalah urutan dari yang paling pendek.", "Benar", "3 < 7 < 11 (urutan membesar/terpendek ke terpanjang).")
sa("c2", "mudah", T, Kn, S2, "Berapakah selisih panjang antara 26 cm dan 19 cm?", "7", "26 - 19 = 7 cm.", verifikasi={"ekspresi": "26 - 19", "hasil": "7"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S4, "Tongkat 30 cm dibanding gabungan dua lidi 14 cm dan 18 cm. Manakah lebih panjang?", ["gabungan dua lidi", "tongkat 30 cm", "keduanya sama", "tidak dapat dihitung"], "A", "Lidi = 14 + 18 = 32 cm. 32 cm > 30 cm.", "Belum menjumlahkan sebelum membandingkan")
mc("c3", "sedang", R, Pr, S2, "Berapa cm selisih panjang meja 75 cm dengan kursi 48 cm?", ["27 cm", "37 cm", "23 cm", "33 cm"], "A", "75 - 48 = 27 cm.", "Salah pengurangan bersusun", verifikasi={"ekspresi": "75 - 48", "hasil": "27"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Pita merah 32 cm dan pita kuning 28 cm. Pita merah lebih panjang ... cm.", ["4 cm", "3 cm", "5 cm", "6 cm"], "A", "32 - 28 = 4 cm.", verifikasi={"ekspresi": "32 - 28", "hasil": "4"})
mc("c3", "mudah", T, Pr, S3, "Manakah urutan dari yang terpanjang: 18 cm, 35 cm, 9 cm?", ["35 cm, 18 cm, 9 cm", "9 cm, 18 cm, 35 cm", "18 cm, 35 cm, 9 cm", "35 cm, 9 cm, 18 cm"], "A", "35 > 18 > 9.")
tf("c3", "sedang", T, Pr, S2, "Selisih antara penggaris 30 cm dan pensil 13 cm adalah 17 cm.", "Benar", "30 - 13 = 17 cm.")
mc("c3", "sedang", T, Pr, S4, "Tali A (12 cm + 8 cm) dan Tali B 25 cm. Selisih keduanya adalah ....", ["5 cm", "4 cm", "6 cm", "10 cm"], "A", "25 - 20 = 5 cm.", verifikasi={"ekspresi": "25 - (12 + 8)", "hasil": "5"})
tf("c3", "sedang", T, Pr, S3, "Urutan 40 cm, 25 cm, 15 cm adalah urutan dari yang paling pendek.", "Salah", "Itu urutan dari paling panjang ke paling pendek.")
sa("c3", "sedang", T, Pr, S2, "Berapakah selisih panjang antara papan 80 cm dan papan 55 cm?", "25", "80 - 55 = 25 cm.", verifikasi={"ekspresi": "80 - 55", "hasil": "25"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Kawat A 42 cm, kawat B 39 cm. Kawat manakah yang lebih pendek?", ["kawat B", "kawat A", "keduanya sama", "tidak pasti"], "A", "39 cm lebih pendek dari 42 cm.")
mc("c3", "sedang", X, Pr, S2, "Berapakah selisih panjang antara 64 cm dan 29 cm?", ["35 cm", "45 cm", "33 cm", "37 cm"], "A", "64 - 29 = 35 cm.", verifikasi={"ekspresi": "64 - 29", "hasil": "35"})
tf("c3", "sedang", X, Pr, S4, "Dua pensil masing-masing 9 cm sama panjang dengan satu penggaris 18 cm.", "Benar", "9 + 9 = 18 cm.")
sa("c3", "sedang", X, Pr, S4, "Panjang gabungan lidi 16 cm dan lidi 24 cm adalah ... cm.", "40", "16 + 24 = 40 cm.", verifikasi={"ekspresi": "16 + 24", "hasil": "40"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Urutkan panjang berikut dari yang terpendek: 52 cm, 19 cm, 38 cm!", ["19 cm, 38 cm, 52 cm", "52 cm, 38 cm, 19 cm", "19 cm, 52 cm, 38 cm", "38 cm, 19 cm, 52 cm"], "A", "19 < 38 < 52.")
mc("c3", "sedang", K, Pr, S4, "Pita 27 cm disambung pita 33 cm. Panjangnya dibanding pita 50 cm?", ["lebih panjang 10 cm", "lebih pendek 10 cm", "sama panjang", "lebih panjang 5 cm"], "A", "27 + 33 = 60 cm; 60 - 50 = 10 cm.")

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S1
mc("c4", "sedang", T, Kn, S1, "Benda A lebih panjang dari B. B lebih panjang dari C. Hubungan A dan C?", ["benda A lebih panjang dari benda C", "benda A lebih pendek dari benda C", "benda A sama dengan C", "tidak dapat ditentukan"], "A", "Sifat transitif: jika A > B dan B > C, maka A > C.")
mc("c4", "sedang", T, Kn, S2, "Mengapa selisih panjang selalu berupa bilangan positif dalam ukuran nyata?", ["karena selisih mengukur jarak perbedaan antara dua ukuran", "karena angkanya selalu genap", "karena penggaris dari plastik", "karena tidak ada angka nol"], "A", "Selisih menyatakan besarnya perbedaan nilai.")
tf("c4", "sedang", T, Kn, S3, "Jika tiga benda diurutkan, benda di tengah pasti bukan yang terpanjang.", "Benar", "Benda di tengah nilainya di antara terkecil dan terbesar.")
tf("c4", "sedang", T, Kn, S4, "Menggabungkan dua pensil 10 cm menghasilkan ukuran lebih pendek dari pensil 15 cm.", "Salah", "10 + 10 = 20 cm, dan 20 cm lebih panjang dari 15 cm.")
sa("c4", "sedang", T, Kn, S2, "Pita 90 cm dipotong 47 cm. Berapakah selisih potongan panjang dan pendek?", "4", "Potongan: 47 cm dan (90 - 47 = 43 cm). Selisih = 47 - 43 = 4 cm.", verifikasi={"ekspresi": "47 - (90 - 47)", "hasil": "4"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Tongkat X 48 cm, Tongkat Y 53 cm, Tongkat Z 45 cm. Manakah paling panjang?", ["tongkat Y", "tongkat X", "tongkat Z", "semua sama"], "A", "53 cm adalah ukuran terbesar.")
mc("c4", "sedang", X, Kn, S3, "Urutan dari terpanjang: Benda P (31 cm), Q (44 cm), R (28 cm)?", ["Q, P, R", "P, Q, R", "R, P, Q", "Q, R, P"], "A", "44 > 31 > 28 cm.")
tf("c4", "sedang", X, Kn, S2, "Selisih antara 65 cm dan 35 cm adalah 20 cm.", "Salah", "65 - 35 = 30 cm, bukan 20 cm.")
mc("c4", "sulit", X, Me, S4, "Tali 1 meter (100 cm) dipotong 62 cm. Berapa selisih dua bagian itu?", ["24 cm", "26 cm", "28 cm", "22 cm"], "A", "Bagian 1 = 62 cm, bagian 2 = 38 cm. Selisih = 62 - 38 = 24 cm.", verifikasi={"ekspresi": "62 - (100 - 62)", "hasil": "24"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Pita A 24 cm, pita B 30 cm. Berapa kekurangan pita A agar sama?", ["6 cm", "5 cm", "7 cm", "8 cm"], "A", "30 - 24 = 6 cm.", verifikasi={"ekspresi": "30 - 24", "hasil": "6"})
mc("c4", "sulit", K, Me, S2, "Kabel 85 cm dipotong menjadi dua bagian. Satu bagian 50 cm. Selisihnya?", ["15 cm", "20 cm", "10 cm", "25 cm"], "A", "Bagian 2 = 85 - 50 = 35 cm. Selisih = 50 - 35 = 15 cm.", verifikasi={"ekspresi": "50 - (85 - 50)", "hasil": "15"})
tf("c4", "sulit", K, Me, S3, "Benda 45 cm selalu lebih pendek daripada gabungan dua benda 20 cm.", "Salah", "Gabungan dua benda 20 cm adalah 40 cm. 45 cm lebih panjang, bukan lebih pendek.")
mc("c4", "sulit", K, Me, S4, "Sedotan A 14 cm, B 16 cm, C 20 cm. Selisih (A+B) dengan C?", ["10 cm", "8 cm", "12 cm", "6 cm"], "A", "(14 + 16) - 20 = 30 - 20 = 10 cm.", verifikasi={"ekspresi": "(14 + 16) - 20", "hasil": "10"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Pita merah 40 cm. Pita biru 15 cm lebih pendek. Berapa panjang pita biru?", ["25 cm", "20 cm", "30 cm", "22 cm"], "A", "40 - 15 = 25 cm.", verifikasi={"ekspresi": "40 - 15", "hasil": "25"})
mc("c5", "sedang", T, Me, S2, "Bambu A 78 cm, bambu B 59 cm. Berapa cm bambu B harus ditambah agar sama?", ["19 cm", "18 cm", "20 cm", "21 cm"], "A", "78 - 59 = 19 cm.", verifikasi={"ekspresi": "78 - 59", "hasil": "19"})
mc("c5", "sedang", T, Me, S3, "Empat lidi: 12 cm, 25 cm, 18 cm, 30 cm. Berapakah selisih terpanjang dan terpendek?", ["18 cm", "15 cm", "20 cm", "12 cm"], "A", "30 - 12 = 18 cm.", verifikasi={"ekspresi": "30 - 12", "hasil": "18"})
mc("c5", "sulit", T, Me, S4, "Kawat 95 cm dipotong untuk 3 jemuran masing-masing 25 cm. Berapa sisa kawat?", ["20 cm", "15 cm", "25 cm", "18 cm"], "A", "95 - (3 x 25) = 95 - 75 = 20 cm.", verifikasi={"ekspresi": "95 - (3 * 25)", "hasil": "20"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Dua balok kayu selisih panjangnya 14 cm. Balok pendek 26 cm. Berapa balok panjang?", ["40 cm", "38 cm", "42 cm", "36 cm"], "A", "26 + 14 = 40 cm.", verifikasi={"ekspresi": "26 + 14", "hasil": "40"})
mc("c5", "sulit", K, Me, S4, "Tali A 45 cm, tali B 35 cm. Jika disambung lalu dipotong 52 cm, berapa sisanya?", ["28 cm", "25 cm", "30 cm", "26 cm"], "A", "(45 + 35) - 52 = 80 - 52 = 28 cm.", verifikasi={"ekspresi": "(45 + 35) - 52", "hasil": "28"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Mengapa mengurutkan ukuran panjang sangat penting saat membuat rak buku?", ["agar buku dapat tersusun rapi sesuai tinggi dan tidak terjepit", "agar catnya tidak rusak", "karena rak terbuat dari paku", "tidak ada manfaatnya"], "A", "Mengetahui urutan tinggi membuat penataan ruang buku pas.")
mc("c6", "sulit", K, Me, S4, "Pita 84 cm dipotong menjadi dua. Bagian satu 12 cm lebih panjang. Panjangnya?", ["48 cm", "42 cm", "50 cm", "46 cm"], "A", "(84 - 12) : 2 = 72 : 2 = 36 cm. Bagian panjang = 36 + 12 = 48 cm.", verifikasi={"ekspresi": "((84 - 12) / 2) + 12", "hasil": "48"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi: (3 x 25 cm) - (2 x 28 cm) + 11 cm!", ["30 cm", "28 cm", "32 cm", "25 cm"], "A", "75 - 56 + 11 = 19 + 11 = 30 cm.", verifikasi={"ekspresi": "(3 * 25) - (2 * 28) + 11", "hasil": "30"})
mc("c6", "sulit", P, Me, S3, "Tongkat A 40 cm, B 55 cm, C 35 cm. Selisih (A+C) dengan B?", ["20 cm", "15 cm", "25 cm", "18 cm"], "A", "(40 + 35) - 55 = 75 - 55 = 20 cm.", verifikasi={"ekspresi": "(40 + 35) - 55", "hasil": "20"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab63_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab63.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
