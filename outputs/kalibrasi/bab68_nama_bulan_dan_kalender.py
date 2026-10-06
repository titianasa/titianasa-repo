#!/usr/bin/env python3
"""
Generator dan validator Bab 68 Matematika Kelas 2 SD:
"Nama Bulan dan Kalender" (Fase A)
bab_id: 08b8abca-5f36-47c3-82c6-345af73a157b
article_id: 0ab4454e-1894-4ac8-b58e-5651933e5ee3
quiz_id: c4adbd4e-a5c7-4a8b-aff9-70729c24206a
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "m1o2q3s4u501"  # Dua Belas Bulan dalam Setahun
S2 = "n2p3r4t5v602"  # Jumlah Hari dalam Setiap Bulan
S3 = "o3q4s5u6w703"  # Membaca Lembaran Kalender
S4 = "p4r5t6v7x804"  # Menghitung Rentang Bulan dan Peristiwa

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Satu tahun terdiri dari dua belas bulan.
Nama-nama bulan berurutan teratur.
Januari, Februari, Maret, April.
Mei, Juni, Juli, Agustus.
September, Oktober, November, Desember.
Januari adalah bulan pertama.
Desember adalah bulan terakhir.
Setelah Desember, tahun berganti baru!

:::definition
title: Satu Tahun
Rentang waktu yang lamanya tepat dua belas bulan berurutan.
:::"""

s2_content = """Tiap bulan memiliki jumlah hari.
Ada bulan yang berumur 30 hari.
Ada bulan yang berumur 31 hari.
Khusus Februari umumnya 28 hari.
Empat tahun sekali menjadi 29 hari.
April, Juni, September, November berjumlah 30.
Bulan lainnya berjumlah 31 hari.
Hafalkan jumlah hari setiap bulan!

:::steps
title: Mengingat Jumlah Hari Tiap Bulan
1. Ingat bulan April, Juni, September, November (30 hari).
2. Ingat bulan Februari istimewa (28 atau 29 hari).
3. Bulan selain itu semuanya memiliki 31 hari.
:::"""

s3_content = """Kalender memuat susunan tanggal.
Tiap lembar memuat satu bulan.
Baris atas menuliskan nama hari.
Angka-angka tersusun rapi ke bawah.
Warna merah menandakan hari libur.
Kita bisa melihat hari suatu tanggal.
Cari angka tanggalnya di kalender.
Tarik pandangan ke atas melihat harinya!

:::common_trap
title: Mengira Semua Bulan Berumur Tiga Puluh Hari
Tidak semua bulan 30 hari!
Banyak bulan memiliki 31 hari.
Februari bahkan memiliki 28 hari.
Cek selalu kalender untuk kepastiannya!
:::"""

s4_content = """Kalender mencatat peristiwa penting.
Hari ulang tahun dan hari libur.
Hari Kemerdekaan Indonesia pada 17 Agustus.
Hari Pendidikan Nasional pada 2 Mei.
Kita bisa menghitung rentang bulan.
Dari Januari ke April berjarak 3 bulan.
Satu tahun sama dengan 12 bulan.
Gunakan kalender untuk merencanakan waktu!

:::callout
variant: summary
title: Ringkasan
text: Satu tahun ada 12 bulan. Kalender membantu melihat hari dan tanggal penting.
:::"""

sections = [
    {
        "id": S1,
        "title": "Dua Belas Bulan dalam Setahun",
        "minutes": 6,
        "goal": "Siswa mengenal 12 nama bulan dalam setahun secara berurutan.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Jumlah Hari dalam Setiap Bulan",
        "minutes": 6,
        "goal": "Siswa mengenal jumlah hari pada setiap bulan (28, 30, atau 31 hari).",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membaca Lembaran Kalender",
        "minutes": 6,
        "goal": "Siswa mampu membaca tanggal, hari, dan hari libur pada kalender.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menghitung Rentang Bulan dan Peristiwa",
        "minutes": 6,
        "goal": "Siswa mampu menghitung rentang waktu antarbulan dan mengingat tanggal penting.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Nama Bulan dan Kalender",
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
# 2. DEFINISI BANK 50 SOAL BAB 68
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
mc("c1", "mudah", D, F, S1, "Satu tahun terdiri dari berapa bulan?", ["12 bulan", "10 bulan", "7 bulan", "24 bulan"], "A", "1 tahun = 12 bulan.", verifikasi={"ekspresi": "12 * 1", "hasil": "12"})
tf("c1", "mudah", D, F, S1, "Bulan pertama dalam penanggalan masehi adalah bulan Januari.", "Benar", "Januari adalah bulan ke-1.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Bulan terakhir dalam satu tahun adalah bulan ....", ["Desember", "November", "Januari", "Oktober"], "A", "Desember adalah bulan ke-12.")
mc("c1", "mudah", T, F, S2, "Bulan yang memiliki jumlah hari paling sedikit adalah bulan ....", ["Februari", "April", "Juni", "Agustus"], "A", "Februari memiliki 28 atau 29 hari.")
sa("c1", "mudah", T, F, S3, "Angka bertinta merah pada kalender menandakan hari ... libur.", "libur", "Warna merah menandakan libur.")

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Bulan sesudah bulan Maret adalah bulan ....", ["April", "Mei", "Februari", "Juni"], "A", "Urutan: Januari, Februari, Maret, April.")
tf("c2", "mudah", D, Kn, S2, "Semua bulan dalam setahun memiliki jumlah hari yang sama.", "Salah", "Ada bulan yang 30 hari, 31 hari, dan Februari 28 hari.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Berapakah jumlah hari dalam bulan April?", ["30 hari", "31 hari", "28 hari", "29 hari"], "A", "April memiliki 30 hari.", "Mengira bulan April memiliki 31 hari", verifikasi={"ekspresi": "30 * 1", "hasil": "30"})
mc("c2", "mudah", R, Kn, S1, "Bulan kelima dalam urutan tahun adalah bulan ....", ["Mei", "April", "Juni", "Maret"], "A", "Bulan ke-5 adalah Mei.", "Salah mengingat urutan bulan ke-5")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Bulan sebelum bulan Agustus adalah bulan ....", ["Juli", "Juni", "September", "Oktober"], "A", "Sebelum Agustus adalah Juli.")
mc("c2", "mudah", T, Kn, S2, "Bulan berikut yang memiliki 31 hari adalah ....", ["Agustus", "Juni", "September", "April"], "A", "Agustus memiliki 31 hari.")
tf("c2", "mudah", T, Kn, S4, "Hari Kemerdekaan Indonesia diperingati setiap tanggal 17 Agustus.", "Benar", "17 Agustus adalah hari kemerdekaan.")
sa("c2", "mudah", T, Kn, S1, "Dua tahun sama dengan ... bulan.", "24", "2 x 12 = 24 bulan.", verifikasi={"ekspresi": "2 * 12", "hasil": "24"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S4, "Berapa bulan rentang waktu dari bulan Januari ke bulan Mei?", ["4 bulan", "5 bulan", "3 bulan", "2 bulan"], "A", "5 - 1 = 4 bulan.", "Menghitung dengan menyertakan kedua bulan secara keliru", verifikasi={"ekspresi": "5 - 1", "hasil": "4"})
mc("c3", "sedang", R, Pr, S1, "Ibu bekerja di luar kota selama 3 tahun. Berapa bulan itu?", ["36 bulan", "24 bulan", "48 bulan", "30 bulan"], "A", "3 x 12 = 36 bulan.", "Salah mengalikan tahun ke bulan", verifikasi={"ekspresi": "3 * 12", "hasil": "36"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Tiga bulan setelah bulan September adalah bulan ....", ["Desember", "November", "Januari", "Oktober"], "A", "September (9) + 3 = Desember (12).")
mc("c3", "mudah", T, Pr, S4, "Dari awal Maret sampai akhir Mei lamanya adalah ... bulan.", ["3 bulan", "2 bulan", "4 bulan", "1 bulan"], "A", "Maret, April, Mei = 3 bulan.", verifikasi={"ekspresi": "5 - 3 + 1", "hasil": "3"})
tf("c3", "sedang", T, Pr, S2, "Bulan Juli dan Agustus berturut-turut sama-sama memiliki 31 hari.", "Benar", "Juli 31 hari, Agustus 31 hari.")
mc("c3", "sedang", T, Pr, S3, "Jika tanggal 12 jatuh pada hari Rabu, tanggal 19 adalah hari ....", ["Rabu", "Kamis", "Selasa", "Jumat"], "A", "12 + 7 = 19, maka harinya sama yaitu Rabu.")
tf("c3", "sedang", T, Pr, S1, "Bulan ke-10 dalam penanggalan masehi adalah bulan November.", "Salah", "Bulan ke-10 adalah Oktober, November bulan ke-11.")
sa("c3", "sedang", T, Pr, S1, "Empat puluh delapan bulan sama dengan ... tahun.", "4", "48 : 12 = 4 tahun.", verifikasi={"ekspresi": "48 / 12", "hasil": "4"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S2, "Berapakah jumlah hari gabungan dari bulan Juni dan Juli?", ["61 hari", "60 hari", "62 hari", "59 hari"], "A", "Juni (30) + Juli (31) = 61 hari.", verifikasi={"ekspresi": "30 + 31", "hasil": "61"})
mc("c3", "sedang", X, Pr, S3, "Sebulan penuh ada 30 hari. Berapa minggu penuh dalam bulan itu?", ["4 minggu", "3 minggu", "5 minggu", "2 minggu"], "A", "30 : 7 = 4 minggu sisa 2 hari.", verifikasi={"ekspresi": "30 // 7", "hasil": "4"})
tf("c3", "sedang", X, Pr, S4, "Hari Sumpah Pemuda diperingati setiap tanggal 28 Oktober.", "Benar", "28 Oktober adalah Hari Sumpah Pemuda.")
sa("c3", "sedang", X, Pr, S1, "Setengah tahun sama dengan ... bulan.", "6", "12 : 2 = 6 bulan.", verifikasi={"ekspresi": "12 / 2", "hasil": "6"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Manakah kelompok bulan yang semuanya memiliki tepat 30 hari?", ["April, Juni, September", "Januari, Maret, Mei", "Juli, Agustus, Oktober", "Februari, April, Juni"], "A", "April, Juni, September semuanya 30 hari.")
mc("c3", "sedang", K, Pr, S4, "Pameran buku buka dari 10 Agustus hingga 24 Agustus. Berapa hari?", ["15 hari", "14 hari", "13 hari", "16 hari"], "A", "24 - 10 + 1 = 15 hari.", verifikasi={"ekspresi": "24 - 10 + 1", "hasil": "15"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa nama bulan dalam kalender tidak berubah urutannya setiap tahun?", ["karena peredaran bumi mengelilingi matahari berlangsung secara tetap dan teratur", "karena kalender dicetak massal", "karena pemerintah melarangnya", "supaya anak tidak bingung"], "A", "Sistem kalender didasarkan pada peredaran bumi mengelilingi matahari.")
mc("c4", "sedang", T, Kn, S2, "Apa yang membedakan tahun kabisat dengan tahun biasa?", ["bulan Februari memiliki 29 hari", "bulan Januari memiliki 32 hari", "satu tahun hanya 11 bulan", "semua bulan menjadi 30 hari"], "A", "Tahun kabisat menambah 1 hari di Februari (29 hari).")
tf("c4", "sedang", T, Kn, S3, "Jika tanggal 1 jatuh hari Minggu, tanggal 29 pasti hari Minggu.", "Benar", "1 + 7 + 7 + 7 + 7 = 29.")
tf("c4", "sedang", T, Kn, S4, "Rentang dari bulan Mei ke bulan Agustus lamanya tepat 5 bulan.", "Salah", "8 - 5 = 3 bulan, bukan 5 bulan.")
sa("c4", "sedang", T, Kn, S1, "Berapa bulan selisih waktu antara 3 tahun dan 26 bulan?", "10", "(3 x 12) - 26 = 36 - 26 = 10 bulan.", verifikasi={"ekspresi": "(3 * 12) - 26", "hasil": "10"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S3, "Sebuah bulan diawali hari Senin dan berakhir 31 hari. Berapa hari Senin?", ["5 hari Senin", "4 hari Senin", "6 hari Senin", "3 hari Senin"], "A", "Tanggal 1, 8, 15, 22, 29 = 5 hari Senin.", verifikasi={"ekspresi": "(31 // 7) + 1", "hasil": "5"})
mc("c4", "sedang", X, Kn, S4, "Lani lahir 15 Maret 2016. Pada 15 Maret 2024, umur Lani adalah?", ["8 tahun", "7 tahun", "9 tahun", "10 tahun"], "A", "2024 - 2016 = 8 tahun.", verifikasi={"ekspresi": "2024 - 2016", "hasil": "8"})
tf("c4", "sedang", X, Kn, S2, "Gabungan hari bulan Januari dan Februari biasa adalah 60 hari.", "Salah", "31 + 28 = 59 hari, bukan 60 hari.")
mc("c4", "sulit", X, Me, S4, "Kursus melukis berlangsung 1,5 tahun. Berapa bulan lama kursus tersebut?", ["18 bulan", "15 bulan", "20 bulan", "16 bulan"], "A", "12 + 6 = 18 bulan.", verifikasi={"ekspresi": "12 + 6", "hasil": "18"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Jika sekarang bulan November, bulan apakah 5 bulan yang lalu?", ["Juni", "Mei", "Juli", "April"], "A", "11 - 5 = 6 (Juni).")
mc("c4", "sulit", K, Me, S2, "Dalam setahun biasa (365 hari), berapa jumlah minggu dan sisa hari?", ["52 minggu lebih 1 hari", "50 minggu lebih 5 hari", "52 minggu tepat", "51 minggu"], "A", "365 : 7 = 52 sisa 1 hari.")
tf("c4", "sulit", K, Me, S3, "Bulan berumur 31 hari selalu memiliki 5 hari libur akhir pekan.", "Salah", "Jumlah akhir pekan tergantung hari dimulainya tanggal 1.")
mc("c4", "sulit", K, Me, S4, "Proyek dimulai 1 Februari dan selesai 30 April tahun biasa. Berapa hari?", ["89 hari", "90 hari", "88 hari", "91 hari"], "A", "28 + 31 + 30 = 89 hari.", verifikasi={"ekspresi": "28 + 31 + 30", "hasil": "89"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Jika sekarang bulan Oktober, bulan apakah 7 bulan yang akan datang?", ["Mei", "April", "Juni", "Maret"], "A", "(10 + 7) - 12 = 17 - 12 = 5 (Mei).")
mc("c5", "sedang", T, Me, S2, "Berapa total hari dalam caturwulan pertama (Januari sampai April biasa)?", ["120 hari", "119 hari", "121 hari", "118 hari"], "A", "31 + 28 + 31 + 30 = 120 hari.", verifikasi={"ekspresi": "31 + 28 + 31 + 30", "hasil": "120"})
mc("c5", "sedang", T, Me, S3, "Tanggal 4 jatuh hari Selasa. Tanggal berapakah hari Selasa keempat bulan itu?", ["tanggal 25", "tanggal 24", "tanggal 26", "tanggal 27"], "A", "Selasa 1: 4, ke-2: 11, ke-3: 18, ke-4: 25.", verifikasi={"ekspresi": "4 + (3 * 7)", "hasil": "25"})
mc("c5", "sulit", T, Me, S4, "Pak Rudi menabung tiap bulan Rp100.000 selama 2 tahun. Berapa tabungan Pak Rudi?", ["Rp2.400.000", "Rp2.000.000", "Rp1.200.000", "Rp2.200.000"], "A", "2 x 12 = 24 bulan x 100.000 = Rp2.400.000.")

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Bila seseorang lahir bulan Desember, bulan apakah ia merayakan ulang tahun ke-18 bulan?", ["Juni", "Mei", "Juli", "Agustus"], "A", "18 bulan = 1 tahun 6 bulan. Desember + 6 bulan = Juni.")
mc("c5", "sulit", K, Me, S4, "Doni berusia 8 tahun 4 bulan. Sinta berusia 6 tahun 9 bulan. Selisih usia?", ["19 bulan", "20 bulan", "18 bulan", "21 bulan"], "A", "Doni = 100 bulan, Sinta = 81 bulan. Selisih = 19 bulan.", verifikasi={"ekspresi": "((8 * 12) + 4) - ((6 * 12) + 9)", "hasil": "19"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Mengapa kalender kabisat terjadi setiap 4 tahun sekali?", ["karena bumi mengitari matahari butuh 365 seperempat hari, sisa seperempat dikumpulkan", "agar tahun genap", "karena permintaan astronom", "tidak ada alasan"], "A", "Kelebihan 0,25 hari tiap tahun genap menjadi 1 hari tiap 4 tahun.")
mc("c6", "sulit", K, Me, S3, "Suatu bulan dimulai hari Sabtu dan ada 31 hari. Berapa hari Minggu di bulan itu?", ["5 hari Minggu", "4 hari Minggu", "6 hari Minggu", "3 hari Minggu"], "A", "Minggu jatuh pada tanggal 2, 9, 16, 23, 30 (total 5 hari).", verifikasi={"ekspresi": "(31 - 1) // 7 + 1", "hasil": "5"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Hitunglah hasil operasi waktu: (3 x 12 bulan) - (2 x 10 bulan) + 8 bulan!", ["24 bulan", "22 bulan", "26 bulan", "20 bulan"], "A", "36 - 20 + 8 = 16 + 8 = 24 bulan.", verifikasi={"ekspresi": "(3 * 12) - (2 * 10) + 8", "hasil": "24"})
mc("c6", "sulit", P, Me, S4, "Dua balita: Balita A (32 bulan), Balita B (2 tahun 5 bulan). Selisih usia?", ["3 bulan", "2 bulan", "4 bulan", "1 bulan"], "A", "Balita B = 29 bulan. Selisih = 32 - 29 = 3 bulan.", verifikasi={"ekspresi": "32 - ((2 * 12) + 5)", "hasil": "3"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab68_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab68.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
