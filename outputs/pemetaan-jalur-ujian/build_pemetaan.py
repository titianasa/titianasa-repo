#!/usr/bin/env python3
"""Lapis klasifikasi deterministik: topik lama -> rumah kanonik + kecocokan seksi jalur.
Masukan : topik_lama_unik.csv, referensi_lama.csv (hasil ekspor DB)
Keluaran: pemetaan_topik_v1.csv, pemetaan_referensi_v1.csv, ringkasan.json
Tidak memakai LLM. Semua keputusan di sini bisa ditinjau dan diubah lewat tabel di bawah."""
import csv, json, collections, os, re

D = os.path.dirname(os.path.abspath(__file__))

# --- 1. mapel lama -> rumah kanonik (PETA_KANONIK_KURIKULUM_TITIAN_ASA_V1 bagian 3) ---
SUBJECT_HOME = {
    "Matematika": "mathematics.matematika", "English": "english",
    "Bahasa Indonesia": "indonesian", "Sastra Indonesia": "indonesian.literature",
    "Fisika": "science.physics", "Kimia": "science.chemistry", "Biologi": "science.biology",
    "Informatika": "computing", "Geografi": "social_sciences.geography",
    "Sejarah": "social_sciences.history", "Ekonomi": "social_sciences.economics",
    "Sosiologi": "social_sciences.sociology", "Antropologi": "social_sciences.anthropology",
    "Pendidikan Kewarganegaraan": "social_sciences.civic_education",
    "Penalaran & Logika": "reasoning", "Filsafat": "reasoning.philosophy",
    "Akuntansi": "career_vocational.accounting", "Bahasa Arab": "other_languages.arabic",
    "PJOK": "arts_health_life.physical_education", "Seni Budaya": "arts_health_life.arts",
    "Prakarya & Kewirausahaan": "arts_health_life.craft_entrepreneurship",
    "Pendidikan Agama Islam": "religious_studies.islamic_madrasah",
    "Pendidikan Agama Khonghucu": "religious_studies.confucian",
    "Pendidikan Agama Hindu": "religious_studies.hindu",
    "Pendidikan Agama Katolik": "religious_studies.catholic",
    "Pendidikan Agama Kristen": "religious_studies.christian",
    "Pendidikan Agama Buddha": "religious_studies.buddhist",
    "Ilmu Tafsir": "religious_studies.islamic_advanced", "Ilmu Hadis": "religious_studies.islamic_advanced",
    "Akhlak Tasawuf": "religious_studies.islamic_advanced", "Ushul Fikih": "religious_studies.islamic_advanced",
    "Ilmu Kalam": "religious_studies.islamic_advanced",
}
# bundel sekolah & "mapel" yang sebenarnya path: tidak punya rumah sendiri -> harus di-rumahkan ulang per bab
BUNDLE = {"IPA": "REHOME:science.*", "IPAS": "REHOME:science.*+social_sciences.*", "IPS": "REHOME:social_sciences.*"}
PATH_LIKE = {"Wawasan ASN & Kepegawaian": "REHOME:path.career.public_service (rujuk civic_education, career_readiness, reasoning)",
             "Wawasan BUMN & Dunia Kerja": "REHOME:path.career.bumn (rujuk career_readiness, business_management, reasoning)"}

# --- 2. Matematika: kluster lama -> konsep kanonik (POHON_HIERARKI_MATEMATIKA_V1) ---
MATH = {
 "Aljabar Dasar": ("algebra.patterns_expressions", "MATH-PROCEDURE"),
 "Aljabar Linear": ("algebra.linear_algebra", "MATH-PROOF"),
 "Analisis Real": ("analysis.real", "MATH-PROOF"),
 "Barisan & Deret": ("algebra.sequences_series", "MATH-PROCEDURE"),
 "Bilangan & Operasi Dasar": ("number.whole_operations", "MATH-PROCEDURE"),
 "Bilangan Berpangkat & Bentuk Akar": ("number.real_exponents_roots", "MATH-PROCEDURE"),
 "Bilangan Kompleks": ("number.complex", "MATH-PROCEDURE"),
 "Dimensi Tiga": ("geometry.solid_shapes", "MATH-VISUAL"),
 "Eksponen & Logaritma": ("algebra.exponential_logarithmic", "MATH-PROCEDURE"),
 "Fungsi & Grafik": ("algebra.relations_functions", "MATH-INTERPRET"),
 "Geometri Analitik": ("geometry.analytic_conics", "MATH-VISUAL"),
 "Geometri Bidang": ("geometry.plane_shapes", "MATH-VISUAL"),
 "Geometri Dasar": ("geometry.plane_shapes", "MATH-VISUAL"),
 "Geometri Ruang": ("geometry.solid_shapes", "MATH-VISUAL"),
 "Integral (Kalkulus Integral)": ("calculus.integration", "MATH-PROCEDURE"),
 "Irisan Kerucut": ("geometry.analytic_conics", "MATH-VISUAL"),
 "Kalkulus Lanjut": ("calculus.multivariable", "MATH-PROCEDURE"),
 "Limit & Kekontinuan": ("calculus.limits_continuity", "MATH-INTERPRET"),
 "Logika Matematika": ("discrete.logic_sets_proof", "MATH-CONCEPT"),
 "Matematika Diskrit": ("discrete.combinatorics_graphs", "MATH-PROCEDURE"),
 "Matematika Terapan & Komputasi": ("modeling.numerical_computation", "MATH-MODEL"),
 "Matriks & Transformasi Geometri": ("algebra.matrices_vectors", "MATH-PROCEDURE"),
 "Mekanika Matematis": ("modeling.mechanics", "MATH-MODEL"),
 "Numerasi & Penalaran Kuantitatif": ("modeling.quantitative_reasoning", "MATH-MODEL"),
 "Pecahan, Desimal & Persen": ("number.fractions", "MATH-PROCEDURE"),
 "Pengenalan Data": ("data.representation", "MATH-INTERPRET"),
 "Pengukuran": ("geometry.measurement", "MATH-CONCEPT"),
 "Perbandingan & Aritmetika Sosial": ("number.decimal_percent_ratio", "MATH-MODEL"),
 "Persamaan & Fungsi Kuadrat": ("algebra.quadratic", "MATH-PROCEDURE"),
 "Persamaan & Pertidaksamaan Linear": ("algebra.linear_equations", "MATH-PROCEDURE"),
 "Persamaan Diferensial": ("analysis.differential_equations", "MATH-PROCEDURE"),
 "Probabilitas & Statistika Inferensial": ("statistics.inference", "MATH-INTERPRET"),
 "Sistem Persamaan & Program Linear": ("algebra.linear_equations", "MATH-MODEL"),
 "Statistika & Peluang Dasar": ("data.descriptive_statistics", "MATH-INTERPRET"),
 "Statistika & Peluang Lanjut": ("probability.random_variables", "MATH-INTERPRET"),
 "Teori Bilangan": ("number_theory.elementary", "MATH-PROOF"),
 "Trigonometri": ("geometry.trigonometry", "MATH-PROCEDURE"),
 "Turunan (Kalkulus Diferensial)": ("calculus.differentiation", "MATH-PROCEDURE"),
 "Vektor": ("algebra.matrices_vectors", "MATH-VISUAL"),
}

# Kluster lama yang mencakup >1 konsep kanonik: kata kunci judul topik -> konsep (urutan penting)
MATH_OVERRIDE = {
 "Pengenalan Data": [(r"rata|median|modus|kuartil|jangkauan|simpangan|ukuran", "data.descriptive_statistics")],
 "Statistika & Peluang Dasar": [(r"peluang|kejadian|ruang sampel|frekuensi harapan|pencacahan|permutasi|kombinasi|kaidah", "probability.foundations_counting")],
 "Statistika & Peluang Lanjut": [(r"uji|hipotesis|interval|estimasi|regresi|korelasi|inferensi|sampel|populasi", "statistics.inference"),
                                  (r"permutasi|kombinasi|pencacahan|aturan", "probability.foundations_counting")],
 "Probabilitas & Statistika Inferensial": [(r"uji|hipotesis|interval|estimasi|regresi|korelasi|inferensi|sampling|populasi", "statistics.inference")],
 "Pecahan, Desimal & Persen": [(r"persen|desimal|rasio|perbandingan", "number.decimal_percent_ratio")],
 "Bilangan & Operasi Dasar": [(r"bulat|negatif|garis bilangan", "number.integers"), (r"nilai tempat|cacah|pembulatan", "number.whole_place_value"),
                               (r"faktor|kelipatan|fpb|kpk|prima|habis dibagi", "number.factors_multiples")],
 "Matriks & Transformasi Geometri": [(r"transformasi|refleksi|rotasi|translasi|dilatasi|pencerminan|pergeseran", "geometry.transformations_coordinates")],
 "Sistem Persamaan & Program Linear": [(r"program linear|optimasi|optimisasi|nilai maksimum|nilai minimum", "modeling.optimization_operations")],
 "Geometri Dasar": [(r"luas|keliling|volume|satuan|ukuran", "geometry.measurement")],
 "Geometri Analitik": [(r"lingkaran|parabola|elips|hiperbola|irisan", "geometry.analytic_conics"), (r"koordinat|jarak|titik tengah|kartesius", "geometry.transformations_coordinates")],
 "Numerasi & Penalaran Kuantitatif": [(r"data|grafik|tabel|diagram", "data.representation")],
}

# --- 3. Inggris: kluster lama -> strand kanonik / aset milik jalur / ekstensi ---
G = "english.grammar_vocabulary"
ENG = {}
for k in ["Advanced Grammar & Style", "Clauses", "Comparison & Degrees", "Conditionals & Wishes", "Gerunds & Infinitives",
          "Modal Verbs", "Parts of Speech", "Reported Speech", "Sentence Structure", "Tenses", "Voice", "Building Simple Sentences",
          "Punctuation & Mechanics", "Common Errors for Indonesian Learners", "Core Vocabulary", "Vocabulary Building",
          "Word Formation", "Idiomatic English", "Time, Number & Measurement Expressions"]:
    ENG[k] = (G, "CANONICAL")
ENG.update({"Alphabet & Pronunciation": ("english.pronunciation", "CANONICAL"),
            "Listening": ("english.receptive_listening", "CANONICAL"), "Reading": ("english.receptive_reading", "CANONICAL"),
            "Speaking": ("english.productive_speaking", "CANONICAL"), "Conversation in Context": ("english.productive_speaking", "CANONICAL"),
            "Functional Language": ("english.productive_speaking", "CANONICAL"), "Writing": ("english.productive_writing", "CANONICAL"),
            "Teks Argumentatif & Evaluatif": ("english.productive_writing", "CANONICAL"),
            "Teks Faktual & Prosedural": ("english.productive_writing", "CANONICAL"),
            "Teks Naratif & Personal": ("english.productive_writing", "CANONICAL")})
for k in ["IELTS Academic", "IELTS General Training", "PTE Academic", "TOEFL ITP", "TOEFL iBT", "TOEIC",
          "Duolingo English Test & Tes Lain", "Persiapan Tes Internasional"]:
    ENG[k] = ("path.english_exams", "PATH-OWNED (strategi/format tes)")
for k in ["English for Academic Purposes", "English for Business & Professional", "English for Specific Purposes"]:
    ENG[k] = ("english.esp (usulan strand baru)", "EXTENSION")
for k in ["Fonetik & Fonologi", "Analisis Wacana & Linguistik Historis", "Kajian Penerjemahan & Interpretasi", "Linguistik Korpus & Komputasional",
          "Linguistik Terapan & SLA Lanjut", "Metodologi Pengajaran (TEFL/TESOL)", "Metodologi Riset Linguistik Terapan",
          "Morfologi", "Penilaian & Evaluasi Bahasa", "Psikolinguistik & Pemerolehan Bahasa", "Sastra & Budaya",
          "Semantik & Pragmatik", "Sintaksis", "Sosiolinguistik", "Teori Sastra & Kritik", "Translation Skills (Indonesia ↔ Inggris)"]:
    ENG[k] = ("english.linguistics_specialist (P2, di luar pohon v1)", "EXTENSION")

# --- 3b. Penalaran & Logika lama: isinya campuran; tiap kluster dirumahkan ke rumah kanonik aslinya (Keputusan D1) ---
REASONING = {
 "Aritmetika Dasar & Cepat": ("mathematics.matematika", "", "MERGE-KE-MATEMATIKA"),
 "Deret & Pola Bilangan": ("mathematics.matematika", "algebra.sequences_series", "MERGE-KE-MATEMATIKA"),
 "Pengetahuan Kuantitatif": ("mathematics.matematika", "", "MERGE-KE-MATEMATIKA"),
 "Soal Cerita & Pemodelan": ("mathematics.matematika", "modeling.quantitative_reasoning", "MERGE-KE-MATEMATIKA"),
 "Logika Matematika Terapan": ("mathematics.matematika", "discrete.logic_sets_proof", "MERGE-KE-MATEMATIKA"),
 "Logika Verbal": ("reasoning", "reasoning.logic_argumentation", "CANONICAL"),
 "Pemecahan Masalah": ("reasoning", "reasoning.problem_solving", "CANONICAL"),
 "Penalaran Analitis": ("reasoning", "reasoning.problem_solving", "CANONICAL"),
 "Kemampuan Verbal Dasar": ("indonesian", "", "REHOME-KE-INDONESIA"),
 "Pemahaman Bacaan": ("indonesian", "", "REHOME-KE-INDONESIA"),
 "Strategi Menghadapi Tes": ("path.exam_strategy", "", "PATH-OWNED (strategi/format tes)"),
}

# --- 4. kecocokan seksi jalur: mapel yang WAJAR ada di seksi itu ---
S = lambda *a: set(a)
FIT = {
 ("Fokus Ujian TKA", "TKA Literasi Membaca"): S("Bahasa Indonesia", "Sastra Indonesia"),
 ("Fokus Ujian TKA", "TKA Numerasi"): S("Matematika", "Penalaran & Logika"),
 ("Fokus Ujian TKA", "TKA Bahasa Inggris"): S("English"),
 ("Fokus Ujian TKA", "TKA Pilihan — Saintek"): S("Fisika", "Kimia", "Biologi", "Informatika", "Matematika"),
 ("Fokus Ujian TKA", "TKA Pilihan — Soshum"): S("Sejarah", "Geografi", "Ekonomi", "Sosiologi", "Antropologi"),
 ("Fokus Ujian TKA", "AKM Literasi"): S("Bahasa Indonesia", "Penalaran & Logika", "Sastra Indonesia"),
 ("Fokus Ujian TKA", "AKM Numerasi"): S("Matematika", "Penalaran & Logika"),
 ("Persiapan Ujian Masuk Perguruan Tinggi", "Materi Mata Pelajaran — Saintek"): S("Fisika", "Kimia", "Biologi", "Informatika", "Matematika"),
 ("Persiapan Ujian Masuk Perguruan Tinggi", "Materi Mata Pelajaran — Soshum"): S("Sejarah", "Geografi", "Ekonomi", "Sosiologi", "Antropologi"),
 ("Persiapan Ujian Masuk Perguruan Tinggi", "UTBK-SNBT — Tes Potensi Skolastik"): S("Penalaran & Logika", "Bahasa Indonesia", "Matematika", "Filsafat"),
 ("Persiapan Ujian Masuk Perguruan Tinggi", "UTBK-SNBT — Literasi & Penalaran Matematika"): S("Matematika", "Bahasa Indonesia", "English", "Sastra Indonesia", "Penalaran & Logika"),
 ("Persiapan Ujian Masuk Perguruan Tinggi", "UM-PTKIN (PTKIN & Keislaman)"): S("Pendidikan Agama Islam", "Ilmu Tafsir", "Ilmu Hadis", "Akhlak Tasawuf", "Ushul Fikih", "Ilmu Kalam", "Bahasa Arab"),
 ("Fokus Ujian BUMN", "Tes Kemampuan Dasar (TKD)"): S("Penalaran & Logika", "Bahasa Indonesia", "Matematika", "Wawasan BUMN & Dunia Kerja"),
 ("Fokus Ujian BUMN", "Tes Core Values AKHLAK"): S("Wawasan BUMN & Dunia Kerja", "Wawasan ASN & Kepegawaian", "Pendidikan Kewarganegaraan"),
 ("Fokus Ujian BUMN", "Learning Agility"): S("Penalaran & Logika", "Wawasan BUMN & Dunia Kerja"),
 ("Fokus Ujian BUMN", "Tes Bahasa Inggris"): S("English"),
 ("Fokus Ujian CPNS", "SKD — Tes Wawasan Kebangsaan (TWK)"): S("Wawasan ASN & Kepegawaian", "Pendidikan Kewarganegaraan", "Sejarah"),
 ("Fokus Ujian CPNS", "SKD — Tes Intelegensia Umum (TIU)"): S("Penalaran & Logika", "Bahasa Indonesia", "Matematika"),
 ("Fokus Ujian CPNS", "SKD — Tes Karakteristik Pribadi (TKP)"): S("Wawasan ASN & Kepegawaian", "Penalaran & Logika"),
 ("Fokus Ujian CPNS", "SKB — Seleksi Kompetensi Bidang"): S("Wawasan ASN & Kepegawaian"),
 ("Kurikulum Cambridge", "Cambridge English — Young Learners (YLE)"): S("English"),
 ("Kurikulum Cambridge", "Cambridge English — Main Suite"): S("English"),
 ("Kurikulum Cambridge", "Cambridge Advanced — AS & A Level"): S("Matematika", "Fisika", "Kimia", "Biologi", "Informatika", "Ekonomi"),
 ("Kurikulum Cambridge", "Cambridge Upper Secondary — IGCSE"): S("Matematika", "Fisika", "Kimia", "Biologi", "Informatika", "Ekonomi", "Geografi", "Sejarah", "English", "Bahasa Arab", "Akuntansi"),
 ("Kurikulum Cambridge", "Cambridge Lower Secondary (Stage 7-9)"): S("Matematika", "English", "IPA", "Informatika", "Sejarah", "Geografi"),
 ("Kurikulum Cambridge", "Cambridge Primary (Stage 1-6)"): S("Matematika", "English", "IPAS", "IPA", "Informatika"),
}
# seksi yang memang bukan rangkuman mapel: dump ("lihat semua") atau spesialis
DUMP = {("Persiapan Ujian Masuk Perguruan Tinggi", "Ujian Mandiri PTN"): "DUMP: 925 topik = gabungan seksi lain; jadikan aturan/aset ujian per PTN, bukan daftar topik",
        ("Persiapan Ujian Masuk Perguruan Tinggi", "Olimpiade Sains Nasional (OSN)"): "ENRICHMENT: referensi ke unit F3-F4 tiap mapel, bukan daftar topik sendiri"}
ENGLISH_PATH = "Belajar Bahasa Inggris"
CEFR_SECTION = {"A1 - Basic": "A1", "A2 - Elementary": "A2", "B1 - Intermediate": "B1", "B2 - Upper Intermediate": "B2", "C1 - Advanced": "C1", "C2 - Proficiency": "C2"}
# template generik STANDAR_BLUEPRINT bagian 4 (tebakan awal per strand, bukan per leaf)
ENG_TEMPLATE = {"english.receptive_listening": "INTERPRET", "english.receptive_reading": "INTERPRET", "english.productive_speaking": "COMMUNICATE",
                "english.productive_writing": "COMMUNICATE", "english.pronunciation": "PRACTICE", "english.grammar_vocabulary": "CONCEPT",
                "path.english_exams": "EVALUATE"}


def home_of(subject, cluster):
    if subject in SUBJECT_HOME: return SUBJECT_HOME[subject]
    if subject in BUNDLE: return BUNDLE[subject]
    if subject in PATH_LIKE: return PATH_LIKE[subject]
    return "UNMAPPED"


def main():
    topik = list(csv.DictReader(open(f"{D}/topik_lama_unik.csv")))
    refs = list(csv.DictReader(open(f"{D}/referensi_lama.csv")))
    by_topic = collections.defaultdict(list)
    for r in refs: by_topic[r["topik_id"]].append(r)

    out_t, stats = [], collections.Counter()
    for t in topik:
        s, c = t["subject"], t["cluster"]
        home, concept, tmpl, kind = home_of(s, c), "", "", "CANONICAL"
        if s == "Matematika":
            concept, tmpl = MATH.get(c, ("", ""))
            if not concept: kind = "MATH-CLUSTER-BARU"
            for pat, alt in MATH_OVERRIDE.get(c, []):
                if re.search(pat, t["topic"].lower()):
                    if alt != concept: stats["override_math"] += 1
                    concept = alt; break
        elif s == "English":
            concept, kind = ENG.get(c, ("", "ENG-CLUSTER-BARU"))
            tmpl = ENG_TEMPLATE.get(concept, "")
        elif s == "Penalaran & Logika" and c in REASONING:
            home, concept, kind = REASONING[c]
        elif home.startswith("REHOME"): kind = "REHOME"
        else: kind = "HOME-ONLY (konsep/leaf belum dipetakan)"
        cefr = sorted({CEFR_SECTION[r["seksi"]] for r in by_topic[t["id"]] if r["jalur"] == ENGLISH_PATH and r["seksi"] in CEFR_SECTION}) if s == "English" else []
        fits = []
        for r in by_topic[t["id"]]:
            key = (r["jalur"], r["seksi"])
            if r["jalur"] == ENGLISH_PATH: fits.append("ok"); continue
            if key in DUMP: fits.append("dump/enrichment"); continue
            allowed = FIT.get(key)
            fits.append("ok" if (allowed is None or s in allowed) else "OFF-SCOPE")
        n_off = fits.count("OFF-SCOPE")
        paths = sorted({r["jalur"] for r in by_topic[t["id"]]})
        stats["kind:" + kind] += 1
        out_t.append({**t, "rumah_kanonik": home, "konsep_kanonik": concept, "template_blueprint": tmpl, "cefr": "|".join(cefr), "jenis_pemetaan": kind,
                      "jumlah_jalur": len(paths), "referensi_off_scope": n_off})
    with open(f"{D}/pemetaan_topik_v1.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_t[0].keys())); w.writeheader(); w.writerows(out_t)

    tmap = {t["id"]: t for t in out_t}
    out_r, off = [], collections.Counter()
    for r in refs:
        t = tmap[r["topik_id"]]; key = (r["jalur"], r["seksi"]); s = t["subject"]
        if r["jalur"] == ENGLISH_PATH: fit = "ok"
        elif key in DUMP: fit = "dump/enrichment"
        else:
            allowed = FIT.get(key); fit = "ok" if (allowed is None or s in allowed) else "OFF-SCOPE"
        if fit == "OFF-SCOPE": off[(r["jalur"], r["seksi"], s)] += 1
        out_r.append({**r, "rumah_kanonik": t["rumah_kanonik"], "konsep_kanonik": t["konsep_kanonik"], "kecocokan_seksi": fit})
    with open(f"{D}/pemetaan_referensi_v1.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_r[0].keys())); w.writeheader(); w.writerows(out_r)

    per_path = collections.defaultdict(collections.Counter)
    for r in out_r: per_path[r["jalur"]][r["kecocokan_seksi"]] += 1
    summary = {"topik_unik": len(out_t), "referensi": len(out_r),
               "jenis_pemetaan": {k[5:]: v for k, v in stats.items() if k.startswith("kind:")},
               "topik_math_dikoreksi_per_judul": stats["override_math"],
               "kecocokan_per_jalur": {k: dict(v) for k, v in per_path.items()},
               "off_scope_teratas": [{"jalur": k[0], "seksi": k[1], "mapel": k[2], "n": v} for k, v in off.most_common(25)],
               "unmapped_subject": sorted({t["subject"] for t in out_t if t["rumah_kanonik"] == "UNMAPPED"})}
    json.dump(summary, open(f"{D}/ringkasan.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
