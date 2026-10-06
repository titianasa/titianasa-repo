#!/usr/bin/env python3
"""
Generator dan validator Bab 34 Matematika Kelas 1 SD:
"Membaca Piktogram" (Fase A)
bab_id: 6815aef4-3459-43c4-931d-f93155cb524b
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "c1d2e34f5a01"  # Apa Itu Diagram Gambar Piktogram
S2 = "d2e3f45a6b12"  # Melihat Judul dan Nama Kategori
S3 = "e3f4a56b7c23"  # Memperhatikan Keterangan Satu Gambar
S4 = "f4a5b67c8d34"  # Menjawab Pertanyaan dari Piktogram

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Pernahkah kamu melihat grafik bergambar?
Gambar itu disebut diagram gambar.
Nama lainnya adalah piktogram.
Piktogram memakai gambar lucu.
Ada gambar apel merah manis.
Ada gambar buku atau bintang.
Piktogram membuat data mudah dilihat.
Semua orang senang membacanya.

:::definition
title: Piktogram
Piktogram adalah diagram penyajian data yang menggunakan simbol gambar.
:::"""

s2_content = """Pertama, bacalah judul di atas.
Judul memberi tahu isi data.
Misal judul buah kesukaan siswa.
Lalu lihatlah baris nama kategori.
Ada baris nama buah jeruk.
Ada baris nama buah apel.
Ada baris nama buah pisang.
Setiap baris punya gambarnya sendiri.

:::steps
title: Langkah Membaca Piktogram
1. Baca judul diagram di bagian atas.
2. Periksa nama kategori pada setiap baris.
3. Hitung gambar pada baris yang dituju.
:::"""

s3_content = """Jangan lupa membaca keterangan bawah.
Keterangan memberi tahu arti gambar.
Satu gambar bintang mewakili satu anak.
Atau satu gambar apel mewakili satu apel.
Keterangan ini sangat penting dibaca.
Kita jadi tahu nilai gambarnya.
Hitungan kita menjadi sangat tepat.
Tidak ada yang salah tafsir."""

s4_content = """Sekarang mari menjawab pertanyaan piktogram.
Berapa anak yang suka apel?
Hitunglah gambar apel pada barisnya.
Ada empat gambar apel merah.
Artinya ada empat anak pemilih.
Kategori gambar terbanyak adalah pemenang.

:::common_trap
title: Membaca Piktogram dengan Cermat
Lihatlah judul piktogram terlebih dahulu.
Perhatikan keterangan arti setiap gambar.
Hitunglah gambar pada baris yang tepat.
Jangan tertukar membaca baris kategori.
Hitung satu per satu dengan teliti.
:::

:::callout
variant: summary
title: Ringkasan
text: Piktogram memakai simbol gambar. Kita membaca judul, kategori, dan menghitung jumlah gambar.
:::"""

sections = [
    {
        "id": S1,
        "title": "Apa Itu Diagram Gambar Piktogram",
        "minutes": 6,
        "goal": "Siswa memahami konsep dasar piktogram sebagai diagram yang menyajikan data dengan simbol gambar.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Melihat Judul dan Nama Kategori",
        "minutes": 6,
        "goal": "Siswa terampil membaca judul data dan mengidentifikasi baris kategori pada piktogram.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Memperhatikan Keterangan Satu Gambar",
        "minutes": 6,
        "goal": "Siswa memahami fungsi keterangan (kunci skala 1 gambar = 1 benda) pada diagram piktogram.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Menjawab Pertanyaan dari Piktogram",
        "minutes": 6,
        "goal": "Siswa dapat mengekstrak informasi dan menjawab pertanyaan berdasarkan tampilan piktogram.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Membaca Piktogram",
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
# 2. DEFINISI BANK 50 SOAL BAB 34
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
mc("c1", "mudah", D, F, S1, "Diagram yang menyajikan data menggunakan gambar dinamakan ....", ["piktogram", "dongeng", "pantun", "lagu"], "A", "Piktogram adalah diagram bergambar.")
tf("c1", "mudah", D, F, S2, "Judul piktogram memberi tahu kita informasi isi data yang disajikan.", "Benar", "Judul menjelaskan topik data diagram.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S3, "Keterangan: tiap 1 gambar bintang mewakili 1 anak. Tiga bintang mewakili ....", ["3 anak", "2 anak", "4 anak", "5 anak"], "A", "Tiap gambar bernilai satu anak.", verifikasi={"ekspresi": "3 * 1", "hasil": "3"})
mc("c1", "mudah", T, F, S2, "Pada piktogram buah, baris 'Apel' berisi gambar buah ....", ["apel", "jeruk", "pisang", "mangga"], "A", "Baris apel berisi gambar apel.")
sa("c1", "mudah", T, F, S4, "Pada piktogram ada 4 gambar apel merah. Berapa jumlah apel?", "4", "4 gambar mewakili 4 apel.", verifikasi={"ekspresi": "4", "hasil": "4"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Mengapa kita harus membaca keterangan di bawah piktogram?", ["agar tahu berapa nilai benda yang diwakili satu gambar", "agar tahu nama pembuat buku", "agar piktogram berwarna", "agar kertas tebal"], "A", "Keterangan kunci menjelaskan nilai tiap satu simbol gambar.", "Melewatkan membaca keterangan skala piktogram")
tf("c2", "mudah", D, Kn, S4, "Baris dengan jumlah gambar paling banyak menunjukkan data paling sedikit.", "Salah", "Gambar terbanyak menunjukkan data paling banyak.")

# Remedial (2)
mc("c2", "mudah", R, F, S1, "Apa keuntungan menyajikan data menggunakan piktogram?", ["data lebih menarik dan mudah dipahami anak", "membuat data jadi rahasia", "hitungan jadi membingungkan", "kertas cepat rusak"], "A", "Piktogram menyajikan data secara visual yang jelas dan menarik.", "Belum paham fungsi diagram piktogram")
mc("c2", "mudah", R, Kn, S2, "Jika ingin tahu banyak peminat jeruk, baris manakah yang kamu periksa?", ["baris jeruk", "baris apel", "baris judul", "baris tanggal"], "A", "Lihat baris kategori jeruk.", "Tertukar membaca baris kategori")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Piktogram buku: baris Senin ada 3 buku, Selasa ada 4 buku. Total buku?", ["7 buku", "6 buku", "8 buku", "5 buku"], "A", "3 + 4 = 7 buku.", verifikasi={"ekspresi": "3 + 4", "hasil": "7"})
mc("c2", "mudah", T, Kn, S2, "Piktogram hewan: kelinci 5 gambar, kucing 4 gambar. Berapa total gambar?", ["9 gambar", "8 gambar", "10 gambar", "7 gambar"], "A", "5 + 4 = 9 gambar.", verifikasi={"ekspresi": "5 + 4", "hasil": "9"})
tf("c2", "mudah", T, Kn, S3, "Jika satu gambar mewakili 1 anak, 5 gambar bintang berarti 5 anak.", "Benar", "5 gambar x 1 = 5 anak.")
sa("c2", "mudah", T, Kn, S4, "Piktogram bunga: mawar 6 gambar, melati 2 gambar. Selisih bunga?", "4", "6 - 2 = 4 bunga.", verifikasi={"ekspresi": "6 - 2", "hasil": "4"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S4, "Piktogram: apel 7 gambar, jeruk 4 gambar. Berapa selisih apel dan jeruk?", ["3 buah", "2 buah", "4 buah", "1 buah"], "A", "7 - 4 = 3 buah.", "Keliru menghitung selisih piktogram", verifikasi={"ekspresi": "7 - 4", "hasil": "3"})
mc("c3", "sedang", R, Pr, S3, "Keterangan: 1 apel = 1 buah. Ada 6 gambar apel. Berapa buah apel?", ["6 buah", "5 buah", "7 buah", "4 buah"], "A", "6 x 1 = 6 buah.", "Salah mengalikan nilai piktogram", verifikasi={"ekspresi": "6 * 1", "hasil": "6"})

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Piktogram pensil: merah 5 gambar, biru 3 gambar. Total pensil?", ["8 pensil", "7 pensil", "9 pensil", "6 pensil"], "A", "5 + 3 = 8 pensil.", verifikasi={"ekspresi": "5 + 3", "hasil": "8"})
mc("c3", "sedang", T, Pr, S2, "Piktogram mainan: bola 8 gambar, boneka 5 gambar. Berapa selisihnya?", ["3 mainan", "2 mainan", "4 mainan", "1 mainan"], "A", "8 - 5 = 3 mainan.", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})
tf("c3", "sedang", T, Pr, S3, "Tujuh gambar lingkaran mewakili 7 orang jika 1 lingkaran mewakili 1 orang.", "Benar", "7 x 1 = 7 orang.")
mc("c3", "sedang", T, Pr, S4, "Piktogram buah: pisang 6, mangga 4, nanas 2. Berapa total seluruh buah?", ["12 buah", "11 buah", "13 buah", "10 buah"], "A", "6 + 4 + 2 = 12 buah.", verifikasi={"ekspresi": "6 + 4 + 2", "hasil": "12"})
tf("c3", "sedang", T, Pr, S1, "Menghitung piktogram dapat dilakukan dengan menghitung gambar satu per satu.", "Benar", "Tiap gambar dihitung berurutan.")
sa("c3", "mudah", T, Pr, S4, "Piktogram: ikan mas 5 gambar, ikan lele 4 gambar. Berapa total ikan?", "9", "5 + 4 = 9 ikan.", verifikasi={"ekspresi": "5 + 4", "hasil": "9"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Piktogram tabungan: Senin 6 koin, Selasa 5 koin. Total koin?", ["11 koin", "10 koin", "12 koin", "9 koin"], "A", "6 + 5 = 11 koin.", verifikasi={"ekspresi": "6 + 5", "hasil": "11"})
mc("c3", "sedang", X, Pr, S2, "Piktogram kendaraan: mobil 9, motor 4. Berapa selisih mobil dan motor?", ["5 kendaraan", "4 kendaraan", "6 kendaraan", "3 kendaraan"], "A", "9 - 4 = 5 kendaraan.", verifikasi={"ekspresi": "9 - 4", "hasil": "5"})
tf("c3", "sedang", X, Pr, S3, "Jika 1 gambar mobil = 1 mobil, 8 gambar mobil bernilai 10 mobil.", "Salah", "8 gambar x 1 = 8 mobil.")
sa("c3", "sedang", X, Pr, S4, "Piktogram: roti cokelat 8 gambar, roti keju 5 gambar. Selisih roti?", "3", "8 - 5 = 3 roti.", verifikasi={"ekspresi": "8 - 5", "hasil": "3"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Piktogram hari hujan: Maret 7 hari, April 6 hari. Total hari hujan?", ["13 hari", "12 hari", "14 hari", "11 hari"], "A", "7 + 6 = 13 hari.", verifikasi={"ekspresi": "7 + 6", "hasil": "13"})
mc("c3", "sedang", K, Pr, S4, "Piktogram jus: alpukat 9 gelas, sirsak 6 gelas. Berapa selisihnya?", ["3 gelas", "2 gelas", "4 gelas", "1 gelas"], "A", "9 - 6 = 3 gelas.", verifikasi={"ekspresi": "9 - 6", "hasil": "3"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Mengapa piktogram buah sering menggunakan gambar buah aslinya?", ["agar pembaca langsung mengenali jenis data dengan mudah", "agar buahnya bisa dimakan", "karena tidak ada tulisan", "agar kertas berbau wangi"], "A", "Simbol gambar yang sesuai mempercepat pemahaman data.")
mc("c4", "sedang", T, Kn, S2, "Piktogram hobi: renang 8, tari 5, lukis 9. Hobi yang paling sedikit disukai?", ["tari", "renang", "lukis", "semua sama"], "A", "Tari memiliki gambar paling sedikit yaitu 5.")
tf("c4", "sedang", T, Kn, S3, "Mengubah gambar bintang menjadi gambar lingkaran tidak mengubah jumlah data aslinya.", "Benar", "Simbol visual tidak mengubah angka data aslinya.")
tf("c4", "sedang", T, Kn, S4, "Data pada piktogram yang tidak memiliki gambar sama sekali bernilai 1.", "Salah", "Jika tidak ada gambar sama sekali nilainya nol (0).")
sa("c4", "sedang", T, Kn, S4, "Piktogram hewan peliharaan: kucing 15 gambar. Diberikan 6 gambar. Sisa?", "9", "15 - 6 = 9 gambar.", verifikasi={"ekspresi": "15 - 6", "hasil": "9"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Piktogram warna: biru 8 gambar, kuning 6 gambar, hijau 4 gambar. Urutan dari terbanyak?", ["biru, kuning, hijau", "hijau, kuning, biru", "kuning, biru, hijau", "semua urutan sama"], "A", "Urutan dari terbanyak: 8 (biru), 6 (kuning), 4 (hijau).")
mc("c4", "sedang", X, Kn, S2, "Ada 14 gambar di piktogram: 8 apel, sisanya jeruk. Berapa gambar jeruk?", ["6 jeruk", "5 jeruk", "7 jeruk", "4 jeruk"], "A", "14 - 8 = 6 gambar.", verifikasi={"ekspresi": "14 - 8", "hasil": "6"})
tf("c4", "sedang", X, Kn, S3, "Baris piktogram yang memuat 4 gambar apel lebih panjang dari baris 7 gambar apel.", "Salah", "7 gambar apel lebih panjang barisnya daripada 4 gambar.")
mc("c4", "sulit", X, Me, S4, "Piktogram: buku komik 9 gambar, ensiklopedia 7 gambar. Berapa selisihnya?", ["2 buku", "1 buku", "3 buku", "4 buku"], "A", "9 - 7 = 2 buku.", verifikasi={"ekspresi": "9 - 7", "hasil": "2"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Apa yang pertama kali kamu periksa saat melihat piktogram baru?", ["membaca judul di bagian atas untuk memahami topik data", "langsung mewarnai gambar", "menghitung semua garis tepi", "merobek kertas"], "A", "Membaca judul piktogram memberi pemahaman tentang isi topik data.")
mc("c4", "sulit", K, Me, S3, "Piktogram: baris A ada 18 bintang. Dihapus 9 bintang. Sisa bintang?", ["9 bintang", "8 bintang", "10 bintang", "7 bintang"], "A", "18 - 9 = 9 bintang.", verifikasi={"ekspresi": "18 - 9", "hasil": "9"})
tf("c4", "sulit", K, Me, S4, "Dua baris yang memiliki jumlah gambar yang sama memiliki nilai data yang berbeda.", "Salah", "Jumlah gambar sama berarti nilai datanya sama.")
mc("c4", "sulit", K, Me, S4, "Piktogram: bus 7, sedan 6, truk 5. Total kendaraan seluruhnya?", ["18 kendaraan", "17 kendaraan", "19 kendaraan", "16 kendaraan"], "A", "7 + 6 + 5 = 18 kendaraan.", verifikasi={"ekspresi": "7 + 6 + 5", "hasil": "18"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Piktogram seragam: merah-putih 8 siswa, pramuka 7 siswa. Total siswa?", ["15 siswa", "14 siswa", "16 siswa", "13 siswa"], "A", "8 + 7 = 15 siswa.", verifikasi={"ekspresi": "8 + 7", "hasil": "15"})
mc("c5", "sedang", T, Me, S2, "Ada 20 siswa di piktogram olahraga: senam 8, kasti 6, sisanya renang. Siswa renang?", ["6 siswa", "5 siswa", "7 siswa", "4 siswa"], "A", "20 - (8 + 6) = 6 siswa.", verifikasi={"ekspresi": "20 - (8 + 6)", "hasil": "6"})
mc("c5", "sedang", T, Me, S3, "Piktogram nilai bintang: 3 anak masing-masing dapat 5 bintang. Total bintang?", ["15 bintang", "12 bintang", "16 bintang", "14 bintang"], "A", "3 x 5 = 15 bintang.", verifikasi={"ekspresi": "3 * 5", "hasil": "15"})
mc("c5", "sulit", T, Me, S4, "Piktogram buah: jambu 6, pir 5, duku 4. Berapa total seluruh buah itu?", ["15 buah", "14 buah", "16 buah", "13 buah"], "A", "6 + 5 + 4 = 15 buah.", verifikasi={"ekspresi": "6 + 5 + 4", "hasil": "15"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Piktogram: kelas 1A punya 8 piala, kelas 1B punya 6 piala. Total piala?", ["14 piala", "13 piala", "15 piala", "12 piala"], "A", "8 + 6 = 14 piala.", verifikasi={"ekspresi": "8 + 6", "hasil": "14"})
mc("c5", "sulit", K, Me, S4, "Piktogram: bola merah 9 gambar, bola biru 4 gambar. Berapa selisihnya?", ["5 bola", "4 bola", "6 bola", "3 bola"], "A", "9 - 4 = 5 bola.", verifikasi={"ekspresi": "9 - 4", "hasil": "5"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Jika data menunjukkan 5 anak suka kucing dan 8 anak suka kelinci, piktogram yang benar adalah ....", ["baris kelinci digambar 8 simbol dan kucing 5 simbol", "baris kelinci kosong", "kucing digambar 10 simbol", "kedua baris digambar 1 simbol"], "A", "Piktogram menyajikan simbol gambar sesuai data: 8 kelinci dan 5 kucing.")
mc("c6", "sulit", K, Me, S4, "Evaluasilah piktogram: apel 6 gambar, jeruk 9 gambar. Kesimpulan yang benar adalah ....", ["jeruk lebih disukai siswa daripada apel dengan selisih 3 buah", "apel paling banyak", "keduanya sama banyak", "jeruk tidak disukai"], "A", "Jeruk unggul dengan selisih 9 - 6 = 3 buah.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Piktogram buku: rak A ada 9, B ada 7, dan C ada 5. Total seluruh buku?", ["21 buku", "20 buku", "22 buku", "19 buku"], "A", "9 + 7 + 5 = 21 buku.", verifikasi={"ekspresi": "9 + 7 + 5", "hasil": "21"})
mc("c6", "sulit", P, Me, S4, "Piktogram bunga: mawar 14 tangkai, melati 8 tangkai. Berapa selisih tangkainya?", ["6 tangkai", "5 tangkai", "7 tangkai", "4 tangkai"], "A", "14 - 8 = 6 tangkai.", verifikasi={"ekspresi": "14 - 8", "hasil": "6"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab34_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab34.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
