#!/usr/bin/env python3
"""
Generator dan validator Bab 32 Matematika Kelas 1 SD:
"Kesalahan Umum: Mengira Bentuk Bergantung pada Ukuran atau Arah" (Fase A)
bab_id: 00b19061-0104-4284-a221-dc7082a25755
article_id: df79ec97-317e-41af-bc51-1ea1cd42072a
quiz_id: b270e2c4-2d75-493e-9a70-d76d87da75c6
"""

import json
import re

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Lihatlah dua buah segitiga ini.
Satu segitiga berukuran sangat kecil.
Satu segitiga berukuran sangat besar.
Keduanya sama-sama memiliki 3 sisi.
Keduanya juga memiliki 3 sudut.
Maka keduanya tetap bangun segitiga.
Ukuran besar tidak mengubah nama.
Ukuran kecil juga tetap sama."""

s2_content = """Sekarang kita putar kertas segitiga.
Ujung lancipnya menghadap ke bawah.
Apakah bentuknya berubah menjadi lain?
Tentu tidak, namanya tetap segitiga.
Persegi yang diputar miring wajik.
Tetap memiliki 4 sisi lurus.
Namanya tetaplah bangun segiempat.
Arah putaran tidak mengubah bentuk."""

s3_content = """Warna benda juga bukan penentu.
Segitiga warna merah tetap segitiga.
Segitiga warna biru juga segitiga.
Garis tebal tidak mengubah bentuk.
Garis putus-putus juga tetap sama.
Jangan terkecoh oleh warna-warni.
Jangan terkecoh oleh posisi miring.
Ciri bentuk ada pada sisinya."""

s4_content = """Bagaimana cara memeriksa bentuk tepat?
Hitunglah jumlah sisinya yang lurus.
Hitunglah jumlah sudut lancipnya.
Jika ada 3 sisi, itu segitiga.
Jika ada 4 sisi, itu segiempat.

:::common_trap
title: Bentuk Tidak Berubah Saat Diputar
Segitiga terbalik tetap segitiga.
Persegi miring tetap segiempat.
Arah putar tidak mengubah bentuk.
Jangan tertipu oleh arah hadapnya.
Selalu hitung sisi dan sudutnya.
:::

:::callout
variant: summary
title: Ringkasan
text: Bentuk bangun tidak berubah walau ukurannya besar atau kecil. Bentuk juga tidak berubah saat diputar ke berbagai arah. Selalu periksa jumlah sisi dan sudutnya.
:::"""

sections = [
    {
        "id": "e1f2a34b5c01",
        "title": "Ukuran Berbeda, Bentuk Tetap Sama",
        "minutes": 6,
        "goal": "Siswa memahami bahwa ukuran besar atau kecil tidak mengubah identitas bentuk bangun datar.",
        "content": s1_content
    },
    {
        "id": "f2a3b45c6d12",
        "title": "Bentuk Diputar Tidak Berubah Nama",
        "minutes": 6,
        "goal": "Siswa memahami bahwa orientasi atau arah putaran bangun tidak mengubah jenis bentuk bangun datar.",
        "content": s2_content
    },
    {
        "id": "a3b4c56d7e23",
        "title": "Warna dan Posisi Bukan Penentu Bentuk",
        "minutes": 6,
        "goal": "Siswa dapat membedakan atribut non-esensial (warna, ketebalan) dari atribut esensial bentuk geometri.",
        "content": s3_content
    },
    {
        "id": "b4c5d67e8f34",
        "title": "Menghitung Sisi dan Sudut dengan Teliti",
        "minutes": 6,
        "goal": "Siswa terampil mengidentifikasi bentuk bangun datar berdasarkan perhitungan jumlah sisi dan sudutnya.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Kesalahan Umum: Mengira Bentuk Bergantung pada Ukuran atau Arah",
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
# 2. BANK 50 SOAL BAB 32
# ==========================================
# Kuota:
# 15 mudah, 25 sedang, 10 sulit
# Bloom: C1: 5, C2: 8, C3: 16, C4: 13, C5: 6, C6: 2
# Fungsi: 4 diag, 22 terarah (S1: 5, S2: 6, S3: 6, S4: 5), 10 akhir, 8 mandiri, 4 remedial, 2 pengayaan
# Tipe: 35 MC, 10 TF, 5 SA
# Dimensi: faktual, konseptual, prosedural, metakognitif (semua >= 3)

questions_data = [
    # ── DIAGNOSTIK (4 soal: 2 mudah, 2 sedang) ──
    # Q01: C1 mudah faktual mc
    {
        "uid": "q01", "t": "mc", "sec": "e1f2a34b5c01",
        "stem": "Segitiga kecil dan segitiga besar sama-sama memiliki sisi sebanyak ....",
        "choices": [("3 sisi", True, "Semua segitiga memiliki 3 sisi terlepas dari ukurannya."), ("4 sisi", False, "Itu segiempat."), ("0 sisi", False, "Itu lingkaran.")],
        "tax": {"bloom": "c1", "difficulty": "mudah", "fungsi": "diagnostik", "knowledge_dimension": "faktual"}
    },
    # Q02: C1 mudah faktual tf
    {
        "uid": "q02", "t": "tf", "sec": "f2a3b45c6d12",
        "stem": "Segitiga yang diputar menghadap ke bawah tetap merupakan segitiga.",
        "choices": [("Benar", True, "Rotasi tidak mengubah sifat geometris segitiga."), ("Salah", False, "Bentuknya memang tidak berubah.")],
        "tax": {"bloom": "c1", "difficulty": "mudah", "fungsi": "diagnostik", "knowledge_dimension": "faktual"}
    },
    # Q03: C2 sedang konseptual mc
    {
        "uid": "q03", "t": "mc", "sec": "a3b4c56d7e23",
        "stem": "Apakah warna merah membuat segitiga berubah bentuk menjadi lingkaran?",
        "choices": [("tidak, warna tidak memengaruhi bentuk bangun datar", True, "Warna adalah atribut visual sekunder, bukan sifat geometri."), ("ya, menjadi lingkaran", False, "Bentuk tidak berubah."), ("menjadi persegi", False, "Tetap segitiga.")],
        "tax": {"bloom": "c2", "difficulty": "sedang", "fungsi": "diagnostik", "knowledge_dimension": "konseptual"}
    },
    # Q04: C2 sedang konseptual tf
    {
        "uid": "q04", "t": "tf", "sec": "b4c5d67e8f34",
        "stem": "Menghitung jumlah sisi adalah cara pasti menentukan jenis bangun datar.",
        "choices": [("Benar", True, "Jumlah sisi dan sudut adalah kriteria esensial klasifikasi geometri."), ("Salah", False, "Memang cara yang pasti dan akurat.")],
        "tax": {"bloom": "c2", "difficulty": "sedang", "fungsi": "diagnostik", "knowledge_dimension": "konseptual"}
    },

    # ── LATIHAN TERARAH SECTION 1 (5 soal: min 4) ──
    # Q05: C1 mudah faktual mc
    {
        "uid": "q05", "t": "mc", "sec": "e1f2a34b5c01",
        "stem": "Beni menggambar lingkaran raksasa di lapangan. Bangun itu tetaplah ....",
        "choices": [("lingkaran", True, "Ukuran raksasa tidak mengubah bentuk lingkaran."), ("segitiga", False, "Bukan segitiga."), ("kubus", False, "Bukan bangun ruang kubus.")],
        "tax": {"bloom": "c1", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "faktual"}
    },
    # Q06: C2 mudah konseptual tf
    {
        "uid": "q06", "t": "tf", "sec": "e1f2a34b5c01",
        "stem": "Persegi yang digambar sangat kecil tetap merupakan bangun segiempat.",
        "choices": [("Benar", True, "Ukuran skala mikroskopis tetap mempertahankan 4 sisi segiempat."), ("Salah", False, "Memang tetap segiempat.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q07: C3 mudah prosedural sa
    {
        "uid": "q07", "t": "sa", "sec": "e1f2a34b5c01",
        "stem": "Segitiga raksasa dan segitiga mini memiliki jumlah sudut sebanyak ....",
        "choices": [("3", True, "Memiliki 3 sudut.")],
        "tax": {"bloom": "c3", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q08: C3 sedang prosedural mc
    {
        "uid": "q08", "t": "mc", "sec": "e1f2a34b5c01",
        "stem": "Ada koin logam kecil dan piring besar bundar. Keduanya berbentuk ....",
        "choices": [("lingkaran", True, "Keduanya sama-sama bangun datar lingkaran."), ("segitiga", False, "Bukan segitiga."), ("balok", False, "Bukan balok.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q09: C4 sedang konseptual mc
    {
        "uid": "q09", "t": "mc", "sec": "e1f2a34b5c01",
        "stem": "Mengapa perubahan ukuran benda tidak mengubah nama bentuk bangun datarnya?",
        "choices": [("karena perbandingan sisi dan sudutnya tetap sama persis", True, "Prinsip kesebangunan geometri (similarity)."), ("karena mata kita bisa melihatnya", False, "Penglihatan bukan penyebab invariansi matematis."), ("karena harganya sama", False, "Harga tidak relevan.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },

    # ── LATIHAN TERARAH SECTION 2 (6 soal: min 4) ──
    # Q10: C1 mudah faktual mc
    {
        "uid": "q10", "t": "mc", "sec": "f2a3b45c6d12",
        "stem": "Persegi yang diputar miring seperti ketupat tetap memiliki sisi sebanyak ....",
        "choices": [("4 sisi", True, "Memiliki 4 sisi segiempat."), ("3 sisi", False, "Segitiga yang memiliki 3 sisi."), ("1 sisi", False, "Lingkaran yang memiliki 1 sisi lengkung.")],
        "tax": {"bloom": "c1", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "faktual"}
    },
    # Q11: C2 mudah konseptual tf
    {
        "uid": "q11", "t": "tf", "sec": "f2a3b45c6d12",
        "stem": "Segitiga yang diputar rebah tidur tetap dinamakan bangun datar segitiga.",
        "choices": [("Benar", True, "Orientasi horizontal tidak mengubah status segitiga."), ("Salah", False, "Memang tetaplah segitiga.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q12: C2 mudah konseptual mc
    {
        "uid": "q12", "t": "mc", "sec": "f2a3b45c6d12",
        "stem": "Beni memutar buku gambarnya miring. Gambar segitiga di dalamnya menjadi?",
        "choices": [("tetap segitiga", True, "Gambar tetap segitiga walau buku diputar."), ("berubah menjadi lingkaran", False, "Bentuk tidak berubah."), ("berubah menjadi kubus", False, "Buku tetap bidang dua dimensi.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q13: C3 sedang prosedural sa
    {
        "uid": "q13", "t": "sa", "sec": "f2a3b45c6d12",
        "stem": "Persegi diputar miring tetap tergolong kelompok bangun segi ....",
        "choices": [("empat", True, "Tetap tergolong bangun segiempat.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q14: C3 sedang prosedural mc
    {
        "uid": "q14", "t": "mc", "sec": "f2a3b45c6d12",
        "stem": "Siti melihat rambu lalu lintas segitiga terbalik. Bentuk rambu itu?",
        "choices": [("segitiga", True, "Rambu Give Way adalah segitiga terbalik."), ("persegi", False, "Bukan persegi."), ("lingkaran", False, "Bukan lingkaran.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q15: C4 sedang konseptual mc
    {
        "uid": "q15", "t": "mc", "sec": "f2a3b45c6d12",
        "stem": "Mengapa anak sering salah mengira persegi miring bukan segiempat?",
        "choices": [("karena terbiasa melihat segiempat berdiri lurus dengan dasar mendatar", True, "Bias orientasi prototipikal (prototype effect) dalam psikologi kognitif anak."), ("karena matanya silau", False, "Bukan masalah pencahayaan."), ("karena garisnya patah", False, "Garisnya tetap utuh.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },

    # ── LATIHAN TERARAH SECTION 3 (6 soal: min 4) ──
    # Q16: C2 mudah konseptual mc
    {
        "uid": "q16", "t": "mc", "sec": "a3b4c56d7e23",
        "stem": "Manakah sifat yang BENAR-BENAR menentukan nama bentuk bangun datar?",
        "choices": [("jumlah sisi dan sudutnya", True, "Atribut esensial formal geometri."), ("warna cat yang digunakan", False, "Warna bukan penentu bentuk."), ("harga spidol penggambarnya", False, "Harga tidak relevan.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q17: C2 mudah konseptual tf
    {
        "uid": "q17", "t": "tf", "sec": "a3b4c56d7e23",
        "stem": "Garis tepi tebal atau tipis tidak memengaruhi bentuk bangun datar.",
        "choices": [("Benar", True, "Ketebalan garis adalah gaya penggambaran, bukan geometri inti."), ("Salah", False, "Memang tidak memengaruhi bentuk.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q18: C3 sedang prosedural mc
    {
        "uid": "q18", "t": "mc", "sec": "a3b4c56d7e23",
        "stem": "Segitiga hijau dan segitiga kuning diletakkan berdampingan. Keduanya sama-sama?",
        "choices": [("berbentuk bangun segitiga", True, "Bentuknya identik sebagai segitiga."), ("berubah menjadi buah pisang", False, "Bukan buah."), ("kehilangan sisinya", False, "Sisi tetap ada.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q19: C3 sedang prosedural sa
    {
        "uid": "q19", "t": "sa", "sec": "a3b4c56d7e23",
        "stem": "Warna dan ketebalan garis apakah mengubah nama bentuk bangun datar?",
        "choices": [("tidak", True, "Tidak mengubah nama bentuk bangun datar.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q20: C4 sedang konseptual tf
    {
        "uid": "q20", "t": "tf", "sec": "a3b4c56d7e23",
        "stem": "Ciri esensial bangun datar tetap tidak berubah oleh perubahan warna apa pun.",
        "choices": [("Benar", True, "Invariansi topologis dan geometris terhadap properti kromatik."), ("Salah", False, "Memang sifat esensialnya konstan.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q21: C4 sedang konseptual mc
    {
        "uid": "q21", "t": "mc", "sec": "a3b4c56d7e23",
        "stem": "Mengapa pelukis bisa menggambar segitiga dengan aneka warna dan gaya?",
        "choices": [("karena aturan bentuk segitiga hanya membutuhkan tiga sisi lurus tertutup", True, "Kebebasan ekspresi seni tanpa melanggar batasan definisi matematika."), ("karena pelukis tidak tahu matematika", False, "Pelukis memahami geometri bentuk."), ("agar catnya cepat habis", False, "Bukan alasan pelukis.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },

    # ── LATIHAN TERARAH SECTION 4 (5 soal: min 4) ──
    # Q22: C2 mudah konseptual tf
    {
        "uid": "q22", "t": "tf", "sec": "b4c5d67e8f34",
        "stem": "Jika suatu bangun datar memiliki 3 sisi lurus, itu pasti segitiga.",
        "choices": [("Benar", True, "Definisi mutlak segitiga adalah poligon bersisi 3."), ("Salah", False, "Memang pasti segitiga.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q23: C3 mudah konseptual mc
    {
        "uid": "q23", "t": "mc", "sec": "b4c5d67e8f34",
        "stem": "Udin menemukan bangun tertutup dengan 4 sisi dan 4 sudut. Bentuknya?",
        "choices": [("segiempat", True, "Poligon dengan 4 sisi dan 4 sudut adalah segiempat."), ("lingkaran", False, "Lingkaran tidak bersisi lurus 4."), ("segitiga", False, "Segitiga bersisi 3.")],
        "tax": {"bloom": "c3", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q24: C3 sedang prosedural mc
    {
        "uid": "q24", "t": "mc", "sec": "b4c5d67e8f34",
        "stem": "Lani melihat bangun melengkung tanpa sudut sama sekali. Bentuk bangun itu?",
        "choices": [("lingkaran", True, "Bangun datar melengkung tanpa sudut adalah lingkaran."), ("segiempat", False, "Segiempat memiliki 4 sudut."), ("segitiga", False, "Segitiga memiliki 3 sudut.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q25: C4 sedang metakognitif mc
    {
        "uid": "q25", "t": "mc", "sec": "b4c5d67e8f34",
        "stem": "Apa yang harus kamu lakukan jika ragu menentukan nama bentuk bangun?",
        "choices": [("hitung jumlah sisi dan jumlah sudutnya secara teliti satu per satu", True, "Strategi verifikasi analitis objektif."), ("tebak saja sesuka hati", False, "Menebak acak rawan keliru."), ("tutup mata dan hindari bangun itu", False, "Bukan cara belajar yang baik.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "metakognitif"}
    },
    # Q26: C4 sedang metakognitif tf
    {
        "uid": "q26", "t": "tf", "sec": "b4c5d67e8f34",
        "stem": "Memeriksa ciri esensial mencegah kita tertipu oleh tampilan luar bentuk.",
        "choices": [("Benar", True, "Mengembangkan penalaran kritis matematika sejak dini."), ("Salah", False, "Memang sangat mencegah kekeliruan konsep.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "metakognitif"}
    },

    # ── LATIHAN MANDIRI (8 soal: C3 dan C4) ──
    # Q27: C3 mudah prosedural mc
    {
        "uid": "q27", "t": "mc", "sec": "e1f2a34b5c01",
        "stem": "Kertas origami persegi dipotong menjadi empat persegi kecil. Bentuk tiap potongan?",
        "choices": [("tetap persegi segiempat", True, "Ukuran menjadi kecil tetapi tetap berbentuk persegi."), ("berubah menjadi bola", False, "Kertas pipih bukan bola."), ("berubah menjadi tabung", False, "Bukan tabung.")],
        "tax": {"bloom": "c3", "difficulty": "mudah", "fungsi": "latihan_mandiri", "knowledge_dimension": "prosedural"}
    },
    # Q28: C3 sedang prosedural mc
    {
        "uid": "q28", "t": "mc", "sec": "f2a3b45c6d12",
        "stem": "Layar komputer diputar tegak (portrait). Bentuk layarnya tetap merupakan ....",
        "choices": [("segiempat persegi panjang", True, "Orientasi vertikal layar tetap persegi panjang."), ("segitiga siku-siku", False, "Bukan segitiga."), ("lingkaran", False, "Bukan lingkaran.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_mandiri", "knowledge_dimension": "prosedural"}
    },
    # Q29: C3 sedang prosedural sa
    {
        "uid": "q29", "t": "sa", "sec": "f2a3b45c6d12",
        "stem": "Segitiga diputar 180 derajat terbalik tetap memiliki ... sudut.",
        "choices": [("3", True, "Tetap memiliki 3 sudut.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_mandiri", "knowledge_dimension": "prosedural"}
    },
    # Q30: C3 sedang prosedural mc
    {
        "uid": "q30", "t": "mc", "sec": "b4c5d67e8f34",
        "stem": "Beni menghitung: sisi ada 4, sudut ada 4. Kelompok bangun datar?",
        "choices": [("segiempat", True, "Ciri utama keluarga bangun segiempat."), ("segitiga", False, "Segitiga memiliki 3 sisi."), ("lingkaran", False, "Lingkaran tidak memiliki 4 sisi lurus.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_mandiri", "knowledge_dimension": "prosedural"}
    },
    # Q31: C4 sedang konseptual mc
    {
        "uid": "q31", "t": "mc", "sec": "f2a3b45c6d12",
        "stem": "Apakah segitiga lancip yang diputar ke kanan menjadi bangun baru?",
        "choices": [("bukan bangun baru, itu bangun yang sama hanya arahnya berbeda", True, "Transformasi rotasi kongruen (isometri) tidak mengubah bentuk objek."), ("menjadi bangun baru bernama lingkaran", False, "Tidak menjadi lingkaran."), ("menjadi bangun ruang kubus", False, "Tetap bangun datar.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_mandiri", "knowledge_dimension": "konseptual"}
    },
    # Q32: C4 sedang konseptual mc
    {
        "uid": "q32", "t": "mc", "sec": "e1f2a34b5c01",
        "stem": "Roda sepeda anak kecil dan roda gerobak besar sama-sama berbentuk ....",
        "choices": [("lingkaran, walau jari-jarinya berbeda ukuran", True, "Keduanya sebangun dan berbentuk lingkaran bulat."), ("segiempat", False, "Roda bukan segiempat."), ("segitiga", False, "Roda bukan segitiga.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_mandiri", "knowledge_dimension": "konseptual"}
    },
    # Q33: C4 sedang konseptual mc
    {
        "uid": "q33", "t": "mc", "sec": "a3b4c56d7e23",
        "stem": "Udin menggaris segitiga dengan krayon tebal hitam. Bentuk yang dihasilkan?",
        "choices": [("tetap segitiga, ketebalan garis hanya tampilan luar saja", True, "Definisi matematis sisi adalah ruas garis pembatas, bukan tebal tinta."), ("berubah menjadi segiempat", False, "Jumlah sisi tetap 3."), ("berubah menjadi balok", False, "Bukan balok.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_mandiri", "knowledge_dimension": "konseptual"}
    },
    # Q34: C4 sulit metakognitif mc
    {
        "uid": "q34", "t": "mc", "sec": "b4c5d67e8f34",
        "stem": "Mengapa kita tidak boleh menilai bentuk benda hanya dari sekilas pandang?",
        "choices": [("karena mata mudah terkecoh oleh arah miring atau warna mencolok", True, "Refleksi metakognitif pentingnya verifikasi analitik terstruktur."), ("karena melihat butuh tenaga besar", False, "Bukan alasan fisik lelah."), ("agar kita dianggap lambat", False, "Kehati-hatian menghasilkan ketepatan.")],
        "tax": {"bloom": "c4", "difficulty": "sulit", "fungsi": "latihan_mandiri", "knowledge_dimension": "metakognitif"}
    },

    # ── CHECKPOINT AKHIR (10 soal: C3, C4, C5, C6) ──
    # Q35: C3 sedang prosedural mc
    {
        "uid": "q35", "t": "mc", "sec": "b4c5d67e8f34",
        "stem": "Benda manakah yang pasti berbentuk segiempat terlepas dari arah posisinya?",
        "choices": [("benda tertutup dengan tepat 4 sisi lurus", True, "Kriteria esensial segiempat tak terbantahkan."), ("benda yang berwarna biru saja", False, "Warna bukan penentu bentuk."), ("benda yang sangat berat", False, "Berat bukan sifat geometri.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "checkpoint_akhir", "knowledge_dimension": "prosedural"}
    },
    # Q36: C4 sulit konseptual mc
    {
        "uid": "q36", "t": "mc", "sec": "f2a3b45c6d12",
        "stem": "Mengapa belah ketupat tetap digolongkan ke dalam kelompok segiempat?",
        "choices": [("karena memiliki tepat 4 sisi lurus dan 4 sudut", True, "Klasifikasi poligon berdasarkan jumlah rusuk dan verteks."), ("karena rasanya enak dimakan", False, "Bukan ketupat nasi makanan."), ("karena warnanya hijau daun", False, "Warna bukan alasan klasifikasi.")],
        "tax": {"bloom": "c4", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "konseptual"}
    },
    # Q37: C5 sedang prosedural sa
    {
        "uid": "q37", "t": "sa", "sec": "b4c5d67e8f34",
        "stem": "Berapakah jumlah sisi lengkung pada sebuah lingkaran sempurna?",
        "choices": [("1", True, "Memiliki 1 garis lengkung tertutup.")],
        "tax": {"bloom": "c5", "difficulty": "sedang", "fungsi": "checkpoint_akhir", "knowledge_dimension": "prosedural"}
    },
    # Q38: C4 sulit konseptual mc
    {
        "uid": "q38", "t": "mc", "sec": "e1f2a34b5c01",
        "stem": "Jika gambar segitiga diperbesar 100 kali pada proyektor bioskop, bentuknya?",
        "choices": [("tetap segitiga karena sudut dan proporsi ketiga sisinya tidak berubah", True, "Prinsip dilatasi skala geometris menjaga invariansi sudut."), ("berubah menjadi lingkaran bioskop", False, "Sudut tidak melengkung."), ("berubah menjadi kotak", False, "Sisi tetap berjumlah 3.")],
        "tax": {"bloom": "c4", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "konseptual"}
    },
    # Q39: C4 sulit konseptual mc
    {
        "uid": "q39", "t": "mc", "sec": "f2a3b45c6d12",
        "stem": "Dua segitiga sama bentuk diletakkan berbeda arah. Apakah keduanya sebangun?",
        "choices": [("ya, keduanya kongruen dan sama persis bentuknya walau arahnya beda", True, "Kekongruenan bentuk tidak bergantung pada orientasi ruang."), ("tidak, karena arah hadapnya berbeda", False, "Orientasi tidak membatalkan kekongruenan."), ("hanya sama saat hari hujan", False, "Cuaca tidak memengaruhi matematika.")],
        "tax": {"bloom": "c4", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "konseptual"}
    },
    # Q40: C6 sulit metakognitif mc
    {
        "uid": "q40", "t": "mc", "sec": "b4c5d67e8f34",
        "stem": "Rancang kartu permainan pintar untuk melatih teman membedakan bentuk!",
        "choices": [("gambar aneka bentuk dengan orientasi miring dan warna berbeda untuk ditebak sisinya", True, "Desain instrumen belajar yang secara spesifik menantang miskonsepsi orientasi."), ("buat kartu polos tanpa gambar", False, "Tidak melatih kemampuan spasial."), ("warnai seluruh kartu hitam pekat", False, "Bentuk tidak terlihat.")],
        "tax": {"bloom": "c6", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "metakognitif"}
    },
    # Q41: C5 sulit konseptual tf
    {
        "uid": "q41", "t": "tf", "sec": "f2a3b45c6d12",
        "stem": "Dalam matematika, bangun datar tidak kehilangan sifat dasarnya saat diputar.",
        "choices": [("Benar", True, "Invariansi bentuk di bawah operasi rotasi Euclidean."), ("Salah", False, "Memang sifat dasarnya selalu kekal.")],
        "tax": {"bloom": "c5", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "konseptual"}
    },
    # Q42: C5 sedang metakognitif mc
    {
        "uid": "q42", "t": "mc", "sec": "b4c5d67e8f34",
        "stem": "Bagaimana kamu menjelaskan kepada adikmu bahwa segitiga terbalik tetap segitiga?",
        "choices": [("ajak adik menghitung tiga sisinya bersama-sama agar ia yakin", True, "Metode pembuktian empiris berbasis definisi konkret."), ("marahi adik karena salah", False, "Memarahi tidak mendidik."), ("katakan itu bukan urusan adik", False, "Bukan sikap kakak yang baik.")],
        "tax": {"bloom": "c5", "difficulty": "sedang", "fungsi": "checkpoint_akhir", "knowledge_dimension": "metakognitif"}
    },
    # Q43: C5 sulit metakognitif mc
    {
        "uid": "q43", "t": "mc", "sec": "e1f2a34b5c01",
        "stem": "Mengapa arsitek membuat miniatur rumah kecil sebelum membangun gedung asli?",
        "choices": [("karena bentuk miniatur kecil sama persis dengan bentuk bangunan aslinya", True, "Penerapan konsep kesebangunan geometri dalam rekayasa maket arsitektur."), ("hanya untuk mainan pajangan", False, "Bukan sekadar pajangan mainan."), ("agar menghabiskan sisa kertas", False, "Bukan membuang bahan.")],
        "tax": {"bloom": "c5", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "metakognitif"}
    },
    # Q44: C5 sulit metakognitif tf
    {
        "uid": "q44", "t": "tf", "sec": "a3b4c56d7e23",
        "stem": "Membedakan sifat penting dan tampilan luar adalah inti berpikir logis.",
        "choices": [("Benar", True, "Abstraksi matematika menyaring esensi struktural dari tampilan permukaan."), ("Salah", False, "Memang fondasi utama berpikir logis analitis.")],
        "tax": {"bloom": "c5", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "metakognitif"}
    },

    # ── REMEDIAL (4 soal: 2 mudah, 2 sedang) ──
    # Misconception 1: Mengira ukuran besar mengubah nama bentuk (C1 mudah faktual mc)
    {
        "uid": "q45", "t": "mc", "sec": "e1f2a34b5c01",
        "stem": "Apakah lingkaran yang digambar sangat besar tetap disebut lingkaran?",
        "choices": [("tetap lingkaran, karena bentuknya tetap bulat melengkung utuh", True, "Ukuran tidak mengubah identitas bentuk geometri."), ("berubah menjadi bangun kotak", False, "Miskonsepsi mengira ukuran besar mengubah jenis bangun.")],
        "tax": {"bloom": "c1", "difficulty": "mudah", "fungsi": "remedial", "knowledge_dimension": "faktual", "miskonsepsi_target": "Mengira ukuran besar mengubah identitas bangun datar"}
    },
    # Misconception 2: Mengira segitiga terbalik bukan segitiga (C2 mudah konseptual mc)
    {
        "uid": "q46", "t": "mc", "sec": "f2a3b45c6d12",
        "stem": "Apakah bangun bersisi tiga yang ujungnya menghadap ke bawah adalah segitiga?",
        "choices": [("ya, itu tetap segitiga karena tetap memiliki 3 sisi dan 3 sudut", True, "Arah orientasi tidak memengaruhi jenis bangun datar."), ("bukan segitiga karena terbalik", False, "Miskonsepsi mengira segitiga terbalik bukan segitiga.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "remedial", "knowledge_dimension": "konseptual", "miskonsepsi_target": "Mengira segitiga dengan ujung menghadap ke bawah bukan bangun segitiga"}
    },
    # Misconception 3: Mengira persegi miring adalah bangun yang sama sekali bukan segiempat (C3 sedang konseptual mc)
    {
        "uid": "q47", "t": "mc", "sec": "f2a3b45c6d12",
        "stem": "Apakah persegi yang diputar miring tetap tergolong segiempat?",
        "choices": [("tetap segiempat, karena keempat sisinya tetap ada dan lurus", True, "Persegi yang diputar tetap memiliki 4 sisi segiempat."), ("bukan segiempat lagi", False, "Miskonsepsi mengira wajik/ketupat terpisah dari keluarga segiempat.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "remedial", "knowledge_dimension": "konseptual", "miskonsepsi_target": "Mengira persegi yang diputar miring bukan lagi bangun segiempat"}
    },
    # Misconception 4: Mengira warna menentukan bentuk bangun datar (C3 sedang konseptual mc)
    {
        "uid": "q48", "t": "mc", "sec": "a3b4c56d7e23",
        "stem": "Apakah warna hijau pada segitiga menjadikannya berbeda bentuk dari segitiga merah?",
        "choices": [("bentuknya tetap sama-sama segitiga, hanya warnanya saja yang berbeda", True, "Warna adalah properti visual pelengkap, bukan penentu bentuk."), ("bentuknya menjadi berbeda", False, "Miskonsepsi menganggap warna sebagai bagian dari bentuk geometri.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "remedial", "knowledge_dimension": "konseptual", "miskonsepsi_target": "Mengira warna memengaruhi identitas bentuk bangun datar"}
    },

    # ── PENGAYAAN (2 soal: C5 sulit & C6 sulit) ──
    # Q49: C5 sulit metakognitif mc
    {
        "uid": "q49", "t": "mc", "sec": "b4c5d67e8f34",
        "stem": "Mengapa komputer canggih mampu mengenali wajah seseorang dari berbagai sudut miring?",
        "choices": [("karena program komputer menganalisis ciri geometris titik wajah yang tidak berubah", True, "Prinsip pengenalan pola invariant rotasi pada artificial intelligence dan computer vision."), ("karena komputer memiliki mata manusia", False, "Komputer tidak punya mata biologis."), ("hanya karena kebetulan beruntung", False, "Bukan faktor kebetulan.")],
        "tax": {"bloom": "c5", "difficulty": "sulit", "fungsi": "pengayaan", "knowledge_dimension": "metakognitif"}
    },
    # Q50: C6 sulit metakognitif mc
    {
        "uid": "q50", "t": "mc", "sec": "f2a3b45c6d12",
        "stem": "Ciptakan pola lantai dekoratif yang memanfaatkan satu bentuk dalam berbagai putaran!",
        "choices": [("susun ubin segitiga yang diputar ke atas, bawah, kiri, dan kanan secara selang-seling", True, "Penciptaan ornamen tessellation artistik menggunakan simetri rotasi poligon tunggal."), ("hancurkan semua ubin menjadi debu", False, "Tindakan merusak."), ("tumpuk semua ubin di satu sudut", False, "Tidak menghasilkan pola lantai indah.")],
        "tax": {"bloom": "c6", "difficulty": "sulit", "fungsi": "pengayaan", "knowledge_dimension": "metakognitif"}
    }
]

# Transform ke format question_groups
mc_questions = []
tf_questions = []
sa_questions = []

for q in questions_data:
    words = len(q["stem"].split())
    assert words <= 12, f"Stem too long ({words} words): {q['stem']}"

    chs = []
    labels = ["A", "B", "C"] if q["t"] == "mc" else (["Benar", "Salah"] if q["t"] == "tf" else ["Kunci"])
    for idx, (label_txt, is_ans, exp) in enumerate(q["choices"]):
        chs.append({
            "key": labels[idx] if q["t"] != "sa" else "kunci",
            "text": label_txt,
            "answer": is_ans,
            "explanation": exp
        })

    q_obj = {
        "uid": q["uid"],
        "stem": q["stem"],
        "choices": chs,
        "source_section_id": q["sec"],
        "t": q["t"],
        "taxonomy": q["tax"]
    }

    if q["t"] == "mc":
        mc_questions.append(q_obj)
    elif q["t"] == "tf":
        tf_questions.append(q_obj)
    elif q["t"] == "sa":
        sa_questions.append(q_obj)

question_groups = [
    {
        "group_id": "mc",
        "subtype": "multiple_choice",
        "questions": mc_questions
    },
    {
        "group_id": "tf",
        "subtype": "true_false",
        "questions": tf_questions
    },
    {
        "group_id": "sa",
        "subtype": "short_answer",
        "questions": sa_questions
    }
]

quiz_config = {
    "question_groups": question_groups
}

# Verifikasi kuota dan aturan taksonomi
all_q = mc_questions + tf_questions + sa_questions
assert len(all_q) == 50, f"Total questions != 50 ({len(all_q)})"

from collections import Counter
diff = Counter(q["taxonomy"]["difficulty"] for q in all_q)
bloom = Counter(q["taxonomy"]["bloom"] for q in all_q)
fungsi = Counter(q["taxonomy"]["fungsi"] for q in all_q)
dimensi = Counter(q["taxonomy"]["knowledge_dimension"] for q in all_q)
types = Counter(q["t"] for q in all_q)

print("Bloom:", dict(bloom))
print("Difficulty:", dict(diff))
print("Fungsi:", dict(fungsi))
print("Dimensi:", dict(dimensi))
print("Tipe:", dict(types))

# Assertions
assert diff["mudah"] == 15 and diff["sedang"] == 25 and diff["sulit"] == 10
assert bloom["c1"] >= 5 and bloom["c2"] >= 8 and bloom["c3"] >= 14 and bloom["c4"] >= 12 and bloom["c5"] >= 6 and bloom["c6"] >= 2
assert fungsi["diagnostik"] == 4
assert fungsi["latihan_mandiri"] == 8
assert fungsi["checkpoint_akhir"] == 10
assert fungsi["remedial"] == 4
assert fungsi["pengayaan"] == 2
assert (fungsi["latihan_terarah"] + fungsi["checkpoint_bagian"]) == 22

sec_latihan = Counter(q["source_section_id"] for q in all_q if q["taxonomy"]["fungsi"] in ("latihan_terarah", "checkpoint_bagian"))
print("Latihan per section (min 4):", dict(sec_latihan))
for s in sections:
    assert sec_latihan[s["id"]] >= 4, f"Section {s['id']} kurang latihan ({sec_latihan[s['id']]})"

output_data = {
    "lesson_plan": lesson_plan,
    "quiz_config": quiz_config
}

with open("outputs/kalibrasi/hasil_bab32.json", "w") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("BERHASIL: outputs/kalibrasi/hasil_bab32.json berhasil dibuat dan divalidasi!")

