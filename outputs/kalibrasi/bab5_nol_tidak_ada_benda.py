#!/usr/bin/env python3
"""
Generator dan validator Bab 5 Matematika Kelas 1 SD:
"Nol sebagai Tidak Ada Benda" (Fase A)
bab_id: be561344-564c-4554-8638-9cda7d78ca8c
article_id: b4ee33b8-5dbc-4507-8ddb-be354bd0d584
quiz_id: 59b4fa1e-3f45-4b75-a0b5-c799a82e05d8
"""
import json, uuid, random, re, os
from collections import Counter

random.seed(45)
S1, S2, S3, S4 = "a5b4c39d6e81", "b6c5d40e7f92", "c7d6e51f8a03", "d8e7f62a9b14"

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
mc("c1", "mudah", D, F, S1, "Lambang bilangan nol ditulis angka ....", ["0", "1", "10", "2"], "A", "Nol dilambangkan dengan angka 0.", verifikasi={"ekspresi": "0", "hasil": "0"})
tf("c1", "mudah", D, F, S1, "Nol artinya ada sepuluh benda.", "Salah", "Nol artinya kosong atau tidak ada benda sama sekali.")
mc("c1", "mudah", T, F, S2, "Pada garis bilangan, angka 0 berada tepat sebelum ....", ["1", "2", "3", "4"], "A", "Angka 0 berada tepat sebelum angka 1.", verifikasi={"ekspresi": "1", "hasil": "1"})
mc("c1", "mudah", T, F, S4, "Bentuk angka nol menyerupai ....", ["bulat lonjong", "garis tegak", "tiga garis", "kotak berlubang"], "A", "Angka 0 berbentuk bulat lonjong.")
sa("c1", "mudah", T, F, S1, "Sebutkan nama bilangan untuk lambang 0.", "nol", "Lambang 0 dibaca nol.")

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
mc("c2", "mudah", D, Kn, S3, "Sebuah toples kosong. Banyak permen di toples ....", ["0", "1", "2", "10"], "A", "Toples kosong berarti ada 0 permen.", verifikasi={"ekspresi": "0", "hasil": "0"})
tf("c2", "mudah", D, Kn, S2, "Garis bilangan membilang mulai dari angka 0.", "Benar", "Membilang jarak dimulai dari titik nol.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Kotak pensil kosong. Banyak pensil di dalam kotak ....", ["0", "1", "2", "10"], "A", "Bila kotak kosong tanpa isi, jumlahnya adalah 0.", "Mengira benda kosong tetap dihitung satu", verifikasi={"ekspresi": "0", "hasil": "0"})
mc("c2", "mudah", R, Kn, S3, "Bandingkan 0 kue dan 3 kue. Pernyataan tepat ....", ["0 kue lebih sedikit dari 3 kue", "0 kue lebih banyak dari 3 kue", "keduanya sama banyak", "0 kue lebih besar dari 3"], "A", "Nol selalu bernilai lebih sedikit dari bilangan positif.", "Menganggap nol lebih besar dari angka lain")

# Terarah (4)
mc("c2", "mudah", T, Kn, S1, "Piring tidak berisi kue sama sekali. Lambang bilangannya ....", ["0", "1", "2", "3"], "A", "Piring tanpa kue dilambangkan dengan 0.", verifikasi={"ekspresi": "0", "hasil": "0"})
mc("c2", "mudah", T, Kn, S2, "Posisi angka 0 pada garis bilangan ada di ....", ["paling kiri", "paling kanan", "tengah antara 1 dan 2", "setelah angka 5"], "A", "Angka 0 berada di sebelah paling kiri sebelum 1.")
tf("c2", "mudah", T, Kn, S3, "Nol buah apel lebih banyak daripada tiga apel.", "Salah", "Nol berarti tidak ada apel, jadi lebih sedikit daripada 3.")
sa("c2", "mudah", T, F, S3, "Tulis lambang angka untuk keranjang kosong.", "0|nol", "Keranjang kosong memiliki lambang angka 0.", verifikasi={"ekspresi": "0", "hasil": "0"})

# ── C3 MUDAH (2 soal: 2 terarah) ──────────────────────────────────────────
mc("c3", "mudah", T, Pr, S4, "Langkah awal menulis angka 0 adalah mulai dari ....", ["bagian atas melengkung ke kiri", "bagian bawah ditarik ke atas", "garis lurus tengah", "titik kanan mendatar"], "A", "Menulis angka 0 diawali dari atas melengkung ke kiri lalu memutar.")
tf("c3", "mudah", T, Kn, S3, "Bilangan cacah 0 lebih kecil daripada 1.", "Benar", "Angka 0 bernilai lebih kecil dari 1.")

# ── C3 SEDANG (12 soal: 4 checkpoint, 2 remedial, 6 terarah) ──────────────
mc("c3", "sedang", K, Kn, S1, "Ada 3 burung terbang pergi semua. Burung tersisa ....", ["0", "1", "2", "3"], "A", "Semua burung sudah pergi, maka tersisa 0 burung.", verifikasi={"ekspresi": "3 - 3", "hasil": "0"})
mc("c3", "sedang", K, Kn, S2, "Lengkapi garis bilangan: ..., 1, 2, 3.", ["0", "4", "5", "6"], "A", "Sebelum angka 1 pada garis bilangan adalah angka 0.", verifikasi={"ekspresi": "0", "hasil": "0"})
mc("c3", "sedang", K, Kn, S3, "Perbandingan yang benar antara 5 dan 0 adalah ....", ["5 lebih besar dari 0", "0 lebih besar dari 5", "5 sama dengan 0", "5 lebih kecil dari 0"], "A", "Lima bernilai lebih besar daripada nol.")
tf("c3", "sedang", K, Kn, S4, "Angka 0 berbentuk garis lurus tegak.", "Salah", "Angka 0 berbentuk bulat lonjong melingkar tertutup.")

# Remedial (2)
mc("c3", "sedang", R, Me, S1, "Doni melihat akuarium tanpa ikan sama sekali. Tulis ....", ["0", "1", "10", "2"], "A", "Akuarium tanpa ikan berarti ikannya ada 0 ekor.", "Lupa mencatat kondisi kosong sebagai nol", verifikasi={"ekspresi": "0", "hasil": "0"})
mc("c3", "sedang", R, Me, S2, "Lina mulai melangkah dari angka 1 di garis bilangan. Seharusnya ....", ["mulai dari titik 0", "mulai dari titik 2", "mulai dari angka 10", "bebas dari mana saja"], "A", "Mengukur jarak langkah harus dimulai dari titik 0.", "Mengabaikan titik nol saat melangkah")

# Terarah (6)
mc("c3", "sedang", T, Kn, S1, "Kandang ayam kosong tanpa ayam. Jumlah ayam ....", ["0", "1", "2", "3"], "A", "Kandang kosong berarti berisi 0 ekor ayam.", verifikasi={"ekspresi": "0", "hasil": "0"})
mc("c3", "sedang", T, Kn, S2, "Bila belum melangkah sama sekali, jarak langkahnya ....", ["0", "1", "2", "10"], "A", "Belum melangkah berarti nilainya 0 langkah.", verifikasi={"ekspresi": "0", "hasil": "0"})
mc("c3", "sedang", T, Pr, S3, "Bilangan terkecil dari urutan 2, 0, 1 adalah ....", ["0", "1", "2", "3"], "A", "Bilangan paling kecil adalah 0.", verifikasi={"ekspresi": "0", "hasil": "0"})
mc("c3", "sedang", T, Pr, S4, "Bila lingkaran angka 0 terbuka di samping, itu ....", ["belum selesai ditulis", "sudah benar", "angka satu", "angka sepuluh"], "A", "Angka 0 harus tersambung rapat melingkar.")
tf("c3", "sedang", T, Kn, S2, "Jarak dari 0 ke 1 adalah satu langkah.", "Benar", "Satu loncatan dari 0 menuju 1 bernilai satu.")
sa("c3", "sedang", T, F, S1, "Bila semua balon meletus, sisa balon ....", "0|nol", "Semua meletus berarti tersisa 0 balon.", verifikasi={"ekspresi": "0", "hasil": "0"})

# ── C4 SEDANG (10 soal: 3 checkpoint, 7 terarah) ───────────────────────────
mc("c4", "sedang", K, Kn, S1, "Toples A ada 4 permen, toples B kosong. Toples B ....", ["0", "4", "1", "2"], "A", "Toples kosong berarti berisi 0 permen.", verifikasi={"ekspresi": "0", "hasil": "0"})
mc("c4", "sedang", K, Kn, S3, "Manakah pernyataan yang paling tepat?", ["0 lebih kecil dari semua bilangan cacah lain", "0 lebih besar dari 1", "0 sama banyak dengan 1", "0 kue lebih banyak dari 2 kue"], "A", "Nol adalah bilangan cacah terkecil.")
tf("c4", "sedang", K, Kn, S2, "Pada mistar ukur, angka 10 menjadi titik awal.", "Salah", "Pengukuran panjang selalu dimulai dari garis angka 0.")

# Terarah (7)
mc("c4", "sedang", T, Kn, S1, "Ali makan 2 biskuit sampai habis. Sisa biskuit Ali ....", ["0", "1", "2", "3"], "A", "Biskuit habis berarti tersisa 0.", verifikasi={"ekspresi": "2 - 2", "hasil": "0"})
mc("c4", "sedang", T, Kn, S2, "Angka berapakah yang berada tepat sebelum 1?", ["0", "2", "3", "5"], "A", "Tepat sebelum angka 1 adalah angka 0.", verifikasi={"ekspresi": "1 - 1", "hasil": "0"})
mc("c4", "sedang", T, Pr, S3, "Setelah angka 1, hitungan mundur berakhir di angka ....", ["0", "2", "3", "4"], "A", "Hitungan mundur menuju nol berakhir di angka 0.", verifikasi={"ekspresi": "1 - 1", "hasil": "0"})
mc("c4", "sedang", T, Pr, S4, "Perbedaan bentuk angka 0 dan huruf O adalah ....", ["angka 0 lebih lonjong ramping", "angka 0 punya garis silang", "angka 0 berbentuk segitiga", "tidak ada bedanya"], "A", "Angka 0 umumnya dibuat lebih lonjong dan ramping.")
tf("c4", "sedang", T, Pr, S1, "Piring kosong dapat ditulis dengan lambang bilangan 0.", "Benar", "Ketiadaan benda ditulis dengan angka 0.")
tf("c4", "sedang", T, Kn, S3, "Nol buku lebih banyak daripada sepuluh buku.", "Salah", "Nol buku berarti tidak ada buku sama sekali.")
sa("c4", "sedang", T, Pr, S2, "Berapa langkah dari angka 0 ke angka 2?", "2|dua", "Dari 0 ke 2 berjarak dua langkah loncatan.", verifikasi={"ekspresi": "2 - 0", "hasil": "2"})

# ── C5 SEDANG (3 soal: 3 checkpoint) ──────────────────────────────────────
mc("c5", "sedang", K, Me, S1, "Rudi mengira piring kosong tidak perlu angka. Penjelasan tepat ....", ["piring kosong ditulis angka 0", "piring kosong ditulis angka 1", "piring kosong tidak punya lambang", "piring kosong bernilai 10"], "A", "Dalam matematika, ketiadaan benda dilambangkan dengan angka 0.")
mc("c5", "sedang", K, Kn, S3, "Bilangan paling kecil di antara 4, 0, 2 adalah ....", ["0", "2", "4", "1"], "A", "Nol adalah bilangan terkecil di antara 4, 0, 2.", verifikasi={"ekspresi": "0", "hasil": "0"})
mc("c5", "sedang", K, Me, S2, "Mengapa garis bilangan dimulai dari 0?", ["karena 0 menunjukkan belum ada langkah", "karena 0 angka terbesar", "karena 0 sama dengan angka 10", "agar garis terlihat panjang"], "A", "Titik nol menjadi penanda belum adanya jarak atau pergerakan.")

# ── C3 SULIT (2 soal: 2 mandiri) ──────────────────────────────────────────
mc("c3", "sulit", X, Kn, S2, "Di antara bilangan 0, 5, 2, 8, yang paling kecil ....", ["0", "2", "5", "8"], "A", "Angka 0 adalah yang paling kecil.", verifikasi={"ekspresi": "0", "hasil": "0"})
sa("c3", "sulit", X, F, S4, "Tuliskan lambang bilangan nol.", "0", "Lambang bilangan nol ditulis 0.", verifikasi={"ekspresi": "0", "hasil": "0"})

# ── C4 SULIT (3 soal: 3 mandiri) ──────────────────────────────────────────
mc("c4", "sulit", X, Kn, S1, "Pohon tidak berbuah sama sekali. Banyak buahnya ....", ["0", "1", "2", "10"], "A", "Tidak berbuah sama sekali berarti ada 0 buah jambu.", verifikasi={"ekspresi": "0", "hasil": "0"})
mc("c4", "sulit", X, Kn, S3, "Angka pertama pada garis bilangan dari terkecil adalah ....", ["0", "1", "2", "3"], "A", "Urutan dari nilai terkecil diawali angka 0.", verifikasi={"ekspresi": "0", "hasil": "0"})
tf("c4", "sulit", X, Me, S2, "Mulai mengukur dari angka 0 menghasilkan ukuran yang tepat.", "Benar", "Titik awal pengukuran benda harus tepat di angka 0.")

# ── C5 SULIT (3 soal: 3 mandiri) ──────────────────────────────────────────
mc("c5", "sulit", X, Me, S1, "Lima permen Edo habis dibagikan. Sisa permen Edo ....", ["0", "1", "5", "10"], "A", "Semua permen habis dibagikan sehingga tersisa 0 permen.", verifikasi={"ekspresi": "5 - 5", "hasil": "0"})
mc("c5", "sulit", X, Kn, S3, "Pernyataan mana yang salah mengenai angka nol?", ["angka 0 lebih besar dari angka 1", "angka 0 melambangkan kosong", "angka 0 berada sebelum angka 1", "angka 0 adalah bilangan cacah"], "A", "Pernyataan angka 0 lebih besar dari 1 adalah keliru.")
mc("c5", "sulit", X, Me, S4, "Siti menulis angka 0 mirip garis lurus 1. Nasihat tepat ....", ["buat garis melengkung lonjong tertutup", "tambahkan ekor di bawah", "buat dua titik terpisah", "putar kertas ke samping"], "A", "Angka 0 harus bulat lonjong melingkar, bukan garis tegak.")

# ── C6 SULIT (2 soal: 2 pengayaan) ────────────────────────────────────────
mc("c6", "sulit", P, Kn, S1, "Rancang simbol rambu parkir kosong di sekolah ....", ["gambar mobil dengan tanda angka 0", "gambar mobil penuh warna", "tulis kata jalan terus", "gambar 10 motor"], "A", "Tanda angka 0 dengan mobil memperjelas bahwa tidak ada mobil terparkir.")
mc("c6", "sulit", P, Pr, S2, "Rancang garis lompat angka di lantai kelas ....", ["beri tanda kotak mulai dari angka 0 ke 10", "acak angka dari 10 ke 0 di lantai", "tulis angka 1 tanpa titik mulai", "buat garis lurus tanpa angka"], "A", "Menandai kotak mulai dari 0 ke 10 memudahkan siswa bermain lompat angka.")

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

uid = lambda i: str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab5_soal_{i}"))
groups = {"mc": [], "tf": [], "sa": []}

random.seed(45)
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
    ("Apa Itu Angka Nol?", S1),
    ("Nol pada Garis Bilangan", S2),
    ("Membandingkan dengan Nol", S3),
    ("Menulis Angka Nol", S4)
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
    (S1, "Aku memahami makna nol sebagai kondisi kosong tanpa benda.", "Apa Itu Angka Nol?",
f"""Lihat piring di atas meja.
Ada dua kue di piring.
Adik memakan semua kue.
Sekarang tidak ada kue tersisa.
Piring itu sudah kosong.
Kosong artinya tidak ada benda.
Kita melambangkannya dengan angka 0.
Angka 0 dibaca nol.

:::definition
term: Bilangan Nol
definition: Bilangan untuk menyatakan tidak ada benda atau kosong.
:::

:::callout
variant: tip
title: Ingat ya
text: Tidak ada benda ditulis dengan angka 0.
:::""", 3),

    (S2, "Aku dapat menentukan letak angka nol pada garis bilangan.", "Nol pada Garis Bilangan",
f"""Perhatikan garis bilangan ini.
Mulai membilang dari angka 0.
Lalu maju ke angka 1.
Lalu 2, 3, dan seterusnya.
Angka 0 ada sebelum 1.
Nol berada paling kiri.
Saat belum melangkah, nilainya nol.

:::table
headers: ["Posisi","Lambang","Arti"]
rows: [["titik awal.","0.","belum melangkah."],["satu langkah.","1.","maju satu langkah."]]
caption: Posisi Nol pada Garis Bilangan
:::""", 4),

    (S3, "Aku bisa membandingkan jumlah benda dengan nol.", "Membandingkan dengan Nol",
f"""Mari bandingkan benda dengan nol.
Ada keranjang berisi 3 apel.
Ada keranjang kosong tanpa apel.
Keranjang kosong bernilai 0 apel.
Tiga apel lebih banyak dari 0.
Nol selalu bernilai paling sedikit.
Angka 0 lebih kecil dari 1.

:::steps
title: Cara membandingkan dengan nol
items: ["Cek apakah ada benda di tempatnya.","Bila kosong beri nilai 0.","Benda yang ada pasti lebih banyak dari 0."]
:::""", 4),

    (S4, "Aku bisa menulis lambang angka nol dengan rapi.", "Menulis Angka Nol",
f"""Menulis angka 0 sangat mudah.
Bentuk angka 0 bulat lonjong.
Mulai goresan dari atas.
Putar melingkar ke bawah.
Lalu sambungkan kembali ke atas.
Tulis angka 0 dengan rapi.

:::common_trap
term: Menghitung Benda Dua Kali atau Terlewat
explanation: Bila toples kosong, jangan sebut satu. Tulis angka 0 karena tidak ada benda.
:::

:::callout
variant: summary
title: Ringkasan
text: Nol berarti tidak ada benda. Lambang angka nol ditulis 0.
:::""", 3),
]

lp = {
    "level": "Kelas 1 SD — Fase A",
    "title": "Nol sebagai Tidak Ada Benda",
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab5.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"lesson_plan": lp, "quiz_config": quiz}, f, ensure_ascii=False, indent=2)

print("BERHASIL:", out_path, "berhasil dibuat dan divalidasi!")
