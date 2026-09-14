#!/usr/bin/env python3
"""Deterministic question plans — computed in code, never by the model.

A bab's question bank is 50 questions that must, together, hit a target
mix of subtype, Bloom level, difficulty and source section. Asking the
model for that mix per API call doesn't work once the bank is filled in
small chunks: each call rounds its own quota, and ten chunks of five
drift a long way from one plan for fifty.

So the plan is made here, once, as a list of SLOTS. Each generate call is
then told exactly which slots it must fill (`slots` in the request), and
the filler asks only for slots the database doesn't have yet — which is
also what makes an interrupted run resumable without re-generating
anything, and what keeps a failed chunk from costing more than itself.
"""

from collections import Counter

# Mirrors quiz_taxonomy.rs's bloom_weights / DIFFICULTY_WEIGHTS so the
# bank a bab gets matches what the quiz prompt asks for anyway.
STAGE_BLOOM = {
    "sd": [("c1", 20), ("c2", 35), ("c3", 30), ("c4", 15)],
    "smp": [("c1", 10), ("c2", 25), ("c3", 35), ("c4", 20), ("c5", 10)],
    "sma": [("c1", 5), ("c2", 20), ("c3", 35), ("c4", 25), ("c5", 10), ("c6", 5)],
    "kuliah": [("c2", 15), ("c3", 30), ("c4", 30), ("c5", 15), ("c6", 10)],
    "pascasarjana": [("c2", 5), ("c3", 20), ("c4", 35), ("c5", 25), ("c6", 15)],
    "umum": [("c1", 5), ("c2", 20), ("c3", 35), ("c4", 30), ("c5", 10)],
}
DIFFICULTY = [("mudah", 30), ("sedang", 50), ("sulit", 20)]

# What a bank is made of, per kind of subject (the bab plan's
# `jenis_soal`). `short_answer` matters where there is something to
# work out — a learner can pass pure multiple choice by elimination
# without ever doing the arithmetic. Where the answer is a concept, an
# exact-match short answer marks right answers wrong ("fotosintesis" vs
# "proses fotosintesis"), so multi-select carries the harder recall.
BANK_MIXES = {
    "hitungan": [("multiple_choice", 50), ("true_false", 20), ("short_answer", 30)],
    "konsep": [("multiple_choice", 55), ("true_false", 20), ("multiple_choice_multiple", 25)],
    "bahasa": [("multiple_choice", 50), ("true_false", 20), ("short_answer", 30)],
}
BANK_SUBTYPES = BANK_MIXES["hitungan"]
BANK_SIZE = 50

# The checkpoint pool per section. One subtype (and so one AI call per
# section): a 2-question comprehension check doesn't need variety as much
# as the Latihan does, and five extra calls per bab would cost more than
# the variety is worth.
CHECKPOINT_SUBTYPE = "multiple_choice"
CHECKPOINT_POOL = 4
CHECKPOINT_BLOOM = ["c1", "c2", "c2", "c3"]
CHECKPOINT_DIFFICULTY = ["mudah", "mudah", "sedang", "sedang"]


def _has_word(text, word):
    import re
    return re.search(rf"(?<![a-z0-9]){re.escape(word)}(?![a-z0-9])", text) is not None


def stage_of(level: str) -> str:
    """Same order as quiz_taxonomy::Stage::infer: an explicit jenjang
    wins, the Tahap number is only Matematika's fallback. Reading the
    number first sent SMA physics ("Tahap 2 — Mekanika (SMA)") as SMP."""
    low = (level or "").lower()
    if "pascasarjana" in low or _has_word(low, "s2") or _has_word(low, "s3") or "magister" in low or "doktor" in low:
        return "pascasarjana"
    if _has_word(low, "s1") or "kuliah" in low or "universitas" in low or "mahasiswa" in low or "perguruan tinggi" in low:
        return "kuliah"
    if any(_has_word(low, w) for w in ["cpns", "asn", "bumn", "skd", "skb", "twk", "tiu", "tkp", "ielts", "toefl", "toeic", "profesional", "dewasa", "umum"]):
        return "umum"
    if _has_word(low, "sma") or _has_word(low, "smk") or _has_word(low, "ma") or "utbk" in low or "snbt" in low:
        return "sma"
    if _has_word(low, "smp") or _has_word(low, "mts"):
        return "smp"
    if _has_word(low, "sd") or _has_word(low, "mi"):
        return "sd"
    for n, stage in [("1", "sd"), ("2", "smp"), ("3", "sma"), ("4", "kuliah"), ("5", "pascasarjana")]:
        if f"tahap {n}" in low:
            return stage
    return "sma"


def apportion(weights, total):
    """Largest remainder, same rule as quiz_taxonomy::apportion — the
    counts always add up to `total` exactly."""
    if total <= 0 or not weights:
        return [0] * len(weights)
    sum_w = sum(w for _, w in weights)
    exact = [(total * w) / sum_w for _, w in weights]
    counts = [int(x) for x in exact]
    remainder = total - sum(counts)
    order = sorted(range(len(weights)), key=lambda i: (-(exact[i] - counts[i]), i))
    for i in order[:remainder]:
        counts[i] += 1
    return counts


def _spread(values, total):
    """`values` repeated so each appears in proportion, as a flat list."""
    counts = apportion(values, total)
    out = []
    for (name, _), n in zip(values, counts):
        out.extend([name] * n)
    return out


def bank_blueprint(section_ids, level, size=BANK_SIZE, mix="hitungan"):
    """`size` slots: subtype × Bloom × difficulty × section, balanced on
    every axis. Deterministic — the same bab always gets the same plan,
    which is what lets a resumed run compare against what's stored."""
    slots = []
    subtypes = BANK_MIXES.get(mix, BANK_MIXES["hitungan"])
    per_subtype = apportion(subtypes, size)
    bloom_weights = STAGE_BLOOM[stage_of(level)]
    for (subtype, _), count in zip(subtypes, per_subtype):
        blooms = _spread(bloom_weights, count)
        difficulties = _spread(DIFFICULTY, count)
        for i in range(count):
            slots.append(
                {
                    "group_id": subtype_group(subtype),
                    "subtype": subtype,
                    "bloom": blooms[i],
                    "difficulty": difficulties[i],
                    # Round-robin so every section is tested by every
                    # subtype, instead of section 1 taking all the MCs.
                    "section_id": section_ids[i % len(section_ids)] if section_ids else None,
                }
            )
    return slots


def checkpoint_blueprint(section_id):
    return [
        {
            "group_id": "cp",
            "subtype": CHECKPOINT_SUBTYPE,
            "bloom": CHECKPOINT_BLOOM[i],
            "difficulty": CHECKPOINT_DIFFICULTY[i],
            "section_id": section_id,
        }
        for i in range(CHECKPOINT_POOL)
    ]


def subtype_group(subtype):
    return {"multiple_choice": "mc", "true_false": "tf", "short_answer": "sa", "multiple_choice_multiple": "mm"}[subtype]


def deficit(slots, existing):
    """Which planned slots aren't in the database yet.

    `existing` is what's actually stored — [(group_id, bloom, difficulty,
    section_id)] — read fresh before every chunk. A question the model
    labelled c3 when c4 was asked for still counts as the c3 slot it
    ended up being; the next chunk simply asks for what is still missing
    instead of re-generating the one that drifted. Nothing is ever
    regenerated to fix a label.
    """
    have = Counter(existing)
    missing = []
    for slot in slots:
        key = (slot["group_id"], slot["bloom"], slot["difficulty"], slot["section_id"])
        if have[key] > 0:
            have[key] -= 1
        else:
            missing.append(slot)
    # A question that exists but matches no planned slot (a drifted
    # label) still counts against the bank's size — otherwise the bank
    # would grow past 50 chasing exact labels.
    surplus = sum(have.values())
    return missing[: max(0, len(missing) - surplus)]


def chunks(slots, size=5):
    """Group the missing slots into calls: one call per (group, section)
    so each can reference exactly the section it is written from, capped
    at `size` questions — small enough that a truncated reply costs one
    chunk, not a whole bank."""
    buckets = {}
    for slot in slots:
        buckets.setdefault((slot["group_id"], slot["section_id"]), []).append(slot)
    out = []
    for (group_id, section_id), group_slots in buckets.items():
        for i in range(0, len(group_slots), size):
            out.append({"group_id": group_id, "section_id": section_id, "slots": group_slots[i : i + size]})
    return out


if __name__ == "__main__":
    sections = [f"s{i}" for i in range(1, 6)]
    for level in ["Tahap 1 — Matematika Dasar", "Tahap 2 — Mekanika (SMA)", "Tahap 5 — Fisika Tingkat Universitas", "Tahap 4 — Tes Wawasan Kebangsaan (TWK)"]:
        print(level, "->", stage_of(level))
    plan = bank_blueprint(sections, "Tahap 2 — Mekanika (SMA)", mix="konsep")
    print(f"{len(plan)} slot")
    print("subtype :", Counter(s["subtype"] for s in plan))
    print("bloom   :", Counter(s["bloom"] for s in plan))
    print("kesukaran:", Counter(s["difficulty"] for s in plan))
    print("bagian  :", Counter(s["section_id"] for s in plan))
    print("panggilan:", len(chunks(plan)))
