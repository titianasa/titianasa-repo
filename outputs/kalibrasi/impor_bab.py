#!/usr/bin/env python3
"""Menulis hasil bab (skema aplikasi) ke DB dev dan menyegarkan bab_bank_stats.
Pakai: python3 impor_bab.py hasil_babN.json BAB_ID   (jalankan validasi_bab.py dulu; skrip ini menolak yang tidak lolos)"""
import json, subprocess, sys
f, bab = sys.argv[1], sys.argv[2]
fase = sys.argv[3] if len(sys.argv) > 3 else None
jenis = sys.argv[4] if len(sys.argv) > 4 else ""
if fase and subprocess.run([sys.executable, "validasi_bab.py", f, fase] + ([jenis] if jenis else [])).returncode: sys.exit("validasi gagal, tidak ditulis")
d = json.load(open(f))
# soal: buang bidang bantu 'verifikasi' (bukan bagian skema aplikasi)
for g in d["quiz_config"]["question_groups"]:
    for q in g["questions"]: q.pop("verifikasi", None)
# web interaktif -> blok :::interactive_web di dalam bagian materi (penanda [[interaktif:N]] atau di akhir bagian)
for n, it in enumerate(d.pop("interaktif", []), 1):
    blk = ":::interactive_web\ntitle: " + json.dumps(it.get("title", "Web interaktif"), ensure_ascii=False) + "\nheight_mode: auto\nhtml: " + json.dumps(it["html"], ensure_ascii=False) + "\n:::"
    for sec in d["lesson_plan"]["sections"]:
        if sec["id"] == it["section_id"]:
            mark = f"[[interaktif:{n}]]"
            sec["content"] = sec["content"].replace(mark, blk) if mark in sec["content"] else sec["content"].rstrip() + "\n\n" + blk
def sql(s):
    r = subprocess.run(["docker","exec","-i","titian-bun-postgres","psql","-U","titian","titian_bun","-At","-v","ON_ERROR_STOP=1"], input=s, text=True, capture_output=True)
    if r.returncode: sys.exit(r.stderr[:400])
    return r.stdout.strip()
kids = sql(f"select id||'|'||content_type from module_items where parent_id='{bab}' and node_type='item' order by order_index").split("\n")
art = next(k.split("|")[0] for k in kids if k.endswith("|article")); quiz = next(k.split("|")[0] for k in kids if k.endswith("|quiz"))
sql(f"begin;\nupdate module_items set lesson_plan=$a${json.dumps(d['lesson_plan'], ensure_ascii=False)}$a$::jsonb, updated_at=now() where id='{art}';\nupdate module_items set quiz_config=$b${json.dumps(d['quiz_config'], ensure_ascii=False)}$b$::jsonb, updated_at=now() where id='{quiz}';\n"
    f"""insert into bab_bank_stats (bab_id, bank_id, total, diagnostik, latihan, mandiri, checkpoint, pengayaan, updated_at)
select '{bab}', '{quiz}', count(*), count(*) filter (where x->'taxonomy'->>'fungsi'='diagnostik'), count(*) filter (where x->'taxonomy'->>'fungsi' in ('latihan_terarah','checkpoint_bagian')),
 count(*) filter (where x->'taxonomy'->>'fungsi'='latihan_mandiri'), count(*) filter (where x->'taxonomy'->>'fungsi'='checkpoint_akhir'), count(*) filter (where x->'taxonomy'->>'fungsi'='pengayaan'), now()
from module_items q, jsonb_array_elements(q.quiz_config->'question_groups') g, jsonb_array_elements(g->'questions') x where q.id='{quiz}' and coalesce(trim(x->>'answer'),'')<>'' and coalesce(x->>'stem',x->>'text','')<>''
on conflict (bab_id) do update set bank_id=excluded.bank_id,total=excluded.total,diagnostik=excluded.diagnostik,latihan=excluded.latihan,mandiri=excluded.mandiri,checkpoint=excluded.checkpoint,pengayaan=excluded.pengayaan,updated_at=now();\ncommit;""")
print("tersimpan:", sql(f"select total from bab_bank_stats where bab_id='{bab}'"), "soal pada", bab)
