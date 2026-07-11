# Development Journey — Method & Tooling

*How a 17-module, rigorously-hardened biomechanics course got built in ~13 days, then
survived a second, adversarial pass — a feasibility assessment, a critique of that
assessment, and a grounded repair plan — that retrofitted its earliest modules under the
same tooling. This is the story of how the **`rigorous-explainer` skill**, its
**hardening loop**, and the **`rigor-reviewer` agent** co-evolved with the course into a
repeatable, largely-autonomous authoring *and repair* pipeline.*

This report foregrounds the **method and the tooling**, not the course content. It is
assembled from durable artifacts — the repo's git history (2026-06-28 → 2026-07-11), the
skill's own `CHANGELOG.md`, the audit and change-plan docs, the feasibility-assessment
and implementation-plan documents, each hardening script's "WHY THIS EXISTS" header, the
agent-design docs, and the project memory — not from raw session transcripts. Where a
claim rests on a specific dated commit or documented incident, that is the evidence; the
granular within-session narrative of the earliest modules lives only in the (large,
deliberately un-read) transcripts and is summarized here, not reconstructed.

---

## 1. The shape of the thing

The deliverable is a public course at <https://az9713.github.io/biomechanics/>: seventeen
**self-contained HTML modules** — MathJax + inline SVG/SMIL, no build step, no JS
framework — plus a landing page and README. But the *durable* result is not the HTML. It
is a **method**: a skill that encodes how to write a rigorous explainer, a loop of
mechanical gates that make "rigorous" enforceable, and an independent reviewer agent that
judges what no script can. The course was the proving ground; the pipeline is the
invention.

**Timeline at a glance** (first commit of each module):

| Date | Milestone |
|---|---|
| 06-28 | Modules 1–3 seeded; landing page + README; Module 3 built section-by-section |
| 06-29→07-01 | Module 4 (cartilage/biphasic); **first audit → `check_svg.py`**; 51 hard issues fixed in M1–4 |
| 07-01→07-03 | Module 5 (muscle); **"prose in HTML, Python for figures" locked**; `check_frame`, `check_prose`; MIT-PhD K-problems |
| 07-03→07-04 | Module 6 (tendon); **`check_proofs`**; `checktex` control-char gate; CHANGELOG batch folds M4–6 lessons into the skill |
| 07-05 | Module 7 (standing); `.nojekyll` Pages fix; problem-figure upgrade |
| 07-05→07-08 | Module 8 (walking) **built externally by Codex, then elevated**; regression → **`check_code` + `check_probfig`**; **`rigor-reviewer` agent built & calibrated** |
| 07-09 | Module 9 (running) — **first module reviewed by the agent**; Module 10 (balance); **`check_frame` hardened to fail on clipping** |
| 07-10 | Modules 11–17 built in one autonomous `/goal` run; each 3-pass-reviewed; **course complete (17/17)** |
| 07-10→07-11 | **The retrofit**: a feasibility assessment, a critique, a Phase-0-grounded 6-phase repair plan, and a parallel review-gated retrofit of Modules 1–5, 7, 12 |

The velocity is not the point. The point is that each module was *harder to get wrong than
the last*, because every defect that shipped was converted into a gate or a rule before
the next module began.

---

## 2. The `rigorous-explainer` skill

The skill (`~/.claude/skills/rigorous-explainer/`, **not** in this repo, so it has no git
history of its own — its evolution is tracked in `CHANGELOG.md` and the repo's
`skill-change-list.md` / `skill-improvements-from-audit.md`) produces *one self-contained
HTML document that derives a result rigorously and teaches it*. Its non-negotiable core is
**five pillars**:

1. Define every symbol/term at first use (self-contained).
2. One building spine — each section uses the previous; off-path rigor to an Appendix.
3. Extensive visuals — never a wall of words; a visual every screenful.
4. Rigorous, step-by-step proofs; box the headline; **uniform rigor across siblings**.
5. Clickable section cross-references.

The skill ships a scaffold (`assets/template.html`), on-demand `references/*.md`
(pedagogy checklist, figures-and-animation, math-html-gotchas, shipping), and — the load-
bearing part — a **suite of validation scripts** that turn the pillars from aspirations
into a pass/fail gate.

### The governing insight: gates over prose

The recurring lesson, stated explicitly in the CHANGELOG, is that **the highest-frequency
judgement rules must live in the always-loaded `SKILL.md`, and the crisp mechanizable ones
must become scripts** — because `references/` are loaded on demand and were *being missed
mid-build*. A rule that lives only in a reference file is a rule that gets skipped under
load. So the skill's evolution is largely the story of **promoting drift-prone written
rules into mechanical gates.**

---

## 3. The hardening loop — a gate for every scar

The single most important artifact is the **hardening loop**: a set of scripts, each run
after *every* edit, all required to pass. It began small and grew to twelve checks, and —
this is the key — **almost every gate was born from a specific defect that shipped.** The
loop is a museum of past mistakes, each one now un-repeatable.

| Gate | What it catches | Born from |
|---|---|---|
| `checktex.py` | `$`/`$$`, brace, `\left`-`\right`, `\begin`-`\end`, `\boxed` balance — and **stray control chars** (TAB/VT/FF/BS/CR) | math splicing; the control-char rule (07-04) fingerprints `$…$`/backslash math **mangled by a double-quoted shell** (`$W`→empty, `\t`→TAB) |
| `checklt.py` | raw `<` / `>` inside `$…$` (must be `\lt`/`\gt`) | MathJax silently eating `<1` as an unclosed tag |
| `check_links.py` | broken `#id` links; unlinked `§N` refs | forward-refs to not-yet-built sections |
| `check_svg.py` | malformed `viewBox` arity; literal `_`/`^` in `<text>`; ASCII math placeholders | **the `"0 0 0 0 W H"` bug on ~11 Module-4 figures** (six values, renders browser-dependent) + literal underscores — the first audit's headline finding (07-01) |
| `verify_dom.py` | headless-Chrome: 0 `mjx-merror`, 0 stray `$`; **swallowed-prose** advisory | MathJax typesetting failures invisible in source; the residual shell-mangle case checktex can't see (07-04) |
| `check_overlap.py` | geometric: any label sitting on a curve or dashed reference line | **Module 4's sweep found 11 real overlaps the eye had passed** — "do not eyeball a preview for overlaps" |
| `check_frame.py` | figures **clipped past the viewBox edge** (HARD); wasted-margin (advisory) | added 07-02 for empty margins; **hardened 07-09 to fail on clipping** after 13 Module-10 problem figures put an x-axis title at `y0+30` *below* the box — clipped, and *every other check passed*; a human caught it |
| `check_prose.py` | mechanizable awkward constructions (X-is-X copula, "worth VERBing happen", doubled function words) | the "summation is summation in $a$" line that shipped in a Python-raw-string §4 (07-03) |
| `check_proofs.py` | a `.prop`/`.thm`/`.lem` with no adjacent `.proof` (asserted proposition) | **the Module 6 §6 proof gap** (6.1/6.2 asserted beside a proved 6.3) — the "uniform rigor across siblings" pillar made mechanical |
| `check_code.py` | PEP8 (`pycodestyle`) on every `<pre><code>` block; fails on E303 blank-line spacing, E501 long lines | **Module 8's lab code shipped triple-spaced** — `<pre>` preserves blank lines verbatim (unlike collapsing inter-tag HTML) |
| `check_probfig.py` | problem (C/D/K) figures that are neither a drawn entity nor a labelled plot | **Module 8's C/D/K figures regressed to bare arrows/glyphs** — the "flat physics figure" license read as blanket permission; the 3-layer semantic rule |
| `autolink_sections.py` | rewrites `§N` spans into real links once the section exists | the forward-reference convention (spans without `href`, converted on build) |

Two meta-lessons are baked into these gates:

- **"Every other check passed" is the danger signal, not the all-clear.** The Module-10
  clipping bug and the Module-8 flat-figure regression both slipped through green
  checks — each then *became* a new check. The loop grows precisely at the seams between
  existing gates.
- **Size viewBoxes to content, or trust the gate.** Hand-computed coordinates are
  unreliable (glyph extents, markers, off-scale computed points like an s-plane pole);
  `check_frame` exists because a human cannot eyeball this reliably.

Alongside the loop sit the **math-in-HTML gotchas** that the CHANGELOG and
`math-html-gotchas.md` codify: author math-bearing strings as Python **raw strings**
(`\tau` is a tab, `\nu` a newline, `\boxed` a backspace); **never splice `$…$` through a
double-quoted shell arg** (the shell is `$`- and `\`-active a layer above Python); write
Python figure files with `encoding="utf-8"` on Windows (cp1252 crashes on `σ ε τ ≈ →`);
re-splice figures by **unique `aria-label`, never by `viewBox`** (dims collide and clobber
the wrong figure); assert exactly one splice marker; and renumber `Fig. N` references
after any insert.

---

## 4. Conventions that crystallized

Beyond the gates, a handful of **working conventions** were discovered mid-build and then
made standing policy (in the repo `CLAUDE.md` and the auto-memory):

- **Prose in HTML, Python for figures only (the "leaner way", locked at Module 5).** Early
  modules authored section prose *inside Python raw strings* and spliced the block in —
  which **evaded the read-aloud audit** and shipped awkward phrasing ("summation is
  summation in $a$"). The rule: write prose/proofs *directly in the `.html`* (where
  `check_prose` and the aloud audit see them); use Python only to compute *figures*.
- **Publish-while-incomplete (policy, 07-01).** The moment a `moduleNN.html` is committed,
  wire it into **both** listing pages (`index.html` marked *(in progress)*, `README.md`
  live-URL) — a module goes live as soon as it's committed, not only when finished.
- **MIT-PhD K-depth (retrofitted at Module 5 §10).** Computational (K) problems must
  require **simulation / optimization / an inverse problem / a sensitivity sweep / a
  regime comparison** — never "substitute the numbers into the boxed formula." A plug-in
  problem reveals nothing the derivation didn't; this became a hard reviewer criterion.
- **Tier-2 figures + slim labelled arrows (the Module-3 "figure riddle" lesson).** Anatomy
  gets shaded-primitive Tier-2 SVG (capsule bones, sphere heads, drop shadows); physics
  gets flat schematics — **but** problem-set figures always lead with the recognizable
  entity first (body/joint/foot), never "abstract arrows on a bare line." Never
  AI-generate anatomy. Vectors are thin shaft + small sharp arrowhead
  (`markerUnits="userSpaceOnUse"`), never fat triangles.
- **The reusable figure pipeline.** One hidden `<svg width=0>` `<defs>` block (gradients +
  slim arrow markers) once per module; parametric generators (a posable body, a `Plot`
  helper) emit `<svg>` bodies to JSON, spliced into `<!--FIGN-->` markers. The generators
  are session-transient scratch; the durable record is the committed HTML.
- **Halo every in-plot label** (`paint-order:stroke; stroke:#fff`) so curves under text
  stay legible — *except* white-on-fill labels, which the stroke would bloat (Module 4).

---

## 5. The `rigor-reviewer` agent

By Module 8 the mechanical loop was mature — but it could only prove *syntactic* things.
The gap it could never close is **judgement**: is the rigor *uniform*, does the prose read
aloud like a native wrote it, is a K-problem *deep* or plug-in, is the section
*self-contained*? So on **07-08** an independent reviewer agent was built (`Add agent-team
design docs and the rigor-reviewer agent`) and, the same day, **calibrated and approved**
(`reviewer agent built, calibrated & approved`).

Its design is a deliberate exercise in **least-privilege agent construction** (documented
in `building-a-claude-code-agent.md`):

- **It is one Markdown file** (`.claude/agents/rigor-reviewer.md`) — no service, no
  daemon. Invoked, it boots a **fresh, blank-context** Claude with that file as its system
  prompt, does its work in *its own* context, and returns **one final message**. That
  isolation is the entire value: **fresh eyes**.
- **Tools: `Read, Grep, Glob, Skill` — deliberately no Write/Edit/Bash.** It is *provably*
  read-only; the safety is a consequence of the absent tool, not a hope about behavior.
  ("It judges; it does not rewrite.") Bash was considered so it could re-run the scripts —
  and dropped, because the scripts already run in the caller's loop *before* the reviewer
  is dispatched, and granting Bash re-widens the blast radius.
- **Model `fable`, context fresh (never a fork)** — a fork would inherit the caller's whole
  reasoning and destroy the independence.
- **It judges exactly the four things scripts cannot:** rigor parity, read-aloud prose,
  K-depth, self-containment — loading the acceptance standard via `Skill`
  (`/rigorous-explainer`) and returning structured findings.

The operating pattern, refined across Modules 9–17: after a module's hardening loop hits
zero, dispatch **three reviewers in parallel** over section groups (§0–4, §5–9,
labs+K-depth), collect their findings, apply them in a batch, re-harden to zero, then
commit. The reviewer *judges*; the main loop *fixes*. This is exactly the "when is a
subagent justified" rule from the project memory: a subagent earns its cost only when
**separation itself is the value** (independent review) — not for work the main loop can do.

**The reviewers earn their keep.** Across this project they caught defects that every
syntactic check passed: a Module-10 heuristic that was *quantitatively wrong*; and, in the
autonomous 11–17 run, a real `np.argmax(resid > 1.5*tail)` bug in a Module-15 lab that
printed the wrong cutoff, two Module-16 computational problems that were plug-in and were
recast into genuine sweeps, and a Module-17 damping gain that was **dimensionally
unsound** (`k_d` given units of torque, not torque·time) with a Froude speed that was
arithmetically off. None of these is catchable by a regex; all were fixed before the
module's final commit.

---

## 6. The Codex interlude — enforcing the standard on foreign code

Module 8 is the instructive exception: it was **built by a different tool (Codex)** as a
thin draft (see `CODEX_HANDOFF_REPORT.md`, 07-05), then **elevated to the Module-7
standard** rather than accepted as-is. The elevation exposed two defects the existing loop
did not catch — lab code came out **triple-spaced** (blank lines inside `<pre>` render
verbatim) and the 30 problem figures had **regressed to flat arrows/charts** with no
recognizable entity. Both were fixed (07-08: `reformat lab code blocks to PEP8`, `rebuild
all 30 problem figures to the 3-layer standard`), and — the durable payoff — **both
directly birthed new gates** (`check_code`, `check_probfig`). A foreign contribution
stress-tested the standard and made it stronger: the pipeline now enforces what it had
previously only assumed.

---

## 7. The autonomous run — Modules 11–17

The final phase (07-10) was a single **autonomous `/goal`**: *"complete Module 11–17
without my intervention. Success is defined by all sections meeting the
`/rigorous-explainer` + `CLAUDE.md` requirements and feedback by the rigor-reviewer.
Commit and push per module completion."* Seven modules were built end-to-end with no
human input between the goal and completion — the pipeline running itself.

By this point the **per-module cadence** was a fixed, transferable loop:

1. **Plan the spine** from `prompt.txt` (the course spec) + the forward-references prior
   modules had made to this one.
2. **Build section-by-section** — prose authored directly in the HTML; figure geometry,
   plot data, and animation keyframes *computed in Python* (never eyeballed), emitted to
   JSON, spliced into markers.
3. **Harden after every edit** — all twelve checks to zero; then `autolink_sections`.
4. **Dispatch three `rigor-reviewer` passes in parallel** once the loop is green.
5. **Apply every finding in a batch**, re-harden to zero.
6. **Commit, push, and wire live** into `index.html` + `README.md`.

Each module in this run carried **~40–45 computed figures**, a **30-problem set**
(10 conceptual / 10 derivational / 10 computational, K-depth enforced) plus 5 diagnostics,
**3–4 Python labs** with verified numbers, and every proposition proved. The run delivered:

- **M11** Reaching/Manipulation — two-link kinematics, Jacobian, friction cone, force closure.
- **M12** Whole-Body Coordination — optimal control, LQR, impedance, the uncontrolled manifold.
- **M13** Daily-Life Case Studies — chair-rise, stairs, lifting (L5/S1), stumble recovery.
- **M14** Aging & Adaptation — reserve/margin drift, sarcopenia, osteoporosis, the mechanostat.
- **M15** Measurement & Inverse Dynamics — the measurement-to-torque pipeline + error budget.
- **M16** Continuum & FE Tissue Models — stress/strain tensors, constitutive laws, a working FE solver.
- **M17** Capstone Projects — the modeling method turned onto complete, validated questions,
  closing with a one-page appendix distilling all 17 modules.

The autonomous run is the pipeline's own validation: a method mature enough that seven
substantial, rigorously-hardened, independently-reviewed modules could be produced with
the human setting the goal and the machine — main loop plus reviewer agents — walking the
same disciplined arc each time.

---

## 8. The retrofit — grounding a repair plan in fresh evidence, then repairing under the same reviewer gate

The course was complete and live on 07-10. What followed was a second, adversarial pass:
an external feasibility assessment, a critique of that assessment, a repair plan grounded
in *fresh* mechanical evidence rather than the assessment's inferences, and a parallel,
worktree-isolated retrofit of the earliest modules — each one run through the exact same
build → harden → review → fix loop that closed out Modules 11–17, now proven to also work
on **editing existing rigorous content**, not just authoring new content.

### 8.1 A second opinion, revised, not overwritten

A third party ("Grok 4.5 high") produced `rigorous-explainer-feasibility-assessment.md`:
feasible as a retrofit, not a greenfield rebuild; Modules 1–2 below the current bar;
Modules 3–5 "rigor-thin" (`props ≫ proofs`); Modules 6–16 at bar; Module 17
catalog-incomplete. Asked for a critique of that assessment (not a rewrite), the response
drew on first-hand knowledge of building Modules 11–17 this session — knowledge the
scan-based assessment did not have — and flagged five places where a **structural scan
systematically misreads the codebase**: file size used as a maturity proxy (it isn't —
hardened figures get *smaller* via polyline decimation); a `.prop`-vs-`.proof` `<div>`
count read as a rigor verdict (it can't distinguish a genuine gap from a `.def`, a cited
law, or a mislabeled-but-complete proof); Modules 11–16 filed as "residual polish risk"
when they were in fact built and 3-pass-reviewed under the *current* regime; a stale
`viewBox` bug cited without checking whether it had already been fixed; and Module 17
read as "catalog-incomplete" by a keyword scan that missed content written under a
different name (`prompt.txt`'s "poroelastic" ⟷ the module's actual term, "biphasic
consolidation").

The instruction that followed was explicit and load-bearing for everything after it:
*"revise… preserve what you agree, revise what you have a different opinion… make a new
copy, do not overwrite the existing ones."* `rigorous-explainer-feasibility-assessment-revised.md`
was written as a **new file** alongside the original — a non-destructive-editing norm
that turned out to be the same "do no harm" discipline the retrofit itself would need at
module scale (commit `f899679`).

### 8.2 Ground the plan before writing it, not after

Asked whether the revised assessment could become an implementation plan, the answer was
yes — but only after running **Phase 0**: the full 11-check hardening loop against **all
17 modules**, fresh, before authoring a single task (`phase0.py`, background, ~280 s;
`phase0_result.json`). This is the same "gates over prose" discipline from §2 applied one
level up — to *planning itself*, not just to module content — and it paid off
immediately:

- **8 of 17 modules were failing a hard gate that instant**, and the boundary was
  mechanically **M1–M8**, not the M1–M4 both assessments had guessed. `check_code`
  (PEP8) and clip-hard `check_frame` postdate roughly Module 8 and Module 10
  respectively, so Modules 6–8 — filed as "at bar" by both assessments — were failing
  gates that simply did not exist when they were built and had never been re-run.
- **Reading, not counting, the flagged `.prop`/`.thm` blocks in Modules 3 and 5**
  confirmed the critique empirically: the raw prop-vs-proof gaps (M3 −6, M5 −5) collapsed
  to **~4 real** and **~1–2 real** once `.def` blocks, cited standard laws (Hertz
  contact; Hill's 1938 force–velocity equation), and one derivation that was already
  complete but mislabeled `.prop` instead of `.proof` were excluded. A div count cannot
  make this distinction; reading the boxed text can.

`IMPLEMENTATION_PLAN.md` was written from this ground truth — six phases, cheapest and
most-certain first, with an explicit "do no harm" retrofit discipline (work is corrective,
not a rebuild; never rewrite thin-but-correct structure into verbose bulk) — and committed
alongside the raw inventory as its supporting evidence, not a claim taken on faith
(commit `b675cc1`).

### 8.3 Phase 1 — a mechanical sweep, and a regression caught inside the fix

Phase 1 swept Modules 1–8 to zero on `check_code` and `check_frame` using `autopep8` for
PEP8 and an auto-fitter that applied `check_frame`'s own suggested viewBoxes. The first
version of the PEP8 fixer produced a real regression: it round-tripped each code block
through `html.unescape`/re-escape and, in doing so, **re-escaped live `<a>` section-links
sitting inside code comments into visible `&lt;a&gt;` text** — a defect a systematic
post-fix grep across every touched file caught immediately, not a defect that shipped.
The fix protects live HTML tags with placeholders across the unescape/escape round-trip,
the same "protect the thing the tool doesn't know is there" pattern behind the shell-arg
math-splicing gotcha in §2.

Fixing the clips surfaced a second, more interesting bug: Module 6's tangent-stiffness
curve (the dashed-blue $k = \mathrm{d}F/\mathrm{d}x$ line) wasn't a viewBox-sizing
problem at all — its plotted y-values diverged to **−193,883**, a wrong-formula
figure-generation bug that had shipped and passed every prior check, only surfaced
because `check_frame`'s clip detector forced a look at what the figure was *actually
plotting*. It was regenerated from the correct piecewise-linear stiffness law
($k(x) = k_\text{lin}\min(x/x^{*},1)$) rather than papered over with a bigger box —
exactly the "size viewBoxes to content, or trust the gate" lesson from §3, this time
applied to a case where the gate exposed a physics bug, not a layout one (commit
`a3d1aed`).

### 8.4 Parallel retrofit — the same loop, now applied to editing, not authoring

| Track | Scope | Isolation |
|---|---|---|
| M1, M2 | Full Phase 2–4 (proofs, domain fixes, 30-problem sets) — the two largest tracks, run first | worktree agent, Opus |
| M3, M4, M5 | Phase 2–3 (proofs + named domain fixes) — smaller, run in parallel once M1/M2 landed | worktree agent, Opus |
| M7, M12 | One or two bare problem figures each (`check_probfig` flags) | worktree agent (M7) / solo (M12) |

Each track ran the **exact cadence from §7**: build/fix → harden every gate to zero →
commit inside an isolated worktree → report → the coordinator merges (disjoint files, so
every merge was conflict-free) → re-verifies the full gate set on the merged result →
dispatches one or more `rigor-reviewer` passes → applies every finding → re-hardens →
commits. The only change from the greenfield M11–17 run is what the loop is *applied to*
— existing, previously-shipped content, not a blank section — which is a materially
different job (do-no-harm discipline, preserve what's already correct) proven to work
under the same pipeline.

### 8.5 The reconciliation problem parallel agents create

The sequential M11–17 build never had this problem: each module was built *after* the
ones it referenced, so a forward-reference always pointed at something that already
existed in its final form. Parallel agents editing **disjoint files simultaneously**
cannot see each other's edits, so any fact shared across files needs a coordinator
reconciliation pass **after** every track merges — a new discipline this phase
introduced to the pipeline, illustrated by three concrete instances:

- **A wrong citation, caught and fixed.** Module 2 cited "Module 1, §6" for the
  single-leg-stance hip joint-reaction number (2.5× body weight ≈ 1715 N); the actual
  derivation lives in Module 3 §4. Retargeted post-merge (commit `0f31652`).
- **"More correct" is not always the right fix — a do-no-harm judgment call.** Asked to
  reconcile Module 3's hip-reaction ratio (a boxed 2.5×W vs. an audit note suggesting
  ~3×W once the abductor's line of action is inclined), the Module 3 agent computed the
  honest resultant magnitude (**≈2.7×W**, tilted ~21° from vertical) — and then
  deliberately did **not** overwrite the boxed 2.5×W value, because that number is
  load-bearing in two other places: Module 2's citation, and Module 4's contact-pressure
  integral ($\int p\,\mathrm dA = 1715\,\mathrm N$). It added the refinement as a
  documented sibling `.keyresult` instead — recognizing that a *more precise* number
  had a larger blast radius than the imprecision was worth fixing (commit `079f409`).
- **An agent-to-agent handoff, mediated by merge order.** The Module 4 agent gave the
  Hertz-contact proof a stable anchor (`id="hertz"`) and, in its own report, explicitly
  recommended that Module 3's forward-reference retarget there instead of the coarser
  section-level anchor it had used. Because the coordinator merged Module 4 before
  reconciling Module 3's link, that recommendation could be applied precisely — a
  cross-track dependency resolved by a human/coordinator reading both reports, not by
  the agents coordinating directly (commit `890723a`).

### 8.6 What the reviewer caught this time

The reviewer gate (§5) earned its keep again, on retrofit work specifically:

- **A scrambled assembly that passed every mechanical gate.** Module 1's rebuilt
  30-problem set shipped with D8 and D10's *statements* silently missing, D7 and D9
  each holding the *other's* mismatched figure and solution, and K8's figure swapped
  into the wrong slot — and all 11 hardening checks were green. This is the same
  "every other check passed" pattern that birthed `check_code` and `check_probfig` in
  §3 and §6, now shown to recur on a *retrofit*, not only a fresh build — mechanical
  syntax gates cannot see that a section answers the wrong question. It was fixed by
  **resuming the same builder agent inside its own worktree** (it retained its own
  figure generators and full context, rather than starting a fresh agent from scratch),
  then verified by a **second, narrowly-scoped reviewer pass over only the previously
  broken parts** — cheaper and more targeted than a full re-audit (commits `7bf792c`,
  `883935a`).
- **A disguised plug-in problem, deepened.** Module 2's K6 (allometric scaling) merely
  evaluated an already-derived scaling law at five body masses and called it a "regime
  comparison" — the exact plug-in-dressed-as-computation failure the MIT-PhD K-depth
  standard exists to catch. Deepened into a genuine two-regime comparison with a
  numerically `brentq`-solved yield-crossover mass, figure regenerated to match
  (commit `96092cd`).
- **A physics/notation bug invisible to syntax, obvious to a reader.** Module 7's D4
  figure labeled the center-of-mass *velocity* with an acceleration dot ($\dot v$)
  where the governing equation ($\xi = x_\text{com} + \dot x_\text{com}/\omega_0$)
  needs velocity, not acceleration — a one-character error no script checks for, caught
  by a reviewer reading the figure against the equation it illustrates (commit
  `4e02ae7`).
- **Rigor-parity applied to how an exemption is framed, not just how a proof is
  written.** Module 5's Prop 6.1 (Hill's 1938 force–velocity law) was correctly left
  unproved as a cited empirical result — but its sibling Prop 3.1 stated that exemption
  *inside its box*, while Prop 6.1's lived only in the surrounding prose. Moved in-box
  to match: the "uniform rigor across siblings" pillar (§2) extended to *how an
  exemption reads*, not only to which results carry a `.proof` (commit `42f5220`).

### 8.7 Closing the loop on the pipeline's own documentation

The retrofit's last phase turned the same discipline on the project's own conventions:

- **`CLAUDE.md` and `AGENTS.md`'s own hardening-loop lists had drifted behind the
  skill's actual 11-script set** — both were missing `check_svg`, `check_code`, and
  `check_probfig`, which exist and have been enforced all session. The exact "gates over
  prose" lesson from §2, now shown to apply to the *conventions layer itself*, not only
  to module content — a written rule can drift even when the mechanism it describes has
  moved on.
- **`AGENTS.md` pointed at a skills path that does not exist on this machine**
  (`~/.Codex/skills/…`) — a broken reference found only by attempting to verify it
  (`ls`), not by reading the text, which read as perfectly plausible. Repointed to the
  canonical, verified `~/.claude/skills/…` install (commit `0366aae`).
- **A real accessibility gap, closed:** three modules (1, 3, 4) had live SMIL
  animations that predated the template's `prefers-reduced-motion` freeze guard and had
  never received it.
- **`HANDOFF.md` had gone stale** — it still presented the Module 11–17 completion as
  "current state" with no mention of the retrofit. Rewritten, with the genuinely
  remaining low-priority polish items (course-wide SVG typography, figure-by-number
  citations, an inter-module nav rail) listed **explicitly** rather than left implicit —
  mirroring the reviewer's own discipline of distinguishing what was fixed from what was
  deliberately deferred, instead of letting silence stand in for either (commit
  `2a6f6f6`).
- **A final, full-course Phase-0-style sweep** — all 11 checks against all 17
  modules — confirmed **0 hard-gate failures**, closing the loop the retrofit opened.

## 9. What the journey actually produced

The visible artifact is a 17-module course that has now been built once and repaired
once, under the same discipline both times. The **durable** artifact is a reusable
authoring-*and-repair* system with three interlocking parts, each with a clear job:

- **The skill** encodes *what "rigorous and well-taught" means* (five pillars + template +
  references) — the standard.
- **The hardening loop** makes the mechanizable half of that standard **pass/fail**, so it
  can't drift under load — and it *grows a gate every time a new class of defect escapes*.
- **The reviewer agent** judges the un-mechanizable half with fresh, provably-read-only
  eyes — and it grows sharper as its findings feed back into the skill.

The through-line is a single discipline: **convert every mistake into a rule, every
crisp rule into a gate, and every judgement the gates can't make into an independent
reviewer.** That discipline, not the seventeen HTML files, is the result — and it is why
the last third of the course could build itself, and why the earliest third could later
be *repaired* by the same means: a plan grounded in fresh gate output rather than
inherited assumptions, parallel work isolated enough to be safe and reconciled enough to
stay consistent, and a reviewer that does not get more lenient just because the content
it's reading was written by an earlier version of the same pipeline.

---

*Sources: this repo's git history (2026-06-28 → 2026-07-11); the skill `CHANGELOG.md`;
`skill-change-list.md`, `skill-improvements-from-audit.md`, `audit-modules.md`;
`building-a-claude-code-agent.md`, `when-to-spawn-a-subagent.md`; each hardening script's
header comment; `CODEX_HANDOFF_REPORT.md`; `CLAUDE.md`, `AGENTS.md`, `HANDOFF.md`; the
retrofit's own record — `rigorous-explainer-feasibility-assessment.md`,
`rigorous-explainer-feasibility-assessment-revised.md`, `IMPLEMENTATION_PLAN.md`, and
`phase0_result.json` — and the project auto-memory. Compiled at completion of the
17-module course (§1–§7) and updated at the close of the subsequent retrofit (§8–§9).
Session-level texture of the earliest modules resides in the (unread, backed-up)
transcripts under `claude-transcripts/`.*
