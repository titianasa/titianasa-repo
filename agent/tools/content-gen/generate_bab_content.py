#!/usr/bin/env python3
"""Stage 2 — fills each bab's Pembahasan (Modul Belajar) and Latihan (quiz).

Per bab, in this order:
  1. Modul Belajar -> POST /ai/generate-lesson-plan (does NOT persist),
     then PATCH /module-items/{id}/lesson-plan with ai_generated=true.
     The article is a sectioned Modul Belajar FROM THE START — no
     flat-article-then-convert step. The PATCH also re-projects the plan
     into content_blocks, so the reading view is filled by the same call.
  2. quiz -> PATCH a one-group quiz_config skeleton onto Latihan, then
     POST /ai/generate-quiz-group referencing the article written in
     step 1, so the questions test that bab's own material instead of
     inventing unrelated ones. Every question comes back carrying its
     taxonomy (tingkat kesukaran + Bloom C1-C6).

Resumable: a bab whose article already has a lesson_plan (and whose quiz
already has questions) is skipped, so an interrupted run costs nothing
to resume. Pass --redo-articles to rewrite articles that currently hold
only flat content_blocks from the old pipeline, and --redo-quizzes to
regenerate quizzes written before questions carried a taxonomy. A redo
goes through the same API as a first run (mode=replace), so nothing is
deleted behind the server's back.

Usage:
  python3 generate_bab_content.py bab_matematika_tahap1.json --topics 1
  python3 generate_bab_content.py bab_matematika_tahap1.json --all
"""

import json, os, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiz_sweep as qs

SCRATCH = os.path.dirname(os.path.abspath(__file__))
QUIZ_SUBTYPE = "multiple_choice"
QUIZ_COUNT = 5


def psql(sql):
    return subprocess.run(
        ["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-t", "-A", "-c", sql],
        capture_output=True, text=True).stdout.strip()


def plan_section_count(item_id):
    """0 = no Modul Belajar yet. Counts sections, not blocks: an item
    left over from the old flat-article pipeline has content_blocks but
    no lesson_plan, and must be rewritten rather than skipped."""
    out = psql(f"select coalesce(jsonb_array_length(lesson_plan->'sections'), 0) from module_items where id='{item_id}';")
    return int(out.splitlines()[0] or 0) if out else 0


def quiz_question_count(item_id):
    out = psql(f"select coalesce(jsonb_array_length(quiz_config->'question_groups'), 0) from module_items where id='{item_id}';")
    if out in ("", "0"):
        return 0
    q = psql(f"""select coalesce(sum(jsonb_array_length(g->'questions')), 0)
                 from module_items, jsonb_array_elements(quiz_config->'question_groups') g
                 where id='{item_id}';""")
    return int(q.splitlines()[0] or 0) if q else 0


def build_modul_belajar(token, item_id, bab, topic_title, level):
    """Two steps, because generation deliberately does not persist — the
    server hands the plan back for review and the caller decides to keep
    it. `ai_generated` on the save is what stamps generated_by='ai'."""
    status, body = qs.api("POST", "/ai/generate-lesson-plan", token, {
        "item_id": item_id,
        "topic": f"{bab} (bagian dari topik \"{topic_title}\")",
        "duration_minutes": 45,
        "level": level,
        "language": "id",
        "notes": "Tulis sebagai modul belajar mandiri yang utuh untuk bab ini: mulai dari konsep, "
                 "contoh bertahap, kesalahan umum, lalu rangkuman. Jangan membahas bab lain.",
    }, timeout=900)
    if status not in (200, 201):
        return status, body

    plan = body.get("lesson_plan")
    if not plan:
        return 0, {"error": "no lesson_plan in response"}
    return qs.api("PATCH", f"/module-items/{item_id}/lesson-plan", token, {
        "lesson_plan": plan,
        "ai_generated": True,
    }, timeout=300)


def main():
    data = json.load(open(os.path.join(SCRATCH, sys.argv[1])))
    limit = None
    if "--topics" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--topics") + 1])
    redo_articles = "--redo-articles" in sys.argv
    redo_quizzes = "--redo-quizzes" in sys.argv
    # --bab <substring>: touch only the bab whose title contains it, so a
    # single bad bab can be redone without rewriting its good siblings.
    only_bab = sys.argv[sys.argv.index("--bab") + 1].lower() if "--bab" in sys.argv else None
    topics = data["topik"][:limit] if limit else data["topik"]
    level = data.get("level") or data.get("tahap") or ""

    qs.log(f"=== ISI BAB: {data['mapel']} / {data['tahap']} — {len(topics)} topik ===")
    token = qs.mint_user("qa-bab-dev@example.com", "curriculum_developer")

    art_ok = art_skip = art_fail = quiz_ok = quiz_skip = quiz_fail = 0
    t_start = time.time()

    for ti, t in enumerate(topics, 1):
        tid, ttitle = t["topic_id"], t["topic_title"]
        status, tree = qs.api("GET", f"/modules/{tid}/items", token)
        if status != 200:
            qs.log(f"[{ti}] {ttitle}: GAGAL baca tree ({status})")
            continue
        sections = [n for n in tree.get("items", []) if n["node_type"] == "section"]
        qs.log(f"[{ti}/{len(topics)}] {ttitle} — {len(sections)} bab")

        for si, sec in enumerate(sections, 1):
            bab = sec["title"]
            if only_bab and only_bab not in bab.lower():
                continue
            kids = sec.get("children", [])
            artikel = next((k for k in kids if k["content_type"] == "article"), None)
            kuis = next((k for k in kids if k["content_type"] == "quiz"), None)
            if not artikel or not kuis:
                qs.log(f"   [{si}] {bab[:45]}: struktur tidak lengkap, dilewati")
                continue

            # ── 1. modul belajar ──
            if plan_section_count(artikel["id"]) > 0 and not redo_articles:
                art_skip += 1
            else:
                t0 = time.time()
                status, body = build_modul_belajar(token, artikel["id"], bab, ttitle, level)
                if status in (200, 201):
                    n = plan_section_count(artikel["id"])
                    qs.log(f"   [{si}] {bab[:45]}: modul belajar {n} bagian ({time.time()-t0:.0f}s)")
                    art_ok += 1
                else:
                    qs.log(f"   [{si}] {bab[:45]}: MODUL GAGAL {status} {json.dumps(body, ensure_ascii=False)[:160]}")
                    art_fail += 1
                    continue

            # ── 2. kuis latihan, dibuat DARI modul bab ini ──
            if quiz_question_count(kuis["id"]) > 0 and not redo_quizzes:
                quiz_skip += 1
                continue
            status, body = qs.api("PATCH", f"/module-items/{kuis['id']}/quiz-config", token, {"quiz_config": {
                # The jenjang the Bloom/difficulty target spread is
                # computed from — without it every paper gets the
                # middle-of-the-road profile regardless of Tahap.
                "level": level,
                "sections": [{"section_id": "s1", "title": bab}],
                "question_groups": [{
                    "group_id": "g1", "type": QUIZ_SUBTYPE, "section_id": "s1",
                    "instruction": "Pilih jawaban yang paling tepat.",
                    "questions": [],
                }],
            }})
            if status != 200:
                qs.log(f"   [{si}] {bab[:45]}: KERANGKA KUIS GAGAL {status} {body}")
                quiz_fail += 1
                continue

            t0 = time.time()
            status, body = qs.api("POST", "/ai/generate-quiz-group", token, {
                "item_id": kuis["id"], "group_id": "g1", "mode": "replace", "count": QUIZ_COUNT,
                "context_prompt": f"Uji pemahaman materi bab \"{bab}\" dari topik \"{ttitle}\". "
                                  f"Soal harus menguji isi modul rujukan, bukan materi di luar bab ini.",
                "reference_module_item_ids": [artikel["id"]],
                "mark_draft": True,
            }, timeout=900)
            if status == 200:
                qs.log(f"   [{si}] {bab[:45]}: kuis {body.get('question_count')} soal ({time.time()-t0:.0f}s)")
                quiz_ok += 1
            else:
                qs.log(f"   [{si}] {bab[:45]}: KUIS GAGAL {status} {json.dumps(body, ensure_ascii=False)[:160]}")
                quiz_fail += 1

    dur = time.time() - t_start
    qs.log(f"=== SELESAI dalam {dur/60:.1f} menit ===")
    qs.log(f"    modul belajar: {art_ok} dibuat, {art_skip} dilewati, {art_fail} gagal")
    qs.log(f"    kuis         : {quiz_ok} dibuat, {quiz_skip} dilewati, {quiz_fail} gagal")
    if art_ok + quiz_ok:
        qs.log(f"    rata-rata {dur/(art_ok+quiz_ok):.0f} detik per item AI")

    for rid in qs.report.get("cleanup", {}).get("refresh_token_ids", []):
        subprocess.run(["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun",
                        "-c", f"delete from refresh_tokens where id = '{rid}';"], capture_output=True, text=True)
    qs.log("token QA dibersihkan")


if __name__ == "__main__":
    main()
