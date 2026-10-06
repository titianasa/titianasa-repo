#!/usr/bin/env python3
"""Pencocokan bab lama Matematika (topik P0) -> leaf pohon kanonik, tanpa LLM.
TF-IDF cosine sederhana pada token berimbuhan-dipangkas. Hasilnya USULAN, bukan keputusan:
skor rendah harus ditinjau manusia. Keluaran: pemetaan_leaf_matematika_v1.csv, ringkasan_leaf_matematika.json"""
import csv, re, math, json, collections, os

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(D)

STOP = set("dan yang dengan pada dari untuk dalam secara ke di atau sebuah suatu itu ini bagi oleh sebagai antara serta juga akan dapat adalah bentuk".split())
GENERIC_VERBS = set("menentukan menghitung menjelaskan menggunakan memahami mengenal membedakan menyelesaikan menerapkan menganalisis mengidentifikasi memilih membaca menyusun membuat mengubah memeriksa".split())
PREF = ("meng", "meny", "men", "mem", "me", "peng", "peny", "pen", "pem", "per", "ber", "ter", "di", "ke", "se")
SUFF = ("kan", "nya", "an", "i")


def stem(w):
    for s in SUFF:
        if w.endswith(s) and len(w) - len(s) >= 4:
            w = w[: -len(s)]; break
    for p in PREF:
        if w.startswith(p) and len(w) - len(p) >= 4:
            w = w[len(p):]; break
    return w


ABBR = {"spldv": "sistem persamaan linear dua variabel", "spltv": "sistem persamaan linear tiga variabel", "kpk": "kelipatan persekutuan terkecil", "fpb": "faktor persekutuan terbesar"}


def toks(text):
    text = text.lower()
    for a, full in ABBR.items(): text = re.sub(r"\b%s\b" % a, full, text)
    text = text.replace("×", " kali ").replace("÷", " bagi ")
    out = []
    for w in re.findall(r"[a-z0-9]+", text):
        if w in STOP or w in GENERIC_VERBS: continue
        out.append(stem(w))
    return out


def load_leaves():
    tree = open(f"{OUT}/POHON_HIERARKI_MATEMATIKA_V1.md").read().splitlines()
    leaves, cur, cname = [], None, ""
    for line in tree:
        m = re.match(r"^[├└]─ ([a-z_]+\.[a-z_]+) — (.+)$", line)
        if m: cur, cname = m.group(1), m.group(2); continue
        m = re.match(r"^(?:│  |   )(?:├─|└─) (.+)$", line)
        if m and cur: leaves.append({"concept": cur, "concept_name": cname, "leaf": m.group(1).strip()})
    return leaves


def main():
    leaves = load_leaves()
    lingkup = {r["topik_id"]: r for r in csv.DictReader(open(f"{D}/lingkup_p0_v1.csv"))
               if (r["mapel"] == "Matematika" and r["tier"] in ("P0a", "P0b")) or r["tier"] == "MERGE"}
    babs = [b for b in csv.DictReader(open(f"{D}/bab_lama.csv")) if b["topik_id"] in lingkup]

    docs = [toks(l["leaf"]) + toks(l["concept_name"]) * 0 for l in leaves]      # konsep tidak ikut agar tidak mendominasi
    bdocs = [toks(b["bab"] + " " + b["topik"]) for b in babs]
    df = collections.Counter(w for d in docs + bdocs for w in set(d))
    N = len(docs) + len(bdocs)
    idf = {w: math.log((N + 1) / (c + 1)) + 1 for w, c in df.items()}

    def vec(d):
        c = collections.Counter(d); v = {w: n * idf.get(w, 1) for w, n in c.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        return {w: x / norm for w, x in v.items()}
    lv = [vec(d) for d in docs]

    rows = []
    for b, d in zip(babs, bdocs):
        bv = vec(d); topic = lingkup[b["topik_id"]]; home = topic["konsep_kanonik"]
        scored = []
        for i, l in enumerate(leaves):
            raw = sum(bv.get(w, 0) * x for w, x in lv[i].items())
            scored.append((raw, i))
        in_c = max(((r, i) for r, i in scored if leaves[i]["concept"] == home), default=(0, None))
        glob = max(scored, default=(0, None))
        # utamakan leaf di konsep topik; menyeberang konsep hanya bila jauh lebih cocok
        cross = glob[1] is not None and leaves[glob[1]]["concept"] != home and glob[0] >= 0.45 and glob[0] >= in_c[0] + 0.30
        raw, i = glob if (cross or in_c[1] is None) else in_c
        l = leaves[i] if i is not None else None
        same = bool(l and l["concept"] == home)
        if l is None or raw < 0.15: status = "TANPA-LEAF"
        elif cross: status = "PERLU-TINJAU"
        elif raw >= 0.45: status = "AUTO-KUAT"
        elif raw >= 0.25: status = "PERLU-TINJAU"
        else: status = "LEMAH"
        if re.search(r"kesalahan umum|rangkuman|latihan|strategi", b["bab"].lower()) and status != "AUTO-KUAT":
            status = "BAGIAN-PENDUKUNG"
        extra = []
        if l is not None and status in ("AUTO-KUAT", "PERLU-TINJAU"):
            for r2, j in sorted(scored, reverse=True):
                if j != i and leaves[j]["concept"] == l["concept"] and r2 >= max(0.25, 0.7 * raw) and len(extra) < 2: extra.append(leaves[j]["leaf"])
        rows.append({"bab_id": b["bab_id"], "topik_id": b["topik_id"], "topik": b["topik"], "bab": b["bab"], "konsep_topik": home,
                     "leaf_usulan": l["leaf"] if l else "", "leaf_tambahan": " || ".join(extra), "konsep_leaf": l["concept"] if l else "", "skor": round(raw, 3),
                     "konsep_sama": int(same), "status": status})
    with open(f"{D}/pemetaan_leaf_matematika_v1.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

    st = collections.Counter(r["status"] for r in rows)
    cov = collections.defaultdict(set)
    for r in rows:
        if r["status"] in ("AUTO-KUAT", "PERLU-TINJAU"):
            cov[(r["konsep_leaf"], r["leaf_usulan"])].add(r["topik_id"])
            for x in filter(None, r["leaf_tambahan"].split(" || ")): cov[(r["konsep_leaf"], x)].add(r["topik_id"])
    covered = {k for k in cov}
    unc = [l for l in leaves if (l["concept"], l["leaf"]) not in covered]
    multi = sorted(((k, len(v)) for k, v in cov.items() if len(v) >= 3), key=lambda x: -x[1])[:15]
    summ = {"bab": len(rows), "topik": len(lingkup), "status": dict(st), "leaf_total": len(leaves), "leaf_tercakup": len(covered),
            "leaf_belum_tercakup": len(unc), "leaf_belum_tercakup_per_konsep": dict(collections.Counter(l["concept"] for l in unc)),
            "leaf_dirujuk_>=3_topik_berbeda": [{"leaf": k[1], "konsep": k[0], "topik": n} for k, n in multi]}
    strong = {(r["konsep_leaf"], r["leaf_usulan"]) for r in rows if r["status"] == "AUTO-KUAT"}
    ADV = {"number.complex", "algebra.linear_algebra", "geometry.differential", "analysis.real", "analysis.differential_equations", "analysis.advanced",
           "number_theory.algebraic", "discrete.foundations", "modeling.finance_games", "modeling.stochastic_processes", "modeling.numerical_computation",
           "calculus.multivariable", "modeling.mechanics", "number_theory.elementary", "discrete.combinatorics_graphs", "modeling.optimization_operations",
           "statistics.inference", "probability.random_variables"}
    with open(f"{D}/status_leaf_matematika_v1.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["konsep", "leaf", "status", "jumlah_topik", "tingkat_konsep"])
        for l in leaves:
            k = (l["concept"], l["leaf"]); n = len(cov.get(k, ()))
            st = "belum-tercakup" if k not in covered else ("tercakup-kuat" if k in strong else "tercakup-lemah/gabungan")
            w.writerow([l["concept"], l["leaf"], st, n, "lanjut/kuliah (asumsi)" if l["concept"] in ADV else "sekolah-ujian (asumsi)"])
    summ["leaf_sekolah_ujian_belum_tercakup"] = sum(1 for l in leaves if (l["concept"], l["leaf"]) not in covered and l["concept"] not in ADV)
    json.dump(summ, open(f"{D}/ringkasan_leaf_matematika.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(summ, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
