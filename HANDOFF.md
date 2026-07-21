# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last handoff written:** 2026-07-20 (session close — committed the realism pass).

---

## Current state (as of latest push)

- **ENTIRE COURSE COMPLETE & LIVE:** modules 1–17 at
  https://az9713.github.io/biomechanics/
- **Remote tip = local tip = `3fd6fbe`** ("Course-wide biological figure
  realism: anatomy_kit + data-driven figures"). Working tree **clean**; local
  and `origin/main` match.
- **The big prior open item is now resolved.** The "biological figure realism"
  pass (Winter-proportion figures + `anatomy_kit/`) that the previous handoff
  described as *"DONE but NOT committed"* is **committed and pushed** at `3fd6fbe`.
  The live site now shows the realism figures (not the older chunky-pictogram set
  from `f114a91`).
- **Bugs fixed while committing:** the realism pass had left **9 truncated
  `aria-label`s** sliced mid-`$…$` (unclosed inline math) — module11 ×8,
  module16 ×1. All fixed (labels cut back to before the dangling `$`, ended with
  an ellipsis; they're screen-reader text, never typeset). module16's odd parity
  was caught by `checktex`; module11's even-parity pair only by `checklt`.
- **Verified:** all 17 modules pass the **nine hard gates** — `checktex`,
  `checklt`, `check_links`, `check_svg`, `check_code`, `verify_dom` (0 MathJax
  errors), `check_overlap`, `check_frame`, `check_bodyprop`.
- **`.gitignore` now excludes** `body_template.JPEG` (copyright reference image)
  and `mcps/` (unrelated local MCP folders). Neither is on the public repo.

## Next task

- **No committed-in next task — the course is complete and clean.** Start from
  whatever the user brings next. If they ask for "more polish," the standing
  optional tracks are: Servier/OpenStax "Real" plates for menisci / pennate
  muscle; full Winter-pose regen of any remaining still-capsule-y problem-set
  bodies. Neither is required.
- **If the user asks for something else, that takes precedence.**
- Any figure edit → re-run the hardening loop (all nine gates) before commit.
  **Only commit on the user's explicit "commit push."**

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
