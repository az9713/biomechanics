# Module 0 §6–§9 + Appendix reviewer pass — findings ledger (2026-09-15)

Reviewers (Opus 5 overrides; `model: fable` in the agent file failed at the Fable limit):
r6 (§6), r7 (§7), r8 (§8), r9c (§9 prose+diag+C), r9d (§9 D), r9k (§9 K), rA (Appendix), kcheck (K numbers, shell).
Line numbers are PRE-edit. Appliers: scratchpad `fix6.py` (APPLIED), `fix9cd.py` (APPLIED).

## APPLIED
- r6 1–21 (fix6.py). Hill K -> K_{1/2} everywhere (Def 6.2, Lab 8A math + fig24 text, Appendix rows, D7). r9d#19/r8#14/rA#8 therefore CLOSED.
- r9c 1–9, r9d 1–9 (fix9cd.py). D6 rewritten (water ions; Lemma 5.1 within 10% for pH 4.34–8.56). D7 rewritten (n_H <= 1.908/log10 rho; rho=3 -> 4.0; K9 bound 2.0).
  Lemma 5.1 citation sweep: C5 x2, lines 1127, 1137, 1360, 1983.
- Also applied for consistency: line 9 (16% is products), Diagnostic 2 (2.6%, 20–30% isometric), C6 (ATP share 0.25 kJ).

## TO APPLY — §9 (r9c 10–20, r9d 10–18)
- r9c10 Diag 5: "computes the free energy of a Ca&#8211;O bond in bone as" -> "computes the Coulomb attraction of a Ca&#8211;O pair in bone as"; "Dissolution is slow for kinetic and surface reasons, not because the bond is thermally unreachable." -> "Whether mineral dissolves is set by the free energy of dissolution at the fluid's composition (§3 Proposition 3.3), not by one pair energy in vacuum." (898 kBT is Coulomb alone; Born well 786, §5 ~976)
- r9c11 C7: "Both steps assume many ions within the region over which the potential varies, so that an average is meaningful;" -> "The first step assumes many ions within a screening length, and the second assumes $|ze\phi|\ll k_BT$, which fails because $\ell_B = 0.74\ \mathrm{nm}$ is close to $\lambda_D$;" ; delete ", which is well confirmed".
- r9c12 line 9: "every gated parameter in this module declares ... &#8212; and that discipline caught three errors that no other check would have." -> "every constitutive parameter ... measured, and that declaration exposed §0's circular stiffness ladder."
- r9c13 C10: define gate "(a script run on the document before publication)"; last sentence -> "The checks in this build test form (a declaration exists, delimiters balance); none of the three errors was an error of form."
- r9c14 "and every tissue property computed here is a product of one of each." -> "and tissue-level properties such as cartilage's swelling pressure (a GAG assay times a stoichiometry) are a product of one of each."
- r9c15 C8: "a calculation of the kind §2 Proposition 2.1 shows requires the full internal-coordinate problem." -> "and by §2 Proposition 2.1 any estimate that freezes the strands' relative motion is only an upper bound on $\kappa$; the true value needs the relaxed internal coordinates."
- r9c16 C9 last: "The bound and the measurement agree." -> "Both arguments reach the same conclusion: collagen's stiffness is not entropic."
- r9c17 crowding: "by factors of several" -> "by an amount this module does not estimate"; source the 20–30% (Ellis 2001, volume occupancy) or delete.
- r9c18 pattern sentence -> "the error sat in a step asserted beside a computation (a table value's source, a mechanism's attribution, a hypothesis's scope), not in the computation itself."
- r9c19 "Rather than leave these in the version history, they belong here, because each is a lesson about how the errors were found." -> "They belong here rather than only in the version history, because each shows how an error was found."; "Eight sections have built" -> "Nine sections have built"; ", which is worth stating plainly rather than leaving in the commit history." -> ", and this section states them plainly."
- r9c20 "What it captures" 7 results -> table (result | value | inputs | section) + lead-in; "Each has a one-line answer" -> "Each has a short answer".
- r9d10 Lemma 5.1 proof (~1122) "C_b = [A-] up to a constant": add neglect of free H+/OH- (valid pH 4.34–8.56 at 24 mM per D6).
- r9d11 D2 statement "Proposition 3.3" -> "Proposition 3.4 and Definition 3.1" (CHECK Def 3.1 is dG=dH-TdS).
- r9d12 D1 -> CsCl lattice (alpha_M 1.7627, V_f=(2r0/sqrt3)^3 = 1.5396 r0^3 -> denominator 13.86 r0^4); CHECK §2 ~452/468 gamma_s definition.
- r9d13 D8 "The two coincide exactly when $k_2 \ll k_{-1}$" -> "The two coincide in the limit $k_2 \ll k_{-1}$, and the gap $K_M - K_d = k_2/k_1$ holds exactly at all rates."
- r9d14 D4 — already covered by my rewrite.
- r9d15 D3 last sentence -> FJC correction second order; Marko–Siggia first order ~(x/Lc)/2; §4 fig loses 10% at 0.17 (checked: 11%).
- r9d16 D1 "packing factor" -> "structure constant" (2 places).
- r9d17 D10 n_sep/n_K -> N_sep/N_K. r9d18 D10 V -> E_m; c_K = 140 mM from §7's table.

## TO APPLY — K problems (r9k 1–10 so far; kcheck)
- K2 (r9k1, kcheck5): ADP ∝ Pi^1.35 gives 201 uM ADP vs §3's 70 uM; §3 end ceiling 8.76 pN. Use §3 end composition (exponent ~0.836): end 8.76 pN, 9 pN crossing -> 42.4 s. Recompute 16 s, Fig 26. Delete "Second, the trajectory ends at 8.30 pN ... than §1 made."
- K1 (r9k2, kcheck6): MgO Pauling n = 7 (§2 ~403, ~483; 273 GPa); CaO 5.14 not below 5; say "§2 inverted route B; this inverts route A". K-depth r9k9: equation linear in n; deepen (Born–Mayer exp repulsion / polarizability fit across 4 crystals) or cut; delete "hand-waved".
- K7 (r9k3,4,5; kcheck1,2): Euler dt=20 us unconverged: converged peak 8.82 uM, factor 7.98 (not 10.08, 7.0); c0, bound0, integrator, leak unstated; floor below 0.1 uM after ~24/33 ms; "check not input" circular (R=135 chosen); "more than half free or pumped" false (38% of released-by-peak; bound 63%); "fixed buffer ratio wrong in opposite directions" asserted. Fig 29 caption ~2032.
- K9 (r9k6, kcheck3): "could triple" -> 2.2-fold (0.216 uM); closed form n*=log10 99=1.996 -> plug-in; deepen: fit n_H, K to noisy force–pCa data.
- K10 (r9k7): plug-in; deepen: ion count from K7 pumped Ca x volume, strokes from duty ratio; twitch vs 1 s tetanus.
- K8 (r9k8): repeats §4; "roughly ten Kuhn segments" -> "five to nine"; residue mass 110 vs §4 "about 100"; "108 MPa at one residue" vs table 0.9; deepen: sweep b 1–2 nm, N_min 5–20.
- K4 (r9k10): floor at 5 points, 2.8e4 already in §3; deepen: slippage/leak sweep or feasibility along K2 trajectory.
- Minor rounding (kcheck): K6 "about 9%" = 9.55%; Appendix "five times" = 4.54x; K4 2.8e4 = 2.76e4; K5 "seven times" = 7.44x; K2 "doubles" 51.2 vs 52.4 s.

## TO APPLY — §8 (r8 1–15 so far)
1 "Neither problem has a closed form": Lab 8B margin(T) is linear, slope +49.2 J/mol/K, zero at 416 K (143 C); restrict "no closed form" (also h2) to 8A; deepen 8B.
2 "never comes near stalling" vs §3 ~777 "close enough to stall" (same -5.2 state, fatigued column). "in a working muscle" -> "at the end of a fatiguing bout"; replace claim with margin-stays-negative wording.
3 "no closed form for n_H=3 — quartic" false; half occupancy exactly c_tot = K + S_tot/2 = 36.0 uM; table 36.3 -> 36.0.
4 "the left side is strictly increasing" -> right side; negative cooperativity claim false.
5 "differ by a factor of four at rest" unsupported; 0.1 uM is FREE in §1; total needed 0.17 uM (factor 1.7).
6 "fixed ligand (§6)"/"fits Proposition 6.2"/caption/~1686/Appendix ~2246: dashed curve is Def 6.2 under Prop 6.2's ligand-in-excess hypothesis.
7 after S_tot sentence: lab uses force–calcium Hill curve as binding curve; 0.93 gap depends on n_H=3; half-point holds any n_H.
8 S_tot = 70 uM: no source/prov/table row; add prov (data-sym must be canonical! check GATED) + table row.
9 "will report it with a good fit, because the depleted curve is still sigmoid": compute fit (K_app, n_app, residual) or delete.
10 "Neither §3 nor §6 alone could have found that" -> "§3 alone gives the sign...; the contrast with §6 needed both"; climb coefficient 2Rg ln r = 153 vs |−dS + Rg lnQ| = 104.
11 before "Three temperature-dependent terms": state Q and ratio fixed at §3 fatigued values, dCp=0 over 27 K, pump given crossbridge Ea; 13.3x ~ order of magnitude.
12 "kinetic in one case and partly thermodynamic in the other" -> add "by §3's ledger".
13 "a margin of −5.24" undefined -> "a net free energy ΔG_net (Prop 3.5, m=2; below, the margin, negative when the pump can run) of"; add kJ/mol to table header.
14 CLOSED (K_{1/2}).
15 c_SR, c_cyt undefined -> [Ca2+]_SR/[Ca2+]_cyt; gloss troponin C.

## TO APPLY — §7 (r7 1–10 so far)
1 Fig 22 caption: half GAG -> Π 156 -> 42 kPa (73% loss); href #donnan -> module04.html#degeneration (Module 4 §8).
2 +10 nm telopeptides not derived: box 290 nm derived; "remaining 10 nm is the measured length of the non-helical telopeptides"; delete marker's second explanation; Appendix L_c row.
3 "roughly 16x" abundance only; with placement His@6.0 vs Cys@8.3 = 6x; His@7.3 = 41x; cytosolic Cys mostly free thiols.
4 burial LOWERS histidine pKa; rise to 7.3 needs neighbouring negative charge.
5 "The pumps of §3 are not restoring the potential..." false debt (Na/K pump not in module) -> replacement given.
6 c_F "predicts" -> "consistent with"; reconcile ranges 0.175–0.306 vs "0.25 to under 0.1"; (Module 4 marker "module0" — KEEP: state names source module, judged correct).
7 GAG m basis: per litre interstitial water vs §5 wet weight; 40–70 mg/mL needs source/marker.
8 Def 7.3 keratan sulfate: 2m/458 is an upper bound for adult cartilage.
9 "unchanged to five decimal places"/"thousands of times": sodium ~1e-4 per AP; replacement given.
10 C/A discrepancy: head-group in series LOWERS C; replacement given.

## TO APPLY — Appendix (rA F1–F11 partial)
F1 Nernst row E -> E_Nernst + notation row. F2 [Ca]_SR row §5 -> §3. F3 add withdrawn-claims row; remove 108 as ceiling at body ~560 and ~157. F4 add OSF row; "Two entries" -> "Three entries". F5 Prop 5.3 "proved given van 't Hoff (imported)". F6 Props 3.3/3.4 transformed convention imported (Alberty, Def 3.4). F7 add 9 omitted proved results (Lemma 1.1, Prop 1.1, 1.2, Lemma 2.1, Prop 3.2, Cor 3.1, Lemma 4.1, Prop 4.2, Lemma 5.1). F8 CLOSED. F9 split k_pair / k_bond rows. F10 permeability kappa -> k of Module 4 §3. F11 wrong section pointers: ell_c (§4, §9 not §8), rho (not in §7), S_t... (truncated).

## PENDING BATCHES
r7 11–20 + 2 lower; r8 16–20; r9k 11–20; rA F6–F19 (batches 2–4).
