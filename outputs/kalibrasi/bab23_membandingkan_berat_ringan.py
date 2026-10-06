#!/usr/bin/env python3
"""
Generator dan validator Bab 23 Matematika Kelas 1 SD:
"Membandingkan Berat dan Ringan" (Fase A)
bab_id: 3c9e530c-124c-4ae6-8f27-4c4fe95290d4
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "c3d2e11f4a01"  # Mengenal Berat dan Ringan
S2 = "d4e3f22a5b12"  # Membandingkan Berat dengan Kedua Tangan
S3 = "e5f4a33b6c23"  # Membandingkan dengan Timbangan Sederhana
S4 = "f6a5b44c7d34"  # Ukuran Besar Belum Tentu Lebih Berat

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Benda memiliki berat yang berbeda.
Ada benda yang berat.
Ada juga benda yang ringan.
Buku tebal terasa berat diangkat.
Kertas selembar terasa sangat ringan.
Bulu ayam melayang karena ringan.
Batu besar sulit kita angkat.

:::definition
title: Berat dan Ringan
Berat adalah tarikan beban saat diangkat.
Ringan adalah beban yang mudah diangkat.
:::"""

s2_content = """Kita bisa menimbang dengan tangan.
Gunakan tangan kiri dan kanan.
Letakkan buku di tangan kanan.
Letakkan pensil di tangan kiri.
Rasakan tarikan ke bawahnya.
Tangan kanan merasa lebih tertekan.
Artinya buku lebih berat.

:::steps
title: Menimbang dengan Tangan
1. Angkat kedua tangan ke depan.
2. Letakkan satu benda pada tiap telapak.
3. Rasakan tangan yang lebih tertarik ke bawah.
:::"""

s3_content = """Gunakan gantungan baju sebagai timbangan.
Gantungkan dua kantong di ujungnya.
Sisi yang turun lebih berat.
Sisi yang naik lebih ringan.
Bila lurus sejajar artinya seimbang.
Kedua benda itu sama berat.
Timbangan sederhana sangat membantu kita.
Alat ini bekerja sangat adil."""

s4_content = """Hati-hati dengan ukuran benda.
Ukuran besar belum tentu berat.
Balon tiup berukuran sangat besar.
Namun balon sangat ringan melayang.
Kelereng kaca berukuran cukup kecil.
Namun kelereng lebih berat.

:::common_trap
title: Benda Besar Belum Tentu Berat
Benda berukuran besar belum tentu berat.
Balon udara berukuran sangat besar.
Namun balon sangat ringan ditiup.
Sebaliknya batu kecil terasa berat.
Jangan tertipu oleh besar bendanya.
:::

:::callout
variant: summary
title: Ringkasan
text: Sisi timbangan yang turun lebih berat. Sisi yang naik lebih ringan. Benda besar belum tentu lebih berat.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Berat dan Ringan",
        "minutes": 6,
        "goal": "Siswa dapat membedakan konsep berat dan ringan pada benda-benda di sekitarnya.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Membandingkan Berat dengan Kedua Tangan",
        "minutes": 6,
        "goal": "Siswa dapat membandingkan berat dua benda secara langsung menggunakan kedua belah tangan.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membandingkan dengan Timbangan Sederhana",
        "minutes": 6,
        "goal": "Siswa dapat membaca hasil timbangan sederhana (sisi turun lebih berat, sisi naik lebih ringan, sejajar seimbang).",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Ukuran Besar Belum Tentu Lebih Berat",
        "minutes": 6,
        "goal": "Siswa memahami bahwa volume atau ukuran benda yang besar tidak selalu berarti benda tersebut lebih berat.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membandingkan Berat dan Ringan",
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
# 2. DEFINISI BANK 50 SOAL BAB 23
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
mc("c1", "mudah", D, F, S1, "Lawan kata dari benda berat adalah benda ....", ["ringan", "panjang", "tinggi", "luas"], "A", "Lawan kata berat adalah ringan.")
tf("c1", "mudah", D, F, S3, "Pada timbangan sederhana, sisi yang turun menandakan benda lebih berat.", "Benar", "Benda lebih berat akan menekan sisi timbangan ke bawah.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Benda yang paling ringan di antara berikut adalah ....", ["selembar kapas", "sebuah semangka", "batu bata", "lemari kayu"], "A", "Kapas sangat ringan dan mudah terbawa angin.")
mc("c1", "mudah", T, F, S2, "Saat menimbang dengan tangan, benda diletakkan di atas ....", ["telapak tangan", "siku tangan", "pundak", "kepala"], "A", "Kita menaruh benda pada kedua telapak tangan.")
sa("c1", "mudah", T, F, S3, "Jika timbangan lurus sejajar rata, kedua benda disebut sama?", "berat", "Lurus sejajar menandakan berat kedua benda sama.")

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Balon karet yang ditiup besar terasa sangat ....", ["ringan", "berat", "panjang", "keras"], "A", "Balon berisi udara sehingga tetap sangat ringan.")
tf("c2", "mudah", D, Kn, S2, "Tangan yang merasakan tarikan lebih kuat memegang benda yang lebih berat.", "Benar", "Beban berat menarik tangan ke bawah lebih kuat.")

# Remedial (2)
mc("c2", "mudah", R, F, S4, "Apakah benda yang berukuran besar pasti lebih berat?", ["belum tentu", "pasti selalu berat", "selalu paling ringan", "tidak pernah berat"], "A", "Ukuran besar belum tentu berat, seperti balon dan bantal busa.", "Mengira benda besar selalu lebih berat")
mc("c2", "mudah", R, Kn, S3, "Pada timbangan gantungan baju, sisi yang naik menandakan benda lebih ....", ["ringan", "berat", "panjang", "besar"], "A", "Sisi yang terangkat ke atas adalah sisi benda lebih ringan.", "Tertukar posisi timbangan naik dan turun")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Batu kerikil lebih .... daripada sebuah meja kayu.", ["ringan", "berat", "panjang", "tinggi"], "A", "Kerikil kecil jauh lebih ringan dari meja kayu.")
mc("c2", "mudah", T, Kn, S2, "Buku di tangan kanan terasa lebih berat. Maka pensil di tangan kiri lebih ....", ["ringan", "berat", "besar", "panjang"], "A", "Lawan dari lebih berat adalah lebih ringan.")
tf("c2", "mudah", T, Kn, S4, "Batu kecil selalu lebih ringan daripada balon tiup yang besar.", "Salah", "Batu kecil padat lebih berat daripada balon berisi udara.")
sa("c2", "mudah", T, Kn, S3, "Sebuah apel seberat 5 kelereng. Berapa kelereng berat apel itu?", "5", "Beratnya setara dengan 5 butir kelereng.", verifikasi={"ekspresi": "5", "hasil": "5"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Tangan kiri memegang melon, tangan kanan memegang jeruk. Tangan manakah turun lebih rendah?", ["tangan kiri", "tangan kanan", "keduanya sejajar", "tidak bergerak"], "A", "Melon lebih berat sehingga tangan kiri turun lebih rendah.", "Salah menentukan tangan yang tertekan lebih ke bawah")
mc("c3", "sedang", R, Pr, S4, "Sebongkah kapas besar dan sebuah kelereng besi. Manakah benda yang lebih berat?", ["kelereng besi", "kapas besar", "keduanya sama", "tidak tahu"], "A", "Kelereng besi jauh lebih berat meski berukuran kecil.", "Terkecoh ukuran besar kapas dibanding kelereng besi")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berat mangga 6 kelereng. Jeruk 4 kelereng. Berapa jumlah kelereng keduanya?", ["10 kelereng", "9 kelereng", "11 kelereng", "8 kelereng"], "A", "6 + 4 = 10 kelereng.", verifikasi={"ekspresi": "6 + 4", "hasil": "10"})
mc("c3", "sedang", T, Pr, S2, "Tas sekolah seberat 8 buku. Tas adik 3 buku. Berapa selisih beratnya?", ["5 buku", "4 buku", "6 buku", "3 buku"], "A", "8 - 3 = 5 buku.", verifikasi={"ekspresi": "8 - 3", "hasil": "5"})
tf("c3", "sedang", T, Pr, S3, "Bila dua kantong seimbang di timbangan, kedua benda sama berat.", "Benar", "Posisi sejajar menandakan kedua beban sama berat.")
mc("c3", "sedang", T, Pr, S4, "Bantal busa besar seberat 2 apel. Semangka seberat 6 apel. Mana lebih berat?", ["semangka", "bantal busa", "keduanya sama", "tidak tahu"], "A", "Semangka setara 6 apel, bantal hanya 2 apel.")
tf("c3", "sedang", T, Pr, S1, "Bulu burung melayang karena bulu burung memiliki berat yang besar.", "Salah", "Bulu burung melayang karena sangat ringan.")
sa("c3", "mudah", T, Pr, S2, "Kotak pensil 7 kelereng. Penghapus 2 kelereng. Berapa selisih kelerengnya?", "5", "7 - 2 = 5 kelereng.", verifikasi={"ekspresi": "7 - 2", "hasil": "5"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Buku = 12 kelereng. Buku tipis = 5 kelereng. Berapa selisih kelerengnya?", ["7 kelereng", "6 kelereng", "8 kelereng", "5 kelereng"], "A", "12 - 5 = 7 kelereng.", verifikasi={"ekspresi": "12 - 5", "hasil": "7"})
mc("c3", "sedang", X, Pr, S2, "Siti membawa 4 apel di tangan kiri dan 4 apel di tangan kanan. Tangan Siti ....", ["sejajar seimbang", "kiri turun", "kanan turun", "naik semua"], "A", "Beban sama di kedua tangan membuat posisi sejajar seimbang.")
tf("c3", "sedang", X, Pr, S3, "Sisi timbangan yang terangkat ke atas menampung benda yang lebih berat.", "Salah", "Sisi terangkat menampung benda yang lebih ringan.")
sa("c3", "sedang", X, Pr, S4, "Sebuah kado beratnya 9 kelereng. Kado kecil 4 kelereng. Selisih beratnya?", "5", "9 - 4 = 5 kelereng.", verifikasi={"ekspresi": "9 - 4", "hasil": "5"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Benda A = 15 kelereng. Benda B = 8 kelereng. Berapa selisih beratnya?", ["7 kelereng", "6 kelereng", "8 kelereng", "5 kelereng"], "A", "15 - 8 = 7 kelereng.", verifikasi={"ekspresi": "15 - 8", "hasil": "7"})
mc("c3", "sedang", K, Pr, S3, "Sebuah boneka = 10 koin. Mobil mainan = 6 koin. Boneka lebih berat ....", ["4 koin", "3 koin", "5 koin", "2 koin"], "A", "10 - 6 = 4 koin.", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Benda A lebih berat dari B. Benda B lebih berat dari C. Benda terberat adalah ....", ["benda A", "benda B", "benda C", "sama semua"], "A", "A > B > C, maka benda A adalah yang terberat.")
mc("c4", "sedang", T, Kn, S2, "Doni mengangkat tas dengan satu jari terasa sakit, tapi botol tidak. Mengapa?", ["karena tas jauh lebih berat dari botol", "karena warna tas hitam", "karena botol dari plastik", "karena tas ada tali"], "A", "Beban tas yang berat memberikan tekanan kuat ke jari tangan.")
tf("c4", "sedang", T, Kn, S3, "Timbangan miring ke kiri berarti kantong kiri menampung benda lebih berat.", "Benar", "Sisi yang turun ke bawah adalah sisi yang lebih berat.")
tf("c4", "sedang", T, Kn, S4, "Dua benda berbeda bentuk pasti memiliki berat yang berbeda pula.", "Salah", "Benda berbeda bentuk bisa memiliki berat yang persis sama.")
sa("c4", "sedang", T, Kn, S4, "Apel = 5 kelereng. Jeruk = 3 kelereng. Berapa total kelereng untuk 2 apel?", "10", "5 + 5 = 10 kelereng.", verifikasi={"ekspresi": "5 + 5", "hasil": "10"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Jika 1 pepaya = 4 mangga, maka 3 pepaya seberat berapa mangga?", ["12 mangga", "10 mangga", "14 mangga", "8 mangga"], "A", "3 x 4 = 12 mangga.", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})
mc("c4", "sedang", X, Kn, S2, "Di tangan kanan ada batu 8 kelereng. Tangan kiri batu 11 kelereng. Ke arah mana miring?", ["ke arah tangan kiri", "ke arah tangan kanan", "tetap sejajar", "tidak tahu"], "A", "Tangan kiri memegang 11 kelereng (lebih berat) sehingga turun lebih rendah.")
tf("c4", "sedang", X, Kn, S4, "Semua benda yang terapung di air pasti berukuran sangat kecil.", "Salah", "Batang kayu besar atau perahu besar tetap dapat terapung.")
mc("c4", "sulit", X, Me, S3, "Benda A = 8 kelereng. Benda B = 5 kelereng. Berapa kelereng harus ditambah ke B agar seimbang?", ["3 kelereng", "2 kelereng", "4 kelereng", "5 kelereng"], "A", "8 - 5 = 3 kelereng.", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Mengapa perahu kertas bisa melayang di atas air?", ["karena kertas sangat ringan", "karena kertas menyerap air", "karena bentuk perahu tajam", "karena air berwarna biru"], "A", "Beban kertas yang ringan memungkinkannya mengapung.")
mc("c4", "sulit", K, Me, S2, "Edo memegang 14 kelereng di saku kiri dan 9 kelereng di saku kanan. Selisih beban saku?", ["5 kelereng", "4 kelereng", "6 kelereng", "3 kelereng"], "A", "14 - 9 = 5 kelereng.", verifikasi={"ekspresi": "14 - 9", "hasil": "5"})
tf("c4", "sulit", K, Me, S3, "Menggantung beban sama berat di kedua sisi akan membuat timbangan sejajar seimbang.", "Benar", "Beban yang sama berat akan membuat kedua lengan timbangan seimbang rata.")
mc("c4", "sulit", K, Me, S4, "Balon = 1 kelereng. Buku = 9 kelereng. Berapa selisih berat 1 buku dan 1 balon?", ["8 kelereng", "7 kelereng", "9 kelereng", "10 kelereng"], "A", "9 - 1 = 8 kelereng.", verifikasi={"ekspresi": "9 - 1", "hasil": "8"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Paket A (7 kg) digabung dengan Paket B (9 kg). Berapa total berat keduanya?", ["16 kg", "15 kg", "17 kg", "14 kg"], "A", "7 + 9 = 16 kg.", verifikasi={"ekspresi": "7 + 9", "hasil": "16"})
mc("c5", "sedang", T, Me, S2, "Tangan kanan membawa 12 apel. Diambil 4 apel. Berapa apel sisa di tangan kanan?", ["8 apel", "7 apel", "9 apel", "6 apel"], "A", "12 - 4 = 8 apel.", verifikasi={"ekspresi": "12 - 4", "hasil": "8"})
mc("c5", "sedang", T, Me, S3, "Di timbangan ada semangka (10 jeruk) dan melon (6 jeruk). Berapa selisihnya?", ["4 jeruk", "3 jeruk", "5 jeruk", "2 jeruk"], "A", "10 - 6 = 4 jeruk.", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})
mc("c5", "sulit", T, Me, S4, "Doni mengira semangka pasti lebih berat dari ember kosong besar. Apakah Doni benar?", ["benar, semangka lebih padat dan berat", "salah, ember lebih besar pasti lebih berat", "salah, keduanya sama ringan", "salah, semangka terapung"], "A", "Semangka padat dan berair sehingga jauh lebih berat daripada ember kosong.")

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Labu = 11 kelereng. Pepaya = 7 kelereng. Berapa selisih kelereng labu dan pepaya?", ["4 kelereng", "3 kelereng", "5 kelereng", "2 kelereng"], "A", "11 - 7 = 4 kelereng.", verifikasi={"ekspresi": "11 - 7", "hasil": "4"})
mc("c5", "sulit", K, Me, S3, "Timbangan menunjukkan 1 durian seimbang dengan 15 apel. Berapa apel untuk 1 durian?", ["15 apel", "14 apel", "16 apel", "13 apel"], "A", "Karena seimbang, berat 1 durian setara dengan 15 apel.", verifikasi={"ekspresi": "15", "hasil": "15"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Rancanglah cara sederhana mengetahui mana yang lebih berat antara apel dan jeruk!", ["letakkan apel di satu tangan dan jeruk di tangan lain lalu rasakan tekanannya", "ukur panjang kedua buah dengan penggaris", "lihat buah mana yang warnanya lebih cerah", "gelindingkan kedua buah di lantai"], "A", "Menimbang dengan kedua belah tangan adalah cara membandingkan berat.")
mc("c6", "sulit", K, Me, S3, "Susunlah alat timbangan gantung sederhana di rumah menggunakan barang bekas!", ["gantungan baju dengan dua kantong plastik di kedua ujungnya", "tali rafia yang digulung menjadi bola", "kardus bekas yang dilipat", "botol plastik yang diisi air penuh"], "A", "Gantungan baju dan dua kantong plastik berfungsi baik sebagai timbangan gantung.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "1 nanas = 3 mangga. 1 mangga = 2 apel. Berapa apel seberat 1 nanas?", ["6 apel", "5 apel", "7 apel", "8 apel"], "A", "3 x 2 = 6 apel.", verifikasi={"ekspresi": "3 * 2", "hasil": "6"})
mc("c6", "sulit", P, Me, S4, "1 balok kayu = 8 kelereng. 1 balok besi = 12 kelereng. Berapa total kelereng keduanya?", ["20 kelereng", "18 kelereng", "22 kelereng", "16 kelereng"], "A", "8 + 12 = 20 kelereng.", verifikasi={"ekspresi": "8 + 12", "hasil": "20"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab23_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab23.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
