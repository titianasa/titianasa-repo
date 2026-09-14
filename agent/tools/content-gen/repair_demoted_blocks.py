#!/usr/bin/env python3
"""Rebuild tables and step lists that were demoted to prose.

`lesson_plan::sanitize_generated` demotes any directive block the schema
rejects, and it used to demote by dumping the block's own source. A
model that pretty-printed `rows:` over several lines therefore had its
table validated as `rows == "["`, demoted, and stored — so the learner
read raw JSON on the page.

The parser now reads multi-line JSON (and `title:` on a table is
renamed rather than demoted), but content generated before that is
already prose in the database. The demotion is regular enough to undo:
the JSON survived verbatim, the header row survived as a " · " line,
and the caption as the line above it. This puts the directive back and
saves through the API, so the server validates what it gets.
"""

import json
import re
import subprocess
import sys

sys.path.insert(0, "/home/john/Dev/sanja-workspace/alr/agent/tools/content-gen")
import quiz_sweep as qs

DRY = "--apply" not in sys.argv


def psql(sql):
    out = subprocess.run(
        ["docker", "exec", "-i", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-t", "-A", "-c", sql],
        capture_output=True, text=True, check=True,
    )
    return out.stdout


def is_label(text):
    """A demoted `caption:`/`title:` line, not a sentence of the article."""
    t = text.strip()
    return 0 < len(t) <= 80 and not t.endswith((".", ":", "!", "?")) and not t.startswith(("-", "#", ">", ":::", "*"))


def rebuild(content):
    """Returns (new_content, [kinds rebuilt])."""
    paras = content.split("\n\n")
    out, fixed, i = [], [], 0
    while i < len(paras):
        if paras[i].strip() != "[":
            out.append(paras[i])
            i += 1
            continue
        # Accumulate until the run parses as JSON.
        run, j, parsed = "", i, None
        while j < len(paras) and j - i < 120:
            run = run + "\n" + paras[j]
            j += 1
            try:
                parsed = json.loads(run)
                break
            except json.JSONDecodeError:
                continue
        if parsed is None or not isinstance(parsed, list) or not parsed:
            out.append(paras[i])
            i += 1
            continue

        if all(isinstance(r, list) and all(isinstance(c, str) for c in r) for r in parsed):
            widths = {len(r) for r in parsed}
            headers = None
            if len(widths) == 1 and out and " · " in out[-1]:
                candidate = [h.strip() for h in out[-1].strip().split(" · ")]
                if len(candidate) == widths.pop():
                    headers = candidate
                    out.pop()
            if headers:
                caption = out.pop().strip() if out and is_label(out[-1]) else None
                block = [":::table"]
                if caption:
                    block.append(f"caption: {caption}")
                block.append(f"headers: {json.dumps(headers, ensure_ascii=False)}")
                block.append(f"rows: {json.dumps(parsed, ensure_ascii=False)}")
                block.append(":::")
                out.append("\n".join(block))
                fixed.append("table")
            elif (
                len(widths) == 1
                and parsed[0]
                and len(parsed[0]) == 2
                and len(out) >= 2
                and is_label(out[-1])
                and is_label(out[-2])
            ):
                # A `:::comparison` demotes to left_label, right_label,
                # then its pairs — no " · " header line to find.
                right = out.pop().strip()
                left = out.pop().strip()
                out.append(
                    "\n".join(
                        [
                            ":::comparison",
                            f"left_label: {left}",
                            f"right_label: {right}",
                            f"rows: {json.dumps(parsed, ensure_ascii=False)}",
                            ":::",
                        ]
                    )
                )
                fixed.append("comparison")
            else:
                out.append("\n".join("- " + " · ".join(r) for r in parsed))
                fixed.append("table→daftar")
        elif all(isinstance(s, str) for s in parsed):
            title = out.pop().strip() if out and is_label(out[-1]) else None
            block = [":::steps"]
            if title:
                block.append(f"title: {title}")
            block.append(f"items: {json.dumps(parsed, ensure_ascii=False)}")
            block.append(":::")
            out.append("\n".join(block))
            fixed.append("steps")
        else:
            out.append(paras[i])
            j = i + 1
        i = j
    return "\n\n".join(out), fixed


def main():
    token = qs.mint_user("qa-bab-dev@example.com", "curriculum_developer")
    rows = psql("select id, title from module_items where lesson_plan is not null order by title;")
    total = {}
    for line in rows.strip().splitlines():
        item_id, title = line.split("|", 1)
        plan = json.loads(psql(f"select lesson_plan from module_items where id='{item_id}';").strip())
        changed, kinds = False, []
        for section in plan.get("sections", []):
            new, fixed = rebuild(section.get("content", ""))
            if fixed:
                section["content"] = new
                changed = True
                kinds += fixed
        if not changed:
            continue
        for k in kinds:
            total[k] = total.get(k, 0) + 1
        print(f"{'[dry] ' if DRY else ''}{title[:52]:54} {len(kinds):2} blok: {', '.join(sorted(set(kinds)))}")
        if not DRY:
            status, body = qs.api("PATCH", f"/module-items/{item_id}/lesson-plan", token, {"lesson_plan": plan}, timeout=120)
            if status != 200:
                print(f"   GAGAL {status}: {str(body)[:300]}")
                continue
            left = psql(f"select count(*) from jsonb_array_elements((select lesson_plan from module_items where id='{item_id}')->'sections') s where s->>'content' ~ '^\\[$' or s->>'content' like '%' || chr(10) || '[' || chr(10) || '%';").strip()
            print(f"   tersimpan, sisa blok JSON mentah: {left}")
    print("\ntotal:", total or "tidak ada yang perlu diperbaiki")


main()
