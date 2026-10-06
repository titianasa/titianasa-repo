# ADR-0015: Grup Belajar, Grup Kelas, Ruang Kelas & Liga

Status: Accepted (arah, kuota, dan nama disetujui user 2026-09-21; asumsi di §9 menunggu konfirmasi)
Date: 2026-09-21
Supersedes: -
Superseded by: -
Related: ADR-0002 (mastery), ADR-0003 (FRSS), ADR-0005 (credit economy), ADR-0006 (RBAC), ADR-0013 (AI Learning Engine), ADR-0014 (Admin Pusat)

## Context

`titian-web` sudah punya fitur Grup dan Liga (`/grup`, `store/group-store.ts`, `lib/group-mock-data.ts`, `components/group/*`, ±8.000 baris). **Seluruhnya data tiruan di browser** (persist localStorage). Backend tidak punya route/tabel grup. Yang ada hanya liga tier per pengguna (`services/league.rs`, `GET /me/league`, `GET /leaderboard/weekly`).

Masalah pada prototipe yang membentuk keputusan ini:
- Skor liga hard-code (720/350/650/200), tidak pernah dihitung dari aktivitas belajar.
- Identitas `"user-me"` / `"Kamu (John)"` dan cek `name.includes("Kamu")` tersebar di UI.
- `evaluateSeasonProgression` hanya mengubah label; peserta tidak dipindah divisi, skor tidak di-reset, musim tidak punya tanggal sungguhan.
- `purchaseGroupAccess`, kuota anggota, dan kode undangan tidak ditegakkan (semua di klien; kode pakai `Math.random()`).
- Absensi, sertifikat, "convert to class" ditiru ulang di sisi grup padahal backend sudah punya `cohorts`, `attendance_records`, `certificates`, `class_sessions` (Phase 9, 16, 19, 28).

Keputusan produk user (2026-09-21): aplikasi belum live, jadi struktur kelas lama **boleh dihapus/disesuaikan**. Grup dijadikan cara belajar bersama yang **fleksibel** dan terikat ke langganan Plus/Pro.

## Decision

### 1. Tiga konsep dan namanya

| Nama di UI | Apa | Siapa yang boleh buat |
|---|---|---|
| **Grup Belajar** | Kelompok belajar bebas. Punya anggota, konten yang di-attach, target, dan liga. | Plus, Pro |
| **Ruang Kelas** | **Payung** pengajaran. Punya guru/pemilik, jadwal & sesi, absensi, sertifikat, penilaian, dan (opsional) harga. Berisi 1..n Grup Kelas. | Pro |
| **Grup Kelas** | Grup Belajar yang tergabung di satu Ruang Kelas (Kelas A, Kelas B, ...). Mewarisi fitur pengajaran Ruang Kelas. | Pro (dibuat baru di dalam Ruang Kelas, atau hasil "convert" dari Grup Belajar) |

Grup Global (`kind='global'`) adalah grup sistem, di luar tiga di atas (§4).

### 2. Matriks hak per tier

| Kemampuan | Gratis | Plus | Pro |
|---|---|---|---|
| Ikut Grup Belajar | maks **3** | maks **1000** | maks **1000** |
| Buat Grup Belajar | tidak | maks **50** | maks **100** |
| Anggota per grup | - | Grup Belajar maks **100** | Grup Belajar maks **100**; Grup Kelas maks **1000** |
| Target grup, attach konten, liga sederhana | tidak | ya | ya |
| Liga aktif per grup | - | **3** (asumsi §9) | tanpa batas praktis |
| Liga berjenjang (sirkuit divisi, naik/turun) | tidak | tidak | ya |
| Buat Ruang Kelas, Grup Kelas | tidak | tidak | ya |
| Convert Grup Belajar → Grup Kelas | tidak | tidak | ya |
| Absensi, sesi terjadwal, sertifikat, penilaian di Grup Kelas | tidak | tidak | ya |
| Monetisasi (Ruang Kelas berbayar) | tidak | tidak | ya |

Aturan tegas:
- **Semua batas dicek di backend**, lewat `subscription::entitlements()` yang diperluas (bukan di klien). Angka kuota hidup di **satu fungsi** `group_limits(tier)`, supaya mengubah angka = mengubah satu tempat.
- Grup Global tidak menghabiskan kuota join.
- **Downgrade tidak menghapus apa pun.** Grup dan liga yang sudah ada tetap ada dan bisa dibaca. Yang berhenti: membuat baru di atas kuota baru, dan fitur khusus tier yang hilang (Grup Kelas beku: tidak bisa buat sesi/absensi/sertifikat/liga baru; data lama tetap terlihat).

### 3. Gamifikasi: satu XP global, liga = jendela pandang

- XP tetap ditulis **sekali** ke `xp_events` (Phase 8). **Tidak ada mata uang XP kedua.**
- **Poin Liga** adalah angka terpisah yang **dihitung on-read** dari sumber data aslinya (attempt, exam session, event belajar) dalam **jendela musim**, sesuai **aturan skor** liga tersebut. Poin liga tidak pernah ditulis oleh klien.
- Poin Liga, XP, dan Mastery **tiga hal berbeda** (mengikuti §6.1 roadmap dan guard di STATE.md). Peringkat liga tidak masuk `mastery.compute` / `frss.apply`. Liga hanya membaca.
- **Hadiah XP liga** (bonus juara) diberikan saat musim ditutup, lewat `xp_events` dengan `reference = "league:{season_id}:{user_id}"` (idempoten), dengan **batas bonus per pengguna per minggu** agar liga tidak menjadi mesin farming XP.

**Bentuk liga (`format`) menentukan sumber skor**, karena liga dipakai untuk banyak keperluan:

| `format` | Contoh pemakaian | Sumber poin liga | Aturan skor (`scoring_rule`) |
|---|---|---|---|
| `tryout` | Tryout bersama sekelas | 1 `assessment` yang di-attach | `best_attempt` / `first_attempt` |
| `ujian` | Ujian harian, ujian simulasi | 1 `assessment` yang di-attach, jendela waktu ketat | `first_attempt` (1 kali kesempatan) |
| `latihan` | Latihan soal grup di kelas | bank soal / modul yang di-attach | `accuracy_weighted` atau `count` (banyak soal benar) |
| `learning_path` | Liga per learning path | kemajuan + kenaikan mastery pada path itu | `path_progress` |
| `olimpiade` | Olimpiade, kompetisi terbuka | beberapa `assessment` (babak) | `sum_of_rounds` dengan tie-break waktu |
| `aktivitas` | Liga mingguan kebiasaan belajar | COUNT event belajar (bukan SUM XP) | `activity_count` |
| `manual` | **Ujian beneran** (tatap muka/di luar aplikasi) | nilai yang **dimasukkan guru** | `manual` |

Atribut lain di liga:
- `integrity`: `casual` atau `proctored`. `proctored` memakai pengawasan yang sudah ada (`item_proctor`, `item_guard`, halaman `/pengawasan`); dipilih untuk `ujian` simulasi dan `olimpiade`.
- `xp_policy`: `normal` (XP belajar biasa tetap berjalan), `bonus_only`, atau `none`. **Ujian beneran (`manual`) selalu `none`**: nilai resmi tidak boleh diberi imbalan XP.
- **Tie-break deterministik**: poin ↓, lalu waktu penyelesaian/pencapaian lebih cepat, lalu `user_id`. Sama di semua format.
- **Musim (`cadence`)**: `one_off` (tryout, ujian, olimpiade: satu jendela, tanpa promosi) atau `weekly`/`monthly`/`custom` (berulang, boleh berjenjang).

### 4. Semua liga berada di dalam grup, termasuk yang global

- Liga **wajib** milik satu grup. Tidak ada liga tanpa grup.
- **Grup Global** (`kind='global'`, satu baris, di-seed migrasi) berisi seluruh pengguna **secara implisit** (tidak ada baris anggota per pengguna, supaya tidak jutaan baris). Liga global mingguan (`format='aktivitas'`) memakai **rumus gabungan yang sudah ada di `services/league.rs`** (streak berbatas 30 hari + rata-rata mastery yakin-saja + COUNT event) sehingga tetap tahan "dibeli" dengan XP.
- `GET /me/league` dan `GET /leaderboard/weekly` **tidak diubah kontraknya**; keduanya kelak membaca lewat kode yang sama dengan liga global (tidak ada dua implementasi rumus).

### 5. Ruang Kelas: penerus `cohorts`, bukan tabel kedua

- Tabel fisik **`cohorts` dipakai sebagai Ruang Kelas**; **tidak di-rename secara fisik** di P45–P49 (menghindari sentuhan ke ±10 service: enrollment, attendance, certificate, class_session, gradebook, dst.). "Ruang Kelas" adalah nama domain di UI, kontrak API, dan dokumen. Rename fisik boleh dijadwalkan terpisah.
- Perubahan pada `cohorts` (aditif): `product_id` menjadi **nullable** (Ruang Kelas gratis/tidak dijual tidak perlu produk), tambah `owner_id`, `description`, `status`.
- **Grup Kelas** = `study_groups` dengan `kind='kelas'` dan `cohort_id` terisi. Satu Ruang Kelas boleh punya banyak Grup Kelas.
- Anggota Grup Kelas wajib punya `enrollments` di Ruang Kelas itu. Bergabung ke Grup Kelas otomatis membuat enrollment (status mengikuti harga, §7).
- `class_sessions` mendapat `group_id` nullable: sesi bisa untuk **satu Grup Kelas** (roster = anggota grup ∩ enrollment aktif) atau untuk seluruh Ruang Kelas (`group_id` null).
- Sertifikat tetap diterbitkan **per enrollment** (mekanisme Phase 9/19 tidak berubah).
- **`org_classes` (LMS organisasi/sekolah, Phase 15–18) tidak diubah.** Itu konsol institusi terpisah. Apakah kelak digabung ke Ruang Kelas adalah keputusan sendiri (asumsi §9).
- Halaman lama `/kelas` (siswa) dan `/mengajar` (guru) **diadaptasi**, bukan dibuang: `/kelas` menjadi daftar Ruang Kelas yang diikuti, `/mengajar` menjadi konsol Ruang Kelas milik guru.

### 6. Attach konten Titian ke grup

Grup **tidak menyalin** konten. `group_content` menyimpan **referensi**: `kind` ∈ {`learning_path`, `module_item`, `assessment`, `question_bank`} + `ref_id` + urutan + tenggat opsional.
- Progres anggota dibaca dari `learning_events` / `item_progress` / `attempts` yang sudah ada (satu sumber kebenaran).
- Hanya konten yang **boleh dilihat** pembuat grup yang bisa di-attach (draft milik orang lain ditolak, pola 404 "jangan bocorkan keberadaan").
- Konten yang butuh langganan tetap mengikuti entitlement **masing-masing anggota**; grup tidak membuka paywall.
- **Target grup** (`group_targets`) dihitung on-read dari event nyata dalam periode target, bukan counter yang ditulis klien.

### 7. Monetisasi, hanya di level Ruang Kelas

- Harga melekat di **Ruang Kelas** lewat `learning_products` yang ada (QRIS stub + wallet 30/70, ADR-0005/Phase 9). Grup Belajar (Plus) **tidak bisa dijual**.
- Akses dicek di backend lewat `enrollments.status` (`active`), bukan flag klien.
- **Convert Grup Belajar → Grup Kelas tidak pernah mengeluarkan anggota.** Bila Ruang Kelas tujuan berbayar, anggota lama mendapat enrollment `pending`: tetap di grup dan melihat obrolan/liga, tetapi tab khusus kelas (absensi, sertifikat, materi kelas) terkunci sampai membayar.
- Un-link Grup Kelas menjadi Grup Belajar hanya boleh bila belum ada absensi/sertifikat yang terbit; selain itu grup **diarsipkan**, bukan diputus.

### 8. Liga berjenjang (Pro)

- **Sirkuit** (`league_circuits`) = beberapa liga dalam satu grup dengan `tier` 1 (teratas) sampai N. Anggota baru masuk tier terbawah.
- Penutupan musim **satu sirkuit sekaligus**: hitung hasil semua divisi dari **snapshot beku dulu**, baru terapkan perpindahan. Dengan begitu orang yang baru naik tidak ikut dievaluasi lagi di divisi tujuan pada musim yang sama.
- Aturan: `promotion_slots` & `relegation_slots` per divisi; tier 1 tidak punya promosi, tier terbawah tidak punya degradasi; **poin 0 tidak boleh dipromosikan** (boleh didegradasi); promosi dan degradasi tidak boleh beririsan (`relegated` diambil dari sisa setelah `promoted`); **tamu (guest) tidak ikut perpindahan**.
- Setiap perpindahan tercatat (`league_movements`) sebagai riwayat.
- Penutupan musim dijalankan job terjadwal di antrean `jobs` (ADR-0014/P40-002), **idempoten** (status musim berpindah lewat `UPDATE ... WHERE status='active'` sebagai klaim), waktu batas musim dalam **WIB**.

### 9. Asumsi yang menunggu konfirmasi user
1. Kuota "50/100 grup" dibaca sebagai **grup yang boleh dibuat**; "1000/1000" dibaca sebagai **grup yang boleh diikuti** (praktis tanpa batas). Bila maksud user berbeda (mis. 50/100 = grup yang diikuti, 1000 = anggota per grup), cukup ubah `group_limits()`.
2. ~~Batas anggota per grup~~ **Dikonfirmasi user 2026-09-21: Grup Belajar 100 anggota, Grup Kelas 1000 anggota** (kapasitas mengikuti jenis grup, bukan tier pemilik). Menjadi nilai default `study_groups.max_members` saat dibuat/di-convert.
3. Liga aktif per grup untuk Plus: **3**; Pro tanpa batas praktis.
4. Batas bonus XP liga per pengguna per minggu: awal **500 XP** (angka kerja; ubah lewat konfigurasi).
5. Kelak `org_classes` (sekolah) digabung ke Ruang Kelas atau tetap terpisah: **ditunda**, di luar Phase 45–50.
6. Downgrade: tanpa masa tenggang (langsung beku sesuai §2). Bisa ditambah grace period bila diminta.

### 10. Privasi & keamanan
- Bergabung ke liga berarti nama tampilan terlihat di papan peringkat grup itu. Papan **Grup Global** menyediakan **opt-out** (tampil sebagai alias "Pelajar #xxxx").
- Poin liga berbasis event hanya dihitung dari event yang **persetujuannya aktif** (P39-007); tanpa persetujuan, pengguna tetap bisa ikut liga berbasis attempt (skor jawaban eksplisit), tetapi tidak liga `aktivitas`.
- Kode undangan: acak kriptografis (bukan `Math.random`), bisa kedaluwarsa, dibatasi jumlah pakai, dan bisa dicabut. Endpoint join dibatasi laju (Redis, pola P39-005).
- Aksi admin grup (hapus anggota, ubah peran, tutup liga, ubah nilai manual) masuk **log audit** (pola `admin_audit`).
- Nilai `manual` hanya bisa diisi/diubah oleh owner/admin grup, dan setiap perubahan tercatat.

## Consequences

- Satu sumber kebenaran skor (data belajar asli): peringkat tidak bisa dipalsukan klien, dan konsisten dengan profil global.
- Grup tidak menduplikasi absensi/sertifikat: fitur pengajaran yang sudah teruji dipakai ulang lewat `cohort_id`.
- Fitur `weekly_xp` mentah dari prototipe **dihapus**; diganti `aktivitas` (COUNT) demi ketahanan terhadap farming XP.
- Pekerjaan frontend besar: `group-store.ts` (1.011 baris) dan `group-mock-data.ts` (1.108 baris) diganti hook react-query per fase; mock hanya tersisa sebagai seed dev.
- Menambah dua konsep baru untuk pengguna (Ruang Kelas vs Grup Kelas). Copy UI harus menjelaskannya singkat (payung vs kelompok).
