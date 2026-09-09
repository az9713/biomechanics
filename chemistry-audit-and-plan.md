# Chemistry Audit and Chemistry-Layer Plan

Date: 2026-09-09. Scope: `module01.html` … `module17.html`, against `prompt.txt`.

---

## Part 1 — The audit

### 1.1 The finding in one sentence

**Chemistry is present in this course as nouns, never as equations.** The course
names ATP, `Ca_10(PO_4)_6(OH)_2`, RANKL, OPG, sclerostin, troponin, SERCA,
acetylcholine and proteoglycans. It derives almost none of them. There is exactly
**one** true physical-chemistry derivation in 5.6 MB of course material:
**Module 4 §2**, which builds the electrochemical potential
`mu_i = mu_i^o + R_g T ln c_i + z_i F psi`, applies Donnan equilibrium, and closes
with van 't Hoff osmotic pressure. That section is the template. Everything else
in the chemical spine is narrative.

### 1.2 Keyword census (raw hit counts per module)

Counts over the full HTML of each module. A row of `0` means the concept does not
appear anywhere in the course.

| Concept | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9 | M10 | M11 | M12 | M13 | M14 | M15 | M16 | M17 |
|---|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| Gibbs / free energy | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Enthalpy | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Entropy | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Equilibrium constant | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Rate constant k_on / k_off | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Arrhenius / activation energy | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pH | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pKa | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Nernst | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Debye screening | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bond types (covalent / H-bond / vdW) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Amino acid / peptide | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Metabolism (glycolysis, mitochondria) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Redox / ROS / oxidative stress | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Boltzmann / k_B T | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Entropic elasticity / worm-like chain | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Fick / diffusion coefficient | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Enzyme / catalysis | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Glycation / AGE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Chemical potential | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ATP | 0 | 0 | 0 | 0 | 29 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Donnan | 0 | 0 | 0 | 28 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Proteoglycan / GAG | 0 | 0 | 0 | 40 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| Collagen | 1 | 18 | 2 | 32 | 0 | 64 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 9 | 0 |
| Cross-link | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| Hydroxyapatite | 1 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Myosin / actin | 0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Calcium | 1 | 0 | 0 | 0 | 74 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Read the table as a map: chemistry clusters in **M2, M4, M5, M6** and is absent
from **M7–M17** entirely. Modules 7–17 are pure mechanics and control.

### 1.3 Evidence, module by module

**Module 2 §5 — "Where E comes from: the mineral–collagen composite".**
Gives the hydroxyapatite formula and a Voigt/Reuss bound (`E_R ~ 2.0 GPa` to
`E_V ~ 50 GPa`, measured `17 GPa`). The composite mechanics are derived. The
chemistry is not: no calcium-phosphate solubility product, no nucleation in the
collagen gap zone, no pH dependence, no reason why `E_collagen ~ 1 GPa`. A table
row reads "Water / non-collagenous proteins — Interface, sacrificial bonds" — a
bond mechanism named in three words and never modelled.

**Module 2 §7 — the mechanostat.** Names sclerostin, RANKL, OPG, osteoblast,
osteoclast, osteocyte and mechanotransduction. Then models all of it as one
phenomenological ODE `dZ/dt = k Z (eps - eps_hi)`, explicitly labelled "a stated
constitutive law, not a derived theorem". The signalling chemistry has no equations.

**Module 4 §2 — the one real chemistry section.** Electroneutrality
`c_+ = c_- + c_F`, the Donnan condition `c_+ c_- = c_0^2` derived by cancelling the
Donnan potential out of the electrochemical potential, then van 't Hoff
`pi = R_g T [(c_+ + c_-) - 2 c_0]`. Fully rigorous. This is the standard to match.

**Module 5 §2–§3 — crossbridges and excitation–contraction coupling.** ATP appears
29 times, always as a label on a cycle diagram: "burning exactly one molecule of ATP
per turn". No `Delta G`. No coupling of that free energy to the work of a power
stroke. No efficiency. The action potential, the DHPR/RyR gate, the SERCA pump and
the Ca–troponin switch are described in words; not one Nernst potential, not one
mass-action binding equation, not one Hill coefficient. Activation dynamics (§5)
becomes a first-order ODE with fitted time constants instead of the binding kinetics
that set those constants.

**Module 6 §1 — collagen, crimp, and the J-curve.** 64 mentions of collagen. The
J-shaped law is derived from *geometric* crimp straightening. The molecular origin
of the toe region (entropic, at the `k_B T` scale) is absent; `cross-link` appears
twice and is never chemistry.

**Module 10 §10 leaves an explicit chemistry IOU:** "To Module 14 — the biology and
chemistry behind the four parameter drifts." **Module 14 does not repay it.**
Module 14 scores 0 for glycation, 1 for collagen, 1 for cross-link. Sarcopenia,
osteoporosis and osteoarthritis are modelled as parameters drifting on an
exponential; the chemistry that drives the drift is not there. That is a broken
promise inside the course's own repayment convention.

### 1.4 Against the original spec

`prompt.txt` line 211 defines a **"Required Biological / Chemical Spine"** of 25
items. It also fixes a Mandatory Teaching Pipeline whose **step 4 is "Molecular /
cellular substrate"**, and line 65 says: "whenever chemistry … is required, bring
that knowledge in rigorously."

Spine items delivered **as mathematics**: osmotic swelling pressure (M4 §2). One of
twenty-five.

Spine items delivered **as narrative only**: collagen chemistry, mineralization,
calcium phosphate / hydroxyapatite, mechanotransduction, osteocyte signalling,
osteoblast / osteoclast dynamics, cartilage proteoglycans, synovial fluid chemistry,
ATP metabolism, crossbridge cycling, excitation–contraction coupling, calcium release
and reuptake, ion gradients, action potentials, neuromuscular junction physiology,
fatigue mechanisms.

Spine items **absent entirely**: inflammation, tissue repair, tendon adaptation,
muscle hypertrophy, muscle atrophy, endocrine effects on bone and muscle.

The gap is structural, not accidental. `prompt.txt` line 285 lists the Modeling
Levels the course climbs — **Level 0 is "scalar force, torque, work, power, stress,
strain"**. The ladder has no rung below Level 0. There was never a slot for a mole,
a bond energy, or a rate constant, so nothing built on that ladder could land there.

---

## Part 2 — The plan

### 2.1 Design principle

Add the missing rung: **Level −1, the molecular and chemical substrate.** Every new
section must convert a chemical quantity into a mechanical number the existing course
already uses. If a proposed section cannot name the mechanical parameter it explains,
it does not belong.

Worked example of the standard (numbers verified in Python): at `T = 310.15 K`,
`k_B T = 4.28 zJ` and `R_g T = 2.58 kJ/mol`. In-vivo ATP hydrolysis at
`Delta G ~ -55 kJ/mol` is `91.3 zJ` per molecule, i.e. `21.3 k_B T`. One power
stroke does `(5 pN)(10 nm) = 50 zJ = 11.7 k_B T`. So a crossbridge is about `55%`
efficient, and whole-muscle efficiency near `25%` is that figure minus the activation
overhead — SERCA pumping the calcium back. None of that calculation exists anywhere
in the course today, and it is what explains Module 9's cost of transport.

### 2.2 Shape — decided 2026-09-09

**One new module plus threading.** Chosen by the user over the four-module option:

1. **`module00.html` — Chemical Foundations.** New, built **first**, to the **full
   course standard**: 30 problems, 5 diagnostics, computational labs, Tier-2 figures,
   appendix. It fixes the notation and the three laws everything else cites.
2. **Chemistry and biology threaded into the existing seventeen** as new sections in
   the modules where each topic belongs. No Modules 18–20.

**Scope includes biology** (user's choice): cell signalling, endocrinology and tissue
turnover are in, not only physical chemistry. Deriving the M2 §7 mechanostat needs
RANKL/OPG mass action, so the line could not be held at chemistry alone anyway.

#### The renumbering problem, and the scheme that avoids it

Threading means inserting sections into finished modules. Two facts, both measured:

- **Safe:** section anchors are semantic slugs (`#hillmodel`, `#sarcomere`,
  `#activation`), not numbers. All **59** cross-file links in the repo point at
  slugs, so inserting a section breaks none of them.
- **Dangerous:** displayed section numbers are used heavily in prose —
  **250** `§N` references in M4, **248** in M5, **208** in M6, 75 in M2. A mid-module
  insert that renumbers §6 onward would silently invalidate hundreds of references.
  `check_links.py` would still pass, because the links resolve; they would just point
  at the wrong section. That is the worst class of defect: green gates, wrong book.

**Scheme: letter-suffixed chemistry sections.** A chemistry section attached to §5
is numbered **§5C**, with slug id `chem-<topic>`, placed immediately after §5.
It sits in the right pedagogical position, and **renumbers nothing** — every one of
the existing `§N` references stays correct. `C` reads as "the chemistry of this
section", and the course already uses decimal and lettered section labels
(§3.5, "8.1 What it gets right", "A. Appendix").

### 2.2b Threading map

Chemistry sections to insert, by module. Each is listed as
`§NC — title` → *the existing quantity it derives*.

**Module 2 — bone**
- §5C Chemistry of the mineral–collagen composite → *derives `E_apatite ~ 100 GPa`
  and `E_collagen ~ 1 GPa` from bond stiffness and bond density; calcium-phosphate
  solubility product, supersaturation, nucleation in the collagen gap zone, pH
  dependence, and why bone stops near 50% mineral.*
- §7C The signalling chemistry of the mechanostat → *Wnt/sclerostin and RANKL/OPG as
  a mass-action model, integrated to **derive** the mechanostat curve that §7 states
  as a constitutive law.*

**Module 4 — cartilage**
- §1C Proteoglycan chemistry → *derives the fixed charge density `c_F` that §2 takes
  as given, from GAG sulfation.*
- §7C Synovial fluid chemistry → *hyaluronan and lubricin; the polymer physics behind
  the boundary-lubrication `mu_eq` that §7 assumes.*
- §8C Enzymatic degradation kinetics → *MMPs and aggrecanases as a rate model of the
  osteoarthritis cascade §8 tells as a story.*

**Module 5 — muscle**
- §2C Crossbridge thermodynamics → *`Delta G` of ATP against power-stroke work;
  the ~55% crossbridge and ~25% whole-muscle efficiency; the Fenn effect.*
- §3C Nernst, Goldman–Hodgkin–Katz, and the Na/K pump → *derives the resting and
  action potential §3 narrates, and the metabolic cost of excitability.*
- §5C Cooperative Ca–troponin binding → *derives the activation ODE and its
  asymmetric rise and fall time constants that §5 fits.*
- §6C Arrhenius and `Q_10` → *the temperature dependence of `v_max`; why a cold
  muscle is weaker and warm-up works.*

**Module 6 — tendon and ligament**
- §1C Collagen molecular chemistry and entropic elasticity → *Gly-X-Y, hydroxyproline,
  the hydrogen-bond ladder, the D-period; the `k_B T`-scale entropic origin of the toe
  region that §1 explains by crimp geometry alone.*
- §5C Cross-link chemistry → *lysyl-oxidase enzymatic against non-enzymatic glycation
  cross-links; how cross-link density sets the modulus and the hysteresis loop of §7.*

**Modules 8 and 9 — walking, running**
- §xC Bioenergetics of locomotion → *the phosphocreatine, glycolytic and oxidative ATP
  supply systems as a kinetic model with rate ceilings and capacities; produces the
  cost of transport and the power–duration curve these modules quote empirically.*

**Module 14 — aging**
- §2C Protein turnover and sarcopenia → *synthesis-against-breakdown balance as the
  chemistry behind the strength drift.*
- §3C Endocrine control of bone → *PTH, vitamin D and oestrogen; bone as the body's
  calcium buffer; the chemistry of the osteoporosis drift.*
- §4C Glycation kinetics → *AGE accumulation in glucose and time, predicting the
  tendon stiffening and bone embrittlement §3–§4 assert.* **This repays the IOU
  Module 10 §10 left and Module 14 never paid.**

**Modules 15, 16, 17 — light**
- M15: biochemical markers as measurements (CTX, P1NP, blood lactate) and their error
  model, alongside the mechanical instruments.
- M16: the chemical-potential driving term that generalizes the poroelastic model
  already there.
- M17: one chemistry-anchored capstone project.

Total: **one new module plus roughly seventeen threaded sections across nine
modules.**

### 2.3 Module 0 — Chemical Foundations

Purpose: give the reader the vocabulary and the three laws every later chemistry
section uses. Everything is anchored to a tissue, never to a generic beaker.

- §0 Motivation — why a bond energy sets a bone's stiffness.
- §1 The mole, concentration, and the `k_B T` / `R_g T` bridge. Energy per molecule
  against energy per mole; why `k_B T = 4.28 zJ` at body temperature is the ruler for
  every molecular event in the body.
- §2 Bonding and the stiffness ladder: covalent, ionic, hydrogen, van der Waals,
  hydrophobic. Derive a modulus from a bond stiffness and a bond density, and show it
  recovers `E ~ 100 GPa` for apatite and `E ~ 1 GPa` for collagen — the two numbers
  Module 2 §5 uses without justification.
- §3 Thermodynamics: `Delta G = Delta H - T Delta S`, chemical potential,
  `Delta G = Delta G^o + R_g T ln Q`, equilibrium `Delta G^o = -R_g T ln K`, and
  reaction coupling — how an unfavourable reaction runs on a favourable one.
- §4 Entropic elasticity: the freely jointed and worm-like chain, force as
  `-T dS/dx`, and why rubber and the elastin in a ligament stiffen when heated while
  steel softens. This is the missing molecular origin of Module 6's toe region.
- §5 Water, ions, and the electric double layer: dielectric screening, Debye length,
  pH, pKa, buffering. Sets up Donnan (M4 §2) and the Nernst potential threaded into M5 §3C.
- §6 Kinetics: mass action, `k_on` / `k_off`, `K_d`, cooperative (Hill) binding,
  Arrhenius and `Q_10`, Michaelis–Menten. Why a muscle is weaker when cold.
- §7 The macromolecules: the amino acid, the peptide bond, the Gly-X-Y triple helix,
  the glycosaminoglycan, the phospholipid bilayer.
- §8 Computational lab: solve a binding equilibrium and an Arrhenius temperature
  sweep numerically.
- §9 What the model captures and misses, 5 diagnostics, 30 problems.
- Appendix: notation, physical constants, chemical parameter table.

### 2.7 Build constraints this plan must respect

1. **Symbol namespace, assigned before writing.** `F` is force everywhere but Faraday
   in M4; `mu` is friction in M4 §7 and chemical potential in M4 §2; `k` is the
   remodeling gain in M2 §7 and wants to be a rate constant; `R` is the joint reaction,
   and M4 already renamed the gas constant `R_g`. Fix a chemistry namespace in the
   Module 0 appendix and use it in every threaded section. Threading makes this
   sharper, not softer: a chemistry section now sits inside a module that already
   binds those symbols.
2. **K problems must compute, not substitute.** The course standard forbids plugging
   numbers into a boxed formula. Every computational problem must integrate, optimize,
   invert, or sweep — fit `k_on` / `k_off` from a measured twitch, sweep glucose to
   find the AGE crossover age, solve the ATP supply model for the power–duration curve.
3. **Figures.** Molecular figures (helices, lattices, reaction coordinates, titration
   curves) are the molecular analogue of the "never AI-generate anatomy" rule: draw
   them programmatically as Tier-2 SVG. Approve one representative figure before
   mass-producing thirty.
4. **`checktex` risk.** `\leftrightarrow` is a known false positive. `\rightleftharpoons`
   for chemical equilibria is untested — test one before writing forty.
5. **Publish-while-incomplete.** Module 0 goes live in `index.html` and `README.md`
   on its first commit.
6. **Never renumber an existing section.** Use the `§NC` letter-suffix scheme of
   §2.2. A renumber would silently misdirect up to 250 in-prose references per module
   while every automated gate still passed.
7. **Re-run the full hardening loop on every module a threaded section touches**, plus
   a `rigor-reviewer` pass. Threading reopens modules the editor pass closed at
   `a93a55c`; that is the accepted cost of the chosen shape.

---

## Part 3 — Decisions and build order

Decided with the user on 2026-09-09:

| Question | Decision |
|---|---|
| Shape | Thread into the existing 17, plus one new `module00.html` |
| Scope | Chemistry **and** biology (signalling, endocrine, tissue turnover) |
| Module 0 depth | Full course standard — 30 problems, labs, figures, appendix |
| Build order | Module 0 first |

**Order of work**

1. **Module 0**, section by section under the standing convention: build one section,
   report with a short summary and two `★ Insight` bullets, review, then commit and
   push. Fix the chemistry symbol namespace in its appendix before §1 is written.
   Get one representative molecular figure approved before mass-producing the rest.
2. **Module 5** threaded sections (§2C, §3C, §5C, §6C) — the largest chemistry deficit
   against the largest existing narrative, and the ATP efficiency calculation is the
   course's best single demonstration of the new layer.
3. **Module 2** (§5C, §7C), then **Module 6** (§1C, §5C), then **Module 4**
   (§1C, §7C, §8C) — these four modules hold nearly all the existing chemistry nouns.
4. **Module 14** (§2C, §3C, §4C) — repays the Module 10 IOU.
5. **Modules 8 and 9** bioenergetics section.
6. **Modules 15, 16, 17** light additions.

Each threaded section re-runs the module's full hardening loop and a
`rigor-reviewer` pass before commit.
