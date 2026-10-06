#!/usr/bin/env python3
"""
Generator dan validator Bab 31 Matematika Kelas 1 SD:
"Posisi Benda: Atas, Bawah, Kiri, Kanan, Depan, Belakang" (Fase A)
bab_id: 2db6ec75-80cb-41f8-8b1d-7ee3e772796e
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a1b2c34d5e01"  # Posisi Atas dan Bawah
S2 = "b2c3d45e6f12"  # Posisi Kiri dan Kanan
S3 = "c3d4e56f7a23"  # Posisi Depan dan Belakang
S4 = "d4e5f67a8b34"  # Menentukan Letak Benda Sehari-hari

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Lihatlah meja belajarmu sekarang.
Buku tulismu ada di atas meja.
Lampu belajar juga di atas meja.
Sekarang lihat bagian bawah mejamu.
Ada tempat sampah di bawah meja.
Sandal rumah juga di bawah meja.
Atas adalah arah ke langit.
Bawah adalah arah ke lantai.

:::definition
title: Atas dan Bawah
Atas menunjukkan letak lebih tinggi.
Bawah menunjukkan letak lebih rendah dekat lantai.
:::"""

s2_content = """Rentangkan kedua tanganmu ke samping.
Tangan kanan memegang pensil tulismu.
Tangan kiri memegang buku gambarmu.
Pensil berada di sebelah kanan.
Buku berada di sebelah kiri.
Kiri dan kanan letaknya berlawanan.
Keduanya membantu kita mencari arah.
Latihlah mengenal tangan kananmu.

:::steps
title: Mengenal Kanan dan Kiri
1. Angkat tangan yang biasa untuk bersalaman (kanan).
2. Tangan di sisi satunya adalah tangan kiri.
:::"""

s3_content = """Perhatikan suasana di ruang kelas.
Papan tulis ada di depan kelas.
Guru berdiri di depan siswa.
Papan pajangan ada di belakang kelas.
Pintu keluar ada di belakangmu.
Depan adalah arah pandangan matamu.
Belakang adalah arah punggungmu.
Keduanya saling bertolak belakang."""

s4_content = """Mari sebutkan letak semua benda.
Kucing tidur di atas kursi.
Bola terselip di belakang pintu.
Gelas ada di kanan piring.
Sendok ada di kiri mangkuk.

:::common_trap
title: Memperhatikan Titik Acuan
Kiri dan kanan membutuhkan acuan.
Tangan kananmu menghadap ke depan.
Bila teman berbalik badan arahnya berbeda.
Selalu perhatikan titik acuan benda.
Jangan terburu-buru menentukan arah.
:::

:::callout
variant: summary
title: Ringkasan
text: Posisi benda ditentukan dari acuan. Ada atas dan bawah, kiri dan kanan, serta depan dan belakang.
:::"""

sections = [
    {
        "id": S1,
        "title": "Posisi Atas dan Bawah",
        "minutes": 6,
        "goal": "Siswa memahami konsep orientasi spasial posisi atas dan posisi bawah terhadap suatu benda acuan.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Posisi Kiri dan Kanan",
        "minutes": 6,
        "goal": "Siswa memahami orientasi spasial posisi sebelah kiri dan sebelah kanan diri atau benda.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Posisi Depan dan Belakang",
        "minutes": 6,
        "goal": "Siswa memahami orientasi spasial posisi depan dan belakang terhadap suatu titik acuan.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menentukan Letak Benda Sehari-hari",
        "minutes": 6,
        "goal": "Siswa terampil mendeskripsikan dan menentukan letak relatif berbagai benda di lingkungan nyata.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Posisi Benda: Atas, Bawah, Kiri, Kanan, Depan, Belakang",
    "topic": "Mengenal Bentuk Bangun Datar dan Bangun Ruang",
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
# 2. DEFINISI BANK 50 SOAL BAB 31
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
mc("c1", "mudah", D, F, S1, "Buku dan lampu belajar diletakkan di .... meja belajar.", ["atas", "bawah", "belakang", "kiri"], "A", "Buku ditaruh di atas permukaan meja.")
tf("c1", "mudah", D, F, S3, "Papan tulis di dalam kelas biasanya berada di depan siswa.", "Benar", "Papan tulis berada di depan ruangan menghadap siswa.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Tangan yang biasa kita gunakan untuk bersalaman adalah tangan ....", ["kanan", "kiri", "kaki", "kepala"], "A", "Bersalaman umumnya memakai tangan kanan.")
mc("c1", "mudah", T, F, S3, "Arah yang berlawanan dengan arah depan adalah ....", ["belakang", "atas", "bawah", "kanan"], "A", "Lawan dari depan adalah belakang.")
sa("c1", "mudah", T, F, S1, "Ada 3 buku di atas meja dan 2 di bawah meja. Total buku?", "5", "3 + 2 = 5 buku.", verifikasi={"ekspresi": "3 + 2", "hasil": "5"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Bila tangan kanan memegang pensil, tangan kiri memegang penghapus di sebelah ....", ["kiri", "kanan", "atas", "bawah"], "A", "Penghapus berada di sebelah kiri.", "Tertukar antara posisi kiri dan kanan")
tf("c2", "mudah", D, Kn, S4, "Kucing yang bersembunyi di bawah kursi berada lebih rendah dari dudukan kursi.", "Benar", "Posisi bawah berarti berada lebih rendah dekat lantai.")

# Remedial (2)
mc("c2", "mudah", R, F, S1, "Sepatu ditaruh di lantai kolong meja. Posisi sepatu berada di ....", ["bawah meja", "atas meja", "depan meja", "samping langit"], "A", "Kolong meja adalah posisi bagian bawah.", "Keliru menentukan posisi bawah benda")
mc("c2", "mudah", R, Kn, S3, "Saat kita berjalan maju lurus, arah punggung kita menghadap ke ....", ["belakang", "depan", "kiri", "atas"], "A", "Punggung selalu menghadap ke arah belakang.", "Tertukar antara arah depan pandangan dan arah punggung")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Di atas lemari ada 4 kardus. Di bawah lemari ada 3 kardus. Total kardus?", ["7 kardus", "6 kardus", "8 kardus", "5 kardus"], "A", "4 + 3 = 7 kardus.", verifikasi={"ekspresi": "4 + 3", "hasil": "7"})
mc("c2", "mudah", T, Kn, S2, "Di sebelah kanan ada 5 kursi, di sebelah kiri ada 4 kursi. Total kursi?", ["9 kursi", "8 kursi", "10 kursi", "7 kursi"], "A", "5 + 4 = 9 kursi.", verifikasi={"ekspresi": "5 + 4", "hasil": "9"})
tf("c2", "mudah", T, Kn, S3, "Benda yang berada tepat di depan mata kita berada di arah belakang.", "Salah", "Benda di depan pandangan mata berada di arah depan.")
sa("c2", "mudah", T, Kn, S4, "Ada 6 gelas di kanan piring dan 2 gelas di kiri. Selisih gelas?", "4", "6 - 2 = 4 gelas.", verifikasi={"ekspresi": "6 - 2", "hasil": "4"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Beni dan Siti saling berhadapan. Tangan kanan Beni lurus dengan tangan .... Siti.", ["kiri", "kanan", "depan", "belakang"], "A", "Saat saling berhadapan, arah kanan dan kiri menjadi berkebalikan.", "Salah menentukan arah kiri kanan saat berhadapan")
mc("c3", "sedang", R, Pr, S4, "Budi melangkah 4 langkah ke depan, lalu mundur 2 langkah ke belakang. Posisi langkah?", ["2 langkah", "6 langkah", "3 langkah", "1 langkah"], "A", "4 - 2 = 2 langkah di depan posisi awal.", "Keliru menghitung langkah maju dan mundur", verifikasi={"ekspresi": "4 - 2", "hasil": "2"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Di rak atas ada 6 buku. Di rak bawah ada 2 buku. Berapa selisihnya?", ["4 buku", "3 buku", "5 buku", "2 buku"], "A", "6 - 2 = 4 buku.", verifikasi={"ekspresi": "6 - 2", "hasil": "4"})
mc("c3", "sedang", T, Pr, S2, "Lani melangkah 5 langkah ke kanan, lalu 3 langkah lagi ke kanan. Total langkah?", ["8 langkah", "7 langkah", "9 langkah", "6 langkah"], "A", "5 + 3 = 8 langkah ke kanan.", verifikasi={"ekspresi": "5 + 3", "hasil": "8"})
tf("c3", "sedang", T, Pr, S3, "Berjalan mundur berarti menggerakkan tubuh ke arah belakang.", "Benar", "Mundur artinya bergerak ke arah belakang.")
mc("c3", "sedang", T, Pr, S4, "Di depan kelas ada 7 siswa berbaris. 3 siswa masuk ke kelas. Sisa siswa?", ["4 siswa", "3 siswa", "5 siswa", "2 siswa"], "A", "7 - 3 = 4 siswa.", verifikasi={"ekspresi": "7 - 3", "hasil": "4"})
tf("c3", "sedang", T, Pr, S1, "Lampu gantung di langit-langit kamar berada di bawah tempat tidur.", "Salah", "Lampu gantung berada di atas kamar.")
sa("c3", "mudah", T, Pr, S2, "Ada 4 pot bunga di kiri dan 4 pot di kanan gerbang. Total pot?", "8", "4 + 4 = 8 pot bunga.", verifikasi={"ekspresi": "4 + 4", "hasil": "8"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Di atas meja ada 8 apel. Diambil adik 3 apel. Berapa apel tersisa?", ["5 apel", "4 apel", "6 apel", "3 apel"], "A", "8 - 3 = 5 apel.", verifikasi={"ekspresi": "8 - 3", "hasil": "5"})
mc("c3", "sedang", X, Pr, S2, "Edo melompat 6 kali ke kiri dan 5 kali ke kanan. Berapa total lompatan?", ["11 lompatan", "10 lompatan", "12 lompatan", "9 lompatan"], "A", "6 + 5 = 11 lompatan.", verifikasi={"ekspresi": "6 + 5", "hasil": "11"})
tf("c3", "sedang", X, Pr, S4, "Sendok makan selalu berada di sebelah kiri piring saat dipegang tangan kiri.", "Benar", "Jika dipegang tangan kiri, sendok berada di sebelah kiri.")
sa("c3", "sedang", X, Pr, S3, "Di depan rumah ada 9 pohon. Di belakang ada 4 pohon. Selisih pohon?", "5", "9 - 4 = 5 pohon.", verifikasi={"ekspresi": "9 - 4", "hasil": "5"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Di rak atas ada 7 piring. Di rak bawah ada 6 piring. Total piring?", ["13 piring", "12 piring", "14 piring", "11 piring"], "A", "7 + 6 = 13 piring.", verifikasi={"ekspresi": "7 + 6", "hasil": "13"})
mc("c3", "sedang", K, Pr, S3, "Mobil bergerak maju 8 meter lalu maju lagi 6 meter. Berapa total meter?", ["14 meter", "13 meter", "15 meter", "12 meter"], "A", "8 + 6 = 14 meter.", verifikasi={"ekspresi": "8 + 6", "hasil": "14"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Mengapa kita menyebut lampu di plafon berada di posisi atas?", ["karena posisinya lebih tinggi dari kepala kita ke arah langit", "karena lampunya menyala terang", "karena harganya mahal", "karena berwarna kuning"], "A", "Posisi atas adalah arah vertikal ke tempat yang lebih tinggi.")
mc("c4", "sedang", T, Kn, S2, "Jika kamu berdiri menghadap matahari terbit di timur, tangan kananmu menunjuk arah ....", ["selatan", "utara", "barat", "atas"], "A", "Menghadap timur, tangan kanan menunjuk arah selatan.")
tf("c4", "sedang", T, Kn, S3, "Orang yang duduk di barisan depan punggungnya menghadap ke siswa di belakangnya.", "Benar", "Siswa di baris depan membelakangi siswa di baris belakang.")
tf("c4", "sedang", T, Kn, S4, "Arah kanan seseorang akan selalu sama meskipun orang tersebut berputar balik arah.", "Salah", "Jika berputar balik arah, posisi kanan dan kiri ikut berbalik.")
sa("c4", "sedang", T, Kn, S4, "Di depan ada 16 mobil. 7 mobil melaju pergi. Berapa mobil tersisa di depan?", "9", "16 - 7 = 9 mobil.", verifikasi={"ekspresi": "16 - 7", "hasil": "9"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Burung terbang di atas pohon. Kucing berjalan di bawah pohon. Berapa tinggi kucing dibanding pohon?", ["kucing berada lebih rendah dari pohon", "kucing lebih tinggi dari burung", "kucing melayang", "kucing di awan"], "A", "Posisi bawah berarti lebih rendah di permukaan tanah.")
mc("c4", "sedang", X, Kn, S2, "Ada 14 bendera di sisi kanan jalan. Dipindahkan 6 bendera ke kiri. Sisa bendera kanan?", ["8 bendera", "7 bendera", "9 bendera", "6 bendera"], "A", "14 - 6 = 8 bendera.", verifikasi={"ekspresi": "14 - 6", "hasil": "8"})
tf("c4", "sedang", X, Kn, S3, "Bila berbaris menghadap depan, punggungmu menghadap ke papan tulis depan.", "Salah", "Wajah menghadap depan, sedangkan punggung menghadap ke belakang.")
mc("c4", "sulit", X, Me, S4, "Robot berjalan 10 langkah ke depan lalu mundur 3 langkah. Berapa jarak dari start?", ["7 langkah", "6 langkah", "8 langkah", "5 langkah"], "A", "10 - 3 = 7 langkah.", verifikasi={"ekspresi": "10 - 3", "hasil": "7"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Benda yang paling aman ditaruh di rak paling bawah agar tidak mudah pecah adalah ....", ["bola basket", "gelas kaca tipis", "lampu hias", "piring keramik"], "A", "Bola plastik aman di bawah karena tidak mudah pecah jika jatuh.")
mc("c4", "sulit", K, Me, S2, "Di kanan ada 9 murid. Di kiri ada 7 murid. Berapa selisih banyaknya murid?", ["2 murid", "1 murid", "3 murid", "4 murid"], "A", "9 - 7 = 2 murid.", verifikasi={"ekspresi": "9 - 7", "hasil": "2"})
tf("c4", "sulit", K, Me, S3, "Melihat kaca spion mobil membantu pengemudi melihat keadaan di depan mobil.", "Salah", "Kaca spion digunakan untuk melihat kendaraan di bagian belakang.")
mc("c4", "sulit", K, Me, S4, "Kereta mainan punya 18 gerbong. 9 gerbong di belakang terlepas. Sisa gerbong?", ["9 gerbong", "8 gerbong", "10 gerbong", "7 gerbong"], "A", "18 - 9 = 9 gerbong.", verifikasi={"ekspresi": "18 - 9", "hasil": "9"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Ada 3 rak susun. Tiap rak berisi 5 buku. Berapa total seluruh buku di ketiga rak?", ["15 buku", "12 buku", "16 buku", "14 buku"], "A", "3 x 5 = 15 buku.", verifikasi={"ekspresi": "3 * 5", "hasil": "15"})
mc("c5", "sedang", T, Me, S2, "Doni berdiri di tengah. Di kanannya ada 6 teman, di kirinya ada 8 teman. Total teman?", ["14 teman", "13 teman", "15 teman", "12 teman"], "A", "6 + 8 = 14 teman.", verifikasi={"ekspresi": "6 + 8", "hasil": "14"})
mc("c5", "sedang", T, Me, S3, "Semut maju 12 cm lalu mundur 4 cm. Berapa cm jarak dari posisi awal?", ["8 cm", "7 cm", "9 cm", "6 cm"], "A", "12 - 4 = 8 cm.", verifikasi={"ekspresi": "12 - 4", "hasil": "8"})
mc("c5", "sulit", T, Me, S4, "Ada 5 bola di depan, 4 di belakang, dan 6 di atas. Berapa total bola?", ["15 bola", "14 bola", "16 bola", "13 bola"], "A", "5 + 4 + 6 = 15 bola.", verifikasi={"ekspresi": "5 + 4 + 6", "hasil": "15"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Di kolong meja ada 16 kardus. Dikeluarkan 7 kardus. Berapa kardus sisa di bawah meja?", ["9 kardus", "8 kardus", "10 kardus", "7 kardus"], "A", "16 - 7 = 9 kardus.", verifikasi={"ekspresi": "16 - 7", "hasil": "9"})
mc("c5", "sulit", K, Me, S3, "Udin melangkah 15 langkah ke depan lalu berbalik dan melangkah 8 langkah. Jarak dari start?", ["7 langkah", "6 langkah", "8 langkah", "5 langkah"], "A", "15 - 8 = 7 langkah.", verifikasi={"ekspresi": "15 - 8", "hasil": "7"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Susunlah tata letak ruang belajar yang nyaman: buku, lampu, dan tempat sampah!", ["buku dan lampu di atas meja, tempat sampah di bawah meja", "tempat sampah di atas kasur dan buku di lantai basah", "lampu belajar ditaruh di dalam laci tertutup", "semua benda ditumpuk di atas kursi"], "A", "Buku dan lampu di atas meja, tempat sampah di lantai bawah meja.")
mc("c6", "sulit", K, Me, S4, "Rancanglah denah barisan upacara bendera yang rapi berdasarkan arah mata angin!", ["pemimpin barisan berdiri di depan menghadap seluruh peserta upacara", "pemimpin upacara bersembunyi di paling belakang", "semua peserta membelakangi tiang bendera", "peserta tidur di bawah pohon"], "A", "Pemimpin upacara berdiri tegak di posisi paling depan menghadap barisan.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S2, "Ada 4 baris kursi kanan dan 4 baris kiri. Tiap baris 2 kursi. Total kursi?", ["16 kursi", "14 kursi", "18 kursi", "12 kursi"], "A", "(4 + 4) x 2 = 16 kursi.", verifikasi={"ekspresi": "(4 + 4) * 2", "hasil": "16"})
mc("c6", "sulit", P, Me, S3, "Katak lompat maju 14 petak, mundur 5 petak, lalu maju 3 petak. Posisi sekarang?", ["12 petak", "11 petak", "13 petak", "10 petak"], "A", "14 - 5 + 3 = 12 petak.", verifikasi={"ekspresi": "14 - 5 + 3", "hasil": "12"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab31_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab31.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
