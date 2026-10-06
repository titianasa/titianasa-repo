#!/usr/bin/env python3
"""
Generator dan validator Bab 39 Matematika Kelas 2 SD:
"Penjumlahan Bersusun dengan Teknik Menyimpan" (Fase A)
bab_id: 2048821c-5857-4fac-842b-b260b885851d
article_id: 120b0d9a-98a3-41a6-8a15-f838fe93bd8c
quiz_id: d4ec033f-c6b0-4db9-98aa-8eb284037c44
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "e5f6a7b8c901"  # Menulis Bersusun Lurus Nilai Tempat
S2 = "f6a7b8c9d002"  # Konsep Menyimpan Satuan ke Puluhan
S3 = "a7b8c9d0e103"  # Langkah Penjumlahan Bersusun Menyimpan
S4 = "b8c9d0e1f204"  # Menyelesaikan Soal Cerita Bersusun

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Menjumlah bilangan besar lebih mudah bersusun.
Tuliskan bilangan atas dan bawah.
Satuan harus lurus dengan satuan.
Puluhan harus lurus dengan puluhan.
Garis bawah dibuat dengan tanda tambah.
Selalu mulai hitung dari satuan.
Setelah satuan, baru hitung puluhan.
Urutan ini sangat penting diperhatikan.

:::definition
title: Penjumlahan Bersusun
Penjumlahan bersusun adalah susunan bilangan lurus ke bawah sesuai nilai tempatnya.
:::"""

s2_content = """Kadang satuan dijumlahkan melebihi sembilan.
Misalnya delapan ditambah lima.
Hasil delapan tambah lima adalah tiga belas.
Tiga belas memiliki satu puluhan.
Tiga belas memiliki tiga satuan.
Tuliskan angka tiga pada satuan.
Simpanlah angka satu pada puluhan.
Simpanan ini bernilai satu puluhan.

:::steps
title: Aturan Menyimpan
1. Hitung jumlah kolom satuan.
2. Jika hasilnya sepuluh atau lebih, simpan satu puluhan.
3. Tulis angka satuan di bawah.
:::"""

s3_content = """Mari coba hitung tiga puluh delapan tambah dua puluh lima.
Tuliskan tiga puluh delapan di atas.
Tuliskan dua puluh lima di bawah.
Hitung satuan delapan tambah lima.
Delapan tambah lima jadi tiga belas.
Tulis tiga, simpan satu puluhan.
Hitung puluhan satu tambah tiga tambah dua.
Hasil puluhan adalah enam.
Maka jawabannya enam puluh tiga!"""

s4_content = """Ayo gunakan dalam soal cerita.
Rani punya tiga puluh tujuh pensil.
Ayah membelikan delapan belas pensil lagi.
Tiga puluh tujuh tambah delapan belas.
Tujuh tambah delapan sama dengan lima belas.
Tulis lima, simpan angka satu.
Satu tambah tiga tambah satu jadi lima.
Semua pensil ada lima puluh lima.

:::common_trap
title: Lupa Menambahkan Simpanan
Banyak anak lupa angka simpanan.
Angka satu simpanan harus dijumlahkan.
Jangan sampai tertinggal saat menghitung puluhan!
:::

:::callout
variant: summary
title: Ringkasan
text: Tulis bilangan lurus nilai tempat. Hitung mulai dari satuan. Jangan lupa tambahkan angka simpanan pada puluhan.
:::"""

sections = [
    {
        "id": S1,
        "title": "Menulis Bersusun Lurus Nilai Tempat",
        "minutes": 6,
        "goal": "Siswa mampu menyusun dua bilangan dua angka sejajar lurus menurut satuan dan puluhannya.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Konsep Menyimpan Satuan ke Puluhan",
        "minutes": 6,
        "goal": "Siswa memahami bahwa bila satuan berjumlah 10 atau lebih, 1 puluhan disimpan ke nilai tempat puluhan.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Langkah Penjumlahan Bersusun Menyimpan",
        "minutes": 6,
        "goal": "Siswa mampu menyelesaikan penjumlahan bersusun pendek dengan satu kali menyimpan secara berurutan dan benar.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menyelesaikan Soal Cerita Bersusun",
        "minutes": 6,
        "goal": "Siswa mampu menerapkan penjumlahan bersusun dengan teknik menyimpan untuk menyelesaikan soal cerita kontekstual.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Penjumlahan Bersusun dengan Teknik Menyimpan",
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
# 2. DEFINISI BANK 50 SOAL BAB 39
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
mc("c1", "mudah", D, F, S1, "Saat menjumlahkan bersusun, bagian yang dihitung pertama kali adalah ....", ["satuan", "puluhan", "ratusan", "bebas"], "A", "Penjumlahan bersusun selalu dimulai dari kolom satuan.")
tf("c1", "mudah", D, F, S2, "Angka 14 terdiri dari 4 puluhan dan 1 satuan.", "Salah", "14 terdiri dari 1 puluhan dan 4 satuan, bukan sebaliknya.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Posisi angka satuan pada penjumlahan bersusun diletakkan lurus dengan ....", ["satuan", "puluhan", "garis", "tanda tambah"], "A", "Nilai tempat yang sama harus lurus ke bawah.")
mc("c1", "mudah", T, F, S3, "Berapakah hasil dari 23 ditambah 14?", ["37", "36", "38", "35"], "A", "23 + 14 = 37 (tanpa menyimpan).", verifikasi={"ekspresi": "23 + 14", "hasil": "37"})
sa("c1", "mudah", T, F, S2, "Pada angka 16, berapakah nilai angka yang disimpan ke puluhan?", "1", "16 = 1 puluhan disimpan dan 6 satuan ditulis.")

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Jika satuan dijumlahkan menghasilkan 12, angka yang ditulis di bawah adalah ....", ["2", "1", "12", "3"], "A", "Tulis angka satuan 2 di bawah, lalu simpan 1 di atas kolom puluhan.", "Tertukar antara angka yang ditulis dan angka yang disimpan")
tf("c2", "mudah", D, Kn, S3, "Pada 28 + 15, jumlah satuan 8 + 5 memerlukan teknik menyimpan.", "Benar", "8 + 5 = 13 (lebih dari 9, jadi menyimpan 1 puluhan).")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Mengapa angka 1 disimpan di atas kolom puluhan?", ["karena nilainya adalah 1 puluhan", "karena angkanya kecil", "karena tidak muat", "karena hiasan"], "A", "Hasil satuan 10 atau lebih bernilai 1 puluhan yang ditambahkan ke puluhan.", "Tidak mengerti konsep nilai tempat simpanan")
mc("c2", "mudah", R, Kn, S3, "Berapakah hasil dari 25 ditambah 18?", ["43", "33", "42", "44"], "A", "5 + 8 = 13 (tulis 3 simpan 1); 1 + 2 + 1 = 4 puluhan. Hasil 43.", "Lupa menambahkan angka 1 simpanan pada puluhan", verifikasi={"ekspresi": "25 + 18", "hasil": "43"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Tulis 45 di atas dan 23 di bawah. Angka 5 lurus dengan angka ....", ["3", "2", "4", "0"], "A", "Angka 5 dan 3 sama-sama satuan sehingga harus lurus.")
mc("c2", "mudah", T, Kn, S4, "Ibu membeli 26 telur lalu membeli 17 telur lagi. Ini diselesaikan dengan cara ....", ["penjumlahan", "pengurangan", "pembagian", "pengukuran"], "A", "Membeli lagi berarti jumlah telur bertambah.")
tf("c2", "mudah", T, Kn, S2, "Jika penjumlahan satuan menghasilkan 8, kita harus menyimpan 1 puluhan.", "Salah", "Jika satuan kurang dari 10, tidak ada yang disimpan.")
sa("c2", "mudah", T, Kn, S3, "Berapakah hasil dari 34 ditambah 25?", "59", "34 + 25 = 59.", verifikasi={"ekspresi": "34 + 25", "hasil": "59"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Berapakah hasil dari 47 ditambah 26?", ["73", "63", "74", "72"], "A", "7 + 6 = 13 (tulis 3 simpan 1); 1 + 4 + 2 = 7. Jadi 73.", "Lupa menjumlahkan angka simpanan pada puluhan", verifikasi={"ekspresi": "47 + 26", "hasil": "73"})
mc("c3", "sedang", R, Pr, S4, "Budi punya 39 kelereng dan adik punya 15 kelereng. Berapa jumlahnya?", ["54 kelereng", "44 kelereng", "55 kelereng", "53 kelereng"], "A", "39 + 15 = 54 kelereng.", "Keliru menjumlahkan satuan yang menyimpan", verifikasi={"ekspresi": "39 + 15", "hasil": "54"})

# Terarah (6): S1, S2, S3, S4, S2, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berapakah hasil dari 41 ditambah 32 secara bersusun?", ["73", "72", "74", "71"], "A", "41 + 32 = 73.", verifikasi={"ekspresi": "41 + 32", "hasil": "73"})
mc("c3", "mudah", T, Pr, S2, "Hasil 9 + 7 adalah 16. Berapa angka yang disimpan ke puluhan?", ["1", "6", "9", "7"], "A", "Tulis 6 pada satuan, simpan 1 pada puluhan.")
tf("c3", "sedang", T, Pr, S3, "Hasil penjumlahan bersusun 36 + 27 adalah 63.", "Benar", "6 + 7 = 13 (tulis 3 simpan 1); 1 + 3 + 2 = 6. Hasil 63.")
mc("c3", "sedang", T, Pr, S4, "Di perpustakaan ada 48 buku cerita dan 25 buku sains. Berapa totalnya?", ["73 buku", "63 buku", "74 buku", "72 buku"], "A", "48 + 25 = 73 buku.", verifikasi={"ekspresi": "48 + 25", "hasil": "73"})
tf("c3", "sedang", T, Pr, S1, "Menjumlahkan 52 + 13 bersusun dimulai dari angka puluhan dulu.", "Salah", "Selalu mulai dari angka satuan.")
sa("c3", "sedang", T, Pr, S3, "Berapakah hasil dari 58 ditambah 24?", "82", "8 + 4 = 12 (simpan 1); 1 + 5 + 2 = 8. Jadi 82.", verifikasi={"ekspresi": "58 + 24", "hasil": "82"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Berapakah hasil dari 35 ditambah 42 bersusun?", ["77", "76", "78", "75"], "A", "35 + 42 = 77.", verifikasi={"ekspresi": "35 + 42", "hasil": "77"})
mc("c3", "sedang", X, Pr, S3, "Berapakah hasil dari 29 ditambah 38?", ["67", "57", "68", "66"], "A", "29 + 38 = 67.", verifikasi={"ekspresi": "29 + 38", "hasil": "67"})
tf("c3", "sedang", X, Pr, S2, "Pada penjumlahan 17 + 25, angka satuan yang ditulis adalah 2.", "Benar", "7 + 5 = 12, maka angka 2 ditulis pada satuan.")
sa("c3", "sedang", X, Pr, S4, "Kandang A ada 37 ayam, kandang B ada 26 ayam. Berapa semua ayam?", "63", "37 + 26 = 63 ayam.", verifikasi={"ekspresi": "37 + 26", "hasil": "63"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Berapakah hasil dari 44 ditambah 37?", ["81", "71", "82", "80"], "A", "44 + 37 = 81.", verifikasi={"ekspresi": "44 + 37", "hasil": "81"})
mc("c3", "sedang", K, Pr, S3, "Berapakah hasil dari 56 ditambah 29?", ["85", "75", "86", "84"], "A", "56 + 29 = 85.", verifikasi={"ekspresi": "56 + 29", "hasil": "85"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S3
mc("c4", "sedang", T, Kn, S1, "Doni menjumlahkan 25 + 4 dengan menyusun 4 di bawah 2. Kesalahan Doni adalah ....", ["angka 4 adalah satuan harus lurus dengan 5", "angka 4 harus di atas", "kurang tanda tambah", "tidak ada yang salah"], "A", "4 adalah satuan, maka harus lurus dengan satuan (angka 5).")
mc("c4", "sedang", T, Kn, S2, "Jika sebuah penjumlahan bersusun menyimpan 1 puluhan, maka jumlah satuannya pasti ....", ["10 atau lebih", "kurang dari 10", "selalu 0", "angka ganjil saja"], "A", "Menyimpan terjadi hanya bila hasil satuan bernilai 10 atau lebih.")
tf("c4", "sedang", T, Kn, S3, "Hasil dari 38 + 27 bernilai sama dengan 45 + 20.", "Benar", "38 + 27 = 65, dan 45 + 20 = 65. Keduanya sama.")
tf("c4", "sedang", T, Kn, S4, "Sebuah toko punya 46 roti, datang lagi 29 roti. Total roti adalah 65.", "Salah", "46 + 29 = 75 roti, bukan 65.")
sa("c4", "sedang", T, Kn, S4, "Siti menanam 28 bunga mawar dan 35 bunga melati. Berapa total bunga?", "63", "28 + 35 = 63 bunga.", verifikasi={"ekspresi": "28 + 35", "hasil": "63"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S3, "Andi menghitung 48 + 37 dan mendapat jawaban 75. Mengapa Andi salah?", ["Andi lupa menambahkan 1 puluhan simpanan", "Andi salah menjumlah satuan", "Andi mengurangkan bilangan", "jawaban Andi sudah benar"], "A", "8 + 7 = 15; 1 + 4 + 3 = 8 puluhan. Jawabannya 85, Andi mendapat 75 karena lupa simpanan.")
mc("c4", "sedang", X, Kn, S4, "Pak Tani memanen 36 semangka di pagi hari dan 47 semangka di sore hari. Total panen?", ["83 semangka", "73 semangka", "84 semangka", "82 semangka"], "A", "36 + 47 = 83 semangka.", verifikasi={"ekspresi": "36 + 47", "hasil": "83"})
tf("c4", "sedang", X, Kn, S1, "Pada 50 + 38 bersusun, satuan 0 + 8 menghasilkan simpanan ke puluhan.", "Salah", "0 + 8 = 8, tidak ada yang disimpan.")
mc("c4", "sulit", X, Me, S3, "Berapakah hasil dari 67 ditambah 28?", ["95", "85", "96", "94"], "A", "67 + 28 = 95.", verifikasi={"ekspresi": "67 + 28", "hasil": "95"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Pada penjumlahan 59 + 24, langkah yang benar setelah 9 + 4 = 13 adalah ....", ["tulis 3 di satuan lalu simpan 1 di puluhan", "tulis 13 di satuan", "tulis 1 di satuan", "hapus angka 1"], "A", "Tulis 3 pada satuan, simpan 1 di atas kolom puluhan.")
mc("c4", "sulit", K, Me, S3, "Berapakah hasil dari 49 ditambah 49?", ["98", "88", "99", "97"], "A", "49 + 49 = 98.", verifikasi={"ekspresi": "49 + 49", "hasil": "98"})
tf("c4", "sulit", K, Me, S4, "Jika Siti punya 38 stiker dan Lani punya 47 stiker, stiker mereka lebih dari 80.", "Benar", "38 + 47 = 85 stiker. 85 lebih dari 80.")
mc("c4", "sulit", K, Me, S4, "Sebuah bus berisi 37 orang, naik lagi 28 orang. Berapa orang sekarang?", ["65 orang", "55 orang", "66 orang", "64 orang"], "A", "37 + 28 = 65 orang.", verifikasi={"ekspresi": "37 + 28", "hasil": "65"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Operasi penjumlahan bersusun berikut yang menghasilkan nilai 72 adalah ....", ["48 + 24", "45 + 25", "50 + 20", "38 + 33"], "A", "48 + 24 = 72.")
mc("c5", "sedang", T, Me, S2, "Jika 37 + 2B = 63, berapakah angka satuan B yang tepat?", ["6", "5", "7", "4"], "A", "63 - 37 = 26, jadi B = 6.", verifikasi={"ekspresi": "63 - 37 - 20", "hasil": "6"})
mc("c5", "sedang", T, Me, S3, "Berapakah hasil penjumlahan 55 ditambah 38?", ["93", "83", "94", "92"], "A", "55 + 38 = 93.", verifikasi={"ekspresi": "55 + 38", "hasil": "93"})
mc("c5", "sulit", T, Me, S4, "Di rak buku ada 45 majalah dan 39 komik. Berapa jumlah majalah dan komik?", ["84 buah", "74 buah", "85 buah", "83 buah"], "A", "45 + 39 = 84 buah.", verifikasi={"ekspresi": "45 + 39", "hasil": "84"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Berapakah hasil penjumlahan bersusun dari 58 ditambah 36?", ["94", "84", "95", "93"], "A", "58 + 36 = 94.", verifikasi={"ekspresi": "58 + 36", "hasil": "94"})
mc("c5", "sulit", K, Me, S4, "Paman memetik 48 jeruk dan bibi memetik 45 jeruk. Berapa total jeruk dipetik?", ["93 jeruk", "83 jeruk", "94 jeruk", "92 jeruk"], "A", "48 + 45 = 93 jeruk.", verifikasi={"ekspresi": "48 + 45", "hasil": "93"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S3, "Riko menghitung 37 + 28 bersusun dan menulis 515. Apa saran terbaik untuk Riko?", ["satuan 15 harus disimpan 1 puluhannya ke kolom puluhan", "hasil Riko sudah benar", "kurangkan saja angkanya", "jangan pakai bersusun"], "A", "Riko menulis 15 langsung di bawah. Harusnya tulis 5 simpan 1, hasil 65.")
mc("c6", "sulit", K, Me, S4, "Dua kelompok pramuka beranggotakan 38 orang dan 47 orang. Bagaimana cara termudah menghitungnya?", ["hitung bersusun 38 + 47 dengan menyimpan 1 puluhan", "hitung mundur dari 100", "tebak nilainya", "kurangkan anggotanya"], "A", "Penjumlahan bersusun dengan teknik menyimpan adalah cara terstruktur dan akurat.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Berapakah hasil dari 26 + 37 + 19 jika dijumlahkan bertahap?", ["82", "72", "83", "81"], "A", "26 + 37 = 63; 63 + 19 = 82.", verifikasi={"ekspresi": "26 + 37 + 19", "hasil": "82"})
mc("c6", "sulit", P, Me, S4, "Pak RT menyiapkan 28 kursi merah, 34 kursi biru, dan 29 kursi hijau. Berapa kursi?", ["91 kursi", "81 kursi", "92 kursi", "90 kursi"], "A", "28 + 34 = 62; 62 + 29 = 91 kursi.", verifikasi={"ekspresi": "28 + 34 + 29", "hasil": "91"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab39_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab39.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
