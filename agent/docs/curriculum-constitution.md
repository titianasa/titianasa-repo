# Curriculum Constitution — Grammar 11-Section Pattern

Status: **Accepted** (human-reviewed 2026-08-23, per P2-011)

This is the Constitution referenced by `ALR_Phase_Detail_Breakdown.md` 2.9
and 2.13: a fixed, mandatory pattern for every grammar lesson, used both as
the rail for the AI Curriculum Generation Agent (P2-013) and as the
checklist a human author is held to. It lives here — a file a human
reviews — rather than only inside a generator prompt, per 2.13's explicit
requirement.

## Applies to

Any lesson linked (via `lesson_concepts`) to at least one `concepts` row
with `type = 'grammar'`. A lesson with no grammar concept linked is not
held to this pattern (e.g. a pure vocabulary or pronunciation lesson).

## The 11 sections, in order

Every grammar lesson's content must contain a `heading` block for each of
these, identified by its numeric prefix — the heading text must start with
the two-digit number shown:

```
01 — What is it?      (penjelasan sederhana / simple explanation)
02 — Form              (e.g. Subject + have/has + V3)
03 — Positive          (e.g. I have finished my homework.)
04 — Negative          (e.g. I haven't finished my homework.)
05 — Question          (e.g. Have you finished your homework?)
06 — When to use it?   (penjelasan penggunaan / usage explanation)
07 — Signal words      (e.g. already, yet, just, ever, never, since, for)
08 — Common mistakes   (e.g. ❌ I have went there. → ✅ I have gone there.)
09 — Practice
10 — Speaking
11 — Writing
```

Sections must all be present; this document does not currently mandate a
specific order beyond the numbering itself (the validator only checks
presence, not sequence — see below).

## Why numeric-prefix matching, not keyword matching

An earlier draft of this validator considered matching on keywords (e.g.
does some heading contain "Form?"). That produces false positives — a
heading like "Formal greetings" would match "Form", and "Question words"
would match "Question" even in a lesson that isn't actually covering the
Constitution's "05 — Question" section as intended. Requiring the heading
text to literally start with the section's two-digit prefix ("05 — ...")
is unambiguous and matches how the format is written in practice (see the
block above).

## Enforcement

`service/curriculum_constitution.rs::validate_grammar_lesson` — checked at
`POST /lessons/{id}/submit-review` (P2-005) for any lesson linked to a
grammar concept. A lesson missing one or more sections is rejected with
`422 grammar_constitution_incomplete` and the response names exactly which
section(s) are missing, so an author doesn't have to guess.

This is a **submit-review gate**, not a draft-time restriction — an author
can save an incomplete draft freely while writing; the Constitution is only
enforced at the point where the lesson asks to move toward `published`.
