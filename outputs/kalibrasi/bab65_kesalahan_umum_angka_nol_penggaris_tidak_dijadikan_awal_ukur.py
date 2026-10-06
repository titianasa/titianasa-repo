#!/usr/bin/env python3
"""
Generator dan validator Bab 65 Matematika Kelas 2 SD:
"Kesalahan Umum: Angka Nol Penggaris Tidak Dijadikan Awal Ukur" (Fase A)
bab_id: 6e71b6fe-da7a-466d-9351-fd5ee0edcb38
article_id: 2c2e6d4e-c745-4fee-b539-d3b863dcbab0
quiz_id: 6efd8bf3-b37e-41a4-b8a9-29bdd726dd40
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "j1l2n3p4r501"  # Mengenali Kesalahan Memulai dari Tepi Penggaris
S2 = "k2m3o4q5s602"  # Mengenali Kesalahan Memulai dari Angka Satu
S3 = "l3n4p5r6t703"  # Cara Memperbaiki Pengukuran Tanpa Angka Nol
S4 = "m4o5q6s7u804"  # Membiasakan Pengukuran yang Tepat

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Banyak anak membuat kesalahan ukur.
Kesalahan pertama adalah mengukur dari tepi.
Tepi plastik terluar penggaris.
Padahal ada ruang kosong di sana.
Garis nol ada agak ke dalam.
Jika mulai dari tepi plastik.
Maka hasil ukur menjadi tidak tepat.
Ukuran terbaca lebih pendek dari kenyataan.
Awalilah selalu tepat di garis nol!

:::definition
title: Garis Angka Nol
Garis skala pertama penanda titik awal pengukuran panjang pada penggaris.
:::"""

s2_content = """Kesalahan kedua adalah mulai angka satu.
Anak menaruh benda di angka 1.
Lalu melihat ujung benda di 9.
Mereka mengira panjang benda 9 cm.
Ini adalah anggapan yang keliru!
Benda tidak dimulai dari angka nol.
Panjang benda sebenarnya adalah 8 cm.
Mulai dari 1 membuat ukuran bertambah.
Hati-hati, jangan terjebak angka satu!

:::common_trap
title: Langsung Membaca Angka Akhir
Jangan langsung membaca angka ujung.
Angka ujung bukan panjang sebenarnya.
Kurangkan angka akhir dengan angka awal.
Hasil pengurangan adalah panjang asli.
:::"""

s3_content = """Bagaimana jika penggaris patah?
Bagian angka nol telah hilang.
Kita masih bisa menggunakannya!
Letakkan pangkal benda di angka 2.
Lihat ujung benda di angka 10.
Hitung selisih kedua angka.
10 dikurang 2 adalah 8.
Panjang benda itu adalah 8 cm.
Gunakan pengurangan: Ujung dikurang pangkal!

:::steps
title: Menghitung Panjang Benda yang Bergeser
1. Catat angka awal (pangkal benda).
2. Catat angka akhir (ujung benda).
3. Hitung selisih: Angka akhir - Angka awal.
4. Tulis hasil pengurangan dengan satuan cm.
:::"""

s4_content = """Mari kita biasakan mengukur cermat.
Lihat posisi pangkal benda dahulu.
Pastikan tepat di garis angka nol.
Setelah itu baru lihat ujungnya.
Ujung menunjukkan panjang benda secara langsung.
Jika berawal di 0 dan berujung di 15.
Panjang benda pasti 15 cm.
Ukur dengan teliti dan cermat!

:::callout
variant: summary
title: Ringkasan
text: Jangan ukur dari tepi kosong. Jangan mulai dari angka satu. Selalu mulai tepat di angka nol!
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenali Kesalahan Memulai dari Tepi Penggaris",
        "minutes": 6,
        "goal": "Siswa memahami kesalahan mengukur dari tepi luar penggaris tanpa garis skala 0.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengenali Kesalahan Memulai dari Angka Satu",
        "minutes": 6,
        "goal": "Siswa menyadari kesalahan mengira angka akhir sebagai panjang jika mulai dari angka 1.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Cara Memperbaiki Pengukuran Tanpa Angka Nol",
        "minutes": 6,
        "goal": "Siswa mampu mengoreksi pengukuran dengan rumus selisih: angka akhir dikurang angka awal.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Membiasakan Pengukuran yang Tepat",
        "minutes": 6,
        "goal": "Siswa membiasakan mengecek titik awal di angka 0 sebelum membaca angka akhir.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Angka Nol Penggaris Tidak Dijadikan Awal Ukur",
    "topic": "Mengukur Panjang dan Berat",
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
# 2. DEFINISI BANK 50 SOAL BAB 65
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
mc("c1", "mudah", D, F, S1, "Titik awal yang benar saat mengukur benda adalah garis angka ....", ["0", "1", "2", "tepi plastik"], "A", "Garis angka 0 adalah titik awal yang benar.")
tf("c1", "mudah", D, F, S2, "Jika mulai dari angka 1 ke 7, panjang benda adalah 7 cm.", "Salah", "Panjangnya adalah 7 - 1 = 6 cm, bukan 7 cm.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Mengapa tidak boleh mengukur dari tepi luar penggaris?", ["karena ada celah kosong sebelum garis 0", "karena tepi penggaris licin", "karena tidak boleh disentuh", "karena angkanya hilang"], "A", "Celah kosong sebelum angka 0 menyebabkan ukuran salah.")
mc("c1", "mudah", T, F, S2, "Benda diletakkan dari angka 1 sampai angka 6. Berapa panjang benda?", ["5 cm", "6 cm", "7 cm", "1 cm"], "A", "6 - 1 = 5 cm.", verifikasi={"ekspresi": "6 - 1", "hasil": "5"})
sa("c1", "mudah", T, F, S3, "Pensil dari angka 2 sampai angka 9 panjangnya ... cm.", "7", "9 - 2 = 7 cm.", verifikasi={"ekspresi": "9 - 2", "hasil": "7"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Benda diletakkan dari angka 3 sampai angka 10. Berapakah panjang benda?", ["7 cm", "10 cm", "3 cm", "13 cm"], "A", "10 - 3 = 7 cm.", verifikasi={"ekspresi": "10 - 3", "hasil": "7"})
tf("c2", "mudah", D, Kn, S4, "Memulai dari angka nol membuat angka ujung langsung menjadi panjang benda.", "Benar", "Karena nilai awal adalah nol (ujung - 0 = ujung).")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Tono mengukur pita dari angka 1 ke angka 11, disebut 11 cm. Kesalahan Tono?", ["lupa mengurangkan dengan angka awal 1", "penggarisnya bengkok", "pitanya terlipat", "salah memilih satuan"], "A", "Jika mulai dari 1, panjang sebenarnya = 11 - 1 = 10 cm.", "Mengira angka akhir adalah panjang benda")
mc("c2", "mudah", R, Kn, S1, "Rini menaruh pensil di tepi plastik tanpa garis 0. Apa akibatnya?", ["hasil ukur menjadi tidak akurat", "pensilnya menjadi patah", "penggaris menjadi rusak", "hasil ukur pasti pas"], "A", "Tepi tanpa garis 0 memiliki ruang kosong yang mengacaukan ukuran.", "Mengukur dari tepi fisik terluar penggaris")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Di manakah posisi garis nol pada penggaris plastik umumnya?", ["sedikit masuk ke dalam dari tepi ujung", "tepat di tengah penggaris", "di ujung paling belakang", "tidak ada garis nol"], "A", "Garis 0 biasanya berjarak sedikit dari tepi luar.")
mc("c2", "mudah", T, Kn, S2, "Krayon dari angka 1 sampai angka 8 memiliki panjang ....", ["7 cm", "8 cm", "9 cm", "1 cm"], "A", "8 - 1 = 7 cm.", verifikasi={"ekspresi": "8 - 1", "hasil": "7"})
tf("c2", "mudah", T, Kn, S3, "Penggaris tanpa angka 0 masih bisa dipakai dengan cara mengurangkan.", "Benar", "Gunakan selisih angka akhir dikurang angka awal.")
sa("c2", "mudah", T, Kn, S4, "Penghapus diletakkan dari angka 0 ke 5 memiliki panjang ... cm.", "5", "5 - 0 = 5 cm.", verifikasi={"ekspresi": "5 - 0", "hasil": "5"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Spidol diukur dari angka 4 ke angka 18. Berapakah panjang spidol?", ["14 cm", "18 cm", "22 cm", "4 cm"], "A", "18 - 4 = 14 cm.", "Hanya membaca angka akhir tanpa dikurang angka awal", verifikasi={"ekspresi": "18 - 4", "hasil": "14"})
mc("c3", "sedang", R, Pr, S3, "Penggaris patah mulai angka 5 sampai angka 17. Berapa panjang kawat?", ["12 cm", "17 cm", "5 cm", "22 cm"], "A", "17 - 5 = 12 cm.", "Bingung mengukur dengan skala bergeser", verifikasi={"ekspresi": "17 - 5", "hasil": "12"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Langkah pertama sebelum melihat angka akhir pada penggaris adalah ....", ["memeriksa apakah pangkal benda tepat di angka nol", "langsung mencatat angka", "membalik penggaris", "mematahkan penggaris"], "A", "Pastikan pangkal tepat di garis angka 0.")
mc("c3", "mudah", T, Pr, S4, "Benda diletakkan dari angka 0 sampai 19. Panjang benda adalah ....", ["19 cm", "18 cm", "20 cm", "0 cm"], "A", "19 - 0 = 19 cm.", verifikasi={"ekspresi": "19 - 0", "hasil": "19"})
tf("c3", "sedang", T, Pr, S2, "Benda dari angka 1 sampai 12 lebih panjang dari benda (0 ke 11 cm).", "Salah", "12 - 1 = 11 cm, dan 11 - 0 = 11 cm. Keduanya sama panjang.")
mc("c3", "sedang", T, Pr, S3, "Tongkat diukur dari angka 6 sampai 25. Panjang tongkat adalah ....", ["19 cm", "25 cm", "31 cm", "18 cm"], "A", "25 - 6 = 19 cm.", verifikasi={"ekspresi": "25 - 6", "hasil": "19"})
tf("c3", "sedang", T, Pr, S4, "Melihat angka awal sangat penting sebelum menyimpulkan panjang benda.", "Benar", "Titik awal menentukan apakah perlu dikurang atau tidak.")
sa("c3", "sedang", T, Pr, S3, "Berapakah panjang benda dari angka 4 sampai angka 16 dalam cm?", "12", "16 - 4 = 12 cm.", verifikasi={"ekspresi": "16 - 4", "hasil": "12"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Jika penggaris mulai angka 0 tetapi ditaruh miring, ukuran menjadi ....", ["tidak tepat atau meleset", "pasti benar", "lebih rapi", "menjadi nol"], "A", "Kemiringan membuat panjang garis meleset.")
mc("c3", "sedang", X, Pr, S2, "Benda A (1 ke 10 cm) dan Benda B (0 ke 9 cm). Panjang keduanya ....", ["sama panjang yaitu 9 cm", "benda A lebih panjang", "benda B lebih panjang", "tidak dapat dibandingkan"], "A", "Benda A = 10 - 1 = 9 cm. Benda B = 9 cm. Keduanya sama.")
tf("c3", "sedang", X, Pr, S3, "Pengukuran dari angka 7 ke 21 sama hasilnya dengan dari angka 0 ke 14.", "Benar", "21 - 7 = 14 cm, dan 14 - 0 = 14 cm.")
sa("c3", "sedang", X, Pr, S3, "Sebuah batang lidi diukur dari angka 8 ke 27. Panjangnya adalah ... cm.", "19", "27 - 8 = 19 cm.", verifikasi={"ekspresi": "27 - 8", "hasil": "19"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Benda dari angka 5 sampai 23. Berapakah panjang benda tersebut?", ["18 cm", "23 cm", "28 cm", "17 cm"], "A", "23 - 5 = 18 cm.", verifikasi={"ekspresi": "23 - 5", "hasil": "18"})
mc("c3", "sedang", K, Pr, S4, "Ani mengukur buku: pangkal di 0, ujung di 28. Panjang buku Ani?", ["28 cm", "27 cm", "29 cm", "20 cm"], "A", "28 - 0 = 28 cm.", verifikasi={"ekspresi": "28 - 0", "hasil": "28"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Apa yang membedakan tepi fisik penggaris dengan garis angka nol?", ["tepi fisik adalah batas kayu/plastik, garis nol adalah awal skala ukuran", "tidak ada bedanya", "tepi fisik selalu bernomor", "garis nol di tengah"], "A", "Tepi fisik adalah bahan penggaris, garis nol adalah awal satuan.")
mc("c4", "sedang", T, Kn, S2, "Mengapa anak sering salah memulai dari angka 1?", ["karena terbiasa menghitung membilang mulai dari angka satu", "karena angka nol tidak terlihat", "karena disuruh guru", "karena angka 1 besar"], "A", "Kebiasaan membilang mulai 1 terbawa ke pengukuran skala.")
tf("c4", "sedang", T, Kn, S3, "Benda dari angka 3 ke 15 lebih panjang daripada benda dari angka 0 ke 13.", "Salah", "15 - 3 = 12 cm, sedangkan 13 cm lebih panjang dari 12 cm.")
tf("c4", "sedang", T, Kn, S4, "Jika pangkal di angka nol, panjang benda adalah angka akhir ditambah 1.", "Salah", "Panjang benda tepat sama dengan angka akhir, bukan ditambah 1.")
sa("c4", "sedang", T, Kn, S3, "Berapakah selisih panjang antara (2 ke 16 cm) dan (0 ke 11 cm)?", "3", "(16 - 2) - 11 = 14 - 11 = 3 cm.", verifikasi={"ekspresi": "(16 - 2) - 11", "hasil": "3"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S2, "Budi berkata: 'Pensilku dari angka 1 ke 9 berarti 9 cm.' Tanggapan yang tepat?", ["keliru, seharusnya 9 dikurang 1 yaitu 8 cm", "benar sekali", "seharusnya 9 ditambah 1", "pensilnya memendek"], "A", "Mulai dari 1 harus dikurangkan dengan 1.")
mc("c4", "sedang", X, Kn, S3, "Benda X (4 ke 18 cm) dan Y (2 ke 17 cm). Manakah lebih panjang?", ["Benda Y karena panjangnya 15 cm", "Benda X karena ujungnya 18", "keduanya sama panjang", "tidak dapat dihitung"], "A", "X = 18 - 4 = 14 cm. Y = 17 - 2 = 15 cm. 15 cm > 14 cm.")
tf("c4", "sedang", X, Kn, S1, "Ujung penggaris kayu yang aus atau cuil tidak mempengaruhi garis nol jika garisnya utuh.", "Benar", "Yang penting garis skala angka 0 masih terlihat jelas.")
mc("c4", "sulit", X, Me, S3, "Pita A (2 ke 14), B (5 ke 20), C (0 ke 13). Manakah terpanjang?", ["pita B", "pita A", "pita C", "semua sama"], "A", "A = 12 cm, B = 15 cm, C = 13 cm. B terpanjang.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Mengapa penggaris dibuat dengan garis nol berjarak sedikit dari tepinya?", ["agar garis nol tidak mudah rusak atau aus bila tepi penggaris terbentur", "supaya terlihat antik", "agar penggaris lebih mahal", "karena tidak sengaja"], "A", "Melindungi garis 0 dari keausan benturan fisik.")
mc("c4", "sulit", K, Me, S2, "Penggaris terpotong: Benda A (3 ke 21), Benda B (5 ke 25). Selisih panjangnya?", ["2 cm", "1 cm", "3 cm", "0 cm"], "A", "A = 18 cm, B = 20 cm. Selisih = 20 - 18 = 2 cm.", verifikasi={"ekspresi": "(25 - 5) - (21 - 3)", "hasil": "2"})
tf("c4", "sulit", K, Me, S4, "Mengukur dari angka 0 membutuhkan langkah pengurangan angka awal.", "Salah", "Jika mulai dari nol, angka di ujung langsung menjadi nilai panjang tanpa pengurangan.")
mc("c4", "sulit", K, Me, S3, "Kayu dari angka 8 ke 35. Kayu kedua dari angka 0 ke 29. Selisih panjang keduanya?", ["2 cm", "3 cm", "1 cm", "4 cm"], "A", "Kayu 1 = 35 - 8 = 27 cm. Kayu 2 = 29 cm. Selisih = 29 - 27 = 2 cm.", verifikasi={"ekspresi": "29 - (35 - 8)", "hasil": "2"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Penggaris A berongga 1 cm sebelum nol, B pas nol. Diukur dari tepi luar?", ["penggaris A menghasilkan bacaan 1 cm lebih besar dari penggaris B", "keduanya sama", "penggaris B lebih besar", "tidak ada bedanya"], "A", "Rongga 1 cm membuat pembacaan bergeser.")
mc("c5", "sedang", T, Me, S2, "Doni selalu mulai dari angka 1 dan mencatat 16 cm. Berapa panjang sebenarnya?", ["15 cm", "16 cm", "17 cm", "14 cm"], "A", "16 - 1 = 15 cm.", verifikasi={"ekspresi": "16 - 1", "hasil": "15"})
mc("c5", "sedang", T, Me, S3, "Dua pensil: Pensil 1 (4 ke 19 cm), Pensil 2 (6 ke 23 cm). Gabungan keduanya?", ["32 cm", "30 cm", "34 cm", "28 cm"], "A", "(19 - 4) + (23 - 6) = 15 + 17 = 32 cm.", verifikasi={"ekspresi": "(19 - 4) + (23 - 6)", "hasil": "32"})
mc("c5", "sulit", T, Me, S4, "Tali diukur dari 5 ke 42 cm. Dipotong untuk ikat kado 25 cm. Berapa sisa tali?", ["12 cm", "10 cm", "15 cm", "14 cm"], "A", "(42 - 5) - 25 = 37 - 25 = 12 cm.", verifikasi={"ekspresi": "(42 - 5) - 25", "hasil": "12"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Benda A (7 ke 29) dan Benda B (10 ke 36). Berapakah selisih panjang keduanya?", ["4 cm", "3 cm", "5 cm", "2 cm"], "A", "A = 22 cm, B = 26 cm. Selisih = 26 - 22 = 4 cm.", verifikasi={"ekspresi": "(36 - 10) - (29 - 7)", "hasil": "4"})
mc("c5", "sulit", K, Me, S4, "Kawat dari 6 ke 54 cm dipotong menjadi 4 bagian sama panjang. Panjang satu bagian?", ["12 cm", "10 cm", "14 cm", "11 cm"], "A", "(54 - 6) : 4 = 48 : 4 = 12 cm.", verifikasi={"ekspresi": "(54 - 6) / 4", "hasil": "12"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Mengapa pengrajin kayu membuat tanda goresan segitiga tepat di garis nol?", ["agar ujung meteran dapat terkunci tepat di garis skala nol tanpa bergeser", "agar terlihat cantik", "karena kayunya keras", "tidak ada tujuannya"], "A", "Tanda goresan menjaga ketepatan posisi nol.")
mc("c6", "sulit", K, Me, S3, "Dua penggaris patah disambung: A (mulai 4 ke 18), B (mulai 3 ke 20). Total panjangnya?", ["31 cm", "29 cm", "33 cm", "28 cm"], "A", "(18 - 4) + (20 - 3) = 14 + 17 = 31 cm.", verifikasi={"ekspresi": "(18 - 4) + (20 - 3)", "hasil": "31"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Hitunglah hasil dari: (panjang benda 5 ke 25) + (panjang benda 8 ke 33) - 12 cm!", ["33 cm", "31 cm", "35 cm", "30 cm"], "A", "(25 - 5) + (33 - 8) - 12 = 20 + 25 - 12 = 45 - 12 = 33 cm.", verifikasi={"ekspresi": "(25 - 5) + (33 - 8) - 12", "hasil": "33"})
mc("c6", "sulit", P, Me, S4, "Dua anak mengukur kawat 60 cm. Anak A mulai angka 2. Angka akhir anak A?", ["62 cm", "58 cm", "60 cm", "64 cm"], "A", "Ujung = 60 + 2 = 62 cm.", verifikasi={"ekspresi": "60 + 2", "hasil": "62"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab65_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab65.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
