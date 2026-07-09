# Module 9 - Running and Jumping (build plan)

**Status:** draft plan for review. No `module09.html` content has been authored yet.

**Source basis.** This plan is drawn from `prompt.txt` Module 9 ("Cover / Include"
lists), the Module 1 syllabus row 9 ("What limits jump height and landing safety?"),
and the forward-references earlier modules explicitly hand to Module 9:
- **Module 6 §2/§3/§10:** the tendon as a 1-D lumped spring is promoted to *the leg as
  a spring-mass hopper*; the Achilles energy-return / running-economy IOU is repaid here.
- **Module 8 §2/§4:** walking gives way to running near `Fr ~ 1/2`; the pendular model
  hands off spring-mass dynamics, flight, and tendon recoil to Module 9.
- **Module 7 §8/limits:** large-angle and spring-mass dynamics, and dynamic tissue
  loading under impact, are forwarded to Module 9.
- **Module 2:** static/quasi-static bone loads give way to the dynamic impact wave and
  strain-rate effects (Module 9 impact).
- **Module 3 §3:** the dynamic terms that push peak hip JRF to ~3-5 W in running.

**One-line thesis.** Running is bouncing: the leg is a spring and the body a mass, so
each stance stores and returns elastic energy while flight is free-fall - and both the
height you can jump and the safety of a landing are set by *impulse-momentum acting over
a distance or time*, so a force spread over a longer stop is a smaller, safer force.

## Building Spine

Each section needs the one before it; off-spine rigor goes to the Appendix.

| Section | Title | Uses | Headline / boxed result |
|---|---|---|---|
| 0 | **Why running is bouncing** | Modules 6, 8 | Motivate running as a spring-mass bounce, not a fast walk: no double support, an aerial phase, elastic energy banked and returned each step. Central question: what sets jump height and landing safety? |
| 1 | **Running-gait notation and events** | Module 8 gait cycle | Define stance, flight (aerial) phase, contact time, flight time, step/stride, cadence, and **duty factor** `beta = t_c/(t_c+t_f)`. Contrast with walking: running replaces double support with flight, so `beta < 1/2`. Box the timing identities. |
| 2 | **The spring-loaded inverted pendulum (SLIP)** | Section 1, Module 6 spring | Point mass on a massless linear leg spring. Define leg stiffness `k_leg`, rest length `L_0`, angle of attack `alpha_0`. Box the **stance ODE** (radial spring + gravity in polar form) and the **flight ballistic law**; state the conserved energy. |
| 3 | **Stance dynamics and the ground reaction force** | Section 2 | Integrate the SLIP stance phase. Derive the GRF profile, the single-hump vs **double-hump** condition, the peak vertical force, and its scaling with speed and `k_leg`. Validate peak GRF against measured ~2-3 body weights in running. |
| 4 | **Flight phase and the walk-to-run transition** | Sections 2-3 | Ballistic COM trajectory, flight time, apex height. Derive why gait switches from pendular to bouncing near `Fr ~ 1/2` / `beta = 1/2` (repays Module 8 §2/§4). |
| 5 | **Impulse and momentum** | Section 3 GRF | Box the **impulse-momentum theorem** `J = integral F dt = Delta p`. Get takeoff velocity from the net stance impulse (GRF minus gravity); separate braking and propulsive impulse. |
| 6 | **Jump height from takeoff velocity** | Section 5 | Box `h = v_0^2/(2g)`. Vertical jump as impulse over a push-off distance; **countermovement (CMJ) vs squat (SJ) jump** and why the countermovement adds height (bridge to Section 7). |
| 7 | **Stretch-shortening cycle and tendon recoil** | Sections 2, 5, 6; Module 6 | Repay the Module 6 Achilles IOU: pre-stretch stores elastic energy, active state and reflex potentiation add to it, and the tendon returns it at push-off. Box the **running-economy split** (muscle supplies only the losses); resilience per bounce. |
| 8 | **Landing mechanics and force absorption** | Section 5 | Box landing force from work-energy `F_avg = (1/2 m v_land^2)/d` and impulse `F_avg = m v_land/Delta t`. Stiff vs soft landing: longer stopping distance/time lowers peak force. Eccentric (negative) muscle work absorbs the energy. |
| 9 | **Impact loading and injury risk** | Section 8; Module 2 | Repay the Module 2 dynamic-impact IOU: the impact transient, **loading rate**, and cumulative dose vs tissue tolerance. Map to stress fractures (bone), ACL rupture (ligament), and tendon overuse; strain-rate stiffening. |
| 10 | **Computational labs** | Sections 2, 3, 6, 7, 8 | Four labs: (a) SLIP stance integration + leg-stiffness/speed sweep of peak GRF and gait pattern; (b) vertical-jump simulation (force-time -> takeoff velocity -> height), CMJ vs SJ; (c) landing-impact simulation, peak force vs stopping distance; (d) tendon contribution to running economy (muscle-vs-tendon energy split, sweep tendon stiffness). |
| 11 | **Problem set, diagnostics, limitations, repayment table** | all | 30 problems C1-C10, D1-D10, K1-K10; 5 diagnostics; what SLIP captures/misses; IOU ledger to Modules 10, 12, 13, 14, 15. |
| A | **Appendix** | all | Grouped notation table and parameter table, each linked back to first use. |

## Decisions Locked For This Module

1. **Running is not a fast walk.** It is a distinct spring-mass, aerial regime: no
   double support, flight replaces it, and energy is stored elastically rather than
   exchanged pendularly. The module opens by contrasting the two regimes, not by
   appending speed to Module 8.
2. **The leg spring is the organizing idealization, honestly labelled.** SLIP promotes
   Module 6's 1-D lumped tendon spring to a *whole-leg* effective spring. `k_leg` is an
   **effective limb stiffness** (tendon + muscle + geometry + posture), not the Achilles
   stiffness alone - state this so the reader does not conflate them.
3. **Landing safety is impulse-momentum over a distance/time, not a single "impact
   force" number.** The central safety lesson is that the *same* momentum change spread
   over a longer stop is a smaller peak force. Every landing result is framed this way.
4. **The stretch-shortening cycle is mechanical, not magic.** The CMJ advantage is
   explained by elastic storage + active-state build-up + reflex potentiation, each
   named - never as free energy. Quantify the elastic share.
5. **Injury risk is loading rate and cumulative dose vs tissue tolerance**, repaying
   Module 2's dynamic-impact IOU - not "impact = bad." Distinguish a single overload
   (ACL) from accumulated dose (stress fracture, tendinopathy).
6. **Computational problems must be scientific.** K problems require simulation,
   optimization, inverse estimation, sensitivity sweeps, or regime comparisons. No
   plug-in-the-number arithmetic. (K-depth will be checked with the rigor-reviewer,
   including a deliberate plug-in injection to confirm the reviewer flags it.)

## Forward References This Module Must Satisfy

- **Module 6:** the leg as a spring-mass hopper; Achilles elastic storage and return;
  running economy; resilience by loop integration.
- **Module 8:** walk-to-run transition near `Fr ~ 1/2`; spring-mass replaces pendular.
- **Module 7:** large-angle and spring-mass dynamics; dynamic tissue loading under impact.
- **Module 2:** dynamic impact wave and strain-rate effects on bone.
- **Module 3:** dynamic terms raising peak hip JRF to ~3-5 W in running.
- **Module 1:** SLIP, impulse-momentum, jump height, landing impact, sport/injury risk.

## New Forward References This Module Will Create

- **Module 10:** perturbed running and landing, cutting/side-steps, unexpected surfaces,
  reactive balance during flight and touchdown.
- **Module 12:** whole-body coordination and optimal control of jumping and sprinting;
  redundancy in multi-joint push-off.
- **Module 13:** uphill/downhill running, sprint acceleration, and sport-specific tasks.
- **Module 14:** tendinopathy, stress fractures, ACL injury, and aging of elastic tissue.
- **Module 15:** force-plate GRF and loading-rate measurement, IMU contact-time
  estimation, and the impact-quantification pipeline.

## Figure Families

Get one representative figure approved before mass-producing a family. Problem-set
(C/D/K) figures always lead with the recognizable Tier-2 entity, then hang the
FBD/vectors/plot on it.

1. **Tier-2 running gait sequence.** Recognizable running body through stance
   compression, toe-off, flight, and landing, with the leg-spring overlay and the
   stance/flight labels unambiguous.
2. **SLIP schematic.** Point mass on a massless spring leg: rest length `L_0`, angle of
   attack `alpha_0`, compression, and the stance/flight phase split - drawn on a
   recognizable body silhouette, not a bare line.
3. **Computed GRF profiles.** Single-hump vs double-hump vertical GRF from SLIP
   integration, peak force and contact time labelled by data, over stance percent.
4. **Flight trajectory + walk-run transition.** Ballistic COM arc with apex; a computed
   `Fr` / duty-factor plot marking the pendular-to-bouncing switch.
5. **Impulse-momentum diagram.** Force-time curve with the area (= impulse) shaded,
   braking vs propulsive split, and before/after COM velocity vectors on the body.
6. **Vertical jump.** CMJ vs SJ force-time and COM-height traces, push-off distance, and
   takeoff velocity mapped to jump height.
7. **SSC / tendon recoil.** Leg-spring energy loop, muscle-vs-tendon energy split, and a
   running-economy comparison bar - integral-conserving (energy in = returned + lost).
8. **Landing force vs stopping distance.** Recognizable landing body, stiff vs soft
   landing, computed `F`-vs-`d` curve, and shaded eccentric absorption work.
9. **Impact loading / injury.** Loading-rate transient, tissue-tolerance-vs-dose panel,
   and stress-fracture / ACL / tendon sites anchored to a recognizable limb - labels
   name the actual variables (loading rate, peak force, contact time, tissue tolerance,
   cumulative dose), not "age" or "impact."

All figure labels must pass the semantic audit: a reader should know what every shape
represents before solving the problem. No bare line-and-arrow riddles, no unlabelled
pivots or angles, no duplicate D/K diagrams unless the problem is truly the same.

## Problem-Set Plan

Each problem includes a Tier-2 or computed figure, a short **Probes:** note, and a
collapsible solution; K solutions use Python-verified numbers with a copy button.

- **Conceptual C1-C10:** running-vs-walking regime, duty factor and flight, SLIP
  assumptions, why longer stopping distance is safer, CMJ-vs-SJ intuition, tendon energy
  return, loading rate vs peak force, single-overload vs cumulative-dose injury, and
  SLIP's limitations.
- **Derivational D1-D10:** timing identities, SLIP stance/flight equations, peak-GRF and
  double-hump conditions, walk-run transition inequality, impulse-momentum takeoff
  velocity, `h = v_0^2/(2g)`, CMJ energy accounting, landing force from work-energy and
  from impulse, and loading-rate expressions.
- **Computational K1-K10:** SLIP stance integration, leg-stiffness/speed sweep of peak
  GRF and gait pattern, vertical-jump simulation and CMJ-vs-SJ comparison, jump-height
  optimization over push-off strategy, landing-impact sim with stopping-distance
  sensitivity, tendon-vs-muscle energy split and stiffness sweep, running-economy regime
  comparison, and an injury-dose sensitivity analysis. Every K must require
  simulation / optimization / inverse / sweep / regime comparison - no plug-in.

## Build Order

1. Create and approve **this plan**.
2. Draft `module09.html` skeleton from the module template: style, MathJax, TOC, copy
   buttons, empty section anchors.
3. Build **Section 0 only**, with one representative Tier-2/physics-hybrid figure. Run
   the full hardening loop; **dispatch `rigor-reviewer`** for an independent pass once
   the scripts hit 0; fix findings (bounded rounds); then report a short summary plus
   two `Insight` bullets for user review.
4. Continue section-by-section after review. **Commit/push only on the user's "commit
   push."**
5. On the first approved commit, wire `module09.html` into **both** `index.html` (mark
   *(in progress)*, shift the pending line to "Modules 10-17") and `README.md` (live URL).
6. **Reviewer carry-forwards:** run `rigor-reviewer` as the *registered* agent (fresh
   session loads `.claude/agents/rigor-reviewer.md` and enforces read-only tools); and
   before trusting it on the K set, inject one deliberately plug-in K problem into a
   scratch copy and confirm it flags `K-DEPTH: fail`.

## Verification Gates

After every edit pass (all to 0 / advisory clean):

```powershell
$S='C:/Users/simon/.claude/skills/rigorous-explainer/scripts'
python $S/checktex.py module09.html
python $S/checklt.py module09.html
python $S/check_links.py module09.html
python $S/check_svg.py module09.html
python $S/verify_dom.py module09.html
python $S/check_overlap.py module09.html
python $S/check_frame.py module09.html
python $S/check_prose.py module09.html
python $S/check_proofs.py module09.html
python $S/check_code.py module09.html
python $S/check_probfig.py module09.html
python $S/autolink_sections.py module09.html
```

Treat `check_overlap.py` as the mechanical gate for label/curve collisions; the
three-layer semantic figure audit and the read-aloud prose audit are still required by
eye. `rigor-reviewer` runs after the scripts pass, before user review.
