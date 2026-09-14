#!/usr/bin/env python3
"""Rename and reorder the items inside every bab.

Titles number the Latihan instead of sizing them ("Latihan 1 — <bab>",
not "Latihan 10 soal — <bab>"): the size is a property of the paper the
server draws, and printing it in the title makes every future change to
a draw count a rename. A bab's order is fixed — Pembahasan, then the
Latihan shortest first — and set explicitly, because the order they
were created in is the order the generator needed (the bank has to
exist before the items that draw from it), not the order a learner
should meet them in.

Which quiz is which is read from `quiz_config`, never from the title.
"""

import json
import subprocess
import sys

sys.path.insert(0, "/home/john/Dev/sanja-workspace/alr/agent/tools/content-gen")
import quiz_sweep as qs
from generate_bab_content import LATIHAN, latihan_title, pembahasan_title, quiz_config

DRY = "--apply" not in sys.argv


def psql(sql):
    return subprocess.run(
        ["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-t", "-A", "-F", "|", "-c", sql],
        capture_output=True, text=True).stdout.strip()


def main():
    token = qs.mint_user("qa-bab-dev@example.com", "curriculum_developer")
    rows = psql("""
        select distinct m.id, m.title from modules m
        join module_items mi on mi.module_id = m.id
        where mi.content_type = 'quiz' order by 2;""")
    renamed = reordered = 0
    for line in rows.splitlines():
        module_id, module_title = line.split("|", 1)
        status, tree = qs.api("GET", f"/modules/{module_id}/items", token)
        if status != 200:
            print(f"{module_title}: gagal baca tree ({status})")
            continue
        for sec in (n for n in tree.get("items", []) if n["node_type"] == "section"):
            kids = sec.get("children", [])
            articles = [k for k in kids if k["content_type"] == "article"]
            pools, bank = {}, None
            for k in (k for k in kids if k["content_type"] == "quiz"):
                config = quiz_config(k["id"]) or {}
                pool = config.get("question_pool") or {}
                if pool.get("draw_count"):
                    pools[pool["draw_count"]] = k
                elif config.get("question_groups"):
                    bank = k
            if not bank and not pools:
                continue
            bab = sec["title"]

            total_latihan = len(pools) + (1 if bank else 0)
            wanted = {}
            for n, art in enumerate(articles, start=1):
                wanted[art["id"]] = pembahasan_title(bab, n, len(articles))
            for ordinal, count in enumerate(LATIHAN[:-1], start=1):
                if count in pools:
                    wanted[pools[count]["id"]] = latihan_title(ordinal, bab, total_latihan)
            if bank:
                wanted[bank["id"]] = latihan_title(total_latihan, bab, total_latihan)

            ordered = [a["id"] for a in articles]
            ordered += [pools[c]["id"] for c in LATIHAN[:-1] if c in pools]
            if bank:
                ordered.append(bank["id"])
            ordered += [k["id"] for k in kids if k["id"] not in ordered]

            for k in kids:
                want = wanted.get(k["id"])
                if want and want != k["title"]:
                    print(f"{'[dry] ' if DRY else ''}  {k['title'][:46]:48} -> {want[:46]}")
                    renamed += 1
                    if not DRY:
                        st, body = qs.api("PATCH", f"/module-items/{k['id']}", token, {"title": want})
                        if st != 200:
                            print(f"      GAGAL rename {st}: {str(body)[:160]}")
            # Always sent: items created in one batch can share an
            # order_index, so a tree that already reads in the right
            # order is not proof the stored order is right.
            if True:
                reordered += 1
                if not DRY:
                    st, body = qs.api("POST", "/module-items/reorder", token,
                                      {"module_id": module_id, "parent_id": sec["id"], "ordered_ids": ordered})
                    if st not in (200, 204):
                        print(f"      GAGAL urutan {st}: {str(body)[:160]}")
    print(f"\n{'[dry] ' if DRY else ''}{renamed} judul, {reordered} bab diurut ulang")


main()
