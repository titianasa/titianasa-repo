# Phase 34 — Dashboard "Pilih Fokus Belajar" Preset Picker

🟢 **SELESAI** — selesai dan teruji (2026-09-07).

## Konteks

User minta beberapa preset ditampilkan sebagai pilihan fokus belajar di dashboard: Belajar Bahasa Inggris, Kurikulum Indonesia (dibagi per jenjang SD Kelas 1 sampai SMA Kelas 3), Kurikulum Cambridge, Fokus Ujian TKA, Persiapan Ujian Masuk Perguruan Tinggi, Ujian CPNS, Ujian BUMN.

Tidak ada konten kurikulum nyata untuk 6 dari 7 preset ini (cuma "English"/"IELTS" yang sungguhan ada, sisanya masih data smoke-test). Keputusan scope: buat FOLDER organisasi asli (kosong, `is_folder=true`, tanpa `subject_id`) lewat migrasi — bukan konten karangan — reuse penuh tree `modules` self-nesting yang sudah ada (Phase 31) dan `ModuleBrowser`/`/belajar` yang SUDAH punya empty state jujur ("Belum ada materi di sini."). Tidak ada tabel baru, tidak ada endpoint baru — picker di dashboard cuma link statis ke id folder yang sudah di-seed, pola yang sama dengan `DEFAULT_SUBJECT_ID` di `lib/curriculum.ts`. Breakdown 12 jenjang Kurikulum Indonesia otomatis muncul lewat `ModuleBrowser` yang sudah ada begitu folder itu diklik — nol kode picker tambahan diperlukan untuk itu.

**Bug desain nyata ditemukan lewat smoke test**: draft awal cuma bikin folder root untuk 6 preset BARU, dan "Belajar Bahasa Inggris" dibiarkan link ke `/belajar` root TANPA parent — ternyata itu artinya folder Bahasa Inggris akan menampilkan SEMUA modul root lain juga, TERMASUK 6 folder preset baru itu sendiri sebagai sibling (Kurikulum Indonesia, CPNS, dll nongol di halaman yang harusnya cuma Bahasa Inggris). Fix: migrasi kedua (`0031_english_preset_folder.sql`) memberi Bahasa Inggris folder root sendiri juga, supaya ketujuh preset simetris — tidak ada satu pun yang link ke root polos lagi.

## Perubahan

- `titian-backend-rust/migrations/0030_learning_preset_folders.sql` — 6 folder root (Kurikulum Indonesia + 5 lainnya) + 12 folder anak (jenjang SD1-SMA3) di bawah Kurikulum Indonesia. ID literal tetap (bukan `gen_random_uuid()`) supaya frontend bisa link langsung.
- `titian-backend-rust/migrations/0031_english_preset_folder.sql` — folder root ke-7 untuk Belajar Bahasa Inggris (fix desain di atas).
- `titian-web/src/components/dashboard/learning-preset-picker.tsx` (baru) — grid 7 card, masing-masing `Link` ke `/belajar?parent=<id>`.
- `titian-web/src/app/(app)/beranda/page.tsx` — pasang `<LearningPresetPicker />` setelah `RoleStatusCard`.

## DoD
`cargo check` bersih (migrasi saja, tanpa perubahan Rust). `npx tsc --noEmit` + `npx eslint src` bersih. Smoke test browser asli: dashboard menampilkan ketujuh card dengan judul/deskripsi benar; navigasi langsung ke folder Kurikulum Indonesia menampilkan seluruh 12 folder jenjang dengan urutan benar (SD Kelas 1 → SMA Kelas 3); navigasi ke folder Bahasa Inggris menampilkan "Belum ada materi di sini." bersih, TANPA folder preset lain ikut muncul (bukti fix desain di atas bekerja).

## Follow-up (sesi sama, 2026-09-07) — tinggi card, preset per mata pelajaran, detail folder

User minta 3 hal lagi setelah lihat hasilnya: (1) tinggi/besar card disamakan — card "Ujian Masuk Perguruan Tinggi" (judul 2 baris) lebih tinggi dari card lain sebaris karena `<Link>` (elemen `<a>`, inline by default) tidak stretch mengikuti tinggi grid cell; (2) tambah kategori preset KEDUA — belajar per mata pelajaran (Matematika, IPA, IPS, Ekonomi, Sejarah, Geografi, Fisika, Kimia, Biologi, Filsafat) untuk yang mau belajar 1 subjek end-to-end tanpa dibagi jenjang; (3) folder tanpa konten (misal Kurikulum Cambridge) tidak menampilkan detail apa pun selain "Belajar" generik + empty state — tidak jelas folder itu tentang apa.

**Perubahan:**
- `titian-backend-rust/migrations/0032_subject_preset_folders.sql` — folder root "Semua Mata Pelajaran" (card ke-8) + 10 folder anak per mata pelajaran, pola sama persis dengan 0030 (folder organisasi kosong, id literal tetap).
- `learning-preset-picker.tsx` — `Link` dan `Card` dikasih `h-full`/`w-full` + `line-clamp-2` di judul dan deskripsi, supaya tinggi card konsisten terlepas dari panjang teks; card ke-8 "Semua Mata Pelajaran" ditambahkan ke array `PRESETS`.
- `components/belajar/module-browser.tsx` — fetch `useModule(parentId)` (data folder saat ini, BUKAN ancestor) dan tampilkan judul+deskripsinya sendiri sebagai heading, tepat di atas empty state/daftar anak — ini yang tadinya hilang untuk folder preset manapun yang belum ada isinya.
- `app/(app)/belajar/page.tsx` — heading generik "Belajar / Jelajahi materi yang tersedia" cuma tampil di root (`!parentId`), supaya tidak dobel dengan heading baru ModuleBrowser begitu masuk ke satu folder.

**DoD**: `npx tsc --noEmit` + `npx eslint src` bersih. Smoke test browser: dashboard 8 card tinggi seragam; `/belajar?parent=<cambridge-id>` menampilkan heading "Kurikulum Cambridge" + deskripsinya di atas "Belum ada materi di sini." (bukan cuma "Belajar" generik lagi); `/belajar?parent=<semua-mapel-id>` menampilkan 10 folder mata pelajaran berurutan.

## Follow-up 2 (sesi sama, 2026-09-07) — posisi section + turunan di 6 preset yang masih kosong

User minta section "Pilih Fokus Belajar" dipindah ke bawah, tepat di atas section "Belajar bareng tutor asli" (sebelumnya di atas, dekat salam pembuka) — dan 6 dari 8 preset (Belajar Bahasa Inggris, Kurikulum Cambridge, Fokus Ujian TKA, Ujian Masuk Perguruan Tinggi, Ujian CPNS, Ujian BUMN) dilengkapi turunan/pembagian di dalamnya — sebelumnya cuma Kurikulum Indonesia (12 jenjang) dan Semua Mata Pelajaran (10 mapel) yang punya sub-folder, 6 lainnya cuma folder tunggal kosong.

**Perubahan:**
- `titian-web/src/app/(app)/beranda/page.tsx` — `<LearningPresetPicker />` dipindah dari sebelum `<StatCards />` ke tepat sebelum card "Belajar bareng tutor asli" di paling bawah.
- `titian-backend-rust/migrations/0033_preset_folder_subtrees.sql` — 24 folder anak baru, pola sama persis dengan migrasi sebelumnya, dipetakan ke struktur nyata masing-masing:
  - Belajar Bahasa Inggris → 7 level CEFR-style (Pre-Basic, A1–C2)
  - Kurikulum Cambridge → 4 tahap (Primary, Lower Secondary, Upper Secondary/IGCSE, Advanced/A Level)
  - Fokus Ujian TKA → 3 jenjang (SD, SMP, SMA)
  - Ujian Masuk Perguruan Tinggi → 3 jalur (UTBK-SNBT Saintek, UTBK-SNBT Soshum, Ujian Mandiri PTN)
  - Ujian CPNS → 4 tahap seleksi nyata (SKD: TWK/TIU/TKP, lalu SKB)
  - Ujian BUMN → 3 tahap Rekrutmen Bersama BUMN (TKD, Tes Bahasa Inggris, Tes AKHLAK)

Tidak ada perubahan kode picker/ModuleBrowser — pola "folder anak otomatis muncul begitu diklik" yang sudah dibangun untuk Kurikulum Indonesia langsung berlaku ke semua preset lain tanpa kerja tambahan.

**DoD**: `cargo check` bersih. `npx tsc --noEmit` + `npx eslint src` bersih. Smoke test browser: dashboard menampilkan section preset tepat di atas "Belajar bareng tutor asli"; folder Bahasa Inggris menampilkan 7 level CEFR; folder Ujian CPNS menampilkan 4 tahap seleksi sesuai struktur ujian nyata.

## Follow-up 3 (sesi sama, 2026-09-07) — 4 mapel tambahan

`titian-backend-rust/migrations/0034_more_subject_presets.sql` — 4 folder mapel baru di bawah "Semua Mata Pelajaran" (order_index lanjut dari 9): Sosiologi, Bahasa Indonesia, Pendidikan Kewarganegaraan, Akuntansi. Pola sama persis dengan 0032, tidak ada perubahan kode. **DoD**: `cargo check` bersih, smoke test browser — folder "Semua Mata Pelajaran" sekarang menampilkan 14 mapel berurutan, 4 yang baru muncul di akhir.
