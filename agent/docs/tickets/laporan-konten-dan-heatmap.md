# Laporan Konten & Heatmap Belajar

Permintaan user 2026-09-14, di luar penomoran fase. Menyentuh ADR-0013 (L1 jejak → L2 pemahaman) dan ADR-0014 (Admin Pusat). Keputusan user: heatmap untuk **admin + siswa + guru kelas**; pelapor **cukup terima kasih** (tanpa status/tindak lanjut ke pelapor); tombol lapor di **soal kuis + checkpoint + bagian Modul Belajar**.

## A. Laporan konten → tiket Admin Pusat

**Data** (migrasi `0057`). `content_reports` = satu laporan per orang per tiket (lapor lagi = memperbarui). `content_tickets` = satu tiket aktif per konten (`module_item_id`, `target_type` question|checkpoint_question|section, `content_uid`), dijaga indeks unik parsial `status in (open, in_review)`. Sepuluh siswa melaporkan kunci yang sama = satu tiket, `report_count` 10. Setelah tiket selesai/ditolak, laporan baru membuka tiket baru.

**Menunjuk tempat perbaikan.** Latihan 1/2 mengundi dari bank, jadi soalnya tidak ada di item itu. `owner_of` menelusuri `question_pool.source_item_id`, sehingga tiket menunjuk **bank** (tempat soal diperbaiki). Item tempat siswa melapor tetap dicatat di `reported_from_item_id`.

**Yang dilihat siswa ikut disimpan** (`context`): nomor tampil, pilihan yang sudah diacak dan dilabel ulang, dan jawabannya. Laporan "kuncinya harusnya B" hanya bisa dicek terhadap huruf di layar siswa, bukan huruf yang tersimpan.

**Pengaman.** Melapor butuh akses yang sama dengan melihat konten (`module_item::get_detail`). `content_uid` harus benar-benar ada. Kategori `other` wajib disertai pesan. Pesan maksimal 1000 karakter, konteks maksimal 8 KB, dan maksimal 30 laporan per pengguna per 24 jam (`429 report_limit_reached`).

**Admin** (`AdminPusat`: lihat = View, ubah = Manage). `GET/PATCH /admin/content-tickets[/{id}]`. Detail memuat konten saat ini **beserta kuncinya**, semua laporan (hanya peran pelapor, tanpa identitas), dan jalur `content_context` (mapel › folder › topik › bab › item). Menolak wajib disertai catatan. Setiap perubahan status masuk `admin_audit_log`.

**Frontend.** `ReportContentButton` (bendera dan dialog kategori) muncul di header setiap soal (`QuizQuestionRenderer.headerAction`), di baris "Laporkan soal: 1 2 3" untuk layout tabel/alur, di checkpoint (asli dan pratinjau), di judul setiap bagian Modul Belajar, dan di panel "Materi bagian ini" Live AI Chat. Halaman baru **Admin Pusat › Laporan Konten**: tab status beserta jumlahnya, filter jenis masalah, daftar tiket dan panel detail, serta tombol "Perbaiki di Studio" dan "Pratinjau".

## B. Fakta jawaban & heatmap

**`content_context.rs`** menentukan letak item dalam kurikulum: `path` folder dari akar sampai topik, `bab` (section terdekat), dan mapel (item → modul → folder terdekat). Kedalaman folder berbeda antar mapel, jadi yang disimpan adalah jalurnya, bukan asumsi "level 2 = Tahap".

**`question_answer_facts`** (migrasi `0058`, dipartisi per bulan seperti `learning_events`; partisi dibuat sampai 2027-12, plus default dan pengaman saat boot `ensure_month_partitions`). Satu baris per jawaban yang dinilai: mapel, `folder_path`, topik, bab, bagian asal soal, subtype, kesulitan, Bloom, benar/salah, dan poin. Nilainya **disalin saat menjawab**, supaya bab yang diganti namanya atau soal yang dilabel ulang bulan depan tidak mengubah riwayat. Ditulis dari submit kuis (bukan pratinjau; `source` practice/tryout) dan submit checkpoint (`source` checkpoint).

**`metrics_daily_question`**: rollup per hari WIB × soal oleh job `metrics_rollup` setiap jam. Heatmap Admin Pusat membaca tabel ini, tidak pernah tabel fakta (ADR-0014). Heatmap siswa dan kelas membaca fakta langsung (query kecil berindeks per user).

**`learning_heatmap.rs`**: satu implementasi untuk tiga lingkup (`/admin/learning/heatmap`, `/me/learning-heatmap`, `/classes/{id}/learning-heatmap` untuk guru kelas atau admin organisasi, dengan `student_id` opsional yang harus anggota kelas). Drill-down berjalan di atas `folder_path`; level yang anaknya hanya satu otomatis dilewati (tidak perlu klik "Semua Mata Pelajaran" untuk sampai ke "Matematika"). Konten di luar bab dikelompokkan sebagai "Tanpa bab". Sumbu kolom bisa Bloom (C1–C6) atau kesulitan. "Soal tersulit" (admin n ≥ 5, kelas n ≥ 3) menampilkan tanda **label tidak cocok**: berlabel mudah tapi p < 0,30, atau berlabel sulit tapi p > 0,85 (ADR-0013 §2.2).

**Frontend** `LearningHeatmap`: sel berwarna merah→hijau sesuai % benar, pudar bila n < 5, breadcrumb bisa diklik, dan baris bisa di-drill. Dipasang di: Admin Pusat › Pembelajaran (placeholder diganti; mengikuti pemilih periode di header, termasuk Rentang), Progres › tab **Peta Belajar** (siswa), dan Kelas › tab **Peta Belajar** (guru, dengan pilihan seluruh kelas atau per siswa, tanpa tautan pratinjau).

## Bukti

- Unit: 255 lulus (baru: `single_child_levels_are_skipped_and_differing_depths_just_work`).
- Integration baru: `reports_on_the_same_question_collect_into_one_ticket_that_an_admin_works` (tiket menunjuk bank, 2 pelapor = count 2, lapor ulang tidak menambah count, admin melihat kunci tanpa identitas pelapor, tolak wajib catatan, audit tercatat, laporan setelah selesai membuka tiket baru) dan `graded_answers_become_facts_that_heatmaps_drill_through` (6 fakta dari siswa dan 0 dari pratinjau, breadcrumb Matematika › Tahap 1 › topik, sel C1 = 3, admin kosong sebelum rollup lalu 6/5 sesudahnya, guru lain 403, siswa di luar kelas 404).
- Integration penuh: 164 lulus. Yang gagal adalah 26 kegagalan lama ditambah `admin_participants_test::sedang_online…`, yang sudah tercatat flaky saat suite penuh berjalan paralel dan lulus saat dijalankan sendiri.
- Browser (`Bun.WebView`, user QA siswa dan platform_admin dibuat khusus; datanya dihapus setelahnya): 10 bendera untuk 10 soal, dialog "Kunci jawaban salah" dan pesan → "Terima kasih!"; Peta Belajar siswa terisi sampai bab "Nilai Tempat" per Bloom; Admin › Laporan Konten menampilkan tiket dengan konten saat ini, kunci, dan jalur kurikulum, dan "Tolak" dengan catatan berhasil; Admin › Pembelajaran setelah rollup sama dengan angka siswa di kedua sumbu, dan rentang tanggal di luar data menghasilkan 0.

## Belum dikerjakan / catatan

- Tidak ada backfill fakta untuk attempt sebelum hari ini (hasil per soal tidak pernah disimpan; menilai ulang dari `question_snapshot` bisa dilakukan kalau datanya penting).
- Statistik butir lengkap ADR-0013 §2.2 (daya beda point-biserial, pemilih pengecoh, waktu) masih Fase 41; heatmap dan "soal tersulit" adalah pondasinya.
- Laporan dari siswa belum mengalir ke `content_findings` Fase 42; tabel tiket dirancang agar bisa menjadi salah satu sumbernya.
