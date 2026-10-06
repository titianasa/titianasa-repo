#!/usr/bin/env python3
"""
Generator dan validator Bab 64 Matematika Kelas 2 SD:
"Membaca Timbangan Sederhana: Kilogram" (Fase A)
bab_id: 34fbf801-352f-4032-a8a7-8d7594c06ad0
article_id: 24b800bd-7a48-46f8-9a6c-da9f19a85ffc
quiz_id: 588308c1-f773-484e-baf1-7932b273d8c6
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "i1k2m3o4q501"  # Mengenal Timbangan dan Satuan Kilogram
S2 = "j2l3n4p5r602"  # Membaca Jarum Timbangan
S3 = "k3m4o5q6s703"  # Membandingkan Berat Berdasarkan Kilogram
S4 = "l4n5p6r7t804"  # Menghitung Berat Gabungan dan Selisih

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Selain panjang, benda memiliki berat.
Alat pengukur berat adalah timbangan.
Ada timbangan duduk dan dapur.
Satuan baku berat adalah kilogram.
Kilogram disingkat menjadi kg.
Gunakan huruf k dan g kecil.
Kilogram dipakai menimbang beras.
Juga menimbang buah dan semangka!

:::definition
title: Kilogram (kg)
Satuan baku yang digunakan untuk menyatakan ukuran berat benda.
:::"""

s2_content = """Perhatikan jarum pada timbangan.
Sebelum dipakai menimbang benda.
Jarum harus menunjuk angka nol.
Lalu letakkan benda di atasnya.
Wadah akan menekan timbangan.
Jarum berputar ke kanan.
Jarum berhenti di suatu angka.
Angka itu adalah berat benda.
Jika menunjuk 3, beratnya 3 kg!

:::steps
title: Langkah Membaca Timbangan Jarum
1. Pastikan jarum tepat di angka 0.
2. Letakkan benda di piringan timbangan.
3. Tunggu sampai jarum diam tidak bergoyang.
4. Baca angka yang ditunjuk jarum timbangan.
:::"""

s3_content = """Kita bisa membandingkan berat benda.
Bandingkan angka kilogramnya.
Beras beratnya 5 kg.
Melon beratnya 2 kg.
Angka 5 lebih besar dari 2.
Maka beras lebih berat dari melon.
Melon lebih ringan dari beras.
Jika angkanya sama, beratnya seimbang.
Telitilah melihat angka penunjuknya!"""

s4_content = """Kita juga bisa menghitung berat.
Ibu membeli 3 kg apel.
Ibu juga membeli 2 kg jeruk.
Berapa berat seluruh buah Ibu?
Jumlahkan: 3 ditambah 2.
Total berat buah adalah 5 kg.
Berapa selisih berat apel dan jeruk?
Kurangi: 3 dikurang 2.
Selisih beratnya adalah 1 kg!

:::common_trap
title: Mengira Benda Besar Selalu Lebih Berat
Benda yang berukuran besar belum tentu lebih berat.
Kapas besar bisa lebih ringan dari sebongkah batu kecil.
Gunakan timbangan untuk memastikan beratnya!
:::

:::callout
variant: summary
title: Ringkasan
text: Timbangan mengukur berat. Satuan kilogram disingkat kg. Pastikan jarum mulai dari nol.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Timbangan dan Satuan Kilogram",
        "minutes": 6,
        "goal": "Siswa mengenal timbangan dan satuan baku kilogram (kg).",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Membaca Jarum Timbangan",
        "minutes": 6,
        "goal": "Siswa mampu membaca posisi jarum timbangan sederhana dengan benar.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membandingkan Berat Berdasarkan Kilogram",
        "minutes": 6,
        "goal": "Siswa mampu membandingkan benda lebih berat atau lebih ringan berdasarkan satuan kg.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menghitung Berat Gabungan dan Selisih",
        "minutes": 6,
        "goal": "Siswa mampu menjumlahkan dan mengurangkan berat benda dalam kilogram.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membaca Timbangan Sederhana: Kilogram",
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
# 2. DEFINISI BANK 50 SOAL BAB 64
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
mc("c1", "mudah", D, F, S1, "Alat yang paling tepat untuk mengukur berat semangka adalah ....", ["timbangan", "penggaris", "termometer", "jam tangan"], "A", "Timbangan adalah alat pengukur berat.")
tf("c1", "mudah", D, F, S1, "Satuan kilogram disingkat dengan huruf kecil kg.", "Benar", "Kilogram disingkat kg.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Sebelum benda diletakkan, jarum timbangan harus menunjuk angka ....", ["0", "1", "5", "10"], "A", "Timbangan harus diatur dari angka nol sebelum dipakai.", verifikasi={"ekspresi": "0 / 1", "hasil": "0"})
mc("c1", "mudah", T, F, S3, "Semangka 4 kg dan apel 1 kg. Manakah yang lebih berat?", ["semangka", "apel", "keduanya sama", "tidak tahu"], "A", "4 kg lebih besar daripada 1 kg.")
sa("c1", "mudah", T, F, S2, "Jarum timbangan menunjuk angka 7. Berat benda adalah ... kg.", "7", "Beratnya adalah 7 kg.", verifikasi={"ekspresi": "7 - 0", "hasil": "7"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Pepaya 3 kg dan melon 3 kg. Pernyataan yang benar adalah ....", ["kedua buah sama berat", "pepaya lebih berat", "melon lebih berat", "pepaya lebih ringan"], "A", "Kedua buah memiliki berat yang sama yaitu 3 kg.")
tf("c2", "mudah", D, Kn, S4, "Berat gabungan beras 5 kg dan beras 2 kg adalah 7 kg.", "Benar", "5 + 2 = 7 kg.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Jarum menunjuk angka 1 saat kosong. Jika benda ditimbang, jarum di 5. Berat sebenarnya?", ["4 kg", "5 kg", "6 kg", "1 kg"], "A", "5 - 1 = 4 kg.", "Lupa mengoreksi jarum awal yang tidak di angka nol", verifikasi={"ekspresi": "5 - 1", "hasil": "4"})
mc("c2", "mudah", R, Kn, S3, "Mengapa bantal yang besar bisa lebih ringan dari batu kecil?", ["karena kapas di dalam bantal sangat ringan", "karena bantal empuk", "karena batu warnanya hitam", "karena bantal dari kain"], "A", "Ukuran besar tidak menjamin benda lebih berat.", "Mengira benda besar selalu lebih berat")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Benda manakah yang biasa ditimbang menggunakan satuan kilogram?", ["karung beras", "sebutir obat pil", "selembar kertas", "sebutir beras"], "A", "Karung beras cukup berat sehingga menggunakan kilogram.")
mc("c2", "mudah", T, Kn, S2, "Sebungkus gula ditimbang, jarum menunjuk angka 2. Berat gula adalah ....", ["2 kg", "1 kg", "3 kg", "0 kg"], "A", "Beratnya 2 kg.", verifikasi={"ekspresi": "2 - 0", "hasil": "2"})
tf("c2", "mudah", T, Kn, S1, "Panjang buku tulis diukur menggunakan timbangan dapur.", "Salah", "Panjang diukur dengan penggaris, bukan timbangan.")
sa("c2", "mudah", T, Kn, S3, "Beras 8 kg lebih berat ... kg daripada beras 5 kg.", "3", "8 - 5 = 3 kg.", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S4, "Ibu membeli 6 kg beras dan 4 kg gula. Berapa kg total belanjaan Ibu?", ["10 kg", "2 kg", "24 kg", "8 kg"], "A", "6 + 4 = 10 kg.", "Melakukan pengurangan saat ditanya total berat", verifikasi={"ekspresi": "6 + 4", "hasil": "10"})
mc("c3", "sedang", R, Pr, S4, "Berapakah selisih berat antara labu 9 kg dan nanas 2 kg?", ["7 kg", "11 kg", "8 kg", "6 kg"], "A", "9 - 2 = 7 kg.", "Melakukan penjumlahan saat ditanya selisih", verifikasi={"ekspresi": "9 - 2", "hasil": "7"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Manakah penulisan berat kilogram yang benar menurut aturan baku?", ["15 kg", "15 KG", "15 Kg", "15 kG"], "A", "Singkatan kilogram ditulis huruf kecil: kg.")
mc("c3", "mudah", T, Pr, S3, "Urutan dari yang paling ringan: labu 6 kg, jeruk 2 kg, melon 4 kg?", ["jeruk, melon, labu", "labu, melon, jeruk", "melon, jeruk, labu", "jeruk, labu, melon"], "A", "2 kg < 4 kg < 6 kg.")
tf("c3", "sedang", T, Pr, S2, "Jika jarum menunjuk angka antara 4 dan 5 tepat di tengah, beratnya lebih dari 4 kg.", "Benar", "Posisi di antara 4 dan 5 berarti lebih dari 4 kg.")
mc("c3", "sedang", T, Pr, S4, "Pak Tani memanen 14 kg jagung dan 15 kg ubi. Berapa kg panen seluruhnya?", ["29 kg", "28 kg", "30 kg", "27 kg"], "A", "14 + 15 = 29 kg.", verifikasi={"ekspresi": "14 + 15", "hasil": "29"})
tf("c3", "sedang", T, Pr, S3, "Benda 12 kg lebih ringan daripada gabungan dua benda masing-masing 5 kg.", "Salah", "5 + 5 = 10 kg, dan 12 kg lebih berat dari 10 kg.")
sa("c3", "sedang", T, Pr, S4, "Satu karung 25 kg beras dikurangi 8 kg. Berapa sisa beras dalam kg?", "17", "25 - 8 = 17 kg.", verifikasi={"ekspresi": "25 - 8", "hasil": "17"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Manakah pasangan alat dan benda yang paling cocok digunakan?", ["timbangan untuk sekarung kentang", "penggaris untuk berat minyak", "termometer untuk panjang pensil", "timbangan untuk panjang kain"], "A", "Sekarung kentang ditimbang dengan timbangan.")
mc("c3", "sedang", X, Pr, S2, "Berapa kilogram berat dua kantong apel jika masing-masing kantong beratnya 4 kg?", ["8 kg", "6 kg", "10 kg", "4 kg"], "A", "4 + 4 = 8 kg.", verifikasi={"ekspresi": "4 + 4", "hasil": "8"})
tf("c3", "sedang", X, Pr, S3, "Sebuah melon 3 kg sama beratnya dengan tiga buah nanas masing-masing 1 kg.", "Benar", "3 x 1 = 3 kg.")
sa("c3", "sedang", X, Pr, S4, "Total berat 18 kg mangga dan 14 kg pepaya adalah ... kg.", "32", "18 + 14 = 32 kg.", verifikasi={"ekspresi": "18 + 14", "hasil": "32"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Urutan dari paling berat: daging 18 kg, ikan 12 kg, ayam 24 kg?", ["ayam, daging, ikan", "ikan, daging, ayam", "daging, ayam, ikan", "ayam, ikan, daging"], "A", "24 kg > 18 kg > 12 kg.")
mc("c3", "sedang", K, Pr, S4, "Kardus A 26 kg, kardus B 19 kg. Berapakah selisih berat keduanya?", ["7 kg", "8 kg", "6 kg", "9 kg"], "A", "26 - 19 = 7 kg.", verifikasi={"ekspresi": "26 - 19", "hasil": "7"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S1
mc("c4", "sedang", T, Kn, S1, "Mengapa timbangan badan tidak cocok digunakan untuk menimbang sebutir kelereng?", ["karena kelereng terlalu ringan untuk menggerakkan pegas timbangan badan", "karena kelereng bulat", "karena timbangan badan terbuat dari kaca", "karena tidak ada angka nol"], "A", "Timbangan badan dirancang untuk beban berat manusia.")
mc("c4", "sedang", T, Kn, S2, "Sebelum ditimbang, jarum menunjuk angka 2. Benda ditimbang, jarum di 8. Berat benda?", ["6 kg", "8 kg", "10 kg", "2 kg"], "A", "8 - 2 = 6 kg.", verifikasi={"ekspresi": "8 - 2", "hasil": "6"})
tf("c4", "sedang", T, Kn, S3, "Jika benda X lebih berat dari Y, dan Y lebih berat dari Z, maka X terberat.", "Benar", "X > Y > Z.")
tf("c4", "sedang", T, Kn, S4, "Mengurangi 15 kg dengan 15 kg menghasilkan berat 1 kg.", "Salah", "15 - 15 = 0 kg, bukan 1 kg.")
sa("c4", "sedang", T, Kn, S4, "Berapakah selisih berat antara (16 kg + 14 kg) dan 22 kg?", "8", "30 - 22 = 8 kg.", verifikasi={"ekspresi": "(16 + 14) - 22", "hasil": "8"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Apa perbedaan utama fungsi timbangan dan penggaris?", ["timbangan mengukur berat, sedangkan penggaris mengukur panjang", "timbangan untuk sekolah, penggaris untuk pasar", "timbangan dari kayu, penggaris dari besi", "keduanya sama saja"], "A", "Fungsi timbangan adalah mengukur berat, penggaris mengukur panjang.")
mc("c4", "sedang", X, Kn, S3, "Benda P (15 kg), Q (22 kg), R (18 kg). Manakah perbandingan yang BENAR?", ["benda Q adalah yang paling berat", "benda P lebih berat dari R", "benda R paling berat", "semua benda sama berat"], "A", "22 kg adalah beban terberat.")
tf("c4", "sedang", X, Kn, S4, "Dua kantong terigu masing-masing 12 kg lebih berat dari sekarung 25 kg.", "Salah", "12 + 12 = 24 kg, dan 24 kg lebih ringan dari 25 kg.")
mc("c4", "sulit", X, Me, S4, "Ibu membeli 45 kg beras. Digunakan memasak 18 kg, lalu membeli lagi 12 kg. Beras Ibu?", ["39 kg", "38 kg", "40 kg", "36 kg"], "A", "45 - 18 + 12 = 27 + 12 = 39 kg.", verifikasi={"ekspresi": "45 - 18 + 12", "hasil": "39"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Mengapa penting memastikan timbangan selalu bersih dan jarumnya di angka 0?", ["agar hasil timbangan tepat dan tidak merugikan pembeli", "agar timbangannya tampak berkilau", "agar pembeli tidak melihat angka", "tidak ada gunanya"], "A", "Timbangan yang bersih dan terkalibrasi menjamin ketepatan ukuran.")
mc("c4", "sulit", K, Me, S2, "Timbangan tanpa benda menunjuk 3 kg. Saat beras diletakkan menunjuk 28 kg. Berat beras?", ["25 kg", "28 kg", "31 kg", "24 kg"], "A", "28 - 3 = 25 kg.", verifikasi={"ekspresi": "28 - 3", "hasil": "25"})
tf("c4", "sulit", K, Me, S3, "Tiga karung masing-masing 10 kg lebih berat daripada satu karung 35 kg.", "Salah", "3 x 10 = 30 kg, dan 30 kg lebih ringan dari 35 kg.")
mc("c4", "sulit", K, Me, S4, "Pak Budi memanen 75 kg semangka. Dijual 48 kg. Berapa kg sisa semangka Pak Budi?", ["27 kg", "28 kg", "26 kg", "29 kg"], "A", "75 - 48 = 27 kg.", verifikasi={"ekspresi": "75 - 48", "hasil": "27"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Pedagang ingin menimbang 50 kg ubi. Ia punya timbangan batas 20 kg. Berapa kali timbang?", ["3 kali timbang", "2 kali timbang", "4 kali timbang", "1 kali timbang"], "A", "20 kg + 20 kg + 10 kg = 3 kali timbang.")
mc("c5", "sedang", T, Me, S2, "Dua karung jagung beratnya sama. Ditimbang bersama jarum di 36 kg. Berat satu karung?", ["18 kg", "16 kg", "19 kg", "20 kg"], "A", "36 : 2 = 18 kg.", verifikasi={"ekspresi": "36 / 2", "hasil": "18"})
mc("c5", "sedang", T, Me, S3, "Empat kantong buah: 8 kg, 15 kg, 12 kg, 20 kg. Selisih terberat dan teringan?", ["12 kg", "10 kg", "14 kg", "15 kg"], "A", "20 - 8 = 12 kg.", verifikasi={"ekspresi": "20 - 8", "hasil": "12"})
mc("c5", "sulit", T, Me, S4, "Kardus berisi 5 bungkus gula masing-masing 3 kg. Berat kardus kosong 2 kg. Total berat?", ["17 kg", "15 kg", "18 kg", "16 kg"], "A", "(5 x 3) + 2 = 15 + 2 = 17 kg.", verifikasi={"ekspresi": "(5 * 3) + 2", "hasil": "17"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Tiga keranjang jeruk berat total 60 kg. Dua keranjang masing-masing 18 kg. Keranjang ke-3?", ["24 kg", "22 kg", "25 kg", "20 kg"], "A", "60 - (18 + 18) = 60 - 36 = 24 kg.", verifikasi={"ekspresi": "60 - (18 + 18)", "hasil": "24"})
mc("c5", "sulit", K, Me, S4, "Beras 80 kg dibagikan rata ke dalam 4 karung kecil. Berapa kg berat 3 karung kecil?", ["60 kg", "50 kg", "40 kg", "70 kg"], "A", "80 : 4 = 20 kg per karung; 3 x 20 = 60 kg.", verifikasi={"ekspresi": "(80 / 4) * 3", "hasil": "60"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Mengapa timbangan pasar perlu diuji dan dicap resmi oleh petugas pemerintah secara berkala?", ["untuk memastikan ukuran tetap adil dan jujur bagi pembeli dan penjual", "agar harganya lebih mahal", "karena pemerintah suka timbangan", "supaya dicat baru"], "A", "Uji tera memastikan timbangan tidak curang dan akurat.")
mc("c6", "sulit", K, Me, S4, "Jumlah berat A dan B = 70 kg. Selisihnya 14 kg. Berapa berat benda yang lebih berat?", ["42 kg", "40 kg", "44 kg", "38 kg"], "A", "(70 - 14) : 2 = 56 : 2 = 28 kg. Benda A = 28 + 14 = 42 kg.", verifikasi={"ekspresi": "((70 - 14) / 2) + 14", "hasil": "42"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi: (4 x 18 kg) - (3 x 15 kg) + 9 kg!", ["36 kg", "34 kg", "38 kg", "32 kg"], "A", "72 - 45 + 9 = 27 + 9 = 36 kg.", verifikasi={"ekspresi": "(4 * 18) - (3 * 15) + 9", "hasil": "36"})
mc("c6", "sulit", P, Me, S3, "Truk membawa 3 karung (25 kg) dan 2 peti (15 kg). Berapa total beban muatannya?", ["105 kg", "100 kg", "110 kg", "95 kg"], "A", "(3 x 25) + (2 x 15) = 75 + 30 = 105 kg.", verifikasi={"ekspresi": "(3 * 25) + (2 * 15)", "hasil": "105"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab64_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab64.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
