# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook. Don't
duplicate content that already lives in the files referenced below — open them.

## Current state (as of latest push)
- **Modules 1–4 are COMPLETE and live** at https://az9713.github.io/biomechanics/ .
  Each has the full §0–§9 (+ 30-problem §9 for M3/M4) + Appendix.
- **Module 5 (Muscles as Chemo-Electro-Mechanical Actuators) — IN PROGRESS.**
  - Plan **written and approved**: `module05-plan.md`. Locked: **§0–§10 + Appendix**
    (labs = §9; captures/misses + problems = §10) with the **full 30-problem set**
    (C1–C10 / D1–D10 / K1–K10 + 5 diagnostics) in §10.
  - **§0 (motivation) and §1 (muscle architecture) are COMPLETE and live**
    (`module05.html`): §0 = Tier-2 arm hero + neural→activation→force→torque
    pipeline; §1 = the muscle-hierarchy zoom (Fig. 3), pennation force triangle
    (Fig. 4), boxed **Proposition 1.1** $F_{\max}=\sigma\,\mathrm{PCSA}\cos\theta_p$,
    parameter table, and a §0 validation. Linked from `index.html` *(in progress)* +
    `README.md`. Full hardening loop passes.
- **Course-wide improvements landed this round (all Modules 1–5):**
  - **Every figure is auto-numbered "Fig. N"** (CSS counter in each module's style).
  - **All 51 `check_svg` hard issues fixed in Modules 1–4** — SVG `<text>` labels now
    use Unicode subscripts / `<tspan baseline-shift>` (no literal `_`/`^`), and
    Module 4's 11 malformed `viewBox` are corrected. All four pass the full loop
    (checktex/checklt/check_links/check_svg/verify_dom/check_overlap = 0).
  - **The `rigorous-explainer` skill was upgraded** (LOCAL — under
    `~/.claude/skills/`, NOT in this git repo, so it won't appear in `git status`):
    new `scripts/check_svg.py` (now in the hardening loop), a `prefers-reduced-motion`
    guard + problem-set skeleton in `assets/template.html`, and new rules in
    `references/pedagogy-checklist.md` + `figures-and-animation.md`. See
    `skill-change-list.md` for the full list.
- Everything (repo side) is committed and pushed to `main`
  (https://github.com/az9713/biomechanics). Working tree clean apart from untracked
  `.ignore/` and `prompt.txt`.

## Where to read things (reference, don't re-derive)
- **`CLAUDE.md`** (repo root) — authoritative conventions: build loop, hardening
  loop, figure rules, git/publish, publish-while-incomplete. **Read it.**
- **`module04-learnings.md`** (repo root) — the build playbook from Module 4: the
  generator/assembler figure pipeline, what each hardening check catches, the bugs
  the toolchain surfaced, math-in-HTML gotchas. **Read before any figure-heavy work.**
- **`module04-plan.md`** — the §-by-§ plan template (how Module 4 was scoped).
- **`prompt.txt`** — the original course spec; the source of truth for scope/structure
  of all 17 modules.
- **`svg-figure-tiers.md`** — figure-style decision doc.
- **Skill:** `C:\Users\simon\.claude\skills\rigorous-explainer\` — SKILL.md,
  `scripts/*.py` (hardening tools incl. the new `check_svg.py`), `references/*.md`,
  `assets/template.html`.
- **Audit + planning docs (this round):** `audit-modules.md` (per-module quality
  findings for all 5 modules — the **substance backlog**: e.g. M2 torsion section,
  M1 joint-reaction/low-back numbers, M3 nonholonomic fix), `check-svg-fixlist.md`
  (label/viewBox fixes — DONE), `skill-improvements-from-audit.md` +
  `skill-change-list.md` (skill upgrades — DONE).

## Next task
- **Module 5 §2 — The sarcomere: crossbridges and the length–tension law.**
  Sliding-filament model; actin–myosin crossbridge cycle (attach → power-stroke →
  detach, 1 ATP/cycle); active force ∝ filament overlap → derive the piecewise
  **length–tension curve** $f_L(\ell)$ (ascending / plateau / descending) from
  overlap geometry, **boxed**. Validate: plateau near optimal sarcomere length
  $\ell_0\approx2.7\ \mu\mathrm m$, force → 0 near ~1.27 and ~4.2 µm. See
  `module05-plan.md` "§2". Then continue §3 (ECC/calcium) … §10 per the plan.
- **§2 is the natural first SMIL animation** — animate the sliding filaments /
  overlap changing with length; the §1 sarcomere inset (Fig. 3) is the static
  figure it should animate. Compute overlap geometry in Python; keyframes = physics.
- Continue **section-by-section**; report each with a summary + 2 `★ Insight`
  bullets; **commit only on the user's "commit push."**
- **Parallel track (optional, separate from building §2):** the **substance backlog**
  in `audit-modules.md` — the higher-value content fixes (M2 torsion; M1 joint
  reaction + low-back number; M3 nonholonomic relabel; M4 Hertz-validity caveat).
  These are content changes, not the label/skill work already done.
- If the user asks for something else, that takes precedence.

## How to work (the essentials — full detail in `CLAUDE.md`)
- **Invoke the `rigorous-explainer` skill** at the start; follow its SKILL.md build loop.
- **Section-by-section.** Build ONE section → report with a short summary + 2
  `★ Insight` bullets → user reviews → commit/push **only on "commit push."**
- **Figures:** compute plot/geometry data with Python in the scratchpad (run in the
  background — numpy startup is slow); Tier-2 shaded for anatomy, flat schematic for
  physics/plots; slim arrows only; reuse a shared `<defs>` block. **Get one
  representative figure per family approved before mass-producing.**
- **Hardening loop after every edit** — `checktex / checklt / check_links /
  check_svg / verify_dom / check_overlap` all to 0; then `autolink_sections.py`.
  Never eyeball a plot for overlaps; `check_overlap.py` enforces it. **Note:**
  `check_svg` fails on literal `_`/`^` in `<text>` and bad `viewBox` — use Unicode
  subscripts or `<tspan baseline-shift>`; and `baseline-shift="sub"` grows a label
  box downward, so re-run `check_overlap` after adding subscripts near a ref line.
- **Publish-while-incomplete:** when a `moduleNN.html` is committed, keep it linked in
  `index.html` + `README.md` (marked *(in progress)* until complete).

## Suggested skills
- **`rigorous-explainer`** (primary — the whole course is built with it).
