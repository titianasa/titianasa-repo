# Checkpoint per Bagian, Bank Soal 10/25/50, XP Anti-Farm, Generate Hemat Token

Permintaan user 2026-09-13/14, di luar penomoran Phase 39/40 (bukan lewat pipeline tiket Opus). Rencana lengkap: `~/.claude/plans/wild-brewing-hummingbird.md`.

Pemicunya review Topik 2 Matematika: materi bagus tapi (a) tidak ada pengecekan pemahaman sebelum siswa lanjut, (b) latihan cuma 5 soal pilihan ganda per bab, (c) tidak ada pengacakan yang berarti, (d) generate 50 soal/bab akan boros token kalau gagal harus mengulang dari nol.

Riset kode menemukan 4 hal yang membuat permintaan itu mustahil dipenuhi tanpa dibenahi lebih dulu, dan semuanya diperbaiki di sini.

## Fase 1 — Kertas soal dibuat server, undian, acak aman, XP

**Kunci jawaban dulu bocor.** `module_item::get_detail` mengirim `quiz_config` & `lesson_plan` mentah ke siapa pun yang boleh membuka item — termasuk `answer`, `explanation`, `option_scores`. Mengacak pilihan tidak ada gunanya selama kuncinya ada di response. Sekarang `quiz_config::learner_view` / `lesson_plan::learner_view` membuang kunci untuk semua yang bukan penulis/reviewer/guru kelas modul itu (`module_item::sees_answer_key`), termasuk di response terjemahan modul.

**Kertas soal (`services/quiz_paper.rs`, migrasi `0054`).** Saat siswa menekan "Mulai", server menyusun kertas: soal terundi dari bank, urutan diacak, pilihan diacak **dan dilabel ulang A/B/C/D sesuai posisi tampil**, dinomori ulang 1..N, tanpa kunci. Pemetaan `huruf tampil → label asli` disimpan di `attempts.paper`, jadi grading bisa menerjemahkan balik dan hanya menilai soal yang benar-benar keluar. Attempt yang masih berjalan dikembalikan apa adanya, jadi refresh/tab kedua tidak mengundi ulang (sekaligus memperbaiki attempt "nyangkut" yang dulu memblokir percobaan berikutnya dengan 409).

**Undian terstratifikasi.** `question_pool { source_item_id, draw_count }` di `quiz_config`. Undian menjaga proporsi (grup × Bloom), menyebar ke bagian modul asal, dan mengutamakan soal yang belum pernah dilihat siswa itu. Kalau satu strata kehabisan soal baru, jatahnya dialihkan ke strata lain yang masih punya (geser maksimal ±1) — tanpa itu, bank 10 soal yang diundi 5 selalu mengulang soal lama di percobaan kedua.

**Urutan yang tidak boleh diacak** (`quiz_config::detect_order_constraints`, otomatis saat simpan):
- `choices_fixed` — ada pilihan "Semua benar"/"Tidak ada yang benar"/"A dan C", atau pilihan berupa angka yang tersusun naik/turun. Pilihan tidak diacak dan huruf tidak diganti.
- `order_locked` — stem merujuk soal sebelumnya ("berdasarkan jawaban soal sebelumnya"). Soal itu menempel pada pendahulunya sebagai satu rantai saat diundi maupun diacak.
- Struktural (sudah ada, dipertahankan): grup non-flat (tabel, alur, word bank, bacaan) tidak pernah diundi/diacak, dan nomornya tidak diubah karena sel tabel/langkah alur menunjuk nomor soal.

**XP anti-farm** (`xp::quiz_xp`). Dulu setiap submit dibayar flat 20 XP — dan `skill_category` dibaca dari field `subtype` yang tidak pernah ada di grup (selalu `None`). Sekarang: lulus pertama = 2 XP × jumlah soal kertas (10→20, 25→50, 50→100), ulangan hanya dibayar kecil bila `best_score` naik, gagal tidak dibayar. Dedupe lewat `xp_events.reference` unik, jadi mustahil dobel.

## Fase 2 — Checkpoint per bagian

Kolam soal disimpan di `lesson_plan.sections[].checkpoint` (bentuk kuis, hanya subtype yang dinilai otomatis & satu kontrol per soal). Progres per siswa di `section_checkpoint_progress` (migrasi `0055`) — bukan dari telemetri `section_read`, yang bergantung persetujuan dan dilaporkan klien, jadi tidak layak jadi gerbang.

Alur: bagian ditutup 2 soal undian dari kolam 4. Benar semua → bagian berikutnya terbuka (+2 XP per soal yang pertama kali benar). Ada yang salah → bagian dikunci (`reread`), siswa melihat pembahasan soal yang salah, dan harus membaca ulang: tombol baru aktif setelah bagian di-scroll sampai habis **dan** waktu minimum lewat (`max(30 detik, menit bagian × 15)`), lalu keluar undian baru yang mengutamakan soal yang belum muncul. Bagian dikerjakan berurutan; `POST /module-items/{id}/complete` menolak selama masih ada checkpoint yang belum lulus, jadi tombol "Selesai" tidak bisa dipakai melompati pemahaman — dan Latihan baru terbuka lewat guard `completion_rule: required` yang sudah ada.

Frontend: kartu checkpoint dipakai bersama oleh reader artikel dan **Live AI Chat** (tanpa itu mode chat jadi jalan pintas). Bagian yang belum terbuka disembunyikan beserta daftar isinya. Editor Studio ikut membawa `checkpoint` lewat Y.Map (`checkpoint_json`) — tanpa itu, satu kali penulis menyimpan teks akan menghapus seluruh kolam soal.

## Fase 3 — Generate hemat token & konsisten

- **Budget thinking Vertex** (`generationConfig.thinkingConfig.thinkingBudget`, 512). Inilah penyebab `MAX_TOKENS` pada permintaan 3 soal: token "berpikir" Gemini dipotong dari jatah output yang sama, dan sebelumnya tidak pernah dibatasi. Suhu kini dibaca dari pengaturan peran Admin Pusat, bukan hardcode.
- **Slot eksplisit** (`slots` di `POST /ai/generate-quiz-group`) menggantikan kuota otomatis per panggilan. Blueprint 50 slot dihitung di kode (`blueprint.py`), jadi bank yang diisi 5-5 tetap mengikuti SATU rencana, bukan sepuluh pembulatan.
- **Rujukan per bagian** (`reference_section_id`): prompt memuat satu bagian modul secara utuh, bukan potongan 3.000 karakter seluruh artikel.
- **Resume dari database**: sebelum tiap potongan, isi bank dibaca ulang dan hanya slot yang kurang yang diminta. Label yang meleset tidak pernah digenerate ulang — potongan berikutnya menutup kekurangannya. Timeout klien tidak menggandakan soal.
- **Split adaptif**: balasan terpotong diulang lebih kecil (5 → 2 → 1), bukan request yang sama.
- **Buang duplikat sebelum simpan** (Jaccard ≥ 0,6 atas kata isi), dibatasi ke grup yang sama — di situlah bank berpotongan mengulang dirinya. Jumlah yang dibuang dilaporkan (`dropped_duplicates`) agar skrip meminta penggantinya. **Awalnya lintas grup, dan itu memecahkan 2 test**: provider palsu di test mengembalikan soal identik untuk setiap grup, sehingga seluruh batch grup kedua terbuang dan panggilan gagal 422. Lintas-grup juga salah secara isi: fakta yang sama ditanyakan sebagai pilihan ganda dan sebagai isian adalah dua latihan berbeda.
- **Keterbacaan stem per jenjang** (`quiz_taxonomy::stem_readability`) — SD maksimal 20 kata.

**Struktur per bab sesudahnya** (urutan tetap): `Pembahasan — <bab>` (checkpoint tiap bagian, guard required) · `Latihan 1 — <bab>` (10 soal, undian) · `Latihan 2 — <bab>` (25 soal, undian) · `Latihan 3 — <bab>` (bank 50 soal). Judul memberi nomor, bukan jumlah soal; nomor hanya muncul bila ada lebih dari satu (juga untuk Pembahasan).

## Bukti

**Unit test** (248 lulus): undian terstratifikasi & proporsi bank terjaga, dua seed beda → kertas beda, ulangan menghindari soal yang sudah dilihat, pelabelan ulang + terjemahan jawaban balik, `choices_fixed`/`order_locked` dihormati, grup non-flat tidak diacak/dinomori ulang, deteksi urutan (termasuk `false` eksplisit penulis tidak ditimpa), rumus XP, blueprint, dedupe.

**Integration test baru (6, semuanya lewat HTTP sungguhan)**: kunci jawaban tidak sampai ke siswa tapi sampai ke penulis · kuis bank mengundi 5 dari 20 dan dinomori 1..5 · refresh mengembalikan kertas identik · jawaban dalam huruf tampil dinilai benar (skor 100) dan 15 soal yang tidak keluar tidak ikut dinilai · ulangan 5 dari bank 10 seluruhnya soal baru · 3× lulus sempurna tetap 10 XP · bank di modul lain ditolak · checkpoint: kolam tidak bocor, bagian berurutan, "Selesai" ditolak, salah → `reread` + `reread_too_soon`, lulus semua → artikel selesai → Latihan terbuka.

**Browser sungguhan** (`Bun.WebView`, modul QA sekali-pakai, dihapus setelahnya): bagian 2 terkunci sebelum checkpoint · jawaban salah → "Baca ulang bagian ini dulu" dengan tombol "Coba lagi dalam 29 detik" nonaktif · setelah waktunya lewat, undian baru, benar → "Checkpoint lulus · +4 XP" dua kali · Latihan mengundi 5 soal, pembahasan **tidak** tampil sebelum submit dan tampil sesudahnya, skor 100 walau pilihan sudah diacak dan dilabel ulang.

**Pilot generate 1 bab** (Topik 2 / "Mengenal Bilangan Cacah"): 1,8 menit, **110.507 token**, hasil di database persis blueprint — 50 soal (MC 25 / benar-salah 10 / isian 15; C1 10 / C2 18 / C3 15 / C4 7; 10 soal per bagian, semua bertanda bagian asal), 20 soal checkpoint (4 per bagian), 1 duplikat dibuang, 1 slot meleset label dan ditutup putaran kedua tanpa generate ulang apa pun.

Proyeksi kasar: ±110k token & ~2 menit per bab → ~770k token & ~14 menit per topik → 334 topik Matematika ≈ 257 juta token, ~78 jam berurutan (jauh lebih murah dari perkiraan awal 390 jam, terutama karena budget thinking).

## Penyimpangan sadar dari rencana

- **Budget thinking = konstanta 512**, belum jadi pengaturan per peran di Admin Pusat (butuh kolom + UI). Suhu sudah dari pengaturan peran.
- **Checkpoint hanya pilihan ganda** (4 soal per bagian, 1 panggilan AI). Campur jenis butuh 1 grup per jenis = 3× panggilan per bagian; untuk pengecekan 2 soal, biayanya tidak sepadan. Latihan tetap beragam (3 jenis).
- **Dedupe dibatasi ke grup yang sama** (lihat alasan di Fase 3).

## Sisa pekerjaan

- Generate ulang 6 bab lain Topik 2 + seluruh Topik 1 dengan pipeline baru (Topik 2 bab "Mengenal Bilangan Cacah" sudah).
- `metrics_rollup_test::subscriptions_rollup_computes_new_active_and_churned` **gagal hanya antara pukul 00:00–01:00 WIB**: test lama itu menaruh langganan berakhir "1 jam lalu", yang jatuh di tanggal kemarin. Rapuh terhadap waktu, bukan akibat perubahan ini, belum diperbaiki.
- `admin_participants_test::sedang_online...` sempat gagal sekali saat suite penuh berjalan paralel, lulus saat dijalankan sendiri.

## Revisi setelah review Topik 2 (2026-09-14)

**Urutan & judul.** `generate_bab_content.py` kini memberi nomor (`LATIHAN = [10, 25, 50]`, `latihan_title`, `pembahasan_title`) dan memanggil `POST /module-items/reorder` untuk tiap bab — urutan pembuatan (bank dulu) bukan urutan yang ditemui siswa. Item mana yang bank dan mana yang mengundi dibaca dari `quiz_config`, bukan dari judul. `restructure_bab_items.py` menerapkannya ke konten yang sudah ada: 21 judul, 14 bab diurut ulang. Bab Topik 1 yang masih punya satu Latihan tetap `Latihan — <bab>`.

**JSON mentah di artikel.** Dua penyebab: (1) `alm_parser::parse_key_value_body` membaca per baris, jadi `rows: [` yang ditulis model dalam beberapa baris terbaca sebagai string `"["`; (2) model menulis `title:` pada `:::table` (skema: `caption`). Blok gagal skema lalu di-demote dengan menumpahkan sumbernya — JSON-nya sampai ke layar siswa. Perbaikan: parser membaca nilai JSON multi-baris (sadar string & kurung); `sanitize_generated` mencoba mengganti nama kunci yang keliru (`KEY_ALIASES`) sebelum demote; demote tidak pernah lagi mengeluarkan JSON (array → daftar). Konten yang sudah tersimpan dipulihkan oleh `repair_demoted_blocks.py`: 4 artikel, 25 blok (14 tabel, 7 langkah, 4 perbandingan), disimpan lewat API sehingga divalidasi server.

**Pratinjau (`/belajar/{id}/preview`).** Pintu siswa dan pintu pratinjau dipisah tegas, tidak ditebak dari peran. `/belajar/{id}` = siswa: item belum terbit menampilkan "Materi ini belum terbit" + tombol "Buka pratinjau" (bila boleh). `/belajar/{id}/preview` = penulis/reviewer/admin/kolaborator (`assessment::can_preview`: `ModuleItem::ViewUnpublished` atau grant viewer; status apa pun; `can_preview` ikut di `GET /module-items/{id}`). Tombol "Pratinjau" di editor item Studio dan "Live Preview" editor Modul Belajar kini membuka URL ini.
- **Kuis**: `POST /lessons/{id}/attempts?mode=preview` → attempt bertanda `is_preview` (migrasi `0056`). Kertas & grading asli, tapi: tanpa XP/streak/misi, tanpa `record_completion`, tanpa learning event, tanpa proctoring, tidak dihitung `max_attempts`, tidak masuk antrean nilai manual, dan tidak memblokir hapus item/modul (`purge_preview_attempts` ikut membersihkan evaluasi & feedback-nya).
- **Modul Belajar**: semua bagian terbuka; checkpoint lewat endpoint tanpa status `POST …/checkpoint/preview` (undian) dan `…/checkpoint/preview/grade` (nilai) — tidak ada baris `section_checkpoint_progress`, "Soal lain" mengundi ulang. Live AI Chat mengirim `preview: true` sehingga pertanyaan tidak dicatat. Telemetri klien dimatikan selama halaman pratinjau terbuka (`suppressTelemetry`).

**Tinjau kunci jawaban setelah submit.** Kertas dari server memang tanpa kunci, dan kartu hasil hanya menampilkan "Jawaban benar" untuk soal salah — soal benar-salah & isian terlihat tanpa kunci. Sekarang setiap soal punya panel di bawahnya (`answer-review.tsx`): Benar/Salah, "Lihat kunci" per soal (jawabanmu, kunci + teks pilihannya, alternatif yang diterima, pembahasan); untuk layout tabel/alur panelnya berderet di bawah grup. Kartu skor: "Tampilkan/Sembunyikan semua kunci" dan "Kunci soal yang salah saja". Awalnya tersembunyi.
**Huruf di pembahasan.** Pembahasan ditulis dengan huruf tersimpan ("Pilihan C benar"), padahal pilihan diacak & dilabel ulang — bertentangan dengan "Kunci: B". `quiz_paper::explanation_as_shown` menerjemahkan huruf setelah kata "pilihan/opsi/jawaban" (termasuk daftar "A dan C") ke huruf yang tampil, di hasil kuis dan checkpoint; prompt generate kini meminta pembahasan menyebut isi pilihan, bukan hurufnya.

Bukti tambahan: `quiz_paper_test::the_preview_door_is_separate_from_the_learner_door_and_leaves_no_history`, `section_checkpoint_test::an_author_previews_checkpoints_on_a_draft_without_leaving_any_progress`, unit `explanation_letters_follow_the_shuffled_choices`; integration penuh 163 lulus / 26 gagal lama (daftar sama). Browser (`Bun.WebView`, token QA dihapus): URL siswa pada draf → pesan + tombol pratinjau; artikel pratinjau terbuka semua, 6 tabel ter-render tanpa JSON, checkpoint dinilai & "Soal lain"; kuis draf 10 soal → skor, 10 panel kunci, tampil semua/sembunyikan per soal bekerja; di DB 0 progres, 0 checkpoint, 0 XP, 0 learning event untuk sesi QA.

**Batas output token.** Artikel satu bab adalah satu panggilan; balasan yang terpotong dulu dibuang dan diminta ulang utuh — kena batas yang sama lagi. Sekarang `generate_plan` melanjutkan: bagian yang sudah tertutup (`<<<END_SECTION>>>`) disimpan, panggilan berikutnya hanya meminta sisanya dengan menyebut judul bagian yang sudah ada (bukan mengirim ulang isinya), maksimal 5 lintasan. `GenerationRequest.allow_partial` membuat Vertex menyerahkan teks `MAX_TOKENS` bertanda `truncated` alih-alih error — hanya untuk pemanggil yang bisa melanjutkan; generator JSON (kuis) tetap menganggapnya error dan tetap memakai split 5→2→1 per soal. Jadi: keluaran terstruktur dipecah per unit, keluaran prosa dilanjutkan.

Bukti: unit 253 lulus (parser multi-baris, kurung dalam prosa/string, rename `title`→`caption`, demote tanpa JSON); integration `quiz_paper_test` 6 lulus (pratinjau draf & kuis terbit, 0 XP, siswa tetap ditolak di draf) dan `ai_retry_test::an_article_cut_off_by_the_output_ceiling_is_continued_not_regenerated` (4 bagian utuh dari 2 lintasan, prompt lanjutan menyebut judul tanpa mengirim isi). Cek langsung ke server: penulis memulai Latihan 1 terbit (10 soal) dan Latihan 3 draf (47 soal), `preview=true`, tanpa kunci jawaban; attempt & token QA dihapus.
