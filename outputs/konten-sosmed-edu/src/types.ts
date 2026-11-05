export type Slide = {
  bg?: "cream" | "yellow" | "navy" | "soft";
  kicker?: string;
  title: string; // <a>..</a> = kata beraksen
  body?: string;
  note?: string; // catatan tulisan tangan
  dense?: boolean; // judul lebih kecil, untuk slide padat
  tight?: boolean; // lebih rapat lagi (6 butir atau lebih)
  phone?: string;
  items?: { e: string; t: string; d?: string }[];
  steps?: { w: string; t: string; d?: string; hot?: boolean; done?: boolean }[]; // garis waktu: w = chip tanggal
  checks?: (string | { t: string; d?: string })[];
  xs?: boolean; // checks ditampilkan sebagai tanda silang (yang jangan dilakukan)
  stats?: { n: string; l: string }[];
  cmp?: [{ h: string; rows: (string | { t: string; d?: string })[] }, { h: string; rows: (string | { t: string; d?: string })[] }];
  src?: string; // baris kecil sumber / catatan "cek resmi"
  tag?: string;
  cta?: boolean;
  hand?: string; // teks tulisan tangan di atas alamat web saat cta (bawaan: "belajar gratis di")
};
export type Post = { id: string; name: string; slides: Slide[] };
