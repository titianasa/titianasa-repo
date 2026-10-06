#!/usr/bin/env python3
"""Menerapkan rencana kurikulum: python3 terapkan.py rencana/matematika_sd.json [--dry]
Satu transaksi; --dry membatalkan (ROLLBACK) setelah menampilkan ringkasan."""
import json, subprocess, sys
plan_path = sys.argv[1]
dry = "--dry" in sys.argv
plan = json.load(open(plan_path))
sql = "begin;\ndo $x$ begin perform set_config('app.plan', $plan$" + json.dumps(plan, ensure_ascii=False) + "$plan$, false); end $x$;\n"
sql += open(__file__.replace("terapkan.py", "terapkan_rencana.sql")).read()
sql += "\n" + ("rollback;" if dry else "commit;") + "\n"
r = subprocess.run(["docker", "exec", "-i", "titian-bun-postgres", "psql", "-U", "titian", "titian_bun", "-v", "ON_ERROR_STOP=1", "-q"], input=sql, text=True, capture_output=True)
print(r.stdout.strip()[:600]); print("\n".join(l[:300] for l in r.stderr.splitlines() if "NOTICE" in l or "ERROR" in l or "DETAIL" in l or "CONTEXT" in l or "HINT" in l)[:6000])
sys.exit(r.returncode)
