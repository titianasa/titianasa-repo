#!/usr/bin/env python3
"""
Generator dan validator Bab 62 Matematika Kelas 2 SD:
"Mengukur Panjang Benda dengan Penggaris" (Fase A)
bab_id: 635e2ea2-e5ec-4a55-acc3-2293ecada739
article_id: 453a321a-b4ae-4168-9ce8-5bdc804868dc
quiz_id: cb7cecb4-19f6-40b9-ad78-0eb33cdca45f
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "g1i2k3m4o501"  # Menyejajarkan Penggaris dengan Benda
S2 = "h2j3l4n5p602"  # Memastikan Pangkal Benda Tepat di Titik Nol
S3 = "i3k4m5o6q703"  # Membaca Garis Skala pada Ujung Benda
S4 = "j4l5n6p7r804"  # Menuliskan Hasil Ukur Panjang

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Mari kita belajar mengukur benda.
Siapkan penggaris dan benda di meja.
Tempelkan penggaris sejajar dengan benda.
Garis penggaris harus lurus menempel.
Penggaris tidak boleh miring.
Jika miring, ukurannya menjadi salah.
Pastikan keduanya berimpit rapi.
Lurus adalah kunci ketepatan ukur!

:::definition
title: Sejajar
Posisi penggaris dan benda terletak lurus berdampingan tanpa kemiringan.
:::"""

s2_content = """Langkah kedua sangat penting.
Perhatikan ujung pangkal benda.
Pasang tepat di garis angka nol.
Ingat, garis angka nol penggaris!
Bukan di ujung kayu terluar.
Ujung penggaris sering punya sisa kosong.
Garis nol adalah awal pengukuran.
Awali dari nol dengan tepat!

:::steps
title: Langkah Mengukur Benda
1. Tempelkan penggaris lurus sejajar benda.
2. Tempatkan pangkal benda di garis angka 0.
3. Lihat angka pada ujung benda lainnya.
4. Tulis hasil ukur dengan satuan cm.
:::"""

s3_content = """Sekarang lihat ujung benda satunya.
Lihatlah lurus dari atas.
Mata tidak boleh melihat miring.
Lihat garis angka yang berimpit.
Jika ujung berimpit angka 11.
Maka panjang benda adalah 11 cm.
Jika mendekati angka 11.
Kita sebut panjangnya kira-kira 11 cm.
Amati garis skala dengan teliti!"""

s4_content = """Setelah mengukur, kita menuliskan hasilnya.
Tulis angka hasil pengukuranmu.
Lalu sertakan satuan sentimeter.
Contoh: Panjang pensil adalah 14 cm.
Jangan lupa menuliskan satuan cm!
Tanpa satuan, orang lain bingung.
Apakah sentimeter atau meter?
Satuan membuat ukuran menjadi jelas.

:::common_trap
title: Melihat Skala Penggaris dari Sudut Miring
Melihat garis ukur dari samping membuat angka meleset.
Arahkan pandangan mata tepat tegak lurus dari atas garis skala!
:::

:::callout
variant: summary
title: Ringkasan
text: Sejajarkan penggaris. Mulai tepat di garis nol. Baca angka ujung tegak lurus.
:::"""

sections = [
    {
        "id": S1,
        "title": "Menyejajarkan Penggaris dengan Benda",
        "minutes": 6,
        "goal": "Siswa mampu meletakkan penggaris lurus sejajar dengan benda yang diukur.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Memastikan Pangkal Benda Tepat di Titik Nol",
        "minutes": 6,
        "goal": "Siswa memahami pentingnya menempatkan pangkal benda tepat pada garis skala angka 0.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Membaca Garis Skala pada Ujung Benda",
        "minutes": 6,
        "goal": "Siswa mampu membaca skala pada ujung benda dengan pandangan tegak lurus.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menuliskan Hasil Ukur Panjang",
        "minutes": 6,
        "goal": "Siswa mampu menuliskan hasil pengukuran panjang lengkap dengan satuan cm.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengukur Panjang Benda dengan Penggaris",
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
# 2. DEFINISI BANK 50 SOAL BAB 62
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
mc("c1", "mudah", D, F, S2, "Pengukuran panjang dengan penggaris sebaiknya diawali dari garis angka ....", ["0", "1", "2", "10"], "A", "Garis angka 0 adalah titik awal pengukuran.")
tf("c1", "mudah", D, F, S1, "Saat mengukur, penggaris harus diletakkan sejajar dengan benda.", "Benar", "Penggaris harus lurus menempel sejajar.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Jika penggaris diletakkan miring saat mengukur, maka hasil ukur akan ....", ["salah atau tidak tepat", "pasti benar", "lebih bagus", "menjadi dua kali lipat"], "A", "Penggaris miring menghasilkan ukuran yang keliru.")
mc("c1", "mudah", T, F, S3, "Arah pandangan mata saat melihat skala penggaris harus ....", ["tegak lurus dari atas", "miring dari kiri", "miring dari kanan", "sambil memejamkan mata"], "A", "Pandangan tegak lurus mencegah pembacaan meleset.")
sa("c1", "mudah", T, F, S4, "Pensil dari angka 0 ke angka 9 memiliki panjang ... cm.", "9", "Panjangnya adalah 9 cm.", verifikasi={"ekspresi": "9 - 0", "hasil": "9"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Manakah penulisan hasil ukur panjang yang paling LENGKAP dan BENAR?", ["Panjang garpu = 16 cm", "Panjang garpu = 16", "Panjang garpu = cm", "16"], "A", "Harus menyertakan angka dan satuan cm.")
tf("c2", "mudah", D, Kn, S2, "Garis angka 0 selalu terletak tepat di tepi kayu terluar penggaris.", "Salah", "Banyak penggaris memiliki celah kosong sebelum garis 0.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Mengapa kita tidak boleh mengukur dari tepi terluar penggaris tanpa garis 0?", ["karena ada ruang kosong sebelum garis nol", "karena tepi penggaris tajam", "karena angkanya hilang", "karena warnanya gelap"], "A", "Ruang kosong sebelum angka 0 membuat hasil ukur berlebih.", "Mengukur dari ujung fisik penggaris")
mc("c2", "mudah", R, Kn, S3, "Budi melihat skala dari samping sehingga angka terbaca 13 bukan 12. Kesalahan Budi?", ["pandangan mata miring tidak tegak lurus", "penggarisnya rusak", "pensilnya memendek", "salah memilih pensil"], "A", "Mata harus tegak lurus di atas garis skala.", "Melihat skala dari arah miring")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Benda manakah yang pengukurannya paling tepat menggunakan penggaris lurus?", ["spidol papan tulis", "bola kasti", "gelas kaca", "bola basket"], "A", "Spidol memiliki batang yang lurus.")
mc("c2", "mudah", T, Kn, S2, "Pangkal sisir diletakkan tepat di angka 0. Ujungnya di angka 13. Panjang sisir?", ["13 cm", "12 cm", "14 cm", "0 cm"], "A", "13 - 0 = 13 cm.", verifikasi={"ekspresi": "13 - 0", "hasil": "13"})
tf("c2", "mudah", T, Kn, S4, "Menuliskan panjang '15' tanpa satuan cm membuat orang lain bingung.", "Benar", "Satuan harus selalu disertakan.")
sa("c2", "mudah", T, Kn, S3, "Kuas lukis berawal di angka 0 dan berakhir di angka 17. Panjangnya ... cm.", "17", "17 - 0 = 17 cm.", verifikasi={"ekspresi": "17 - 0", "hasil": "17"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Ani mulai mengukur dari angka 1 hingga angka 8. Berapakah panjang benda Ani?", ["7 cm", "8 cm", "9 cm", "1 cm"], "A", "8 - 1 = 7 cm.", "Langsung membaca angka akhir padahal mulai dari angka 1", verifikasi={"ekspresi": "8 - 1", "hasil": "7"})
mc("c3", "sedang", R, Pr, S4, "Doni mengukur dua sedotan: 12 cm dan 8 cm. Berapa panjang gabungannya?", ["20 cm", "18 cm", "22 cm", "10 cm"], "A", "12 + 8 = 20 cm.", "Salah menjumlahkan panjang dua benda", verifikasi={"ekspresi": "12 + 8", "hasil": "20"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Sebelum membaca angka skala, kita harus memastikan posisi penggaris ....", ["lurus dan menempel sejajar pada benda", "miring ke atas", "terangkat dari meja", "terbalik"], "A", "Penggaris harus lurus menempel sejajar.")
mc("c3", "mudah", T, Pr, S4, "Panjang buku gambar dari angka 0 ke 24 adalah ....", ["24 cm", "23 cm", "25 cm", "20 cm"], "A", "24 - 0 = 24 cm.", verifikasi={"ekspresi": "24 - 0", "hasil": "24"})
tf("c3", "sedang", T, Pr, S2, "Jika benda diletakkan dari angka 2 ke 10, panjangnya adalah 8 cm.", "Benar", "10 - 2 = 8 cm.")
mc("c3", "sedang", T, Pr, S3, "Ujung benda berada di antara 14 dan 15, sangat dekat ke 15. Panjangnya sekitar ....", ["15 cm", "14 cm", "10 cm", "16 cm"], "A", "Dibulatkan ke angka terdekat yaitu 15 cm.")
tf("c3", "sedang", T, Pr, S4, "Panjang penghapus 5 cm bila digabung dengan penghapus 6 cm menjadi 10 cm.", "Salah", "5 + 6 = 11 cm, bukan 10 cm.")
sa("c3", "sedang", T, Pr, S4, "Gunting ditaruh dari angka 0 sampai 16. Berapakah panjang gunting dalam cm?", "16", "16 - 0 = 16 cm.", verifikasi={"ekspresi": "16 - 0", "hasil": "16"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Bagaimana cara meletakkan penggaris pada tepi meja yang panjang?", ["letakkan berimpit lurus di tepi meja", "letakkan menyilang di tengah meja", "letakkan berdiri tegak", "letakkan miring"], "A", "Berimpit lurus di sepanjang tepi yang diukur.")
mc("c3", "sedang", X, Pr, S2, "Benda diukur dari angka 3 sampai angka 12. Berapakah panjang benda?", ["9 cm", "12 cm", "3 cm", "15 cm"], "A", "12 - 3 = 9 cm.", verifikasi={"ekspresi": "12 - 3", "hasil": "9"})
tf("c3", "sedang", X, Pr, S3, "Mata yang melihat lurus tegak ke skala menghasilkan bacaan paling teliti.", "Benar", "Posisi tegak lurus menghindari kesalahan paralaks.")
sa("c3", "sedang", X, Pr, S4, "Pita 19 cm digunting 7 cm. Berapakah sisa panjang pita dalam cm?", "12", "19 - 7 = 12 cm.", verifikasi={"ekspresi": "19 - 7", "hasil": "12"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Pangkal benda di angka 4 dan ujungnya di angka 15. Berapa panjang benda?", ["11 cm", "15 cm", "19 cm", "10 cm"], "A", "15 - 4 = 11 cm.", verifikasi={"ekspresi": "15 - 4", "hasil": "11"})
mc("c3", "sedang", K, Pr, S4, "Panjang tali A 14 cm dan tali B 13 cm. Berapa panjang gabungannya?", ["27 cm", "26 cm", "28 cm", "25 cm"], "A", "14 + 13 = 27 cm.", verifikasi={"ekspresi": "14 + 13", "hasil": "27"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S1
mc("c4", "sedang", T, Kn, S1, "Edo mengukur pensil dengan penggaris miring, terukur 13 cm. Panjang sebenarnya?", ["lebih pendek dari 13 cm", "lebih panjang dari 13 cm", "tepat 13 cm", "tidak bisa dipastikan"], "A", "Garis miring selalu lebih panjang dari garis lurus tegak.")
mc("c4", "sedang", T, Kn, S2, "Mengapa penggaris harus diawali dari angka 0 dan bukan angka 1?", ["agar angka di ujung langsung menunjukkan panjang benda", "agar penggaris tidak patah", "karena angka 0 paling bagus", "karena angka 1 terlalu kecil"], "A", "Mulai dari 0 membuat angka di ujung langsung menjadi nilai panjang.")
tf("c4", "sedang", T, Kn, S3, "Melihat penggaris dari arah kanan membuat angka skala terlihat bergeser.", "Benar", "Sudut pandang miring membuat bacaan skala meleset.")
tf("c4", "sedang", T, Kn, S4, "Mengukur buku menggunakan dua penggaris berbeda satuan menghasilkan angka sama.", "Salah", "Satuan yang berbeda menghasilkan angka yang berbeda.")
sa("c4", "sedang", T, Kn, S4, "Berapakah selisih panjang antara pensil 18 cm dan krayon 7 cm?", "11", "18 - 7 = 11 cm.", verifikasi={"ekspresi": "18 - 7", "hasil": "11"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Mengapa kita tidak mengukur lingkaran bola dengan penggaris kaku?", ["karena penggaris kaku tidak bisa melengkung mengikuti permukaan bola", "karena penggaris kaku terlalu licin", "karena bola warnanya bulat", "karena bolanya memantul"], "A", "Penggaris kaku hanya untuk garis lurus.")
mc("c4", "sedang", X, Kn, S2, "Benda A 9 cm dan Benda B (3 ke 13 cm). Manakah lebih panjang?", ["Benda B karena panjangnya 10 cm", "Benda A karena mulai dari 0", "sama panjang", "tidak dapat dihitung"], "A", "Benda A = 9 cm, Benda B = 13 - 3 = 10 cm. 10 cm > 9 cm.")
tf("c4", "sedang", X, Kn, S3, "Ujung benda berimpit angka 20 artinya panjangnya pasti 20 cm.", "Salah", "Hanya pasti 20 cm jika pangkalnya diletakkan di angka 0.")
mc("c4", "sulit", X, Me, S4, "Kawat 45 cm dipotong menjadi 3 bagian sama panjang. Panjang satu bagian?", ["15 cm", "12 cm", "18 cm", "14 cm"], "A", "45 : 3 = 15 cm.", verifikasi={"ekspresi": "45 / 3", "hasil": "15"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Apa yang terjadi jika ujung pensil yang diraut tumpul diletakkan tidak pas di garis 0?", ["hasil pengukuran menjadi kurang akurat", "pensil menjadi patah", "penggaris menjadi kotor", "tidak ada pengaruhnya"], "A", "Penempatan ujung yang tidak tepat membuat ukuran meleset.")
mc("c4", "sulit", K, Me, S2, "Penggaris patah dari angka 6 ke angka 23. Berapakah panjang benda itu?", ["17 cm", "23 cm", "16 cm", "18 cm"], "A", "23 - 6 = 17 cm.", verifikasi={"ekspresi": "23 - 6", "hasil": "17"})
tf("c4", "sulit", K, Me, S3, "Pengukuran dari angka 5 ke 18 lebih pendek dari angka 0 ke 12.", "Salah", "18 - 5 = 13 cm, sedangkan 12 - 0 = 12 cm. 13 cm lebih panjang, bukan lebih pendek.")
mc("c4", "sulit", K, Me, S4, "Dua batang kayu digabung panjangnya 38 cm. Kayu pertama 19 cm. Kayu kedua?", ["19 cm", "18 cm", "20 cm", "17 cm"], "A", "38 - 19 = 19 cm.", verifikasi={"ekspresi": "38 - 19", "hasil": "19"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Lina mengukur buku memakai penggaris 20 cm, kurang 7 cm. Berapa panjang buku?", ["27 cm", "25 cm", "26 cm", "28 cm"], "A", "20 + 7 = 27 cm.", verifikasi={"ekspresi": "20 + 7", "hasil": "27"})
mc("c5", "sedang", T, Me, S2, "Benda diletakkan dari angka 7 ke 25. Benda lain dari 0 ke 17. Selisihnya?", ["1 cm", "2 cm", "0 cm", "3 cm"], "A", "Benda 1 = 25 - 7 = 18 cm. Benda 2 = 17 cm. Selisih = 18 - 17 = 1 cm.", verifikasi={"ekspresi": "(25 - 7) - 17", "hasil": "1"})
mc("c5", "sedang", T, Me, S3, "Tiga pensil sama panjang disusun dari 0 sampai 21 cm. Berapa panjang satu pensil?", ["7 cm", "6 cm", "8 cm", "9 cm"], "A", "21 : 3 = 7 cm.", verifikasi={"ekspresi": "21 / 3", "hasil": "7"})
mc("c5", "sulit", T, Me, S4, "Tongkat 60 cm dipotong 15 cm, lalu dipotong lagi 18 cm. Berapa sisa tongkat?", ["27 cm", "28 cm", "25 cm", "30 cm"], "A", "60 - 15 - 18 = 27 cm.", verifikasi={"ekspresi": "60 - 15 - 18", "hasil": "27"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Kayu A (4 ke 22 cm) dan Kayu B 19 cm. Manakah pernyataan BENAR?", ["Kayu B lebih panjang 1 cm dari Kayu A", "Kayu A lebih panjang dari Kayu B", "kedua kayu sama panjang", "Kayu A 22 cm"], "A", "Kayu A = 22 - 4 = 18 cm. Kayu B = 19 cm. 19 - 18 = 1 cm.")
mc("c5", "sulit", K, Me, S4, "Pita 50 cm dipotong menjadi 5 potong sama panjang. Berapa panjang 2 potong?", ["20 cm", "10 cm", "25 cm", "15 cm"], "A", "50 : 5 = 10 cm per potong; 2 x 10 = 20 cm.", verifikasi={"ekspresi": "(50 / 5) * 2", "hasil": "20"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Bagaimana cara mengukur keliling tempat pensil yang berbentuk kotak lurus?", ["mengukur keempat sisinya dengan penggaris lalu menjumlahkannya", "mengukur satu sisi saja", "menimbang tempat pensil", "melihat warnanya"], "A", "Ukur tiap sisi dengan penggaris lalu jumlahkan seluruh sisinya.")
mc("c6", "sulit", K, Me, S4, "Tali 72 cm dipotong jadi 4 bagian sama panjang. Berapa panjang satu bagian?", ["18 cm", "16 cm", "19 cm", "17 cm"], "A", "72 : 4 = 18 cm.", verifikasi={"ekspresi": "72 / 4", "hasil": "18"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi: (4 x 15 cm) - (2 x 18 cm) + 6 cm!", ["30 cm", "28 cm", "32 cm", "26 cm"], "A", "60 - 36 + 6 = 24 + 6 = 30 cm.", verifikasi={"ekspresi": "(4 * 15) - (2 * 18) + 6", "hasil": "30"})
mc("c6", "sulit", P, Me, S3, "Sebuah batang bambu 90 cm dipotong menjadi 6 bagian sama. Panjang tiap bagian?", ["15 cm", "14 cm", "16 cm", "12 cm"], "A", "90 : 6 = 15 cm.", verifikasi={"ekspresi": "90 / 6", "hasil": "15"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab62_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab62.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
