#!/usr/bin/env python3
"""Compact listing of a subject's canonical topics for bab planning:
numbered in export order, grouped by tahap and domain, with the learning
paths that reference each domain (trimmed to what distinguishes them)."""
import collections, json, sys

EXPORT = "/tmp/claude-1000/-home-john-Dev-sanja-workspace-alr/9a74c488-7a92-4015-bac7-8b8bcd8f6581/scratchpad/topics/all.json"
subject = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
end = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
rows = [r for r in json.load(open(EXPORT)) if r["subject"] == subject]
last_tahap = last_domain = None
for i, r in enumerate(rows, start=1):
    if not start <= i <= end:
        continue
    if r["tahap"] != last_tahap:
        print(f"\n## {r['tahap']}")
        last_tahap, last_domain = r["tahap"], None
    if r["domain"] != last_domain:
        dom = [x for x in rows if x["tahap"] == r["tahap"] and x["domain"] == r["domain"]]
        paths = collections.Counter(p for x in dom for p in x["paths"])
        short = sorted({" › ".join(p.split(" › ")[:3]) for p in paths})
        print(f"### {r['domain']}  [dipakai: {' | '.join(short)}]")
        last_domain = r["domain"]
    print(f"{i}. {r['topic']}")
