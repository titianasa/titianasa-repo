#!/usr/bin/env python3
"""
Generator dan validator Bab 6 Matematika Kelas 1 SD:
"Kesalahan Umum: Menghitung Benda Dua Kali atau Terlewat" (Fase A)
bab_id: fbbbc28d-9b64-49a4-80d2-f8b34f084a87
article_id: 80af5d92-f077-48ac-bbc3-a7b727dfdccf
quiz_id: 35c93c9e-b26e-43ff-9c65-c9ebbdcf3593
"""
import json, uuid, random, re, os
from collections import Counter

random.seed(46)
S1, S2, S3, S4 = "a6b5c49d7e91", "b7c6d50e8f02", "c8d7e61f9a13", "d9e8f72a0b24"

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
mc("c1", "mudah", D, F, S1, "Bila satu benda dihitung dua kali, jumlahnya ....", ["terlalu banyak", "terlalu sedikit", "tetap tepat", "menjadi nol"], "A", "Menghitung dua kali membuat jumlah akhir berlebih.")
tf("c1", "mudah", D, F, S2, "Bila ada benda terlewat, hitungan jadi bertambah.", "Salah", "Benda yang terlewat membuat hitungan berkurang, bukan bertambah.")
mc("c1", "mudah", T, F, S3, "Tanda coret kecil pada gambar berguna agar ....", ["tidak dihitung dua kali", "gambar menjadi bagus", "benda bertambah banyak", "warna menjadi hitam"], "A", "Mencoret gambar menandakan benda sudah dihitung.")
mc("c1", "mudah", T, F, S4, "Memeriksa ulang hitungan artinya ....", ["menghitung sekali lagi", "menebak hasil hitungan", "menghapus semua angka", "berhenti berhitung"], "A", "Memeriksa ulang dilakukan dengan menghitung sekali lagi.")
sa("c1", "mudah", T, F, S1, "Satu benda harus ditunjuk berapa kali?", "1|satu kali", "Tunjuk setiap benda tepat satu kali.", verifikasi={"ekspresi": "1", "hasil": "1"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
mc("c2", "mudah", D, Kn, S3, "Cara merapikan benda agar mudah dihitung ....", ["susun berbaris lurus", "tumpuk bertingkat tinggi", "sebar secara acak", "sembunyikan di meja"], "A", "Menyusun benda berbaris lurus memudahkan hitungan urut.")
tf("c2", "mudah", D, Kn, S1, "Satu benda hanya boleh dihitung satu kali.", "Benar", "Prinsip membilang adalah satu benda satu nama bilangan.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, "Ada 5 apel dihitung jadi 6. Berapa apel dihitung dobel?", ["1", "2", "3", "0"], "A", "Hasil berlebih satu menunjukkan satu apel disentuh dua kali.", "Menghitung benda dua kali sehingga hasil bertambah satu", verifikasi={"ekspresi": "6 - 5", "hasil": "1"})
mc("c2", "mudah", R, Kn, S2, "Ada 8 bintang dihitung jadi 7. Berapa bintang terlewat?", ["1", "2", "3", "0"], "A", "Hasil berkurang satu menunjukkan satu bintang terlewat.", "Melewatkan satu benda saat membilang", verifikasi={"ekspresi": "8 - 7", "hasil": "1"})

# Terarah (4)
mc("c2", "mudah", T, Kn, S1, "Tono hitung 3 mobil jadi 4. Berapa mobil terhitung dobel?", ["1", "2", "3", "0"], "A", "Hasil 4 dari 3 mobil berarti ada satu mobil terhitung dua kali.", verifikasi={"ekspresi": "4 - 3", "hasil": "1"})
mc("c2", "mudah", T, Kn, S2, "Ada 6 balon terhitung 5 balon. Berapa balon terlewat?", ["1", "2", "3", "0"], "A", "Hasil 5 dari 6 balon menunjukkan satu balon terlewat.", verifikasi={"ekspresi": "6 - 5", "hasil": "1"})
tf("c2", "mudah", T, Kn, S3, "Menghitung sambil melempar benda membuat hitungan teliti.", "Salah", "Melempar benda membuat benda berantakan dan salah hitung.")
sa("c2", "mudah", T, F, S4, "Berapa kali kita menunjuk tiap benda saat membilang?", "1|satu kali", "Tunjuk tiap benda tepat satu kali.", verifikasi={"ekspresi": "1", "hasil": "1"})

# ── C3 MUDAH (2 soal: 2 terarah) ──────────────────────────────────────────
mc("c3", "mudah", T, Pr, S3, "Saat menghitung sebaris benda, arah yang baik ....", ["dari kiri ke kanan", "acak lompat-lompat", "dari tengah memutar", "bebas tanpa aturan"], "A", "Membilang dari kiri ke kanan menjaga urutan pandangan.")
tf("c3", "mudah", T, Kn, S2, "Bila 10 pensil terlewat 1, hasilnya terhitung 9.", "Benar", "Sepuluh dikurangi satu pensil terlewat terhitung 9.", verifikasi={"ekspresi": "10 - 1", "hasil": "9"})

# ── C3 SEDANG (12 soal: 4 checkpoint, 2 remedial, 6 terarah) ──────────────
mc("c3", "sedang", K, Kn, S1, f"Berapa jumlah sebenarnya dari {e('🍎', 4)}?", ["4", "5", "6", "3"], "A", "Jumlah sebenarnya adalah 4 apel.", verifikasi={"ekspresi": "4", "hasil": "4"})
mc("c3", "sedang", K, Kn, S2, f"Berapa jumlah sebenarnya dari {e('🐱', 5)}?", ["5", "4", "6", "3"], "A", "Jumlah sebenarnya adalah 5 kucing.", verifikasi={"ekspresi": "5", "hasil": "5"})
mc("c3", "sedang", K, Pr, S3, "Strategi menghitung gambar yang berserak adalah ....", ["coret gambar yang sudah dihitung", "hitung gambar dalam hati", "tutup mata saat berhitung", "tebak jumlah gambarnya"], "A", "Memberi coretan pensil menandai gambar yang sudah dihitung.")
tf("c3", "sedang", K, Me, S4, "Hitungan pertama 7 dan kedua 9 sudah pasti tepat.", "Salah", "Hasil berbeda 7 dan 9 menandakan perlu dihitung ulang.")

# Remedial (2)
mc("c3", "sedang", R, Me, S3, "Dina bingung mana kelereng yang sudah dihitung. Solusinya ....", ["geser kelereng yang sudah dihitung ke samping", "aduk semua kelereng", "hitung sambil berlari", "tinggalkan kelerengnya"], "A", "Menggeser benda yang sudah dihitung memisahkan dari sisa benda.", "Tidak memisahkan benda yang sudah dihitung")
mc("c3", "sedang", R, Me, S1, "Bila ada 6 kelereng terhitung 7, berapa kelereng dobel?", ["1", "2", "3", "0"], "A", "Kelebihan satu kelereng menandakan satu kelereng disentuh dobel.", "Koordinasi sentuhan dan sebutan angka tidak selaras", verifikasi={"ekspresi": "7 - 6", "hasil": "1"})

# Terarah (6)
mc("c3", "sedang", T, Kn, S1, "Mengapa tidak boleh menghitung benda dua kali?", ["agar jumlah benda tidak berlebih", "agar benda tidak rusak", "agar tangan tidak kotor", "agar cepat selesai"], "A", "Menghitung dua kali membuat hasil berlebih dari jumlah sebenarnya.")
mc("c3", "sedang", T, Kn, S2, "Ada 9 bola terlewat 1, maka terhitung berapa bola?", ["8", "7", "9", "10"], "A", "Sembilan terlewat satu akan terhitung 8 bola.", verifikasi={"ekspresi": "9 - 1", "hasil": "8"})
mc("c3", "sedang", T, Pr, S3, "Berapa benda yang dikelompokkan agar mudah membilang belasan?", ["10", "2", "5", "20"], "A", "Membuat kelompok 10 sangat mempermudah membilang belasan.", verifikasi={"ekspresi": "10", "hasil": "10"})
mc("c3", "sedang", T, Pr, S4, "Hitungan pertama 8 dan kedua 9 berselisih berapa?", ["1", "2", "3", "0"], "A", "Sembilan dikurangi 8 berselisih 1.", verifikasi={"ekspresi": "9 - 8", "hasil": "1"})
tf("c3", "sedang", T, Kn, S2, "Mata tergesa-gesa menyebabkan benda terlewat.", "Benar", "Tergesa-gesa membuat konsentrasi buyar dan benda terlewat.")
sa("c3", "sedang", T, F, S3, "Bila ada 5 gambar dan dicoret 2, berapa sisa belum dicoret?", "3|tiga", "Lima dikurangi 2 tersisa 3 gambar.", verifikasi={"ekspresi": "5 - 2", "hasil": "3"})

# ── C4 SEDANG (10 soal: 3 checkpoint, 7 terarah) ───────────────────────────
mc("c4", "sedang", K, Kn, S1, "Rani hitung 6 cangkir jadi 8. Berapa cangkir terhitung dua kali?", ["2", "1", "3", "4"], "A", "Lebih 2 angka berarti ada dua cangkir terhitung dua kali.", verifikasi={"ekspresi": "8 - 6", "hasil": "2"})
mc("c4", "sedang", K, Kn, S2, "Doni hitung 10 buku jadi 8. Berapa buku yang terlewat?", ["2", "1", "3", "4"], "A", "Kurang 2 angka berarti ada dua buku terlewat.", verifikasi={"ekspresi": "10 - 8", "hasil": "2"})
tf("c4", "sedang", K, Me, S3, "Menumpuk benda acak memudahkan hitungan berurutan.", "Salah", "Tumpukan acak justru menyulitkan dan membuat benda terlewat.")

# Terarah (7)
mc("c4", "sedang", T, Kn, S1, "Ada 12 pensil terhitung 13. Berapa pensil dihitung dobel?", ["1", "2", "3", "0"], "A", "Tiga belas dikurangi 12 berarti 1 pensil terhitung dobel.", verifikasi={"ekspresi": "13 - 12", "hasil": "1"})
mc("c4", "sedang", T, Kn, S2, "Bila menghitung lingkaran acak di kertas, trik terbaik ....", ["beri nomor atau coretan tiap lingkaran", "hitung memutar terus", "hitung cepat tanpa tunjuk", "tutup sebagian lingkaran"], "A", "Memberi nomor atau coretan memastikan tiap lingkaran dihitung sekali.")
mc("c4", "sedang", T, Pr, S3, "Langkah menggeser balok mainan saat berhitung ....", ["ambil satu, sebut angka, taruh di kotak kanan", "ambil banyak sekaligus", "lempar balok ke lantai", "aduk semua balok"], "A", "Ambil satu balok, sebutkan angkanya, lalu pindahkan ke sisi kanan.")
mc("c4", "sedang", T, Pr, S4, "Hitungan pertama 12, kedua 12. Berapa hasil yang benar?", ["12", "10", "14", "24"], "A", "Dua hasil yang konsisten menunjukkan hitungan yang benar adalah 12.", verifikasi={"ekspresi": "12", "hasil": "12"})
tf("c4", "sedang", T, Pr, S1, "Menyentuh benda bersamaan dengan menyebut angka itu tepat.", "Benar", "Sinkronisasi sentuhan dan ucapan menghasilkan ketelitian.")
tf("c4", "sedang", T, Kn, S3, "Menghitung susunan melingkar tidak perlu penanda titik awal.", "Salah", "Menghitung susunan melingkar wajib memiliki penanda titik mulai.")
sa("c4", "sedang", T, Pr, S4, "Berapa hasil jika 7 benda dihitung dua kali semua?", "14|empat belas", "Tujuh dikali dua adalah 14.", verifikasi={"ekspresi": "7 * 2", "hasil": "14"})

# ── C5 SEDANG (3 soal: 3 checkpoint) ──────────────────────────────────────
mc("c5", "sedang", K, Me, S3, "Ali menghitung koin yang berserakan. Saran terbaik untuk Ali ....", ["kelompokkan koin tiap lima atau sepuluh", "hitung koin dengan tergesa-gesa", "tebak saja jumlah koinnya", "buang koin yang kecil"], "A", "Mengelompokkan tiap 5 atau 10 sangat mempercepat dan meneliti hitungan.")
mc("c5", "sedang", K, Kn, S1, "Perbedaan akibat menghitung dua kali dibanding terlewat ....", ["dua kali jadi berlebih, terlewat jadi berkurang", "dua kali jadi berkurang, terlewat jadi berlebih", "keduanya menghasilkan angka yang sama", "tidak ada perbedaan sama sekali"], "A", "Menghitung dua kali menyebabkan lebih, sedangkan terlewat menyebabkan kurang.")
mc("c5", "sedang", K, Me, S4, "Mengapa kita tidak boleh malu menghitung ulang?", ["karena menghitung ulang menjamin ketepatan", "karena menghitung ulang buang waktu", "agar kelihatan sibuk di kelas", "supaya mendapat hadiah"], "A", "Menghitung ulang adalah sikap ilmiah untuk menjamin ketepatan.")

# ── C3 SULIT (2 soal: 2 mandiri) ──────────────────────────────────────────
mc("c3", "sulit", X, Kn, S3, "Manakah cara paling aman menghitung 15 kelereng?", ["pindahkan ke toples satu per satu", "lihat kelereng dari kejauhan", "hitung sambil mengaduk kelereng", "tebak bilangannya"], "A", "Memindahkan satu per satu adalah cara paling aman dan akurat.")
sa("c3", "sulit", X, F, S2, "Bila 7 benda dihitung terlewat satu, terhitung berapa?", "6|enam", "Tujuh terlewat satu akan terhitung 6.", verifikasi={"ekspresi": "7 - 1", "hasil": "6"})

# ── C4 SULIT (3 soal: 3 mandiri) ──────────────────────────────────────────
mc("c4", "sulit", X, Kn, S1, "Siti hitung 9 bunga jadi 10. Berapa bunga dihitung dobel?", ["1", "2", "3", "0"], "A", "Kelebihan satu hitungan menandakan satu bunga terhitung dua kali.", verifikasi={"ekspresi": "10 - 9", "hasil": "1"})
mc("c4", "sulit", X, Kn, S3, "Bila benda tersusun melingkar, tanda mulainya ....", ["beri benda awal tanda atau warna khusus", "mulai dari mana saja tanpa tanda", "putar lingkaran cepat-cepat", "hitung tanpa berhenti"], "A", "Beri penanda pada benda pertama agar tahu kapan harus berhenti.")
tf("c4", "sulit", X, Me, S4, "Sikap tenang dan teliti mencegah kesalahan membilang.", "Benar", "Ketenangan membantu mata dan tangan bekerja selaras.")

# ── C5 SULIT (3 soal: 3 mandiri) ──────────────────────────────────────────
mc("c5", "sulit", X, Me, S3, "Budi hitung 14, Rani hitung 15. Berapa selisih hitungan mereka?", ["1", "2", "3", "0"], "A", "Lima belas dikurangi 14 berselisih satu.", verifikasi={"ekspresi": "15 - 14", "hasil": "1"})
mc("c5", "sulit", X, Kn, S2, "Di antara pilihan ini, mana kesalahan yang membuat angka berkurang?", ["melewatkan benda saat membilang", "menghitung benda dua kali", "menambah benda baru", "membilang angka dobel"], "A", "Melewatkan benda adalah satu-satunya yang membuat hasil berkurang.")
mc("c5", "sulit", X, Me, S4, "Sebelum menyerahkan tugas hitung, sikap terbaik siswa ....", ["menghitung ulang sekali lagi untuk cek", "langsung lari mengumpulkan buku", "menutup buku tanpa memeriksa", "mengganti jawaban secara acak"], "A", "Memeriksa ulang adalah sikap terbaik siswa sebelum mengumpulkan.")

# ── C6 SULIT (2 soal: 2 pengayaan) ────────────────────────────────────────
mc("c6", "sulit", P, Kn, S3, "Rancang aturan lomba menghitung biji congklak ....", ["peserta memindahkan biji satu per satu ke wadah", "peserta mengambil biji sekepalan tangan", "peserta menebak biji tanpa menyentuh", "peserta menghitung dari jarak jauh"], "A", "Memindahkan biji satu per satu adalah metode adil dan terukur.")
mc("c6", "sulit", P, Pr, S4, "Buatlah lembar periksa hitungan kelompok di kelas ....", ["sediakan kolom hitungan pertama dan hitungan kedua", "sediakan kolom gambar kartun saja", "tulis angka tanpa kotak hitung", "kosongkan seluruh lembar kertas"], "A", "Menyediakan kolom hitungan pertama dan kedua melatih kebiasaan cek ulang.")

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

uid = lambda i: str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab6_soal_{i}"))
groups = {"mc": [], "tf": [], "sa": []}

random.seed(46)
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
    ("Bahaya Menghitung Benda Dua Kali", S1),
    ("Bahaya Ada Benda Terlewat", S2),
    ("Strategi Menghitung Teliti", S3),
    ("Memeriksa Ulang Hitungan", S4)
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
    (S1, "Aku tahu bahaya menghitung benda dua kali.", "Bahaya Menghitung Benda Dua Kali",
f"""Kadang kita salah saat berhitung.
Satu benda disentuh dua kali.
Akibatnya angka menjadi terlalu banyak.

Contoh pada buah jeruk:
Ada 4 jeruk di meja.
Bila dihitung dua kali, jadi 5.
Jawaban itu keliru.
Satu benda hanya satu hitungan.

:::definition
term: Menghitung Dua Kali
definition: Menyentuh satu benda lebih dari satu kali sehingga jumlah berlebih.
:::

:::callout
variant: tip
title: Tips
text: Tunjuk satu benda sekali saja ya.
:::""", 3),

    (S2, "Aku tahu bahaya jika ada benda terlewat.", "Bahaya Ada Benda Terlewat",
f"""Ada juga kesalahan benda terlewat.
Mata kita melompati satu benda.
Akibatnya angka menjadi terlalu sedikit.

Contoh pada pensil warna:
Ada 6 pensil warna.
Bila satu terlewat, jadi 5.
Jawaban itu juga keliru.
Semua benda harus dihitung tuntas.

:::table
headers: ["Kesalahan","Akibat Hitungan"]
rows: [["dihitung dua kali.","terlalu banyak."],["benda terlewat.","terlalu sedikit."]]
caption: Akibat Kesalahan Berhitung
:::""", 4),

    (S3, "Aku bisa menggunakan cara cerdas berhitung teliti.", "Strategi Menghitung Teliti",
f"""Ayo gunakan cara cerdas berhitung.
Susun benda menjadi baris lurus.
Tunjuk benda dari kiri ke kanan.

Untuk gambar, beri coretan kecil.
Benda yang dicoret sudah terhitung.
Kamu juga bisa memindahkan bendanya.
Pindahkan ke kotak lain perlahan.

:::steps
title: Cara berhitung teliti
items: ["Susun benda berbaris lurus.","Tunjuk benda satu per satu.","Pindahkan atau coret benda yang selesai dihitung."]
:::""", 4),

    (S4, "Aku selalu memeriksa ulang hasil hitunganku.", "Memeriksa Ulang Hitungan",
f"""Setelah berhitung, periksa ulang lagi.
Hitung sekali lagi dari awal.
Pastikan jumlahnya tetap sama.
Hitungan teliti membuat kita percaya diri.

:::common_trap
term: Menghitung Benda Dua Kali atau Terlewat
explanation: Jangan tergesa-gesa. Tunjuk benda perlahan dengan tenang dari kiri ke kanan.
:::

:::callout
variant: summary
title: Ringkasan
text: Tunjuk tiap benda sekali. Jangan lewati benda. Periksa kembali hitunganmu.
:::""", 3),
]

lp = {
    "level": "Kelas 1 SD — Fase A",
    "title": "Kesalahan Umum: Menghitung Benda Dua Kali atau Terlewat",
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab6.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"lesson_plan": lp, "quiz_config": quiz}, f, ensure_ascii=False, indent=2)

print("BERHASIL:", out_path, "berhasil dibuat dan divalidasi!")
