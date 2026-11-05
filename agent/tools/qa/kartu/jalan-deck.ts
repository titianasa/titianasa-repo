// Walks a deck like a learner on the web: every card, plus the proof at several moments and the callback opened.
import { DECKS } from "../../../../titian-web/src/content/kartu/index.ts";
import { openView } from "../webview.ts";
const slug = process.argv[2]; const d = DECKS[slug];
const view = openView(540, 960); const WEB = process.env.WEB ?? "http://localhost:3010"; const OUT = process.env.OUT ?? "jalan";
const shot = async (f: string) => { const r: any = await view.cdp("Page.captureScreenshot", { format: "png" }); await Bun.write(`${OUT}/${f}.png`, Buffer.from(r.data, "base64")); };
for (let n = Number(process.argv[3] ?? 1); n <= d.cards.length + 1; n++) {
  await view.navigate(`${WEB}/puzzle-kartu/${slug}?kartu=${n}&rasio=9x16&web`); await Bun.sleep(2500);
  const c: any = d.cards[n - 2];
  await shot(`${slug}-${String(n).padStart(2, "0")}`);
  if (c?.t === "lab" && c.lab.k === "bukti-pythagoras") { await Bun.sleep(1800); await shot(`${slug}-${n}-b`); await Bun.sleep(3000); await shot(`${slug}-${n}-c`); }
  if (c?.t === "ingat") { await view.evaluate(`[...document.querySelectorAll('button')].find(b => b.innerText.includes('Buka kartunya'))?.click()`); await Bun.sleep(1500); await shot(`${slug}-${n}-buka`); }
  console.log(n, c?.t ?? "cover");
}
view.close(); process.exit(0);
