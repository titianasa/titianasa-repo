#!/usr/bin/env python3
"""
Generator dan validator Bab 69 Matematika Kelas 2 SD:
"Waktu Kegiatan Sehari-hari" (Fase A)
bab_id: 3dc5d6a0-4ecd-4df6-8655-3477084bdd63
article_id: 28e5a6a3-c7c8-48a6-ac4b-0d4610c475be
quiz_id: 3814a3f0-c7f6-4268-9df8-b32fa8c503fa
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "n1p2r3t4v501"  # Jadwal Pagi, Siang, Sore, dan Malam
S2 = "o2q3s4u5w602"  # Membaca Waktu Kegiatan Sehari-hari
S3 = "p3r4t5v6x703"  # Menghitung Durasi / Lama Kegiatan
S4 = "q4s5u6w7y804"  # Menentukan Waktu Mulai atau Selesai

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Hari kita terbagi menjadi beberapa bagian.
Ada pagi, siang, sore, dan malam.
Pagi hari kita bangun dan sarapan.
Lalu kita berangkat ke sekolah.
Siang hari kita pulang sekolah.
Sore hari kita bermain bersama teman.
Malam hari kita belajar dan tidur.
Semua kegiatan memiliki waktunya sendiri!

:::definition
title: Pembagian Waktu
Pagi (terbit fajar), siang (matahari terik), sore (matahari condong), dan malam (gelap).
:::"""

s2_content = """Setiap kegiatan dicatat dengan jam.
Pukul 05.00 pagi kita bangun tidur.
Pukul 07.00 pagi sekolah dimulai.
Pukul 09.30 kita istirahat makan bekal.
Pukul 12.00 siang pelajaran selesai.
Pukul 19.00 malam kita makan malam.
Pukul 21.00 malam kita tidur nyenyak.
Jam membantu kegiatan teratur!

:::steps
title: Membaca Jam Kegiatan
1. Lihat kegiatan yang sedang dilakukan.
2. Periksa posisi jarum jam dinding.
3. Sebutkan waktu dengan keterangan pagi atau malam.
:::"""

s3_content = """Berapa lama suatu kegiatan berlangsung?
Lama kegiatan disebut durasi.
Siti mulai belajar pukul 08.00.
Siti selesai belajar pukul 10.00.
Berapa lama Siti belajar?
Kurangi waktu selesai dengan mulai.
10 dikurang 8 adalah 2.
Jadi Siti belajar selama 2 jam!

:::common_trap
title: Menjumlahkan Waktu Saat Mencari Durasi
Mencari lama waktu menggunakan pengurangan.
Bukan penjumlahan waktu!
Kurangkan jam selesai dengan jam mulai.
:::"""

s4_content = """Kita bisa mencari jam selesai.
Budi bermain mulai pukul 15.00.
Budi bermain selama 2 jam.
Pukul berapa Budi selesai bermain?
Jumlahkan waktu mulai dan durasi.
15 ditambah 2 adalah 17.
Maka Budi selesai pukul 17.00 sore.
Atau pukul 5 sore!

:::callout
variant: summary
title: Ringkasan
text: Durasi = selesai - mulai. Waktu selesai = mulai + durasi.
:::"""

sections = [
    {
        "id": S1,
        "title": "Jadwal Pagi, Siang, Sore, dan Malam",
        "minutes": 6,
        "goal": "Siswa mengenal bagian hari dan waktu kegiatan yang sesuai.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Membaca Waktu Kegiatan Sehari-hari",
        "minutes": 6,
        "goal": "Siswa mampu membaca jam kegiatan rutin harian dengan tepat.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Menghitung Durasi / Lama Kegiatan",
        "minutes": 6,
        "goal": "Siswa mampu menghitung lama waktu kegiatan (waktu selesai dikurang mulai).",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menentukan Waktu Mulai atau Selesai",
        "minutes": 6,
        "goal": "Siswa mampu menentukan waktu mulai atau selesai bila durasi diketahui.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Waktu Kegiatan Sehari-hari",
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
# 2. DEFINISI BANK 50 SOAL BAB 69
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
mc("c1", "mudah", D, F, S1, "Kegiatan sarapan pagi umumnya dilakukan pada waktu ....", ["pagi hari", "malam hari", "sore hari", "tengah malam"], "A", "Sarapan dilakukan pada pagi hari.")
tf("c1", "mudah", D, F, S2, "Pukul 07.00 pagi biasanya siswa memulai kegiatan belajar di sekolah.", "Benar", "Sekolah umumnya dimulai pukul 07.00 pagi.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Kegiatan tidur malam yang baik biasanya dimulai pada waktu ....", ["malam hari", "siang terik", "pagi hari", "subuh"], "A", "Tidur malam dilakukan pada malam hari.")
mc("c1", "mudah", T, F, S2, "Pukul 12.00 siang saat matahari tepat di atas kepala disebut ....", ["tengah hari", "subuh", "senja", "tengah malam"], "A", "Pukul 12.00 adalah tengah hari.")
sa("c1", "mudah", T, F, S3, "Mulai pukul 08.00 selesai pukul 10.00. Lamanya adalah ... jam.", "2", "10 - 8 = 2 jam.", verifikasi={"ekspresi": "10 - 8", "hasil": "2"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Budi membaca buku dari 08.00 sampai 09.00. Lama membaca?", ["1 jam", "2 jam", "3 jam", "30 menit"], "A", "9 - 8 = 1 jam.", verifikasi={"ekspresi": "9 - 8", "hasil": "1"})
tf("c2", "mudah", D, Kn, S4, "Jika mulai 09.00 dan bermain 2 jam, selesai pukul 11.00.", "Benar", "9 + 2 = 11.00.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S3, "Lani les menari dari 15.00 ke 17.00. Berapa jam Lani les?", ["2 jam", "32 jam", "3 jam", "1 jam"], "A", "17 - 15 = 2 jam.", "Menjumlahkan jam mulai dan jam selesai", verifikasi={"ekspresi": "17 - 15", "hasil": "2"})
mc("c2", "mudah", R, Kn, S4, "Belajar mulai pukul 07.00 selama 3 jam. Selesai pukul berapa?", ["10.00", "04.00", "09.00", "11.00"], "A", "7 + 3 = 10.00.", "Mengurangkan waktu saat mencari waktu selesai", verifikasi={"ekspresi": "7 + 3", "hasil": "10"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Matahari terbenam di ufuk barat menandakan tibanya waktu ....", ["sore menuju malam", "pagi hari", "siang terik", "tengah hari"], "A", "Matahari terbenam terjadi pada waktu sore.")
mc("c2", "mudah", T, Kn, S2, "Kegiatan upacara bendera hari Senin biasanya dilakukan pukul ....", ["07.00 pagi", "13.00 siang", "19.00 malam", "21.00 malam"], "A", "Upacara bendera dilakukan pukul 07.00 pagi.")
tf("c2", "mudah", T, Kn, S3, "Kegiatan dari 08.00 ke 12.00 berlangsung selama 5 jam.", "Salah", "12 - 8 = 4 jam, bukan 5 jam.")
sa("c2", "mudah", T, Kn, S4, "Mulai jam 06.00 berjalan pagi 1 jam. Selesai jam ... tepat.", "7", "6 + 1 = 7.", verifikasi={"ekspresi": "6 + 1", "hasil": "7"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Upacara mulai 07.00 selesai 07.30. Berapa menit lama upacara?", ["30 menit", "60 menit", "10 menit", "45 menit"], "A", "07.30 - 07.00 = 30 menit.", "Salah menghitung durasi pecahan jam", verifikasi={"ekspresi": "30 * 1", "hasil": "30"})
mc("c3", "sedang", R, Pr, S4, "Selesai memasak pukul 11.00, memasak selama 2 jam. Mulai pukul?", ["09.00", "13.00", "08.00", "10.00"], "A", "11 - 2 = 09.00.", "Menjumlahkan waktu untuk mencari waktu mulai", verifikasi={"ekspresi": "11 - 2", "hasil": "9"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S3, "Ibu mencuci dari pukul 08.00 sampai 11.00. Berapa jam lama ibu mencuci?", ["3 jam", "2 jam", "4 jam", "1 jam"], "A", "11 - 8 = 3 jam.", verifikasi={"ekspresi": "11 - 8", "hasil": "3"})
mc("c3", "mudah", T, Pr, S4, "Rudi mulai berenang pukul 14.00 selama 2 jam. Selesai pukul ....", ["16.00", "15.00", "17.00", "18.00"], "A", "14 + 2 = 16.00.", verifikasi={"ekspresi": "14 + 2", "hasil": "16"})
tf("c3", "sedang", T, Pr, S1, "Waktu tidur malam selama 8 jam adalah waktu istirahat yang sehat.", "Benar", "Anak usia SD disarankan tidur 8-9 jam sehari.")
mc("c3", "sedang", T, Pr, S3, "Bimbel mulai 15.30 dan selesai 17.30. Berapa jam bimbel berlangsung?", ["2 jam", "1 jam", "3 jam", "4 jam"], "A", "17 - 15 = 2 jam.", verifikasi={"ekspresi": "17 - 15", "hasil": "2"})
tf("c3", "sedang", T, Pr, S4, "Mulai jam 08.30 dan belajar 1 jam selesai pukul 10.30.", "Salah", "08.30 + 1 jam = 09.30, bukan 10.30.")
sa("c3", "sedang", T, Pr, S3, "Latihan pramuka dari 14.00 ke 17.00 berlangsung selama ... jam.", "3", "17 - 14 = 3 jam.", verifikasi={"ekspresi": "17 - 14", "hasil": "3"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S2, "Kegiatan membersihkan rumah dari 07.30 sampai 09.30 berlangsung selama ....", ["2 jam", "1 jam", "3 jam", "4 jam"], "A", "9 - 7 = 2 jam.", verifikasi={"ekspresi": "9 - 7", "hasil": "2"})
mc("c3", "sedang", X, Pr, S3, "Perjalanan bus mulai 06.00 dan tiba 10.00. Lama perjalanan bus?", ["4 jam", "3 jam", "5 jam", "6 jam"], "A", "10 - 6 = 4 jam.", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})
tf("c3", "sedang", X, Pr, S4, "Jika mulai makan siang pukul 12.00 selama 30 menit, selesai pukul 12.30.", "Benar", "12.00 + 30 menit = 12.30.")
sa("c3", "sedang", X, Pr, S4, "Selesai main jam 18.00 setelah main 3 jam. Mulai jam ... sore.", "15", "18 - 3 = 15.00 (jam 3 sore).", verifikasi={"ekspresi": "18 - 3", "hasil": "15"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Kakak belajar dari 19.00 sampai 21.00. Berapa menit lama belajar kakak?", ["120 menit", "60 menit", "90 menit", "180 menit"], "A", "21 - 19 = 2 jam = 120 menit.", verifikasi={"ekspresi": "(21 - 19) * 60", "hasil": "120"})
mc("c3", "sedang", K, Pr, S4, "Ayah bekerja bakti dari 07.00 selama 4 jam. Pukul berapa ayah selesai?", ["11.00", "10.00", "12.00", "09.00"], "A", "7 + 4 = 11.00.", verifikasi={"ekspresi": "7 + 4", "hasil": "11"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S3
mc("c4", "sedang", T, Kn, S1, "Mengapa penting mengatur jadwal waktu kegiatan sehari-hari secara disiplin?", ["agar tubuh tetap sehat dan semua tugas selesai tepat waktu", "supaya tidak perlu tidur", "agar jam dinding tidak rusak", "supaya hari cepat berlalu"], "A", "Disiplin jadwal menjaga kesehatan dan keteraturan hidup.")
mc("c4", "sedang", T, Kn, S2, "Kegiatan A (08.00-11.00) dan Kegiatan B (13.00-15.00). Manakah lebih lama?", ["kegiatan A karena berlangsung 3 jam", "kegiatan B karena 2 jam", "keduanya sama", "tidak dapat dihitung"], "A", "A = 3 jam, B = 2 jam. 3 jam > 2 jam.")
tf("c4", "sedang", T, Kn, S3, "Dua kegiatan masing-masing 90 menit sama totalnya dengan 3 jam.", "Benar", "90 + 90 = 180 menit = 3 jam.")
tf("c4", "sedang", T, Kn, S4, "Mulai pukul 10.30 selama 2 jam 30 menit akan selesai pada pukul 12.00.", "Salah", "10.30 + 2 jam 30 menit = 13.00, bukan 12.00.")
sa("c4", "sedang", T, Kn, S3, "Selisih durasi antara kegiatan 4 jam dan kegiatan 90 menit adalah ... menit.", "150", "(4 x 60) - 90 = 240 - 90 = 150 menit.", verifikasi={"ekspresi": "(4 * 60) - 90", "hasil": "150"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S3, "Dodi tidur siang dari 13.00 sampai 14.30. Berapa menit Dodi tidur?", ["90 menit", "60 menit", "75 menit", "120 menit"], "A", "1 jam 30 menit = 60 + 30 = 90 menit.", verifikasi={"ekspresi": "60 + 30", "hasil": "90"})
mc("c4", "sedang", X, Kn, S4, "Pentas seni mulai 09.00. Ada 3 sesi masing-masing 1 jam. Selesai pukul?", ["12.00", "11.00", "13.00", "10.00"], "A", "9 + 3 = 12.00.", verifikasi={"ekspresi": "9 + 3", "hasil": "12"})
tf("c4", "sedang", X, Kn, S1, "Tidur siang selama 1 jam membuat tubuh anak bertambah lemas dan lelah.", "Salah", "Tidur siang sejenak justru memulihkan tenaga dan kesegaran tubuh.")
mc("c4", "sulit", X, Me, S3, "Siti les matematika 1 jam, istirahat 15 menit, lalu les bahasa 45 menit. Total?", ["2 jam", "1 jam 45 menit", "2 jam 15 menit", "1 jam 30 menit"], "A", "60 + 15 + 45 = 120 menit = 2 jam.", verifikasi={"ekspresi": "(60 + 15 + 45) / 60", "hasil": "2"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Jika istirahat sekolah pukul 09.30 selama 30 menit, bel masuk kembali pukul?", ["10.00", "09.50", "10.30", "09.45"], "A", "09.30 + 30 menit = 10.00.")
mc("c4", "sulit", K, Me, S3, "Kereta berangkat 07.15 dan tiba 10.15. Berapa menit perjalanan kereta?", ["180 menit", "150 menit", "200 menit", "120 menit"], "A", "3 jam = 3 x 60 = 180 menit.", verifikasi={"ekspresi": "(10 - 7) * 60", "hasil": "180"})
tf("c4", "sulit", K, Me, S4, "Jika kegiatan selesai pukul 16.00 setelah 5 jam, kegiatan dimulai pukul 10.00.", "Salah", "16 - 5 = 11.00, bukan 10.00.")
mc("c4", "sulit", K, Me, S4, "Ujian berlangsung 2 jam. Selesai pukul 10.30. Pukul berapa ujian dimulai?", ["08.30", "09.00", "08.00", "07.30"], "A", "10.30 - 2 jam = 08.30.")

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Edo belajar 2 jam sore dan 1 jam malam tiap hari. Berapa jam dalam 5 hari?", ["15 jam", "12 jam", "10 jam", "20 jam"], "A", "(2 + 1) x 5 = 3 x 5 = 15 jam.", verifikasi={"ekspresi": "(2 + 1) * 5", "hasil": "15"})
mc("c5", "sedang", T, Me, S2, "Matematika selesai 08.30, istirahat 30 menit, lalu IPA 1 jam. Selesai pukul?", ["10.00", "09.30", "10.30", "11.00"], "A", "08.30 + 30 menit + 1 jam = 10.00.")
mc("c5", "sedang", T, Me, S3, "Lomba lari A butuh 45 menit, lomba B butuh 75 menit. Berapa jam keduanya?", ["2 jam", "1 jam 30 menit", "2 jam 30 menit", "3 jam"], "A", "45 + 75 = 120 menit = 2 jam.", verifikasi={"ekspresi": "(45 + 75) / 60", "hasil": "2"})
mc("c5", "sulit", T, Me, S4, "Film mulai 19.30 durasi 105 menit. Pukul berapa film tersebut selesai?", ["21.15", "21.00", "21.30", "20.45"], "A", "105 menit = 1 jam 45 menit. 19.30 + 1 jam 45 mnt = 21.15.")

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Tiga anak main bergantian: A (20 mnt), B (35 mnt), C (25 mnt). Selesai berapa mnt?", ["80 menit", "75 menit", "90 menit", "70 menit"], "A", "20 + 35 + 25 = 80 menit.", verifikasi={"ekspresi": "20 + 35 + 25", "hasil": "80"})
mc("c5", "sulit", K, Me, S4, "Perjalanan 4 jam istirahat 30 menit. Berangkat 06.30, tiba pukul berapa?", ["11.00", "10.30", "11.30", "10.00"], "A", "06.30 + 4 jam 30 menit = 11.00.")

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Mengapa pembagian waktu 24 jam internasional menggunakan format 00.00 hingga 23.59?", ["agar membedakan waktu siang dan malam secara pasti tanpa tertukar", "karena angkanya lebih banyak", "agar jam lebih besar", "tidak ada gunanya"], "A", "Format 24 jam mencegah kebingungan antara jam pagi dan malam.")
mc("c6", "sulit", K, Me, S3, "Dua pekerja: Pekerja A kerja 7 jam, Pekerja B kerja 450 menit. Siapa lebih lama?", ["Pekerja B karena 450 menit = 7,5 jam", "Pekerja A", "keduanya sama", "tidak dapat dihitung"], "A", "Pekerja B = 450 : 60 = 7,5 jam. 7,5 > 7 jam.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Hitung total jam: (4 x 45 menit) + (2 x 90 menit)!", ["6 jam", "5 jam", "7 jam", "4 jam"], "A", "(4 x 45) + (2 x 90) = 180 + 180 = 360 menit = 6 jam.", verifikasi={"ekspresi": "((4 * 45) + (2 * 90)) / 60", "hasil": "6"})
mc("c6", "sulit", P, Me, S4, "Pak guru mengajar 3 kelas masing-masing 70 menit, istirahat 10 mnt tiap jeda. Total?", ["230 menit", "210 menit", "240 menit", "220 menit"], "A", "(3 x 70) + (2 x 10) = 210 + 20 = 230 menit.", verifikasi={"ekspresi": "(3 * 70) + (2 * 10)", "hasil": "230"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab69_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab69.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
