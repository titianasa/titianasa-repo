/**
 * Music bed for the Titian Asa introduction clip, made by `google/lyria-3-pro-preview` through OpenRouter (same method
 * as game/scripts/video/music.ts: one request, the audio comes back as base64 pieces in the stream).
 *
 *   bun music.ts      → audio/bgm.<ext>
 */
import { writeFileSync } from "node:fs";
import { envVar, spend } from "/home/john/Dev/sanja-workspace/alr/game/scripts/audio/lib";

const MODEL = "google/lyria-3-pro-preview";
const PROMPT =
  "Instrumental only, no vocals, no lyrics. About 60 seconds. A warm, joyful and friendly acoustic-pop track for a one-minute introduction video of a learning platform for Indonesian students and young adults: bright ukulele strumming, playful marimba and glockenspiel melody, soft hand claps and finger snaps, light bass, a gentle upbeat groove around 110 BPM. Optimistic, hopeful, cosy and modern. It starts right away without a long intro, stays light enough to sit under a narrator's voice, lifts a little in the middle, and ends on a clear, happy final chord at the very end.";

const before = await spend();
const r = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: { Authorization: `Bearer ${envVar("OPENROUTER_KEY_PARE")}`, "Content-Type": "application/json" },
  body: JSON.stringify({ model: MODEL, modalities: ["audio", "text"], stream: true, messages: [{ role: "user", content: PROMPT }] }),
});
if (!r.ok || !r.body) throw new Error(`${r.status} ${(await r.text()).slice(0, 400)}`);
let audio = "", said = "", format = "", buf = "";
const dec = new TextDecoder();
for await (const chunk of r.body as unknown as AsyncIterable<Uint8Array>) {
  buf += dec.decode(chunk, { stream: true });
  let nl: number;
  while ((nl = buf.indexOf("\n")) >= 0) {
    const line = buf.slice(0, nl).trim();
    buf = buf.slice(nl + 1);
    if (!line.startsWith("data:") || line === "data: [DONE]") continue;
    const j = JSON.parse(line.slice(5));
    if (j.error) throw new Error(JSON.stringify(j.error).slice(0, 300));
    const d = j.choices?.[0]?.delta ?? {};
    if (typeof d.content === "string") said += d.content;
    if (d.audio?.data) audio += d.audio.data;
    if (d.audio?.format) format = d.audio.format;
  }
}
if (!audio) throw new Error(`no audio in the answer (text: ${said.slice(0, 200)})`);
const bytes = Buffer.from(audio, "base64");
const head = bytes.subarray(0, 4).toString("latin1");
const ext = head.startsWith("ID3") || (bytes[0] === 0xff && (bytes[1] & 0xe0) === 0xe0) ? "mp3" : head === "RIFF" ? "wav" : head === "OggS" ? "ogg" : head === "fLaC" ? "flac" : format || "pcm";
const file = `${import.meta.dir}/audio/bgm.${ext}`;
writeFileSync(file, bytes);
console.log(file, `${(bytes.length / 1024).toFixed(0)} kB`, (await Bun.$`ffprobe -v error -show_entries format=duration -of csv=p=0 ${file}`.text()).trim(), "s", `· OpenRouter spend $${((await spend()) - before).toFixed(4)}`);
