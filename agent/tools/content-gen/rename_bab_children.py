#!/usr/bin/env python3
"""Renames each bab section's children so the title carries its own
context:  "Pembahasan" -> "Pembahasan — <Judul Bab>".

Role-only names ("Pembahasan", "Latihan") only read correctly inside the
tree, where the parent is visible. In search, a flat list or any file
management view that context is gone and every topic looks identical —
185 items all called "Pembahasan". The full name also leaves room for a
second one later: "Pembahasan — <Bab> — Cara Cepat".

Idempotent: a child already carrying its bab name is left alone.
Usage:  python3 rename_bab_children.py bab_matematika_tahap1.json [--dry-run]
"""

import json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiz_sweep as qs

SCRATCH = os.path.dirname(os.path.abspath(__file__))
ROLES = ("Pembahasan", "Latihan")
SEP = " — "


def main():
    data_path = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    path = data_path if os.path.isabs(data_path) else os.path.join(SCRATCH, data_path)
    data = json.load(open(path))
    topics = data["topik"]

    qs.log(f"=== RENAME ANAK BAB: {data['mapel']} / {data['tahap']} — {len(topics)} topik ===")
    token = qs.mint_user("qa-bab-dev@example.com", "curriculum_developer")

    renamed = already = failed = 0
    for i, t in enumerate(topics, 1):
        tid, title, bab = t["topic_id"], t["topic_title"], t["bab"]
        status, tree = qs.api("GET", f"/modules/{tid}/items", token)
        if status != 200:
            qs.log(f"[{i}/{len(topics)}] {title}: GAGAL baca ({status})")
            failed += 1
            continue

        todo = []
        for node in tree.get("items", []):
            if node["node_type"] != "section":
                continue
            for child in node.get("children", []):
                for role in ROLES:
                    # Match the bare role only — a child already renamed
                    # ("Pembahasan — X") must not be renamed again into
                    # "Pembahasan — X — X" on a second run.
                    if child["title"] == role:
                        todo.append((child["id"], f"{role}{SEP}{node['title']}"))
                    elif child["title"].startswith(role + SEP):
                        already += 1

        if not todo:
            qs.log(f"[{i}/{len(topics)}] {title}: sudah bernama lengkap, dilewati")
            continue
        qs.log(f"[{i}/{len(topics)}] {title}: rename {len(todo)} anak")
        if dry_run:
            for _, new in todo[:2]:
                qs.log(f"      contoh -> {new}")
            continue

        for item_id, new_title in todo:
            status, body = qs.api("PATCH", f"/module-items/{item_id}", token, {"title": new_title})
            if status not in (200, 204):
                qs.log(f"    GAGAL rename -> '{new_title}': {status} {body}")
                failed += 1
            else:
                renamed += 1
        time.sleep(0.1)

    qs.log(f"=== SELESAI: {renamed} di-rename, {already} sudah benar, {failed} gagal ===")

    import subprocess
    for rid in qs.report.get("cleanup", {}).get("refresh_token_ids", []):
        subprocess.run(["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun",
                        "-c", f"delete from refresh_tokens where id = '{rid}';"], capture_output=True, text=True)
    qs.log("token QA dibersihkan")


if __name__ == "__main__":
    main()
