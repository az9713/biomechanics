# Anatomy figure audit — defect register (2026-07-27)

Course-wide visual audit of every human-anatomy figure, triggered by `/goal
audit all modules; fix all diagrams with incorrect/incomplete anatomy;
regenerate`. Findings are **coordinate-verified from the SVG source** (the
pre-rendered contact sheets were truncated at 1340 px and unreliable — ignore
them). Each module's anatomy figures were inventoried via GRAD (flesh/bone
gradient) references.

## PROGRESS (updated 2026-07-27)

Fixes are underway, worst-first, gate-verified and committed per module.

**Done & pushed (~55 figures):**
- **m03 f26** — clipped viewBox fixed (`8b1cdce`).
- **m04 f15, m06 f21, m13 f4** — three named stroke-width slabs thinned (`f6d866c`).
- **m13 f5/f9/f16/f23 — all four "trunk-column" no-legs figures REGENERATED** with
  correct posed bodies (stair-climber, incline-walker, stairs up+down, slope
  up+down) via `anatomy_kit.body_group` + feet on the treads/slopes
  (`cd9bc84`/`f9c388e`/`4080630`/`10d601b`). Element-wise body-swap recipe: grab
  the figure's 6 broken limb rects + spheres, blank them, replace the head circle
  with a `body_group` posed to the scene's anchor; verify by render.
- **m07 figs 18/23/29/30/31/32 — 8 broken inset/lifter bodies REGENERATED.** The
  bent-forward lifters (18, 32) were replaced preserving the **hip/shoulder/arm
  axes** so the L5/S1 pivot + erector-spinae/disc-compression/moment-arm overlays
  stay aligned; the standing insets (23, 29, 30, 31 — one-legged, armless) got a
  parametric standing `body_group`; fig31's stiffness "slab" bars + fig29's
  hip-strategy arrow thinned (sparing the `#5a86a8` balance beams). All gates clean.
  **m07 residual:** the sheet-numbered "fig16" hyperextension backbend could NOT be
  located in document order (numbering mismatch) — left for careful fresh work;
  fig2/3/15/40/48 are minor/clean.
- **m11** — 4 of the 5 defect classes cleared:
  - the **6 blank figures** (empty body `<g>`) now render correct Winter seated
    bodies via `anatomy_kit.body_group` + fig12 slab thinned (`81703fd`);
  - **29 detached heads** seated on slim necks (`035b7f8`);
  - **60 leader/force stroke-width slabs** thinned by the 0.3×length signature
    (`035b7f8`… see `pushed` after). All gates green.
  - **m11 residual (minor, still TODO):** fig2 missing foot/hand; fig16 & fig23
    elbow posture (through-arm / wrong-way wave); missing hands on
    fig17/25/29/33/34/40/42; faded elbow-up IK branches (fig5/17/28).

**PROVEN BATCH-FIX RECIPE (reuse for m07/m12/m13/m09/m10/m15):**
1. **Emit a missing/broken body:** compute a joints dict (seated or standing) and
   call `anatomy_kit.py.body.body_group(joints, show_arms, show_feet)`; splice the
   returned `<g>` in place of the empty/broken body group. m11's seat pose is a
   good template (see git `81703fd`). Verify the module has the gradient ids
   `b_limb/b_head/b_sph` (all present in m07/11/12/13).
2. **Seat a detached head + slim the neck-ball (shared-coord batch):** if the head
   circle and neck rect are at *fixed inner coords* across N figures (they were in
   m11: head `cy=89 r=14`, neck `y=113.2 w=38.2` ×29; m12/m13 share the SAME
   `y=113.2 w=38.2` neck-ball), lower the head to seat and replace each fat
   neck-ball with a slim vertical neck capsule (width ~14) at the same centreline
   (`cx = rect.x + w/2`). One regex pass fixes all N.
3. **Thin stroke-width slabs — BY RATIO, never by width alone** (see caveat below):
   for each `<line>`, thin to ~2.6 only if `stroke-width>10` AND
   `stroke-width/length>0.15` AND the stroke is not a wood-tone floor/chair line
   (`#c9b79a/#b09a78/#9a8f7a/#6a5a3a`). This hits exactly the 0.3×length bug and
   spares limbs/muscle/FEM/floor. (Works when limbs are *rects*, as in m11/12/13;
   in m09/m10 limbs are thick `#c98a5e` LINES — exclude that colour too, or the
   legs vanish.)
4. After each module: run all nine gates (esp. `check_bodyprop`, `check_frame`,
   `check_overlap`, `verify_dom`) + eyeball a render of the touched figures; commit.

## ⚠ FIGURE-NUMBER CAVEAT — locate by caption, not by number
The per-module findings below number figures by their **position in the audit
contact-sheet**, which does NOT equal document order (`<figure>` index) — e.g. m13
"fig 15" = document svg #19. Some modules also draw bodies inside scaled/translated
`<g>` groups, so a finding's coordinates are **post-transform** values that do not
appear literally in the markup. Before editing any remaining figure: match it by
its **aria-label / figcaption text**, and resolve the group transform (or replace
the whole body group via `anatomy_kit.body_group`, as done for m11's empty bodies)
rather than trusting raw coordinates. Mis-targeting by number will corrupt a
correct figure.

## Root cause (one regression, many figures)

The **biological-figure-realism pass** (commit `3fd6fbe`, 2026-07-20) rebuilt the
*exposition* figures with the correct `anatomy_kit.body_group` (Winter
proportions — these are good), but the **problem-set (C/D/K) figures and several
section figures use a different, broken body drawer**. Its defect signatures:

1. **Detached / undersized head** — head is a bare `<circle url(#b_head)>` at a
   hand-picked coord with **no neck segment**, floating a visible gap above the
   shoulder; often ~2× too small (→ 15–16 head-heights tall).
2. **Footless legs** — shanks end in blunt capsule stumps; no foot, or a foot
   ellipse detached from / below the ankle.
3. **One-leg / one-arm bodies** — contralateral limb absent entirely (not drawn
   behind).
4. **"Trunk-column" bodies** — head + stacked trunk capsules with **no legs at
   all**, in figures whose whole subject is leg work (m13 5, 9, 16, 23).
5. **Single-capsule limb, no joint** — one capsule hip→ground with no knee (or
   shoulder→hand with no elbow).
6. **Backwards knee** — shank rotated to the wrong side of the thigh (verify by
   cross-product); m09 fig 2 (5 of 6 legs), m15 fig 3.
7. **Flat unshaded head** — `fill="#f3ece0"` instead of `url(#b_head)`.
8. **Neck ball too large** — a "neck" segment nearly the head's diameter → reads
   as two stacked heads.
9. **Stroke-width slab bug (module 10 + m13 f4)** — ground / plumb / force
   `<line>`s given `stroke-width` = ~0.3 × segment length → **78–174 px slabs and
   barcodes that bury the anatomy** (the limb-width formula wrongly applied to
   non-limb lines). Also fat-rectangle "arrows" instead of slim markers.
10. **Mis-anchored arrows** — arrow tip lands in empty space, not on the
    structure it labels (m08 f17, m10, m13 f4, m14 f5/f18).
11. **Femur with no neck** — proximal femur = shaft + head sphere bolted on the
    shaft axis, no femoral neck / greater trochanter; fall-impact arrow aimed at
    the head (inside the acetabulum) instead of the lateral greater trochanter
    (m14 f5/f18; the CORRECT proximal femur exists in m14 fig 1).

**Fix strategy:** the original generators were session-transient and are gone;
the broken bodies are **baked as static SVG** in each `moduleNN.html`. Regenerate
each affected body from the correct `anatomy_kit.body_group` (posed to match the
figure), keep the physics overlays (arrows/labels/COM), fix stroke widths to
~2.5–3 px slim markers, then re-run the 9 hard gates on each touched module.

## Confirmed defects (coordinate-verified)

### Module 8 — 17 flagged (10 defect, 7 minor)
- **defect**: f3 (single-capsule stance leg, no knee/ankle/foot; neck-ball head),
  f7 (walker inset: floating head + 2 foot dots, no body), f8 (same, head
  missing), f11 (falling elder: 2 capsules + flat head, no arms/2nd leg/foot;
  blob "floor"), f17 (ankle arrow tip in empty space), f18 (one-leg body, no
  foot), f19 (legs drawn ~horizontal → looks seated splayed), f24 (one-leg,
  single capsule, no knee/foot), f28 (one-leg, no foot), f39 (no pelvis/legs/feet
  — trunk stops mid-air).
- **minor**: f5, f10 (neck-ball/flat head), f20, f31 (foot floats above slope),
  f23 (detached alpha-leg sphere), f25 (one arm, no feet), f41 (one arm, no feet).
- clean: f1, f9, f12, f13, f16, f21, f22, f26, f27, f32, f35.

### Module 9 — 12 flagged (root: broken standing-body generator + anterior-shank pose)
- **defect**: f2 (5 of 6 legs bend knee backwards), f13 (one arm through the head,
  front leg no knee), f14 (right body: no legs — floor-length "gown", zero-length
  shank, no feet; COM dots inside head), f17 (same gown body; label over head),
  f20 (left gown body + right diamond legs), f27 (gown body), f32 (gown body).
- **minor**: f1 (both running feet piled on one spot), f2 (no feet), f9 & f19
  (muscle-tendon: no shank/calcaneus), f18 (diamond legs, ankles meet at a point,
  no feet), f30 (diamond legs, no elbow).
- clean: f16, f25, f26 (spring-mass abstraction).

### Module 10 — 15 flagged (root: stroke-width slab bug + single-point-shoulder body)
- **defect (slab bug)**: f2, f3, f9, f10, f13, f16, f17, f18, f23, f30, f31, f32
  — ground `<line>` stroke-width 69–174 buries feet/lower legs; plumb/impulse
  lines are stroke-width 54–165 barcodes; several fat-rectangle "arrows".
- **defect (body template)**: f2, f3, f15 (both arms from ONE midline point → no
  shoulder width, wishbone trunk; torso narrower than head; shank fatter than
  thigh; feet only ~13% stature and both point +x), f30 (stepping leg single
  capsule, no knee/foot).
- **minor**: f5 (ground block offset left of feet), f20 (short ground + label over
  head).
- clean: f1, f21, f24, f29.

### Module 12 — 8 flagged (all defect; one shared seated-body generator)
- f1, f5, f14, f17, f28, f36 (head detached 8.7 px + ~2× undersized, seated
  body), f40 (same + forearm ends with no hand), f21 (standing walker: head
  detached; **neither shank has a foot** — 2 foot ellipses pile in the midline
  below both ankles).
- clean: f16, f18, f22. Note: seated figures draw only one arm/leg (sagittal
  occlusion — not counted).

### Module 13 — 19 flagged (17 defect, 2 minor)
- **defect**: f2 (4 montage bodies: no arms/feet, detached heads, 2 one-leg),
  f4 (worst head gap 19.9 px; no arms; footless; W arrow stroke-width 16 red
  bar), f5 (**trunk column, no legs** — climbing stairs!), f6 (detached head, one
  footless leg), f9 (**trunk column, no legs** — incline walk), f15 (both chairs:
  detached head, one leg, no foot), f16 (**trunk columns** — stairs up/down),
  f17 (one footless leg, one arm), f18 (squat/stoop: one footless leg — foot
  placement is the whole point), f19 (detached head, one arm, one footless leg),
  f23 (**trunk columns** — slope), f25 (head 17 px off; no arms; footless), f31
  (detached head; no arms; one footless leg; no chair), f33 (one footless leg —
  the recovery STEP is missing), f34 (one arm, one footless leg).
- **minor**: f1 (sit pose reads as backward lunge), f8 & f21 (jar "hand" = 8
  evenly-spaced pads, not a 4-fingers+thumb grip), f27 (one leg/arm, footless).
- clean: f7, f11, f20, f22, f28, f29, f30 (top-view / plot / point-mass).

### Module 14 — 4 flagged (2 defect, 2 minor) — regional femur only, no whole bodies
- **defect**: f5, f18 (femur head bolted on shaft axis, **no neck/trochanter**;
  fall arrow aimed at head not lateral greater trochanter — CORRECT femur is in
  fig 1).
- **minor**: f17, f32 (neck-less femur icon).

### Module 15 — flagged (2 defect + non-Winter problem-body generator)
- **defect**: f3 (knee broken open 21.5 px AND bends backwards; one leg/arm; foot
  detached), f4 (**whole body drawn twice** with 25 px offset → doubled head +
  capsule pile; markers 22–47 px off their segments; foot detached 40 px).
- **minor**: f1 (one foot, one arm; neck ball 71% of head), f3/f4/f8 (flat
  unshaded heads), figs 21/25/26/30/32/33/41 (reusable problem body is non-Winter:
  hip at 42.6% stature vs 53%, big head, short legs, 8% feet floating above the
  plate), figs 16/17/31 (head + single capsule, no limbs).

### Module 16 — clean (no anatomy; stress cubes / bars / beam are intentional)
- Non-anatomy note: f14 & f26 label shear symmetry "σxx = σxx" (should be
  σxy = σyx); f25 writes Cauchy "t = σxx nx" (should be tᵢ = σᵢⱼ nⱼ). Outside the
  anatomy goal but worth a correctness fix.

### Module 17 — clean (fig 1 flowchart; decorative icon only)

### Module 4 — 1 defect
- **defect**: f15 (load arrow stroke-width 20.8, tip 18 units left of the condyle
  → "F=R≈1715 N" points into empty space; fat wedge head). clean: f1,3,24,27,33.

### Module 5 — 1 defect (its only body figure)
- **defect**: f1 — (a) `#b_bone`/`#b_sph` defs are defined AFTER the figure →
  **tibia does not render** (m05 has no hidden pre-defs `<svg width=0>` block that
  every other module has); (b) tibia floats 17 units above the foot, no ankle;
  (c) Achilles inserted anterior to the ankle (drawn as a dorsiflexor); (d)
  dangling `url(#a_blu)` marker (no head). **Fix: move defs ahead of fig 1 + add
  a_blu.**

### Module 6 — 3 defect, 1 minor
- **defect**: f1-left (Achilles inserted anterior/midfoot, not calcaneus), f2
  (trailing foot points backwards — 100% posterior to ankle), f21 (plantar fascia
  `<line>` stroke-width 62.9 → red slab burying arch, 22 units below ground).
- **minor**: f1-right (ACL stops inside condyle, never crosses to tibia; sw 16).
  clean: f3, f5.

### Module 7 — 10 defect, 6 minor (shared small-body generator)
- **defect**: f18 (one leg single-capsule no knee, blunt no foot; one arm no
  hand), f23/f24/f29/f30/f31/f41 (**NO THIGH** — trunk→hip→shank to foot; no
  arms; detached head no neck), f31 (+ stroke-width 21 bars burying body),
  f16 (hip HYPEREXTENDED ~52° → backbend not hip-flexion; no neck; one leg/arm),
  f42/f52 (ground `<line>` sw 145 buries + clips viewBox; only leg ends in slab
  no knee/foot; arm sprouts mid-back; head 28 units off trunk axis; r_L arrow
  sw 56).
- **minor**: f2/f15/f32 (one leg+one arm), f3 (one foot, one arm, oversized
  shoulder ball), f30 (co-contraction arrows float as "wings", sw 12), f29/f41
  (annotation slabs sw 15), f40 (head floats 6 units, no neck), f48 (lone severed
  head — no trunk/limbs). clean: f1, f17, f36.
- Analyzer: `…/a21d973c-…/scratchpad/an.py` — `an.run('moduleNN.html',{figs})`.

### Module 1 — 3 defect, 2 minor
- **defect**: f13 & f21 (byte-identical bodies — **knee bends backward** 39°
  hyperextension; problem wants a straight-legged stoop; fix knee to ~(152,210)),
  plus one-capsule arm (no elbow/forearm) and no neck.
- clean: most of m01 (f1,7,8,9,10,11,12,14,15,17,18,19,20,23,24,25,26).

### Module 2 — 1 defect, 3 minor (regional femur/bone)
- **defect**: f1-right (drawn neck-shaft angle **146°**, not the 125° stated
  twice → coxa valga; move head centre to ~(276,41)).
- **minor**: f1-right (GT a 2u notch, condyles no flare, GT/angle labels overprint
  illegibly), f5 (45° fracture line floats beside the bone, not in the shaft),
  f18-left (5 "trabecular struts" radiate into the **pelvis/ilium**, not the
  femoral head the caption names — clip fan to head+neck).

### Module 3 — 5 defect, + 1 marker bug
- **defect**: f26 (**CLIPPED** — viewBox `0 0 460 270` cuts both bodies' feet at
  y=305; fix viewBox `0 0 460 322`), f27 (cane is a rect 2× thigh thickness in
  body-material fill → reads as a third limb; make it ~5-6u, wood/grey), f29
  (labelled "index finger" drawn at the far ulnar edge opposite the thumb and 3×
  too long — index is next to the thumb, middle is longest), f35 (the "extensor"
  is drawn on the SAME anterior side as the flexor and overlaps it → no
  antagonist, defeats the co-contraction figure; redraw extensor posterior onto
  an olecranon lever).
- **minor**: f28 (swing leg has no foot).
- **marker bug (also hits others)**: f47 "Rs" arrow stroke-width 16 + `a_red`
  marker that has **no `markerUnits`** → head renders as a ~120u wedge over the
  arm. **Fix `a_red` (and siblings) with `markerUnits="userSpaceOnUse"`** in the
  shared defs. (m01's `mRed` already has it — that's why m01's thick red bars are
  fine.) f46 same arrow at sw 1.8 is fine.
- clean: m03 1,2,6,7,8,30–34,36–38,41–46,52,55.

### Module 11 — 21 defect, 4 minor (34 figures; 3 systematic generator bugs)
- **ROOT A — stroke-width = 0.30 × line length** on 108 guide/force/leader
  `<line>`s across 24 figures → opaque slabs/barcodes over the arm (e.g. f9/f22/f32
  sw 86.6 covers the whole arm; f3 sw 61.3; f6 sw 61; f16 sw 61.5; f28 sw 52.5).
  Fix once in the line helper; **exclude** the legit `#c9b79a`/`#b09a78` floor+chair
  lines (sw 37.4).
- **ROOT B — 6 figures have an EMPTY `<g filter="url(#b_sh)"></g>`: the seated
  body was never emitted at all** (f8, f11, f12, f38, f39, f45 — captions say
  "lifting"/"pinch grip"/"power grip"/"best posture"/"hand lap→cup"). Must emit
  the body.
- **ROOT C — detached head + neck-ball** (head r14 bottom y103 over a neck rect
  whose top is y113.2 = 10.2u gap; neck ball 1.35× head diameter) on 28 figures.
- **posture defects**: f16-left (elbow included angle 21° — forearm passes through
  the upper arm; shoulder 29° behind trunk), f23 (single "wave" arm **bends the
  wrong way** — forearm on the posterior side of the humerus, 34° hyperextension),
  f2 (shank ends with no ankle sphere/foot; hand a 15u stub; `hand` label 115u off
  with no leader).
- **minor**: f17/f25/f29/f33/f34/f40/f42 (arm ends in a bare capsule, no palm/
  fingers, at a "fingertip"/force target), f5/f17/f28 (faded elbow-up branch is
  the non-anatomical IK solution — caption or rotate out of plane), fat-arrow
  vectors from ROOT A.
- clean: f1 (glenoid/scapula + NIH bone art). No viewBox clipping; every arm/leg
  has both segments + elbow/knee sphere; forearm/upper-arm 1.42 is correct.

## Tally
~**115 findings across ~110 figures**; roughly **90 defect-level**. Nearly every
module affected except 16/17. Three-quarters trace to a handful of shared
generator bugs (stroke-width-slab, detached-head/neck-ball, missing-neck, empty
body group, non-Winter problem body, dangling/`markerUnits`-less arrow markers).

## Remaining broken-body DOCUMENT indices (resolved past the sheet-number mismatch)
Reconnoitered 2026-07-27 (heads+limb-rect counts). Fix via the element-wise
body-swap recipe (grab the broken limb rects+spheres, blank them, replace the head
circle with a posed `body_group`; verify by render):
- **m07** (doc `<figure>` index): **18** (bent-forward lift: 1 leg no knee/foot, 1
  arm no hand), **23** (broomstick balancer: 1 leg), **29** & **31** (two-body,
  no-thigh), **30** (icy-patch: no-thigh), **32** (stoop-lift: 1 leg), **42** &
  **52** (flexed-spine: hip hyperextension + no neck). fig3 is the clean Winter
  body; fig2 is the pendulum schematic (leave).
- **m13 remaining** (posed bodies, lower severity): detached heads + missing feet +
  one-limb on the C/D problem bodies — add a foot ellipse at each bare ankle and
  seat each head; per-figure (heads at varying coords, not a shared template).
- **m09/m10**: broken gait bodies (gown legs, backward knees) + slabs where **limbs
  are `#c98a5e` LINES** (exclude that colour from the slab-thin, or legs vanish).
- **m01 f13/f21, m15**: backward knees inside transformed groups — resolve the
  transform (or replace via body_group). **m02/m14**: neck-less femurs.

## ⚠ CRITICAL SAFETY CAVEAT (verified 2026-07-27) — do NOT blind-sweep stroke-width
**Limbs are drawn as thick `<line>`s, not just rects.** A survey of every
`<line stroke-width>15>` found that the SAME width range holds both the slab-bug
lines AND legitimate anatomy: **limb capsules `stroke="#c98a5e"` at width 15–20**
(m10 has 72, m09 has 8 — these are the actual legs/arms), **muscle bars
`#2a7d2a`/`#b0361f`/`#7a1f1f`** (m01/05/06), **floor/chair lines
`#c9b79a`/`#b09a78`/`#9a8b6a` at 37–54**, and **FEM bars `#9c8760`** (m16). A blind
"set every fat line to 3px" sweep would **turn every leg and arm into a hairline
and destroy the bodies.** The slab-bug lines must be identified **per figure by
coordinate** (the audit did this), never by width alone. Build the geometric
checker + a before/after visual baseline FIRST, then fix per-figure and re-render
to confirm nothing collapsed.

## Fix order (highest leverage first)
1. **Stroke-width fix — PER FIGURE, NOT a sweep** (see caveat above). For each
   flagged slab line (ground/plumb/force lines the audit lists by module/fig),
   thin to ~2.5–3, leaving limb/muscle/floor/FEM lines untouched. Clears the
   "slab/barcode" class across m04/06/07/10/11/12/13.
2. **Arrow markers** — give `a_red`/`a_grn`/`a_blu`/siblings
   `markerUnits="userSpaceOnUse"` in each module's shared defs (fixes wedge-blob
   heads, e.g. m03 f47, m04 f15); add the missing `a_blu` in m05.
3. **Emit the 6 empty bodies** in m11 (f8/11/12/38/39/45).
4. **Neck + head seating** — attach every detached head via a real neck capsule,
   shrink neck-balls to ~0.55× head; regenerate the shared seated/standing bodies
   from `anatomy_kit.body_group` (m11, m12, m13, m07).
5. **Feet** — emit a foot at every shank distal endpoint (m07, m09, m10, m11, m12,
   m13, m15); fix feet that float above the ground/plate.
6. **The 4 "trunk-column" no-legs bodies** m13 f5/f9/f16/f23 and the no-thigh
   bodies m07 f23/24/29/30/31/41 — draw real flexed legs.
7. **Backwards knees/elbows** — m01 f13/f21, m09 f2, m11 f16/f23, m15 f3; and
   hip-hyperextension m07 f16.
8. **m05 f1 defs-ordering** (move shared defs before the first figure).
9. **Femur neck** — m14 f5/f18 (reuse m14 f1's correct proximal femur; retarget
   fall arrow to the lateral greater trochanter); m02 f1 125° neck-shaft.
10. **Regional logic** — m03 f29 finger order, f35 antagonist side, f27 cane;
    m06 f1/f2 Achilles/foot direction, f21 fascia; m12/m13 5-digit hands.
11. **Clipping** — m03 f26 viewBox; m07 f42/f52 ground overshoot.

After each module: run the 9 hard gates (esp. `check_bodyprop`, `check_frame`,
`check_overlap`, `verify_dom`) before commit.

## Verification tooling (from the audit agents — session-transient)
- `…/a21d973c-…/scratchpad/an.py` — `an.run('moduleNN.html',{figs})` prints limb
  endpoints, joint circles, and fat lines per figure.
- `…/a21d973c-…/scratchpad/render.py` — **full-height** per-figure renderer
  (the fix for the truncation bug; use h ≈ 700×figs, not this session's capped
  `build_sheets.py`).

## Reusable renderer for verification
A full-height per-figure renderer exists at
`…/a21d973c-…/scratchpad/render.py` (from the audit agents); per-figure PNGs in
`…/scratchpad/figs/`. The `build_sheets.py` in this session's scratchpad has the
**truncation bug** (height capped) — do not trust its sheets.
