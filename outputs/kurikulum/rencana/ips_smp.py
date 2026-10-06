#!/usr/bin/env python3
"""Rencana kurikulum IPS SMP Kelas 7-9 (Fase D). Menghasilkan ips_smp.json."""
import json, subprocess

def q(sql):
    r = subprocess.run(["docker","exec","-i","titian-bun-postgres","psql","-U","titian","titian_bun","-At","-c",sql],capture_output=True,text=True)
    return [l for l in r.stdout.split("\n") if l]

SUBJ = "(select id from modules where title='IPS' and parent_id=(select id from modules where title='Semua Mata Pelajaran' and parent_id is null))"
TAHAPS = q("select title from modules where parent_id=%s order by order_index" % SUBJ)
TB_ = [t for t in TAHAPS if t.startswith("Tahap B")][0]

def bab_of(topic):
    return q("select b.title from module_items b join modules m on m.id=b.module_id join modules g on g.id=m.parent_id join modules t on t.id=g.parent_id where b.node_type='section' and b.status<>'archived' and m.title=$$%s$$ and t.parent_id=%s order by b.order_index" % (topic, SUBJ))


RG, IS, EKO, SJ, GL_ = "Ruang, Lingkungan & Kependudukan", "Interaksi & Lembaga Sosial", "Kegiatan Ekonomi & Kewirausahaan", "Sejarah Indonesia", "Globalisasi & Kerja Sama Internasional"

def S(topik, grup, ku, extra=()):
    bab = [{"dari": topik, "judul": t} for t in bab_of(topik) if not t.startswith("Kesalahan Umum")]
    bab += list(extra)
    bab.append("Kesalahan Umum: " + ku)
    return {"topik": topik, "grup": grup, "bab": bab}

def N(topik, grup, bab, ku):
    return {"topik": topik, "grup": grup, "bab": list(bab) + ["Kesalahan Umum: " + ku]}

kelas = {
"7": [
 N("Berpikir Sejarah: Waktu, Sumber & Bukti", SJ, ["Konsep Waktu: Kronologi, Periodisasi, dan Kesinambungan","Sumber Sejarah: Primer dan Sekunder","Menyusun Garis Waktu Peristiwa","Sebab dan Akibat dalam Peristiwa Sejarah"], "Sejarah Dianggap Hanya Hafalan Tahun dan Nama"),
 N("Masa Praaksara di Indonesia", SJ, ["Manusia Purba dan Situs Penemuannya","Kehidupan Masa Berburu dan Mengumpulkan Makanan","Masa Bercocok Tanam dan Perundagian","Kepercayaan dan Hasil Budaya Masa Praaksara"], "Masa Praaksara Dianggap Tanpa Budaya karena Belum Ada Tulisan"),
 N("Kerajaan Hindu-Buddha di Indonesia", SJ, ["Masuk dan Berkembangnya Hindu-Buddha di Nusantara","Kerajaan Kutai, Tarumanegara, dan Kalingga","Kerajaan Sriwijaya dan Mataram Kuno","Kerajaan Majapahit dan Kerajaan-Kerajaan Lain","Peninggalan Budaya Hindu-Buddha"], "Pengaruh India Dianggap Menggantikan Budaya Asli Nusantara"),
 N("Membaca Ruang: Peta, Atlas & Koordinat", RG, ["Unsur-Unsur Peta dan Skala","Membaca Atlas dan Peta Tematik","Koordinat Lintang dan Bujur","Menggambar Sketsa Peta Lingkungan Sekitar"], "Skala Peta Dianggap Tidak Memengaruhi Jarak Sebenarnya"),
 S("Letak & Luas Indonesia", RG, "Letak Astronomis dan Letak Geografis Dianggap Sama"),
 S("Potensi Sumber Daya Alam", RG, "Sumber Daya Alam yang Melimpah Dianggap Tidak Perlu Dikelola"),
 N("Kebutuhan, Kelangkaan & Pilihan", EKO, ["Kebutuhan dan Keinginan Manusia","Kelangkaan Sumber Daya","Skala Prioritas dan Biaya Peluang","Mengambil Keputusan Ekonomi Sehari-hari"], "Langka Dianggap Sama dengan Mahal atau Sulit Ditemukan"),
 N("Kegiatan Ekonomi: Produksi, Distribusi & Konsumsi", EKO, ["Kegiatan Produksi dan Faktor Produksi","Kegiatan Distribusi","Kegiatan Konsumsi","Hubungan Produsen, Distributor, dan Konsumen"], "Distribusi Dianggap Hanya Kegiatan Mengirim Barang"),
 S("Bentuk Interaksi Sosial", IS, "Konflik Dianggap Selalu Berakibat Buruk"),
 S("Pengaruh Interaksi terhadap Kehidupan", IS, "Interaksi Sosial Dianggap Hanya Terjadi secara Tatap Muka"),
],
"8": [
 N("Kerajaan Islam di Indonesia", SJ, ["Masuk dan Berkembangnya Islam di Nusantara","Kerajaan Islam di Sumatra dan Jawa","Kerajaan Islam di Kalimantan, Sulawesi, dan Maluku","Peninggalan dan Akulturasi Budaya Islam"], "Islam Dianggap Datang dan Menyebar Sekaligus di Semua Wilayah"),
 N("Kedatangan Bangsa Eropa dan Kolonialisme", SJ, ["Motif Bangsa Eropa Mencari Rempah","Portugis dan Spanyol di Nusantara","VOC dan Pemerintah Hindia Belanda","Dampak Kolonialisme bagi Masyarakat Nusantara"], "Kolonialisme Dianggap Hanya Berdampak pada Ekonomi"),
 N("Perlawanan terhadap Kolonialisme", SJ, ["Perlawanan Rakyat di Maluku, Aceh, dan Sulawesi","Perlawanan Rakyat di Jawa dan Sumatra","Strategi dan Kelemahan Perlawanan Daerah","Tokoh Perlawanan dan Nilai yang Dapat Diteladani"], "Perlawanan Daerah Dianggap Terkoordinasi secara Nasional"),
 N("Pendudukan Jepang di Indonesia", SJ, ["Kedatangan Jepang dan Kebijakannya","Organisasi Bentukan Jepang","Kehidupan Rakyat pada Masa Pendudukan Jepang","Dampak Pendudukan Jepang bagi Persiapan Kemerdekaan"], "Jepang Dianggap Datang sebagai Pembebas tanpa Kepentingan Sendiri"),
 S("Kondisi Penduduk Indonesia", RG, "Kepadatan Penduduk Dianggap Sama dengan Jumlah Penduduk"),
 S("Interaksi Antarruang", RG, "Interaksi Antarruang Dianggap Hanya Terjadi antarnegara"),
 S("Lembaga Keluarga & Pendidikan", IS, "Lembaga Sosial Dianggap Sama dengan Gedung atau Organisasi"),
 S("Lembaga Ekonomi & Politik", IS, "Lembaga Politik Dianggap Hanya Berperan Saat Pemilu"),
 S("Perubahan Sosial Budaya", IS, "Perubahan Sosial Dianggap Selalu Bermakna Kemajuan"),
 N("Pasar dan Terbentuknya Harga", EKO, ["Pengertian dan Jenis Pasar","Permintaan dan Penawaran","Terbentuknya Harga Keseimbangan","Faktor yang Memengaruhi Harga"], "Harga Naik Dianggap Selalu Karena Penjual Serakah"),
 N("Uang, Bank & Lembaga Keuangan", EKO, ["Fungsi dan Sejarah Uang","Bank dan Lembaga Keuangan Nonbank","Menabung, Kredit, dan Bunga Sederhana","Inflasi dan Nilai Uang"], "Uang Dianggap Sama dengan Kekayaan"),
 N("Ketenagakerjaan dan Kesempatan Kerja", EKO, ["Angkatan Kerja dan Pengangguran","Jenis Pekerjaan dan Sektor Ekonomi","Keterampilan yang Dibutuhkan Dunia Kerja","Hak dan Kewajiban Pekerja"], "Pengangguran Dianggap Sama dengan Tidak Bekerja Sementara"),
],
"9": [
 N("Pergerakan Nasional Indonesia", SJ, ["Latar Belakang Munculnya Pergerakan Nasional","Budi Utomo, Sarekat Islam, dan Indische Partij","Sumpah Pemuda dan Persatuan Bangsa","Tokoh Pergerakan Nasional dan Perannya"], "Pergerakan Nasional Dianggap Hanya Dijalankan oleh Satu Kelompok"),
 N("Proklamasi dan Mempertahankan Kemerdekaan", SJ, ["Persiapan Kemerdekaan: BPUPKI dan PPKI","Peristiwa Rengasdengklok dan Proklamasi","Pembentukan Negara dan Pemerintahan Awal","Perjuangan Mempertahankan Kemerdekaan","Pelajaran dari Perjuangan Kemerdekaan"], "Kemerdekaan Dianggap Selesai pada Saat Proklamasi"),
 S("Perubahan Akibat Interaksi Antarruang", RG, "Interaksi Antarruang Dianggap Selalu Menguntungkan Semua Wilayah"),
 S("Pelestarian Lingkungan", RG, "Pelestarian Lingkungan Dianggap Tanggung Jawab Pemerintah Saja"),
 S("Lembaga Agama", IS, "Lembaga Agama Dianggap Hanya Mengurus Ibadah"),
 S("Penyimpangan Sosial di Masyarakat", IS, "Semua Perilaku yang Berbeda Dianggap Penyimpangan"),
 N("Perdagangan Antardaerah dan Internasional", EKO, ["Alasan Terjadinya Perdagangan","Ekspor, Impor, dan Neraca Perdagangan","Kebijakan Perdagangan dan Bea Masuk","Peran Pelabuhan dan Transportasi dalam Perdagangan"], "Impor Dianggap Selalu Merugikan Perekonomian"),
 N("Kewirausahaan", EKO, ["Ciri dan Sikap Wirausaha","Mengenali Peluang Usaha","Menyusun Rencana Usaha Sederhana","Menghitung Modal, Biaya, dan Keuntungan"], "Wirausaha Dianggap Hanya untuk Pemilik Modal Besar"),
 S("Bentuk Globalisasi", GL_, "Globalisasi Dianggap Hanya Menyangkut Ekonomi"),
 S("Dampak Positif & Negatif Globalisasi", GL_, "Dampak Globalisasi Dianggap Sama bagi Setiap Kelompok"),
 S("Kerja Sama ASEAN", GL_, "ASEAN Dianggap Hanya Kerja Sama Ekonomi"),
 S("Kerja Sama Internasional Lain", GL_, "Organisasi Internasional Dianggap Bisa Memaksa Kebijakan Negara Anggota"),
 S("Modernisasi & Westernisasi", GL_, "Modernisasi Dianggap Sama dengan Meniru Budaya Barat"),
 S("Menghadapi Tantangan Global", GL_, "Menghadapi Globalisasi Dianggap Berarti Menolak Budaya Asing"),
],
}

plan = {
 "mapel": "IPS", "tahap": TB_, "tahaps": TAHAPS, "jenjang": "SMP", "kode": "ips", "cambridge_label": False,
 "grup": [SJ, RG, EKO, IS, GL_], "label": {"kurikulum": "merdeka-smp", "jalur": "smp-mts", "rumpun": "sosial-humaniora"},
 "kelas": kelas,
 "ki": {"jenjang": "SMP / MTs — Kelas 7-9", "kelas": "Kelas {n} SMP/MTs", "bundle": "IPS"},
 "tka": [{"folder": "TKA SMP/MTs", "bundle": "IPS", "kelas": [8, 9]}],
}
json.dump(plan, open("ips_smp.json", "w"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in kelas.items()}, "topik", sum(len(v) for v in kelas.values()), "bab", sum(len(t["bab"]) for v in kelas.values() for t in v))
