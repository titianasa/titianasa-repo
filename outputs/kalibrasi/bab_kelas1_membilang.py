import json, uuid, random, re, os
from collections import Counter

random.seed(7)
S1, S2, S3, S4 = "a1f3c09d2b41", "b2e4d18c3a52", "c3d5e27b4c63", "d4c6f36a5d74"

def e(s, n):  # baris benda, dipisah tiap 5 agar mudah dihitung
    return " ".join("".join([s] * min(5, n - i)) for i in range(0, n, 5))

D, T, X = "diagnostik", "latihan_terarah", "latihan_mandiri"
K, R, P = "checkpoint_akhir", "remedial", "pengayaan"
F, Kn, Pr, Me = "faktual", "konseptual", "prosedural", "metakognitif"

Q = []

def mc(b, d, f, dim, s, stem, opts, ans, ex, m=None, verifikasi=None):
    Q.append(dict(t="mc", b=b, d=d, f=f, dim=dim, s=s, stem=stem, opts=opts, ans=ans, ex=ex, m=m, verifikasi=verifikasi))

def tf(b, d, f, dim, s, text, ans, ex, verifikasi=None):
    Q.append(dict(t="tf", b=b, d=d, f=f, dim=dim, s=s, stem=text, ans=ans, ex=ex, verifikasi=verifikasi))

def sa(b, d, f, dim, s, stem, ans, ex, verifikasi=None):
    Q.append(dict(t="sa", b=b, d=d, f=f, dim=dim, s=s, stem=stem, ans=ans, ex=ex, verifikasi=verifikasi))

# ── C1 MUDAH (5 soal: 2 diagnostik, 3 terarah) ─────────────────────────────
# Diagnostik (2)
mc("c1", "mudah", D, F, S2, "Angka ini dibaca apa? 7", ["tujuh", "lima", "sembilan", "tiga"], "A", "Angka 7 dibaca tujuh.")
tf("c1", "mudah", D, F, S2, "Angka 3 dibaca lima.", "Salah", "Angka 3 dibaca tiga, bukan lima.")

# Terarah (3): S1, S2, S1
mc("c1", "mudah", T, F, S1, f"Berapa banyak? {e('🍎', 3)}", ["2", "3", "4", "5"], "B", "Ada tiga apel. Kita menghitung: 1, 2, 3.", verifikasi={"ekspresi": "3", "hasil": "3"})
mc("c1", "mudah", T, F, S2, "Setelah angka 4 ada angka ....", ["3", "6", "5", "2"], "C", "Urutannya 1, 2, 3, 4, 5. Setelah 4 ada 5.", verifikasi={"ekspresi": "4+1", "hasil": "5"})
sa("c1", "mudah", T, F, S1, f"Berapa banyak? {e('⭐', 6)}", "6|enam", "Hitung satu per satu. Angka terakhir 6.", verifikasi={"ekspresi": "6", "hasil": "6"})

# ── C2 MUDAH (8 soal: 2 diagnostik, 2 remedial, 4 terarah) ──────────────────
# Diagnostik (2)
mc("c2", "mudah", D, Kn, S1, "Membilang artinya ....", ["menyebut angka berurutan", "menggambar benda", "menulis nama", "melompat"], "A", "Membilang adalah menghitung dengan menyebut angka berurutan.")
tf("c2", "mudah", D, Pr, S1, "Saat membilang, kita menunjuk tiap benda.", "Benar", "Menunjuk membantu kita tidak lupa dan tidak dua kali.")

# Remedial (2)
mc("c2", "mudah", R, Kn, S1, f"Budi menghitung {e('🐟', 4)}: 1, 2, 3, 4. Berapa ikan?", ["4, angka terakhir", "1, angka pertama", "10, angka terbesar", "2, angka tengah"], "A", "Angka terakhir yang disebut menunjukkan banyak benda. Jadi ada 4 ikan.", "Angka pertama dianggap sebagai banyak benda", verifikasi={"ekspresi": "4", "hasil": "4"})
mc("c2", "mudah", R, F, S2, "Angka ini 9. Dibaca ....", ["sembilan", "enam", "delapan", "tujuh"], "A", "Angka 9 dibaca sembilan. Angka 6 dibaca enam.", "Angka 6 dan 9 tertukar")

# Terarah (4): S3, S3, S2, S2
mc("c2", "mudah", T, Kn, S3, f"Angka yang cocok untuk {e('🍌', 2)} adalah ....", ["2", "3", "1", "4"], "A", "Ada dua pisang. Angkanya 2.", verifikasi={"ekspresi": "2", "hasil": "2"})
mc("c2", "mudah", T, Kn, S3, "Kartu angka 5 cocok dengan ....", [e('🚗', 3), e('🚗', 4), e('🚗', 5), e('🚗', 6)], "C", "Kartu 5 cocok dengan lima mobil.")
tf("c2", "mudah", T, Kn, S2, f"Angka 5 cocok dengan {e('🐱', 4)}.", "Salah", "Ada empat kucing, jadi angka 5 tidak cocok.")
sa("c2", "mudah", T, F, S2, f"Tulis angkanya: {e('🎈', 7)}", "7|tujuh", "Ada tujuh balon. Angkanya 7.", verifikasi={"ekspresi": "7", "hasil": "7"})

# ── C3 MUDAH (2 soal: 2 terarah) ──────────────────────────────────────────
# Terarah (2): S4, S2
mc("c3", "mudah", T, Pr, S4, f"Kita menghitung {e('🍓', 6)}. Mulai dari mana?", ["menunjuk satu sambil bilang 1", "langsung bilang 6", "bilang 10", "menutup mata"], "A", "Mulai dari satu stroberi. Tunjuk sambil bilang 1.")
mc("c3", "mudah", T, Kn, S2, "Ina punya 8 kelereng. Kartu angkanya ....", ["6", "7", "8", "9"], "C", "Delapan kelereng cocok dengan kartu 8.", verifikasi={"ekspresi": "8", "hasil": "8"})

# ── C3 SEDANG (12 soal: 4 checkpoint, 2 remedial, 6 terarah) ──────────────
# Checkpoint akhir (4)
mc("c3", "sedang", K, Pr, S1, f"Berapa banyak? {e('🌸', 9)}", ["7", "8", "9", "10"], "C", "Hitung satu per satu sampai akhir. Angka terakhir 9.", verifikasi={"ekspresi": "9", "hasil": "9"})
mc("c3", "sedang", K, Kn, S3, "Kartu 7 cocok dengan ....", [e('✏️', 6), e('✏️', 7), e('✏️', 8), e('✏️', 5)], "B", "Tujuh pensil cocok dengan kartu 7.")
mc("c3", "sedang", K, Pr, S1, f"Berapa banyak? {e('🥕', 10)}", ["8", "9", "10", "5"], "C", "Ada dua baris lima. Semua ada sepuluh.", verifikasi={"ekspresi": "5*2", "hasil": "10"})
tf("c3", "sedang", K, Pr, S1, f"{e('🐦', 6)} Ada 7 burung.", "Salah", "Kita hitung: ada 6 burung, bukan 7.")

# Remedial (2)
mc("c3", "sedang", R, Me, S4, f"Tio menghitung {e('🍊', 5)} bilang 6. Salahnya apa?", ["Satu jeruk dihitung dua kali", "Jeruknya kurang", "Angkanya terlalu kecil", "Tidak ada yang salah"], "A", "Ada 5 jeruk. Tio menghitung satu jeruk dua kali.", "Menghitung benda dua kali")
mc("c3", "sedang", R, Me, S4, f"Dina menghitung {e('⚽', 7)} bilang 6. Salahnya apa?", ["Satu bola terlewat", "Bolanya terlalu banyak", "Angkanya terlalu besar", "Tidak ada yang salah"], "A", "Ada 7 bola. Dina melewatkan satu bola.", "Benda terlewat saat dihitung")

# Terarah (6): S2, S4, S3, S3, S1, S1
mc("c3", "sedang", T, Kn, S2, "Kartu angka untuk 9 buku adalah ....", ["7", "8", "9", "10"], "C", "Sembilan buku cocok dengan kartu 9.", verifikasi={"ekspresi": "9", "hasil": "9"})
mc("c3", "sedang", T, Pr, S4, f"Agar tidak salah hitung {e('🐸', 8)}, kita ....", ["menunjuk atau mencoret tiap katak", "menebak saja", "menghitung cepat sekali", "menghitung dua kali tiap katak"], "A", "Menunjuk atau mencoret membuat tiap katak terhitung satu kali.")
mc("c3", "sedang", T, Kn, S3, f"Nia punya {e('🍬', 10)}. Angka yang cocok ....", ["9", "10", "5", "1"], "B", "Sepuluh permen cocok dengan angka 10.", verifikasi={"ekspresi": "10", "hasil": "10"})
tf("c3", "sedang", T, Kn, S3, f"Angka 8 cocok dengan {e('🐢', 9)}.", "Salah", "Kura-kura ada 9. Angka 8 tidak cocok.")
tf("c3", "sedang", T, Kn, S1, "Angka terakhir menunjukkan banyak benda.", "Benar", "Benar. Angka terakhir menunjukkan banyaknya.")
sa("c3", "sedang", T, Pr, S1, f"Berapa banyak? {e('🌟', 8)}", "8|delapan", "Hitung satu per satu. Angka terakhir 8.", verifikasi={"ekspresi": "8", "hasil": "8"})

# ── C4 SEDANG (10 soal: 3 checkpoint, 7 terarah) ───────────────────────────
# Checkpoint akhir (3)
mc("c4", "sedang", K, Kn, S3, f"Kartu mana cocok untuk {e('🐟', 3)} bukan {e('🐟', 4)}?", ["3", "4", "5", "2"], "A", "Tiga ikan cocok dengan kartu 3. Empat ikan cocok dengan 4.", verifikasi={"ekspresi": "3", "hasil": "3"})
mc("c4", "sedang", K, Pr, S4, "Rudi membilang 1, 2, 3, 5, 6. Yang terlewat ....", ["angka 4", "angka 6", "angka 2", "tidak ada"], "A", "Urutan yang benar 1, 2, 3, 4, 5, 6. Angka 4 terlewat.", verifikasi={"ekspresi": "4", "hasil": "4"})
tf("c4", "sedang", K, Kn, S3, f"{e('🍎', 5)} dan {e('🍐', 5)} cocok dengan angka sama.", "Benar", "Kedua kelompok ada lima. Angkanya sama: 5.")

# Terarah (7): S3, S4, S2, S1, S4, S3, S4
mc("c4", "sedang", T, Kn, S3, f"Mana yang angkanya sama dengan {e('🐶', 6)}?", [e('🐱', 5), e('🐱', 6), e('🐱', 7), e('🐱', 4)], "B", "Anjing ada 6. Kucing yang ada 6 juga.")
mc("c4", "sedang", T, Pr, S4, f"Ada {e('🎈', 10)}. Cara menghitung paling rapi ....", ["mencoret tiap balon", "menebak", "menghitung dari tengah", "menghitung dua kali"], "A", "Mencoret tiap balon membantu kita tidak lupa.")
mc("c4", "sedang", T, Kn, S2, "Kartu angka cocok untuk 🚌🚌🚌🚌 adalah ....", ["4", "3", "2", "5"], "A", "Ada 4 bus. Kartu yang cocok adalah 4.", verifikasi={"ekspresi": "4", "hasil": "4"})
mc("c4", "sedang", T, Kn, S1, "Aku berhitung sampai 5. Banyak bendanya ada ....", ["1", "3", "5", "10"], "C", "Angka terakhir yang disebut adalah banyaknya.", verifikasi={"ekspresi": "5", "hasil": "5"})
tf("c4", "sedang", T, Pr, S4, f"Menghitung {e('🌷', 7)} dua kali hasilnya harus sama.", "Benar", "Jika kita teliti, hasilnya sama setiap kali.")
tf("c4", "sedang", T, Kn, S3, f"Angka 5 cocok dengan {e('🐸', 6)}.", "Salah", "Katak ada 6, jadi angka 5 tidak cocok.")
sa("c4", "sedang", T, Pr, S4, f"Berapa banyak? {e('🍪', 9)}", "9|sembilan", "Hitung dengan teliti. Ada sembilan kue.", verifikasi={"ekspresi": "9", "hasil": "9"})

# ── C5 SEDANG (3 soal: 3 checkpoint) ──────────────────────────────────────
mc("c5", "sedang", K, Me, S4, f"Dita membilang {e('🍇', 7)} dapat 7. Cara mengeceknya ....", ["menghitung sekali lagi", "langsung yakin", "menghapus jawaban", "menebak"], "A", "Menghitung lagi adalah cara mengecek jawaban.")
mc("c5", "sedang", K, Kn, S3, f"Pasangan yang benar untuk {e('🐦', 4)} adalah ....", ["angka 4", "angka 5", "angka 3", "angka 1"], "A", "Empat burung cocok dengan angka 4.", verifikasi={"ekspresi": "4", "hasil": "4"})
mc("c5", "sedang", K, Me, S4, f"Andi bilang ada 6 {e('⭐', 5)}. Mana yang benar?", ["Andi salah, ada 5", "Andi benar", "Ada 4", "Ada 1"], "A", "Bintangnya ada 5. Andi salah hitung.", verifikasi={"ekspresi": "5", "hasil": "5"})

# ── C3 SULIT (2 soal: 2 mandiri) ──────────────────────────────────────────
mc("c3", "sulit", X, Pr, S4, f"Ada {e('🍒', 10)}. Cara hitung cepat dan benar ....", ["hitung tiap baris lima, lalu semua", "tebak saja", "hitung satu baris saja", "tidak usah dihitung"], "A", "Dua baris lima membuat semuanya sepuluh.")
sa("c3", "sulit", X, Pr, S1, f"Berapa banyak? {e('🌼', 10)}", "10|sepuluh", "Ada dua baris lima. Semua ada sepuluh.", verifikasi={"ekspresi": "5+5", "hasil": "10"})

# ── C4 SULIT (3 soal: 3 mandiri) ──────────────────────────────────────────
mc("c4", "sulit", X, Kn, S3, "Di antara pilihan, mana pasangan yang salah?", ["🐟-3", "🐟🐟-2", "🐟🐟🐟-3", "🐟🐟🐟🐟-4"], "A", "Satu ikan seharusnya cocok dengan 1, bukan 3.")
mc("c4", "sulit", X, Pr, S4, f"Mana hasil membilang {e('🐝', 8)} yang tepat?", ["8", "6", "10", "7"], "A", "Hitung dengan teliti. Ada delapan lebah.", verifikasi={"ekspresi": "8", "hasil": "8"})
tf("c4", "sulit", X, Me, S4, "Saat ragu, kita boleh menghitung sekali lagi.", "Benar", "Menghitung lagi membantu memeriksa jawaban.")

# ── C5 SULIT (3 soal: 3 mandiri) ──────────────────────────────────────────
mc("c5", "sulit", X, Me, S4, "Mira membilang 6, Toni 7. Yang tepat ....", ["hitung bersama lagi", "Mira pasti benar", "Toni pasti benar", "tebak saja"], "A", "Hitung lagi bersama dan bandingkan dulu.")
mc("c5", "sulit", X, Kn, S3, f"Kartu paling tepat untuk {e('🐱', 6)} adalah ....", ["angka 6", "angka 5", "angka 7", "angka 9"], "A", "Enam kucing cocok dengan angka 6.", verifikasi={"ekspresi": "6", "hasil": "6"})
mc("c5", "sulit", X, Me, S4, "Yang bukan cara mengecek hitungan adalah ....", ["menebak", "menghitung lagi", "menunjuk tiap benda", "mencoret benda"], "A", "Menebak bukan cara mengecek.")

# ── C6 SULIT (2 soal: 2 pengayaan) ────────────────────────────────────────
mc("c6", "sulit", P, Kn, S3, "Kartu tepat untuk 7 topi memuat ....", ["angka 7 dan 7 topi", "angka 5", "gambar 9 topi", "kartu kosong"], "A", "Kartu yang tepat memuat angka 7 dan tujuh topi.", verifikasi={"ekspresi": "7", "hasil": "7"})
mc("c6", "sulit", P, Pr, S4, "Mengajari adik menghitung 6 bola. Langkah pertama ....", ["menunjuk satu bola, bilang 1", "bilang 6", "bilang 10", "bermain"], "A", "Mulai dari satu bola. Tunjuk sambil bilang 1.")

assert len(Q) == 50, f"Total soal: {len(Q)}"

# Validasi stem length <= 12 kata
for i, q in enumerate(Q):
    wcnt = len(q["stem"].split())
    assert wcnt <= 12, f"Stem Q#{i+1} terlalu panjang ({wcnt} kata): {q['stem']}"

# Distribusi taxonomy
c_b = Counter(q["b"] for q in Q)
c_d = Counter(q["d"] for q in Q)
c_f = Counter(q["f"] for q in Q)
c_dim = Counter(q["dim"] for q in Q)
c_t = Counter(q["t"] for q in Q)

print("Bloom:", dict(c_b))
print("Difficulty:", dict(c_d))
print("Fungsi:", dict(c_f))
print("Dimensi:", dict(c_dim))
print("Tipe:", dict(c_t))

# Hitung latihan per section
latihan_sec = Counter(q["s"] for q in Q if q["f"] in ("latihan_terarah", "checkpoint_bagian"))
print("Latihan per section (min 4):", dict(latihan_sec))
for sec_id, count in latihan_sec.items():
    assert count >= 4, f"Bagian {sec_id} hanya punya {count} latihan, minimum 4!"

uid = lambda i: str(uuid.uuid5(uuid.NAMESPACE_DNS, f"k1_bab1_soal_{i}"))
groups = {"mc": [], "tf": [], "sa": []}

random.seed(42)
for idx, q in enumerate(Q):
    tax = {
        "bloom": q["b"],
        "difficulty": q["d"],
        "fungsi": q["f"],
        "knowledge_dimension": q["dim"]
    }
    if q.get("m"):
        tax["miskonsepsi_target"] = q["m"]
    base = {
        "uid": uid(idx),
        "answer": q["ans"],
        "taxonomy": tax,
        "explanation": q["ex"],
        "source_section_id": q["s"]
    }
    if q.get("verifikasi"):
        base["verifikasi"] = q["verifikasi"]
    if q["t"] == "mc":
        opts = list(q["opts"])
        ans_text = opts[ord(q["ans"]) - 65]
        random.shuffle(opts)
        label = "ABCD"[opts.index(ans_text)]
        base.update(
            stem=q["stem"],
            answer=label,
            choices=[{"label": "ABCD"[i], "text": o} for i, o in enumerate(opts)]
        )
        groups["mc"].append(base)
    elif q["t"] == "tf":
        base["text"] = q["stem"]
        groups["tf"].append(base)
    else:
        base["stem"] = q["stem"]
        groups["sa"].append(base)

n = 0
qg = []
for gid, typ, ins, extra in (
    ("mc", "multiple_choice", "Pilih jawaban yang paling tepat.", {}),
    ("tf", "true_false", "Tentukan benar atau salah.", {"options": ["Benar", "Salah"]}),
    ("sa", "short_answer", "Jawab singkat dengan satu angka atau satu kata.", {})
):
    for x in groups[gid]:
        n += 1
        x["number"] = n
    qg.append({
        "type": typ,
        "group_id": gid,
        "instruction": ins,
        "questions": groups[gid],
        "ai_meta": {"draft": True},
        **extra
    })

secs = [
    ("Menghitung Benda Satu per Satu", S1),
    ("Membaca dan Menulis Angka", S2),
    ("Mencocokkan Benda dengan Angka", S3),
    ("Menghitung dengan Teliti", S4)
]

quiz = {
    "level": "Kelas 1 SD — Fase A",
    "sections": [{"title": t, "section_id": i} for t, i in secs],
    "passing_score": 70.0,
    "shuffle_choices": True,
    "shuffle_question_order": True,
    "question_groups": qg
}

# Materi
mat = [
    (S1, "Aku bisa menghitung benda satu per satu.", "Menghitung Benda Satu per Satu",
f"""Ayo berhitung! Menghitung disebut **membilang**.

Lihat kucing ini: {e('🐱', 3)}

Kita tunjuk satu kucing. Kita bilang **satu**. Tunjuk lagi. Bilang **dua**. Tunjuk lagi. Bilang **tiga**.

Ada **tiga** kucing.

:::definition
term: Membilang
definition: Menyebut angka satu per satu untuk menghitung benda.
:::

:::callout
variant: tip
title: Ingat ya
text: Angka terakhir yang kamu sebut adalah banyak bendanya.
:::""", 3),

    (S2, "Aku bisa membaca dan menulis angka 1 sampai 10.", "Membaca dan Menulis Angka",
f"""Setiap angka punya nama.
Setiap angka punya lambang.

:::table
headers: ["Angka","Dibaca","Banyak"]
rows: [["1","satu","{e('🍎', 1)}"],["2","dua","{e('🍎', 2)}"],["3","tiga","{e('🍎', 3)}"],["4","empat","{e('🍎', 4)}"],["5","lima","{e('🍎', 5)}"]]
caption: Angka 1 sampai 5
:::

Ada angka 6 sampai 10.
Ayo kita baca bersama.
Enam, tujuh, delapan, sembilan, sepuluh.
Kita tulis lambangnya: 6, 7, 8, 9, 10.""", 4),

    (S3, "Aku bisa mencocokkan banyak benda dengan angka.", "Mencocokkan Benda dengan Angka",
f"""Setiap kelompok benda punya satu angka.

{e('🚗', 4)} punya angka **4**.

{e('🚗', 6)} punya angka **6**.

:::steps
title: Cara mencocokkan
items: ["Hitung bendanya satu per satu.","Ingat angka terakhir.","Ambil kartu angka yang sama."]
:::

Contoh: {e('🌸', 5)}. Kita hitung: 1, 2, 3, 4, 5. Kartunya **5**.""", 4),

    (S4, "Aku bisa menghitung dengan teliti dan mengecek hasilku.", "Menghitung dengan Teliti",
f"""Agar tidak salah, hitung dengan teliti.
Tunjuk tiap benda dengan tenang.

:::steps
title: Menghitung teliti
items: ["Tunjuk atau coret tiap benda.","Jangan ada yang terlewat.","Jangan hitung dua kali.","Hitung lagi untuk mengecek."]
:::

:::common_trap
term: Menghitung Benda Dua Kali atau Terlewat
explanation: Jangan lewatkan benda. Jangan hitung dua kali. Coret tiap benda agar aman.
:::

:::callout
variant: summary
title: Ringkasan
text: Membilang adalah menghitung benda berurutan. Angka terakhir adalah banyak bendanya.
:::""", 3),
]

lp = {
    "level": "Kelas 1 SD — Fase A",
    "title": "Membilang dan Mencocokkan Benda dengan Bilangan",
    "topic": "Bilangan sampai 20",
    "language": "id",
    "sections": [{"id": i, "goal": g, "title": t, "content": c, "minutes": m} for i, g, t, c, m in mat]
}

# Verifikasi metrik materi
for i, s in enumerate(lp["sections"]):
    raw_words = s["content"].split()
    assert len(raw_words) <= 120, f"Section {i+1} melebihi 120 kata ({len(raw_words)} kata)"
    # Clean directives for sentence analysis
    clean = re.sub(r':::[a-z_]+.*?(?:\n.*?)*?:::', '', s["content"], flags=re.DOTALL)
    sentences = [sent.strip() for sent in re.split(r'[.!?\n]+', clean) if sent.strip()]
    lens = [len(sent.split()) for sent in sentences]
    if lens:
        avg = sum(lens) / len(lens)
        mx = max(lens)
        assert avg <= 6.0, f"Section {i+1} avg sentence len > 6 ({avg:.1f})"
        assert mx <= 10, f"Section {i+1} max sentence len > 10 ({mx})"

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_bab_kelas1.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"lesson_plan": lp, "quiz_config": quiz}, f, ensure_ascii=False, indent=2)

print("BERHASIL:", out_path, "berhasil dibuat dan divalidasi!")
