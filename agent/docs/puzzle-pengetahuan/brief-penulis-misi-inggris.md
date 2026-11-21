# Brief penulis misi Bahasa Inggris

Brief ini untuk agen yang menulis misi Bahasa Inggris dari deck kartu kanonik (ADR-0028, sampai A2). Satu agen menulis satu file batch di `titian-web/scripts/misi-inggris/` dan mendaftarkannya di `scripts/misi-inggris/index.ts`. File lain tidak disentuh, tidak ada commit, dan tidak ada tulis ke database.

## Baca dulu
- `agent/docs/puzzle-pengetahuan/temuan-misi.md`: masalah yang sudah pernah terjadi dan aturannya, termasuk bagian Bahasa Inggris. Jangan ulangi.
- `agent/docs/adr/0028-misi-bertema-di-atas-kartu-kanonik.md`: apa itu misi. `0026`: satu catatan pengetahuan, banyak jalur. `0030`: kartu jembatan.
- `titian-web/scripts/misi-inggris/pre-a1-a.ts` dan `pre-a1-b.ts`: contoh BAB, TEMA, SYARAT, KEMAMPUAN, KATA, dan NAMA yang sudah lolos.
- Tipe `Tema`, `Pakai`, `Kata`, dan semua pemeriksaan di `titian-web/scripts/misi-inggris.ts`.
- `titian-web/src/components/puzzle/pieces.ts`: daftar `POS` (part of speech) dan `ROLES` (keluarga kata) yang boleh dipakai di KATA. Tambahkan entri baru di sana kalau perlu, dengan istilah akademik bahasa Inggris dan padanan Indonesianya.
- Deck-nya sendiri, lewat `src/content/kartu/index.ts` (DECKS). Baca SETIAP kartu sampai habis. Daftar kartu materi beserta indeksnya:
  `cd titian-web && bun -e 'import { DECKS } from "./src/content/kartu/index.ts"; import { isExercise } from "./src/content/kartu/types.ts"; const d = DECKS["SLUG"]; d.cards.forEach((c, i) => { if (!isExercise(c)) console.log(i, c.t, (c as any).title) })'`

## Yang dilihat dan dikerjakan siswa
- **Tebak** (sebelum materi, gratis): soal dan tiga pilihan. Elemen keenam `say` membuatnya soal dengar: kalimat Inggris itu diputar, dan teksnya baru tampil kalau siswa menekan "Lihat teksnya".
- **Latihan rangkai** (`latihan`, [kalimat Inggris, arti Indonesia]): satu kalimat dikerjakan empat kali, berganti bentuk. Susun blok dengan bantuan pola, dengar lalu susun, susun sendiri, lalu **ketik tanpa bantuan dari arti Indonesianya**. Setiap blok berlabel part of speech dan arti dari KATA.
- **Pilih** (`pilih`): pilihan dengan alasan yang tampil sesudah menjawab. Dengan elemen keenam, pilih menjadi **dengar lalu pilih**.
- **Uji akhir**: isian (`isian`) diketik, lalu kalimat `pakai` dan `target` **diketik bebas** dari situasi Indonesianya, tanpa blok.
- Server menerima bentuk pendek dan panjang sebagai jawaban yang sama (I'm/I am, don't/do not, that's/that is, can't/cannot, we'll/we will, you've/you have), tanpa membedakan huruf besar, koma, titik koma, petik, dan tanda di tengah. 's dan 'd dibaca dari kata sesudahnya: He's gone = He has/is gone, He's a teacher = He is…, She's visited = She has…, I'd better = I had better (bukan I would), I'd like = I would like. Bentuk panjang yang benar tidak perlu ditulis sebagai bentuk lain. Selain itu jawaban harus kata yang sama dengan urutan yang sama, atau salah satu **bentuk lain** yang kamu tulis (lihat di bawah).
- Kalimat pernyataan dengan satu keterangan waktu di awal atau akhir (yesterday, today, every day, on Monday(s), last week, in the morning, at night, after school…) otomatis diterima dalam urutan sebaliknya bila sisa kalimatnya diawali subjek: "I was at home yesterday." juga menerima "Yesterday, I was at home.". Perintah dan pertanyaan tidak dipindah.

## Yang ditulis
- **BAB**: satu entri per deck {deck, key unik berawalan level (mis. `a1-tense-present`), title = judul deck dalam istilah akademik bahasa Inggris (mis. "Present Simple"), icon satu emoji}. Level diambil otomatis dari jalur CEFR: Pre-A1 = 0, A1 = 1, A2 = 2.
- **TEMA**: bagi tiap deck menjadi tema mengikuti urutan mengajar deck itu. Satu tema = satu misi. Biasanya 2 sampai 4 tema per deck, 3 sampai 9 kartu per tema. Setiap indeks kartu materi (termasuk kartu `ingat` dan `audio`) masuk tepat satu tema, urut naik. Isi tiap tema:
  - `id` unik global berawalan level: `pre-`, `a1-`, `a2-` (mis. `a1-present-rutin`). Jangan ganti id setelah diimpor.
  - `deck`, `judul` (bahasa Indonesia, istilah grammar tetap Inggris: "Present Simple untuk Kebiasaan"), `sub`, `kartu`, `tokoh` [nama Indonesia, satu emoji].
  - `cerita` (1–2 kalimat): situasi nyata di Indonesia yang diselesaikan dengan bahasa tema itu, cocok untuk pelajar SD sampai dewasa. Misinya diperankan: siswa memesan, mengeja, bertanya arah, mengenalkan teman, bukan "mengisi soal".
  - `tujuan`, `pola` (rumus singkat, mis. "I/you/we/they + V1 · he/she/it + V1-s").
  - Tepat 3 `tebak` [soal, benar, salah, salah, alasan] atau dengan elemen keenam [..., kalimat dengar].
  - `latihan`: 4 sampai 6 kalimat rangkai, 3 sampai 12 potongan. Ditambah `pilih` kalau perlu; total latihan + pilih minimal 4. Tema yang materinya tidak bisa dirangkai (nama huruf, bunyi, tekanan kata) boleh hanya pilih: `latihan: []`, `pakai: []`, `target: ["", ""]`, minimal 4 pilih.
  - `latihan` boleh punya elemen ketiga [kalimat, arti, [bentuk lain]]: dipakai hanya saat diketik, blok tetap menyusun kalimat utamanya.
  - `pakai`: minimal 2 kalimat uji [kalimat, situasi, catatan] atau dengan elemen keempat [..., [bentuk lain yang sama benar]]. `target`: [kalimat misi, artinya].
  - Minimal 3 `isian` [teks dengan ___, jawaban, penjelasan] atau dengan elemen keempat [..., [jawaban lain yang sama benar]].
  - `kapital: true` (opsional) untuk tema yang menguji huruf besar dan tanda baca: isian, latihan ketik, dan uji akhir tema itu dinilai peka kapital, koma, dan tanda akhir, dan pemain menampilkan "Perhatikan huruf besar dan tanda baca." Kalimat diketik lengkap dengan tanda akhirnya. Jawaban isian tema ini boleh memuat tanda baca. Keterangan waktu tidak dipindah otomatis di tema ini. Di tema `k34` dan tema `ubin: true`, isiannya disusun dari ubin huruf (lihat `brief-penulis-jenjang-inggris.md`), dan pengecohnya memuat versi kapital/kecil lain dan tanda akhir lain.
- **SYARAT**: id tema -> id tema yang langsung dibutuhkan. Di dalam deck, tiap tema sesudah yang pertama bersandar pada tema sebelumnya. Tema pertama deck bersandar pada tema deck prasyarat kanonik unitnya (`PRASYARAT` di `titian-backend-go/data/kanonik/bahasa_inggris.py`) yang sudah punya misi, biasanya tema terakhirnya. Jangan menambah prasyarat yang sudah tersirat. Batas rantai 12 per level.
- **KEMAMPUAN**: satu atau dua per deck {id unik berawalan level, title kegiatan nyata ("Memesan makan di warung"), sentence (satu kalimat Inggris yang menunjukkannya), needs (tema terakhir yang dibutuhkan)}.
- **KATA**: setiap kata di kalimat latihan, pakai, target, dan kemampuan harus sudah ada di KATA file mana pun. Cari dulu di file batch lain; jangan menulis kata dua kali. Format [kata huruf kecil, arti singkat, cara baca ala ejaan Indonesia seperti di deck (`SE-ven`, `dhis`), part of speech dari `POS`, keluarga dari `ROLES`]. Bentuk jamak dan -s biasa (books, likes) dikenali sendiri dari kata dasarnya. Bentuk tak beraturan ditulis di `BENTUK` ({ children: "child", went: "go" } atau sebagai kata sendiri bila maknanya perlu dipelajari terpisah, mis. `bought` sebagai verb-past). Bentuk pendek (I'm, don't, it's) adalah kata sendiri dengan part of speech `contraction`. Kata yang tidak dipakai kalimat mana pun ditolak.
- **NAMA**: nama orang, kota, bulan, hari, dan bahasa (Rina, Kediri, June, English, Mr) yang muncul berhuruf kapital di tengah kalimat. Nama tidak menjadi kepingan.
  - Nama berlaku hanya dengan huruf kapitalnya di tengah kalimat. "See you in May." = bulan, "You may go." = modal, jadi nama yang juga kata (May, March, Rose) aman. Di awal kalimat kapital tidak berarti apa-apa dan **kata yang menang**: "May I go?" = modal. Jangan memulai kalimat dengan nama yang juga kata ("In May, …" bukan "May is …").
  - `Rina's` otomatis dibaca Rina + 's (milik); cukup tulis `Rina` di NAMA. Entri lama seperti `Emma's` tetap boleh.
  - Kata berpola huruf kapital + tanda hubung (T-shirt, X-ray) adalah kata biasa: tulis `t-shirt` di KATA.
- **Kata berulang** ("five five", "very very") boleh; pemain menyediakan dua blok. Yang ditolak hanya salah ketik kata tugas (the the, a a, is is…).
- **Satu kata, beberapa makna** (homonim): kepingannya tetap satu (slug sama). Tambahkan elemen keenam di KATA: `[kata, arti, baca, pos, keluarga, [[frase, arti di frase itu, pos, keluarga], ...]]`, misalnya `["there", "di sana", "dhee", "adverb", "keterangan", [["there is", "ada", "expression", "sambung"], ["there are", "ada", "expression", "sambung"]]]`. Di kalimat yang memuat frase itu, blok dan anatomi kalimat memakai arti tersebut; di tempat lain arti utama. Frase huruf kecil tanpa tanda baca, memuat kata itu, dan harus dipakai di kalimat mana pun. Arti utama ditentukan pemilik entri; penulis lain mengusulkan arti tambahan ke pemilik file, bukan menulis kata dua kali.
- **Bentuk yang menunjuk dua kata** (leaves = jamak leaf atau verba leave): `BENTUK` tetap arti bawaan, lalu `BENTUK_FRASE: [["leaves", "leave", "leaves at"]]` membuat bentuk itu menunjuk kata lain di kalimat yang memuat frase tersebut.

## Bentuk latihan lain (opsional per tema)

Selain `latihan` dan `pilih`, tema boleh memuat enam bentuk berikut kalau materinya memang butuh. Tipe dan pemeriksaannya ada di `titian-web/scripts/misi-bentuk.ts` (dipakai juga oleh generator Matematika nanti). Pemain menjalankan bentuk ini sebagai satu putaran di awal Latihan, sebelum kalimat rangkai: tiap butir sekali, yang salah diulang sekali di akhir. Server yang menilai (`internal/grading/bentuk.go`), dan kunci baru sampai ke pemain sesudah menjawab. Bentuk ini tidak menggantikan syarat minimal latihan + pilih.

| Field | Dipakai untuk | Pemeriksaan generator |
|---|---|---|
| `pilah` | memilah 4–10 kata/frasa ke 2 atau 3 kelompok (noun/verb, is/has, /s/ /z/ /ɪz/) | kelompok berbeda dan tidak kosong, isi tidak kembar, isi bukan nama kelompoknya |
| `pasangan` | dengar satu kata, pilih di antara kata yang bunyinya mirip | pengecoh berbeda; kalimat dengar (bila ada) memuat kata benarnya dan tidak memuat pengecoh |
| `dikte` | dengar ejaan, email, nomor, tanggal, lalu ketik | jawaban hanya huruf, angka, `/ . @ - ' +`; tidak tertulis di soal; ucapannya bukan jawabannya sendiri |
| `urutkan` | menyusun 3–6 langkah instruksi atau cerita | langkah tidak kembar; urutan lain berupa susunan lengkap; langkah diperiksa seperti kalimat latihan |
| `geser` | kalimat sudah tersusun, satu potongan salah tempat | awalnya kata yang sama dengan tepat satu potongan pindah; kalimat benar dan bentuk lainnya diperiksa seperti kalimat latihan |
| `ketuk` | mengetuk bagian gambar dari data (denah, peta jalan, wajah) | area tidak bertumpuk, di dalam gambar, minimal 44 px di ponsel 375 px, tidak tampak kembar; tulisan area jawaban tidak ada di soal |

Contoh kecil:

```ts
pilah: [{ soal: "Lengkapi She ___ …. Pilah: is atau has?", kelompok: ["is", "has"],
  isi: [["tall", 0], ["long hair", 1], ["bald", 0], ["brown eyes", 1, "Mata dimiliki, jadi has."]],
  alasan: "Is untuk orangnya, has untuk bagian yang dimiliki.", /* dengar: true untuk bunyi */ }],
pasangan: [{ benar: "ship", salah: "sheep", say: "I want to see the ship.", alasan: "Ship: i pendek." }],
dikte: [{ soal: "Dengarkan. Ketik alamat email yang disebut.", say: "It's sari dot putri at mail dot com.",
  jawab: "sari.putri@mail.com", alasan: "Dot = titik, at = @." }],
urutkan: [{ soal: "Urutkan langkah resepnya.", langkah: ["First, fry some garlic.", "Then add the rice and an egg.", "Last, wash the plates."],
  alasan: "First, then, last.", /* lain: [[0, 2, 1]], say: "…" untuk urutkan dengar */ }],
geser: [{ soal: "Pindahkan always.", kalimat: "I always get up at six.", mulai: "I get up always at six.",
  arti: "Aku selalu bangun jam enam.", alasan: "Adverb of frequency sebelum kata kerja utama." }],
ketuk: [{ gambar: { judul: "Denah rumah", lebar: 100, tinggi: 90, area: [
    { id: "kitchen", x: 55, y: 0, w: 45, h: 45, ikon: "🍳", warna: "ruang" },
    { id: "bathroom", x: 40, y: 45, w: 25, h: 45, ikon: "🛁", warna: "air" }, /* … */ ] },
  soal: [{ tanya: "Dengarkan, lalu ketuk ruangannya.", say: "This is the kitchen.", area: "kitchen", alasan: "Kitchen = dapur." }] }],
```

- **Satu jawaban benar.** Tulis setiap urutan atau kalimat lain yang sama benar di `lain` (urutkan: indeks langkah; geser: kalimat; dikte: jawaban lain seperti `5/6/2010`). Dikte tidak membedakan spasi dan huruf besar kecuali tema `kapital`; selain itu jawaban harus sama persis, jadi angka nol di depan (`05`) ditulis sebagai bentuk lain bila sama benar.
- **Geser apostrof**: potongan yang diawali `~` menempel pada potongan sebelumnya di layar. `"My sister ~s ~' room is big."` tampil "My sisters' room is big."; awalnya `"My sister ~' ~s room is big."` (sister's).
- **Ketuk**: gambar dibuat dari data, bukan aset. Koordinat dalam satuan bebas (lebar 100 paling mudah); sisi terpendek area minimal 13,2 satuan per 100 lebar. Warna punya makna: `ruang`, `air`, `taman`, `jalan`, `bangunan`, `kulit`, `papan`, `netral`. Area jawaban jangan diberi tulisan yang disebut soalnya; yang ditanya diberi ikon atau dibiarkan kosong dan ditemukan dari patokan (opposite, next to).
- **Bentuk dengar** (`pasangan`, `dikte`, `urutkan` dengan `say`, `pilah` dengan `dengar`, `ketuk` dengan `say`) memakai suara browser seperti soal dengar lain; jangan membuat audio. Kalimat dengar bertanda baca, soal diawali "Dengarkan". Selama suara masih dari browser, teks ucapan ikut terkirim ke pemain (untuk dibacakan), jadi kunci dengar belum sepenuhnya tersembunyi.

## Kalimat A2 yang boleh (2026-11-22)
- Pernyataan diawali When/Where + anak kalimat **dengan koma**: "When I get home, I'll call you." (If/Because/Before… sejak dulu boleh). Tanpa koma dianggap tanya.
- Seruan: "What a beautiful view!", "What nice weather!", "How brave!", "How fast she runs!" (adjective/adverb di KATA, diakhiri !).
- Dua kalimat dalam satu butir: satu `.`/`!`/`?` di tengah, kalimat kedua kapital ("Oh no. Is there a bus?"). Titik koma boleh ("I was tired; I went home.").
- Tanya bertag "You're new here, right?" / "…, OK?" dan tanya diawali And/So/But/Or + kata tanya ("And what does platform mean?"). "So do I." tetap pernyataan.
- Titik dua di tengah: "The lesson is: never give up."
- Tahun 1000–2099 sebagai potongan ("I was born in 2019."), tidak perlu di KATA.
- Kalimat langsung dengan petik lurus `"`: `Mum said, "Come home."`, `"I'm hungry," said Budi.`, `"Are you OK?" asked Rina.` Petik menempel di awal/akhir potongan, berpasangan; tanya di dalam petik diakhiri ?. Jangan petik lengkung atau petik tunggal. Kalimat dengar dan jawaban isian juga boleh memuat petik.
- Keterangan waktu tidak dipindah otomatis dari kalimat dengan anak kalimat, dua kalimat, `;`, atau petik; tulis urutan lain sebagai bentuk lain bila perlu.

## Aturan mutu (pemilik ketat)
- **Bahasa Inggris benar dan wajar** untuk level itu, British English seperti deck (colour, favourite, Mr tanpa titik). Kalimat latihan hanya memakai kosakata dan grammar tema itu dan level sebelumnya.
- **Ketik harus bisa benar.** Arti dan situasi Indonesia harus menentukan satu kalimat saja dari kata-kata itu:
  - Dia: tulis (laki-laki) atau (perempuan), atau sebut namanya. Generator menolak he/she tanpa penanda.
  - Itu: "Itu X" bisa That's atau It's. Pakai "Bentuknya X", "Benda itu X", atau "(pakai it)".
  - Pilihan kata yang sama benar ditunjuk di arti: "(pakai can)", "(pakai could)", "(pakai may)", "(pakai have)", "(tanpa years old)", "(dengan years old)", "(tanpa o'clock)", "(pakai please)".
  - Uji akhir menyebut cara mulainya bila ada beberapa awal yang wajar ("mulai dengan my name").
  - Kalau urutan lain atau bentuk lain memang sama benar, tulis sebagai **bentuk lain** (elemen keempat `pakai`, ketiga `latihan`, keempat `isian`), bukan dilarang: please di depan atau di belakang, "Do you have a pen?" untuk "Have you got a pen?", posisi adverb of frequency yang wajar, "on Sundays" untuk "on Sunday" bila keduanya cocok dengan situasinya. Server tidak menebak bentuk lain sendiri (kecuali pemindahan keterangan waktu di atas), jadi tulis setiap varian yang benar, dan hanya varian yang benar-benar wajar untuk arti itu. Setiap bentuk lain diperiksa seperti kalimat biasa (kata terdaftar, tanda baca).
- **Isian**: jawaban satu sampai tiga kata, tepat satu jawaban benar, tidak tertulis di soalnya sendiri. Sebut bentuk yang diminta dalam kurung: arti Indonesia, "(be)", "(bentuk pendek)", "(tulis dengan huruf)", "(ejaan British)". Hindari jawaban yang punya sinonim (study/learn, eat/have) kecuali kurungnya memilih.
- **Tebak dan pilih**: tepat satu jawaban benar. Pilihan dibandingkan persis (setelah spasi tepi dibuang), jadi "See you on Monday." dan "see you on monday." boleh menjadi dua pilihan. Pilihan salah adalah kekeliruan khas penutur Indonesia dari kartu "Yang sering keliru" (I hungry, She are, a apple, Who is your name?), bukan pilihan asal. Periksa setiap pilihan sendiri: kalimat yang juga benar ("Yes, I do.") tidak boleh menjadi pengecoh.
- **Soal dengar**: diawali "Dengarkan.", kalimat dengarnya kalimat utuh bertanda baca, dan soalnya bisa dijawab dari mendengar saja.
- **Bahasa Indonesia alami** seperti tutor yang baik: kalimat pendek, "kamu", tanpa basa-basi, tanpa "Yuk, mari kita…". Istilah grammar memakai istilah akademik Inggris (Subject Pronouns, Present Simple, Countable Nouns), bukan "tata bahasa".
- Situasi konkret kehidupan Indonesia: sekolah, Pare, pasar, warung, stasiun, rumah. Harga dan angka realistis.

## Periksa sebelum selesai (semua harus lolos)
1. `cd titian-web && MISI_CEK=1 bun scripts/misi-inggris.ts` mencetak ringkasan tanpa baris masalah. Mode ini hanya memeriksa dan tidak menulis file apa pun. Generator memeriksa: kartu materi tepat satu tema, kalimat Inggris (kapital, tanda baca, a/an, subjek dan be, kata tanya dan tanda tanya, I kapital, potongan 3–12; pembuka do/don't/have dianggap tanya hanya bila diikuti subjek, jadi "Don't cross the road." dan "Have a nice weekend!" boleh), kata terdaftar di KATA, part of speech dan keluarga dikenal, arti he/she, isian pendek dan tidak bocor, pilihan tidak kembar, urutan lain memakai kata yang sama, prasyarat tanpa siklus, tidak tersirat, rantai ≤ 12, dan prasyarat kanonik antar-deck.
2. `../agent/tools/batas-ram.sh 3G bunx tsc --noEmit -p .` (dari folder titian-web) bersih untuk file-mu.
3. Generator penuh dan uji kering importer dijalankan koordinator, bukan agen penulis. Jangan mencoba menjalankannya.
4. Baca ulang setiap tebak, pilih, isian, arti latihan, dan situasi uji sekali lagi sambil bertanya: "kalau siswa paham dan mengetik kalimat lain yang juga benar, apakah ditolak?"

Mesin punya RAM 15 GB yang dipakai bersama server dev: jangan menyalakan server atau browser. Jangan membuat audio atau memanggil layanan AI berbayar; baris `say` cukup ditulis.

## Batas kerja
Kerjakan sendiri. Jangan menjalankan agen atau subagen lain: pemilik membatasi dua agen sekaligus untuk seluruh pekerjaan.

## Laporan (singkat)
Tema per deck (id, judul, indeks kartu), jumlah tebak/pilih/latihan/isian/uji, SYARAT yang dipilih, kata baru di KATA, materi yang belum bisa dilatih dengan baik oleh bentuk yang ada (sebut bentuk latihan yang cocok), isi kartu yang menurutmu salah, dan bagian deck yang terlalu berat untuk Kelas 3–6 (kebutuhan kartu jembatan).
