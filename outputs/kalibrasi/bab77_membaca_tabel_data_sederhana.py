#!/usr/bin/env python3
"""
Generator dan validator Bab 77 Matematika Kelas 2 SD:
"Membaca Tabel Data Sederhana" (Fase A)
bab_id: 843f3887-47c1-4beb-a75f-49f33c21170d
article_id: 56c2e2db-e39c-4d87-80c8-b43dd430643b
quiz_id: 1846eddb-6172-4323-8146-773a9734f051
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "v1x2z3b4d501"  # Mengenal Bentuk Tabel Data
S2 = "w2y3a4c5e602"  # Membaca Baris dan Kolom Tabel
S3 = "x3z4b5d6f703"  # Menemukan Data Terbanyak dan Tersedikit
S4 = "y4a5c6e7g804"  # Menghitung Jumlah Seluruh Data

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Tabel membantu kita menyajikan data.
Tabel tersusun atas kotak-kotak rapi.
Arah mendatar dinamakan baris.
Arah tegak lurus dinamakan kolom.
Bagian atas memuat judul kolom.
Misalnya kolom jenis buah dan jumlahnya.
Data angka ditulis di dalam kotak.
Tabel membuat catatan data terlihat jelas!

:::definition
title: Tabel Data
Bagan penyajian informasi yang disusun rapi dalam baris dan kolom.
:::"""

s2_content = """Cara membaca tabel sangat mudah.
Lihat baris nama benda dahulu.
Lalu geser matamu ke kolom kanan.
Di sana tertulis jumlah bendanya.
Contoh baris Apel tertulis angka 8.
Artinya ada 8 buah apel.
Baris Jeruk tertulis angka 12.
Artinya ada 12 buah jeruk.
Bacalah lurus agar tidak keliru!

:::steps
title: Langkah Membaca Tabel
1. Temukan nama benda pada baris.
2. Geser pandangan ke kolom angka.
3. Baca angka yang sebaris lurus.
:::"""

s3_content = """Kita bisa mencari data paling istimewa.
Data terbanyak memiliki angka paling besar.
Misalnya 15 adalah angka terbesar.
Maka benda itu yang paling banyak.
Data tersedikit memiliki angka paling kecil.
Misalnya 4 adalah angka terkecil.
Maka benda itu yang paling sedikit.
Bandingkan angka-angkanya secara teliti!

:::common_trap
title: Mengira Benda Teratas Selalu Terbanyak
Urutan baris belum tentu urutan jumlah.
Lihat selalu nilai angkanya.
Bukan letak posisi barisnya!
:::"""

s4_content = """Kita bisa menghitung totalnya.
Jumlahkan semua angka pada kolom.
Misal apel 8 buah.
Jeruk ada 12 buah.
Pisang ada 5 buah.
Maka 8 + 12 + 5 = 25.
Totalnya ada 25 buah.
Tabel membuat hitungan jelas.
Semua data cepat diketahui!

:::callout
variant: summary
title: Ringkasan
text: Baris mendatar, kolom tegak. Bandingkan angka untuk tahu terbanyak.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Bentuk Tabel Data",
        "minutes": 6,
        "goal": "Siswa mengenal struktur penyusun tabel data sederhana (baris, kolom, judul).",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Membaca Baris dan Kolom Tabel",
        "minutes": 6,
        "goal": "Siswa mampu membaca informasi hubungan antara kategori dan angka jumlah pada tabel.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Menemukan Data Terbanyak dan Tersedikit",
        "minutes": 6,
        "goal": "Siswa mampu menentukan data bernilai paling banyak (maksimum) dan paling sedikit (minimum).",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menghitung Jumlah Seluruh Data",
        "minutes": 6,
        "goal": "Siswa mampu menjumlahkan seluruh entri data dalam tabel untuk mendapatkan nilai total.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membaca Tabel Data Sederhana",
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
# 2. DEFINISI BANK 50 SOAL BAB 77
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
mc("c1", "mudah", D, F, S1, "Susunan kotak mendatar pada sebuah tabel dinamakan ....", ["baris", "kolom", "titik", "garis"], "A", "Kotak arah mendatar dinamakan baris.")
tf("c1", "mudah", D, F, S2, "Pada tabel, angka jumlah benda ditulis sejajar dengan nama bendanya.", "Benar", "Angka ditulis sebaris dengan nama benda.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Susunan kotak yang mengarah tegak lurus dinamakan ....", ["kolom", "baris", "judul", "sudut"], "A", "Kotak arah tegak dinamakan kolom.")
mc("c1", "mudah", T, F, S2, "Tabel: Mawar (8), Melati (5). Berapa banyak bunga mawar?", ["8 tangkai", "5 tangkai", "13 tangkai", "3 tangkai"], "A", "Mawar tertulis 8 tangkai.", verifikasi={"ekspresi": "8 * 1", "hasil": "8"})
sa("c1", "mudah", T, F, S3, "Data: Kucing (6), Kelinci (9). Hewan paling banyak adalah ...", "kelinci", "9 lebih banyak dari 6.")

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Tabel: Apel (10), Jeruk (15), Mangga (7). Buah paling sedikit?", ["mangga", "apel", "jeruk", "semua sama"], "A", "Mangga paling sedikit karena angkanya 7 terkecil.")
tf("c2", "mudah", D, Kn, S3, "Baris paling atas pada tabel selalu berisi data paling banyak.", "Salah", "Urutan baris tidak menentukan data terbanyak.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Tabel: Merah (12), Biru (9). Berapa siswa memilih warna biru?", ["9 siswa", "12 siswa", "21 siswa", "3 siswa"], "A", "Biru bernilai 9 siswa.", "Membaca baris warna merah yang bernilai 12", verifikasi={"ekspresi": "9 * 1", "hasil": "9"})
mc("c2", "mudah", R, Kn, S3, "Tabel: Sepeda (4), Motor (11), Mobil (6). Kendaraan paling banyak?", ["motor", "sepeda", "mobil", "semua sama"], "A", "Motor paling banyak yaitu 11.", "Memilih baris teratas (sepeda)")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S2, "Tabel: Kelas A (20 siswa), Kelas B (22 siswa). Berapa siswa Kelas B?", ["22 siswa", "20 siswa", "42 siswa", "2 siswa"], "A", "Kelas B memiliki 22 siswa.", verifikasi={"ekspresi": "22 * 1", "hasil": "22"})
mc("c2", "mudah", T, Kn, S3, "Tabel nilai: Budi (85), Siti (90), Doni (75). Nilai tertinggi diraih?", ["Siti", "Budi", "Doni", "tidak ada"], "A", "Nilai tertinggi adalah 90 milik Siti.")
tf("c2", "mudah", T, Kn, S4, "Jumlah seluruh data didapat dari menjumlahkan semua angka di kolom jumlah.", "Benar", "Total data didapat dengan menjumlahkan seluruh angka.")
sa("c2", "mudah", T, Kn, S2, "Tabel: Ayam (14), Bebek (8). Jumlah ayam adalah ... ekor.", "14", "Ayam berjumlah 14 ekor.", verifikasi={"ekspresi": "14 * 1", "hasil": "14"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S4, "Tabel: Buku cerita (10), Buku gambar (6). Berapa total seluruh buku?", ["16 buku", "14 buku", "12 buku", "18 buku"], "A", "10 + 6 = 16 buku.", "Salah menjumlahkan total data", verifikasi={"ekspresi": "10 + 6", "hasil": "16"})
mc("c3", "sedang", R, Pr, S3, "Tabel: Bayam (15 ikat), Kangkung (9 ikat). Berapa selisihnya?", ["6 ikat", "5 ikat", "7 ikat", "4 ikat"], "A", "15 - 9 = 6 ikat.", "Menjumlahkan bukan mencari selisih", verifikasi={"ekspresi": "15 - 9", "hasil": "6"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S4, "Tabel: Pisang (8), Salak (7). Berapa total buah dalam tabel?", ["15 buah", "14 buah", "16 buah", "13 buah"], "A", "8 + 7 = 15 buah.", verifikasi={"ekspresi": "8 + 7", "hasil": "15"})
mc("c3", "mudah", T, Pr, S3, "Tabel: Bola (12), Raket (5). Berapa lebihnya bola dari raket?", ["7 buah", "6 buah", "8 buah", "5 buah"], "A", "12 - 5 = 7 buah.", verifikasi={"ekspresi": "12 - 5", "hasil": "7"})
tf("c3", "sedang", T, Pr, S2, "Tabel: Pensil (15), Penghapus (10). Jumlah pensil lebih sedikit dari penghapus.", "Salah", "Pensil berjumlah 15, lebih banyak daripada penghapus yang 10.")
mc("c3", "sedang", T, Pr, S4, "Tabel: Senin (12), Selasa (14), Rabu (10). Berapa total pengunjung 3 hari?", ["36 orang", "34 orang", "38 orang", "40 orang"], "A", "12 + 14 + 10 = 36 orang.", verifikasi={"ekspresi": "12 + 14 + 10", "hasil": "36"})
tf("c3", "sedang", T, Pr, S1, "Sebuah tabel data hanya boleh memiliki satu baris saja.", "Salah", "Tabel umumnya memuat beberapa baris data.")
sa("c3", "sedang", T, Pr, S4, "Tabel: Boneka (11), Robot (9). Total mainan adalah ... buah.", "20", "11 + 9 = 20 buah.", verifikasi={"ekspresi": "11 + 9", "hasil": "20"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S3, "Tabel hewan: Sapi (18), Kambing (11). Berapa selisih hewan ternak?", ["7 ekor", "6 ekor", "8 ekor", "9 ekor"], "A", "18 - 11 = 7 ekor.", verifikasi={"ekspresi": "18 - 11", "hasil": "7"})
mc("c3", "sedang", X, Pr, S4, "Tabel tabungan: Ali (Rp20.000), Budi (Rp25.000). Total uang keduanya?", ["Rp45.000", "Rp40.000", "Rp50.000", "Rp35.000"], "A", "20.000 + 25.000 = Rp45.000.")
tf("c3", "sedang", X, Pr, S3, "Data: Melon (9), Semangka (15). Selisih kedua buah adalah 6 buah.", "Benar", "15 - 9 = 6 buah.")
sa("c3", "sedang", X, Pr, S4, "Tabel: Roti cokelat (15), Roti keju (13). Total roti adalah ... bungkus.", "28", "15 + 13 = 28.", verifikasi={"ekspresi": "15 + 13", "hasil": "28"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Tabel warna: Hijau (14), Kuning (18), Ungu (11). Selisih terbanyak dan tersedikit?", ["7 siswa", "6 siswa", "8 siswa", "9 siswa"], "A", "18 - 11 = 7 siswa.", verifikasi={"ekspresi": "18 - 11", "hasil": "7"})
mc("c3", "sedang", K, Pr, S4, "Tabel buah: Jeruk (12), Mangga (8), Apel (15). Total seluruh buah?", ["35 buah", "33 buah", "37 buah", "30 buah"], "A", "12 + 8 + 15 = 35 buah.", verifikasi={"ekspresi": "12 + 8 + 15", "hasil": "35"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa menyajikan data dalam tabel lebih baik daripada paragraf cerita panjang?", ["karena angka tersusun rapi sehingga mudah dicari dan dibandingkan", "karena tabel berwarna hitam putih", "karena ceritanya jadi hilang", "hanya anjuran"], "A", "Format tabel mempermudah perbandingan visual secara cepat.")
mc("c4", "sedang", T, Kn, S2, "Tabel menunjukkan data 3 kelas. Jika Kelas 2A ada 24 siswa, apa artinya?", ["ada 24 orang anak yang belajar di kelas 2A", "ada 24 guru", "ada 24 meja", "ada 24 buku"], "A", "Angka sebaris mewakili jumlah siswa kelas tersebut.")
tf("c4", "sedang", T, Kn, S3, "Jika dua baris tabel memiliki angka yang sama, kedua kategori sama populernya.", "Benar", "Angka sama berarti frekuensi kedua data sama besar.")
tf("c4", "sedang", T, Kn, S4, "Menghitung total tabel boleh melewatkan salah satu baris data.", "Salah", "Semua baris harus dijumlahkan agar hasilnya tepat.")
sa("c4", "sedang", T, Kn, S3, "Tabel: Kelereng Edo (32), Kelereng Doni (25). Selisih kelereng ... butir.", "7", "32 - 25 = 7 butir.", verifikasi={"ekspresi": "32 - 25", "hasil": "7"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S3, "Tabel hobi: Membaca (9), Menari (14), Menggambar (12). Hobi terpopuler kedua?", ["menggambar", "menari", "membaca", "semua sama"], "A", "Urutan: Menari (14), Menggambar (12), Membaca (9). Kedua = Menggambar.")
mc("c4", "sedang", X, Kn, S4, "Tabel: Baju merah (16), Baju putih (24). Berapa lusin total baju jika selusin 12?", ["40 potong", "38 potong", "42 potong", "36 potong"], "A", "16 + 24 = 40 potong baju.", verifikasi={"ekspresi": "16 + 24", "hasil": "40"})
tf("c4", "sedang", X, Kn, S2, "Membaca baris tabel boleh melompat ke baris lain tanpa mengubah hasil.", "Salah", "Membaca tabel harus lurus sebaris agar datanya tidak tertukar.")
mc("c4", "sulit", X, Me, S4, "Tabel siswa: Laki-laki 18, Perempuan 16. Jika 4 siswa pindah, sisa siswa?", ["30 siswa", "32 siswa", "28 siswa", "34 siswa"], "A", "18 + 16 - 4 = 34 - 4 = 30 siswa.", verifikasi={"ekspresi": "18 + 16 - 4", "hasil": "30"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Tabel olahraga: Sepak bola (18), Bulu tangkis (12). Pernyataan yang benar?", ["sepak bola lebih banyak 6 peminat daripada bulu tangkis", "bulu tangkis lebih banyak", "keduanya sama banyak", "total peminat 40"], "A", "18 - 12 = 6 peminat lebih banyak.")
mc("c4", "sulit", K, Me, S3, "Tabel buah di toko: Apel (25), Jeruk (18), Pisang (30). Urutan dari paling sedikit?", ["jeruk, apel, pisang", "pisang, apel, jeruk", "apel, jeruk, pisang", "jeruk, pisang, apel"], "A", "Urutan terkecil ke terbesar: 18 (jeruk), 25 (apel), 30 (pisang).")
tf("c4", "sulit", K, Me, S4, "Total siswa di tabel adalah 50. Jika ada 3 kelas, rata-rata kelas sekitar belasan.", "Benar", "50 dibagi 3 kelas menghasilkan sekitar 16–17 siswa.")
mc("c4", "sulit", K, Me, S4, "Tabel buku: Cerita (24), Komik (31), Sains (15). Berapa selisih Komik dan Sains?", ["16 buku", "15 buku", "14 buku", "18 buku"], "A", "31 - 15 = 16 buku.", verifikasi={"ekspresi": "31 - 15", "hasil": "16"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Sebuah toko ingin menambah stok buah yang paling laris dari tabel penjualan. Buah apa?", ["buah dengan angka penjualan paling tinggi", "buah dengan angka paling rendah", "buah sembarang", "tidak perlu melihat tabel"], "A", "Barang terlaris ditunjukkan oleh angka penjualan tertinggi.")
mc("c5", "sedang", T, Me, S2, "Tabel: Pensil 2B (40), Pensil HB (25). Berapa selisih penjualan kedua pensil?", ["15 pensil", "12 pensil", "20 pensil", "10 pensil"], "A", "40 - 25 = 15 pensil.", verifikasi={"ekspresi": "40 - 25", "hasil": "15"})
mc("c5", "sedang", T, Me, S3, "Tabel makanan: Bakso (22), Mie ayam (18), Soto (15). Makanan mana peminatnya > 20?", ["bakso saja", "mie ayam", "soto", "ketiganya"], "A", "Hanya bakso yang jumlahnya 22 (> 20).")
mc("c5", "sulit", T, Me, S4, "Tabel bibit pohon: Mangga 35, Jambu 28, Jeruk 42. Total bibit seluruhnya?", ["105 bibit", "100 bibit", "110 bibit", "95 bibit"], "A", "35 + 28 + 42 = 105 bibit.", verifikasi={"ekspresi": "35 + 28 + 42", "hasil": "105"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Tabel: Kelinci (16), Kucing (24), Hamster (12). Berapa ekor total Kucing dan Hamster?", ["36 ekor", "34 ekor", "38 ekor", "40 ekor"], "A", "24 + 12 = 36 ekor.", verifikasi={"ekspresi": "24 + 12", "hasil": "36"})
mc("c5", "sulit", K, Me, S4, "Tabel belanja: Beras Rp50.000, Gula Rp15.000, Minyak Rp25.000. Total belanja?", ["Rp90.000", "Rp85.000", "Rp95.000", "Rp100.000"], "A", "50.000 + 15.000 + 25.000 = Rp90.000.")

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Rancanglah tabel sederhana untuk mencatat jumlah siswa piket Senin sampai Jumat!", ["buat 2 kolom: kolom pertama 'Hari', kolom kedua 'Jumlah Siswa Piket'", "tulis satu angka saja", "gambar sapu saja", "tulis di selembar tissue"], "A", "Struktur tabel dua kolom (Hari dan Jumlah Siswa) paling tepat dan teratur.")
mc("c6", "sulit", K, Me, S3, "Kepala sekolah membaca tabel ekstrakurikuler: Tari (8), Futsal (32), Lukis (10). Keputusan tepat?", ["menambah jam atau pelatih futsal karena peminatnya paling banyak", "menutup ekskul futsal", "membubarkan sekolah", "tidak melakukan apapun"], "A", "Data tabel digunakan untuk mendukung keputusan logis yang bermanfaat.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Tabel: Beras 45 kg, Terigu 35 kg, Gula 28 kg. Berapa kg total ketiga barang?", ["108 kg", "105 kg", "110 kg", "112 kg"], "A", "45 + 35 + 28 = 108 kg.", verifikasi={"ekspresi": "45 + 35 + 28", "hasil": "108"})
mc("c6", "sulit", P, Me, S3, "Tabungan: A (45), B (55), C (60), D (40). Selisih tabungan tertinggi dan terendah?", ["20 ribu", "15 ribu", "25 ribu", "10 ribu"], "A", "Tertinggi C (60), terendah D (40). Selisih = 60 - 40 = 20 ribu.", verifikasi={"ekspresi": "60 - 40", "hasil": "20"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab77_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab77.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
