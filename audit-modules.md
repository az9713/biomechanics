# Course-wide audit — Modules 1–5

Read-only quality audit of `module01.html`–`module05.html` (Module 5 covers only
the built §0–§1). Produced by a per-module deep read + arithmetic/coordinate
checks. Nothing in the modules was changed. Findings are de-duplicated and
prioritized; the recurring cross-cutting themes are the highest-leverage fixes.

---

## A. Cross-cutting themes (fix the pattern once → every module improves)

1. **Literal underscores in SVG figure labels** (M1 §4/§5, M2 mechanostat, M3 §4
   FBD + D2/D3 + K-figs; M5 already fixed). Labels render as `W_s`, `F_ab`, `d_m`,
   `ε_lo` with a visible underscore — reads as a code variable, not math, and
   violates the course's own SVG-subscript rule. **Fix:** sweep to Unicode
   subscripts (`Wₛ`, `dₘ`) or `<tspan baseline-shift="sub">` for capitals.
2. **SVG label typography doesn't match the MathJax body.** Template now uses a
   serif math font (STIX) + `class="v"/"vb"`, but Modules 1–5 predate it, so a
   figure's `F_m` looks unlike the caption's `$F_m$`. **Fix:** retrofit the three
   CSS rules + tag labels across all modules.
3. **Unflagged symbol collisions**, despite the course prizing this: `M` = moment
   vs body mass (M1); `a,b` = moment arm / Hertz radius / Baumgarte gain (M3);
   `T` = temperature vs dimensionless time (M4, listed twice in its notation
   table). **Fix:** rename or add a "reuse flagged" note at each site.
4. **Figures auto-numbered but never referenced by number.** Prose still says "the
   figure below." **Fix:** cite "Fig. 3 shows…".
5. **§9 problem-set navigation (M3, M4).** 30 collapsible problems, no sub-TOC, no
   back-to-top. **Fix:** TOC sub-links (`#conceptual/#derivational/#computational`)
   + per-group "↑ contents" and/or "expand all solutions."
6. **Disclosure-label inconsistency:** diagnostics say "Answer," problems say
   "solution"/"Show solution" (M3, M4). **Fix:** unify or state the distinction.
7. **No `prefers-reduced-motion` guard on the SMIL animations** (M3; applies
   wherever animations exist). **Fix:** freeze to a representative frame under that
   media query.
8. **No inter-module navigation.** Each module is an island. **Fix:** a slim
   "◀ Module N−1 · Module N · Module N+1 ▶" header rail.

## B. Concrete defects (should just be fixed)

- **M4: malformed `viewBox="0 0 0 0 440 240"` on ~11 problem figures** (C2–C10,
  D2/D3/D8/D10). Six values is invalid → browser-dependent scaling. Drop the
  leading `0 0`; re-run `check_overlap`.
- **M1: animation caption/keyframe mismatch** — caption says the moment-arm bar
  "collapses to zero as the arm reaches vertical," but keyframes stop at 75°
  (bar ≈78 px). Extend to 90° or soften the caption.
- **M2: habitual-trajectory curve is invisible** — the black line at y=130 sits
  exactly on the grey 100% dashed reference line. Offset one or restyle.
- **M3: "nonholonomic" is a rigor error** — the planar roll-and-glide knee has a
  *configuration-dependent (holonomic)* instantaneous axis; genuine nonholonomy
  needs 3-D. Relabel and tighten the §1 "rolling wheel" aside.

## C. Per-module high-impact substance

### Module 1
- **Use the force-balance half of Law 1.** `∑F=0` is introduced but never used; the
  joint compression (~700 N to hold a 49 N bag) is one step away and motivates
  Module 2.
- **Quantify the low-back climax.** "Several thousand newtons" is the payoff but the
  only unquantified claim — add the erector-spinae / L5–S1 worked number.
- **Fix two lever claims:** define `d_m` explicitly as the *perpendicular* moment
  arm; "human limbs are third-class levers" is over-general (ankle plantarflexion
  at toe-off is second-class).
- Add a literature reality-check (elbow-flexor moment arm ~3–4 cm, MVC torque
  ~50–80 N·m) to make "right order of magnitude" checkable.

### Module 2
- **§4 Torsion is an orphan** — no derivation, figure, number, `G`, or angle of
  twist. Build it out with `τ=Tρ/J` and the 45° helical spiral-fracture figure.
- **§10 problem set is thin and solution-less** — far below Modules 3/4. Add
  collapsible solutions and more problems.
- **Two derivation gaps in flagship §3:** show neutral axis = centroidal axis
  (`∫y dA=0`); derive Prop 3.3's 1.44× equal-area result instead of asserting it.
- **Reconcile bone-strength numbers** (100/130/150/170 MPa appear with no statement
  that tension governs bending failure).
- Add a Voigt/Reuss rule-of-mixtures bound to *validate* the 17 GPa modulus; add a
  nanostructure figure.

### Module 3
- **Hip `R=2.5W` likely understates** (vertical-force assumption; abductor line of
  action → ~3W), and a *static* prediction is validated against *walking*
  telemetry — compare like with like.
- **K1–K10 only exercise §7** — no computational problems for hip JRF (§4), contact
  pressure (§5), or stability ratio (§6), the module's most clinical numbers.
- **§5 claims congruence matters most but the figure only sweeps modulus** — add the
  `p₀∝R_eff^(−2/3)` congruence curve so the headline claim is shown.

### Module 4
- **Hertz is oversold** — flags the thin-layer issue but not that `a≈R_eff`
  (small-contact assumption broken) and the hip is *conforming* (wrong contact
  class). Add one honesty sentence.
- **10% held strain sits outside the stated small-strain/linear regime** — drop to
  ~2–5% or acknowledge it.
- **§6 switches to a knee** while the numeric spine is the hip reaction — reconcile
  or note the generic illustration.

### Module 5 (§0–§1 only)
- **§0↔§1 force reconciliation is asserted, not shown** — add an elbow-flexor-group
  mini-table so the ~600 N is demonstrated (a second validation).
- The sarcomere inset (Fig. 3) is the natural first SMIL when §2 is built; Fig. 4's
  pennation vertex is slightly crowded.

## D. Polish (compact)

- **M1:** reconcile "12×" vs "13×"; state Prop 3.1's distal-mass assumption; tighten
  Appendix `r_s` sourcing; whole-body figure for §6's "same law everywhere"; note
  `cosθ` is even (above-horizontal case).
- **M2:** define `ε*` at first use; state Poisson ratio / 1-D scope; note the strain
  band is illustrative (~2000–3000 µε real); soften `n≈1.3` (typical 2–5); add an
  integrated capstone example; remove dead autolink comment stubs.
- **M3:** link the two Grübler forms; base D8 on §6.1's cleaner argument; cite the
  ~0.35 shoulder stability ratio; unify the pendulum sign convention; decimate
  ~200-point polylines (file ~311 KB).
- **M4:** align footstep-`F` precision (0.986/0.99/0.990); complete the "every
  symbol" notation table (missing `E_tens`, `μ_bl`, `S₀`, `α`, loop gain);
  distinguish the two ~10–12 MPa moduli; note the multi-mode `1/e` timing.

## Biggest wins (short list)
1. The cross-cutting sweep A1–A3 (subscripts, SVG typography, symbol-collision
   flags) — touches every module.
2. The M4 `viewBox` bug (B1).
3. Pure-upside substance: M1 joint-reaction + low-back numbers; M2 torsion section
   + problem solutions; M3 nonholonomic fix.
