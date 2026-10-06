#!/usr/bin/env python3
"""
Generator dan validator Bab 50 Matematika Kelas 2 SD:
"Kesalahan Umum: Mengira Perkalian Hanya Satu Kali Penjumlahan" (Fase A)
bab_id: 97b1e914-a14a-415a-86f3-b4464318ad0e
article_id: 7a13d7c5-7f41-4322-a982-f70914da7db8
quiz_id: e307373f-506e-4bb5-a3d8-1e434f07a718
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "b3c4d5e6f701"  # Menjumlahkan Pengali dan Bilangan
S2 = "c4d5e6f7a802"  # Hanya Menjumlah Sekali
S3 = "d5e6f7a8b903"  # Tertukar Perkalian dan Pembagian
S4 = "e6f7a8b9c004"  # Strategi Pemeriksaan Mandiri

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Banyak anak sering keliru berhitung.
Mereka mengira perkalian adalah penjumlahan biasa.
Misalnya tiga kali empat.
Ada yang menjawab tujuh.
Padahal tiga tambah empat tujuh.
Perkalian artinya empat tambah empat tambah empat.
Hasil tiga kali empat dua belas.
Tanda kali berbeda dari tambah!

:::definition
title: Perkalian Bukan Tambah Biasa
Perkalian adalah menjumlahkan bilangan berulang kali, bukan menjumlahkan kedua angkanya.
:::"""

s2_content = """Kesalahan lain adalah berhenti terlalu cepat.
Dua kali lima dikira hanya lima.
Padahal angka lima ada dua.
Lima ditambah lima adalah sepuluh.
Perhatikan selalu angka di depan.
Angka depan menunjukkan banyaknya pengulangan.
Jika angka depannya empat.
Maka bilangan dijumlahkan empat kali!

:::steps
title: Cara Menghindari Kesalahan Hitung
1. Lihat angka di depan sebagai pengulang.
2. Tulis bilangan berulang sebanyak pengulang.
3. Jumlahkan semua bilangan tersebut.
:::"""

s3_content = """Jangan sampai tertukar tanda operasi.
Tanda silang untuk perkalian.
Perkalian membuat kumpulan benda bertambah.
Tanda titik dua untuk pembagian.
Pembagian memecah benda menjadi bagian kecil.
Dua belas bagi tiga adalah empat.
Bukan tiga puluh enam!
Selalu perhatikan tanda operasinya."""

s4_content = """Bagaimana cara memeriksa hitunganmu?
Gunakan gambar kelompok lingkaran kecil.
Atau hitung dengan membilang lompat.
Misalnya lima kali dua.
Membilang lompat dua sebanyak lima kali.
Dua, empat, enam, delapan, sepuluh.
Hitunganmu pasti benar dan teliti!

:::common_trap
title: Mengira 3 x 4 Sama dengan 3 + 4
Tanda x bukan tanda +!
3 x 4 artinya 4 + 4 + 4 = 12.
3 + 4 hanya menghasilkan 7.
:::

:::callout
variant: summary
title: Ringkasan
text: Perkalian menjumlah berulang kali. Hindari hanya menjumlahkan dua angka atau mengabaikan tanda operasi.
:::"""

sections = [
    {
        "id": S1,
        "title": "Menjumlahkan Pengali dan Bilangan",
        "minutes": 6,
        "goal": "Siswa mampu mengidentifikasi dan memperbaiki kesalahan menjumlahkan dua angka pada operasi perkalian.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Hanya Menjumlah Sekali",
        "minutes": 6,
        "goal": "Siswa mampu menyadari bahwa perkalian melibatkan pengulangan utuh sesuai bilangan pengali.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Tertukar Perkalian dan Pembagian",
        "minutes": 6,
        "goal": "Siswa mampu membedakan dengan tegas simbol dan arti perkalian versus pembagian.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Strategi Pemeriksaan Mandiri",
        "minutes": 6,
        "goal": "Siswa terbiasa melakukan pengecekan mandiri menggunakan gambar atau teknik membilang lompat.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Mengira Perkalian Hanya Satu Kali Penjumlahan",
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
# 2. DEFINISI BANK 50 SOAL BAB 50
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
mc("c1", "mudah", D, F, S1, "Bentuk 3 x 4 diartikan sebagai penjumlahan berulang ....", ["4 + 4 + 4", "3 + 4", "3 + 3 + 3 + 3", "4 + 3"], "A", "3 x 4 adalah angka 4 dijumlahkan sebanyak 3 kali.")
tf("c1", "mudah", D, F, S2, "Bentuk perkalian 2 x 6 bernilai sama dengan 6 + 6.", "Benar", "2 kali angka 6 dijumlahkan: 6 + 6 = 12.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S3, "Tanda titik dua (:) dalam matematika adalah simbol untuk operasi ....", ["pembagian", "perkalian", "penjumlahan", "pengurangan"], "A", "Tanda : melambangkan pembagian.")
mc("c1", "mudah", T, F, S1, "Berapakah hasil dari 2 x 7 yang benar?", ["14", "9", "12", "16"], "A", "2 x 7 = 7 + 7 = 14.", verifikasi={"ekspresi": "2 * 7", "hasil": "14"})
sa("c1", "mudah", T, F, S4, "Berapakah hasil dari 3 x 5?", "15", "3 x 5 = 15.", verifikasi={"ekspresi": "3 * 5", "hasil": "15"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Ali menghitung 4 x 3 = 7. Mengapa jawaban Ali keliru?", ["Ali menjumlahkan 4 + 3 bukan mengalikannya", "jawaban Ali sudah benar", "Ali harusnya mengurang 4 - 3", "Ali salah tulis angka"], "A", "Ali keliru mengira perkalian adalah penjumlahan biasa 4 + 3.")
tf("c2", "mudah", D, Kn, S3, "Operasi 12 : 3 menghasilkan nilai yang sama dengan 12 x 3.", "Salah", "12 : 3 = 4, sedangkan 12 x 3 = 36. Nilainya berbeda jauh.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Berapakah hasil yang benar dari 3 x 6?", ["18", "9", "12", "15"], "A", "3 x 6 = 6 + 6 + 6 = 18.", "Mengira 3 x 6 = 3 + 6 = 9", verifikasi={"ekspresi": "3 * 6", "hasil": "18"})
mc("c2", "mudah", R, Kn, S2, "Budi mengira 2 x 8 hasilnya 8. Berapakah hasil yang benar?", ["16", "10", "8", "14"], "A", "2 x 8 = 8 + 8 = 16.", "Mengabaikan pengulangan perkalian dua", verifikasi={"ekspresi": "2 * 8", "hasil": "16"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Manakah pernyataan yang BENAR mengenai perkalian 5 x 2?", ["hasilnya adalah 10", "hasilnya adalah 7", "sama artinya dengan 5 + 2", "hasilnya bilangan ganjil"], "A", "5 x 2 = 2 + 2 + 2 + 2 + 2 = 10.")
mc("c2", "mudah", T, Kn, S2, "Berapakah hasil dari 4 x 4?", ["16", "8", "12", "20"], "A", "4 x 4 = 16.", verifikasi={"ekspresi": "4 * 4", "hasil": "16"})
tf("c2", "mudah", T, Kn, S1, "Operasi 3 x 5 sama artinya dengan menjumlahkan 3 dengan 5.", "Salah", "3 x 5 artinya menjumlahkan 5 sebanyak 3 kali (15), bukan 3 + 5 (8).")
sa("c2", "mudah", T, Kn, S4, "Berapakah hasil dari 2 x 9?", "18", "2 x 9 = 18.", verifikasi={"ekspresi": "2 * 9", "hasil": "18"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Siti menghitung 5 x 4 dan menulis 9. Berapakah hasil sebenarnya?", ["20", "15", "9", "25"], "A", "5 x 4 = 20. 9 adalah hasil penjumlahan 5 + 4.", "Menjumlahkan 5 + 4 bukan mengalikan", verifikasi={"ekspresi": "5 * 4", "hasil": "20"})
mc("c3", "sedang", R, Pr, S3, "Dono menghitung 16 : 4 = 64 karena mengalikan. Hasil pembagian benar?", ["4", "64", "8", "12"], "A", "16 : 4 = 4. 64 adalah hasil 16 x 4.", "Mengalikan bukannya membagi", verifikasi={"ekspresi": "16 / 4", "hasil": "4"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berapakah selisih hasil 4 x 3 dengan 4 + 3?", ["5", "7", "12", "4"], "A", "4 x 3 = 12 dan 4 + 3 = 7. Selisihnya 12 - 7 = 5.", verifikasi={"ekspresi": "(4 * 3) - (4 + 3)", "hasil": "5"})
mc("c3", "mudah", T, Pr, S2, "Berapakah hasil dari 3 x 8?", ["24", "11", "21", "27"], "A", "3 x 8 = 24.", verifikasi={"ekspresi": "3 * 8", "hasil": "24"})
tf("c3", "sedang", T, Pr, S1, "Hasil dari 6 x 2 sama dengan hasil dari 6 + 2.", "Salah", "6 x 2 = 12, sedangkan 6 + 2 = 8.")
mc("c3", "sedang", T, Pr, S3, "Manakah dari pasangan operasi berikut yang hasilnya BERBEDA?", ["12 : 2 dan 12 x 2", "2 x 6 dan 6 x 2", "3 x 4 dan 4 + 4 + 4", "10 : 2 dan 15 : 3"], "A", "12 : 2 = 6, sedangkan 12 x 2 = 24. Hasilnya berbeda.")
tf("c3", "sedang", T, Pr, S4, "Membilang lompat 3 sebanyak 4 kali menghasilkan angka 12.", "Benar", "3, 6, 9, 12.")
sa("c3", "sedang", T, Pr, S2, "Berapakah hasil dari 5 x 6?", "30", "5 x 6 = 30.", verifikasi={"ekspresi": "5 * 6", "hasil": "30"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Berapakah hasil dari 4 x 7?", ["28", "11", "24", "32"], "A", "4 x 7 = 28.", verifikasi={"ekspresi": "4 * 7", "hasil": "28"})
mc("c3", "sedang", X, Pr, S2, "Rudi punya 3 kantong isi 6 bola. Rudi mengira ada 9 bola. Seharusnya?", ["18 bola", "9 bola", "15 bola", "12 bola"], "A", "3 x 6 = 18 bola. 9 adalah 3 + 6.", verifikasi={"ekspresi": "3 * 6", "hasil": "18"})
tf("c3", "sedang", X, Pr, S4, "Pemeriksaan perkalian dapat dilakukan dengan menggambar kelompok lingkaran.", "Benar", "Gambar lingkaran membantu memvisualisasikan penjumlahan berulang.")
sa("c3", "sedang", X, Pr, S3, "Berapakah hasil dari 20 : 4?", "5", "20 : 4 = 5.", verifikasi={"ekspresi": "20 / 4", "hasil": "5"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Berapakah hasil dari 6 x 3?", ["18", "9", "15", "21"], "A", "6 x 3 = 18.", verifikasi={"ekspresi": "6 * 3", "hasil": "18"})
mc("c3", "sedang", K, Pr, S2, "Berapakah hasil dari 4 x 8?", ["32", "12", "28", "36"], "A", "4 x 8 = 32.", verifikasi={"ekspresi": "4 * 8", "hasil": "32"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S1
mc("c4", "sedang", T, Kn, S1, "Mengapa hasil 5 x 3 jauh lebih besar daripada 5 + 3?", ["karena angka 3 dijumlahkan berulang sebanyak 5 kali", "karena perkalian selalu salah", "karena 5 bilangan ganjil", "karena 3 bilangan genap"], "A", "5 x 3 = 15 (menjumlahkan 3 lima kali), sedangkan 5 + 3 = 8.")
mc("c4", "sedang", T, Kn, S2, "Seorang anak menulis 3 x 7 = 7 + 7 = 14. Apa kesalahan anak itu?", ["baru menjumlahkan 2 kali bukan 3 kali", "anak itu harusnya mengurang", "hasilnya harusnya 10", "jawaban anak sudah benar"], "A", "Anak itu hanya menjumlahkan 7 dua kali (2 x 7), padahal pengalinya 3 (3 x 7 = 21).")
tf("c4", "sedang", T, Kn, S3, "Menghitung 18 : 2 sama artinya dengan membilang lompat 2 sampai 18.", "Benar", "Banyaknya lompatan adalah hasil bagi (9 kali).")
tf("c4", "sedang", T, Kn, S4, "Hasil dari 4 x 5 sama dengan hasil dari 4 + 5.", "Salah", "4 x 5 = 20, sedangkan 4 + 5 = 9.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari (4 x 5) - (4 + 5)?", "11", "4 x 5 = 20; 4 + 5 = 9; 20 - 9 = 11.", verifikasi={"ekspresi": "(4 * 5) - (4 + 5)", "hasil": "11"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Manakah dari operasi berikut yang hasilnya PALING TEPAT untuk 6 x 4?", ["24", "10", "20", "28"], "A", "6 x 4 = 24. 10 adalah penjumlahan 6 + 4.", verifikasi={"ekspresi": "6 * 4", "hasil": "24"})
mc("c4", "sedang", X, Kn, S3, "Jika kamu ingin membagi 15 permen ke 3 anak, operasi apa yang kamu pakai?", ["15 : 3", "15 x 3", "15 + 3", "15 - 3"], "A", "Membagikan benda ke beberapa anak memakai pembagian: 15 : 3.")
tf("c4", "sedang", X, Kn, S2, "Bentuk perkalian 1 x 9 hasilnya adalah 10.", "Salah", "1 x 9 = 9, bukan 10 (1 + 9 = 10).")
mc("c4", "sulit", X, Me, S4, "Di antara operasi berikut, manakah yang selisihnya PALING BESAR dengan penjumlahannya?", ["6 x 6", "2 x 3", "2 x 2", "3 x 3"], "A", "6 x 6 = 36 dan 6 + 6 = 12 (selisih 24). Paling besar di antara pilihan lain.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Edo menjawab 5 x 5 = 10. Jawaban yang tepat dan alasan yang benar adalah ....", ["25, karena 5 x 5 artinya 5 + 5 + 5 + 5 + 5", "10, karena 5 ditambah 5", "15, karena 5 dikali 3", "20, karena 5 dikali 4"], "A", "5 x 5 = 25 (penjumlahan 5 sebanyak 5 kali).")
mc("c4", "sulit", K, Me, S2, "Lina menghitung 2 x 10 dan menjawab 10. Apa saran yang tepat untuk Lina?", ["Lina harus menjumlahkan angka 10 sebanyak 2 kali", "jawaban Lina sudah benar", "Lina harus mengurang 10 dengan 2", "Lina harus membagi 10"], "A", "Lina lupa menjumlahkan 10 dua kali (10 + 10 = 20).")
tf("c4", "sulit", K, Me, S4, "Hasil dari (3 x 4) lebih besar daripada hasil (3 + 4).", "Benar", "3 x 4 = 12 dan 3 + 4 = 7. 12 lebih besar dari 7.")
mc("c4", "sulit", K, Me, S4, "Berapakah hasil dari (5 x 4) - (3 x 3)?", ["11", "9", "13", "10"], "A", "5 x 4 = 20; 3 x 3 = 9; 20 - 9 = 11.", verifikasi={"ekspresi": "(5 * 4) - (3 * 3)", "hasil": "11"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Jika P x 4 = 24, berapakah nilai P + 4?", ["10", "8", "12", "9"], "A", "P = 24 : 4 = 6; P + 4 = 6 + 4 = 10.", verifikasi={"ekspresi": "(24 / 4) + 4", "hasil": "10"})
mc("c5", "sedang", T, Me, S2, "Berapakah nilai pengali K jika K x 7 = 28?", ["4", "3", "5", "6"], "A", "K = 28 : 7 = 4.", verifikasi={"ekspresi": "28 / 7", "hasil": "4"})
mc("c5", "sedang", T, Me, S3, "Sebuah bilangan dikalikan 4 menghasilkan 36. Jika dibagi 4 menghasilkan ....", ["9", "8", "7", "10"], "A", "36 : 4 = 9.", verifikasi={"ekspresi": "36 / 4", "hasil": "9"})
mc("c5", "sulit", T, Me, S4, "Berapakah hasil dari (6 x 5) - (6 + 5)?", ["19", "18", "20", "17"], "A", "6 x 5 = 30; 6 + 5 = 11; 30 - 11 = 19.", verifikasi={"ekspresi": "(6 * 5) - (6 + 5)", "hasil": "19"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Manakah dari perhitungan berikut yang TIDAK MENGALAMI kesalahan penjumlahan?", ["4 x 5 = 20", "4 x 5 = 9", "3 x 7 = 10", "2 x 8 = 10"], "A", "4 x 5 = 20 adalah perkalian yang benar.")
mc("c5", "sulit", K, Me, S4, "Berapakah hasil dari (7 x 3) + (18 : 2)?", ["30", "28", "32", "26"], "A", "7 x 3 = 21; 18 : 2 = 9; 21 + 9 = 30.", verifikasi={"ekspresi": "(7 * 3) + (18 / 2)", "hasil": "30"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Bagaimana cara membuktikan pada teman bahwa 3 x 4 bukan 7?", ["tunjukkan dengan gambar 3 piring masing-masing 4 benda berjumlah 12", "katakan bahwa guru yang memberitahu", "suruh teman menghafal tabel", "tidak perlu dibuktikan"], "A", "Visualisasi konkret 3 piring isi 4 benda membuktikan totalnya 12 secara meyakinkan.")
mc("c6", "sulit", K, Me, S4, "Jika N = 4 x 6 dan M = 24 : 4, berapakah hasil N - M?", ["18", "16", "20", "14"], "A", "N = 24, M = 6; N - M = 24 - 6 = 18.", verifikasi={"ekspresi": "(4 * 6) - (24 / 4)", "hasil": "18"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi gabungan: (5 x 8) - (32 : 4) + (3 x 4)!", ["44", "42", "46", "40"], "A", "5 x 8 = 40; 32 : 4 = 8; 3 x 4 = 12; 40 - 8 + 12 = 44.", verifikasi={"ekspresi": "(5 * 8) - (32 / 4) + (3 * 4)", "hasil": "44"})
mc("c6", "sulit", P, Me, S4, "Budi punya 4 kotak isi 7 stiker. Kakak memberi 6 stiker. Total stiker?", ["34 stiker", "32 stiker", "36 stiker", "30 stiker"], "A", "(4 x 7) + 6 = 28 + 6 = 34 stiker.", verifikasi={"ekspresi": "(4 * 7) + 6", "hasil": "34"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab50_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab50.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")

