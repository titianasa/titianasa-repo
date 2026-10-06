#!/usr/bin/env python3
"""
Generator dan validator Bab 75 Matematika Kelas 2 SD:
"Kesalahan Umum: Mengira Lingkaran Memiliki Sudut" (Fase A)
bab_id: 300fd5d2-8735-4d93-b02c-323ca3081b4a
article_id: 0dbd1c9c-58b2-4145-850a-55bb167a916b
quiz_id: fd91d28e-3cc0-4186-98e5-02f0e2f684e4
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "t1v2x3z4b501"  # Garis Lengkung Tanpa Pojok
S2 = "u2w3y4a5c602"  # Mengapa Lingkaran Tidak Memiliki Sudut?
S3 = "v3x4z5b6d703"  # Membedakan Lingkaran dengan Segi Banyak
S4 = "w4y5a6c7e804"  # Benda Lingkaran dan Manfaat Roda

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Lingkaran adalah bangun datar yang unik.
Tepian lingkaran berupa satu garis lengkung.
Garis lengkung itu tersambung sangat halus.
Tidak ada patahan garis sama sekali.
Raba tepian uang koin logam.
Rasakan dengan jarimu secara melingkar.
Tidak ada bagian tajam atau pojok.
Semuanya terasa mulus dan rata!

:::definition
title: Lingkaran
Bangun datar yang dibatasi oleh satu garis lengkung tertutup bersambung.
:::"""

s2_content = """Banyak anak mengira lingkaran punya sudut.
Ingat kembali syarat terbentuknya sudut.
Sudut butuh dua garis lurus bertemu.
Pertemuan dua garis membentuk pojok lancip.
Pada lingkaran tidak ada garis lurus.
Maka tidak ada pojok sama sekali.
Lingkaran memiliki nol titik sudut.
Jangan terkecoh lagi dengan bentuk bulat!

:::steps
title: Memeriksa Sudut Bangun Datar
1. Cari garis lurus pembatas bangun.
2. Cari pojok tajam pertemuan dua garis.
3. Lingkaran tidak punya garis lurus dan pojok.
:::"""

s3_content = """Bandingkan lingkaran dengan bangun lain.
Segitiga memiliki 3 sudut lancip.
Segiempat memiliki 4 sudut siku.
Segilima memiliki 5 sudut tumpul.
Namun lingkaran memiliki 0 sudut.
Lingkaran dibatasi 1 sisi lengkung.
Segi banyak dibatasi garis lurus.
Perbedaan ini sangat mudah dilihat!

:::common_trap
title: Mengira Lingkaran Memiliki Sudut Tak Terhingga
Untuk anak SD, lingkaran tidak berpojok.
Lingkaran memiliki 0 sudut sama sekali.
Bukan banyak sudut, melainkan tanpa sudut!
:::"""

s4_content = """Tanpa sudut membuat lingkaran istimewa.
Roda sepeda dibuat berbentuk lingkaran bulat.
Karena tanpa sudut, roda berputar mulus.
Bayangkan jika roda berbentuk kotak persegi.
Pasti sepedamu berjalan tersendat-sendat!
Koin, piring, dan cincin juga bundar.
Bentuk tanpa sudut sangat bermanfaat!

:::callout
variant: summary
title: Ringkasan
text: Lingkaran 1 sisi lengkung. Lingkaran memiliki tepat 0 sudut.
:::"""

sections = [
    {
        "id": S1,
        "title": "Garis Lengkung Tanpa Pojok",
        "minutes": 6,
        "goal": "Siswa memahami bahwa lingkaran dibatasi satu garis lengkung halus tanpa pojok.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengapa Lingkaran Tidak Memiliki Sudut?",
        "minutes": 6,
        "goal": "Siswa memahami alasan matematis mengapa lingkaran memiliki tepat 0 titik sudut.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membedakan Lingkaran dengan Segi Banyak",
        "minutes": 6,
        "goal": "Siswa membedakan ciri fisik lingkaran dengan bangun bersisi lurus (poligon).",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Benda Lingkaran dan Manfaat Roda",
        "minutes": 6,
        "goal": "Siswa mengenali aplikasi bentuk lingkaran dalam kehidupan sehari-hari (roda, koin).",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Mengira Lingkaran Memiliki Sudut",
    "topic": "Bangun Datar dan Bangun Ruang Sederhana",
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
# 2. DEFINISI BANK 50 SOAL BAB 75
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
mc("c1", "mudah", D, F, S2, "Berapakah banyak titik sudut yang dimiliki oleh bangun lingkaran?", ["0 sudut", "1 sudut", "2 sudut", "4 sudut"], "A", "Lingkaran tidak memiliki sudut sama sekali (0 sudut).", verifikasi={"ekspresi": "1 - 1", "hasil": "0"})
tf("c1", "mudah", D, F, S1, "Lingkaran dibatasi oleh satu garis lengkung yang tertutup.", "Benar", "Pembatas lingkaran adalah satu garis lengkung bersambung.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Berapakah jumlah garis lurus yang membatasi sebuah bangun lingkaran?", ["0 garis lurus", "1 garis lurus", "2 garis lurus", "4 garis lurus"], "A", "Lingkaran tidak dibatasi oleh garis lurus sama sekali.", verifikasi={"ekspresi": "0 * 1", "hasil": "0"})
mc("c1", "mudah", T, F, S3, "Berapa banyak sudut yang dimiliki oleh bangun segitiga?", ["3 sudut", "4 sudut", "0 sudut", "5 sudut"], "A", "Segitiga memiliki 3 sudut.", verifikasi={"ekspresi": "1 * 3", "hasil": "3"})
sa("c1", "mudah", T, F, S2, "Jumlah sudut pada bangun lingkaran adalah ... buah.", "0", "Lingkaran memiliki 0 sudut.", verifikasi={"ekspresi": "0 + 0", "hasil": "0"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Benda berikut yang memiliki permukaan berbentuk lingkaran adalah ....", ["uang koin logam", "buku tulis", "papan tulis", "garis mistar"], "A", "Koin logam berbentuk lingkaran.")
tf("c2", "mudah", D, Kn, S2, "Lingkaran memiliki empat titik sudut yang tersembunyi di dalamnya.", "Salah", "Lingkaran tidak memiliki sudut sama sekali.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Doni mengira lingkaran memiliki 1 sudut melingkar. Mengapa Doni keliru?", ["karena sudut hanya terbentuk jika dua garis lurus bertemu", "karena lingkaran terlalu bulat", "karena koin itu bulat", "karena Doni malas"], "A", "Sudut harus terbentuk dari pertemuan dua garis lurus.", "Mengira garis lengkung adalah sebuah sudut")
mc("c2", "mudah", R, Kn, S3, "Di antara bangun berikut, manakah bangun yang TIDAK memiliki sudut?", ["lingkaran", "persegi", "segitiga", "trapesium"], "A", "Lingkaran tidak memiliki sudut.", "Memilih bangun datar lain yang memiliki sudut")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S3, "Berapakah selisih jumlah sudut antara persegi dan lingkaran?", ["4 sudut", "3 sudut", "2 sudut", "5 sudut"], "A", "4 - 0 = 4 sudut.", verifikasi={"ekspresi": "4 - 0", "hasil": "4"})
mc("c2", "mudah", T, Kn, S4, "Mengapa roda kendaraan dibuat berbentuk bangun lingkaran?", ["agar roda dapat berputar dengan mulus dan lancar", "agar bannya terlihat keren", "agar roda lebih berat", "supaya tidak bisa dicuri"], "A", "Bentuk tanpa sudut memungkinkan perputaran roda yang mulus.")
tf("c2", "mudah", T, Kn, S3, "Bangun segiempat dan segitiga sama-sama memiliki titik sudut.", "Benar", "Keduanya memiliki sudut (segiempat 4, segitiga 3).")
sa("c2", "mudah", T, Kn, S1, "Lingkaran dibatasi oleh ... buah garis lengkung tertutup.", "1", "Dibatasi 1 garis lengkung.", verifikasi={"ekspresi": "1 * 1", "hasil": "1"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Berapakah jumlah sudut dari gabungan 2 segitiga dan 1 lingkaran?", ["6 sudut", "7 sudut", "5 sudut", "8 sudut"], "A", "(2 x 3) + 0 = 6 sudut.", "Menambahkan sudut pada lingkaran", verifikasi={"ekspresi": "(2 * 3) + 0", "hasil": "6"})
mc("c3", "sedang", R, Pr, S4, "Ada 4 koin logam di atas meja. Berapa total sudut keempat koin?", ["0 sudut", "4 sudut", "8 sudut", "12 sudut"], "A", "4 x 0 = 0 sudut.", "Mengira tiap koin memiliki 1 sudut", verifikasi={"ekspresi": "4 * 0", "hasil": "0"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S3, "Berapakah selisih banyak sudut antara segilima dan lingkaran?", ["5 sudut", "4 sudut", "6 sudut", "3 sudut"], "A", "5 - 0 = 5 sudut.", verifikasi={"ekspresi": "5 - 0", "hasil": "5"})
mc("c3", "mudah", T, Pr, S4, "Siti menggambar 3 lingkaran dan 2 persegi. Berapa total sudut gambarnya?", ["8 sudut", "6 sudut", "10 sudut", "12 sudut"], "A", "(3 x 0) + (2 x 4) = 8 sudut.", verifikasi={"ekspresi": "(3 * 0) + (2 * 4)", "hasil": "8"})
tf("c3", "sedang", T, Pr, S1, "Satu garis lengkung lingkaran dapat membentuk sudut jika ditekuk.", "Salah", "Bila ditekuk membentuk pojok, bentuknya bukan lagi lingkaran sempurna.")
mc("c3", "sedang", T, Pr, S2, "Berapa banyak titik sudut pada 5 buah bangun lingkaran terpisah?", ["0 sudut", "5 sudut", "10 sudut", "1 sudut"], "A", "5 x 0 = 0 sudut.", verifikasi={"ekspresi": "5 * 0", "hasil": "0"})
tf("c3", "sedang", T, Pr, S4, "Roda gerobak berbentuk lingkaran tidak akan tersendat saat berputar di jalan.", "Benar", "Karena tidak memiliki sudut, roda berputar rata.")
sa("c3", "sedang", T, Pr, S3, "Total sudut dari 1 bangun segienam ditambah 3 lingkaran adalah ... sudut.", "6", "6 + (3 x 0) = 6.", verifikasi={"ekspresi": "6 + (3 * 0)", "hasil": "6"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Bila seutas tali dibuat lingkaran tertutup, berapa sudut yang terbentuk?", ["0 sudut", "1 sudut", "2 sudut", "4 sudut"], "A", "Lingkaran memiliki 0 sudut.", verifikasi={"ekspresi": "0 * 1", "hasil": "0"})
mc("c3", "sedang", X, Pr, S3, "Budi punya 4 segiempat dan 5 lingkaran. Berapa jumlah semua sudutnya?", ["16 sudut", "20 sudut", "12 sudut", "18 sudut"], "A", "(4 x 4) + (5 x 0) = 16 sudut.", verifikasi={"ekspresi": "(4 * 4) + (5 * 0)", "hasil": "16"})
tf("c3", "sedang", X, Pr, S2, "Menghitung sudut lingkaran menghasilkan angka nol.", "Benar", "Lingkaran memang memiliki nol sudut.")
sa("c3", "sedang", X, Pr, S4, "Ada 2 sepeda, tiap roda berbentuk lingkaran. Total sudut semua rodanya?", "0", "4 roda x 0 = 0 sudut.", verifikasi={"ekspresi": "4 * 0", "hasil": "0"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Berapakah jumlah sudut dari 3 segitiga dan 2 lingkaran digabungkan?", ["9 sudut", "6 sudut", "11 sudut", "12 sudut"], "A", "(3 x 3) + (2 x 0) = 9 sudut.", verifikasi={"ekspresi": "(3 * 3) + (2 * 0)", "hasil": "9"})
mc("c3", "sedang", K, Pr, S4, "Kumpulan benda: jam dinding bulat, piring makan, koin. Berapa sudut ketiganya?", ["0 sudut", "3 sudut", "6 sudut", "1 sudut"], "A", "Semuanya lingkaran = 0 sudut.", verifikasi={"ekspresi": "3 * 0", "hasil": "0"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S1
mc("c4", "sedang", T, Kn, S1, "Mengapa sebuah uang logam tidak pernah melukai jari kita dengan pojok tajam?", ["karena tepian uang logam melengkung mulus tanpa pojok sudut", "karena terbuat dari kapas", "karena uang itu tipis", "karena uang itu dingin"], "A", "Bentuk lingkaran tidak memiliki sudut lancip yang tajam.")
mc("c4", "sedang", T, Kn, S2, "Seorang siswa berkata: 'Lingkaran bersudut 360'. Apa maksud sebenarnya?", ["360 derajat adalah ukuran satu putaran sudut, bukan jumlah pojok sudutnya", "ada 360 pojok kecil", "ada 360 jarum", "siswa itu berbohong"], "A", "Derajat putaran berbeda dengan jumlah titik sudut bangun datar.")
tf("c4", "sedang", T, Kn, S3, "Lingkaran termasuk dalam kelompok bangun datar segi banyak (poligon).", "Salah", "Poligon dibatasi garis lurus, sedangkan lingkaran garis lengkung.")
tf("c4", "sedang", T, Kn, S4, "Jika roda mobil dibuat berbentuk segitiga, mobil akan berjalan sangat nyaman.", "Salah", "Sudut segitiga akan membuat mobil berguncang hebat.")
sa("c4", "sedang", T, Kn, S2, "Banyak pojok lancip pada bangun lingkaran adalah ... buah.", "0", "Lingkaran memiliki 0 pojok lancip.", verifikasi={"ekspresi": "0 * 1", "hasil": "0"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Bila lingkaran dipotong lurus tepat di tengah, bangun setengah lingkaran punya sudut?", ["punya 2 sudut", "tidak punya sudut", "punya 4 sudut", "punya 1 sudut"], "A", "Garis potong lurus bertemu garis lengkung di 2 titik sudut.", verifikasi={"ekspresi": "1 * 2", "hasil": "2"})
mc("c4", "sedang", X, Kn, S3, "Perhatikan bangun: segitiga, segiempat, segilima, lingkaran. Manakah tanpa sudut?", ["lingkaran", "segitiga", "segiempat", "segilima"], "A", "Hanya lingkaran yang tidak memiliki sudut.")
tf("c4", "sedang", X, Kn, S2, "Lingkaran memiliki titik sudut paling banyak di antara semua bangun datar.", "Salah", "Lingkaran tidak memiliki titik sudut sama sekali (0 sudut).")
mc("c4", "sulit", X, Me, S4, "Tiga anak menggambar: Ali gambar 2 segiempat, Budi 3 lingkaran, Cici 1 segitiga. Total sudut?", ["11 sudut", "14 sudut", "8 sudut", "9 sudut"], "A", "(2 x 4) + (3 x 0) + (1 x 3) = 8 + 0 + 3 = 11 sudut.", verifikasi={"ekspresi": "(2 * 4) + (3 * 0) + (1 * 3)", "hasil": "11"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Garis pembatas lingkaran dinamakan juga keliling lingkaran berupa garis ....", ["lengkung tertutup", "lurus patah", "sejajar putus", "bercabang tiga"], "A", "Keliling lingkaran berupa garis lengkung tertutup.")
mc("c4", "sulit", K, Me, S2, "Jika sudut diartikan sebagai pojok lancip, berapa pojok pada lingkaran sempurna?", ["0 pojok", "1 pojok", "2 pojok", "tak terhingga"], "A", "Lingkaran sempurna memiliki 0 pojok.", verifikasi={"ekspresi": "0 * 1", "hasil": "0"})
tf("c4", "sulit", K, Me, S3, "Sebuah lingkaran yang diperbesar ukurannya tetap memiliki nol sudut.", "Benar", "Ukuran membesar tidak mengubah fakta bahwa tepinya lengkung tanpa sudut.")
mc("c4", "sulit", K, Me, S4, "Sebuah roda berputar 5 putaran penuh. Berapa kali roda menabrak sudutnya sendiri?", ["0 kali", "5 kali", "10 kali", "1 kali"], "A", "Karena tidak punya sudut, roda tidak pernah menabrak sudutnya.", verifikasi={"ekspresi": "5 * 0", "hasil": "0"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Mengapa mangkuk makan sering dirancang berbibir lingkaran daripada segiempat?", ["agar mudah dibersihkan tanpa kotoran tersangkut di pojok sudut", "supaya makanan tumpah", "karena lebih berat", "supaya cepat pecah"], "A", "Tanpa sudut membuat makanan tidak terselip di celah pojok.")
mc("c5", "sedang", T, Me, S2, "Seorang anak menjumlahkan sudut: 4 segiempat + 6 lingkaran. Berapakah hasilnya?", ["16 sudut", "22 sudut", "24 sudut", "10 sudut"], "A", "(4 x 4) + (6 x 0) = 16 sudut.", verifikasi={"ekspresi": "(4 * 4) + (6 * 0)", "hasil": "16"})
mc("c5", "sedang", T, Me, S3, "Bandingkan jumlah sudut: Bangun A (10 lingkaran) vs Bangun B (1 segitiga). Siapa lebih banyak?", ["Bangun B (3 sudut)", "Bangun A (10 sudut)", "keduanya sama banyak", "tidak dapat dihitung"], "A", "Bangun A = 0 sudut, Bangun B = 3 sudut. Bangun B lebih banyak.")
mc("c5", "sulit", T, Me, S4, "Sebuah pola hiasan roda tersusun dari 8 lingkaran konsentris. Berapa total sudut hiasan?", ["0 sudut", "8 sudut", "16 sudut", "32 sudut"], "A", "8 x 0 = 0 sudut.", verifikasi={"ekspresi": "8 * 0", "hasil": "0"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Berapa banyak lingkaran yang harus digambar agar total sudutnya menyamai 1 segiempat?", ["tidak akan pernah bisa menyamai karena sudut lingkaran selalu 0", "4 lingkaran", "1 lingkaran", "10 lingkaran"], "A", "Berapa pun lingkaran dijumlahkan, sudutnya selalu 0 sehingga tidak bisa menyamai 4 sudut.")
mc("c5", "sulit", K, Me, S3, "Hitung total sudut bangun berikut: 5 segitiga, 4 segiempat, dan 7 lingkaran!", ["31 sudut", "28 sudut", "35 sudut", "38 sudut"], "A", "(5 x 3) + (4 x 4) + (7 x 0) = 15 + 16 + 0 = 31 sudut.", verifikasi={"ekspresi": "(5 * 3) + (4 * 4) + (7 * 0)", "hasil": "31"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Eksperimen: menggelindingkan balok kayu vs bola kayu pada bidang miring. Hasilnya?", ["bola kayu meluncur menggelinding cepat karena tanpa sudut penghambat", "balok kayu lebih cepat", "keduanya sama cepat", "balok terbang"], "A", "Bentuk bulat tanpa sudut mengurangi hambatan saat menggelinding.")
mc("c6", "sulit", K, Me, S4, "Jika kamu diminta membuat jam dinding yang paling mudah dibaca arah jarumnya?", ["berbentuk lingkaran dengan titik pusat tepat di tengah jarum", "berbentuk segitiga sempit", "berbentuk bintang banyak sudut", "berbentuk garis lurus"], "A", "Lingkaran simetris dengan jarak yang sama dari pusat ke setiap angka.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S2, "Hitung ekspresi total sudut: (7 x 4 sudut) + (6 x 3 sudut) + (9 x 0 sudut)!", ["46 sudut", "40 sudut", "48 sudut", "42 sudut"], "A", "28 + 18 + 0 = 46 sudut.", verifikasi={"ekspresi": "(7 * 4) + (6 * 3) + (9 * 0)", "hasil": "46"})
mc("c6", "sulit", P, Me, S3, "Mosaik dibuat dari 8 segilima dan 12 lingkaran. Berapakah jumlah seluruh sudutnya?", ["40 sudut", "36 sudut", "48 sudut", "52 sudut"], "A", "(8 x 5) + (12 x 0) = 40 sudut.", verifikasi={"ekspresi": "(8 * 5) + (12 * 0)", "hasil": "40"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab75_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab75.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")

