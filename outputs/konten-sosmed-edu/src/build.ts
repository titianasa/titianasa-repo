// Membuat halaman slide (preview-ig.html / preview-tiktok.html) untuk batch edukasi 30 hari.
// Jalankan: bun build.ts → lalu bun render.ts untuk mengekspor PNG.
import type { Post, Slide } from "./types";
import { A } from "./posts-a";
import { B } from "./posts-b";
import { C } from "./posts-c";

const POSTS: Post[] = [...A, ...B, ...C];
const acc = (s: string) => s.replace(/<a>/g, '<span class="acc">').replace(/<\/a>/g, "</span>");
const li = (x: string | { t: string; d?: string }) => (typeof x === "string" ? x : `${x.t}${x.d ? `<small>${x.d}</small>` : ""}`);

function slideHtml(p: Post, s: Slide, i: number): string {
  const n = p.slides.length;
  const id = `p${p.id}-s${i + 1}`;
  return `<section class="slide bg-${s.bg ?? "cream"}${s.phone ? " has-phone" : ""}${s.tag ? " has-tag" : ""}${s.dense ? " dense" : ""}${s.tight ? " tight" : ""}" id="${id}">
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
      ${s.body ? `<p class="body">${s.body}</p>` : ""}
      ${s.stats ? `<div class="stats">${s.stats.map((x) => `<div class="stat"><div class="n">${x.n}</div><div class="l">${x.l}</div></div>`).join("")}</div>` : ""}
      ${s.steps ? `<ul class="steps">${s.steps.map((x) => `<li class="${x.hot ? "hot" : ""}${x.done ? " done" : ""}"><span class="chip">${x.w}</span><div><b>${x.t}</b>${x.d ? `<small>${x.d}</small>` : ""}</div></li>`).join("")}</ul>` : ""}
      ${s.cmp ? `<div class="cmp">${s.cmp.map((c) => `<div class="col"><h3>${c.h}</h3><ul>${c.rows.map((r) => `<li>${li(r)}</li>`).join("")}</ul></div>`).join("")}</div>` : ""}
      ${s.checks ? `<ul class="checks${s.xs ? " x" : ""}">${s.checks.map((c) => `<li><div>${li(c)}</div></li>`).join("")}</ul>` : ""}
      ${s.items ? `<ul class="items">${s.items.map((it) => `<li><span class="em">${it.e}</span><div><b>${it.t}</b>${it.d ? `<small>${it.d}</small>` : ""}</div></li>`).join("")}</ul>` : ""}
      ${s.note ? `<div class="note">${s.note}</div>` : ""}
      ${s.src ? `<div class="src">${s.src}</div>` : ""}
    </div>
    ${s.phone ? `<div class="phone"><img src="assets/${s.phone}"/></div>` : ""}
    ${s.tag ? `<div class="tag">${s.tag}</div>` : ""}
  </main>
  <footer class="${s.cta ? "cta" : ""}">
    ${s.cta ? `<span class="hand">${s.hand ?? "belajar gratis di"}</span>` : ""}
    <span class="url">titianasa.com</span>
  </footer>
</section>`;
}

const css = await Bun.file(import.meta.dir + "/slides.css").text();
for (const [ratio, h] of [["ig", 1350], ["tiktok", 1920]] as const) {
  const html = `<!doctype html><html lang="id"><head><meta charset="utf-8"/><title>Titian Asa — konten edukasi ${ratio}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Fredoka:wght@400..700&family=Nunito:wght@400..900&display=block" rel="stylesheet"/>
<style>:root{--h:${h}px}${css}</style></head><body class="r-${ratio}">
${POSTS.map((p) => p.slides.map((s, i) => slideHtml(p, s, i)).join("\n")).join("\n")}
</body></html>`;
  await Bun.write(`${import.meta.dir}/preview-${ratio}.html`, html);
}
await Bun.write(import.meta.dir + "/manifest.json", JSON.stringify(POSTS.map((p) => ({ id: p.id, name: p.name, slides: p.slides.length })), null, 2));
console.log("posts:", POSTS.length, "slides:", POSTS.reduce((a, p) => a + p.slides.length, 0));
