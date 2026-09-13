# ADR-0014: Admin Pusat — Dashboard Seluruh Aplikasi & Pusat Kendali AI

Status: Accepted
Date: 2026-09-13 (diusulkan & disetujui user pada tanggal yang sama)
Supersedes: -
Superseded by: -
Related: ADR-0005 (credit economy), ADR-0006 (RBAC), ADR-0013 (AI Learning Engine)

## Context

Titian belum punya tempat untuk melihat aplikasi secara utuh. Yang ada hanya `/organisasi` (konsol satu organisasi), `/pengawasan` (proctoring tryout), dan Studio (penulisan konten). Tidak ada satu layar pun yang menjawab pertanyaan paling dasar pengelola platform: berapa peserta aktif hari ini, berapa pendapatan bulan ini, berapa topik kurikulum yang sudah berisi konten, berapa biaya AI minggu ini, atau kelas mana yang tingkat kehadirannya jatuh.

ADR-0013 menambah kebutuhan kedua yang lebih mendesak: agen konten AI bekerja **semi-otonom**, dan setiap usulannya harus **dilaporkan dan disetujui lebih dulu**. Tanpa Admin Pusat, lapisan L4 ADR-0013 tidak punya tempat untuk dijalankan.

Kondisi data saat ini (2026-09-13) yang membentuk keputusan ini:
- Peran `platform_admin` sudah ada di RBAC (ADR-0006), jadi gerbang izin tidak perlu dibuat dari nol.
- Data penjualan tersebar di `orders` (`kind`, `amount_idr`, `status`, `subscription_tier`), `subscriptions`, `transactions` + `credits` (ekonomi diamond, ADR-0005), `learning_products`/`enrollments` (marketplace), dan `ad_views`.
- `users` tidak punya kolom aktivitas terakhir, sehingga "peserta aktif" belum bisa dihitung. Setelah ADR-0013, sumbernya adalah `learning_events`.
- `ai_tasks` sudah mencatat setiap panggilan AI beserta token dan statusnya.

## Decision

### 1. Posisi dan akses
- Area baru `/admin` di titian-web, terpisah dari Studio (penulisan) dan `/organisasi` (satu organisasi). Admin Pusat melihat **seluruh platform lintas organisasi**.
- Akses awal: `platform_admin`. Peran yang lebih sempit ditambahkan ke RBAC saat dibutuhkan, **tanpa mengubah peran yang ada**:
  - `pusat_kurikulum`: kurikulum, konten, dan antrean usulan AI
  - `pusat_ai`: pengaturan model AI dan level otonomi (perubahan ini berdampak ke biaya dan kualitas seluruh platform, jadi dipisah dari peran lain)
  - `pusat_bisnis`: penjualan dan peserta
  - `pusat_viewer`: hanya baca
- Setiap tindakan admin (menyetujui usulan AI, mengubah level otonomi, rollback versi) masuk **log audit** permanen (siapa, kapan, apa, alasan).

### 2. Isi dashboard

| Halaman | Menjawab | Sumber |
|---|---|---|
| **Ringkasan** | kondisi platform hari ini dalam satu layar: peserta aktif, pendaftar baru, pendapatan hari ini/bulan ini, usulan AI menunggu, peringatan | agregat semua domain |
| **Peserta** | berapa yang aktif (harian/mingguan/bulanan); corong onboarding → modul pertama → aktif minggu ke-2; retensi per kohort; sebaran jenjang/tujuan/organisasi | `users`, `user_learning_profiles`, `learning_events` |
| **Pembelajaran** | modul/kuis selesai, waktu belajar, sebaran penguasaan per mapel & tahap, hasil tryout, bab tersulit se-platform | `learning_events`, statistik ADR-0013 L2 |
| **Kurikulum & Konten** | cakupan kurikulum (topik yang sudah berisi Modul Belajar + latihan dari 4.949), progres generate AI, sebaran taksonomi per tahap (vs target), konten dengan health score terendah | `modules`, `module_items`, statistik butir |
| **Usulan AI** | antrean usulan perubahan konten: diff, bukti data, skor QA; tombol setujui / tolak / minta revisi; riwayat keputusan; pengaturan level otonomi per jenis perubahan | `content_findings`, `content_proposals` (ADR-0013) |
| **Kelas & Guru** | sesi terjadwal vs terlaksana, tingkat kehadiran per kelas/organisasi, kecepatan guru menilai, ulasan tutor | `class_sessions`, `session_participant_records`, `org_*`, `tutor_reviews`, `assignment_submissions` |
| **Penjualan** | pendapatan per jenis (`orders.kind`), langganan aktif, MRR, churn, konversi gratis → berbayar, GMV marketplace, perputaran diamond (kredit masuk/terpakai), iklan ditonton | `orders`, `subscriptions`, `transactions`, `credits`, `learning_products`, `enrollments`, `ad_views` |
| **Operasional AI** | panggilan & token per fitur/model, biaya, tingkat gagal, tingkat 429/Vertex sibuk, kesehatan antrean job | `ai_tasks`, `jobs` |
| **Pengaturan AI** | model untuk setiap peran AI (fitur & agen), model cadangan, temperatur, batas token, anggaran harian; katalog model & harganya; tombol uji model; riwayat perubahan | `ai_model_catalog`, `ai_role_settings` (ADR-0013 §3.5) |
| **Organisasi** | daftar organisasi dan ukuran/aktivitas masing-masing, dengan tautan ke konsol `/organisasi`-nya | `organizations`, `user_organization_roles` |

Setiap angka punya **periode** (hari ini / 7 hari / 30 hari / rentang), **pembanding** (vs periode sebelumnya), dan **drill-down** ke daftar di baliknya.

### 3. Arsitektur data
- **Dashboard tidak pernah menjalankan query analitik berat di tabel transaksi saat halaman dibuka.** Angka dibaca dari **tabel agregat** (`metrics_daily_*`: per hari × dimensi seperti organisasi, mapel, jenjang) yang dihitung ulang oleh job di antrean generik `jobs` (dibangun di Fase 40, dipakai juga oleh agen AI ADR-0013 di Fase 42).
- Agregat harian dihitung ulang untuk **3 hari terakhir** pada setiap putaran, supaya data yang datang terlambat (pembayaran tertunda, event offline) tetap masuk.
- "Hari ini" dihitung langsung dari tabel sumber dengan query ringan yang berindeks. Selebihnya dari agregat.
- Zona waktu pelaporan: **WIB (Asia/Jakarta)**, disimpan eksplisit di setiap agregat, supaya "hari ini" tidak bergeser 7 jam.
- Setelah migrasi GCP, event dan agregat bisa diekspor ke BigQuery untuk analisis ad-hoc. Admin Pusat tetap membaca agregat Postgres, jadi dashboard tidak bergantung pada BigQuery.

### 4. Laporan & peringatan
- **Laporan otomatis** dari agen Pelapor (ADR-0013): ringkasan harian dan mingguan, berisi angka utama, perubahan penting, usulan AI yang menunggu, dan anomali. Ditampilkan di Ringkasan, dengan opsi dikirim lewat email.
- **Peringatan berbasis aturan (deterministik, bukan AI)**, misalnya: pendapatan harian turun >40% vs rata-rata 7 hari, tingkat gagal AI >10%, antrean job macet >1 jam, kehadiran kelas turun di bawah ambang, atau bab yang health score-nya jatuh di bawah 70.

### 5. Privasi
- Halaman agregat tidak menampilkan data pribadi. Drill-down ke individu hanya untuk peran yang berhak, dan setiap pembukaan data individu dicatat di log audit.
- Ekspor data pribadi (CSV) memerlukan izin terpisah dan tercatat, sejalan dengan bagian Privasi ADR-0013 (UU No. 27/2022).

### 6. Tahapan (Fase 40, bisa paralel dengan Fase 39 ADR-0013)
1. Kerangka `/admin` + gerbang `platform_admin` + log audit.
2. Tabel `metrics_daily_*` + job agregasi.
3. Halaman **Ringkasan, Penjualan, Peserta (dasar), Kurikulum & Konten (cakupan), Operasional AI**. Semua sumbernya sudah ada hari ini.
4. **Pengaturan AI**: katalog model + pengaturan per peran, dan semua 26 titik kode yang sekarang membaca model dari `Config` dipindahkan ke resolver pengaturan. Diisi awal dengan `gemini-3.8-flash` (Vertex) untuk teks & vision, serta STT/TTS OpenRouter yang sedang dipakai.
5. Setelah Fase 39: Peserta aktif & retensi, Pembelajaran, Kelas & Guru.
6. Fase 42: halaman **Usulan AI** (prasyarat agen konten semi-otonom).

## Alternatives considered

- **Tool BI eksternal (Metabase/Looker Studio) sebagai dashboard.** Ditolak sebagai solusi utama. Cocok untuk angka baca-saja, tetapi Admin Pusat juga harus **bertindak** (menyetujui usulan AI, mengatur otonomi, rollback versi) dengan RBAC dan log audit Titian sendiri. Tool eksternal tetap boleh dipakai tim internal untuk analisis ad-hoc di atas agregat.
- **Menghitung semua angka langsung dari tabel sumber.** Ditolak. Setelah `learning_events` berjalan (ADR-0013), query langsung akan membebani database produksi setiap kali dashboard dibuka.
- **Memperluas `/organisasi` menjadi Admin Pusat.** Ditolak. Konsol organisasi dibatasi satu organisasi dan dipakai pelanggan. Mencampur tampilan lintas organisasi ke dalamnya membuka risiko kebocoran data antarorganisasi.

## Consequences

- Pengelola platform akhirnya punya satu tempat untuk melihat peserta, penjualan, kurikulum, kelas, dan biaya AI.
- Agen konten ADR-0013 punya jalur persetujuan manusia yang jelas. Semi-otonomi bisa berjalan dengan aman.
- Ada beban baru berupa job agregasi dan tabel agregat. Keduanya memakai antrean yang sama dengan agen AI, sehingga kesehatan antrean menjadi metrik yang wajib dipantau.
- Angka "peserta aktif" dan "pembelajaran" baru bermakna setelah Fase 39 mencatat event. Sebelum itu, halamannya menampilkan "belum cukup data", bukan angka nol yang menyesatkan.
