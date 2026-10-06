#!/usr/bin/env python3
"""
Generator dan validator Bab 44 Matematika Kelas 2 SD:
"Kesalahan Umum: Lupa Menyimpan dan Salah Meminjam" (Fase A)
bab_id: bd259b2d-d675-414a-a3b4-a18ca9c77e09
article_id: 8d24b692-26c1-46e9-82ea-155850e820ae
quiz_id: 1d605ab0-a25b-48b0-b954-43d3e82cffb7
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "b2c3d4e5f601"  # Lupa Menambahkan Simpanan
S2 = "c3d4e5f6a702"  # Angka Simpanan Tertukar atau Ditulis Utuh
S3 = "d4e5f6a7b803"  # Salah Meminjam pada Pengurangan
S4 = "e5f6a7b8c904"  # Strategi Memeriksa Mandiri

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Banyak anak membuat kesalahan kecil.
Kesalahan paling umum adalah lupa simpanan.
Misalnya tiga puluh tujuh tambah dua puluh lima.
Tujuh tambah lima adalah dua belas.
Tulis dua dan simpan satu puluhan.
Namun saat menghitung puluhan, satu terlupa.
Tiga tambah dua dihitung lima.
Hasilnya lima puluh dua, itu salah!
Harusnya enam puluh dua.

:::definition
title: Lupa Menyimpan
Lupa menyimpan adalah kekeliruan melewatkan angka simpanan puluhan saat berhitung.
:::"""

s2_content = """Kesalahan lain adalah angka tertukar.
Pada angka dua belas, dua satuan.
Angka satu bernilai puluhan.
Tulis dua di bawah, bukan satu.
Ada juga yang menulis dua belas utuh.
Tiga puluh tujuh tambah dua puluh lima.
Ditulis lima ratus dua belas.
Tentu saja itu sangat keliru!

:::steps
title: Mencegah Angka Tertukar
1. Periksa angka satuan yang ditulis.
2. Pastikan hanya angka puluhan yang disimpan.
3. Jangan pernah menulis dua angka bersamaan.
:::"""

s3_content = """Pengurangan juga memiliki jebakan umum.
Misalnya enam puluh dua kurang dua puluh tujuh.
Dua tidak bisa dikurang tujuh.
Banyak anak membalik menjadi tujuh kurang dua.
Itu adalah kesalahan yang besar!
Kita harus meminjam satu puluhan.
Enam dicoret menjadi lima.
Dua belas kurang tujuh jadi lima.
Lima kurang dua jadi tiga.
Jawaban benar tiga puluh lima."""

s4_content = """Bagaimana cara agar selalu teliti?
Tulis angka simpanan kecil di atas.
Coret angka puluhan yang sudah dipinjam.
Periksa hasil pengurangan dengan penjumlahan.
Jangan terburu-buru saat menghitung.
Latihan teratur membuatmu semakin hebat!

:::common_trap
title: Membalik Pengurangan Satuan
Jangan pernah membalik angka bawah mengurang atas.
Jika satuan atas kecil, wajib meminjam puluhan!
:::

:::callout
variant: summary
title: Ringkasan
text: Tulis simpanan di atas puluhan. Coret puluhan saat meminjam. Cek hasil hitungan secara mandiri.
:::"""

sections = [
    {
        "id": S1,
        "title": "Lupa Menambahkan Simpanan",
        "minutes": 6,
        "goal": "Siswa mampu mengidentifikasi dan menghindari kesalahan lupa menambahkan angka simpanan pada penjumlahan bersusun.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Angka Simpanan Tertukar atau Ditulis Utuh",
        "minutes": 6,
        "goal": "Siswa mampu mengidentifikasi kekeliruan menulis angka simpanan terbalik atau menulis dua angka sekaligus pada kolom satuan.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Salah Meminjam pada Pengurangan",
        "minutes": 6,
        "goal": "Siswa mampu menghindari jebakan membalik posisi angka satuan dan lupa mengurangi puluhan saat meminjam.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Strategi Memeriksa Mandiri",
        "minutes": 6,
        "goal": "Siswa mampu mempraktikkan strategi mencoret dan mengecek ulang jawaban dengan operasi kebalikan.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Lupa Menyimpan dan Salah Meminjam",
    "topic": "Penjumlahan dan Pengurangan sampai 100",
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
# 2. DEFINISI BANK 50 SOAL BAB 44
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
mc("c1", "mudah", D, F, S1, "Angka 1 simpanan diletakkan di atas kolom ....", ["puluhan", "satuan", "garis bawah", "tanda tambah"], "A", "Angka simpanan adalah 1 puluhan sehingga ditaruh di atas puluhan.")
tf("c1", "mudah", D, F, S3, "Pada pengurangan, jika satuan atas kecil kita boleh membalik angkanya.", "Salah", "Tidak boleh membalik angka, kita harus meminjam 1 puluhan.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Pada hasil satuan 15, angka yang disimpan ke puluhan adalah ....", ["1", "5", "15", "0"], "A", "Angka 5 ditulis pada satuan, angka 1 disimpan ke puluhan.")
mc("c1", "mudah", T, F, S4, "Saat meminjam puluhan, tanda yang berguna di buku tulis adalah ....", ["mencoret angka puluhan lama", "menghapus soal", "menebalkan angka", "memberi lingkaran besar"], "A", "Mencoret angka puluhan lama mengingatkan bahwa nilainya sudah berkurang 1.")
sa("c1", "mudah", T, F, S1, "Berapakah hasil yang benar dari 26 ditambah 18?", "44", "6 + 8 = 14 (simpan 1); 1 + 2 + 1 = 4. Hasil 44.", verifikasi={"ekspresi": "26 + 18", "hasil": "44"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Beni menghitung 38 + 25 = 53. Kesalahan yang dibuat Beni adalah ....", ["lupa menambahkan 1 puluhan simpanan", "salah menghitung 8 + 5", "mengurangkan bilangan", "tidak ada yang salah"], "A", "8 + 5 = 13; 1 + 3 + 2 = 6 puluhan. Jawabannya 63, bukan 53.", "Lupa menjumlahkan angka simpanan")
tf("c2", "mudah", D, Kn, S3, "Pada 54 - 28, angka 4 meminjam 1 puluhan sehingga menjadi 14.", "Benar", "10 + 4 = 14 satuan.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Mengapa tidak boleh menulis 13 langsung pada kolom satuan?", ["karena satu kolom hanya boleh diisi satu angka", "karena angkanya ganjil", "karena hasilnya terlalu besar", "karena tidak ada tanda"], "A", "Sistem nilai tempat hanya memuat satu angka pada tiap kolom.", "Belum paham aturan penulisan nilai tempat")
mc("c2", "mudah", R, Kn, S3, "Berapakah hasil yang benar dari 51 dikurang 26?", ["25", "35", "26", "36"], "A", "11 - 6 = 5; 4 - 2 = 2. Hasil 25.", "Salah meminjam atau lupa mengurangi puluhan", verifikasi={"ekspresi": "51 - 26", "hasil": "25"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S3, "Edo menghitung 53 - 18 dan menulis 45 karena 8 - 3 = 5. Kesalahan Edo?", ["membalik angka satuan bawah dikurang atas", "lupa meminjam puluhan", "jawaban Edo sudah benar", "salah menjumlahkan"], "A", "Edo membalik satuan bawah dikurang atas. Harusnya pinjam jadi 13 - 8 = 5.")
mc("c2", "mudah", T, Kn, S4, "Untuk memastikan 65 - 28 = 37 benar, kita bisa memeriksa dengan ....", ["37 + 28", "65 + 37", "37 - 28", "65 - 37"], "A", "37 + 28 = 65 membuktikan pengurangan benar.")
tf("c2", "mudah", T, Kn, S1, "Menjumlahkan 47 + 38 tanpa menyimpan akan menghasilkan jawaban benar.", "Salah", "7 + 8 = 15 memerlukan teknik menyimpan 1 puluhan.")
sa("c2", "mudah", T, Kn, S3, "Pada 72 - 35, setelah dipinjam 1 puluhan, angka 7 berubah jadi berapa?", "6", "7 berkurang 1 menjadi 6.")

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S1, "Berapakah hasil yang benar dari 48 ditambah 37?", ["85", "75", "86", "76"], "A", "8 + 7 = 15; 1 + 4 + 3 = 8. Jadi 85 (bukan 75).", "Lupa menambahkan simpanan", verifikasi={"ekspresi": "48 + 37", "hasil": "85"})
mc("c3", "sedang", R, Pr, S3, "Berapakah hasil yang benar dari 64 dikurang 28?", ["36", "46", "35", "44"], "A", "14 - 8 = 6; 5 - 2 = 3. Jadi 36 (bukan 46).", "Lupa mengurangi puluhan yang dipinjam", verifikasi={"ekspresi": "64 - 28", "hasil": "36"})

# Terarah (6): S1, S2, S3, S4, S1, S3 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Hitunglah dengan teliti hasil dari 29 ditambah 43!", ["72", "62", "73", "71"], "A", "9 + 3 = 12 (simpan 1); 1 + 2 + 4 = 7. Jadi 72.", verifikasi={"ekspresi": "29 + 43", "hasil": "72"})
mc("c3", "mudah", T, Pr, S3, "Hitunglah dengan teliti hasil dari 75 dikurang 39!", ["36", "46", "35", "37"], "A", "15 - 9 = 6; 6 - 3 = 3. Jadi 36.", verifikasi={"ekspresi": "75 - 39", "hasil": "36"})
tf("c3", "sedang", T, Pr, S4, "Memeriksa pengurangan dengan penjumlahan membantu menemukan kekeliruan berhitung.", "Benar", "Operasi kebalikan adalah cara efektif mengecek jawaban.")
mc("c3", "sedang", T, Pr, S2, "Rina menghitung 36 + 27 dan menulis 513. Berapa hasil yang benar?", ["63", "53", "64", "62"], "A", "6 + 7 = 13 (tulis 3 simpan 1); 1 + 3 + 2 = 6. Jadi 63.", verifikasi={"ekspresi": "36 + 27", "hasil": "63"})
tf("c3", "sedang", T, Pr, S1, "Jika 45 + 28 dijumlahkan, hasil puluhannya adalah 6.", "Salah", "1 (simpanan) + 4 + 2 = 7 puluhan, bukan 6.")
sa("c3", "sedang", T, Pr, S3, "Berapakah hasil yang benar dari 83 dikurang 47?", "36", "13 - 7 = 6; 7 - 4 = 3. Hasil 36.", verifikasi={"ekspresi": "83 - 47", "hasil": "36"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Dono menghitung 57 + 26 dan mendapat 73. Berapa hasil yang seharusnya?", ["83", "73", "84", "82"], "A", "7 + 6 = 13; 1 + 5 + 2 = 8. Seharusnya 83.", verifikasi={"ekspresi": "57 + 26", "hasil": "83"})
mc("c3", "sedang", X, Pr, S3, "Siti menghitung 81 - 45 = 44 karena menghitung 5 - 1 = 4. Jawaban benarnya?", ["36", "46", "35", "37"], "A", "11 - 5 = 6; 7 - 4 = 3. Seharusnya 36.", verifikasi={"ekspresi": "81 - 45", "hasil": "36"})
tf("c3", "sedang", X, Pr, S2, "Pada 48 + 39, angka 7 ditulis di satuan dan 1 disimpan di puluhan.", "Benar", "8 + 9 = 17, jadi tulis 7 simpan 1.")
sa("c3", "sedang", X, Pr, S4, "Periksa apakah 71 - 38 = 33 benar. Berapa hasil dari 33 + 38?", "71", "33 + 38 = 71, berarti pengurangan benar.", verifikasi={"ekspresi": "33 + 38", "hasil": "71"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Berapakah hasil yang benar dari 49 ditambah 38?", ["87", "77", "88", "86"], "A", "9 + 8 = 17; 1 + 4 + 3 = 8. Jadi 87.", verifikasi={"ekspresi": "49 + 38", "hasil": "87"})
mc("c3", "sedang", K, Pr, S3, "Berapakah hasil yang benar dari 92 dikurang 57?", ["35", "45", "34", "36"], "A", "12 - 7 = 5; 8 - 5 = 3. Jadi 35.", verifikasi={"ekspresi": "92 - 57", "hasil": "35"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S3
mc("c4", "sedang", T, Kn, S1, "Andi menghitung 68 + 24 = 82. Apa kesalahan yang paling mungkin terjadi?", ["Andi lupa menambahkan angka 1 simpanan pada puluhan", "Andi salah menjumlahkan 8 + 4", "Andi mengurangkan puluhan", "Andi menulis angka terbalik"], "A", "8 + 4 = 12; puluhan harusnya 1 + 6 + 2 = 9 (hasil 92). Andi dapat 82 karena lupa simpanan.")
mc("c4", "sedang", T, Kn, S2, "Pada 29 + 14, Riko menulis 313. Riko belum mengerti bahwa ....", ["angka 1 pada 13 harus disimpan ke nilai tempat puluhan", "angka 3 tidak boleh ditulis", "penjumlahan harus dari kiri", "29 lebih besar dari 14"], "A", "13 terdiri dari 1 puluhan dan 3 satuan. 1 puluhan harus disimpan.")
tf("c4", "sedang", T, Kn, S3, "Pada 80 - 36, satuan 0 meminjam 1 puluhan sehingga menjadi 10.", "Benar", "10 + 0 = 10.")
tf("c4", "sedang", T, Kn, S4, "Jika hasil pemeriksaan penjumlahan berbeda dari bilangan semula, jawaban kita sudah benar.", "Salah", "Jika berbeda, berarti ada kekeliruan pada hitungan kita.")
sa("c4", "sedang", T, Kn, S4, "Hitunglah 85 dikurang 48 dengan teliti dan benar!", "37", "15 - 8 = 7; 7 - 4 = 3. Hasil 37.", verifikasi={"ekspresi": "85 - 48", "hasil": "37"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S3, "Mengapa siswa sering salah menghitung 70 - 34 menjadi 44?", ["karena membalik satuan menjadi 4 - 0 = 4 dan tidak meminjam", "karena salah membaca angka", "karena menjumlahkan 70 + 34", "karena lupa tanda kurang"], "A", "Siswa keliru membalik 4 - 0 = 4. Harusnya 10 - 4 = 6 dan 6 - 3 = 3 (hasil 36).")
mc("c4", "sedang", X, Kn, S4, "Budi menghitung 62 - 27 = 45. Budi mengecek 45 + 27 = 72. Budi tahu bahwa ....", ["jawabannya salah karena hasil pengecekan bukan 62", "jawabannya sudah benar", "soalnya yang keliru", "alat tulisnya rusak"], "A", "Hasil pengecekan 72 berbeda dari 62, membuktikan jawaban 45 salah.")
tf("c4", "sedang", X, Kn, S1, "Lupa simpanan pada penjumlahan bersusun menyebabkan jawaban kurang 10 dari yang benar.", "Benar", "Karena 1 puluhan (bernilai 10) tidak ikut ditambahkan.")
mc("c4", "sulit", X, Me, S3, "Berapakah hasil yang benar dari 91 dikurang 56?", ["35", "45", "34", "36"], "A", "11 - 6 = 5; 8 - 5 = 3. Hasil 35.", verifikasi={"ekspresi": "91 - 56", "hasil": "35"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Pada penjumlahan 58 + 27, langkah nilai tempat yang tepat adalah ....", ["tulis 5 di satuan dan simpan 1 di puluhan", "tulis 15 di satuan", "tulis 1 di satuan", "simpan 5 di puluhan"], "A", "8 + 7 = 15; tulis 5 pada satuan, simpan 1 puluhan.")
mc("c4", "sulit", K, Me, S3, "Sebuah toko punya 84 telur, terjual 49 butir. Berapa sisa telur yang benar?", ["35 butir", "45 butir", "34 butir", "36 butir"], "A", "14 - 9 = 5; 7 - 4 = 3. Jadi 35 butir.", verifikasi={"ekspresi": "84 - 49", "hasil": "35"})
tf("c4", "sulit", K, Me, S4, "Mencoret angka puluhan yang dipinjam justru membuat hitungan membingungkan dan salah.", "Salah", "Mencoret adalah cara visual efektif mengingat puluhan berkurang 1.")
mc("c4", "sulit", K, Me, S4, "Lina punya 93 pita, dipakai 48 pita. Berapa sisa pita Lina yang benar?", ["45 pita", "55 pita", "44 pita", "46 pita"], "A", "13 - 8 = 5; 8 - 4 = 4. Hasil 45 pita.", verifikasi={"ekspresi": "93 - 48", "hasil": "45"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Perbaiki kesalahan hitung ini: 46 + 38 = 74. Jawaban yang tepat adalah ....", ["84", "74", "85", "83"], "A", "6 + 8 = 14; 1 + 4 + 3 = 8 puluhan. Jawaban tepat 84.", verifikasi={"ekspresi": "46 + 38", "hasil": "84"})
mc("c5", "sedang", T, Me, S2, "Di antara penjumlahan berikut, mana yang membutuhkan teknik menyimpan?", ["47 + 25", "42 + 23", "51 + 24", "60 + 15"], "A", "7 + 5 = 12 memerlukan teknik menyimpan 1 puluhan.")
mc("c5", "sedang", T, Me, S3, "Perbaiki kesalahan hitung ini: 82 - 37 = 55. Jawaban yang tepat adalah ....", ["45", "55", "46", "44"], "A", "12 - 7 = 5; 7 - 3 = 4. Jawaban tepat 45.", verifikasi={"ekspresi": "82 - 37", "hasil": "45"})
mc("c5", "sulit", T, Me, S4, "Pak Dani panen 95 mangga, busuk 48 mangga. Berapa mangga yang masih bagus?", ["47 mangga", "57 mangga", "46 mangga", "48 mangga"], "A", "15 - 8 = 7; 8 - 4 = 4. Jadi 47 mangga.", verifikasi={"ekspresi": "95 - 48", "hasil": "47"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Di antara pengurangan berikut, mana yang membutuhkan teknik meminjam?", ["72 - 38", "78 - 32", "65 - 21", "89 - 44"], "A", "2 lebih kecil dari 8 sehingga 72 - 38 butuh meminjam.")
mc("c5", "sulit", K, Me, S4, "Pak Lurah punya 100 bibit tanaman, dibagikan 57 bibit. Berapa sisa bibit?", ["43 bibit", "53 bibit", "42 bibit", "44 bibit"], "A", "100 - 57 = 43 bibit.", verifikasi={"ekspresi": "100 - 57", "hasil": "43"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Edo sering lupa menambahkan angka simpanan. Apa nasihat terbaik untuk Edo?", ["tuliskan angka 1 simpanan dengan jelas di atas kolom puluhan", "hitung lebih cepat tanpa coretan", "jangan gunakan penjumlahan bersusun", "hitung dari puluhan dulu"], "A", "Menulis angka 1 di atas kolom puluhan adalah pengingat visual terbaik.")
mc("c6", "sulit", K, Me, S3, "Mengapa kita tidak boleh membalik pengurangan satuan saat angka atas lebih kecil?", ["karena nilai bilangan atas yang dikurangi bukan sebaliknya", "karena dilarang guru", "karena hasilnya selalu nol", "karena angkanya jadi genap"], "A", "Pengurangan tidak bersifat komutatif; bilangan atas adalah jumlah awal yang dikurangi.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Temukan kesalahan pada hitungan: 90 - 43 = 57. Bagaimana pembetulannya?", ["satuan 10 - 3 = 7 puluhan 8 - 4 = 4 jawaban benar 47", "jawaban 57 sudah benar", "seharusnya 90 + 43", "satuan harusnya 0"], "A", "9 berkurang 1 menjadi 8, sehingga 8 - 4 = 4. Hasil benar 47.")
mc("c6", "sulit", P, Me, S4, "Selesaikan operasi campuran dengan teliti: 48 + 37 - 29!", ["56", "46", "57", "55"], "A", "48 + 37 = 85; 85 - 29 = 56.", verifikasi={"ekspresi": "48 + 37 - 29", "hasil": "56"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab44_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab44.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
