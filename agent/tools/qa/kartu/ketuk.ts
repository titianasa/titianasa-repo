// Opens a card in web mode, taps SVG shapes inside the lab by selector index, and captures the result.
import { openView } from "../webview.ts";
const [slug, n, sel, ...idx] = process.argv.slice(2);
const view = openView(540, 960);
const WEB = process.env.WEB ?? "http://localhost:3010"; const OUT = process.env.OUT ?? "shots";
await view.navigate(`${WEB}/puzzle-kartu/${slug}?kartu=${n}&rasio=9x16&web`); await Bun.sleep(3000);
for (const i of idx) { await view.evaluate(`(() => { const el = document.querySelectorAll('.pz-visual ${sel}')[${i}]; el?.dispatchEvent(new MouseEvent('click', { bubbles: true })); })()`); await Bun.sleep(500); }
await Bun.sleep(600);
const r: any = await view.cdp("Page.captureScreenshot", { format: "png" });
await Bun.write(`${OUT}/${slug}-${n}-ketuk.png`, Buffer.from(r.data, "base64")); view.close(); process.exit(0);
