# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook. Don't
duplicate content that already lives in the files referenced below — open them.

## Current state (as of latest push)
- **Modules 1–4 are COMPLETE and live** at https://az9713.github.io/biomechanics/ .
  Module 4 (Cartilage / Synovial Fluid / Joint Contact Biophysics) finished this
  round: §0–§9 (with the full **30-problem §9**: C1–C10 / D1–D10 / K1–K10) + the
  **Appendix** (notation + parameter tables). No `(in progress)` marker remains.
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
- **Module 5** (muscle actuators / tendons — see `prompt.txt` Course Structure +
  the `index.html` syllabus) is **not started**. Draw its §-by-§ plan from
  `prompt.txt` + Module 4's forward-references (the `<span class="secref">Module N</span>`
  and `§N` promissory notes), exactly as was done for Modules 3 and 4. Then build
  section-by-section.
- If the user asks for something else, that takes precedence over starting Module 5.

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
