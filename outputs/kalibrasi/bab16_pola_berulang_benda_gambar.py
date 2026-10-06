#!/usr/bin/env python3
"""
Generator dan validator Bab 16 Matematika Kelas 1 SD:
"Mengenal Pola Berulang pada Benda dan Gambar" (Fase A)
bab_id: 91cb7028-3f4d-4b61-98ca-cf9b46d5d3da
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a6b5c49d7e01"  # Apa Itu Pola Berulang?
S2 = "b7c6d50e8f12"  # Pola Dua Unsur (AB - AB)
S3 = "c8d7e61f9a23"  # Pola Tiga Unsur (ABC - ABC)
S4 = "d9e8f72a0b34"  # Menemukan Inti Pola Pengulang

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Pernahkah kamu melihat pagar bergaris warna?
Ada merah, putih, merah, lalu putih.
Susunan itu disebut pola berulang.
Pola adalah susunan yang teratur.
Benda muncul kembali secara berulang.
Benda tidak ditaruh sembarangan.
Semua tersusun dengan rapi.
Ayo belajar mengenali pola.

:::definition
title: Arti Pola Berulang
Pola adalah susunan gambar teratur.
Benda berulang menurut urutan tertentu.
:::"""

s2_content = """Ada pola dengan dua benda bergantian.
Kita sebut pola dua unsur (AB-AB).
Contohnya: sendok, garpu, sendok, garpu.
Benda bergantian secara teratur.
Setelah sendok selalu ada garpu.
Setelah garpu kembali ke sendok.
Sangat mudah untuk ditebak.
Dua benda bergantian terus.

:::steps
title: Membaca Pola Dua Unsur
1. Sebutkan nama benda pertama (A).
2. Sebutkan nama benda kedua (B).
3. Ulangi sebutan benda pertama dan kedua.
:::"""

s3_content = """Ada juga pola dengan tiga benda.
Kita sebut pola tiga unsur (ABC-ABC).
Contohnya: apel, jeruk, pisang.
Lalu apel, jeruk, pisang lagi.
Ketiga buah berulang secara teratur.
Setelah pisang, kembali ke apel.
Perhatikan urutannya baik-baik.
Jangan sampai ada yang tertukar."""

s4_content = """Bagaimana menemukan kelanjutan pola?
Cari kelompok dasar pengulangnya.
Kelompok dasar itu disebut inti pola.
Jika intinya segitiga lalu lingkaran.
Maka setelah segitiga pasti lingkaran.

:::common_trap
title: Mengira Pola Berubah Saat Melihat Banyak Gambar
Lihatlah kelompok pertamanya terlebih dahulu.
Pola selalu mengulang kelompok yang sama.
Jangan menebak gambar baru yang aneh.
Cari pengulangan yang persis sama.
:::

:::callout
variant: summary
title: Ringkasan
text: Pola berulang tersusun teratur. Temukan kelompok inti pengulang untuk menebak benda berikutnya.
:::"""

sections = [
    {
        "id": S1,
        "title": "Apa Itu Pola Berulang?",
        "minutes": 6,
        "goal": "Siswa dapat memahami pengertian pola berulang sebagai susunan benda yang teratur.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Pola Dua Unsur (AB - AB)",
        "minutes": 6,
        "goal": "Siswa dapat mengenali dan membaca susunan pola berulang dua benda bergantian.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Pola Tiga Unsur (ABC - ABC)",
        "minutes": 6,
        "goal": "Siswa dapat mengenali dan membaca susunan pola berulang tiga benda bergantian.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menemukan Inti Pola Pengulang",
        "minutes": 6,
        "goal": "Siswa dapat menentukan inti pola pengulang untuk menebak benda berikutnya.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengenal Pola Berulang pada Benda dan Gambar",
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
# 2. DEFINISI BANK 50 SOAL BAB 16
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
mc("c1", "mudah", D, F, S1, "Susunan benda yang berulang secara teratur disebut ....", ["pola", "kumpulan", "deret", "garis"], "A", "Susunan berulang yang teratur disebut pola.")
tf("c1", "mudah", D, F, S2, "Pola dua unsur AB-AB memiliki dua benda yang bergantian.", "Benar", "Pola AB memiliki dua jenis benda yang bergantian secara berulang.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Kelompok dasar yang diulang pada suatu pola disebut ....", ["inti pola", "ujung pola", "sisa pola", "warna pola"], "A", "Kelompok pengulang dasar disebut inti pola.")
mc("c1", "mudah", T, F, S2, "Berapa banyak macam benda dalam pola dua unsur?", ["2 macam", "3 macam", "4 macam", "1 macam"], "A", "Pola dua unsur terdiri atas 2 macam benda.", verifikasi={"ekspresi": "2", "hasil": "2"})
sa("c1", "mudah", T, F, S3, "Berapa banyak macam benda pada pola tiga unsur ABC?", "3", "Pola ABC memiliki 3 macam benda.", verifikasi={"ekspresi": "3", "hasil": "3"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Pola: bola, kubus, bola, kubus. Benda berikutnya adalah ....", ["bola", "kubus", "tabung", "bintang"], "A", "Setelah kubus kembali ke bola.")
tf("c2", "mudah", D, Kn, S3, "Pola apel, jeruk, pisang, apel, jeruk, pisang memiliki 3 unsur.", "Benar", "Ada 3 buah yaitu apel, jeruk, dan pisang.")

# Remedial (2)
mc("c2", "mudah", R, F, S4, "Untuk menebak kelanjutan pola, kita harus mencari ....", ["inti pengulangannya", "warna paling terang", "benda paling besar", "benda yang paling akhir"], "A", "Mencari inti pengulangan adalah kunci memahami pola.", "Menebak pola secara acak tanpa melihat inti")
mc("c2", "mudah", R, Kn, S2, "Pola: merah, biru, merah, biru. Warna berikutnya adalah ....", ["merah", "biru", "kuning", "hijau"], "A", "Setelah biru adalah merah.", "Tertukar urutan pengulangan pola dua warna")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Manakah yang merupakan susunan pola teratur?", ["bintang, bulan, bintang, bulan", "bintang, bulan, matahari, pohon", "bulan, bulan, bulan, bintang", "matahari, pohon, awan, hujan"], "A", "Bintang dan bulan bergantian secara teratur.")
mc("c2", "mudah", T, Kn, S2, "Pola: sendok, garpu, sendok, garpu. Berapa pasang sendok-garpu pada 4 benda itu?", ["2 pasang", "3 pasang", "1 pasang", "4 pasang"], "A", "4 benda terbagi jadi 2 pasang.", verifikasi={"ekspresi": "4 // 2", "hasil": "2"})
tf("c2", "mudah", T, Kn, S3, "Susunan lingkaran, segitiga, lingkaran, segitiga adalah pola tiga unsur.", "Salah", "Hanya ada 2 bentuk (lingkaran dan segitiga), jadi pola dua unsur.")
sa("c2", "mudah", T, Kn, S4, "Pola: 1, 2, 1, 2, 1, .... Angka berikutnya adalah?", "2", "Setelah angka 1 adalah angka 2.", verifikasi={"ekspresi": "2", "hasil": "2"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Pola: buku, pensil, buku, pensil, buku, .... Benda selanjutnya adalah ....", ["pensil", "buku", "penghapus", "penggaris"], "A", "Setelah buku selalu pensil.", "Salah melanjutkan pola benda berulang")
mc("c3", "sedang", R, Pr, S3, "Pola: merah, kuning, hijau, merah, kuning, .... Warna berikutnya adalah ....", ["hijau", "merah", "kuning", "biru"], "A", "Setelah kuning adalah hijau.", "Salah menentukan kelanjutan pola tiga unsur")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Jika pola dua benda berulang 3 kali, ada berapa total benda?", ["6 benda", "5 benda", "7 benda", "4 benda"], "A", "2 x 3 = 6 benda.", verifikasi={"ekspresi": "2 * 3", "hasil": "6"})
mc("c3", "sedang", T, Pr, S2, "Pola: segitiga, kotak, segitiga, kotak. Berapa banyak segitiga pada susunan 8 benda?", ["4", "3", "5", "6"], "A", "8 / 2 = 4 segitiga.", verifikasi={"ekspresi": "8 // 2", "hasil": "4"})
tf("c3", "sedang", T, Pr, S3, "Pola apel, mangga, apel, mangga memiliki inti apel dan mangga.", "Benar", "Inti pengulangannya adalah pasangan apel dan mangga.")
mc("c3", "sedang", T, Pr, S4, "Pola: 3, 5, 3, 5, 3, 5. Berapa kali pasangan (3, 5) berulang?", ["3 kali", "2 kali", "4 kali", "5 kali"], "A", "Ada 6 angka, 6 / 2 = 3 kali.", verifikasi={"ekspresi": "6 // 2", "hasil": "3"})
tf("c3", "sedang", T, Pr, S1, "Pola berulang boleh memasukkan benda acak sesuka hati.", "Salah", "Pola harus teratur dan konsisten, tidak boleh sembarangan.")
sa("c3", "mudah", T, Pr, S2, "Pola tiga benda berulang 2 kali. Berapa total bendanya?", "6", "3 x 2 = 6 benda.", verifikasi={"ekspresi": "3 * 2", "hasil": "6"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Pola: topi, dasi, topi, dasi, topi, dasi. Berapa banyak topi seluruhnya?", ["3 topi", "2 topi", "4 topi", "5 topi"], "A", "6 benda dengan pola dua unsur memuat 3 topi.", verifikasi={"ekspresi": "6 // 2", "hasil": "3"})
mc("c3", "sedang", X, Pr, S2, "Pola: 4, 7, 4, 7, 4, 7, 4. Angka berikutnya adalah ....", ["7", "4", "5", "8"], "A", "Setelah 4 adalah 7.", verifikasi={"ekspresi": "7", "hasil": "7"})
tf("c3", "sedang", X, Pr, S3, "Pola ABC jika berulang 3 kali berjumlah 9 benda.", "Benar", "3 x 3 = 9 benda.", verifikasi={"ekspresi": "3 * 3", "hasil": "9"})
sa("c3", "sedang", X, Pr, S4, "Pola dua benda berulang 5 kali. Berapa total bendanya?", "10", "2 x 5 = 10 benda.", verifikasi={"ekspresi": "2 * 5", "hasil": "10"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Jika pola dua unsur berulang 4 kali, berapa total benda?", ["8 benda", "6 benda", "10 benda", "7 benda"], "A", "2 x 4 = 8 benda.", verifikasi={"ekspresi": "2 * 4", "hasil": "8"})
mc("c3", "sedang", K, Pr, S3, "Pola: 1, 2, 3, 1, 2, 3, 1, 2, .... Angka berikutnya adalah ....", ["3", "1", "2", "4"], "A", "Urutan inti adalah 1, 2, 3. Jadi setelah 2 adalah 3.", verifikasi={"ekspresi": "3", "hasil": "3"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Manakah dari susunan berikut yang BUKAN merupakan pola teratur?", ["kucing, anjing, kucing, kelinci", "kucing, anjing, kucing, anjing", "merah, biru, merah, biru", "1, 2, 1, 2"], "A", "Kucing, anjing, kucing, kelinci tidak teratur pengulangannya.")
mc("c4", "sedang", T, Kn, S2, "Pola A: bulat, kotak, bulat, kotak. Pola B: 1, 2, 1, 2. Persamaan kedua pola adalah ....", ["keduanya berpola dua unsur AB", "memiliki gambar yang sama", "memiliki angka yang sama", "keduanya berpola tiga unsur"], "A", "Keduanya memiliki struktur dua unsur bergantian.")
tf("c4", "sedang", T, Kn, S3, "Pola bunga, daun, ranting, bunga, daun, ranting memiliki inti 2 benda.", "Salah", "Inti pengulangnya ada 3 benda, bukan 2 benda.")
tf("c4", "sedang", T, Kn, S4, "Jika inti pola adalah bintang dan hati, gambar ke-5 pasti hati.", "Salah", "Pola: bintang(1), hati(2), bintang(3), hati(4), bintang(5). Jadi ke-5 adalah bintang.")
sa("c4", "sedang", T, Kn, S4, "Berapa banyak pengulangan inti pola pada deret 12 benda berpola 3 unsur?", "4", "12 / 3 = 4 kali pengulangan.", verifikasi={"ekspresi": "12 // 3", "hasil": "4"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Pola: A, B, A, B, A, .... Huruf pada urutan ke-8 adalah ....", ["B", "A", "C", "D"], "A", "Urutan genap selalu B (2, 4, 6, 8).")
mc("c4", "sedang", X, Kn, S2, "Pola 1, 2, 1, 2 memiliki banyak angka 1 dan 2 yang ....", ["sama banyak", "lebih banyak angka 1", "lebih banyak angka 2", "tidak tentu"], "A", "Pengulangan lengkap memuat jumlah yang sama banyak.")
tf("c4", "sedang", X, Kn, S4, "Pada pola tiga unsur, benda ke-1 dan benda ke-4 adalah benda yang sama.", "Benar", "Benda ke-4 memulai kembali inti pola (sama dengan ke-1).")
mc("c4", "sulit", X, Me, S4, "Ada deret: 2, 4, 2, 4, 2, 4, 2, 4. Berapa jumlah semua angka 2?", ["4", "3", "5", "2"], "A", "Ada 4 angka 2.", verifikasi={"ekspresi": "8 // 2", "hasil": "4"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Manakah pola yang memiliki struktur pengulangan sama dengan apel, jeruk, apel, jeruk?", ["garpu, sendok, garpu, sendok", "apel, apel, jeruk, jeruk", "apel, pisang, jeruk, mangga", "jeruk, jeruk, jeruk, apel"], "A", "Keduanya berpola dua unsur bergantian AB-AB.")
mc("c4", "sulit", K, Me, S2, "Jika pada 10 benda berpola dua unsur dihitung, berapa banyak benda kedua?", ["5", "4", "6", "3"], "A", "10 / 2 = 5 benda.", verifikasi={"ekspresi": "10 // 2", "hasil": "5"})
tf("c4", "sulit", K, Me, S3, "Pola dua unsur yang berulang 6 kali memiliki total 14 benda.", "Salah", "Totalnya 2 x 6 = 12 benda, bukan 14.")
mc("c4", "sulit", K, Me, S4, "Pola: merah, kuning, hijau. Benda ke-7 memiliki warna apa?", ["merah", "kuning", "hijau", "biru"], "A", "1, 4, 7 adalah merah.")

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Ada susunan: pensil, buku, pensil, pensil, buku. Bagian mana yang keliru?", ["pensil kedua muncul dua kali", "buku tidak ada", "pensil pertama salah", "semua sudah benar"], "A", "Pensil kedua berulang dua kali sehingga merusak pola.")
mc("c5", "sedang", T, Me, S2, "Jika kamu ingin membuat pagar pola dua warna sepanjang 12 tiang, berapa tiang tiap warna?", ["6 tiang", "5 tiang", "7 tiang", "4 tiang"], "A", "12 / 2 = 6 tiang tiap warna.", verifikasi={"ekspresi": "12 // 2", "hasil": "6"})
mc("c5", "sedang", T, Me, S3, "Dina menyusun jeruk, apel, pisang, jeruk, apel. Buah apa berikutnya agar lengkap?", ["pisang", "jeruk", "apel", "mangga"], "A", "Pengulangan kedua membutuhkan pisang di akhir.")
mc("c5", "sulit", T, Me, S4, "Pada pola segitiga, kotak, lingkaran yang berulang 4 kali, berapa total bentuknya?", ["12 bentuk", "10 bentuk", "14 bentuk", "9 bentuk"], "A", "3 x 4 = 12 bentuk.", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Kalung merah, biru bergantian. Ada 8 manik merah, berapa manik biru dibutuhkan?", ["8 manik", "7 manik", "9 manik", "6 manik"], "A", "Manik merah dan biru sama banyak, yaitu 8.", verifikasi={"ekspresi": "8", "hasil": "8"})
mc("c5", "sulit", K, Me, S4, "Sebuah gelang memuat 15 manik berpola tiga warna sama rata. Berapa banyak manik tiap warna?", ["5 manik", "4 manik", "6 manik", "3 manik"], "A", "15 / 3 = 5 manik tiap warna.", verifikasi={"ekspresi": "15 // 3", "hasil": "5"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Susunlah pola dua unsur baru menggunakan bentuk geometri!", ["lingkaran, kotak, lingkaran, kotak", "lingkaran, segitiga, kotak, bintang", "kotak, kotak, kotak, kotak", "segitiga, lingkaran, bintang, bulan"], "A", "Lingkaran dan kotak bergantian membentuk pola dua unsur.")
mc("c6", "sulit", K, Me, S4, "Rancanglah pola tiga unsur dengan total 9 benda!", ["tiga kali pengulangan dari 3 benda", "dua kali pengulangan dari 4 benda", "empat kali pengulangan dari 2 benda", "satu kali pengulangan dari 9 benda"], "A", "3 x 3 = 9 benda.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Rancanglah gelang dengan 16 manik berpola dua warna selang-seling! Berapa manik warna pertama?", ["8 manik", "6 manik", "10 manik", "7 manik"], "A", "16 / 2 = 8 manik.", verifikasi={"ekspresi": "16 // 2", "hasil": "8"})
mc("c6", "sulit", P, Me, S4, "Susunlah aturan pola tiga unsur agar kita langsung tahu gambar ke-10!", ["gambar ke-10 sama dengan gambar ke-1", "gambar ke-10 sama dengan gambar ke-2", "gambar ke-10 sama dengan gambar ke-3", "gambar ke-10 tidak bisa ditentukan"], "A", "Kelipatan 3 berakhir di 9, sehingga ke-10 mengulang gambar ke-1.")

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab16_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab16.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
