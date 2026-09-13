#!/usr/bin/env python3
"""Converts a topic's flat bab-articles into bab SECTIONS, each holding
its own explanation article and quiz.

    Topik (module)
    └── <Judul Bab>            node_type=section
        ├── Pembahasan         content_type=article
        └── Latihan            content_type=quiz

The specific name lives on the section; the children are named for their
ROLE, so a second angle later ("Pembahasan Lanjutan") or a second quiz
slots in without renaming anything. Runs against the same bab JSON the
flat pass used, and is idempotent — a topic already in the new shape is
only re-ordered, never duplicated.

Usage:  python3 convert_bab_sections.py bab_matematika_tahap1.json [--dry-run]
"""

import json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiz_sweep as qs

SCRATCH = os.path.dirname(os.path.abspath(__file__))
CHILDREN = [("Pembahasan", "article"), ("Latihan", "quiz")]


def main():
    data_path = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    path = data_path if os.path.isabs(data_path) else os.path.join(SCRATCH, data_path)
    data = json.load(open(path))
    topics = data["topik"]
    progress_path = os.path.join(SCRATCH, f"progress_sections_{os.path.basename(data_path)}")
    done = set(json.load(open(progress_path))) if os.path.exists(progress_path) else set()

    qs.log(f"=== KONVERSI SECTION: {data['mapel']} / {data['tahap']} — {len(topics)} topik ({len(done)} selesai) ===")
    token = qs.mint_user("qa-bab-dev@example.com", "curriculum_developer")

    converted = failed = 0
    for i, t in enumerate(topics, 1):
        tid, title, bab = t["topic_id"], t["topic_title"], t["bab"]
        if tid in done:
            continue

        status, tree = qs.api("GET", f"/modules/{tid}/items", token)
        if status != 200:
            qs.log(f"[{i}/{len(topics)}] {title}: GAGAL baca ({status})")
            failed += 1
            continue
        roots = tree.get("items", [])
        sections = {n["title"]: n for n in roots if n["node_type"] == "section"}
        flat_articles = [n for n in roots if n["node_type"] == "item" and n["title"] in bab]

        qs.log(f"[{i}/{len(topics)}] {title}: {len(sections)}/{len(bab)} section ada, {len(flat_articles)} artikel datar akan dihapus")
        if dry_run:
            continue

        ok = True
        # 1. one section per bab (skip the ones a previous run made)
        for judul in bab:
            if judul in sections:
                continue
            status, body = qs.api("POST", f"/modules/{tid}/items", token, {"node_type": "section", "title": judul})
            if status not in (200, 201):
                qs.log(f"    GAGAL buat section '{judul}': {status} {body}")
                ok = False
                break
            sections[judul] = {"id": body["id"], "title": judul}

        # 2. Pembahasan + Latihan inside each section
        if ok:
            status, tree = qs.api("GET", f"/modules/{tid}/items", token)
            live = {n["title"]: n for n in tree.get("items", []) if n["node_type"] == "section"}
            for judul in bab:
                node = live.get(judul)
                if not node:
                    ok = False
                    break
                have = {c["title"] for c in node.get("children", [])}
                for child_title, ctype in CHILDREN:
                    if child_title in have:
                        continue
                    status, body = qs.api(
                        "POST", f"/modules/{tid}/items", token,
                        {"node_type": "item", "title": child_title, "content_type": ctype, "parent_id": node["id"]},
                    )
                    if status not in (200, 201):
                        qs.log(f"    GAGAL buat '{child_title}' di '{judul}': {status} {body}")
                        ok = False
                        break
                if not ok:
                    break

        # 3. drop the old flat bab articles (empty shells, no content_blocks)
        if ok:
            for node in flat_articles:
                status, body = qs.api("DELETE", f"/module-items/{node['id']}", token)
                if status not in (200, 204):
                    qs.log(f"    GAGAL hapus artikel datar '{node['title']}': {status} {body}")
                    ok = False

        # 4. order the sections, then each section's own children
        if ok:
            status, tree = qs.api("GET", f"/modules/{tid}/items", token)
            live = {n["title"]: n for n in tree.get("items", []) if n["node_type"] == "section"}
            ordered = [live[j]["id"] for j in bab if j in live]
            if len(ordered) != len(bab):
                qs.log(f"    GAGAL urutkan section: {len(ordered)}/{len(bab)}")
                ok = False
            else:
                qs.api("POST", "/module-items/reorder", token, {"module_id": tid, "parent_id": None, "ordered_ids": ordered})
                for judul in bab:
                    node = live[judul]
                    by_title = {c["title"]: c["id"] for c in node.get("children", [])}
                    child_ids = [by_title[ct] for ct, _ in CHILDREN if ct in by_title]
                    if len(child_ids) == len(CHILDREN):
                        qs.api("POST", "/module-items/reorder", token,
                               {"module_id": tid, "parent_id": node["id"], "ordered_ids": child_ids})

        if ok:
            done.add(tid)
            json.dump(sorted(done), open(progress_path, "w"), indent=1)
            converted += 1
        else:
            failed += 1
        time.sleep(0.15)

    qs.log(f"=== SELESAI: {converted} dikonversi, {failed} gagal ===")

    import subprocess
    for rid in qs.report.get("cleanup", {}).get("refresh_token_ids", []):
        subprocess.run(["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun",
                        "-c", f"delete from refresh_tokens where id = '{rid}';"], capture_output=True, text=True)
    qs.log("token QA dibersihkan")


if __name__ == "__main__":
    main()
