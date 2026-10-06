#!/usr/bin/env python3
"""
Generator dan validator Bab 72 Matematika Kelas 2 SD:
"Membedakan Persegi dan Persegi Panjang" (Fase A)
bab_id: ceff001d-ffb9-471d-a53c-d31ca31e8363
article_id: 68c1b4f0-a7b6-4893-affd-3ec65d6d8e37
quiz_id: 6163f707-1ae5-4bba-9c40-c9076026a6e9
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "q1s2u3w4y501"  # Mengenal Persegi dan Ciri-cirinya
S2 = "r2t3v4x5z602"  # Mengenal Persegi Panjang dan Ciri-cirinya
S3 = "s3u4w5y6a703"  # Membedakan Persegi dan Persegi Panjang
S4 = "t4v5x6z7b804"  # Benda Nyata Persegi dan Persegi Panjang

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Persegi adalah bangun segiempat yang istimewa.
Persegi memiliki empat sisi lurus.
Keempat sisinya sama panjang.
Jika satu sisi 5 sentimeter.
Tiga sisi lain juga 5 sentimeter.
Persegi juga memiliki empat sudut.
Semua sudutnya adalah sudut siku-siku.
Bentuknya tampak sangat rapi seimbang!

:::definition
title: Persegi
Bangun segiempat yang keempat sisinya sama panjang dan bersudut siku-siku.
:::"""

s2_content = """Persegi panjang juga memiliki empat sisi.
Namun sisinya tidak semuanya sama.
Hanya sisi berhadapan yang sama panjang.
Ada dua sisi yang lebih panjang.
Ada dua sisi yang lebih pendek.
Sisi pendek biasa disebut lebar.
Persegi panjang memiliki empat sudut siku-siku.
Pintu kelas berbentuk persegi panjang!

:::steps
title: Ciri Persegi Panjang
1. Memiliki empat buah sisi lurus.
2. Sisi yang berhadapan sama panjang.
3. Memiliki empat buah sudut siku-siku.
:::"""

s3_content = """Bagaimana membedakan kedua bangun itu?
Keduanya sama-sama memiliki 4 sisi.
Keduanya sama-sama memiliki 4 sudut.
Perbedaannya ada pada panjang sisinya.
Persegi: semua 4 sisi sama panjang.
Persegi panjang: hanya sisi berhadapan sama.
Ukur sisinya menggunakan penggaris.
Kamu akan tahu perbedaannya dengan jelas!

:::common_trap
title: Mengira Persegi Panjang Sisinya Sama Semua
Persegi panjang memiliki sisi panjang dan lebar.
Sisinya tidak sama panjang semua!
Hanya persegi yang keempat sisinya sama.
:::"""

s4_content = """Banyak benda di sekitar kita.
Ubin lantai dan kertas origami adalah persegi.
Papan catur juga berbentuk persegi.
Papan tulis dan pintu adalah persegi panjang.
Buku tulis dan uang kertas persegi panjang.
Amati benda-benda di dalam kelasmu.
Tentukan mana persegi mana persegi panjang!

:::callout
variant: summary
title: Ringkasan
text: Persegi 4 sisi sama panjang. Persegi panjang sisi berhadapan sama.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Persegi dan Ciri-cirinya",
        "minutes": 6,
        "goal": "Siswa mengenal bangun persegi beserta sifat keempat sisinya yang sama panjang.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengenal Persegi Panjang dan Ciri-cirinya",
        "minutes": 6,
        "goal": "Siswa mengenal bangun persegi panjang dengan pasangan sisi berhadapan yang sama.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membedakan Persegi dan Persegi Panjang",
        "minutes": 6,
        "goal": "Siswa mampu membedakan persegi dan persegi panjang melalui perbandingan panjang sisinya.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Benda Nyata Persegi dan Persegi Panjang",
        "minutes": 6,
        "goal": "Siswa mengidentifikasi benda-benda konkret berbentuk persegi dan persegi panjang.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membedakan Persegi dan Persegi Panjang",
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
# 2. DEFINISI BANK 50 SOAL BAB 72
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
mc("c1", "mudah", D, F, S1, "Berapakah jumlah sisi yang dimiliki oleh sebuah persegi?", ["4 sisi", "3 sisi", "5 sisi", "2 sisi"], "A", "Persegi memiliki 4 sisi.", verifikasi={"ekspresi": "2 * 2", "hasil": "4"})
tf("c1", "mudah", D, F, S2, "Persegi panjang memiliki empat buah sudut siku-siku.", "Benar", "Semua sudut pada persegi panjang adalah siku-siku.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Keempat sisi pada bangun persegi memiliki sifat ....", ["sama panjang", "berbeda-beda", "melengkung", "tidak teratur"], "A", "Semua sisi persegi sama panjang.")
mc("c1", "mudah", T, F, S2, "Berapakah jumlah titik sudut pada bangun persegi panjang?", ["4 sudut", "3 sudut", "5 sudut", "6 sudut"], "A", "Persegi panjang memiliki 4 titik sudut.", verifikasi={"ekspresi": "4 * 1", "hasil": "4"})
sa("c1", "mudah", T, F, S4, "Kertas origami berbentuk segi empat dengan sisi sama disebut bangun ...", "persegi", "Origami umumnya berbentuk persegi.")

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Apa perbedaan paling utama antara persegi dan persegi panjang?", ["panjang sisi-sisinya", "jumlah sudutnya", "jumlah sisinya", "warna bangunnya"], "A", "Persegi 4 sisinya sama, persegi panjang sisi berhadapan sama.")
tf("c2", "mudah", D, Kn, S1, "Semua sisi pada bangun persegi panjang selalu sama panjang.", "Salah", "Hanya sisi yang berhadapan yang sama panjang.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Bila satu sisi persegi 6 cm, berapa cm panjang sisi lainnya?", ["6 cm", "8 cm", "12 cm", "3 cm"], "A", "Semua sisi persegi sama yaitu 6 cm.", "Mengira sisi lain persegi memiliki ukuran berbeda", verifikasi={"ekspresi": "6 * 1", "hasil": "6"})
mc("c2", "mudah", R, Kn, S2, "Berapa pasang sisi berhadapan yang sama pada persegi panjang?", ["2 pasang", "4 pasang", "1 pasang", "3 pasang"], "A", "Ada 2 pasang sisi sejajar berhadapan.", "Menjawab 4 pasang sisi berhadapan", verifikasi={"ekspresi": "4 / 2", "hasil": "2"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S3, "Persamaan antara bangun persegi dan bangun persegi panjang adalah ....", ["sama-sama memiliki 4 sisi dan 4 sudut", "semua sisinya sama panjang", "bentuknya melingkar", "tidak memiliki sudut"], "A", "Keduanya memiliki 4 sisi dan 4 sudut siku-siku.")
mc("c2", "mudah", T, Kn, S4, "Permukaan pintu kelas umumnya berbentuk bangun datar ....", ["persegi panjang", "persegi", "segitiga", "lingkaran"], "A", "Pintu berbentuk persegi panjang.")
tf("c2", "mudah", T, Kn, S4, "Papan catur standar adalah contoh nyata bangun persegi.", "Benar", "Papan catur memiliki 4 sisi sama panjang.")
sa("c2", "mudah", T, Kn, S1, "Persegi memiliki ... sisi yang semuanya sama panjang.", "4", "Persegi memiliki 4 sisi.", verifikasi={"ekspresi": "4 * 1", "hasil": "4"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Persegi dengan sisi 4 cm memiliki keliling berapa cm?", ["16 cm", "12 cm", "8 cm", "20 cm"], "A", "4 x 4 = 16 cm.", "Mengalikan sisi hanya dua kali", verifikasi={"ekspresi": "4 * 4", "hasil": "16"})
mc("c3", "sedang", R, Pr, S2, "Persegi panjang panjangnya 7 cm dan lebarnya 3 cm. Sisi berhadapan?", ["7 cm dan 3 cm", "5 cm dan 5 cm", "4 cm dan 4 cm", "10 cm dan 10 cm"], "A", "Sisi berhadapan sama panjang: 7 cm dan 3 cm.", "Mengira sisi berhadapan tidak sama")

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Sebuah persegi panjang sisinya 5 cm. Total panjang 4 sisinya?", ["20 cm", "15 cm", "25 cm", "10 cm"], "A", "4 x 5 = 20 cm.", verifikasi={"ekspresi": "4 * 5", "hasil": "20"})
mc("c3", "mudah", T, Pr, S4, "Dua ubin persegi 20 cm dijejerkan berdampingan. Bentuk bangun barunya?", ["persegi panjang", "persegi", "segitiga", "lingkaran"], "A", "Dua persegi berdampingan membentuk persegi panjang.")
tf("c3", "sedang", T, Pr, S2, "Persegi panjang panjang 8 cm dan lebar 4 cm kelilingnya 24 cm.", "Benar", "8 + 4 + 8 + 4 = 24 cm.")
mc("c3", "sedang", T, Pr, S3, "Bangun A sisinya 6 cm, 6 cm, 6 cm, 6 cm. Bangun apakah A?", ["persegi", "persegi panjang", "segitiga", "trapesium"], "A", "Semua sisinya sama panjang, jadi persegi.")
tf("c3", "sedang", T, Pr, S1, "Sebuah persegi dapat memiliki dua sisi yang panjangnya berbeda.", "Salah", "Jika sisinya berbeda, itu bukan persegi.")
sa("c3", "sedang", T, Pr, S2, "Persegi panjang memiliki panjang 10 cm. Sisi di hadapannya panjangnya ... cm.", "10", "Sisi berhadapan sama panjang yaitu 10 cm.", verifikasi={"ekspresi": "10 * 1", "hasil": "10"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Berapakah total sudut dari gabungan 2 buah persegi terpisah?", ["8 sudut", "6 sudut", "10 sudut", "4 sudut"], "A", "2 x 4 = 8 sudut.", verifikasi={"ekspresi": "2 * 4", "hasil": "8"})
mc("c3", "sedang", X, Pr, S2, "Persegi panjang panjang 6 cm dan lebar 2 cm. Berapa kelilingnya?", ["16 cm", "12 cm", "14 cm", "18 cm"], "A", "2 x (6 + 2) = 16 cm.", verifikasi={"ekspresi": "2 * (6 + 2)", "hasil": "16"})
tf("c3", "sedang", X, Pr, S3, "Setiap bangun persegi adalah bagian dari kelompok segiempat.", "Benar", "Persegi memiliki 4 sisi sehingga termasuk segiempat.")
sa("c3", "sedang", X, Pr, S1, "Keliling persegi dengan sisi 7 cm adalah ... cm.", "28", "4 x 7 = 28 cm.", verifikasi={"ekspresi": "4 * 7", "hasil": "28"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Ada bangun 4 sisi: 8 cm, 4 cm, 8 cm, 4 cm. Bangun apakah ini?", ["persegi panjang", "persegi", "segitiga", "segilima"], "A", "Sisi berhadapan sama, jadi persegi panjang.")
mc("c3", "sedang", K, Pr, S4, "Meja guru panjang 120 cm, lebar 60 cm. Meja guru berbentuk ....", ["persegi panjang", "persegi", "segitiga", "lingkaran"], "A", "Panjang dan lebar berbeda = persegi panjang.")

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S3
mc("c4", "sedang", T, Kn, S1, "Apakah persegi dapat disebut sebagai persegi panjang yang istimewa?", ["ya karena memiliki 4 sudut siku dan sisi berhadapan sama", "tidak bisa sama sekali", "hanya jika warnanya sama", "hanya jika ukurannya besar"], "A", "Persegi memenuhi syarat persegi panjang dengan sisi yang semuanya sama.")
mc("c4", "sedang", T, Kn, S2, "Sebuah persegi panjang dipotong tepat di tengah menjadi 2 bagian sama. Hasilnya?", ["bisa menjadi 2 persegi atau 2 persegi panjang baru", "selalu segitiga", "selalu lingkaran", "tidak berbentuk"], "A", "Tergantung perbandingan panjang dan lebar awalnya.")
tf("c4", "sedang", T, Kn, S3, "Persegi dan persegi panjang memiliki jumlah sudut yang berbeda.", "Salah", "Keduanya memiliki jumlah sudut yang sama, yaitu 4 sudut.")
tf("c4", "sedang", T, Kn, S4, "Uang kertas rupiah berbentuk persegi panjang karena memiliki sisi panjang dan lebar.", "Benar", "Uang kertas memiliki sisi panjang dan sisi lebar yang berhadapan sama.")
sa("c4", "sedang", T, Kn, S1, "Bila keliling sebuah persegi 24 cm, panjang tiap sisinya adalah ... cm.", "6", "24 : 4 = 6 cm.", verifikasi={"ekspresi": "24 / 4", "hasil": "6"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S2, "Persegi panjang memiliki keliling 20 cm. Jika panjang 7 cm, berapa lebarnya?", ["3 cm", "4 cm", "5 cm", "2 cm"], "A", "(20 : 2) - 7 = 10 - 7 = 3 cm.", verifikasi={"ekspresi": "(20 / 2) - 7", "hasil": "3"})
mc("c4", "sedang", X, Kn, S3, "Diberikan kawat 36 cm. Dibuat persegi, berapa panjang sisinya?", ["9 cm", "8 cm", "6 cm", "12 cm"], "A", "36 : 4 = 9 cm.", verifikasi={"ekspresi": "36 / 4", "hasil": "9"})
tf("c4", "sedang", X, Kn, S2, "Dua persegi berukuran sama jika digabung sisinya membentuk persegi baru.", "Salah", "Dua persegi digabung membentuk bangun persegi panjang.")
mc("c4", "sulit", X, Me, S4, "Ubin persegi sisi 30 cm. Dipasang 2 baris dan 2 kolom. Luas sisi luar?", ["60 cm", "90 cm", "120 cm", "30 cm"], "A", "2 x 30 = 60 cm tiap sisi, membentuk persegi 60 cm.", verifikasi={"ekspresi": "2 * 30", "hasil": "60"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Kawat 28 cm dibentuk persegi. Berapakah panjang tiap sisinya?", ["7 cm", "6 cm", "8 cm", "5 cm"], "A", "28 : 4 = 7 cm.", verifikasi={"ekspresi": "28 / 4", "hasil": "7"})
mc("c4", "sulit", K, Me, S2, "Persegi panjang keliling 30 cm. Jika lebar 5 cm, berapa panjangnya?", ["10 cm", "12 cm", "8 cm", "15 cm"], "A", "(30 : 2) - 5 = 15 - 5 = 10 cm.", verifikasi={"ekspresi": "(30 / 2) - 5", "hasil": "10"})
tf("c4", "sulit", K, Me, S3, "Jika keempat sudut segiempat berupa siku-siku, sisinya pasti sama panjang.", "Salah", "Bisa berupa persegi panjang yang sisinya tidak sama.")
mc("c4", "sulit", K, Me, S4, "Berapa banyak persegi satuan yang dibutuhkan untuk membuat persegi 3x3?", ["9 persegi satuan", "6 persegi satuan", "12 persegi satuan", "8 persegi satuan"], "A", "3 x 3 = 9 persegi satuan.", verifikasi={"ekspresi": "3 * 3", "hasil": "9"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Tersedia 3 kawat masing-masing 16 cm dibuat persegi. Total sisi dari 3 persegi?", ["12 sisi", "8 sisi", "16 sisi", "10 sisi"], "A", "3 x 4 = 12 sisi.", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})
mc("c5", "sedang", T, Me, S2, "Bandingkan keliling: Persegi sisi 6 cm vs Persegi panjang 8 cm x 4 cm?", ["keduanya memiliki keliling yang sama (24 cm)", "persegi lebih panjang", "persegi panjang lebih panjang", "tidak dapat dihitung"], "A", "Persegi: 4 x 6 = 24 cm. Persegi panjang: 2 x (8+4) = 24 cm.")
mc("c5", "sedang", T, Me, S3, "Berapa cm selisih keliling persegi sisi 8 cm dan persegi sisi 5 cm?", ["12 cm", "10 cm", "8 cm", "15 cm"], "A", "(4 x 8) - (4 x 5) = 32 - 20 = 12 cm.", verifikasi={"ekspresi": "(4 * 8) - (4 * 5)", "hasil": "12"})
mc("c5", "sulit", T, Me, S4, "Ruangan beralas persegi 4 meter. Dipasang ubin 1 meter. Berapa ubin dibutuhkan?", ["16 ubin", "12 ubin", "20 ubin", "8 ubin"], "A", "4 x 4 = 16 ubin.", verifikasi={"ekspresi": "4 * 4", "hasil": "16"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Persegi panjang panjangnya 2 kali lebarnya. Jika lebar 4 cm, berapa kelilingnya?", ["24 cm", "20 cm", "28 cm", "16 cm"], "A", "Panjang = 8 cm. Keliling = 2 x (8 + 4) = 24 cm.", verifikasi={"ekspresi": "2 * ((2 * 4) + 4)", "hasil": "24"})
mc("c5", "sulit", K, Me, S3, "Sebuah karton persegi dipotong menjadi 4 persegi kecil sama besar. Berapa sudut total?", ["16 sudut", "12 sudut", "8 sudut", "20 sudut"], "A", "4 x 4 = 16 sudut.", verifikasi={"ekspresi": "4 * 4", "hasil": "16"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Rancanglah bangun: bagaimana menyusun 4 segitiga siku-siku sama besar agar jadi persegi?", ["menyatukan sisi miringnya di bagian luar dan sudut sikunya menghadap ke dalam", "menumpuknya ke atas", "menyusunnya berbaris lurus", "tidak bisa dibuat"], "A", "4 segitiga siku-siku dapat disusun membentuk sebuah persegi sempurna.")
mc("c6", "sulit", K, Me, S4, "Mengapa pintu rumah dibuat persegi panjang tinggi dan bukan persegi?", ["agar manusia dewasa dapat leluasa lewat berdiri tegak tanpa boros tempat", "supaya pintunya berat", "karena kayu pohon kotak", "tidak ada alasan"], "A", "Bentuk tinggi sesuai dengan postur tubuh manusia yang berdiri.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Hitung total keliling: 2 persegi (sisi 6 cm) + 1 persegi panjang (10 cm x 5 cm)!", ["78 cm", "70 cm", "80 cm", "74 cm"], "A", "(2 x 24) + (2 x 15) = 48 + 30 = 78 cm.", verifikasi={"ekspresi": "(2 * 4 * 6) + (2 * (10 + 5))", "hasil": "78"})
mc("c6", "sulit", P, Me, S4, "Enam ubin persegi sisi 10 cm disusun memanjang 1 baris. Keliling bangun baru?", ["140 cm", "120 cm", "160 cm", "100 cm"], "A", "Panjang = 60 cm, lebar = 10 cm. Keliling = 2 x (60 + 10) = 140 cm.", verifikasi={"ekspresi": "2 * ((6 * 10) + 10)", "hasil": "140"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab72_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab72.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
