# Feasibility assessment: `/rigorous-explainer` on all 17 modules

**Author:** Grok 4.5 high (xAI)  
**Date:** 2026-07-10  
**Status:** Assessment only — skill not run; no modules modified.  
**Sources:** `prompt.txt`, `HANDOFF.md`, `audit-modules.md`, `skill-improvements-from-audit.md`, `rigorous-explainer` SKILL.md + scripts, structural inventory of `module01.html`–`module17.html`.

**Verdict:** Feasible, but **not as a single greenfield run**. All 17 modules already exist and are live. The real work is **raising uneven modules to the *current* skill bar**, and closing known content gaps against `prompt.txt` — not “build the course from zero.”

---

## 1. What “run rigorous-explainer on all 17” actually means

| Interpretation | Feasible? | Effort order |
|---|---|---|
| **A. Greenfield rebuild** of every module from `prompt.txt` + skill | Yes, technically | Very large (months of agent time) — wasteful; most of M6–M16 already meet the bar |
| **B. Upgrade / retrofit** to current skill + course standards | **Recommended** | Large but targeted: heavy on M1–M2 (and partly M3–M5, M17); light on M6–M16 |
| **C. Re-run hardening scripts only** on existing HTML | Easy | Hours — does **not** fix missing proofs, thin problem sets, or domain substance |

`HANDOFF.md` already states the course is complete and live. The skill is a **build protocol**, not a content oracle: it does not auto-generate the 17-module biomechanics syllabus. Scope still comes from `prompt.txt`.

---

## 2. Structural snapshot (size as a rough “maturity” proxy)

Quantitative inventory of all 17 modules at assessment time:

| Module | Size | Props / proofs | Keyresults | Solutions (`sol`) | C/D/K labels (approx) | Probes | Codewrap | Figures | Title |
|---|---|---|---|---|---|---|---|---|---|
| M01 | 44–45 KB | 4 / **2** | 1 | 0 | 0/0/0 | 0 | 0 | 5 | Mechanical Foundations |
| M02 | 38 KB | 3 / **1** | 2 | 0 | 0/0/0 | 0 | 0 | 6 | Bones as Hierarchical Load-Bearing Structures |
| M03 | 311–312 KB | 6 / **0** | 7 | 35 | sparse labels | 30 | 11 | 54 | Joints as Constrained Mechanical Interfaces |
| M04 | 335 KB | 3 / **1** | 0 | 35 | partial | 30 | 12 | 52 | Cartilage, Synovial Fluid, Joint Contact |
| M05 | 372–373 KB | 5 / **0** | 12 | 35 | 10/10/10 | 30 | 2 | 33 | Muscles as Chemo-Electro-Mechanical Actuators |
| M06 | 317–318 KB | 11 / 11 | 13 | 35 | 11/10/10 | 30 | 3 | 24 | Tendons, Ligaments, Fascia |
| M07 | 287 KB | 17 / 17 | 11 | 35 | 10/10/11 | 31 | 2 | 51 | Standing, Posture, Load Bearing |
| M08 | 138–139 KB | 10 / 10 | 5 | 30 | 10/10/10 | 30 | 4 | 41 | Walking Biomechanics |
| M09 | 207–208 KB | 15 / 15 | 2 | 31 | 10/10/10 | 30 | 4 | 41 | Running and Jumping |
| M10 | 538 KB | 15 / 15 | 6 | 35 | 10/10/10 | 30 | 4 | 41 | Balance, Stability, Sensorimotor Control |
| M11 | 298 KB | 9 / 9 | 1 | 35 | 10/10/10 | 30 | 4 | 44 | Reaching, Waving, Holding, Gripping |
| M12 | 295–296 KB | 11 / 11 | 2 | 35 | 10/10/10 | 30 | 4 | 43 | Whole-Body Coordination and Motor Control |
| M13 | 178 KB | 6 / 6 | 4 | 35 | 10/10/10 | 30 | 4 | 43 | Daily-Life Movement Case Studies |
| M14 | 190 KB | 7 / 7 | 1 | 35 | 10/10/10 | 30 | 4 | 43 | Aging, Injury, Degeneration, Adaptation |
| M15 | 211 KB | 6 / 6 | 0 | 35 | 10/10/12 | 30 | 5 | 44 | Measurement, Estimation, Inverse Dynamics |
| M16 | 176–177 KB | 8 / 8 | 2 | 35 | 10/10/10 | 30 | 4 | 42 | Continuum and FE-Style Tissue Models |
| M17 | 73 KB | 0 / 0 | 2 | 17 | 0/0/0 (different form) | 12 | 3 | 7 | Capstone Modeling Projects |

### Maturity bands

| Modules | Size band | Props ≈ proofs? | Full 30 C/D/K + solutions? | Rough status vs current skill |
|---|---|---|---|---|
| **M1** | 45 KB | 4 props / **2 proofs** | **No** (no C/D/K, 0 sols) | **Below bar** — early prototype |
| **M2** | 38 KB | 3 props / **1 proof** | **No** | **Below bar** — thinnest module |
| **M3–M5** | 310–370 KB | **proofs ≪ props** (M3: 6/0, M5: 5/0) | Yes (~35 sols, probes) | **Content-rich, rigor thin** |
| **M6–M7, M9–M16** | 180–540 KB | ≈ matched | Yes | **Meet evolved standard** (with residual polish risk) |
| **M8** | 139 KB | 10/10 | Yes | **Elevated draft** — denser than M1–2, lighter than M10 |
| **M17** | 73 KB | 0 props | Different form (capstones, ~12 probes, 17 sols) | **Intentionally different** — thinner catalog than `prompt.txt` |

**Pattern:** The skill (and course conventions) matured mid-build. Later modules absorbed new gates (`check_svg`, `check_code`, `check_probfig`, clip-hard `check_frame`, 3-layer problem figures, rigor-reviewer, K-depth). Early modules were never rebuilt under that regime.

### Section spines of thin / anomalous modules (inventory)

**Module 1**
- §0 Motivation — why a coffee cup gets heavy
- §1 Definitions, notation, and the governing law
- §2 The moment of a force
- §3 Static equilibrium of a body segment
- §4 Main result — joint torque to hold a load
- §5 From joint torque to muscle force: mechanical disadvantage
- §6 The same law at shoulder, hip, knee, ankle, and low back
- §7 Worked numerical example
- §8 Computational lab and sensitivity analysis
- §9 What the model captures and misses
- §10 Diagnostic questions and problems
- Appendix — anthropometric parameters  
- Also hosts a full **Course map — all 17 modules** (`#syllabus`)

**Module 2**
- §0 Motivation — a femur that carries tonnes yet snaps in a fall
- §1 Stress, strain, and the elastic law
- §2 Axial loading
- §3 Bending
- §4 Torsion
- §5 Where *E* comes from: mineral–collagen composite
- §6 Failure: yield, fatigue, fracture
- §7 Adaptation: Wolff’s law
- §8 Computational lab: remodeling ODE
- §9 What the model captures and misses
- §10 Diagnostic questions and problems
- Appendix — parameters

**Module 3** (content-rich spine; proofs thin)
- §0–§6 theory (DOF, taxonomy, Lagrange multipliers, JRF, contact, stability)
- §7 Computational lab (7.1–7.7)
- §8 Captures / misses / repaid
- §9 Diagnostics + 30 problems
- Appendix

**Module 5**
- §0–§8 architecture through torque
- §9 Computational labs
- §10 Limits + diagnostics/problems
- Appendix

**Module 8**
- §0–§10 gait through older-adult falls
- §11 Labs
- §12 Problems
- Appendix

**Module 17**
- §0–§1 method
- §2–§7 six worked capstones (standing, sit-to-stand, walk, run, jump/landing, hip fracture)
- §8 More capstones catalog
- §9 Validation / uncertainty
- §10 Problems and extensions
- Appendix — course in one page

---

## 3. What the skill requires (and what it does *not*)

### Skill *does* require (enforceable / semi-enforceable)

**Five pillars:**
1. Define every symbol and term at first use, self-contained.
2. One building spine — each section uses the previous; demote off-path rigor to Appendix.
3. Extensive visuals — never a wall of words; visual every screenful; split prose >~10 lines.
4. Rigorous, step-by-step derivations and proofs — box headline results; **uniform rigor across siblings** (if one result is a `.prop`+`.proof`, peers of equal weight must be proved the same way).
5. Clickable section cross-references.

**Hardening loop (current skill scripts):**
```
checktex.py      # delimiter/brace balance + stray control chars
checklt.py       # raw <,> in math
check_links.py   # #id links; unlinked § refs
check_svg.py     # viewBox arity + literal _/^ in <text>
verify_dom.py    # headless Chrome: mjx-merror, stray $, swallowed-prose advisory
check_overlap.py # labels over curves/dashed lines (hard)
check_frame.py   # CLIPPING hard-fail; wasted margin advisory
check_prose.py   # awkward constructions (advisory)
check_proofs.py  # .prop/.thm/.lem with no adjacent .proof (advisory)
check_code.py    # Python <pre><code> PEP8 via pycodestyle (hard)
check_probfig.py # bare problem figures (advisory; does not replace 3-layer audit)
autolink_sections.py
```

**Process conventions (skill + project):**
- Section-by-section build; prose lives in HTML, not Python raw strings.
- Computed geometry/plot data in scripts; figures spliced or pasted.
- Tier-2 SVG for anatomy/real entities; flat/schematic for pure physics + all SMIL.
- Problem-set (C/D/K) figures always lead with a recognizable Tier-2 entity (3-layer semantic clarity).
- Slim vector arrows (`markerUnits="userSpaceOnUse"`), never fat triangles.
- Code listings: `.codewrap` + Copy button; PEP8; no blank-line-bloated `<pre>` blocks.
- Captures/misses section for models; forward-refs as promises.
- Optional ship to GitHub Pages only on user request.

### Skill *cannot* guarantee (gaps vs `prompt.txt`)

| Prompt requirement | In skill? | Gap |
|---|---|---|
| 23-step “Mandatory Teaching Pipeline” per topic | **No** as a checklist item | Skill has motivation → derive → lab-ish → captures/misses, not the full 23 steps |
| Full Cover lists per module (e.g. M1: COP, GRF, dynamic equilibrium; M2: full torsion/fatigue/FE-ish failure) | **No** — domain-agnostic | Content completeness is **author + `prompt.txt`**, not skill |
| Biological/chemical spine depth | Prompted lightly | No mechanical check that osteocyte signaling / ATP / etc. appear |
| “Each module ≥1 computational lab” with parameter table + sensitivity | Partially (template + codewrap) | No gate that a lab exists or covers sensitivity |
| K-depth (no plug-in substitution) | **Course convention** + rigor-reviewer | Not in skill scripts; human/agent judgment |
| 30 problems C/D/K + probes + solutions | **Course convention**, not skill core | Skill assumes problem figures if you have C/D/K; does not require 30 |
| Domain correctness | Explicitly **out of skill** (`skill-improvements-from-audit.md`) | Needs rigor-reviewer / human |
| Inter-module navigation | Skill **declines** (single-doc product) | Course-level only |
| Multiscale / Level 0–10 modeling ladder | In `prompt.txt` only | No cross-module coverage map in skill |

So: **the skill is sufficient to build high-quality *documents*; it is not sufficient alone to prove the *course* matches the original syllabus.**

### Prompt “Mandatory Teaching Pipeline” (for reference — not skill-gated)

For every topic, `prompt.txt` requires this sequence:

1. Daily-life phenomenon  
2. Anatomical structure  
3. Physical mechanism  
4. Molecular / cellular substrate  
5. Mechanical idealization  
6. Coordinate system  
7. Variables and units  
8. Free-body diagram described in text  
9. Governing equations  
10. Constitutive law, if applicable  
11. Assumptions  
12. Parameter values with realistic human-scale numbers  
13. Nondimensional parameters, if useful  
14. Worked numerical example  
15. Python simulation  
16. Plotted output  
17. Sensitivity analysis  
18. Biological adaptation or failure mode  
19. Clinical / aging / injury relevance  
20. What the model captures  
21. What the model misses  
22. How one would measure or validate the model experimentally  
23. Daily-life interpretation  

Mature modules approximate a subset of this (motivation → model → numbers → lab → limits). Almost no module literally walks all 23 steps for every topic.

---

## 4. Content gaps (modules vs `prompt.txt` + course standard)

### Critical (would fail a “full rigorous-explainer pass” on today’s bar)

#### Module 1
- Missing or near-absent prompt topics: **center of pressure**, **ground reaction force**, **dynamic equilibrium** (keyword scan: 0 for those phrases as stated; COP/GRF coverage not at M7/M10 depth).
- Prompt also asks for dimensional analysis / scaling arguments and multi-joint torque derivations; some exist in thin form, not at later-module depth.
- No full C/D/K set, no collapsible solutions, no modern `codewrap` labs.
- Half of propositions unproved (skill pillar 4 / `check_proofs`).
- Known substance debt (`audit-modules.md`):
  - Use the force-balance half of Law 1 (`∑F=0`) for joint compression (~700 N to hold a 49 N bag).
  - Quantify the low-back climax (“several thousand newtons” uncomputed).
  - Define `d_m` as perpendicular moment arm; “human limbs are third-class levers” is over-general.
  - Literature reality-check for elbow-flexor moment arm / MVC torque.
- Animation caption/keyframe mismatch (bar “collapses to zero” vs keyframes stop at 75°).

#### Module 2
- **Torsion orphan** (audit): under-derived vs prompt’s “torsional shear stress” — needs `τ = Tρ/J`, *G*, angle of twist, 45° helical spiral-fracture figure.
- Thin / solution-less problem set vs M3+ standard (far below 30 C/D/K + solutions).
- Derivation gaps: neutral axis = centroidal axis (`∫y dA = 0`); Prop 3.3’s 1.44× equal-area result asserted not derived.
- Bone-strength numbers (100/130/150/170 MPa) without “tension governs bending failure” reconciliation.
- Missing or thin: Voigt/Reuss bound for modulus validation; nanostructure figure; stress concentration depth relative to prompt.
- Rigor parity: 3 props, 1 proof.
- Habitual-trajectory curve invisible (sits on grey reference line) — visual bug.

#### Modules 3–5 (structural but not “proved”)
- Large, figure-rich, 30-problem sets — but **propositions largely asserted**:
  - M3: 6 props / **0 proofs**
  - M4: 3 props / **1 proof**
  - M5: 5 props / **0 proofs**
- That is a **direct skill pillar-4 failure** even if content breadth is good.
- Residual audit items:
  - **M3:** “nonholonomic” rigor error (planar roll-and-glide is holonomic / configuration-dependent axis); hip `R ≈ 2.5W` may understate (~3W with abductor line); static prediction vs walking telemetry; K1–K10 only exercise §7 lab, not hip JRF / contact / stability; §5 congruence claim not shown as `p₀ ∝ R_eff^(−2/3)` curve.
  - **M4:** Hertz oversold (thin-layer + conforming contact; `a ≈ R_eff` breaks small-contact assumption); 10% held strain outside small-strain regime; §6 switches to knee while numeric spine is hip.
  - **M5:** §0↔§1 force reconciliation asserted; early audit noted partial module during build (now full spine exists but proofs lag).
- Old mechanical bugs (e.g. M4 malformed `viewBox="0 0 0 0 W H"`) may remain if never re-hardened under `check_svg`.

#### Module 17
- HANDOFF: 6 worked capstones + catalog of 9 more; validation section; problems.
- `prompt.txt` lists **15** capstone types, including:
  1. Quiet standing with delayed feedback *(worked)*  
  2. Sit-to-stand knee torque *(worked)*  
  3. Walking inverted pendulum *(worked)*  
  4. Running spring-mass *(worked)*  
  5. Jump and landing *(worked)*  
  6. Hip fracture sideways fall *(worked)*  
  7. Two-link arm reaching / IK *(catalog / thin)*  
  8. Grip force vs friction *(catalog / thin)*  
  9. Stair-climbing work/power *(catalog / thin)*  
  10. Age-related fall-risk toy model  
  11. Cartilage stress relaxation (poroelastic)  
  12. Tendon hysteresis and energy return  
  13. Bone adaptation under repeated loading  
  14. Muscle activation dynamics and joint torque  
  15. Simplified whole-body movement simulator  
- Structure is intentionally project-style (OK under skill for a capstone module), but thinner figures/proof packaging than M10-class modules (7 figures, 0 props/proofs).
- Keyword scan: poroelastic ≈ 0; grip/stair/two-link present only lightly.

### Medium (scope or consistency, not “empty”)

| Area | Issue |
|---|---|
| **M1 syllabus dump** | M1 still hosts a full 17-module course map — odd for a self-contained module under skill “one spine” |
| **M8** | Elevated from a thin Codex draft; 10 proofs OK, but file is lighter than neighbors — worth a targeted depth pass, not a full rewrite. Problem figures were rebuilt to 3-layer standard after regression. |
| **Cross-cutting audit A1–A8** (`audit-modules.md`) | SVG `_` underscores in labels; SVG typography vs MathJax body; unflagged symbol collisions (`M`, `a/b`, `T`, …); figures auto-numbered but prose says “the figure below”; problem-set sub-TOC; disclosure-label inconsistency (“Answer” vs “solution”); no `prefers-reduced-motion` on older SMIL; no inter-module navigation rail |
| **Mandatory pipeline** | Almost no module literally walks all 23 prompt steps per topic; mature modules approximate |
| **Symbol collisions across modules** | Course-wide single-letter reuse (`W`, `k`, `g`, `E`, …) fixed case-by-case later; early modules weaker |

### Low risk (likely already at bar)

**M6–M7, M9–M16:** matched props/proofs, ~30 problems with solutions + Probes, multi-lab code, large computed figure sets, rigor-reviewer history in HANDOFF. Residual risk is polish + re-run of **newest** checks, not rebuild.

Known residual backlog called out in HANDOFF / audit (parallel track):
- M2 torsion section  
- M1 joint-reaction / low-back number  
- M3 nonholonomic relabel  
- M4 Hertz-validity caveat  

---

## 5. Skill gaps (requirements / tooling the skill is missing for *this* course)

These are gaps **in the skill relative to running the full course to bar**, not bugs in individual modules. Companion analysis in `skill-improvements-from-audit.md` established the meta-lesson: **prose rules rot; only checks endure.**

### Encode-as-check opportunities (already planned in skill-improvements; partial progress since)

| Finding | Intended skill upgrade | Status at skill today |
|---|---|---|
| Malformed `viewBox` | `check_svg.py` 4-value assert | **Present** |
| `_` / `^` in SVG text | label linter | **Present** in `check_svg` |
| Figures never referenced by number | advisory | Advisory in `check_svg` |
| Mixed disclosure labels | advisory | Advisory in `check_svg` |
| Heavy polylines / file weight | advisory | Advisory in `check_svg` |
| Figure clipping past viewBox | hard fail | **Present** in `check_frame` (post–M10) |
| PEP8 / blank-line-bloated code | hard fail | **Present** in `check_code` |
| Bare problem figures | advisory | **Present** in `check_probfig` (does not replace semantic audit) |

### Still not skill-gated (course needs these outside pure skill)

1. **No course-syllabus gate** — skill cannot fail a module for missing GRF/COP/torsion coverage from `prompt.txt`.
2. **No “lab completeness” check** — physical/biological question, parameter table, sensitivity, failure modes, extension challenge (prompt lab template).
3. **No K-depth checker** — only rigor-reviewer + human; scripts cannot tell plug-in arithmetic from optimization / inverse / regime comparison.
4. **No 30-problem schema** — C/D/K + Probes + solutions + Tier-2 figure is project policy; skill documents problem-figure rules after M8 regression but does not require a 30-problem set.
5. **`check_proofs` is advisory** — M3/M5 can “pass” mechanical hardening while failing pillar 4 (asserted propositions).
6. **Semantic figure quality** — `check_probfig` only narrows bare abstractions; still needs manual 3-layer audit (M8 lesson: every mechanical check green, figures still uninterpretable).
7. **Domain facts** — skill correctly refuses to own these (nonholonomic, Hertz class, hip 2.5W vs 3W); without rigor-reviewer, domain errors ship.
8. **Repo playbook vs skill loop drift** — project `CLAUDE.md` / `Agents.md` sometimes list a shorter hardening set than current SKILL.md (risk of agents “hardening” to an outdated list missing `check_code` / `check_probfig` / `check_svg`).
9. **Series-level product** — prev/next nav, shared notation across modules, repayment of forward-refs: outside skill scope by design.
10. **23-step teaching pipeline** — not represented as a skill checklist.
11. **Sibling keyresult rigor** — `check_proofs` cannot see “boxed `.keyresult` law asserted beside proved peer”; judgment call remains human/reviewer.
12. **Punchline quantification** — pedagogy checklist rule exists; no mechanical check that a climax number was computed.

**Bottom line:** Running the skill “as written” on all 17 will produce **good HTML pedagogy** only if each invocation is **fed** `prompt.txt` scope + course problem-set standard + rigor-reviewer. The skill alone is under-specified for “finish the course to PhD standard.”

### What the skill correctly refuses to encode (from skill-improvements-from-audit)

- Domain rigor errors (M3 nonholonomic, M4 Hertz, bone tension-vs-compression).
- Specific content additions (“build out torsion,” “compute the low-back number”).
- Inter-module navigation as a default template rule.
- Supplying literature validation numbers (can only prompt “validate against measured value”).

---

## 6. Feasibility by workstream (if you proceed later)

### Recommended plan (not executing)

| Phase | Modules | Work | Feasibility |
|---|---|---|---|
| **0. Baseline** | All | Run full current hardening loop; inventory fails | High, fast |
| **1. Rebuild to bar** | **M1, M2** | Treat as new modules under skill + `prompt.txt` Cover lists + 30-problem set + proofs + modern labs/figures | High effort, high value |
| **2. Rigor retrofit** | **M3–M5** | Add `.proof` for every `.prop`; fix audit substance; re-harden under full loop; optional problem rebalance (M3 K-set span) | Medium–high |
| **3. Targeted upgrade** | **M8, M17** | Depth pass (M8); expand worked/catalog capstones closer to prompt’s 15 (M17) | Medium |
| **4. Polish pass** | **M6–M7, M9–M16** | Re-harden newest gates; fix any clip/overlap/code/probfig; spot-check K-depth | Low–medium |
| **5. Course-level** | index/README/nav | Optional inter-module rail; close `audit-modules.md` backlog; align CLAUDE.md hardening list with SKILL.md | Low |

### Rough effort (order of magnitude)

- **One mature module from scratch** (M10-class): multi-session, section-by-section, ~40 figures, 30 problems, labs, rigor-reviewer.
- **Full greenfield × 17:** not practical given existing assets — would discard large correct work in M6–M16.
- **Upgrade path above:** roughly **~30–50% of a full rebuild cost**, concentrated in M1–M5 + M17.

### Risk factors (why autonomous full-run is dangerous)

- Skill explicitly warns: **skipping “approve one representative figure”** caused M8 problem-figure regression (flat abstraction misread as license; mechanical checks all green).
- Autonomous bulk runs skip user section review (course convention: section → ★ Insights → user → commit only on “commit push”).
- Early modules are small enough that “upgrade” can accidentally **overwrite good thin structure** with verbose bulk if not planned against `prompt.txt`.
- Numpy figure pipelines + headless Chrome checks are slow; wall-clock dominates multi-module runs.
- `autolink_sections.py` rewrites the whole file and invalidates edit caches; leaves `.bak` files.
- Shell-mangled math (`python -c "…$…"`) can pass `checktex`/`verify_dom` while swallowing prose — raw-string / Write-Edit discipline required.
- Session-transient figure generators live in scratchpad; regenerating early modules needs either re-authoring generators or editing committed SVG in place.

### Course build loop (established; any retrofit should follow it)

1. Invoke rigorous-explainer / follow SKILL.md.  
2. Plan spine from `prompt.txt` + prior-module forward-refs.  
3. Build **one section** → short summary + 2 ★ Insight bullets → user review.  
4. Prose in HTML; Python for figures only.  
5. Hardening loop after every edit.  
6. After scripts hit 0, dispatch **rigor-reviewer** (rigor parity, read-aloud prose, K-depth, self-containment).  
7. Commit/push only on user “commit push”; publish-while-incomplete: wire `index.html` + `README.md` live URLs.

---

## 7. Go / no-go summary

| Question | Answer |
|---|---|
| Can the skill be applied to all 17 modules? | **Yes** |
| Should you rebuild all 17 from zero with it? | **No** — most mid/late modules already satisfy it |
| Will the skill alone ensure `prompt.txt` completeness? | **No** — major content/process gap |
| Biggest content holes for a true “skill bar” pass? | **M1, M2** (structure + topics); **M3–M5** (proof parity); **M17** (catalog breadth); residual **audit-modules** domain fixes |
| Biggest skill holes for this course? | Syllabus/lab/K-depth gates; advisory proofs; domain review out of band; 23-step pipeline not encoded |
| Best next move if you decide to proceed | **Phase 0 harden inventory**, then **M1 or M2 full upgrade** as the pilot for the retrofit pattern — not “run skill on all 17 overnight” |

---

## 8. Recommendation

**Feasible as a multi-phase retrofit, not as one `/rigorous-explainer` sweep.**

1. Treat **M6–M16 as mostly done** (verify, don’t rebuild).  
2. Treat **M1–M2 as incomplete relative to today’s skill**.  
3. Treat **M3–M5 as content-complete / rigor-incomplete**.  
4. Treat **M17 as structurally complete / catalog-incomplete vs prompt**.  
5. Before any mass run, either **encode course-specific gates** (lab present, problem count, K-depth review mandatory) into the project playbook, or accept that skill success ≠ syllabus success.

### Suggested success criteria for a future retrofit (course-specific, not pure skill)

For each module to be declared “at bar”:

- [ ] Full current skill hardening loop = 0 hard fails  
- [ ] Every `.prop`/`.thm`/`.lem` has adjacent `.proof` (or demoted)  
- [ ] Sibling boxed results share rigor level (eyeball + rigor-reviewer)  
- [ ] `prompt.txt` Cover list items present or explicitly deferred with repayment pointer  
- [ ] ≥1 computational lab with code + interpreted output + sensitivity  
- [ ] Problem set at course standard (typically 10C+10D+10K + diagnostics + solutions + Probes + Tier-2 figures), or justified alternate form (M17 capstones)  
- [ ] All K problems pass K-depth test (not plug-in substitution)  
- [ ] Rigor-reviewer pass (or equivalent human domain review) for domain facts  
- [ ] Captures/misses + notation appendix  
- [ ] Live wiring in `index.html` + `README.md`  

### Useful follow-ups (zero-build)

1. **Phase 0 hardening inventory table** — exit codes per check × module (makes gaps mechanical rather than size-based).  
2. **Prompt coverage matrix** — Cover bullets × module rows, mark present / thin / missing.  
3. **Pilot upgrade of M1 or M2** under full skill + problem-set standard, then copy the pattern.

---

## 9. Reference pointers

| Artifact | Role |
|---|---|
| `prompt.txt` | Source of truth for 17-module scope and teaching pipeline |
| `HANDOFF.md` | Live resume point; claims full course complete & live |
| `CLAUDE.md` / `Agents.md` | Standing project conventions |
| `audit-modules.md` | Substance + cross-cutting defects for M1–M5 |
| `skill-improvements-from-audit.md` | What of the audit belongs in the skill vs not |
| `~/.claude/skills/rigorous-explainer/SKILL.md` | Skill pillars, workflow, hardening loop |
| `~/.claude/skills/rigorous-explainer/scripts/` | Mechanical gates |
| `.claude/agents/rigor-reviewer.md` | Independent judgment on rigor/prose/K-depth/self-containment |
| Live site | https://az9713.github.io/biomechanics/ |
| Repo | https://github.com/az9713/biomechanics |

---

*End of assessment. Written by Grok 4.5 high (xAI). No modules were modified; `/rigorous-explainer` was not run.*
