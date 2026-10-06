from sma_gen import build, N
import os
V = ("TKA SMA/MA", "Pilihan Soshum")
def go(*a, **k):
    build(*a, tka_via=V, **k)

go("Ekonomi", "eko", ["Tahap 1 — Pengantar%", "Tahap 2 — Ekonomi Mikro%", "Tahap 3 — Ekonomi Makro%", "Tahap 4 — Ekonomi Terapan%"], "ekonomi-bisnis", "Ekonomi",
   pindah_grup={"Konsep Dasar Ilmu Ekonomi": 10, "Sistem Ekonomi": 10, "Kegiatan Ekonomi": 10, "Permintaan, Penawaran & Harga": 10, "Elastisitas": 10,
                "Struktur Pasar": 11, "Teori Perilaku Konsumen & Produsen": 11, "Pendapatan Nasional": 11, "Konsumsi, Tabungan & Investasi": 11, "Uang & Perbankan": 11, "Inflasi & Kebijakan Moneter": 11,
                "APBN, APBD & Kebijakan Fiskal": 12, "Ketenagakerjaan & Pengangguran": 12, "Perdagangan Internasional": 12, "Pasar Modal & Investasi": 12, "Badan Usaha & Koperasi": 12, "Ekonomi Pembangunan & Kesejahteraan": 12})

go("Geografi", "geo", ["Tahap 1 — Dasar Geografi%", "Tahap 2 — Geografi Fisik%", "Tahap 3 — Geografi Manusia%", "Tahap 4 — Kebencanaan%"], "sosial-humaniora", "Geografi",
   pindah_grup={"Hakikat & Konsep Geografi": 10, "Peta & Penginderaan Jauh": 10, "Sistem Informasi Geografis": 10, "Bumi & Tata Surya": 10, "Litosfer & Tenaga Geologi": 10,
                "Atmosfer & Iklim": 11, "Hidrosfer": 11, "Biosfer": 11, "Sumber Daya Alam": 11, "Mitigasi Bencana": 11,
                "Kependudukan": 12, "Desa, Kota & Wilayah": 12, "Geografi Regional Dunia": 12, "Poros Maritim & Ketahanan Pangan": 12},
   tambah=[(12, None, N("Pembangunan Berkelanjutan & Tata Ruang Wilayah", "Tahap 4 — Kebencanaan & Geografi Global", "Poros Maritim & Ketahanan Pangan",
     ["Konsep dan Pilar Pembangunan Berkelanjutan","Tata Ruang dan Perencanaan Wilayah","Daya Dukung dan Daya Tampung Lingkungan","Analisis Kasus Pembangunan Wilayah di Indonesia"], "Pembangunan Dianggap Selalu Bertentangan dengan Pelestarian Lingkungan"))])

go("Sejarah", "sej", ["Tahap 1 — Dasar Ilmu Sejarah%", "Tahap 2 — Indonesia Masa%", "Tahap 3 — Kolonialisme%", "Tahap 4 — Indonesia Merdeka%", "Tahap 5 — Sejarah Dunia%"], "sosial-humaniora", "Sejarah",
   pindah_grup={"Konsep Dasar Sejarah": 10, "Sumber & Metode Sejarah": 10, "Masa Praaksara": 10, "Kerajaan Hindu-Buddha": 10, "Kerajaan Islam Nusantara": 10, "Peradaban Kuno": 10,
                "Kolonialisme & Imperialisme": 11, "Perlawanan Daerah": 11, "Pergerakan Nasional": 11, "Pendudukan Jepang": 11, "Proklamasi & Revolusi Kemerdekaan": 11, "Revolusi Besar Dunia": 11,
                "Demokrasi Liberal & Terpimpin": 12, "Orde Baru": 12, "Reformasi & Indonesia Kontemporer": 12, "Perang Dunia & Perang Dingin": 12})

go("Sosiologi", "sos", ["Tahap 1 — Dasar Sosiologi%", "Tahap 2 — Struktur%", "Tahap 3 — Perubahan%", "Tahap 4 — Penelitian%"], "sosial-humaniora", "Sosiologi",
   pindah_grup={"Perilaku Menyimpang & Pengendalian Sosial": 11})

go("Akuntansi", "akt", ["Tahap 1 — Dasar Akuntansi%", "Tahap 2 — Siklus%", "Tahap 3 — Akuntansi Perusahaan Dagang%", "Tahap 4 — Akuntansi Kejuruan%"], "ekonomi-bisnis", "Akuntansi",
   pindah_grup={"Pengantar Akuntansi": 10, "Persamaan Dasar Akuntansi": 10, "Akun & Mekanisme Debit-Kredit": 10, "Pencatatan & Penggolongan": 10, "Penyesuaian & Kertas Kerja": 10, "Laporan Keuangan & Penutupan": 10,
                "Transaksi Perusahaan Dagang": 11, "Jurnal Khusus & Buku Pembantu": 11, "Persediaan & Harga Pokok Penjualan": 11, "Siklus Akhir Perusahaan Dagang": 11,
                "Akuntansi Perusahaan Manufaktur": 12, "Komputer Akuntansi": 12, "Administrasi Pajak": 12, "Praktik Akuntansi Lembaga": 12})
