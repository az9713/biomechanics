---
name: rigorous-explainer
description: >-
  Build a rigorous, figure-rich, self-contained HTML explainer/tutorial for any
  technical or mathematical topic — with step-by-step derivations and proofs,
  hand-drawn SVG diagrams, in-page animations, and every symbol defined before
  use. Use this whenever the user wants to derive, prove, explain, or teach
  something rigorously as a document or web page: "derive X", "prove Y
  step by step", "explain Z with figures", "turn these notes into a tutorial",
  "make an interactive math/physics/CS explainer", "MathJax HTML write-up",
  or wants a publishable lesson with diagrams and animations — even if they
  don't say the word "tutorial". Also covers hardening math-in-HTML (MathJax
  rendering bugs, broken section links) and shipping the result to GitHub Pages.
---

# rigorous-explainer

Produce a single **self-contained HTML** document (MathJax + inline SVG/SMIL, no
build step) that derives a result rigorously and *teaches* it. Optionally ship it
live to GitHub Pages.

This skill's folder contains everything you need:
- `assets/template.html` — the starting scaffold (MathJax config + CSS kit + pattern stubs).
- `scripts/*.py` — validation/fix tools; each takes the HTML path as `argv[1]`.
- `references/*.md` — load the relevant one when you reach that step (don't load all up front).

## Five pillars (non-negotiable — this is what "rigorous explainer" means)
1. **Define every symbol and term at first use, self-contained** (a forward link may be added, never substituted).
2. **One building spine** — each section uses the previous; demote off-path rigor to an Appendix.
3. **Extensive visuals — never a wall of words** — a symbol→geometry figure per proof, SMIL animation for anything hard to picture statically, plus a table/chart/labeled diagram wherever it beats prose. Target a visual every screenful; split any paragraph over ~10 lines.
4. **Rigorous, step-by-step derivations and proofs** — show every step; box the headline result. **Uniform rigor across siblings:** every boxed result earns its box — if one result in a section is a `.prop`/`.thm` with a `.proof`, its boxed neighbours (e.g. sibling constitutive laws) must be proved the same way, not left as an inline "…gives X" assertion. Mismatched rigor ("the author ran out of steam") is a defect no syntactic checker catches — audit it per section (`check_proofs.py` inventories it). See `references/pedagogy-checklist.md` §4.
5. **Clickable section cross-references** — `id` on every heading; refs auto-linked.

Details and checklists: `references/pedagogy-checklist.md`.

## Workflow

### 1. Plan the spine
Outline the sections so section N needs N−1. Lead with a concrete **Section 0
motivation** (an everyday hook) before any abstraction. Decide what is mainline
vs. Appendix. Confirm scope/audience/depth with the user if unclear. If the spine
explains a **model**, plan a near-the-end "what it captures / what it misses"
section that names each idealization and points to where it is later repaid (a
following section, an Appendix, or a sister document) — honest limitations are
content, not an apology.

### 2. Scaffold
Copy `assets/template.html` to the output file and fill in the title/sub/TOC. It
already has the working MathJax config, the CSS kit (`.thm/.def/.lem/.prop/
.proof/.secref/.keyresult`), and stubs for a setup figure and a SMIL animation.

**Code listings get a Copy button.** Every `<pre>` code block is wrapped in
`<div class="codewrap">` with a `.copybtn` (clipboard SVG icon + "Copy", flips to
"Copied!" for 1.5 s). The scaffold ships the `.codewrap`/`.copybtn` CSS and the
`copyCode()` script (async Clipboard API on https, `execCommand` fallback for
local `file://`); it copies `code.textContent` so the reader gets the exact
source. Reuse this wrapper for every code listing you add.

**Author code compact and PEP8 — `<pre>` preserves whitespace verbatim.** Unlike the
rest of the HTML (where inter-tag newlines collapse and are invisible), a `<pre><code>`
block renders every source newline. So blank lines *between statements* — harmless
elsewhere — come out as visible gaps that triple-space the listing (this shipped in a
Module 8 built by a different tool whose output had blank lines between every source
line; the prose collapsed fine, only the `<pre>` listings looked broken). Rule: inside
`<pre><code>`, write **one statement per line, no blank lines between related
statements** (a single blank line to separate logical groups is fine), keep lines
**≤ 79 chars**, and follow **PEP8** (arithmetic without spaces — `a*b` — is PEP8-fine
and keeps lines short; E226 is not enforced). `check_code.py` gates this: it runs
`pycodestyle` on every Python `<pre><code>` block and **fails on any PEP8 issue**,
including `E303` (the too-many-blank-lines spacing bug) and `E501` (line too long).
Authoring code with the Write tool (never pasting from a source that double-spaces
lines) avoids the problem at the source.

### 3. Derive rigorously
Write the math in `$…$` / `$$…$$`. Use the boxed environments for
definitions/theorems/lemmas/props and `.proof` for proofs (show every step; end
with `∎` via `<span class="qed">`). **Define each symbol and term the first time
it appears.** **Choose the representation that makes the quantity you are teaching
explicit** in the equations, not merely the one that is easiest to compute — e.g.
keep redundant coordinates that expose a constraint force rather than reduced ones
that project it away. Where you can, **validate**: land a result next to an
independent check — a measured value, or a known limiting case the formula must
reproduce. **Prose lives in the HTML, computation lives in the scripts.** Write the
section's prose and proofs *directly in the `.html`* (where the read-aloud audit and
`check_prose.py` see it); use scripts only to compute figure data. **Never author
section prose inside a Python raw string** and splice the block in — prose-in-code
evades the aloud audit and ships awkward phrasing (this is how "summation is summation
in $a$" shipped). **Uniform rigor across siblings:** if one boxed result in a section
gets a `.prop`+`.proof`, its peer boxed results (e.g. sibling constitutive laws) must be
proved the same way, not left as an inline "…gives X" `.keyresult`. `check_proofs.py`
flags the crisp case (a proposition with no `.proof`); the keyresult-vs-proof call is a
judgement — eyeball each section's boxed results and confirm peers match.

### 4. Visualize
Give each proof a **setup SVG figure** mapping its symbols onto geometry. **Compute
real geometry, plot data, and animation keyframes in a script** (Bézier tangents,
radius of curvature, solver output) — don't eyeball, run the model even when the
answer seems obvious (the surprises are the teachable moments), and keep the
generator so figures can be regenerated. **Genuinely 3-D content (curves on
surfaces, quadric intersections, cones) is never faked with hand-placed ellipses**
— generate it: orthographic-project computed 3-D points, assert every sampled
point back onto its defining equations, dash hidden arcs via surface normals, and
splice the SVG between markers (recipe in `references/figures-and-animation.md`,
"project computed geometry"). **SVG labels use real glyphs in the MathJax-matching
serif kit** (`class="v"` italic variables / `class="vb"` bold vectors — in the
template; details in the same reference). Add **SMIL** animations for processes.
**Every SVG marker/id must be unique across the page.** Before mass-producing many
figures in one style, get **one representative figure approved first** — cheap
insurance against redrawing them all. **When a figure exists to show effect X (a
decoupling, a spike, a crossover), verify the computation actually produces X — print
the punchline number — *before* building the figure around it** (a "catapult" plot
nearly shipped showing amplification ≈ 1.0×). **Match the model to the figure's job:**
if honest first-principles dynamics belongs to a later lab, use a cleaner
kinematic/prescribed-input decomposition for the earlier illustration and *label it as
such*, don't dress a half-baked sim as a prediction. Use **Remotion** only for a
shareable MP4/GIF (e.g. a README clip). Patterns, the exact geometry formulas, and the
**splice-pipeline hazards** (viewBox collisions, marker asserts, portrait
`max-width`, figure renumbering, unbounded-curve arrows):
`references/figures-and-animation.md`.

**Cadence — no walls of words.** No stretch of prose should run more than ~10
lines without a figure, table, chart, list, or boxed result, and long paragraphs
get split (one idea each). Pick the lightest aid that carries the point: a
**table** for comparisons/parameter sets, a **chart** for quantitative trends
(compute the data, don't sketch it), a **labeled diagram** for structure/anatomy,
a **SMIL animation** for anything that happens over time, a **boxed equation** for
the headline. If a sentence describes a spatial or temporal relationship, draw it
as well. A **dense reference table is not self-explanatory** — pair it with per-row
prose, and when the mapping is conceptual add a visual index (e.g. a before/after
grid) rather than leaning on the table alone. **No cap on prose length** — this
limits walls of words, not word count;
keep the full explanation and rigor, and break it up rather than cutting it. Audit
by scrolling the rendered page: any text-only stretch taller than a screen is a
defect, fixed by interleaving a visual or splitting the paragraph — never by
deleting content.

**Anatomical / real-entity figures — default to Tier-2 SVG.** Split figures into
*physics/abstract* (FBDs, force vectors, governing-equation sketches, charts, and
**all animations**) which stay **flat/schematic** — abstraction is correct there —
and *real-entity* figures (anatomy, devices, objects) which get volume.
**Exception — problem-set (C/D/K) figures always lead with the recognizable
Tier-2 entity.** The flat-schematic license above is for *standalone* physics
figures embedded in a section that has already established the anatomy in prose and
neighbouring figures. A problem figure stands alone next to a bare question, so the
three-layer rule below **overrides** the flat default: draw the body / foot / leg /
joint / spine (Tier-2, shaded, recognizable) **first**, then hang the FBD, vectors,
angles, or plot on it. A biomechanics problem figure that is *only* arrows, lines,
a bare circle, or a bare chart — no recognizable entity — is a geometry puzzle and
fails Layer 1, even though it "is a physics figure." (This is exactly how Module 8's
C/D/K set regressed: the flat-abstraction rule was read as license, the enforced
hardening loop had no interpretability gate to catch it, and the "approve one
representative figure first" guard was skipped in an autonomous run.) For the
latter, hand-author **Tier-2 SVG**: simple primitives (rounded-capsule `<rect>`s,
circles) shaded for 3-D — a cylinder gradient across each part (a `<rect rx>`
rotated to its axis with an object-bounding-box gradient), sphere (radial)
gradients on heads/knobs, a soft `feDropShadow`, and a blurred specular highlight.
Tier-2 reads as 3-D yet stays self-contained, crisp, editable, and license-free.
Fidelity ladder: **Tier-1** flat schematic (physics figures + animations stay
here); **Tier-2** shaded primitives (**DEFAULT** for anatomy); **Tier-3**
hand-traced Bézier silhouettes + multi-layer shading (hero figures only — high
effort, and freehand outlines can be subtly wrong while looking authoritative);
**"Real"** = adapt an open-license vector illustration (textbook-accurate, but
needs attribution + a borrowed style). **Never AI-generate anatomy** (hallucination
risk); when true realism is required prefer "Real" with attribution over freehand
Tier-3. Generate shaded bone capsules programmatically (compute each part's
length/angle so the gradient aligns) rather than placing them by hand.

**Problem-figure semantic clarity: three adherence layers.** Use these layers to decide how strongly to enforce figure guidance.

**Layer 1 -- non-negotiable figure rules.** A figure must reduce cognitive load, not create a geometry puzzle. The reader should know what they are looking at before using the figure to solve the technical problem. Match the figure to the task being taught, not just to the topic: a derivation figure must expose the geometry or logical construction behind the formula; a computational figure must expose the computation when it has visual structure (sweep, inverse solve, optimization, threshold, sensitivity, or regime comparison); a conceptual figure must make the concrete mechanism visible. If an equation uses a pivot, force, moment arm, angle, center of mass, boundary, or control point, those quantities must be visible and labeled on the figure. Shared physical models do not justify duplicate-looking figures for different tasks.

**Layer 2 -- problem-type checklist.** Before finalizing a problem set, audit figures by problem role. For conceptual (C) problems, ask whether the drawing makes the mechanism or contrast immediate. For derivational (D) problems, ask whether the derivation can be reconstructed from the labeled geometry: pivots, sign conventions, moment arms, force directions, angles, limits, and named state variables. For computational (K) problems, ask whether the visual shows the actual numerical operation: axes, ticks, units, curves, bars, legends, optimum, threshold, inverse mapping, sensitivity ranking, or computed comparison. Related D/K problems may share a small anatomy inset or visual vocabulary, but they should not look like the same figure if one asks for a derivation and the other asks for a computation.

**Layer 3 -- domain patterns and examples.** Treat these as examples, not universal mandates. For biomechanics/anatomy, draw the recognizable entity before the variables: body, foot, knee, spine, trunk, load, support base, or joint. Label quantities where they live: COM, COP, XcoM, base of support, foot edge, L5/S1, trunk COM, load, phi, r_t, r_L, muscle arm d, muscle force, ground reaction, and spinal compression. For computational biomechanics problems, a strong pattern is a small anatomy inset establishing the model plus a larger plot/bar/sweep/ranking panel showing the actual calculation. For force and load figures, arrows must be anchored to the structure they act on, and moment arms should be drawn from the pivot to the line of action or projection used in the equation.

**Full-body default (biomechanics posture / gait / balance / load).** When the teaching context is a *person* — standing, leaning, walking, running, jumping, lifting, swaying, single-leg stance, compass gait, COP/GRF/COM on a human — the figure must show a **recognizable whole body** in Module&nbsp;1 style, not an isolated head (circle), lone limb (capsule), or V-shaped compass-stick legs. Minimum Tier-2 chain: **shaded head** (`sphH` / `b_head`) + **multi-segment trunk** (≥2 torso capsules or a flexed spine chain) + **both legs** with **foot polygons** on the ground line + **arms** when reach/load/balance matters. Generate poses programmatically from joint pixel-coordinates (`figlib` / `fig9lib` pattern); never place one capsule and call it a person. **Exempt** (regional close-ups are fine): elbow/forearm FBD, pelvis-on-one-leg frontal FBD, knee/socket contact, foot-arch truss, cartilage/tendon/bone tissue, pure plots/phase portraits, SLIP point-mass schematics *when explicitly labeled as the lumped model*. A problem-set figure in a gait/balance module that is only arrows on a bare line or a single pill-box fails Layer&nbsp;1 even if `check_probfig` passes.

**A body must be proportionally consistent with its OWN limbs — derive the scale from
the drawing, not from a constant.** When adding a body onto a figure that already draws
part of it (compass-gait legs, an inverted-pendulum link, a shank FBD), do **not** pick
the body unit `U` independently: derive it from the existing limb — a full hip→foot leg
of length `L` implies `U = L/2.35` (thigh 1.20U + shank 1.15U) — then size head
(r = 0.55U), torso (0.95U wide), and limb **thickness** (thigh 0.52U, shank 0.44U, upper
arm 0.40U, forearm 0.34U) from that same `U`, and thicken the pre-existing limb to match.
The defect this prevents shipped across ~20 Module-8 figures: a chunky template body
(head r=27, torso 49 wide) was bolted onto the module's existing 15px hairline compass
legs — because the instruction was *"the model legs are physics, leave them thin"*. The
result matched neither the template nor the old style, and the body's own `U=62` was
inconsistent with its legs' implied `U=75`. **"It's the physics model, not anatomy" is
not a licence to leave a limb hairline** — the reader sees one figure, and a chunky bust
on sticks is a proportion clash, not a modelling choice. `check_bodyprop.py` now
HARD-fails it (thickness/length < 0.18). **And note how it escaped:** every other gate
passed (`check_probfig` only asks whether *some* entity is drawn), and the human review
sampled 3 figures out of ~30 — none of them the C/D/K set that carried the defect. When
a change touches a whole class of figures, **render every figure in that class, not a
sample**, and check them against the *user's* standard rather than your own rationale for
deviating from it.

**Semantic audit beyond scripts.** `check_overlap.py` can prove that labels do not sit on curves, but it cannot prove that a figure is interpretable. After the mechanical checks pass, inspect each problem figure for semantic clarity: What is the object? What are the forces or variables? Where are the pivots, angles, and moment arms? What task does this figure serve? If the reader must decode the drawing before starting the math, redraw it.

**Number and reference every figure.** The template auto-numbers each `<figure>`
"Fig. N" via a CSS counter — so every figure needs a `<figcaption>`, and prose
should cite figures *by number* ("as Fig. 3 shows"), never "the figure below"
(which breaks when a figure moves). **Guard animations for reduced motion:** the
template freezes SMIL under `@media (prefers-reduced-motion: reduce)` — keep the
static figure carrying the pedagogy so a frozen animation still teaches.

### 5. Cross-link
Ensure every heading has an `id`, then:
```
python scripts/autolink_sections.py FILE.html      # wraps §N / §N.M / ranges; map auto-derived from headings
```

### 6. Harden — run after EVERY edit pass
```
python scripts/checktex.py   FILE.html     # $/$$ + brace/\left-right/\begin-end/\boxed balance + stray control chars (shell/format-mangled math)
python scripts/checklt.py    FILE.html     # literal <,> inside math  (fix: escape_math_lt.py)
python scripts/check_links.py FILE.html    # every #id link resolves; flags unlinked § refs
python scripts/check_svg.py  FILE.html     # viewBox arity + literal _/^ in <text> (0 hard); advisories
python scripts/verify_dom.py FILE.html     # headless Chrome: 0 mjx-merror, 0 stray $, links OK; + swallowed-prose advisory
python scripts/check_overlap.py FILE.html  # headless Chrome: 0 labels over a curve/dashed line
python scripts/check_frame.py FILE.html    # headless Chrome: HARD-fails on figures CLIPPED past the viewBox edge (content cut off); advisory on >20% wasted margin
python scripts/check_prose.py FILE.html    # awkward/non-native constructions: X-is-X, "worth VERBing happen", … (advisory)
python scripts/check_proofs.py FILE.html   # a .prop/.thm/.lem with no adjacent .proof = asserted proposition (advisory; sibling-keyresult rigor is a judgement call — eyeball it)
python scripts/check_code.py FILE.html     # every Python <pre><code> block is PEP8 (pycodestyle): fails on E303 blank-line spacing bug, E501 long lines, etc.
python scripts/check_probfig.py FILE.html  # problem (C/D/K) figures that are neither a drawn entity nor a labelled plot — floating arrows/bare glyph/text (advisory; then eyeball ALL problem figures for the 3-layer semantic audit)
python scripts/check_bodyprop.py FILE.html # headless Chrome: HARD-fails a body figure with a HAIRLINE limb (thickness/length < 0.18; template limbs run 0.23-0.43) — the "chunky head+torso on thin stick legs" defect

```
**The `check_probfig` advisory does NOT replace the semantic audit — it only narrows
the candidates.** A green `check_probfig` means no figure is a *bare* abstraction; it
does NOT mean the figures are interpretable. After it runs, still eyeball **every**
C/D/K figure against the three-layer rule: does it lead with the recognizable Tier-2
entity, are the pivot/force/moment-arm/angle/COM visible and labelled where they
live, are arrows anchored to the structure, and does a K figure carry a small model
inset beside its computation? Module 8's regression passed every mechanical check;
only this manual pass catches "the reader must decode the drawing before the math."
**Verify the DOM, never a screenshot** — MathJax is async and screenshots go blank
mid-typeset. **`check_svg.py` catches label/figure defects statically** — a
malformed `viewBox` (the plausible-looking `"0 0 0 0 W H"` has six values and
renders browser-dependent) and a literal `_`/`^` in an SVG `<text>` (write a Unicode
sub/superscript or a `<tspan baseline-shift>`); it also prints advisories
(ASCII-Greek placeholders, figures never cited by number, mixed disclosure labels,
heavy polylines). **`check_overlap.py` enforces "labels clear the curves"** geometrically
(see `references/figures-and-animation.md`): it flags any figure `<text>` sitting on
a `<polyline>` or long dashed reference `<line>` and prints its box + the hit, so you
reposition data-aware and re-run to 0. Don't eyeball a preview for overlaps. **`check_frame.py`
catches two viewBox-fit bugs, one HARD, one advisory.** It measures each figure's `getBBox()` (which
honours `transform`s, unlike a static coordinate scrape) against its viewBox. (a) **CLIPPING (HARD,
exit 1)** — content spills *past* a viewBox edge and the browser cuts it off. The one that shipped in
Module 10: 13 problem figures put an x-axis title at `y0+30 = 182` inside a `viewBox="0 0 300 180"`,
so the bottom line of every plot label ("gain kₚ", "delay τ (s)", "placement error e (m)") rendered
below the box and was clipped — and *every other check passed* (checktex/check_svg/check_overlap/
verify_dom all green), because clipping is outside the box: not a `<`/`>`/`_` issue, not a
label-over-curve hit, not wasted interior margin. A human caught it. Clipping is never intentional,
so it now fails the build; the script prints how many px past which edge and an enlarged viewBox to
paste. **Sizing a figure's viewBox from hand-computed coordinates is unreliable** (text glyph
extents, markers, and off-scale computed points — e.g. an s-plane pole placed off-axis — exceed the
attribute coordinates you can see), so **size viewBoxes to content or trust this gate to catch the
miss.** (b) **WASTED MARGIN (advisory)** — the viewBox is a round number bigger than the drawing,
leaving a big empty band (a real one: a diagram in the lower third of `0 0 460 250`, 56% blank above
it); it prints the margins and a tightened viewBox, but retightening is a judgement call so it never
fails. `check_svg`'s viewBox check is *arity only* — it cannot see clipping or wasted space, which is why this
is a separate browser check. **`check_prose.py` is the sentence-level backstop** — it greps the
*mechanically-detectable* awkward constructions that have actually shipped (an *X-is-X* tautological
copula like "summation is summation in $a$"; a verb-stacked non-idiom like "worth watching happen";
a doubled function word; a stiff "the &lt;noun&gt; of which"). Advisory, and deliberately narrow: most
non-native phrasing is **not** regex-detectable, so it does **not** replace the read-aloud audit in
`references/pedagogy-checklist.md` ("Sentence-level prose craft") — and that audit explicitly covers
prose you authored **inside a generator script** (a `build_secN.py` raw string, a Python-emitted
figcaption), which is exactly where the aloud reflex fails to fire. If `checklt` fires, run `python scripts/escape_math_lt.py FILE.html`.
The *why* behind each check: `references/math-html-gotchas.md` (read it the first
time something "won't render"). Re-checking in a browser? cache-bust with `?v=N`.

### 7. Ship (only if the user asks — it publishes)
GitHub Pages + an `index.html` redirect; a README with a **clickable preview
screenshot → live page** (GitHub can't embed live HTML/MP4) plus a GIF for motion;
commit only deliverables. Full recipe (gh commands, .gitignore, screenshot via
`scripts/shoot.py`, Unicode-math-in-README rule): `references/shipping.md`.

## Scripts quick reference
| Script | Does | Fails (exit 1) when |
|---|---|---|
| `checktex.py` | MathJax delimiter/brace balance + stray control chars (shell/format-mangled math) | any imbalance or stray TAB/VT/FF/BS/BEL/CR |
| `checklt.py` | literal `<`/`>` inside math | any found |
| `escape_math_lt.py` | fix: `<`→`\lt`, `>`→`\gt` in math (writes .bak) | delimiter imbalance |
| `check_links.py` | `#id` links resolve; warns on unlinked §refs | broken link |
| `check_svg.py` | `viewBox` arity + literal `_`/`^` in `<text>`; advisories (placeholders, uncited figures, mixed `<summary>`, heavy polylines) | malformed `viewBox` or `_`/`^` in a label |
| `check_overlap.py` | headless Chrome: figure `<text>` sitting on a curve/dashed ref line | any label overlaps |
| `check_frame.py` | headless Chrome: `getBBox` vs `viewBox` — content CLIPPED past an edge (hard) + >20% wasted margin (advisory), each with a corrected viewBox to paste | content clipped past the viewBox edge |
| `check_prose.py` | awkward/non-native constructions (X-is-X, "worth VERBing happen", doubled word, stiff "of which") | — (advisory) |
| `check_proofs.py` | a `.prop`/`.thm`/`.lem` with no adjacent `.proof` (asserted proposition); sibling-keyresult rigor is a judgement call it can't see | — (advisory) |
| `check_code.py` | every Python `<pre><code>` block via `pycodestyle` (PEP8): E303 blank-line spacing bug (`<pre>` preserves whitespace), E501 long lines, spacing | any PEP8 issue |
| `check_probfig.py` | problem (C/D/K) figures that are neither a drawn Tier-2 entity nor a labelled plot (floating arrows/bare glyph/text); narrows candidates for the manual 3-layer semantic audit | — (advisory) |
| `check_bodyprop.py` | body-figure PROPORTION: per limb, thickness/length (scale-free) + thickness vs head radius. Catches a chunky head/torso bolted onto hairline stick limbs | a limb's thickness/length < 0.18 (template limbs are 0.23–0.43) |
| `autolink_sections.py` | wrap §refs in links, map from headings (.bak) | — |
| `verify_dom.py` | rendered-DOM checks via headless Chrome + swallowed-prose advisory (inline `$…$` that ate a sentence; source re-read) | mjx-merror or broken link |
| `shoot.py` | reliable headless screenshot → PNG | load failed |

## Reference output
The skill distills the build of a worked example (a physics derivation, "the ruck
in a rug"): live at https://az9713.github.io/ruck-in-a-rug/ — every instruction
here is satisfiable by, and consistent with, that document.
