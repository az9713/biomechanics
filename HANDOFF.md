# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last handoff written:** 2026-09-09. **Two phases are stacked, and their order
matters.** The editor pass is complete but **unpromoted**. A new chemistry phase is
planned but **not started**. Promotion must happen first — see the next task.

---

## Current state (as of `45ba749`, pushed, remote verified)

### Phase A — the editor pass: COMPLETE, NOT PROMOTED

All fifteen modules (3–17) have a report in `editor-reports/`, an applied draft in
`edited/`, all nine gates at or better than the pristine baseline, and a
`## 6. Changes applied` table. Modules 1 and 2 were done in place (`3a4dae1`,
`ac93c14`). Roughly 1000 anchored edits, ~14 000 lines of report.

**Nothing has been promoted.** `edited/moduleNN.html` and the live `moduleNN.html`
both sit in the repo, and `index.html` / `README.md` still point at the originals.
Measured drift between them (lines differing):

| Module | 4 | 5 | 6 | 14 |
|---|---|---|---|---|
| lines differing | 523 | 460 | 345 | 324 |

Promotion for a signed-off module is `mv edited/moduleNN.html moduleNN.html`, then
re-run the nine gates in place and push.

One known drift to fix before promoting module 3: `edited/module03.html:858` states
a range its own equation contradicts at one endpoint.

`edited/` is committed and pushed, so the drafts are live but unlinked at
`https://az9713.github.io/biomechanics/edited/moduleNN.html`. Nothing finds them
without the URL.

### Phase B — the chemistry / interweaving layer: PLANNED, NOT STARTED

Audit and plan are in **`chemistry-audit-and-plan.md`** (`29e9087`, revised
`45ba749`). Read that file, not this summary, before building.

The audit finding: **chemistry appears in the course as nouns, never as equations.**
Exactly one real physical-chemistry derivation exists in 5.6 MB — Module 4 §2
(electrochemical potential → Donnan → van 't Hoff). Eighteen chemistry concepts score
zero across all seventeen modules (Gibbs, entropy, `K_eq`, Arrhenius, pH, Nernst,
`k_B T`, Fick, amino acid, and more). `prompt.txt:211` specifies a **Required
Biological / Chemical Spine** of 25 items; one is delivered as mathematics.

Root cause: the teaching pipeline in `prompt.txt` has step 3 "physical mechanism" and
**step 4 "molecular / cellular substrate"**. The build ran steps 5–19 and skipped 4.
The Modeling Levels ladder starts at Level 0 = scalar force, so there was never a rung
for a mole or a bond energy.

**Decisions taken with the user (2026-09-09):**

| Question | Decision |
|---|---|
| Shape | Interweave into the existing 17, plus one new `module00.html` |
| Scope | Chemistry **and** biology (signalling, endocrine, tissue turnover) |
| Module 0 depth | Full course standard — 30 problems, labs, figures, appendix |
| Build order | Module 0 first |
| Structure | Subsection at point of first use. **No `§NC` letter suffixes** — that scheme was proposed, then rejected by the editor pass as adjacency rather than interweaving |
| Enforcement | New `check_provenance.py` added to the hardening loop |

**The user's defining requirement:** chemistry, biology and physics must be
*interwoven*, with every physics result traceable back to its biological and chemical
origin. The unit of work is a **trace** — molecule → cell → tissue → body — ending on
a number the course already prints. A chemistry passage that does not terminate on an
existing mechanical result is decoration.

---

## Next task

**1. Resolve promotion before writing any chemistry. This is a hard prerequisite.**

The chemistry plan interweaves into M2, M4, M5, M6 and M14 — the same files that have
324–523 lines of unpromoted editorial edits waiting in `edited/`. Building chemistry
into the originals means a later promotion clobbers it, or forces a three-way merge.

Ask the user: promote all fifteen at once, or module by module after they read each
report? Then promote, re-gate in place, and push. Only then start Phase B.

**2. Write `check_provenance.py` before any prose.** Run it over all 17 modules and
keep the output as the baseline inventory of every borrowed constitutive parameter
(`E`, `c_F`, `mu`, `sigma_Y`, the remodeling gain `k`, Hill's `a/F_max`, every time
constant). That inventory **is** the definitive worklist — it replaces the judgement
calls in `chemistry-audit-and-plan.md` §2.2b with a measured list. The gate flags any
boxed parameter whose section declares none of: *derived here*, *derived in Module 0
§X*, or *measured, not derived, because …*.

**3. Then `module00.html` §0**, section by section under the standing convention:
build one section → report with a short summary and two `★ Insight` bullets → user
reviews → commit and push. Fix the chemistry symbol namespace in its appendix before
§1 is written (`F` is force everywhere but Faraday in M4; `mu` is friction in M4 §7
and chemical potential in M4 §2; `k` is the M2 remodeling gain and wants to be a rate
constant; M4 already renamed the gas constant `R_g`). Get one representative molecular
figure approved before mass-producing the rest.

Then Module 5 → Module 2 → Module 6 → Module 4 → Module 14 → Modules 8/9 →
Modules 15/16/17. Full order and per-module traces in `chemistry-audit-and-plan.md`
§2.2b and Part 3.

If the user asks for something else, that takes precedence.

---

## Lessons that bind the next phase

These came out of the editor pass and apply directly to building chemistry figures
and derivations.

**The nine gates do not see wrong content, only broken content.** Every gate was green
on a caption describing an axis the figure did not have (m06), a curve plotting `L·p`
on an axis labelled "peak stress" (m14), and a grip curve drawn at 1.3× the true load
in a problem about slip (m11).

- **Decode `<polyline>` point strings back into data** and compare against the model.
  **Calibrate from the axis `<line>` elements, not the tick `<text>` baselines** — m04
  found those baselines sit 3 px low, and that offset alone shifts a recovered peak
  pressure by 0.065 MPa, manufacturing a discrepancy that is not there.
- **Render at least once.** `check_overlap` tests text against curves and dashed lines,
  never text against text. m15 found a label sitting on another label and an optimal
  curve hidden under the truth curve — invisible to every gate.
- **Run the code before reading the prose.** A module claiming "every number was
  produced by running the code" usually has problems carrying no code at all (m14's
  ten K problems had none while the module said so three times).
- **Grep for residue after every apply.** Every module that looked found some: a
  replacement made in one place, the superseded value left standing elsewhere.
- **Prove an apply, don't read it.** Reset to pristine, re-run `apply.py`, confirm the
  output is byte-identical. That is the only way to know the script did not die before
  its single `write_text`.

**New, from the chemistry planning session:** `check_links.py` passes on a *renumbered*
section — the links still resolve, they just point at the wrong section. M4 carries 250
in-prose `§N` references, M5 248, M6 208. **Never renumber an existing section**; add
chemistry as a subsection, which shifts no integer. Green gates, wrong book is the
worst defect class this repo can produce.

---

## Where to read things (reference, don't re-derive)

- `CLAUDE.md` — standing conventions: build loop, the nine gates, git/publish.
- `chemistry-audit-and-plan.md` — Phase B audit, plan, threading map, build order.
- `prompt.txt` — original course spec; source of truth for scope. Line 211 is the
  Required Biological/Chemical Spine; line 285 the Modeling Levels ladder.
- `EDITOR_DOMAIN.md` — the domain brief the `science-editor` skill loads.
  (`EDITOR_PROMPT.md` describes a *different* manuscript — ignore its `# Domain:`.)
- `editor-reports/moduleNN.md` — per-module editor reports with change tables.
- `moduleNN-plan.md` — per-module build plans for modules 4–10.

## Session-transient scratch (regenerate; durable record is the committed output)

- **`scratchpad/tools/BRIEF.md`** — the 117-line agent brief that drove the editor
  pass. Ten steps: load `science-editor` + `EDITOR_DOMAIN.md` + `editor-reports/module02.md`
  as format model; never touch the original, write only `edited/`, run no git command
  (reset is `cp`, not `git checkout`); record the nine-gate baseline on a pristine copy
  first, end rule is *zero where the baseline was zero, never worse anywhere*; own
  scratchpad per agent; run the code before reading the prose; read against the
  five-part standard; report shaped like `module02.md`; one re-runnable `apply.py` with
  `rep()` asserting each anchor is unique; author math only via Write/Edit or a Python
  raw string, never a double-quoted shell arg; re-gate; report in ten lines.
  **Worth promoting into the repo next session rather than rebuilding again.**
- `scratchpad/tools/extract.py` (every `<pre><code>` block out to a runnable `.py`),
  `txt.py` (dump a line range with `<svg>` collapsed, UTF-8, never truncated),
  `apply_skel.py`.
- `scratchpad/interweave_section.md` — the revised §2.2 text, already spliced into
  `chemistry-audit-and-plan.md`. Nothing to regenerate.

## How to work (essentials — full detail in `CLAUDE.md`)

- **Section by section.** Build one section → report with a short summary and two
  `★ Insight` bullets → user reviews → commit and push. Standing rule: after each
  module or work unit, commit and push without waiting to be asked.
- **Run the full hardening loop after every edit pass** — all nine scripts in
  `CLAUDE.md`, plus `check_provenance.py` once it exists, plus a `rigor-reviewer` pass.
- **Never author math-bearing HTML inside a double-quoted shell argument.** The shell
  eats `$…$` and turns `\t` into a TAB. Use Write/Edit, or splice from a file using a
  Python raw string. Large markdown with `§`, backticks and em-dashes also breaks bash
  heredocs in this environment — use the Write tool and splice from the file.
