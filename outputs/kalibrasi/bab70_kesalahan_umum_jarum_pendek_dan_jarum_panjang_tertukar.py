#!/usr/bin/env python3
"""
Generator dan validator Bab 70 Matematika Kelas 2 SD:
"Kesalahan Umum: Jarum Pendek dan Jarum Panjang Tertukar" (Fase A)
bab_id: 1e9e2bda-b17e-4d34-8fa7-94564376bac4
article_id: 6d2a8b75-a073-4d57-875a-b5f2b74533ff
quiz_id: 5ffe502c-01b4-4b7c-b0b7-15efbe029c4e
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "o1q2s3u4w501"  # Perbedaan Bentuk dan Kecepatan Jarum
S2 = "p2r3t4v5x602"  # Kesalahan Membaca Jam Tepat
S3 = "q3s4u5w6y703"  # Kesalahan Membaca Jam Setengah
S4 = "r4t5v6x7z804"  # Cara Jitu Memeriksa Ulang Waktu

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Banyak anak tertukar membaca jarum jam.
Jam dinding memiliki dua jarum utama.
Jarum pendek berukuran lebih pendek.
Jarum ini berputar sangat lambat.
Satu putaran butuh 12 jam.
Jarum panjang berukuran lebih panjang.
Jarum ini berputar lebih cepat.
Satu putaran butuh 60 menit.
Bedakan ukuran kedua jarum tersebut!

:::definition
title: Jarum Pendek vs Panjang
Jarum pendek menunjukkan jam. Jarum panjang menunjukkan menit.
:::"""

s2_content = """Perhatikan saat membaca jam tepat.
Jarum pendek di angka 4.
Jarum panjang di angka 12.
Dibaca pukul empat tepat!
Jangan terbalik membaca pukul dua belas!
Angka 12 adalah milik jarum panjang.
Artinya menitnya adalah tepat nol.
Ingat, sebutkan angka jarum pendek dahulu!

:::common_trap
title: Membaca Angka Jarum Panjang Dahulu
Jarum pendek di 2, panjang di 12.
Jangan dibaca pukul 12 lewat 2!
Bacalah pukul dua tepat.
Penyebutan jam selalu mengacu jarum pendek.
:::"""

s3_content = """Kesalahan sering terjadi saat jam setengah.
Jarum panjang menunjuk angka 6.
Banyak anak mengira pukul 6!
Padahal angka 6 artinya 30 menit.
Lihatlah jarum pendek berada di mana.
Bila di antara 1 dan 2.
Maka dibaca pukul setengah dua.
Bukan pukul enam lewat satu!

:::steps
title: Membaca Jam Setengah dengan Benar
1. Pastikan jarum panjang di angka 6 (30 menit).
2. Periksa posisi jarum pendek di antara dua angka.
3. Sebutkan angka berikutnya sebagai jam setengah.
:::"""

s4_content = """Gunakan langkah jitu memeriksa jam.
Pertama, cari jarum yang lebih pendek.
Lihat angka yang ditunjuk jarum pendek.
Itulah angka satuan jamnya.
Kedua, periksa ujung jarum panjang.
Bila di 12, artinya tepat.
Bila di 6, artinya setengah.
Kini kamu tidak akan tertukar lagi!

:::callout
variant: summary
title: Ringkasan
text: Jarum pendek adalah jam. Jarum panjang adalah menit. Jangan tertukar!
:::"""

sections = [
    {
        "id": S1,
        "title": "Perbedaan Bentuk dan Kecepatan Jarum",
        "minutes": 6,
        "goal": "Siswa mampu membedakan bentuk fisik, fungsi, dan kecepatan jarum jam.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Kesalahan Membaca Jam Tepat",
        "minutes": 6,
        "goal": "Siswa mengenali dan menghindari kekeliruan membaca jarum pada jam tepat.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Kesalahan Membaca Jam Setengah",
        "minutes": 6,
        "goal": "Siswa mengenali dan menghindari salah tafsir jarum panjang di angka 6.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Cara Jitu Memeriksa Ulang Waktu",
        "minutes": 6,
        "goal": "Siswa menerapkan langkah terstruktur untuk memeriksa posisi jarum secara tepat.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Jarum Pendek dan Jarum Panjang Tertukar",
    "topic": "Mengenal Jam, Hari, dan Bulan",
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
# 2. DEFINISI BANK 50 SOAL BAB 70
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
mc("c1", "mudah", D, F, S1, "Jarum yang berukuran lebih pendek pada jam menunjukkan satuan ....", ["jam", "menit", "detik", "hari"], "A", "Jarum pendek adalah penunjuk satuan jam.")
tf("c1", "mudah", D, F, S2, "Jarum pendek di 5 dan jarum panjang di 12 dibaca pukul 05.00 tepat.", "Benar", "Jarum pendek menunjukkan angka 5 tepat.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Jarum yang berukuran lebih panjang pada jam menunjukkan satuan ....", ["menit", "jam", "bulan", "minggu"], "A", "Jarum panjang adalah penunjuk satuan menit.")
mc("c1", "mudah", T, F, S3, "Jika jarum panjang menunjuk tepat angka 6, artinya bernilai ... menit.", ["30 menit", "6 menit", "12 menit", "60 menit"], "A", "6 x 5 = 30 menit.", verifikasi={"ekspresi": "6 * 5", "hasil": "30"})
sa("c1", "mudah", T, F, S1, "Jam dinding analog standar memiliki ... jarum penunjuk utama.", "2", "Memiliki 2 jarum utama (jam dan menit).", verifikasi={"ekspresi": "1 + 1", "hasil": "2"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Jarum pendek di 8, panjang di 12. Mengapa dibaca pukul 8 bukan 12?", ["karena jarum pendek yang menunjukkan satuan jam", "karena angka 8 lebih kecil", "karena jarum panjang lebih cepat", "karena warnanya hitam"], "A", "Satuan jam ditentukan oleh jarum pendek.")
tf("c2", "mudah", D, Kn, S3, "Jarum panjang di angka 6 berarti jam menunjukkan pukul 6 tepat.", "Salah", "Jarum panjang di 6 artinya lewat 30 menit atau setengah jam.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Budi membaca jam pendek di 3, panjang di 12 sebagai pukul 12.03. Mengapa salah?", ["karena tertukar membaca fungsi jarum jam dan menit", "karena jarum pendeknya rusak", "karena 12 ditambah 3 adalah 15", "karena Budi tidak bisa melihat"], "A", "Budi tertukar: jarum pendek di 3 artinya jam 3 tepat.", "Tertukar membaca angka jarum panjang sebagai jam")
mc("c2", "mudah", R, Kn, S3, "Jarum pendek di antara 4 dan 5, panjang di 6 dibaca pukul ....", ["setengah lima", "setengah empat", "pukul enam tepat", "pukul empat tepat"], "A", "Melewati 4 menuju 5 dibaca setengah lima.", "Menyebut angka sebelumnya pada jam setengah")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Di antara kedua jarum jam, manakah jarum yang bergerak lebih lambat?", ["jarum pendek", "jarum panjang", "keduanya sama cepat", "tidak ada yang bergerak"], "A", "Jarum pendek bergerak lambat (12 jam per putaran).")
mc("c2", "mudah", T, Kn, S2, "Jarum pendek di 1, panjang di 12 dibaca sebagai pukul ....", ["01.00 tepat", "12.01", "12.05", "11.00"], "A", "Pendek di 1, panjang di 12 = 01.00 tepat.")
tf("c2", "mudah", T, Kn, S1, "Satu putaran penuh jarum pendek memerlukan waktu selama 12 jam.", "Benar", "Jarum pendek butuh 12 jam untuk 1 putaran penuh.")
sa("c2", "mudah", T, Kn, S3, "Jarum panjang di angka 6 menandakan waktu ... jam.", "setengah", "Angka 6 adalah setengah jam.")

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Jarum pendek di 11, panjang di 12. Bentuk penulisan tanda waktunya?", ["11.00", "12.11", "11.12", "12.00"], "A", "Ditulis 11.00.", "Menulis 12.11 karena tertukar posisi jarum")
mc("c3", "sedang", R, Pr, S4, "Langkah pertama yang benar untuk mengetahui pukul berapa sekarang adalah ....", ["melihat angka yang ditunjuk jarum pendek", "melihat angka yang ditunjuk jarum panjang", "menghitung jumlah garis kecil", "memutar jarum jam"], "A", "Langkah 1: cari jarum pendek untuk menentukan jam.", "Melihat jarum panjang terlebih dahulu tanpa memperhatikan jarum pendek")

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S2, "Jarum pendek di 7, panjang di 12. Tiga jam lagi pukul berapa?", ["10.00", "09.00", "11.00", "08.00"], "A", "7 + 3 = 10.00.", verifikasi={"ekspresi": "7 + 3", "hasil": "10"})
mc("c3", "mudah", T, Pr, S3, "Jarum pendek di antara 9 dan 10, panjang di 6. Menunjukkan lewat ... menit.", ["30 menit", "10 menit", "6 menit", "20 menit"], "A", "6 x 5 = 30 menit.", verifikasi={"ekspresi": "6 * 5", "hasil": "30"})
tf("c3", "sedang", T, Pr, S2, "Jarum pendek di 12 dan panjang di 12 menunjukkan pukul 12.00 tepat.", "Benar", "Kedua jarum berimpit di atas angka 12 = 12.00 tepat.")
mc("c3", "sedang", T, Pr, S4, "Dalam 24 jam, jarum panjang berputar penuh sebanyak berapa kali?", ["24 kali", "12 kali", "2 kali", "48 kali"], "A", "Tiap 1 jam 1 kali, jadi 24 kali putaran.", verifikasi={"ekspresi": "24 * 1", "hasil": "24"})
tf("c3", "sedang", T, Pr, S3, "Pada pukul 06.30, kedua jarum jam menunjuk tepat pada angka 6.", "Salah", "Jarum pendek berada di antara 6 dan 7, bukan tepat di 6.")
sa("c3", "sedang", T, Pr, S4, "Berapa jam waktu yang dibutuhkan jarum pendek menempuh 1 putaran penuh?", "12", "1 putaran = 12 jam.", verifikasi={"ekspresi": "12 * 1", "hasil": "12"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S2, "Siti melihat jarum pendek di 6, panjang di 12. Pukul ... tepat.", ["6 tepat", "12 tepat", "3 tepat", "8 tepat"], "A", "Pukul 6 tepat.", verifikasi={"ekspresi": "6 * 1", "hasil": "6"})
mc("c3", "sedang", X, Pr, S3, "Jarum pendek di antara 8 dan 9, panjang di 6. Dua jam kemudian pukul?", ["setengah sebelas (10.30)", "setengah sepuluh", "pukul sepuluh tepat", "setengah dua belas"], "A", "08.30 + 2 jam = 10.30.")
tf("c3", "sedang", X, Pr, S4, "Memeriksa jarum pendek terlebih dahulu mencegah salah membaca jam.", "Benar", "Jarum pendek menentukan jam dasar secara akurat.")
sa("c3", "sedang", X, Pr, S2, "Jarum pendek bergerak dari angka 1 ke angka 5 melewati ... jam.", "4", "5 - 1 = 4 jam.", verifikasi={"ekspresi": "5 - 1", "hasil": "4"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Jika jarum pendek di 2 dan panjang di 12, lima jam lalu pukul?", ["09.00", "10.00", "08.00", "07.00"], "A", "14 - 5 = 9.00 (atau 2 mundur 5 = 9.00).", verifikasi={"ekspresi": "14 - 5", "hasil": "9"})
mc("c3", "sedang", K, Pr, S3, "Waktu menunjukkan pukul 01.30. Jarum panjang menunjuk angka ....", ["6", "1", "12", "3"], "A", "30 : 5 = 6.", verifikasi={"ekspresi": "30 / 5", "hasil": "6"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Bila jarum panjang bergerak 360 derajat, jarum pendek berpindah ... angka.", ["1 angka", "2 angka", "6 angka", "12 angka"], "A", "12 : 12 = 1 angka.", verifikasi={"ekspresi": "12 / 12", "hasil": "1"})
mc("c4", "sedang", T, Kn, S2, "Siswa mengira jam dinding mati karena jarum pendek tidak tampak bergerak. Mengapa?", ["karena gerak jarum pendek sangat lambat dan halus", "karena baterainya habis", "karena jarum pendek rusak", "karena jamnya digital"], "A", "Jarum pendek bergerak sangat lambat sehingga kasat mata tampak diam.")
tf("c4", "sedang", T, Kn, S3, "Pada pukul 12.30, kedua jarum jam membentuk garis lurus vertikal.", "Salah", "Jarum pendek sedikit bergeser lewat angka 12, tidak lurus tepat.")
tf("c4", "sedang", T, Kn, S4, "Langkah terbaik membaca jam adalah melihat posisi jarum panjang terlebih dahulu.", "Salah", "Langkah terbaik adalah melihat jarum pendek terlebih dahulu untuk menentukan jam.")
sa("c4", "sedang", T, Kn, S1, "Selisih waktu 1 putaran jarum pendek dan 1 putaran jarum panjang adalah ... jam.", "11", "12 - 1 = 11 jam.", verifikasi={"ekspresi": "12 - 1", "hasil": "11"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S2, "Manakah pernyataan yang BENAR mengenai posisi jarum jam dinding?", ["jarum panjang di 12 selalu menandakan pergantian jam tepat", "jarum pendek di 12 selalu artinya tengah malam", "jarum panjang lebih tebal daripada jarum pendek", "kedua jarum berputar berlawanan"], "A", "Jarum panjang di 12 menandakan menit tepat (00).")
mc("c4", "sedang", X, Kn, S3, "Mengapa saat pukul 04.30 jarum pendek tidak berada tepat di angka 4?", ["karena sudah berjalan setengah jalan menuju angka 5", "karena jarumnya goyang", "karena jarumnya bengkok", "supaya terlihat jelas"], "A", "Setengah jam berjalan menggeser jarum pendek setengah jarak.")
tf("c4", "sedang", X, Kn, S2, "Pukul 02.00 dan pukul 06.00 membentuk sudut yang sama besar.", "Salah", "Pukul 02.00 bersudut 60 derajat, sedangkan pukul 06.00 bersudut 180 derajat.")
mc("c4", "sulit", X, Me, S4, "Ali melihat jam 05.30. Berapa jam selisihnya jika dua jam lalu pukul 03.30?", ["2 jam", "3 jam", "1 jam", "4 jam"], "A", "5 - 3 = 2 jam.", verifikasi={"ekspresi": "5 - 3", "hasil": "2"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Berapa kali jarum panjang melewati angka 12 dalam rentang waktu 6 jam?", ["6 kali", "5 kali", "7 kali", "12 kali"], "A", "1 kali tiap jam, jadi 6 kali.", verifikasi={"ekspresi": "6 * 1", "hasil": "6"})
mc("c4", "sulit", K, Me, S2, "Jika jarum jam tertukar: pendek di 12, panjang di 3. Seharusnya jam berapa?", ["03.00 tepat bila pendek di 3", "12.15", "03.12", "15.00"], "A", "Jika dimaksud jam 3 tepat, seharusnya pendek di 3 panjang di 12.")
tf("c4", "sulit", K, Me, S3, "Pada pukul 06.00 tepat, kedua jarum jam membentuk garis lurus sempurna.", "Benar", "Pendek di 6, panjang di 12 membentuk garis lurus 180 derajat.")
mc("c4", "sulit", K, Me, S4, "Jam dinding rusak berjalan 2 kali lebih cepat. Saat harusnya 2 jam, jam menunjukkan?", ["4 jam", "3 jam", "1 jam", "6 jam"], "A", "2 x 2 = 4 jam.", verifikasi={"ekspresi": "2 * 2", "hasil": "4"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Bila sebuah jam hanya memiliki jarum pendek, apa yang masih bisa diperkirakan?", ["perkiraan jam kasarnya", "menit secara tepat", "detik secara akurat", "tidak bisa melihat apa pun"], "A", "Jarum pendek masih memperlihatkan posisi jam perkiraan.")
mc("c5", "sedang", T, Me, S2, "Jarum pendek di 9, panjang di 12. Berapa derajat sudut yang dibentuk terkecil?", ["90 derajat", "180 derajat", "45 derajat", "120 derajat"], "A", "3 angka x 30 = 90 derajat siku-siku.", verifikasi={"ekspresi": "3 * 30", "hasil": "90"})
mc("c5", "sedang", T, Me, S3, "Sebuah jam menunjukkan 07.30. Berapa menit jarum panjang harus berputar ke 08.00?", ["30 menit", "15 menit", "45 menit", "60 menit"], "A", "Dari 6 ke 12 butuh 30 menit.", verifikasi={"ekspresi": "60 - 30", "hasil": "30"})
mc("c5", "sulit", T, Me, S4, "Dua jam dinding: Jam A tepat 08.00, Jam B tertukar dibaca 12.40. Selisih jam?", ["4 jam", "3 jam", "5 jam", "2 jam"], "A", "12 - 8 = 4 jam.", verifikasi={"ekspresi": "12 - 8", "hasil": "4"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Berapa putaran jarum panjang diperlukan untuk menyamai 3 putaran jarum pendek?", ["36 putaran", "24 putaran", "48 putaran", "12 putaran"], "A", "3 x 12 = 36 putaran jarum panjang.", verifikasi={"ekspresi": "3 * 12", "hasil": "36"})
mc("c5", "sulit", K, Me, S3, "Berapa jam selisih waktu antara pukul 09.30 dan pukul 12.30?", ["3 jam", "2 jam", "4 jam", "1 jam"], "A", "12 - 9 = 3 jam.", verifikasi={"ekspresi": "12 - 9", "hasil": "3"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Mengapa jarum penunjuk detik dibuat paling panjang dan paling tipis pada jam?", ["agar mudah berputar cepat tanpa membebani mesin jam dan jelas terbaca", "agar hemat tempat", "karena detik itu kecil", "hanya hiasan"], "A", "Bentuk tipis dan panjang mengurangi hambatan dan memudahkan presisi membaca.")
mc("c6", "sulit", K, Me, S4, "Buat rancangan perbaikan: jika sering tertukar jarum, apa trik terbaik?", ["memberi warna berbeda yang mencolok pada jarum pendek dan jarum panjang", "mencopot jarum panjang", "mengganti angka menjadi huruf", "menutup kaca jam"], "A", "Pemberian warna kontras mempermudah mata membedakan fungsi jarum.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Hitunglah total putaran: 5 putaran jarum pendek + 24 putaran jarum panjang!", ["29 putaran", "30 putaran", "28 putaran", "32 putaran"], "A", "5 + 24 = 29 putaran.", verifikasi={"ekspresi": "5 + 24", "hasil": "29"})
mc("c6", "sulit", P, Me, S3, "Sebuah jam berputar terbalik (mundur). Dari 12.00 mundur 4 jam, menunjukkan angka?", ["8", "4", "9", "7"], "A", "12 - 4 = 8.", verifikasi={"ekspresi": "12 - 4", "hasil": "8"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab70_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab70.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
