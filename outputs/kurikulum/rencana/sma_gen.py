"""Generator rencana SMA untuk mapel yang strukturnya sudah baik (Fisika, Kimia, Biologi):
kelas diambil dari label jenjang yang ada, dengan koreksi (pindah kelas, tambah, hapus)."""
import json, subprocess

def q(sql):
    r = subprocess.run(["docker","exec","-i","titian-bun-postgres","psql","-U","titian","titian_bun","-At","-F","|","-c",sql],capture_output=True,text=True)
    return [l for l in r.stdout.split("\n") if l]

def build(mapel, kode, tahap_like, rumpun, tka_bundle, pindah=None, pindah_grup=None, tambah=(), hapus=(), grup_baru=(), keluar=(), ku_pola="Kesalahan Umum: {t}", out=None, tka_via=("TKA SMA/MA", "Pilihan Saintek")):
    pindah = pindah or {}; pindah_grup = pindah_grup or {}
    subj = "(select id from modules where title='%s' and parent_id=(select id from modules where title='Semua Mata Pelajaran' and parent_id is null))" % mapel
    rows = q("""select t.title, g.title, m.title, l.value, m.id from modules t join modules g on g.parent_id=t.id join modules m on m.parent_id=g.id and not m.is_folder
      join module_labels l on l.module_id=m.id and l.kind='jenjang' where t.parent_id=%s and (%s) order by t.order_index, g.order_index, m.order_index""" % (subj, " or ".join("t.title like '%s'" % x for x in tahap_like)))
    tahaps = sorted({r.split("|")[0] for r in rows}, key=lambda x: x)
    tahaps = [l.split("|")[0] for l in q("select title from modules t where t.parent_id=%s and (%s) order by order_index" % (subj, " or ".join("t.title like '%s'" % x for x in tahap_like)))]
    kelas = {"10": [], "11": [], "12": []}; tinggal = []
    for r in rows:
        tahap, grup, topik, jen, tid = r.split("|")
        if topik in hapus or topik in keluar: continue
        if not jen.startswith("SMA-"):
            tinggal.append(topik); continue
        n = pindah.get(topik) or pindah_grup.get(grup) or jen.split("-")[1]
        babs = [b for b in q("select title from module_items where module_id='%s' and node_type='section' and status<>'archived' order by order_index" % tid)]
        bab = [{"dari": topik, "judul": b} for b in babs if not b.startswith("Kesalahan Umum")]
        if len(babs) < 5 or any(b.startswith("Kesalahan Umum") for b in babs) is False and len(babs) < 5:
            pass
        if not any(b.startswith("Kesalahan Umum") for b in babs) and len(babs) < 5:
            bab.append(ku_pola.format(t=topik))
        elif any(b.startswith("Kesalahan Umum") for b in babs):
            bab += [{"dari": topik, "judul": b} for b in babs if b.startswith("Kesalahan Umum")]
        kelas[str(n)].append({"topik": topik, "bab": bab})
    for n, setelah, entri in tambah:
        lst = kelas[str(n)]
        idx = 0 if setelah == "START" else next((i for i, e in enumerate(lst) if e["topik"] == setelah), len(lst) - 1) + 1 if setelah else len(lst)
        lst.insert(idx, entri)
    for k in kelas:
        for e in kelas[k]: e.pop("_sort", None)
    plan = {"mapel": mapel, "tahap": tahaps[0], "tahaps": tahaps, "jenjang": "SMA", "kode": kode, "cambridge_label": False,
            "grup": list(grup_baru), "label": {"kurikulum": "merdeka-sma", "jalur": "sma-ma", "rumpun": rumpun}, "hapus_topik": list(hapus), "biarkan": list(keluar) + tinggal,
            "kelas": kelas,
            "ki": {"jenjang": "SMA / MA — Kelas 10-12", "kelas": "Kelas {n} SMA/MA", "bundle": mapel},
            "tka": ([{"via": list(tka_via), "bundle": tka_bundle, "kelas": [10, 11, 12]}] if tka_bundle else [])}
    json.dump(plan, open(out or kode + ".json", "w"), ensure_ascii=False, indent=1)
    print(mapel, {k: len(v) for k, v in kelas.items()}, "bab", sum(len(t["bab"]) for v in kelas.values() for t in v))
    return plan

def N(topik, tahap, grup, bab, ku):
    return {"topik": topik, "tahap": tahap, "grup": grup, "bab": list(bab) + ["Kesalahan Umum: " + ku]}
