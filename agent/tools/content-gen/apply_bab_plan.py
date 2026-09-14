#!/usr/bin/env python3
"""Builds every bab of a subject from a Claude-authored bab plan.

Division of labour (user decision 2026-09-14): Claude designs the bab
structure of every topic — titles, order, each bab's objective and
scope, the jenjang and standards it is written to. Gemini writes the
content later (generate_bab_content.py), and only when the user says so.

Per topic this:
  * removes the four generic placeholders (Artikel 1/2, Kuis 1/2) — only
    when they are genuinely empty, never anything with content;
  * creates, per bab, a section node holding exactly
      Pembahasan — <bab>   article, completion required before Latihan
      Latihan 1 — <bab>    draws 10 from the bank
      Latihan 2 — <bab>    draws 25 from the bank
      Latihan 3 — <bab>    the bank itself (empty groups, mix per subject)
    in that order;
  * stores the plan on the topic (modules.metadata.bab_plan) so the
    generator writes to it.

Idempotent: a bab that already exists (same title under the topic) is
left alone, and a topic whose babs are all there only gets its metadata
refreshed. Topic titles in the plan are checked against the database —
a plan keyed to the wrong topic stops instead of writing.

Plan file (bab_plans/<subject>.json):
{
  "subject": "Fisika",
  "tahap": {"Tahap 2 — Mekanika (SMA)": {"jenjang": "SMA/MA Fase E–F", "standar": ["..."], "jenis_soal": "hitungan"}},
  "default": {"bahasa": "id", "jenis_soal": "hitungan"},
  "topik": {
    "12": {"t": "Besaran Vektor & Skalar", "bab": [["Judul bab", "Tujuan satu kalimat", ["cakupan", "..."]], ...]}
  }
}
Topic keys are the 1-based position in the subject's listing
(list_topics.py), i.e. the export order.

Usage: python3 apply_bab_plan.py bab_plans/Fisika.json [--dry-run] [--only 12,13]
"""

import concurrent.futures as cf
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiz_sweep as qs
from generate_bab_content import LATIHAN, PASSING_SCORE, INSTRUCTIONS, latihan_title, pembahasan_title, psql, psql_json
import blueprint as bp

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT = "/tmp/claude-1000/-home-john-Dev-sanja-workspace-alr/9a74c488-7a92-4015-bac7-8b8bcd8f6581/scratchpad/topics/all.json"
PLACEHOLDERS = {"Artikel 1", "Artikel 2", "Kuis 1", "Kuis 2"}
JENIS = set(bp.BANK_MIXES)


def subject_topics(subject):
    rows = [r for r in json.load(open(EXPORT)) if r["subject"] == subject]
    return {str(i): r for i, r in enumerate(rows, start=1)}


def validate(plan, topics):
    errors = []
    for key, entry in plan["topik"].items():
        row = topics.get(key)
        if not row:
            errors.append(f"#{key}: tidak ada di daftar")
            continue
        if entry.get("t") and entry["t"].strip() != row["topic"].strip():
            errors.append(f"#{key}: judul plan '{entry['t']}' ≠ database '{row['topic']}'")
        babs = entry.get("bab") or []
        if not 3 <= len(babs) <= 10:
            errors.append(f"#{key} {row['topic']}: {len(babs)} bab (harus 3–10)")
        titles = [b[0].strip() for b in babs]
        if len(set(titles)) != len(titles):
            errors.append(f"#{key} {row['topic']}: judul bab kembar")
        for b in babs:
            if len(b) != 3 or not b[0].strip() or not b[1].strip() or not isinstance(b[2], list) or not b[2]:
                errors.append(f"#{key} {row['topic']}: bab tidak lengkap {b!r:.80}")
            elif len(b[0]) > 90:
                errors.append(f"#{key}: judul bab terlalu panjang: {b[0]}")
        tahap = plan.get("tahap", {}).get(row["tahap"])
        if not tahap or not tahap.get("jenjang"):
            errors.append(f"#{key}: tahap '{row['tahap']}' belum punya jenjang di plan")
        jenis = entry.get("jenis_soal") or (tahap or {}).get("jenis_soal") or plan.get("default", {}).get("jenis_soal")
        if jenis not in JENIS:
            errors.append(f"#{key}: jenis_soal '{jenis}' tidak dikenal")
    return errors


def is_empty_placeholder(item_id):
    row = psql_json(f"""select json_build_object(
        'lp', lesson_plan is not null and jsonb_array_length(coalesce(lesson_plan->'sections', '[]')) > 0,
        'qc', coalesce(jsonb_array_length(quiz_config->'question_groups'), 0) > 0,
        'blocks', (select count(*) from content_blocks where item_id = '{item_id}'),
        'attempts', (select count(*) from attempts where item_id = '{item_id}'),
        'status', status) from module_items where id = '{item_id}';""")
    return row and not row["lp"] and not row["qc"] and row["blocks"] == 0 and row["attempts"] == 0 and row["status"] == "draft"


def build_bab(token, topic_id, bab_title, order, mix, level):
    """One section with its four items, wired. Returns section id or raises."""
    def create(body):
        status, item = qs.api("POST", f"/modules/{topic_id}/items", token, body)
        if status not in (200, 201):
            raise RuntimeError(f"buat {body['title'][:40]}: {status} {str(item)[:160]}")
        return item["id"]

    section_id = create({"node_type": "section", "title": bab_title})
    article_id = create({"node_type": "item", "title": pembahasan_title(bab_title), "content_type": "article", "parent_id": section_id})
    bank_id = create({"node_type": "item", "title": latihan_title(len(LATIHAN), bab_title), "content_type": "quiz", "parent_id": section_id})
    pooled = [create({"node_type": "item", "title": latihan_title(i, bab_title), "content_type": "quiz", "parent_id": section_id}) for i in range(1, len(LATIHAN))]

    groups = [{"group_id": bp.subtype_group(st), "type": st, "instruction": INSTRUCTIONS[bp.subtype_group(st)], "questions": []} for st, _ in bp.BANK_MIXES[mix]]
    base = {"level": level, "passing_score": PASSING_SCORE, "shuffle_choices": True, "shuffle_question_order": True}
    calls = [("PATCH", f"/module-items/{bank_id}/quiz-config", {"quiz_config": {**base, "question_groups": groups}})]
    for item_id, count in zip(pooled, LATIHAN[:-1]):
        calls.append(("PATCH", f"/module-items/{item_id}/quiz-config", {"quiz_config": {**base, "question_groups": [], "question_pool": {"source_item_id": bank_id, "draw_count": count}}}))
    calls.append(("PATCH", f"/module-items/{article_id}/guards", {"guard_config": {"completion_rule": "required"}}))
    calls.append(("POST", "/module-items/reorder", {"module_id": topic_id, "parent_id": section_id, "ordered_ids": [article_id, *pooled, bank_id]}))
    for method, path, body in calls:
        status, resp = qs.api(method, path, token, body)
        if status not in (200, 201, 204):
            raise RuntimeError(f"{method} {path}: {status} {str(resp)[:160]}")
    return section_id


def apply_topic(token, plan, key, entry, row, dry):
    topic_id = row["id"]
    tahap = plan["tahap"][row["tahap"]]
    defaults = plan.get("default", {})
    mix = entry.get("jenis_soal") or tahap.get("jenis_soal") or defaults.get("jenis_soal", "hitungan")
    bahasa = entry.get("bahasa") or tahap.get("bahasa") or defaults.get("bahasa", "id")
    jenjang = entry.get("jenjang") or tahap["jenjang"]
    level = f"{row['tahap']} · jenjang {jenjang}"
    babs = [b[0].strip() for b in entry["bab"]]

    status, tree = qs.api("GET", f"/modules/{topic_id}/items", token)
    if status != 200:
        return f"#{key} GAGAL baca tree {status}"
    items = tree.get("items", [])
    existing_sections = {n["title"]: n for n in items if n["node_type"] == "section"}
    placeholders = [n for n in items if n["node_type"] == "item" and n["title"] in PLACEHOLDERS]
    missing = [b for b in babs if b not in existing_sections]
    if dry:
        return f"#{key} {row['topic'][:40]}: {len(missing)} bab baru, {len(placeholders)} placeholder, jenjang {jenjang}, {mix}"

    for ph in placeholders:
        if is_empty_placeholder(ph["id"]):
            qs.api("DELETE", f"/module-items/{ph['id']}", token, None)

    for b in missing:
        build_bab(token, topic_id, b, babs.index(b), mix, level)

    # Bab order = plan order (anything else under the topic keeps its place after).
    status, tree = qs.api("GET", f"/modules/{topic_id}/items", token)
    top = tree.get("items", [])
    by_title = {n["title"]: n["id"] for n in top if n["node_type"] == "section"}
    ordered = [by_title[b] for b in babs if b in by_title] + [n["id"] for n in top if n["id"] not in {by_title.get(b) for b in babs}]
    qs.api("POST", "/module-items/reorder", token, {"module_id": topic_id, "parent_id": None, "ordered_ids": ordered})

    meta = psql_json(f"select metadata from modules where id = '{topic_id}';") or {}
    meta["bab_plan"] = {
        "version": 1,
        "author": "claude",
        "planned_at": time.strftime("%Y-%m-%d"),
        "jenjang": jenjang,
        "bahasa": bahasa,
        "jenis_soal": mix,
        "standar": tahap.get("standar", []) + entry.get("standar", []),
        "jalur": row["paths"],
        "catatan": entry.get("catatan"),
        "bab": [{"judul": b[0].strip(), "tujuan": b[1].strip(), "cakupan": [c.strip() for c in b[2]]} for b in entry["bab"]],
    }
    status, body = qs.api("PATCH", f"/modules/{topic_id}", token, {"metadata": meta})
    if status != 200:
        return f"#{key} metadata GAGAL {status} {str(body)[:120]}"
    return f"#{key} {row['topic'][:40]}: +{len(missing)} bab"


def main():
    path = sys.argv[1]
    dry = "--dry-run" in sys.argv
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
    plan = json.load(open(os.path.join(HERE, path) if not os.path.isabs(path) else path))
    topics = subject_topics(plan["subject"])
    errors = validate(plan, topics)
    if errors:
        print(f"PLAN TIDAK VALID ({len(errors)}):")
        for e in errors[:40]:
            print("  ", e)
        sys.exit(1)
    keys = [k for k in plan["topik"] if not only or k in only]
    print(f"{plan['subject']}: {len(keys)} topik, {sum(len(plan['topik'][k]['bab']) for k in keys)} bab di plan; {len(topics)} topik di database")
    uncovered = [f"#{k} {r['topic']}" for k, r in topics.items() if k not in plan["topik"]]
    if uncovered and not only:
        print(f"  belum ada di plan: {len(uncovered)} → {', '.join(uncovered[:8])}")

    token = qs.mint_user("qa-bab-dev@example.com", "curriculum_developer")
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=1 if dry else 6) as pool:
        futures = {pool.submit(apply_topic, token, plan, k, plan["topik"][k], topics[k], dry): k for k in keys}
        for f in cf.as_completed(futures):
            try:
                print("  ", f.result(), flush=True)
            except Exception as e:  # noqa: BLE001 — report and keep going; rerun resumes
                print(f"   #{futures[f]} GAGAL: {e}", flush=True)
    print(f"selesai {time.time() - t0:.0f}s")
    for rid in qs.report.get("cleanup", {}).get("refresh_token_ids", []):
        psql(f"delete from refresh_tokens where id = '{rid}';")


if __name__ == "__main__":
    main()
