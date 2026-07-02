# How the audit maps onto the `rigorous-explainer` skill

Companion to [`audit-modules.md`](audit-modules.md). It takes each audit finding
and asks: **can this be encoded in the `rigorous-explainer` skill** (as a hardening
check, a template change, or a pedagogy-checklist rule) so future modules get it
automatically — or is it a one-off content/domain decision that the skill cannot
and should not own? **No skill files have been changed; this is the plan.**

Finding IDs (A1, B1, C-M2, …) refer to `audit-modules.md`.

---

## The meta-lesson

The three biggest cross-cutting problems — **A1** (literal `_` underscores in SVG
labels), **A2** (SVG label typography), **A3** (unflagged symbol collisions) — were
**already written rules** in the skill, yet they drifted into every module. Two
reasons: the rules were added *after* Modules 1–4 were built, and **nothing
mechanically enforced them.** Only the hardening scripts (`checktex`,
`check_overlap`, …) actually held the line.

> **Prose rules rot; only checks endure.** The highest-value skill improvement is
> not more prose — it is **converting the drift-prone mechanical rules into
> hardening checks.**

This reframes everything below.

---

## 1. Encode as hardening checks (strongest — turns rules into gates)

| Win | New / updated check | Why it works |
|---|---|---|
| **B1** malformed `viewBox` | `check_svg.py`: assert every `viewBox` has exactly 4 numeric values | Purely mechanical; caught a real rendering bug across ~11 figures; ~zero false positives |
| **A1** underscores / ASCII placeholders in labels | label linter: flag `_` and bare `theta/omega/Pi` inside `<text>` | Rule already exists in prose; a grep-level check makes it a gate |
| **A4** figures never referenced by number | advisory: warn if "Fig. k" never appears in prose | Cheap; advisory (some figures are purely illustrative) |
| **A6** disclosure-label consistency | advisory: flag mixed `<summary>` texts ("Answer" vs "solution") | Trivial grep; advisory (split may be intentional) |
| **D** file weight / heavy polylines | advisory: warn on >~120-point polylines or large file size | Mechanical; advisory |

These belong in `scripts/` and the step-6 hardening loop. **Spend here first.**

## 2. Encode in the template (new docs inherit it free)

- **A7 `prefers-reduced-motion`** — add a `@media (prefers-reduced-motion: reduce)`
  block that freezes SMIL. One-time, universal. **Strong yes.**
- **A2 SVG math typography** — *already done* (STIX CSS + `class="v"/"vb"`). The only
  gap is retrofitting existing modules, which a template cannot do retroactively.
- **A5 problem-set sub-nav** — ship a commented "problem-set skeleton" snippet
  (sub-TOC + back-to-top) for any doc with a large problem set.

## 3. Encode as pedagogy-checklist rules (general discipline, not domain facts)

Process patterns the audit proved recur — safe to generalize:

- **Quantify the punchline.** Every quantitative claim in prose — especially the
  motivational climax — must be backed by a shown computation or an explicit
  forward-ref. (M1's "several thousand newtons"; M2's asserted 45°/fracture claims.)
- **Uniform rigor.** Don't leave an *asserted* proposition beside fully-proved
  neighbours (M2 Prop 3.3; M2 neutral-axis step). If one result is derived, its
  siblings should be.
- **Exercise the whole governing law.** If you introduce a law with two halves, use
  both (M1 introduced `∑F=0` and never used it).
- **Problems span the spine, and every problem has a solution.** Strengthen the
  existing §8 (M2 had 3 solution-less problems; M3's computational set covered only
  one section).
- **Symbol-collision habit** (A3) — already present; add the concrete practice "keep
  a running single-letter symbol table; flag any letter reused, with a note," which
  the collision check (§1) assists.
- **Caption ↔ animation agreement** — extend the existing "figure and derivation
  must agree" rule (pillar 4) to "caption claims must match the animation's actual
  keyframes" (M1's bar-to-zero mismatch, B2).

## 4. Cannot / should not encode — and why

- **Domain rigor errors** — M3's *nonholonomic* mislabel, M4's Hertz-validity
  overselling, M2's tension-vs-compression bone strength, M3's 2.5W-vs-3W hip. The
  skill is **domain-agnostic**; it cannot verify mechanics facts, and baking physics
  into a general explainer skill is scope creep that would be wrong for the next
  topic. **These need a subject-matter / adversarial-domain reviewer, not the
  skill.**
- **Specific content additions** — "build out torsion," "compute the low-back
  number," "add a rule-of-mixtures bound," "sweep congruence not just modulus." These
  are *what to say*, decided by the author's grasp of the topic. The skill governs
  *how to build*, not *what is true*. Encoding them would over-fit to biomechanics.
- **A8 inter-module navigation** — the skill targets **single self-contained
  documents**; a "◀ prev · next ▶" rail is a property of a *multi-document series*
  (this course), not general to rigorous explainers. At most a one-line optional
  note; it must **not** become a default rule, or the template ships dead markup for
  the common single-doc case.
- **"Validate against a measured literature value" (M1, M3)** — half-encodable: it is
  *already* pillar 7, and the audit shows it under-applied, so **strengthening the
  reminder is worth it** — but the skill can only *prompt* it; it cannot supply the
  number or know one exists. Stays a checklist reminder, never a check.
- **B2 / B3 visual-semantics bugs** (caption says "to zero"; curve hidden under a
  gridline) — only *partly* mechanizable. B3 could extend `check_overlap` to flag a
  data polyline coincident with a same-position reference line, but it is heuristic
  and risks false positives; B2 needs semantic understanding. Best left as checklist
  reminders plus a modest optional `check_overlap` extension, not hard gates.

---

## Net recommendation (when ready to change the skill)

1. **Add `check_svg.py`** to the hardening loop: `viewBox` arity + label
   underscores/placeholders (+ optional advisories). *Single highest-leverage
   change* — it stops the exact drift that produced A1 and B1.
2. **Template:** add the `prefers-reduced-motion` block and a problem-set-skeleton
   snippet.
3. **`pedagogy-checklist.md`:** add the four process rules in §3
   (quantify-the-punchline, uniform-rigor, exercise-the-whole-law,
   problems-span-the-spine + always-a-solution).
4. **Leave alone:** all domain-specific substance and inter-module nav — author,
   reviewer, and project concerns, not skill concerns.

---

### Encodable-vs-not, at a glance

| Audit finding | Skill? | Vehicle |
|---|---|---|
| A1 label underscores | ✅ | check + (existing) rule |
| A2 SVG typography | ✅ done | template CSS |
| A3 symbol collisions | ◑ | rule + advisory check |
| A4 reference figs by number | ◑ | advisory check + rule |
| A5 problem-set sub-nav | ✅ | template snippet |
| A6 disclosure labels | ◑ | advisory check |
| A7 reduced-motion | ✅ | template CSS |
| A8 inter-module nav | ❌ | project-specific |
| B1 viewBox arity | ✅ | check |
| B2 caption↔animation | ◑ | rule (semantic) |
| B3 curve under gridline | ◑ | optional check extension |
| B4 nonholonomic mislabel | ❌ | domain review |
| C (all per-module substance) | ❌ | domain content |
| "validate vs literature" | ◑ | rule/prompt only |

✅ encode · ◑ partial (reminder/advisory) · ❌ out of scope
