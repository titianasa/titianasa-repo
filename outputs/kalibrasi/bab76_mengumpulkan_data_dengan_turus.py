#!/usr/bin/env python3
"""
Generator dan validator Bab 76 Matematika Kelas 2 SD:
"Mengumpulkan Data dengan Turus" (Fase A)
bab_id: b6da4b99-f132-41bf-b58b-ed34ffbfa215
article_id: 4d9e0272-f797-4fcf-ae0d-f972f6b21169
quiz_id: 77a3fdc9-8d5e-485b-83cf-7d93ff8e97f5
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "u1w2y3a4c501"  # Mengenal Data Sederhana
S2 = "v2x3z4b5d602"  # Mengenal Tanda Turus
S3 = "w3y4a5c6e703"  # Aturan Ikat Lima pada Turus
S4 = "x4z5b6d7f804"  # Praktik Menghitung dengan Turus

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Data adalah kumpulan informasi nyata.
Misalnya warna kesukaan teman sekelas.
Bisa juga buah kesukaan siswa.
Bila hanya diingat bisa lupa.
Maka data harus dicatat rapi.
Mencatat data membuat kita tahu.
Mana yang paling banyak disukai.
Mari belajar mencatat data bersama!

:::definition
title: Data
Catatan keterangan atau informasi yang diperoleh dari hasil pengamatan.
:::"""

s2_content = """Bagaimana cara mencatat yang cepat?
Kita bisa menggunakan tanda turus.
Turus berupa garis lurus tegak.
Satu benda diwakili satu garis.
Bila ada 3 apel merah.
Kita buat 3 garis tegak.
Mencatat dengan turus sangat mudah.
Kita tidak perlu menulis angka panjang!

:::steps
title: Menulis Garis Turus
1. Lihat satu benda yang dihitung.
2. Buat satu garis lurus tegak (|).
3. Lanjutkan untuk benda berikutnya.
:::"""

s3_content = """Ada aturan khusus kelipatan lima.
Empat garis tegak dibuat berdampingan.
Garis kelima dibuat mencoret miring.
Coretan miring mengikat empat garis.
Satu ikat turus bernilai 5.
Menghitung turus menjadi sangat cepat.
Kita cukup berhitung loncat lima:
5, 10, 15, dan seterusnya!

:::common_trap
title: Mengira Satu Ikat Berisi 4 Garis
Satu ikat berisi lima hitungan.
Empat garis tegak ditambah satu miring.
Empat tambah satu sama dengan lima!
:::"""

s4_content = """Mari praktik menghitung benda nyata.
Hitung pensil warna di kotak.
Buat satu garis tiap pensil.
Bila terkumpul dua ikat penuh.
Ditambah tiga garis tegak lepas.
Artinya ada 5 + 5 + 3.
Totalnya ada tiga belas pensil.
Mencatat dengan turus tidak terlewat!

:::callout
variant: summary
title: Ringkasan
text: Turus adalah garis lurus. Tiap 5 garis diikat miring.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Data Sederhana",
        "minutes": 6,
        "goal": "Siswa mengenal konsep data sebagai catatan informasi faktual.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengenal Tanda Turus",
        "minutes": 6,
        "goal": "Siswa memahami simbol turus (|) sebagai alat pencatat hitungan satu per satu.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Aturan Ikat Lima pada Turus",
        "minutes": 6,
        "goal": "Siswa memahami aturan mencoret miring pada hitungan kelima sebagai ikatan 5.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Praktik Menghitung dengan Turus",
        "minutes": 6,
        "goal": "Siswa mampu menghitung total benda nyata dari representasi ikatan turus.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengumpulkan Data dengan Turus",
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
# 2. DEFINISI BANK 50 SOAL BAB 76
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
mc("c1", "mudah", D, F, S1, "Catatan informasi yang dikumpulkan dari pengamatan dinamakan ....", ["data", "cerita", "gambar", "lagu"], "A", "Catatan informasi dinamakan data.")
tf("c1", "mudah", D, F, S2, "Satu garis tegak turus mewakili hitungan sebanyak satu benda.", "Benar", "Satu garis turus bernilai 1 benda.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Bagaimanakah bentuk dasar dari tanda turus?", ["garis lurus tegak", "lingkaran bulat", "tanda silang", "segitiga lancip"], "A", "Bentuk turus berupa garis lurus tegak.")
mc("c1", "mudah", T, F, S3, "Berapakah nilai hitungan dari satu ikat turus lengkap?", ["5 hitungan", "4 hitungan", "6 hitungan", "10 hitungan"], "A", "Satu ikat turus bernilai 5.", verifikasi={"ekspresi": "4 + 1", "hasil": "5"})
sa("c1", "mudah", T, F, S3, "Satu ikat turus terdiri dari ... garis tegak dan 1 garis miring.", "4", "4 tegak + 1 miring = 5.", verifikasi={"ekspresi": "5 - 1", "hasil": "4"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Garis kelima pada ikatan turus digambar dengan cara ....", ["mencoret miring menyilang", "membuat lingkaran", "membuat titik tebal", "dihapus kembali"], "A", "Garis kelima dicoret miring menyilang.")
tf("c2", "mudah", D, Kn, S4, "Menghitung data dengan turus memudahkan kita berhitung loncat lima.", "Benar", "Tiap ikat bernilai 5, sehingga bisa loncat lima.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S3, "Bila ada 4 garis tegak dan 1 garis coret miring, nilainya adalah ....", ["5", "4", "6", "3"], "A", "4 + 1 = 5.", "Hanya menghitung 4 garis tegak", verifikasi={"ekspresi": "4 + 1", "hasil": "5"})
mc("c2", "mudah", R, Kn, S2, "Untuk mencatat 3 ekor kucing, berapa garis turus tegak yang dibuat?", ["3 garis", "2 garis", "4 garis", "5 garis"], "A", "Dibuat 3 garis tegak.", "Mengira butuh garis miring untuk 3 garis", verifikasi={"ekspresi": "1 * 3", "hasil": "3"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Contoh data yang dapat dicatat di kelas adalah ....", ["warna kesukaan teman sekelas", "nama matahari", "warna langit malam", "suara petir"], "A", "Warna kesukaan teman adalah data kelas.")
mc("c2", "mudah", T, Kn, S4, "Ada 2 ikat turus penuh. Berapakah jumlah nilai bendanya?", ["10 benda", "8 benda", "12 benda", "15 benda"], "A", "2 x 5 = 10 benda.", verifikasi={"ekspresi": "2 * 5", "hasil": "10"})
tf("c2", "mudah", T, Kn, S3, "Garis coret miring turus dibuat setelah ada lima garis tegak.", "Salah", "Coret miring adalah garis kelima (setelah 4 garis tegak).")
sa("c2", "mudah", T, Kn, S2, "Sebanyak 7 buku dicatat turus: 1 ikat lima dan ... garis tegak.", "2", "7 = 5 + 2.", verifikasi={"ekspresi": "7 - 5", "hasil": "2"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Berapakah nilai dari 3 ikat turus penuh?", ["15", "12", "18", "10"], "A", "3 x 5 = 15.", "Menghitung 3 ikat sebagai 12", verifikasi={"ekspresi": "3 * 5", "hasil": "15"})
mc("c3", "sedang", R, Pr, S4, "Terdapat 1 ikat turus penuh dan 4 garis tegak. Berapakah totalnya?", ["9", "8", "10", "7"], "A", "5 + 4 = 9.", "Mengira bernilai 8", verifikasi={"ekspresi": "5 + 4", "hasil": "9"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Siti mencatat 5 siswa suka apel dan 5 suka jeruk. Berapa total siswa?", ["10 siswa", "8 siswa", "12 siswa", "15 siswa"], "A", "5 + 5 = 10 siswa.", verifikasi={"ekspresi": "5 + 5", "hasil": "10"})
mc("c3", "mudah", T, Pr, S4, "Ada 2 ikat turus dan 3 garis tegak. Berapakah total nilainya?", ["13", "11", "15", "12"], "A", "(2 x 5) + 3 = 10 + 3 = 13.", verifikasi={"ekspresi": "(2 * 5) + 3", "hasil": "13"})
tf("c3", "sedang", T, Pr, S2, "Untuk menuliskan bilangan 8, kita butuh 1 ikat lima dan 3 garis tegak.", "Benar", "8 = 5 + 3.")
mc("c3", "sedang", T, Pr, S3, "Berapakah jumlah ikat penuh untuk menuliskan bilangan 20 dengan turus?", ["4 ikat", "3 ikat", "5 ikat", "6 ikat"], "A", "20 : 5 = 4 ikat.", verifikasi={"ekspresi": "20 / 5", "hasil": "4"})
tf("c3", "sedang", T, Pr, S1, "Mencatat data hanya boleh menggunakan ingatan tanpa perlu ditulis.", "Salah", "Ingatan manusia terbatas sehingga data wajib dicatat.")
sa("c3", "sedang", T, Pr, S4, "Ada 4 ikat turus penuh. Nilai seluruhnya adalah ...", "20", "4 x 5 = 20.", verifikasi={"ekspresi": "4 * 5", "hasil": "20"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S2, "Berapakah garis tegak lepas yang tersisa pada penulisan angka 14?", ["4 garis", "3 garis", "2 garis", "1 garis"], "A", "14 = (2 x 5) + 4 = sisa 4 garis.", verifikasi={"ekspresi": "14 - 10", "hasil": "4"})
mc("c3", "sedang", X, Pr, S3, "Ali menulis 6 ikat turus penuh. Berapakah total data Ali?", ["30 data", "25 data", "35 data", "24 data"], "A", "6 x 5 = 30 data.", verifikasi={"ekspresi": "6 * 5", "hasil": "30"})
tf("c3", "sedang", X, Pr, S4, "Tiga ikat turus penuh dan 2 garis lepas sama nilainya dengan 17.", "Benar", "(3 x 5) + 2 = 15 + 2 = 17.")
sa("c3", "sedang", X, Pr, S1, "Data 8 mangga dan 7 pisang. Total buah adalah ... buah.", "15", "8 + 7 = 15 buah.", verifikasi={"ekspresi": "8 + 7", "hasil": "15"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Berapa banyak ikatan lima dan sisa garis untuk bilangan 23?", ["4 ikat dan 3 garis", "3 ikat dan 8 garis", "5 ikat dan 0 garis", "4 ikat dan 1 garis"], "A", "23 = (4 x 5) + 3.")
mc("c3", "sedang", K, Pr, S4, "Kumpulan turus: 3 ikat penuh dan 1 garis lepas. Nilainya adalah ....", ["16", "15", "14", "18"], "A", "(3 x 5) + 1 = 15 + 1 = 16.", verifikasi={"ekspresi": "(3 * 5) + 1", "hasil": "16"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S1
mc("c4", "sedang", T, Kn, S1, "Mengapa tanda turus lebih disukai saat menghitung orang lewat secara langsung?", ["karena kita cukup menambah satu garis setiap ada orang lewat", "karena garis turus berwarna warni", "karena tidak perlu kertas", "agar orang tidak lewat"], "A", "Turus dicatat seketika tanpa perlu menghitung ulang dari awal.")
mc("c4", "sedang", T, Kn, S2, "Apa yang terjadi jika kita tidak mengikat turus pada kelipatan 5?", ["kita akan sulit dan lama saat menghitung kembali jumlah totalnya", "turus akan robek", "angka jadi salah", "kertas jadi penuh"], "A", "Garis tegak berjejer tanpa ikatan sangat sulit dihitung cepat.")
tf("c4", "sedang", T, Kn, S3, "Dalam 25 data, terdapat tepat empat ikatan turus penuh.", "Salah", "25 data terdiri dari 5 ikatan turus penuh, bukan 4.")
tf("c4", "sedang", T, Kn, S4, "Dua kelompok turus masing-masing 2 ikat dan 4 garis lepas berjumlah 26.", "Salah", "Tiap kelompok: 14. 14 + 14 = 28, bukan 26.")
sa("c4", "sedang", T, Kn, S3, "Untuk menyajikan data 35 siswa, dibutuhkan ... ikat turus penuh.", "7", "35 : 5 = 7 ikat.", verifikasi={"ekspresi": "35 / 5", "hasil": "7"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S2, "Budi menulis turus: ||||/ ||||/ |||. Manakah bilangan yang benar?", ["13", "12", "14", "15"], "A", "5 + 5 + 3 = 13.", verifikasi={"ekspresi": "5 + 5 + 3", "hasil": "13"})
mc("c4", "sedang", X, Kn, S3, "Selisih nilai antara 5 ikat turus dan 3 ikat turus adalah ....", ["10", "5", "15", "8"], "A", "(5 x 5) - (3 x 5) = 25 - 15 = 10.", verifikasi={"ekspresi": "(5 * 5) - (3 * 5)", "hasil": "10"})
tf("c4", "sedang", X, Kn, S1, "Hasil sensus pemilih ketua kelas paling praktis dihitung dengan turus di papan.", "Benar", "Turus di papan memudahkan guru dan siswa melihat suara langsung.")
mc("c4", "sulit", X, Me, S4, "Data buku: Matematika 4 ikat, Bahasa 3 ikat 2 garis. Berapa selisihnya?", ["3 buku", "4 buku", "5 buku", "2 buku"], "A", "Matematika: 20. Bahasa: 17. Selisih = 20 - 17 = 3 buku.", verifikasi={"ekspresi": "(4 * 5) - ((3 * 5) + 2)", "hasil": "3"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Jika ada 22 sepeda yang lewat di jalan raya, bagaimana turus dicatat?", ["4 ikat lima dan 2 garis lepas", "3 ikat lima dan 7 garis", "5 ikat lima", "2 ikat lima dan 2 garis"], "A", "22 = (4 x 5) + 2.")
mc("c4", "sulit", K, Me, S2, "Total garis yang digambar (tegak + miring) untuk angka 18 adalah ....", ["18 garis", "15 garis", "20 garis", "14 garis"], "A", "Tiap 1 hitungan = 1 garis, jadi total ada 18 garis.", verifikasi={"ekspresi": "18 * 1", "hasil": "18"})
tf("c4", "sulit", K, Me, S3, "Garis coretan miring pada ikatan turus dihitung sebagai 2 buah garis.", "Salah", "Garis coret miring dihitung tepat 1 hitungan (hitungan ke-5).")
mc("c4", "sulit", K, Me, S4, "Tersedia 38 kelereng. Berapa ikat lima dan sisa garis turusnya?", ["7 ikat dan 3 garis", "6 ikat dan 8 garis", "8 ikat dan 0 garis", "5 ikat dan 3 garis"], "A", "38 = (7 x 5) + 3.")

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Dalam pemilihan ketua kelas ada 3 calon. Suara tercatat: A (12), B (15), C (8). Pemenangnya?", ["Calon B", "Calon A", "Calon C", "semua sama"], "A", "Calon B mendapat suara terbanyak yaitu 15 suara.")
mc("c5", "sedang", T, Me, S2, "Bandingkan turus A (4 ikat) dan turus B (3 ikat + 4 garis). Siapa lebih banyak?", ["Turus A lebih banyak 1 angka", "Turus B lebih banyak", "keduanya sama banyak", "tidak dapat dihitung"], "A", "Turus A = 20, Turus B = 19. Selisih = 1 angka.", verifikasi={"ekspresi": "(4 * 5) - ((3 * 5) + 4)", "hasil": "1"})
mc("c5", "sedang", T, Me, S3, "Bila ingin mencatat 45 orang siswa, berapa garis miring pengikat yang digambar?", ["9 garis miring", "8 garis miring", "10 garis miring", "7 garis miring"], "A", "45 : 5 = 9 ikat, artinya ada 9 garis miring.", verifikasi={"ekspresi": "45 / 5", "hasil": "9"})
mc("c5", "sulit", T, Me, S4, "Pak Tani mencatat ternak: ayam 6 ikat, bebek 4 ikat 3 garis. Total ternak?", ["53 ekor", "50 ekor", "55 ekor", "48 ekor"], "A", "(6 x 5) + (4 x 5 + 3) = 30 + 23 = 53 ekor.", verifikasi={"ekspresi": "(6 * 5) + ((4 * 5) + 3)", "hasil": "53"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Di perpustakaan ada 48 buku cerita. Berapa ikat lima dan sisa lepasnya?", ["9 ikat dan 3 garis", "8 ikat dan 8 garis", "10 ikat dan 0 garis", "7 ikat dan 4 garis"], "A", "48 = (9 x 5) + 3.")
mc("c5", "sulit", K, Me, S4, "Ada 2 keranjang buah: A (5 ikat 2 garis), B (4 ikat 4 garis). Selisih buahnya?", ["3 buah", "2 buah", "4 buah", "5 buah"], "A", "A = 27, B = 24. Selisih = 27 - 24 = 3 buah.", verifikasi={"ekspresi": "((5 * 5) + 2) - ((4 * 5) + 4)", "hasil": "3"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Rancanglah cara mencatat kendaraan lewat di gerbang sekolah selama 15 menit!", ["siapkan lembar turus berkolom: motor, mobil, sepeda, lalu beri garis tiap lewat", "ingat di kepala saja", "teriak setiap ada mobil", "tutup gerbang sekolah"], "A", "Tabel turus terbagi kolom jenis kendaraan adalah metode paling sistematis.")
mc("c6", "sulit", K, Me, S3, "Mengapa pola ikat lima lebih dipilih daripada mengikat tiap sepuluh garis?", ["karena mata kita mudah mengenali kelompok 5 tanpa pusing menghitung satu-satu", "karena angka 10 jelek", "hanya kebetulan", "agar kertas cepat habis"], "A", "Kelompok 5 secara visual pas dan cepat dikenali oleh persepsi mata manusia.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S2, "Hitung total data: 7 ikat lima + 8 ikat lima + 4 garis lepas!", ["79 data", "75 data", "80 data", "74 data"], "A", "(7 x 5) + (8 x 5) + 4 = 35 + 40 + 4 = 79 data.", verifikasi={"ekspresi": "(7 * 5) + (8 * 5) + 4", "hasil": "79"})
mc("c6", "sulit", P, Me, S4, "Panen: apel 8 ikat, jeruk 6 ikat, mangga 5 ikat. Total buah?", ["95 buah", "90 buah", "85 buah", "100 buah"], "A", "(8 + 6 + 5) x 5 = 19 x 5 = 95 buah.", verifikasi={"ekspresi": "(8 + 6 + 5) * 5", "hasil": "95"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab76_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab76.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
