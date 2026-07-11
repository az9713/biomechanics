# Pedagogy checklist — the pillars

A rigorous explainer is judged on whether a reader can follow it top to bottom
without jumping around. Enforce these:

## 1. Define every symbol AND term before first use, self-contained
- The first time a symbol appears, name it inline: "the bending stiffness $B$",
  "the curvature $\kappa=1/R$". Same for jargon: "*nucleation* (creating it from
  the flat state)".
- "Self-contained" means the definition is *here*, not only "see §7". A forward
  link is fine **in addition**, never **instead**.
- Audit: read the doc top-down; the first occurrence of any symbol/term must
  carry its meaning. Things introduced only in a later section are a bug.
- **Audit symbol collisions across the whole document, not per section.** Keep a
  running notation table as you write (it becomes the Appendix); flag any symbol
  that carries two meanings across sections — we hit `W`, `g`, `β`, `k` — and
  rename or explicitly disambiguate it at each point of use.

## 2. One building spine — each section needs the previous
- Order sections so section N uses results from N−1. Add a one-line **bridge** at
  each section start ("With the equation of §2 in hand, we now solve it …").
- If a block is rigorous but off the main path (an exact/alternative treatment),
  **demote it to an Appendix** rather than interrupting the spine.
- Introduce a quantity where it is *earned* (e.g. a length scale right where the
  competition that produces it appears), not in an early standalone dump.
- **Exercise the whole governing law you introduce.** If you state a law with two
  halves (e.g. force balance *and* moment balance), use both — don't introduce
  `∑F=0` and then only ever apply `∑M=0`, leaving the joint-reaction / normal-force
  half computed nowhere. An introduced-but-unused equation is a promise unkept.
- **If the spine is a model, end it with "captures / misses."** Give a section to
  what the idealization gets right and what it omits, mapping each omission to
  where it is later repaid (a following section, an Appendix, a sister document).
  This is part of the rigor, not a disclaimer.

## 3. Motivation first
- Lead with a concrete, everyday hook (a "Section 0") that shows where the
  problem comes from and previews what each later section delivers. Then take the
  idealized object as given and analyze it.

## 4. Rigorous, step-by-step derivations and proofs
- Use boxed environments: `.def` (definition), `.thm` (theorem), `.lem` (lemma),
  `.prop` (proposition); proofs in `.proof` (auto-prefixed "Proof.", `∎` via `.qed`).
- Show **every** step. Box the headline result with `$$\boxed{…}$$`.
- Give each proof a setup figure (see `figures-and-animation.md`).
- **The figure and the derivation must agree — each audits the other.** A scaling
  exponent or symbol placed on a plot, then *derived* in the proof, catches a wrong
  label the eye would pass (a `p₀∝R^{−1/3}` plot was corrected to `R^{−2/3}` only
  when the derivation was written out). Build both; let them cross-check. **This
  extends to animations: a caption's claim must match the animation's actual
  keyframes** — don't write "the bar collapses to zero" over a `values=…` list that
  stops at 75°. Read the keyframes, not your intention.
- **Quantify the punchline.** Every quantitative claim in prose — *especially the
  motivational climax* — must be backed by a shown computation or an explicit
  forward-reference, never left as a bare assertion ("the spinal force reaches
  several thousand newtons" with no calculation is a gap, not a flourish). If you
  can name a number, derive it or cite where it is derived.
- **Uniform rigor across siblings.** Don't leave an *asserted* proposition sitting
  beside fully-proved neighbours. If Theorem 3.2 is derived step by step, the
  Proposition 3.3 next to it should be too (or be demoted) — mismatched rigor reads
  as "the author ran out of steam here." Every boxed result earns its box.
  `check_proofs.py` flags a `.prop`/`.thm`/`.lem` with no adjacent `.proof`; the
  subtler "a boxed `.keyresult` law left with only an inline derivation beside a proved
  peer law" is a judgement call it can't see — read each section's boxed results and
  confirm peers of equal weight are proved alike. (A *definition*, a one-line
  substitution, a cited standard result, or an empirical fit legitimately needs no
  proof — Hertz contact and Hill's 1938 equation are *stated*, not proved.)
- **Sim fidelity: verify the effect before you draw it.** When a figure exists to
  *show* something (a decoupling, a spike, a power amplification, a crossover), print
  the punchline number from the computation and confirm it actually appears *before*
  building the figure around it — a "catapult" figure nearly shipped showing an
  amplification of ≈ 1.0× (no effect) because the first two model formulations didn't
  produce the decoupling. **Match the model to the figure's job:** if honest
  first-principles dynamics is the domain of a later lab, use a cleaner
  kinematic/prescribed-input *decomposition* for the earlier illustration and label it
  as such ("derived from the constraint and measured signals, as ultrasound confirms")
  — never dress a half-working dynamic sim as a first-principles prediction. And make
  **known-limit validation** routine: a refined model should reproduce the coarse one
  in the appropriate limit (the SLS → Maxwell/Kelvin–Voigt; the series-elastic MTU →
  the rigid tendon as k→∞), and that limit is worth stating as a proved proposition.

## 5. Section cross-references are clickable
- Put `id`s on every heading: `<h2 id="setup">1. …</h2>`. Reference as
  `<a class="secref" href="#setup">§1</a>`.
- Don't hand-maintain these: run `scripts/autolink_sections.py FILE.html` — it
  derives the number→id map from the headings and wraps every `§N` / `§N.M` /
  range. Re-run after edits; it skips already-linked refs.
- **A forward-reference is a promise.** What the document already claims about a
  later section binds you. If working notes or a plan conflict with what the text
  has already told the reader, the **text wins** — reconcile before building.

## 6. Visual rhythm — no walls of words
A rigorous explainer is also a *readable* one. Dense prose is where readers
drop off, so enforce a visual cadence as strictly as the math.

**No word limit.** This pillar bans *walls* of words, not words. Completeness and
rigor come first — never shorten, simplify, or drop content to satisfy it. The fix
for a wall is always to *interleave a visual or split the paragraph*, never to cut
the explanation.

- **The 10-line rule.** No paragraph runs longer than ~10 rendered lines. Split
  it — one idea per paragraph. Long enumerations become `<ul>`/`<ol>`, not
  comma-runs buried in a sentence.
- **A visual every screenful.** No text-only stretch taller than ~1 screen.
  Between figures, break the page with a table, chart, list, definition/`.thm`
  box, or a boxed result.
- **Pick the lightest aid that carries the point:**
  | Need | Use |
  |---|---|
  | Compare options / list parameters | table |
  | Quantitative trend or relationship | chart (compute real data, don't sketch) |
  | Structure, anatomy, geometry | labeled SVG diagram |
  | Something that happens over time / a process | SMIL animation |
  | The headline equation or fact | `$$\boxed{…}$$` / `.keyresult` |
- **Show, don't tell.** If a sentence describes a spatial or temporal
  relationship, draw it alongside the prose (add the figure, keep the words).
- **Number every figure, and reference it by number.** Each `<figure>` gets an
  auto-numbered caption ("Fig. N.", via the template's CSS counter) so prose and
  problems can point to it — which means *every* figure needs a `<figcaption>`, and
  the text says "Fig. 3", never "the figure below". SVG-text labels use Unicode
  subscripts, or a `<tspan baseline-shift="sub">` for glyphs Unicode lacks (capital
  letters like $r_L$). Details in `figures-and-animation.md`.
- **A dense table is not self-explanatory.** Pair a reference table with per-row
  prose; when the mapping is conceptual (idealization → fix, symbol → picture),
  add a *visual index* (e.g. a before/after grid) instead of leaning on the table
  alone. A table compresses; prose explains; a picture locates.
- **Animations must degrade gracefully.** A SMIL animation is an *enrichment*, never
  the only carrier of a point — the static frame beside it must already teach. The
  template freezes SMIL under `@media (prefers-reduced-motion: reduce)`; keep that,
  so a reader who suppresses motion (vestibular safety) still gets the figure.
- **Audit.** Scroll the *rendered* page top to bottom. Any screen that is wall-
  to-wall text is a defect — add a visual or split the prose before shipping.

### Sentence-level prose craft (structural rhythm is not enough)
Splitting paragraphs and adding visuals fixes *walls*; it does nothing for clumsy
*sentences*. A rigorous explainer is judged sentence by sentence too. These faults
recur — each makes prose read as unfinished, or as *non-native*, even when it is
grammatically correct:

- **One metaphor per idea; the next sentence must advance, not restate.** Two
  images of the same thing back to back (e.g. "a cable under tension," then "a rope
  you can tension on demand") make the second sentence echo the first instead of
  adding anything. State the picture once, then move forward. (A motif you *reuse
  later for payoff* — "a cable does none of these things" after the list — is
  different and good; the fault is immediate, redundant repetition.)
- **Don't echo a word across adjacent clauses — especially as a different part of
  speech.** "under *tension* … you can *tension*" (noun, then verb) reads as a
  stumble. Vary the word or cut the clause.
- **No tautological copula (`X is X`).** "Summation is summation in $a$", "a force
  is a force" — an *X-is-X* clause asserts nothing. Write the actual content:
  "the summation lives in $a$, not in the calcium."
- **No invented or verb-stacked idioms.** "worth watching *happen*", "easier to
  picture *happen*", "allows *to* compute" are seams a native reader trips on. Use
  the real idiom — "worth watching", "easier to follow in motion", "lets you
  compute". *If you are not certain a phrase is standard English, replace it with
  plain words.* This is the highest-frequency non-native tell.
- **Recast a stiff `the <noun> of which` relative when a plain version is shorter.**
  "one ODE, the miniature of which we have been integrating" → "the same ODE we have
  been integrating in miniature."
- **Every referent must be on the page.** Openers that borrow their antecedent from
  the previous paragraph — "The moment you ask" (ask *what?*), "This shows",
  "That's why" — leave the sentence leaning on context it doesn't restate. Name it:
  "Ask these four questions, and …"; "This *cancellation* shows …".
- **Audit — and audit generator-script prose too.** Read each paragraph as if aloud.
  **Prose you authored inside a generator (raw strings in a `build_secN.py`, a
  figcaption emitted from Python) is still prose** — the reader can't tell it came
  from code, and it is exactly where the aloud reflex fails to fire. A doubled
  metaphor, an *X-is-X* tautology, an invented idiom, a word repeated across clauses,
  or a "this/that/it" with no visible referent is a defect — fix it before shipping,
  the same way you fix a wall of text. `scripts/check_prose.py` greps the
  mechanically-detectable subset (tautological copula, verb-stacked idiom, doubled
  function word, stiff "of which") as an **advisory** backstop; it cannot see most
  awkwardness, so the aloud pass is still the real check.

## 7. Validate against an independent check
- Where a result can be checked, check it: an empirical/measured value, or a known
  **limiting case** the formula must reproduce (a one-element sanity check, a
  symmetric special case, a dimensional limit). A derivation pinned to an outside
  number is *evidence*; one that is only internally consistent is a story.
- **Compute even the "obvious" cases.** Run the model rather than asserting the
  result — the cases you were sure of are where the instructive surprises hide.
- **Where a measured literature value exists, cite it and show the model lands in
  range.** "Correct order of magnitude" is a claim, not a check, until it sits next
  to a real number with a source (measured moment arm, peak stress, telemetry). And
  compare *like with like* — validate a static prediction against a static/quiet
  measurement, a dynamic one against gait/telemetry; matching a static model to a
  walking number is a coincidence, not a validation.

## 8. Diagnostics and problem sets
- **Label what each problem probes** — the concept it tests and the section it
  draws on. The labels double as a *coverage map*: they expose gaps and
  duplication across the set at a glance.
- **Vary the kind, not just the difficulty.** Span *conceptual* (reason),
  *derivational* (prove / extend), and *computational* (edit-and-run) — each tests
  a skill the others miss.
- **Computational problems must build understanding, not test arithmetic — scale
  them to the audience.** A "substitute the given numbers into the boxed formula"
  problem reveals nothing the derivation didn't already show; for any technical
  reader (and emphatically for an expert one), it is busywork. A real computational
  problem requires one of: **numerical integration** (run the ODE, simulate the
  train), **optimization** (solve the argmax / the constrained share-out, find an
  optimal angle or rate), an **inverse problem** (recover the input or a parameter
  from the output — deconvolve, fit), a **sensitivity sweep** (how does the optimum
  move as a parameter changes?), or a **regime comparison** (two cost functions, two
  energetic pathways). The test for each: *does solving it surface science the reader
  could not read straight off the boxed result?* If not, deepen it or cut it. Know
  the audience's level and pitch to it — never water down for an expert reader.
- Put answers behind a reveal (`<details>`; MathJax still typesets hidden content),
  and **verify any computed answer** by running it — quote real numbers, never
  invented ones. Use **one** disclosure label throughout (don't mix "Answer" on
  diagnostics with "Solution" on problems unless the distinction is deliberate and
  stated).
- **Problems must span the whole spine, and every problem carries a solution.** If
  the computational set only edits the §7 lab, §§4–6 get no compute problem — spread
  them across the sections that hold the module's key numbers. Three unanswered
  problems is a thin set for a module that derived a dozen results: give each
  problem *and* each diagnostic a worked, runnable solution.
- **For a large set (10+), give it navigation.** A sub-nav
  (`#conceptual/#derivational/#computational`) plus per-group "↑ contents" links
  keeps 20–30 collapsibles usable (template ships a skeleton).

## Restructuring safely (reorder / renumber)
Reordering a numbered document means sections, equation tags, the TOC, and every
cross-reference must stay consistent. Do it as a scripted **placeholder two-pass
remap**, never a chain of naive replaces (which double-map, e.g. 6→4 then 4→2):
1. Build the old→new maps (sections, `(eq.tags)`, `\tag{…}`).
2. **Pass 1:** replace every OLD token with a unique placeholder (`@E0@`, `@E1@`…).
3. **Pass 2:** replace placeholders with their NEW values.
4. Rebuild the TOC from the new headings; re-run `autolink_sections.py` so the
   visible `§N` text matches the new numbers.
5. Re-run all checkers (the renumber must not break delimiter balance or links).
After any restructure, equation/theorem labels may fall out of source order; renumber them too, or accept and note it.

## Always, after every edit pass
Run the hardening loop (see SKILL.md step 6). Cheap, and it catches the silent
failures in `math-html-gotchas.md` immediately rather than three edits later.
