# Module 10 — Balance, Stability, Perturbation Recovery, and Sensorimotor Control (build plan)

**Status:** draft plan for review. No `module10.html` content has been authored yet.

**Source basis.** Drawn from `prompt.txt` Module 10 (the Cover/Include lists), the
Module 7 IOUs (its §6 "why we sway" delay teaser, its XcoM/capturability result, its
ankle/hip PD control), the Module 8 older-adult-falls stack and utilized-COF slip
mechanics, the Module 9 closing IOU (perturbed running/landing that a fixed-gait SLIP
cannot show), and the current `rigorous-explainer` figure/hardening rules.

**One-line thesis.** Balance is not a geometry problem (is the COM over the foot?) but
an **active feedback-control problem solved under delay and noise**: the body estimates
its own state from a bank of noisy, latent sensors, feeds that estimate through gains
that must stay inside a delay-bounded stability island, and — when a perturbation drives
the extrapolated COM past the foot — abandons fixed-support control for a change of
support (a step). Aging is read not as "age" but as the drift of four control
parameters — reflex delay, torque capacity, torque rate, and sensor noise — that
shrinks that island and the recovery envelope.

## Boundary with Module 7 (what NOT to re-derive)

Module 7 already built, and is referenced (not repeated), here:

- the sagittal inverted-pendulum EOM and its **saddle** linearization (M7 §3–§4);
- the **extrapolated centre of mass** `ξ = x_com + ẋ_com/ω₀` and the **capturability**
  condition `ξ ∈ BoS` (M7 §4, Prop. 4.2);
- the scalar **ankle PD law** `τ = Kp θ + Kd θ̇` and the **hip strategy** (M7 §5, §7);
- the first qualitative statement that **delay makes us sway** (M7 §6).

Module 10 opens exactly where M7 §6 stopped. The delay stops being a caveat and becomes
the protagonist; the scalar law becomes a **state-space** law; and the perfectly known
state becomes an **estimate** built from real sensors. Every recap cites the M7 anchor
and moves on within a paragraph.

## Building Spine

| Section | Title | Uses | Headline / boxed result |
|---|---|---|---|
| 0 | **Why balance is active control, not geometry** | M7, M8, M9 | Motivate balance as feedback under delay + noise. The static "COM over base" picture (M7 §1) is necessary but not sufficient; a body with momentum, latent sensors, and a shove needs a controller, an estimator, and — past a limit — a step. |
| 1 | **Static balance, dynamic balance, and the margin of stability** | M7 §1, §4 | Recap the static margin and XcoM (M7), then define the **dynamic margin of stability** `b = d_BoS − ξ` as a *recovery budget*: the impulse/lean a fixed-support controller can still arrest. Box the dynamic-stability condition and the margin as its slack. |
| 2 | **The state-space inverted pendulum** | M7 §3–§5 | Upgrade the scalar law to `ẋ = A x + B u`, `x = [θ, θ̇]ᵀ`. Controllability of (A,B), state feedback `u = −K x`, and the **LQR** intuition (why the optimal gains balance effort against deviation). Box the closed-loop `A − BK` and its eigenvalue placement. |
| 3 | **The sensors: vestibular, proprioceptive, and visual channels** | M7, Module 5 muscle | Anatomically correct, glossed: vestibular (semicircular canals → head angular velocity; otoliths → linear acceleration + tilt), **muscle spindles** (Ia/II → length + velocity), **Golgi tendon organs** (Ib → tendon force), joint/cutaneous proprioception, vision (optic flow). Cast each as a noisy, latent **measurement model** `y = C x + ν` with a channel latency. Introduce **reflex loops** (monosynaptic stretch reflex) and **sensory reweighting**. |
| 4 | **Delayed feedback and the instability it breeds** | §2, §3, M7 §6 | Formalize M7 §6. The closed loop is a **delay-differential equation** `θ̈ = ω₀²θ − (Kp θ(t−τ) + Kd θ̇(t−τ))/(mℓ²)`. Derive the characteristic equation, the **critical delay** at fixed gains, and the **stability island** in the (gain, delay) plane. Box the critical-delay / gain-margin result; show why raising gain under delay trades decay rate for oscillation. |
| 5 | **Stochastic perturbations and sensor noise** | §2, §4 | Quiet standing as a **noise-driven bounded process**: under stabilizing feedback the COM/COP behave like an Ornstein–Uhlenbeck-type wander. Signal-dependent motor noise and sensor-noise variance. Derive the stationary sway variance from gain and noise intensity, and connect to posturographic statistics (sway path length, 95% ellipse area). Box the variance–gain relation. |
| 6 | **State estimation: the Kalman-filter intuition** | §2, §3, §5 | The controller cannot feed back the true state — only noisy, delayed measurements. Fuse an internal-model **prediction** with the **measurement** by a gain that weights each by its uncertainty. Derive the scalar Kalman gain `K = σ_pred²/(σ_pred² + σ_meas²)` and the steady-state estimator, then the **delay predictor** (Smith-predictor / state-prediction) that pushes the estimate forward by τ to recover the island lost in §4. Box the fused-estimate update and the predictor. |
| 7 | **Perturbation recovery: fixed vs change of support** | §1, §2, M7 §7 | The recovery ladder: **ankle → hip → step**. While `ξ ∈ BoS`, fixed-support (ankle/hip) suffices; once the perturbation drives `ξ` past the foot edge, a **step is mandatory** (capturability, M7). Derive **foot placement** for a capture step (`x_foot ≈ ξ + margin`) and the reactive-stepping threshold. Box the step-vs-no-step criterion and the capture-step placement. |
| 8 | **Slips and trips: two distinct failure modes** | §7, M8 utilized COF | Mechanically separate them. **Slip:** the base accelerates out from under the COM (foot forward, `μ_required > μ_available`) → backward fall; recovery = friction arrest + rapid step. **Trip:** the swing foot is arrested, COM pitches forward → **elevating vs lowering** strategy set by swing phase. Box the slip condition (utilized vs available COF) and the trip angular-momentum budget; tie foot clearance and required COF back to M8. |
| 9 | **Aging as parameter drift, not "age"** | §2, §4, §7, M8 §10 | Read decline through four named control parameters: reflex delay `τ↑`, peak ankle torque `τ_max↓`, torque rate `↓`, sensor-noise variance `σ²↑`. Each **shrinks the stability island** (§4), **widens the sway** (§5), and **narrows the recovery envelope** (§7). Falls risk = the intersection of a shrinking island with an unchanged (or larger) perturbation distribution. Repays M8's falls stack with the control-theoretic mechanism; keeps the biology/chemistry layers as forward refs to Module 14. |
| 10 | **Computational labs** | §2, §4, §5, §6, §9 | Four labs: (A) **balance recovery after a push** — state-space plant + delayed feedback, simulate the shove and the recovery trajectory, find the largest arrestable impulse; (B) **stability-island mapping** — sweep (gain, delay), classify stable/oscillatory/unstable, overlay the analytic boundary; (C) **Kalman estimator** — fuse noisy delayed sensors, compare filtered estimate + predictor against raw feedback in the loop; (D) **aging sweep** — vary `τ, τ_max, rate, σ` and map recovery-success / critical-impulse surfaces. |
| 11 | **Problem set, diagnostics, limitations, repayment table** | all | 30 problems (C1–C10, D1–D10, K1–K10) + 5 diagnostics; what the model captures/misses (linearization, sagittal-only, single-segment); IOU ledger to Modules 12, 13, 14, 15. |
| A | **Appendix** | all | Grouped notation table and parameter table, each symbol/value linked back to first use. |

## Decisions Locked For This Module

1. **State space is the mathematical spine.** M7 was scalar; from §2 on everything —
   feedback, the DDE, estimation, LQR — lives in `x = [θ, θ̇]ᵀ`. This is the promised
   "state-space inverted pendulum."
2. **Sensors are measurement models, not anatomy for its own sake.** Each channel is
   introduced with correct, glossed anatomy (Pillar 1) but earns its place as a
   `y = Cx + ν` with a latency and a noise variance. The control-theoretic role — what
   it measures, how noisy, how late — is the point.
3. **Delay is the protagonist.** The headline derivation is the delayed-feedback
   stability boundary (§4). It must be *derived* (characteristic equation → critical
   delay / island), not asserted, and it must visibly formalize M7 §6.
4. **Kalman is taught as intuition + scalar derivation + delay predictor**, not full
   matrix-Riccati machinery. MIT-PhD audience can take the scalar gain and the
   predictor and see why estimation buys back the stability the delay cost.
5. **Fixed-support and change-of-support are different control regimes.** The step is
   not "a bigger ankle response" — it is a discrete change of the base of support,
   governed by capturability. Foot placement is derived, not hand-waved.
6. **Slip ≠ trip.** Two distinct mechanisms (base-out-from-under vs swing-foot-arrest),
   two distinct recoveries. Do not blur them into "a perturbation."
7. **Aging = named parameters, never "age."** `τ, τ_max, rate, σ` drift; the figures and
   problems label those variables and their effect on the island and the envelope. The
   biology/chemistry of *why* they drift is forwarded to Module 14.
8. **K problems must be scientific** (MIT-PhD standard): simulation, optimization,
   inverse estimation, sensitivity sweep, or regime comparison — never plug-in
   arithmetic. E.g. map the island (opt/sim), recover a disturbance impulse from a sway
   trace (inverse), sweep aging parameters for the critical impulse (sensitivity).

## Forward References This Module Must Satisfy

- **Module 7:** the "why we sway" delay problem (§6) formalized; XcoM/capturability reused;
  ankle/hip strategies extended to a recovery ladder.
- **Module 8:** older-adult falls given a control-theoretic mechanism; utilized-vs-available
  COF reused for the slip condition; foot clearance for trips.
- **Module 9:** reactive balance in running/landing (perturbed step, unexpected surface) that
  a fixed-gait SLIP cannot represent.
- **Module 5:** muscle length/velocity/force as what spindles and GTOs actually transduce.

## New Forward References This Module Will Create

- **Module 12:** optimal control and whole-body coordination of recovery; redundancy in
  multi-joint stepping; the full LQR/optimal-feedback treatment.
- **Module 13:** task- and terrain-specific perturbations (cutting, turning, uneven ground,
  sport-specific reactive balance).
- **Module 14:** the biology and chemistry *behind* the parameter drift — sarcopenia, neural
  conduction slowing, vestibular hair-cell and receptor loss, medication effects.
- **Module 15:** measuring balance — force plates and COP, motion capture of sway, EMG reflex
  latencies, and the estimation/uncertainty pipeline that this module assumes.

## Figure Families

Get one representative figure approved before mass-producing a family.

1. **Perturbed standing (Tier-2 whole body).** Recognizable standing body taking a horizontal
   shove: the push impulse (slim arrow), the COM, the extrapolated COM leaving the base of
   support, and the recovery step. The teaching contrast: `ξ` inside BoS (no step) vs past the
   edge (step mandatory).
2. **State-space phase portrait.** `(θ, θ̇)` plane: the open-loop **saddle** (M7) vs the
   closed-loop **stable spiral** under `u = −Kx`, with a computed recovery trajectory from a
   post-push initial condition.
3. **Sensor map.** Recognizable head + leg with the vestibular apparatus (inner ear), a muscle
   spindle (in the muscle belly), a Golgi tendon organ (at the tendon), the eye/optic-flow, each
   labeled with its **latency** and a small noisy signal trace. Anatomy correct, never
   AI-freehand.
4. **Delayed-feedback stability island.** Computed boundary in the (gain, delay) plane (or
   (Kp, Kd) at fixed τ), with three sample trajectories — decaying (inside), marginal
   (on boundary), growing oscillation (outside) — anchored to their points.
5. **Stochastic sway / stabilogram.** Computed COM–COP wander, the 95% sway ellipse, and the
   OU stationary envelope; the variance shrinking as gain rises (to a point).
6. **Kalman fusion.** Three computed traces — true state, noisy delayed measurement, filtered
   estimate — plus the predictor pushing the estimate forward by τ to close the delay gap.
7. **Recovery ladder.** Ankle → hip → step as a function of where `ξ` sits relative to the foot
   edge; capture-step foot-placement geometry (`x_foot ≈ ξ + margin`).
8. **Slip vs trip diptych.** Slip (stance foot shoots forward, backward fall, `μ_req > μ_avail`)
   beside trip (swing foot blocked, forward pitch, elevating vs lowering), each with the
   governing inequality labeled on the body.
9. **Aging island shrink.** The stability island (fig. 4) contracting as `τ↑, τ_max↓, rate↓,
   σ↑`, beside a recovery-success (or critical-impulse) curve vs perturbation magnitude for a
   young and an aged parameter set. Labels name the variables, never "age."

All figure labels must pass the semantic audit: a reader knows what every shape represents
before solving the problem. No bare line-and-arrow riddles, no unlabeled pivots, no duplicated
D/K diagrams unless the underlying problem is truly the same. SVG `<text>` uses Unicode
subscripts, not `$…$`.

## Problem-Set Plan

Each problem includes a Tier-2 or computed figure, a short **Probes:** note, and a collapsible
solution; K solutions use Python-verified numbers with copy-buttoned code.

- **Conceptual C1–C10:** static vs dynamic margin; why delay forces sway; what each sensor
  measures and its failure mode (eyes closed, foam, galvanic/vestibular loss, aging); why a step
  is a different regime, not a bigger ankle response; slip vs trip distinction; sensory
  reweighting; why high gain is not simply better.
- **Derivational D1–D10:** dynamic margin from XcoM; state-space `A, B` and controllability;
  closed-loop eigenvalues under `u = −Kx`; the DDE characteristic equation and critical delay;
  stationary sway variance from gain and noise; scalar Kalman gain; the predictor; capture-step
  placement; slip COF condition; trip angular-momentum budget.
- **Computational K1–K10:** simulate recovery after a push and find the largest arrestable
  impulse (sim); map the (gain, delay) stability island and compare to the analytic boundary
  (sim/opt); tune gains for fastest decay inside the island (opt); reconstruct a disturbance
  impulse from an observed sway trace (**inverse**); Kalman estimator vs raw noisy feedback in
  the loop (regime comparison); sway-variance vs gain sweep with an optimum (sensitivity);
  critical delay vs pendulum length/gain sweep (sensitivity); capture-step success vs foot-
  placement error (sim); aging parameter sweep → critical-impulse surface (sensitivity); slip
  recovery vs available COF and reaction delay (regime comparison).

Each K problem must be tested against the depth standard: *does solving it surface science the
reader could not read off the boxed result?* Deepen or cut any that reduce to substitution.

## Build Order

1. Create and approve this plan.
2. Draft `module10.html` skeleton from the existing module template: style, MathJax, TOC, copy
   buttons, and empty section anchors.
3. Build Section 0 only, with one representative figure. Run the full hardening loop and report
   a short summary plus two `★ Insight` bullets.
4. Dispatch `rigor-reviewer` (registered agent, read-only) once the section's scripts hit 0;
   fix findings in bounded rounds before user review.
5. Continue section-by-section after review; commit/push only on "commit push."
6. On the first approved commit/push, wire `module10.html` into both `index.html` (as
   *(in progress)*) and `README.md` (live URL), shifting the pending range from "Modules 10–17"
   to "Modules 11–17."

## Verification Gates

After every edit pass — all to 0:

```powershell
$S='C:/Users/<user>/.claude/skills/rigorous-explainer/scripts'
python $S/checktex.py    module10.html
python $S/checklt.py     module10.html
python $S/check_links.py module10.html
python $S/check_svg.py   module10.html
python $S/verify_dom.py  module10.html
python $S/check_overlap.py module10.html
python $S/check_frame.py module10.html
python $S/check_prose.py module10.html
python $S/check_proofs.py module10.html
python $S/check_code.py  module10.html
python $S/check_probfig.py module10.html
```

Then `autolink_sections.py` to convert `<span class="secref">§N</span>` forward-refs to links,
and `rm` the `.bak` it leaves. Treat `check_overlap.py` as the mechanical gate for label/curve
collisions; the semantic audit is still required by eye. Dispatch `rigor-reviewer` after the
scripts pass, before user review.
