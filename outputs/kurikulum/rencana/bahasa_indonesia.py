#!/usr/bin/env python3
"""Rencana kurikulum Bahasa Indonesia Kelas 1-12 (Fase A-F). Menghasilkan bahasa_indonesia.json."""
import json, subprocess

def q(sql):
    r = subprocess.run(["docker","exec","-i","titian-bun-postgres","psql","-U","titian","titian_bun","-At","-c",sql],capture_output=True,text=True)
    return [l for l in r.stdout.split("\n") if l]

SUBJ = "(select id from modules where title='Bahasa Indonesia' and parent_id=(select id from modules where title='Semua Mata Pelajaran' and parent_id is null))"
TAHAPS = q("select title from modules where parent_id=%s order by order_index" % SUBJ)
TA = [t for t in TAHAPS if t.startswith("Tahap A")][0]; TB = [t for t in TAHAPS if t.startswith("Tahap B")][0]; TD = [t for t in TAHAPS if t.startswith("Tahap D")][0]
RUMPUN = (q("select l.value from module_labels l join modules s on s.id=l.module_id where s.title='Menulis Huruf & Kata' and l.kind='rumpun' limit 1") or ["bahasa-sastra"])[0]

def bab_of(topic):
    return q("select b.title from module_items b join modules m on m.id=b.module_id join modules g on g.id=m.parent_id join modules t on t.id=g.parent_id where b.node_type='section' and b.status<>'archived' and m.title=$$%s$$ and t.parent_id=%s order by b.order_index" % (topic, SUBJ))

def keep(topic): return [{"dari": topic, "judul": t} for t in bab_of(topic)]
def E(topik): return {"topik": topik, "bab": keep(topik)}            # topik lama, tidak berpindah grup
def N(topik, tahap, grup, bab): return {"topik": topik, "tahap": tahap, "grup": grup, "bab": bab}   # topik baru

MB, MP = "Menyimak & Berbicara", "Membaca & Menulis Permulaan"
KD, TS = "Kosakata & Struktur Dasar", "Teks Sederhana"
MBSMP = "Menyimak & Berbicara SMP"; KEB, TEKS = "Kebahasaan SMP", "Teks Fungsional SMP"

kelas = {
"1": [E("Mengenal Huruf & Bunyi"), E("Suku Kata & Kata"), E("Membaca Kata & Kalimat Sederhana"), E("Menyimak Cerita"), E("Bercerita Lisan"),
      N("Menyimak dan Menirukan", TA, MB, ["Menyimak Bunyi di Sekitar Kita","Menirukan Kata dan Kalimat Pendek","Menyimak Perintah Sederhana","Bernyanyi dan Bertepuk Menurut Suku Kata","Kesalahan Umum: Kata yang Didengar Tertukar dengan Kata Mirip"])],
"2": [E("Menulis Huruf & Kata"), E("Menulis Kalimat Sederhana"), E("Tanda Baca Dasar"), E("Bertanya & Menjawab"), E("Menyampaikan Pendapat Sederhana"),
      N("Membaca Teks Pendek dan Menjawab Pertanyaan", TA, MP, ["Membaca Teks Pendek Tiga sampai Lima Kalimat","Menemukan Tokoh dan Tempat dalam Teks","Menjawab Pertanyaan Apa, Siapa, dan di Mana dari Teks","Menyimpulkan Kejadian Sederhana dalam Cerita","Kesalahan Umum: Menjawab dari Ingatan, Bukan dari Teks"])],
"3": [E("Kosakata Baru & Makna Kata"), E("Kata Benda, Kata Kerja & Kata Sifat"), E("Kalimat Berita, Tanya & Perintah"), E("Berbalas Pantun & Permainan Bahasa"),
      N("Menyimak Informasi Lisan", TA, MB, ["Menyimak Pengumuman Singkat","Mencatat Kata Penting dari yang Disimak","Menjawab Pertanyaan tentang Isi Simakan","Menceritakan Kembali yang Disimak","Kesalahan Umum: Mendengar Sebagian lalu Menebak Sisanya"]),
      N("Menulis Paragraf Sederhana", TA, MP, ["Kalimat Utama dan Kalimat Penjelas","Menulis Paragraf dari Gambar","Menyusun Kalimat Menjadi Paragraf","Menulis Cerita Pendek Tiga Kalimat","Kesalahan Umum: Kalimat Tidak Berhubungan dalam Satu Paragraf"])],
"4": [E("Teks Deskripsi Sederhana"), E("Teks Narasi Sederhana"), E("Huruf Kapital & Tanda Baca"), E("Sinonim & Antonim Dasar"), E("Menemukan Informasi (Retrieve)"),
      N("Berbicara: Melaporkan dan Menyampaikan Informasi", TA, MB, ["Menyusun Pokok Informasi yang Akan Disampaikan","Menyampaikan Informasi dengan Suara Jelas","Memakai Gambar sebagai Alat Bantu","Menjawab Pertanyaan Pendengar","Kesalahan Umum: Berbicara Terlalu Cepat atau Terlalu Pelan"])],
"5": [E("Teks Petunjuk & Prosedur"), E("Teks Informasi Sederhana"), E("Teks Informasi"),
      N("Kata Berimbuhan dan Kata Ulang", TA, KD, ["Awalan me- dan ber-","Akhiran -an dan -kan","Kata Ulang dan Maknanya","Membedakan Kata Dasar dan Kata Berimbuhan","Kesalahan Umum: Awalan di- Tertukar dengan Kata Depan di"]),
      N("Menulis Paragraf Narasi dan Deskripsi", TA, TS, ["Kerangka Cerita: Awal, Tengah, Akhir","Menulis Paragraf Deskripsi Tempat","Menulis Paragraf Narasi dari Pengalaman","Menyunting Ejaan dan Tanda Baca Tulisan Sendiri","Kesalahan Umum: Cerita Tidak Memiliki Akhir"])],
"6": [E("Puisi Anak & Pantun"), E("Surat Pribadi & Undangan"), E("Interpretasi & Integrasi Teks"),
      {"topik": "Teks Sastra", "bab": ["Memahami Tema dan Amanat Teks Sastra","Menganalisis Tokoh dan Latar","Menafsirkan Bahasa Kiasan dan Ungkapan","Menilai Pesan Moral dan Budaya dalam Teks Sastra"]},
      N("Pidato dan Presentasi Sederhana", TA, MB, ["Menyusun Naskah Pidato Singkat","Intonasi, Jeda, dan Ekspresi","Menyampaikan Presentasi dengan Bahan Visual","Menanggapi Pertanyaan Audiens","Kesalahan Umum: Naskah Dibaca Tanpa Menatap Audiens"]),
      N("Teks Laporan Pengamatan Sederhana", TA, TS, ["Tujuan dan Ciri Laporan Pengamatan","Mengamati dan Mencatat Data","Menyusun Laporan Tiga Bagian","Menyajikan Data dalam Tabel Sederhana","Kesalahan Umum: Pendapat Pribadi Masuk ke Laporan"])],
"7": [E("Puisi Rakyat: Pantun, Syair & Gurindam"), E("Cerita Fabel & Legenda"), E("Kalimat Tunggal & Majemuk"), E("Konjungsi & Kata Hubung"), E("Teks Deskripsi"), E("Teks Narasi & Cerita Fantasi"), E("Teks Prosedur"), E("Evaluasi & Refleksi Teks"),
      N("Menyimak Informasi dan Menyimpulkan", TB, MBSMP, ["Menyimak Teks Lisan dan Menemukan Gagasan Utama","Mencatat Poin Penting Sambil Menyimak","Menyimpulkan Isi Simakan","Menilai Ketepatan Informasi yang Didengar","Kesalahan Umum: Kesimpulan Melampaui Isi Simakan"]),
      N("Berbicara: Menceritakan Pengalaman dan Mendeskripsikan", TB, MBSMP, ["Menyusun Urutan Cerita Lisan","Mendeskripsikan Benda atau Tempat Secara Lisan","Memilih Kosakata yang Tepat saat Berbicara","Menanggapi Teman Bicara dengan Santun","Kesalahan Umum: Cerita Lisan Melompat-lompat"]),
      N("Kosakata: Makna Kata, Ungkapan, dan Peribahasa", TB, KEB, ["Makna Kata dalam Konteks Kalimat","Ungkapan dan Idiom Sehari-hari","Peribahasa dan Nilai yang Dikandungnya","Membedakan Kata Bermakna Mirip","Kesalahan Umum: Peribahasa Diartikan Secara Harfiah"])],
"8": [E("Cerpen"), E("Drama Singkat"), E("Imbuhan & Pembentukan Kata"), E("Kata Baku & Tidak Baku"), E("Teks Laporan Percobaan"), E("Teks Persuasi"),
      E("Struktur Teks Berita"), E("Unsur ADIKSIMBA (5W+1H)"), E("Kaidah Kebahasaan Teks Berita"), E("Menulis Teks Berita"), E("Fakta & Opini dalam Berita"), E("Mengenali Berita Palsu (Hoaks)"),
      E("Ciri & Jenis Iklan"), E("Struktur Teks Iklan"), E("Kaidah Kebahasaan Iklan"), E("Teks Multimodal (Grafik, Tabel, Infografis)"),
      N("Wawancara dan Pidato", TB, MBSMP, ["Menyusun Pertanyaan Wawancara","Melakukan Wawancara dan Mencatat Jawaban","Menyusun Naskah Pidato Persuasif","Menyampaikan Pidato dengan Intonasi dan Gestur","Kesalahan Umum: Pertanyaan Wawancara Hanya Bisa Dijawab Ya atau Tidak"])],
"9": [E("Unsur Intrinsik & Ekstrinsik"), E("Ejaan Bahasa Indonesia (EYD)"), E("Kalimat Efektif Dasar"), E("Teks Tanggapan"), E("Teks Rekon & Cerita Inspiratif"), E("Menyimpulkan Isi Tersirat"), E("Teks Digital & Media Daring"),
      E("Menyusun Slogan"), E("Merancang Poster"), E("Menganalisis Daya Persuasi Iklan"),
      N("Teks Argumentasi", TB, TEKS, ["Klaim, Alasan, dan Bukti dalam Argumentasi","Menyusun Argumen dari Data","Menilai Kekuatan Sebuah Argumen","Menulis Teks Argumentasi Singkat","Kesalahan Umum: Pendapat Dianggap Sama dengan Bukti"]),
      N("Diskusi dan Debat Sederhana", TB, MBSMP, ["Aturan dan Peran dalam Diskusi","Menyampaikan dan Menanggapi Pendapat dalam Diskusi","Menyusun Alasan untuk Mendukung Pendapat","Debat Sederhana: Menyanggah dengan Santun","Kesalahan Umum: Menyerang Orang, Bukan Pendapat"])],
}

# ---- SMA (Kelas 10-12): 92 topik lama disebar rata; 5 duplikat dikeluarkan dari tulang punggung
SMA_KELUAR = ["Ide Pokok & Kalimat Utama", "Membandingkan Dua Teks atau Lebih", "Simpulan & Inferensi", "Strategi Membaca Cepat", "Perbaikan Kalimat & Ejaan"]
sma10 = ["Kelas Kata","Frasa, Klausa & Kalimat","Penulisan Huruf Kapital","Penulisan Kata & Partikel","Sinonim & Antonim","Homonim, Homofon & Homograf","Paragraf & Pengembangannya","Ringkasan & Parafrasa","Menemukan Ide Pokok","Menyimpulkan Isi Bacaan","Makna Tersirat & Inferensi","Skimming & Scanning",
 "Struktur Teks LHO","Kaidah Kebahasaan LHO","Fakta & Klasifikasi dalam LHO","Menulis Teks LHO","Menyunting Teks LHO",
 "Struktur Teks Prosedur","Kaidah Kebahasaan Prosedur","Menulis Teks Prosedur","Struktur Teks Eksplanasi","Pola Pengembangan Eksplanasi","Menulis Teks Eksplanasi",
 "Struktur & Tesis Eksposisi","Argumen & Fakta Pendukung","Menulis Teks Eksposisi",
 "Struktur Teks Biografi","Unsur Kebahasaan Biografi","Keteladanan Tokoh dalam Biografi","Menceritakan Kembali Isi Biografi","Menulis Biografi Singkat"]
sma11 = ["Ciri & Struktur Anekdot","Makna Tersirat Anekdot","Nilai & Karakteristik Hikayat","Perbandingan Hikayat & Cerpen","Unsur Intrinsik Cerpen","Menulis Cerpen",
 "Unsur Fisik & Batin Puisi","Diksi & Citraan dalam Puisi","Majas & Gaya Bahasa","Rima, Irama & Tipografi","Memahami Amanat Puisi","Menulis Puisi","Musikalisasi & Pembacaan Puisi",
 "Struktur Teks Negosiasi","Kesantunan dalam Negosiasi","Simulasi Negosiasi",
 "Struktur Teks Debat","Mosi & Penyusunan Argumen","Peran Tim Afirmasi, Oposisi & Netral","Menyanggah dengan Santun","Menyimpulkan Hasil Debat","Etika Berdiskusi",
 "Unsur & Struktur Resensi","Menulis Resensi Buku",
 "Kalimat Efektif","Kalimat Majemuk","Tanda Baca","Penulisan Unsur Serapan","Polisemi & Hiponim","Makna Denotatif & Konotatif","Menilai Kredibilitas Sumber","Membandingkan Dua Teks","Surat Resmi & Surat Lamaran"]
sma12 = ["Struktur Teks Ceramah","Teknik Berceramah","Sistematika Proposal","Kaidah Kebahasaan Proposal","Struktur Karya Ilmiah","Sitasi & Daftar Pustaka","Menulis Karya Ilmiah Sederhana",
 "Struktur Naskah Drama","Menganalisis Pementasan Drama","Struktur Teks Editorial","Fakta & Opini dalam Editorial","Menulis Editorial",
 "Unsur Intrinsik & Ekstrinsik Novel","Analisis Tokoh & Penokohan","Nilai dalam Novel","Teks Kritik & Esai","Perbedaan Kritik & Esai","Menulis Kritik Sastra",
 "Konjungsi & Kohesi","Kesalahan Berbahasa Umum","Penulisan Angka & Bilangan","Bentuk Baku & Tidak Baku","Idiom & Peribahasa","Diksi yang Tepat",
 "Teks Multimodal: Grafik & Infografis","Laporan & Notulen","Presentasi Ilmiah","Penalaran Verbal dalam Bacaan"]
NEWD = "Teks Debat & Diskusi"
kelas["10"] = [E(t) for t in sma10] + [N("Menyimak Kritis dan Menanggapi Informasi Lisan", TD, NEWD, ["Menyimak Pidato dan Menemukan Tujuannya","Membedakan Fakta dan Opini dalam Simakan","Mencatat dan Meringkas yang Disimak","Menanggapi dengan Santun dan Tepat","Kesalahan Umum: Menerima Informasi Lisan tanpa Memeriksa"])]
kelas["11"] = [E(t) for t in sma11]
kelas["12"] = [E(t) for t in sma12] + [N("Teks Argumentasi dan Esai Argumentatif", TD, "Teks Eksposisi & Negosiasi", ["Klaim, Data, dan Jaminan dalam Argumentasi","Menyusun Argumen dari Data","Menilai Kekuatan dan Kelemahan Argumen","Menulis Esai Argumentatif","Kesalahan Umum: Klaim Tanpa Bukti yang Memadai"])]

used = {t["topik"] for v in kelas.values() for t in v}
alltopics = q("select s.title from modules s join modules g on g.id=s.parent_id join modules t on t.id=g.parent_id where t.parent_id=%s and not s.is_folder" % SUBJ)
missing = sorted(set(alltopics) - used - set(SMA_KELUAR))
extra = [t for t in used if t not in alltopics and not any(x["topik"] == t and x.get("tahap") for v in kelas.values() for x in v)]
print("topik lama tak terpakai (di luar duplikat & Tahap F):", [m for m in missing][:40])
print("topik direncanakan tapi tidak ada:", extra)

plan = {
 "mapel": "Bahasa Indonesia", "tahap": TA, "tahaps": TAHAPS, "jenjang": "AUTO", "kode": "bin", "cambridge_label": False,
 "grup": [], "label": {"rumpun": RUMPUN},
 "biarkan": sorted(set(alltopics) - used),
 "kelas": kelas,
 "ki": {"jenjang": {"SD": "SD / MI — Kelas 1-6", "SMP": "SMP / MTs — Kelas 7-9", "SMA": "SMA / MA — Kelas 10-12"},
        "kelas": {"SD": "Kelas {n} SD/MI", "SMP": "Kelas {n} SMP/MTs", "SMA": "Kelas {n} SMA/MA"}, "bundle": "Bahasa Indonesia"},
 "tka": [{"folder": "TKA SD/MI", "bundle": "Bahasa Indonesia", "kelas": [5, 6]}, {"folder": "TKA SMP/MTs", "bundle": "Bahasa Indonesia", "kelas": [8, 9]}],
}
plan.setdefault("tka", []).append({"via": ["TKA SMA/MA", "Mata Pelajaran Wajib"], "bundle": "Bahasa Indonesia", "kelas": [10, 11, 12]})
json.dump(plan, open("bahasa_indonesia.json", "w"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in kelas.items()}, "topik", sum(len(v) for v in kelas.values()), "| dibiarkan:", len(plan["biarkan"]))
