#!/usr/bin/env python3
"""
Generator dan validator Bab 80 Matematika Kelas 2 SD:
"Kesalahan Umum: Turus Kelima Tidak Dicoret Silang" (Fase A)
bab_id: 4c5810ef-08c8-4d45-9df2-e16416c19c71
article_id: 015444ca-4a0b-4786-8d19-ee7c8b056108
quiz_id: f3dbfa2b-d3eb-46cb-b09b-6dd79d86a635
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "y1a2c3e4g501"  # Mengenal Miskonsepsi Garis Berjajar
S2 = "z2b3d4f5h602"  # Arti Coretan Miring Turus Kelima
S3 = "a3c4e5g6i703"  # Memperbaiki Turus Belum Diikat
S4 = "b4d5f6h7j804"  # Membiasakan Hitung Loncat Lima

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Ada kesalahan yang sering terjadi.
Siswa menggambar garis tegak terus-menerus.
Garis digambar panjang tanpa ikatan.
Misal ada 8 garis tegak berderet.
Mata kita menjadi sangat pusing.
Kita harus menghitung satu per satu.
Waktu terbuang dan rawan keliru.
Itu cara mencatat yang salah!

:::definition
title: Turus Tanpa Ikatan
Kesalahan membuat garis tegak berjejer tanpa mencoretkan garis kelima.
:::"""

s2_content = """Turus kelima harus dicoret miring.
Buat 4 garis tegak berjajar.
Lalu tarik garis kelima melintang.
Garis miring memotong 4 garis tegak.
Sekarang garis terikat menjadi satu.
Satu ikatan ini bernilai 5.
Garis miring adalah hitungan kelima.
Bukan garis hiasan tambahan!

:::steps
title: Cara Mengikat Turus
1. Gambar 4 garis tegak: ||||.
2. Tarik garis ke-5 miring memotong: <s>||||</s>.
3. Terbentuklah 1 ikat bernilai 5.
:::"""

s3_content = """Bagaimana memperbaiki turus yang salah?
Jika ada 7 garis tegak berjejer.
Coret garis ke-5 secara miring.
Empat garis pertama kini terikat.
Tersisa 2 garis tegak di samping.
Sekarang tampak 1 ikat dan 2 garis.
Data langsung mudah dibaca: 7!

:::common_trap
title: Mengira Garis Miring Dihitung Terpisah
Garis miring bukan garis tambahan.
Garis miring adalah data ke-5.
Satu ikat utuh tetap bernilai 5!
:::"""

s4_content = """Turus terikat sangat menyenangkan.
Kita berhitung loncat lima:
5, 10, 15, 20, dan seterusnya.
Lalu tambahkan sisa garis lepasnya.
Menghitung menjadi cepat dan tepat.
Tidak ada lagi garis terlewat.
Mencatat data menjadi sangat rapi!

:::callout
variant: summary
title: Ringkasan
text: Empat garis tegak, kelima coret miring. Hitung loncat lima.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Miskonsepsi Garis Berjajar",
        "minutes": 6,
        "goal": "Siswa mengenali kesalahan mencatat turus tanpa ikatan pada kelipatan 5.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Arti Coretan Miring Turus Kelima",
        "minutes": 6,
        "goal": "Siswa memahami bahwa goresan ke-5 mengikat 4 goresan tegak sebelumnya.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Memperbaiki Turus Belum Diikat",
        "minutes": 6,
        "goal": "Siswa mampu mengelompokkan dan mengoreksi turus garis panjang menjadi ikatan 5.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Membiasakan Hitung Loncat Lima",
        "minutes": 6,
        "goal": "Siswa terampil membaca total data turus terikat dengan strategi hitung loncat 5.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Turus Kelima Tidak Dicoret Silang",
    "topic": "Tabel dan Turus",
    "level": "Kelas 2 SD · Fase A",
    "sections": sections
}

# Verifikasi teks materi sesuai kriteria validasi
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
# 2. DEFINISI BANK 50 SOAL BAB 80
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
mc("c1", "mudah", D, F, S2, "Pada satu ikatan turus penuh, garis kelima digambar secara ....", ["miring memotong", "tegak berdiri", "melingkar bulat", "titik kecil"], "A", "Garis kelima digambar miring mencoret 4 garis tegak.")
tf("c1", "mudah", D, F, S1, "Menggambar 8 garis tegak berjejer tanpa ikatan adalah cara turus yang benar.", "Salah", "Turus harus diikat tiap kelipatan lima.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Mencatat 10 data dengan 10 garis tegak berjejer tanpa ikatan adalah cara yang ....", ["salah dan membingungkan", "sangat benar", "dianjurkan guru", "paling cepat"], "A", "Garis berjejer panjang tanpa ikatan kelipatan lima adalah cara yang salah.")
mc("c1", "mudah", T, F, S2, "Berapa banyak garis tegak yang dipotong oleh garis miring kelima?", ["4 garis", "3 garis", "5 garis", "2 garis"], "A", "Garis miring memotong tepat 4 garis tegak.", verifikasi={"ekspresi": "4 * 1", "hasil": "4"})
sa("c1", "mudah", T, F, S2, "Garis coret miring turus mewakili hitungan ke-...", "5", "Garis miring adalah hitungan ke-5.", verifikasi={"ekspresi": "5 * 1", "hasil": "5"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Mengapa garis tegak turus tidak boleh dibiarkan berjejer panjang tanpa ikatan?", ["karena mata sulit membedakan jumlahnya dan rawan salah hitung", "karena tintanya cepat habis", "karena kertas jadi rusak", "hanya anjuran"], "A", "Garis panjang tanpa kelompok menyulitkan penghitungan cepat.")
tf("c2", "mudah", D, Kn, S2, "Garis coret miring dihitung sebagai data tambahan terpisah di luar kelompok lima.", "Salah", "Garis miring adalah data ke-5 dalam kelompok tersebut.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Doni menggambar 6 garis tegak berderet: ||||||. Apa kesalahan Doni?", ["garis kelima tidak dicoret miring", "garisnya terlalu pendek", "kurang 2 garis", "warnanya salah"], "A", "Seharusnya 4 garis tegak dicoret 1 garis miring, lalu 1 garis tegak di samping.", "Menggambar garis berjejer tanpa ikatan lima")
mc("c2", "mudah", R, Kn, S2, "Satu kelompok turus: 4 garis tegak dan 1 garis miring. Totalnya adalah ....", ["5", "6", "4", "7"], "A", "4 + 1 = 5.", "Mengira garis miring tidak dihitung", verifikasi={"ekspresi": "4 + 1", "hasil": "5"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S3, "Bagaimana memperbaiki 9 garis tegak yang berjejer panjang?", ["ikat 5 garis pertama, lalu biarkan 4 garis di sampingnya", "hapus semua garis", "tambah 1 garis lagi", "beri lingkaran besar"], "A", "9 = 1 ikat lima dan 4 garis lepas.")
mc("c2", "mudah", T, Kn, S4, "Hitung loncat lima untuk 3 ikat turus penuh: 5, 10, ....", ["15", "12", "14", "20"], "A", "3 x 5 = 15.", verifikasi={"ekspresi": "3 * 5", "hasil": "15"})
tf("c2", "mudah", T, Kn, S4, "Menghitung turus terikat jauh lebih cepat daripada menghitung garis lepas satu per satu.", "Benar", "Ikatan lima memungkinkan berhitung loncat lima secara cepat.")
sa("c2", "mudah", T, Kn, S4, "Dua ikat turus penuh bernilai angka ...", "10", "2 x 5 = 10.", verifikasi={"ekspresi": "2 * 5", "hasil": "10"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Ada 12 garis tegak lurus berjejer. Jika diperbaiki, akan terbentuk ....", ["2 ikat lima dan 2 garis lepas", "1 ikat lima dan 7 garis", "3 ikat lima", "2 ikat lima dan 4 garis"], "A", "12 = (2 x 5) + 2.", "Salah mengelompokkan kelipatan 5")
mc("c3", "sedang", R, Pr, S4, "Hitung nilai turus: 3 ikat penuh dan 3 garis lepas!", ["18", "15", "16", "20"], "A", "(3 x 5) + 3 = 15 + 3 = 18.", "Mengira 3 ikat bernilai 12", verifikasi={"ekspresi": "(3 * 5) + 3", "hasil": "18"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S3, "Ada 8 garis tegak. Berapa garis miring yang harus dibuat untuk memperbaikinya?", ["1 garis miring", "2 garis miring", "3 garis miring", "0 garis miring"], "A", "8 hanya memiliki 1 kelipatan lima.", verifikasi={"ekspresi": "8 // 5", "hasil": "1"})
mc("c3", "mudah", T, Pr, S4, "Nilai dari 2 ikat turus dan 4 garis lepas adalah ....", ["14", "12", "15", "13"], "A", "10 + 4 = 14.", verifikasi={"ekspresi": "10 + 4", "hasil": "14"})
tf("c3", "sedang", T, Pr, S1, "Garis turus boleh digambar mendatar semua seperti tangga tidur.", "Salah", "Turus digambar tegak dan dicoret miring pada hitungan ke-5.")
mc("c3", "sedang", T, Pr, S2, "Jika kita menggambar garis ke-5 tegak juga, garis tersebut menjadi garis ke-....", ["5 yang belum diikat", "6 yang sah", "4 pengikat", "10"], "A", "Garis ke-5 yang tegak belum membentuk ikatan lima.")
tf("c3", "sedang", T, Pr, S3, "Mengubah deretan 10 garis tegak menjadi 2 ikat turus tidak mengubah jumlah data.", "Benar", "Nilai total tetap 10, hanya penyajiannya lebih rapi.")
sa("c3", "sedang", T, Pr, S4, "Empat ikat turus dan 3 garis bernilai angka ...", "23", "(4 x 5) + 3 = 23.", verifikasi={"ekspresi": "(4 * 5) + 3", "hasil": "23"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S3, "Ada deretan 16 garis tegak tanpa ikatan. Berapa ikat lima yang bisa dibentuk?", ["3 ikat lima", "2 ikat lima", "4 ikat lima", "1 ikat lima"], "A", "16 = (3 x 5) + 1 garis sisa.", verifikasi={"ekspresi": "16 // 5", "hasil": "3"})
mc("c3", "sedang", X, Pr, S4, "Hitung total data turus: 5 ikat penuh dan 2 garis lepas!", ["27", "25", "26", "28"], "A", "(5 x 5) + 2 = 27.", verifikasi={"ekspresi": "(5 * 5) + 2", "hasil": "27"})
tf("c3", "sedang", X, Pr, S2, "Garis coret miring turus ditarik dari kiri atas ke kanan bawah atau sebaliknya.", "Benar", "Garis miring memotong keempat garis tegak.")
sa("c3", "sedang", X, Pr, S4, "Tiga ikat turus dan 4 garis lepas sama dengan ... data.", "19", "15 + 4 = 19 data.", verifikasi={"ekspresi": "15 + 4", "hasil": "19"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Budi punya 21 garis tegak. Ia mencoret garis miring tiap 5 hitungan. Berapa ikat terbentuk?", ["4 ikat lima", "3 ikat lima", "5 ikat lima", "2 ikat lima"], "A", "21 = (4 x 5) + 1 garis sisa.", verifikasi={"ekspresi": "21 // 5", "hasil": "4"})
mc("c3", "sedang", K, Pr, S4, "Nilai data dari 6 ikat turus penuh adalah ....", ["30", "25", "35", "28"], "A", "6 x 5 = 30.", verifikasi={"ekspresi": "6 * 5", "hasil": "30"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S1
mc("c4", "sedang", T, Kn, S1, "Apa bahaya terbesar bila kita tidak mencoret miring garis kelima pada data besar?", ["sangat mudah salah hitung karena mata silau melihat deretan garis tegak", "spidol akan patah", "kertas robek sendiri", "tidak ada bahaya"], "A", "Mata manusia kesulitan membedakan jumlah garis sejajar di atas 4 tanpa kelompok.")
mc("c4", "sedang", T, Kn, S2, "Seorang siswa membuat 5 garis tegak lalu 1 garis miring (total 6 garis). Perbaikannya?", ["garis miring seharusnya memotong 4 garis pertama saja sebagai garis ke-5", "tambah lagi garis miring", "hapus semua garis", "biarkan 6 garis"], "A", "Garis miring adalah garis ke-5, bukan garis ke-6.")
tf("c4", "sedang", T, Kn, S3, "Dalam 20 data, terdapat tepat 4 garis miring pengikat.", "Benar", "20 : 5 = 4 ikat, berarti ada 4 garis miring.")
tf("c4", "sedang", T, Kn, S4, "Garis lepas di samping ikatan turus jumlahnya boleh mencapai 5 garis tegak.", "Salah", "Jika sudah mencapai 5 garis, wajib langsung diikat menjadi kelompok baru.")
sa("c4", "sedang", T, Kn, S3, "Dalam 35 data turus, jumlah ikatan lima yang benar adalah ... ikat.", "7", "35 : 5 = 7 ikat.", verifikasi={"ekspresi": "35 // 5", "hasil": "7"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Lani mencatat 15 siswa dengan membuat 15 garis tegak lurus. Berapa ikat seharusnya?", ["3 ikat penuh", "2 ikat dan 5 garis", "4 ikat", "1 ikat dan 10 garis"], "A", "15 : 5 = 3 ikat penuh.", verifikasi={"ekspresi": "15 // 5", "hasil": "3"})
mc("c4", "sedang", X, Kn, S4, "Turus A: 4 ikat 1 garis. Turus B: 3 ikat 4 garis. Selisihnya?", ["2 data", "3 data", "1 data", "4 data"], "A", "A = 21, B = 19. Selisih = 21 - 19 = 2 data.", verifikasi={"ekspresi": "((4 * 5) + 1) - ((3 * 5) + 4)", "hasil": "2"})
tf("c4", "sedang", X, Kn, S2, "Garis coret miring turus hanya boleh dibuat dengan tinta warna merah.", "Salah", "Garis miring dibuat dengan alat tulis yang sama.")
mc("c4", "sulit", X, Me, S3, "Siswa mencatat 23 data dengan turus. Berapa jumlah seluruh goresan garis yang digambar?", ["23 goresan", "20 goresan", "25 goresan", "19 goresan"], "A", "Tiap 1 hitungan data = 1 goresan (tegak atau miring), total 23 goresan.", verifikasi={"ekspresi": "23 * 1", "hasil": "23"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Mengapa garis ke-5 tidak digambar sejajar tegak tetapi dibuat miring?", ["agar mengunci kelompok 4 garis tegak sehingga tampak jelas sebagai 1 paket 5", "agar terlihat miring", "karena tangannya terpeleset", "tidak sengaja"], "A", "Garis miring membedakan ikatan 5 secara visual dari garis lepas.")
mc("c4", "sulit", K, Me, S3, "Ada 3 kelompok turus, masing-masing 2 ikat dan 3 garis. Total nilai ketiganya?", ["39 data", "36 data", "42 data", "35 data"], "A", "Tiap kelompok: 13. 3 x 13 = 39 data.", verifikasi={"ekspresi": "3 * ((2 * 5) + 3)", "hasil": "39"})
tf("c4", "sulit", K, Me, S4, "Jika sisa garis tegak ada 4, kita belum boleh mencoret garis miring.", "Benar", "Garis miring baru ditarik saat ada data ke-5 masuk.")
mc("c4", "sulit", K, Me, S4, "Tersedia data 47 siswa. Berapa banyak ikatan penuh dan garis lepas yang terbentuk?", ["9 ikat penuh dan 2 garis lepas", "8 ikat dan 7 garis", "10 ikat penuh", "7 ikat dan 12 garis"], "A", "47 = (9 x 5) + 2.")

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Edo kesulitan menghitung turus di papan tulis karena garisnya berjejer panjang. Saran terbaik?", ["bantu mengikat garis tiap kelipatan 5 dengan garis coret miring", "hapus semua dan pulang", "hitung pakai tebakan", "tinggalkan saja"], "A", "Mengikat turus tiap 5 goresan adalah solusi sistematis.")
mc("c5", "sedang", T, Me, S2, "Turus A (5 ikat) dan Turus B (4 ikat 6 garis). Siapakah bernilai lebih banyak?", ["keduanya sama banyak", "turus A lebih banyak", "turus B lebih banyak", "tidak dapat dihitung"], "A", "Turus A = 25. Turus B = 20 + 6 = 26! Nilai B (26) > A (25).", verifikasi={"ekspresi": "((4 * 5) + 6) - (5 * 5)", "hasil": "1"})
mc("c5", "sedang", T, Me, S3, "Berapa garis miring yang harus digambar jika kita mencatat 40 orang pemilih ketua kelas?", ["8 garis miring", "7 garis miring", "9 garis miring", "10 garis miring"], "A", "40 : 5 = 8 ikat penuh = 8 garis miring.", verifikasi={"ekspresi": "40 // 5", "hasil": "8"})
mc("c5", "sulit", T, Me, S4, "Dua anak mencatat kendaraan: Siti (6 ikat 2 garis), Dayu (5 ikat 4 garis). Berapa selisihnya?", ["3 kendaraan", "2 kendaraan", "4 kendaraan", "5 kendaraan"], "A", "Siti = 32, Dayu = 29. Selisih = 32 - 29 = 3 kendaraan.", verifikasi={"ekspresi": "((6 * 5) + 2) - ((5 * 5) + 4)", "hasil": "3"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Miskonsepsi: Ani mencoret garis miring pada garis ke-4. Akibatnya nilai 1 ikat menjadi?", ["bernilai 4 sehingga hitungan salah", "tetap 5", "menjadi 10", "tidak berubah"], "A", "Mengikat pada garis ke-4 menyebabkan kelompok bernilai 4 bukan 5.")
mc("c5", "sulit", K, Me, S4, "Pak Guru memeriksa catatan turus: 7 ikat dan 4 garis lepas. Nilai data tersebut?", ["39 data", "35 data", "40 data", "37 data"], "A", "(7 x 5) + 4 = 35 + 4 = 39 data.", verifikasi={"ekspresi": "(7 * 5) + 4", "hasil": "39"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Rancanglah aturan baku pencatatan turus di kelas agar semua siswa mencatat seragam!", ["setiap data ke-5 wajib dicoret miring memotong 4 garis tegak sebelumnya", "bebas mencoret kapan saja", "tidak boleh ada garis miring", "semua garis harus miring"], "A", "Aturan baku pengikatan tiap kelipatan 5 memastikan konsistensi pencatatan.")
mc("c6", "sulit", K, Me, S4, "Mengapa sistem turus ikatan 5 sangat cocok untuk menghitung pemilu secara langsung?", ["karena tiap ada 1 suara langsung dicatat dan kelompok 5 langsung terlihat tanpa menghitung ulang", "karena kertasnya murah", "agar ramai", "hanya tradisi lama"], "A", "Pencatatan bertahap seketika dan kemudahan visual ikatan 5 adalah keunggulan utama.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Ubahlah 58 garis tegak menjadi kelompok turus yang benar. Berapa ikat dan sisa?", ["11 ikat lima dan 3 garis lepas", "10 ikat dan 8 garis", "12 ikat penuh", "9 ikat dan 13 garis"], "A", "58 = (11 x 5) + 3.")
mc("c6", "sulit", P, Me, S4, "Tiga pos: 8 ikat, 6 ikat 3 garis, dan 5 ikat 1 garis. Total data?", ["99 data", "95 data", "100 data", "96 data"], "A", "40 + 33 + 26 = 99 data.", verifikasi={"ekspresi": "(8 * 5) + ((6 * 5) + 3) + ((5 * 5) + 1)", "hasil": "99"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab80_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab80.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
