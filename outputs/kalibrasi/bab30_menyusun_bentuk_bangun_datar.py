#!/usr/bin/env python3
"""
Generator dan validator Bab 30 Matematika Kelas 1 SD:
"Menyusun Bentuk dari Bangun Datar" (Fase A)
bab_id: af49d609-ee5b-47e1-81f3-c69ec04796d0
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "b1c2d33e4f01"  # Menggabung Dua Bangun Datar
S2 = "c2d3e44f5a12"  # Menyusun Gambar Benda Menarik
S3 = "d3e4f55a6b23"  # Mengurai Bangun Datar Menjadi Bagian Kecil
S4 = "e4f5a66b7c34"  # Bermain Puzzle Bentuk Geometri

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Ambil dua kertas segitiga sama.
Tempelkan kedua sisi miringnya rapat.
Lihatlah keajaiban yang terjadi kini.
Dua segitiga berubah menjadi segiempat.
Kita juga bisa menggabung persegi.
Dua persegi menjadi persegi panjang.
Bangun datar bisa saling bersatu.
Gabungan itu membentuk bangun baru.

:::definition
title: Penggabungan Bangun
Dua atau lebih bangun datar dapat disatukan menjadi satu bentuk baru.
:::"""

s2_content = """Mari berkreasi menyusun gambar indah.
Pasang segitiga di atas segiempat.
Bentuk atap dan dinding rumah.
Tambahkan lingkaran di kanan kiri.
Sekarang tampak seperti mobil mini.
Kita juga bisa membuat pohon.
Bisa juga membuat robot seru.
Semua tersusun dari bangun datar.

:::steps
title: Membuat Gambar Rumah
1. Siapkan segiempat untuk dinding rumah.
2. Pasang segitiga di atasnya untuk atap.
3. Tambahkan segiempat kecil untuk pintu.
:::"""

s3_content = """Bangun datar juga bisa diurai.
Ambil selembar kertas segiempat persegi.
Lipat dari pojok ke pojok.
Lalu gunting lipatan lurus itu.
Satu segiempat menjadi dua segitiga.
Kita memotongnya menjadi bagian kecil.
Bentuk besar berasal dari kecil.
Sangat mudah untuk kita coba."""

s4_content = """Pernahkah kamu bermain puzzle tangram?
Tangram punya tujuh keping bentuk.
Ada keping segitiga dan segiempat.
Kita susun keping tanpa bertumpuk.
Keping tersusun menjadi aneka bentuk.

:::common_trap
title: Bagian Asli Tidak Lenyap
Dua segitiga disatukan menjadi segiempat.
Tetapi kedua segitiga tidak hilang lenyap.
Keduanya hanya saling menempel rapat.
Bentuk baru tersusun dari bagiannya.
:::

:::callout
variant: summary
title: Ringkasan
text: Dua segitiga bisa digabung jadi segiempat. Satu segiempat bisa dipotong jadi dua segitiga. Tangram punya 7 keping.
:::"""

sections = [
    {
        "id": S1,
        "title": "Menggabung Dua Bangun Datar",
        "minutes": 6,
        "goal": "Siswa memahami bahwa dua atau lebih bangun datar dapat digabungkan membentuk bangun baru.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Menyusun Gambar Benda Menarik",
        "minutes": 6,
        "goal": "Siswa dapat menyusun berbagai bentuk benda (rumah, mobil, robot) dari kombinasi bangun datar.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mengurai Bangun Datar Menjadi Bagian Kecil",
        "minutes": 6,
        "goal": "Siswa memahami cara mengurai satu bangun datar menjadi bentuk-bentuk yang lebih sederhana.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Bermain Puzzle Bentuk Geometri",
        "minutes": 6,
        "goal": "Siswa dapat bermain dan menyelesaikan puzzle susun keping bentuk geometri (tangram).",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Menyusun Bentuk dari Bangun Datar",
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
# 2. DEFINISI BANK 50 SOAL BAB 30
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
mc("c1", "mudah", D, F, S1, "Dua segitiga sama besar yang ditempelkan sisi miringnya dapat membentuk ....", ["segiempat", "lingkaran", "bola", "titik"], "A", "Dua segitiga siku-siku dapat membentuk satu bangun segiempat.")
tf("c1", "mudah", D, F, S4, "Permainan puzzle tangram tradisional terdiri dari 7 keping bentuk datar.", "Benar", "Tangram terdiri dari 7 keping bangun datar.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Bagian atap pada gambar rumah sederhana biasanya menggunakan bentuk ....", ["segitiga", "lingkaran", "tabung", "bola"], "A", "Atap rumah umumnya digambar dengan bentuk segitiga.")
mc("c1", "mudah", T, F, S3, "Memotong selembar kertas persegi dari pojok ke pojok menghasilkan ....", ["dua segitiga", "dua lingkaran", "dua tabung", "tiga persegi"], "A", "Potongan diagonal persegi menghasilkan 2 buah segitiga.")
sa("c1", "mudah", T, F, S1, "Berapa segitiga yang diperlukan untuk membentuk 1 segiempat persegi?", "2", "Dibutuhkan 2 segitiga sama besar.", verifikasi={"ekspresi": "2", "hasil": "2"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Jika satu segiempat dipotong menjadi dua segitiga, apakah kertasnya bertambah luas?", ["tidak, luas kertas tetap sama", "ya, menjadi jauh lebih luas", "luasnya berkurang separuh", "kertasnya menghilang"], "A", "Kertas hanya terbagi dua tanpa mengubah luas keseluruhan.", "Mengira luas bertambah saat bangun dipotong")
tf("c2", "mudah", D, Kn, S1, "Dua bangun persegi yang digabung berdampingan dapat membentuk persegi panjang.", "Benar", "Dua persegi jejer membentuk satu persegi panjang.")

# Remedial (2)
mc("c2", "mudah", R, F, S2, "Bentuk bangun datar yang paling cocok digunakan untuk menggambar roda mobil adalah ....", ["lingkaran", "segitiga", "segiempat", "persegi"], "A", "Roda berbentuk lingkaran agar bisa berputar.", "Memilih bentuk bersudut untuk roda gambar mobil")
mc("c2", "mudah", R, Kn, S4, "Saat menyusun puzzle keping geometri, keping-keping tersebut harus diletakkan ....", ["rapat berdampingan tanpa bertumpuk", "bertumpuk tiga lapis", "saling menindih miring", "berhamburan jauh"], "A", "Keping puzzle disusun berdampingan tanpa saling menumpuk.", "Menumpuk keping puzzle saat menyusun bentuk")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Ada 3 segitiga dan 4 segiempat kertas. Berapa total keping kertas?", ["7 keping", "6 keping", "8 keping", "5 keping"], "A", "3 + 4 = 7 keping kertas.", verifikasi={"ekspresi": "3 + 4", "hasil": "7"})
mc("c2", "mudah", T, Kn, S2, "Menggambar 1 mobil butuh 1 segiempat dan 2 lingkaran. Berapa bangun datar dipakai?", ["3 bangun", "2 bangun", "4 bangun", "5 bangun"], "A", "1 + 2 = 3 bangun datar.", verifikasi={"ekspresi": "1 + 2", "hasil": "3"})
tf("c2", "mudah", T, Kn, S3, "Sebuah lingkaran dapat dipotong menghasilkan dua buah segitiga lurus.", "Salah", "Potongan lingkaran memiliki tepi melengkung, bukan segitiga lurus.")
sa("c2", "mudah", T, Kn, S4, "Dalam puzzle tangram ada 5 segitiga dan 2 keping segiempat. Total keping?", "7", "5 + 2 = 7 keping.", verifikasi={"ekspresi": "5 + 2", "hasil": "7"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Siti menggabungkan 4 buah persegi kecil yang sama. Bentuk apa yang bisa terbentuk?", ["sebuah persegi besar", "sebuah lingkaran bulat", "sebuah bola ruang", "sebuah kerucut"], "A", "Empat persegi kecil bisa disusun menjadi satu persegi besar.", "Keliru memprediksi hasil gabungan persegi")
mc("c3", "sedang", R, Pr, S3, "Dua lembar kertas segiempat dipotong tengah masing-masing jadi 2 segitiga. Total segitiga?", ["4 segitiga", "3 segitiga", "5 segitiga", "2 segitiga"], "A", "2 x 2 = 4 segitiga.", "Salah menghitung hasil penguraian dua bangun", verifikasi={"ekspresi": "2 * 2", "hasil": "4"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Tersedia 6 segitiga. Jika tiap 2 segitiga jadi 1 segiempat, berapa segiempat terbentuk?", ["3 segiempat", "2 segiempat", "4 segiempat", "5 segiempat"], "A", "6 / 2 = 3 segiempat.", verifikasi={"ekspresi": "6 // 2", "hasil": "3"})
mc("c3", "sedang", T, Pr, S2, "Budi membuat 2 gambar rumah. Satu rumah butuh 3 bangun datar. Total bangun dipakai?", ["6 bangun", "5 bangun", "7 bangun", "4 bangun"], "A", "2 x 3 = 6 bangun datar.", verifikasi={"ekspresi": "2 * 3", "hasil": "6"})
tf("c3", "sedang", T, Pr, S3, "Memotong persegi panjang menjadi dua sama panjang bisa menghasilkan dua persegi.", "Benar", "Persegi panjang yang dipotong tegak di tengah bisa menjadi 2 persegi.")
mc("c3", "sedang", T, Pr, S4, "Tangram punya 7 keping. 3 keping dipakai membuat burung. Berapa keping sisa?", ["4 keping", "3 keping", "5 keping", "2 keping"], "A", "7 - 3 = 4 keping.", verifikasi={"ekspresi": "7 - 3", "hasil": "4"})
tf("c3", "sedang", T, Pr, S1, "Tiga buah segitiga sama sisi tidak bisa disusun berdampingan di kertas.", "Salah", "Tiga segitiga bisa disusun bersisian membentuk trapesium datar.")
sa("c3", "mudah", T, Pr, S3, "Ada 3 kertas persegi. Tiap kertas dipotong jadi 2 segitiga. Berapa segitiga terbentuk?", "6", "3 x 2 = 6 segitiga.", verifikasi={"ekspresi": "3 * 2", "hasil": "6"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Lani punya 8 segitiga kecil. Tiap 2 segitiga dibuat 1 segiempat. Berapa segiempat jadi?", ["4 segiempat", "3 segiempat", "5 segiempat", "2 segiempat"], "A", "8 / 2 = 4 segiempat.", verifikasi={"ekspresi": "8 // 2", "hasil": "4"})
mc("c3", "sedang", X, Pr, S2, "Gambar roket butuh 1 segitiga, 2 segiempat, dan 3 lingkaran. Total bangun?", ["6 bangun", "5 bangun", "7 bangun", "4 bangun"], "A", "1 + 2 + 3 = 6 bangun datar.", verifikasi={"ekspresi": "1 + 2 + 3", "hasil": "6"})
tf("c3", "sedang", X, Pr, S4, "Menyusun keping puzzle tangram boleh saling menumpuk satu di atas lainnya.", "Salah", "Aturan tangram keping harus diletakkan datar tanpa menumpuk.")
sa("c3", "sedang", X, Pr, S4, "Ada 12 keping geometri di meja. 5 keping dipasang pada puzzle. Berapa keping sisa?", "7", "12 - 5 = 7 keping.", verifikasi={"ekspresi": "12 - 5", "hasil": "7"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Edo punya 5 keping persegi. Diberi kakak 4 keping persegi. Berapa keping persegi Edo?", ["9 keping", "8 keping", "10 keping", "7 keping"], "A", "5 + 4 = 9 keping.", verifikasi={"ekspresi": "5 + 4", "hasil": "9"})
mc("c3", "sedang", K, Pr, S2, "Satu robot butuh 4 segiempat dan 4 lingkaran. Berapa total bangun datar untuk 1 robot?", ["8 bangun", "7 bangun", "9 bangun", "6 bangun"], "A", "4 + 4 = 8 bangun datar.", verifikasi={"ekspresi": "4 + 4", "hasil": "8"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Mengapa dua segitiga siku-siku sama besar bisa digabung menjadi satu bangun segiempat?", ["karena sisi miring keduanya bisa ditempelkan lurus saling melengkapi", "karena segitiga punya 4 sisi", "karena warnanya sama", "karena kertasnya basah"], "A", "Sisi miring yang ditempelkan membentuk bangun segiempat utuh.")
mc("c4", "sedang", T, Kn, S2, "Jika ingin menggambar pemandangan pohon rindang, kombinasi bentuk yang paling tepat adalah ....", ["lingkaran untuk daun dan segiempat untuk batang", "segitiga untuk roda mobil", "lingkaran untuk atap rumah", "segiempat untuk bola sepak"], "A", "Batang segiempat memanjang dengan dedaunan lingkaran rimbun.")
tf("c4", "sedang", T, Kn, S3, "Satu bangun datar yang dipotong menjadi dua bagian menghasilkan dua bangun yang utuh.", "Benar", "Tiap potongan membentuk bidang bangun datar baru yang utuh.")
tf("c4", "sedang", T, Kn, S4, "Keping puzzle tangram dapat disusun membentuk gambar kucing atau burung.", "Benar", "Keping tangram sangat fleksibel membentuk aneka pola binatang.")
sa("c4", "sedang", T, Kn, S4, "Ada 15 keping puzzle tangram. 8 keping berwarna biru. Berapa keping warna lain?", "7", "15 - 8 = 7 keping.", verifikasi={"ekspresi": "15 - 8", "hasil": "7"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Empat segitiga kecil disusun rapat menjadi satu segitiga yang lebih besar. Berapa segitiga kecil?", ["4 segitiga", "3 segitiga", "5 segitiga", "2 segitiga"], "A", "Tersusun dari 4 segitiga kecil.", verifikasi={"ekspresi": "4", "hasil": "4"})
mc("c4", "sedang", X, Kn, S2, "Membuat 2 gambar truk butuh 4 lingkaran roda tiap truk. Berapa total roda?", ["8 roda", "6 roda", "10 roda", "7 roda"], "A", "2 x 4 = 8 roda lingkaran.", verifikasi={"ekspresi": "2 * 4", "hasil": "8"})
tf("c4", "sedang", X, Kn, S1, "Dua lingkaran bundar yang ditempelkan bisa membentuk sebuah bangun persegi sempurna.", "Salah", "Tepi lingkaran melengkung sehingga tidak bisa membentuk persegi bersisi lurus.")
mc("c4", "sulit", X, Me, S3, "Ada 5 lembar persegi. Tiap lembar dipotong jadi 2 segitiga. Berapa segitiga yang diperoleh?", ["10 segitiga", "8 segitiga", "12 segitiga", "9 segitiga"], "A", "5 x 2 = 10 segitiga.", verifikasi={"ekspresi": "5 * 2", "hasil": "10"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Jika kamu memiliki 3 persegi yang dijejarkan memanjang, bangun apa yang terbentuk?", ["segiempat persegi panjang", "lingkaran besar", "segitiga lancip", "balok tebal"], "A", "Jejeran persegi membentuk persegi panjang.")
mc("c4", "sulit", K, Me, S2, "Siti membuat kolase: 6 segitiga, 5 segiempat, dan 3 lingkaran. Berapa total keping?", ["14 keping", "13 keping", "15 keping", "12 keping"], "A", "6 + 5 + 3 = 14 keping datar.", verifikasi={"ekspresi": "6 + 5 + 3", "hasil": "14"})
tf("c4", "sulit", K, Me, S3, "Kertas segiempat yang digunting berliku-liku tidak beraturan menghasilkan bangun geometri sederhana.", "Salah", "Guntingan berliku tidak menghasilkan bangun geometri baku.")
mc("c4", "sulit", K, Me, S4, "Tersedia 18 keping tangram. 11 keping terpasang di gambar rumah. Berapa keping sisa?", ["7 keping", "6 keping", "8 keping", "5 keping"], "A", "18 - 11 = 7 keping.", verifikasi={"ekspresi": "18 - 11", "hasil": "7"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Berapa banyak segitiga kecil yang dibutuhkan untuk membuat 4 bangun segiempat persegi?", ["8 segitiga", "6 segitiga", "10 segitiga", "7 segitiga"], "A", "4 x 2 = 8 segitiga kecil.", verifikasi={"ekspresi": "4 * 2", "hasil": "8"})
mc("c5", "sedang", T, Me, S2, "Ada 16 keping bentuk: 7 segitiga, 4 segiempat, sisanya lingkaran. Berapa lingkaran?", ["5 lingkaran", "4 lingkaran", "6 lingkaran", "3 lingkaran"], "A", "16 - 7 - 4 = 5 lingkaran.", verifikasi={"ekspresi": "16 - 7 - 4", "hasil": "5"})
mc("c5", "sedang", T, Me, S3, "Sebuah segiempat dipotong jadi 2 segitiga. Masing-masing dipotong lagi jadi 2. Berapa segitiga akhir?", ["4 segitiga", "3 segitiga", "5 segitiga", "2 segitiga"], "A", "2 x 2 = 4 segitiga.", verifikasi={"ekspresi": "2 * 2", "hasil": "4"})
mc("c5", "sulit", T, Me, S4, "Dua set tangram lengkap masing-masing berisi 7 keping. Berapa total seluruh keping?", ["14 keping", "12 keping", "16 keping", "15 keping"], "A", "2 x 7 = 14 keping.", verifikasi={"ekspresi": "2 * 7", "hasil": "14"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Udin membuat 5 segiempat dari segitiga (tiap segiempat butuh 2 segitiga). Berapa segitiga dipakai?", ["10 segitiga", "8 segitiga", "12 segitiga", "9 segitiga"], "A", "5 x 2 = 10 segitiga.", verifikasi={"ekspresi": "5 * 2", "hasil": "10"})
mc("c5", "sulit", K, Me, S3, "Tersedia 20 keping segitiga. Dibuat segiempat memakai 14 segitiga. Berapa segitiga sisa?", ["6 segitiga", "5 segitiga", "7 segitiga", "4 segitiga"], "A", "20 - 14 = 6 segitiga.", verifikasi={"ekspresi": "20 - 14", "hasil": "6"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Rancanglah sebuah gambar kereta api cepat menggunakan gabungan aneka bangun datar!", ["menyusun gerbong segiempat memanjang, roda lingkaran di bawah, dan segitiga di moncong depan", "menggambar satu lingkaran saja di tengah kertas", "menumpuk batu bata asli di lantai", "meniup gelembung sabun ke udara"], "A", "Kombinasi segiempat gerbong, segitiga moncong, dan roda lingkaran.")
mc("c6", "sulit", K, Me, S4, "Susunlah strategi tercepat dalam menyelesaikan puzzle tangram bergambar hewan!", ["pasang potongan keping terbesar terlebih dahulu lalu lengkapi dengan keping kecil", "acak semua keping tanpa rencana", "tumpuk semua keping di satu sudut", "buang keping yang tidak disukai"], "A", "Memasang keping besar utama memudahkan peletakan keping kecil pelengkap.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Tersedia 18 keping segitiga. Jika tiap segiempat butuh 2 segitiga, berapa segiempat dihasilkan?", ["9 segiempat", "8 segiempat", "10 segiempat", "7 segiempat"], "A", "18 / 2 = 9 segiempat.", verifikasi={"ekspresi": "18 // 2", "hasil": "9"})
mc("c6", "sulit", P, Me, S3, "Ada 6 kertas persegi. Tiap kertas dipotong jadi 2 segitiga. Berapa total segitiga?", ["12 segitiga", "10 segitiga", "14 segitiga", "8 segitiga"], "A", "6 x 2 = 12 segitiga.", verifikasi={"ekspresi": "6 * 2", "hasil": "12"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab30_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab30.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
