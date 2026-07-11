# Module 7 Problem-Figure Upgrade Plan

Date: 2026-07-05

## Goal

Improve the Module 7 problem-set figures for C1-C10, D1-D10, and K1-K10 so they match or exceed the visual and pedagogical standard established by Module 6.

The immediate finding from the comparison report is that Module 7's computational figures are the weakest group. K3 and K6 are the clearest examples: K3 is text-only, and K6 is a sparse symbolic schematic, while the corresponding Module 6 K figures are full computed plots with axes, ticks, labels, legends, and visible numerical structure.

## Constraints

- Do not water down the scientific level.
- Keep prose in `module07.html`; use Python only for figure data and SVG generation.
- Do not author section/problem prose inside Python raw strings.
- Use Tier-2 anatomical/body context where the figure represents a real body, stance, gait, joint, or balance situation.
- Use slim vector arrows with fixed-size arrowheads, not fat wedge/triangle load glyphs.
- Use SVG text labels with Unicode subscripts/symbols, not MathJax `$...$` inside SVG text.
- Run the rigorous-explainer hardening loop after edits.
- Do not commit until explicitly asked.

## Target Standard

Module 6 is the baseline. For Module 7 to be considered upgraded, the revised figures should generally have:

- Computed plots for computational problems where the problem asks for simulation, sweep, inverse calculation, optimization, or regime comparison.
- Axes, numeric ticks, units, legends, and marked thresholds/optima where relevant.
- Enough labels that the figure can be read without guessing what each curve, arrow, point, or limit means.
- Body/support context for balance/posture problems, especially where COM, COP, XcoM, BOS, impulses, perturbations, or stance geometry are involved.
- Visual derivation structure for D problems, not just formula callouts.
- No text-only computational figures unless the problem itself is purely symbolic and no visual computation is possible.

## Work Order

### 1. Style-Proof Batch

Start with two figures before mass-producing the full set:

- `K3`: replace the text-only gain/delay callout with a real frequency-to-control-parameter visualization.
- `K6`: replace the sparse XcoM thumbnail with a computed impulse/XcoM limit figure.

These two should establish the Module 7 computational figure style.

After building these, preview them and get user approval before revising the rest of K1-K10.

### 2. Computational Figures K1-K10

Priority order:

1. `K3`
2. `K6`
3. `K1`
4. `K2`
5. `K5`
6. `K7`
7. `K8`
8. `K10`
9. `K4`
10. `K9`

Rationale:

- `K3` and `K6` are the most visibly sparse.
- `K1`, `K2`, `K5`, `K7`, `K8`, and `K10` are far below Module 6's computational figure density.
- `K4` and `K9` are less severe but should still be checked for plot quality, labels, units, and interpretability.

Expected upgrades:

- Convert thumbnail/callout figures into actual computed plots or computed annotated schematics.
- Add axes, ticks, units, legends, and marked numerical results.
- Show sweeps, response curves, phase/gain behavior, stability regions, impulse limits, or optimization landscapes where the problem asks for those computations.
- Keep the computation source in scratchpad scripts and splice only the figure bodies into `module07.html`.

### 3. Derivational Figures D1-D10

Priority order:

1. `D7`
2. `D5`
3. `D4`
4. `D8`
5. `D1`
6. `D2`
7. `D9`
8. `D6`
9. `D3`
10. `D10`

Rationale:

- `D7` is currently equation/text-only.
- `D5` is mostly a formula/result callout.
- Several D figures have no plotted curve or visual derivation structure.
- Some D figures have body context but still lack the visual mechanics behind the derivation.

Expected upgrades:

- Add geometry, force-balance, root-locus, response-curve, phase-plane, or control-block visual structure as appropriate.
- Use the SVG to show why the derivation works, not merely restate the final equation.
- Keep equations in the prose where possible; the figure should clarify the relationship visually.

### 4. Conceptual Figures C1-C10

Priority order:

1. `C8`
2. `C3`
3. `C7`
4. `C5`
5. `C10`
6. `C2`
7. `C1`
8. `C4`
9. `C6`
10. `C9`

Rationale:

- The conceptual group is mixed, not globally bad.
- `C8` is the clearest weak conceptual figure.
- Several Module 7 C figures already include useful body context and should be polished rather than fully replaced.

Expected upgrades:

- Add body/support context where it improves interpretation.
- Increase label clarity where Module 7 currently has fewer labels than Module 6.
- Avoid unnecessary redraws for already adequate figures.

## Figure Families To Build

### Balance/Posture Body Schematics

Use Tier-2 body context for:

- COM relative to base of support
- COP shifts
- Stance width
- Perturbation arrows
- Ankle/hip/step strategy
- XcoM and capture limits

### Control-System Plots

Use computed plots for:

- Frequency response
- Gain/damping sweeps
- Delay margins
- Step responses
- Stability regions
- Phase lag

### XcoM / COP / BOS Figures

Use a consistent visual vocabulary:

- Ground line and support polygon/base
- COM marker
- XcoM marker
- COP marker
- Perturbation/impulse arrow
- Clearly labeled capture boundary
- Numerical annotations tied to computed values

### Derivation Figures

Use visual derivation aids:

- Free-body diagrams
- Small phase-plane sketches
- Root-locus or pole diagrams
- Curve sketches with slopes/limits marked
- Geometric decomposition of COM/COP/XcoM relations

## Verification

After each edit batch, run:

```powershell
$S="C:/Users/<user>/.Codex/skills/rigorous-explainer/scripts"
python $S/checktex.py module07.html
python $S/checklt.py module07.html
python $S/check_links.py module07.html
python $S/verify_dom.py module07.html
python $S/check_overlap.py module07.html
python $S/check_frame.py module07.html
python $S/check_prose.py module07.html
python $S/check_proofs.py module07.html
```

Also render representative figures with:

```powershell
python $S/shoot.py FILE out.png --size WxH
```

Then rerun the Module 6 vs Module 7 figure-density comparison to confirm the weak Module 7 groups improved.

## Review Cadence

Recommended workflow:

1. Build and preview `K3` and `K6` only.
2. Get user approval on the upgraded computational figure style.
3. Upgrade the remaining K figures.
4. Upgrade D figures.
5. Polish C figures.
6. Run the full hardening loop.
7. Provide a short summary with two `★ Insight` bullets, following the established project cadence.

## Definition Of Done

The upgrade is complete when:

- All 30 Module 7 problem figures still exist.
- K figures are no longer mostly thumbnail/callout style.
- K3 and K6 are full computation-backed figures.
- Sparse D figures have visual derivation structure.
- Conceptual figures have adequate context and labels without unnecessary redraws.
- Hardening checks pass or any advisory warnings are explicitly documented.
- The follow-up comparison shows Module 7 problem figures are at least comparable to Module 6 in pedagogical richness, especially for K1-K10.
