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
  - **§0–§3 are COMPLETE and live** (`module05.html`). **§3 (excitation–contraction
    coupling → calcium → activation)** = EC-coupling pathway NMJ→DHPR/RyR→SR→troponin
    (Fig. 9, mechanical gating — NOT cardiac CICR), troponin/tropomyosin switch (Fig. 10),
    **Def 3.1 activation** $a$∈[0,1] + **Prop 3.1** cooperative steady-state
    $a_\infty=[Ca]^n/(Ca_{50}^n+[Ca]^n)$ (Fig. 11 sigmoid), and the **single twitch**
    (Fig. 12): fast Ca²⁺ driver vs slow activation $a$ (force ∝ $a$), reaching only ~0.22
    vs tetanic ceiling ~0.73. KEY: $a$ is the SLOW variable force tracks; $a$ relaxes
    toward $a_\infty$ via $\dot a=(a_\infty-a)/\tau_a$ = §5's ODE in miniature (advisor
    fix — avoids an $a$-means-two-things contradiction with §5/§7). Validation: twitch
    time-to-peak ~25 ms, half-relax ~40 ms (fast-fibre range). §3 figure pipeline in
    scratchpad: `gen3.py`→`d3.json`, `emit3.py` (twitch+sigmoid), `emit_schem3.py`
    (ecc+troponin), `build_sec3.py` (idempotent splice). Commit `510552e`. Full loop passes.
  - **§0 (motivation), §1 (muscle architecture), and §2 (sarcomere → length–tension
    law):** §0 = Tier-2 arm hero +
    neural→activation→force→torque pipeline; §1 = the muscle-hierarchy zoom (Fig. 3),
    pennation force triangle (Fig. 4), boxed **Proposition 1.1**
    $F_{\max}=\sigma\,\mathrm{PCSA}\cos\theta_p$, parameter table, and a §0 validation;
    **§2** = sliding-filament model, four-state crossbridge cycle (Fig. 5, 1 ATP/cycle,
    rigor-mortis hook), overlap-at-4-lengths panels (Fig. 6), boxed **Proposition 2.1**
    length–tension law $f_L(\ell)$ + computed curve (Fig. 7), and the **module's first
    SMIL** — a breathing sarcomere with a synced operating-point dot (Fig. 8). Filament
    dims: thick 1.60 / thin 1.30 / bare-zone 0.10 µm → landmarks $\ell_0$=2.70, zeros
    1.27 & 4.20 µm (Gordon–Huxley–Julian 1966). Added the `prefers-reduced-motion` guard
    (file predated it). Commit `e7cd0dd`. Full hardening loop passes.
    - **§2 figure pipeline (scratchpad, session-transient):** `gen2.py` (all geometry →
      `d2.json`: f_L breakpoints, SMIL keyframes, per-panel filament coords), `emit.py`
      (panels), `emit2.py` (f_L curve), `emit_smil.py` (SMIL), `build_sec2.py`
      (assembles prose + the 4 figures, idempotent splice between the last §1 paragraph
      and `<script>`). `sample.py` = playwright transform-sampler that verifies SMIL
      actually animates. Durable record is `module05.html`, not these.
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
- **Module 5 §4 — Motor units, recruitment, and rate coding.** Motor unit = one
  motoneuron + its fibres. **Henneman size principle** (recruit small→large), **rate
  coding**, and twitch **summation → unfused → fused tetanus**. Whole-muscle neural
  drive $u(t)\in[0,1]$ = recruitment × firing rate — the lumped command §5 turns into
  activation $a$. Pick up the §3 hooks: the single twitch only reaches ~0.22 of the
  tetanic ceiling (so fire fast → twitches sum), and the fast/slow fibre-type spread.
  See `module05-plan.md` "§4". **This is the module's 2nd SMIL** — animate twitch
  summation building to a fused tetanus (drive the summed-force keyframes from the §3
  twitch shape so movie and physics agree). Then §5 (activation ODE, boxed) … §10.
- **SMIL is established** (§2 Fig. 8 + the `prefers-reduced-motion` guard are in place).
  Reuse `sample.py` (playwright transform-sampler) to verify any new animation actually
  moves before writing prose around it. §3's twitch integrator (`gen3.py`) is the basis
  for the §4 summation keyframes.
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
