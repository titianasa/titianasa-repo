#!/usr/bin/env python3
"""Lingkup P0: topik lama yang dipakai TKA / ujian masuk PT / tes Inggris (penggerak produksi).
Cambridge hanya konversi (label). BUMN/CPNS ditunda. Topik MERGE tidak diproduksi (duplikat Matematika)."""
import csv, collections, os
D = os.path.dirname(os.path.abspath(__file__))
refs = list(csv.DictReader(open(f"{D}/pemetaan_referensi_v1.csv")))
top = {r["id"]: r for r in csv.DictReader(open(f"{D}/pemetaan_topik_v1.csv"))}
GROUP = {"Fokus Ujian TKA": "TKA", "Persiapan Ujian Masuk Perguruan Tinggi": "PTN", "Belajar Bahasa Inggris": "ENG", "Kurikulum Cambridge": "CAMB"}
fl = collections.defaultdict(set)
for r in refs:
    g = GROUP.get(r["jalur"])
    if not g or r["kecocokan_seksi"] != "ok": continue
    if top[r["topik_id"]]["jenis_pemetaan"] == "EXTENSION": continue
    if g == "PTN" and r["seksi"].startswith("UM-PTKIN"): g = "PTKIN"
    fl[r["topik_id"]].add(g)
rows = []
for tid, g in fl.items():
    t = top[tid]; drivers = g & {"TKA", "PTN", "ENG"}
    if t["jenis_pemetaan"] == "MERGE-KE-MATEMATIKA": tier = "MERGE"
    elif drivers: tier = "P0a" if len(drivers) >= 2 else "P0b"
    elif "PTKIN" in g: tier = "P1-PTKIN"
    else: tier = "KONVERSI-SAJA"
    rows.append({"topik_id": tid, "mapel": t["subject"], "kluster": t["cluster"], "topik": t["topic"], "rumah_kanonik": t["rumah_kanonik"],
                 "konsep_kanonik": t["konsep_kanonik"], "template_blueprint": t["template_blueprint"], "cefr": t["cefr"],
                 "TKA": int("TKA" in g), "PTN": int("PTN" in g), "ENG": int("ENG" in g), "PTKIN": int("PTKIN" in g), "CAMB": int("CAMB" in g),
                 "jumlah_penggerak": len(drivers), "tier": tier, "jenis_pemetaan": t["jenis_pemetaan"], "bab_lama": t["bab"], "bab_bermateri": t["bab_materi"]})
order = {"P0a": 0, "P0b": 1, "MERGE": 2, "P1-PTKIN": 3, "KONVERSI-SAJA": 4}
rows.sort(key=lambda x: (order[x["tier"]], -x["jumlah_penggerak"], x["mapel"], x["kluster"], x["topik"]))
with open(f"{D}/lingkup_p0_v1.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(collections.Counter(r["tier"] for r in rows))
