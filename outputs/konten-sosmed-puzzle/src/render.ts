// Films every card of Titian Asa in both sizes, 4:5 and 9:16, into MP4 and PNG: the missions' explanation cards and the
// decks of ADR-0025. Needs titian-web running on :3000.
//   bun render.ts                  all cards, skipping the ones already done
//   bun render.ts noun-pengertian  only these sets
// The cards are CSS loops, so each frame is set exactly (document.getAnimations) instead of recorded in real time. A
// long card (data-loop) is an exercise: its question, then its answer, and its PNG shows the answer.
// Output: ../<size>/<slug>/NN.{mp4,png} plus semua-mp4.zip and semua-png.zip; the app's Bagikan sheet uses copies in
// titian-web/public/kartu-media/<slug>/<size>.
import { $ } from "bun";
import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync } from "node:fs";
import { openView } from "/home/john/Dev/sanja-workspace/alr/agent/tools/qa/webview.ts";
import { DECKS } from "/home/john/Dev/sanja-workspace/alr/titian-web/src/content/kartu/index.ts";

const dir = import.meta.dir;
const WEB = "http://localhost:3000";
const PUBLIC = "/home/john/Dev/sanja-workspace/alr/titian-web/public/kartu-media";
const FPS = 10;
const SIZES = [
  { name: "4x5", width: 1080, height: 1350 },
  { name: "9x16", width: 1080, height: 1920 },
];
const missions: Record<string, { aha: unknown[] }> = await Bun.file("/home/john/Dev/sanja-workspace/alr/titian-web/src/content/puzzle-kartu.json").json();
const counts = { ...Object.fromEntries(Object.entries(missions).map(([slug, m]) => [slug, m.aha.length + 2])), ...Object.fromEntries(Object.entries(DECKS).map(([slug, d]) => [slug, d.cards.length + 1])) };
const only = process.argv.slice(2);
const sets = Object.entries(counts).filter(([slug]) => !only.length || only.includes(slug));

const view = openView(1080, 1350);
await view.navigate(`${WEB}/login`);

for (const size of SIZES) {
  await view.cdp("Emulation.setDeviceMetricsOverride", { width: size.width, height: size.height, deviceScaleFactor: 1, mobile: false });
  const clip = { x: 0, y: 0, width: size.width, height: size.height, scale: 1 };
  for (const [slug, total] of sets) {
    const out = `${dir}/../${size.name}/${slug}`;
    const pub = `${PUBLIC}/${slug}/${size.name}`;
    mkdirSync(out, { recursive: true });
    mkdirSync(pub, { recursive: true });
    for (let n = 1; n <= total; n++) {
      const name = String(n).padStart(2, "0");
      if (existsSync(`${out}/${name}.mp4`)) continue;
      await view.navigate(`${WEB}/puzzle-kartu/${slug}?kartu=${n}&rasio=${size.name}`);
      for (let t = 0; t < 120; t++) {
        if (await view.evaluate<boolean>(`!!document.querySelector("#kartu .pz-card") && document.fonts.status === "loaded"`).catch(() => false)) break;
        await Bun.sleep(250);
      }
      await view.evaluate(`document.fonts.ready.then(() => true)`);
      await view.evaluate(`(() => { const s = document.createElement("style"); s.textContent = "nextjs-portal,.tsqd-parent-container,[data-next-badge-root]{display:none!important} html,body{margin:0;overflow:hidden!important}"; document.head.append(s); })()`);
      await Bun.sleep(400);
      const LOOP = Number(await view.evaluate<string>(`document.querySelector("#kartu .pz-card").dataset.loop`));
      const FRAMES = (LOOP / 1000) * FPS;
      const frames = `${out}/.f${name}`;
      mkdirSync(frames, { recursive: true });
      const set_t = (t: number) => view.evaluate(`document.getAnimations().forEach((a) => { a.pause(); a.currentTime = ${t} + (a.effect.getTiming().delay || 0); })`);
      for (let f = 0; f < FRAMES; f++) {
        await set_t((f / FRAMES) * LOOP);
        const { data } = await view.cdp<{ data: string }>("Page.captureScreenshot", { format: "jpeg", quality: 95, clip });
        await Bun.write(`${frames}/${String(f).padStart(2, "0")}.jpg`, Buffer.from(data, "base64"));
      }
      await set_t(LOOP > 3200 ? LOOP * 0.75 : LOOP * 0.4);
      const still = await view.cdp<{ data: string }>("Page.captureScreenshot", { format: "png", clip });
      await Bun.write(`${out}/${name}.png`, Buffer.from(still.data, "base64"));
      await $`ffmpeg -y -loglevel error -framerate ${FPS} -i ${frames}/%02d.jpg -vf fps=30,format=yuv420p -c:v libx264 -crf 22 -movflags +faststart ${out}/${name}.mp4`;
      copyFileSync(`${out}/${name}.mp4`, `${pub}/${name}.mp4`);
      copyFileSync(`${out}/${name}.png`, `${pub}/${name}.png`);
      rmSync(frames, { recursive: true });
      console.log(`${size.name} ${slug} ${name}`);
    }
    for (const ext of ["mp4", "png"]) {
      const zip = `${pub}/semua-${ext}.zip`;
      rmSync(zip, { force: true });
      const files = readdirSync(out).filter((f) => f.endsWith(`.${ext}`)).map((f) => `${out}/${f}`);
      await $`zip -q -j ${zip} ${files}`;
    }
  }
}
view.close();
process.exit(0);
