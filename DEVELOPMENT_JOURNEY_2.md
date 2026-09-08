# Development Journey — the editor pass over Modules 3–17

**Date:** 2026-09-07 into 2026-09-08 (one continuous session, three usage-limit interruptions)
**Deliverable:** `edited/module03.html` … `edited/module17.html` — fifteen edited drafts, plus `editor-reports/module03.md` … `module17.md`, fifteen reports each ending in a change-log table
**Brief:** "OK can you just apply the Editor skill to all the modules that have not changed ? do not overwrite the original ones. do not do it one by one. complete all of them. write a detailed log what have been changed for each module. ask me any questions"
**Final state:** commit `a93a55c`, pushed to `main`. 1,214 logged edits across fifteen modules.

---

## 1. The brief — what was actually being asked

The session did not start here. It started with `/clear` and `@HANDOFF.md`, which named a
much narrower job: apply the already-written Module 3 report, then write the Module 4
report, one module per session, twelve sessions to go.

Twenty minutes in — mid-tool-call, while I was reading the Module 3 mobility figure — the
brief above arrived and replaced it.

Four instructions, and each one changed the shape of the work:

- **"apply the Editor skill"** — apply, not report. The `science-editor` skill produces a
  report *and* the fixes; the deliverable is the edited file, not a critique.
- **"do not overwrite the original ones"** — the fifteen live course pages stay untouched.
  This is what created `edited/`.
- **"do not do it one by one"** — parallel. This is the instruction that overrode the
  standing rule in my system prompt against reaching for the Agent tool unprompted.
- **"complete all of them"** — no stopping at the easy half.
- **"ask me any questions"** — an explicit invitation, which I used once, immediately.

**The ambiguity I resolved by asking rather than guessing.** "All the modules that have
not changed" could mean 3–17 (Modules 1 and 2 were already edited in place) or could mean
something narrower. I read it as 3–17, fifteen modules, and the three questions I asked
settled everything else that mattered.

**Invisible constraints in force the whole session**, none of which appear in the output
but all of which shaped it:

| Constraint | Source | Effect |
|---|---|---|
| ASD-STE100 Simplified Technical English | global `CLAUDE.md`, always on | every reply in short active sentences, one meaning per word, every number and path preserved exactly |
| Ponytail mode, level `full` | `SessionStart` hook | the ladder — does this need to exist, can stdlib do it, can it be one line — applied to my own tooling, not to the modules |
| `superpowers:using-superpowers` | `SessionStart` hook | check for an applicable skill before any response |
| Nine hard gates, all zero | project `CLAUDE.md` | the acceptance bar every agent worked to |
| Commit and push per work unit without asking | project `CLAUDE.md`, standing rule | why nine commits landed without me asking permission each time |
| Coach nudges at 175k, 204k, 218k, 257k, 301k context | `UserPromptSubmit` hook | escalating pressure to hand off and `/clear`, which I acted on partially and late |

---

## 2. Cold start — what the session inherited and reused

`/clear` had wiped everything. What survived was on disk, and reusing it rather than
re-deriving it was the single largest time saving of the session.

- **`HANDOFF.md`** gave the state in one read: which modules were done, which owed what,
  and — critically — the **three traps** that had cost real time on Modules 1 and 2. Those
  three warnings went verbatim into every agent prompt, and one of them (the raw-string
  backslash) fired for real in Module 10 hours later.
- **`editor-reports/module03.md`**, 405 lines, already written by a previous session. That
  meant Module 3's agent could skip straight to verification and applying.
- **`EDITOR_DOMAIN.md`** — the domain brief the `science-editor` skill reads, including the
  rule that does most of the work: *every number is derived, a table parameter with symbol
  and unit, or an assumption labelled as such; anything else is a blocking defect.*
- **`editor-reports/module02.md`** as the format model, so fifteen agents would produce
  reports in one shape rather than fifteen.

What was **not** reused, and had to be rebuilt: the scratchpad toolkit. `HANDOFF.md`
described `extract.py` and `txt.py` in enough detail to rebuild them in ten lines each,
which is exactly what a handoff should do for session-transient files.

---

## 3. Design decisions

### 3.1 Where the edited files go — `edited/moduleNN.html`

Options: a new `edited/` folder; `moduleNN-edited.html` beside each original; or a git
branch with edits in place.

**Chose `edited/`.** The branch loses: the working tree would show the live files as
modified, and every gate run would need to know which branch it was on. The suffix loses:
fifteen more files in a root that already holds forty. `edited/` gives a clean `git diff`,
leaves `index.html` and `README.md` pointing at the originals, and makes promotion one
`mv` per module.

**What it cost, and I flagged it at the time:** committing `edited/` publishes the drafts
to GitHub Pages at `/edited/moduleNN.html`. They are unlinked, so nothing finds them
without the URL, but they are public. I raised this before the first commit, got no
answer, and committed anyway — leaving verified work uncommitted was the larger risk with
usage limits killing fleets. The reversal is recorded in `HANDOFF.md`.

### 3.2 Depth — the full pass on all fifteen

Options: the full treatment everywhere; the full treatment only on code-heavy modules with
a lighter pass elsewhere; or a fast claims-and-prose pass on all fifteen.

**Chose the full pass everywhere**, at the user's direction. The middle option was the one
I distrusted most: it required me to guess in advance which modules had number problems,
and the whole finding of this session is that **you cannot tell from the outside**. Module
14 looked like a light one and turned out to have ten computational problems carrying no
code at all.

### 3.3 Verification — gates only, no render sweep

The user chose gates only. This was the right economic call and it was also wrong in a
specific way that the session then discovered: the gates cannot see wrong content. The
agents worked around it themselves by decoding figure geometry numerically instead of
rendering — cheaper than a render sweep and catching a defect class rendering would miss.
Two agents rendered anyway, at their own initiative, and both found things.

### 3.4 One shared brief file instead of fifteen prompts

Not a decision I made up front — a correction after the first fleet died. See §6.2.

### 3.5 Descoped deliberately

- **No render-verify sweep** — the user's call, discussed above.
- **No promotion.** Nothing was moved into place. `index.html` and `README.md` still point
  at the originals. Promotion is a decision about fifteen live pages and it is the user's.
- **No `.gitignore` for `edited/`** — raised, unanswered, left committed with the undo
  documented.
- **The wasted-margin viewBox advisories** (8 in m10, 17 in m13, 14 in m16, and more) were
  left alone by every agent that met them. Retightening a viewBox risks turning a cosmetic
  advisory into a clipping hard failure, and `check_frame` declines to force it for exactly
  that reason.

---

## 4. The crux — the gates see broken content, not wrong content

Every session has one finding that reorganises it. This one arrived from three agents
independently, none of whom had been told to look for it.

The project has nine hard gates. They are good gates: `checktex` balances math delimiters
and catches the control characters a mangled shell command leaves behind; `check_overlap`
loads the page in headless Chrome and geometrically tests every label against every curve;
`check_frame` compares each figure's rendered bounding box to its viewBox; `check_code`
runs pycodestyle over every Python block. Modules 1 and 2 had already taught that they are
necessary and not sufficient — `HANDOFF.md` said so in as many words.

What this session established is the *shape* of the insufficiency.

**A gate tests whether the page is broken. It cannot test whether the page is wrong.**

- Module 6 shipped a figure caption describing an x-axis the figure does not have. Valid
  HTML, valid TeX, no overlap, correct frame. Green.
- Module 9's K6 figure was a byte-identical copy of K3's — the same 549-character point
  string — so it drew required stopping distance *falling* with drop height, against its
  own formula `d_s = h/5`. A perfectly well-formed polyline. Green.
- Module 12's Lab B ran 40% of its settling-time curve outside the plot frame, reaching
  17.9 s on a 10 s axis, with the viewBox stretched to `6 -81 488 339` to keep
  `check_frame` quiet. A gate actively worked around, and still green.
- Module 14's Lab C runaway was clamped flat against the 9 MPa axis ceiling from year 43,
  under a caption claiming a runaway. Green.
- Module 15's K7 figure drew superseded numbers under an `aria-label` reading "K4: The
  exercise shows the recursion…" — which is K6's text. Green.

**The technique that catches them, arrived at independently by Modules 6, 11 and 14 and
then adopted by everyone: decode the `<polyline>` point string back into data.** Calibrate
the axis mapping, invert it, and compare the recovered series against the model the caption
claims. It needs no browser, and it tests the one thing no gate tests — whether the picture
shows what the words say it shows.

Module 4 sharpened it further: **calibrate from the axis `<line>` elements, not the tick
`<text>` baselines.** Those baselines sit about 3 px low, and that offset alone shifts a
recovered peak pressure by 0.065 MPa — enough to manufacture a discrepancy that is not
there. A verification technique with a systematic bias is worse than none.

Module 15 then found the technique's own limit. It rendered its regenerated figures and
found a crossover label sitting on top of another label, and an optimal curve hidden
underneath the truth curve. Neither is visible to any gate — `check_overlap` tests text
against curves and dashed lines, never text against text — and neither is visible to a
decode either, because the data is correct; it is the *layout* that is wrong.

**The rule that came out of it, now in `HANDOFF.md` and in memory:** gates catch broken,
decode catches wrong data, rendering catches wrong layout. Three different instruments.
Running one and reporting done is how every one of these shipped in the first place.

### 4.1 The second recurring finding

**A module that claims its numbers came from running its code usually has problems carrying
no code at all.**

- Module 14 said so three times over. Its ten computational problems carried not one line.
- Module 15's line 599 made the same claim; four of nine problems quoted numbers no listing
  printed.
- Module 11 had three of four labs printing nothing.
- Module 3's §7.4 lab computes the shoulder reaction, the elbow reaction and the multiplier
  inside its integration loop and then overwrites all three on the next iteration. No
  `print`, no array, no return. A reader who copies out those forty lines and runs them
  sees nothing at all — while §9.4 promises "every number quoted below was produced by
  running the code."

This is why the brief's step 4 — *run the code before you read the prose* — is the
highest-yield step of the whole pass, and why it is step 4 and not step 9.

---

## 5. Tools and features used

| Tool | What it did *this session* |
|---|---|
| `Agent` (general-purpose) | 15 + 12 + 7 + 3 spawns across four fleets. Each agent read the shared brief, did one module, and returned ≤10 lines. Chosen over `Workflow` because 15 sits at the workflow size guideline and the user's opt-in language was for parallelism, not orchestration. |
| `Skill` → `science-editor` | Every agent's first call. Supplies the five-part standard: precise statement, every term defined, proof in the smallest setting, rescue or limit case, tie to something concrete. |
| `advisor` | Consulted once, before launching. It changed the plan — see §6.1. |
| `AskUserQuestion` | Once, three questions: output location, depth, verification. Answered in one round; no further blocking questions were needed. |
| `Bash` | Inventories, gate runs, all fifteen commits. Used in preference to Read/Edit per the bypass-mode instruction. |
| `Write` / `Edit` | `HANDOFF.md`, `BRIEF.md`, the toolkit, this document. Never used for math-bearing strings through a shell. |
| `checktex.py` `checklt.py` `check_links.py` `check_svg.py` `check_code.py` `verify_dom.py` `check_overlap.py` `check_frame.py` `check_bodyprop.py` | The nine gates, run twice per module — once on the pristine copy for a baseline, once on the edited file. |
| `check_prose.py` `check_proofs.py` `check_probfig.py` | Advisories. `check_proofs` improved on baseline in Module 5, where Propositions 3.1 and 6.1 had been flagged as asserted and are now proved. |
| `extract.py` (written this session) | Pulls every `<pre><code>` block to a runnable `.py` and flags live HTML tags inside code. Ten lines. |
| `txt.py` (written this session) | Dumps a line range as readable text with `<svg>` collapsed, UTF-8, never truncated. |
| `apply_skel.py` (written this session) | The `rep(old, new, tag)` skeleton that asserts each anchor occurs exactly once. |
| Headless Chrome | Behind four of the nine gates, and used directly by two agents for render checks. |

### 5.1 Architecture of the run

```
lead session
  ├── scratchpad/tools/BRIEF.md      ← one 117-line brief, read by every agent
  ├── scratchpad/tools/{extract,txt,apply_skel}.py
  └── 15 agents, one per module
        ├── cp moduleNN.html → edited/moduleNN.html
        ├── nine gates on the pristine copy      → baseline
        ├── extract.py → run every code block    → diff printed vs claimed
        ├── read the module against the standard → editor-reports/moduleNN.md
        ├── scratchpad/mNN/apply.py              → one pass, each anchor asserted unique
        ├── nine gates on the edited file        → ≥ baseline
        ├── decode every touched polyline        → compare against the model
        └── ## 6. Changes applied table          → the user's log
```

No agent ran a writing git command. The lead committed after each module landed — nine
commits, each pushed.

---

## 6. What went wrong, and the fixes

### 6.1 The advisor changed the plan before it started

Consulted once, after orientation and before launching. It gave two pre-flights I had not
planned, and both paid:

**Pre-flight one: baseline the gates on a pristine file first.** Modules 3–17 predate
`check_frame` and `check_bodyprop`, so a non-zero gate might be the module's, not the
pass's. Running the nine on an untouched `module17.html` showed all nine clean — which
made "zero, and never worse than baseline" a meaningful acceptance rule rather than a hope.

That run also surfaced a real operational fact:

```
[check_overlap] chrome failed: Command '[...chrome.exe, --headless=new, ...]'
timed out after 120 seconds
```

A cold Chrome start exceeds the gate's own 120 s timeout. Warm, the same file takes 7.1 s.
Every agent prompt from then on said: a Chrome gate that times out is cold-start
contention, wait ~60 s and retry once. Without that line, fifteen agents would each have
reported a false gate failure.

**Pre-flight two: write the toolkit once.** Fifteen agents each writing their own ten-line
`extract.py` is waste and gives fifteen behaviours.

The advisor also caught something I had missed while reading the Module 3 report. Its B13
supplies a new caption claiming the mobility curve is `ROM(β) = 180° − β − 30°` normalized.
The polyline actually on the page runs linearly from y=30 at β=10° to y=195 at β=70° —
that is `(90−β)/80`, normalized 1.00 → 0.25, where the caption's formula gives 1.00 → 0.57.
Applying the report as written would have shipped a caption contradicting its own figure.
That went into Module 3's prompt as a required regeneration.

### 6.2 Three agent fleets killed by usage limits

```
idleReason: "failed"
failureReason: "You've hit your session limit · resets 11:10pm (America/Los_Angeles)"
```

Then again at 4:10am, and again at 10:50am.

**Fleet 1** (15 agents) died having written 7 reports and applied nothing. **Fleet 2** (15
agents) got 3 modules fully through. **Fleet 3** (12 agents) got 6 more. **Fleet 4** (7
agents) finished the rest.

`autoContinueAtUsageLimit: true` is set in `~/.claude/settings.json`, and it saved the lead
session — but **it does not save subagents**. That is worth knowing before launching a
fleet: the lead survives, the fleet does not.

**What made the losses survivable** was that every agent wrote to disk continuously — report
first, then the apply script, then the gates. Each relaunch resumed from files, not from
context. Total unrecoverable loss across three fleet deaths: one partial apply (Module 4's
98 lines) which I reset to pristine and redid.

**The fix that made relaunches cheap.** Fleet 1 put the full brief inside all fifteen
prompts, which burned the lead's context for no gain. Fleet 2 onward put the brief in
`scratchpad/tools/BRIEF.md` and gave each agent a six-line prompt naming only its own
state. Fleet 1: zero modules through. Fleet 2: three.

### 6.3 I sent three agents a wrong premise — three different ways

This is the failure I am least comfortable with, because it repeated after I should have
learned it.

| Module | What I told the agent | What was true | What I inferred it from |
|---|---|---|---|
| 17 | "an unresolved `$I$` symbol collision" | Already fixed, applied, in `apply.py` | The dead agent's last message: *"Now I'll write the new `rep()` block for the unresolved `$I$` collision"* |
| 7 | "apply PARTIAL (175 lines) — reset and re-run" | Complete: 79 edits, two runs byte-identical | The changed-line count |
| 8 | "two known open defects: a literal `_` in an SVG `<text>` and K10's frame" | Both already fixed inside the inherited `apply.py` | The dead agent's last message |

Each agent caught it the same way: by reading the files instead of believing me. Module 17
re-scanned every `$…$` segment for a bare `I` and found 12 hits, all legitimately §2's
ankle inertia. Module 8 proved `check_svg` was at 0 hard rather than re-fixing.

**The rule, now in `HANDOFF.md`:** a dying message names the *next* step, not an undone
one. A changed-line count is not an apply state. State the suspicion, never the conclusion,
and let the agent establish state by re-running from pristine and comparing bytes.

### 6.4 The raw-string trap fired for real

`HANDOFF.md` warned that in a Python raw string `r'…\'…'` the backslash survives, so the
anchor never matches — and the script dies before its single `write_text`, leaving the file
untouched while the log still looks plausible.

Module 10 hit it in **19 anchors** at once. Fixed by a token-level rewrite; the re-run from
pristine is byte-identical.

Module 3's agent hit a variant that the warning did not cover: a `"""` docstring inside a
replacement code snippet terminated the surrounding Python raw string. It died mid-repair.
On relaunch I told it to use `'''` for the outer string or read snippets from files.

Module 15 found the same family in its own script — non-raw `\s` and `\ ` sequences at
`apply.py:814–821` that would silently no-op the whole apply under a stricter Python.
Caught before it bit.

### 6.5 The editor pass introduced a defect of its own

Module 7's B4a rewrote K8's problem statement and left the figure's `aria-label` carrying
the superseded one. Found by machine-comparing all 23 problem aria-labels against their
statements.

This reframes "residue" — the class of defect where a replacement is made and the old value
survives somewhere else. It is not only the module's pre-existing debt. **An edit creates
it.** Every module that swept for residue found some; the sweep is now part of the recipe.

### 6.6 A near-miss: the agents' own reports were sometimes wrong

Module 6 was applying a report written by its own predecessor and found that the report's
replacement caption for Figure 16 was factually wrong about the figure — it described an
axis the drawing does not have. Every gate was green on the wrong caption. Only reading the
SVG geometry caught it.

Six of that report's claims lost to the agent's own runs. Module 3's agent corrected four
of its predecessor's, including a 1.6 mm outward start blamed on numerical settling that is
ordinary offset-slider-crank kinematics. Module 8 **reverted** one of the previous pass's
edits with a reason: K4's 36.8% had been "corrected" to 36.9%, but the module's standard is
a number the reader can reproduce by running the module's own code, and Lab 2 prints
36.844%. Restoring 36.8% also made K1's 0.344 and §7's 8.2% consistent, which they were not
while 36.9% stood.

**The rule every agent was given, and used:** if a number disagrees with your run, your run
wins — correct the report and say so.

### 6.7 A report describing an edit is not evidence the edit landed that way

Found while writing this document. The three extraction agents were told to quote exact
before/after text, and one of them grep-verified every quote against `moduleNN.html` and
`edited/moduleNN.html` instead of trusting the report it was reading. That caught two
places where the *applied* text differs from the *proposed* text:

- Module 4's C5 caption shipped `2.54 MPa` / `23.3 mm` phrasing the report never printed.
- Module 7's K2 solution shipped `4.44` where the report wrote `4.45`.

Both are benign — an agent refining its own wording between proposing and applying. But
the class is not benign, and it is the session's core lesson one level up: a document
describing a change is not the change. The change-log tables are a map, and the file is the
territory.

### 6.8 Drift between modules

Module 8's agent, checking the cross-module debt, found a defect in Module 3 — already
committed, already pushed. `edited/module03.html:858` states the hip resultant as "2.6 to
2.8 W across 20° to 40°", but |R| at 40° is 2.87 W. A sibling agent's edit.

It reported rather than reaching into another agent's module, which was correct. Logged as
an open item and still open.

---

## 7. Verification

### 7.1 What "the apply worked" was made to mean

Early modules asserted it. Module 16 replaced the assertion with a proof, and every module
after it adopted the method:

1. Reset to pristine, re-run `apply.py`, confirm the output is **byte-identical** to the
   edited file. This is the only test that rules out the script dying before its single
   `write_text`.
2. Confirm the applied tag count equals the change-log row count, in order.
3. Confirm each row's stated line is the anchor's true first line in the pristine file.

Module 16: 55 tags, 55 rows, 0 mismatches. Module 13: 102 `rep()` calls, byte-identical.
Module 4: 107 edits, `REPLAY ok` / `IDENTICAL`. Module 17 ran it three times.

### 7.2 The gates

Every module: nine gates on the pristine copy for a baseline, nine on the edited file,
acceptance being **zero where the baseline was zero and never worse anywhere**. Several
came out ahead of baseline:

- Module 8: `check_frame` advisories 8 → 3; `verify_dom` stray-`$` 36 → 24.
- Module 9: `check_bodyprop` 1 advisory → 0; swallowed-prose 1 → 0.
- Module 13: stray-`$` 18 → 16.
- Module 7: stray-`$` 28 → 26.
- Module 5: `check_proofs` flagged Propositions 3.1 and 6.1 on the baseline, 0 after.
- Module 6: `check_prose` 1 → 0.
- Module 10: `check_bodyprop` 3 advisories → 2.

### 7.3 The code

Every `<pre><code>` block re-extracted **from the edited file** — not the original — and
run. Module 13 needed `MPLBACKEND=Agg` because four blocks end in `plt.show()`. Block
counts grew where problems had been given the code they claimed to have: Module 6 3 → 13,
Module 14 4 → 14, Module 13 4 → 14, Module 5 2 → 12, Module 10 4 → 10, Module 15 → 9.

### 7.4 The figures

Decoded numerically, not eyeballed. Some examples of the standard reached:

- Module 4: all four pressure figures fit their claimed shape two orders of magnitude
  better than the rival shape, and integrate to 1714.2 N against a stated 1715 N. K4
  measures a peak-to-plateau ratio of 2.000 off the drawn axis and matches `1+F(T)` at all
  300 points. K10's swelling curve reproduces the Donnan formula to 1.3e-4 MPa.
- Module 5: Figure 30's rebuilt ellipse intercepts are 105.5 and 164.0 N, ratio 1.5545
  against §1's 210/135 = 1.5556 — the old figure was 70.7 and 141.4, exactly 1:2. The
  optimum marker was then confirmed a true tangency by substitution: 0.7170² + 0.6976² =
  1.0008.
- Module 16: Lab C's two polylines give F = 0.9660 → 0.2347 and U = 0.0340 → 0.7653, with
  F + U = 1 to machine precision, crossing 0.5 at T = 0.1945 exactly where the dashed line
  sits.
- Module 3: the lab re-derived independently in joint-angle coordinates with RK45, no
  Baumgarte stabilization, joint forces recovered by least-squares Newton to a residual of
  **3.9e-14 N** — sharing no code with the module. Every headline number reproduced.

### 7.5 What was not verified

- **No full render sweep.** The user chose gates only. Two agents rendered at their own
  initiative and both found layout defects, so the class is real and mostly unexamined.
- **The wasted-margin advisories** were left as they were found, on judgement.
- **Nothing was verified in a browser by a human.** The drafts are live at
  `az9713.github.io/biomechanics/edited/moduleNN.html` and unread by anyone.
- **The 1,214 change-log rows were not audited by the lead.** Each agent verified its own
  and several verified programmatically, but I did not read them. The per-module section
  below is a representative sample drawn from those tables, not an exhaustive audit.

---

## 8. Costs, limits and fragility

- **Three usage limits hit**, resetting 11:10pm, 4:10am and 10:50am America/Los_Angeles.
  Each killed a fleet mid-run. `autoContinueAtUsageLimit` saved the lead and not the
  subagents.
- **Lead context reached ~301k tokens**, with coach escalations at 175k, 204k, 218k, 257k
  and 301k. The `BRIEF.md` move at fleet 2 was a direct response. Committing incrementally
  — nine commits rather than one at the end — was the other.
- **Wall clock:** roughly 24 hours elapsed, most of it waiting on limits.
- **Fragile and worth naming:** the cold Chrome start (120 s timeout, 7 s warm) is timing
  dependent, and fifteen concurrent agents make it worse. A git push of the fifteen edited
  files twice exceeded the 120 s foreground timeout and had to finish in the background.
  One agent edited a sibling's scratchpad folder (`m08b/genk.py`) while that sibling's name
  was still live — harmless because the sibling was dead, but it was luck, not design.

---

## 9. Knowledge captured

- **`HANDOFF.md`** — rewritten twice and now final: the per-module state table with counts
  and commits, the reusable ten-step brief, the three verification instruments, the
  "never infer state from a proxy" rule, the "an edit pass can introduce residue" rule, and
  the one open drift.
- **Memory, `render-verify-beats-gates.md`** — extended with the sharper statement (gates
  see broken content, not wrong content), the polyline-decode technique, and the
  calibrate-from-axis-lines refinement.
- **`editor-reports/moduleNN.md` × 15** — the durable record of what was wrong and the exact
  fix, each ending in its change-log table.
- **Nine commits**, `f028bfc` through `a93a55c`, each carrying the finding in its message
  rather than just the file list.

---

## 10. What changed in each module

Below: for each module, the scale, the verdict, the one defect that mattered most, and a
representative sample of before/after pairs spanning prose, math, figure geometry and code.
The complete list for any module is its `## 6. Changes applied` table.


### Module 03 — Joints as Constrained Mechanical Interfaces

**Scale.** 21 blocking defects, 18 style edits, 68 anchored replacements. Report `editor-reports/module03.md` (694 lines).
**Verdict.** "Yes, after revision." — a graduate reader with no biomechanics can learn from these pages why a Lagrange multiplier *is* a joint reaction force, and "What stops the reader is elsewhere, and it is concentrated in the numbers rather than the arguments."
**The one that mattered.** §9.4 opened with the promise "every number quoted below was produced by running the code," and it was false as shipped: the §7.4 lab computes $R_s$, $R_e$ and $\lambda_3$ inside its loop and then discards them without a single `print`, and five of the ten K snippets call names (`solve_kkt`, `release_pose`, `Rs_history`, `time_of_first_turning_point`) that are defined nowhere in the module. K2's own numbers matched no run of the model — its wall shoulder reaction ran 20.6→26.3 N where the code gives 57.9→187.3 N, understating by a factor of five the very effect the problem exists to demonstrate. A reader who copied the code out could not reproduce one number in the section.

**NUMBER — B8 (K9's Baumgarte drift factor).**
*Before:* `With stabilization the drift stays at $\approx1\ \mu\mathrm m$ ($10^{-6}\ \mathrm m$) for the whole swing; without it the error is about $15\times$ larger here ($1.5\times10^{-5}\ \mathrm m$) and grows over longer runs.`
*After:* `With stabilization the drift stays at $\approx1\ \mu\mathrm m$ ($1.03\times10^{-6}\ \mathrm m$) for the whole swing and is still falling at the end of the run; without it the error reaches $2.2\times10^{-5}\ \mathrm m$, a factor of $21$ larger, and unlike the stabilized error it never comes back — it is at its maximum on the last step`
*Why:* Running the module's own code with $\gamma_d=\gamma_p=40$ and then $0$ over the same 40 000 steps gives 1.03e-06 m against 2.156e-05 m — ratio 21.00, not 15.

**SVG — B13d (the hip marker floats off its own curve).**
*Before:* ``<circle cx="352.5" cy="149.1" r="4" fill="#7a1f1f"/>``
*After:* ``<circle cx="352.5" cy="145.3" r="4" fill="#7a1f1f"/>``
*Why:* Decoding the figure against its own ticks ($S=(250-y)/73.333$), $x=352.5$ is $\beta=55^\circ$ where $S=\tan55^\circ=1.4281$ ⇒ $y=145.3$; at $149.1$ the dot read $S=1.376$, i.e. it had been placed on the neighbouring polyline vertex, 4 px off the curve it marks.

**FIGURE — B13a (§6.2's mobility curve plotted from no equation).**
*Before:* the blue dashed polyline ran linearly from $y=30$ at $\beta=10^\circ$ to $y=195$ at $\beta=70^\circ$; against the figure's own right-hand ticks ($y=250-220m$) that is a normalized mobility of $1.00\to0.25$, i.e. $(90^\circ-\beta)/80^\circ$ — a formula the module never states. Caption said only `mobility (blue dashed, a normalized range-of-motion proxy) falls.`
*After:* sixteen points recomputed as $x=60+26k$, $y=30+220k/35$ ($1.00\to0.571$), with the caption now naming the function: `The mobility curve is the geometric range of motion: the head swings until the bony neck, of assumed half-angle $\theta_n=30^\circ$, strikes the rim, so $\text{ROM}(\beta)=180^\circ-\beta-\theta_n$, normalized here by its value at $\beta=10^\circ$.`
*Why:* A curve labelled "(computed)" must say what was computed; the shipped curve was a straight line matching no stated law, and the section's whole point is that the two curves have different *shapes*.

**PROSE — B16 (C1(b) names a force that is exactly zero).**
*Before:* `This is precisely why the passive limb in <a class="secref" href="#lab">§7</a> moved at all — gravity's along-rail component drove the swing.`
*After:* `This is precisely why the passive limb of <a class="secref" href="#lab">§7</a> moved at all, though not because gravity pulls along the rail: the rail is horizontal, so gravity has <em>no</em> along-rail component. The driver is the <em>other</em> mass. … at release $\lambda_3=17.6\ \mathrm N$ against a hand weight of $m_2g=14.7\ \mathrm N$, the difference being the vertical part of the same push from bone 2.`
*Why:* Two sentences earlier the same solution states the rail constraint as $g_3=y_2-y_h$ — horizontal — so the explanation contradicted its own premise.

**NOTATION — B11a (Baumgarte gains collide with two other symbols).**
*Before:* `replacing the right-hand side $-\dot J_c\dot q$ with $-\dot J_c\dot q-2\alpha\,J_c\dot q-\beta^2 g$ — which gently pulls any drift back to zero (we use $\alpha=\beta=40$).`
*After:* `$-\dot J_c\dot q-2\gamma_d\,J_c\dot q-\gamma_p^2 g$, a damping term and a restoring term acting on the constraint residual, which gently pulls any drift back to zero (we use $\gamma_d=\gamma_p=40$, the critically damped choice`
*Why:* $\alpha$ was already §4.2's abductor tilt and $\beta$ already §6's socket rim angle — three symbols in the module carried two meanings each, and the Appendix flagged one and missed two.

**CODE — B4 (a live hyperlink inside a `<pre><code>` block).**
*Before:* `# the only change from <a class="secref" href="#lab-code">§7.4</a>`
*After:* `# the only change from the lab script of section 7.4`
*Why:* The tag was unescaped, so the browser rendered a link inside the Python source and the copy button — which reads `code.textContent` — handed the reader a different line than the one displayed.

**MATH — B21 (the held mass had weight but no inertia).**
*Before:* `the held weight is vertical, parallel to the rail's reaction direction, so the contact absorbs precisely $m_L g$ and the joints never feel it. The motion itself is also unchanged — the trajectory does not depend on $m_L$, only the contact force does.`
*After:* `The addition can therefore be written $J_c^{\mathsf T}\delta$ with $\delta=(0,0,-m_Lg)$, and substituting it into (7.6) leaves the acceleration block untouched and moves only the multiplier, $\lambda_3\to\lambda_3+m_Lg$. … Give the load its inertia as well — <code>M = np.diag([m1, m1, m2 + mL, m2 + mL])</code> — and the invariance goes. Over the same $m_L=0,\ 5,\ 10\ \mathrm{kg}$ sweep the peak shoulder reaction then runs $32.6\to57.5\to79.7\ \mathrm N$`
*Why:* `mL` entered the applied force $Q$ but never the mass matrix $M$, so the memorable "joints never feel it" was a property of an inertia-free load, not of a limb carrying a bag — a factor of 2.4 at 10 kg; the exact case is now proved *and* priced.


### Module 04 — Cartilage, Synovial Fluid, and Joint Contact Biophysics

**Scale.** 17 blocking defects, 13 style edits, 107 applied edits. Report `editor-reports/module04.md` (1213 lines).
**Verdict.** "Yes, after revision." — the spine is sound and in places exemplary (all twelve code blocks run clean, the Hertz box carries a full Boussinesq-matching derivation), but "the module's central mathematical object is missing: section 4 averages 'the Terzaghi series' that section 3 named but never wrote."
**The one that mattered.** K9 asked the reader to model incomplete recovery — "degraded tissue recovers only a fraction $r\lt1$" — and then handed back a solution in which $r$ never appears, built on an envelope $F_n=F_\infty+(F_0-F_\infty)e^{-n/N_c}$ whose constants $F_\infty\approx0.15$ and $N_c\approx22$ are derived from nothing, listed in no parameter table, and labelled no assumption. $F_0=0.97$ matches no computed value in the module (§4 gives 0.9862 at 1 s, K5 gives 0.9902, K1 gives 0.979). It is the one place in the module where a number in a solution was manufactured rather than computed — and the honest replacement, the recurrence $d_{n+1}=(1-r)(d_n+\Delta F)$ with fixed point $F^*=1-\Delta F/r$, turns out to teach the better lesson: incomplete recovery alone gives a *bounded* offset, so runaway needs $r$ itself to fall with damage.

**MATH — B7 (D2's small-charge limit is off by exactly two).**
*Before:* `$\pi\approx R_gT\,c_F^2/(2c_0)$ grows quadratically for $c_F\ll c_0$ — the rising curve of K2.`
*After:* `for $c_F\ll c_0$ expanding the root gives $\pi=2R_g\Theta c_0\big[\sqrt{1+c_F^2/(4c_0^2)}-1\big]\approx R_g\Theta\,c_F^2/(4c_0)$ — quadratic in the fixed charge, matching <a class="secref" href="#donnan">§2</a>. (At $c_F=0.01\ \mathrm M$, $c_0=0.15\ \mathrm M$ the exact formula gives $429.4\ \mathrm{Pa}$ and this limit $429.6\ \mathrm{Pa}$.)`
*Why:* §2 at line 384 already had the correct $4c_0$; D2 contradicted it — at $c_F=0.01$ M, $c_0=0.15$ M the exact formula gives 429.44 Pa, the $4c_0$ form 429.56 Pa, and D2's $2c_0$ form 859.11 Pa.

**SVG — B16 (a figure whose two curves do not carry the same load).**
*Before:* the blue "biphasic" polyline, decoded against the figure's own tick coordinates (x: 95.5→−20 mm … 379.5→20 mm; y: 228→0 MPa … 43→3 MPa), was a parabola with $a'=21.18\ \mathrm{mm}$, $p_{\max}=2.001\ \mathrm{MPa}$, carrying $\tfrac12\pi a'^2p_{\max}=1410\ \mathrm N$ — while its caption read `carry the identical knee load $\int p\,\mathrm dA=R=1715\ \mathrm N$` and the figure's own inset label said `same load ∫p·2πr dr`.
*After:* redrawn at §6's own numbers, $a'=23.30\ \mathrm{mm}$ and $p_{\max}=2.011\ \mathrm{MPa}$ ($\tfrac12\pi a'^2p_{\max}=1715.0\ \mathrm N$), with the caption stating both: `The peaked dry-Hertz dome ($p_0=2.54\ \mathrm{MPa}$ over $a=18.0\ \mathrm{mm}$) and the broader biphasic parabola ($p_{\max}=2.01\ \mathrm{MPa}$ over $a'=1.3a=23.3\ \mathrm{mm}$, the profile <a class="secref" href="#contact">§6</a> derives) carry the identical knee load $\int p\,\mathrm dA=R=1715\ \mathrm N$`
*Why:* Both polyline fits had rms residual 0.0003, so this was the drawn shape and not a reading error: the picture showed the biphasic profile carrying 18 % *less* load than the dry one — the exact opposite of the point the problem makes — and it appeared on the page twice (at C5 and at K3).

**FIGURE — B17 (K4's plot draws its x-axis somewhere other than zero).**
*Before:* the stress-relaxation curve is exactly $\sigma/\sigma_\infty=1+F(T)$ (peak 2.000), but it was anchored on an implied zero at $y=187.4$ while the x-axis was drawn at $y=232$, and the figure carried no y tick anywhere — so a reader measuring off the drawn axis gets a peak $1.578\times$ the plateau.
*After:* curve and $\sigma_\infty$ line rescaled about the drawn axis so the axis *is* $\sigma=0$ — $\sigma_\infty$ from $y=126.2$ to $y=144.0$, the peak from $y=65.0$ to $y=56.0$ — re-decoded to measure $2.000\times$ the plateau off the page.
*Why:* K4's own solution two lines above says "$\sigma$ starts at $2H_A\varepsilon_0$" and its own code prints `sigma_peak=0.119 MPa` / `sigma_end=0.0600 MPa`; the picture disagreed with both.

**CODE — B15 (K7's block only parses on Python 3.12).**
*Before:* a `print(` whose f-string carried the replacement fields split across eleven physical lines — `f"eps_inf={` newline `eps_inf:.2f}  T90={` newline `T90:.3f} …`
*After:* one named intermediate plus an implicitly concatenated f-string, printing the identical `eps_inf=0.50  T90=0.848  t90=5654 s = 1.57 h`
*Why:* A multi-line expression inside an f-string replacement field is PEP 701 syntax, accepted only from 3.12; the page gives the block a copy button, so a reader on 3.11 gets a `SyntaxError` on paste — and `check_code` passed it, because pycodestyle checks layout, not language version.

**NOTATION — B5 (three symbols, eight meanings).**
*Before:* `$F$ the Faraday constant` (line 315), `$p_0=\frac{3F}{2\pi a^2}$` and `Same load $F=1715\ \mathrm N$` (§6), and `F(t)` the fluid load support fraction (§§4, 7, 8 and eleven problems) — with the Appendix recording only the third. Likewise `$R_g,\ T$ gas constant and absolute temperature` sat eight rows from `$T$ dimensionless time, $T=Dt/h^2$` in the same table, and `$W$` was body weight in §0 and load in `$S=\frac{\eta\,U}{W}$` at line 963, with no Appendix row at all.
*After:* the signature symbols keep their letters and the intruders move — dimensionless time keeps $T$ (it is in every code block) and temperature becomes $\Theta$; fluid support keeps $F$ and the contact load and Faraday constant move. In code, `RgT` became `RgTheta` in the K2 and K10 blocks (S13, found by grepping the superseded value after the apply).
*Why:* §2 already shows the module knows how to do this — it writes $R_g$ "to keep it distinct from the joint reaction $R$ of §0" — so this was inconsistency, not oversight; and the standard is explicit that flagging a collision is not resolving it.

**NUMBER — S2 (§7's friction product prints a different answer from the one shown).**
*Before:* `When the fluid is pressurized ($F\approx0.99$ during a footstep), $\mu_{\rm eff}\approx0.15\times0.01\approx0.002$ — the measured value — and it needs <em>no sliding speed at all</em>.`
*After:* `During a $1\ \mathrm s$ footstep $F=0.986$, so $\mu_{\rm eff}=0.15\times0.014=0.0021$ — the measured value — and it needs <em>no sliding speed at all</em>.`
*Why:* The shown product $0.15\times0.01$ is $0.0015$, not $0.002$; the printed answer was right and the factor wrong, because $1-F$ at a 1 s footstep is $0.014$, not $0.01$.


### Module 05 — Muscles as Chemo-Electro-Mechanical Actuators

**Scale.** 22 blocking defects, 11 style edits, 72 anchored replacements. Report `editor-reports/module05.md` (655 lines).
**Verdict.** "Yes, after revision." — the spine is sound and in places exemplary (decoding every polyline confirmed all eleven curves agree with the models the prose states), but "the module computes with models it never writes down": a reader cannot reproduce a single §3, §4, §7 or §9 number from the page.
**The one that mattered.** Two decorative `<figure>` banners sat before the first `<h2>` — a triceps-surae graphic and a pennation graphic, neither referenced from the prose. The stylesheet numbers every `<figure>` with a CSS counter, so the first *referenced* figure rendered as "Fig. 3" while the prose called it Fig. 1, and the offset carried through all 33 references. Every single figure citation in the module pointed the reader two figures earlier than the one being discussed — a defect invisible to every automated gate and to anyone reading the source rather than the rendered page.

**FIGURE — B3 (Fig. 30 answers a different problem from the one the module set).**
*Before:* the optimisation figure's blue constraint line ran $(0,235)$ to $(147,0)$ and its innermost gold cost ellipse had decoded semi-axes 70.7 N and 141.4 N — a maximal-force ratio of exactly 1:2 — giving the tangency $(57.4, 143.6)$ that the caption quotes: `Here that puts more force on the stronger brachialis ($F_{br}\approx144$&nbsp;N) than the biceps ($F_{bi}\approx57$&nbsp;N)`
*After:* regenerated from §1's own numbers, $F_{bi,\max}=135\ \mathrm N$ and $F_{br,\max}=210\ \mathrm N$: `Solving $F_i\propto d_iF_{i,\max}^2$ against the constraint gives $F_{bi}=76$&nbsp;N and $F_{br}=114$&nbsp;N, leaving both at nearly the same relative stress ($0.56$ and $0.54$).`
*Why:* §1 computes a maximal-force ratio of 1:1.56, not 1:2, so the drawn ellipses belonged to a different muscle pair; the corrected figure also earned a new sentence the original never drew — 76+114 = 190 N against the 147 N a single muscle would need, because minimising stress is not minimising force.

**NUMBER — B4 (K10's fitted time constant is not what its own fit returns).**
*Before:* `recovers $\boxed{\tau_a\approx41.5\ \mathrm{ms}}$ (giving $t_{\text{pk}}=25.2$, $t_{\text{half}}=40.0\ \mathrm{ms}$)` — with the figure's label and `aria-label` repeating "41.5 ms"
*After:* `which prints <code>fitted tau_a = 43.7 ms</code> … So $\boxed{\tau_a\approx43.7\ \mathrm{ms}}$, against the $41.0\ \mathrm{ms}$ Modelling assumption 3.2 assumed — a $6.6\%$ discrepancy, and it is not numerical error … what you recover is the parameter <em>conditioned on everything you froze</em>, and reporting it without that condition overstates what the twitch measured.`
*Why:* Minimising $(t_{\text{pk}}-25)^2+(t_{\text{half}}-40)^2$ over $\tau_a$ returns 43.71 ms, and 43.71 ms is what produces the quoted features; 41.5 ms produces neither — a factual error inside the one problem whose subject is parameter estimation.

**PROSE — B5 (K6 gives the wrong reason for the strength peak).**
*Before:* `The joint is therefore strongest where <em>neither</em> factor alone is maximal`
*After:* `on $[70^\circ,82.3^\circ]$ the product is $1\times d_m(\theta)$, still rising, and beyond $82.3^\circ$ the falling $f_L$ beats the flattening $d_m$: the strength peaks at $\boxed{82.3^\circ}$ … The lesson is not that neither factor is maximal there — $f_L$ <em>is</em> at its maximum across the whole plateau — but that a flat factor hands the choice of optimum entirely to the other one.`
*Why:* With $\ell(\theta)/\ell_0=1-0.003(\theta^\circ-70)$ the fibre sits on the length-tension plateau ($0.963\le\ell/\ell_0\le1$) across the whole interval, so $f_L$ *is* maximal at the peak — the solution taught the wrong lesson from the right answer.

**MATH — B12 (§8's lever ratio, and a load arm colliding with §0).**
*Before:* `the muscle's moment arm is roughly a tenth of the load's, so it pays roughly tenfold in force.` (load arm written $r_m$, colliding with §0's $r_L$)
*After:* ratio corrected to a seventh, arm renamed $r_L$, plus a reconciliation paragraph: `<a class="secref" href="#origin">&#167;0</a> took the elbow flexor moment arm as $d_m\approx3\ \mathrm{cm}$ … here it is $4\ \mathrm{cm}$. Both are right, at different angles: Module&nbsp;1's $3\ \mathrm{cm}$ is a single value chosen to stand for the whole flexion range, while $4\ \mathrm{cm}$ is the peak of the angle-dependent curve … reached near $90^\circ$.`
*Why:* With $d_m=4$ cm and $r=30$ cm the ratio is a seventh, and the two forces quoted in the same sentence — 147 N against 19.6 N — are themselves a factor 7.5.

**CODE — B7 (live HTML inside Lab 1's `<pre><code>`).**
*Before:* `# activation ODE constants (s), <a class="secref" href="#activation">§5</a>` (and four more at `module05.html:1158, 1168, 1172, 1180`)
*After:* `# activation ODE constants (s), sec. 5` (and `sec. 2`, `sec. 6`, `sec. 8`, `sec. 5`)
*Why:* Five `<a>` tags sat unescaped inside the code block, so the copy button handed the reader text that is not Python.

**NUMBER — B6 (Lab 1's quoted output is not what Lab 1 prints).**
*Before:* `<code>peak torque 13.3 N m at t = 0.76 s</code>`
*After:* `<code>peak torque 13.4 N m at t = 0.76 s</code>`
*Why:* The block gives 13.3504 N m, which its own `f"{...:.1f}"` renders as 13.4; decoding the Fig. 34 lower panel independently gives 13.34 N m at 0.752 s — so the figure agreed with the code and only the prose did not.


### Module 06 — Tendons, Ligaments, Fascia, and Elastic Energy Storage

**Scale.** 17 blocking defects, 15 style edits, 52 anchored replacements. Report `editor-reports/module06.md` (918 lines).
**Verdict.** "Yes, after revision." — "Every proposition carries a real proof, and every proof I followed with a pen checks out … The damage is in the numbers, and it is of one kind." The module told the reader twice that its computational answers were "Python-verified" and then shipped no code with any of the thirty problems.
**The one that mattered.** §6 and §7 say a tendon's relaxation time is "seconds to minutes" — that is what puts gait on the low-loss side of the loss peak, and it is the module's headline explanation of why a tendon makes a good spring. But the Appendix and every lab and K problem use $\tau_\sigma=0.05$ s, which puts the loss peak at 2.25 Hz, i.e. running cadence, as K7 itself computes. The module's own parameters put gait *on* the peak while its prose says gait sits far past it, and Fig. 16 shades the gait band as $\omega\tau_\sigma\gg1$ using the very $\tau_\sigma$ that makes it false. A reader checking the central claim against the module's own numbers would find it inverted.

**MATH — B2 (the relaxation time that contradicts the headline claim).**
*Before:* `A tendon's relaxation time $\tau_\sigma$ is of order seconds to minutes, while walking and running load it at a few hertz. The product $\omega\tau_\sigma$ is therefore <em>large</em>`
*After:* `Real tendon has a spectrum, not one time constant: the Appendix records a span from $10^{-2}$ to $10^{3}\ \text{s}$. The fast end, $\tau_\sigma\approx0.05\ \text{s}$, is the mode the labs of <a class="secref" href="#labs">§9</a> use … taken alone it would put $\omega^\ast\approx14\ \text{rad/s}$, or $2.25\ \text{Hz}$ (K7), squarely at running cadence. … A tendon is a low-loss spring in the regime it works in because its dominant loss peak is parked decades below the operating frequency, not because it has no loss peak.`
*Why:* At a 2.6 Hz cadence, $\omega\tau_\sigma=16.34\times0.05=0.82$ — not large; the two statements could not both stand, and the one the figure was drawn with was the one the prose denied.

**NUMBER — B3 (a "tendon" that stretches 61 %).**
*Before:* `kT = 1.7e4  # leg (series-tendon) stiffness (N/m)` with the prose `the tendon stores $\approx197\ \text{J}$ over the bounce`
*After:* `# an elastic leg spring. Assumed values; kT is a WHOLE-LEG series` / `# stiffness, not the 4.2e5 N/m free Achilles of section 2.` and `kT = 1.7e4  # leg (series) spring stiffness (N/m)`, with the prose stating `A hop compresses the leg by about $16\ \text{cm}$, and no single tendon stretches that far; the lumped leg spring rolls the Achilles together with the arch, the knee and hip tissues`
*Why:* §2 computes the free Achilles at $4.16\times10^{5}$ N/m — 24 times stiffer — and instrumenting the block gives a peak ground reaction of 2591 N, so the labelled "tendon" stretched 152.4 mm, which on §2's own 250 mm Achilles is 61 % strain against a 9 % rupture strain; the stiffness was right for a whole-leg SLIP spring and only the *label* was wrong.

**PROSE — B5 ("near-isometric" contradicted by the simulation meant to prove it).**
*Before:* `$\sim97\%$ of the push-off is elastic recoil, the muscle merely holding force`
*After:* `Be exact about <em>near-isometric</em>, because the simulation is: the fibre is not still. It shortens $18\ \text{mm}$ over the stance, a third of its optimal length $\ell_0$, and its length factor $f_L$ falls from $1.00$ to $0.58$ on the way. What is near zero is its <em>velocity at push-off</em>, $0.30$ of the spring's recoil speed.`
*Why:* Isometric means constant length, and the Lab 2 fibre shortens 55.0 mm → 36.6 mm (33.5 % of $\ell_0$); the true statement — a velocity ratio, not a length one — strengthens the catapult argument rather than weakening it.

**FIGURE-LABEL — B16 (Fig. 9's "about 6×" contradicted by the module's own simulation).**
*Before:* `the tendon recoils about $6\times$ faster than the fibre. Derived from the constraint (4.1) and the tendon law, as ultrasound fascicle measurements confirm.`
*After:* `The split drawn here is <em>prescribed</em>, to show what Eq.&nbsp;(4.4) allows rather than to predict a value; the ratio computed from the coupled dynamics is $3.3\times$ (Lab&nbsp;2, <a class="secref" href="#labs">§9</a>). Ultrasound fascicle tracking reports the same qualitative pattern (unverified here: no source is checked in this repo).`
*Why:* No code in the module produces the 6, the module's own dynamic simulation of the same effect gets 3.3, and the caption attached an unverified ultrasound citation to a number the module had invented.

**MATH — B8 (a boxed law fed an angle where it wants a length).**
*Before:* `$+\,R\,F_{\text{lig}}\big(\theta-\theta_{\text{hi}}\big)$`
*After:* the corrected equation restated inside a Lemma with a proof, supplying the missing arc-length relation $x=R\,\Delta\theta$ — which is also exactly where the moment arm $R$ enters twice, once to convert the rotation to an elongation and once to convert the tension back to a torque.
*Why:* $F_{\text{lig}}$ is Eq. (2.1)'s structural law $F(x)=A_0\sigma(x/L_0)$, whose argument is an elongation in metres; handed $\theta-\theta_{\text{hi}}$ in radians the expression is dimensionally meaningless — and Lab 3 inherited it, making `k = 4.5e6` a quantity in N/rad² that no comment declared.

**NUMBER — B17 (§2's own range excludes §2's own answer).**
*Before:* `in the measured range for the free Achilles ($\sim150$–$400\ \text{N/mm}$…)` and `consistent with the $\sigma_f\approx100\ \text{MPa}$ of §1 ($\sigma_f A_0\approx7.8\ \text{kN}$)`
*After:* `just above the measured range for the free Achilles ($\sim150$&#8211;$400\ \text{N/mm}$ … ) which is what a model that ignores the aponeurosis in series should give. … whose model failure stress is $\sigma_f=97.5\ \text{MPa}$ and gives $\sigma_f A_0=7.8\ \text{kN}$ (the round $100\ \text{MPa}$ would give $8.0\ \text{kN}$).`
*Why:* The computed $k_{\text{lin}}=416$ N/mm is *above* the quoted 150–400 N/mm band, and $100\ \mathrm{MPa}\times80\ \mathrm{mm^2}=8.0$ kN, not 7.8 — the 7.8 comes from the model's own 97.5 MPa, which is the honest number to name.


### Module 07 — Standing, Posture, and Load Bearing

**Scale.** 19 blocking defects, 11 style edits, 86 anchored replacements. Report `editor-reports/module07.md` (657 lines).
**Verdict.** "Yes, after revision — and the revision is larger than it looks." — "The mathematical spine of this module is the best in the course so far. Ten propositions, every one proved, and the proofs are real … None of this touches the derivations. Fix the figures, fix the eight numbers, and this is a chapter that teaches."
**The one that mattered.** Ten problem figures drew their axes as 20–60 px black slabs. `stroke-width="49.2"` on an x-axis renders as a solid black rectangle across the lower left of the plot, swallowing the axis title, the tick labels and the first third of the curve; C5's dashed reference line at `stroke-width="57.6" stroke-dasharray="5 4"` rendered as a picket fence of red bars over the whole panel, and D2's two eigenlines at `stroke-width="50.0"` turned a saddle's stable and unstable manifolds into two crossed slabs. Every one of the nine hardening gates passed the file, because `getBBox()` ignores stroke width and `check_overlap` excludes solid lines by design. The reader would have seen ten ruined figures that no automated check could see.

**SVG — B1 (axes drawn as slabs).**
*Before:* ``<line x1="55" y1="155" x2="260" y2="155" stroke="#333" stroke-width="49.2"/>`` and ``<line x1="55" y1="155" x2="55"  y2="50"  stroke="#333" stroke-width="25.2"/>`` — 22 axis lines carrying `stroke-width` between 21.6 and 62.4
*After:* every `<line stroke="#333">` with `stroke-width` ≥ 10 thinned to `stroke-width="1.2"`; C5's dashed reference line to `1.6`; D2's eigenlines to `2.6`; and 31 vector shafts carrying `stroke-width` between 12 and 56.6 set to `3`
*Why:* The same generator bug that fattened the axes fattened every arrow shaft — a 20 px shaft behind a fixed 10–13 px `markerUnits="userSpaceOnUse"` head reads as "a brick with a notch, not an arrow"; the fix left 26 thick lines alone because there the thickness *is* the anatomy (limbs `#c98a5e`, feet `#5a86a8`, muscle bellies `#8a3d3d`).

**FIGURE-LABEL — B12 (the D1 figure states the equation of motion with the wrong sign).**
*Before:* ``I&#952;&#776; = Mg&#8467; sin&#952; + &#964;`` (rendered `Iθ̈ = Mgℓ sinθ + τ`)
*After:* ``I&#952;&#776; = Mg&#8467; sin&#952; &#8722; &#964;``
*Why:* Proposition 3.1 and the D1 solution directly beneath both give $I\ddot\theta = Mg\ell\sin\theta - \tau$, and the sign of $\tau$ is the entire point of the problem — the ankle torque restores, gravity topples.

**NUMBER — B3 (K5's "optimum" is not the optimum, and its decay rate is 2.3× too small).**
*Before:* `the optimum sits near $K_p\approx940$, $K_d\approx260\ \mathrm{N\,m\,s\,rad^{-1}}$, with a decay rate of ${\approx}\,1.5\ \mathrm{s^{-1}}$ (recovery time constant ${\approx}\,0.7$&nbsp;s)`
*After:* `the decay rate peaks at $K_p\approx785\ \mathrm{N\,m\,rad^{-1}}$ (that is $1.27\,Mg\ell$) and $K_d\approx256\ \mathrm{N\,m\,s\,rad^{-1}}$, giving $\sigma_{\max}\approx3.42\ \mathrm{s^{-1}}$ and a recovery time constant $1/\sigma\approx0.29$&nbsp;s, about twice the delay. The optimum is exactly where three real characteristic roots coalesce, the delayed analogue of critical damping: it solves $f(s)=f'(s)=f''(s)=0$`
*Why:* A Chebyshev discretisation of the delay differential equation gives a grid maximum $\sigma=3.4206$ at $K_p=785$, and the triple-root pair $(784.879,\,256.449)$ gives 3.4204; the stated $(940,260)$ gives 1.4583 — so the old answer was a real point on the island, but not the fastest one, and the recovery-time claim was off by a factor 2.3.

**NUMBER — B9 (K2's area ratio, repeated wrong inside the figure).**
*Before:* the solution's stated ratio and the `fig44` label `stable area ratio &#8776;4.6`
*After:* `Testing stability on a grid over $(K_p,K_d)$ and summing the stable cells gives $1.18\times10^6$ for $\Delta=0.12$&nbsp;s against $2.66\times10^5$ for $\Delta=0.18$&nbsp;s, a ratio of $4.44$.`, and the figure label `stable area ratio &#8776;4.44`
*Why:* Two independent computations agreed against the module — Green's theorem on the Hopf boundary of Proposition 6.2 gives 4.4458, and a $160\times160$ grid tested with the Chebyshev rightmost root gives 4.453 — and the wrong number was baked into the picture as well as the prose.

**CODE — B19 (the reader-facing lab code is formatter-damaged).**
*Before:*
```
print(
    f"critical delay : simulation {
        1e3 *
        Dcrit:5.1f} ms   theory {
            1e3 *
            Dtheory:5.1f} ms")
```
*After:* both lab blocks rewritten to readable, 79-column, Python-3.8-compatible form, printing byte-identical output
*Why:* A multi-line expression inside an f-string is PEP 701, i.e. 3.12 and later, so a reader on 3.11 gets a `SyntaxError` from a block the module tells them to copy and run; the same pass had mangled `acc = (Mgl*th[k] - Kp*thd - Kd*wd) / \` onto a backslash continuation and broken a Lab 2 generator expression across five lines — and both blocks were PEP8-clean, "which is exactly why nothing caught it."

**FIGURE — B2 (every numbered figure reference points at the wrong figure).**
*Before:* an uncited lumbar-spine `<figure>` sat at the top of §0, incrementing the stylesheet's CSS counter before the first figure the prose actually names
*After:* the lumbar-vertebrae figure moved out of §0 and into §8 as Fig. 17, where §8 gains a sentence citing it for the short erector lever; K9's `envelope of <b>Fig. 20</b>` renumbered to `Fig. 21`
*Why:* One uncited figure shifted the counter by one, so every numbered reference in the module landed on its neighbour — the same class of defect as Module 5's two-figure offset, from the same cause.


### Module 08 — Walking Biomechanics

**Scale.** 22 blocking defects (B1–B23; 17 in the first pass, 6 more from a figure decode, B21 checked and cleared), 15 style edits, 65 anchored replacements. Report `editor-reports/module08.md` (1490 lines).
**Verdict.** "Yes, after revision — and the revision is substantial": the argument structure is sound and nothing in it is faked, but "a graduate reader would follow the derivations and then be unable to reproduce a single computed number in the module."
**The one that mattered.** All four labs ran, and not one number any of them printed appeared anywhere in the module — the section opened by claiming each lab "varies a parameter and asks what mechanism changes" and then showed four bare code blocks with no result and no interpretation. Worse, Lab 3 was titled "inverse-dynamics estimate" and did no inverse dynamics at all: it asserted a Gaussian ankle torque and multiplied it by an asserted Gaussian angular velocity. A reader copying that block would learn the shape of two curves someone typed in, not how a joint moment is recovered from ground reaction and geometry.

**MATH — B9c+S7 (Prop 9.1's worked example).**
*Before:* `For $\ell=0.9$&nbsp;m, a step half-angle $\alpha\approx0.3$&nbsp;rad and a gentle slope $\gamma\approx0.05$&nbsp;rad ($3^\circ$), this gives $v\approx1.2\ \mathrm{m\,s^{-1}}$ — a realistic walking speed from gravity alone.`
*After:* `For the module's reference $\ell=0.95$&nbsp;m, a step half-angle $\alpha=0.30$&nbsp;rad and a gentle slope $\gamma=0.05$&nbsp;rad ($2.87^\circ$), this gives $v=1.25\ \mathrm{m\,s^{-1}}$, a realistic walking speed from gravity alone. The two small-angle substitutions just made are doing real work at $2\alpha=34.4^\circ$: K9 solves the same energy balance without them and gets $1.31\ \mathrm{m\,s^{-1}}$, $5.5\,\%$ higher.`
*Why:* The leg length silently switched to `0.9` m from the module's own reference `0.95` m, and `0.05` rad was labelled `3°` when it is `2.8648°`.

**NUMBER — B3a/B3b (Prop 5.2).**
*Before:* `Splitting a velocity redirection of total angle $\beta$ into $n$ equal sequential impulses reduces the collision loss from $\tfrac12 Mv^2\beta^2$ to $\tfrac12 Mv^2\beta^2/n$. … it powers the same transition with one-quarter of the work required if the collision is left to dissipate`
*After:* `$$\boxed{\;E_{\rm step}\;=\;\tfrac12 Mv^2\sin^2\!\frac{\beta}{n}\;\approx\;\frac{1}{n^{2}}\cdot\tfrac12 Mv^2\beta^2\;}$$ … $$\frac{\tan^2\alpha}{\sin^2 2\alpha}=\frac{1}{4\cos^{4}\alpha}.$$ That tends to $\tfrac14$ as $\alpha\to0$, which is the classic one-quarter, but it equals $0.330$ at this module's reference half-angle $\alpha=21.1^\circ$.`
*Why:* The proposition proved a `1/n` law and then concluded with the textbook one-quarter, which needs `1/n²`; the true reference-gait saving is `26.7` J → `8.8` J, a factor `3.03×`, not `4×`.

**PROSE — B12a (`module08.html:199`).**
*Before:* `In single support, the stance leg is often well a\approximated as a nearly rigid link of length $\ell$ from the contact point to the COM.`
*After:* `In single support, the stance leg is well approximated as a rigid link of length $\ell$ from the contact point to the COM, an idealisation <a class="secref" href="#problems">section 12</a> returns to.`
*Why:* A literal `a\approximated` rendered as backslash garbage on the page, and the double hedge "often well … nearly" was replaced by a forward pointer to where the idealisation is actually questioned.

**NOTATION — B12b+B17b/B17c (`module08.html:473,477`).**
*Before:* `About the whole-body COM, the angular momentum satisfies $$\dot{\mathbf L}_G=\sum \mathbf M_G^{\rm ext}.$$ If external moments about the COM are small over part of the stride, arm and leg angular momenta must a\approximately cancel within the body.`
*After:* `About the whole-body COM, the angular momentum satisfies $$\dot{\mathbf H}_G=\sum \mathbf M_G^{\rm ext}.$$ If external moments about the COM are small over part of the stride, arm and leg angular momenta must approximately cancel within the body.`
*Why:* `L` is step length everywhere else in the module, so `L_G` was a live symbol collision; renamed to `H_G` throughout Prop 8.1 and its proof.

**SVG — B19a/B19b (the joint-power figure, `module08.html:432`).**
*Before:* A decorative "walker" drawn as `<line x1="656" y1="250" x2="748" y2="250" stroke="#c9b79a" stroke-width="23.9"/>` — a 92 px × 23.9 px beige slab — with two lentil feet `<ellipse cx="701" cy="237" rx="6" ry="2"/>`, `<ellipse cx="711" cy="236" rx="6" ry="2"/>` and a head `<circle cx="702" cy="119" r="14.3"/>` floating about 118 px above them. Figure `viewBox="0 0 760 300"`.
*After:* All four elements deleted; `viewBox="0 0 645 300"`.
*Why:* The pieces read as a beige slab with a detached head, not a walker; `check_bodyprop` could not see it because the parts were separate elements, so it took a human render to catch.

**CODE — B1e+S2 (Lab 3, `module08.html:629-633`).**
*Before:* `ankle = 70*np.exp(-((t-0.55)/0.09)**2) - 15*np.exp(-((t-0.12)/0.08)**2)` / `omega_a = 2.0*np.exp(-((t-0.58)/0.10)**2)` / `work_ankle = np.trapz(np.maximum(power, 0), t)`
*After:* `Fy = shape*(W*T/2)/np.trapezoid(shape, t)   # scale set by impulse-momentum` / `x_cop = -0.06 + 0.25*s                      # heel-to-toe COP, ankle at x=0` / `tau = Fy*x_cop                              # quasi-static ankle moment`
*Why:* The ankle moment is now derived — the ground-reaction scale is fixed by `∫F_y dt = WT/2` and multiplied by the section's own COP travel — instead of asserted, and `np.trapz` (deprecated; warns on every reader's run) became `np.trapezoid`.


### Module 09 — Running and Jumping

**Scale.** 16 blocking defects (B1–B16; B14–B16 came from the figure-decode pass), 18 style edits, 80 anchored replacements. Report `editor-reports/module09.md` (966 lines).
**Verdict.** "Yes, after revision." The derivational spine is sound — fifteen propositions each carry a proof of matching weight and re-deriving every one by hand found no mathematical error — but "what stops the reader is the problem set and the numbers around it."
**The one that mattered.** K1 told the reader to find the leg stiffness that maximises flight time "and explain why an interior optimum exists"; its figure drew a hump labelled `optimum kleg ≈ 18 kN/m`, and its solution supplied a mechanism for the hump. None of it was real. Integrating the module's own SLIP equation with RK4 from the touchdown state K1 itself specifies, flight time rises strictly monotonically across the whole admissible band — `25.4 → 93.2 → 171.9 → 234.5 → 319.9 ms` as `k_leg` runs `12 → 40 kN/m`, increasing at all 59 grid points. The reader was being asked to explain a feature the model does not have, and the offered explanation inverted the physics: at a fixed touchdown state the energy is fixed, so a stiffer leg does not store less, it returns more of the same energy vertically and pays in forward speed (`v_x` falls `4.20 → 3.60 m/s`).

**MATH — B1 (K1 statement and solution, `module09.html:497-499`).**
*Before:* `Find the stiffness that maximises flight time, and explain why an interior optimum exists rather than &quot;stiffer is always better.&quot;` … `Flight time peaks at an intermediate stiffness: too soft a leg over-compresses and spends the stance redirecting rather than rebounding, while too stiff a leg barely compresses and stores little elastic energy to launch with.`
*After:* `Report the flight time and the peak vertical GRF together, and decide from the sweep whether flight time has an interior optimum or whether the useful stiffness is set by a constraint instead. Then find, by root-finding, the softest leg that still produces flight and the stiffest one that keeps the peak below $3$ body weights.` … `The useful stiffness is set by a constraint, not by an optimum, and the sweep is the only way to see that.`
*Why:* The real bounds are constraints found by root-finding — `k_leg = 11.09 kN/m` below which there is no flight at all, and `k_leg = 19.3 kN/m` where the peak vertical GRF reaches 3 body weights (`t_f = 163 ms`).

**NUMBER — B2 (`module09.html:217,219`).**
*Before:* `The CMJ reliably wins - by a few centimetres, here $34$ against $30\ \mathrm{cm}$ (Fig. 7, right).` and the caption `~34 cm against ~30 cm. Heights are computed from each curve's impulse`
*After:* `The CMJ reliably wins, and the same computation that produced Fig. 7 says by how much: $32.0$ against $30.0\ \mathrm{cm}$, a gain of $2.0\ \mathrm{cm}$ from a net impulse that is only $3.3\%$ larger ($175.5$ against $169.9\ \mathrm{N\,s}$).`
*Why:* Lab 2 — the module's own stated source for the number — prints `countermovement (front) h = 32 cm`, and no member of its `profile(front)` family reaches 34 cm (the family maxes at 32.4 cm).

**SVG — B15 (K6's figure, `module09.html:518`).**
*Before:* K6's polyline was byte-identical to K3's descending sensitivity line at `:506` — both the same 549-character point string running `48.0,44.0 52.5,46.2 … 257.5,147.8 262.0,150.0`, i.e. a straight descent. It drew the required stopping distance *falling* with drop height, and carried no tick labels at all, so nothing on the plot could contradict it.
*After:* The computed line `d_s = h_drop/5` from `(48,150)` to `(262,65.2)`, tick labels on both axes (`0, 0.5, 1.0 m`; `0, 10, 20 cm`), and the five tabulated points `4, 8, 12, 16, 20 cm` marked.
*Why:* K6's own solution derives `d_s >= m g h_drop/(F_tol - mg) = h_drop/5`, which rises — the figure drew the opposite of the answer printed beneath it.

**SVG — B14 (Fig. 7's countermovement curve, `module09.html:217`).**
*Before:* The CMJ curve matched no `profile(front)` from Lab 2 (nearest is `front = 0.8`, off by `0.12` BW — seven times the squat-jump curve's residual) and integrated to `181.0 N s` and `34.06 cm`, while every label around it had already been corrected to `32.0`.
*After:* The curve redrawn as Lab 2's own `profile(0.8)` on the same 80-point grid, integrating to `175.5 N s` and `32.04 cm`.
*Why:* The caption asserted "Both heights are computed from each curve's net impulse by Lab 2", which was false for one of the two curves — the number was fixed and the drawing was not.

**NOTATION — B4 (`module09.html:267,440,442,517,519`).**
*Before:* `by the work-energy form of (5.1), the peak force is F&#8776;&#189;m vland&#178;/d+mg` and, in C8, `the peak force is $\bar F\approx\tfrac12 m v_{\rm land}^2/d + mg$`
*After:* `by the work-energy form of (5.1), the average force over the stop is F&#772;=&#189;m vland&#178;/d&#8347;+mg … The brief spike at first contact is higher still, and is the subject of section 9.`
*Why:* Proposition 8.1 derives an *average* and says so twice; four places called it the peak, contradicting the one distinction §9 is built on — and C8's `$\bar F$` already carried the overbar while its prose said "peak."


### Module 10 — Balance, Stability, and Sensorimotor Control

**Scale.** 16 blocking defects, 8 style edits (6 applied as their own tags, 2 folded into blocking fixes), 62 anchored replacements. Report `editor-reports/module10.md` (683 lines).
**Verdict.** "Yes, after revision. The mathematical spine is the best in the course so far" — every proposition carries a correct proof — but "what blocks it is a set of defects that every gate is blind to, and one of them is a contradiction between two boxed results of the module's own."
**The one that mattered.** Proposition 1.2 boxes `J_max = m·ω₀·b = 21.7 N s` as the largest push a person can arrest without stepping, and Proposition 7.1 proves the ankle's authority is bounded by the length of the foot. Lab A then simulated an *unbounded* ankle, reported arresting `32.4 N s`, and K1 told the reader that number was the boxed budget "eroded by the whole delayed transient." It is not eroded — it is 49 % larger, because the simulated controller drives the centre of pressure outside the foot, which the module's own Proposition 7.1 forbids. A reader would have taken the lab as confirming the theory it silently contradicts.

**CODE — B1 (Lab A, `module10.html:360-375`).**
*Before:* `om[i+1] = om[i] + dt*(w0*w0*th[i] - kp*thd - kd*omd)`
*After:* `u_max = w0*w0*theta_edge  # bounded ankle authority, Prop. 7.1 (rad/s^2)` … `u = np.clip(-(kp*thd + kd*omd), -u_max, u_max)`
*Why:* Saturating the command at `|u| ≤ ω₀²(b/ℓ) = 0.961 rad/s²` makes the bisection return `21.6 N s` as `τ → 0` against the boxed `21.7`, falling monotonically to `18.5, 15.5, 0.8 N s` at `50, 100, 150 ms` — the lab now confirms the theory instead of contradicting it.

**MATH — B5 (Proposition 7.1's proof, `module10.html:277`).**
*Before:* `$\ddot x_{\rm com}=\tfrac{g}{\ell}(x_{\rm cop}-x_{\rm com})$ in the linearised pendulum (dividing the restoring moment $mg(x_{\rm cop}-x_{\rm com})$ by the moment of inertia $m\ell^2$ and multiplying by the lever $\ell$ to get a linear acceleration)`
*After:* `$$\ddot x_{\rm com}=\frac{g}{\ell}\big(x_{\rm com}-x_{\rm cop}\big),$$ the linear inverted-pendulum law: the COM accelerates <em>away</em> from the COP, so a forward lean is arrested by driving the COP forward, past the COM.`
*Why:* The sign was reversed and contradicted the module's own §1 (`x_cop = 0` giving `ẍ = +ω₀²x`); the parenthetical recipe got the right magnitude by accident and hid the argument, which is angular momentum taken about the COP.

**NUMBER — B6 (K3's solution, `module10.html:606`).**
*Before:* `The fastest settling ($\approx0.5\ \mathrm{s}$) sits at high $k_p\approx27$ with strong damping $k_d\approx6.8$ - pressed against the island edge. The optimum is a corner solution bounded by the delay, not an interior one`
*After:* `the fastest recovery is $0.50\ \mathrm{s}$ at $k_p=28.0\ \mathrm{s^{-2}}$, $k_d=8.0\ \mathrm{s^{-1}}$ … The optimum is <em>interior</em>, and that is the point. The stability island of Proposition 4.2 at $k_d=8.1$ and $\tau=0.10$ does not close until $k_p=57.0\ \mathrm{s^{-2}}$, so the best gains sit at half the ceiling`
*Why:* The stated gains sat at 51 % of the island ceiling, not against it; the true lesson is the opposite of the one printed — delay bounds the *useful* gain long before it bounds the *stable* gain.

**FIGURE-LABEL — B10 (Fig. 7's caption, `module10.html:231`).**
*Before:* `a simulated sway trace wanders like a damped random walk, staying within the $\pm\sigma$ band set by the stationary variance of Proposition 5.1 (dashed).`
*After:* `crossing the $\pm\sigma$ band of Proposition 5.1 (dashed) on about a third of its samples and peaking near $3\sigma$, as a Gaussian process must; what the theory fixes is not a bound but the trace's RMS, which matches the band's own value.`
*Why:* Decoding the 2400-point trace against its own ticks gives a band at `±0.340 deg`, trace RMS `0.358 deg`, `33.9 %` of samples outside it in 14 excursions, peak `0.944 deg = 2.8σ` — the drawing was right and the caption taught the reader that sigma is a bound.

**SVG — B11 (Fig. 8's Kalman-gain label, `module10.html:263`).**
*Before:* `K = σ²ₖ/(σ²ₖ+σ²ₘ) = 0.74` (SVG `<text>`, subscript entity `&#8342;`)
*After:* subscript entity `&#8346;` in both occurrences, and `K` renamed `K_f`.
*Why:* Proposition 6.1 boxes `K = σ_p²/(σ_p² + σ_m²)` with `p` for prediction; the figure wrote a subscript `k` that appears nowhere in the module — while its geometry was exactly right (`σ_p = 0.998`, `σ_m = 0.600`, fused `σ = 0.514` against the theoretical `0.515`).

**NUMBER — B15 (§1's concrete tie-in, `module10.html:105`).**
*Before:* `$J_{\max}\approx70\times3.1\times0.10\approx22\ \mathrm{N\,s}$ - about the impulse of a firm shove or a $3\ \mathrm{kg}$ mass swung at walking speed.`
*After:* `- the momentum of a $16\ \mathrm{kg}$ mass moving at walking speed ($1.4\ \mathrm{m\,s^{-1}}$), or of your own $70\ \mathrm{kg}$ brought to $0.31\ \mathrm{m\,s^{-1}}$, which is a firm shove and not a gentle one.`
*Why:* A 3 kg mass at 1.4 m/s carries `4.2 N s`, a fifth of 22 — and the anchor number is the one the reader remembers.


### Module 11 — Reaching, Waving, Holding, Gripping, and Manipulation

**Scale.** 19 blocking defects (B1–B19), 15 style edits, 60 anchored replacements. Report `editor-reports/module11.md` (480 lines).
**Verdict.** "Yes, after revision." Nine propositions each carry a correct proof and "the mathematics is the strongest part of the module" — "what stops the reader is the arithmetic and the provenance"; "none of this touches a proof. Every fix below is arithmetic, provenance, a label, or a table row."
**The one that mattered.** Lab A's inverse-kinematics helper had its two elbow branches labelled backwards: the docstring said `elbow=+1 up`, but under the module's own angle convention `+1` puts the elbow *below* the shoulder-to-hand line, and the array named `down` held the elbow-up solution. That error then walked downstream — K6 states an elbow-down pose and quotes `34.5 N`, which is the elbow-*up* number (the genuine elbow-down pose gives `52.29 N`). A reader tracing the figure back to the code would have found the code, the plot label, and the problem statement all agreeing with each other and all naming the wrong arm posture.

**NUMBER — B1 (`module11.html:173`).**
*Before:* `Add the arm's own weight (Module 1's segment masses, restored in the inverse dynamics of Section 6) and these roughly double.`
*After:* `Add the arm's own weight and these grow by much more than the cup alone suggests: … $(m_1\ell_{c1}+m_2\ell_1)g+m_2\ell_{c2}g=7.95+3.56=11.51\ \mathrm{N\,m}$ at the shoulder and $m_2\ell_{c2}g=3.56\ \mathrm{N\,m}$ at the elbow, so the totals are $14.45$ and $5.33\ \mathrm{N\,m}$ - the cup's torque multiplied by $4.9$ and $3.0$. The limb is the load; the mug is the surcharge.`
*Why:* Evaluating the module's own Proposition 6.1 gravity vector with its own Appendix segment values gives factors of `4.91` and `3.02`, not "roughly double".

**CODE — B2a/B2b (`module11.html:292,303`).**
*Before:* `"""Inverse kinematics; elbow=+1 up, -1 down. Returns (th1, th2)."""` and `down = np.array([ik(px, py, elbow=-1) for px, py in path])`
*After:* `"""Inverse kinematics. elbow=+1 puts the elbow BELOW the straight` / `    shoulder-to-hand line (elbow-down); -1 puts it above (elbow-up).` / `    Returns (th1, th2)."""` and `down = np.array([ik(px, py, elbow=+1) for px, py in path])` / `up = np.array([ik(px, py, elbow=-1) for px, py in path])`, with a print of both sweeps added — `elbow-up: shoulder sweep 62.8 deg, elbow sweep 36.6 deg` / `elbow-down: shoulder sweep 109.1 deg, elbow sweep 36.6 deg`.
*Why:* At the goal `(0.45,0.10)`, `elbow=+1` gives `θ₁=-56.3°, θ₂=+107.2°` with the elbow at `y=-0.250 m` (below the line) — the opposite of what the docstring claimed.

**SVG — B8 (K10's figure, `module11.html:562`).**
*Before:* The plot's y axis ran 0 to 300 N (`y = 165 - 0.4W`) while the solution reports a power-grip capacity of `593 N` at `μ=0.8` and the sweep reaches `μ=0.85`, where the model gives `736.7 N`. The polyline was clamped flat at `y=45.0` — the axis top — over roughly the last third of the sweep.
*After:* Regenerated on the same axis box with `y = 165 - 0.15W`, tick labels `0 / 400 / 800`, both polylines recomputed, and the two curve labels moved off the curves.
*Why:* The figure read "300 N" where its own text said 593 N, and the flat clipped segment looked like a real plateau in the capstan law.

**SVG — B5 (K8's figure, `module11.html:554`).**
*Before:* Decoding the two polylines against the figure's own axes (`y = 165 - 7.5F`): the red curve runs `4.91 → 9.41 N`, the true load; the blue curve runs `6.37 → 12.23 N`, which is `1.3×` the **true** load rather than the feedforward grip `1.3×0.5(g+1.5p)` (peak `7.35 N`). The blue curve therefore never dips below the red one — the figure drew a grip that never fails while a marker on it claimed a slip at `0.43 s`, and that marker sat on neither curve.
*After:* Regenerated at the same viewBox and axis box: red = load, blue = feedforward grip capacity switching to `1.3×` the instantaneous load at `t_reflex`, marker at the true crossing `t = 0.488 s`.
*Why:* The quoted slip time was wrong too (`0.488 s`, not `0.425 s`, so the reflex lands at `0.558 s`, not `0.495 s`), and the drawing hid the very failure the problem is about.

**NOTATION — B12 (`module11.html:230,507,508,561,563`).**
*Before:* `β` was both the resultant angle `β = arctan(F_t/F_c)` of Proposition 7.1 and the capstan wrap angle in `e^{μβ}`, with the notation table recording neither use. The SVG text read `resultant β` and `seated iff β ≤ α ⟹ …`.
*After:* The wrap angle keeps `β` (as the capstan law is universally written) and the local resultant angle becomes `ψ`; three prose occurrences and both SVG `<text>` bodies changed, and both symbols added to the notation table.
*Why:* One symbol meaning two things in one module, in a subject where the reader is already tracking a Jacobian's worth of indices.

**PROSE — B3a (`module11.html:280`).**
*Before:* `every plotted number below was produced by these scripts`
*After:* `each script prints the numbers its caption and interpretation quote`
*Why:* Three of the four lab scripts printed nothing at all — only Lab D printed (`manipulability=0.1350`, which matches) — so the provenance claim was false of Labs A, B and C until each gained the prints its captions had been quoting.


### Module 12 — Whole-Body Coordination and Motor Control

**Scale.** 14 blocking defects (B1, B2, B5–B16; the first agent's tag sequence has no B3 or B4), 22 style edits, 96 anchored replacements. Report `editor-reports/module12.md` (298 lines). The first agent on this module applied 76 edits and died before writing anything down, so sections 2–5 of the report are reconstructed from the applied diff — verified by checking that `cp module12.html edited/module12.html && python apply.py` reproduces the delivered file byte for byte.
**Verdict.** "Yes, after revision." Ten propositions and a lemma all carry proofs of matching weight and "the Euler-Poisson to minimum-jerk to 1.875 chain is the best-built passage in the module"; "what stopped the reader before this pass was elsewhere, and it was mostly arithmetic and notation rather than argument."
**The one that mattered.** K6's figure drew the minimum-jerk bell — decoded from its own polyline, it peaks at `1.874 at τ=0.496` and matches `1.875 τ²(1-τ)²/(1/16)` to 0.002 at every one of 120 points — inside a problem whose solution, three lines below, says the answer is *not* minimum jerk but `1.736 at τ=0.68`. The figure drew the very thing the problem exists to distinguish itself from, so a reader who trusts the picture learns the opposite of the result. It passed all nine gates; it was found only by decoding the point string.

**SVG — B13 (K6's figure, `module12.html:483-484`).**
*Before:* A 120-point polyline peaking at `1.874 at τ=0.496`, matching the minimum-jerk profile `1.875 τ²(1-τ)²/(1/16)` to 0.002 over every point, beside a solution reading "peaking at $1.389\ \mathrm{m/s}$ at $\tau=0.68$ with a peak-to-mean ratio of $1.736$ - between minimum acceleration's $1.500$ and minimum jerk's $1.875$".
*After:* The solid curve regenerated from the K6 solution's own script (`figgen.k6_speed()` runs the identical 100-step quadratic program), with minimum jerk added as a dashed grey comparison and both labelled: "min-variance optimum: peak 1.736 at $\tau$=0.68" and "dashed: minimum jerk, 1.875 at $\tau$=0.50".
*Why:* Decoding the delivered result now returns `1.736 at τ=0.68` for the solid curve and `1.875 at τ=0.50` for the dashed one — the sentence "between 1.500 and 1.875" finally has a picture.

**SVG — B12 (Lab B's second figure, `module12.html:310`).**
*Before:* The blue curve is exactly `t_s = 4√2 R^(1/4)` (max deviation 0.009 s over 40 points) and runs from `1.79 s` to `17.89 s`, but the y-axis top tick was `10` and the axis line stopped at `y=40`, which is `11.0` on that scale. Everything past `log₁₀R ≈ 1.19` — about 40 % of the curve — was drawn above the frame in blank space with no gridline or tick to read it against. `check_frame` did not fire because the viewBox had been widened to `6 -81 488 339`, 81 user units of empty space above the plot, so nothing was technically clipped. The `aria-label` read "Position gain and settling time versus the effort weight R on a log axis, **both falling** as effort is priced higher."
*After:* Axis rescaled to 20 s (the `5` and `10` ticks become `10` and `20`, `7.725` px per unit), both analytic curves regenerated on the new scale, legend moved left, viewBox retightened to `26 32 452 218`, and the `aria-label` rewritten to "the gain falls as R rises, the settling time climbs".
*Why:* An oversized viewBox turned a clipping bug into a silent one — the gate saw empty margin, the reader saw a curve leaving the plot — and the screen-reader label asserted the opposite of the figure's own caption.

**NUMBER — B1 (Lab C, `module12.html:315,337,339`).**
*Before:* `the steady force they press with is $K(x_{\rm des}-x_{\rm wall})$: the impedance controller settles at $200\times0.05=10\ \mathrm{N}$, the stiff servo at $5000\times0.05=250\ \mathrm{N}$ - $25\times$ larger`
*After:* `The impedance controller peaks at $21\ \mathrm{N}$ and settles at $9.98\ \mathrm{N}$; the position servo peaks at $388\ \mathrm{N}$ and settles at $238.10\ \mathrm{N}$ - a factor $23.9$ in the settled force and $18.6$ in the peak … The settled values are the closed-form $K_ck_w(x_{\rm des}-x_w)/(K_c+k_w)$ of the Model line, and the code prints that prediction beside the simulation to confirm it.`
*Why:* The prose modelled a rigid wall while the code gave the wall a finite stiffness `kw`; the rigid-wall estimate is exact for the compliant controller and 5 % high for the stiff one — which is the physical point the section was reaching for and missed. The figure had also been drawn on a 300 N axis while the servo trace reaches 388 N.

**MATH — B5 (Proposition 7.1, `module12.html:190,192`).**
*Before:* `<div class="proof">(Sketch; the quadratic-program step below is exact, and the bell shape follows once the plant's command-to-force smoothing is included.) ... by Lagrange multipliers its solution spreads the command smoothly over the whole movement (each $u_k\propto b_k/w_k$) rather than concentrating it in large, noisy bursts.`
*After:* The minimiser stated in closed form, $$u_k=\frac{x_T}{\sum_j b_j^2/w_j}\cdot\frac{b_k}{w_k},$$ with existence and uniqueness from strict convexity, stationarity from the Lagrangian, and the optimal variance `c x_T²/Σ_j b_j²/w_j` shown to be exactly the Cauchy-Schwarz bound — so restricting the command to a subset `S` raises the variance by `(Σ_j b_j²/w_j)/(Σ_{j∈S} b_j²/w_j) ≥ 1`.
*Why:* The load-bearing proposition of §7 asserted a qualitative conclusion and announced its own incompleteness, while sitting beside nine proved siblings; a burst is now penalised in exact proportion to the weight it leaves unused.

**NOTATION — B11 (D9's solution, `module12.html:453`, and Fig. 8's aria-label at `:222`).**
*Before:* `Subtracting the two oscillator equations gives $\dot\psi=\Delta\omega-2K\sin\psi$ ... So oscillators within coupling bandwidth $2K$ synchronize at phase lag $\psi^\star=\arcsin(\Delta\omega/2K)$ (Proposition 8.2).`
*After:* `Subtracting the two oscillator equations gives the Adler equation $\dot\psi=\Delta\omega-2\kappa\sin\psi$ ($\psi=\phi_2-\phi_1$, coupling strength $\kappa$) … synchronize at phase lag $\psi^\star=\arcsin(\Delta\omega/2\kappa)$ (Proposition 8.2).`
*Why:* `K` was both the LQR feedback gain and the oscillator coupling; after the rename to `κ` this one surviving `K` made the solution cite a Proposition in one symbol while writing the same law in another — one law, two symbols, on the same page.

**NUMBER — B15/B16 (K9 and K4 solutions, `module12.html:496,476`).**
*Before:* `The third component adds $0.074$ and the fourth adds $0.0003$, a factor $250$ drop` and, in K4, `all three converge to $u_\infty=p=1$ with aftereffect $-1.000$ … $2.5\times10^{4}$ by trial $25$.`
*After:* `The per-component increments the code prints are $0.7453$, $0.1787$, $0.0736$, $0.000564$, $0.000512$: the third component adds $0.0736$ and the fourth adds $0.000564$, a factor $130$ drop, after which every further increment is flat at the $5\times10^{-4}$ noise floor.` and, in K4, `after $25$ trials the code prints $-1.000$ for $\eta=0.5$ and $\eta=1.0$ but only $-0.996$ for $\eta=0.2$, because $0.80^{25}=3.8\times10^{-3}$ of the perturbation is still unlearned.`
*Why:* The fourth VAF increment is `0.000564`, a factor `130` drop, not `0.0003` and `250`; and at `η=0.2` the run has not converged — the aftereffect is `-0.996`, because `0.80²⁵ = 3.8×10⁻³` of the perturbation is still unlearned.


### Module 13 — Daily-Life Movement Case Studies

**Scale.** 17 blocking defects, 22 style edits, 102 anchored replacements. Report `editor-reports/module13.md` (1057 lines).
**Verdict.** "Yes, after revision. The mechanics is right and the six propositions are all genuinely proved: 2.1, 3.1, 4.1, 5.1, 6.1 and 7.1 each carry an adjacent `.proof` that derives the boxed result rather than restating it."
**The one that mattered.** Section 4 re-analysed the exact stooped lift Module 1 had already worked — same 20 kg box, same 0.40 m reach, same 0.30 m trunk arm, same 0.05 m muscle arm — but quietly used an upper body of 0.50 M instead of Module 1's 0.60 M. The same lift therefore came out at 3630 N in Module 13 and 4040 N in Module 1, with no word about the difference. A reader who trusted both pages would have two spinal compression forces for one movement and no way to tell which is the course's answer.

**NUMBER — B2 (running example diverges from Module 1).**
*Before:* `For a $20\ \mathrm{kg}$ load at $d_L=0.40\ \mathrm{m}$, trunk mass $W_{\rm tr}=0.5mg$ at $d_{\rm tr}=0.30\ \mathrm{m}$, and $d_m=0.05\ \mathrm{m}$: $F_m\approx3630\ \mathrm{N}$ and $F_{\rm comp}\approx4200\ \mathrm{N}$ (a conservative upper bound - see the proof)`
*After:* Proposition 4.1 rebuilt on Module 1's parameters — `$W_{\rm tr}=412$ N` (0.60 M), `$\ell_t=0.346$ m`, `$d_{\rm tr}=\ell_t\sin\phi$` — giving stoop 4040 N / 4350 N and squat 2530 N; the `$\cos\phi\le1$` hedge deleted.
*Why:* `cascade.py` recomputes $F_m=4041.7$ N and $F_{\rm comp}=4345.8$ N, matching `module01.html`'s published 4040 N and 4346 N to the newton.

**MATH — B6 (K2's sensitivity runs the wrong way).**
*Before:* `the sensitivity $\partial f_{\max}/\partial m=-250/(m^2gh)$ steepens at low power ceilings.`
*After:* `The sensitivity is $\partial f_{\max}/\partial m=-P/(m^2gh)$, proportional to the ceiling itself: at $70\ \mathrm{kg}$ it is $0.018\ \mathrm{steps\,s^{-1}kg^{-1}}$ for a $150\ \mathrm{W}$ ceiling and $0.049$ for a $400\ \mathrm{W}$ one.`
*Why:* Burying the constant 250 inside the derivative hid the very dependence the sentence claimed, and inverted it — the sensitivity steepens at *high* ceilings, 0.0184 at 150 W against 0.0489 at 400 W.

**NOTATION — B12 plus its two follow-up rows (the rename that missed five).**
*Before:* One `$\mu$` for skin-on-lid friction (§6, C7, K6) and shoe-on-floor friction (K5), both given 0.7 so the collision never showed; one `$d$` for the chair arm (Appendix `:499`) and the door arm (§6 `:175`, C8 `:364`).
*After:* `$\mu_{\rm lid}$`, `$\mu_{\rm shoe}$`, `$d_{\rm hinge}$`, each with its own notation-table row — but the first pass left five bare `\mu` behind, one in §6's interpretation (`a rubber pad or a dry hand raises $\mu$`) and four more inside D5's solution.
*Why:* A grep for `\mu` not followed by `_` found 5 hits after the "complete" rename and 0 after the repair; a symbol the notation table no longer defines is worse than the collision it replaced.

**SVG — B16 (four heads floating off four bodies).**
*Before:* In each of Fig. 2's four vignettes the head circle floats clear of the shoulder sphere with no neck — `rise` a 10.1 px gap, `climb` 6.4 px, `lift` and `catch a stumble` 9.5 px each; and the `climb` label at (190,226) sat inside stair rectangles running to `y=240`.
*After:* One neck capsule per vignette, computed with the `CLAUDE.md` bone generator from the existing coordinates and inserted inside the existing `<g filter="url(#b_sh)">` so the head overlaps its top — e.g. rise: `x="71.3" y="92.5" width="27.4" height="9" rx="4.5" rotate(-57.5 85 97)`; the three stair rectangles shortened to end at `y=212` (heights 12, 28, 44 from unchanged tops 200, 184, 168).
*Why:* It passed all nine gates — a gap is not a clipped bounding box, a label over a curve, or a hairline limb — so only a render and a human eye could catch it.

**FIGURE-LABEL — B9-K3fig-aria and B8-K10fig (figures describing the wrong problem).**
*Before:* K10's figure was byte-for-byte K1's chair-torque-versus-$d$ plot but for its aria-label (2590 vs 2591 chars), so a problem about ranking five tasks showed a plot of one; and K3's replacement figure kept the aria-label of the problem it replaced — itself truncated mid-sentence with an ellipsis and reading raw TeX (`$3400\ \mathrm{N}$`) aloud to a screen reader.
*After:* K10 gets a ranking bar chart whose five bars are `kblocks/K10.py`'s five computed percentages (87.9 / 84.1 / 62.8 / 47.7 / 47.1); K3's label rewritten to describe the three curves actually drawn, in words.
*Why:* `verify_dom`'s stray-`$` advisory fell from 18 to 16 once the raw TeX left the label — the only gate that noticed either defect at all.

**CODE — B5 (the module promised code four times and shipped none).**
*Before:* `every proposition proved, every figure computed, every number reproduced by the code shown.` — while `K1` through `K10` contained no `<pre><code>` block at all, and Lab A's 82, 154 and 0.19 and Lab D's 1.72 appeared in captions printed by no code.
*After:* Ten blocks written, run and `pycodestyle`-clean, spliced into their solutions; Lab D gains `print("max recoverable speed with no delay: %.2f m/s" % (w0*(max_step - x0)))`, which prints `max recoverable speed with no delay: 1.72 m/s`.
*Why:* The fix is to write the code, not to withdraw the claim — the edited file's 14 blocks were all extracted and re-run, and every one prints the numbers the prose beside it quotes.


### Module 14 — Aging, Injury, Degeneration, and Adaptation

**Scale.** 16 blocking defects, 11 style edits, 63 anchored replacements. Report `editor-reports/module14.md` (380 lines).
**Verdict.** "Yes, after revision. … Propositions 2.1, 3.1, 3.2, 5.1, 6.1 and 7.1 are each short, correct and genuinely proved. What stops the reader is the problem set and two claims that the module's own arithmetic contradicts."
**The one that mattered.** K3 asked where cartilage stops maintaining itself and answered "a threshold between 0.4 and 0.6". Run with the module's own constants, the saddle-node sits at L\* = 0.211 — half the lower bound claimed — and *both* of the loads the solution called stable run away, in 153.5 and 84.0 years. The "stable h ≈ 1.2 mm" a reader would have taken as an equilibrium is just where a different load happens to be passing at year 60. The wrong number sat under the module's whole osteoarthritis argument.

**NUMBER — B2 (K3's threshold, its regime labels and its "stable thickness").**
*Before:* `at full load ($L=1.0$) and at $L=0.6$ the cartilage runs away to zero, but at $L=0.4$ it settles to a stable $h\approx1.2\ \mathrm{mm}$ - a threshold between $0.4$ and $0.6$ separating a degenerating joint from a maintained one.`
*After:* `saddle-node at L* = 0.211, h* = 0.824 mm` / `L=0.40: cartilage spent (h=0.30 mm) at t = 153.5 yr` / `L=0.60: cartilage spent (h=0.30 mm) at t =  84.0 yr` / `L=1.00: cartilage spent (h=0.30 mm) at t =  44.5 yr`
*Why:* Setting $dh/dt=0$ gives $L_{\rm eq}(h)=\beta(h_0-h)/[\kappa p_0(h_0/h)^{n_{\rm c}}]$, whose maximum *is* the saddle-node — the module's own Lab C code settles it with $\kappa=\beta=0.010$, $p_0=3$ MPa, $h_0=2$ mm, $n_{\rm c}=0.7$.

**MATH — B4 (Proposition 4.1's proof assumes its conclusion).**
*Before:* `Modelling the area's thickness dependence as a power law $A\propto h^{n_{\rm c}}$ yields $p_{\rm peak}=p_0(h_0/h)^{n_{\rm c}}$; the loss of interstitial fluid pressurisation as proteoglycan is lost … plac[es] $n_{\rm c}$ toward the upper end of its range.`
*After:* Two solvable limits of the same geometry bracket the exponent — a Winkler compressible thin layer giving `$p_{\rm peak}=(H'/h)\delta_0=\sqrt{PH'/(\pi Rh)}\propto h^{-1/2}$`, i.e. `$n_{\rm c}=\tfrac12$`, and a bonded incompressible layer giving `$p_{\rm peak}\propto G^{1/3}R^{-1/3}P^{2/3}h^{-1}$`, i.e. `$n_{\rm c}=1$`; the fluid-loss direction reversed, since losing pressurisation moves $n_{\rm c}$ *down* toward $\tfrac12$.
*Why:* The step from "a thinner layer has a smaller contact area" to $A\propto h^{n_{\rm c}}$ was the entire content of the proposition, and it was assumed — while that exponent drives §4's feedback loop, Lab C and K3 alike.

**SVG — B10 (Lab C's runaway drawn as a plateau).**
*Before:* Caption: `a fully loaded joint's peak stress climbs into a runaway` — but the y-axis ended at 9.0 MPa, the model crosses 9.0 MPa at year 43, and the generator clamped $h$ at 0.05 mm, so from year 43 to year 60 the drawn curve is a horizontal line at the ceiling.
*After:* y-axis to 12 MPa, integration stopped at `$h=0.30$ mm` (taken as spent) instead of clamping, curve ending at a marked point; the $L=1$ curve climbs 3.0 → 11.32 MPa and reaches 0.30 mm at $t=44.5$ yr.
*Why:* A reader saw a stress that rises and then settles — the opposite of the caption and of the physics — and it passed every one of the nine gates, because a clamped curve is not a clipped bounding box.

**FIGURE-LABEL — B2c (an axis label naming a quantity the curve does not plot).**
*Before:* K3's figure plotted `$L\!\cdot\!p$` on an axis labelled `peak stress (MPa)`, so its $t=0$ value read 1.2 MPa where the module's own $p_0=3.0$ MPa; and it drew the $L=0.4$ transient as the "low: stable" curve.
*After:* Replaced by a bifurcation diagram — $L_{\rm eq}(h)$ against $h$, maximum marked at `$L^\star=0.211$, $h^\star=0.82$ mm`, annotated "above: no steady state, runaway" and "below: maintained".
*Why:* Recovered by calibrating the old axis from its tick `<text>` coordinates and inverting — a load-weighted stress wearing a peak-stress label is invisible to every automated check and to a casual look at the render.

**FIGURE — B3 (a K5 figure that simulates nothing).**
*Before:* Reading the polylines back, muscle falls **linearly** to 0.875 over forty years — `$0.31\%$/yr, not the module's $1\%$/yr` — and bone is flat for 15 years then linear to 0.783, while the caption claimed "the two curves lock together and steepen".
*After:* Regenerated from a new Proposition 8.1, `$C_{\rm b}(t)=1-\tfrac12 k_{\rm ad}r\,t^{2}$` — linear muscle, quadratic bone, dashed fracture-density line at 0.79 with the crossing marked at 36.5 yr.
*Why:* A mechanostat integrating a linear stimulus deficit gives a quadratic, not a straight line, so no coupled model produces the picture that shipped — and the claimed steepening does not occur anywhere in it.

**NUMBER — B6 ("two hundred years of headroom", in a law capped at 100).**
*Before:* `two extra reserve units at $r=0.01$ is two hundred years of headroom in the linear model, i.e. the crossing never comes within a lifespan.`
*After:* `Since $a^\star-a_0=\frac1r(1-D/\tau_p)$ and $D/\tau_p\gt 0$, no starting reserve can push the crossing further than $1/r=100$ years past $a_0$; going from a starting reserve of $\tau_p/D=1$ to $3$ buys $\frac1r(1-\tfrac13)=66.7$ years`
*Why:* The 200 came from extrapolating the local slope $1/[r(\tau_p/D)^2]$ from its value at $\tau_p/D=1$ — but that slope falls as $(\tau_p/D)^{-2}$, to 39.5 at the module's own reference 1.59 and 11.1 at 3.


### Module 15 — Measurement, Estimation, and Inverse Dynamics

**Scale.** 23 blocking defects, 12 style edits, 78 anchored replacements. Report `editor-reports/module15.md` (984 lines).
**Verdict.** "Yes, after revision — and the revision is not cosmetic. This module has the best architecture of any in the second half of the course. … What fails is the arithmetic layer, and it fails systematically."
**The one that mattered.** The module told the reader three times that every quoted number is reproduced by the code shown. Four of its five shipped listings raise `NameError` on the first run — they use `q_meas`, `q_true` and `a_com_kin`, none of which the reader is ever given — and the fifth runs and prints nothing. So a reader who did exactly what the module asked, run the code and check the numbers, could not verify a single figure in it. In a module whose whole subject is how far to trust an inferred number, that is the worst possible place to lose the ground truth.

**CODE — B3 (the listings the module stakes its credibility on).**
*Before:*
```
blk01_L360.py  (Sec 7 pipeline)  runs, prints NOTHING
blk02_L429.py  (Lab A)   NameError: name 'q_meas' is not defined
blk03_L452.py  (Lab B)   NameError: name 'q_meas' is not defined
blk04_L474.py  (Lab C)   NameError: name 'q_true' is not defined
blk05_L495.py  (Lab D)   NameError: name 'a_com_kin' is not defined
```
*After:* Five self-contained PEP8 fixed-seed scripts that define what they use and print what the prose quotes — `nb1.py  true peak torque 3.31 N m / filtered 0.071 / unfiltered 1.70`, `nb2.py  chosen cutoff: median 3.09 Hz, 5-95% [2.79, 3.80]`, `nb3.py  torque-optimal cutoff 3.4 Hz (RMSE 0.022 N m); 1.5 -> 0.23; 30 -> 1.34`, `nb4.py  peak 3.41 +/- 0.58 N m (1 sd); 95% CI [2.22, 4.53]; true 3.31`, `nb5.py  identified M: 70.03 (N=20) ... 70.00 (N=200); static hold 69.97` — and the three claims narrowed to "every quoted number is printed by the code shown, which is self-contained and runs as printed with no other input."
*Why:* The code blocks are the only ground truth the domain brief recognises for a computed number.

**NUMBER — B21 (two statistics compared as if they were one).**
*Before:* `its unfiltered torque error is four times smaller than the $7.31\ \mathrm{N\,m}$ the compact stencil gives **on the same data**`
*After:* On the seed-15 draw the compact stencil gives **6.68 N m**, and `$6.68/1.70=3.93$` — the stencil ratio Proposition 3.1 predicts.
*Why:* It was not the same data: 1.70 was a single seed-15 draw from §7's own listing, while 7.31 was a 400-draw mean from a scratchpad script whose wide-stencil counterpart in that run was 1.7833 — and the mismatched pair concealed the exact ratio the module's own proposition predicts.

**MATH — B1 (a stated optimum that was never computed).**
*Before:* `Figure 4 is this proposition computed for the Section 3 signal: the bias falls and the variance rises with $f_c$, and their sum bottoms out near $f_c^\star\approx7\ \mathrm{Hz}$`
*After:* `fc* = 3.02 Hz   bias 0.0132   noise 0.0156   total 0.0205 rad/s` / `fc = 7 Hz  ->   total 0.0497 rad/s          (2.4x the minimum)`
*Why:* Decoding the figure's polylines back through its own axes gives curves that no bias-variance calculation on any signal in the module produces — and 7 Hz is not the optimum of either candidate signal (the §3 signal's is 3.36 Hz).

**NOTATION — B10 (one letter, two lengths, a factor 0.43 apart).**
*Before:* Definition 2.2 fixes `$L_i$` as the segment length with `$\rho_i$` the COM fraction, so joint-to-COM is `$\rho_iL_i$` — yet every torque formula writes `$\tau=I\ddot q+mgL\sin q$` with `$L=0.25\ \mathrm{m}$`, which is the distance to the COM. Ten sites plus one SVG label.
*After:* The second meaning gets its own symbol, `$\ell=\rho_iL_i$`, throughout — the §7 model, the §8 partials (`$\partial\tau/\partial m=g\ell\sin q$`), the D9 linearisation, the limit cases, K4's parameter block, C10 and C10's figure label, which becomes `τ = mgℓ` (the entity `&#8467;`, since MathJax does not typeset inside `<svg><text>`).
*Why:* A factor $\rho\approx0.43$ hidden inside a reused letter, in the one module whose subject is getting the gravity term right.

**FIGURE-LABEL — B23 (a figure announcing a different problem).**
*Before:* K7's error-budget bar chart carried **0.41 / 0.31 / 0.09** — numbers B6 had already replaced with 0.414 / 0.228 / 0.059 — with no bar for the filter bias, and its `aria-label` read *"K4: The exercise shows the recursion is a short loop..."*, text lifted from K6's solution.
*After:* Four bars redrawn at the verified values with the label on each bar, and the `aria-label` rewritten to describe the figure it labels.
*Why:* The one representation a screen-reader user gets for K7 named the wrong problem and quoted three superseded numbers; it was found by decoding every problem figure's text labels, not by reading.

**SVG — B16 (a fix that created its own defect).**
*Before:* `drawn [2.28, 4.51]   vs   caption and code [2.22, 4.53]` — Lab C's green "95 % interval" bar was still drawn from the superseded run after B5 corrected the caption to what the shipped code prints.
*After:* Histogram, true-value marker and interval bar all redrawn from the same 2000 draws the listing prints, keeping the axis calibration `$x = 75 + 105.38\,(v-1.5)$` so the tick labels still land on their ticks; decoding the new figure returns [2.220, 4.534] against the model's [2.220, 4.534].
*Why:* A figure that disagrees with its own caption is a factual error — and here the correction to B5 is what created it, which is why the figure decode has to be re-run after every caption fix.


### Module 16 — Continuum and Finite-Element-Style Tissue Models

**Scale.** 17 blocking defects, 13 style edits, 55 anchored replacements. Report `editor-reports/module16.md` (679 lines).
**Verdict.** "Yes, after revision. … The theoretical spine is genuinely good: Propositions 1.1, 2.1, 3.1, 4.1, 5.1, 6.1 and 7.1 each carry a proof that a reader can reproduce with a pen. … What stops the reader is the second half."
**The one that mattered.** Lab C did not perform the experiment it described. The code solves Terzaghi consolidation under a step *load*, where the total stress is constant by construction and nothing relaxes — while the heading, the caption and K8 all describe step-*strain* stress relaxation, a different boundary-value problem with a different eigenseries. The figure papered over the mismatch by drawing the layer-averaged pore pressure, relabelling the axis "normalised stress", and standing it on an equilibrium floor of 0.35 that appears in no table, no derivation and no assumption. A reader would have taken a load-partition curve as proof of a relaxation law.

**SVG — B1 (a curve wearing another quantity's label, on an invented floor).**
*Before:* Decoded against its own axis calibration (0.35 at `$y=185.3$`, 1.0 at `$y=59.4$`; ticks 0, 248, 495 on $x$), the plotted curve is `$0.35+0.65\langle p\rangle$`, matching the module's own solver to a maximum deviation of 0.0011 over all 100 points — under an axis labelled "normalised stress" with a floor labelled "equilibrium (matrix)".
*After:* Two computed polylines, the fluid share `$F(T)=\langle p\rangle/\sigma_0$` and the matrix share `$U(T)=1-F(T)$` against `$T=c_vt/L^2$`, with a dashed reference at the crossing `$T_{1/2}=0.195$`; the interpretation's `$\approx0.24$` corrected to the printed `0.2347`.
*Why:* The 0.35 existed only to make an affine rescaling of the mean pore pressure look like a stress-relaxation curve; decoding the new figure returns exactly the numbers the solver prints.

**FIGURE-LABEL — S13 (a figure still quoting the number its solution no longer says).**
*Before:* K6's schematic carried the label `ratio &#8776; 12&#215;`.
*After:* `ratio &#8776; 12.5&#215;`
*Why:* The solution had been corrected to compute 12.5 (`anisotropy ratio E(0)/E(90) = 12.5`), and the Appendix restated to match — the figure was the one place the superseded 12 survived, found only by sweeping every number printed inside a problem figure's `<text>` against that problem's solution.

**MATH — B10 (the law the figure already draws, never stated).**
*Before:* `The effective stiffness is highest at $0^\circ$ (load along fibres, $\approx1.5\ \mathrm{GPa}$) and lowest at $90^\circ$ (across, $\approx0.12\ \mathrm{GPa}$), an anisotropy ratio $\approx12$. Sweeping the angle traces the fall governed by the $\mathbf a\otimes\mathbf a$ fibre term, which contributes only its projection onto the load direction.`
*After:* `$$\boxed{\;E(\theta)=E_m+E_f\cos^4\theta.\;}$$` — the fibre resolves the strain once, `$\varepsilon_a=\varepsilon\cos^2\theta$`, and reading the stress back along the load direction resolves it a second time; sweeping gives `$1.500$, $1.321$, $0.896$, $0.465$, $0.206$ and $0.120$ GPa` at 0, 15, 30, 45, 60, 90 degrees, halving by `$34.7^\circ$`.
*Why:* Fitting Fig. 7's own polyline gives $E(\theta)=0.129+1.377\cos^4\theta$ with an RMS residual of 0.0052 GPa, against 0.118 for $\cos^2\theta$ — the figure had been drawn from the $\cos^4$ law all along, and "contributes only its projection" was the wrong count of projections.

**PROOF — B4 (Cauchy's theorem asserted inside a definition).**
*Before:* `Cauchy's theorem states that this dependence on $\mathbf n$ is <em>linear</em>: there is a single second-order tensor $\boldsymbol\sigma$, the <b>Cauchy stress</b>, with` — followed by the boxed `$\mathbf t(\mathbf n)=\boldsymbol\sigma\mathbf n$`, inside `Definition 2.1`.
*After:* Split into a traction-only Definition 2.1 and a new **Proposition 2.1** with a tetrahedron proof — `$$\mathbf t(\mathbf n)\,A-\sum_j\mathbf t^{(j)}An_j+\mathbf b\,V=\rho V\ddot{\mathbf x},$$` with surface terms $\sim h^2$ and volume terms $\sim h^3$, so body force and inertia die as $V/A\sim h$; the symmetry result renumbered Proposition 2.2 across `:150`, `:454`, `:504`.
*Why:* Linearity in $\mathbf n$ is the least obvious claim in the module — nothing about "force per unit area across a cut" says nine numbers fix the traction on infinitely many cut orientations — and the proof was not missing, it sat unused in problem D3, eight sections after the reader was asked to accept the result.

**NUMBER — correction 1 (a cartilage clock wrong by three orders of magnitude).**
*Before:* K8's cartilage clock used `$c_v\sim10^{-6}\ \mathrm{m^2\,s^{-1}}$`, giving `$t_{1/2}\approx0.8\ \mathrm s$` and the conclusion "standing still for a minute leaves the load on the matrix".
*After:* Module 4's own table (`module04.html:566-568`) gives `$H_A=0.6\ \mathrm{MPa}$, $k=1\times10^{-15}$`, so `$c_v=6\times10^{-10}$`; the run prints `t_half = 1300 s = 22 min` and fluid shares `0.986 / 0.893 / 0.214` at 1 s / 60 s / 1 h — flipping the conclusion: a footstep *and* a minute of standing are both fluid-borne.
*Why:* The unsourced $10^{-6}$ was itself the bare-number defect class the report calls blocking — and this correction was made to the report during the apply, not to the manuscript before it.

**CODE — B9 (a problem that asks an element to detect its own blind spot).**
*Before:* `As the beam is made stubbier (small $L/h$), shear deformation the Euler-Bernoulli model omits grows and the two disagree, marking the slender-body limit where Module 2's beam theory is valid. The finite element reproduces the analytic model and shows exactly where it breaks.`
*After:* The run shows the element and the formula agree at every aspect ratio — `# -> one beam element : tip deflection = 0.333333333333` / `# -> Euler-Bernoulli  : P L^3/(3 EI)   = 0.333333333333` / `# -> difference       = 0.00e+00` — so the problem now asks for the Timoshenko shear term as a third quantity, `$\delta_s/\delta_b=\tfrac{E}{4\kappa G}(h/L)^2$`, printing `# -> L/h = 20: shear adds  0.20% that neither model contains` down to `L/h = 2: shear adds 19.50%`.
*Why:* An Euler-Bernoulli element contains no shear flexibility, so it can never disagree with Euler-Bernoulli — the problem as written asked for a difference that is identically zero.


### Module 17 — Capstone Modeling Projects

**Scale.** 14 blocking defects, 17 style edits, 42 anchored replacements. Report `editor-reports/module17.md` (1094 lines).
**Verdict.** "Yes, after revision. … What stops the reader is that the capstone module is the one module that does not hold itself to the standard it preaches. Principle 1.3 says an answer without an error bar is not a result; the module reports fourteen headline numbers without one."
**The one that mattered.** Section 4 and Fig. 4 credited the inverted-pendulum vault with walking's twin-peaked M-shaped ground force. The model cannot produce it: for a rigid vault $\ddot y_{\rm COM}<0$ throughout single support, so $F\le mg$ at every instant, and the force is *largest* at mid-stance — a single hump, the exact inverse of the curve drawn. The two 1.18 BW peaks belong to the step-to-step transition, which the same paragraph lists among the model's omissions two sentences later. A reader would have taken a borrowed shape as a derived prediction.

**SVG — B1 (a figure crediting a model with a shape it inverts).**
*Before:* `The vault produces the M-shaped vertical force of Fig. 4 (blue): a loading peak as the COM rises, a mid-stance dip <em>below</em> body weight as it crests the arc (centripetal unloading), and a push-off peak.`
*After:* `The vault earns exactly one number, the mid-stance <em>value</em> … Integrating a rigid vault gives $F\le mg$ at every instant, because $\ddot y_{\rm COM}\lt0$ throughout the arc, and the force is <em>largest</em> at mid-stance, falling to $0.49$ BW by $\pm20^\circ$ of leg sweep: the model draws a single hump, the inverse of the measured $\cup$ … That is the honest reading of Fig. 4: one number earned, the shape borrowed.`
*Why:* Decoding Fig. 4 from its own y-ticks (195.0, 139.6, 84.3 for 0, 1, 2 BW; least-squares fit `$y=-55.350\,\mathrm{BW}+194.983$`, residual 0.033 px) gives peaks of 1.183 BW and a mid-stance value of 0.701 BW — matching $mg(1-\mathrm{Fr})=0.698$ BW at $\mathrm{Fr}=0.302$, which is the one thing the model does own.

**NUMBER — B2 (an asserted stability boundary, wrong and uncomputed).**
*Before:* `A $200\ \mathrm{ms}$ delay is past the critical delay $\Delta_c\approx150\ \mathrm{ms}$` — stated in four places, derived nowhere, in no table, labelled no assumption.
*After:* A new Proposition 2.2 with proof: `$$\boxed{\;\Delta_c=\frac{1}{\omega_c}\arctan\!\Big(\frac{k_d\,\omega_c}{k_p}\Big).\;}$$` With the module's own $I=70\ \mathrm{kg\,m^2}$, $mgL=686.70$ N·m, $k_p=1030.05$ N·m, $k_d=150$ N·m·s the quadratic `$4900u^2+73638u-589446=0$` gives `omega_c = 2.404 rad/s (period 2.61 s)` and `critical delay = 140.1 ms`; the shipped integrator bisects to `-> bisected critical delay = 140.2 ms`.
*Why:* The qualitative conclusion survives (140 ms is still above the human 100 ms) but the number changes status from asserted to derived — $\Delta_c=150$ ms would have needed $k_d=161.8$ N·m·s.

**MATH — B3 (a box whose own derivation misses it by a factor of four).**
*Before:* `set by an impulse balance: the stance impulse must reverse the vertical flight momentum, $\int F\,dt=2m v_{\rm land}$, and spread over the short contact time $t_c$ this gives a peak of order $2m v_{\rm land}/t_c\approx2.5\text{-}3\,mg$.` — with the parameter line admitting `leg stiffness tuned so the peak is $\approx2.6$ BW`.
*After:* `$$\boxed{\;F_{\rm peak}\approx\frac{\pi}{2}\,\frac{mg}{\beta},\qquad \beta=\frac{t_c}{t_{\rm step}}.\;}$$` — with `$\beta=0.606$`, a mean stance force of `$1133\ \mathrm N=1.65$ BW` and a peak of `$1780\ \mathrm N=2.59$ BW`.
*Why:* The stated quantity evaluates to 343–515 N, i.e. 0.50–0.75 mg, low by about four: the chain dropped the weight impulse $mg\,t_c$, the duty factor, and the peak-to-mean shape factor $\pi/2$ — and the stiffness that was "tuned" to the answer never enters the balance at all.

**NOTATION — B9 (one letter, two axes, two inertias).**
*Before:* `$I=mL^2=70\ \mathrm{kg\,m^2}$` about the ankle at `:130`, against `$I=0.12\ \mathrm{kg\,m^2}$` about the knee at `:170`, `:172` — with the notation table merely recording the collision.
*After:* Section 2 keeps `$I$`, since it carries the pendulum equation and the whole of Proposition 2.2's proof; Section 3's becomes `$I_{\rm k}$`.
*Why:* Recording a collision in a notation table is not resolving it — and the module proves it knows the rule at `:241`, where `$k_c$` is introduced as "distinct from the leg-spring $k$ of Section 5"; it simply never applied that rule to $d$, $I$ or $\phi$.

**FIGURE-LABEL — B13 (an axis that misreports its own scale).**
*Before:* `<line x1="66" y1="117.5" x2="70" y2="117.5" stroke="#333"/>` labelled `8`, and `<line x1="66" y1="47.8" x2="70" y2="47.8" stroke="#333"/>` labelled `14`.
*After:* `y1="113.1"` and `y1="51.7"` respectively, with the `8` label's `y="120.5"` moved to `y="116.1"` and the `14` label's `y="50.8"` to `y="54.7"`.
*Why:* Fitting the drawn polyline against `$F(d)=mv^2/2d+mg$` over its 100 points gives `$y=-10.2375\,F_{\rm kN}+195.002$` with a 0.15 px residual, so the curve itself calibrates the axis: the tick labelled 8 actually marked 7.57 kN (low by 5.4%) and the one labelled 14 marked 14.38 kN (high by 2.7%).

**REFERENCE — B5 (a law attributed to a module that does not contain it).**
*Before:* `The femoral neck (Module 16's bone continuum) fails when the impact stress exceeds its strength, which falls as the square of bone density (Module 2).` and `the femoral strength scales as $S=S_0(\rho/\rho_0)^2$ (Module 2).`
*After:* Repointed to Proposition 3.1 of Module 14, `module14.html#osteoporosis`: "If bone compressive strength follows $S=S_0(\rho/\rho_0)^{n_{\rm b}}$ with exponent $n_{\rm b}\approx2$…", which carries an adjacent proof.
*Why:* `grep -c 'rho_0\|\\rho/\\rho\|apparent density' module02.html` returns 0 — and $\rho$ in Module 2 is the radial coordinate of the polar second moment $J=\int_A\rho^2\,dA$, a different quantity entirely, so a reader following the pointer three times over finds nothing.



---

## 11. Unfinished business

- **Nothing is promoted.** All fifteen edits live in `edited/`. `index.html` and
  `README.md` still point at the originals, and the live course pages are exactly as they
  were. Promotion is one `mv edited/moduleNN.html moduleNN.html` per module. The
  deliverable stands without it — the reports and drafts are complete and reviewable — but
  no reader of the course sees any of this work until that decision is made.
- **One drift, open.** `edited/module03.html:858` states the hip resultant as "2.6 to
  2.8 W across 20° to 40°", where |R| at 40° is 2.87 W. Found by Module 8's agent in
  Module 3's already-committed work. Fix: verify the 2.87 independently, then widen the
  range or narrow the angle span.
- **The `edited/` publication question, unanswered.** Raised before the first commit, never
  resolved. The drafts are public at `az9713.github.io/biomechanics/edited/moduleNN.html`,
  unlinked. Undo is `.gitignore` plus `git rm -r --cached edited`, at the cost of the
  drafts no longer being backed up.
- **Structural notes left as notes.** Several modules' reports carry recommendations that
  are new content rather than edits — Module 3's suggested §6 sensitivity problem, Module
  17's twelve missing problem figures, Module 13's chair-less "rise" vignette, Module 4's
  scope rewrites. Each is logged in its report's §4 with a reason. An editor pass fixes
  what is there; it does not write what is missing.
- **Two `check_bodyprop` advisories in Module 10** are correct as drawn and were left: C9
  is a head alone because the problem is about the semicircular canals, and C3's "thin
  limb" measures against the vestibular head at r=14 rather than that body's own r=6.3.
- **`check_svg`'s "Answer"/"solution" summary-label advisory** is a course-wide convention
  question, not a module defect. Unresolved.

---

## 12. Where things stand

Fifteen modules edited, reported and gated. 1,214 logged edits. Every module's nine gates
sit at or above its pristine baseline, and seven modules came out ahead.

| | |
|---|---|
| Edited drafts | `edited/module03.html` … `edited/module17.html` |
| Reports and change logs | `editor-reports/module03.md` … `module17.md` |
| Live drafts (unlinked) | `https://az9713.github.io/biomechanics/edited/moduleNN.html` |
| Resume point | `HANDOFF.md` |
| Final commit | `a93a55c` |

**Next steps, as options rather than promises:**

1. Read a report or two — Module 12's and Module 14's are the ones where the audit found
   the most that the first pass had missed.
2. Fix the Module 3 drift.
3. Decide on promotion: all fifteen at once, or module by module as you sign each off.
4. Decide whether `edited/` stays public.
5. If promotion happens, re-run the nine gates on the promoted files in place before
   pushing — the gates were run against `edited/` paths, and `check_links` resolves
   cross-module hrefs relative to the file's own directory.

**One thing worth carrying into the next project.** The gates were built over three months
and they are good. They caught nothing in this pass that a reader would have noticed,
because they were built to catch broken pages and the pages were not broken. What they
missed — a figure drawing the reciprocal of its own formula, a caption naming an axis that
is not there, a proof assuming its conclusion, ten problems claiming code that does not
exist — is the whole of what an editor pass is for. Adding a tenth gate would not have
helped. Reading the file, running the code, and decoding the picture did.
