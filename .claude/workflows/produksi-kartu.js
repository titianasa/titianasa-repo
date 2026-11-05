export const meta = {
  name: 'produksi-kartu',
  description: 'Satu putaran produksi deck kartu: 6 penulis paralel, tiap hasil diperiksa pemeriksa independen, lalu digabung dan diuji',
  whenToUse: 'Produksi massal deck Titian (agent/docs/puzzle-pengetahuan/produksi-massal-kartu.md). Args opsional: {agen: 6, isi: 4, tingkat: "k1,k2"}',
  phases: [
    { title: 'Antrean', detail: 'ambil tugas putaran berikutnya dari antrian-produksi.ts' },
    { title: 'Tulis', detail: 'satu penulis per tugas, menulis berkasnya sendiri di produksi/' },
    { title: 'Periksa', detail: 'pemeriksa independen per tugas, membetulkan di berkas yang sama' },
    { title: 'Gabung', detail: 'indeks, tsc, gerbang, uji muat dan galat browser, ekspor deck, seed' },
  ],
}

const ALR = '/home/john/Dev/sanja-workspace/alr'
const WEB = `${ALR}/titian-web`
const DOC = `${ALR}/agent/docs/puzzle-pengetahuan`
const agen = (args && args.agen) || 6
const isi = (args && args.isi) || 4
const tingkat = (args && args.tingkat) || ''

const TUGAS = {
  type: 'object',
  properties: {
    tugas: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          berkas: { type: 'string' },
          tingkat: { type: 'string' },
          kategori: { type: 'string' },
          item: {
            type: 'array',
            items: {
              type: 'object',
              properties: { jenis: { type: 'string' }, slug: { type: 'string' }, unit: { type: 'string' } },
              required: ['jenis', 'unit'],
            },
          },
        },
        required: ['id', 'berkas', 'tingkat', 'item'],
      },
    },
  },
  required: ['tugas'],
}
const LAPORAN_TULIS = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    deck: {
      type: 'array',
      items: {
        type: 'object',
        properties: { slug: { type: 'string' }, jenis: { type: 'string' }, lolosGerbang: { type: 'boolean' }, ragu: { type: 'string' } },
        required: ['slug', 'jenis', 'lolosGerbang'],
      },
    },
    kebutuhan: { type: 'array', items: { type: 'string' } },
  },
  required: ['id', 'deck', 'kebutuhan'],
}
const LAPORAN_PERIKSA = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    temuan: {
      type: 'array',
      items: {
        type: 'object',
        properties: { slug: { type: 'string' }, kartu: { type: 'string' }, masalah: { type: 'string' }, perbaikan: { type: 'string' } },
        required: ['slug', 'masalah', 'perbaikan'],
      },
    },
    semuaLolos: { type: 'boolean' },
  },
  required: ['id', 'temuan', 'semuaLolos'],
}
const LAPORAN_GABUNG = {
  type: 'object',
  properties: {
    tsc: { type: 'string' },
    gerbang: { type: 'string' },
    muat: { type: 'string' },
    galat: { type: 'string' },
    seed: { type: 'string' },
    catatan: { type: 'array', items: { type: 'string' } },
  },
  required: ['tsc', 'gerbang', 'muat', 'galat', 'seed', 'catatan'],
}

phase('Antrean')
const antre = await agent(
  `Di ${WEB}, jalankan \`bun scripts/antrian-produksi.ts --putaran --json --agen ${agen} --isi ${isi}${tingkat ? ` --tingkat ${tingkat}` : ''}\` dan kembalikan isinya persis sebagai daftar tugas (field id, berkas, tingkat, kategori, item[jenis, slug, unit]). Jangan mengubah berkas apa pun.`,
  { label: 'antrean', phase: 'Antrean', schema: TUGAS, effort: 'low' },
)
const tugas = (antre && antre.tugas) || []
if (!tugas.length) {
  log('Antrean kosong: semua deck sudah berstandar dan lolos gerbang.')
  return { tugas: [], selesai: true }
}
log(`${tugas.length} tugas, ${tugas.reduce((a, t) => a + t.item.length, 0)} deck`)

const daftar = (t) =>
  t.item.map((i) => `- ${i.jenis}: ${i.slug ? `deck \`${i.slug}\`` : `unit \`${i.unit}\` (deck baru)`}`).join('\n')

const hasil = await pipeline(
  tugas,
  (t) =>
    agent(
      `Kamu penulis deck kartu Titian. Baca dan ikuti ${DOC}/brief-penulis.md sepenuhnya.

Tugas \`${t.id}\` (tingkat ${t.tingkat}, ${t.kategori || ''}). Satu-satunya berkas yang boleh kamu tulis: ${WEB}/${t.berkas}
Deck:
${daftar(t)}

Untuk setiap deck jalankan spesifikasinya (\`bun scripts/spek-deck.ts ...\` di ${WEB}), tulis deck sampai standar penuh, jalankan susun-produksi, tsc, dan periksa-kartu sampai lolos. Kembalikan laporan per deck.`,
      { label: `tulis:${t.id}`, phase: 'Tulis', schema: LAPORAN_TULIS },
    ),
  (tulis, t) =>
    agent(
      `Kamu pemeriksa deck kartu Titian. Baca dan ikuti ${DOC}/brief-pemeriksa.md sepenuhnya.

Periksa berkas ${WEB}/${t.berkas} (tugas \`${t.id}\`, tingkat ${t.tingkat}). Deck di dalamnya:
${daftar(t)}
${tulis ? `Catatan penulis yang perlu dicek khusus: ${JSON.stringify(tulis.deck.filter((d) => d.ragu || !d.lolosGerbang))}` : 'Penulis tidak melapor: periksa apakah berkasnya ada dan lengkap; kalau tidak ada, laporkan saja.'}

Betulkan langsung di berkas itu, jalankan tsc dan periksa-kartu sampai lolos, lalu kembalikan temuan dan perbaikan.`,
      { label: `periksa:${t.id}`, phase: 'Periksa', schema: LAPORAN_PERIKSA },
    ).then((p) => ({ tugas: t, tulis, periksa: p })),
)

phase('Gabung')
const slugs = hasil
  .filter(Boolean)
  .flatMap((h) => (h.tulis ? h.tulis.deck.map((d) => d.slug) : []))
const gabung = await agent(
  `Kamu penggabung putaran produksi kartu Titian. Kerjakan di ${WEB}, berurutan:
1. \`bun scripts/susun-produksi.ts\` lalu \`bunx tsc --noEmit -p .\`. Kalau ada galat di berkas produksi/, betulkan seminimal mungkin di berkas itu.
2. \`bun scripts/periksa-kartu.ts ${slugs.join(' ')}\`, lalu catat yang belum lolos.
3. Pastikan server web dev menyala di port 3010 (\`ss -ltn | grep 3010\`). Kalau mati, nyalakan dengan \`setsid nohup bun run dev -- -p 3010 > /home/john/.cache/titian-qa-tmp/web-3010.log 2>&1 < /dev/null & disown\` dan tunggu sampai halaman /puzzle-kartu/<slug> mengembalikan 200.
4. Dari folder /home/john/.cache/titian-qa-tmp/scratch (bukan dari repo), jalankan \`bun ${ALR}/agent/tools/qa/kartu/fit.ts ${slugs.join(',')}\` (harus "NO OVERFLOW"), lalu \`bun ${ALR}/agent/tools/qa/kartu/isu.ts\` untuk setiap kartu lab dan figure deck-deck itu (format slug:nomor, kartu pertama = 2; harus "0 issue"). Hapus folder .*bun-chrome yang tertinggal di folder itu.
5. \`bun scripts/export-decks.ts\`, lalu di ${ALR}/titian-backend-go \`python3 -I data/kanonik/build.py\`.
Jangan commit dan jangan deploy. Kembalikan ringkasan setiap langkah dan catatan masalah yang belum selesai.`,
  { label: 'gabung', phase: 'Gabung', schema: LAPORAN_GABUNG },
)

return {
  tugas: hasil.filter(Boolean).map((h) => ({
    id: h.tugas.id,
    deck: h.tulis ? h.tulis.deck : null,
    kebutuhan: h.tulis ? h.tulis.kebutuhan : [],
    temuanPemeriksa: h.periksa ? h.periksa.temuan.length : null,
    lolos: h.periksa ? h.periksa.semuaLolos : false,
  })),
  gagal: tugas.length - hasil.filter(Boolean).length,
  gabung,
}
