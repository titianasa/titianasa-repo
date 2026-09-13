#!/usr/bin/env python3
"""Cross-bab near-duplicate report for one topic's quizzes.

Two questions from DIFFERENT quiz items are flagged when their stems
share most of their content words (Jaccard >= threshold after dropping
LaTeX, numbers and Indonesian stopwords). Same-quiz pairs are ignored:
a group already sees its own questions when it is generated.

Usage: duplicate_report.py [backup.json]   (no arg = live database)
"""
import itertools, json, re, subprocess, sys

THRESHOLD = 0.35
STOP = set("""yang dan di ke dari pada adalah ini itu dengan untuk dalam sebagai atau tersebut berikut
berapa manakah apakah bagaimana bilangan bilangan-bilangan suatu sebuah seorang jika maka tepat benar
paling pernyataan perhatikan dua tiga empat satu nilai garis adalah ... disebut""".split())

def words(text):
    text = re.sub(r"\$[^$]*\$", " ", text or "")
    toks = re.findall(r"[a-zA-Z]+", text.lower())
    return {t for t in toks if len(t) > 2 and t not in STOP}

def load():
    if len(sys.argv) > 1:
        return [(x["title"], x["quiz_config"]) for x in json.load(open(sys.argv[1]))]
    out = subprocess.run(["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-t", "-A", "-c",
        "select jsonb_agg(jsonb_build_object('title', title, 'quiz_config', quiz_config) order by created_at) from module_items "
        "where content_type='quiz' and title like 'Latihan —%' and coalesce(jsonb_array_length(quiz_config->'question_groups'),0) > 0;"],
        capture_output=True, text=True).stdout
    return [(x["title"], x["quiz_config"]) for x in json.loads(out)]

qs = []
for title, cfg in load():
    for g in cfg["question_groups"]:
        for q in g["questions"]:
            stem = q.get("stem") or q.get("text") or ""
            qs.append((title.replace("Latihan — ", "")[:30], q.get("number"), (q.get("taxonomy") or {}).get("bloom", "?").upper(), stem, words(stem)))

pairs = []
for a, b in itertools.combinations(qs, 2):
    if a[0] == b[0] or not a[4] or not b[4]:
        continue
    j = len(a[4] & b[4]) / len(a[4] | b[4])
    if j >= THRESHOLD:
        pairs.append((j, a, b))
pairs.sort(key=lambda p: -p[0])
print(f"soal: {len(qs)} | pasangan mirip antar-bab (Jaccard >= {THRESHOLD}): {len(pairs)}")
for j, a, b in pairs:
    print(f"  {j:.2f}  [{a[0]} #{a[1]} {a[2]}] {re.sub(chr(10),' ',a[3])[:70]}")
    print(f"        [{b[0]} #{b[1]} {b[2]}] {re.sub(chr(10),' ',b[3])[:70]}")
