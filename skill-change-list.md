# Proposed changes to the `rigorous-explainer` skill

Concrete, actionable change list, grouped by which skill file each touches. Drawn
from [`audit-modules.md`](audit-modules.md) and
[`skill-improvements-from-audit.md`](skill-improvements-from-audit.md). IDs like
**A1 / B1** refer to findings in `audit-modules.md`.

> **Status: PLAN ONLY. No skill files have been changed.** This document is the
> backlog; each item is a proposed edit awaiting go-ahead.

Skill location: `C:\Users\simon\.claude\skills\rigorous-explainer\`
(`SKILL.md`, `assets/template.html`, `scripts/*.py`, `references/*.md`).

---

## 1. New script — `scripts/check_svg.py` (+ add to the hardening loop)

The single highest-leverage change: convert drift-prone written rules into a gate.

1. **`viewBox` arity** — fail if any `viewBox` has ≠ 4 numeric values. *(B1: the
   `"0 0 0 0 440 240"` bug on ~11 Module-4 figures.)*
2. **Literal underscores in `<text>`** — fail on `_` inside SVG label text. *(A1.)*
3. **ASCII math placeholders in `<text>`** — fail on bare `theta`, `omega`, `Pi`,
   `lambda`, `sqrt`, `^`, etc. in labels. *(A1; the figures-ref "never leave ASCII
   placeholders" rule.)*
4. **(advisory) Figures never cited by number** — warn if "Fig. N" never appears in
   prose. *(A4.)*
5. **(advisory) Mixed `<summary>` labels** — warn on both "Answer" and
   "solution"/"Show solution" in one file. *(A6.)*
6. **(advisory) Heavy figures** — warn on polylines > ~120 points or oversized
   files. *(D: M3 ≈ 311 KB.)*

## 2. `SKILL.md`

7. Add `check_svg.py` to the **step-6 hardening loop** (command block + scripts
   quick-reference table).
8. Under **step 4 (Visualize):** one line each — "reference every figure by its
   number" and "guard animations with reduced-motion" (points to template +
   checklist).

## 3. `assets/template.html`

9. **`prefers-reduced-motion` guard for SMIL.** CSS alone cannot pause SMIL — ship a
   tiny JS snippet that calls `svg.pauseAnimations()` when
   `matchMedia('(prefers-reduced-motion: reduce)')` matches, freezing to frame 0.
   *(A7.)*
10. **Problem-set skeleton snippet** (commented) — a sub-TOC linking
    `#conceptual/#derivational/#computational` + a per-group "↑ contents" and
    optional "expand/collapse all solutions." *(A5.)*
11. *(Already shipped this session — listed for completeness, no action:)* the
    figure CSS counter ("Fig. N"), the STIX SVG-math typography + `class="v"/"vb"`
    *(A2)*.

## 4. `references/pedagogy-checklist.md` (new / strengthened discipline rules)

12. **Quantify the punchline** — every quantitative prose claim, especially the
    motivational climax, must be backed by a shown computation or an explicit
    forward-ref. *(M1 low-back; M2 45°/fracture.)*
13. **Uniform rigor** — no *asserted* proposition sitting beside fully-proved
    neighbours; derive siblings to the same standard. *(M2 Prop 3.3, neutral-axis
    step.)*
14. **Exercise the whole governing law** — if you introduce a law with two halves,
    use both. *(M1's unused `∑F=0`.)*
15. **Strengthen §8 (problem sets)** — computational problems must span the *whole
    spine*, not just the lab; every problem and diagnostic carries a solution. *(M2
    3 solution-less problems; M3 K-set covers only §7.)*
16. **Caption ↔ animation agreement** — extend pillar 4's "figure and derivation
    must agree" to "caption claims must match the animation's actual keyframes."
    *(M1 bar-to-zero, B2.)*
17. **Reference figures by number** — pairs with the auto-numbering feature. *(A4.)*
18. **Reduced-motion accessibility** — checklist line paired with the template
    guard. *(A7.)*
19. **Strengthen pillar 1 symbol-collision habit** — keep a running single-letter
    symbol table; flag any reuse with an in-text note (the new check assists).
    *(A3.)*
20. **Strengthen pillar 7** — make "validate against a measured literature value
    where one exists" an explicit per-section prompt (currently under-applied).
    *(M1, M3.)*

## 5. `references/figures-and-animation.md`

21. Add the **`viewBox` arity pitfall** ("0 0 0 0 W H" reads plausible but is
    invalid) as a documented gotcha, cross-referencing `check_svg.py`.
22. *(Optional, heuristic)* note a possible **`check_overlap.py` extension**: flag a
    data polyline coincident with a same-position, same-colour reference line — but
    mark it advisory/false-positive-prone, not a hard gate. *(B3.)*

## 6. Explicitly NOT to encode (and why)

23. **Domain rigor facts** (M3 nonholonomic; M4 Hertz validity; M2
    tension-vs-compression; M3 2.5W-vs-3W) — the skill is domain-agnostic; these
    need a subject-matter reviewer, not a general rule.
24. **Specific content additions** (build torsion, compute low-back, add
    rule-of-mixtures) — *what to say*, not *how to build*.
25. **Inter-module prev/next nav (A8)** — the skill targets single self-contained
    docs; must not become a default (would ship dead markup). At most a one-line
    "optional for a series" note.
26. **Hard gate on symbol collisions** — too context-dependent; advisory only
    (item 19), not pass/fail.

---

## Suggested implementation order

1. **`check_svg.py`** (items 1–6) + wire into `SKILL.md` (item 7). *Stops the exact
   drift that produced A1 and B1.*
2. **Template** (items 9–10).
3. **`pedagogy-checklist.md`** (items 12–20).
4. **`figures-and-animation.md`** (items 21–22).

## Note on scope

These changes improve the skill for **future** documents. They do **not**
retroactively fix Modules 1–4 — that is a separate content pass (see
`audit-modules.md`), except where a new check (item 1) would now *flag* the existing
defects on the next hardening run.
