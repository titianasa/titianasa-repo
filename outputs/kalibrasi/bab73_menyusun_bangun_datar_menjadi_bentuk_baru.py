#!/usr/bin/env python3
"""
Generator dan validator Bab 73 Matematika Kelas 2 SD:
"Menyusun Bangun Datar Menjadi Bentuk Baru" (Fase A)
bab_id: af96890e-6965-4c4e-8f99-fd0fd0483127
article_id: c6716e96-721e-4452-bc22-48f42520274a
quiz_id: 3dc8bef0-ebc5-411e-815b-c308506e3cc8
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "r1t2v3x4z501"  # Menggabungkan Dua Bangun Datar
S2 = "s2u3w4y5a602"  # Menyusun Bentuk Objek dari Potongan
S3 = "t3v4x5z6b703"  # Mengenal Tangram dan Pola
S4 = "u4w5y6a7c804"  # Memotong dan Mengurai Bangun Datar

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Bangun datar dapat digabungkan.
Dua bangun kecil menjadi bangun besar.
Dua segitiga sama kaki digabung.
Keduanya dapat membentuk satu persegi.
Dua persegi ditaruh berdampingan.
Keduanya membentuk satu persegi panjang.
Sisi-sisi yang menempel menjadi satu.
Bentuk baru pun segera tercipta!

:::definition
title: Penggabungan Bangun Datar
Menyatukan dua atau lebih bidang datar hingga membentuk bangun baru.
:::"""

s2_content = """Kita bisa membuat gambar rumah.
Atap rumah berbentuk bangun segitiga.
Dinding rumah berbentuk bangun segiempat.
Pintu rumah berbentuk persegi panjang kecil.
Kita juga bisa membuat perahu.
Badan perahu dari trapesium segiempat.
Layarnya tersusun dari dua segitiga.
Menyusun bangun datar sangat menyenangkan!

:::steps
title: Langkah Menyusun Objek
1. Pilih kepingan bangun datar yang sesuai.
2. Pasang bagian dasar objek terlebih dahulu.
3. Tempelkan kepingan lain di atasnya.
:::"""

s3_content = """Ada permainan bernama tangram.
Tangram adalah teka-teki kuno.
Tangram terdiri dari 7 kepingan.
Ada 5 keping bentuk segitiga.
Ada 1 keping bentuk persegi.
Ada 1 keping jajar genjang.
Ketujuh keping dapat disusun bebas.
Bisa menjadi burung, ikan, atau manusia!

:::common_trap
title: Mengira Bangun Baru Selalu Bertambah Sisinya
Dua sisi yang saling berimpit menempel.
Sisi tempelan tidak lagi dihitung luar.
Bangun baru sisinya tidak selalu banyak!
:::"""

s4_content = """Bangun datar juga dapat dipotong.
Satu kertas persegi dilipat menyilang.
Gunting lipatan itu di tengahnya.
Satu persegi menjadi dua segitiga.
Persegi panjang dapat dipotong lurus.
Hasilnya adalah dua persegi kecil.
Memotong bangun datar menghasilkan bentuk baru.
Cobalah berkreasi dengan kertas lipat!

:::callout
variant: summary
title: Ringkasan
text: Gabungkan bangun untuk mencipta. Potong bangun untuk mengurai bentuk.
:::"""

sections = [
    {
        "id": S1,
        "title": "Menggabungkan Dua Bangun Datar",
        "minutes": 6,
        "goal": "Siswa memahami bahwa dua bangun datar dapat digabungkan membentuk bangun baru.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Menyusun Bentuk Objek dari Potongan",
        "minutes": 6,
        "goal": "Siswa dapat menyusun berbagai bangun datar menjadi bentuk objek kreatif (rumah, perahu).",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mengenal Tangram dan Pola",
        "minutes": 6,
        "goal": "Siswa mengenal permainan teka-teki tangram dan keping penyusunnya.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Memotong dan Mengurai Bangun Datar",
        "minutes": 6,
        "goal": "Siswa memahami dekomposisi atau pemotongan bangun datar menjadi beberapa bagian.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Menyusun Bangun Datar Menjadi Bentuk Baru",
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
# 2. DEFINISI BANK 50 SOAL BAB 73
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
mc("c1", "mudah", D, F, S3, "Berapa jumlah total kepingan pada permainan teka-teki tangram?", ["7 keping", "5 keping", "6 keping", "8 keping"], "A", "Tangram memiliki 7 kepingan.", verifikasi={"ekspresi": "5 + 1 + 1", "hasil": "7"})
tf("c1", "mudah", D, F, S1, "Dua segitiga sama besar dapat digabungkan membentuk bangun segiempat.", "Benar", "Dua segitiga dapat digabung menjadi persegi atau persegi panjang.")

# Terarah (3): S1, S2, S4
mc("c1", "mudah", T, F, S1, "Bila dua persegi sama besar dijejerkan menempel, terbentuk bangun ....", ["persegi panjang", "segitiga", "lingkaran", "segilima"], "A", "Dua persegi berdampingan membentuk persegi panjang.")
mc("c1", "mudah", T, F, S2, "Bangun datar yang cocok untuk menggambar atap rumah adalah ....", ["segitiga", "lingkaran", "persegi panjang", "oval"], "A", "Atap rumah umumnya berbentuk segitiga.")
sa("c1", "mudah", T, F, S3, "Pada tangram, kepingan berbentuk segitiga ada sebanyak ... buah.", "5", "Tangram memuat 5 keping segitiga.", verifikasi={"ekspresi": "7 - 2", "hasil": "5"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Kertas persegi dipotong diagonal dari pojok ke pojok menjadi ....", ["2 segitiga", "2 persegi", "2 lingkaran", "3 segiempat"], "A", "Potongan diagonal menghasilkan 2 buah segitiga.", verifikasi={"ekspresi": "1 * 2", "hasil": "2"})
tf("c2", "mudah", D, Kn, S3, "Semua kepingan pada tangram memiliki bentuk yang sama persis.", "Salah", "Keping tangram terdiri dari segitiga, persegi, dan jajar genjang.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Berapa banyak persegi kecil dibutuhkan untuk membuat persegi 2x2?", ["4 persegi", "2 persegi", "3 persegi", "5 persegi"], "A", "2 x 2 = 4 persegi kecil.", "Mengira butuh hanya 2 persegi", verifikasi={"ekspresi": "2 * 2", "hasil": "4"})
mc("c2", "mudah", R, Kn, S4, "Jika persegi panjang dipotong lurus di tengah, diperoleh 2 bangun ....", ["persegi", "segitiga", "lingkaran", "segilima"], "A", "Bisa menghasilkan 2 persegi kecil.", "Menjawab segitiga padahal dipotong tegak lurus")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S2, "Untuk menggambar perahu layar, layar perahu dibuat dari bangun ....", ["segitiga", "lingkaran", "persegi", "segienam"], "A", "Layar perahu berbentuk segitiga.")
mc("c2", "mudah", T, Kn, S3, "Ada berapa keping persegi pada satu set permainan tangram lengkap?", ["1 keping", "2 keping", "3 keping", "0 keping"], "A", "Hanya ada 1 keping persegi.", verifikasi={"ekspresi": "1 * 1", "hasil": "1"})
tf("c2", "mudah", T, Kn, S4, "Satu bangun segiempat selalu dapat dipecah menjadi dua segitiga.", "Benar", "Tarik garis diagonal untuk membaginya jadi 2 segitiga.")
sa("c2", "mudah", T, Kn, S1, "Dua buah segitiga siku-siku sama besar digabung membentuk ... bangun persegi.", "1", "Dua segitiga siku-siku membentuk 1 persegi.", verifikasi={"ekspresi": "2 / 2", "hasil": "1"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Tiga persegi satuan dijejerkan lurus. Berapa banyak sisi luar bangun baru?", ["8 sisi", "12 sisi", "10 sisi", "6 sisi"], "A", "Panjang 3, lebar 1. Keliling = 2 x (3+1) = 8 sisi.", "Menjumlahkan semua sisi tanpa membuang sisi tempel", verifikasi={"ekspresi": "2 * (3 + 1)", "hasil": "8"})
mc("c3", "sedang", R, Pr, S4, "Sebuah karton persegi dipotong menjadi 4 segitiga. Berapa kali lipatan diagonal?", ["2 kali", "1 kali", "3 kali", "4 kali"], "A", "2 lipatan diagonal membagi persegi jadi 4 segitiga.", "Menjawab 4 kali lipatan", verifikasi={"ekspresi": "4 / 2", "hasil": "2"})

# Terarah (6): S1, S2, S3, S4, S2, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berapa banyak segitiga kecil yang menyusun bangun pada gambar 2 persegi?", ["4 segitiga", "2 segitiga", "6 segitiga", "8 segitiga"], "A", "Tiap persegi butuh 2 segitiga, 2 x 2 = 4 segitiga.", verifikasi={"ekspresi": "2 * 2", "hasil": "4"})
mc("c3", "mudah", T, Pr, S2, "Siti membuat 3 gambar rumah. Tiap rumah butuh 1 segitiga. Berapa segitiga?", ["3 segitiga", "2 segitiga", "4 segitiga", "6 segitiga"], "A", "3 x 1 = 3 segitiga.", verifikasi={"ekspresi": "3 * 1", "hasil": "3"})
tf("c3", "sedang", T, Pr, S1, "Menggabungkan dua persegi panjang selalu menghasilkan bentuk lingkaran.", "Salah", "Gabungan dua persegi panjang tetap menghasilkan bangun bersegi lurus.")
mc("c3", "sedang", T, Pr, S3, "Berapa keping jajar genjang yang terdapat pada permainan tangram?", ["1 keping", "2 keping", "3 keping", "4 keping"], "A", "Ada tepat 1 keping jajar genjang.", verifikasi={"ekspresi": "1 * 1", "hasil": "1"})
tf("c3", "sedang", T, Pr, S4, "Memotong selembar kertas persegi dapat menghasilkan 4 persegi kecil.", "Benar", "Lipat bagi dua horizontal dan vertikal.")
sa("c3", "sedang", T, Pr, S1, "Empat buah persegi disusun 2 baris dan 2 kolom membentuk ... persegi besar.", "1", "Susunan 2x2 membentuk 1 persegi besar.", verifikasi={"ekspresi": "4 / 4", "hasil": "1"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Berapa banyak persegi kecil untuk membentuk persegi panjang ukuran 2x3?", ["6 persegi", "5 persegi", "4 persegi", "8 persegi"], "A", "2 x 3 = 6 persegi kecil.", verifikasi={"ekspresi": "2 * 3", "hasil": "6"})
mc("c3", "sedang", X, Pr, S2, "Budi membuat roket dari 1 segitiga dan 2 segiempat. Berapa bangun datar?", ["3 bangun", "2 bangun", "4 bangun", "5 bangun"], "A", "1 + 2 = 3 bangun datar.", verifikasi={"ekspresi": "1 + 2", "hasil": "3"})
tf("c3", "sedang", X, Pr, S3, "Jumlah keping bukan segitiga pada tangram berjumlah tepat 2 keping.", "Benar", "1 persegi + 1 jajar genjang = 2 keping.")
sa("c3", "sedang", X, Pr, S4, "Sebuah persegi panjang dipotong lurus melintang menjadi ... bagian segiempat.", "2", "Potongan membagi menjadi 2 bagian.", verifikasi={"ekspresi": "1 * 2", "hasil": "2"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Berapa buah segitiga siku-siku sama besar untuk menyusun 1 persegi?", ["2 segitiga", "3 segitiga", "4 segitiga", "1 segitiga"], "A", "Butuh 2 segitiga siku-siku.", verifikasi={"ekspresi": "2 * 1", "hasil": "2"})
mc("c3", "sedang", K, Pr, S3, "Dari 7 keping tangram, 5 adalah segitiga. Berapa keping yang bukan segitiga?", ["2 keping", "3 keping", "1 keping", "4 keping"], "A", "7 - 5 = 2 keping.", verifikasi={"ekspresi": "7 - 5", "hasil": "2"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S1
mc("c4", "sedang", T, Kn, S1, "Ketika dua segitiga digabung menjadi persegi, ke mana perginya 2 sisi hipotenusa?", ["menjadi garis batas di dalam bidang yang saling berimpit", "hilang menguap", "patah menjadi sudut", "berubah jadi lingkaran"], "A", "Kedua sisi saling menempel di dalam sehingga menjadi satu kesatuan bidang.")
mc("c4", "sedang", T, Kn, S2, "Mengapa kita bisa membentuk gambar kucing atau burung dari keping tangram?", ["karena bentuk geometris dapat dirangkai meniru siluet hewan", "karena kepingannya hidup", "karena ada lem ajaib", "karena warnanya hitam"], "A", "Kombinasi sudut dan sisi bangun datar dapat membentuk berbagai siluet.")
tf("c4", "sedang", T, Kn, S3, "Pada tangram, ukuran kelima segitiga penyusunnya semuanya sama besar.", "Salah", "Ada 2 segitiga besar, 1 sedang, dan 2 segitiga kecil.")
tf("c4", "sedang", T, Kn, S4, "Memotong pojok kertas segiempat akan mengurangi jumlah sudut kertas tersebut.", "Salah", "Memotong pojok justru menambah 1 sudut baru sehingga menjadi 5 sudut.")
sa("c4", "sedang", T, Kn, S2, "Untuk membuat 5 rumah mainan, dibutuhkan atap segitiga sebanyak ... buah.", "5", "5 x 1 = 5 atap segitiga.", verifikasi={"ekspresi": "5 * 1", "hasil": "5"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Tersedia 8 segitiga kecil sama besar. Berapa persegi dapat dibuat?", ["4 persegi", "3 persegi", "2 persegi", "5 persegi"], "A", "8 : 2 = 4 persegi.", verifikasi={"ekspresi": "8 / 2", "hasil": "4"})
mc("c4", "sedang", X, Kn, S3, "Ada 2 set tangram lengkap. Berapa total keping segitiga dari kedua set?", ["10 segitiga", "7 segitiga", "14 segitiga", "8 segitiga"], "A", "2 x 5 = 10 segitiga.", verifikasi={"ekspresi": "2 * 5", "hasil": "10"})
tf("c4", "sedang", X, Kn, S2, "Susunan kepingan datar pada tangram boleh saling menumpuk satu sama lain.", "Salah", "Aturan tangram semua keping harus berdampingan rata tanpa menumpuk.")
mc("c4", "sulit", X, Me, S4, "Kertas segilima dipotong lurus membelah dua. Salah satu potongan bersisi 3. Potongan lain?", ["bersisi 4 (segiempat)", "bersisi 5", "bersisi 2", "bersisi 6"], "A", "Garis potong menambah sisi pada kedua belahan: 1 segitiga dan 1 segiempat.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Ada 12 segitiga siku-siku sama besar. Berapa persegi panjang 2 keping yang jadi?", ["6 persegi panjang", "4 persegi panjang", "8 persegi panjang", "12 persegi panjang"], "A", "12 : 2 = 6 bangun.", verifikasi={"ekspresi": "12 / 2", "hasil": "6"})
mc("c4", "sulit", K, Me, S2, "Siswa membuat gambar kereta: 1 lokomotif (segiempat), 4 gerbong (segiempat). Berapa roda bulat?", ["10 roda", "8 roda", "6 roda", "12 roda"], "A", "Tiap gerbong/lokomotif 2 roda = 5 x 2 = 10 roda.", verifikasi={"ekspresi": "5 * 2", "hasil": "10"})
tf("c4", "sulit", K, Me, S3, "Dua segitiga kecil pada tangram jika digabung besarnya sama dengan segitiga sedang.", "Benar", "2 segitiga kecil tangram sama persis luasnya dengan 1 segitiga sedang.")
mc("c4", "sulit", K, Me, S4, "Sebuah persegi dipotong diagonal, lalu tiap bagian dipotong lagi. Berapa segitiga?", ["4 segitiga", "2 segitiga", "6 segitiga", "8 segitiga"], "A", "2 x 2 = 4 segitiga.", verifikasi={"ekspresi": "2 * 2", "hasil": "4"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Berapa banyak segitiga siku-siku dibutuhkan untuk membuat persegi ukuran 4x4?", ["32 segitiga", "16 segitiga", "24 segitiga", "8 segitiga"], "A", "16 persegi satuan x 2 = 32 segitiga.", verifikasi={"ekspresi": "16 * 2", "hasil": "32"})
mc("c5", "sedang", T, Me, S2, "Sebuah hiasan bunga tersusun dari 1 pusat segilima dan 5 kelopak segitiga. Total sisi luar?", ["10 sisi", "15 sisi", "12 sisi", "8 sisi"], "A", "Tiap kelopak menyisakan 2 sisi luar: 5 x 2 = 10 sisi luar.", verifikasi={"ekspresi": "5 * 2", "hasil": "10"})
mc("c5", "sedang", T, Me, S3, "Bila ada 3 kotak tangram, berapakah jumlah seluruh kepingan dari ketiga kotak?", ["21 keping", "18 keping", "24 keping", "15 keping"], "A", "3 x 7 = 21 keping.", verifikasi={"ekspresi": "3 * 7", "hasil": "21"})
mc("c5", "sulit", T, Me, S4, "Selembar karton dipotong jadi 3 persegi. Tiap persegi dipotong jadi 2 segitiga. Berapa segitiga?", ["6 segitiga", "5 segitiga", "8 segitiga", "4 segitiga"], "A", "3 x 2 = 6 segitiga.", verifikasi={"ekspresi": "3 * 2", "hasil": "6"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Berapa banyak persegi satuan yang dibutuhkan untuk menyusun balok lantai 4x5?", ["20 persegi", "18 persegi", "22 persegi", "25 persegi"], "A", "4 x 5 = 20 persegi satuan.", verifikasi={"ekspresi": "4 * 5", "hasil": "20"})
mc("c5", "sulit", K, Me, S3, "Empat set tangram dikumpulkan. Berapa selisih jumlah keping segitiga dan persegi?", ["16 keping", "12 keping", "20 keping", "8 keping"], "A", "(4 x 5) - (4 x 1) = 20 - 4 = 16 keping.", verifikasi={"ekspresi": "(4 * 5) - (4 * 1)", "hasil": "16"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Rancanglah sebuah rumah mainan: bagaimana memanfaatkan 7 keping tangram tanpa sisa?", ["gunakan 2 segitiga besar untuk atap, persegi dan jajar genjang untuk dinding dan cerobong", "buang keping yang sulit", "tumpuk saja di belakang", "potong kepingnya"], "A", "Semua keping dapat disusun membentuk komposisi rumah utuh.")
mc("c6", "sulit", K, Me, S4, "Bagaimana membagi selembar kertas segienam beraturan menjadi 6 bangun segitiga sama sisi?", ["menghubungkan setiap titik sudut ke titik pusat tengah segienam", "memotong lurus dari sisi kiri ke kanan", "melipatnya secara sembarang", "tidak bisa dibagi segitiga"], "A", "Garis dari titik pusat ke 6 sudut membentuk 6 segitiga sama sisi.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Hitung total potongan: 5 persegi dipotong jadi segitiga + 4 persegi panjang dipotong 2 persegi!", ["18 potongan", "16 potongan", "20 potongan", "14 potongan"], "A", "(5 x 2) + (4 x 2) = 10 + 8 = 18 potongan.", verifikasi={"ekspresi": "(5 * 2) + (4 * 2)", "hasil": "18"})
mc("c6", "sulit", P, Me, S3, "Sebuah mosaik dibuat dari 6 set tangram lengkap. Berapa total seluruh kepingnya?", ["42 keping", "36 keping", "48 keping", "40 keping"], "A", "6 x 7 = 42 keping.", verifikasi={"ekspresi": "6 * 7", "hasil": "42"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab73_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab73.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")

