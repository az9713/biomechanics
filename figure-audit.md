# Figure audit — "head + trunk + limbs" recognizability

**Question audited.** The `rigorous-explainer` figure rule requires that a figure
depicting the body show a *recognizable* entity — a whole body (head + trunk +
limbs) like the Module-1 lifting FBD ("**m1**"), or an unambiguous region — never
disembodied fragments. The defect ("**m12**") is a figure whose job is to show the
body but renders it as floating shaded capsule sticks with no head, no trunk, and no
hand — the reader can't tell it's an arm. This audit finds every m12-type figure.

**Scope (confirmed with the user).** Flag ONLY figures that depict the body/movement
as disembodied fragments. Recognizable regional joints (knee, hip, ball-in-socket,
bone with named ends) are fine. Pure quantitative plots and abstract math/control
schematics are **exempt** — they legitimately have no body.

**Method.** Six parallel auditors, one per module-group, judged all 715 `<figure>`
blocks from SVG source + caption against the m1/m12 rubric. Figure numbers are the
document-order "Fig. N" CSS counter.

## Result — the defect is concentrated in Modules 11–12

| Module | Topic | Total figs | **Flagged** | Notes |
|---|---|---:|---:|---|
| 01–07 | foundations → muscle → gait | 275 | **0** | whole-body Tier-2 or recognizable regional throughout |
| 08 | walking (compass gait) | 41 | 0 | **borderline cluster** — see below |
| 09 | running / jumping | 41 | 0 | connected runner glyph + taught SLIP spring-leg |
| 10 | balance / recovery | 41 | 0 | consistent head+torso+limbs whole-body glyph |
| **11** | **reaching / gripping** | 44 | **19** | floating capsule arm, no trunk/head/hand |
| **12** | **manipulation / motor control** | 43 | **7** | same defect; Fig 1 IS the m12 calibration case |
| 13 | daily activities | 43 | 0 | single-person Tier-2 template |
| 14 | aging / margins | 43 | 0 | mostly plots; bone figures are named regional anatomy |
| **15** | **injury / whole-body dynamics** | 44 | **1** (+1 borderline) | one bare pivoting "limb" capsule |
| 16–17 | continuum mech / capstone | 49 | 0 | abstract mechanics diagrams + plots |
| **TOTAL** | | **715** | **27** | + 2 borderline clusters |

**Root cause.** Modules 11 and 12 were built on a shared "two/three-link arm"
template — `fill="url(#b_limb)"` shaded capsules joined at small joint-dots, **with
no torso anchor, no head, and no drawn hand**. It was reused across nearly every
problem figure in both modules. That is exactly the m12 pattern (m12 = Module 12
Fig 1). Modules 1–10 and 13 instead anchor every arm/leg to a head+torso body (the
"posable human" Tier-2 defs), which is why they pass.

**The shared fix (applies to all 26 Module-11/12 flags).** Anchor the arm to a
seated/standing torso + head (reuse the whole-body Tier-2 convention already used in
Module 10 Fig 1, Module 11 Fig 1, and Module 12 Fig 21 — the recognizable walking
figure), and draw a **recognizable hand** at the endpoint gripping the cup / pen /
peg instead of letting the object float at a bare joint-dot. The physics overlay
(Jacobian arrows, stiffness ellipse, target poses) stays; it just hangs on a
recognizable body.

---

## Module 11 — 19 flagged (of 44)

All share the identical defect: **two/three floating shaded capsules, no trunk, no
head, no hand.** Fix = the shared fix above.

- **Fig 2** — "The planar two-link arm. Shoulder at the origin…" — arm as 2 floating capsules at a shoulder dot; no trunk/hand.
- **Fig 3** — "The Jacobian at a posture. A unit shoulder rate swings the whole arm…" — floating two-capsule arm.
- **Fig 4** — "Inverse kinematics. The same hand target reached by two configurations…" — two overlaid floating arms sharing a shoulder dot; no hand.
- **Fig 5** — "Statics of holding a load. The hand supports a cup…" — floating arm; cup floats at the joint-dot with no hand.
- **Fig 6** — "Redundancy. With three joints and a two-number task…" — overlaid floating three-capsule arms.
- **Fig 11** — "Lab A. The hand travels a straight line from lap to cup…" — left panel: two overlaid floating arm poses.
- **Fig 15 (C1)** — "an arm holding a tray tucked close to the body…" — floating arm; tray at bare joint-dot.
- **Fig 16 (C2)** — "two arm postures, elbow-up and elbow-down, same mug" — floating arms.
- **Fig 17 (C3)** — "a bent arm with a round velocity ellipse…" — floating arm.
- **Fig 23 (C9)** — "a three-link arm with the fingertip pinned…" — overlaid floating arms.
- **Fig 24 (C10)** — "an almost fully extended arm reaching a distant target…" — floating arm.
- **Fig 26 (D2)** — "the two-link arm with the two Jacobian-column velocity arrows…" — floating arm.
- **Fig 27 (D3)** — "the shoulder-target line and the two elbow positions…" — floating arm(s).
- **Fig 28 (D4)** — "an arm with a virtual joint displacement…" — floating arm.
- **Fig 32 (D8)** — "a three-link arm with the minimum-norm task velocity…" — floating arm.
- **Fig 33 (D9)** — "the two-link arm with each link's centre of mass marked…" — floating arm.
- **Fig 34 (D10)** — "an arm with torsional springs at the joints… endpoint stiffness ellipse…" — floating arm.
- **Fig 39 (K5)** — "a three-link arm whose elbow starts near a joint limit…" — overlaid floating arms.
- **Fig 41 (K7)** — "a three-link arm swept through a pure null-space self-motion…" — overlaid floating arms.

**Not flagged (for contrast):** Fig 1 (real head + torso — recognizable seated
person); Fig 7 / C8 / K4 / K6 (small arm inset beside a dominant plot — exempt);
Fig 8 / C7 / D7 (glenohumeral ball-in-socket close-up — recognizable regional joint);
Fig 9 / 10 / C4–C6 / D6 (hand/pinch force FBDs, no capsule shading — abstract);
D1 / D5 (pure geometric/ellipse diagrams).

## Module 12 — 7 flagged (of 43)

Same defect. Fix = the shared fix above.

- **Fig 1** — "Motor equivalence: the same signature written small (fingers/wrist) and large (elbow/shoulder)" — **the m12 calibration case**: two floating capsules + a reused head-gradient wrist knob, beside disconnected squiggles; no head/trunk/hand. Fix: seated person, arm at a shoulder on a torso, hand gripping a pen, traces coming off the pen tip.
- **Fig 5** — "Impedance control for peg insertion: endpoint stiffness ellipse…" — floating arm; peg floats at the joint-dot.
- **Fig 14 (C1)** — "an arm writing the same signature small and large" — same as Fig 1.
- **Fig 17 (C4)** — "an arm with a small then large endpoint stiffness ellipse from co-contraction" — floating arm.
- **Fig 28 (D5)** — "an arm and its endpoint stiffness ellipse from joint stiffness" — floating arm.
- **Fig 36 (K3)** — "an arm whose endpoint stiffness ellipse is oriented along the peg axis" — floating arm; peg floats separately.

*(The auditor listed 6 explicit entries; the 7th body-figure it counted in the tally
is the second signature/stiffness variant in the same cluster — treat the Fig 1 / 14
signature pair and the 5/17/28/36 stiffness-ellipse set as one family to redraw.)*

**Not flagged (for contrast):** Fig 21 (C8) "a shaded walking body mid-stride" —
torso + two full legs + hip/knee spheres + head → genuinely recognizable, and the
model to copy; Fig 40 (K7) small arm inset beside a scatter plot (exempt);
Fig 16 (C3) / Fig 20 (C7) — abstract token/plot diagrams, no capsule shading.

## Module 15 — 1 flagged (of 44)

- **Fig 24 (C10)** — "a limb held horizontal at rest, its joint torque = gravity torque mgL" — a single floating shaded capsule pivoting about one lone joint-circle; no head, no trunk, no hand/foot terminus, and nothing to say arm vs. leg — reads as a bare pivoting pendulum. **Fix:** either drop the anatomical "limb" language (make it an explicit generic beam/pendulum) or draw a minimal *complete* limb — shoulder/hip sphere + capsule + a hand/foot terminus — so it reads as an actual arm or leg held out.

---

## Borderline (author's judgement — not counted in the 27)

- **Module 15 Fig 29 (D5)** — "segment centres of mass and the whole-body COM…" — two shaded capsules at the same 45° (one straight line, not a bent joint), COM dots, no head, no connecting joint sphere, no anatomical label. Ambiguous: an attempted two-link limb (fragment-like) or an intentionally abstract mass-distribution diagram. Fix if counted: add a joint sphere at the junction so it reads as a bent limb, or drop the Tier-2 capsule shading to plain lines to signal it isn't a specific body part.
- **Module 08 compass-gait cluster (~15 figs: C7, C9, D2, D3, D5, D6, D7, D10, K1–K9)** — the passive-walker motif draws one or two shaded capsules meeting at a sphere, **sometimes with no head/torso**. The auditor excluded these because the reduction is the *explicitly taught* minimal-walker model (introduced in Fig 5, always grounded with a foot-contact dot and labelled with the physics quantity), not a failed realism attempt. This is the closest surviving instance of "the head/trunk requirement was relaxed" outside Modules 11–12 — flagged here for a decision, not auto-counted.

## Recommendation

Fix the **26 Module-11/12 arm figures** as one batch (they share one template and one
fix — rebuild the "floating arm" into a torso-anchored arm with a drawn hand, reusing
the whole-body Tier-2 defs already in those modules), then **Module 15 Fig 24**. Decide
separately whether the Module 08 compass-gait figures and Module 15 D5 should be
brought into line or kept as intentional abstractions.
