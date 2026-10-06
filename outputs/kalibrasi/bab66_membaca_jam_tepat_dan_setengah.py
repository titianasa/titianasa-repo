#!/usr/bin/env python3
"""
Generator dan validator Bab 66 Matematika Kelas 2 SD:
"Membaca Jam Tepat dan Setengah" (Fase A)
bab_id: 862e9526-7fb1-44d0-b6ca-c09bcd660abd
article_id: 3d0f5576-691d-4b3b-ba4a-2f4d2292a146
quiz_id: 3ff26c16-85e5-44e2-bcc4-e6d5d73b97b6
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "k1m2o3q4s501"  # Mengenal Dua Jarum Jam
S2 = "l2n3p4r5t602"  # Membaca Jam Tepat
S3 = "m3o4q5s6u703"  # Membaca Jam Setengah
S4 = "n4p5r6t7v804"  # Menuliskan Tanda Waktu

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Lihatlah jam dinding di kelasmu.
Jam memiliki dua jarum penting.
Ada jarum pendek dan jarum panjang.
Jarum pendek menunjukkan satuan jam.
Jarum panjang menunjukkan satuan menit.
Kedua jarum berputar ke arah kanan.
Jarum berputar teratur setiap saat.
Kenali perbedaan kedua jarum jam!

:::definition
title: Jarum Jam
Jarum pendek menunjuk angka jam. Jarum panjang menunjuk angka menit.
:::"""

s2_content = """Pertama, mari membaca jam tepat.
Lihat jarum panjang di angka 12.
Artinya menit menunjukkan tepat nol.
Lalu lihat posisi jarum pendek.
Jika jarum pendek di angka 3.
Maka dibaca pukul tiga tepat.
Jika jarum pendek di angka 8.
Maka dibaca pukul delapan tepat.
Mudah sekali membaca jam tepat!

:::steps
title: Langkah Membaca Jam Tepat
1. Periksa jarum panjang tepat di 12.
2. Lihat angka yang ditunjuk jarum pendek.
3. Sebutkan pukul sesuai angka jarum pendek.
:::"""

s3_content = """Sekarang kita belajar jam setengah.
Jarum panjang menunjuk angka 6.
Angka 6 artinya tiga puluh menit.
Jarum pendek ada di tengah angka.
Misalnya di antara 1 dan 2.
Maka dibaca pukul setengah dua.
Artinya sudah lewat tiga puluh menit.
Perhatikan posisi jarum di tengah!

:::common_trap
title: Salah Menyebut Jam Setengah
Jarum pendek di antara 2 dan 3.
Jarum panjang di angka 6.
Bukan setengah dua!
Sebutlah angka berikutnya: setengah tiga.
:::"""

s4_content = """Waktu dapat kita tuliskan rapi.
Gunakan tanda titik pemisah waktu.
Pukul lima tepat ditulis 05.00.
Dua angka depan adalah jam.
Dua angka belakang adalah menit.
Pukul setengah enam ditulis 05.30.
Tiga puluh menit artinya setengah jam.
Tuliskan tanda waktu dengan benar!

:::callout
variant: summary
title: Ringkasan
text: Jarum panjang di 12 artinya tepat. Jarum panjang di 6 artinya setengah.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Dua Jarum Jam",
        "minutes": 6,
        "goal": "Siswa mengenal fungsi jarum pendek (jam) dan jarum panjang (menit).",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Membaca Jam Tepat",
        "minutes": 6,
        "goal": "Siswa mampu membaca jam saat jarum panjang menunjuk tepat angka 12.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membaca Jam Setengah",
        "minutes": 6,
        "goal": "Siswa mampu membaca jam saat jarum panjang menunjuk angka 6 (setengah jam).",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menuliskan Tanda Waktu",
        "minutes": 6,
        "goal": "Siswa mampu menuliskan tanda waktu format jam dan menit (misal 08.00 dan 08.30).",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membaca Jam Tepat dan Setengah",
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
# 2. DEFINISI BANK 50 SOAL BAB 66
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
mc("c1", "mudah", D, F, S1, "Jarum pendek pada jam dinding berfungsi untuk menunjukkan ....", ["jam", "menit", "detik", "hari"], "A", "Jarum pendek adalah penunjuk satuan jam.")
tf("c1", "mudah", D, F, S2, "Jika jarum panjang di angka 12, waktu menunjukkan jam tepat.", "Benar", "Angka 12 adalah penanda menit tepat.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Jarum panjang pada jam dinding berfungsi untuk menunjukkan ....", ["menit", "jam", "bulan", "tahun"], "A", "Jarum panjang adalah penunjuk satuan menit.")
mc("c1", "mudah", T, F, S3, "Jika jarum panjang menunjuk angka 6, artinya sudah lewat ... menit.", ["30 menit", "6 menit", "12 menit", "60 menit"], "A", "6 x 5 = 30 menit.", verifikasi={"ekspresi": "6 * 5", "hasil": "30"})
sa("c1", "mudah", T, F, S2, "Jarum pendek di 4, jarum panjang di 12. Pukul ... tepat.", "4", "Pukul 4 tepat.", verifikasi={"ekspresi": "4 - 0", "hasil": "4"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Jarum pendek di antara 7 dan 8, jarum panjang di 6 dibaca ....", ["setengah delapan", "setengah tujuh", "pukul tujuh tepat", "pukul delapan tepat"], "A", "Menuju angka 8, jadi dibaca setengah delapan.")
tf("c2", "mudah", D, Kn, S4, "Penulisan waktu pukul sembilan tepat adalah 09.30.", "Salah", "09.30 adalah setengah sepuluh, bukan sembilan tepat.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S3, "Jarum pendek di antara 3 dan 4, jarum panjang di 6. Dibaca pukul?", ["setengah empat", "setengah tiga", "setengah lima", "pukul empat tepat"], "A", "Sudah melewati 3 menuju 4, dibaca setengah empat.", "Menyebut angka yang sudah lewat pada jam setengah")
mc("c2", "mudah", R, Kn, S1, "Budi mengira jarum panjang menunjuk jam. Mengapa anggapan itu keliru?", ["karena jarum panjang menunjukkan menit", "karena jarum pendek lebih cepat", "karena jarum panjang diam", "karena warnanya merah"], "A", "Jarum penunjuk jam adalah jarum pendek.", "Tertukar fungsi jarum pendek dan jarum panjang")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Arah putaran jarum jam yang normal bergerak ke arah ....", ["kanan", "kiri", "atas saja", "bawah saja"], "A", "Jarum jam berputar searah jarum jam ke kanan.")
mc("c2", "mudah", T, Kn, S2, "Jarum pendek di 10, jarum panjang di 12. Waktu menunjukkan pukul ....", ["10.00", "12.00", "10.12", "02.00"], "A", "Ditulis 10.00.")
tf("c2", "mudah", T, Kn, S3, "Jarum panjang di angka 6 berarti jarum telah berputar setengah lingkaran.", "Benar", "Angka 6 adalah setengah dari 12 putaran penuh.")
sa("c2", "mudah", T, Kn, S4, "Pukul setengah tiga jika ditulis angka adalah 02. ... menit.", "30", "Ditulis 02.30.", verifikasi={"ekspresi": "6 * 5", "hasil": "30"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S4, "Bagaimana penulisan angka untuk waktu pukul setengah sepuluh pagi?", ["09.30", "10.30", "09.00", "10.00"], "A", "Setengah sepuluh adalah pukul 9 lewat 30 menit (09.30).", "Menulis 10.30 untuk setengah sepuluh")
mc("c3", "sedang", R, Pr, S2, "Dari pukul 08.00 sampai pukul 11.00 berselang waktu ... jam.", ["3 jam", "2 jam", "4 jam", "1 jam"], "A", "11 - 8 = 3 jam.", "Salah menghitung lama waktu jam tepat", verifikasi={"ekspresi": "11 - 8", "hasil": "3"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S2, "Kegiatan dimulai pukul 07.00 dan selesai pukul 09.00. Berapa lama kegiatan?", ["2 jam", "1 jam", "3 jam", "4 jam"], "A", "9 - 7 = 2 jam.", verifikasi={"ekspresi": "9 - 7", "hasil": "2"})
mc("c3", "mudah", T, Pr, S4, "Pukul 06.30 dibaca sebagai pukul ....", ["setengah tujuh", "setengah enam", "enam tepat", "tujuh tepat"], "A", "06.30 adalah setengah tujuh.")
tf("c3", "sedang", T, Pr, S3, "Jarum pendek di antara 11 dan 12, panjang di 6 dibaca setengah dua belas.", "Benar", "Melewati 11 menuju 12 dibaca setengah dua belas.")
mc("c3", "sedang", T, Pr, S4, "Belajar mulai pukul 08.30 dan selesai pukul 10.30. Berapa lama belajar?", ["2 jam", "1 jam", "3 jam", "4 jam"], "A", "10 - 8 = 2 jam.", verifikasi={"ekspresi": "10 - 8", "hasil": "2"})
tf("c3", "sedang", T, Pr, S2, "Pukul 01.00 sampai pukul 05.00 lamanya adalah 6 jam.", "Salah", "5 - 1 = 4 jam, bukan 6 jam.")
sa("c3", "sedang", T, Pr, S2, "Berapa jam selisih waktu antara pukul 04.00 dan pukul 10.00?", "6", "10 - 4 = 6 jam.", verifikasi={"ekspresi": "10 - 4", "hasil": "6"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Berapa kali jarum panjang berputar penuh dalam rentang waktu 3 jam?", ["3 kali", "2 kali", "4 kali", "1 kali"], "A", "Satu jam = satu putaran penuh jarum panjang.", verifikasi={"ekspresi": "3 * 1", "hasil": "3"})
mc("c3", "sedang", X, Pr, S2, "Siti tidur pukul 09.00 malam dan bangun pukul 05.00 pagi. Berapa jam Siti tidur?", ["8 jam", "7 jam", "9 jam", "6 jam"], "A", "Dari 9 ke 12 = 3 jam; dari 12 ke 5 = 5 jam; 3 + 5 = 8 jam.", verifikasi={"ekspresi": "(12 - 9) + 5", "hasil": "8"})
tf("c3", "sedang", X, Pr, S4, "Penulisan 04.30 sama artinya dengan pukul empat lewat tiga puluh menit.", "Benar", "04.30 adalah 4 lewat 30 menit.")
sa("c3", "sedang", X, Pr, S3, "Satu jam ada 60 menit. Maka setengah jam ada ... menit.", "30", "60 : 2 = 30 menit.", verifikasi={"ekspresi": "60 / 2", "hasil": "30"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Jarum pendek di antara 12 dan 1, panjang di 6. Waktu menunjukkan pukul?", ["setengah satu", "setengah dua belas", "pukul satu tepat", "pukul dua belas tepat"], "A", "Di antara 12 dan 1 menuju 1 dibaca setengah satu.")
mc("c3", "sedang", K, Pr, S4, "Lomba lari mulai pukul 07.30 dan selesai pukul 09.30. Berapa jam berlangsung?", ["2 jam", "1 jam", "3 jam", "4 jam"], "A", "9 - 7 = 2 jam.", verifikasi={"ekspresi": "9 - 7", "hasil": "2"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S1
mc("c4", "sedang", T, Kn, S1, "Mengapa jarum pendek bergerak lebih lambat daripada jarum panjang?", ["karena 1 putaran jarum pendek butuh waktu 12 jam", "karena jarum pendek lebih gemuk", "karena jarum pendek rusak", "agar baterai hemat"], "A", "Jarum pendek membutuhkan 12 jam untuk 1 putaran penuh.")
mc("c4", "sedang", T, Kn, S2, "Jarum pendek menunjuk angka 6 dan jarum panjang menunjuk 12. Pukul berapakah itu?", ["pukul 06.00 tepat", "pukul 12.00 tepat", "pukul 06.30", "pukul 12.30"], "A", "Jarum pendek di 6, panjang di 12 = pukul 06.00 tepat.")
tf("c4", "sedang", T, Kn, S3, "Pada pukul setengah empat, jarum pendek berada tepat di angka 4.", "Salah", "Jarum pendek berada di antara angka 3 dan 4, bukan tepat di 4.")
tf("c4", "sedang", T, Kn, S4, "Perbedaan antara 07.00 dan 07.30 adalah selisih waktu tiga puluh menit.", "Benar", "07.30 - 07.00 = 30 menit.")
sa("c4", "sedang", T, Kn, S2, "Dua jam setelah pukul 08.00 adalah pukul ... tepat.", "10", "8 + 2 = 10.", verifikasi={"ekspresi": "8 + 2", "hasil": "10"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Saat jarum jam berputar, jarum panjang bergerak 1 putaran. Jarum pendek berpindah?", ["berpindah 1 angka", "berpindah 2 angka", "berpindah 12 angka", "tidak bergerak"], "A", "1 jam = jarum panjang 1 putaran, jarum pendek pindah 1 angka.", verifikasi={"ekspresi": "12 / 12", "hasil": "1"})
mc("c4", "sedang", X, Kn, S3, "Manakah posisi jarum jam yang menunjukkan waktu istirahat pukul 09.30?", ["jarum pendek di antara 9 dan 10, jarum panjang di 6", "jarum pendek di 9, jarum panjang di 12", "jarum pendek di 6, jarum panjang di 9", "jarum pendek di antara 8 dan 9, jarum panjang di 6"], "A", "09.30 = pendek di antara 9 dan 10, panjang di 6.")
tf("c4", "sedang", X, Kn, S2, "Dari pukul 03.00 ke 07.00 jarum pendek bergeser sejauh 5 angka.", "Salah", "7 - 3 = 4 angka, bukan 5 angka.")
mc("c4", "sulit", X, Me, S4, "Rudi belajar dari 06.30 sampai 08.30, lalu istirahat 30 menit. Pukul berapa selesai?", ["09.00", "08.30", "09.30", "10.00"], "A", "08.30 + 30 menit = 09.00.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Berapa kali jarum panjang dan pendek bertemu tepat berimpit dalam rentang 12 jam?", ["11 kali", "12 kali", "10 kali", "24 kali"], "A", "Kedua jarum berimpit 11 kali dalam rentang 12 jam.", verifikasi={"ekspresi": "12 - 1", "hasil": "11"})
mc("c4", "sulit", K, Me, S2, "Acara dimulai pukul 10.00 dan berakhir 4 jam kemudian. Pukul berapakah itu?", ["14.00 (pukul 2 siang)", "12.00", "15.00", "13.00"], "A", "10 + 4 = 14.00 (jam 2 siang).", verifikasi={"ekspresi": "10 + 4", "hasil": "14"})
tf("c4", "sulit", K, Me, S3, "Jarum jam dinding tepat membentuk garis lurus pada pukul 03.00.", "Salah", "Pada pukul 03.00 jarum membentuk sudut siku-siku, bukan garis lurus.")
mc("c4", "sulit", K, Me, S4, "Budi mulai membaca pukul 04.30 dan selesai 90 menit kemudian. Jam berapakah itu?", ["06.00", "05.30", "06.30", "05.00"], "A", "90 menit = 1 jam 30 menit. 04.30 + 1 jam 30 menit = 06.00.")

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Jika jam dinding terlambat 30 menit, saat jam asli 08.00 jam dinding menunjuk?", ["07.30", "08.30", "08.00", "09.00"], "A", "Terlambat 30 menit = 08.00 - 30 menit = 07.30.")
mc("c5", "sedang", T, Me, S2, "Kereta berangkat pukul 06.00 dan tiba pukul 11.00. Berapa lama perjalanan?", ["5 jam", "4 jam", "6 jam", "3 jam"], "A", "11 - 6 = 5 jam.", verifikasi={"ekspresi": "11 - 6", "hasil": "5"})
mc("c5", "sedang", T, Me, S3, "Bila sekarang pukul 08.30, pukul berapa 2 jam yang lalu?", ["06.30", "07.30", "05.30", "10.30"], "A", "08.30 - 2 jam = 06.30.")
mc("c5", "sulit", T, Me, S4, "Ibu memasak dari 08.30 ke 10.00, lalu mencuci 45 menit. Pukul berapa selesai?", ["10.45", "10.30", "11.00", "10.15"], "A", "10.00 + 45 menit = 10.45.")

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Adik les musik selama 2 jam, selesai pukul 16.00. Pukul berapa adik mulai les?", ["14.00", "15.00", "13.00", "12.00"], "A", "16 - 2 = 14.00 (jam 2 siang).", verifikasi={"ekspresi": "16 - 2", "hasil": "14"})
mc("c5", "sulit", K, Me, S4, "Tiga film pendek diputar: 30 menit, 45 menit, 45 menit. Total waktu putar?", ["2 jam", "1 jam", "3 jam", "2 jam 30 menit"], "A", "30 + 45 + 45 = 120 menit = 2 jam.", verifikasi={"ekspresi": "(30 + 45 + 45) / 60", "hasil": "2"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Mengapa jam digital lebih mudah dibaca oleh anak daripada jam analog jarum?", ["karena jam digital langsung menampilkan angka jam dan menit secara jelas", "karena jam digital ada layarnya", "karena jam digital tidak pakai baterai", "tidak ada bedanya"], "A", "Jam digital langsung memperlihatkan angka tanpa perlu menafsirkan jarum.")
mc("c6", "sulit", K, Me, S4, "Satu hari ada 24 jam. Jarum pendek berputar penuh sebanyak ... kali.", ["2 kali", "1 kali", "3 kali", "4 kali"], "A", "24 : 12 = 2 kali putaran penuh jarum pendek.", verifikasi={"ekspresi": "24 / 12", "hasil": "2"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi: (3 x 4 jam) - (2 x 3 jam) + 2 jam!", ["8 jam", "6 jam", "10 jam", "7 jam"], "A", "12 - 6 + 2 = 6 + 2 = 8 jam.", verifikasi={"ekspresi": "(3 * 4) - (2 * 3) + 2", "hasil": "8"})
mc("c6", "sulit", P, Me, S3, "Sebuah jam dinding tercepat 5 menit tiap jam. Dalam 6 jam, bertambah ... menit.", ["30 menit", "25 menit", "35 menit", "20 menit"], "A", "6 x 5 = 30 menit.", verifikasi={"ekspresi": "6 * 5", "hasil": "30"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab66_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab66.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
