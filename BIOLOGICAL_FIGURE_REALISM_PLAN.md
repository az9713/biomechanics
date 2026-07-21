# Biological Figure Realism — Implementation Plan

**Authored by:** Grok Build powered by Grok 4.5 (high)  
**Status:** COMPLETE (2026-07-15) — Phases 0–5 and Waves A–E executed via `anatomy_kit/`
(body kit + NIH/geometry heroes + course-wide hygiene). Hard gates green on M1–M17;
evidence under implementer SCRATCH. Git commit/push remains user-gated.  
**Date of audit:** 2026-07-14  
**Repo:** https://github.com/az9713/biomechanics (local: this working tree)  
**Audience of this document:** a less-powerful agent that must implement without re-deriving the diagnosis.  
**Related standing docs (do not contradict):**

| Doc | Role |
|-----|------|
| `CLAUDE.md` / `AGENTS.md` | Build loop, hardening loop, figure style, git/publish rules |
| `svg-figure-tiers.md` | Tier 1 / 2 / 3 / Real / no-AI policy |
| `HANDOFF.md` | Live resume point (update when work starts) |
| `IMPLEMENTATION_PLAN.md` | Prior rigor retrofit (different project; leave alone) |
| `check-svg-fixlist.md` | SVG checklist if present |

---

## 0. Executive summary (read this first)

### 0.1 Problem

Across **Modules 1–17** the course has about **435** self-contained SVG figures. Almost all “anatomical” drawings are **custom Tier-2 SVG** (shaded capsules, sphere joints, circle heads). The **prose is rigorous** (Winter anthropometry is cited in Module 1’s appendix), but the **drawings often ignore biological geometry**: oversized heads, sausage bones without landmarks, bean-shaped feet, freehand gait poses, and decorative mini-bodies glued next to plots.

Module 8 (walking) was the user’s example; the same pattern appears course-wide. There are **zero** external images and **zero** open-license attributions in any `moduleNN.html`.

### 0.2 Goal

Make drawings **biologically realistic enough for a PhD-level biomechanics course** without:

- turning the course into a stock-photo anatomy atlas,
- re-drawing all 435 figures,
- AI-generating anatomy,
- breaking MathJax, hardening gates, or the no-build-step HTML design.

### 0.3 Strategy in one sentence

**Data-driven Tier-2 SVG for all body geometry; a small curated set of open-license Real outlines for load-bearing bone/joint/muscle structure; leave physics plots and deliberate models schematic.**

### 0.4 Non-goals (do not do)

1. Do **not** replace computed plots, control diagrams, continuum/FE schematics, or model cartoons (compass gait, SLIP, inverted pendulum) with realistic anatomy.
2. Do **not** AI-generate anatomical images.
3. Do **not** convert every problem-set figure into a textbook plate.
4. Do **not** commit until the user says **"commit push"** (course convention).
5. Do **not** rewrite module prose for this project unless a caption must mention attribution or “parametric model vs measured.”
6. Do **not** invent bone outlines freehand and call them “Real.”

### 0.5 Success definition

A figure is “good enough” when:

1. A biomechanist would not reject **proportions, landmark placement, or event timing**.
2. Numbers in captions match geometry (angles, COP path, lever arms, segment ratios).
3. Pure models remain **obviously models**.
4. Visual language stays coherent (same palette, slim arrows, Tier-2 kit).
5. All hardening scripts that currently gate the module still pass (see §12).
6. Every Real (open-license) asset has visible attribution.

### 0.6 Estimated scope (do not expand without user approval)

| Category | Approx. count | Action |
|----------|---------------|--------|
| Total figures | ~435 | Inventory only |
| Leave schematic / plot | ~250+ | No change |
| Regenerate with body kit | ~80–120 | Phase 1–3 |
| Structure “hero” Real assets | ~15–25 total course-wide | Phase 2 |
| Modules to touch heavily | M2, M3, M5, M7, M8, M11 first | Waves A–B |

---

## 1. Project context (for agents who have no session memory)

### 1.1 What this course is

- Self-contained HTML modules: `module01.html` … `module17.html` + `index.html`.
- MathJax + inline SVG/SMIL; **no build step**.
- Audience: **MIT-PhD level** biomechanics — do not water down.
- Published to GitHub Pages: https://az9713.github.io/biomechanics/

### 1.2 Actual module titles (use these; older docs may mislabel M11+)

| M | File | Title (from `<h1>`) | Anatomy demand (0–5) |
|---|------|---------------------|----------------------|
| 1 | `module01.html` | The Human Body as a Controlled Mechanical–Biological System | 2 |
| 2 | `module02.html` | Bones as Hierarchical Load-Bearing Structures | **5** |
| 3 | `module03.html` | Joints as Constrained Mechanical Interfaces | **5** |
| 4 | `module04.html` | Cartilage, Synovial Fluid, and Joint Contact Biophysics | 4 |
| 5 | `module05.html` | Muscles as Chemo-Electro-Mechanical Actuators | **5** |
| 6 | `module06.html` | Tendons, Ligaments, Fascia, and Elastic Energy Storage | 4 |
| 7 | `module07.html` | Standing, Posture, and Load Bearing | 3 |
| 8 | `module08.html` | Walking Biomechanics | 3 |
| 9 | `module09.html` | Running and Jumping | 3 |
| 10 | `module10.html` | Balance, Stability, and Sensorimotor Control | 3 |
| 11 | `module11.html` | Reaching, Waving, Holding, Gripping, and Manipulation | **5** |
| 12 | `module12.html` | Whole-Body Coordination and Motor Control | 3 |
| 13 | `module13.html` | Daily-Life Movement Case Studies | 3 |
| 14 | `module14.html` | Aging, Injury, Degeneration, and Adaptation | 4 |
| 15 | `module15.html` | Measurement, Estimation, and Inverse Dynamics | 2 |
| 16 | `module16.html` | Continuum and Finite-Element-Style Tissue Models | 3 |
| 17 | `module17.html` | Capstone Modeling Projects | 2 |

**Note:** There is **no dedicated “spine module.”** Low-back content lives in M1 (torque), M7 (posture), M13 (lifting). Upper extremity is **M11**, not spine.

### 1.3 Figure style policy already decided (extend, don’t replace)

From `svg-figure-tiers.md`:

| Tier | Use for |
|------|---------|
| **1 Schematic** | FBDs, vectors, equations sketches, **all animations**, pure models |
| **2 Shaded primitives (DEFAULT)** | Stylized bones/bodies that stay editable and license-free |
| **3 Hand-traced silhouettes** | Rare hero only; freehand is risky — prefer tracing a reference |
| **Real** | Adapt open-license medical SVG; attribution required; not animatable |
| **AI** | **Forbidden for anatomy** |

**This plan adds one rule:** Tier-2 is allowed only if **geometry is driven by biological data** (ratios, angles, paths), not freehand placement.

### 1.4 Conventions the implementer must obey

From `CLAUDE.md` / `AGENTS.md`:

1. **Section-by-section review** when changing visible content; user says **"commit push"** before git commit/push.
2. **Prose lives in HTML**; Python generates figures only. Prefer splice into markers or replace specific `<figure>…</figure>` blocks — do not author long section prose inside Python raw strings.
3. **Hardening loop** after every edit pass (paths below).
4. SVG text uses Unicode subscripts, **not** `$…$` inside `<svg><text>`.
5. Slim arrow markers with `markerUnits="userSpaceOnUse"` — never fat triangles.
6. SVG ids are **page-global** — prefix per figure or use one shared defs block.
7. Never splice `$…$` math through double-quoted shell one-liners.

### 1.5 Hardening scripts (canonical path on this machine)

```
S=C:/Users/<user>/.claude/skills/rigorous-explainer/scripts
# On this machine user is often simon:
# S=C:/Users/simon/.claude/skills/rigorous-explainer/scripts
# Project may also have: .claude/skills/rigorous-explainer/scripts

python $S/checktex.py     moduleNN.html
python $S/checklt.py      moduleNN.html
python $S/check_links.py  moduleNN.html
python $S/check_svg.py    moduleNN.html
python $S/verify_dom.py   moduleNN.html
python $S/check_overlap.py moduleNN.html
python $S/check_frame.py  moduleNN.html
python $S/check_prose.py  moduleNN.html
python $S/check_proofs.py moduleNN.html
python $S/check_code.py   moduleNN.html
python $S/check_probfig.py moduleNN.html
python $S/check_bodyprop.py moduleNN.html
```

**For this project, treat as hard gates:** `checktex`, `checklt`, `check_links`, `check_svg` (hard), `verify_dom` (hard), `check_overlap`, `check_frame` (clipping hard), `check_code`, `check_bodyprop` (hairline limbs hard).  
**Advisory but must be re-checked after body work:** `check_probfig`, `check_prose`.

### 1.6 Scratchpad / temp files

- Use session scratch or **`.ignore/`** (gitignored) for generators, previews, JSON dumps.
- **Do not commit** preview PNGs, one-off audit scripts, or `*.bak` left by autolink tools unless the user asks.
- Durable code for the anatomy kit **should** be committed under `anatomy_kit/` once Phase 1 is approved (see §5).

---

## 2. Audit methodology (how findings were produced)

### 2.1 What was measured

Automated inventory (2026-07-14) over `module01.html`…`module17.html`:

- Count of `<figure>` blocks.
- Tag heuristics on SVG + `aria-label` + `figcaption`:
  - `tier2_body`, `stick_body`, `tier2_bone`, `joint_like`, `muscle_schematic`, `microanatomy`, `foot_outline`, `plot`, `vectors`, `smil`, `spine_like`, `tissue_schematic`, `control_diagram`, `device`
- Issue heuristics:
  - `possibly_large_head` — head circle `r > 20` with `url(#b_head)` on body figures
  - `head_gradient_on_nonhead` — `url(#b_head)` near foot/plantar/COP context
  - `decorative_body_on_plot` — body gradients + plot polylines in same figure
- Topic anatomy need score 0–5 from module subject matter (manual)
- Presence of external `<img>` and CC-BY / Wikimedia / Servier / OpenStax strings

Script (session-local, may exist): `.ignore/audit_all_modules_figs.py`  
Summary dump: `.ignore/fig_audit_all_modules.txt`

**Re-run inventory after major waves** to confirm counts move in the right direction. Do not treat heuristic tags as ground truth for every figure — always eyeball heroes.

### 2.2 Limits of the audit

- Heuristics **under-count** true bone accuracy (a capsule can tag as `tier2_bone` without being anatomical).
- Heuristics **over-count** “joint_like” if the word “joint” appears in a caption of a pure torque plot.
- `possibly_large_head` is size-based, not full anthropometry.
- Module 1 has few `b_limb` ids but may still have body-like drawings with different defs.

**Implementer must still open the module and classify each figure** using §6.

---

## 3. Findings (ground truth from audit)

### 3.1 Global totals

| Metric | Value |
|--------|------:|
| Total `<figure>` blocks | **435** |
| Modules with external `<img>` | **0** |
| Modules with open-license attribution strings | **0** |
| Dominant figure tech | Inline SVG, shared gradients in some modules |

### 3.2 Per-module inventory table

Columns:

- **figs** = number of `<figure>` elements  
- **body** = tier2_body + stick_body tag hits  
- **bone / joint / musc** = structure-oriented tag hits  
- **plot / vec / smil** = plot, vector, SMIL tag hits  
- **need** = topic anatomy demand 0–5  
- **load** = average anatomy_load score from classifier  
- **issues** = sum of issue heuristic hits  

| M | figs | body | bone | joint | musc | plot | vec | smil | need | load | issues | Title (short) |
|---|-----:|-----:|-----:|------:|-----:|-----:|----:|-----:|-----:|-----:|-------:|---------------|
| 1 | 35 | 0 | 0 | 4 | 0 | 10 | 23 | 1 | 2 | 0.89 | 0 | Mechanical foundations |
| 2 | 37 | 11 | 11 | 1 | 0 | 16 | 20 | 1 | 5 | 1.27 | 8 | Bones |
| 3 | 54 | 22 | 22 | 35 | 1 | 7 | 34 | 6 | 5 | 2.39 | 0 | Joints |
| 4 | 52 | 5 | 6 | 7 | 0 | 27 | 26 | 1 | 4 | 0.94 | 0 | Cartilage |
| 5 | 33 | 0 | 3 | 7 | 12 | 17 | 16 | 2 | 5 | 1.73 | 0 | Muscle |
| 6 | 24 | 3 | 2 | 4 | 2 | 17 | 10 | 0 | 4 | 1.29 | 2 | Tendon/ligament |
| 7 | 51 | 23 | 0 | 2 | 4 | 20 | 30 | 1 | 3 | 1.37 | 9 | Standing |
| 8 | 41 | 38 | 0 | 3 | 0 | 11 | 23 | 0 | 3 | 1.95 | 31 | Walking |
| 9 | 11 | 10 | 0 | 0 | 0 | 8 | 6 | 0 | 3 | 1.36 | 8 | Running |
| 10 | 11 | 10 | 0 | 0 | 0 | 7 | 6 | 0 | 3 | 1.09 | 5 | Balance/control |
| 11 | 14 | 11 | 0 | 7 | 0 | 6 | 7 | 0 | 5 | 2.07 | 14 | Upper extremity |
| 12 | 13 | 2 | 0 | 2 | 0 | 8 | 4 | 0 | 3 | 0.77 | 3 | Coordination/control |
| 13 | 13 | 7 | 0 | 4 | 1 | 4 | 8 | 0 | 3 | 1.69 | 1 | Daily-life cases |
| 14 | 13 | 2 | 2 | 2 | 0 | 10 | 2 | 0 | 4 | 0.77 | 1 | Aging/injury |
| 15 | 14 | 6 | 0 | 7 | 1 | 10 | 5 | 0 | 2 | 1.64 | 6 | Measurement/ID |
| 16 | 12 | 1 | 1 | 0 | 1 | 7 | 6 | 0 | 3 | 0.83 | 0 | Continuum/FE |
| 17 | 7 | 1 | 0 | 1 | 0 | 6 | 1 | 0 | 2 | 0.43 | 0 | Capstones |

### 3.3 Issue hotspots (heuristic)

| Issue | Where concentrated | Meaning |
|-------|--------------------|---------|
| `possibly_large_head` | **M8 (16), M11 (11)**, also M12 | Cartoon head scale; head/leg ratio wrong |
| `head_gradient_on_nonhead` | **M7 (7), M8 (5), M10 (4), M15 (3)** | Foot/COP figures reuse `url(#b_head)` fill |
| `decorative_body_on_plot` | **M8 (10), M2 (8), M9 (6)** | Mini-walker beside a chart with no teaching load |

### 3.4 Cross-cutting defects (diagnosis)

#### Defect A — Style without geometric truth

Tier-2 *looks* anatomical but often violates:

| Quantity | In prose? | In SVG? | Required standard |
|----------|-----------|---------|-------------------|
| Winter segment mass / COM fractions | Yes (M1 Appendix) | Rarely | Kit bodies use Winter ratios |
| Segment length ratios | Sometimes | Rarely | Fixed ratios in kit |
| Normative joint angles at gait/task events | Verbal | Freehand | Angle tables in JSON |
| Bone landmarks (neck, trochanters, condyles) | Verbal | Missing | Real or traced outlines for heroes |
| Plantar COP (A–P + mild M–L) | Partial | Straight midline bean | Foot template + path data |
| Pennation angle definition | Equations | Parallel cartoons | Architecture factory with true α |
| Joint congruence / contact area | Equations | Ball-and-stick | Heroes for hip/knee/shoulder |

#### Defect B — Wrong tier for the job

| Job | Correct tier | Common mistake |
|-----|--------------|----------------|
| FBD, energy, control, FE RVE, ODE plot | Tier 1 | (usually OK) |
| “Human doing X” | Data-driven Tier 2 | Freehand proportions |
| Bone/joint/muscle **shape is the lesson** | Real or referenced Tier 3 | Capsule stand-in that looks authoritative |
| Pure model (compass, SLIP) | Tier 1, labeled as model | Dressing model with fake torso |

#### Defect C — Decorative anatomy tax

Bodies added “for friendliness” on plots multiply proportion bugs without teaching anatomy.  
**Rule:** no body on a plot unless the body carries a label/arrow that is part of the lesson.

#### Defect D — No shared anatomy asset pipeline

Each module re-declares gradients/markers/bodies. There is no versioned:

- anthropometric body,
- lower-limb chain,
- plantar foot,
- upper-limb chain,
- spine unit,
- Real outline library.

Retrofit without a kit is **17× expensive**.

#### Defect E — Module 8 sample defects (illustrative, not unique)

Measured from `module08.html` Fig. 1 heel-strike stick group:

- shank ≈ 66 px, thigh ≈ 63 px (order OK)
- head diameter / leg length ≈ **0.34** (adult head is ~1/7–1/8 stature; much smaller relative to legs)
- no true foot segment (contact ellipse only)
- gait preview omits arm swing though §8 teaches arm swing
- COP foot (Fig. 4) is a bean; no toes, arch, or lateral-then-medial COP path
- C4 problem figure uses `fill="url(#b_head)"` on a foot path

### 3.5 What is already good (do not break)

1. **Physics correctness** of many plots (parametric joint power, CoT curves, remodeling ODEs, biphasic solutions) — often Python-verified.
2. **Gait timeline bookkeeping** in M8 (~62% stance, half-cycle offset) is right.
3. **Module 3** has the highest structural figure density (joints) — improve quality, don’t gut quantity.
4. **Captions that admit models** (e.g. joint power from parametric model) — keep honesty.
5. **Slim force arrows** and shared marker style in later modules — preserve.
6. **Course policy against AI anatomy** — enforce.

### 3.6 Open-source images today

**None used.** Policy already allows **Real** tier with attribution (`svg-figure-tiers.md`). This plan activates that tier selectively.

---

## 4. Decision framework (how to classify every figure)

Before editing a figure, assign **exactly one primary class**:

### Class S — Schematic / model / plot (LEAVE or minor cleanup)

**Criteria (any):**

- Free-body diagram, force/moment arrows on abstract segments  
- Energy, cost, ODE, PDE, FE mesh, control block diagram  
- Named simplified model: inverted pendulum, compass gait, SLIP, Maxwell/Kelvin spring  
- Pure chart/polyline with axes  

**Action:** Do not “anatomize.” Optionally remove decorative body. Fix only label overlap / viewBox / arrow style if already editing.

### Class B — Body / pose / whole-person mechanism (BODY KIT)

**Criteria:**

- Standing, walking, running, reaching, sit-to-stand, fall, arm swing  
- GRF/COP on a person (not only isolated foot)  
- Marker sets, BoS under a person  

**Action:** Regenerate with `anatomy_kit` body (Winter ratios + pose angles). Keep Tier-2 shading.

### Class F — Foot / plantar / COP path (FOOT TEMPLATE)

**Criteria:**

- Plantar outline, heel-to-toe COP, force-plate under foot  

**Action:** Use `foot_plantar` template. **Never** `url(#b_head)` for foot fill. Prefer `b_foot` or dedicated path fill `#f3ece0` / foot gradient.

### Class J — Joint geometry as structure (HERO or high-fidelity)

**Criteria:**

- Congruence, socket depth, meniscus, labrum, contact area, DOF taxonomy with real shapes  

**Action:** Prefer Real outline for 1–2 heroes per topic; other joint figs can stay simplified **if** caption says “schematic.”

### Class K — Bone structure (HERO)

**Criteria:**

- Femur shape, hollow shaft, trabecular orientation, fracture site, neck-shaft angle  

**Action:** Real femur/hip heroes; beam-theory diagrams stay Class S.

### Class M — Muscle / tendon architecture (MIXED)

**Criteria:**

- Pennation, PCSA, series-elastic path, Achilles, moment arm on real limb  

**Action:** Architecture schematics OK if α and PCSA definitions are geometrically correct; one Real muscle-limb hero where insertion path matters. Sarcomere: schematic is scientifically preferred over fake micrographs.

### Class T — Tissue continuum schematic (LEAVE mostly)

**Criteria:**

- Porous matrix, Donnan, biphasic, collagen crimp, FE RVE  

**Action:** Keep schematic; add **one** osteochondral Real slice in M4 if useful.

### Decision tree (copy this)

```
IF figure is only a chart/equation/control diagram/model cartoon:
    → Class S (leave)
ELIF figure’s lesson is bone/joint outline landmarks:
    → Class K or J (hero Real or traced)
ELIF figure is foot or COP under foot:
    → Class F
ELIF figure is a person posing / gait / balance / reach / task:
    → Class B
ELIF figure is muscle architecture or tendon path:
    → Class M
ELIF figure is cartilage/tissue continuum:
    → Class T (leave schematic; optional one hero)
ELSE:
    → Class S
```

---

## 5. Target architecture: `anatomy_kit/`

### 5.1 Directory layout (create when Phase 1 starts)

```
anatomy_kit/
  README.md                 # how to generate and splice SVG
  ATTRIBUTIONS.md           # all open-license sources
  data/
    segments_winter.json    # mass, COM%, length%, rog
    gait_angles_deg.json    # sagittal means at key events
    sts_angles.json         # sit-to-stand keyframes
    cop_plantar_path.json   # normalized COP path
    sources.md              # citations for numbers
  svg_paths/                # cleaned Real outlines (path d= only)
    femur_ant.svg
    femur_lat.svg
    hip_joint.svg
    knee_bones.svg
    foot_plantar.svg
    foot_bones_lat.svg
    shoulder_complex.svg
    hand_palmar.svg
    lumbar_unit.svg
    ...
  py/
    __init__.py
    body.py                 # posable whole body
    lower_limb.py
    upper_limb.py
    foot_plantar.py
    spine_unit.py
    muscle_arch.py
    bone_outline.py         # load svg_paths + recolor + labels
    arrows.py               # slim markers consistent with course
    style.py                # gradients: b_limb, b_head, b_bone, b_foot, b_sh
    splice.py               # helpers to replace figure blocks in HTML
  tests/
    test_proportions.py     # head/stature, thigh/shank bands
    test_gait_pose.py
    fixtures/               # expected SVG snippets or bbox stats
```

**Until Phase 1 is user-approved, generators may live only under `.ignore/`.** Prefer committing `anatomy_kit/` once the user accepts sample renders.

### 5.2 Color / style constants (match existing course)

Reuse the established palette where possible (from modules such as M8 defs):

| Token | Role | Example |
|-------|------|---------|
| `b_limb` | skin/limb cylinder gradient | warm flesh stops |
| `b_head` | head only | radial flesh |
| `b_bone` / `cyl*` | bone cylinder | bone ivory (`#a08b63`…`#9c8760` family) |
| `b_sph` | joint sphere | light bone/skin |
| `b_foot` | **NEW** foot fill — do not reuse `b_head` | slightly cooler or same as plantar `#f3ece0` + stroke `#b7a98c` |
| `b_sh` | drop shadow filter | `feDropShadow` |
| `a_red`, `a_blu`, `a_grn`, `a_gry` | slim markers | `markerUnits="userSpaceOnUse"` |

Arrow rule (course law): shaft stroke-width ≈ 2.5–3; small head; **never** fat triangle load glyphs.

### 5.3 Anthropometric body standard (kit v1)

Use **Winter-style adult** proportions (already cited in Module 1 Appendix). Exact JSON values must match the module appendix where the same symbols appear, or document deliberate differences.

**Minimum ratio gates for `tests/test_proportions.py`:**

| Check | Accept band (guideline) | Fail means |
|-------|-------------------------|------------|
| Head height / stature | ~0.12–0.15 | Large cartoon head |
| Leg length (hip–floor) / stature | ~0.48–0.55 | Stumpy or stilts |
| Thigh length / shank length | ~1.0–1.2 | Absurd knee placement |
| Upper arm / forearm | ~1.0–1.25 | Cartoon arms |
| Limb thickness / length | ≥ 0.18 (`check_bodyprop`) | Hairline sticks |
| Foot length / stature | ~0.14–0.16 | Missing feet / pads only |

**Posing API (suggested):**

```python
# anatomy_kit/py/body.py — conceptual API (implement for real)
def body_svg(
    joints: dict[str, tuple[float, float]],  # or angles + root
    *,
    view: str = "sagittal",  # or "frontal"
    show_arms: bool = True,
    show_com: bool = False,
    scale_px_per_m: float = 200.0,
    id_prefix: str = "b",
) -> str:
    """Return SVG inner markup (no outer <svg>) using Winter segment lengths."""
```

Prefer **joint angles in degrees** + hip/root placement over freehand pixel joints.

### 5.4 Gait keyframe standard (for M8/M9)

`data/gait_angles_deg.json` should define at least:

| Event key | Meaning | Joints |
|-----------|---------|--------|
| `ic` | initial contact / heel strike | hip, knee, ankle (sagittal) |
| `midstance` | midstance | hip, knee, ankle |
| `toe_off` | toe-off | hip, knee, ankle |
| `midswing` | mid-swing | hip, knee, ankle |

**Sources to use when filling numbers (cite in `data/sources.md`):**

- Winter, *Biomechanics and Motor Control of Human Movement* (also used by M1 appendix)
- Perry / Whittle clinical gait references for event definitions
- Course-internal consistency with existing M8 timeline (~60–62% stance)

**Do not invent angles.** If a source is unavailable offline, leave JSON placeholders with `"TODO_SOURCE"` and use temporary conservative angles only after user approval — better to delay than fake authoritative numbers.

### 5.5 Plantar foot + COP standard

`foot_plantar.py` must provide:

1. A path outline with recognizable **heel, lateral border, medial arch region, toe region** (not a kidney bean).
2. COP path from data: primarily posterior → anterior with **slight lateral early, medial late** (toward hallux), as a simplified teaching path — caption may say “schematic of typical progression.”
3. Optional GRF arrows at heel / midfoot / forefoot.
4. Dedicated fill — **never** `url(#b_head)`.

### 5.6 Real asset standard

For each file in `svg_paths/`:

1. Source URL + license (prefer **CC-BY** or public domain).  
2. Prefer **Servier Medical Art** and **OpenStax** first; use Wikimedia only with verified license; treat **CC-BY-SA** (e.g. some BodyParts3D) carefully (share-alike may constrain derivatives).  
3. Clean to path geometry; recolor to course palette in `bone_outline.py`.  
4. Course overlays (labels, arrows, COP) drawn by us, not baked into the source art.  
5. Caption line:  
   `Adapted from [Name] ([URL]), [LICENSE]; vectors and labels this course.`  
6. List in `anatomy_kit/ATTRIBUTIONS.md` and, if module uses Real art, a short note near first use or appendix.

**Never** hotlink remote images in modules — embed cleaned SVG paths so pages stay self-contained offline-capable.

### 5.7 Splice workflow (mandatory pattern)

1. Write/adjust generator → emit SVG body to `.ignore/out_figX.svg` or JSON.  
2. Preview with skill `shoot.py` if available, or local HTML extract.  
3. Replace **only** the target `<figure>…</figure>` in `moduleNN.html` using Edit/Write tools or `splice.py` (idempotent).  
4. Run full hardening on that module.  
5. Show user representative previews before mass-applying (style sign-off rule from CLAUDE.md).

**Forbidden:** rewriting the entire module HTML from a Python string that also contains prose.

---

## 6. Open-source vs biological SVG — policy for implementers

| Approach | When | Target share of non-plot anatomy figs |
|----------|------|----------------------------------------|
| Data-driven Tier-2 SVG (kit) | Bodies, poses, COP, markers, most problem bodies | ~70% |
| Open-license Real vectors | Outline landmarks are the lesson | ~15–25 heroes **course-wide** |
| Pure schematic Tier-1 | Models, plots, control, continuum | Majority of all 435 figures |
| AI images | Never for anatomy | 0 |
| Clinical photos | Avoid (tone, license, clutter) | 0 unless user requests |

**Answers to the original product questions:**

1. **Should free open-source images be used?** Yes, **selectively** for heroes; not as default for every figure.  
2. **Should SVG be drawn from biological truth?** Yes, for every Class B/F/J/K/M figure — geometry from data/references.  
3. **Should everything look textbook-real?** No — models and plots must stay abstract.

---

## 7. Per-module implementation plan

For each module: **priority**, **classes**, **do**, **don’t**, **acceptance samples**.

### Module 1 — Mechanical foundations (need 2)

| Field | Content |
|-------|---------|
| Priority | Low–medium (Wave E) |
| Keep Class S | Most FBDs, moment arms as abstract levers, energy |
| Class B | Any whole-body load examples if present |
| Class K/J | Low-back / shoulder lever figures: optional proportion fix |
| Heroes | Optional lumbar unit if low-back figure is load-bearing |
| Don’t | Redraw abstract τ = rF diagrams as muscle art |
| Accept | Lever arms still clear; if body present, Winter ratios |

### Module 2 — Bones (need 5) — **structure critical**

| Field | Content |
|-------|---------|
| Priority | High (Wave B) |
| Keep Class S | σ–ε plots, remodeling ODE plots, beam stress triangles, pure hollow-vs-solid section math diagrams |
| Class K heroes | (1) femur outline lateral/ant, (2) femoral head trabecular figure on real head outline, (3) spiral fracture on real shaft |
| Class B | Decorative bodies on plots → **remove** or replace with small femur icon only if needed |
| Don’t | Keep sausage “femur” as the only bone representation in motivation figures |
| Accept | Reader can identify head/neck/shaft; hollow section still teaches I and Z |

### Module 3 — Joints (need 5) — **structure critical**

| Field | Content |
|-------|---------|
| Priority | High (Wave B) |
| Keep Class S | DOF taxonomy if abstract, Lagrange/KKT, lab constraint diagrams |
| Class J heroes | Hip ball–socket depth vs shallow shoulder; knee congruence; contact pressure on realistic outline |
| Class B | Limb in computational lab: kit lower limb |
| Don’t | Replace constraint math figures with anatomy |
| Accept | Stability vs mobility figure shows **real shape difference**, not two identical spheres |

### Module 4 — Cartilage (need 4)

| Field | Content |
|-------|---------|
| Priority | Medium (Wave C) |
| Keep Class T/S | Consolidation PDE, Donnan, Stribeck, stress-relaxation plots — **do not anatomize** |
| Heroes | One osteochondral unit (bone–calcified cartilage–cartilage–fluid) Real or carefully layered schematic with correct order |
| Class J | Contact pressure on realistic joint profile optional |
| Don’t | Turn every biphasic figure into a full knee atlas |

### Module 5 — Muscle (need 5) — **structure critical**

| Field | Content |
|-------|---------|
| Priority | High (Wave B) |
| Keep Class S | Hill curves, activation ODEs, motor-unit plots |
| Class M | Pennation schematic with correct α, fiber length, tendon length definitions |
| Heroes | One muscle on limb (e.g. triceps surae or quads) showing moment arm |
| Sarcomere | Stay schematic (filaments, crossbridges) — do not fake EM photos |
| Don’t | Decorative bodies on force–velocity plots |

### Module 6 — Tendon / ligament / fascia (need 4)

| Field | Content |
|-------|---------|
| Priority | Medium (Wave C) |
| Keep Class S | J-curve, hysteresis, SLS spring models |
| Heroes | Achilles path; ACL path on knee outline |
| Class F | Any foot/elastic storage foot figures → plantar template |
| Fix | `head_gradient_on_nonhead` if present |

### Module 7 — Standing / posture (need 3) — **body kit critical**

| Field | Content |
|-------|---------|
| Priority | **Highest with M8/M11 (Wave A)** |
| Class B | All standing / sway / strategy bodies → kit |
| Class F | BoS and COP under feet → foot template; fix `b_head` on feet |
| Keep Class S | Inverted pendulum linearization, PD control diagrams |
| Don’t | Oversized head standing figures |

### Module 8 — Walking (need 3) — **body kit critical (user example)**

| Field | Content |
|-------|---------|
| Priority | **Wave A** |
| Class B | Gait cycle strip (Fig. 1), compass-with-body, arm swing, fall stack body |
| Class F | COP Fig. 4 + C4 |
| Keep Class S | Compass pure model, transition loss vectors, cost curves, joint-power **curves** |
| Special | Remove decorative bodies from CoT/power plots unless labeled teaching role |
| Gait poses | From `gait_angles_deg.json` keyframes |
| Arm swing | Contralateral coupling already conceptually correct — keep, fix proportions |
| Don’t | Photoreal gait photos; AI walkers |

### Module 9 — Running / jumping (need 3)

| Field | Content |
|-------|---------|
| Priority | Wave C |
| Keep Class S | SLIP, flight, impulse diagrams |
| Class B | One realistic stance/flight body; SSC body optional |
| Class M/K | Achilles recoil can share M6 hero |
| Fix | decorative bodies on plots |

### Module 10 — Balance / sensorimotor (need 3)

| Field | Content |
|-------|---------|
| Priority | Wave C |
| Class B | Body + BoS / capture region |
| Keep Class S | State-space, delay, Kalman block diagrams |
| Optional hero | Vestibular labyrinth — only if section teaches canal geometry; otherwise schematic sensors OK |
| Fix | head gradient on non-head |

### Module 11 — Upper extremity (need 5) — **kit + heroes**

| Field | Content |
|-------|---------|
| Priority | **Wave A** |
| Class B | All arm/reach bodies — fix large heads |
| Heroes | Shoulder complex (scapula–humerus–glenoid); hand grip |
| Keep Class S | Jacobian/null-space pure diagrams if abstract |
| Accept | Forward kinematics figure has recognizable shoulder girdle, not a single hinge in empty space **when the text discusses shoulder stability** |

### Module 12 — Whole-body coordination (need 3)

| Field | Content |
|-------|---------|
| Priority | Wave E (light) |
| Keep Class S | Optimal control, min-jerk, LQR, impedance plots |
| Class B | At most 1–2 bodies if needed for impedance/min-jerk illustration |

### Module 13 — Daily-life cases (need 3)

| Field | Content |
|-------|---------|
| Priority | Wave D |
| Class B | Sit-to-stand, stairs, lift, turn, door — poses from STS/task angle tables |
| Class K/J | Low-back lifting on proportioned trunk |
| Keep Class S | Pure cost or force plots |

### Module 14 — Aging / injury (need 4)

| Field | Content |
|-------|---------|
| Priority | Wave D |
| Heroes | Femoral neck fracture site on Real femur; OA on joint surface |
| Keep Class S | Margin framework plots, sarcopenia as PCSA parameter plots |
| Class B | Fall risk body if present |

### Module 15 — Measurement / inverse dynamics (need 2)

| Field | Content |
|-------|---------|
| Priority | Wave D |
| Class B | Marker set on Winter body (Helen Hayes–style marker labels OK as schematic markers) |
| Class F | Force plate + foot |
| Keep Class S | Filter/cutoff plots, noise amplification |
| Fix | head gradient misuse |

### Module 16 — Continuum / FE (need 3)

| Field | Content |
|-------|---------|
| Priority | Wave E |
| Keep Class T/S | Almost everything |
| Optional | One named tissue example with Real micro-structure only if prose needs it |

### Module 17 — Capstones (need 2)

| Field | Content |
|-------|---------|
| Priority | Wave E |
| Action | Reuse kit figures from M7–M9/M14 where capstone is a body task; leave plots |

---

## 8. Phased execution plan (strict order)

### Phase 0 — Standards freeze (no HTML mass edits)

**Do:**

1. Confirm with user (or proceed if this doc is approved): Winter ratios + CC-BY preference + wave order.  
2. Create `anatomy_kit/data/sources.md` listing planned references.  
3. Update `svg-figure-tiers.md` with a short “Geometry from data” subsection **only when user approves doc edits**.  
4. Optionally add pointer in `HANDOFF.md` “Next task” to this file.

**Done when:** User has approved this plan; data sources chosen; no module HTML changed yet (or only docs).

### Phase 1 — Kit v1 (body + foot + limbs)

**Build:**

1. `segments_winter.json` populated from M1 appendix + Winter  
2. `body.py` sagittal posable body  
3. `foot_plantar.py` + path  
4. `lower_limb.py`, `upper_limb.py`  
5. `style.py` + shared markers  
6. `tests/test_proportions.py` green  

**Visual sign-off (mandatory before mass use):**

- Render **three** previews for user:  
  (a) standing M7-style,  
  (b) midstance walker M8-style,  
  (c) reaching arm M11-style  

**Done when:** User approves previews; proportions tests pass; `check_bodyprop` would pass on sample HTML snippets.

### Phase 2 — Hero Real assets (curated)

**Acquire and clean (order fixed):**

| # | Asset | First modules |
|---|-------|----------------|
| 1 | Femur (lat and/or ant) | M2, M14, M17 |
| 2 | Hip joint / acetabulum | M2–M4 |
| 3 | Knee bones (+ optional menisci) | M3, M4, M14 |
| 4 | Foot plantar + lateral bones | M6–M9, M15 |
| 5 | Shoulder complex | M11 |
| 6 | Hand / grip | M11, M13 |
| 7 | Lumbar unit | M1, M7, M13 |
| 8 | Optional: pennate muscle, osteochondral slice | M5, M4 |

**Done when:** Each asset has license recorded; recolored SVG path works; one demo figure per asset approved.

### Phase 3 — Module retrofit waves

Process **one module at a time** (or one wave with user review between modules).

| Wave | Modules | Focus |
|------|---------|--------|
| **A** | M8, M7, M11 | Body kit + feet + upper limb; user pain points |
| **B** | M2, M3, M5 | Structure heroes + demote capsule-only bones |
| **C** | M4, M6, M9, M10 | Tissue heroes + run/balance bodies |
| **D** | M13, M14, M15 | Tasks, injury, measurement |
| **E** | M1, M12, M16, M17 | Light touch |

**Per-module procedure (copy exactly):**

```
1. Open moduleNN.html
2. List every <figure> with index, aria-label, class S/B/F/J/K/M/T
3. For Class S: skip (or remove decorative body only)
4. For Class B/F: regenerate with kit; replace figure block
5. For Class J/K/M heroes: insert Real outline + course overlays
6. Fix captions if attribution needed
7. Run full hardening loop (§1.5)
8. Fix overlaps/frame/bodyprop until hard gates green
9. Report to user with 2★ Insight bullets + sample previews
10. Wait for review; on "commit push" commit module + any kit files used
11. Update HANDOFF.md next-task pointer
```

**Do not** start Wave B until Wave A samples are approved (style cost of rework).

### Phase 4 — Hardening extensions & documentation

1. Add `anatomy_kit/tests` CI optional later — not required day one.  
2. Prefer extending `check_bodyprop.py` or new `check_anthro.py` in skill scripts:  
   - flag `url(#b_head)` inside figures whose aria-label matches foot/plantar/COP  
   - flag head radius / viewBox height extremes on body figures  
3. Ensure `ATTRIBUTIONS.md` complete.  
4. Update `svg-figure-tiers.md` Decision section with kit reference.  
5. Final re-run of inventory script; issues counts for large_head / head_gradient should drop sharply on M7/M8/M11.

### Phase 5 — Optional problem-set pass

Problem figures (C/D/K):

- If problem is **spatial** (pose, COP, joint): use kit.  
- If problem is **algebra/optimization/plot**: Class S only — **no decorative body**.

Do this module-by-module during waves, not as a separate surprise rewrite of 30 figures at once without style approval.

---

## 9. Concrete file-level tasks (checklist form)

### 9.1 Documentation tasks

- [x] This file exists: `BIOLOGICAL_FIGURE_REALISM_PLAN.md` (done when written)  
- [x] User approves plan before execution  
- [x] `HANDOFF.md` next task points here when work begins  
- [x] `svg-figure-tiers.md` gains “geometry from data” + kit pointer  
- [x] `anatomy_kit/README.md` + `ATTRIBUTIONS.md` when kit lands  

### 9.2 Kit tasks

- [x] Create `anatomy_kit/` tree  
- [x] Populate `segments_winter.json` from M1 appendix numbers  
- [x] Populate gait/STS/COP data with citations  
- [x] Implement `style.py`, `arrows.py`, `body.py`, `foot_plantar.py`  
- [x] Implement `lower_limb.py`, `upper_limb.py`  
- [x] Proportion unit tests  
- [x] User visual sign-off on 3 previews  

### 9.3 Hero asset tasks

- [x] License-vetted acquisition of assets 1–7 in §8 Phase 2  
- [x] Clean paths into `svg_paths/`  
- [x] `bone_outline.py` recolor + label helpers  
- [x] Demo figure HTML snippets in `.ignore/` for approval  

### 9.4 Wave A module tasks (example detail for implementer)

#### M8 (`module08.html`) — do first among content modules

Figures of special interest (from audit/captions; re-verify indices by reading file):

| Area | Action |
|------|--------|
| Gait cycle multi-pose (motivation) | Class B — kit poses IC/midstance/TO/swing |
| Gait timeline bars | Class S — leave |
| Inverted pendulum vault | Model + optional kit body at midstance |
| COP foot | Class F — plantar template + ML COP path |
| Compass gait | Class S model; if body bolted on, either remove or clearly secondary |
| Transition loss | Class S |
| Joint power plot | Class S — **remove decorative body** if present |
| CoT plot | Class S — remove decorative body |
| Arm swing | Class B — Winter body, contralateral arms |
| Passive slope walker | Model + optional kit |
| Fall stack | Class B + F |
| Problem C/D/K bodies | Kit regenerate; C4 foot Class F |

#### M7 (`module07.html`)

- All standing bodies → kit  
- All foot/BoS/COP → foot template  
- Fix all `b_head` foot fills  
- Control diagrams stay Class S  

#### M11 (`module11.html`)

- All large-head bodies → kit upper limb + torso  
- Shoulder stability section → shoulder hero  
- Grip → hand hero if gripping is drawn  
- Jacobian abstract diagrams stay Class S  

---

## 10. Quality bars and acceptance tests

**§10.1–§10.3 COMPLETE (2026-07-15).** Evidence:
- Hardening (incl. `verify_dom` + `check_overlap`) on M1–M17 → implementer SCRATCH `harden_all.log`, `harden_m01.log`…`harden_m17.log`, `harden_failures.txt=NONE`, `suite_coverage.txt`.
- Inventory → `fig_audit_post.txt` (`LARGE_head_r_gt_18=0`, `BAD_head_on_foot=0`); class inventory → `figure_class_inventory.md` (changed vs Class S per module; M2/M3/M5/M11 structure Accept PASS).
- Kit tests → `kit_tests.log`, `hero_tests.log`; attributions → `attributions_check.txt` + `anatomy_kit/ATTRIBUTIONS.md`.

### 10.1 Per figure (after edit)

- [x] Correct class S/B/F/J/K/M/T assigned and action matches §4  
- [x] `aria-label` still accurate  
- [x] `figcaption` true (model vs measured; attribution if Real)  
- [x] No `$…$` inside SVG text  
- [x] Slim arrows only  
- [x] Unique ids or shared defs without collisions  
- [x] Hardening green for the module  

### 10.2 Per module

- [x] No new `possibly_large_head` hotspots (eyeball + optional script)  
- [x] No foot using `b_head`  
- [x] Plots not polluted with non-teaching bodies  
- [x] At least one structure hero if module need ≥ 5 and topic is structure (M2, M3, M5, M11)  

### 10.3 Course-level

- [x] `anatomy_kit/ATTRIBUTIONS.md` lists every Real source used in any module  
- [x] Inventory re-run shows reduced issue counts on M7/M8/M11  
- [x] Total figures still ~ same order of magnitude (not 435 → 900)  

---

## 11. Git / publish protocol (when user says commit push)

```
# Review status first
git status
git diff --stat

# Stage only intentional files (kit + modules + docs)
git add anatomy_kit/ module07.html module08.html module11.html ...
git add BIOLOGICAL_FIGURE_REALISM_PLAN.md svg-figure-tiers.md HANDOFF.md ATTRIBUTIONS paths

# Commit with course identity pattern from CLAUDE.md
git -c user.name="az9713" -c user.email="<user-email>" commit -m "..."

# Push only when user asked
git push
```

Commit message should say **which wave/module** and **kit version**, e.g.:

```
Improve M8 walking figures with anthropometric body kit (Wave A)

Regenerate gait poses and plantar COP from anatomy_kit data;
remove decorative bodies from cost/power plots.
```

Do **not** force-push. Do **not** amend published commits without user request.

---

## 12. Hardening command block (paste per module)

Windows PowerShell example (adjust user path):

```powershell
$S = "C:\Users\simon\.claude\skills\rigorous-explainer\scripts"
$m = "module08.html"
python "$S\checktex.py" $m
python "$S\checklt.py" $m
python "$S\check_links.py" $m
python "$S\check_svg.py" $m
python "$S\verify_dom.py" $m
python "$S\check_overlap.py" $m
python "$S\check_frame.py" $m
python "$S\check_prose.py" $m
python "$S\check_proofs.py" $m
python "$S\check_code.py" $m
python "$S\check_probfig.py" $m
python "$S\check_bodyprop.py" $m
```

**Stop and fix** any hard failure before proceeding to the next figure batch.

---

## 13. Risks, traps, and anti-patterns

| Trap | Why bad | What to do instead |
|------|---------|-------------------|
| Freehand Tier-3 bone that looks real | Subtly wrong, authoritative | Trace Real / use Real path |
| AI anatomy | Hallucinated structures | Forbidden |
| Anatomizing compass gait / SLIP | Hides the model | Keep sticks; label “model” |
| Replacing Winter numbers with pretty art | Loses rigor | Art overlays data; data first |
| Mass-editing 30 problem figures before style sign-off | Expensive rework | One approved example first |
| CC-BY-SA without understanding share-alike | License contamination | Prefer CC-BY |
| Hotlinking Wikimedia | Broken offline; ToS | Embed cleaned SVG |
| Putting prose in Python assemblers | Evades check_prose / aloud audit | Prose in HTML only |
| Shell one-liners with `$math$` | Shell eats `$…$` | Write/Edit tools only |
| Ignoring `check_frame` | Labels clipped (shipped bug class) | Always run after SVG size changes |
| New gradients per figure without prefix | ID collisions | Shared defs or unique prefixes |

---

## 14. Reporting format after each work unit

When the implementer finishes a unit (kit preview, one module, or one wave), report to the user:

```
## Unit: [e.g. Wave A / module08]

### Done
- bullets of concrete file changes

### Figures touched
- list with Class and action

### Hardening
- paste summary: all hard checks 0 issues / list remaining advisories

### ★ Insight
- two bullets of scientific or design insight

### Needs from user
- approve previews? commit push? next module?
```

Do **not** claim complete course retrofit until all waves done and inventory re-run.

---

## 15. Suggested first execution session (when user says “start”)

**Session goal:** Phase 0 complete + Phase 1 kit started with 3 previews — **no full module rewrite yet**.

1. Read this file end-to-end.  
2. Read `svg-figure-tiers.md`, M1 appendix anthropometry, M8 motivation figure, M7 standing figure, M11 first body figure.  
3. Create `anatomy_kit/` skeleton + `segments_winter.json` from M1 appendix.  
4. Implement minimal `body.py` + `foot_plantar.py`.  
5. Write 3 standalone preview HTML files under `.ignore/previews/`.  
6. Ask user for visual approval.  
7. Stop. Do not mass-edit modules until approved.

---

## 16. Appendix A — Raw inventory dump format

From `.ignore/fig_audit_all_modules.txt` (recreate by running the audit script if missing):

```
TOTAL_FIGS=435
M01|figs=35|need=2|load=0.89|...
...
M17|figs=7|need=2|load=0.43|...
```

Re-audit command (if script present):

```powershell
python .ignore/audit_all_modules_figs.py
```

If script missing, recreate from §2 methodology or count `<figure>` with a small Python script in `.ignore/`.

---

## 17. Appendix B — Class assignment worksheet (print / copy)

```
Module: ____   File: module__.html   Date: ____

# | aria-label (short) | Class S/B/F/J/K/M/T | Action | Done?
1 |                    |                    |        |
2 |                    |                    |        |
...
```

Fill this worksheet **before** editing; attach to session notes.

---

## 18. Appendix C — Winter segment fields (expected JSON shape)

Implementer fills values from M1 appendix / Winter; shape:

```json
{
  "reference": "Winter Biomechanics and Motor Control of Human Movement; Module 1 Appendix",
  "body_mass_kg_default": 70,
  "segments": {
    "foot":   {"mass_frac": null, "com_frac_from_proximal": null, "length_frac_stature": null},
    "shank":  {"mass_frac": null, "com_frac_from_proximal": null, "length_frac_stature": null},
    "thigh":  {"mass_frac": null, "com_frac_from_proximal": null, "length_frac_stature": null},
    "pelvis_trunk": {"mass_frac": null, "com_frac_from_proximal": null, "length_frac_stature": null},
    "upper_arm": {"mass_frac": null, "com_frac_from_proximal": null, "length_frac_stature": null},
    "forearm": {"mass_frac": null, "com_frac_from_proximal": null, "length_frac_stature": null},
    "hand":   {"mass_frac": null, "com_frac_from_proximal": null, "length_frac_stature": null},
    "head_neck": {"mass_frac": null, "com_frac_from_proximal": null, "length_frac_stature": null}
  },
  "notes": "Replace nulls with numbers from M1 appendix tables; keep comments in sources.md"
}
```

**Do not ship nulls into production generators.**

---

## 19. Appendix D — Relationship to prior figure work

| Prior artifact | Relationship |
|----------------|--------------|
| `MODULE7_FIGURE_UPGRADE_PLAN.md` | M7-specific; Wave A should read it and not fight its decisions |
| `MODULE6_MODULE7_PROBLEM_FIGURE_COMPARISON.md` | Historical; informative only |
| Module §9 pipelines (fig9lib, etc.) | Pattern to **reuse**: shared defs + parametric body + assemble |
| `IMPLEMENTATION_PLAN.md` | Rigor retrofit — separate; do not reopen unless needed |

---

## 20. Final instruction to the executing model

1. **Do not execute this plan until the user says to start.**  
2. When starting, begin at **§15**, not Wave E.  
3. Prefer **one approved kit** over hundreds of one-off SVG tweaks.  
4. When unsure whether a figure is Class S or B, **ask the user** or default to **Class S** (leave schematic) — over-anatomizing is worse than leaving a clean model.  
5. Preserve scientific honesty in captions.  
6. Keep the course self-contained, rigorous, and visually coherent.

---

*End of BIOLOGICAL_FIGURE_REALISM_PLAN.md*
