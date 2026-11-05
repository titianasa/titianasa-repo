// Slide pages (preview-ig.html / preview-tiktok.html) for @pare.titianasa, November 2026 (30 days, posts.ts).
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
  table?: { head: string[]; rows: string[][] }; // an infographic table
  src?: string; // a small source line under the content
};
export type Post = { id: string; name: string; slides: Slide[] };

const URL = "pare.titianasa.com";
const BRAND = "Kampung Bahasa Pare";

const POSTS: Post[] = await import("./posts.ts").then((m) => m.POSTS);

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
      ${s.big ? `<div class="bigcard"><div class="big${s.big.replace(/<[^>]+>/g, "").length > 34 ? " long" : ""}">${s.big}</div>${s.sub ? `<div class="sub">${s.sub}</div>` : ""}</div>` : ""}
      ${s.body ? `<p class="body">${s.body}</p>` : ""}
      ${s.table ? `<table class="tbl"><thead><tr>${s.table.head.map((h) => `<th>${h}</th>`).join("")}</tr></thead><tbody>${s.table.rows.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join("")}</tr>`).join("")}</tbody></table>` : ""}
      ${s.items ? `<ul class="items">${s.items.map((it) => `<li><span class="em">${it.e}</span><div><b>${it.t}</b>${it.d ? `<small>${it.d}</small>` : ""}</div></li>`).join("")}</ul>` : ""}
      ${s.note ? `<div class="note">${s.note}</div>` : ""}
      ${s.src ? `<div class="src">${s.src}</div>` : ""}
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
