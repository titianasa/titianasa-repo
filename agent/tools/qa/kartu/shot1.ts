import { openView } from "../webview.ts";
const [slug, n] = process.argv.slice(2);
const view = openView(540, 960);
const WEB = process.env.WEB ?? "http://localhost:3010"; const OUT = process.env.OUT ?? "shots";
await view.navigate(`${WEB}/puzzle-kartu/${slug}?kartu=${n}&rasio=9x16${process.env.MODE === "web" ? "&web" : ""}`); await Bun.sleep(2500);
const r: any = await view.cdp("Page.captureScreenshot", { format: "png" });
await Bun.write(`${OUT}/${slug}-${n}.png`, Buffer.from(r.data, "base64")); view.close(); process.exit(0);
