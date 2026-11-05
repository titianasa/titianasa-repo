import type { Post } from "./types";

// Hari 1–10 (21–30 Okt 2026): TKA, jalur masuk PTN, TOEFL baru.
export const A: Post[] = [
  {
    id: "01", name: "jadwal-tka-sma-2026",
    slides: [
      { bg: "yellow", kicker: "TKA SMA/SMK/MA 2026", tag: "Update Okt 2026", title: "Jadwal <a>TKA</a> dari sekarang sampai hasil", body: "Simpan dulu. Geser buat lihat tanggal pentingnya.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Yang sudah lewat", title: "Tiga tahap ini <a>sudah selesai</a>", steps: [
        { w: "27 Jul–27 Sep", t: "Pendaftaran", d: "Didaftarkan lewat sekolah", done: true },
        { w: "21–27 Sep", t: "Simulasi", done: true },
        { w: "5–18 Okt", t: "Gladi bersih", done: true },
      ] },
      { bg: "soft", kicker: "Yang paling penting", title: "Ujiannya <a>dimulai</a> pekan ini", stats: [{ n: "26 Okt", l: "mulai pelaksanaan utama" }, { n: "8 Nov", l: "hari terakhir pelaksanaan utama" }], body: "Cek jadwal dan ruang ujianmu di sekolah, ya." },
      { bg: "cream", dense: true, kicker: "Yang akan datang", title: "Tiga tanggal <a>yang perlu diingat</a>", steps: [
        { w: "26 Okt–8 Nov", t: "Pelaksanaan utama", hot: true },
        { w: "16–29 Nov", t: "Ujian susulan", d: "Bagi yang berhak mengikuti susulan" },
        { w: "23 Des", t: "Pengumuman hasil", hot: true },
      ] },
      { bg: "yellow", kicker: "Biar nggak salah info", title: "Jadwal bisa <a>berubah.</a>", body: "Pegang tanggal dari sekolah dan pengumuman resmi Kemendikdasmen.", src: "Sumber: pemberitaan Kemendikdasmen/BBPMP, Okt 2026. Cek ulang di sekolahmu sebelum hari ujian.", cta: true, hand: "tips belajar tiap hari di" },
    ],
  },
  {
    id: "02", name: "5-kesalahan-belajar-jelang-ujian",
    slides: [
      { bg: "cream", kicker: "Jujur, pernah nggak?", title: "5 kesalahan belajar <a>jelang ujian</a>", body: "Dan gantinya yang lebih ampuh.", note: "geser →" },
      { bg: "soft", kicker: "Kesalahan 1", title: "Begadang <a>semalam suntuk</a>", body: "Otak yang kurang tidur susah mengingat dan gampang panik.", items: [{ e: "✅", t: "Gantinya", d: "Berhenti belajar lebih awal, tidur cukup." }] },
      { bg: "cream", kicker: "Kesalahan 2", title: "Baca ulang <a>catatan doang</a>", body: "Terasa paham, padahal cuma akrab dengan tulisannya.", items: [{ e: "✅", t: "Gantinya", d: "Tutup buku, coba jelaskan dari ingatan." }] },
      { bg: "soft", kicker: "Kesalahan 3", title: "Lompati yang <a>sulit</a>", body: "Topik yang dihindari biasanya yang paling banyak keluar salahnya.", items: [{ e: "✅", t: "Gantinya", d: "Mulai dari yang paling lemah, sedikit demi sedikit." }] },
      { bg: "cream", kicker: "Kesalahan 4", title: "Latihan soal <a>tanpa waktu</a>", body: "Di ruang ujian, waktu ikut menentukan.", items: [{ e: "✅", t: "Gantinya", d: "Pasang timer, latihan seperti ujian sungguhan." }] },
      { bg: "yellow", kicker: "Kesalahan 5", title: "Bandingin diri <a>sama orang lain</a>", body: "Yang penting kamu lebih baik dari dirimu kemarin.", note: "pelan-pelan nggak apa-apa~", cta: true },
    ],
  },
  {
    id: "03", name: "cara-bagi-waktu-ujian",
    slides: [{
      bg: "soft", dense: true, kicker: "Tips hari-H", title: "3 langkah <a>bagi waktu</a> saat ujian",
      checks: [{ t: "Kerjakan yang mudah dulu", d: "Nilai aman dulu, rasa percaya diri ikut naik." }, { t: "Tandai yang ragu, lanjut", d: "Jangan lama-lama di satu soal." }, { t: "Sisakan waktu untuk cek ulang", d: "Banyak salah kecil ketahuan di sini." }],
      note: "simpan buat nanti~", cta: true, hand: "tips belajar lain di",
    }],
  },
  {
    id: "04", name: "peta-jalur-masuk-ptn",
    slides: [
      { bg: "navy", kicker: "Mau kuliah di PTN?", title: "Peta <a>3 jalur</a> masuk PTN", body: "Ada yang pakai rapor, ada yang pakai tes. Kenali dulu sebelum memilih.", note: "geser →" },
      { bg: "cream", kicker: "Jalur 1", title: "<a>SNBP</a>", body: "Seleksi berdasarkan prestasi akademik, tanpa tes tulis. Tiap sekolah punya kuota peserta.", items: [{ e: "📈", t: "Yang dinilai", d: "Nilai rapor dan prestasi" }, { e: "🏫", t: "Syarat awal", d: "Masuk kuota sekolah (eligible)" }] },
      { bg: "soft", kicker: "Jalur 2", title: "<a>SNBT</a>", body: "Seleksi lewat tes UTBK. Nilai dihitung dengan IRT, jadi bukan sekadar jumlah benar.", items: [{ e: "📝", t: "Yang dinilai", d: "Hasil tes UTBK" }, { e: "🎯", t: "Siapa yang ikut", d: "Lulusan baru dan lulusan tahun-tahun sebelumnya" }] },
      { bg: "cream", kicker: "Jalur 3", title: "Seleksi <a>mandiri</a>", body: "Diadakan tiap kampus, jadi jadwal, biaya, dan caranya beda-beda.", items: [{ e: "🏛️", t: "Tips", d: "Buka situs kampus incaranmu, catat jadwalnya." }] },
      { bg: "soft", dense: true, kicker: "Beda cepat", title: "SNBP vs <a>SNBT</a>", cmp: [{ h: "SNBP", rows: ["Pakai rapor", "Tanpa tes tulis", "Ada kuota sekolah"] }, { h: "SNBT", rows: ["Pakai tes UTBK", "Nilai IRT", "Terbuka untuk banyak peserta"] }] },
      { bg: "yellow", kicker: "Catatan penting", title: "Aturan 2027 <a>belum final.</a>", body: "Jadwal dan syarat resmi akan diumumkan panitia SNPMB. Pantau terus.", src: "Cek di snpmb.id untuk ketentuan terbaru.", tag: "Segera hadir: latihan SNBT", cta: true, hand: "tips masuk PTN di" },
    ],
  },
  {
    id: "05", name: "tidur-cukup-sebelum-ujian",
    slides: [{
      bg: "navy", kicker: "Pengingat malam ini", title: "Otak yang <a>cukup tidur</a> lebih gampang mengingat.",
      body: "Sebelum ujian, kurangi begadang. Tidur itu bagian dari belajar.", note: "selamat istirahat~", cta: true, hand: "teman belajarmu di",
    }],
  },
  {
    id: "06", name: "checklist-hari-ujian-tka",
    slides: [
      { bg: "yellow", kicker: "TKA mulai hari ini", tag: "26 Okt", title: "Checklist <a>hari-H</a> ujian", body: "Tiga tahap: semalam, pagi hari, dan di ruang ujian.", note: "geser →" },
      { bg: "cream", dense: true, kicker: "Malam sebelumnya", title: "Siapkan <a>semuanya</a>", checks: ["Kartu peserta dan identitas, sesuai arahan sekolah", "Jadwal dan lokasi ujianmu", "Alat yang diizinkan saja", "Tidur lebih awal"] },
      { bg: "soft", dense: true, kicker: "Pagi hari", title: "Berangkat <a>tenang</a>", checks: ["Sarapan dulu", "Berangkat lebih awal dari perkiraan", "Cek ulang bawaan sebelum keluar rumah"] },
      { bg: "cream", dense: true, kicker: "Di ruang ujian", title: "Fokus ke <a>soal</a>", checks: ["Baca instruksi dengan teliti", "Ada kendala teknis? Angkat tangan, lapor pengawas", "Tarik napas dalam kalau mulai panik"] },
      { bg: "soft", dense: true, kicker: "Sebaiknya jangan", title: "Hal yang <a>bikin rugi</a>", xs: true, checks: ["Belajar materi baru semalaman", "Lupa sarapan", "Bandingkan jawaban saat jeda", "Panik karena satu soal sulit"] },
      { bg: "yellow", kicker: "Semangat!", title: "Kamu sudah <a>sejauh ini.</a>", body: "Tinggal dijalani satu soal demi satu soal.", cta: true, hand: "tips belajar tiap hari di" },
    ],
  },
  {
    id: "07", name: "deg-degan-sebelum-ujian",
    slides: [
      { bg: "soft", kicker: "Deg-degan itu wajar", title: "4 trik <a>menenangkan diri</a> sebelum ujian", body: "Bisa dilakukan di tempat duduk, dua menit saja.", note: "geser →" },
      { bg: "cream", kicker: "Trik 1", title: "Napas <a>4-4-4</a>", body: "Tarik napas 4 hitungan, tahan 4, hembuskan 4. Ulang beberapa kali.", items: [{ e: "🌬️", t: "Kenapa membantu", d: "Napas pelan memberi sinyal tenang ke tubuh." }] },
      { bg: "soft", kicker: "Trik 2", title: "Tulis <a>kekhawatiranmu</a>", body: "Tulis apa yang kamu takutkan di kertas kecil. Pikiran terasa lebih ringan setelah keluar dari kepala.", items: [{ e: "📝", t: "Cukup satu menit", d: "Nggak perlu rapi." }] },
      { bg: "cream", kicker: "Trik 3", title: "Gerak <a>sebentar</a>", body: "Regangkan bahu, jalan kecil, kepal-lepas tangan. Badan rileks, pikiran ikut.", items: [{ e: "🚶", t: "Dua menit saja" }] },
      { bg: "yellow", kicker: "Trik 4", title: "Bilang ke diri: <a>aku sudah siap.</a>", body: "Kamu sudah belajar. Sekarang tinggal menunjukkan yang kamu tahu.", cta: true, hand: "teman belajarmu di" },
    ],
  },
  {
    id: "08", name: "sumpah-pemuda-bahasa",
    slides: [{
      bg: "navy", kicker: "Hari Sumpah Pemuda", title: "Satu bahasa <a>menyatukan.</a> Banyak bahasa <a>membuka pintu.</a>",
      body: "Bangga berbahasa Indonesia, dan terus belajar bahasa lain supaya jembatanmu makin panjang.", note: "selamat Hari Sumpah Pemuda!", cta: true, hand: "belajar bahasa di Kampung Bahasa Pare",
    }],
  },
  {
    id: "09", name: "toefl-ibt-baru-2026",
    slides: [
      { bg: "yellow", kicker: "Mau kuliah atau kerja di luar negeri?", title: "TOEFL iBT <a>berubah</a> sejak Januari 2026", body: "Skor baru, format baru. Ini ringkasannya.", note: "geser →" },
      { bg: "cream", kicker: "Yang berubah", title: "Skalanya jadi <a>1 sampai 6</a>", stats: [{ n: "1–6", l: "skala skor, kelipatan 0,5" }, { n: "4", l: "bagian tes" }, { n: "±2 jam", l: "perkiraan lama tes" }], src: "Berlaku sejak 21 Januari 2026. Sumber: ets.org." },
      { bg: "soft", dense: true, kicker: "Cara hitung skor", title: "Skor total = <a>rata-rata</a> 4 bagian", body: "Hasilnya dibulatkan ke 0,5 terdekat.", items: [{ e: "🔢", t: "Masa transisi", d: "Selama 2 tahun, laporan skor juga memuat skor setara skala 0–120." }] },
      { bg: "cream", dense: true, kicker: "Isi tesnya", title: "Tugas di tiap <a>bagian</a>", cmp: [{ h: "Reading & Listening", rows: ["Complete the Words", "Read in Daily Life", "Listen and Choose a Response", "Academic Talk"] }, { h: "Writing & Speaking", rows: ["Build a Sentence", "Write an Email", "Listen and Repeat", "Take an Interview"] }] },
      { bg: "soft", kicker: "Info praktis", title: "Hasil cepat, <a>berlaku 2 tahun</a>", items: [{ e: "📬", t: "Skor keluar", d: "3 hari setelah tanggal tes" }, { e: "⏳", t: "Masa berlaku", d: "2 tahun dari tanggal tes" }] },
      { bg: "yellow", kicker: "Sebelum daftar", title: "<a>Cek syarat</a> kampus dan beasiswamu", body: "Pastikan mereka menerima skala skor yang baru.", tag: "Segera hadir: mock test", cta: true, hand: "latihan bahasa Inggris di" },
    ],
  },
  {
    id: "10", name: "15-menit-bahasa-inggris",
    slides: [{
      bg: "yellow", kicker: "Bingung mulai dari mana?", tag: "Gratis!", title: "Cukup <a>15 menit</a> sehari, tapi rutin.",
      body: "Belajar sedikit tiap hari lebih awet daripada maraton semalam. Mulai dari satu kata di Kampung Bahasa Pare.", phone: "london.webp", cta: true,
    }],
  },
];
