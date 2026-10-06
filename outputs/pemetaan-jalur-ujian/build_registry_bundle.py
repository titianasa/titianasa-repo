#!/usr/bin/env python3
"""Paket registri kanonik (JSON) untuk diimpor ke database oleh `import_canonical_registry`.
Menyatukan: pohon Matematika (253 leaf), registri Inggris (203 unit), aset path ujian Inggris, dan jalur yang diturunkan dari LABEL.
Jalur tidak menyimpan salinan: node hanya merujuk unit (module_id) atau aset milik path. Semua isi di sini USULAN yang masih perlu ditinjau."""
import csv, json, os, re, collections

D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(D)
def slug(s, n=70): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:n].strip("-")

bab = {r["bab_id"]: r for r in csv.DictReader(open(f"{D}/bab_lama.csv"))}
bab_by_topic = collections.defaultdict(list)
for r in bab.values(): bab_by_topic[r["topik_id"]].append(r)
for v in bab_by_topic.values(): v.sort(key=lambda r: int(r["order_index"]))
def has(b): return str(b["punya_materi"]).lower() in ("t", "true", "1")

domains = [{"code": "mathematics", "name": "Matematika"}, {"code": "english", "name": "Bahasa Inggris"}]
subjects = [{"code": "matematika", "domain": "mathematics", "name": "Matematika"}, {"code": "bahasa_inggris", "domain": "english", "name": "Bahasa Inggris"}]
strands, concepts, units = [], [], []

# ---------------- Matematika: pohon ----------------
STRAND_NAMES = {}
tree = open(f"{OUT}/POHON_HIERARKI_MATEMATIKA_V1.md").read().splitlines()
cur_strand = cur_concept = None; s_order = c_order = u_order = 0; seen = set(); leaf_index = {}
for line in tree:
    m = re.match(r"^## \d+\. Strand `([a-z_]+)` — (.+)$", line)
    if m: cur_strand = m.group(1); STRAND_NAMES[cur_strand] = m.group(2); s_order += 1; strands.append({"subject": "matematika", "code": cur_strand, "name": m.group(2), "order": s_order}); c_order = 0; continue
    m = re.match(r"^[├└]─ ([a-z_]+\.[a-z_]+) — (.+)$", line)
    if m and cur_strand: cur_concept = m.group(1); c_order += 1; concepts.append({"strand": cur_strand, "code": cur_concept, "name": m.group(2), "order": c_order}); u_order = 0; continue
    m = re.match(r"^(?:│  |   )(?:├─|└─) (.+)$", line)
    if m and cur_concept:
        name = m.group(1).strip(); u_order += 1
        mid = f"math.{cur_concept}.{slug(name)}.v1"
        if mid in seen: mid = mid.replace(".v1", f"-{u_order}.v1")
        seen.add(mid)
        units.append({"module_id": mid, "concept": cur_concept, "name": name, "legacy_title": None, "cefr": None, "template": None, "tier": None, "status": "planned",
                      "labels": [["domain", "mathematics"], ["subject", "matematika"], ["strand", cur_strand], ["concept", cur_concept]], "sources": [], "source_topic_id": None, "order": u_order})
        leaf_index[(cur_concept, name)] = units[-1]

# sumber Matematika: bab lama yang cocok dengan leaf (hasil pemetaan leaf)
topik_meta = {r["id"]: r for r in csv.DictReader(open(f"{D}/pemetaan_topik_v1.csv"))}
ref = list(csv.DictReader(open(f"{D}/referensi_lama.csv")))
LABEL_MATH = {("TKA Numerasi", "Matematika"): [["exam", "tka"], ["exam-component", "numerasi"]], ("AKM Numerasi", "Matematika"): [["exam", "akm"], ["exam-component", "numerasi"]],
    ("UTBK-SNBT — Literasi & Penalaran Matematika", "Penalaran Matematika (PM)"): [["exam", "utbk-snbt"], ["exam-component", "penalaran-matematika"]],
    ("UTBK-SNBT — Tes Potensi Skolastik", "Pengetahuan Kuantitatif (PK)"): [["exam", "utbk-snbt"], ["exam-component", "pengetahuan-kuantitatif"]]}
CAMB_MATH = {"IGCSE Mathematics (0580)": "cambridge:igcse-math", "IGCSE Additional Mathematics (0606)": "cambridge:igcse-addmath", "A Level Mathematics — Pure (9709)": "cambridge:a-level-pure",
             "A Level Mathematics — Statistics": "cambridge:a-level-stats", "A Level Further Mathematics (9231)": "cambridge:a-level-further"}
topic_labels = collections.defaultdict(set)
for r in ref:
    if r["mapel"] != "Matematika": continue
    for l in LABEL_MATH.get((r["seksi"].strip(), r["subseksi"].strip()), []): topic_labels[r["topik_id"]].add(tuple(l))
    if r["subseksi"] in CAMB_MATH: ns, v = CAMB_MATH[r["subseksi"]].split(":"); topic_labels[r["topik_id"]].add((ns, v))
mapped = 0
for r in csv.DictReader(open(f"{D}/pemetaan_leaf_matematika_v1.csv")):
    if r["status"] not in ("AUTO-KUAT", "PERLU-TINJAU"): continue
    leaves = [r["leaf_usulan"]] + [x for x in r["leaf_tambahan"].split(" || ") if x]
    for lf in leaves:
        u = leaf_index.get((r["konsep_leaf"], lf))
        if not u: continue
        if r["bab_id"] not in {s["bab_id"] for s in u["sources"]}:
            b = bab.get(r["bab_id"]); u["sources"].append({"bab_id": r["bab_id"], "kekuatan": "kuat" if r["status"] == "AUTO-KUAT" else "tinjau", "punya_materi": bool(b and has(b))}); mapped += 1
        for l in topic_labels.get(r["topik_id"], ()):
            if list(l) not in u["labels"]: u["labels"].append(list(l))
        u["source_topic_id"] = u["source_topic_id"] or r["topik_id"]
for u in units:
    if u["sources"]: u["status"] = "draft" if any(s["punya_materi"] for s in u["sources"]) else "kerangka"

# ---------------- Inggris: registri ----------------
KONSEP_NAME = {}
E_STRAND = {"receptive_listening": "Menyimak (reseptif)", "receptive_reading": "Membaca (reseptif)", "productive_speaking": "Berbicara (produktif)", "productive_writing": "Menulis (produktif)", "grammar_vocabulary": "Tata bahasa dan kosakata", "pronunciation": "Pelafalan"}
reg = list(csv.DictReader(open(f"{D}/registry_inggris_v1.csv")))
c_seen = {}; c_ord = collections.Counter()
for i, (k, v) in enumerate(E_STRAND.items(), 1): strands.append({"subject": "bahasa_inggris", "code": k, "name": v, "order": i})
for r in reg:
    key = (r["strand"], r["konsep_kode"])
    if key not in c_seen:
        code = r["module_id"].split(".")[2]; c_seen[key] = f"english.{code}"; c_ord[r["strand"]] += 1
        concepts.append({"strand": r["strand"], "code": f"english.{code}", "name": r["konsep"], "order": c_ord[r["strand"]]})
order_in = collections.Counter()
for r in reg:
    cc = c_seen[(r["strand"], r["konsep_kode"])]; order_in[cc] += 1
    labels = [l.split(":", 1) for l in r["label"].split(";")]
    srcs = [{"bab_id": b["bab_id"], "kekuatan": "kuat", "punya_materi": has(b)} for b in bab_by_topic.get(r["sumber_topik_id"], [])]
    units.append({"module_id": r["module_id"], "concept": cc, "name": r["unit"], "legacy_title": r["judul_lama"], "cefr": r["cefr"], "template": r["template"], "tier": r["tier"],
                  "status": {"SIAP-DIPAKAI": "draft", "SEBAGIAN": "draft", "KOSONG": "kerangka"}.get(r["kesiapan"], "planned"), "labels": labels, "sources": srcs,
                  "source_topic_id": r["sumber_topik_id"], "bank_soal_lama": int(r["soal_ada"]), "order": order_in[cc]})
by_mid = {u["module_id"]: u for u in units}

# ---------------- aset milik path (Inggris) ----------------
assets = []
for a in csv.DictReader(open(f"{D}/aset_path_inggris_v1.csv")):
    bs = bab_by_topic.get(a["sumber_topik_id"], [])
    assets.append({"asset_key": a["asset_id"], "ujian": a["ujian"], "kind": a["jenis_aset"], "title": a["judul_lama"], "merujuk_strand": a["merujuk_strand"] or None,
                   "source_topic_id": a["sumber_topik_id"], "status": "draft" if a["kesiapan"] == "ADA-MATERI" else "kerangka",
                   "sources": [{"bab_id": b["bab_id"], "punya_materi": has(b)} for b in bs]})

# ---------------- jalur (diturunkan dari label, tanpa salinan) ----------------
def with_label(ns, val): return [u for u in units if [ns, val] in u["labels"]]
def has_lab(u, ns, val): return [ns, val] in u["labels"]
def unit_nodes(us, role="required"): return [{"type": "unit", "module_id": u["module_id"], "role": role} for u in us]
def by_concept_groups(us):
    cord = {c["code"]: (c["strand"], c["order"]) for c in concepts}; sord = {s["code"]: s["order"] for s in strands}
    g = collections.OrderedDict()
    for u in sorted(us, key=lambda u: (sord[cord[u["concept"]][0]], cord[u["concept"]][1], u["order"])): g.setdefault(u["concept"], []).append(u)
    names = {c["code"]: c["name"] for c in concepts}
    return [{"type": "group", "title": names[k], "children": unit_nodes(v)} for k, v in g.items()]
paths = []
CEFR = ["A1", "A2", "B1", "B2", "C1", "C2"]
paths.append({"slug": "cefr-inggris", "name": "Bahasa Inggris berdasarkan CEFR", "kind": "fondasi", "description": "Satu himpunan unit Inggris, diurutkan menurut tingkat CEFR. Cambridge dan tes bahasa merujuk unit yang sama.",
              "nodes": [{"type": "group", "title": f"CEFR {c}", "children": unit_nodes(sorted([u for u in units if u["cefr"] == c], key=lambda u: (u["concept"], u["order"])))} for c in CEFR]})
CAMB_E = [("yle-starters", "YLE Starters (Pre-A1)"), ("yle-movers", "YLE Movers (A1)"), ("yle-flyers", "YLE Flyers (A2)"), ("ket-a2", "A2 Key (KET)"), ("pet-b1", "B1 Preliminary (PET)"), ("fce-b2", "B2 First (FCE)"), ("cae-c1", "C1 Advanced (CAE)"), ("cpe-c2", "C2 Proficiency (CPE)")]
paths.append({"slug": "cambridge-english", "name": "Cambridge English (YLE dan Main Suite)", "kind": "sertifikasi", "description": "Label pada unit CEFR yang sama; tidak ada salinan materi.",
              "nodes": [{"type": "group", "title": t, "children": unit_nodes(with_label("cambridge", k))} for k, t in CAMB_E]})
paths.append({"slug": "tka-bahasa-inggris", "name": "TKA — Bahasa Inggris", "kind": "ujian", "description": "Komponen Bahasa Inggris. Struktur resmi per jenjang belum diverifikasi.", "nodes": [{"type": "gate", "title": "Placement per konsep", "rules": {}}] + by_concept_groups(with_label("exam", "tka") and [u for u in with_label("exam", "tka") if u["cefr"]])})
paths.append({"slug": "utbk-literasi-bahasa-inggris", "name": "UTBK-SNBT — Literasi Bahasa Inggris", "kind": "ujian", "description": "Subtes literasi Bahasa Inggris.", "nodes": by_concept_groups([u for u in with_label("exam", "utbk-snbt") if u["cefr"]])})
EXAM_NAME = {"ielts": "IELTS", "toefl-ibt": "TOEFL iBT", "toefl-itp": "TOEFL ITP", "toeic": "TOEIC", "pte-academic": "PTE Academic", "duolingo": "Duolingo English Test"}
for ex, nm in EXAM_NAME.items():
    own = [a for a in assets if a["ujian"] == ex]
    paths.append({"slug": ex, "name": f"Persiapan {nm}", "kind": "sertifikasi", "description": "Aset strategi dan simulasi milik path, ditambah unit keterampilan Inggris yang dirujuk.",
                  "nodes": [{"type": "group", "title": "Strategi dan format ujian (milik path)", "children": [{"type": "asset", "asset_key": a["asset_key"], "role": "assessment" if a["kind"] == "assessment" else "required"} for a in own]}] + [{"type": "group", "title": "Unit keterampilan yang dirujuk", "children": by_concept_groups([u for u in with_label("exam", ex) if u["cefr"]])}]})
umum = [a for a in assets if a["ujian"] == "umum"]
paths.append({"slug": "persiapan-tes-internasional", "name": "Persiapan tes internasional (umum)", "kind": "sertifikasi", "description": "Strategi lintas tes: IELTS, TOEFL, TOEIC.", "nodes": [{"type": "asset", "asset_key": a["asset_key"], "role": "required"} for a in umum]})
MATH_PATHS = [("tka-numerasi", "TKA — Numerasi", "ujian", ("exam-component", "numerasi"), ("exam", "tka")), ("akm-numerasi", "AKM — Numerasi", "ujian", ("exam", "akm"), None),
    ("utbk-penalaran-matematika", "UTBK-SNBT — Penalaran Matematika", "ujian", ("exam-component", "penalaran-matematika"), None), ("utbk-pengetahuan-kuantitatif", "UTBK-SNBT — Pengetahuan Kuantitatif", "ujian", ("exam-component", "pengetahuan-kuantitatif"), None),
    ("cambridge-igcse-mathematics", "Cambridge IGCSE Mathematics (0580)", "sertifikasi", ("cambridge", "igcse-math"), None), ("cambridge-igcse-additional-mathematics", "Cambridge IGCSE Additional Mathematics (0606)", "sertifikasi", ("cambridge", "igcse-addmath"), None),
    ("cambridge-a-level-pure", "Cambridge A Level Mathematics — Pure (9709)", "sertifikasi", ("cambridge", "a-level-pure"), None), ("cambridge-a-level-further", "Cambridge A Level Further Mathematics (9231)", "sertifikasi", ("cambridge", "a-level-further"), None)]
for slg, nm, kind, lab, alt in MATH_PATHS:
    us = [u for u in units if u["module_id"].startswith("math.") and has_lab(u, *lab)]
    paths.append({"slug": slg, "name": nm, "kind": kind, "description": "Unit Matematika yang dirujuk; diturunkan dari label pada unit, bukan dari salinan. Pemetaan leaf masih usulan.", "nodes": by_concept_groups(us)})

paths = [p for p in paths if any(n["type"] != "group" or n.get("children") for n in p["nodes"]) and sum(1 for _ in p["nodes"]) > 0]
bundle = {"versi": "v1", "domains": domains, "subjects": subjects, "strands": strands, "concepts": concepts, "units": units, "path_assets": assets, "paths": paths}
json.dump(bundle, open(f"{D}/registry_kanonik_v1.json", "w"), ensure_ascii=False)
def count_nodes(ns): return sum(1 + count_nodes(n.get("children", [])) for n in ns)
print("domain", len(domains), "mapel", len(subjects), "strand", len(strands), "konsep", len(concepts), "unit", len(units), f"(Matematika {sum(1 for u in units if u['module_id'].startswith('math.'))}, Inggris {sum(1 for u in units if u['module_id'].startswith('english.'))})")
print("Matematika: bab tertaut ke leaf", mapped, "| unit Matematika bersumber:", sum(1 for u in units if u["module_id"].startswith("math.") and u["sources"]), "| status", dict(collections.Counter(u["status"] for u in units)))
print("aset path", len(assets), "| jalur", len(paths), "| node total", sum(count_nodes(p["nodes"]) for p in paths))
for p in paths: print("  ", p["slug"], count_nodes(p["nodes"]))
