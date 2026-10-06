#!/usr/bin/env python3
"""
Generator dan validator Bab 33 Matematika Kelas 1 SD:
"Mengumpulkan dan Menghitung Data Sederhana" (Fase A)
bab_id: e59718a7-b595-42dc-ac3a-f7bee217f110
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "d1e2f34a5b01"  # Apa Itu Data Sederhana
S2 = "e2f3a45b6c12"  # Cara Bertanya dan Mengumpulkan Data
S3 = "f3a4b56c7d23"  # Mencatat Data dengan Tanda Turus
S4 = "a4b5c67d8e34"  # Menghitung Total Hasil Pengumpulan Data

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Pernahkah kamu menghitung buah apel?
Atau buah kesukaan teman sekelasmu?
Catatan keterangan itu dinamakan data.
Data berisi fakta yang benar.
Data memberi kita informasi jelas.
Kita tahu buah yang disukai.
Kita tahu warna kesukaan teman.
Semua tersimpan rapi dalam catatan.

:::definition
title: Data Sederhana
Data adalah catatan keterangan tentang fakta di sekitar kita.
:::"""

s2_content = """Bagaimana cara kita mengumpulkan data?
Kita bisa bertanya langsung ramah.
Tanyakan satu per satu temanmu.
Siti suka buah jeruk manis.
Beni suka buah pisang kuning.
Edo suka buah apel merah.
Setiap jawaban dicatat dengan teliti.
Jangan sampai ada yang terlewat.

:::steps
title: Mengumpulkan Data Teman
1. Siapkan kertas dan pensil catatanmu.
2. Bertanyalah dengan sopan satu kali.
3. Tulis jawaban teman dengan teliti.
:::"""

s3_content = """Mari belajar memakai tanda turus.
Satu benda diberi garis tegak.
Dua benda diberi dua garis.
Tiga dan empat juga sama.
Garis kelima dicoret miring mengikat.
Satu ikat turus berjumlah lima.
Menghitung kelipatan lima sangat cepat.
Catatan menjadi rapi dan jelas."""

s4_content = """Sekarang mari hitung total datanya.
Ada lima teman suka jeruk.
Ada tiga teman suka pisang.
Ada empat teman suka apel.
Jumlahkan semua coretan garis tadi.
Total seluruh teman ada dua belas.

:::common_trap
title: Menghitung Data Satu per Satu
Setiap orang hanya menjawab satu kali.
Jangan mencatat jawaban teman ganda.
Tanda turus dicoret satu per satu.
Coretan kelima miring mengikat seikat lima.
Hitunglah dengan teliti dan jujur.
:::

:::callout
variant: summary
title: Ringkasan
text: Data adalah catatan keterangan benda. Kita bisa bertanya dan mencatat memakai tanda turus.
:::"""

sections = [
    {
        "id": S1,
        "title": "Apa Itu Data Sederhana",
        "minutes": 6,
        "goal": "Siswa memahami pengertian data sederhana sebagai catatan keterangan fakta di lingkungan sekitar.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Cara Bertanya dan Mengumpulkan Data",
        "minutes": 6,
        "goal": "Siswa memahami teknik sederhana mengumpulkan data melalui wawancara dan pengamatan langsung.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Mencatat Data dengan Tanda Turus",
        "minutes": 6,
        "goal": "Siswa terampil mencatat data menggunakan simbol turus (tally marks) dengan ikatan lima.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menghitung Total Hasil Pengumpulan Data",
        "minutes": 6,
        "goal": "Siswa dapat menjumlahkan dan menyimpulkan total hasil pengumpulan data sederhana.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengumpulkan dan Menghitung Data Sederhana",
    "topic": "Diagram dan Piktogram",
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
# 2. DEFINISI BANK 50 SOAL BAB 33
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
mc("c1", "mudah", D, F, S1, "Catatan keterangan tentang fakta yang dikumpulkan disebut ....", ["data", "dongeng", "pantun", "khayalan"], "A", "Data adalah catatan keterangan tentang fakta nyata.")
tf("c1", "mudah", D, F, S3, "Satu ikat tanda turus lengkap terdiri dari 5 garis.", "Benar", "Empat garis tegak diikat satu garis miring berjumlah 5.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Cara mengumpulkan data kesukaan teman di kelas adalah dengan ....", ["bertanya langsung sopan", "menebak sendiri", "mengarang jawaban", "pura-pura tahu"], "A", "Bertanya langsung menghasilkan data yang jujur dan benar.")
mc("c1", "mudah", T, F, S3, "Tiga buah buku diwakili dengan tanda turus sebanyak .... garis tegak.", ["3 garis", "2 garis", "4 garis", "5 garis"], "A", "Tiap satu benda diwakili satu garis turus tegak.", verifikasi={"ekspresi": "3", "hasil": "3"})
sa("c1", "mudah", T, F, S4, "Ada 2 teman suka apel dan 3 suka jeruk. Berapa total teman?", "5", "2 + 3 = 5 teman.", verifikasi={"ekspresi": "2 + 3", "hasil": "5"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Saat mencatat buah kesukaan, setiap teman ditanya sebanyak ....", ["satu kali", "tiga kali", "sepuluh kali", "bebas terserah"], "A", "Tiap orang menjawab satu kali agar data tidak ganda.", "Mencatat jawaban orang yang sama berulang kali")
tf("c2", "mudah", D, Kn, S4, "Menghitung data turus dengan seikat lima lebih lambat daripada menghitung satu-satu.", "Salah", "Ikatan lima mempermudah menghitung kelipatan 5 dengan cepat.")

# Remedial (2)
mc("c2", "mudah", R, F, S3, "Berapakah jumlah garis pada tanda turus empat garis tegak dan satu garis miring?", ["5 garis", "4 garis", "6 garis", "3 garis"], "A", "4 tegak + 1 miring = 5 garis.", "Belum paham ikatan turus berjumlah 5", verifikasi={"ekspresi": "4 + 1", "hasil": "5"})
mc("c2", "mudah", R, Kn, S1, "Mengapa kita mengumpulkan data buah kesukaan teman?", ["agar tahu buah apa yang paling disukai teman sekelas", "agar teman marah", "agar tugas makin sulit", "untuk disembunyikan"], "A", "Data membantu kita memperoleh informasi yang jelas.", "Belum memahami manfaat mengumpulkan data")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Ada 4 data mobil merah dan 3 data mobil biru. Total mobil?", ["7 mobil", "6 mobil", "8 mobil", "5 mobil"], "A", "4 + 3 = 7 mobil.", verifikasi={"ekspresi": "4 + 3", "hasil": "7"})
mc("c2", "mudah", T, Kn, S2, "Di kelas ada 5 teman suka susu dan 4 suka jus. Total teman?", ["9 teman", "8 teman", "10 teman", "7 teman"], "A", "5 + 4 = 9 teman.", verifikasi={"ekspresi": "5 + 4", "hasil": "9"})
tf("c2", "mudah", T, Kn, S3, "Dua ikat tanda turus bernilai 10 benda.", "Benar", "5 + 5 = 10 benda.")
sa("c2", "mudah", T, Kn, S4, "Tiga teman suka kucing, 5 suka kelinci. Berapa selisih banyaknya peminat?", "2", "5 - 3 = 2 peminat.", verifikasi={"ekspresi": "5 - 3", "hasil": "2"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Ada 8 ekor burung. Berapa ikat lima dan sisa garis turusnya?", ["1 ikat lima dan 3 garis", "2 ikat lima", "1 ikat lima dan 2 garis", "8 garis miring semua"], "A", "8 = 5 (1 ikat) + 3 garis lepas.", "Keliru menuliskan turus untuk bilangan di atas 5")
mc("c3", "sedang", R, Pr, S4, "Data warna: 6 merah dan 3 biru. Berapa selisihnya?", ["3 warna", "2 warna", "4 warna", "1 warna"], "A", "6 - 3 = 3.", "Keliru menghitung selisih data", verifikasi={"ekspresi": "6 - 3", "hasil": "3"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Data pensil ada 5 buah, penghapus ada 4 buah. Total alat tulis?", ["9 buah", "8 buah", "10 buah", "7 buah"], "A", "5 + 4 = 9 buah.", verifikasi={"ekspresi": "5 + 4", "hasil": "9"})
mc("c3", "sedang", T, Pr, S2, "Siti bertanya pada 10 teman. 6 anak menjawab suka bakso. Sisanya suka mi ayam?", ["4 anak", "3 anak", "5 anak", "2 anak"], "A", "10 - 6 = 4 anak.", verifikasi={"ekspresi": "10 - 6", "hasil": "4"})
tf("c3", "sedang", T, Pr, S3, "Sebanyak 7 garis turus ditulis sebagai 1 ikat lima dan 2 garis tegak.", "Benar", "5 + 2 = 7 garis.")
mc("c3", "sedang", T, Pr, S4, "Data mainan: 7 bola, 4 boneka, dan 2 robot. Total mainan?", ["13 mainan", "12 mainan", "14 mainan", "11 mainan"], "A", "7 + 4 + 2 = 13 mainan.", verifikasi={"ekspresi": "7 + 4 + 2", "hasil": "13"})
tf("c3", "sedang", T, Pr, S1, "Data yang kita buat boleh dikarang sendiri tanpa bertanya atau mengamati.", "Salah", "Data harus memuat fakta nyata yang sebenarnya.")
sa("c3", "mudah", T, Pr, S3, "Ada 2 ikat turus lima dan 3 garis lepas. Berapa total nilainya?", "13", "5 + 5 + 3 = 13.", verifikasi={"ekspresi": "5 + 5 + 3", "hasil": "13"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Edo mencatat 8 sepeda dan 6 motor di jalan. Berapa total kendaraan?", ["14 kendaraan", "13 kendaraan", "15 kendaraan", "12 kendaraan"], "A", "8 + 6 = 14 kendaraan.", verifikasi={"ekspresi": "8 + 6", "hasil": "14"})
mc("c3", "sedang", X, Pr, S2, "Lani menanyai 12 teman. 7 teman suka mangga. Berapa teman suka buah lain?", ["5 teman", "4 teman", "6 teman", "3 teman"], "A", "12 - 7 = 5 teman.", verifikasi={"ekspresi": "12 - 7", "hasil": "5"})
tf("c3", "sedang", X, Pr, S3, "Satu ikat turus lima ditambah 4 garis bernilai 9 benda.", "Benar", "5 + 4 = 9 benda.")
sa("c3", "sedang", X, Pr, S4, "Ada 9 teman suka membaca dan 5 suka melukis. Selisih teman?", "4", "9 - 5 = 4 teman.", verifikasi={"ekspresi": "9 - 5", "hasil": "4"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Data bunga: 8 mawar merah dan 7 melati putih. Berapa total bunga?", ["15 bunga", "14 bunga", "16 bunga", "13 bunga"], "A", "8 + 7 = 15 bunga.", verifikasi={"ekspresi": "8 + 7", "hasil": "15"})
mc("c3", "sedang", K, Pr, S4, "Data hewan: 16 ikan di kolam. 7 ikan diambil. Berapa sisa ikan?", ["9 ikan", "8 ikan", "10 ikan", "7 ikan"], "A", "16 - 7 = 9 ikan.", verifikasi={"ekspresi": "16 - 7", "hasil": "9"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Mengapa tanda turus dikelompokkan tiap 5 garis dengan coretan miring?", ["agar mata kita mudah dan cepat menghitung kelipatan lima", "agar kertasnya cepat penuh", "agar gambar tampak bagus", "agar garisnya tidak terbang"], "A", "Pengelompokan lima mempermudah pembacaan jumlah secara cepat.")
mc("c4", "sedang", T, Kn, S2, "Jika ada teman yang menjawab dua kali buah kesukaannya, apa yang harus dilakukan?", ["mencatatnya satu kali saja", "mencatat dua-duanya berkali-kali", "menghukum teman itu", "merobek buku catatan"], "A", "Satu orang hanya boleh menyumbang satu pilihan data.")
tf("c4", "sedang", T, Kn, S3, "Tiga ikat turus lima memiliki nilai yang sama dengan 15 garis tegak.", "Benar", "3 x 5 = 15.")
tf("c4", "sedang", T, Kn, S4, "Data buah kesukaan teman paling banyak selalu memiliki nilai angka paling kecil.", "Salah", "Pilihan yang paling disukai memiliki nilai angka terbanyak.")
sa("c4", "sedang", T, Kn, S4, "Ada 18 teman di kelas. 9 teman suka renang. Berapa teman tidak suka renang?", "9", "18 - 9 = 9 teman.", verifikasi={"ekspresi": "18 - 9", "hasil": "9"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Berdasarkan data: apel 8 buah, jeruk 5 buah, pisang 3 buah. Buah paling disukai?", ["apel", "jeruk", "pisang", "semua sama"], "A", "Apel memiliki jumlah terbanyak yaitu 8 buah.")
mc("c4", "sedang", X, Kn, S2, "Udin mencatat 15 burung: 6 gereja, 4 merpati, sisanya pipit. Berapa burung pipit?", ["5 pipit", "4 pipit", "6 pipit", "3 pipit"], "A", "15 - (6 + 4) = 5 burung.", verifikasi={"ekspresi": "15 - (6 + 4)", "hasil": "5"})
tf("c4", "sedang", X, Kn, S3, "Sebanyak 12 data dicatat sebagai satu ikat lima dan 2 garis lepas.", "Salah", "12 data adalah 2 ikat lima dan 2 garis lepas.")
mc("c4", "sulit", X, Me, S4, "Data susu: cokelat 9 kotak, putih 7 kotak. Berapa selisih kedua susu?", ["2 kotak", "1 kotak", "3 kotak", "4 kotak"], "A", "9 - 7 = 2 kotak.", verifikasi={"ekspresi": "9 - 7", "hasil": "2"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Langkah pertama yang paling tepat saat ingin mengumpulkan data hobi teman adalah ....", ["membuat daftar hobi lalu bertanya satu per satu", "langsung menebak hobi teman", "menyalin tugas teman lain", "mengarang data sesuka hati"], "A", "Menyiapkan daftar pertanyaan lalu bertanya satu per satu secara teratur.")
mc("c4", "sulit", K, Me, S3, "Tiga ikat turus lima ditambah 3 garis. Berapa nilai yang diperoleh?", ["18 nilai", "17 nilai", "19 nilai", "16 nilai"], "A", "(3 x 5) + 3 = 15 + 3 = 18.", verifikasi={"ekspresi": "3 * 5 + 3", "hasil": "18"})
tf("c4", "sulit", K, Me, S4, "Jika apel disukai 10 anak dan jeruk 4 anak, jeruk lebih disukai daripada apel.", "Salah", "10 anak pada apel lebih banyak daripada 4 anak pada jeruk.")
mc("c4", "sulit", K, Me, S4, "Data pensil: merah 7, biru 6, hijau 5. Berapa total pensil ketiga warna?", ["18 pensil", "17 pensil", "19 pensil", "16 pensil"], "A", "7 + 6 + 5 = 18 pensil.", verifikasi={"ekspresi": "7 + 6 + 5", "hasil": "18"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Data buku cerita: fabel 8 buku, komik 7 buku. Total buku cerita?", ["15 buku", "14 buku", "16 buku", "13 buku"], "A", "8 + 7 = 15 buku.", verifikasi={"ekspresi": "8 + 7", "hasil": "15"})
mc("c5", "sedang", T, Me, S2, "Ada 20 siswa di kelas. 8 suka lari, 6 suka lompat. Berapa suka senam?", ["6 siswa", "5 siswa", "7 siswa", "4 siswa"], "A", "20 - (8 + 6) = 20 - 14 = 6 siswa.", verifikasi={"ekspresi": "20 - (8 + 6)", "hasil": "6"})
mc("c5", "sedang", T, Me, S3, "Empat ikat turus lima. Berapa total seluruh data yang terkumpul?", ["20 data", "18 data", "22 data", "16 data"], "A", "4 x 5 = 20 data.", verifikasi={"ekspresi": "4 * 5", "hasil": "20"})
mc("c5", "sulit", T, Me, S4, "Data bola: basket 6, voli 5, kasti 4. Berapa total seluruh bola olahraga?", ["15 bola", "14 bola", "16 bola", "13 bola"], "A", "6 + 5 + 4 = 15 bola.", verifikasi={"ekspresi": "6 + 5 + 4", "hasil": "15"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Ada 2 ikat turus lima dan 4 garis lepas. Berapa total nilainya?", ["14 data", "13 data", "15 data", "12 data"], "A", "10 + 4 = 14 data.", verifikasi={"ekspresi": "2 * 5 + 4", "hasil": "14"})
mc("c5", "sulit", K, Me, S4, "Data buah: mangga 9, jeruk 5. Berapa selisih mangga dengan jeruk?", ["4 buah", "3 buah", "5 buah", "2 buah"], "A", "9 - 5 = 4 buah.", verifikasi={"ekspresi": "9 - 5", "hasil": "4"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Bagaimana cara menyajikan laporan data buah kesukaan kelas secara jelas dan rapi?", ["menuliskan nama buah, tanda turus ikat lima, dan total angka di tabel", "menggambar coret-coretan abstrak di dinding sekolah", "menyobek kertas hasil catatan wawancara teman", "mengingat semuanya di dalam kepala tanpa mencatat"], "A", "Menyajikan nama buah, turus ikatan lima, dan angka dalam tabel rapi.")
mc("c6", "sulit", K, Me, S4, "Jika ada 16 suara: pilihan A dapat 9 suara, sisanya pilihan B. Pemenangnya?", ["pilihan A menang karena unggul 2 suara", "pilihan B menang", "keduanya seri", "tidak ada yang menang"], "A", "B = 16 - 9 = 7 suara. Pilihan A menang dengan 9 suara (unggul 2 suara).")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Data 22 anak dicatat turus. Berapa ikat lima dan garis lepas yang terbentuk?", ["4 ikat lima dan 2 garis lepas", "3 ikat lima dan 7 garis", "5 ikat lima", "2 ikat lima dan 12 garis"], "A", "22 = (4 x 5) + 2 = 4 ikat lima dan 2 garis lepas.")
mc("c6", "sulit", P, Me, S4, "Kelompok A mengumpulkan 14 data, kelompok B mengumpulkan 7 data. Berapa total keduanya?", ["21 data", "20 data", "22 data", "19 data"], "A", "14 + 7 = 21 data.", verifikasi={"ekspresi": "14 + 7", "hasil": "21"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab33_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab33.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
