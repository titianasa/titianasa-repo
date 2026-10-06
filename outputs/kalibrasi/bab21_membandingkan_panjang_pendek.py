#!/usr/bin/env python3
"""
Generator dan validator Bab 21 Matematika Kelas 1 SD:
"Membandingkan Panjang dan Pendek" (Fase A)
bab_id: 04d73660-ba68-49e6-a429-d2bd25bda8b9
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a1b0c99d2e01"  # Mengenal Panjang dan Pendek
S2 = "b2c1d00e3f12"  # Mengenal Tinggi dan Rendah
S3 = "c3d2e11f4a23"  # Membandingkan Langsung Dua Benda
S4 = "d4e3f22a5b34"  # Mengurutkan dari Terpanjang atau Terpendek

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Benda di sekitar kita berbeda ukuran.
Ada benda yang panjang.
Ada juga benda yang pendek.
Penggaris guru lebih panjang dari pensil.
Penghapus karet lebih pendek dari pensil.
Panjang adalah jarak ujung ke ujung.
Ayo amati pensil di mejamy.

:::definition
title: Panjang dan Pendek
Panjang adalah bentangan dari satu ujung ke ujung lain.
Pendek adalah bentangan yang lebih kecil.
:::"""

s2_content = """Ukuran arah tegak kita sebut tinggi.
Lawan kata tinggi adalah rendah.
Pohon kelapa tumbuh menjulang tinggi.
Rumput di halaman tumbuh rendah.
Jerapah memiliki leher yang tinggi.
Kucing bertubuh lebih rendah dari jerapah.
Tinggi diukur dari bawah ke atas.

:::steps
title: Membandingkan Tinggi Benda
1. Letakkan kedua benda di lantai datar.
2. Amati puncak paling atas kedua benda.
3. Benda yang puncaknya lebih atas adalah lebih tinggi.
:::"""

s3_content = """Bagaimana membandingkan dua pensil?
Jangan letakkan pensil sembarangan.
Kedua ujung pensil harus sejajar.
Tempelkan ujungnya pada garis lurus.
Lalu lihat ujung yang lain.
Pensil lebih menjulur adalah lebih panjang.
Perbandingan menjadi adil dan tepat.
Kedua pangkal harus lurus rata."""

s4_content = """Kita bisa mengurutkan tiga benda.
Misalnya tali merah, hijau, biru.
Ratakan ujung pangkal ketiganya.
Urutkan dari yang paling panjang.
Atau urutkan dari yang terpendek.

:::common_trap
title: Ujung Pangkal Tidak Sejajar
Jangan bandingkan dua benda yang bergeser.
Kedua ujung pangkal harus sejajar lurus.
Benda yang maju tampak lebih panjang.
Padahal aslinya belum tentu panjang.
Ratakan dulu ujung kirinya.
:::

:::callout
variant: summary
title: Ringkasan
text: Bandingkan panjang dengan menyejajarkan ujung pangkal pada garis yang sama.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Panjang dan Pendek",
        "minutes": 6,
        "goal": "Siswa dapat membedakan konsep panjang dan pendek pada benda di sekitarnya.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengenal Tinggi dan Rendah",
        "minutes": 6,
        "goal": "Siswa dapat membedakan ukuran vertikal tinggi dan rendah pada benda atau makhluk hidup.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membandingkan Langsung Dua Benda",
        "minutes": 6,
        "goal": "Siswa dapat membandingkan panjang dua benda dengan menyejajarkan salah satu ujungnya.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Mengurutkan dari Terpanjang atau Terpendek",
        "minutes": 6,
        "goal": "Siswa dapat menyusun serangkaian benda dari yang paling panjang ke terpendek atau sebaliknya.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membandingkan Panjang dan Pendek",
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
# 2. DEFINISI BANK 50 SOAL BAB 21
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
mc("c1", "mudah", D, F, S1, "Lawan kata dari panjang adalah ....", ["pendek", "tinggi", "rendah", "besar"], "A", "Lawan kata panjang adalah pendek.")
tf("c1", "mudah", D, F, S2, "Pohon kelapa lebih tinggi daripada rumput di halaman.", "Benar", "Pohon kelapa tumbuh menjulang tinggi, sedangkan rumput rendah.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Benda yang biasanya lebih panjang dari pensil adalah ....", ["penggaris guru", "penghapus karet", "rautan", "uang koin"], "A", "Penggaris guru jauh lebih panjang dari pensil.")
mc("c1", "mudah", T, F, S2, "Hewan yang memiliki tubuh paling tinggi adalah ....", ["jerapah", "kucing", "kelinci", "bebek"], "A", "Jerapah memiliki leher dan tubuh yang sangat tinggi.")
sa("c1", "mudah", T, F, S3, "Ada pita 10 cm dan 4 cm. Berapa cm panjang pita terpendek?", "4", "Pita 4 cm adalah yang paling pendek.", verifikasi={"ekspresi": "4", "hasil": "4"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Pensil baru lebih .... daripada pensil yang sering diraut.", ["panjang", "pendek", "rendah", "ringan"], "A", "Pensil baru belum terpotong rautan sehingga lebih panjang.")
tf("c2", "mudah", D, Kn, S3, "Membandingkan panjang benda boleh dilakukan tanpa meratakan ujungnya.", "Salah", "Ujung pangkal kedua benda harus sejajar rata.")

# Remedial (2)
mc("c2", "mudah", R, F, S3, "Syarat membandingkan dua pensil secara adil adalah ....", ["ujung pangkal harus sejajar", "warna pensil harus sama", "pensil harus baru", "harga pensil harus sama"], "A", "Kedua ujung pangkal harus sejajar pada satu garis lurus.", "Membandingkan panjang tanpa menyamakan ujung pangkal")
mc("c2", "mudah", R, Kn, S2, "Lawan kata dari ukuran tinggi adalah ....", ["rendah", "pendek", "kecil", "sempit"], "A", "Ukuran vertikal tegak berpasangan: tinggi dan rendah.", "Tertukar konsep tinggi-rendah dengan panjang-pendek")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Kereta api lebih .... daripada sebuah mobil.", ["panjang", "pendek", "rendah", "kecil"], "A", "Kereta api memiliki gerbong berderet sehingga sangat panjang.")
mc("c2", "mudah", T, Kn, S2, "Gedung bertingkat lebih .... daripada rumah satu lantai.", ["tinggi", "rendah", "pendek", "tipis"], "A", "Gedung bertingkat menjulang tinggi ke atas.")
tf("c2", "mudah", T, Kn, S4, "Tali 12 cm lebih panjang daripada tali 8 cm.", "Benar", "12 cm lebih panjang daripada 8 cm.", verifikasi={"ekspresi": "12", "hasil": "12"})
sa("c2", "mudah", T, Kn, S3, "Ada pensil A 15 cm dan B 11 cm. Berapa cm pensil yang lebih panjang?", "15", "Pensil A dengan panjang 15 cm lebih panjang.", verifikasi={"ekspresi": "15", "hasil": "15"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Pensil A dan B disejajarkan pangkalnya. Ujung B lebih maju. Pensil mana lebih panjang?", ["pensil B", "pensil A", "keduanya sama", "tidak tahu"], "A", "Ujung yang lebih menjulur saat pangkal rata adalah lebih panjang.", "Salah menentukan benda lebih panjang saat pangkal sejajar")
mc("c3", "sedang", R, Pr, S4, "Urutan dari terpanjang: pita 15 cm, 5 cm, 9 cm adalah ....", ["15 cm, 9 cm, 5 cm", "5 cm, 9 cm, 15 cm", "9 cm, 15 cm, 5 cm", "15 cm, 5 cm, 9 cm"], "A", "Dari terpanjang: 15 cm, 9 cm, lalu 5 cm.", "Salah mengurutkan panjang benda dari yang terpanjang")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berapa cm selisih panjang penggaris 20 cm dan pensil 12 cm?", ["8 cm", "6 cm", "10 cm", "7 cm"], "A", "20 - 12 = 8 cm.", verifikasi={"ekspresi": "20 - 12", "hasil": "8"})
mc("c3", "sedang", T, Pr, S2, "Pohon A tingginya 5 meter. Pohon B tingginya 9 meter. Berapa selisih tingginya?", ["4 meter", "5 meter", "3 meter", "2 meter"], "A", "9 - 5 = 4 meter.", verifikasi={"ekspresi": "9 - 5", "hasil": "4"})
tf("c3", "sedang", T, Pr, S3, "Dua tongkat sama panjang jika kedua ujungnya bertemu pas saat disejajarkan.", "Benar", "Kedua ujung sama rata berarti panjangnya sama persis.")
mc("c3", "sedang", T, Pr, S4, "Ada tali 3 cm, 10 cm, 7 cm. Berapa cm panjang tali di posisi tengah?", ["7 cm", "3 cm", "10 cm", "5 cm"], "A", "Urutan panjang: 3 cm, 7 cm, 10 cm. Posisi tengah adalah 7 cm.", verifikasi={"ekspresi": "7", "hasil": "7"})
tf("c3", "sedang", T, Pr, S1, "Penghapus 3 cm lebih panjang daripada pensil 14 cm.", "Salah", "Penghapus 3 cm jauh lebih pendek.")
sa("c3", "mudah", T, Pr, S2, "Tiang bendera 7 meter dan tiang lampu 4 meter. Berapa selisih tingginya?", "3", "7 - 4 = 3 meter.", verifikasi={"ekspresi": "7 - 4", "hasil": "3"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Boni punya tali 16 cm. Dito punya tali 10 cm. Berapa cm kelebihan tali Boni?", ["6 cm", "5 cm", "7 cm", "8 cm"], "A", "16 - 10 = 6 cm.", verifikasi={"ekspresi": "16 - 10", "hasil": "6"})
mc("c3", "sedang", X, Pr, S2, "Tinggi Doni 118 cm, tinggi Eko 110 cm. Berapa cm Doni lebih tinggi dari Eko?", ["8 cm", "6 cm", "10 cm", "7 cm"], "A", "118 - 110 = 8 cm.", verifikasi={"ekspresi": "118 - 110", "hasil": "8"})
tf("c3", "sedang", X, Pr, S3, "Benda yang pangkalnya maju pasti ukuran aslinya lebih panjang.", "Salah", "Harus diratakan dulu pangkalnya agar adil.")
sa("c3", "sedang", X, Pr, S4, "Urutkan panjang 18 cm, 6 cm, 12 cm dari terpendek. Berapa cm pita pertama?", "6", "Paling pendek adalah 6 cm.", verifikasi={"ekspresi": "6", "hasil": "6"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Panjang buku 25 cm dan kotak pensil 19 cm. Berapa cm selisih panjangnya?", ["6 cm", "5 cm", "7 cm", "8 cm"], "A", "25 - 19 = 6 cm.", verifikasi={"ekspresi": "25 - 19", "hasil": "6"})
mc("c3", "sedang", K, Pr, S3, "Ada dua sedotan: merah 14 cm dan putih 9 cm. Sedotan merah lebih panjang ....", ["5 cm", "4 cm", "6 cm", "3 cm"], "A", "14 - 9 = 5 cm.", verifikasi={"ekspresi": "14 - 9", "hasil": "5"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Tongkat A lebih panjang dari B. Tongkat B lebih panjang dari C. Terpanjang adalah ....", ["tongkat A", "tongkat B", "tongkat C", "keduanya sama"], "A", "A > B > C, maka A adalah tongkat terpanjang.")
mc("c4", "sedang", T, Kn, S2, "Pohon mangga lebih rendah dari kelapa. Kelapa lebih rendah dari beringin. Siapa tertinggi?", ["pohon beringin", "pohon kelapa", "pohon mangga", "semua sama"], "A", "Beringin > kelapa > mangga, maka beringin paling tinggi.")
tf("c4", "sedang", T, Kn, S3, "Jika pangkal dua sedotan sejajar rata, sedotan terpanjang akan menonjol lebih jauh.", "Benar", "Ujungnya akan lebih menjulur ke depan.")
tf("c4", "sedang", T, Kn, S4, "Urutan 4 cm, 8 cm, 12 cm tersusun dari terpanjang ke terpendek.", "Salah", "4 < 8 < 12, tersusun dari terpendek ke terpanjang.")
sa("c4", "sedang", T, Kn, S4, "Pita merah 15 cm, biru 8 cm, hijau 11 cm. Berapa cm panjang pita terpanjang?", "15", "Paling panjang adalah pita merah 15 cm.", verifikasi={"ekspresi": "15", "hasil": "15"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Pensil A (12 cm) dipotong 2 cm. Berapa cm panjang pensil A sekarang?", ["10 cm", "11 cm", "9 cm", "8 cm"], "A", "12 - 2 = 10 cm.", verifikasi={"ekspresi": "12 - 2", "hasil": "10"})
mc("c4", "sedang", X, Kn, S2, "Tinggi adik 90 cm. Kakak lebih tinggi 20 cm. Berapa cm tinggi kakak?", ["110 cm", "100 cm", "115 cm", "120 cm"], "A", "90 + 20 = 110 cm.", verifikasi={"ekspresi": "90 + 20", "hasil": "110"})
tf("c4", "sedang", X, Kn, S3, "Mengukur panjang tali yang terlipat menghasilkan ukuran yang sebenarnya.", "Salah", "Tali harus diluruskan agar ukurannya tepat.")
mc("c4", "sulit", X, Me, S4, "Ada 3 tongkat: 5 cm, 9 cm, 14 cm. Berapa selisih terpanjang dan terpendek?", ["9 cm", "8 cm", "10 cm", "5 cm"], "A", "14 - 5 = 9 cm.", verifikasi={"ekspresi": "14 - 5", "hasil": "9"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Mengapa penggaris guru disebut lebih panjang daripada pensil siswa?", ["karena jarak dari ujung ke ujung penggaris lebih jauh", "karena warna penggaris lebih gelap", "karena penggaris lebih berat", "karena penggaris dari kayu"], "A", "Panjang didefinisikan sebagai jarak dari satu ujung ke ujung lain.")
mc("c4", "sulit", K, Me, S2, "Tinggi tiang A 12 meter. Tiang B 8 meter. Berapa jumlah tinggi kedua tiang?", ["20 meter", "18 meter", "22 meter", "16 meter"], "A", "12 + 8 = 20 meter.", verifikasi={"ekspresi": "12 + 8", "hasil": "20"})
tf("c4", "sulit", K, Me, S3, "Dua pensil yang ditaruh sejajar dengan panjang sama akan membentuk garis rata di kedua ujung.", "Benar", "Kedua ujungnya rata sejajar.")
mc("c4", "sulit", K, Me, S4, "Pita 20 cm dipotong menjadi dua bagian: 12 cm dan ....", ["8 cm", "7 cm", "9 cm", "10 cm"], "A", "20 - 12 = 8 cm.", verifikasi={"ekspresi": "20 - 12", "hasil": "8"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Dua tali disambung: tali A (7 cm) dan tali B (8 cm). Berapa total panjang sambungan?", ["15 cm", "14 cm", "16 cm", "13 cm"], "A", "7 + 8 = 15 cm.", verifikasi={"ekspresi": "7 + 8", "hasil": "15"})
mc("c5", "sedang", T, Me, S2, "Pohon kelapa 10 meter. Pohon pisang 3 meter. Berapa meter pohon kelapa melampaui pohon pisang?", ["7 meter", "6 meter", "8 meter", "5 meter"], "A", "10 - 3 = 7 meter.", verifikasi={"ekspresi": "10 - 3", "hasil": "7"})
mc("c5", "sedang", T, Me, S3, "Beni meletakkan pensil pendek lebih maju dari pensil panjang. Apa akibat perbuatannya?", ["pensil pendek tampak seolah lebih panjang", "pensil panjang makin panjang", "ukuran pensil berubah", "tidak ada pengaruh"], "A", "Mendorong ke depan menciptakan ilusi lebih panjang.")
mc("c5", "sulit", T, Me, S4, "Tali 18 cm dipotong 6 cm untuk layangan. Berapa cm sisa tali?", ["12 cm", "11 cm", "13 cm", "10 cm"], "A", "18 - 6 = 12 cm.", verifikasi={"ekspresi": "18 - 6", "hasil": "12"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Ada tiga ranting: 6 cm, 11 cm, 15 cm. Berapa selisih ranting terpanjang dan terpendek?", ["9 cm", "8 cm", "10 cm", "7 cm"], "A", "15 - 6 = 9 cm.", verifikasi={"ekspresi": "15 - 6", "hasil": "9"})
mc("c5", "sulit", K, Me, S4, "Kawat 20 cm dibagi dua sama panjang. Berapa cm panjang tiap bagian?", ["10 cm", "8 cm", "12 cm", "9 cm"], "A", "20 / 2 = 10 cm.", verifikasi={"ekspresi": "20 // 2", "hasil": "10"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Rancanglah susunan 3 benda dari yang tertinggi ke terendah!", ["tiang bendera, lemari, kursi", "kursi, lemari, tiang bendera", "lemari, kursi, tiang bendera", "kursi, tiang bendera, lemari"], "A", "Tiang bendera paling tinggi, lemari sedang, kursi paling rendah.")
mc("c6", "sulit", K, Me, S3, "Susunlah cara membandingkan panjang dua tali yang kusut secara tepat!", ["luruskan kedua tali lalu sejajarkan ujung pangkalnya", "langsung bandingkan saat tali masih terlipat", "ukur hanya salah satu tali", "tarik salah satu tali lebih kencang"], "A", "Luruskan kedua tali dan sejajarkan ujung pangkalnya pada garis yang sama.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Susunlah 3 sedotan berukuran 4 cm, 6 cm, 8 cm secara berurutan. Berapa total panjang ketiganya?", ["18 cm", "16 cm", "20 cm", "14 cm"], "A", "4 + 6 + 8 = 18 cm.", verifikasi={"ekspresi": "4 + 6 + 8", "hasil": "18"})
mc("c6", "sulit", P, Me, S4, "Jika kamu ingin menyusun pagar dari bambu terpanjang, urutan manakah yang tepat?", ["15 m, 12 m, 9 m, 6 m", "6 m, 9 m, 12 m, 15 m", "12 m, 15 m, 9 m, 6 m", "9 m, 6 m, 12 m, 15 m"], "A", "Dari terpanjang: 15 m, 12 m, 9 m, lalu 6 m.")

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab21_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab21.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
