# Codex Handoff Report — Quantitative Human Musculoskeletal Science

Generated: 2026-07-05  
Workspace: `C:\Users\simon\Downloads\human_movement_science_me`  
Repo: `https://github.com/az9713/biomechanics`  
Live site: `https://az9713.github.io/biomechanics/`

## Executive State

This is a public GitHub Pages course made from self-contained HTML modules:
MathJax, inline SVG/SMIL, no build step, no JavaScript framework. The durable
course artifacts are the committed `moduleNN.html` files plus the index/README.
Scratch figure generators are intentionally session-transient unless promoted to
documentation.

The most important handoff correction is that `HANDOFF.md` is stale. It says
Module 6 is complete and Module 7 is next. The actual repository state is newer:

- `main` and `origin/main` are at `d04089e`.
- Modules 1-7 are complete and linked from `index.html` and `README.md`.
- Module 7 is live: `https://az9713.github.io/biomechanics/module07.html`
  returned HTTP 200 during this audit.
- Modules 8-17 are pending; the next development module is Module 8,
  Walking Biomechanics.
- The working tree has only pre-existing untracked items:
  `.ignore/`, `AGENTS.md`, `here.sh.txt`, `prompt.txt`.

## Current Files

Core course files:

- `index.html`: landing page and syllabus; currently lists Modules 1-7 and a
  pending Modules 8-17 line.
- `README.md`: live-page list; currently includes Modules 1-7.
- `module01.html` through `module07.html`: self-contained course modules.
- `module04-plan.md`, `module05-plan.md`, `module06-plan.md`,
  `module07-plan.md`: approved build plans for later modules.
- `module04-learnings.md`: durable playbook from the first large 30-problem,
  many-figure module.
- `audit-modules.md`, `check-svg-fixlist.md`,
  `skill-improvements-from-audit.md`, `skill-change-list.md`: audit and
  tooling-upgrade records.
- `svg-figure-tiers.md`: figure-style decision document.
- `prompt.txt`: original course spec and real source of truth for scope. It is
  present but currently untracked.
- `.nojekyll`: committed Pages fix; keeps GitHub Pages from running Jekyll.
- `CLAUDE.md`: standing project conventions. In this workspace, `AGENTS.md`
  mirrors much of this, but `CLAUDE.md` plus the newer repo state should be
  treated as the source for the Claude-era conventions.
- `HANDOFF.md`: useful, but stale as noted above.

History files:

- `.ignore/**/cc*_skeleton.txt`: 38 Claude Code skeleton transcripts, roughly
  50k lines. These are untracked and should remain out of commits.

Skill:

- `C:\Users\simon\.claude\skills\rigorous-explainer\`
- The project instructions sometimes mention `.Codex`; the actual skill path
  inspected here is `.claude`.

## Module Inventory

Approximate source inventory from the current HTML files:

| Module | Topic | Status | h2 | figures | details | C/D/K problems |
|---|---|---:|---:|---:|---:|---:|
| 1 | Mechanical foundations | Complete/live | 13 | 5 | 0 | 0 |
| 2 | Bones / beam theory / remodeling | Complete/live | 12 | 6 | 0 | 0 |
| 3 | Joints as constrained interfaces | Complete/live | 11 | 54 | 35 | 30 |
| 4 | Cartilage / synovial fluid / contact | Complete/live | 11 | 52 | 35 | 30 |
| 5 | Muscles as chemo-electro-mechanical actuators | Complete/live | 12 | 33 | 35 | 30 |
| 6 | Tendons, ligaments, fascia, elastic storage | Complete/live | 12 | 24 | 35 | 30 |
| 7 | Standing, posture, load bearing | Complete/live | 12 | 51 | 35 | 30 |

Module 7 is the current frontier module. It covers:

- §0 motivation: standing is not passive.
- §1 base of support, COM, static margin.
- §2 GRF and COP.
- §3 inverted-pendulum dynamics.
- §4 upright linearization and instability.
- §5 ankle-strategy PD control.
- §6 delayed feedback and sway.
- §7 hip strategy, co-contraction, knee locking.
- §8 load bearing and L5/S1 compression.
- §9 two computational labs.
- §10 limitations, diagnostics, 30 problems.
- Appendix notation and parameters.

Module 7 also explicitly forwards idealizations to Modules 8, 9, 12, 13, and
14. The immediate next module is Module 8, which should cash the walking /
moving-base inverted-pendulum and frontal-plane balance IOUs.

## Development Timeline

Git history and the `cc*_skeleton.txt` transcripts agree on the major arc:

1. 2026-06-28: initial Modules 1-3 were added, then Module 3 was substantially
   rebuilt section-by-section.
2. Module 3 established several durable rules:
   redundant Cartesian coordinates were chosen over joint angles in §7 because
   multipliers expose joint reactions; anatomy figures moved from abstract
   line/triangle diagrams to Tier-2 recognizable bodies; §9 expanded to 30
   problems with one figure per problem.
3. Module 4 converted Module 3's joint reaction into cartilage contact physics.
   Its 30-problem section drove the generator/assembler pattern, `check_overlap`,
   figure-label halo rules, and the `module04-learnings.md` playbook.
4. Module 5 introduced the leaner process: prose authored directly in HTML,
   Python used only for figure data. It also raised the computational-problem
   bar: K problems must require simulation, optimization, inverse analysis,
   sensitivity, or regime comparison, not plug-in arithmetic.
5. Module 6 produced the largest process hardening:
   `check_proofs.py`, a stronger `checktex.py` control-character gate, the
   "uniform rigor across siblings" rule, the "verify the effect before drawing
   the figure" rule, and the Windows Unicode guidance.
6. Module 7 was completed in one later session and committed as `949f40f`.
   The README was corrected in `ef503bb`. A Pages 404 was traced to Jekyll
   build failure, not a missing HTML file; `.nojekyll` was committed in
   `d04089e`, and the live Module 7 URL now serves 200.

Important historical lesson from the skeletons: user corrections were often
substantive, not cosmetic. Examples:

- "What are the triangles?" led to the no-abstract-arrows rule.
- Module 3 §7 had to be reformulated because reduced coordinates hid the
  force the section promised to teach.
- Module 4's overlap sweep found real label/curve collisions that visual
  inspection had missed.
- Module 6's Maxwell/Kelvin-Voigt proof issue passed the automated checks until
  the sibling-rigor rule and `check_proofs.py` were added.
- Module 7's lifting calculation caught a narrative bug: 15 kg did not cross
  the stated compression threshold; the section was corrected to 20 kg.

## The Rigorous-Explainer Skill

The skill is a local production system for rigorous, figure-rich HTML lessons.
Important files:

- `SKILL.md`: always-loaded rule set and workflow.
- `assets/template.html`: MathJax config, CSS kit, figure counter, proof boxes,
  code copy button, reduced-motion SMIL guard.
- `references/pedagogy-checklist.md`: self-contained symbol definitions, spine,
  motivation, proof rigor, visual rhythm, validation, diagnostics/problems, and
  safe restructuring.
- `references/figures-and-animation.md`: SVG style, Tier-2 anatomy, marker/id
  rules, computed plots, SMIL, 3-D projection, splice hazards.
- `references/math-html-gotchas.md`: MathJax delimiter, raw `<`/`>` in math,
  SVG text math limitations, raw string and shell quoting hazards, Windows UTF-8.
- `references/shipping.md`: GitHub Pages and README publishing recipe.
- `scripts/*.py`: hardening and preview tools.

The skill's non-negotiables:

- Define every symbol and term at first use.
- Keep one building spine; section N should depend on earlier sections.
- No walls of words; use visuals/tables/boxes without cutting rigor.
- Derivations and proofs must show real steps; sibling boxed results need
  uniform rigor.
- Section references are clickable once targets exist.
- Prose belongs in the HTML; Python computes figures, numbers, and SVG bodies.

## Hardening Loop

The standing loop after every edit is:

```powershell
$S='C:/Users/simon/.claude/skills/rigorous-explainer/scripts'
python "$S/checktex.py" moduleNN.html
python "$S/checklt.py" moduleNN.html
python "$S/check_links.py" moduleNN.html
python "$S/check_svg.py" moduleNN.html
python "$S/verify_dom.py" moduleNN.html
python "$S/check_overlap.py" moduleNN.html
python "$S/check_frame.py" moduleNN.html
python "$S/check_prose.py" moduleNN.html
python "$S/check_proofs.py" moduleNN.html
```

Current Module 7 static checks run in this Codex audit:

- `checktex`: 686 math segments, 0 issues.
- `checklt`: 0 raw `<`/`>` math issues.
- `check_links`: 187 internal links, 0 broken, 0 unlinked section refs.
- `check_svg`: 0 hard issues, 2 advisories:
  mixed "Answer"/"solution" disclosure labels, and 5 long polylines.
- `check_proofs`: 0 asserted propositions.
- `check_prose`: 0 advisory prose flags.

Browser-based checks could not be rerun locally from this managed Codex sandbox
because the scripts attempted to write temporary instrumented HTML under
`C:\Users\simon\AppData\Local\Temp`, which is not writable here. Setting
`TEMP/TMP/TMPDIR` did not override Python's selected temp directory because
`C:\tmp` also denied writes in this environment. This is an environment issue,
not a discovered content failure. The Module 7 skeleton transcript records the
finished-module browser checks as green:

- `check_overlap`: 0 label/curve overlaps.
- `verify_dom`: 0 MathJax errors, 0 broken links, 0 swallowed prose.
- Full-page visual sanity check passed.

Live URL verification did succeed via an escalated network check:

- `https://az9713.github.io/biomechanics/module07.html` returned HTTP 200.

## Figure System

Default figure style:

- Physics/FBD/plots/animations: flat schematic SVG, but computed.
- Anatomy/real entities: Tier-2 shaded SVG with capsule bones, sphere joints,
  gradients, drop shadows, and recognizable body or joint context.
- Never AI-generate anatomy.
- Every vector is a slim arrow with `markerUnits="userSpaceOnUse"`.
- No fat triangle/wedge load glyphs.
- SVG IDs are page-global; prefix or use one shared hidden defs block.
- SVG text does not use MathJax. Use Unicode glyphs or `<tspan>` subscripts.
- Computed labels and markers must sit on computed coordinates.
- Run `check_overlap.py`; do not trust visual inspection for label/curve
  clearance.

For future figure-heavy sections:

- Build one representative figure per family and get sign-off before producing
  dozens.
- Use the lean splice pattern only for figures:
  `genN.py -> figsN.json -> splice only between <!--FIG:key--> markers`.
- Assert each marker exists exactly once.
- Re-splice by unique `aria-label`, not by viewBox dimensions.
- Keep prose out of generator raw strings.

## Project Workflow

The user's preferred cadence is:

1. Plan from `prompt.txt` plus prior-module forward references.
2. Build one section.
3. Report a short summary plus two `★ Insight` bullets.
4. User reviews.
5. Commit/push only when the user says `commit push`.

Publish-while-incomplete policy:

- As soon as a module is first committed, wire it into both `index.html` and
  `README.md`.
- Mark it `(in progress)` until complete.
- Remove the marker on completion.

Git conventions:

- Commit as `az9713 <az9713@yahoo.com>`.
- Claude-era trailers used:
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` and
  `Claude-Session: <session url>`.
- For Codex continuation, preserve the explicit session trailer convention the
  user wants before committing. Do not infer a new trailer silently.

## Known Gaps And Risks

1. `HANDOFF.md` is stale and should be refreshed before the next real build.
   It currently sends the next developer to Module 7, but Module 7 is already
   complete.
2. `prompt.txt` is the source of truth for course scope but is currently
   untracked. This may be intentional from the Claude workflow, but it is a
   handoff risk because multiple docs refer to it as authoritative.
3. `AGENTS.md` was supplied in the prompt and exists untracked locally. It
   includes useful conventions, but some status is stale relative to git.
4. Module 7 has two `check_svg` advisories. They were accepted historically, but
   if polishing before Module 8, unifying disclosure labels and decimating the
   long polylines would be low-risk cleanup.
5. Earlier audit backlog still matters:
   - Module 1: add joint-reaction / low-back number improvements.
   - Module 2: deepen torsion and add stronger problem solutions.
   - Module 3: nonholonomic wording fix, broader K problem coverage, hip JRF
     validation caveat.
   - Module 4: Hertz validity caveat / conforming-contact honesty.
6. Browser hardening scripts need a temp-directory workaround in this Codex
   sandbox before they can run locally. Options: patch the scripts to accept a
   `--tmpdir` argument, run them outside the sandbox, or use the existing Claude
   environment where they already worked.

## Next Development Task

Start Module 8: Walking Biomechanics.

Before writing `module08.html`:

1. Refresh `HANDOFF.md` or at least consciously ignore its stale Module 7 next
   step.
2. Read `prompt.txt` Module 8.
3. Grep Modules 1-7 for `Module&nbsp;8` and `Module 8` to collect IOUs.
4. Write `module08-plan.md` first and get approval.
5. Build section-by-section, preserving the Module 7 standard:
   formal derivations where peers are formal, one figure per problem in the
   final problem set, and computational K problems that require real modeling.

Module 8 should likely repay these Module 7 IOUs:

- Multi-segment dynamics beyond a single inverted pendulum.
- Walking as a moving-base / step-to-step inverted pendulum.
- Frontal-plane and medio-lateral balance.
- COP trajectory through gait.

## Recommended Codex Operating Notes

- Read the target module and adjacent plan before editing. The text already
  contains binding promises.
- Use `rg` first; the HTML files are large but structured.
- Do not commit until explicitly told.
- Do not commit `.ignore/` or session scratch files.
- Prefer `apply_patch` for report/doc/code edits in this environment.
- For figure generation, use a scratch directory in the workspace or an allowed
  temp root; keep generated scripts out of commits unless the user asks.
- After `autolink_sections.py`, re-read the edited region before any further
  patch because the file is rewritten and a `.bak` may be created.
- Treat "green checks" as necessary but insufficient. Cross-problem numerical
  consistency and sibling proof rigor still need a human read.

