#!/usr/bin/env python3
"""
Generator dan validator Bab 46 Matematika Kelas 2 SD:
"Perkalian 2, 5, dan 10" (Fase A)
bab_id: 357fb377-39d7-4797-8092-45c9128b143a
article_id: 94dd6b46-476f-455c-8cb7-1f43ca3fdef6
quiz_id: 62b90adb-20bb-481a-aaa0-919cf1b73d3a
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "d5e6f7a8b901"  # Perkalian 2
S2 = "e6f7a8b9c002"  # Perkalian 5
S3 = "f7a8b9c0d103"  # Perkalian 10
S4 = "a8b9c0d1e204"  # Membandingkan dan Menyelesaikan Masalah

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Perkalian dua sangat istimewa.
Perkalian dua artinya melipatgandakan bilangan.
Kamu bisa membilang lompat dua.
Dua, empat, enam, delapan, sepuluh.
Semua hasil perkalian dua genap.
Tiga kali dua adalah enam.
Tujuh kali dua adalah empat belas.
Sangat mudah untuk diingat!

:::definition
title: Perkalian Dua
Perkalian dua adalah penjumlahan dua bilangan yang sama besar.
:::"""

s2_content = """Perkalian lima memiliki pola unik.
Gunakan jari tanganmu untuk membilang.
Satu tangan memiliki lima jari.
Membilang lompat lima sangat seru.
Lima, sepuluh, lima belas, dua puluh.
Perhatikan angka satuan paling belakang.
Satuannya selalu nol atau lima.
Empat kali lima adalah dua puluh.

:::steps
title: Pola Satuan Perkalian Lima
1. Kalikan bilangan dengan angka lima.
2. Jika bilangan ganjil, satuan lima.
3. Jika bilangan genap, satuan nol.
:::"""

s3_content = """Perkalian sepuluh paling mudah dikuasai.
Kamu hanya perlu menambah nol.
Tulis angka yang dikalikan.
Lalu beri angka nol di belakangnya.
Tiga kali sepuluh jadi tiga puluh.
Tujuh kali sepuluh jadi tujuh puluh.
Sembilan kali sepuluh jadi sembilan puluh.
Semua hasil perkalian sepuluh puluhan!"""

s4_content = """Mari kita hubungkan perkalian ini.
Dua kali lima hasilnya sepuluh.
Maka perkalian sepuluh kelipatan lima.
Enam kali lima adalah tiga puluh.
Tiga kali sepuluh juga tiga puluh.
Gunakan pola ini untuk berhitung cepat.
Latihan membuat hitunganmu semakin tepat!

:::common_trap
title: Terbalik Menambah Nol
Angka nol hanya ditambah pada perkalian sepuluh.
Jangan menambahkan nol pada perkalian lima!
Enam kali lima adalah tiga puluh, bukan enam puluh.
:::

:::callout
variant: summary
title: Ringkasan
text: Perkalian dua menghasilkan genap. Perkalian lima berakhiran nol atau lima. Perkalian sepuluh cukup tambah angka nol.
:::"""

sections = [
    {
        "id": S1,
        "title": "Perkalian 2",
        "minutes": 6,
        "goal": "Siswa mampu menghitung perkalian 2 menggunakan strategi lompat dua atau menggandakan bilangan.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Perkalian 5",
        "minutes": 6,
        "goal": "Siswa mampu menentukan hasil perkalian 5 dengan mengenali pola angka satuan 0 dan 5.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Perkalian 10",
        "minutes": 6,
        "goal": "Siswa mampu menghitung perkalian 10 menggunakan aturan penambahan angka 0 pada nilai tempat puluhan.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Membandingkan dan Menyelesaikan Masalah",
        "minutes": 6,
        "goal": "Siswa mampu membandingkan hasil dan menyelesaikan masalah perkalian 2, 5, dan 10 secara terpadu.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Perkalian 2, 5, dan 10",
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
# 2. DEFINISI BANK 50 SOAL BAB 46
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
mc("c1", "mudah", D, F, S1, "Semua bilangan hasil perkalian 2 selalu merupakan bilangan ....", ["genap", "ganjil", "nol", "ratusan"], "A", "Perkalian 2 menghasilkan bilangan kelipatan 2 yang genap.")
tf("c1", "mudah", D, F, S3, "Hasil perkalian suatu bilangan dengan 10 selalu berakhiran angka 0.", "Benar", "Angka satuan pada perkalian 10 selalu 0.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Angka satuan pada hasil perkalian 5 selalu angka 0 atau ....", ["5", "2", "3", "7"], "A", "Pola satuan perkalian 5 selalu bergantian antara 0 dan 5.")
mc("c1", "mudah", T, F, S3, "Berapakah hasil dari 4 x 10?", ["40", "14", "44", "400"], "A", "4 x 10 = 40.", verifikasi={"ekspresi": "4 * 10", "hasil": "40"})
sa("c1", "mudah", T, F, S1, "Berapakah hasil dari 5 x 2?", "10", "5 x 2 = 10.", verifikasi={"ekspresi": "5 * 2", "hasil": "10"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Manakah dari bilangan berikut yang merupakan hasil perkalian 5?", ["35", "32", "34", "38"], "A", "35 berakhiran angka 5, jadi kelipatan 5.")
tf("c2", "mudah", D, Kn, S1, "Hasil perkalian 7 x 2 bernilai sama dengan 7 + 7.", "Benar", "Perkalian 2 adalah menggandakan bilangan itu sendiri.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Berapakah hasil dari 6 x 5?", ["30", "25", "35", "60"], "A", "6 x 5 = 30.", "Mengira perkalian 5 sama dengan tambah 0", verifikasi={"ekspresi": "6 * 5", "hasil": "30"})
mc("c2", "mudah", R, Kn, S3, "Berapakah hasil dari 8 x 10?", ["80", "18", "88", "800"], "A", "8 x 10 = 80.", "Menjumlahkan 8 + 10 bukan mengalikan", verifikasi={"ekspresi": "8 * 10", "hasil": "80"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Berapakah hasil dari 6 x 2?", ["12", "14", "10", "8"], "A", "6 x 2 = 12.", verifikasi={"ekspresi": "6 * 2", "hasil": "12"})
mc("c2", "mudah", T, Kn, S4, "Manakah pernyataan yang benar mengenai hubungan perkalian 5 dan 10?", ["dua kali perkalian 5 sama dengan perkalian 10", "perkalian 5 selalu lebih besar dari 10", "hasil perkalian keduanya selalu ganjil", "keduanya tidak berhubungan"], "A", "Karena 2 x 5 = 10, maka dua kelompok 5 sama dengan satu kelompok 10.")
tf("c2", "mudah", T, Kn, S2, "Hasil perkalian bilangan genap dengan 5 selalu berakhiran angka 5.", "Salah", "Perkalian bilangan genap dengan 5 selalu berakhiran angka 0 (contoh: 4 x 5 = 20).")
sa("c2", "mudah", T, Kn, S3, "Berapakah hasil dari 6 x 10?", "60", "6 x 10 = 60.", verifikasi={"ekspresi": "6 * 10", "hasil": "60"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Berapakah hasil dari 9 x 2?", ["18", "16", "20", "19"], "A", "9 x 2 = 18.", "Keliru membilang lompat 2", verifikasi={"ekspresi": "9 * 2", "hasil": "18"})
mc("c3", "sedang", R, Pr, S2, "Berapakah hasil dari 7 x 5?", ["35", "30", "40", "45"], "A", "7 x 5 = 35.", "Salah pola kelipatan 5", verifikasi={"ekspresi": "7 * 5", "hasil": "35"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berapakah hasil dari 8 x 2?", ["16", "14", "18", "12"], "A", "8 x 2 = 16.", verifikasi={"ekspresi": "8 * 2", "hasil": "16"})
mc("c3", "mudah", T, Pr, S2, "Berapakah hasil dari 5 x 5?", ["25", "20", "30", "15"], "A", "5 x 5 = 25.", verifikasi={"ekspresi": "5 * 5", "hasil": "25"})
tf("c3", "sedang", T, Pr, S3, "Bilangan 75 adalah hasil dari perkalian 7 x 10.", "Salah", "7 x 10 = 70 bukan 75.")
mc("c3", "sedang", T, Pr, S4, "Berapakah hasil dari (3 x 10) + (2 x 5)?", ["40", "35", "45", "30"], "A", "3 x 10 = 30; 2 x 5 = 10; 30 + 10 = 40.", verifikasi={"ekspresi": "(3 * 10) + (2 * 5)", "hasil": "40"})
tf("c3", "sedang", T, Pr, S1, "Hasil dari 4 x 2 lebih besar daripada 3 x 5.", "Salah", "4 x 2 = 8, sedangkan 3 x 5 = 15. 8 lebih kecil dari 15.")
sa("c3", "sedang", T, Pr, S2, "Berapakah hasil dari 8 x 5?", "40", "8 x 5 = 40.", verifikasi={"ekspresi": "8 * 5", "hasil": "40"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Ada 7 pasang sepatu. Berapa banyak sepatu seluruhnya?", ["14 buah", "12 buah", "16 buah", "10 buah"], "A", "7 x 2 = 14 buah.", verifikasi={"ekspresi": "7 * 2", "hasil": "14"})
mc("c3", "sedang", X, Pr, S2, "Ada 9 kantong permen, tiap kantong 5 permen. Berapa total permen?", ["45 butir", "40 butir", "50 butir", "35 butir"], "A", "9 x 5 = 45 butir.", verifikasi={"ekspresi": "9 * 5", "hasil": "45"})
tf("c3", "sedang", X, Pr, S4, "Hasil dari 6 x 5 sama dengan hasil dari 3 x 10 yaitu 30.", "Benar", "Keduanya bernilai 30.")
sa("c3", "sedang", X, Pr, S3, "Berapakah hasil dari 9 x 10?", "90", "9 x 10 = 90.", verifikasi={"ekspresi": "9 * 10", "hasil": "90"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Berapakah hasil dari 4 x 5?", ["20", "25", "15", "10"], "A", "4 x 5 = 20.", verifikasi={"ekspresi": "4 * 5", "hasil": "20"})
mc("c3", "sedang", K, Pr, S3, "Berapakah hasil dari 5 x 10?", ["50", "40", "60", "15"], "A", "5 x 10 = 50.", verifikasi={"ekspresi": "5 * 10", "hasil": "50"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S1
mc("c4", "sedang", T, Kn, S1, "Manakah dari bilangan berikut yang BUKAN hasil perkalian 2?", ["17", "12", "16", "20"], "A", "17 adalah bilangan ganjil, tidak mungkin hasil kali 2.")
mc("c4", "sedang", T, Kn, S2, "Mengapa hasil 7 x 5 berakhiran angka 5?", ["karena 7 adalah bilangan ganjil", "karena 7 kelipatan 5", "karena 5 bilangan genap", "hanya kebetulan"], "A", "Bilangan ganjil dikali 5 selalu menghasilkan angka satuan 5.")
tf("c4", "sedang", T, Kn, S3, "Hasil perkalian 10 selalu dapat dibagi habis menjadi puluhan utuh.", "Benar", "Karena satuannya selalu 0, nilainya berupa puluhan tepat.")
tf("c4", "sedang", T, Kn, S4, "Hasil dari 5 x 2 sama dengan hasil dari 2 x 10.", "Salah", "5 x 2 = 10, sedangkan 2 x 10 = 20.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari (6 x 2) + (3 x 10)?", "42", "6 x 2 = 12; 3 x 10 = 30; 12 + 30 = 42.", verifikasi={"ekspresi": "(6 * 2) + (3 * 10)", "hasil": "42"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Lina punya 6 vas bunga. Tiap vas ada 2 mawar merah. Berapa mawar Lina?", ["12 tangkai", "10 tangkai", "14 tangkai", "8 tangkai"], "A", "6 x 2 = 12 tangkai.", verifikasi={"ekspresi": "6 * 2", "hasil": "12"})
mc("c4", "sedang", X, Kn, S3, "Di kelas ada 8 kelompok siswa. Tiap kelompok dapat 10 pensil. Total pensil?", ["80 pensil", "70 pensil", "90 pensil", "18 pensil"], "A", "8 x 10 = 80 pensil.", verifikasi={"ekspresi": "8 * 10", "hasil": "80"})
tf("c4", "sedang", X, Kn, S2, "Bilangan ganjil dikalikan dengan 5 selalu menghasilkan angka satuan 0.", "Salah", "Bilangan ganjil dikali 5 menghasilkan angka satuan 5 (misal 3 x 5 = 15).")
mc("c4", "sulit", X, Me, S4, "Manakah dari operasi berikut yang hasilnya PALING KECIL?", ["8 x 2", "3 x 5", "2 x 10", "4 x 5"], "A", "3 x 5 = 15; 8 x 2 = 16; 4 x 5 = 20; 2 x 10 = 20. Paling kecil 15.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Di antara bilangan 22, 25, 28, dan 31, mana hasil perkalian 5?", ["25", "22", "28", "31"], "A", "25 berakhiran angka 5, yaitu 5 x 5 = 25.")
mc("c4", "sulit", K, Me, S4, "Budi punya 4 uang logam 500 rupiah. Berapa keping untuk perkalian 4 x 5?", ["20", "25", "15", "10"], "A", "4 x 5 = 20.", verifikasi={"ekspresi": "4 * 5", "hasil": "20"})
tf("c4", "sulit", K, Me, S1, "Menjumlahkan bilangan yang sama sebanyak 2 kali sama dengan mengalikannya dengan 2.", "Benar", "A + A = 2 x A.")
mc("c4", "sulit", K, Me, S3, "Pak Pos mengantar 7 ikat surat. Tiap ikat ada 10 surat. Berapa surat?", ["70 surat", "60 surat", "80 surat", "17 surat"], "A", "7 x 10 = 70 surat.", verifikasi={"ekspresi": "7 * 10", "hasil": "70"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Berapakah nilai N pada kalimat matematika: N x 2 = 18?", ["9", "8", "7", "10"], "A", "9 x 2 = 18, jadi N = 9.", verifikasi={"ekspresi": "18 / 2", "hasil": "9"})
mc("c5", "sedang", T, Me, S2, "Berapakah nilai P pada kalimat matematika: P x 5 = 45?", ["9", "8", "7", "10"], "A", "9 x 5 = 45, jadi P = 9.", verifikasi={"ekspresi": "45 / 5", "hasil": "9"})
mc("c5", "sedang", T, Me, S3, "Berapakah nilai Q pada kalimat matematika: Q x 10 = 70?", ["7", "6", "8", "9"], "A", "7 x 10 = 70, jadi Q = 7.", verifikasi={"ekspresi": "70 / 10", "hasil": "7"})
mc("c5", "sulit", T, Me, S4, "Berapakah hasil dari (7 x 5) - (6 x 2)?", ["23", "25", "21", "27"], "A", "7 x 5 = 35; 6 x 2 = 12; 35 - 12 = 23.", verifikasi={"ekspresi": "(7 * 5) - (6 * 2)", "hasil": "23"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S4, "Manakah pernyataan yang BENAR mengenai hasil perkalian berikut?", ["4 x 10 sama dengan 8 x 5", "3 x 10 lebih kecil dari 5 x 5", "6 x 2 sama dengan 3 x 5", "7 x 2 lebih besar dari 3 x 10"], "A", "4 x 10 = 40 dan 8 x 5 = 40. Keduanya bernilai sama.")
mc("c5", "sulit", K, Me, S4, "Berapakah hasil dari (5 x 10) - (5 x 5)?", ["25", "20", "30", "15"], "A", "5 x 10 = 50; 5 x 5 = 25; 50 - 25 = 25.", verifikasi={"ekspresi": "(5 * 10) - (5 * 5)", "hasil": "25"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S3, "Bagaimana cara tercepat menghitung 9 x 10 tanpa menjumlahkan berulang?", ["tulis angka 9 lalu tambahkan angka 0 di belakangnya", "hitung lompat 5 sebanyak sembilan kali", "jumlahkan 9 dengan 10", "kurangkan 10 dengan 9"], "A", "Menambahkan angka 0 di belakang adalah aturan tercepat perkalian 10.")
mc("c6", "sulit", K, Me, S4, "Jika A x 5 = 30 dan B x 2 = 16, berapakah hasil A + B?", ["14", "12", "16", "15"], "A", "A = 6, B = 8; 6 + 8 = 14.", verifikasi={"ekspresi": "(30 / 5) + (16 / 2)", "hasil": "14"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi gabungan: (8 x 5) + (7 x 2) - (2 x 10)!", ["34", "32", "36", "30"], "A", "8 x 5 = 40; 7 x 2 = 14; 2 x 10 = 20; 40 + 14 - 20 = 34.", verifikasi={"ekspresi": "(8 * 5) + (7 * 2) - (2 * 10)", "hasil": "34"})
mc("c6", "sulit", P, Me, S4, "Toko punya 5 kotak bola tenis isi 10. Terjual 15 bola. Sisa bola?", ["35 bola", "40 bola", "30 bola", "25 bola"], "A", "5 x 10 = 50; 50 - 15 = 35 bola.", verifikasi={"ekspresi": "(5 * 10) - 15", "hasil": "35"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab46_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab46.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
