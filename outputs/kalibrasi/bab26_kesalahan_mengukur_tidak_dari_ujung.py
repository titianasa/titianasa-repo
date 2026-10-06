#!/usr/bin/env python3
"""
Generator dan validator Bab 26 Matematika Kelas 1 SD:
"Kesalahan Umum: Mengukur Tidak Dimulai dari Ujung Benda" (Fase A)
bab_id: 93ab55a1-daca-46a5-a650-06310afab6f0
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "c1d2e33f4a01"  # Mengapa Harus Mulai dari Ujung Benda
S2 = "d2e3f44a5b12"  # Jangan Ada Celah dan Jangan Menumpuk
S3 = "e3f4a55b6c23"  # Memeriksa Titik Nol pada Timbangan
S4 = "f4a5b66c7d34"  # Langkah Memeriksa Ulang Hasil Ukuran

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Mengukur panjang butuh ketelitian.
Banyak anak melakukan kesalahan.
Mereka menaruh alat dari tengah benda.
Itu membuat ukuran tampak lebih pendek.
Ada juga yang mulai dari luar.
Itu membuat ukuran tampak lebih panjang.
Ukuran yang benar mulai dari ujung.
Ujung alat pas di ujung benda.

:::definition
title: Ujung Benda
Ujung benda adalah bagian tepi paling awal.
Pengukuran harus selalu dimulai tepat dari tepi itu.
:::"""

s2_content = """Susun satuan ukur dengan rapi.
Jangan meninggalkan celah kosong di tengah.
Celah membuat hitungan jadi kurang.
Jangan pula menyusun bertumpuk.
Tumpukan membuat hitungan jadi berlebih.
Alat ukur harus lurus rapat.
Rapatkan ujung ke ujung satuan.
Maka hasil ukur tepat dan jujur.

:::steps
title: Menyusun Satuan Ukur
1. Letakkan satuan pertama tepat di ujung.
2. Rapatkan satuan berikutnya tanpa celah.
3. Pastikan satuan tidak saling bertumpuk.
:::"""

s3_content = """Kesalahan juga terjadi pada timbangan.
Kadang timbangan sudah miring di awal.
Sebelum dipakai timbangan harus seimbang.
Periksa posisi lengan timbangan gantungan baju.
Kedua kantong harus sama berat.
Posisi awal harus lurus mendatar.
Jangan menimbang saat alat masih bergoyang.
Tunggu timbangan diam dan tenang."""

s4_content = """Selalu periksa ulang hasil pengukuranmu.
Lihat kembali dari ujung awal benda.
Periksa sampai ujung akhir benda.
Hitung kembali jumlah satuan ukurnya.

:::common_trap
title: Mengukur dari Tengah Benda
Beni mengukur pensil dengan klip kertas.
Beni mulai menaruh klip dari tengah.
Hasilnya pensil tampak sangat pendek.
Ukuran itu salah.
Selalu letakkan klip pertama tepat di ujung.
:::

:::callout
variant: summary
title: Ringkasan
text: Mulailah mengukur tepat dari ujung. Susun satuan rapat tanpa celah dan tanpa tumpukan. Timbangan harus seimbang di awal.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengapa Harus Mulai dari Ujung Benda",
        "minutes": 6,
        "goal": "Siswa memahami pentingnya menempatkan alat ukur tepat pada ujung awal benda dan tidak dari tengah atau luar.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Jangan Ada Celah dan Jangan Menumpuk",
        "minutes": 6,
        "goal": "Siswa mengenali kesalahan menyisakan celah kosong atau menumpuk satuan ukur saat mengukur panjang.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Memeriksa Titik Nol pada Timbangan",
        "minutes": 6,
        "goal": "Siswa mengenali kesalahan menimbang dengan timbangan yang belum seimbang mendatar pada posisi awal.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Langkah Memeriksa Ulang Hasil Ukuran",
        "minutes": 6,
        "goal": "Siswa membiasakan diri mengecek ulang pengukuran secara teliti dari ujung ke ujung.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Mengukur Tidak Dimulai dari Ujung Benda",
    "topic": "Membandingkan dan Mengukur dengan Satuan Tak Baku",
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
# 2. DEFINISI BANK 50 SOAL BAB 26
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
mc("c1", "mudah", D, F, S1, "Saat mengukur panjang pensil, kita harus mulai dari ....", ["ujung paling tepi", "tengah pensil", "luar pensil", "bebas mana saja"], "A", "Pengukuran harus selalu dimulai tepat di ujung paling tepi.")
tf("c1", "mudah", D, F, S2, "Menyusun klip kertas untuk mengukur panjang harus rapat tanpa celah.", "Benar", "Klip harus dijajarkan rapat dari ujung ke ujung.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Kesalahan yang membuat jumlah klip terhitung terlalu banyak adalah ....", ["klip disusun bertumpuk", "klip ditaruh berjarak renggang", "klip ditaruh lurus", "klip sama panjang"], "A", "Menumpuk klip menyebabkan jumlah klip terpakai lebih banyak.")
mc("c1", "mudah", T, F, S3, "Sebelum menimbang, posisi timbangan gantungan baju harus ....", ["lurus mendatar seimbang", "miring ke kiri", "miring ke kanan", "terus berputar"], "A", "Timbangan harus seimbang mendatar di awal penimbangan.")
sa("c1", "mudah", T, F, S4, "Berapa klip panjang pensil jika diukur pas dari ujung dapat 5?", "5", "Panjang pensil tepat 5 klip kertas.", verifikasi={"ekspresi": "5", "hasil": "5"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Apa yang terjadi jika mengukur pensil dimulai dari tengah?", ["pensil terhitung lebih pendek", "pensil terhitung lebih panjang", "pensil menjadi bengkok", "pensil bertambah panjang"], "A", "Memulai dari tengah menghilangkan bagian awal sehingga terhitung lebih pendek.", "Mengukur mulai dari tengah benda")
tf("c2", "mudah", D, Kn, S3, "Timbangan yang sudah miring sebelum dipakai menghasilkan ukuran yang salah.", "Benar", "Posisi awal yang miring membuat hasil penimbangan tidak adil dan keliru.")

# Remedial (2)
mc("c2", "mudah", R, F, S2, "Jika ada celah kosong antar-klip, hasil ukuran pensil menjadi tampak ....", ["lebih sedikit klip", "lebih banyak klip", "sangat tepat", "lebih berat"], "A", "Celah kosong membuat klip yang terpasang lebih sedikit dari seharusnya.", "Menyisakan celah renggang saat mengukur")
mc("c2", "mudah", R, Kn, S4, "Beni mengukur dapat 3 klip. Siti mengukur dari ujung dapat 6 klip. Selisihnya?", ["3 klip", "2 klip", "4 klip", "1 klip"], "A", "6 - 3 = 3 klip.", "Salah menghitung koreksi hasil ukur", verifikasi={"ekspresi": "6 - 3", "hasil": "3"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Ujung penggaris harus diletakkan sejajar dengan ....", ["ujung awal benda", "bagian tengah benda", "meja guru", "buku tulis"], "A", "Ujung awal alat ukur harus tepat sejajar ujung awal benda.")
mc("c2", "mudah", T, Kn, S2, "Panjang pita asli 7 klip. Doni menumpuk klip jadi 9 klip. Berapa lebihnya?", ["2 klip", "1 klip", "3 klip", "4 klip"], "A", "9 - 7 = 2 klip lebih banyak.", verifikasi={"ekspresi": "9 - 7", "hasil": "2"})
tf("c2", "mudah", T, Kn, S1, "Mengukur panjang benda boleh dimulai dari titik mana saja sesuka hati.", "Salah", "Pengukuran harus selalu dimulai dari ujung benda secara konsisten.")
sa("c2", "mudah", T, Kn, S3, "Berapa kelereng selisih timbangan jika kiri 8 dan kanan 5?", "3", "8 - 5 = 3 kelereng.", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Doni mulai mengukur dari luar pensil sejauh 2 cm. Pensil tampak ....", ["lebih panjang dari aslinya", "lebih pendek dari aslinya", "sama panjang", "tidak berubah"], "A", "Mulai dari luar pensil menambah panjang semu sehingga tampak lebih panjang.", "Mengukur mulai dari luar ujung benda")
mc("c3", "sedang", R, Pr, S3, "Sebelum memasukkan kelereng, timbangan condong ke kanan. Apa yang harus dilakukan?", ["seimbangkan dahulu hingga mendatar", "langsung timbang saja", "tambah beban di kanan", "abaikan saja"], "A", "Timbangan harus diseimbangkan mendatar sebelum menimbang.", "Menimbang tanpa memeriksa posisi awal seimbang")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Panjang pensil asli 6 klip. Karena mulai dari tengah, terhitung 4 klip. Selisihnya?", ["2 klip", "1 klip", "3 klip", "4 klip"], "A", "6 - 4 = 2 klip.", verifikasi={"ekspresi": "6 - 4", "hasil": "2"})
mc("c3", "sedang", T, Pr, S2, "Edo mengukur tali: 5 klip rapat ditambah 3 klip rapat. Berapa total klip?", ["8 klip", "7 klip", "9 klip", "6 klip"], "A", "5 + 3 = 8 klip.", verifikasi={"ekspresi": "5 + 3", "hasil": "8"})
tf("c3", "sedang", T, Pr, S3, "Menimbang saat timbangan masih bergoyang cepat menghasilkan ukuran yang tepat.", "Salah", "Timbangan harus ditunggu tenang dan diam sebelum dibaca.")
mc("c3", "sedang", T, Pr, S4, "Langkah pertama yang benar saat mengecek ulang ukuran panjang adalah ....", ["melihat apakah titik awal tepat di ujung", "langsung menghitung angka", "memotong benda", "mengganti penggaris"], "A", "Periksa dahulu apakah posisi awal alat sudah tepat di ujung.")
tf("c3", "sedang", T, Pr, S1, "Menaruh alat ukur tepat di ujung membuat hasil ukur akurat dan benar.", "Benar", "Posisi tepat di ujung menjamin panjang keseluruhan terukur benar.")
sa("c3", "mudah", T, Pr, S2, "Panjang balok 10 klip. Tersusun 6 klip. Berapa klip yang kurang?", "4", "10 - 6 = 4 klip.", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Panjang buku 8 jengkal. Dihitung tanpa ujung dapat 5 jengkal. Berapa jengkal terlewat?", ["3 jengkal", "2 jengkal", "4 jengkal", "1 jengkal"], "A", "8 - 5 = 3 jengkal.", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})
mc("c3", "sedang", X, Pr, S2, "Budi memakai 12 batang korek api berjejer rapat. 4 batang patah. Berapa batang utuh?", ["8 batang", "7 batang", "9 batang", "6 batang"], "A", "12 - 4 = 8 batang.", verifikasi={"ekspresi": "12 - 4", "hasil": "8"})
tf("c3", "sedang", X, Pr, S3, "Kedua kantong timbangan kosong harus sama tinggi sebelum diisi benda.", "Benar", "Kedua kantong kosong harus seimbang rata sama tinggi.")
sa("c3", "sedang", X, Pr, S4, "Penggaris mengukur 15 cm. Terlewat 5 cm di awal. Berapa cm terukur?", "10", "15 - 5 = 10 cm.", verifikasi={"ekspresi": "15 - 5", "hasil": "10"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Panjang tongkat 14 jengkal. Adik menghitung 9 jengkal. Berapa selisihnya?", ["5 jengkal", "4 jengkal", "6 jengkal", "3 jengkal"], "A", "14 - 9 = 5 jengkal.", verifikasi={"ekspresi": "14 - 9", "hasil": "5"})
mc("c3", "sedang", K, Pr, S2, "Ukur pita = 7 klip. Ditambah 6 klip lagi. Berapa jumlah klip pita?", ["13 klip", "12 klip", "14 klip", "11 klip"], "A", "7 + 6 = 13 klip.", verifikasi={"ekspresi": "7 + 6", "hasil": "13"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Mengapa pangkal kedua pensil harus diratakan sejajar sebelum dibandingkan panjangnya?", ["agar perbandingan panjang adil dan benar", "agar pensil tidak patah", "agar warnanya kelihatan", "agar meja tidak kotor"], "A", "Pangkal sejajar memastikan perbandingan dimulai dari garis awal yang sama.")
mc("c4", "sedang", T, Kn, S2, "Manakah susunan klip kertas yang memberikan hasil pengukuran paling benar?", ["lurus rapat tanpa celah dan tidak bertumpuk", "berbelok-belok zig-zag", "bertumpuk tiga lapis", "renggang dengan jarak lebar"], "A", "Susunan lurus rapat tanpa celah dan tanpa tumpukan adalah yang benar.")
tf("c4", "sedang", T, Kn, S3, "Menimbang benda dengan kantong bocor akan membuat timbangan tetap akurat.", "Salah", "Kantong bocor menyebabkan kelereng jatuh dan hitungan salah.")
tf("c4", "sedang", T, Kn, S4, "Menghitung klip dari ujung sampai ujung lain memastikan tidak ada bagian terlewat.", "Benar", "Pengecekan menyeluruh memastikan seluruh panjang terukur.")
sa("c4", "sedang", T, Kn, S4, "Panjang pensil 16 cm. Ujung awal tergeser 4 cm. Berapa cm panjang sisa?", "12", "16 - 4 = 12 cm.", verifikasi={"ekspresi": "16 - 4", "hasil": "12"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Jika pangkal pensil A lebih maju dari B, bagaimana membandingkannya?", ["sejajarkan kedua pangkalnya terlebih dahulu", "langsung lihat ujung depannya", "potong pensil yang panjang", "balik arah pensil"], "A", "Kedua pangkal harus disejajarkan rata terlebih dahulu.")
mc("c4", "sedang", X, Kn, S2, "Ani menyusun 8 klip bertumpuk. Rina menyusun 6 klip lurus pas. Berapa selisihnya?", ["2 klip", "1 klip", "3 klip", "4 klip"], "A", "8 - 6 = 2 klip.", verifikasi={"ekspresi": "8 - 6", "hasil": "2"})
tf("c4", "sedang", X, Kn, S4, "Mengukur pensil miring menghasilkan panjang yang sama dengan mengukur lurus.", "Salah", "Garis miring lebih panjang daripada garis lurus sejajar.")
mc("c4", "sulit", X, Me, S3, "Timbangan seimbang saat 1 mangga = 10 kelereng. Jika ada 2 mangga, butuh berapa kelereng?", ["20 kelereng", "18 kelereng", "22 kelereng", "15 kelereng"], "A", "10 + 10 = 20 kelereng.", verifikasi={"ekspresi": "10 + 10", "hasil": "20"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Apa bahaya jika kita mengukur kain tidak dari ujungnya?", ["kain yang dibeli ukurannya salah dan kurang", "kain menjadi kusut", "warna kain pudar", "gunting kain tumpul"], "A", "Ukuran menjadi salah sehingga kain yang didapat tidak sesuai kebutuhan.")
mc("c4", "sulit", K, Me, S2, "Pita diukur: sisi kiri 9 klip, sisi kanan 4 klip. Berapa selisih klipnya?", ["5 klip", "4 klip", "6 klip", "3 klip"], "A", "9 - 4 = 5 klip.", verifikasi={"ekspresi": "9 - 4", "hasil": "5"})
tf("c4", "sulit", K, Me, S3, "Timbangan gantungan baju boleh ditiup saat membaca hasil timbangannya.", "Salah", "Tiupan angin membuat timbangan goyang dan tidak akurat.")
mc("c4", "sulit", K, Me, S4, "Meja = 18 jengkal. Terhitung 11 jengkal karena celah. Berapa jengkal terlewat?", ["7 jengkal", "6 jengkal", "8 jengkal", "5 jengkal"], "A", "18 - 11 = 7 jengkal.", verifikasi={"ekspresi": "18 - 11", "hasil": "7"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Panjang tali A = 9 jengkal. Tali B = 13 jengkal. Berapa total jengkal keduanya?", ["22 jengkal", "20 jengkal", "24 jengkal", "21 jengkal"], "A", "9 + 13 = 22 jengkal.", verifikasi={"ekspresi": "9 + 13", "hasil": "22"})
mc("c5", "sedang", T, Me, S2, "Doni butuh 15 klip untuk tongkat. Baru ada 8 klip. Berapa klip kekurangannya?", ["7 klip", "6 klip", "8 klip", "5 klip"], "A", "15 - 8 = 7 klip.", verifikasi={"ekspresi": "15 - 8", "hasil": "7"})
mc("c5", "sedang", T, Me, S3, "Di timbangan ada 16 kelereng. Diambil 7 kelereng agar seimbang. Berapa kelereng sisa?", ["9 kelereng", "8 kelereng", "10 kelereng", "7 kelereng"], "A", "16 - 7 = 9 kelereng.", verifikasi={"ekspresi": "16 - 7", "hasil": "9"})
mc("c5", "sulit", T, Me, S4, "Beni mengukur tali dapat 5 hasta. Dayu dapat 7 hasta. Mengapa hasil mereka berbeda?", ["karena panjang lengan Beni dan Dayu berbeda", "karena tali memendek sendiri", "karena mata angin", "karena tali kotor"], "A", "Ukuran hasta bergantung pada panjang lengan masing-masing orang.")

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Jarak pintu = 14 langkah. Baru melangkah 6 langkah. Berapa langkah sisa?", ["8 langkah", "7 langkah", "9 langkah", "6 langkah"], "A", "14 - 6 = 8 langkah.", verifikasi={"ekspresi": "14 - 6", "hasil": "8"})
mc("c5", "sulit", K, Me, S3, "1 buku = 6 koin. 1 kotak pensil = 8 koin. Berapa koin total berat kedua benda?", ["14 koin", "13 koin", "15 koin", "12 koin"], "A", "6 + 8 = 14 koin.", verifikasi={"ekspresi": "6 + 8", "hasil": "14"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Susunlah cara mengukur pensil memakai klip kertas dari awal sampai selesai!", ["sejajarkan klip pertama di ujung, susun berderet rapat lurus, lalu hitung totalnya", "susun klip di tengah pensil lalu tebak sisanya", "tumpuk klip setinggi mungkin di atas pensil", "taruh klip berserakan di sekitar meja"], "A", "Mulai dari ujung, susun rapat lurus tanpa celah, lalu hitung seluruhnya.")
mc("c6", "sulit", K, Me, S3, "Rancanglah cara memastikan timbangan gantung sudah adil sebelum digunakan!", ["gantungkan kedua kantong kosong dan pastikan lengan timbangan mendatar diam", "tiup timbangan agar berputar", "masukkan benda langsung tanpa melihat posisi awal", "pegang salah satu ujung lengan timbangan"], "A", "Pastikan kedua kantong kosong membuat lengan timbangan mendatar lurus.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S2, "Pita 20 cm diukur dengan klip 2 cm. Berapa klip yang tersusun pas?", ["10 klip", "8 klip", "12 klip", "9 klip"], "A", "20 / 2 = 10 klip.", verifikasi={"ekspresi": "20 // 2", "hasil": "10"})
mc("c6", "sulit", P, Me, S4, "Koreksi ukuran: buku 8 klip, kotak 12 klip. Berapa total klip kedua benda?", ["20 klip", "18 klip", "22 klip", "19 klip"], "A", "8 + 12 = 20 klip.", verifikasi={"ekspresi": "8 + 12", "hasil": "20"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab26_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab26.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
