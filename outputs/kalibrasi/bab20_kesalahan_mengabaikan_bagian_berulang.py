#!/usr/bin/env python3
"""
Generator dan validator Bab 20 Matematika Kelas 1 SD:
"Kesalahan Umum: Mengabaikan Bagian yang Berulang" (Fase A)
bab_id: eff4a1b7-ef50-40e1-84e3-327487c6778a
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a0b9c89d1e01"  # Hanya Melihat Gambar Terakhir (Lupa Pola)
S2 = "b1c0d90e2f12"  # Mengulang Benda Sama Berturut-turut
S3 = "c2d1e01f3a23"  # Memasukkan Benda Baru Tanpa Aturan
S4 = "d3e2f12a4b34"  # Menemukan dan Memperbaiki Gambar yang Rusak

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Banyak anak membuat kesalahan ini.
Mereka hanya melihat gambar terakhir.
Lalu langsung menebak kelanjutannya.
Padahal pola punya kelompok pengulang.
Kita harus melihat dari awal.
Temukan kelompok yang berulang rapi.
Jangan hanya melihat ujungnya saja.

:::definition
title: Inti Pola Berulang
Inti pola adalah kelompok dasar pengulang.
Pola selalu mengulang kelompok itu.
:::"""

s2_content = """Kesalahan kedua adalah mengulang benda.
Misal pola: sendok, garpu, sendok.
Lalu ada anak menjawab sendok.
Itu keliru karena sendok berulang.
Setelah sendok seharusnya garpu.
Benda harus bergantian teratur.
Jangan mengulang benda yang sama.

:::steps
title: Menghindari Pengulangan Keliru
1. Sebutkan benda secara bergantian.
2. Periksa apakah benda berdekatan sama.
3. Pastikan urutan selalu berselang-seling.
:::"""

s3_content = """Kesalahan ketiga adalah menambah benda.
Benda asing tiba-tiba dimasukkan.
Misal pola apel dan jeruk.
Lalu anak menebak buah pisang.
Pisang bukan bagian dari pola.
Gunakan hanya anggota inti pola.
Jangan membuat aturan baru sendiri.
Tetap gunakan benda yang ada."""

s4_content = """Ayo belajar menjadi detektif pola.
Cari satu gambar yang salah.
Bintang, bulan, bintang, bintang.
Bulan kedua hilang diganti bintang.
Perbaiki dengan gambar yang benar.

:::common_trap
title: Meniru Gambar Terakhir
Jangan hanya melihat gambar paling ujung.
Ingatlah kembali kelompok inti polanya.
Pola bergantian selalu mengulang dari awal.
Setelah B pasti kembali ke A.
:::

:::callout
variant: summary
title: Ringkasan
text: Kunci pola adalah keteraturan pengulangan. Temukan inti pola untuk menentukan benda berikutnya.
:::"""

sections = [
    {
        "id": S1,
        "title": "Hanya Melihat Gambar Terakhir (Lupa Pola)",
        "minutes": 6,
        "goal": "Siswa dapat menyadari kekeliruan menebak hanya dari gambar terakhir tanpa melihat inti pengulangan.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengulang Benda Sama Berturut-turut",
        "minutes": 6,
        "goal": "Siswa dapat menghindari kesalahan menaruh benda yang sama berturut-turut pada pola bergantian.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Memasukkan Benda Baru Tanpa Aturan",
        "minutes": 6,
        "goal": "Siswa dapat memahami bahwa pola tertutup hanya memakai anggota yang ada dalam kelompok inti.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menemukan dan Memperbaiki Gambar yang Rusak",
        "minutes": 6,
        "goal": "Siswa dapat mendeteksi ketidakteraturan pada pola yang rusak dan memperbaikinya.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Mengabaikan Bagian yang Berulang",
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
# 2. DEFINISI BANK 50 SOAL BAB 20
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
mc("c1", "mudah", D, F, S1, "Untuk melanjutkan pola, kita harus melihat ....", ["inti pola dari awal", "hanya gambar terakhir", "warna paling terang", "gambar terbesar"], "A", "Melihat inti pola dari awal sangat penting untuk menentukan kelanjutan.")
tf("c1", "mudah", D, F, S2, "Pada pola bergantian AB, benda A dan B muncul berselang-seling.", "Benar", "Benda bergantian secara teratur satu per satu.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Berapa banyak macam benda dalam inti pola dua unsur?", ["2", "3", "4", "1"], "A", "Inti pola dua unsur memiliki 2 macam benda.", verifikasi={"ekspresi": "2", "hasil": "2"})
mc("c1", "mudah", T, F, S2, "Berapa banyak benda yang berulang pada pola tiga unsur?", ["3", "2", "4", "5"], "A", "Ada 3 benda berulang pada pola tiga unsur.", verifikasi={"ekspresi": "3", "hasil": "3"})
sa("c1", "mudah", T, F, S3, "Bolehkah memasukkan benda baru yang tidak ada pada pola?", "tidak", "Pola hanya menggunakan anggota inti pengulang.")

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Pola: sendok, garpu, sendok, .... Jawaban yang keliru adalah ....", ["sendok", "garpu", "piring", "gelas"], "A", "Menjawab sendok adalah keliru karena mengulang benda yang sama berturut-turut.")
tf("c2", "mudah", D, Kn, S3, "Pada pola apel dan jeruk, kita boleh menebak pisang.", "Salah", "Pisang adalah benda asing di luar anggota pola.")

# Remedial (2)
mc("c2", "mudah", R, F, S1, "Apa akibat jika kita hanya melihat gambar terakhir?", ["jawaban bisa salah", "jawaban pasti benar", "pola menjadi rapi", "soal selesai cepat"], "A", "Hanya melihat ujung membuat kita lupa inti pola.", "Hanya melihat gambar terakhir tanpa melihat inti pola")
mc("c2", "mudah", R, Kn, S2, "Pola: merah, biru, merah, .... Warna berikutnya adalah ....", ["biru", "merah", "kuning", "hijau"], "A", "Setelah merah adalah biru.", "Mengulang warna yang sama berturut-turut")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Pola: topi, dasi, topi, .... Benda selanjutnya adalah ....", ["dasi", "topi", "sepatu", "kaos"], "A", "Setelah topi adalah dasi.")
mc("c2", "mudah", T, Kn, S2, "Pola: 1, 2, 1, 2, 1, .... Angka berikutnya adalah ....", ["2", "1", "3", "4"], "A", "Setelah angka 1 kembali ke angka 2.", verifikasi={"ekspresi": "2", "hasil": "2"})
tf("c2", "mudah", T, Kn, S4, "Pola bintang, bulan, bintang, bintang memiliki gambar yang rusak.", "Benar", "Bintang kedua di ujung merusak keteraturan pola.")
sa("c2", "mudah", T, Kn, S4, "Pola: 5, 6, 5, 6, 5, .... Angka berikutnya adalah?", "6", "Setelah 5 adalah 6.", verifikasi={"ekspresi": "6", "hasil": "6"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Pola: bulat, kotak, bulat, kotak. Bentuk manakah yang BUKAN anggota pola?", ["segitiga", "bulat", "kotak", "semua anggota"], "A", "Segitiga adalah benda baru yang asing.", "Memasukkan bentuk baru di luar pola")
mc("c3", "sedang", R, Pr, S4, "Ada pola rusak: apel, jeruk, apel, apel. Buah perbaikannya adalah ....", ["jeruk", "apel", "pisang", "mangga"], "A", "Apel terakhir diganti jeruk agar teratur.", "Salah memperbaiki gambar yang rusak pada pola")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Pola dua unsur berulang 4 kali. Berapa total bendanya?", ["8", "6", "10", "7"], "A", "2 x 4 = 8 benda.", verifikasi={"ekspresi": "2 * 4", "hasil": "8"})
mc("c3", "sedang", T, Pr, S2, "Pola: 3, 7, 3, 7, 3, 7. Berapa kali angka 3 muncul?", ["3 kali", "2 kali", "4 kali", "5 kali"], "A", "Angka 3 muncul 3 kali.", verifikasi={"ekspresi": "6 // 2", "hasil": "3"})
tf("c3", "sedang", T, Pr, S3, "Pola kucing, anjing, kucing boleh dilanjutkan kelinci.", "Salah", "Kelinci bukan bagian dari inti pengulangan.")
mc("c3", "sedang", T, Pr, S4, "Deret: 2, 4, 2, 2, 2. Berapa angka yang salah letak?", ["1 angka", "2 angka", "3 angka", "0 angka"], "A", "Angka ke-4 harusnya 4, jadi ada 1 yang salah letak.", verifikasi={"ekspresi": "1", "hasil": "1"})
tf("c3", "sedang", T, Pr, S1, "Menebak pola dari gambar awal dan akhir selalu benar.", "Salah", "Harus memeriksa seluruh keteraturan inti pengulang.")
sa("c3", "mudah", T, Pr, S2, "Pola 3 bentuk berulang 2 kali. Berapa total bentuknya?", "6", "3 x 2 = 6 bentuk.", verifikasi={"ekspresi": "3 * 2", "hasil": "6"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Pola: merah, putih, merah, putih. Pada 8 bendera, berapa bendera merah?", ["4", "3", "5", "6"], "A", "8 / 2 = 4 bendera merah.", verifikasi={"ekspresi": "8 // 2", "hasil": "4"})
mc("c3", "sedang", X, Pr, S2, "Pola: pensil, buku, pensil, buku. Urutan ke-6 adalah ....", ["buku", "pensil", "penghapus", "penggaris"], "A", "Urutan genap selalu buku.")
tf("c3", "sedang", X, Pr, S4, "Susunan 1, 2, 1, 2, 1, 2 tidak memiliki angka rusak.", "Benar", "Semua angka teratur bergantian.")
sa("c3", "sedang", X, Pr, S4, "Pola 2 benda berulang 5 kali. Berapa total bendanya?", "10", "2 x 5 = 10 benda.", verifikasi={"ekspresi": "2 * 5", "hasil": "10"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Pola: bulan, bintang berulang 3 kali. Berapa gambar bulan?", ["3", "2", "4", "6"], "A", "Ada 3 gambar bulan.", verifikasi={"ekspresi": "3", "hasil": "3"})
mc("c3", "sedang", K, Pr, S3, "Pola: sendok, garpu, piring berulang 2 kali. Berapa total benda?", ["6", "5", "7", "8"], "A", "3 x 2 = 6 benda.", verifikasi={"ekspresi": "3 * 2", "hasil": "6"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Mengapa pola segitiga, kotak, segitiga tidak boleh dilanjutkan segitiga?", ["karena bentuk harus bergantian", "karena segitiga terlalu kecil", "karena kotak terlalu besar", "karena warnanya beda"], "A", "Pola dua unsur mengharuskan bentuk bergantian.")
mc("c4", "sedang", T, Kn, S2, "Pola: 1, 3, 1, 3, 1, 3. Berapa selisih jumlah angka 1 dan angka 3?", ["0", "1", "2", "3"], "A", "Angka 1 ada 3, angka 3 ada 3. Selisihnya 3 - 3 = 0.", verifikasi={"ekspresi": "3 - 3", "hasil": "0"})
tf("c4", "sedang", T, Kn, S3, "Menambah benda baru pada pola tertutup merusak aturan pola.", "Benar", "Aturan pola tertutup hanya memakai anggota inti.")
tf("c4", "sedang", T, Kn, S4, "Deret: bulat, lonjong, bulat, bulat memiliki 1 bentuk rusak.", "Benar", "Bulat terakhir seharusnya lonjong.")
sa("c4", "sedang", T, Kn, S4, "Ada 12 benda berpola 2 unsur. Berapa pasang inti pola?", "6", "12 / 2 = 6 pasang.", verifikasi={"ekspresi": "12 // 2", "hasil": "6"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Edo melihat deret: A, B, A, B, A. Edo menebak A. Mengapa tebakan Edo salah?", ["karena setelah A harusnya B", "karena huruf B hilang", "karena huruf A terlalu banyak", "karena urutannya acak"], "A", "Pola bergantian mengharuskan setelah A adalah B.")
mc("c4", "sedang", X, Kn, S2, "Pola dua warna berulang pada 14 ubin. Berapa ubin warna kedua?", ["7", "6", "8", "5"], "A", "14 / 2 = 7 ubin.", verifikasi={"ekspresi": "14 // 2", "hasil": "7"})
tf("c4", "sedang", X, Kn, S4, "Pola rusak tidak dapat diperbaiki sama sekali.", "Salah", "Pola rusak bisa diperbaiki dengan mengganti benda yang keliru.")
mc("c4", "sulit", X, Me, S3, "Deret 16 gambar memuat pola dua unsur. Berapa banyak inti pola?", ["8", "7", "9", "6"], "A", "16 / 2 = 8 inti pengulang.", verifikasi={"ekspresi": "16 // 2", "hasil": "8"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Kesalahan terbesar saat menebak pola adalah ....", ["hanya melihat benda terakhir", "melihat dari benda awal", "menghitung jumlah benda", "mencari kelompok berulang"], "A", "Hanya melihat benda terakhir membuat kita melupakan aturan pola.")
mc("c4", "sulit", K, Me, S2, "Deret: 4, 8, 4, 8, 4, 8, 4, 8. Berapa jumlah angka 4?", ["4", "3", "5", "8"], "A", "Ada 4 angka 4.", verifikasi={"ekspresi": "8 // 2", "hasil": "4"})
tf("c4", "sulit", K, Me, S3, "Pola tiga unsur yang berulang 4 kali memiliki total 15 benda.", "Salah", "Totalnya 3 x 4 = 12 benda, bukan 15.")
mc("c4", "sulit", K, Me, S4, "Pada deret 10 gambar bergantian, ada 1 gambar rusak. Berapa gambar benar?", ["9", "8", "10", "7"], "A", "10 - 1 = 9 gambar benar.", verifikasi={"ekspresi": "10 - 1", "hasil": "9"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Susunan: merah, biru, biru, merah. Apa yang harus diubah agar rapi bergantian?", ["ganti biru pertama jadi merah", "ganti biru kedua jadi merah", "hapus merah pertama", "biarkan saja"], "A", "Pola selang-seling membutuhkan perubahan pada warna yang bertumpuk.")
mc("c5", "sedang", T, Me, S2, "Siti menyusun 10 manik bergantian. Manik ke-4 terlepas. Manik apa penggantinya?", ["manik kedua", "manik pertama", "manik baru", "manik acak"], "A", "Urutan genap (2, 4, ...) selalu memakai manik kedua.")
mc("c5", "sedang", T, Me, S3, "Pola bentuk: kotak, bulat. Doni memasukkan segitiga di tengah. Apa kesalahan Doni?", ["menambah bentuk baru", "mengulang bentuk sama", "salah menghitung", "kurang bentuk"], "A", "Segitiga adalah bentuk asing di luar pola.")
mc("c5", "sulit", T, Me, S4, "Ada deret 12 balok. 2 balok keliru warna. Berapa balok yang sudah tepat?", ["10 balok", "9 balok", "11 balok", "8 balok"], "A", "12 - 2 = 10 balok tepat.", verifikasi={"ekspresi": "12 - 2", "hasil": "10"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Pola dua bentuk berulang 6 kali. Berapa banyak bentuk pertama?", ["6", "5", "7", "4"], "A", "Ada 6 bentuk pertama.", verifikasi={"ekspresi": "6", "hasil": "6"})
mc("c5", "sulit", K, Me, S4, "Deret: 5, 9, 5, 9, 5, 5. Berapa angka 5 keliru yang harus diganti?", ["1 angka", "2 angka", "3 angka", "0 angka"], "A", "Angka ke-6 harusnya 9, jadi ada 1 angka.", verifikasi={"ekspresi": "1", "hasil": "1"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Rancanglah aturan pola agar tidak terjadi dua benda sama berdekatan!", ["benda bergantian selang-seling", "benda pertama diulang tiga kali", "benda diletakkan acak", "semua benda sama"], "A", "Aturan selang-seling mencegah benda sama berdekatan.")
mc("c6", "sulit", K, Me, S4, "Susunlah perbaikan untuk deret: 1, 2, 1, 1, 1, 2!", ["ganti angka ke-4 menjadi 2", "ganti angka ke-1 menjadi 2", "ganti semua jadi 1", "hapus angka 2"], "A", "Angka ke-4 harusnya 2 agar berpola 1, 2, 1, 2, 1, 2.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Rancanglah gelang 18 manik berpola 3 warna. Berapa manik warna pertama?", ["6 manik", "5 manik", "7 manik", "8 manik"], "A", "18 / 3 = 6 manik.", verifikasi={"ekspresi": "18 // 3", "hasil": "6"})
mc("c6", "sulit", P, Me, S4, "Jika deret 20 gambar punya 2 gambar rusak, berapa gambar yang benar?", ["18 gambar", "16 gambar", "19 gambar", "17 gambar"], "A", "20 - 2 = 18 gambar.", verifikasi={"ekspresi": "20 - 2", "hasil": "18"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab20_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab20.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
