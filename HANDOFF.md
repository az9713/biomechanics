# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last handoff written:** 2026-09-07 (editor phase: Modules 1 and 2 applied and
pushed; the Module 3 REPORT is written but NOT YET APPLIED; Modules 4–17 queued.
The user has asked for the editor pass on ALL remaining modules, 3 through 17.)

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
| 3 | `editor-reports/module03.md` — 13 blocking, 11 style | **NO** | report only |
| 4–17 | not written | — | — |

Both reports are committed (`b59b44f`) and stay as the record of what was wrong.
Working tree clean apart from the untracked tool dirs `.agents/` and `.codex/`
(local scaffolding — leave untracked, like `mcps/`).

## Next task — APPLY `editor-reports/module03.md`, then report on `module04.html`

The Module 3 report is done and committed. It was written against a full
re-implementation of the §7.4 lab, so its numbers are computed, not recalled.
**Step 1 is to apply it** with the pipeline below, then commit, push and gate.
**Step 2 is the Module 4 report**, then Modules 5 through 17, one per session.

### What the Module 3 report found (13 blocking, 11 style)

The arguments are sound — Theorem 3.1, Proposition 3.2, (4.1) and (6.1) all carry
real proofs and all check. The damage is in the numbers:

- **B1** K2's five numbers reproduce from no run of the model (rail $R_s$ 19.7 N vs
  a computed 32.6 N; wall $R_s$ 20.6→26.3 N vs a computed 57.9→187.3 N). Full
  replacement with verified numbers is in the report.
- **B2** Two mutually inconsistent elbow examples: §4.1 uses Module 1's reference
  human (3 cm arm, 630 N, 566 N); D2 (`:1928`, `:1931`) and the Appendix (`:2131`)
  use a 5 cm arm and 401 N / 336 N. The Appendix records only the wrong one.
- **B3** §9.4 claims every number was produced by running the code. The §7.4 lab
  computes $R_s,R_e,\lambda_3$ and never prints them, and 5 of the 10 K snippets
  call names defined nowhere (`solve_kkt`, `release_pose`, `Rs_history`,
  `time_of_first_turning_point`). Running all 11 blocks gives 5 `NameError`s.
- **B4** A live `<a>` tag sits inside a `<pre><code>` block at `:1989`.
- **B5** §4.3 gives the leaned hip load as 1.3 W (plot) and 1.1 W (caption).
- **B6** The cane claim is qualitative with a bare "~1 body weight". Verified: a
  0.15 W cane at 0.30 m removes 1.05 W. Arithmetic supplied.
- **B7** K10's four forces are unreproducible and their ordering (wrist 11 N above
  elbow 2 N) inverts §7.5's own proximal-carries-more finding. Computed with the
  Appendix's own $L_3,m_3$: 19.1 / 5.3 / 2.9 / 11.6 N.
- **B8** K9 says 15× and 1.5e-5 m; computed 21× and 2.2e-5 m.
- **B9** §5.3's stated ν≈0.5 gives $E^*=6.67$ MPa, not the stated 6; ν_bone is
  never given. The fix also *derives* §5.1's asserted $A_c≈10$ cm² (Hertz gives
  a=17.9 mm → 10.1 cm²).
- **B10** ~12 bare empirical numbers with no table row (β=55°/22°, both moduli,
  the damage threshold — drawn as both "15" and "15–25" MPa, R_eff, 3–5 W gait,
  ~240 body DOF). Ten Appendix rows supplied.
- **B11** α and $a$ each carry two or three meanings; the Appendix flags neither.
  Rename the Baumgarte gains to γ_d, γ_p.
- **B12** (6.1) silently assumes a frictionless rigid socket, while μ≈0.005 sits
  unused in the Appendix. The two gaps close each other.
- **B13** §6.2's mobility curve is captioned "(computed)" with no equation.

### Verification assets (regenerate; scratchpad is session-transient)

`m03/lab.py` re-implements §7.4 as `run(L1,L2,m1,m2,mL,g,yh,amp,a,b,dt,nstep,
wall,xw) -> dict of arrays`. It reproduces the module exactly: W_L=34.335 N,
R_s 11.64 N at release and 32.61 N peak (ratio 2.80), contact peak 22.32 N and
min 6.21 N, R_e peak 11.61 N, x2 0.358→-0.027 m, max|g| 1.03e-6 m. `verify.py`
sweeps K1–K9; `k2k10.py` does the wall case and a 3-link version; `hertz.py`
does §5 and the cane. Rebuild these before applying, and re-check any number.

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
