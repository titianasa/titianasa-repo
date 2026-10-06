// Membaca JSON array string LaTeX dari stdin, mencetak yang gagal dirender KaTeX (opsi sama dengan tampilan aplikasi).
import { createRequire } from "module";
const require = createRequire("/home/john/Dev/sanja-workspace/alr/titian-web/package.json");
const katex = require("katex");
const items = JSON.parse(await new Promise(r => { let s = ""; process.stdin.on("data", d => s += d); process.stdin.on("end", () => r(s)); }));
const bad = [];
for (const it of items) {
  try { katex.renderToString(it.latex, { throwOnError: true, displayMode: it.display, strict: "error", output: "htmlAndMathml" }); }
  catch (e) { bad.push({ where: it.where, latex: it.latex, error: String(e.message).slice(0, 120) }); }
}
console.log(JSON.stringify(bad));
