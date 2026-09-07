# Domain: quantitative human musculoskeletal science

This is the subject of the manuscript. Know it before you edit it. This file is the
domain brief for the `science-editor` skill (`~/.claude/skills/science-editor/`).
`EDITOR_PROMPT.md` in this repo describes a different manuscript; ignore its
`# Domain:` section here.

## What the manuscript is

Seventeen modules plus a landing page, written as self-contained HTML lessons with
MathJax and inline SVG/SMIL figures, no build step. `index.html` is the map and the
syllabus; `module01.html` through `module17.html` are the lessons. Module 17 is the
capstone. `prompt.txt` is the original course specification and the source of truth
for scope and structure: it lists what each module must cover, the required
mathematical spine, the required biological spine, and a 23-step teaching pipeline
per topic (daily-life phenomenon → anatomy → mechanism → cellular substrate →
idealization → coordinates → variables and units → free-body diagram → governing
equations → constitutive law → assumptions → parameter values → nondimensional
groups → worked example → Python simulation → plot → sensitivity → adaptation or
failure → clinical relevance → what the model captures → what it misses → how to
validate → daily-life interpretation).

Every module follows one page shape: `§0` motivation, numbered sections `§1…§N`
with derivations and computed figures, a computational lab with Python code and
sensitivity analysis, a "what the model captures and misses" section, a problem
set, and an Appendix. Section headings are `<h2 id="…">`; in-page references are
`§N` links. Per-module build plans exist for modules 4 to 10 (`moduleNN-plan.md`);
`CLAUDE.md` holds the standing conventions; `HANDOFF.md` is the resume point.

The course exists to answer one question: how does the human skeleton and
musculoskeletal system enable daily physical life, quantitatively and
mechanistically? The body is treated as a controlled, elastic, adaptive, chemically
powered, electrically signaled, multibody, load-bearing, self-repairing
mechanical-biological system under gravity with noisy sensors, nonlinear actuators,
deformable tissues, contact constraints, delayed feedback, and stability limits.
The manuscript is a textbook, not an audit. Its claims are earned by derivation and
by computation in the text, not by citation.

## The objectives or results that must never be blurred

`prompt.txt` bans qualitative substitutes for mechanics. Any of the following, or a
sentence of the same shape, is a blocking defect unless a force, torque, moment arm,
stress, stiffness, energy, power, pressure, delay, gain, or margin follows it:
"the glutes stabilize the hip", "the calves push off", "cartilage cushions the
joint", "bones support the body", "the nervous system coordinates movement".

Pairs the field runs together, each with its own definition and its own test:

- **Joint torque, joint reaction force, and muscle force.** Torque is the moment the
  muscles must supply about the joint axis; the reaction force is the contact load
  the joint surfaces carry; the muscle force is the reaction force's largest
  contributor because of mechanical disadvantage (short moment arm). A passage that
  reports one and names another is wrong.
- **Center of mass and center of pressure.** The first is a property of the body's
  mass distribution; the second is the point of application of the resultant ground
  reaction force. They coincide only in static equilibrium, and quiet standing is not
  static.
- **Stress, strain, stiffness, and strength.** Stress is force per area; strain is
  relative deformation; stiffness is the slope of the stress-strain (or force-
  displacement) curve; strength is the stress at failure. A sentence that says a
  tissue is "strong" when it means stiff is a defect.
- **Static equilibrium, quasi-static, and dynamic.** State which one the model
  assumes and where inertial terms are dropped.
- **Activation, force, and torque in muscle.** Neural drive → activation dynamics →
  force via the Hill relations (length, velocity) → torque via the moment arm. Each
  arrow is a separate model with its own equation.
- **Elastic, viscoelastic, hyperelastic, poroelastic, biphasic.** Each is a named
  constitutive law with its own boxed equation. "Viscoelastic" without a model
  (Kelvin-Voigt, Maxwell, standard linear solid) is not a statement.
- **Feedback and feedforward; delay and gain; stability and robustness.** In the
  control modules (7, 10, 12) every controller is written as an equation with its
  gains and its delay, and every stability claim is a computed margin.
- **The level ladder** (Level 0 scalar estimate → Level 10 multiscale adaptation).
  Each module states which level its models sit on. A Level-1 statics estimate
  presented as a dynamic result is a defect.

## The mathematics the reader meets, and what may not be assumed

The reader has a graduate degree in a quantitative field and has never studied
anatomy or biomechanics. Every anatomical term is glossed at first use, in the
same sentence, in plain words: "femoral head (the ball atop the thigh bone)". This is
the course's Pillar 1 and it is already audited; hold every new passage to it.

Every one of the following must be built in the text before it is used, in the
module that first needs it, with a proof in the smallest setting that shows the
mechanism: the moment of a force and the moment arm; static equilibrium of a
segment; center of mass and center of pressure; ground reaction force; dimensional
analysis and scaling; Euler-Bernoulli beam bending, torsion, second moment of area;
stress and strain tensors; strain energy density; the bone remodeling ODE;
fracture and fatigue criteria; constraint equations and Lagrange multipliers, with
the multiplier identified as the joint reaction; degrees of freedom of a joint;
Hertz contact; Donnan swelling; the biphasic consolidation PDE and fluid load
support; Stribeck lubrication regimes; the Hill muscle model (length-tension,
force-velocity) and the activation ODE; motor-unit recruitment and rate coding;
Kelvin-Voigt, Maxwell, and standard linear solid; hysteresis and energy return;
the inverted pendulum and its linearization; the PD controller and delayed feedback
instability; the compass-gait model, step-to-step transition cost, Froude number;
the spring-loaded inverted pendulum; impulse-momentum and jump height; margin of
stability and extrapolated center of mass; state-space models, sensor noise, and
the Kalman filter; the two-link arm, its Jacobian, and `τ = Jᵀ F`; the friction
cone; minimum-jerk trajectories, the linear quadratic regulator, impedance control,
and model predictive control; finite differences, filtering, and inverse dynamics;
parameter identification and uncertainty; the deformation gradient, hyperelastic
and fiber-reinforced laws, and a finite-element toy.

The five-part standard applied to this manuscript: a boxed result earns its box. If
one result in a section gets a `.prop` with an adjacent `.proof`, its sibling boxed
results of equal weight in the same section get the same treatment. A boxed
`.keyresult` that is a definition or a one-line substitution needs no proof; a boxed
constitutive law or a stability condition does. This gap shipped once (Module 6 §6:
6.1 and 6.2 asserted beside a proved 6.3) and was fixed; check for it everywhere.

Module 1 `§1`–`§4` (`module01.html`, ids `setup`, `moment`, `equil`, `main`) is the
worked model of the standard: definitions with examples, the moment of a force
proved in the planar case, equilibrium of one segment, then the boxed joint-torque
result with its worked number. Hold every other section to that shape.

## The methods, models, or architectures, and where they come from

The models are the ones listed in `prompt.txt` under "Include simulations such as".
Each is derived in its module from Newton-Euler or Lagrangian mechanics plus a
stated constitutive law. None is presented as a diagram to accept.

Primary sources: the modules cite named textbooks in prose (for example, Winter,
*Biomechanics and Motor Control of Human Movement*, for the anthropometric
regression fractions in the Module 1 Appendix). The repo holds no PDFs. Treat every
such citation as **unverified**: do not repair, extend, or add a citation from
memory. Where a number rests on a citation alone, say the citation is unverified
and leave the number; do not replace it with one you recall.

## The evidence-grading scheme

No letter grades. Every number in the manuscript belongs to exactly one of three
classes, and the prose must make the class visible:

- **Derived**: follows from a boxed result and stated inputs. Check the arithmetic.
- **Parameter**: taken from the module's Appendix parameter table or a stated
  parameter table in the section, with its symbol and unit. Check the value against
  the table; a mismatch between text and table is a factual error.
- **Assumed**: a modeling choice stated as such ("take the moment arm as 0.03 m").
  Check that it is labelled as an assumption and that the sensitivity analysis
  covers it.

A number that is none of these (a bare physiological value with no table entry, no
derivation, and no "assume") is a blocking defect. The fix is to add it to the
parameter table with its symbol, or to derive it, or to label it an assumption.
Only empirical numbers are flagged this way; the user's decision (2026-09-07) is
that derivation in the text is the source, so no paper citation is required.

## The running example

There is no single running example. The course threads a reference human and a
set of recurring scenarios; a module that introduces a fresh toy body without need
is a structural defect.

- **Reference human**: 70 kg adult, segment masses and centers of mass as
  regression fractions of total mass `M` and segment length `ℓ` (Module 1
  Appendix: forearm+hand mass `m_s = 0.022 M = 1.54 kg`, forearm+hand COM
  `r_s ≈ 0.43 ℓ_fa = 0.116 m`, grip distance `r_L = 0.35 m`, elbow flexor moment
  arm `d_m = 0.03 m`, `g = 9.81 m s⁻²`, stated inter-individual scatter
  10–15 %).
- **Recurring scenarios**: the cup or bag held in the hand (Module 1, 11, 13); the
  femur under bending and the sideways fall (Modules 2, 14, 17); the knee and hip
  as the hinge and the ball-and-socket (Modules 3, 4); the Achilles tendon as the
  energy store (Modules 6, 9); quiet standing as the inverted pendulum with delayed
  feedback (Modules 7, 10, 17); the two-link arm (Modules 11, 12); sit-to-stand and
  stair climbing (Modules 1, 13, 17).

Check that a scenario reused in a later module uses the same symbols and the same
parameter values as its first appearance, or states why they differ.

## Measured results the prose must match

There are no laboratory measurements. Every computed number comes from the Python
code in the module: the lab section's script and the copy-buttoned code inside each
computational problem's `<details class="sol">`. Those code blocks are the ground
truth. To check a number in a solution or a caption, run the code and compare;
a mismatch is a factual error. Every computed figure's polyline coordinates and
every SMIL keyframe are generated from the same code as the numbers, so a figure
that disagrees with its caption's number is also a factual error.

Findings the manuscript must not soften: quiet standing is unstable without
feedback and the delayed-feedback stability boundary is a computed gain-delay
curve; a joint reaction force exceeds body weight by the mechanical-disadvantage
ratio; interstitial fluid pressurization carries most cartilage load at short
times and decays on the consolidation timescale; running economy depends on tendon
energy return, not muscle work alone.

## Conventions of this manuscript

- **Audience**: MIT-PhD level. Do not water down. Computational (K) problems must
  require numerical integration, optimization, an inverse problem, a sensitivity
  sweep, or a regime comparison. A plug-the-numbers-into-the-box problem is
  busywork at this level and is a defect (Module 5 §10 was retrofitted for this).
- **Problem set**: 5 diagnostics + 30 problems (C1–C10 conceptual, D1–D10
  derivational, K1–K10 computational). Every problem has a figure, a "Probes:" note
  naming the mechanism it tests, and a collapsible solution. K solutions carry
  Python-verified numbers with code.
- **Symbols**: introduced once, one meaning for the whole module; cross-section
  collisions (W, k, g, E were fixed once) are defects. Every module's Appendix holds
  a notation table and a parameter table; every symbol in the text appears there.
- **Forward references**: `<span class="secref">§N</span>` until the section exists;
  then a real link. A forward reference the reader must accept on faith is a defect
  even when the link works.
- **Medium**: HTML with MathJax. Replacement text must be valid HTML with `$…$` /
  `$$…$$` delimiters, no raw `<` or `>` inside math (`\lt \gt \le`), headings only
  `<h2>`/`<h3>`, boxes only the existing classes `.def`, `.prop`, `.thm`, `.lem`,
  `.proof`, `.keyresult`, `.probes`, `.sol`. SVG `<text>` uses Unicode subscripts
  and entities, never `$…$`. No em-dashes in new prose.
- **Figures**: Tier-2 shaded anatomy for real entities, flat schematic for physics
  diagrams and animations; every vector a slim labelled arrow attached to the
  entity. Each figure referenced from the prose and captioned to stand alone.
- **Hardening gates** (run after any applied edit; all must pass):
  `checktex.py checklt.py check_links.py check_svg.py verify_dom.py
  check_overlap.py check_frame.py check_prose.py check_proofs.py check_code.py
  check_probfig.py check_bodyprop.py` in
  `~/.claude/skills/rigorous-explainer/scripts/`. `check_proofs.py` flags a
  `.prop`/`.thm`/`.lem` with no adjacent `.proof`; the sibling-keyresult case is the
  editor's judgement.
- **Known past defect classes** to look for first: asserted sibling results beside a
  proved one; awkward prose that came from Python raw strings ("Summation is
  summation in $a$", "worth watching happen"); shell-mangled math where a sentence
  became one italic run; plug-in K problems; symbol reuse across sections; a
  motivation section that names the phenomenon but not the question the module
  answers; a closing section that does not say what the reader can now do.
- **Tooling**: Python with NumPy, SciPy, SymPy, Matplotlib. Code blocks are PEP8
  (`check_code.py`).
