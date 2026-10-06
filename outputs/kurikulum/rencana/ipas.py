#!/usr/bin/env python3
"""Rencana kurikulum IPAS SD Kelas 3-6 (Fase B-C). Menghasilkan ipas.json."""
import json, subprocess

def q(sql):
    r = subprocess.run(["docker","exec","-i","titian-bun-postgres","psql","-U","titian","titian_bun","-At","-c",sql],capture_output=True,text=True)
    return [l for l in r.stdout.split("\n") if l]

SUBJ = "(select id from modules where title='IPAS' and parent_id=(select id from modules where title='Semua Mata Pelajaran' and parent_id is null))"
TAHAPS = q("select title from modules where parent_id=%s order by order_index" % SUBJ)
TA = [t for t in TAHAPS if t.startswith("Tahap A")][0]

def bab_of(topic):
    return q("select b.title from module_items b join modules m on m.id=b.module_id join modules g on g.id=m.parent_id join modules t on t.id=g.parent_id where b.node_type='section' and b.status<>'archived' and m.title=$$%s$$ and t.parent_id=%s order by b.order_index" % (topic, SUBJ))

MH, TB, BZ, EN, CB, BA, LK = "Makhluk Hidup & Lingkungannya", "Tubuh Manusia & Kesehatan", "Benda, Zat & Perubahannya", "Energi, Gaya & Gerak", "Cahaya, Bunyi, Listrik & Magnet", "Bumi & Antariksa", "Lingkungan & Kelestarian"
DM, PW, EK, SB = "Diri, Keluarga & Masyarakat", "Peta, Wilayah & Kenampakan Alam", "Ekonomi Sehari-hari", "Sejarah & Budaya"

def S(topik, grup, ku=None, extra=(), mv=(), skip=(), sosial=False, pakai=None):
    """bab lama (dipertahankan urutannya) + bab pindahan + bab baru + 'Kesalahan Umum' di akhir."""
    bab = [{"dari": topik, "judul": t} for t in bab_of(topik) if t not in skip and not t.startswith("Kesalahan Umum")]
    bab += [{"dari": d, "judul": j} for d, j in mv]
    bab += list(extra)
    if ku: bab.append("Kesalahan Umum: " + ku)
    d = {"topik": topik, "grup": grup, "bab": bab}
    if sosial: d["cam"] = False
    if pakai: d["pakai"] = pakai
    return d

def N(topik, grup, bab, ku, sosial=False):
    d = {"topik": topik, "grup": grup, "bab": list(bab) + ["Kesalahan Umum: " + ku]}
    if sosial: d["cam"] = False
    return d

kelas = {
"3": [
 S("Ciri-Ciri Makhluk Hidup", MH, "Api dan Awan yang Bergerak Dianggap Hidup"),
 S("Tumbuhan di Sekitar Kita", MH, "Tumbuhan yang Diam Dianggap Tidak Hidup"),
 S("Bagian Tumbuhan & Fungsinya", MH, "Akar Dianggap Hanya untuk Berpegangan pada Tanah"),
 S("Hewan di Sekitar Kita", MH, "Hewan Dikelompokkan Hanya dari Ukuran Tubuhnya"),
 S("Anggota Tubuhku", TB, "Bagian Tubuh yang Kembar Dianggap Punya Fungsi Sama"),
 S("Panca Indra & Fungsinya", TB, "Lidah Dianggap Satu-Satunya Alat untuk Merasakan Makanan"),
 S("Kebersihan Diri", TB, "Sabun Dianggap Cukup tanpa Air Mengalir dan Waktu yang Cukup"),
 S("Benda & Sifatnya", BZ, "Benda Berat Dianggap Selalu Berukuran Besar"),
 S("Benda di Sekitar & Kegunaannya", BZ, "Kegunaan Benda Dianggap Tidak Bergantung pada Bahannya"),
 S("Cuaca & Musim", BA, "Cuaca dan Musim Dianggap Sama"),
 S("Siang & Malam", BA, "Matahari Dianggap Bergerak Mengelilingi Bumi"),
 S("Diri Sendiri & Keluarga", DM, mv=[("Anggota Keluarga","Keragaman Latar Belakang dalam Keluarga"),("Anggota Keluarga","Tradisi dan Peristiwa Penting Keluarga")], sosial=True),
 S("Peran di Rumah", DM, "Pekerjaan Rumah Dianggap Tugas Satu Anggota Saja", sosial=True),
 S("Lingkungan Rumah & Sekolah", DM, "Lingkungan Buatan Dianggap Tidak Perlu Dirawat", sosial=True),
 S("Kebutuhan & Keinginan", EK, "Semua yang Diinginkan Dianggap sebagai Kebutuhan", sosial=True),
 S("Uang & Jual Beli", EK, "Harga Murah Selalu Dianggap Paling Baik", sosial=True),
 S("Arah Mata Angin", PW, "Timur dan Barat Tertukar saat Membaca Arah", sosial=True),
 S("Membaca Peta Sederhana", PW, "Simbol Peta Ditafsirkan Tanpa Membaca Legenda", sosial=True),
 S("Sejarah Daerah Tempat Tinggal", SB, "Cerita Rakyat Dianggap Sama dengan Fakta Sejarah", sosial=True),
 S("Tokoh & Pahlawan Daerah", SB, "Pahlawan Dianggap Hanya Mereka yang Berperang", sosial=True),
],
"4": [
 S("Bagian Hewan & Fungsinya", MH, "Semua Hewan Dianggap Bernapas dengan Paru-Paru"),
 S("Daur Hidup Hewan", MH, "Semua Hewan Dianggap Mengalami Metamorfosis yang Sama"),
 N("Daur Hidup Tumbuhan", MH, ["Biji dan Syarat Berkecambah","Tahap Pertumbuhan dari Kecambah hingga Dewasa","Bunga, Buah, dan Terbentuknya Biji Baru","Cara Tumbuhan Berkembang Biak: Biji dan Tunas","Mengamati dan Mencatat Pertumbuhan Kecambah"], "Semua Tumbuhan Dianggap Tumbuh dari Biji"),
 S("Merawat Tubuh", TB, "Merasa Sehat Dianggap Berarti Tidak Perlu Merawat Tubuh"),
 S("Sifat Benda di Sekitar", BZ, "Benda yang Sama Dianggap Selalu Sama Sifatnya di Semua Keadaan"),
 S("Padat, Cair & Gas", BZ, "Udara Dianggap Bukan Benda karena Tidak Terlihat"),
 S("Perubahan Wujud", BZ, "Embun Dianggap Muncul dari Bocornya Wadah"),
 S("Bentuk-Bentuk Energi", EN, "Energi Dianggap Sesuatu yang Bisa Dipegang"),
 S("Gaya & Gerak", EN, "Benda Dianggap Berhenti Sendiri Tanpa Ada Gaya Gesek"),
 S("Sumber & Perambatan Bunyi", CB, "Bunyi Dianggap Bisa Merambat di Ruang Hampa"),
 S("Sifat Cahaya", CB, "Mata Dianggap Memancarkan Cahaya untuk Melihat", skip=["Pembiasan dan Penguraian Cahaya"], extra=["Bayangan Terbentuk saat Cahaya Terhalang"]),
 S("Siklus Air", BA, "Air Dianggap Habis setelah Menguap"),
 S("Matahari, Bulan & Bintang", BA, "Bulan Dianggap Memancarkan Cahayanya Sendiri"),
 S("Kenampakan Alam Indonesia", PW, "Gunung dan Bukit Dianggap Sama", sosial=True),
 S("Tetangga & Lingkungan", DM, "Tetangga Dianggap Bukan Bagian dari Kehidupan Sehari-hari", sosial=True),
 S("Aturan di Rumah & Sekolah", DM, "Aturan Dianggap Hanya untuk Membatasi Kebebasan", sosial=True),
 S("Keberagaman Suku & Budaya", DM, "Perbedaan Dianggap Penyebab Perpecahan", sosial=True),
 S("Pekerjaan di Sekitar Kita", EK, "Pekerjaan Dianggap Hanya yang Menghasilkan Uang", sosial=True),
 S("Kerajaan di Indonesia (Pengantar)", SB, "Kerajaan Dianggap Hanya Ada di Pulau Jawa", sosial=True),
],
"5": [
 S("Sistem Pencernaan", TB, "Makanan Dianggap Langsung Menjadi Tenaga tanpa Diolah"),
 S("Sistem Pernapasan", TB, "Paru-Paru Dianggap Mengambil Semua Udara yang Dihirup"),
 S("Sistem Peredaran Darah", TB, "Denyut Nadi Dianggap Tidak Berhubungan dengan Jantung"),
 S("Rangka & Otot", TB, "Otot Dianggap Mendorong Tulang untuk Bergerak"),
 S("Makanan Bergizi & Kesehatan", TB, "Makanan Mahal Dianggap Pasti Bergizi", skip=[]),
 S("Habitat & Tempat Hidup", MH, "Satu Jenis Hewan Dianggap Bisa Hidup di Habitat Apa Saja"),
 N("Rantai Makanan & Jaring-Jaring Makanan", MH, ["Produsen, Konsumen, dan Pengurai","Menyusun Rantai Makanan","Jaring-Jaring Makanan dalam Ekosistem","Aliran Energi dari Matahari ke Konsumen","Akibat Berkurangnya Satu Jenis Makhluk Hidup"], "Arah Panah Dianggap Menunjukkan Siapa Memakan Siapa"),
 S("Merawat Hewan & Tumbuhan", MH, "Merawat Dianggap Cukup dengan Memberi Makan"),
 S("Campuran & Larutan Sederhana", BZ, "Semua yang Tercampur Air Dianggap Larut"),
 S("Sumber Energi & Energi Alternatif", EN, "Energi Terbarukan Dianggap Tidak Pernah Habis dan Tidak Berdampak"),
 S("Pesawat Sederhana", EN, "Pesawat Sederhana Dianggap Mengurangi Usaha, Bukan Gaya"),
 S("Cermin & Bayangan", CB, "Bayangan pada Cermin Datar Dianggap Terbalik Kiri-Kanannya dengan Sendirinya"),
 N("Pembiasan & Penguraian Cahaya", CB, ["Cahaya Dibelokkan saat Berpindah Medium",{"dari":"Sifat Cahaya","judul":"Pembiasan dan Penguraian Cahaya"},"Pelangi dan Penguraian Cahaya Putih","Lensa Cembung pada Lup Sederhana"], "Benda dalam Air Dianggap Tepat di Posisi yang Terlihat"),
 S("Listrik Sederhana & Rangkaian", CB, "Baterai Dianggap Menyimpan Listrik Terus-Menerus", mv=[("Listrik & Magnet Sederhana","Gejala Listrik Statis di Sekitar Kita")]),
 S("Magnet", CB, "Semua Logam Dianggap Ditarik Magnet"),
 S("Cuaca & Musim di Indonesia", BA, "Awan Gelap Dianggap Pasti Menjadi Hujan", mv=[("Cuaca Sederhana","Pengukuran Suhu Udara dan Pengamatan Cuaca")]),
 S("Bencana Alam & Kesiapsiagaan", BA, "Bencana Dianggap Tidak Bisa Dikurangi Dampaknya"),
 S("Sumber Daya Alam", LK, "Sumber Daya Alam Dianggap Tidak Akan Habis"),
 S("Letak Geografis Indonesia", PW, "Letak Astronomis dan Letak Geografis Dianggap Sama", sosial=True),
 N("Provinsi & Ibu Kota", PW, ["Membaca Peta Wilayah Indonesia","Provinsi di Pulau Sumatra, Jawa, dan Kalimantan","Provinsi di Sulawesi, Bali, Nusa Tenggara, Maluku, dan Papua","Ibu Kota Provinsi dan Ciri Khas Daerahnya"], "Ibu Kota Provinsi Dianggap Sama dengan Kota Terbesarnya", sosial=True),
 S("Gotong Royong & Kerja Sama", DM, "Gotong Royong Dianggap Hanya Kerja Bakti Fisik", sosial=True),
 S("Kegiatan Produksi & Konsumsi", EK, "Produksi Dianggap Hanya Kegiatan di Pabrik", sosial=True),
 N("Kerajaan Hindu-Buddha di Nusantara", SB, ["Masuknya Agama Hindu dan Buddha ke Nusantara","Kerajaan Kutai dan Tarumanegara","Kerajaan Sriwijaya","Kerajaan Majapahit","Peninggalan Kerajaan Hindu-Buddha"], "Candi Dianggap Selalu Tempat Ibadah Umat Buddha", sosial=True),
 N("Kerajaan Islam di Nusantara", SB, ["Masuknya Islam ke Nusantara melalui Jalur Perdagangan","Kerajaan Samudra Pasai dan Aceh","Kerajaan Demak dan Mataram Islam","Kerajaan Ternate, Tidore, dan Gowa-Tallo","Peninggalan Kerajaan Islam"], "Kerajaan Islam Dianggap Muncul setelah Semua Kerajaan Hindu-Buddha Runtuh", sosial=True),
],
"6": [
 S("Sistem Tata Surya Sederhana", BA, "Ukuran dan Jarak Planet Dianggap Sama dengan Gambar di Buku"),
 S("Rotasi & Revolusi Bumi", BA, "Musim Dianggap Terjadi karena Bumi Lebih Dekat atau Jauh dari Matahari"),
 S("Perkembangbiakan Makhluk Hidup", MH, "Semua Makhluk Hidup Dianggap Berkembang Biak dengan Cara yang Sama"),
 N("Adaptasi Makhluk Hidup", MH, ["Adaptasi Bentuk Tubuh Hewan","Adaptasi Tingkah Laku Hewan","Adaptasi Tumbuhan terhadap Lingkungan","Hubungan Adaptasi dengan Habitat"], "Adaptasi Dianggap Terjadi Seketika pada Satu Individu"),
 S("Bahan & Kegunaannya", BZ, "Bahan Alami Dianggap Selalu Lebih Baik daripada Bahan Buatan"),
 S("Percobaan Sederhana Zat", BZ, "Percobaan Dianggap Berhasil Hanya Jika Hasilnya Sesuai Dugaan"),
 N("Perubahan Bentuk Energi", EN, ["Energi Tidak Hilang, Hanya Berubah Bentuk","Perubahan Energi pada Alat Listrik","Perubahan Energi pada Makhluk Hidup","Perubahan Energi pada Kendaraan dan Mesin"], "Energi Dianggap Habis setelah Dipakai"),
 N("Gaya Gravitasi dan Gaya Gesek", EN, ["Gaya Gravitasi Menarik Benda ke Bumi","Berat dan Jatuhnya Benda","Gaya Gesek dan Permukaan Benda","Manfaat dan Kerugian Gaya Gesek"], "Benda Berat Dianggap Jatuh Lebih Cepat di Udara karena Gravitasinya Lebih Besar"),
 S("Hemat Energi", EN, "Alat yang Dimatikan Dianggap Tidak Lagi Memakai Listrik"),
 S("Pelestarian Lingkungan", LK, "Menanam Satu Pohon Dianggap Cukup untuk Melestarikan Lingkungan", skip=[]),
 S("Interaksi Manusia & Lingkungan", PW, "Kegiatan Manusia Dianggap Tidak Memengaruhi Kenampakan Alam", sosial=True),
 S("Norma di Masyarakat", DM, "Norma Dianggap Sama dengan Hukum Tertulis", sosial=True),
 S("Menabung & Mengelola Uang Saku", EK, "Menabung Dianggap Hanya Menyisihkan Sisa Uang", sosial=True),
 N("Masa Penjajahan di Indonesia", SB, ["Kedatangan Bangsa Eropa dan Perdagangan Rempah","Penjajahan Portugis, Spanyol, dan Belanda","Perlawanan Rakyat terhadap Penjajah","Pendudukan Jepang di Indonesia"], "Penjajahan Dianggap Berlangsung Sama Lamanya di Semua Daerah", sosial=True),
 N("Perjuangan dan Proklamasi Kemerdekaan", SB, ["Kebangkitan Nasional dan Sumpah Pemuda","Persiapan Kemerdekaan Indonesia","Peristiwa Proklamasi 17 Agustus 1945","Mempertahankan Kemerdekaan","Meneladani Perjuangan Pahlawan Nasional"], "Kemerdekaan Dianggap Diraih hanya dalam Satu Hari", sosial=True),
],
}

HAPUS = ["Wujud Benda: Padat, Cair & Gas","Perubahan Wujud Benda","Ciri Makhluk Hidup Sederhana","Anggota Tubuh & Panca Indra","Anggota Keluarga","Rumah & Sekolahku","Cuaca Sederhana","Makanan Sehat","Cahaya & Sifatnya","Bunyi & Pendengaran","Listrik & Magnet Sederhana","Menjaga Lingkungan","Merawat Diri & Kebersihan","Hidup Rukun di Lingkungan","Benda Hidup & Tak Hidup","Bermain & Bergerak"]
GRUP = [MH, TB, BZ, EN, CB, BA, LK, DM, PW, EK, SB]
plan = {
 "mapel": "IPAS", "tahap": TA, "tahaps": TAHAPS, "jenjang": "SD", "kode": "ipas", "cambridge_label": True,
 "grup": GRUP, "label": {"kurikulum": "merdeka-sd", "jalur": "sd-mi", "rumpun": "sains-teknologi"},
 "hapus_topik": HAPUS, "kelas": kelas,
 "ki": {"jenjang": "SD / MI — Kelas 1-6", "kelas": "Kelas {n} SD/MI", "bundle": "IPAS"},
 "cambridge": {"bundle": "Science (IPAS)"},
 "tka": [{"folder": "TKA SD/MI", "bundle": "IPAS", "kelas": [5, 6]}],
}
json.dump(plan, open("ipas.json", "w"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in kelas.items()}, "topik", sum(len(v) for v in kelas.values()), "bab", sum(len(t["bab"]) for v in kelas.values() for t in v))
