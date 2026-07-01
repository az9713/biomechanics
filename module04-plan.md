# Plan: Module 4 — Cartilage, Synovial Fluid, and Joint Contact Biophysics

## Context
Continuation of the quantitative human-musculoskeletal course in
`C:\Users\simon\Downloads\human_movement_science_me`. Modules 1–3 are COMPLETE
and live. Module 4 develops the **tissue** that lives at the joint interface
Module 3 left idealized. It is the first *continuum/biphasic* module.

**Scope sources** (read these first; this plan is derived from them):
1. `prompt.txt` → "### Module 4" (cover-list + required includes) and the
   mandatory 23-step teaching pipeline + per-module lab/diagnostic requirements.
2. **`module03.html` forward-references that bind us** (promises to the reader):
   - §5 (contact pressure): "the biphasic behaviour we develop quantitatively in
     **Module 4**"; cartilage degeneration → osteoarthritis "(**Module 4**)";
     Hertz peak pressure given only as a *preview*.
   - §8 repayment table + §8.3: **frictionless → Module 4** (real μ≈0.005, biphasic
     lubrication); **elastic/Hertz contact → Module 4** (biphasic, viscoelastic,
     creeps; contact area varies); **bilateral → unilateral contact** partly here.
   - Module 3 **Appendix** supplies the *inputs*: hip reaction $R\approx2.5W\approx
     1715\ \mathrm N$, contact area $A_c\approx10\ \mathrm{cm^2}$, mean pressure
     $p\approx1.7\ \mathrm{MPa}$, $\mu\approx0.005$, $\nu\approx0.5$.

Format/scope locked (no need to re-ask): one self-contained `module04.html` via
the `rigorous-explainer` skill; Tier-2 anatomy + computed plots (compute data with
Python first); full hardening loop; builds on and links back to Modules 1–3,
forward to Modules 14 (OA/aging) and 16 (continuum/FE).

## Deliverable
`C:\Users\simon\Downloads\human_movement_science_me\module04.html`

## Spine (each section uses the previous)
- **§0 Motivation.** A 2–4 mm layer of soft tissue carries ~1.7 MPa (Module 3 §5)
  millions of cycles a year for decades, at friction *below ice* (μ≈0.005). How
  does something that soft survive that — and why does it eventually fail (OA)?
  Answer: cartilage is not a solid; it is a charged, fluid-filled porous gel.
- **§1 Cartilage as a hydrated, charged, porous composite.** Define the three
  players: **collagen** network (carries tension), **proteoglycans** (fixed
  negative charge), **interstitial water** (~70–80% by weight). Volume fractions;
  the "solid matrix + interstitial fluid" idealization that the rest builds on.
- **§2 Osmotic (Donnan) swelling pressure.** Fixed charge → counter-ion imbalance
  → Donnan osmotic pressure $\pi=RT\!\big(\sqrt{c_F^2+4c_0^2}-2c_0\big)$ that
  pre-stresses the matrix in tension and resists compression. Worked number
  ($c_F\sim0.2$ M, $c_0\sim0.15$ M → π ~ 0.1–0.2 MPa). This is the *resting*
  load-bearing the dry models of Module 3 missed.
- **§3 The biphasic model (MAIN RESULT, boxed).** Mixture theory: incompressible
  solid matrix saturated with incompressible fluid; **Darcy drag** through
  permeability $k$; aggregate modulus $H_A$. Derive the 1-D confined-compression
  **consolidation PDE** $\partial u/\partial t = H_A k\,\partial^2 u/\partial z^2$
  — a diffusion equation with diffusivity $D=H_Ak$ and gel time $\tau\sim h^2/(H_Ak)$.
- **§4 Interstitial fluid pressurization & load sharing.** The headline mechanism:
  under fast load the *fluid* carries almost all the stress (fluid load-support
  fraction → 1), shielding the solid matrix; over time $\sim\tau$ the fluid exudes
  and stress transfers to the solid. With $h\sim2$ mm, $H_A\sim0.6$ MPa,
  $k\sim10^{-15}\,\mathrm{m^4/Ns}$ → $\tau\sim$ thousands of s ≫ a footstep, so
  walking is carried by fluid pressure. Why cartilage survives.
- **§5 Computational lab 1 — stress relaxation / creep.** Finite-difference the
  §3 consolidation PDE; apply a step strain (confined compression), plot stress
  relaxing peak→equilibrium with time constant $\tau$. Parameter table, code
  listing, sensitivity ($\tau\propto h^2/(H_Ak)$), extension challenge. (prompt.txt:
  "Python simulation of cartilage stress relaxation".)
- **§6 Contact: from joint reaction to a pressure field.** Take $R\approx1715$ N
  from Module 3 §5; **Hertzian** elastic contact gives contact radius and peak
  pressure ($p_0=3F/2\pi a^2$, $a\propto(FR_{\rm eff}/E^*)^{1/3}$ — derived in M3
  D7); then show biphasic fluid pressurization *flattens and spreads* it. Refines
  M3's mean-pressure estimate into a real distribution.
- **§7 Computational lab 2 — lubrication.** Why μ is so low. Regimes: **boundary**
  (lubricin/hyaluronic-acid molecules), **fluid-film**, **elastohydrodynamic**,
  and the dominant **biphasic/interstitial-fluid-pressurization** mode (fluid
  carries the load → contact friction tiny). **Stribeck curve** μ vs
  (viscosity·speed/load); synovial fluid as shear-thinning (non-Newtonian).
  Python: μ vs Stribeck number. (prompt.txt: "lubrication-dependent friction".)
- **§8 Degeneration / osteoarthritis mechanics.** The failure cascade as a
  positive feedback: proteoglycan loss → lower fixed charge → less osmotic
  pre-stress (§2) → more load on collagen → fibrillation; rising permeability $k$
  → fluid exudes faster → fluid load-support (§4) drops → solid matrix overloaded
  → more damage. Ties peak pressure (M3 §5) and aging (forward-ref Module 14).
- **§9 Captures / misses + diagnostics + problems.** Captures/misses with a
  repayment table forward to **Module 16** (full continuum/FE, anisotropy,
  finite strain) and **Module 14** (OA as aging). Then **5 diagnostic questions**
  + **3 problems** (conceptual / derivational / computational) as the baseline
  per prompt.txt. *(Optional: expand to the 10×3 set as the user requested for
  Module 3 — ask before doing the larger build.)*
- **Appendix** — parameter table ($H_A$, $k$, fixed charge density $c_F$, water
  fraction, synovial viscosity, μ regimes, thickness $h$, τ) + notation;
  links back to Modules 1–3, forward to 14 & 16.

## Mathematical spine introduced here
Mixture/biphasic theory · Darcy's law & permeability · Donnan osmotic pressure ·
1-D consolidation (diffusion) PDE + finite differences · Hertzian contact (reused
from M3 D7) · Stribeck/lubrication regimes · poroelasticity (toy level; full
continuum deferred to Module 16).

## Figures (Tier-2 anatomy + computed plots; follow the CLAUDE.md figure rule)
Build a reusable generator + shared `<defs>` (per CLAUDE.md "Figure style"); get
ONE representative figure approved before mass-producing.
- §1 **cartilage micro-structure** (Tier-2): collagen arcades + proteoglycan
  aggrecan brushes + water, as a shaded layer on subchondral bone.
- §2 Donnan: fixed-charge + mobile-ion schematic **+ computed** π vs $c_F$ curve.
- §3 confined-compression setup (porous solid + fluid + permeable platen) schematic.
- §4 **computed** fluid load-support fraction vs time (→1 fast, decays over τ);
  optional SMIL of fluid exuding under a held load.
- §5 **computed** stress-relaxation curve (peak → equilibrium).
- §6 Tier-2 joint contact **+ computed** Hertz pressure profile, with the biphasic
  flattening overlaid.
- §7 **computed** Stribeck curve + a lubrication-regimes schematic.
- §8 OA cascade diagram (positive-feedback loop) + pressure-redistribution sketch.

## Build steps
1. Compute all figure/plot data in the scratchpad: Donnan π(c_F), the consolidation
   PDE (finite differences → relaxation curve + fluid-support fraction), Hertz
   profile, Stribeck curve. Emit SVG polyline coords + key numbers.
2. Rebuild the Tier-2 figure toolkit (shared defs + generators) from the CLAUDE.md
   pattern; approve one representative figure first.
3. Write `module04.html` from the skill template; embed computed coordinates;
   define every symbol/term at first use; box the biphasic governing equation.
4. Harden after every edit: `checktex.py`, `checklt.py` (+`escape_math_lt.py`),
   `check_links.py`, `verify_dom.py`, `shoot.py` preview. Cross-link to module0[123]
   and run `autolink_sections.py` once sections exist.

## Verification
- All checkers pass: 0 tex, 0 raw `<`/`>`, 0 broken links, 0 mjx-merror.
- Cross-links to `module03.html#contact` / `#model` etc. resolve.
- Spot-check numbers: Donnan π ~ 0.1–0.2 MPa; gel time τ ~ 10³–10⁴ s with
  $h\sim2$ mm; fluid load support → ~1 on a footstep timescale; μ ~ 0.001–0.02.
- The §6 contact pressure must be consistent with Module 3 §5's $p\approx1.7$ MPa
  mean (and Hertz peak above it).

## Workflow reminders (from CLAUDE.md — do not re-derive)
Section-by-section; report each with a short summary + 2 `★ Insight` bullets;
**commit only on the user's "commit push."** Figures must be recognizable Tier-2
with clean labelled vector arrows (never abstract arrows-on-a-line); SVG-text
labels use Unicode subscripts, not `$…$`.

## Status
NOT STARTED. This file = the Module 4 plan. Begin at §0 on the user's go-ahead.
Modules 5–17 follow the same pattern (draw each plan from `prompt.txt` + the prior
module's forward-references when starting it).
