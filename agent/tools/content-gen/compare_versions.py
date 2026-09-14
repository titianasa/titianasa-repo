#!/usr/bin/env python3
"""Side-by-side metrics for one topic: a JSON backup (v1) vs the live DB (v2).

Usage: compare_versions.py <backup.json> <module_id>
"""
import collections, json, re, subprocess, sys

BANNED = ["himpunan", "unsur identitas", "rasional", "notasi ilmiah", "kuantitas", "literasi numerasi", "aritmetika", "fondasi"]


def live(module_id):
    out = subprocess.run(
        ["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-t", "-A", "-c",
         f"select jsonb_agg(jsonb_build_object('title', title, 'content_type', content_type, 'lesson_plan', lesson_plan, 'quiz_config', quiz_config) order by order_index) "
         f"from module_items where module_id='{module_id}' and content_type is not null;"],
        capture_output=True, text=True).stdout
    return json.loads(out)


def prose(text):
    # Drop ALM directive blocks' keys, math, markdown symbols — keep readable sentences.
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    text = re.sub(r"\$[^$]*\$", " X ", text)
    text = re.sub(r"^:::\w*$", " ", text, flags=re.M)
    text = re.sub(r"^\s*(term|definition|explanation|variant|title|text|left_label|right_label|rows|items|steps):", " ", text, flags=re.M)
    return re.sub(r"[#*_`>|\[\]]", " ", text)


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+|\n+", prose(text))
    return [p for p in (x.strip() for x in parts) if len(p.split()) >= 3]


def article_stats(items):
    rows = []
    for it in items:
        if it["content_type"] != "article" or not it["lesson_plan"]:
            continue
        secs = it["lesson_plan"]["sections"]
        body = "\n".join(s["content"] for s in secs)
        sents = sentences(body)
        lens = [len(s.split()) for s in sents]
        low = body.lower()
        rows.append({
            "bab": it["title"].replace("Pembahasan — ", ""),
            "kata": len(prose(body).split()),
            "bagian": len(secs),
            "rata_kalimat": sum(lens) / max(1, len(lens)),
            "pct_panjang": 100 * sum(1 for l in lens if l > 15) / max(1, len(lens)),
            "terlarang": sum(low.count(t) for t in BANNED),
            "emdash": body.count("—"),
            "judul_bagian": [s["title"] for s in secs],
        })
    return rows


def quiz_stats(items):
    types, bloom, counts = collections.Counter(), collections.Counter(), []
    for it in items:
        if it["content_type"] != "quiz" or not it["quiz_config"]:
            continue
        n = 0
        for g in it["quiz_config"].get("question_groups", []):
            for q in g.get("questions", []):
                types[g["type"]] += 1
                tax = q.get("taxonomy") or {}
                bloom[f"{tax.get('bloom', '?')}/{tax.get('difficulty', '?')}"] += 1
                n += 1
        counts.append(n)
    return types, bloom, counts


def summary(label, items):
    arts = article_stats(items)
    types, bloom, counts = quiz_stats(items)
    kata = [a["kata"] for a in arts]
    print(f"\n==================== {label} ====================")
    print(f"Artikel: {len(arts)} bab | kata/bab rata {sum(kata)/max(1,len(kata)):.0f} (min {min(kata)}, maks {max(kata)}) | total {sum(kata)}")
    print(f"Rata kata/kalimat: {sum(a['rata_kalimat'] for a in arts)/len(arts):.1f} | kalimat >15 kata: {sum(a['pct_panjang'] for a in arts)/len(arts):.0f}%")
    print(f"Istilah terlarang (total): {sum(a['terlarang'] for a in arts)} | tanda pisah (—): {sum(a['emdash'] for a in arts)}")
    nt = sum(1 for a in arts if any("nilai tempat" in t.lower() for t in a["judul_bagian"]))
    print(f"Bab yang punya BAGIAN berjudul 'nilai tempat': {nt} dari {len(arts)}")
    print(f"Kuis: {sum(counts)} soal ({counts}) | jenis: {dict(types)}")
    print(f"Taksonomi: {dict(sorted(bloom.items()))}")
    print("Judul bagian per bab:")
    for a in arts:
        print(f"  [{a['kata']:>4} kata, {a['rata_kalimat']:.1f} kt/kal] {a['bab']}")
        print(f"      {' | '.join(a['judul_bagian'])}")


if __name__ == "__main__":
    summary("V1 (sebelum)", json.load(open(sys.argv[1])))
    summary("V2 (sesudah)", live(sys.argv[2]))
