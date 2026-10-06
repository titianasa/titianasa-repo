#!/usr/bin/env python3
"""Plan for completing the canonical units that have no materi yet (no AI).

Input (exported from the dev DB into a work dir): units.json, babs.json,
concept_topics.json. Output: plan_unit_materi.json with one action per unit:
  into      generate into an existing kerangka bab that IS this unit
  scaffold  create a new bab (named by the unit) in a legacy topic, then generate
  review    an existing bab with materi looks like the same subject: NOT generated
  no_topic  no legacy topic to put a new bab in: NOT generated
Duplicate check: idf-weighted overlap of the unit name with each bab that
already has materi in the unit's topics (title x3 + section titles), after a
crude id/en stemmer, so "Membulatkan" finds "Pembulatan".
"""
import json, math, re, sys, collections

d = sys.argv[1] if len(sys.argv) > 1 else "."
units = json.load(open(f"{d}/units.json"))
babs = json.load(open(f"{d}/babs.json"))
ctopics = json.load(open(f"{d}/concept_topics.json"))

STOP = set("""yang dan dengan untuk dari pada adalah ini itu atau dalam akan tidak jika maka saat juga oleh dapat bisa agar sesuai
serta antara hingga sampai secara lebih kata the and for are with that this from have you not was can of in on to a an is as by at be
using use how what why when your their its cara dasar konsep pengantar dalam bilangan""".split())

def stem(w):
    w = w.lower()
    for p in ("meng", "meny", "mem", "men", "me", "peng", "peny", "pem", "pen", "pe", "ber", "ter", "di", "ke", "se"):
        if w.startswith(p) and len(w) - len(p) >= 4:
            w = w[len(p):]
            break
    for s in ("kan", "nya", "an", "i", "ing", "ed", "es", "s"):
        if w.endswith(s) and len(w) - len(s) >= 4:
            w = w[: -len(s)]
            break
    return w

def toks(text):
    return [stem(t) for t in re.split(r"[^A-Za-z0-9]+", text or "") if len(t) >= 3 and t.lower() not in STOP]

docs = {}
for b in babs:
    tf = collections.Counter()
    for t in toks(b["title"]):
        tf[t] += 3
    for t in toks(b.get("sections") or ""):
        tf[t] += 1
    docs[b["bab"]] = tf
N = len(docs)
df = collections.Counter(t for tf in docs.values() for t in tf)
idf = lambda t: math.log(1 + N / (df.get(t, 0) + 0.5))

by_topic = collections.defaultdict(list)
for b in babs:
    by_topic[b["topic"]].append(b)

concept_major = {}
for r in ctopics:
    c = concept_major.get(r["concept"])
    if c is None or r["n"] > c[1]:
        concept_major[r["concept"]] = (r["topic"], r["n"])

def overlap_small(a, b):
    a, b = set(toks(a)), set(toks(b))
    return len(a & b) / max(1, min(len(a), len(b)))

plan, counts = [], collections.Counter()
used_bab = set()
for u in units:
    if any(s["materi"] for s in u["sources"]):
        continue
    ut = toks(u["name"])
    topics = set()
    if u["topic"]: topics.add(u["topic"])
    for s in u["sources"]: topics.add(s["topic"])
    if u["concept"] in concept_major: topics.add(concept_major[u["concept"]][0])
    best = None
    for tp in topics:
        for b in by_topic.get(tp, []):
            tf = docs[b["bab"]]
            tot = sum(idf(t) for t in set(ut)) or 1
            sc = sum(idf(t) for t in set(ut) if t in tf) / tot
            if best is None or sc > best[0]:
                best = (sc, b)
    entry = {"module_id": u["module_id"], "name": u["name"], "subj": u["subj"], "concept": u["concept_name"], "strand": u["strand"], "cefr": u["cefr"], "labels": u["labels"]}
    if best and best[0] >= 0.45:
        entry.update(action="review", candidate={"bab": best[1]["bab"], "title": best[1]["title"], "score": round(best[0], 2)})
    else:
        into = [s for s in u["sources"] if s["article"] and s["bank"] and not s["materi"] and overlap_small(u["name"], s["title"]) >= 0.5]
        into = [s for s in into if s["bab"] not in used_bab]  # one bab serves one unit
        if into:
            into.sort(key=lambda s: (s["strength"] != "kuat", -overlap_small(u["name"], s["title"])))
            used_bab.add(into[0]["bab"])
            entry.update(action="into", bab=into[0]["bab"], bab_title=into[0]["title"])
        else:
            topic = u["topic"] or next((s["topic"] for s in u["sources"]), None) or (concept_major.get(u["concept"]) or (None,))[0]
            if topic:
                entry.update(action="scaffold", topic=topic)
            else:
                entry.update(action="no_topic")
    counts[(u["subj"], entry["action"])] += 1
    plan.append(entry)

json.dump(plan, open(f"{d}/plan_unit_materi.json", "w"), ensure_ascii=False, indent=1)
for k, v in sorted(counts.items()): print(k, v)
print("total", len(plan))
