#!/usr/bin/env python3
"""
Generator dan validator Bab 29 Matematika Kelas 1 SD:
"Mengenal Kubus, Balok, Bola, dan Tabung" (Fase A)
bab_id: 3102d5f3-0f64-419f-96df-b598390c38ae
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "c1d2e33f4a01"  # Mengenal Kubus dan Balok
S2 = "d2e3f44a5b12"  # Mengenal Bola dan Tabung
S3 = "e3f4a55b6c23"  # Benda yang Menggelinding dan Menumpuk
S4 = "f4a5b66c7d34"  # Mengelompokkan Benda Ruang di Sekitar

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Peganglah sebuah dadu permainan.
Dadu berbentuk bangun ruang kubus.
Semua sisi kubus sama besar.
Bentuk sisinya persegi sama rata.
Sekarang lihatlah kotak pasta gigimu.
Kotak pasta gigi berbentuk balok.
Balok memiliki sisi lebih panjang.
Keduanya adalah benda berbentuk kotak.

:::definition
title: Kubus dan Balok
Kubus memiliki semua sisi persegi sama besar.
Balok memiliki sisi persegi panjang yang tidak sama.
:::"""

s2_content = """Lihat bola sepak di lapangan.
Bola berbentuk bulat utuh melengkung.
Bola tidak memiliki sudut tajam.
Bola bisa menggelinding ke mana saja.
Sekarang amati kaleng susu kental.
Kaleng susu berbentuk bangun tabung.
Alas tabung berbentuk lingkaran datar.
Tutup tabung juga berbentuk lingkaran.

:::steps
title: Ciri Tabung
1. Memiliki alas berbentuk lingkaran.
2. Memiliki tutup berbentuk lingkaran.
3. Memiliki sisi lengkung yang menyelimuti.
:::"""

s3_content = """Benda ruang memiliki sifat gerak.
Bola sangat mudah menggelinding cepat.
Tabung tidur juga bisa menggelinding.
Tetapi kubus tidak bisa menggelinding.
Kubus dan balok mudah ditumpuk.
Permukaannya datar dan tidak goyang.
Tabung berdiri juga bisa ditumpuk.
Susunan balok bisa sangat rapi."""

s4_content = """Banyak benda ruang di rumah.
Lemari pakaian berbentuk balok besar.
Kotak kado kecil berbentuk kubus.
Kelereng mainan berbentuk bola kecil.
Gelas minum berbentuk tabung silinder.

:::common_trap
title: Membedakan Kubus dan Balok
Kubus semua sisinya sama besar.
Balok memiliki sisi lebih panjang.
Kotak dadu berbentuk kubus.
Kotak pasta gigi berbentuk balok.
Jangan tertukar antara kubus dan balok.
:::

:::callout
variant: summary
title: Ringkasan
text: Kubus dan balok berbentuk kotak. Bola berbentuk bulat. Tabung beralas lingkaran. Bola menggelinding, balok mudah ditumpuk.
:::"""

sections = [
    {
        "id": S1,
        "title": "Mengenal Kubus dan Balok",
        "minutes": 6,
        "goal": "Siswa mengenal bangun ruang kubus dan balok serta ciri permukaan kotaknya.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Mengenal Bola dan Tabung",
        "minutes": 6,
        "goal": "Siswa mengenal bangun ruang bola dan tabung serta bentuk permukaannya.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Benda yang Menggelinding dan Menumpuk",
        "minutes": 6,
        "goal": "Siswa memahami sifat benda yang dapat menggelinding dan benda yang dapat ditumpuk.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Mengelompokkan Benda Ruang di Sekitar",
        "minutes": 6,
        "goal": "Siswa dapat mengidentifikasi dan mengelompokkan aneka benda ruang di lingkungan sehari-hari.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Mengenal Kubus, Balok, Bola, dan Tabung",
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
# 2. DEFINISI BANK 50 SOAL BAB 29
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
mc("c1", "mudah", D, F, S1, "Dadu permainan memiliki bentuk bangun ruang ....", ["kubus", "bola", "tabung", "lingkaran"], "A", "Dadu berbentuk kubus dengan 6 sisi persegi sama besar.")
tf("c1", "mudah", D, F, S2, "Bola sepak dapat menggelinding dengan sangat mudah.", "Benar", "Bentuk bulat bola membuatnya mudah menggelinding.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S2, "Alas dan tutup pada kaleng susu berbentuk ....", ["lingkaran", "segitiga", "bintang", "persegi"], "A", "Kaleng tabung memiliki alas dan tutup lingkaran datar.")
mc("c1", "mudah", T, F, S3, "Benda ruang yang paling mudah ditumpuk rapi adalah ....", ["balok kayu", "bola kasti", "kelereng bulat", "jeruk purut"], "A", "Balok dan kubus memiliki permukaan datar sehingga mudah ditumpuk.")
sa("c1", "mudah", T, F, S1, "Berapa banyak sisi pada sebuah bangun kubus?", "6", "Kubus memiliki 6 sisi datar.", verifikasi={"ekspresi": "6", "hasil": "6"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S4, "Kotak pasta gigi dan kotak sepatu termasuk bentuk ....", ["balok", "bola", "tabung", "lingkaran"], "A", "Kotak pasta gigi dan sepatu berbentuk balok memanjang.", "Tertukar antara kubus dan balok")
tf("c2", "mudah", D, Kn, S1, "Semua sisi pada kubus memiliki ukuran yang sama besar.", "Benar", "Kubus tersusun dari 6 sisi persegi yang sama besar.")

# Remedial (2)
mc("c2", "mudah", R, F, S1, "Apa perbedaan sisi kubus dan sisi balok?", ["sisi kubus sama persegi, sisi balok ada yang lebih panjang", "kubus bulat melengkung", "balok tidak punya sisi", "keduanya sama persis"], "A", "Kubus semua sisinya persegi sama besar, balok punya sisi lebih panjang.", "Mengira kubus dan balok sama persis bentuk sisinya")
mc("c2", "mudah", R, Kn, S3, "Mengapa bola sepak tidak bisa ditumpuk ke atas dengan stabil?", ["karena permukaannya melengkung tanpa bidang datar", "karena bola terlalu berat", "karena bola kempes", "karena warnanya hitam putih"], "A", "Permukaan bola melengkung bulat sehingga menggelinding jika ditumpuk.", "Mengira semua benda bisa ditumpuk tinggi tanpa jatuh")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Ada 4 kubus dan 3 balok mainan. Berapa jumlah kotak mainan itu?", ["7 kotak", "6 kotak", "8 kotak", "5 kotak"], "A", "4 + 3 = 7 buah kotak.", verifikasi={"ekspresi": "4 + 3", "hasil": "7"})
mc("c2", "mudah", T, Kn, S2, "Berapa jumlah alas dan tutup berbentuk lingkaran pada 1 tabung?", ["2 lingkaran", "1 lingkaran", "3 lingkaran", "0 lingkaran"], "A", "Tabung memiliki 1 alas dan 1 tutup lingkaran (total 2).", verifikasi={"ekspresi": "1 + 1", "hasil": "2"})
tf("c2", "mudah", T, Kn, S3, "Dadu kubus dapat menggelinding lancar seperti bola tenis.", "Salah", "Kubus bersisi datar sehingga tidak bisa menggelinding mulus.")
sa("c2", "mudah", T, Kn, S4, "Di rak ada 5 bola dan 3 tabung kaleng. Berapa total benda?", "8", "5 + 3 = 8 benda.", verifikasi={"ekspresi": "5 + 3", "hasil": "8"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Manakah pasangan benda yang keduanya berbentuk tabung silinder?", ["kaleng biskuit dan drum air", "kotak pensil dan dadu", "bola bekel dan jeruk", "buku tulis dan kertas"], "A", "Kaleng biskuit dan drum air berbentuk tabung.", "Keliru mengenali benda tabung sehari-hari")
mc("c3", "sedang", R, Pr, S3, "Budi ingin membuat menara susun tinggi. Benda mana yang paling tepat dipilih?", ["balok-balok kayu datar", "bola-bola tenis", "kelereng kaca", "buah semangka bulat"], "A", "Balok kayu bersisi datar sangat kokoh untuk menara susun.", "Memilih benda bulat untuk menara susun")

# Terarah (6): S1, S2, S3, S4, S1, S2 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S1, "Satu kubus punya 6 sisi. Berapa total sisi pada 2 kubus?", ["12 sisi", "10 sisi", "14 sisi", "8 sisi"], "A", "6 + 6 = 12 sisi.", verifikasi={"ekspresi": "6 + 6", "hasil": "12"})
mc("c3", "sedang", T, Pr, S2, "Dua tabung memiliki alas lingkaran. Berapa total lingkaran alas dan tutup keduanya?", ["4 lingkaran", "3 lingkaran", "5 lingkaran", "2 lingkaran"], "A", "2 x 2 = 4 lingkaran.", verifikasi={"ekspresi": "2 * 2", "hasil": "4"})
tf("c3", "sedang", T, Pr, S3, "Tabung yang diletakkan mendatar atau tidur dapat menggelinding.", "Benar", "Sisi lengkung selimut tabung bisa menggelinding saat dibaringkan.")
mc("c3", "sedang", T, Pr, S4, "Di keranjang ada 9 kelereng bola. Diambil 4 kelereng. Berapa sisa kelereng?", ["5 kelereng", "4 kelereng", "6 kelereng", "3 kelereng"], "A", "9 - 4 = 5 kelereng.", verifikasi={"ekspresi": "9 - 4", "hasil": "5"})
tf("c3", "sedang", T, Pr, S1, "Kotak lemari pakaian raksasa memiliki bentuk dasar bangun kubus dadu.", "Salah", "Lemari pakaian biasanya memiliki sisi panjang sehingga berbentuk balok.")
sa("c3", "mudah", T, Pr, S2, "Satu balok punya 6 sisi. Berapa total sisi 2 balok?", "12", "6 + 6 = 12 sisi.", verifikasi={"ekspresi": "6 + 6", "hasil": "12"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S1, "Doni punya 8 kubus mainan. Diberikan ke adik 3 kubus. Berapa kubus sisa?", ["5 kubus", "4 kubus", "6 kubus", "3 kubus"], "A", "8 - 3 = 5 kubus.", verifikasi={"ekspresi": "8 - 3", "hasil": "5"})
mc("c3", "sedang", X, Pr, S2, "Ada 6 kaleng tabung di meja. Ditambah 5 kaleng lagi. Berapa kaleng sekarang?", ["11 kaleng", "10 kaleng", "12 kaleng", "9 kaleng"], "A", "6 + 5 = 11 kaleng.", verifikasi={"ekspresi": "6 + 5", "hasil": "11"})
tf("c3", "sedang", X, Pr, S3, "Menumpuk 3 kubus ke atas lebih mudah roboh daripada menumpuk 3 bola.", "Salah", "Menumpuk kubus sangat stabil, sedangkan menumpuk bola langsung menggelinding jatuh.")
sa("c3", "sedang", X, Pr, S4, "Ada 14 bola kasti dan 6 balok kayu. Berapa selisih banyaknya?", "8", "14 - 6 = 8 buah.", verifikasi={"ekspresi": "14 - 6", "hasil": "8"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S1, "Edo punya 7 balok kayu. Budi punya 8 balok kayu. Berapa total balok keduanya?", ["15 balok", "14 balok", "16 balok", "13 balok"], "A", "7 + 8 = 15 balok.", verifikasi={"ekspresi": "7 + 8", "hasil": "15"})
mc("c3", "sedang", K, Pr, S3, "Di lantai ada 10 bola kelereng. Menggelinding keluar kamar 4 butir. Berapa kelereng sisa?", ["6 kelereng", "5 kelereng", "7 kelereng", "4 kelereng"], "A", "10 - 4 = 6 butir.", verifikasi={"ekspresi": "10 - 4", "hasil": "6"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S4
mc("c4", "sedang", T, Kn, S1, "Jika kotak kado memiliki 6 sisi yang semuanya persegi persis, maka benda itu adalah ....", ["kubus", "balok", "tabung", "bola"], "A", "Ciri 6 sisi persegi sama besar adalah kubus.")
mc("c4", "sedang", T, Kn, S2, "Manakah pernyataan yang benar mengenai bangun tabung?", ["memiliki dua permukaan lingkaran dan satu permukaan lengkung", "memiliki 6 sisi persegi", "tidak memiliki permukaan datar sama sekali", "bisa menggelinding ke segala arah seperti bola"], "A", "Tabung memiliki alas dan tutup lingkaran serta selimut lengkung.")
tf("c4", "sedang", T, Kn, S3, "Benda dengan permukaan datar bisa ditumpuk dengan rapi dan aman.", "Benar", "Permukaan datar memberikan tumpuan yang kokoh saat ditumpuk.")
tf("c4", "sedang", T, Kn, S4, "Semua benda yang berbentuk kotak pasti memiliki panjang sisi yang sama rata.", "Salah", "Balok berbentuk kotak tetapi panjang sisinya berbeda.")
sa("c4", "sedang", T, Kn, S4, "Ada 16 kotak pensil balok. 7 kotak dibagikan. Berapa kotak pensil sisa?", "9", "16 - 7 = 9 kotak.", verifikasi={"ekspresi": "16 - 7", "hasil": "9"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Batu bata dan kotak susu kemasan memiliki kesamaan bentuk bangun ruang, yaitu ....", ["balok", "kubus", "bola", "tabung"], "A", "Batu bata dan kotak susu berbentuk balok.")
mc("c4", "sedang", X, Kn, S2, "Udin punya 15 kaleng susu tabung. 6 kaleng kosong dibuang. Berapa kaleng sisa?", ["9 kaleng", "8 kaleng", "10 kaleng", "7 kaleng"], "A", "15 - 6 = 9 kaleng.", verifikasi={"ekspresi": "15 - 6", "hasil": "9"})
tf("c4", "sedang", X, Kn, S4, "Buah jeruk dan buah semangka bulat memiliki bentuk dasar bangun bola.", "Benar", "Keduanya bulat melengkung utuh menyerupai bola.")
mc("c4", "sulit", X, Me, S3, "Tersedia 12 kubus. Dibuat 2 menara sama tinggi. Berapa kubus tiap menara?", ["6 kubus", "5 kubus", "7 kubus", "4 kubus"], "A", "12 / 2 = 6 kubus.", verifikasi={"ekspresi": "12 // 2", "hasil": "6"})

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S1, "Mengapa kotak sepatu dibuat berbentuk balok dan bukan bola?", ["agar mudah disusun rapi di rak tanpa menggelinding", "agar lebih cepat berputar", "agar bisa ditendang", "agar warnanya cerah"], "A", "Bentuk balok memudahkan penyimpanan dan penumpukan rapi.")
mc("c4", "sulit", K, Me, S2, "Di toko ada 18 bola plastik. Terjual 9 bola. Berapa bola tersisa?", ["9 bola", "8 bola", "10 bola", "7 bola"], "A", "18 - 9 = 9 bola.", verifikasi={"ekspresi": "18 - 9", "hasil": "9"})
tf("c4", "sulit", K, Me, S3, "Sebuah bola basket yang dibelah dua menghasilkan dua buah bangun kubus.", "Salah", "Belahan bola berbentuk setengah bola, bukan kubus.")
mc("c4", "sulit", K, Me, S4, "Ada 20 balok kayu. Dipakai membuat jembatan 13 balok. Berapa balok sisa?", ["7 balok", "6 balok", "8 balok", "5 balok"], "A", "20 - 13 = 7 balok.", verifikasi={"ekspresi": "20 - 13", "hasil": "7"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Tiga buah dadu kubus masing-masing punya 6 sisi. Berapa total sisi ketiganya?", ["18 sisi", "16 sisi", "20 sisi", "15 sisi"], "A", "3 x 6 = 18 sisi datar.", verifikasi={"ekspresi": "3 * 6", "hasil": "18"})
mc("c5", "sedang", T, Me, S2, "Ada 4 tabung kaleng. Tiap tabung punya 2 lingkaran datar. Berapa total lingkaran datar?", ["8 lingkaran", "6 lingkaran", "10 lingkaran", "7 lingkaran"], "A", "4 x 2 = 8 lingkaran.", verifikasi={"ekspresi": "4 * 2", "hasil": "8"})
mc("c5", "sedang", T, Me, S3, "Jika kamu ingin membuat gerobak mainan yang berjalan, bagian roda harus berbentuk ....", ["tabung tipis atau lingkaran", "kubus dadu", "balok persegi panjang", "segitiga"], "A", "Bagian roda harus bundar agar bisa berputar menggelinding.")
mc("c5", "sulit", T, Me, S4, "Di meja ada 6 kubus, 4 balok, dan 5 bola. Berapa total seluruh benda ruang itu?", ["15 benda", "14 benda", "16 benda", "13 benda"], "A", "6 + 4 + 5 = 15 benda.", verifikasi={"ekspresi": "6 + 4 + 5", "hasil": "15"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S1, "Dua balok (tiap balok 6 sisi) ditambah 1 kubus (6 sisi). Berapa total sisi ketiganya?", ["18 sisi", "16 sisi", "20 sisi", "15 sisi"], "A", "(2 x 6) + 6 = 18 sisi.", verifikasi={"ekspresi": "2 * 6 + 6", "hasil": "18"})
mc("c5", "sulit", K, Me, S3, "Menara balok tingginya 14 balok. Roboh 6 balok. Berapa balok yang masih berdiri?", ["8 balok", "7 balok", "9 balok", "6 balok"], "A", "14 - 6 = 8 balok.", verifikasi={"ekspresi": "14 - 6", "hasil": "8"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S1, "Rancanglah susunan istana balok yang kokoh dan tidak mudah roboh!", ["letakkan balok-balok besar di bagian bawah lalu tumpuk kubus kecil di atasnya", "letakkan bola di bagian paling bawah sebagai pondasi", "tumpuk tabung posisi tidur di bawah", "taruh semua benda terbalik miring"], "A", "Pondasi balok datar di bawah memberikan dasar yang paling kokoh.")
mc("c6", "sulit", K, Me, S4, "Kelompokkan benda berikut berdasarkan bentuknya: dadu, kotak pasta gigi, kaleng susu, dan bola kasti!", ["dadu (kubus), pasta gigi (balok), kaleng susu (tabung), bola kasti (bola)", "semua benda di atas berbentuk balok kotak", "dadu dan kaleng berbentuk bola", "pasta gigi dan bola kasti berbentuk tabung"], "A", "Dadu kubus, pasta gigi balok, kaleng tabung, bola kasti bola.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S2, "Ada 5 kaleng tabung (tiap kaleng 2 lingkaran). Berapa total lingkaran dari 5 kaleng?", ["10 lingkaran", "8 lingkaran", "12 lingkaran", "9 lingkaran"], "A", "5 x 2 = 10 lingkaran.", verifikasi={"ekspresi": "5 * 2", "hasil": "10"})
mc("c6", "sulit", P, Me, S3, "Koleksi mainan: 4 kubus, 5 balok, 6 bola, dan 3 tabung. Berapa total mainan?", ["18 mainan", "16 mainan", "20 mainan", "17 mainan"], "A", "4 + 5 + 6 + 3 = 18 mainan.", verifikasi={"ekspresi": "4 + 5 + 6 + 3", "hasil": "18"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab29_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab29.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
