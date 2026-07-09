# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook. Don't
duplicate content that already lives in the files referenced below — open them.

## Current state (as of latest push)
- **Modules 1–9 are COMPLETE and live** at https://az9713.github.io/biomechanics/ .
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
- **Agent team for the build loop (NEW this session, commit `d0d12b8`).** A reviewer agent
  now sits between "hardening scripts pass" and "user review": **`.claude/agents/rigor-reviewer.md`**
  — a read-only (Read/Grep/Glob/Skill; **NO** Write/Edit/Bash) independent judge of the four things
  the scripts can't check (rigor parity, read-aloud prose, K-depth, self-containment).
  **Calibrated & APPROVED** against Module 8 (sharp — no false alarms on accepted work,
  rigor-parity sensitivity confirmed on a §5 injection). Full record: memory
  `rigor-reviewer-calibration.md`. Design rationale in repo root: `when-to-spawn-a-subagent.md`
  + `building-a-claude-code-agent.md`.
- Everything committed and pushed to `main` (https://github.com/az9713/biomechanics);
  local `d0d12b8` == remote. `prompt.txt` and the Codex docs (`AGENTS.md`, `CODEX_HANDOFF_REPORT.md`,
  `MODULE6_MODULE7_PROBLEM_FIGURE_COMPARISON.md`, `MODULE7_FIGURE_UPGRADE_PLAN.md`) are **now
  committed** (`d0d12b8`). Working tree clean; `.ignore/`, `here.sh.txt`, `module08-preview.png`
  are now **gitignored** (scratch/preview — leave them).

## Next task
- **Module 9 — Running and Jumping — COMPLETE & live.** All of §0–§11 + Appendix
  built, each hardened to 0 and rigor-reviewer-approved, committed and pushed. Live at
  https://az9713.github.io/biomechanics/module09.html; wired into `index.html` +
  `README.md` (no longer *(in progress)*; pending line "Modules 10–17"). Spine: §0
  motivation → §1 gait/duty factor → §2 SLIP → §3 GRF (single vs double hump) → §4 flight
  + Froude ceiling → §5 impulse-momentum → §6 jump height → §7 stretch-shortening/tendon
  recoil (repays M6) → §8 landing (1/d) → §9 impact/injury (mechanics-first, repays M2) →
  §10 four Python labs → §11 30 problems + diagnostics + limitations + repayment →
  Appendix (notation + parameters). Latest commit at handoff time: run `git log -1`.
  - **K-DEPTH carry-forward RESOLVED:** the reviewer's K-depth sensitivity was validated on
    a scratch probe (flagged a plug-in K, passed genuine sim/opt/inverse ones) — see memory
    `rigor-reviewer-calibration.md`. It passed all 10 §11 K problems.
- **NEXT = Module 10 — Balance, Stability, Perturbation Recovery, and Sensorimotor
  Control.** Draw the plan from `prompt.txt` ("Module 10") + the forward-references Modules
  7–9 make to it (grep `module0[1-9].html` for `Module&nbsp;10`): perturbed standing/running,
  slips/trips/recovery steps, margin of stability / XcoM, sensory fusion and reflex delay,
  reactive vs predictive control. Write `module10-plan.md` first, get it approved, then build
  section-by-section (leaner way: prose in HTML, Python figures only), MIT-PhD level, full
  hardening loop every edit, dispatch `rigor-reviewer` after scripts hit 0. Publish-while-
  incomplete on first commit.
- **Use the reviewer in the build loop:** after a section's hardening scripts hit 0, dispatch
  `rigor-reviewer` for an independent judgment pass **before** user review; fix its findings
  (bounded rounds), then report to the user. **Two carry-forward items:** (1) it must run as the
  **registered** agent — this session only tested it via a general-purpose *fallback* because the
  file was created mid-session; a fresh session loads `.claude/agents/rigor-reviewer.md` properly
  and enforces its read-only tools. (2) **K-depth sensitivity is UNTESTED** — before trusting it on
  the M9 problem set, inject one deliberately plug-in K problem into a scratch copy and confirm the
  reviewer flags `K-DEPTH: fail`.
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

## Session-transient scratch (GONE after clear; durable record is `module09.html`/`module08.html`)
Scratchpad dir differs per session. **Module 9 is COMPLETE** — to edit an M9 figure, just edit
the committed inline `<svg>` in `module09.html` directly, or regenerate from these patterns:
- **Per-section figure generators** (each emits an `<svg>`/`<figure>` body, spliced into the HTML):
  `fig0.py` (§0 running-bounce sequence), `fig1.py` (§1 gait timeline), `fig_slip.py` (§2 SLIP
  schematic), `fig_grf.py` (§3 GRF; uses `slip_stance.py`/`slip_sym.py`→`grf.json`/`grf5.json`),
  `fig_flight.py` (§4), `fig_impulse.py` (§5), `fig_jump.py`+`jump.py` (§6), `fig_tendon.py`+
  `fig_econ.py`+`tendon.json` (§7), `fig_land.py`+`land.json` (§8), `fig_impact.py`+`impact.json`
  (§9). Labs: `lab1_slip.py`…`lab4_econ.py` (§10, all PEP8).
- **`fig_prob9.py`** — the 30 §11 problem figures via a REUSABLE generator (shared `body`/`coil`/
  `slip`/`plot`/`kfig` helpers) → `prob9.json` keyed `C1…K10`. Splice pattern: replace the 30
  `<figure style="margin:.5rem 0">…</figure>` blocks **in document order** (C1…C10,D1…D10,K1…K10),
  then strip literal `_` inside `<text>` (`re.sub(r'(<text[^>]*>)([^<]*)(</text>)', …)`) — SVG text
  can't use `$…$`, and `check_svg` hard-fails on a literal `_`/`^` in a label.
- **Gotcha that bit repeatedly:** never route `\`-macros (`\to \rm \approx \tfrac`) through a
  **double-quoted** `python3 -c "…"` shell arg — bash collapses `\\`→`\`, then Python turns `\t`→TAB,
  `\r`→CR, `\a`→BEL and corrupts the math. Use a `<<'PY'` heredoc, the Write/Edit tools, or a
  `lambda` replacement (not a regex template, which reinterprets `\i`,`\d`). `checktex` catches the
  stray control char.

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
