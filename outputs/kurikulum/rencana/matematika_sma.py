#!/usr/bin/env python3
"""Rencana kurikulum Matematika SMA Kelas 10-12 (Fase E-F). Menghasilkan matematika_sma.json."""
import json, subprocess

def q(sql):
    r = subprocess.run(["docker","exec","-i","titian-bun-postgres","psql","-U","titian","titian_bun","-At","-c",sql],capture_output=True,text=True)
    return [l for l in r.stdout.split("\n") if l]

TAHAP = q("select title from modules where title like 'Tahap 3 — Matematika Lanjut%' limit 1")[0]
TID = "(select id from modules where title=$$%s$$)" % TAHAP

def bab_of(topic):
    return q("select b.title from module_items b join modules m on m.id=b.module_id where b.node_type='section' and b.status<>'archived' and m.title=$$%s$$ and m.parent_id in (select id from modules where parent_id=%s) order by b.order_index" % (topic, TID))

def M(dari, judul, baru=None):
    d = {"dari": dari, "judul": judul}
    if baru: d["baru"] = baru
    return d

def keep(topic):
    return [M(topic, t) for t in bab_of(topic)]

def group_of(topic):
    r = q("select g.title from modules s join modules g on g.id=s.parent_id where s.title=$$%s$$ and g.parent_id=%s limit 1" % (topic, TID))
    if not r: raise SystemExit("topik tidak ada di Tahap 3: " + topic)
    return r[0]

def T(topik, bab=None, grup=None):
    return {"topik": topik, "grup": grup or group_of(topik), "bab": bab if bab is not None else keep(topik)}

NEWG = "Persamaan & Pertidaksamaan"

k10 = [
 T("Konsep Relasi & Fungsi"), T("Domain, Kodomain & Range"), T("Fungsi Linear & Grafiknya"),
 T("Persamaan dan Pertidaksamaan Nilai Mutlak", ["Konsep Nilai Mutlak dan Jarak pada Garis Bilangan","Persamaan Nilai Mutlak Linear","Pertidaksamaan Nilai Mutlak Linear","Nilai Mutlak Bentuk Kuadrat dan Grafiknya","Kesalahan Umum: Nilai Mutlak Selalu Dianggap Membuang Tanda Negatif"], NEWG),
 T("Pertidaksamaan Rasional dan Irasional", ["Pertidaksamaan Bentuk Pecahan dan Titik Pembuat Nol","Menentukan Daerah Penyelesaian dengan Garis Bilangan","Pertidaksamaan Bentuk Akar dan Syarat Bilangan di Bawah Akar","Aplikasi Pertidaksamaan Rasional dan Irasional","Kesalahan Umum: Kedua Ruas Dikali dengan Bilangan Bertanda Tak Diketahui"], NEWG),
 T("Akar Persamaan Kuadrat"), T("Diskriminan & Sifat Akar"), T("Menyusun Persamaan Kuadrat"), T("Pertidaksamaan Kuadrat"), T("Fungsi Kuadrat & Grafiknya"), T("Aplikasi Maksimum & Minimum"),
 T("Sistem Persamaan Linear Tiga Variabel"), T("Sistem Persamaan Linear-Kuadrat"), T("Pertidaksamaan Linear Dua Variabel"),
 T("Fungsi Eksponen"), T("Persamaan & Pertidaksamaan Eksponen"), T("Konsep Logaritma"), T("Sifat-Sifat Logaritma"), T("Persamaan & Pertidaksamaan Logaritma"), T("Aplikasi: Pertumbuhan & Peluruhan"),
 T("Ukuran Sudut (Derajat & Radian)"), T("Perbandingan Trigonometri Segitiga Siku-Siku"), T("Sudut Istimewa & Relasi Antar Sudut"), T("Identitas Trigonometri"), T("Aturan Sinus & Cosinus"),
 T("Barisan Aritmetika"), T("Deret Aritmetika"), T("Barisan Geometri"), T("Deret Geometri"),
 T("Pernyataan & Nilai Kebenaran"), T("Negasi, Konjungsi & Disjungsi"), T("Implikasi & Biimplikasi"), T("Konvers, Invers & Kontraposisi"), T("Kuantor Universal & Eksistensial"), T("Penarikan Kesimpulan (Modus Ponens, Tollens, Silogisme)"),
 T("Distribusi Frekuensi & Histogram"), T("Ukuran Pemusatan Data Berkelompok"), T("Ukuran Letak (Kuartil, Desil, Persentil)"), T("Ukuran Penyebaran (Ragam & Simpangan Baku)"),
]
k11 = [
 T("Komposisi Fungsi"), T("Fungsi Invers"), T("Fungsi Rasional & Asimtot"),
 T("Suku Banyak (Polinomial)", ["Konsep dan Nilai Suku Banyak","Pembagian Suku Banyak dengan Cara Bersusun dan Horner","Teorema Sisa","Teorema Faktor dan Akar-Akar Persamaan Suku Banyak","Kesalahan Umum: Teorema Sisa Dipakai untuk Pembagi Berderajat Lebih dari Satu"], NEWG),
 T("Model Matematika Program Linear"), T("Nilai Optimum Fungsi Objektif"),
 T("Deret Geometri Tak Hingga"), T("Notasi Sigma"), T("Induksi Matematika"),
 T("Konsep & Jenis Matriks"), T("Operasi Matriks"), T("Determinan Matriks"), T("Invers Matriks"), T("Penyelesaian SPL dengan Matriks"), T("Transformasi Geometri"),
 T("Luas Segitiga dengan Trigonometri"), T("Grafik Fungsi Trigonometri"), T("Persamaan Trigonometri"), T("Rumus Jumlah & Selisih Sudut"),
 T("Sistem Koordinat Kartesius"), T("Jarak Titik, Garis & Titik Tengah"), T("Gradien & Persamaan Garis"), T("Persamaan Lingkaran"), T("Garis Singgung Lingkaran"),
 T("Konsep Vektor & Notasi"), T("Operasi Vektor"), T("Vektor di Ruang Dimensi Dua (R²)"), T("Vektor di Ruang Dimensi Tiga (R³)"), T("Perkalian Skalar (Dot Product)"), T("Perkalian Silang (Cross Product)"), T("Proyeksi Vektor"),
 T("Kaidah Pencacahan"),
 T("Konsep Limit Fungsi"), T("Limit Fungsi Aljabar"), T("Limit Fungsi Trigonometri"),
 T("Konsep Turunan & Laju Perubahan"), T("Aturan Turunan Dasar"), T("Aturan Rantai"), T("Turunan Fungsi Trigonometri"),
]
k12 = [
 T("Limit di Ketakhinggaan"), T("Kekontinuan Fungsi"),
 T("Turunan Implisit"), T("Nilai Maksimum & Minimum"), T("Kemonotonan & Titik Belok"), T("Aplikasi Turunan: Optimasi"),
 T("Integral Tak Tentu"), T("Integral Tentu & Teorema Dasar Kalkulus"), T("Integral Substitusi"), T("Integral Parsial"), T("Integral Fungsi Trigonometri"), T("Luas Daerah di Bawah Kurva"), T("Volume Benda Putar"),
 T("Permutasi"), T("Kombinasi"), T("Peluang Kejadian Majemuk"), T("Peluang Bersyarat"), T("Distribusi Binomial"),
 T("Kedudukan Titik, Garis & Bidang"), T("Jarak dalam Ruang"), T("Sudut dalam Ruang"), T("Proyeksi pada Bidang"), T("Irisan Bidang pada Bangun Ruang"),
 T("Konsep Bilangan Imajiner"), T("Operasi Bilangan Kompleks"), T("Bentuk Polar & Eksponensial"), T("Teorema De Moivre"), T("Akar Bilangan Kompleks"),
 T("Parabola"), T("Elips"), T("Hiperbola"), T("Persamaan Umum Irisan Kerucut"),
]
kelas = {"10": k10, "11": k11, "12": k12}

# Semua kelompok yang dipakai, lalu topik Tahap 3 lain dibiarkan (bukan tulang punggung SMA).
used = {t["topik"] for v in kelas.values() for t in v}
grup = []
for v in kelas.values():
    for t in v:
        if t["grup"] not in grup: grup.append(t["grup"])
allt = q("select s.title from modules s join modules g on g.id=s.parent_id where g.parent_id=%s and not s.is_folder" % TID)
biarkan = sorted(set(allt) - used)

plan = {
 "mapel": "Matematika", "tahap": TAHAP, "jenjang": "SMA", "kode": "mtk", "cambridge_label": False,
 "grup": grup, "label": {"kurikulum": "merdeka-sma", "jalur": "sma-ma", "rumpun": "matematika-logika"},
 "biarkan": biarkan, "kelas": kelas,
 "ki": {"jenjang": "SMA / MA — Kelas 10-12", "kelas": "Kelas {n} SMA/MA", "bundle": "Matematika"},
 "tka": [{"folder": "Mata Pelajaran Wajib", "bundle": "Matematika", "kelas": [11, 12]}],
}
plan.setdefault("tka", []).append({"via": ["TKA SMA/MA", "Mata Pelajaran Wajib"], "bundle": "Matematika", "kelas": [10, 11, 12]})
json.dump(plan, open("matematika_sma.json", "w"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in kelas.items()}, "topik", sum(len(v) for v in kelas.values()), "bab", sum(len(t["bab"]) for v in kelas.values() for t in v), "| dibiarkan:", len(biarkan))
