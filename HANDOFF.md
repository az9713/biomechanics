# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last handoff written:** 2026-07-28 (anatomy fix phase COMPLETE — all ~90
defect figures done incl. the last bespoke one; only optional cosmetics remain).

---

## Current state (anatomy phase COMPLETE)

The course-wide **anatomy regression** from the realism pass (`3fd6fbe`) is
**fully fixed — all ~90 defect figures done**, every one gate-checked AND
rendered. The final bespoke figure (m02 fig1) is now corrected and pushed. All
pushed to `main`; remote tip = local tip. Working tree clean apart from
known-untracked tool dirs `.agents/` and `.codex/` (local scaffolding — leave
untracked, like `mcps/`).

**m02 fig1 — DONE (latest commit):** the hand-authored teaching-femur `<path>`
drew a ~146° neck-shaft angle (coxa valga) against a caption stating ~125°.
Rebuilt as a coherent single-outline proximal femur at 125° (head at (276,41),
neck axis 55° off the vertical shaft, greater-trochanter bump, condyle base),
fixed the dashed 125° guideline, and un-overlapped the GT / neck-shaft labels.
Nine gates pass; render-verified in context (`scratchpad/fig1_ctx.png`).

**What got fixed (all committed + render-verified):**
- **Every broken body regenerated** via `anatomy_kit.body_group`: m11 (6 empty
  `<g>` + 29 detached heads + 60 slabs), m12 (7 heads), m13 (4 trunk-columns),
  m07 (8 bodies, overlays kept aligned), m09 (5 gown-legs).
- **Every locatable backward knee:** m01 (f13/f21/C7), m09 fig2 (5 gait poses).
- **Every neck-less femur reachable as capsule/sphere:** m14 (fig5/17/18/32) —
  neck capsule + greater trochanter + retargeted fall arrow.
- **Every slab-buried figure:** m10 (~13 figs), plus m04/06/07/11/12/13 — thinned
  by the 0.3×length ratio, **excluding** `#c98a5e` limb-lines + wood-tone floor.
- **m15 fig4** doubled-body — deleted the duplicate offset copy.

## Next task — **cosmetic cleanup (optional, low priority; not incorrect-anatomy)**

The anatomy defect register is cleared. What remains is purely cosmetic — the
bodies are already recognizable and anatomically correct; these are polish items.
If the user brings something else, that takes precedence.
- **m10** wishbone shoulders (both arms spring from one midline point).
- **m09** fig1 (feet piled at one point), fig13 (stance leg has no knee).
- **m13** any residual detached heads / missing feet after the trunk-column pass.
Locate each by CAPTION; render-verify; gate + commit per figure. If the user
brings something else, that takes precedence.

## Where to read things (reference, don't re-derive)
- `ANATOMY_AUDIT.md` (repo root) — the full defect register, the 4 proven fix
  recipes, resolved document indices, and the safety caveats below. **Read it
  before touching any figure.**
- `CLAUDE.md` — standing conventions (build loop, nine hard gates, git/publish,
  figure style, the "Standing rules (tutor)" block).
- `anatomy_kit/README.md` — how `body_group` / `capsule` / `sphere` / `head` work.
- `prompt.txt` — course structure source of truth.

## Critical safety caveats (bit us this session)
- **Limbs in m09/m10 are drawn as thick `#c98a5e` `<line>`s.** NEVER blind-sweep
  stroke-width to thin slabs — you'll delete legs. Every slab fix excludes
  `#c98a5e` (and wood-tone floor/chair lines).
- **Figure numbering mismatch:** audit sheet-numbers ≠ document `<figure>` index.
  Locate every figure by its **caption**.
- **Some bodies sit in transformed `<g>`s** — audit coords are post-transform;
  resolve the transform before trusting coordinates.
- Spring/arc abstractions are NOT defects — render-and-judge, don't "fix" them.

## Session-transient scratch (regenerate; durable record is the committed HTML)
- Audit/render tooling lived in the OS scratchpad and is **gone** — none needed
  to finish m02 fig1 (a direct `<path>` edit + `shoot.py` render is enough).
  If you want the coordinate helpers back: `an.py` (`an.run('moduleNN.html',
  {figs})` → limb endpoints/joints/fat-lines) + `render.py` (full-height
  per-figure renderer) — regenerate from the pattern in `ANATOMY_AUDIT.md`.

## How to work (essentials — full detail in `CLAUDE.md`)
- **Nine hard gates after every figure edit** (all 0): checktex, checklt,
  check_links, check_svg, check_code, verify_dom, check_overlap, check_frame,
  check_bodyprop. Then **render-verify** with `shoot.py` — don't trust gates alone
  (they do NOT catch backward knees / detached heads / footless legs).
- **Commit + push per figure**, as `az9713` / `az9713@users.noreply.github.com`,
  with the standard trailer block. Public repo — never reintroduce the private
  `az9713@yahoo.com` email (it still lives in git history; needs a filter-repo
  rewrite + force-push, coordinate with the user first).
- **Keep the session small** — this handoff exists because the fix phase ran to
  ~680k context. Finish m02 fig1, then stop or `/clear`.
