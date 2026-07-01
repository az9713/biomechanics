# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook. Don't
duplicate content that already lives in the files referenced below — open them.

## Current state (as of latest push)
- **Modules 1–4 are COMPLETE and live** at https://az9713.github.io/biomechanics/ .
  Module 4 (Cartilage / Synovial Fluid / Joint Contact Biophysics): §0–§9 (with the
  full **30-problem §9**: C1–C10 / D1–D10 / K1–K10) + the **Appendix**. No
  `(in progress)` marker remains.
- **Module 5 (Muscles as Chemo-Electro-Mechanical Actuators) — IN PROGRESS.**
  - Plan **written and approved**: `module05-plan.md` (the §-by-§ spine). Decisions
    locked with the user: **§0–§10 + Appendix** (labs get their own §9,
    captures/misses + problems §10) and the **full 30-problem set** (C1–C10 /
    D1–D10 / K1–K10 + 5 diagnostics) in §10.
  - **§0 (motivation) is COMPLETE and live** (`module05.html`, last commit
    `e3b5682`): Tier-2 shaded-arm hero figure + the neural-drive→activation→force→
    torque pipeline schematic; repays Module 1's "muscle force given" and Module 3's
    blank applied force $Q$. All hardening checks pass. Linked from `index.html`
    (marked *(in progress)*) and `README.md`.
- Everything is committed and pushed to `main` (public repo
  https://github.com/az9713/biomechanics). Working tree is clean apart from
  untracked `.ignore/` and `prompt.txt`.

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
  `scripts/*.py` (hardening tools), `references/*.md`, `assets/template.html`.

## Next task
- **Module 5 §1 — Muscle architecture: the force-producing hierarchy** (fascicles,
  pennation angle $\theta_p$, PCSA, specific tension $\sigma$ → $F_{\max}=\sigma\cdot
  \mathrm{PCSA}$; along-tendon projection $\cos\theta_p$). See `module05-plan.md`
  "§1" for the full scope. Build section-by-section per the plan (§2 length–tension,
  §3 ECC/calcium, … §7 the boxed Hill model, §8 torque, §9 labs, §10 problems).
- **§1 is the first figure-heavy section** — per the style-sign-off rule, build/preview
  **one representative Tier-2 figure (the muscle hierarchy: whole muscle → fascicle →
  fiber → sarcomere) and get it approved** before drawing the rest.
- If the user asks for something else, that takes precedence over continuing Module 5.

## How to work (the essentials — full detail in `CLAUDE.md`)
- **Invoke the `rigorous-explainer` skill** at the start; follow its SKILL.md build loop.
- **Section-by-section.** Build ONE section → report with a short summary + 2
  `★ Insight` bullets → user reviews → commit/push **only on "commit push."**
- **Figures:** compute plot/geometry data with Python in the scratchpad (run in the
  background — numpy startup is slow); Tier-2 shaded for anatomy, flat schematic for
  physics/plots; slim arrows only; reuse a shared `<defs>` block. **Get one
  representative figure per family approved before mass-producing.**
- **Hardening loop after every edit** — `checktex / checklt / check_links /
  verify_dom / check_overlap` all to 0; then `autolink_sections.py`. Never eyeball a
  plot for overlaps; `check_overlap.py` enforces it.
- **Publish-while-incomplete:** when a `moduleNN.html` is committed, keep it linked in
  `index.html` + `README.md` (marked *(in progress)* until complete).

## Suggested skills
- **`rigorous-explainer`** (primary — the whole course is built with it).
