// The 30 posts of November 2026 for @pare.titianasa (one a day, 1–30 Nov). Rendered by build.ts and render.ts.
// Sources: lessons game/src/game/content/en/, levels data/pare/content.json (ladder), missions data/pare/missions.json,
// test facts from ets.org, ielts.org and pearsonpte.com (checked 20 Oct 2026). See ../kalender-dan-caption.md.
import type { Post } from "./build.ts";

const RESMI = "Sumber: situs resmi penyelenggara, dicek Oktober 2026. Cek lagi sebelum daftar.";

export const POSTS: Post[] = [
  // ---------------------------------------------------------------- week 1
  {
    id: "01", name: "kampung-bahasa-sekarang-3d",
    slides: [{
      bg: "navy", kicker: "Kabar baru", tag: "Baru!",
      title: "Kampung Bahasa sekarang <a>3D.</a>",
      body: "Lapangan senja, Kampung Inggris, odong-odong, dan teman belajar yang lalu-lalang. Jalur belajar bahasa Inggrisnya tetap: <b>Basic sampai C2</b>.",
      phone: "3d-lapangan.webp", cta: true,
    }],
  },
  {
    id: "02", name: "tur-kampung-bahasa-3d",
    slides: [
      { bg: "navy", kicker: "Tur singkat", title: "Jalan-jalan dulu, yuk. <a>Versi 3D.</a>", small: true, body: "Ini sudut-sudut Kampung Bahasa yang bisa kamu datangi.", phone: "3d-lapangan.webp", note: "geser →" },
      { bg: "cream", kicker: "Kampung Inggris", title: "Semua warganya <a>ngomong Inggris</a>", small: true, body: "Ada English Class Academy, perpustakaan, kafe Tom, diner Chef Oliver, laundry, sampai kantor pos.", phone: "3d-kampung-inggris.webp" },
      { bg: "soft", kicker: "Keliling", title: "Gowes pakai <a>sepeda ontel</a>", small: true, body: "Sewa sepeda, lalu keliling jalan Kampung Bahasa.", phone: "3d-sepeda.webp" },
      { bg: "cream", kicker: "Keliling", title: "Atau naik <a><span class='nb'>odong-odong</span></a>", small: true, body: "Kereta kelinci keliling Kampung Bahasa, duduk bareng warga lain. Turun di halte mana saja.", phone: "3d-odong.webp" },
      { bg: "soft", kicker: "Laper?", title: "Jajan ke <a>pakde dan budhe</a>", small: true, body: "Pecel Bu Sri, bakso Cak Mat, es degan Mbak Lis. Makan dulu biar staminamu penuh lagi.", phone: "3d-jajan.webp" },
      { bg: "yellow", kicker: "Tapi ingat", title: "Belajarnya tetap <a>serius.</a>", body: "Tiap sudut punya bahasa Inggrisnya sendiri. Buka di browser, langsung mulai.", cta: true },
    ],
  },
  {
    id: "03", name: "level-basic",
    slides: [
      { bg: "soft", kicker: "Seri level · 1 dari 7", title: "Level Basic: <a>mulai dari nol</a>", small: true, body: "Setara Pra-A1. Buat kamu yang baru kenal bahasa Inggris, atau yang mau mengulang dari awal.", phone: "jalur.webp", note: "geser →" },
      { bg: "cream", kicker: "Yang dipelajari", title: "6 bab <a>pertama</a>", items: [
        { e: "🔤", t: "Huruf & bunyi" }, { e: "👋", t: "Sapaan & perkenalan" }, { e: "🔢", t: "Angka 1–10" },
        { e: "🍜", t: "Makanan & minuman" }, { e: "⏰", t: "Rutinitas harian" }, { e: "🧭", t: "Perjalanan & arah" },
      ] },
      { bg: "soft", kicker: "Habis Basic, kamu bisa", title: "Langsung <a>kepakai</a>", items: [
        { e: "🙋", t: "Menyapa dan memperkenalkan diri" },
        { e: "🍽️", t: "Memesan makanan sederhana" },
        { e: "🗺️", t: "Menanyakan arah dasar" },
      ] },
      { bg: "cream", kicker: "Kata pertama yang wajib", title: "Kata <a>sakti</a>", big: "Excuse me.", sub: "iks-KYUZ mi<i>Permisi.</i>" },
      { bg: "yellow", kicker: "Berikutnya", title: "Habis Basic, <a>lanjut A1.</a>", body: "Tiap level punya bab, latihan, dan misinya sendiri. Sudah bisa? Ikut ujian lompat level.", cta: true },
    ],
  },
  {
    id: "04", name: "toefl-ielts-pte-toeic-bedanya",
    slides: [
      { bg: "cream", kicker: "Infografik", title: "TOEFL, IELTS, PTE, TOEIC: <a>bedanya apa?</a>", small: true, body: "Sama-sama tes bahasa Inggris. Bentuk, skor, dan tujuannya beda.", note: "geser →" },
      { bg: "soft", kicker: "Sekilas", title: "Skor & <a>lamanya</a>", small: true, table: { head: ["Tes", "Skor", "Lama"], rows: [
        ["TOEFL iBT", "1–6", "±2 jam"], ["TOEFL ITP", "310–677", "115 menit"], ["IELTS", "band 0–9", "2 jam 45 menit"],
        ["PTE Academic", "10–90", "±2 jam"], ["TOEIC L&R", "10–990", "2 jam"],
      ] }, src: RESMI },
      { bg: "cream", kicker: "Yang diuji", title: "Bagian <a>tesnya</a>", small: true, table: { head: ["Tes", "Bagian"], rows: [
        ["TOEFL iBT", "Reading, Listening, Writing, Speaking"], ["TOEFL ITP", "Listening, Structure, Reading"],
        ["IELTS", "Listening, Reading, Writing, Speaking"], ["PTE Academic", "Speaking & Writing, Reading, Listening"],
        ["TOEIC L&R", "Listening, Reading"],
      ] }, src: RESMI },
      { bg: "soft", kicker: "Pilih sesuai tujuan", title: "Biasanya <a>dipakai untuk</a>", small: true, items: [
        { e: "🎓", t: "Kuliah & beasiswa luar negeri", d: "IELTS, TOEFL iBT, PTE Academic" },
        { e: "🏫", t: "Kampus & instansi dalam negeri", d: "TOEFL ITP sering diminta" },
        { e: "💼", t: "Dunia kerja", d: "TOEIC, soalnya seputar kantor" },
      ], note: "syaratnya beda-beda, cek tujuanmu~" },
      { bg: "cream", kicker: "Jujur aja", title: "Satu fondasi, <a>semua tes</a>", small: true, body: "Kampung Bahasa bukan kelas persiapan tes. Tapi isinya sama dengan yang diuji: <b>tata bahasa, kosakata, membaca, mendengar, menulis</b>. Itu yang kamu bangun dari Basic sampai C2." },
      { bg: "yellow", kicker: "Format bisa berubah", title: "Cek lagi <a>sebelum daftar</a>", small: true, body: "Situs resminya: ets.org (TOEFL, TOEIC), ielts.org, pearsonpte.com.", cta: true },
    ],
  },
  {
    id: "05", name: "misi-minggu-pertama",
    slides: [
      { bg: "navy", kicker: "Misi level Basic", title: "Minggu pertamamu di <a>Kampung Inggris</a>", small: true, body: "Kalimat yang baru dipelajari langsung dipakai bareng warga.", phone: "3d-kampung-inggris.webp", note: "geser →" },
      { bg: "cream", kicker: "Misi", title: "Kenalan dengan <a>tetangga</a>", small: true, body: "Miss Kate memberimu tiga kartu nama kosong. Kenali tiga warga dan isi kartu mereka.", phone: "misi-susun.webp" },
      { bg: "soft", kicker: "Misi", title: "Belanja <a>pertama</a>", body: "Beli satu camilan di toko dengan uang saku sendiri. Tanyakan harganya, lalu dengarkan jawabannya." },
      { bg: "cream", kicker: "Misi", title: "Makan siang <a>pertama</a>", small: true, body: "Pesan minuman di kafe dalam bahasa Inggris, lalu makan di warung." },
      { bg: "soft", kicker: "Misi", title: "Turis <a>tersesat</a>", body: "Anna, seorang turis, kebingungan. Antar dia ke kafe, lalu ke taman, dan bantu dia dengan bahasa Inggris." },
      { bg: "yellow", kicker: "Misi besar", title: "Penutupnya: <a>pesta sambutan</a>", small: true, body: "Miss Kate melepasmu sehari penuh tanpa bantuan. Sorenya, warga mengadakan pesta sambutan di taman.", cta: true },
    ],
  },
  {
    id: "06", name: "salah-kaprah-a1",
    slides: [
      { bg: "soft", kicker: "Level A1", title: "5 kesalahan yang <a>sering banget</a>", small: true, body: "Kamu pernah nulis yang mana?", note: "geser →" },
      { bg: "cream", kicker: "Salah 1", title: "Bukan have, <a>tapi has</a>", big: "She has a bike.", sub: "<b>✗ She have a bike.</b><i>he, she, it memakai has.</i>" },
      { bg: "soft", kicker: "Salah 2", title: "Habis like, <a>pakai -ing</a>", big: "I like swimming.", sub: "<b>✗ I like swim.</b><i>Setelah like, kegiatan memakai -ing.</i>" },
      { bg: "cream", kicker: "Salah 3", title: "Tanya umur, <a>are di depan</a>", small: true, big: "How old are you?", sub: "<b>✗ How old you are?</b><i>Dalam pertanyaan, are sebelum subjek.</i>" },
      { bg: "soft", kicker: "Salah 4", title: "Let's tanpa <a>to</a>", big: "Let's go!", sub: "<b>✗ Let's to go!</b><i>Setelah Let's langsung kata kerja dasar.</i>" },
      { bg: "cream", kicker: "Salah 5", title: "Air nggak bisa <a>dihitung</a>", small: true, big: "I want some water.", sub: "<b>✗ I want a water.</b><i>water tidak bisa dihitung, jadi tanpa a.</i>" },
      { bg: "yellow", kicker: "Biar nempel", title: "Latihan sampai <a>terbiasa</a>", small: true, body: "Tiap konsep di Kampung Bahasa ada contohnya, kalimat untuk disusun, dan soal isian.", cta: true },
    ],
  },
  {
    id: "07", name: "pilih-karakter-di-lemari",
    slides: [
      { bg: "soft", kicker: "Lemari", title: "Pilih karakter yang <a>sesuai denganmu</a>", small: true, body: "Ada karakter siap pakai, putra dan putri. Pilih satu, lalu ubah sesukamu.", phone: "3d-lemari.webp", note: "geser →" },
      { bg: "cream", kicker: "Bisa diatur", title: "Dari rambut <a>sampai tas</a>", small: true, items: [
        { e: "🧍", t: "Tubuh & rambut" }, { e: "🧕", t: "Penutup kepala" },
        { e: "👕", t: "Atasan, terusan, bawahan" }, { e: "🎒", t: "Alas kaki, tas, aksesori" },
      ], note: "coba apa saja gratis~" },
      { bg: "soft", kicker: "Gaya lokal", title: "Tampil kayak <a>anak Pare</a>", small: true, body: "Batik, peci, jilbab, seragam sekolah, pramuka, sampai tas ransel.", phone: "3d-lemari-2.webp" },
      { bg: "yellow", kicker: "Biar dikenali", title: "Teman belajar <a>kenal kamu</a>", small: true, body: "Karaktermu tampil di Kampung Bahasa, lengkap dengan nama dan levelmu.", cta: true },
    ],
  },
  // ---------------------------------------------------------------- week 2
  {
    id: "08", name: "tebak-a-atau-some",
    slides: [
      { bg: "yellow", kicker: "Tebak, yuk", title: "I want ___ water. <a>Isi apa?</a>", small: true, items: [{ e: "A", t: "a" }, { e: "B", t: "an" }, { e: "C", t: "some" }], note: "jawab di komentar, lalu geser →" },
      { bg: "cream", kicker: "Jawabannya", title: "<a>some</a> water", big: "I want some water.", sub: "ai wont sam WO-ta<i>Saya mau air.</i>", body: "water tidak bisa dihitung, jadi tidak memakai a atau an.", cta: true },
    ],
  },
  {
    id: "09", name: "level-a1",
    slides: [
      { bg: "soft", kicker: "Seri level · 2 dari 7", title: "Level A1: <a>cerita sehari-hari</a>", small: true, body: "Keluarga, rumah, sekolah, kerja, kota. Mulai pakai kalimat utuh.", note: "geser →" },
      { bg: "cream", kicker: "Yang dipelajari", title: "Topik <a>A1</a>", items: [
        { e: "👨‍👩‍👧", t: "Keluarga & pekerjaan" }, { e: "🗓️", t: "Waktu, hari & angka sampai 100" }, { e: "🏠", t: "Rumah & tempat di kota" },
        { e: "🌦️", t: "Makanan, warna, pakaian & cuaca" }, { e: "🧩", t: "Present simple & continuous, can, there is/are, was/were" },
      ] },
      { bg: "soft", kicker: "Habis A1, kamu bisa", title: "Makin <a>pede</a>", items: [
        { e: "🗣️", t: "Menceritakan keluarga dan rutinitas" }, { e: "📅", t: "Membuat janji bertemu" },
        { e: "💰", t: "Bertanya jam, harga, dan arah" }, { e: "📖", t: "Membaca pesan dan menu sederhana" },
      ] },
      { bg: "cream", kicker: "Contoh kalimat A1", title: "Cerita <a>kebiasaan</a>", big: "I always get up at six.", sub: "ai OL-weiz get ap et siks<i>Saya selalu bangun jam enam.</i>" },
      { bg: "yellow", kicker: "Berikutnya", title: "Lanjut <a>A2</a>", body: "Atau langsung ikut ujian lompat level kalau sudah merasa bisa.", cta: true },
    ],
  },
  {
    id: "10", name: "toefl-ibt-format-baru",
    slides: [
      { bg: "navy", kicker: "Infografik", title: "TOEFL iBT <a>format baru</a>", small: true, body: "Sejak Januari 2026, skornya pakai skala <b>1 sampai 6</b>, bukan 0–120 lagi.", note: "geser →" },
      { bg: "cream", kicker: "4 bagian", title: "Isi <a>tesnya</a>", small: true, table: { head: ["Bagian", "Soal", "Waktu"], rows: [
        ["Reading", "50", "±30 menit"], ["Listening", "47", "±29 menit"], ["Writing", "12", "±23 menit"], ["Speaking", "11", "±8 menit"],
      ] }, note: "sediakan sekitar 2 jam", src: RESMI },
      { bg: "soft", kicker: "Cara menilai", title: "Skornya <a>sekarang</a>", small: true, items: [
        { e: "🔢", t: "Tiap bagian dapat skor 1–6" },
        { e: "➗", t: "Skor total = rata-rata empat bagian", d: "Dibulatkan ke setengah poin terdekat." },
        { e: "🔁", t: "Masa transisi dua tahun", d: "Kamu juga dapat skor setara skala lama 0–120." },
      ] },
      { bg: "cream", kicker: "Yang perlu tahu", title: "Soalnya <a>menyesuaikan</a>", small: true, body: "Tesnya menyesuaikan kemampuanmu. Karena itu waktu dan jumlah soal bisa sedikit berbeda antarpeserta." },
      { bg: "yellow", kicker: "Mulai dari mana?", title: "Bangun <a>fondasinya</a> dulu", small: true, body: "Membaca, mendengar, menulis, dan dipakai ngobrol. Di Kampung Bahasa, semuanya dilatih dari Basic.", cta: true },
    ],
  },
  {
    id: "11", name: "misi-a1-keluarga-brown",
    slides: [
      { bg: "navy", kicker: "Misi level A1", title: "Tinggal bareng <a>keluarga Brown</a>", small: true, body: "Di A1 kamu pindah ke rumah keluarga Brown, di sebelah Diner Kampung Inggris.", phone: "3d-kampung-inggris.webp", note: "geser →" },
      { bg: "cream", kicker: "Misi", title: "Pohon keluarga <a>Brown</a>", small: true, body: "Mrs. Brown memintamu mengenal semua anggota keluarganya. Siapa kakak, siapa adik?" },
      { bg: "soft", kicker: "Misi", title: "Pelayan <a>sehari</a>", body: "Pelayan diner sakit. Chef Oliver memintamu makan dulu sebagai pelanggan, lalu gantian jadi pelayan." },
      { bg: "cream", kicker: "Misi", title: "Baju untuk <a>pesta</a>", body: "Jack bingung mau pakai apa ke pesta Emma. Pilihkan pakaiannya, lalu deskripsikan pakaian orang lain." },
      { bg: "soft", kicker: "Misi", title: "Tas Emma <a>hilang</a>", body: "Officer Jones memintamu menanyai warga dan menyusun urutan kejadian kemarin sore." },
      { bg: "yellow", kicker: "Misi besar A1", title: "Kamu jadi <a>panitia pesta</a>", small: true, body: "Pesta tahunan Kampung Inggris: kamu yang merencanakan, menyiapkan, lalu jadi tuan rumah.", cta: true },
    ],
  },
  {
    id: "12", name: "salah-kaprah-a2",
    slides: [
      { bg: "soft", kicker: "Level A2", title: "5 kesalahan yang <a>bikin kebalik</a>", small: true, body: "Sering lolos di chat, tapi bikin artinya beda.", note: "geser →" },
      { bg: "cream", kicker: "Salah 1", title: "yet pakai <a>present perfect</a>", small: true, big: "I haven't finished yet.", sub: "<b>✗ I didn't finish yet.</b><i>yet dipakai dengan present perfect.</i>" },
      { bg: "soft", kicker: "Salah 2", title: "Setelah if, <a>tanpa will</a>", small: true, big: "If it rains, I'll stay home.", sub: "<b>✗ If it will rain, I'll stay home.</b><i>Setelah if memakai present simple.</i>" },
      { bg: "cream", kicker: "Salah 3", title: "Tujuan pakai <a>to</a>", big: "I came here to learn English.", sub: "<b>✗ I came here for learn English.</b><i>Tujuan dengan kata kerja: to + kata kerja.</i>" },
      { bg: "soft", kicker: "Salah 4", title: "enjoy <a>+ -ing</a>", big: "I enjoy cooking.", sub: "<b>✗ I enjoy to cook.</b><i>enjoy diikuti -ing.</i>" },
      { bg: "cream", kicker: "Salah 5", title: "Dilarang ≠ <a>tidak perlu</a>", small: true, big: "You don't have to come.", sub: "<b>✗ You mustn't come (kalau maksudnya boleh tidak datang).</b><i>mustn't = dilarang; tidak perlu = don't have to.</i>" },
      { bg: "yellow", kicker: "Biar nempel", title: "Salah dulu, <a>baru bisa</a>", small: true, body: "Yang salah muncul lagi di latihan sampai kamu paham.", cta: true },
    ],
  },
  {
    id: "13", name: "kalimat-kerja-paruh-waktu",
    slides: [
      { bg: "navy", kicker: "Buat pejuang WHV", title: "5 kalimat buat <a>kerja paruh waktu</a>", small: true, body: "Semuanya dari level A2, tempat kamu kerja paruh waktu di toko pakaian Mal Kota.", note: "geser →" },
      { bg: "cream", kicker: "Minta tolong rekan kerja", title: "Bisa <a>bantu?</a>", big: "Could you do me a favour?", sub: "kud yu du mi e FEI-ver<i>Bisa minta tolong?</i>" },
      { bg: "soft", kicker: "Pelanggan harus antre", title: "Minta <a>menunggu</a>", big: "Would you mind waiting?", sub: "wud yu maind WEI-ting<i>Keberatan menunggu?</i>" },
      { bg: "cream", kicker: "Belum tahu jawabannya", title: "Jangan <a>panik</a>", big: "Let me check.", sub: "let mi cek<i>Saya cek dulu.</i>" },
      { bg: "soft", kicker: "Ditanya berapa lama", title: "Kasih <a>perkiraan</a>", big: "It takes about twenty minutes.", sub: "it teiks e-BAUT TWEN-ti MI-nits<i>Kira-kira dua puluh menit.</i>" },
      { bg: "cream", kicker: "Kalau pelanggan bilang ini", title: "Rezeki <a>kasir</a>", big: "Keep the change.", sub: "kip dhe ceinj<i>Ambil saja kembaliannya.</i>" },
      { bg: "yellow", kicker: "Misi A2", title: "Hari pertama <a>kerja</a>", small: true, body: "Melamar ke Mbak Lala, belajar peraturan toko, lalu jaga kasir di Sabtu yang ramai.", cta: true },
    ],
  },
  {
    id: "14", name: "ngobrol-langsung-dengan-warga",
    slides: [
      { bg: "navy", kicker: "Fitur baru", tag: "Baru!", title: "Ngobrol langsung <a>dengan warga</a>", small: true, body: "Ketuk warga di dekatmu, tulis dalam bahasa Inggris, dan dia membalas di atas kepalanya.", phone: "3d-ngobrol-warga.webp", note: "geser →" },
      { bg: "cream", kicker: "Caranya", title: "Semudah <a>nyapa</a>", items: [
        { e: "🚶", t: "Dekati warga", d: "Mr. Smith, Tom, Chef Oliver, Mrs. Hughes, dan lainnya." },
        { e: "👆", t: "Ketuk, kotak chat muncul" },
        { e: "⌨️", t: "Tulis dalam bahasa Inggris" },
        { e: "💬", t: "Balasannya muncul, lengkap dengan arti" },
      ] },
      { bg: "soft", kicker: "Sesuai levelmu", title: "Nggak bikin <a>pusing</a>", small: true, body: "Warga membalas pendek, pakai kata sesuai levelmu, dan sering balik bertanya supaya obrolan jalan terus. Jawabannya dibantu AI." },
      { bg: "cream", kicker: "Nggak hilang", title: "Tercatat di <a>ruang chat</a>", small: true, body: "Obrolanmu dengan tiap warga tersimpan di daftar chat. Lanjutkan kapan saja, di HP atau laptop." },
      { bg: "yellow", kicker: "Latihan speaking versi ketik", title: "Ngobrol <a>tanpa malu</a>", small: true, body: "Salah tulis? Warga tetap menjawab, dan memakai bentuk yang benar di balasannya.", cta: true },
    ],
  },
  // ---------------------------------------------------------------- week 3
  {
    id: "15", name: "peta-kampung-inggris",
    slides: [
      { bg: "soft", kicker: "Biar nggak nyasar", title: "Peta <a>Kampung Inggris</a>", small: true, body: "Buka peta, ketuk tempatnya, lalu ikuti tandanya.", phone: "3d-peta.webp", note: "geser →" },
      { bg: "cream", kicker: "Siapa di mana · 1", title: "Tempat <a>belajar</a>", items: [
        { e: "🏫", t: "English Class Academy", d: "Miss Kate, gurumu" }, { e: "📚", t: "Library", d: "Mr. Smith, pustakawan" },
        { e: "🏨", t: "Guesthouse", d: "Mrs. Hughes" }, { e: "✉️", t: "Post Office", d: "Mr. Patel" },
      ] },
      { bg: "soft", kicker: "Siapa di mana · 2", title: "Tempat <a>nongkrong</a>", items: [
        { e: "☕", t: "Café", d: "Tom, barista" }, { e: "🍳", t: "Diner", d: "Chef Oliver" },
        { e: "🛒", t: "Minimart", d: "Mrs. Brown" }, { e: "🧺", t: "Laundry", d: "Mr. Green" },
      ] },
      { bg: "yellow", kicker: "Tiap warga punya misi", title: "Sapa <a>semuanya</a>", small: true, body: "Hampir tiap warga Kampung Inggris punya misi sampingan sendiri.", cta: true },
    ],
  },
  {
    id: "16", name: "level-a2",
    slides: [
      { bg: "soft", kicker: "Seri level · 3 dari 7", title: "Level A2: <a>keluar dari zona nyaman</a>", small: true, body: "Belanja, ke dokter, kerja, liburan. Bahasa Inggris untuk urusan beneran.", note: "geser →" },
      { bg: "cream", kicker: "Yang dipelajari", title: "Topik <a>A2</a>", items: [
        { e: "🛍️", t: "Belanja & uang" }, { e: "🩺", t: "Kesehatan" }, { e: "💼", t: "Pekerjaan" }, { e: "✈️", t: "Perjalanan & liburan" },
        { e: "🧩", t: "Past simple & continuous, present perfect, going to/will, have to/should" },
      ] },
      { bg: "soft", kicker: "Habis A2, kamu bisa", title: "Urus <a>sendiri</a>", items: [
        { e: "🏷️", t: "Berbelanja dan menawar" }, { e: "🤒", t: "Menjelaskan keluhan ke dokter" },
        { e: "🧳", t: "Menceritakan pengalaman dan rencana" }, { e: "📧", t: "Membaca email dan pengumuman pendek" },
      ] },
      { bg: "cream", kicker: "Contoh kalimat A2", title: "Cerita <a>rencana</a>", big: "I'm flying to Jakarta on Friday.", sub: "aim FLAI-ing tu je-KAR-ta on FRAI-dei<i>Saya terbang ke Jakarta hari Jumat.</i>" },
      { bg: "yellow", kicker: "Ada tulisannya juga", title: "Nulis email, <a>dinilai AI</a>", small: true, body: "Di A2 kamu mulai menulis email dan cerita pendek, lalu dapat masukan dari penilai AI.", cta: true },
    ],
  },
  {
    id: "17", name: "ielts-sekilas",
    slides: [
      { bg: "navy", kicker: "Infografik", title: "IELTS <a>sekilas</a>", body: "Empat bagian, satu skor band. Ini yang perlu kamu tahu.", note: "geser →" },
      { bg: "cream", kicker: "4 bagian · 2 jam 45 menit", title: "Isi <a>tesnya</a>", small: true, table: { head: ["Bagian", "Waktu", "Catatan"], rows: [
        ["Listening", "±30 menit", "40 soal"], ["Reading", "60 menit", "40 soal"], ["Writing", "60 menit", "2 tugas"], ["Speaking", "11–14 menit", "tatap muka dengan penguji"],
      ] }, src: RESMI },
      { bg: "soft", kicker: "Dua jenis", title: "Academic atau <a>General Training?</a>", small: true, items: [
        { e: "🎓", t: "Academic", d: "Untuk kuliah dan pendaftaran profesi." },
        { e: "🧳", t: "General Training", d: "Untuk kerja, pelatihan, atau migrasi." },
      ], note: "listening & speaking-nya sama" },
      { bg: "cream", kicker: "Cara menilai", title: "Skor <a>band</a>", small: true, items: [
        { e: "🔢", t: "Tiap bagian: band 0–9", d: "Bisa setengah band, misalnya 6,5." },
        { e: "➗", t: "Overall = rata-rata empat bagian", d: "Dibulatkan ke setengah band terdekat." },
      ] },
      { bg: "yellow", kicker: "Mulai dari mana?", title: "Writing butuh <a>tata bahasa</a>", small: true, body: "Esai yang bagus berdiri di atas kalimat yang benar. Itu yang kamu latih bab demi bab, dari A1 sampai C1.", cta: true },
    ],
  },
  {
    id: "18", name: "misi-a2-gaji-pertama",
    slides: [
      { bg: "navy", kicker: "Misi level A2", title: "Ke Kota, kerja, lalu <a>liburan</a>", small: true, body: "Di A2 kamu keluar dari Kampung Inggris dan mengurus semuanya sendiri.", note: "geser →" },
      { bg: "cream", kicker: "Misi", title: "Saksi <a>mata</a>", body: "Gerobak buah terguling di depan Mal Kota. Pak Satpam memintamu menanyai tiga saksi." },
      { bg: "soft", kicker: "Misi", title: "Hadiah dengan <a>anggaran</a>", small: true, body: "Mrs. Brown berulang tahun. Emma dan Jack menitipkan Rp100.000 untuk memilih hadiah di Mal Kota." },
      { bg: "cream", kicker: "Misi", title: "Di <a>klinik</a>", body: "Kamu kurang enak badan. Dokter Rina di Rumah Sakit Kota memeriksamu. Jelaskan keluhanmu." },
      { bg: "soft", kicker: "Misi", title: "Liburan yang <a>kacau</a>", body: "Kereta dibatalkan, kamar hotel belum siap, cuaca berubah. Selesaikan semuanya dalam bahasa Inggris." },
      { bg: "yellow", kicker: "Misi besar A2", title: "Gaji pertama, <a>liburan pertama</a>", small: true, body: "Pakai gaji pertamamu untuk mengajak keluarga Brown berlibur ke Kota. Kamu yang mengatur semuanya.", cta: true },
    ],
  },
  {
    id: "19", name: "salah-kaprah-b1",
    slides: [
      { bg: "soft", kicker: "Level B1", title: "5 kesalahan <a>level menengah</a>", small: true, body: "Sudah lancar ngobrol? Coba cek, masih ada yang ini?", note: "geser →" },
      { bg: "cream", kicker: "Salah 1", title: "yesterday pakai <a>past</a>", small: true, big: "I saw him yesterday.", sub: "<b>✗ I have seen him yesterday.</b><i>Waktu lampau yang jelas memakai Simple Past.</i>" },
      { bg: "soft", kicker: "Salah 2", title: "Setelah if, <a>tanpa would</a>", small: true, big: "If I had money, I would buy a car.", sub: "<b>✗ If I would have money, …</b><i>Setelah if memakai Simple Past.</i>" },
      { bg: "cream", kicker: "Salah 3", title: "said atau <a>told?</a>", big: "He told me that he was busy.", sub: "<b>✗ He said me that he was busy.</b><i>tell memakai objek langsung, say tidak.</i>" },
      { bg: "soft", kicker: "Salah 4", title: "Tanya sopan, <a>urutan biasa</a>", small: true, big: "Can you tell me where the station is?", sub: "<b>✗ … where is the station?</b><i>Pertanyaan tak langsung memakai urutan kalimat biasa.</i>" },
      { bg: "cream", kicker: "Salah 5", title: "make tanpa <a>to</a>", big: "She made me wait.", sub: "<b>✗ She made me to wait.</b><i>Setelah make + objek, kata kerja tanpa to.</i>" },
      { bg: "yellow", kicker: "Biar nempel", title: "Dari contoh <a>ke kebiasaan</a>", small: true, body: "Lihat contohnya, susun kalimatnya, isi soalnya, lalu pakai di misi.", cta: true },
    ],
  },
  {
    id: "20", name: "kalimat-sopan-melayani-tamu",
    slides: [
      { bg: "navy", kicker: "Buat calon kru kapal pesiar", title: "Kalimat sopan buat <a>melayani tamu</a>", small: true, body: "Diambil dari bab layanan dan bertanya dengan sopan, level B1 dan B2.", note: "geser →" },
      { bg: "cream", kicker: "Menerima pesanan", title: "Tanya <a>selera</a>", big: "Certainly. Would you like it mild or spicy?", sub: "<i>Tentu. Mau yang tidak pedas atau pedas?</i>" },
      { bg: "soft", kicker: "Tamu ingin difoto", title: "Pola <a>Would you mind</a>", small: true, big: "Would you mind taking a photo of us, please?", sub: "<b>✗ Would you mind to take photo us?</b><i>Would you mind + V-ing.</i>" },
      { bg: "cream", kicker: "Ada masalah", title: "Minta maaf <a>resmi</a>", small: true, big: "We apologise for any inconvenience this may have caused.", sub: "<i>Kami mohon maaf atas ketidaknyamanan ini.</i>" },
      { bg: "soft", kicker: "Lewat email", title: "Minta <a>konfirmasi</a>", big: "I would be grateful if you could confirm the date.", sub: "<i>Saya akan berterima kasih bila Anda dapat memastikan tanggalnya.</i>" },
      { bg: "yellow", kicker: "Misi B1", title: "Jaga meja <a>informasi</a>", small: true, body: "Musim liburan, Terminal Bus Kampung Bahasa penuh pelancong bingung. Kamu yang jaga meja informasinya.", cta: true },
    ],
  },
  {
    id: "21", name: "kenalan-sama-miss-kate",
    slides: [
      { bg: "soft", kicker: "Gurumu di Kampung Inggris", title: "Kenalan sama <a>Miss Kate</a>", small: true, body: "Datangi dia di depan English Class Academy untuk membuka jalur belajarmu.", phone: "3d-miss-kate.webp", note: "geser →" },
      { bg: "cream", kicker: "Dari Miss Kate", title: "Yang dia <a>kasih</a>", items: [
        { e: "📚", t: "Jalur belajar", d: "Materi, latihan, sampai ujian level." },
        { e: "⭐", t: "Misi pertamamu", d: "Kartu nama kosong untuk kenalan dengan warga." },
        { e: "🎉", t: "Ujian minggu pertama", d: "Sehari penuh tanpa bantuan, lalu pesta sambutan dari warga." },
      ] },
      { bg: "yellow", kicker: "Sampai akhir cerita", title: "Dari Pare <a>sampai London</a>", small: true, body: "Di level tertinggi, surat Miss Kate datang dari Pare: maukah kamu pulang dan menyambut para pendatang baru?", cta: true },
    ],
  },
  // ---------------------------------------------------------------- week 4
  {
    id: "22", name: "tebak-preposisi",
    slides: [
      { bg: "yellow", kicker: "Tebak, yuk", title: "I am interested ___ music. <a>Isi apa?</a>", small: true, items: [{ e: "A", t: "on" }, { e: "B", t: "in" }, { e: "C", t: "at" }], note: "jawab di komentar, lalu geser →" },
      { bg: "cream", kicker: "Jawabannya", title: "interested <a>in</a>", big: "I am interested in music.", sub: "<b>✗ I am interested on music.</b><i>interested selalu berpasangan dengan in.</i>", cta: true },
    ],
  },
  {
    id: "23", name: "level-b1-dan-b2",
    slides: [
      { bg: "soft", kicker: "Seri level · 4 & 5 dari 7", title: "B1 & B2: <a>mulai berpendapat</a>", small: true, body: "Dari bercerita ke berdiskusi. Di sini bahasa Inggrismu mulai terasa lancar.", note: "geser →" },
      { bg: "cream", kicker: "Level B1", title: "Opini & <a>alasan</a>", items: [
        { e: "🗞️", t: "Topik: opini, berita & media, pendidikan" }, { e: "🧩", t: "Present perfect, conditionals" },
        { e: "✅", t: "Bisa: memberi pendapat dengan alasan, menulis email semi-formal, bercerita pengalaman" },
      ] },
      { bg: "soft", kicker: "Contoh kalimat B1", title: "Kalau <a>seandainya</a>", small: true, big: "If I had more time, I would learn Japanese.", sub: "<i>Kalau saya punya lebih banyak waktu, saya akan belajar bahasa Jepang.</i>" },
      { bg: "cream", kicker: "Level B2", title: "Diskusi & <a>debat</a>", items: [
        { e: "🌍", t: "Topik: diskusi, lingkungan, teknologi" }, { e: "🧩", t: "Passive voice, reported speech" },
        { e: "✅", t: "Bisa: berdiskusi topik abstrak, presentasi singkat, memahami artikel panjang" },
      ] },
      { bg: "yellow", kicker: "Contoh kalimat B2", title: "Bahasa <a>resmi</a>", small: true, big: "I am writing to enquire about council tax.", sub: "<i>Saya menulis untuk menanyakan pajak daerah.</i>", cta: true },
    ],
  },
  {
    id: "24", name: "pte-academic-sekilas",
    slides: [
      { bg: "navy", kicker: "Infografik", title: "PTE Academic <a>sekilas</a>", body: "Tes di komputer, sekitar 2 jam, hasilnya cepat.", note: "geser →" },
      { bg: "cream", kicker: "3 bagian", title: "Isi <a>tesnya</a>", items: [
        { e: "🎙️", t: "Speaking & Writing", d: "Bicara dan menulis dalam satu bagian." },
        { e: "📖", t: "Reading" }, { e: "🎧", t: "Listening" },
      ], src: RESMI },
      { bg: "soft", kicker: "Skor & hasil", title: "Angka yang <a>perlu tahu</a>", small: true, items: [
        { e: "🔢", t: "Skor 10–90", d: "Memakai Global Scale of English." },
        { e: "⏱️", t: "Sekali duduk, sekitar 2 jam" },
        { e: "📬", t: "Hasil biasanya dalam 2 hari kerja", d: "Kadang sampai 5 hari kerja." },
      ] },
      { bg: "cream", kicker: "Ciri khasnya", title: "Speaking <a>ke mikrofon</a>", small: true, body: "Kamu bicara ke komputer, bukan ke penguji. Biasakan bicara jelas tanpa menunggu lawan bicara." },
      { bg: "yellow", kicker: "Latihan dari sekarang", title: "Biasakan <a>pakai bahasa Inggris</a>", small: true, body: "Chat wajib bahasa Inggris, misi percakapan dengan warga, dan ngobrol langsung dengan warga di Kampung Bahasa.", cta: true },
    ],
  },
  {
    id: "25", name: "misi-b1-b2-dari-pare-ke-london",
    slides: [
      { bg: "navy", kicker: "Misi level B1 & B2", title: "Dari Pare <a>ke London</a>", body: "Ceritamu berlanjut: jadi reporter, lalu kuliah di London.", phone: "3d-london.webp", note: "geser →" },
      { bg: "cream", kicker: "B1 · Kampung Post", title: "Jadi <a>reporter</a>", body: "Magang di Kampung Post: wawancara warga, meliput banjir di Pasar Pare, sampai menulis kolom opini." },
      { bg: "soft", kicker: "B1 · Misi besar", title: "Edisi <a>khusus</a>", body: "Kampung Post genap sepuluh tahun. Satu halaman edisi khususnya kamu yang tulis, lalu dibawa sampai ke London." },
      { bg: "cream", kicker: "B2 · London", title: "Kontrak <a>flat</a>", body: "Tinggal di flat Mr. Doyle bersama Aisha dan Luca. Pahami dulu pasal kontraknya sebelum tanda tangan." },
      { bg: "soft", kicker: "B2 · Kampus", title: "Debat & <a>presentasi</a>", small: true, body: "Catat kuliah Dr. Bennett, ikut klub debat, tulis petisi, lalu ajukan proposal ke konferensi mahasiswa." },
      { bg: "yellow", kicker: "Misi besar B2", title: "Konferensi <a>internasional</a>", small: true, body: "Tiga hari meneliti, tampil di panel, dan berdebat. Di resepsi penutup, seseorang memperhatikanmu.", cta: true },
    ],
  },
  {
    id: "26", name: "salah-kaprah-b2-c1",
    slides: [
      { bg: "soft", kicker: "Level B2 & C1", title: "Salah yang masih lolos di <a>level atas</a>", small: true, body: "Yang sudah lancar pun sering kepeleset di sini.", note: "geser →" },
      { bg: "cream", kicker: "Salah 1", title: "Penyesalan pakai <a>had + V3</a>", small: true, big: "If I had known, I would have come.", sub: "<b>✗ If I would have known, …</b><i>Setelah if memakai had + V3.</i>" },
      { bg: "soft", kicker: "Salah 2", title: "Modal + <a>have</a>, bukan had", small: true, big: "It must have been the chicken.", sub: "<b>✗ It must had been the chicken.</b><i>Setelah modal selalu have + V3.</i>" },
      { bg: "cream", kicker: "Salah 3", title: "unless sudah <a>negatif</a>", small: true, big: "Unless you pay, you can't stay.", sub: "<b>✗ Unless you don't pay, you can stay.</b><i>Jangan tambah don't setelah unless.</i>" },
      { bg: "soft", kicker: "Salah 4", title: "Bukan very, <a>tapi far</a>", big: "The film was far better than the book.", sub: "<b>✗ … very better than the book.</b><i>Sebelum comparative pakai far atau much.</i>" },
      { bg: "cream", kicker: "Salah 5", title: "Pasangan kata <a>tetap</a>", small: true, big: "The actor gave a wonderful performance.", sub: "<b>✗ The actor made a wonderful performance.</b><i>performance berpasangan dengan give.</i>" },
      { bg: "yellow", kicker: "Naik terus", title: "Sampai <a>C2</a>", body: "Kolokasi, idiom, dan register dipelajari di level C1 dan C2.", cta: true },
    ],
  },
  {
    id: "27", name: "toefl-itp-sekilas",
    slides: [
      { bg: "navy", kicker: "Infografik", title: "TOEFL ITP <a>sekilas</a>", body: "Tes yang sering diminta kampus dan instansi di Indonesia.", note: "geser →" },
      { bg: "cream", kicker: "Level 1 · 140 soal · 115 menit", title: "Isi <a>tesnya</a>", small: true, table: { head: ["Bagian", "Soal", "Waktu"], rows: [
        ["Listening", "50", "35 menit"], ["Structure & Written Expression", "40", "25 menit"], ["Reading", "50", "55 menit"],
      ] }, src: RESMI },
      { bg: "soft", kicker: "Skor", title: "310 sampai <a>677</a>", items: [
        { e: "🔢", t: "Skor total 310–677" },
        { e: "🚫", t: "Tidak ada batas lulus dari ETS", d: "Tiap kampus atau instansi menentukan skor yang diminta." },
        { e: "🗣️", t: "Tanpa bagian speaking dan writing" },
      ] },
      { bg: "cream", kicker: "Bagian Structure", title: "Isinya <a>tata bahasa</a>", small: true, body: "Melengkapi kalimat dan menemukan bagian yang salah. Persis yang kamu latih di bab tata bahasa tiap level." },
      { bg: "yellow", kicker: "Cicil dari sekarang", title: "Tata bahasa, <a>bab demi bab</a>", small: true, body: "Tiap konsep: contoh, kesalahan umum, kalimat untuk disusun, dan soal isian.", cta: true },
    ],
  },
  {
    id: "28", name: "level-c1-c2-puncaknya",
    slides: [
      { bg: "navy", kicker: "Seri level · 6 & 7 dari 7", title: "C1 & C2: <a>puncaknya</a>", body: "Bahasa Inggris untuk kerja profesional, akademik, dan sastra.", phone: "3d-london.webp", note: "geser →" },
      { bg: "cream", kicker: "Level C1", title: "Akademik & <a>negosiasi</a>", items: [
        { e: "📑", t: "Topik: bahasa akademik, negosiasi, idiom, nuansa & register" },
        { e: "✅", t: "Bisa: menulis esai terstruktur, bernegosiasi, memahami humor & idiom" },
      ] },
      { bg: "soft", kicker: "Misi C1 · Thames Policy Lab", title: "Jadi <a>analis muda</a>", small: true, body: "Balas email klien yang tersinggung, negosiasi dengan Mr. Chen, sampai menghadapi wartawan di konferensi pers krisis." },
      { bg: "cream", kicker: "Level C2", title: "Sastra & <a>retorika</a>", items: [
        { e: "📖", t: "Topik: sastra, retorika, bahasa profesional" },
        { e: "✅", t: "Bisa: berkomunikasi hampir seperti penutur asli, menyunting tulisan orang lain" },
      ] },
      { bg: "soft", kicker: "Misi C2", title: "Pidato sampai <a>juru bahasa</a>", small: true, body: "Berpidato di Speakers' Corner, debat gaya Oxford, lalu jadi penerjemah untuk KBRI London." },
      { bg: "yellow", kicker: "Misi besar C2", title: "Bukumu <a>terbit</a>", body: "Kumpulan esai tentang perjalananmu dari Pare ke London. Lalu surat dari Miss Kate datang.", cta: true },
    ],
  },
  {
    id: "29", name: "toeic-sekilas",
    slides: [
      { bg: "navy", kicker: "Infografik", title: "TOEIC <a>sekilas</a>", body: "Tes bahasa Inggris untuk dunia kerja.", note: "geser →" },
      { bg: "cream", kicker: "Listening & Reading · 200 soal", title: "Isi <a>tesnya</a>", small: true, table: { head: ["Bagian", "Soal", "Waktu"], rows: [
        ["Listening", "100", "±45 menit"], ["Reading", "100", "75 menit"],
      ] }, src: RESMI },
      { bg: "soft", kicker: "Skor", title: "10 sampai <a>990</a>", items: [
        { e: "🎧", t: "Listening 5–495" }, { e: "📖", t: "Reading 5–495" }, { e: "➕", t: "Total 10–990" },
      ] },
      { bg: "cream", kicker: "Soalnya tentang apa?", title: "Situasi <a>kantor</a>", small: true, body: "Percakapan kerja, pengumuman, email, dan dokumen. Mirip misi kerja di level A2 sampai C1." },
      { bg: "yellow", kicker: "Latihan dari sekarang", title: "Email, rapat, <a>klien</a>", small: true, body: "Di level B2 dan C1 kamu menulis email resmi, merapikan catatan rapat, dan bernegosiasi.", cta: true },
    ],
  },
  {
    id: "30", name: "basic-sampai-c2-satu-jalur",
    slides: [{
      bg: "yellow", kicker: "Satu jalur",
      title: "Basic sampai C2, <a>di satu tempat.</a>", small: true,
      body: "Materi bersuara, latihan, menulis tanpa autocorrect, misi bareng warga, dan ngobrol langsung di Kampung Inggris 3D.",
      phone: "3d-kampung-inggris.webp", cta: true,
    }],
  },
];
