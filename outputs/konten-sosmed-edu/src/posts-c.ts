import type { Post } from "./types";

// Hari 21–30 (10–19 Nov 2026): KIP Kuliah, writing, kosakata, rencana belajar, SNBP, kalender PTN.
export const C: Post[] = [
  {
    id: "21", name: "kip-kuliah-mulai-dari-data",
    slides: [
      { bg: "soft", kicker: "Mau daftar KIP Kuliah?", title: "Persiapannya <a>mulai dari data keluarga</a>", body: "Penerima dilihat dari data kesejahteraan keluarga. Rapikan dari sekarang.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Langkah persiapan", title: "4 hal yang bisa <a>kamu lakukan sekarang</a>", steps: [
        { w: "1", t: "Cek data keluargamu", d: "Tanya ke desa/kelurahan atau dinas sosial" },
        { w: "2", t: "Data nggak sesuai?", d: "Ajukan pemutakhiran lewat desa/kelurahan" },
        { w: "3", t: "Kumpulkan dokumen", d: "Identitas, rapor, bukti ekonomi keluarga" },
        { w: "4", t: "Pantau jadwal resmi", d: "Tiap tahun bisa berbeda" },
      ] },
      { bg: "soft", kicker: "Biar nggak terlambat", title: "Mulai dari <a>sebelum</a> pendaftaran dibuka.", body: "Pemutakhiran data butuh waktu, jadi jangan menunggu pengumuman." },
      { bg: "yellow", kicker: "Catatan", title: "Aturan 2027 <a>belum diumumkan.</a>", body: "Pantau portal resmi KIP Kuliah dan pengumuman kampus.", src: "Cek: kip-kuliah.kemendiktisaintek.go.id", cta: true, hand: "tips kuliah di" },
    ],
  },
  {
    id: "22", name: "struktur-esai-opini",
    slides: [
      { bg: "cream", kicker: "Writing IELTS dan TOEFL", title: "Struktur esai opini <a>yang rapi</a>", body: "Kerangka 4 paragraf yang bisa dipakai berulang.", note: "geser →" },
      { bg: "soft", dense: true, kicker: "Kerangka", title: "4 paragraf, <a>satu argumen</a>", steps: [
        { w: "1", t: "Pembuka", d: "Jelaskan topik + nyatakan sikapmu" },
        { w: "2", t: "Alasan pertama", d: "Pernyataan, penjelasan, contoh" },
        { w: "3", t: "Alasan kedua", d: "Pernyataan, penjelasan, contoh" },
        { w: "4", t: "Penutup", d: "Tegaskan kembali sikapmu" },
      ] },
      { bg: "cream", dense: true, kicker: "Frasa pembantu", title: "Biar <a>mengalir</a>", items: [{ e: "➕", t: "Menambah", d: "Moreover, In addition" }, { e: "↔️", t: "Membandingkan", d: "However, On the other hand" }, { e: "🏁", t: "Menyimpulkan", d: "In conclusion, To sum up" }] },
      { bg: "soft", dense: true, kicker: "Kebiasaan baik", title: "Sebelum <a>menulis</a>", checks: ["Luangkan 3–5 menit untuk kerangka", "Satu paragraf, satu ide", "Sisakan waktu membaca ulang"] },
      { bg: "yellow", kicker: "Latihan", title: "Tulis <a>satu paragraf</a> tiap hari.", body: "Pendek tapi rutin lebih ampuh.", tag: "Segera hadir: mock test", cta: true, hand: "latihan bahasa di" },
    ],
  },
  {
    id: "23", name: "10-kata-akademik-bahasa-inggris",
    slides: [
      { bg: "yellow", kicker: "Naikin kosakata", title: "10 kata <a>akademik</a> yang sering muncul", body: "Sering dipakai di bacaan, esai, dan presentasi.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Kata 1–3", title: "Mulai <a>dari sini</a>", items: [{ e: "🔍", t: "analyze", d: "menganalisis" }, { e: "🧾", t: "evidence", d: "bukti" }, { e: "⭐", t: "significant", d: "penting, berarti" }] },
      { bg: "soft", dense: true, kicker: "Kata 4–6", title: "Lanjut <a>tiga lagi</a>", items: [{ e: "🧩", t: "factor", d: "faktor" }, { e: "💥", t: "impact", d: "dampak" }, { e: "🧭", t: "approach", d: "pendekatan" }] },
      { bg: "cream", dense: true, kicker: "Kata 7–10", title: "Empat <a>terakhir</a>", items: [{ e: "❓", t: "issue", d: "isu, masalah" }, { e: "📌", t: "require", d: "membutuhkan" }, { e: "💡", t: "concept", d: "konsep" }, { e: "📖", t: "according to", d: "menurut" }] },
      { bg: "soft", dense: true, kicker: "Cara menghafal", title: "Pakai dalam <a>kalimatmu sendiri</a>", checks: ["Tulis satu kalimat tentang hidupmu per kata", "Ulang di hari ke-2, ke-4, dan ke-7", "Ucapkan keras-keras"] },
      { bg: "yellow", kicker: "Besok lagi", title: "Kata baru <a>dipakai</a>, bukan dicatat doang.", cta: true, hand: "belajar bahasa di" },
    ],
  },
  {
    id: "24", name: "trik-listening",
    slides: [{
      bg: "cream", dense: true, kicker: "Listening", title: "4 trik <a>listening</a> yang sering terlewat",
      checks: ["Baca soal dulu sebelum audio diputar", "Garis bawahi kata kunci", "Tebak jenis jawabannya: angka, nama, atau tempat", "Satu soal terlewat? Lanjut, jangan menengok ke belakang"],
      note: "simpan buat latihan~", cta: true, hand: "latihan bahasa di",
    }],
  },
  {
    id: "25", name: "rencana-belajar-8-minggu",
    slides: [
      { bg: "navy", kicker: "Target skor tes bahasa?", title: "Rencana belajar <a>8 minggu</a>", body: "Cocok untuk IELTS maupun TOEFL. Sesuaikan waktunya dengan jadwalmu.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Peta 8 minggu", title: "Dari <a>fondasi</a> sampai simulasi", steps: [
        { w: "Mgg 1–2", t: "Fondasi", d: "Tes awal, kosakata, tata bahasa dasar" },
        { w: "Mgg 3–4", t: "Reading dan Listening", d: "Latihan soal + analisis salah" },
        { w: "Mgg 5–6", t: "Writing dan Speaking", d: "Tulis dan rekam tiap hari" },
        { w: "Mgg 7", t: "Simulasi penuh", d: "Pakai timer, seperti tes asli" },
        { w: "Mgg 8", t: "Rapikan", d: "Perbaiki titik lemah, istirahat cukup" },
      ] },
      { bg: "soft", dense: true, kicker: "Rutinitas harian", title: "Sedikit, tapi <a>tiap hari</a>", checks: ["30–60 menit per hari lebih awet dari maraton", "Catat kesalahan, ulang pekan depannya", "Satu hari libur per pekan"] },
      { bg: "cream", kicker: "Ingat", title: "Tes awal itu <a>bukan vonis.</a>", body: "Gunanya cuma untuk tahu mulai dari mana." },
      { bg: "yellow", kicker: "Mulai minggu 1", title: "Bangun <a>kebiasaannya</a> dulu.", body: "Latihan harian bahasa Inggris gratis di Kampung Bahasa Pare.", cta: true, hand: "mulai di" },
    ],
  },
  {
    id: "26", name: "4-pertanyaan-pilih-jurusan",
    slides: [{
      bg: "soft", dense: true, kicker: "Bingung pilih jurusan?", title: "Jawab <a>4 pertanyaan</a> ini dulu",
      items: [{ e: "⏳", t: "Apa yang bikin kamu lupa waktu?" }, { e: "📊", t: "Pelajaran apa yang nilainya konsisten?" }, { e: "💼", t: "Seperti apa pekerjaan yang kamu bayangkan?" }, { e: "🔎", t: "Apa prospek dan biayanya?", d: "Cari tahu dari alumni dan situs kampus" }],
      note: "tulis jawabannya, lalu bandingkan~", cta: true, hand: "tips kuliah di",
    }],
  },
  {
    id: "27", name: "setelah-tka-apa-selanjutnya",
    slides: [
      { bg: "yellow", kicker: "16 November", tag: "Susulan mulai", title: "Setelah <a>TKA</a>, ngapain?", body: "Ujian susulan dijadwalkan 16–29 November 2026.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Yang sudah ujian", title: "Sambil menunggu <a>hasil</a>", checks: ["Istirahat dulu, kamu sudah berjuang", "Lanjutkan belajar untuk rapor dan seleksi PTN", "Mulai riset jurusan dan kampus incaran"] },
      { bg: "soft", dense: true, kicker: "Yang penting dicatat", title: "Dua <a>tanggal</a> ini", stats: [{ n: "16–29 Nov", l: "ujian susulan" }, { n: "23 Des", l: "pengumuman hasil" }] },
      { bg: "yellow", kicker: "Soal seleksi PTN", title: "Hubungannya dengan SNBP/SNBT? <a>Tunggu panitia.</a>", body: "Ketentuan resmi 2027 akan diumumkan panitia SNPMB.", src: "Cek di snpmb.id.", cta: true, hand: "tips masuk PTN di" },
    ],
  },
  {
    id: "28", name: "snbp-yang-perlu-dicek",
    slides: [
      { bg: "soft", kicker: "Mau coba SNBP?", title: "5 hal yang <a>perlu kamu cek</a>", body: "Berdasarkan pola SNBP tahun-tahun terakhir.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Cek 1", title: "Data di <a>PDSS</a>", checks: ["NISN-mu terdaftar", "Nilai rapor semester 1–5 sudah diinput sekolah"] },
      { bg: "soft", dense: true, kicker: "Cek 2", title: "Kuota <a>sekolahmu</a>", body: "Hanya siswa terbaik tiap sekolah yang eligible. Acuan sebelumnya: kuota menurut akreditasi sekolah.", stats: [{ n: "A", l: "40%" }, { n: "B", l: "25%" }, { n: "C", l: "5%" }], src: "Acuan terakhir; aturan 2027 belum diumumkan." },
      { bg: "cream", dense: true, kicker: "Cek 3", title: "Prodi yang <a>realistis</a>", checks: ["Lihat daya tampung dan peminat tahun lalu", "Pilih satu yang ambisius, satu yang aman"] },
      { bg: "soft", dense: true, kicker: "Cek 4", title: "Untuk seni dan olahraga", checks: ["Siapkan portofolio khusus", "Cek ketentuan unggah di panitia"] },
      { bg: "yellow", kicker: "Terakhir", title: "Selalu <a>pegang aturan resmi.</a>", body: "Jadwal dan syarat 2027 diumumkan panitia SNPMB.", src: "Cek di snpmb.id.", cta: true, hand: "tips masuk PTN di" },
    ],
  },
  {
    id: "29", name: "3-teknik-belajar-ampuh",
    slides: [
      { bg: "cream", kicker: "Belajar lebih awet", title: "3 teknik belajar <a>yang terbukti membantu</a>", body: "Lebih sedikit waktu, lebih lama ingatnya.", note: "geser →" },
      { bg: "soft", kicker: "Teknik 1", title: "<a>Active recall</a>", body: "Tutup catatan, lalu coba ingat atau jelaskan dari kepala. Bagian yang macet itulah yang perlu diulang.", items: [{ e: "🧠", t: "Contoh", d: "Jawab soal tanpa melihat materi." }] },
      { bg: "cream", kicker: "Teknik 2", title: "<a>Spaced repetition</a>", body: "Ulang materi dengan jarak waktu yang makin lebar, bukan sekaligus.", items: [{ e: "🔁", t: "Contoh", d: "Ulang hari ini, 2 hari lagi, lalu seminggu lagi." }] },
      { bg: "soft", kicker: "Teknik 3", title: "<a>Pomodoro</a>", body: "Fokus 25 menit, istirahat 5 menit. Ulang beberapa putaran.", items: [{ e: "⏱️", t: "Contoh", d: "Taruh HP jauh selama 25 menit." }] },
      { bg: "yellow", kicker: "Kombinasi", title: "Belajar sampai <a>bisa & terbiasa.</a>", body: "Yang salah diulang sampai paham. Itu cara kami belajar.", cta: true, hand: "belajar bareng di" },
    ],
  },
  {
    id: "30", name: "kalender-menuju-ptn-2027",
    slides: [
      { bg: "navy", kicker: "Angkatan 2027", title: "Kalender <a>menuju PTN</a> 2027", body: "Yang sudah pasti dan yang masih perkiraan.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Sudah dijadwalkan", title: "Satu tanggal <a>yang pasti</a>", steps: [{ w: "23 Des 2026", t: "Pengumuman hasil TKA", hot: true }] },
      { bg: "soft", dense: true, kicker: "Masih perkiraan", title: "Yang <a>belum resmi</a>", steps: [
        { w: "Desember", t: "Kalender resmi SNPMB", d: "Biasanya diumumkan sekitar waktu ini" },
        { w: "Feb 2027", t: "Pendaftaran SNBP", d: "Perkiraan" },
        { w: "Mar–Apr 2027", t: "Pendaftaran & tes SNBT", d: "Perkiraan" },
      ] },
      { bg: "cream", dense: true, kicker: "Mulai sekarang", title: "Yang bisa <a>kamu siapkan</a>", checks: ["Rapikan nilai rapor", "Riset jurusan dan kampus", "Biasakan latihan soal rutin"] },
      { bg: "yellow", kicker: "Catatan", title: "Tanggal di atas <a>perkiraan</a>, kecuali yang jelas disebut.", body: "Pegang pengumuman resmi panitia SNPMB.", src: "Cek di snpmb.id.", cta: true, hand: "tips masuk PTN di" },
    ],
  },
];
