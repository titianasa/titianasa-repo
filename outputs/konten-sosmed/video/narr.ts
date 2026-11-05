/**
 * Narration of the Titian Asa introduction clip, same method as game/scripts/video/basic-audio.ts: ElevenLabs
 * `eleven_v3`, the owner's narrator "Citra", several takes per line, each checked by the listening model.
 *
 *   bun narr.ts [n …]      → audio/narr<n>.mp3 and audio/narr.json (seconds each)
 */
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { listen } from "/home/john/Dev/sanja-workspace/alr/game/scripts/audio/lib";

const DIR = import.meta.dir + "/audio";
const KEY = readFileSync("/home/john/Dev/sanja-workspace/alr/game/.env.local", "utf8").match(/^ELEVEN_LABS_API_KEY=(.*)$/m)?.[1]?.trim().replace(/^["']|["']$/g, "");
if (!KEY) throw new Error("ELEVEN_LABS_API_KEY is not set in game/.env.local");
const NARRATOR = "RbNgJzKAV7jpYJNtCBpj"; // "Citra"
const MODEL = "eleven_v3";

/** One line per scene. `say` is what the voice reads when it differs from the caption (the web address). */
export const SCRIPT: { text: string; tag: string; say?: string }[] = [
  { tag: "[excited]", text: "Halo! Kenalin, kami Titian Asa." },
  { tag: "[warm]", text: "Titian itu jembatan, asa itu harapan. Kami percaya, semua asa pasti ada jalannya." },
  { tag: "[cheerful]", text: "Di sini, kamu belajar sampai bisa dan terbiasa. Yang salah diulang, sampai benar-benar paham." },
  { tag: "[excited]", text: "Dan sekarang, Kampung Bahasa Pare sudah buka!" },
  { tag: "[cheerful]", text: "Belajar lima bahasa: Inggris, Mandarin, Arab, Jepang, dan Korea." },
  { tag: "[playful]", text: "Ikut kelas, jalani misi bareng warga, dan ngobrol sama teman belajar." },
  { tag: "[curious]", text: "Segera hadir juga: ruang belajar, persiapan TKA dan SNBT, tryout, sampai tes bahasa Inggris internasional.", say: "Segera hadir juga: ruang belajar, persiapan T K A dan S N B T, tryout, sampai tes bahasa Inggris internasional." },
  { tag: "[warm]", text: "Gratis, langsung dari browser. Yuk, mulai belajar di titianasa.com!", say: "Gratis, langsung dari browser. Yuk, mulai belajar di Titian Asa, dot com!" },
];

async function tts(text: string): Promise<Uint8Array> {
  for (let i = 1; ; i++) {
    const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${NARRATOR}?output_format=mp3_44100_128`, {
      method: "POST",
      headers: { "xi-api-key": KEY!, "Content-Type": "application/json" },
      body: JSON.stringify({ text, model_id: MODEL, language_code: "id", voice_settings: { stability: 0.5, similarity_boost: 0.8, style: 0.3, use_speaker_boost: true } }),
    }).catch(() => null);
    if (r?.ok) return new Uint8Array(await r.arrayBuffer());
    const msg = r ? `${r.status}: ${(await r.text()).slice(0, 300)}` : "no connection";
    if (i >= 4 || (r && r.status < 500 && r.status !== 429)) throw new Error(`elevenlabs ${msg}`);
    await Bun.sleep(2000 * i);
  }
}
const seconds = async (f: string) => Number((await Bun.$`ffprobe -v error -show_entries format=duration -of csv=p=0 ${f}`.text()).trim());
const fold = (s: string) => s.toLowerCase().replace(/\[[^\]]*\]/g, "").replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
function match(want: string, got: string) {
  const a = fold(want).split(" "), b = fold(got).split(" ");
  let j = 0, hit = 0;
  for (const w of a) { const k = b.indexOf(w, j); if (k >= 0) { hit++; j = k + 1; } }
  return hit / a.length;
}

const only = process.argv.slice(2).map(Number);
const secs: number[] = existsSync(`${DIR}/narr.json`) ? JSON.parse(readFileSync(`${DIR}/narr.json`, "utf8")) : [];
for (const [i, line] of SCRIPT.entries()) {
  if (only.length ? !only.includes(i) : existsSync(`${DIR}/narr${i}.mp3`)) continue;
  const spoken = line.say ?? line.text;
  const takes: { n: number; sec: number; score: number; heard: string }[] = [];
  for (let n = 0; n < 3; n++) {
    const file = `${DIR}/takes/${i}-${n}.mp3`;
    writeFileSync(file, await tts(`${line.tag} ${spoken}`));
    const wav = new Uint8Array(await Bun.$`ffmpeg -loglevel error -i ${file} -ac 1 -ar 24000 -f wav -`.arrayBuffer());
    const v = await listen("id (Indonesian)", spoken, wav);
    takes.push({ n, sec: await seconds(file), score: v.ok ? 1 : match(spoken, String(v.heard ?? "")), heard: String(v.heard ?? "") });
  }
  // a take that says the whole line; of those, the middle one in length (neither rushed nor dragging)
  const said = takes.filter((t) => t.score >= 0.9).sort((a, b) => a.sec - b.sec);
  const pick = said[Math.floor((said.length - 1) / 2)];
  if (!pick) throw new Error(`line ${i}: no take said the text (${takes.map((t) => `${t.score.toFixed(2)} "${t.heard}"`).join(" | ")})`);
  writeFileSync(`${DIR}/narr${i}.mp3`, readFileSync(`${DIR}/takes/${i}-${pick.n}.mp3`));
  secs[i] = Math.round(pick.sec * 100) / 100;
  console.log(i, `take ${pick.n + 1}`, `${pick.sec.toFixed(2)} s`, "·", takes.map((t) => `${t.sec.toFixed(1)}s/${t.score.toFixed(2)}`).join(" "), "·", line.text);
}
writeFileSync(`${DIR}/narr.json`, JSON.stringify(secs));
console.log("total speech", secs.reduce((a, b) => a + b, 0).toFixed(1), "s");
