#!/usr/bin/env python3
"""Alur cepat: tulis -> validator -> perbaiki otomatis -> penjawab buta kunci -> (telaah hanya bila berisiko) -> impor.
Semua panggilan lewat OpenRouter; model diatur lewat argumen. Tanpa salin-tempel.

  python3 otomatis_bab.py --urutan 1-5 --penulis MODEL --penjawab MODEL [--penelaah MODEL] [--paralel 3] [--dry] [--tanpa-impor]

Biaya dan waktu tiap bab dicatat di log_otomatis.jsonl untuk kalibrasi."""
import argparse, asyncio, csv, json, os, re, subprocess, sys, time, urllib.request, uuid
HERE = os.path.dirname(os.path.abspath(__file__))
def env_key():
    for p in (os.path.join(HERE, "../../titian-backend-rust/.env"),):
        for l in open(p):
            if l.startswith("OPENROUTER_API_KEY="): return l.split("=", 1)[1].strip().strip('"')
    sys.exit("OPENROUTER_API_KEY tidak ditemukan")
FASE = lambda k: "A" if k <= 2 else "B" if k <= 4 else "C" if k <= 6 else "D" if k <= 9 else "E"
JENIS = {"Matematika": "hitungan", "Fisika": "hitungan", "Kimia": "hitungan", "Akuntansi": "hitungan", "Bahasa Indonesia": "bahasa", "Bahasa Inggris": "bahasa", "Penalaran & Logika": "penalaran"}
def psql(q): return subprocess.run(["docker", "exec", "-i", "titian-bun-postgres", "psql", "-U", "titian", "titian_bun", "-At", "-F", "|", "-c", q], capture_output=True, text=True).stdout.strip()
def chat(model, system, user, key, json_mode=True, max_tokens=32000):
    body = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "max_tokens": max_tokens, "temperature": 0.4}
    if json_mode: body["response_format"] = {"type": "json_object"}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", json.dumps(body).encode(), {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=900)); u = r.get("usage", {})
    txt = r["choices"][0]["message"]["content"]
    return txt, u.get("prompt_tokens", 0), u.get("completion_tokens", 0), u.get("cost")
def as_json(txt):
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    return json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
def prompt_penulis(row):
    raw = open(os.path.join(HERE, "PROMPT_GENERATE_BAB_V2.md")).read().split("\n---\n", 1)[1]
    top = psql(f"select module_id from module_items where id='{row['bab_id']}'")
    lain = psql(f"select title from module_items where module_id='{top}' and node_type='section' and status<>'archived' and id<>'{row['bab_id']}' order by order_index").split("\n")
    ku = next((t for t in lain if t.startswith("Kesalahan Umum")), "-")
    rep = {"MAPEL": row["mapel"], "KELAS": row["kelas"], "FASE": FASE(int(row["kelas"])), "TOPIK": row["topik"], "BAB": row["bab"], "BAB_LAIN": "; ".join(lain), "KESALAHAN_UMUM": ku, "JENIS_SOAL": JENIS.get(row["mapel"], "konsep"), "NOMOR": row["urutan"]}
    for k, v in rep.items(): raw = raw.replace("{{" + k + "}}", str(v))
    return raw, rep
def validasi(path, fase, jenis):
    r = subprocess.run([sys.executable, os.path.join(HERE, "validasi_bab.py"), path, fase, jenis], capture_output=True, text=True, cwd=HERE)
    return r.returncode == 0, [l.strip() for l in r.stdout.splitlines() if "✗" in l]
def tanpa_kunci(d):
    out = {"materi": d["lesson_plan"], "soal": []}
    for g in d["quiz_config"]["question_groups"]:
        for q in g["questions"]:
            it = {"uid": q["uid"], "tipe": g["type"], "teks": q.get("stem") or q.get("text")}
            if g["type"] == "multiple_choice": it["pilihan"] = q["choices"]
            if g["type"] == "true_false": it["pilihan"] = ["Benar", "Salah"]
            out["soal"].append(it)
    return out
def norm(s): return re.sub(r"\s+", " ", str(s).strip().strip(".,!?").lower())
def cocok(d, ans):
    bad = []
    for g in d["quiz_config"]["question_groups"]:
        for q in g["questions"]:
            got = ans.get(q["uid"]); key = q["answer"]
            ok = got is not None and (str(got).strip().upper() == key.upper() if g["type"] == "multiple_choice" else norm(got) in [norm(k) for k in key.split("|")])
            if not ok: bad.append(q["uid"])
    return bad
def tukar_soal(d, baru):
    by = {q["uid"]: q for q in baru}
    for g in d["quiz_config"]["question_groups"]:
        g["questions"] = [by.get(q["uid"], q) for q in g["questions"]]
async def kerjakan(row, a, key, sem):
    async with sem:
        t0 = time.time(); log = {"urutan": row["urutan"], "bab": row["bab"], "token_masuk": 0, "token_keluar": 0, "biaya": 0.0, "putaran": 0, "status": "gagal"}
        def hitung(r): log["token_masuk"] += r[1]; log["token_keluar"] += r[2]; log["biaya"] += float(r[3] or 0); return r[0]
        call = lambda *x, **k: asyncio.to_thread(chat, *x, key, **k)
        sistem, rep = prompt_penulis(row); fase, jenis = rep["FASE"], rep["JENIS_SOAL"]
        path = os.path.join(HERE, f"hasil_bab{row['urutan']}_auto.json")
        d = as_json(hitung(await call(a.penulis, "Kamu menulis bab pembelajaran. Keluarkan hanya JSON.", sistem)))
        for ronde in range(a.putaran + 1):
            log["putaran"] = ronde; json.dump(d, open(path, "w"), ensure_ascii=False, indent=1)
            ok, err = validasi(path, fase, jenis)
            if not ok:
                if ronde == a.putaran: log["catatan"] = err[:5]; break
                d = as_json(hitung(await call(a.penulis, "Perbaiki bab ini. Keluarkan hanya JSON lengkap yang sudah diperbaiki.", f"BAB SEBELUMNYA:\n{json.dumps(d, ensure_ascii=False)}\n\nPELANGGARAN DARI VALIDATOR (perbaiki semuanya, jangan mengubah yang sudah benar):\n" + "\n".join(err))))
                continue
            ans = as_json(hitung(await call(a.penjawab, "Kamu murid teliti. Kerjakan tiap soal sendiri. Keluarkan hanya JSON {\"jawaban\": {uid: jawaban}}.", json.dumps(tanpa_kunci(d), ensure_ascii=False)))).get("jawaban", {})
            bad = cocok(d, ans)
            if bad and ronde < a.putaran:
                ket = [q for g in d["quiz_config"]["question_groups"] for q in g["questions"] if q["uid"] in bad]
                fix = as_json(hitung(await call(a.penulis, "Periksa soal-soal ini: penjawab independen tidak cocok dengan kuncimu. Hitung ulang dari nol. Perbaiki kunci yang salah atau tulis ulang soal yang ambigu. Keluarkan JSON {\"soal\": [soal lengkap dengan uid yang sama]}.", json.dumps({"materi": d["lesson_plan"], "soal_bermasalah": ket, "jawaban_penjawab": {u: ans.get(u) for u in bad}}, ensure_ascii=False)))).get("soal", [])
                tukar_soal(d, fix); continue
            if bad: log["catatan"] = f"{len(bad)} soal tidak cocok"; break
            perlu = a.telaah_semua or (row.get("pertama") == "1")
            if perlu and a.penelaah:
                rk = as_json(hitung(await call(a.penelaah, open(os.path.join(HERE, "PROMPT_PENELAAH_BAB.md")).read().split("Langkah 2")[1], json.dumps(d, ensure_ascii=False))))
                if rk.get("putusan") != "lulus":
                    if ronde == a.putaran: log["catatan"] = [i["masalah"] for i in rk.get("isu", []) if i["tingkat"] != "minor"][:5]; break
                    d = as_json(hitung(await call(a.penulis, "Perbaiki bab ini sesuai isu penelaah. Keluarkan hanya JSON lengkap.", f"BAB:\n{json.dumps(d, ensure_ascii=False)}\n\nISU:\n{json.dumps(rk.get('isu', []), ensure_ascii=False)}"))); continue
            log["status"] = "lolos"
            if not a.tanpa_impor:
                r = subprocess.run([sys.executable, os.path.join(HERE, "impor_bab.py"), path, row["bab_id"], fase, jenis], capture_output=True, text=True, cwd=HERE); log["impor"] = r.stdout.strip()[-60:] or r.stderr[-100:]
            break
        log["detik"] = round(time.time() - t0); open(os.path.join(HERE, "log_otomatis.jsonl"), "a").write(json.dumps(log, ensure_ascii=False) + "\n"); print(log); return log
async def main():
    p = argparse.ArgumentParser(); p.add_argument("--urutan", required=True); p.add_argument("--penulis", required=True); p.add_argument("--penjawab", required=True); p.add_argument("--penelaah")
    p.add_argument("--paralel", type=int, default=3); p.add_argument("--putaran", type=int, default=2); p.add_argument("--telaah-semua", action="store_true"); p.add_argument("--dry", action="store_true"); p.add_argument("--tanpa-impor", action="store_true"); a = p.parse_args()
    lo, hi = (a.urutan.split("-") + [a.urutan])[:2] if "-" in a.urutan else (a.urutan, a.urutan)
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "../kurikulum/antrean_generate_v1.csv"))) if int(lo) <= int(r["urutan"]) <= int(hi)]
    seen = set()
    for r in rows: r["pertama"] = "1" if r["topik"] not in seen else "0"; seen.add(r["topik"])
    if a.dry: print(prompt_penulis(rows[0])[0][:1500], "...\n[dry] baris:", len(rows)); return
    key = env_key(); sem = asyncio.Semaphore(a.paralel); res = await asyncio.gather(*[kerjakan(r, a, key, sem) for r in rows])
    print("lolos", sum(r["status"] == "lolos" for r in res), "dari", len(res), "| biaya", round(sum(r["biaya"] for r in res), 4), "USD")
asyncio.run(main())
