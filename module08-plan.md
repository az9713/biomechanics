# Module 8 - Walking Biomechanics (build plan)

**Status:** draft plan for review. No `module08.html` content has been authored yet.

**Source basis.** This plan is drawn from `prompt.txt` Module 8, the Module 1
syllabus row for walking biomechanics, the Module 7 closing IOU to walking, and
the current `rigorous-explainer` figure rules.

**One-line thesis.** Walking is controlled falling: the body vaults over the stance
leg like an inverted pendulum, loses energy when the velocity is redirected from
one step to the next, and uses timed push-off, joint work, and coordination to
make that loss small enough that walking is metabolically cheap but not free.

## Building Spine

| Section | Title | Uses | Headline / boxed result |
|---|---|---|---|
| 0 | **Why walking is cheap, but not free** | Module 7 | Motivate walking as a sequence of inverted-pendulum vaults plus step-to-step redirection. The central question is not "what muscles fire?" but "where does mechanical work get saved, lost, and repaid?" |
| 1 | **Gait-cycle notation and events** | Module 1 kinematics | Define stride, step, cadence, stride length, walking speed, stance, swing, heel strike, loading response, midstance, terminal stance, toe-off, double support, and single support. Box the bookkeeping identities, including speed from step length and cadence. |
| 2 | **The inverted-pendulum COM arc** | Module 7 inverted pendulum | Treat stance as vaulting over a nearly rigid leg. Derive COM height, speed exchange, kinetic/potential energy exchange, and the Froude number `Fr = v^2/(g ell)`. |
| 3 | **Ground reaction force and COP trajectory in walking** | Module 7 COP/GRF | Upgrade the standing COP from a balance-control point to a moving heel-to-toe pressure trajectory. Relate GRF to COM acceleration and show why the force vector moves under the foot during stance. |
| 4 | **Compass gait model** | Sections 1-3 | Build the two-rigid-leg sagittal model: stance leg as pivot, swing leg as second pendulum, heel-strike relabeling, and the impact map. This is the minimal model that can walk. |
| 5 | **Step-to-step transition cost** | Section 4 | Derive the mechanical cost of redirecting COM velocity from one inverted-pendulum arc to the next. Show why pre-emptive push-off before heel strike can reduce collision loss. |
| 6 | **Joint torques and joint powers** | Modules 1, 3, 5, 7 | Define inverse dynamics for ankle, knee, and hip in the sagittal plane. Box `P_j = tau_j dot(theta_j)` and separate negative work, positive work, ankle push-off, knee shock absorption, and hip work. |
| 7 | **Speed, cadence, stride length, and cost** | Sections 1-6 | Explain why preferred walking speed is an optimization problem, not a fixed constant. Build a metabolic-cost proxy from transition work, joint work, and cadence/step-length tradeoffs. |
| 8 | **Arm swing and whole-body angular momentum** | Sections 6-7 | Show arm swing as a passive/low-cost angular-momentum management strategy, not decoration. Connect to trunk rotation and reduced muscular work. |
| 9 | **Passive dynamic walking and stability** | Sections 4-8 | Explain the downhill passive-dynamic walker: gravity supplies the losses, the gait is a limit cycle, and stability depends on the basin of attraction. On level ground, muscles must repay the lost energy. |
| 10 | **When walking fails: older-adult falls and post-fall decline** | Sections 1-9 | Use the physics-chemistry-biology stack: margin of stability, trip/impact mechanics, bone mineral/collagen chemistry, inflammation, sarcopenia, sensory loss, slower reflexes, fear/deconditioning, and why a fall often starts a health-decline cascade rather than ending as a single mechanical event. |
| 11 | **Computational labs** | Sections 2, 5, 6, 7, 9, 10 | Four labs: COM arc/Froude sweep; step-to-step transition and push-off timing sweep; inverse-dynamics estimate of ankle/knee/hip torque and power from synthetic gait kinematics plus GRF; fall-margin sensitivity sweep for older-adult gait. |
| 12 | **Problem set, diagnostics, limitations, repayment table** | all | 30 problems: C1-C10, D1-D10, K1-K10; 5 diagnostics; what the model captures/misses; IOU ledger to Modules 9, 10, 12, 13, 14, and 15. |
| A | **Appendix** | all | Grouped notation table and parameter table, each linked back to first use. |

## Decisions Locked For This Module

1. **Walking is not standing with translation appended.** Module 7's inverted
   pendulum becomes a moving, step-reset pendulum. The COP is no longer only the
   controller's handle inside a fixed base; it travels from heel toward toe while
   the stance foot redirects the COM.
2. **Walking is not running.** This module uses pendular energy exchange and
   compass-gait collisions. It should point forward to Module 9 for spring-mass
   running, flight phase, tendon recoil, and SLIP dynamics.
3. **Passive dynamic walking must be honest.** On a slope, gravity supplies the
   lost energy. On level ground, positive muscle work must supply it. The course
   should not imply passive dynamics is a free lunch.
4. **Inverse dynamics is introduced as an estimate, not magic.** The ankle, knee,
   and hip torques are inferred from kinematics, segment parameters, and external
   forces; measurement uncertainty is forwarded to Module 15.
5. **Computational problems must be scientific.** K problems must require
   simulation, optimization, inverse estimation, sensitivity sweeps, or regime
   comparisons. No plug-in arithmetic problems.
6. **Falls are a stack, not a slogan.** The older-adult falls discussion must
   explicitly separate physics (stability margins, foot clearance, reaction
   time, impact energy), chemistry/materials (bone mineral density, collagen,
   vitamin D/calcium, inflammation, medications), and biology (sarcopenia,
   sensory degradation, reflex delay, pain, fear, deconditioning, hospitalization
   complications). The point is to teach why falling is both a mechanical failure
   and a biological turning point.

## Forward References This Module Must Satisfy

- **Module 7:** inverted pendulum in motion; step-to-step transition; COP trajectory.
- **Module 1:** work, energy, power, torque, COM, GRF, and moment arms in an actual locomotor task.
- **Module 5:** muscle work and power during push-off; energetic cost as a proxy for activation.
- **Module 6:** elastic storage is mentioned only as a bridge to running; walking remains pendular.

## New Forward References This Module Will Create

- **Module 9:** running and jumping as spring-mass / SLIP dynamics, flight, impact loading, tendon recoil.
- **Module 10:** perturbations during gait, slips, trips, recovery steps, sensorimotor noise.
- **Module 12:** full whole-body coordination, optimal control, and redundancy resolution.
- **Module 13:** uphill/downhill walking, stair climbing, turning while walking, and task-specific cases.
- **Module 14:** sarcopenia, osteoporosis, frailty, inflammation, and post-fall decline.
- **Module 15:** motion capture, filtering, force plates, uncertainty, and the full inverse-dynamics pipeline.

## Figure Families

Get one representative figure approved before mass-producing a family.

1. **Tier-2 gait-cycle sequence.** Whole-body recognizable poses for heel strike,
   loading response, midstance, terminal stance, toe-off, and swing. Labels must
   make stance/swing, double/single support, and limb identity unambiguous.
2. **Computed COM arc and energy exchange.** Inverted-pendulum path with computed
   COM height, speed, kinetic energy, and potential energy curves.
3. **Foot COP/GRF trajectory.** Recognizable foot, heel-to-toe COP path, GRF
   vector, COM acceleration, and time labels across stance.
4. **Compass gait schematic.** Two-leg model with stance pivot, swing leg, hip
   mass, angles, collision/relabeling, and slope/level-ground variants.
5. **Step-to-step transition diagram.** Velocity vectors before and after
   redirection, push-off impulse, collision impulse, and loss/work annotations.
6. **Joint torque and power plots.** Ankle, knee, hip torques and powers over gait
   percent, with positive and negative work shaded and labels placed by data.
7. **Cost landscape.** Speed/cadence/stride-length sweep with a clear optimum,
   not a decorative curve.
8. **Passive dynamic walker.** Toy walker plus phase portrait or small SMIL loop,
   driven by computed or explicitly stated model quantities.
9. **Older-adult fall stack figure.** A recognizable walking older body, trip or
   slip perturbation, shrinking margin of stability, impact path to hip/wrist,
   and a linked stack panel for physics, chemistry/materials, and biology. The
   figure must avoid implying "age" itself is the mechanism; it should label the
   actual variables: foot clearance, COM velocity, reaction delay, hip strength,
   bone mineral/collagen integrity, inflammation, pain, and deconditioning.

All figure labels must pass the semantic audit: a reader should know what every
shape represents before solving the problem. No bare line-and-arrow riddles, no
unlabeled pivots, no duplicate D/K diagrams unless the underlying problem is truly
the same.

## Problem-Set Plan

Each problem will include a Tier-2 or computed figure, a short **Probes:** note,
and a collapsible solution. C/D/K diagrams should be task-specific:

- **Conceptual C1-C10:** gait-event definitions, pendular exchange, COP/GRF
  interpretation, double support, passive dynamic walking, arm swing, and model
  limitations, including why older-adult falls are multi-causal.
- **Derivational D1-D10:** speed/cadence bookkeeping, COM arc geometry, Froude
  scaling, GRF-COM relation, compass-gait equations, impact map, transition work,
  joint power, cost-optimum conditions, and simple fall-margin inequalities.
- **Computational K1-K10:** COM arc simulation, Froude sweep, transition-cost
  optimization, push-off timing, inverse-dynamics torque estimates, power/work
  integration, cadence/stride optimization, arm-swing angular-momentum comparison,
  passive-walker stability sweep, and older-adult fall-margin sensitivity.

## Build Order

1. Create and approve this plan.
2. Draft `module08.html` skeleton from the existing module template: style,
   MathJax, TOC, copy buttons, and empty section anchors.
3. Build Section 0 only, with one representative Tier-2/physics hybrid figure.
   Run the hardening loop and report a short summary plus two `Insight` bullets.
4. Continue section-by-section after review.
5. On the first approved commit/push for Module 8, wire `module08.html` into
   both `index.html` and `README.md` as live and in progress, shifting the pending
   module range from 8-17 to 9-17.

## Verification Gates

After every edit pass:

```powershell
$S='C:/Users/<user>/.claude/skills/rigorous-explainer/scripts'
python $S/checktex.py module08.html
python $S/checklt.py module08.html
python $S/check_links.py module08.html
python $S/check_svg.py module08.html
python $S/verify_dom.py module08.html
python $S/check_overlap.py module08.html
python $S/check_frame.py module08.html
python $S/check_prose.py module08.html
python $S/check_proofs.py module08.html
```

Browser-based checks may need escalation because headless Chrome writes profile
and cache files outside the sandbox. Treat `check_overlap.py` as the mechanical
gate for label/curve collisions; the semantic audit is still required by eye.
