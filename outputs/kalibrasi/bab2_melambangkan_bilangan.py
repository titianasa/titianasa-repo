#!/usr/bin/env python3
"""
Generator dan validator Bab 2 Matematika Kelas 1 SD:
"Melambangkan Bilangan 1 sampai 10" (Fase A)
bab_id: fa425867-778c-4f4f-a616-bb190f43bf54
article_id: 2e842292-566a-4a20-bc3d-741859e23f07
quiz_id: 3f161919-d418-4aeb-adb9-30cf17b3131c
"""
import json, uuid, random, re, os
from collections import Counter

random.seed(42)
S1, S2, S3, S4 = "a2b1c09d3e51", "b3c2d10e4f62", "c4d3e21f5a73", "d5e4f32a6b84"

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
mc("c1", "mudah", D, F, S1, "Lambang bilangan tiga adalah ....", ["3", "2", "4", "5"], "A", "Tiga dilambangkan dengan angka 3.", verifikasi={"ekspresi": "3", "hasil": "3"})
tf("c1", "mudah", D, F, S1, "Angka 1 adalah lambang bilangan lima.", "Salah", "Angka 1 adalah lambang bilangan satu, bukan lima.")
mc("c1", "mudah", T, F, S1, "Lambang bilangan lima adalah ....", ["5", "3", "4", "2"], "A", "Lima dilambangkan dengan angka 5.", verifikasi={"ekspresi": "5", "hasil": "5"})
mc("c1", "mudah", T, F, S2, "Lambang bilangan delapan adalah ....", ["8", "7", "9", "6"], "A", "Delapan dilambangkan dengan angka 8.", verifikasi={"ekspresi": "8", "hasil": "8"})
sa("c1", "mudah", T, F, S2, "Tulis lambang bilangan tujuh.", "7|tujuh", "Tujuh ditulis dengan angka 7.", verifikasi={"ekspresi": "7", "hasil": "7"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
mc("c2", "mudah", D, Kn, S3, "Arti lambang bilangan adalah ....", ["tanda angka untuk banyak benda", "nama huruf pada buku", "gambar benda bergerak", "warna pada kertas"], "A", "Lambang bilangan adalah tanda angka untuk menunjukkan banyak benda.")
tf("c2", "mudah", D, Kn, S3, "Kata 'empat' adalah nama bilangan.", "Benar", "Empat adalah nama bilangan, sedangkan 4 adalah lambangnya.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S4, "Angka ini 6. Dibaca apa?", ["enam", "sembilan", "delapan", "tujuh"], "A", "Angka 6 memiliki lingkaran di bawah, dibaca enam.", "Angka 6 dan 9 tertukar karena bentuk terbalik")
mc("c2", "mudah", R, Kn, S4, "Angka ini 9. Lingkarannya di mana?", ["di bagian atas", "di bagian bawah", "di sebelah kiri", "di tengah-tengah"], "A", "Angka 9 memiliki lingkaran di bagian atas.", "Salah mengenali posisi lengkung angka 9")

# Terarah (4)
mc("c2", "mudah", T, Kn, S1, f"Lambang bilangan untuk {e('🍎', 4)} adalah ....", ["4", "3", "5", "2"], "A", "Ada 4 apel, lambang bilangannya adalah angka 4.", verifikasi={"ekspresi": "4", "hasil": "4"})
mc("c2", "mudah", T, Kn, S2, f"Lambang bilangan untuk {e('⭐', 7)} adalah ....", ["7", "6", "8", "9"], "A", "Ada 7 bintang, lambang bilangannya adalah angka 7.", verifikasi={"ekspresi": "7", "hasil": "7"})
tf("c2", "mudah", T, Kn, S3, "Angka 10 terdiri dari angka 2 dan 0.", "Salah", "Angka 10 terdiri dari angka 1 dan 0.")
sa("c2", "mudah", T, F, S1, f"Tulis lambang bilangan untuk {e('🚗', 2)}.", "2|dua", "Ada 2 mobil, lambang bilangannya 2.", verifikasi={"ekspresi": "2", "hasil": "2"})

# ── C3 MUDAH (2 soal: 2 terarah) ──────────────────────────────────────────
mc("c3", "mudah", T, Pr, S4, "Saat menulis angka 1, mulai dari ....", ["atas ditarik ke bawah", "bawah ditarik ke atas", "kanan ke kiri", "tengah memutar"], "A", "Menulis angka 1 dimulai dari atas lurus ke bawah.")
mc("c3", "mudah", T, Kn, S3, "Nama bilangan 'sembilan' lambangnya ....", ["9", "6", "8", "7"], "A", "Nama bilangan sembilan memiliki lambang angka 9.", verifikasi={"ekspresi": "9", "hasil": "9"})

# ── C3 SEDANG (12 soal: 4 checkpoint, 2 remedial, 6 terarah) ──────────────
mc("c3", "sedang", K, Kn, S1, "Urutan lambang bilangan dari yang terkecil adalah ....", ["1, 2, 3, 4", "1, 3, 2, 4", "4, 2, 3, 1", "2, 1, 4, 3"], "A", "Urutan maju dari yang terkecil adalah 1, 2, 3, 4.")
mc("c3", "sedang", K, Kn, S2, "Urutan lambang bilangan setelah 6 adalah ....", ["7, 8, 9, 10", "8, 7, 9, 10", "6, 7, 9, 8", "10, 9, 8, 7"], "A", "Setelah angka 6 adalah 7, 8, 9, dan 10.")
mc("c3", "sedang", K, Kn, S3, "Pasangan nama dan lambang yang benar ....", ["delapan pasangannya 8", "enam pasangannya 9", "tiga pasangannya 5", "tujuh pasangannya 1"], "A", "Nama delapan berpasangan dengan lambang angka 8.")
tf("c3", "sedang", K, Kn, S2, "Angka 6 dan angka 9 bentuknya terbalik.", "Benar", "Angka 6 lengkungnya di bawah, sedangkan angka 9 lengkungnya di atas.")

# Remedial (2)
mc("c3", "sedang", R, Me, S3, "Budi menulis 'dua' dengan angka 5. Yang benar ....", ["angka 2", "angka 3", "angka 4", "angka 1"], "A", "Nama bilangan dua dilambangkan dengan angka 2, bukan 5.", "Tertukar lambang bilangan", verifikasi={"ekspresi": "2", "hasil": "2"})
mc("c3", "sedang", R, Me, S4, "Siti menulis angka 6 mirip angka 9. Agar benar ....", ["letakkan lingkaran di bawah", "putar kertas ke samping", "tambahkan garis silang", "hapus ekornya"], "A", "Angka 6 memiliki lingkaran di bagian bawah.", "Salah orientasi atas bawah pada angka 6 dan 9")

# Terarah (6)
mc("c3", "sedang", T, Kn, S1, f"Banyak {e('🐱', 5)}. Lambang bilangannya ....", ["5", "4", "3", "6"], "A", "Ada 5 kucing, lambangnya adalah angka 5.", verifikasi={"ekspresi": "5", "hasil": "5"})
mc("c3", "sedang", T, Pr, S4, "Saat menulis angka 8, kita membuat ....", ["dua lingkaran bersambung", "tiga garis lurus", "satu garis miring", "satu titik besar"], "A", "Angka 8 dibentuk meliuk rapi seperti dua lingkaran bersambung.")
mc("c3", "sedang", T, Kn, S3, "Bilangan di antara 3 dan 5 adalah ....", ["4", "2", "6", "1"], "A", "Bilangan di antara 3 dan 5 adalah 4.", verifikasi={"ekspresi": "4", "hasil": "4"})
tf("c3", "sedang", T, Kn, S2, "Setelah angka 9 adalah angka 10.", "Benar", "Urutan membilang maju setelah sembilan adalah sepuluh (10).")
tf("c3", "sedang", T, Kn, S3, "Kata 'sepuluh' lambangnya adalah angka 5.", "Salah", "Nama sepuluh lambangnya angka 10.")
sa("c3", "sedang", T, F, S3, "Tulis angka untuk nama bilangan enam.", "6|enam", "Nama bilangan enam lambangnya angka 6.", verifikasi={"ekspresi": "6", "hasil": "6"})

# ── C4 SEDANG (10 soal: 3 checkpoint, 7 terarah) ───────────────────────────
mc("c4", "sedang", K, Kn, S1, "Piring memuat 3 kue. Lambang yang cocok ....", ["3", "2", "4", "5"], "A", "Banyak kue ada 3, maka kartu lambang bilangannya adalah 3.", verifikasi={"ekspresi": "3", "hasil": "3"})
mc("c4", "sedang", K, Kn, S2, "Kotak memuat 10 pensil. Lambang yang cocok ....", ["10", "9", "8", "7"], "A", "Banyak pensil 10, lambangnya angka 10.", verifikasi={"ekspresi": "10", "hasil": "10"})
tf("c4", "sedang", K, Kn, S3, "Angka 7 lebih kecil daripada angka 6.", "Salah", "Angka 7 lebih besar daripada angka 6.")

# Terarah (7)
mc("c4", "sedang", T, Kn, S1, "Urutan angka yang rumpang: 1, 2, ..., 4.", ["3", "5", "6", "2"], "A", "Angka yang melengkapi urutan 1, 2, ..., 4 adalah 3.", verifikasi={"ekspresi": "2+1", "hasil": "3"})
mc("c4", "sedang", T, Kn, S2, "Urutan angka yang rumpang: 7, ..., 9, 10.", ["8", "6", "5", "7"], "A", "Angka di antara 7 dan 9 adalah 8.", verifikasi={"ekspresi": "7+1", "hasil": "8"})
mc("c4", "sedang", T, Kn, S3, f"Manakah kelompok dengan lambang angka 6?", [e('🐟', 6), e('🐟', 5), e('🐟', 7), e('🐟', 4)], "A", "Kelompok ikan berjumlah 6 berpasangan dengan lambang 6.")
mc("c4", "sedang", T, Pr, S4, "Langkah menulis angka 4 yang rapi adalah ....", ["tarik miring, geser mendatar, beri garis tegak", "buat lingkaran lalu garis lurus", "putar garis melengkung dua kali", "tarik garis bawah ke atas"], "A", "Menulis angka 4 diawali garis miring, geser mendatar, lalu dipotong garis tegak.")
tf("c4", "sedang", T, Pr, S4, "Menulis angka dimulai dari bagian atas.", "Benar", "Sebagian besar angka ditulis mulai dari atas ke bawah.")
tf("c4", "sedang", T, Kn, S1, f"{e('🌸', 4)} cocok dengan lambang angka 6.", "Salah", "Bunga ada 4, cocok dengan lambang angka 4.")
sa("c4", "sedang", T, Pr, S2, "Angka berapakah antara 7 dan 9?", "8|delapan", "Angka di antara 7 dan 9 adalah 8.", verifikasi={"ekspresi": "8", "hasil": "8"})

# ── C5 SEDANG (3 soal: 3 checkpoint) ──────────────────────────────────────
mc("c5", "sedang", K, Me, S4, "Edo menulis angka 6, tetapi terbalik jadi 9. Cara memperbaikinya ....", ["buat lingkaran berada di bawah", "balik kertas buku tulis", "hapus angka dan tebak", "tulis angka 10"], "A", "Edo harus membuat lingkaran di bawah agar menjadi angka 6.")
mc("c5", "sedang", K, Kn, S3, "Manakah pasangan yang tidak cocok?", ["tujuh - 9", "lima - 5", "tiga - 3", "delapan - 8"], "A", "Nama tujuh harus berpasangan dengan lambang 7, bukan 9.")
mc("c5", "sedang", K, Me, S3, "Dina ingin menulis lambang bilangan sepuluh. Pilihan tepat ....", ["10", "01", "1", "0"], "A", "Sepuluh dilambangkan dengan angka 10, angka 1 di depan dan 0 di belakang.", verifikasi={"ekspresi": "10", "hasil": "10"})

# ── C3 SULIT (2 soal: 2 mandiri) ──────────────────────────────────────────
mc("c3", "sulit", X, Kn, S2, "Kartu angka yang urut dari kecil adalah ....", ["5, 6, 7, 8", "8, 7, 6, 5", "5, 7, 6, 8", "6, 5, 8, 7"], "A", "Urutan dari kecil yang tepat adalah 5, 6, 7, 8.")
sa("c3", "sulit", X, F, S3, "Berapakah lambang bilangan untuk kata 'sepuluh'?", "10|sepuluh", "Sepuluh dilambangkan dengan angka 10.", verifikasi={"ekspresi": "10", "hasil": "10"})

# ── C4 SULIT (3 soal: 3 mandiri) ──────────────────────────────────────────
mc("c4", "sulit", X, Kn, S1, f"Ada {e('🍬', 3)} dan {e('🍬', 2)}. Lambang gabungannya ....", ["5", "4", "6", "3"], "A", "Tiga permen digabung dua permen menjadi 5 permen, lambangnya 5.", verifikasi={"ekspresi": "3+2", "hasil": "5"})
mc("c4", "sulit", X, Kn, S3, "Nama bilangan 'delapan' lebih besar dari lambang ....", ["7", "9", "10", "8"], "A", "Delapan (8) lebih besar dari 7.", verifikasi={"ekspresi": "8-1", "hasil": "7"})
tf("c4", "sulit", X, Me, S4, "Mengecek tulisan angka membantu tulisan mudah dibaca.", "Benar", "Mengecek kembali memastikan angka tidak terbalik atau salah tulis.")

# ── C5 SULIT (3 soal: 3 mandiri) ──────────────────────────────────────────
mc("c5", "sulit", X, Me, S4, "Rani ingin membedakan angka 6 dan 9. Nasihat tepat ....", ["perhatikan letak lengkung lingkarannya", "hitung garis lurusnya saja", "warnai angka dengan pensil", "anggap kedua angka sama"], "A", "Perhatikan letak lengkungnya: angka 6 di bawah, angka 9 di atas.")
mc("c5", "sulit", X, Kn, S3, "Kartu angka yang berurutan setelah 5 adalah ....", ["6, 7, 8", "7, 6, 8", "8, 7, 6", "5, 7, 6"], "A", "Urutan angka setelah 5 adalah 6, 7, 8.")
mc("c5", "sulit", X, Me, S3, "Doni bingung memilih lambang untuk 'empat'. Cara bantu Doni ....", ["tunjukkan kartu angka 4", "sebut angka sembilan", "gambar sepuluh titik", "beri kartu angka 2"], "A", "Menunjukkan kartu angka 4 membantu Doni melihat lambang yang tepat.")

# ── C6 SULIT (2 soal: 2 pengayaan) ────────────────────────────────────────
mc("c6", "sulit", P, Kn, S3, "Desain kartu angka 8 yang lengkap harus memuat ....", ["angka 8 dan 8 gambar benda", "angka 8 tanpa gambar", "tulisan tujuh saja", "hanya gambar 5 bintang"], "A", "Kartu yang lengkap memuat lambang angka 8 beserta 8 gambar benda.")
mc("c6", "sulit", P, Pr, S4, "Kamu membuat poster angka 1 sampai 10. Agar rapi ....", ["tulis angka berurutan dari 1 sampai 10", "tulis angka secara acak", "tulis angka 10 di awal", "lewati angka yang sulit"], "A", "Menulis angka berurutan dari 1 sampai 10 membuat poster rapi dan mudah dibaca.")

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

uid = lambda i: str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab2_soal_{i}"))
groups = {"mc": [], "tf": [], "sa": []}

random.seed(42)
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
    ("Mengenal Lambang 1 sampai 5", S1),
    ("Mengenal Lambang 6 sampai 10", S2),
    ("Menghubungkan Nama dan Lambang Bilangan", S3),
    ("Menulis Angka dengan Benar", S4)
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
    (S1, "Aku bisa mengenali dan membaca lambang bilangan 1 sampai 5.", "Mengenal Lambang 1 sampai 5",
f"""Mari mengenal lambang bilangan 1 sampai 5.
Setiap benda punya lambang angka.

Lihat benda di sekitarmu:
Ada 1 matahari di langit.
Ada 2 mata pada wajahmu.
Ada 3 roda pada becak.
Ada 4 kaki meja belajarmu.
Ada 5 jari di satu tanganmu.

:::definition
term: Lambang Bilangan
definition: Tanda angka untuk menunjukkan banyak benda.
:::

:::callout
variant: tip
title: Ingat ya
text: Angka 1 sampai 5 sangat mudah diingat.
:::""", 3),

    (S2, "Aku bisa mengenali dan membaca lambang bilangan 6 sampai 10.", "Mengenal Lambang 6 sampai 10",
f"""Sekarang kita lanjut ke angka 6 sampai 10.

Ayo kita sebut bersama:
Ada 6 pensil warna di kotak.
Ada 7 warna pada pelangi.
Ada 8 kaki gurita di laut.
Ada 9 buah apel di keranjang.
Ada 10 jari pada kedua tanganmu.

:::table
headers: ["Nama","Lambang","Banyak Benda"]
rows: [["enam","6","{e('✏️', 6)}"],["tujuh","7","{e('✏️', 7)}"],["delapan","8","{e('✏️', 8)}"],["sembilan","9","{e('✏️', 9)}"],["sepuluh","10","{e('✏️', 10)}"]]
caption: Lambang Bilangan 6 sampai 10
:::""", 4),

    (S3, "Aku bisa memasangkan nama bilangan dengan lambang bilangannya.", "Menghubungkan Nama dan Lambang Bilangan",
f"""Nama bilangan memakai susunan huruf.
Lambang bilangan memakai bentuk angka.

Keduanya mempunyai arti yang sama.
Kata "tiga" lambangnya adalah 3.
Kata "tujuh" lambangnya adalah 7.
Kata "sepuluh" lambangnya adalah 10.

:::steps
title: Cara memasangkan nama dan lambang
items: ["Baca nama bilangannya dengan jelas.","Ingat bentuk angkanya.","Pilih lambang angka yang tepat."]
:::""", 4),

    (S4, "Aku bisa menulis angka dengan rapi dan benar.", "Menulis Angka dengan Benar",
f"""Tulis angka dengan hati-hati ya.
Mulailah goresan pensil dari atas.

Hati-hati dengan angka 6 dan 9.
Angka 6 punya lingkaran di bawah.
Angka 9 punya lingkaran di atas.

:::common_trap
term: Menghitung Benda Dua Kali atau Terlewat
explanation: Tunjuk benda satu per satu agar hitungan dan tulisan angkamu tepat.
:::

:::callout
variant: summary
title: Ringkasan
text: Lambang bilangan ditulis dengan angka. Menulis angka dimulai dari atas.
:::""", 3),
]

lp = {
    "level": "Kelas 1 SD — Fase A",
    "title": "Melambangkan Bilangan 1 sampai 10",
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab2.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"lesson_plan": lp, "quiz_config": quiz}, f, ensure_ascii=False, indent=2)

print("BERHASIL:", out_path, "berhasil dibuat dan divalidasi!")
