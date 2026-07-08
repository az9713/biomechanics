# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook. Don't
duplicate content that already lives in the files referenced below — open them.

## Current state (as of latest push)
- **Modules 1–8 are COMPLETE and live** at https://az9713.github.io/biomechanics/ .
  Each `moduleNN.html` is self-contained (MathJax + inline SVG/SMIL, no build step) and
  passes the full hardening loop. Latest commit **`7936b0e`** on `main`.
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
- Everything committed and pushed to `main` (https://github.com/az9713/biomechanics).
  Working tree clean apart from **known untracked noise**: `.ignore/` (transcripts),
  `prompt.txt` (source spec — intentionally untracked), `here.sh.txt`, and **Codex
  artifacts** `AGENTS.md`, `CODEX_HANDOFF_REPORT.md`, `MODULE6_MODULE7_PROBLEM_FIGURE_COMPARISON.md`,
  `MODULE7_FIGURE_UPGRADE_PLAN.md`, `module08-preview.png` — **leave these untracked; do not commit.**

## Next task
- **Module 9 — Running and Jumping.** Draw the plan from `prompt.txt` (Course Structure,
  "Module 9") + the forward-references Module 8 makes to it (grep the built `module0[1-8].html`
  for `Module&nbsp;9`): the **spring-mass / SLIP** model, **flight phase**, the **walk→run
  transition** at Fr≈0.5 (M8 §2/§4 explicitly hand this to M9), **impact loading / impulse**,
  **tendon recoil** (repays M6's Achilles energy-storage IOU), **countermovement jump**,
  **stretch-shortening cycle**, **landing mechanics**, **injury risk**. Write
  **`module09-plan.md` first**, get it approved, then build section-by-section (leaner way:
  prose in HTML, Python for figures only), MIT-PhD level, full hardening loop after every edit,
  **commit only on the user's "commit push."** Publish-while-incomplete: link in `index.html`
  (shift the pending line to "Modules 10–17") + `README.md` on first commit, marked *(in progress)*.
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

## Skill upgrades made THIS session (LOCAL — in `~/.claude/skills/rigorous-explainer/`, NOT in this repo)
- **`scripts/check_code.py`** — runs `pycodestyle` on every Python `<pre><code>` block; **fails**
  on E303 (the `<pre>`-preserves-blank-lines spacing bug) and E501. Added to the hardening loop.
- **`scripts/check_probfig.py`** — advisory: flags problem (C/D/K) figures that are neither a drawn
  Tier-2 entity nor a real plot (floating arrows/bare glyph/text). Added to the loop.
- **`SKILL.md`** — (1) PEP8/compact code-authoring rule; (2) **problem-figure exception**: C/D/K
  figures always lead with the recognizable Tier-2 entity (overrides the "physics figures stay
  flat" default), plus a note that `check_probfig` does NOT replace the manual 3-layer semantic audit.
  These matter for every future module's figure + code quality.

## Session-transient scratch (GONE after clear; regenerate from the pattern — durable record is `module08.html`)
Scratchpad dir differs per session. Module 8 figure/lab generators:
- **`fig7lib.py`** — shared Tier-2 helpers (`cap` shaded capsule, `sph` shaded sphere, `rot`,
  `body` posable walking body). Note: an old `leg()` helper drew *upward*; don't reuse it —
  build legs with `cap()` between explicit points.
- **`fig_p8_v2.py`** — the 30 C/D/K problem figures (recognizable entity + anchored variables for
  C/D; small Tier-2 model inset + computation panel for K) → idempotent inline `<figure>` replace
  keyed by `<b>C1.</b>`…`<b>K10.</b>`.
- **`gen_fig67.py`** (joint-power + cost-of-transport plots), **`gen_sec_figs.py`** (§1 gait
  timeline, §8 arm swing, §9 passive walker) — idempotent inline replace by SVG `aria-label`.
- **`clean_labs.py`** — the 4 PEP8 lab code blocks; splices by anchor string.
- All idempotent, all session-transient. To edit a figure: regenerate from these, or edit the
  committed inline `<svg>` in `module08.html` directly.

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
