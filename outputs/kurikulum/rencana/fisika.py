from sma_gen import build, N
T2 = "Tahap 2 — Mekanika (SMA)"; T3 = "Tahap 3 — Getaran, Termodinamika & Gelombang"; T4 = "Tahap 4 — Listrik, Magnet & Fisika Modern (SMA)"
build("Fisika", "fis", ["Tahap 2 — Mekanika (SMA)", "Tahap 3 — Getaran%", "Tahap 4 — Listrik%"], "sains-teknologi", "Fisika",
 pindah_grup={"Suhu & Kalor": 10},
 tambah=[
  (10, "START", N("Besaran, Satuan & Analisis Dimensi", T2, "Besaran & Pengukuran", ["Besaran Pokok, Turunan, dan Satuan SI","Dimensi Besaran Fisika","Menggunakan Analisis Dimensi untuk Memeriksa Rumus","Konversi Satuan dan Notasi Ilmiah pada Soal Fisika"], "Dimensi Dianggap Sama dengan Satuan")),
  (10, "Besaran, Satuan & Analisis Dimensi", N("Pengukuran & Ketidakpastian", T2, "Besaran & Pengukuran", ["Jangka Sorong dan Mikrometer Sekrup","Ketidakpastian Pengukuran Tunggal","Ketidakpastian Pengukuran Berulang","Angka Penting dalam Perhitungan","Menyajikan Hasil Pengukuran dalam Grafik"], "Ketidakpastian Dianggap sebagai Kesalahan Orang yang Mengukur")),
  (10, "Gaya Normal & Tegangan Tali", N("Dinamika pada Bidang Miring & Lift", T2, "Dinamika (Hukum Newton)", ["Menguraikan Gaya pada Bidang Miring","Bidang Miring dengan Gesekan","Gaya Normal pada Lift Bergerak","Sistem Dua Benda pada Bidang Miring"], "Gaya Normal Dianggap Selalu Sama dengan Berat Benda")),
  (10, "Daya & Efisiensi", N("Energi Terbarukan & Perubahan Iklim", T2, "Besaran & Pengukuran", ["Sumber Energi Fosil dan Terbarukan","Pembangkit Listrik Surya, Angin, dan Air","Efek Rumah Kaca dan Pemanasan Global","Analisis Dampak dan Solusi Energi Bersih"], "Energi Terbarukan Dianggap Tidak Punya Dampak Lingkungan")),
  (12, "Daya pada Arus Bolak-Balik", N("Gelombang Elektromagnetik & Spektrumnya", T4, "Induksi Elektromagnetik & Arus Bolak-Balik", ["Terbentuknya Gelombang Elektromagnetik","Spektrum Gelombang Elektromagnetik","Sifat dan Cepat Rambat Gelombang Elektromagnetik","Pemanfaatan Gelombang Elektromagnetik dalam Teknologi"], "Gelombang Elektromagnetik Dianggap Membutuhkan Medium")),
 ])
