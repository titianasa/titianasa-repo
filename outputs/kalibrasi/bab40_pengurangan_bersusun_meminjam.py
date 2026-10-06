#!/usr/bin/env python3
"""
Generator dan validator Bab 40 Matematika Kelas 2 SD:
"Pengurangan Bersusun dengan Teknik Meminjam" (Fase A)
bab_id: be5feac4-17aa-4e63-9f9b-1c53766550a6
article_id: 68ff39e5-7bc9-4c8f-94bf-8b4b5991a451
quiz_id: 191f4cab-d026-49d7-a519-069a30ee38a8
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "c9d0e1f2a301"  # Penulisan Pengurangan Bersusun
S2 = "d0e1f2a3b402"  # Konsep Meminjam Satu Puluhan
S3 = "e1f2a3b4c503"  # Langkah Pengurangan Bersusun Meminjam
S4 = "f2a3b4c5d604"  # Penerapan Pengurangan Soal Cerita

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Pengurangan bersusun disusun rapi ke bawah.
Bilangan awal ditulis di atas.
Bilangan pengurang ditulis di bawah.
Satuan diletakkan lurus dengan satuan.
Puluhan diletakkan lurus dengan puluhan.
Garis bawah diberi tanda kurang.
Hitung selalu dimulai dari satuan.
Setelah satuan, baru hitung puluhan.

:::definition
title: Pengurangan Bersusun
Pengurangan bersusun adalah cara mengurangkan bilangan dengan menyusun ke bawah sesuai nilai tempatnya.
:::"""

s2_content = """Kadang satuan atas lebih kecil.
Misalnya dua dikurang tujuh.
Dua tidak bisa dikurang tujuh.
Kita perlu meminjam satu puluhan.
Satu puluhan bernilai sepuluh satuan.
Sepuluh ditambah dua menjadi dua belas.
Sekarang dua belas bisa dikurang tujuh.
Puluhan di sebelah kiri berkurang satu.

:::steps
title: Langkah Meminjam
1. Pinjam satu puluhan dari angka sebelah kiri.
2. Ubah satu puluhan menjadi sepuluh satuan.
3. Tambahkan ke angka satuan awal.
4. Kurangi angka puluhan dengan satu.
:::"""

s3_content = """Ayo hitung lima puluh dua kurang dua puluh tujuh.
Tulis lima puluh dua di atas.
Tulis dua puluh tujuh di bawah.
Dua tidak cukup dikurang tujuh.
Pinjam satu puluhan dari lima.
Angka lima dicoret menjadi empat.
Satuan dua menjadi dua belas.
Dua belas kurang tujuh jadi lima.
Empat kurang dua jadi dua.
Jawabannya adalah dua puluh lima!"""

s4_content = """Mari selesaikan soal cerita bersama.
Paman memiliki enam puluh satu mangga.
Sebanyak dua puluh empat mangga dibagikan.
Berapa sisa mangga paman sekarang?
Enam puluh satu kurang dua puluh empat.
Satu pinjam puluhan menjadi sebelas.
Sebelas kurang empat sama dengan tujuh.
Sisa lima puluhan kurang dua jadi tiga.
Sisa mangga paman tiga puluh tujuh.

:::common_trap
title: Lupa Mengurangi Angka Puluhan
Saat meminjam, puluhan sudah berkurang satu.
Jangan hitung memakai angka puluhan lama.
Coretlah puluhan agar tidak salah hitung!
:::

:::callout
variant: summary
title: Ringkasan
text: Susun bilangan lurus nilai tempat. Pinjam puluhan bila satuan kurang. Jangan lupa kurangi puluhan yang dipinjam.
:::"""

sections = [
    {
        "id": S1,
        "title": "Penulisan Pengurangan Bersusun",
        "minutes": 6,
        "goal": "Siswa mampu menyusun pengurangan dua bilangan dua angka sejajar menurut satuan dan puluhannya.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Konsep Meminjam Satu Puluhan",
        "minutes": 6,
        "goal": "Siswa memahami bahwa 1 puluhan dapat diubah menjadi 10 satuan saat satuan atas tidak cukup dikurangkan.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Langkah Pengurangan Bersusun Meminjam",
        "minutes": 6,
        "goal": "Siswa mampu menyelesaikan pengurangan bersusun dengan teknik meminjam secara berurutan dan tepat.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Penerapan Pengurangan Soal Cerita",
        "minutes": 6,
        "goal": "Siswa mampu menerapkan pengurangan bersusun dengan teknik meminjam dalam memecahkan masalah kontekstual sehari-hari.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Pengurangan Bersusun dengan Teknik Meminjam",
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
# 2. DEFINISI BANK 50 SOAL BAB 40
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
mc("c1", "mudah", D, F, S1, "Saat melakukan pengurangan bersusun, kolom mana yang dihitung pertama?", ["kolom satuan", "kolom puluhan", "kolom ratusan", "bebas"], "A", "Pengurangan bersusun selalu dimulai dari kolom satuan di sebelah kanan.")
tf("c1", "mudah", D, F, S2, "Satu puluhan yang dipinjam bernilai 10 satuan.", "Benar", "1 puluhan = 10 satuan.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Berapakah hasil dari 48 dikurang 25 secara bersusun?", ["23", "22", "24", "25"], "A", "8 - 5 = 3; 4 - 2 = 2. Hasil 23 (tanpa meminjam).", verifikasi={"ekspresi": "48 - 25", "hasil": "23"})
mc("c1", "mudah", T, F, S2, "Jika meminjam 1 puluhan untuk angka satuan 3, satuan menjadi ....", ["13", "12", "14", "15"], "A", "10 + 3 = 13 satuan.")
sa("c1", "mudah", T, F, S3, "Berapakah hasil dari 37 dikurang 14?", "23", "37 - 14 = 23.", verifikasi={"ekspresi": "37 - 14", "hasil": "23"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Kapan kita perlu meminjam pada pengurangan bersusun?", ["saat angka satuan atas lebih kecil dari bawah", "saat angka puluhan lebih besar", "setiap kali berhitung", "tidak pernah"], "A", "Meminjam diperlukan jika satuan atas tidak cukup dikurangkan.", "Keliru mengenali kondisi meminjam")
tf("c2", "mudah", D, Kn, S3, "Pada pengurangan 65 - 28, angka 5 perlu meminjam dari 6.", "Benar", "Karena 5 lebih kecil dari 8, maka 5 harus meminjam 1 puluhan dari 6.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Setelah 1 puluhan dipinjam dari angka 7, angka 7 menjadi ....", ["6", "5", "8", "7"], "A", "Karena sudah dipinjam 1, maka 7 - 1 = 6.", "Lupa mengurangi nilai puluhan yang telah dipinjam")
mc("c2", "mudah", R, Kn, S3, "Berapakah hasil dari 42 dikurang 17?", ["25", "35", "26", "24"], "A", "12 - 7 = 5; 3 - 1 = 2 puluhan. Hasil 25.", "Salah menghitung puluhan setelah meminjam", verifikasi={"ekspresi": "42 - 17", "hasil": "25"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Pada 54 - 21, angka 4 lurus dengan angka ....", ["1", "2", "5", "0"], "A", "Angka 4 dan 1 sama-sama satuan sehingga harus lurus.")
mc("c2", "mudah", T, Kn, S4, "Lani punya 35 balon, meletus 18 balon. Sisa balon dihitung dengan ....", ["pengurangan", "penjumlahan", "perkalian", "pengukuran"], "A", "Balon meletus berarti jumlah balon berkurang.")
tf("c2", "mudah", T, Kn, S2, "Meminjam 1 puluhan membuat angka satuan bertambah 1.", "Salah", "Meminjam 1 puluhan menambah 10 satuan, bukan 1 satuan.")
sa("c2", "mudah", T, Kn, S3, "Berapakah hasil dari 56 dikurang 23?", "33", "56 - 23 = 33.", verifikasi={"ekspresi": "56 - 23", "hasil": "33"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Berapakah hasil dari 53 dikurang 27?", ["26", "36", "25", "27"], "A", "13 - 7 = 6; 4 - 2 = 2. Hasil 26.", "Lupa mengurangi puluhan yang dipinjam", verifikasi={"ekspresi": "53 - 27", "hasil": "26"})
mc("c3", "sedang", R, Pr, S4, "Toko punya 62 telur, pecah 19 butir. Berapa sisa telur utuh?", ["43 butir", "53 butir", "42 butir", "44 butir"], "A", "62 - 19 = 43 butir.", "Keliru saat meminjam pada soal cerita", verifikasi={"ekspresi": "62 - 19", "hasil": "43"})

# Terarah (6): S1, S2, S3, S4, S2, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berapakah hasil dari 68 dikurang 34 secara bersusun?", ["34", "33", "35", "32"], "A", "68 - 34 = 34.", verifikasi={"ekspresi": "68 - 34", "hasil": "34"})
mc("c3", "mudah", T, Pr, S2, "Pada 74 - 38, setelah meminjam, angka 4 menjadi ....", ["14", "13", "15", "16"], "A", "10 + 4 = 14.")
tf("c3", "sedang", T, Pr, S3, "Hasil pengurangan 63 dikurang 28 adalah 35.", "Benar", "13 - 8 = 5; 5 - 2 = 3. Hasil 35.")
mc("c3", "sedang", T, Pr, S4, "Pak Dani panen 75 kelapa, terjual 38 kelapa. Berapa sisa kelapa?", ["37 kelapa", "47 kelapa", "36 kelapa", "38 kelapa"], "A", "75 - 38 = 37 kelapa.", verifikasi={"ekspresi": "75 - 38", "hasil": "37"})
tf("c3", "sedang", T, Pr, S1, "Mengurangkan 85 - 32 bersusun dimulai dari angka puluhan.", "Salah", "Selalu mulai dari angka satuan.")
sa("c3", "sedang", T, Pr, S3, "Berapakah hasil dari 71 dikurang 36?", "35", "11 - 6 = 5; 6 - 3 = 3. Hasil 35.", verifikasi={"ekspresi": "71 - 36", "hasil": "35"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Berapakah hasil dari 79 dikurang 45 bersusun?", ["34", "33", "35", "32"], "A", "79 - 45 = 34.", verifikasi={"ekspresi": "79 - 45", "hasil": "34"})
mc("c3", "sedang", X, Pr, S3, "Berapakah hasil dari 64 dikurang 29?", ["35", "45", "34", "36"], "A", "14 - 9 = 5; 5 - 2 = 3. Hasil 35.", verifikasi={"ekspresi": "64 - 29", "hasil": "35"})
tf("c3", "sedang", X, Pr, S2, "Pada 82 - 45, angka 8 dicoret dan berubah menjadi 7.", "Benar", "Karena dipinjam 1 puluhan, maka 8 menjadi 7.")
sa("c3", "sedang", X, Pr, S4, "Sebuah bus berisi 54 penumpang, turun 27 orang. Berapa sisa penumpang?", "27", "54 - 27 = 27 orang.", verifikasi={"ekspresi": "54 - 27", "hasil": "27"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Pada 85 - 48, berapa hasil pengurangan angka satuannya?", ["7", "6", "8", "9"], "A", "15 - 8 = 7.", verifikasi={"ekspresi": "15 - 8", "hasil": "7"})
mc("c3", "sedang", K, Pr, S3, "Berapakah hasil dari 73 dikurang 46?", ["27", "37", "28", "26"], "A", "73 - 46 = 27.", verifikasi={"ekspresi": "73 - 46", "hasil": "27"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S3
mc("c4", "sedang", T, Kn, S1, "Rudi menghitung 52 - 7 dengan menulis 7 di bawah 5. Kesalahan Rudi adalah ....", ["7 adalah satuan harus lurus dengan 2", "7 harus ditulis dua kali", "kurang tanda kurang", "tidak ada salah"], "A", "Satuan harus lurus dengan satuan (angka 2).")
mc("c4", "sedang", T, Kn, S2, "Pada 60 - 24, bagaimana cara mengurangkan angka satuannya?", ["pinjam 1 puluhan dari 6 sehingga 0 menjadi 10", "kurangkan saja 4 - 0", "hasilnya selalu 0", "tidak bisa dihitung"], "A", "0 pinjam 1 puluhan menjadi 10, lalu 10 - 4 = 6.")
tf("c4", "sedang", T, Kn, S3, "Hasil pengurangan 82 - 37 sama dengan 75 - 30.", "Benar", "82 - 37 = 45, dan 75 - 30 = 45. Keduanya sama.")
tf("c4", "sedang", T, Kn, S4, "Paman punya 81 ayam, dijual 45 ayam. Sisa ayam paman adalah 46 ayam.", "Salah", "81 - 45 = 36 ayam, bukan 46 ayam.")
sa("c4", "sedang", T, Kn, S4, "Koperasi punya 83 buku, terjual 49 buku. Berapa sisa buku?", "34", "83 - 49 = 34 buku.", verifikasi={"ekspresi": "83 - 49", "hasil": "34"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S3, "Edo menghitung 74 - 38 dan mendapat 46. Mengapa jawaban Edo salah?", ["Edo lupa mengurangi angka 7 menjadi 6 setelah meminjam", "Edo salah menghitung satuan", "Edo menjumlahkan kedua bilangan", "jawaban Edo sudah benar"], "A", "Edo lupa mencoret 7 jadi 6. Hasil yang benar adalah 36.")
mc("c4", "sedang", X, Kn, S4, "Perpustakaan punya 92 majalah, dipinjam murid 58 majalah. Sisa majalah?", ["34 majalah", "44 majalah", "35 majalah", "33 majalah"], "A", "92 - 58 = 34 majalah.", verifikasi={"ekspresi": "92 - 58", "hasil": "34"})
tf("c4", "sedang", X, Kn, S1, "Pada pengurangan 98 - 45, kita perlu menggunakan teknik meminjam.", "Salah", "8 lebih besar dari 5, jadi tidak perlu meminjam.")
mc("c4", "sulit", X, Me, S3, "Berapakah hasil dari 91 dikurang 47?", ["44", "54", "45", "43"], "A", "91 - 47 = 44.", verifikasi={"ekspresi": "91 - 47", "hasil": "44"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Pada pengurangan 90 - 36, setelah dipinjam 1 puluhan, angka puluhan 9 menjadi ....", ["8", "7", "9", "6"], "A", "9 berkurang 1 menjadi 8.")
mc("c4", "sulit", K, Me, S3, "Berapakah hasil pengurangan bersusun 84 dikurang 39?", ["45", "55", "46", "44"], "A", "84 - 39 = 45.", verifikasi={"ekspresi": "84 - 39", "hasil": "45"})
tf("c4", "sulit", K, Me, S4, "Jika Siti punya 72 permen dan dibagikan 38 permen, sisanya kurang dari 30.", "Salah", "72 - 38 = 34 permen. 34 lebih dari 30.")
mc("c4", "sulit", K, Me, S4, "Sebuah bioskop punya 95 kursi, terisi 58 penonton. Berapa kursi kosong?", ["37 kursi", "47 kursi", "38 kursi", "36 kursi"], "A", "95 - 58 = 37 kursi.", verifikasi={"ekspresi": "95 - 58", "hasil": "37"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Pengurangan bersusun berikut yang menghasilkan nilai 38 adalah ....", ["72 - 34", "70 - 30", "85 - 45", "65 - 25"], "A", "72 - 34 = 38.")
mc("c5", "sedang", T, Me, S2, "Jika 72 - 3B = 35, berapakah nilai angka satuan B?", ["7", "6", "8", "5"], "A", "72 - 35 = 37, jadi B = 7.", verifikasi={"ekspresi": "72 - 35 - 30", "hasil": "7"})
mc("c5", "sedang", T, Me, S3, "Berapakah hasil dari 93 dikurang 56?", ["37", "47", "38", "36"], "A", "93 - 56 = 37.", verifikasi={"ekspresi": "93 - 56", "hasil": "37"})
mc("c5", "sulit", T, Me, S4, "Pak guru punya 86 lembar kertas gambar, dibagikan 49 lembar. Berapa sisa kertas?", ["37 lembar", "47 lembar", "38 lembar", "36 lembar"], "A", "86 - 49 = 37 lembar.", verifikasi={"ekspresi": "86 - 49", "hasil": "37"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Berapakah hasil dari 82 dikurang 47?", ["35", "45", "36", "34"], "A", "82 - 47 = 35.", verifikasi={"ekspresi": "82 - 47", "hasil": "35"})
mc("c5", "sulit", K, Me, S4, "Di kolam ada 94 ikan, dipancing 48 ikan. Berapa sisa ikan di kolam?", ["46 ikan", "56 ikan", "47 ikan", "45 ikan"], "A", "94 - 48 = 46 ikan.", verifikasi={"ekspresi": "94 - 48", "hasil": "46"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S3, "Beni menghitung 61 - 25 dan mendapat 44 karena menghitung 5 - 1. Apa saranmu?", ["angka atas harus dikurang bawah bukan dibalik jika kurang harus pinjam", "jawaban Beni sudah tepat", "kurangkan saja puluhannya", "tambahkan kedua angka"], "A", "Satuan atas (1) harus meminjam dari puluhan menjadi 11 - 5 = 6, bukan dibalik 5 - 1.")
mc("c6", "sulit", K, Me, S4, "Ada 80 butir kelereng, diberikan 36 butir ke adik. Bagaimana langkah terbaik menghitungnya?", ["pinjam 1 puluhan dari 8 menjadi 10 satuan lalu 10 - 6 = 4 dan 7 - 3 = 4", "kurangkan 6 dari 0 dapat 6", "hitung mundur 36 kali", "tebak hasilnya 50"], "A", "Meminjam 1 puluhan dari angka 8 membuat satuan menjadi 10 sehingga 80 - 36 = 44.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Berapakah hasil dari 100 dikurang 45 secara bertahap?", ["55", "45", "65", "50"], "A", "100 - 40 = 60; 60 - 5 = 55.", verifikasi={"ekspresi": "100 - 45", "hasil": "55"})
mc("c6", "sulit", P, Me, S4, "Pak Lurah punya 90 bibit pohon, ditanam 37 bibit lalu ditanam lagi 28 bibit. Sisa bibit?", ["25 bibit", "35 bibit", "24 bibit", "26 bibit"], "A", "37 + 28 = 65; 90 - 65 = 25 bibit.", verifikasi={"ekspresi": "90 - (37 + 28)", "hasil": "25"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab40_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab40.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")

