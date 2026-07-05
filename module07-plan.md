# Module 7 — Standing, Posture, and Load Bearing (build plan)

**One-line thesis.** Standing upright is an *unstable* equilibrium; it exists only
because a delayed feedback controller actively holds it. Module 7 is where the course
turns from open-loop tissue/torque mechanics (Modules 1–6) into **closed-loop
neural control** — repaying Module 5's IOU on reflexes, spindles, and co-contraction.

## The building spine (each section needs the previous)

| § | Title | Uses | Headline / boxed result |
|---|-------|------|--------------------------|
| 0 | **Why standing is not passive** (motivation) | — | Under anaesthesia the body collapses; a skeleton can't stand. COM sits above the ankle → gravity topples it → posture is *actively defended*. Preview the inverted-pendulum-with-delayed-controller punchline: sway is the controller's signature. |
| 1 | **The standing body: base of support, COM, and the static margin** | M1 (COM, torque), M3 (foot joints) | Foot tripod → base-of-support (BoS) polygon. COM. **Static balance condition:** vertical COM projection ∈ BoS (necessary, *not sufficient*). Introduce the **dynamic** upgrade to come: the extrapolated COM (XcoM = COM + v/ω₀, Hof) as the hinge into §3–4. |
| 2 | **Ground reaction force and center of pressure** | §1 | GRF as the resultant of the pressure field; **COP = ∫r·p dA / ∫p dA** (boxed def), the force-plate observable. Geometric/force definition only here — the *dynamic* COP–COM relationship is a consequence of §3's EOM, so it is deferred to §3 (dependency order). |
| 3 | **Dynamics of the inverted pendulum** | §2 | Single-segment body about the ankle: **I θ̈ = m g ℓ sinθ − τ_ankle** (boxed, proved from Newton–Euler). Derive the dynamic **COP−COM ∝ −θ̈** relationship here (COP leads COM; it is the controller's handle). |
| 4 | **Linearization around upright — the instability** | §3 | Small-angle: **θ̈ = ω₀² θ − τ/I**, ω₀²=mgℓ/I. Eigenvalues **±ω₀** → one positive real root → *inherently unstable*. Compute the toppling time constant 1/ω₀ (~ hundreds of ms). This is "balancing a broom." |
| 5 | **Ankle strategy: PD control of ankle torque** | §4 | Proprioceptive feedback → **τ = K_p θ + K_d θ̇** (spindle senses length∝angle ⇒ P, its rate ⇒ D — biology *gives* the PD law, not engineering fiat). Closed-loop char. eqn; **stability requires K_p > mgℓ** (active stiffness must beat gravitational toppling stiffness) + K_d>0. Root-locus figure. |
| 6 | **The delay problem — why we sway** (crown jewel; **full rigor, user-requested**) | §5 | Neural delay Δ≈150–200 ms → **τ = K_p θ(t−Δ) + K_d θ̇(t−Δ)**, a delay-differential equation. Full treatment: characteristic quasi-polynomial with e^{−sΔ} (transcendental, ∞ roots); **D-subdivision / Stépán method** for the stability chart; derive the critical-delay boundary (Hopf) where a conjugate pair crosses the imaginary axis, giving the sway frequency ω_c; map the full stable region in (K_p, K_d) at fixed Δ. Too-high gain × delay → limit-cycle. **Postural sway = a delayed controller operating near its margin.** |
| 7 | **When the ankle isn't enough: hip strategy, co-contraction, knee lock** | §5–6 | COP can't leave the BoS ⇒ ankle torque saturates at (foot length)×(body weight). CNS switches to **hip strategy** (counter-rotation, two-segment). **Co-contraction** raises effective K_p at a metabolic cost (repays M5's co-contraction/redundancy IOU: agonist–antagonist stiffening *is* a redundancy resolution). **Knee locking** = passive removal of a DOF. |
| 8 | **Load bearing: the equilibrium the controller defends, and its spinal cost** | §3–4, M1 §6 | *Bridge:* a forward lean / holding a load is a **shifted equilibrium the same controller must hold** — and defending it *costs the spine*. Trunk-as-lever static analysis: erector-spinae short moment arm (~0.05 m) vs long load arm → **L5/S1 compression of several kN** (must reproduce/extend Module 1 §6: torque 100–400 N·m, "several thousand N"). |
| 9 | **Computational labs** | §6, §8 | (1) **Quiet standing with perturbations** — integrate the delayed-PD inverted pendulum; show sway, and the instability when (gain×delay) crosses the §6 boundary; recover COP trace. (2) **Forward lean & low-back torque** — L5/S1 compression vs lean angle and held load. |
| 10 | **30-problem set + diagnostics + what-it-captures/misses + repayment table** | all | C1–C10 / D1–D10 / K1–K10 (K's = simulation / stability-boundary root-find / inverse-problem / sensitivity sweep, MIT-PhD level), 5 diagnostics, limitations, IOU ledger → Modules 8/9/12. |
| A | **Appendix** | — | Grouped notation table + parameter table (anthropometrics, gains, delay), each linked to its section. |

## Decisions locked (from advisor review)
1. **Two-theme bridge resolved:** §8 "Load Bearing" is *not* a statics bolt-on — it is
   framed as the shifted equilibrium the §3–7 controller defends, with L5/S1 compression as
   the *cost* of defending it. Keeps Pillar 2 (one spine).
2. **Cross-module L5/S1 consistency:** §8 explicitly cites **Module 1 §6** and reproduces its
   parameters (erector arm ~0.05 m, load arm ≤0.4 m, compression "several thousand N",
   torque 100–400 N·m). The single-leg 1715 N hip reaction (M2 §2 / M3 §4) is *not* re-derived
   here — cite if referenced. If the audit-backlog "M1 low-back number" turns out wrong, fix both.
3. **Module 5 IOU ledger:** M7 **repays** reflexes + spindles + closed-loop control (§5–6) and
   **co-contraction** (§7, as a redundancy resolution). The full **whole-limb redundancy /
   cost-function debate is forwarded to Module 12** (as M5 already hedged). §10 repayment table
   states repaid-here vs forwarded-onward explicitly.
4. **Enrichments folded in:** XcoM / margin-of-stability (Hof) as the §1→§3 hinge; spindle→P+D
   mapping in §5 (turns "PD" from engineering choice into biological consequence).

## Forward-references this module must satisfy
- **Module 5** (only module with M7 IOUs): "reflexes, muscle spindles, closed-loop control,
  co-contraction strategy" → §5–§7. "Redundancy / cost-function debate → M7, M12" → co-contraction
  piece in §7; whole-limb piece forwarded to M12 (state in §10 table).

## New forward-references this module will *create* (span, no href, autolinked later)
- **Module 8** (walking) — the inverted pendulum in motion; step-to-step transition; COP trajectory.
- **Module 9** (running/jumping) — SLIP / spring-mass, impact loading.
- **Module 12** (whole-limb) — the full muscle-redundancy / cost-function problem.

## Figure families (get ONE representative approved per family before mass-producing)
- **Tier-2 whole-body postural figures** (standing skeleton/body with COM, BoS, GRF, COP; ankle
  vs hip strategy; forward-lean spine lever) — reuse the posable-body + shaded-capsule pattern.
- **Flat/schematic physics**: FBD of the inverted pendulum; root-locus & delay stability-boundary
  plots; COP–COM time traces; L5/S1 free-body.
- **SMIL animations**: the sway limit cycle (near the stability margin); ankle→hip strategy switch.
- All computed in Python (scratchpad, background runs); slim arrows only; shared `<defs>` block.

## Build order & process (per CLAUDE.md)
Leaner way — prose authored directly in `module07.html`, Python for figures only (splice via
`<!--FIG:key-->` markers). Section-by-section: build one → report + 2 ★ Insights → user reviews →
commit only on "commit push." Full hardening loop after every edit. Publish-while-incomplete:
link in `index.html` + `README.md` marked *(in progress)* on first commit.
