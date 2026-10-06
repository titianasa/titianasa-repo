#!/usr/bin/env python3
"""
Generator dan validator Bab 61 Matematika Kelas 2 SD:
"Mengenal Penggaris dan Sentimeter" (Fase A)
bab_id: 8494241d-f68c-4d53-acad-2055e7ed9ca6
article_id: ade8df9e-37b2-45c5-b1e3-68e5bdc49c22
quiz_id: ed99c459-27e9-4510-b69e-fd73080a15cb
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "f1h2j3l4n501"  # Mengenal Alat Ukur Penggaris
S2 = "g2i3k4m5o602"  # Satuan Baku Sentimeter (cm)
S3 = "h3j4l5n6p703"  # Garis-Garis pada Penggaris
S4 = "i4k5m6o7q804"  # Membaca Nilai Ukur Sederhana

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Penggaris adalah alat ukur panjang.
Bentuknya lurus dan pipih.
Bisa terbuat dari plastik.
Bisa juga dari kayu.
Penggaris mengukur benda yang pendek.
Contohnya pensil dan buku tulis.
Benda lurus mudah diukur penggaris.
Gunakan penggaris untuk mengukur rapi!

:::definition
title: Penggaris
Alat untuk mengukur panjang benda-benda pendek yang lurus.
:::"""

s2_content = """Pada penggaris ada satuan baku.
Satuan itu adalah sentimeter.
Sentimeter disingkat menjadi cm.
Huruf c dan m kecil.
Hasil ukur sentimeter selalu sama.
Siapa pun yang mengukur hasilnya sama.
Ini beda dengan jengkal tangan!
Jengkal setiap orang bisa berbeda.

:::steps
title: Menuliskan Satuan Sentimeter
1. Tulis angka hasil ukur.
2. Beri spasi kecil.
3. Tulis singkatan cm dengan huruf kecil.
:::"""

s3_content = """Lihatlah angka pada penggaris.
Ada deretan angka teratur.
Dimulai dari angka nol.
Lalu satu, dua, tiga, seterusnya.
Ada garis panjang bernomor.
Jarak antarangka adalah satu sentimeter.
Dari 0 ke 1 adalah 1 cm.
Dari 0 ke 2 adalah 2 cm.
Semua jarak garis bernomor sama rata!"""

s4_content = """Bagaimana membaca panjang benda?
Letakkan ujung benda di angka nol.
Lalu lihat ujung yang lain.
Jika tepat di angka 10.
Maka panjang benda adalah 10 cm.
Bila berujung di angka 15.
Panjang benda adalah 15 cm.
Membaca penggaris sangat mudah!

:::common_trap
title: Mengira Singkatan Sentimeter Menggunakan Huruf Kapital
Sentimeter disingkat cm, bukan CM atau Cm.
Gunakan huruf kecil untuk singkatan satuan baku!
:::

:::callout
variant: summary
title: Ringkasan
text: Penggaris mengukur panjang benda. Sentimeter disingkat cm. Ukuran dimulai dari nol.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Alat Ukur Penggaris",
        "minutes": 6,
        "goal": "Siswa mengenal fungsi penggaris sebagai alat ukur panjang benda pendek yang lurus.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Satuan Baku Sentimeter (cm)",
        "minutes": 6,
        "goal": "Siswa memahami sentimeter (cm) sebagai satuan baku pengukur panjang.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Garis-Garis pada Penggaris",
        "minutes": 6,
        "goal": "Siswa memahami skala angka dan jarak 1 sentimeter antarangka pada penggaris.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Membaca Nilai Ukur Sederhana",
        "minutes": 6,
        "goal": "Siswa mampu membaca nilai panjang benda dari angka 0 sampai ujung benda.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengenal Penggaris dan Sentimeter",
    "topic": "Mengukur Panjang dan Berat",
    "level": "Kelas 2 SD · Fase A",
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
# 2. DEFINISI BANK 50 SOAL BAB 61
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
mc("c1", "mudah", D, F, S1, "Alat yang paling tepat untuk mengukur panjang pensil adalah ....", ["penggaris", "termometer", "timbangan", "jam dinding"], "A", "Penggaris digunakan untuk mengukur panjang benda pendek.")
tf("c1", "mudah", D, F, S2, "Sentimeter adalah contoh satuan baku pengukur panjang.", "Benar", "Sentimeter adalah satuan baku.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Singkatan baku yang benar untuk sentimeter adalah ....", ["cm", "km", "kg", "sm"], "A", "Sentimeter disingkat cm dengan huruf kecil.")
mc("c1", "mudah", T, F, S3, "Angka awal yang tertulis pada pangkal penggaris adalah ....", ["0", "1", "10", "100"], "A", "Penggaris dimulai dari angka 0.", verifikasi={"ekspresi": "0 / 1", "hasil": "0"})
sa("c1", "mudah", T, F, S4, "Pensil dari angka 0 sampai 12 memiliki panjang ... cm.", "12", "Panjangnya adalah 12 cm.", verifikasi={"ekspresi": "12 - 0", "hasil": "12"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Benda manakah yang paling mudah diukur menggunakan penggaris?", ["buku tulis", "lingkar pohon", "jalan raya", "lapangan bola"], "A", "Buku tulis bentuknya lurus dan pendek.")
tf("c2", "mudah", D, Kn, S2, "Hasil ukur dengan jengkal selalu sama untuk setiap orang.", "Salah", "Jengkal tiap orang berbeda-beda ukurannya.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Mengapa kita menggunakan sentimeter dan bukan jengkal tangan?", ["karena hasil sentimeter selalu sama bagi semua orang", "karena jengkal terlalu panjang", "karena penggaris berwarna warni", "karena jengkal tidak bisa dipakai"], "A", "Sentimeter adalah satuan baku sehingga hasilnya tetap.", "Belum paham keunggulan satuan baku")
mc("c2", "mudah", R, Kn, S4, "Penghapus diletakkan dari 0 hingga 4 cm. Panjangnya adalah ....", ["4 cm", "0 cm", "5 cm", "3 cm"], "A", "4 - 0 = 4 cm.", "Bingung membaca ujung skala penggaris", verifikasi={"ekspresi": "4 - 0", "hasil": "4"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Benda manakah yang permukaannya paling cocok diukur dengan penggaris lurus?", ["tepi meja tulis", "bola sepak", "topi bundar", "gelas minum"], "A", "Tepi meja tulis berbentuk lurus.")
mc("c2", "mudah", T, Kn, S4, "Krayon diletakkan dari angka 0 sampai 8. Panjang krayon adalah ....", ["8 cm", "7 cm", "9 cm", "0 cm"], "A", "Panjangnya 8 cm.", verifikasi={"ekspresi": "8 - 0", "hasil": "8"})
tf("c2", "mudah", T, Kn, S3, "Jarak dari angka 0 ke 5 pada penggaris adalah 5 cm.", "Benar", "5 - 0 = 5 cm.")
sa("c2", "mudah", T, Kn, S4, "Jepit kertas dari angka 0 ke angka 3 panjangnya ... cm.", "3", "3 - 0 = 3 cm.", verifikasi={"ekspresi": "3 - 0", "hasil": "3"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S4, "Ranting diukur dari 0 sampai 14 cm. Berapakah panjang ranting tersebut?", ["14 cm", "13 cm", "15 cm", "10 cm"], "A", "Panjang = 14 - 0 = 14 cm.", "Salah membaca angka akhir", verifikasi={"ekspresi": "14 - 0", "hasil": "14"})
mc("c3", "sedang", R, Pr, S3, "Berapa sentimeter jarak antara angka 4 dan angka 9 pada penggaris?", ["5 cm", "4 cm", "9 cm", "13 cm"], "A", "9 - 4 = 5 cm.", "Hanya melihat angka terakhir tanpa menghitung selisih", verifikasi={"ekspresi": "9 - 4", "hasil": "5"})

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Manakah benda yang TIDAK cocok diukur dengan penggaris pendek 30 cm?", ["panjang jalan raya", "panjang pensil", "lebar buku", "panjang penghapus"], "A", "Jalan raya terlalu panjang untuk penggaris 30 cm.")
mc("c3", "mudah", T, Pr, S4, "Pita diukur dari 0 sampai 18 cm. Panjang pita adalah ....", ["18 cm", "17 cm", "19 cm", "16 cm"], "A", "18 - 0 = 18 cm.", verifikasi={"ekspresi": "18 - 0", "hasil": "18"})
tf("c3", "sedang", T, Pr, S3, "Jarak dari angka 3 ke angka 7 sama dengan 4 cm.", "Benar", "7 - 3 = 4 cm.")
mc("c3", "sedang", T, Pr, S4, "Dua pensil masing-masing 10 cm digabung lurus. Total panjangnya adalah ....", ["20 cm", "15 cm", "25 cm", "10 cm"], "A", "10 + 10 = 20 cm.", verifikasi={"ekspresi": "10 + 10", "hasil": "20"})
tf("c3", "sedang", T, Pr, S2, "Satuan meter dan sentimeter menghasilkan ukuran yang tidak baku.", "Salah", "Meter dan sentimeter adalah satuan baku.")
sa("c3", "sedang", T, Pr, S4, "Spidol dari angka 0 sampai 15 cm memiliki panjang ... cm.", "15", "15 - 0 = 15 cm.", verifikasi={"ekspresi": "15 - 0", "hasil": "15"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S2, "Panjang buku 25 cm. Jika ditulis singkat, penulisan yang benar adalah ....", ["25 cm", "25 CM", "25 Cm", "25 cM"], "A", "Singkatan cm harus huruf kecil.")
mc("c3", "sedang", X, Pr, S3, "Berapa jarak dari angka 6 ke angka 13 pada penggaris?", ["7 cm", "6 cm", "8 cm", "19 cm"], "A", "13 - 6 = 7 cm.", verifikasi={"ekspresi": "13 - 6", "hasil": "7"})
tf("c3", "sedang", X, Pr, S4, "Tali dari angka 0 sampai angka 22 memiliki panjang 22 cm.", "Benar", "22 - 0 = 22 cm.")
sa("c3", "sedang", X, Pr, S4, "Berapa cm panjang penggaris jika berujung di angka 30 dari nol?", "30", "30 - 0 = 30 cm.", verifikasi={"ekspresi": "30 - 0", "hasil": "30"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Berapa langkah 1 cm dari angka 5 sampai angka 11?", ["6 langkah", "5 langkah", "7 langkah", "4 langkah"], "A", "11 - 5 = 6 langkah.", verifikasi={"ekspresi": "11 - 5", "hasil": "6"})
mc("c3", "sedang", K, Pr, S4, "Panjang sedotan dari 0 sampai 16 cm. Berapa panjang sedotan itu?", ["16 cm", "15 cm", "17 cm", "14 cm"], "A", "16 - 0 = 16 cm.", verifikasi={"ekspresi": "16 - 0", "hasil": "16"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa penggaris plastik lentur kurang tepat untuk menggaris lurus?", ["karena mudah melengkung saat ditekan", "karena warnanya tembus pandang", "karena tidak ada angkanya", "karena terlalu panjang"], "A", "Bahan lentur dapat berbelok atau melengkung.")
mc("c4", "sedang", T, Kn, S2, "Budi mengukur meja 80 cm, Siti mengukur 80 cm. Mengapa hasilnya sama?", ["karena sentimeter adalah satuan baku yang nilainya tetap", "karena mereka berteman", "karena mejanya kecil", "karena melihat gambar"], "A", "Satuan baku memberikan hasil yang konsisten.")
tf("c4", "sedang", T, Kn, S3, "Jarak angka 2 ke 6 lebih panjang daripada jarak angka 10 ke 13.", "Benar", "6 - 2 = 4 cm, sedangkan 13 - 10 = 3 cm. 4 cm > 3 cm.")
tf("c4", "sedang", T, Kn, S4, "Benda dari angka 1 sampai angka 8 memiliki panjang 8 cm.", "Salah", "Panjangnya adalah 8 - 1 = 7 cm, bukan 8 cm.")
sa("c4", "sedang", T, Kn, S3, "Berapakah selisih jarak antara (0 ke 9 cm) dan (0 ke 4 cm)?", "5", "9 - 4 = 5 cm.", verifikasi={"ekspresi": "9 - 4", "hasil": "5"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Manakah yang paling tepat diukur menggunakan meteran gulung?", ["panjang pintu kelas", "panjang penghapus", "panjang permen", "lebar perangko"], "A", "Pintu kelas panjangnya melebihi penggaris 30 cm.")
mc("c4", "sedang", X, Kn, S3, "Jarak angka 4 ke 10 sama panjangnya dengan jarak angka ....", ["10 ke 16", "10 ke 15", "10 ke 14", "10 ke 18"], "A", "10 - 4 = 6 cm. 16 - 10 = 6 cm.")
tf("c4", "sedang", X, Kn, S2, "Mengukur panjang dengan korek api menghasilkan satuan baku.", "Salah", "Korek api adalah satuan tidak baku.")
mc("c4", "sulit", X, Me, S4, "Pita merah 12 cm, pita biru 19 cm. Berapakah selisih panjang keduanya?", ["7 cm", "6 cm", "8 cm", "5 cm"], "A", "19 - 12 = 7 cm.", verifikasi={"ekspresi": "19 - 12", "hasil": "7"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Mengapa penggaris kayu lebih kaku dibandingkan penggaris plastik tipis?", ["karena sifat bahan kayu padat dan tebal", "karena ada angkanya", "karena dicat warna", "karena bentuknya bulat"], "A", "Bahan kayu tidak mudah meliuk saat ditarik garis.")
mc("c4", "sulit", K, Me, S3, "Sebuah benda ditaruh dari angka 5 sampai 17. Berapa panjangnya?", ["12 cm", "17 cm", "5 cm", "11 cm"], "A", "17 - 5 = 12 cm.", verifikasi={"ekspresi": "17 - 5", "hasil": "12"})
tf("c4", "sulit", K, Me, S4, "Dua pensil masing-masing 9 cm bila disambung panjangnya 20 cm.", "Salah", "9 + 9 = 18 cm, bukan 20 cm.")
mc("c4", "sulit", K, Me, S2, "Mengapa satuan baku sangat penting dalam perdagangan internasional?", ["agar ukuran barang yang dikirim tepat dan adil bagi semua", "agar terlihat hebat", "karena harganya mahal", "karena bahasa asing"], "A", "Satuan baku menjamin keadilan dan kepastian ukuran di mana pun.")

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Penggaris 30 cm dipatahkan jadi dua: 12 cm dan .... Berapa sisanya?", ["18 cm", "16 cm", "14 cm", "20 cm"], "A", "30 - 12 = 18 cm.", verifikasi={"ekspresi": "30 - 12", "hasil": "18"})
mc("c5", "sedang", T, Me, S2, "Pita 24 cm dipotong menjadi 4 bagian sama panjang. Berapa panjang tiap bagian?", ["6 cm", "5 cm", "7 cm", "8 cm"], "A", "24 : 4 = 6 cm.", verifikasi={"ekspresi": "24 / 4", "hasil": "6"})
mc("c5", "sedang", T, Me, S3, "Berapakah hasil dari (jarak 0 ke 15 cm) + (jarak 2 ke 8 cm)?", ["21 cm", "20 cm", "22 cm", "19 cm"], "A", "15 + (8 - 2) = 15 + 6 = 21 cm.", verifikasi={"ekspresi": "15 + (8 - 2)", "hasil": "21"})
mc("c5", "sulit", T, Me, S4, "Tali A panjangnya 35 cm. Tali B 12 cm lebih pendek. Berapa panjang tali B?", ["23 cm", "22 cm", "24 cm", "20 cm"], "A", "35 - 12 = 23 cm.", verifikasi={"ekspresi": "35 - 12", "hasil": "23"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Penggaris patah ujungnya, skala mulai angka 3. Benda sampai angka 18. Panjangnya?", ["15 cm", "18 cm", "21 cm", "14 cm"], "A", "18 - 3 = 15 cm.", verifikasi={"ekspresi": "18 - 3", "hasil": "15"})
mc("c5", "sulit", K, Me, S4, "Tiga batang lidi masing-masing 8 cm, 12 cm, dan 15 cm digabung. Panjang total?", ["35 cm", "32 cm", "36 cm", "30 cm"], "A", "8 + 12 + 15 = 35 cm.", verifikasi={"ekspresi": "8 + 12 + 15", "hasil": "35"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Bagaimana cara mengukur keliling buku jika hanya punya penggaris 15 cm?", ["ukur tiap sisi satu per satu lalu jumlahkan semua panjang sisinya", "cukup tebak saja", "lipat bukunya", "gunakan timbangan"], "A", "Mengukur setiap sisi dengan penggaris lalu menjumlahkannya.")
mc("c6", "sulit", K, Me, S4, "Kayu 50 cm dipotong 3 kali masing-masing 12 cm. Berapa sisa panjang kayu?", ["14 cm", "16 cm", "12 cm", "18 cm"], "A", "3 x 12 = 36 cm; 50 - 36 = 14 cm.", verifikasi={"ekspresi": "50 - (3 * 12)", "hasil": "14"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi: (3 x 14 cm) - (2 x 15 cm) + 8 cm!", ["20 cm", "18 cm", "22 cm", "16 cm"], "A", "42 - 30 + 8 = 12 + 8 = 20 cm.", verifikasi={"ekspresi": "(3 * 14) - (2 * 15) + 8", "hasil": "20"})
mc("c6", "sulit", P, Me, S3, "Rantai terdiri dari 5 cincin. Tiap cincin menambah 4 cm. Berapa panjang 5 cincin?", ["20 cm", "16 cm", "24 cm", "18 cm"], "A", "5 x 4 = 20 cm.", verifikasi={"ekspresi": "5 * 4", "hasil": "20"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab61_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab61.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
