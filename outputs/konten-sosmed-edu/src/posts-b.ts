import type { Post } from "./types";

// Hari 11–20 (31 Okt – 9 Nov 2026): SNBT, beasiswa, IELTS/TOEFL, speaking.
export const B: Post[] = [
  {
    id: "11", name: "7-subtes-utbk-snbt",
    slides: [
      { bg: "navy", kicker: "Mau SNBT?", title: "Kenalan sama <a>7 subtes</a> UTBK", body: "Biar tahu apa yang diujikan, bukan cuma ikut-ikutan belajar.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Kelompok 1: Tes Potensi Skolastik", title: "4 subtes <a>kemampuan berpikir</a>", items: [{ e: "🧠", t: "Penalaran Umum" }, { e: "📚", t: "Pengetahuan dan Pemahaman Umum" }, { e: "📖", t: "Pemahaman Bacaan dan Menulis" }, { e: "➗", t: "Pengetahuan Kuantitatif" }] },
      { bg: "soft", kicker: "Kelompok 2", title: "<a>Literasi</a> dua bahasa", items: [{ e: "🇮🇩", t: "Literasi Bahasa Indonesia", d: "Memahami dan menyimpulkan teks" }, { e: "🇬🇧", t: "Literasi Bahasa Inggris", d: "Membaca teks berbahasa Inggris" }] },
      { bg: "cream", kicker: "Kelompok 3", title: "Penalaran <a>Matematika</a>", body: "Bukan hafalan rumus, tapi menalar masalah sehari-hari dengan konsep matematika.", items: [{ e: "🧩", t: "Latihan terbaik", d: "Banyak soal cerita dengan variasi." }] },
      { bg: "soft", dense: true, kicker: "Strategi", title: "Mulai dari <a>yang paling lemah</a>", checks: ["Coba satu paket soal untuk lihat titik lemahmu", "Fokus perbaiki satu subtes tiap pekan", "Latihan dengan timer"] },
      { bg: "yellow", kicker: "Catatan", title: "Komposisi 2027 <a>belum final.</a>", body: "Struktur di atas mengikuti pola beberapa tahun terakhir. Cek panitia SNPMB untuk yang resmi.", src: "Cek di snpmb.id.", tag: "Segera hadir: latihan SNBT", cta: true, hand: "tips masuk PTN di" },
    ],
  },
  {
    id: "12", name: "mitos-vs-fakta-masuk-ptn",
    slides: [
      { bg: "yellow", kicker: "Jangan percaya dulu", title: "3 mitos masuk PTN <a>yang sering salah kaprah</a>", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Mitos 1", title: "“Rapor bagus <a>pasti</a> lolos SNBP.”", cmp: [{ h: "Mitos", rows: ["Nilai tinggi sudah cukup"] }, { h: "Fakta", rows: ["Kamu juga harus masuk kuota sekolah (eligible)", "Lalu bersaing di prodi pilihanmu"] }] },
      { bg: "soft", dense: true, kicker: "Mitos 2", title: "“Nilai UTBK = <a>jumlah soal benar</a>.”", cmp: [{ h: "Mitos", rows: ["Semua soal bobotnya sama"] }, { h: "Fakta", rows: ["Nilai memakai IRT", "Tingkat kesulitan soal ikut diperhitungkan"] }] },
      { bg: "cream", dense: true, kicker: "Mitos 3", title: "“Pilih jurusan <a>yang lagi populer</a> aja.”", cmp: [{ h: "Mitos", rows: ["Populer = pasti cocok"] }, { h: "Fakta", rows: ["Cocok minat dan kemampuan bikin kuliah lebih lancar", "Cek peluangmu, bukan cuma popularitasnya"] }] },
      { bg: "yellow", kicker: "Intinya", title: "Cari info <a>dari sumber resmi.</a>", body: "Tanya sekolah, cek situs panitia seleksi, dan situs kampus incaranmu.", cta: true, hand: "tips belajar di" },
    ],
  },
  {
    id: "13", name: "irt-nilai-bukan-jumlah-benar",
    slides: [
      { bg: "soft", kicker: "Biar nggak kaget", title: "Kenapa nilai UTBK <a>bukan sekadar</a> jumlah benar?", note: "geser →" },
      { bg: "cream", kicker: "IRT itu apa", title: "Skor yang <a>memperhitungkan</a> tingkat kesulitan soal", body: "Setiap soal punya tingkat kesulitan. Soal yang sulit dan kamu jawab benar nilainya lebih berarti." },
      { bg: "soft", dense: true, kicker: "Contoh sederhana", title: "Benar sama banyak, <a>nilai bisa beda</a>", cmp: [{ h: "Siswa A", rows: [{ t: "Benar soal mudah", d: "bobot lebih kecil" }] }, { h: "Siswa B", rows: [{ t: "Benar soal sulit", d: "bobot lebih besar" }] }] },
      { bg: "cream", dense: true, kicker: "Jadi gimana belajarnya", title: "Latih <a>semua tingkat</a>", checks: ["Pastikan soal mudah nggak salah", "Biasakan soal bertingkat sulit", "Jangan habiskan waktu di satu soal"] },
      { bg: "yellow", kicker: "Mau coba?", title: "Latihan dengan <a>penilaian IRT</a>", body: "Kami siapkan tryout dengan timer nyata dan penilaian IRT.", tag: "Segera hadir", cta: true, hand: "pantau di" },
    ],
  },
  {
    id: "14", name: "peta-beasiswa",
    slides: [
      { bg: "navy", kicker: "Kuliah gratis itu ada", title: "Peta <a>beasiswa</a>, dari dalam sampai luar negeri", body: "Contoh jalur yang bisa kamu kenali sejak sekarang.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Dalam negeri", title: "Untuk <a>S1</a>", items: [{ e: "🎓", t: "KIP Kuliah", d: "Bantuan pemerintah, dilihat dari kondisi ekonomi" }, { e: "🏛️", t: "Beasiswa kampus", d: "Tiap kampus punya skemanya sendiri" }, { e: "🏢", t: "Perusahaan dan yayasan", d: "Contoh: Beasiswa Bakti BCA" }] },
      { bg: "soft", dense: true, kicker: "Luar negeri", title: "Untuk <a>S1</a>", items: [{ e: "🇯🇵", t: "MEXT (Jepang)", d: "S1 periode pendaftaran 2026: 1–19 April, studi mulai April 2027" }], src: "Sumber: Kedubes Jepang. Cek siklus berikutnya di situs resmi." },
      { bg: "cream", dense: true, kicker: "Pascasarjana", title: "Untuk <a>S2 dan S3</a>", items: [{ e: "🇮🇩", t: "LPDP", d: "Beasiswa pemerintah Indonesia" }, { e: "🇬🇧", t: "Chevening (Inggris)", d: "Siklus 2027/28 ditutup 6 Okt 2026" }, { e: "🌏", t: "GKS dan Australia Awards", d: "Pantau jadwal tiap tahun" }] },
      { bg: "soft", kicker: "Pola yang sama", title: "Hampir semua dibuka <a>setahun sekali.</a>", body: "Catat bulan buka tiap beasiswa, lalu hitung mundur persiapannya: dokumen, esai, dan skor bahasa.", note: "mulai dari sekarang~" },
      { bg: "yellow", kicker: "Satu hal pasti", title: "Bahasa Inggris <a>hampir selalu dibutuhkan.</a>", body: "Latihan dari sekarang supaya skormu siap saat pendaftaran dibuka.", cta: true, hand: "belajar bahasa Inggris di" },
    ],
  },
  {
    id: "15", name: "checklist-dokumen-beasiswa",
    slides: [{
      bg: "cream", dense: true, tight: true, kicker: "Siapkan dari sekarang", title: "Checklist <a>dokumen</a> beasiswa",
      checks: [{ t: "Rapor atau transkrip nilai" }, { t: "Surat rekomendasi", d: "Minta jauh-jauh hari ke guru atau dosen" }, { t: "Esai atau surat motivasi" }, { t: "Skor tes bahasa", d: "Kalau diminta" }, { t: "Identitas dan dokumen keluarga" }, { t: "Bukti prestasi dan organisasi" }],
      src: "Tiap beasiswa punya daftar sendiri. Selalu cek persyaratan resminya.", cta: true, hand: "tips beasiswa di",
    }],
  },
  {
    id: "16", name: "esai-motivasi-beasiswa",
    slides: [
      { bg: "yellow", kicker: "Bagian yang paling ditakuti", title: "Cara menulis esai <a>motivasi</a> beasiswa", body: "Struktur 5 paragraf yang gampang diikuti.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Kerangka", title: "5 paragraf, <a>satu cerita</a>", steps: [
        { w: "1", t: "Pembuka", d: "Cerita singkat yang menarik" },
        { w: "2", t: "Siapa kamu", d: "Pencapaian dan prosesnya" },
        { w: "3", t: "Kenapa program ini", d: "Alasan yang spesifik" },
        { w: "4", t: "Rencana setelah lulus", d: "Dampak untuk orang lain" },
        { w: "5", t: "Penutup", d: "Tegas dan singkat" },
      ] },
      { bg: "soft", dense: true, kicker: "Lakukan", title: "Bikin esai <a>yang diingat</a>", checks: ["Pakai contoh nyata, bukan klaim kosong", "Jujur dan pakai suaramu sendiri", "Minta dua orang membaca sebelum dikirim", "Patuhi batas kata"] },
      { bg: "cream", dense: true, kicker: "Hindari", title: "Yang bikin esai <a>biasa saja</a>", xs: true, checks: ["Kalimat klise tanpa cerita", "Menyalin contoh dari internet", "Terlalu banyak janji muluk"] },
      { bg: "yellow", kicker: "Simpan dulu", title: "Draf pertama <a>boleh jelek.</a>", body: "Yang penting ditulis. Memperbaikinya belakangan.", cta: true, hand: "tips beasiswa di" },
    ],
  },
  {
    id: "17", name: "wawancara-beasiswa",
    slides: [
      { bg: "soft", kicker: "Deg-degan?", title: "Persiapan <a>wawancara</a> beasiswa", body: "Pertanyaan yang sering muncul dan cara menjawabnya.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Sering ditanya", title: "5 pertanyaan <a>yang hampir pasti muncul</a>", items: [{ e: "1️⃣", t: "Ceritakan tentang dirimu" }, { e: "2️⃣", t: "Kenapa kamu layak dapat beasiswa ini?" }, { e: "3️⃣", t: "Apa rencanamu setelah lulus?" }, { e: "4️⃣", t: "Ceritakan kegagalan dan pelajarannya" }, { e: "5️⃣", t: "Kenapa memilih jurusan atau negara ini?" }] },
      { bg: "soft", dense: true, kicker: "Rumus jawaban", title: "Pakai cara <a>STAR</a>", steps: [
        { w: "S", t: "Situasi", d: "Apa konteksnya" },
        { w: "T", t: "Tugas", d: "Apa tanggung jawabmu" },
        { w: "A", t: "Aksi", d: "Apa yang kamu lakukan" },
        { w: "R", t: "Hasil", d: "Apa dampaknya" },
      ] },
      { bg: "cream", dense: true, kicker: "Latihan", title: "Biar nggak <a>blank</a>", checks: ["Rekam dirimu menjawab, lalu tonton ulang", "Latihan bareng teman", "Siapkan 3 cerita singkat tentang dirimu"] },
      { bg: "yellow", kicker: "Ingat", title: "Mereka cari <a>orang yang jujur</a>, bukan yang sempurna.", cta: true, hand: "teman belajarmu di" },
    ],
  },
  {
    id: "18", name: "ielts-vs-toefl-vs-itp",
    slides: [
      { bg: "navy", kicker: "Bingung pilih tes?", title: "IELTS, TOEFL iBT, atau <a>TOEFL ITP?</a>", body: "Ketiganya beda. Pilih sesuai yang diminta tujuanmu.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Dua tes internasional", title: "IELTS vs <a>TOEFL iBT</a>", cmp: [{ h: "IELTS", rows: ["Skor band 0–9", "Speaking dengan penguji", "Mengukur 4 keterampilan"] }, { h: "TOEFL iBT", rows: ["Skor baru 1–6", "Speaking dijawab ke komputer", "Mengukur 4 keterampilan"] }] },
      { bg: "soft", kicker: "Yang sering dipakai kampus", title: "<a>TOEFL ITP</a>", body: "Tes pilihan ganda berbasis kertas yang sering dipakai institusi untuk syarat kelulusan atau seleksi internal.", items: [{ e: "📄", t: "Isi", d: "Listening, Structure & Written Expression, Reading" }, { e: "🚫", t: "Tanpa", d: "Speaking dan Writing" }] },
      { bg: "cream", dense: true, kicker: "Cara memilih", title: "Ikuti <a>syarat tujuanmu</a>", checks: ["Cek jenis tes yang diterima kampus atau beasiswa", "Cek skor minimalnya", "Bandingkan jadwal dan biaya tes"] },
      { bg: "yellow", kicker: "Mau latihan?", title: "Mulai dari <a>kebiasaan</a> bahasa Inggrismu.", body: "Latihan harian dulu, baru tes simulasi.", tag: "Segera hadir: mock test", cta: true, hand: "belajar di" },
    ],
  },
  {
    id: "19", name: "tka-hari-terakhir-utama",
    slides: [{
      bg: "yellow", kicker: "8 November", title: "Hari terakhir <a>pelaksanaan utama</a> TKA.",
      body: "Apa pun hasilnya nanti, kamu sudah berani menjalaninya. Tarik napas, istirahat, kamu hebat.", note: "peluk dari kami~",
      src: "Hasil TKA dijadwalkan diumumkan 23 Desember 2026. Cek info resmi di sekolahmu.", cta: true, hand: "teman belajarmu di",
    }],
  },
  {
    id: "20", name: "5-kesalahan-speaking",
    slides: [
      { bg: "cream", kicker: "Speaking itu bisa dilatih", title: "5 kesalahan <a>speaking</a> bahasa Inggris", body: "Yang bikin kamu terdengar kurang yakin, padahal sudah bisa.", note: "geser →" },
      { bg: "soft", kicker: "Kesalahan 1", title: "Diam lama <a>cari kalimat sempurna</a>", body: "Jeda panjang bikin canggung.", items: [{ e: "✅", t: "Gantinya", d: "Mulai bicara dulu, perbaiki sambil jalan." }] },
      { bg: "cream", kicker: "Kesalahan 2", title: "Jawab <a>satu kata</a> doang", body: "“Yes.” “No.” Penguji ingin mendengar kemampuanmu.", items: [{ e: "✅", t: "Gantinya", d: "Jawaban + alasan + contoh singkat." }] },
      { bg: "soft", kicker: "Kesalahan 3", title: "<a>Menghafal</a> jawaban", body: "Terdengar kaku dan gampang ketahuan.", items: [{ e: "✅", t: "Gantinya", d: "Hafal kerangka, bukan kalimatnya." }] },
      { bg: "cream", kicker: "Kesalahan 4", title: "Takut salah <a>grammar</a>", body: "Kelancaran dan kejelasan sama pentingnya.", items: [{ e: "✅", t: "Gantinya", d: "Lanjut bicara, koreksi diri kalau sempat." }] },
      { bg: "yellow", kicker: "Cara melatih", title: "Biasakan <a>bicara tiap hari.</a>", body: "Di Kampung Bahasa Pare, chat di kampung Inggris wajib pakai bahasa Inggris. Auto kepake.", phone: "chat.webp", cta: true, hand: "latihan gratis di" },
    ],
  },
];
