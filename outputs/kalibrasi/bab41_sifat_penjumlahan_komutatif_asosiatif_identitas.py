#!/usr/bin/env python3
"""
Generator dan validator Bab 41 Matematika Kelas 2 SD:
"Sifat Penjumlahan: Komutatif, Asosiatif, dan Unsur Identitas" (Fase A)
bab_id: 22efddab-1027-40ff-9c21-e7335103e867
article_id: 1821f52c-d52e-49d4-abed-f7479d94d478
quiz_id: 467a9cab-63b4-4a67-bdfa-14a9a433ec6e
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "f3a4b5c6d701"  # Sifat Komutatif (Pertukaran)
S2 = "a4b5c6d7e802"  # Sifat Asosiatif (Pengelompokan)
S3 = "b5c6d7e8f903"  # Unsur Identitas (Angka Nol)
S4 = "c6d7e8f9a004"  # Berhitung Cepat dengan Sifat Penjumlahan

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Penjumlahan memiliki sifat sangat istimewa.
Urutan bilangan boleh dibolak-balik.
Lima belas ditambah dua puluh.
Sama dengan dua puluh tambah lima belas.
Keduanya menghasilkan tiga puluh lima.
Sifat ini disebut sifat pertukaran.
Dalam matematika disebut komutatif.
Hasil jumlahnya akan selalu sama.

:::definition
title: Sifat Komutatif
Sifat komutatif adalah pertukaran urutan bilangan tanpa mengubah hasil penjumlahan.
:::"""

s2_content = """Bagaimana jika ada tiga bilangan?
Kita bisa menjumlahkan dua bilangan dulu.
Gunakan tanda kurung untuk mengelompokkan.
Misalnya dua belas tambah delapan tambah lima.
Dua belas tambah delapan jadi dua puluh.
Dua puluh tambah lima jadi dua puluh lima.
Sifat ini disebut sifat pengelompokan.
Nama lainnya adalah sifat asosiatif.

:::steps
title: Mengelompokkan Penjumlahan
1. Pilih dua bilangan yang mudah dijumlahkan.
2. Beri tanda kurung dan hitung dahulu.
3. Jumlahkan hasilnya dengan bilangan ketiga.
:::"""

s3_content = """Angka nol adalah angka yang unik.
Setiap bilangan ditambah nol tidak berubah.
Tiga puluh lima ditambah nol tetap sama.
Hasilnya tetap tiga puluh lima.
Nol disebut unsur identitas penjumlahan.
Benda tidak bertambah jika ditambah nol.
Sangat mudah diingat di kepala!"""

s4_content = """Sifat penjumlahan membuat kita berhitung cepat.
Cari pasangan bilangan yang menghasilkan puluhan.
Misalnya tujuh belas tambah tiga belas.
Tujuh belas tambah tiga belas menghasilkan tiga puluh.
Lalu tambahkan dengan bilangan lainnya.
Hitungan rumit menjadi sangat mudah.

:::common_trap
title: Mengira Sifat Berlaku pada Pengurangan
Sifat pertukaran hanya berlaku pada penjumlahan.
Tujuh kurang dua tidak sama dengan dua kurang tujuh.
Jangan gunakan sifat pertukaran pada pengurangan!
:::

:::callout
variant: summary
title: Ringkasan
text: Urutan penjumlahan boleh dibalik. Tiga bilangan boleh dikelompokkan. Menambah nol hasilnya tidak berubah.
:::"""

sections = [
    {
        "id": S1,
        "title": "Sifat Komutatif (Pertukaran)",
        "minutes": 6,
        "goal": "Siswa memahami bahwa membalik urutan dua bilangan yang dijumlahkan tidak mengubah hasil akhir.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Sifat Asosiatif (Pengelompokan)",
        "minutes": 6,
        "goal": "Siswa mampu mengelompokkan tiga bilangan penjumlahan menggunakan tanda kurung untuk mempermudah perhitungan.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Unsur Identitas (Angka Nol)",
        "minutes": 6,
        "goal": "Siswa memahami bahwa menjumlahkan bilangan berapapun dengan nol menghasilkan bilangan itu sendiri.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Berhitung Cepat dengan Sifat Penjumlahan",
        "minutes": 6,
        "goal": "Siswa mampu memanfaatkan sifat komutatif dan asosiatif untuk memasangkan bilangan menjadi puluhan utuh.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Sifat Penjumlahan: Komutatif, Asosiatif, dan Unsur Identitas",
    "topic": "Penjumlahan dan Pengurangan sampai 100",
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
# 2. DEFINISI BANK 50 SOAL BAB 41
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
mc("c1", "mudah", D, F, S1, "Sifat pertukaran pada penjumlahan disebut juga sifat ....", ["komutatif", "asosiatif", "distributif", "identitas"], "A", "Sifat pertukaran urutan bilangan disebut komutatif.")
tf("c1", "mudah", D, F, S3, "Sebuah bilangan jika ditambah nol nilainya akan berubah.", "Salah", "Bilangan ditambah nol hasilnya tetap sama, tidak berubah.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S3, "Berapakah hasil dari 47 ditambah 0?", ["47", "0", "48", "40"], "A", "47 + 0 = 47.", verifikasi={"ekspresi": "47 + 0", "hasil": "47"})
mc("c1", "mudah", T, F, S2, "Sifat pengelompokan pada penjumlahan disebut sifat ....", ["asosiatif", "komutatif", "identitas", "kurang"], "A", "Pengelompokan bilangan menggunakan kurung disebut asosiatif.")
sa("c1", "mudah", T, F, S1, "Jika 15 + 20 = 35, berapakah 20 + 15?", "35", "Sifat komutatif menjamin 20 + 15 = 35.", verifikasi={"ekspresi": "20 + 15", "hasil": "35"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Bentuk pertukaran dari 24 + 13 adalah ....", ["13 + 24", "24 - 13", "13 - 24", "24 + 24"], "A", "Pertukaran komutatif membalik posisi bilangan menjadi 13 + 24.", "Keliru memahami bentuk sifat pertukaran")
tf("c2", "mudah", D, Kn, S4, "Menjumlahkan 18 + 12 menghasilkan puluhan utuh 30.", "Benar", "18 + 12 = 30.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Mengapa 16 + 25 hasilnya sama dengan 25 + 16?", ["karena penjumlahan memiliki sifat pertukaran komutatif", "karena angkanya genap", "karena ditambah nol", "karena dikurang"], "A", "Sifat komutatif memastikan hasil penjumlahan tidak berubah saat posisi dibalik.", "Belum memahami makna sifat komutatif")
mc("c2", "mudah", R, Kn, S3, "Berapakah hasil dari 0 ditambah 68?", ["68", "0", "69", "60"], "A", "0 + 68 = 68.", "Mengira angka nol menghilangkan bilangan", verifikasi={"ekspresi": "0 + 68", "hasil": "68"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S2, "Bentuk (14 + 16) + 7 sama nilainya dengan ....", ["14 + (16 + 7)", "(14 + 7) - 16", "14 - 16 + 7", "16 + 7 - 14"], "A", "Sifat asosiatif memindahkan tanda kurung pengelompokan.")
mc("c2", "mudah", T, Kn, S3, "Angka berapakah yang menjadi unsur identitas penjumlahan?", ["0", "1", "2", "10"], "A", "Angka 0 adalah unsur identitas karena tidak mengubah nilai bilangan.")
tf("c2", "mudah", T, Kn, S1, "Sifat pertukaran juga berlaku sama persis pada operasi pengurangan.", "Salah", "Sifat komutatif hanya berlaku pada penjumlahan, bukan pengurangan.")
sa("c2", "mudah", T, Kn, S4, "Berapakah hasil dari 25 ditambah 15?", "40", "25 + 15 = 40.", verifikasi={"ekspresi": "25 + 15", "hasil": "40"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Berapakah hasil dari (23 + 17) + 15?", ["55", "45", "56", "54"], "A", "23 + 17 = 40; 40 + 15 = 55.", "Keliru menjumlahkan dalam kurung lebih dulu", verifikasi={"ekspresi": "(23 + 17) + 15", "hasil": "55"})
mc("c3", "sedang", R, Pr, S4, "Hitung cepat 19 + 25 + 1 dengan memasangkan bilangan!", ["45", "35", "46", "44"], "A", "Pasangkan 19 + 1 = 20; 20 + 25 = 45.", "Tidak melihat pasangan angka yang mudah dijumlahkan", verifikasi={"ekspresi": "19 + 25 + 1", "hasil": "45"})

# Terarah (6): S1, S2, S3, S4, S2, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Jika 32 + 45 = 77, berapakah hasil dari 45 + 32?", ["77", "76", "78", "75"], "A", "Dengan komutatif, 45 + 32 = 77.", verifikasi={"ekspresi": "45 + 32", "hasil": "77"})
mc("c3", "mudah", T, Pr, S3, "Berapakah hasil dari 85 + 0 + 5?", ["90", "85", "95", "80"], "A", "85 + 0 = 85; 85 + 5 = 90.", verifikasi={"ekspresi": "85 + 0 + 5", "hasil": "90"})
tf("c3", "sedang", T, Pr, S2, "Hasil dari (15 + 25) + 30 sama dengan 70.", "Benar", "40 + 30 = 70.")
mc("c3", "sedang", T, Pr, S4, "Berapakah hasil dari 28 + 14 + 12?", ["54", "44", "55", "53"], "A", "28 + 12 = 40; 40 + 14 = 54.", verifikasi={"ekspresi": "28 + 14 + 12", "hasil": "54"})
tf("c3", "sedang", T, Pr, S1, "Persamaan 50 + 23 = 23 + 50 menunjukkan sifat asosiatif.", "Salah", "Itu menunjukkan sifat komutatif (pertukaran).")
sa("c3", "sedang", T, Pr, S2, "Berapakah hasil dari 16 + (14 + 25)?", "55", "16 + 14 = 30; 30 + 25 = 55.", verifikasi={"ekspresi": "16 + (14 + 25)", "hasil": "55"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Berapakah hasil dari 38 + 29 jika dihitung sebagai 29 + 38?", ["67", "57", "68", "66"], "A", "29 + 38 = 67.", verifikasi={"ekspresi": "29 + 38", "hasil": "67"})
mc("c3", "sedang", X, Pr, S2, "Berapakah nilai dari (31 + 19) + 24?", ["74", "64", "75", "73"], "A", "31 + 19 = 50; 50 + 24 = 74.", verifikasi={"ekspresi": "(31 + 19) + 24", "hasil": "74"})
tf("c3", "sedang", X, Pr, S3, "Nilai dari 0 + 73 sama dengan 73 + 0.", "Benar", "Keduanya bernilai 73.")
sa("c3", "sedang", X, Pr, S4, "Berapakah hasil cepat dari 36 + 18 + 14?", "68", "36 + 14 = 50; 50 + 18 = 68.", verifikasi={"ekspresi": "36 + 18 + 14", "hasil": "68"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Berapakah hasil dari 25 + (25 + 32)?", ["82", "72", "83", "81"], "A", "25 + 25 = 50; 50 + 32 = 82.", verifikasi={"ekspresi": "25 + (25 + 32)", "hasil": "82"})
mc("c3", "sedang", K, Pr, S4, "Berapakah hasil penjumlahan 27 + 35 + 13?", ["75", "65", "76", "74"], "A", "27 + 13 = 40; 40 + 35 = 75.", verifikasi={"ekspresi": "27 + 35 + 13", "hasil": "75"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Jika 48 + A = 19 + 48, berapakah bilangan pengganti A?", ["19", "48", "29", "0"], "A", "Menurut sifat komutatif, nilai A adalah 19.", verifikasi={"ekspresi": "19", "hasil": "19"})
mc("c4", "sedang", T, Kn, S2, "Jika (26 + 14) + B = 26 + (14 + 35), berapakah nilai B?", ["35", "14", "26", "50"], "A", "Menurut sifat asosiatif, nilai B adalah 35.", verifikasi={"ekspresi": "35", "hasil": "35"})
tf("c4", "sedang", T, Kn, S3, "Menjumlahkan 92 + 0 memberikan hasil yang sama dengan 92 dikurang 0.", "Benar", "92 + 0 = 92 dan 92 - 0 = 92.")
tf("c4", "sedang", T, Kn, S4, "Pasangan terbaik untuk 43 agar jadi puluhan utuh adalah 15.", "Salah", "Pasangan 43 adalah yang berakhiran 7 (misal 17), bukan 15.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil cepat dari 42 + 29 + 18?", "89", "42 + 18 = 60; 60 + 29 = 89.", verifikasi={"ekspresi": "42 + 29 + 18", "hasil": "89"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Manakah pernyataan di bawah ini yang benar?", ["56 + 27 = 27 + 56", "56 - 27 = 27 - 56", "56 + 0 = 0", "56 + 27 = 56"], "A", "Sifat komutatif hanya benar untuk penjumlahan.")
mc("c4", "sedang", X, Kn, S4, "Budi punya kelereng 24, 38, dan 16. Berapa seluruh kelereng Budi?", ["78 kelereng", "68 kelereng", "79 kelereng", "77 kelereng"], "A", "24 + 16 = 40; 40 + 38 = 78 kelereng.", verifikasi={"ekspresi": "24 + 38 + 16", "hasil": "78"})
tf("c4", "sedang", X, Kn, S2, "Nilai dari (20 + 30) + 40 sama dengan 20 + (30 + 40).", "Benar", "Keduanya bernilai 90 karena berlakunya sifat asosiatif.")
mc("c4", "sulit", X, Me, S4, "Hitung cepat 37 + 19 + 23 + 11 dengan memasangkan bilangan!", ["90", "80", "100", "85"], "A", "(37 + 23) + (19 + 11) = 60 + 30 = 90.", verifikasi={"ekspresi": "37 + 19 + 23 + 11", "hasil": "90"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Jika K + 64 = 64, berapakah nilai bilangan K?", ["0", "1", "64", "10"], "A", "Bilangan ditambah 0 hasilnya tetap 64, jadi K = 0.", verifikasi={"ekspresi": "0", "hasil": "0"})
mc("c4", "sulit", K, Me, S2, "Berapakah nilai N jika (45 + 18) + 22 = 45 + N?", ["40", "30", "50", "38"], "A", "18 + 22 = 40, jadi N = 40.", verifikasi={"ekspresi": "18 + 22", "hasil": "40"})
tf("c4", "sulit", K, Me, S3, "Jika A + 0 = 54, maka A + 10 bernilai 54.", "Salah", "A = 54, sehingga A + 10 = 64, bukan 54.")
mc("c4", "sulit", K, Me, S4, "Ibu membeli 33 apel, 26 jeruk, dan 17 salak. Berapa total buah?", ["76 buah", "66 buah", "77 buah", "75 buah"], "A", "33 + 17 = 50; 50 + 26 = 76 buah.", verifikasi={"ekspresi": "33 + 26 + 17", "hasil": "76"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Berapakah hasil dari 63 + 28 jika dihitung dengan membalik urutan bilangannya?", ["91", "81", "92", "90"], "A", "28 + 63 = 91.", verifikasi={"ekspresi": "28 + 63", "hasil": "91"})
mc("c5", "sedang", T, Me, S2, "Jika (36 + 24) + P = 85, berapakah nilai bilangan P?", ["25", "15", "35", "20"], "A", "60 + P = 85, maka P = 25.", verifikasi={"ekspresi": "85 - 60", "hasil": "25"})
mc("c5", "sedang", T, Me, S3, "Sebuah keranjang berisi 48 buah, ditambah 0 buah lagi. Berapa buah sekarang?", ["48 buah", "0 buah", "49 buah", "40 buah"], "A", "48 + 0 = 48 buah.", verifikasi={"ekspresi": "48 + 0", "hasil": "48"})
mc("c5", "sulit", T, Me, S4, "Hitunglah hasil dari 34 + 28 + 16 + 12 secara efisien!", ["90", "80", "100", "85"], "A", "(34 + 16) + (28 + 12) = 50 + 40 = 90.", verifikasi={"ekspresi": "34 + 28 + 16 + 12", "hasil": "90"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Nilai dari 42 + 28 + 25 sama dengan ....", ["95", "85", "96", "94"], "A", "42 + 28 = 70; 70 + 25 = 95.", verifikasi={"ekspresi": "42 + 28 + 25", "hasil": "95"})
mc("c5", "sulit", K, Me, S4, "Tiga keranjang berisi 39, 25, dan 21 butir telur. Total telur semuanya?", ["85 butir", "75 butir", "86 butir", "84 butir"], "A", "39 + 21 = 60; 60 + 25 = 85 butir.", verifikasi={"ekspresi": "39 + 25 + 21", "hasil": "85"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Siti menghitung 18 + 75 lebih cepat dengan cara 75 + 18. Mengapa cara Siti baik?", ["memulai dari bilangan lebih besar mempermudah perhitungan mental", "karena 18 harus dihilangkan", "karena 75 adalah angka genap", "hasilnya menjadi berbeda"], "A", "Memulai berhitung dari bilangan yang lebih besar membuat hitungan mental lebih singkat.")
mc("c6", "sulit", K, Me, S4, "Untuk menghitung 26 + 39 + 14, kelompok mana yang paling cerdas dipilih?", ["(26 + 14) lalu ditambah 39", "(26 + 39) lalu ditambah 14", "(39 - 14) lalu ditambah 26", "bebas tanpa aturan"], "A", "26 + 14 menghasilkan puluhan utuh 40, sehingga 40 + 39 = 79 sangat mudah dihitung.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S2, "Berapakah hasil dari (15 + 25) + (18 + 22) + 16?", ["96", "86", "95", "97"], "A", "40 + 40 + 16 = 96.", verifikasi={"ekspresi": "(15 + 25) + (18 + 22) + 16", "hasil": "96"})
mc("c6", "sulit", P, Me, S4, "Hitunglah jumlah empat bilangan: 17 + 26 + 23 + 24!", ["90", "80", "100", "88"], "A", "(17 + 23) + (26 + 24) = 40 + 50 = 90.", verifikasi={"ekspresi": "17 + 26 + 23 + 24", "hasil": "90"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab41_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab41.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
