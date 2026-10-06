#!/usr/bin/env python3
"""
Generator dan validator Bab 32 Matematika Kelas 1 SD:
"Kesalahan Umum: Mengira Bentuk Bergantung pada Ukuran atau Arah" (Fase A)
bab_id: 00b19061-0104-4284-a221-dc7082a25755
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "e1f2a34b5c01"  # Ukuran Berbeda, Bentuk Tetap Sama
S2 = "f2a3b45c6d12"  # Bentuk Diputar Tidak Berubah Nama
S3 = "a3b4c56d7e23"  # Warna dan Posisi Bukan Penentu Bentuk
S4 = "b4c5d67e8f34"  # Menghitung Sisi dan Sudut dengan Teliti

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Lihatlah dua buah segitiga ini.
Satu segitiga berukuran sangat kecil.
Satu segitiga berukuran sangat besar.
Keduanya sama-sama memiliki 3 sisi.
Keduanya juga memiliki 3 sudut.
Maka keduanya tetap bangun segitiga.
Ukuran besar tidak mengubah nama.
Ukuran kecil juga tetap sama.

:::definition
title: Ukuran Bukan Penentu Bentuk
Bangun datar tetap memiliki nama yang sama walau diperbesar atau diperkecil.
:::"""

s2_content = """Sekarang kita putar kertas segitiga.
Ujung lancipnya menghadap ke bawah.
Apakah bentuknya berubah menjadi lain?
Tentu tidak, namanya tetap segitiga.
Persegi yang diputar miring wajik.
Tetap memiliki 4 sisi lurus.
Namanya tetaplah bangun segiempat.
Arah putaran tidak mengubah bentuk.

:::steps
title: Memeriksa Bentuk yang Diputar
1. Amati bangun yang posisinya terbalik atau miring.
2. Hitung jumlah sisi pembatasnya yang lurus.
3. Hitung jumlah titik sudutnya di setiap pojok.
:::"""

s3_content = """Warna benda juga bukan penentu.
Segitiga warna merah tetap segitiga.
Segitiga warna biru juga segitiga.
Garis tebal tidak mengubah bentuk.
Garis putus-putus juga tetap sama.
Jangan terkecoh oleh warna-warni.
Jangan terkecoh oleh posisi miring.
Ciri bentuk ada pada sisinya."""

s4_content = """Bagaimana cara memeriksa bentuk tepat?
Hitunglah jumlah sisinya yang lurus.
Hitunglah jumlah sudut lancipnya.
Jika ada 3 sisi, itu segitiga.
Jika ada 4 sisi, itu segiempat.

:::common_trap
title: Bentuk Tidak Berubah Saat Diputar
Segitiga terbalik tetap segitiga.
Persegi miring tetap segiempat.
Arah putar tidak mengubah bentuk.
Jangan tertipu oleh arah hadapnya.
Selalu hitung sisi dan sudutnya.
:::

:::callout
variant: summary
title: Ringkasan
text: Ukuran dan arah putaran tidak mengubah bentuk. Segitiga selalu 3 sisi dan segiempat selalu 4 sisi.
:::"""

sections = [
    {
        "id": S1,
        "title": "Ukuran Berbeda, Bentuk Tetap Sama",
        "minutes": 6,
        "goal": "Siswa memahami bahwa ukuran besar atau kecil tidak mengubah identitas bentuk bangun datar.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Bentuk Diputar Tidak Berubah Nama",
        "minutes": 6,
        "goal": "Siswa memahami bahwa orientasi atau arah putaran bangun tidak mengubah jenis bentuk bangun datar.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Warna dan Posisi Bukan Penentu Bentuk",
        "minutes": 6,
        "goal": "Siswa dapat membedakan atribut non-esensial (warna, ketebalan) dari atribut esensial bentuk geometri.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menghitung Sisi dan Sudut dengan Teliti",
        "minutes": 6,
        "goal": "Siswa terampil mengidentifikasi bentuk bangun datar berdasarkan perhitungan jumlah sisi dan sudutnya.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Mengira Bentuk Bergantung pada Ukuran atau Arah",
    "topic": "Mengenal Bentuk Bangun Datar dan Bangun Ruang",
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
# 2. DEFINISI BANK 50 SOAL BAB 32
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
mc("c1", "mudah", D, F, S1, "Sebuah segitiga berukuran sangat besar tetap dinamakan ....", ["segitiga", "segiempat", "lingkaran", "kubus"], "A", "Ukuran besar tidak mengubah nama bangun segitiga.")
tf("c1", "mudah", D, F, S2, "Segitiga yang diputar ujungnya menghadap ke bawah tetaplah segitiga.", "Benar", "Arah putaran tidak mengubah bentuk bangun datar.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Persegi yang diputar miring seperti ketupat tetap merupakan bangun ....", ["segiempat", "segitiga", "lingkaran", "bola"], "A", "Persegi miring tetap memiliki 4 sisi sehingga segiempat.")
mc("c1", "mudah", T, F, S3, "Segitiga yang diwarnai merah dan biru memiliki bentuk yang ....", ["sama", "berbeda jauh", "berubah jadi segiempat", "hilang sisinya"], "A", "Warna tidak memengaruhi bentuk bangun datar.")
sa("c1", "mudah", T, F, S4, "Berapa banyak sisi pada segitiga yang diputar terbalik?", "3", "Segitiga terbalik tetap memiliki 3 sisi.", verifikasi={"ekspresi": "3", "hasil": "3"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Bangun datar selalu ditentukan oleh jumlah ....", ["sisi dan sudutnya", "warna dan tebal garisnya", "besar kecilnya kertas", "tempat diletakkannya"], "A", "Identitas bangun datar ditentukan oleh sisi dan sudutnya.", "Mengira warna atau ukuran menentukan nama bangun")
tf("c2", "mudah", D, Kn, S1, "Bila segitiga digambar sangat kecil, namanya berubah menjadi titik.", "Salah", "Meskipun kecil, selama punya 3 sisi tetap segitiga.")

# Remedial (2)
mc("c2", "mudah", R, F, S2, "Mengapa persegi yang diputar miring tetap disebut segiempat?", ["karena tetap dibatasi oleh 4 sisi lurus dan 4 sudut", "karena warnanya tidak berubah", "karena ukurannya membesar", "karena bisa menggelinding"], "A", "Tetap memiliki 4 sisi lurus dan 4 sudut.", "Mengira persegi diputar miring bukan lagi segiempat")
mc("c2", "mudah", R, Kn, S3, "Apakah mengganti warna kertas mengubah bentuk bangun datar?", ["tidak mengubah bentuk sama sekali", "ya, bentuk langsung berubah", "berubah menjadi lingkaran", "sisinya bertambah banyak"], "A", "Warna adalah atribut luar yang tidak mengubah bentuk.", "Mengira warna memengaruhi bentuk geometri")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Ada 3 segitiga besar dan 4 segitiga kecil. Berapa total segitiga?", ["7 segitiga", "6 segitiga", "8 segitiga", "5 segitiga"], "A", "3 + 4 = 7 segitiga.", verifikasi={"ekspresi": "3 + 4", "hasil": "7"})
mc("c2", "mudah", T, Kn, S2, "Ada 5 segiempat tegak dan 3 segiempat miring. Total segiempat?", ["8 segiempat", "7 segiempat", "9 segiempat", "6 segiempat"], "A", "5 + 3 = 8 segiempat.", verifikasi={"ekspresi": "5 + 3", "hasil": "8"})
tf("c2", "mudah", T, Kn, S3, "Lingkaran kecil dan lingkaran raksasa keduanya tetap bangun lingkaran.", "Benar", "Ukuran tidak mengubah bentuk lingkaran.")
sa("c2", "mudah", T, Kn, S4, "Sebuah bangun punya 4 sisi lurus walau posisinya miring. Berapa sudutnya?", "4", "Segiempat selalu memiliki 4 sudut.", verifikasi={"ekspresi": "4", "hasil": "4"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Udin melihat segitiga dengan pucuk ke bawah. Bentuk bangun itu adalah ....", ["segitiga", "segiempat", "lingkaran", "balok"], "A", "Segitiga dengan arah hadap apa pun tetap segitiga.", "Terkecoh arah lancip segitiga ke bawah")
mc("c3", "sedang", R, Pr, S4, "Ada 2 segitiga terbalik. Berapa total seluruh sisinya?", ["6 sisi", "5 sisi", "7 sisi", "4 sisi"], "A", "2 x 3 = 6 sisi.", "Salah menghitung sisi bangun yang posisinya diputar", verifikasi={"ekspresi": "2 * 3", "hasil": "6"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Dua segitiga kecil punya 6 sisi. Satu segitiga besar punya 3 sisi. Total sisi?", ["9 sisi", "8 sisi", "10 sisi", "7 sisi"], "A", "6 + 3 = 9 sisi.", verifikasi={"ekspresi": "6 + 3", "hasil": "9"})
mc("c3", "sedang", T, Pr, S2, "Tiga segiempat diputar miring. Berapa total seluruh sudut ketiganya?", ["12 sudut", "10 sudut", "14 sudut", "9 sudut"], "A", "3 x 4 = 12 sudut.", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})
tf("c3", "sedang", T, Pr, S3, "Menggambar segitiga dengan garis putus-putus menjadikannya bangun segiempat.", "Salah", "Garis putus-putus tetap membentuk segitiga jika ada 3 sisi.")
mc("c3", "sedang", T, Pr, S4, "Di papan ada 9 segitiga berbagai arah. 4 segitiga dihapus. Berapa segitiga sisa?", ["5 segitiga", "4 segitiga", "6 segitiga", "3 segitiga"], "A", "9 - 4 = 5 segitiga.", verifikasi={"ekspresi": "9 - 4", "hasil": "5"})
tf("c3", "sedang", T, Pr, S1, "Segitiga raksasa di lapangan memiliki sisi lebih banyak dari segitiga di buku.", "Salah", "Semua segitiga memiliki tepat 3 sisi tanpa memandang ukuran.")
sa("c3", "mudah", T, Pr, S4, "Ada 2 segiempat besar dan 1 segiempat kecil. Berapa total sudut ketiganya?", "12", "3 x 4 = 12 sudut.", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Budi punya 8 kartu lingkaran kecil dan 4 lingkaran besar. Total kartu lingkaran?", ["12 kartu", "11 kartu", "13 kartu", "10 kartu"], "A", "8 + 4 = 12 kartu lingkaran.", verifikasi={"ekspresi": "8 + 4", "hasil": "12"})
mc("c3", "sedang", X, Pr, S2, "Lani punya 7 segiempat tegak dan 6 segiempat miring. Total segiempat?", ["13 segiempat", "12 segiempat", "14 segiempat", "11 segiempat"], "A", "7 + 6 = 13 segiempat.", verifikasi={"ekspresi": "7 + 6", "hasil": "13"})
tf("c3", "sedang", X, Pr, S4, "Persegi yang diputar miring 45 derajat tetap memiliki tepat 4 titik sudut.", "Benar", "Posisi putar tidak mengurangi atau menambah titik sudut.")
sa("c3", "sedang", X, Pr, S1, "Ada 15 segitiga di kertas. 6 segitiga berukuran kecil. Berapa segitiga besar?", "9", "15 - 6 = 9 segitiga.", verifikasi={"ekspresi": "15 - 6", "hasil": "9"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Edo menggambar 5 segitiga tegak dan 5 segitiga terbalik. Berapa total segitiga?", ["10 segitiga", "9 segitiga", "11 segitiga", "8 segitiga"], "A", "5 + 5 = 10 segitiga.", verifikasi={"ekspresi": "5 + 5", "hasil": "10"})
mc("c3", "sedang", K, Pr, S4, "Dua segiempat diputar miring. Berapa total sisi kedua segiempat itu?", ["8 sisi", "7 sisi", "9 sisi", "6 sisi"], "A", "2 x 4 = 8 sisi.", verifikasi={"ekspresi": "2 * 4", "hasil": "8"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Mengapa sebuah uang koin kecil dan roda sepeda besar sama-sama disebut lingkaran?", ["keduanya sama-sama dibatasi satu garis lengkung bulat utuh", "keduanya sama-sama terbuat dari besi", "keduanya berputar bersamaan", "keduanya bernilai sama"], "A", "Ciri geometri lingkaran sama-sama garis lengkung bulat.")
mc("c4", "sedang", T, Kn, S2, "Jika selembar kartu persegi diputar sembarang arah, hal yang TIDAK berubah adalah ....", ["jumlah sisi dan jumlah sudutnya", "arah hadap pojoknya", "kemiringan sisinya", "letak bayangannya"], "A", "Jumlah sisi dan sudut tetap tidak berubah.")
tf("c4", "sedang", T, Kn, S3, "Segitiga warna kuning memiliki sudut lebih runcing daripada segitiga warna hijau.", "Salah", "Warna tidak ada hubungannya dengan ukuran sudut bangun.")
tf("c4", "sedang", T, Kn, S4, "Untuk menentukan bentuk bangun, kita cukup menghitung jumlah sisi lurusnya.", "Benar", "Menghitung jumlah sisi lurus memastikan jenis bangun datar.")
sa("c4", "sedang", T, Kn, S4, "Ada 16 bangun di meja. 7 bangun berbentuk segiempat miring. Sisanya segitiga?", "9", "16 - 7 = 9 bangun.", verifikasi={"ekspresi": "16 - 7", "hasil": "9"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Manakah dari kelompok bangun berikut yang semuanya tetap merupakan bangun segitiga?", ["segitiga besar, segitiga kecil, dan segitiga terbalik", "segitiga, lingkaran, dan bola", "buku tulis, pintu, dan penggaris segitiga", "kubus, balok, dan tabung"], "A", "Segitiga besar, kecil, terbalik semuanya tetap segitiga.")
mc("c4", "sedang", X, Kn, S2, "Ada 14 segiempat miring wajik. Diambil 6 buah. Berapa segiempat miring sisa?", ["8 segiempat", "7 segiempat", "9 segiempat", "6 segiempat"], "A", "14 - 6 = 8 buah.", verifikasi={"ekspresi": "14 - 6", "hasil": "8"})
tf("c4", "sedang", X, Kn, S2, "Sebuah lingkaran jika diputar arah hadapnya tetap berupa bangun lingkaran.", "Benar", "Lingkaran diputar ke arah mana pun tetaplah lingkaran sempurna.")
mc("c4", "sulit", X, Me, S3, "Tiga segitiga merah dan 2 segitiga hijau. Berapa total sudut seluruh segitiga itu?", ["15 sudut", "14 sudut", "16 sudut", "12 sudut"], "A", "(3 + 2) x 3 = 15 sudut.", verifikasi={"ekspresi": "(3 + 2) * 3", "hasil": "15"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Siti mengira bangun persegi kecil bukan segiempat. Cara membetulkan pendapatnya adalah ....", ["mengajak Siti menghitung keempat sisinya yang lurus", "mengganti warna kertas Siti", "memperbesar kertas itu", "merobek kertas itu"], "A", "Membimbing menghitung 4 sisi lurus membuktikan segiempat.")
mc("c4", "sulit", K, Me, S2, "Ada 18 bangun datar miring. 11 berbentuk segiempat, sisanya segitiga. Berapa segitiga?", ["7 segitiga", "6 segitiga", "8 segitiga", "5 segitiga"], "A", "18 - 11 = 7 segitiga.", verifikasi={"ekspresi": "18 - 11", "hasil": "7"})
tf("c4", "sulit", K, Me, S3, "Sebuah kertas dipotong kecil-kecil berbentuk segitiga. Sifat segitiganya hilang lenyap.", "Salah", "Potongan bentuk segitiga tetap memiliki sifat segitiga.")
mc("c4", "sulit", K, Me, S4, "Empat segiempat (tiap bangun 4 sisi). Berapa sisi yang harus ditambah agar jadi 20?", ["4 sisi", "3 sisi", "5 sisi", "2 sisi"], "A", "20 - 16 = 4 sisi.", verifikasi={"ekspresi": "20 - (4 * 4)", "hasil": "4"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Dua segitiga raksasa dan 2 segitiga mini. Berapa total sisi keempat segitiga itu?", ["12 sisi", "10 sisi", "14 sisi", "9 sisi"], "A", "4 x 3 = 12 sisi.", verifikasi={"ekspresi": "4 * 3", "hasil": "12"})
mc("c5", "sedang", T, Me, S2, "Tiga segiempat tegak dan 1 segiempat miring (tiap bangun 4 sudut). Total sudut?", ["16 sudut", "14 sudut", "18 sudut", "12 sudut"], "A", "4 x 4 = 16 sudut.", verifikasi={"ekspresi": "4 * 4", "hasil": "16"})
mc("c5", "sedang", T, Me, S3, "Budi mewarnai 5 segitiga merah dan 5 lingkaran biru. Berapa total seluruh bangun?", ["10 bangun", "9 bangun", "11 bangun", "8 bangun"], "A", "5 + 5 = 10 bangun datar.", verifikasi={"ekspresi": "5 + 5", "hasil": "10"})
mc("c5", "sulit", T, Me, S4, "Ada 2 segitiga terbalik dan 2 segiempat wajik. Berapa total seluruh sudutnya?", ["14 sudut", "12 sudut", "15 sudut", "13 sudut"], "A", "(2 x 3) + (2 x 4) = 6 + 8 = 14 sudut.", verifikasi={"ekspresi": "2 * 3 + 2 * 4", "hasil": "14"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Doni punya 6 lingkaran besar dan 8 lingkaran kecil. Berapa total keping lingkaran?", ["14 lingkaran", "13 lingkaran", "15 lingkaran", "12 lingkaran"], "A", "6 + 8 = 14 lingkaran.", verifikasi={"ekspresi": "6 + 8", "hasil": "14"})
mc("c5", "sulit", K, Me, S3, "Ada 15 kartu bangun warna-warni. 8 kartu segitiga, sisanya segiempat. Berapa segiempat?", ["7 segiempat", "6 segiempat", "8 segiempat", "5 segiempat"], "A", "15 - 8 = 7 segiempat.", verifikasi={"ekspresi": "15 - 8", "hasil": "7"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Jika kamu ingin membuktikan kepada teman bahwa bangun wajik adalah segiempat, apa langkahmu?", ["menghitung bersama bahwa bangun itu memiliki 4 sisi lurus dan 4 sudut", "mewarnai bangun itu dengan warna kesukaannya", "membalik kertas hingga teman pusing", "menyuruh teman diam"], "A", "Membuktikan secara logis lewat perhitungan 4 sisi dan 4 sudut.")
mc("c6", "sulit", K, Me, S4, "Kelompokkan bangun-bangun berikut: segitiga kecil, segitiga terbalik, segiempat besar, segiempat miring!", ["segitiga (kecil dan terbalik), segiempat (besar dan miring)", "semua bangun di atas termasuk lingkaran", "segitiga terbalik adalah lingkaran", "segiempat miring adalah segitiga"], "A", "Pengelompokan tepat berdasarkan jenis sisi dan sudutnya.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Ada 3 segitiga kecil dan 3 segiempat besar. Berapa total seluruh sisinya?", ["21 sisi", "18 sisi", "24 sisi", "15 sisi"], "A", "(3 x 3) + (3 x 4) = 9 + 12 = 21 sisi.", verifikasi={"ekspresi": "3 * 3 + 3 * 4", "hasil": "21"})
mc("c6", "sulit", P, Me, S3, "Dua segiempat miring dan 3 segitiga terbalik. Berapa total seluruh sudutnya?", ["17 sudut", "16 sudut", "18 sudut", "15 sudut"], "A", "(2 x 4) + (3 x 3) = 8 + 9 = 17 sudut.", verifikasi={"ekspresi": "2 * 4 + 3 * 3", "hasil": "17"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab32_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab32.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
