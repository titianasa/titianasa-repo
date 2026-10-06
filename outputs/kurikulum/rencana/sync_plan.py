#!/usr/bin/env python3
"""Menyelaraskan daftar bab rencana dengan keadaan DB sekarang (urutan bab, judul KU) dan membuang topik ganda."""
import json, glob
from sma_gen import q
import sys
for f in (sys.argv[1:] or sorted(glob.glob("*.json"))):
    p = json.load(open(f))
    subj = "(select id from modules where title='%s' and parent_id=(select id from modules where title='Semua Mata Pelajaran' and parent_id is null))" % p["mapel"].replace("'", "''")
    seen = set(); n = 0
    for k, lst in p["kelas"].items():
        out = []
        for e in lst:
            if e["topik"] in seen: continue
            seen.add(e["topik"])
            key = e["topik"]
            babs = q("""select b.title from module_items b join modules m on m.id=b.module_id join modules g on g.id=m.parent_id join modules t on t.id=g.parent_id where b.node_type='section' and b.status<>'archived' and m.title=$$%s$$ and t.parent_id=%s and m.source_module_id is null and exists (select 1 from module_labels l where l.module_id=m.id and l.kind='jenjang' and l.value like $$%%-%s$$) order by b.order_index""" % (key, subj, k))
            if babs:
                e["bab"] = [{"dari": key, "judul": b} for b in babs]; n += 1
            out.append(e)
        p["kelas"][k] = out
    json.dump(p, open(f, "w"), ensure_ascii=False, indent=1)
    print(f, "topik", len(seen), "disinkron", n)
