#!/usr/bin/env python3
"""
Generator dan validator Bab 58 Matematika Kelas 2 SD:
"Melanjutkan Pola Bilangan Naik dan Turun" (Fase A)
bab_id: df5ad5ea-9459-4c38-8946-77c42694304a
article_id: ab94f9bc-40e1-4a85-ada4-4068855fec78
quiz_id: 6ba70c0a-8077-46d3-a49b-f4223de647b3
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "c1e2g3i4k501"  # Mengenal Aturan Pola Bilangan
S2 = "d2f3h4j5l602"  # Melanjutkan Pola Bilangan Naik
S3 = "e3g4i5k6m703"  # Melanjutkan Pola Bilangan Turun
S4 = "f4h5j6l7n804"  # Menemukan Angka yang Hilang di Tengah Pola

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Pernahkah kamu melihat ubin warna-warni?
Ubin tersusun dengan rapi.
Angka juga bisa bersusun rapi.
Susunan itu disebut pola bilangan.
Setiap pola punya aturan khusus.
Aturan dicari dari selisihnya.
Bandingkan dua angka yang berdampingan.
Selisih itulah rahasia polanya!

:::definition
title: Aturan Pola Bilangan
Aturan pola bilangan adalah penambahan atau pengurangan bilangan tetap pada setiap langkah.
:::"""

s2_content = """Sekarang perhatikan pola bilangan naik.
Pada pola naik, angka membesar.
Operasi yang dipakai adalah penjumlahan.
Contoh: 3, 6, 9, 12.
Setiap langkah ditambah tiga (+3).
Contoh lain: 4, 8, 12, 16.
Setiap langkah ditambah empat (+4).
Tambahkan bilangan secara teratur!

:::steps
title: Cara Melanjutkan Pola Naik
1. Hitung selisih dua angka pertama.
2. Pastikan selisih berikutnya sama.
3. Tambahkan selisih ke angka terakhir.
:::"""

s3_content = """Bagaimana dengan pola bilangan turun?
Pada pola turun, angka mengecil.
Operasi yang dipakai adalah pengurangan.
Contoh: 30, 26, 22, 18.
Setiap langkah dikurang empat (-4).
Contoh lain: 25, 22, 19, 16.
Setiap langkah dikurang tiga (-3).
Kurangkan bilangan dengan teliti!"""

s4_content = """Kadang ada angka yang hilang.
Angka itu berada di tengah.
Bagaimana cara menemukannya?
Cari dulu aturan polanya.
Gunakan selisih angka yang lengkap.
Gunakan aturan untuk mengisi titik-titik.
Cek kembali agar urutan pas!

:::common_trap
title: Salah Menentukan Arah Naik atau Turun
Periksa apakah angka membesar atau mengecil.
Membesar berarti pola naik (tambah).
Mengecil berarti pola turun (kurang).
Jangan terbalik menggunakan operasinya!
:::

:::callout
variant: summary
title: Ringkasan
text: Pola naik memakai aturan tambah. Pola turun memakai aturan kurang. Selisih selalu teratur.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Aturan Pola Bilangan",
        "minutes": 6,
        "goal": "Siswa memahami konsep pola bilangan dan cara menemukan aturannya dari selisih bilangan.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Melanjutkan Pola Bilangan Naik",
        "minutes": 6,
        "goal": "Siswa mampu menentukan aturan dan melanjutkan pola bilangan naik hingga 100.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Melanjutkan Pola Bilangan Turun",
        "minutes": 6,
        "goal": "Siswa mampu menentukan aturan dan melanjutkan pola bilangan turun secara tepat.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menemukan Angka yang Hilang di Tengah Pola",
        "minutes": 6,
        "goal": "Siswa mampu mencari nilai bilangan yang belum diketahui pada pola naik atau turun.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Melanjutkan Pola Bilangan Naik dan Turun",
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
# 2. DEFINISI BANK 50 SOAL BAB 58
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
mc("c1", "mudah", D, F, S1, "Susunan angka yang berulang secara teratur disebut ....", ["pola bilangan", "kumpulan huruf", "garis lurus", "daftar nama"], "A", "Pola bilangan adalah susunan angka yang teratur menurut aturan tertentu.")
tf("c1", "mudah", D, F, S2, "Pada pola bilangan naik, nilai angka semakin bertambah besar.", "Benar", "Pola naik bertambah besar.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Lanjutan dari pola bilangan 3, 6, 9 adalah ....", ["12", "11", "10", "15"], "A", "9 + 3 = 12.", verifikasi={"ekspresi": "9 + 3", "hasil": "12"})
mc("c1", "mudah", T, F, S3, "Lanjutan dari pola bilangan 20, 18, 16 adalah ....", ["14", "15", "12", "13"], "A", "16 - 2 = 14.", verifikasi={"ekspresi": "16 - 2", "hasil": "14"})
sa("c1", "mudah", T, F, S1, "Berapakah aturan penambahan pada pola 5, 8, 11?", "3", "8 - 5 = 3.", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Untuk mencari angka yang hilang, langkah pertama adalah ....", ["mencari aturan selisihnya", "menebak sembarang angka", "menjumlahkan semua angka", "mengurangi angka terbesar"], "A", "Aturan selisih menjadi kunci membuka seluruh pola.")
tf("c2", "mudah", D, Kn, S3, "Pola bilangan 50, 45, 40 adalah pola bilangan naik.", "Salah", "Pola tersebut berkurang 5, jadi merupakan pola bilangan turun.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Lanjutan dari 4, 8, 12 adalah ....", ["16", "14", "15", "18"], "A", "12 + 4 = 16.", "Keliru menghitung loncatan 4", verifikasi={"ekspresi": "12 + 4", "hasil": "16"})
mc("c2", "mudah", R, Kn, S3, "Lanjutan dari 25, 21, 17 adalah ....", ["13", "14", "12", "15"], "A", "17 - 4 = 13.", "Keliru pengurangan pada pola turun", verifikasi={"ekspresi": "17 - 4", "hasil": "13"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Berapakah beda selisih pada pola 7, 11, 15, 19?", ["4", "3", "5", "2"], "A", "11 - 7 = 4.", verifikasi={"ekspresi": "11 - 7", "hasil": "4"})
mc("c2", "mudah", T, Kn, S3, "Pola: 30, 27, 24, 21. Aturan pola tersebut adalah ....", ["berkurang 3", "bertambah 3", "berkurang 4", "bertambah 4"], "A", "30 - 27 = 3, pola berkurang 3.")
tf("c2", "mudah", T, Kn, S4, "Angka yang hilang pada pola 2, 4, ..., 8 adalah 6.", "Benar", "2 + 2 = 4, 4 + 2 = 6, 6 + 2 = 8.")
sa("c2", "mudah", T, Kn, S2, "Berapakah angka setelah 16 pada pola tambah 4?", "20", "16 + 4 = 20.", verifikasi={"ekspresi": "16 + 4", "hasil": "20"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S4, "Lengkapi angka yang hilang: 10, 14, ..., 22!", ["18", "16", "17", "20"], "A", "14 + 4 = 18.", "Salah menentukan angka tengah pola", verifikasi={"ekspresi": "14 + 4", "hasil": "18"})
mc("c3", "sedang", R, Pr, S3, "Lengkapi pola turun: 40, 35, 30, ...!", ["25", "20", "28", "24"], "A", "30 - 5 = 25.", "Keliru melanjutkan pola turun", verifikasi={"ekspresi": "30 - 5", "hasil": "25"})

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Aturan dari pola bilangan 6, 12, 18, 24 adalah ....", ["bertambah 6", "bertambah 5", "berkurang 6", "bertambah 4"], "A", "12 - 6 = 6, bertambah 6.")
mc("c3", "mudah", T, Pr, S2, "Lanjutan dari pola bilangan 15, 18, 21 adalah ....", ["24", "23", "25", "22"], "A", "21 + 3 = 24.", verifikasi={"ekspresi": "21 + 3", "hasil": "24"})
tf("c3", "sedang", T, Pr, S4, "Pada pola 5, 10, ..., 20, angka yang hilang adalah 12.", "Salah", "10 + 5 = 15, bukan 12.")
mc("c3", "sedang", T, Pr, S3, "Lanjutan dari pola bilangan 50, 44, 38 adalah ....", ["32", "30", "34", "31"], "A", "38 - 6 = 32.", verifikasi={"ekspresi": "38 - 6", "hasil": "32"})
tf("c3", "sedang", T, Pr, S2, "Pola bilangan 7, 14, 21, 28 memiliki aturan bertambah 7.", "Benar", "Setiap langkah bertambah 7.")
sa("c3", "sedang", T, Pr, S4, "Isilah titik-titik pada pola: 8, 12, 16, ...!", "20", "16 + 4 = 20.", verifikasi={"ekspresi": "16 + 4", "hasil": "20"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Berapakah beda dari pola 13, 20, 27, 34?", ["7", "6", "8", "5"], "A", "20 - 13 = 7.", verifikasi={"ekspresi": "20 - 13", "hasil": "7"})
mc("c3", "sedang", X, Pr, S2, "Lanjutan dari 21, 25, 29 adalah ....", ["33", "32", "34", "31"], "A", "29 + 4 = 33.", verifikasi={"ekspresi": "29 + 4", "hasil": "33"})
tf("c3", "sedang", X, Pr, S3, "Pola 60, 52, 44 memiliki aturan berkurang 8.", "Benar", "60 - 52 = 8, berkurang 8.")
sa("c3", "sedang", X, Pr, S4, "Isilah titik-titik pada pola: 45, 40, ..., 30!", "35", "40 - 5 = 35.", verifikasi={"ekspresi": "40 - 5", "hasil": "35"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Lanjutan dari pola 70, 63, 56 adalah ....", ["49", "48", "50", "47"], "A", "56 - 7 = 49.", verifikasi={"ekspresi": "56 - 7", "hasil": "49"})
mc("c3", "sedang", K, Pr, S4, "Lengkapi pola: 12, ..., 20, 24!", ["16", "14", "18", "15"], "A", "12 + 4 = 16.", verifikasi={"ekspresi": "12 + 4", "hasil": "16"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Manakah dari susunan berikut yang BUKAN merupakan pola teratur?", ["3, 6, 10, 12", "2, 4, 6, 8", "5, 10, 15, 20", "10, 20, 30, 40"], "A", "3 ke 6 (+3), 6 ke 10 (+4), 10 ke 12 (+2), selisih tidak sama.")
mc("c4", "sedang", T, Kn, S2, "Pola: 6, 11, 16, 21. Apakah angka ke-6 pada pola ini?", ["31", "26", "36", "30"], "A", "Angka ke-5 = 26, angka ke-6 = 31.", verifikasi={"ekspresi": "6 + (5 * 5)", "hasil": "31"})
tf("c4", "sedang", T, Kn, S3, "Pada pola turun 85, 75, 65, angka berikutnya adalah 50.", "Salah", "65 - 10 = 55, bukan 50.")
tf("c4", "sedang", T, Kn, S4, "Jika dua angka pertama bertambah 4, angka ketiga pasti bertambah 4.", "Benar", "Aturan pola berlaku tetap untuk seluruh langkah.")
sa("c4", "sedang", T, Kn, S4, "Tentukan angka yang hilang: 50, ..., 38, 32!", "44", "Selisih = 38 - 32 = 6; 50 - 6 = 44.", verifikasi={"ekspresi": "50 - 6", "hasil": "44"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Berapakah selisih antara suku ke-4 dan suku ke-1 pada pola 3, 7, 11, 15?", ["12", "10", "14", "8"], "A", "15 - 3 = 12.", verifikasi={"ekspresi": "15 - 3", "hasil": "12"})
mc("c4", "sedang", X, Kn, S3, "Pola: 90, 82, 74, ... Berapakah angka ke-4?", ["66", "68", "64", "70"], "A", "74 - 8 = 66.", verifikasi={"ekspresi": "74 - 8", "hasil": "66"})
tf("c4", "sedang", X, Kn, S2, "Pola bilangan 2, 5, 8, 11 memiliki aturan bertambah 4.", "Salah", "5 - 2 = 3, bertambah 3 bukan 4.")
mc("c4", "sulit", X, Me, S4, "Pola: 15, 23, 31, 39. Berapakah angka ke-6 pola tersebut?", ["55", "47", "53", "57"], "A", "Beda = 8. Ke-5 = 47, ke-6 = 47 + 8 = 55.", verifikasi={"ekspresi": "15 + (5 * 8)", "hasil": "55"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Jika pola dimulai dari 10 bertambah 6, angka ke-4 adalah ....", ["28", "22", "34", "26"], "A", "10, 16, 22, 28 (angka ke-4 adalah 28).", verifikasi={"ekspresi": "10 + (3 * 6)", "hasil": "28"})
mc("c4", "sulit", K, Me, S2, "Pola: 8, 17, 26, 35. Berapakah jumlah suku ke-4 dan ke-5?", ["79", "70", "81", "75"], "A", "Ke-4 = 35; ke-5 = 44; 35 + 44 = 79.", verifikasi={"ekspresi": "35 + (35 + 9)", "hasil": "79"})
tf("c4", "sulit", K, Me, S4, "Pola yang melompat mundur selalu berhenti pada bilangan negatif.", "Salah", "Pola dapat berhenti pada nol atau bilangan cacah lainnya.")
mc("c4", "sulit", K, Me, S3, "Pola turun mulai dari 100 berkurang 12. Angka ke-4 adalah ....", ["64", "76", "52", "68"], "A", "100 - (3 x 12) = 100 - 36 = 64.", verifikasi={"ekspresi": "100 - (3 * 12)", "hasil": "64"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Pola A (2, 5, 8) dan Pola B (1, 5, 9). Manakah selisih lebih besar?", ["pola B karena selisihnya 4", "pola A karena selisihnya 3", "sama besar", "tidak dapat dihitung"], "A", "Pola A beda 3, Pola B beda 4. Beda B lebih besar.")
mc("c5", "sedang", T, Me, S2, "Pola: 4, 10, 16, 22. Berapakah suku ke-8 dari pola tersebut?", ["46", "40", "52", "48"], "A", "4 + (7 x 6) = 4 + 42 = 46.", verifikasi={"ekspresi": "4 + (7 * 6)", "hasil": "46"})
mc("c5", "sedang", T, Me, S3, "Pola turun: 80, 71, 62, 53. Angka ke-7 dari pola ini adalah ....", ["26", "35", "17", "28"], "A", "80 - (6 x 9) = 80 - 54 = 26.", verifikasi={"ekspresi": "80 - (6 * 9)", "hasil": "26"})
mc("c5", "sulit", T, Me, S4, "Lengkapi pola ganda: 10, A, 20, 25, B. Berapakah A + B?", ["45", "40", "50", "35"], "A", "A = 15, B = 30. A + B = 15 + 30 = 45.", verifikasi={"ekspresi": "15 + 30", "hasil": "45"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Pola bertambah 7 dimulai dari 5. Angka berapakah yang bernilai 47?", ["angka ke-7", "angka ke-6", "angka ke-8", "angka ke-5"], "A", "(47 - 5) : 7 + 1 = 42 : 7 + 1 = 6 + 1 = 7.")
mc("c5", "sulit", K, Me, S4, "Pola turun: 95, 87, 79, ... Berapakah selisih antara suku ke-1 dan ke-6?", ["40", "35", "45", "32"], "A", "Beda = 8. Suku ke-6 = 95 - 40 = 55. Selisih = 95 - 55 = 40.", verifikasi={"ekspresi": "5 * 8", "hasil": "40"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Bagaimana cara menyusun pola bilangan naik dengan aturan bertambah 8 dari 3?", ["mulai dari 3 lalu terus menambahkan 8 pada setiap langkah", "tambahkan 3 pada angka 8", "kalikan 3 dengan 8", "buat urutan acak"], "A", "Mulai dari bilangan awal 3, lalu tambah 8 berulang-ulang.")
mc("c6", "sulit", K, Me, S4, "Ada pola: 5, 11, 17, 23, 29. Buatlah pola baru dengan aturan dikurang 6!", ["29, 23, 17, 11, 5", "30, 24, 18, 12", "5, 11, 17, 23", "29, 20, 15, 10"], "A", "Membalik urutan menghasilkan pola turun dengan aturan berkurang 6.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil dari (4 + 20) ditambah (50 - 24)!", ["50", "48", "52", "46"], "A", "Pola 1 ke-5 = 4 + 20 = 24. Pola 2 ke-4 = 50 - 24 = 26. 24 + 26 = 50.", verifikasi={"ekspresi": "(4 + 20) + (50 - 24)", "hasil": "50"})
mc("c6", "sulit", P, Me, S3, "Sebuah lampu menyala di detik 4, 11, 18, 25. Di detik ke berapa nyala ke-8?", ["53", "46", "60", "50"], "A", "Nyala ke-8 = 4 + (7 x 7) = 4 + 49 = 53 detik.", verifikasi={"ekspresi": "4 + (7 * 7)", "hasil": "53"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab58_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab58.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
