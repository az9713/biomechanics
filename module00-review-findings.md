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

## Appendix (rA) — first partial list, SUPERSEDED by the final-numbering section below
F1 Nernst row E -> E_Nernst + notation row. F2 [Ca]_SR row §5 -> §3. F3 add withdrawn-claims row; remove 108 as ceiling at body ~560 and ~157. F4 add OSF row; "Two entries" -> "Three entries". F5 Prop 5.3 "proved given van 't Hoff (imported)". F6 Props 3.3/3.4 transformed convention imported (Alberty, Def 3.4). F7 add 9 omitted proved results (Lemma 1.1, Prop 1.1, 1.2, Lemma 2.1, Prop 3.2, Cor 3.1, Lemma 4.1, Prop 4.2, Lemma 5.1). F8 CLOSED. F9 split k_pair / k_bond rows. F10 permeability kappa -> k of Module 4 §3. F11 wrong section pointers: ell_c (§4, §9 not §8), rho (not in §7), S_t... (truncated).

## TO APPLY — Appendix (rA, FINAL numbering from the resend; supersedes the partial list above)
- F1 Nernst row: write `$E_{\text{Nernst}} = (R_gT/zF)\ln(c_{\text{out}}/c_{\text{in}})$`; add Water notation row `$E_{\text{Nernst}}$ | equilibrium membrane potential (§5 Prop 5.2) | Young's modulus $E$; activation energy $E_a$` (body 1038 already writes E_Nernst).
- F2 row `[Ca2+]_SR | 1 mM free` cites §5; its marker and 41.29/47.50/49.59 are at ~750 in §3 -> `href="#thermo">§3`.
- F3 register has no withdrawn status: add row `withdrawn claims | 3 | §9 — §0's calibrated ladder; entropic collagen; the 108 MPa ceiling, replaced by the Gaussian-valid 2.2–3.6 MPa (§4)`; body ~560 "$108\ \mathrm{MPa}$ at the physical limit" and ~157 "at most $108$" still read as ceilings.
- F4 no row for OSF (box ~1148, flagged ~1152 as outside its regime; "Onsager–Samaras" has 0 matches — the flagged case is OSF): add `electrostatic persistence length | $\ell_{\text{OSF}} = \ell_B\lambda_D^2/4A^2$ | §5 — quoted, not derived; $\lambda_D \gg A$ fails at plasma strength; an upper bound here`; "Two entries" -> "Three entries".
- F5 Donnan row "Prop 5.3 — proved; van 't Hoff invoked at 0.28 M" -> `§5 Prop 5.3 — proved given van 't Hoff's law (imported, ~1086); applied at $0.28\ \mathrm M$, which is not dilute (≈7% high)`.
- F6 rows Prop 3.3 / Prop 3.4 "proved": append `; the transformed-convention form is imported (Alberty, Def 3.4)`.
- F7 register omits 9 proved results: Lemma 1.1, Prop 1.1, Prop 1.2, Lemma 2.1, Prop 3.2, Corollary 3.1, Lemma 4.1, Prop 4.2, Lemma 5.1 -> one row each, "proved".
- F8 split row `$k_{\text{pair}}$, $k_{\text{bond}}$` into `$k_{\text{pair}}$ | Born-pair curvature, N m⁻¹ (§2 Lem 2.1)` and `$k_{\text{bond}}$, effective $k$ | §0 bond stiffness; the calibrated 25 / 0.30 N m⁻¹ were withdrawn (§9)`.
- F9 row κ collision "a permeability $\kappa$" -> `the permeability $k$ of Module 4 §3; a curvature` (body 137 writes Module 4's permeability as k); add that k to the k_pair row's collisions.
- F10 pointers: L_c row "§8 uses $\ell_c$" -> "§4 uses $\ell_c$ for crosslink spacing"; ρ row "mass density in §4 and §7" -> "mass density in §4"; S row "$S_{\text{tot}}$ ... in §8" -> "in §6 and §8".
- F11 c_F row "predicted by §7 from a GAG assay; varies 0.25 to under 0.1 M" -> `§5; §7 traces it to a GAG assay (40–70 mg/mL → 0.175–0.306 M); falls under 0.1 M with depth, age and disease, and $\Pi$ is roughly linear in it`. (Check "roughly linear": r7#1 shows halving c_F gives a 73% loss — NOT linear; word it from Prop 5.3.)
- F12 ℓp row "§9 K3 shows salt explains part of that spread" -> "§9 K3 makes salt a quantitative candidate for part of that spread".
- F13 [uncertain] ε_r water 73.2 at 37 °C: Malmberg–Maryott gives 74.15 at 37 °C (73.2 ≈ 40 °C). Cite a source in the ~974 marker; if 74.2, rerun ℓ_B (0.736 -> 0.727 nm), λ_D, 12.3 k_BT. VERIFY with a script before changing.
- F14 parameter table missing rows: buffer set ~1133 (24 mM bicarbonate, 1 mM P_i, 8 mM histidine, three pKa); fatigued ATP/ADP/P_i ~702–704 (5.0 mM, 70 μM, 15 mM); K7 pump K_M = 0.5 μM, release 135 μM, τ = 4 ms -> rows "measured" + caveat.
- F15 k_pair Ca–O row -> `§2 Lem 2.1 — from $z$, $r_0 = 0.240$ nm and Pauling's $n = 8$, itself fixed on alkali-halide compressibilities`.
- F16 notation rows missing: σ (stress ~107; σ_N SD ~349; LJ diameter ~543) -> `$\sigma$, $\sigma_N$ | stress; SD of a count (Prop 1.2); LJ collision diameter (§2) | each other`; also γ_i (~1015), M_s, c_site, u_0 (~276), ℓ_p^0 (~1146), 𝓑 (~451), 𝖠,𝖡,𝖣 and 𝐮 (~433), D-period (~560).
- F17 row `$x$, $R$` collisions: append "; §9 K7's released amount $R$" (or rename per r9k#17 to Δc_rel and skip this); add row `$\tau$ | release time constant (§9 K7) | shear stress $\tau$ (Module 2)`.
- F18 row `$n$, $c$, $n_V$` meaning -> `amount of substance ($n$ in §1 only; $N_i$ from §3 on), molar concentration, number density`.
- F19 Q10 row -> `$2.5$ over $25$–$35\ ^\circ\mathrm C$, giving $E_a = 70.0\ \mathrm{kJ\,mol^{-1}}$` (at 310.15/320.15 K the same Q10 gives 75.6).
- Lower: constants header "value at T = 310.15 K" over T-independent constants; F_faraday row never used in body; μ_i row lists Poisson's ν as a collision.

## TO APPLY — §7 (r7 11–22)
- 11 ~1376 "The charge separated is $Q = (C/A)\,V\,A$, and dividing by the elementary charge gives the ion count:" -> "Using the measured $1\ \mu\mathrm{F\,cm^{-2}}$ (the $0.78$ estimate gives $6.2$ ppm), the charge separated is ..." (4.41e7 ions at 1.0; 3.44e7 at 0.78).
- 12 ~1318 "Collagen is the one protein in this course whose mechanics the module has computed, and its architecture is unusually rigid and unusually easy to state." -> "Collagen is the protein whose mechanics this module has computed in most detail, and its architecture is unusually rigid and simple to state." (§4 derived elastin).
- 13 ~1360 "is false, and an earlier draft of this section's verification script asserted it and failed." -> "is false: cysteine, 0.9 units from 7.4, is closer than histidine at 1.4."
- 14 ~1360 "By §5 Definition 5.4 a buffer contributes capacity only within about 1.5 units of its own pKa, so at pH 7.4" -> "By §5 Lemma 5.1 a buffer's capacity 1.5 units from its $\mathrm{p}K_a$ is $12\%$ of its peak, so at pH $7.4$". NOTE: fix9cd.py already changed "Definition 5.4" to "Lemma 5.1" here; apply the rest of the wording.
- 15 ~1372 keyresult "C/A = \epsilon_0\epsilon_r/d" and ~1376 "Q = (C/A) V A": undefined, and A, V, Q collide (Helmholtz A, §5 spacing A, Arrhenius A; V volume; Q quotient) -> $C_m/A_m = \epsilon_0\epsilon_r/d_{\text{hc}}$, $Q_m = (C_m/A_m)\,|E|\,A_m$, with "where $C_m$ is membrane capacitance, $A_m = 4\pi r^2$ its area, $d_{\text{hc}}$ the hydrocarbon thickness, $|E|$ the magnitude of §5's membrane potential, and $Q_m$ the separated charge"; "dielectric constant" (~1374, ~1394) -> "relative permittivity". Add Appendix rows.
- 16 ~1345/1347 "c_F = 2m/M_{\text{disacc}} = 2m/458": m collides with Prop 3.5's m -> $m_{\text{GAG}}$, $M_{m,\text{disacc}}$ in keyresult and surrounding prose; Appendix rows.
- 17 ~1310 Def 7.1 "a side chain $\mathrm R$, all on one carbon." -> add "(in proline the amino nitrogen bonds back into the side chain, closing a ring)"; gloss "hyaluronan, a very long unsulfated GAG" (~1343), "disulfide bonds, S–S links between two cysteines" (~1362), "carbonyl (the C=O group)" (~1312); also "lone pair", "amide", "X-ray fibre diffraction" (~1337).
- 18 ~1360 pKa list inline, four paragraphs no visual -> table: residue / free pKa / |7.4−pKa| / capacity factor 4r/(1+r)² / % of residues (His 6.0 / 1.4 / 0.15 / 2.3; Cys 8.3 / 0.9 / 0.40 / 1.4). Compute all rows in a script.
- 19 ~1314 "is unaffected by a $20\%$ change in a quantity it was using to show a factor of ten was impossible." -> "is unaffected by a $10\%$ change either way, because it misses a physical chain by a factor of ten."; delete "and its test is not whether the pictures are pretty" (~1306), "The glycine is not decoration and its position is not arbitrary." (~1322), "is not a fudge: it" (~1330; new reading "The $10\ \mathrm{nm}$ discrepancy is the telopeptides").
- 20 ~1394 "Two of those predictions land within a few per cent, one lands inside a measured range, and one &#8212; the capacitance &#8212; lands within $30\%$ and says where the rest is." -> "One prediction lands within $1\%$ (glycine), one matches by construction (the contour length), one lands inside a measured range, and one, the capacitance, lands $22\%$ below measurement."; ~1396 "every tissue property this course computes is a product of one of each." -> "most tissue properties this course computes, such as $c_F$, are a product of one of each."
- 21 ~1368 "so about $3.1\times10^{6}$ lipids per square micrometre of membrane." -> "so about $1.5\times10^{6}$ lipids per leaflet, or $3.1\times10^{6}$ per square micrometre of bilayer."
- 22 ~1353 caption "which is why <a ... module04.html#donnan>Module 4</a> treats GAG loss as the initiating event rather than a consequence." -> covered by finding 1 (use module04.html#degeneration, "starts its degeneration loop at GAG loss").

## TO APPLY — §8 (r8 16–21)
- 16 ~1556 "Terms 2 and 3 both scale with $T$ and have opposite signs, so they do not cancel" (also code docstring ~1572) -> "Terms 2 and 3 scale with $T$ with opposite signs and unequal sizes. Per $R_g$ per kelvin, $2\ln(10^4) = 18.4$ against $|\ln Q| = 8.47$ plus $\Delta S^{\circ\prime}/R_g = 4.03$, so the climb should dominate by $5.9$. The lab settles it." (Changing the docstring changes the listing: re-run it and check_code.)
- 17 ~1673 "Cooling makes the pump <em>thermodynamically more comfortable</em> and <em>kinetically crippled</em>." -> "Cooling makes the margin more favourable by $1.33\ \mathrm{kJ\,mol^{-1}}$ and every rate $13.3$ times slower."; "the $4.13\ \mathrm{kJ\,mol^{-1}}$ that buys beats the $2.81$ lost from ATP" -> "the $4.13\ \mathrm{kJ\,mol^{-1}}$ saved on the climb exceeds the $2.81$ lost from ATP".
- 18 ~1675 "Two mechanisms that produce the same symptom &#8212; slow relaxation &#8212; and only one of them is thermodynamic." -> "Two mechanisms produce the same symptom, slow relaxation, and only one of them has a thermodynamic part."
- 19 ~1537 "A model that made that substitution would predict a twitch where there is almost none." -> "A model that made that substitution would predict $98\%$ occupancy where the equilibrium gives $5\%$."; "the fixed-ligand formula says the filament is fully activated and the truth is that it is five per cent activated" -> "the fixed-ligand formula gives $0.984$ occupancy and the equilibrium gives $0.051$".
- 20 ~1524 "Run it and the fixed-ligand formula turns out not to be a small correction away from the truth. It is wrong by almost the whole range of the dependent variable:" -> "Run it, and the fixed-ligand formula is not a small correction: its occupancy is wrong by up to $0.93$ of the $0$-to-$1$ range:"
- 21 (low) ~1404 after the quoted "that assumption is badly violated" add "&#8212; a half-sarcomere with $70\ \mu\mathrm M$ of sites holds about $45\,000$ of them against those $64$ ions." (70e-6 × 1.06e-15 × 6.022e23 ≈ 44,700.)

## TO APPLY — K problems (r9k 11–20)
- 11 K2 integrates nothing (Pi linear in t, ADP algebraic): "[ATP] falling only from 5.5 to 5.0 mM" has no schedule, "halving it doubles the crossing time" asserted. Deepen: state [ATP](t); Pi as an ODE with PCr/creatine-kinase buffering, or sweep the Pi rate and plot crossing time. (Combine with r9k#1 exponent fix.)
- 12 K6 unsolvable: "You are given four measured rates" but none given -> add "$k/k_{37} = 0.0796,\ 0.197,\ 0.556,\ 0.970$"; "Individual rate measurements carrying up to $6\%$ scatter produce a cooling prediction good to $2\%$" rests on one noise draw (Appendix row "K6 shows a two-point Q10 is five times less accurate" repeats it; kcheck: 4.54x) -> Monte Carlo 10^4 draws at σ = 4%, report both error distributions.
- 13 K3: ℓ_OSF ∝ 1/I exactly, thresholds are a ratio not a bisection; "The threshold is therefore sharp in a useful way &#8212; there is no broad crossover to worry about." -> "The dependence is a power law, so there is no threshold; each tenfold dilution makes the term tenfold larger."; "already $10\%$ electrostatic" -> "already $9\%$ electrostatic" (1.45/15.95). Deepen: sweep A over 0.4–3 nm.
- 14 ~1904 "Answers are quoted from code that runs; the numbers below are reproducible, not illustrative." but no K solution shows code -> add PEP8 listings, or "Each solution states its method, inputs and step size, so each number can be recomputed."
- 15 Fig 27 (K4) steps drawn at half-decade midpoints between five samples; true steps working 10^2.22, 10^2.96, 10^4.44; rest 10^2.10, 10^2.63, 10^3.51, 10^5.26; omits rest level 4 and working level 3; no marker at 2.8e4 -> dense log grid + marker.
- 16 K4 "which real pumps do not do, because the stoichiometry is built into the protein" and caption "which no protein can do" asserted (SERCA slippage lowers effective ratio under load); "picking for the worst case is what the reticulum pump appears to have done" is a design inference -> "Two binding sites fix the nominal ratio at two; under a steep gradient slippage lowers the effective ratio below two."
- 17 K7 symbols: "$J_{\text{in}} = (R/\tau)e^{-t/\tau}$ with $R = 135\ \mu\mathrm M$" -> $\Delta c_{\text{rel}}$; "($K = 1\ \mu\mathrm M$, $n_H = 3$)" -> $K_{1/2}$ (CHECK: fix6 did not touch K7's K); define $J_{\text{out}} = v_{\max}c/(K_M+c)$ and $S_{\text{tot}} = 70\ \mu\mathrm M$.
- 18 K1, K3, K6, K8, K9, K10 have no figure (only K2, K4, K5, K7 = FIG26–29) -> computed plots: K1 fitted n vs Pauling n; K3 ℓ_OSF vs I log–log; K6 Arrhenius fit + two-point line; K8 E vs M_c with N≥10 cut; K9 θ(c) n_H = 1,2,3 vs spec box; K10 ATP/work bars.
- 19 K10 "energy at $52.74$" prices a twitch at the fatigued ΔG (at rest 62.52: 24.9 mJ, 30.1%); "against §1's $8.30\times10^{-20}$ J per ATP is $60\%$" mixes values (57% at 52.74); delete "and why the reticulum pump is the largest single ATP consumer in a resting muscle"; state which ΔG and report both.
- 20 K4 "$n_{\max}$" collides with Born n; §3 Prop 3.5 uses m -> $m_{\max}$.
- Minor: K5 calls plasma bicarbonate/pH 7.40 "intracellular" (cytosolic pH 7.1 gives a 38% penalty); K8 110 vs 100 g/mol per residue.

## kcheck — COMPLETE (all numbers above; nothing pending)
Matches everywhere except: K7 (unconverged Euler: 8.817 μM and 7.98 converged; Euler dt 20/10/5/1/0.2 μs = 10.078/9.208/8.980/8.847/8.823; peak at 7.13 ms released 112.3, bound 69.9, pumped 33.7, free 8.8), K9 (2.16x), Diagnostic 1 (9.55e-3, APPLIED), K2 input conflict, K1 MgO premise. Minor rounding: K6 9.55%, Appendix 4.54x, K4 2.76e4, K5 7.44x, K2 51.2 vs 52.4 s, K8 110 g/mol and "108 MPa at one residue" vs 0.9.

## STATUS
All reviewer batches received (every agent sent DONE). Nothing is held in agents.
