#!/usr/bin/env python3
"""Pemetaan Bahasa Inggris P0: topik lama -> leaf pohon `english` (POHON_HIERARKI_DOMAIN_LAIN_V1 bagian 2) + CEFR + kesiapan pakai ulang.
Aturan berbasis kluster dan judul topik (judul lama berbahasa Inggris, leaf berbahasa Indonesia, jadi tidak memakai TF-IDF).
Masukan : lingkup_p0_v1.csv, pemetaan_topik_v1.csv, statistik_bank_inggris.csv (ekspor DB)
Keluaran: pemetaan_inggris_v1.csv, ringkasan_inggris.json. HASILNYA USULAN untuk ditinjau."""
import csv, json, os, collections

D = os.path.dirname(os.path.abspath(__file__))

# leaf pohon english (22 leaf; pohon v1 masih setingkat konsep)
LEAF = {
 "LIS1": ("english.receptive_listening", "Mengenali bunyi, kata, dan informasi eksplisit"),
 "LIS2": ("english.receptive_listening", "Memahami ide utama, detail, inferensi, dan sikap pembicara"),
 "LIS3": ("english.receptive_listening", "Mengevaluasi tujuan serta keandalan teks lisan"),
 "REA1": ("english.receptive_reading", "Memahami kosakata dalam konteks"),
 "REA2": ("english.receptive_reading", "Menemukan gagasan utama dan detail pendukung"),
 "REA3": ("english.receptive_reading", "Membuat inferensi dan menilai argumen"),
 "REA4": ("english.receptive_reading", "Membaca teks akademik, fungsional, dan sastra"),
 "SPK1": ("english.productive_speaking", "Mengucapkan bunyi, tekanan kata, dan intonasi"),
 "SPK2": ("english.productive_speaking", "Berinteraksi dalam percakapan transaksional/interpersonal"),
 "SPK3": ("english.productive_speaking", "Menyampaikan opini dan argumen"),
 "SPK4": ("english.productive_speaking", "Mempresentasikan topik dengan kelancaran sesuai CEFR"),
 "WRT1": ("english.productive_writing", "Menulis kalimat, paragraf, dan teks koheren"),
 "WRT2": ("english.productive_writing", "Menulis deskripsi, narasi, prosedur, dan laporan"),
 "WRT3": ("english.productive_writing", "Menulis argumentasi serta tanggapan akademik"),
 "WRT4": ("english.productive_writing", "Merevisi tulisan berdasarkan rubrik"),
 "GRV1": ("english.grammar_vocabulary", "Menggunakan kelas kata, tenses, aspek, dan modalitas"),
 "GRV2": ("english.grammar_vocabulary", "Menggunakan frasa, klausa, serta kalimat kompleks"),
 "GRV3": ("english.grammar_vocabulary", "Mengembangkan kosakata umum, akademik, dan kolokasi"),
 "GRV4": ("english.grammar_vocabulary", "Menggunakan strategi pembentukan dan penebakan kata"),
 "PRN1": ("english.pronunciation", "Membedakan fonem dan pasangan bunyi minimal"),
 "PRN2": ("english.pronunciation", "Memproduksi bunyi sulit, ritme, serta intonasi"),
 "PRN3": ("english.pronunciation", "Memantau dan memperbaiki pelafalan mandiri"),
}
# kluster lama -> leaf (satu kluster = satu leaf, kecuali ada aturan judul di TITLE)
CLUSTER = {
 "Parts of Speech": "GRV1", "Tenses": "GRV1", "Modal Verbs": "GRV1", "Voice": "GRV1", "Comparison & Degrees": "GRV1", "Common Errors for Indonesian Learners": "GRV1",
 "Clauses": "GRV2", "Sentence Structure": "GRV2", "Building Simple Sentences": "GRV2", "Conditionals & Wishes": "GRV2", "Reported Speech": "GRV2",
 "Gerunds & Infinitives": "GRV2", "Advanced Grammar & Style": "GRV2",
 "Core Vocabulary": "GRV3", "Vocabulary Building": "GRV3", "Idiomatic English": "GRV3", "Time, Number & Measurement Expressions": "GRV3", "Word Formation": "GRV4",
 "Alphabet & Pronunciation": "PRN1", "Fluency & Pronunciation Practice": "PRN2",
 "Conversation in Context": "SPK2", "Functional Language": "SPK2",
 "Punctuation & Mechanics": "WRT1",
 "Teks Argumentatif & Evaluatif": "WRT3", "Teks Faktual & Prosedural": "WRT2", "Teks Naratif & Personal": "WRT2",
}
TITLE = {  # (kluster, judul topik) -> leaf, untuk kluster keterampilan yang isinya campuran
 ("Listening", "Listening for Gist"): "LIS2", ("Listening", "Listening for Specific Information"): "LIS1", ("Listening", "Conversations & Interviews"): "LIS2",
 ("Listening", "Connected & Fast Speech"): "LIS1", ("Listening", "Understanding Different Accents"): "LIS1", ("Listening", "Note-Taking While Listening"): "LIS2",
 ("Listening", "Listening to Lectures & Podcasts"): "LIS3",
 ("Reading", "Vocabulary in Context"): "REA1", ("Reading", "Main Ideas & Supporting Details"): "REA2", ("Reading", "Reading for Detail"): "REA2",
 ("Reading", "Skimming & Scanning"): "REA2", ("Reading", "Understanding Text Structure"): "REA2", ("Reading", "Speed Reading Techniques"): "REA2",
 ("Reading", "Inference & Implied Meaning"): "REA3", ("Reading", "Critical Reading & Evaluating Arguments"): "REA3",
 ("Speaking", "Everyday Conversation"): "SPK2", ("Speaking", "Handling Interviews"): "SPK2", ("Speaking", "Expressing & Defending Opinions"): "SPK3",
 ("Speaking", "Discussion & Debate"): "SPK3", ("Speaking", "Presentation Skills"): "SPK4", ("Speaking", "Narrating Events & Storytelling"): "SPK4",
 ("Speaking", "Describing People, Places & Things"): "SPK4", ("Speaking", "Fluency & Pronunciation Practice"): "PRN2",
 ("Writing", "Sentence to Paragraph"): "WRT1", ("Writing", "Paragraph Structure & Cohesion"): "WRT1", ("Writing", "Descriptive Writing"): "WRT2",
 ("Writing", "Narrative Writing"): "WRT2", ("Writing", "Expository Writing"): "WRT2", ("Writing", "Argumentative & Persuasive Writing"): "WRT3",
 ("Writing", "Summarizing & Paraphrasing"): "WRT3", ("Writing", "Editing & Proofreading"): "WRT4",
}
PRN_TITLE = {"Intonation Patterns": "PRN2", "Sentence Stress & Rhythm": "PRN2", "Word Stress": "PRN2", "Consonant Clusters & Digraphs": "PRN2"}
TEMPLATE = {"LIS": "INTERPRET", "REA": "INTERPRET", "SPK": "COMMUNICATE", "WRT": "COMMUNICATE", "GRV": "CONCEPT", "PRN": "PRACTICE"}
STANDARD_CEFR_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]


def main():
    lingkup = {r["topik_id"]: r for r in csv.DictReader(open(f"{D}/lingkup_p0_v1.csv")) if r["mapel"] == "English" and r["tier"] in ("P0a", "P0b")}
    topik = {r["id"]: r for r in csv.DictReader(open(f"{D}/pemetaan_topik_v1.csv"))}
    stat = {r["topik_id"]: r for r in csv.DictReader(open(f"{D}/statistik_bank_inggris.csv"))}
    rows = []
    for tid, l in lingkup.items():
        t = topik[tid]; s = stat.get(tid, {"bab": 0, "bab_materi": 0, "soal": 0, "soal_bertag": 0})
        bab, mat, soal, tag = int(s["bab"]), int(s["bab_materi"]), int(s["soal"]), int(s["soal_bertag"])
        cl, ti = t["cluster"], t["topic"]
        code, jenis = "", ""
        if t["jenis_pemetaan"].startswith("PATH-OWNED"): jenis = "STRATEGI-TES-MILIK-PATH"
        elif t["jenis_pemetaan"] == "CANONICAL":
            code = TITLE.get((cl, ti)) or PRN_TITLE.get(ti) or CLUSTER.get(cl, "")
            jenis = "UNIT-KANONIK" if code else "PERLU-PENENTUAN-LEAF"
        else: jenis = t["jenis_pemetaan"]
        strand, leaf = LEAF.get(code, ("", ""))
        if not jenis.startswith(("UNIT", "PERLU")): reuse = "-"
        elif bab and mat == bab and soal >= 20: reuse = "SIAP-DIPAKAI"      # materi lengkap + >=20 soal untuk bank tahap 1
        elif mat > 0 or soal >= 20: reuse = "SEBAGIAN"
        else: reuse = "KOSONG"
        rows.append({"topik_id": tid, "kluster": cl, "topik": ti, "jenis": jenis, "leaf_kode": code, "strand": strand, "leaf_usulan": leaf,
                     "template": TEMPLATE.get(code[:3], "EVALUATE" if jenis.startswith("STRATEGI") else ""), "cefr": t["cefr"], "tier": l["tier"],
                     "TKA": l["TKA"], "PTN": l["PTN"], "ENG": l["ENG"], "CAMB": l["CAMB"], "bab": bab, "bab_materi": mat, "soal": soal, "soal_bertag": tag, "kesiapan_pakai_ulang": reuse})
    rows.sort(key=lambda r: (r["jenis"], r["leaf_kode"], r["cefr"], r["topik"]))
    with open(f"{D}/pemetaan_inggris_v1.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

    units = [r for r in rows if r["jenis"].startswith("UNIT")]
    matrix = collections.defaultdict(collections.Counter)
    for r in units: matrix[f"{r['leaf_kode']} {r['leaf_usulan']}"][r["cefr"] or "-"] += 1
    reuse = collections.Counter(r["kesiapan_pakai_ulang"] for r in units)
    empty_leaves = [f"{k} {v[1]}" for k, v in LEAF.items() if not any(r["leaf_kode"] == k for r in units)]
    per_cefr = collections.defaultdict(collections.Counter)
    for r in units: per_cefr[r["cefr"] or "-"][r["kesiapan_pakai_ulang"]] += 1
    summ = {"topik_p0_inggris": len(rows), "per_jenis": dict(collections.Counter(r["jenis"] for r in rows)),
            "unit_kanonik": len(units), "kesiapan_pakai_ulang": dict(reuse),
            "kesiapan_per_cefr": {k: dict(per_cefr[k]) for k in STANDARD_CEFR_ORDER + ["-"] if k in per_cefr},
            "bab_unit": sum(r["bab"] for r in units), "bab_bermateri_unit": sum(r["bab_materi"] for r in units), "soal_unit": sum(r["soal"] for r in units),
            "soal_bertag_bloom_kesulitan": sum(r["soal_bertag"] for r in units),
            "leaf_tanpa_topik": empty_leaves,
            "matriks_leaf_x_cefr": {k: dict(v) for k, v in sorted(matrix.items())}}
    json.dump(summ, open(f"{D}/ringkasan_inggris.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(summ, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
