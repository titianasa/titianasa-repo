#!/usr/bin/env python3
"""Stage 2 — fills a bab with everything a learner needs:

  1. Pembahasan (Modul Belajar)  — one call, told which bab its siblings
     cover so it stays inside its own boundary.
  2. Checkpoint pools            — one call per section, written FROM
     that section, stored inside the plan (lesson_plan.sections[].checkpoint).
  3. Latihan 3 (50 soal)         — the bab's question bank, filled in
     chunks of 5 against a deterministic 50-slot blueprint.
  4. Latihan 1 & 2 (10 / 25)     — no AI at all: they draw from the bank
     per attempt (quiz_config.question_pool).
  5. Order and titles            — Pembahasan first, then the Latihan
     shortest first, numbered rather than sized in their titles.

Token discipline, which is the whole reason this is shaped the way it is:
  * The blueprint is computed in code (blueprint.py), so chunking never
    drifts from the plan and each call is told its exact slots.
  * Before every chunk the DATABASE is read and only the missing slots
    are asked for. An interrupted run resumes for free; a client timeout
    can't double-write, because the next read sees what landed.
  * A chunk that comes back truncated (MAX_TOKENS) is retried SMALLER
    (5 → 2 → 1), never as the same request that just failed.
  * Duplicates the server drops are reported back and simply re-requested
    as part of the next deficit.

Usage:
  python3 generate_bab_content.py bab_matematika_tahap1.json --topics 1
  python3 generate_bab_content.py bab_topik2_only.json --bab "bilangan cacah"
  python3 generate_bab_content.py bab_matematika_tahap1.json --all --redo-articles
"""

import json, os, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blueprint as bp
import quiz_sweep as qs

SCRATCH = os.path.dirname(os.path.abspath(__file__))
CHUNK = 5
# Latihan are numbered, not sized, in their titles: a learner picks
# "Latihan 1" and finds out how long it is when they start it, which is
# also what lets the sizes change later without renaming anything. The
# order here is the order they appear in the bab, and the LAST one owns
# the bank the others draw from.
LATIHAN = [10, 25, 50]
PASSING_SCORE = 70
INSTRUCTIONS = {
    "mc": "Pilih jawaban yang paling tepat.",
    "tf": "Tentukan benar atau salah.",
    "sa": "Jawab singkat — kerjakan sendiri.",
    "mm": "Pilih SEMUA jawaban yang benar.",
}


def latihan_title(ordinal, bab, total=len(LATIHAN)):
    """Numbering appears only once a bab has more than one Latihan —
    a lone "Latihan 3" would promise a 1 and a 2 that don't exist."""
    return f"Latihan {ordinal} — {bab}" if total > 1 else f"Latihan — {bab}"


def pembahasan_title(bab, ordinal=None, total=1):
    """One article stays "Pembahasan — X"; the numbering only appears
    once a bab has more than one, same convention as Latihan."""
    return f"Pembahasan {ordinal} — {bab}" if total > 1 and ordinal else f"Pembahasan — {bab}"


def psql(sql):
    return subprocess.run(
        ["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-t", "-A", "-c", sql],
        capture_output=True, text=True).stdout.strip()


def psql_json(sql):
    out = psql(sql)
    return json.loads(out) if out and out != "null" else None


def lesson_plan(item_id):
    return psql_json(f"select lesson_plan from module_items where id='{item_id}';")


def quiz_config(item_id):
    return psql_json(f"select quiz_config from module_items where id='{item_id}';")


def stored_slots(item_id):
    """What the bank actually holds right now, as blueprint keys."""
    config = quiz_config(item_id) or {}
    out = []
    for group in config.get("question_groups", []):
        for q in group.get("questions", []):
            tax = q.get("taxonomy") or {}
            out.append((group["group_id"], tax.get("bloom"), tax.get("difficulty"), q.get("source_section_id")))
    return out


def topic_plan(topic_id):
    """The Claude-authored bab plan stored on the topic
    (modules.metadata.bab_plan, written by apply_bab_plan.py): jenjang,
    language, question mix, standards, and each bab's objective and
    scope. None for topics planned before plans were stored."""
    meta = psql_json(f"select metadata from modules where id='{topic_id}';") or {}
    return meta.get("bab_plan")


def bab_brief(plan, bab_title):
    if not plan:
        return ""
    entry = next((b for b in plan.get("bab", []) if b.get("judul") == bab_title), None)
    lines = []
    if entry:
        if entry.get("tujuan"):
            lines.append(f"Tujuan bab: {entry['tujuan']}")
        if entry.get("cakupan"):
            lines.append("Cakupan WAJIB (semua harus diajarkan, jangan melebar di luar ini):\n" + "\n".join(f"  - {c}" for c in entry["cakupan"]))
    if plan.get("standar"):
        lines.append("Acuan standar: " + "; ".join(plan["standar"]))
    if plan.get("jalur"):
        lines.append("Topik ini dipakai di learning path: " + "; ".join(plan["jalur"]) + ". Tulis agar berguna untuk semuanya: istilah, notasi, dan tingkat kedalaman mengikuti standar di atas.")
    return "\n".join(lines)


def plan_level(plan, fallback):
    """An explicit jenjang beats the folder name: 'Tahap 2 — Mekanika'
    alone says nothing about SMA."""
    if plan and plan.get("jenjang"):
        return f"{fallback} · jenjang {plan['jenjang']}"
    return fallback


def tokens_used_since(started_at):
    value = psql(f"select coalesce(sum(tokens_used), 0) from ai_tasks where created_at >= '{started_at}';")
    return int(value or 0)


# ── 1. Modul Belajar ────────────────────────────────────────────────

def build_modul_belajar(token, item_id, bab, topic_title, level, siblings, position, brief="", language="id"):
    """The first pilot sent "Jangan membahas bab lain" without ever saying
    which bab those were, so it could not be obeyed: bab 1 "Mengenal
    Bilangan Cacah" wrote sections on reading numerals (bab 3), place
    value (bab 2) and ordering (bab 5). A boundary can only be respected
    once it is drawn."""
    others = [f"{i + 1}. {t}" for i, t in enumerate(siblings) if i != position]
    batas = (
        f"Bab ini adalah bab ke-{position + 1} dari {len(siblings)} dalam topik \"{topic_title}\".\n"
        f"Bab LAIN dalam topik ini (masing-masing ditulis terpisah — JANGAN mengajarkannya di sini):\n"
        + "\n".join(f"  {o}" for o in others)
        + "\n\nBatas materi: tulis HANYA porsi bab ini. Bila konsep milik bab lain terpaksa disinggung "
        "sebagai prasyarat, sebut satu kalimat lalu lanjut — jangan membuat bagian tersendiri untuknya."
    )
    status, body = qs.api("POST", "/ai/generate-lesson-plan", token, {
        "item_id": item_id,
        "topic": f"{bab} (bagian dari topik \"{topic_title}\")",
        "duration_minutes": 45,
        "level": level,
        "language": language,
        "notes": "Tulis sebagai modul belajar mandiri yang utuh untuk bab ini: mulai dari konsep, "
                 "contoh bertahap, kesalahan umum, lalu rangkuman.\n\n" + (brief + "\n\n" if brief else "") + batas,
    }, timeout=900)
    if status not in (200, 201):
        return status, body
    plan = body.get("lesson_plan")
    if not plan:
        return 0, {"error": "no lesson_plan in response"}
    return qs.api("PATCH", f"/module-items/{item_id}/lesson-plan", token, {"lesson_plan": plan, "ai_generated": True}, timeout=300)


# ── shared: one generate call, split smaller when truncated ─────────

def generate_slots(token, item_id, group_id, slots, context, article_id, section_id, log_prefix):
    """Returns (made, dropped, error). A truncated reply is retried with
    fewer slots instead of the same request — the model didn't fail, the
    budget did."""
    made = dropped = 0
    queue = [slots]
    while queue:
        batch = queue.pop(0)
        status, body = qs.api("POST", "/ai/generate-quiz-group", token, {
            "item_id": item_id,
            "group_id": group_id,
            "mode": "append",
            "count": len(batch),
            "slots": [{"bloom": s["bloom"], "difficulty": s["difficulty"], "section_id": s["section_id"]} for s in batch],
            "context_prompt": context,
            "reference_module_item_ids": [article_id],
            "reference_section_id": section_id,
            "mark_draft": True,
        }, timeout=900)
        if status == 200:
            # `question_count` is the group's total after the merge, not
            # how many this call added — the caller measures the delta.
            made += len(batch) - (body.get("dropped_duplicates") or 0)
            dropped += body.get("dropped_duplicates") or 0
            continue
        truncated = "MAX_TOKENS" in json.dumps(body)
        if truncated and len(batch) > 1:
            half = max(1, len(batch) // 2)
            qs.log(f"{log_prefix} terpotong pada {len(batch)} soal — dipecah jadi {half}+{len(batch) - half}")
            queue[:0] = [batch[:half], batch[half:]]
            continue
        return made, dropped, f"{status} {json.dumps(body, ensure_ascii=False)[:120]}"
    return made, dropped, None


# ── 2. Checkpoint pools ─────────────────────────────────────────────

def build_checkpoints(token, article_id, bab, level, plan, parent_id, module_id):
    """Checkpoint questions live inside the plan, and the generator only
    writes into quiz items — so they are generated into a scratch quiz
    item (one group per section), moved into the plan, and the scratch
    item is deleted."""
    def pool_size(section):
        groups = (section.get("checkpoint") or {}).get("question_groups") or [{}]
        return len(groups[0].get("questions") or [])

    # Top up a thin pool, don't just skip it: a pool of 2 with a draw of
    # 2 hands the learner the SAME two questions after a failed
    # checkpoint, which is exactly what the re-read is meant to prevent.
    sections = [s for s in plan.get("sections", []) if pool_size(s) < bp.CHECKPOINT_POOL]
    if not sections:
        return 0, None

    status, item = qs.api("POST", f"/modules/{module_id}/items", token, {
        "parent_id": parent_id, "node_type": "item", "title": f"(sementara) Checkpoint — {bab}", "content_type": "quiz",
    })
    if status not in (200, 201):
        return 0, f"gagal membuat item sementara: {status} {item}"
    scratch_id = item["id"]

    try:
        groups = [{"group_id": f"cp{i}", "type": bp.CHECKPOINT_SUBTYPE, "instruction": "Pilih jawaban yang tepat.", "questions": []} for i, _ in enumerate(sections)]
        wanted = [bp.CHECKPOINT_POOL - pool_size(section) for section in sections]
        status, body = qs.api("PATCH", f"/module-items/{scratch_id}/quiz-config", token, {"quiz_config": {"level": level, "question_groups": groups}})
        if status != 200:
            return 0, f"kerangka checkpoint gagal: {status} {body}"

        made_total = 0
        for i, section in enumerate(sections):
            slots = bp.checkpoint_blueprint(section["id"])[: wanted[i]]
            made, _, error = generate_slots(
                token, scratch_id, f"cp{i}", slots,
                f"Soal pengecekan pemahaman untuk bagian \"{section['title']}\" dari bab \"{bab}\". "
                "Uji apakah siswa memahami isi bagian ini, bukan bagian lain.",
                article_id, section["id"], f"      checkpoint {section['title'][:28]}",
            )
            made_total += made
            if error:
                return made_total, f"checkpoint bagian {i + 1} gagal: {error}"

        written = quiz_config(scratch_id) or {}
        by_group = {g["group_id"]: g for g in written.get("question_groups", [])}
        for i, section in enumerate(sections):
            group = by_group.get(f"cp{i}")
            if not group or not group.get("questions"):
                continue
            existing = ((section.get("checkpoint") or {}).get("question_groups") or [{}])[0].get("questions") or []
            merged = existing + group["questions"]
            for n, q in enumerate(merged, 1):
                q["number"] = n
            section["checkpoint"] = {"question_groups": [{"group_id": "cp", "type": group["type"], "questions": merged}]}
        status, body = qs.api("PATCH", f"/module-items/{article_id}/lesson-plan", token, {"lesson_plan": plan}, timeout=300)
        if status != 200:
            return made_total, f"gagal menyimpan checkpoint ke modul: {status} {json.dumps(body, ensure_ascii=False)[:160]}"
        return made_total, None
    finally:
        qs.api("DELETE", f"/module-items/{scratch_id}", token, None)


# ── 3-4. Bank + the two pooled Latihan ──────────────────────────────

def ensure_bank_item(token, module_id, parent_id, bab, existing_quiz_id, level, section_ids, mix="hitungan"):
    title = latihan_title(len(LATIHAN), bab)
    if existing_quiz_id:
        qs.api("PATCH", f"/module-items/{existing_quiz_id}", token, {"title": title})
        bank_id = existing_quiz_id
    else:
        status, item = qs.api("POST", f"/modules/{module_id}/items", token, {"parent_id": parent_id, "node_type": "item", "title": title, "content_type": "quiz"})
        if status not in (200, 201):
            return None, f"gagal membuat bank: {status} {item}"
        bank_id = item["id"]

    config = quiz_config(bank_id) or {}
    have = {g["group_id"] for g in config.get("question_groups", [])}
    groups = config.get("question_groups", [])
    for subtype, _ in bp.BANK_MIXES.get(mix, bp.BANK_SUBTYPES):
        gid = bp.subtype_group(subtype)
        if gid not in have:
            groups.append({"group_id": gid, "type": subtype, "instruction": INSTRUCTIONS[gid], "questions": []})
    config.update({"level": level, "question_groups": groups, "passing_score": PASSING_SCORE, "shuffle_choices": True, "shuffle_question_order": True})
    status, body = qs.api("PATCH", f"/module-items/{bank_id}/quiz-config", token, {"quiz_config": config})
    if status != 200:
        return None, f"kerangka bank gagal: {status} {json.dumps(body, ensure_ascii=False)[:160]}"
    _ = section_ids
    return bank_id, None


def ensure_pooled(token, module_id, parent_id, bab, bank_id, level, existing_pools):
    """The shorter Latihan hold no questions of their own — they draw
    from the bank on every attempt, so retaking one is a different paper
    and costs nothing to generate.

    Existing ones are recognised by the draw they are configured for,
    not by their title, so renaming never creates a duplicate."""
    made = []
    for ordinal, count in enumerate(LATIHAN[:-1], start=1):
        title = latihan_title(ordinal, bab)
        if count in existing_pools:
            made.append(existing_pools[count])
            continue
        status, item = qs.api("POST", f"/modules/{module_id}/items", token, {"parent_id": parent_id, "node_type": "item", "title": title, "content_type": "quiz"})
        if status not in (200, 201):
            return None, f"gagal membuat {title}: {status} {item}"
        made.append(item["id"])
        status, body = qs.api("PATCH", f"/module-items/{item['id']}/quiz-config", token, {"quiz_config": {
            "level": level,
            "question_groups": [],
            "passing_score": PASSING_SCORE,
            "shuffle_choices": True,
            "shuffle_question_order": True,
            "question_pool": {"source_item_id": bank_id, "draw_count": count},
        }})
        if status != 200:
            return None, f"gagal mengatur {title}: {status} {json.dumps(body, ensure_ascii=False)[:160]}"
    return made, None


def fill_bank(token, bank_id, article_id, bab, topic_title, level, section_titles, section_ids, mix="hitungan", brief=""):
    plan_slots = bp.bank_blueprint(section_ids, level, mix=mix)
    before = len(stored_slots(bank_id))
    dropped_total = 0
    # Later rounds ask for fewer questions at a time: at 7 bab the model
    # started repeating itself when asked for five more from the same
    # short section, and the duplicate filter then left the bank short.
    for attempt in range(5):
        missing = bp.deficit(plan_slots, stored_slots(bank_id))
        if not missing:
            break
        if attempt:
            qs.log(f"      putaran {attempt + 1}: {len(missing)} slot belum terisi")
        # After two rounds the remaining slots are usually ones a single
        # ~270-word section simply can't carry any more of (a fifth
        # distinct C4 question about rounding, say). Widen the reference
        # to the whole bab rather than asking the same impossible thing
        # again — the duplicate filter was throwing away every retry.
        widened = attempt >= 2
        for chunk in bp.chunks([{**m, "section_id": None} if widened else m for m in missing], CHUNK if attempt == 0 else 2):
            title = section_titles.get(chunk["section_id"], "seluruh bab")
            made, dropped, error = generate_slots(
                token, bank_id, chunk["group_id"], chunk["slots"],
                f"Soal latihan untuk bab \"{bab}\" (topik \"{topic_title}\"), bagian \"{title}\". "
                "Uji isi bagian itu, bukan materi bab lain." + (f"\n\n{brief}" if brief else ""),
                article_id, chunk["section_id"], f"      bank {chunk['group_id']}/{title[:22]}",
            )
            _ = made
            dropped_total += dropped
            if error:
                qs.log(f"      bank {chunk['group_id']} GAGAL: {error}")
    stored = stored_slots(bank_id)
    return len(stored) - before, dropped_total, len(bp.deficit(plan_slots, stored))


# ── driver ──────────────────────────────────────────────────────────

def main():
    data = json.load(open(os.path.join(SCRATCH, sys.argv[1])))
    limit = int(sys.argv[sys.argv.index("--topics") + 1]) if "--topics" in sys.argv else None
    redo_articles = "--redo-articles" in sys.argv
    only_bab = sys.argv[sys.argv.index("--bab") + 1].lower() if "--bab" in sys.argv else None
    topics = data["topik"][:limit] if limit else data["topik"]
    level = data.get("level") or data.get("tahap") or ""

    qs.log(f"=== ISI BAB: {data['mapel']} / {data['tahap']} — {len(topics)} topik ===")
    token = qs.mint_user("qa-bab-dev@example.com", "curriculum_developer")
    started_at = psql("select now();")
    t_start = time.time()
    art_ok = art_skip = art_fail = cp_ok = bank_ok = bank_short = 0

    for ti, t in enumerate(topics, 1):
        tid, ttitle = t["topic_id"], t["topic_title"]
        status, tree = qs.api("GET", f"/modules/{tid}/items", token)
        if status != 200:
            qs.log(f"[{ti}] {ttitle}: GAGAL baca tree ({status})")
            continue
        sections = [n for n in tree.get("items", []) if n["node_type"] == "section"]
        tplan = topic_plan(tid)
        tlevel = plan_level(tplan, t.get("level") or level)
        language = (tplan or {}).get("bahasa", "id")
        mix = (tplan or {}).get("jenis_soal", "hitungan")
        qs.log(f"[{ti}/{len(topics)}] {ttitle} — {len(sections)} bab · {tlevel} · {mix}")

        for si, sec in enumerate(sections, 1):
            bab = sec["title"]
            if only_bab and only_bab not in bab.lower():
                continue
            kids = sec.get("children", [])
            artikel = next((k for k in kids if k["content_type"] == "article"), None)
            if not artikel:
                qs.log(f"   [{si}] {bab[:45]}: tidak ada item Pembahasan, dilewati")
                continue
            # Which quiz is which is read from the configs, never from
            # the titles — the titles have been renamed twice already.
            existing_quiz, existing_pools = None, {}
            for k in (k for k in kids if k["content_type"] == "quiz"):
                config = quiz_config(k["id"]) or {}
                pool = config.get("question_pool") or {}
                if pool.get("draw_count"):
                    existing_pools[pool["draw_count"]] = k["id"]
                elif config.get("question_groups") or "Latihan" in k["title"]:
                    existing_quiz = existing_quiz or k
            qs.log(f"   [{si}] {bab[:45]}")

            # 1. artikel
            plan = lesson_plan(artikel["id"])
            if plan and plan.get("sections") and not redo_articles:
                art_skip += 1
            else:
                t0 = time.time()
                status, body = build_modul_belajar(token, artikel["id"], bab, ttitle, tlevel, [s["title"] for s in sections], si - 1, bab_brief(tplan, bab), language)
                if status not in (200, 201):
                    qs.log(f"      MODUL GAGAL {status} {json.dumps(body, ensure_ascii=False)[:160]}")
                    art_fail += 1
                    continue
                plan = lesson_plan(artikel["id"])
                art_ok += 1
                qs.log(f"      modul belajar {len(plan.get('sections', []))} bagian ({time.time() - t0:.0f}s)")

            section_ids = [s["id"] for s in plan.get("sections", [])]
            section_titles = {s["id"]: s.get("title", "") for s in plan.get("sections", [])}

            # 2. checkpoint per bagian
            t0 = time.time()
            made, error = build_checkpoints(token, artikel["id"], bab, tlevel, plan, sec["id"], tid)
            if error:
                qs.log(f"      CHECKPOINT GAGAL: {error}")
            elif made:
                cp_ok += 1
                qs.log(f"      checkpoint {made} soal untuk {len(section_ids)} bagian ({time.time() - t0:.0f}s)")

            # an article with checkpoints must be finished before its Latihan opens
            qs.api("PATCH", f"/module-items/{artikel['id']}/guards", token, {"guard_config": {"completion_rule": "required"}})

            # 3. bank + 4. pooled variants
            bank_id, error = ensure_bank_item(token, tid, sec["id"], bab, existing_quiz["id"] if existing_quiz else None, tlevel, section_ids, mix)
            if error:
                qs.log(f"      {error}")
                continue
            t0 = time.time()
            made, dropped, short = fill_bank(token, bank_id, artikel["id"], bab, ttitle, tlevel, section_titles, section_ids, mix, bab_brief(tplan, bab))
            suffix = f", {dropped} duplikat dibuang" if dropped else ""
            if short:
                bank_short += 1
                qs.log(f"      bank {made} soal baru{suffix} — {short} slot MASIH KOSONG ({time.time() - t0:.0f}s)")
            else:
                bank_ok += 1
                qs.log(f"      bank lengkap {bp.BANK_SIZE} soal (+{made} baru{suffix}, {time.time() - t0:.0f}s)")
            pooled_ids, error = ensure_pooled(token, tid, sec["id"], bab, bank_id, tlevel, existing_pools)
            if error:
                qs.log(f"      {error}")
                pooled_ids = []

            # 5. one fixed order per bab: Pembahasan, then the Latihan
            # shortest first. Created order is not that order (the bank
            # has to exist before the ones that draw from it), so it is
            # set explicitly rather than left to whenever each was made.
            articles = [k for k in kids if k["content_type"] == "article"]
            for n, art in enumerate(articles, start=1):
                want = pembahasan_title(bab, n, len(articles))
                if art["title"] != want:
                    qs.api("PATCH", f"/module-items/{art['id']}", token, {"title": want})
            ordered = [a["id"] for a in articles] + pooled_ids + [bank_id]
            leftover = [k["id"] for k in kids if k["id"] not in ordered]
            status, _ = qs.api("POST", "/module-items/reorder", token,
                               {"module_id": tid, "parent_id": sec["id"], "ordered_ids": ordered + leftover})
            if status not in (200, 204):
                qs.log(f"      urutan gagal disimpan ({status})")

    dur = time.time() - t_start
    tokens = tokens_used_since(started_at)
    qs.log(f"=== SELESAI dalam {dur / 60:.1f} menit ===")
    qs.log(f"    modul belajar: {art_ok} dibuat, {art_skip} dilewati, {art_fail} gagal")
    qs.log(f"    checkpoint   : {cp_ok} bab")
    qs.log(f"    bank soal    : {bank_ok} lengkap, {bank_short} belum lengkap")
    qs.log(f"    token        : {tokens:,} total" + (f" (~{tokens // max(1, art_ok + cp_ok + bank_ok):,} per bab)" if art_ok + cp_ok + bank_ok else ""))

    for rid in qs.report.get("cleanup", {}).get("refresh_token_ids", []):
        subprocess.run(["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun",
                        "-c", f"delete from refresh_tokens where id = '{rid}';"], capture_output=True, text=True)
    qs.log("token QA dibersihkan")


if __name__ == "__main__":
    main()
