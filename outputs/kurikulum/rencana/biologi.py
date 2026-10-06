from sma_gen import build, N
T1 = "Tahap 1 — Dasar Biologi & Keanekaragaman Hayati (SMA)"; T2 = "Tahap 2 — Sel & Jaringan (SMA)"
RL, KL = "Ruang Lingkup Biologi", "Klasifikasi & Keanekaragaman Hayati"
new10 = [
 (RL, "Ruang Lingkup & Metode Ilmiah Biologi", ["Objek, Cabang, dan Peran Biologi","Tingkat Organisasi Kehidupan","Langkah-Langkah Metode Ilmiah","Merancang Percobaan Sederhana dengan Variabel","Menyajikan Data dan Menarik Kesimpulan"], "Hipotesis yang Ditolak Dianggap Percobaan yang Gagal"),
 (RL, "Mikroskop & Pengamatan Mikroskopis", ["Bagian dan Cara Kerja Mikroskop Cahaya","Menyiapkan Preparat dan Mengamati Sel","Menghitung Perbesaran dan Ukuran Objek","Mikroskop Elektron dan Perkembangan Teknologi Pengamatan"], "Perbesaran Lensa Objektif dan Okuler Dijumlahkan"),
 (KL, "Sistem Klasifikasi & Tata Nama Binomial", ["Dasar dan Tujuan Klasifikasi","Tingkatan Takson dari Domain hingga Spesies","Tata Nama Binomial Linnaeus","Kunci Determinasi dan Sistem Lima Kingdom","Sistem Tiga Domain"], "Kemiripan Bentuk Dianggap Selalu Berarti Kekerabatan Dekat"),
 (KL, "Virus", ["Ciri dan Struktur Virus","Reproduksi Virus: Litik dan Lisogenik","Peran Virus bagi Kesehatan dan Lingkungan","Pencegahan dan Penanganan Penyakit Akibat Virus"], "Virus Dianggap Makhluk Hidup Sepenuhnya"),
 (KL, "Archaebacteria & Eubacteria", ["Ciri, Struktur, dan Bentuk Bakteri","Archaebacteria dan Habitat Ekstremnya","Reproduksi dan Pertumbuhan Bakteri","Peran Bakteri: Menguntungkan dan Merugikan"], "Semua Bakteri Dianggap Penyebab Penyakit"),
 (KL, "Protista", ["Ciri Umum dan Pengelompokan Protista","Protista Mirip Hewan (Protozoa)","Protista Mirip Tumbuhan (Alga)","Protista Mirip Jamur dan Perannya"], "Protista Dianggap Sama dengan Bakteri"),
 (KL, "Fungi", ["Ciri dan Struktur Jamur","Klasifikasi Jamur","Reproduksi Jamur","Peran Jamur dalam Kehidupan"], "Jamur Dianggap Tumbuhan"),
 (KL, "Plantae: Lumut, Paku & Tumbuhan Berbiji", ["Ciri Umum dan Pengelompokan Tumbuhan","Lumut dan Daur Hidupnya","Paku dan Daur Hidupnya","Tumbuhan Biji Terbuka (Gymnospermae)","Tumbuhan Biji Tertutup: Monokotil dan Dikotil"], "Lumut dan Paku Dianggap Tumbuhan Berbiji"),
 (KL, "Animalia: Invertebrata", ["Ciri Umum dan Pengelompokan Hewan","Porifera dan Cnidaria","Platyhelminthes, Nemathelminthes, dan Annelida","Mollusca, Arthropoda, dan Echinodermata"], "Hewan Tak Bertulang Belakang Dianggap Sederhana dan Tidak Penting"),
 (KL, "Animalia: Vertebrata", ["Ciri Umum Chordata","Pisces dan Amphibia","Reptilia dan Aves","Mammalia dan Peranannya"], "Paus dan Lumba-Lumba Dianggap Ikan"),
]
tambah = []
prev = "START"
for grup, judul, bab, ku in new10:
    tambah.append((10, prev, N(judul, T1, grup, bab, ku))); prev = judul
tambah.append((11, "Kultur Jaringan", N("Pertumbuhan & Perkembangan Tumbuhan", T2, "Jaringan Tumbuhan", ["Pertumbuhan Primer dan Sekunder","Perkecambahan dan Faktor yang Memengaruhinya","Hormon Tumbuhan: Auksin, Giberelin, Sitokinin","Hormon Tumbuhan: Etilen dan Asam Absisat","Gerak Tumbuhan dan Fotoperiodisme"], "Pertumbuhan dan Perkembangan Dianggap Sama")))
build("Biologi", "bio", [T1, "Tahap 2 — Sel%", "Tahap 3 — Fisiologi%", "Tahap 4 — Metabolisme%", "Tahap 5 — Evolusi%"], "sains-teknologi", "Biologi",
 pindah_grup={"Ekologi": 10}, tambah=tambah)
