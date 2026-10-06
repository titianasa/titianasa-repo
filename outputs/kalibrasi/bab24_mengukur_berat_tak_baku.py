#!/usr/bin/env python3
"""
Generator dan validator Bab 24 Matematika Kelas 1 SD:
"Mengukur Berat dengan Satuan Tak Baku" (Fase A)
bab_id: 0d7b9701-39a5-43c2-83bb-f746fb3487e6
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "d1e2f33a4b01"  # Mengenal Satuan Berat Tak Baku
S2 = "e2f3a44b5c12"  # Cara Menimbang Sampai Seimbang
S3 = "f3a4b55c6d23"  # Membandingkan Berat Berdasarkan Jumlah Satuan
S4 = "a4b5c66d7e34"  # Pentingnya Keseragaman Satuan Ukur

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Kita bisa mengukur berat benda.
Gunakan satuan tak baku.
Benda kecil seragam sangat cocok.
Contohnya kelereng kaca yang sama.
Bisa juga memakai uang koin.
Koin logam punya berat serupa.
Balok kayu kecil juga bisa.
Semua bisa menjadi satuan ukur.

:::definition
title: Satuan Berat Tak Baku
Satuan tak baku adalah benda kecil yang dipakai menimbang.
Contohnya kelereng, koin, atau klip kertas.
:::"""

s2_content = """Siapkan timbangan gantungan baju.
Gantung kantong plastik di ujungnya.
Letakkan buku di kantong kiri.
Masukkan kelereng ke kantong kanan.
Masukkan satu per satu pelan.
Amati posisi gantungan bajunya.
Berhenti saat timbangan lurus mendatar.
Hitung kelereng di dalam kantong.

:::steps
title: Menimbang Sampai Seimbang
1. Letakkan benda di satu sisi timbangan.
2. Masukkan kelereng satu demi satu ke sisi lain.
3. Berhenti saat timbangan lurus sejajar mendatar.
:::"""

s3_content = """Kita dapat membandingkan berat benda.
Bandingkan jumlah satuan kelerengnya.
Buku seimbang dengan 6 kelereng.
Pensil seimbang dengan 2 kelereng.
Angka 6 lebih dari 2.
Maka buku lebih berat.
Pensil jauh lebih ringan.
Jumlah satuan menunjukkan berat benda."""

s4_content = """Ada aturan penting saat menimbang.
Satuan penimbang harus selalu seragam.
Gunakan kelereng berukuran sama besar.
Jangan mencampur kelereng dan koin.

:::common_trap
title: Membandingkan Satuan Beda Jenis
Buku beratnya 4 kelereng.
Kotak pensil beratnya 6 koin.
Kita tidak boleh langsung membandingkan.
Kelereng dan koin berbeda berat.
Gunakan selalu satuan yang sejenis.
:::

:::callout
variant: summary
title: Ringkasan
text: Timbang sampai posisi seimbang mendatar. Gunakan satuan yang sama jenisnya saat membandingkan berat benda.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Satuan Berat Tak Baku",
        "minutes": 6,
        "goal": "Siswa mengenal benda-benda seragam seperti kelereng atau koin sebagai satuan penimbang berat tak baku.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Cara Menimbang Sampai Seimbang",
        "minutes": 6,
        "goal": "Siswa memahami prosedur menimbang dengan memasukkan satuan tak baku satu per satu hingga posisi timbangan seimbang mendatar.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membandingkan Berat Berdasarkan Jumlah Satuan",
        "minutes": 6,
        "goal": "Siswa dapat membandingkan berat dua benda berdasarkan jumlah cacah satuan tak baku yang sama.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Pentingnya Keseragaman Satuan Ukur",
        "minutes": 6,
        "goal": "Siswa memahami bahwa satuan ukur penimbang harus seragam dan tidak boleh dicampur antarjenis saat membandingkan.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengukur Berat dengan Satuan Tak Baku",
    "topic": "Membandingkan dan Mengukur dengan Satuan Tak Baku",
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
# 2. DEFINISI BANK 50 SOAL BAB 24
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
mc("c1", "mudah", D, F, S1, "Benda kecil yang sering digunakan sebagai satuan berat tak baku adalah ....", ["kelereng", "batu bata", "air seember", "sepatu"], "A", "Kelereng kecil seragam sangat tepat untuk satuan penimbang tak baku.")
tf("c1", "mudah", D, F, S2, "Timbangan berhenti diisi saat posisinya sudah lurus mendatar.", "Benar", "Posisi lurus mendatar menunjukkan keadaan seimbang.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Selain kelereng, benda yang bisa dipakai mengukur berat tak baku adalah ....", ["uang koin logam", "kapur tulis hancur", "daun kering robek", "pasir acak"], "A", "Uang koin logam memiliki ukuran dan berat seragam.")
mc("c1", "mudah", T, F, S2, "Alat rumah tangga sederhana yang bisa dijadikan timbangan adalah ....", ["gantungan baju", "sapu ijuk", "gayung air", "panci masak"], "A", "Gantungan baju dengan dua lengan bisa digunakan sebagai timbangan gantung.")
sa("c1", "mudah", T, F, S3, "Sebuah apel seimbang dengan 4 kelereng. Berapa kelereng berat apel?", "4", "Berat apel sama dengan 4 kelereng.", verifikasi={"ekspresi": "4", "hasil": "4"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Apakah boleh mencampur kelereng dan koin saat menimbang satu benda?", ["tidak boleh", "sangat dianjurkan", "boleh kapan saja", "bebas terserah"], "A", "Satuan penimbang harus seragam agar hasilnya jelas.", "Mencampur jenis satuan penimbang")
tf("c2", "mudah", D, Kn, S3, "Benda dengan jumlah kelereng lebih banyak adalah benda yang lebih berat.", "Benar", "Makin banyak kelereng penyeimbang, makin berat benda itu.")

# Remedial (2)
mc("c2", "mudah", R, F, S2, "Kapan kita berhenti memasukkan kelereng ke timbangan?", ["saat kedua sisi sejajar rata", "saat timbangan miring sekali", "saat kantong plastik robek", "saat kelereng habis"], "A", "Berhenti memasukkan kelereng ketika timbangan sudah seimbang mendatar.", "Tidak tahu kapan proses menimbang selesai")
mc("c2", "mudah", R, Kn, S4, "Buku = 5 kelereng. Kotak = 5 koin. Mengapa tidak bisa dipastikan sama berat?", ["karena berat 1 kelereng belum tentu sama dengan 1 koin", "karena warna kelereng beda", "karena koin dari logam", "karena bentuk kotak"], "A", "Kelereng dan koin berbeda jenis sehingga berat satuannya berbeda.", "Membandingkan dua benda dengan satuan penimbang berbeda")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Buku = 6 kelereng. Penggaris = 2 kelereng. Berapa kelereng selisih beratnya?", ["4 kelereng", "3 kelereng", "5 kelereng", "2 kelereng"], "A", "6 - 2 = 4 kelereng.", verifikasi={"ekspresi": "6 - 2", "hasil": "4"})
mc("c2", "mudah", T, Kn, S2, "Saat menimbang, kelereng dimasukkan ke kantong secara ....", ["satu per satu pelan", "langsung sepuluh butir", "dilempar cepat", "bersama wadahnya"], "A", "Kelereng dimasukkan satu demi satu agar seimbang pas.")
tf("c2", "mudah", T, Kn, S4, "Memakai kelereng besar dan kecil bercampur membuat ukuran berat tidak adil.", "Benar", "Keseragaman ukuran penimbang sangat penting untuk keadilan pengukuran.")
sa("c2", "mudah", T, Kn, S3, "Kotak pensil = 7 koin. Penghapus = 2 koin. Berapa koin selisihnya?", "5", "7 - 2 = 5 koin.", verifikasi={"ekspresi": "7 - 2", "hasil": "5"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Benda A = 9 kelereng. Benda B = 4 kelereng. Benda manakah yang lebih ringan?", ["benda B", "benda A", "keduanya sama", "tidak tahu"], "A", "Benda B butuh kelereng lebih sedikit (4 < 9), jadi lebih ringan.", "Tertukar menentukan benda lebih ringan dari jumlah satuan")
mc("c3", "sedang", R, Pr, S4, "Doni ingin menimbang jeruk. Manakah penimbang yang paling tepat digunakan?", ["10 butir kelereng kaca yang sama besar", "5 kelereng dan 5 koin dicampur", "batu kerikil aneka ukuran", "pasir segenggam"], "A", "Kelereng seragam berukuran sama adalah pilihan terbaik.", "Memilih alat ukur tak baku yang tidak seragam")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Mangga seimbang dengan 8 kelereng. Berapa kelereng berat 2 mangga?", ["16 kelereng", "14 kelereng", "18 kelereng", "12 kelereng"], "A", "8 + 8 = 16 kelereng.", verifikasi={"ekspresi": "8 + 8", "hasil": "16"})
mc("c3", "sedang", T, Pr, S2, "Buku = 10 koin. Rautan = 3 koin. Berapa koin selisih beratnya?", ["7 koin", "6 koin", "8 koin", "5 koin"], "A", "10 - 3 = 7 koin.", verifikasi={"ekspresi": "10 - 3", "hasil": "7"})
tf("c3", "sedang", T, Pr, S3, "Benda yang seimbang dengan 12 koin lebih ringan dari benda seimbang 5 koin.", "Salah", "12 koin lebih berat daripada 5 koin.")
mc("c3", "sedang", T, Pr, S4, "Mengapa penimbang harus menggunakan kelereng berukuran sama besar?", ["agar setiap butir kelereng memiliki berat yang setara", "agar timbangan terlihat indah", "agar kelereng tidak jatuh", "agar muat banyak"], "A", "Keseragaman kelereng menjamin berat per butir setara.")
tf("c3", "sedang", T, Pr, S1, "Satu buah jeruk selalu seimbang dengan tepat 100 kelereng.", "Salah", "100 kelereng terlalu banyak dan berat untuk satu buah jeruk.")
sa("c3", "mudah", T, Pr, S2, "Gunting seimbang dengan 6 kelereng. Berapa kelereng untuk 2 gunting?", "12", "6 + 6 = 12 kelereng.", verifikasi={"ekspresi": "6 + 6", "hasil": "12"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Topi = 5 kelereng. Sepatu = 14 kelereng. Berapa kelereng selisih keduanya?", ["9 kelereng", "8 kelereng", "10 kelereng", "7 kelereng"], "A", "14 - 5 = 9 kelereng.", verifikasi={"ekspresi": "14 - 5", "hasil": "9"})
mc("c3", "sedang", X, Pr, S2, "Botol seimbang setelah diberi 4 koin lalu ditambah 3 koin. Berapa koin berat botol?", ["7 koin", "6 koin", "8 koin", "5 koin"], "A", "4 + 3 = 7 koin.", verifikasi={"ekspresi": "4 + 3", "hasil": "7"})
tf("c3", "sedang", X, Pr, S3, "Benda A = 11 kelereng dan Benda B = 11 kelereng memiliki berat yang sama.", "Benar", "Jumlah kelereng sama menandakan berat kedua benda sama.")
sa("c3", "sedang", X, Pr, S4, "Apel = 8 koin. Jeruk = 5 koin. Berapa koin selisih beratnya?", "3", "8 - 5 = 3 koin.", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Buku gambar = 12 kelereng. Pensil warna = 7 kelereng. Selisih beratnya?", ["5 kelereng", "4 kelereng", "6 kelereng", "3 kelereng"], "A", "12 - 7 = 5 kelereng.", verifikasi={"ekspresi": "12 - 7", "hasil": "5"})
mc("c3", "sedang", K, Pr, S3, "Kue bolu = 9 kelereng. Donat = 4 kelereng. Berapa kelereng total berat keduanya?", ["13 kelereng", "12 kelereng", "14 kelereng", "11 kelereng"], "A", "9 + 4 = 13 kelereng.", verifikasi={"ekspresi": "9 + 4", "hasil": "13"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Benda A = 6 kelereng, B = 9 kelereng, C = 3 kelereng. Benda terberat adalah ....", ["benda B", "benda A", "benda C", "sama semua"], "A", "Benda B memiliki jumlah kelereng terbanyak (9 kelereng).")
mc("c4", "sedang", T, Kn, S2, "Mengapa gantungan baju harus lurus mendatar saat menimbang?", ["karena itu tanda beban kiri dan kanan sama berat", "karena gantungan baju mudah patah", "agar kelereng tidak menggelinding", "agar terlihat rapi"], "A", "Posisi mendatar menandakan keseimbangan beban kedua sisi.")
tf("c4", "sedang", T, Kn, S3, "Urutan benda dari teringan: 3 kelereng, 7 kelereng, 11 kelereng.", "Benar", "3 < 7 < 11 adalah urutan dari teringan ke terberat.")
tf("c4", "sedang", T, Kn, S4, "Menimbang dua buku dengan kelereng berbeda ukuran menghasilkan perbandingan yang adil.", "Salah", "Ukuran penimbang berbeda membuat perbandingan menjadi tidak adil.")
sa("c4", "sedang", T, Kn, S4, "Bola = 15 kelereng. Kok bulu tangkis = 3 kelereng. Berapa selisihnya?", "12", "15 - 3 = 12 kelereng.", verifikasi={"ekspresi": "15 - 3", "hasil": "12"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Jika 1 jeruk = 4 kelereng, berapa kelereng berat 3 jeruk?", ["12 kelereng", "10 kelereng", "14 kelereng", "8 kelereng"], "A", "3 x 4 = 12 kelereng.", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})
mc("c4", "sedang", X, Kn, S2, "Sisi kiri ada 1 mangga. Sisi kanan ada 5 kelereng tapi sisi kiri masih turun. Artinya?", ["mangga lebih berat dari 5 kelereng", "mangga lebih ringan dari 5 kelereng", "mangga seimbang", "kelereng terlalu banyak"], "A", "Sisi mangga turun berarti mangga lebih berat dari 5 kelereng.")
tf("c4", "sedang", X, Kn, S4, "Buku seberat 5 kelereng lebih berat daripada sepatu seberat 8 kelereng.", "Salah", "5 kelereng lebih sedikit dari 8 kelereng, jadi buku lebih ringan.")
mc("c4", "sulit", X, Me, S3, "Benda A = 14 kelereng, B = 6 kelereng. Berapa selisih kelereng kedua benda?", ["8 kelereng", "7 kelereng", "9 kelereng", "6 kelereng"], "A", "14 - 6 = 8 kelereng.", verifikasi={"ekspresi": "14 - 6", "hasil": "8"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Mengapa air tidak cocok digunakan sebagai satuan butiran penimbang tak baku?", ["karena air berbentuk cair dan sulit dihitung satu-satu", "karena air terlalu berat", "karena air tidak berwarna", "karena air dingin"], "A", "Air cair tidak berupa satuan butiran yang dapat dihitung cacahnya dengan mudah.")
mc("c4", "sulit", K, Me, S2, "Kotak pensil = 8 koin. Diambil 3 koin dari timbangan. Berapa koin tersisa?", ["5 koin", "4 koin", "6 koin", "3 koin"], "A", "8 - 3 = 5 koin.", verifikasi={"ekspresi": "8 - 3", "hasil": "5"})
tf("c4", "sulit", K, Me, S3, "Sebuah melon = 20 kelereng. Dua melon setara dengan 30 kelereng.", "Salah", "Dua melon setara dengan 20 + 20 = 40 kelereng, bukan 30.")
mc("c4", "sulit", K, Me, S4, "Paket A = 16 kelereng. Paket B = 9 kelereng. Berapa selisih berat paket A dan B?", ["7 kelereng", "6 kelereng", "8 kelereng", "5 kelereng"], "A", "16 - 9 = 7 kelereng.", verifikasi={"ekspresi": "16 - 9", "hasil": "7"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Buku = 7 kelereng. Tempat pensil = 6 kelereng. Berapa kelereng total keduanya?", ["13 kelereng", "12 kelereng", "14 kelereng", "11 kelereng"], "A", "7 + 6 = 13 kelereng.", verifikasi={"ekspresi": "7 + 6", "hasil": "13"})
mc("c5", "sedang", T, Me, S2, "Timbangan sisi kiri ada apel (6 kelereng). Sisi kanan baru ada 2 kelereng. Berapa kelereng kurangnya?", ["4 kelereng", "3 kelereng", "5 kelereng", "2 kelereng"], "A", "6 - 2 = 4 kelereng.", verifikasi={"ekspresi": "6 - 2", "hasil": "4"})
mc("c5", "sedang", T, Me, S3, "Benda A = 10 koin. Benda B = 14 koin. Benda manakah yang membutuhkan koin lebih sedikit?", ["benda A", "benda B", "keduanya sama", "tidak tahu"], "A", "Benda A butuh 10 koin, lebih sedikit daripada 14 koin.")
mc("c5", "sulit", T, Me, S4, "Dayu menimbang pensil = 3 klip. Udin menimbang pensil = 3 koin. Mengapa tidak boleh dibandingkan?", ["karena klip dan koin memiliki berat yang berbeda", "karena pensilnya warna-warni", "karena Dayu dan Udin beda kelas", "karena timbangannya rusak"], "A", "Satuan ukur yang berbeda jenis tidak dapat dibandingkan nilainya secara langsung.")

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Sebuah mangga = 8 kelereng. Pepaya = 15 kelereng. Berapa selisih kelerengnya?", ["7 kelereng", "6 kelereng", "8 kelereng", "5 kelereng"], "A", "15 - 8 = 7 kelereng.", verifikasi={"ekspresi": "15 - 8", "hasil": "7"})
mc("c5", "sulit", K, Me, S3, "1 buku = 5 kelereng. Jika ada 3 buku, berapa kelereng yang dibutuhkan?", ["15 kelereng", "12 kelereng", "16 kelereng", "10 kelereng"], "A", "3 x 5 = 15 kelereng.", verifikasi={"ekspresi": "3 * 5", "hasil": "15"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Rancanglah langkah mengukur berat apel memakai gantungan baju dan kelereng!", ["taruh apel di kantong kiri lalu masukkan kelereng satu-satu di kanan sampai seimbang", "masukkan apel dan kelereng di satu kantong yang sama", "gantungkan apel tanpa kelereng sama sekali", "lempar kelereng ke arah gantungan baju"], "A", "Apel ditaruh di satu sisi dan kelereng dimasukkan bertahap ke sisi lain hingga seimbang.")
mc("c6", "sulit", K, Me, S4, "Susunlah aturan penting saat membandingkan berat 3 benda dengan timbangan tak baku!", ["gunakan jenis dan ukuran satuan penimbang yang sama persis untuk semua benda", "gunakan benda penimbang yang berbeda-beda agar seru", "ukur tanpa menunggu timbangan seimbang", "campur kelereng, koin, dan batu kerikil"], "A", "Aturan utama: gunakan satuan penimbang yang seragam untuk semua pengukuran.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "1 nanas = 10 kelereng. 1 jeruk = 4 kelereng. Berapa kelereng untuk 1 nanas dan 2 jeruk?", ["18 kelereng", "16 kelereng", "20 kelereng", "14 kelereng"], "A", "10 + 4 + 4 = 18 kelereng.", verifikasi={"ekspresi": "10 + 4 + 4", "hasil": "18"})
mc("c6", "sulit", P, Me, S3, "Kotak A = 8 koin. Kotak B = 11 koin. Kotak C = 5 koin. Berapa total koin ketiganya?", ["24 koin", "22 koin", "25 koin", "20 koin"], "A", "8 + 11 + 5 = 24 koin.", verifikasi={"ekspresi": "8 + 11 + 5", "hasil": "24"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab24_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab24.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
