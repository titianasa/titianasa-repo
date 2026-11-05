// Memeriksa slide yang isinya meluap (teks menabrak footer atau keluar dari kanvas). Jalankan: bun check.ts
import { openView } from "/home/john/Dev/sanja-workspace/alr/agent/tools/qa/webview.ts";
const dir = import.meta.dir;
for (const ratio of ["ig", "tiktok"]) {
  const view = openView(1200, 1000);
  await view.navigate(`file://${dir}/preview-${ratio}.html`);
  await view.evaluate(`document.fonts.ready.then(() => true)`);
  await Bun.sleep(2000);
  const bad = await view.evaluate<string[]>(`(() => {
    const out = [];
    for (const s of document.querySelectorAll(".slide")) {
      const sr = s.getBoundingClientRect(), f = s.querySelector("footer").getBoundingClientRect(), c = s.querySelector(".copy").getBoundingClientRect(), h = s.querySelector("header").getBoundingClientRect();
      const m = s.querySelector("main"); const ph = s.querySelector(".phone");
      const lowest = Math.max(c.bottom, ph ? ph.getBoundingClientRect().bottom : 0);
      const overFooter = lowest - f.top, overTop = h.bottom - c.top;
      if (overFooter > -8 || overTop > 0 || m.scrollHeight > m.clientHeight + 2) out.push(s.id + " footer:" + Math.round(overFooter) + " top:" + Math.round(overTop));
    }
    return out;
  })()`);
  console.log(ratio, bad.length ? bad.join("\n  ") : "semua muat");
}
process.exit(0);
