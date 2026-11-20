# ADR-0031: Latihan memakai engine Parilabs Academy

Status: diterima (pemilik, 2026-11-19)

## Arahan pemilik
> Untuk latihan, saya ingin kamu menggunakan engine yang sekarang digunakan di Parilabs Academy, karena di situ sudah lengkap: sistem modul, bank soal, exam runner, sampai proktornya. Kamu bikin itu, kamu sesuaikan dengan yang ada di titianasa.

Keputusan pemilik:
- **Cara pakai:** kode disalin ke Titian dan menggantikan versi lama Titian, karena Titian belum launch (lihat memori "free to change before launch"). Setelah disalin, kedua produk berjalan terpisah.
- **Isi:** bank soal Parilabs (IELTS, PTE, TOEFL ITP, beserta audionya) ikut diimpor.

## Sumber
- **Backend:** `/home/john/Dev/parelabs-workspace/parelabs-backend-go` (Go, multi-tenant `org_*`).
  - Paket yang relevan: `internal/quiz`, `internal/grading`, `internal/proctor`, `internal/assignment`, `internal/observer`, bagian ujian dan latihan dari `internal/elearning`, serta `internal/platform/access`.
  - Skema dan migrasi: `db/migrations`, `db/schema.sql`.
  - Dokumen: `docs/elearning-v2/` (terutama `03_INTEGRASI_SISTEM_MODUL.md` dan `17_PENGAWASAN_LIVE_DAN_LOG.md`), `docs/ielts`, `docs/pte`, `docs/toefl-itp`.
- **Web:** `/home/john/Dev/parelabs-workspace/app-parelabs-v2` (Next 15, multi-tenant `[tenantSlug]`).
  - Komponen: `components/labs` (player tugas, proktor, ujilab, latihan), `components/editor` (editor modul dan soal), `components/widgets`, `components/admin/learning-rules-editor.tsx`.

## Yang diganti di Titian
- **Backend:** `internal/module`, `internal/program`, `internal/question`, `internal/assessment`, `internal/quiz`, dan tabel lama `modules`, `module_items`, `programs`, `question_banks`, `questions`, `assessments`, `attempts`, `exam_sessions`, `proctoring_*`.
- **Web:** Studio (modul, program, bank soal), Latihan (ujian, try out, mock exam), dan Pengawasan.
- Data lama yang masih berguna dipindah dulu, lalu yang lama dihapus. Arsipkan sebelum menghapus (aturan repo).

## Yang tetap milik Titian
- Identitas dan akun, organisasi Titian (sekolah dan lembaga), ekonomi dan langganan.
- Kanonik, jalur, kartu, misi (Belajar), Kelas (tutor AI), Misi (Kampung Bahasa, Grup).
- Desain Titian dan web Vite + TanStack (ADR pindahan Vite, 2026-11-19).
- Engine Parilabs mengikuti gaya Titian, bukan sebaliknya.

## Pemetaan prinsip
- **Tenant.** Organisasi Titian dipetakan menjadi tenant Parilabs (`org_id`). Pelajar mandiri tanpa organisasi memakai jalur pribadi, yaitu `org_id IS NULL` atau "me" seperti di Parilabs. Cara tepatnya diputuskan di fase 0.
- **Latihan dan jalur.** Latihan menautkan modul dan bank soal ke unit kanonik dan jalur (TKA, SNBT, dan lainnya), supaya hasil latihan ikut menjadi bukti penguasaan (ADR-0026).
- **Bagian yang tidak relevan tidak disalin.** Fitur khusus Parilabs, seperti SpeakingPro 2, mitra, sertifikat, dan white-label, hanya disalin kalau Latihan Titian membutuhkannya.

## Fase
0. **Inventaris dan kontrak.** Hasilnya `agent/docs/latihan-parilabs/00_INVENTARIS.md`, berisi:
   - daftar tabel, endpoint, dan komponen yang disalin, beserta ketergantungannya;
   - pemetaan ke tabel dan akun Titian;
   - daftar fitur Titian lama yang hilang atau perlu padanan.
1. **Skema.** Migrasi Titian untuk tabel `org_*` yang dipakai: program, modul, item, aturan belajar, bank soal, percobaan, dan proktor (event, lock, frame, kelas-proktor).
2. **Backend.** Salin paket Go, lalu sesuaikan dengan platform Titian: auth, `httpx`, tenant, storage, dan AI resolver. Setiap paket wajib punya tes integrasi.
3. **Web.** Salin player tugas, exam runner, proktor (dinding pantau dan live), editor modul dan soal, serta aturan belajar ke `titian-web` (Vite). Tampilan mengikuti desain Titian.
4. **Isi.** Impor bank IELTS, PTE, dan TOEFL ITP beserta audionya. Pindahkan bank soal Titian (TKA, SNBT, kurikulum) ke format modul.
5. **Bersih-bersih.** Hapus domain lama setelah diarsip, uji penuh, lalu deploy dengan konfirmasi.

## Akibat
- Ini pekerjaan besar: backend Parilabs yang relevan puluhan ribu baris, dan `components/labs` saja sekitar 76 ribu baris. Pekerjaannya bertahap, lintas sesi, dan tunduk pada batas dua agen sekaligus.
- Setelah disalin, perbaikan di Parilabs tidak otomatis masuk ke Titian, dan sebaliknya.

## Keputusan lanjutan (pemilik, 2026-11-19, setelah inventaris fase 0)
- **Hak isi.** Bank IELTS (Cambridge), PTE (Pearson), dan TOEFL ITP (ETS) diimpor hanya ke database dev. Isinya baru naik ke prod setelah pemilik memastikan hak pakainya.
- **Efek latihan.** Hasil latihan menjadi bukti dan ditampilkan, tetapi status unit tetap dari deck materi dan misi (ADR-0026 aturan 3).
- **Gratis dan berbayar.** Setiap bank punya satu test gratis (`public`). Sisanya dibuka lewat langganan Titian.
- **Pelajar mandiri.** Isi Latihan dimiliki satu org platform "Titian Asa" (`public` atau grant produk). Percobaan pelajar mandiri tanpa `org_id`, sedangkan siswa sekolah lewat org sekolahnya.
- **Usulan inventaris yang dipakai** (`latihan-parilabs/00_INVENTARIS.md` §9; boleh diubah pemilik):
  - K1: yang diganti hanya domain ujian. Pustaka Belajar (`modules`, kuis bab) tetap. Kuis bab disalin ke format modul.
  - K5: tautan ujian publik dibuat di fase opsional.
  - K6: generator AI memakai `ai/quizgen` Titian.
  - K7: cukup status terbit milik modul dan item.
  - K8: rute `/latihan/*` dan paket `internal/latihan`.
  - K9: kursus IELTS e-learning v2 tidak ikut disalin.
