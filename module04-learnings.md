# Module 4 — Build Learnings & Playbook

*Cartilage, Synovial Fluid, and Joint Contact Biophysics. Written after completing
§0–§9 (with the 30-problem §9) + Appendix. This is the durable record of **how** the
module was built, what broke, and what to reuse for the next figure-heavy module.*

---

## 0. TL;DR — the five things that mattered most

1. **Split the figure work into a *generator* (computes plot geometry → JSON) and an
   *assembler* (holds all prose/solutions, splices figures in).** This made a
   30-figure section tractable and every fix cheap.
2. **`check_overlap.py` is not optional.** It found **12** label/curve collisions
   across the 30 figures that had passed the eye in previews. Never eyeball a plot
   for overlaps.
3. **Figures and prose cross-check each other.** Writing a derivation caught a wrong
   exponent *in the figure* (`R^(−1/3)` → `R^(−2/3)`); the overlap checker caught a
   curve clipping the axis. Build both and let them audit each other.
4. **Get one representative figure per family approved before mass-producing.**
   Approved *primitives* (gradients, arrowheads) ≠ approved *compositions*. The
   three-figure sign-off is one cheap round-trip against a 30-figure redo.
5. **Raw strings for anything with LaTeX.** `"\tau"` is a tab; `"\nu"` a newline;
   `"\varepsilon"` a vertical tab. Author every math-bearing Python string as `r"""…"""`.

---

## 1. The figure pipeline (the core reusable asset)

Three scratchpad scripts, run in order. They are session-transient; the durable
output is the HTML. Regenerate from this pattern for any figure-heavy module.

| Script | Role | Output |
|---|---|---|
| `gen9.py` | a small `P` plot helper + one function per **computed** figure | `svg9.json` (figure bodies), `nums9.json` (verified numbers) |
| `schem9.py` | hand-authored **Tier-2 / schematic** figure bodies | `schem9.json` |
| `assemble9.py` | all 30 problem statements + solutions; pulls figure bodies from the JSONs and **splices** the block into the HTML | edits `module04.html` |

### The `P` plot helper (in `gen9.py`)
A tiny class with `X(x)/Y(y)` data→pixel mappers (linear or log), plus
`frame/grid/curve/vline/dot/tx`. Every figure function builds its body with these
and calls `store(key, p, aria)`; `store` wraps the body in `<svg class="setupfig">`.
Key point: **compute the curve, then place labels relative to the computed curve** —
never hand-guess a y-coordinate.

### The assembler is *idempotent*
`assemble9.py` finds the region between two literal markers
(`<h3>Problems</h3>` … `<p>That closes…`) and replaces it. Re-running after any
figure tweak re-splices cleanly. This is why the 12 overlap fixes stayed cheap: edit
`gen9.py`, regenerate JSON, re-run the assembler, re-check — never 30 hand-edits.
Back up the target file first (`cp module04.html module04.baseline.html`) because the
working-tree baseline may be uncommitted and unrecoverable by git.

### Reuse approved figures verbatim
The C1/D1 seed figures came from the approved sign-off preview
(`trio_preview.html`); the assembler extracts their `<svg>…</svg>` by splitting on
`<figure>` rather than redrawing them. Approved art should be *reused*, not recreated.

---

## 2. Two figure tiers — decide by content, not by section

- **Physics / quantitative → flat, but computed.** F(t) curves, stress-relaxation,
  Stribeck, Hertz pressure profiles, eigenmodes, τ-vs-h — all Tier-1 flat schematics,
  but every point comes from the model (`Fseries`, Hertz formulas, cosine modes), not
  a sketch. ~17 of the 30 figures.
- **Real-entity → Tier-2 shaded.** Cartilage-on-bone, confined plugs, the Donnan
  brush, the OA feedback loop — shaded capsule/gradient primitives from the shared
  `<defs>` (`b_bone/b_sph/b_cart/b_sh/a_red/a_blu/a_grn/a_mus/b_brush`). ~11 figures.
- **Arrows are always slim.** Thin shaft + small sharp head; heavier load → thicker
  *shaft*, same head. Never a fat triangle/wedge (the rejected §0 "load triangle").
- **SVG `<text>` uses Unicode, never `$…$`** (MathJax doesn't typeset inside SVG).
  Subscripts/superscripts via Unicode or `<tspan baseline-shift>`. In normal HTML
  (e.g. the Appendix tables) `$…$` is fine and preferred.

---

## 3. The hardening loop — what each check actually catches

Run **all five after every edit pass**; all must reach 0 (stray-$ ~6 is advisory).

```
S=C:/Users/simon/.claude/skills/rigorous-explainer/scripts
python $S/checktex.py     module04.html   # $/$$ + brace/\begin-end/\boxed balance
python $S/checklt.py      module04.html   # literal <,> inside math
python $S/check_links.py  module04.html   # #id links resolve; unlinked §refs
python $S/verify_dom.py   module04.html   # headless Chrome: mjx-merror, stray $, links
python $S/check_overlap.py module04.html  # headless Chrome: text over curve/dashed line
```

- **`check_overlap.py` is the enforcer.** It geometrically tests every figure
  `<text>` against every `<polyline>` (curve) and long dashed reference line, handling
  rotation/scale. It excludes solid lines (axes, arrows, leaders) and short dashes
  (legend swatches) — so leaders and legends are *safe fixes*. When it flags a label
  it prints the box + the hit point; reposition data-aware and re-run to 0.
- **`verify_dom`'s `0 mjx-merror` is the proof that the math rendered** — `checktex`
  only proves delimiters balance. Verify the DOM, never a screenshot (MathJax is async;
  screenshots go blank mid-typeset).

---

## 4. Bugs this process caught (and which check caught them)

| Bug | How it surfaced | Fix |
|---|---|---|
| Hertz peak labelled `p₀ ∝ R^(−1/3)` | writing the **D7 derivation** (correct is `R^(−2/3)`) | fix the figure label |
| p₀ curve ran off the top of the d7 axis | `check_overlap` flag + preview | rescale `/6`, not `/4` |
| Every y-axis **title** rendered horizontal and clipped | **preview render** | rotate any `<text>` with `x<32` (post-process) |
| 12 labels sitting on curves/dashed lines | `check_overlap` | move to computed-empty regions + leaders |
| Broken `class=\"secref\"` in HTML | build assertion | raw-string `\"` keeps the backslash — use `'` or de-escape |

**Lesson:** most of these are invisible in a quick look at the rendered page. The
value of the toolchain is catching the ones the eye passes.

---

## 5. Overlap fixes — the repeatable technique

When `check_overlap` flags a label:
1. **Evaluate the curve** at the label's x; find the vertical gap to the nearest other
   curve or the axis.
2. **Place the label in the gap**, or in a genuinely empty corner (compute where the
   curves *aren't*: e.g. on the F(t) log plot the upper-right is empty because both
   curves have decayed there — that's where the τ annotations went).
3. **Add a thin solid leader** from the label back to the point it annotates
   (solid lines are excluded from the check).
4. For crowded multi-curve plots (the eigenmodes), **expand the y-range for headroom
   and put a legend in the strip above the data** (max mode value = 1.0, so `p>1.0`
   is guaranteed empty).
5. Re-run until 0. Don't stop at "looks fine."

---

## 6. Math-in-HTML gotchas (concrete, from this build)

- **Python raw strings for LaTeX.** `\t \n \r \b \f \v \a \0 \x` are all escape
  sequences. `\tau`, `\nu`, `\rho`, `\beta`, `\frac`, `\varepsilon`, `\alpha` all
  contain one. Author all math-bearing content as `r"""…"""`.
- **The single-line raw-string quote trap.** `r"...\"secref\"..."` keeps the
  backslashes, producing invalid `class=\"secref\"` in the HTML. Either use
  single-quoted attributes inside (`r"...'secref'..."`) or de-escape at build time
  (`s.replace('\\"','"')` with an `assert` after). Triple-quoted `r"""…"""` with plain
  `"` avoids the whole problem.
- **No raw `<`/`>` inside `$…$`** — use `\lt \gt \le \ge`. `checklt` enforces it;
  `escape_math_lt.py` fixes it. (Watched for this in D10's `$G\lt1$`, K9's `$r\lt1$`,
  C-solutions' `$a\gg h$`.)
- **SVG ids are page-global.** With ~30 figures on one page, prefix per figure and
  define shared gradients/markers **once** in a hidden `<svg width=0>` defs block that
  every later figure references by id.
- **Halo all figure text** (`paint-order:stroke; stroke:#fff`) so labels read over
  anything — **but exempt white-on-fill labels** (`fill="#fff"` / `class="onfill"`),
  or the white stroke bloats them into blobs.

---

## 7. Pedagogy & physics-content decisions

- **Match the sister module's structure exactly.** §9 mirrors module03 §9:
  `<h3 id="conceptual|derivational|computational">` subheads; each problem =
  `qbox` card + bold title + `Probes:` note (with §-links) + figure + collapsible
  `<details class="sol">`.
- **Cover the whole spine, spread across families.** The 30 problems map deliberately
  onto §1→§8 so each of C/D/K touches composite, Donnan, consolidation, F(t),
  relaxation/creep, Hertz, friction, and OA.
- **Computational solutions carry Python-verified numbers + copy-buttoned code.** The
  code *is* the verification; the prose quotes what the code prints.
- **Validate against independent results.** The Hertz **mean** pressure
  (1.69 MPa) reproduces Module 3's force/area estimate (1.7 MPa) — the contact model
  and the joint-reaction model agree. Every headline number checks against a limit or
  a prior module (see §9 below).
- **Honest limitations are content.** The "what it captures / what it misses"
  accounting (repayment table + Appendix) names each idealization and points to where
  it's cashed (Modules 14, 16).

---

## 8. Validated numbers (the cross-checks that gave confidence)

| Quantity | Value | Independent check |
|---|---|---|
| Donnan swelling π | 0.156 MPa | → 0 as c_F → 0; ≈ handbook 0.16 MPa |
| Hertz contact radius a | 17.95 mm | ≈ stated 18 mm |
| Hertz peak p₀ / mean p̄ | 2.54 / 1.69 MPa | **p̄ matches Module 3's 1.7 MPa** |
| gel time τ = h²/D | 6667 s ≈ 1.9 h | dimensional; τ ∝ h² across 0.5–4 mm |
| F(footstep) / F(1 h stand) | 0.990 / 0.214 | short-time √T law; F(0)=1 |
| charge halved → π loss | 0.156 → 0.042 MPa (73%) | super-linear near operating point |

---

## 9. Collaboration & workflow

- **Section-by-section; commit only on "commit push."** (This module's §9+Appendix
  were pre-authorized as a batch, but the default is per-section review.)
- **Figure sign-off before mass production.** The reviewer pushed back on skipping it
  by rationalizing "the primitives are approved" — the *compositions* weren't, and
  this user has a documented history of rejecting figures. Three representative
  figures (one C, one D, one K) → thumbs-up → then the other 27. Cheap insurance.
- **Previewing figures to the user:** `SendUserFile` didn't render in the user's
  client. Fallback that worked: `python -m http.server` in the scratchpad + open via
  the Chrome tool. Note `file://` URLs are blocked by the navigate tool — **serve over
  `127.0.0.1`**, don't try to open the file directly.
- **numpy startup is slow here** — run figure-compute scripts in the background
  writing to a file, or the 2-min foreground timeout fires.
- **Publish-while-incomplete.** The module went live (linked in `index.html` +
  `README.md`, marked *(in progress)*) as soon as §0–§8 were committed; the marker was
  removed only when §9 + Appendix completed it.

---

## 10. Checklist for the next figure-heavy module

- [ ] Draw the section plan from `prompt.txt` + the prior module's forward-references.
- [ ] Copy the `gen9.py` `P` helper; write one function per computed figure; **run in
      background**; verify numbers against a limit/prior module.
- [ ] Hand-author Tier-2 schematics in a `schem*.py`; reference the shared `<defs>`.
- [ ] Build **one representative figure per family; get it approved** before the rest.
- [ ] Author problems/solutions in an **idempotent assembler** using **raw strings**;
      splice between two literal markers; back up the target first.
- [ ] Run the **full hardening loop after every pass**; drive `check_overlap` to 0 by
      data-aware repositioning + leaders + legends — never by eye.
- [ ] Confirm the rendered result in-browser (served over localhost).
- [ ] Commit only on "commit push"; keep `index.html` + `README.md` in sync; flip the
      *(in progress)* marker when the module is complete.
