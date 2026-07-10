# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook. Don't
duplicate content that already lives in the files referenced below — open them.

## Current state (as of latest push)
- **Modules 1–10 are COMPLETE and live** at https://az9713.github.io/biomechanics/ .
  Each `moduleNN.html` is self-contained (MathJax + inline SVG/SMIL, no build step) and
  passes the full hardening loop. Latest module-content commit **`d19e434`** on `main`
  (this handoff commit only adds a `.gitignore` entry + refreshes this file).
  - **Module 7** (Standing, Posture, Load Bearing): §0–§10 + Appendix; delayed-PD inverted
    pendulum, 15 proved props, SMIL sway animation, 30-problem set. Commit `949f40f`;
    `.nojekyll` deploy fix `d04089e`.
  - **Module 8** (Walking Biomechanics): §0–§12 + Appendix; controlled-falling inverted
    pendulum → Froude → compass-gait impact map → step-to-step transition + push-off →
    inverse-dynamics joint power → energetics → arm swing → passive dynamic walking →
    older-adult falls (physics/chem/bio stack) → 4 labs → 30-problem set → Appendix.
    11 proved props; every section has a figure; all plots computed.
    - **Built by elevating a prior Codex draft** (thin rigor + placeholder figures) to the M7
      standard, then two follow-up fixes this session: **(a)** relabeled the 4 lab code blocks
      to PEP8/compact (commit `9b326a7`); **(b)** rebuilt all 30 C/D/K problem figures to the
      3-layer semantic-clarity standard (commit `7936b0e`).
- **Agent team for the build loop (NEW this session, commit `d0d12b8`).** A reviewer agent
  now sits between "hardening scripts pass" and "user review": **`.claude/agents/rigor-reviewer.md`**
  — a read-only (Read/Grep/Glob/Skill; **NO** Write/Edit/Bash) independent judge of the four things
  the scripts can't check (rigor parity, read-aloud prose, K-depth, self-containment).
  **Calibrated & APPROVED** against Module 8 (sharp — no false alarms on accepted work,
  rigor-parity sensitivity confirmed on a §5 injection). Full record: memory
  `rigor-reviewer-calibration.md`. Design rationale in repo root: `when-to-spawn-a-subagent.md`
  + `building-a-claude-code-agent.md`.
- Everything committed and pushed to `main` (https://github.com/az9713/biomechanics); local ==
  remote. Working tree clean apart from local scratch (`.ignore/`, preview PNGs) and the
  **gitignored `claude-transcripts/`** — that folder is per-project transcript backups written by
  the `/sync-transcripts` skill (global infra, recorded in MMS memory; NOT biomechanics-repo state).

## Next task
- **Module 10 — Balance, Stability, Perturbation Recovery, and Sensorimotor
  Control — COMPLETE & live.** Built end-to-end this session (autonomous `/goal`
  run): §0–§11 + Appendix, committed and pushed (latest `d19e434`), live at
  https://az9713.github.io/biomechanics/module10.html and wired into `index.html`
  (pending line now "Modules 11–17") + `README.md`. Spine: §0 motivation (balance =
  active feedback under delay+noise) → §1 margin of stability / XcoM (critical
  impulse J=mω₀b) → §2 state-space controller + controllability → §3 sensors as
  measurement models + observability → §4 delayed-feedback DDE + stability island
  (τ_c≈137 ms, inside the human loop) → §5 stochastic sway + Lyapunov variance → §6
  Kalman fusion + delay predictor → §7 recovery ladder ankle→hip→step + capture
  placement → §8 slips vs trips → §9 aging as parameter drift → §10 four Python labs
  (all verified, PEP8) → §11 30 problems (K-depth all pass) + diagnostics +
  limitations + repayment → Appendix. Every proposition proved; all figures computed
  (figlib.py poser + Plot helper, session-transient in scratchpad); full hardening
  loop to 0.
  - **Rigor-reviewer: 3 parallel passes (§0–4, §5–9, §10–11 K-depth), all addressed.**
    R3 verdict READY (all 10 K problems pass K-depth). R1 caught one real correctness
    bug — the §4 "period near 4τ" heuristic was quantitatively wrong (fixed to the
    phase-margin-erosion picture). R2 essentially clean (one H/L symbol nit, fixed).
    Nits on Lab B/K2 prose, Lab D framing, a caption garden-path, K8 anchoring — all fixed.
    - **Post-completion fixes:** clipped x-axis titles in 13 problem figures (viewBox too short
      for the `y0+30` axis title) → content-aware figure heights (commit `6c3ec57`); then
      **hardened `check_frame.py` to HARD-fail on figure CLIPPING** (content past the viewBox
      edge — no other check saw it), which caught 2 more real clips (K3 s-plane poles off-scale,
      fig8 top) — commit `d19e434`. SKILL.md + CLAUDE.md updated for the clip gate.
- **NEXT = Module 11 — Reaching, Waving, Holding, Gripping, and Manipulation.**
  Draw the plan from `prompt.txt` ("Module 11", line ~699) + forward-refs Modules
  1–10 make to it. Same build loop: plan → section-by-section (prose in HTML, Python
  figures only) → hardening loop every edit → dispatch `rigor-reviewer` after scripts
  hit 0 → publish-while-incomplete on first commit.
- **Use the reviewer in the build loop (for Module 11):** after a section's hardening scripts hit
  0, dispatch `rigor-reviewer` (registered, read-only Read/Grep/Glob/Skill) for an independent
  judgment pass on the four things scripts can't check (rigor parity, read-aloud prose, K-depth,
  self-containment); fix findings in bounded rounds, then report. Confirmed effective on M10 (3
  parallel passes; K-depth validated on all 10 K problems; caught a real §4 correctness bug the
  scripts missed). For a big module, run it in a few section-group passes in parallel.
- **Parallel/backup track:** the **substance backlog** in `audit-modules.md` (M2 torsion section,
  M1 joint-reaction/low-back number, M3 nonholonomic relabel, M4 Hertz-validity caveat).
- If the user asks for something else, that takes precedence.

## Where to read things (reference, don't re-derive)
- **`CLAUDE.md`** (repo root) — authoritative conventions: build loop, hardening loop, figure
  rules, git/publish, publish-while-incomplete. **Read it.**
- **`prompt.txt`** — original course spec; source of truth for scope/structure of all 17 modules.
- **`module04-learnings.md`** — build playbook (generator/assembler figure pipeline, what each
  hardening check catches, math-in-HTML gotchas). Read before figure-heavy work.
- **`module04-plan.md` … `module08-plan.md`** — the §-by-§ plan templates.
- **`audit-modules.md`** — the substance backlog for earlier modules.
- **Skill:** `C:\Users\simon\.claude\skills\rigorous-explainer\` — SKILL.md, `scripts/*.py`
  (hardening tools), `references/*.md`, `assets/template.html`.
- **`.claude/agents/rigor-reviewer.md`** — the reviewer agent; **`building-a-claude-code-agent.md`**
  + **`when-to-spawn-a-subagent.md`** (repo root) — how the agent team works and when a subagent is
  justified. Memory `rigor-reviewer-calibration.md` — its approved-for-use status + open K-depth item.

## Skill upgrades made THIS session (LOCAL — in `~/.claude/skills/rigorous-explainer/`, NOT in this repo)
- **`scripts/check_code.py`** — runs `pycodestyle` on every Python `<pre><code>` block; **fails**
  on E303 (the `<pre>`-preserves-blank-lines spacing bug) and E501. Added to the hardening loop.
- **`scripts/check_probfig.py`** — advisory: flags problem (C/D/K) figures that are neither a drawn
  Tier-2 entity nor a real plot (floating arrows/bare glyph/text). Added to the loop.
- **`SKILL.md`** — (1) PEP8/compact code-authoring rule; (2) **problem-figure exception**: C/D/K
  figures always lead with the recognizable Tier-2 entity (overrides the "physics figures stay
  flat" default), plus a note that `check_probfig` does NOT replace the manual 3-layer semantic audit.
  These matter for every future module's figure + code quality.
- **`scripts/check_frame.py`** (Module-10 session) — now **HARD-fails on figure CLIPPING** (content
  spilling past the `<svg viewBox>` edge and cut off by the browser), not just wasted margin. No
  other check saw clipping (it's outside the box — not a `<`/`>`/`_`, overlap, or margin issue); it
  shipped as clipped x-axis titles in 13 M10 problem figures. Also catches off-scale computed points
  (an s-plane pole placed off-axis). Lesson baked into SKILL.md + repo `CLAUDE.md`: size viewBoxes to
  content or trust this gate. Hardening loop is now 9 checks.

## Session-transient scratch (GONE after clear; durable record is the committed `moduleNN.html`)
Scratchpad dir differs per session. **Module 10 is COMPLETE** — to edit an M10 figure, edit the
committed inline `<svg>` in `module10.html` directly, or regenerate from these patterns:
- **`figlib.py`** — shared helpers: a posable Tier-2 `body(hipx,hipy,lean,scale,step,arms)` (capsule
  limbs + sphere joints + head, returns svg + COM + ankle coords) and a `Plot` class (data→SVG
  polyline mapping + axes). Reused by every M10 figure generator.
- **Per-figure generators** (each emits a `<figure>` body → `.txt`/JSON, spliced into markers in the
  HTML): `fig0.py` (perturbed standing ξ-in/out), `fig1.py` (margin), `fig2.py` (phase portrait —
  computed saddle vs spiral), `fig3.py` (sensor map), `fig4.py` (stability island + DDE traces),
  `fig5.py` (stochastic sway), `fig6.py` (Kalman fusion), `fig7.py` (recovery ladder), `fig8.py`
  (slip/trip), `fig9.py` (aging), `fig10.py` (Lab-A result). `labs.py`+`build_labs.py` (4 lab code
  blocks, PEP8-verified), `verify_K.py` (K3/K4/K6/K7/K8/K10 numbers).
- **`prob_fig.py`** — the 30 §11 problem figures via a reusable generator (mini `body`/`Plot`/
  `sensor_head`/`s_plane`/`gaussian_fusion` helpers) → `prob.json` keyed `C1…K10`. Splice: replace the
  30 `<figure style="margin:.5rem 0">…problem figure…</figure>` blocks in document order. **Key
  gotchas relearned:** SVG `<text>` can't use `$…$` or literal `_`/`^` (`check_svg` hard-fails —
  use `<tspan baseline-shift="sub">` or Unicode); `svg()` computes a **content-aware viewBox height**
  so axis titles at `y0+30` don't clip (and `check_frame` now HARD-fails clipping); use `find -printf`
  / one Python call, not per-file subprocess loops (MSYS fork is ~100× slower).
- **Gotcha (unchanged):** never route `\`-macros through a **double-quoted** `python -c "…"` shell arg
  (bash `\\`→`\`, then Python `\t`→TAB etc. corrupts math). Use a `<<'PY'` heredoc / Write-Edit tools /
  a `lambda` replacement (not a regex template). `checktex` catches the stray control char.

## How to work (essentials — full detail in `CLAUDE.md`)
- **Invoke `rigorous-explainer`** at the start; follow its SKILL.md build loop.
- **Section-by-section:** build ONE section → report + 2 `★ Insight` bullets → user reviews →
  commit/push **only on "commit push."**
- **Figures:** Tier-2 shaded for anatomy, flat/computed for physics/plots — BUT **problem-set
  C/D/K figures always lead with the recognizable Tier-2 entity** (this session's fix). Compute
  geometry/plot data in Python (background runs — numpy startup is slow); slim arrows anchored to
  the structure; reuse the shared `<defs>` block. Get one representative figure approved before
  mass-producing.
- **Hardening loop after every edit** — all to 0: `checktex / checklt / check_links / check_svg /
  check_overlap / verify_dom / check_proofs / check_code / check_probfig`; then `autolink_sections.py`.
- **Deploy:** `.nojekyll` is committed, so pushes deploy clean. If a Pages build stalls,
  `gh api -X POST repos/az9713/biomechanics/pages/builds` nudges a fresh one.
- **Gotcha (bit hard this session):** never route `\`-heavy Python (`\approx`, `\alpha`, `\tau`)
  through a Bash-tool heredoc — `\a`→BEL etc. corrupts the file. Author such scripts with the
  Write tool using raw strings.
