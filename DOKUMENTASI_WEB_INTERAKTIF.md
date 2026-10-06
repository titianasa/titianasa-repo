# Blueprint & Dokumentasi Teknologi Web Interaktif Titian Asa

Dokumen ini merupakan panduan arsitektur, teknologi, dan implementasi fitur **Web Interaktif** (`:::interactive_web`) pada platform Titian Asa. Fitur ini dirancang untuk mendukung **46 Mata Pelajaran**, **20.000+ Modul**, dan **89.000+ Bab Pembelajaran** di skala nasional.

---

## 1. Arsitektur Sistem

Ekosistem Web Interaktif terdiri dari 4 lapisan:

```mermaid
flowchart TD
    DB[(PostgreSQL)] -->|ALM Block :::interactive_web| Backend[Titian Backend Rust]
    Backend -->|Vertex AI Gemini| AI[Generator Media Interaktif]
    Backend -->|JSON API / ALM Stream| Web[Titian Web Next.js / Content Studio]
    Web -->|srcDoc + Injected Bridge| Iframe[Iframe Interaktif Terisolasi]
    Iframe <-->|postMessage (Titian Bridge)| Web
```

### Keamanan Sandbox & Izin Browser
Iframe dijalankan dengan isolasi terkelola:
- **Sandbox**: `allow-scripts allow-forms allow-modals allow-same-origin`
- **Izin Fitur (`allow`)**: `fullscreen; autoplay; microphone`
- **Kombinasi ini memungkinkan**:
  - Pemuatan library edukasi CDN tepercaya (`cdnjs`, `jsdelivr`).
  - Web Speech API untuk latihan pelafalan (*speaking*) dan audio (*listening*).
  - Mode Layar Penuh (*Fullscreen API*).
  - Isolasi penuh dari cookie dan sesi otentikasi induk platform.

---

## 2. Pustaka & Web API Terkurasi per Kategori Mapel

### A. Matematika & Statistika
- **Pustaka**:
  - `KaTeX` (`https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js`): Formula matematika presisi tinggi dan cepat.
  - `Chart.js` (`https://cdn.jsdelivr.net/npm/chart.js`): Grafik batang, lingkaran, garis, radar, dan dispersi data.
  - `FunctionPlot` / Canvas 2D: Plotting fungsi kalkulus dinamis, kurva trigonometri, dan sistem koordinat Kartesius.
- **Kasus Penggunaan**:
  - Eksplorasi Teorema Pythagoras dengan segitiga dinamis.
  - Simulasi pecahan nyata (konsep loyang pizza, balok cokelat).
  - Analisis statistik data survei dengan slider dinamis.

### B. Sains Alam (Fisika, Kimia, Biologi)
- **Pustaka**:
  - `Three.js` (`https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`): Model 3D anatomi organ tubuh, tata surya, dan struktur molekul yang dapat diputar 360°.
  - `Matter.js` (`https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js`): Simulasi fisika 2D (tumbukan, gravitasi, ayunan bandul, pegas Hooke).
  - HTML5 Canvas Optics: Pembiasan cermin/lensa cekung & cembung, hukum pemantulan, dan rangkaian listrik (Hukum Ohm).
- **Kasus Penggunaan**:
  - Simulasi gravitasi dan gerak parabola roket.
  - Titrasi asam-basa virtual dengan indikator warna pH.
  - Simulator persilangan genetik Mendel (*Punnett Square*).

### C. Bahasa & Fonetik (Indonesia, Inggris, Arab, Mandarin, Jepang, Korea, IELTS)
- **Pustaka & Web API**:
  - `HanziWriter` (`https://cdn.jsdelivr.net/npm/hanzi-writer@3.5/dist/hanzi-writer.min.js`): Animasi dan kuis urutan goresan (*stroke order*) karakter Hanzi Mandarin & Kanji Jepang.
  - HTML5 Canvas Handwriting Engine: Latihan menulis huruf Arab (Hijaiyah), Hangul Korea, dan Alfabet dengan garis bantu, *touch smoothing*, dan tombol hapus/reset.
  - Web Speech API (`window.speechSynthesis`): Audio penutur asli untuk latihan *listening* multi-bahasa.
  - Web Speech API (`window.SpeechRecognition` / `webkitSpeechRecognition`): Merekam suara siswa untuk evaluasi ketepatan pelafalan (*speaking practice*).
- **Kasus Penggunaan**:
  - Kuis pengucapan kata bahasa Inggris / percakapan IELTS.
  - Latihan menulis kaligrafi Arab dengan panduan arah goresan.
  - Tebak nada dan goresan pinyin Mandarin.

### D. Informatika, Coding & Logika
- **Pustaka**:
  - `Pyodide` (WebAssembly): Eksekusi kode Python nyata langsung di browser siswa.
  - `sql.js` (WebAssembly SQLite): Latihan query basis data interaktif.
  - Algoritma Visualizer Canvas: Animasi penelusuran graf, sorting (Bubble, Quick, Merge), dan simulasi gerbang logika (AND, OR, NOT, XOR).

### E. Vokasi (SMK Teknik Otomotif, Akuntansi, Bisnis)
- **Pustaka**:
  - `Three.js`: Visualisasi 3D siklus mesin 4-tak (langkah hisap, kompresi, usaha, buang) dan komponen kelistrikan kendaraan.
  - Interactive Spreadsheet Engine: Jurnal umum, buku besar, neraca saldo dinamis untuk mata pelajaran Akuntansi.
  - Economic Curve Simulator: Kurva permintaan dan penawaran dengan slider pergeseran ekuilibrium pasar.

### F. Sosial, Humaniora & Studi Agama
- **Pustaka**:
  - `Leaflet.js` & GeoJSON: Peta interaktif lempeng tektonik, jalur rempah Nusantara, dan sebaran flora/fauna garis Wallace-Weber.
  - Interactive Timeline: Garis waktu sejarah dinamis dengan narasi multimedia.
  - Tajwid Parser & Colorizer: Pewarnaan hukum tajwid otomatis pada ayat Al-Qur'an.

---

## 3. Titian LMS Bridge API (`window.Titian`)

Setiap dokumen web interaktif yang dimuat secara otomatis disuntikkan objek global `window.Titian`. Pengembang modul atau generator AI dapat menggunakan API ini untuk berkomunikasi dua arah dengan platform Titian Asa:

```javascript
// 1. Mengirimkan nilai asesmen / skor latihan interaktif
window.Titian.submitScore(score, maxScore);
// Contoh: window.Titian.submitScore(85, 100);

// 2. Menandai bahwa siswa telah menyelesaikan seluruh simulasi/materi
window.Titian.complete({ topic: 'Pecahan', timeSpent: 120 });

// 3. Memicu selebrasi konfeti saat siswa berhasil
window.Titian.celebrate();

// 4. Mendengarkan perubahan tema (Light/Dark mode) secara dinamis
window.Titian.onThemeChange(function(theme) {
  console.log("Tema aktif:", theme); // 'light' atau 'dark'
});
```

---

## 4. Standar Tampilan & Responsivitas

1. **Dark Mode (Wajib)**:
   - Gunakan CSS Variables pada `:root` dan `html.dark, body.dark`.
   - Hindari warna statis bernilai keras (*hardcoded*) seperti `#ffffff` untuk background atau `#000000` untuk teks.
   ```css
   :root {
     --bg: #f8fafc;
     --card-bg: #ffffff;
     --text: #0f172a;
     --border: #e2e8f0;
     --primary: #2563eb;
   }
   html.dark, body.dark {
     --bg: #090d16;
     --card-bg: #131b2e;
     --text: #f8fafc;
     --border: #1e293b;
     --primary: #3b82f6;
   }
   ```
2. **Auto-Height & Pencegahan Infinite Loop**:
   - Iframe secara otomatis menetralkan `min-height: 100vh` dengan injeksi `min-height: 0 !important; height: auto !important;`.
   - Ukuran dihitung berdasarkan batas bawah elemen konten aktual (`rect.bottom + window.pageYOffset + paddingBottom`).
3. **Layar Penuh (Fullscreen)**:
   - Tombol Layar Penuh tersedia di pojok kanan atas kartu simulasi.
   - Kompatibel dengan tombol <kbd>Esc</kbd> keyboard dan kontrol sentuh mobile.

