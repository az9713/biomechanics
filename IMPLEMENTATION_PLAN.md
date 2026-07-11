# Implementation plan — bringing all 17 modules to the current skill bar

**Author:** Claude · **Date:** 2026-07-10 · **Scope:** full retrofit (assessment phases 0–6)
**Basis:** the revised feasibility assessment (`rigorous-explainer-feasibility-assessment-revised.md`) + a **Phase-0 mechanical inventory run this session** (all 11 hardening checks × 17 modules; exit codes are ground truth, not scan inferences).
**Prime directive:** every module is already **live**. This is a *retrofit*, not a rebuild — work on a branch, re-harden after every pass, never rewrite good thin structure into verbose bulk, and keep the **rigor-reviewer as a hard gate** before any commit.

---

## Phase 0 — mechanical inventory (DONE this session)

Ran `checktex, checklt, check_links, check_svg, verify_dom, check_overlap, check_frame, check_code, check_prose, check_proofs, check_probfig` on `module01…17.html`. Exit codes:

| Module | Hard gates | Failing hard gates (count) | Proof gap (props−proofs) | Other advisories |
|---|---|---|---|---|
| **M01** | ❌ | `check_frame` clip · `check_code` (7) | −2 (Prop 5.1 muscle force unproved) | — |
| **M02** | ❌ | `check_code` (19) | −2 (thm unproved) | — |
| **M03** | ❌ | `check_frame` clip · `check_code` (27) | −6 raw → **~4 real** (Hertz cited/deferred; 7 are `.def`) | — |
| **M04** | ❌ | `check_code` (39) | −2 | — |
| **M05** | ❌ | `check_frame` clip · `check_code` (21) | −5 raw → **~1–2 real** (Prop 6.1 = Hill 1938 cited; 1 block already ∎ but mislabeled `.prop`) | — |
| **M06** | ❌ | `check_frame` clip · `check_code` (48) | 0 (exact parity) | — |
| **M07** | ❌ | `check_frame` clip · `check_code` (26) | 0 | `check_probfig`: C10, D4 bare |
| **M08** | ❌ | `check_frame` clip | 0 | — |
| **M09** | ✅ | — | 0 | — |
| **M10** | ✅ | — | 0 | — |
| **M11** | ✅ | — | 0 | — |
| **M12** | ✅ | — | 0 | `check_probfig`: 1 flagged (`?`) — inspect |
| **M13–M17** | ✅ | — | 0 (M17 project-form, no props) | — |

**Three findings that reshape the plan:**

1. **8 of 17 modules fail a HARD gate right now** — all in `check_code` (PEP8 on `<pre>` blocks) and/or `check_frame` (figure clipping). **M9–M17 are hard-gate-clean.**
2. **The "predates the newest gates" boundary is M1–M8, not M1–M4.** M6/M7/M8 — nominally "at bar" — fail `check_code`/`check_frame` only because those gates were added at ~M8/~M10 and never re-run against them. This is mechanical, not a quality regression in their math.
3. **The proof-gap counts over-read** (confirmed by reading M3/M5): raw −6/−5 collapse to ~4/~1–2 real, because `.def` blocks, cited standard laws (Hertz, Hill 1938), and one already-∎ derivation mislabeled `.prop` are all in the raw count. Phase 2 is smaller than a div-count implies.

---

## The retrofit, phase by phase

Ordered cheapest-and-highest-certainty first. Phases 1–2 are mechanical/low-risk; 3–4 are the real content work (M1/M2); 5–6 are optional/polish.

### Phase 1 — Hard-gate green sweep (M1–M8) · *low risk, do first*
Make all 17 modules pass every hard gate. Purely corrective; no new content.
- **`check_code` (M1–M7):** fix PEP8 in the `<pre><code>` blocks — mostly E501 (long lines) and E303 (blank-line spacing). Counts: M1=7, M2=19, M3=27, M4=39, M5=21, M6=48, M7=26. Re-author lines with Write/Edit (one statement per line, ≤79 chars); re-run `check_code` to 0.
- **`check_frame` (M1, M3, M5, M6, M7, M8):** each has ≥1 figure clipped past its viewBox. The script prints the enlarged viewBox to paste (e.g. M1 `39 33 289 159`, M3 `101 13 334 190`, M5 `-12 10 352 130`, M6 `-12 -64 365 223`, M7 `0 28 498 167`, M8 `30 16 289 135`). Apply, re-run to 0.
- **Gate:** all 8 modules exit 0 on all hard gates. One commit per module (or one sweep commit) with a re-run log.

### Phase 2 — Rigor-parity retrofit (M1–M5) · *low–medium*
Close the proof gaps — but **read each boxed result first** and take the cheapest correct action, not "write N proofs":
- **M5 (~1–2 real):** relabel the descending-limb block `class="prop"`→`class="proof"` (it already ends in ∎); confirm-exempt Prop 1.1 (architecture identity), Prop 6.1 (Hill 1938, cited), Prop 3.1 (Hill kinetics, cited); add a short derivation only where genuinely missing (e.g. Prop 2.1 piecewise assembly).
- **M3 (~4 real):** add `.proof` to Mobility (Grübler count), Theorem 3.1 (constrained EOM), Prop 3.2 (the multiplier), Stability ratio / Hip reaction; **defer Hertz** to Module 4's biphasic contact with a forward pointer (`.keyresult` + "derived in §…").
- **M1 (−2):** prove Prop 5.1 (muscle force) and its sibling; **M2 (−2):** prove the two flagged thm; **M4 (−2):** prove or demote the 2 gap items (M4 is otherwise reviewer-clean).
- **Sibling-parity eyeball** on every touched section (a proved result must not sit beside an asserted `.keyresult` peer of equal weight).
- **Gate:** `check_proofs` says "every proposition/theorem/lemma is proved" for M1–M5, and a human/reviewer confirms no mislabeled sibling remains.

### Phase 3 — Domain-substance fixes (M1–M7) · *medium* — the `audit-modules.md` backlog
- **M1:** compute the ~700 N joint-compression number (the unused `∑F=0` half of Law 1); quantify the low-back "several thousand newtons" climax; fix the `d_m` moment-arm definition + the third-class-lever over-generalization; reconcile the animation caption/keyframe mismatch; add COP/GRF/dynamic-equilibrium coverage.
- **M2:** add the torsion strand (`τ=Tρ/J`, `G`, angle of twist, 45° helical-fracture figure); reconcile bone-strength numbers with tension-governs-bending; fix the invisible habitual-trajectory curve; derive the neutral-axis / Prop-3.3 gaps.
- **M3:** relabel "nonholonomic" correctly; reconcile hip `R≈2.5W` vs ~3W with the abductor line.
- **M4:** add the Hertz-validity caveat for thin-layer conforming contact; flag the 10%-strain excursion outside small-strain; align §6's knee example with the hip numeric spine.
- **M5:** reconcile the §0↔§1 force numbers.
- **M7:** redraw the 2 bare problem figures (`check_probfig`: C10, D4) to lead with a Tier-2 entity. **M12:** inspect the 1 flagged figure.
- **Gate:** each fix re-hardened to 0; reviewer confirms the domain claim.

### Phase 4 — Problem-set build to standard (M1, M2) · *high effort — the real cost*
M1 and M2 lack the 30-problem C/D/K set with solutions/Probes/Tier-2 figures.
- Build 10 conceptual + 10 derivational + 10 computational + diagnostics per module, each with a collapsible `<details class="sol">` solution and a Tier-2 figure; **K problems must pass the K-depth test** (sim/opt/inverse/sensitivity/regime — no plug-in).
- **Style sign-off:** approve one representative figure before mass-producing.
- **Gate:** `check_probfig` = 30 clean figures; rigor-reviewer K-depth pass.

### Phase 5 — M17 optional depth · *low, optional*
M17 covers all 15 capstones (6 worked + 9 §8 briefs). Optionally deepen selected briefs from model-sketch to worked simulation. **Not** "add missing capstones" — coverage is already complete.

### Phase 6 — Course-level · *low*
- **Align the project `CLAUDE.md` / `AGENTS.md` hardening list with SKILL.md's current 11-check loop** (drift risk flagged in the assessment; do before any mass run).
- Close remaining `audit-modules.md` cross-cutting items; optional inter-module nav/notation rail.

---

## Cross-cutting rules (every phase)
1. **Branch + re-harden.** Work on a retrofit branch; run the full 11-check loop to 0 after every edit pass; `rm` `.bak` files `autolink_sections.py` leaves.
2. **Rigor-reviewer is a hard gate** before each module's commit (the fix that gated the M8-class regression — see the assessment).
3. **Do no harm.** Do not delete correct content to satisfy a checker; fix the specific issue.
4. **Publish-while-incomplete stays.** Modules are already live; keep them live — no module goes dark mid-retrofit.

## Per-module "at bar" acceptance checklist
- [ ] Full 11-check loop = 0 hard fails
- [ ] Every `.prop`/`.thm`/`.lem` has a `.proof` **or** is a demoted/exempt definition-substitution-cited-law
- [ ] Sibling boxed results share rigor level (reviewer eyeball)
- [ ] `prompt.txt` Cover-list items present or explicitly deferred with a repayment pointer
- [ ] ≥1 computational lab with code + interpreted output + sensitivity
- [ ] 30-problem set (10C+10D+10K + diagnostics + solutions + Probes + Tier-2 figures), or justified alternate form (M17)
- [ ] All K problems pass the K-depth test (not plug-in)
- [ ] Rigor-reviewer pass for domain facts
- [ ] Captures/misses + notation appendix
- [ ] Live wiring in `index.html` + `README.md`

## Effort summary
- **Bulk of the work:** Phase 4 (M1/M2 problem sets) + Phase 3 (M1/M2 domain content).
- **Cheap high-value quick wins:** Phase 1 (hard-gate sweep — makes all 17 green) and Phase 2 (proof relabels, smaller than the raw counts).
- **M9–M17:** confirm-for-drift only; already hard-gate-clean and reviewer-vetted.

*Phase 0 artifact: `phase0_result.json` (repo root) — the raw exit-code inventory this plan is built on.*
