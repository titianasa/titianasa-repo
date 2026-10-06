#!/usr/bin/env python3
"""
Generator dan validator Bab 37 Matematika Kelas 1 SD:
"Kesalahan Umum: Mengira Satu Gambar Selalu Mewakili Satu Benda" (Fase A)
bab_id: 999e9f53-c533-4b4b-8535-f5d32ca24f88
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "e1f2a34b5c01"  # Mengapa Harus Membaca Keterangan Skala
S2 = "f2a3b45c6d12"  # Miskonsepsi Mengira Selalu Satu Lawan Satu
S3 = "a3b4c56d7e23"  # Mengenal Gambar yang Mewakili Dua Benda
S4 = "b4c5d67e8f34"  # Langkah Pasti Membaca Piktogram dengan Benar

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Banyak anak langsung menghitung gambar.
Mereka lupa membaca keterangan bawah.
Padahal keterangan sangatlah penting.
Keterangan adalah kunci rahasia diagram.
Keterangan memberi tahu nilai gambar.
Tanpa membaca keterangan piktogram.
Hitungan kita bisa salah total.
Mari selalu membacanya dahulu.

:::definition
title: Keterangan Skala
Keterangan skala memberi tahu berapa banyak benda yang diwakili oleh satu simbol gambar.
:::"""

s2_content = """Biasanya satu gambar mewakili satu benda.
Itu disebut skala satu-satu.
Namun kadang ada diagram berbeda.
Satu gambar bisa mewakili dua benda.
Bahkan bisa mewakili lima benda.
Jangan buru-buru menyimpulkan sendiri.
Lihatlah tulisan keterangan diagram.
Keterangan memberi tahu aturan mainnya.

:::steps
title: Urutan Membaca Piktogram
1. Baca judul data di paling atas.
2. Baca keterangan skala di paling bawah.
3. Hitung gambar sesuai nilai skala.
:::"""

s3_content = """Bagaimana jika satu gambar mewakili dua?
Kita bisa membilang loncat dua.
Dua, empat, enam, dan delapan.
Atau kita menjumlahkan angka dua.
Dua tambah dua jadi empat.
Tiga gambar bernilai enam benda.
Membilang loncat dua sangat asyik.
Hitungan kita menjadi sangat tepat."""

s4_content = """Mari kita ingat langkah pastinya.
Pertama, bacalah judul di atas.
Kedua, bacalah keterangan di bawah.
Ketiga, hitung gambar dengan teliti.
Gunakan aturan skala yang tertulis.
Kini kamu sudah ahli piktogram!

:::common_trap
title: Membaca Keterangan Piktogram
Jangan langsung menghitung gambar.
Baca keterangan skala di bawah diagram.
Perhatikan arti setiap satu gambar.
Bila 1 gambar mewakili 2 benda, bilang loncat dua.
Keterangan adalah kunci jawaban yang benar.
:::

:::callout
variant: summary
title: Ringkasan
text: Bacalah keterangan skala sebelum menghitung. Satu gambar bisa mewakili dua benda. Hitunglah dengan membilang loncat.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengapa Harus Membaca Keterangan Skala",
        "minutes": 6,
        "goal": "Siswa memahami peran vital legenda keterangan skala sebagai penentu nilai kuantitas gambar.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Miskonsepsi Mengira Selalu Satu Lawan Satu",
        "minutes": 6,
        "goal": "Siswa menyadari kesalahan umum mengasumsikan satu simbol selalu bernilai satu benda tanpa membaca keterangan.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mengenal Gambar yang Mewakili Dua Benda",
        "minutes": 6,
        "goal": "Siswa mampu menghitung nilai piktogram skala loncat dua (1 simbol = 2 benda) dengan tepat.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Langkah Pasti Membaca Piktogram dengan Benar",
        "minutes": 6,
        "goal": "Siswa menguasai prosedur menyeluruh membaca piktogram: judul, keterangan skala, dan perhitungan teliti.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Satu Gambar Mewakili Lebih dari Satu Benda",
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
# 2. DEFINISI BANK 50 SOAL BAB 37
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
mc("c1", "mudah", D, F, S1, "Keterangan pada piktogram berguna untuk memberi tahu ....", ["nilai benda yang diwakili tiap gambar", "nama pencetak buku", "harga kertas gambar", "warna cat dinding"], "A", "Keterangan skala memberi tahu nilai tiap simbol gambar.")
tf("c1", "mudah", D, F, S2, "Apakah satu gambar pada diagram piktogram selalu mewakili tepat satu benda?", "Salah", "Satu gambar bisa mewakili 2, 5, atau 10 benda.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S3, "Keterangan: 1 gambar bintang = 2 anak. Dua gambar bintang mewakili ....", ["4 anak", "2 anak", "3 anak", "5 anak"], "A", "2 x 2 = 4 anak.", verifikasi={"ekspresi": "2 * 2", "hasil": "4"})
mc("c1", "mudah", T, F, S4, "Sebelum mulai menghitung jumlah data piktogram, kita wajib membaca ....", ["keterangan skala di bawah", "cerita dongeng", "daftar isi buku", "halaman belakang"], "A", "Membaca keterangan skala adalah kunci kebenaran hitungan.")
sa("c1", "mudah", T, F, S3, "Keterangan: 1 apel mewakili 2 buah. Tiga gambar apel mewakili berapa buah?", "6", "3 x 2 = 6 buah apel.", verifikasi={"ekspresi": "3 * 2", "hasil": "6"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Apa kesalahan yang sering dilakukan anak saat membaca piktogram berskala dua?", ["langsung menghitung gambar satu per satu tanpa melipatgandakan", "membaca judul di atas", "melihat nama kategori", "menghitung dengan teliti"], "A", "Kesalahan umum adalah lupa mengalikan nilai skala gambar.", "Mengira satu simbol selalu mewakili satu benda")
tf("c2", "mudah", D, Kn, S1, "Kita boleh langsung menebak isi piktogram tanpa membaca tulisan keterangan.", "Salah", "Tanpa membaca keterangan, hitungan kita bisa salah total.")

# Remedial (2)
mc("c2", "mudah", R, F, S3, "Keterangan: 1 bunga = 2 tangkai. Ada 4 gambar bunga. Berapa tangkai bunga?", ["8 tangkai", "4 tangkai", "6 tangkai", "10 tangkai"], "A", "4 x 2 = 8 tangkai bunga.", "Keliru menghitung data berskala dua", verifikasi={"ekspresi": "4 * 2", "hasil": "8"})
mc("c2", "mudah", R, Kn, S2, "Mengapa satu gambar bisa mewakili dua atau lima benda sekaligus?", ["agar gambar tidak terlalu banyak dan muat rapi di kertas", "agar anak bingung", "karena kehabisan spidol", "agar kertas cepat robek"], "A", "Skala mempermudah penyajian data berjumlah besar agar ringkas dan rapi.", "Belum paham alasan penggunaan skala gambar")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Keterangan: 1 buku = 2 buah. Baris A ada 3 gambar buku. Berapa buku?", ["6 buku", "3 buku", "5 buku", "4 buku"], "A", "3 x 2 = 6 buku.", verifikasi={"ekspresi": "3 * 2", "hasil": "6"})
mc("c2", "mudah", T, Kn, S2, "Ada 6 anak pemilih. Jika 1 bintang mewakili 2 anak, digambar berapa bintang?", ["3 bintang", "6 bintang", "2 bintang", "4 bintang"], "A", "6 : 2 = 3 bintang.", verifikasi={"ekspresi": "6 // 2", "hasil": "3"})
tf("c2", "mudah", T, Kn, S3, "Bila 1 mobil mewakili 2 mobil, 5 gambar mobil berarti 10 mobil.", "Benar", "5 x 2 = 10 mobil.")
sa("c2", "mudah", T, Kn, S4, "Keterangan: 1 balon = 2 buah. Berapa nilai dari 4 gambar balon?", "8", "4 x 2 = 8 balon.", verifikasi={"ekspresi": "4 * 2", "hasil": "8"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Keterangan: 1 lingkaran = 2 orang. Ada 5 lingkaran. Berapa orang seluruhnya?", ["10 orang", "5 orang", "7 orang", "8 orang"], "A", "5 x 2 = 10 orang.", "Hanya menghitung banyaknya simbol tanpa mengalikan skala", verifikasi={"ekspresi": "5 * 2", "hasil": "10"})
mc("c3", "sedang", R, Pr, S4, "Data: 8 jeruk dan 4 apel (1 gambar = 2 buah). Berapa selisih buahnya?", ["4 buah", "2 buah", "6 buah", "3 buah"], "A", "8 - 4 = 4 buah.", "Keliru menghitung selisih berskala", verifikasi={"ekspresi": "8 - 4", "hasil": "4"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Keterangan: 1 pensil = 2 batang. Ada 3 pensil merah dan 2 pensil biru. Total?", ["10 batang", "5 batang", "8 batang", "7 batang"], "A", "(3 + 2) x 2 = 5 x 2 = 10 batang.", verifikasi={"ekspresi": "(3 + 2) * 2", "hasil": "10"})
mc("c3", "sedang", T, Pr, S2, "Keterangan: 1 gambar = 2 orang. Peminat lari ada 6 gambar. Berapa orang?", ["12 orang", "6 orang", "8 orang", "10 orang"], "A", "6 x 2 = 12 orang.", verifikasi={"ekspresi": "6 * 2", "hasil": "12"})
tf("c3", "sedang", T, Pr, S3, "Menghitung 1 gambar = 2 benda dapat dilakukan dengan membilang loncat dua.", "Benar", "Loncat dua: 2, 4, 6, 8, ...")
mc("c3", "sedang", T, Pr, S4, "Keterangan: 1 bola = 2 buah. Baris A ada 4 bola, baris B ada 2 bola. Selisih?", ["4 buah", "2 buah", "6 buah", "3 buah"], "A", "(4 - 2) x 2 = 2 x 2 = 4 buah.", verifikasi={"ekspresi": "(4 - 2) * 2", "hasil": "4"})
tf("c3", "sedang", T, Pr, S1, "Jika 1 gambar mewakili 2 anak, 3 gambar bintang bernilai 3 anak.", "Salah", "3 gambar bernilai 3 x 2 = 6 anak.")
sa("c3", "mudah", T, Pr, S3, "Keterangan: 1 koin = 2 keping. Berapa keping dari 6 gambar koin?", "12", "6 x 2 = 12 keping.", verifikasi={"ekspresi": "6 * 2", "hasil": "12"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Keterangan: 1 kotak susu = 2 kotak. Ada 7 gambar susu. Berapa total susu?", ["14 kotak", "7 kotak", "9 kotak", "12 kotak"], "A", "7 x 2 = 14 kotak.", verifikasi={"ekspresi": "7 * 2", "hasil": "14"})
mc("c3", "sedang", X, Pr, S2, "Ada 10 roti. Jika 1 gambar mewakili 2 roti, berapa gambar yang dibuat?", ["5 gambar", "10 gambar", "4 gambar", "6 gambar"], "A", "10 : 2 = 5 gambar.", verifikasi={"ekspresi": "10 // 2", "hasil": "5"})
tf("c3", "sedang", X, Pr, S3, "Tujuh gambar bintang bernilai 14 anak jika 1 bintang mewakili 2 anak.", "Benar", "7 x 2 = 14 anak.")
sa("c3", "sedang", X, Pr, S4, "Keterangan: 1 pohon = 2 batang. Ada 8 gambar pohon. Berapa total pohon?", "16", "8 x 2 = 16 pohon.", verifikasi={"ekspresi": "8 * 2", "hasil": "16"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Keterangan: 1 ikan = 2 ekor. Di kolam ada 6 gambar ikan. Berapa ekor?", ["12 ekor", "6 ekor", "8 ekor", "10 ekor"], "A", "6 x 2 = 12 ekor.", verifikasi={"ekspresi": "6 * 2", "hasil": "12"})
mc("c3", "sedang", K, Pr, S4, "Keterangan: 1 topi = 2 buah. Baris A ada 5 topi, baris B ada 3 topi. Selisih?", ["4 buah", "2 buah", "6 buah", "3 buah"], "A", "(5 - 3) x 2 = 2 x 2 = 4 buah.", verifikasi={"ekspresi": "(5 - 3) * 2", "hasil": "4"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Mengapa diagram buah di kebun menggunakan skala 1 gambar = 2 pohon?", ["karena jumlah pohon sangat banyak sehingga lebih rapi jika disingkat", "karena kertasnya habis", "agar pohonnya tumbuh cepat", "supaya gambar tidak bisa dibaca"], "A", "Skala menyederhanakan data yang kuantitasnya banyak.")
mc("c4", "sedang", T, Kn, S2, "Ada 4 gambar apel (keterangan: 1 apel = 2 buah). Berapa buah apel sebenarnya?", ["8 buah", "4 buah", "6 buah", "10 buah"], "A", "Jawaban benar adalah 4 x 2 = 8 buah.", verifikasi={"ekspresi": "4 * 2", "hasil": "8"})
tf("c4", "sedang", T, Kn, S3, "Baris dengan 3 gambar berskala 2 bernilai lebih sedikit dari baris 5 gambar berskala 1.", "Salah", "3 x 2 = 6 benda, lebih banyak daripada 5 x 1 = 5 benda.")
tf("c4", "sedang", T, Kn, S4, "Keterangan skala piktogram harus dipakai secara konsisten untuk seluruh baris data.", "Benar", "Skala berlaku sama untuk seluruh kategori data diagram.")
sa("c4", "sedang", T, Kn, S4, "Keterangan: 1 buku = 2 buah. Ada 9 gambar buku. Berapa total buku?", "18", "9 x 2 = 18 buku.", verifikasi={"ekspresi": "9 * 2", "hasil": "18"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Diagram A: 4 gambar (skala 2). Diagram B: 8 gambar (skala 1). Perbandingan keduanya?", ["keduanya sama banyak bernilai 8", "diagram A lebih banyak", "diagram B lebih banyak", "tidak bisa dihitung"], "A", "A: 4 x 2 = 8. B: 8 x 1 = 8. Keduanya sama banyak.")
mc("c4", "sedang", X, Kn, S2, "Ada 16 anak. Jika 1 bintang = 2 anak, berapa banyak bintang pada baris?", ["8 bintang", "16 bintang", "6 bintang", "10 bintang"], "A", "16 : 2 = 8 bintang.", verifikasi={"ekspresi": "16 // 2", "hasil": "8"})
tf("c4", "sedang", X, Kn, S3, "Memiliki 5 gambar pada skala 2 menghasilkan total 10 benda.", "Benar", "5 x 2 = 10 benda.")
mc("c4", "sulit", X, Me, S4, "Keterangan: 1 kue = 2 potong. Doni punya 8 gambar, diambil 3 gambar. Sisa kue?", ["10 potong", "8 potong", "12 potong", "6 potong"], "A", "(8 - 3) x 2 = 5 x 2 = 10 potong kue.", verifikasi={"ekspresi": "(8 - 3) * 2", "hasil": "10"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Lani langsung menjawab data tanpa membaca keterangan di bawah. Sikap Lani ....", ["kurang teliti karena bisa salah menghitung nilai sebenarnya", "sangat hebat dan pintar", "paling benar di kelas", "patut dicontoh"], "A", "Membaca keterangan adalah prosedur wajib agar hitungan benar.")
mc("c4", "sulit", K, Me, S2, "Keterangan: 1 stiker = 2 lembar. Baris A ada 7 stiker, baris B ada 4 stiker. Selisih?", ["6 lembar", "3 lembar", "8 lembar", "4 lembar"], "A", "(7 - 4) x 2 = 3 x 2 = 6 lembar.", verifikasi={"ekspresi": "(7 - 4) * 2", "hasil": "6"})
tf("c4", "sulit", K, Me, S3, "Jika skala 1 gambar = 2 anak, 6 anak digambar dengan 6 simbol bintang.", "Salah", "6 anak digambar dengan 6 : 2 = 3 simbol bintang.")
mc("c4", "sulit", K, Me, S4, "Keterangan: 1 mobil = 2 unit. Sedan 4 gambar, bus 3 gambar, truk 2 gambar. Total?", ["18 unit", "16 unit", "20 unit", "14 unit"], "A", "(4 + 3 + 2) x 2 = 9 x 2 = 18 unit mobil.", verifikasi={"ekspresi": "(4 + 3 + 2) * 2", "hasil": "18"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Keterangan: 1 buah = 2 biji. Mangga 5 gambar, jeruk 4 gambar. Berapa total seluruh buah?", ["18 buah", "16 buah", "20 buah", "14 buah"], "A", "(5 + 4) x 2 = 9 x 2 = 18 buah.", verifikasi={"ekspresi": "(5 + 4) * 2", "hasil": "18"})
mc("c5", "sedang", T, Me, S2, "Ada 20 siswa: renang 6 gambar (skala 2), sisanya lari. Berapa gambar lari?", ["4 gambar", "5 gambar", "3 gambar", "6 gambar"], "A", "Renang = 6 x 2 = 12. Lari = 20 - 12 = 8 siswa. Gambar lari = 8 : 2 = 4 gambar.", verifikasi={"ekspresi": "(20 - 6 * 2) // 2", "hasil": "4"})
mc("c5", "sedang", T, Me, S3, "Keterangan: 1 bintang = 2 nilai. Dayu dapat 8 bintang, Siti dapat 5 bintang. Selisih?", ["6 nilai", "4 nilai", "8 nilai", "3 nilai"], "A", "(8 - 5) x 2 = 3 x 2 = 6 nilai.", verifikasi={"ekspresi": "(8 - 5) * 2", "hasil": "6"})
mc("c5", "sulit", T, Me, S4, "Keterangan: 1 burung = 2 ekor. Merpati 4, pipit 3, gereja 2. Berapa ekor?", ["18 ekor", "16 ekor", "20 ekor", "14 ekor"], "A", "(4 + 3 + 2) x 2 = 9 x 2 = 18 ekor burung.", verifikasi={"ekspresi": "(4 + 3 + 2) * 2", "hasil": "18"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Keterangan: 1 piala = 2 buah. Kelas A punya 5 gambar, kelas B punya 3 gambar. Selisih?", ["4 buah", "2 buah", "6 buah", "3 buah"], "A", "(5 - 3) x 2 = 4 buah piala.", verifikasi={"ekspresi": "(5 - 3) * 2", "hasil": "4"})
mc("c5", "sulit", K, Me, S3, "Ada 18 kelereng. Disajikan piktogram skala 2. Berapa banyak gambar kelereng dibuat?", ["9 gambar", "8 gambar", "10 gambar", "7 gambar"], "A", "18 : 2 = 9 gambar.", verifikasi={"ekspresi": "18 // 2", "hasil": "9"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Baris A ada 3 gambar, B ada 4. Mengapa baris A bisa bernilai lebih banyak?", ["karena baris A berskala 1 gambar = 5 benda, sedangkan B berskala 1 gambar = 1 benda", "karena baris A digambar warna merah", "karena baris B gambarnya jelek", "karena kertasnya miring"], "A", "Nilai total bergantung pada skala keterangan gambar masing-masing diagram.")
mc("c6", "sulit", K, Me, S4, "Evaluasilah diagram: apel 4 gambar, jeruk 6 gambar (keterangan: 1 gambar = 2 buah). Kesimpulan yang benar?", ["jeruk lebih banyak 4 buah daripada apel", "apel lebih banyak dari jeruk", "keduanya sama banyak", "apel berjumlah 12 buah"], "A", "Jeruk: 6 x 2 = 12. Apel: 4 x 2 = 8. Selisih: 12 - 8 = 4 buah.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Keterangan: 1 bunga = 2 tangkai. Mawar 9 gambar, melati 7 gambar, dahlia 4 gambar. Total?", ["40 tangkai", "38 tangkai", "42 tangkai", "36 tangkai"], "A", "(9 + 7 + 4) x 2 = 20 x 2 = 40 tangkai.", verifikasi={"ekspresi": "(9 + 7 + 4) * 2", "hasil": "40"})
mc("c6", "sulit", P, Me, S4, "Keterangan: 1 koin = 2 rupiah. Edo punya 12 gambar koin, Beni punya 5 gambar koin. Selisih?", ["14 rupiah", "12 rupiah", "16 rupiah", "10 rupiah"], "A", "(12 - 5) x 2 = 7 x 2 = 14 rupiah.", verifikasi={"ekspresi": "(12 - 5) * 2", "hasil": "14"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab37_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab37.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
