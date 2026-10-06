#!/usr/bin/env python3
"""Penelaahan silang tanpa melihat kunci.
  buat HASIL.json                      -> tanpa_kunci_<nama>.json (soal tanpa kunci/pembahasan) untuk model penelaah
  bandingkan HASIL.json JAWABAN.json   -> membandingkan jawaban penelaah dengan kunci; exit 1 jika ada yang berbeda
JAWABAN.json: {"jawaban": {"<uid>": "B" | "Benar" | "teks isian"}}"""
import json, sys, os, re
def norm(s): return re.sub(r"\s+", " ", str(s).strip().strip(".,!?").lower())
cmd, f = sys.argv[1], sys.argv[2]
d = json.load(open(f)); base = os.path.splitext(os.path.basename(f))[0].replace("hasil_", "")
if cmd == "buat":
    out = {"lesson_plan": d["lesson_plan"], "interaktif": d.get("interaktif", []), "soal": []}
    for g in d["quiz_config"]["question_groups"]:
        for q in g["questions"]:
            item = {"uid": q["uid"], "tipe": g["type"], "bloom": q["taxonomy"]["bloom"], "kesulitan": q["taxonomy"]["difficulty"], "teks": q.get("stem") or q.get("text")}
            if g["type"] == "multiple_choice": item["pilihan"] = q["choices"]
            if g["type"] == "true_false": item["pilihan"] = ["Benar", "Salah"]
            out["soal"].append(item)
    p = os.path.join(os.path.dirname(os.path.abspath(f)), f"tanpa_kunci_{base}.json"); json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("dibuat", p, "-> beri PROMPT_PENELAAH_BAB.md + berkas ini ke model penelaah (Langkah 1), lalu berkas hasil lengkap (Langkah 2)")
else:
    ans = json.load(open(sys.argv[3]))["jawaban"]; bad = []; n = 0
    for g in d["quiz_config"]["question_groups"]:
        for q in g["questions"]:
            n += 1; got = ans.get(q["uid"]); key = q["answer"]
            ok = got is not None and (str(got).strip().upper() == key.upper() if g["type"] == "multiple_choice" else norm(got) in [norm(k) for k in key.split("|")])
            if not ok: bad.append((q["number"], g["type"], q.get("stem") or q.get("text"), key, got))
    rate = 100 * (n - len(bad)) / n
    print(f"kecocokan penelaah dengan kunci: {n - len(bad)}/{n} ({rate:.0f}%)")
    for b in bad: print(f"  ✗ no.{b[0]} [{b[1]}] {str(b[2])[:80]} | kunci={b[3]} | penelaah={b[4]}")
    print("LOLOS (100%)" if not bad else "PERIKSA: setiap ketidakcocokan harus diselesaikan (kunci salah, soal ambigu, atau jawaban penelaah salah) sebelum impor")
    sys.exit(1 if bad else 0)
