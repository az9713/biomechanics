# Plan: Module 5 — Muscles as Chemo-Electro-Mechanical Actuators

## Context
Continuation of the quantitative human-musculoskeletal course in
`C:\Users\simon\Downloads\human_movement_science_me`. Modules 1–4 are COMPLETE
and live. Module 5 supplies the **active force generator** that every prior
module either invented as an abstraction or left blank: Module 1's "net muscle
moment," Module 3's "applied force $Q$" on the constrained joint. It is the
first *chemo-electro-mechanical* module — a signal becomes a force.

**Scope sources** (read these first; this plan is derived from them):
1. `prompt.txt` → "### Module 5" (cover-list + required includes) + the mandatory
   per-module lab/diagnostic requirements the earlier modules followed.
2. **Binding forward-references we must repay** (promises to the reader):
   - **Module 1 §9 captures/misses table** (three explicit IOUs):
     (a) *"Single net muscle moment" → antagonist co-contraction; many muscles
     share the load* (Modules 5, 12); (b) *"Constant muscle moment arm $d_m$" →
     $d_m$ varies with joint angle* (Module 5); (c) *"Muscle force unlimited" →
     force–length–velocity limits, fatigue* (Modules 5, 14).
   - **Module 3 §8** ("ideal or absent muscle"): *"repaid in Modules 5 and 7 …
     a Hill-type muscle with force–length–velocity behaviour, activation dynamics,
     and pennation, plus an optimization to choose among more muscles than there
     are degrees of freedom."* → obligates §7 (Hill model) + §8 (redundancy
     optimization).
   - **Module 3 C10** (muscle redundancy): motion alone under-determines muscle
     forces → co-contraction matters. Repaid by §8's optimization.
   - **Module 1 syllabus row** (the module's own charter): "How does a nerve
     signal become joint torque? — Hill model, activation ODE, force–length–
     velocity; crossbridge cycling, Ca²⁺ dynamics, motor-unit recruitment;
     activation → torque; fatigue; lifting/push-off."
3. **Inputs we reuse** (don't re-derive): Module 1's $\tau=F_m\,d_m$ and the
   third-class-lever mechanical disadvantage ($F_m\approx12\times$ load); Module 3's
   joint reaction / KKT redundancy framing; Module 1 Appendix anthropometry.

Format/scope locked (no need to re-ask): one self-contained `module05.html` via
the `rigorous-explainer` skill; Tier-2 anatomy + computed plots (compute data with
Python first); full hardening loop; builds on and links back to Modules 1 & 3,
forward to Module 6 (tendon series-elastic / energy storage), Module 7 (neural
control / reflexes / co-contraction in posture), Modules 12 & 14 (fatigue, aging).

## Deliverable
`C:\Users\simon\Downloads\human_movement_science_me\module05.html`

## Spine (each section uses the previous)
- **§0 Motivation.** Everyday hook: you decide to lift a bag, and ~100 ms later
  the biceps pulls. Module 1 told us the elbow needs torque $\tau=F_m d_m$ and
  that $F_m$ can be $\sim12\times$ the load; Module 3 left the muscle force $Q$
  **blank**. How does a chemical/electrical nerve signal become a *graded,
  controllable* force — and why can't you produce max force instantly, why does
  it depend on length and speed, why does it fatigue? Sets up the pipeline
  **neural drive → activation → contractile force → joint torque.**
- **§1 Muscle architecture — the force-producing hierarchy.** Whole muscle →
  fascicles → fibers → myofibrils → **sarcomeres** (the contractile unit). Define
  **pennation angle** $\theta_p$, **physiological cross-sectional area** (PCSA),
  **specific tension** $\sigma\!\approx\!0.3\ \mathrm{MPa}$ → maximal isometric
  force $F_{\max}=\sigma\cdot\mathrm{PCSA}$, and the along-tendon projection
  $F_{\text{tendon}}=F_{\text{fiber}}\cos\theta_p$. The anatomical substrate every
  later force term scales. *(Tier-2 anatomy.)*
- **§2 The sarcomere: crossbridges → the length–tension law (boxed).** Sliding-
  filament model; actin–myosin **crossbridge cycle** (attach → power-stroke →
  detach) with one **ATP** hydrolysed per cycle; active force $\propto$ number of
  attached crossbridges $\propto$ thick/thin **filament overlap**. Derive the
  piecewise **active length–tension** curve $f_L(\ell)$ (ascending limb, plateau,
  descending limb) from overlap geometry — the first mechanical law, boxed.
- **§3 Excitation–contraction coupling: action potential → calcium.**
  **Neuromuscular junction**, motor end-plate **action potential**, $\mathrm{Ca^{2+}}$
  release from the sarcoplasmic reticulum, **troponin/tropomyosin** unblocking the
  binding sites. The $\mathrm{Ca^{2+}}$ transient sets the *fraction of available
  crossbridges* — this is the physical meaning of **activation** $a\in[0,1]$. A
  single-twitch $\mathrm{Ca^{2+}}$/force response introduced here.
- **§4 Motor units, recruitment, and rate coding.** Motor unit = one motoneuron +
  its fibers. **Henneman size principle** (recruitment order small→large),
  **rate coding**, twitch **summation → unfused → fused tetanus**. Whole-muscle
  neural drive $u(t)\in[0,1]$ = recruitment × firing rate. Maps the CNS command
  onto the lumped excitation $u$ that §5 turns into $a$. *(SMIL: twitch summation
  to tetanus.)*
- **§5 Activation dynamics (ODE, boxed).** Collapse §3–§4 into a first-order
  activation ODE $\dot a=(u-a)/\tau_a(u,a)$ with **asymmetric activation vs
  deactivation** time constants ($\tau_{\text{act}}\!\sim\!10$ ms,
  $\tau_{\text{deact}}\!\sim\!40$ ms) — why force lags and outlasts the command.
  This is the required "activation dynamics ODE." *(Computed $a(t)$ response to a
  step / burst of $u$.)*
- **§6 Force–velocity relation (Hill's hyperbola, boxed).** Concentric shortening
  drops force; eccentric lengthening raises it above isometric. **Hill's 1938**
  equation $(F+a_H)(v+b_H)=(F_0+a_H)b_H$ as a hyperbola $f_V(v)$; mechanical
  **power** $P=Fv$ with its optimum at $\sim\!1/3\,v_{\max}$. The second mechanical
  law; tie the shortening-rate limit back to the crossbridge cycling rate of §2.
- **§7 The Hill-type muscle model (MAIN SYNTHESIS, boxed).** Assemble everything:
  contractile element $F_{CE}=a(t)\,F_{\max}\,f_L(\ell)\,f_V(v)$, a **parallel
  elastic** element $F_{PE}(\ell)$ (passive), and pennation:
  $F_{\text{tendon}}=\big(F_{CE}+F_{PE}\big)\cos\theta_p$. **Tendon assumption
  (state explicitly):** treat the tendon as *rigid* here — muscle-tendon-unit
  length = fiber length, so $\ell$ and $v$ come straight from joint kinematics and
  the labs integrate a clean ODE. Name the **series-elastic** element as the next
  refinement and defer the compliant-SE equilibrium (implicit CE–SE solve each
  step, tendon energy storage) to **Module 6**. The module's headline equation,
  boxed — it consumes §1 ($F_{\max}$, $\theta_p$), §2 ($f_L$), §5 ($a$), §6 ($f_V$).
  *(Schematic block diagram + computed $f_L\cdot f_V$ slices.)*
- **§8 From muscle force to joint torque: variable moment arm, agonist–antagonist.**
  $\tau=F_{\text{muscle}}\,d_m(\theta)$ with the moment arm **now a function of
  angle** — repays Module 1's "constant $d_m$" IOU. **Agonist–antagonist** pairs,
  **co-contraction**, net torque $\tau=\tau_{\text{ago}}-\tau_{\text{anti}}$;
  **mechanical advantage**. **Muscle redundancy introduced lightly here** (more
  muscles than DOFs → motion under-determines forces; state the static
  optimization $\min\sum(F_i/F_{i,\max})^2$ s.t. the torque constraint and solve
  the small biceps/brachialis case) — the **heavy version** (whole-limb, CNS
  control, cost-function debate) is a **Module 7** repayment, per M3 §8's "Modules
  5 *and* 7." Worked **biceps-curl** static model, validated against Module 1's
  isometric result. *(Tier-2 elbow with $d_m(\theta)$; agonist–antagonist figure.)*
- **§9 Computational labs** (each with the mandatory 10-part lab checklist from
  `prompt.txt`: physical question · biological question · assumptions · equations ·
  parameter table · Python code · plotted output · interpretation · sensitivity ·
  failure modes · extension challenge).
  - **Lab 1 — activation → joint torque.** Integrate the §5 activation ODE + §7
    Hill model + §8 moment arm through a movement; primary **biceps curl**, with
    **quadriceps–knee** and **calf–Achilles–ankle** as variants (comparison table).
    (prompt.txt: "Python simulation of joint torque from muscle activation.")
  - **Lab 2 — fatigue-sensitive force.** Add a fatigue/recovery state variable that
    lowers effective $F_{\max}$ under sustained activation; plot force decay and
    recovery. (prompt.txt: "Python simulation of fatigue-sensitive force output";
    repays Module 1's "muscle force unlimited" IOU, forward-ref Module 14.)
- **§10 Captures / misses + diagnostics + problems.** Captures/misses with a
  **repayment table** → Module 6 (tendon series-elastic & elastic energy storage),
  Module 7 (reflexes, spindles, closed-loop control & co-contraction in posture,
  the heavy redundancy problem), Module 12 (multi-muscle whole-limb), Module 14
  (fatigue physiology, aging); plus *how to measure/validate* (EMG, dynamometry,
  ultrasound fascicle imaging) per pipeline step 22. Then **diagnostics + problems**
  — baseline **5 diagnostics + 3 problems** (1 conceptual / 1 derivational / 1
  computational) per prompt.txt, *or* the full **30-problem set** (C1–C10 / D1–D10 /
  K1–K10) as built for Modules 3 & 4. **Confirm which with the user before the big
  build.**
- **Appendix** — parameter table ($\sigma$, PCSA & $F_{\max}$ for biceps/quads/
  gastroc, optimal length $\ell_0$, $v_{\max}$, pennation angles, $\tau_{\text{act}}/
  \tau_{\text{deact}}$, Hill $a_H/b_H$, moment arms $d_m(\theta)$) + grouped
  notation table (every §0–§9 symbol linked to its section); links back to
  Modules 1 & 3, forward to 6, 7, 12, 14.

## Mathematical spine introduced here
Filament-overlap geometry → piecewise length–tension $f_L$ · first-order
activation ODE (asymmetric time constants) · Hill force–velocity hyperbola $f_V$ ·
the composite Hill-type force law $F=a\,F_{\max}f_L f_V+F_{PE}$ with pennation ·
$\tau=F\,d_m(\theta)$ · constrained static optimization for muscle redundancy
(KKT reused from Module 3, small case only) · numerical ODE integration (labs) ·
a fatigue state-variable ODE. *(Series-elastic tendon quantified → Module 6;
closed-loop neural control + heavy redundancy → Module 7.)*

**Symbol-collision discipline** (pre-empt, per CLAUDE.md Pillar 1): joint torque
$\tau$ vs activation/deactivation time constants $\tau_{\text{act}},\tau_{\text{deact}}$;
activation $a$ vs Hill constant $a_H$; specific tension $\sigma$ vs any stress
$\sigma$ borrowed from Modules 2/4 — subscript throughout and define at first use.

## Figures (Tier-2 anatomy + computed plots; follow the CLAUDE.md figure rule)
Build a reusable generator + shared `<defs>` (per CLAUDE.md "Figure style"); get
**ONE representative figure approved before mass-producing** — the Tier-2 muscle
hierarchy and the posable-limb figures are the ones to approve first.
- §0 pipeline schematic: nerve → muscle → lifted bag (whole-arm Tier-2 + labelled arrows).
- §1 **muscle hierarchy** (Tier-2): whole muscle → fascicle → fiber → sarcomere
  zoom; separate **pennation-angle** diagram with $F_{\text{fiber}}$/$F_{\text{tendon}}$ arrows.
- §2 **computed** $f_L(\ell)$ curve + sarcomere filament-overlap sketches at 3–4 lengths.
- §3 NMJ + **computed** $\mathrm{Ca^{2+}}$/twitch transient; troponin unblocking schematic.
- §4 size-principle recruitment ladder + **computed** twitch-summation→tetanus (SMIL).
- §5 **computed** $a(t)$ vs $u(t)$ step/burst, showing $\tau_{\text{act}}\neq\tau_{\text{deact}}$.
- §6 **computed** Hill force–velocity hyperbola (concentric+eccentric) + power curve.
- §7 Hill-model **block diagram** (CE ∥ PE, in series with SE, pennation) + computed $f_L\!\cdot\!f_V$ slices.
- §8 Tier-2 elbow with **computed** $d_m(\theta)$; agonist–antagonist pair + net-torque curve.
- §9 **computed** activation→torque time series (three joints) + fatigue decay/recovery curve.

## Build steps
1. Compute all figure/plot data in the scratchpad (background — numpy startup is
   slow): $f_L$ overlap geometry, $\mathrm{Ca^{2+}}$/twitch + tetanus summation,
   activation ODE $a(t)$, Hill $f_V$ + power, $d_m(\theta)$, the redundancy
   optimization, the two labs (activation→torque, fatigue). Emit SVG polyline
   coords / SMIL keyframes + key numbers.
2. Rebuild the Tier-2 figure toolkit (shared defs + posable-limb & muscle
   generators) from the CLAUDE.md pattern; **approve one representative figure first.**
3. Write `module05.html` from the skill template; embed computed coordinates;
   define every symbol/term at first use; **box** the §2 length–tension law, §5
   activation ODE, §6 Hill hyperbola, and the §7 composite Hill model.
4. Harden after every edit: `checktex.py`, `checklt.py` (+`escape_math_lt.py`),
   `check_links.py`, `verify_dom.py`, `check_overlap.py`, `shoot.py` preview.
   Cross-link to module0[134] and run `autolink_sections.py` once sections exist.

## Verification (spot-check numbers)
- $F_{\max}$: biceps $\sim\!500$ N, quadriceps $\sim\!5000$ N (PCSA × $\sigma$)
  give sane orders of magnitude; $\sigma\approx0.2$–$0.35$ MPa.
- $f_L$ plateau at optimal sarcomere length $\ell_0\approx2.7\ \mu\mathrm m$
  (human), force → 0 near $\sim\!1.27\ \mu\mathrm m$ and $\sim\!4.2\ \mu\mathrm m$.
- Hill $v_{\max}\sim\!10\,\ell_0/\mathrm s$; peak power near $v\approx v_{\max}/3$;
  eccentric plateau $\sim\!1.4$–$1.8\,F_0$.
- Activation ODE: $\tau_{\text{act}}\sim\!10$ ms, $\tau_{\text{deact}}\sim\!40$ ms.
- §8 biceps-curl torque + moment arm must reproduce Module 1's static result as
  the $a=1$, $v=0$ isometric special case (a known-limit validation).
- Redundancy optimization returns the physically expected agonist-dominant split
  and non-negative forces.
- All checkers pass: 0 tex, 0 raw `<`/`>`, 0 broken links, 0 mjx-merror, 0 overlaps.

## Workflow reminders (from CLAUDE.md — do not re-derive)
Section-by-section; report each with a short summary + 2 `★ Insight` bullets;
**commit only on the user's "commit push."** Publish-while-incomplete: on first
commit, link `module05.html` from `index.html` (marked *(in progress)*) and add
its live URL to `README.md`. Figures must be recognizable Tier-2 with clean
labelled vector arrows (never abstract arrows-on-a-line); SVG-text labels use
Unicode subscripts, not `$…$`.

## Status
NOT STARTED — plan reviewed and **approved by the user**. Begin at §0 on the
user's go-ahead. **Decisions locked (confirmed with the user):**
1. **Section count = §0–§10 + Appendix** — labs get their own §9, captures/misses +
   problems get §10 (one heading longer than Modules 3 & 4; §9 no longer overloaded).
2. **Full 30-problem set** in §10 — 10 conceptual (C1–C10) + 10 derivational
   (D1–D10) + 10 computational (K1–K10) + 5 diagnostics, each with a figure and a
   collapsible worked solution (K solutions Python-verified), as built for Modules
   3 & 4.
