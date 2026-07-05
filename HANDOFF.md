# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook. Don't
duplicate content that already lives in the files referenced below — open them.

## Current state (as of latest push)
- **Modules 1–6 are COMPLETE and live** at https://az9713.github.io/biomechanics/ .
  Modules 1–4: §0–§9 (+ 30-problem §9 for M3/M4) + Appendix. Module 5 (Muscles): §0–§10 +
  Appendix. **Module 6 (Tendons, Ligaments, Fascia, and Elastic Energy Storage): §0–§10 +
  Appendix — COMPLETE, latest commit `5741566`.** §0 motivation → §1 collagen/crimp/J-law →
  §2 nonlinear spring → §3 elastic energy → §4 series-elastic MTU (repays M5's rigid-tendon
  debt) → §5 viscoelasticity → §6 Maxwell/KV/SLS → §7 hysteresis/complex modulus → §8
  ligaments/knee four-bar/plantar-fascia arch → §9 three computational labs → **§10 30-problem
  set** (C1–C10 / D1–D10 / K1–K10, each with its own figure; K's genuinely computational +
  Python-verified) + 5 diagnostics + repayment table (→ Modules 9/14/16) → Appendix (grouped
  notation + parameter tables). 11 Propositions, all proved. Full hardening loop passes on all
  six modules. Working tree clean apart from untracked `.ignore/`, `here.sh.txt`, `prompt.txt`.
- **Module 6 build lessons (all already encoded in `CLAUDE.md` + the skill — do not re-litigate):**
  - **Cross-problem numerical consistency is a rigor axis no checker sees.** A §10 K-solution
    printed a tendon resilience (74%) that contradicted C4 / §3 / §9 (~90–93%) on the same page;
    caught only by an adversarial read. When a parameter appears in a boxed result, every
    problem's answer must agree with it — the Appendix parameter table is the ledger to check against.
  - **A model that resists a clean sweep is telling you something.** The §4 hop is a near-passive
    bounce whose fibre is velocity-capped, so amplification/elastic-fraction sweeps came out flat;
    the honest computational results were a rigid-limit root-find (K3) and a resonance optimum (K4).
    Don't force a sweep out of a model that hasn't got one — re-pose the problem.
- **Two conventions Module 5 established — still in force (both in `CLAUDE.md`):**
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
- **Module 6 is DONE, committed & pushed (`5741566`), live.** Next = **Module 7.**
- **Module 7 — draw its plan from `prompt.txt` (Course Structure) + Module 6's forward
  references**, exactly as Modules 3/4/5/6 were scoped. Module 6's §10 repayment table points
  forward to **Module 9** (running/jumping SLIP), **Module 14** (creep-to-rupture, fatigue,
  ageing) and **Module 16** (finite-strain / poroelastic continuum) — check whether Module 7
  in `prompt.txt` is the next in sequence and what earlier modules deferred *to it* (grep the
  built `moduleNN.html` for `Module&nbsp;7` forward-refs). Write `module07-plan.md` first, get it
  approved, then build section-by-section: leaner way (prose in HTML, Python for figures),
  MIT-PhD level, full hardening loop after every edit, **commit only on the user's "commit push."**
  Publish-while-incomplete: link it in `index.html` + `README.md` as soon as it is first committed,
  marked *(in progress)* until complete (drop the marker on completion, as Module 6 just did).
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
