# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last handoff written:** 2026-07-27 (session close — course-wide anatomy audit
complete; FIX PHASE PENDING).

---

## ⇒ RESUME HERE: execute the anatomy fixes in `ANATOMY_AUDIT.md`

A full coordinate-verified visual audit of every human-anatomy figure (2026-07-27,
7 parallel agents) found a **course-wide regression from the realism pass
(`3fd6fbe`)**: exposition figures are good (Winter `anatomy_kit.body_group`), but
the **problem-set body figures across modules 1–15 are broken** — **~90
defect-level figures.** The audit is DONE and fully documented; **no re-auditing
needed** — just execute.

**FIX PROGRESS (2026-07-27, ~63 of ~90 figures, 19 commits `8b1cdce`→HEAD):**
- **m11 DONE** (6 blank bodies emitted, 29 heads seated, 60 slabs thinned).
- **m12 DONE** (7 heads seated, shoulder-ball gradient, slabs).
- **m13 trunk-columns DONE** (f5/f9/f16/f23 no-legs bodies regenerated).
- **m07 broken bodies DONE** (18/23/29/30/31/32 — 8 bodies regenerated, overlays
  kept aligned).
- **m03 f26 clip, m04 f15, m06 f21, m13 f4** slab/clip fixes.
- See `ANATOMY_AUDIT.md` PROGRESS + the three **PROVEN RECIPES** (emit body /
  seat-head-by-shared-coord / thin-slabs-by-0.3×length-ratio / element-wise
  body-swap preserving hip-shoulder-arm axes for overlay-bearing figures).

**REMAINING (~27, per-figure) — start here next session:**
- **m09/m10** (biggest chunk): broken gait/gown bodies + slabs where **limbs are
  `#c98a5e` LINES** (exclude that colour from the slab-thin, or legs vanish). These
  bodies are line-based, not rect-based — remove the line body, insert a posed
  `body_group` at the scene ground anchor.
- **m13 remaining**: per-figure detached heads + missing feet + one-limb on the
  C/D problem bodies (heads at varying coords — no shared template; add a foot at
  each bare ankle, seat each head).
- **m01 f13/f21, m15**: backward knees inside transformed groups (resolve transform
  or body-swap). **m02/m14**: neck-less femurs. **m07** sheet-"fig16" hyperextension
  (locate by caption — numbering mismatch). **m12** fig21 walker ground-slab.
- Continue worst-first; gate (all nine) + render-verify + commit per figure/module.

- **Work-list + root causes + fix order:** `ANATOMY_AUDIT.md` (repo root). Read it
  first, fix in the order it gives.
- **Root-cause families** (fixing a few clears most figures): (A) annotation
  `<line stroke-width>` set to ~0.3×length → 60–174px slabs burying anatomy
  (m04/06/07/10/11/12/13); (B) detached head + oversized "neck-ball", no real neck
  (m07/11/12/13); (C) footless shank stumps / one-leg / one-arm / no-thigh bodies;
  (D) **6 m11 figures whose body `<g>` is EMPTY** (f8/11/12/38/39/45); (E) backward
  knees (m01 f13/f21, m09 f2, m15 f3) & through-arm/wrong-way elbows (m11 f16/f23);
  (F) `a_red`/siblings missing `markerUnits="userSpaceOnUse"` → wedge-blob heads;
  (G) m13 f5/f9/f16/f23 = "trunk-column" bodies with NO legs.
- **How to fix:** original generators are gone; bodies are baked static SVG.
  Regenerate each from `anatomy_kit.body_group` posed to match, keep the physics
  overlays, thin the annotation strokes, fix markers. After EACH module: run all
  nine hard gates (esp. `check_bodyprop`, `check_frame`, `check_overlap`,
  `verify_dom`) then commit+push that module.
- **Audit tooling** (session-transient scratch, regenerate if gone):
  `…/a21d973c-…/scratchpad/an.py` (`an.run('moduleNN.html',{figs})` → limb
  endpoints/joints/fat-lines) and `render.py` (full-height per-figure renderer —
  the truncation-safe replacement for the capped `build_sheets.py`).

## Prior state (unchanged facts)

- Modules 1–17 are LIVE at https://az9713.github.io/biomechanics/; remote tip =
  local tip. The realism pass is committed at `3fd6fbe`. `.gitignore` excludes
  `body_template.JPEG` and `mcps/`.
- **Caution:** the nine hard gates previously reported "all green" but did NOT
  catch these anatomy defects — they are geometric/semantic (backward knees,
  detached heads, footless legs, fat annotation strokes, empty body groups) that
  `check_bodyprop` (proportion-only) and the others do not test. Trust the audit
  register, not a prior "green" claim.
- **Only commit on the user's explicit "commit push."** (The audit docs were
  committed as a completed work unit.)

## Recently explored & dropped (don't re-propose unprompted)

- **Costco flat-pictogram restyle** (from `body_template.JPEG`): investigated
  2026-07-20, user dropped it. The crux finding: a *solid* silhouette occludes
  the physics overlay (hip/COM/GRF/moment-arm), so it can't replace FBD-bearing
  whole-body figures. Course keeps its **Tier-2 shaded / data-driven** figures.

## Where to read things (reference, don't re-derive)

- `CLAUDE.md` — standing conventions (build loop, hardening, git/publish, figures).
- `anatomy_kit/README.md` — how the durable body/figure generators + tests work.
- `anatomy_kit/ATTRIBUTIONS.md` — NIH BioArt public-domain licenses.
- `BIOLOGICAL_FIGURE_REALISM_{PLAN,IMPLEMENTATION_REPORT}.md` — the realism spec +
  full history (incl. §5A per-figure catalog).
- `svg-figure-tiers.md` — Tier 1/2/Real + "geometry from data" rule.
- `prompt.txt` — course structure source of truth.
- Hardening scripts — `C:\Users\<user>\.claude\skills\rigorous-explainer\scripts\`.

## Session-transient scratch (regenerate; durable record is the committed output)

- **`anatomy_kit/py/*.py`** — these are the **durable, committed** generators
  (body/foot/heroes + previews + apply scripts). Not transient. Regenerate figures
  or previews from `anatomy_kit/README.md`.
- One-off analysis from the 2026-07-20 session (figure classifiers, the pictogram
  mockup, the hardening-sweep script) lived in the OS scratchpad and is **gone** —
  none of it is needed; the durable record is the committed modules + gates.

## How to work (essentials — full detail in `CLAUDE.md`)

- **Commit only on the user's explicit "commit push."** Push to public `main`.
  Commit as `az9713` with the `az9713@users.noreply.github.com` email; keep the
  standard trailer block.
- **Hardening loop after every figure edit** (all nine hard gates above must be 0)
  — and don't trust a prior session's "all green" claim; re-run it (this session
  found 9 bugs a prior "green" handoff had missed).
- **Figures:** Tier-2 + data-driven via `anatomy_kit/`; never AI anatomy; slim
  arrows; Unicode in SVG `<text>`, not `$…$`. Approve one representative figure
  before mass-producing a style.
