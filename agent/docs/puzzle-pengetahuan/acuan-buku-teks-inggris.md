# Acuan buku teks Bahasa Inggris per kelas

Status: dikumpulkan 2026-11-03 untuk menyusun jalur `inggris-kurikulum-indonesia` per kelas. Sumbernya buku siswa resmi Kurikulum Merdeka dari Pusat Perbukuan. PDF diunduh dari salinan `static-sc.cloudapp.web.id/content/pdf/bukuteks/kurikulum21/`, karena server resmi tidak terjangkau dari mesin dev. PDF, teks, dan peta per buku (`peta-*.json`) ada di `~/.cache/titian-qa-tmp/bse-en/`. Gabungannya ada di `titian-backend-go/data/kanonik/sumber/buku-teks-inggris.json`.

**Bahasa Inggris wajib mulai Fase B (Kelas III)** menurut CP 046/2025. Karena itu tidak ada buku Kelas I–II, dan seri English for Nusantara Kids dimulai dari jilid 1 untuk Kelas III. CP hanya menetapkan keterampilan dan target CEFR: A1 di Fase B–C, A2 di Fase D, B1 di Fase E, dan B2 di Fase F. Jumlah kosakata berfrekuensi tinggi yang ditargetkan berturut-turut 1000, 2000, 3000, dan 4000 kata. CP tidak menyebut tata bahasa.

| Kelas | Fase | Berkas | Judul (tahun) | Bab |
|---|---|---|---|---|
| III | B | `Inggris_FN_BS_KLS_III` | English for Nusantara Kids (2024) | My Self; My Family; My Family's Activities at Home; My School; My Classroom; My Teacher |
| IV | B | `Inggris_FN_BS_KLS_IV` | English for Nusantara Kids (2024) | My Morning Routine; Meal Time; My Toys; My School Activities; My PE Class; My School Days |
| V | C | `Inggris_FN_BS_KLS_V` | English for Nusantara Kids (2024) | Buying Some Mangoes and Spinach; In the Kitchen; Visiting Bara's House; A Market Day; At the Library; Reading a Lot of Stories |
| VI | C | `Inggris_FN_BS_KLS_VI` | English for Nusantara Kids (2024) | Healthy Vegetables; Our Hygiene Habits; A Trip to the Zoo; Let's Play!; Having Fun in Our After-School Club; Our School Project |
| VII | D | `Bahasa-Inggris-BS-KLS-VII` | English for Nusantara (2022) | The Beginning; About Me; Culinary and Me; Home Sweet Home; My School Activities; This is My School |
| VIII | D | `Bahasa-Inggris-BS-KLS-VIII-nsn` | English for Nusantara (2022) | The Beginning; Celebrating Independence Day; Kindness Begins with Me; Love Our World; No Littering; Embrace Yourself |
| IX | D | `Inggris_BS_KLS_IX` | English for Nusantara (2022) | The Beginning; Exploring Fauna of Indonesia; Taking Trips; Journey to Fantasy Worlds; Upcycling Used Materials; Digital Life |
| X | E | `Bahasa-Inggris-BS-KLS-X` | Work in Progress (2022) | Great Athletes; Sports Events; Sports and Health; Healthy Foods; Graffiti; Fractured Stories |
| XI | F | `Bahasa-Inggris-BS-KLS-XI-efc` | English for Change (2022) | Digital Literacies and My Identities; Love Your Environment; Healthy Life for a Healthy Future; Indonesian Environmental Figures; Personal Money Management |
| XII | F | `Inggris_BS_KLS_XII` | Life Today (2022) | Narrative Text: The Story of a Friendly Future; Argumentative Text: E-Money; Hortatory Exposition: Netiquette; Discussion Text: Carbon Footprint |
| XI lanjut | F | `Inggris_BS_KLS_XI_TL_Rev` | Let's Elevate Our English (2024) | Are We Connected to Nature?; Discovering Ourselves; Why is Water Important?; Why Should We Live a Healthy Life? |
| XII lanjut | F | `Inggris_Lanjut_BS_KLS_XII` | Train of Thoughts (2022) | Digging the Hidden Gem of Borneo; Connected to Social Media; Get in Touch With Nature; Future Method of Payment; Today's Life |

## Cara memetakan

Ada 242 subbab yang dipetakan. Tiap subbab punya bukti halaman PDF. Yang dihitung hanya unsur yang dijadikan fokus: tujuan pembelajaran, kotak tata bahasa atau ungkapan, jenis teks yang dibahas strukturnya, keterampilan yang dilatih secara eksplisit, dan kosakata tema. Kata yang hanya kebetulan muncul di bacaan tidak dihitung.

Pemetaannya dikerjakan empat agen secara paralel, satu per jenjang. Setelah itu sampel buktinya dicek langsung ke halaman PDF.

Ada beberapa catatan khusus:

- **Kelas X:** tata bahasa hanya tercantum di tabel Scope & Sequence (h. 12–14), tanpa kotak atau latihan di dalam bab. Tata bahasa ini dicatat di field `scope`.
- **Ketidakcocokan dengan isi buku:** kadang Scope & Sequence atau label buku tidak cocok dengan isinya, dan pemetaan mengikuti isi. Contohnya, teks "linear narrative" di Kelas XI unit 4 adalah kisah hidup tokoh nyata, sehingga dipetakan sebagai recount. Lalu Kelas VIII Ch1 U3 disebut kartu ucapan, padahal isinya recount.
- **Kesalahan di buku:** Kelas XI Tingkat Lanjut h. 117 menukar contoh noun clause dengan adjective clause. Deck tidak boleh menyalin kesalahan ini.

## Yang tidak diajarkan buku

Buku-buku ini berbasis tema dan jenis teks, dan banyak tata bahasa tidak pernah dijadikan fokus. Contohnya future will dan going to, present perfect, used to, past perfect, conditional 2 dan 3, serta indirect question. Totalnya 67 unit setingkat A1–B2 tidak diajarkan buku mana pun.

Jalur Kurikulum Indonesia mengisi unit-unit ini menurut target CEFR di CP. Unitnya disebar ke kelas-kelas dalam fasenya mengikuti urutan prasyarat. Unit C1 dan C2 tidak masuk jalur sekolah. Isian ini dihitung hanya dari buku wajib. Dengan begitu, materi yang hanya ada di buku Tingkat Lanjut tetap sampai ke semua siswa. Contohnya must dan have to, yang hanya diajarkan di Tingkat Lanjut XII, masuk ke Kelas 9.

Daftar lengkapnya dicetak oleh `python3 data/kanonik/sumber/cek_cakupan.py`.
