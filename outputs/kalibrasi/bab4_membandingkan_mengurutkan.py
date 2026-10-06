#!/usr/bin/env python3
"""
Generator dan validator Bab 4 Matematika Kelas 1 SD:
"Membandingkan dan Mengurutkan Bilangan sampai 20" (Fase A)
bab_id: 09db88f4-6516-43c8-8ac8-39f69a17d484
article_id: 691aee5a-dd3f-478d-9ce7-1c0550762ba6
quiz_id: 9bb8d68b-d7fa-43f3-9de6-1ce3b71a8bd6
"""
import json, uuid, random, re, os
from collections import Counter

random.seed(44)
S1, S2, S3, S4 = "a4b3c29d5e71", "b5c4d30e6f82", "c6d5e41f7a93", "d7e6f52a8b04"

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
mc("c1", "mudah", D, F, S1, "Kata untuk membandingkan jumlah benda adalah ....", ["lebih banyak", "paling panjang", "sangat cepat", "warna merah"], "A", "Untuk membandingkan jumlah benda kita gunakan lebih banyak atau lebih sedikit.")
tf("c1", "mudah", D, F, S2, "Angka 15 lebih kecil daripada angka 10.", "Salah", "Angka 15 lebih besar daripada angka 10.")
mc("c1", "mudah", T, F, S2, "Angka yang lebih kecil dari 8 adalah ....", ["5", "9", "10", "12"], "A", "Angka 5 bernilai lebih kecil dari 8.", verifikasi={"ekspresi": "5", "hasil": "5"})
mc("c1", "mudah", T, F, S3, "Urutan dari kecil mulai dari angka paling ....", ["kecil", "besar", "panjang", "berat"], "A", "Mengurutkan dari kecil dimulai dari angka yang nilainya paling kecil.")
sa("c1", "mudah", T, F, S4, "Tulis bilangan terbesar di antara 5 dan 9.", "9|sembilan", "Bilangan terbesar antara 5 dan 9 adalah 9.", verifikasi={"ekspresi": "9", "hasil": "9"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
mc("c2", "mudah", D, Kn, S1, "Bila dua piring berisi masing-masing 5 kue, artinya ....", ["sama banyak", "lebih banyak", "lebih sedikit", "berbeda jauh"], "A", "Jumlah kue sama-sama 5 berarti sama banyak.")
tf("c2", "mudah", D, Kn, S3, "Urutan 11, 12, 13 adalah urutan dari kecil.", "Benar", "Angka 11 ke 13 bertambah besar, jadi urut dari kecil.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Budi memilih bilangan yang lebih besar dari 12: ....", ["15", "10", "8", "11"], "A", "Lima belas lebih besar dari 12.", "Melihat angka satuan 2 lebih besar dari 0", verifikasi={"ekspresi": "15", "hasil": "15"})
mc("c2", "mudah", R, Kn, S4, "Mengurutkan dari terbesar berarti susunannya ....", ["makin ke kanan makin kecil", "makin ke kanan makin besar", "angkanya selalu sama", "acak tanpa pola"], "A", "Urutan dari terbesar bergerak menurun ke nilai yang lebih kecil.", "Tertukar pengertian urutan terbesar dan terkecil")

# Terarah (4)
mc("c2", "mudah", T, Kn, S1, f"Ada {e('🍎', 7)} dan {e('🍊', 4)}. Berapa banyak apel?", ["7", "4", "3", "11"], "A", "Banyak buah apel pada gambar adalah 7 buah.", verifikasi={"ekspresi": "7", "hasil": "7"})
mc("c2", "mudah", T, Kn, S2, "Manakah bilangan yang lebih besar antara 16 dan 19?", ["19", "16", "15", "10"], "A", "Sembilan belas bernilai lebih besar dari 16.", verifikasi={"ekspresi": "19", "hasil": "19"})
tf("c2", "mudah", T, Kn, S3, "Urutan 12, 8, 5 sudah terurut dari terkecil.", "Salah", "Urutan 12, 8, 5 adalah dari terbesar ke terkecil.")
sa("c2", "mudah", T, F, S1, f"Berapa banyak kue di tiap piring jika sama banyak ({e('🍬', 6)})?", "6|enam", "Tiap piring berisi 6 kue.", verifikasi={"ekspresi": "6", "hasil": "6"})

# ── C3 MUDAH (2 soal: 2 terarah) ──────────────────────────────────────────
mc("c3", "mudah", T, Pr, S4, "Bilangan terbesar di antara 6, 15, dan 9 adalah ....", ["15", "9", "6", "5"], "A", "Paling besar di antara ketiga bilangan adalah 15.", verifikasi={"ekspresi": "15", "hasil": "15"})
tf("c3", "mudah", T, Kn, S3, "Urutan 11, 14, 18 adalah dari terkecil.", "Benar", "Angka 11, 14, 18 tersusun dari terkecil.")

# ── C3 SEDANG (12 soal: 4 checkpoint, 2 remedial, 6 terarah) ──────────────
mc("c3", "sedang", K, Kn, S1, f"Berapa selisih banyak {e('⭐', 10)} dan {e('⭐', 8)}?", ["2", "1", "3", "4"], "A", "Sepuluh bintang dikurangi 8 bintang berselisih 2 bintang.", verifikasi={"ekspresi": "10 - 8", "hasil": "2"})
mc("c3", "sedang", K, Kn, S2, "Bilangan yang nilainya lebih kecil dari 17 adalah ....", ["14", "18", "19", "20"], "A", "Empat belas bernilai lebih kecil dari 17.", verifikasi={"ekspresi": "14", "hasil": "14"})
mc("c3", "sedang", K, Kn, S3, "Bilangan paling kecil dari 8, 12, 16, 20 adalah ....", ["8", "12", "16", "20"], "A", "Bilangan dengan nilai paling kecil adalah 8.", verifikasi={"ekspresi": "8", "hasil": "8"})
tf("c3", "sedang", K, Kn, S4, "Urutan 11, 15, 19 tersusun dari terbesar.", "Salah", "Urutan 11, 15, 19 tersusun dari yang terkecil.")

# Remedial (2)
mc("c3", "sedang", R, Me, S2, "Siti ragu apakah 17 lebih besar dari 13. Cara membuktikannya ....", ["lihat posisi di garis bilangan", "tebak angka yang bagus", "tulis angka terbalik", "pilih angka yang pendek"], "A", "Pada garis bilangan, 17 terletak di sebelah kanan 13 sehingga lebih besar.", "Tidak menggunakan acuan garis bilangan")
mc("c3", "sedang", R, Me, S3, "Bilangan paling kecil dari 14, 9, 12 adalah ....", ["9", "12", "14", "10"], "A", "Bilangan dengan nilai paling kecil adalah 9.", "Mengabaikan nilai tempat puluhan saat mengurutkan", verifikasi={"ekspresi": "9", "hasil": "9"})

# Terarah (6)
mc("c3", "sedang", T, Kn, S1, f"Berapa selisih banyak {e('🐱', 5)} dan {e('🐱', 3)}?", ["2", "1", "3", "4"], "A", "Lima kucing dikurangi 3 kucing berselisih 2.", verifikasi={"ekspresi": "5 - 3", "hasil": "2"})
mc("c3", "sedang", T, Kn, S2, "Bilangan di antara 13 dan 17 yang paling besar ....", ["16", "14", "15", "12"], "A", "Di antara 13 dan 17 ada 14, 15, 16. Paling besar adalah 16.", verifikasi={"ekspresi": "16", "hasil": "16"})
mc("c3", "sedang", T, Pr, S3, "Langkah mengurutkan bilangan dari terkecil ....", ["cari angka paling kecil lebih dulu", "tulis angka secara acak", "pilih angka terbesar lebih dulu", "jumlahkan semua angka"], "A", "Cari angka dengan nilai paling kecil sebagai langkah awal.")
mc("c3", "sedang", T, Pr, S4, "Bilangan sebelum 20 pada hitungan mundur adalah ....", ["19", "18", "17", "21"], "A", "Tepat sebelum 20 saat hitung mundur adalah 19.", verifikasi={"ekspresi": "20 - 1", "hasil": "19"})
tf("c3", "sedang", T, Kn, S2, "Dua puluh adalah bilangan paling besar sampai 20.", "Benar", "Di antara bilangan 1 sampai 20, 20 adalah nilai terbesar.")
sa("c3", "sedang", T, F, S3, "Bilangan terkecil dari 7, 3, 5 adalah ....", "3|tiga", "Bilangan terkecil dari 7, 3, 5 adalah 3.", verifikasi={"ekspresi": "3", "hasil": "3"})

# ── C4 SEDANG (10 soal: 3 checkpoint, 7 terarah) ───────────────────────────
mc("c4", "sedang", K, Kn, S1, f"Berapa selisih banyak {e('✏️', 12)} dan {e('✏️', 9)}?", ["3", "2", "4", "1"], "A", "Dua belas spidol dan 9 pensil berselisih 3.", verifikasi={"ekspresi": "12 - 9", "hasil": "3"})
mc("c4", "sedang", K, Kn, S4, "Bilangan terbesar di antara 13, 20, 17 adalah ....", ["20", "17", "13", "10"], "A", "Bilangan dengan nilai terbesar adalah 20.", verifikasi={"ekspresi": "20", "hasil": "20"})
tf("c4", "sedang", K, Kn, S2, "Angka 16 berada di sebelah kiri angka 14.", "Salah", "Pada garis bilangan, 16 berada di sebelah kanan 14.")

# Terarah (7)
mc("c4", "sedang", T, Kn, S1, "Berapa selisih kelereng Ali 15 dan Beni 11?", ["4", "3", "5", "2"], "A", "Lima belas dikurangi sebelas sama dengan 4.", verifikasi={"ekspresi": "15 - 11", "hasil": "4"})
mc("c4", "sedang", T, Kn, S2, "Berapa bilangan yang hilang: 13, ..., 15?", ["14", "12", "16", "11"], "A", "Di antara 13 dan 15 adalah 14.", verifikasi={"ekspresi": "13 + 1", "hasil": "14"})
mc("c4", "sedang", T, Pr, S3, "Sisipkan angka yang hilang agar urut dari kecil: 10, ..., 14.", ["12", "15", "9", "16"], "A", "Angka 12 berada di antara 10 dan 14.", verifikasi={"ekspresi": "12", "hasil": "12"})
mc("c4", "sedang", T, Pr, S4, "Urutan kartu dari terbesar: 18, 14, ....", ["10", "19", "20", "16"], "A", "Setelah 18 dan 14, angka berikutnya harus lebih kecil, yaitu 10.", verifikasi={"ekspresi": "10", "hasil": "10"})
tf("c4", "sedang", T, Pr, S1, "Memasangkan satu per satu membuktikan perbandingan benda.", "Benar", "Memasangkan benda secara langsung membuktikan mana yang lebih banyak.")
tf("c4", "sedang", T, Kn, S2, "Bilangan 11 lebih dekat ke 20 daripada ke 10.", "Salah", "Bilangan 11 lebih dekat ke 10 daripada ke 20.")
sa("c4", "sedang", T, Pr, S4, "Tulis bilangan terbesar dari 11, 19, 15.", "19|sembilan belas", "Bilangan terbesar adalah 19.", verifikasi={"ekspresi": "19", "hasil": "19"})

# ── C5 SEDANG (3 soal: 3 checkpoint) ──────────────────────────────────────
mc("c5", "sedang", K, Me, S3, "Andi mengurutkan kartu: 7, 15, 11. Kesalahan Andi ....", ["15 seharusnya diletakkan di akhir", "angka 7 paling besar", "angka 11 paling kecil", "semua urutan sudah tepat"], "A", "Karena 15 lebih besar dari 11, maka 15 diletakkan di akhir.")
mc("c5", "sedang", K, Kn, S2, "Pernyataan berikut yang tidak tepat adalah ....", ["12 lebih besar dari 14", "17 lebih besar dari 15", "10 lebih kecil dari 20", "19 lebih besar dari 18"], "A", "Dua belas seharusnya lebih kecil dari 14.")
mc("c5", "sedang", K, Me, S1, "Untuk memastikan dua toples sama banyak, kita ....", ["hitung jumlah isi kedua toples", "lihat warna toplesnya saja", "tebak tanpa membuka toples", "timbang dengan tangan kosong"], "A", "Menghitung isi kedua toples membuktikan secara tepat apakah isinya sama banyak.")

# ── C3 SULIT (2 soal: 2 mandiri) ──────────────────────────────────────────
mc("c3", "sulit", X, Kn, S2, "Manakah bilangan yang nilainya di antara 15 dan 18?", ["17", "14", "19", "20"], "A", "Tujuh belas berada di antara 15 dan 18.", verifikasi={"ekspresi": "17", "hasil": "17"})
sa("c3", "sulit", X, F, S4, "Bilangan terbesar dari 9, 17, 13 adalah ....", "17|tujuh belas", "Angka terbesar adalah 17.", verifikasi={"ekspresi": "17", "hasil": "17"})

# ── C4 SULIT (3 soal: 3 mandiri) ──────────────────────────────────────────
mc("c4", "sulit", X, Kn, S1, "Toples B isi 16, toples A isi 14. B lebih banyak ....", ["2", "4", "1", "3"], "A", "Enam belas adalah dua permen lebih banyak dari 14.", verifikasi={"ekspresi": "16 - 14", "hasil": "2"})
mc("c4", "sulit", X, Kn, S3, "Bilangan terkecil dari 6, 11, 15, 19 adalah ....", ["6", "11", "15", "19"], "A", "Bilangan terkecil adalah 6.", verifikasi={"ekspresi": "6", "hasil": "6"})
tf("c4", "sulit", X, Me, S2, "Melihat garis bilangan membantu membandingkan dua angka.", "Benar", "Posisi kiri dan kanan pada garis bilangan memudahkan perbandingan.")

# ── C5 SULIT (3 soal: 3 mandiri) ──────────────────────────────────────────
mc("c5", "sulit", X, Me, S4, "Bilangan terbesar dari 8, 14, 11, 20 adalah ....", ["20", "14", "11", "8"], "A", "Bilangan terbesar di antara keempat kartu adalah 20.", verifikasi={"ekspresi": "20", "hasil": "20"})
mc("c5", "sulit", X, Kn, S2, "Bilangan manakah yang bernilai di antara 10 dan 12?", ["11", "13", "14", "9"], "A", "Di antara 10 dan 12 terdapat bilangan 11.", verifikasi={"ekspresi": "11", "hasil": "11"})
mc("c5", "sulit", X, Me, S3, "Cara terbaik menyusun lima kartu acak dari kecil ....", ["cari yang terkecil satu per satu", "tebak urutan secara cepat", "susun tanpa melihat angka", "letakkan kartu terbesar di awal"], "A", "Mencari angka terkecil secara bertahap menjamin susunan benar.")

# ── C6 SULIT (2 soal: 2 pengayaan) ────────────────────────────────────────
mc("c6", "sulit", P, Kn, S3, "Susun aturan permainan garis bilangan dari kecil ....", ["pemain melompat maju dari angka kecil ke besar", "pemain melompat mundur secara acak", "pemain berdiri diam di satu angka", "pemain melompati angka secara bebas"], "A", "Aturan melompat maju dari kecil ke besar mengajarkan urutan naik.")
mc("c6", "sulit", P, Pr, S4, "Buatlah kartu petunjuk urutan terbesar di kelas ....", ["tulis tanda panah turun dari angka terbesar", "acak semua angka di kertas", "tutup angka dengan gambar", "tulis satu angka saja"], "A", "Tanda panah turun membantu siswa memahami arah urutan menurun.")

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

uid = lambda i: str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab4_soal_{i}"))
groups = {"mc": [], "tf": [], "sa": []}

random.seed(44)
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
    ("Membandingkan Banyak Benda", S1),
    ("Membandingkan Dua Lambang Bilangan", S2),
    ("Mengurutkan Bilangan dari Terkecil", S3),
    ("Mengurutkan Bilangan dari Terbesar", S4)
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
    (S1, "Aku bisa membandingkan banyak dua kelompok benda konkret.", "Membandingkan Banyak Benda",
f"""Mari membandingkan banyak benda di sekitarmu.
Kita bisa pasangkan benda satu per satu.

Ada 7 apel merah segar.
Ada 4 jeruk manis.
Apel lebih banyak dari jeruk.
Jeruk lebih sedikit dari apel.
Jika jumlah sama, sebut sama banyak.

:::definition
term: Lebih Banyak
definition: Jumlah benda yang lebih besar saat dibandingkan.
:::

:::callout
variant: tip
title: Tips
text: Pasangkan benda untuk melihat beda jumlahnya.
:::""", 3),

    (S2, "Aku bisa membandingkan dua bilangan sampai 20.", "Membandingkan Dua Lambang Bilangan",
f"""Kita juga bisa membandingkan angka.
Lihat angka pada garis bilangan.

Angka 15 dan angka 11:
Angka 15 bernilai lebih besar.
Angka 11 bernilai lebih kecil.
Angka di kanan bernilai lebih besar.

:::table
headers: ["Angka","Posisi","Bandingkan"]
rows: [["11.","sebelah kiri.","lebih kecil."],["15.","sebelah kanan.","lebih besar."]]
caption: Membandingkan 11 dan 15
:::""", 4),

    (S3, "Aku bisa mengurutkan bilangan dari terkecil.", "Mengurutkan Bilangan dari Terkecil",
f"""Sekarang kita urutkan bilangan.
Ayo mulai dari yang terkecil.

Ada angka 12, 7, dan 15:
Paling kecil adalah angka 7.
Berikutnya adalah angka 12.
Paling besar adalah angka 15.
Urutan dari terkecil: 7, 12, 15.

:::steps
title: Cara mengurutkan dari terkecil
items: ["Cari angka paling kecil lebih dulu.","Pilih angka berikutnya yang lebih besar.","Tulis angka paling besar di akhir."]
:::""", 4),

    (S4, "Aku bisa mengurutkan bilangan dari terbesar.", "Mengurutkan Bilangan dari Terbesar",
f"""Kita juga bisa mengurutkan mundur.
Urutkan dari bilangan paling besar.

Ada angka 8, 19, dan 14:
Paling besar adalah angka 19.
Lalu angka 14 berikutnya.
Paling kecil adalah angka 8.
Urutan dari terbesar: 19, 14, 8.

:::common_trap
term: Menghitung Benda Dua Kali atau Terlewat
explanation: Hitung benda dengan teliti sebelum membandingkan agar tidak salah urutan.
:::

:::callout
variant: summary
title: Ringkasan
text: Bandingkan benda dengan memasangkannya. Urutkan bilangan dari terkecil atau terbesar.
:::""", 3),
]

lp = {
    "level": "Kelas 1 SD — Fase A",
    "title": "Membandingkan dan Mengurutkan Bilangan sampai 20",
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab4.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"lesson_plan": lp, "quiz_config": quiz}, f, ensure_ascii=False, indent=2)

print("BERHASIL:", out_path, "berhasil dibuat dan divalidasi!")
