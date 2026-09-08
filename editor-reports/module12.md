# Editor report: module12.html (Whole-Body Coordination and Motor Control)

Editorial pass. Standard: the five-part rule of the `science-editor` skill, read against `EDITOR_DOMAIN.md`. Every location is `module12.html:LINE` (the pristine 598-line file). Every replacement is valid HTML with MathJax delimiters and uses only the box classes the stylesheet defines. The edit is applied to `edited/module12.html` by one re-runnable script, `apply.py` (session scratchpad, folder `m12/`), which asserts that every anchor occurs exactly once; `figgen.py` beside it recomputes the three figure bodies that had to be redrawn.

**How this report was produced, stated plainly.** The first agent on this module applied 76 edits and died before writing anything down; its findings are gone. Sections 2 to 5 below are therefore **reconstructed from the applied diff**, not transcribed from that agent's notes. Before writing a word I checked that the reconstruction is complete: `cp module12.html edited/module12.html && python apply.py` reproduces the delivered `edited/module12.html` byte for byte, so the tag list *is* the whole change set and nothing was hand-edited outside the script. Every one of those 76 edits was then re-verified rather than trusted. All fourteen Python blocks in the edited file were extracted and run, and every number the prose quotes beside them was diffed against the printed output; every `<polyline>` in every figure was decoded back into data by calibrating from the tick coordinates and inverting the mapping, then compared against the model the caption claims. That audit found six further defects, three of them in figures that had passed all nine gates. They are B11 to B16 below and are applied in the same script, bringing the total to 96 edits.

## 1. Verdict

Yes, after revision. A graduate reader with no biomechanics can learn from these pages why a body with more actuators than task constraints needs a selection principle, how minimum jerk, the LQR, impedance, internal models, and optimal feedback control each supply one, and why the last of them predicts the shape of motor variability rather than merely tolerating it. The derivational spine is genuinely sound: Lemma 2.1, Propositions 1.1, 3.1, 4.1, 5.1, 6.1, 6.2, 7.2, 8.1 and 8.2 all carry proofs of matching weight, `check_proofs.py` finds no asserted sibling, and the Euler-Poisson to minimum-jerk to 1.875 chain is the best-built passage in the module. What stopped the reader before this pass was elsewhere, and it was mostly arithmetic and notation rather than argument. Lab C computed the contact force against a *rigid* wall in prose and a *finite* one in code and reported a 25x ratio that is 23.9x, while its own script printed one number per controller and never the peak the figure drew. Three symbols carried two meanings each across sections: `K` was both the LQR gain and the oscillator coupling, `\tau` was both normalised movement time and the feedback delay, `\eta` was both the variational perturbation and the learning rate. The module promised three times that computational solutions quote numbers the code produces, and shipped ten K solutions with no code at all. Proposition 7.1 was stated as a paragraph of prose with a proof labelled "(Sketch)". The module never said where its models sit on the level ladder. Six empirical counts and ranges (7 joint degrees of freedom, ~50 muscles, motor units per muscle, 80-90 % VAF, 3-5 synergies, the 1.7-1.9 measured peak/mean ratio) were bare numbers in no table.

The second pass found the residue the first one left, and it is the more interesting half. **Two figures contradicted their own text.** K6's figure drew the minimum-jerk bell (peak 1.874 at $\tau=0.50$, matching minimum jerk to 0.002) inside a problem whose solution says in as many words that the answer is *not* minimum jerk but 1.736 at $\tau=0.68$. Lab B's second figure plotted a settling time that reaches 17.9 s on an axis whose top tick was 10 s, so 40 % of the curve was drawn outside the plot frame; the viewBox had been stretched to `6 -81 488 339` to keep `check_frame` quiet, and the figure's own `aria-label` said both quantities fall when only one does. K5's figure showed a 60-trial schematic peaking at 0.719 beside a solution reporting a 340-trial run peaking at 0.811. Two further numbers were simply wrong: K9's "the fourth adds 0.0003, a factor 250 drop" is 0.000564 and a factor 130, and K4's "all three converge with aftereffect $-1.000$" is $-0.996$ for $\eta=0.2$ in the run the code prints. And D9's solution still stated the Adler equation with `K` after Proposition 8.2 had been renamed to $\kappa$, so the module gave one law two symbols. All nine gates were green on every one of these.

## 2. Blocking defects

Ranked by severity: results that are wrong or unproved first, then figures that contradict their text, then symbol collisions, then unlabelled numbers, then missing scaffolding. **Each heading is named for its `apply.py` tag family, so a row of the change table in section 6 can be looked up directly here**; the headings are therefore not in numerical order. The first agent's tag sequence has no B3 or B4: whatever they were is either merged into B5 and B6 or was dropped before the apply, and cannot be recovered.

### B1. Lab C models a rigid wall in prose and a compliant one in code, and its stated 25x ratio is 23.9x  [B1a-B1g]

Location: `module12.html:315` (Parameters/Equations), `:317` (code), `:337` (figure and caption), `:339` (Interpretation), `:394-395` (C5 solution and its figure), `:559` (Appendix parameter row).

Quoted (line 315): "<b>Parameters.</b> wall at $0.10\ \mathrm{m}$, target $0.15\ \mathrm{m}$; impedance $K=200\ \mathrm{N/m}$, servo $K_p=5000\ \mathrm{N/m}$. <b>Equations.</b> $F=K(x_{\rm eq}-x)-D\dot x$."

Quoted (line 339): "the steady force they press with is $K(x_{\rm des}-x_{\rm wall})$: the impedance controller settles at $200\times0.05=10\ \mathrm{N}$, the stiff servo at $5000\times0.05=250\ \mathrm{N}$ - $25\times$ larger".

Quoted (line 337, caption): "The stiff position servo presses with ~250 N (K_p x overshoot), the impedance controller with only ~10 N - a 25x difference".

Four separate failures in one lab. (a) **Factual error.** The code gives the wall a finite stiffness `kw` and the prose does not; a controller of stiffness $K_c$ against a wall of stiffness $k_w$ settles at the series value $K_ck_w(x_{\rm des}-x_w)/(K_c+k_w)$, not $K_c(x_{\rm des}-x_w)$. Computed: 9.98 N and 238.10 N, a ratio of 23.9, not 25. The rigid-wall estimate is exact for the compliant controller and 5 % high for the stiff one, which is the physical point the section was reaching for and missed. (b) **Number class.** $k_w$ appeared nowhere: not in the Parameters line, not in the Appendix. (c) **The code printed the wrong thing.** `run()` returned one number per controller; the figure drew a peak of 388 N that no printed number named, and the caption's "~250 N" described neither the peak nor the settled value. (d) **The figure was drawn on a 300 N axis** with tick labels 150 and 300 while the servo trace reaches 388 N.

The applied fix rewrites all six places from one recomputation. Parameters now name $k_w=10^{5}\ \mathrm{N/m}$ and give the series formula; the code returns `(peak, settled)` and prints the closed-form prediction beside the simulation; the figure's y-axis is relabelled to 200/400 N and both polylines are regenerated from the trace; the caption, the Interpretation, C5's solution and the Appendix row all quote 9.98 / 238.10 N, peaks 21 / 388 N, ratios 23.9 and 18.6. Decoding the delivered polylines back into newtons reproduces the recomputed trace to 0.12 N over all 1200 points.

### B2. The module promises three times that computational solutions quote numbers the code produces, and ships ten solutions with no code  [B2a, B2b, K1-K10]

Location: `module12.html:373` and `:460` (the promises), `:464-501` (the ten K solutions).

Quoted (line 373): "Each carries a <em>Probes</em> note and a collapsible worked solution; computational solutions quote numbers the code produces."

Quoted (line 460): "not substitution into a boxed formula. Numbers quoted are those the code produces."

Missing part 5, the tie to something concrete, and a false claim besides. Not one of K1 to K10 carried a code block; the numbers in them were asserted. Where they could be checked they were mostly right and sometimes not: K9's VAF sequence was given as 0.785 / 0.951 / 0.998 against a computed 0.745 / 0.924 / 0.998, and K7's ratio as 6.4 against a computed 6.39. This is the module's own house standard (`EDITOR_DOMAIN.md`: "K solutions carry Python-verified numbers with code") and it was not met.

The applied fix rewrites all ten solutions around a standalone, copy-buttoned Python block and quotes only numbers that block prints. Each rewrite also deepens the problem where it had drifted toward substitution: K3 now searches two inverse-kinematics branches and sweeps the co-contraction split at a fixed budget (posture buys a factor 5.0 in the along/across stiffness ratio, co-contraction only 1.19); K5 runs a 340-trial two-state model against a one-state control and shows the rebound one state cannot produce; K6 solves the constrained quadratic program for a concrete plant; K8 integrates the Adler equation across the locking edge and shows the lag sweeping the full quarter turn; K9 shows the 90 % threshold *understating* the true rank. Both promises are rewritten to the stronger, now-true form.

### B5. Proposition 7.1 is a paragraph of prose with a proof labelled "(Sketch)"  [B5a, B5b]

Location: `module12.html:190` (statement), `:192` (proof).

Quoted (line 192): "<div class=\"proof\">(Sketch; the quadratic-program step below is exact, and the bell shape follows once the plant's command-to-force smoothing is included.) ... by Lagrange multipliers its solution spreads the command smoothly over the whole movement (each $u_k\propto b_k/w_k$) rather than concentrating it in large, noisy bursts."

Missing parts 1 and 3. The statement asserted a qualitative conclusion ("spreads the motor command smoothly ... rather than in abrupt bursts") with no displayed minimiser, and the proof announced its own incompleteness. It is the load-bearing proposition of Section 7 and it sat beside nine proved siblings.

The applied fix states the minimiser in closed form,
$$u_k=\frac{x_T}{\sum_j b_j^2/w_j}\cdot\frac{b_k}{w_k},$$
and proves it: strict convexity gives existence and uniqueness, the Lagrangian gives stationarity, and the optimal variance $c\,x_T^2/\sum_jb_j^2/w_j$ is exactly the Cauchy-Schwarz bound, so restricting the command to a subset $S$ of steps raises the variance by $\big(\sum_jb_j^2/w_j\big)/\big(\sum_{j\in S}b_j^2/w_j\big)\ge1$ - a burst is penalised in exact proportion to the weight it leaves unused. A following paragraph then says what the proposition does *not* give (the bell shape depends on the plant) and hands that step to K6 with its computed 1.736.

### B6. Three symbols carry two meanings each across sections  [B6a1-B6a13, B6b1-B6b4, B6c1-B6c4]

`EDITOR_DOMAIN.md`: "a symbol means one thing for the whole module; a cross-section collision is a defect."

(a) **$K$** was the LQR feedback gain at `:130` and `:224-232` the oscillator coupling, with $K_x$ and $K_q$ the stiffness matrices in between. Quoted (line 224): "sinusoidal coupling of strength $K\gt 0$". Renamed to $\kappa$ in Proposition 8.2, its proof, its boxed condition, Figure 8's three in-figure labels and caption, the K8 statement, diagnostic 5, and the Appendix notation row, which now reads "coupling strength (never the LQR gain $K$)".

(b) **$\tau$** was the normalised movement time $t/T$ at `:110` and the feedback delay at `:415` and in K10. Quoted (line 415): "a first-order delayed loop is stable only for gain $k\lt \pi/2\tau$". Renamed to $\tau_d$ in C10, both axis labels of the two delay figures, the two in-figure formula labels, K10, and the Appendix, with a new notation row for $\tau_d$.

(c) **$\eta$** was the admissible variation in Lemma 2.1 at `:92` and the learning rate in Proposition 6.2. Renamed to $\zeta$ in the lemma's proof, D1's solution and the D1 figure label, with a new Appendix row and a parenthetical naming the reservation.

### B7 / B8. Three empirical counts and two population ranges are bare numbers  [B7a, B7b, B7c, B8]

Location: `module12.html:65` (Definition 1 and the missing count), `:218` and `:411` (VAF and synergy count), `:560` (Appendix).

Quoted (line 218): "a handful typically account for $80$-$90\%$ of the variance across postures and gaits."

`EDITOR_DOMAIN.md` admits exactly three classes for a number. "About seven joint degrees of freedom", "some fifty muscles", "thousands of motor units", "80-90 %" and "3-5 synergies" were none of the three: no derivation, no table entry, no "assume".

The applied fix adds a paragraph after Definition 1 that *counts* the seven (three glenohumeral, one elbow, one forearm rotation, two wrist), states $m=3$ for fingertip position and $m=6$ for full pose, and ends "These three counts are representative anatomical figures, listed in the Appendix parameter table; the argument needs only that each exceeds the count above it." Both population ranges are labelled representative and cross-linked to the K problem that recovers the quantity from data whose truth is known. Five new Appendix parameter rows carry the counts, the ranges, the Lab C stiffnesses (marked assumed) and K3's and K6's assumed constants.

### B9. The module never places its models on the level ladder  [B9]

Location: `module12.html:57`.

`EDITOR_DOMAIN.md`: "The module must place its models on the level ladder ... A Level-1 statics estimate presented as a dynamic result is a defect." Section 0 went from the thesis straight to the arc of the module. A reader meeting a double integrator in Section 4 and Module 11's full $M\ddot{\mathbf q}+C\dot{\mathbf q}+\mathbf g$ in Section 0 has no way to know which is the claim.

The applied fix inserts a "Where these models sit on the level ladder" paragraph before the arc: Sections 1 and 3 are Level 1 (purely kinematic, no force is written); Sections 4, 5 and 7 are Level 2 and linearized; Sections 6 and 8 are single-state scalar models; nothing here computes a muscle force, and Module 5 owns the step from command to force.

### B10 / S2. Definition 1 maps joint angles to "hand pose" and then sets $m=3$  [S2a, S2b, B10]

Location: `module12.html:65` and `:67` (the figure label), `:436` (the D5 figure label).

Pose is position plus orientation, six numbers, not three. The map is to hand *position*; the pose count is the interesting aside, and the new counting paragraph of B8 now makes it explicitly ($m=6$ still leaves one freedom). Separately, the D5 figure rendered $K_x=J^{-\mathsf T}K_qJ^{-1}$ with a modifier small **b** instead of a superscript **T** (`&#7495;` for `&#7488;`), so the figure displayed a different operator from the boxed result it illustrates.

### B11. D9's solution states the Adler equation with the LQR's symbol  [B11a, B11b]  *(second pass)*

Location: `module12.html:453` (D9 solution), `:222` (Figure 8's `aria-label`).

Quoted (line 453): "Subtracting the two oscillator equations gives $\dot\psi=\Delta\omega-2K\sin\psi$ ... So oscillators within coupling bandwidth $2K$ synchronize at phase lag $\psi^\star=\arcsin(\Delta\omega/2K)$ (Proposition 8.2)."

This is the collision of B6(a), surviving in the one place the first pass did not reach. It is worse than the original defect because the solution now cites a Proposition that uses $\kappa$ while itself using $K$, so the module states one law with two symbols on the same page. Figure 8's screen-reader label had the same residue ("delta-omega minus 2K sin psi") while its visible labels had been converted.

Replacement (D9 solution):

```html
<details class="sol"><summary>Solution</summary><div>Subtracting the two oscillator equations gives the Adler equation $\dot\psi=\Delta\omega-2\kappa\sin\psi$ ($\psi=\phi_2-\phi_1$, coupling strength $\kappa$). A locked state $\dot\psi=0$ needs $\sin\psi^\star=\Delta\omega/2\kappa$, solvable iff $|\Delta\omega|\le2\kappa$; linearising, $d\dot\psi/d\psi=-2\kappa\cos\psi^\star$, so the root with $\cos\psi^\star\gt 0$ is stable and the other unstable. Oscillators within the coupling bandwidth $2\kappa$ therefore synchronize at phase lag $\psi^\star=\arcsin(\Delta\omega/2\kappa)$ (Proposition 8.2).</div></details></div>
```

### B13. K6's figure draws the minimum-jerk bell inside a problem whose answer is not minimum jerk  [B13a, B13b, B13c]  *(second pass)*

Location: `module12.html:483` (the K6 figure), `:484` (the solution's closing paragraph).

Decoded from the delivered `<polyline>`: 120 points, calibrated from the tick lines at $y=155\to0$, $97.9\to1$, $40.7\to2$ and $x=55\to\tau{=}0$, $265\to\tau{=}1$. The curve peaks at **1.874 at $\tau=0.496$** and matches $1.875\,\tau^2(1-\tau)^2/(1/16)$ to 0.002 over every point. It is the minimum-jerk profile. K6's own solution, three lines below it, reads: "its speed profile is single-peaked, peaking at $1.389\ \mathrm{m/s}$ at $\tau=0.68$ with a peak-to-mean ratio of $1.736$ - between minimum acceleration's $1.500$ and minimum jerk's $1.875$". The figure therefore draws the very thing the problem exists to distinguish itself from, and a reader who trusts the picture learns the opposite of the result.

This passed `checktex`, `checklt`, `check_links`, `check_svg`, `check_code`, `verify_dom`, `check_overlap`, `check_frame` and `check_bodyprop`. It was found by decoding the point string.

The applied fix regenerates the solid curve from the K6 solution's own script (`figgen.k6_speed()` runs the identical 100-step quadratic program), adds minimum jerk as a dashed grey comparison so the sentence "between 1.500 and 1.875" has a picture, and labels both: "min-variance optimum: peak 1.736 at $\tau$=0.68" and "dashed: minimum jerk, 1.875 at $\tau$=0.50". Decoding the delivered result gives 1.736 at $\tau=0.68$ for the solid curve and 1.875 at $\tau=0.50$ for the dashed one. The solution's closing paragraph is extended to read the figure: "the computed optimum (solid) is both lower and later than the minimum-jerk profile (dashed), because the command must stop pushing early enough for the $40\ \mathrm{ms}$ lag to bleed off before the hold window opens." The code's comparison line, which had the 1.736 typed in as a literal, now computes it.

### B12. Lab B's second figure draws 40 % of its settling-time curve outside the plot frame  [B12a-B12g]  *(second pass)*

Location: `module12.html:310` (the figure), `:284` (Lab B Equations), `:303` (Lab B code).

Decoded from the delivered `<polyline>`: the blue curve is exactly $t_s=4\sqrt2\,R^{1/4}$ (max deviation 0.009 s over 40 points) and runs from 1.79 s to **17.89 s**. The y-axis top tick was **10**, and the axis line stopped at $y=40$, which is 11.0 on that scale. Everything past $\log_{10}R\approx1.19$ was drawn above the frame, in blank space, with no gridline or tick to read it against. `check_frame` did not fire because the viewBox had been widened to `6 -81 488 339` - 81 user units of empty space above the plot - so nothing was technically clipped. The `aria-label` compounded it: "Position gain and settling time versus the effort weight R on a log axis, **both falling** as effort is priced higher." The settling time rises; the figure's own caption says so.

The applied fix rescales the axis to 20 s (the "5" and "10" ticks become "10" and "20", $7.725$ px per unit), regenerates both analytic curves on the new scale, moves the legend left so it clears the rescaled gain curve, retightens the viewBox to `26 32 452 218`, and rewrites the `aria-label` to "the gain falls as R rises, the settling time climbs". Decoding the delivered curves gives 0.104-9.994 for the gain against $R^{-1/2}$ (error 0.007) and 1.786-17.890 for the settling time against $4\sqrt2R^{1/4}$ (error 0.009), both wholly inside the frame. Because Section 10 claims "every plotted number below was produced by the code shown", Lab B's script now prints the closed-loop poles and $t_s$ as well as the gains, and the Equations line states the closed form the figure is drawn from.

### B14. K5's figure is a 60-trial schematic beside a 340-trial solution  [B14a, B14b]  *(second pass)*

Location: `module12.html:479` (the K5 figure).

Decoded: 60 points on a trial axis labelled 0 / 30 / 60, peaking at **0.719 at trial 41** and troughing at $-0.270$ at trial 45. K5's solution reports a run of 200 adaptation trials, a 20-trial reversal and an error clamp, with the net command reaching **0.811 at trial 199**, $-0.275$ at 219 and rebounding to $+0.254$ at **231**; it also turns on a one-state control run that "ends the reversal at $-0.733$ and decays monotonically to $-0.002$, never crossing zero". Neither the trial axis nor any of the four numbers matched, and the control run - the part that carries the argument, since one state *cannot* rebound - was not drawn at all.

The applied fix draws the run the solution reports, from the solution's own recursion: both the two-state net command and the one-state control, decimated to 89 points (below `check_svg`'s 120-point advisory) with trials 199, 219, 220 and 231 forced into the sample so the transitions are exact, on a 0 / 170 / 340 axis with a zero reference line. Labels: "two states: peak 0.811, trough -0.284, rebound +0.254 at trial 231" and "dashed, one state: -0.733, no rebound". Decoding the delivered curves returns those values.

### B15 / B16. Two numbers in applied solutions disagree with the code beside them  [B15a, B15b, B16a, B16b]  *(second pass)*

Location: `module12.html:496` (K9 solution) and `:476` (K4 solution).

(a) Quoted (K9): "The third component adds $0.074$ and the fourth adds $0.0003$, a factor $250$ drop, and that is where the signal stops and the noise floor begins."

Run: the increments are 0.745300, 0.178720, 0.073613, **0.000564**, 0.000512. The fourth adds 0.000564, not 0.0003, and the drop is a factor **130**, not 250. The elbow argument survives - the point is that the fourth increment is at the noise floor and the fifth is the same size - but the two numbers were not printed by anything. The replacement quotes the printed increments in full and names the $5\times10^{-4}$ floor, and the code now prints the per-component increment beside the cumulative VAF so the elbow is legible from the output.

(b) Quoted (K4): "all three converge to $u_\infty=p=1$ with aftereffect $-1.000$. At $\eta=2.5$ the rate is $|1-\eta g|=1.50$ and the error grows: $57.7$ at trial $10$, $2.5\times10^{4}$ by trial $25$."

Run: the printed aftereffects at trial 25 are $-0.996$, $-1.000$, $-1.000$. For $\eta=0.2$ the run has not converged: $0.80^{25}=3.8\times10^{-3}$ of the perturbation is still unlearned. The $2.5\times10^{4}$ was also never printed (the script printed $u_{25}$, not $e_{25}$) and is negative. The replacement says which rates reach $-1.000$ at trial 25 and which does not, and why; the code now prints $e_{25}$, which reads $-2.53\times10^{4}$ for $\eta=2.5$ and $3.78\times10^{-3}$ for $\eta=0.2$.

## 3. Style and clarity edits

Line-level, applied in one pass. Locations are pristine line numbers.

- `:47` [S10] "This everyday miracle, called <b>motor equivalence</b> (Fig. 1), is the doorway to the deepest problem in movement science" -> "This everyday fact, called <b>motor equivalence</b> (Fig. 1), states the central problem of movement science". Two pieces of hype in one clause.
- `:53` [S17] "it picks movements that are <em>strikingly stereotyped</em>" -> "<em>stereotyped</em>".
- `:96` [S9] "Measured reaches are remarkably uniform" -> "Measured reaches vary little from person to person or trial to trial". Says what the uniformity is over.
- `:110` [S6] "Three predictions of Proposition 3.1 (Fig. 3) are borne out by measurement and give the model its authority." -> "Proposition 3.1 makes three predictions (Fig. 3), and each is checkable against a measured reach without fitting anything." Active, and it names the test rather than the verdict.
- `:110` [S6b] The 1.875 prediction now cites the 1.7-1.9 representative range and points at K1's competing 1.500, so the claim is falsifiable on the page.
- `:112` [S15] "it is really a description of the desired hand path, not yet a controller" -> "it describes the desired hand path rather than a controller".
- `:130` [S1] The LQR existence caveat named "the pendulum plant of Module 11", which this module never uses; replaced with "the double-integrator hand of Lab B and Module 11's arm linearized about a posture".
- `:156` [S8] "There is a deep stability reason the body prefers impedance." -> "Stability is the reason the body prefers impedance, and the argument is short."
- `:174` [S11] "The aftereffect is the smoking gun of an internal model" -> "the direct evidence for". Metaphor that cannot be cashed out into the mathematics.
- `:186` [S18] "We now unify the module." -> "Three loose ends now close together." A sentence that only announced the next sentence, replaced with one that names them.
- `:188` [S7] "This changes the optimization completely. There is no longer" -> "There is then no longer". Deletes the announcement.
- `:204` [S12] "while the null space breathes" -> "while the null-space coordinates vary freely".
- `:232` [S19] "the same Adler equation governs synchronizing fireflies and coupled clocks" now carries the equation inline, since "the Adler equation" had been named only in a figure caption.
- `:279`, `:281` [S5a, S5b] Figure 4's "(Curves offset slightly for visibility.)" and Lab A's "confirm they superimpose exactly" contradicted each other. Both rewritten: the profiles coincide to machine precision, and a small offset is drawn in so both stay visible.
- `:270` [S21] Lab A's Interpretation quotes a peak acceleration of $\pm9.24\ \mathrm{m/s^2}$ at $\tau\approx0.21$ and $0.79$; the code computed the array and printed neither, so Section 10's "every plotted number below was produced by the code shown" was false for this lab. The script now prints both. (Run: `peak |accel| 9.24 m/s^2 = 5.77 D/T^2 at tau = 0.211 and 0.789`.)
- `:337` [S22] Lab C's caption named the 388 N peak but not the $-85\ \mathrm{N}$ reversal, which is the only feature of the plot below the zero line and the largest thing on it a reader cannot account for. The caption now names it, and the impedance controller's $-3.5\ \mathrm{N}$ ring beside it.
- `:494` [S20] K9's statement asked only for the number of synergies reaching 90 % VAF; it now also asks whether that threshold recovers the true number, which is the question the solution answers.

## 4. Structural notes

- **The dependency graph runs backwards only, and the closing section pays.** Section 9's robot-versus-human table is the best structural device in the module: every row names an ingredient and points at the section that built it, and the paragraph under it reads the "Human" column as one design. The repayment ledger does the same for the five borrowings. Neither needed an edit.
- **Section 7 is the hinge and now carries its weight.** Before this pass it opened by announcing a unification, stated its central proposition in prose, and sketched the proof. It now names the three loose ends, proves the proposition in closed form with the Cauchy-Schwarz gap as the burst penalty, and hands the bell-shape step to K6 with a computed number. Nothing else in the module needed restructuring.
- **The problem set is the right shape and the K problems are not substitution.** All ten require an integration, an optimisation, an inverse solve, a sweep or a regime comparison, which is the `EDITOR_DOMAIN.md` standard; K3 (two branches plus a constrained split search) and K6 (a two-constraint quadratic program) are the deepest. The gap was never depth, it was that none of them shipped the code they claimed.
- **What is still unproved is unproved deliberately, and says so.** Section 5's passivity argument is stated, not proved; that is correct at this level and the limitations table names it. The "what the model captures and misses" table is honest about inverse optimal control being open and about synergies being descriptive.
- **One figure defect is logged and left.** K4's figure (`module12.html:476`) draws the $\eta=2.5$ divergence clamped to the frame edges, alternating between $+1.24$ and $-0.50$ on the plot's own scale while the true errors are $\pm1.5^{\,n}$ and reach $57.7$ by trial 10. I left it: the in-figure label says "$\eta=2.5$ diverges", the alternating sign is drawn, and a curve pinned to both frame edges reads as off-scale rather than as settled, so it is not the m14 failure (a runaway drawn flat under a caption claiming a runaway). A log-$|e|$ inset would make the $57.7$ readable and is the fix if the user wants it.
- **The three figures redrawn in this pass are now generated from the same script as their numbers.** `figgen.py` re-runs K6's quadratic program, K5's two recursions and Lab B's closed forms and emits the polylines directly, so a future change to a solution's parameters cannot silently leave its picture behind. That is the pattern the rest of the module's computed figures already follow.

## 5. What already works

- **Lemma 2.1 to Proposition 3.1 to the 1.875 ratio** is the model passage. The Euler-Poisson equation is proved by variation and repeated integration by parts, minimum jerk is fed into it with $p=3$, the sixth derivative vanishes, the six boundary conditions are solved as a stated linear system with the coefficients written out, and the peak-to-mean ratio falls out as $30/16$. A reader can reproduce every line with a pen, which is exactly the third part of the standard.
- **Proposition 4.1's HJB proof** guesses $V=\mathbf x^{\mathsf T}P\mathbf x$, minimises the bracket, substitutes back, symmetrises, and lands on the Riccati equation without a gap.
- **Proposition 7.2 is short, exact, and does the module's most surprising work**: two lines of variance algebra produce the uncontrolled-manifold signature, and Lab D confirms it numerically at 6.65 against a predicted 6.67.
- **Anatomical glossing (Pillar 1) holds throughout.** "Glenohumeral joint (the shoulder ball-and-socket, which rotates about three axes)", "pronation and supination, the twist that turns the palm over" - every term is glossed in the sentence that introduces it.
- **The everyday hooks are real and they are cashed out.** The two signatures, the failed self-tickle, the force-field aftereffect and the pianist's finger are each tied to a proposition rather than left as anecdote.
- **Every one of the ten propositions and one lemma carries an adjacent proof of matching weight.** `check_proofs.py` reports zero asserted results, and reading the boxed `.keyresult` siblings by eye finds no unproved peer - the Module 6 Section 6 failure class is absent here.

## 6. Changes applied

96 edits, applied by one re-runnable `apply.py` against a pristine copy, in tag order. Tags B1-B10 and S1-S20 are the first pass, reconstructed from the diff and re-verified; B11-B16 and S21-S22 are the second pass. "Line (original)" is the first line of the anchor in the pristine 598-line `module12.html`; where an edit's anchor is text the first pass introduced, the line given is that of the problem or lab it sits in.

| tag | line (original) | what changed | how verified |
|---|---|---|---|
| B10 | 436 | D5 figure label `J⁻ᵇKq J⁻¹` (entity `&#7495;`, modifier small b) corrected to `J⁻ᵀKq J⁻¹` (`&#7488;`), matching the boxed Proposition 5.1 | read the entity codepoint against the boxed result |
| B9 | 57 | new "Where these models sit on the level ladder" paragraph before the arc: Sections 1 and 3 Level 1, Sections 4/5/7 Level 2 and linearized, Sections 6 and 8 single-state, no muscle force anywhere | `EDITOR_DOMAIN.md` level-ladder rule; each section re-read to confirm its level |
| B8 | 65 | new paragraph counting the arm's 7 joint DOF by name (3 glenohumeral, 1 elbow, 1 forearm, 2 wrist), stating m=3 for position and m=6 for pose, and labelling the ~50 muscles and motor-unit counts as representative Appendix figures | hand count against the named joints; Appendix rows added in B1g |
| S2a | 65 | Definition 1 "joint angles to hand **pose** $\in\mathbb R^m$" → "hand **position**"; pose is 6 numbers, the definition uses 3 | dimension check against $m=3$ in the same sentence |
| S2b | 67 | Figure 2's label "hand pose (3)" → "hand position (3)" | same |
| B7a | 218 | synergy VAF "$80$-$90\%$ ... typically" labelled a representative range, cross-linked to the Appendix and to K9, which recovers the rank from data of known truth | number-class rule: representative + table entry |
| B7b | 411 | C9's "often $3$-$5$" synergies labelled "a representative $3$-$5$; Appendix" | same |
| B7c | 560 | Appendix row "Synergies for $90\%$ VAF (typical)" → "(representative)" | same |
| B5a | 190 | Proposition 7.1 restated with the closed-form minimiser $u_k=(x_T/\sum_j b_j^2/w_j)(b_k/w_k)$ and the burst penalty named as the Cauchy-Schwarz gap | derived by hand; the same formula is what K6's code evaluates and its endpoint lands at 0.4000 m |
| B5b | 192 | "(Sketch)" proof replaced by a full one: strict convexity → existence and uniqueness; Lagrangian → stationarity; optimal variance = the Cauchy-Schwarz bound; subset restriction raises variance by $(\sum_j)/(\sum_{j\in S})\ge1$. New paragraph hands the bell-shape step to K6 with its computed 1.736 and 42.4 | hand derivation; the 1.736 / 1.500 / 1.875 / 42.4 all printed by the K6 block (`blk10`) |
| B6c1 | 92 | Lemma 2.1's proof: variation renamed $\eta\to\zeta$ (collides with the Section 6 learning rate), with the reservation stated | symbol sweep of the whole file |
| B6c2 | 421 | D1 solution: same rename | same |
| B6c3 | 420 | D1 figure label "x + εη" → "x + εζ" | same |
| B6c4 | 420 | D1 figure label "η, η′,… = 0 at both ends" → "ζ, ζ′,…" | same |
| B6a1 | 224 | Proposition 8.2: oscillator coupling $K\to\kappa$, with the reservation against the LQR gain $K$ and the stiffnesses $K_x,K_q$ stated | symbol sweep |
| B6a2 | 225 | the two oscillator equations rewritten in $\kappa$ | same |
| B6a3 | 226 | phase-difference line rewritten in $\kappa$ and the flow named the **Adler equation** at first use | the name was previously introduced only in a figure caption |
| B6a4 | 227 | boxed locking condition $|\Delta\omega|\le2\kappa$ | same |
| B6a5 | 228 | locked phase $\psi^\star=\arcsin(\Delta\omega/2\kappa)$ | same |
| B6a6 | 230 | Proposition 8.2's proof rewritten in $\kappa$ throughout | same |
| B6a7 | 222 | Figure 8 in-figure label "lock if \|Δω\| ≤ 2K" → "2κ" | same |
| B6a8 | 452 | D9 figure label "ψ̇ = Δω − 2K sin ψ" → "2κ" | same |
| B6a9 | 491 | K8 figure axis label "coupling K" → "coupling κ" | same |
| B6a10 | 222 | Figure 8 caption rewritten in $\kappa$ and the Adler equation named | same |
| B6a11 | 508 | diagnostic 5 ("locking count") rewritten in $\kappa$ | recomputed: \|Δω\|=2π(0.2)=1.26, 2κ=2·2π(0.3)=3.77 rad/s, locks |
| B6a12 | 549 | Appendix notation row now reads "coupling strength (never the LQR gain $K$)" | symbol sweep |
| B6a13 | 490 | K8 statement: "as a function of coupling $K$" → "of the coupling strength $\kappa$" | same |
| B6b1 | 415 | C10: delayed-loop bound $k\lt\pi/2\tau$ → $k\lt\pi/(2\tau_d)$, with the reservation against $\tau=t/T$ of Section 3 stated | symbol sweep; the same $\tau$ is the normalised time in Proposition 3.1 |
| B6b2 | 414, 490 | both delay figures' x-axis label "delay τ (s)" → "delay τ_d (s)" (2 occurrences) | same |
| B6b2b | 414 | C10 figure label "delay caps the gain: k < π/2τ" → "k &lt; π/(2τ_d)" | same |
| B6b2c | 499 | K10 figure formula label "= π/2τ" → "= π/(2τ_d)" | same |
| B6b3 | 561 | Appendix parameter row $k_{\max}=\pi/(2\tau)$ → $\pi/(2\tau_d)$ | same |
| B6b4 | 547 | two new Appendix notation rows: $\tau_d$ (feedback delay, never $t/T$) and $\zeta$ (admissible variation) | same |
| B1a | 315 | Lab C Parameters/Equations: wall stiffness $k_w=10^5$ N/m named, controller stiffness renamed $K_c$, damping and mass and step listed, and the series steady force $K_ck_w(x_{\rm des}-x_w)/(K_c+k_w)$ stated | the code always used a finite `kw`; the prose said "rigid" |
| B1b | 317 | Lab C code rewritten: `run()` returns (peak, settled), a `steady()` closed form is printed beside the simulation, and the rigid-wall estimate is printed for comparison | run: `impedance peak 20.9 settled 9.98 predicted 9.98 / servo peak 387.7 settled 238.10 predicted 238.10 / steady ratio 23.9 x, peak ratio 18.6 x` |
| B1c | 337 | Lab C figure regenerated: y-axis ticks 150/300 → 200/400 N, both polylines redrawn from the trace, in-figure labels now "servo: peak 388 N, settles 238 N" and "impedance: peak 21 N, settles 10 N", caption rewritten around the computed numbers | decoded the delivered polylines back to newtons and re-ran the trace: agree to 0.12 N over 1200 points; peaks 387.8 / 21.6 N |
| B1d | 339 | Lab C Interpretation rewritten: 21 / 9.98 N and 388 / 238.10 N, factors 23.9 and 18.6, the closed form named, and the rigid-wall estimate shown to be exact for the compliant controller and 5 % high for the stiff one | same run; $200\times0.05=10$ vs 9.98 and $5000\times0.05=250$ vs 238.10 |
| B1e | 395 | C5 solution: "$250\ \mathrm{N}$ vs $10\ \mathrm{N}$" replaced by the computed settled and peak pairs and the factor 23.9 | same run |
| B1f1 | 394 | C5 figure bar height rescaled from the 25x ratio to the computed 23.9x | arithmetic on the bar's pixel height |
| B1f2 | 394 | C5 figure label "servo: 25× the contact force" → "servo: 23.9× the settled force" | same run |
| B1g | 559 | Appendix parameter table: Lab C row rewritten to 9.98 vs 238.10 N (23.9×), peaks 21 and 388 N; five new rows for the joint/muscle/motor-unit counts, the 1.7-1.9 peak/mean range, the 80-90 % VAF range, the Lab C stiffnesses (assumed) and K3's and K6's assumed constants | number-class rule; each value traced to its printing run or to the assumption label |
| K1 | 464 | K1 solution rewritten with a code block; adds the explicit minimum-acceleration cubic $x=D(3\tau^2-2\tau^3)$, the 25.0 % sharper-peak statement and the representative 1.7-1.9 range | run: `min-jerk 1.8750 / min-accel 1.5000 / jerk profile is 25.0% more peaked` |
| K2 | 468 | K2 solution rewritten with a code block; adds the closed-form ARE solution $K=[R^{-1/2},\sqrt2R^{-1/4}]$, $t_s=8/K_2=4\sqrt2R^{1/4}$, and the inverse solve $t_s=1.8\Rightarrow R=0.01025$ | run: `1.79 / 3.18 / 5.66 / 10.06 s; target ts=1.80 -> k2=4.4444 -> R=0.01025` |
| K3 | 472 | K3 solution rewritten with a code block; now a real optimisation over two IK branches and the co-contraction split at a fixed 65 N·m/rad budget | run: eigenvalues 723 / 88 N/m ratio 8.24; long axis 31.2° vs 173.9°; along/across 8.21 vs 1.63 (factor 5.0); best split $k_1=5.00\to9.76$ (factor 1.19); axis sweep 553/723/576/258/88/235 N/m |
| K4 | 476 | K4 solution rewritten with a code block; the sweep now locates the $\eta g=2$ boundary and names deadbeat $\eta g=1$ as the fastest stable rate | run: rates 0.80 / 0.50 / 0.00 / 1.50; $e_{10}$ = 0.107 / 9.77e-4 / 0 / 57.7 |
| K5 | 480 | K5 solution rewritten with a code block; a 340-trial two-state run against a one-state control, with spontaneous recovery as the discriminator | run: `end of adaptation n=199: fast 0.142 slow 0.669 net 0.811 / end of reversal n=219: net -0.275 / clamp: net -0.284 at 220, rebounds to +0.254 at 231 / single-state: -0.733, best after -0.002` |
| K6 | 484 | K6 solution rewritten with a code block; a two-constraint quadratic program (reach D **and** end at rest) with a 0.3 s hold window | run: `endpoint 0.4000 m, terminal speed 8.8e-16 m/s; speed peaks 1.389 m/s at tau=0.68; peak/mean 1.736; SD x42.4 / x10.0 / x3.2` |
| K7 | 488 | K7 solution rewritten with a code block; the posture, the hand-x Jacobian row, the null and task directions and both variances now quoted from the run | run: `q=(81.3, -107.2) deg; row (-0.1000, 0.1966); null (0.891, 0.453); Var(null) 3.938e-04, Var(task) 6.160e-05, ratio 6.39 (1/rho 6.67)` |
| K8 | 492 | K8 solution rewritten with a code block; adds the lag sweeping 30.0° → 64.2° → 89.7° across the band and the saddle-node's algebraic approach at $\Delta\omega=2\kappa$ | run: bandwidths 0.50 / 1.00 / 2.00 rad/s; locks at 30.0° / 64.2° / 89.7°; drifts to 265.091 rad at Δω=1.2 |
| K9 | 496 | K9 solution rewritten with a code block; the VAF sequence corrected from the asserted 0.785 / 0.951 / 0.998 to the computed values, and the finding inverted: the 90 % threshold *understates* the rank, the elbow identifies it | run: `k=1 0.7453, k=2 0.9240, k=3 0.9976, k=4 0.9982, k=5 0.9987; smallest k with VAF >= 0.90: 2; true rank 3` |
| K10 | 500 | K10 solution rewritten with a code block; adds the explicit contrast with K2's unbounded-gain optimum and why prediction raises the ceiling | run: `31.42 / 15.71 / 10.47 / 7.85 /s for τ_d = 0.05 / 0.10 / 0.15 / 0.20 s` |
| S20 | 494 | K9 statement extended: "Then ask whether the $90\%$ threshold recovers the true number." | the solution's answer is that it does not; the statement now asks the question |
| K9fig1 | 495 | K9 figure polyline redrawn at the computed VAFs (0.745, 0.924, 0.998, 0.998, 0.999); it had encoded the asserted 0.785 / 0.951 series | decoded the delivered points back through the tick calibration: 0.745 / 0.924 / 0.998 / 0.998 / 0.999 |
| K9fig2_102 … _270 | 495 | the five marker circles moved onto the redrawn polyline (5 edits) | same decode |
| K7fig | 487 | K7 figure label "joints co-vary: ratio 6.4" → "ratio 6.39" | run prints 6.39 |
| S1 | 130 | LQR existence caveat: "the pendulum plant of Module 11" (not used in this module) → "the double-integrator hand of Lab B and Module 11's arm linearized about a posture" | both plants appear in the module; the pendulum does not |
| S10 | 47 | "everyday miracle … doorway to the deepest problem" → "everyday fact … states the central problem" | hype rule |
| S17 | 53 | "strikingly stereotyped" → "stereotyped" | hype rule |
| S9 | 96 | "remarkably uniform" → "vary little from person to person or trial to trial" | hedging/hype rule; names what the uniformity is over |
| S6 | 110 | "Three predictions … are borne out by measurement and give the model its authority" → "Proposition 3.1 makes three predictions, and each is checkable against a measured reach without fitting anything" | active voice; states the test not the verdict |
| S6b | 110 | the 1.875 prediction now cites the representative 1.7-1.9 range and K1's competing 1.500 | number-class rule + K1's run |
| S15 | 112 | "it is really a description of the desired hand path, not yet a controller" → "it describes the desired hand path rather than a controller" | hedging rule |
| S8 | 156 | "There is a deep stability reason the body prefers impedance." → "Stability is the reason the body prefers impedance, and the argument is short." | hype rule |
| S11 | 174 | "the smoking gun of an internal model" → "the direct evidence for an internal model" | metaphor rule |
| S18 | 186 | "We now unify the module." → "Three loose ends now close together." | cut the sentence that only announces the next |
| S7 | 188 | "This changes the optimization completely. There is no longer" → "There is then no longer" | same |
| S12 | 204 | "while the null space breathes" → "while the null-space coordinates vary freely" | metaphor rule |
| S19 | 232 | "the same Adler equation governs synchronizing fireflies and coupled clocks" now carries $\dot\psi=\Delta\omega-2\kappa\sin\psi$ inline | the name had been defined only inside a figure caption |
| S5a | 279 | Figure 4 caption "(Curves offset slightly for visibility.)" → an explicit statement that the profiles coincide to machine precision and the offset is drawn in | it contradicted Lab A's "superimpose exactly" |
| S5b | 281 | Lab A Extension "confirm they superimpose exactly" → "to machine precision", with a pointer to the drawn offset | same |
| B2a | 373 | "computational solutions quote numbers the code produces" → "every computational solution carries the Python that produced its numbers, and every number it quotes is one that code prints" | now true: K1-K10 all carry code (B2b's count re-checked below) |
| B2b | 460 | "Numbers quoted are those the code produces." → "Each solution carries a standalone Python block; the numbers quoted are the numbers it prints. Together with the four labs, all fourteen blocks in this module run as shown." | `check_code.py` counts 14 blocks; all 14 extracted and run to completion |
| B11a | 453 | D9 solution: the Adler equation restated in $\kappa$ (it had kept $K$ after Proposition 8.2 was renamed, so the module gave one law two symbols), and the stability step made explicit with $d\dot\psi/d\psi=-2\kappa\cos\psi^\star$ | symbol sweep of the delivered file: `grep` for `2K` now returns nothing |
| B11b | 222 | Figure 8 `aria-label` "delta-omega minus 2K sin psi" → "minus 2 kappa sin psi" | same sweep, screen-reader text included |
| B12a | 310 | Lab B figure: viewBox `6 -81 488 339` → `26 32 452 218`, and the `aria-label` "both falling as effort is priced higher" → "the gain falls as R rises, the settling time climbs" | the settling time rises; the 81 units of empty space above the plot were there only to stop `check_frame` calling the overflow a clip |
| B12b | 310 | Lab B figure y-axis rescaled: ticks "5"/"10" → "10"/"20" (7.725 px per unit) so the 17.9 s settling time fits | $t_s(R{=}100)=4\sqrt2\cdot100^{1/4}=17.89$ s, printed by the edited Lab B block |
| B12c | 310 | both Lab B polylines regenerated on the new scale from $K_1=R^{-1/2}$ and $t_s=4\sqrt2R^{1/4}$ over 40 points | decoded the delivered curves: gain 0.104-9.994 (error 0.007 vs the model), settling 1.786-17.890 (error 0.009); both wholly inside the axes |
| B12d | 310 | Lab B legend moved left (x 230→108) so it clears the rescaled gain curve, and the settling-time entry now carries its formula | `check_overlap.py` reports 0 label/curve overlaps after the move |
| B12e | 310 | Lab B caption rewritten: both curves named as computed from the closed forms, the 10→0.1 gain span and 1.79→17.9 s settling span quoted, and the axis ceiling explained | the edited Lab B block prints `ts=1.79 / 5.66 / 17.89 s` |
| B12f | 303 | Lab B code now prints the closed-loop poles and the settling time beside the gains | run: `R=0.01 K=[10. 4.472] poles [-2.236±2.236j] ts=1.79 s` … `R=100.00 K=[0.1 0.447] poles [-0.224±0.224j] ts=17.89 s`, matching the Interpretation's quoted poles |
| B12g | 284 | Lab B Equations line now states the closed-form Riccati solution, the pole locations and $t_s=8/K_2=4\sqrt2R^{1/4}$ that the figure is drawn from | derived by hand and confirmed by the run above |
| B13a | 483 | K6 figure: the polyline was the minimum-jerk bell (decoded peak 1.874 at $\tau=0.496$, matching min-jerk to 0.002) inside a problem whose answer is 1.736 at $\tau=0.68$. Solid curve regenerated from K6's own quadratic program; minimum jerk added as a dashed comparison; both labelled with their numbers | decoded the delivered curves: solid 1.736 at $\tau=0.68$, dashed 1.875 at $\tau=0.50$; `blk10` prints `speed peaks 1.389 m/s at tau=0.68; peak/mean 1.736` |
| B13b | 484 | K6 solution's closing paragraph now reads the figure and says why the optimum is lower and later than minimum jerk (the 40 ms lag must bleed off before the hold window opens) | the decoded solid curve peaks later and lower than the dashed one, as stated |
| B13c | 484 | K6 code: the comparison line had 1.736 typed in as a literal; it now computes `vel.max()/(D/T)` | run prints `min-acceleration 1.500 < 1.736 < min-jerk 1.875` from the computed value |
| B14a | 479 | K5 figure: the 60-trial schematic (decoded peak 0.719 at trial 41) replaced by the run the solution reports - the two-state net command and the one-state control over 340 trials, 89 points with trials 199/219/220/231 forced into the sample, on a 0/170/340 axis with a zero reference line and both curves labelled | decoded the delivered curves: two-state peak 0.811, trough -0.284, one-state trough -0.732; `blk09` prints 0.811 / -0.275 / -0.284 / +0.254 at 231 / -0.733 |
| B14b | 479 | K5 figure `aria-label` extended to describe the 200 + 20 + clamp structure and the one-state control | matches the redrawn figure |
| B15a | 496 | K9 solution: "the fourth adds $0.0003$, a factor $250$ drop" → the printed increments 0.7453 / 0.1787 / 0.0736 / 0.000564 / 0.000512, the factor 130, and the $5\times10^{-4}$ noise floor named | run: increments as listed; $0.073613/0.000564=130.4$ |
| B15b | 496 | K9 code now prints each component's increment beside the cumulative VAF, so the elbow is legible from the output | run: `k=3 cumulative VAF 0.9976 this component adds 0.073613 / k=4 … adds 0.000564` |
| B16a | 476 | K4 solution: "all three converge … with aftereffect $-1.000$" corrected - the run prints $-0.996$ for $\eta=0.2$ because $0.80^{25}=3.8\times10^{-3}$ is still unlearned; the trial-25 error for $\eta=2.5$ given its sign | run: aftereffects -0.996 / -1.000 / -1.000; $e_{25}=-2.53\times10^{4}$ for $\eta=2.5$ |
| B16b | 476 | K4 code now prints $e_{25}$, the number the solution quotes, which it previously did not | run: `eta=0.2 … e25= 0.00378 … aftereffect -0.996` |
| S21 | 270 | Lab A code now prints the peak acceleration and the two instants it occurs at, which the Interpretation quotes | run: `peak |accel| 9.24 m/s^2 = 5.77 D/T^2 at tau = 0.211 and 0.789`; closed form $\tau=(3\pm\sqrt3)/6$ |
| S22 | 337 | Lab C caption now names the $-85\ \mathrm{N}$ servo reversal (the only feature below the zero line) and the impedance controller's $-3.5\ \mathrm{N}$ ring | decoded the delivered polylines: minima -84.7 N and -3.5 N, matching the re-run trace |

### Gate results

Run on `edited/module12.html` after the 96 edits, with the pristine `module12.html` as the baseline. Rule: zero where the baseline was zero, never worse anywhere.

| gate | baseline (`module12.html`) | after (`edited/module12.html`) |
|---|---|---|
| `checktex` | 603 segments, 0 issues | 880 segments, **0 issues** |
| `checklt` | 0 | **0** |
| `check_links` | 118 links, 0 broken, 0 unlinked | 137 links, **0 broken, 0 unlinked** |
| `check_svg` | 0 hard, 1 advisory (12 polylines >120 pts) | **0 hard**, 1 advisory (12 polylines >120 pts - unchanged) |
| `check_code` | 4 blocks, 0 issues | 14 blocks, **0 issues** |
| `verify_dom` | 0 mjx-merror, 0 broken links, 18 stray `$` + 1 swallowed-prose (advisory) | **0 mjx-merror, 0 broken**, same 18 + 1 advisories |
| `check_overlap` | 0 | **0** |
| `check_frame` | 0 clipped, 9 margin advisories | **0 clipped**, 9 margin advisories (same nine figures) |
| `check_bodyprop` | 0 hard, 2 advisories (C3, C5 floating bust) | **0 hard**, 2 advisories (unchanged) |

Advisory gates outside the nine: `check_prose` 0 flags, `check_proofs` 0 asserted propositions, `check_probfig` 30 problem figures all recognizable entities or real plots.

The two `verify_dom` advisories and the nine `check_frame` margin advisories are pre-existing and untouched; the swallowed-prose flag is Proposition 6.1's genuinely long display `\mathbf r=\mathbf s-\hat{\mathbf s}_{\rm self}=\dots`, not a shell-mangled sentence. The `check_svg` advisory counts the twelve dense computed plots that were already in the module; the six polylines regenerated in this pass carry 40, 40, 100, 100, 89 and 89 points and add nothing to it.
