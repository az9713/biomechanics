# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last handoff written:** 2026-09-07 (editor phase: Modules 1 and 2 applied and
pushed; Modules 3–17 not yet reviewed).

---

## Current state — the EDITOR phase (the anatomy phase is closed)

The course-wide **anatomy regression** is fully fixed (~90 figures, all
gate-checked and render-verified). That phase is done. What is running now is a
**`science-editor` pass, module by module**: read a `moduleNN.html` against the
five-part standard, write a report, then apply it.

| Module | Report | Applied | Commit |
|---|---|---|---|
| 1 | `editor-reports/module01.md` — 19 blocking, 15 style | yes | `3a4dae1` |
| 2 | `editor-reports/module02.md` — 22 blocking, 20 style | yes | `ac93c14` |
| 3–17 | not written | — | — |

Both reports are committed (`b59b44f`) and stay as the record of what was wrong.
Working tree clean apart from the untracked tool dirs `.agents/` and `.codex/`
(local scaffolding — leave untracked, like `mcps/`).

## Next task — the editor pass on `module03.html`

Same two steps, same order:

1. **Report.** Invoke the `science-editor` skill on `module03.html`, read against
   `EDITOR_DOMAIN.md`. Output goes to `editor-reports/module03.md` and must give,
   per defect: `module03.html:LINE`, the quoted text, the fault, and **the full
   replacement HTML**. Extract and run every `<pre><code>` block; check each
   printed number against the prose.
2. **Apply.** See the pipeline below. Then commit and push.

Module 3 is the largest so far (2176 lines, 322 KB) and its §9 holds 30 problems
with figures, so expect a bigger report than Module 2's 22 defects.

## The apply pipeline (proven on Modules 1 and 2 — reuse it)

Write **one re-runnable `apply.py`** in the scratchpad. Do not hand-edit 40 places.

- `rep(old, new, tag)` **asserts the anchor occurs exactly once**, then replaces;
  the script logs every tag so you can check the log against B1..Bn.
- New/repaired SVG bodies come from a `genfigs.py` → `figs.json`; `apply.py`
  splices them in. Prose stays in the HTML, figures come from Python.
- `git checkout -- moduleNN.html` is the reset. The loop is: edit `genfigs.py` →
  rerun → `git checkout` → `python apply.py` → gates.
- Run it against a **pristine** file. It is not idempotent.

**Three traps that cost real time on Modules 1 and 2:**
- In a Python **raw** string `\'` keeps the backslash, so `r'…\'…'` never matches
  the file. This crashed `apply.py` silently — it died before its single
  `write_text`, leaving the file untouched while the logs looked plausible.
- A regex that maps `\beta`→`beta` **before** stripping `\\[a-zA-Z]+` glues
  `\sin`+`beta` into `\sinbeta` and deletes it. Map function names first.
- `check_overlap.py` tests text against curves and dashed lines, **not text
  against text**. Legend-on-label collisions are invisible to it — look at the
  renders.

## Where to read things (reference, don't re-derive)

- `editor-reports/*.md` — what was wrong with each module and the exact fix.
- `EDITOR_DOMAIN.md` — the domain brief the `science-editor` skill reads.
- `CLAUDE.md` — standing conventions: build loop, the nine hard gates, git and
  publish, figure style, math-in-HTML gotchas, the K-problem depth standard.
- `ANATOMY_AUDIT.md` — the closed anatomy phase: defect register, four fix
  recipes, and the safety caveats (thick `#c98a5e` limb lines, figures located by
  caption not index, transformed `<g>`s).
- `anatomy_kit/README.md` — `body_group` / `capsule` / `sphere` / `head`.
- `prompt.txt` — course structure, source of truth.

## How to work (essentials — full detail in `CLAUDE.md`)

- **Nine hard gates after every edit pass**, all zero: `checktex`, `checklt`,
  `check_links`, `check_svg`, `check_code`, `verify_dom`, `check_overlap`,
  `check_frame`, `check_bodyprop`. Then read the advisories (`check_prose`,
  `check_proofs`, `check_probfig`).
- **Then render-verify with `shoot.py` and look at the PNGs.** Every real defect
  found in the last two modules — a wedge cut on the wrong diagonal, a legend
  printed through a number, a curve running off the top — passed all nine gates.
  Gates are necessary and not sufficient.
- **Commit + push per module**, as `az9713` / `az9713@users.noreply.github.com`,
  with the standard trailer block. Public repo — never reintroduce the private
  `az9713@yahoo.com` email (it still lives in git history; a rewrite needs
  filter-repo plus a force-push, so coordinate with the user first).
- Subagents doing an apply should run **no writing git command**; the lead
  commits after re-running the static gates.

## Open items (small, not blocking)

- **Cosmetic anatomy leftovers** (not incorrect anatomy): m10 wishbone shoulders,
  m09 fig1 (feet piled at one point) and fig13 (stance leg has no knee), m13 any
  residual detached head. Locate by caption; render-verify; gate; commit.
- **A stroke-width gate for `check_svg.py`** was suggested while fixing the
  Module 2 black bars — it would catch the "realism commit" failure class
  mechanically. It lives in the shared `rigorous-explainer` skill, so it is a
  change to the toolchain, not to a module.
- `autoContinueAtUsageLimit: true` is now set in `~/.claude/settings.json`, so a
  usage limit no longer ends a session's work — it waits and continues.
