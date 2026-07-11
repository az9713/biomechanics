# Plan: Module 6 — Tendons, Ligaments, Fascia, and Elastic Energy Storage

## Context
Continuation of the quantitative human-musculoskeletal course in
`C:\Users\<user>\Downloads\human_movement_science_me`. Modules 1–5 are COMPLETE
and live. Module 6 develops the **passive connective tissues** — the collagenous
springs and constraints that Modules 3 and 5 idealised away. It is the course's
tissue-mechanics counterpart to Module 5's active muscle: where Module 5 built the
contractile actuator, Module 6 builds the elastic elements it pulls against.

**Scope sources** (read these first; this plan is derived from them):
1. `prompt.txt` → "### Module 6" (cover-list + required includes).
2. **Forward-references that bind us** (promises already made to the reader):
   - **Module 5 §7** — "Modelling assumption 7.1 (rigid tendon)" defers the
     **series-elastic element** (elastic energy storage & return, the fibre↔tendon
     speed difference, and the implicit CE–SE force balance solved each timestep) to
     Module 6. Reinforced by the §10 repayment table and the §10 roadmap figure
     (Fig. 33), which draws an arrow **Module 5 → Module 6 "series-elastic tendon."**
   - **Module 3 §5** (`module03.html:1131`) — capsule and ligaments at end-of-range
     are "nonlinear springs we model in **Module 6**."
   - **Module 3 §8** (`:1595`) — "Ligaments and tendons as rigid constraints … repaid
     in **Module 6**": replace each hard constraint with a nonlinear spring so the
     **elastic energy a stretched tendon stores and returns** (efficient running)
     reappears.
   - **Module 3 §8** (`:1601`) — the fixed-axis / ideal-hinge idealisation is also
     flagged "repaid in Module 6": ligament **laxity** off the nominal path AND the
     **rolling-gliding / instantaneous-axis / knee screw-home** kinematics. **User
     decision: repay this in full in §8** — a subsection deriving how ligament
     geometry (the crossed cruciate four-bar) drives the migrating instantaneous
     centre and the screw-home rotation, not just the laxity part.
   - **Module 3 §9** (`:2106`) — Module 3 "feeds Module 6 (ligaments and tendons as
     compliant springs)."
   - **Module 1** syllabus row 6 — "Where does jumping energy come from?" Nonlinear
     springs, viscoelasticity (Kelvin–Voigt, SLS), hysteresis; tendon recoil; energy
     return; running economy. (Descriptive, no extra debt.)

Format/scope locked (no need to re-ask): one self-contained `module06.html` via the
`rigorous-explainer` skill (leaner way — prose in HTML, Python for figures only);
Tier-2 anatomy + computed plots; full hardening loop after every edit; MIT-PhD
audience; builds on and links back to Modules 1/3/5, forward to Modules 9
(running/jumping SLIP), 14 (fatigue / creep-to-rupture / ageing), 16 (continuum/FE
tissue). **30-problem §10** (C1–C10 / D1–D10 / K1–K10) + 5 diagnostics, matching
M3/M4/M5 — this is the locked default, not a hedge.

## Deliverable
`C:\Users\<user>\Downloads\human_movement_science_me\module06.html`

## Spine (each section uses the previous)
- **§0 Motivation.** Running is bouncing. A runner's leg is a pogo stick: the
  Achilles and the foot arch stretch on landing and recoil on push-off, returning
  most of the energy for free. Muscle alone (Module 5) cannot explain running
  economy or the kangaroo's near-flat metabolic cost at speed — the missing element
  is a passive **spring** in series with the motor. Hook: where *does* jumping energy
  come from (Module 1's question for this module)?
- **§1 Collagen: the material and its crimp.** Structure of tendon / ligament /
  fascia — collagen fibrils in a hierarchical rope, wavy **crimp** at rest. Define
  stress $\sigma$, strain $\varepsilon$, modulus. The rest-crimp straightening under
  load is **fibre recruitment**, and it produces the **J-shaped** stress–strain curve
  with its compliant **toe region** then a stiff linear region. Sets up the nonlinear
  spring. (Tissue composition contrast: tendon ≈ aligned, stiff; ligament ≈ less
  aligned; fascia ≈ planar sheet — same collagen, different architecture.)
- **§2 Tendon as a nonlinear spring.** From material curve (§1) to **structural**
  force–elongation $F(x)$ via cross-section and length. Define **stiffness**
  $k=\mathrm dF/\mathrm dx$ (slope, rises through the toe to a constant), **compliance**
  $1/k$. Hookean idealisation $F=kx$ vs the nonlinear toe model. This is where Module 3's
  "capsule/ligaments are nonlinear springs" and "replace the rigid constraint with a
  spring" promises are first discharged.
- **§3 Elastic energy storage and return.** Energy $E=\int F\,\mathrm dx$; the linear
  case $E=\tfrac12 kx^2$ (boxed) and the toe-region integral. **Resilience** = fraction
  returned. Worked Achilles numbers (~35 J stored per running step, ~90–93% returned),
  the catapult efficiency, why a tendon is a near-ideal spring. Payoff of §2.
- **§4 The series-elastic element — coupling tendon to muscle (repays Module 5).**
  The **muscle–tendon unit** (MTU): contractile element CE (Module 5's Hill model) in
  **series** with the elastic tendon SE (§2). Kinematic constraint
  $\ell_{\text{MTU}}=\ell_{CE}\cos\theta_p+\ell_{SE}$; force equality
  $F_{CE}(\ell_{CE},v_{CE})=F_{SE}(\ell_{SE})$. Because the tendon can carry a large
  force at small length change, the fibre and tendon move at **different speeds**: the
  fibre shortens slowly (at a favourable point on the force–velocity curve) while the
  tendon recoils fast — **power amplification** the rigid-tendon model *cannot*
  produce. The technical crux: the equality is an **implicit** equation solved each
  timestep (a 1-D root find / DAE) — spell out the algorithm; contrast with M5's
  rigid-tendon shortcut that made the ODE explicit. Discharges all three parts of the
  M5 debt.
- **§5 Viscoelasticity — tendons are not perfect springs.** The phenomena the elastic
  model misses: **creep** (strain grows under held stress), **stress relaxation**
  (stress decays under held strain), **rate-dependent stiffness**, and **hysteresis**
  (loading ≠ unloading path). Introduce the two ideal elements — Hookean **spring**
  and Newtonian **dashpot** $\sigma=\eta\dot\varepsilon$ — as the vocabulary for §6.
- **§6 Lumped viscoelastic models (mathematical core).** Build and solve the
  constitutive ODEs of the three canonical models from spring+dashpot combinations:
  **Maxwell** (series — relaxes fully, but unbounded creep), **Kelvin–Voigt** (parallel
  — bounded creep, but no instantaneous elasticity and no relaxation), **Standard
  Linear Solid** (SLS — captures both; box its ODE
  $\dot\sigma+\tfrac{\sigma}{\tau_\sigma}=E_R(\dot\varepsilon+\tfrac{\varepsilon}{\tau_\varepsilon})$).
  A table of what each captures/misses. SLS is the model the labs use.
- **§7 Hysteresis loops and energy dissipation.** Cyclic loading of the SLS (§6) traces
  a **loop**; its enclosed **area = energy dissipated per cycle**. Define resilience /
  loss fraction; show the rate dependence (faster cycling → different loop). Why tendon
  is a good spring (low hysteresis ~5–10%) while ligament and fascia dissipate more —
  and why that matters (damping, shock absorption vs. energy return). Needs §3 (energy)
  and §6 (ODE).
- **§8 Ligaments as passive constraints; fascia as force transmission; the foot arch.**
  Ligaments as **one-sided** (slack→taut) nonlinear springs that limit joint range —
  repaying Module 3's rigid-constraint idealisation. Then a **rolling-gliding /
  instantaneous-axis** subsection (repays Module 3 §8 in full): the knee's crossed
  cruciate ligaments form a **four-bar linkage** whose instant centre migrates as the
  joint flexes, producing rolling-then-gliding contact and the terminal **screw-home**
  rotation — the ligament geometry, not a fixed hinge, sets the path. Fascia as
  force-transmission tissue (myofascial load paths,
  planar sheets). The **plantar fascia** + the foot **arch** as a tension truss; the
  **windlass mechanism** (toe dorsiflexion tightens the fascia, raising the arch).
  Arch mechanics as elastic energy storage during stance.
- **§9 Computational labs.** Three simulations, per prompt.txt, at MIT-PhD depth:
  1. **Tendon recoil** — release a stretched nonlinear/SLS spring on a small mass;
     integrate the ODE; show the recoil and (SLS) the hysteretic energy loss.
  2. **Running/jumping elastic energy storage** — a mass on a muscle–tendon spring
     (SLIP-like catapult / stretch-shortening cycle). **Demonstrate computationally the
     fibre↔tendon speed decoupling and power amplification** (discharge M5 debt (b) with
     a *result*, not an assertion) and the stride energy budget (elastic vs. active
     fraction). (prompt.txt: "running/jumping elastic energy storage.")
  3. **Ligament constraint under joint motion** — a one-sided spring that engages as a
     joint rotates past neutral; the restoring torque vs. angle, and how laxity shifts
     the engagement. (prompt.txt: "ligament constraint under joint motion.")
- **§10 Captures / misses + 30-problem set + diagnostics.** Captures/misses with a
  repayment table forward to **Module 9** (running/jumping SLIP dynamics), **Module 14**
  (creep-to-rupture, fatigue, ageing/adaptation), and **Module 16** (finite-strain
  continuum / poroelastic collagen). Then **10 conceptual (C1–C10) + 10 derivational (D1–D10) + 10
  computational (K1–K10)** problems + **5 diagnostics**, each with its own figure and a
  collapsible solution; K solutions Python-verified. **MIT-PhD K-standard stated in the
  section itself:** every K problem must require simulation / optimization / an inverse
  problem / a sensitivity sweep / a regime comparison — never plug-in substitution into a
  boxed formula (the standard retrofitted into M5; named here up front).
- **Appendix** — grouped **notation table** (every §0–§10 symbol, linked to its section)
  + grouped **parameter table** (collagen modulus, tendon stiffness & cross-section,
  toe-region strain, resilience/hysteresis %, Achilles stored energy, plantar-fascia
  stiffness, SLS time constants $\tau_\sigma,\tau_\varepsilon$, dashpot $\eta$), each
  value derivation/problem-cited. Links back to Modules 1/3/5, forward to 9/14/16.

## Mathematical spine introduced here
Nonlinear (J-shaped) elasticity & fibre recruitment · structural spring stiffness /
compliance · elastic strain energy $\int F\,dx$ · series (CE–SE) coupling as an
implicit force-balance / DAE solved per timestep · spring–dashpot viscoelasticity ·
the Maxwell / Kelvin–Voigt / Standard-Linear-Solid constitutive ODEs · creep, stress
relaxation, rate-dependent hysteresis loops & dissipated energy · one-sided
(unilateral) constraint springs · the windlass / tension-truss arch. (Finite-strain
continuum and poroelastic collagen deferred to Module 16; creep-to-rupture to 14.)

## Figures (Tier-2 anatomy + computed plots; follow the CLAUDE.md figure rule)
Rebuild the reusable generator + shared `<defs>` block (per CLAUDE.md "Figure style");
**get ONE representative figure approved before mass-producing.** Compute all plot data
with Python (background runs); Tier-2 shaded for anatomy, flat schematic for
physics/plots; slim labelled arrows only; SVG-text subscripts via
`<tspan baseline-shift='sub'>` (Unicode subscripts have no c/d/l/v…).
- §0 Tier-2 runner mid-stride as a pogo stick (leg = spring), Achilles/arch highlighted.
- §1 Tier-2 collagen hierarchy (crimped fibrils → fascicle → tendon) **+ computed**
  J-shaped $\sigma$–$\varepsilon$ curve with the toe/linear regions and the recruitment
  cartoon.
- §2 **computed** $F(x)$ and its slope $k(x)$; Hookean vs nonlinear overlay.
- §3 **computed** energy-under-the-curve shading; a resilience bar (stored vs returned).
- §4 Tier-2 MTU schematic (CE spring-box + pennation + tendon SE) **+ computed** fibre
  vs tendon length/velocity traces showing the speed decoupling.
- §5 spring & dashpot primitives; **computed** creep and stress-relaxation step responses.
- §6 the three model schematics (Maxwell/KV/SLS) side by side **+ computed** each one's
  relaxation & creep signature (a small-multiples grid).
- §7 **computed** hysteresis loops at two rates with the enclosed-area (dissipation)
  shaded; a tendon-vs-ligament resilience comparison.
- §8 Tier-2 foot arch + plantar fascia with the windlass (toe dorsiflexion) **+ computed**
  one-sided restoring-torque-vs-angle curve; **+** a knee crossed-cruciate **four-bar**
  schematic with the **computed** migrating instant centre (screw-home) traced over flexion.
- §9 the three lab result plots (recoil trace; stride energy budget + speed decoupling;
  ligament engagement torque).
- §10 hub/roadmap figure (repayment arrows to Modules 9/14/16) + a figure per problem.

## Build steps
1. Draft the plan (this file) → **user approval gate** (HANDOFF: "get it approved").
2. Compute all figure/plot data in the scratchpad (background numpy): J-curve, $k(x)$,
   energy integral, SLS creep/relaxation/hysteresis, MTU root-find traces, windlass
   torque, the three labs. Emit SVG polyline coords + key numbers to JSON.
3. Rebuild the Tier-2 toolkit (shared defs + generators) from the CLAUDE.md pattern;
   **approve one representative figure first.**
4. Build **section by section**, leaner way (prose authored directly in `module06.html`,
   Python for figures spliced via `<!--FIG:key-->` markers). Define every symbol/term at
   first use; box the headline results ($E=\tfrac12kx^2$, the SLS ODE, the MTU balance).
   Report each section with a short summary + 2 `★ Insight` bullets; **commit only on the
   user's "commit push."**
5. **Harden after every edit** — `checktex / checklt / check_links / check_svg /
   verify_dom / check_overlap` all to 0; `check_frame`/`check_prose` advisories cleared;
   then `autolink_sections.py` once sections exist (re-Read before the next Edit; rm the
   `.bak`). Never eyeball a plot for overlaps.
6. **Publish-while-incomplete:** on the first commit, wire `module06.html` into
   `index.html` (with *(in progress)*) and add its live URL to `README.md`; shift the
   pending "Modules 7–17" line.

## Verification
- All checkers pass: 0 tex, 0 raw `<`/`>`, 0 broken links, 0 mjx-merror, 0 overlaps.
- Cross-links to `module03.html#…`, `module05.html#hillmodel` etc. resolve; every Module
  3 / Module 5 forward-ref above is answered in the named section.
- Spot-check numbers (Python-verified): tendon strain at rupture ~8–10%, toe ends
  ~2–4%; Achilles stored energy ~30–40 J/step running, resilience ~0.90–0.93; tendon
  hysteresis ~5–10%; SLS relaxation/creep time constants order 1–10³ s; the §9 catapult
  must return the energy the §3 numbers predict (integral-conserving check).
- The §4 MTU root-find must reproduce Module 5's rigid-tendon limit as tendon stiffness
  $k\to\infty$ (known-limit validation).

## Workflow reminders (from CLAUDE.md — do not re-derive)
Section-by-section; report each with a short summary + 2 `★ Insight` bullets; **commit
only on "commit push."** Figures must be recognizable Tier-2 with clean labelled vector
arrows (never abstract arrows-on-a-line); SVG-text labels use Unicode subscripts /
`<tspan baseline-shift='sub'>`, not `$…$`. Prose in HTML, never in a Python raw string.

## Status
DRAFT — awaiting user approval. This file = the Module 6 plan. On approval, begin at §0
(after computing figure data and approving one representative figure). Modules 7–17 follow
the same pattern (draw each plan from `prompt.txt` + the prior module's forward-refs).
