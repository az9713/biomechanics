# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last handoff written:** 2026-09-08 (editor phase, Modules 3–17, run as fifteen
parallel agents. 3 modules complete, 9 applied but owing gates or a change log,
3 not started. Last commit `f028bfc`, pushed.)

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

| Module | edited | report | log | gates | State |
|---|---|---|---|---|---|
| 1, 2 | applied in place | yes | yes | pass | done earlier (`3a4dae1`, `ac93c14`) |
| **6** | 345 | 918 ln | yes | **all 9 pass** | **COMPLETE** — 17 blocking, 15 style, 52 edits |
| **11** | 129 | 480 ln | yes | **all 9 pass** | **COMPLETE** — 19 blocking, 15 style, 60 edits |
| **14** | 324 | 380 ln | yes | **all 9 pass** | **COMPLETE** — 15 blocking, 13 style, 63 edits |
| 3 | 355 | 624 ln | yes | not run | **RESET AND RE-APPLY** — see below |
| 4 | 480 | 853 ln | no | not run | applied; owes gates + log |
| 7 | 168 | 536 ln | no | not run | partway through the apply |
| 8 | 226 | 1211 ln | no | passed once | owes log; agent died checking a figure |
| 9 | 108 | 867 ln | yes | not run | owes the final gate run |
| 12 | 391 | none | no | not run | 76 edits applied; owes report, gates, log |
| 13 | 325 | 992 ln | yes | not run | owes gates |
| 16 | 362 | 672 ln | yes | passed | owes only the log write-out |
| 17 | 357 | 770 ln | yes | not run | owes two residual claim fixes + gates |
| 5, 10, 15 | 0 | none | no | — | **NOT STARTED** |

## Next task — finish the twelve

Three jobs, in this order. They are independent; run them in parallel again.

1. **Reset and re-apply Module 3.** Its agent died mid-repair of its own
   `apply.py` (a `"""` docstring inside a replacement snippet terminated the
   surrounding raw string). The script is **not idempotent**, so
   `edited/module03.html` may hold a partial apply. Do
   `cp module03.html edited/module03.html`, fix the script, run it once.
2. **Gates + change log** for 4, 7, 8, 9, 12, 13, 16, 17. Most of the work is
   done; what is owed is the nine gates and the `## 6. Changes applied` table.
   Module 12 also owes its report; Module 17 owes two residual claim fixes.
3. **Full pass** for 5, 10, 15 — all ten brief steps.

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
into data.** Calibrate from the tick `<text>` coordinates, invert the mapping,
compare against the model. Carry this into every remaining module — it is
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

- **Cosmetic anatomy leftovers:** m10 wishbone shoulders, m09 fig1 (feet piled
  at one point) and fig13 (stance leg has no knee), m13 any residual detached
  head. Locate by caption; render-verify; gate; commit.
- **A stroke-width gate for `check_svg.py`** would catch the "realism commit"
  failure class mechanically. It lives in the shared `rigorous-explainer` skill,
  so it is a toolchain change, not a module change.
- Two full agent fleets were lost to usage limits mid-run. `autoContinueAtUsage
  Limit: true` is set in `~/.claude/settings.json`, but it did not save the
  subagents — only the lead. Launch fleets early in a limit window.
