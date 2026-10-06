#!/usr/bin/env python3
"""
Generator dan validator Bab 36 Matematika Kelas 1 SD:
"Membandingkan Banyak Data pada Piktogram" (Fase A)
bab_id: b6371ddd-513c-41f0-83f0-6baf8594d2a8
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a1b2c34d5e11"  # Menentukan Data Terbanyak dan Paling Sedikit
S2 = "b2c3d45e6f22"  # Membandingkan Lebih Banyak dan Lebih Sedikit
S3 = "c3d4e56f7a33"  # Menghitung Selisih dengan Memasangkan Gambar
S4 = "d4e5f67a8b44"  # Mengurutkan Kategori Data dari Terbanyak

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Lihatlah piktogram buah di papan.
Ada baris gambar yang sangat panjang.
Ada juga baris gambar yang pendek.
Baris terpanjang adalah data terbanyak.
Baris terpendek adalah data paling sedikit.
Hanya dengan melihat sekilas mata.
Kita bisa langsung tahu pemenangnya.
Membaca piktogram sangat mudah sekali.

:::definition
title: Membandingkan Baris Data
Baris simbol terpanjang menunjukkan data terbanyak. Baris terpendek menunjukkan data tersedikit.
:::"""

s2_content = """Mari kita bandingkan dua baris.
Baris apel ada lima gambar.
Baris jeruk ada tiga gambar.
Lima lebih banyak dari tiga.
Maka peminat apel lebih banyak.
Peminat jeruk tentu lebih sedikit.
Jika jumlah gambarnya sama persis.
Artinya kedua data sama banyak.

:::steps
title: Cara Membandingkan Dua Kategori
1. Hitung jumlah gambar pada baris pertama.
2. Hitung jumlah gambar pada baris kedua.
3. Bandingkan angka mana yang lebih besar.
:::"""

s3_content = """Bagaimana cara mencari selisih gambar?
Pasangkan satu gambar apel dan jeruk.
Pasangan pertama, kedua, dan ketiga.
Sekarang lihatlah gambar yang tersisa.
Ada dua apel tidak punya pasangan.
Dua itulah selisih banyak gambarnya.
Cara memasangkan gambar sangat praktis.
Kita terhindar dari salah hitung."""

s4_content = """Sekarang kita bisa mengurutkan datanya.
Urutkan dari baris yang paling banyak.
Lalu ke baris yang sedang.
Terakhir baris yang paling sedikit.
Semua urutan tersusun sangat rapi.

:::common_trap
title: Menghitung Selisih Gambar
Selisih adalah sisa yang tidak berpasangan.
Pasangkan gambar satu per satu.
Gambar yang tidak punya pasangan adalah selisih.
Jangan menjumlahkan kedua data saat mencari selisih.
Hitunglah selisih dengan cermat.
:::

:::callout
variant: summary
title: Ringkasan
text: Bandingkan panjang baris gambar. Pasangkan simbol satu per satu. Gambar tanpa pasangan adalah selisihnya.
:::"""

sections = [
    {
        "id": S1,
        "title": "Menentukan Data Terbanyak dan Paling Sedikit",
        "minutes": 6,
        "goal": "Siswa dapat menentukan kategori dengan kuantitas tertinggi dan terendah pada diagram piktogram.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Membandingkan Lebih Banyak dan Lebih Sedikit",
        "minutes": 6,
        "goal": "Siswa dapat membandingkan dua kategori data menggunakan konsep lebih banyak, lebih sedikit, atau sama banyak.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Menghitung Selisih dengan Memasangkan Gambar",
        "minutes": 6,
        "goal": "Siswa dapat menentukan selisih kuantitas dua kategori melalui metode pemasangan satu-satu (one-to-one matching).",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Mengurutkan Kategori Data dari Terbanyak",
        "minutes": 6,
        "goal": "Siswa dapat menyusun urutan kategori data piktogram dari yang paling banyak hingga paling sedikit dan sebaliknya.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membandingkan Banyak Data pada Piktogram",
    "topic": "Diagram dan Piktogram",
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
# 2. DEFINISI BANK 50 SOAL BAB 36
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
mc("c1", "mudah", D, F, S1, "Baris simbol gambar yang paling panjang pada piktogram menunjukkan data ....", ["paling banyak", "paling sedikit", "paling kecil", "kosong"], "A", "Baris terpanjang menunjukkan data terbanyak.")
tf("c1", "mudah", D, F, S2, "Jika baris A ada 5 apel dan baris B 5 jeruk, kedua buah sama banyak.", "Benar", "Angka 5 sama dengan angka 5.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S3, "Baris bintang ada 4 gambar, baris bulan ada 3 gambar. Selisihnya adalah ....", ["1 gambar", "2 gambar", "3 gambar", "0 gambar"], "A", "4 - 3 = 1 gambar.", verifikasi={"ekspresi": "4 - 3", "hasil": "1"})
mc("c1", "mudah", T, F, S4, "Urutan bilangan 2, 5, 8 dari yang paling banyak adalah ....", ["8, 5, 2", "2, 5, 8", "5, 2, 8", "8, 2, 5"], "A", "Urutan dari terbesar: 8, 5, 2.")
sa("c1", "mudah", T, F, S1, "Piktogram: pensil 7 gambar, penghapus 4 gambar. Benda apakah yang paling banyak?", "pensil", "7 pensil lebih banyak dari 4 penghapus.")

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Bagaimana cara mudah mencari selisih dua baris gambar pada piktogram?", ["memasangkan gambar satu per satu lalu menghitung sisanya", "menjumlahkan seluruh gambar kedua baris", "menghapus salah satu baris", "menebak tanpa menghitung"], "A", "Metode pemasangan 1-ke-1 mempermudah melihat selisih.", "Menjumlahkan dua kelompok data saat mencari selisih")
tf("c2", "mudah", D, Kn, S1, "Baris gambar yang lebih pendek selalu menunjukkan jumlah benda yang lebih banyak.", "Salah", "Baris lebih pendek menunjukkan jumlah yang lebih sedikit.")

# Remedial (2)
mc("c2", "mudah", R, F, S2, "Baris apel 6 gambar, baris pisang 4 gambar. Pernyataan yang benar adalah ....", ["apel lebih banyak dari pisang", "pisang lebih banyak dari apel", "apel sama banyak dengan pisang", "apel lebih sedikit dari pisang"], "A", "6 apel lebih banyak dari 4 pisang.", "Keliru membandingkan kuantitas dua baris piktogram")
mc("c2", "mudah", R, Kn, S3, "Ada 5 gambar buku dan 2 pensil. Berapa gambar buku yang tidak punya pasangan?", ["3 buku", "2 buku", "4 buku", "1 buku"], "A", "5 - 2 = 3 buku.", "Salah menghitung sisa pasangan gambar", verifikasi={"ekspresi": "5 - 2", "hasil": "3"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Piktogram hewan: ayam 8 gambar, bebek 3 gambar. Hewan yang paling sedikit adalah ....", ["bebek", "ayam", "keduanya sama", "semua banyak"], "A", "Bebek paling sedikit yaitu 3 gambar.")
mc("c2", "mudah", T, Kn, S2, "Baris mangga 5 buah, baris melon 3 buah. Berapa lebihnya mangga dari melon?", ["2 buah", "1 buah", "3 buah", "4 buah"], "A", "5 - 3 = 2 buah.", verifikasi={"ekspresi": "5 - 3", "hasil": "2"})
tf("c2", "mudah", T, Kn, S3, "Selisih antara 7 gambar bintang dan 4 gambar bintang adalah 3 gambar.", "Benar", "7 - 4 = 3 gambar.")
sa("c2", "mudah", T, Kn, S4, "Data: topi 6, dasi 9, sepatu 4. Benda apakah yang paling banyak?", "dasi", "Dasi memiliki 9 gambar (terbanyak).")

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Piktogram: bola merah 8 buah, bola biru 5 buah. Selisih kedua bola?", ["3 bola", "2 bola", "4 bola", "1 bola"], "A", "8 - 5 = 3 bola.", "Keliru mengurangkan data selisih", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})
mc("c3", "sedang", R, Pr, S4, "Urutkan data peminat buah: apel 7, jeruk 3, pisang 5 dari yang tersedikit!", ["jeruk, pisang, apel", "apel, pisang, jeruk", "pisang, jeruk, apel", "semua urutan sama"], "A", "Urutan dari tersedikit: jeruk (3), pisang (5), apel (7).", "Terbalik mengurutkan data dari tersedikit")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Piktogram kelereng: Edo 6 butir, Beni 4 butir. Berapa total kelereng keduanya?", ["10 butir", "9 butir", "11 butir", "8 butir"], "A", "6 + 4 = 10 butir.", verifikasi={"ekspresi": "6 + 4", "hasil": "10"})
mc("c3", "sedang", T, Pr, S2, "Lani punya 9 stiker bunga, Siti punya 6 stiker. Siti kurang berapa agar sama?", ["3 stiker", "2 stiker", "4 stiker", "1 stiker"], "A", "9 - 6 = 3 stiker.", verifikasi={"ekspresi": "9 - 6", "hasil": "3"})
tf("c3", "sedang", T, Pr, S3, "Memasangkan 6 apel dengan 6 jeruk menghasilkan selisih nol (sama banyak).", "Benar", "6 - 6 = 0, tidak ada gambar tersisa.")
mc("c3", "sedang", T, Pr, S4, "Urutkan banyak hewan dari yang terbanyak: burung 9, kucing 6, kelinci 4!", ["burung, kucing, kelinci", "kelinci, kucing, burung", "kucing, burung, kelinci", "semua sama"], "A", "Urutan dari terbanyak: 9 (burung), 6 (kucing), 4 (kelinci).")
tf("c3", "sedang", T, Pr, S1, "Data yang bernilai 9 gambar lebih sedikit daripada data yang bernilai 4 gambar.", "Salah", "9 lebih banyak daripada 4.")
sa("c3", "mudah", T, Pr, S3, "Ada 8 gambar balon merah dan 5 balon kuning. Berapa selisihnya?", "3", "8 - 5 = 3 balon.", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Piktogram tabungan: Senin 7 koin, Selasa 5 koin. Selisih koin kedua hari?", ["2 koin", "1 koin", "3 koin", "4 koin"], "A", "7 - 5 = 2 koin.", verifikasi={"ekspresi": "7 - 5", "hasil": "2"})
mc("c3", "sedang", X, Pr, S2, "Piktogram minuman: teh 8 gelas, susu 5 gelas. Berapa gelas susu lebih sedikit dari teh?", ["3 gelas", "2 gelas", "4 gelas", "1 gelas"], "A", "8 - 5 = 3 gelas.", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})
tf("c3", "sedang", X, Pr, S3, "Sepuluh gambar mobil dan 7 gambar motor memiliki selisih sebanyak 3 kendaraan.", "Benar", "10 - 7 = 3 kendaraan.")
sa("c3", "sedang", X, Pr, S4, "Data boneka: beruang 9, kelinci 6. Berapa selisih banyaknya boneka?", "3", "9 - 6 = 3 boneka.", verifikasi={"ekspresi": "9 - 6", "hasil": "3"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Piktogram tanaman: mawar 9 pot, melati 7 pot. Berapa pot mawar lebih banyak?", ["2 pot", "1 pot", "3 pot", "4 pot"], "A", "9 - 7 = 2 pot.", verifikasi={"ekspresi": "9 - 7", "hasil": "2"})
mc("c3", "sedang", K, Pr, S4, "Bintang kelas: 1A ada 12, 1B ada 9, 1C ada 14. Urutan dari terbanyak?", ["1C, 1A, 1B", "1A, 1B, 1C", "1B, 1A, 1C", "1C, 1B, 1A"], "A", "Urutan dari terbanyak: 14 (1C), 12 (1A), 9 (1B).")

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Jika baris piktogram digambar dengan ukuran acak-acakan, apa kesulitan yang muncul?", ["kita tidak bisa membandingkan banyak data hanya dari panjang barisnya", "angka di piktogram hilang", "kertas piktogram terbakar", "gambar berubah sendiri"], "A", "Panjang baris hanya akurat jika ukuran simbol seragam.")
mc("c4", "sedang", T, Kn, S2, "Piktogram hobi: bola 10, renang 6, catur 3. Selisih peminat bola dan catur?", ["7 peminat", "6 peminat", "8 peminat", "5 peminat"], "A", "10 - 3 = 7 peminat.", verifikasi={"ekspresi": "10 - 3", "hasil": "7"})
tf("c4", "sedang", T, Kn, S3, "Mencari selisih data piktogram dilakukan dengan menjumlahkan kedua baris data.", "Salah", "Selisih dicari dengan pengurangan (data besar dikurangi kecil).")
tf("c4", "sedang", T, Kn, S4, "Mengurutkan piktogram dari paling sedikit berarti meletakkan baris terpanjang di awal.", "Salah", "Dari paling sedikit berarti baris terpendek diletakkan di awal.")
sa("c4", "sedang", T, Kn, S4, "Piktogram: apel 15 buah, jeruk 8 buah. Berapa selisih apel dan jeruk?", "7", "15 - 8 = 7 buah.", verifikasi={"ekspresi": "15 - 8", "hasil": "7"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Piktogram warna kesukaan: merah 9 anak, biru 7 anak, hijau 5 anak. Selisih merah dan hijau?", ["4 anak", "3 anak", "5 anak", "2 anak"], "A", "9 - 5 = 4 anak.", verifikasi={"ekspresi": "9 - 5", "hasil": "4"})
mc("c4", "sedang", X, Kn, S2, "Ada 16 buah: 9 mangga, sisanya jambu. Berapa buah mangga lebih banyak dari jambu?", ["2 buah", "1 buah", "3 buah", "4 buah"], "A", "Jambu = 16 - 9 = 7. Selisih mangga dan jambu = 9 - 7 = 2 buah.", verifikasi={"ekspresi": "9 - (16 - 9)", "hasil": "2"})
tf("c4", "sedang", X, Kn, S3, "Dua baris yang masing-masing berisi 8 simbol memiliki selisih sebanyak 8 simbol.", "Salah", "Jika kedua baris sama banyak (8 dan 8), selisihnya adalah 0.")
mc("c4", "sulit", X, Me, S4, "Piktogram: roti cokelat 10, roti nanas 6, roti stroberi 4. Urutan dari terbanyak?", ["cokelat, nanas, stroberi", "stroberi, nanas, cokelat", "nanas, cokelat, stroberi", "semua sama banyak"], "A", "Urutan dari terbanyak: 10 (cokelat), 6 (nanas), 4 (stroberi).")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Berdasarkan piktogram: kelinci 11 gambar, kucing 7 gambar, burung 4 gambar. Paling sedikit?", ["burung", "kucing", "kelinci", "semua sama"], "A", "Burung paling sedikit dengan 4 gambar.")
mc("c4", "sulit", K, Me, S2, "Piktogram baju: putih 14 lembar, batik 8 lembar. Berapa selisih baju putih dan batik?", ["6 lembar", "5 lembar", "7 lembar", "4 lembar"], "A", "14 - 8 = 6 lembar.", verifikasi={"ekspresi": "14 - 8", "hasil": "6"})
tf("c4", "sulit", K, Me, S3, "Jika selisih apel dan jeruk adalah 0, berarti apel dan jeruk sama banyak.", "Benar", "Selisih 0 artinya kuantitas kedua data persis sama.")
mc("c4", "sulit", K, Me, S4, "Data olahraga: lari 9 anak, senam 7 anak, renang 4 anak. Total seluruh peserta?", ["20 anak", "19 anak", "21 anak", "18 anak"], "A", "9 + 7 + 4 = 20 anak.", verifikasi={"ekspresi": "9 + 7 + 4", "hasil": "20"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Piktogram buah: semangka 8 buah, melon 7 buah. Total kedua buah tersebut?", ["15 buah", "14 buah", "16 buah", "13 buah"], "A", "8 + 7 = 15 buah.", verifikasi={"ekspresi": "8 + 7", "hasil": "15"})
mc("c5", "sedang", T, Me, S2, "Ada 20 siswa: 8 suka komik, 7 suka dongeng, sisanya majalah. Berapa selisih komik dan majalah?", ["3 siswa", "2 siswa", "4 siswa", "1 siswa"], "A", "Majalah = 20 - (8 + 7) = 5. Selisih = 8 - 5 = 3 siswa.", verifikasi={"ekspresi": "8 - (20 - (8 + 7))", "hasil": "3"})
mc("c5", "sedang", T, Me, S3, "Baris A ada 12 bintang, baris B ada 7. Berapa bintang yang tidak berpasangan?", ["5 bintang", "4 bintang", "6 bintang", "3 bintang"], "A", "12 - 7 = 5 bintang tanpa pasangan.", verifikasi={"ekspresi": "12 - 7", "hasil": "5"})
mc("c5", "sulit", T, Me, S4, "Piktogram mainan: yoyo 6, gasing 5, layangan 4. Berapa total seluruh mainan tradisional?", ["15 mainan", "14 mainan", "16 mainan", "13 mainan"], "A", "6 + 5 + 4 = 15 mainan.", verifikasi={"ekspresi": "6 + 5 + 4", "hasil": "15"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Piktogram bunga: mawar 10 tangkai, melati 6 tangkai. Berapa tangkai selisih mawar dan melati?", ["4 tangkai", "3 tangkai", "5 tangkai", "2 tangkai"], "A", "10 - 6 = 4 tangkai.", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})
mc("c5", "sulit", K, Me, S3, "Ada 17 bendera merah dan 9 bendera putih. Berapa selisih kedua warna bendera?", ["8 bendera", "7 bendera", "9 bendera", "6 bendera"], "A", "17 - 9 = 8 bendera.", verifikasi={"ekspresi": "17 - 9", "hasil": "8"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Piktogram: jus apel 8, jus jeruk 5, jus mangga 9. Kesimpulan analisis yang paling tepat adalah ....", ["jus mangga paling disukai dan selisihnya 4 gelas dengan jeruk", "jus jeruk paling banyak", "semua jus sama larisnya", "jus apel tidak ada peminat"], "A", "Mangga terbanyak (9), selisih dengan jeruk = 9 - 5 = 4 gelas.")
mc("c6", "sulit", K, Me, S4, "Evaluasilah urutan berikut: apel (8), jeruk (5), pisang (11). Urutan dari terbanyak yang benar adalah ....", ["pisang, apel, jeruk", "apel, jeruk, pisang", "jeruk, apel, pisang", "pisang, jeruk, apel"], "A", "Urutan dari terbanyak: 11 (pisang), 8 (apel), 5 (jeruk).")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Piktogram tabungan: kelas A punya 14 koin, kelas B punya 7 koin. Berapa selisih koin keduanya?", ["7 koin", "6 koin", "8 koin", "5 koin"], "A", "14 - 7 = 7 koin.", verifikasi={"ekspresi": "14 - 7", "hasil": "7"})
mc("c6", "sulit", P, Me, S4, "Tiga jenis buah di piktogram: 9 jeruk, 7 apel, dan 5 pir. Berapa total seluruh buah?", ["21 buah", "20 buah", "22 buah", "19 buah"], "A", "9 + 7 + 5 = 21 buah.", verifikasi={"ekspresi": "9 + 7 + 5", "hasil": "21"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab36_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab36.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
