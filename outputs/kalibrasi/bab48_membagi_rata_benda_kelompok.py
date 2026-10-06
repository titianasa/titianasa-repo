#!/usr/bin/env python3
"""
Generator dan validator Bab 48 Matematika Kelas 2 SD:
"Membagi Rata Benda ke dalam Kelompok" (Fase A)
bab_id: e0067e7c-0622-4678-97a9-5f9292b622b6
article_id: b54613ce-d3cf-4c11-a9b0-cec757e85f0b
quiz_id: bf1494be-eb33-4d36-842b-e39c6dccf2bc
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "f8a9b0c1d201"  # Dua Cara Membagi Benda
S2 = "a9b0c1d2e302"  # Membagi ke Beberapa Wadah
S3 = "b0c1d2e3f403"  # Mengelompokkan Sesuai Isi
S4 = "c1d2e3f4a504"  # Latihan Gabungan Bagi Rata

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Membagi benda memiliki dua cara seru.
Cara pertama membagi ke wadah tertentu.
Cara kedua mengelompokkan sesuai isi benda.
Keduanya menghasilkan pembagian yang adil.
Semua benda habis terbagi rata.
Tidak ada benda yang tersisa.
Mari kita pelajari kedua caranya!

:::definition
title: Pembagian Kelompok
Pembagian kelompok adalah menata benda secara adil ke dalam beberapa kumpulan.
:::"""

s2_content = """Cara pertama: wadah sudah diketahui.
Kamu mencari berapa isi tiap wadah.
Ada dua belas butir kelereng.
Dibagikan ke dalam tiga kantong.
Bagi satu per satu bergantian.
Tiap kantong mendapat empat butir.
Dua belas bagi tiga sama dengan empat.
Setiap kantong terisi sama rata!

:::steps
title: Membagi ke Dalam Wadah
1. Siapkan semua wadah yang ada.
2. Masukkan satu benda ke tiap wadah.
3. Ulangi sampai semua benda habis.
:::"""

s3_content = """Cara kedua: isi wadah sudah ditentukan.
Kamu mencari berapa wadah yang dibutuhkan.
Ada lima belas kue lezat.
Tiap piring diisi lima kue.
Ambil lima kue untuk piring pertama.
Ambil lima kue untuk piring kedua.
Ambil lima kue untuk piring ketiga.
Kue habis dalam tiga piring.
Lima belas bagi lima sama dengan tiga!"""

s4_content = """Kedua cara menghasilkan angka sama.
Dua belas bagi tiga adalah empat.
Dua belas bagi empat adalah tiga.
Keduanya saling berkaitan erat.
Perhatikan apa yang ditanyakan soal.
Apakah mencari isi atau wadah?
Membaca dengan teliti adalah kuncinya!

:::common_trap
title: Salah Menentukan Hasil
Jangan bingung antara wadah dan isi.
Dua belas bagi tiga artinya empat per wadah.
Bukan tiga kelereng per wadah!
Perhatikan pembagi pada soal cerita.
:::

:::callout
variant: summary
title: Ringkasan
text: Membagi rata bisa mencari banyaknya isi wadah atau mencari banyaknya wadah yang dibutuhkan.
:::"""

sections = [
    {
        "id": S1,
        "title": "Dua Cara Membagi Benda",
        "minutes": 6,
        "goal": "Siswa memahami dua makna pembagian: membagi ke sejumlah wadah (partitif) dan mengelompokkan sesuai isi (kuotatif).",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Membagi ke Beberapa Wadah",
        "minutes": 6,
        "goal": "Siswa mampu menentukan isi tiap wadah jika jumlah benda dan banyak wadah sudah diketahui.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mengelompokkan Sesuai Isi",
        "minutes": 6,
        "goal": "Siswa mampu menentukan banyaknya wadah yang dibutuhkan jika isi tiap wadah sudah ditentukan.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Latihan Gabungan Bagi Rata",
        "minutes": 6,
        "goal": "Siswa mampu menyelesaikan masalah kontekstual pembagian kelompok benda secara terpadu.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membagi Rata Benda ke dalam Kelompok",
    "topic": "Mengenal Perkalian dan Pembagian",
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
# 2. DEFINISI BANK 50 SOAL BAB 48
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
mc("c1", "mudah", D, F, S1, "Membagi benda secara adil artinya setiap wadah berisi benda ....", ["sama banyak", "berbeda-beda", "acak", "selalu sepuluh"], "A", "Pembagian adil mewajibkan isi tiap wadah sama banyak.")
tf("c1", "mudah", D, F, S2, "Ada 8 kue dibagi ke 2 piring. Tiap piring mendapat 4 kue.", "Benar", "8 : 2 = 4 kue tiap piring.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Ada 10 apel dimasukkan ke dalam 5 kantong. Tiap kantong berisi ....", ["2 apel", "3 apel", "5 apel", "1 apel"], "A", "10 : 5 = 2 apel per kantong.", verifikasi={"ekspresi": "10 / 5", "hasil": "2"})
mc("c1", "mudah", T, F, S3, "Ada 12 pensil. Tiap kotak diisi 4 pensil. Banyak kotak yang dibutuhkan adalah ....", ["3 kotak", "4 kotak", "2 kotak", "5 kotak"], "A", "12 : 4 = 3 kotak.", verifikasi={"ekspresi": "12 / 4", "hasil": "3"})
sa("c1", "mudah", T, F, S4, "Berapakah hasil dari 14 : 7?", "2", "14 : 7 = 2.", verifikasi={"ekspresi": "14 / 7", "hasil": "2"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Ibu punya 16 jeruk. Tiap kantong diisi 4 jeruk. Berapa kantong yang dipakai?", ["4 kantong", "3 kantong", "5 kantong", "2 kantong"], "A", "16 : 4 = 4 kantong.", verifikasi={"ekspresi": "16 / 4", "hasil": "4"})
tf("c2", "mudah", D, Kn, S1, "Membagi benda ke wadah sama dengan mengelompokkan benda sesuai isi.", "Benar", "Keduanya adalah bentuk pembagian adil yang saling berkaitan.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Ada 15 kelereng dibagi rata ke 3 anak. Berapa butir tiap anak?", ["5 butir", "3 butir", "4 butir", "6 butir"], "A", "15 : 3 = 5 butir.", "Tertukar banyak anak dengan banyak isi", verifikasi={"ekspresi": "15 / 3", "hasil": "5"})
mc("c2", "mudah", R, Kn, S3, "Ada 18 buku. Tiap tas diisi 6 buku. Berapa tas yang dibutuhkan?", ["3 tas", "4 tas", "2 tas", "5 tas"], "A", "18 : 6 = 3 tas.", "Salah menghitung pembagian wadah", verifikasi={"ekspresi": "18 / 6", "hasil": "3"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Manakah pernyataan yang menunjukkan kegiatan membagi rata ke dalam kelompok?", ["membagi 12 permen ke 3 anak masing-masing 4", "memberi anak pertama 5 dan anak kedua 7", "mengumpulkan semua permen", "memakan permen bersama"], "A", "Membagi 12 permen masing-masing 4 adalah pembagian rata.")
mc("c2", "mudah", T, Kn, S2, "Ada 16 donat dibagikan ke 4 kotak sama banyak. Isi tiap kotak adalah ....", ["4 donat", "5 donat", "3 donat", "6 donat"], "A", "16 : 4 = 4 donat.", verifikasi={"ekspresi": "16 / 4", "hasil": "4"})
tf("c2", "mudah", T, Kn, S3, "Ada 20 kelereng dimasukkan ke kantong isi 5 kelereng. Butuh 5 kantong.", "Salah", "20 : 5 = 4 kantong, bukan 5 kantong.")
sa("c2", "mudah", T, Kn, S4, "Berapakah hasil dari 18 : 2?", "9", "18 : 2 = 9.", verifikasi={"ekspresi": "18 / 2", "hasil": "9"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Ada 20 kue dimasukkan ke 4 toples sama rata. Berapa isi tiap toples?", ["5 kue", "4 kue", "6 kue", "3 kue"], "A", "20 : 4 = 5 kue per toples.", "Salah menghitung bagi empat", verifikasi={"ekspresi": "20 / 4", "hasil": "5"})
mc("c3", "sedang", R, Pr, S3, "Ada 24 mangga. Tiap keranjang isi 6 mangga. Berapa keranjang?", ["4 keranjang", "3 keranjang", "5 keranjang", "6 keranjang"], "A", "24 : 6 = 4 keranjang.", "Salah menentukan banyak kelompok", verifikasi={"ekspresi": "24 / 6", "hasil": "4"})

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berapakah hasil dari 21 : 3?", ["7", "6", "8", "5"], "A", "21 : 3 = 7.", verifikasi={"ekspresi": "21 / 3", "hasil": "7"})
mc("c3", "mudah", T, Pr, S3, "Ada 25 bunga. Tiap vas ada 5 bunga. Berapa vas bunga yang dibutuhkan?", ["5 vas", "4 vas", "6 vas", "3 vas"], "A", "25 : 5 = 5 vas.", verifikasi={"ekspresi": "25 / 5", "hasil": "5"})
tf("c3", "sedang", T, Pr, S2, "Membagi 18 benda ke 3 wadah menghasilkan 9 benda tiap wadah.", "Salah", "18 : 3 = 6 bukan 9.")
mc("c3", "sedang", T, Pr, S4, "Ada 24 roti dibagi sama rata kepada 6 anak. Berapa roti tiap anak?", ["4 roti", "3 roti", "5 roti", "6 roti"], "A", "24 : 6 = 4 roti.", verifikasi={"ekspresi": "24 / 6", "hasil": "4"})
tf("c3", "sedang", T, Pr, S3, "Membagi 24 benda ke kelompok isi 4 butuh 8 kelompok.", "Salah", "24 : 4 = 6 kelompok, bukan 8 kelompok.")
sa("c3", "sedang", T, Pr, S4, "Berapakah hasil dari 28 : 4?", "7", "28 : 4 = 7.", verifikasi={"ekspresi": "28 / 4", "hasil": "7"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Ada 27 kelereng dibagi rata ke 3 anak. Berapa kelereng tiap anak?", ["9 butir", "8 butir", "7 butir", "6 butir"], "A", "27 : 3 = 9 butir.", verifikasi={"ekspresi": "27 / 3", "hasil": "9"})
mc("c3", "sedang", X, Pr, S2, "Sebanyak 30 telur dimasukkan ke 5 wadah sama rata. Berapa telur per wadah?", ["6 butir", "5 butir", "7 butir", "8 butir"], "A", "30 : 5 = 6 butir.", verifikasi={"ekspresi": "30 / 5", "hasil": "6"})
tf("c3", "sedang", X, Pr, S4, "Hasil dari 30 : 3 sama dengan hasil dari 20 : 2 yaitu 10.", "Benar", "30 : 3 = 10 dan 20 : 2 = 10.")
sa("c3", "sedang", X, Pr, S3, "Berapakah hasil dari 27 : 9?", "3", "27 : 9 = 3.", verifikasi={"ekspresi": "27 / 9", "hasil": "3"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Ada 32 permen dibagikan rata ke 4 anak. Berapa permen tiap anak?", ["8 permen", "7 permen", "9 permen", "6 permen"], "A", "32 : 4 = 8 permen.", verifikasi={"ekspresi": "32 / 4", "hasil": "8"})
mc("c3", "sedang", K, Pr, S3, "Ada 30 buku diikat masing-masing 6 buku. Berapa ikatan buku?", ["5 ikatan", "4 ikatan", "6 ikatan", "7 ikatan"], "A", "30 : 6 = 5 ikatan.", verifikasi={"ekspresi": "30 / 6", "hasil": "5"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Apa beda membagi ke 3 piring dengan membagi tiap piring isi 3?", ["soal pertama mencari isi per piring, soal kedua mencari banyak piring", "keduanya sama persis pertanyaannya", "soal pertama perkalian, soal kedua pembagian", "tidak ada perbedaan"], "A", "Yang satu mencari isi (partitif), yang satu mencari wadah (kuotatif).")
mc("c4", "sedang", T, Kn, S2, "Lina punya 24 pita, dipotong sama panjang menjadi 4 bagian. Berapa panjang tiap pita?", ["6 meter", "5 meter", "7 meter", "8 meter"], "A", "24 : 4 = 6 meter.", verifikasi={"ekspresi": "24 / 4", "hasil": "6"})
tf("c4", "sedang", T, Kn, S3, "Jika isi per kelompok makin banyak, maka wadah yang dibutuhkan makin sedikit.", "Benar", "Makin banyak isi tiap wadah, wadah yang dibutuhkan berkurang.")
tf("c4", "sedang", T, Kn, S4, "Hasil dari 28 : 7 lebih besar daripada hasil 24 : 4.", "Salah", "28 : 7 = 4, sedangkan 24 : 4 = 6. 4 lebih kecil dari 6.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari (36 : 4) + 3?", "12", "36 : 4 = 9; 9 + 3 = 12.", verifikasi={"ekspresi": "(36 / 4) + 3", "hasil": "12"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Budi punya 20 ikan. Ia punya 4 akuarium. Berapa isi tiap akuarium?", ["5 ekor", "4 ekor", "6 ekor", "3 ekor"], "A", "20 : 4 = 5 ekor ikan.", verifikasi={"ekspresi": "20 / 4", "hasil": "5"})
mc("c4", "sedang", X, Kn, S3, "Pak Tani panen 35 semangka. Dimasukkan keranjang isi 5 semangka. Berapa keranjang?", ["7 keranjang", "6 keranjang", "8 keranjang", "5 keranjang"], "A", "35 : 5 = 7 keranjang.", verifikasi={"ekspresi": "35 / 5", "hasil": "7"})
tf("c4", "sedang", X, Kn, S2, "Membagi 16 jeruk ke 2 piring menghasilkan lebih banyak daripada 32 jeruk ke 4 piring.", "Salah", "16 : 2 = 8 dan 32 : 4 = 8, keduanya bernilai sama besar.")
mc("c4", "sulit", X, Me, S4, "Manakah dari pembagian berikut yang menghasilkan nilai PALING BESAR?", ["32 : 4", "30 : 5", "28 : 7", "24 : 6"], "A", "32 : 4 = 8; 30 : 5 = 6; 28 : 7 = 4; 24 : 6 = 4. Paling besar 8.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Siti membagikan 24 jeruk ke 8 piring sama rata. Tiap piring mendapat ....", ["3 jeruk", "4 jeruk", "2 jeruk", "5 jeruk"], "A", "24 : 8 = 3 jeruk.", verifikasi={"ekspresi": "24 / 8", "hasil": "3"})
mc("c4", "sulit", K, Me, S3, "Di kelas ada 32 siswa. Dibentuk kelompok belajar isi 4 orang. Berapa kelompok terbentuk?", ["8 kelompok", "7 kelompok", "9 kelompok", "6 kelompok"], "A", "32 : 4 = 8 kelompok.", verifikasi={"ekspresi": "32 / 4", "hasil": "8"})
tf("c4", "sulit", K, Me, S4, "Hasil dari 36 : 6 dua kali lipat lebih besar dari hasil 18 : 6.", "Benar", "36 : 6 = 6 dan 18 : 6 = 3. 6 adalah dua kali dari 3.")
mc("c4", "sulit", K, Me, S4, "Berapakah hasil dari (40 : 5) - (18 : 3)?", ["2", "3", "4", "1"], "A", "40 : 5 = 8; 18 : 3 = 6; 8 - 6 = 2.", verifikasi={"ekspresi": "(40 / 5) - (18 / 3)", "hasil": "2"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Ada 28 permen dibagikan ke beberapa kantong isi 7 permen. Kalimat pembagian yang benar?", ["28 : 7 = 4", "28 : 4 = 7", "28 - 7 = 21", "28 + 7 = 35"], "A", "28 permen dikelompokkan per 7: 28 : 7 = 4 kantong.")
mc("c5", "sedang", T, Me, S2, "Berapakah nilai Y pada kalimat matematika: 35 : Y = 7?", ["5", "6", "4", "7"], "A", "35 : 5 = 7, jadi Y = 5.", verifikasi={"ekspresi": "35 / 7", "hasil": "5"})
mc("c5", "sedang", T, Me, S3, "Berapakah nilai Z pada kalimat matematika: Z : 6 = 5?", ["30", "25", "36", "24"], "A", "30 : 6 = 5, jadi Z = 30.", verifikasi={"ekspresi": "6 * 5", "hasil": "30"})
mc("c5", "sulit", T, Me, S4, "Berapakah hasil dari (30 : 5) + (24 : 4)?", ["12", "10", "14", "11"], "A", "30 : 5 = 6; 24 : 4 = 6; 6 + 6 = 12.", verifikasi={"ekspresi": "(30 / 5) + (24 / 4)", "hasil": "12"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Berapakah nilai X pada kalimat matematika: 36 : X = 9?", ["4", "3", "5", "6"], "A", "36 : 4 = 9, jadi X = 4.", verifikasi={"ekspresi": "36 / 9", "hasil": "4"})
mc("c5", "sulit", K, Me, S4, "Berapakah hasil dari (45 : 5) - (21 : 3)?", ["2", "3", "1", "4"], "A", "45 : 5 = 9; 21 : 3 = 7; 9 - 7 = 2.", verifikasi={"ekspresi": "(45 / 5) - (21 / 3)", "hasil": "2"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Kesimpulan apa yang didapat dari 24 : 4 = 6 dan 24 : 6 = 4?", ["wadah dan isi dapat saling bertukar posisi", "pembagian tidak punya aturan", "hasilnya selalu berbeda", "angka 24 tidak bisa dibagi bilangan lain"], "A", "Banyak wadah dan isi per wadah memiliki sifat timbal balik yang setara.")
mc("c6", "sulit", K, Me, S3, "Jika 30 buku dimasukkan ke N tas masing-masing 5 buku, berapakah nilai N?", ["6 tas", "5 tas", "7 tas", "4 tas"], "A", "N = 30 : 5 = 6 tas.", verifikasi={"ekspresi": "30 / 5", "hasil": "6"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi campuran: (40 : 4) - (15 : 3) + (18 : 2)!", ["14", "12", "16", "10"], "A", "40 : 4 = 10; 15 : 3 = 5; 18 : 2 = 9; 10 - 5 + 9 = 14.", verifikasi={"ekspresi": "(40 / 4) - (15 / 3) + (18 / 2)", "hasil": "14"})
mc("c6", "sulit", P, Me, S4, "Ada 36 spidol dibagi ke 6 kotak. Satu kotak hilang. Berapa spidol tersisa?", ["30 spidol", "24 spidol", "32 spidol", "28 spidol"], "A", "36 : 6 = 6 spidol per kotak; sisa 5 kotak = 5 x 6 = 30 spidol.", verifikasi={"ekspresi": "36 - (36 / 6)", "hasil": "30"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab48_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab48.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
