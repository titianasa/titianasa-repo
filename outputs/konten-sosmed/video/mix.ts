/**
 * Adds the music bed under the narration of the finished clip (video stream copied, nothing re-rendered): the music
 * ducks under the voice, fades in and out. Needs timeline.json from render.ts and audio/bgm.mp3 from music.ts.
 *
 *   bun mix.ts      → ../../video/titian-asa-perkenalan-v2-musik.mp4
 */
import { readFileSync } from "node:fs";
const DIR = import.meta.dir, TOTAL = 60, LEAD = 0.45;
const { starts, secs }: { starts: number[]; secs: number[] } = JSON.parse(readFileSync(`${DIR}/timeline.json`, "utf8"));
const src = `${DIR}/../../video/titian-asa-perkenalan-v1.mp4`, out = `${DIR}/../../video/titian-asa-perkenalan-v2-musik.mp4`;
const ins = secs.flatMap((_, i) => ["-i", `${DIR}/audio/narr${i}.mp3`]);
const filt = secs.map((_, i) => `[${i + 1}:a]aresample=44100,adelay=${Math.round((starts[i] + LEAD) * 1000)}:all=1[a${i}]`);
const m = secs.length + 1;
filt.push(`${secs.map((_, i) => `[a${i}]`).join("")}amix=inputs=${secs.length}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100,apad=whole_dur=${TOTAL},asplit=2[vo][key]`);
filt.push(`[${m}:a]aresample=44100,atrim=0:${TOTAL},afade=t=in:d=0.4,afade=t=out:st=${TOTAL - 2}:d=2,volume=0.30[mu]`);
filt.push(`[mu][key]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[mud]`);
filt.push(`[vo][mud]amix=inputs=2:normalize=0,alimiter=limit=0.89,atrim=0:${TOTAL}[a]`);
await Bun.$`ffmpeg -loglevel error -y -i ${src} ${ins} -i ${DIR}/audio/bgm.mp3 -filter_complex ${filt.join(";")} -map 0:v -map [a] -c:v copy -c:a aac -b:a 192k -ac 2 -t ${TOTAL} -movflags +faststart ${out}`;
console.log(out, (await Bun.$`ffprobe -v error -show_entries format=duration -of csv=p=0 ${out}`.text()).trim(), "s");
