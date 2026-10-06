from sma_gen import build, N
T2 = "Tahap 2 — Struktur Atom & Ikatan"
build("Kimia", "kim", ["Tahap 2 — Struktur%", "Tahap 3 — Stoikiometri%", "Tahap 4 — Kimia Fisik%", "Tahap 5 — Elektrokimia%"], "sains-teknologi", "Kimia",
 pindah={"Molaritas, Molalitas & Fraksi Mol": 11, "Pengenceran Larutan": 11},
 pindah_grup={"Hidrokarbon & Minyak Bumi": 10, "Konsentrasi & Sifat Koligatif": 12},
 tambah=[(10, "START", N("Ilmu Kimia, Keselamatan Laboratorium & Kimia Hijau", T2, "Struktur Atom", ["Ruang Lingkup dan Peran Ilmu Kimia","Metode Ilmiah dalam Percobaan Kimia","Keselamatan Kerja dan Simbol Bahaya Bahan Kimia","Prinsip Kimia Hijau dan Pengelolaan Limbah"], "Bahan Kimia Dianggap Selalu Berbahaya")),
         ])
