# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last written:** 2026-09-09 (second refresh, at the Module 0 §1 boundary).
Phase A (editor pass) is **complete and promoted**. Phase B (chemistry and biology
interweaving) has its **gate and worklist built**, and **Module 0 §0 and §1 are
written, reviewed and live**. Start at "Next task": Module 0 §2.

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

### Phase B step 1 remainder onward — NOT STARTED

Module 0 §2–§9 and its Appendix are unwritten; no chemistry prose exists in Modules
1–17 yet.

---

## Next task

**Build `module00.html` §2** — bonding and the stiffness ladder — under the standing
convention: build one section → report with a short summary and two `★ Insight`
bullets → user reviews → commit and push (the standing tutor rule says commit without
waiting to be asked).

Its content spec is `chemistry-audit-and-plan.md` §2.3. **§2 is the section that pays
§0's largest debt**, and the debt is named in §0's own provenance markers: §0
*calibrated* the effective bond stiffnesses `25 N/m` and `0.30 N/m` backwards from
Module 2 §5's measured moduli, so its `104 GPa` and `1.07 GPa` are that measurement
returned, not a prediction. §2 must run the calculation **forwards**: define an
interatomic potential, take its second derivative at the minimum, sum over the
coordination number and the loading direction, and show what survives of the bare
`530 N/m` Ca–O pair stiffness that would otherwise predict `2200 GPa` for apatite.
When it succeeds, flip the `E_apatite` / `E_collagen` markers from `measured` to
`derived` (or say plainly why they must stay `measured`).

Three standing constraints:

1. **Rigor parity binds §2 hardest.** A derived `E_apatite` beside an asserted
   `E_collagen` is the Module 6 §6 defect in a new place. Collagen's fibril
   stiffness is hydrogen-bonded and architectural; if §2 cannot do it forwards,
   say so and hand it to §4, rather than boxing an assertion beside a proof.
2. **The chemistry symbol namespace is already fixed** in §2.2c's canonical-name
   table, extended by §1's list above. Module 0's Appendix follows that record.
   Register `k_bond` there; §2.2c has no entry for it.
3. When §2 lands, flip its TOC entry in `module00.html` from
   `<span class="pending">` to a link, update the "§0 and §1 are complete" note
   below the TOC, and re-run `autolink_sections.py` — 27 forward `§N` refs are
   still unlinked and will resolve as sections land.

Then, in order (full traces in `chemistry-audit-and-plan.md` §2.2b and Part 3):
Module 5 → Module 2 → Module 6 → Module 4 → Module 14 → Modules 8/9 →
Modules 15/16/17.

**Scope, stated plainly.** "Finish the chemistry and biology update for all modules"
is Module 0 at full course standard (30 problems, labs, figures, appendix — Modules 3
and 4 are ~2200 lines each) plus interwoven traces into eleven existing modules. It
is **many sessions**, not one. Work it in order, commit each unit without being
asked, refresh this file at each module boundary, and do not let a session grow past
~150k context. Do not report the phase complete until it is.

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
2026-09-09 and exist in exactly one copy. `provenance-baseline.txt` in this repo is
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
