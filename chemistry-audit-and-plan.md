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
passage must convert a chemical or cellular quantity into a mechanical number the
existing course already uses. If a proposed passage cannot name the mechanical
parameter it explains, it does not belong.

**The unit of work is a trace, not a topic.** Under the interweaving requirement
(§2.2) the deliverable for each item is an unbroken chain
**molecule → cell → tissue → body**, ending on a number the course already prints.
A chemistry passage that does not terminate on an existing mechanical result is
decoration, however correct it is.

Worked example of the standard (numbers verified in Python): at `T = 310.15 K`,
`k_B T = 4.28 zJ` and `R_g T = 2.58 kJ/mol`. In-vivo ATP hydrolysis at
`Delta G ~ -55 kJ/mol` is `91.3 zJ` per molecule, i.e. `21.3 k_B T`. One power
stroke does `(5 pN)(10 nm) = 50 zJ = 11.7 k_B T`. So a crossbridge is about `55%`
efficient, and whole-muscle efficiency near `25%` is that figure minus the activation
overhead — SERCA pumping the calcium back. None of that calculation exists anywhere
in the course today, and it is what explains Module 9's cost of transport.

### 2.2 Shape — decided 2026-09-09, revised same day for interweaving

**Requirement added by the user:** chemistry, biology and physics must be
**interwoven**, and every physics result must be traceable back to its biological
and chemical origin.

That requirement kills the letter-suffix scheme this plan carried in its first
draft. A `§5C` section placed after §5 is **adjacency, not interweaving**: it leaves
§5 asserting `E_apatite = 100 GPa` and explains the number somewhere else. A reader
of §5 alone gets the book we already have. Worse, the suffix institutionalises the
split — it declares that physics lives in `§N` and chemistry in `§NC`, which is the
opposite of the requirement.

Judged against the five-part standard, the defect is exact. For the claim
`E = 17 GPa`, part 3 is *a proof in the smallest setting that shows the mechanism*.
Under the interweaving requirement the mechanism for a tissue property **is** the
chemistry, so the chemistry is not an addendum to that proof — it is the missing
first half of it, and it belongs **before** the Voigt/Reuss bound, because the bound
consumes `E_m` and `E_c` as inputs. A derivation that assumes its inputs and bounds
them afterwards is incomplete at the point of assumption.

**This is not new scope.** `prompt.txt` fixes a Multiscale Scope and a teaching
pipeline whose **step 3 is "physical mechanism" and step 4 is "molecular / cellular
substrate"**. The build executed steps 5–19 and skipped step 4. Interweaving means
running step 4 in every topic. This effort completes the original specification; it
does not extend it.

#### The revised shape

1. **`module00.html` — Chemical Foundations.** New, built **first**, to the full
   course standard. Its role is explicitly a **reference for the interwoven
   derivations**, not a container for the chemistry. A standalone foundations module
   is itself the anti-pattern the requirement forbids, so it earns its place only by
   being cited: **every section of Module 0 must be cited from at least one physics
   derivation in Modules 1–17**, or it is unearned and gets cut.
2. **Extend the derivation chains backwards inside Modules 1–17.** Every module runs
   a chain — load → stress → strain → material property → outcome — that currently
   *starts* at "material property, given". Interweaving means it starts at bond, ion
   and reaction and runs forward unbroken.
3. **Scope is chemistry *and* biology,** with biology as the load-bearing middle
   layer. Tracing physics to chemistry alone skips a layer and becomes reductionist
   hand-waving: a bond energy does not explain a remodeling rate — an osteoclast
   population does. Molecule → cell → tissue → body is the trace, and the cell rung
   is not optional.

#### Placement: subsection at the point of first use

Chemistry enters as a **subsection inside the physics section that first uses the
quantity** — `§5.4 Where the two moduli come from`, not a sibling `§5C`.

This is strictly better than the letter suffix on both counts:

- **Equally safe for renumbering.** A subsection under §5 does not shift §6, so all
  **250** in-prose `§N` references in M4, 248 in M5, 208 in M6 and 75 in M2 stay
  correct, and all 59 slug-based cross-file links are untouched either way.
- **Pedagogically correct.** The chemistry sits inside the derivation instead of
  beside it. The course already uses this form (`§3.5`, `8.1 What it gets right`).

#### The provenance rule — the gate that makes "interwoven" checkable

Every boxed constitutive parameter in the course — `E`, `c_F`, `mu`, `sigma_Y`, the
remodeling gain `k`, Hill's `a/F_max`, every time constant — must declare one of
three states:

1. **Derived here** from chemistry or cell biology, in this section.
2. **Derived in Module 0 §X**, with a link.
3. **Measured, not derived** — and the text says so, and says why no derivation is
   offered.

State 3 is legitimate and must be **visible**. The honesty of the book depends on
the reader knowing which parameters are earned and which are borrowed. Every other
standard in this repo is held by a script; an "interwoven" requirement with no gate
will drift by the third module. **Add `check_provenance.py`** to the hardening loop:
it flags any boxed parameter whose section declares none of the three states.

#### The three-layer opening

Every `§0` currently opens with a daily-life phenomenon and goes straight to
mechanics. Under interweaving, each `§0` states the three-layer question up front:
what you observe (physics), which tissue does it (biology), which molecule makes
that tissue behave that way (chemistry). Cheap to write, and it sets the reader's
expectation for the whole module.

#### Honest cost

The first draft of this plan was additive: seventeen new sections, existing prose
untouched. This revision **edits the existing derivations** in M2, M4, M5 and M6 —
the densest files in the repo — because that is where the chains have to be
extended. It is a larger job than the version this document carried before.

### 2.2b Interweaving map

Organised by **the physics result whose provenance is being supplied**, because that
is the unit of work the requirement defines. Format: *existing physics claim* →
**the trace that must be written**, and where it goes.

**Module 2 — bone**
- `E_apatite ~ 100 GPa`, `E_collagen ~ 1 GPa` (§5, currently asserted as inputs to
  the Voigt/Reuss bound) → **bond stiffness and bond density give both moduli**;
  calcium-phosphate solubility, supersaturation, nucleation in the collagen gap zone,
  and why mineralisation stops near 50%. Goes **before** the bound, inside §5.
- The mechanostat ODE `dZ/dt = k Z (eps - eps_hi)` (§7, self-labelled "a stated
  constitutive law, not a derived theorem") → **osteocyte fluid-shear sensing, then
  Wnt/sclerostin and RANKL/OPG mass action, then osteoblast and osteoclast
  populations, then the remodeling rate**, integrated to *derive* the mechanostat
  curve. This is the full molecule → cell → tissue trace and the course's best
  demonstration of the three-layer standard.

**Module 4 — cartilage**
- Fixed charge density `c_F` (§2, given) → **GAG sulfation chemistry**, placed inside
  §1 where the composite is introduced, so §2's Donnan derivation consumes a quantity
  the reader has watched being built.
- Boundary friction `mu_eq` (§7, given) → **hyaluronan and lubricin polymer physics.**
- The osteoarthritis cascade (§8, told as a narrative) → **MMP and aggrecanase
  kinetics** driving `c_F` down, closing the loop back onto §2.

**Module 5 — muscle**
- Crossbridge force and efficiency (§2) → **`Delta G` of ATP hydrolysis against
  power-stroke work**: `21.3 k_B T` available, `11.7 k_B T` delivered, about 55%
  crossbridge efficiency, about 25% whole-muscle after SERCA overhead.
- The action potential (§3, narrated) → **Nernst and Goldman–Hodgkin–Katz**, plus
  Na/K pump stoichiometry and the metabolic cost of excitability.
- Activation time constants (§5, fitted) → **cooperative Ca–troponin binding**, whose
  Hill coefficient and rate constants *are* the asymmetric rise and fall.
- `v_max` (§6, a constant) → **Arrhenius and `Q_10`**: why a cold muscle is weaker.

**Module 6 — tendon and ligament**
- The toe region (§1, derived from crimp geometry alone) → **entropic elasticity at
  the `k_B T` scale**, plus Gly-X-Y, hydroxyproline, the hydrogen-bond ladder and the
  D-period. The geometric and the entropic contribution must be separated, not merged.
- Modulus and hysteresis (§2, §7) → **cross-link density**: lysyl-oxidase enzymatic
  cross-links against non-enzymatic glycation cross-links.

**Module 14 — aging** (repays the IOU Module 10 §10 left)
- Each of the four parameter drifts gets its chemistry and cell biology: **protein
  turnover balance** (sarcopenia), **PTH, vitamin D and oestrogen, with bone as the
  body's calcium buffer** (osteoporosis), and **AGE accumulation kinetics in glucose
  and time** (tendon stiffening, bone embrittlement).

**Modules 8 and 9 — walking, running**
- Cost of transport and the power–duration curve (quoted empirically) → **the
  phosphocreatine, glycolytic and oxidative ATP supply systems** as a kinetic model
  with rate ceilings and capacities.

**Modules 15, 16, 17 — light**
- M15: biochemical markers (CTX, P1NP, lactate) and their error model.
- M16: the chemical-potential driving term generalising the existing poroelastic model.
- M17: one capstone project whose chain runs from molecule to whole-body outcome.

### 2.2c Provenance gate — decisions of 2026-09-09

§2.2 fixes the *rule*. This subsection fixes the two things a script needs that a
human reader does not: **which numbers it inspects**, and **what an acceptable answer
looks like in the text**. Both were put to the user as open design choices on
2026-09-09; both were decided in favour of the recommendation recorded below. Read
this before touching `check_provenance.py` — the definitions here are the contract,
and the script is only its implementation.

#### Why the gate needs a definition at all

A checker cannot know where a number came from. It can only read the page. So the
page has to say. And it cannot be pointed at "every number", because the boxes of
this course are full of numbers that have nothing to do with chemistry.

Worked from `module02.html`, the two kinds sitting side by side in one `.keyresult`:

| Number in a box | What it is | Gate? |
|---|---|---|
| `E ≈ 17 GPa` (`module02.html:171`) | cortical bone stiffness — a measured material property; mineral platelets and collagen crosslinks *set* it | yes |
| `σ_c ≈ 170 MPa` (`module02.html:181`) | compressive strength of cortical bone | yes |
| `G ≈ 3.3 GPa` (`module02.html:298`) | shear modulus of cortical bone | yes |
| `M = 70 kg` (`module02.html:181`) | the chosen reference human | no — a modelling choice |
| `R = 14 mm`, `r = 7 mm` | idealised femur geometry | no — a modelling choice |
| `g = 9.81` | universal constant | no |
| the load factor `2.5` | an assumption, derived later in Module 3 | no — already declared in prose |
| `F ≈ 1717 N`, `n ≈ 45` | computed *outputs* of the box | no |

The failure mode on each side is real. Flag everything and the gate reports several
hundred hits per module, its output stops being read, and it is dead inside a week.
Flag too little and the honesty claim of §2.2 is empty.

#### Decision 1 — what counts as a "boxed parameter"

**A symbol that carries physical units, appears inside a boxed result, and names a
property of a tissue or a material** — not a geometry, not a body mass, not a
universal constant, not a computed output of the box it sits in.

That definition catches `E`, `σ_c`, `G`, `c_F`, `μ_eq`, the remodeling gain `k`,
Hill's `a/F_max` and the constitutive time constants. It leaves `70 kg` and `14 mm`
alone.

**It is not executable as a regular expression, so the script splits it in two.**
"Names a property of a tissue" is a human judgement; no pattern decides it.

- **The mechanical half (the script).** Inside `.keyresult`, `.prop`, `.thm`, `.lem`
  or a `\boxed{}`, match an assignment of the form
  *symbol* `=`/`\approx`/`\sim`/`\simeq` *number* [`\times10^{n}`] *unit*, where the
  unit is a `\mathrm{}` or `\text{}` group. `<svg>` and `<pre><code>` content is
  skipped entirely — figure text and lab code are not prose claims.
- **The judgement half (a list in the script).** A **constitutive inclusion list** of
  canonical symbol names. Only a symbol on that list is gated.

**Inclusion, never exclusion.** A global exclusion list would be wrong on this course,
because the symbol namespace already collides: `T` is torque in Module 2 and
temperature in every chemistry section; `a` is acceleration in Module 1 and Hill's
constant in Module 5; `F` is force everywhere and Faraday's constant in Module 4;
`mu` is friction in Module 4 §7 and chemical potential in Module 4 §2; `k` is the
Module 2 remodeling gain and wants to be a rate constant. An exclusion list silently
un-gates the interesting cases. An inclusion list fails visibly instead.

**The list is written from the inventory, not from memory.** `check_provenance.py`
has an `--inventory` mode that dumps every mechanical-half hit across all 17 modules,
grouped by symbol, with counts and `file:line`. That dump is committed as
`provenance-baseline.txt`. Reading it, and only then writing the inclusion list, is
the step §2.2b and Part 3 call "replaces the judgement calls with a measured list".

#### Decision 2 — the exact wording a section must carry

The three permitted states are unchanged from §2.2: *derived here*, *derived in
Module 0 §X*, *measured, not derived, because …*.

Two routes were considered for how a section says one of them.

**Plain prose.** The course already does this once, and does it well.
`module02.html:181` reads: "The factor $2.5$ is an assumption here (Appendix) …
Module 3 derives the factor from that balance." That is a textbook state-2
declaration in ordinary English. But no script can find it reliably: the next author
writes "we take", "assumed", "quoted from", "this module does not derive", and fifty
other phrasings. Grepping a phrase list gives false passes and false failures
forever, which is the same as no gate.

**An explicit marker.** Found every time, no guessing. Costs an authoring step and a
17-module retrofit.

**Decided: the marker, with the prose sentence inside it**, so the reader sees normal
writing and the script sees a reliable hook.

```html
<span class="prov" data-sym="E" data-state="measured">measured, not derived: the
composite modulus of cortical bone is reported from mechanical test, and
<a href="module00.html#bonding">Module&nbsp;0 §2</a> derives only its two
end-member inputs.</span>
```

- `data-state` takes exactly one of `derived` (state 1), `module0` (state 2),
  `measured` (state 3). Any other value is a hard failure.
- `data-state="module0"` requires an `<a href>` inside the span. A pointer with no
  link is not a pointer.
- `data-state="measured"` requires the word `because` or a `:` followed by at least
  40 characters. State 3 without a reason is the exact dishonesty the gate exists to
  stop.
- **A `<span>` per symbol, not an attribute on the box.** `module02.html:181` carries
  two gated parameters in one `.keyresult`; a box-level attribute cannot describe
  both.
- **Scope is one declaration per symbol per module**, anywhere in the file, first use
  recommended. The gate checks existence per `(module, symbol)`, not per box —
  otherwise every box that mentions `E` sprouts a marker and the prose drowns.
- **It must render visibly.** §2.2 says state 3 "must be visible"; a bare `<span>` is
  not. One CSS rule in the module `<style>`, added to the skill template:
  `.prov{border-left:3px solid #c08a00;padding-left:.5em;display:inline-block}`.

**Canonical `data-sym` names are fixed here, not in Module 0.** `HANDOFF.md` defers
the chemistry symbol namespace to Module 0's appendix, but the first marker written
needs the names already settled, so the record leads and Module 0 follows it:

| `data-sym` | meaning | collides with |
|---|---|---|
| `E` | Young's modulus (tissue) | — |
| `G` | shear modulus | Gibbs free energy → use `DeltaG` |
| `sigma_c` | compressive strength | — |
| `sigma_Y` | yield strength | — |
| `c_F` | fixed charge density | — |
| `mu_fric` | friction coefficient | chemical potential → `mu_chem` |
| `mu_chem` | chemical potential | friction → `mu_fric` |
| `k_remodel` | Module 2 mechanostat gain | rate constants → `k_on`, `k_off` |
| `k_on`, `k_off`, `K_d` | binding kinetics | — |
| `a_hill`, `F_max` | Hill's constant, peak isometric force | acceleration `a` |
| `F_faraday` | Faraday's constant | force `F` |
| `R_g` | gas constant | radius `R` (Module 4 already renamed this) |
| `k_B` | Boltzmann's constant | `k_remodel` |
| `E_apatite`, `E_collagen` | end-member moduli, Module 2 §5 | `E` |
| `tau_*` | constitutive time constants | — |
| `dG0_ATP` | transformed standard free energy of ATP hydrolysis | Gibbs free energy `G` → `DeltaG` |
| `c_metab` | measured cellular metabolite concentration (ATP, ADP, Pi, Ca) | fixed charge density `c_F`; lattice parameter `c` |

**Fallback, not the default.** If per-use markers prove too heavy to retrofit, each
module's appendix parameter table already lists every parameter with a source column,
and the gate could read that instead. This is recorded as an option only — it is
weaker, because it moves the admission away from the point of use, which is where a
reader needs it.

#### Amendments forced by the first inventory run — same day

Decision 1 was written before the script existed, and the first `--inventory` run
over all 17 modules contradicted two parts of it. Both are corrected here, with the
evidence, because this record is the contract and the script only implements it.

**Amendment A — the scope is the whole prose body, not only boxed results.**

The first run, restricted to `.keyresult` / `.prop` / `.thm` / `.lem` / `\boxed{}`,
found **91 units-bearing assignments in 5.6 MB of course** — and `E ≈ 17 GPa` was
not among them. The course does not state its constitutive parameters inside boxes.
It states them in prose, in definition blocks and in tables, and *consumes* them in
boxes. `module02.html:171` puts `E ≈ 17 GPa` inside Definition 1.3; `module04.html`
first gives `c_F` in a composition table. A gate that only reads boxes would have
passed a course with every borrowed number undeclared, which is the exact failure it
exists to prevent.

Widening the scan to the whole body (minus `<svg>` and `<pre><code>`) raises the
count to **494 assignments over 156 distinct symbols**. The box flag is kept, but as
a priority hint printed by `--inventory`, never as a filter.

This does not loosen the gate, because the *inclusion list* was always the real
filter. Boxing was a proxy for "the course commits to this number", and it turned out
to be the wrong proxy.

**Amendment B — units filter the inventory, not the gate.**

Requiring a `\mathrm{}` unit is what keeps the inventory readable. But two of the
parameters §2.2b names are dimensionless: the boundary friction coefficient `mu` in
Module 4 §7 and Poisson's ratio `nu`. Neither carries a unit group, so neither was
visible. Corrected: an assignment **with** a unit enters the inventory; an assignment
of a symbol **already on the inclusion list** is gated with or without one.

**Amendment C — a list entry may be narrowed to a unit.**

`k` is leg stiffness in `kN/m` in Modules 8–9 and hydraulic permeability in
`m⁴/(N·s)` in Module 4. The first is a lumped whole-body fit; the second is a
borrowed constitutive parameter that owes a chemistry trace. One symbol, two
meanings, so a list entry may be written `k@m^4` to bind it to a unit. This is the
same collision problem that made an exclusion list unworkable, met once inside the
inclusion list.

#### The measured inclusion list, and the baseline it produced

The list now in `check_provenance.py` was written by reading the inventory, and every
entry is tagged in the source: `[inv]` for one the course already uses, `[pre]` for a
name pre-registered so the chemistry build's first use is gated rather than
retrofitted. Voigt and Reuss bounds `E_V`, `E_R` are deliberately **not** gated —
they are computed in Module 2 §5, not borrowed.

Running the gate over the 17 modules as they stand gives **37 undeclared gated
parameters**. That number, and the `file:line` for each, is committed as
**`provenance-baseline.txt`** (inventory in Part 1, worklist in Part 2). It is the
"measured list" Part 3 step 0 calls for, and it replaces the judgement calls in
§2.2b. Regenerate it, never hand-edit it.


**Amendment 4 (2026-09-09, forced by Module 0 §3).** The table above was written from an inventory of the *existing* seventeen modules, so it held no chemistry parameter at all. §3 is the first section to state one, and it states two kinds: a tabulated standard free energy and a set of measured cellular concentrations. Both are added above as `[pre]` entries in `check_provenance.py`, so that the first use in Module 5's crossbridge energetics is gated rather than retrofitted. `c_metab` is deliberately generic: one marker declares the provenance of a whole measured concentration set, because those six numbers come from one method and share one caveat.

#### What the gate does not do

It does not check that a declaration is *true*. A section can mark `E` as
`data-state="derived"` and derive nothing. That is the same class of defect the nine
gates already fail to see — "green gates, wrong book" — and it stays with the
`rigor-reviewer` pass, not with a script.

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
6. **Never renumber an existing section.** Chemistry enters as a **subsection at the
   point of first use** (§2.2), which shifts no integer section number. A renumber
   would silently misdirect up to 250 in-prose references per module while every
   automated gate still passed — green gates, wrong book.
7. **Re-run the full hardening loop on every module a trace touches**, plus a
   `rigor-reviewer` pass. Interweaving reopens the derivations the editor pass closed
   at `a93a55c`; that is the accepted cost of the chosen shape.
8. **Add `check_provenance.py` to the hardening loop** before the first trace is
   written (§2.2). Every boxed constitutive parameter must declare *derived here*,
   *derived in Module 0 §X*, or *measured, not derived, because …*. Without a gate,
   "interwoven" drifts by the third module.
9. **Rigor parity applies to the traces.** The existing rule — if one boxed result in
   a section gets a Proposition and a proof, its siblings of equal weight must too —
   now binds the chemistry. A derived `E_apatite` sitting beside an asserted
   `E_collagen` is the Module 6 §6 defect in a new place.

---

## Part 3 — Decisions and build order

Decided with the user on 2026-09-09:

| Question | Decision |
|---|---|
| Shape | Interweave into the existing 17, plus one new `module00.html` |
| Scope | Chemistry **and** biology (signalling, endocrine, tissue turnover) |
| Module 0 depth | Full course standard — 30 problems, labs, figures, appendix |
| Build order | Module 0 first |
| Structure | Subsection at point of first use; **no** `§NC` letter suffixes |
| Enforcement | `check_provenance.py` added to the hardening loop |
| Gated symbols | Units-bearing tissue/material properties inside a boxed result, chosen by an **inclusion list** written from the measured inventory (§2.2c) — never an exclusion list, because the symbol namespace collides |
| Declaration form | `<span class="prov" data-sym="…" data-state="derived\|module0\|measured">prose</span>`, one per symbol per module, rendered visibly (§2.2c) |

**Order of work**

0. **`check_provenance.py` first**, before any prose. Write the gate, run it over all
   17 existing modules, and keep its output as the baseline inventory of every
   borrowed parameter in the course. That inventory *is* the definitive worklist —
   it replaces the judgement calls in §2.2b with a measured list.
1. **Module 0**, section by section under the standing convention: build one section,
   report with a short summary and two `★ Insight` bullets, review, then commit and
   push. Fix the chemistry symbol namespace in its appendix before §1 is written, and
   get one representative molecular figure approved before mass-producing the rest.
   Its sections are written **to serve the traces in step 2 onward**, not as a survey
   of chemistry.
2. **Module 5** — the largest deficit against the largest existing narrative, and the
   ATP efficiency trace is the single best demonstration of the standard.
3. **Module 2**, whose §7 mechanostat trace is the course's only full
   molecule → cell → tissue → body chain; then **Module 6**, then **Module 4**.
4. **Module 14** — repays the Module 10 IOU.
5. **Modules 8 and 9** — bioenergetics of locomotion.
6. **Modules 15, 16, 17** — light additions.

Each trace re-runs the module's full hardening loop, `check_provenance.py`, and a
`rigor-reviewer` pass before commit.

**Open question deferred to the build.** Module 0 is written first but is defined by
what the traces need. Expect to revise it after Modules 5 and 2 are interwoven — the
traces will show which foundations sections were guessed at and which are load-bearing.
That is intended, not a planning failure.
