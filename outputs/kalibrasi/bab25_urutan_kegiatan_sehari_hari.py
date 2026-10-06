#!/usr/bin/env python3
"""
Generator dan validator Bab 25 Matematika Kelas 1 SD:
"Urutan Kegiatan Sehari-hari: Pagi, Siang, Malam" (Fase A)
bab_id: b429b476-3987-451c-8f38-7ca8db5bacec
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "b1c2d33e4f01"  # Kegiatan di Waktu Pagi Hari
S2 = "c2d3e44f5a12"  # Kegiatan Siang dan Sore Hari
S3 = "d3e4f55a6b23"  # Kegiatan di Waktu Malam Hari
S4 = "e4f5a66b7c34"  # Mengenal Durasi Sebentar dan Lama

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Pagi hari matahari mulai terbit.
Langit tampak mulai terang.
Udara terasa sejuk dan segar.
Kita bangun tidur tepat waktu.
Merapikan tempat tidur sendiri.
Mandi lalu sarapan pagi bergizi.
Kita berangkat ke sekolah.
Semua dilakukan di waktu pagi.

:::definition
title: Waktu Pagi
Pagi hari dimulai saat matahari terbit di timur.
Kegiatan pagi meliputi bangun, sarapan, dan berangkat sekolah.
:::"""

s2_content = """Matahari tepat di atas kepala.
Udara siang terasa cukup panas.
Kita pulang dari sekolah.
Berganti baju dan cuci tangan.
Makan siang bersama keluarga.
Lalu istirahat sejenak di rumah.
Saat sore udara mulai sejuk.
Anak-anak boleh bermain bersama teman.

:::steps
title: Urutan Siang dan Sore
1. Pulang dari sekolah saat siang.
2. Makan siang lalu istirahat sejenak.
3. Bermain bersama teman pada sore hari.
:::"""

s3_content = """Matahari terbenam di ufuk barat.
Langit mulai menjadi gelap gulita.
Bulan dan bintang mulai terlihat.
Lampu di rumah mulai dinyalakan.
Kita makan malam bersama keluarga.
Belajar dan mengulang pelajaran sekolah.
Kemudian kita tidur malam nyenyak.
Tubuh beristirahat sampai esok pagi."""

s4_content = """Setiap kegiatan butuh waktu berbeda.
Ada kegiatan yang berlangsung sebentar.
Mencuci tangan butuh waktu sebentar.
Ada juga kegiatan yang lama.
Tidur malam butuh waktu lama.

:::common_trap
title: Membedakan Sebentar dan Lama
Meyeduh teh butuh waktu sebentar.
Belajar di sekolah butuh waktu lama.
Jangan terbalik membedakan durasi waktu.
Kegiatan cepat selesai adalah sebentar.
Kegiatan panjang adalah lama.
:::

:::callout
variant: summary
title: Ringkasan
text: Hari dibagi menjadi pagi, siang, sore, dan malam. Ada kegiatan sebentar dan ada kegiatan lama.
:::"""

sections = [
    {
        "id": S1,
        "title": "Kegiatan di Waktu Pagi Hari",
        "minutes": 6,
        "goal": "Siswa mengenal tanda-tanda pagi hari dan contoh urutan kegiatan rutin di waktu pagi.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Kegiatan Siang dan Sore Hari",
        "minutes": 6,
        "goal": "Siswa mengenal tanda-tanda waktu siang serta sore dan kegiatan rutin yang biasa dilakukan.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Kegiatan di Waktu Malam Hari",
        "minutes": 6,
        "goal": "Siswa mengenal tanda-tanda malam hari dan kegiatan istirahat yang dilakukan di malam hari.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Mengenal Durasi Sebentar dan Lama",
        "minutes": 6,
        "goal": "Siswa dapat membedakan durasi kejadian yang berlangsung sebentar atau lama dalam keseharian.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Urutan Kegiatan Sehari-hari: Pagi, Siang, Malam",
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
# 2. DEFINISI BANK 50 SOAL BAB 25
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
mc("c1", "mudah", D, F, S1, "Matahari terbit di sebelah timur pada waktu ....", ["pagi hari", "malam hari", "tengah malam", "sore hari"], "A", "Matahari terbit menandakan datangnya waktu pagi hari.")
tf("c1", "mudah", D, F, S4, "Mencuci tangan berlangsung lebih sebentar daripada tidur malam.", "Benar", "Cuci tangan hanya butuh beberapa detik, tidur malam berjam-jam.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Kegiatan yang biasa kita lakukan saat siang hari adalah ....", ["pulang sekolah", "tidur malam", "melihat bintang", "sarapan pagi"], "A", "Siswa pulang dari sekolah saat siang hari.")
mc("c1", "mudah", T, F, S3, "Benda langit yang tampak menerangi malam hari adalah ....", ["bulan dan bintang", "matahari terik", "pelangi siang", "awan cerah"], "A", "Bulan dan bintang tampak bersinar pada malam hari.")
sa("c1", "mudah", T, F, S1, "Pukul berapa anak sekolah bangun pagi jika bangun jam 5?", "5", "Bangun pagi pukul 5.", verifikasi={"ekspresi": "5", "hasil": "5"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Manakah contoh kegiatan yang berlangsung sangat sebentar?", ["mengedipkan mata", "belajar di sekolah", "tidur semalaman", "menanam padi"], "A", "Mengedipkan mata berlangsung sangat cepat dalam sekejap.")
tf("c2", "mudah", D, Kn, S2, "Saat siang hari matahari berada tepat di atas kepala kita.", "Benar", "Matahari berada di posisi tertinggi saat tengah hari.")

# Remedial (2)
mc("c2", "mudah", R, F, S1, "Sebelum berangkat ke sekolah pada pagi hari, kita sebaiknya ....", ["sarapan pagi", "tidur malam", "melihat bintang", "menyalakan lilin"], "A", "Sarapan pagi penting memberi tenaga sebelum belajar.", "Melewatkan sarapan sebelum berangkat sekolah")
mc("c2", "mudah", R, Kn, S4, "Memakai sepatu membutuhkan waktu yang lebih .... daripada membaca satu buku tebal.", ["sebentar", "lama", "banyak", "jauh"], "A", "Memakai sepatu cepat selesai, membaca buku tebal butuh waktu lama.", "Tertukar durasi sebentar dan lama")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Budi sarapan 15 menit. Mandi 10 menit. Berapa menit selisih waktunya?", ["5 menit", "4 menit", "6 menit", "3 menit"], "A", "15 - 10 = 5 menit.", verifikasi={"ekspresi": "15 - 10", "hasil": "5"})
mc("c2", "mudah", T, Kn, S2, "Doni bermain bola 2 jam di sore hari. Jam main adik 1 jam. Berapa jumlah jamnya?", ["3 jam", "2 jam", "4 jam", "1 jam"], "A", "2 + 1 = 3 jam.", verifikasi={"ekspresi": "2 + 1", "hasil": "3"})
tf("c2", "mudah", T, Kn, S3, "Matahari terbenam di ufuk barat menandakan malam akan tiba.", "Benar", "Terbenamnya matahari menandai berakhirnya siang dan datangnya malam.")
sa("c2", "mudah", T, Kn, S4, "Berapa jam Siti tidur jika tidur dari jam 9 sampai jam 5 pagi?", "8", "Durasi tidur adalah 8 jam.", verifikasi={"ekspresi": "8", "hasil": "8"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Urutan kegiatan setelah pulang sekolah yang tepat adalah ....", ["ganti baju lalu cuci tangan dan makan siang", "langsung tidur tanpa melepas sepatu", "bermain bola tanpa ganti seragam", "makan malam"], "A", "Ganti baju, cuci tangan, baru makan siang.", "Melakukan aktivitas tanpa berganti pakaian seragam")
mc("c3", "sedang", R, Pr, S3, "Urutan kegiatan malam sebelum tidur yang benar adalah ....", ["belajar lalu gosok gigi kemudian tidur", "tidur lalu belajar", "makan sarapan lalu tidur", "berangkat sekolah"], "A", "Belajar, menggosok gigi, lalu tidur nyenyak.", "Urutan kegiatan malam tertukar")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Edo belajar 3 jam di pagi hari dan 2 jam di sore hari. Total jam belajar?", ["5 jam", "4 jam", "6 jam", "3 jam"], "A", "3 + 2 = 5 jam.", verifikasi={"ekspresi": "3 + 2", "hasil": "5"})
mc("c3", "sedang", T, Pr, S2, "Siti istirahat siang 2 jam. Kakak istirahat 1 jam. Berapa selisih jam istirahat?", ["1 jam", "2 jam", "3 jam", "0 jam"], "A", "2 - 1 = 1 jam.", verifikasi={"ekspresi": "2 - 1", "hasil": "1"})
tf("c3", "sedang", T, Pr, S3, "Belajar di sekolah berlangsung lebih sebentar daripada minum segelas air.", "Salah", "Belajar di sekolah berlangsung berjam-jam (lama), minum hanya sebentar.")
mc("c3", "sedang", T, Pr, S4, "Lari pagi butuh 30 menit. Minum butuh 5 menit. Selisih waktunya adalah ....", ["25 menit", "20 menit", "35 menit", "15 menit"], "A", "30 - 5 = 25 menit.", verifikasi={"ekspresi": "30 - 5", "hasil": "25"})
tf("c3", "sedang", T, Pr, S1, "Udara pada pagi hari terasa jauh lebih panas daripada siang hari.", "Salah", "Pagi hari udara masih sejuk, siang hari terasa lebih panas.")
sa("c3", "mudah", T, Pr, S3, "Rani belajar malam selama 2 jam. Kakak belajar 3 jam. Berapa total jam belajar?", "5", "2 + 3 = 5 jam.", verifikasi={"ekspresi": "2 + 3", "hasil": "5"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Udin menyiapkan buku 10 menit. Sarapan 15 menit. Berapa menit total waktu?", ["25 menit", "20 menit", "30 menit", "15 menit"], "A", "10 + 15 = 25 menit.", verifikasi={"ekspresi": "10 + 15", "hasil": "25"})
mc("c3", "sedang", X, Pr, S2, "Kakak membaca buku 40 menit di sore hari. Adik 20 menit. Berapa selisih menitnya?", ["20 menit", "10 menit", "30 menit", "15 menit"], "A", "40 - 20 = 20 menit.", verifikasi={"ekspresi": "40 - 20", "hasil": "20"})
tf("c3", "sedang", X, Pr, S3, "Kita melihat matahari bersinar terang di langit saat tengah malam.", "Salah", "Tengah malam matahari tidak tampak di langit.")
sa("c3", "sedang", X, Pr, S4, "Perjalanan ke sekolah butuh 15 menit. Jalan kaki pulang 15 menit. Total menit?", "30", "15 + 15 = 30 menit.", verifikasi={"ekspresi": "15 + 15", "hasil": "30"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Dina tidur 8 jam. Adik tidur 10 jam. Berapa jam selisih waktu tidur mereka?", ["2 jam", "1 jam", "3 jam", "4 jam"], "A", "10 - 8 = 2 jam.", verifikasi={"ekspresi": "10 - 8", "hasil": "2"})
mc("c3", "sedang", K, Pr, S3, "Makan malam 20 menit. Mengulang pelajaran 40 menit. Berapa menit total waktu malam?", ["60 menit", "50 menit", "70 menit", "40 menit"], "A", "20 + 40 = 60 menit.", verifikasi={"ekspresi": "20 + 40", "hasil": "60"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Urutan pergantian waktu dalam satu hari yang benar adalah ....", ["pagi, siang, sore, malam", "siang, pagi, malam, sore", "malam, sore, siang, pagi", "pagi, malam, siang, sore"], "A", "Urutan alami perputaran hari: pagi, siang, sore, lalu malam.")
mc("c4", "sedang", T, Kn, S2, "Mengapa kita tidak dianjurkan bermain panas-panasan di luar saat tengah hari?", ["karena sinar matahari sangat terik dan menyengat", "karena banyak bintang di langit", "karena udara sangat dingin", "karena sedang malam"], "A", "Tengah hari matahari sangat panas dan bisa membuat tubuh cepat lelah.")
tf("c4", "sedang", T, Kn, S3, "Kegiatan tidur malam biasanya memakan waktu paling lama dibanding kegiatan harian lain.", "Benar", "Tidur malam rata-rata berlangsung selama 8 jam.")
tf("c4", "sedang", T, Kn, S4, "Menyikat gigi membutuhkan waktu yang lebih lama daripada libur kenaikan kelas.", "Salah", "Libur sekolah berlangsung berminggu-minggu, menyikat gigi hanya beberapa menit.")
sa("c4", "sedang", T, Kn, S4, "Belajar sekolah 5 jam. Bermain sore 2 jam. Berapa jam selisih keduanya?", "3", "5 - 2 = 3 jam.", verifikasi={"ekspresi": "5 - 2", "hasil": "3"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Jika sekarang waktu sore hari, waktu yang akan datang berikutnya adalah ....", ["malam hari", "pagi hari", "siang hari", "tengah hari"], "A", "Setelah sore hari matahari terbenam dan tiba malam hari.")
mc("c4", "sedang", X, Kn, S2, "Di antara kegiatan berikut, manakah yang membutuhkan waktu paling lama?", ["belajar satu semester di sekolah", "mengikat tali sepatu", "makan sebuah biskuit", "membuka pintu"], "A", "Satu semester berlangsung selama beberapa bulan lamanya.")
tf("c4", "sedang", X, Kn, S4, "Bersin dan menguap adalah contoh kegiatan yang berlangsung sangat lama.", "Salah", "Bersin dan menguap hanya butuh beberapa detik (sebentar).")
mc("c4", "sulit", X, Me, S3, "Ayah bekerja 8 jam. Ibu memasak 2 jam. Berapa selisih jam kegiatan mereka?", ["6 jam", "5 jam", "7 jam", "4 jam"], "A", "8 - 2 = 6 jam.", verifikasi={"ekspresi": "8 - 2", "hasil": "6"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Kapan waktu yang paling tepat untuk menyiram tanaman agar tidak cepat layu?", ["pagi atau sore hari", "tengah hari saat terik", "tengah malam buta", "saat tidur"], "A", "Pagi atau sore hari saat suhu sejuk sangat baik menyiram tanaman.")
mc("c4", "sulit", K, Me, S2, "Budi bermain sepeda 45 menit. Istirahat 15 menit. Berapa menit total kegiatan sore?", ["60 menit", "50 menit", "70 menit", "40 menit"], "A", "45 + 15 = 60 menit.", verifikasi={"ekspresi": "45 + 15", "hasil": "60"})
tf("c4", "sulit", K, Me, S3, "Menggosok gigi sebelum tidur malam membuat gigi tetap sehat dan bersih.", "Benar", "Gosok gigi malam membersihkan sisa makanan saat tidur.")
mc("c4", "sulit", K, Me, S4, "Tidur siang 1 jam. Tidur malam 8 jam. Berapa jam total tidur dalam sehari?", ["9 jam", "8 jam", "10 jam", "7 jam"], "A", "1 + 8 = 9 jam.", verifikasi={"ekspresi": "1 + 8", "hasil": "9"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Siswa kelas 1 belajar 4 jam tiap pagi. Dalam 3 hari, berapa jam total belajarnya?", ["12 jam", "10 jam", "14 jam", "8 jam"], "A", "4 x 3 = 12 jam.", verifikasi={"ekspresi": "4 * 3", "hasil": "12"})
mc("c5", "sedang", T, Me, S2, "Kegiatan sore dimulai pukul 4 dan selesai pukul 6. Berapa jam durasi kegiatan itu?", ["2 jam", "1 jam", "3 jam", "4 jam"], "A", "6 - 4 = 2 jam.", verifikasi={"ekspresi": "6 - 4", "hasil": "2"})
mc("c5", "sedang", T, Me, S3, "Jika malam hari lampu padam, benda apa yang membantu kita melihat?", ["lilin atau senter", "kacamata hitam", "kipas angin", "buku pelajaran"], "A", "Lilin atau senter memancarkan cahaya saat listrik padam di malam hari.")
mc("c5", "sulit", T, Me, S4, "Urutkan kegiatan ini dari yang paling sebentar ke paling lama!", ["berkedip, mandi, tidur malam", "tidur malam, mandi, berkedip", "mandi, tidur malam, berkedip", "mandi, berkedip, tidur malam"], "A", "Berkedip (detik) < mandi (menit) < tidur malam (jam).")

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Pagi hari suhu 24 derajat. Siang hari suhu 30 derajat. Berapa derajat kenaikan suhu?", ["6 derajat", "5 derajat", "7 derajat", "4 derajat"], "A", "30 - 24 = 6 derajat.", verifikasi={"ekspresi": "30 - 24", "hasil": "6"})
mc("c5", "sulit", K, Me, S3, "Lampu belajar menyala dari pukul 7 malam sampai 9 malam. Berapa jam lampu menyala?", ["2 jam", "1 jam", "3 jam", "4 jam"], "A", "9 - 7 = 2 jam.", verifikasi={"ekspresi": "9 - 7", "hasil": "2"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Rancanglah jadwal pagi hari yang rapi sebelum berangkat ke sekolah!", ["bangun tepat waktu, merapikan kasur, mandi, sarapan, lalu berangkat", "sarapan, tidur lagi, berangkat, baru mandi", "berangkat sekolah dulu baru bangun tidur", "langsung mandi pakai baju tidur"], "A", "Urutan sehat: bangun, rapikan kasur, mandi, sarapan, lalu berangkat.")
mc("c6", "sulit", K, Me, S2, "Susunlah kegiatan sore hari yang seimbang antara bermain dan membantu orang tua!", ["membantu merapikan mainan setelah selesai bermain di halaman", "bermain terus sampai larut malam tanpa henti", "menonton TV sambil mengotori lantai", "tidur sepanjang sore sampai esok"], "A", "Bermain wajar lalu merapikan mainan dan membantu keluarga.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Tiap malam Edo tidur 8 jam. Berapa jam tidur selama 2 malam?", ["16 jam", "14 jam", "18 jam", "12 jam"], "A", "8 + 8 = 16 jam.", verifikasi={"ekspresi": "8 + 8", "hasil": "16"})
mc("c6", "sulit", P, Me, S4, "Kegiatan A butuh 15 menit. Kegiatan B butuh 25 menit. Berapa total menit keduanya?", ["40 menit", "35 menit", "45 menit", "30 menit"], "A", "15 + 25 = 40 menit.", verifikasi={"ekspresi": "15 + 25", "hasil": "40"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab25_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab25.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
