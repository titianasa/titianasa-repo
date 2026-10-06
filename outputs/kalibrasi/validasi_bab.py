#!/usr/bin/env python3
"""Validator satu bab (materi + bank 50). Pakai: python3 validasi_bab.py hasil_babN.json FASE   (FASE = A|B|C|D|E)
Keluar 0 jika lolos, 1 jika ada pelanggaran. Tanpa token."""
import json, re, sys, collections
f, fase = sys.argv[1], sys.argv[2].upper()
jenis = sys.argv[3].lower() if len(sys.argv) > 3 else ""
d = json.load(open(f)); lp, qc = d["lesson_plan"], d["quiz_config"]
SENT = {"A": (6, 10), "B": (10, 16), "C": (14, 22), "D": (18, 28), "E": (22, 34)}[fase]
WORDS = {"A": 120, "B": 180, "C": 250, "D": 300, "E": 400}[fase]
NSEC = {"A": (3, 4), "B": (4, 4), "C": (4, 5), "D": (5, 5), "E": (5, 5)}[fase]
err = []
def E(m): err.append(m)
# ── materi
secs = lp.get("sections", [])
if not NSEC[0] <= len(secs) <= NSEC[1]: E(f"jumlah bagian {len(secs)} di luar {NSEC}")
ids = set()
for s in secs:
    for k in ("id", "title", "goal", "content", "minutes"):
        if not s.get(k): E(f"bagian {s.get('id')} tanpa {k}")
    ids.add(s.get("id"))
    txt = re.sub(r"^:::.*$", "", s.get("content", ""), flags=re.M)
    txt = re.sub(r"^(term|definition|title|text|variant|explanation|items|headers|rows|caption):", "", txt, flags=re.M)
    txt = re.sub(r"\$\$.+?\$\$|(?<!\\)\$.+?(?<!\\)\$", " M ", txt, flags=re.S)
    txt = re.sub(r"[*#`>|\[\]\"]", " ", txt)
    words = re.findall(r"\w+", txt)
    if len(words) > WORDS * 1.1: E(f"bagian '{s.get('title')}' {len(words)} kata > {WORDS}")
    sents = [x for x in re.split(r"[.!?\n]+", txt) if len(re.findall(r"\w+", x)) >= 2]
    lens = [len(re.findall(r"\w+", x)) for x in sents]
    if lens and sum(lens) / len(lens) > SENT[0] * 1.15: E(f"bagian '{s.get('title')}' rata-rata {sum(lens)/len(lens):.1f} kata/kalimat > {SENT[0]}")
    if lens and max(lens) > SENT[1] + 3: E(f"bagian '{s.get('title')}' kalimat terpanjang {max(lens)} kata > {SENT[1]}")
allc = " ".join(s.get("content", "") for s in secs)
if ":::common_trap" not in allc: E("tidak ada blok :::common_trap (kesalahan umum)")
if ":::steps" not in allc and ":::table" not in allc and ":::definition" not in allc: E("tidak ada blok terstruktur (definition/steps/table)")
# ── bank
qs = []
for g in qc.get("question_groups", []):
    for q in g["questions"]: qs.append((g["type"], q))
if len(qs) != 50: E(f"jumlah soal {len(qs)} != 50")
C = collections.Counter
bloom = C(q["taxonomy"]["bloom"] for _, q in qs); diff = C(q["taxonomy"]["difficulty"] for _, q in qs); fg = C(q["taxonomy"]["fungsi"] for _, q in qs)
dim = C(q["taxonomy"].get("knowledge_dimension") for _, q in qs)
for k, v in {"c1": 5, "c2": 8, "c3": 14, "c4": 12, "c5": 6, "c6": 2}.items():
    if bloom[k] < v: E(f"bloom {k} = {bloom[k]} < {v}")
if dict(diff) != {"mudah": 15, "sedang": 25, "sulit": 10}: E(f"kesulitan {dict(diff)}")
if dict(fg) != {"diagnostik": 4, "latihan_terarah": 22, "latihan_mandiri": 8, "checkpoint_akhir": 10, "remedial": 4, "pengayaan": 2}: E(f"fungsi {dict(fg)}")
for k in ("faktual", "konseptual", "prosedural"):
    if dim[k] < 3: E(f"dimensi {k} = {dim[k]} < 3")
if dim["metakognitif"] < 2: E(f"dimensi metakognitif = {dim['metakognitif']} < 2")
types = C(t for t, _ in qs)
if set(types) - {"multiple_choice", "true_false", "short_answer"}: E(f"tipe tidak didukung: {set(types)}")
if fase in "AB" and types["short_answer"] > 5: E("isian > 10% untuk Fase A-B")
uids = [q.get("uid") for _, q in qs]
if len(set(uids)) != len(uids) or not all(uids): E("uid tidak unik / kosong")
stems = [(q.get("stem") or q.get("text") or "").strip().lower() for _, q in qs]
if len(set(stems)) != len(stems): E("ada stem kembar")
letters = C()
for t, q in qs:
    tax = q["taxonomy"]; stem = q.get("stem") or q.get("text") or ""
    if not stem.strip() or not q.get("explanation", "").strip(): E(f"{q.get('uid')}: stem/pembahasan kosong")
    if q.get("source_section_id") not in ids: E(f"{q.get('uid')}: source_section_id tidak ada di materi")
    if fase in "AB" and len(re.findall(r"\w+", re.sub(r"[^\w\s]", " ", stem))) > 16: E(f"{q.get('uid')}: stem terlalu panjang untuk Fase {fase}")
    if t == "multiple_choice":
        ch = q.get("choices", [])
        if len(ch) != 4: E(f"{q.get('uid')}: pilihan {len(ch)} != 4")
        labs = [c.get("label") for c in ch]
        if labs != ["A", "B", "C", "D"][:len(ch)]: E(f"{q.get('uid')}: label {labs}")
        if q.get("answer") not in labs: E(f"{q.get('uid')}: kunci {q.get('answer')} tidak ada")
        if len({c.get("text") for c in ch}) != len(ch): E(f"{q.get('uid')}: pilihan kembar")
        if any(re.search(r"semua (jawaban )?(benar|salah)|tidak ada (yang )?benar", c.get("text", ""), re.I) for c in ch): E(f"{q.get('uid')}: pilihan 'semua benar/salah'")
        letters[q.get("answer")] += 1
    elif t == "true_false":
        if q.get("answer") not in ("Benar", "Salah"): E(f"{q.get('uid')}: kunci TF {q.get('answer')}")
        if tax["bloom"] in ("c5", "c6"): E(f"{q.get('uid')}: TF tidak boleh C5/C6")
        if "text" not in q: E(f"{q.get('uid')}: TF harus memakai 'text'")
    else:
        if not str(q.get("answer", "")).strip(): E(f"{q.get('uid')}: kunci isian kosong")
    if tax["fungsi"] == "remedial" and (t != "multiple_choice" or not tax.get("miskonsepsi_target")): E(f"{q.get('uid')}: remedial harus pilihan ganda + miskonsepsi_target")
    if tax["fungsi"] == "pengayaan" and tax["bloom"] != "c6": E(f"{q.get('uid')}: pengayaan harus c6")
if letters and max(letters.values()) / sum(letters.values()) > 0.4: E(f"posisi kunci timpang: {dict(letters)}")
# ── LaTeX: harus bisa dirender KaTeX aplikasi; pembatas hanya $...$ dan $$...$$
import subprocess, os
MATH = re.compile(r"\$\$(.+?)\$\$|(?<!\\)\$(.+?)(?<!\\)\$", re.S)
segs = []
def scan(where, text):
    if not isinstance(text, str): return
    if re.search(r"\\\(|\\\[|\\begin\{(equation|align)", text): E(f"{where}: pembatas LaTeX tidak didukung (pakai $...$ atau $$...$$)")
    for m in MATH.finditer(text): segs.append({"where": where, "latex": (m.group(1) or m.group(2)), "display": m.group(1) is not None})
    rest = MATH.sub("", text).replace("\\$", "")
    if "$" in rest: E(f"{where}: tanda $ tunggal (rupiah harus ditulis \\$)")
    if "\\ce{" in text: E(f"{where}: \\ce{{}} (mhchem) tidak tersedia; pakai \\mathrm{{H_2O}}")
for sc in secs: scan("materi:" + str(sc.get("title")), sc.get("content", ""))
for t, q in qs:
    u = q.get("uid")
    scan(f"{u}:stem", q.get("stem") or q.get("text")); scan(f"{u}:pembahasan", q.get("explanation"))
    for c in q.get("choices", []): scan(f"{u}:pilihan{c.get('label')}", c.get("text"))
    if t == "short_answer" and re.search(r"[$\\]", str(q.get("answer", ""))): E(f"{u}: kunci isian tidak boleh berisi LaTeX; tulis polos, mis. 2x+3|2x + 3")
if segs:
    r = subprocess.run(["node", os.path.join(os.path.dirname(os.path.abspath(__file__)), "cek_latex.mjs")], input=json.dumps(segs), capture_output=True, text=True)
    try:
        for b in json.loads(r.stdout or "[]"): E(f"LaTeX tidak valid di {b['where']}: {b['latex'][:50]} -> {b['error']}")
    except Exception: E("pemeriksa LaTeX (node) gagal berjalan: " + r.stderr[:150])

# ── verifikasi hitungan (kunci diperiksa oleh kode, bukan oleh penulis)
import math, fractions
SAFE = {k: getattr(math, k) for k in ("sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "log", "log10", "exp", "pi", "e", "factorial", "comb", "perm", "gcd", "radians", "degrees", "floor", "ceil")}
SAFE.update({"abs": abs, "round": round, "min": min, "max": max, "sum": sum, "Fraction": fractions.Fraction, "pow": pow})
def num_of(text):
    m = re.search(r"-?\d+(?:[.,]\d+)?", str(text).replace(" ", "")); return float(m.group(0).replace(",", ".")) if m else None
nver = 0
for t, q in qs:
    v = q.get("verifikasi")
    if not v: continue
    nver += 1; u = q.get("uid")
    try:
        got = eval(str(v["ekspresi"]), {"__builtins__": {}}, SAFE); want = float(str(v["hasil"]).replace(",", "."))
        if abs(float(got) - want) > 1e-6 * max(1, abs(want)): E(f"{u}: verifikasi gagal, ekspresi = {got}, tertulis {want}")
        key = q.get("answer") if t != "multiple_choice" else next((c["text"] for c in q.get("choices", []) if c.get("label") == q.get("answer")), "")
        kn = num_of(str(key).split("|")[0])
        if t != "true_false" and kn is not None and abs(kn - want) > 1e-6 * max(1, abs(want)): E(f"{u}: kunci ({kn}) tidak sama dengan hasil verifikasi ({want})")
    except Exception as ex: E(f"{u}: verifikasi tidak bisa dijalankan ({ex})")
if jenis == "hitungan" and nver < 20: E(f"soal hitungan wajib punya 'verifikasi' pada minimal 20 soal (ada {nver})")
# ── web interaktif
inter = d.get("interaktif", [])
ALLOW_CDN = ("cdn.jsdelivr.net", "cdnjs.cloudflare.com")
import tempfile
for it in inter:
    h = it.get("html", ""); tt = it.get("title", "?")
    if it.get("section_id") not in ids: E(f"interaktif '{tt}': section_id tidak ada di materi")
    if not h.lstrip().lower().startswith("<!doctype html"): E(f"interaktif '{tt}': harus dimulai <!DOCTYPE html>")
    if len(h) > 120000: E(f"interaktif '{tt}': {len(h)} karakter > 120000")
    if re.search(r"<iframe|<object|<embed|\son(click|change|input|load)\s*=", h, re.I): E(f"interaktif '{tt}': iframe/object/embed/handler inline dilarang")
    if re.search(r"""(href|src)\s*=\s*["']https?://(?!(%s))""" % "|".join(re.escape(x) for x in ALLOW_CDN), h, re.I): E(f"interaktif '{tt}': sumber luar di luar CDN yang diizinkan")
    if not re.search(r"Titian\.(complete|submitScore)\(", h): E(f"interaktif '{tt}': tidak memanggil window.Titian.complete()/submitScore()")
    if "--primary" not in h or "--background" not in h: E(f"interaktif '{tt}': tidak memakai token warna Titian (--primary, --background)")
    if "html.dark" not in h and "data-theme" not in h: E(f"interaktif '{tt}': tidak ada gaya mode gelap")
    if "100vh" in h: E(f"interaktif '{tt}': jangan memakai 100vh (tampil sebagai blok di artikel)")
    for i, m in enumerate(re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", h, re.S | re.I)):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tf: tf.write(m.group(1)); p = tf.name
        r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
        if r.returncode: E(f"interaktif '{tt}': JavaScript tidak valid: {r.stderr.strip().splitlines()[-1][:120]}")
        os.unlink(p)
print(f"{f}: {len(qs)} soal, {len(segs)} rumus, {nver} terverifikasi, {len(inter)} web interaktif, bloom {dict(sorted(bloom.items()))}, dimensi {dict(dim)}, tipe {dict(types)}")
for m in err: print("  ✗", m)
print("LOLOS" if not err else f"GAGAL ({len(err)} pelanggaran)"); sys.exit(1 if err else 0)
