#!/usr/bin/env python3
"""Appends Cambridge International (IGCSE / AS & A Level) syllabus
references to the `standar` array of tahaps whose subject genuinely has
a Cambridge equivalent — the same "several curricula share one bab plan"
pattern Claude's original Fisika/Kimia work already used (see those
rows' `standar` arrays). Doesn't touch subjects with no real Cambridge
counterpart (madrasah subjects, Indonesia-specific civics/history,
professional exam prep, etc).

All syllabus codes verified against cambridgeinternational.org as
current for 2026 examinations before writing this (Geography is 0460,
NOT the UK-only 9-1 variant 0976; Business Studies is still 0450, the
0264 code only starts 2027).

Idempotent: only appends a code if the tahap's `standar` array doesn't
already contain a string with that syllabus number.

Usage: python3 add_cambridge_references.py [--dry-run]
"""
import json
import subprocess
import sys

DRY_RUN = "--dry-run" in sys.argv


def psql(sql: str) -> str:
    return subprocess.run(
        ["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-t", "-A", "-c", sql],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


# (subject, tahap title substring) -> Cambridge reference to append.
# IGCSE covers roughly age 14-16 (~SMA kelas 10 in Indonesia); AS & A
# Level covers ~16-19 (~SMA kelas 11-12 / awal kuliah) — same "batas
# atas" framing the Fisika/Kimia rows already use for the S1 tahap that
# overlaps it.
ADDITIONS: list[tuple[str, str, str]] = [
    ("Matematika", "Tahap 3", "Cambridge IGCSE Mathematics 0580"),
    ("Matematika", "Tahap 4", "Cambridge International AS & A Level Mathematics 9709"),
    ("Biologi", "Tahap 2", "Cambridge IGCSE Biology 0610"),
    ("Biologi", "Tahap 3", "Cambridge IGCSE Biology 0610"),
    ("Biologi", "Tahap 4", "Cambridge International AS & A Level Biology 9700"),
    ("Biologi", "Tahap 5", "Cambridge International AS & A Level Biology 9700"),
    ("Biologi", "Tahap 6", "Batas atas A Level Biology 9700 untuk topik yang juga dipakai jalur Cambridge"),
    ("Ekonomi", "Tahap 1", "Cambridge IGCSE Economics 0455"),
    ("Ekonomi", "Tahap 2", "Cambridge IGCSE Economics 0455"),
    ("Ekonomi", "Tahap 3", "Cambridge International AS & A Level Economics 9708"),
    ("Ekonomi", "Tahap 4", "Cambridge International AS & A Level Economics 9708"),
    ("Ekonomi", "Tahap 5", "Batas atas A Level Economics 9708 untuk topik yang juga dipakai jalur Cambridge"),
    ("Akuntansi", "Tahap 1", "Cambridge IGCSE Accounting 0452"),
    ("Akuntansi", "Tahap 2", "Cambridge IGCSE Accounting 0452"),
    ("Akuntansi", "Tahap 3", "Cambridge IGCSE Accounting 0452"),
    ("Akuntansi", "Tahap 5", "Cambridge International AS & A Level Accounting 9706"),
    ("Bisnis & Manajemen", "Tahap 1", "Cambridge IGCSE Business Studies 0450"),
    ("Bisnis & Manajemen", "Tahap 2", "Cambridge International AS & A Level Business 9609"),
    ("Bisnis & Manajemen", "Tahap 3", "Cambridge International AS & A Level Business 9609"),
    ("Geografi", "Tahap 1", "Cambridge IGCSE Geography 0460"),
    ("Geografi", "Tahap 2", "Cambridge IGCSE Geography 0460"),
    ("Geografi", "Tahap 3", "Cambridge International AS & A Level Geography 9696"),
    ("Geografi", "Tahap 4", "Cambridge International AS & A Level Geography 9696"),
    ("Geografi", "Tahap 5", "Batas atas A Level Geography 9696 untuk topik yang juga dipakai jalur Cambridge"),
    # Sejarah: only "Sejarah Dunia" and the university tahap overlap —
    # Cambridge IGCSE/A Level History covers general/world historical
    # themes, not Indonesia-specific depth studies, so the other tahaps
    # (Indonesia praaksara-Islam, kolonialisme, kemerdekaan) are left
    # alone rather than force a misleading match.
    ("Sejarah", "Tahap 5", "Cambridge IGCSE History 0470 dan AS & A Level History 9489 — topik sejarah dunia yang relevan"),
    ("Informatika", "Tahap 2", "Cambridge IGCSE Computer Science 0478"),
    ("Informatika", "Tahap 3", "Cambridge IGCSE Computer Science 0478"),
    ("Informatika", "Tahap 4", "Cambridge IGCSE Computer Science 0478"),
    ("Informatika", "Tahap 5", "Cambridge International AS & A Level Computer Science 9618"),
    ("Bahasa Inggris", "Tahap 3", "Cambridge IGCSE English as a Second Language 0510"),
    ("Bahasa Inggris", "Tahap 4", "Cambridge IGCSE English as a Second Language 0510"),
    ("Bahasa Inggris", "Tahap 5", "Cambridge IGCSE English as a Second Language 0510"),
    ("Bahasa Inggris", "Tahap 6", "Cambridge International AS & A Level English Language 9093"),
]


def main():
    raw = psql(
        "select json_agg(row_to_json(x) order by x.subject, x.tahap) from ("
        "  select t.id as tahap_id, s.title as subject, t.title as tahap, cs.standar "
        "  from curriculum_standards cs join modules t on t.id = cs.tahap_folder_id join modules s on s.id = t.parent_id"
        ") x;"
    )
    rows = json.loads(raw)
    by_key = {(r["subject"], r["tahap"]): r for r in rows}

    applied = 0
    skipped = 0
    for subject, tahap_prefix, addition in ADDITIONS:
        matches = [r for (subj, tahap), r in by_key.items() if subj == subject and tahap.startswith(tahap_prefix)]
        if not matches:
            print(f"!! no tahap found for {subject} / {tahap_prefix}", file=sys.stderr)
            continue
        for row in matches:
            # Idempotent: skip if a reference to the same syllabus
            # number is already present (re-running never duplicates).
            code = next((tok for tok in addition.split() if tok.isdigit() or (len(tok) == 4 and tok.isalnum())), None)
            already = code and any(code in s for s in row["standar"])
            if already:
                skipped += 1
                continue
            new_array = row["standar"] + [addition]
            array_sql = "{" + ",".join('"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"' for s in new_array) + "}"
            array_sql = array_sql.replace("'", "''")
            sql = f"update curriculum_standards set standar = '{array_sql}', updated_at = now() where tahap_folder_id = '{row['tahap_id']}';"
            if DRY_RUN:
                print(f"[dry-run] {subject} / {row['tahap']} += {addition!r}")
            else:
                psql(sql)
            applied += 1

    print(f"\n=== {applied} referensi Cambridge {'akan' if DRY_RUN else ''} ditambahkan, {skipped} sudah ada (dilewati) ===")


if __name__ == "__main__":
    main()
