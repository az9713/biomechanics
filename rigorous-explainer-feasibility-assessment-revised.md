# Feasibility assessment (revised): `/rigorous-explainer` on all 17 modules

**Author:** Claude (revision of the Grok 4.5-high assessment of 2026-07-10)
**Date:** 2026-07-10
**Status:** Assessment only — skill not run; no modules modified.
**Sources:** the v1 assessment (`rigorous-explainer-feasibility-assessment.md`); `prompt.txt`, `HANDOFF.md`, `audit-modules.md`, `skill-improvements-from-audit.md`, the skill `CHANGELOG.md`; the repo **git history** (138 commits, 2026-06-28 → 2026-07-10); `rigorous-explainer` SKILL.md + scripts; and **first-hand knowledge of building Modules 11–17 and fixing Module 14 this session** (each built under the full 12-check loop + 3-pass rigor-reviewer).

**Verdict (unchanged from v1):** Feasible, but **not as a single greenfield run**. All 17 modules exist and are live. The real work is **raising the earliest modules to the *current* skill bar and closing content gaps against `prompt.txt`** — not "build the course from zero."

> **Why this revision exists.** The v1 assessment is careful and its thesis is right. It was built from *structural scans + keyword counts* without reading section prose or the git log — which is cheap and unbiased but has two systematic biases: it **undercounts paraphrased coverage** and **over-reads `<div>` counts as rigor**. This revision keeps v1's structure and correct conclusions, and corrects five claims where the scan-only method misled or where events since (the autonomous 11–17 run) overtook it. A transparent diff is in §10.

---

## 1. What "run rigorous-explainer on all 17" actually means

| Interpretation | Feasible? | Effort order |
|---|---|---|
| **A. Greenfield rebuild** of every module | Yes, technically | Very large — wasteful; most of M6–M16 already meet the bar |
| **B. Upgrade / retrofit** to current skill + course standards | **Recommended** | Large but targeted: heavy on M1–M2; verify-then-fix on M3–M5, M17; light on M6–M16 |
| **C. Re-run hardening scripts only** on existing HTML | Easy | Hours — does **not** fix missing proofs, thin problem sets, or domain substance |

`HANDOFF.md` states the course is complete and live. The skill is a **build protocol**, not a content oracle: it does not generate the biomechanics syllabus. Scope comes from `prompt.txt`. **Agree with v1 in full.**

---

## 2. Structural snapshot — and why size is *not* a maturity proxy

v1's per-module inventory table (props/proofs, keyresults, solutions, C/D/K, probes, codewrap, figures) is useful and preserved by reference. **But one column must be demoted: file size (KB).**

**Size is a weak proxy and is sometimes *inverted*.** KB is dominated by figure count and SVG polyline density, not rigor. In the 11–17 build I routinely **decimated heavy polylines** to clear `check_svg`'s >120-point advisory — so a *more* hardened figure is a *smaller* one. M8 at 139 KB vs M10 at 538 KB reflects figure weight and decimation history, not completeness. Use size only as the faintest hint; the real maturity signals are **(a) mechanical exit codes and (b) proof/rigor parity confirmed by reading**, both of which v1's own Phase 0 correctly elevates.

### Maturity bands (revised)

| Modules | Props ≈ proofs? | Full 30 C/D/K + solutions? | Status vs current skill |
|---|---|---|---|
| **M1** | 4 props / 2 proofs | No (no C/D/K, 0 sols) | **Below bar** — early prototype |
| **M2** | 3 props / 1 proof | No | **Below bar** — thinnest module |
| **M3–M5** | proofs `<` props by `<div>` count (M3 6/0, M5 5/0) | Yes (~35 sols, probes) | **Content-rich; rigor-parity UNVERIFIED — must read, not count** |
| **M6–M7, M9–M10** | matched | Yes | **At bar** — reviewer history in HANDOFF |
| **M11–M16** | matched | Yes | **At bar and reviewer-vetted** — built this session under the full loop + 3-pass review, findings fixed |
| **M8** | 10/10 | Yes | **Elevated Codex draft** — problem figures rebuilt to 3-layer; a *read*, not a rebuild, decides if depth suffices |
| **M17** | 0 props (project form) | Alternate form (capstones) | **Structurally complete; catalog depth vs breadth is the question, not missing capstones** |

**Pattern (agree):** the skill and course conventions matured mid-build; later modules absorbed gates (`check_svg`, `check_code`, `check_probfig`, clip-hard `check_frame`, K-depth, the rigor-reviewer) that early modules never saw. **Correction to v1:** it binned M11–M16 with M6–M9 as "meet evolved standard, residual polish risk." That understates them — M11–M16 were *born under the final regime* (12-check loop to zero **and** three parallel rigor-reviewer passes with every finding fixed and committed). They are not "probably pass the newest checks"; they are the modules the newest checks and the reviewer were *designed on*. Polish risk applies to M6–M9; M11–M16 are the current high-water mark.

### The `props ≫ proofs` counts are a flag to verify, not a verdict

v1 calls M3 (6/0) and M5 (5/0) "a direct skill pillar-4 failure even if content breadth is good." **This over-claims from a `<div>`-class count.** Three reasons it must be downgraded to *"highest-priority thing to confirm by reading"*:

1. A derivation can be **rigorous in prose** without a `.proof` wrapper; the count sees wrappers, not arguments.
2. `.keyresult` boxes are frequently **definitions or one-line substitutions that need no proof** — the skill's *own* exemption (a boxed definition, a cited standard like Hertz, an empirical fit like Hill's equation is *stated, not proved*). M5's 12 keyresults are exactly the population that exemption targets; counting them as unproved propositions is the error the exemption exists to prevent.
3. `check_proofs` is **advisory** precisely because the crisp case (a bare `.prop` with no adjacent `.proof`) is mechanical but the sibling-parity case is a judgement.

So: M3/M5 rigor parity is a **real risk worth putting first in the retrofit**, but whether it is an actual failure requires reading the sections — which the scan did not do. Treat as *unverified*, not *failed*.

---

## 3. What the skill requires (and what it does *not*) — agree, preserved

**Five pillars, the 12-script hardening loop, and the process conventions** are stated correctly in v1 (§3). No revision. The load-bearing correct point, preserved verbatim in spirit: **the skill is sufficient to build high-quality *documents*; it is not sufficient alone to prove the *course* matches the syllabus.** This is the sharpest and most durable claim in the assessment.

The one calibration: the current loop is **12 checks** (`checktex`, `checklt`, `check_links`, `check_svg`, `verify_dom`, `check_overlap`, `check_frame`, `check_prose`, `check_proofs`, `check_code`, `check_probfig`, `autolink_sections`). A retrofit must run *this* list — the risk v1 flags in §5.8 (repo `CLAUDE.md` sometimes lists a shorter set) is real and worth fixing first.

---

## 4. Content gaps (revised where the scan misled)

### M1 and M2 — **agree, below bar**

v1's diagnosis stands and is well-sourced against `audit-modules.md`:

- **M1:** no full C/D/K set, no collapsible solutions, no modern `codewrap` labs; half the propositions unproved; missing/thin COP, GRF, dynamic-equilibrium coverage; the `∑F=0` half of Law 1 unused (the ~700 N joint-compression number uncomputed); the low-back climax ("several thousand newtons") unquantified; `d_m` moment-arm definition and third-class-lever over-generalisation; an animation caption/keyframe mismatch. **These are genuine and are the right pilot target.**
- **M2:** the **torsion orphan** (needs `τ = Tρ/J`, `G`, angle of twist, the 45° helical fracture figure); a thin/solution-less problem set far below the 30 C/D/K standard; neutral-axis and Prop-3.3 derivation gaps; bone-strength numbers without the tension-governs-bending reconciliation; a habitual-trajectory curve invisible on a grey reference line. **Agree — M2 is the thinnest module.**

These two are the highest-value work and the correct place to pilot the retrofit pattern. No change from v1.

### M3–M5 — **content-complete; rigor parity UNVERIFIED (was: "failure")**

v1 lists real residual audit items I'd keep on the board (M3 "nonholonomic" relabel; M3 hip `R ≈ 2.5W` vs ~3W with the abductor line; M4 Hertz-validity caveat for thin-layer conforming contact; M4 10%-strain outside small-strain regime; M4 §6 switching to the knee while the numeric spine is the hip; M5 §0↔§1 force reconciliation). **Keep these** — they are domain substance a reviewer/human must settle.

**Revision:** reframe the headline from "pillar-4 failure" to "**rigor parity unverified — read before ruling**," per §2 above. The retrofit action is the same (add `.proof` where a `.prop` genuinely asserts an un-earned result; demote or leave alone where a box is a definition/substitution/cited law), but the *finding* should not pre-judge from counts.

**Stale specific, corrected:** v1 worries M4's malformed `viewBox="0 0 0 0 W H"` "may remain if never re-hardened." **The git log shows it was swept:** commit (07-01) *"Fix all 51 check_svg hard issues in Modules 1–4 (labels + viewBox)"*, preceded by `check-svg-fixlist.md` (the exact worklist). So that *specific* bug is almost certainly gone. The *general* point survives — M1–M4 never saw the **post-M10** gates (clip-hard `check_frame`, `check_code`, `check_probfig`) — but the cited example is a snapshot-without-git miss. Phase 0 will confirm mechanically.

### M17 — **catalog depth, not missing capstones (was: "catalog-incomplete")**

v1 reads `prompt.txt`'s 15 capstone types against M17 and flags 9 as "catalog / thin" or absent, with "poroelastic ≈ 0." **Two corrections:**

1. **All 15 are present.** M17 has **6 fully-worked capstones** (standing, sit-to-stand, walking, running, jump/landing, hip fracture) **plus a §8 catalog table covering the other 9** (reaching/IK, grip-vs-friction, stair work/power, fall-risk toy model, cartilage stress relaxation, tendon hysteresis, bone adaptation, muscle activation, whole-body simulator), each with a model + key equation + expected result. Coverage is complete; the honest critique is **depth** — the 9 are structured *briefs*, not worked simulations.
2. **"poroelastic ≈ 0" is a keyword-scan artifact.** The cartilage-relaxation row is written as "biphasic consolidation," not "poroelastic" — the concept is present under the term the course actually uses (Module 4's / Module 16's vocabulary). A keyword grep for "poroelastic" is the wrong probe.
3. **`prompt.txt` says "Offer... projects *such as*."** The 15 are framed as an illustrative menu, not a build-all-15 mandate. A capstone module that works six end-to-end and briefs the remaining nine is a defensible — arguably correct — reading of the spec, not a shortfall. Reframe M17 from "incomplete" to "**complete in breadth; a depth pass on selected briefs is optional, not required.**"

### The 23-step "Mandatory Teaching Pipeline" — **a superset menu, not a per-topic mandate**

v1 lists "23-step pipeline not encoded" as a gap and notes "almost no module walks all 23 steps for every topic." **This treats an illustrative superset as a literal obligation.** 23 steps × ~8 topics × 17 modules is not a build target any author would honour literally; the list is a checklist to draw the *relevant subset* from per topic (motivation → structure → idealisation → equations → assumptions → numbers → simulation → limits → validation is the recurring backbone). v1 concedes "mature modules approximate a subset" — which is the correct read — so it should not also be scored as a skill hole. **Downgrade** from "gap" to "the skill's motivation→derive→lab→captures/misses arc *is* the intended subset; per-topic completeness is an authoring judgement, not a checklist to encode."

---

## 5. Skill gaps for *this course* — agree, with one reframed risk

v1's §5 is the strongest section and is preserved. The skill genuinely lacks, and the course needs outside the skill:

1. **No course-syllabus gate** — cannot fail a module for missing GRF/COP/torsion. ✔ agree.
2. **No lab-completeness check** (question + parameter table + sensitivity + failure mode + extension). ✔ agree.
3. **No K-depth checker** — only the rigor-reviewer + human tell plug-in arithmetic from simulation/optimization/inverse/regime. ✔ agree, and confirmed this session: the reviewer caught **two Module-16 K-problems that were plug-in** and forced their recast into genuine sweeps — a script could not have.
4. **No 30-problem schema** as a hard requirement. ✔ agree.
5. **`check_proofs` is advisory** — M3/M5 can pass mechanical hardening while (possibly) failing pillar 4. ✔ agree (with §2's "verify by reading" caveat).
6. **Semantic figure quality** still needs the manual 3-layer audit. ✔ agree.
7. **Domain facts** are out of skill by design. ✔ agree.
8. **Repo playbook vs skill-loop drift** — `CLAUDE.md` may list a shorter hardening set than SKILL.md. ✔ agree — **fix before any mass run.**
9. **Series-level product** (nav, shared notation) — out of scope by design. ✔ agree.
10. **23-step pipeline** — reframed (see §4): the intended subset is already the skill's arc; not a genuine hole.
11. **Sibling `.keyresult` rigor** — human/reviewer judgement. ✔ agree.
12. **Punchline quantification** — pedagogy rule exists; no mechanical check. ✔ agree.

**Reframed risk — the autonomous-run danger is partly overtaken by events.** v1's headline caution ("autonomous full-run is dangerous — M8's flat-figure regression happened with all mechanical checks green") is sound *ex ante* but cites a hazard **that has since been gated**. The M8 regression predates `check_probfig` and the rigor-reviewer; those two *were the fix*. In the 11–17 autonomous run the manual "approve one representative figure" step was not silently skipped — it was **replaced** by `check_probfig` (narrows bare abstractions) plus the rigor-reviewer's semantic + K-depth audit, which is exactly what caught the plug-in K-problems, a dimensionally-unsound damping gain, and an arithmetic Froude error before commit. So: *autonomous runs of un-reviewed modules are dangerous* (true, and the M8 evidence is real), but *the pipeline that ran 11–17 was not un-reviewed* — it carried the reviewer as a mandatory gate. The correct standing rule is **"autonomous is acceptable only with the rigor-reviewer in the loop as a hard gate,"** not "autonomous is dangerous."

---

## 6. Feasibility by workstream — agree, lightly adjusted

| Phase | Modules | Work | Feasibility |
|---|---|---|---|
| **0. Baseline** | All | Run the **full current 12-check loop**; record exit codes per module | High, fast — do this first |
| **1. Rebuild to bar** | **M1, M2** | Treat as new under skill + `prompt.txt` Cover lists + 30-problem set + proofs + modern labs/figures | High value — the pilot |
| **2. Rigor verify-then-retrofit** | **M3–M5** | **Read** the propositions first; add `.proof` only where a result is genuinely asserted un-earned; fix the named audit substance; re-harden | Medium (less than v1 implied if many "gaps" are exempt keyresults) |
| **3. Optional depth** | **M8, M17** | M8: read-then-decide on a depth pass. M17: optionally deepen selected §8 briefs — **not** "add missing capstones" (they're present) | Low–medium, optional |
| **4. Polish** | **M6–M7, M9–M10** | Re-run newest gates; spot-check K-depth | Low |
| **5. Confirm** | **M11–M16** | Re-run the loop for drift only; already reviewer-vetted this session | Very low |
| **6. Course-level** | index/README/nav | Optional inter-module rail; align `CLAUDE.md` hardening list with SKILL.md; close `audit-modules.md` backlog | Low |

**Effort estimate:** v1's "~30–50% of a full rebuild, concentrated in M1–M5 + M17" is about right, and likely **toward the lower end** once §2's "verify before ruling" prunes the M3/M5 work and §4 removes the M17 "missing capstones" item. The real spend is **M1 + M2** (genuine rebuilds) plus the **named M3–M5 domain fixes**.

### Risk factors (agree; the M8 one reframed)

All of v1's operational risks are real and I hit several this session: `autolink_sections.py` invalidating edit caches and leaving `.bak` files; shell-mangled `$…$` passing `checktex`/`verify_dom` while swallowing prose (raw-string / Write-Edit discipline required); numpy + headless-Chrome wall-clock dominating; session-transient figure generators needing re-authoring to touch early-module SVGs. **The one reframe:** "skipping approve-one-figure caused M8" → *that gap is now gated by `check_probfig` + the reviewer;* the residual risk is running autonomously **without** the reviewer, not autonomy itself.

---

## 7. Go / no-go summary (revised cells marked \*)

| Question | Answer |
|---|---|
| Can the skill be applied to all 17 modules? | **Yes** |
| Should you rebuild all 17 from zero? | **No** — most mid/late modules already satisfy it |
| Will the skill alone ensure `prompt.txt` completeness? | **No** — the durable correct point |
| Biggest content holes for a true "skill bar" pass? | **M1, M2** (structure + topics); **M3–M5** (named domain fixes + *verify* proof parity\*); residual **audit-modules** items. *(M17 removed — coverage is complete; depth optional.\*)* |
| Biggest skill holes for this course? | Syllabus / lab / K-depth gates; advisory proofs; domain review out of band. *(23-step pipeline removed as a "hole".\*)* |
| Best next move | **Phase 0 harden inventory**, then **M1 or M2 full upgrade** as the pilot — with the **rigor-reviewer as a mandatory gate**, not "run skill on all 17 overnight" |

---

## 8. Recommendation (agree, tightened)

**Feasible as a multi-phase retrofit, not one `/rigorous-explainer` sweep.**

1. Treat **M11–M16 as done and reviewer-vetted** (confirm for drift only).\*
2. Treat **M6–M10 as at bar** (polish + newest-gate re-run).
3. Treat **M1–M2 as genuine rebuilds** relative to today's bar.
4. Treat **M3–M5 as content-complete; rigor parity to be *verified by reading*, then retrofitted only where genuinely asserted**, plus the named domain fixes.\*
5. Treat **M17 as complete in breadth**; a depth pass on §8 briefs is optional.\*
6. Before any mass run, **align the project `CLAUDE.md` hardening list with SKILL.md** and make the **rigor-reviewer a hard gate** — then autonomy is safe (it was, for 11–17).\*

### Success criteria for "at bar" (per module) — unchanged from v1, correct as written

- [ ] Full current 12-check hardening loop = 0 hard fails
- [ ] Every `.prop`/`.thm`/`.lem` has an adjacent `.proof` **or is demoted / is an exempt definition-substitution-cited-law**\*
- [ ] Sibling boxed results share rigor level (eyeball + rigor-reviewer)
- [ ] `prompt.txt` Cover-list items present or explicitly deferred with a repayment pointer
- [ ] ≥1 computational lab with code + interpreted output + sensitivity
- [ ] Problem set at course standard (10C+10D+10K + diagnostics + solutions + Probes + Tier-2 figures), or a justified alternate form (M17 capstones)
- [ ] All K problems pass the K-depth test (not plug-in)
- [ ] Rigor-reviewer pass (or equivalent human domain review) for domain facts
- [ ] Captures/misses + notation appendix
- [ ] Live wiring in `index.html` + `README.md`

### Useful zero-build follow-ups (agree)

1. **Phase 0 hardening inventory table** — exit codes per check × module (replaces size/count proxies with mechanical truth).
2. **Prompt coverage matrix** — Cover bullets × module rows, marked present / thin / missing (by *reading*, not keyword grep — the poroelastic lesson).\*
3. **Pilot upgrade of M1 or M2** under the full skill + problem-set standard + reviewer, then copy the pattern.

---

## 9. Reference pointers (agree; git history added)

| Artifact | Role |
|---|---|
| `prompt.txt` | Source of truth for 17-module scope and the teaching-pipeline *menu* |
| `HANDOFF.md` | Live resume point; course complete & live |
| `CLAUDE.md` / `AGENTS.md` | Standing project conventions (align the hardening list with SKILL.md) |
| `audit-modules.md` | Substance + cross-cutting defects for M1–M5 |
| `skill-improvements-from-audit.md` | What of the audit belongs in the skill vs not |
| `~/.claude/skills/rigorous-explainer/CHANGELOG.md` | The skill's own iteration record |
| **repo git history** | **The build timeline; settles "was X already fixed?" mechanically (e.g. the 51 check_svg fixes on M1–4)** |
| `~/.claude/skills/rigorous-explainer/{SKILL.md,scripts/}` | Pillars, workflow, the 12 gates |
| `.claude/agents/rigor-reviewer.md` | Independent judgement on rigor/prose/K-depth/self-containment |
| Live site / repo | https://az9713.github.io/biomechanics/ · https://github.com/az9713/biomechanics |

---

## 10. Diff from the v1 (Grok) assessment — what changed and why

| # | v1 claim | Revision | Reason |
|---|---|---|---|
| 1 | File-size (KB) used as a rough maturity proxy | **Demoted to near-zero weight; noted it can *invert*** | Size tracks figure/polyline weight; hardened figures are *decimated* (smaller). Exit codes + read-confirmed parity are the real signals. |
| 2 | M3/M5 `props ≫ proofs` = "direct pillar-4 failure" | **"Rigor parity unverified — read before ruling"** | A `<div>` count can't see prose derivations or the skill's own definition/substitution/cited-law exemptions (M5's 12 keyresults). |
| 3 | M6–M16 all "meet evolved standard, polish risk" | **M11–M16 credited as reviewer-vetted this session** (born under the full loop + 3-pass review) | They are the modules the newest gates + reviewer were designed on, with findings fixed and committed — not merely "probably pass." |
| 4 | M4 `viewBox="0 0 0 0 W H"` "may remain" | **Almost certainly already fixed** (git: "Fix all 51 check_svg hard issues in Modules 1–4", 07-01) | Snapshot-without-git miss; the *general* "M1–4 never saw post-M10 gates" point survives. |
| 5 | M17 "catalog-incomplete"; "poroelastic ≈ 0" | **Complete in breadth (6 worked + 9 briefs = all 15); "poroelastic" is a keyword artifact for "biphasic consolidation"; prompt says "such as"** | Coverage is present; the real critique is *depth of the 9 briefs*, which is optional against an illustrative menu. |
| 6 | "23-step pipeline not encoded" listed as a skill hole | **Reframed as a superset menu; the skill's arc is the intended subset** | 23 × topics × modules is not a literal mandate; v1 itself concedes "approximate a subset." |
| 7 | "Autonomous full-run is dangerous" (M8 evidence) | **"Autonomous is safe *with the rigor-reviewer as a hard gate*"** | The M8 regression predates `check_probfig` + the reviewer, which were the fix; the 11–17 run carried them and caught real defects. |

**What did not change (preserved because it is right):** the A/B/C reframe; skill-builds-documents-not-a-course; M1/M2 below bar with the specific audit debts; the named M3–M5 domain fixes; the entire skill-gaps list (§5.1–5.9, 5.11–5.12); the operational risk factors; the phased plan; the go/no-go structure; the per-module "at bar" success criteria; and the "encode-as-check opportunities already shipped" table.

---

*End of revised assessment. This revision was written by Claude with first-hand knowledge of the Modules 11–17 build; it corrects five scan-only inferences in the Grok v1 and preserves its (correct) thesis, plan, and skill-gap analysis. No modules were modified; `/rigorous-explainer` was not run. The v1 document is unchanged at `rigorous-explainer-feasibility-assessment.md`.*
