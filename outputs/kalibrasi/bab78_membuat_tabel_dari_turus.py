#!/usr/bin/env python3
"""
Generator dan validator Bab 78 Matematika Kelas 2 SD:
"Membuat Tabel dari Turus" (Fase A)
bab_id: ae3fa615-28c8-40fd-9621-0993bfe0d286
article_id: bb72b7f6-577b-423b-96df-a5dbdc5a2188
quiz_id: b3681947-3acf-4d29-9de3-8de7899c4a6b
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "w1y2a3c4e501"  # Dari Tanda Turus ke Angka
S2 = "x2z3b4d5f602"  # Menyiapkan Format Tabel Tiga Kolom
S3 = "y3a4c5e6g703"  # Memasukkan Data ke Tabel
S4 = "z4b5d6f7h804"  # Memeriksa dan Menjumlahkan Total

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Turus diubah menjadi angka bilangan.
Caranya dengan menghitung tanda turus.
Tiap satu ikat bernilai lima.
Hitung loncat lima terlebih dahulu:
5, 10, 15, dan seterusnya.
Lalu tambahkan sisa garis tegak.
Misal dua ikat tambah empat garis.
5 + 5 + 4 = 14.
Angka 14 siap dituliskan!

:::definition
title: Mengubah Turus ke Angka
Proses menghitung nilai kumpulan turus menjadi lambang bilangan biasa.
:::"""

s2_content = """Buatlah tabel yang memuat tiga kolom.
Kolom pertama memuat nama benda.
Kolom kedua memuat coretan turus.
Kolom ketiga memuat lambang angka.
Beri garis pemisah yang rapi.
Gunakan penggaris saat menggambar kolom.
Tabel siap diisi data!

:::steps
title: Kolom Tabel Lengkap
1. Kolom 1: Nama benda atau kategori.
2. Kolom 2: Tanda turus garis pencatat.
3. Kolom 3: Banyak benda dalam angka.
:::"""

s3_content = """Salin data turus ke tabel.
Tulis nama benda pada baris.
Gambar turus di kolom kedua.
Tulis angka di kolom ketiga.
Pastikan keduanya sebaris lurus.
Jangan sampai angka tertukar baris.
Semua baris diisi dengan teliti.
Tabel menjadi rapi dan jelas!

:::common_trap
title: Salah Menghitung Jumlah Garis
Hitung garis turus dengan sabar.
Satu ikat adalah lima hitungan.
Jangan sampai salah menuliskan angkanya!
:::"""

s4_content = """Langkah terakhir adalah menulis total.
Buat baris jumlah di bawah.
Jumlahkan semua angka kolom ketiga.
Periksa kembali hitungan garis turus.
Apakah total angka sudah cocok?
Bila sudah cocok, pekerjaan selesai.
Data tersaji sangat sempurna!

:::callout
variant: summary
title: Ringkasan
text: Hitung turus jadi angka. Masukkan ke baris tabel yang lurus.
:::"""

sections = [
    {
        "id": S1,
        "title": "Dari Tanda Turus ke Angka",
        "minutes": 6,
        "goal": "Siswa mampu mengonversi kumpulan tanda turus menjadi lambang bilangan angka.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Menyiapkan Format Tabel Tiga Kolom",
        "minutes": 6,
        "goal": "Siswa memahami struktur tabel data tiga kolom (Nama, Turus, Jumlah Angka).",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Memasukkan Data ke Tabel",
        "minutes": 6,
        "goal": "Siswa mampu memindahkan data turus dan angka padanannya ke dalam baris tabel secara tepat.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Memeriksa dan Menjumlahkan Total",
        "minutes": 6,
        "goal": "Siswa mampu memeriksa kebenaran data dan menghitung baris total keseluruhan pada tabel.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membuat Tabel dari Turus",
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
# 2. DEFINISI BANK 50 SOAL BAB 78
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
mc("c1", "mudah", D, F, S1, "Lambang bilangan angka untuk dua ikat turus penuh adalah ....", ["10", "8", "12", "15"], "A", "2 x 5 = 10.", verifikasi={"ekspresi": "2 * 5", "hasil": "10"})
tf("c1", "mudah", D, F, S2, "Tabel data dari turus biasanya memuat kolom nama, turus, dan angka.", "Benar", "Tiga kolom tersebut adalah format standar tabel turus.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Pada tabel lengkap, kolom turus diletakkan di antara nama benda dan ....", ["banyaknya dalam angka", "judul tabel", "nomor halaman", "warna kertas"], "A", "Kolom turus diletakkan di tengah antara nama dan angka.")
mc("c1", "mudah", T, F, S1, "Berapakah angka yang tepat untuk 1 ikat turus dan 3 garis tegak?", ["8", "7", "9", "6"], "A", "5 + 3 = 8.", verifikasi={"ekspresi": "5 + 3", "hasil": "8"})
sa("c1", "mudah", T, F, S1, "Nilai angka untuk 3 ikat turus penuh adalah ...", "15", "3 x 5 = 15.", verifikasi={"ekspresi": "3 * 5", "hasil": "15"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Jika baris Jeruk memuat 2 ikat turus, angka di kolom jumlah adalah ....", ["10", "8", "12", "15"], "A", "2 ikat bernilai 10.", verifikasi={"ekspresi": "2 * 5", "hasil": "10"})
tf("c2", "mudah", D, Kn, S3, "Angka pada kolom jumlah boleh ditulis sembarang tanpa mencocokkan turus.", "Salah", "Angka wajib cocok persis dengan nilai turus.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Turus: 2 ikat penuh dan 1 garis tegak. Angka yang sesuai adalah ....", ["11", "9", "10", "12"], "A", "10 + 1 = 11.", "Mengira 2 ikat adalah 8", verifikasi={"ekspresi": "10 + 1", "hasil": "11"})
mc("c2", "mudah", R, Kn, S3, "Baris Pensil memuat 1 ikat dan 4 garis. Angka yang ditulis adalah ....", ["9", "8", "10", "7"], "A", "5 + 4 = 9.", "Lupa menghitung garis miring pengikat", verifikasi={"ekspresi": "5 + 4", "hasil": "9"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S2, "Apa manfaat menuliskan angka di samping kolom turus pada tabel?", ["agar pembaca langsung tahu jumlahnya tanpa perlu menghitung garis lagi", "agar tabelnya ramai", "supaya kertasnya penuh", "hanya hiasan"], "A", "Kolom angka mempermudah membaca jumlah secara instan.")
mc("c2", "mudah", T, Kn, S3, "Baris Mangga memuat 3 ikat dan 2 garis. Angka jumlahnya adalah ....", ["17", "15", "16", "18"], "A", "15 + 2 = 17.", verifikasi={"ekspresi": "15 + 2", "hasil": "17"})
tf("c2", "mudah", T, Kn, S4, "Baris 'Jumlah' diletakkan di bagian paling bawah tabel data.", "Benar", "Baris jumlah diletakkan di baris terakhir.")
sa("c2", "mudah", T, Kn, S1, "Empat ikat turus penuh sama dengan angka ...", "20", "4 x 5 = 20.", verifikasi={"ekspresi": "4 * 5", "hasil": "20"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Ubahlah ke angka: 3 ikat turus dan 4 garis lepas!", ["19", "18", "17", "20"], "A", "15 + 4 = 19.", "Menghitung 3 ikat bernilai 12", verifikasi={"ekspresi": "15 + 4", "hasil": "19"})
mc("c3", "sedang", R, Pr, S4, "Tabel: Apel 12, Jeruk 8. Berapa angka pada baris jumlah total?", ["20", "18", "22", "19"], "A", "12 + 8 = 20.", "Salah menjumlahkan 12 dan 8", verifikasi={"ekspresi": "12 + 8", "hasil": "20"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berapakah angka dari 2 ikat turus dan 2 garis tegak?", ["12", "10", "14", "11"], "A", "10 + 2 = 12.", verifikasi={"ekspresi": "10 + 2", "hasil": "12"})
mc("c3", "mudah", T, Pr, S3, "Data: Sepeda 7 turus, Becak 5 turus. Total kendaraan adalah ....", ["12 kendaraan", "10 kendaraan", "14 kendaraan", "11 kendaraan"], "A", "7 + 5 = 12 kendaraan.", verifikasi={"ekspresi": "7 + 5", "hasil": "12"})
tf("c3", "sedang", T, Pr, S2, "Tanda turus ditulis pada kolom judul paling atas di luar kotak tabel.", "Salah", "Tanda turus ditulis di dalam kolom kedua pada badan tabel.")
mc("c3", "sedang", T, Pr, S4, "Tabel 3 baris: Merah 14, Biru 11, Hijau 5. Total baris jumlah?", ["30", "28", "32", "29"], "A", "14 + 11 + 5 = 30.", verifikasi={"ekspresi": "14 + 11 + 5", "hasil": "30"})
tf("c3", "sedang", T, Pr, S3, "Satu baris tabel boleh memuat nama apel tetapi turusnya mangga.", "Salah", "Turus harus sesuai dengan nama benda pada baris tersebut.")
sa("c3", "sedang", T, Pr, S1, "Turus 5 ikat penuh bernilai angka ...", "25", "5 x 5 = 25.", verifikasi={"ekspresi": "5 * 5", "hasil": "25"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Konversikan ke angka: 4 ikat turus dan 3 garis lepas!", ["23", "21", "24", "22"], "A", "20 + 3 = 23.", verifikasi={"ekspresi": "20 + 3", "hasil": "23"})
mc("c3", "sedang", X, Pr, S3, "Baris Ayam ada 3 ikat dan 1 garis. Angka pada tabel adalah ....", ["16", "15", "17", "14"], "A", "15 + 1 = 16.", verifikasi={"ekspresi": "15 + 1", "hasil": "16"})
tf("c3", "sedang", X, Pr, S1, "Tiga ikat turus dan lima garis lepas sama nilainya dengan 20.", "Benar", "15 + 5 = 20 (bisa dijadikan 4 ikat penuh).")
sa("c3", "sedang", X, Pr, S4, "Tabel: Kelas A (18), Kelas B (14). Total kedua kelas adalah ... siswa.", "32", "18 + 14 = 32 siswa.", verifikasi={"ekspresi": "18 + 14", "hasil": "32"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Nilai angka dari 6 ikat turus penuh adalah ....", ["30", "25", "35", "28"], "A", "6 x 5 = 30.", verifikasi={"ekspresi": "6 * 5", "hasil": "30"})
mc("c3", "sedang", K, Pr, S4, "Tabel buah: Salak (15), Duku (13), Sawo (7). Angka baris total adalah ....", ["35", "33", "37", "34"], "A", "15 + 13 + 7 = 35.", verifikasi={"ekspresi": "15 + 13 + 7", "hasil": "35"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Jika ada 28 siswa, berapa ikat penuh dan sisa garis yang dibuat?", ["5 ikat penuh dan 3 garis", "4 ikat dan 8 garis", "6 ikat penuh", "5 ikat dan 1 garis"], "A", "28 = (5 x 5) + 3.")
mc("c4", "sedang", T, Kn, S2, "Mengapa saat membuat tabel kita perlu menarik garis pemisah kolom yang lurus?", ["agar data tidak bercampur aduk antara nama, turus, dan angka", "supaya kertas tampak gelap", "agar mistar tidak hilang", "hanya kebiasaan"], "A", "Garis lurus memisahkan kategori data dengan jelas dan rapi.")
tf("c4", "sedang", T, Kn, S3, "Jika kolom turus tertera 14 tetapi kolom angka tertulis 15, tabel tersebut keliru.", "Benar", "Ada ketidakcocokan antara turus dan angka.")
tf("c4", "sedang", T, Kn, S4, "Menghitung baris jumlah total tabel boleh menebak tanpa menjumlahkan.", "Salah", "Baris jumlah wajib dihitung tepat secara penjumlahan.")
sa("c4", "sedang", T, Kn, S3, "Baris Kelinci: 4 ikat dan 2 garis. Angka kolom banyak benda adalah ...", "22", "20 + 2 = 22.", verifikasi={"ekspresi": "20 + 2", "hasil": "22"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Manakah pasangan turus dan angka bilangan berikut yang benar?", ["3 ikat dan 2 garis = 17", "2 ikat dan 4 garis = 12", "1 ikat dan 3 garis = 9", "4 ikat = 18"], "A", "(3 x 5) + 2 = 15 + 2 = 17.")
mc("c4", "sedang", X, Kn, S3, "Total tabel adalah 40. Jika 3 baris berjumlah 31, berapakah baris ke-4?", ["9", "8", "10", "7"], "A", "40 - 31 = 9.", verifikasi={"ekspresi": "40 - 31", "hasil": "9"})
tf("c4", "sedang", X, Kn, S2, "Judul tabel wajib ditulis tersembunyi di bawah meja agar aman.", "Salah", "Judul tabel diletakkan di atas agar mudah dibaca semua orang.")
mc("c4", "sulit", X, Me, S4, "Tabel panen: Padi (45 karung), Jagung (35 karung), Kedelai (18 karung). Total karung?", ["98 karung", "95 karung", "100 karung", "96 karung"], "A", "45 + 35 + 18 = 98 karung.", verifikasi={"ekspresi": "45 + 35 + 18", "hasil": "98"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Berapakah jumlah garis lurus (tegak dan miring) untuk membuat data angka 24?", ["24 garis", "20 garis", "22 garis", "25 garis"], "A", "Setiap 1 satuan diwakili 1 goresan garis, total 24 garis.", verifikasi={"ekspresi": "24 * 1", "hasil": "24"})
mc("c4", "sulit", K, Me, S2, "Sebuah tabel memiliki 5 baris data dan 1 baris total. Berapa baris kotak?", ["6 baris", "5 baris", "7 baris", "8 baris"], "A", "5 data + 1 total = 6 baris.", verifikasi={"ekspresi": "5 + 1", "hasil": "6"})
tf("c4", "sulit", K, Me, S3, "Bila ada data nol (tidak ada), kolom turus dikosongkan dan kolom angka ditulis 0.", "Benar", "Data nol berarti tidak ada turus (|) dan angkanya 0.")
mc("c4", "sulit", K, Me, S4, "Tabel: Mawar (2 ikat 4 garis), Melati (3 ikat 1 garis). Berapa selisih batangnya?", ["2 batang", "3 batang", "1 batang", "4 batang"], "A", "Melati = 16, Mawar = 14. Selisih = 16 - 14 = 2 batang.", verifikasi={"ekspresi": "16 - 14", "hasil": "2"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Ani punya data: 36 buku cerita. Ia ingin menyusun turus di tabel. Bentuknya?", ["7 ikat penuh dan 1 garis lepas", "6 ikat dan 6 garis", "8 ikat penuh", "5 ikat dan 11 garis"], "A", "36 = (7 x 5) + 1.")
mc("c5", "sedang", T, Me, S2, "Jika kolom turus dihilangkan dari tabel tiga kolom, apakah tabel masih terbaca?", ["masih bisa terbaca karena sudah ada nama benda dan angka jumlahnya", "tabel langsung hancur", "angka menjadi hilang", "tidak bisa sama sekali"], "A", "Tabel dua kolom (nama dan angka) tetap menyajikan informasi lengkap.")
mc("c5", "sedang", T, Me, S3, "Data: Kucing (15), Kelinci (12), Ikan (18). Berapa selisih hewan terbanyak dan tersedikit?", ["6 ekor", "5 ekor", "7 ekor", "8 ekor"], "A", "Terbanyak Ikan (18), tersedikit Kelinci (12). 18 - 12 = 6 ekor.", verifikasi={"ekspresi": "18 - 12", "hasil": "6"})
mc("c5", "sulit", T, Me, S4, "Tabel pemilih: Calon A (24), Calon B (28), Calon C (18). Berapa total pemilih?", ["70 pemilih", "68 pemilih", "72 pemilih", "66 pemilih"], "A", "24 + 28 + 18 = 70 pemilih.", verifikasi={"ekspresi": "24 + 28 + 18", "hasil": "70"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Di tabel tertulis: Sapi (20), Kambing (15). Selisih turus ikat lima keduanya?", ["1 ikat lima", "2 ikat lima", "3 ikat lima", "0 ikat lima"], "A", "Sapi = 4 ikat, Kambing = 3 ikat. Selisih = 4 - 3 = 1 ikat lima.", verifikasi={"ekspresi": "4 - 3", "hasil": "1"})
mc("c5", "sulit", K, Me, S4, "Tabel barang toko: Buku (42), Pensil (58), Penggaris (20). Berapa total barang?", ["120 buah", "115 buah", "125 buah", "110 buah"], "A", "42 + 58 + 20 = 120 buah.", verifikasi={"ekspresi": "42 + 58 + 20", "hasil": "120"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Langkah tepat setelah selesai menghitung suara pemilihan di papan tulis adalah ....", ["memindahkan hitungan turus papan ke dalam tabel bertuliskan angka rapi", "menghapus papan tanpa mencatat", "merobek kertas", "pulang ke rumah"], "A", "Merekap turus ke dalam tabel formal adalah dokumentasi data yang benar.")
mc("c6", "sulit", K, Me, S4, "Seorang siswa membuat tabel dari turus tetapi totalnya berbeda dengan turus. Solusinya?", ["menghitung ulang garis turus satu per satu dan menjumlahkan ulang angkanya", "mengarang angka baru", "menghapus tabelnya", "menyalahkan teman"], "A", "Verifikasi ulang hitungan turus dan penjumlahan adalah prosedur ilmiah.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Tabel: Ayam (8 ikat), Bebek (6 ikat 2 garis), Angsa (3 ikat 4 garis). Total unggas?", ["91 ekor", "88 ekor", "95 ekor", "86 ekor"], "A", "40 + 32 + 19 = 91 ekor.", verifikasi={"ekspresi": "(8 * 5) + ((6 * 5) + 2) + ((3 * 5) + 4)", "hasil": "91"})
mc("c6", "sulit", P, Me, S4, "Data 4 kelas: 2A (28), 2B (27), 2C (29), 2D (26). Berapa total siswa kelas 2?", ["110 siswa", "108 siswa", "112 siswa", "106 siswa"], "A", "28 + 27 + 29 + 26 = 110 siswa.", verifikasi={"ekspresi": "28 + 27 + 29 + 26", "hasil": "110"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab78_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab78.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
