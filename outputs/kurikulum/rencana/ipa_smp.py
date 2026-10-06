#!/usr/bin/env python3
"""Rencana kurikulum IPA SMP Kelas 7-9 (Fase D). Menghasilkan ipa_smp.json."""
import json, subprocess

def q(sql):
    r = subprocess.run(["docker","exec","-i","titian-bun-postgres","psql","-U","titian","titian_bun","-At","-c",sql],capture_output=True,text=True)
    return [l for l in r.stdout.split("\n") if l]

SUBJ = "(select id from modules where title='IPA' and parent_id=(select id from modules where title='Semua Mata Pelajaran' and parent_id is null))"
TAHAPS = q("select title from modules where parent_id=%s order by order_index" % SUBJ)
TB_ = [t for t in TAHAPS if t.startswith("Tahap B")][0]

def bab_of(topic):
    return q("select b.title from module_items b join modules m on m.id=b.module_id join modules g on g.id=m.parent_id join modules t on t.id=g.parent_id where b.node_type='section' and b.status<>'archived' and m.title=$$%s$$ and t.parent_id=%s order by b.order_index" % (topic, SUBJ))


HK, MT, KL, KM, OK, EO, TU, SO = "Hakikat IPA & Pengukuran", "Materi & Perubahannya", "Suhu, Kalor & Pemuaian", "Keanekaragaman & Klasifikasi Makhluk Hidup", "Organisasi Kehidupan", "Ekosistem & Lingkungan", "Struktur & Fungsi Tumbuhan", "Sistem Organ Manusia & Kesehatan"
GG, EU, GB, CO, LM, PA, ZA, PB, BU, TL = "Gerak & Gaya", "Energi, Usaha & Pesawat Sederhana", "Getaran, Gelombang & Bunyi", "Cahaya & Optik", "Listrik & Magnet", "Partikel, Reaksi & Asam-Basa", "Zat Aditif & Adiktif", "Pewarisan Sifat & Bioteknologi", "Bumi & Antariksa", "Teknologi & Lingkungan"

def S(topik, grup, ku=None, extra=(), mv=(), skip=()):
    bab = [{"dari": topik, "judul": t} for t in bab_of(topik) if t not in skip and not t.startswith("Kesalahan Umum")]
    bab += [{"dari": d, "judul": j} for d, j in mv]
    bab += list(extra)
    if ku: bab.append("Kesalahan Umum: " + ku)
    return {"topik": topik, "grup": grup, "bab": bab}

def N(topik, grup, bab, ku):
    return {"topik": topik, "grup": grup, "bab": list(bab) + ["Kesalahan Umum: " + ku]}

kelas = {
"7": [
 S("Metode Ilmiah", HK, "Hipotesis Dianggap Harus Selalu Terbukti Benar"),
 S("Keselamatan Kerja Laboratorium", HK, "Simbol Bahaya Dianggap Tidak Perlu Dibaca pada Percobaan Sederhana"),
 S("Besaran Pokok & Turunan", HK, "Satuan Dianggap Sama dengan Besaran"),
 S("Satuan & Sistem Internasional", HK, "Awalan Satuan Kilo, Sentimeter, dan Mili Tertukar"),
 S("Konversi Satuan", HK, "Mengalikan Padahal Seharusnya Membagi saat Mengonversi Satuan"),
 S("Notasi Ilmiah", HK, "Pangkat Negatif Dianggap Menghasilkan Bilangan Negatif"),
 S("Alat Ukur Panjang", HK, "Skala Dibaca dari Sudut Pandang Miring"),
 S("Alat Ukur Massa & Waktu", HK, "Massa dan Berat Dianggap Sama"),
 S("Ketelitian & Angka Penting", HK, "Nol di Belakang Koma Dianggap Tidak Bermakna"),
 S("Penyajian Data Percobaan", HK, "Titik pada Grafik Dihubungkan Zigzag tanpa Melihat Pola"),
 S("Klasifikasi Materi", MT, "Udara Dianggap Bukan Materi"),
 S("Sifat Fisika & Kimia", MT, "Warna dan Bau Dianggap Selalu Sifat Kimia"),
 S("Perubahan Fisika & Kimia", MT, "Perubahan Wujud Dianggap Perubahan Kimia"),
 S("Unsur, Senyawa & Campuran", MT, "Air Dianggap Campuran Hidrogen dan Oksigen"),
 S("Pemisahan Campuran", MT, "Semua Campuran Dianggap Bisa Dipisahkan dengan Penyaringan"),
 S("Massa Jenis", MT, "Benda Besar Dianggap Pasti Bermassa Jenis Besar"),
 S("Sifat Zat Padat, Cair & Gas", MT, "Gas Dianggap Tidak Bermassa"),
 S("Perubahan Wujud Zat", MT, "Suhu Dianggap Terus Naik selama Zat Mendidih"),
 S("Adhesi & Kohesi", MT, "Adhesi dan Kohesi Tertukar"),
 S("Kapilaritas", MT, "Air Dianggap Naik pada Pipa Kecil karena Disedot", extra=["Kapilaritas pada Tumbuhan dan Kain"]),
 S("Suhu & Termometer", KL, "Suhu dan Kalor Dianggap Sama"),
 S("Kalor & Perubahan Suhu", KL, "Benda Bersuhu Tinggi Dianggap Pasti Menyimpan Kalor Lebih Banyak"),
 S("Kalor & Perubahan Wujud", KL, "Suhu Dianggap Naik selama Zat Melebur"),
 S("Pemuaian Zat", KL, "Lubang pada Logam Dianggap Menyempit saat Dipanaskan"),
 S("Konduksi, Konveksi & Radiasi", KL, "Konveksi Dianggap Bisa Terjadi pada Zat Padat"),
 S("Penerapan Kalor dalam Kehidupan", KL, "Selimut Dianggap Menghasilkan Panas untuk Tubuh"),
 S("Ciri-Ciri Makhluk Hidup", KM, "Benda yang Bergerak Dianggap Hidup"),
 S("Klasifikasi & Taksonomi Dasar", KM, "Paus dan Lumba-Lumba Dianggap Ikan"),
 S("Kunci Determinasi", KM, "Ciri yang Tidak Diamati Dijadikan Dasar Pemisahan"),
 S("Kingdom Monera & Protista", KM, "Semua Bakteri Dianggap Penyebab Penyakit"),
 S("Kingdom Fungi", KM, "Jamur Dianggap Tumbuhan"),
 S("Kingdom Plantae", KM, "Lumut dan Paku Dianggap Tumbuhan Berbiji"),
 S("Kingdom Animalia", KM, "Semua Hewan Bertulang Belakang Dianggap Mamalia"),
 S("Mikroskop & Penggunaannya", OK, "Perbesaran Lensa Objektif dan Okuler Dijumlahkan"),
 S("Sel sebagai Unit Kehidupan", OK, "Sel Hewan dan Sel Tumbuhan Dianggap Sama Strukturnya"),
 S("Jaringan", OK, "Jaringan Dianggap Sama dengan Organ"),
 S("Organ & Sistem Organ", OK, "Organ Dianggap Bekerja Sendiri-Sendiri"),
 S("Organisme", OK, "Populasi dan Komunitas Tertukar"),
 S("Komponen Ekosistem", EO, "Komponen Abiotik Dianggap Tidak Berpengaruh pada Makhluk Hidup"),
 S("Rantai & Jaring Makanan", EO, "Pengurai Dianggap Tidak Termasuk dalam Rantai Makanan"),
 N("Interaksi dalam Ekosistem", EO, ["Simbiosis Mutualisme, Komensalisme, dan Parasitisme","Predasi dan Kompetisi","Interaksi Antara Komponen Biotik dan Abiotik","Menganalisis Pola Interaksi dalam Suatu Ekosistem"], "Parasitisme dan Predasi Dianggap Sama"),
 N("Daur Materi di Alam", EO, ["Daur Air","Daur Karbon dan Oksigen","Daur Nitrogen","Peran Pengurai dalam Daur Materi"], "Daur Materi Dianggap Menambah Jumlah Materi Baru di Bumi"),
 S("Pencemaran Lingkungan", EO, "Limbah Organik Dianggap Tidak Mencemari"),
 S("Pemanasan Global", EO, "Efek Rumah Kaca Dianggap Selalu Merugikan"),
],
"8": [
 S("Jarak & Perpindahan", GG, "Jarak Dianggap Selalu Sama dengan Perpindahan"),
 S("Kelajuan & Kecepatan", GG, "Kelajuan dan Kecepatan Dianggap Sama"),
 S("Percepatan", GG, "Perlambatan Dianggap Bukan Percepatan"),
 S("Gerak Lurus Beraturan (GLB)", GG, "Benda Bergerak Dianggap Selalu Membutuhkan Gaya"),
 S("Gerak Lurus Berubah Beraturan (GLBB)", GG, "Kecepatan Nol Dianggap Berarti Percepatan Nol"),
 S("Grafik Gerak", GG, "Grafik Dianggap Lintasan Sebenarnya Benda"),
 S("Jenis-Jenis Gaya", GG, "Gaya Dianggap Hanya Ada saat Benda Bersentuhan"),
 S("Resultan Gaya", GG, "Gaya Dijumlahkan tanpa Memperhatikan Arah"),
 S("Hukum Newton Sederhana", GG, "Gaya Aksi dan Reaksi Dianggap Bekerja pada Benda yang Sama"),
 S("Tekanan pada Zat Padat", GG, "Gaya Besar Dianggap Pasti Menghasilkan Tekanan Besar"),
 S("Tekanan Hidrostatis", GG, "Tekanan Zat Cair Dianggap Bergantung pada Bentuk Bejana"),
 N("Tekanan Zat Gas dan Udara", GG, ["Udara Memiliki Massa dan Menekan ke Segala Arah","Tekanan Udara dan Ketinggian","Alat Ukur Tekanan Udara: Barometer dan Manometer","Penerapan Tekanan Udara dalam Kehidupan"], "Udara Dianggap Tidak Menimbulkan Tekanan"),
 S("Hukum Pascal", GG, "Zat Cair Dianggap Bisa Dimampatkan"),
 S("Hukum Archimedes", GG, "Benda Berat Dianggap Pasti Tenggelam"),
 S("Bentuk-Bentuk Energi", EU, "Energi Dianggap Sesuatu yang Bisa Dilihat"),
 S("Energi Kinetik & Potensial", EU, "Energi Potensial Dianggap Hanya Bergantung pada Massa"),
 S("Usaha", EU, "Menahan Beban Diam Dianggap Melakukan Usaha"),
 N("Hukum Kekekalan Energi", EU, ["Energi Tidak Dapat Dimusnahkan","Energi Mekanik pada Ayunan dan Lintasan Curam","Energi yang Terbuang sebagai Kalor","Analisis Perubahan Energi pada Kendaraan dan Alat Rumah Tangga"], "Energi Dianggap Hilang saat Ada Gesekan"),
 S("Pesawat Sederhana: Tuas", EU, "Tuas Dianggap Menghemat Usaha"),
 S("Katrol & Bidang Miring", EU, "Bidang Miring Dianggap Mengurangi Kerja yang Dilakukan"),
 S("Efisiensi Pesawat Sederhana", EU, "Efisiensi Dianggap Bisa Melebihi 100%"),
 S("Getaran & Periode", GB, "Periode dan Frekuensi Dianggap Sama"),
 S("Sifat Gelombang", GB, "Gelombang Dianggap Memindahkan Materi"),
 S("Gelombang Transversal & Longitudinal", GB, "Bukit Gelombang Transversal Dianggap Sama dengan Rapatan Gelombang Longitudinal"),
 S("Frekuensi & Nada", GB, "Nada Tinggi Dianggap Sama dengan Bunyi Keras"),
 S("Bunyi & Syarat Terdengar", GB, "Bunyi Dianggap Merambat di Ruang Hampa"),
 S("Pemantulan Bunyi & Gema", GB, "Gema Dianggap Selalu Terdengar di Semua Ruangan"),
 S("Sifat-Sifat Cahaya", CO, "Cahaya Dianggap Membutuhkan Medium untuk Merambat"),
 S("Pemantulan Cahaya", CO, "Sudut Datang dan Sudut Pantul Diukur dari Permukaan Cermin"),
 S("Pembiasan Cahaya", CO, "Cahaya Dianggap Selalu Membelok Menjauhi Garis Normal"),
 S("Cermin Datar & Lengkung", CO, "Bayangan Maya Dianggap Tidak Bisa Dilihat"),
 S("Lensa Cembung & Cekung", CO, "Lensa Cembung Dianggap Selalu Menghasilkan Bayangan Diperbesar"),
 S("Alat Optik: Mata & Kacamata", CO, "Rabun Dekat dan Rabun Jauh Tertukar"),
 S("Lup, Mikroskop & Teleskop", CO, "Perbesaran Alat Optik Dianggap Selalu Bertambah Jika Lensa Ditambah"),
 S("Atom, Ion & Molekul", PA, "Ion dan Atom Dianggap Sama Muatannya"),
 S("Lambang Unsur", PA, "Lambang Unsur Dianggap Singkatan Nama Indonesia"),
 S("Model Atom Sederhana", PA, "Elektron Dianggap Mengorbit seperti Planet"),
 S("Rumus Kimia Sederhana", PA, "Angka Indeks dan Koefisien Tertukar"),
 S("Sifat Bahan & Pemanfaatannya", PA, "Bahan Sintetis Dianggap Selalu Berbahaya"),
 S("Akar, Batang & Daun", TU, "Semua Akar Dianggap Tumbuh di Dalam Tanah"),
 S("Jaringan Tumbuhan", TU, "Semua Sel Tumbuhan Dianggap Mampu Melakukan Fotosintesis"),
 S("Fotosintesis & Faktornya", TU, "Tumbuhan Dianggap Tidak Bernapas pada Siang Hari"),
 S("Transportasi pada Tumbuhan", TU, "Air Dianggap Naik karena Dipompa oleh Akar Saja"),
 S("Gerak pada Tumbuhan", TU, "Tumbuhan yang Diam Dianggap Tidak Bergerak"),
 N("Sistem Gerak Manusia", SO, ["Rangka: Fungsi dan Jenis Tulang","Sendi dan Jenis Gerakannya","Otot Rangka dan Cara Kerjanya","Gangguan Sistem Gerak dan Cara Mencegahnya"], "Otot Dianggap Mendorong Tulang untuk Bergerak"),
 N("Sistem Pencernaan Manusia", SO, ["Organ Pencernaan dan Alurnya","Pencernaan Mekanik dan Kimiawi","Penyerapan Sari Makanan","Gangguan Pencernaan dan Pola Makan Sehat"], "Semua Pencernaan Terjadi di Lambung"),
 N("Sistem Pernapasan Manusia", SO, ["Organ Pernapasan dan Alur Udara","Pertukaran Gas di Alveolus","Mekanisme Bernapas: Dada dan Perut","Gangguan Pernapasan dan Bahaya Asap Rokok"], "Paru-Paru Dianggap Mengambil Semua Oksigen dari Udara yang Dihirup"),
 N("Sistem Peredaran Darah Manusia", SO, ["Komponen Darah dan Fungsinya","Jantung dan Pembuluh Darah","Peredaran Darah Besar dan Kecil","Golongan Darah dan Gangguan Peredaran Darah"], "Darah dalam Pembuluh Balik Dianggap Selalu Berwarna Biru"),
 N("Sistem Ekskresi Manusia", SO, ["Zat Sisa dan Organ Ekskresi","Ginjal dan Pembentukan Urine","Kulit, Paru-Paru, dan Hati sebagai Organ Ekskresi","Gangguan Ekskresi dan Menjaga Kesehatan Ginjal"], "Ekskresi Dianggap Sama dengan Defekasi"),
 S("Penyakit Menular & Tidak Menular", SO, "Semua Penyakit Dianggap Menular"),
 S("Sistem Kekebalan Tubuh", SO, "Vaksin Dianggap Membuat Orang Sakit"),
],
"9": [
 S("Listrik Statis", LM, "Benda Bermuatan Dianggap Selalu Mengalirkan Listrik"),
 S("Arus & Beda Potensial", LM, "Arus Listrik Dianggap Berkurang Setelah Melewati Lampu"),
 S("Hukum Ohm", LM, "Hambatan Dianggap Bergantung pada Arus yang Melaluinya"),
 S("Rangkaian Seri & Paralel", LM, "Lampu pada Rangkaian Paralel Dianggap Redup Jika Ditambah"),
 S("Energi & Daya Listrik", LM, "Daya dan Energi Listrik Dianggap Sama"),
 S("Kemagnetan", LM, "Kutub Magnet yang Dipotong Dianggap Menjadi Kutub Tunggal"),
 S("Induksi Elektromagnetik Sederhana", LM, "GGL Induksi Dianggap Muncul Meski Fluks Tidak Berubah"),
 N("Transformator & Transmisi Listrik", LM, ["Prinsip Kerja Transformator","Transformator Penaik dan Penurun Tegangan","Efisiensi Transformator","Transmisi Listrik dari Pembangkit ke Rumah"], "Transformator Dianggap Menambah Energi Listrik"),
 S("Struktur Bumi & Bencana Alam", BU, "Gempa dan Gunung Api Dianggap Tidak Berhubungan dengan Lempeng Tektonik"),
 S("Rotasi, Revolusi & Gerhana", BU, "Fase Bulan Dianggap Disebabkan Bayangan Bumi"),
 S("Tata Surya", BU, "Jarak Antarplanet pada Gambar Dianggap Sesuai Skala Sebenarnya"),
 N("Atmosfer & Cuaca", BU, ["Lapisan-Lapisan Atmosfer","Unsur Cuaca dan Pembentukan Awan","Angin, Tekanan Udara, dan Hujan","Iklim dan Perubahan Iklim"], "Cuaca dan Iklim Dianggap Sama"),
 S("Pewarisan Sifat", PB, "Sifat yang Didapat Selama Hidup Dianggap Dapat Diwariskan"),
 S("Materi Genetik Sederhana", PB, "Gen dan Kromosom Dianggap Sama"),
 S("Hukum Mendel Dasar", PB, "Sifat Dominan Dianggap Sifat yang Paling Banyak di Populasi"),
 S("Persilangan Monohibrid", PB, "Perbandingan 3:1 Dianggap Pasti Terjadi pada Setiap Jumlah Keturunan"),
 S("Penerapan Pewarisan Sifat", PB, "Golongan Darah Dianggap Diwariskan Hanya dari Satu Orang Tua"),
 S("Bioteknologi Konvensional", PB, "Fermentasi Dianggap Sama dengan Pembusukan"),
 S("Bioteknologi Modern Sederhana", PB, "Semua Produk Rekayasa Genetika Dianggap Berbahaya"),
 N("Sistem Reproduksi Manusia", SO, ["Organ Reproduksi Laki-Laki dan Perempuan","Pubertas dan Perubahan pada Remaja","Pembuahan, Kehamilan, dan Perkembangan Janin","Kesehatan Reproduksi dan Pencegahan Penyakit"], "Perubahan Pubertas Dianggap Sama Waktunya bagi Setiap Remaja"),
 N("Sistem Koordinasi: Saraf & Hormon", SO, ["Sistem Saraf: Neuron dan Otak","Gerak Refleks dan Gerak Sadar","Hormon dan Kelenjar Endokrin","Gangguan Sistem Koordinasi dan Cara Menjaganya"], "Gerak Refleks Dianggap Diatur oleh Otak"),
 S("Ciri Asam & Basa", PA, "Semua Zat yang Rasanya Asam Dianggap Aman Dikonsumsi"),
 S("Indikator Alami & Buatan", PA, "Perubahan Warna Indikator Dianggap Selalu Sama pada Semua Jenis Indikator"),
 S("Skala pH Sederhana", PA, "pH Nol Dianggap Berarti Zat Netral"),
 S("Reaksi Netralisasi", PA, "Hasil Netralisasi Dianggap Selalu Berupa Air Saja"),
 S("Garam dalam Kehidupan", PA, "Semua Garam Dianggap Sama dengan Garam Dapur"),
 N("Reaksi Kimia Sederhana", PA, ["Ciri-Ciri Terjadinya Reaksi Kimia","Pereaksi, Hasil Reaksi, dan Persamaan Kata","Hukum Kekekalan Massa","Faktor yang Memengaruhi Laju Reaksi","Reaksi Kimia dalam Kehidupan Sehari-hari"], "Massa Dianggap Berkurang saat Kertas Terbakar"),
 S("Zat Aditif Makanan", ZA, "Semua Zat Aditif Dianggap Berbahaya"),
 S("Zat Adiktif & Bahayanya", ZA, "Rokok Elektrik Dianggap Aman karena Tidak Berasap Tebal"),
 S("Pola Hidup Sehat", SO, "Berat Badan Ideal Dianggap Satu-Satunya Tanda Sehat"),
 S("Teknologi Kesehatan Sederhana", TL, "Alat Kesehatan Digital Dianggap Menggantikan Pemeriksaan Dokter"),
 S("Teknologi Ramah Lingkungan", TL, "Produk Berlabel Ramah Lingkungan Dianggap Tidak Berdampak"),
],
}

HAPUS = ["Besaran & Satuan","Alat Ukur & Ketelitian","Zat Aditif & Adiktif","Struktur & Fungsi Jaringan Tumbuhan","Fotosintesis","Bioteknologi Sederhana","Teknologi Terinspirasi Tumbuhan"]
GRUP = [HK, MT, KL, KM, OK, EO, GG, EU, GB, CO, TU, SO, PA, ZA, PB, BU, LM, TL]
plan = {
 "mapel": "IPA", "tahap": TB_, "tahaps": TAHAPS, "jenjang": "SMP", "kode": "ipa", "cambridge_label": True,
 "grup": GRUP, "label": {"kurikulum": "merdeka-smp", "jalur": "smp-mts", "rumpun": "sains-teknologi"},
 "hapus_topik": HAPUS, "kelas": kelas,
 "ki": {"jenjang": "SMP / MTs — Kelas 7-9", "kelas": "Kelas {n} SMP/MTs", "bundle": "IPA"},
 "cambridge": {"bundle": "Science (IPA)"},
 "tka": [{"folder": "TKA SMP/MTs", "bundle": "IPA", "kelas": [8, 9]}],
}
json.dump(plan, open("ipa_smp.json", "w"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in kelas.items()}, "topik", sum(len(v) for v in kelas.values()), "bab", sum(len(t["bab"]) for v in kelas.values() for t in v))
