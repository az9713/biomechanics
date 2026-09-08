# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last handoff written:** 2026-09-08 (editor phase, Modules 3–17, run as fifteen
parallel agents. **8 complete**; 7 relaunched and in flight. Last commit
pushed; see the table below for each module's commit.)

---

## Current state — the EDITOR phase, run in parallel

The anatomy regression is closed. What is running now is a **`science-editor`
pass on every module the phase had not yet reached**: read `moduleNN.html`
against the five-part standard, write a report, apply it, gate it, log it.

**The user's instruction that set this shape (2026-09-08):** do all remaining
modules, **not one by one**, **never overwrite the originals**, and **write a
detailed log of what changed for each module**. Three decisions they made:
output goes to `edited/moduleNN.html`; every module gets the full pass (extract
and run every code block, re-derive every number); gates only, no per-module
render-verify sweep.

### Where each module stands

`edited` = lines differing from the original. `log` = the report carries its
`## 6. Changes applied` table.

| Module | State |
|---|---|
| 1, 2 | done in place (`3a4dae1`, `ac93c14`) |
| **3** | **COMPLETE** — 21 blocking, 18 style, 70 edits (`2f7e8a4`) |
| **6** | **COMPLETE** — 17 blocking, 15 style, 52 edits (`f028bfc`) |
| **9** | **COMPLETE** — 16 blocking, 18 style, 80 tags |
| **11** | **COMPLETE** — 19 blocking, 15 style, 60 edits (`f028bfc`) |
| **12** | **COMPLETE** — 12 blocking, 22 style, 96 edits (`d48bfc8`) |
| **13** | **COMPLETE** — 102 edits (`49ab3a3`) |
| **14** | **COMPLETE** — 15 blocking, 13 style, 63 edits (`979bd0a`) |
| **16** | **COMPLETE** — 17 blocking, 13 style, 55 edits (`979bd0a`) |
| **4** | **COMPLETE** — 17 blocking, 13 style, 107 edits |
| **5** | **COMPLETE** — 22 blocking, 11 style, 72 edits; Fig. 30 rebuilt and verified |
| **7** | **COMPLETE** — 86 tags; K2's figure regenerated from the Hopf boundary |
| 8 | report + 226 edits, no change log; open: a literal `_` in an SVG `<text>` (check_svg HARD) and K10's frame |
| 10 | report written, apply NOT run; check_frame is the point of this module |
| 15 | report + 298 edits; open: which listing prints what K2–K10 quote |
| **17** | **COMPLETE** — 63 edits; course closure verified |

**Twelve complete. Seven were relaunched 2026-09-08 with the defect each one's
predecessor named in its dying words.**

## Next task — finish the seven, then promote

1. **Wait on the seven in flight** (4, 5, 7, 8, 10, 15, 17). Each was relaunched
   with the exact defect its predecessor named. If a fleet dies again, relaunch
   from the table above — every entry names what that module still owes.
2. **Module 7 needs a reset, not a resume.** Its apply is partial (175 lines)
   and the script is not idempotent. Its failure was an anchor written with an
   HTML entity where the file holds the literal character (`·` U+00B7). Check
   every anchor for entity-vs-literal mismatch: `·`, `≈`, `−` (U+2212, not a
   hyphen), `°`, `×`, Greek, and the Unicode subscripts the house style uses in
   SVG `<text>`.
3. **Then promote.** When a module is signed off, `mv edited/moduleNN.html
   moduleNN.html`. Decide with the user whether to promote all at once or
   module by module.

### Prove the apply, don't read it

Four agents converged on the same check independently, and it should now be
standard: reset to pristine, re-run `apply.py`, and confirm the output is
**byte-identical** to the edited file. Then confirm the tag count equals the
change-log row count, in order, and that each row's stated line is the anchor's
true first line in the pristine file. This is the only way to know the script
did not die before its single `write_text` — the failure that leaves the file
untouched while the log still looks plausible.

### An edit pass can INTRODUCE residue

m07 found a regression this project's own editor pass created: B4a rewrote
K8's problem statement and left the figure's `aria-label` carrying the
superseded one. It surfaced by machine-comparing all 23 problem aria-labels
against their statements. **Run that comparison after every apply** — residue is
not only the module's pre-existing debt.

### Never infer apply state from a proxy

Twice the lead mis-read a module's state and sent a wrong instruction: once from
an agent's dying message, once from a changed-line count (175 lines looked
partial; it was 79 complete edits). Neither is evidence. **The only test is to
re-run the script from pristine and compare bytes.**

### A dying message names the NEXT step, not an undone one

When relaunching a killed agent, do not build its instruction from its last
words. m17 was told its `$I$` collision was unresolved because its predecessor
died saying "now I'll write the rep() block for the unresolved $I$ collision" —
but that work was already in `apply.py` and applied. **Read the files to
establish state; use the dying message only as a hint about where to look.**

### Grep for residue after every apply

Every module that looked for it found some: a replacement made in one place and
the superseded value left standing elsewhere. m16's K6 figure label still read
"ratio 12×" after its solution had been corrected to 12.5. m13's μ rename left
five bare `\mu` behind after the notation table had stopped defining one.
m09's Fig. 7 still integrated to 181.0 N·s after every label around it read
32.0.

### The reusable brief (this is the important artifact)

**`scratchpad/tools/BRIEF.md`** is the 117-line agent brief that produced the
three complete modules. It is session-transient — **rebuild it from this
description**, or better, promote it into the repo next session:

Ten steps. (0) Load `science-editor`, then `EDITOR_DOMAIN.md`, `HANDOFF.md`,
`CLAUDE.md`, and `editor-reports/module02.md` as the format model. (1) Never
touch the original; write only `edited/moduleNN.html`; **run no git command at
all** — the reset is `cp`, not `git checkout`. (2) Record the nine-gate baseline
on the pristine copy first; the end rule is *zero where the baseline was zero,
never worse anywhere*; a Chrome gate that times out is cold-start contention, so
retry once. (3) Shared tools, own scratchpad folder per agent. (4) **Run the
code before reading the prose** — highest-yield step. (5) Read the whole module
against the five-part standard plus the house rules. (6) Write the report shaped
like `module02.md`. (7) One re-runnable `apply.py`, `rep()` asserting each anchor
is unique, plus the three known traps. (8) Author math only via Write/Edit or a
Python raw string, never a double-quoted shell arg. (9) Re-gate, then write the
change table. (10) Report back in ten lines.

Also in `scratchpad/tools/`: `extract.py` (every `<pre><code>` block out to a
runnable `.py`, flagging live HTML tags inside code), `txt.py` (dump a line
range, `<svg>` collapsed, UTF-8, never truncated), `apply_skel.py`.

**Give each agent a short prompt pointing at the brief plus its own state.** The
first launch put the whole brief in fifteen prompts and burned the lead session's
context for no gain.

## The lesson the three completed modules all reported

**The nine gates do not see wrong content, only broken content.** Every gate was
green on each of these:

- m06: the report's own replacement caption for Fig. 16 described an x-axis the
  figure does not have (it plots the dimensionless $\omega\tau_\sigma$; the peak
  vertex is at 0.74 and the band spans 8–90).
- m14: a curve plotting $L\cdot p$ on an axis labelled "peak stress"; a muscle
  drifting at 0.31 %/yr under a module claiming 1 %/yr; a runaway clamped flat
  at the 9 MPa axis ceiling from year 43, under a caption claiming a runaway.
- m11: a grip curve drawn at 1.3× the true load, so the figure showed no slip in
  a problem about slip; and a 737 N curve clipped flat against a 300 N axis.

**The technique that caught them all: decode the `<polyline>` point strings back
into data.** Invert the axis mapping and compare against the model.
**Calibrate from the axis `<line>` elements, not the tick `<text>` baselines** —
m04 found those baselines sit 3 px low, and that offset alone shifts a recovered
peak pressure by 0.065 MPa, i.e. it manufactures a discrepancy that is not there. Carry this into every remaining module — it is
cheaper than a render sweep and it catches a different class of defect.

Second recurring finding: **a module that claims "every number was produced by
running the code" usually has problems carrying no code at all.** m14's ten K
problems had none, while the module said so three times. m11 had three of four
labs printing nothing. m03's §7.4 lab computes its headline forces and prints
none of them.

## Open decision for the user

`edited/` is committed and pushed, so the drafts are reachable on Pages at
`https://az9713.github.io/biomechanics/edited/moduleNN.html`. They are **not**
linked from `index.html` or `README.md`, so nothing finds them without the URL.
If that is unwanted, add `edited/` to `.gitignore` and `git rm -r --cached
edited` — but then the drafts stop being backed up.

When a module is signed off, promotion is `mv edited/moduleNN.html moduleNN.html`.

## Where to read things (reference, don't re-derive)

- `editor-reports/*.md` — what was wrong with each module, the exact fix, and
  (where present) the `## 6. Changes applied` table.
- `EDITOR_DOMAIN.md` — the domain brief the `science-editor` skill reads.
- `CLAUDE.md` — standing conventions: build loop, the nine hard gates, git and
  publish, figure style, math-in-HTML gotchas, the K-problem depth standard.
- `ANATOMY_AUDIT.md` — the closed anatomy phase.
- `prompt.txt` — course structure, source of truth.

## How to work (essentials — full detail in `CLAUDE.md`)

- **Extract and RUN every `<pre><code>` block before reading for rigor.**
- **Nine hard gates after every edit pass**, all zero: `checktex`, `checklt`,
  `check_links`, `check_svg`, `check_code`, `verify_dom`, `check_overlap`,
  `check_frame`, `check_bodyprop`. Then read the advisories.
- **Then look at the figures** — decode the polylines, or render. Gates are
  necessary and not sufficient.
- **Commit + push per module**, as `az9713` /
  `az9713@users.noreply.github.com`, with the standard trailer block. Public
  repo — never reintroduce the private `az9713@yahoo.com` address.
- Subagents doing an apply run **no writing git command**; the lead commits
  after re-running the gates.

## Open items (small, not blocking)

- **Cosmetic anatomy leftovers:** only **m10 wishbone shoulders** remains.
  m09's piled feet and knee-less stance leg are fixed and render-verified;
  m13's figures re-rendered with no detached head. Locate by caption.
- **A stroke-width gate for `check_svg.py`** would catch the "realism commit"
  failure class mechanically. It lives in the shared `rigorous-explainer` skill,
  so it is a toolchain change, not a module change.
- Two full agent fleets were lost to usage limits mid-run. `autoContinueAtUsage
  Limit: true` is set in `~/.claude/settings.json`, but it did not save the
  subagents — only the lead. Launch fleets early in a limit window.
