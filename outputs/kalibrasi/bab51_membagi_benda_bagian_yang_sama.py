#!/usr/bin/env python3
"""
Generator dan validator Bab 51 Matematika Kelas 2 SD:
"Membagi Benda Menjadi Bagian yang Sama" (Fase A)
bab_id: a580d7f6-cabe-4657-a872-e070d85d5196
article_id: 44f49f33-5a5f-4560-b08c-606791be1bea
quiz_id: 99c7784c-754f-44b5-b9a6-6e26bc3e191f
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "e1f2a3b4c501"  # Benda Utuh dan Membaginya
S2 = "f2a3b4c5d602"  # Arti Bagian yang Sama Besar
S3 = "a3b4c5d6e703"  # Membagi Benda Konkret
S4 = "b4c5d6e7f804"  # Membedakan Bagian Adil vs Tidak Adil

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Sebuah benda yang belum dipotong disebut utuh.
Misalnya satu apel yang masih bulat.
Atau selembar kertas yang masih rapi.
Kita bisa memotong benda utuh tersebut.
Benda utuh menjadi beberapa potongan.
Setiap potongan berasal dari satu keutuhan.
Mari belajar memotong benda dengan baik!

:::definition
title: Benda Utuh
Benda utuh adalah satu kesatuan benda lengkap yang belum dibagi atau dipotong.
:::"""

s2_content = """Saat memotong benda, perhatikan ukurannya.
Apakah potongannya sama besar?
Membagi adil artinya ukuran potongannya sama.
Bentuk dan luasnya tidak boleh berbeda.
Jika satu besar dan satu kecil, itu tidak sama.
Hanya potongan sama besar yang disebut pecahan adil.
Keadilan pembagian sangat penting!

:::steps
title: Cara Membagi Sama Besar
1. Tentukan garis tengah yang tepat.
2. Potong atau lipat pas di garis itu.
3. Cocokkan kedua bagian agar pas menempel.
:::"""

s3_content = """Kita bisa membagi berbagai benda.
Satu pizza dipotong menjadi dua bagian sama.
Satu roti dipotong menjadi empat bagian sama.
Lipatlah kertas menjadi dua bagian sejajar.
Kedua sisi akan saling menutupi rapat.
Ini membuktikan kedua bagian sama besar.
Sangat mudah dan menyenangkan!"""

s4_content = """Ayo amati hasil potongan benda.
Bila potongan satu lebih besar, pembagian tidak adil.
Kedua anak akan berebut bagian besar.
Pembagian pecahan wajib sama persis.
Perhatikan selalu garis potongnya.
Pastikan tidak ada bagian yang dirugikan!

:::common_trap
title: Membagi Asal Menjadi Dua
Memotong menjadi dua belum tentu sama besar!
Jika satu bagian besar dan satu kecil, itu bukan setengah.
Setengah wajib sama besar.
:::

:::callout
variant: summary
title: Ringkasan
text: Membagi benda menjadi pecahan harus menghasilkan potongan-potongan yang berukuran sama besar.
:::"""

sections = [
    {
        "id": S1,
        "title": "Benda Utuh dan Membaginya",
        "minutes": 6,
        "goal": "Siswa memahami konsep satu kesatuan benda utuh sebelum dipotong atau dibagi.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Arti Bagian yang Sama Besar",
        "minutes": 6,
        "goal": "Siswa memahami kriteria mutlak pembagian sama besar (adil) pada suatu objek.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membagi Benda Konkret",
        "minutes": 6,
        "goal": "Siswa mampu mempraktikkan pembagian benda nyata atau bangun datar menjadi beberapa bagian sama besar.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Membedakan Bagian Adil vs Tidak Adil",
        "minutes": 6,
        "goal": "Siswa mampu mengidentifikasi dan membedakan potongan benda yang sama besar dengan yang tidak sama besar.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membagi Benda Menjadi Bagian yang Sama",
    "topic": "Mengenal Setengah dan Seperempat",
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
# 2. DEFINISI BANK 50 SOAL BAB 51
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
mc("c1", "mudah", D, F, S1, "Benda yang belum dipotong atau dibagi sama sekali disebut ....", ["benda utuh", "benda pecahan", "benda sisa", "benda rusak"], "A", "Benda yang masih lengkap dan belum dipotong adalah benda utuh.")
tf("c1", "mudah", D, F, S2, "Membagi adil artinya setiap bagian harus berukuran sama besar.", "Benar", "Pembagian adil mewajibkan ukuran semua bagian sama persis.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Jika satu semangka dipotong menjadi dua bagian sama besar, berapa potong?", ["2 potong", "3 potong", "4 potong", "1 potong"], "A", "Dipotong jadi dua menghasilkan 2 potong.", verifikasi={"ekspresi": "2 / 1", "hasil": "2"})
mc("c1", "mudah", T, F, S3, "Satu kertas dilipat tepat di tengah. Berapa bagian sama yang terbentuk?", ["2 bagian", "3 bagian", "4 bagian", "5 bagian"], "A", "Melipat kertas di garis tengah menghasilkan 2 bagian sama.", verifikasi={"ekspresi": "1 * 2", "hasil": "2"})
sa("c1", "mudah", T, F, S4, "Berapakah potongan yang didapat jika satu kue dipotong jadi 4 sama rata?", "4", "Dipotong jadi 4 bagian sama menghasilkan 4 potong.", verifikasi={"ekspresi": "4 / 1", "hasil": "4"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Manakah potongan yang menunjukkan pembagian yang adil?", ["semua potongan berukuran sama besar", "satu bagian besar satu kecil", "potongan dipotong sembarang", "potongan berbeda bentuk"], "A", "Pembagian adil menghasilkan potongan berukuran sama besar.")
tf("c2", "mudah", D, Kn, S1, "Memotong selembar kertas sembarang menghasilkan bagian yang sama besar.", "Salah", "Memotong sembarang menghasilkan potongan berbeda ukuran, tidak sama besar.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Ada roti dipotong jadi 2. Bagian kiri jauh lebih besar. Apakah adil?", ["tidak adil karena ukurannya berbeda", "adil karena sudah jadi dua", "sangat adil", "adil jika dimakan bersama"], "A", "Syarat adil harus sama besar, bukan sekadar dipotong jadi dua.", "Mengira asal dipotong dua sudah adil")
mc("c2", "mudah", R, Kn, S4, "Budi memotong apel jadi 2. Satu untuk adik, satu untuk Budi. Syarat adil?", ["kedua potongan harus sama besar", "potongan Budi harus lebih besar", "potongan adik harus lebih kecil", "tidak ada syarat"], "A", "Kedua bagian harus berukuran sama besar.", "Mengabaikan syarat kesamaan ukuran")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Ibu membagi semangka utuh menjadi 4 potong sama besar. Tiap potong berukuran ....", ["sama besar", "berbeda-beda", "acak", "satu besar tiga kecil"], "A", "Karena dibagi sama besar, maka tiap potong berukuran sama besar.")
mc("c2", "mudah", T, Kn, S3, "Sebuah pita dipotong di tengah menjadi 2 bagian sama panjang. Berapa bagian?", ["2 bagian", "4 bagian", "3 bagian", "1 bagian"], "A", "Dipotong sekali di tengah menghasilkan 2 bagian.", verifikasi={"ekspresi": "2 / 1", "hasil": "2"})
tf("c2", "mudah", T, Kn, S4, "Jika dua potongan kertas saling menutupi dengan pas, maka keduanya sama besar.", "Benar", "Saling menutupi pas (kongruen) menandakan ukuran sama besar.")
sa("c2", "mudah", T, Kn, S2, "Berapakah jumlah bagian jika dua kue utuh masing-masing dipotong jadi dua?", "4", "2 x 2 = 4 bagian.", verifikasi={"ekspresi": "2 * 2", "hasil": "4"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Ada 8 potong pizza dibagi rata ke 2 anak. Berapa potong tiap anak?", ["4 potong", "2 potong", "6 potong", "8 potong"], "A", "8 : 2 = 4 potong tiap anak.", "Salah menghitung pembagian", verifikasi={"ekspresi": "8 / 2", "hasil": "4"})
mc("c3", "sedang", R, Pr, S4, "Ada 12 kue dibagi sama rata ke 3 piring. Berapa kue tiap piring?", ["4 kue", "3 kue", "5 kue", "6 kue"], "A", "12 : 3 = 4 kue tiap piring.", "Keliru pembagian rata", verifikasi={"ekspresi": "12 / 3", "hasil": "4"})

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Ada 6 donat dibagikan sama rata kepada 2 anak. Berapa donat per anak?", ["3 donat", "2 donat", "4 donat", "1 donat"], "A", "6 : 2 = 3 donat.", verifikasi={"ekspresi": "6 / 2", "hasil": "3"})
mc("c3", "mudah", T, Pr, S3, "Satu kue dipotong jadi 4 sama besar. Dimakan 1 potong. Sisa berapa potong?", ["3 potong", "2 potong", "4 potong", "1 potong"], "A", "4 - 1 = 3 potong tersisa.", verifikasi={"ekspresi": "4 - 1", "hasil": "3"})
tf("c3", "sedang", T, Pr, S2, "Dua anak mendapat apel potong sama besar, artinya mereka mendapat bagian adil.", "Benar", "Potongan sama besar berarti adil.")
mc("c3", "sedang", T, Pr, S4, "Ada 10 permen dibagi ke 2 kantong sama banyak. Berapa permen tiap kantong?", ["5 permen", "4 permen", "6 permen", "3 permen"], "A", "10 : 2 = 5 permen.", verifikasi={"ekspresi": "10 / 2", "hasil": "5"})
tf("c3", "sedang", T, Pr, S1, "Satu kue utuh nilainya lebih sedikit daripada satu potongan kecil kue.", "Salah", "Benda utuh selalu lebih banyak dan lebih besar daripada satu potongannya.")
sa("c3", "sedang", T, Pr, S3, "Berapakah hasil dari 16 potong kue dibagi rata ke 4 anak?", "4", "16 : 4 = 4 potong per anak.", verifikasi={"ekspresi": "16 / 4", "hasil": "4"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Ada 14 cokelat dibagikan rata ke 2 anak. Berapa cokelat tiap anak?", ["7 cokelat", "6 cokelat", "8 cokelat", "5 cokelat"], "A", "14 : 2 = 7 cokelat.", verifikasi={"ekspresi": "14 / 2", "hasil": "7"})
mc("c3", "sedang", X, Pr, S2, "Sebuah melon dipotong jadi 4 bagian sama. Dua potong dimakan. Berapa sisa potong?", ["2 potong", "1 potong", "3 potong", "0 potong"], "A", "4 - 2 = 2 potong.", verifikasi={"ekspresi": "4 - 2", "hasil": "2"})
tf("c3", "sedang", X, Pr, S4, "Membagi roti menjadi 4 bagian sama besar menghasilkan potongan lebih kecil daripada dibagi 2.", "Benar", "Makin banyak potongan, ukuran tiap potongan makin kecil.")
sa("c3", "sedang", X, Pr, S3, "Berapakah hasil dari 20 apel dibagi sama rata ke 4 keranjang?", "5", "20 : 4 = 5 apel per keranjang.", verifikasi={"ekspresi": "20 / 4", "hasil": "5"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Ada 18 kue dibagi sama rata ke 2 piring. Berapa kue di tiap piring?", ["9 kue", "8 kue", "10 kue", "7 kue"], "A", "18 : 2 = 9 kue.", verifikasi={"ekspresi": "18 / 2", "hasil": "9"})
mc("c3", "sedang", K, Pr, S3, "Ada 24 biskuit dibagi sama rata ke 4 anak. Berapa biskuit tiap anak?", ["6 biskuit", "5 biskuit", "7 biskuit", "8 biskuit"], "A", "24 : 4 = 6 biskuit.", verifikasi={"ekspresi": "24 / 4", "hasil": "6"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa garis lipatan kertas harus tepat di tengah agar adil?", ["agar kedua sisi terbagi menjadi dua bagian sama luas", "agar kertas tidak rusak", "agar warnanya tetap sama", "agar kertas menjadi lebih tebal"], "A", "Garis tengah menjamin kedua bagian sama persis luasnya.")
mc("c4", "sedang", T, Kn, S2, "Lina punya 2 potong semangka yang sama besar. Totalnya sama dengan ....", ["satu semangka utuh", "dua semangka utuh", "setengah semangka", "tiga semangka"], "A", "Dua potong sama besar dari satu semangka jika disatukan membentuk satu semangka utuh.")
tf("c4", "sedang", T, Kn, S3, "Tiga potong kue yang berbeda ukuran dapat disebut bagian yang sama besar.", "Salah", "Ukuran berbeda berarti tidak sama besar.")
tf("c4", "sedang", T, Kn, S4, "Memotong persegi melalui satu garis di dekat pojok menghasilkan dua bagian sama besar.", "Salah", "Garis di dekat pojok menghasilkan satu bagian kecil dan satu bagian besar, tidak sama besar.")
sa("c4", "sedang", T, Kn, S4, "Berapakah hasil dari (16 : 2) + 4?", "12", "16 : 2 = 8; 8 + 4 = 12.", verifikasi={"ekspresi": "(16 / 2) + 4", "hasil": "12"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Budi punya 1 kue utuh. Siti punya 2 potong kue setengah. Siapa lebih banyak?", ["kue Budi dan Siti sama banyak", "Budi punya lebih banyak", "Siti punya lebih banyak", "tidak dapat dibandingkan"], "A", "1 kue utuh setara dengan 2 potong kue setengah.")
mc("c4", "sedang", X, Kn, S3, "Sebuah pizza dipotong jadi 4 sama besar. Doni makan 2 potong. Berapa potong sisa?", ["2 potong", "1 potong", "3 potong", "4 potong"], "A", "4 - 2 = 2 potong tersisa.", verifikasi={"ekspresi": "4 - 2", "hasil": "2"})
tf("c4", "sedang", X, Kn, S2, "Satu apel utuh selalu lebih kecil dari setengah apel.", "Salah", "Satu apel utuh dua kali lebih besar dari setengah apel.")
mc("c4", "sulit", X, Me, S4, "Di antara pilihan pembagian apel berikut, manakah potongan yang PALING BESAR?", ["dibagi menjadi 2 bagian sama besar", "dibagi menjadi 4 bagian sama besar", "dibagi menjadi 8 bagian sama besar", "dibagi menjadi 6 bagian sama besar"], "A", "Makin sedikit pembagiannya (dibagi 2), ukuran tiap potongannya paling besar.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Apa yang terjadi jika kita menyatukan kembali semua potongan benda yang adil?", ["akan membentuk kembali satu benda utuh semula", "bendanya akan bertambah banyak", "bendanya menjadi hilang", "bentuknya berubah menjadi cair"], "A", "Semua pecahan jika digabungkan kembali akan membentuk keutuhan asalnya.")
mc("c4", "sulit", K, Me, S2, "Ada 28 permen dibagi ke 4 mangkuk sama banyak. Berapa permen per mangkuk?", ["7 permen", "6 permen", "8 permen", "5 permen"], "A", "28 : 4 = 7 permen.", verifikasi={"ekspresi": "28 / 4", "hasil": "7"})
tf("c4", "sulit", K, Me, S4, "Empat potong kue seperempat sama banyaknya dengan satu kue utuh.", "Benar", "4 x seperempat = 1 kue utuh.")
mc("c4", "sulit", K, Me, S4, "Berapakah hasil dari (32 : 4) - (12 : 3)?", ["4", "3", "5", "6"], "A", "32 : 4 = 8; 12 : 3 = 4; 8 - 4 = 4.", verifikasi={"ekspresi": "(32 / 4) - (12 / 3)", "hasil": "4"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Dua anak ingin membagi 1 kue persegi secara adil. Garis potong harus dibuat ....", ["tepat membagi dua simetris di tengah", "di pojok sembarang", "dekat salah satu sisi", "melengkung acak"], "A", "Garis tengah simetris membagi luas secara adil dan sama besar.")
mc("c5", "sedang", T, Me, S2, "Berapakah nilai N jika N potong kue sama besar membentuk satu kue utuh dibagi 4?", ["4 potong", "2 potong", "3 potong", "5 potong"], "A", "Dibagi 4 berarti membutuhkan 4 potong sama besar.", verifikasi={"ekspresi": "4 / 1", "hasil": "4"})
mc("c5", "sedang", T, Me, S3, "Ibu memotong 2 kue, tiap kue dipotong jadi 4 sama besar. Total potongan?", ["8 potong", "6 potong", "10 potong", "4 potong"], "A", "2 x 4 = 8 potong.", verifikasi={"ekspresi": "2 * 4", "hasil": "8"})
mc("c5", "sulit", T, Me, S4, "Berapakah hasil dari (24 : 2) + (16 : 4)?", ["16", "14", "18", "12"], "A", "24 : 2 = 12; 16 : 4 = 4; 12 + 4 = 16.", verifikasi={"ekspresi": "(24 / 2) + (16 / 4)", "hasil": "16"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Sebuah tali panjangnya 36 cm. Dipotong jadi 4 bagian sama panjang. Panjang tiap bagian?", ["9 cm", "8 cm", "10 cm", "7 cm"], "A", "36 : 4 = 9 cm.", verifikasi={"ekspresi": "36 / 4", "hasil": "9"})
mc("c5", "sulit", K, Me, S4, "Berapakah hasil dari (40 : 4) - (18 : 3)?", ["4", "3", "5", "6"], "A", "40 : 4 = 10; 18 : 3 = 6; 10 - 6 = 4.", verifikasi={"ekspresi": "(40 / 4) - (18 / 3)", "hasil": "4"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Mengapa konsep bagian yang sama besar sangat penting dalam kehidupan bermasyarakat?", ["karena menjamin keadilan dan kejujuran saat berbagi", "karena peraturan dari buku", "agar makanan cepat habis", "tidak terlalu penting"], "A", "Membagi sama besar menjamin keadilan nyata tanpa ada yang dirugikan.")
mc("c6", "sulit", K, Me, S3, "Kayu 30 cm dipotong jadi 2 sama panjang. Tiap potong dibagi 3. Panjang tiap bagian?", ["5 cm", "6 cm", "4 cm", "10 cm"], "A", "30 : 2 = 15 cm; 15 : 3 = 5 cm.", verifikasi={"ekspresi": "(30 / 2) / 3", "hasil": "5"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi gabungan: (48 : 4) - (20 : 2) + (15 : 3)!", ["7", "5", "9", "6"], "A", "48 : 4 = 12; 20 : 2 = 10; 15 : 3 = 5; 12 - 10 + 5 = 7.", verifikasi={"ekspresi": "(48 / 4) - (20 / 2) + (15 / 3)", "hasil": "7"})
mc("c6", "sulit", P, Me, S4, "Ada 3 kue, tiap kue dipotong jadi 4 bagian. Dibagi ke 6 anak. Tiap anak?", ["2 potong", "3 potong", "1 potong", "4 potong"], "A", "3 x 4 = 12 potong; 12 : 6 = 2 potong per anak.", verifikasi={"ekspresi": "(3 * 4) / 6", "hasil": "2"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab51_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab51.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
