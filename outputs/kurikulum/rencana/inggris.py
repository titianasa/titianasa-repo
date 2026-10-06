#!/usr/bin/env python3
"""Rencana Bahasa Inggris (sekolah): Kelas dari tangga CEFR. Menghasilkan inggris.json.
A1 -> K1-5, A2 -> K6-9, B1 -> K9-12, B2 awal -> K12. B2 lanjut, C1, C2 hanya di perpustakaan & jalur Belajar Bahasa Inggris."""
import json
from sma_gen import q
SUBJ = "(select id from modules where title='Bahasa Inggris' and parent_id=(select id from modules where title='Semua Mata Pelajaran' and parent_id is null))"
TAHAPS = q("select title from modules where parent_id=%s and order_index<=5 order by order_index" % SUBJ)
rows = q("""select t.order_index, g.order_index, m.order_index, m.title, g.title, m.id,
  coalesce((select min(substr(bl.title,1,2)) from modules al join modules bg on bg.id=al.parent_id join modules bl on bl.id=bg.parent_id join modules br on br.id=bl.parent_id where al.source_module_id=m.id and br.title='Belajar Bahasa Inggris'),'-')
  from modules t join modules g on g.parent_id=t.id join modules m on m.parent_id=g.id and not m.is_folder
  where t.parent_id=%s and t.order_index<=5 and m.source_module_id is null""" % SUBJ)
items = []
for r in rows:
    a, b, c, title, grp, mid, cefr = r.split("|")
    items.append((cefr, int(a), int(b), int(c), title, grp, mid))
EXCL = {'English for Business & Professional','English for Specific Purposes','Persiapan Tes Internasional','English for Academic Purposes','Advanced Grammar & Style','Sastra & Budaya'}
items = [i for i in items if i[5] not in EXCL] + [i for i in items if i[5] in EXCL]
keluar_all = [i for i in items if i[5] in EXCL]
items = [i for i in items if i[5] not in EXCL]
items.sort()
bylev = {}
for it in items: bylev.setdefault(it[0], []).append(it)
print({k: len(v) for k, v in bylev.items()})
def take(level, n, pool):
    got = pool[level][:n]; pool[level] = pool[level][n:]; return got
pool = {k: list(v) for k, v in bylev.items()}
quota = [("1", [("A1", 5)]), ("2", [("A1", 6)]), ("3", [("A1", 6)]), ("4", [("A1", 6)]), ("5", [("A1", 99)]),
         ("6", [("A2", 10)]), ("7", [("A2", 11)]), ("8", [("A2", 11)]), ("9", [("A2", 99), ("B1", 6)]),
         ("10", [("B1", 22)]), ("11", [("B1", 22)]), ("12", [("B1", 99), ("B2", 6)])]
kelas = {}; used = set()
for k, qs in quota:
    lst = []
    for lev, n in qs:
        lst += take(lev, n, pool)
    lst.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    entries = []
    for cefr, a, b, c, title, grp, mid in lst:
        babs = q("select title from module_items where module_id='%s' and node_type='section' and status<>'archived' order by order_index" % mid)
        bab = [{"dari": title, "judul": t} for t in babs]
        if len(babs) and not any(t.startswith("Kesalahan Umum") for t in babs) and len(babs) < 5:
            bab.append("Kesalahan Umum: " + title)
        if not bab and title == 'Present Perfect Continuous':
            bab = ['Form and Meaning of the Present Perfect Continuous','Duration with For and Since','Ongoing Actions versus Completed Results','Present Perfect versus Present Perfect Continuous','Kesalahan Umum: Present Perfect Continuous']
        entries.append({"topik": title, "bab": bab}); used.add(mid)
    kelas[k] = entries
# duplikat judul topik dalam satu subjek akan salah cocok; periksa
titles = [e["topik"] for v in kelas.values() for e in v]
dups = {t for t in titles if titles.count(t) > 1}
print("judul kembar:", dups)
biarkan = [it[4] for v in pool.values() for it in v] + [it[4] for it in keluar_all]
plan = {"mapel": "Bahasa Inggris", "tahap": TAHAPS[0], "tahaps": TAHAPS, "jenjang": "AUTO", "kode": "ing", "cambridge_label": False,
        "grup": [], "label": {"rumpun": "bahasa-sastra"}, "biarkan": sorted(set(biarkan)), "kelas": kelas,
        "ki": {"jenjang": {"SD": "SD / MI — Kelas 1-6", "SMP": "SMP / MTs — Kelas 7-9", "SMA": "SMA / MA — Kelas 10-12"},
               "kelas": {"SD": "Kelas {n} SD/MI", "SMP": "Kelas {n} SMP/MTs", "SMA": "Kelas {n} SMA/MA"}, "bundle": "Bahasa Inggris"},
        "tka": [{"folder": "TKA SMP/MTs", "bundle": "Bahasa Inggris", "kelas": [8, 9]}, {"via": ["TKA SMA/MA", "Mata Pelajaran Wajib"], "bundle": "Bahasa Inggris", "kelas": [10, 11, 12]}]}
json.dump(plan, open("inggris.json", "w"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in kelas.items()}, "dibiarkan", len(plan["biarkan"]))
