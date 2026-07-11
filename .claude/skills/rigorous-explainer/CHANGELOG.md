# Changelog — rigorous-explainer skill

## 2026-07-04 — Learnings from Modules 4–6 captured (4 documentation changes)

Four edits folded lessons from building Modules 4/5/6 of the biomechanics course into
the skill, so they are not re-discovered per module. All edits were made with the Edit
tool against existing files (exact-string anchors). No scripts changed in this batch —
these four are documentation; the two *scripts* they reference (`check_proofs.py`, and
the `checktex.py` control-char gate) were added earlier the same day (see "Related
enforcement" below).

Guiding principle: **the highest-frequency judgement rules must live in the
always-loaded `SKILL.md`** (references are loaded on demand and were being missed
mid-build); detailed how-to lives in `references/`; the two crisp mechanizable cases are
enforced by scripts in the hardening loop.

---

### Change 1 — Hoist two build rules into the always-loaded `SKILL.md`
**File:** `SKILL.md` (workflow steps 3 "Derive rigorously" and 4 "Visualize").
**Why:** the §6 proof gap happened because "uniform rigor across siblings" lived only in
`references/pedagogy-checklist.md`, which is loaded on demand and wasn't in context
during the build. Only `SKILL.md` is guaranteed loaded. (A sibling Pillar-4 statement of
the same rule was added at line 31 during the earlier §6 fix.)
**How implemented:** two Edit calls.
- Step 3, appended after the "validate…reproduce." sentence:
  > **Prose lives in the HTML, computation lives in the scripts.** Write the section's
  > prose and proofs *directly in the `.html`* … **Never author section prose inside a
  > Python raw string** … prose-in-code evades the aloud audit … **Uniform rigor across
  > siblings:** if one boxed result in a section gets a `.prop`+`.proof`, its peer boxed
  > results … must be proved the same way … `check_proofs.py` flags the crisp case …
  > the keyresult-vs-proof call is a judgement — eyeball each section's boxed results.
- Step 4, replacing the "one representative figure approved first … Remotion …" tail:
  > **When a figure exists to show effect X … verify the computation actually produces
  > X — print the punchline number — *before* building the figure around it** … **Match
  > the model to the figure's job:** if honest first-principles dynamics belongs to a
  > later lab, use a cleaner kinematic/prescribed-input decomposition … and *label it as
  > such* … the **splice-pipeline hazards** (viewBox collisions, marker asserts, portrait
  > `max-width`, figure renumbering, unbounded-curve arrows): `references/figures-and-animation.md`.

### Change 2 — New "Splice-pipeline hazards" section in `figures-and-animation.md`
**File:** `references/figures-and-animation.md` (new `## Splice-pipeline hazards
(learned the hard way — Modules 4–6)`, inserted after the "Reusable figure toolkit"
section, before "Get the geometry RIGHT"); plus a twin-axis clause added to the
"Labels must clear the curves" section.
**Why (incidents this session):** a viewBox-keyed re-splice clobbered §2's Fig. 5 with
§3's Fig. 6 (shared `0 0 482 285`); a forgotten `<!--FIG-->` marker; a portrait network
figure rendered ~1000 px tall; inserting the FBD figure renumbered the response grid
(Fig. 13→14) and broke a reference; Maxwell creep clipped flat read as bounded.
**How implemented:** one Edit adding the section (five bullets) + one Edit extending the
data-aware-labels bullet. The five hazards:
1. **Assert exactly one marker** — `assert s.count(marker)==1` in every splice script.
2. **Re-splice by unique `aria-label`, never by viewBox** (viewBox dims collide).
3. **`width="100%" style="max-width:300px"`** on portrait/schematic SVGs (`check_frame`
   won't catch on-page scale).
4. **Figure numbers shift on insert** — after any insert/delete, grep `Fig\. [0-9]`
   downstream and re-point.
5. **Don't clip an unbounded curve flat** — stop at the frame edge + `marker-end`
   arrow + "unbounded ↑"; an asymptote line is a claim, draw it only where it holds.
Twin-axis clause: a diagonal reference curve (Φ, `k(x)`) has no fixed empty side — place
labels in the band between it and the primary curve, or delete a redundant text label.

### Change 3 — New "Sim fidelity" bullet in `pedagogy-checklist.md` §4
**File:** `references/pedagogy-checklist.md` §4 (after the "Uniform rigor across
siblings" bullet, which was itself enriched).
**Why:** in §4 of Module 6 the first two catapult-sim formulations produced no
decoupling (amplification ≈ 1.0×); a figure nearly shipped around a non-effect. Also,
the sibling-rigor audit needed explicit *exemptions* so it doesn't over-flag.
**How implemented:** one Edit that (a) appended exemptions to the uniform-rigor bullet
(a definition, one-line substitution, cited standard like **Hertz contact**, or
empirical fit like **Hill's 1938 equation** is *stated, not proved*), and (b) added a new
bullet:
> **Sim fidelity: verify the effect before you draw it.** … print the punchline number
> … *before* building the figure … **Match the model to the figure's job** … use a
> cleaner kinematic/prescribed-input *decomposition* … label it as such … make
> **known-limit validation** routine (the SLS → Maxwell/Kelvin–Voigt; the MTU → the
> rigid tendon as k→∞).

### Change 4 — New §8 "Windows Python + Unicode" in `math-html-gotchas.md`
**File:** `references/math-html-gotchas.md` (new `## 8. Windows Python + Unicode: write
and print in UTF-8`, inserted after §7, before "Subresource Integrity").
**Why:** figure generators emit `σ ε τ Φ ≈ → ↑` constantly; on Windows the cp1252
default crashed `open(...,'w').write(...)` and `print(...)` twice during the build.
**How implemented:** one Edit adding the section:
- **Writing:** `open(path, "w", encoding="utf-8")` (and `encoding="utf-8"` to read).
- **Printing:** run with `PYTHONIOENCODING=utf-8 python gen.py`, or keep prints ASCII.
- Note: not a rendering bug — the HTML is fine once written; the script dies first.

---

### Related enforcement added earlier the same day (context, not part of these 4)
- `scripts/checktex.py` — now hard-fails on stray control chars (TAB/VT/FF/BS/BEL/CR),
  the fingerprint of `$…$`/backslash math mangled by a double-quoted shell. Paired with a
  new rule in `math-html-gotchas.md §7` ("never splice math through a `"…"`-quoted shell").
- `scripts/verify_dom.py` — added a **swallowed-prose** advisory (inline `$…$` that ate a
  sentence — the residual no-control-char case checktex can't see).
- `scripts/check_proofs.py` — **new**; flags a `.prop`/`.thm`/`.lem` with no adjacent
  `.proof` (advisory). Added to the hardening loop in `SKILL.md` and the project
  `CLAUDE.md`.
