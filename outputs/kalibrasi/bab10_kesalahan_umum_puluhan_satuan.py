#!/usr/bin/env python3
"""
Generator dan validator Bab 10 Matematika Kelas 1 SD:
"Kesalahan Umum: Puluhan dan Satuan Tertukar" (Fase A)
bab_id: fd0e4d90-dcd7-4825-90fe-e3af6218a0bc
article_id: 1594127c-7891-4e5c-9874-38585bd2ca23
quiz_id: d0b8f55b-bf3f-44bb-8b29-78e9d34055d2
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "a0b9c89d1e01"  # Bahaya Angka Tertukar
S2 = "b1c0d90e2f12"  # Membaca Angka Terbalik
S3 = "c2d1e01f3a23"  # Strategi Kotak Nilai Tempat
S4 = "d3e2f12a4b34"  # Mengecek Ulang Tulisan Angka

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Kesalahan paling sering adalah angka tertukar.
Contohnya menulis tiga puluh dua.
Harusnya ditulis 32.
Tetapi anak menulis 23.
Angka 32 dan 23 sangat berbeda.
32 nilainya tiga puluhan.
23 nilainya hanya dua puluhan.
Jangan sampai tertukar kamar angkanya."""

s2_content = """Ada juga kesalahan saat membaca.
Mata membaca dari kanan ke kiri.
Angka 41 dibaca empat belas.
Itu adalah bacaan yang salah.
Angka 41 dibaca empat puluh satu.
Angka 14 baru empat belas.
Selalu baca dari angka kiri.
Kiri puluhan, kanan satuan."""

s3_content = """Gunakan cara kotak nilai tempat.
Buat dua kotak berdampingan.
Kotak kiri bertuliskan puluhan.
Kotak kanan bertuliskan satuan.
Tiga puluh tujuh?
Taruh 3 di kotak puluhan.
Taruh 7 di kotak satuan.
Hasilnya pasti tepat 37.

:::steps
1. Buat kotak puluhan di kiri dan satuan di kanan.
2. Tulis angka puluhan terlebih dahulu.
3. Tulis angka satuan di sebelahnya.
:::"""

s4_content = """Selalu periksa ulang angka tulisanmu.
Dengarkan kata puluhan di depan.
Pastikan angka kiri sudah cocok.
Ketelitian membuat nilaimu sempurna.

:::common_trap
title: Menulis Angka Sesuai Urutan Tangan Tanpa Berpikir
Jangan terburu-buru menulis angka.
Ingat selalu angka kiri adalah puluhan.
Angka kanan adalah satuan.
Ucapkan kembali bilangannya untuk memastikan.
:::

:::callout
variant: summary
title: Ringkasan
text: Puluhan di kiri dan satuan di kanan. Jangan tertukar posisinya. Cek ulang sebelum selesai.
:::"""

sections = [
    {
        "id": S1,
        "title": "Bahaya Angka Tertukar",
        "minutes": 6,
        "goal": "Siswa dapat mengenali kesalahan saat angka puluhan dan satuan tertukar serta akibatnya.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Membaca Angka Terbalik",
        "minutes": 6,
        "goal": "Siswa dapat menghindari membaca bilangan terbalik dari kanan ke kiri.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Strategi Kotak Nilai Tempat",
        "minutes": 6,
        "goal": "Siswa dapat menggunakan tabel atau kotak puluhan-satuan untuk mencegah kesalahan posisi.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Mengecek Ulang Tulisan Angka",
        "minutes": 6,
        "goal": "Siswa memiliki kebiasaan metakognitif untuk mencocokkan kata puluhan dengan angka depan.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Puluhan dan Satuan Tertukar",
    "topic": "Bilangan sampai 100 dan Nilai Tempat",
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
# 2. DEFINISI BANK 50 SOAL BAB 10
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
mc("c1", "mudah", D, F, S1, "Angka 32 dan 23 memiliki nilai yang ....", ["berbeda", "sama", "mirip", "kembar"], "A", "32 bernilai tiga puluh dua, 23 bernilai dua puluh tiga.")
tf("c1", "mudah", D, F, S2, "Angka 41 dibaca empat belas.", "Salah", "Angka 41 dibaca empat puluh satu. Empat belas adalah 14.")

# Terarah (3): S1, S2, S4
mc("c1", "mudah", T, F, S1, "Menulis tiga puluh dua yang benar adalah ....", ["32", "23", "302", "30"], "A", "Tiga puluh dua ditulis 32.", verifikasi={"ekspresi": "30 + 2", "hasil": "32"})
mc("c1", "mudah", T, F, S2, "Angka 14 dibaca ....", ["empat belas", "empat puluh satu", "empat puluh", "satu empat"], "A", "Angka 14 dibaca empat belas.")
sa("c1", "mudah", T, F, S4, "Berapakah nilai puluhan pada angka 41?", "40|empat puluh", "Angka 4 menempati puluhan bernilai 40.", verifikasi={"ekspresi": "4 * 10", "hasil": "40"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S3, "Pada kotak nilai tempat, puluhan ditaruh di sebelah ....", ["kiri", "kanan", "tengah", "bawah"], "A", "Kotak puluhan berada di sebelah kiri.")
tf("c2", "mudah", D, Kn, S1, "Angka 51 lebih besar daripada 15.", "Benar", "51 bernilai lima puluhan sedangkan 15 bernilai satu puluhan.")

# Remedial (2)
mc("c2", "mudah", R, Pr, S1, "Budi ingin menulis dua puluh lima, tapi menulis 52. Cara memperbaikinya?", ["tulis angka 2 di depan angka 5", "tambah angka nol", "balik kertasnya", "biarkan saja"], "A", "Dua puluh lima diawali angka 2, jadi 25.", "Menulis angka terbalik dari satuan baru puluhan")
mc("c2", "mudah", R, Kn, S2, "Siti membaca 31 sebagai tiga belas. Kesalahan Siti adalah ....", ["membaca dari kanan ke kiri", "lupa membaca angka 1", "salah menyebut angka", "sudah benar"], "A", "Siti membaca dari kanan. Seharusnya dibaca dari kiri yaitu tiga puluh satu.", "Membaca urutan angka terbalik")

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Bilangan manakah yang bernilai paling kecil?", ["18", "81", "80", "88"], "A", "18 hanya memiliki satu puluhan, jadi paling kecil.", verifikasi={"ekspresi": "10 + 8", "hasil": "18"})
mc("c2", "mudah", T, Kn, S3, "Berapakah hasil dari 4 puluhan ditambah 7 satuan?", ["47", "74", "407", "11"], "A", "4 puluhan (40) dan 7 satuan (7) menjadi 47.", verifikasi={"ekspresi": "40 + 7", "hasil": "47"})
tf("c2", "mudah", T, Kn, S2, "Angka 52 dibaca dua puluh lima.", "Salah", "Angka 52 dibaca lima puluh dua.")
sa("c2", "mudah", T, F, S4, "Tulis angka yang benar untuk tujuh puluh empat!", "74|tujuh puluh empat", "Tujuh puluh empat ditulis 74 bukan 47.", verifikasi={"ekspresi": "70 + 4", "hasil": "74"})

# ── C3 MUDAH (2 soal: 2 terarah) ──────────────────────────────────────────
# Terarah (2): S1, S3
mc("c3", "mudah", T, Pr, S1, "Berapakah selisih nilai angka jika 91 tertukar menjadi 19?", ["72", "80", "19", "91"], "A", "91 - 19 = 72.", verifikasi={"ekspresi": "91 - 19", "hasil": "72"})
sa("c3", "mudah", T, Pr, S3, "Jika 3 ditaruh di puluhan dan 7 di satuan, bilangan itu adalah ....", "37|tiga puluh tujuh", "3 puluhan dan 7 satuan menjadi 37.", verifikasi={"ekspresi": "30 + 7", "hasil": "37"})

# ── C3 SEDANG (12 soal: 4 checkpoint, 2 remedial, 6 terarah) ──────────────
# Checkpoint akhir (4)
mc("c3", "sedang", K, Pr, S1, "Berapakah selisih nilai angka 32 dan 23?", ["9", "10", "1", "12"], "A", "32 dikurangi 23 sama dengan 9.", verifikasi={"ekspresi": "32 - 23", "hasil": "9"})
mc("c3", "sedang", K, Pr, S2, "Berapakah nilai puluhan pada angka 61?", ["60", "6", "1", "16"], "A", "Nilai tempat 6 di depan adalah 60.", verifikasi={"ekspresi": "6 * 10", "hasil": "60"})
tf("c3", "sedang", K, Kn, S3, "Kotak puluhan selalu diisi angka pertama dari kiri.", "Benar", "Angka pertama dari kiri adalah puluhan.")
tf("c3", "sedang", K, Pr, S4, "Memeriksa ulang angka tulisan tidak diperlukan jika sudah cepat.", "Salah", "Memeriksa ulang sangat penting untuk menghindari kesalahan.")

# Remedial (2)
mc("c3", "sedang", R, Pr, S3, "Dono mengisi kotak nilai tempat untuk 58: puluhan diisi 8, satuan diisi 5. Dono salah karena ....", ["tertukar posisi puluhan dan satuan", "kotak puluhan kurang", "nilainya terlalu besar", "sudah benar"], "A", "Puluhan adalah 5 dan satuan adalah 8, Dono menaruhnya terbalik.", "Salah menempatkan angka pada tabel nilai tempat")
mc("c3", "sedang", R, Kn, S4, "Sebelum mengumpulkan tugas menulis angka 71, apa yang harus dicegah?", ["jangan tertukar dengan angka 17", "jangan menulis angka 7", "jangan menghapus angka", "tidak ada"], "A", "Pastikan tidak tertukar antara 71 dan 17.", "Membaca angka belasan tertukar dengan puluhan")

# Terarah (6): S1, S2, S2, S3, S3, S4
mc("c3", "sedang", T, Pr, S1, "Berapakah selisih antara 42 dan 24?", ["18", "16", "20", "8"], "A", "42 dikurangi 24 sama dengan 18.", verifikasi={"ekspresi": "42 - 24", "hasil": "18"})
mc("c3", "sedang", T, Pr, S2, "Berapakah selisih nilai antara 71 dan 17?", ["54", "50", "44", "40"], "A", "71 dikurangi 17 sama dengan 54.", verifikasi={"ekspresi": "71 - 17", "hasil": "54"})
mc("c3", "sedang", T, Pr, S2, "Berapakah nilai puluhan pada angka 82?", ["80", "8", "2", "20"], "A", "8 di posisi puluhan bernilai 80.", verifikasi={"ekspresi": "8 * 10", "hasil": "80"})
mc("c3", "sedang", T, Pr, S3, "Tulis angka dengan 5 di puluhan dan 3 di satuan!", ["53", "35", "503", "8"], "A", "5 puluhan dan 3 satuan membentuk 53.", verifikasi={"ekspresi": "50 + 3", "hasil": "53"})
tf("c3", "sedang", T, Kn, S3, "Angka 63 terdiri dari 6 puluhan dan 3 satuan.", "Benar", "63 = 6 puluhan + 3 satuan.")
sa("c3", "sedang", T, Pr, S4, "Berapakah selisih nilai jika angka 53 tertukar menjadi 35?", "18|delapan belas", "53 dikurangi 35 sama dengan 18.", verifikasi={"ekspresi": "53 - 35", "hasil": "18"})

# ── C4 SEDANG (13 soal: 2 checkpoint, 4 mandiri, 7 terarah) ──────────────
# Checkpoint akhir (2)
mc("c4", "sedang", K, Kn, S1, "Berapakah selisih nilai puluhan antara 72 dan 27?", ["50", "70", "20", "5"], "A", "70 dikurangi 20 sama dengan 50.", verifikasi={"ekspresi": "70 - 20", "hasil": "50"})
tf("c4", "sedang", K, Kn, S2, "Angka 91 dan 19 memiliki jumlah puluhan yang sama.", "Salah", "91 punya 9 puluhan sedangkan 19 hanya 1 puluhan.")

# Mandiri (4)
mc("c4", "sedang", X, Kn, S1, "Berapakah selisih bilangan 63 jika angkanya tertukar menjadi 36?", ["27", "30", "17", "20"], "A", "63 dikurangi 36 sama dengan 27.", verifikasi={"ekspresi": "63 - 36", "hasil": "27"})
mc("c4", "sedang", X, Kn, S2, "Jika kamu ingin membeli 81 kelereng, jangan sebut delapan belas karena kamu akan dapat ....", ["18 kelereng", "81 kelereng", "80 kelereng", "8 kelereng"], "A", "Delapan belas hanya 18, jauh lebih sedikit dari 81.", verifikasi={"ekspresi": "18", "hasil": "18"})
mc("c4", "sedang", X, Kn, S3, "Pada bilangan 49, angka yang harus dimasukkan ke kotak satuan adalah ....", ["9", "4", "40", "90"], "A", "Angka 9 di kanan adalah satuan.", verifikasi={"ekspresi": "49 % 10", "hasil": "9"})
sa("c4", "sedang", X, Pr, S4, "Berapakah selisih nilai antara 82 dan 28?", "54|lima puluh empat", "82 dikurangi 28 sama dengan 54.", verifikasi={"ekspresi": "82 - 28", "hasil": "54"})

# Terarah (7): S1, S1, S2, S2, S3, S3, S4
mc("c4", "sedang", T, Kn, S1, "Manakah bilangan yang akan berkurang paling banyak jika angkanya tertukar?", ["82", "34", "56", "23"], "A", "82 menjadi 28 berkurang 54, paling banyak.")
tf("c4", "sedang", T, Kn, S1, "Pada bilangan dua angka yang tidak kembar, menukar posisi angka selalu mengubah nilainya.", "Benar", "Posisi puluhan dan satuan yang ditukar pada bilangan tidak kembar pasti menghasilkan nilai berbeda.")
mc("c4", "sedang", T, Kn, S2, "Berapakah nilai puluhan pada angka 92?", ["90", "9", "2", "20"], "A", "Angka 9 di depan bernilai 90.", verifikasi={"ekspresi": "9 * 10", "hasil": "90"})
tf("c4", "sedang", T, Kn, S2, "Angka 34 dibaca empat puluh tiga.", "Salah", "Angka 34 dibaca tiga puluh empat.")
mc("c4", "sedang", T, Kn, S3, "Dua anak mengisi kotak nilai tempat untuk angka 65. Siapakah yang benar?", ["Anak A: 6 puluhan dan 5 satuan", "Anak B: 5 puluhan dan 6 satuan", "Keduanya benar", "Keduanya salah"], "A", "65 terdiri dari 6 puluhan dan 5 satuan.")
tf("c4", "sedang", T, Me, S3, "Kotak nilai tempat membantu mata kita tidak salah letak.", "Benar", "Kotak memberi pemisah yang jelas antara puluhan dan satuan.")
mc("c4", "sedang", T, Me, S4, "Langkah terbaik mengecek tulisan lambang bilangan adalah ....", ["baca kembali dari kiri dan cocokkan artinya", "tutup buku langsung", "menghapus semua angka", "mengganti warnanya"], "A", "Membaca kembali dari kiri memastikan angka depan sudah sesuai puluhan.")

# ── C5 SULIT (6 soal: 2 checkpoint, 4 mandiri) ───────────────────────────
# Checkpoint akhir (2)
mc("c5", "sulit", K, Me, S1, "Berapakah kerugian pembeli jika harga barang 49 terbayar 94?", ["45", "55", "35", "50"], "A", "94 dikurangi 49 sama dengan 45.", verifikasi={"ekspresi": "94 - 49", "hasil": "45"})
mc("c5", "sulit", K, Me, S4, "Saat guru mendiktekan enam puluh dua, Toni menulis 26. Apa saran untuk Toni?", ["dengar kata enam puluh di awal lalu tulis 6", "tulis 2 di depan", "abaikan kata puluh", "tulis angka 0"], "A", "Kata puluhan di awal menandakan angka depannya adalah 6.")

# Mandiri (4)
mc("c5", "sulit", X, Kn, S1, "Bilangan dua angka berapakah yang selisih dengan kebalikannya adalah 27?", ["74", "50", "20", "11"], "A", "74 jika dibalik menjadi 47. Selisih 74 - 47 = 27.")
mc("c5", "sulit", X, Me, S2, "Mengapa orang sering tertukar antara belasan dan puluhan saat membaca?", ["karena keduanya menggunakan angka yang mirip tetapi letaknya berbeda", "karena warnanya sama", "karena tidak ada artinya", "hanya kebetulan"], "A", "Angka 1 di depan berarti belasan, sedangkan di belakang berarti satuan.")
mc("c5", "sulit", X, Kn, S3, "Jika kotak puluhan diisi 8 dan kotak satuan diisi 2, bilangannya adalah ....", ["82", "28", "802", "10"], "A", "8 puluhan dan 2 satuan membentuk bilangan 82.", verifikasi={"ekspresi": "80 + 2", "hasil": "82"})
mc("c5", "sulit", X, Kn, S4, "Manakah bilangan yang nilainya TIDAK berubah meskipun angkanya tertukar?", ["66", "65", "64", "60"], "A", "Pada 66, kedua angkanya sama sehingga jika dibalik tetap 66.")

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ──────────────────────────
# Checkpoint akhir (2)
mc("c6", "sulit", K, Me, S3, "Rancanglah poster sederhana untuk mengingatkan teman agar tidak tertukar angka puluhan!", ["Tulis: Puluhan di Kiri, Satuan di Kanan!", "Tulis: Baca Sembarangan Saja!", "Tulis: Angka Belakang Dulu!", "Tulis: Tidak Usah Belajar!"], "A", "Slogan yang tepat dan mudah diingat anak kelas 1.")
mc("c6", "sulit", K, Kn, S4, "Buatlah aturan untuk membedakan bilangan puluhan dan kebalikannya!", ["lihat selalu angka di posisi puluhan terlebih dahulu", "lihat angka yang paling kecil", "tebak yang paling panjang", "tidak perlu aturan"], "A", "Membandingkan angka depan (puluhan) adalah aturan paling pasti.")

# Pengayaan (2)
mc("c6", "sulit", P, Me, S1, "Analisis akibat fatal jika nomor rumah 92 tertukar dengan 29 bagi kurir paket!", ["paket akan diantar ke rumah yang salah dan sangat jauh", "paket tetap sampai", "tidak ada pengaruhnya", "kurir makin cepat sampai"], "A", "Nomor rumah yang tertukar menyebabkan salah alamat pengiriman.")
mc("c6", "sulit", P, Pr, S1, "Temukan bilangan antara 60 dan 70 yang jika angkanya tertukar berkurang sebanyak 36!", ["62", "64", "68", "61"], "A", "62 jika ditukar menjadi 26. Selisih 62 - 26 = 36.")

# ==========================================
# 3. VERIFIKASI & GENERASI STRUKTUR APLIKASI
# ==========================================
assert len(Q) == 50, f"Total soal: {len(Q)} != 50"

mc_list, tf_list, sa_list = [], [], []

for i, q in enumerate(Q, 1):
    tax = {
        "bloom": q["b"],
        "difficulty": q["d"],
        "fungsi": q["f"],
        "knowledge_dimension": q["dim"]
    }
    if q.get("m"):
        tax["miskonsepsi_target"] = q["m"]

    # Deterministic UUID5
    u = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab10_soal_{i}"))

    base = {
        "uid": u,
        "number": i,
        "taxonomy": tax,
        "source_section_id": q["s"],
        "explanation": q["ex"]
    }
    if q.get("verifikasi"):
        base["verifikasi"] = q["verifikasi"]

    if q["t"] == "mc":
        opts = list(q["opts"])
        correct_text = opts[0]
        random.shuffle(opts)
        choices = [{"label": L, "text": opt} for L, opt in zip(["A", "B", "C", "D"], opts)]
        ans_label = next(c["label"] for c in choices if c["text"] == correct_text)
        base["stem"] = q["stem"]
        base["choices"] = choices
        base["answer"] = ans_label
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab10.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
