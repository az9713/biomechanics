# HANDOFF — resume point for the biomechanics course

**Read this first each new session, then `CLAUDE.md` for the full conventions.**
This file is the live "what to do next"; `CLAUDE.md` is the standing playbook.
Don't duplicate what already lives in the files referenced below — open them.

**Last handoff written:** 2026-07-27 (anatomy fix phase ~complete; ONE bespoke
figure + cosmetics remain).

---

## Current state (as of latest push `f6e7317`)

The course-wide **anatomy regression** from the realism pass (`3fd6fbe`) is
**fixed — ~89 of ~90 defect figures done**, every one gate-checked AND rendered,
across ~36 commits (`8b1cdce` → `f6e7317`). All pushed to `main`; remote tip =
local tip = `f6e7317`. Working tree clean apart from known-untracked tool dirs
`.agents/` and `.codex/` (local scaffolding — leave untracked, like `mcps/`).

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

## Next task — **m02 fig1 (the one real remaining figure)**

**Goal:** the teaching femur in `module02.html` fig1 is a single closed `<path>`
whose neck-shaft angle reads ~146° (coxa valga) instead of the normal ~125°.
Correct it to ~125°.

**Why it was deferred, not skipped:** it is NOT a capsule+sphere body (the proven
recipes don't apply) — it's one hand-authored closed outline. Fixing it means
recomputing the head-arc centre + neck vertices of that path so the outline stays
coherent, which needs **iterative render-verification** — and in the prior session
Chrome renders had started timing out at 2 min, so a bone-outline edit could not
be safely verified. A fresh session (renders working again) is the right place.

**How to do it (est. ~10 min in a clean session):**
1. Locate fig1 by caption (numbering mismatch — don't trust sheet-position numbers).
2. Read the femur `<path d="…">`; identify the head-arc (`A rx ry …`) + the neck
   segment feeding into the shaft. Reuse **m14 fig5's** now-correct proximal-femur
   geometry (neck at ~125° off the shaft axis + a lateral greater trochanter) as
   the shape reference.
3. Recompute the head centre (medial-superior of the shaft top) and neck vertices;
   edit the `d` in place. Retarget any fall/impact arrow to the **lateral greater
   trochanter**, not the head.
4. **Render-verify** (`shoot.py`) — confirm the outline is coherent and the angle
   reads ~125°. Revert the edit if the outline breaks; do not ship unverified.
5. Run all nine hard gates → commit + push that figure.

## Then — cosmetic cleanup (optional, low priority; not incorrect-anatomy)
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
