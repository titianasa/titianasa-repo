#!/usr/bin/env python3
"""
Generator dan validator Bab 79 Matematika Kelas 2 SD:
"Membandingkan Data pada Tabel" (Fase A)
bab_id: b2d4659b-5ce3-4e62-b92e-06cc64243b35
article_id: 69e0a6ff-822f-4c4f-bcb6-a0fe1f97f246
quiz_id: 767c57ee-ebb2-42a5-b810-32e37c8353c6
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "x1z2b3d4f501"  # Istilah Perbandingan Data
S2 = "y2a3c4e5g602"  # Menghitung Selisih Dua Data
S3 = "z3b4d5f6h703"  # Mengurutkan Data pada Tabel
S4 = "a4c5e6g7i804"  # Menarik Kesimpulan dari Tabel

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Tabel membantu kita membandingkan data.
Ada kata lebih banyak.
Ada kata lebih sedikit.
Ada juga kata sama banyak.
Bandingkan dua angka pada baris.
Angka 15 lebih banyak dari 9.
Angka 6 lebih sedikit dari 10.
Jika angkanya sama nilainya setara!

:::definition
title: Membandingkan Data
Menentukan hubungan lebih banyak, lebih sedikit, atau sama banyak antara dua nilai.
:::"""

s2_content = """Berapa selisih antara dua data?
Selisih dicari dengan pengurangan.
Kurangkan angka besar dengan kecil.
Contoh apel 14 dan jeruk 8.
Selisihnya adalah 14 dikurang 8.
14 - 8 = 6 buah.
Apel lebih banyak 6 buah.
Jeruk lebih sedikit 6 buah!

:::steps
title: Menghitung Selisih Data
1. Cari angka yang lebih besar.
2. Cari angka yang lebih kecil.
3. Kurangkan: Angka besar dikurangi angka kecil.
:::"""

s3_content = """Data dapat diurutkan teratur.
Bisa dari yang paling sedikit.
Bisa juga dari yang terbanyak.
Lihat semua angka pada kolom.
Urutkan angka dari kecil ke besar.
Atau balik dari besar ke kecil.
Urutan membuat data sangat rapi!

:::common_trap
title: Mengira Mengurutkan Baris Mengubah Data Asli
Mengurutkan hanya menyusun kembali urutan tampilan.
Nilai angka tiap benda tetap sama.
Jangan sampai tertukar pasangan bendanya!
:::"""

s4_content = """Data tabel memberi petunjuk nyata.
Kita bisa membuat keputusan tepat.
Buku yang sedikit dibaca ditambah.
Makanan paling laris disediakan lebih banyak.
Tabel bukan sekadar deretan angka.
Tabel membantu kehidupan kita sehari-hari!

:::callout
variant: summary
title: Ringkasan
text: Bandingkan angka tabel. Cari selisih dengan cara pengurangan.
:::"""

sections = [
    {
        "id": S1,
        "title": "Istilah Perbandingan Data",
        "minutes": 6,
        "goal": "Siswa memahami konsep perbandingan kuantitas (lebih banyak, lebih sedikit, sama banyak).",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Menghitung Selisih Dua Data",
        "minutes": 6,
        "goal": "Siswa mampu menghitung selisih matematis antara dua kategori data dengan operasi pengurangan.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mengurutkan Data pada Tabel",
        "minutes": 6,
        "goal": "Siswa mampu mengurutkan entri tabel dari nilai terkecil ke terbesar atau sebaliknya.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menarik Kesimpulan dari Tabel",
        "minutes": 6,
        "goal": "Siswa mampu menyimpulkan informasi dan implikasi praktis dari perbandingan data tabel.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membandingkan Data pada Tabel",
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
# 2. DEFINISI BANK 50 SOAL BAB 79
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
mc("c1", "mudah", D, F, S1, "Kata perbandingan untuk angka 18 terhadap angka 12 adalah ....", ["lebih banyak dari", "lebih sedikit dari", "sama banyak dengan", "setengah dari"], "A", "18 lebih banyak daripada 12.")
tf("c1", "mudah", D, F, S2, "Selisih antara dua data dihitung dengan cara mengurangkan angka yang lebih besar.", "Benar", "Selisih = Angka besar - Angka kecil.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Tabel: Apel 15, Mangga 15. Hubungan perbandingan kedua buah adalah ....", ["sama banyak", "apel lebih banyak", "mangga lebih banyak", "tidak ada apel"], "A", "15 sama nilainya dengan 15.")
mc("c1", "mudah", T, F, S2, "Tabel: Ayam 10, Bebek 4. Berapa selisih ayam dan bebek?", ["6 ekor", "5 ekor", "7 ekor", "4 ekor"], "A", "10 - 4 = 6 ekor.", verifikasi={"ekspresi": "10 - 4", "hasil": "6"})
sa("c1", "mudah", T, F, S2, "Tabel: Bola 14, Raket 8. Selisih kedua alat olahraga adalah ... buah.", "6", "14 - 8 = 6 buah.", verifikasi={"ekspresi": "14 - 8", "hasil": "6"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Urutan angka data: 12, 5, 20 dari yang paling sedikit adalah ....", ["5, 12, 20", "20, 12, 5", "12, 5, 20", "5, 20, 12"], "A", "Urutan terkecil ke terbesar: 5, 12, 20.")
tf("c2", "mudah", D, Kn, S1, "Jika Siti punya 10 buku dan Edo 14 buku, Siti punya lebih banyak buku.", "Salah", "Siti memiliki 10 buku, lebih sedikit dari 14 buku Edo.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Tabel: Merah (16), Biru (9). Berapa lebihnya siswa penyuka warna merah?", ["7 siswa", "6 siswa", "8 siswa", "5 siswa"], "A", "16 - 9 = 7 siswa.", "Menjumlahkan bukannya mengurangkan", verifikasi={"ekspresi": "16 - 9", "hasil": "7"})
mc("c2", "mudah", R, Kn, S1, "Tabel: Pensil (8), Penghapus (11). Pernyataan yang benar adalah ....", ["pensil lebih sedikit daripada penghapus", "pensil lebih banyak", "keduanya sama banyak", "penghapus ada 8"], "A", "8 lebih sedikit daripada 11.", "Salah menafsirkan kata lebih sedikit")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S3, "Tabel hewan: Kucing (7), Ikan (15), Burung (4). Hewan urutan kedua terbanyak?", ["kucing", "ikan", "burung", "semua sama"], "A", "Urutan terbanyak: Ikan (15), Kucing (7), Burung (4). Kedua = Kucing.")
mc("c2", "mudah", T, Kn, S4, "Toko mencatat susu rasa cokelat paling cepat habis terjual. Toko sebaiknya ....", ["menambah persediaan susu rasa cokelat", "berhenti menjual susu cokelat", "menutup toko", "membuang susu"], "A", "Barang yang laris sebaiknya ditambah stoknya.")
tf("c2", "mudah", T, Kn, S2, "Selisih antara 20 buku dan 15 buku adalah 10 buku.", "Salah", "20 - 15 = 5 buku, bukan 10 buku.")
sa("c2", "mudah", T, Kn, S2, "Tabel: Kelereng Ali 25, Kelereng Budi 18. Selisih kelereng ... butir.", "7", "25 - 18 = 7 butir.", verifikasi={"ekspresi": "25 - 18", "hasil": "7"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Tabel: Mawar (22), Melati (15). Berapa selisih bunga keduanya?", ["7 tangkai", "6 tangkai", "8 tangkai", "5 tangkai"], "A", "22 - 15 = 7 tangkai.", "Keliru saat menghitung selisih 22 dan 15", verifikasi={"ekspresi": "22 - 15", "hasil": "7"})
mc("c3", "sedang", R, Pr, S3, "Urutan buah dari yang terbanyak: Apel (18), Jeruk (25), Pisang (14)?", ["jeruk, apel, pisang", "apel, jeruk, pisang", "pisang, apel, jeruk", "jeruk, pisang, apel"], "A", "Dari terbanyak: Jeruk (25), Apel (18), Pisang (14).", "Mengurutkan dari yang tersedikit")

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S2, "Tabel: Kelas A (28), Kelas B (24). Berapa selisih siswa kedua kelas?", ["4 siswa", "3 siswa", "5 siswa", "2 siswa"], "A", "28 - 24 = 4 siswa.", verifikasi={"ekspresi": "28 - 24", "hasil": "4"})
mc("c3", "mudah", T, Pr, S4, "Data pemilih: Rani (18), Doni (12). Rani menang dengan selisih suara ....", ["6 suara", "5 suara", "7 suara", "4 suara"], "A", "18 - 12 = 6 suara.", verifikasi={"ekspresi": "18 - 12", "hasil": "6"})
tf("c3", "sedang", T, Pr, S3, "Urutan dari terkecil untuk angka 30, 15, 22 adalah 15, 22, 30.", "Benar", "Urutan terkecil: 15, 22, 30.")
mc("c3", "sedang", T, Pr, S2, "Tabel ternak: Sapi 35, Kambing 22. Berapa ekor sapi lebih banyak dari kambing?", ["13 ekor", "12 ekor", "14 ekor", "11 ekor"], "A", "35 - 22 = 13 ekor.", verifikasi={"ekspresi": "35 - 22", "hasil": "13"})
tf("c3", "sedang", T, Pr, S1, "Bila angka pada tabel sama besar, maka selisihnya adalah nol.", "Benar", "Dua angka yang sama memiliki selisih 0.")
sa("c3", "sedang", T, Pr, S2, "Tabel: Penggaris 19, Pensil 12. Selisih kedua barang adalah ... buah.", "7", "19 - 12 = 7 buah.", verifikasi={"ekspresi": "19 - 12", "hasil": "7"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S2, "Tabel tabungan: Dayu (Rp30.000), Udin (Rp18.000). Selisih tabungan mereka?", ["Rp12.000", "Rp10.000", "Rp14.000", "Rp15.000"], "A", "30.000 - 18.000 = Rp12.000.")
mc("c3", "sedang", X, Pr, S3, "Tabel nilai: Matematika (88), IPA (76), IPS (82). Urutan dari nilai terendah?", ["IPA, IPS, Matematika", "Matematika, IPS, IPA", "IPS, IPA, Matematika", "IPA, Matematika, IPS"], "A", "Terendah ke tertinggi: 76 (IPA), 82 (IPS), 88 (Matematika).")
tf("c3", "sedang", X, Pr, S4, "Dari tabel penjualan, barang paling laris adalah barang berangka terkecil.", "Salah", "Barang paling laris memiliki angka penjualan terbesar.")
sa("c3", "sedang", X, Pr, S2, "Tabel: Topi merah 24, Topi biru 15. Selisih topi adalah ... buah.", "9", "24 - 15 = 9 buah.", verifikasi={"ekspresi": "24 - 15", "hasil": "9"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Tabel buah di pasar: Salak 45 kg, Duku 32 kg. Selisih berat kedua buah?", ["13 kg", "12 kg", "14 kg", "15 kg"], "A", "45 - 32 = 13 kg.", verifikasi={"ekspresi": "45 - 32", "hasil": "13"})
mc("c3", "sedang", K, Pr, S3, "Empat baris data: A (14), B (28), C (19), D (31). Selisih tertinggi dan terendah?", ["17", "16", "18", "15"], "A", "31 - 14 = 17.", verifikasi={"ekspresi": "31 - 14", "hasil": "17"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Jika tabel menunjukkan data olahraga, mengapa penting mengetahui peminat paling sedikit?", ["agar guru bisa memberi perhatian dan motivasi lebih untuk olahraga tersebut", "untuk membuang bolanya", "agar lapangannya ditutup", "tidak penting"], "A", "Mengetahui peminat sedikit membantu evaluasi dan bimbingan.")
mc("c4", "sedang", T, Kn, S2, "Tabel hobi: Lukis (14), Musik (19), Tari (11). Berapa selisih Musik dan Tari?", ["8 orang", "7 orang", "9 orang", "6 orang"], "A", "19 - 11 = 8 orang.", verifikasi={"ekspresi": "19 - 11", "hasil": "8"})
tf("c4", "sedang", T, Kn, S3, "Mengubah urutan baris tabel akan mengubah jumlah total data pada baris bawah.", "Salah", "Total penjumlahan data tetap sama meski letak baris ditukar.")
tf("c4", "sedang", T, Kn, S4, "Dari tabel perpustakaan, buku yang sering dipinjam adalah buku paling diminati.", "Benar", "Frekuensi peminjaman tinggi menunjukkan minat yang tinggi.")
sa("c4", "sedang", T, Kn, S2, "Tabel: Sepeda motor 38, Sepeda 19. Selisih kendaraan adalah ... buah.", "19", "38 - 19 = 19 buah.", verifikasi={"ekspresi": "38 - 19", "hasil": "19"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S2, "Tabel nilai: Lani (92), Siti (85). Berapa poin Siti harus mengejar Lani?", ["7 poin", "6 poin", "8 poin", "5 poin"], "A", "92 - 85 = 7 poin.", verifikasi={"ekspresi": "92 - 85", "hasil": "7"})
mc("c4", "sedang", X, Kn, S3, "Tabel panen: Jagung 40 kg, Padi 65 kg, Kedelai 35 kg. Barang urutan paling sedikit?", ["kedelai", "jagung", "padi", "semua sama"], "A", "Kedelai (35 kg) adalah yang paling sedikit.")
tf("c4", "sedang", X, Kn, S1, "Pernyataan 'apel lebih banyak 5 buah dari jeruk' berarti apel lebih sedikit.", "Salah", "Apel lebih banyak, bukan lebih sedikit daripada jeruk.")
mc("c4", "sulit", X, Me, S4, "Tabel: Kaos putih (34), Kaos hitam (26). Jika 5 kaos putih terjual, selisih sekarang?", ["3 potong", "8 potong", "5 potong", "2 potong"], "A", "Kaos putih sekarang: 34 - 5 = 29. Selisih = 29 - 26 = 3 potong.", verifikasi={"ekspresi": "(34 - 5) - 26", "hasil": "3"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Tabel pengunjung: Sabtu 48 orang, Minggu 75 orang. Berapa kenaikan pengunjung?", ["27 orang", "25 orang", "29 orang", "30 orang"], "A", "75 - 48 = 27 orang.", verifikasi={"ekspresi": "75 - 48", "hasil": "27"})
mc("c4", "sulit", K, Me, S3, "Empat tim mengumpulkan poin: Tim A (45), B (60), C (38), D (52). Juara kedua adalah ....", ["Tim D", "Tim B", "Tim A", "Tim C"], "A", "Peringkat: B (60), D (52), A (45), C (38). Juara kedua = Tim D.")
tf("c4", "sulit", K, Me, S4, "Jika selisih data A dan B adalah 0, maka A dan B memiliki nilai sama banyak.", "Benar", "Selisih 0 membuktikan kedua nilai sama besar.")
mc("c4", "sulit", K, Me, S4, "Tabel uang kas: Januari Rp50.000, Februari Rp75.000. Berapa persen selisihnya?", ["Rp25.000", "Rp20.000", "Rp30.000", "Rp15.000"], "A", "75.000 - 50.000 = Rp25.000.")

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Tabel menunjukkan pengunjung museum hari Senin 10 orang, hari Minggu 95 orang. Mengapa?", ["karena hari Minggu adalah hari libur sekolah dan keluarga berwisata", "karena hari Minggu museum tutup", "hanya kebetulan", "agar museum kosong"], "A", "Hari libur meningkatkan minat kunjungan wisata keluarga.")
mc("c5", "sedang", T, Me, S2, "Tabel: Bibit jambu 42, Bibit mangga 58. Berapa bibit jambu harus ditambah agar sama?", ["16 bibit", "14 bibit", "18 bibit", "15 bibit"], "A", "58 - 42 = 16 bibit.", verifikasi={"ekspresi": "58 - 42", "hasil": "16"})
mc("c5", "sedang", T, Me, S3, "Tabel: Calon A (35 suara), Calon B (48 suara), Calon C (25 suara). Siapa terpilih ketua?", ["Calon B", "Calon A", "Calon C", "semua terpilih"], "A", "Calon B meraih suara terbanyak yaitu 48 suara.")
mc("c5", "sulit", T, Me, S4, "Tabungan: Edo 45 ribu, Beni 60 ribu. Berapa uang Beni dibagi agar sama?", ["Rp7.500", "Rp15.000", "Rp10.000", "Rp5.000"], "A", "Selisih 15.000. Dibagi 2 = Rp7.500.")

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Tabel panen: Pak Budi 85 kg, Pak Tono 68 kg. Berapa selisih panen padi keduanya?", ["17 kg", "15 kg", "19 kg", "16 kg"], "A", "85 - 68 = 17 kg.", verifikasi={"ekspresi": "85 - 68", "hasil": "17"})
mc("c5", "sulit", K, Me, S3, "Peringkat nilai 4 siswa: Euis 95, Fitri 88, Galih 92, Hendra 85. Siapakah juara 3?", ["Fitri", "Euis", "Galih", "Hendra"], "A", "Urutan: 1 (Euis 95), 2 (Galih 92), 3 (Fitri 88), 4 (Hendra 85). Juara 3 = Fitri.")

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Jika tabel menu kantin menunjukkan nasi goreng terjual 50 piring, bubur 10 piring?", ["kantin sebaiknya memasak lebih banyak nasi goreng besok pagi", "kantin berhenti jualan", "bubur dimasak lebih banyak", "semua menu dihapus"], "A", "Keputusan logis adalah menambah porsi makanan yang paling diminati pembeli.")
mc("c6", "sulit", K, Me, S4, "Evaluasi tabel kehadiran: Kelas 2A hadir 98%, Kelas 2B 90%. Saran terbaik untuk 2B?", ["mencari penyebab ketidakhadiran siswa dan memberi motivasi semangat sekolah", "menghukum kelas 2B", "menutup kelas 2B", "membiarkan saja"], "A", "Mencari akar masalah dan memotivasi siswa adalah solusi edukatif.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S2, "Tabel: Stok A (65), B (48), C (82). Berapa selisih stok tertinggi dan terendah?", ["34 barang", "32 barang", "36 barang", "30 barang"], "A", "Tertinggi C (82), terendah B (48). Selisih = 82 - 48 = 34 barang.", verifikasi={"ekspresi": "82 - 48", "hasil": "34"})
mc("c6", "sulit", P, Me, S4, "Tabungan: Jan (45 rb), Feb (55 rb), Mar (70 rb). Kenaikan Jan ke Mar?", ["25 rb", "20 rb", "30 rb", "15 rb"], "A", "70 - 45 = 25 rb.", verifikasi={"ekspresi": "70 - 45", "hasil": "25"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab79_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab79.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
