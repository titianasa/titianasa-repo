#!/usr/bin/env python3
"""
Generator dan validator Bab 74 Matematika Kelas 2 SD:
"Mengelompokkan Benda Berbentuk Bangun Ruang" (Fase A)
bab_id: b19d9c3c-a652-4e49-910a-0b8e952c861a
article_id: bb9eada6-531b-4d61-afcb-570932a12ab3
quiz_id: 9c27d3fd-f3e7-4d45-b141-04f9d72872b4
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "s1u2w3y4a501"  # Mengenal Bangun Ruang Sederhana
S2 = "t2v3x4z5b602"  # Kubus dan Balok
S3 = "u3w4y5a6c703"  # Tabung, Kerucut, dan Bola
S4 = "v4x5z6b7d804"  # Mengelompokkan Benda di Sekitar Kita

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Bangun ruang berbeda dengan bangun datar.
Bangun datar itu rata dan tipis.
Bangun ruang memiliki isi atau volume.
Bangun ruang bisa kita pegang nyata.
Ada banyak bentuk bangun ruang.
Contohnya kubus, balok, dan bola.
Ada juga tabung dan kerucut.
Mari mengenal bentuk mereka satu persatu!

:::definition
title: Bangun Ruang
Bangun tiga dimensi yang memiliki ruang dan dibatasi dinding sisi.
:::"""

s2_content = """Kubus dan balok memiliki ruang kotak.
Kubus dibatasi enam sisi persegi sama.
Semua sisi kubus sama besar.
Dadu mainan adalah contoh kubus.
Balok memiliki sisi persegi panjang.
Sisi balok tidak semuanya sama.
Kardus sepatu dan lemari adalah balok.
Keduanya sama-sama memiliki delapan pojok!

:::steps
title: Ciri Kubus dan Balok
1. Memiliki 6 buah dinding sisi.
2. Memiliki 12 buah rusuk tepi.
3. Memiliki 8 buah titik sudut pojok.
:::"""

s3_content = """Mari melihat bentuk melengkung.
Tabung memiliki alas dan tutup bulat.
Bentuk alas dan tutupnya lingkaran.
Kaleng biskuit dan susu berbentuk tabung.
Kerucut memiliki satu puncak lancip.
Topi ulang tahun berbentuk kerucut.
Bola memiliki permukaan melengkung halus.
Bola tidak memiliki sudut sama sekali!

:::common_trap
title: Mengira Bola Memiliki Sudut
Bola berbentuk bulat sempurna melengkung.
Bola tidak memiliki sudut dan rusuk.
Bola dapat menggelinding ke mana saja!
:::"""

s4_content = """Amati benda di dalam rumahmu.
Kelompokkan benda-benda itu dengan benar.
Kotak kapur masuk kelompok kubus.
Kotak pensil masuk kelompok balok.
Drum minyak masuk kelompok tabung.
Bola kasti masuk kelompok bola.
Caping petani masuk kelompok kerucut.
Mudah sekali mengelompokkan bangun ruang!

:::callout
variant: summary
title: Ringkasan
text: Kubus dan balok berkotak. Tabung, kerucut, dan bola melengkung.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Bangun Ruang Sederhana",
        "minutes": 6,
        "goal": "Siswa mengenal konsep bangun ruang tiga dimensi yang memiliki isi/volume.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Kubus dan Balok",
        "minutes": 6,
        "goal": "Siswa memahami sifat dan ciri fisik kubus dan balok.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Tabung, Kerucut, dan Bola",
        "minutes": 6,
        "goal": "Siswa mengenal bangun ruang bersisi lengkung (tabung, kerucut, bola).",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Mengelompokkan Benda di Sekitar Kita",
        "minutes": 6,
        "goal": "Siswa mampu mengelompokkan benda konkret berdasarkan bentuk bangun ruangnya.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengelompokkan Benda Berbentuk Bangun Ruang",
    "topic": "Bangun Datar dan Bangun Ruang Sederhana",
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
# 2. DEFINISI BANK 50 SOAL BAB 74
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
mc("c1", "mudah", D, F, S1, "Benda tiga dimensi yang memiliki isi dan ruang dinamakan ....", ["bangun ruang", "bangun datar", "garis lurus", "titik sudut"], "A", "Bangun berdimensi tiga dinamakan bangun ruang.")
tf("c1", "mudah", D, F, S3, "Bangun ruang bola tidak memiliki titik sudut sama sekali.", "Benar", "Bola permukaannya melengkung tanpa sudut.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Berapakah jumlah sisi yang membatasi sebuah bangun kubus?", ["6 sisi", "4 sisi", "8 sisi", "12 sisi"], "A", "Kubus memiliki 6 sisi persegi.", verifikasi={"ekspresi": "2 * 3", "hasil": "6"})
mc("c1", "mudah", T, F, S3, "Bentuk alas pada bangun ruang tabung adalah bangun datar ....", ["lingkaran", "persegi", "segitiga", "segiempat"], "A", "Alas tabung berbentuk lingkaran.")
sa("c1", "mudah", T, F, S2, "Bangun kubus memiliki ... buah titik sudut pada pojoknya.", "8", "Kubus memiliki 8 titik sudut.", verifikasi={"ekspresi": "4 * 2", "hasil": "8"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Benda di bawah ini yang berbentuk bangun ruang balok adalah ....", ["kardus mie instan", "bola kasti", "kaleng susu", "caping tani"], "A", "Kardus mie instan berbentuk balok.")
tf("c2", "mudah", D, Kn, S2, "Semua sisi pembatas pada bangun ruang balok wajib berbentuk persegi.", "Salah", "Sisi balok sebagian besar berbentuk persegi panjang.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Dadu permainan memiliki 6 sisi sama besar. Dadu berbentuk ....", ["kubus", "balok", "tabung", "bola"], "A", "Dadu berbentuk kubus karena 6 sisinya persegi sama.", "Mengira dadu berbentuk balok")
mc("c2", "mudah", R, Kn, S3, "Benda berbentuk kerucut memiliki satu ujung lancip yang disebut ....", ["titik puncak", "titik pusat", "sisi datar", "lingkaran"], "A", "Ujung lancip kerucut disebut titik puncak.", "Menyebut titik sudut biasa pada kerucut")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S3, "Benda berikut yang memiliki bentuk dasar bangun tabung adalah ....", ["kaleng biskuit", "lemari baju", "kelereng", "kotak pensil tipis"], "A", "Kaleng biskuit berbentuk tabung.")
mc("c2", "mudah", T, Kn, S4, "Topi pesta ulang tahun anak-anak umumnya berbentuk bangun ruang ....", ["kerucut", "tabung", "bola", "balok"], "A", "Topi ulang tahun berbentuk kerucut.")
tf("c2", "mudah", T, Kn, S1, "Uang kertas dan daun kering adalah contoh dari bangun ruang.", "Salah", "Uang kertas dan daun tipis adalah bangun datar.")
sa("c2", "mudah", T, Kn, S2, "Banyak rusuk kerangka yang dimiliki sebuah bangun kubus adalah ... rusuk.", "12", "Kubus memiliki 12 rusuk.", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Berapakah jumlah gabungan sisi dari 2 buah bangun kubus?", ["12 sisi", "8 sisi", "16 sisi", "10 sisi"], "A", "2 x 6 = 12 sisi.", "Mengalikan sisi kubus dengan 4", verifikasi={"ekspresi": "2 * 6", "hasil": "12"})
mc("c3", "sedang", R, Pr, S3, "Tabung memiliki sisi alas, sisi tutup, dan selimut. Berapa total sisinya?", ["3 sisi", "2 sisi", "4 sisi", "1 sisi"], "A", "Alas + tutup + selimut = 3 sisi.", "Hanya menghitung 2 sisi bulat tanpa selimut", verifikasi={"ekspresi": "2 + 1", "hasil": "3"})

# Terarah (6): S1, S2, S3, S4, S2, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Berapa banyak titik sudut yang ada pada 2 buah kardus balok?", ["16 sudut", "12 sudut", "8 sudut", "24 sudut"], "A", "2 x 8 = 16 titik sudut.", verifikasi={"ekspresi": "2 * 8", "hasil": "16"})
mc("c3", "mudah", T, Pr, S4, "Budi punya 4 bola kasti dan 3 kelereng. Berapa total benda bulat?", ["7 benda", "6 benda", "8 benda", "5 benda"], "A", "4 + 3 = 7 benda berbentuk bola.", verifikasi={"ekspresi": "4 + 3", "hasil": "7"})
tf("c3", "sedang", T, Pr, S2, "Sebuah balok memiliki jumlah rusuk yang sama dengan kubus yaitu 12.", "Benar", "Balok dan kubus sama-sama memiliki 12 rusuk.")
mc("c3", "sedang", T, Pr, S3, "Berapa buah sisi datar berbentuk lingkaran yang dimiliki bangun tabung?", ["2 sisi", "1 sisi", "3 sisi", "0 sisi"], "A", "Tabung memiliki 2 sisi datar lingkaran (alas dan tutup).", verifikasi={"ekspresi": "1 + 1", "hasil": "2"})
tf("c3", "sedang", T, Pr, S4, "Semua kaleng minuman bersoda termasuk dalam kelompok bangun balok.", "Salah", "Kaleng minuman bersoda berbentuk tabung.")
sa("c3", "sedang", T, Pr, S2, "Tiga buah kubus diletakkan terpisah. Total semua sisinya adalah ... sisi.", "18", "3 x 6 = 18 sisi.", verifikasi={"ekspresi": "3 * 6", "hasil": "18"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S2, "Berapakah jumlah rusuk dari gabungan 2 buah balok terpisah?", ["24 rusuk", "20 rusuk", "18 rusuk", "16 rusuk"], "A", "2 x 12 = 24 rusuk.", verifikasi={"ekspresi": "2 * 12", "hasil": "24"})
mc("c3", "sedang", X, Pr, S3, "Ada 5 kaleng susu di meja. Berapa jumlah seluruh sisi lingkarannya?", ["10 sisi", "8 sisi", "15 sisi", "5 sisi"], "A", "5 x 2 = 10 sisi lingkaran.", verifikasi={"ekspresi": "5 * 2", "hasil": "10"})
tf("c3", "sedang", X, Pr, S3, "Sebuah kerucut memiliki satu sisi datar lingkaran sebagai alasnya.", "Benar", "Kerucut beralas 1 lingkaran datar.")
sa("c3", "sedang", X, Pr, S4, "Di kelas ada 3 kardus balok dan 2 dadu kubus. Total benda kotak?", "5", "3 + 2 = 5 benda kotak.", verifikasi={"ekspresi": "3 + 2", "hasil": "5"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Berapakah selisih jumlah rusuk dan titik sudut pada sebuah kubus?", ["4 rusuk", "2 rusuk", "6 rusuk", "8 rusuk"], "A", "12 - 8 = 4.", verifikasi={"ekspresi": "12 - 8", "hasil": "4"})
mc("c3", "sedang", K, Pr, S4, "Kumpulan benda: bola basket, kaleng susu, kotak sepatu, kelereng. Berapa bola?", ["2 benda", "1 benda", "3 benda", "4 benda"], "A", "Bola basket dan kelereng = 2 benda bola.", verifikasi={"ekspresi": "1 + 1", "hasil": "2"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa sebuah kotak kardus dapat diisi buku tetapi kertas gambar tidak?", ["karena kardus memiliki ruang tiga dimensi di dalamnya", "karena kertas gambar licin", "karena kardus berwarna cokelat", "karena kertas terlalu berat"], "A", "Kardus memiliki volume/ruang penampung di dalamnya.")
mc("c4", "sedang", T, Kn, S2, "Apa perbedaan utama antara bentuk kubus dan bentuk balok?", ["semua sisi kubus persegi sama, sedangkan balok sisi berhadapan sama", "kubus tidak punya sudut", "balok lebih bulat", "kubus sisinya ada 8"], "A", "Kubus dibatasi 6 persegi sama, balok dibatasi persegi panjang.")
tf("c4", "sedang", T, Kn, S3, "Benda berbentuk kubus dapat menggelinding dengan sangat lancar seperti bola.", "Salah", "Kubus memiliki sisi datar dan sudut lancip sehingga tidak dapat menggelinding lancar.")
tf("c4", "sedang", T, Kn, S4, "Sebuah kotak pensil yang memiliki ruang isi adalah contoh bangun datar.", "Salah", "Kotak pensil beruang adalah contoh bangun ruang (balok).")
sa("c4", "sedang", T, Kn, S2, "Selisih banyak rusuk kubus dengan banyak sisinya adalah ... rusuk.", "6", "12 - 6 = 6 rusuk.", verifikasi={"ekspresi": "12 - 6", "hasil": "6"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Bila dua kubus satuan direkatkan satu sisinya, bentuk bangun barunya?", ["balok", "kubus besar", "tabung", "kerucut"], "A", "Panjangnya menjadi 2 kali lipat membentuk balok.")
mc("c4", "sedang", X, Kn, S3, "Sebuah kerucut dipotong ujung lancipnya mendatar. Bentuk permukaan potongan?", ["lingkaran kecil", "persegi", "segitiga", "garis lurus"], "A", "Irisan mendatar pada kerucut menghasilkan lingkaran.")
tf("c4", "sedang", X, Kn, S2, "Menumpuk 3 kubus ke atas akan membentuk sebuah bangun ruang balok.", "Benar", "Susunan kubus ke atas memanjang menjadi balok tinggi.")
mc("c4", "sulit", X, Me, S4, "Tersedia 4 kubus dan 3 balok. Berapa total titik sudut seluruhnya?", ["56 sudut", "48 sudut", "64 sudut", "42 sudut"], "A", "(4 x 8) + (3 x 8) = 7 x 8 = 56 titik sudut.", verifikasi={"ekspresi": "(4 * 8) + (3 * 8)", "hasil": "56"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Rangka kubus dibuat dari kawat. Tiap rusuk 5 cm. Berapa cm total kawat?", ["60 cm", "48 cm", "50 cm", "72 cm"], "A", "12 x 5 = 60 cm.", verifikasi={"ekspresi": "12 * 5", "hasil": "60"})
mc("c4", "sulit", K, Me, S3, "Berapa banyak lingkaran datar yang ada pada 3 tabung dan 2 kerucut?", ["8 lingkaran", "6 lingkaran", "10 lingkaran", "7 lingkaran"], "A", "(3 x 2) + (2 x 1) = 6 + 2 = 8 lingkaran.", verifikasi={"ekspresi": "(3 * 2) + (2 * 1)", "hasil": "8"})
tf("c4", "sulit", K, Me, S4, "Sebuah drum minyak dapat menggelinding dan juga dapat berdiri tegak stabil.", "Benar", "Sisi selimutnya bisa menggelinding, alas datarnya bisa berdiri tegak.")
mc("c4", "sulit", K, Me, S4, "Berapa kubus satuan kecil yang dibutuhkan untuk membuat kubus besar 2x2x2?", ["8 kubus satuan", "6 kubus satuan", "4 kubus satuan", "12 kubus satuan"], "A", "2 x 2 x 2 = 8 kubus satuan.", verifikasi={"ekspresi": "2 * 2 * 2", "hasil": "8"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Bila ingin membuat wadah air minum yang praktis digenggam dan tidak tumpah?", ["tabung dengan tutup rapat", "kerucut terbalik terbuka", "balok bolong", "bola bulat utuh"], "A", "Tabung memiliki alas stabil dan tutup yang bisa dirapatkan.")
mc("c5", "sedang", T, Me, S2, "Bandingkan jumlah sisi: 3 kubus vs 2 balok. Berapa selisih jumlah sisinya?", ["6 sisi", "4 sisi", "8 sisi", "2 sisi"], "A", "(3 x 6) - (2 x 6) = 18 - 12 = 6 sisi.", verifikasi={"ekspresi": "(3 * 6) - (2 * 6)", "hasil": "6"})
mc("c5", "sedang", T, Me, S3, "Empat kaleng drum ditumpuk vertikal. Berapa sisi lingkaran yang tampak luar?", ["2 sisi lingkaran", "4 sisi lingkaran", "8 sisi lingkaran", "1 sisi lingkaran"], "A", "Hanya lingkaran paling atas dan paling bawah yang terlihat bebas.", verifikasi={"ekspresi": "1 + 1", "hasil": "2"})
mc("c5", "sulit", T, Me, S4, "Tono memiliki kawat 72 cm. Dibuat kerangka balok dengan rusuk sama. Panjang rusuk?", ["6 cm", "5 cm", "7 cm", "8 cm"], "A", "72 : 12 = 6 cm.", verifikasi={"ekspresi": "72 / 12", "hasil": "6"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Sebuah kardus balok memiliki panjang rusuk: 4 panjang, 4 lebar, 4 tinggi. Total rusuk?", ["12 rusuk", "10 rusuk", "14 rusuk", "16 rusuk"], "A", "4 + 4 + 4 = 12 rusuk.", verifikasi={"ekspresi": "4 + 4 + 4", "hasil": "12"})
mc("c5", "sulit", K, Me, S3, "Dua kerucut identik ditempelkan kedua alas lingkarannya. Berapa titik puncak luar?", ["2 puncak", "1 puncak", "3 puncak", "0 puncak"], "A", "Ada 2 puncak di kedua ujungnya.", verifikasi={"ekspresi": "1 + 1", "hasil": "2"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Mengapa kemasan susu cair sering memakai bentuk balok daripada bentuk bola?", ["karena bentuk balok mudah ditumpuk rapat di dalam truk dan rak toko", "karena bola terlalu murah", "agar susunya dingin", "hanya kebetulan"], "A", "Balok efisien dalam ruang penyimpanan tanpa menyisakan rongga kosong.")
mc("c6", "sulit", K, Me, S4, "Rancanglah sebuah menara mainan yang paling kokoh dari kubus, balok, dan bola!", ["taruh balok dan kubus di bawah sebagai pondasi, bola di paling atas", "taruh bola di paling bawah", "semua bola di bawah", "miringkan baloknya"], "A", "Alas datar balok/kubus stabil di bawah, bola di atas agar tidak goyang.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S2, "Hitung total titik sudut: 5 kubus + 3 balok + 4 tabung!", ["64 sudut", "56 sudut", "72 sudut", "60 sudut"], "A", "(5 x 8) + (3 x 8) + (4 x 0) = 40 + 24 + 0 = 64 sudut.", verifikasi={"ekspresi": "(5 * 8) + (3 * 8)", "hasil": "64"})
mc("c6", "sulit", P, Me, S3, "Hitung total seluruh rusuk dari 6 buah kubus dan 4 buah balok!", ["120 rusuk", "108 rusuk", "124 rusuk", "112 rusuk"], "A", "(6 x 12) + (4 x 12) = 72 + 48 = 120 rusuk.", verifikasi={"ekspresi": "(6 * 12) + (4 * 12)", "hasil": "120"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab74_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab74.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
