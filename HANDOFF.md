# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last written:** 2026-09-09 (fifth refresh, at the Module 0 §4 boundary).
Phase A (editor pass) is **complete and promoted**. Phase B (chemistry and biology
interweaving) has its **gate and worklist built**, and **Module 0 §0–§4 are written, hardened and live**. Start at
"Next task": Module 0 §5 — but first check whether the §4 reviewer pass
landed; if no findings commit exists, re-run it before building §5.

---

## Current state

Everything below is committed and pushed to `main`
(https://github.com/az9713/biomechanics). Working tree clean; local `HEAD` and
`origin/main` verified equal at each step.

### Phase A — the editor pass: COMPLETE AND PROMOTED (`121cce9`)

All fifteen modules (3–17) have a report in `editor-reports/` and an applied draft
that is now **the live file**. Modules 1 and 2 were done in place earlier
(`3a4dae1`, `ac93c14`). Roughly 1000 anchored edits, ~14 000 lines of report.

Promotion, 2026-09-09: the user chose *promote all fifteen at once*. Each
`edited/moduleNN.html` was moved over its original and `edited/` was removed, so the
draft URLs `https://az9713.github.io/biomechanics/edited/moduleNN.html` now 404.
Two verifications were run and both passed:

1. **The move was proved, not assumed.** `git show HEAD:edited/moduleNN.html` diffed
   against the promoted file. Fourteen byte-identical; module 3 differed only by the
   one intended fix. **Use `--strip-trailing-cr`** — without it Git's LF↔CRLF
   conversion makes every line appear changed and the check looks like total
   corruption.
2. **All twelve gates re-run in place on all fifteen.** Zero hard failures, zero
   `mjx-merror`, zero broken links, zero label overlaps, zero clipped figures.
   Remaining advisories are the pre-existing ones the reports already log (e.g.
   `editor-reports/module03.md:687` records "0 hard, 3 advisory" before and after).

The module 3 drift is **closed**. `module03.html:860` said the hip resultant spans
2.6–2.8 W over α = 20° to 40°; its own equation
$|R| = W_s\sqrt{(1+b/a)^2 + ((b/a)\tan\alpha)^2}$ with $W_s = \tfrac56 W$, $b/a = 2$
gives 2.5725 / 2.6788 / 2.8646 W at 20° / 30° / 40°, so the upper endpoint is 2.9.
Corrected. No other line restates the range.

> `DEVELOPMENT_JOURNEY_2.html` describes the **pre-promotion** state (around its
> lines 1019–1029 it says "nothing is promoted" and lists the 2.8 drift as open). It
> is a dated record of that session. **Do not re-open those items from it.**

### Phase B step 0 — the provenance gate: COMPLETE (`ce3620d`)

The gate that makes "interwoven" checkable exists, and its first run produced the
chemistry worklist.

- **`check_provenance.py`** — in the skill scripts directory with the other twelve
  gates, and added to the `CLAUDE.md` hardening loop. `--self-test` passes 9
  fixtures. `--inventory` dumps the worklist. It splits the definition in two: a
  regex finds every `symbol = number unit` assignment, and an explicit **inclusion
  list** of canonical symbols does the judgement half. Inclusion never exclusion —
  the namespace collides (`T` torque/temperature, `a` acceleration/Hill, `F`
  force/Faraday, `mu` friction/chemical potential, `k` remodeling gain/rate
  constant), and an exclusion list would silently un-gate the interesting cases.
- **`chemistry-audit-and-plan.md` §2.2c** — the contract the script implements, with
  both decisions, the reasons, the rejected alternative, the canonical `data-sym`
  names, and three amendments the first run forced. **Read §2.2c before touching the
  script or writing a marker.** The script is only the implementation.
- **`provenance-baseline.txt`** — generated, never hand-edited. Part 1 the full
  inventory (494 assignments, 156 distinct symbols across 17 modules); Part 2 the
  gate output: **37 gated parameters used with no provenance declaration**, each with
  `file:line`. **That is the chemistry worklist**, and it replaces the judgement
  calls in `chemistry-audit-and-plan.md` §2.2b.

The declaration a section must carry:

```html
<span class="prov" data-sym="E" data-state="measured">measured, not derived,
because …</span>
```

`data-state` is exactly one of `derived` / `module0` / `measured`. State `module0`
must contain an `<a href>`; state `measured` must give a reason. One declaration per
symbol per module, first use recommended. The `.prov` CSS rule is in the skill
template so it renders visibly rather than only parsing.

### Phase B step 1 — Module 0 §0: DONE (`d985962`, `54bd525`, `b849a77`)

**A `rigor-reviewer` pass ran and returned NEEDS-FIXES; all its findings are
applied (`b849a77`).** Rigor parity and K-depth passed; prose and
self-containment failed. The severe one was a **circularity I wrote**: §0 claimed
the mineral and collagen moduli "fall out of the ladder", but the ladder's `k`
column is *defined* as the `k` for which `E = k/r₀` holds, so 25 and 0.30 N/m had
been calibrated **from** Module 2 §5's measured moduli. §0 now says so and carries
`.prov` markers for `E_apatite` and `E_collagen`. **Lesson for §2 and for every
later trace: a calibrated parameter dressed as a derived one passes every gate.**
The reviewer also caught a wrong formula (the Coulomb curvature of the attractive
term alone is negative and is not a bond stiffness; the Born result is
`k = (n−1)C/r₀³`) and three over-claims. Run the reviewer on every section.

Reviewer note carried forward: the plan's `data-sym` table has **no entry for bond
stiffness `k`**, which collides with Module 2's remodeling gain and Module 4's
permeability. §0 names it `k_bond` in-text; the Appendix must register it.

`module00.html` exists and is live, wired into `index.html` and `README.md`. §0
("why a bond energy sets a bone's stiffness") is complete: the three-layer opening,
the $E\sim k/r_0$ scaling bridge, the four-rung stiffness ladder that recovers Module
2 §5's two end members (104 GPa, 1.07 GPa), the $k_BT$ ruler, and the roadmap table
naming the debt each of §1–§9 repays. Numbers Python-verified. All thirteen gates
green; `check_provenance` reports 6 assignments / 1 declaration / 0 issues — the
course's first live `.prov` marker (`E` for cortical bone, state `measured`).

**`checktex.py` was fixed in the same commit.** `\left`/`\right` now count only when
a *delimiter* follows; a letter means a named arrow or harpoon. So
`\rightleftharpoons` (needed for every chemical equilibrium) and the
`\leftrightarrow` false positive `CLAUDE.md` documents both stop firing. Re-run over
all 17 existing modules: 0 issues, no regression. The script is still outside git.

**Figure style: APPROVED 2026-09-09.** The user signed off §0's Fig. 1 (three-panel
zoom: femur → mineralised fibril → one Ca–O bond as a spring) as the representative
molecular figure. The checkpoint `CLAUDE.md` requires is closed — molecular figures
may now be drawn without asking again. The style lives in scratchpad `fig0lib.py`
(shared `m0*` defs: `m0bone/m0sph/m0coll/m0apat`, atom gradients `m0aCa/m0aO/m0aC/
m0aN/m0aP`, markers `m0red/m0blu/m0grn/m0gry`; helpers `bone/atom/spring/arrow/txt/
zoomwedge`) and is already spliced into `module00.html` between the `<!-- DEFS0 -->`
and `<!-- FIG1 -->` marker pairs by `assemble0.py` (idempotent).

### Phase B step 1 — Module 0 §1: DONE (`0346f4f`, `72b5b16`)

§1 ("the mole, concentration, and the $k_BT$ / $R_gT$ bridge") is complete and live.
It is the unit every later chemistry section is quoted in. Contents: Definitions
1.1–1.3 (amount of substance, molar concentration, equivalents and osmolarity); the
boxed identity `n_V = c N_A`, `1 M = 0.6022 nm⁻³`, spacing `1.184 nm (c/M)^(−1/3)`;
an eleven-decade concentration ladder for the body; **Lemma 1.1** (lattice counting →
the dilution free energy `k_BT ln(c/c°)`); **Proposition 1.1** (the `N_A` bridge and
its same-composition condition); the dictionary table and the boxed
`1 k_BT = 2.58 kJ/mol`; the ATP repayment (19.4 k_BT → a crossbridge cannot average
more than **8.30 pN** over Module 5's 10 nm stroke); and **Proposition 1.2**
(binomial → Poisson counting noise: resting calcium is ~64 free ions in one
half-sarcomere, 12.5%). Three computed figures. All thirteen gates green.

**A `rigor-reviewer` pass ran and returned NEEDS-FIXES; all 36 findings are applied
(`72b5b16`).** Numbers and every cross-module citation verified correct. Three
lessons worth carrying:

1. **A proof can be valid in its conclusion and wrong in its argument.** The first
   Proposition 1.1 derived `ΔG = N_A Δg` from "the total entropy is the sum of the
   per-molecule entropies" — false for identical particles, and flatly contradicting
   the Lemma 1.1 it cited. The fix was to *define* `Δg` as the system free-energy
   change per molecule of reaction advance at fixed composition, so the result
   follows from what a molar quantity means. **`check_proofs.py` sees a `.proof`
   next to a `.prop` and passes; it cannot read the argument.**
2. **"if and only if" is where over-claims hide.** "Vanishes iff every species sits
   at its reference concentration" was wrong three times over — `Q = 1` suffices.
3. **Rebuild a figure, re-read its caption.** Fig. 3 was drawn horizontally, then
   rebuilt as a vertical ladder because seven rotated labels collided; the caption
   still said "below/above" and "left to right". Every gate stayed green. This is
   the course's worst defect class and it recurred inside one session.

**Symbol namespace fixed by §1** (Module 0's Appendix must register these): `M_m`
molar mass, `M_tot` a total molecule count (`M` stays body mass / bending moment),
`A` the Helmholtz free energy (`F` stays force), `u_0` per-molecule internal energy
(`ε` is permittivity in §0), `n_V` number density, `μ` chemical potential (against
Module 4 §7's `μ_fric`), `σ_N` a standard deviation (against §0's stress `σ`), `c°`
the standard concentration. §1 names each collision in prose at first use.

**`check_svg.py` was patched** (same session, script still outside git): its
figure-citation regex was `Fig\.\s*\d+`, which never matched this course's
`Fig.&nbsp;N`, so every module falsely reported "figures but no Fig. N reference".
It now accepts `&nbsp;`. Re-run over modules 0, 2, 4 and 10 — no new failures.

### Phase B step 1 — Module 0 §2: DONE (`c6d8e44`, `59a19c0`)

§2 ("bonding and the stiffness ladder") is complete and live. It pays §0's largest
debt. §0 had *calibrated* its bond stiffnesses backwards from Module 2 §5's measured
moduli, so its `104 GPa` was that measurement handed back; §2 runs the arrow forwards.

Contents: **Definition 2.1** (Born ionic potential) and **Lemma 2.1**
(`k_pair = (n−1)𝒜/r₀³ = 467 N/m` for Ca–O); **Proposition 2.1** — the affine estimate
is a rigorous *upper bound*, proved as a Schur complement, which is also the theorem
that makes Module 2 §5's Voigt average an upper bound; **Proposition 2.2** — the boxed
`K = n|U_latt|/(9V_f)`, i.e. a bulk modulus **is** a cohesive energy density and the
structure constant cancels — with the rocksalt corollary
`K = (n−1)α_M|z₁z₂|C_e/(18r₀⁴)`. Validated on NaCl (24.8 predicted vs 24.4 measured),
MgO (273 vs 160) and CaO (187 vs 111), with the 1.7× divalent-oxide overshoot diagnosed
and the implied `n` printed. Then apatite: `V_f = 0.5279 nm³` (P6₃/m, Z = 1),
`|U_latt| = 34191 kJ/mol` (Born–Fajans–Haber; Zhang & Tamilselvan, *J. Mater. Sci.
Mater. Med.* **18**, 79–87, 2007), `n = 8` → **`K = 95.6 GPa`** and **`E = 143 GPa`**
against a measured 114. The 17× gap decomposes exactly: `α_M/12 = 1/6.87` is lattice
bookkeeping, then dilution (204 → 108 GJ/m³), then the polarizability residual. Four
figures (5–8). `E_apatite` flipped from `measured` to `derived`.

**A `rigor-reviewer` pass ran and returned NEEDS-FIXES; all 31 findings are applied
(`59a19c0`).** Every number it recomputed independently held. Four lessons:

1. **A "first-principles" parameter can be calibrated one step upstream.** §2 claimed
   "Nothing elastic enters" because `n` came from Pauling's electron-configuration rule
   rather than from a fitted compressibility. But Pauling's five integers were
   themselves chosen to reproduce *alkali-halide* compressibilities. So NaCl's success
   is a consistency check inside the calibration class, not a prediction — the exact
   distinction §2 was lecturing §0 about. **Ask where a "table value" came from before
   calling a result derived.** The state stays `derived`, with the borrowing disclosed
   inside the marker.
2. **A section can deny a hypothesis and then use it.** §2 said the inversion-centre
   condition "is true of rocksalt and false of almost everything else", naming apatite —
   then forty lines later derived `ν = ¼` from the Cauchy relation, which needs that
   same condition. Now stated as an assumption, with its 143 → 132 GPa cost given.
3. **A figure can carry a marker for a calculation that was never run.** Fig. 6 drew a
   route-A point on apatite; route A is the rocksalt formula. Every gate passed.
4. **Render every figure and look at it.** Two figures passed all nine gates while
   being visibly wrong — a dotted leader line that read as a curve, and three rungs
   crammed illegibly onto a log axis. `check_frame` caught a third (clipping) only
   after the redraw.

**`check_provenance.py` was patched** (script still outside git): its `module0` state
required the literal substring `<a href`, which rejects every link in this course —
they are all written `<a class="secref" href=…>`. Now a regex for any `<a …href=`.
Self-test still 9/9.

**Symbol namespace fixed by §2** (Module 0's Appendix must register these): `k_bond` /
`k_pair` bond stiffness; `𝒜` the Born attraction coefficient (`A` stays §1's Helmholtz
free energy); `γ_s` the structure constant in `V = γ_s r³` (`c` is §1's concentration
*and* apatite's lattice parameter); `n` the Born exponent (against §1's amount of
substance); `ν` Poisson's ratio (against §1's stoichiometric `ν_i`); `C_e` the Coulomb
constant `e²/4πε₀`; `U_latt`; `V_f`; `α_M` the Madelung constant; `K` bulk modulus.

<!-- SEC3-HANDOFF -->
### Phase B step 1 — Module 0 §3: DONE (`455ca86`)

§3 ("thermodynamics: free energy, chemical potential, and coupling") is complete and
live. It pays the two debts §1 named *and* a third §1 had borrowed without listing.

Contents: **Definition 3.1** (enthalpy, entropy, Gibbs free energy) and the boxed
`ΔG = ΔH − TΔS`, marked explicitly as a rearranged definition that earns no proof;
**Proposition 3.1**, the maximum-work theorem `W ≤ −ΔG`, proved from the Clausius
inequality — this is the inequality §1 used to bound crossbridge force and labelled
"§3 derives it"; **Definition 3.2** (chemical potential) and **Proposition 3.2**
(`μ_i = μ_i° + R_gT ln(c_i/c°)`, carried over from §1 Lemma 1.1 by the `N_Ak_B = R_g`
identity); **Definition 3.3** (reaction quotient, standard free-energy change);
**Proposition 3.3**, the headline boxed `ΔG = ΔG° + R_gT ln Q`; **Proposition 3.4**,
boxed `ΔG° = −R_gT ln K_eq`, with uniqueness proved from affine ⇒ injective;
**Definition 3.4**, the transformed biochemical standard state; and **Proposition 3.5**
(coupling), whose load-bearing hypothesis is the *shared intermediate*. Three figures
(9–11). All thirteen gates green.

**A `rigor-reviewer` pass ran and returned NEEDS-FIXES; all 28 findings are applied
(`e64b6ad`).** Rigor parity, prose and self-containment all failed; K-depth passed
trivially (§3 has no problems). The reviewer reproduced every headline number by hand
and all held, and decoded Fig. 9/10/11 pixel positions back to those values. Fixes were
applied to **`sec3.html`**, the prose fragment, and re-spliced — so `assemble3.py`
stays the single path into the page and the whole chain is still idempotent.

**Four arguments reached a true conclusion by a wrong route — the §1 defect class,
caught for the third section running.**
1. Prop 3.5's proof credited the sum rule to the shared intermediate. The sum rule is
   only linearity of `Σν_iμ_i`; the intermediate supplies a **constraint**, `ξ₂ = mξ₁`,
   which collapses two reaction extents to one and removes the unfavourable half's
   freedom to stand still. The old A→B→C construction also mismodelled the mechanism:
   SERCA does not finish hydrolysis before it pumps. Rewritten via extents.
2. Prop 3.2 scaled by `N_A` using a finite-addition reading — the exact argument §1's
   reviewer had already corrected once. It is the chain rule (`N_i = N_molec/N_A`),
   true for any `G`; the dilute hypothesis is inherited from Lemma 1.1.
3. Prop 3.4's statement said "exactly one composition" while its own proof said
   infinitely many compositions are equilibria. **Uniqueness is in `Q`.**
4. Prop 3.4 and Prop 3.5 both leaned on "ΔG < 0 means it runs", which is Prop 3.1 at
   `W = 0` and was never stated. Added **Corollary 3.1.1** with a proof.

Alberty's Legendre-transform theorem had been asserted inside Definition 3.4 while
every number below rests on it; now named as a borrowed import, with a sketch.

**Three claims were false or overstated and are corrected.** "Any model that lets a
crossbridge deliver a constant force is violating the second law" is false — a constant
5 pN sits under both ceilings; the disclaimer is now quantitative (§1's measured head
force of 3–6 pN lies below both ceilings, so the limit never binds). "3:1 is impossible
at rest" overstated a +8.7 kJ/mol margin that a gradient factor of 3.09 would close;
"forbidden" is kept only for the working muscle. And thermodynamics **caps** the
stoichiometry at two — it does not pick two over one.

**Numbers, all Python-verified in `nums3.py` with assertions:**
- `ΔG°′` moved from 298.15 K to 310.15 K using the boxed `ΔG = ΔH − TΔS`: **−30.90
  kJ/mol** (from tabulated −30.5 and ΔH°′ = −20.5, so ΔS°′ = 33.5 J/mol·K).
- ATP in skeletal muscle: **−62.5 kJ/mol resting, −52.7 kJ/mol fatigued**. The whole
  difference from the standard value is the `R_gT ln Q` term.
- `K_eq = 1.60×10⁵`; a resting cell sits **3.4×10¹⁰** from equilibrium.
- **SERCA**: a 10⁴ calcium gradient costs 23.75 kJ/mol per ion. Two per ATP spends
  76% of the budget at rest, 90% fatigued. Three costs 71.3 and stands above **both**
  budgets, so 3:1 is thermodynamically forbidden. The measured stoichiometry is two.
  **A biological design parameter recovered from thermodynamics alone** — the most
  valuable thing the section does.
- Max gradient a 2:1 pump can hold: 1.8×10⁵ at rest, 2.8×10⁴ fatigued, against an
  actual 10⁴ — which is where Module 5's slowed relaxation in a fatigued muscle
  comes from.

**§1 was corrected, not contradicted.** §1 derived a crossbridge ceiling of
`8.30 pN` to three figures from a round `50 kJ/mol`. §3 computes the ceiling at both
compositions and finds it is **not one number**: 10.38 pN resting, 8.76 pN fatigued.
§1 now carries a **fourth caution** saying so and pointing at §3 (`fix1_ceiling.py`,
anchor asserted unique, idempotent). §3 states plainly that this is *not* the cause
of fatigue — the measured force loss is far larger and its mechanism is phosphate
acting on the crossbridge cycle, which is Module 5's business.

**`check_provenance.py` gained two `[pre]` chemistry names** — `dG0_ATP` and
`c_metab`. The `GATED` table had been written from an inventory of the seventeen
*pre-chemistry* modules, so it contained no chemistry parameter at all and §3's
markers were rejected as non-canonical. Recorded as **amendment 4** in
`chemistry-audit-and-plan.md` §2.2c, so Module 5's crossbridge energetics is gated
at first use rather than retrofitted. Self-test still 9/9. **Script still outside git.**

**Four lessons from this section.**
1. **A gate can be structurally blind rather than wrong.** The provenance table was
   complete for the modules it was built from and empty for the ones it was built
   *for*. Nothing failed; the first chemistry marker simply had no legal name.
2. **Unicode has no subscript `g`.** The figure generator's subscript table silently
   substituted subscript `s`, so Fig. 9's slope label read `R_sT` when this course's
   gas constant is `R_g`. Every gate passed. **Only rendering the figure and reading
   it caught this.** Multi-letter and unavailable subscripts need a `<tspan
   baseline-shift="sub">`, which is how `ln K_eq` is drawn.
3. **A link gate can pass on the wrong book.** `autolink_sections.py` wrapped any bare
   `§N` in a local link without checking for a preceding "Module N", so `module00.html`
   carried four **wrong-book** references: "Module 4 §2" pointed at Module 0's §2 and
   "Module 5 §3" at Module 0's §3. `check_links` passed on all four, because the
   anchors resolve. One of the four was created by this session's own autolink run.
   **Fixed at the root** — the script now refuses a `§N` preceded by `Module <k>` and
   prints how many it left alone (7 in this file). A sweep of all 18 modules: module17's
   two hits are false positives; **`module04.html:1868` is ambiguous and untouched**
   ("testing them against Module 3 (§6)" links §6 to Module 4's own `#contact`, which
   may be intended). Worth a decision when Module 4's trace is written.
4. **`check_overlap` again beat the eye, 4–0.** Two labels on a dashed drop line, one
   on a bilayer midline, one on a dashed budget line — all invisible in a preview I
   had already looked at twice.

**Symbol namespace fixed by §3** (Module 0's Appendix must register these): `H`
enthalpy (against Module 4's `H_A`); `S` entropy; `T` absolute temperature (against
Module 3's torque `T`); `G` Gibbs free energy (against shear modulus `G`); `μ_i`
chemical potential (against Module 4 §7's `μ_fric` and §2's `ν`); `Q` reaction
quotient; `K_eq` equilibrium constant (against §2's bulk modulus `K`); `W`
non-expansion work, with `W_ne` reserved for any calculation that also carries
Module 1's body weight `W`; `ν_i` stoichiometric coefficient; `ΔG°′` the transformed
standard quantity, primed throughout and never mixed with the unprimed `ΔG°`.

---

### §4 — a conflict found before writing, and it is not small

Scoping §4 turned up a **contradiction between the plan, §0/§2, and Module 6**, plus
a claim that is quantitatively wrong. Resolve this before writing a line of §4.

**1. Module 6 does not have the hole §4 was told to fill.** `chemistry-audit-and-plan.md`
§2.3 says §4 is "the missing molecular origin of Module 6's toe region", and
`module00.html`'s roadmap table says §4's customer is "Module 6's toe region,
currently derived from crimp geometry alone". But `module06.html:144` says the toe
"is *not* the collagen stretching — it is the crimp straightening out", and
`module06.html:151` says it "is not a material property of a single fibril — a
straightened fibril is nearly linear. It is a *population* effect", then **proves**
a parabolic toe from a uniform crimp distribution (Module 6 Proposition 1). Module 6
already owns the toe, structurally and with a proof. §4 must **not** claim to supply
its origin; doing so would contradict a proved result in a live module.

**2. The "factor of fifty" §2 handed to §4 cannot be paid the way §2 said.** §0's
`E_collagen` marker and §2's closing both assert the collagen fibril's compliance
"is entropic, not a bond length being stretched", and §2 says "the factor of fifty is
§4's to compute". Checked numerically (`probe4.py` in scratchpad): rubber elasticity
`E = 3nk_BT` at 1.07 GPa demands one network chain per **(0.23 nm)³** and a molar
mass between crosslinks of **10 g/mol** — a tenth of one amino-acid residue, and a
chain spacing equal to a single bond length. The entropic mechanism is not fifty times
short of collagen, it is about **1000×** short, and the network it implies is
physically impossible. **§0 and §2 over-claimed, and §4 must say so.**

**3. What §4 can honestly derive instead — and it is a real forward prediction.**
The same `E = 3nk_BT` applied to **elastin** (measured `E ≈ 1.1 MPa`, density
1300 kg/m³) gives a molar mass between crosslinks of **9.1 kDa** against a literature
**6–7 kDa** — right within a factor of 1.4, with no elastic datum among the inputs.
That is §4's apatite moment, and elastin is the tissue protein whose elasticity
genuinely *is* entropic. Natural rubber checks the same way (4.9 kDa). The honest
shape of §4 is therefore:
- derive `f = −T ∂S/∂x` and the freely jointed and worm-like chain properly;
- get `E = 3nk_BT`, predict elastin forward, and **succeed**;
- apply it to collagen, **fail by 1000×**, and correct §0/§2's claim — naming the
  real causes of collagen's compliance (interfibrillar shear and the helix's own
  bending compliance, not chain entropy);
- keep the **thermoelastic discriminator**, which is the section's cleanest teaching
  result: entropic force is `∝ T`, so elastin and rubber *stiffen* when heated while
  steel softens. That is a measurable test of which mechanism a tissue uses.
- relate to Module 6 by paying a debt it actually leaves open — *why* a straightened
  fibril is nearly linear (`module06.html:151` asserts it) — and by supplying the
  molecular basis of the elastin in Module 6 §8's ligaments and fascia. Not the toe.

Numbers to reuse: `probe4.py`. Collagen `ℓ_p ≈ 14.5 nm` and contour length `≈ 300 nm`
for tropocollagen are the §4/§7 shared inputs; **put them in one JSON both sections
read**, per the plan's own warning about two sections quoting different values.
<!-- SEC3-HANDOFF -->

<!-- SEC4-HANDOFF -->
### Phase B step 1 — Module 0 §4: DONE (`151a8f2`, `53cec80`)

§4 ("entropic elasticity: the chain, and what it can and cannot stiffen") is complete
and live. It builds the machinery §0 and §2 pointed at, then **withdraws the claim they
made**, which is the most useful thing it does.

Contents: **Definition 4.1** (chain, Kuhn segment, contour length, ideal chain);
**Proposition 4.1**, the split of tension into energetic and entropic parts with the
boxed `f = −T ∂S/∂x` for an ideal chain, proved from the fixed-volume counterpart of §3
Prop 3.1; **Lemma 4.1** (random-walk statistics, `⟨R²⟩ = Nb²`, Gaussian by CLT);
**Proposition 4.2** (an ideal chain is Hookean, `k = 3k_BT/Nb²`); **Definition 4.3**
(persistence length); the **Marko–Siggia interpolation**, boxed but deliberately *not*
proved because no closed form exists — the text says so and flags it as a different
status from every other box in the module; **Proposition 4.3** (`E = 3nk_BT`, proved by
affine averaging with `ν = ½`, noting §2 derived `ν = ¼` for a central-force crystal).
Three figures (12–14). All thirteen gates green.

**Numbers, Python-verified in `nums4.py` + `ceiling4.py` with assertions:**
- one tropocollagen chain: `N = 10.3` Kuhn segments of `29 nm`, coil size `93 nm`,
  entropic spring constant **1.48 µN/m** — softer than §2's Ca–O bond (`467 N/m`) by
  **3.2×10⁸**. That ratio alone should have warned §2 off.
- **the forward prediction:** natural rubber `1.47` vs `1.5 MPa` measured (**0.98×**),
  elastin `1.55` vs `1.1 MPa` (**1.41×**), from crosslink chemistry with no elastic
  datum among the inputs. §4's counterpart to §2's apatite result.
- **collagen fails.** Inverting `E = 3nk_BT` at `1.07 GPa` demands
  `M_c = 10.1 g/mol` — a crosslink every *tenth* of an amino-acid residue, and a chain
  spacing of `0.23 nm`, which is §2's bond length. Incoherent, not merely unmet.
- **the corrected margins** (see the lesson below): `1.67 MPa` at a real protein's
  crosslink spacing → **642× short**; `108 MPa` with a crosslink at *every* residue,
  the absolute physical limit → **9.9× short**.
- the discriminator: entropic stiffness `∝ T` gives **+5.8%** from 20 to 37 °C while
  steel loses **0.51%**. Opposite signs, so it is a real measurement, not a calibration.

**§0 and §2 were corrected in six anchored edits.** Both had asserted collagen's
compliance is entropic and deferred the arithmetic to §4. Withdrawn. The honest account
is a three-step **energetic** ladder — bond count `50 GPa`, helix bending and unwinding
to `≈6 GPa`, interfibrillar shear to `≈1 GPa` — and entropy enters collagen only in the
**telopeptides**, at the very foot of the toe. `E_collagen` stays `measured`, for a
better reason than before.

**§4 does NOT claim Module 6's toe region**, which the plan told it to. Module 6 already
derives the toe from crimp and fibre recruitment with a proof, and explicitly denies it
is molecular. What §4 supplies is the **licence** for that derivation: Prop 4.2 shows
that had the compliance been entropic, a straightened fibril would not be linear and
Module 6's population argument would double-count.

`check_provenance` gained two more `[pre]` names: `E_elastin`, `lp_collagen`. The
`lp_collagen` marker discloses that the persistence length is itself fitted with the
very model §4 uses, and that `14.5 nm` is the choice *most favourable* to the entropic
hypothesis — which still fails.

**Lessons from this section.**
1. **The number that gets you is the one you assert while computing something
   adjacent.** §4's first version said an entropic network "cannot exceed a few
   megapascals at any physically possible crosslink spacing" and quoted `973×`. Both
   wrong: `973` was collagen against elastin's *measured* modulus (a different
   comparison), and the ceiling is `108 MPa`, not a few. I had looked at elastin and
   rubber — real proteins — and never asked what the formula does at its own limit.
   Caught by checking my own arithmetic before the reviewer did; corrected in five
   places, because the wrong number had already propagated into §0 and §2.
2. **Unicode has no subscript B either.** Fig. 13's y-axis rendered `3nk₈T` because the
   subscript table substituted subscript 8. Identical class to §3's `R_sT`. Every gate
   passed; only rendering caught it. **Any subscript that is not a digit or one of
   `ₐₑₒₓₕₖₗₘₙₚₛₜᵢᵣ` needs a `<tspan baseline-shift="sub">`.**
3. **An anchor that wraps a line break will not match.** Two appliers failed on
   `module00.html` because my literal had a space where the file had `\n`. Use a regex
   with `\s+`, or grep the exact bytes first.
4. `check_frame` caught the Fig. 12 force arrow clipped 2 px past the viewBox;
   `check_overlap` caught four labels on curves, **two of which named the very curve
   they sat on**.

**Symbol namespace fixed by §4** (Module 0's Appendix must register these): `b` Kuhn
length (against §2's Born constant `B`); `L_c` contour length; `ℓ_p` persistence length;
`x` extension; `f` single-chain tension (lower case, against Module 1's whole-body `F`);
`n`/`n_ch` chains per unit volume (against §2's Born exponent and §1's amount of
substance); `M_c` molar mass between crosslinks; `κ` bending rigidity; `Ω` configuration
count; `ξ` reaction extent (bound in §3, reused here); `ν = ½` for an incompressible
network, against §2's `ν = ¼`.

**A `rigor-reviewer` pass ran (`rev4`) and returned NEEDS-FIXES; findings 1&#8211;5 are
applied (`138dfe7`).** It recomputed every headline number by hand and all matched, and
decoded every polyline in Figs 12&#8211;14 against the model. The failures were
arguments, not arithmetic. Three were serious:

1. **"No entropic network reaches a gigapascal" was stated universally**, but Prop 4.3
   proves it only for **Gaussian** networks. A semiflexible network crosslinked *inside*
   its persistence length scales as `κ²/(k_BT ξ² ℓ_c³)` (MacKintosh, Käs & Janmey 1995)
   and is not bounded by `3nk_BT`. Every claim is now scoped, and the route closed
   twice: collagen has `ℓ_c ≈ 150–300 nm` against `ℓ_p = 14.5 nm`, so it *is* flexible;
   and the semiflexible modulus has `k_BT` in the **denominator**, so such a network
   *softens* on warming and §4's own Fig. 14 discriminator would not read it as
   entropic. **This is the question this handoff told a fresh session to ask, and the
   answer is that the conclusion survives but the statement did not.**
2. **My own correction introduced a second error.** The boxed `E_max = 108 MPa` sat at
   `M_c = 100 g/mol` — shorter than one Kuhn segment, outside the `N ≫ 1` hypothesis
   Prop 4.3 needs, as §4 admitted one sentence later. Boxing it gave result typography
   to a number the theorem does not produce. Demoted to prose; the box now holds the
   **Gaussian-valid** ceiling, `M_c ≈ 3–5 kDa → 2.2–3.6 MPa`, i.e. **300–500× short**,
   with **642×** at elastin's real spacing as the honest headline (`ceiling4b.py`).
3. **A real error in Prop 4.2's proof.** It wrote `Ω(x) ∝ P(R)` while `x = |R|`.
   Constraining the *magnitude* brings a `4πx²` Jacobian and a spurious `−2k_BT/x`
   term. Restated: the constraint fixes the end-to-end **vector**, which is what an
   apparatus holds, so the Jacobian is absent.

Plus two pieces of **residue** from §4's own withdrawal — §2 still said "the restoring
force here is entropic", and §3's closing still sent §4 after Module 6's toe. Both
corrected; residue sweep for all five withdrawn phrasings is zero.

> **Findings 6 onward were truncated in delivery and are NOT applied.** The remainder
> was requested from `rev4` by `SendMessage`. Finding 6 began "[self-containment] mod…".
> **Ask `rev4` for the rest** (or re-run a reviewer on §4 scoped to self-containment and
> prose only) before treating §4 as closed.
<!-- SEC4-HANDOFF -->

### Phase B step 1 remainder onward — NOT STARTED

Module 0 §5–§9 and its Appendix are unwritten; no chemistry prose exists in
Modules 1–17 yet. **Five of ten sections done.**

---

## Next task

**First: check whether `rev4`'s findings were applied.** Look for a commit titled
"Module 0 §4: apply the rigor-reviewer findings". If there is none, the reviewer pass on
§4 never landed — re-run `rigor-reviewer` on the `<!-- SEC4 -->` block before anything
else, and put the question about **semiflexible networks** to it explicitly (a taut
semiflexible network can be far stiffer than `3nk_BT`; if that route reaches a
gigapascal, §4's refutation must be narrowed to Gaussian networks rather than to
entropic elasticity in general).

**Then build `module00.html` §5** — water, ions, and the electric double layer:
dielectric screening, the Debye length, pH, pKa and buffering. Content spec is
`chemistry-audit-and-plan.md` §2.3.

§5 is the most heavily *pre-sold* section in the module. Four sections have already
promised it something, and each promise is a debt with a named creditor:

1. **§3** dropped the electrical work term at the reticulum membrane, justifying it by
   the SR membrane's near-zero potential, and said explicitly that this "would be false
   at the cell surface". §5 owes the electrochemical potential and the Nernst equation.
2. **§4** quoted a persistence length without saying what sets it, and closed by saying
   that for a charged biopolymer much of the bending rigidity is electrostatic
   self-repulsion which collapses when salt screens it. §5 owes that screening —
   and note this is a *quantitative* debt: if screening changes `ℓ_p` by a large factor,
   §4's tropocollagen numbers move.
3. **§3** Definition 3.4 used **ionic strength** `I = ½Σc_iz_i²` and glossed it as
   "§5's subject". §5 owes the real treatment.
4. **Module 4 §2**'s Donnan swelling pressure and **Module 5 §3**'s membrane potential
   are the downstream customers named in Module 0's own roadmap table.

Four standing constraints:

1. **Rigor parity binds.** §4 boxed five results, proved three, and marked the
   Marko–Siggia interpolation as explicitly unproved with a reason. §5's candidates
   (Debye–Hückel screening, the Nernst equation, Henderson–Hasselbalch, the Donnan
   condition) are all derivable — so derive them, or say in the box why not.
2. **Ask where every table value came from.** Three sections running have caught a
   parameter that arrived looking derived and was fitted: §2's Born exponent (alkali-
   halide compressibilities), §3's `ΔG°′` (a fitted equilibrium model), §4's persistence
   length (fitted with the very model that consumes it). Dielectric constants, pKa
   values and activity coefficients all carry the same question.
3. **Do not assert a limit you have not computed.** This is §4's lesson and it cost a
   correction commit. Any sentence of the form "cannot exceed" or "at most" must have a
   line in the verification script behind it.
4. When §5 lands, flip its TOC entry from `<span class="pending">` to a link, update the
   "§0–§4 are complete" note below the TOC, re-run `autolink_sections.py` (27 forward
   `§N` refs still unlinked) and `rm` the `.bak`.

Then §6 → §7 → §8 → §9 → Appendix, and only then the traces into the existing modules,
in order (`chemistry-audit-and-plan.md` §2.2b and Part 3): Module 5 → Module 2 →
Module 6 → Module 4 → Module 14 → Modules 8/9 → Modules 15/16/17.

**Scope, stated plainly.** Module 0 at full course standard is ten sections plus an
Appendix, with §9 alone carrying 30 problems, 5 diagnostics and Python-verified
solutions — roughly the size of §0–§4 put together. **Five of ten sections are done.**
This is **many sessions**, not one. Work in order, commit each section without being
asked, refresh this file at every section boundary, and do not let a session grow past
~150k context — the session that built §3 and §4 ran to over 400k and that is the most
expensive habit in this project's history.

If the user asks for something else, that takes precedence.

---

## Lessons that bind this phase

**The nine gates do not see wrong content, only broken content.** Every gate was
green on a caption describing an axis the figure did not have (m06), a curve plotting
`L·p` on an axis labelled "peak stress" (m14), and a grip curve drawn at 1.3× the
true load (m11).

- **Decode `<polyline>` point strings back into data** and compare against the model.
  **Calibrate from the axis `<line>` elements, not the tick `<text>` baselines** — m04
  found those baselines sit 3 px low, and that offset alone shifts a recovered peak
  pressure by 0.065 MPa, manufacturing a discrepancy that is not there.
- **Render at least once.** `check_overlap` tests text against curves and dashed
  lines, never text against text. m15 found a label sitting on another label and an
  optimal curve hidden under the truth curve — invisible to every gate.
- **Run the code before reading the prose.** m14's ten K problems carried no code
  while the module claimed three times that every number was produced by running it.
- **Grep for residue after every apply.** Every module that looked found some.
- **Prove an apply, don't read it.** Re-run the script from pristine and confirm the
  output is byte-identical.

**`check_links.py` passes on a *renumbered* section** — the links still resolve, they
just point at the wrong section. M4 carries 250 in-prose `§N` references, M5 248, M6
208. **Never renumber an existing section**; add chemistry as a subsection, which
shifts no integer. Green gates, wrong book is the worst defect class this repo can
produce.

**Write the gate before the prose, and believe the gate over the plan.** §2.2 words
the rule as "every *boxed* constitutive parameter". Restricted to boxes, the first
run found 91 assignments in 5.6 MB and **missed `E ≈ 17 GPa` entirely** — it sits
inside Definition 1.3 at `module02.html:171`, and `c_F` first appears in a table. The
course states its parameters in prose and consumes them in boxes. Scope widened to
the whole body: 494 assignments. A plausible definition, written in good faith from
the plan's own wording, was wrong, and only running it showed that.

---

## Where to read things (reference, don't re-derive)

- `CLAUDE.md` — standing conventions: build loop, the hardening gates, git/publish.
- `chemistry-audit-and-plan.md` — Phase B audit, plan, **§2.2c the provenance
  contract**, §2.2b the threading map, Part 3 the build order.
- `provenance-baseline.txt` — the measured worklist (regenerate, never hand-edit).
- `prompt.txt` — original course spec. Line 211 the Required Biological/Chemical
  Spine; line 285 the Modeling Levels ladder.
- `EDITOR_DOMAIN.md` — the domain brief the `science-editor` skill loads.
  (`EDITOR_PROMPT.md` describes a *different* manuscript — ignore its `# Domain:`.)
- `editor-reports/moduleNN.md` — per-module editor reports with change tables.
- `moduleNN-plan.md` — per-module build plans for modules 4–10.

---

## Lives outside this repo (no version control — a real risk)

`C:\Users\simon\.claude\skills\rigorous-explainer\` holds all thirteen gate scripts
and `assets/template.html`. **That directory is not a git repository.**
`check_provenance.py` (~300 lines) and the `.prov` style in the template were written
2026-09-09 and exist in exactly one copy. **Two more single-copy edits landed at the §3
boundary:** `check_provenance.py` gained the `dG0_ATP` / `c_metab` chemistry names, and
`autolink_sections.py` gained the cross-module guard that stops it producing wrong-book
links. That guard is the one piece of this directory whose loss would silently
reintroduce the worst defect class in the repo, so it is the thing most worth backing
up. `provenance-baseline.txt` in this repo is
its *output*, not the tool. Worth backing up; not done, because the other twelve
gates live the same way and changing that convention was not asked for.

## Session-transient scratch (regenerate; durable record is the committed output)

- **`scratchpad/tools/BRIEF.md`** — the 117-line agent brief that drove the editor
  pass. Ten steps: load `science-editor` + `EDITOR_DOMAIN.md` + a format-model
  report; never touch the original; record the gate baseline on a pristine copy
  first, end rule *zero where the baseline was zero, never worse anywhere*; run the
  code before reading the prose; one re-runnable `apply.py` with `rep()` asserting
  each anchor is unique; author math only via Write/Edit or a Python raw string.
  **Worth promoting into the repo rather than rebuilding again.**
- `scratchpad/tools/extract.py` (every `<pre><code>` block out to a runnable `.py`),
  `txt.py` (dump a line range with `<svg>` collapsed, UTF-8, never truncated),
  `apply_skel.py`.
- **Module 0 §2 scratch (regenerate from the pattern; the durable record is
  `module00.html`):** `nums2.py` (verifies every §2 number forward — pair stiffness,
  the three rocksalt controls by both routes, apatite, the `α_M/12` decomposition and
  the five bond rungs in `k_BT`; writes `nums2.json`), `gen2.py` (Figs. 5–8, writes
  `svg2.json`), `sec2.html` (the §2 prose fragment), `assemble2.py` (splices fragment
  plus figures between `<!-- SEC2 -->` markers — idempotent), `fix2.py` (the 31
  reviewer edits, every anchor asserted unique before any write), `txt.py` (dump a line
  range with `<svg>` collapsed).
  - **Figure lessons worth reusing.** A predicted-vs-measured panel must be kept
    **square** (equal pixels per decade on both axes) or its 45° reference lines are
    not 45°, and a "perpendicular" label offset silently lands on a line. A descent
    ladder should use **evenly spaced rows with bar lengths ∝ log E** (152 px/decade
    from a 10 GPa base), not a true log axis — 143, 114 and 104 GPa are unreadable on
    one. Put curve identities in a **legend**, not inline, whenever two curves converge
    (the Born attraction and the sum coincide beyond 0.35 nm). And stop an asymptotic
    curve before it runs along an axis line, or it will strike through legend text.
  - **Two authoring traps hit this session, both already in memory:** `\'` inside a
    Python raw string keeps the backslash, so an anchor containing an apostrophe needs
    `"""…"""` quoting; and `module00.html` spells the section sign as a literal `§` and
    its dashes as `&ndash;`/`&#8212;` inconsistently, so an anchor written with
    `&#167;` matches nothing. Grep the exact bytes before writing an anchor.
- **Module 0 §1 scratch (regenerate from `gen1.py`'s pattern if needed):**
  `nums1.py` (verifies every §1 number at 310.15 K), `gen1.py` (the three §1
  figures — a `txt`/`sub` helper, a vertical-ladder idiom shared by Figs. 2 and 3
  with a greedy label-stacking rule that guarantees a 19 px gap, and the Fig. 4
  log-log noise plot; splices between the `<!-- FIGN -->` markers, idempotent),
  `fix1.py` (the 36 reviewer edits, anchor-checked before writing — its `variants()`
  helper matches an anchor whether the file spells a dash `&#8212;` or `—`),
  `handoff1.py`. The durable record is `module00.html`.
- The Phase B step 0 scratch (`sec22c.md`, `amend22c.md`, `splice22c.py`,
  `gateall.sh`) is spent — its output is committed in
  `chemistry-audit-and-plan.md` and `provenance-baseline.txt`. Nothing to regenerate.

## How to work (essentials — full detail in `CLAUDE.md`)

- **Section by section.** Build one section → report with a short summary and two
  `★ Insight` bullets → user reviews → commit and push. Standing rule: after each
  module or work unit, commit and push without waiting to be asked.
- **Run the full hardening loop after every edit pass** — every script in the
  `CLAUDE.md` block, now including `check_provenance.py`, plus a `rigor-reviewer`
  pass.
- **Never author math-bearing HTML inside a double-quoted shell argument.** The shell
  eats `$…$` and turns `\t` into a TAB. Use Write/Edit, or splice from a file using a
  Python raw string. The same applies to large markdown with `§`, backticks and
  em-dashes, and to regexes full of backslashes — a bash heredoc mangles those too.
  Write the file with the Write tool, then splice by path.
- **Prose lives in `moduleNN.html`; Python builds figures only.** Never author
  section prose inside a Python raw string — it evades the read-aloud audit.
