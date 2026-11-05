/**
 * Renders motion.html frame by frame (same idea as game/scripts/video: the browser is seeked, not played, so the
 * clip is exact) and cuts the 60-second, 1,800-frame clip with the narration. No music bed.
 *
 *   bun render.ts [--subs]   → ../../video/titian-asa-perkenalan-v1.mp4
 */
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { openView } from "/home/john/Dev/sanja-workspace/alr/agent/tools/qa/webview.ts";
import { SCRIPT } from "./narr";

const DIR = import.meta.dir;
const WORK = process.env.VIDEO_WORK ?? "/tmp/titian-video";
const FPS = 30, TOTAL = 60, LEAD = 0.45;
const secs: number[] = JSON.parse(readFileSync(`${DIR}/audio/narr.json`, "utf8"));
// each scene lasts its sentence plus an equal share of the spare time; the closing scene keeps a longer hold
const spare = TOTAL - secs.reduce((a, b) => a + b, 0);
const share = (spare - 1.5) / secs.length;
const frames = secs.map((s, i) => Math.round((s + share + (i === secs.length - 1 ? 1.5 : 0)) * FPS));
frames[frames.length - 1] += TOTAL * FPS - frames.reduce((a, b) => a + b, 0);
const starts = frames.map((_, i) => frames.slice(0, i).reduce((a, b) => a + b, 0) / FPS);
const subs = process.argv.includes("--subs");
const TL = { starts, total: TOTAL, caps: subs ? SCRIPT.map((l) => l.text) : [], capAt: starts.map((s) => s + LEAD), capEnd: starts.map((s, i) => s + LEAD + secs[i] + 0.3) };
console.log(starts.map((s, i) => `${s.toFixed(2)}s +${(frames[i] / FPS).toFixed(2)} (voice ${secs[i]})`).join("\n"));

mkdirSync(`${WORK}/frames`, { recursive: true });
const view = openView(1080, 1920);
await view.navigate("about:blank");
await view.cdp("Emulation.setDeviceMetricsOverride", { width: 1080, height: 1920, deviceScaleFactor: 1, mobile: false });
await view.cdp("Page.addScriptToEvaluateOnNewDocument", { source: `window.RENDER = true; window.TL = ${JSON.stringify(TL)};` });
await view.navigate(`file://${DIR}/motion.html`);
await view.evaluate(`Promise.all([document.fonts.ready, ...[...document.images].map((i) => i.decode().catch(() => {}))]).then(() => true)`);
await Bun.sleep(1500);
console.log("fonts:", await view.evaluate(`["Fredoka","Nunito","Caveat"].map((f) => f + "=" + document.fonts.check("700 20px " + f)).join(" ")`));
const only = process.env.FRAMES?.split(",").map(Number); // a few stills for review
for (let f = 0; f < TOTAL * FPS; f++) {
  if (only && !only.includes(f)) continue;
  await view.evaluate(`window.seek(${f / FPS})`);
  const { data } = await view.cdp<{ data: string }>("Page.captureScreenshot", { format: "jpeg", quality: 92 });
  await Bun.write(`${WORK}/frames/${String(f).padStart(5, "0")}.jpg`, Buffer.from(data, "base64"));
  if (f % 300 === 0) console.log("frame", f);
}
if (only) process.exit(0);

const out = `${DIR}/../../video/titian-asa-perkenalan-v1${subs ? "-teks" : ""}.mp4`;
const ins = secs.flatMap((_, i) => ["-i", `${DIR}/audio/narr${i}.mp3`]);
const filt = secs.map((_, i) => `[${i + 1}:a]aresample=44100,adelay=${Math.round((starts[i] + LEAD) * 1000)}:all=1[a${i}]`);
filt.push(`${secs.map((_, i) => `[a${i}]`).join("")}amix=inputs=${secs.length}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100,apad=whole_dur=${TOTAL},atrim=0:${TOTAL}[a]`);
await Bun.$`ffmpeg -loglevel error -y -threads 2 -framerate ${FPS} -i ${WORK}/frames/%05d.jpg ${ins} -filter_complex ${filt.join(";")} -map 0:v -map [a] -frames:v ${TOTAL * FPS} -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ac 2 -t ${TOTAL} -movflags +faststart ${out}`;
writeFileSync(`${DIR}/timeline.json`, JSON.stringify({ starts, frames, secs }, null, 2));
console.log(out, (await Bun.$`ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames,width,height:format=duration -of default=nw=1 ${out}`.text()).trim().replace(/\n/g, " "));
process.exit(0);
