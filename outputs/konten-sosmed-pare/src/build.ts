// Slide pages (preview-ig.html / preview-tiktok.html) for the Kampung Bahasa Pare accounts (@pare.titianasa).
// Run: bun build.ts   → then bun render.ts to export PNGs. Same slide model as ../../konten-sosmed/src/build.ts,
// with the app's own brand chip and pare.titianasa.com on every slide.
type Slide = {
  bg?: "cream" | "yellow" | "navy" | "soft";
  kicker?: string;
  title: string; // <a>..</a> = accent words, <s>..</s> = struck-through list price
  small?: boolean; // a long title: one size down
  per?: string; // a short line right under the title (a price's period)
  body?: string;
  note?: string; // handwritten aside
  phone?: string;
  items?: { e: string; t: string; d?: string }[];
  big?: string; // the sentence on the card
  sub?: string; // how to say it, <i>..</i> = its meaning
  tag?: string; // tilted corner sticker
  cta?: boolean; // big url block
};
type Post = { id: string; name: string; slides: Slide[] };

const URL = "pare.titianasa.com";
const BRAND = "Kampung Bahasa Pare";

const POSTS: Post[] = [
  {
    id: "01", name: "suasana-pare-di-hp-mu",
    slides: [{
      bg: "navy", kicker: "Buat para pejuang bahasa", tag: "Gratis!",
      title: "Suasana Kampung Inggris Pare, <a>sekarang di HP-mu.</a>", small: true,
      body: "English Area, camp, jajan, dan teman belajar baru. Belajar bahasa Inggris dari <b>Basic sampai C2</b>, langsung dari browser.",
      phone: "senja.webp", cta: true,
    }],
  },
  {
    id: "02", name: "kamu-tipe-yang-mana",
    slides: [
      { bg: "yellow", kicker: "Jujur aja", title: "4 tipe pejuang bahasa. <a>Kamu yang mana?</a>", small: true, body: "Geser, cari yang paling kamu banget.", note: "geser →" },
      { bg: "cream", kicker: "Tipe 1 · Lagi di Pare", title: "<span class='nb'>English Area-nya</span> <a>lanjut sampai camp.</a>", small: true, body: "Pulang kursus, lanjut latihan dari kasur. Di Kampung Inggris versi HP ini, chat-nya juga wajib bahasa Inggris.", phone: "chat-ramai.webp" },
      { bg: "soft", kicker: "Tipe 2 · Mager ke Pare", title: "Rebahan, tapi tetap <a>belajar.</a>", small: true, body: "Nggak perlu packing dan cari camp. Suasana Kampung Inggris Pare ada di HP-mu: kelas, misi, sampai jajan pecel.", phone: "jajan.webp" },
      { bg: "cream", kicker: "Tipe 3 · Belum sempat ke Pare", title: "Cicil dulu <a>dari sini.</a>", small: true, body: "Kerja atau kuliah belum bisa ditinggal? Mulai dari Basic sekarang. Pas berangkat ke Pare nanti, kamu sudah nggak dari nol.", phone: "jalur.webp" },
      { bg: "soft", kicker: "Tipe 4 · Alumni Pare", title: "Kangen Pare? <a>Balik lagi, yuk.</a>", small: true, body: "Sepeda ontel, pecel, camp, English Area. Nostalgianya dapat, bahasa Inggrisnya nyambung lagi.", phone: "senja.webp" },
      { bg: "yellow", kicker: "Apa pun tipemu", title: "Mulainya <a>sama.</a>", body: "Buka di browser, pilih bahasa Inggris, kerjakan pelajaran pertama. Gratis.", cta: true },
    ],
  },
  {
    id: "03", name: "cara-belajar-bahasa-inggris",
    slides: [
      { bg: "soft", kicker: "Panduan singkat", title: "Cara belajar bahasa Inggris di <a>Kampung Bahasa</a>", small: true, body: "5 langkah, dari <b>hello</b> pertama sampai ngobrol beneran.", phone: "jalur.webp", note: "geser →" },
      { bg: "cream", kicker: "Langkah 1", title: "Baca <a>materinya</a> dulu", body: "Tiap kata ada cara baca, arti, dan suaranya. Belum ada soal, belum ada nilai.", phone: "materi.webp" },
      { bg: "cream", kicker: "Langkah 2", title: "Lanjut <a>latihan</a>", body: "Soalnya dari materi yang baru kamu baca. Jawab benar, dapat XP dan uang saku.", phone: "benar.webp" },
      { bg: "cream", kicker: "Langkah 3", title: "Tulis <a>sendiri</a>", body: "Ketik jawabanmu tanpa autocorrect. Yang nempel di kepala, itu yang keluar.", phone: "tulis.webp" },
      { bg: "cream", kicker: "Langkah 4", title: "Jalani <a>misi</a>", body: "Kenalan dengan tetangga, belanja, tanya arah. Kalimat yang tadi dipelajari langsung dipakai.", phone: "misi-susun.webp" },
      { bg: "yellow", kicker: "Langkah 5", title: "Naik level, <a>lanjut terus</a>", body: "Bab dan misinya selesai, levelmu naik: Basic, A1, A2, sampai C2.", phone: "hasil.webp", cta: true },
    ],
  },
  {
    id: "04", name: "sehari-di-kampung-bahasa",
    slides: [
      { bg: "navy", kicker: "Suasananya Pare banget", title: "Sehari di <a>Kampung Bahasa</a>", small: true, body: "Belajarnya serius. Sisanya kayak anak camp beneran.", phone: "ramai.webp", note: "geser →" },
      { bg: "cream", kicker: "Pagi", title: "Masuk <a>kelas</a> dulu", body: "Baca materi, kerjakan latihan, lalu jalani misi dari tutor.", phone: "materi.webp" },
      { bg: "soft", kicker: "Siang", title: "Jajan ke <a>pakde dan budhe</a>", small: true, body: "Pecel Bu Sri, bakso Cak Mat, es degan Mbak Lis. Makan dulu, biar staminamu penuh lagi.", phone: "jajan.webp" },
      { bg: "cream", kicker: "Sore", title: "Healing di <a>lapangan senja</a>", small: true, body: "Hangout bareng teman belajar lain, lalu mampir ke Speaking Club yang buka dari jam 4 sore.", phone: "senja.webp" },
      { bg: "soft", kicker: "Keliling", title: "Naik <a><span class='nb'>odong-odong</span></a>", body: "Di sini namanya kereta kelinci. Keliling Kampung Bahasa, turun di halte mana saja. Atau sewa sepeda ontel.", phone: "odong.webp" },
      { bg: "yellow", kicker: "Malam", title: "Kenalan sama <a>teman baru</a>", small: true, body: "Ngobrol di chat sampai ngantuk. Ingat, di Kampung Inggris wajib bahasa Inggris.", phone: "chat-ramai.webp", cta: true },
    ],
  },
  {
    id: "05", name: "english-area-dan-punishment",
    slides: [
      { bg: "soft", kicker: "Aturan Kampung Inggris", title: "Di sini <a>English Area.</a>", body: "Kayak di Pare: masuk area ini, ngobrolnya wajib bahasa Inggris.", phone: "chat-ramai.webp", note: "geser →" },
      { bg: "cream", kicker: "Melanggar?", title: "Ada <a>punishment.</a>", body: "Pakai bahasa lain di chat Kampung Inggris, nyawamu berkurang satu. Tenang, nggak sampai disuruh nyanyi di depan camp." },
      { bg: "soft", kicker: "Tenang, ada bantuan", title: "Bingung mau <a>bilang apa?</a>", small: true, items: [
        { e: "💡", t: "Frasa cepat", d: "Kalimat siap pakai, tinggal ketuk." },
        { e: "🔤", t: "Cari terjemahan", d: "Ketik bahasa Indonesianya, dapat bahasa Inggrisnya." },
      ] },
      { bg: "cream", kicker: "Tanpa autocorrect", title: "Yang ngetik <a>kamu sendiri.</a>", small: true, body: "Papan ketiknya bawaan Kampung Bahasa, tanpa koreksi otomatis. Salah ketik? Justru di situ belajarnya.", phone: "tulis.webp" },
      { bg: "yellow", kicker: "Mau jago speaking?", title: "Ada <a>voice note & telepon.</a>", small: true, body: "Ngobrol pakai suara dengan teman belajar. Tersedia di paket Plus dan Pro.", cta: true },
    ],
  },
  {
    id: "06", name: "5-kalimat-kenalan-di-camp",
    slides: [
      { bg: "cream", kicker: "Hari pertama di camp", title: "5 kalimat bahasa Inggris buat <a>kenalan</a>", small: true, body: "Semuanya dari Bab 1 di Kampung Inggris. Coba ucapin satu-satu.", note: "geser →" },
      { bg: "soft", kicker: "Kalimat 1", title: "Sapa <a>dulu</a>", big: "Good morning!", sub: "gud MOR-ning<i>Selamat pagi!</i>" },
      { bg: "cream", kicker: "Kalimat 2", title: "Sebut <a>namamu</a>", big: "My name is Rina.", sub: "mai neim iz RI-na<i>Nama saya Rina.</i>" },
      { bg: "soft", kicker: "Kalimat 3", title: "Bilang <a>senang kenalan</a>", big: "Nice to meet you.", sub: "nais tu mit yu<i>Senang bertemu denganmu.</i>" },
      { bg: "cream", kicker: "Kalimat 4", title: "Cerita <a>asalmu</a>", big: "I am from Indonesia.", sub: "ai em from in-do-NI-sya<i>Saya dari Indonesia.</i>" },
      { bg: "soft", kicker: "Kalimat 5", title: "Tanya <a>kabar</a>", big: "How are you?<br/>I'm fine, thank you.", sub: "hau ar yu · aim fain, THENGK yu<i>Apa kabar? Saya baik, terima kasih.</i>" },
      { bg: "yellow", kicker: "Giliran kamu", title: "Sekarang <a>pakai beneran.</a>", body: "Di misi pertama, tetanggamu bakal nanya: <b>Where are you from?</b>", cta: true },
    ],
  },
  {
    id: "07", name: "buat-para-pejuang",
    slides: [
      { bg: "navy", kicker: "Pare itu tempat orang berjuang", title: "Kamu pejuang <a>yang mana?</a>", small: true, body: "Tujuannya beda-beda. Bahasa Inggrisnya dimulai dari tempat yang sama.", phone: "level.webp", note: "geser →" },
      { bg: "cream", kicker: "Pejuang beasiswa", title: "Kejar <a>beasiswa ke London</a>", small: true, body: "Di level B1, ceritamu mengejar beasiswa pertukaran ke London, lengkap dengan latihan wawancara visa pelajar. Di B2, kamu jadi mahasiswa pertukaran." },
      { bg: "soft", kicker: "Pejuang WHV", title: "Bahasa Inggris buat <a>kerja & hidup</a>", small: true, body: "Belanja, tanya arah, urusan dokter, sampai kerja paruh waktu dan gaji pertama. Itu yang kamu latih di level A1 dan A2." },
      { bg: "cream", kicker: "Calon kru kapal pesiar", title: "Melayani tamu dengan <a>sopan</a>", small: true, body: "Ada bab makan di luar, layanan dan keluhan, sampai bertanya dengan sopan. Semuanya dipakai langsung di misi." },
      { bg: "soft", kicker: "Pengin jago speaking", title: "Dipakai <a>tiap hari</a>", body: "Chat wajib bahasa Inggris, misi percakapan dengan warga, plus voice note dan telepon di paket Plus dan Pro." },
      { bg: "yellow", kicker: "Apa pun tujuanmu", title: "Mulainya <a>dari sini.</a>", body: "7 level, dari Basic sampai C2. Sudah bisa? Ikut ujian lompat level biar naik lebih cepat.", cta: true },
    ],
  },
  {
    id: "08", name: "gratis-plus-pro",
    slides: [
      { bg: "cream", kicker: "Pilih sesuai kebutuhan", tag: "Promo 75%", title: "Gratis dulu. <a>Mau lebih?</a>", body: "Ada paket Plus dan Pro. Bayar sekali, berlaku 30 hari, nggak diperpanjang otomatis.", phone: "paket.webp", note: "geser →" },
      { bg: "soft", kicker: "Gratis", title: "Cukup buat <a>mulai</a>", items: [
        { e: "📚", t: "Jalur belajar Basic sampai C2", d: "Naik level satu per satu." },
        { e: "❤️", t: "5 nyawa", d: "Habis? Penuh lagi dalam 24 jam." },
        { e: "💬", t: "Chat teks dengan teman belajar" },
      ] },
      { bg: "cream", kicker: "Plus", tag: "Promo 75%", title: "<a>Rp10.000</a> <s>Rp40.000</s>", per: "untuk 30 hari", items: [
        { e: "❤️", t: "Nyawa tanpa batas", d: "Belajar kapan saja dan lebih cepat, tanpa nunggu 24 jam." },
        { e: "🎙️", t: "Voice note dan telepon", d: "Latihan speaking dengan teman belajar." },
        { e: "🚫", t: "Bebas iklan" },
        { e: "💰", t: "Bonus uang saku Rp20.000", d: "Dipakai di dalam Kampung Bahasa." },
      ] },
      { bg: "soft", kicker: "Pro · paling lengkap", tag: "Promo 75%", title: "<a>Rp30.000</a> <s>Rp120.000</s>", per: "untuk 30 hari", items: [
        { e: "⭐", t: "Semua manfaat Plus", d: "Termasuk nyawa tanpa batas." },
        { e: "🔓", t: "Semua level, pelajaran, dan misi terbuka", d: "Belajar dari mana saja, nggak harus urut." },
        { e: "🎓", t: "Gratis ujian loncat level" },
        { e: "💰", t: "Bonus uang saku Rp100.000" },
      ] },
      { bg: "yellow", kicker: "Intinya", title: "Nyawa tanpa batas, <a>belajar kapan saja.</a>", small: true, body: "Nggak ada jeda nunggu nyawa penuh, jadi kamu maju lebih cepat. Bayar lewat QRIS dari dalam aplikasi.", cta: true },
    ],
  },
  {
    id: "09", name: "inggris-lengkap-empat-menyusul",
    slides: [{
      bg: "soft", kicker: "Kabar dari Kampung Bahasa",
      title: "Inggris sudah lengkap. <a>Empat bahasa lagi menyusul.</a>", small: true,
      items: [
        { e: "🇬🇧", t: "Inggris: Basic sampai C2", d: "Jalur belajar dan misinya lengkap." },
        { e: "🌏", t: "Mandarin, Arab, Jepang, Korea", d: "Bab awal sudah buka, lanjutannya sedang disusun." },
      ],
      note: "mulai dari Inggris dulu, yuk~", cta: true,
    }],
  },
];

const acc = (s: string) => s.replace(/<a>/g, '<span class="acc">').replace(/<\/a>/g, "</span>");

function slideHtml(p: Post, s: Slide, i: number): string {
  const n = p.slides.length;
  const id = `p${p.id}-s${i + 1}`;
  return `<section class="slide bg-${s.bg ?? "cream"}${s.phone ? " has-phone" : ""}${s.tag ? " has-tag" : ""}" id="${id}">
  <div class="dots"></div>
  <svg class="doodle sun" viewBox="0 0 100 100"><g stroke="var(--line)" stroke-width="4" stroke-linecap="round">${Array.from({ length: 12 }, (_, k) => { const a = (k * Math.PI) / 6; return `<line x1="${50 + Math.cos(a) * 34}" y1="${50 + Math.sin(a) * 34}" x2="${50 + Math.cos(a) * 46}" y2="${50 + Math.sin(a) * 46}"/>`; }).join("")}</g><circle cx="50" cy="50" r="25" fill="var(--sunfill)" stroke="var(--line)" stroke-width="4"/><path d="M40 54 q10 9 20 0" fill="none" stroke="var(--line)" stroke-width="3.5" stroke-linecap="round"/><circle cx="41" cy="45" r="3" fill="var(--line)"/><circle cx="59" cy="45" r="3" fill="var(--line)"/></svg>
  <svg class="doodle spark" viewBox="0 0 40 40"><path d="M20 2 C22 14,26 18,38 20 C26 22,22 26,20 38 C18 26,14 22,2 20 C14 18,18 14,20 2Z" fill="var(--sparkfill)" stroke="var(--line)" stroke-width="3" stroke-linejoin="round"/></svg>
  <header>
    <div class="brand"><span class="logo"><img src="assets/pare.png"/></span><span>${BRAND}</span></div>
    ${n > 1 ? `<div class="pager">${i + 1}/${n}</div>` : ""}
  </header>
  <main>
    <div class="copy">
      ${s.kicker ? `<div class="kicker">${s.kicker}</div>` : ""}
      <h1${s.small ? ' class="sm"' : ""}>${acc(s.title)}</h1>
      ${s.per ? `<div class="per">${s.per}</div>` : ""}
      ${s.big ? `<div class="bigcard"><div class="big">${s.big}</div>${s.sub ? `<div class="sub">${s.sub}</div>` : ""}</div>` : ""}
      ${s.body ? `<p class="body">${s.body}</p>` : ""}
      ${s.items ? `<ul class="items">${s.items.map((it) => `<li><span class="em">${it.e}</span><div><b>${it.t}</b>${it.d ? `<small>${it.d}</small>` : ""}</div></li>`).join("")}</ul>` : ""}
      ${s.note ? `<div class="note">${s.note}</div>` : ""}
    </div>
    ${s.phone ? `<div class="phone"><img src="assets/${s.phone}"/></div>` : ""}
    ${s.tag ? `<div class="tag">${s.tag}</div>` : ""}
  </main>
  <footer class="${s.cta ? "cta" : ""}">
    ${s.cta ? `<span class="hand">belajar gratis di</span>` : ""}
    <span class="url">${URL}</span>
  </footer>
</section>`;
}

const css = await Bun.file(import.meta.dir + "/slides.css").text();
for (const [ratio, h] of [["ig", 1350], ["tiktok", 1920]] as const) {
  const html = `<!doctype html><html lang="id"><head><meta charset="utf-8"/><title>${BRAND} — konten ${ratio}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Fredoka:wght@400..700&family=Nunito:wght@400..900&display=block" rel="stylesheet"/>
<style>:root{--h:${h}px}${css}</style></head><body class="r-${ratio}">
${POSTS.map((p) => p.slides.map((s, i) => slideHtml(p, s, i)).join("\n")).join("\n")}
</body></html>`;
  await Bun.write(`${import.meta.dir}/preview-${ratio}.html`, html);
}
await Bun.write(import.meta.dir + "/manifest.json", JSON.stringify(POSTS.map((p) => ({ id: p.id, name: p.name, slides: p.slides.length })), null, 2));
console.log("slides:", POSTS.reduce((a, p) => a + p.slides.length, 0));
