# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook. Don't
duplicate content that already lives in the files referenced below — open them.

## Current state (as of latest push)
- **ENTIRE COURSE COMPLETE: all 17 modules built, hardened, reviewed, and live**
  at https://az9713.github.io/biomechanics/ .
- **Retrofit pass COMPLETE** (this session): a feasibility assessment
  (`rigorous-explainer-feasibility-assessment.md` + a revised critique
  `rigorous-explainer-feasibility-assessment-revised.md`) led to
  `IMPLEMENTATION_PLAN.md`, grounded in a mechanical **Phase-0 inventory**
  (`phase0_result.json`) across all 17 modules × the 11-check hardening loop.
  All six phases are done:
  - **Phase 1** — hard-gate green sweep: M1–M8 (the modules that predated the
    newest gates) fixed to 0 on `check_code`/`check_frame`; two real figure bugs
    fixed along the way (M6's tangent-stiffness curve, M7's viewBox mismatches).
  - **Phase 2/3** — rigor-parity + domain-substance retrofits on **M1, M2, M3,
    M4, M5** (parallel worktree agents, one per module) + **M7** (redrew two
    bare problem figures) + **M12** (fixed one bare problem figure). Each
    proved/demoted every flagged proposition, closed the named
    `audit-modules.md` domain gaps (M2's torsion strand, M1's GRF/COP section +
    joint-reaction/low-back numbers, M3's nonholonomic relabel + hip-reaction
    reconciliation, M4's Hertz-validity + strain caveats, M5's force
    reconciliation), and — for M1/M2 — built the missing 30-problem C/D/K sets.
    **Every module went through build → harden-to-0 → 3-pass rigor-review →
    fix → re-verify → merge → commit.** The reviewer caught real bugs each time
    it ran (a scrambled D-section assembly in M1, a disguised-plug-in K
    problem in M2, a velocity/acceleration mislabel in an M7 figure) — it is
    a load-bearing gate, not a formality.
  - **Phase 4** — M1 and M2's 30-problem sets, built + reviewed (see above).
  - **Phase 5** — M17 optional depth: **skipped** (M17 already covers all 15
    `prompt.txt` capstones — 6 worked + 9 briefs — per the revised assessment;
    deepening the briefs is optional polish, not a gap).
  - **Phase 6** — aligned `CLAUDE.md`'s and `AGENTS.md`'s hardening-loop lists
    with the skill's actual 11-check set (both were missing `check_svg`,
    `check_code`, `check_probfig`; `AGENTS.md` also pointed at a nonexistent
    `~/.Codex/skills/` path, repointed to the canonical `~/.claude/skills/`);
    added the missing `prefers-reduced-motion` SMIL guard to M1/M3/M4 (M2/M5
    already had it from the template).
- **Residual / explicitly deferred** (low priority, not blocking — from
  `audit-modules.md` §A, the cross-cutting themes):
  - Course-wide **SVG label typography retrofit** (matching the MathJax serif
    font in figure `<text>`) — not done for M1–M5.
  - Course-wide **symbol-collision flags** beyond what was fixed in-pass.
  - **Figures not cited by number** in prose ("the figure below" vs "Fig. 3").
  - **§9/§11 problem-set sub-TOC navigation** (per-group "↑ contents" links).
  - **No inter-module navigation rail** (◀ Module N−1 · N · N+1 ▶).
  - M3: K1–K10 only exercise §7 (no computational problems for hip JRF/contact
    pressure/stability ratio); §5's congruence claim isn't shown as a swept curve.
  - These were out of scope for the targeted agent tracks (which fixed the
    *named* defects, not the broad low-priority sweeps) — pick up as a future
    session if the course needs another pass.
- Everything committed and pushed to `main` (https://github.com/az9713/biomechanics);
  local == remote. Working tree clean apart from local scratch (`.ignore/`, preview
  PNGs) and the gitignored `claude-transcripts/` + `.claude/worktrees/`.

## Next task
- **No blocking work.** If resuming cold: skim the residual list above and
  `audit-modules.md` §A for optional polish, or ask the user what's next.
- `IMPLEMENTATION_PLAN.md` + `phase0_result.json` are the retrofit's durable
  record — read them before assuming something is still broken; re-run the
  hardening loop to get current ground truth rather than trusting old notes.

## Where to read things (reference, don't re-derive)
- **`CLAUDE.md`** (repo root) — authoritative conventions: build loop, hardening loop,
  figure rules, git/publish, publish-while-incomplete. **Read it.**
- **`AGENTS.md`** — same conventions, for tools that read this filename instead.
- **`prompt.txt`** — original course spec; source of truth for scope/structure of all 17 modules.
- **`IMPLEMENTATION_PLAN.md`** + **`phase0_result.json`** — this session's retrofit plan
  and its grounding mechanical inventory.
- **`rigorous-explainer-feasibility-assessment.md`** / **`-revised.md`** — the
  feasibility analysis (Grok v1 + a corrected revision) that the retrofit plan was built from.
- **`DEVELOPMENT_JOURNEY.md`** — the full development history of the skill, the
  rigor-reviewer agent, and the module-by-module build (read this instead of
  digging through old HANDOFF revisions or git log for "how did we get here").
- **`audit-modules.md`** — the substance backlog for Modules 1–5 (mostly closed
  this session; residual items listed above).
- **Skill:** `C:\Users\simon\.claude\skills\rigorous-explainer\` — SKILL.md, `scripts/*.py`
  (hardening tools), `references/*.md`, `assets/template.html`.
- **`.claude/agents/rigor-reviewer.md`** — the reviewer agent (read-only judge of rigor
  parity, prose, K-depth, self-containment). Dispatch it after hardening scripts hit 0,
  before considering any section/module done — it has caught a real bug every module
  it's been run on this session.

## How to work (essentials — full detail in `CLAUDE.md`)
- **Invoke `rigorous-explainer`** at the start; follow its SKILL.md build loop.
- **Section-by-section:** build ONE section → report + 2 `★ Insight` bullets → user reviews →
  commit/push **only on "commit push"** (unless the user has explicitly granted broader
  autonomy for a bounded task, as with this session's retrofit).
- **Figures:** Tier-2 shaded for anatomy, flat/computed for physics/plots — BUT **problem-set
  C/D/K figures always lead with the recognizable Tier-2 entity**. Compute geometry/plot data
  in Python (background runs — numpy startup is slow); slim arrows anchored to the structure;
  reuse the shared `<defs>` block. Get one representative figure approved before mass-producing.
- **Hardening loop after every edit** — all to 0 (11 checks): `checktex / checklt /
  check_links / check_svg / verify_dom / check_overlap / check_frame / check_prose /
  check_proofs / check_code / check_probfig`; then `autolink_sections.py`.
- **Parallel work:** independent modules (disjoint files) can be retrofitted by parallel
  worktree-isolated agents; the rigor-reviewer gate stays mandatory before merging any of
  them as "done." Cross-module citations/numbers need a coordinator reconciliation pass
  after merge — agents working in parallel can't see each other's edits.
- **Deploy:** `.nojekyll` is committed, so pushes deploy clean. If a Pages build stalls,
  `gh api -X POST repos/az9713/biomechanics/pages/builds` nudges a fresh one.
- **Gotcha:** never route `\`-heavy Python (`\approx`, `\alpha`, `\tau`) through a
  Bash-tool heredoc or a double-quoted shell arg — corrupts math-bearing HTML. Author
  such scripts with the Write tool using raw strings, or edit HTML directly with Write/Edit.
