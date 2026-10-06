#!/usr/bin/env python3
"""Rencana kurikulum Matematika SD Kelas 1-6 (Fase A-C). Menghasilkan matematika_sd.json."""
import json, subprocess

def q(sql):
    r = subprocess.run(["docker","exec","-i","titian-bun-postgres","psql","-U","titian","titian_bun","-At","-c",sql],capture_output=True,text=True)
    return [l for l in r.stdout.split("\n") if l]

def bab_of(topic):
    return q("select b.title from module_items b join modules m on m.id=b.module_id where b.node_type='section' and b.status<>'archived' and m.title=$$%s$$ and m.parent_id in (select id from modules where parent_id=(select id from modules where title like 'Tahap 1 — Matematika Dasar%%')) order by b.order_index" % topic)

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

G1, G2, G3, G4, G5, G6 = "Bilangan & Operasi Dasar", "Pecahan, Desimal & Persen", "Pola & Aljabar Dasar", "Pengukuran", "Geometri Dasar", "Pengenalan Data"
BCNT="Bilangan Cacah & Nilai Tempat"; PP="Penjumlahan & Pengurangan"; PKP="Perkalian & Pembagian"; UOH="Urutan Operasi Hitung"
BBGB="Bilangan Bulat & Garis Bilangan"; FKFK="Faktor, Kelipatan, FPB & KPK"; KP="Konsep Pecahan"; PSP="Pecahan Senilai & Penyederhanaan"
OHP="Operasi Hitung Pecahan"; BD="Bilangan Desimal"; PPS="Persen & Perbandingan Sederhana"; KPDP="Konversi Pecahan–Desimal–Persen"
SP="Satuan Panjang"; SB="Satuan Berat & Massa"; SW="Satuan Waktu"; SKD="Satuan Kuantitas & Debit"; KS="Konversi Satuan"
MBD="Mengenal Bangun Datar"; KBD="Keliling Bangun Datar"; LBD="Luas Bangun Datar"; MBR="Mengenal Bangun Ruang"; VLP="Volume & Luas Permukaan Bangun Ruang"; SIM="Simetri & Pencerminan"
MMD="Mengumpulkan & Menyajikan Data"; TDB="Tabel & Diagram Batang"; DGL="Diagram Garis & Lingkaran"; RMM="Rata-Rata, Median & Modus Sederhana"

kelas = {
"1": [
 T("Bilangan sampai 20", G1, ["Membilang dan Mencocokkan Benda dengan Bilangan","Melambangkan Bilangan 1 sampai 10","Mengenal Bilangan 11 sampai 20","Membandingkan dan Mengurutkan Bilangan sampai 20","Nol sebagai Tidak Ada Benda","Kesalahan Umum: Menghitung Benda Dua Kali atau Terlewat"]),
 T("Bilangan sampai 100 dan Nilai Tempat", G1, ["Membilang dan Membaca Bilangan sampai 100", M(BCNT,"Mengenal Bilangan Cacah"), "Puluhan dan Satuan", "Menulis Lambang Bilangan sampai 100", M(BCNT,"Membandingkan & Mengurutkan Bilangan Cacah"), "Kesalahan Umum: Puluhan dan Satuan Tertukar"], pakai=BCNT),
 T("Penjumlahan dan Pengurangan sampai 20", G1, [M(PP,"Makna Penjumlahan dan Pengurangan"),"Penjumlahan sampai 10 dengan Benda dan Gambar","Pengurangan sampai 10 dengan Benda dan Gambar","Penjumlahan dan Pengurangan sampai 20","Soal Cerita Bergambar: Menambah dan Mengurangi","Kesalahan Umum: Salah Menghitung Loncatan pada Garis Bilangan"]),
 T("Pola dan Urutan", G3, ["Mengenal Pola Berulang pada Benda dan Gambar","Melanjutkan Pola Bentuk, Warna, dan Ukuran","Pola Bilangan Sederhana","Menyusun Benda Menurut Urutan","Kesalahan Umum: Mengabaikan Bagian yang Berulang"]),
 T("Membandingkan dan Mengukur dengan Satuan Tak Baku", G4, ["Membandingkan Panjang dan Pendek", M(SP,"Satuan Panjang Tak Baku dan Alat Ukurnya"), "Membandingkan Berat dan Ringan","Mengukur Berat dengan Satuan Tak Baku","Urutan Kegiatan Sehari-hari: Pagi, Siang, Malam","Kesalahan Umum: Mengukur Tidak Dimulai dari Ujung Benda"]),
 T("Mengenal Bentuk Bangun Datar dan Bangun Ruang", G5, [M(MBD,"Apa Itu Bangun Datar"),"Mengenal Segitiga, Segiempat, dan Lingkaran","Mengenal Kubus, Balok, Bola, dan Tabung","Menyusun Bentuk dari Bangun Datar","Posisi Benda: Atas, Bawah, Kiri, Kanan, Depan, Belakang","Kesalahan Umum: Mengira Bentuk Bergantung pada Ukuran atau Arah"]),
 T("Data Sederhana dan Piktogram", G6, ["Mengumpulkan dan Menghitung Data Sederhana","Membaca Piktogram","Membuat Piktogram Sederhana","Membandingkan Banyak Data pada Piktogram","Kesalahan Umum: Satu Gambar Mewakili Lebih dari Satu Benda"]),
],
"2": [
 T("Penjumlahan dan Pengurangan sampai 100", G1, ["Strategi Menjumlah dan Mengurang dalam Pikiran"] + keep(PP, exclude={"Makna Penjumlahan dan Pengurangan"}), pakai=PP),
 T("Mengenal Perkalian dan Pembagian", G1, [M(PKP,"Makna Perkalian sebagai Penjumlahan Berulang"),"Perkalian 2, 5, dan 10",M(PKP,"Makna Pembagian sebagai Pembagian Rata"),"Membagi Rata Benda ke dalam Kelompok","Soal Cerita Bergambar: Perkalian dan Pembagian","Kesalahan Umum: Mengira Perkalian Hanya Satu Kali Penjumlahan"]),
 T("Mengenal Setengah dan Seperempat", G2, ["Membagi Benda Menjadi Bagian yang Sama","Mengenal Setengah","Mengenal Seperempat","Membandingkan Utuh, Setengah, dan Seperempat","Kesalahan Umum: Bagian yang Tidak Sama Besar Dianggap Sama"]),
 T("Bilangan Genap, Ganjil, dan Pola Bilangan", G3, ["Mengenal Bilangan Genap dan Ganjil","Membilang Loncat 2, 5, dan 10","Melanjutkan Pola Bilangan Naik dan Turun","Mengurai Bilangan Dua Angka","Kesalahan Umum: Salah Melanjutkan Pola pada Loncatan"]),
 T("Mengukur Panjang dan Berat", G4, ["Mengenal Penggaris dan Sentimeter","Mengukur Panjang Benda dengan Penggaris","Membandingkan Benda Berdasarkan Panjang Terukur","Membaca Timbangan Sederhana: Kilogram","Kesalahan Umum: Angka Nol Penggaris Tidak Dijadikan Awal Ukur"]),
 T("Mengenal Jam, Hari, dan Bulan", G4, ["Membaca Jam Tepat dan Setengah","Urutan Hari dalam Seminggu","Nama Bulan dan Kalender","Waktu Kegiatan Sehari-hari","Kesalahan Umum: Jarum Pendek dan Jarum Panjang Tertukar"]),
 T("Bangun Datar dan Bangun Ruang Sederhana", G5, ["Sisi dan Sudut Bangun Datar","Membedakan Persegi dan Persegi Panjang","Menyusun Bangun Datar Menjadi Bentuk Baru","Mengelompokkan Benda Berbentuk Bangun Ruang","Kesalahan Umum: Mengira Lingkaran Memiliki Sudut"]),
 T("Tabel dan Turus", G6, ["Mengumpulkan Data dengan Turus","Membaca Tabel Data Sederhana","Membuat Tabel dari Turus","Membandingkan Data pada Tabel","Kesalahan Umum: Turus Kelima Tidak Dicoret Silang"]),
],
"3": [
 T("Bilangan sampai 1.000", G1, ["Membaca dan Menulis Bilangan sampai 1.000","Nilai Tempat Ratusan, Puluhan, dan Satuan","Membandingkan dan Mengurutkan Bilangan sampai 1.000","Membulatkan Bilangan ke Puluhan Terdekat","Kesalahan Umum: Angka Nol pada Nilai Tempat Diabaikan"]),
 T("Perkalian & Pembagian", G1, ["Tabel Perkalian 1 sampai 10"] + keep(PKP, exclude={"Makna Perkalian sebagai Penjumlahan Berulang","Makna Pembagian sebagai Pembagian Rata"}), pakai=PKP),
 T("Konsep Pecahan", G2, keep(KP)),
 T("Pola Bilangan dan Kalimat Matematika", G3, ["Pola Bilangan Bertambah dan Berkurang Tetap","Menemukan Aturan Pola","Mengenal Kalimat Matematika","Mencari Bilangan yang Belum Diketahui","Kesalahan Umum: Aturan Pola Diterapkan pada Suku yang Salah"]),
 T("Satuan Panjang", G4, keep(SP, exclude={"Satuan Panjang Tak Baku dan Alat Ukurnya"})),
 T("Satuan Berat & Massa", G4, keep(SB)),
 T("Satuan Waktu", G4, keep(SW)),
 T("Bangun Datar dan Sifat-Sifatnya", G5, keep(MBD, exclude={"Apa Itu Bangun Datar"}), pakai=MBD),
 T("Mengumpulkan & Menyajikan Data", G6, keep(MMD)),
],
"4": [
 T("Bilangan sampai 10.000", G1, ["Nilai Tempat sampai Ribuan", M(BCNT,"Membaca & Menulis Lambang Bilangan"), M(BCNT,"Bentuk Panjang & Bentuk Baku Bilangan"), M(BCNT,"Membulatkan Bilangan Sesuai Ketelitian yang Diminta"), M(BCNT,"Kesalahan Umum: Tertukar Nilai Angka dengan Nilai Tempat")]),
 T("Urutan Operasi Hitung", G1, keep(UOH)),
 T("Pecahan Senilai & Penyederhanaan", G2, keep(PSP)),
 T("Pola Bilangan dan Persamaan Sederhana", G3, ["Pola Bilangan Kelipatan","Pola Gambar Bertingkat","Persamaan Sederhana dengan Satu Operasi","Menyelesaikan Persamaan dengan Operasi Kebalikan","Kesalahan Umum: Salah Memilih Operasi Kebalikan"]),
 T("Konversi Satuan", G4, keep(KS)),
 T("Keliling Bangun Datar", G5, keep(KBD)),
 T("Sudut dan Garis", G5, ["Mengenal Sudut: Lancip, Siku-Siku, dan Tumpul","Mengukur Sudut dengan Busur Derajat","Garis Sejajar, Berpotongan, dan Tegak Lurus","Sudut pada Bangun Datar","Kesalahan Umum: Membaca Skala Busur dari Angka yang Salah"]),
 T("Mengenal Bangun Ruang", G5, keep(MBR)),
 T("Tabel & Diagram Batang", G6, keep(TDB)),
],
"5": [
 T("Bilangan sampai 1.000.000", G1, [M(BCNT,"Nilai Tempat: Satuan sampai Jutaan"),"Membaca dan Menulis Bilangan sampai 1.000.000","Membandingkan dan Mengurutkan Bilangan Besar","Bilangan Besar dalam Kehidupan: Penduduk dan Jarak","Menaksir Hasil Operasi Hitung Bilangan Besar","Kesalahan Umum: Angka Nol pada Bilangan Besar Terlewat"]),
 T("Faktor, Kelipatan, FPB & KPK", G1, keep(FKFK)),
 T("Operasi Hitung Pecahan", G2, keep(OHP)),
 T("Bilangan Desimal", G2, keep(BD)),
 T("Satuan Kuantitas & Debit", G4, keep(SKD)),
 T("Luas Bangun Datar", G5, keep(LBD)),
 T("Koordinat dan Posisi", G5, ["Membaca Posisi pada Peta Berpetak","Mengenal Koordinat pada Bidang (Kuadran I)","Menentukan dan Menggambar Titik pada Koordinat","Menentukan Rute pada Peta Koordinat","Kesalahan Umum: Urutan Sumbu x dan y Tertukar"]),
 T("Diagram Garis & Lingkaran", G6, keep(DGL)),
],
"6": [
 T("Bilangan Bulat & Garis Bilangan", G1, keep(BBGB)),
 T("Persen & Perbandingan Sederhana", G2, keep(PPS)),
 T("Konversi Pecahan–Desimal–Persen", G2, keep(KPDP)),
 T("Rasio dan Skala", G2, ["Mengenal Rasio dan Cara Menuliskannya","Rasio Senilai dan Penyederhanaan Rasio","Membagi Suatu Besaran Menurut Rasio","Skala pada Peta dan Model","Kesalahan Umum: Urutan Perbandingan Tertukar"]),
 T("Pemecahan Masalah Terpadu", G3, ["Memahami Soal Cerita dan Apa yang Ditanyakan","Membuat Model Matematika dari Cerita","Memeriksa Apakah Jawaban Masuk Akal","Soal Campuran Bilangan dan Pengukuran","Kesalahan Umum: Salah Memilih Operasi dari Kata Kunci"]),
 T("Volume & Luas Permukaan Bangun Ruang", G5, keep(VLP)),
 T("Simetri & Pencerminan", G5, keep(SIM)),
 T("Rata-Rata, Median & Modus Sederhana", G6, keep(RMM)),
 T("Kemungkinan Kejadian", G6, ["Kejadian Pasti, Mungkin, dan Mustahil","Membandingkan Kemungkinan Kejadian","Percobaan Sederhana dengan Koin dan Dadu","Menyatakan Kemungkinan dengan Pecahan","Kesalahan Umum: Hasil Sebelumnya Dianggap Mempengaruhi Percobaan Berikutnya"]),
],
}

plan = {
 "mapel": "Matematika", "tahap": next(iter(q("select title from modules where title like 'Tahap 1 — Matematika Dasar%' limit 1"))),
 "jenjang": "SD", "kode": "mtk", "cambridge_label": True,
 "grup": [G1, G2, G3, G4, G5, G6],
 "label": {"kurikulum": "merdeka-sd", "jalur": "sd-mi", "rumpun": "matematika-logika"},
 "arsip": [{"topik": BCNT, "bab": "Pembulatan & Taksiran Sederhana"}],
 "kelas": kelas,
 "ki": {"jenjang": "SD / MI — Kelas 1-6", "kelas": "Kelas {n} SD/MI", "bundle": "Matematika"},
 "cambridge": {"bundle": "Mathematics (Matematika)"},
 "tka": [{"folder": "TKA SD/MI", "bundle": "Matematika", "kelas": [5, 6]}],
}
json.dump(plan, open("matematika_sd.json", "w"), ensure_ascii=False, indent=1)
tp = sum(len(v) for v in kelas.values()); tb = sum(len(t["bab"]) for v in kelas.values() for t in v)
print("kelas", {k: len(v) for k, v in kelas.items()}, "topik", tp, "bab", tb)
