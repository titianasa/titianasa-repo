// Counts the Next.js dev issue badge on a card: 0 means no console error or hydration mismatch.
import { openView } from "../webview.ts";
const view = openView(540, 960);
for (const [slug, n] of process.argv.slice(2).map((a) => a.split(":"))) {
  await view.navigate(`${process.env.WEB ?? "http://localhost:3010"}/puzzle-kartu/${slug}?kartu=${n}&rasio=9x16&web`); await Bun.sleep(5000);
  const t = await view.evaluate<string>(`(() => { const p = document.querySelector('nextjs-portal'); const s = p?.shadowRoot; if (!s) return 'tanpa portal'; const b = [...s.querySelectorAll('*')].map(e => e.textContent ?? '').find(x => /\\d+ Issues?$/.test(x.trim())); return b ? b.trim() : '0 issue'; })()`);
  console.log(slug, n, t);
}
view.close(); process.exit(0);
