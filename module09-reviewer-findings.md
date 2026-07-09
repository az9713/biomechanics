# The Fable 5 rigor-reviewer on Module 9 §0–§5 — findings, fixes, and an honest assessment

**What this is.** A section-by-section capture of everything the `rigor-reviewer`
agent flagged while Module 9 (Running and Jumping) was built through Section 5, how
each item was resolved, and a candid read on how much a **Fable 5** reviewer actually
bought. Written to let someone judge the value of the reviewer step without having to
trust a one-line "it helped."

## The setup (so the results are interpretable)

- **The reviewer.** `.claude/agents/rigor-reviewer.md`, `model: fable` — i.e. **the same
  model (Fable 5) that wrote the sections**. Read-only tools (`Read, Grep, Glob, Skill`);
  it cannot edit, run scripts, or execute code. It judges four things no script can:
  **rigor parity**, **read-aloud prose quality**, **computational-problem (K) depth**, and
  **self-containment** (every symbol/term defined at first use).
- **When it ran.** Only *after* the mechanical hardening loop was already green
  (`checktex / checklt / check_links / check_svg / verify_dom / check_overlap /
  check_frame / check_prose / check_proofs / check_code / check_probfig` all at 0). So
  every finding below is, by construction, something **the eleven scripts could not
  catch**.
- **Scope discipline.** Each dispatch was told to review exactly one section and to treat
  the not-yet-built sections as intentional stubs. It respected that in all six runs.

## Scoreboard

| § | Topic | Verdict | Findings | Category of the misses |
|---|-------|---------|----------|------------------------|
| 0 | Motivation (running is bouncing) | NEEDS-FIXES | 2 | 1 undefined term, 1 physics category-error |
| 1 | Gait notation + duty factor | NEEDS-FIXES | 2 | 1 figure/claim mismatch, 1 undefined term |
| 2 | SLIP model | NEEDS-FIXES | 1 | cross-section symbol collision (`v`) |
| 3 | Stance dynamics + GRF | **READY** | 0 | — (clean first pass) |
| 4 | Flight + walk→run transition | **READY** | 0 | — (clean first pass) |
| 5 | Impulse & momentum | NEEDS-FIXES | 2 (+1 optional) | symbol overload (`v_y`), circular argument |

Six reviews, **four needed fixes, two were clean**. **Eight** distinct findings, plus one
optional figure note and one "not-a-defect" observation. **Zero false positives** — every
flagged item was a real problem, and on the two clean sections it said so plainly instead
of inventing work.

---

## Section-by-section detail

### §0 — Motivation

**Finding 1 — undefined term (self-containment).** The sentence *"There is no double
support to smooth the ride"* used the gait term **double support** without ever defining
it in §0. Cold to any reader who skipped Module 8.
- **Fix:** → *"There is no double support (the brief overlap when both feet are on the
  ground) to smooth the ride."*

**Finding 2 — physics category-error (prose/precision).** The thesis sentence read
*"both are governed by **impulse acting over a distance or a time**."* But impulse is
strictly ∫F dt — a **time** integral. It is **force** that acts over a distance (→ work →
height) or over a time (→ impulse → velocity). Calling impulse "over a distance" is a
category slip, and this sentence is the hinge the whole back half of the module hangs on.
- **Fix:** → *"both are governed by **force acting over a distance or a time**."*
- **Why it matters:** §5–§8 depend on cleanly separating force-over-distance from
  force-over-time. Shipping the confusion in the topic sentence would have undercut four
  later sections. This is the single most valuable catch of the six reviews.

### §1 — Gait notation and the duty factor

**Finding 1 — figure/claim mismatch (self-containment).** Prose asserted *"Four events
punctuate one stance, and **Fig. 2 places them in time**,"* naming touchdown, midstance,
toe-off, and flight. But Fig. 2 labels **phases** (stance/flight bars), not events —
midstance, being interior to a stance, is not even a boundary and appears nowhere on it.
The figure could not deliver what the sentence promised.
- **Fix:** → *"Four events punctuate the cycle, and the table below defines each; Fig. 2
  shows the stance and flight phases they bound across the stride."* (The events live in
  the table; the figure carries the phases.)

**Finding 2 — undefined term (self-containment).** **swing** appeared only as a figure
label ("R swing"/"L swing") and by implication in the caption, but was never defined in
prose, unlike its sibling "stance phase."
- **Fix:** added at first use — *"the complementary **swing phase** is the interval when
  that foot is off the ground, advancing to its next contact."*

*Non-blocking note it also raised (and I deliberately skipped):* a second timeline row for
walking would make the flight-replaces-double-support contrast visual rather than told. It
correctly marked this **optional**, and §0's figure already carries the contrast.

### §2 — The spring-loaded inverted pendulum

The reviewer **independently re-derived all three propositions by hand** and confirmed
them correct: the polar equations of motion (spring sign, gravity projections), the energy
proof (it verified the "every term cancels" step is *literally* exact, not a hand-wave),
and the ballistic law. It also confirmed the locked design decision — `k_leg` framed as
effective whole-limb stiffness, not the Module 6 Achilles tendon — was honored.

**Finding — cross-section symbol collision (self-containment).** §1 defines `v` as the
**mean forward running speed** (`v = fL`). Prop 2.2 silently reused `v` for the
**instantaneous centre-of-mass speed** in the flight energy `½mv² + mgy`. A reader
carrying §1's `v` misreads the kinetic-energy term.
- **Fix:** rewrote the flight energy in components, `½m(ẋ² + ẏ²) + mgy`, with an explicit
  gloss: *"...where ẋ² + ẏ² is the squared instantaneous speed of the centre of mass (not
  the mean running speed v of section 1)."*
- **Why a script can't see it:** `checktex` balances delimiters; nothing parses that one
  glyph carries two incompatible meanings across a section boundary.

### §3 — Stance dynamics and the ground reaction force — **clean**

Verdict **READY, zero findings.** The reviewer independently confirmed
`F_z = k_leg(L₀−r)sinφ = m(g+ÿ)` (both equalities and their reconciliation), the peak-force
keyresult as a legitimate substitution into the proved proposition, and the single-vs-
double-hump argument. It specifically checked the **figure honesty** requirement — that the
computed running curve and the *representative* walking curve were labelled by provenance
so the schematic was not passed off as a SLIP prediction — and found it honest. It said so
without padding.

### §4 — Flight and the walk-to-run transition — **clean**

Verdict **READY, zero findings.** It re-derived the flight kinematics and the Froude
ceiling `F_z = mg(1−Fr)` (checking the centripetal direction and signs), verified
`√(gL₀) ≈ 3.13 m/s`, and — the point most worth an independent eye — confirmed the section
**honestly separates** the *kinematic* ceiling (Fr = 1, derived) from the *observed*
energetic transition (Fr ≈ 0.5, forwarded, not overclaimed). It also confirmed the §2 `v`
de-collision was carried through consistently.

### §5 — Impulse and momentum

The reviewer verified both propositions (the theorem from `F = dp/dt` + the fundamental
theorem of calculus; the symmetric-stance split) and confirmed the **numerical** claim
`183.2 = 116.1 + 67.1 N·s`.

**Finding 1 — symbol overload (self-containment).** §4 had fixed `v_y` as a **positive
constant** (`v_y > 0`, the takeoff speed). The Prop 5.2 proof then reused `v_y` as a
**velocity-vs-time function**, writing `v_y(0) = −v_y` and `v_y(t_c) = +v_y` — the same
glyph as both function and constant, and `v_y(0)` can even be misread as the product
`v_y·0 = 0`, which contradicts the intended `−v_y`.
- **Fix:** introduced a distinct name for the velocity function — *"Let v(t) be the
  vertical velocity ... the runner arrives at v(0) = −v_y and leaves at v(t_c) = +v_y, with
  v_y > 0 the takeoff speed"* — keeping `v_y` the positive constant.
- **Meta-point:** this is the **third** appearance of the exact same author blind spot
  (`v` in §2, `v_y` here) — a systematic tendency to overload velocity symbols that the
  reviewer caught every time. See "What this reveals" below.

**Finding 2 — circular argument (correctness/prose).** The horizontal-impulse prose read
*"at steady speed they are equal and opposite, so by (5.1) the net horizontal impulse is
zero and the forward speed is unchanged"* — which assumes equal areas to then re-derive the
steady speed that was the premise.
- **Fix:** ran the logic one direction — *"Because the forward speed holds steady from step
  to step, (5.1) forces the net horizontal impulse to vanish, so the braking and propulsive
  lobes must have equal area."*

**Finding 3 — figure parameterization note (optional, honesty).** Fig. 6's symmetric
stance (peak ≈ 2.5 BW, `v_y ≈ 0.48 m/s`) is a *different* illustrative run than §3/§4
(≈ 2.6 BW, `v_y ≈ 0.9 m/s`). Legitimate and honestly captioned, but a reader tracking "one
runner" could be momentarily confused.
- **Fix (taken, though optional):** added a caption clause — *"a steady-state
  parameterization chosen so the endpoints mirror exactly, not the same run as Figs. 4–5."*

**Not-a-defect observation it correctly declined to fix:** the module labels vertical
*force* `F_z` but vertical *position/velocity* `y`/`v_y`; that convention was set in
already-approved §3, so it flagged it for awareness rather than treating it as a §5 fault.
Good judgment about scope.

---

## What the reviewer bought

**1. It caught a real physics error in the module's thesis sentence.** The §0
impulse-vs-force category slip is the kind of thing that passes every syntactic check
(valid TeX, renders fine, reads smoothly) and then quietly undermines four downstream
sections at exactly the level — MIT-PhD — where it is least forgivable. No script in the
loop can see it.

**2. It is a consistency instrument across section boundaries.** Five of the eight findings
are **self-containment** issues: `v`/`v_y` collisions, undefined `swing`/`double support`,
a figure claiming to show events it only bounds. These are precisely the errors that
accumulate silently in a long, incrementally-built document, because the author has the
whole thing in working memory and stops noticing what a fresh reader cannot infer. A
read-only agent with a clean context is structurally better positioned to catch them than
the author is.

**3. Its clean verdicts are informative, not lazy.** §3 and §4 came back **READY with zero
findings**, each with an itemized account of what was checked (derivations re-done by hand,
figure provenance audited, honesty of the Fr = 1 vs Fr ≈ 0.5 distinction confirmed). A
reviewer that flagged something on every section would be noise; this one distinguishes
"clean" from "not," which is the whole point.

**4. Independent re-derivation is real assurance.** On every section it re-did the algebra
from scratch — the polar EOM, the energy cancellation, the impulse split `183.2 = 116.1 +
67.1`, the Froude centripetal balance — and found the math correct. It caught **zero**
mathematical errors, but that is a *result*, not a failure: it means the derivations are
independently corroborated, which is worth having on record for a rigor course.

## What it did **not** buy — the honest "lack of"

**1. It is not an independent-*model* check.** The reviewer is Fable 5, the same model that
wrote the sections. It catches the author's *local* blind spots (things you miss because
you're too close to the text), but **shared** blind spots — an error both the writer and
the reviewer's training would wave through — can survive. A genuinely independent audit
would run a *different* model as reviewer. The one-line change (`model: fable` → another
tier) is noted as an open option.

**2. Every finding was low-to-moderate severity.** Nothing it caught was a show-stopper or
a deep conceptual error. The value was in **precision and consistency**, not in rescuing a
broken derivation — partly because the derivations were sound, and partly (see #1) because
a same-model reviewer may not reach errors of the author's own conceptual depth.

**3. One of its four dimensions was never exercised.** `K-DEPTH` — whether computational
problems demand real simulation/optimization rather than plug-in arithmetic — has had
**nothing to test**, because §0–§5 contain no problem set (that is §11). The reviewer's
single most course-specific check is, so far, **unvalidated on this module**. There is a
standing carry-forward to inject a deliberately shallow K problem and confirm the reviewer
flags `K-DEPTH: fail` before trusting it on the real problem set.

**4. It needed a well-scoped prompt to be sharp.** Each dispatch spelled out exactly what
to verify (the specific equations, the honesty requirement, the symbol list). Given that,
it was precise; a vaguer "review this" would likely have produced vaguer output. The
quality of the review tracked the quality of the tasking.

## What the findings reveal about the *author* (the real tell)

The most telling pattern is not in any single catch but across them: **five of eight
findings are the author under-specifying or overloading symbols and terms** — `v`, `v_y`,
`swing`, `double support`. The velocity-symbol overload recurred **three times** (§2, and
again as `v_y` in §5) despite the §2 fix. That is a stable, systematic authoring weakness,
and it is exactly the class of defect a fresh-context reader catches reliably and the
in-flow author does not. The reviewer's value here is less "finds bugs" and more
"**enforces the discipline the author keeps sliding off of**." For a self-contained rigor
course whose first pillar is *define every symbol at first use*, that enforcement is the
main event.

## Bottom line

Across §0–§5 the Fable 5 reviewer flagged **eight real issues, zero false positives**,
including one genuine physics error in the module's thesis and a recurring symbol-overload
blind spot the author could not shake — all of them invisible to the eleven mechanical
checks, all fixed before the sections went live. It is a strong **consistency-and-precision
gate** and a real second set of eyes on cross-section coherence.

Its two honest limits: it is **not model-independent** (shared blind spots can survive, and
a different-model reviewer would be a stronger audit), and its **K-depth dimension is still
untested** on this module. Net: clearly worth running as the gate between "scripts pass" and
"human review" — with the asterisk that the biggest gains would come from pointing a
*stronger or different* model at the same job for the parts that matter most.

---
*Findings drawn verbatim from the six `rigor-reviewer` runs during the Module 9 §0–§5
build. Sections live at https://az9713.github.io/biomechanics/module09.html.*
