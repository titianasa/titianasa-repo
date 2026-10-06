#!/usr/bin/env python3
"""
Generator dan validator Bab 22 Matematika Kelas 1 SD:
"Satuan Panjang Tak Baku dan Alat Ukurnya" (Fase A)
bab_id: ec8a861b-90c8-47a1-8903-455d6874b092
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "e2f1a00b3c12"  # Mengukur dengan Jengkal dan Hasta
S2 = "f3a2b11c4d23"  # Mengukur dengan Depa dan Langkah Kaki
S3 = "a4b3c22d5e34"  # Mengukur dengan Benda Kecil di Sekitar
S4 = "b5c4d33e6f45"  # Mengapa Hasil Ukuran Tak Baku Berbeda?

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Kita bisa mengukur tanpa penggaris.
Gunakan anggota tubuh kita.
Jengkal adalah bentangan jari tangan.
Dari ibu jari sampai kelingking.
Hasta diukur dari siku lengan.
Sampai ke ujung jari tengah.
Jengkal cocok untuk mengukur buku.
Hasta cocok untuk papan tulis.

:::definition
title: Jengkal dan Hasta
Jengkal adalah bentangan ibu jari ke kelingking.
Hasta adalah jarak dari siku ke ujung jari tengah.
:::"""

s2_content = """Untuk benda panjang gunakan depa.
Depa adalah rentangan kedua tangan.
Rentangkan tangan lurus ke samping.
Depa cocok untuk dinding kelas.
Untuk lantai kita gunakan langkah.
Langkahkan kaki secara wajar.
Hitung setiap langkah yang dibuat.
Langkah kaki mengukur panjang kelas.

:::steps
title: Mengukur dengan Depa
1. Berdiri rapat pada tepi dinding.
2. Rentangkan kedua tangan ke samping.
3. Hitung berapa kali rentangan tanganmu.
:::"""

s3_content = """Kita juga bisa memakai benda.
Benda kecil seragam dapat digunakan.
Contohnya batang korek api.
Bisa juga memakai klip kertas.
Jajarkan klip di samping pensil.
Jangan sampai ada celah kosong.
Jangan menumpuk klip kertas itu.
Hitung berapa banyak klip terpakai."""

s4_content = """Satuan tak baku punya sifat unik.
Hasil ukurannya bisa berbeda-beda.
Tangan ayah lebih besar darimu.
Buku diukur ayah dapat 2 jengkal.
Buku diukur kamu dapat 3 jengkal.

:::common_trap
title: Mengira Ukuran Jengkal Selalu Sama
Jengkal tangan setiap orang berbeda.
Tangan orang dewasa lebih panjang.
Tangan anak-anak lebih pendek.
Jumlah jengkal anak akan lebih banyak.
Semua hasil ukuran tetap benar.
:::

:::callout
variant: summary
title: Ringkasan
text: Satuan tak baku memakai jengkal, hasta, depa, langkah, atau klip kertas.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengukur dengan Jengkal dan Hasta",
        "minutes": 6,
        "goal": "Siswa mengenal dan dapat menggunakan jengkal dan hasta untuk mengukur panjang benda.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengukur dengan Depa dan Langkah Kaki",
        "minutes": 6,
        "goal": "Siswa mengenal dan dapat menggunakan depa dan langkah kaki untuk mengukur jarak atau benda panjang.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mengukur dengan Benda Kecil di Sekitar",
        "minutes": 6,
        "goal": "Siswa dapat mengukur panjang benda menggunakan benda kecil seperti klip kertas atau korek api.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Mengapa Hasil Ukuran Tak Baku Berbeda?",
        "minutes": 6,
        "goal": "Siswa memahami alasan mengapa hasil pengukuran dengan satuan tak baku dapat menghasilkan angka yang berbeda.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Satuan Panjang Tak Baku dan Alat Ukurnya",
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
# 2. DEFINISI BANK 50 SOAL BAB 22
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
mc("c1", "mudah", D, F, S1, "Jengkal diukur dari ujung ibu jari sampai ujung ....", ["kelingking", "telunjuk", "jari manis", "jari tengah"], "A", "Jengkal adalah bentangan dari ibu jari hingga kelingking.")
tf("c1", "mudah", D, F, S2, "Depa adalah ukuran bentangan kedua tangan ke samping.", "Benar", "Depa diukur dari ujung tangan kiri ke ujung tangan kanan.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Hasta diukur mulai dari siku tangan sampai ke ujung ....", ["jari tengah", "ibu jari", "kelingking", "pergelangan"], "A", "Hasta diukur dari siku lengan sampai ke ujung jari tengah.")
mc("c1", "mudah", T, F, S2, "Satuan tak baku yang cocok untuk mengukur lapangan adalah ....", ["langkah kaki", "jengkal", "klip kertas", "korek api"], "A", "Langkah kaki sangat cocok untuk jarak jauh seperti lapangan.")
sa("c1", "mudah", T, F, S3, "Berapa batang korek api jika panjang pensil sama dengan 4 batang?", "4", "Panjangnya sama dengan 4 batang korek api.", verifikasi={"ekspresi": "4", "hasil": "4"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Mengapa jengkal ayah dan jengkal anak berbeda?", ["karena ukuran tangan berbeda", "karena mata uang berbeda", "karena waktu berbeda", "karena warna kulit berbeda"], "A", "Ukuran tangan orang dewasa lebih besar dari tangan anak-anak.")
tf("c2", "mudah", D, Kn, S3, "Mengukur dengan klip kertas boleh ada celah renggang.", "Salah", "Klip kertas harus dijajarkan rapat tanpa celah.")

# Remedial (2)
mc("c2", "mudah", R, F, S1, "Alat ukur tubuh yang cocok untuk buku tulis adalah ....", ["jengkal", "depa", "langkah", "meteran rol"], "A", "Buku tulis berukuran kecil, cocok diukur dengan jengkal.", "Menggunakan satuan tak baku yang tidak proporsional")
mc("c2", "mudah", R, Kn, S4, "Jika tangan pengukur makin besar, jumlah jengkal yang dibutuhkan makin ....", ["sedikit", "banyak", "panjang", "berat"], "A", "Tangan besar mencakup bentangan lebih lebar sehingga butuh jengkal lebih sedikit.", "Mengira tangan besar menghasilkan angka jengkal lebih banyak")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Panjang buku adalah 2 jengkal. Meja 6 jengkal. Meja lebih panjang ....", ["4 jengkal", "3 jengkal", "5 jengkal", "2 jengkal"], "A", "6 - 2 = 4 jengkal.", verifikasi={"ekspresi": "6 - 2", "hasil": "4"})
mc("c2", "mudah", T, Kn, S2, "Dinding kelas diukur dengan depa menghasilkan 8 depa. Pintu 2 depa. Selisihnya?", ["6 depa", "5 depa", "7 depa", "4 depa"], "A", "8 - 2 = 6 depa.", verifikasi={"ekspresi": "8 - 2", "hasil": "6"})
tf("c2", "mudah", T, Kn, S4, "Hasil pengukuran jengkal dua anak bisa berbeda sedikit.", "Benar", "Ukuran jengkal tiap anak belum tentu sama persis.")
sa("c2", "mudah", T, Kn, S3, "Sebuah pulpen sepanjang 5 klip kertas. Berapa klip untuk 2 pulpen?", "10", "5 + 5 = 10 klip kertas.", verifikasi={"ekspresi": "5 + 5", "hasil": "10"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Saat mengukur pensil dengan klip, klip harus ditaruh secara ....", ["rapat lurus tanpa celah", "bertumpuk-tumpuk", "miring melingkar", "berjauhan"], "A", "Klip harus diletakkan rapat lurus tanpa celah dan tanpa tumpukan.", "Menumpuk atau merenggangkan alat ukur tak baku")
mc("c3", "sedang", R, Pr, S4, "Meja diukur Doni dapat 8 jengkal, diukur Ayah dapat 5 jengkal. Selisihnya?", ["3 jengkal", "2 jengkal", "4 jengkal", "5 jengkal"], "A", "8 - 5 = 3 jengkal.", "Salah menghitung selisih hasil pengukuran tak baku", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Panjang papan tulis 8 hasta. Panjang meja 3 hasta. Berapa jumlah panjangnya?", ["11 hasta", "10 hasta", "12 hasta", "9 hasta"], "A", "8 + 3 = 11 hasta.", verifikasi={"ekspresi": "8 + 3", "hasil": "11"})
mc("c3", "sedang", T, Pr, S2, "Budi melangkah 14 kali dari pintu ke jendela. Sisa 6 langkah. Jarak total?", ["20 langkah", "18 langkah", "19 langkah", "17 langkah"], "A", "14 + 6 = 20 langkah.", verifikasi={"ekspresi": "14 + 6", "hasil": "20"})
tf("c3", "sedang", T, Pr, S3, "Mengukur panjang dengan korek api yang ukurannya berbeda-beda adalah cara yang benar.", "Salah", "Benda pengukur harus berukuran sama seragam.")
mc("c3", "sedang", T, Pr, S4, "Buku diukur Siti dapat 4 jengkal. Diukur Edo dapat 4 jengkal. Artinya tangan mereka ....", ["sama panjang", "berbeda jauh", "milik orang dewasa", "sangat pendek"], "A", "Jumlah jengkal sama menandakan ukuran bentangan tangan mereka sama.")
tf("c3", "sedang", T, Pr, S1, "Satu hasta umumnya lebih panjang daripada satu jengkal.", "Benar", "Hasta mengukur dari siku ke jari tengah, jengkal hanya jari tangan.")
sa("c3", "mudah", T, Pr, S2, "Panjang lorong 18 langkah. Dito sudah jalan 10 langkah. Berapa langkah sisa?", "8", "18 - 10 = 8 langkah.", verifikasi={"ekspresi": "18 - 10", "hasil": "8"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Ibu jari ke kelingking Dina 10 cm. 3 jengkal Dina sama dengan berapa cm?", ["30 cm", "20 cm", "25 cm", "35 cm"], "A", "10 + 10 + 10 = 30 cm.", verifikasi={"ekspresi": "3 * 10", "hasil": "30"})
mc("c3", "sedang", X, Pr, S2, "Panjang panggung 12 depa. Lebar panggung 5 depa. Berapa selisihnya?", ["7 depa", "6 depa", "8 depa", "5 depa"], "A", "12 - 5 = 7 depa.", verifikasi={"ekspresi": "12 - 5", "hasil": "7"})
tf("c3", "sedang", X, Pr, S3, "Satu batang pensil sama panjang dengan 6 klip kertas yang dijajarkan rapat.", "Benar", "Klip kertas yang seragam dapat mengukur panjang pensil.")
sa("c3", "sedang", X, Pr, S4, "Meja diukur 7 jengkal anak dan 4 jengkal guru. Berapa selisih angkanya?", "3", "7 - 4 = 3 jengkal.", verifikasi={"ekspresi": "7 - 4", "hasil": "3"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Tali A panjangnya 9 jengkal. Tali B panjangnya 13 jengkal. Berapa jengkal tali B lebih panjang?", ["4 jengkal", "3 jengkal", "5 jengkal", "2 jengkal"], "A", "13 - 9 = 4 jengkal.", verifikasi={"ekspresi": "13 - 9", "hasil": "4"})
mc("c3", "sedang", K, Pr, S3, "Penghapus = 2 klip. Kotak pensil = 8 klip. Kotak pensil setara berapa penghapus?", ["4 penghapus", "3 penghapus", "5 penghapus", "2 penghapus"], "A", "8 / 2 = 4 penghapus.", verifikasi={"ekspresi": "8 // 2", "hasil": "4"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Urutan ukuran tak baku dari yang paling pendek ke paling panjang adalah ....", ["jengkal, hasta, depa", "depa, hasta, jengkal", "hasta, jengkal, depa", "jengkal, depa, hasta"], "A", "Jengkal (tangan) < hasta (lengan) < depa (rentangan dua tangan).")
mc("c4", "sedang", T, Kn, S2, "Mengapa lapangan bola lebih tepat diukur dengan langkah daripada jengkal?", ["karena lapangan sangat luas dan butuh alat lebih cepat", "karena jengkal tidak bisa dipakai di tanah", "karena langkah lebih berat", "karena jengkal hanya untuk kain"], "A", "Langkah kaki jauh lebih efisien untuk mengukur jarak yang sangat panjang.")
tf("c4", "sedang", T, Kn, S3, "Klip kertas besar dan klip kertas kecil boleh dicampur saat mengukur satu pensil.", "Salah", "Alat ukur tak baku harus menggunakan ukuran yang seragam.")
tf("c4", "sedang", T, Kn, S4, "Tangan orang dewasa lebih panjang, sehingga hasil bilangannya lebih kecil.", "Benar", "Karena satuan lebih besar, maka jumlah kali pengulangan lebih sedikit.")
sa("c4", "sedang", T, Kn, S4, "Tali diukur Dayu dapat 15 jengkal, diukur Udin 11 jengkal. Berapa selisihnya?", "4", "15 - 11 = 4 jengkal.", verifikasi={"ekspresi": "15 - 11", "hasil": "4"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Jika 1 hasta sama dengan 2 jengkal, maka 4 hasta sama dengan berapa jengkal?", ["8 jengkal", "6 jengkal", "10 jengkal", "7 jengkal"], "A", "4 x 2 = 8 jengkal.", verifikasi={"ekspresi": "4 * 2", "hasil": "8"})
mc("c4", "sedang", X, Kn, S2, "Ani melangkah 15 langkah. Roni melangkah 12 langkah untuk jarak yang sama. Langkah siapa lebih panjang?", ["Roni", "Ani", "keduanya sama", "tidak tahu"], "A", "Roni butuh langkah lebih sedikit, artinya langkah kaki Roni lebih panjang.")
tf("c4", "sedang", X, Kn, S4, "Ukuran jengkal tangan setiap orang di dunia selalu sama persis.", "Salah", "Ukuran tangan manusia berbeda-beda tergantung usia dan tubuh.")
mc("c4", "sulit", X, Me, S3, "Pensil A = 5 klip. Pensil B = 7 klip. Pensil C = 4 klip. Berapa total klip ketiganya?", ["16 klip", "15 klip", "17 klip", "14 klip"], "A", "5 + 7 + 4 = 16 klip.", verifikasi={"ekspresi": "5 + 7 + 4", "hasil": "16"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Manakah pernyataan yang BENAR mengenai jengkal dan hasta?", ["hasta lebih panjang dari jengkal", "jengkal lebih panjang dari hasta", "jengkal dan hasta sama persis", "jengkal diukur dari siku"], "A", "Hasta mengukur dari siku ke jari, jadi lebih panjang dari jengkal.")
mc("c4", "sulit", K, Me, S2, "Pagar sekolah = 10 depa. Jika 1 depa = 2 langkah, berapa langkah panjang pagar?", ["20 langkah", "18 langkah", "22 langkah", "15 langkah"], "A", "10 x 2 = 20 langkah.", verifikasi={"ekspresi": "10 * 2", "hasil": "20"})
tf("c4", "sulit", K, Me, S3, "Penggaris plastik dan klip kertas keduanya adalah satuan baku standar.", "Salah", "Klip kertas adalah satuan tak baku, sedangkan penggaris adalah satuan baku.")
mc("c4", "sulit", K, Me, S4, "Meja = 6 jengkal ayah atau 10 jengkal adik. Berapa selisih jengkal mereka?", ["4 jengkal", "3 jengkal", "5 jengkal", "2 jengkal"], "A", "10 - 6 = 4 jengkal.", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Meja guru = 8 jengkal. Meja siswa = 5 jengkal. Berapa jengkal total panjang kedua meja?", ["13 jengkal", "12 jengkal", "14 jengkal", "11 jengkal"], "A", "8 + 5 = 13 jengkal.", verifikasi={"ekspresi": "8 + 5", "hasil": "13"})
mc("c5", "sedang", T, Me, S2, "Ruang kelas = 9 depa. Koridor = 11 depa. Berapa total panjang keduanya?", ["20 depa", "19 depa", "21 depa", "18 depa"], "A", "9 + 11 = 20 depa.", verifikasi={"ekspresi": "9 + 11", "hasil": "20"})
mc("c5", "sedang", T, Me, S3, "Beni mengukur tali dengan 8 batang korek api. 2 batang patah. Berapa batang utuh terpakai?", ["6 batang", "5 batang", "7 batang", "4 batang"], "A", "8 - 2 = 6 batang.", verifikasi={"ekspresi": "8 - 2", "hasil": "6"})
mc("c5", "sulit", T, Me, S4, "Mengapa pedagang kain sekarang memakai meteran bukan hasta?", ["agar ukuran kain selalu pasti dan adil bagi pembeli", "karena hasta terlalu sulit dipakai", "karena tangan pedagang terlalu panjang", "karena kain terlalu licin"], "A", "Meteran adalah satuan baku yang ukurannya adil dan tidak berubah.")

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Papan tulis = 10 jengkal. Lemari = 6 jengkal. Berapa jengkal selisih panjangnya?", ["4 jengkal", "3 jengkal", "5 jengkal", "2 jengkal"], "A", "10 - 6 = 4 jengkal.", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})
mc("c5", "sulit", K, Me, S4, "Jika tali diukur 12 jengkal anak sama dengan 8 jengkal ibu, berapa selisih jengkalnya?", ["4 jengkal", "3 jengkal", "5 jengkal", "2 jengkal"], "A", "12 - 8 = 4 jengkal.", verifikasi={"ekspresi": "12 - 8", "hasil": "4"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Rancanglah urutan alat ukur tubuh dari rentang terpendek ke terpanjang!", ["jengkal, hasta, depa", "depa, hasta, jengkal", "hasta, depa, jengkal", "jengkal, depa, hasta"], "A", "Urutan: jengkal (jari), hasta (lengan), depa (dua tangan).")
mc("c6", "sulit", K, Me, S3, "Susunlah cara mengukur panjang buku memakai penghapus secara tepat!", ["jajarkan penghapus berderet lurus dari ujung ke ujung", "tumpuk penghapus ke atas", "taruh satu penghapus di tengah saja", "ukur miring melintang"], "A", "Jajarkan penghapus rapat lurus dari ujung satu ke ujung lain.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "1 depa setara 4 hasta. Jika dinding = 3 depa, berapa hasta panjang dinding?", ["12 hasta", "10 hasta", "14 hasta", "8 hasta"], "A", "3 x 4 = 12 hasta.", verifikasi={"ekspresi": "3 * 4", "hasil": "12"})
mc("c6", "sulit", P, Me, S3, "1 buku = 5 klip. Jika kamu punya 4 buku berjejer, berapa klip total panjangnya?", ["20 klip", "18 klip", "22 klip", "16 klip"], "A", "4 x 5 = 20 klip.", verifikasi={"ekspresi": "4 * 5", "hasil": "20"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab22_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab22.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
