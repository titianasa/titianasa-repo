#!/usr/bin/env python3
"""Applies a Claude-authored bab structure to canonical library topics.

Per topic: delete the 4 generic placeholders (Artikel 1/2, Kuis 1/2),
then create one article item per bab, in order. Resumable — a topic
already carrying its bab list is skipped, so re-running after an
interruption costs nothing.

Usage:  python3 apply_bab.py bab_matematika_tahap1.json [--dry-run]
"""

import json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiz_sweep as qs  # reuse the proven TokenHolder + retrying api() helpers

SCRATCH = os.path.dirname(os.path.abspath(__file__))
PLACEHOLDER_TITLES = {"Artikel 1", "Artikel 2", "Kuis 1", "Kuis 2"}


def load_progress(path):
    return set(json.load(open(path))) if os.path.exists(path) else set()


def save_progress(path, done):
    with open(path, "w") as f:
        json.dump(sorted(done), f, indent=1)


def main():
    data_path = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    data = json.load(open(os.path.join(SCRATCH, data_path) if not os.path.isabs(data_path) else data_path))
    topics = data["topik"]

    progress_path = os.path.join(SCRATCH, f"progress_{os.path.basename(data_path)}")
    done = load_progress(progress_path)
    qs.log(f"=== {data['mapel']} / {data['tahap']} — {len(topics)} topik ({len(done)} sudah selesai) ===")

    token = qs.mint_user("qa-bab-dev@example.com", "curriculum_developer")

    applied = skipped = failed = 0
    for i, t in enumerate(topics, 1):
        tid, title, bab = t["topic_id"], t["topic_title"], t["bab"]
        if tid in done:
            skipped += 1
            continue

        status, tree = qs.api("GET", f"/modules/{tid}/items", token)
        if status != 200:
            qs.log(f"[{i}/{len(topics)}] {title}: GAGAL baca item ({status}) {tree}")
            failed += 1
            continue
        existing = tree.get("items", [])
        existing_titles = {n["title"] for n in existing}

        stale = [n for n in existing if n["title"] in PLACEHOLDER_TITLES]
        # Compared as a SET, never as a list: a bab already created by an
        # earlier run comes back in whatever order `order_index` happens
        # to hold (see the reorder note below), so an order mismatch here
        # must not be read as "missing" and re-created as a duplicate.
        missing = [j for j in bab if j not in existing_titles]
        if not stale and not missing:
            qs.log(f"[{i}/{len(topics)}] {title}: bab sudah ada, hanya diurutkan ulang")
        else:
            qs.log(f"[{i}/{len(topics)}] {title}: hapus {len(stale)} placeholder, buat {len(missing)} bab")
        if dry_run:
            continue

        ok = True
        for node in stale:
            status, body = qs.api("DELETE", f"/module-items/{node['id']}", token)
            if status not in (200, 204):
                qs.log(f"    GAGAL hapus {node['title']}: {status} {body}")
                ok = False
        for judul in missing:
            status, body = qs.api(
                "POST", f"/modules/{tid}/items", token,
                {"node_type": "item", "title": judul, "content_type": "article"},
            )
            if status not in (200, 201):
                qs.log(f"    GAGAL buat bab '{judul}': {status} {body}")
                ok = False
                break

        # POST /modules/{id}/items never sets order_index — it is not in
        # the insert at all, so every new item lands on 0 — while
        # get_tree sorts strictly by order_index. Without this step the
        # bab come back in arbitrary order. Reorder explicitly, by title,
        # into the order the bab list declares.
        if ok:
            status, tree = qs.api("GET", f"/modules/{tid}/items", token)
            by_title = {n["title"]: n["id"] for n in tree.get("items", [])}
            ordered_ids = [by_title[j] for j in bab if j in by_title]
            if len(ordered_ids) != len(bab):
                qs.log(f"    GAGAL urutkan: {len(ordered_ids)}/{len(bab)} bab ditemukan")
                ok = False
            else:
                status, body = qs.api(
                    "POST", "/module-items/reorder", token,
                    {"module_id": tid, "parent_id": None, "ordered_ids": ordered_ids},
                )
                if status not in (200, 204):
                    qs.log(f"    GAGAL urutkan: {status} {body}")
                    ok = False

        if ok:
            done.add(tid)
            save_progress(progress_path, done)
            applied += 1
        else:
            failed += 1
        time.sleep(0.2)

    qs.log(f"=== SELESAI: {applied} diterapkan, {skipped} dilewati, {failed} gagal ===")

    # The minted credential never outlives the run (QA-access convention).
    import subprocess
    for row_id in qs.report.get("cleanup", {}).get("refresh_token_ids", []):
        subprocess.run(
            ["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun",
             "-c", f"delete from refresh_tokens where id = '{row_id}';"],
            capture_output=True, text=True,
        )
    qs.log(f"token QA dibersihkan ({len(qs.report.get('cleanup', {}).get('refresh_token_ids', []))} baris)")


if __name__ == "__main__":
    main()
