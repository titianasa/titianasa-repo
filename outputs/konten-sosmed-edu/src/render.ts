// Exports every slide of preview-*.html to PNG. Run after build.ts: bun render.ts
import { openView } from "/home/john/Dev/sanja-workspace/alr/agent/tools/qa/webview.ts";
const dir = import.meta.dir;
const posts: { id: string; name: string; slides: number }[] = await Bun.file(dir + "/manifest.json").json();
for (const [ratio, out, h] of [["ig", "instagram", 1350], ["tiktok", "tiktok", 1920]] as const) {
  const view = openView(1200, 1000);
  await view.navigate(`file://${dir}/preview-${ratio}.html`);
  await view.evaluate(`document.fonts.ready.then(() => true)`);
  await Bun.sleep(2500);
  console.log(ratio, "fonts:", await view.evaluate(`["Fredoka","Nunito","Caveat"].map(f => f + "=" + document.fonts.check("700 20px " + f)).join(" ")`));
  for (const p of posts.filter((q) => !process.env.ONLY || process.env.ONLY.split(",").includes(q.id))) for (let i = 1; i <= p.slides; i++) {
    const box = await view.evaluate<{ x: number; y: number }>(`(() => { const r = document.getElementById("p${p.id}-s${i}").getBoundingClientRect(); return { x: r.x + scrollX, y: r.y + scrollY }; })()`);
    const { data } = await view.cdp<{ data: string }>("Page.captureScreenshot", { format: "png", captureBeyondViewport: true, clip: { x: box.x, y: box.y, width: 1080, height: h, scale: 1 } });
    const file = p.slides > 1 ? `${p.id}-${p.name}/${p.id}-${i}.png` : `${p.id}-${p.name}.png`;
    await Bun.write(`${dir}/../${out}/${file}`, Buffer.from(data, "base64"));
  }
}
process.exit(0);
