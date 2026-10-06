#!/usr/bin/env python3
"""
Generator dan validator Bab 15 Matematika Kelas 1 SD:
"Kesalahan Umum: Salah Menghitung Loncatan pada Garis Bilangan" (Fase A)
bab_id: e139db0f-918f-4dc2-926b-819fc18a3fe9
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "b7c6d55e8f67"  # Menghitung Titik vs Menghitung Loncatan
S2 = "c8d7e66f9a78"  # Menentukan Titik Awal Loncatan dengan Tepat
S3 = "d9e8f77a0b89"  # Membedakan Loncatan Maju dan Loncatan Mundur
S4 = "e0f9a88b1c90"  # Menuliskan Operasi Hitung Berdasarkan Gambar Garis Bilangan

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Garis bilangan memuat deretan angka berurutan.
Banyak anak salah saat menghitung.
Mereka menghitung titik bilangan pertama.
Padahal kita harus menghitung loncatannya.
Satu loncatan adalah jarak antartitik.
Lompat satu kali bernilai satu.
Lompat dua kali bernilai dua.
Jangan menghitung titik tempat kita berdiri.

:::definition
title: Menghitung Loncatan
Loncatan adalah jarak perpindahan antartitik.
Bukan banyaknya titik yang disentuh.
:::"""

s2_content = """Mulai melompat dari bilangan yang tepat.
Titik awal adalah angka mula-mula.
Contohnya pada hitungan $4 + 3$.
Kita mulai berdiri tepat di angka 4.
Angka 4 belum dihitung sebagai loncatan.
Dari 4 melompat 3 langkah ke kanan.
Loncatan mendarat di angka 7.
Maka $4 + 3 = 7$.

:::steps
title: Langkah Melompat pada Garis Bilangan
1. Cari titik awal bilangan pertama.
2. Hitung tiap lengkungan loncatan.
3. Lihat angka pada tempat mendarat.
:::"""

s3_content = """Arah loncatan menentukan operasi hitung.
Melompat ke kanan artinya nilai bertambah.
Itu adalah operasi penjumlahan.
Melompat ke kiri artinya nilai berkurang.
Itu adalah operasi pengurangan.
Perhatikan mata panah pada garis.
Panah ke kanan berarti maju.
Panah ke kiri berarti mundur."""

s4_content = """Kita bisa membaca garis bilangan.
Lihat titik awal panah bermula.
Hitung berapa langkah panah melengkung.
Lihat di mana ujung panah berhenti.
Tuliskan kalimat matematika yang sesuai.

:::common_trap
title: Menghitung Titik Awal sebagai Loncatan Pertama
Kesalahan paling sering adalah menghitung titik awal.
Jika mulai di angka 5, jangan katakan satu di angka 5.
Katakan satu saat sudah melompat ke angka 6.
Loncatan dihitung saat kaki berpindah tempat.
:::

:::callout
variant: summary
title: Ringkasan
text: Hitung lengkungan loncatan, bukan titiknya. Ke kanan bertambah (+), ke kiri berkurang (-).
:::"""

sections = [
    {
        "id": S1,
        "title": "Menghitung Loncatan Bukan Titik",
        "minutes": 6,
        "goal": "Siswa dapat membedakan antara menghitung titik bilangan dengan menghitung banyaknya lengkungan loncatan.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Menentukan Titik Awal Loncatan",
        "minutes": 6,
        "goal": "Siswa dapat menetapkan titik awal bilangan tanpa menghitungnya sebagai loncatan pertama.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Arah Loncatan: Maju dan Mundur",
        "minutes": 6,
        "goal": "Siswa dapat mengidentifikasi operasi tambah untuk loncatan ke kanan dan kurang untuk loncatan ke kiri.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Membaca Operasi dari Garis Bilangan",
        "minutes": 6,
        "goal": "Siswa dapat menuliskan kalimat matematika yang benar dari model garis bilangan bergambar.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Salah Menghitung Loncatan pada Garis Bilangan",
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
# 2. DEFINISI BANK 50 SOAL BAB 15
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
mc("c1", "mudah", D, F, S1, "Saat berhitung pada garis bilangan, kita menghitung ....", ["lengkungan loncatan", "titik yang dilewati", "angka yang tertulis", "garis lurus"], "A", "Kita menghitung lengkungan loncatan antartitik.")
tf("c1", "mudah", D, F, S3, "Melompat ke arah kanan artinya menambah.", "Benar", "Loncatan ke kanan pada garis bilangan berarti operasi penjumlahan.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Satu loncatan bernilai berapa langkah?", ["1 langkah", "2 langkah", "0 langkah", "3 langkah"], "A", "Satu loncatan bernilai 1 langkah perpindahan.")
mc("c1", "mudah", T, F, S2, "Titik tempat pertama kali kita berdiri disebut titik ....", ["awal", "akhir", "lompat", "panah"], "A", "Tempat awal berdiri disebut titik awal.")
sa("c1", "mudah", T, F, S3, "Loncatan ke kiri menunjukkan operasi apa?", "pengurangan|kurang", "Loncatan ke kiri menunjukkan operasi pengurangan.")

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Pada penjumlahan $3 + 4$, kita mulai melompat dari angka ....", ["3", "4", "0", "7"], "A", "Titik awal adalah angka 3.", verifikasi={"ekspresi": "3", "hasil": "3"})
tf("c2", "mudah", D, Kn, S1, "Titik awal berdiri sudah dihitung sebagai satu loncatan.", "Salah", "Titik awal belum berpindah tempat, jadi belum ada loncatan.")

# Remedial (2)
mc("c2", "mudah", R, F, S1, "Mengapa titik awal berdiri tidak boleh dihitung satu?", ["karena kaki belum melompat", "karena nilainya nol", "karena angkanya kecil", "karena tidak ada titik"], "A", "Loncatan baru terhitung saat kaki berpindah tempat.", "Menghitung titik awal sebagai loncatan pertama")
mc("c2", "mudah", R, Kn, S3, "Dari angka 5 melompat 2 langkah ke kiri tiba di ....", ["3", "7", "4", "2"], "A", "5 - 2 = 3.", "Salah arah loncatan penjumlahan dan pengurangan", verifikasi={"ekspresi": "5 - 2", "hasil": "3"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Dari angka 2 ke angka 5 terdapat berapa loncatan?", ["3 loncatan", "4 loncatan", "2 loncatan", "5 loncatan"], "A", "5 - 2 = 3 loncatan.", verifikasi={"ekspresi": "5 - 2", "hasil": "3"})
mc("c2", "mudah", T, Kn, S2, "Pada operasi $8 - 3$, kita mulai berdiri di angka ....", ["8", "3", "5", "0"], "A", "Pengurangan dimulai dari bilangan mula-mula yaitu 8.", verifikasi={"ekspresi": "8", "hasil": "8"})
tf("c2", "mudah", T, Kn, S3, "Melompat ke kiri membuat bilangan menjadi lebih kecil.", "Benar", "Arah kiri bernilai semakin kecil (pengurangan).")
sa("c2", "mudah", T, Kn, S4, "Dari angka 6 melompat maju 3 langkah tiba di angka?", "9", "6 + 3 = 9.", verifikasi={"ekspresi": "6 + 3", "hasil": "9"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Beni berdiri di 4 lalu lompat maju 3 kali. Beni tiba di ....", ["7", "6", "8", "5"], "A", "4 + 3 = 7.", "Salah menghitung posisi akhir loncatan", verifikasi={"ekspresi": "4 + 3", "hasil": "7"})
mc("c3", "sedang", R, Pr, S4, "Garis bilangan mulai di 9 lalu mundur 4 langkah. Kalimatnya?", ["$9 - 4 = 5$", "$9 + 4 = 13$", "$4 + 5 = 9$", "$9 - 5 = 4$"], "A", "Mulai 9 mundur 4 adalah 9 - 4 = 5.", "Salah menuliskan kalimat matematika dari garis bilangan")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berapa banyak loncatan dari angka 6 menuju angka 10?", ["4 loncatan", "5 loncatan", "3 loncatan", "6 loncatan"], "A", "10 - 6 = 4 loncatan.", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})
mc("c3", "sedang", T, Pr, S2, "Mulai di angka 7 melompat maju 5 langkah tiba di ....", ["12", "11", "13", "10"], "A", "7 + 5 = 12.", verifikasi={"ekspresi": "7 + 5", "hasil": "12"})
tf("c3", "sedang", T, Pr, S3, "Dari angka 12 melompat mundur 4 langkah tiba di angka 8.", "Benar", "12 - 4 = 8.", verifikasi={"ekspresi": "12 - 4", "hasil": "8"})
mc("c3", "sedang", T, Pr, S4, "Panah mulai dari 5 melompat ke kanan 4 kali. Operasinya adalah ....", ["$5 + 4$", "$5 - 4$", "$4 + 5$", "$4 - 5$"], "A", "Mulai 5 ke kanan 4 adalah 5 + 4.")
tf("c3", "sedang", T, Pr, S1, "Dari angka 3 ke angka 7 ada 5 loncatan.", "Salah", "Ada 7 - 3 = 4 loncatan, bukan 5 loncatan.")
sa("c3", "mudah", T, Pr, S2, "Dari angka 15 mundur 5 langkah tiba di angka berapa?", "10", "15 - 5 = 10.", verifikasi={"ekspresi": "15 - 5", "hasil": "10"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Dari angka 8 ke angka 14 terdapat berapa loncatan?", ["6 loncatan", "5 loncatan", "7 loncatan", "8 loncatan"], "A", "14 - 8 = 6 loncatan.", verifikasi={"ekspresi": "14 - 8", "hasil": "6"})
mc("c3", "sedang", X, Pr, S2, "Mulai dari 11 melompat maju 6 langkah tiba di ....", ["17", "16", "18", "15"], "A", "11 + 6 = 17.", verifikasi={"ekspresi": "11 + 6", "hasil": "17"})
tf("c3", "sedang", X, Pr, S3, "Dari 16 melompat ke kiri 6 langkah tiba di angka 9.", "Salah", "16 - 6 = 10, bukan 9.")
sa("c3", "sedang", X, Pr, S4, "Berapa banyak loncatan mundur dari 18 menuju 12?", "6", "18 - 12 = 6 loncatan.", verifikasi={"ekspresi": "18 - 12", "hasil": "6"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Loncatan dari 9 ke 15 sama banyaknya dengan loncatan dari ....", ["4 ke 10", "3 ke 10", "5 ke 10", "2 ke 9"], "A", "15 - 9 = 6 dan 10 - 4 = 6.")
mc("c3", "sedang", K, Pr, S2, "Mulai di angka 13 mundur 7 langkah tiba di ....", ["6", "5", "7", "8"], "A", "13 - 7 = 6.", verifikasi={"ekspresi": "13 - 7", "hasil": "6"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Seorang anak menghitung angka 3, 4, 5 sebagai 3 loncatan. Apa kesalahannya?", ["ia menghitung titik bukan loncatan", "ia melompat mundur", "ia salah membaca angka", "ia melompat terlalu jauh"], "A", "Dari 3 ke 5 hanya ada 2 loncatan, anak itu salah menghitung titik.")
mc("c4", "sedang", T, Kn, S2, "Manakah garis bilangan yang menunjukkan operasi $6 + 5 = 11$?", ["mulai 6 lompat maju 5 ke 11", "mulai 5 lompat maju 6 ke 10", "mulai 6 lompat mundur 5 ke 1", "mulai 11 lompat maju 5 ke 16"], "A", "Mulai di 6 lalu melompat maju 5 kali tiba di 11.")
tf("c4", "sedang", T, Kn, S3, "Melompat maju 4 langkah lalu mundur 4 langkah kembali ke titik semula.", "Benar", "4 - 4 = 0 langkah dari titik awal.")
tf("c4", "sedang", T, Kn, S4, "Panah ke kiri dari 14 ke 9 artinya operasi $14 + 5$.", "Salah", "Panah ke kiri artinya operasi pengurangan: 14 - 5 = 9.")
sa("c4", "sedang", T, Kn, S4, "Dari 8 melompat ke kanan hingga tiba di 16. Berapa kali melompat?", "8", "16 - 8 = 8 kali.", verifikasi={"ekspresi": "16 - 8", "hasil": "8"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Bila ingin menghitung loncatan dengan benar, kita harus menghitung ....", ["jarak perpindahan antartitik", "jumlah semua angka", "angka paling besar", "angka yang dilewati dua kali"], "A", "Loncatan dihitung dari jarak perpindahan antartitik.")
mc("c4", "sedang", X, Kn, S2, "Operasi $7 + 6$ dan $8 + 5$ pada garis bilangan memiliki ....", ["titik akhir mendarat yang sama", "titik awal berdiri sama", "banyak loncatan sama", "arah yang berbeda"], "A", "Keduanya mendarat di titik 13.")
tf("c4", "sedang", X, Kn, S4, "Dari angka 20 melompat mundur 8 kali mendarat di angka 11.", "Salah", "20 - 8 = 12, bukan 11.")
mc("c4", "sulit", X, Me, S1, "Mengapa hasil hitung bertambah satu jika kita menghitung titiknya?", ["karena titik awal ikut terhitung", "karena loncatannya dobel", "karena angkanya salah", "karena garisnya kurang panjang"], "A", "Menghitung titik akan memasukkan titik awal yang belum melompat.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Edo melompat dari 5 ke 9. Siti melompat dari 11 ke 15. Siapa melompat lebih banyak?", ["sama banyak yaitu 4 loncatan", "Edo lebih banyak", "Siti lebih banyak", "tidak bisa dihitung"], "A", "9 - 5 = 4 dan 15 - 11 = 4 loncatan.")
mc("c4", "sulit", K, Me, S2, "Mulai di titik M melompat maju 5 kali tiba di 14. Berapakah M?", ["9", "8", "10", "7"], "A", "14 - 5 = 9.", verifikasi={"ekspresi": "14 - 5", "hasil": "9"})
tf("c4", "sulit", K, Me, S3, "Pada garis bilangan, dua loncatan kecil 2 langkah sama dengan satu loncatan 4 langkah.", "Benar", "2 + 2 = 4 langkah.")
mc("c4", "sulit", K, Me, S4, "Dari 17 melompat mundur berapa kali agar tiba di 8?", ["9 kali", "8 kali", "10 kali", "7 kali"], "A", "17 - 8 = 9 kali.", verifikasi={"ekspresi": "17 - 8", "hasil": "9"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Andi berkata dari 2 ke 6 ada 5 loncatan. Bagaimana memperbaikinya?", ["tunjukkan bahwa ada 4 lengkungan loncatan", "benarkan jawaban Andi", "katakan ada 6 loncatan", "suruh mulai dari angka 0"], "A", "Tunjukkan 4 lengkungan: 2-3, 3-4, 4-5, 5-6.")
mc("c5", "sedang", T, Me, S2, "Katak mulai melompat di angka 6 dan ingin tiba di 15. Berapa loncatan dibutuhkan?", ["9 loncatan", "8 loncatan", "10 loncatan", "7 loncatan"], "A", "15 - 6 = 9 loncatan.", verifikasi={"ekspresi": "15 - 6", "hasil": "9"})
mc("c5", "sedang", T, Me, S3, "Apa yang terjadi jika kita salah arah melompat saat menghitung $12 - 4$?", ["hasilnya menjadi 16 bukan 8", "hasilnya menjadi 10", "hasilnya tetap 8", "tidak terjadi apa-apa"], "A", "Jika melompat ke kanan hasilnya jadi 16 (salah).")
mc("c5", "sulit", T, Me, S4, "Belalang di 16 lompat mundur 5 lalu mundur 3. Di mana ia mendarat?", ["angka 8", "angka 9", "angka 7", "angka 10"], "A", "16 - 5 - 3 = 8.", verifikasi={"ekspresi": "16 - 5 - 3", "hasil": "8"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Bagaimana cara mudah mengecek kebenaran loncatan garis bilangan?", ["hitung jumlah lengkungan busurnya", "hitung banyaknya angka", "hitung garis lurusnya", "tebak dari panjang panah"], "A", "Menghitung lengkungan busur memastikan jumlah loncatan benar.")
mc("c5", "sulit", K, Me, S4, "Kelinci di 7 ingin ke 19 dengan 2 loncatan sama panjang. Berapa panjang tiap loncatan?", ["6 langkah", "5 langkah", "7 langkah", "4 langkah"], "A", "(19 - 7) / 2 = 6 langkah.", verifikasi={"ekspresi": "(19 - 7) // 2", "hasil": "6"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Susunlah aturan menghitung loncatan garis bilangan agar tidak keliru!", ["mulai hitung satu setelah melompat satu langkah", "hitung angka awal sebagai satu", "hitung semua angka yang ada", "abaikan tanda panah"], "A", "Hitung satu setelah kaki mendarat pada langkah pertama.")
mc("c6", "sulit", K, Me, S4, "Rancanglah garis bilangan yang menunjukkan operasi $8 + 7 - 3$!", ["mulai 8 maju 7 lalu mundur 3 ke 12", "mulai 8 maju 7 lalu maju 3 ke 18", "mulai 8 mundur 7 lalu maju 3", "mulai 7 maju 8 ke 15"], "A", "8 + 7 = 15 lalu mundur 3 ke 12.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Rancanglah rute loncatan dari 5 menuju 20 dengan tiga loncatan sama!", ["tiga loncatan masing-masing 5 langkah", "tiga loncatan masing-masing 4 langkah", "tiga loncatan masing-masing 6 langkah", "tiga loncatan masing-masing 3 langkah"], "A", "(20 - 5) / 3 = 5 langkah.", verifikasi={"ekspresi": "(20 - 5) // 3", "hasil": "5"})
mc("c6", "sulit", P, Me, S4, "Susunlah kalimat matematika dari garis bilangan: mulai 18 mundur 6 lalu mundur lagi 4!", ["$18 - 6 - 4 = 8$", "$18 - 6 + 4 = 16$", "$18 + 6 - 4 = 20$", "$18 - 10 = 7$"], "A", "18 - 6 - 4 = 8.")

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab15_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab15.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
