# Development Journey — Method & Tooling

*How a 17-module, rigorously-hardened biomechanics course got built in ~13 days — and,
more importantly, how the **`rigorous-explainer` skill**, its **hardening loop**, and the
**`rigor-reviewer` agent** co-evolved with it into a repeatable, largely-autonomous
authoring pipeline.*

This report foregrounds the **method and the tooling**, not the course content. It is
assembled from durable artifacts — the repo's git history (138 commits, 2026-06-28 →
2026-07-10), the skill's own `CHANGELOG.md`, the audit and change-plan docs, each
hardening script's "WHY THIS EXISTS" header, the agent-design docs, and the project
memory — not from raw session transcripts. Where a claim rests on a specific dated
commit or documented incident, that is the evidence; the granular within-session
narrative of the earliest modules lives only in the (large, deliberately un-read)
transcripts and is summarized here, not reconstructed.

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

## 8. What the journey actually produced

The visible artifact is a 17-module course. The **durable** artifact is a reusable authoring
system with three interlocking parts, each with a clear job:

- **The skill** encodes *what "rigorous and well-taught" means* (five pillars + template +
  references) — the standard.
- **The hardening loop** makes the mechanizable half of that standard **pass/fail**, so it
  can't drift under load — and it *grows a gate every time a new class of defect escapes*.
- **The reviewer agent** judges the un-mechanizable half with fresh, provably-read-only
  eyes — and it grows sharper as its findings feed back into the skill.

The through-line is a single discipline: **convert every mistake into a rule, every
crisp rule into a gate, and every judgement the gates can't make into an independent
reviewer.** That discipline, not the seventeen HTML files, is the result — and it is why
the last third of the course could build itself.

---

*Sources: this repo's git history (2026-06-28 → 2026-07-10); the skill `CHANGELOG.md`;
`skill-change-list.md`, `skill-improvements-from-audit.md`, `audit-modules.md`;
`building-a-claude-code-agent.md`, `when-to-spawn-a-subagent.md`; each hardening script's
header comment; `CODEX_HANDOFF_REPORT.md`; `CLAUDE.md`, `HANDOFF.md`, and the project
auto-memory. Compiled at completion of the 17-module course. Session-level texture of the
earliest modules resides in the (unread, backed-up) transcripts under `claude-transcripts/`.*
