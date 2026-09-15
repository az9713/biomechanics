# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last written:** 2026-09-14 (twelfth refresh — **Phase B step 2: Modules 5, 2 DONE;
Module 6 reviewed, fixed and COMMITTED (`04825e8`); three Sonnet agents in flight for
Modules 4, 14, 8/9; Modules 15, 16, 17 queued as wave 2**; see "Module 6 — reviewed"
and "Agents in flight" below). Latest content commit `04825e8`.
A two-minute overview of this file lives at `HANDOFF.html` (repo root, also live at
https://az9713.github.io/biomechanics/HANDOFF.html). This file stays the source of truth.

Phase A (editor pass) is **complete and promoted**. Phase B (chemistry and biology
interweaving) has its **gate and worklist built**, and **Module 0 is COMPLETE** — ten sections plus an
appendix, all live, all thirteen gates green. Start at "Next task".

**Open item 1 below (the `rev5` findings) is CLOSED** — applied at `8846725`, with the
fourth autolink defect fixed at the root at `f9a903f`. Two items remain open: the missing
reviewer passes on Module 0 §6–§9 and the Appendix, then Phase B step 2 — the traces into
Modules 5, 2, 6, 4, 14, 8/9 and 15/16/17. The §0 reviewer's note about registering bond
stiffness is also closed: the Appendix notation table carries
`$k_{\text{pair}}$, $k_{\text{bond}}$` with its collision note (verified 2026-09-10).

## Decisions of 2026-09-13 (the user answered; do not re-ask)

1. **Step 2 session cut: continue across module boundaries.** Build Module 5, then
   Module 2, then Module 6, and so on, in one session as far as context allows.
   Still refresh this file at every module boundary. The session that recorded these
   decisions was already at ~151k context before any trace was written, so it
   handed off here instead of starting Module 5 at 3× cost per turn.
2. **Gate scripts: synced** (`387508f`). The tracked copies of `check_provenance.py`,
   `autolink_sections.py` and `checktex.py` now match the live ones. Item 2 below is
   closed.
3. **Module 0 §6–§9 + Appendix reviewer pass: deferred.** Go straight to the traces.
   If a trace exposes an error in a cited Module 0 section, fix it then. The pass
   stays an open item (see "Next task").
4. **New problems: yes, append as K11+.** The three the plan names — fit `k_on`/`k_off`
   from a measured twitch (Module 5), the AGE crossover sweep (Module 14), the
   ATP-supply power–duration model (Module 8/9) — go after the existing K10 with a
   figure, a Probes note and a Python-verified solution. No existing number changes.
5. **Git-history rewrite (item 1 below): not decided, not needed for step 2.** Do not
   raise it again unless the user does.

**Two decisions were raised 2026-09-10.** Item 2 is closed above; item 1 stays open.

1. **Rewrite git history to remove personal info?** The tracked files are clean at
   `ec3e0d2` (`git grep -Iic simon` returns nothing, and no email address was ever in a
   tracked file). The history is not: **209 commits** carry the author or committer
   email `az9713@yahoo.com`, and **253 commit messages** carry a
   `claude.ai/code/session_…` URL. Removing them needs `git filter-repo` and a force
   push over `main`. That changes every commit hash, so every cited hash must be
   remapped — distinct hashes cited per file: 28 in this file, 13 in
   `DEVELOPMENT_JOURNEY.md`, 6 in `HANDOFF.html`, 3 each in `CLAUDE.md`, `AGENTS.md` and
   `CODEX_HANDOFF_REPORT.md`, 2 each in `DEVELOPMENT_JOURNEY_2.md` and
   `DEVELOPMENT_JOURNEY_2.html` (`README.md` cites none). GitHub keeps old SHAs
   reachable after a force push; a full purge needs GitHub Support. **Do not rewrite
   without an explicit yes, and confirm again before the push.**
2. **Sync the three stale tracked gate scripts?** Copy `check_provenance.py`,
   `autolink_sections.py` and `checktex.py` from the live skill directory over
   `.claude/skills/rigorous-explainer/scripts/`. Three file copies. Detail in "The
   tracked gate scripts are stale" below.

Commits after `ec3e0d2` use `az9713@users.noreply.github.com` — now the `CLAUDE.md`
convention — so they add nothing to the **email** half of item 1. They still end
with the `Claude-Session:` trailer the environment requires, so the **session-URL**
half grows by one per commit (254 at `8bbebd3`, this refresh not counted). Dropping the
trailer is the user's call.

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

> **Findings 6 onward were also delivered and applied (`258ba22`).** §4's reviewer
> pass is CLOSED. That commit fixed a live TOC bug (§4's entry was still
> `<span class="pending">`), four wrong arguments, two figure defects found by
> decoding polylines, four literature over-confidences, five more pieces of
> withdrawn-claim residue, and the namespace collisions on G, W, R and N.
<!-- SEC4-HANDOFF -->

<!-- M0-HANDOFF -->
### Phase B step 1 — Module 0: **COMPLETE** (`4403e98`)

Ten sections plus an appendix, all live at
https://az9713.github.io/biomechanics/module00.html. **Zero pending TOC entries**,
no *(in progress)* marker in `index.html`, all thirteen gates green: 2989 math
segments 0 issues; 500 internal links 0 broken; 126 parameter assignments with 14
provenance declarations and 0 issues; 0 label overlaps; 0 clipped or wasteful
figures; 0 `mjx-merror`; 2 code blocks PEP8 clean.

| § | subject | key commits |
|---|---|---|
| §0 | motivation | `d985962` `54bd525` `b849a77` |
| §1 | the mole and the `k_BT` ruler | `0346f4f` `72b5b16` |
| §2 | bonding and the stiffness ladder | `c6d8e44` `59a19c0` |
| §3 | thermodynamics | `455ca86` `e64b6ad` |
| §4 | entropic elasticity | `151a8f2` `53cec80` `138dfe7` `258ba22` |
| §5 | water, ions, the double layer | `8d1a66f` |
| §6 | kinetics | `76c9e82` |
| §7 | the macromolecules | `59d8859` |
| §8 | computational lab | `0f56c9a` |
| §9 | limits, diagnostics, 30 problems | `7a205a8` `4403e98` |
| Appendix | notation, constants, parameters | `0eee81c` |

**What the module delivers.** Every constant Modules 1–17 borrow is now either
traced to chemistry or marked measured with a reason. Derived forwards, with no
elastic datum among the inputs: apatite's modulus (§2, 143 GPa against 114
measured), elastin's modulus (§4, bracketing the measurement at 1.55 dry / 0.77
hydrated against 1.1), collagen's contour length (§7, 1014 residues × 0.286 nm +
10 nm of telopeptide = 300 nm), cartilage's fixed charge (§7, from a GAG assay
through a stoichiometry), and both calcium pumps' stoichiometry ceilings (§3 and
§5 — two per ATP into the reticulum, one out through the cell surface, and both
are what is observed).

**Four errors the module found in itself, all four the same class.** Each was
well-formed, internally consistent, passed every automated gate, and was wrong.
1. §0's stiffness ladder was **circular** — its `k` column had been calibrated from
   the moduli it claimed to predict. Caught by asking where a table value came from.
2. §0 and §2 attributed collagen's compliance to **entropy**. It is short by 642× at
   any real crosslink spacing. Caught by computing an attribution that had only been
   asserted. Withdrawn in six anchored edits.
3. §4's own **correction** was then wrong too: it boxed a 108 MPa ceiling evaluated
   at a crosslink spacing shorter than one Kuhn segment, outside the hypothesis of
   the proposition it was using. Caught by a reviewer asking whether a boxed number
   is one the theorem produces.
4. §9 K2 said "half the drop happens in the first 12 s". Drawing it put the marker
   at **16 s**. Caught by rendering the figure.

§9 makes the pattern its closing lesson: **the claim that fails is not the one you
compute, it is the one you assert while computing something adjacent.**

**Three script bugs fixed at the root** (all outside git — see the risk note below):
- `autolink_sections.py` linked `§N` inside `<pre>` blocks, rewriting "Section 6" in
  a Python docstring into an `<a>` and corrupting code a reader is told to run. Now
  excludes `<pre>`. A sweep of all 18 modules confirms only `module00` was hit.
- the same script linked cross-module refs to local anchors: "Module 4 §2" pointed
  at Module 0's own §2, and `check_links` passed because the anchor resolved. Now
  refuses a `§N` preceded by `Module <k>` and reports how many it skipped.
- `check_provenance.py` gained eight `[pre]` chemistry names (`dG0_ATP`, `c_metab`,
  `E_elastin`, `lp_collagen`, `eps_r_water`, `k_on` family, `Q10` family,
  `L_collagen`, `v_max`); its `GATED` table had been built from the pre-chemistry
  modules and contained no chemistry parameter at all.

**Reviewer coverage — INCOMPLETE, and this is the module's one real gap.** §0–§4
each had a `rigor-reviewer` pass and each returned NEEDS-FIXES with real findings
applied. **§5's pass (`rev5`) was dispatched and never applied; §6, §7, §8, §9 and
the Appendix had no pass at all.** See "Next task".

**Two figure lessons worth carrying.**
- **Unicode has no subscript `g` or `B`**, and a lookup table substitutes a wrong
  letter silently: Fig. 9 rendered `R_sT` and Fig. 13 `3nk₈T`, both past all
  thirteen gates. Any non-digit subscript needs a `<tspan baseline-shift="sub">`.
- `check_overlap` beat the eye every single time it was run — 4–0 on §3, 4–0 on §4,
  4–0 on §5, 3–0 on §6, 10–0 on §7, 3 passes on one §9 bell curve whose "inside"
  turned out to be on the curve at two separate places. **Never eyeball a preview
  for overlaps.**

**Session-transient scratch** (regenerate from the pattern; the durable record is
`module00.html`): `nums0-7.py` and `lab9.py` (every number, with assertions),
`lab8a.py`/`lab8b.py` (the §8 labs, spliced verbatim into the page so the code shown
is the code that ran), `gen3-9fig.py` (figures; `gen3.py` holds the shared helpers
`txt/line/poly/dot/rect/svg/num/sb/sci` that every later generator imports),
`assemble3-9.py` and `assembleA.py` (idempotent splicers), and the `fix*.py`
appliers. **Two applier lessons:** generate an applier by hand, not by
string-replacing the previous one — `assemble4.py`'s TOC substitution silently
failed that way and shipped a live bug; and write appliers with the Write tool, not
a heredoc, because the shell turned `\b` into a literal backspace and `\text` into a
tab more than once.
<!-- M0-HANDOFF -->
---

## Next task

**Module 0 is COMPLETE** (`4403e98`). Ten sections plus an appendix, zero pending
TOC entries, no *(in progress)* marker in `index.html`, all thirteen gates green.
Phase B step 1 is closed.

**Before anything else — two open items from Module 0.**

1. **`rev5`'s findings on §5 are APPLIED** (`8846725`, 45 fixes) — and the pass was
   worth it. The worst finding was a **third false debt**: §5 claimed Module 4 §2
   "takes a swelling pressure as given" when Module 4 already proves it with a boxed
   `.thm` and two `.proof` divs, reaching the same expression in different notation.
   Ten more statements were simply wrong (the buffer half-width, the permittivity
   sign, "eight times more dilute", the pH window and its false comparison with
   sodium, 898 k_BT attributed to a section that never states it, a promised table
   that did not exist, a Module 5 anchor pointing at the wrong section). Prop 5.1's
   prefactor, van 't Hoff, and Def 5.4's formula all needed their status corrected,
   and OSF turned out to be used **outside its own validity condition** (λ_D ≫ A
   fails at plasma strength; it survives only because discreteness makes it an upper
   bound). Fig 16 had a line invisible under another line — a defect no gate can see,
   because `check_overlap` tests text against lines and never line against line.

   **A fourth autolink defect came out of the same review** (`f9a903f`): the script
   was rewriting section refs inside `<svg>`, and a sweep found **23 injected anchors
   across three modules** — 8 in module00 from this session, but **14 in module04 and
   1 in module17 from earlier sessions**, carried in live figures with every gate
   passing. Root cause fixed (`<svg>` excluded alongside `<a>` and `<pre>`) and all
   23 cleaned. That is three containers the script should never have edited; the
   lesson recorded in the commit is that a rewrite pass needs an **allowlist** of
   where it may act, not a growing denylist.

2. **§6–§9 and the Appendix have had no reviewer pass at all.** Four sections and an
   appendix went in without one, which is a departure from the standing convention
   and the reason it exists. §9 in particular carries 30 problem solutions whose
   arguments nobody has checked; its numbers are verified (`lab9.py`, all assertions
   passing) but "the arithmetic is right" is exactly the assurance that failed three
   times in this module.

<!-- M5-TRACE -->
### Phase B step 2 — Module 5: DONE (`3703a91`; second reviewer pass `8c64e58`, 20 more findings applied — two reviewers ran because the first one's report truncated)

Four traces plus K11, live at https://az9713.github.io/biomechanics/module05.html.
Every trace is a new `<h3>` at the point of first use; nothing renumbered. All
thirteen gates green; `check_provenance` 73 assignments, 7 declarations, 0 issues.
A `rigor-reviewer` pass returned NEEDS-FIXES with **24 findings, all applied** (the
worst: a false `module0` state on the `Q10` marker — Module 0 measures the `Q10` and
derives `E_a` from it; an unbridged −90 mV in the pump ledger four lines after the
lemma returned −86; five symbol collisions `u`, `V`, `s`, `c`, `P` against the module's
own drive, volume, occupancy, curvature and power).

| trace | what it proves or computes | provenance |
|---|---|---|
| §2 *What one stroke costs* | one ATP = 24.2 / 20.4 k_BT (rest / fatigued, Module 0 §3); stroke work 11.7 k_BT at 5 pN; η_xb = 0.48 / 0.57; muscle bound 0.29–0.34 after a measured pump share 0.30–0.40; **Lemma 2.1** σ = χ n_fil N_half φ_att f_head = 11–18 N/cm² against the measured 30 | `F_max` measured (its inputs are inferred from the same fibres) |
| §3 *Where the voltage comes from* | Nernst table from Module 0 §5; **Lemma 3.1** GHK with a constant-field proof; rest −86 mV and spike +42 mV from P_Na/P_K = 0.02 and 20 (assumed), P_Cl/P_K = 2; Na/K pump 46.3 kJ/mol per ATP via Module 0 Prop 3.5, 3 Na is the ceiling in working muscle (4 Na costs 61.4, forbidden fatigued by 8.7); one impulse costs 1.8 µM ATP, under 2% of a crossbridge cycle across the fibre | `tau_relax` measured (τ_r, τ_d: what would derive them is RyR gating and a SERCA Michaelis–Menten rate) |
| §5 *Where the two time constants come from* | **Proposition 5.1** τ(Ca) = τ_deact/(1+(Ca/Ca50)^n); τ_act = 40/(1+1.4³) = 10.7 ms from no new input; consistency with Module 0's per-site k_on = 10⁸ M⁻¹s⁻¹ (10 ms at Ca50) | `tau_act` derived; `tau_deact`, `k_on` measured |
| §6 *Why a cold muscle is slow* | **Proposition 6.2** v_max(T) Arrhenius-scaled; 8 → 2.68 ℓ₀/s at 25 °C; force at 0.8 ℓ₀/s halves (0.64 → 0.32 F₀); peak power ×0.335; k_cyc ≈ 1080 s⁻¹ inferred, reconciled with Module 0's 10 s⁻¹ turnover | `Q10`, `v_max` measured |
| K11 | kinetic twitch inverse fit: pure binding kinetics cannot reach (25, 40 ms); with one downstream lag two branches fit — A: k_off 22.3 s⁻¹ + τ_x 4.6 ms, peak 0.39; B: instant binding + τ_x 43.7 ms (K10's model), peak 0.215 — non-identifiable on timing; the twitch/tetanus ratio (0.29 vs 0.53 of 0.73) picks B, conditioned on the frozen Ca50 | — |

**Findings worth carrying.** (1) The plan's "21.3 k_BT, ~55%" was 55 kJ/mol; Module 0's
measured compositions give 62.5 → 48%. Module 0 wins over the plan. (2) Two Hill-type
"rates" a hundredfold apart described the same cycle in two modules (1080 s⁻¹
detachment step vs 10 s⁻¹ per-head turnover); both are right and the reconciliation
sentence now sits in §6. (3) The reviewer's report **truncated after 5 of 24
findings** in the idle notification; the rest came only after a request for batches of
≤5 with a DONE marker (memory `reviewer-results-truncate`). (4) Figures added to a
module that cites figures by number must be **uncounted `<div>`s** (now in `CLAUDE.md`).

Scratch (session-transient; durable record is `module05.html`): `nums5.py` (every
number, assertions) → `nums5.json`; `gen5.py` (a `P` plot helper + five figures) →
`svg5.json`; `splice5.py` (idempotent marker splice); `k11.py` (the K11 listing,
PEP8, run to produce the quoted output).
<!-- /M5-TRACE -->

<!-- M2-TRACE -->
### Phase B step 2 — Module 2: DONE (`c42bf3a`, follow-up `0a6caeb`)

Two traces into `module02.html`, plus nine provenance markers, the `.prov` CSS, two
uncounted figures, and Appendix rows. All gates green (`check_provenance` 0 issues;
`check_overlap` 0). A `rigor-reviewer` pass returned NEEDS-FIXES with **17 findings,
all applied**. The worst three: a dimensional slip inside the boxed bound (`F_max/Z`
where the left side was already a fractional rate); the K4 caveat I wrote was itself
wrong (with a physiological gain `Z` is frozen on K4's timescale and the damage settles
toward 0.25·1.6⁶ = 4.2 at any ramp rate — K4's critical rate is an artefact of the toy
`k`, not "set by repair alone"); and three symbol collisions inside one proposition
(`n` safety factor, `δ = Z − Z_eq`, `g` gravity) plus `F_max`/`R_max` reading as a force
and a radius. **Symbols now used in §7's Proposition 7.3:** `Φ_F`, `Φ_R` (max fluxes),
`n_H` (Hill coefficient), `ξ` (departure level, 0.05), `q = ((1−ξ)/ξ)^{1/n_H}`. The
"1.5–3 years" and "70–130×" are now stated as lower bounds. The reviewer hit its
session limit right after delivering; its report also truncated first and arrived in
full only on a batched re-request.

**Open decision for the user (unchanged):** K1, K2, K4 and K9 all rest on the toy
`k = 80`; the §7 subsection and K4's Probes line now say so. Rerunning them with a
physiological gain would change their numbers (outside decision 4). Leave or rerun?

- **§5 *The end members, derived forward*:** Module 0 §2 Prop 2.2's apatite (143 vs
  114 GPa) and §4's collagen ladder (50 → 6 → 1 GPa, measured); the Reuss–Voigt
  bracket recomputed 2.12–72.0 GPa (was 1.98–50.5); K8's η 0.33 → 0.23; Module 0
  Prop 2.1 makes E ≤ E_V a proved inequality. Markers: `E_apatite` module0,
  `E_collagen`/`E`/`G` measured (G: isotropic estimate 6.5 vs measured 3.3 — anisotropy).
  §6: `sigma_Y`/`sigma_c` measured (bond-rupture E/10 = 1.7 GPa is 13×/10× the
  measured; the gap is the flaw population).
- **§7 *Where the law's shape comes from*:** **Proposition 7.3** — net rate = F_max
  θ_F − R_max(1−θ_R) with two Hill arms gives (i) monotone with one zero, (ii) a lazy
  zone within δF_max of zero when thresholds are the δ-departure points, half-points
  at ε_lo/g and gε_hi, g = ((1−δ)/δ)^(1/n), (iii) the boxed gain bound **k ≤ (1+4δ) n
  F_max/(4 ε_hi Z)**. Numbers (δ = 0.05): n = 3 puts formation half-on at 4000 µε and
  90% at 8300, beyond the yield strain 7600 → **n ≳ 6** is required; with F_max/Z ≲
  10⁻³/day, **k ≤ 0.6–1.2 (strain·day)⁻¹, 70–130× below the module's toy 80**, so
  adaptation time constants are **1.5–3 years, not 8–12 days**. K4's "same timescale"
  premise is now caveated in its Probes line (problem left as stated). Markers:
  `k_remodel` measured (bounded), `tau_relax` (K4's τ_r) measured.
- **Open decision for the user:** K4's arithmetic is correct for its declared toy `k`
  but its physical premise is now contradicted by Proposition 7.3. Options: leave
  with the caveat (done), or rerun K4 with a physiological gain (changes its numbers —
  outside decision 4's "no existing number changes").

Scratch: `nums2.py` → `nums2.json`, `gen2.py` (imports gen5's helper) → `svg2.json`,
`splice2.py`.
<!-- /M2-TRACE -->

**The Module 5 scoping notes below are kept for the record (line numbers are those of
2026-09-13 and are stale).** `module05.html` is 1840 lines, has `<!-- SECn-START/END -->` markers for §4–§10, and
**has no `.prov` CSS rule** — copy lines 57–61 of `module00.html`'s `<style>` first,
or the markers will parse but not render. Its gate worklist (`provenance-baseline.txt`):
`F_max` (line 396, §1), `tau_relax` (834, §3), `tau_act`/`tau_deact` (978, §5),
`v_max` (1578, §10). The four traces and where each enters (line numbers of 2026-09-13):

| trace | enters at | cites in Module 0 |
|---|---|---|
| ATP ΔG vs power-stroke work; crossbridge efficiency ~55%, whole-muscle ~25% after SERCA overhead; a `.prov` for `F_max` via specific tension = heads/area × force/head × duty ratio | §2, new `<h3>` after the `active force ∝ attached crossbridges` keyresult (line 487), before "Force follows overlap" (489) | `#thermo` (ΔG at rest −62.5 / fatigued −52.7 kJ/mol; Prop 3.1 work bound; the 10.38/8.76 pN ceilings), `#mole` |
| Nernst / GHK for the action potential, Na/K pump stoichiometry and the cost of excitability; SERCA 2:1 from Prop 3.5 | §3, new `<h3>` after "From voltage to calcium" (736–747), before "Calcium unblocks the sites" (749) | `#water` Prop 5.2 (line 1036), `#thermo` Prop 3.5 (733) and the pump ledger (746–777) |
| cooperative Ca–troponin binding kinetics: `k_on`/`k_off` and the Hill coefficient **are** `tau_act`/`tau_deact`; `.prov` for both and for `tau_relax` | §5, new `<h3>` after "Why the asymmetry" (990–996), before "Activation is a low-pass filter" (998) | `#kinetics` "Cooperativity" (1208) and "Rate, mass action" (1177) |
| `v_max` from Arrhenius / `Q_10`: why a cold muscle is weaker; `.prov` for `v_max` | §6, new `<h3>` after "Why speed costs force" (1040–1046), before "Power peaks in the middle" (1048) | `#kinetics` "Temperature: Arrhenius, and the cold muscle" (1233), "Enzymes" (1267) |
| **K11** — fit `k_on`/`k_off` from the measured twitch of Modelling assumption 3.2 (inverse problem) | §10, after K10; the problem map table at line 1316 gets K11 in the §3–§5 row | — |

Prop 3.1's proof (line 796) already derives the Hill form from all-or-none binding;
trace 3 must build on it, not restate it. Every new subsection: Definition/Proposition
with `.proof`, one computed figure (Python in scratchpad → SVG body → spliced by
marker), numbers in a `nums5.py` with assertions, prov markers with the exact
`data-sym` names above. Then the full thirteen-gate loop, `autolink_sections.py`
(now with the cross-module guard), a `rigor-reviewer` pass, apply, commit, push.

**Module 6 — DONE (`04825e8`): all 18 `rev6` findings applied, all thirteen gates green,
committed and pushed 2026-09-14.** What was fixed: figure `m6cA` drew a second D-period with 4 then 3 bars crossing (one period
now); three citations pointed at sources that do not say what was claimed (Module 0 §4
for the hydroxyproline ladder, Module 2 §5 for gap-zone nucleation, "Proposition 1 at
Φ = 0" → Definition 2); the 0.02 D gap agreement pins `L_c` to 1.3 nm, sharper than
Module 0's own few-per-cent claim; tendon 20 % above fibril is the opposite of what
hierarchy predicts (said so); ligamentum-flavum composition is dry mass used as a volume
fraction, the parallel mixing rule is named, the toe-modulus test is left open; ρ, N_A,
k_BT, M_c defined and `T`-as-temperature added to the Appendix collision note; α chain
and persistence length glossed; E/10 labelled a textbook estimate this course does not
derive; three walls of words split; "slide back" → "slide past its neighbour and
dissipate the work"; §8 heading "What fills a ligament's free range"; `L_c, D` Appendix
row moved under §1; `4.478 ≈ 4.48` in the statement. Proposition 1′ label kept (reviewer:
acceptable; "1a" if ever changed). Gate advisories are pre-existing (one old figure's
margin, one bust schematic, six stray `$`).

**Module 4 — DONE (`dda8bd4`, 2026-09-15).** Agent `m04` (Sonnet) wrote the three scoped
traces (§1 `c_F` stoichiometry 0.175–0.306 M for 40–70 mg/mL; §7 viscosity Arrhenius
`E_a` 16.1 kJ/mol, gel time 6667 → 8574 s, friction −12 % vs Stribeck film +29 %; §8
Lemma 8.1 Michaelis–Menten aggrecan loss + Proposition 8.1 Donnan elasticity `Λ_π`,
156 → 42 kPa), seven markers, figure `m4cA`, Appendix rows; its own rigor-reviewer pass
returned 21 findings, all applied; thirteen gates green; the lead rendered the figure
and re-ran seven gates before committing. No missing `data-sym` names.

**Modules 8 and 9 — DONE (`c755891`, 2026-09-15).** Agent `m0809` (Sonnet): Module 9 §7
trace (Definition 4 three ATP-supply systems; **Proposition 7.2** critical-power
hyperbola; structural CP 1829 W elite / 1219 W recreational; PCr store 23.4 kJ) + K11
(inverse fit to six world records: CP 1797 W, W′ 56.8 kJ; leave-one-out pins CP
1774–1832 W, not W′ 52–78 kJ; marathon 95 % of CP, 800 m 129 %); Module 8 §7 forward
pointer (200 W walking vs ~1.2 kW ceiling). Reviewer 19 findings, 17 applied (the
agent's tail listing the 2 unapplied was truncated and re-requested; record it here
when it arrives). **Provenance gate Amendment 5 (`eac002c`)** came out of this module:
five `[pre]` names (`VO2max`, `E_O2`, `PCr_conc`, `C_gly`, `CoT_run`), `E` bound to
`E@Pa` (module09's SLIP energy `E` is not a modulus), `kappa@m^2` dropped from `k_perm`
(module08's swing-cost coefficient is not a permeability). Tracked script copy synced.

**Agents in flight — wave 1 (launched 2026-09-14 after the Module 6 commit; the user
chose `general-purpose` on **Sonnet**, at most 3 at a time): `m04`, `m14`, `m0809`.
Wave 2: `m15` launched when `m04` reported, `m16` when `m0809` reported (both Sonnet); `m17` still queued — launch it when `m14`, `m15` or `m16` reports (3-agent cap) (their prompts were
the light-addition entries of `chemistry-audit-and-plan.md` §2.2b lines ~295–297: M15
marker error model, M16 chemical-potential driving term generalising the poroelastic
law, M17 one capstone chain molecule → whole body; same guardrails, same report format).
A first launch of six Fable agents failed at once on the usage limit (resets 4:50 pm
Pacific); the only residue is the `.prov` CSS rule now in `module04.html`, kept.**
Agents survive a `/clear` and report into whichever session is live (`rev6` did exactly
that). Each edits ONLY its own `moduleNN.html` (`m0809` owns 08 and 09), runs all thirteen gates, dispatches its own `rigor-reviewer`,
applies findings, and ends with a report: files edited, each trace with key numbers,
gate results, reviewer findings applied, **canonical `data-sym` names missing from the
GATED table**, anything left undone. They were forbidden every git write command and
every shared file (`module00.html`, `index.html`, `README.md`, this file, the plan, the
baseline, the skill scripts). Scratch files are prefixed `m04_`, `m14_`, … in the
scratchpad. Do not poll them or send "are you done" messages.

**Integration steps when the reports arrive** (one pass, in this order):
1. For each reported missing `data-sym` name: add it to `check_provenance.py`'s GATED
   table as a `[pre]` entry AND record it as an amendment in
   `chemistry-audit-and-plan.md` §2.2c; then re-run `check_provenance.py` on that module.
2. Spot-check each module: render every new figure and look at it; read each new
   `.prov` marker for truth; confirm the K11 (Modules 14 and 8/9) meets the K-depth
   standard.
3. Commit **per module** with the `az9713` identity and the trailers in `CLAUDE.md`;
   push; confirm the live page.
4. Refresh this file (mark each module DONE with its hash), then `/clear`.
Known risks to give the reviewer: the label "Proposition 1′" (the module numbers
results 1–11 through the file, so a primed number was used to avoid renumbering);
the licence paragraph must not over-claim Module 0 §4 (it proves the Gaussian
entropic bound; the 50 → 6 → 1 GPa ladder is *located*, not derived); the
ligamentum-flavum three-quarters-elastin and the 0.75 × 1.1 = 0.8 MPa are stated as
composition × measured modulus, not derived; `T` (temperature) vs Lemma 1's torque `T`. Three traces: §1 *Where the
molecule's numbers come from* (Module 0 §7 → `L_collagen` module0; **Proposition 1′**
gap/overlap 0.48/0.52 D from L_c/D = 4.478 vs measured gap 0.54 D; the Module 0 §4
licence for a straight fibril being Hookean; `E`, `sigma_f` measured), §7 *two kinds of
cross-link* (qualitative; AGE kinetics deferred to Module 14), §8 *elastin predicted
forwards* (`E_elastin` module0; ligamentum flavum 0.75 × 1.1 = 0.8 MPa; +5.8 % thermal
discriminator). Scratch: `nums6.py`, `gen6.py` (generates and splices its one figure).
The original scoping notes follow. `module06.html` is 1274 lines, has
**no `.prov` CSS** (copy the rule from `module02.html`'s `<style>`), 25 `<figure>`s cited
by number 36 times (so new figures must be uncounted `<div>`s), and numbers its results
without a section prefix (Definition 1, Proposition 1 … Proposition 11, Lemma 1) — a
new result needs a new type or the next free number (Proposition 12, Lemma 2), never a
renumber. Gate worklist: `E_lin` and `sigma_f` at line 141 (Definition 1's figure/box
in §1). Traces the plan names, with what Module 0 now supplies: **§1** — the Gly-X-Y
helix, hydroxyproline, the hydrogen-bond ladder and the 67 nm D-period (Module 0 §7 Def
7.2, `L_collagen` derived 300 nm) and the *licence* for "a straightened fibril is
nearly linear" (Module 0 §4 Prop 4.2; **do not** claim the toe — Module 6 Proposition 1
already proves it from crimp, see HANDOFF "§4 — a conflict"); **§2/§7** — modulus and
hysteresis from cross-link density (enzymatic lysyl-oxidase vs glycation cross-links;
Module 0 §7 side chains); **§8** — elastin's modulus predicted forwards (Module 0 §4
Prop 4.3, `E_elastin` 1.55 MPa vs 1.1) for ligaments and fascia. Then the thirteen gates,
a reviewer pass (ask for ≤5 findings per message, DONE marker), commit, push.

**Module 4 — SCOPED 2026-09-14, nothing written into `module04.html`.** It is 2397
lines, has **no `.prov` CSS**, numbers results with a section prefix (Proposition 3.1),
and cites no figure by number (still use uncounted `<div>`s). Gate worklist
(`provenance-baseline.txt`): `mu_fric` (line 102, §0), `c_F` (336, §2), `sigma_0` (564,
§3 caption — an applied platen stress, declare *measured* as a loading choice), `E` and
`nu` (877, §6), `H_A` (1314), `k_perm` (1776). Module 4's own symbols to respect: `Θ`
is temperature, `F` is fluid load support (so never Faraday), `W` body weight, `D`
diffusivity, `k` permeability, `S` Stribeck number; write an enzyme concentration as
`[Enz]`, not `E`. The three traces, with numbers already verified in scratch
`nums4.py` (written, **run it first**; `gen4.py` draws and splices one figure
`m4cA` — π against `c_F` with a GAG-mass top scale — into a marker pair you must first
place in the §8 subsection):
- **§1, before the `<hr>` that precedes `<!-- … href="#donnan">§2</a> -->`:** `c_F` from
  Module 0 §7 Def 7.3 — chondroitin-sulfate disaccharide 458 g/mol carries 2 charges,
  so `c_F = 2·GAG/458`: 0.2 M ⇔ 45.8 mg/mL, and the healthy 30–70 mg/mL range gives
  0.13–0.31 M. Marker `c_F` state `module0` (link `module00.html#macro`). **Do not
  re-derive Donnan**: Module 4 §2 already proves it (Module 0 §5's marker records that
  its "debt" there was false). Put the `E`, `nu`, `H_A`, `k_perm`, `sigma_0` markers
  (all *measured*, with reasons: composite/porous properties from confined-compression
  and indentation tests; `k` is a Darcy permeability that carries the water viscosity)
  in the same subsection.
- **§7, after the paragraph ending "…precisely when fluid support has failed.":**
  viscosity's temperature dependence via Module 0 §6 Prop 6.3 — water 0.890 → 0.692
  mPa·s from 25 to 37 °C is a ratio 1.286, `E_a` = 16.1 kJ/mol; Darcy `k ∝ 1/η`, so a
  cold joint has a longer gel time and *more* fluid support: F(1 s) 0.982 → 0.984 and
  `μ_eff` falls by 12 % (×0.882), while the classical Stribeck film term rises 29 %.
  Marker `mu_fric` *measured* (lubricin/hyaluronan boundary layer, an interfacial
  property this course does not compute).
- **§8, before "<p>These two struts feed a single vicious cycle:</p>":** a Lemma 8.1
  from Module 0 Prop 6.4 (Michaelis–Menten): aggrecan cleavage is first-order in the
  substrate at `[A] ≪ K_M` and zero-order at saturation, so `c_F` decays exponentially
  with `k_deg = k_cat[Enz]/K_M` — constants *measured*, not carried. Then the module's
  own formula: π(0.2 M) = 156 kPa → π(0.1 M) = 42 kPa, **a 73 % loss of swelling
  pressure for a 50 % loss of charge** (convexity of the Donnan law). Figure `m4cA`.
- Appendix: notation has 3 columns, parameters 4; add rows for the GAG stoichiometry,
  `E_a(η)`, and the 156/42 kPa pair.

**Then the rest of step 2**, in the order `chemistry-audit-and-plan.md` §2.2b and
Part 3 fix (Modules 5, 2, 6 done; **4, 14, 8/9 in flight on three Sonnet agents; 15, 16,
17 queued — integrate each report as it arrives, launch a wave-2 agent per freed slot**):

> ~~Module 5~~ → ~~Module 2~~ → ~~Module 6~~ → ~~Module 4~~ → ~~Modules 8/9~~ →
> {Module 14, Module 15, Module 16} in flight → Module 17 queued

Module 0 now has something to trace *from* for each of them, and the tracing is the
easier half: the chemistry exists, is proved, and carries provenance markers. What
each trace has to do is enter the target module **as a subsection at the point of
first use** — never as a renumbering, which would silently misdirect up to 250
in-prose `§N` references per module while every gate still passed.

The specific debts Module 0 has now made payable:

| target | what Module 0 supplies | where |
|---|---|---|
| Module 2 §5 | the two end-member moduli, derived forwards | §2 Prop 2.2 |
| Module 4 §2 | the swelling pressure from a GAG assay | §5 Prop 5.3, §7 |
| Module 5 §2 | crossbridge energetics and the force ceiling | §3, and §6 for its temperature dependence |
| Module 5 §3 | the Nernst potential and the pump ledger | §5 Prop 5.2 |
| Module 6 §1 | the licence for "a straightened fibril is linear" | §4 Prop 4.2 |
| Module 6 §8 | elastin's modulus, predicted forwards | §4 Prop 4.3 |
| Module 4 §7 | the temperature dependence of viscosity | §6 Prop 6.3 |

**Four standing constraints, unchanged and now well tested:**

1. **Rigor parity binds.** A boxed result is proved unless the box says why it cannot
   be. Module 0 has exactly two unproved boxes and both are labelled — Marko&#8211;Siggia
   (an interpolation) and the Hill equation (a fitted curve, deliberately left
   unboxed for that reason).
2. **Ask where every table value came from.** This caught three errors in Module 0.
   A parameter that arrives looking derived may be fitted one step upstream: §2's
   Born exponent was fitted to alkali-halide compressibilities, §3's `ΔG°′` is a
   fitted equilibrium model, §4's persistence length is fitted with the very model
   that consumes it.
3. **Do not assert a limit you have not computed.** This is the module's own
   recurring defect, and it recurred four times: §0's calibrated ladder, §2/§4's
   entropic collagen, §4's 108 MPa ceiling outside its own hypothesis, and §9 K2's
   "12 s" that was 16 s. Every sentence of the form "cannot exceed", "at most" or
   "half the drop by" needs a line in a verification script behind it.
4. **Run the full thirteen-gate loop plus a reviewer pass on every module a trace
   touches.** Interweaving reopens derivations the editor pass closed at `a93a55c`;
   that is the accepted cost of the chosen shape.

**Scope, stated plainly.** Phase B step 1 (Module 0) took one long session and is
done. Step 2 is eleven modules of interwoven traces, each needing the full gate loop
and a reviewer pass on the module it touches. That is **many sessions**. Commit each
trace without being asked, refresh this file at every module boundary, and do not let
a session grow past ~150k context — the session that built §3 through the Appendix
ran past 700k, which works but costs roughly fifteen times a fresh session per turn.

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

## The tracked gate scripts are stale (corrected 2026-09-10 — this section used to
## say they were not in git at all)

The scripts **run** from `C:\Users\<user>\.claude\skills\rigorous-explainer\scripts\`,
which is not a git repository. A **copy is tracked in this repo** at
`.claude/skills/rigorous-explainer/scripts/`, which earlier refreshes of this file
did not know about. That copy was compared against the live one on 2026-09-10 and is
**three files behind**:

| script | state of the tracked copy |
|---|---|
| `check_provenance.py` | **absent entirely** — ~300 lines, written 2026-09-09, one copy on disk |
| `autolink_sections.py` | 25 lines behind: no `<pre>` exclusion, no `<svg>` exclusion, **no cross-module guard** |
| `checktex.py` | 5 lines behind: no `\left`/`\right` delimiter fix, so `\rightleftharpoons` still false-positives |

The other twelve match byte for byte (`diff --strip-trailing-cr`). Losing the
cross-module guard is the one that matters: it is what stops the autolinker producing
wrong-book links, the worst defect class this repo can produce. **Copying those three
files over the tracked ones closes the risk and takes a minute.** Not done — the user
has not been asked since the staleness was measured. `provenance-baseline.txt` in this
repo is `check_provenance.py`'s *output*, not the tool.

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
