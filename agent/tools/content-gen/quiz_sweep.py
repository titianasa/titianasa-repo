#!/usr/bin/env python3
"""Full QA sweep of every quiz subtype and every quiz template:
generate real content via the real AI provider, publish, take the quiz
as a learner, and check the auto-graded key actually scores correct.
Everything is checkpointed to report.json after every single step, so
progress can be inspected (or resumed from) at any point."""

import json, os, random, sys, time, urllib.request, urllib.error

BASE = "http://localhost:8090"
SCRATCH = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRATCH, "quiz_sweep")
os.makedirs(OUT_DIR, exist_ok=True)
REPORT_PATH = os.path.join(OUT_DIR, "report.json")
LOG_PATH = os.path.join(OUT_DIR, "log.txt")
SUBJECT_ID = "6e9e3fe2-a3c7-4a8f-bb87-c092c29771e2"

class TokenHolder:
    """A long sweep easily outlives a short-TTL JWT access token — this
    holds both the access token and the raw refresh token so `api()` can
    silently re-exchange and retry on a 401, the same one-shot-refresh
    pattern titian-web's own authedRequest uses. Mutated in place, so
    every call site sharing one instance sees the refreshed token."""

    def __init__(self, access, refresh):
        self.access = access
        self.refresh = refresh


DEV_TOKEN = None
REVIEWER_TOKEN = None
STUDENT_TOKEN = None

report = {"subtypes": {}, "templates": {}, "cleanup": {"module_ids": [], "refresh_token_ids": []}}


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


def save_report():
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def _raw_request(method, path, access_token, body=None, timeout=120):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else b"{}" if method in ("POST", "PATCH", "PUT") else None
    headers = {"Content-Type": "application/json"}
    if access_token is not None:
        headers["Authorization"] = f"Bearer {access_token}"
    req = urllib.request.Request(url, method=method, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        return resp.status, (json.loads(raw) if raw else {})


def api(method, path, token, body=None, retries=6, timeout=120):
    """`token` is a TokenHolder, a bare access-token string, or None."""
    holder = token if isinstance(token, TokenHolder) else None
    already_refreshed = False
    for attempt in range(retries):
        access = holder.access if holder else token
        try:
            return _raw_request(method, path, access, body, timeout)
        except urllib.error.HTTPError as e:
            raw = e.read()
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = {"raw": raw.decode(errors="replace")}
            blob = json.dumps(parsed)
            if e.code == 401 and holder is not None and not already_refreshed:
                already_refreshed = True
                try:
                    rstatus, rbody = _raw_request("POST", "/auth/refresh", None, {"refresh_token": holder.refresh})
                    if rstatus == 200:
                        holder.access = rbody["access_token"]
                        log(f"  refreshed expired access token for {method} {path}")
                        continue
                except Exception as re:
                    log(f"  token refresh itself failed: {re}")
                return e.code, parsed
            if e.code == 429 or "RESOURCE_EXHAUSTED" in blob or "rate" in blob.lower():
                wait = min(150, (2**attempt) * 6 + random.uniform(0, 4))
                log(f"  rate-limited {method} {path} (attempt {attempt+1}/{retries}), waiting {wait:.0f}s")
                time.sleep(wait)
                continue
            return e.code, parsed
        except Exception as e:
            wait = min(60, (2**attempt) * 3)
            log(f"  transport error {method} {path}: {e} — retry in {wait}s")
            time.sleep(wait)
    return 599, {"error": "exhausted_retries"}


def psql_scalar(sql):
    """docker exec psql -t -A sometimes appends a trailing 'INSERT 0 1'
    status line after the RETURNING value even in tuples-only mode —
    only the first line is ever the real scalar."""
    import subprocess

    out = subprocess.run(["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-t", "-A", "-c", sql], capture_output=True, text=True).stdout
    first = out.strip().split("\n")[0].strip()
    if not first:
        raise RuntimeError(f"psql query returned nothing: {sql}\nstdout={out!r}")
    return first


def mint_user(email, role):
    """Resumable: if this email already exists (a prior partial run),
    reuse it and its org/role instead of crashing on a duplicate key —
    only the refresh token is always minted fresh."""
    import subprocess

    existing = subprocess.run(["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-t", "-A", "-c", f"select id from users where email = '{email}'"], capture_output=True, text=True).stdout.strip()
    if existing:
        user_id = existing.split("\n")[0].strip()
        log(f"  reusing existing user {email} ({user_id})")
    else:
        user_id = psql_scalar(f"""insert into users (google_id, email, name) values ('google-{email}', '{email}', 'QA Sweep') returning id""")
        org_id = psql_scalar(f"""insert into organizations (name, slug, type) values ('QA Org', 'qa-org-{email}', 'school') returning id""")
        psql_scalar(f"""insert into user_organization_roles (user_id, organization_id, role) values ('{user_id}', '{org_id}', '{role}') returning user_id""")

    raw = subprocess.run(["python3", "-c", "import secrets,base64;print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip('='))"], capture_output=True, text=True).stdout.strip()
    h = subprocess.run(["python3", "-c", f"import hashlib;print(hashlib.sha256({raw!r}.encode()).hexdigest())"], capture_output=True, text=True).stdout.strip()
    row_id = psql_scalar(f"""insert into refresh_tokens (user_id, token_hash, expires_at) values ('{user_id}', '{h}', now() + interval '6 hours') returning id""")
    report["cleanup"]["refresh_token_ids"].append(row_id)

    status, res = api("POST", "/auth/refresh", None, {"refresh_token": raw})
    if status != 200:
        raise RuntimeError(f"failed to mint token for {email}: {status} {res}")
    return TokenHolder(res["access_token"], raw)


def create_item(title):
    status, mod_ = api("POST", "/modules", DEV_TOKEN, {"is_folder": False, "subject_id": SUBJECT_ID, "title": title})
    if status not in (200, 201):
        raise RuntimeError(f"module create failed: {status} {mod_}")
    module_id = mod_["id"]
    report["cleanup"]["module_ids"].append(module_id)
    status, item = api("POST", f"/modules/{module_id}/items", DEV_TOKEN, {"node_type": "item", "title": title, "content_type": "quiz"})
    if status not in (200, 201):
        raise RuntimeError(f"item create failed: {status} {item}")
    return module_id, item["id"]


def value_to_key(n):
    return str(n) if not isinstance(n, str) else n


def first_valid_submission(ans):
    """An authored answer key may list several acceptable alternates as
    "a|b/c;d" (answer_match.rs's expand_answer_key splits on the same
    three separators) — a real learner only ever types ONE of them, so
    submitting the raw joined string back (as this harness first did)
    is not a valid learner input and will never match anything. Picking
    the first alternate is what a round-trip "does the key work" check
    should actually submit."""
    if isinstance(ans, str):
        for sep in ("|", "/", ";"):
            if sep in ans:
                return ans.split(sep)[0].strip()
    return ans


def publish_take_and_grade(item_id, subtypes_by_id):
    """submit-review -> publish (dev/reviewer) -> attempt -> submit each
    auto-graded question's OWN answer -> return per-question results."""
    status, sr = api("POST", f"/module-items/{item_id}/submit-review", DEV_TOKEN, {})
    if status != 200:
        return {"stage": "submit_review", "status": status, "body": sr}
    status, pub = api("POST", f"/module-items/{item_id}/publish", REVIEWER_TOKEN, {})
    if status != 200:
        return {"stage": "publish", "status": status, "body": pub}

    status, item = api("GET", f"/module-items/{item_id}", DEV_TOKEN)
    if status != 200:
        return {"stage": "reread", "status": status, "body": item}
    config = item.get("quiz_config") or {}

    status, attempt = api("POST", f"/lessons/{item_id}/attempts", STUDENT_TOKEN, {})
    if status != 201:
        return {"stage": "create_attempt", "status": status, "body": attempt}
    attempt_id = attempt["attempt_id"]

    quiz_answers = {}
    expected_correct_keys = set()
    for g in config.get("question_groups", []):
        subtype = subtypes_by_id.get(g.get("type"))
        if not subtype or subtype["grading_mode"] != "auto":
            continue
        for q in g.get("questions", []):
            key = value_to_key(q.get("number"))
            ans = q.get("answer", q.get("answers"))
            if ans is None:
                continue
            quiz_answers[key] = first_valid_submission(ans)
            expected_correct_keys.add(key)

    status, submitted = api("POST", f"/attempts/{attempt_id}/submit", STUDENT_TOKEN, {"quiz_answers": quiz_answers})
    if status != 200:
        return {"stage": "submit", "status": status, "body": submitted}

    per_question = {}
    for r in submitted.get("results", []):
        per_question[r["question_number"]] = r

    mismatches = []
    for key in expected_correct_keys:
        r = per_question.get(key)
        if r is None:
            mismatches.append({"key": key, "issue": "missing_from_results"})
        elif r.get("correct") is not True:
            mismatches.append({"key": key, "issue": "own_answer_not_scored_correct", "result": r})

    return {
        "stage": "done",
        "score": submitted.get("score"),
        "auto_questions_checked": len(expected_correct_keys),
        "mismatches": mismatches,
        "all_correct": len(mismatches) == 0,
    }


GENERIC_BRIEFS = {
    "production": "Buat satu prompt tugas produksi (esai singkat atau rekaman) bertema pengetahuan umum tingkat SMA, jelas dan spesifik, dalam Bahasa Indonesia.",
    "default": "Buat soal pengetahuan umum tingkat SMA dalam Bahasa Indonesia, topik bebas namun jelas dan faktual. Sertakan bacaan/konteks singkat bila tipe soal membutuhkannya.",
}


def sweep_subtypes():
    status, subtypes_resp = api("GET", "/quiz-subtypes", DEV_TOKEN)
    if status != 200:
        raise RuntimeError(f"failed to list subtypes: {status} {subtypes_resp}")
    subtypes = subtypes_resp["items"]
    subtypes_by_id = {s["id"]: s for s in subtypes}
    testable = [s for s in subtypes if s["shape"] != "interactive"]
    skipped = [s for s in subtypes if s["shape"] == "interactive"]
    for s in skipped:
        report["subtypes"][s["id"]] = {"family": s["family"], "grading_mode": s["grading_mode"], "skipped": "interactive_shape_not_ai_generatable"}
    save_report()

    log(f"=== SUBTYPE SWEEP: {len(testable)} generatable subtypes (skipping {len(skipped)} interactive) ===")

    meta = report.get("_subtype_sweep_meta")
    if meta and meta.get("item_id"):
        module_id, item_id = meta["module_id"], meta["item_id"]
        log(f"  resuming subtype sweep item {item_id}")
    else:
        module_id, item_id = create_item("QA Sweep - Subtypes")
        report["_subtype_sweep_meta"] = {"module_id": module_id, "item_id": item_id}
        sections = [{"section_id": "s1", "title": "Sweep"}]
        groups = [{"group_id": f"sub-{i}", "type": s["id"], "section_id": "s1", "questions": [{"number": i + 1}]} for i, s in enumerate(testable)]
        status, patched = api("PATCH", f"/module-items/{item_id}/quiz-config", DEV_TOKEN, {"quiz_config": {"sections": sections, "question_groups": groups}})
        if status != 200:
            raise RuntimeError(f"failed to seed subtype sweep config: {status} {patched}")
        save_report()

    for i, s in enumerate(testable):
        if report["subtypes"].get(s["id"], {}).get("gen_ok"):
            log(f"[{i+1}/{len(testable)}] '{s['id']}' already generated ok, skipping")
            continue
        gid = f"sub-{i}"
        brief = GENERIC_BRIEFS.get(s["family"], GENERIC_BRIEFS["default"])
        log(f"[{i+1}/{len(testable)}] generating subtype '{s['id']}' (family={s['family']}, grading={s['grading_mode']})...")
        status, res = api("POST", "/ai/generate-quiz-group", DEV_TOKEN, {"item_id": item_id, "group_id": gid, "mode": "replace", "count": 3, "context_prompt": brief}, timeout=180)
        entry = {"family": s["family"], "grading_mode": s["grading_mode"], "gen_status": status, "gen_ok": status == 200, "gen_response": res}
        report["subtypes"][s["id"]] = entry
        save_report()
        time.sleep(1.2)

    log("=== subtype sweep: publishing + taking as learner + checking auto-graded keys ===")
    grading = publish_take_and_grade(item_id, subtypes_by_id)
    report["subtypes"]["__attempt_check__"] = grading
    save_report()
    log(f"subtype sweep attempt check: {json.dumps(grading, ensure_ascii=False)[:500]}")


def sweep_templates():
    status, subtypes_resp = api("GET", "/quiz-subtypes", DEV_TOKEN)
    subtypes_by_id = {s["id"]: s for s in subtypes_resp["items"]}
    status, tmpl_resp = api("GET", "/quiz-templates", DEV_TOKEN)
    if status != 200:
        raise RuntimeError(f"failed to list templates: {status} {tmpl_resp}")
    templates = tmpl_resp["items"]
    log(f"=== TEMPLATE SWEEP: {len(templates)} templates ===")

    for ti, t in enumerate(templates):
        tid = t["id"]
        if report["templates"].get(tid, {}).get("stage") == "done":
            log(f"--- template [{ti+1}/{len(templates)}] '{tid}' already done, skipping ---")
            continue
        log(f"--- template [{ti+1}/{len(templates)}] '{tid}' ({t['name']}) ---")
        status, applied = api("POST", f"/quiz-templates/{tid}/apply", DEV_TOKEN, {})
        if status != 200:
            report["templates"][tid] = {"stage": "apply", "status": status, "body": applied}
            save_report()
            continue

        module_id, item_id = create_item(f"QA Sweep - {tid}")
        status, patched = api("PATCH", f"/module-items/{item_id}/quiz-config", DEV_TOKEN, {"quiz_config": applied})
        if status != 200:
            report["templates"][tid] = {"stage": "patch", "status": status, "body": patched}
            save_report()
            continue

        group_results = []
        for g in applied.get("question_groups", []):
            subtype = subtypes_by_id.get(g.get("type"))
            if subtype and subtype["shape"] == "interactive":
                group_results.append({"group_id": g["group_id"], "type": g["type"], "skipped": "interactive_shape_not_ai_generatable"})
                continue
            count = len(g.get("questions", [])) or 1
            log(f"  generating group '{g['group_id']}' (type={g.get('type')}, count={count})...")
            status, res = api("POST", "/ai/generate-quiz-group", DEV_TOKEN, {"item_id": item_id, "group_id": g["group_id"], "mode": "replace", "count": count}, timeout=180)
            group_results.append({"group_id": g["group_id"], "type": g.get("type"), "count": count, "gen_status": status, "gen_ok": status == 200, "gen_response": res})
            report["templates"][tid] = {"stage": "generating", "groups": group_results}
            save_report()
            time.sleep(1.2)

        log(f"  publishing + taking '{tid}' as learner...")
        grading = publish_take_and_grade(item_id, subtypes_by_id)
        report["templates"][tid] = {"stage": "done", "groups": group_results, "attempt_check": grading}
        save_report()
        log(f"  '{tid}' attempt check: score={grading.get('score')} all_correct={grading.get('all_correct')} mismatches={len(grading.get('mismatches', []) or [])}")


def cleanup():
    """Deletes the modules/items this sweep created (test content) and
    every refresh_tokens row it minted (the credential — always removed,
    per this project's QA-access convention). Deliberately does NOT
    delete the qa-sweep-*@example.com user rows themselves: they fan out
    into ~15 gamification/attempt-history tables (xp, streaks, ai_tasks,
    attempts...), several of which have nullable FKs that can also point
    at OTHER real users (graded_by/marked_by/approved_by) — safe bulk
    deletion isn't possible without real risk of touching someone else's
    data, so the synthetic accounts are left in place instead."""
    import subprocess

    log("cleanup: removing test modules/items...")
    module_ids = report.get("cleanup", {}).get("module_ids", [])
    for mid in module_ids:
        # Every sweep item got a real attempt (publish_take_and_grade)
        # and an ai_task per generation call — both reference the item
        # and must go before the item itself can be deleted.
        subprocess.run(["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-c", f"delete from attempts where item_id in (select id from module_items where module_id = '{mid}');"], capture_output=True, text=True)
        subprocess.run(["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-c", f"delete from module_items where module_id = '{mid}';"], capture_output=True, text=True)
        subprocess.run(["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-c", f"delete from modules where id = '{mid}';"], capture_output=True, text=True)
    log(f"cleanup: removed {len(module_ids)} modules")

    log("cleanup: removing minted refresh tokens...")
    row_ids = report.get("cleanup", {}).get("refresh_token_ids", [])
    for rid in row_ids:
        subprocess.run(["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-c", f"delete from refresh_tokens where id = '{rid}';"], capture_output=True, text=True)
    log(f"cleanup: removed {len(row_ids)} refresh_tokens rows")
    log("cleanup: NOT deleting qa-sweep-*@example.com user rows (see cleanup() docstring) — flag these to the user.")


def main():
    global DEV_TOKEN, REVIEWER_TOKEN, STUDENT_TOKEN, report

    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH) as f:
            loaded = json.load(f)
        report.update(loaded)
        log(f"resuming from existing report.json ({len(report.get('subtypes', {}))} subtypes, {len(report.get('templates', {}))} templates already recorded)")

    log("minting QA sweep users...")
    DEV_TOKEN = mint_user("qa-sweep-dev@example.com", "curriculum_developer")
    REVIEWER_TOKEN = mint_user("qa-sweep-reviewer@example.com", "reviewer")
    STUDENT_TOKEN = mint_user("qa-sweep-student@example.com", "student")
    save_report()
    log("users ready. starting sweeps.")

    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "subtypes"):
        sweep_subtypes()
    if which in ("all", "templates"):
        sweep_templates()

    log("=== SWEEP COMPLETE ===")
    save_report()

    if "--no-cleanup" not in sys.argv:
        cleanup()
        save_report()


if __name__ == "__main__":
    main()
