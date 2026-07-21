# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook. Don't
duplicate content that already lives in the files referenced below — open them.

**Last handoff written:** 2026-07-15 (session close — biological figure realism).  
**Agent:** Grok Build powered by Grok 4.5 (high).

---

## Current state

### Course baseline (already on remote `main`)
- **ENTIRE COURSE COMPLETE:** modules 1–17 live at
  https://az9713.github.io/biomechanics/
- **Remote tip (unchanged by this session):** `f114a91`
  (*Modules 8/11/12/15 figures: chunky-pictogram proportions + v-elbow fix*).
- Prior rigor retrofit (`IMPLEMENTATION_PLAN.md`, `phase0_result.json`) remains the
  record for that pass — still valid.

### THIS SESSION — Biological figure realism (**DONE but NOT committed**)

Full plan executed: **`BIOLOGICAL_FIGURE_REALISM_PLAN.md`** (status COMPLETE).

| Deliverable | Path | Notes |
|-------------|------|--------|
| Plan | `BIOLOGICAL_FIGURE_REALISM_PLAN.md` | Phases 0–5, Waves A–E, §9/§10 checked |
| Dev report (MD) | `BIOLOGICAL_FIGURE_REALISM_IMPLEMENTATION_REPORT.md` | Full history + **§5A per-figure catalog** |
| Dev report (HTML) | `BIOLOGICAL_FIGURE_REALISM_IMPLEMENTATION_REPORT.html` | Full conversion of the MD (no content skipped) |
| Anatomy kit | `anatomy_kit/` | **New package** — body/foot/heroes/tests/previews/NIH SVGs |
| Figure policy | `svg-figure-tiers.md` | Added “Geometry from data” rule |
| Modules touched | `module01.html` … `module17.html` | Heroes + hygiene + aria rewrites |
| Conventions | `CLAUDE.md`, `AGENTS.md` | May have unrelated local mods too — review before commit |

**What the kit does (durable product):**
- Winter-proportion posable body + gait poses (`anatomy_kit/py/body.py`)
- Plantar foot + COP path (never `b_head` fill) (`foot_plantar.py`)
- Geometry heroes: femur/hip/knee/shoulder/lumbar/foot (`geometry_heroes.py`)
- NIH BioArt **public domain** SVGs: upper leg + arm bones (`svg_paths/nih_*.svg`)
- Attributions: `anatomy_kit/ATTRIBUTIONS.md`
- Tests: `test_proportions.py`, `test_heroes_and_exports.py`, `test_aria_labels.py`
- Apply scripts: `wave_a_apply.py`, `phase2_apply.py`, `finish_all_waves.py`, `fetch_nih_heroes.py`

**Hardening (last known green):** M1–M17 passed hard suite including
`checktex/checklt/check_links/check_svg/verify_dom/check_overlap/check_frame/check_bodyprop/check_code`
with 0 hard failures. Inventory: large-head r>18 → 0; path-level head-fill-on-foot → 0.
Problem-figure placeholder aria-labels → 0 (`test_aria_labels.py`).

**Git state at handoff (CRITICAL):**
- Branch: `main` @ `f114a91` (remote).
- **Working tree DIRTY** — realism work is **local only, not pushed**.
- Do **not** assume Pages has the new figures until after **commit push**.

### Uncommitted / untracked (review before commit)

**Modified (tracked):**
- `module01.html` … `module17.html` (all 17)
- `svg-figure-tiers.md`
- `HANDOFF.md` (this file)
- `CLAUDE.md`, `AGENTS.md` (check diff — may include non-realism edits)
- `.claude/skills/rigorous-explainer/SKILL.md` (check diff)

**Untracked (should be added if committing realism):**
- `anatomy_kit/` (entire tree)
- `BIOLOGICAL_FIGURE_REALISM_PLAN.md`
- `BIOLOGICAL_FIGURE_REALISM_IMPLEMENTATION_REPORT.md`
- `BIOLOGICAL_FIGURE_REALISM_IMPLEMENTATION_REPORT.html`
- `.claude/skills/rigorous-explainer/scripts/check_bodyprop.py` (if intentional skill update)
- `mcps/` (unknown/unrelated — **do not blindly add**; inspect)

**Do not commit:** `.ignore/` session scripts, temp previews, SCRATCH logs.

---

## Next task

1. **Primary — user says “commit push”:**  
   - Review `git diff` especially `CLAUDE.md` / `AGENTS.md` / skill files.  
   - Stage realism deliverables only (kit + modules + plan + reports + svg-figure-tiers + this HANDOFF).  
   - Commit with a clear message (e.g. “Course-wide biological figure realism: anatomy_kit + Waves A–E”).  
   - Push `main`; confirm remote HEAD matches local.  
   - User hard-refreshes live Pages (`?v=N`).

2. **If continuing polish instead of commit:**  
   - Optional: full Winter pose regen of remaining problem-set bodies (still capsule-y ones).  
   - Optional: Servier/OpenStax Real plates for menisci / pennate muscle.  
   - Re-run kit tests + hardening after any further edit.

3. **If user asks for something else**, that takes precedence.

---

## Where to read things (reference, don't re-derive)

| Doc | Why open it |
|-----|-------------|
| **This file** | Resume point |
| `CLAUDE.md` | Build loop, hardening, git/publish, figure rules |
| `BIOLOGICAL_FIGURE_REALISM_PLAN.md` | Spec that was executed |
| `BIOLOGICAL_FIGURE_REALISM_IMPLEMENTATION_REPORT.md` | Full development history + **§5A per-figure tables** |
| `BIOLOGICAL_FIGURE_REALISM_IMPLEMENTATION_REPORT.html` | Same report, browser-readable |
| `anatomy_kit/README.md` | How to regenerate previews/tests/apply scripts |
| `anatomy_kit/ATTRIBUTIONS.md` | NIH PD licenses |
| `svg-figure-tiers.md` | Tier 1/2/Real + geometry-from-data rule |
| `prompt.txt` | Course structure source of truth |
| `IMPLEMENTATION_PLAN.md` + `phase0_result.json` | Prior rigor retrofit (separate) |
| Hardening scripts | `C:\Users\<user>\.claude\skills\rigorous-explainer\scripts\` |

---

## Session-transient scratch (regenerate; durable record is kit + modules)

These lived under `.ignore/` and/or implementer SCRATCH; **not required in git**.
Patterns to rebuild if needed:

| Pattern | Role |
|---------|------|
| `anatomy_kit/py/*.py` | **Durable** generators (committed with kit) |
| `.ignore/harden_all.py` | Full hard suite → logs |
| `.ignore/fix_aria_labels*.py` | Aria rewrite (already applied to HTML) |
| `.ignore/per_figure_changes.py` | Regenerates §5A catalog from live modules |
| `.ignore/md_to_html_report.py` | MD → HTML report conversion |
| `.ignore/finish` / gate fix scripts | One-shot harden/viewBox/bodyprop fixes already baked into HTML |

**Session SCRATCH** (may be deleted by OS/harness):  
`C:\Users\simon\AppData\Local\Temp\grok-goal-92ae88c38da1\implementer\`  
Had: `harden_all.log`, `harden_m01`…`m17.log`, `fig_audit_post.txt`,
`figure_class_inventory.md`, kit/aria test logs. Re-run tests +
`.ignore/harden_all.py` if you need fresh evidence.

---

## How to work (essentials — full detail in `CLAUDE.md`)

- **Commit only on user “commit push”** (or explicit autonomy grant).
- **Section-by-section** for new content; hardening loop after HTML edits.
- **Figures:** Tier-2 + data-driven geometry via `anatomy_kit/`; Class S stays schematic;
  never AI anatomy; slim arrows; Unicode in SVG text not `$…$`.
- **Publish-while-incomplete:** if committing incomplete modules, wire `index.html` +
  `README.md` live links (full course already live).
- **Hardening (must pass for figure work):**
  `checktex checklt check_links check_svg verify_dom check_overlap check_frame
  check_bodyprop check_code` (+ prose/proofs/probfig as advisory).

### Quick verification after resume

```bash
python anatomy_kit/tests/test_proportions.py
python anatomy_kit/tests/test_heroes_and_exports.py
python anatomy_kit/tests/test_aria_labels.py
# optional full harden:
# python .ignore/harden_all.py   # if script still present
```

### Quick previews

```bash
python anatomy_kit/py/build_previews.py
python anatomy_kit/py/build_phase2_previews.py
# open anatomy_kit/previews/*.html
# open BIOLOGICAL_FIGURE_REALISM_IMPLEMENTATION_REPORT.html
```

---

## Suggested first actions for next agent

1. Read this file + skim `BIOLOGICAL_FIGURE_REALISM_IMPLEMENTATION_REPORT.md` §0–§3 and §5A.  
2. `git status` — confirm dirty tree matches list above.  
3. Ask user: **commit push** now, or more polish first?  
4. If commit: stage carefully, exclude `mcps/` unless user wants it; push; verify remote.

---

*End of handoff — 2026-07-15.*
