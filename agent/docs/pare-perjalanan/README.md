# Perjalanan belajar di Kampung Bahasa Pare

Folder ini berisi **skenario lengkap** seorang pemain yang belajar bahasa Inggris dari nol sampai C2: tiap level adalah satu tahap hidup, tiap bab ditutup satu misi, dan tiap level ditutup satu Misi Besar yang membuka wilayah baru. Aturannya (cara misi dinilai, syarat lulus, multipemain) ada di [ADR-0019](../adr/0019-jalur-belajar-dan-misi-pare.md); folder ini adalah isinya.

Status: **rencana**. Belum ada kode jalur atau misi. Isi pelajaran Basic sampai B1 sudah ada; isi B2 sampai C2 belum ditulis (yang ada di sini adalah silabusnya).

## Isi folder

| Berkas | Isi |
|---|---|
| [en-ringkasan.md](en-ringkasan.md) | Angka keseluruhan, Misi Besar tiap level, alur cerita sepuluh warga inti, dan daftar kebutuhan pembangunan (tokoh, tempat, aplikasi komputer, jenis langkah, mode multipemain, isi yang belum ditulis) |
| [en-0-basic.md](en-0-basic.md) | Basic — Pendatang baru |
| [en-1-a1.md](en-1-a1.md) | A1 — Menjadi warga |
| [en-2-a2.md](en-2-a2.md) | A2 — Merantau ke kota |
| [en-3-b1.md](en-3-b1.md) | B1 — Magang jadi reporter |
| [en-4-b2.md](en-4-b2.md) | B2 — Mahasiswa pertukaran di London |
| [en-5-c1.md](en-5-c1.md) | C1 — Profesional & peneliti |
| [en-6-c2.md](en-6-c2.md) | C2 — Duta & mentor |
| [adaptasi-bahasa-lain.md](adaptasi-bahasa-lain.md) | Cara menerapkan skenario ini ke Mandarin, Jepang, Korea, dan Arab |

## Perjalanannya dalam satu halaman

| Level | Tahap hidup | Wilayah | Bab | Misi Besar | Yang terbuka sesudahnya |
|---|---|---|---|---|---|
| Basic | Pendatang baru | Kampung Inggris | 5 | Minggu pertamaku di Kampung | Permukiman |
| A1 | Menjadi warga | Permukiman | 14 | Pesta kampung | Pusat kota |
| A2 | Merantau ke kota | Pusat kota | 14 | Gaji pertama, liburan pertama | Distrik media & kampus |
| B1 | Magang jadi reporter | Distrik media & kampus | 14 | Edisi khusus Kampung Post | London (beasiswa) |
| B2 | Mahasiswa pertukaran | London, kawasan mahasiswa | 12 | Konferensi Mahasiswa Internasional | London, City & Westminster |
| C1 | Profesional & peneliti | London, City & Westminster | 12 | Proyek unggulan | London, South Bank |
| C2 | Duta & mentor | South Bank, lalu pulang ke Pare | 10 | Karya besar & pulang kampung | Balai Mentor |

Jumlah: 81 bab, 81 misi bab, 7 Misi Besar, 70 misi warga (10 warga × 7 level).

## Cara membaca halaman level

Tiap halaman level punya urutan yang sama, dan urutan itu juga urutan yang dilihat pemain:

1. **Sekilas** — jumlah kata, konsep, bab, pelajaran, perkiraan waktu, dan apakah isi pelajarannya sudah ditulis.
2. **Yang perlu kamu siapkan** — bekal untuk satu level (panjang tulisan, perangkat, hal yang berbeda dari level sebelumnya).
3. **Syarat naik level** — daftar centang: semua bab, sejumlah misi warga, Misi Besar.
4. **Dunia yang terbuka** — tempat, tokoh, dan aplikasi komputer baru.
5. **Peta bab** — satu tabel: bab, tata bahasa, jumlah kata, jumlah pelajaran, misi bab, pola, mode.
6. **Bab demi bab** — untuk tiap bab: apa yang bisa dilakukan sesudahnya, tata bahasa, kosakata, fungsi bahasa, pelafalan, bahan Praktik; lalu **misi bab** secara lengkap:
   - cerita dan hasil nyata;
   - bekal dan kalimat kunci;
   - langkah demi langkah, tiap langkah dengan jenisnya (`dialog`, `dengar`, `tulis`, …);
   - **dinilai dari** apa (butir yang masuk skor);
   - tantangan bintang ketiga (mulai A2);
   - apa yang terjadi **dengan pemain lain**, dan penggantinya kalau sepi;
   - hadiah.
7. **Misi Besar** — tiga babak.
8. **Misi warga** — satu per warga inti; pilih beberapa.
9. **Acara dunia** — kegiatan bersama pada waktu nyata; opsional.

Arti jenis langkah dan cara tiap jenis diverifikasi: ADR-0019 §6. Cara skor dan bintang dihitung: ADR-0019 §16.3. Arti mode (solo, ramai, pasangan, kelompok, asinkron): ADR-0019 §17.3.

## Dari mana halaman ini berasal

Halaman `en-*.md` **dihasilkan**, jangan disunting tangan. Sumbernya data bertipe di repo game:

```
alr/game/src/game/content/journey/
  types.ts        bentuk data: level, bab, misi, misi warga, tokoh, tempat, aplikasi
  en.ts           perjalanan bahasa Inggris (menggabungkan berkas di bawah)
  en/world.ts     tokoh, tempat, aplikasi komputer
  en/l0.ts … l6.ts   satu berkas per level
alr/game/scripts/journey.ts   pemeriksa + penghasil halaman
```

```
cd alr/game
bun scripts/journey.ts            # periksa; keluar dengan kode 1 kalau ada yang tidak cocok
bun scripts/journey.ts --write    # periksa, lalu tulis ulang en-*.md di folder ini
```

Yang diperiksa skrip, per level:

- tiap konsep tata bahasa di silabus (`benchmark.ts`, `benchmark-plan.ts`) ada di **tepat satu** bab;
- anggaran kata tiap bab cocok: per kategori kata untuk level yang isinya sudah ada, atau dengan jumlah kata baru di kontrak untuk B2–C2;
- situasi, bacaan, dialog, dan tugas menulis habis terbagi ke bab (judul bacaan dan tugas menulis yang sudah ada dicocokkan satu per satu);
- tiap misi menyebut tokoh, tempat, pola, mode, dan jenis langkah yang dikenal, dan hanya memakai tokoh, tempat, serta aplikasi yang sudah terbuka di level itu;
- tiap misi punya kalimat kunci, hasil, cara dinilai, keterangan multipemain, dan (mulai A2) tantangan bintang ketiga;
- tiap warga inti punya tepat satu misi per level.

Saat ini ketujuh level lolos semua pemeriksaan itu.

## Yang perlu diingat saat membaca angka

- **Perkiraan waktu** dihitung dari jumlah pelajaran dan misi dengan menit per unit yang saya tetapkan sendiri (6 menit per pelajaran di Basic sampai 10 menit di C2, dan seterusnya; lihat konstanta di `scripts/journey.ts`). Belum diukur pada pemain.
- **Anggaran kata per bab** untuk Basic–B1 dijumlahkan per kategori supaya cocok dengan isi yang ada, tetapi penugasan kata satu per satu ke bab belum dibuat. Itu pekerjaan saat membangun, dan angkanya boleh bergeser sedikit antar bab.
- **Ranah kosakata, judul bacaan, dan jenis tulisan B2–C2** adalah rencana. Isinya ditulis nanti dan harus lolos benchmark yang sama dengan level lain.
- **Jadwal acara dunia** (jam WIB) adalah tebakan; belum ada data kapan pemain ramai.
- Semua nama tokoh, lembaga, dan tempat di London adalah fiktif kecuali nama tempat umum (Borough Market, British Library, Southbank Centre, Speakers' Corner, West End).
