# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last written:** 2026-09-09. Phase A (editor pass) is **complete and promoted**.
Phase B (chemistry and biology interweaving) has its **gate and worklist built**;
no chemistry prose exists yet. Start at "Next task".

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

### Phase B step 1 onward — NOT STARTED

`module00.html` does not exist. No chemistry prose has been written anywhere.

---

## Next task

**Build `module00.html` §0** (Chemical Foundations — motivation), section by section
under the standing convention: build one section → report with a short summary and
two `★ Insight` bullets → user reviews → commit and push.

Its content spec is `chemistry-audit-and-plan.md` §2.3. §0's job is "why a bond
energy sets a bone's stiffness" — and under the three-layer opening rule it states
up front what you observe (physics), which tissue does it (biology), and which
molecule makes that tissue behave that way (chemistry).

Two things to settle inside §0, before §1 is written:

1. **Get one representative molecular figure approved before drawing the rest.**
   `CLAUDE.md` requires this for any section needing many figures in one style; a
   style fix applied to 30 figures is expensive. Build the shared hidden `<defs>`
   block and one figure, render it, and show it marked *veto this before I draw the
   rest*.
2. **The chemistry symbol namespace is already fixed** in §2.2c's canonical-name
   table — Module 0's appendix follows that record, not the other way round. Do not
   re-derive it.

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
