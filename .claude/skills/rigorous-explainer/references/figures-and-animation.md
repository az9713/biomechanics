# Figures and animation

Hand-authored inline SVG beats generative images for rigorous diagrams: you get
exact geometry, and every symbol in the math can be placed on the picture. The
goal of a figure here is **mapping symbols to geometry**, not decoration.

## Design principles (read first)
- **Context before abstraction.** Attach abstract vectors/quantities to a
  *recognizable* object — a labeled body, a named joint, the real mechanism. Bare
  arrows on a bare axis read as a riddle ("what are these triangles?"); the same
  arrows on a drawn limb teach. "Not decoration" does not mean "no referent."
- **Every vector is a slim arrow — never a fat triangle/wedge.** A force, load,
  reaction, slide/friction, flow, or motion vector is a *thin shaft + small sharp
  arrowhead* attached to the thing it acts on and labeled. Two failure modes make a
  triangle read as a mystery shape instead of an arrow:
  - **Marker scaling.** `<marker>` defaults to `markerUnits="strokeWidth"`, which
    multiplies the head by the shaft's `stroke-width`. A 10-px head on a 5-px line
    becomes a ~50-px blob. Set **`markerUnits="userSpaceOnUse"`** so the head stays
    a fixed ~10–13 px regardless of shaft weight.
  - **Squat aspect.** An arrowhead must be clearly longer than it is wide and taper
    to a point (e.g. path `M0,0 L11,4 L0,8 Z`, `refX` at the tip so it touches the
    target, `orient="auto"`). A head as wide as its shaft, or wider, points at
    nothing.
  Shaft `stroke-width≈2.5–3`; put the label beside the shaft, not under the head.
  **A "load arrow" is just this slim force arrow** — for a heavier load thicken the
  *shaft* a little, never the head. There is no separate fat-triangle load glyph.
- **Make the teaching difference legible — exaggerate it.** When the point of a
  figure is a *difference* (before/after, long vs short lever, deep vs shallow
  socket), push the contrast past realism until it reads at a glance. A
  faithful-but-subtle difference teaches nothing.
- **Match fidelity to purpose, and mix when it helps.** Physics/abstract figures
  (FBDs, force vectors, charts, all animations) stay flat/schematic (Tier-1); real
  entities (anatomy, devices) get Tier-2 volume — the full ladder is in SKILL.md
  step 4. The strong hybrid: **overlay schematic Tier-1 vectors on a Tier-2
  object** — an FBD drawn on a shaded limb gives correctness *and* context.

## The "setup figure" pattern (one per proof / key result)
Put a small SVG at the top of each proof whose caption maps each symbol in the
statement to a feature of the drawing. Structure:
```html
<div class="proof">
<figure><svg class="setupfig" viewBox="0 0 W H" width="100%" role="img" aria-label="...">
  <defs><marker id="UNIQUE" ...>...</marker></defs>
  ... lines / paths / text labels ...
</svg><figcaption><b>Setup.</b> "x is …, θ is the angle …, R = 1/κ is …".</figcaption></figure>
... derivation ...
</div>
```
- `viewBox` + `width="100%"` makes it responsive; the CSS caps width inside proofs.
- **`viewBox` takes exactly four numbers** — `"minX minY W H"`. A copy-paste slip
  like `viewBox="0 0 0 0 440 240"` (six values) *looks* plausible but is invalid per
  spec: the browser ignores it and falls back to intrinsic sizing, so the figure
  scales differently in different browsers (this shipped on ~11 figures once).
  `check_svg.py` now fails the build on any non-4-value `viewBox`.
- **Unique ids.** `<marker>`, gradients, clips share one global namespace across
  the whole page — prefix per figure (`t1ah`, `p2ah`). Colliding ids = missing arrows.

## Number every figure (and so: caption every figure)
Every figure carries a running number — "Fig. 1", "Fig. 2", … — so prose and
problems can point to a specific one.
- **Don't hand-type the number.** The template auto-numbers via a CSS counter:
  `body{counter-reset:fig}` · `figure{counter-increment:fig}` ·
  `figcaption::before{content:"Fig. " counter(fig) ". "}`. It renumbers itself when
  you reorder or insert figures — nothing to maintain, and it can never drift out of
  order the way a hand-typed "Fig. 4" does.
- **Consequence: every figure MUST have a `<figcaption>`** — that is where the number
  prints. A bare `<svg>` with no `<figure>`/`<figcaption>` wrapper gets no number;
  wrap it. (Decorative/defs-only `<svg width="0">` blocks are not `<figure>`s, so
  they are correctly skipped.)
- **Refer to figures by number** in the text ("as Fig. 3 shows"), never "the figure
  below" — that breaks the moment a figure moves.

## Text labels inside SVG: subscripts and math glyphs (never `$…$`)
MathJax does **not** typeset inside `<svg><text>`; render symbol labels with real
glyphs instead:
- **Subscripts/superscripts Unicode HAS go inline as entities** — `Fₘ` = `F&#8344;`,
  `d₁` = `d&#8321;`. Unicode covers subscript digits and most *lowercase* letters
  (ₐ ₑ ₕ ᵢ ⱼ ₖ ₗ ₘ ₙ ₒ ₚ ᵣ ₛ ₜ ᵤ ᵥ ₓ).
- **Subscripts Unicode LACKS — capital letters especially — use a `<tspan>`:**
  `r_L` → `r<tspan baseline-shift="sub" font-size="8">L</tspan>`. There is no
  subscript-capital-"L" codepoint, so the Unicode trick would silently wrong-case it
  to a lowercase "l". Capital superscripts likewise via `baseline-shift="super"`.
- Angle brackets ⟨ ⟩ = `&#10216;`/`&#10217;`; minus (not hyphen) = `&#8722;`;
  times = `&#215;`; ≈ = `&#8776;`.
- **Never leave ASCII placeholders** (`omega x x dt`, `theta`, `Pi = R^T L`) in
  labels — write the real glyphs (`ω × x dt`, `θ`, `Π = RᵀL` via tspan). Placeholder
  text reads as a draft and silently diverges from the math it names.

## Match SVG label typography to the body math (CSS, no MathJax needed)
SVG `<text>` inherits the page's prose font, so labels look like a different
document than the MathJax captions beside them. Three CSS rules (in the template)
close ~90% of the gap:
```css
figure svg text{ font-family:"STIX Two Math",STIXGeneral,"Times New Roman",Georgia,serif; }
figure svg text.v{ font-style:italic; }   /* variables */
figure svg text.vb{ font-weight:bold; }   /* \mathbf vectors */
```
Tag each label by what it is **in the math**, mirroring TeX conventions:
- `class="v"` → anything TeX sets italic: scalars and Greek (*r*, *L*, *θ*, *ω*),
  named points (*O*, *C*), and short expressions (`τ = r × Mg`, `dL/dt = τ`).
- `class="vb"` → upright-bold `\mathbf` symbols (frame vectors **E₁**, **e₃**).
- no class → prose annotations ("vertical", "precession cone") stay upright.
Italic glyphs are **wider** — re-run `check_overlap.py` after applying; the first
use of this kit exposed a real label collision that upright text had hidden. The
100% fix (pixel-identical labels) is rendering each label with `tex2svg` at build
time inside a generator script — only worth it once a generator exists anyway;
avoid `foreignObject` (breaks in `<img>` embedding and some print pipelines).

## Reusable figure toolkit (when a document has many figures)
A document with dozens of figures should not re-declare its shading and arrowheads
in each one. Build the styling **once** and share it:
- Put the gradients, filters, and markers in a single hidden defs block —
  `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>…</defs></svg>`
  — placed once before the first figure; every later `<svg>` references them by id
  (`fill="url(#b_limb)"`, `marker-end="url(#a_red)"`). The shared ids are defined
  exactly once, so they stay globally unique.
- Write a **parametric generator** — one function per figure family (a posed body,
  a labeled joint, a plot from computed data) — and keep it with the project.
  Regenerating beats hand-editing many SVGs when the style changes. A small plot
  helper (data→pixel `X/Y` mappers, `curve/vline/dot/text`) lets every label sit on
  a *computed* coordinate; emit each figure body to JSON, keyed by id.
- **Prose lives in the HTML; Python generates figures only.** Author the section's
  prose (and problem solutions) **directly in the `.html` file**, where the
  read-aloud audit and `check_prose.py` can see it — they scan the HTML, not your
  scripts. Python's job is the *figures*: emit each `<svg>` body to JSON. Place them
  one of two ways: (a) **default** — paste the final figure bodies into the HTML with
  an editor; or (b) **if the figures churn** — write the prose in the HTML with a
  `<!-- FIGN -->…<!-- /FIGN -->` marker where each figure goes, and run a tiny splice
  step that replaces *only the bytes between each figure's markers* with the JSON
  body (idempotent, so a figure fix is one regenerate-and-re-splice, never N
  hand-edits). **Never author section prose inside a Python raw string** and splice
  the whole block in: prose embedded in a generator reads as *code*, so the aloud
  audit never fires on it — the exact path that shipped an "X-is-X" tautology and a
  "worth VERBing happen" non-idiom. The script may move *figure SVG*, never prose.
  Reuse already-approved figures *verbatim* (extract their `<svg>` from the sign-off
  preview) instead of redrawing them, and back up the target file first.
- This keeps the document **self-contained** (no external assets) even as the
  figure count grows.

## Splice-pipeline hazards (learned the hard way — Modules 4–6)
The `gen{N}.py → figs{N}.json → splice{N}.py`-with-`<!--FIG:key-->`-markers pattern is
reliable, but five concrete traps recur:
- **Assert exactly one marker.** Every splice must do `assert s.count(marker)==1`
  before replacing. This turns a forgotten `<!--FIG:key-->` (easy to omit) or a
  double-paste into a *loud* failure instead of a silent no-op. It has caught real
  omissions.
- **Re-splice by unique `aria-label`, never by viewBox.** Two figures often share the
  same viewBox dimensions (e.g. two `0 0 482 285` plots). A positional regex keyed on
  the viewBox will re-splice the *wrong* figure and silently clobber a good one (a §2
  plot was overwritten by a §3 plot this way). Target the SVG by a substring of its
  unique `aria-label`, or give every figure a distinct viewBox.
- **Constrain portrait/schematic figures with `style="max-width:…"`.** `width="100%"`
  is safe only for landscape plots; a portrait viewBox (e.g. `0 0 200 256`) stretched to
  a 50 rem column renders ~1000 px tall. Add `width="100%" style="max-width:300px"` to
  the `<svg>` for tall network/schematic diagrams. (`check_frame.py` won't catch this —
  it measures wasted *viewBox* margin, not on-page scale.)
- **Figure numbers shift when you insert a figure.** The CSS counter auto-numbers by
  document order, so inserting a `<figure>` mid-section renumbers every later one (a
  new Fig. 13 pushed the response grid to Fig. 14). After any insert/delete, `grep`
  the downstream `Fig\. [0-9]` references and re-point them.
- **Don't clip an unbounded curve flat.** A curve that grows without bound (Maxwell
  creep, a diverging integral), clipped at the axis top, *reads as a plateau* — the
  opposite of the point. Stop the polyline where it exits the frame and add an up-arrow
  (`marker-end`) with an "unbounded ↑" label. Likewise, an asymptote/plateau reference
  line is a *claim*: draw it only on the panels where it actually holds (a σ→0 relaxer
  must not carry a σ=1 plateau line).

## Get the geometry RIGHT (don't eyeball)
- **Tangent to a cubic Bézier** P0,P1,P2,P3 at parameter t: direction ∝
  B'(t) = 3(1−t)²(P1−P0) + 6(1−t)t(P2−P1) + 3t²(P3−P2). Draw the tangent line
  along that vector so it actually touches the curve.
- **Radius of curvature** of a plane curve: R = 1/κ,
  κ = |x'y'' − y'x''| / (x'² + y'²)^{3/2}. Size an osculating circle to the real R,
  not an arbitrary one.
- **de Casteljau split** lets you highlight an exact sub-arc of a Bézier.
- A small Python/JS calc for these points is cheaper than re-eyeballing.
- **Generate plot data and animation keyframes the same way** — polylines from
  computed arrays, SMIL `values` lists from a simulation, joint forces from a
  solver — never by hand. Keep the generator script: figures get re-tuned, and a
  script reproduces them exactly.
- **Markers and data labels sit on *computed* positions, not eyeballed ones.**
  Evaluate the curve at the point you annotate (a peak, a 1/e crossing, an
  operating point) and place the dot/label there, so a label can never point at the
  wrong curve; align tick labels to the curve's actual base too. Annotate with the
  **exact computed value** ("F = 0.986"), not a rounded guess — it's free once the
  script has run.
- **Comparing two distributions of the same total? Conserve the integral — and
  check it numerically.** When you overlay two curves that represent one conserved
  quantity (two contact-pressure profiles both carrying the same load, two PDFs, two
  spectra of equal energy), verify each integrates to that total before drawing
  (`∫p(r)·2πr dr` for both, confirm they match). Otherwise "flatter" silently means
  "less total," and the comparison lies. This is the distribution analogue of
  putting markers on computed positions.
- **To show a scaling law, normalize away the confounds so only that law is left.**
  Demonstrating `τ ∝ h²`? Scale the *other* parameters (e.g. the ramp time `t0 ∝ h²`)
  so the curves become self-similar and coincide except for the one shift the law
  predicts — then the figure shows `τ ∝ h²` as a clean horizontal translation and
  nothing else. This is the opposite move from "exaggerate the difference": here you
  *suppress* every variation except the target relationship.

## Genuinely 3-D content: project computed geometry, never fake perspective
Hand-placed ellipses "suggesting" 3-D are where figure bugs live: a vector drawn on
the wrong side of a rotated axis, a dot orbiting in the picture plane instead of
around the true rotation axis, an "intersection curve" that satisfies neither
surface. When a figure shows real 3-D objects (curves on surfaces, quadric
intersections, cones, swept paths), write a small **stdlib-Python generator** that
computes the 3-D geometry and projects it — then the drawing *cannot* disagree
with the equations. Recipe (all hand-rollable, no numpy):

- **Orthographic camera.** Pick azimuth/elevation, build an orthonormal triad,
  project by dot products:
  ```python
  AZ, EL = radians(35), radians(18)
  VIEW  = (cos(EL)*cos(AZ), cos(EL)*sin(AZ), sin(EL))   # toward the viewer
  RIGHT = (-sin(AZ), cos(AZ), 0.0)
  UP    = cross(VIEW, RIGHT)
  screen = (cx + s*dot(P, RIGHT), cy - s*dot(P, UP))    # y flips: SVG y is down
  ```
- **Curves on surfaces: parametrize analytically, then ASSERT.** For the
  intersection of two quadrics, eliminate one coordinate between the equations and
  parametrize the rest trigonometrically. Before drawing, assert **every sampled
  point satisfies both defining equations to 1e-9** — this is the figure's unit
  test; a wrong sign or swapped axis fails loudly instead of shipping.
- **Hidden-line removal for convex bodies is one dot product.** A surface point is
  visible iff its outward normal has `dot(n, VIEW) > 0` (sphere: `n ∝ P`; ellipsoid
  `Σ x_i²/a_i² = 1`: `n ∝ (x_i/a_i²)`). A curve lying on *two* bodies needs both
  normals to pass. Split the sampled loop into visible/hidden runs → solid strokes
  vs dashed at ~45% opacity. (Convex-only is usually enough; mutual occlusion
  *between* bodies can be skipped textbook-style — note the ceiling in a comment.)
- **Silhouettes are exact, not sampled.** For an ellipsoid `xᵀAx = 1` the
  orthographic outline is the 2-D ellipse `yᵀ(BᵀA⁻¹B)⁻¹y = 1` with `B = [RIGHT UP]`
  — one 2×2 eigendecomposition. A sphere's outline is a circle. No surface meshing.
- **Splice output between literal markers** in the HTML
  (`<!-- FIGN-GENERATED:BEGIN/END -->`, same idempotent-replace pattern as the
  toolkit section above), keep the script in `tools/`, and name it in the
  figcaption ("computed by tools/gen_figN.py, not drawn by hand") — that sentence
  is a rigor claim the reader can check.
- **Animate along the computed path.** Feed the projected closed curve to
  `<animateMotion path="M… L… Z">` on a `<circle r="5">` at the origin (path
  coordinates are absolute). **Never** use `animateTransform type="rotate"` for
  precession/orbit-like motion — it spins the dot in the *picture plane*, which is
  the wrong projection of a 3-D circle (visibly wrong: the dot sweeps through the
  floor).

## Charts that span orders of magnitude — log axis + operating band
When the x-quantity covers several decades (timescales, frequencies, stiffnesses) a
linear axis crushes the small end against zero. Use a **log axis** with computed
decade ticks — `X(t) = x0 + (x1−x0)·(log10 t − log10 tmin)/(log10 tmax − log10 tmin)`
— so two phenomena orders of magnitude apart (a 1 s footstep and a 6700 s gel time)
read on one plot. Shade the **operating band**, the regime real use lives in (e.g.
"steps & gait"), so the reader sees at a glance where on the curve the physics
matters — and keep the band's edges honest to the plotted curve, don't overstate it.

## Labels must clear the curves — halo everything
The commonest wart on a computed chart: the *curves and reference lines come from
computed coordinates, but the text labels are hand-placed by eye*, so a label ends
up sitting on a curve, or a dashed reference line strikes straight through the text.
It's the inverse of the markers rule — the dot is placed correctly, the caption
isn't. Fix it at three levels, cheapest first:
- **Halo every in-plot label (do this always).** One CSS rule draws a white outline
  *behind* the text so anything passing under it stays legible:
  `svg.setupfig text{ paint-order:stroke; stroke:#fff; stroke-width:2.5px; stroke-linejoin:round; }`
  This alone rescues "line strikes through text" (a `σ∞`/`mean`/`μ_eq` label on its
  own dashed line) and makes an on-curve label readable — no repositioning needed.
  **But exempt white/light labels that sit on a solid fill** (bar values like
  `99%`, `+`/`−` glyphs inside coloured circles, a caption on a shaded shape): a
  *white* stroke on *white* text bloats the glyphs into fuzzy blobs (the counters
  fill in). Those labels already contrast against their fill, so turn the halo off
  for them — `.setupfig text[fill="#fff"],.setupfig text.onfill{ stroke:none; }`
  (attribute selector auto-exempts white fills; add `class="onfill"` for other
  light fills). Rule of thumb: halo = dark-on-light text; never white-on-white.
- **Place annotations in whitespace; put reference-line labels just *above* the
  line.** A bump leaves its top corners empty; a decaying curve leaves one side
  empty — drop the label there, with a thin leader line to the point if needed.
  Never free-float a long label across the middle of a curve.
- **Make placement data-aware (the principled fix).** The curve `y(x)` is already
  computed — evaluate it at the label's x and offset the text to the empty side
  (above if the curve is low there, below if high). This is the markers rule
  extended to labels: overlaps become impossible by construction. On **twin-axis
  plots** a diagonal reference curve (a recruited-fraction Φ, a rising stiffness
  `k(x)`) sweeps *diagonally* through the panel, so there is no fixed "empty side" —
  find the vertical band between that curve and the primary curve at the label's x and
  drop the text there; if a steep curve leaves no room at all, delete the redundant
  text label rather than forcing it (the guide line + caption already carry it).
Two more: keep **axis titles clear of the first/last tick label** (else "ε/ε₀" and
the "1" tick merge into "ε/ε₀¹"); and **enforce it mechanically, don't eyeball it**
— `scripts/check_overlap.py FILE` loads the page in headless Chrome and
geometrically tests every `<text>` in each `.setupfig` against every `<polyline>`
and every long dashed reference `<line>` (using `getBoundingClientRect` +
`getScreenCTM`, so rotation and %-width scaling are exact; solid axes/gridlines/
ticks/arrows/leaders and short legend-swatch dashes are excluded → no false
positives). It prints each offender's user-space box and the colliding point, so
you reposition data-aware and re-run until it reports 0. A static preview shows an
overlap only if you happen to be looking for it; this doesn't rely on the eye. Run
it in the hardening loop, not as an afterthought — a documented rule with no
checker is a rule that silently rots (a Module-4 sweep found 11 real overlaps the
eye had passed).

**A related trap `check_overlap` does *not* catch: a data curve hidden under a
reference line.** If a plotted trajectory happens to lie on a gridline or a dashed
reference of the same colour/position (e.g. a "habitual" remodeling curve sitting
exactly on the 100% dashed line), the data vanishes — but this is line-on-line, not
text-on-line, so the checker is silent. Guard it *by eye at draw time*: offset the
reference line a hair, or give the data curve a distinct style/endpoint marker. (A
`check_overlap` extension to flag coincident same-position lines is possible but
heuristic and false-positive-prone, so it stays a manual guard, not a gate.)

## In-document animation: SVG SMIL (no JS, offline)
Use SMIL for processes that are hard to picture statically (a cycle, a wave, a
mechanism). It loops natively and needs no JavaScript.
- `<animateTransform attributeName="transform" type="translate" values="…" keyTimes="…" dur="5s" repeatCount="indefinite"/>` inside a `<g>` moves that group.
- Toggle phase labels with `<animate attributeName="opacity" values="1;1;0;0" keyTimes="…">`.
- **Sync** elements by giving them the same `dur` and `keyTimes`; encode the
  motion in each element's `values` list.
- **Drive the keyframes from the same solution as the static plot of the process —
  not by hand.** If a figure elsewhere charts the process (a relaxation curve, a
  load-support fraction `F(t)`), pull the animation's `values` from that same
  solution: settle a platen by the degree of consolidation `U = 1 − F`, fade a
  pressure overlay by `F`. Then the movie and the chart agree frame for frame
  instead of telling two slightly different stories.
- **Map the animation clock to physical time deliberately.** SMIL runs on a 0..1
  clock; if the process is diffusive/multiscale, map that clock to *log* physical
  time so the visible change is paced like the real process (fast early, slow late),
  not linearly.
- **`keyTimes` and `values` must have equal counts** (and `keyTimes` start at 0, end
  at 1, monotonic). A count mismatch silently kills the animation — check it.
- **Back-and-forth motion along a path** (a ball oscillating in a potential well
  between turning points): one `<animateMotion>` with
  `keyPoints="0;1;0" keyTimes="0;0.5;1" calcMode="linear"` — no return path to author.
- **Watch for no-op animations**: animating `stroke-dashoffset` on a path that has
  no `stroke-dasharray` changes nothing, yet looks intentional in source. If an
  animation exists, confirm something on screen actually moves (sampled-frame check
  below).
- **A tinted, semi-transparent `<rect>` animated in `opacity` reads as a *fading
  field*** (pressure, temperature, concentration): overlay it on the shaded body and
  ramp its opacity ∝ the field's magnitude, so the field visibly drains away.
- **Toggle paired labels at one position with opposed opacity ramps** (label A
  `values="1;…;0"`, label B `values="0;…;1"`, same `keyTimes`) to narrate phases in
  place ("t=0: fluid carries the load" → "t~τ: matrix carries the load").
- **The loop can carry meaning.** `repeatCount="indefinite"` snaps back to the
  start; if that reset *is* part of the story (a gait cycle re-loading, a wave
  recurring), name it in the caption rather than apologising for it.
- Verify it animates by sampling: in the browser, `svg.pauseAnimations();
  svg.setCurrentTime(t); el.transform.animVal.getItem(0).matrix.e` at a few `t`.
  A static screenshot only confirms the `t=0` layout — confirm motion by the count
  check above plus a sampled frame.

Example (a patch that shoves then partly recovers — a ratchet):
```html
<g>
  <rect x="60" y="104" width="34" height="14" fill="#7a1f1f" fill-opacity="0.55"/>
  <animateTransform attributeName="transform" type="translate"
    values="0 0; 0 0; 120 0; 120 0; 60 0; 60 0" keyTimes="0;0.2;0.4;0.6;0.8;1"
    dur="5s" repeatCount="indefinite"/>
</g>
```

## Shareable video: Remotion (when you want an MP4/GIF, not in-doc)
Remotion (React + TypeScript) renders a composition to MP4/GIF — good for READMEs
and talks. Minimal `package.json` scripts:
```json
"scripts": {
  "studio":  "remotion studio",
  "render":  "remotion render <CompId> out/clip.mp4",
  "gif":     "remotion render <CompId> out/clip.gif --codec=gif"
}
```
- Downscale GIFs for READMEs: `--codec=gif --scale=0.5 --frames=0-179` (smaller file).
- The composition is a normal React component animated by `useCurrentFrame()`.
- Rule of thumb: **SMIL for in-page animation, Remotion for a shareable clip.**
  GitHub READMEs can't embed live HTML or an MP4 player — embed the **GIF** inline
  and link the MP4.
