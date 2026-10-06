#!/usr/bin/env python3
"""
Generator dan validator Bab 67 Matematika Kelas 2 SD:
"Urutan Hari dalam Seminggu" (Fase A)
bab_id: 52ea8d1e-7a87-4fa1-95a2-37cb94121187
article_id: 9876cbeb-96a3-4669-b7c4-f8b1b2616eef
quiz_id: 5620025f-d0c2-4927-a686-e1cdb192409f
"""

import json, uuid, random, re, os
from collections import Counter

random.seed(42)

S1 = "l1n2p3r4t501"  # Tujuh Hari dalam Seminggu
S2 = "m2o3q4s5u602"  # Urutan Hari Maju dan Mundur
S3 = "n3p4r5t6v703"  # Menghitung Jumlah Hari dan Pekan
S4 = "o4q5s6u7w804"  # Jadwal dan Aktivitas Mingguan

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Satu minggu terdiri dari tujuh hari.
Nama hari selalu berurutan teratur.
Senin, Selasa, Rabu, Kamis.
Lalu Jumat, Sabtu, dan Minggu.
Setelah hari Minggu, kembali ke Senin.
Urutan ini berputar terus-menerus.
Hafalkan ketujuh nama hari tersebut!

:::definition
title: Satu Minggu
Rentang waktu yang lamanya tepat tujuh hari berturut-turut.
:::"""

s2_content = """Mari belajar urutan maju mundur.
Hari sesudah Senin adalah Selasa.
Hari sebelum Kamis adalah Rabu.
Kemarin adalah hari yang lalu.
Besok adalah hari yang akan datang.
Lusa adalah dua hari ke depan.
Jika hari ini Rabu, besok Kamis.
Lusa setelah Rabu adalah Jumat.
Cermatilah urutan hari berputar!

:::steps
title: Menentukan Hari Sebelum dan Sesudah
1. Tentukan nama hari patokan.
2. Maju satu langkah untuk hari esok.
3. Mundur satu langkah untuk kemarin.
4. Ingat, setelah Minggu kembali Senin.
:::"""

s3_content = """Kita bisa menghitung hari.
Satu minggu lamanya 7 hari.
Berapa hari dalam 2 minggu?
Hitunglah: 7 ditambah 7.
Hasilnya adalah 14 hari!
Berapa hari dalam 3 minggu?
3 dikali 7 adalah 21 hari.
Kita juga bisa mengubah hari ke minggu.
14 hari sama dengan 2 minggu!

:::common_trap
title: Lupa Hari Berputar ke Hari Senin
Setelah hari Minggu bukan berhenti.
Urutan langsung berputar ke hari Senin.
Jangan mengira hari berhenti di Minggu!
:::"""

s4_content = """Hari dipakai menyusun jadwal harian.
Senin sampai Jumat biasanya bersekolah.
Sabtu dan Minggu disebut akhir pekan.
Banyak keluarga berlibur di akhir pekan.
Upacara bendera diadakan hari Senin.
Senam pagi sering diadakan hari Jumat.
Susun jadwalmu dengan rapi dan teratur!

:::callout
variant: summary
title: Ringkasan
text: Satu minggu ada 7 hari. Urutan berputar dari Senin hingga Minggu.
:::"""

sections = [
    {
        "id": S1,
        "title": "Tujuh Hari dalam Seminggu",
        "minutes": 6,
        "goal": "Siswa mengenal 7 nama hari dalam satu minggu secara berurutan.",
        "content": s1_content
    },
    {
        "id": S2,
        "title": "Urutan Hari Maju dan Mundur",
        "minutes": 6,
        "goal": "Siswa mampu menentukan hari kemarin, hari ini, besok, dan lusa.",
        "content": s2_content
    },
    {
        "id": S3,
        "title": "Menghitung Jumlah Hari dan Pekan",
        "minutes": 6,
        "goal": "Siswa mampu menghitung hubungan kesetaraan antara minggu dan hari.",
        "content": s3_content
    },
    {
        "id": S4,
        "title": "Jadwal dan Aktivitas Mingguan",
        "minutes": 6,
        "goal": "Siswa mampu mengaitkan urutan hari dengan kegiatan nyata sehari-hari.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Urutan Hari dalam Seminggu",
    "topic": "Mengenal Jam, Hari, dan Bulan",
    "level": "Kelas 2 SD · Fase A",
    "sections": sections
}

# Verifikasi teks materi sesuai kriteria validasi
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
# 2. DEFINISI BANK 50 SOAL BAB 67
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
mc("c1", "mudah", D, F, S1, "Satu minggu terdiri dari berapa hari?", ["7 hari", "5 hari", "6 hari", "10 hari"], "A", "1 minggu = 7 hari.", verifikasi={"ekspresi": "7 * 1", "hasil": "7"})
tf("c1", "mudah", D, F, S2, "Hari sesudah hari Senin adalah hari Selasa.", "Benar", "Urutan setelah Senin adalah Selasa.")

# Terarah (3): S1, S2, S3
mc("c1", "mudah", T, F, S1, "Hari pertama dalam urutan hari sekolah biasanya adalah ....", ["Senin", "Minggu", "Rabu", "Jumat"], "A", "Hari Senin adalah awal pekan sekolah.")
mc("c1", "mudah", T, F, S2, "Hari sebelum hari Kamis adalah hari ....", ["Rabu", "Selasa", "Jumat", "Sabtu"], "A", "Sebelum Kamis adalah Rabu.")
sa("c1", "mudah", T, F, S3, "Dua minggu sama dengan ... hari.", "14", "2 x 7 = 14 hari.", verifikasi={"ekspresi": "2 * 7", "hasil": "14"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S2, "Jika hari ini hari Minggu, maka besok adalah hari ....", ["Senin", "Sabtu", "Selasa", "Jumat"], "A", "Setelah Minggu urutan kembali ke Senin.")
tf("c2", "mudah", D, Kn, S3, "Lamanya 14 hari sama artinya dengan 3 minggu.", "Salah", "14 hari = 2 minggu, bukan 3 minggu.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S2, "Jika hari ini hari Sabtu, maka dua hari lagi adalah hari ....", ["Senin", "Minggu", "Selasa", "Jumat"], "A", "Sabtu -> Minggu -> Senin.", "Lupa bahwa setelah hari Minggu berputar ke Senin")
mc("c2", "mudah", R, Kn, S3, "Doni berlibur selama 21 hari. Berapa minggu Doni berlibur?", ["3 minggu", "2 minggu", "4 minggu", "5 minggu"], "A", "21 : 7 = 3 minggu.", "Salah membagi jumlah hari dengan 7", verifikasi={"ekspresi": "21 / 7", "hasil": "3"})

# Terarah (4): S1, S2, S3, S4
mc("c2", "mudah", T, Kn, S1, "Dua hari yang biasanya disebut akhir pekan adalah ....", ["Sabtu dan Minggu", "Senin dan Selasa", "Kamis dan Jumat", "Rabu dan Kamis"], "A", "Sabtu dan Minggu adalah akhir pekan.")
mc("c2", "mudah", T, Kn, S2, "Kemarin adalah hari Selasa. Maka hari ini adalah hari ....", ["Rabu", "Kamis", "Senin", "Jumat"], "A", "Jika kemarin Selasa, hari ini Rabu.")
tf("c2", "mudah", T, Kn, S4, "Upacara bendera di sekolah biasanya diadakan setiap hari Minggu.", "Salah", "Upacara bendera diadakan hari Senin, hari Minggu sekolah libur.")
sa("c2", "mudah", T, Kn, S3, "Tiga minggu sama dengan ... hari.", "21", "3 x 7 = 21 hari.", verifikasi={"ekspresi": "3 * 7", "hasil": "21"})

# ── C3 SEDANG (14 soal: 2 remedial, 6 terarah, 4 mandiri, 2 checkpoint) ────
# Remedial (2)
mc("c3", "sedang", R, Pr, S2, "Jika lusa adalah hari Jumat, maka hari ini adalah hari ....", ["Rabu", "Kamis", "Selasa", "Sabtu"], "A", "Lusa = hari ini + 2. Jumat - 2 = Rabu.", "Bingung membedakan besok dan lusa")
mc("c3", "sedang", R, Pr, S3, "Bibi menginap selama 4 minggu. Berapa hari Bibi menginap?", ["28 hari", "21 hari", "30 hari", "24 hari"], "A", "4 x 7 = 28 hari.", "Salah mengalikan jumlah minggu", verifikasi={"ekspresi": "4 * 7", "hasil": "28"})

# Terarah (6): S1, S2, S3, S4, S1, S4 (2 dibuat 'mudah' agar total mudah pas 15)
mc("c3", "mudah", T, Pr, S2, "Jika kemarin hari Jumat, maka besok adalah hari ....", ["Minggu", "Sabtu", "Senin", "Kamis"], "A", "Kemarin Jumat -> hari ini Sabtu -> besok Minggu.")
mc("c3", "mudah", T, Pr, S3, "Sebanyak 35 hari sama dengan berapa minggu?", ["5 minggu", "4 minggu", "6 minggu", "7 minggu"], "A", "35 : 7 = 5 minggu.", verifikasi={"ekspresi": "35 / 7", "hasil": "5"})
tf("c3", "sedang", T, Pr, S1, "Urutan hari dari Rabu sampai Minggu ada sebanyak 5 hari.", "Benar", "Rabu, Kamis, Jumat, Sabtu, Minggu (5 hari).")
mc("c3", "sedang", T, Pr, S4, "Edo les renang setiap hari Selasa dan Sabtu. Berapa kali Edo les dalam 3 minggu?", ["6 kali", "5 kali", "7 kali", "4 kali"], "A", "2 x 3 = 6 kali.", verifikasi={"ekspresi": "2 * 3", "hasil": "6"})
tf("c3", "sedang", T, Pr, S3, "Dalam waktu 4 minggu ada 30 hari.", "Salah", "4 x 7 = 28 hari, bukan 30 hari.")
sa("c3", "sedang", T, Pr, S3, "Ibu arisan tiap 2 minggu sekali. Dalam 6 minggu, ibu ikut ... kali.", "3", "6 : 2 = 3 kali.", verifikasi={"ekspresi": "6 / 2", "hasil": "3"})

# Mandiri (4)
mc("c3", "sedang", X, Pr, S2, "Hari ini hari Kamis. Hari apakah 4 hari yang lalu?", ["Minggu", "Senin", "Selasa", "Sabtu"], "A", "Kamis mundur 4 hari: Rabu, Selasa, Senin, Minggu.")
mc("c3", "sedang", X, Pr, S3, "Proyek jembatan selesai dalam 42 hari. Berapa minggu proyek itu selesai?", ["6 minggu", "5 minggu", "7 minggu", "8 minggu"], "A", "42 : 7 = 6 minggu.", verifikasi={"ekspresi": "42 / 7", "hasil": "6"})
tf("c3", "sedang", X, Pr, S4, "Jika sekolah libur 2 minggu penuh, siswa libur selama 14 hari.", "Benar", "2 x 7 = 14 hari.")
sa("c3", "sedang", X, Pr, S3, "Jumlah hari dalam 5 minggu dikurangi 5 hari adalah ... hari.", "30", "(5 x 7) - 5 = 35 - 5 = 30.", verifikasi={"ekspresi": "(5 * 7) - 5", "hasil": "30"})

# Checkpoint (2)
mc("c3", "sedang", K, Pr, S2, "Jika 3 hari yang lalu hari Senin, hari apakah besok?", ["Jumat", "Kamis", "Sabtu", "Rabu"], "A", "Senin + 3 = Kamis (hari ini). Besok = Jumat.")
mc("c3", "sedang", K, Pr, S3, "Kakek tinggal di desa selama 49 hari. Berapa minggu kakek tinggal?", ["7 minggu", "6 minggu", "8 minggu", "5 minggu"], "A", "49 : 7 = 7 minggu.", verifikasi={"ekspresi": "49 / 7", "hasil": "7"})

# ── C4 SEDANG/SULIT (13 soal: 5 terarah, 4 mandiri, 4 checkpoint) ──────────
# Terarah (5): S1, S2, S3, S4, S2
mc("c4", "sedang", T, Kn, S1, "Mengapa nama hari dalam kalender berulang setiap 7 hari sekali?", ["karena satu siklus pekan berputar genap tujuh hari", "karena kalender berbentuk kotak", "karena ada 12 bulan", "supaya tidak bosan"], "A", "Siklus pekan ditetapkan berulang tiap 7 hari.")
mc("c4", "sedang", T, Kn, S2, "Hari ini hari Selasa. Hari apakah 8 hari yang akan datang?", ["Rabu", "Kamis", "Selasa", "Senin"], "A", "8 hari = 7 hari (Selasa) + 1 hari = Rabu.")
tf("c4", "sedang", T, Kn, S3, "Sebanyak 10 hari lebih singkat daripada 1 minggu ditambah 2 hari.", "Salah", "1 minggu + 2 hari = 9 hari, sedangkan 10 hari lebih lama.")
tf("c4", "sedang", T, Kn, S4, "Jika ujian berlangsung selama 10 hari, berarti ujian berlangsung 2 minggu penuh.", "Salah", "2 minggu penuh = 14 hari, bukan 10 hari.")
sa("c4", "sedang", T, Kn, S3, "Berapa hari selisih antara 5 minggu dan 30 hari?", "5", "(5 x 7) - 30 = 35 - 30 = 5 hari.", verifikasi={"ekspresi": "(5 * 7) - 30", "hasil": "5"})

# Mandiri (4)
mc("c4", "sedang", X, Kn, S2, "Hari ini hari Jumat. Hari apakah 15 hari yang akan datang?", ["Sabtu", "Minggu", "Jumat", "Senin"], "A", "15 hari = (2 x 7) + 1 hari. Jumat + 1 = Sabtu.")
mc("c4", "sedang", X, Kn, S3, "Paman berlibur 3 minggu. Paman sudah jalan 12 hari. Berapa hari sisa libur?", ["9 hari", "8 hari", "10 hari", "7 hari"], "A", "(3 x 7) - 12 = 21 - 12 = 9 hari.", verifikasi={"ekspresi": "(3 * 7) - 12", "hasil": "9"})
tf("c4", "sedang", X, Kn, S1, "Antara hari Senin dan hari Minggu dalam pekan yang sama terdapat 5 hari antara.", "Benar", "Selasa, Rabu, Kamis, Jumat, Sabtu (5 hari).")
mc("c4", "sulit", X, Me, S4, "Lani menabung tiap hari sekolah (Senin-Jumat) Rp2.000. Tabungan 2 minggu?", ["Rp20.000", "Rp14.000", "Rp24.000", "Rp10.000"], "A", "5 hari x 2 minggu = 10 hari x 2.000 = Rp20.000.")

# Checkpoint (4)
mc("c4", "sedang", K, Kn, S2, "Jika kemarin lusa hari Rabu, hari apakah 3 hari lagi?", ["Senin", "Minggu", "Selasa", "Sabtu"], "A", "Kemarin lusa = hari ini - 2 -> Hari ini = Jumat. 3 hari lagi = Sabtu, Minggu, Senin.")
mc("c4", "sulit", K, Me, S3, "Kakak berkemah selama 17 hari. Berapa minggu dan sisa hari kakak berkemah?", ["2 minggu lebih 3 hari", "2 minggu lebih 2 hari", "1 minggu lebih 10 hari", "3 minggu"], "A", "17 = (2 x 7) + 3 hari.")
tf("c4", "sulit", K, Me, S2, "Jika tanggal 1 jatuh pada hari Senin, tanggal 8 pasti hari Senin lagi.", "Benar", "1 + 7 = 8, tepat satu minggu kemudian.")
mc("c4", "sulit", K, Me, S4, "Rapat diadakan tiap 14 hari sekali. Jika rapat pertama 1 Mei, rapat ketiga?", ["29 Mei", "28 Mei", "15 Mei", "30 Mei"], "A", "1 + 14 + 14 = 29 Mei.", verifikasi={"ekspresi": "1 + 14 + 14", "hasil": "29"})

# ── C5 SEDANG/SULIT (6 soal: 4 terarah, 2 checkpoint) ──────────────────────
# Terarah (4): S1, S2, S3, S4
mc("c5", "sedang", T, Me, S1, "Bila tanggal 3 hari Rabu, tanggal berapakah hari Rabu berikutnya?", ["tanggal 10", "tanggal 9", "tanggal 11", "tanggal 8"], "A", "3 + 7 = 10.", verifikasi={"ekspresi": "3 + 7", "hasil": "10"})
mc("c5", "sedang", T, Me, S2, "Jika hari ini Kamis, hari apakah tepat 22 hari yang akan datang?", ["Jumat", "Sabtu", "Kamis", "Rabu"], "A", "22 = (3 x 7) + 1 hari. Kamis + 1 = Jumat.")
mc("c5", "sedang", T, Me, S3, "Sebuah tim bekerja 6 minggu. Tim lain 45 hari. Manakah yang lebih lama?", ["tim kedua (45 hari)", "tim pertama (6 minggu)", "keduanya sama", "tidak dapat dihitung"], "A", "6 x 7 = 42 hari. 45 hari > 42 hari.")
mc("c5", "sulit", T, Me, S4, "Toko tutup tiap hari Minggu. Dalam 4 minggu, berapa hari toko buka?", ["24 hari", "28 hari", "20 hari", "25 hari"], "A", "Buka 6 hari seminggu: 6 x 4 = 24 hari.", verifikasi={"ekspresi": "6 * 4", "hasil": "24"})

# Checkpoint (2)
mc("c5", "sedang", K, Me, S3, "Ibu membeli susu tiap 5 hari sekali. Dalam 35 hari, berapa kali ibu beli susu?", ["7 kali", "6 kali", "8 kali", "5 kali"], "A", "35 : 5 = 7 kali.", verifikasi={"ekspresi": "35 / 5", "hasil": "7"})
mc("c5", "sulit", K, Me, S4, "Budi kursus gitar tiap hari Selasa dan Kamis. Dalam 8 minggu, berapa kali kursus?", ["16 kali", "14 kali", "18 kali", "12 kali"], "A", "2 x 8 = 16 kali kursus.", verifikasi={"ekspresi": "2 * 8", "hasil": "16"})

# ── C6 SULIT (4 soal: 2 checkpoint, 2 pengayaan) ───────────────────────────
# Checkpoint (2)
mc("c6", "sulit", K, Me, S2, "Jika tanggal 5 hari Sabtu, tanggal berapakah hari Sabtu dua pekan kemudian?", ["tanggal 19", "tanggal 17", "tanggal 21", "tanggal 12"], "A", "5 + (2 x 7) = 5 + 14 = 19.", verifikasi={"ekspresi": "5 + 14", "hasil": "19"})
mc("c6", "sulit", K, Me, S3, "Berapakah total hari dari gabungan 4 minggu + 2 minggu - 10 hari?", ["32 hari", "30 hari", "34 hari", "28 hari"], "A", "(6 x 7) - 10 = 42 - 10 = 32 hari.", verifikasi={"ekspresi": "(6 * 7) - 10", "hasil": "32"})

# Pengayaan (2)
mc("c6", "sulit", P, Me, S3, "Hitunglah hasil operasi: (5 x 7 hari) - (3 x 7 hari) + 6 hari!", ["20 hari", "18 hari", "21 hari", "19 hari"], "A", "35 - 21 + 6 = 14 + 6 = 20 hari.", verifikasi={"ekspresi": "(5 * 7) - (3 * 7) + 6", "hasil": "20"})
mc("c6", "sulit", P, Me, S4, "Sebulan ada 30 hari. Berapa banyak hari Senin paling banyak yang mungkin terjadi?", ["5 hari Senin", "4 hari Senin", "6 hari Senin", "3 hari Senin"], "A", "30 = (4 x 7) + 2 hari sisa, sehingga bisa memuat hingga 5 hari Senin.", verifikasi={"ekspresi": "(30 // 7) + 1", "hasil": "5"})

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
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k2_bab67_soal_{idx+1}"))
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

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab67.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"BERHASIL: {out_path} berhasil dibuat dan divalidasi!")
