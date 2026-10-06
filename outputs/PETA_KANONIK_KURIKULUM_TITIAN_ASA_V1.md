# Peta Kanonik Kurikulum Titian Asa v1

Status: rancangan normalisasi katalog awal 48 rumpun. Dokumen ini tidak menghapus cakupan; ia menentukan letak yang benar agar aset pembelajaran tidak diproduksi berulang.

## 1. Keputusan arsitektur

Katalog lama memakai kata “mapel” untuk empat hal berbeda: disiplin inti, bundel kurikulum sekolah, spesialisasi, serta target ujian/karier. Keempatnya dipisahkan sebagai berikut.

| Kelas aset | Fungsi | Boleh memiliki materi kanonik sendiri? |
|---|---|---|
| Domain/mata pelajaran inti | rumah jangka panjang bagi konsep reusable | Ya |
| Strand | cabang stabil dalam mata pelajaran | Ya, sebagai organisasi konsep |
| Bundel kurikulum | susunan konsep inti untuk fase/kelas/standar tertentu | Tidak; hanya referensi |
| Learning path | rute menuju tujuan, ujian, sertifikasi, atau pekerjaan | Tidak; hanya referensi, kecuali strategi khusus target |
| Spesialisasi | kompetensi lanjut/kejuruan yang punya konsep khas | Ya, setelah standar kompetensi tersedia |

## 2. Domain kanonik v1

| Kode | Domain | Strand awal |
|---|---|---|
| `mathematics` | Matematika | bilangan, aljabar, geometri-pengukuran, data-peluang, kalkulus, penalaran |
| `indonesian` | Bahasa Indonesia | menyimak, membaca, berbicara, menulis, kebahasaan, sastra |
| `english` | Bahasa Inggris | receptive, productive, grammar, vocabulary, pronunciation |
| `other_languages` | Bahasa lain | empat keterampilan, sistem bunyi/tulisan, tata bahasa, budaya |
| `science` | Sains | keterampilan ilmiah, fisika, kimia, biologi, bumi-antariksa |
| `social_sciences` | Ilmu Sosial & Kewargaan | sejarah, geografi, ekonomi, sosiologi, antropologi, pendidikan Pancasila |
| `computing` | Informatika & Literasi Digital | sistem, data, pemrograman, jaringan, keamanan, AI literacy |
| `arts_health_life` | Seni, Kesehatan & Keterampilan Hidup | seni, PJOK, kesehatan, prakarya, literasi finansial/kewirausahaan |
| `religious_studies` | Keagamaan | pendidikan agama per tradisi; studi Islam lanjutan |
| `career_vocational` | Karier & Kejuruan | akuntansi, bisnis, otomotif, kompetensi kerja lain |
| `reasoning` | Penalaran lintas-domain | logika, argumentasi, pemecahan masalah, literasi kuantitatif |

`reasoning` merupakan layanan lintas-domain: konsepnya tetap kanonik, tetapi dapat dimasukkan ke Matematika, Bahasa Indonesia, Informatika, UTBK, TKA, CPNS, dan BUMN tanpa salinan.

## 3. Pemetaan 48 rumpun saat ini

| Rumpun lama | Posisi baru | Keputusan produksi |
|---|---|---|
| Akhlak Tasawuf | `religious_studies.islamic_advanced` | spesialisasi lanjut; tetap terpisah dari kurikulum madrasah dasar |
| Akidah Akhlak | `religious_studies.islamic_madrasah` | inti madrasah; gunakan strand akidah dan akhlak |
| Akuntansi | `career_vocational.accounting` | spesialisasi/kejuruan; petakan ke kompetensi kerja, bukan kelas generik |
| Al-Qur'an Hadis | `religious_studies.islamic_madrasah` | inti madrasah; koreksi nomenklatur “Hadis” |
| Antropologi | `social_sciences.anthropology` | spesialisasi sosial tingkat lanjut; konsep dapat dipakai Sosiologi/Geografi |
| Bahasa Arab | `other_languages.arabic` | mata pelajaran bahasa; jalur keagamaan hanya mereferensikan bila perlu |
| Bahasa Indonesia | `indonesian` | materi inti P0 |
| Bahasa Inggris | `english` | materi inti P0; CEFR sebagai skala kemampuan, bukan mapel terpisah |
| Bahasa Jepang | `other_languages.japanese` | bahasa pilihan P2 |
| Bahasa Jerman | `other_languages.german` | bahasa pilihan P2 |
| Bahasa Korea | `other_languages.korean` | bahasa pilihan P2 |
| Bahasa Mandarin | `other_languages.mandarin` | bahasa pilihan P2 |
| Bahasa Prancis | `other_languages.french` | bahasa pilihan P2 |
| Biologi | `science.biology` | materi inti P1 |
| Bisnis & Manajemen | `career_vocational.business` | spesialisasi/kejuruan; berbagi konsep dengan Ekonomi/Kewirausahaan |
| Ekonomi | `social_sciences.economics` | materi inti P1 |
| Filsafat | `reasoning.philosophy` | spesialisasi lanjut; konsep argumentasi dipakai lintas-domain |
| Fiqih | `religious_studies.islamic_madrasah` | inti madrasah |
| Fisika | `science.physics` | materi inti P1 |
| Geografi | `social_sciences.geography` | materi inti P1 |
| IPA | bundel `science` Fase A–D | tidak membuat konsep sains kedua; hanya menyusun konsep lintas-sains |
| IPAS | bundel `science` + `social_sciences` Fase B–C | tidak membuat konsep ketiga; hanya susunan fase sekolah dasar |
| IPS | bundel `social_sciences` Fase D | tidak membuat konsep sosial kedua; hanya susunan fase/kelas |
| Ilmu Hadis | `religious_studies.islamic_advanced` | spesialisasi lanjut; hubungan ke Al-Qur'an Hadis eksplisit |
| Ilmu Kalam | `religious_studies.islamic_advanced` | spesialisasi lanjut |
| Ilmu Tafsir | `religious_studies.islamic_advanced` | spesialisasi lanjut |
| Informatika | `computing` | materi inti P1 |
| Kimia | `science.chemistry` | materi inti P1 |
| Matematika | `mathematics` | materi inti P0 |
| PJOK | `arts_health_life.physical_education` | materi inti P1; tambah kesehatan/keselamatan sesuai jenjang |
| Penalaran & Logika | `reasoning` | layanan lintas-domain; bukan salinan materi UTBK/TKA |
| Pendidikan Agama Buddha | `religious_studies.buddhist` | pendidikan agama; struktur per tradisi setara |
| Pendidikan Agama Hindu | `religious_studies.hindu` | pendidikan agama; struktur per tradisi setara |
| Pendidikan Agama Katolik | `religious_studies.catholic` | pendidikan agama; gunakan nama tampil “… dan Budi Pekerti” bila sesuai acuan |
| Pendidikan Agama Khonghucu | `religious_studies.confucian` | pendidikan agama; struktur per tradisi setara |
| Pendidikan Agama Kristen | `religious_studies.christian` | pendidikan agama; gunakan nama tampil “… dan Budi Pekerti” bila sesuai acuan |
| Pendidikan Kewarganegaraan | `social_sciences.civic_education` | ubah nama tampil menjadi Pendidikan Pancasila bila memakai nomenklatur kini |
| Prakarya & Kewirausahaan | `arts_health_life.craft_entrepreneurship` | inti/keterampilan hidup; konsep bisnis direferensikan dari Ekonomi/Bisnis |
| Psikologi | `social_sciences.psychology` | spesialisasi lanjut; jangan dijadikan terapi atau diagnosis klinis |
| Sastra Indonesia | strand `indonesian.literature` | gabungkan ke Bahasa Indonesia, bukan mapel kanonik terpisah |
| Sejarah | `social_sciences.history` | materi inti P1 |
| Sejarah Kebudayaan Islam | `religious_studies.islamic_madrasah` | inti madrasah; gunakan kode permanen, bukan `custom` |
| Seni Budaya | `arts_health_life.arts` | pecah menjadi seni rupa, musik, tari, teater; bundel sekolah hanya mereferensikan |
| Sosiologi | `social_sciences.sociology` | materi inti P1 |
| Teknik Otomotif | `career_vocational.automotive` | satu program keahlian awal, bukan representasi seluruh SMK |
| Ushul Fikih | `religious_studies.islamic_advanced` | spesialisasi lanjut |
| Wawasan ASN & Kepegawaian | path `career.public_service` | bukan mapel inti; konsep hukum/kewargaan/karier direferensikan |
| Wawasan BUMN & Dunia Kerja | path `career.bumn` | bukan mapel inti; konsep karier/bisnis/etika direferensikan |

## 4. Normalisasi learning path yang sudah ada

| Path lama | Bentuk baru | Materi khusus yang boleh dimiliki path |
|---|---|---|
| Belajar Bahasa Inggris | fondasi CEFR + sertifikasi | strategi format tes hanya untuk IELTS/TOEFL/TOEIC/PTE/DET |
| Fokus Ujian BUMN | path karier dan rekrutmen | format seleksi, etika proses, latihan sesuai pengumuman terbaru |
| Fokus Ujian CPNS | path ujian berbasis formasi | strategi SKD; SKB wajib dipisah per rumpun/jabatan |
| Fokus Ujian TKA | path asesmen menurut jenjang dan mata uji | blueprint dan format TKA, bukan salinan Matematika/Bahasa |
| Kurikulum Cambridge | bundel kurikulum + sertifikasi | pemetaan syllabus, format ujian, dan sumber resmi |
| Kurikulum Indonesia | bundel CP menurut fase/jenjang | pemetaan CP/fase; kelas hanya filter/tampilan |
| Persiapan Ujian Masuk PT | path ujian dan tujuan studi | strategi ujian dan pemilihan prodi; konsep berasal dari inti |

## 5. Kode dan label yang perlu dimigrasikan

### Kode mapel yang tidak boleh dipakai lagi

Semua kode `custom` harus diganti sebelum produksi: `akidah-akhlak`, `quran-hadis`, `bahasa-inggris`, `bahasa-jepang`, `bahasa-jerman`, `bahasa-korea`, `bahasa-mandarin`, `bahasa-prancis`, `fikih`, dan `ski`.

### Label terstruktur minimum

```text
domain:science
subject:physics
strand:mechanics
concept:linear-motion
framework:kurikulum-merdeka
phase:E
path:tka-sma
content-type:article
language:id
```

Label `jenjang:SMA-10, kurikulum:merdeka-smk` harus dipecah menjadi dua label terpisah. SMK juga tidak boleh memakai identitas SMA sebagai jenjang utama.

## 6. Prioritas produksi

| Prioritas | Yang dibangun | Alasan |
|---|---|---|
| P0 | Matematika, Bahasa Indonesia, Bahasa Inggris | dipakai lintas jalur, paling tinggi manfaat anti-duplikasi |
| P0 | peta CP/fase dan path TKA/UTBK yang hanya mereferensikan inti | membuktikan reuse untuk sekolah dan ujian |
| P1 | Fisika, Kimia, Biologi, Informatika, Ilmu Sosial inti, PJOK/Seni | melengkapi inti sekolah dan jalur pilihan |
| P1 | pendidikan agama dan madrasah | dibangun bersama penelaah ahli per tradisi |
| P2 | bahasa lain, kejuruan, studi Islam lanjut, psikologi/filsafat | perlu standar domain khusus dan reviewer spesialis |
| P2 | CPNS, BUMN, sertifikasi bahasa lengkap | bergantung kebijakan/format eksternal yang harus selalu diperbarui |

## 7. Langkah kerja selanjutnya

1. Sahkan peta ini sebagai struktur v1, lalu buat registry domain/subject/strand/kode.
2. Pecah `Matematika` menjadi peta strand → konsep sebagai pilot pertama.
3. Peta setiap topik/bab Matematika lama ke konsep yang ada; tandai duplikat, gap, dan konten yang tidak memiliki tujuan belajar.
4. Buat satu Unit Belajar emas: `Menjumlahkan Bilangan Bulat Berbeda Tanda`.
5. Tulis tiga path yang hanya merujuk ke unit tersebut: fondasi SMP, TKA SMA (jika relevan pada levelnya), dan remedial adaptif.
6. Setelah pilot diterima, lakukan migrasi bertahap pada Bahasa Indonesia dan Bahasa Inggris.

Tidak ada produksi massal sebelum langkah 2–5 berhasil: jika sebuah konsep masih tidak dapat dipakai ulang pada tiga konteks itu, struktur kanonik belum cukup baik.
