# Development journal — fixing the Module 2 femur figure (2026-07-28)

A blow-by-blow account of one session: correcting a single anatomical drawing in
an HTML biomechanics course. The change itself is tiny — a few dozen numbers in
one line of SVG. The point of writing it down is to show *how* the work actually
went: how I oriented, how I diagnosed, the one real dead-end I hit and how I got
out of it, and what verified "done" instead of just "looks done."

Plain-language throughout, but nothing is dumbed down — every coordinate, angle,
and file reference that mattered is here.

---

## 1. What the task was

The course is a set of self-contained HTML lessons on the mechanics of the human
skeleton. Each lesson leans heavily on hand-drawn vector figures (SVG). A previous
"realism pass" had accidentally broken about 90 of these figures across the course,
and prior sessions had fixed 89 of them. **One was left**: the opening figure of
Module 2, a teaching diagram of the thigh bone (femur).

The defect: the drawing showed the **neck-shaft angle** at roughly **146°** when
the caption stated **125°** — twice. In plain terms: the femur is not a straight
tube. Near the hip it has a "neck" that juts off the main shaft at an angle, with
the ball of the hip joint on the end. In a healthy adult that angle is about 125°.
The drawing had it splayed out near 146°, which is a real clinical deformity called
*coxa valga*. So the picture contradicted its own label and taught the wrong shape.

Why this one was saved for last: every other broken figure was a stick-figure body
built from reusable "capsule + sphere" parts, so there was a proven recipe. This
femur was **one hand-authored closed outline** — a single continuous loop of arcs
and lines with no reusable parts. Fixing it meant re-deriving that outline's
geometry from scratch, which only works if you can *see* each attempt rendered.
The prior session's screenshots had started timing out, so it was deferred to a
fresh session where rendering worked again.

---

## 2. Orientation: reading the map before touching anything

I did **not** start by opening the figure. I started by reading the two files the
project uses as its memory between sessions:

- `HANDOFF.md` — the live "what to do next." It named the exact task, gave the
  suspected fix (move the head to about (276, 41)), listed the safety caveats, and
  told me to locate the figure *by its caption text, not by its number*.
- `ANATOMY_AUDIT.md` — the full defect register. Its Module 2 entry confirmed the
  numbers: "drawn neck-shaft angle **146°**, not the 125° stated twice → coxa
  valga; move head centre to ~(276,41)."

**Why this matters:** these files encode hard-won warnings. One example that saved
me real time: *"locate every figure by caption, not by number."* The audit was
built from contact-sheet screenshots whose figure numbering does **not** match the
order figures appear in the HTML. If I'd trusted "figure 1 = first figure in the
file," I could have edited the wrong drawing and silently corrupted a correct one.

So my first search was for the caption, not the position:

```
grep -in "femur|fig 1|figure 1" module02.html
```

That pointed me at line 96, an SVG whose `aria-label` began *"Left: NIH BioArt
upper leg bones… Right: lateral femur with neck-shaft angle about 125 degrees."*
The label already *claimed* 125°, which was exactly the contradiction I was hunting.

---

## 3. Finding the actual bone in the markup

The figure has two halves. The left is licensed public-domain bone art (a big block
of machine-generated path data — not mine to touch). The right is the hand-drawn
teaching outline. I read the figure top-to-bottom and found the teaching femur at
**line 156**, a single `<g>` group containing:

- one `<path>` — the bone outline (a closed loop: a head arc, neck lines, shaft
  lines, a condyle arc at the bottom);
- a small highlight circle (a fake glint of light on the ball);
- two dashed `<line>`s — a guideline drawn *through* the neck and *down* the shaft
  to show the angle;
- five text labels: head, GT (greater trochanter), neck-shaft ~125°, shaft, condyles.

The raw path started:

```
M277.6,37.0 A12.0,12.0 0 1 1 287.2,40.6 L296.9,50.7 L299.7,240.9 ...
```

A note on coordinates: SVG's y-axis points **down**, so "up the body" means
*smaller* y. I checked one structural fact before trusting any numbers — the
teaching `<g>` sits directly in the figure with **no transform** on it (the
public-domain art next to it *is* scaled and shifted inside its own group). That
mattered later: it meant a preview of the outline *in isolation* would render at
the exact same geometry as it does on the page. No hidden scaling to account for.

---

## 4. Diagnosis: proving the defect with arithmetic, not eyeballs

The drawing carried its own evidence. Those two dashed guideline segments trace the
*intended* axes: head-center → neck/shaft junction → down the shaft. Their
endpoints were right there in the markup:

- head center (280, 37)
- junction (289.6, 50.7)
- shaft point (291.7, 240.9)

The neck-shaft angle is just the angle between two vectors meeting at the junction:
one pointing back up the neck to the head, one pointing down the shaft. I computed
it rather than trusting my eye:

```python
import math
def ang(head, junc, dist):
    vh = (head[0]-junc[0], head[1]-junc[1])
    vs = (dist[0]-junc[0], dist[1]-junc[1])
    dot = vh[0]*vs[0] + vh[1]*vs[1]
    return math.degrees(math.acos(dot / (math.hypot(*vh)*math.hypot(*vs))))
# -> 145.6
```

**145.6°.** That confirmed the audit exactly and, importantly, told me the *dashed
guideline itself* was wrong, not just the outline. Whatever fix I made had to move
three things in agreement: the outline, the guideline, and (visually) the label.

This is a recurring theme in the project's conventions and in how I worked:
**derive geometry, don't eyeball it.** A picture can look "about right" and still
be 20° off. One `acos` settles it.

---

## 5. Designing the corrected shape

I made a deliberate choice here: **rebuild the outline from clean parametric
geometry** rather than nudge the existing hand-tuned vertices one at a time.
Surgically editing a closed outline is fragile — move one point and the arc it
feeds no longer closes cleanly. Regenerating the whole loop from a few named
anchors is more reliable and, crucially, reproducible.

The anatomy I was drawing, stated plainly:

- a **shaft** — a near-vertical tube;
- at its top, a **greater trochanter** — a bump on the *outer* (lateral) side;
- a **neck** projecting up-and-inward (medial) from the top of the shaft, at 125°
  to the shaft;
- a **head** — the ball — on the end of the neck;
- **condyles** — the widened, rounded bottom at the knee.

I set the design anchors and let a script compute the rest. The key trick for the
angle: if the shaft points straight down, then a 125° neck-shaft angle means the
neck points **55° away from straight up** (because 180 − 125 = 55), tilted toward
the midline. So the neck's direction vector is:

```python
theta = radians(180 - 125)          # 55°
n = (-sin(theta), -cos(theta))      # up and to the left (medial-superior)
```

Placing the head center at (276, 41) and stepping 17 units back along that
direction landed the junction at **(289.93, 50.75)** — almost exactly the original
junction (289.6, 50.7). A sanity `acos` on the result read **125.0°**. Good: the
head target from the audit and a clean 125° axis are mutually consistent.

The outline itself is a single closed loop. I walked it as a silhouette: the
exposed arc of the ball, down one edge of the neck, into the medial side of the
shaft, down to the condyles, across the condyle arc, up the far (lateral) side of
the shaft, over the greater-trochanter bump, and back along the top edge of the
neck to close. The two neck edges are just the neck axis offset sideways by a
half-width (6.6 units) in each direction; where those offset lines cross the head
circle is computed, not guessed.

---

## 6. The one real dead-end — and how I climbed out

I never edited the live file blind. I built a **standalone preview** (the outline
plus the three shared gradient/shadow definitions it references) and rendered it to
a PNG with the project's screenshot tool. The first render came out **wrong** —
badly. Instead of a rounded ball on a neck, I got a thin crescent/spiral with a gap
in it, and the glint-highlight floating in empty space off to the side.

Two separate bugs, both instructive:

**Bug 1 — wrong circle intersection.** A neck edge is a straight line; it crosses
the head circle at *two* points (near side and far side). For the ball and neck to
merge into one smooth blob, the neck has to stop at the point *nearest* the shaft.
My first script took the *far* intersection, so the neck line speared straight
through the ball and out the other side. Fix: take the near root of the
quadratic (`min` of the two solutions, not `max`).

**Bug 2 — wrong arc sweep direction.** SVG arcs have two flags — "large-arc" (take
the long way or the short way) and "sweep" (curve clockwise or counter-clockwise).
The ball's *exposed* surface is the big ~290° sweep on the side away from the neck.
I had large-arc right but the sweep flag backwards, so the arc bulged toward the
neck instead of away from it — that's the crescent. Fix: flip the sweep flag from
`1` to `0`.

There was also a small third thing: the highlight circle was still sitting at the
*old* head position (280, 37) while the head had moved to (276, 41), so it floated
off the ball. I moved it to (272, 37) — upper-left of the new center, where a light
glint belongs.

I flipped the flag, moved the highlight, re-rendered — and now it read as a proper
proximal femur: round head up-and-in, neck angling down at 125°, trochanter bump on
the outside, shaft dropping straight to the condyles.

**The lesson in this:** the arithmetic for the *angle* was right the whole time
(125.0° checked out before I drew anything). What broke was the *drawing grammar* —
which of two arcs, which direction. No amount of staring at coordinates would have
caught it; a two-second render did. **The compute step and the render step catch
different classes of error, and you need both.** Numbers verify the physics;
pixels verify the picture.

---

## 7. Applying the fix to the real file

Only after the isolated preview looked right did I touch `module02.html`. One exact
string replacement swapped the old `<g>` (outline + highlight + guideline + labels)
for the corrected one. In the same edit I:

- rewrote the `<path>` with the new outline;
- moved the highlight circle to (272, 37);
- redrew both dashed guideline segments onto the true 125° axis;
- **separated two labels that had been printing on top of each other** — the audit
  had flagged "GT / angle labels overprint illegibly" as a minor issue, and since I
  was already rewriting this block, it was free to fix. "GT" went up by the
  trochanter apex; "neck-shaft ~125°" moved to clear space to the right.

---

## 8. Verification: what actually made it "done"

The project runs **nine hard gates** — automated checks that must all come back
clean after any figure edit. They split into two speeds:

- **Six fast text/structure checks** (TeX delimiter balance, raw `<`/`>` inside
  math, broken links, SVG structure, Python-block style, DOM math errors). All
  passed — the only flags were pre-existing advisories on *other* figures, nothing
  I'd touched.
- **Three slow checks that load the page in a real headless browser** (label-over-
  curve overlap, content clipped past the frame edge, and a body-proportion sanity
  check). These are slow enough that running all nine together **hit the 2-minute
  command timeout.** I split them off and ran them separately with a longer budget.
  Results: **0 label overlaps**, no hard clipping (only advisory "you have some
  wasted margin" suggestions), and the body-proportion advisories were on unrelated
  bone diagrams, not fig1.

Then — and this is the step the gates *cannot* replace — I **rendered the figure in
its real page context** and looked at it. The gates check syntax, proportion,
overlap, and clipping; they do **not** know a knee is bent backwards or a bone neck
is at the wrong angle. That blind spot is precisely how the original 90-figure
regression slipped through with every gate green. So the human-eye render is
mandatory, not optional.

To render it in context I extracted the whole figure and injected the three shared
graphic definitions it depends on (they live elsewhere in the file, but SVG IDs are
page-global so any figure can borrow them). The result showed the corrected
teaching femur sitting beside the public-domain bone art — same head → neck →
trochanter → shaft topology, angle visibly ~125° and no longer splayed.

---

## 9. Closing out: commit, handoff, memory

Per the project's standing rules, I committed and pushed **without waiting to be
asked**, one commit per figure, using the project's designated public-repo identity
and *not* the private email that must never re-enter this public history.

Then I updated the three places that carry state forward:

1. **`HANDOFF.md`** — rewrote the "next task" from "fix m02 fig1" to "anatomy phase
   complete; only optional cosmetics remain," so a fresh session starts in the right
   place.
2. **The auto-memory index and its detail file** — flipped the tracked note on this
   regression from *"audited, fix deferred"* to *"fully fixed, all 90 done."*
3. Committed the handoff change too.

The working tree ended clean, everything pushed.

---

## 10. How this generalizes — the meta-learnings

Stripped of the specifics, here is the shape of how this kind of task gets done
well. These are the transferable bits.

**Read the memory before the code.** The two handoff files turned a potentially
hour-long "which figure, is it even broken, what's the target" hunt into a
ten-minute targeted fix. They also carried a landmine warning (numbering ≠ order)
that would otherwise have bitten me. Institutional memory beats re-derivation.

**Locate by meaning, not by index.** "The first figure" and "the figure whose
caption says X" are different things, and only the second is safe when your
reference material was built from a different ordering.

**Diagnose with arithmetic; the drawing often carries its own proof.** The bad
angle was recoverable straight from the guideline coordinates via one `acos`. I
confirmed the defect (145.6°) and later confirmed the fix (125.0°) the same way.
Eyeballing "that looks like 125-ish" is exactly how a 20° error survives.

**Regenerate from anchors instead of nudging vertices.** For anything built as a
continuous outline, re-deriving the whole shape from a few named points is more
robust than hand-editing points, because it keeps every dependent curve consistent
by construction — and it's reproducible if you have to redo it.

**Two different verification tools catch two different error classes.** Compute
checks the invariant you care about (here, the 125° angle — right from the start).
Render checks the *rendering* — which arc, which sweep direction, is the highlight
on the ball. My angle math was correct while my picture was a broken crescent. If I
had trusted either check alone, I'd have shipped a wrong figure or wasted time
second-guessing correct numbers. Run both.

**Never edit the live artifact blind.** Every attempt went to a throwaway preview
first. The dead-end (crescent + floating highlight) happened in a scratch file the
user never saw, was fixed in two more render cycles, and only the *working* version
touched `module02.html`.

**Let the automated gates do what they're good at, and don't ask them for what they
can't do.** Nine checks caught nothing here because there was nothing syntactic to
catch — but they're the safety net that lets you move fast on the mechanical stuff.
The thing they *structurally cannot* see (is the anatomy actually right?) is exactly
the thing that needs a human-eye render every single time. Knowing that boundary is
half the discipline.

**Leave the campsite better than you found it.** The overlapping-labels fix wasn't
strictly required, but the block was already being rewritten, so folding in a known
minor defect cost nothing. And the session ends by updating handoff + memory so the
*next* session inherits an accurate map — the same thing that made *this* session
fast.

---

*Net change on disk: a few dozen numbers in one line of SVG. Net work: read the
map, prove the defect, design the shape, render-debug two drawing bugs, verify with
nine gates plus an eye, and hand the state forward. The small diff is the tip; the
verification and the memory-keeping are the iceberg.*
