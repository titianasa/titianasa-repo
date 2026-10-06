#!/usr/bin/env python3
"""
Generator dan validator Bab 3 Matematika Kelas 1 SD:
"Mengenal Bilangan 11 sampai 20" (Fase A)
bab_id: 41947501-8aae-4d62-ae62-f85718123a28
article_id: 26ca1595-db2d-4581-bec5-e46fec4e2233
quiz_id: 909e6657-dd87-4c32-8b67-c1536b4e6971
"""
import json, uuid, random, re, os
from collections import Counter

random.seed(43)
S1, S2, S3, S4 = "a3b2c19d4e61", "b4c3d20e5f72", "c5d4e31f6a83", "d6e5f42a7b94"

def e(s, n):
    return " ".join("".join([s] * min(5, n - i)) for i in range(0, n, 5))

D, T, X = "diagnostik", "latihan_terarah", "latihan_mandiri"
K, R, P = "checkpoint_akhir", "remedial", "pengayaan"
F, Kn, Pr, Me = "faktual", "konseptual", "prosedural", "metakognitif"

Q = []

def mc(b, d, f, dim, s, stem, opts, ans, ex, m=None, verifikasi=None):
    assert len(opts) == 4, f"Options harus tepat 4: {opts}"
    Q.append(dict(t="mc", b=b, d=d, f=f, dim=dim, s=s, stem=stem, opts=opts, ans=ans, ex=ex, m=m, verifikasi=verifikasi))

def tf(b, d, f, dim, s, text, ans, ex, verifikasi=None):
    Q.append(dict(t="tf", b=b, d=d, f=f, dim=dim, s=s, stem=text, ans=ans, ex=ex, verifikasi=verifikasi))

def sa(b, d, f, dim, s, stem, ans, ex, verifikasi=None):
    Q.append(dict(t="sa", b=b, d=d, f=f, dim=dim, s=s, stem=stem, ans=ans, ex=ex, verifikasi=verifikasi))

# ── C1 MUDAH (5 soal: 2 diagnostik, 3 terarah) ─────────────────────────────
mc("c1", "mudah", D, F, S1, "Lambang bilangan sebelas adalah ....", ["11", "12", "10", "13"], "A", "Sebelas dilambangkan dengan angka 11.", verifikasi={"ekspresi": "11", "hasil": "11"})
tf("c1", "mudah", D, F, S1, "Angka 12 dibaca dua puluh.", "Salah", "Angka 12 dibaca dua belas.")
mc("c1", "mudah", T, F, S1, "Lambang bilangan lima belas adalah ....", ["15", "14", "16", "51"], "A", "Lima belas dilambangkan dengan angka 15.", verifikasi={"ekspresi": "15", "hasil": "15"})
mc("c1", "mudah", T, F, S2, "Lambang bilangan delapan belas adalah ....", ["18", "17", "19", "81"], "A", "Delapan belas dilambangkan dengan angka 18.", verifikasi={"ekspresi": "18", "hasil": "18"})
sa("c1", "mudah", T, F, S2, "Tulis lambang bilangan dua puluh.", "20|dua puluh", "Dua puluh dilambangkan dengan angka 20.", verifikasi={"ekspresi": "20", "hasil": "20"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
mc("c2", "mudah", D, Kn, S3, "Bilangan 13 terdiri dari ....", ["10 dan 3", "10 dan 1", "10 dan 5", "1 dan 30"], "A", "Tiga belas terbentuk dari sepuluh ditambah tiga.")
tf("c2", "mudah", D, Kn, S1, "Bilangan belasan berawalan angka 1.", "Benar", "Semua bilangan belasan 11 sampai 19 berawalan angka 1.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S4, "Budi ingin menulis dua belas. Lambangnya ....", ["12", "21", "20", "11"], "A", "Dua belas ditulis 12, bukan 21.", "Tertukar posisi puluhan dan satuan pada 12 dan 21", verifikasi={"ekspresi": "12", "hasil": "12"})
mc("c2", "mudah", R, Kn, S3, "Kumpulan 10 dan 4 membentuk bilangan ....", ["14", "41", "104", "40"], "A", "Sepuluh dan empat membentuk empat belas (14).", "Mengira 10 dan 4 ditulis berdampingan 104", verifikasi={"ekspresi": "10+4", "hasil": "14"})

# Terarah (4)
mc("c2", "mudah", T, Kn, S1, f"Lambang untuk {e('🍎', 12)} adalah ....", ["12", "11", "13", "10"], "A", "Ada 12 apel, lambang bilangannya adalah 12.", verifikasi={"ekspresi": "12", "hasil": "12"})
mc("c2", "mudah", T, Kn, S2, f"Lambang untuk {e('⭐', 16)} adalah ....", ["16", "15", "17", "18"], "A", "Ada 16 bintang, lambang bilangannya adalah 16.", verifikasi={"ekspresi": "16", "hasil": "16"})
tf("c2", "mudah", T, Kn, S3, "Dua puluh adalah tiga kelompok sepuluh.", "Salah", "Dua puluh adalah dua kelompok sepuluh.")
sa("c2", "mudah", T, F, S1, f"Tulis lambang bilangan untuk {e('🎈', 13)}.", "13|tiga belas", "Ada 13 balon, lambang bilangannya 13.", verifikasi={"ekspresi": "13", "hasil": "13"})

# ── C3 MUDAH (2 soal: 2 terarah) ──────────────────────────────────────────
mc("c3", "mudah", T, Pr, S4, "Urutan membilang maju setelah 14 adalah ....", ["15", "13", "16", "17"], "A", "Setelah 14 pada hitungan maju adalah 15.", verifikasi={"ekspresi": "14+1", "hasil": "15"})
mc("c3", "mudah", T, Kn, S3, "Bilangan 10 dan 7 menjadi ....", ["17", "71", "18", "16"], "A", "Sepuluh ditambah tujuh menjadi tujuh belas (17).", verifikasi={"ekspresi": "10+7", "hasil": "17"})

# ── C3 SEDANG (12 soal: 4 checkpoint, 2 remedial, 6 terarah) ──────────────
mc("c3", "sedang", K, Kn, S1, "Urutan bilangan belasan dari yang terkecil adalah ....", ["11, 12, 13, 14", "11, 13, 12, 14", "14, 12, 13, 11", "12, 11, 14, 13"], "A", "Urutan maju yang benar adalah 11, 12, 13, 14.")
mc("c3", "sedang", K, Kn, S2, "Urutan bilangan setelah 17 adalah ....", ["18, 19, 20", "16, 15, 14", "19, 18, 20", "20, 19, 18"], "A", "Setelah 17 berurutan adalah 18, 19, 20.")
mc("c3", "sedang", K, Kn, S3, "Bilangan 16 dibentuk dari ....", ["10 dan 6", "10 dan 5", "10 dan 7", "1 dan 60"], "A", "Enam belas dibentuk dari 10 dan 6.")
tf("c3", "sedang", K, Kn, S2, "Bilangan 19 lebih kecil dari 20.", "Benar", "Sembilan belas berada tepat sebelum dua puluh.")

# Remedial (2)
mc("c3", "sedang", R, Me, S4, "Rani menulis lima belas dengan 51. Yang benar ....", ["15", "50", "14", "16"], "A", "Lima belas diawali angka 1, jadi lambangnya 15.", "Menulis angka satuan terlebih dahulu", verifikasi={"ekspresi": "15", "hasil": "15"})
mc("c3", "sedang", R, Me, S4, "Dodi membilang 10 langsung lompat 12. Yang terlewat ....", ["11", "13", "10", "9"], "A", "Antara 10 dan 12 ada bilangan 11.", "Melewatkan bilangan sebelas saat membilang", verifikasi={"ekspresi": "10+1", "hasil": "11"})

# Terarah (6)
mc("c3", "sedang", T, Kn, S1, f"Banyak {e('🚗', 14)}. Lambangnya ....", ["14", "13", "15", "12"], "A", "Ada 14 mobil, lambangnya adalah 14.", verifikasi={"ekspresi": "14", "hasil": "14"})
mc("c3", "sedang", T, Kn, S2, f"Banyak {e('🌸', 17)}. Lambangnya ....", ["17", "16", "18", "19"], "A", "Ada 17 bunga, lambangnya adalah 17.", verifikasi={"ekspresi": "17", "hasil": "17"})
mc("c3", "sedang", T, Pr, S4, "Cara mudah hitung belasan adalah ....", ["kumpulkan 10 benda lalu hitung sisanya", "tebak banyak benda", "hitung cepat tanpa tunjuk", "hitung dari belakang"], "A", "Mengelompokkan 10 benda membuat hitungan belasan lebih mudah.")
tf("c3", "sedang", T, Kn, S1, "Angka 14 dibaca empat puluh.", "Salah", "Lambang 14 dibaca empat belas, bukan empat puluh.")
tf("c3", "sedang", T, Kn, S3, "Angka 18 itu 10 dan 8.", "Benar", "Delapan belas adalah gabungan 10 dan 8.")
sa("c3", "sedang", T, F, S3, "Berapa hasil gabungan 10 dan 5?", "15|lima belas", "Sepuluh dan lima membentuk 15.", verifikasi={"ekspresi": "10+5", "hasil": "15"})

# ── C4 SEDANG (10 soal: 3 checkpoint, 7 terarah) ───────────────────────────
mc("c4", "sedang", K, Kn, S1, "Bilangan di antara 12 dan 14 adalah ....", ["13", "11", "15", "16"], "A", "Di antara 12 dan 14 adalah 13.", verifikasi={"ekspresi": "12+1", "hasil": "13"})
mc("c4", "sedang", K, Kn, S2, "Bilangan di antara 18 dan 20 adalah ....", ["19", "17", "16", "21"], "A", "Di antara 18 dan 20 adalah 19.", verifikasi={"ekspresi": "18+1", "hasil": "19"})
tf("c4", "sedang", K, Kn, S3, "Dua belas benda lebih sedikit dari sepuluh benda.", "Salah", "Dua belas lebih banyak daripada sepuluh.")

# Terarah (7)
mc("c4", "sedang", T, Kn, S1, "Lengkapi urutan: 11, 12, ..., 14.", ["13", "15", "10", "16"], "A", "Urutan lengkapnya adalah 11, 12, 13, 14.", verifikasi={"ekspresi": "12+1", "hasil": "13"})
mc("c4", "sedang", T, Kn, S2, "Lengkapi urutan: 16, 17, ..., 19.", ["18", "20", "15", "17"], "A", "Urutan lengkapnya adalah 16, 17, 18, 19.", verifikasi={"ekspresi": "17+1", "hasil": "18"})
mc("c4", "sedang", T, Kn, S3, f"Manakah kumpulan dengan jumlah 15?", [e('🍬', 15), e('🍬', 14), e('🍬', 16), e('🍬', 13)], "A", "Kumpulan permen pertama berjumlah 15.")
mc("c4", "sedang", T, Pr, S4, "Agar tidak salah membilang sampai 20, kita ....", ["lingkari tiap kelompok sepuluh", "menghitung sambil bernyanyi", "menebak jumlah akhir", "menghitung dua kali tiap benda"], "A", "Melingkari kelompok sepuluh mempermudah hitungan.")
tf("c4", "sedang", T, Pr, S4, "Menghitung 15 benda lebih rapi dengan membuat kelompok sepuluh.", "Benar", "Membuat sepuluh membantu melihat sisanya.")
tf("c4", "sedang", T, Kn, S1, f"{e('🐱', 11)} cocok dengan lambang 15.", "Salah", "Kucing berjumlah 11, cocok dengan lambang 11.")
sa("c4", "sedang", T, Pr, S2, "Bilangan berapakah antara 15 dan 17?", "16|enam belas", "Bilangan di antara 15 dan 17 adalah 16.", verifikasi={"ekspresi": "15+1", "hasil": "16"})

# ── C5 SEDANG (3 soal: 3 checkpoint) ──────────────────────────────────────
mc("c5", "sedang", K, Me, S4, "Tono menulis 13 menjadi 31. Kesalahan Tono ....", ["angka 1 dan 3 tertukar tempat", "angka 3 terlalu besar", "lupa menulis angka nol", "salah menghitung benda"], "A", "Tono menukar posisi angka puluhan dan satuan.")
mc("c5", "sedang", K, Kn, S3, "Manakah pernyataan yang tidak benar?", ["14 adalah 10 dan 5", "12 adalah 10 dan 2", "17 adalah 10 dan 7", "20 adalah dua kelompok sepuluh"], "A", "Empat belas adalah 10 dan 4, bukan 10 dan 5.")
mc("c5", "sedang", K, Me, S3, "Cara membuktikan ada 16 pensil adalah ....", ["buat seikat isi 10 lalu tambah 6", "hitung sekilas saja", "tebak langsung 16", "lihat panjang kotaknya"], "A", "Membuat seikat isi 10 dan 6 sisanya membuktikan ada 16.")

# ── C3 SULIT (2 soal: 2 mandiri) ──────────────────────────────────────────
mc("c3", "sulit", X, Kn, S2, "Urutan bilangan mundur dari 15 adalah ....", ["15, 14, 13, 12", "12, 13, 14, 15", "15, 16, 17, 18", "14, 15, 13, 12"], "A", "Hitungan mundur dari 15 adalah 15, 14, 13, 12.")
sa("c3", "sulit", X, F, S3, "Berapakah lambang angka untuk delapan belas?", "18|delapan belas", "Delapan belas dilambangkan dengan angka 18.", verifikasi={"ekspresi": "18", "hasil": "18"})

# ── C4 SULIT (3 soal: 3 mandiri) ──────────────────────────────────────────
mc("c4", "sulit", X, Kn, S1, f"Ada {e('✏️', 10)} dan {e('✏️', 4)}. Semuanya berjumlah ....", ["14", "13", "15", "16"], "A", "Sepuluh pensil dan empat pensil menjadi 14 pensil.", verifikasi={"ekspresi": "10+4", "hasil": "14"})
mc("c4", "sulit", X, Kn, S3, "Bilangan yang nilainya paling mendekati 20 adalah ....", ["19", "15", "12", "10"], "A", "Sembilan belas (19) berada tepat satu langkah sebelum 20.", verifikasi={"ekspresi": "20-1", "hasil": "19"})
tf("c4", "sulit", X, Me, S4, "Mengecek hitungan dua kali memastikan tidak ada benda terlewat.", "Benar", "Pengecekan ulang menjamin keakuratan hitungan.")

# ── C5 SULIT (3 soal: 3 mandiri) ──────────────────────────────────────────
mc("c5", "sulit", X, Me, S4, "Andi membilang 18 bola, Budi 19 bola. Yang tepat ....", ["hitung bersama dan kelompokkan per sepuluh", "pilih hitungan Andi saja", "pilih hitungan Budi saja", "tebak ada 20 bola"], "A", "Menghitung bersama dengan kelompok sepuluh memastikan hasil yang benar.")
mc("c5", "sulit", X, Kn, S3, "Kartu angka yang berurutan setelah 15 adalah ....", ["16, 17, 18", "17, 16, 18", "18, 17, 16", "15, 17, 16"], "A", "Urutan angka setelah 15 adalah 16, 17, 18.")
mc("c5", "sulit", X, Me, S3, "Siti ragu apakah bendanya 15 atau 16. Cara cepat ....", ["hitung lima-lima atau buat puluhan", "tebak angka terbesar", "tutup sebagian benda", "kurangi satu benda"], "A", "Membuat kelompok puluhan atau hitung lima-lima sangat cepat dan teliti.")

# ── C6 SULIT (2 soal: 2 pengayaan) ────────────────────────────────────────
mc("c6", "sulit", P, Kn, S3, "Kartu angka 17 yang lengkap memuat ....", ["angka 17 dan gambar 17 benda", "hanya gambar 10 bintang", "angka 7 saja", "tulisan tujuh belas tanpa angka"], "A", "Kartu yang lengkap memuat lambang angka 17 dan 17 gambar benda.")
mc("c6", "sulit", P, Pr, S4, "Rencana menyusun kartu 11 sampai 20 di papan ....", ["susun berderet rapi dari 11 ke 20", "letakkan secara acak", "susun angka genap saja", "pasang angka 20 di awal"], "A", "Menyusun berderet rapi dari 11 ke 20 memudahkan teman sekelas membaca.")

assert len(Q) == 50, f"Total soal: {len(Q)}"

# Validasi stem length <= 12 kata
for i, q in enumerate(Q):
    wcnt = len(q["stem"].split())
    assert wcnt <= 12, f"Stem Q#{i+1} terlalu panjang ({wcnt} kata): {q['stem']}"

# Distribusi taxonomy
c_b = Counter(q["b"] for q in Q)
c_d = Counter(q["d"] for q in Q)
c_f = Counter(q["f"] for q in Q)
c_dim = Counter(q["dim"] for q in Q)
c_t = Counter(q["t"] for q in Q)

print("Bloom:", dict(c_b))
print("Difficulty:", dict(c_d))
print("Fungsi:", dict(c_f))
print("Dimensi:", dict(c_dim))
print("Tipe:", dict(c_t))

# Hitung latihan per section
latihan_sec = Counter(q["s"] for q in Q if q["f"] in ("latihan_terarah", "checkpoint_bagian"))
print("Latihan per section (min 4):", dict(latihan_sec))
for sec_id, count in latihan_sec.items():
    assert count >= 4, f"Bagian {sec_id} hanya punya {count} latihan, minimum 4!"

uid = lambda i: str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab3_soal_{i}"))
groups = {"mc": [], "tf": [], "sa": []}

random.seed(43)
for idx, q in enumerate(Q):
    tax = {
        "bloom": q["b"],
        "difficulty": q["d"],
        "fungsi": q["f"],
        "knowledge_dimension": q["dim"]
    }
    if q.get("m"):
        tax["miskonsepsi_target"] = q["m"]
    base = {
        "uid": uid(idx),
        "taxonomy": tax,
        "explanation": q["ex"],
        "source_section_id": q["s"]
    }
    if q.get("verifikasi"):
        base["verifikasi"] = q["verifikasi"]
    if q["t"] == "mc":
        opts = list(q["opts"])
        ans_text = opts[ord(q["ans"]) - 65]
        random.shuffle(opts)
        label = "ABCD"[opts.index(ans_text)]
        base.update(
            stem=q["stem"],
            answer=label,
            choices=[{"label": "ABCD"[i], "text": o} for i, o in enumerate(opts)]
        )
        groups["mc"].append(base)
    elif q["t"] == "tf":
        base.update(text=q["stem"], answer=q["ans"])
        groups["tf"].append(base)
    else:
        base.update(stem=q["stem"], answer=q["ans"])
        groups["sa"].append(base)

n = 0
qg = []
for gid, typ, ins, extra in (
    ("mc", "multiple_choice", "Pilih jawaban yang paling tepat.", {}),
    ("tf", "true_false", "Tentukan benar atau salah.", {"options": ["Benar", "Salah"]}),
    ("sa", "short_answer", "Jawab singkat dengan satu angka atau satu kata.", {})
):
    for x in groups[gid]:
        n += 1
        x["number"] = n
    qg.append({
        "type": typ,
        "group_id": gid,
        "instruction": ins,
        "questions": groups[gid],
        "ai_meta": {"draft": True},
        **extra
    })

secs = [
    ("Membilang 11 sampai 15", S1),
    ("Membilang 16 sampai 20", S2),
    ("Kumpulan Sepuluh dan Satuan", S3),
    ("Menulis Bilangan Belasan dengan Teliti", S4)
]

quiz = {
    "level": "Kelas 1 SD — Fase A",
    "sections": [{"title": t, "section_id": i} for t, i in secs],
    "passing_score": 70.0,
    "shuffle_choices": True,
    "shuffle_question_order": True,
    "question_groups": qg
}

# ── MATERI PELAJARAN (LESSON PLAN) ─────────────────────────────────────────
mat = [
    (S1, "Aku bisa membilang dan melambangkan bilangan 11 sampai 15.", "Membilang 11 sampai 15",
f"""Mari membilang bilangan setelah 10.
Bilangan setelah 10 adalah belasan.

Ayo kita hitung bersama:
Sepuluh ditambah 1 menjadi sebelas (11).
Sepuluh ditambah 2 menjadi dua belas (12).
Sepuluh ditambah 3 menjadi tiga belas (13).
Sepuluh ditambah 4 menjadi empat belas (14).
Sepuluh ditambah 5 menjadi lima belas (15).

:::definition
term: Bilangan Belasan
definition: Bilangan 11 sampai 19 yang berawalan angka satu.
:::

:::callout
variant: tip
title: Ingat ya
text: Angka 1 selalu ditulis di depan untuk belasan.
:::""", 3),

    (S2, "Aku bisa membilang dan melambangkan bilangan 16 sampai 20.", "Membilang 16 sampai 20",
f"""Ayo membilang sampai 20.
Mari kita sebut bersama.

Sepuluh dan 6 itu 16.
Sepuluh dan 7 itu 17.
Sepuluh dan 8 itu 18.
Sepuluh dan 9 itu 19.
Dua puluh ditulis 20.

:::table
headers: ["Nama","Lambang"]
rows: [["enam belas.","16."],["tujuh belas.","17."],["delapan belas.","18."],["sembilan belas.","19."],["dua puluh.","20."]]
caption: Lambang Bilangan 16 sampai 20
:::""", 4),

    (S3, "Aku memahami bilangan belasan sebagai kumpulan sepuluh dan satuan.", "Kumpulan Sepuluh dan Satuan",
f"""Membilang belasan itu sangat mudah.
Kumpulkan sepuluh benda terlebih dahulu.
Lalu hitung benda yang tersisa.

Contoh kumpulan benda:
12 kelereng adalah 10 kelereng dan 2.
15 permen adalah 10 permen dan 5.
20 balok adalah 10 balok dan 10.

:::steps
title: Cara membilang belasan
items: ["Kumpulkan sepuluh benda pertama.","Hitung sisa benda di luar kelompok.","Gabungkan sepuluh dan sisa menjadi belasan."]
:::""", 4),

    (S4, "Aku bisa menulis lambang bilangan 11 sampai 20 dengan teliti.", "Menulis Bilangan Belasan dengan Teliti",
f"""Tulis lambang belasan dengan urut ya.
Tulis angka 1 terlebih dahulu di depan.
Lalu tulis angka satuannya di belakang.

Hati-hati dengan angka 12 dan 21.
Dua belas ditulis 12.
Dua puluh satu ditulis 21.

:::common_trap
term: Menghitung Benda Dua Kali atau Terlewat
explanation: Lingkari sepuluh benda lebih dulu agar sisa benda mudah dihitung tanpa terlewat.
:::

:::callout
variant: summary
title: Ringkasan
text: Bilangan 11 sampai 19 berawalan 1. Bilangan 20 berawalan 2.
:::""", 3),
]

lp = {
    "level": "Kelas 1 SD — Fase A",
    "title": "Mengenal Bilangan 11 sampai 20",
    "topic": "Bilangan sampai 20",
    "language": "id",
    "sections": [{"id": i, "goal": g, "title": t, "content": c, "minutes": m} for i, g, t, c, m in mat]
}

# Verifikasi metrik materi
for i, s in enumerate(lp["sections"]):
    raw_words = s["content"].split()
    assert len(raw_words) <= 120, f"Section {i+1} melebihi 120 kata ({len(raw_words)} kata)"
    clean = re.sub(r':::[a-z_]+.*?(?:\n.*?)*?:::', '', s["content"], flags=re.DOTALL)
    sentences = [sent.strip() for sent in re.split(r'[.!?\n]+', clean) if sent.strip()]
    lens = [len(sent.split()) for sent in sentences]
    if lens:
        avg = sum(lens) / len(lens)
        mx = max(lens)
        assert avg <= 6.0, f"Section {i+1} avg sentence len > 6 ({avg:.1f})"
        assert mx <= 10, f"Section {i+1} max sentence len > 10 ({mx})"

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab3.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"lesson_plan": lp, "quiz_config": quiz}, f, ensure_ascii=False, indent=2)

print("BERHASIL:", out_path, "berhasil dibuat dan divalidasi!")
