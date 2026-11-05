// Generates the slide pages (preview-ig.html / preview-tiktok.html) for the first 9 posts.
// Run: bun build.ts   → then bun render.ts to export PNGs.
type Slide = {
  bg?: "cream" | "yellow" | "navy" | "soft";
  kicker?: string;
  title: string; // <a>..</a> = accent words
  body?: string;
  note?: string; // handwritten aside
  phone?: string;
  items?: { e: string; t: string; d?: string }[];
  big?: string; // huge centered glyph/text (greeting)
  sub?: string; // romanization under `big`
  tag?: string; // tilted corner sticker
  cta?: boolean; // big url block
};
type Post = { id: string; name: string; slides: Slide[] };

const POSTS: Post[] = [
  {
    id: "01", name: "halo-kami-titian-asa",
    slides: [{
      bg: "cream", kicker: "Kenalan dulu, yuk", tag: "Baru hadir!",
      title: "Semua Asa, <a>Pasti Ada Jalannya!</a>",
      body: "Halo! Kami <b>Titian Asa</b>, teman belajar yang nemenin kamu dari bangku sekolah sampai mimpi paling jauh.",
      note: "belajar sampai bisa & terbiasa~", cta: true,
    }],
  },
  {
    id: "02", name: "titian-asa-itu-apa",
    slides: [
      { bg: "yellow", kicker: "Kenalan 30 detik", title: "Titian Asa itu <a>apa sih?</a>", body: "Geser pelan-pelan. Janji nggak pakai bahasa brosur.", note: "geser →" },
      { bg: "cream", kicker: "Arti nama", title: "Titian = <a>jembatan.</a><br/>Asa = <a>harapan.</a>", body: "Jadi Titian Asa itu jembatan menuju harapanmu. Jembatan belajar, menuju masa depan." },
      { bg: "soft", kicker: "Visi kami", title: "Nggak ada asa yang <a>buntu jalannya.</a>", body: "Mau masuk PTN impian, lancar bahasa asing, atau sekadar nggak remedial lagi. Semua ada jalannya, dan kami mau jadi jembatannya." },
      { bg: "cream", kicker: "Misi kami", title: "Caranya <a>gimana?</a>", items: [
        { e: "🔁", t: "Belajar sampai bisa", d: "Yang salah diulang sampai paham." },
        { e: "🧭", t: "Satu tempat, banyak jalur", d: "Dari materi sekolah sampai bahasa asing." },
        { e: "🎮", t: "Seru, bukan beban", d: "Misi, streak, level, liga." },
        { e: "📱", t: "Gratis buat mulai", d: "Cukup browser di HP atau laptop." },
      ] },
      { bg: "yellow", kicker: "Sekarang giliranmu", title: "Asa kamu <a>apa?</a>", body: "Tulis di kolom komentar. Jalannya kita cari bareng.", cta: true },
    ],
  },
  {
    id: "03", name: "rilis-kampung-bahasa-pare",
    slides: [{
      bg: "navy", kicker: "Belajar bahasa serasa di Pare", tag: "Sudah rilis!",
      title: "Kampung Bahasa <a>Pare</a>",
      body: "Belajar <b>5 bahasa</b> di kampung virtual yang seru. Gratis, langsung dari browser.",
      phone: "kampung.webp", cta: true,
    }],
  },
  {
    id: "04", name: "cara-belajar-kampung-pare",
    slides: [
      { bg: "soft", kicker: "Panduan singkat", title: "Cara belajar di <a>Kampung Bahasa Pare</a>", body: "5 langkah dari anak baru sampai terbang ke luar negeri.", phone: "kampung.webp", note: "geser →" },
      { bg: "cream", kicker: "Langkah 1", title: "Tinggal di <a>kampung</a>", body: "Jelajahi kampung pixel-art. Masuk kelas, mampir ke warung, sapa warga.", phone: "kampung.webp" },
      { bg: "cream", kicker: "Langkah 2", title: "Belajar <a>bertahap</a>", body: "Materi dulu, baru latihan. Yang salah muncul lagi sampai kamu paham.", phone: "latihan.webp" },
      { bg: "cream", kicker: "Langkah 3", title: "Jalani <a>misi</a>", body: "Kenalan dengan tetangga, tanya jalan, belanja di pasar. Semua pakai bahasa asing.", phone: "misi.webp" },
      { bg: "cream", kicker: "Langkah 4", title: "Ngobrol sama <a>teman belajar</a>", body: "Chat dan voice note wajib pakai bahasa yang lagi dipelajari. Auto kepake.", phone: "chat.webp" },
      { bg: "yellow", kicker: "Langkah 5", title: "Naik level, <a>terbang!</a>", body: "Uang dari belajar bisa buat beli tiket ke London, Beijing, Kairo, Tokyo, atau Seoul.", phone: "pesawat.webp", cta: true },
    ],
  },
  {
    id: "05", name: "kenapa-cepat-lupa",
    slides: [
      { bg: "cream", kicker: "Jujur aja", title: "Udah belajar, kok <a>cepet lupa?</a>", body: "Bukan kamu yang kurang pintar. Cara belajarnya yang perlu diganti.", note: "geser →" },
      { bg: "soft", kicker: "Cara 1", title: "Yang salah, <a>diulang.</a>", body: "Soal yang salah nggak dibuang. Dia muncul lagi di waktu yang pas sampai nempel di kepala.", items: [{ e: "🔁", t: "Spaced repetition", d: "Ulang di waktu yang tepat." }] },
      { bg: "cream", kicker: "Cara 2", title: "Dikit, tapi <a>tiap hari.</a>", body: "Lima belas menit rutin lebih ngaruh daripada begadang semalam.", items: [{ e: "🔥", t: "Streak, XP, level", d: "Biar semangatnya nggak padam." }] },
      { bg: "soft", kicker: "Cara 3", title: "Dipakai, <a>bukan dihafal.</a>", body: "Bahasa baru langsung dipakai ngobrol dan jalanin misi. Bukan cuma dicatat.", items: [{ e: "💬", t: "Praktik langsung", d: "Sama warga dan teman belajar." }] },
      { bg: "yellow", kicker: "Intinya", title: "Belajar sampai <a>bisa & terbiasa.</a>", body: "Itu cara belajar di Titian Asa.", cta: true },
    ],
  },
  {
    id: "06", name: "salah-itu-pijakan",
    slides: [{
      bg: "yellow", kicker: "Pengingat hari ini",
      title: "Salah itu bukan gagal. Salah itu <a>pijakan pertama.</a>",
      body: "Tak perlu takut salah. Setiap kesalahan adalah awal menuju paham.",
      note: "simpan buat hari yang berat~", cta: true,
    }],
  },
  {
    id: "07", name: "program-titian-asa",
    slides: [
      { bg: "navy", kicker: "Bocoran program", title: "Satu jembatan, <a>banyak tujuan.</a>", body: "Ini yang lagi kami siapkan. Kampung Bahasa Pare sudah bisa dipakai belajar sekarang.", note: "geser →" },
      { bg: "cream", kicker: "Program 1", tag: "Segera hadir", title: "Ruang <a>Belajar</a>", body: "Materi sekolah SD sampai SMA, Cambridge, dan Bahasa Inggris. Unit demi unit, bareng tutor AI.", items: [{ e: "📚", t: "Kurikulum Merdeka & K13" }, { e: "🌍", t: "Cambridge & CEFR A1–C2" }] },
      { bg: "soft", kicker: "Program 2", tag: "Segera hadir", title: "<a>TKA</a> per jenjang", body: "Latihan Tes Kemampuan Akademik dengan soal bertingkat.", items: [{ e: "✏️", t: "SD/MI · SMP/MTs · SMA/MA" }] },
      { bg: "cream", kicker: "Program 3", tag: "Segera hadir", title: "UTBK <a>SNBT</a>", body: "Kuasai semua subtes menuju PTN impian.", items: [{ e: "🎯", t: "TPS, Literasi, Penalaran Matematika" }] },
      { bg: "soft", kicker: "Program 4", tag: "Segera hadir", title: "Tryout <a>online</a>", body: "Simulasi ujian dengan timer nyata dan penilaian IRT, kayak ujian aslinya.", items: [{ e: "⏱️", t: "TKA, SNBT, Olimpiade" }] },
      { bg: "cream", kicker: "Program 5", tag: "Segera hadir", title: "Mock test <a>global</a>", body: "Simulasi tes bahasa Inggris internasional, lengkap empat keterampilan.", items: [{ e: "🎧", t: "IELTS · TOEFL iBT · PTE" }] },
      { bg: "yellow", kicker: "Program 6", tag: "Segera hadir", title: "Study group <a>& liga</a>", body: "Belajar bareng teman, lalu adu rajin di liga mingguan. Sambil nunggu, belajar bahasa di Pare dulu.", cta: true },
    ],
  },
  {
    id: "08", name: "halo-dalam-5-bahasa",
    slides: [
      { bg: "cream", kicker: "Tes cepat", title: "Bisa bilang halo dalam <a>5 bahasa?</a>", body: "Di Kampung Bahasa Pare, tiap kampung punya bahasanya sendiri.", note: "geser, coba ucapin →" },
      { bg: "soft", kicker: "Kampung Inggris → London", title: "Bahasa <a>Inggris</a>", big: "Hello!<br/>Nice to meet you.", sub: "Halo! Senang bertemu denganmu." },
      { bg: "cream", kicker: "Kampung Mandarin → Beijing", title: "Bahasa <a>Mandarin</a>", big: "你好！<br/>很高兴认识你。", sub: "Nǐ hǎo! Hěn gāoxìng rènshi nǐ." },
      { bg: "soft", kicker: "Kampung Arab → Kairo", title: "Bahasa <a>Arab</a>", big: "<span dir='rtl'>مرحبًا!<br/>تشرفت بمعرفتك.</span>", sub: "Marḥaban! Tasharraftu bi-ma‘rifatik." },
      { bg: "cream", kicker: "Kampung Jepang → Tokyo", title: "Bahasa <a>Jepang</a>", big: "こんにちは！<br/>はじめまして。", sub: "Konnichiwa! Hajimemashite." },
      { bg: "soft", kicker: "Kampung Korea → Seoul", title: "Bahasa <a>Korea</a>", big: "안녕하세요!<br/>만나서 반가워요.", sub: "Annyeonghaseyo! Mannaseo bangawoyo." },
      { bg: "yellow", kicker: "Giliran kamu", title: "Pilih <a>kampungmu.</a>", body: "Mulai dari Basic, naik level pelan-pelan, sampai bisa ngobrol beneran.", cta: true },
    ],
  },
  {
    id: "09", name: "mulai-dari-satu-kata",
    slides: [{
      bg: "yellow", kicker: "Bingung mulai dari mana?", tag: "Gratis!",
      title: "Mulai dari <a>satu kata.</a>",
      body: "Kampung Bahasa Pare sudah buka buat belajar 5 bahasa. Program lainnya nyusul.",
      phone: "london.webp", cta: true,
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
    <div class="brand"><span class="logo"><img src="assets/titian.png"/></span><span>Titian Asa</span></div>
    ${n > 1 ? `<div class="pager">${i + 1}/${n}</div>` : ""}
  </header>
  <main>
    <div class="copy">
      ${s.kicker ? `<div class="kicker">${s.kicker}</div>` : ""}
      <h1>${acc(s.title)}</h1>
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
    <span class="url">titianasa.com</span>
  </footer>
</section>`;
}

const css = await Bun.file(import.meta.dir + "/slides.css").text();
for (const [ratio, h] of [["ig", 1350], ["tiktok", 1920]] as const) {
  const html = `<!doctype html><html lang="id"><head><meta charset="utf-8"/><title>Titian Asa — konten ${ratio}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Fredoka:wght@400..700&family=Nunito:wght@400..900&display=block" rel="stylesheet"/>
<style>:root{--h:${h}px}${css}</style></head><body class="r-${ratio}">
${POSTS.map((p) => p.slides.map((s, i) => slideHtml(p, s, i)).join("\n")).join("\n")}
</body></html>`;
  await Bun.write(`${import.meta.dir}/preview-${ratio}.html`, html);
}
await Bun.write(import.meta.dir + "/manifest.json", JSON.stringify(POSTS.map((p) => ({ id: p.id, name: p.name, slides: p.slides.length })), null, 2));
console.log("slides:", POSTS.reduce((a, p) => a + p.slides.length, 0));
