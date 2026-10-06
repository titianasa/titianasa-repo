#!/usr/bin/env python3
"""
Generator dan validator Bab 35 Matematika Kelas 1 SD:
"Membuat Piktogram Sederhana" (Fase A)
bab_id: c79d512e-6171-4d58-8336-90f6fa91d28d
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "b1c2d34e5f01"  # Menyiapkan Tabel dan Menulis Judul
S2 = "c2d3e45f6a12"  # Memilih Simbol Gambar yang Tepat
S3 = "d3e4f56a7b23"  # Menggambar Simbol dengan Rapi dan Sejajar
S4 = "e4f5a67b8c34"  # Menambahkan Keterangan di Bawah Diagram

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Mari belajar membuat piktogram sendiri.
Langkah pertama adalah menulis judul.
Tulis judul rapi di atas kertas.
Judul memberi tahu isi piktogram.
Lalu buatlah baris nama benda.
Tulis nama apel dan jeruk.
Siapkan tempat menggambar yang bersih.
Sekarang tabel siap kita isi.

:::definition
title: Menyiapkan Piktogram
Membuat piktogram diawali dengan menulis judul dan kolom kategori data.
:::"""

s2_content = """Pilihlah simbol gambar yang mudah.
Jangan memilih gambar terlalu rumit.
Pilihlah bentuk lingkaran atau bintang.
Bisa juga gambar buah kecil.
Semua gambar harus sama bentuknya.
Ukuran tiap gambar juga sama.
Gambar yang seragam tampak rapi.
Semua orang senang melihatnya.

:::steps
title: Langkah Menggambar Simbol
1. Pilih simbol gambar sederhana.
2. Buat ukuran setiap gambar sama besar.
3. Gambar sejajar ke samping dengan rapi.
:::"""

s3_content = """Sekarang kita mulai menggambar simbol.
Lihat data pada catatanmu tadi.
Ada tiga buah apel manis.
Maka gambarlah tiga buah apel.
Gambar berjejer rapi ke samping.
Beri jarak sama antargambar.
Jangan menggambar saling menumpuk.
Kerapian membuat piktogram mudah dibaca."""

s4_content = """Langkah terakhir adalah menulis keterangan.
Tulis keterangan di bagian bawah.
Misal satu bintang mewakili satu anak.
Keterangan ini sangat membantu pembaca.
Kini piktogram buatanmu sudah selesai.

:::common_trap
title: Menggambar Piktogram dengan Rapi
Ukuran setiap gambar harus sama besar.
Jarak antargambar harus rapi teratur.
Jumlah gambar harus sesuai data tabel.
Jangan menggambar lebih atau kurang.
Selalu sertakan keterangan arti gambar.
:::

:::callout
variant: summary
title: Ringkasan
text: Buatlah judul dan pilih simbol. Gambar simbol sesuai data tabel. Tulis keterangan di bawah diagram.
:::"""

sections = [
    {
        "id": S1,
        "title": "Menyiapkan Tabel dan Menulis Judul",
        "minutes": 6,
        "goal": "Siswa dapat mempersiapkan format diagram dan menulis judul data dengan tepat.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Memilih Simbol Gambar yang Tepat",
        "minutes": 6,
        "goal": "Siswa dapat memilih simbol visual yang sederhana, representatif, dan berukuran seragam.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Menggambar Simbol dengan Rapi dan Sejajar",
        "minutes": 6,
        "goal": "Siswa terampil menggambar simbol sesuai kuantitas data dengan susunan sejajar dan proporsional.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menambahkan Keterangan di Bawah Diagram",
        "minutes": 6,
        "goal": "Siswa memahami pentingnya melengkapi diagram piktogram dengan legenda skala yang jelas.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membuat Piktogram Sederhana",
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
# 2. DEFINISI BANK 50 SOAL BAB 35
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
mc("c1", "mudah", D, F, S1, "Langkah awal saat membuat diagram piktogram di kertas adalah ....", ["menulis judul diagram", "mewarnai pinggir kertas", "merobek kertas", "menghapus tabel"], "A", "Menulis judul diagram adalah langkah awal yang tepat.")
tf("c1", "mudah", D, F, S2, "Simbol gambar pada piktogram sebaiknya dipilih yang sederhana dan mudah digambar.", "Benar", "Simbol sederhana mempermudah penggambaran yang seragam.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S3, "Jika data menunjukkan 4 buah jeruk, kita menggambar .... simbol jeruk.", ["4 gambar", "3 gambar", "5 gambar", "2 gambar"], "A", "Jumlah gambar sesuai dengan banyaknya data.", verifikasi={"ekspresi": "4", "hasil": "4"})
mc("c1", "mudah", T, F, S4, "Keterangan kunci arti gambar pada piktogram biasanya ditulis di bagian ....", ["bawah diagram", "belakang buku", "luar ruangan", "bawah meja"], "A", "Keterangan kunci diletakkan di bagian bawah diagram.")
sa("c1", "mudah", T, F, S3, "Ada 3 anak suka susu. Berapa gambar gelas susu yang harus digambar?", "3", "Digambar 3 simbol gelas.", verifikasi={"ekspresi": "3", "hasil": "3"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Mengapa saat menggambar piktogram ukuran setiap simbol harus sama besar?", ["agar diagram tampak rapi dan mudah dibandingkan", "agar pensil cepat habis", "agar gambarnya berantakan", "agar kertas cepat penuh"], "A", "Ukuran seragam membuat perbandingan visual menjadi adil dan rapi.", "Menggambar simbol dengan ukuran berbeda-beda")
tf("c2", "mudah", D, Kn, S4, "Keterangan pada piktogram tidak perlu ditulis jika gambarnya sudah bagus.", "Salah", "Keterangan wajib ada agar pembaca tahu arti gambar.")

# Remedial (2)
mc("c2", "mudah", R, F, S2, "Manakah bentuk simbol yang paling mudah dan cocok untuk piktogram Fase A?", ["lingkaran atau bintang sederhana", "lukisan pemandangan rumit", "gambar naga bersayap", "potret wajah manusia utuh"], "A", "Simbol lingkaran atau bintang sangat mudah dan seragam.", "Memilih simbol yang terlalu rumit")
mc("c2", "mudah", R, Kn, S3, "Jika ada 5 anak peminat buku, apakah boleh hanya digambar 2 buku?", ["tidak boleh, harus digambar tepat 5 buku", "boleh saja sesuka hati", "boleh digambar 10 buku", "boleh dikosongkan"], "A", "Banyak simbol harus tepat sama dengan jumlah data.", "Menggambar jumlah simbol tidak sesuai data")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Lani membuat 3 baris kategori buah dan 2 baris sayur. Total baris?", ["5 baris", "4 baris", "6 baris", "3 baris"], "A", "3 + 2 = 5 baris kategori.", verifikasi={"ekspresi": "3 + 2", "hasil": "5"})
mc("c2", "mudah", T, Kn, S2, "Ada 4 lingkaran biru dan 4 lingkaran merah untuk piktogram. Total lingkaran?", ["8 lingkaran", "7 lingkaran", "9 lingkaran", "6 lingkaran"], "A", "4 + 4 = 8 lingkaran.", verifikasi={"ekspresi": "4 + 4", "hasil": "8"})
tf("c2", "mudah", T, Kn, S3, "Menggambar simbol piktogram secara berjejer ke samping membuat diagram mudah dibaca.", "Benar", "Susunan berjejer ke samping terlihat jelas dan rapi.")
sa("c2", "mudah", T, Kn, S4, "Data ada 6 kelinci. Sudah digambar 2 kelinci. Berapa gambar lagi yang kurang?", "4", "6 - 2 = 4 gambar.", verifikasi={"ekspresi": "6 - 2", "hasil": "4"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Siti menggambar 6 bintang untuk data apel, lalu menambah 3 bintang untuk jeruk. Total bintang?", ["9 bintang", "8 bintang", "10 bintang", "7 bintang"], "A", "6 + 3 = 9 bintang.", "Keliru menjumlahkan simbol yang digambar", verifikasi={"ekspresi": "6 + 3", "hasil": "9"})
mc("c3", "sedang", R, Pr, S4, "Ada 8 data anak. Baru digambar 5 simbol. Berapa simbol yang belum dibuat?", ["3 simbol", "2 simbol", "4 simbol", "1 simbol"], "A", "8 - 5 = 3 simbol.", "Salah menghitung kekurangan simbol piktogram", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Di baris A digambar 5 bola, baris B ada 3 bola. Berapa total seluruh bola?", ["8 bola", "7 bola", "9 bola", "6 bola"], "A", "5 + 3 = 8 bola.", verifikasi={"ekspresi": "5 + 3", "hasil": "8"})
mc("c3", "sedang", T, Pr, S2, "Beni harus menggambar 7 apel dan 5 jeruk. Berapa total seluruh gambar buah?", ["12 buah", "11 buah", "13 buah", "10 buah"], "A", "7 + 5 = 12 buah.", verifikasi={"ekspresi": "7 + 5", "hasil": "12"})
tf("c3", "sedang", T, Pr, S3, "Menggambar simbol saling menumpuk satu sama lain sangat dianjurkan dalam piktogram.", "Salah", "Simbol tidak boleh saling menumpuk agar mudah dihitung.")
mc("c3", "sedang", T, Pr, S4, "Udin menyiapkan 10 stiker bintang. Digunakan 6 stiker untuk piktogram. Sisa stiker?", ["4 stiker", "3 stiker", "5 stiker", "2 stiker"], "A", "10 - 6 = 4 stiker.", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})
tf("c3", "sedang", T, Pr, S1, "Judul piktogram ditulis di paling atas dengan huruf yang jelas.", "Benar", "Judul ditaruh di posisi paling atas tabel diagram.")
sa("c3", "mudah", T, Pr, S3, "Data: 5 mangga dan 4 pisang. Berapa total simbol gambar yang harus dibuat?", "9", "5 + 4 = 9 simbol.", verifikasi={"ekspresi": "5 + 4", "hasil": "9"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Lani menggambar 6 mobil di baris A dan 5 mobil di baris B. Berapa total gambar?", ["11 gambar", "10 gambar", "12 gambar", "9 gambar"], "A", "6 + 5 = 11 gambar.", verifikasi={"ekspresi": "6 + 5", "hasil": "11"})
mc("c3", "sedang", X, Pr, S2, "Ada 12 siswa pemilih. 7 siswa digambar bintang, sisanya bulan. Berapa gambar bulan?", ["5 bulan", "4 bulan", "6 bulan", "3 bulan"], "A", "12 - 7 = 5 gambar.", verifikasi={"ekspresi": "12 - 7", "hasil": "5"})
tf("c3", "sedang", X, Pr, S4, "Menulis '1 gambar = 1 anak' di bawah diagram membuat piktogram jelas.", "Benar", "Keterangan skala membuat nilai data tidak meragukan.")
sa("c3", "sedang", X, Pr, S3, "Harus menggambar 14 simbol bunga. Baru digambar 8 bunga. Kurang berapa?", "6", "14 - 8 = 6 bunga.", verifikasi={"ekspresi": "14 - 8", "hasil": "6"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Dayu menggambar 8 senyum untuk anak ceria dan 6 senyum untuk anak rajin. Total senyum?", ["14 senyum", "13 senyum", "15 senyum", "12 senyum"], "A", "8 + 6 = 14 senyum.", verifikasi={"ekspresi": "8 + 6", "hasil": "14"})
mc("c3", "sedang", K, Pr, S3, "Dalam membuat piktogram pensil: 15 pensil perlu digambar. Sudah selesai 9 pensil. Sisa?", ["6 pensil", "5 pensil", "7 pensil", "4 pensil"], "A", "15 - 9 = 6 pensil.", verifikasi={"ekspresi": "15 - 9", "hasil": "6"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Apa akibatnya jika saat membuat piktogram kita lupa menuliskan judul di atas?", ["pembaca tidak tahu piktogram itu berisi tentang data apa", "kertas gambar robek", "warna gambar menjadi luntur", "simbol gambar hilang sendiri"], "A", "Judul adalah identitas utama topik data yang disajikan.")
mc("c4", "sedang", T, Kn, S2, "Jika kamu menggambar simbol jeruk sebesar bola dan simbol apel sekecil semut, diagram akan ....", ["tampak membingungkan dan tidak sebanding", "sangat sempurna", "mudah dipahami anak kecil", "lebih cepat selesai"], "A", "Ukuran simbol harus seimbang dan seragam.")
tf("c4", "sedang", T, Kn, S3, "Menjaga jarak antarsimbol tetap sama membuat baris data yang lebih banyak terlihat lebih panjang.", "Benar", "Proporsi visual sejajar menunjukkan perbandingan kuantitas secara akurat.")
tf("c4", "sedang", T, Kn, S4, "Bila satu gambar mewakili 1 anak, data 7 anak digambar dengan 3 simbol saja.", "Salah", "7 anak harus digambar dengan tepat 7 simbol.")
sa("c4", "sedang", T, Kn, S4, "Di piktogram hobi: renang 16 gambar. 7 gambar diwarnai biru, sisanya merah. Gambar merah?", "9", "16 - 7 = 9 gambar.", verifikasi={"ekspresi": "16 - 7", "hasil": "9"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Langkah pembuatan piktogram yang tersusun secara urut dan benar adalah ....", ["buat judul, siapkan kategori, gambar simbol sesuai data, tulis keterangan", "gambar simbol acak, buang kertas, tulis nama teman", "tulis keterangan tanpa judul dan tanpa gambar", "warnai kertas sampai hitam"], "A", "Urutan logis: judul, kolom kategori, menggambar simbol, menulis keterangan.")
mc("c4", "sedang", X, Kn, S2, "Ada 15 gambar binatang. 6 gambar kucing, 5 kelinci, sisanya burung. Berapa gambar burung?", ["4 burung", "3 burung", "5 burung", "2 burung"], "A", "15 - (6 + 5) = 4 burung.", verifikasi={"ekspresi": "15 - (6 + 5)", "hasil": "4"})
tf("c4", "sedang", X, Kn, S3, "Menggambar piktogram dengan spidol warna-warni boleh mengubah jumlah simbol data aslinya.", "Salah", "Warna hiasan tidak boleh mengubah jumlah data aslinya.")
mc("c4", "sulit", X, Me, S4, "Tiga anak membuat piktogram: Siti gambar 7 bintang, Edo 5 bintang, Beni 4 bintang. Total bintang?", ["16 bintang", "15 bintang", "17 bintang", "14 bintang"], "A", "7 + 5 + 4 = 16 bintang.", verifikasi={"ekspresi": "7 + 5 + 4", "hasil": "16"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Beni ingin membuat piktogram warna kesukaan. Judul yang paling tepat untuk diagramnya adalah ....", ["Data Warna Kesukaan Siswa Kelas 1", "Daftar Menu Makanan Kantin", "Jadwal Piket Kebersihan Kelas", "Denah Lokasi Sekolah"], "A", "Judul harus mewakili data warna kesukaan siswa.")
mc("c4", "sulit", K, Me, S2, "Tersedia 18 stiker gambar bendera. Digunakan 11 stiker untuk piktogram. Sisa stiker bendera?", ["7 stiker", "6 stiker", "8 stiker", "5 stiker"], "A", "18 - 11 = 7 stiker.", verifikasi={"ekspresi": "18 - 11", "hasil": "7"})
tf("c4", "sulit", K, Me, S3, "Jika data menunjukkan nol (tidak ada pemilih), baris tersebut tetap harus digambar 1 simbol.", "Salah", "Jika data nol (0), baris dikosongkan tanpa simbol.")
mc("c4", "sulit", K, Me, S4, "Data olahraga: lari 7 gambar, senam 6 gambar, renang 5 gambar. Total gambar olahraga?", ["18 gambar", "17 gambar", "19 gambar", "16 gambar"], "A", "7 + 6 + 5 = 18 gambar.", verifikasi={"ekspresi": "7 + 6 + 5", "hasil": "18"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Lani membuat 2 piktogram: piktogram buah butuh 8 simbol, sayur butuh 7 simbol. Total simbol?", ["15 simbol", "14 simbol", "16 simbol", "13 simbol"], "A", "8 + 7 = 15 simbol.", verifikasi={"ekspresi": "8 + 7", "hasil": "15"})
mc("c5", "sedang", T, Me, S2, "Rencanakan piktogram 20 siswa: 8 pilih merah, 6 pilih biru, sisanya kuning. Gambar kuning?", ["6 gambar", "5 gambar", "7 gambar", "4 gambar"], "A", "20 - (8 + 6) = 6 gambar.", verifikasi={"ekspresi": "20 - (8 + 6)", "hasil": "6"})
mc("c5", "sedang", T, Me, S3, "Ada 4 baris kategori piktogram. Tiap baris digambar 4 simbol seragam. Total seluruh simbol?", ["16 simbol", "14 simbol", "18 simbol", "12 simbol"], "A", "4 x 4 = 16 simbol.", verifikasi={"ekspresi": "4 * 4", "hasil": "16"})
mc("c5", "sulit", T, Me, S4, "Piktogram jus: mangga 6 gambar, jeruk 5 gambar, jambu 4 gambar. Berapa total seluruh gambar?", ["15 gambar", "14 gambar", "16 gambar", "13 gambar"], "A", "6 + 5 + 4 = 15 gambar.", verifikasi={"ekspresi": "6 + 5 + 4", "hasil": "15"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Budi punya 14 stiker bintang untuk piktogram. Diberikan ke adik 5 stiker. Sisa stiker?", ["9 stiker", "8 stiker", "10 stiker", "7 stiker"], "A", "14 - 5 = 9 stiker.", verifikasi={"ekspresi": "14 - 5", "hasil": "9"})
mc("c5", "sulit", K, Me, S3, "Data buku: cerita 8 gambar, komik 5 gambar. Berapa selisih gambar yang harus dibuat?", ["3 gambar", "2 gambar", "4 gambar", "1 gambar"], "A", "8 - 5 = 3 gambar.", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Rancanglah susunan piktogram yang paling baik agar mudah dipahami siswa kelas 1!", ["tulis judul jelas di atas, gambar simbol seragam sejajar, beri keterangan skala di bawah", "gambar simbol sebesar-besarnya tanpa tabel dan tanpa judul", "buat gambar tumpang tindih warna hitam pekat", "hilangkan baris kategori nama benda"], "A", "Piktogram ideal: judul jelas di atas, simbol seragam rapi, keterangan di bawah.")
mc("c6", "sulit", K, Me, S3, "Temanmu menggambar 10 apel berdesakan tidak lurus. Apa saran perbaikan terbaikmu?", ["menggambar ulang dengan jarak teratur sejajar ke samping agar rapi", "menghapus setengah gambarnya", "menyobek kertas teman", "mewarnai hitam semua"], "A", "Memberi saran menggambar berjejer dengan jarak teratur.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Tiga baris piktogram masing-masing digambar 7 bintang seragam. Berapa total seluruh bintang?", ["21 bintang", "20 bintang", "22 bintang", "19 bintang"], "A", "3 x 7 = 21 bintang.", verifikasi={"ekspresi": "3 * 7", "hasil": "21"})
mc("c6", "sulit", P, Me, S4, "Data tanaman: mawar 14 pot, melati 7 pot. Berapa selisih gambar simbol kedua tanaman?", ["7 pot", "6 pot", "8 pot", "5 pot"], "A", "14 - 7 = 7 pot.", verifikasi={"ekspresi": "14 - 7", "hasil": "7"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab35_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab35.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
