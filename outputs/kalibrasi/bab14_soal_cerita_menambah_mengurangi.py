#!/usr/bin/env python3
"""
Generator dan validator Bab 14 Matematika Kelas 1 SD:
"Soal Cerita Bergambar: Menambah dan Mengurangi" (Fase A)
bab_id: e88e9977-ea2b-4b9a-8f41-f988cf3a1cfc
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "d3e2f11a4b23"  # Memahami Cerita Penjumlahan (Membeli, Diberi, Datang)
S2 = "e4f3a22b5c34"  # Memahami Cerita Pengurangan (Dimakan, Rusak, Pergi)
S3 = "f5a4b33c6d45"  # Menentukan Operasi Hitung yang Tepat dari Cerita
S4 = "a6b5c44d7e56"  # Menulis Kalimat Matematika dan Menjawab Soal Cerita

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Soal cerita menceritakan kejadian sehari-hari.
Ada kata kunci untuk penjumlahan.
Contohnya membeli lagi, diberi, atau datang.
Kata-kata itu membuat benda bertambah.
Beni punya 4 pensil.
Ayah memberi 3 pensil lagi.
Pensil Beni menjadi bertambah banyak.
Semua pensil digabungkan lalu dihitung.

:::definition
title: Kata Kunci Penjumlahan
Kata seperti membeli lagi, diberi, datang, dan digabung menunjukkan penjumlahan (+).
:::"""

s2_content = """Ada juga kata kunci pengurangan.
Benda berkurang jika dimakan atau hilang.
Benda juga berkurang jika pecah atau pergi.
Siti punya 6 balon.
Dua balon meletus karena panas.
Balon Siti menjadi lebih sedikit.
Sisa balon dihitung dengan teliti.
Balon utuh tersisa 4 buah.

:::steps
title: Menemukan Sisa Benda
1. Cari banyak benda mula-mula.
2. Cari banyak benda yang hilang atau rusak.
3. Kurangkan bilangan mula-mula dengan benda hilang.
:::"""

s3_content = """Bacalah cerita dengan cermat.
Tentukan apakah benda bertambah atau berkurang.
Jika bertambah, gunakan tanda tambah (+).
Jika berkurang, gunakan tanda kurang (-).
Jangan terburu-buru menebak operasi hitung.
Pahami maksud kejadian dalam cerita.
Perhatikan kata kunci yang ada."""

s4_content = """Ubah cerita menjadi kalimat matematika.
Ada 5 burung di pohon.
Tiga burung terbang pergi.
Kalimat matematikanya adalah $5 - 3 = 2$.
Jadi sisa burung ada 2 ekor.
Tuliskan jawaban lengkap dengan satuannya.

:::common_trap
title: Terjebak Kata Tanpa Memahami Cerita
Jangan hanya melihat angka lalu langsung menjumlahkan.
Pahami kejadiannya bertambah atau berkurang.
Jika benda pergi atau hilang, harus dikurangkan.
:::

:::callout
variant: summary
title: Ringkasan
text: Soal cerita diselesaikan dengan kata kunci. Bertambah pakai (+), berkurang pakai (-).
:::"""

sections = [
    {
        "id": S1,
        "title": "Cerita Penjumlahan Bertambah",
        "minutes": 6,
        "goal": "Siswa dapat mengidentifikasi konteks penjumlahan dalam soal cerita bergambar.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Cerita Pengurangan Berkurang",
        "minutes": 6,
        "goal": "Siswa dapat mengidentifikasi konteks pengurangan dalam soal cerita bergambar.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Menentukan Operasi Tambah atau Kurang",
        "minutes": 6,
        "goal": "Siswa dapat memilih operasi hitung (+ atau -) yang sesuai dengan alur soal cerita.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menulis Kalimat Matematika Soal Cerita",
        "minutes": 6,
        "goal": "Siswa dapat menyusun kalimat matematika dan menentukan hasil akhir dari soal cerita.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Soal Cerita Bergambar: Menambah dan Mengurangi",
    "topic": "Penjumlahan dan Pengurangan sampai 20",
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
# 2. DEFINISI BANK 50 SOAL BAB 14
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
mc("c1", "mudah", D, F, S1, "Kata 'diberi lagi' dalam cerita menandakan operasi ....", ["penjumlahan", "pengurangan", "perkalian", "pembagian"], "A", "Kata diberi lagi menandakan benda bertambah (penjumlahan).")
tf("c1", "mudah", D, F, S2, "Kata 'dimakan adik' menandakan benda berkurang.", "Benar", "Dimakan berarti benda diambil sehingga berkurang.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Kata manakah yang menandakan benda bertambah?", ["membeli lagi", "hilang", "rusak", "terbang pergi"], "A", "Membeli lagi membuat benda bertambah.")
mc("c1", "mudah", T, F, S2, "Kata manakah yang menandakan pengurangan?", ["pecah", "diberi", "menemukan", "hadiah"], "A", "Benda pecah berarti berkurang.")
sa("c1", "mudah", T, F, S3, "Apa simbol untuk operasi benda bertambah?", "+", "Simbol penjumlahan adalah tanda +.")

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Ada 3 kucing di halaman. Datang 2 kucing lagi. Jumlahnya?", ["5 ekor", "4 ekor", "6 ekor", "3 ekor"], "A", "3 + 2 = 5 kucing.", verifikasi={"ekspresi": "3 + 2", "hasil": "5"})
tf("c2", "mudah", D, Kn, S2, "Ibu punya 6 telur, pecah 2 telur, sisanya 4 butir.", "Benar", "6 - 2 = 4 butir telur.", verifikasi={"ekspresi": "6 - 2", "hasil": "4"})

# Remedial (2)
mc("c2", "mudah", R, F, S3, "Ada 7 balon meletus 2 balon. Operasi hitungnya adalah ....", ["$7 - 2$", "$7 + 2$", "$2 + 7$", "$7 = 2$"], "A", "Meletus artinya berkurang, jadi 7 - 2.", "Salah menentukan operasi hitung pada soal cerita")
mc("c2", "mudah", R, Kn, S4, "Lani punya 5 permen diberi ibu 3 lagi. Kalimat matematikanya?", ["$5 + 3 = 8$", "$5 - 3 = 2$", "$3 + 3 = 6$", "$5 + 5 = 10$"], "A", "Diberi lagi artinya ditambah: 5 + 3 = 8.", "Salah menyusun kalimat matematika soal cerita")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Di kolam ada 4 bebek. Masuk lagi 3 bebek. Berapa semua?", ["7 bebek", "6 bebek", "8 bebek", "5 bebek"], "A", "4 + 3 = 7 bebek.", verifikasi={"ekspresi": "4 + 3", "hasil": "7"})
mc("c2", "mudah", T, Kn, S2, "Ada 8 mangga jatuh 3 buah. Berapa mangga tersisa?", ["5 buah", "4 buah", "6 buah", "7 buah"], "A", "8 - 3 = 5 buah.", verifikasi={"ekspresi": "8 - 3", "hasil": "5"})
tf("c2", "mudah", T, Kn, S3, "Cerita tentang burung terbang pergi memakai operasi tambah.", "Salah", "Burung pergi membuat jumlah berkurang (operasi kurang).")
sa("c2", "mudah", T, Kn, S4, "Ada 4 bunga dipetik 2 bunga. Berapa sisa bunga?", "2", "4 - 2 = 2 bunga.", verifikasi={"ekspresi": "4 - 2", "hasil": "2"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Edo punya 6 kelereng lalu menang 4 kelereng. Totalnya?", ["10 kelereng", "9 kelereng", "8 kelereng", "7 kelereng"], "A", "6 + 4 = 10 kelereng.", "Salah menghitung hasil penjumlahan cerita", verifikasi={"ekspresi": "6 + 4", "hasil": "10"})
mc("c3", "sedang", R, Pr, S2, "Ada 10 apel dimakan ulat 4 apel. Berapa apel utuh?", ["6 apel", "5 apel", "7 apel", "4 apel"], "A", "10 - 4 = 6 apel.", "Salah menghitung sisa pengurangan cerita", verifikasi={"ekspresi": "10 - 4", "hasil": "6"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Siti memetik 5 jeruk lalu memetik 4 jeruk lagi. Jumlahnya?", ["9 jeruk", "8 jeruk", "10 jeruk", "7 jeruk"], "A", "5 + 4 = 9 jeruk.", verifikasi={"ekspresi": "5 + 4", "hasil": "9"})
mc("c3", "sedang", T, Pr, S2, "Di piring ada 9 kue dimakan ayah 3 kue. Sisanya?", ["6 kue", "5 kue", "7 kue", "4 kue"], "A", "9 - 3 = 6 kue.", verifikasi={"ekspresi": "9 - 3", "hasil": "6"})
tf("c3", "sedang", T, Pr, S3, "Ada 8 buku dibeli 2 buku lagi, totalnya 10 buku.", "Benar", "8 + 2 = 10 buku.", verifikasi={"ekspresi": "8 + 2", "hasil": "10"})
mc("c3", "sedang", T, Pr, S4, "Kalimat matematika untuk 7 burung terbang 3 ekor adalah ....", ["$7 - 3 = 4$", "$7 + 3 = 10$", "$3 + 4 = 7$", "$7 - 4 = 3$"], "A", "Mula-mula 7 lalu terbang 3: 7 - 3 = 4.")
tf("c3", "sedang", T, Pr, S1, "Punya 5 pensil dibelikan 3 pensil jumlahnya 7 pensil.", "Salah", "5 + 3 = 8 pensil, bukan 7 pensil.")
sa("c3", "mudah", T, Pr, S2, "Ada 10 biskuit dimakan 6 biskuit. Berapa sisanya?", "4", "10 - 6 = 4 biskuit.", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Di pohon ada 6 monyet. Datang lagi 5 monyet. Jumlahnya?", ["11 monyet", "10 monyet", "12 monyet", "9 monyet"], "A", "6 + 5 = 11 monyet.", verifikasi={"ekspresi": "6 + 5", "hasil": "11"})
mc("c3", "sedang", X, Pr, S2, "Ada 12 roti dibagikan 4 roti. Berapa sisa roti?", ["8 roti", "7 roti", "9 roti", "6 roti"], "A", "12 - 4 = 8 roti.", verifikasi={"ekspresi": "12 - 4", "hasil": "8"})
tf("c3", "sedang", X, Pr, S3, "Cerita 'menemukan kelereng' diselesaikan dengan tanda kurang.", "Salah", "Menemukan kelereng berarti kelereng bertambah (tanda tambah).")
sa("c3", "sedang", X, Pr, S4, "Beni punya 14 perangko hilang 4. Berapa sisanya?", "10", "14 - 4 = 10 perangko.", verifikasi={"ekspresi": "14 - 4", "hasil": "10"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Ada 8 ikan di akuarium dibeli lagi 7 ikan. Totalnya?", ["15 ikan", "14 ikan", "16 ikan", "13 ikan"], "A", "8 + 7 = 15 ikan.", verifikasi={"ekspresi": "8 + 7", "hasil": "15"})
mc("c3", "sedang", K, Pr, S2, "Ada 15 manggis busuk 5 buah. Berapa manggis bagus?", ["10 buah", "9 buah", "11 buah", "8 buah"], "A", "15 - 5 = 10 buah.", verifikasi={"ekspresi": "15 - 5", "hasil": "10"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Cerita manakah yang kalimat matematikanya $6 + 3 = 9$?", ["punya 6 kue diberi 3 kue lagi", "punya 9 kue dimakan 3 kue", "punya 6 kue dimakan 3 kue", "punya 3 kue dimakan 6 kue"], "A", "Diberi lagi artinya ditambah: 6 + 3 = 9.")
mc("c4", "sedang", T, Kn, S2, "Cerita manakah yang kalimat matematikanya $10 - 4 = 6$?", ["ada 10 burung terbang 4 ekor", "ada 6 burung datang 4 ekor", "ada 10 burung datang 4 ekor", "ada 4 burung terbang 6 ekor"], "A", "Terbang artinya berkurang: 10 - 4 = 6.")
tf("c4", "sedang", T, Kn, S3, "Menghitung sisa benda selalu menggunakan operasi pengurangan.", "Benar", "Sisa dihitung dari benda awal dikurang benda yang hilang/diambil.")
tf("c4", "sedang", T, Kn, S4, "Kalimat $8 + 4 = 12$ cocok untuk cerita balon pecah.", "Salah", "Balon pecah adalah cerita pengurangan, bukan penjumlahan.")
sa("c4", "sedang", T, Kn, S4, "Ada 13 permen dimakan adik hingga sisa 9. Berapa dimakan?", "4", "13 - 9 = 4 permen.", verifikasi={"ekspresi": "13 - 9", "hasil": "4"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Manakah kejadian yang menghasilkan benda paling banyak?", ["punya 8 pensil diberi 5 pensil", "punya 10 pensil hilang 2 pensil", "punya 7 pensil diberi 4 pensil", "punya 9 pensil hilang 1 pensil"], "A", "8 + 5 = 13 pensil, paling banyak.")
mc("c4", "sedang", X, Kn, S2, "Cerita A: $15 - 7$. Cerita B: $16 - 8$. Kedua cerita memiliki ....", ["hasil sisa sama", "hasil berbeda", "banyak awal sama", "benda hilang sama"], "A", "15 - 7 = 8 dan 16 - 8 = 8.")
tf("c4", "sedang", X, Kn, S4, "Ada 11 anak bermain, datang 4 anak, jumlahnya 15 anak.", "Benar", "11 + 4 = 15 anak.", verifikasi={"ekspresi": "11 + 4", "hasil": "15"})
mc("c4", "sulit", X, Me, S3, "Mengapa kita harus membaca soal cerita sampai selesai?", ["agar tahu benda bertambah atau berkurang", "agar hafal nama orang di cerita", "karena angkanya selalu berubah", "supaya tidak perlu berhitung"], "A", "Membaca lengkap membantu memahami apakah benda bertambah atau berkurang.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Ada 9 bola di keranjang lalu ditambah 4 bola. Operasi yang tepat?", ["$9 + 4$", "$9 - 4$", "$4 - 9$", "$9 = 4$"], "A", "Ditambah berarti 9 + 4.")
mc("c4", "sulit", K, Me, S2, "Ibu membuat 16 donat. Dimakan keluarga 9 donat. Sisanya?", ["7 donat", "6 donat", "8 donat", "5 donat"], "A", "16 - 9 = 7 donat.", verifikasi={"ekspresi": "16 - 9", "hasil": "7"})
tf("c4", "sulit", K, Me, S3, "Semua soal cerita dengan kata 'ada' pasti merupakan penjumlahan.", "Salah", "Kata 'ada' hanya menyatakan keadaan awal, bukan jenis operasinya.")
mc("c4", "sulit", K, Me, S4, "Beni punya 15 kelereng. Hilang beberapa hingga sisa 8. Berapa hilang?", ["7 kelereng", "6 kelereng", "8 kelereng", "9 kelereng"], "A", "15 - 8 = 7 kelereng.", verifikasi={"ekspresi": "15 - 8", "hasil": "7"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Ada 7 anak bermain. Datang lagi beberapa anak hingga jadi 12. Berapa anak datang?", ["5 anak", "4 anak", "6 anak", "3 anak"], "A", "12 - 7 = 5 anak.", verifikasi={"ekspresi": "12 - 7", "hasil": "5"})
mc("c5", "sedang", T, Me, S2, "Siti punya 14 pita. Diberikan ke adik hingga tersisa 6 pita. Berapa diberikan?", ["8 pita", "7 pita", "9 pita", "6 pita"], "A", "14 - 6 = 8 pita.", verifikasi={"ekspresi": "14 - 6", "hasil": "8"})
mc("c5", "sedang", T, Me, S3, "Apa langkah pertama menyelesaikan soal cerita matematika?", ["memahami apa yang terjadi pada cerita", "langsung menjumlahkan angkanya", "menebak hasil yang paling besar", "menulis sembarang jawaban"], "A", "Memahami alur cerita adalah langkah paling awal.")
mc("c5", "sulit", T, Me, S4, "Ada 18 buku. Dipinjam 5 buku lalu dipinjam 3 buku lagi. Sisa buku?", ["10 buku", "11 buku", "9 buku", "12 buku"], "A", "18 - 5 - 3 = 10 buku.", verifikasi={"ekspresi": "18 - 5 - 3", "hasil": "10"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Toko punya 8 boneka. Masuk kiriman 7 boneka lalu terjual 5 boneka. Berapa boneka sekarang?", ["10 boneka", "9 boneka", "11 boneka", "8 boneka"], "A", "8 + 7 - 5 = 10 boneka.", verifikasi={"ekspresi": "8 + 7 - 5", "hasil": "10"})
mc("c5", "sulit", K, Me, S4, "Di dahan ada 14 burung. Terbang 6 burung lalu datang 3 burung. Berapa burung sekarang?", ["11 burung", "10 burung", "12 burung", "9 burung"], "A", "14 - 6 + 3 = 11 burung.", verifikasi={"ekspresi": "14 - 6 + 3", "hasil": "11"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Susunlah cerita penjumlahan yang menghasilkan total 12 apel!", ["punya 7 apel dibelikan 5 apel lagi", "punya 12 apel dimakan 5 apel", "punya 8 apel dimakan 4 apel", "punya 15 apel dimakan 3 apel"], "A", "7 + 5 = 12 apel.")
mc("c6", "sulit", K, Me, S4, "Buatlah kalimat matematika untuk cerita: 17 kue dimakan 8 kue!", ["$17 - 8 = 9$", "$17 + 8 = 25$", "$8 + 9 = 17$", "$17 - 9 = 8$"], "A", "17 kue dimakan 8 ditulis 17 - 8 = 9.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Rancanglah soal cerita bertingkat dengan operasi $9 + 6 - 5$!", ["10", "9", "11", "8"], "A", "9 + 6 = 15, lalu 15 - 5 = 10.", verifikasi={"ekspresi": "9 + 6 - 5", "hasil": "10"})
mc("c6", "sulit", P, Me, S4, "Susunlah cerita pengurangan dua kali dari 20 yang bersisa 12!", ["punya 20 kue dibagikan 5 lalu dibagikan 3", "punya 20 kue dibagikan 4 lalu dibagikan 2", "punya 20 kue dibagikan 6 lalu dibagikan 4", "punya 20 kue dibagikan 7 lalu dibagikan 2"], "A", "20 - 5 - 3 = 12 kue.")

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab14_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab14.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")

