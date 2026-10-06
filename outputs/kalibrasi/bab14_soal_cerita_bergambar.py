#!/usr/bin/env python3
"""
Generator dan validator Bab 14 Matematika Kelas 1 SD:
"Soal Cerita Bergambar: Menambah dan Mengurangi" (Fase A)
bab_id: e88e9977-ea2b-4b9a-8f41-f988cf3a1cfc
article_id: 559d9edd-f35e-4b20-846a-f3d0772986f1
quiz_id: 8d360013-8d88-4dca-bc8c-15eed54b6b8e
"""

import json
import re

# ==========================================
# 1. MATERI (LESSON PLAN) SESUAI PROFIL FASE A
# ==========================================
s1_content = """Cerita matematika ada di sekitar kita.
Perhatikan kata kunci yang menambah.
Kata diberi lagi artinya bertambah.
Kata membeli lagi artinya bertambah.
Kata datang lagi juga bertambah.
Benda akan menjadi lebih banyak.
Kita gunakan tanda tambah (+).
Hitunglah semua benda dengan teliti."""

s2_content = """Ada juga cerita yang mengurangi.
Perhatikan kata kunci yang berkurang.
Kata dimakan artinya benda berkurang.
Kata pecah artinya benda berkurang.
Kata diberikan artinya benda berkurang.
Benda menjadi lebih sedikit.
Kita gunakan tanda kurang (-).
Coretlah gambar yang hilang."""

s3_content = """Ayo tentukan operasinya dengan tepat.
Tanyakan: apakah benda bertambah banyak?
Jika bertambah banyak, gunakan tambah.
Tanyakan: apakah benda berkurang?
Jika berkurang, gunakan kurang.
Bayangkan kejadian dalam cerita itu.
Lalu pilihlah tanda yang benar."""

s4_content = """Sekarang kita buat kalimat matematikanya.
Ada 8 ikan di kolam.
Paman memasukkan 4 ikan lagi.
Kalimatnya adalah 8 + 4 = 12.
Ada 12 ikan sekarang.

:::common_trap
title: Terjebak Kata Tanpa Memahami Alur Cerita
Jangan hanya mencari satu kata.
Pahami apa yang terjadi pada benda.
Apakah bendanya bertambah banyak?
Atau bendanya menjadi lebih sedikit?
Bayangkan ceritanya seperti menonton film.
:::

:::callout
variant: summary
title: Ringkasan
text: Kata membeli lagi artinya ditambah (+). Kata dimakan atau pecah artinya dikurangi (-). Pahami cerita sebelum menghitung.
:::"""

sections = [
    {
        "id": "a4b3c29d5e01",
        "title": "Membaca Gambar dan Kata Kunci Menambah",
        "minutes": 6,
        "goal": "Siswa dapat mengenali kata kunci dan situasi cerita bergambar yang menggunakan operasi penjumlahan.",
        "content": s1_content
    },
    {
        "id": "b5c4d30e6f12",
        "title": "Membaca Gambar dan Kata Kunci Mengurangi",
        "minutes": 6,
        "goal": "Siswa dapat mengenali kata kunci dan situasi cerita bergambar yang menggunakan operasi pengurangan.",
        "content": s2_content
    },
    {
        "id": "c6d5e41f7a23",
        "title": "Memilih Tambah atau Kurang",
        "minutes": 6,
        "goal": "Siswa dapat membedakan situasi kontekstual yang membutuhkan penjumlahan atau pengurangan.",
        "content": s3_content
    },
    {
        "id": "d7e6f52a8b34",
        "title": "Menulis Kalimat Matematika dari Cerita",
        "minutes": 6,
        "goal": "Siswa dapat menyusun dan menyelesaikan kalimat matematika berdasarkan alur soal cerita bergambar.",
        "content": s4_content
    }
]

lesson_plan = {
    "title": "Soal Cerita Bergambar: Menambah dan Mengurangi",
    "topic": "Penjumlahan dan Pengurangan sampai 20",
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
# 2. BANK 50 SOAL BAB 14
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
        "uid": "q01", "t": "mc", "sec": "a4b3c29d5e01",
        "stem": "Kata 'membeli lagi' dalam soal cerita menandakan operasi ....",
        "choices": [("penjumlahan (+)", True, "Membeli lagi menambah banyak benda."), ("pengurangan (-)", False, "Benda tidak berkurang."), ("pembagian", False, "Bukan pembagian.")],
        "tax": {"bloom": "c1", "difficulty": "mudah", "fungsi": "diagnostik", "knowledge_dimension": "faktual"}
    },
    # Q02: C1 mudah faktual tf
    {
        "uid": "q02", "t": "tf", "sec": "b5c4d30e6f12",
        "stem": "Kata 'pecah' pada balon menandakan balon menjadi berkurang.",
        "choices": [("Benar", True, "Balon yang pecah tidak bisa dihitung lagi."), ("Salah", False, "Balon memang berkurang.")],
        "tax": {"bloom": "c1", "difficulty": "mudah", "fungsi": "diagnostik", "knowledge_dimension": "faktual"}
    },
    # Q03: C2 sedang konseptual mc
    {
        "uid": "q03", "t": "mc", "sec": "c6d5e41f7a23",
        "stem": "Ada 5 bebek, berenang pergi 2 bebek. Menggunakan tanda?",
        "choices": [("tanda kurang (-)", True, "Bebek pergi berarti berkurang: 5 - 2."), ("tanda tambah (+)", False, "Bebek tidak bertambah."), ("tanda sama dengan saja", False, "Perlu tanda operasi kurang.")],
        "tax": {"bloom": "c2", "difficulty": "sedang", "fungsi": "diagnostik", "knowledge_dimension": "konseptual"}
    },
    # Q04: C2 sedang konseptual tf
    {
        "uid": "q04", "t": "tf", "sec": "d7e6f52a8b34",
        "stem": "Cerita 6 kelereng diberi lagi 3 ditulis 6 + 3.",
        "choices": [("Benar", True, "Diberi lagi adalah penjumlahan 6 + 3."), ("Salah", False, "Kalimat matematika ini sudah benar.")],
        "tax": {"bloom": "c2", "difficulty": "sedang", "fungsi": "diagnostik", "knowledge_dimension": "konseptual"}
    },

    # ── LATIHAN TERARAH SECTION 1 (5 soal: min 4) ──
    # Q05: C1 mudah faktual mc
    {
        "uid": "q05", "t": "mc", "sec": "a4b3c29d5e01",
        "stem": "Kata manakah yang artinya benda BERTAMBAH BANYAK?",
        "choices": [("diberi hadiah", True, "Diberi hadiah membuat benda bertambah."), ("hilang", False, "Hilang artinya berkurang."), ("rusak", False, "Rusak artinya berkurang.")],
        "tax": {"bloom": "c1", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "faktual"}
    },
    # Q06: C2 mudah konseptual tf
    {
        "uid": "q06", "t": "tf", "sec": "a4b3c29d5e01",
        "stem": "Anak ayam menetas membuat jumlah anak ayam bertambah.",
        "choices": [("Benar", True, "Menetas menambah jumlah anak ayam hidup."), ("Salah", False, "Ayam memang bertambah banyak.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q07: C3 mudah prosedural sa
    {
        "uid": "q07", "t": "sa", "sec": "a4b3c29d5e01",
        "stem": "Ada 4 bunga di vas, dipetikkan 3 lagi. Jumlahnya?",
        "choices": [("7", True, "4 + 3 = 7 bunga.")],
        "tax": {"bloom": "c3", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q08: C3 sedang prosedural mc
    {
        "uid": "q08", "t": "mc", "sec": "a4b3c29d5e01",
        "stem": "Rani punya 6 jepit, dibelikan 5 jepit lagi. Jepitnya?",
        "choices": [("11 jepit", True, "6 + 5 = 11 jepit."), ("10 jepit", False, "Kurang satu."), ("12 jepit", False, "Kelebihan satu.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q09: C4 sedang konseptual mc
    {
        "uid": "q09", "t": "mc", "sec": "a4b3c29d5e01",
        "stem": "Manakah gambar cerita yang menunjukkan peristiwa bertambah?",
        "choices": [("burung datang hinggap di pohon", True, "Burung datang menambah kawanan."), ("burung terbang menjauh", False, "Itu berkurang."), ("burung tidur di sarang", False, "Jumlahnya tetap.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },

    # ── LATIHAN TERARAH SECTION 2 (6 soal: min 4) ──
    # Q10: C1 mudah faktual mc
    {
        "uid": "q10", "t": "mc", "sec": "b5c4d30e6f12",
        "stem": "Kata 'diberikan kepada adik' artinya benda menjadi ....",
        "choices": [("berkurang", True, "Memberikan benda mengurangi kepemilikan kita."), ("bertambah", False, "Bukan bertambah."), ("tetap sama", False, "Benda sudah berpindah tangan.")],
        "tax": {"bloom": "c1", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "faktual"}
    },
    # Q11: C2 mudah konseptual mc
    {
        "uid": "q11", "t": "mc", "sec": "b5c4d30e6f12",
        "stem": "Ada 9 kue, dimakan 4 kue. Sisa kue adalah ....",
        "choices": [("5 kue", True, "9 - 4 = 5 kue."), ("4 kue", False, "Kurang satu."), ("6 kue", False, "Kelebihan satu.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q12: C2 mudah konseptual tf
    {
        "uid": "q12", "t": "tf", "sec": "b5c4d30e6f12",
        "stem": "Gambar permen dicoret tanda silang menandakan permen berkurang.",
        "choices": [("Benar", True, "Tanda silang melambangkan pengurangan."), ("Salah", False, "Tanda silang memang berarti berkurang.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q13: C3 sedang prosedural sa
    {
        "uid": "q13", "t": "sa", "sec": "b5c4d30e6f12",
        "stem": "Ada 10 balon, meletus 3 balon. Sisa balon?",
        "choices": [("7", True, "10 - 3 = 7 balon.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q14: C3 sedang prosedural mc
    {
        "uid": "q14", "t": "mc", "sec": "b5c4d30e6f12",
        "stem": "Paman punya 8 pensil, hilang 3 pensil. Pensil paman?",
        "choices": [("5 pensil", True, "8 - 3 = 5 pensil."), ("6 pensil", False, "Kurang teliti."), ("4 pensil", False, "Kurang satu pensil.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q15: C4 sedang konseptual mc
    {
        "uid": "q15", "t": "mc", "sec": "b5c4d30e6f12",
        "stem": "Mengapa kata 'jatuh dan pecah' diselesaikan dengan pengurangan?",
        "choices": [("karena telur yang pecah tidak utuh lagi", True, "Benda yang rusak berkurang dari jumlah awal."), ("hanya kesepakatan soal", False, "Bukan sekadar kesepakatan."), ("karena jatuh itu ke bawah", False, "Bukan alasan arah fisik.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },

    # ── LATIHAN TERARAH SECTION 3 (6 soal: min 4) ──
    # Q16: C2 mudah konseptual mc
    {
        "uid": "q16", "t": "mc", "sec": "c6d5e41f7a23",
        "stem": "Andi punya 7 buku, dipinjam teman 2. Operasinya?",
        "choices": [("7 - 2", True, "Dipinjam berarti berkurang: 7 - 2."), ("7 + 2", False, "Dipinjam bukan bertambah."), ("7 = 2", False, "Tidak ada tanda operasi.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q17: C2 mudah konseptual tf
    {
        "uid": "q17", "t": "tf", "sec": "c6d5e41f7a23",
        "stem": "Ibu memetik 4 mangga lalu memetik 5 lagi diselesaikan penjumlahan.",
        "choices": [("Benar", True, "Memetik lagi menambah mangga: 4 + 5."), ("Salah", False, "Benar diselesaikan penjumlahan.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q18: C3 sedang prosedural mc
    {
        "uid": "q18", "t": "mc", "sec": "c6d5e41f7a23",
        "stem": "Beni punya 12 kelereng, menang 4 kelereng. Sekarang ada?",
        "choices": [("16 kelereng", True, "Menang artinya bertambah: 12 + 4 = 16."), ("8 kelereng", False, "Menang bukan berkurang."), ("15 kelereng", False, "Kurang satu kelereng.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q19: C3 sedang prosedural sa
    {
        "uid": "q19", "t": "sa", "sec": "c6d5e41f7a23",
        "stem": "Ada 15 apel di keranjang, diambil 5. Sisanya?",
        "choices": [("10", True, "15 - 5 = 10 apel.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q20: C4 sedang konseptual tf
    {
        "uid": "q20", "t": "tf", "sec": "c6d5e41f7a23",
        "stem": "Memahami alur cerita lebih penting daripada sekadar menghafal kata.",
        "choices": [("Benar", True, "Makna alur kejadian menentukan operasi hitung."), ("Salah", False, "Pemahaman alur cerita memang sangat penting.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q21: C4 sedang konseptual mc
    {
        "uid": "q21", "t": "mc", "sec": "c6d5e41f7a23",
        "stem": "Manakah cerita yang diselesaikan dengan operasi 8 + 6?",
        "choices": [("8 semut di tanah, datang lagi 6 semut", True, "Datang lagi adalah penjumlahan 8 + 6."), ("8 semut di tanah, mati 6 semut", False, "Mati adalah 8 - 6."), ("8 semut masuk ke lubang", False, "Bukan operasi 8 + 6.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },

    # ── LATIHAN TERARAH SECTION 4 (5 soal: min 4) ──
    # Q22: C3 mudah konseptual tf
    {
        "uid": "q22", "t": "tf", "sec": "d7e6f52a8b34",
        "stem": "Cerita 'Ada 9 burung, terbang 3' ditulis 9 - 3 = 6.",
        "choices": [("Benar", True, "Kalimat matematika dan hasil sudah tepat."), ("Salah", False, "Kalimat matematika ini sudah benar.")],
        "tax": {"bloom": "c3", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "konseptual"}
    },
    # Q23: C3 mudah prosedural mc
    {
        "uid": "q23", "t": "mc", "sec": "d7e6f52a8b34",
        "stem": "Siti punya 7 stiker, diberi kakak 4. Berapa stikernya?",
        "choices": [("11 stiker", True, "7 + 4 = 11 stiker."), ("10 stiker", False, "Kurang satu."), ("12 stiker", False, "Kelebihan satu.")],
        "tax": {"bloom": "c3", "difficulty": "mudah", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q24: C3 sedang prosedural mc
    {
        "uid": "q24", "t": "mc", "sec": "d7e6f52a8b34",
        "stem": "Ada 14 kue di piring, dimakan tamu 6. Sisanya?",
        "choices": [("8 kue", True, "14 - 6 = 8 kue."), ("7 kue", False, "Kurang teliti."), ("9 kue", False, "Kelebihan satu kue.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "prosedural"}
    },
    # Q25: C4 sedang metakognitif mc
    {
        "uid": "q25", "t": "mc", "sec": "d7e6f52a8b34",
        "stem": "Langkah awal terbaik saat membaca soal cerita adalah ....",
        "choices": [("membayangkan peristiwa bendanya di dalam pikiran", True, "Visualisasi memudahkan memahami bertambah atau berkurang."), ("langsung menjumlahkan semua angka", False, "Bisa salah jika ceritanya pengurangan."), ("menebak jawaban acak", False, "Bisa salah tebak.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "metakognitif"}
    },
    # Q26: C4 sedang metakognitif tf
    {
        "uid": "q26", "t": "tf", "sec": "d7e6f52a8b34",
        "stem": "Membuat gambar sederhana mempermudah menyelesaikan soal cerita.",
        "choices": [("Benar", True, "Gambar konkret memvisualisasikan masalah."), ("Salah", False, "Gambar sangat membantu anak SD.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_terarah", "knowledge_dimension": "metakognitif"}
    },

    # ── LATIHAN MANDIRI (8 soal: C3 dan C4) ──
    # Q27: C3 mudah prosedural mc
    {
        "uid": "q27", "t": "mc", "sec": "a4b3c29d5e01",
        "stem": "Ada 5 kelinci, lahir lagi 4 kelinci. Kelincinya?",
        "choices": [("9 kelinci", True, "5 + 4 = 9 kelinci."), ("8 kelinci", False, "Bukan 8."), ("10 kelinci", False, "Bukan 10.")],
        "tax": {"bloom": "c3", "difficulty": "mudah", "fungsi": "latihan_mandiri", "knowledge_dimension": "prosedural"}
    },
    # Q28: C3 sedang prosedural mc
    {
        "uid": "q28", "t": "mc", "sec": "b5c4d30e6f12",
        "stem": "Ada 13 mobil di parkiran, keluar 5 mobil. Sisanya?",
        "choices": [("8 mobil", True, "13 - 5 = 8 mobil."), ("7 mobil", False, "Kurang satu."), ("9 mobil", False, "Kelebihan satu mobil.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_mandiri", "knowledge_dimension": "prosedural"}
    },
    # Q29: C3 sedang prosedural sa
    {
        "uid": "q29", "t": "sa", "sec": "d7e6f52a8b34",
        "stem": "Ada 8 manggis, dibeli lagi 8 manggis. Jumlahnya?",
        "choices": [("16", True, "8 + 8 = 16 manggis.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_mandiri", "knowledge_dimension": "prosedural"}
    },
    # Q30: C3 sedang prosedural mc
    {
        "uid": "q30", "t": "mc", "sec": "c6d5e41f7a23",
        "stem": "Beni punya 11 roti, dibagikan ke teman 3. Rotinya?",
        "choices": [("8 roti", True, "11 - 3 = 8 roti."), ("7 roti", False, "Kurang satu."), ("9 roti", False, "Kelebihan satu roti.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "latihan_mandiri", "knowledge_dimension": "prosedural"}
    },
    # Q31: C4 sedang konseptual mc
    {
        "uid": "q31", "t": "mc", "sec": "d7e6f52a8b34",
        "stem": "Kalimat matematika untuk 'ada 7 kambing, dibeli 6 lagi'?",
        "choices": [("7 + 6 = 13", True, "Bentuk kalimat matematika yang tepat."), ("7 - 6 = 1", False, "Membeli lagi bukan berkurang."), ("7 + 6 = 14", False, "Hasil jumlahnya salah.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_mandiri", "knowledge_dimension": "konseptual"}
    },
    # Q32: C4 sedang konseptual mc
    {
        "uid": "q32", "t": "mc", "sec": "b5c4d30e6f12",
        "stem": "Pohon mangga berbuah 16 buah, rontok 7 buah. Sisanya?",
        "choices": [("9 buah", True, "16 - 7 = 9 buah."), ("8 buah", False, "Kurang teliti."), ("10 buah", False, "Kelebihan satu.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_mandiri", "knowledge_dimension": "konseptual"}
    },
    # Q33: C4 sedang konseptual mc
    {
        "uid": "q33", "t": "mc", "sec": "a4b3c29d5e01",
        "stem": "Di rak ada 9 komik, Ayah menaruh 7 komik. Komiknya?",
        "choices": [("16 komik", True, "9 + 7 = 16 komik."), ("15 komik", False, "Hanya 15."), ("17 komik", False, "Kelebihan satu.")],
        "tax": {"bloom": "c4", "difficulty": "sedang", "fungsi": "latihan_mandiri", "knowledge_dimension": "konseptual"}
    },
    # Q34: C4 sulit metakognitif mc
    {
        "uid": "q34", "t": "mc", "sec": "c6d5e41f7a23",
        "stem": "Mengapa kita tidak boleh asal menambah semua angka di soal?",
        "choices": [("karena ada peristiwa yang mengurangi jumlah benda", True, "Tidak semua soal cerita adalah pertambahan."), ("karena gurunya galak", False, "Bukan alasan matematika."), ("agar cepat selesai", False, "Harus teliti membaca alurnya.")],
        "tax": {"bloom": "c4", "difficulty": "sulit", "fungsi": "latihan_mandiri", "knowledge_dimension": "metakognitif"}
    },

    # ── CHECKPOINT AKHIR (10 soal: C3, C4, C5, C6) ──
    # Q35: C3 sedang prosedural mc
    {
        "uid": "q35", "t": "mc", "sec": "d7e6f52a8b34",
        "stem": "Ada 15 pensil warna, patah 4 pensil. Pensil utuh?",
        "choices": [("11 pensil", True, "15 - 4 = 11 pensil utuh."), ("10 pensil", False, "Kurang satu."), ("12 pensil", False, "Kelebihan satu.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "checkpoint_akhir", "knowledge_dimension": "prosedural"}
    },
    # Q36: C4 sulit konseptual mc
    {
        "uid": "q36", "t": "mc", "sec": "c6d5e41f7a23",
        "stem": "Riko punya 8 kelereng, diberi Ayah beberapa hingga jadi 14. Berapa?",
        "choices": [("6 kelereng", True, "14 - 8 = 6 kelereng."), ("5 kelereng", False, "8 + 5 baru 13."), ("7 kelereng", False, "8 + 7 adalah 15.")],
        "tax": {"bloom": "c4", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "konseptual"}
    },
    # Q37: C5 sedang prosedural sa
    {
        "uid": "q37", "t": "sa", "sec": "d7e6f52a8b34",
        "stem": "Ada 9 buku, disumbangkan 4 buku. Berapa sisa buku?",
        "choices": [("5", True, "9 - 4 = 5 buku.")],
        "tax": {"bloom": "c5", "difficulty": "sedang", "fungsi": "checkpoint_akhir", "knowledge_dimension": "prosedural"}
    },
    # Q38: C4 sulit konseptual mc
    {
        "uid": "q38", "t": "mc", "sec": "d7e6f52a8b34",
        "stem": "Ada 18 kue di meja, dimakan 9 kue. Sisa kue?",
        "choices": [("9 kue", True, "18 - 9 = 9 kue."), ("8 kue", False, "Kurang satu."), ("10 kue", False, "Kelebihan satu kue.")],
        "tax": {"bloom": "c4", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "konseptual"}
    },
    # Q39: C4 sulit konseptual mc
    {
        "uid": "q39", "t": "mc", "sec": "a4b3c29d5e01",
        "stem": "Di akuarium ada 10 ikan, dimasukkan 7 ikan lagi. Ikannya?",
        "choices": [("17 ekor", True, "10 + 7 = 17 ekor ikan."), ("16 ekor", False, "Kurang satu."), ("18 ekor", False, "Kelebihan satu.")],
        "tax": {"bloom": "c4", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "konseptual"}
    },
    # Q40: C6 sulit metakognitif mc
    {
        "uid": "q40", "t": "mc", "sec": "d7e6f52a8b34",
        "stem": "Rancang cerita matematika yang sesuai untuk bentuk 15 - 7!",
        "choices": [("ada 15 balon, meletus 7 balon", True, "Cerita pengurangan yang sangat tepat."), ("ada 15 balon, ditiup 7 balon lagi", False, "Itu pertambahan: 15 + 7."), ("ada 7 balon dibagikan ke 15 anak", False, "Bukan bentuk 15 - 7.")],
        "tax": {"bloom": "c6", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "metakognitif"}
    },
    # Q41: C5 sulit konseptual tf
    {
        "uid": "q41", "t": "tf", "sec": "c6d5e41f7a23",
        "stem": "Soal 'mencari selisih tinggi dua anak' diselesaikan dengan pengurangan.",
        "choices": [("Benar", True, "Selisih tinggi dicari dengan mengurangkan."), ("Salah", False, "Mencari selisih memang menggunakan pengurangan.")],
        "tax": {"bloom": "c5", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "konseptual"}
    },
    # Q42: C5 sedang metakognitif mc
    {
        "uid": "q42", "t": "mc", "sec": "d7e6f52a8b34",
        "stem": "Bagaimana cara memeriksa kembali jawaban soal cerita matematika?",
        "choices": [("cocokkan hasil hitungan dengan alur cerita bendanya", True, "Pastikan jawaban masuk akal dengan jalan cerita."), ("baca soalnya sepuluh kali cepat-cepat", False, "Bukan cara mengecek."), ("hitung hanya angka terakhir", False, "Harus dicek secara menyeluruh.")],
        "tax": {"bloom": "c5", "difficulty": "sedang", "fungsi": "checkpoint_akhir", "knowledge_dimension": "metakognitif"}
    },
    # Q43: C5 sulit metakognitif mc
    {
        "uid": "q43", "t": "mc", "sec": "b5c4d30e6f12",
        "stem": "Jika jawabanmu 10 balon pecah 3 adalah 13, apa kelirumu?",
        "choices": [("kamu menjumlahkan padahal balon pecah harusnya dikurangi", True, "Balon pecah berkurang: 10 - 3 = 7, bukan 13."), ("kurang teliti menghitung tambah", False, "Operasinya salah bukan penjumlahan."), ("lupa menulis satuannya", False, "Operasi hitungnya yang keliru.")],
        "tax": {"bloom": "c5", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "metakognitif"}
    },
    # Q44: C5 sulit metakognitif tf
    {
        "uid": "q44", "t": "tf", "sec": "d7e6f52a8b34",
        "stem": "Mengecek apakah jawaban masuk akal mencegah kesalahan fatal berhitung.",
        "choices": [("Benar", True, "Pengecekan logika cerita menjamin ketepatan."), ("Salah", False, "Pengecekan logika memang sangat mencegah salah.")],
        "tax": {"bloom": "c5", "difficulty": "sulit", "fungsi": "checkpoint_akhir", "knowledge_dimension": "metakognitif"}
    },

    # ── REMEDIAL (4 soal: 2 mudah, 2 sedang) ──
    # Misconception 1: Menjumlahkan saat benda hilang/pecah (C1 mudah faktual mc)
    {
        "uid": "q45", "t": "mc", "sec": "b5c4d30e6f12",
        "stem": "Bila ada 5 telur lalu pecah 2 butir, operasinya adalah ....",
        "choices": [("pengurangan (5 - 2 = 3)", True, "Telur pecah membuat sisa telur berkurang."), ("penjumlahan (5 + 2 = 7)", False, "Telur pecah tidak menambah jumlah telur utuh.")],
        "tax": {"bloom": "c1", "difficulty": "mudah", "fungsi": "remedial", "knowledge_dimension": "faktual", "miskonsepsi_target": "Menggunakan operasi penjumlahan pada kejadian benda pecah atau hilang"}
    },
    # Misconception 2: Mengurangkan saat benda bertambah (C2 mudah konseptual mc)
    {
        "uid": "q46", "t": "mc", "sec": "a4b3c29d5e01",
        "stem": "Bila kamu punya 4 apel lalu dibelikan 3 lagi, operasinya?",
        "choices": [("penjumlahan (4 + 3 = 7)", True, "Dibelikan lagi membuat apelmu bertambah banyak."), ("pengurangan (4 - 3 = 1)", False, "Apel tidak berkurang jika dibelikan lagi.")],
        "tax": {"bloom": "c2", "difficulty": "mudah", "fungsi": "remedial", "knowledge_dimension": "konseptual", "miskonsepsi_target": "Menggunakan pengurangan pada cerita benda bertambah"}
    },
    # Misconception 3: Menulis kalimat matematika terbalik (C3 sedang prosedural mc)
    {
        "uid": "q47", "t": "mc", "sec": "d7e6f52a8b34",
        "stem": "Ada 10 burung, terbang 4. Kalimat matematikanya adalah ....",
        "choices": [("10 - 4 = 6", True, "Angka mula-mula (10) ditulis di depan."), ("4 - 10 = 6", False, "Posisi terbalik, 4 tidak bisa dikurangi 10.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "remedial", "knowledge_dimension": "prosedural", "miskonsepsi_target": "Menulis posisi angka terbalik pada kalimat matematika cerita"}
    },
    # Misconception 4: Mengabaikan satuan pada soal cerita (C3 sedang prosedural mc)
    {
        "uid": "q48", "t": "mc", "sec": "d7e6f52a8b34",
        "stem": "Pertanyaan 'berapa ekor ikan yang tersisa' dijawab dengan satuan ....",
        "choices": [("ekor ikan", True, "Satuan harus sesuai dengan benda yang ditanyakan di cerita."), ("buah kue", False, "Cerita membahas ikan bukan kue.")],
        "tax": {"bloom": "c3", "difficulty": "sedang", "fungsi": "remedial", "knowledge_dimension": "prosedural", "miskonsepsi_target": "Mengabaikan nama satuan benda dalam menjawab soal cerita"}
    },

    # ── PENGAYAAN (2 soal: C5 sulit & C6 sulit) ──
    # Q49: C5 sulit metakognitif mc
    {
        "uid": "q49", "t": "mc", "sec": "c6d5e41f7a23",
        "stem": "Mengapa satu cerita bisa diselesaikan dengan penjumlahan maupun pengurangan?",
        "choices": [("karena penjumlahan dan pengurangan saling berhubungan erat", True, "Hubungan keluarga fakta: jika 8+5=13 maka 13-5=8."), ("hanya karena membingungkan", False, "Bukan karena membingungkan."), ("karena angkanya bebas", False, "Angka terikat hubungan matematika pasti.")],
        "tax": {"bloom": "c5", "difficulty": "sulit", "fungsi": "pengayaan", "knowledge_dimension": "metakognitif"}
    },
    # Q50: C6 sulit metakognitif mc
    {
        "uid": "q50", "t": "mc", "sec": "d7e6f52a8b34",
        "stem": "Rancang cerita bergambar dua langkah: mula-mula 6, jadi 10, lalu 7!",
        "choices": [("ada 6 apel, dipetik 4 jadi 10, lalu dimakan 3 jadi 7", True, "Dua peristiwa runut: 6 + 4 = 10, lalu 10 - 3 = 7. Sempurna!"), ("ada 6 apel, dimakan 4 jadi 2, lalu beli 5 jadi 7", False, "Tidak mencapai 10 di tengah jalan."), ("ada 6 apel tidak berubah", False, "Tidak ada perubahan.")],
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

with open("outputs/kalibrasi/hasil_bab14.json", "w") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("BERHASIL: outputs/kalibrasi/hasil_bab14.json berhasil dibuat dan divalidasi!")

