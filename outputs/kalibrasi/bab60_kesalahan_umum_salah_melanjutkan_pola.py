#!/usr/bin/env python3
"""
Generator dan validator Bab 60 Matematika Kelas 2 SD:
"Kesalahan Umum: Salah Melanjutkan Pola pada Loncatan" (Fase A)
bab_id: 9ed642fc-f623-4c76-aa01-fedd8640ab7d
article_id: 4fcf77ba-7b70-4d87-9cb8-b2ef62b66236
quiz_id: a574b54a-7c69-49ab-87e6-1aca7e074fa6
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "e1g2i3k4m501"  # Kesalahan 1: Selisih Berbeda-beda
S2 = "f2h3j4l5n602"  # Kesalahan 2: Tertukar Menambah dan Mengurang
S3 = "g3i4k5m6o703"  # Kesalahan 3: Keliru Menyeberang Batas Puluhan
S4 = "h4j5l6n7p804"  # Strategi Cek Ulang Pola

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Banyak anak keliru membuat pola.
Aturan pola sering berubah-ubah.
Contoh salah: 2, 4, 7, 9.
Mula-mula ditambah dua.
Lalu tiba-tiba ditambah tiga.
Ini bukan pola yang benar!
Aturan pola harus selalu sama.
Jika tambah dua, tambah dua terus.
Konsisten adalah kunci utama!

:::definition
title: Aturan Pola yang Konsisten
Pola bilangan yang benar memiliki selisih yang selalu sama pada setiap langkah.
:::"""

s2_content = """Kesalahan kedua adalah tertukar operasi.
Pola turun malah ditambah.
Pola naik malah dikurang.
Contoh: 30, 25, 20, 25.
Seharusnya 20 dikurang lima menjadi 15.
Bukan malah ditambah menjadi 25.
Perhatikan selalu arah polanya.
Membesar artinya ditambah.
Mengecil artinya dikurang!

:::steps
title: Langkah Memeriksa Arah Pola
1. Amati dua angka pertama.
2. Jika membesar, gunakan tanda tambah.
3. Jika mengecil, gunakan tanda kurang.
:::"""

s3_content = """Menyeberang puluhan sering menjebak.
Contohnya pada loncat lima.
Dari 28 ditambah lima.
Banyak anak menjawab 32.
Padahal 28 ditambah lima adalah 33!
Uraikan langkah dengan cermat:
28 tambah 2 jadi 30.
30 tambah 3 jadi 33.
Hitunglah teliti saat melewati puluhan!"""

s4_content = """Bagaimana cara agar tidak salah?
Lakukan cek ulang dua kali.
Hitung selisih pasangan angka depan.
Hitung selisih pasangan angka belakang.
Keduanya harus sama persis.
Jika beda, hitung ulang kembali.
Pemeriksaan teliti mencegah kesalahan!

:::common_trap
title: Menganggap Pola Selesai Tanpa Diuji
Jangan langsung puas dengan satu tebakan.
Ujilah aturan pada seluruh bilangan yang ada!
:::

:::callout
variant: summary
title: Ringkasan
text: Pola harus konsisten. Periksa arah naik atau turun. Cek ulang selisih antarbilangan.
:::"""

sections = [
    {
        "id": S1,
        "title": "Kesalahan 1: Selisih Berbeda-beda",
        "minutes": 6,
        "goal": "Siswa mampu mengidentifikasi pola yang salah karena aturan perubahannya tidak konsisten.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Kesalahan 2: Tertukar Menambah dan Mengurang",
        "minutes": 6,
        "goal": "Siswa mampu membedakan operasi tambah untuk pola naik dan kurang untuk pola turun.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Kesalahan 3: Keliru Menyeberang Batas Puluhan",
        "minutes": 6,
        "goal": "Siswa mampu membilang loncat secara tepat saat melewati batas puluhan berikutnya.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Strategi Cek Ulang Pola",
        "minutes": 6,
        "goal": "Siswa mampu memverifikasi kebenaran pola bilangan menggunakan teknik perbandingan selisih.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Salah Melanjutkan Pola pada Loncatan",
    "topic": "Bilangan Genap, Ganjil, dan Pola Bilangan",
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
# 2. DEFINISI BANK 50 SOAL BAB 60
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
mc("c1", "mudah", D, F, S1, "Urutan bilangan 2, 4, 7, 9 BUKAN pola benar karena ....", ["selisihnya tidak sama", "semuanya genap", "angkanya terlalu besar", "tidak ada angka nol"], "A", "2 ke 4 (+2), tapi 4 ke 7 (+3). Selisih tidak teratur.")
tf("c1", "mudah", D, F, S2, "Pola bilangan turun menggunakan operasi penjumlahan.", "Salah", "Pola turun nilainya mengecil sehingga memakai operasi pengurangan.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Jika pola mengecil, operasi yang harus kita gunakan adalah ....", ["pengurangan", "penjumlahan", "perkalian", "pembagian"], "A", "Pola mengecil menggunakan pengurangan.")
mc("c1", "mudah", T, F, S3, "Berapakah hasil dari 28 ditambah 5?", ["33", "32", "34", "30"], "A", "28 + 5 = 33.", verifikasi={"ekspresi": "28 + 5", "hasil": "33"})
sa("c1", "mudah", T, F, S4, "Berapakah selisih angka pada pola 10, 15, 20?", "5", "15 - 10 = 5.", verifikasi={"ekspresi": "15 - 10", "hasil": "5"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Untuk memastikan suatu pola benar, kita perlu memeriksa ....", ["selisih antarsetiap angka", "warna angkanya", "banyaknya halaman", "nama pembuat soal"], "A", "Selisih antarsetiap angka harus sama persis.")
tf("c2", "mudah", D, Kn, S1, "Pola bilangan yang benar selalu memiliki aturan yang tetap.", "Benar", "Aturan pola tidak boleh berubah di tengah jalan.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S3, "Budi menjawab 27 + 5 = 31. Jawaban yang BENAR adalah ....", ["32", "31", "30", "33"], "A", "27 + 5 = 32.", "Salah menyeberang puluhan", verifikasi={"ekspresi": "27 + 5", "hasil": "32"})
mc("c2", "mudah", R, Kn, S2, "Pola turun: 50, 45, 40, ... Lanjutan yang benar adalah ....", ["35", "45", "30", "50"], "A", "40 - 5 = 35.", "Tertukar kurang dengan tambah", verifikasi={"ekspresi": "40 - 5", "hasil": "35"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Manakah dari urutan berikut yang memiliki aturan TIDAK tetap?", ["5, 10, 14, 20", "3, 6, 9, 12", "10, 20, 30, 40", "4, 8, 12, 16"], "A", "5 ke 10 (+5), 10 ke 14 (+4). Aturan berubah-ubah.")
mc("c2", "mudah", T, Kn, S3, "Hitunglah dengan teliti: 46 + 7 = ....", ["53", "52", "51", "54"], "A", "46 + 7 = 53.", verifikasi={"ekspresi": "46 + 7", "hasil": "53"})
tf("c2", "mudah", T, Kn, S4, "Urutan 12, 16, 20, 24 adalah pola yang benar bertambah 4.", "Benar", "Selisih semuanya konsisten 4.")
sa("c2", "mudah", T, Kn, S2, "Berapakah hasil 60 dikurang 8 pada pola turun?", "52", "60 - 8 = 52.", verifikasi={"ekspresi": "60 - 8", "hasil": "52"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Urutan: 4, 8, 12, 15. Di manakah letak kesalahan pola?", ["angka 15 seharusnya 16", "angka 8 seharusnya 7", "angka 12 seharusnya 10", "tidak ada kesalahan"], "A", "12 + 4 = 16, bukan 15.", "Salah melanjutkan pola pertambahan 4")
mc("c3", "sedang", R, Pr, S3, "Hitunglah lompatan mundur melewati puluhan: 42 - 5 = ....", ["37", "38", "36", "35"], "A", "42 - 5 = 37.", "Keliru mundur menyeberang puluhan", verifikasi={"ekspresi": "42 - 5", "hasil": "37"})

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Lanjutan yang benar dari pola bertambah 6: 18, 24, ... adalah ....", ["30", "28", "32", "29"], "A", "24 + 6 = 30.", verifikasi={"ekspresi": "24 + 6", "hasil": "30"})
mc("c3", "mudah", T, Pr, S3, "Berapakah hasil dari 57 + 6?", ["63", "62", "64", "61"], "A", "57 + 6 = 63.", verifikasi={"ekspresi": "57 + 6", "hasil": "63"})
tf("c3", "sedang", T, Pr, S2, "Pada pola 24, 20, 16, jika langkah berikutnya 20 itu keliru.", "Benar", "Seharusnya 16 - 4 = 12, bukan kembali 20.")
mc("c3", "sedang", T, Pr, S4, "Periksa pola: 7, 14, 21, 27. Manakah angka yang salah?", ["27", "21", "14", "7"], "A", "21 + 7 = 28, jadi 27 salah.")
tf("c3", "sedang", T, Pr, S1, "Urutan 1, 3, 6, 10 adalah pola dengan aturan penambahan tetap.", "Salah", "Tambahannya 2, 3, 4 (berubah-ubah), bukan penambahan tetap.")
sa("c3", "sedang", T, Pr, S3, "Berapakah hasil dari 68 + 7?", "75", "68 + 7 = 75.", verifikasi={"ekspresi": "68 + 7", "hasil": "75"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Pola: 3, 7, 11, 14. Angka 14 keliru, seharusnya ....", ["15", "16", "13", "17"], "A", "11 + 4 = 15.", verifikasi={"ekspresi": "11 + 4", "hasil": "15"})
mc("c3", "sedang", X, Pr, S2, "Pola turun: 70, 62, 54, ... Angka berikutnya adalah ....", ["46", "48", "44", "45"], "A", "54 - 8 = 46.", verifikasi={"ekspresi": "54 - 8", "hasil": "46"})
tf("c3", "sedang", X, Pr, S3, "Hasil dari 39 + 4 adalah 42.", "Salah", "39 + 4 = 43, bukan 42.")
sa("c3", "sedang", X, Pr, S4, "Berapakah selisih yang benar dari pola 80, 72, 64?", "8", "80 - 72 = 8.", verifikasi={"ekspresi": "80 - 72", "hasil": "8"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Pola: 45, 36, 27, ... Angka berikutnya adalah ....", ["18", "19", "17", "20"], "A", "27 - 9 = 18.", verifikasi={"ekspresi": "27 - 9", "hasil": "18"})
mc("c3", "sedang", K, Pr, S3, "Berapakah hasil dari 85 - 7?", ["78", "77", "79", "76"], "A", "85 - 7 = 78.", verifikasi={"ekspresi": "85 - 7", "hasil": "78"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa pola 10, 15, 21, 26 salah?", ["karena dari 15 ke 21 bertambah 6 bukan 5", "karena bilangannya ganjil", "karena dimulai dari 10", "karena terlalu panjang"], "A", "Selisihnya tidak konsisten: +5, +6, +5.")
mc("c4", "sedang", T, Kn, S2, "Ali menulis pola: 50, 40, 30, 40. Kesalahan apa yang dilakukan Ali?", ["Ali menjumlahkan pada langkah terakhir padahal pola turun", "Ali salah tulis angka 50", "Ali tidak menulis angka nol", "Ali melompati angka 20"], "A", "Ali tertukar operasi dari pengurangan menjadi penjumlahan.")
tf("c4", "sedang", T, Kn, S3, "Lompatan mundur 6 dari 53 menghasilkan angka 47.", "Benar", "53 - 6 = 47.")
tf("c4", "sedang", T, Kn, S4, "Jika dua suku pertama selisih 5, maka pola otomatis pasti benar.", "Salah", "Kita harus memeriksa seluruh suku sampai akhir.")
sa("c4", "sedang", T, Kn, S3, "Berapakah hasil dari 74 dikurang 9?", "65", "74 - 9 = 65.", verifikasi={"ekspresi": "74 - 9", "hasil": "65"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Pola: 6, 12, 18, 25, 30. Angka berapakah yang merusak pola?", ["25", "18", "30", "12"], "A", "18 + 6 = 24, bukan 25.")
mc("c4", "sedang", X, Kn, S3, "Berapakah hasil dari 62 dikurang 8?", ["54", "52", "56", "53"], "A", "62 - 8 = 54.", verifikasi={"ekspresi": "62 - 8", "hasil": "54"})
tf("c4", "sedang", X, Kn, S2, "Pola yang membesar nilainya selalu menggunakan tanda kurang.", "Salah", "Pola membesar menggunakan tanda tambah.")
mc("c4", "sulit", X, Me, S4, "Dalam pola 16, 23, 30, 38, suku ke-4 harus diperbaiki menjadi ....", ["37", "36", "39", "35"], "A", "Beda = 7. 30 + 7 = 37, bukan 38.", verifikasi={"ekspresi": "30 + 7", "hasil": "37"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Seseorang menulis 5, 9, 13, 18, 21. Manakah bilangan yang tidak sesuai aturan?", ["18", "13", "9", "21"], "A", "13 + 4 = 17, bukan 18.")
mc("c4", "sulit", K, Me, S2, "Pola mundur: 82, 75, 68, ... Suku ke-5 dari pola ini adalah ....", ["54", "61", "47", "50"], "A", "Beda = 7. Suku ke-4 = 61, suku ke-5 = 61 - 7 = 54.", verifikasi={"ekspresi": "82 - (4 * 7)", "hasil": "54"})
tf("c4", "sulit", K, Me, S3, "Penjumlahan 77 + 8 menghasilkan 85, bukan 84.", "Benar", "77 + 8 = 85.")
mc("c4", "sulit", K, Me, S4, "Pola: 4, 11, 18, X, 32. Jika X salah bernilai 26, nilai yang BENAR adalah ....", ["25", "24", "27", "28"], "A", "18 + 7 = 25.", verifikasi={"ekspresi": "18 + 7", "hasil": "25"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Pola: 12, 19, 26, 33. Berapakah suku ke-6 dari pola ini?", ["47", "40", "54", "45"], "A", "12 + (5 x 7) = 12 + 35 = 47.", verifikasi={"ekspresi": "12 + (5 * 7)", "hasil": "47"})
mc("c5", "sedang", T, Me, S2, "Pola mundur: 94, 85, 76, ... Berapakah suku ke-6 dari pola ini?", ["49", "58", "40", "52"], "A", "94 - (5 x 9) = 94 - 45 = 49.", verifikasi={"ekspresi": "94 - (5 * 9)", "hasil": "49"})
mc("c5", "sedang", T, Me, S3, "Berapakah hasil dari (38 + 7) + (52 - 6)?", ["91", "89", "93", "88"], "A", "45 + 46 = 91.", verifikasi={"ekspresi": "(38 + 7) + (52 - 6)", "hasil": "91"})
mc("c5", "sulit", T, Me, S4, "Pola: 20, 27, 34, 42. Agar pola ini benar, suku terakhir harus diganti angka ....", ["41", "40", "43", "39"], "A", "Beda = 7. 34 + 7 = 41.", verifikasi={"ekspresi": "34 + 7", "hasil": "41"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Berapakah selisih antara suku ke-5 dan ke-1 pada pola 5, 13, 21, 29?", ["32", "24", "40", "28"], "A", "Beda = 8. Selisih = 4 x 8 = 32.", verifikasi={"ekspresi": "4 * 8", "hasil": "32"})
mc("c5", "sulit", K, Me, S4, "Hitunglah hasil dari (3 + 28) ditambah (60 - 24)!", ["67", "65", "69", "63"], "A", "Pola 1 ke-5 = 3 + 28 = 31. Pola 2 ke-4 = 60 - 24 = 36. 31 + 36 = 67.", verifikasi={"ekspresi": "(3 + 28) + (60 - 24)", "hasil": "67"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Mengapa sangat penting memeriksa kesamaan selisih pada setiap pasangan bilangan?", ["untuk memastikan pola tidak rusak dan aturannya benar", "agar terlihat pintar", "karena disuruh teman", "tidak penting sama sekali"], "A", "Pola yang valid wajib memiliki selisih seragam dari awal sampai akhir.")
mc("c6", "sulit", K, Me, S4, "Dua pola berawal di 10. Pola A bertambah 4, B bertambah 7. Selisih suku ke-5?", ["12", "15", "10", "14"], "A", "Pola A ke-5 = 10 + 16 = 26. Pola B ke-5 = 10 + 28 = 38. 38 - 26 = 12.", verifikasi={"ekspresi": "(10 + 28) - (10 + 16)", "hasil": "12"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil dari (10 + 50) dikurang (70 - 20)!", ["10", "15", "5", "20"], "A", "Pola 1 ke-6 = 60. Pola 2 ke-5 = 50. 60 - 50 = 10.", verifikasi={"ekspresi": "(10 + 50) - (70 - 20)", "hasil": "10"})
mc("c6", "sulit", P, Me, S3, "Sebuah jam terlambat 3 menit setiap jam. Setelah 6 jam, berapa total keterlambatannya?", ["18 menit", "15 menit", "21 menit", "12 menit"], "A", "6 x 3 = 18 menit.", verifikasi={"ekspresi": "6 * 3", "hasil": "18"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab60_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab60.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
