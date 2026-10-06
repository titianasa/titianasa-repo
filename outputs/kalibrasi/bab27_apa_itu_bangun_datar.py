#!/usr/bin/env python3
"""
Generator dan validator Bab 27 Matematika Kelas 1 SD:
"Apa Itu Bangun Datar" (Fase A)
bab_id: 8803f7e8-b114-40a8-b237-31346dbe8258
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a1b2c33d4e01"  # Mengenal Permukaan Rata dan Pipih
S2 = "b2c3d44e5f12"  # Benda Sehari-hari Berpermukaan Datar
S3 = "c3d4e55f6a23"  # Garis Batas pada Bangun Datar
S4 = "d4e5f66a7b34"  # Perbedaan Bentuk Pipih dan Bervolume

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Lihatlah selembar kertas gambarmu.
Raba permukaannya dengan jarimu.
Permukaan kertas terasa sangat rata.
Kertas tampak sangat pipih.
Bentuk yang rata disebut bangun datar.
Bangun datar tidak memiliki isi tebal.
Bangun datar hanya punya permukaan datar.
Kita bisa menggambarnya di kertas.

:::definition
title: Bangun Datar
Bangun datar adalah bentuk bidang yang rata dan pipih.
Bangun datar tidak memiliki isi tebal atau ruang.
:::"""

s2_content = """Banyak bangun datar di sekitar kita.
Permukaan meja belajar tampak rata.
Permukaan lantai keramik berbentuk datar.
Papan tulis di kelas juga datar.
Jendela kaca juga berpermukaan rata.
Uang kertas juga berbentuk datar.
Semua benda itu memiliki permukaan rata.
Kita mudah menemukannya di rumah.

:::steps
title: Menemukan Permukaan Datar
1. Amati benda di sekelilingmu.
2. Raba permukaannya dengan tangan.
3. Jika terasa rata licin, itu permukaan datar.
:::"""

s3_content = """Setiap bangun datar memiliki tepi.
Tepi itu dibatasi garis lurus.
Ada juga dibatasi garis lengkung.
Garis tepi membentuk batas bangun.
Kita bisa meraba garis tepi itu.
Garis tepi mengelilingi seluruh permukaan.
Tanpa garis tepi bentuk tidak tampak.
Garis membuat bentuk menjadi jelas."""

s4_content = """Mari bedakan pipih dan isi.
Kertas gambar bentuknya pipih rata.
Kotak sepatu memiliki isi dan ruang.
Bola tenis bulat dan memiliki ruang.

:::common_trap
title: Membedakan Pipih dan Ruang
Kertas gambar adalah bangun datar pipih.
Kotak kardus memiliki ruang dan isi.
Jangan tertukar antara lembaran dan kotak.
Bangun datar tidak memiliki isi tebal.
:::

:::callout
variant: summary
title: Ringkasan
text: Bangun datar adalah bentuk rata dan pipih. Bangun datar dibatasi garis tepi dan tidak memiliki isi ruang.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Permukaan Rata dan Pipih",
        "minutes": 6,
        "goal": "Siswa memahami pengertian dasar bangun datar sebagai bentuk yang rata dan pipih.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Benda Sehari-hari Berpermukaan Datar",
        "minutes": 6,
        "goal": "Siswa mampu mengidentifikasi benda-benda di sekitar yang memiliki permukaan bangun datar.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Garis Batas pada Bangun Datar",
        "minutes": 6,
        "goal": "Siswa mengenali bahwa bangun datar dibatasi oleh garis tepi pembatas.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Perbedaan Bentuk Pipih dan Bervolume",
        "minutes": 6,
        "goal": "Siswa dapat membedakan bangun datar yang pipih dengan benda ruang yang memiliki ketebalan isi.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Apa Itu Bangun Datar",
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
# 2. DEFINISI BANK 50 SOAL BAB 27
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
mc("c1", "mudah", D, F, S1, "Bentuk yang rata dan pipih pada sebuah bidang disebut ....", ["bangun datar", "bangun ruang", "garis miring", "benda berat"], "A", "Bangun datar adalah bidang rata dan pipih.")
tf("c1", "mudah", D, F, S4, "Bangun datar memiliki ruang berongga di dalamnya.", "Salah", "Bangun datar itu pipih dan tidak memiliki isi ruang.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Benda di kelas yang permukaannya berbentuk bangun datar adalah ....", ["papan tulis", "bola kasti", "ember air", "gelas minum"], "A", "Permukaan papan tulis rata dan datar.")
mc("c1", "mudah", T, F, S3, "Batas tepi yang mengelilingi bangun datar disebut ....", ["garis tepi", "titik tengah", "warna alas", "ruang isi"], "A", "Garis tepi membatasi keliling bangun datar.")
sa("c1", "mudah", T, F, S1, "Berapa lembar kertas datar jika ada 3 lembar ditambah 2 lembar?", "5", "3 + 2 = 5 lembar kertas datar.", verifikasi={"ekspresi": "3 + 2", "hasil": "5"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Manakah benda yang termasuk bangun ruang dan bukan bangun datar pipih?", ["kotak sepatu", "selembar kertas", "permukaan meja", "layar ponsel"], "A", "Kotak sepatu memiliki isi dan ketebalan ruang.", "Tertukar antara bentuk pipih dan bangun ruang")
tf("c2", "mudah", D, Kn, S1, "Permukaan lantai keramik yang rata termasuk contoh bidang datar.", "Benar", "Keramik memiliki permukaan datar dan rata.")

# Remedial (2)
mc("c2", "mudah", R, F, S3, "Garis yang membatasi bangun datar dapat berupa garis lurus atau garis ....", ["lengkung", "pecah", "titik", "warna"], "A", "Garis pembatas bisa lurus atau melengkung.", "Tidak mengenali jenis garis pembatas bangun datar")
mc("c2", "mudah", R, Kn, S4, "Mengapa kardus mie instan bukan bangun datar?", ["karena kardus memiliki ruang dan isi tebal", "karena kardus berwarna cokelat", "karena kardus ringan", "karena kardus dari kertas"], "A", "Kardus memiliki ruang bervolume, sehingga merupakan bangun ruang.", "Menganggap kardus sebagai bangun datar karena bahannya kertas")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Ani menggambar 4 bangun datar. Budi menggambar 3 bangun datar. Total gambar?", ["7 bangun", "6 bangun", "8 bangun", "5 bangun"], "A", "4 + 3 = 7 bangun datar.", verifikasi={"ekspresi": "4 + 3", "hasil": "7"})
mc("c2", "mudah", T, Kn, S2, "Di meja ada 6 perangko datar. Diambil 2 perangko. Berapa perangko sisa?", ["4 perangko", "3 perangko", "5 perangko", "2 perangko"], "A", "6 - 2 = 4 perangko datar.", verifikasi={"ekspresi": "6 - 2", "hasil": "4"})
tf("c2", "mudah", T, Kn, S3, "Sebuah bangun datar selalu memiliki garis pembatas di tepinya.", "Benar", "Garis pembatas membentuk bentuk tepi bangun datar.")
sa("c2", "mudah", T, Kn, S4, "Ada 8 kartu datar dan 3 kotak kubus. Berapa selisih banyaknya?", "5", "8 - 3 = 5 buah.", verifikasi={"ekspresi": "8 - 3", "hasil": "5"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Boni meraba permukaan bola dan permukaan cermin. Manakah yang datar?", ["permukaan cermin", "permukaan bola", "keduanya datar", "tidak ada"], "A", "Cermin memiliki permukaan rata dan datar, bola bulat melengkung.", "Keliru mengenali permukaan datar pada benda lengkung")
mc("c3", "sedang", R, Pr, S4, "Siti mengelompokkan benda pipih. Benda manakah yang harus ia pilih?", ["daun kering dan kertas lipat", "balok kayu dan bola", "kaleng susu dan kardus", "buah jeruk dan apel"], "A", "Daun kering dan kertas lipat berbentuk pipih mendatar.", "Memilih bangun ruang ke dalam kelompok bentuk pipih")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Satu bangun punya 4 garis tepi. Jika ada 2 bangun serupa, berapa garis tepinya?", ["8 garis", "6 garis", "10 garis", "7 garis"], "A", "4 + 4 = 8 garis.", verifikasi={"ekspresi": "4 + 4", "hasil": "8"})
mc("c3", "sedang", T, Pr, S2, "Ada 9 ubin lantai datar. 3 ubin dicat biru. Berapa ubin belum dicat?", ["6 ubin", "5 ubin", "7 ubin", "4 ubin"], "A", "9 - 3 = 6 ubin.", verifikasi={"ekspresi": "9 - 3", "hasil": "6"})
tf("c3", "sedang", T, Pr, S3, "Bangun yang dibatasi 3 garis lurus memiliki 3 sudut pojok.", "Benar", "Bangun dengan 3 sisi lurus (segitiga) punya 3 sudut.")
mc("c3", "sedang", T, Pr, S4, "Kertas origami tebalnya sangat tipis. Maka origami termasuk ....", ["bangun datar", "bangun ruang", "balok tebal", "bola ruang"], "A", "Bentuk tipis dan rata digolongkan sebagai bangun datar.")
tf("c3", "sedang", T, Pr, S1, "Kita bisa mengisi air ke dalam selembar bangun datar yang digambar di buku.", "Salah", "Gambar bangun datar tidak punya ruang untuk menampung air.")
sa("c3", "mudah", T, Pr, S3, "Sebuah bangun datar memiliki 4 sisi tepi. Berapa sisi tepi bangun tersebut?", "4", "Bangun memiliki 4 sisi tepi.", verifikasi={"ekspresi": "4", "hasil": "4"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Rina memotong 5 kertas segitiga dan 7 kertas segiempat. Berapa total kertas?", ["12 kertas", "11 kertas", "13 kertas", "10 kertas"], "A", "5 + 7 = 12 lembar kertas datar.", verifikasi={"ekspresi": "5 + 7", "hasil": "12"})
mc("c3", "sedang", X, Pr, S2, "Dinding kelas dipasangi 15 poster datar. 6 poster dilepas. Berapa poster tersisa?", ["9 poster", "8 poster", "10 poster", "7 poster"], "A", "15 - 6 = 9 poster.", verifikasi={"ekspresi": "15 - 6", "hasil": "9"})
tf("c3", "sedang", X, Pr, S3, "Garis pembatas lingkaran berupa garis lurus tanpa lengkungan.", "Salah", "Batas lingkaran berupa satu garis lengkung tertutup.")
sa("c3", "sedang", X, Pr, S4, "Di meja ada 14 kartu pipih dan 8 kubus mainan. Berapa selisihnya?", "6", "14 - 8 = 6 buah.", verifikasi={"ekspresi": "14 - 8", "hasil": "6"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Ada 8 stiker datar di buku. Ditambah 6 stiker lagi. Berapa jumlah stiker?", ["14 stiker", "13 stiker", "15 stiker", "12 stiker"], "A", "8 + 6 = 14 stiker.", verifikasi={"ekspresi": "8 + 6", "hasil": "14"})
mc("c3", "sedang", K, Pr, S3, "Bangun A punya 3 garis tepi. Bangun B punya 4 garis tepi. Jumlah garis tepi keduanya?", ["7 garis", "6 garis", "8 garis", "5 garis"], "A", "3 + 4 = 7 garis tepi.", verifikasi={"ekspresi": "3 + 4", "hasil": "7"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Apa perbedaan paling utama antara selembar kertas dan sebuah balok kayu?", ["kertas itu datar pipih sedangkan balok memiliki ketebalan ruang", "kertas lebih berat dari balok", "balok tidak punya warna", "kertas tidak bisa dipegang"], "A", "Kertas pipih rata (datar) sementara balok memiliki volume ruang.")
mc("c4", "sedang", T, Kn, S2, "Di antara benda berikut, manakah kelompok benda yang berpermukaan rata?", ["papan catur, layar TV, dan lantai keramik", "bola sepak, jeruk, dan kelereng", "ember, gayung, dan helm", "batu kali, ban mobil, dan donat"], "A", "Papan catur, layar TV, dan lantai berpermukaan rata.")
tf("c4", "sedang", T, Kn, S3, "Bangun datar tertutup selalu mempunyai tepi keliling yang tersambung utuh.", "Benar", "Garis tepi bangun tertutup menyambung tanpa celah terputus.")
tf("c4", "sedang", T, Kn, S4, "Sebuah gambar lingkaran di atas kertas memiliki isi dan ruang yang bisa ditiup.", "Salah", "Gambar lingkaran hanya bidang datar tanpa volume isi.")
sa("c4", "sedang", T, Kn, S4, "Bangun A dibatasi 4 garis tepi. Bangun B dibatasi 3 garis tepi. Selisih garis tepi?", "1", "4 - 3 = 1 garis tepi.", verifikasi={"ekspresi": "4 - 3", "hasil": "1"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Jika permukaan meja diraba terasa licin dan rata, maka permukaan meja termasuk ....", ["bidang datar", "garis miring", "benda bulat", "bangun lengkung"], "A", "Permukaan yang rata dan mendatar adalah bidang datar.")
mc("c4", "sedang", X, Kn, S2, "Ada 16 buku tulis berpermukaan datar. 9 buku dimasukkan tas. Berapa buku di meja?", ["7 buku", "6 buku", "8 buku", "5 buku"], "A", "16 - 9 = 7 buku.", verifikasi={"ekspresi": "16 - 9", "hasil": "7"})
tf("c4", "sedang", X, Kn, S4, "Gelas minum kaca tergolong sebagai bangun datar pipih.", "Salah", "Gelas adalah benda ruang bervolume karena dapat diisi cairan.")
mc("c4", "sulit", X, Me, S3, "Dua bangun segiempat masing-masing punya 4 tepi. Berapa total tepi keduanya?", ["8 tepi", "6 tepi", "10 tepi", "7 tepi"], "A", "4 + 4 = 8 garis tepi.", verifikasi={"ekspresi": "4 + 4", "hasil": "8"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Mengapa lukisan pemandangan di dinding disebut bangun datar?", ["karena gambarnya menempel rata dan pipih pada kain kanvas", "karena pemandangannya luas", "karena catnya warna-warni", "karena dibeli di pasar"], "A", "Lukisan menempel pada bidang datar kanvas yang rata dan pipih.")
mc("c4", "sulit", K, Me, S2, "Toko punya 18 ubin keramik. Terjual 11 ubin. Berapa ubin tersisa?", ["7 ubin", "6 ubin", "8 ubin", "5 ubin"], "A", "18 - 11 = 7 ubin.", verifikasi={"ekspresi": "18 - 11", "hasil": "7"})
tf("c4", "sulit", K, Me, S3, "Sebuah segitiga dipotong menjadi dua bagian datar, hasilnya tetap datar.", "Benar", "Potongan bentuk pipih tetap berupa bidang datar.")
mc("c4", "sulit", K, Me, S4, "Ada 20 lembar karton datar. Dipakai 13 lembar. Berapa lembar karton tersisa?", ["7 lembar", "6 lembar", "8 lembar", "5 lembar"], "A", "20 - 13 = 7 lembar.", verifikasi={"ekspresi": "20 - 13", "hasil": "7"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Edo membuat 3 bangun datar, tiap bangun butuh 4 lidi. Berapa total lidi yang dipakai?", ["12 lidi", "10 lidi", "14 lidi", "9 lidi"], "A", "3 x 4 = 12 lidi.", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})
mc("c5", "sedang", T, Me, S2, "Dua bangun bertepi 4 digabung. Berapa hasil dari 4 ditambah 4 dikurang 2?", ["6", "5", "7", "4"], "A", "4 + 4 - 2 = 6.", verifikasi={"ekspresi": "4 + 4 - 2", "hasil": "6"})
mc("c5", "sedang", T, Me, S3, "Tiga bangun segitiga masing-masing punya 3 sisi. Berapa total sisi ketiganya?", ["9 sisi", "8 sisi", "10 sisi", "6 sisi"], "A", "3 x 3 = 9 sisi.", verifikasi={"ekspresi": "3 * 3", "hasil": "9"})
mc("c5", "sulit", T, Me, S4, "Manakah pernyataan yang paling tepat menjelaskan perbedaan bangun datar dan bangun ruang?", ["bangun datar berbentuk pipih rata, bangun ruang memiliki isi dan kedalaman", "bangun datar selalu lebih besar dari bangun ruang", "bangun datar selalu berwarna putih", "bangun ruang tidak punya tepi"], "A", "Bangun datar itu 2 dimensi pipih, bangun ruang 3 dimensi bervolume.")

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Siti menggambar 4 segitiga (tiap bangun 3 sisi). Berapa total garis sisinya?", ["12 garis", "10 garis", "14 garis", "9 garis"], "A", "4 x 3 = 12 garis.", verifikasi={"ekspresi": "4 * 3", "hasil": "12"})
mc("c5", "sulit", K, Me, S3, "Ada 17 batang korek api. Dibuat bangun segiempat (4 batang). Berapa sisa korek api?", ["13 batang", "12 batang", "14 batang", "11 batang"], "A", "17 - 4 = 13 batang.", verifikasi={"ekspresi": "17 - 4", "hasil": "13"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Rancanglah sebuah karya gambar yang tersusun dari gabungan bangun-bangun datar di kertas!", ["menggambar rumah menggunakan atap segitiga, dinding segiempat, dan jendela persegi", "menumpuk batu bata asli di atas meja belajar", "meniup gelembung sabun ke udara", "mengisi ember dengan air sumur"], "A", "Menggabungkan aneka bentuk datar di atas kertas menjadi bentuk rumah.")
mc("c6", "sulit", K, Me, S4, "Susunlah aturan cara membedakan benda pipih datar dan benda ruang di sekelilingmu!", ["raba bendanya: jika rata tanpa isi itu datar, jika berongga atau tebal itu bangun ruang", "lihat warnanya saja tanpa menyentuh", "timbang beratnya dengan perkiraan mata", "tanyakan pada teman sebelah tanpa memeriksa"], "A", "Memeriksa permukaan dan ketebalan rongga isi benda secara langsung.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S2, "Dua bangun segitiga (masing-masing 3 sisi) dan 1 segiempat (4 sisi). Berapa total sisi?", ["10 sisi", "9 sisi", "11 sisi", "8 sisi"], "A", "3 + 3 + 4 = 10 sisi.", verifikasi={"ekspresi": "3 + 3 + 4", "hasil": "10"})
mc("c6", "sulit", P, Me, S3, "Dibuat 3 segiempat (tiap bangun 4 lidi). Tersedia 15 lidi. Berapa lidi tersisa?", ["3 lidi", "2 lidi", "4 lidi", "1 lidi"], "A", "15 - (3 * 4) = 3 lidi.", verifikasi={"ekspresi": "15 - (3 * 4)", "hasil": "3"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab27_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab27.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
