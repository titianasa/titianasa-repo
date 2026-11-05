// Every card of the decks whose slug starts with argv[2], in 4:5 and 9:16, film and web: content must stay inside the card.
import { openView } from "../webview.ts";
// KARTU points at another copy of the decks (a snapshot served by its own dev server), so writers can keep editing.
const { DECKS } = await import(process.env.KARTU ?? "../../../../titian-web/src/content/kartu/index.ts");
const prefix = process.argv[2] ?? "";
const [k, n] = (process.argv[3] ?? "0/1").split("/").map(Number);
const prefixes = prefix.split(",");
const decks = Object.values(DECKS).filter((d, i) => prefixes.some((p) => d.slug.startsWith(p)) && i % n === k);
const view = openView(540, 960); const WEB = process.env.WEB ?? "http://localhost:3010";
await view.navigate(`${WEB}/login`);
const out: string[] = []; let done = 0;
// Animations are settled first, so only the card at rest is measured: entrances are finished, and endless pulses
// (pz-a-pop scales a box up and down) are paused at their start. Shapes under a clip-path are skipped: a clipped shape
// (a tangent line in a lab plot) reports its unclipped size, though nothing of it shows outside the clip.
const measure = `(() => { for (const a of document.getAnimations()) { try { a.finish(); } catch { a.pause(); a.currentTime = 0; } } const m = document.querySelector("#kartu .pz-card-main"); if (!m) return null; const b = m.getBoundingClientRect(); let bottom = 0, top = 1e9, right = 0; m.querySelectorAll("*").forEach((e) => { if (e.closest("[clip-path]")) return; const x = e.getBoundingClientRect(); if (!x.width) return; bottom = Math.max(bottom, x.bottom); top = Math.min(top, x.top); right = Math.max(right, x.right); }); return { over: Math.round(Math.max(bottom - b.bottom, b.top - top)), wide: Math.round(right - b.right), page: document.querySelector("#kartu header span:last-child")?.textContent }; })()`;
for (const [name, w, h] of [["9x16", 540, 960]] as const) {
  await view.cdp("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: false });
  for (const d of decks) {
    await view.navigate(`${WEB}/puzzle-kartu/${d.slug}?kartu=1&rasio=${name}`);
    for (let t = 0; t < 400; t++) { if (await view.evaluate<boolean>(`(() => { const e = document.querySelector("#kartu .pz-card-main"); return !!e && Object.keys(e).some((k) => k.startsWith("__reactProps")); })()`).catch(() => false)) break; await Bun.sleep(100); }
    console.log(name, d.slug);
    for (let n = 1; n <= d.cards.length + 1; n++) for (const mode of ["", "&web"]) {
      await view.evaluate(`history.pushState(null, "", "?kartu=${n}&rasio=${name}${mode}")`);
      let r: any = null;
      for (let t = 0; t < 20; t++) { await Bun.sleep(60); r = await view.evaluate(measure); if (r && r.page?.split("/")[0] === String(n)) break; }
      done++;
      if (!r || r.page?.split("/")[0] !== String(n)) { out.push(`STALE ${name}${mode} ${d.slug} ${n}`); continue; }
      if (r.over > 1 || r.wide > 1) { const l = `${name}${mode} ${d.slug} ${n} (${d.cards[n - 2]?.t ?? "cover"}) over=${r.over} wide=${r.wide}`; out.push(l); console.log("ISSUE", l); }
    }
  }
}
console.log("checked", done, "cards in", decks.length, "decks"); console.log(out.join("\n") || "NO OVERFLOW"); view.close(); process.exit(0);
