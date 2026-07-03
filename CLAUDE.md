# Project: Quantitative Human Musculoskeletal Science (course)

A mathematically rigorous biomechanics course delivered as **self-contained HTML
modules** (MathJax + inline SVG/SMIL, no build step). Built with the
`rigorous-explainer` skill. Published to GitHub Pages.

## Where things are
- **Repo:** https://github.com/az9713/biomechanics (PUBLIC), branch `main`.
- **Live site:** https://az9713.github.io/biomechanics/
- **Files:** `index.html` (landing + syllabus), `module01.html`…`module03.html`,
  `README.md`, `svg-figure-tiers.md` (figure-style decision doc), `prompt.txt`
  (the original course spec — the source of truth for scope/structure).
- **Skill:** `C:\Users\simon\.claude\skills\rigorous-explainer\` — `SKILL.md`,
  `scripts/*.py` (hardening tools), `references/*.md`, `assets/template.html`.
- **Temp/figure work:** use this session's scratchpad dir (path differs per
  session) for Python figure-data generation and preview renders — never commit it.

## Status (resume here)
> **⇒ NEW SESSION — READ `HANDOFF.md` (repo root) FIRST.** It is the live resume
> point (current state + next task); this file is the standing conventions.
- **Module 1** (mechanical foundations) — COMPLETE, live.
- **Module 2** (bones / beam theory / remodeling) — COMPLETE, live.
- **Module 3** (joints as constrained interfaces) — COMPLETE, live. §0–§9 +
  Appendix; all `§N` forward-refs autolinked (0 unlinked/broken). Last commit
  `cbb2366`.
  - **§9 has 30 problems** (10 conceptual C1–C10, 10 derivational D1–D10, 10
    computational K1–K10) + 5 diagnostics. Every problem has a **Tier-2 figure**,
    a **"Probes:" note**, and a collapsible `<details class="sol">` solution;
    computational solutions use **Python-verified numbers**.
  - **§9 figure pipeline (reusable, in scratchpad):** `fig9lib.py` (shared
    Tier-2 defs `b_limb/b_torso/b_sph/b_bone/b_sh` + arrow markers `a_red/a_grn/
    a_blu/a_mus`, a programmatic posable **human body**, `cap/sph/body/arrow/
    txt/plot`), `fig9_whole.py` (C1–C3 whole-body), `fig9_regional.py` (C4–C10
    hand/knee/socket/bone/contact/muscle), `fig9_deriv.py` (D1–D10 FBD overlays +
    schematics), `fig9_comp.py` (K-figs: limb scenarios + computed plots),
    `lab9k.py`→`kdata.json` (K2–K10 numbers/plots), `assemble_*.py` (patch the
    figures/problems into the HTML). **One shared `<svg width=0>` defs block** is
    inserted once before `<h3 id="conceptual">`; every figure references it.
  - **Figure rule established with the user:** §9 diagrams must be Tier-2 +
    whole-body/recognizable + clean labelled vector arrows (NOT abstract
    arrows-on-a-line). SVG-text labels use Unicode subscripts, NOT `$…$`.
  - §7 design call (kept): **redundant Cartesian coords** (point-mass positions),
    NOT joint angles, so multipliers expose the joint reactions (§3.5); 2 bones +
    rail → 1 DOF; one KKT solve/step gives λ=(λ1,λ2,λ3); R=|λ_i|·L_i. Lab compute
    scripts: `lab7.py`, `lab7_gen.py`.
- **Module 4** (Cartilage, Synovial Fluid, Joint Contact Biophysics) — COMPLETE, live.
  §0–§9 + Appendix; full §-by-§ plan in `module04-plan.md`. §0 motivation, §1 charged
  porous composite, §2 Donnan swelling, §3 biphasic **consolidation PDE**
  `∂u/∂t=H_Ak ∂²u/∂z²` (boxed), §4 **fluid load support** `F(t)`, §5 stress-relaxation/
  creep FD lab, §6 Hertz→biphasic contact pressure, §7 lubrication / Stribeck /
  `μ_eff=μ_eq(1−F)`, §8 osteoarthritis cascade. Last commit `d9a7607`.
  - **§9 has 30 problems** (10 conceptual C1–C10, 10 derivational D1–D10, 10
    computational K1–K10) + 5 diagnostics + hub figure + repayment table. Every
    problem has a figure (computed plot or Tier-2 schematic), a **"Probes:" note**,
    and a collapsible `<details class="sol">` solution; K solutions use
    **Python-verified numbers** with copy-buttoned code (commit `5ffd39c`).
  - **§9 figure pipeline (reusable, in scratchpad):** `gen9.py` (a `P` plot helper +
    all computed plot/curve bodies → `svg9.json`, numbers → `nums9.json`; y-axis
    titles auto-rotated by post-processing any `<text x<32>`), `schem9.py` (11
    hand-authored Tier-2/schematic bodies → `schem9.json`), `assemble9.py` (all 30
    problem statements/solutions as raw strings; pulls figure bodies from the JSONs,
    reuses the approved trio C1/D1 svgs from `trio_preview.html`, splices the block
    between the `<h3>Problems</h3>` and `<p>That closes…` markers — **idempotent**).
    Session-transient; the durable record is `module04.html`.
  - **Appendix** (`id="appendix"`): grouped **notation table** (every §0–§9 symbol,
    each linked to its section) + grouped **parameter table** (healthy-cartilage
    values, derivation/problem cited). TOC pending-span flipped to a link; 3 in-text
    Appendix refs wired. Fragment `appendix_frag.html` in scratchpad.
  - **COMPLETE & live** in `index.html` + `README.md` (no *(in progress)* marker).
- **Modules 5–17** — future (see `prompt.txt` Course Structure + `index.html`
  syllabus); draw each module's plan from `prompt.txt` + the prior module's
  forward-references when starting it (as was done for Modules 3 and 4).

## How we work (conventions established with the user)
1. **Section-by-section.** Build ONE section → report with a short summary + 2
   `★ Insight` bullets → the user reviews → on **"commit push"** do the git commit
   + push. Do not commit until they say so.
   - **Publish-while-incomplete (policy):** every time a `moduleNN.html` is
     committed and pushed, also make it a **live web page** by wiring it into BOTH
     listing pages and pushing them too: (1) `index.html` — add/keep its
     `<a href="moduleNN.html">` entry (copy the existing module-link markup; append
     *(in progress)* in the `.desc`) and shift the pending "Modules N–17" line;
     (2) `README.md` — add its live URL to the **Live pages** list. A module goes
     live as soon as it's committed, NOT only when complete. (Supersedes the old
     "link only when complete" stance. `README.md` was the one missed for Module 4.)
2. **Per-section build loop:**
   - Compute figure/plot data with Python in the scratchpad; emit SVG polyline
     coords / animation keyframes (don't eyeball geometry).
   - **Prose lives in `moduleNN.html`; Python builds figures only.** Write the
     section's prose/solutions **directly in the HTML** (where the read-aloud audit
     and `check_prose.py` see it). Use Python for the *figures* — emit each `<svg>`
     body to JSON, then either paste them into the HTML or splice them into
     `<!-- FIGN -->…<!-- /FIGN -->` markers that sit in the already-written prose.
     **Never author section prose inside a Python raw string** (`build_secN.py`) and
     splice the whole block in — prose-in-code evades the aloud audit; that is the
     path that shipped the §4 "Summation is summation in $a$" / "worth watching
     happen". The Module 3/4/5 `assemble/build_secN.py` pipeline below is the *old*
     way; prefer the leaner one for §5 onward. (Do the figure generators with Python;
     keep prose out of them.)
   - Write the section HTML (follow `rigorous-explainer` SKILL.md).
   - Harden (see below) after every edit pass.
   - Preview a figure by extracting its `<figure>` to a standalone HTML and
     `shoot.py` → Read the PNG. (MathJax screenshots need the script's virtual-time
     budget; never eyeball a raw screenshot for math.)
   - **To show the *user* a live preview:** the `navigate` tool blocks `file://` and
     `SendUserFile` may not render in their client — serve the dir with
     `python -m http.server` (background) and open `http://127.0.0.1:PORT/…` via the
     Chrome tool (`?v=N` to cache-bust).
   - **Run figure-compute scripts in the background** (`run_in_background`) writing
     to a file — numpy startup is slow here and a foreground run hits the 2-min
     timeout (output is usually written before it fires, but background is clean).
   - **`autolink_sections.py` rewrites the whole file**, invalidating any pending
     Edit's cached state → re-Read (or re-Grep the exact line) before the next Edit,
     and `rm` the `moduleNN.html.bak` it leaves behind.
   - **Style sign-off before mass-producing figures.** When a section needs many
     figures in one style (e.g. §9's 30), build/preview **one representative
     figure and get it approved** before drawing the rest — a style fix applied to
     30 figures is expensive. (Approve the *example*; section review still happens
     per §1.)
3. **Forward references** to not-yet-built sections use `<span class="secref">§N</span>`
   (NO href) so links don't break; convert to real links via `autolink_sections.py`
   once the section exists.
4. **Pillar 1 — define every symbol/term at first use** (self-contained). Audited
   already; watch cross-section **symbol collisions** (we fixed W, k, g, E reuse).
   Gloss anatomical jargon (e.g. "femoral head (the ball atop the thigh bone)").
5. **Cadence — no walls of words, but NO word limit.** Break prose >~10 lines;
   a visual every screenful; never delete content to satisfy this — interleave/split.
6. **Math-in-HTML gotchas:** no raw `<`/`>` inside `$…$` (use `\lt \gt \le`); if
   `checklt` fires run `escape_math_lt.py`. `checktex` false-positives on
   `\leftrightarrow` (use Unicode `↔`). SVG `id`s are **page-global** → prefix per
   figure (e.g. `cylH`, `cyl0`, `cylJ`, `cylB`). **Generating HTML from Python?**
   Author math-bearing strings as **raw strings** (`r"""…"""`) — `\tau` is a tab,
   `\nu` a newline, `\varepsilon` a vtab, `\boxed` a backspace; and a single-line
   `r"...\"x\"..."` keeps the backslash (broken `class=\"…\"`), so use `'`-quoted
   attributes or de-escape (`s.replace('\\"','"')`). (See the skill's
   `references/math-html-gotchas.md` §7.)

## Hardening loop (run after every edit; all must pass)
```
S=C:/Users/simon/.claude/skills/rigorous-explainer/scripts
python $S/checktex.py    moduleNN.html   # delimiter/brace balance — 0 issues
python $S/checklt.py     moduleNN.html   # raw <,> in math — 0
python $S/check_links.py moduleNN.html   # 0 broken (unlinked §refs OK until autolink)
python $S/verify_dom.py  moduleNN.html   # 0 mjx-merror, 0 broken (stray-$ ~6 is advisory)
python $S/check_overlap.py moduleNN.html  # 0 labels over a curve/dashed line (ENFORCED, not by eye)
python $S/check_frame.py moduleNN.html    # figures whose viewBox wastes >20% margin (advisory; retighten min-y/height)
python $S/check_prose.py moduleNN.html    # awkward/non-native constructions: X-is-X, "worth VERBing happen", … (advisory; then read aloud, incl. build_secN.py raw-string prose)
python $S/shoot.py FILE out.png --size WxH   # preview render
```
**`check_frame.py` catches oversized viewBoxes** — a figure whose interior geometry is
computed but whose `<svg viewBox>` is a round number bigger than the drawing, leaving a
blank band on the page (e.g. a diagram in the lower third of `0 0 460 250`). It compares
each figure's rendered `getBBox()` to its viewBox and prints a tightened `viewBox` to
paste. Advisory, not a gate.
**`check_overlap.py` is the enforcement for the label-overlap rule** — it loads the
page in headless Chrome and geometrically tests every `<text>` in each
`.setupfig` against every `<polyline>` (curve) and dashed reference `<line>`
(mean/σ∞/τ), using `getBoundingClientRect`+`getScreenCTM` (handles rotation/scale).
Solid lines (axes, gridlines, ticks, arrows, leaders) and short dashes (legend
swatches) are excluded, so no false positives. When it flags a label it prints the
label's user-space box + the offending point → reposition data-aware and re-run
until 0. **Do not eyeball a preview for overlaps — run this.** (The Module-4 sweep
that established this found 11 real overlaps the eye had passed.)

## Figure style: default **Tier-2 SVG** (see `svg-figure-tiers.md`)
- **Physics diagrams (FBDs, vectors, plots) and ALL animations → flat/schematic
  SVG** (abstraction is correct there; SMIL needs vector).
- **Anatomical / real-entity figures → Tier-2:** shaded capsule bones + sphere
  heads/knobs + `feDropShadow` + specular highlight. Generate bones
  programmatically. **Never AI-generate anatomy.** For true textbook realism the
  route is "Real" (adapt open-license vector art + attribution) — not freehand Tier-3.
- Reusable Tier-2 `<defs>` (prefix ids per figure):
  ```
  <linearGradient id="cylX" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a08b63"/><stop offset="0.42" stop-color="#f8f2e5"/><stop offset="0.62" stop-color="#e6d9bc"/><stop offset="1" stop-color="#9c8760"/></linearGradient>
  <radialGradient id="sphX" cx="38%" cy="34%" r="70%"><stop offset="0" stop-color="#fcf8ef"/><stop offset="0.6" stop-color="#e8dabb"/><stop offset="1" stop-color="#c2ae84"/></radialGradient>
  <filter id="shX" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="2" dy="3" stdDeviation="2.5" flood-color="#000" flood-opacity="0.22"/></filter>
  ```
- Bone generator (run in scratchpad; rotates a `<rect rx>` to the bone axis so the
  cylinder gradient sits across the width):
  ```python
  import numpy as np
  def bone(x1,y1,x2,y2,w,grad):
      cx,cy=(x1+x2)/2,(y1+y2)/2; L=np.hypot(x2-x1,y2-y1)+w*0.15; a=np.degrees(np.arctan2(y2-y1,x2-x1))
      return f'<rect x="{cx-L/2:.1f}" y="{cy-w/2:.1f}" width="{L:.1f}" height="{w:.1f}" rx="{w/2:.1f}" fill="url(#{grad})" transform="rotate({a:.1f} {cx:.1f} {cy:.1f})"/>'
  ```
- **Figures must be recognizable, with clean labelled arrows** (lesson from §9).
  Show a real entity — a whole body, a named joint — and attach the vectors to it.
  **Never** abstract arrows-on-a-bare-line (they read as a riddle: "what are the
  triangles?"). Use whole-body context for posture/stance/gait, regional Tier-2
  for joint-specific topics. Exaggerate a teaching difference (long vs short lever,
  deep vs shallow socket) so it reads at a glance. SVG-`<text>` labels use Unicode
  subscripts (`₁₂₃ₛₑₗₕ` = `&#8321;…&#8347;&#8337;&#8343;&#8341;`), **NOT** `$…$`
  (MathJax does not typeset inside `<svg><text>`).
- **Arrow markers — every vector is a slim arrowhead, NEVER a fat triangle/wedge.**
  A vector (force, load, joint reaction, slide/friction, fluid flow, motion) is a
  *thin shaft + small sharp arrowhead*, attached to the entity it acts on and
  labelled. Use the shared slim markers `a_red/a_blu/a_grn/a_mus`
  (`markerWidth≈9`, path `M0,0 L6,3 L0,6 Z`) — or an equivalent inline marker —
  and set **`markerUnits="userSpaceOnUse"`** so the head is a fixed ~10–13 px and
  does **not** scale with the shaft. Shaft `stroke-width≈2.5–3`; `orient="auto"`,
  `refX` at the tip so the point touches the target; label beside the shaft, not
  under the head. **A "load arrow" is just this slim force arrow** (heavier load →
  thicken the *shaft* modestly, but keep the same slim head — never widen the head).
  - **Do NOT** use a squat triangle whose head is much wider than its shaft, and do
    NOT leave `markerUnits` at the default `strokeWidth` on a thick line: that
    multiplies the marker by the stroke-width into a ~50 px blob that reads as a
    mystery shape, not an arrow (the §0 "load triangle" mistake the user rejected —
    same family as the §9 abstract-triangle riddle). There is **no** separate
    fat-triangle/wedge load glyph in this course.
- **Reusable multi-figure pipeline (built for §9; reuse for any figure-heavy
  module).** Don't re-declare shading/arrowheads in every figure:
  - Put gradients + filters + markers in ONE hidden defs block —
    `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>…</defs></svg>`
    — placed once before the first figure; every later `<svg>` references them by
    id (`url(#b_limb)`, `url(#a_red)`). Shared ids defined exactly once → still unique.
  - Write a **parametric generator**: a **posable human body** = shaded capsule
    limbs + sphere joints + head, drawn from joint pixel-coords (pose per problem);
    plus per-family helpers (joint, socket, plot) and labelled-vector-arrow helpers.
  - The §9 generators (`fig9lib.py`, `fig9_whole/regional/deriv/comp.py`,
    `lab9k.py`, `assemble_*.py`) live in the **scratchpad and are session-transient**
    — regenerate from this pattern; the durable record is here, not those files.
- **Computed plots & SMIL animations (lessons from §3–§7).**
  - **Markers/labels go on *computed* positions, annotated with exact values** (so a
    label always matches its curve); align tick labels to the curve's real base, not
    by eye (the §3 fix where T-labels were re-placed at each curve's computed base).
  - **Log x-axis for decade-spanning quantities** (timescales): map
    `X(t)=x0+(x1−x0)(log10 t−log10 tmin)/(log10 tmax−log10 tmin)` so a 1 s footstep
    and a ~6700 s gel time read on one plot. Shade the physiological **operating
    band** ("steps & gait") but keep its edges honest to the curve.
  - **SMIL keyframes are physics, not art:** drive `values` from the *same* solution
    a static chart uses (platen settles by `U=1−F`; pressure overlay fades by `F`),
    so movie and chart agree. Map the 0..1 animation clock to *log* physical time.
    `keyTimes`/`values` counts MUST match (mismatch = no animation). A tinted
    opacity-animated `<rect>` over the shaded body = a fading field; toggle paired
    phase labels via opposed opacity ramps; a meaningful loop (the gait cycle
    re-imbibing) gets *named* in the caption, not hidden.
  - **SVG-`<text>` math glyphs via entities, never `$…$`:** ⟨ ⟩ = `&#10216;`/`&#10217;`,
    subscripts via `<tspan baseline-shift="sub">`, superscripts `10³⁴⁵` =
    `&#179;`/`&#8308;`/`&#8309;`, minus = `&#8722;`, `≳` = `&#8819;`.
  - **Integral-conserving comparison (§6):** overlaying two distributions of the
    same total (two contact-pressure profiles carrying one load) → verify each
    integrates to that total in Python (`∫p·2πr dr` matched to 1715 N) before
    drawing, so "flatter" can't secretly mean "less load."
  - **Isolate a scaling law by normalizing confounds (§5):** to show `τ∝h²`, scale
    the other params (ramp `t0∝h²`) so the curves coincide except for the predicted
    shift — the law reads as one clean horizontal translation (opposite of
    "exaggerate the difference": here suppress every variation but the target).
  - **Labels must clear computed curves & reference lines (§4–§7 overlap fix).**
    Curves/lines are computed but text is hand-placed → labels land on curves and
    dashed lines strike through text. Fixes, cheapest first: (A) **halo all figure
    text** — `.setupfig text{ paint-order:stroke; stroke:#fff; stroke-width:2.5px;
    stroke-linejoin:round; }` in the module `<style>` (now in the skill template)
    — **but exempt white/light labels on solid fills** (bar %s, `+`/`−` glyphs,
    captions on shapes), else the white stroke bloats them into blobs:
    `.setupfig text[fill="#fff"],.setupfig text.onfill{ stroke:none; }` (halo =
    dark-on-light only, never white-on-white);
    (B) put annotations in whitespace / reference-line labels just *above* the line,
    leader line if needed; (C) data-aware placement (eval the computed curve at the
    label's x, offset to the empty side); keep axis titles off the first/last tick
    (the `ε/ε₀`+`1` merge); (E) **run `check_overlap.py` (now in the hardening loop)
    — it enforces this mechanically; reposition data-aware from its box+hit output
    until it reports 0. Never eyeball a preview for overlaps.**

## Git / publish
- `gh` CLI authenticated as **az9713** (active account). Pages already enabled.
- Commit as: `git -c user.name="az9713" -c user.email="az9713@yahoo.com" commit …`
- Commit message trailers (this environment's convention):
  ```
  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
  Claude-Session: <session url>
  ```
- After push, Pages rebuilds in ~1 min; user must hard-refresh / append `?v=N`
  (fragment-only nav doesn't reload). LF→CRLF git warnings on Windows are harmless.

## Audience & problem-set standard
**Audience = MIT-PhD level.** Do not water down; assume fluency with calculus, ODEs,
optimization, and numerical methods. In particular, **computational (K) problems must
build scientific understanding, not test arithmetic.** A "substitute the given numbers
into the boxed formula" problem (e.g. $F_{\max}=\sigma\,\mathrm{PCSA}\cos\theta_p$ with
numbers) is busywork at this level — it reveals nothing the derivation didn't already
show. Every computational problem must require one of: **numerical integration** (run the
ODE/simulate a train), **optimization** (solve the redundancy/argmax, find an optimal
angle/rate), an **inverse problem** (recover the command or a parameter from the output),
a **sensitivity sweep** (how does the optimum shift with a parameter?), or a **regime
comparison** (concentric vs eccentric energetics, two cost functions). Test each K
problem: *does solving it surface science the reader could not have read straight off the
boxed result?* If not, deepen it or cut it. (This was retrofitted into Module 5 §10 after
the first K1–K10 draft was flagged as plug-in substitution.)

## Note
The user values: rigor (no watering down), correct anatomy, strong visuals
(Tier-2), and reviewing each section before commit. Keep the `★ Insight` summaries.
