#!/usr/bin/env python3
"""
Generator dan validator Bab 17 Matematika Kelas 1 SD:
"Melanjutkan Pola Bentuk, Warna, dan Ukuran" (Fase A)
bab_id: 407cfaf2-5ff6-4cd6-b10e-b7c47e53ac0f
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a7b6c59d8e01"  # Pola Berdasarkan Bentuk Geometri
S2 = "b8c7d60e9f12"  # Pola Berdasarkan Perubahan Warna
S3 = "c9d8e71f0a23"  # Pola Berdasarkan Perubahan Ukuran
S4 = "d0e9f82a1b34"  # Pola Campuran Bentuk dan Warna

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Bentuk bangun datar bisa membentuk pola.
Contohnya lingkaran, segitiga, lingkaran, segitiga.
Lihat bentuk yang bergantian.
Setelah segitiga kembali ke lingkaran.
Setelah lingkaran kembali ke segitiga.
Bentuknya selalu berulang rapi.
Ayo amati bentuknya baik-baik.

:::definition
title: Pola Bentuk
Pola bentuk adalah susunan bentuk berulang teratur.
Bentuk berulang secara bergantian.
:::"""

s2_content = """Bentuk benda bisa saja sama.
Namun warnanya yang berganti-ganti.
Misalnya lingkaran merah, lingkaran biru.
Lalu lingkaran merah, lingkaran biru.
Bentuk tetap lingkaran semua.
Hanya warnanya yang berulang.
Perhatikan perubahan warnanya.

:::steps
title: Menemukan Pola Warna
1. Amati bentuk benda pertama.
2. Perhatikan warna tiap benda.
3. Sebutkan warna secara berurutan.
:::"""

s3_content = """Ukuran benda juga bisa berpola.
Ada ukuran besar dan kecil.
Contoh: bola besar, bola kecil.
Lalu bola besar, bola kecil.
Ada juga urutan membesar.
Kecil, sedang, lalu besar.
Lihat perbedaannya dengan teliti.
Semua tersusun dengan teratur."""

s4_content = """Terkadang ada dua ciri berubah.
Bentuk dan warnanya berganti bersamaan.
Misalnya segitiga merah, persegi biru.
Lalu segitiga merah, persegi biru.
Periksa bentuk dan warnanya.

:::common_trap
title: Lupa Memeriksa Warna
Lihatlah semua ciri gambar.
Bentuknya mungkin sudah tepat segitiga.
Namun warnanya harus ikut tepat.
Periksa bentuk dan warnanya bersamaan.
:::

:::callout
variant: summary
title: Ringkasan
text: Pola bisa berupa bentuk, warna, atau ukuran. Periksa semua ciri agar pilihanmu benar.
:::"""

sections = [
    {
        "id": S1,
        "title": "Pola Berdasarkan Bentuk Geometri",
        "minutes": 6,
        "goal": "Siswa dapat mengenali dan melanjutkan pola keteraturan berdasarkan bentuk geometri bangun datar.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Pola Berdasarkan Perubahan Warna",
        "minutes": 6,
        "goal": "Siswa dapat mengenali dan melanjutkan pola keteraturan berdasarkan variasi warna benda.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Pola Berdasarkan Perubahan Ukuran",
        "minutes": 6,
        "goal": "Siswa dapat mengenali dan melanjutkan pola keteraturan berdasarkan ukuran besar-kecil.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Pola Campuran Bentuk dan Warna",
        "minutes": 6,
        "goal": "Siswa dapat menganalisis dan melanjutkan pola kombinasi dua atribut visual sekaligus.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Melanjutkan Pola Bentuk, Warna, dan Ukuran",
    "topic": "Pola dan Urutan",
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
# 2. DEFINISI BANK 50 SOAL BAB 17
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
mc("c1", "mudah", D, F, S1, "Susunan bentuk lingkaran, segitiga, lingkaran, segitiga berganti secara ....", ["teratur", "acak", "bebas", "berantakan"], "A", "Pola tersusun secara teratur.")
tf("c1", "mudah", D, F, S2, "Pola merah, kuning, merah, kuning adalah pola perubahan warna.", "Benar", "Bentuknya sama tetapi warnanya yang berganti secara teratur.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Berapa banyak bentuk berbeda pada pola segitiga dan lingkaran?", ["2 bentuk", "3 bentuk", "4 bentuk", "1 bentuk"], "A", "Hanya ada 2 bentuk: segitiga dan lingkaran.", verifikasi={"ekspresi": "2", "hasil": "2"})
mc("c1", "mudah", T, F, S2, "Ada berapa warna pada pola merah, hijau, merah, hijau?", ["2 warna", "3 warna", "4 warna", "1 warna"], "A", "Hanya ada 2 warna yaitu merah dan hijau.", verifikasi={"ekspresi": "2", "hasil": "2"})
sa("c1", "mudah", T, F, S3, "Berapa macam ukuran pada pola: bola besar, bola kecil?", "2", "Ada 2 macam ukuran: besar dan kecil.", verifikasi={"ekspresi": "2", "hasil": "2"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Pola: kotak, bulat, kotak, bulat. Bentuk selanjutnya adalah ....", ["kotak", "bulat", "segitiga", "bintang"], "A", "Setelah bulat kembali ke kotak.")
tf("c2", "mudah", D, Kn, S3, "Pola: besar, kecil, besar, kecil memiliki 2 variasi ukuran.", "Benar", "Ada 2 ukuran yaitu besar dan kecil.")

# Remedial (2)
mc("c2", "mudah", R, F, S4, "Saat memilih kelanjutan pola gambar, kita harus memeriksa ....", ["bentuk dan warnanya", "hanya bentuknya", "hanya warnanya", "ukuran kertasnya"], "A", "Periksa semua ciri termasuk bentuk dan warna.", "Hanya melihat bentuk tanpa melihat warna")
mc("c2", "mudah", R, Kn, S2, "Pola: biru, merah, biru, merah, biru. Warna berikutnya adalah ....", ["merah", "biru", "kuning", "hijau"], "A", "Setelah biru adalah merah.", "Tertukar urutan pengulangan warna")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Manakah pasangan bentuk yang bergantian pada pola segitiga-persegi?", ["segitiga dan persegi", "lingkaran dan bintang", "persegi dan lonjong", "semua segitiga"], "A", "Intinya adalah segitiga dan persegi.")
mc("c2", "mudah", T, Kn, S2, "Pola warna: kuning, hijau, kuning, hijau. Benda ke-4 berwarna ....", ["hijau", "kuning", "merah", "biru"], "A", "Urutan: 1 kuning, 2 hijau, 3 kuning, 4 hijau.")
tf("c2", "mudah", T, Kn, S3, "Pola ukuran besar, sedang, kecil hanya memiliki 2 tingkatan ukuran.", "Salah", "Pola tersebut memiliki 3 tingkatan ukuran: besar, sedang, dan kecil.")
sa("c2", "mudah", T, Kn, S4, "Pola dua warna berulang 3 kali. Berapa total bendanya?", "6", "2 x 3 = 6 benda.", verifikasi={"ekspresi": "2 * 3", "hasil": "6"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Pola: bulat, segitiga, kotak, bulat, segitiga, .... Bentuk selanjutnya adalah ....", ["kotak", "bulat", "segitiga", "bintang"], "A", "Setelah segitiga pada inti adalah kotak.", "Salah melanjutkan pola tiga bentuk geometri")
mc("c3", "sedang", R, Pr, S3, "Pola: kecil, sedang, besar, kecil, sedang, .... Ukuran berikutnya adalah ....", ["besar", "kecil", "sedang", "sangat kecil"], "A", "Setelah sedang adalah besar.", "Salah mengurutkan pola ukuran bertingkat")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Ada 8 bentuk berpola dua unsur. Berapa banyak bentuk pertama?", ["4", "3", "5", "6"], "A", "8 / 2 = 4 bentuk pertama.", verifikasi={"ekspresi": "8 // 2", "hasil": "4"})
mc("c3", "sedang", T, Pr, S2, "Pola: merah, putih, merah, putih. Pada 10 bendera, berapa bendera merah?", ["5", "4", "6", "3"], "A", "10 / 2 = 5 bendera merah.", verifikasi={"ekspresi": "10 // 2", "hasil": "5"})
tf("c3", "sedang", T, Pr, S3, "Pola pensil panjang, pendek, panjang, pendek berganti ukuran teratur.", "Benar", "Panjang dan pendek bergantian secara teratur.")
mc("c3", "sedang", T, Pr, S4, "Berapa banyak bentuk pada pola campuran yang berulang 4 kali?", ["8 bentuk", "6 bentuk", "10 bentuk", "7 bentuk"], "A", "2 x 4 = 8 bentuk.", verifikasi={"ekspresi": "2 * 4", "hasil": "8"})
tf("c3", "sedang", T, Pr, S1, "Pola bentuk lingkaran, segitiga, kotak berulang setiap 4 bentuk.", "Salah", "Berulang setiap 3 bentuk, bukan 4 bentuk.")
sa("c3", "mudah", T, Pr, S2, "Pola 3 warna berulang 2 kali. Berapa total bendanya?", "6", "3 x 2 = 6 benda.", verifikasi={"ekspresi": "3 * 2", "hasil": "6"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Pola: segitiga, lingkaran, segitiga, lingkaran. Bentuk ke-7 adalah ....", ["segitiga", "lingkaran", "kotak", "bintang"], "A", "Urutan ganjil (1, 3, 5, 7) selalu segitiga.")
mc("c3", "sedang", X, Pr, S2, "Pola: hitam, putih, hitam, putih. Pada 12 ubin, berapa ubin hitam?", ["6", "5", "7", "4"], "A", "12 / 2 = 6 ubin hitam.", verifikasi={"ekspresi": "12 // 2", "hasil": "6"})
tf("c3", "sedang", X, Pr, S3, "Pola apel besar, apel kecil berulang 5 kali berisi 10 apel.", "Benar", "2 x 5 = 10 apel.", verifikasi={"ekspresi": "2 * 5", "hasil": "10"})
sa("c3", "sedang", X, Pr, S4, "Pola segitiga merah, kotak biru berulang 4 kali. Berapa totalnya?", "8", "2 x 4 = 8 bangun datar.", verifikasi={"ekspresi": "2 * 4", "hasil": "8"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Pola 3 bentuk geometri berulang 3 kali. Berapa jumlah semua bentuk?", ["9 bentuk", "8 bentuk", "6 bentuk", "12 bentuk"], "A", "3 x 3 = 9 bentuk.", verifikasi={"ekspresi": "3 * 3", "hasil": "9"})
mc("c3", "sedang", K, Pr, S2, "Pola: merah, kuning, hijau berulang 2 kali. Berapa jumlah warna kuning?", ["2", "3", "1", "4"], "A", "Tiap pengulangan ada 1 kuning, jadi 1 x 2 = 2.", verifikasi={"ekspresi": "1 * 2", "hasil": "2"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Manakah susunan yang BUKAN merupakan pola bentuk teratur?", ["kotak, bulat, kotak, bintang", "kotak, bulat, kotak, bulat", "segitiga, kotak, segitiga, kotak", "bulat, lonjong, bulat, lonjong"], "A", "Kotak, bulat, kotak, bintang tidak memiliki aturan berulang yang tetap.")
mc("c4", "sedang", T, Kn, S2, "Pola pita: merah, biru, merah, biru. Apa ciri utama pola tersebut?", ["perubahan warna dua unsur", "perubahan bentuk benda", "perubahan ukuran benda", "perubahan jumlah benda"], "A", "Pola tersebut merupakan perubahan warna dua unsur berulang.")
tf("c4", "sedang", T, Kn, S3, "Pola buku besar, buku kecil, buku besar memiliki bentuk berbeda.", "Salah", "Bentuknya tetap buku, yang berbeda adalah ukurannya.")
tf("c4", "sedang", T, Kn, S4, "Pola segitiga merah, persegi biru memiliki perubahan bentuk dan warna.", "Benar", "Kedua ciri (bentuk dan warna) berganti secara teratur.")
sa("c4", "sedang", T, Kn, S4, "Berapa banyak pasang bentuk-warna pada deret 14 benda berpola 2 unsur?", "7", "14 / 2 = 7 pasang.", verifikasi={"ekspresi": "14 // 2", "hasil": "7"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Pola: bulat, segitiga, kotak, bulat, segitiga, kotak. Bentuk ke-8 adalah ....", ["segitiga", "bulat", "kotak", "bintang"], "A", "8 dibagi 3 sisa 2, urutan ke-2 adalah segitiga.")
mc("c4", "sedang", X, Kn, S2, "Lampu hias: merah, kuning, hijau. Lampu ke-6 berwarna apa?", ["hijau", "merah", "kuning", "biru"], "A", "Kelipatan 3 (3, 6) adalah hijau.")
tf("c4", "sedang", X, Kn, S3, "Urutan kecil, besar, kecil, besar adalah pola perubahan warna.", "Salah", "Itu adalah pola variasi ukuran, bukan pola warna.")
mc("c4", "sulit", X, Me, S4, "Pola: bintang kuning, bulan biru berulang 5 kali. Berapa bintang kuning?", ["5", "4", "6", "10"], "A", "Ada 5 bintang kuning pada 5 pengulangan.", verifikasi={"ekspresi": "5", "hasil": "5"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Bandingkan pola A (bulat, kotak) dan pola B (besar, kecil). Keduanya sama-sama ....", ["berpola dua unsur berulang", "mengubah bentuk benda", "mengubah warna benda", "berpola tiga unsur"], "A", "Keduanya memiliki struktur dua unsur berulang AB-AB.")
mc("c4", "sulit", K, Me, S2, "Pola warna merah, putih berulang pada 16 bendera. Berapa bendera putih?", ["8", "7", "9", "6"], "A", "16 / 2 = 8 bendera putih.", verifikasi={"ekspresi": "16 // 2", "hasil": "8"})
tf("c4", "sulit", K, Me, S3, "Pola ukuran pensil berulang 4 kali dari 3 ukuran berjumlah 15 pensil.", "Salah", "3 x 4 = 12 pensil, bukan 15 pensil.")
mc("c4", "sulit", K, Me, S4, "Pola: segitiga hijau, kotak merah berulang 6 kali. Berapa total bangun?", ["12", "10", "14", "8"], "A", "2 x 6 = 12 bangun.", verifikasi={"ekspresi": "2 * 6", "hasil": "12"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Terdapat susunan: bulat, segitiga, bulat, kotak. Manakah yang harus diperbaiki?", ["kotak diganti segitiga", "bulat pertama diganti kotak", "segitiga dihapus", "semua sudah benar"], "A", "Agar berpola dua unsur, kotak harus diganti segitiga.")
mc("c5", "sedang", T, Me, S2, "Lani punya 7 bunga merah dan 7 bunga putih. Berapa total bunga berpola?", ["14 bunga", "12 bunga", "10 bunga", "16 bunga"], "A", "7 + 7 = 14 bunga.", verifikasi={"ekspresi": "7 + 7", "hasil": "14"})
mc("c5", "sedang", T, Me, S3, "Urutan balok: kecil, sedang, besar, kecil, sedang. Balok apa yang kurang?", ["balok besar", "balok kecil", "balok sedang", "balok panjang"], "A", "Pengulangan kedua membutuhkan balok besar.")
mc("c5", "sulit", T, Me, S4, "Pola kombinasi 2 atribut berulang 7 kali. Berapa banyak benda seluruhnya?", ["14 benda", "12 benda", "16 benda", "10 benda"], "A", "2 x 7 = 14 benda.", verifikasi={"ekspresi": "2 * 7", "hasil": "14"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Udin menyusun 18 balok dengan pola 3 bentuk berulang. Berapa kali pengulangan?", ["6 kali", "5 kali", "7 kali", "4 kali"], "A", "18 / 3 = 6 kali pengulangan.", verifikasi={"ekspresi": "18 // 3", "hasil": "6"})
mc("c5", "sulit", K, Me, S4, "Pada kalung manik bentuk-warna, ada 9 pasang manik. Berapa total manik?", ["18 manik", "16 manik", "20 manik", "15 manik"], "A", "9 x 2 = 18 manik.", verifikasi={"ekspresi": "9 * 2", "hasil": "18"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Susunlah pola bentuk dan warna baru dengan dua unsur berulang!", ["segitiga merah, lingkaran biru", "segitiga merah, segitiga hijau", "lingkaran merah, lingkaran biru", "semua bentuk dan warna sama"], "A", "Segitiga merah dan lingkaran biru memadukan bentuk dan warna bergantian.")
mc("c6", "sulit", K, Me, S4, "Rancanglah pola tiga bentuk geometri dengan total 12 bangun datar!", ["empat kali pengulangan pola tiga bentuk", "tiga kali pengulangan pola empat bentuk", "dua kali pengulangan pola enam bentuk", "enam kali pengulangan pola dua bentuk"], "A", "3 x 4 = 12 bangun datar.", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Rancanglah susunan ubin berpola dua warna dengan total 20 ubin! Berapa ubin per warna?", ["10 ubin", "8 ubin", "12 ubin", "9 ubin"], "A", "20 / 2 = 10 ubin tiap warna.", verifikasi={"ekspresi": "20 // 2", "hasil": "10"})
mc("c6", "sulit", P, Me, S4, "Susunlah aturan pola bentuk-warna 3 unsur agar tahu benda ke-13!", ["benda ke-13 sama dengan benda ke-1", "benda ke-13 sama dengan benda ke-2", "benda ke-13 sama dengan benda ke-3", "benda ke-13 tidak dapat dipastikan"], "A", "12 habis dibagi 3, sehingga ke-13 kembali ke unsur pertama.")

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab17_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab17.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
