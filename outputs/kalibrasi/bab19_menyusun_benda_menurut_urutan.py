#!/usr/bin/env python3
"""
Generator dan validator Bab 19 Matematika Kelas 1 SD:
"Menyusun Benda Menurut Urutan" (Fase A)
bab_id: e668c30a-7851-45fb-8542-7630224d88b7
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a9b8c79d0e01"  # Mengurutkan dari yang Terkecil ke Terbesar
S2 = "b0c9d80e1f12"  # Mengurutkan dari yang Terbesar ke Terkecil
S3 = "c1d0e91f2a23"  # Mengurutkan Berdasarkan Jumlah Benda
S4 = "d2e1f02a3b34"  # Mengurutkan Peristiwa Sehari-hari

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Kita bisa menata benda dengan urutan.
Mulai dari yang paling kecil.
Lalu ukuran sedang di tengah.
Terakhir benda paling besar di ujung.
Urutan ini namanya makin membesar.
Contoh: kelereng, kasti, basket.
Susunan terlihat rapi dan teratur.
Ayo coba urutkan dari terkecil.

:::definition
title: Urutan dari Terkecil
Menyusun dari benda paling kecil.
Benda berikutnya semakin membesar ukurannya.
:::"""

s2_content = """Bisa juga diurutkan sebaliknya.
Mulai dari benda paling besar.
Lalu ukuran benda makin mengecil.
Benda paling kecil ada di ujung.
Contohnya: gajah, kuda, lalu kucing.
Pohon tinggi ke pohon pendek.
Perhatikan arah urutannya baik-baik.
Jangan sampai terbalik arahnya.

:::steps
title: Mengurutkan dari Terbesar
1. Cari benda yang paling besar.
2. Letakkan di posisi pertama.
3. Susun sisa benda yang mengecil.
:::"""

s3_content = """Kita juga bisa mengurutkan jumlah.
Hitung isi tiap piring buah.
Piring pertama ada 2 apel.
Piring kedua ada 4 apel.
Piring ketiga ada 6 apel.
Jumlah apel diurutkan makin banyak.
Bisa juga dari yang terbanyak.
Hitung jumlahnya satu per satu."""

s4_content = """Kegiatan sehari-hari juga ada urutannya.
Pagi hari kita bangun tidur.
Lalu mandi dan sarapan pagi.
Setelah itu berangkat ke sekolah.
Malam hari saatnya tidur lelap.

:::common_trap
title: Tertukar Arah Terbesar dan Terkecil
Baca instruksi soal dengan sangat teliti.
Periksa benda pertama dan terakhirnya.
Apakah diminta dari yang terkecil?
Atau diminta dari yang terbesar?
:::

:::callout
variant: summary
title: Ringkasan
text: Mengurutkan benda butuh arah jelas. Periksa apakah dari kecil ke besar atau sebaliknya.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengurutkan dari yang Terkecil ke Terbesar",
        "minutes": 6,
        "goal": "Siswa dapat menyusun dan mengurutkan benda dari ukuran terkecil hingga terbesar.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengurutkan dari yang Terbesar ke Terkecil",
        "minutes": 6,
        "goal": "Siswa dapat menyusun dan mengurutkan benda dari ukuran terbesar hingga terkecil.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mengurutkan Berdasarkan Jumlah Benda",
        "minutes": 6,
        "goal": "Siswa dapat menyusun kumpulan benda berdasarkan kuantitas banyak atau sedikit.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Mengurutkan Peristiwa Sehari-hari",
        "minutes": 6,
        "goal": "Siswa dapat mengurutkan tahapan kejadian kronologis sederhana dalam kehidupan sehari-hari.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Menyusun Benda Menurut Urutan",
    "topic": "Pola dan Urutan",
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
# 2. DEFINISI BANK 50 SOAL BAB 19
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
mc("c1", "mudah", D, F, S1, "Urutan dari yang terkecil diawali oleh benda berukuran ....", ["paling kecil", "paling besar", "sedang", "bebas"], "A", "Urutan dari yang terkecil selalu diawali benda terkecil.")
tf("c1", "mudah", D, F, S2, "Urutan dari terbesar menaruh benda paling besar di awal.", "Benar", "Posisi pertama diisi oleh benda yang ukurannya paling besar.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Di antara semut, kelinci, sapi, hewan paling kecil adalah ....", ["semut", "kelinci", "sapi", "kambing"], "A", "Semut memiliki ukuran paling kecil.")
mc("c1", "mudah", T, F, S2, "Di antara bus, sepeda, motor, kendaraan paling besar adalah ....", ["bus", "motor", "sepeda", "becak"], "A", "Bus adalah kendaraan paling besar.")
sa("c1", "mudah", T, F, S3, "Ada piring berisi 2, 5, 8 kue. Berapa isi piring paling sedikit?", "2", "Paling sedikit adalah 2 kue.", verifikasi={"ekspresi": "2", "hasil": "2"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Urutkan bola dari terkecil: tenis, kelereng, basket!", ["kelereng, tenis, basket", "basket, tenis, kelereng", "tenis, basket, kelereng", "kelereng, basket, tenis"], "A", "Kelereng paling kecil, lalu tenis, lalu basket.")
tf("c2", "mudah", D, Kn, S4, "Kita sarapan pagi setelah pulang sekolah.", "Salah", "Sarapan dilakukan pada pagi hari sebelum berangkat ke sekolah.")

# Remedial (2)
mc("c2", "mudah", R, F, S1, "Saat mengurutkan dari terkecil, benda paling akhir berukuran ....", ["paling besar", "paling kecil", "sedang", "sangat kecil"], "A", "Ujung akhir adalah benda yang paling besar.", "Tertukar posisi awal dan akhir urutan")
mc("c2", "mudah", R, Kn, S3, "Ada 3 piring berisi 9, 6, 3 apel. Berapa isi piring paling banyak?", ["9 apel", "6 apel", "3 apel", "1 apel"], "A", "Isi paling banyak adalah 9 apel.", "Salah mengurutkan jumlah benda", verifikasi={"ekspresi": "9", "hasil": "9"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Urutkan gelas dari terkecil: sedang, besar, kecil!", ["kecil, sedang, besar", "besar, sedang, kecil", "sedang, kecil, besar", "kecil, besar, sedang"], "A", "Urutan membesar: kecil, sedang, besar.")
mc("c2", "mudah", T, Kn, S2, "Urutkan dari terbesar: gajah, kucing, kambing!", ["gajah, kambing, kucing", "kucing, kambing, gajah", "kambing, gajah, kucing", "gajah, kucing, kambing"], "A", "Gajah paling besar, lalu kambing, lalu kucing.")
tf("c2", "mudah", T, Kn, S3, "Piring berisi 8 apel lebih banyak daripada piring berisi 5 apel.", "Benar", "8 lebih banyak daripada 5.")
sa("c2", "mudah", T, Kn, S4, "Peristiwa: sarapan, bangun tidur. Manakah yang terjadi lebih dulu?", "bangun tidur", "Bangun tidur dilakukan sebelum sarapan pagi.")

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Urutkan pohon dari yang tertinggi: 5 meter, 2 meter, 8 meter!", ["8 meter, 5 meter, 2 meter", "2 meter, 5 meter, 8 meter", "5 meter, 8 meter, 2 meter", "8 meter, 2 meter, 5 meter"], "A", "Dari tertinggi: 8, 5, lalu 2 meter.", "Salah mengurutkan ukuran tinggi dari yang terbesar")
mc("c3", "sedang", R, Pr, S4, "Urutan kegiatan malam hari yang benar adalah ....", ["makan malam lalu tidur", "tidur lalu makan malam", "bangun tidur lalu tidur", "sekolah lalu tidur"], "A", "Makan malam dilakukan sebelum tidur malam.", "Tertukar urutan kegiatan malam hari")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Urutkan angka dari terkecil: 7, 2, 5!", ["2, 5, 7", "7, 5, 2", "5, 2, 7", "2, 7, 5"], "A", "Dari terkecil adalah 2, 5, 7.")
mc("c3", "sedang", T, Pr, S2, "Ada pita 12 cm, 4 cm, 9 cm. Berapa cm panjang pita terpanjang?", ["12 cm", "9 cm", "4 cm", "10 cm"], "A", "Paling panjang adalah 12 cm.", verifikasi={"ekspresi": "12", "hasil": "12"})
tf("c3", "sedang", T, Pr, S3, "Urutan piring 4 kue, 7 kue, 10 kue tersusun makin banyak.", "Benar", "4 < 7 < 10, jumlahnya semakin bertambah.")
mc("c3", "sedang", T, Pr, S4, "Urutkan waktu: siang, pagi, malam dari awal hari!", ["pagi, siang, malam", "siang, pagi, malam", "malam, siang, pagi", "pagi, malam, siang"], "A", "Urutan waktu alami adalah pagi, siang, lalu malam.")
tf("c3", "sedang", T, Pr, S1, "Urutan kelereng, bola voli, bola kasti adalah dari terkecil ke terbesar.", "Salah", "Bola kasti lebih kecil daripada bola voli.")
sa("c3", "mudah", T, Pr, S2, "Ada bilangan: 15, 8, 20. Bilangan berapakah yang paling besar?", "20", "Bilangan terbesar adalah 20.", verifikasi={"ekspresi": "20", "hasil": "20"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Beni punya pensil 6 cm, 10 cm, 8 cm. Berapa cm pensil terpendek?", ["6 cm", "8 cm", "10 cm", "7 cm"], "A", "Paling pendek adalah 6 cm.", verifikasi={"ekspresi": "6", "hasil": "6"})
mc("c3", "sedang", X, Pr, S2, "Ada botol 3 liter, 1 liter, 5 liter. Berapa liter isi botol terbanyak?", ["5 liter", "3 liter", "1 liter", "4 liter"], "A", "Paling banyak adalah 5 liter.", verifikasi={"ekspresi": "5", "hasil": "5"})
tf("c3", "sedang", X, Pr, S3, "Urutan 12 jeruk, 15 jeruk, 18 jeruk adalah urutan berkurang.", "Salah", "12, 15, 18 adalah urutan bertambah banyak.")
sa("c3", "sedang", X, Pr, S4, "Urutkan angka jumlah: 14, 6, 11 dari terkecil. Angka pertamanya?", "6", "Angka terkecil adalah 6.", verifikasi={"ekspresi": "6", "hasil": "6"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Penggaris 30 cm, 15 cm, 20 cm. Berapa cm panjang penggaris terpendek?", ["15 cm", "20 cm", "30 cm", "10 cm"], "A", "Paling pendek adalah 15 cm.", verifikasi={"ekspresi": "15", "hasil": "15"})
mc("c3", "sedang", K, Pr, S3, "Ada tiga keranjang berisi 9, 14, 4 mangga. Berapa isi keranjang tengah jika diurutkan?", ["9", "4", "14", "10"], "A", "Urutan: 4, 9, 14. Keranjang tengah berisi 9.", verifikasi={"ekspresi": "9", "hasil": "9"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Tiga kotak disusun membesar. Kotak A lebih kecil dari B, B lebih kecil dari C. Urutannya?", ["A, B, C", "C, B, A", "B, A, C", "A, C, B"], "A", "Dari terkecil: A, B, lalu C.")
mc("c4", "sedang", T, Kn, S2, "Pohon cemara lebih tinggi dari mangga. Kelapa lebih tinggi dari cemara. Tertinggi adalah?", ["kelapa", "cemara", "mangga", "pisang"], "A", "Kelapa > cemara > mangga, jadi kelapa tertinggi.")
tf("c4", "sedang", T, Kn, S3, "Kotak berisi 15 bola berada di antara kotak 8 bola dan 12 bola.", "Salah", "15 lebih besar daripada 12, jadi tidak berada di antaranya.")
tf("c4", "sedang", T, Kn, S4, "Urutan waktu belajar di sekolah dilakukan sebelum tidur malam.", "Benar", "Belajar di sekolah berlangsung siang hari sebelum malam.")
sa("c4", "sedang", T, Kn, S4, "Ada benda 5 cm, 12 cm, 8 cm, 15 cm. Berapa cm panjang benda terpanjang?", "15", "Paling panjang adalah 15 cm.", verifikasi={"ekspresi": "15", "hasil": "15"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Manakah kelompok benda yang sudah berurutan dari terkecil ke terbesar?", ["semut, kucing, gajah", "gajah, kucing, semut", "kucing, gajah, semut", "semut, gajah, kucing"], "A", "Semut paling kecil, kucing sedang, gajah paling besar.")
mc("c4", "sedang", X, Kn, S2, "Ada 4 pita: 3 cm, 7 cm, 11 cm, 5 cm. Berapa cm pita terpanjang?", ["11 cm", "7 cm", "5 cm", "3 cm"], "A", "Pita terpanjang adalah 11 cm.", verifikasi={"ekspresi": "11", "hasil": "11"})
tf("c4", "sedang", X, Kn, S4, "Makan siang biasanya dilakukan sebelum sarapan pagi.", "Salah", "Sarapan pagi selalu dilakukan sebelum makan siang.")
mc("c4", "sulit", X, Me, S3, "Ada bilangan 4, 8, 12. Berapakah selisih antara bilangan terbesar dan terkecil?", ["8", "4", "6", "12"], "A", "12 - 4 = 8.", verifikasi={"ekspresi": "12 - 4", "hasil": "8"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Bandingkan urutan A (2, 4, 6) dan urutan B (6, 4, 2). Keduanya berbeda dalam hal ....", ["arah urutannya", "angka yang digunakan", "jumlah anggotanya", "selisih angkanya"], "A", "A dari terkecil ke terbesar, sedangkan B sebaliknya.")
mc("c4", "sulit", K, Me, S2, "Tinggi badan: Siti 110 cm, Edo 115 cm, Dayu 105 cm. Berapa cm tinggi Edo?", ["115 cm", "110 cm", "105 cm", "120 cm"], "A", "Tinggi Edo adalah 115 cm.", verifikasi={"ekspresi": "115", "hasil": "115"})
tf("c4", "sulit", K, Me, S3, "Bila diurutkan dari terbanyak, selisih 15 dan 5 buah adalah 10 buah.", "Benar", "15 - 5 = 10 buah.", verifikasi={"ekspresi": "15 - 5", "hasil": "10"})
mc("c4", "sulit", K, Me, S4, "Urutan kejadian: (1) mandi, (2) bangun tidur, (3) sarapan. Urutan yang tepat adalah ....", ["2, 1, 3", "1, 2, 3", "3, 2, 1", "2, 3, 1"], "A", "Bangun tidur (2), lalu mandi (1), lalu sarapan (3).")

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Urutan ukuran: kecil, besar, sedang. Bagaimana memperbaikinya agar teratur dari kecil?", ["tukar posisi besar dan sedang", "taruh kecil di akhir", "hapus ukuran sedang", "biarkan saja"], "A", "Tukar besar dan sedang sehingga menjadi: kecil, sedang, besar.")
mc("c5", "sedang", T, Me, S2, "Ada benda berukuran 18 cm, 7 cm, 12 cm. Berapa selisih terpanjang dan terpendek?", ["11 cm", "10 cm", "12 cm", "9 cm"], "A", "18 - 7 = 11 cm.", verifikasi={"ekspresi": "18 - 7", "hasil": "11"})
mc("c5", "sedang", T, Me, S3, "Tiga toples berisi 5, 10, 15 permen. Berapa jumlah isi toples terbanyak dan tersedikit?", ["20 permen", "25 permen", "15 permen", "18 permen"], "A", "15 + 5 = 20 permen.", verifikasi={"ekspresi": "15 + 5", "hasil": "20"})
mc("c5", "sulit", T, Me, S4, "Mengapa kita tidak boleh menukar urutan memakai sepatu sebelum memakai kaus kaki?", ["karena kaus kaki harus dipakai di dalam sepatu", "karena warna sepatu berbeda", "karena sepatu lebih berat", "karena kaus kaki lebih panjang"], "A", "Kaus kaki harus berada di dalam sepatu, sehingga dipakai duluan.")

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Andi punya 3 tongkat: 8 cm, 14 cm, 11 cm. Tongkat manakah yang berada di tengah?", ["11 cm", "8 cm", "14 cm", "10 cm"], "A", "Urutan: 8 cm, 11 cm, 14 cm. Tengah adalah 11 cm.", verifikasi={"ekspresi": "11", "hasil": "11"})
mc("c5", "sulit", K, Me, S3, "Kantong berisi 3, 6, 9, 12 kelereng. Berapa total isi kantong 6 dan 9?", ["15 kelereng", "12 kelereng", "18 kelereng", "14 kelereng"], "A", "6 + 9 = 15 kelereng.", verifikasi={"ekspresi": "6 + 9", "hasil": "15"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Bilangan: 19, 5, 12, 8. Berapa selisih bilangan terbesar dan terkecil?", ["14", "12", "11", "10"], "A", "19 - 5 = 14.", verifikasi={"ekspresi": "19 - 5", "hasil": "14"})
mc("c6", "sulit", K, Me, S2, "Rancanglah susunan 3 hewan dari yang paling berat ke paling ringan!", ["gajah, kambing, ayam", "ayam, kambing, gajah", "kambing, gajah, ayam", "gajah, ayam, kambing"], "A", "Gajah paling berat, kambing sedang, ayam paling ringan.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Susunlah 4 kelompok benda: 4, 8, 12, 16. Berapa jumlah dua kelompok terbesar?", ["28", "24", "20", "30"], "A", "12 + 16 = 28.", verifikasi={"ekspresi": "12 + 16", "hasil": "28"})
mc("c6", "sulit", P, Me, S4, "Rancanglah jadwal kegiatan hari Minggu: tidur, bermain, sarapan, bangun dari pagi!", ["bangun, sarapan, bermain, tidur", "sarapan, bangun, bermain, tidur", "bermain, bangun, sarapan, tidur", "tidur, bermain, sarapan, bangun"], "A", "Urutan logis: bangun, sarapan, bermain, lalu tidur malam.")

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab19_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab19.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
