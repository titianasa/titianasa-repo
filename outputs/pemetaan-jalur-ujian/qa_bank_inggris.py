#!/usr/bin/env python3
"""QA otomatis + seleksi bank tahap 1 untuk unit Bahasa Inggris (registry_inggris_v1.csv).
Tanpa LLM, tanpa biaya token. Membaca soal lama dari DB dev (docker exec psql), memeriksanya, lalu memilih 20 soal per unit
sesuai komposisi tahap 1 (PEMETAAN_KANONIK_JALUR_UJIAN_V1 bagian 10.1). Keluaran (di folder ini):
  qa_unit_inggris_v1.csv        ringkasan per unit
  qa_temuan_inggris_v1.csv      satu baris per temuan (soal, tingkat, alasan)
  seleksi_tahap1_inggris_v1.csv soal terpilih + fungsi usulan
Pemeriksaan di sini hanya struktural dan tag. Konsistensi kunci vs pembahasan (semantik) TIDAK diperiksa: heuristik teks terbukti bising (lihat dokumen bagian 16) dan perlu LLM/manusia."""
import csv, json, re, os, subprocess, collections, sys

D = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("EN_SOAL_JSONL", "/tmp/en_soal.jsonl")
STOP = set("the a an of to in on at for and or is are was were be been it this that with as by from your you not no yes i we they he she his her their our its do does did have has had can could will would".split())


def export():
    ids = [r["sumber_topik_id"] for r in csv.DictReader(open(f"{D}/registry_inggris_v1.csv"))]
    q = ("select json_build_object('topik_id', b.module_id, 'bab_id', b.id, 'bab', b.title, 'quiz_id', q.id, 'gtype', g->>'type', 'q', x)::text "
         "from module_items q join module_items b on b.id=q.parent_id join ids on ids.id=b.module_id, "
         "jsonb_array_elements(coalesce(q.quiz_config->'question_groups','[]'::jsonb)) g, jsonb_array_elements(g->'questions') x "
         "where q.content_type='quiz' and q.quiz_config->'question_pool' is null;")
    sql = "create temp table ids(id uuid);\ninsert into ids values " + ",".join(f"('{i}')" for i in ids) + ";\n" + q + "\n"
    out = subprocess.run(["docker", "exec", "-i", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-At"], input=sql, capture_output=True, text=True, check=True).stdout
    with open(CACHE, "w") as f:
        for line in out.splitlines():
            if line.startswith("{"): f.write(line + "\n")


def toks(s):
    return [w for w in re.findall(r"[a-z0-9']+", (s or "").lower()) if w not in STOP and len(w) > 1]


def norm(s):
    return " ".join(re.findall(r"[a-z0-9]+", (s or "").lower()))


def jacc(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a and b else 0.0


def stem_of(q): return q.get("stem") or q.get("text") or ""


def check(item):
    """-> list of (severity, kode, detail). severity: KRITIS (soal tidak boleh dipakai), MAYOR (perlu tinjau), MINOR (informasi)"""
    q, t = item["q"], item["gtype"]; f = []
    stem = stem_of(q); ans = q.get("answer"); tax = q.get("taxonomy") or {}
    if not stem.strip(): f.append(("KRITIS", "STEM-KOSONG", ""))
    if ans in (None, ""): f.append(("KRITIS", "KUNCI-HILANG", ""))
    if not (q.get("explanation") or "").strip(): f.append(("MAYOR", "PEMBAHASAN-HILANG", ""))
    if not tax.get("bloom") or not tax.get("difficulty"): f.append(("MAYOR", "TAG-BLOOM-KESULITAN-HILANG", ""))
    if "source_section_id" not in q: f.append(("MINOR", "BAGIAN-ASAL-HILANG", ""))
    if t == "multiple_choice":
        ch = q.get("choices") or []
        labels = [c.get("label") for c in ch]; texts = [(c.get("text") or "").strip() for c in ch]
        if len(ch) < 3 or len(ch) > 5: f.append(("KRITIS", "JUMLAH-PILIHAN", str(len(ch))))
        elif len(ch) != 4: f.append(("MINOR", "PILIHAN-BUKAN-4", str(len(ch))))
        fix = "REPARABEL: hapus opsi ke-5" if len(ch) == 5 and (not texts[-1] or texts[-1] == texts[-2]) and ans in labels[:4] else ""
        if len(set(labels)) != len(labels): f.append(("KRITIS", "LABEL-GANDA", fix))
        if len(set(texts)) != len(texts): f.append(("KRITIS", "PILIHAN-KEMBAR", fix))
        if any(not x for x in texts): f.append(("KRITIS", "PILIHAN-KOSONG", fix))
        if ans not in (None, "") and ans not in labels: f.append(("KRITIS", "KUNCI-BUKAN-LABEL", str(ans)))
    elif t == "true_false":
        if ans not in ("Benar", "Salah") and ans not in (None, ""): f.append(("KRITIS", "KUNCI-TF-ANEH", str(ans)))
        first = re.split(r"(?<=[.!?])\s", (q.get("explanation") or "").strip(), maxsplit=1)[0].lower()[:120]
        first = first.replace("salah satu", "")
        if ans == "Benar" and re.match(r"^(pernyataan|kalimat|klaim)\s+(ini|tersebut|itu)?\s*(adalah\s+)?(salah|keliru|tidak benar|tidak tepat)\b", first): f.append(("MAYOR", "PEMBAHASAN-BERTENTANGAN-TF", "kunci Benar, kalimat pertama pembahasan menyatakan salah"))
        if ans == "Salah" and re.match(r"^(pernyataan|kalimat|klaim)\s+(ini|tersebut|itu)?\s*(adalah\s+)?(benar|tepat)\b", first): f.append(("MAYOR", "PEMBAHASAN-BERTENTANGAN-TF", "kunci Salah, kalimat pertama pembahasan menyatakan benar"))
    elif t == "short_answer":
        if ans not in (None, ""):
            if len(str(ans)) > 80: f.append(("MINOR", "KUNCI-ISIAN-PANJANG", str(len(str(ans)))))
    return f


def main():
    if "--export" in sys.argv or not os.path.exists(CACHE): export()
    items = [json.loads(l) for l in open(CACHE)]
    reg = {r["sumber_topik_id"]: r for r in csv.DictReader(open(f"{D}/registry_inggris_v1.csv"))}
    by_unit = collections.defaultdict(list)
    for it in items: by_unit[it["topik_id"]].append(it)

    findings, unit_rows, selection = [], [], []
    global_stem = collections.defaultdict(list)
    for tid, its in by_unit.items():
        for it in its: global_stem[norm(stem_of(it["q"]))].append((tid, it["q"]["uid"]))
    for tid, its in by_unit.items():
        for it in its:
            it["flags"] = check(it); it["tk"] = toks(stem_of(it["q"])); it["key"] = str(it["q"].get("answer"))
        # duplikat dalam unit
        for i in range(len(its)):
            for j in range(i):
                if any(k[1] == "DUPLIKAT" for k in its[i]["flags"]): break
                a, b = its[i], its[j]
                s = jacc(a["tk"], b["tk"])
                if norm(stem_of(a["q"])) == norm(stem_of(b["q"])) or (s >= 0.9 and a["key"] == b["key"]): a["flags"].append(("KRITIS", "DUPLIKAT", f"sama dengan {b['q']['uid'][:8]}")); break
                if s >= 0.9 and a["key"] != b["key"]: a["flags"].append(("MAYOR", "MIRIP-KUNCI-BEDA", f"mirip {b['q']['uid'][:8]}"))
        for it in its:
            q = it["q"]
            if len({u for u, _ in global_stem[norm(stem_of(q))]}) > 1: it["flags"].append(("MINOR", "DUPLIKAT-LINTAS-UNIT", "stem sama di unit lain"))
            for sev, kode, det in it["flags"]:
                findings.append({"module_id": reg[tid]["module_id"], "uid": q["uid"], "tipe": it["gtype"], "tingkat": sev, "kode": kode, "detail": det, "stem": stem_of(q)[:110]})
        good = [it for it in its if not any(f[0] == "KRITIS" for f in it["flags"])]

        # pilih 20 soal tahap 1
        Q = {"mudah": 6, "sedang": 10, "sulit": 4}; BL = {"c1": 2, "c2": 3, "c3": 6, "c4": 5, "c5": 2}; TYPE = {"multiple_choice": 10, "true_false": 4, "short_answer": 6}
        chosen, used_bab = [], collections.Counter()
        def ok(c): return not any(jacc(c["tk"], x["tk"]) > 0.6 for x in chosen)
        def score(c):
            tx = c["q"].get("taxonomy") or {}
            d, b, t = tx.get("difficulty"), tx.get("bloom"), c["gtype"]
            s = 0
            s += 3 if sum(1 for x in chosen if (x["q"].get("taxonomy") or {}).get("difficulty") == d) < Q.get(d, 0) else 0
            s += 2 if sum(1 for x in chosen if (x["q"].get("taxonomy") or {}).get("bloom") == b) < BL.get(b, 0) else 0
            s += 1 if sum(1 for x in chosen if x["gtype"] == t) < TYPE.get(t, 0) else 0
            s -= used_bab[c["bab_id"]] * 0.6      # sebar lintas bab
            s -= 2 * sum(1 for f in c["flags"] if f[0] == "MAYOR")
            return s
        pool = [g for g in good]
        while len(chosen) < 20 and pool:
            best = max(pool, key=score); pool.remove(best)
            if ok(best): chosen.append(best); used_bab[best["bab_id"]] += 1
        # fungsi usulan
        rank = lambda c: ({"c1": 1, "c2": 2, "c3": 3, "c4": 4, "c5": 5}.get((c["q"].get("taxonomy") or {}).get("bloom"), 3), {"mudah": 1, "sedang": 2, "sulit": 3}.get((c["q"].get("taxonomy") or {}).get("difficulty"), 2))
        left = sorted(chosen, key=rank)
        fungsi = {}
        for c in left[:2]: fungsi[c["q"]["uid"]] = "diagnostik"
        rest = [c for c in left[2:]]
        for c in sorted(rest, key=lambda c: -sum(rank(c)))[:3]: fungsi[c["q"]["uid"]] = "latihan_mandiri_transfer"
        rest = [c for c in rest if c["q"]["uid"] not in fungsi]
        mid = [c for c in rest if rank(c)[0] == 3]
        if mid: fungsi[mid[0]["q"]["uid"]] = "remedial"
        rest = [c for c in rest if c["q"]["uid"] not in fungsi]
        for c in sorted(rest, key=lambda c: (-rank(c)[1], -rank(c)[0]))[:6]: fungsi[c["q"]["uid"]] = "checkpoint_akhir"
        for c in chosen:
            tx = c["q"].get("taxonomy") or {}
            selection.append({"module_id": reg[tid]["module_id"], "uid": c["q"]["uid"], "fungsi_usulan": fungsi.get(c["q"]["uid"], "latihan_terarah"), "tipe": c["gtype"],
                              "bloom": tx.get("bloom"), "kesulitan": tx.get("difficulty"), "bab_lama": c["bab"], "bagian_asal": c["q"].get("source_section_id", ""),
                              "temuan_mayor": sum(1 for f in c["flags"] if f[0] == "MAYOR")})
        cnt = collections.Counter(f[0] for it in its for f in it["flags"])
        got_d = collections.Counter((c["q"].get("taxonomy") or {}).get("difficulty") for c in chosen); got_b = collections.Counter((c["q"].get("taxonomy") or {}).get("bloom") for c in chosen)
        unit_rows.append({"module_id": reg[tid]["module_id"], "cefr": reg[tid]["cefr"], "soal": len(its), "soal_layak": len(good), "kritis": cnt["KRITIS"], "mayor": cnt["MAYOR"], "minor": cnt["MINOR"],
                          "tahap1_terpilih": len(chosen), "tahap1_penuh": int(len(chosen) == 20), "sulit_terpilih": got_d["sulit"], "c5_terpilih": got_b["c5"],
                          "tahap2_layak": int(len(good) >= 50), "kesiapan_baru": "LOLOS-QA-OTOMATIS" if len(chosen) == 20 and cnt["MAYOR"] <= 5 else ("TINJAU" if len(chosen) == 20 else "KURANG-SOAL")})
    for fn, rows in [("qa_unit_inggris_v1.csv", unit_rows), ("qa_temuan_inggris_v1.csv", findings), ("seleksi_tahap1_inggris_v1.csv", selection)]:
        with open(f"{D}/{fn}", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    kode = collections.Counter((f["tingkat"], f["kode"]) for f in findings)
    rep = {f["uid"] for f in findings if f["tingkat"] == "KRITIS" and f["detail"].startswith("REPARABEL")}; kr = {f["uid"] for f in findings if f["tingkat"] == "KRITIS"}
    print("soal KRITIS:", len(kr), "| di antaranya reparabel otomatis:", len(rep))
    print("unit dengan soal:", len(unit_rows), "| soal:", len(items), "| temuan:", len(findings))
    print("kesiapan:", collections.Counter(u["kesiapan_baru"] for u in unit_rows), "| tahap2 layak:", sum(u["tahap2_layak"] for u in unit_rows))
    for (sv, k), n in sorted(kode.items(), key=lambda x: (x[0][0], -x[1])): print(f"  {sv:6} {k:34} {n}")


if __name__ == "__main__":
    main()
