#!/usr/bin/env python3
"""Mengubah bank soal skema ringkas (t/key/answer per pilihan/uid q01) menjadi skema aplikasi
(group type, choices label+text, answer huruf, uid unik, number berurutan), lalu menyegarkan bab_bank_stats."""
import re, glob, json, uuid, subprocess, sys
def psql(sql, inp=None):
    r = subprocess.run(["docker","exec","-i","titian-bun-postgres","psql","-U","titian","titian_bun","-At","-v","ON_ERROR_STOP=1"] + (["-c", sql] if inp is None else []), input=inp, text=True, capture_output=True)
    if r.returncode: print(r.stderr[:500]); sys.exit(1)
    return r.stdout.strip()
INSTR = {"multiple_choice": "Pilih jawaban yang paling tepat.", "true_false": "Tentukan benar atau salah.", "short_answer": "Jawab singkat dengan satu angka atau satu kata."}
def convert(qc, sections):
    if qc.get("question_groups") and "type" in qc["question_groups"][0]: return None  # sudah skema aplikasi
    out = []; n = 0
    for g in qc["question_groups"]:
        typ = g.get("subtype") or g.get("type"); qs = []
        for q in g["questions"]:
            n += 1; ch = q.get("choices", []); good = [c for c in ch if c.get("answer")]
            expl = " ".join(c.get("explanation", "") for c in good).strip()
            if typ == "multiple_choice":
                opts = [{"label": c["key"], "text": c["text"]} for c in ch]
                ans = good[0]["key"]
                bad = [f"Pengecoh {c['key']}: {c['explanation']}" for c in ch if not c.get("answer") and c.get("explanation")]
                base = {"stem": q["stem"], "choices": opts, "answer": ans, "explanation": (expl + " " + " ".join(bad)).strip()}
            elif typ == "true_false":
                base = {"text": q["stem"], "answer": good[0]["text"], "explanation": expl}
            else:
                base = {"stem": q["stem"], "answer": "|".join(c["text"] for c in good), "explanation": expl}
            qs.append({"uid": str(uuid.uuid4()), **base, "number": n, "taxonomy": q["taxonomy"], "source_section_id": q.get("source_section_id")})
        grp = {"type": typ, "group_id": g["group_id"], "instruction": INSTR[typ], "questions": qs, "ai_meta": {"draft": True}}
        if typ == "true_false": grp["options"] = ["Benar", "Salah"]
        out.append(grp)
    return {"level": qc.get("level", ""), "sections": [{"title": s["title"], "section_id": s["id"]} for s in sections], "passing_score": 70.0, "shuffle_choices": True, "shuffle_question_order": True, "question_groups": out}
done = 0
for f in sorted(glob.glob("bab*_*.py")):
    h = open(f).read(3000); ids = [re.search(k + r": ([0-9a-f-]{36})", h) for k in ("bab_id", "article_id", "quiz_id")]
    if not all(ids): continue
    bab, art, quiz = [i.group(1) for i in ids]
    qc = json.loads(psql(f"select quiz_config::text from module_items where id='{quiz}'")); lp = json.loads(psql(f"select lesson_plan::text from module_items where id='{art}'"))
    new = convert(qc, lp["sections"])
    if new is None: continue
    new["level"] = lp.get("level", "")
    psql("begin;\nupdate module_items set quiz_config=$q$" + json.dumps(new, ensure_ascii=False) + f"$q$::jsonb where id='{quiz}';\ncommit;", inp=None) if False else subprocess.run(["docker","exec","-i","titian-bun-postgres","psql","-U","titian","titian_bun","-q","-v","ON_ERROR_STOP=1"], input=f"update module_items set quiz_config=$q${json.dumps(new, ensure_ascii=False)}$q$::jsonb where id='{quiz}';", text=True, check=True)
    done += 1
print("dikonversi", done)
