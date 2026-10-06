#!/usr/bin/env python3
"""Rencana kurikulum Matematika SMP Kelas 7-9 (Fase D). Menghasilkan matematika_smp.json."""
import json, subprocess

def q(sql):
    r = subprocess.run(["docker","exec","-i","titian-bun-postgres","psql","-U","titian","titian_bun","-At","-c",sql],capture_output=True,text=True)
    return [l for l in r.stdout.split("\n") if l]

TAHAP = q("select title from modules where title like 'Tahap 2 — Matematika Menengah%' limit 1")[0]

def bab_of(topic):
    return q("select b.title from module_items b join modules m on m.id=b.module_id where b.node_type='section' and b.status<>'archived' and m.title=$$%s$$ and m.parent_id in (select id from modules where parent_id=(select id from modules where title=$$%s$$)) order by b.order_index" % (topic, TAHAP))

def M(dari, judul, baru=None):
    d = {"dari": dari, "judul": judul}
    if baru: d["baru"] = baru
    return d

def keep(topic, exclude=()):
    return [M(topic, t) for t in bab_of(topic) if t not in exclude]

def T(topik, grup, bab, pakai=None):
    d = {"topik": topik, "grup": grup, "bab": bab}
    if pakai: d["pakai"] = pakai
    return d

GB, GA, GL, GP, GG, GR, GS, GBR = "Bilangan Bulat & Rasional", "Aljabar Dasar", "Persamaan & Pertidaksamaan Linear", "Perbandingan & Aritmetika Sosial", "Geometri Bidang", "Geometri Ruang", "Statistika & Peluang Dasar", "Bilangan Berpangkat & Bentuk Akar"
GF = "Relasi, Fungsi & Persamaan Garis"

kelas = {
"7": [
 T("Bilangan Bulat dan Operasinya", GB, ["Mengenal Bilangan Bulat dan Garis Bilangan","Penjumlahan dan Pengurangan Bilangan Bulat","Perkalian dan Pembagian Bilangan Bulat","Operasi Hitung Campuran Bilangan Bulat","Soal Cerita Bilangan Bulat","Kesalahan Umum: Tanda Negatif Hilang saat Mengurangi"]),
 T("Bilangan Rasional: Pecahan dan Desimal", GB, ["Bilangan Rasional dan Bentuk Desimalnya","Membandingkan dan Mengurutkan Bilangan Rasional","Operasi Hitung pada Bilangan Rasional","Pecahan, Desimal, dan Persen dalam Satu Masalah","Kesalahan Umum: Penyebut Dijumlahkan Bersama Pembilang"]),
 T("Variabel, Koefisien & Konstanta", GA, keep("Variabel, Koefisien & Konstanta")),
 T("Operasi Bentuk Aljabar", GA, keep("Operasi Bentuk Aljabar")),
 T("Persamaan Linear Satu Variabel", GL, keep("Persamaan Linear Satu Variabel")),
 T("Pertidaksamaan Linear Satu Variabel", GL, keep("Pertidaksamaan Linear Satu Variabel")),
 T("Perbandingan Senilai", GP, keep("Perbandingan Senilai")),
 T("Perbandingan Berbalik Nilai", GP, keep("Perbandingan Berbalik Nilai")),
 T("Skala & Peta", GP, keep("Skala & Peta")),
 T("Untung, Rugi & Diskon", GP, keep("Untung, Rugi & Diskon")),
 T("Bunga Tunggal, Bruto, Neto & Tara", GP, keep("Bunga Tunggal, Bruto, Neto & Tara")),
 T("Garis & Sudut", GG, keep("Garis & Sudut")),
 T("Segitiga & Jenis-Jenisnya", GG, keep("Segitiga & Jenis-Jenisnya")),
 T("Segiempat & Sifatnya", GG, keep("Segiempat & Sifatnya")),
 T("Penyajian Data", GS, keep("Penyajian Data")),
 T("Ukuran Pemusatan Data", GS, keep("Ukuran Pemusatan Data")),
],
"8": [
 T("Pola Bilangan", GA, keep("Pola Bilangan")),
 T("Pemfaktoran Bentuk Aljabar", GA, keep("Pemfaktoran Bentuk Aljabar")),
 T("Pecahan Aljabar", GA, keep("Pecahan Aljabar")),
 T("Relasi dan Fungsi", GF, ["Mengenal Relasi dan Cara Menyajikannya","Fungsi dan Ciri-Cirinya","Rumus Fungsi dan Nilai Fungsi","Grafik Fungsi Linear","Korespondensi Satu-Satu","Kesalahan Umum: Relasi yang Bukan Fungsi Dianggap Fungsi"]),
 T("Persamaan Garis Lurus", GF, ["Gradien atau Kemiringan Garis","Persamaan Garis Melalui Satu Titik dan Gradien","Persamaan Garis Melalui Dua Titik","Garis Sejajar dan Garis Tegak Lurus","Soal Cerita dengan Model Garis Lurus","Kesalahan Umum: Tanda Gradien Salah"]),
 T("Persamaan Linear Dua Variabel", GL, keep("Persamaan Linear Dua Variabel")),
 T("Sistem Persamaan Linear Dua Variabel", GL, keep("Sistem Persamaan Linear Dua Variabel")),
 T("Aplikasi Sistem Persamaan", GL, keep("Aplikasi Sistem Persamaan")),
 T("Soal Cerita & Pemodelan Matematis", "Numerasi & Penalaran Kuantitatif", keep("Soal Cerita & Pemodelan Matematis")),
 T("Teorema Pythagoras", GG, keep("Teorema Pythagoras")),
 T("Lingkaran: Keliling & Luas", GG, keep("Lingkaran: Keliling & Luas")),
 T("Sudut Pusat, Busur & Juring", GG, keep("Sudut Pusat, Busur & Juring")),
 T("Kubus & Balok", GR, keep("Kubus & Balok")),
 T("Prisma & Limas", GR, keep("Prisma & Limas")),
 T("Ukuran Penyebaran Data Sederhana", GS, keep("Ukuran Penyebaran Data Sederhana")),
 T("Konsep Peluang", GS, keep("Konsep Peluang")),
 T("Peluang Kejadian Sederhana", GS, keep("Peluang Kejadian Sederhana")),
],
"9": [
 T("Bilangan Berpangkat Bulat", GBR, keep("Bilangan Berpangkat Bulat")),
 T("Sifat-Sifat Perpangkatan", GBR, keep("Sifat-Sifat Perpangkatan")),
 T("Bentuk Akar", GBR, keep("Bentuk Akar")),
 T("Merasionalkan Penyebut", GBR, keep("Merasionalkan Penyebut")),
 T("Notasi Ilmiah", GBR, keep("Notasi Ilmiah")),
 T("Kesebangunan & Kekongruenan", GG, keep("Kesebangunan & Kekongruenan")),
 T("Transformasi Geometri", GG, ["Pencerminan (Refleksi) pada Bidang Koordinat","Pergeseran (Translasi)","Perputaran (Rotasi) dan Titik Pusatnya","Perbesaran dan Perkecilan (Dilatasi)","Komposisi Transformasi Sederhana","Kesalahan Umum: Arah Putar dan Titik Pusat Tertukar"]),
 T("Tabung, Kerucut & Bola", GR, keep("Tabung, Kerucut & Bola")),
 T("Luas Permukaan Bangun Ruang", GR, keep("Luas Permukaan Bangun Ruang")),
 T("Volume Bangun Ruang Gabungan", GR, keep("Volume Bangun Ruang Gabungan")),
 T("Peluang Kejadian Majemuk", GS, ["Kejadian Saling Lepas dan Tidak Saling Lepas","Peluang Gabungan Dua Kejadian","Kejadian Saling Bebas","Peluang pada Percobaan Berulang","Kesalahan Umum: Peluang Dijumlahkan Padahal Kejadian Tidak Saling Lepas"]),
 T("Estimasi & Perkiraan", "Numerasi & Penalaran Kuantitatif", keep("Estimasi & Perkiraan")),
],
}

plan = {
 "mapel": "Matematika", "tahap": TAHAP, "jenjang": "SMP", "kode": "mtk", "cambridge_label": True,
 "grup": [GB, GA, GF, GL, GP, GG, GR, GS, GBR, "Numerasi & Penalaran Kuantitatif"],
 "label": {"kurikulum": "merdeka-smp", "jalur": "smp-mts", "rumpun": "matematika-logika"},
 "biarkan": ["Perbandingan Kuantitatif", "Deret Angka & Deret Huruf", "Literasi Numerasi Kontekstual (AKM)", "Aritmetika Cepat & Berhitung Efisien"],
 "kelas": kelas,
 "ki": {"jenjang": "SMP / MTs — Kelas 7-9", "kelas": "Kelas {n} SMP/MTs", "bundle": "Matematika"},
 "cambridge": {"bundle": "Mathematics (Matematika)"},
 "tka": [{"folder": "TKA SMP/MTs", "bundle": "Matematika", "kelas": [8, 9]}],
}
json.dump(plan, open("matematika_smp.json", "w"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in kelas.items()}, "topik", sum(len(v) for v in kelas.values()), "bab", sum(len(t["bab"]) for v in kelas.values() for t in v))
