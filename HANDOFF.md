# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook. Don't
duplicate content that already lives in the files referenced below — open them.

## Current state (as of latest push)
- **Modules 1–5 are COMPLETE and live** at https://az9713.github.io/biomechanics/ .
  Modules 1–4: §0–§9 (+ 30-problem §9 for M3/M4) + Appendix. **Module 5 (Muscles as
  Chemo-Electro-Mechanical Actuators): §0–§10 + Appendix** — 63 figures (2 SMIL), a
  **30-problem §10 set** (C1–C10 / D1–D10 / K1–K10, each with its own figure; K's are
  genuinely computational + Python-verified) + 5 diagnostics + repayment table + grouped
  notation/parameter tables. Full hardening loop passes on all five modules. Latest commit
  **`bc0ff18`**; working tree clean apart from untracked `.ignore/` and `prompt.txt`.
- **Two conventions Module 5 established — carry them into Module 6 (both now in `CLAUDE.md`):**
  - **Leaner way:** author section prose DIRECTLY in `moduleNN.html`; use Python only for
    *figures*, injected via `<!--FIG:key-->` markers with the generic `s5/splice_figs.py`.
    **Never author section prose in a Python raw string** — it evades the read-aloud audit +
    `check_prose.py`. (The old Module 3/4/5-§4 `build_secN.py` assembler is the superseded way.)
  - **Audience = MIT-PhD:** computational (K) problems must require simulation / optimization /
    an inverse problem / a sensitivity sweep — NOT plug-in substitution into a boxed formula.
    (Encoded in `CLAUDE.md` "Audience & problem-set standard" and the skill `pedagogy-checklist.md` §8.)
- **Module 5 figure generators were session-transient** (scratchpad `s4..s10/`, `sprob/`, `sk/`)
  and are GONE after clear — the durable record is `module05.html`. To edit a Module 5 figure,
  either edit the committed inline `<svg>` directly or regenerate from the leaner-way pattern
  (a `genN.py` → `figsN.json` → `splice_figs.py` into `<!--FIG:key-->` markers).
- **SVG-subscript gotcha (bit us twice):** Unicode has no subscript c/d/l/v/etc.; write SVG
  `<text>` subscripts as `<tspan baseline-shift='sub' font-size='7'>` (a `fixsub()` helper in the
  generators maps placeholder entities to it). `ₘₐₓ` (max) is the one that *does* exist.

## Other threads this session (not the biomech repo)
- **New personal skill `handoff-after-clear`** created (`~/.claude/skills/`, LOCAL,
  outside this repo) — the durable session-close/resume protocol, distinct from
  `/handoff`. It is DONE and usable. Its **triggering-optimization is parked**;
  status + how to resume in `~/.claude/skills/handoff-after-clear-workspace/STATUS.md`
  (blocked by: `run_loop`'s improve-step needs `ANTHROPIC_API_KEY` this env lacks;
  and a suspected harness artifact in the trigger eval). Not a biomech task.

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
- **Module 5 is DONE, committed & pushed (`bc0ff18`), live.** Next = **Module 6.**
- **Module 6 — draw its plan from `prompt.txt` (Course Structure) + Module 5's forward
  references**, exactly as Modules 3/4/5 were scoped. The load-bearing forward-ref: Module 5
  deferred the **series-elastic (compliant) tendon** — elastic energy storage & return, the
  fibre↔tendon speed difference, and the implicit CE–SE equilibrium solved each timestep — to
  Module 6 (see §7 "Modelling assumption 7.1 (rigid tendon)" and the §10 repayment table in
  `module05.html`). Write `module06-plan.md` first, get it approved, then build section-by-section:
  leaner way (prose in HTML, Python for figures), MIT-PhD level, the full hardening loop after
  every edit, and **commit only on the user's "commit push."** Publish-while-incomplete: link it in
  `index.html` + `README.md` as soon as it is first committed.
- **Parallel/backup track:** the **substance backlog** in `audit-modules.md` — higher-value
  content fixes to earlier modules (M2 torsion section; M1 joint-reaction + low-back number;
  M3 nonholonomic relabel; M4 Hertz-validity caveat).
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
