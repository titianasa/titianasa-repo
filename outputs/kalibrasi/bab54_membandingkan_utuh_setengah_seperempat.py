#!/usr/bin/env python3
"""
Generator dan validator Bab 54 Matematika Kelas 2 SD:
"Membandingkan Utuh, Setengah, dan Seperempat" (Fase A)
bab_id: 359c8288-1ab7-4462-942c-cd477aa5fe33
article_id: e45f46ef-01e9-445f-819a-983b818eca66
quiz_id: c38db8e4-ad81-483b-99c3-49f9472af672
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "b1c2d3e4f501"  # Urutan Ukuran: Utuh, Setengah, dan Seperempat
S2 = "c2d3e4f5a602"  # Hubungan Antara Setengah dan Seperempat
S3 = "d3e4f5a6b703"  # Membandingkan Nilai Kumpulan Benda
S4 = "e4f5a6b7c804"  # Memecahkan Soal Cerita Perbandingan Pecahan

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Mari kita sejajarkan tiga potong kue.
Kue pertama masih utuh sempurna.
Kue kedua adalah potongan setengah.
Kue ketiga adalah potongan seperempat.
Potongan utuh tentu paling besar.
Potongan setengah berada di tengah.
Potongan seperempat berukuran paling kecil.
Urutan dari terbesar: utuh, setengah, seperempat!

:::definition
title: Urutan Ukuran Pecahan
Satu bagian utuh lebih besar dari setengah ($1/2$).
Setengah ($1/2$) lebih besar dari seperempat ($1/4$).
:::"""

s2_content = """Lihatlah hubungan kedua pecahan ini.
Ambil dua potong kue seperempat.
Satukan kedua potongan tersebut.
Ternyata ukurannya pas satu setengah!
Dua seperempat sama dengan setengah.
Empat seperempat sama dengan utuh.
Dua setengah juga sama dengan utuh.
Semuanya saling berhubungan erat!

:::steps
title: Hubungan Kesetaraan Pecahan
1. Dua bagian seperempat ($1/4 + 1/4$) senilai dengan satu bagian setengah ($1/2$).
2. Dua bagian setengah ($1/2 + 1/2$) senilai dengan satu benda utuh ($1$).
3. Empat bagian seperempat senilai dengan satu benda utuh ($1$).
:::"""

s3_content = """Bagaimana dengan kumpulan benda?
Misalkan ada dua puluh buah jeruk.
Jumlah utuh adalah dua puluh jeruk.
Setengahnya adalah sepuluh jeruk.
Seperempatnya adalah lima jeruk.
Dua puluh lebih banyak dari sepuluh.
Sepuluh lebih banyak dari lima.
Hitungan kita cocok dengan ukuran pecahan!"""

s4_content = """Dalam soal cerita, cermatilah pecahannya.
Budi memakan setengah bagian pizza.
Siti memakan seperempat bagian pizza.
Siapa yang makan lebih banyak?
Budi makan lebih banyak dari Siti!
Karena setengah lebih besar dari seperempat.
Selalu bayangkan ukuran potongannya.

:::common_trap
title: Terkecoh Angka Penyebut
Angka 4 lebih besar dari 2.
Namun potongan $1/4$ lebih kecil dari $1/2$!
Membagi ke 4 orang menghasilkan bagian lebih kecil daripada membagi ke 2 orang.
:::

:::callout
variant: summary
title: Ringkasan
text: Benda utuh > setengah > seperempat. Dua potong seperempat sama besar dengan satu potong setengah.
:::"""

sections = [
    {
        "id": S1,
        "title": "Urutan Ukuran: Utuh, Setengah, dan Seperempat",
        "minutes": 6,
        "goal": "Siswa mampu mengurutkan ukuran pecahan konkret dari yang terbesar maupun terkecil.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Hubungan Antara Setengah dan Seperempat",
        "minutes": 6,
        "goal": "Siswa memahami kesetaraan bahwa dua bagian seperempat bernilai sama dengan satu bagian setengah.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membandingkan Nilai Kumpulan Benda",
        "minutes": 6,
        "goal": "Siswa mampu membandingkan kuantitas objek pada benda utuh, setengah bagian, dan seperempat bagian.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Memecahkan Soal Cerita Perbandingan Pecahan",
        "minutes": 6,
        "goal": "Siswa mampu menyelesaikan permasalahan kontekstual perbandingan pecahan dalam kehidupan sehari-hari.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membandingkan Utuh, Setengah, dan Seperempat",
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
# 2. DEFINISI BANK 50 SOAL BAB 54
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
mc("c1", "mudah", D, F, S1, "Di antara pilihan berikut, manakah potongan yang PALING BESAR ukurannya?", ["satu benda utuh", "setengah bagian", "seperempat bagian", "tidak tentu"], "A", "Benda utuh selalu paling besar dibanding pecahannya.")
tf("c1", "mudah", D, F, S2, "Dua potong kue seperempat sama besarnya dengan satu potong setengah.", "Benar", "1/4 + 1/4 = 1/2.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Urutan pecahan dari yang TERKECIL ke terbesar adalah ....", ["seperempat, setengah, utuh", "utuh, setengah, seperempat", "setengah, seperempat, utuh", "utuh, seperempat, setengah"], "A", "Urutan dari paling kecil: 1/4, lalu 1/2, lalu 1 utuh.")
mc("c1", "mudah", T, F, S3, "Dari 8 apel, berapakah banyak apel untuk bagian setengah?", ["4 apel", "2 apel", "6 apel", "8 apel"], "A", "8 : 2 = 4 apel.", verifikasi={"ekspresi": "8 / 2", "hasil": "4"})
sa("c1", "mudah", T, F, S3, "Dari 8 apel, berapakah banyak apel untuk bagian seperempat?", "2", "8 : 4 = 2 apel.", verifikasi={"ekspresi": "8 / 4", "hasil": "2"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Budi makan $1/2$ roti. Siti makan $1/4$ roti sama ukuran. Siapa makan lebih banyak?", ["Budi makan lebih banyak", "Siti makan lebih banyak", "keduanya sama banyak", "tidak dapat dihitung"], "A", "1/2 lebih besar dari 1/4, jadi Budi makan lebih banyak.")
tf("c2", "mudah", D, Kn, S1, "Pecahan $1/4$ ukurannya lebih besar daripada pecahan $1/2$.", "Salah", "1/4 lebih kecil daripada 1/2.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Mengapa potongan setengah lebih besar daripada potongan seperempat?", ["karena dibagi ke lebih sedikit anak", "karena angka 2 lebih besar dari 4", "karena rotinya beda rasa", "karena warnanya lebih cerah"], "A", "Makin sedikit bagian pembagiannya, makin besar ukurannya.", "Terkecoh angka penyebut lebih besar")
mc("c2", "mudah", R, Kn, S2, "Berapa potongan seperempat yang dibutuhkan untuk menyamai satu kue utuh?", ["4 potong", "2 potong", "3 potong", "1 potong"], "A", "4 potong seperempat menyamai satu benda utuh.", "Salah menyetarakan pecahan utuh", verifikasi={"ekspresi": "4 / 1", "hasil": "4"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S2, "Berapa banyak potongan seperempat agar sama besarnya dengan setengah kue?", ["2 potong", "1 potong", "3 potong", "4 potong"], "A", "Dua potong 1/4 senilai dengan 1/2.", verifikasi={"ekspresi": "2 / 1", "hasil": "2"})
mc("c2", "mudah", T, Kn, S3, "Dari 12 kue, berapa selisih jumlah setengah kue dengan seperempat kue?", ["3 kue", "2 kue", "4 kue", "1 kue"], "A", "Setengah = 6; Seperempat = 3; Selisih = 6 - 3 = 3 kue.", verifikasi={"ekspresi": "(12 / 2) - (12 / 4)", "hasil": "3"})
tf("c2", "mudah", T, Kn, S4, "Anak yang mendapat setengah kue mendapat bagian lebih banyak dari anak yang mendapat seperempat.", "Benar", "1/2 lebih besar dari 1/4.")
sa("c2", "mudah", T, Kn, S3, "Dari 16 permen, berapakah banyak permen setengah bagian?", "8", "16 : 2 = 8 permen.", verifikasi={"ekspresi": "16 / 2", "hasil": "8"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Dari 20 kelereng, berapa kelereng untuk seperempat bagian?", ["5 kelereng", "10 kelereng", "4 kelereng", "6 kelereng"], "A", "20 : 4 = 5 kelereng.", "Keliru menghitung seperempat kumpulan", verifikasi={"ekspresi": "20 / 4", "hasil": "5"})
mc("c3", "sedang", R, Pr, S4, "Ada semangka dibagi. Doni dapat $1/2$, Ali dapat $1/4$. Siapa dapat lebih sedikit?", ["Ali dapat lebih sedikit", "Doni dapat lebih sedikit", "sama banyak", "tidak tahu"], "A", "1/4 lebih kecil dari 1/2, jadi Ali dapat lebih sedikit.", "Tertukar perbandingan lebih sedikit")

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Manakah tanda perbandingan yang BENAR antara $1/2$ dan $1/4$?", ["$1/2 > 1/4$", "$1/2 < 1/4$", "$1/2 = 1/4$", "$1/4 > 1/2$"], "A", "1/2 lebih besar (>) dari 1/4.")
mc("c3", "mudah", T, Pr, S3, "Berapakah jumlah dari setengah 24 ditambah seperempat 24?", ["18", "16", "20", "14"], "A", "(24 : 2) + (24 : 4) = 12 + 6 = 18.", verifikasi={"ekspresi": "(24 / 2) + (24 / 4)", "hasil": "18"})
tf("c3", "sedang", T, Pr, S2, "Tiga potong seperempat nilainya lebih kecil daripada satu potong setengah.", "Salah", "Tiga seperempat (3/4) lebih besar dari setengah (2/4).")
mc("c3", "sedang", T, Pr, S4, "Ibu punya 1 pizza. Setengah untuk ayah, seperempat untuk adik. Sisa bagian?", ["seperempat bagian", "setengah bagian", "satu utuh", "habis"], "A", "1 - 1/2 - 1/4 = 1/4 bagian tersisa.")
tf("c3", "sedang", T, Pr, S3, "Setengah dari 24 sama banyaknya dengan dua kali seperempat dari 24.", "Benar", "Setengah = 12; Dua kali seperempat = 2 x 6 = 12.")
sa("c3", "sedang", T, Pr, S3, "Berapakah selisih antara setengah dari 28 dengan seperempat dari 28?", "7", "(28 : 2) - (28 : 4) = 14 - 7 = 7.", verifikasi={"ekspresi": "(28 / 2) - (28 / 4)", "hasil": "7"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Lina membawa $1/4$ kue. Rani membawa $1/2$ kue. Siapa kue yang lebih kecil?", ["kue Lina lebih kecil", "kue Rani lebih kecil", "sama besar", "tidak ada"], "A", "1/4 lebih kecil dari 1/2, jadi kue Lina lebih kecil.")
mc("c3", "sedang", X, Pr, S2, "Jika kamu menggabungkan 1 potong setengah dan 2 potong seperempat, hasilnya adalah ....", ["satu benda utuh", "dua benda utuh", "setengah benda", "tiga per empat"], "A", "1/2 + 1/4 + 1/4 = 1/2 + 1/2 = 1 benda utuh.")
tf("c3", "sedang", X, Pr, S4, "Memakan satu pizza utuh lebih kenyang daripada memakan setengah pizza.", "Benar", "Satu utuh bernilai dua kali lipat dari setengah.")
sa("c3", "sedang", X, Pr, S3, "Dari 32 buku, berapakah jumlah setengah bagian ditambah 4 buku?", "20", "(32 : 2) + 4 = 16 + 4 = 20.", verifikasi={"ekspresi": "(32 / 2) + 4", "hasil": "20"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Toko punya 36 pensil. Setengah pensil merah, seperempat biru. Berapa pensil merah?", ["18 pensil", "9 pensil", "12 pensil", "24 pensil"], "A", "36 : 2 = 18 pensil merah.", verifikasi={"ekspresi": "36 / 2", "hasil": "18"})
mc("c3", "sedang", K, Pr, S4, "Dari 36 pensil toko tadi, berapakah jumlah pensil biru?", ["9 pensil", "18 pensil", "12 pensil", "6 pensil"], "A", "36 : 4 = 9 pensil biru.", verifikasi={"ekspresi": "36 / 4", "hasil": "9"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa tanda perbandingan $1/2 > 1/4$ bernilai benar?", ["karena membagi 2 menghasilkan potongan lebih besar dari membagi 4", "karena 2 lebih besar dari 4", "karena warnanya beda", "karena garisnya lebih panjang"], "A", "Membagi dua menghasilkan potongan yang luasnya dua kali lebih besar dari membagi empat.")
mc("c4", "sedang", T, Kn, S2, "Manakah dari kesetaraan berikut yang BERNILAI BENAR?", ["$1/2 = 1/4 + 1/4$", "$1/4 = 1/2 + 1/2$", "$1 = 1/4 + 1/4$", "$1/2 = 1/4$"], "A", "1/2 setara dengan 1/4 + 1/4.")
tf("c4", "sedang", T, Kn, S3, "Seperempat dari 40 butir telur sama dengan 20 butir telur.", "Salah", "Seperempat dari 40 adalah 40 : 4 = 10 butir telur, bukan 20.")
tf("c4", "sedang", T, Kn, S4, "Edo makan 2 potong seperempat, artinya Edo makan lebih sedikit dari pemakan 1 potong setengah.", "Salah", "2 potong 1/4 sama besar dengan 1 potong 1/2.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari (setengah dari 40) - (seperempat dari 40)?", "10", "(40 : 2) - (40 : 4) = 20 - 10 = 10.", verifikasi={"ekspresi": "(40 / 2) - (40 / 4)", "hasil": "10"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Urutkan dari yang PALING BESAR: seperempat, benda utuh, setengah!", ["benda utuh, setengah, seperempat", "seperempat, setengah, benda utuh", "setengah, seperempat, benda utuh", "benda utuh, seperempat, setengah"], "A", "Urutan terbesar ke terkecil: utuh, setengah, seperempat.")
mc("c4", "sedang", X, Kn, S3, "Sebuah kolam ada 48 ikan. Setengahnya nila, seperempatnya gurame. Berapa ikan nila?", ["24 ikan", "12 ikan", "18 ikan", "30 ikan"], "A", "48 : 2 = 24 ikan nila.", verifikasi={"ekspresi": "48 / 2", "hasil": "24"})
tf("c4", "sedang", X, Kn, S2, "Empat potong kue setengah nilainya sama dengan satu kue utuh.", "Salah", "Empat potong setengah sama dengan 2 kue utuh, bukan 1.")
mc("c4", "sulit", X, Me, S4, "Doni punya 1 m, Siti setengah meter, Ani seperempat. Siapa terpendek?", ["Ani", "Siti", "Doni", "sama semua"], "A", "1/4 meter adalah yang paling pendek.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Berapa kali lipat ukuran potongan setengah dibanding potongan seperempat?", ["2 kali lipat", "3 kali lipat", "4 kali lipat", "sama besar"], "A", "Potongan setengah tepat 2 kali lebih besar dari potongan seperempat.", verifikasi={"ekspresi": "4 / 2", "hasil": "2"})
mc("c4", "sulit", K, Me, S2, "Ada 3 potong kue seperempat. Berapa potong seperempat lagi agar menjadi 1 kue utuh?", ["1 potong", "2 potong", "3 potong", "4 potong"], "A", "1 kue utuh = 4 potong seperempat. 4 - 3 = 1 potong lagi.", verifikasi={"ekspresi": "4 - 3", "hasil": "1"})
tf("c4", "sulit", K, Me, S4, "Satu kue utuh dikurangi satu potong setengah menghasilkan satu potong setengah.", "Benar", "1 - 1/2 = 1/2.")
mc("c4", "sulit", K, Me, S3, "Berapakah hasil dari (setengah dari 44) + (seperempat dari 44)?", ["33", "30", "36", "28"], "A", "(44 : 2) + (44 : 4) = 22 + 11 = 33.", verifikasi={"ekspresi": "(44 / 2) + (44 / 4)", "hasil": "33"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Jika seperempat tabungan Budi adalah 12 rupiah, berapakah setengah tabungan Budi?", ["24 rupiah", "20 rupiah", "30 rupiah", "18 rupiah"], "A", "Tabungan utuh = 12 x 4 = 48; Setengah tabungan = 48 : 2 = 24 rupiah.", verifikasi={"ekspresi": "(12 * 4) / 2", "hasil": "24"})
mc("c5", "sedang", T, Me, S2, "Jika setengah tali adalah 16 cm, berapakah panjang seperempat tali tersebut?", ["8 cm", "6 cm", "10 cm", "12 cm"], "A", "Tali utuh = 16 x 2 = 32 cm; Seperempat tali = 32 : 4 = 8 cm.", verifikasi={"ekspresi": "(16 * 2) / 4", "hasil": "8"})
mc("c5", "sedang", T, Me, S3, "Ada 56 jeruk. Setengah dibagikan ke tetangga. Seperempat sisanya dimakan. Berapa dimakan?", ["7 jeruk", "6 jeruk", "8 jeruk", "5 jeruk"], "A", "Sisa = 56 : 2 = 28 jeruk; Seperempat dari sisa = 28 : 4 = 7 jeruk.", verifikasi={"ekspresi": "(56 / 2) / 4", "hasil": "7"})
mc("c5", "sulit", T, Me, S4, "Berapakah selisih dari setengah 64 dengan seperempat 64?", ["16", "14", "18", "12"], "A", "(64 : 2) - (64 : 4) = 32 - 16 = 16.", verifikasi={"ekspresi": "(64 / 2) - (64 / 4)", "hasil": "16"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Sebuah bilangan jika diambil setengahnya bernilai 20. Berapakah seperempatnya?", ["10", "8", "12", "15"], "A", "Bilangan utuh = 20 x 2 = 40; Seperempatnya = 40 : 4 = 10.", verifikasi={"ekspresi": "(20 * 2) / 4", "hasil": "10"})
mc("c5", "sulit", K, Me, S4, "Berapakah hasil dari (setengah dari 80) - (seperempat dari 80)?", ["20", "15", "25", "30"], "A", "(80 : 2) - (80 : 4) = 40 - 20 = 20.", verifikasi={"ekspresi": "(80 / 2) - (80 / 4)", "hasil": "20"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Bagaimana cara membuktikan secara konkret bahwa $1/2$ bernilai sama dengan $1/4 + 1/4$?", ["tumpuk dua potong seperempat di atas satu potong setengah, ukurannya pas persis", "tuliskan rumus di kertas", "tanya teman sekelas", "tidak perlu dibuktikan"], "A", "Menumpuk dua potong seperempat di atas setengah membuktikan kesetaraan luasnya secara konkret.")
mc("c6", "sulit", K, Me, S4, "Pita 100 cm dipotong setengahnya. Lalu potongan itu dipotong lagi seperempatnya. Berapa cm potongannya?", ["12.5 cm", "15 cm", "10 cm", "20 cm"], "A", "Setengah = 100 : 2 = 50 cm. Potongan berikutnya adalah pita utuh 100 dipotong seperempat = 25 cm.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi: (setengah dari 96) - (seperempat dari 96) + 10!", ["34", "32", "36", "30"], "A", "(96 : 2) - (96 : 4) + 10 = 48 - 24 + 10 = 34.", verifikasi={"ekspresi": "(96 / 2) - (96 / 4) + 10", "hasil": "34"})
mc("c6", "sulit", P, Me, S3, "Pak Lurah panen 72 semangka. Setengah untuk A, seperempat untuk B. Sisa semangka?", ["18 semangka", "16 semangka", "20 semangka", "14 semangka"], "A", "Warga A = 72 : 2 = 36; Warga B = 72 : 4 = 18; Total dibagikan = 54; Sisa = 72 - 54 = 18 semangka.", verifikasi={"ekspresi": "72 - ((72 / 2) + (72 / 4))", "hasil": "18"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab54_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab54.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
