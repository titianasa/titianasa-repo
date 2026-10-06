#!/usr/bin/env python3
"""
Generator dan validator Bab 55 Matematika Kelas 2 SD:
"Kesalahan Umum: Bagian yang Tidak Sama Besar Dianggap Sama" (Fase A)
bab_id: 51a26744-044b-4c93-921d-1b8583494481
article_id: 06dd249b-21f8-4061-a84c-7658d2231eb1
quiz_id: 443c7d64-42d7-47b6-bdc6-93798812ffe6
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "c1d2e3f4a501"  # Miskonsepsi Potongan Sembarang
S2 = "d2e3f4a5b602"  # Menguji Kesamaan Ukuran dengan Menumpuk/Lipat
S3 = "e3f4a5b6c703"  # Miskonsepsi Pada Pembagian Kumpulan Benda
S4 = "f4a5b6c7d804"  # Cara Memperbaiki dan Kunci Keadilan Pecahan

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Banyak anak keliru saat memotong.
Kue dipotong menjadi dua bagian.
Bagian kanan jauh lebih besar.
Mereka mengira itu setengah.
Padahal itu keliru sekali!
Dua potong sembarang bukan setengah.
Ukuran potongan wajib sama persis.
Jangan terkecoh jumlah potongan!

:::definition
title: Syarat Mutlak Pecahan
Sebuah bagian hanya boleh disebut pecahan jika semua potongan berukuran sama besar.
:::"""

s2_content = """Bagaimana cara menguji potongan kita?
Cobalah menumpuk kedua potongan benda.
Letakkan satu potongan di atas yang lain.
Apakah tepiannya pas menutupi rapat?
Jika ada yang berlebih, potongannya tidak sama.
Artinya potongan itu bukan pecahan setengah!
Lipatan simetri membantu kita memotong adil.
Garis tengah menjamin potongan sama besar.

:::steps
title: Cara Menguji Potongan Sama Besar
1. Tumpuk potongan satu di atas potongan lainnya.
2. Periksa apakah semua sisi saling menutupi.
3. Jika ukurannya pas, potongannya sama besar.
:::"""

s3_content = """Kesalahan juga terjadi pada kumpulan benda.
Budi mempunyai sepuluh buah kelereng.
Budi membagi kelereng menjadi dua kelompok.
Satu kelompok berisi tujuh kelereng.
Kelompok lain berisi tiga kelereng.
Budi mengira tujuh itu setengahnya.
Padahal tujuh dan tiga tidak sama!
Setengah dari sepuluh kelereng adalah lima.
Kedua kelompok wajib sama banyak."""

s4_content = """Ingatlah selalu kunci keadilan dalam pecahan.
Pecahan berasal dari kata pecah yang adil.
Hitunglah jumlahnya dengan teliti.
Ukur panjang atau luasnya dengan cermat.
Jangan membagi benda secara tergesa-gesa.
Berbagilah dengan jujur dan adil!

:::common_trap
title: Mengira Asal Dibagi Menjadi Dua Sudah Setengah
Memotong roti sembarang menjadi dua bagian bukan setengah!
Jika satu bagian besar dan satu kecil, pembagian itu salah.
Setengah wajib berukuran sama besar.
:::

:::callout
variant: summary
title: Ringkasan
text: Pecahan wajib adil dan berukuran sama besar. Asal memotong sembarang bukan pecahan setengah atau seperempat.
:::"""

sections = [
    {
        "id": S1,
        "title": "Miskonsepsi Potongan Sembarang",
        "minutes": 6,
        "goal": "Siswa mengenali kesalahan umum yang menganggap potongan berbeda ukuran sebagai pecahan.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Menguji Kesamaan Ukuran dengan Menumpuk/Lipat",
        "minutes": 6,
        "goal": "Siswa mampu menguji kesamaan ukuran potongan bangun datar dengan cara menumpuk atau melipat.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Miskonsepsi Pada Pembagian Kumpulan Benda",
        "minutes": 6,
        "goal": "Siswa mampu mengenali kesalahan membagi kumpulan objek yang tidak sama banyak.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Cara Memperbaiki dan Kunci Keadilan Pecahan",
        "minutes": 6,
        "goal": "Siswa mampu memperbaiki kesalahan pembagian agar menghasilkan pecahan yang adil dan akurat.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Bagian yang Tidak Sama Besar Dianggap Sama",
    "topic": "Mengenal Setengah dan Seperempat",
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
# 2. DEFINISI BANK 50 SOAL BAB 55
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
mc("c1", "mudah", D, F, S1, "Syarat utama suatu potongan disebut pecahan setengah adalah ....", ["kedua bagian berukuran sama besar", "jumlah potongan ada tiga", "dipotong dengan gunting", "warnanya berbeda"], "A", "Kedua bagian wajib berukuran sama besar.")
tf("c1", "mudah", D, F, S2, "Menumpuk dua potongan membuktikan apakah keduanya sama besar.", "Benar", "Jika kedua potongan saling menutupi rapat saat ditumpuk, berarti sama besar.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S3, "Ada 6 apel dibagi 4 dan 2. Apakah adil?", ["tidak adil karena tidak sama banyak", "sangat adil", "adil bagi yang lapar", "selalu benar"], "A", "Tidak adil karena 4 tidak sama dengan 2.")
mc("c1", "mudah", T, F, S3, "Berapakah pembagian setengah yang benar dari 6 apel?", ["3 apel dan 3 apel", "4 apel dan 2 apel", "5 apel dan 1 apel", "6 apel dan 0 apel"], "A", "6 : 2 = 3 apel per anak.", verifikasi={"ekspresi": "6 / 2", "hasil": "3"})
sa("c1", "mudah", T, F, S3, "Berapa apel tiap anak jika 8 apel dibagi setengah adil?", "4", "8 : 2 = 4 apel.", verifikasi={"ekspresi": "8 / 2", "hasil": "4"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Roti dipotong jadi dua, satu besar satu kecil. Mengapa bukan setengah?", ["karena kedua potongan tidak sama besar", "karena rotinya tawar", "karena pisaunya tumpul", "karena rotinya dingin"], "A", "Bukan setengah karena kedua potongan tidak berukuran sama besar.")
tf("c2", "mudah", D, Kn, S4, "Asal memotong roti menjadi dua bagian pasti menghasilkan setengah.", "Salah", "Jika potongannya tidak sama besar, itu bukan setengah.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Edo memotong kertas miring di pojok jadi 2. Edo bilang setengah. Benarkah?", ["salah karena ukurannya tidak sama besar", "benar karena ada 2 potong", "benar sekali", "pasti betul"], "A", "Salah karena ukuran potongan tidak sama besar.", "Mengira asal dipotong dua sudah pasti setengah")
mc("c2", "mudah", R, Kn, S3, "Ada 10 donat dibagi 6 dan 4. Mengapa bukan setengah?", ["karena 6 tidak sama dengan 5", "karena donatnya manis", "karena kotaknya kecil", "karena jumlahnya genap"], "A", "Setengah dari 10 adalah 5, bukan 6 atau 4.", "Miskonsepsi membagi kelompok tidak sama banyak")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S2, "Saat ditumpuk, potongan A menutupi potongan B dengan pas. Artinya?", ["kedua potongan berukuran sama besar", "potongan A lebih besar", "potongan B lebih tebal", "keduanya berbeda bentuk"], "A", "Menutupi pas artinya berukuran persis sama besar.")
mc("c2", "mudah", T, Kn, S3, "Dono membagi 12 kelereng jadi 8 dan 4. Harusnya Dono membagi ....", ["6 dan 6", "7 dan 5", "8 dan 4", "9 dan 3"], "A", "12 : 2 = 6 kelereng tiap kelompok.", verifikasi={"ekspresi": "12 / 2", "hasil": "6"})
tf("c2", "mudah", T, Kn, S1, "Potongan pizza yang tidak sama besar tidak boleh disebut pecahan adil.", "Benar", "Pecahan mewajibkan keadilan ukuran potongan.")
sa("c2", "mudah", T, Kn, S3, "Berapakah banyak donat per kelompok jika 14 donat dibagi rata?", "7", "14 : 2 = 7 donat.", verifikasi={"ekspresi": "14 / 2", "hasil": "7"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Lina membagi 16 permen jadi 10 dan 6. Berapa selisihnya?", ["4 permen", "2 permen", "3 permen", "5 permen"], "A", "10 - 6 = 4 permen selisihnya.", "Salah menghitung ketimpangan pembagian", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})
mc("c3", "sedang", R, Pr, S4, "Berapa permen yang harus dipindah dari 10 permen agar seimbang dengan 6?", ["2 permen", "1 permen", "3 permen", "4 permen"], "A", "10 - 2 = 8 dan 6 + 2 = 8 permen.", "Keliru menyeimbangkan kelompok", verifikasi={"ekspresi": "(10 - 6) / 2", "hasil": "2"})

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Manakah garis potong persegi yang menghasilkan dua bagian sama besar?", ["garis lurus tepat di tengah", "garis di dekat sudut", "garis lengkung acak", "garis miring sembarang"], "A", "Garis tengah membagi luas persegi sama rata.")
mc("c3", "mudah", T, Pr, S3, "Ada 18 biskuit dibagi jadi 11 dan 7. Berapa harusnya per kelompok?", ["9 biskuit", "8 biskuit", "10 biskuit", "7 biskuit"], "A", "18 : 2 = 9 biskuit per kelompok.", verifikasi={"ekspresi": "18 / 2", "hasil": "9"})
tf("c3", "sedang", T, Pr, S2, "Jika dua potongan kertas memiliki sisa saat ditumpuk, maka keduanya tidak sama besar.", "Benar", "Ada sisa berarti luasnya berbeda.")
mc("c3", "sedang", T, Pr, S4, "Ali membagi semangka jadi 4 potong acak. Apakah tiap potong seperempat?", ["bukan karena ukurannya tidak sama besar", "ya pasti seperempat", "ya karena ada 4 potong", "tergantung bijinya"], "A", "Bukan seperempat karena ukurannya tidak sama besar.")
tf("c3", "sedang", T, Pr, S3, "Membagi 20 kelereng menjadi 12 dan 8 adalah pembagian setengah yang benar.", "Salah", "Setengah dari 20 adalah 10, bukan 12 dan 8.")
sa("c3", "sedang", T, Pr, S3, "Berapakah setengah yang adil dari 22 jeruk?", "11", "22 : 2 = 11 jeruk.", verifikasi={"ekspresi": "22 / 2", "hasil": "11"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Budi memotong tali 30 cm jadi 20 cm dan 10 cm. Apakah setengah?", ["bukan karena panjangnya tidak sama", "ya karena dipotong jadi dua", "ya selalu setengah", "tidak ada yang tahu"], "A", "Bukan setengah karena 20 cm berbeda dengan 10 cm.")
mc("c3", "sedang", X, Pr, S2, "Cara paling tepat membuktikan lipatan kertas menghasilkan setengah adalah ....", ["melihat kedua bagian saling menutup rapat", "menimbang kertas", "mencium aroma kertas", "merobeknya sembarang"], "A", "Menutup rapat membuktikan kedua bagian berukuran sama luas.")
tf("c3", "sedang", X, Pr, S4, "Pecahan seperempat membolehkan salah satu bagian lebih besar dari lainnya.", "Salah", "Keempat bagian pada pecahan seperempat wajib berukuran sama besar.")
sa("c3", "sedang", X, Pr, S3, "Berapakah bagian yang benar jika 24 buku dibagi 4 anak sama rata?", "6", "24 : 4 = 6 buku.", verifikasi={"ekspresi": "24 / 4", "hasil": "6"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S3, "Dari 28 apel, Siti mengambil 16 dan adiknya 12. Berapa selisihnya?", ["4 apel", "2 apel", "3 apel", "5 apel"], "A", "16 - 12 = 4 apel.", verifikasi={"ekspresi": "16 - 12", "hasil": "4"})
mc("c3", "sedang", K, Pr, S4, "Agar pembagian apel Siti dan adiknya adil, tiap anak harusnya dapat ....", ["14 apel", "13 apel", "15 apel", "12 apel"], "A", "28 : 2 = 14 apel per anak.", verifikasi={"ekspresi": "28 / 2", "hasil": "14"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa membagi kue sembarang menjadi dua bagian sering memicu pertengkaran?", ["karena ukurannya tidak sama besar sehingga tidak adil", "karena kuenya tidak enak", "karena warnanya gelap", "karena piringnya kotor"], "A", "Perbedaan ukuran memicu rasa tidak adil bagi yang mendapat bagian kecil.")
mc("c4", "sedang", T, Kn, S2, "Jika dua bangun datar tidak pas saat ditumpuk, manakah kesimpulan yang BENAR?", ["luas kedua bangun tidak sama besar", "luas kedua bangun pasti sama", "kedua bangun pasti lingkaran", "salah satu bangun gaib"], "A", "Tidak pas saat ditumpuk membuktikan luasnya tidak sama besar.")
tf("c4", "sedang", T, Kn, S3, "Membagi 30 mangga menjadi 16 dan 14 adalah pembagian yang adil.", "Salah", "16 dan 14 tidak sama banyak, pembagian adil adalah 15 dan 15.")
tf("c4", "sedang", T, Kn, S4, "Garis yang tidak melalui pusat lingkaran tidak membagi lingkaran jadi dua sama besar.", "Benar", "Hanya garis yang melalui titik pusat yang membagi lingkaran dua sama besar.")
sa("c4", "sedang", T, Kn, S4, "Berapa selisih pembagian 32 kelereng jika dibagi 20 dan 12?", "8", "20 - 12 = 8 kelereng.", verifikasi={"ekspresi": "20 - 12", "hasil": "8"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Lina membagi pizza 4 potong: 2 besar dan 2 kecil. Apakah itu seperempat?", ["bukan karena keempat bagian tidak sama besar", "ya karena ada 4 potong", "pasti seperempat", "tergantung rasa pizza"], "A", "Bukan seperempat karena ukurannya berbeda-beda.")
mc("c4", "sedang", X, Kn, S3, "Ada 36 kelereng dibagi jadi 22 dan 14. Berapa butir harus dipindah agar adil?", ["4 kelereng", "2 kelereng", "6 kelereng", "8 kelereng"], "A", "36 : 2 = 18; 22 - 18 = 4 kelereng harus dipindahkan.", verifikasi={"ekspresi": "(22 - 14) / 2", "hasil": "4"})
tf("c4", "sedang", X, Kn, S2, "Memotong persegi dari pojok sembarang pasti menghasilkan dua segitiga sama besar.", "Salah", "Hanya garis diagonal simetris yang menghasilkan dua segitiga sama besar.")
mc("c4", "sulit", X, Me, S4, "Manakah dari gambar berikut yang PASTI BUKAN pecahan setengah?", ["persegi dipotong garis dekat sudut", "lingkaran dipotong garis diameter tengah", "persegi panjang dipotong garis tengah", "segitiga sama sisi dipotong garis tinggi simetri"], "A", "Garis dekat sudut pada persegi menghasilkan satu segitiga kecil dan satu segi lima besar.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Apa bahaya menganggap potongan sembarang sebagai pecahan setengah?", ["pemahaman konsep pecahan menjadi salah dan keliru", "kertas menjadi sobek", "makanan menjadi basi", "tidak ada bahaya"], "A", "Akan menanamkan miskonsepsi bahwa pecahan tidak membutuhkan keadilan ukuran.")
mc("c4", "sulit", K, Me, S2, "Kain 40 cm dipotong jadi 25 cm dan 15 cm. Berapa cm kelebihan potongan besar?", ["10 cm", "5 cm", "15 cm", "8 cm"], "A", "25 - 15 = 10 cm.", verifikasi={"ekspresi": "25 - 15", "hasil": "10"})
tf("c4", "sulit", K, Me, S4, "Pecahan adalah pembagian matematika yang menjamin nilai yang setara.", "Benar", "Pecahan selalu berlandaskan bagian yang sama besar.")
mc("c4", "sulit", K, Me, S3, "Berapakah hasil dari (setengah adil dari 50) dikurangi (setengah adil dari 30)?", ["10", "8", "12", "15"], "A", "25 - 15 = 10.", verifikasi={"ekspresi": "(50 / 2) - (30 / 2)", "hasil": "10"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Jika seseorang membagi 40 kue jadi 25 dan 15, berapa harus dipindah agar adil?", ["5 kue", "10 kue", "4 kue", "6 kue"], "A", "40 : 2 = 20 kue; 25 - 20 = 5 kue dipindahkan.", verifikasi={"ekspresi": "(25 - 15) / 2", "hasil": "5"})
mc("c5", "sedang", T, Me, S2, "Kayu 60 cm dipotong 35 cm dan 25 cm. Berapa selisih kedua potong?", ["10 cm", "5 cm", "8 cm", "12 cm"], "A", "35 - 25 = 10 cm.", verifikasi={"ekspresi": "35 - 25", "hasil": "10"})
mc("c5", "sedang", T, Me, S3, "Ada 48 jeruk dibagi 4 anak: 15, 15, 10, 8. Harusnya tiap anak dapat ....", ["12 jeruk", "10 jeruk", "14 jeruk", "11 jeruk"], "A", "48 : 4 = 12 jeruk per anak.", verifikasi={"ekspresi": "48 / 4", "hasil": "12"})
mc("c5", "sulit", T, Me, S4, "Berapakah selisih antara bagian terbesar (15) dengan bagian adil (12) pada jeruk tadi?", ["3 jeruk", "2 jeruk", "4 jeruk", "1 jeruk"], "A", "15 - 12 = 3 jeruk.", verifikasi={"ekspresi": "15 - (48 / 4)", "hasil": "3"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S2, "Tali 70 cm dipotong jadi dua: 45 cm dan 25 cm. Berapa panjang bagian adil?", ["35 cm", "30 cm", "40 cm", "25 cm"], "A", "70 : 2 = 35 cm.", verifikasi={"ekspresi": "70 / 2", "hasil": "35"})
mc("c5", "sulit", K, Me, S4, "Berapakah hasil dari (setengah adil dari 84) - 20?", ["22", "20", "24", "18"], "A", "(84 : 2) - 20 = 42 - 20 = 22.", verifikasi={"ekspresi": "(84 / 2) - 20", "hasil": "22"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Bagaimana kamu menasehati teman yang membagi semangka tidak sama besar tapi menyebutnya setengah?", ["jelaskan dengan sopan bahwa pecahan setengah wajib memiliki ukuran potongan yang sama besar", "marahi teman tersebut", "ambil semua potongan semangka", "diam saja"], "A", "Menjelaskan konsep keadilan ukuran pecahan secara bijak dan sopan.")
mc("c6", "sulit", K, Me, S4, "Pita 90 cm dipotong 60 cm dan 30 cm. Berapa selisih kedua pita?", ["30 cm", "20 cm", "10 cm", "15 cm"], "A", "60 - 30 = 30 cm.", verifikasi={"ekspresi": "60 - 30", "hasil": "30"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S4, "Hitunglah hasil operasi: (setengah adil dari 92) - (seperempat adil dari 64) + 10!", ["40", "36", "42", "38"], "A", "(92 : 2) - (64 : 4) + 10 = 46 - 16 + 10 = 40.", verifikasi={"ekspresi": "(92 / 2) - (64 / 4) + 10", "hasil": "40"})
mc("c6", "sulit", P, Me, S3, "Ada 4 kelompok bibit: 30, 25, 25, 20. Berapa selisih terbanyak dan tersedikit?", ["10 bibit", "5 bibit", "15 bibit", "8 bibit"], "A", "Terbanyak = 30, tersedikit = 20. Selisih = 30 - 20 = 10 bibit.", verifikasi={"ekspresi": "30 - 20", "hasil": "10"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab55_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab55.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
