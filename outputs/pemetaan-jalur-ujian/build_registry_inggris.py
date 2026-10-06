#!/usr/bin/env python3
"""Registry Bahasa Inggris v1 dalam struktur baru: Domain -> Mapel -> Strand -> Konsep -> Unit (kata kerja + objek).
Konsep = 22 butir pohon `english` (POHON_HIERARKI_DOMAIN_LAIN_V1 bagian 2). Unit = topik lama yang dinamai ulang.
Masukan : pemetaan_inggris_v1.csv, referensi_lama.csv | Keluaran: registry_inggris_v1.csv, aset_path_inggris_v1.csv, ../POHON_HIERARKI_INGGRIS_V1.md
USULAN untuk ditinjau penelaah Bahasa Inggris; nama unit dan pemetaan konsep belum disahkan."""
import csv, re, os, collections
from build_inggris import LEAF, TEMPLATE

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(D)

KONSEP_SLUG = {"LIS1": "explicit_information", "LIS2": "main_idea_inference_attitude", "LIS3": "evaluate_spoken_text",
 "REA1": "vocabulary_in_context", "REA2": "main_idea_supporting_detail", "REA3": "inference_argument", "REA4": "academic_functional_literary_texts",
 "SPK1": "sounds_stress_intonation", "SPK2": "transactional_interpersonal_interaction", "SPK3": "opinion_argument", "SPK4": "presentation_fluency",
 "WRT1": "sentence_paragraph_coherence", "WRT2": "descriptive_narrative_procedural_report", "WRT3": "argumentation_academic_response", "WRT4": "revision_rubric",
 "GRV1": "word_classes_tenses_modality", "GRV2": "phrases_clauses_complex_sentences", "GRV3": "general_academic_vocabulary_collocation", "GRV4": "word_formation_guessing",
 "PRN1": "phonemes_minimal_pairs", "PRN2": "hard_sounds_rhythm_intonation", "PRN3": "pronunciation_self_monitoring"}
STRAND_SHORT = {"english.receptive_listening": "receptive_listening", "english.receptive_reading": "receptive_reading", "english.productive_speaking": "productive_speaking",
 "english.productive_writing": "productive_writing", "english.grammar_vocabulary": "grammar_vocabulary", "english.pronunciation": "pronunciation"}

NAME = {  # judul lama -> nama unit (kata kerja + objek)
 "Listening for Gist": "Menangkap gagasan pokok teks lisan", "Listening for Specific Information": "Menemukan informasi spesifik dari teks lisan",
 "Conversations & Interviews": "Memahami percakapan dan wawancara", "Connected & Fast Speech": "Memahami ujaran cepat dan bersambung",
 "Understanding Different Accents": "Memahami berbagai aksen bahasa Inggris", "Note-Taking While Listening": "Mencatat informasi saat menyimak",
 "Listening to Lectures & Podcasts": "Memahami kuliah dan podcast",
 "Vocabulary in Context": "Menafsirkan kosakata dari konteks", "Main Ideas & Supporting Details": "Menentukan gagasan utama dan detail pendukung",
 "Reading for Detail": "Membaca untuk informasi terperinci", "Skimming & Scanning": "Menerapkan skimming dan scanning",
 "Understanding Text Structure": "Menganalisis struktur teks", "Speed Reading Techniques": "Membaca cepat secara efektif",
 "Inference & Implied Meaning": "Membuat inferensi dan menangkap makna tersirat", "Critical Reading & Evaluating Arguments": "Mengevaluasi argumen dalam bacaan",
 "Everyday Conversation": "Melakukan percakapan sehari-hari", "Handling Interviews": "Menjawab pertanyaan wawancara",
 "Expressing & Defending Opinions": "Menyampaikan dan mempertahankan opini", "Discussion & Debate": "Berpartisipasi dalam diskusi dan debat",
 "Presentation Skills": "Mempresentasikan topik secara terstruktur", "Narrating Events & Storytelling": "Menarasikan peristiwa dan bercerita",
 "Describing People, Places & Things": "Mendeskripsikan orang, tempat, dan benda", "Fluency & Pronunciation Practice": "Melatih kelancaran dan pelafalan",
 "At School & Campus": "Berkomunikasi di sekolah dan kampus", "At the Workplace": "Berkomunikasi di tempat kerja", "Health & Hospital": "Berkomunikasi di layanan kesehatan",
 "Shopping & Restaurant": "Berkomunikasi saat berbelanja dan makan di restoran", "Telephone & Online Communication": "Berkomunikasi melalui telepon dan daring",
 "Travel, Airport & Hotel": "Berkomunikasi saat bepergian, di bandara, dan di hotel",
 "Agreeing & Disagreeing": "Menyatakan setuju dan tidak setuju", "Apologizing & Complaining": "Meminta maaf dan menyampaikan keluhan",
 "Asking for & Giving Information": "Meminta dan memberi informasi", "Expressing Opinions": "Menyatakan pendapat", "Greetings & Small Talk": "Menyapa dan berbasa-basi",
 "Likes, Dislikes & Preferences": "Menyatakan kesukaan, ketidaksukaan, dan preferensi", "Making Requests & Offers": "Membuat permintaan dan tawaran",
 "Suggestions & Advice": "Memberi saran dan nasihat",
 "Sentence to Paragraph": "Menyusun kalimat menjadi paragraf", "Paragraph Structure & Cohesion": "Menyusun paragraf yang padu", "Descriptive Writing": "Menulis teks deskriptif",
 "Narrative Writing": "Menulis teks naratif", "Expository Writing": "Menulis teks ekspositori", "Argumentative & Persuasive Writing": "Menulis teks argumentatif dan persuasif",
 "Summarizing & Paraphrasing": "Meringkas dan memparafrasa teks", "Editing & Proofreading": "Menyunting dan memeriksa tulisan",
 "Phonetic Symbols (IPA)": "Membaca simbol fonetik (IPA)", "Intonation Patterns": "Menerapkan pola intonasi", "Sentence Stress & Rhythm": "Menerapkan tekanan dan ritme kalimat",
 "Word Stress": "Menerapkan tekanan kata", "Consonant Clusters & Digraphs": "Melafalkan gugus konsonan dan digraf", "Consonant Sounds": "Membedakan bunyi konsonan",
 "The Alphabet & Letter Sounds": "Mengenali abjad dan bunyi huruf", "Vowel Sounds (Short & Long)": "Membedakan bunyi vokal pendek dan panjang",
}
GENRE_READ_WRITE = {"Announcement, Invitation & Notice", "News Item", "Report Text", "Review Text", "Explanation Text", "Procedure Text"}  # juga melatih membaca teks fungsional/akademik (REA4)
PATTERN = {"GRV1": "Menggunakan {t}", "GRV2": "Menggunakan {t}", "GRV3": "Memperluas kosakata: {t}", "GRV4": "Membentuk kata dengan {t}",
           "WRT1": "Menggunakan aturan {t}", "WRT2": "Membaca dan menulis {t}", "WRT3": "Membaca dan menulis {t}", "PRN1": "Melafalkan {t}", "PRN2": "Melafalkan {t}"}
CAMB = {"YLE Starters (Pre-A1)": "cambridge:yle-starters", "YLE Movers (A1)": "cambridge:yle-movers", "YLE Flyers (A2)": "cambridge:yle-flyers", "A2 Key (KET)": "cambridge:ket-a2",
        "B1 Preliminary (PET)": "cambridge:pet-b1", "B2 First (FCE)": "cambridge:fce-b2", "C1 Advanced (CAE)": "cambridge:cae-c1", "C2 Proficiency (CPE)": "cambridge:cpe-c2"}
EXAM_SECTION = {"Persiapan IELTS": "exam:ielts", "Persiapan TOEFL iBT": "exam:toefl-ibt", "Persiapan TOEFL ITP": "exam:toefl-itp", "Persiapan TOEIC": "exam:toeic",
                "Persiapan PTE Academic": "exam:pte-academic", "Persiapan Duolingo English Test": "exam:duolingo"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def unit_name(code, title):
    return NAME.get(title) or PATTERN.get(code, "Menguasai {t}").format(t=title)


def main():
    rows = list(csv.DictReader(open(f"{D}/pemetaan_inggris_v1.csv")))
    refs = collections.defaultdict(set)
    for r in csv.DictReader(open(f"{D}/referensi_lama.csv")):
        tid = r["topik_id"]
        if r["jalur"] == "Fokus Ujian TKA" and r["seksi"] == "TKA Bahasa Inggris": refs[tid] |= {"exam:tka", "exam-component:bahasa-inggris"}
        elif r["jalur"].startswith("Persiapan Ujian Masuk") and r["subseksi"] == "Literasi Bahasa Inggris": refs[tid] |= {"exam:utbk-snbt", "exam-component:literasi-bahasa-inggris"}
        elif r["jalur"] == "Kurikulum Cambridge" and r["subseksi"] in CAMB: refs[tid].add(CAMB[r["subseksi"]])
        elif r["jalur"] == "Belajar Bahasa Inggris" and r["seksi"] in EXAM_SECTION: refs[tid].add(EXAM_SECTION[r["seksi"]])

    units, seen = [], collections.Counter()
    for r in rows:
        if not r["jenis"].startswith("UNIT"): continue
        code = r["leaf_kode"]; strand = STRAND_SHORT[r["strand"]]; konsep = KONSEP_SLUG[code]
        mid = f"english.{strand}.{konsep}.{slug(r['topik'])}.v1"; seen[mid] += 1
        if seen[mid] > 1: mid = mid.replace(".v1", f"-{r['cefr'].lower()}.v1")
        sec = "REA4" if r["topik"] in GENRE_READ_WRITE else ""
        fw = ["framework:kurikulum-merdeka"] if r["kluster"].startswith("Teks ") else []
        labels = fw + [f"domain:english", "subject:bahasa_inggris", f"strand:{strand}", f"concept:{konsep}", f"cefr:{r['cefr']}"] + sorted(refs[r["topik_id"]])
        units.append({"module_id": mid, "strand": strand, "konsep_kode": code, "konsep": LEAF[code][1], "konsep_sekunder": (LEAF[sec][1] if sec else ""),
                      "unit": unit_name(code, r["topik"]), "judul_lama": r["topik"], "cefr": r["cefr"], "template": r["template"], "tier": r["tier"],
                      "TKA": r["TKA"], "PTN": r["PTN"], "CAMB": r["CAMB"], "label": ";".join(labels),
                      "sumber_topik_id": r["topik_id"], "bab_lama": r["bab"], "bab_bermateri": r["bab_materi"], "soal_ada": r["soal"],
                      "kesiapan": r["kesiapan_pakai_ulang"], "bank_tahap1": "SELEKSI-DARI-SOAL-LAMA" if int(r["soal"]) >= 20 else "GENERATE"})
    order = {k: i for i, k in enumerate(LEAF)}
    units.sort(key=lambda u: (order[u["konsep_kode"]], u["cefr"], u["unit"]))
    with open(f"{D}/registry_inggris_v1.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(units[0].keys())); w.writeheader(); w.writerows(units)
    assert len({u["module_id"] for u in units}) == len(units)

    # aset milik path (strategi/blueprint ujian) dan rujukan ke unit keterampilan
    assets = []
    EXAM_OF = {"IELTS Academic": "ielts", "IELTS General Training": "ielts", "PTE Academic": "pte-academic", "TOEFL ITP": "toefl-itp", "TOEFL iBT": "toefl-ibt",
               "TOEIC": "toeic", "Duolingo English Test & Tes Lain": "duolingo", "Persiapan Tes Internasional": "umum"}
    SKILL = [("listening", "receptive_listening"), ("reading", "receptive_reading"), ("speaking", "productive_speaking"), ("writing", "productive_writing"),
             ("structure", "grammar_vocabulary"), ("grammar", "grammar_vocabulary"), ("kosakata", "grammar_vocabulary"), ("vocabulary", "grammar_vocabulary")]
    for r in rows:
        if not r["jenis"].startswith("STRATEGI"): continue
        ex = EXAM_OF.get(r["kluster"], "umum"); t = r["topik"]
        kind = "assessment" if re.search(r"simulasi|evaluasi skor", t.lower()) else "strategy"
        skill = next((s for k, s in SKILL if k in t.lower()), "")
        assets.append({"asset_id": f"path.english_exams.{ex}.{slug(t)}", "sumber_topik_id": r["topik_id"], "ujian": ex, "jenis_aset": kind, "judul_lama": t, "merujuk_strand": skill,
                       "TKA": r["TKA"], "PTN": r["PTN"], "bab_lama": r["bab"], "bab_bermateri": r["bab_materi"], "soal_ada": r["soal"],
                       "kesiapan": "ADA-MATERI" if int(r["bab_materi"]) > 0 else "KERANGKA-SAJA"})
    with open(f"{D}/aset_path_inggris_v1.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(assets[0].keys())); w.writeheader(); w.writerows(assets)

    # pohon teks
    L = ["# Pohon Hierarki Bahasa Inggris v1 (usulan unit)", "",
         "Status: **usulan**, dihasilkan dari registry topik lama oleh `pemetaan-jalur-ujian/build_registry_inggris.py`. Nama unit, pemetaan ke konsep, dan label CEFR belum ditinjau penelaah Bahasa Inggris.",
         "Mengikuti `POHON_HIERARKI_DOMAIN_LAIN_V1.md` bagian 2 (22 butir konsep) dan `STANDAR_KURIKULUM_TITIAN_ASA.md`. Butir pohon itu diperlakukan sebagai **konsep**, dan unit di bawahnya berasal dari topik lama.",
         "", "```text", "english", "└─ bahasa_inggris"]
    by = collections.defaultdict(list)
    for u in units: by[u["konsep_kode"]].append(u)
    strands = collections.OrderedDict()
    for k in LEAF: strands.setdefault(LEAF[k][0], []).append(k)
    ss = list(strands.items())
    for si, (st, codes) in enumerate(ss):
        last_s = si == len(ss) - 1; pre = "   "
        L.append(f"{pre}{'└─' if last_s else '├─'} {STRAND_SHORT[st]}")
        cp = pre + ("   " if last_s else "│  ")
        for ci, code in enumerate(codes):
            last_c = ci == len(codes) - 1
            n = len(by[code]); L.append(f"{cp}{'└─' if last_c else '├─'} english.{KONSEP_SLUG[code]} — {LEAF[code][1]} ({n} unit)")
            up = cp + ("   " if last_c else "│  ")
            us = by[code]
            sek = [u for u in units if u["konsep_sekunder"] == LEAF[code][1]]
            if not us and not sek: L.append(f"{up}└─ (belum ada topik lama; unit baru diperlukan)")
            for ui, u in enumerate(sek):
                L.append(f"{up}{'└─' if ui == len(sek) - 1 else '├─'} [{u['cefr']}] {u['unit']}  (unit sekunder: konsep utamanya {u['konsep_kode']})")
            for ui, u in enumerate(us):
                L.append(f"{up}{'└─' if ui == len(us) - 1 else '├─'} [{u['cefr']}] {u['unit']}")
    L += ["```", "", "Kode CEFR di depan unit adalah label (`cefr:`), bukan cabang pohon. Unit yang sama dirujuk oleh path CEFR, Cambridge, TKA, UTBK, dan persiapan tes; path tidak memiliki salinan.", ""]
    open(f"{OUT}/POHON_HIERARKI_INGGRIS_V1.md", "w").write("\n".join(L))

    s = collections.Counter(u["kesiapan"] for u in units)
    print("unit", len(units), dict(s), "| aset path", len(assets), dict(collections.Counter(a["jenis_aset"] for a in assets)))
    print("konsep tanpa unit:", [LEAF[k][1] for k in LEAF if not by[k]])
    print("label ujian per unit:", collections.Counter(l for u in units for l in u["label"].split(";") if l.startswith(("exam:", "cambridge:"))).most_common())


if __name__ == "__main__":
    main()
