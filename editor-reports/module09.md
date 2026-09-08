# Editor report: module09.html (Running and Jumping)

Editorial pass. Standard: the five-part rule of the `science-editor` skill, read
against `EDITOR_DOMAIN.md`. Every location is `module09.html:LINE`. Every
replacement is valid HTML with MathJax delimiters and uses only the box classes
the stylesheet defines. All four Python blocks in the file (Labs 1 to 4) were
extracted and run; the SLIP stance was independently re-implemented with an RK4
integrator (energy conserved to 1 part in 10^15) and swept; every polyline in
the ten K figures was extracted and checked against a computation. Scripts in
the session scratchpad, folder `m09/`: `verify.py`, `k1.py`, `genK.py`
(`knums.json`). Every number in a replacement below was printed by one of those
runs. `module09-reviewer-findings.md` records a prior Fable 5 rigor review of
sections 0 to 5; all eight of its fixes are present in the file and all eight
hold up. This pass covers sections 0 to 11 and the Appendix, and its findings
are disjoint from that review's.

## 1. Verdict

Yes, after revision. A graduate reader with no biomechanics can learn from these
pages why running is a bounce and walking a vault, how one impulse equation runs
forward into a jump and backward into a landing, and why a tendon rather than a
muscle does the mechanical work of running. The derivational spine is sound:
Propositions 1.1, 1.2, 2.1, 2.2, 2.3, 3.1, 4.1, 4.2, 5.1, 5.2, 6.1, 6.2, 7.1,
8.1 and 9.1 each carry a proof of matching weight, `check_proofs.py` finds no
asserted proposition, and I re-derived every one by hand and found no
mathematical error. The four labs run clean and print exactly what the lab
prose claims.

What stops the reader is the problem set and the numbers around it. K1 asks the
reader to find the leg stiffness that maximises flight time and asserts an
interior optimum at "18 kN/m", its figure draws a hump, and its solution
supplies a mechanism for the hump. None of it is real: at the fixed touchdown
state K1 itself specifies, flight time rises strictly monotonically with
stiffness across the whole admissible band, from 25 ms at 12 kN/m to 320 ms at
40 kN/m, with no interior maximum. That is a drawn result the module's own model
contradicts, the class the domain brief calls the most serious. Section 6 and
Figure 7 report a 34 cm countermovement jump; the module's Lab 2, which is the
stated source of the number, computes 32.0 cm. Section 9's four headline numbers
(1.8 and 0.8 body weights, 10 and 22 ms, 185 and 37 body weights per second)
reproduce exactly, but only from an effective impact mass of 8 kg and a closing
speed of 1.0 m/s that appear nowhere in the module and in no Appendix row. The
Figure 10 caption, its aria-label, C8 and K6 all call the quantity Proposition
8.1 derives the *peak* landing force, when Proposition 8.1 says average and
section 9 exists precisely to insist on the difference. Nine of the ten K
solutions state no computed number at all, which is exactly the condition under
which K1's false claim could ship. Three symbols carry two meanings each, and
the Appendix records two of the three collisions in a single row rather than
resolving them. None of this touches the derivations, which are correct as they
stand.

## 2. Blocking defects

Ranked by severity: a drawn result the model contradicts first, then numbers
that disagree with the code, then numbers with no admissible class, then
conflated quantities, then problem-set depth and notation.

### B1. K1 asserts an interior optimum in flight time that the model does not have

Location: `module09.html:497-499` (statement, figure, solution).

Quoted (statement, line 497): "Find the stiffness that maximises flight time,
and explain why an interior optimum exists rather than &quot;stiffer is always
better.&quot;"

Quoted (figure, line 498): `aria-label="Flight time versus leg stiffness,
peaking at an intermediate optimum."` and the text label
`optimum kleg &#8776; 18 kN/m`, over a polyline that descends to a minimum
`y = 44.0` near `x = 166` and rises on both sides, i.e. a drawn hump.

Quoted (solution, line 499): "Flight time peaks at an intermediate stiffness:
too soft a leg over-compresses and spends the stance redirecting rather than
rebounding, while too stiff a leg barely compresses and stores little elastic
energy to launch with."

Fails part 1 (precise statement) and part 3 (a proof in the smallest setting):
the claim is false, and the mechanism offered for it is false too. Integrating
(2.1) with RK4 at `dt = 2e-5` from the fixed touchdown state Lab 1 uses
(`alpha_0 = 70` deg, `v_x = 4.0` m/s, `v_y = -0.7` m/s, `m = 70` kg,
`L_0 = 1` m), with the total energy conserved to `|dE/E| < 8e-15` at every
point, gives

| k_leg (kN/m) | 11.0 | 12 | 15 | 20 | 26 | 30 | 40 | 60 |
|---|---|---|---|---|---|---|---|---|
| t_f (ms) | 0 (no takeoff) | 25.4 | 93.2 | 171.9 | 234.5 | 265.2 | 319.9 | 383.0 |
| peak F_z (BW) | 2.12 | 2.24 | 2.58 | 3.06 | 3.56 | 3.83 | 4.51 | 5.60 |

`numpy.diff(t_f) > 0` is true at every one of the 59 grid points from 11 to 40
kN/m. There is no interior maximum, and the stated mechanism inverts the
physics: at a *fixed* touchdown state the system energy is fixed, so a stiffer
leg does not store less energy, it stores the same energy over a shorter sweep
and therefore returns more of it vertically. The forward speed pays for it,
falling from 4.20 m/s at 12 kN/m to 3.60 m/s at 40 kN/m. The real bound is a
constraint, not an optimum: root-finding the stiffness at which the peak
vertical GRF reaches 3 body weights gives `k_leg = 19.3 kN/m`, where
`t_f = 163 ms`. Below `k_leg = 11.09 kN/m` (also root-found) the takeoff
vertical velocity is negative and there is no flight at all, so that endpoint is
the boundary gait of Proposition 1.2, not running.

Replacement for the whole K1 block (lines 497 to 499). The polyline is
regenerated from the sweep above: x maps `k_leg` from 11 to 40 kN/m onto 48 to
262, y maps `t_f` from 0 to 340 ms onto 150 to 44.

```html
<div class="prob"><b>K1.</b> Integrate the SLIP stance and sweep the leg stiffness $k_{\rm leg}$ at a fixed touchdown state. Report the flight time and the peak vertical GRF together, and decide from the sweep whether flight time has an interior optimum or whether the useful stiffness is set by a constraint instead. Then find, by root-finding, the softest leg that still produces flight and the stiffest one that keeps the peak below $3$ body weights. <span class="small"><em>Probes: <a class="secref" href="#labs">Lab 1</a>; simulation + constrained inverse. Do not assume the answer: let the sweep say which of the two it is.</em></span>
<figure style="margin:.5rem 0"><svg class="setupfig" viewBox="0 0 300 190" width="100%" role="img" aria-label="Flight time rising monotonically with leg stiffness, with the three-body-weight peak-force limit marked."><line x1="48" y1="150" x2="262" y2="150" stroke="#333"/><line x1="48" y1="44" x2="48" y2="150" stroke="#333"/><text x="155" y="165" font-size="9" fill="#555" text-anchor="middle">leg stiffness k&#8343;&#8337;&#8340; (kN/m)</text><text x="32" y="97.0" font-size="9" fill="#555" text-anchor="middle" transform="rotate(-90 32 97.0)">flight time t&#8332; (ms)</text><text x="48" y="160" font-size="7.5" fill="#777" text-anchor="middle">11</text><text x="262" y="160" font-size="7.5" fill="#777" text-anchor="middle">40</text><polyline points="POLY_K1" fill="none" stroke="#b0361f" stroke-width="2.2"/><line x1="109.3" y1="44" x2="109.3" y2="150" stroke="#2a6ca8" stroke-dasharray="4 3"/><circle cx="109.3" cy="99.2" r="3.5" fill="#2a6ca8"/><text x="150" y="70" font-size="8.5" fill="#2a6ca8" text-anchor="middle">peak GRF hits 3 BW</text><text x="150" y="80" font-size="8.5" fill="#2a6ca8" text-anchor="middle">at 19.3 kN/m</text><text x="230" y="118" font-size="8.5" fill="#b0361f" text-anchor="middle">no interior maximum</text></svg><figcaption>Flight time against leg stiffness at the fixed touchdown state of Lab 1 ($\alpha_0=70^\circ$, $v_x=4.0$, $v_y=-0.7\ \mathrm{m/s}$), computed by RK4 integration of (2.1). The curve rises monotonically over the whole admissible band; what limits stiffness is the peak vertical GRF, which reaches $3$ body weights at $k_{\rm leg}=19.3\ \mathrm{kN/m}$ (dashed).</figcaption></figure>
<details class="sol"><summary>Solution</summary><div><p>Integrate stance to takeoff, read the vertical takeoff velocity, and get $t_{\rm f}=2v_y/g$; scan $k_{\rm leg}$. The sweep settles the question against the guess: flight time rises <em>monotonically</em>, $25.4\to93.2\to171.9\to234.5\to319.9\ \mathrm{ms}$ as $k_{\rm leg}$ runs $12\to15\to20\to26\to40\ \mathrm{kN/m}$, with no interior maximum anywhere in the band (the same sweep continued to $60\ \mathrm{kN/m}$ is still climbing, at $383\ \mathrm{ms}$).</p><p>The reason is Proposition 2.2. At a <em>fixed</em> touchdown state the total energy $E$ is fixed, so stiffness cannot change how much energy the leg has to give back, only the direction in which it gives it. A stiffer spring compresses less, so the leg sweeps through a smaller angle during stance and the takeoff velocity is rotated closer to the touchdown mirror, which is steeper. The vertical component grows and the horizontal one pays for it: $v_x$ falls from $4.20\ \mathrm{m/s}$ at $12\ \mathrm{kN/m}$ to $3.60\ \mathrm{m/s}$ at $40\ \mathrm{kN/m}$. "Stiffer is better" is therefore true for flight time alone and false for running, which also has to go forward.</p><p>The two root-finds give the real bounds. Solving $v_y(k_{\rm leg})=0$ gives $k_{\rm leg}=11.09\ \mathrm{kN/m}$: below that the leg cannot return the body to rest length rising, there is no flight, and by Proposition 1.2 the gait is no longer running. Solving $F_z^{\max}(k_{\rm leg})=3mg$ gives $k_{\rm leg}=19.3\ \mathrm{kN/m}$, where $t_{\rm f}=163\ \mathrm{ms}$; past it the peak leaves the $2$-$3$ body-weight band of <a class="secref" href="#stance">&#167;3</a> and section 9's loading argument starts to bite. The useful stiffness is set by a constraint, not by an optimum, and the sweep is the only way to see that. A genuine interior optimum does exist for this model, but it needs the periodicity closure of K2: once touchdown is no longer free but must be reproduced step after step, stiffness and angle of attack are coupled and the trade-off closes.</p></div></details></div>
```

### B2. Section 6 and Figure 7 give the countermovement jump 34 cm; Lab 2 computes 32.0 cm

Location: `module09.html:217` (Figure 7 caption), `module09.html:219` (prose).

Quoted (line 219): "The CMJ reliably wins - by a few centimetres, here $34$
against $30\ \mathrm{cm}$ (Fig. 7, right)."

Quoted (line 217): "so it carries more area above body weight, a larger impulse,
and by (5.2) a higher takeoff: ~34 cm against ~30 cm. Heights are computed from
each curve's impulse".

Factual error. The caption says the heights are computed from the curves'
impulses, and Lab 2 (`module09.html:343-366`) is the code that does exactly
that. Running it prints `squat jump (symmetric) h = 30 cm` and
`countermovement (front) h = 32 cm`, and the line 368 lab output text agrees:
"the symmetric push-off clears $30\ \mathrm{cm}$ and the front-loaded one
$32\ \mathrm{cm}$". The whole `profile(front)` family maxes at 32.4 cm (at
`front = 0.7`), so no member of it reaches 34 cm. Reproduced exactly:
`v_0 = 2.428` and `2.507` m/s, `h = 30.04` and `32.05` cm.

Replacement for the second half of line 219, from "The CMJ reliably wins":

```html
The CMJ reliably wins, and the same computation that produced Fig. 7 says by how much: $32.0$ against $30.0\ \mathrm{cm}$, a gain of $2.0\ \mathrm{cm}$ from a net impulse that is only $3.3\%$ larger ($175.5$ against $169.9\ \mathrm{N\,s}$). The amplification is (6.1) at work: $h\propto v_0^2$, so a $3.3\%$ impulse gain buys a $6.7\%$ height gain.
```

Replacement for the corresponding clause of the Figure 7 caption (line 217),
from "so it carries more area" to "each curve's impulse":

```html
so it carries more area above body weight, a larger impulse, and by (5.2) a higher takeoff: $32.0$ cm against $30.0$ cm. Both heights are computed from each curve's net impulse by Lab 2 of &#167;10
```

### B3. Section 9's four headline numbers rest on two values stated nowhere

Location: `module09.html:285` (prose), `module09.html:592-606` (Appendix
parameter table).

Quoted (line 285): "A stiff surface ($k_{\rm c}\approx200\ \mathrm{kN/m}$,
barefoot on concrete) gives an impact peak near $1.8$ body weights delivered in
about $10\ \mathrm{ms}$ - a loading rate of order $185$ body weights per second
- while a cushioned shoe or grass ($k_{\rm c}\approx40\ \mathrm{kN/m}$) spreads
the same landing over $22\ \mathrm{ms}$ at $0.8$ body weights, a loading rate
near $37$: about five times gentler".

Fails the evidence-grading rule of the brief: every number must be derived from
stated inputs, be a table parameter with its symbol and unit, or be labelled an
assumption. Equation (9.1) needs three inputs, and only `k_c` is given.
Back-solving the quoted rise times gives `m_imp = 8.11` and `7.85` kg, and the
quoted peaks then give `v_imp = 0.971` and `0.981` m/s, so the intended values
are `m_imp = 8` kg and `v_imp = 1.0` m/s. Substituting them forward reproduces
every quoted figure: `F_peak = 1264.9 N = 1.84 BW` and `565.7 N = 0.82 BW`;
rise times `9.9` and `22.2` ms; rates `185.4` and `37.1` BW/s, a ratio of
exactly 5.0. Both values are modelling choices, not anatomy (foot plus shank of
a 70 kg adult is nearer 4.3 kg by Winter's fractions; 8 kg is an *effective*
impact mass), so they must be labelled as assumptions and put in the table.

Replacement for line 285:

```html
<p>The numbers make the case for a soft contact. Take an effective impact mass $m_{\rm imp}=8\ \mathrm{kg}$ and a vertical closing speed $v_{\rm imp}=1.0\ \mathrm{m/s}$ at first contact; both are assumed here, and $m_{\rm imp}$ is an effective mass, larger than the anatomical foot-plus-shank because the contact also has to arrest part of the thigh and trunk through a stiff, not yet yielding, joint chain. With those two numbers (9.1) does the rest. A stiff surface ($k_{\rm c}\approx200\ \mathrm{kN/m}$, barefoot on concrete) gives an impact peak $F_{\rm peak}=1.0\sqrt{2\times10^{5}\times8}=1265\ \mathrm N=1.8$ body weights, delivered in a rise time $t_{\rm r}=\tfrac{\pi}{2}\sqrt{8/2\times10^{5}}=9.9\ \mathrm{ms}$ - a loading rate of $185$ body weights per second - while a cushioned shoe or grass ($k_{\rm c}\approx40\ \mathrm{kN/m}$) spreads the same landing over $22.2\ \mathrm{ms}$ at $566\ \mathrm N=0.8$ body weights, a loading rate of $37$: exactly five times gentler, the factor $200/40$ that (9.1) predicts for the rate. And the rate, not just the peak, is what tissue feels, because bone is strain-rate sensitive - stiffer and more brittle when loaded fast (the dynamic response Module 2 deferred).</p>
```

Add three rows to the Appendix parameter table (after the "Impact loading rate"
row, line 606):

```html
<tr><td>Effective impact mass $m_{\rm imp}$</td><td>$8\ \mathrm{kg}$ (assumed)</td><td>&#167;9, K8</td></tr>
<tr><td>Impact closing speed $v_{\rm imp}$</td><td>$1.0\ \mathrm{m/s}$ (assumed)</td><td>&#167;9, K8</td></tr>
<tr><td>Contact stiffness $k_{\rm c}$</td><td>$\sim200\ \mathrm{kN/m}$ stiff, $\sim40\ \mathrm{kN/m}$ soft</td><td>&#167;9, K8</td></tr>
```

### B4. The average landing force is called the peak in four places

Location: `module09.html:267` (Figure 10 caption and its aria-label),
`module09.html:440` and `:442` (C8 statement and solution), `module09.html:517`
and `:519` (K6 statement and solution).

Quoted (line 267, caption): "by the work-energy form of (5.1), the peak force is
F&#8776;&#189;m vland&#178;/d+mg". Quoted (line 267, aria-label): "peak landing
force in body weights against stopping distance". Quoted (line 442, C8):
"the peak force is $\bar F\approx\tfrac12 m v_{\rm land}^2/d + mg$". Quoted
(line 517, K6): "find the minimum stopping distance that keeps the peak landing
force below a tissue-tolerance threshold".

Fails part 1 (a precise statement). Proposition 8.1 (line 259) derives an
*average* force and says so twice, D10 (line 492) says "average", and line 271
makes the distinction load-bearing: "Proposition 8.1 is a statement about the
average force. Real landings also carry a brief, much higher spike at first
contact ... and that spike, not the average, is what most threatens the
tissues." Section 9 exists to model that spike. Four places contradict the one
sentence the next section is built on. C8's *question* also asks "how does the
peak force scale with the give", so the question is wrong, not only the answer.

Replacement for the Fig. 10 caption clause (line 267), from "by the work-energy
form" to "cuts it to ~2":

```html
by the work-energy form of (5.1), the average force over the stop is F&#772;=&#189;m vland&#178;/d&#8347;+mg, inversely proportional to how far the centre of mass travels while stopping. A stiff, straight-legged landing (d&#8347;&#8776;5 cm) averages ~11 body weights; bending the knees to stop over d&#8347;&#8776;40 cm cuts it to ~2. The brief spike at first contact is higher still, and is the subject of section 9.
```

and its aria-label clause "peak landing force in body weights against stopping
distance" becomes "average landing force in body weights against stopping
distance".

Replacement for C8 (lines 440 and 442):

```html
<div class="prob"><b>C8.</b> Two people drop from the same height; one lands stiff-legged, one bends deeply. Why is the second far safer, and how does the <em>average</em> force over the stop scale with the give? <span class="small"><em>Probes: <a class="secref" href="#landing">&#167;8</a>.</em></span>
```

```html
<details class="sol"><summary>Solution</summary><div>Both must remove the same downward momentum, so the same impulse; but the average force over the stop is $\bar F=\tfrac12 m v_{\rm land}^2/d_{\rm s} + mg$, inversely proportional to the stopping distance $d_{\rm s}$. Bending the knees to stop over $40\ \mathrm{cm}$ instead of a stiff $5\ \mathrm{cm}$ - eight times the distance - cuts the average from about $11$ body weights to about $2$. Nothing about the drop changed; only the distance over which it was absorbed. The instantaneous peak is higher than this average in both cases, and by (9.1) it is higher again for the stiff landing, so the ranking the average gives is if anything conservative.</div></details></div>
```

K6's statement and solution are replaced in B8 below, with "peak" corrected to
"average" there.

### B5. The section 5 impulse split quotes three numbers from an unstated parameterization

Location: `module09.html:191`.

Quoted: "Integrating the computed stance confirms the split exactly: the
vertical GRF impulse is $183.2\ \mathrm{N\,s}$, matching the weight impulse
$mg\,t_{\rm c}=116.1\ \mathrm{N\,s}$ plus the momentum reversal
$2m v_y=67.1\ \mathrm{N\,s}$".

Fails part 5 (a tie to something concrete) and the evidence-grading rule. The
three numbers are mutually exact - `116.1 + 67.1 = 183.2` to the digit - but
nothing in the module says which stance produced them, and the Figure 6 caption
explicitly disclaims the parameters of Figures 4 and 5 without supplying its
own. A reader cannot reproduce them. The two inputs are recoverable from the
numbers themselves: `t_c = 116.1/(70 x 9.81) = 0.1691 s` and
`v_y = 67.1/(2 x 70) = 0.4793 m/s`. Stating those two makes the whole line
derived from stated inputs.

Replacement for the first sentence of line 191:

```html
Integrating the computed stance confirms the split exactly. That stance has contact time $t_{\rm c}=0.169\ \mathrm s$ and takeoff speed $v_y=0.479\ \mathrm{m/s}$ (a steady-state parameterization chosen so the endpoints mirror; the values differ from the illustrative run of Figs. 4-5), so the vertical GRF impulse is $183.2\ \mathrm{N\,s}$, matching the weight impulse $mg\,t_{\rm c}=116.1\ \mathrm{N\,s}$ plus the momentum reversal $2m v_y=67.1\ \mathrm{N\,s}$ (Fig. 6, top).
```

### B6. K10's solution claims a crossover its own exercise cannot deliver

Location: `module09.html:535`.

Quoted: "Their intersection is the crossover, and it falls near the observed
transition at $\mathrm{Fr}\approx\tfrac12$ - well below the kinematic ceiling
$\mathrm{Fr}=1$."

Fails part 1 and part 4. The crossover speed of two invented cost curves is
whatever their free parameters make it; nothing in the exercise forces it to
`Fr = 0.5`. Building one toy pair of the shape the solution prescribes (walking
cost rising as `Fr^2/(1 - 0.85 Fr)`, running cost near-flat at
`3.9 + 0.05 v`) puts the crossover at `v = 2.64 m/s`, `Fr = 0.71`, not 0.5. The
honest statement is that `Fr = 0.5` is an observation the model must be
*calibrated to*, not a result it produces - which is exactly the
kinematic-versus-energetic distinction section 4 already makes carefully at line
169 and which this solution undoes.

Replacement for line 535 (the solution body):

```html
<details class="sol"><summary>Solution</summary><div>Model walking cost as rising steeply with speed (pendular collision losses growing as the vault is pushed toward its $\mathrm{Fr}=1$ limit) and running cost as flatter (elastic return capping the per-distance work); plot both against speed. Their intersection is the crossover. Where it lands is set entirely by the two curves' free parameters, and that is the point of the problem: with one plausible pair - walking cost $\propto\mathrm{Fr}^2/(1-0.85\,\mathrm{Fr})$, running cost near-flat - the crossover falls at $v=2.6\ \mathrm{m/s}$, i.e. $\mathrm{Fr}=0.71$, and small changes to either curve move it. So the observed $\mathrm{Fr}\approx\tfrac12$ is not a prediction of this model; it is the number the model must be <em>calibrated</em> to, and calibrating it is what fixes the otherwise free running-cost offset. What the exercise does deliver without calibration is the qualitative structure and one hard bound: two competing regimes produce a crossover at all, and it must lie below the kinematic ceiling $\mathrm{Fr}=1$ of (4.2), because past that ceiling walking is not available at any cost. Keeping the derived ceiling and the fitted transition apart is the same discipline <a class="secref" href="#flight">&#167;4</a> applies.</div></details>
```

### B7. K4's solution attributes its optimum to a mechanism outside the model

Location: `module09.html:511`.

Quoted: "Height rises with front-loading because reaching the peak earlier fills
more area under the force-time curve at the same ceiling - but real muscle
cannot rise infinitely fast, so the useful optimum is set by how quickly force
can be developed."

Fails part 3 and part 4. The figure's hump is real - it is the only K figure
that survives the check - but the reason given for it is not. Sweeping Lab 2's
`profile(front)` family gives `h = 23.28, 25.95, 28.72, 30.04, 31.19, 32.05,
32.38, 31.86, 30.04, 26.29, 20.02, 11.30` cm as `front` runs `1.5, 1.3, 1.1,
1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2`. The maximum is interior, at
`front = 0.7`, `h = 32.38` cm, and it is produced by the model itself: past
`front = 0.7` the profile does not merely front-load, it *narrows*, and the area
it loses at the end of the push-off exceeds the area it gains at the start. No
muscle rate limit is needed, and invoking one hides a real property of the
parameterization behind an unmodelled excuse.

Replacement for line 511 (the solution body):

```html
<details class="sol"><summary>Solution</summary><div>Parametrise the profile by how front-loaded it is, compute the height from each profile's net impulse, and search for the maximum under the fixed peak-force ceiling. The sweep gives $h=25.95,\ 30.04,\ 32.05,\ 32.38,\ 30.04,\ 20.02\ \mathrm{cm}$ at front-loading $1.3,\ 1.0,\ 0.8,\ 0.7,\ 0.5,\ 0.3$: an interior maximum at $0.7$, worth $32.4\ \mathrm{cm}$ against the symmetric $30.0$. The optimum is a property of the model, not of muscle. Front-loading helps at first because reaching the ceiling earlier fills more area under the force-time curve at the same peak. Past $0.7$ the same shape parameter also <em>narrows</em> the pulse, and the area lost off the end of the push-off outgrows the area gained at the start; the two effects balance at $0.7$. A real jumper meets a second, tighter limit that this profile family does not model - force cannot rise infinitely fast - so the physiological optimum sits at less front-loading than $0.7$, and the gap between the two is the honest measure of what the impulse argument alone can claim.</div></details>
```

### B8. Nine of the ten computational solutions state no computed number

Location: `module09.html:497-535` (K1 to K10); only K3 (line 507) states a
number.

Quoted (line 495): "Each K problem extends a lab of section 10; none is a
substitution into a boxed formula." Quoted (line 403): "computational (K) for
the science that only emerges by running the model."

Fails part 5. The problems themselves pass the depth standard of `CLAUDE.md` -
each requires simulation, optimization, an inverse solve, a sensitivity sweep or
a regime comparison, and none is plug-in arithmetic. But a solution that
describes a method and reports no result cannot be checked, and B1 is what that
permits: K1's false claim survived every one of the eleven hardening gates
because there was no number to disagree with. Modules 8 and 10 set the same
precedent, so this is a course-wide drift, not a Module 9 invention. The fix
that matches the sibling convention is one computed, verified number per
solution rather than ten new code blocks; the numbers below are all printed by
`m09/genK.py`.

K1, K4 and K10 are replaced above. The remaining six solution bodies:

K2 (line 503), replacing "Bisect or Newton-iterate to the root where the
asymmetry vanishes - the fixed point of the stance map, a genuine periodic
gait.":

```html
Bisect or Newton-iterate to the root where the asymmetry vanishes - the fixed point of the stance map, a genuine periodic gait. At $k_{\rm leg}=15\ \mathrm{kN/m}$, $v_x=4.0\ \mathrm{m/s}$ and $|v_y|=0.7\ \mathrm{m/s}$ the asymmetry $v_y^{\rm to}-|v_y^{\rm td}|$ runs from $+1.37\ \mathrm{m/s}$ at $\alpha_0=58^\circ$ to $-1.47\ \mathrm{m/s}$ at $80^\circ$, crossing zero at $\alpha_0=68.2^\circ$; that stride has $t_{\rm c}=0.192\ \mathrm s$, $t_{\rm f}=0.143\ \mathrm s$ and duty factor $\beta=0.29$, comfortably inside the running regime of Proposition 1.2.
```

K3 (line 507), replacing "$\approx-4$ - so a $+5\%$ mass error shifts the
estimated height by roughly $-20\%$":

```html
$=-4.42$ for Lab 2's push-off ($t_{\rm p}=0.30\ \mathrm s$, $v_0=2.43\ \mathrm{m/s}$) - so a $+5\%$ mass error shifts the estimated height from $30.04$ to $24.04\ \mathrm{cm}$, a $-20.0\%$ change
```

K5 (line 515), replacing "and because $h\propto v_0^2\propto(\text{impulse})^2$
the height gain is amplified relative to the impulse gain":

```html
and because $h\propto v_0^2\propto(\text{impulse})^2$ the height gain is amplified relative to the impulse gain: net impulse $169.9\to175.5\ \mathrm{N\,s}$ is $+3.3\%$, and height $30.04\to32.05\ \mathrm{cm}$ is $+6.7\%$, twice as much, as the square demands
```

K6 (lines 517 and 519), statement and solution, with "peak" corrected to
"average" per B4 and the stopping distance renamed per B9:

```html
<div class="prob"><b>K6.</b> For a range of drop heights, find the minimum stopping distance $d_{\rm s}$ that keeps the <em>average</em> landing force below a tissue-tolerance threshold. <span class="small"><em>Probes: <a class="secref" href="#labs">Lab 3</a>; inverse / design.</em></span>
```

```html
<details class="sol"><summary>Solution</summary><div>Invert $\bar F=\tfrac12 m v_{\rm land}^2/d_{\rm s}+mg\le F_{\rm tol}$ for $d_{\rm s}$: $d_{\rm s}\ge\tfrac12 m v_{\rm land}^2/(F_{\rm tol}-mg)$, with $v_{\rm land}=\sqrt{2gh_{\rm drop}}$. Substituting $v_{\rm land}^2=2gh_{\rm drop}$ collapses the whole expression to $d_{\rm s}\ge mgh_{\rm drop}/(F_{\rm tol}-mg)$, exactly linear in drop height with every other quantity in the constant. Taking $F_{\rm tol}=6mg$ as the assumed tolerance, the constant is $\tfrac15$: the required give is $4,\ 8,\ 12,\ 16,\ 20\ \mathrm{cm}$ for drops of $0.2,\ 0.4,\ 0.6,\ 0.8,\ 1.0\ \mathrm m$. So a landing that is safe from a low box demands a proportionately deeper flex from a high one, and the deepest squat a person can control - roughly $40\ \mathrm{cm}$ of centre-of-mass travel - caps the drop at about $2\ \mathrm m$ at this tolerance. This is a design inversion: solving for the give a safe landing needs, and then reading off the height at which the give runs out.</div></details></div>
```

K7 (line 523), replacing "so near the healthy $R\approx0.92$ a small loss of
resilience already costs a large fractional rise in muscular work":

```html
so near the healthy $R\approx0.92$ a small loss of resilience already costs a large fractional rise in muscular work. Numerically: at $R=0.92$ the economy factor is $25.0$ and the sensitivity $2/(1-R)^2=312.5$; at $R=0.80$ they are $10.0$ and $50.0$, a sensitivity six times smaller. Dropping resilience by four points, $0.92\to0.88$, raises the muscle's work per step from $2.48$ to $3.72\ \mathrm J$ - fifty percent more work for a four-percent worse spring
```

K8 (line 527), replacing "Because the rate scales linearly with $k_{\rm c}$ but
the peak only as $\sqrt{k_{\rm c}}$, softening the contact buys a large
reduction in loading rate for a smaller reduction in peak - quantifying why
cushioning targets the rate.":

```html
Because the rate scales linearly with $k_{\rm c}$ but the peak only as $\sqrt{k_{\rm c}}$, softening the contact buys a large reduction in loading rate for a smaller reduction in peak: halving $k_{\rm c}$ halves the rate but cuts the peak by only $1-1/\sqrt2=29\%$. With the section 9 values $m_{\rm imp}=8\ \mathrm{kg}$ and $v_{\rm imp}=1.0\ \mathrm{m/s}$, a tolerance of $100$ body weights per second admits $k_{\rm c}\le107.9\ \mathrm{kN/m}$, where the peak is $1.35$ body weights - against $1.84$ body weights and $185$ per second on the $200\ \mathrm{kN/m}$ concrete. Cushioning bought a $46\%$ cut in rate for a $27\%$ cut in peak, which is why cushioning is specified against the rate.
```

K9 (line 531), replacing "The steepness of $N(\sigma)$ means a small stress
increase (a stiffer stride, a harder surface) sharply shortens the safe mileage
- a dose calculation, not a single evaluation.":

```html
Assume a Basquin-type curve $N(\sigma)=N_0(\sigma_0/\sigma)^{1/b}$ with $N_0=10^4$ cycles at $\sigma_0=60\ \mathrm{MPa}$ and exponent $b=0.12$ (assumed; the exponent is what a real study would measure), and $700$ loading cycles per kilometre for one limb. At a per-step stress of $45\ \mathrm{MPa}$ that gives $N=1.10\times10^5$ cycles, or $157\ \mathrm{km}$ - about $39\ \mathrm{km}$ per week if the damage must not close within four weeks. Raise the per-step stress to $50\ \mathrm{MPa}$, an eleven percent change, and $N$ falls to $4.6\times10^4$: $65\ \mathrm{km}$, or $16\ \mathrm{km}$ per week. An eleven percent stiffer stride costs a factor $2.4$ in safe mileage. That steepness is the whole point: the dose, not one bad step, is what fractures the bone, and the dose depends violently on a quantity a runner changes without noticing.
```

### B9. Three symbols carry two meanings, and the Appendix records two of them in one row

Location: `module09.html:583` and `:586-587` (Appendix rows),
`module09.html:209-219` and `:259-267` (the `d` collision),
`module09.html:260-263` and `:280-283` (the `\Delta t` collision),
`module09.html:201-219` and `:517-519` (the `h` collision).

Quoted (line 583): "$t_{\rm p},\ d$ | push-off time and the push-off /
stopping distance | &#167;6, &#167;8".

Fails the brief's notation rule: "a symbol means one thing for the whole module
and a cross-section collision is a defect (flagging a collision is not resolving
it)". This row is the collision written down rather than fixed. Three
collisions:

1. `d` is the push-off distance in (6.2) and the stopping distance in (8.1), and
   both appear inside integrals and inside the same `1/d` reasoning. Resolve by
   renaming the stopping distance to `d_s` throughout section 8, Lab 3, Fig. 10,
   C8 and K6.
2. `\Delta t` is the stopping time in (8.1) and the impact rise time in the
   Proposition 9.1 proof. Resolve by naming the rise time `t_r` and keeping
   `\Delta F/\Delta t` as the loading-rate symbol, defined as `F_peak/t_r`.
3. `h` is the jump height in (6.1) and the Appendix and the drop height in K6.
   Resolve by writing `h_drop` in K6.

Replacement for the Proposition 9.1 statement and proof (lines 280 and 283):

```html
$$\boxed{\;F_{\rm peak}=v_{\rm imp}\sqrt{k_{\rm c}\,m_{\rm imp}}\,,\qquad \frac{\Delta F}{\Delta t}\;\equiv\;\frac{F_{\rm peak}}{t_{\rm r}}\;\approx\;\frac{2}{\pi}\,v_{\rm imp}\,k_{\rm c}\;}\tag{9.1}$$
```

```html
<div class="proof">While the joints are still rigid the mass $m_{\rm imp}$ on the contact spring obeys simple harmonic motion, $x(t)=(v_{\rm imp}/\omega)\sin\omega t$ with $\omega=\sqrt{k_{\rm c}/m_{\rm imp}}$, starting at $x=0$ with speed $v_{\rm imp}$. The spring force is $F=k_{\rm c}x=v_{\rm imp}\sqrt{k_{\rm c}m_{\rm imp}}\,\sin\omega t$, which peaks at $F_{\rm peak}=v_{\rm imp}\sqrt{k_{\rm c}m_{\rm imp}}$ a quarter-cycle later, at the rise time $t_{\rm r}=\tfrac{\pi}{2}/\omega=\tfrac{\pi}{2}\sqrt{m_{\rm imp}/k_{\rm c}}$ (the subscript keeps it distinct from the stopping time $\Delta t$ of <a class="secref" href="#landing">&#167;8</a>). The mean loading rate is therefore $F_{\rm peak}/t_{\rm r}=\tfrac{2}{\pi}v_{\rm imp}\,k_{\rm c}$, in which the mass cancels. The peak scales as $\sqrt{k_{\rm c}}$ and the loading rate as $k_{\rm c}$. <span class="qed">&#8718;</span></div>
```

Replacement for the two Appendix rows (lines 583 and 586-587):

```html
<tr><td>$t_{\rm p},\ d$</td><td>push-off time and push-off distance</td><td>&#167;6</td></tr>
```

```html
<tr><td>$v_{\rm land},\ \bar F,\ d_{\rm s},\ \Delta t$</td><td>landing speed, average landing force, stopping distance, stopping time</td><td>&#167;8</td></tr>
<tr><td>$v_{\rm imp},\ m_{\rm imp},\ k_{\rm c}$</td><td>impact closing speed, effective impact mass, contact stiffness</td><td>&#167;9</td></tr><tr><td>$F_{\rm peak},\ t_{\rm r},\ \Delta F/\Delta t$</td><td>impact-force peak $v_{\rm imp}\sqrt{k_{\rm c}m_{\rm imp}}$, its rise time, and the loading rate $F_{\rm peak}/t_{\rm r}$</td><td>&#167;9</td></tr>
```

Proposition 8.1 and its proof (lines 260 and 263) take `d_s` for `d`, as do the
Lab 3 code variable, the Figure 10 axis label and aria-label, C8 and K6.

### B10. Section 3's stiffness sweep quotes a band its own low endpoint is outside

Location: `module09.html:141`.

Quoted: "integrating (2.1) as $k_{\rm leg}$ runs from $11$ to $26\
\mathrm{kN/m}$ (jogging touchdown, $\alpha_0=70^\circ$) lifts the peak from
$2.1$ to $3.6$ body weights and shortens contact from $211$ to $150\
\mathrm{ms}$ - the running-realistic band of $2$-$3$ body weights."

Fails part 1 and part 4. Two problems in one sentence. The computed range 2.1 to
3.6 is offered as "the running-realistic band of 2-3", which the upper endpoint
is outside; and root-finding `v_y(k_leg) = 0` at that touchdown state gives
`k_leg = 11.09 kN/m`, so at the quoted lower endpoint of 11 kN/m the model
produces takeoff velocity `v_y = -0.013 m/s`, i.e. no flight. By the module's own
Proposition 1.2 that is not running. Both endpoints need saying, and saying them
strengthens the section rather than weakening it, because it locates the 2 to 3
band inside the sweep instead of beside it.

Replacement for the second half of line 141, from "A stiffer leg":

```html
A stiffer leg, or a faster or steeper landing, compresses the spring more and raises the peak: integrating (2.1) as $k_{\rm leg}$ runs from $11$ to $26\ \mathrm{kN/m}$ (jogging touchdown, $\alpha_0=70^\circ$) lifts the peak from $2.1$ to $3.6$ body weights and shortens contact from $211$ to $150\ \mathrm{ms}$. The running-realistic band of $2$-$3$ body weights sits inside that sweep, at $k_{\rm leg}$ between about $11$ and $19\ \mathrm{kN/m}$. Both ends of the sweep are instructive. Below $k_{\rm leg}=11.1\ \mathrm{kN/m}$ the leg returns the body to rest length still descending: the takeoff vertical velocity is negative, there is no flight, and by Proposition 1.2 the gait has left the running regime altogether. Above about $19\ \mathrm{kN/m}$ the peak leaves the running band in the other direction, toward the loading that section 9 turns into injury risk. The model therefore brackets running from both sides, which is more than the boxed relation alone shows.
```

### B11. Section 4's illustrative takeoff velocity belongs to no stated run

Location: `module09.html:157`.

Quoted: "For a jog leaving the ground at $v_y\approx0.9\ \mathrm{m/s}$ and
$v_x\approx4\ \mathrm{m/s}$, (4.1) gives $t_{\rm f}\approx0.18\ \mathrm s$, an
apex only about $4\ \mathrm{cm}$ above takeoff, and a flight range near
$0.7\ \mathrm m$".

The three outputs are correct (`t_f = 0.1835 s`, `h_apex = 4.13 cm`,
`d_f = 0.734 m`), but `v_y = 0.9 m/s` is neither derived nor tabled nor labelled
an assumption, and it matches no run in the module: Lab 1 at the Appendix's
`k_leg = 15 kN/m` gives `v_y = 0.457 m/s`, and section 5's stance gives 0.479.
It is a representative value and must say so.

Replacement for the first clause of line 157:

```html
Take a jog leaving the ground at $v_y\approx0.9\ \mathrm{m/s}$ and $v_x\approx4\ \mathrm{m/s}$ - a representative takeoff, faster in the vertical than the illustrative SLIP runs of Figs. 4 and 6, which leave at $0.46$ and $0.48\ \mathrm{m/s}$, and chosen here so the flight is visible on the page. Then (4.1) gives $t_{\rm f}\approx0.18\ \mathrm s$, an apex only about $4\ \mathrm{cm}$ above takeoff, and a flight range near $0.7\ \mathrm m$ (Fig. 5, left).
```

### B12. The push-off distance and mean net force of section 6 have no Appendix row

Location: `module09.html:215`, `module09.html:592-606`.

Quoted: "a mean net force near $515\ \mathrm N$ over $d\approx0.40\ \mathrm m$
for a $70\ \mathrm{kg}$ jumper - launches at $v_0\approx2.4\ \mathrm{m/s}$ and
clears about $30\ \mathrm{cm}$".

The arithmetic is exact (`v_0 = sqrt(2 x 515 x 0.40 / 70) = 2.426 m/s`,
`h = 30.0 cm`), so `v_0` and `h` are derived. But `515 N` and `0.40 m` are the
inputs, and neither is derived, tabled, or labelled an assumption. The Appendix
records the outputs (`v_0 ~ 2.4 m/s, h ~ 30 cm`) and not the inputs. Add two
rows after the "Vertical jump" row (line 601):

```html
<tr><td>Push-off distance $d$</td><td>$\approx0.40\ \mathrm m$ (assumed)</td><td>&#167;6, K4</td></tr>
<tr><td>Mean net push-off force</td><td>$\approx515\ \mathrm N$ (assumed)</td><td>&#167;6</td></tr>
```

and add a row for Lab 2's push-off duration, which K3's `-4.42` depends on:

```html
<tr><td>Push-off duration $t_{\rm p}$</td><td>$0.30\ \mathrm s$ (assumed)</td><td>Lab 2, K3, K5</td></tr>
```

### B13. The module never places its models on the level ladder

Location: `module09.html:123` (the end of section 2).

The brief requires that "each module states which level its models sit on", and
"a Level-1 statics estimate presented as a dynamic result is a defect". Module 9
never names a level. It matters more here than elsewhere because the module runs
three different levels side by side: (4.2) is a one-line statics balance,
Propositions 2.1 to 3.1 are a two-degree-of-freedom nonlinear ODE integrated
numerically, and (9.1) is a linear one-degree-of-freedom collision. No module in
the course currently states its level, so this is a course-wide gap; the
sentence below is the Module 9 half of it.

Insert at the end of line 123, after "locates the walk-to-run transition.":

```html
 Where this sits on the level ladder: the SLIP stance and flight of (2.1)-(2.3) are a Level-3 model - a nonlinear multi-degree-of-freedom system integrated in time, with no control and no actuator dynamics - while the Froude ceiling (4.2) is a Level-1 static balance and the impact law (9.1) a Level-2 linear oscillator. The module never mixes them: each result is used only at its own level, and the two places where a lower-level answer is handed to a higher-level question - the walk-to-run transition of <a class="secref" href="#flight">&#167;4</a> and the impact transient of <a class="secref" href="#impact">&#167;9</a> - say so explicitly.
```

### B14 to B16. Three figures draw a curve their own text contradicts

Found in a second pass that decoded every `<polyline>` point string back into
data: calibrate from the figure's own tick `<text>` coordinates, invert the
mapping, and compare the recovered numbers against the model the caption or the
solution claims. All three passed all nine gates - a wrong-signed slope is not a
delimiter error, not a label over a curve, and not a clipped viewBox.

**B14. `module09.html:217` - Fig. 7's countermovement curve is still the
superseded 34 cm.** B2 changed the figure's label (`CMJ &#8594; 34 cm`), its
aria-label and its caption to the computed `32.0 cm`, but not the curve. Decoded
against its own axis (`y = 260 - (220/3) F`, `x = 380 + 270 t/T_p`), the squat-jump
curve reproduces Lab 2's `profile(1.0)` to within `0.018` BW and integrates to
`170.0 N s` and `30.06 cm` - right. The CMJ curve matches no `profile(front)`
(closest is `front = 0.8`, off by `0.28` BW) and integrates to `181.0 N s` and
`34.06 cm`. The caption asserts "Both heights are computed from each curve's net
impulse by Lab 2", which was false for one of the two curves. Replacement: the
curve redrawn as Lab 2's own `profile(0.8)` on the same 80-point grid, which
integrates to `175.5 N s` and `32.04 cm` - the prose's numbers exactly.

**B15. `module09.html:518` - K6's figure draws the required stopping distance
*falling* with drop height.** Its polyline is byte-identical to K3's descending
sensitivity line at `:506`: a straight line from `(48,44)` to `(262,150)`, i.e.
maximum give for the smallest drop. K6's own solution derives
`d_s >= m g h_drop/(F_tol - mg) = h_drop/5`, which rises. The figure also carried
no tick labels at all, so nothing on the plot could contradict it, and its
aria-label still said "peak force" after B8d had renamed the quantity to the
average. Replacement: the computed line `d_s = h_drop/5` from `(48,150)` to
`(262,65.2)`, tick labels on both axes (`0, 0.5, 1.0 m`; `0, 10, 20 cm`), the
five tabulated points `4, 8, 12, 16, 20 cm` marked, and a corrected aria-label.

**B16. `module09.html:534` - K10's figure draws the running cost *falling* with
speed.** The red curve runs from `(48,90)` to `(250,114)`: cost decreasing. The
exercise's own model, which B6 put in the solution, is `C_run = 3.9 + 0.05 v` -
rising slowly - crossing a walking cost `C_walk = 2 + 1.6 Fr^2/(1 - 0.85 Fr)`
that rises steeply toward the Froude ceiling. A crossover between a rising and a
falling curve is not the crossover the solution explains. Replacement: both
curves computed from those two expressions over `v = 0.8` to `3.3 m/s`, the
crossover marked at the computed `v = 2.62 m/s` (`Fr = 0.70`), speed ticks added,
and the `Fr = 1` kinematic ceiling at `v = 3.13 m/s` drawn as a dashed line so
the figure carries the one bound the exercise delivers without calibration.

## 3. Style and clarity edits

Line-level. Apply in one pass.

1. `module09.html:92` "its net action is remarkably spring-like" &rarr; "its net
   action is spring-like to within a few percent over a stance". Hype word
   without a number attached; the brief bans "remarkably" and the sentence is
   stronger with the qualifier.
2. `module09.html:56` "it is worth stating in advance because everything after
   Section 5 is a variation on it" &rarr; "state it in advance, because
   everything after section 5 is a variation on it". Removes an announcing
   clause; the section reference also uses a capital S here and lower case
   everywhere else.
3. `module09.html:141` "the running-realistic band" is repaired in B10.
4. `module09.html:207` "with no downward momentum to reverse, the factor is
   simply $1/m$" &rarr; "with no downward momentum to reverse, the factor is
   $1/m$". "Simply" adds nothing and the contrast with $1/2m$ carries the point.
5. `module09.html:219` "The CMJ reliably wins - by a few centimetres" is
   repaired in B2; "a few centimetres" becomes the computed 2.0 cm.
6. `module09.html:231` "storing $U\approx31\ \mathrm J$ (Fig. 8, right, and the
   energy budget of Module 6)" &rarr; "storing $U\approx31\ \mathrm J$ (the
   toe-plus-linear tendon model of Module 6, evaluated at $5\ \mathrm{kN}$: its
   $4\ \mathrm{kN}$ point is $13.4\ \mathrm{mm}$ and $20.2\ \mathrm J$)". I
   reproduced 31 J from Module 6's own model, so the citation should say which
   model and at what load rather than gesture at a budget.
7. `module09.html:239` "about $2U\approx62\ \mathrm J$ of muscle mechanical work
   per step, and because both negative and positive muscle work carry a
   metabolic price, all of it costs" &rarr; "about $2U\approx62\ \mathrm J$ of
   muscle mechanical work per step, and both the negative and the positive half
   carry a metabolic price". The trailing "all of it costs" restates the clause
   before it.
8. `module09.html:265` "Nothing about the drop changed; only the distance over
   which it was absorbed." Keep, but the same sentence also closes C8 verbatim
   (line 442). Vary one of them; C8's solution should not read as a paste of
   section 8.
9. `module09.html:271` "Real landings also carry a brief, much higher spike at
   first contact" &rarr; "Real landings also carry a brief spike at first
   contact, higher than the average by a factor that (9.1) will make explicit".
   The forward promise is what the next section delivers, so name it.
10. `module09.html:296` "This is why &quot;impact&quot; alone is the wrong
    villain." &rarr; "This is why impact alone is the wrong quantity to blame."
    "Villain" is a register break in an otherwise flat technical voice.
11. `module09.html:300` "each is a starting point meant to be edited" &rarr;
    "each is a starting point to be edited". Shorter, same content.
12. `module09.html:338`, `:368`, `:383`, `:397` each begin "Output:". Three of
    the four then restate a number that the code prints; that is correct and
    worth keeping. Lab 3's (line 383) prints "$11.0,\ 4.3,\ 2.7,\ 2.1$ body
    weights" with no units sentence around it; give it the same shape as the
    others: "Output: average landing forces of $11.0,\ 4.3,\ 2.7$ and $2.1$
    body weights for stops of $5,\ 15,\ 30$ and $45\ \mathrm{cm}$ - a factor
    $5.2$ across a factor $9$ in give."
13. `module09.html:403` "Thirty problems test the module, ten of each kind"
    &rarr; "Thirty problems test the module, ten of each kind, and every
    computational solution below reports a number you can check against your own
    run." After B8 that sentence is true and it tells the reader what to expect.
14. `module09.html:495` "none is a substitution into a boxed formula" is true of
    the statements as they stand and stays; after B8 it is also true of the
    solutions.
15. `module09.html:538` "It is worth naming the debts, because each is repaid"
    &rarr; "Each debt is named below, and each is repaid". Removes the
    announcing clause.
16. `module09.html:546` "What survives all of this is the essential physics"
    &rarr; "What survives is the physics the idealisations were chosen to keep".
    "Essential" is doing no work; the replacement says which physics and why.
17. The aria-labels at lines 48, 52, 74, 96, 137, 159, 193, 217, 229, 241, 267,
    287 are adequate stand-alone descriptions and stay, except the two repaired
    in B1 and B4.
18. `module09.html:591` "Round figures for a typical adult runner, used in the
    worked examples and the labs of &#167;10; each varies with individual,
    training, surface, and measurement." &rarr; append "Values marked
    (assumed) are modelling choices, not measurements." After B3 and B12 the
    table carries five such rows and the distinction should be stated once at the
    top rather than inferred from the parentheses.

## 4. Structural notes

- **Ordering is clean.** Every result the prose uses is proved before it is
  used. I mapped the dependency graph across all twelve sections and found no
  cycle and no forward jump: sections 3 and 4 consume section 2, sections 6 and
  8 consume section 5, section 7 consumes sections 2 and 6, section 9 consumes
  sections 3 and 8. The problem set only reproduces. The three cross-module
  debts (Modules 2, 6 and 8) are each named where they are incurred and again in
  the repayment ledger.
- **The impulse hinge is the right structural choice** and it is executed. Line
  195 states the plan - jumping and landing are one equation run in opposite
  directions - and sections 6 and 8 deliver it symmetrically, each opening by
  naming its mirror. That is the strongest piece of architecture in the module.
- **Section 7 is the weakest section structurally**, not mathematically.
  Proposition 7.1 is proved and correct, but the three stretch-shortening
  mechanisms at lines 248 to 250 are a bulleted list in which only the first
  carries an equation. The second is quantified indirectly through section 6's
  jump comparison; the third, the stretch reflex, carries no number, no
  timescale and no model, and it is the only claim in the module with none of the
  three. Either give it its latency (it is a short-latency reflex, so a number
  exists and Module 10 will need it anyway) or say plainly that the module states
  it without modelling it, the way section 4 handles the energetic transition.
- **The K figures are schematic and only two of them say so.** K2, K3, K6, K8
  are straight lines and are correct as straight lines, because the relations
  they draw are genuinely linear. K7 and K9 are plausible convex curves. K1 was
  a drawn hump contradicting the model (B1) and K4 a drawn hump the model
  actually produces (B7) - and nothing in either figure distinguished the two
  cases for the reader. Every K figure should carry a `<figcaption>` saying
  whether it is computed or representative; only the section figures do this now.
  The B1 replacement adds one; the other nine want the same one-line treatment.
- **K5's figure does not illustrate K5.** Its aria-label is "Squat-jump versus
  countermovement-jump energy bars" and its two bars are labelled SJ and CMJ
  against an "energy (J)" axis, but K5 asks for impulse and height, and neither
  the problem nor the solution mentions energy. Relabel the axis to "height
  (cm)" and the bars to the computed 30.0 and 32.0, or relabel the problem.
  Not blocking, because no false number is stated, but the figure earns its space
  only after one of the two changes.
- **Four labs is the right number and they are well chosen** - one per section
  spine (bounce, jump, landing, tendon) - but Lab 1 is the only one that
  integrates anything. Labs 2, 3 and 4 evaluate closed forms over a loop. That is
  fine for a lab, since the K problems carry the depth requirement, and after B8
  the K solutions show it.
- **Nothing was cut for length and nothing should be.** The module runs 643
  lines for twelve sections, which is the tightest in the course, and the density
  is right.

## 5. What already works

- **Propositions 2.1 and 2.2 are the model of the standard.** The polar
  equations are derived by projecting gravity onto $\hat{\mathbf r}$ and
  $\hat{\boldsymbol\varphi}$ with both projections written out, and the energy
  proof does the differentiation term by term and says which substitution makes
  each group cancel. I re-derived both by hand and confirmed the cancellation is
  exact, and my RK4 integration conserves (2.2) to 1 part in 10^15 over a full
  stance, which is the numerical statement of the same fact.
- **Proposition 3.1 gives two forms and then earns the second one.** The
  paragraph at line 143 uses $F_z = m(g + \ddot y)$ to explain one hump versus
  two, which is precisely what the first form hides. That is the "prove, do not
  assert" standard applied to a piece of exposition rather than a theorem.
- **Section 4 keeps a derived bound and a fitted observation apart.** Line 169
  says the $\mathrm{Fr}=1$ ceiling is kinematic and derived, that humans switch
  near $\mathrm{Fr}\approx0.5$ for energetic reasons, and that "the precise
  crossover is an energetic, not a kinematic, statement". That is the discipline
  the brief asks for and the only place in the module where a
  not-yet-modelled number is handled correctly. B6 exists because K10 undoes it.
- **All four labs print exactly what their prose claims.** Lab 1: `2.12, 2.58,
  3.06, 3.56` BW and `211, 188, 168, 150` ms against a stated "$2.1$ to $3.6$"
  and "$211$ to $150$". Lab 2: 30 and 32 cm and the sweep `30.0, 31.2, 32.0,
  32.4` against a stated `30.0 -> 32.4`. Lab 3: `11.0, 4.3, 2.7, 2.1` BW. Lab 4:
  `10.0, 16.7, 25.0, 40.0` against a stated `10.0 -> 16.7 -> 25.0 -> 40.0`. All
  four pass `pycodestyle` and none contains a live HTML tag. Every number checked
  against these blocks matched except B2's 34 cm.
- **The section-6 push-off, the section-8 landing and the section-9 impact all
  reproduce arithmetically.** `515 N` over `0.40 m` gives `2.426 m/s` and
  `30.0 cm`; the `0.5 m` drop gives `3.132 m/s`, `11.00 BW` at 5 cm and
  `2.25 BW` at 40 cm; and section 9's six numbers reproduce to the last digit
  from `m_imp = 8 kg` and `v_imp = 1.0 m/s`. The defects there (B3, B12) are that
  the inputs are unstated, not that the outputs are wrong.
- **Section 7's `U = 31 J` is not the loose number it looks like.** It
  reproduces from Module 6's own tendon model: that model's linear branch is
  `416.7 kN/m` offset by half the `7.5 mm` toe, so `5 kN` gives `15.75 mm` (the
  stated "about 16 mm") and `31.0 J` by integration, and the same model's
  `4 kN` point returns Module 6's published `13.4 mm` and `20.2 J`. The
  cross-module number is consistent to three digits.
- **Pillar 1 holds throughout.** Double support, swing phase, stance phase, duty
  factor, angle of attack, muscle-tendon unit, resilience, eccentric, concentric,
  stretch-shortening cycle, ground reaction force, loading rate and impact
  transient are each glossed in the sentence of first use. The two
  velocity-symbol collisions the prior reviewer caught (`v` in section 2, `v_y`
  in section 5) are both fixed in the file, and section 9 volunteers a third
  gloss ("distinct from the forward running speed $v$ of section 1") without
  being asked. B9's three collisions are all in the later half of the module,
  where that discipline lapsed.
- **The closing sections do their job.** The captures-and-misses table names five
  idealisations and where each is repaid, the repayment ledger closes three debts
  and opens five, and line 558 says what the reader can now do. That is the shape
  the brief asks a chapter to end in.
- **`check_probfig.py` passes on all thirty problem figures**, every problem has
  a Probes note, and the five diagnostics at line 407 test exactly the five
  results the module boxes.

## 6. Counts

- Blocking defects: 16 (B1 to B16; B14 to B16 came from the figure-decode
  pass, which inverted every polyline back into data).
- Style and clarity edits: 18.
- Figures decoded back into data and checked against the model their caption or
  solution claims: 32 (every figure carrying a polyline). Contradicted their own
  text: 3 (B14, B15, B16). Reproduced it: 29, including Fig. 10's `1/d_s` curve
  (`14.09` BW at the decoded `3.8 cm`, `1.98` BW at `50 cm`, against
  `F/mg = 1 + v^2/2 g d_s` = `14.09` and `2.00`) and K1's rebuilt sweep
  (`25.3, 93.3, 171.9, 234.5, 319.8 ms`, against the printed
  `25.4, 93.2, 171.9, 234.5, 319.9`).
- Numbers checked against code or hand derivation: 61. Mismatches: 1 (B2's
  34 cm against Lab 2's computed 32.0 cm). Unreproducible for want of a stated
  input: 9 (B3's six, B5's three). Claims contradicted by a run of the model: 2
  (B1's interior optimum, B6's `Fr = 0.5` crossover). Claims misattributed to a
  mechanism outside the model: 1 (B7).
- Code blocks extracted and run: 4 of 4 clean, 0 `NameError`, 0 live HTML tags.
- K problems judged plug-in under the `CLAUDE.md` depth standard: 0. All ten
  require simulation, optimization, an inverse solve, a sensitivity sweep or a
  regime comparison. The defect in the K set is missing verified results (B8),
  not missing depth.

## 7. Changes applied

Applied by one re-runnable script, `m09/apply.py` (80 `rep`/`repline` calls, each
asserting its anchor occurs exactly once), against a pristine
`edited/module09.html`. Line numbers are the ORIGINAL `module09.html` lines; the
edited file is still 643 lines, because no edit adds or removes one. The script
was re-run from a fresh `cp module09.html edited/module09.html` after the last
change and printed all 80 tags, so the applied state is exactly what the script
produces - not a partial run. The A tags take their geometry from
`m09/figfix.py`, which computes every coordinate, asserts each anchor is unique
in the pristine file, and writes `figfix.json`.

Before applying, every number this report asserts was re-verified by re-running
the three scratchpad scripts and all four of the module's own lab blocks.
`m09/genK.py` reproduced `knums.json` byte-identically; `m09/k1.py` reproduced
the RK4 sweep (energy conserved to `|dE/E| < 8e-15`); `m09/verify.py` reproduced
the section-5, section-6, section-8 and section-9 arithmetic; the four extracted
lab blocks printed exactly the numbers the report records. **No number in the
report disagreed with a run.** Ten places where the report's *replacement text*
was wrong or incomplete are listed under "Corrections to the report" below.

| tag | line (original) | what changed | how verified |
|---|---|---|---|
| B1a | 497 | K1's statement no longer asserts an interior optimum. "Find the stiffness that maximises flight time, and explain why an interior optimum exists" replaced with "decide from the sweep whether flight time has an interior optimum or whether the useful stiffness is set by a constraint instead", plus two root-finds (softest leg that still flies; stiffest that keeps the peak below 3 BW). Probes note changed from "simulation + optimization" to "simulation + constrained inverse". | `m09/k1.py`: RK4 at `dt=2e-5`, `numpy.diff(t_f) > 0` at every one of the 59 grid points from 11 to 40 kN/m; `\|dE/E\| < 8e-15` at every point. |
| B1b | 498 | K1's figure rebuilt. The drawn hump (polyline descending to `y=44.0` near `x=166`) and the label `optimum kleg ≈ 18 kN/m` are gone; the new polyline is the computed monotone `t_f(k_leg)` (59 points, `k_leg` 11→40 kN/m mapped to `x` 48→262, `t_f` 0→340 ms mapped to `y` 150→44), with a dashed line and marker at the computed 3-BW limit `k_leg=19.3 kN/m`, `t_f=163 ms` (`x=109.3`, `y=99.2`). aria-label and a new figcaption both state the curve is computed by RK4 and rises monotonically. viewBox tightened to `20 30 280 152`. | Polyline and marker coordinates taken verbatim from `knums["K1"]["poly"]`, `x_3bw`, `y_3bw` in `m09/knums.json`, regenerated by `m09/genK.py`. Rendered with `shoot.py` and read: monotone curve, no clipping. `check_frame` exit 0, wasted-margin count unchanged at 18. |
| B1c | 499 | K1's solution replaced. The false mechanism ("too stiff a leg barely compresses and stores little elastic energy") is gone. New solution reports the sweep `25.4→93.2→171.9→234.5→319.9 ms` at `k_leg = 12→15→20→26→40 kN/m` (still climbing at 383 ms at 60 kN/m), explains it from Prop 2.2 (fixed touchdown state ⇒ fixed energy; stiffness rotates the takeoff velocity, it does not change the store), gives the forward-speed price `v_x 4.20→3.60 m/s`, and states the two root-found bounds `k_leg = 11.09` (no flight) and `19.3 kN/m` (peak reaches 3 BW, `t_f = 163 ms`). | `m09/k1.py` printed every one of these; `m09/verify.py` independently reproduced the same sweep with a forward-Euler integrator at `dt=1e-5`. |
| B2a | 219 | "The CMJ reliably wins - by a few centimetres, here $34$ against $30\ \mathrm{cm}$" replaced with the computed "$32.0$ against $30.0\ \mathrm{cm}$, a gain of $2.0\ \mathrm{cm}$ from a net impulse only $3.3\%$ larger ($175.5$ against $169.9\ \mathrm{N\,s}$)", plus the $h\propto v_0^2$ amplification to $6.7\%$. Keeps the "(Fig. 7, right)" cross-reference. | Lab 2 (`edited/module09.html:343`) run: prints `squat jump h = 30 cm`, `countermovement h = 32 cm`. `m09/genK.py` K5 block: `J_sj=169.93`, `J_cmj=175.52` (+3.29%), `h_sj=30.038`, `h_cmj=32.046` (+6.69%) N·s and cm. |
| B2b | 217 | Fig. 7 caption: "a higher takeoff: ~34 cm against ~30 cm. Heights are computed from each curve's impulse" → "32.0 cm against 30.0 cm. Both heights are computed from each curve's net impulse by Lab 2 of §10" (named, linked). | Same Lab 2 run. |
| B2c | 217 | Fig. 7's own SVG label `CMJ → 34 cm` → `CMJ → 32 cm`. **Not in the report** — found by grepping the figure. | Same Lab 2 run. |
| B2d | 217 | Fig. 7's aria-label "34 versus 30 centimetres of height" → "32 versus 30". **Not in the report.** | Same Lab 2 run. |
| B3a | 285 | Section 9's four headline numbers now derive from stated inputs. The paragraph opens by stating `m_imp = 8 kg` and `v_imp = 1.0 m/s` as *assumed* (with a sentence on why the effective mass exceeds foot-plus-shank), then substitutes them into (9.1) in full: `F_peak = 1.0·√(2×10⁵×8) = 1265 N = 1.8 BW`, `t_r = (π/2)√(8/(2×10⁵)) = 9.9 ms`, rate 185 BW/s; soft contact `22.2 ms`, `566 N = 0.8 BW`, rate 37 — "exactly five times gentler, the factor 200/40 that (9.1) predicts". Keeps the "(Fig. 11, left)" cross-reference. | `m09/verify.py`: back-solving the module's quoted rise times gives `m_imp = 8.11` and `7.85 kg` and `v_imp = 0.971` and `0.981 m/s`; forward substitution of `8 kg`/`1.0 m/s` prints `1264.9 N = 1.84 BW, 9.9 ms, 185.4 BW/s` and `565.7 N = 0.82 BW, 22.2 ms, 37.1 BW/s`; ratio 185.4/37.1 = 5.00. |
| B3b | 606 | Three rows added to the Appendix parameter table: effective impact mass `8 kg (assumed)`, impact closing speed `1.0 m/s (assumed)`, contact stiffness `~200 / ~40 kN/m (assumed)`. | Same; the values are now the table entries B3a's derivation cites. |
| B4a | 267 | Fig. 10 aria-label: "peak landing force in body weights against stopping distance" → "average landing force …"; the `d`/`1/d` wording rephrased for a screen reader ("stopping distance", "an inverse curve"). | Proposition 8.1 (`:259`) derives $\bar F$ and says "average" twice; `:271` makes the average-vs-peak distinction load-bearing. |
| B4b–B4h | 267 | Fig. 10's in-plot labels: both `d` dimension labels → `dₛ`; `small d`/`large d` → `small dₛ`/`large dₛ`; x-axis title `stopping distance d (cm)` → `stopping distance dₛ (cm)`; y-axis title `peak force (BW)` → `average force (BW)`; the on-plot annotation `F ≈ ½mv²/d + mg` → `F̄ ≈ ½mv²/dₛ + mg`. | Rendered with `shoot.py` and read: subscripts and the overbar render correctly. `check_svg` 0 hard/0 advisory; `check_overlap` 0. |
| B4i | 267 | Fig. 10 caption: "the peak force is *F*≈½*m v*<sub>land</sub>²/*d*+*mg*" → "the **average** force over the stop is *F̄*=½*m v*<sub>land</sub>²/*d*<sub>s</sub>+*mg*"; "feels ~11 body weights" → "averages ~11"; a closing sentence added pointing the spike forward to section 9. Keeps the file's `<em>`/`<sub>` markup (the report's replacement had used bare entities). | Prop 8.1 + `:271`. |
| B4j | 440 | C8's *question* fixed: "how does the peak force scale with the give" → "how does the *average* force over the stop scale with the give". | Prop 8.1 derives the average, so the question was wrong, not only the answer. |
| B4k | 442 | C8's solution: "the peak force is $\bar F\approx…$" → "the *average* force over the stop is $\bar F=…/d_{\rm s}+mg$"; "cuts the force" → "cuts the average"; the closing sentence, which was a verbatim paste of `:265`, varied to "Same drop, same momentum; only the absorbing distance differs" (style edit 8); a new closing sentence notes the instantaneous peak exceeds the average in both cases and by (9.1) more so for the stiff landing, so the ranking is conservative. | `m09/verify.py`: `d=5 cm → 7554 N = 11.00 BW`, `d=40 cm → 1545 N = 2.25 BW`. |
| B4l–B4o | 441 | C8's figure: both `d` dimension labels → `dₛ`; `stiff (small d)`/`soft (large d)` → `dₛ`. | Rendered and read. |
| B5 | 191 | The section-5 impulse split now states the parameterization it came from: "That stance has contact time $t_{\rm c}=0.169\ \mathrm s$ and takeoff speed $v_y=0.479\ \mathrm{m/s}$ (the steady-state parameterization chosen so the endpoints mirror; the values differ from the illustrative run of Figs. 4-5)". The three quoted impulses are unchanged. | `m09/verify.py` back-solved them from the quoted numbers: `t_c = 116.1/(70×9.81) = 0.1691 s`, `v_y = 67.1/140 = 0.4793 m/s`; and `116.1 + 67.1 = 183.2` to the digit. |
| B6 | 535 | K10's solution no longer claims its crossover lands at `Fr ≈ 1/2`. Now: where the crossover lands is set by the two curves' free parameters; one plausible pair puts it at `v = 2.6 m/s`, `Fr = 0.71`; `Fr ≈ 1/2` is what the model must be *calibrated* to, not what it predicts; what the exercise does deliver without calibration is the structure plus the hard bound `Fr < 1` from (4.2). | `m09/genK.py` K10 block: walking cost `∝ Fr²/(1−0.85 Fr)`, running cost `3.9 + 0.05 v` → `v_cross = 2.6406 m/s`, `Fr_cross = 0.7108`; `v_ceiling = √(gL₀) = 3.132 m/s`. |
| B7 | 511 | K4's solution no longer attributes its (real) interior optimum to an unmodelled muscle rate limit. Now reports the sweep `h = 25.95, 30.04, 32.05, 32.38, 30.04, 20.02 cm` at front-loading `1.3, 1.0, 0.8, 0.7, 0.5, 0.3`, names `0.7` as the interior maximum, and explains it from the parameterization itself (past 0.7 the shape parameter also *narrows* the pulse, and the area lost off the end outgrows the area gained at the start). The rate limit is kept, but as a *second, tighter* limit the model does not carry. | `m09/genK.py` K4 block, which sweeps Lab 2's own `profile(front)`; Lab 2 itself prints the `1.0→0.7` half of the same sweep (`30.0, 31.2, 32.0, 32.4 cm`). |
| B8a | 503 | K2's solution now reports a result: asymmetry `+1.37 m/s` at `α₀=58°` to `−1.47 m/s` at `80°`, root at `α₀=68.2°`, that stride's `t_c=0.192 s`, `t_f=0.143 s`, duty factor `β=0.29`. | `m09/genK.py` K2 block (`a_lo`, `a_hi`, `root`, `tc`, `tf`); `β = 0.1916/(2×(0.1916+0.1427)) = 0.287` by Definition 1 + Prop 1.2's `T = 2(t_c+t_f)`. |
| B8b | 507 | K3's `≈−4` and "roughly −20%" replaced with `−4.42` for Lab 2's push-off (`t_p=0.30 s`, `v_0=2.43 m/s`) and the height shift `30.04 → 24.04 cm`, a `−20.0%` change. | `m09/verify.py` prints the analytic `−4.42` and the numeric `30.04 → 24.04 cm (−20.0%)` from re-integrating Lab 2's own force trace at `1.05 m`. |
| B8c | 515 | K5's "the height gain is amplified" now carries the numbers: net impulse `169.9 → 175.5 N·s` (`+3.3%`), height `30.04 → 32.05 cm` (`+6.7%`), "twice as much, as the square demands". | `m09/genK.py` K5 block. |
| B8d | 517 | K6's statement: "peak landing force" → "*average* landing force"; the drop height named `h_drop` and the stopping distance `d_s` (resolving the `h` and `d` collisions of B9). | Prop 8.1; B9. |
| B8e | 519 | K6's solution now inverts to the closed form `d_s ≥ m g h_drop/(F_tol − mg)`, states `F_tol = 6mg` as an assumed tolerance, gives the constant `1/5` and the table `4, 8, 12, 16, 20 cm` for drops `0.2…1.0 m`, and closes with the design reading: a ~40 cm controllable squat caps the drop near 2 m. | `m09/genK.py` K6 block: `rows` = `(0.2,…,4.0), (0.4,…,8.0), (0.6,…,12.0), (0.8,…,16.0), (1.0,…,20.0)`; `slope = 20.0 cm/m`. |
| B8f | 523 | K7's solution now gives the numbers: economy factor `25.0` and sensitivity `2/(1−R)² = 312.5` at `R=0.92`; `10.0` and `50.0` at `R=0.80`; and `W_musc 2.48 → 3.72 J` for `R 0.92 → 0.88`, "fifty percent more work for a four-percent worse spring". | `m09/genK.py` K7 block (`e92=25.0`, `d92=312.5`, `d80=50.0`, `w92=2.48`, `w88=3.72`); Lab 4 independently prints `R=0.92 → muscle 2.5 J, factor 25.0` and `R=0.88 → 3.7 J, factor 16.7`. |
| B8g | 527 | K8's solution now gives the numbers: halving `k_c` cuts the peak by only `1 − 1/√2 = 29%`; at the §9 values a `100 BW/s` tolerance admits `k_c ≤ 107.9 kN/m` where the peak is `1.35 BW`, against `1.84 BW` and `185/s` on `200 kN/m` concrete — a `46%` cut in rate for a `27%` cut in peak. | `m09/genK.py` K8 block: `kc_max=107.87`, `Fpk_at=1.3528`, `Fpk_200=1.8420`, `rate_200=185.41`, `halve_rate_peak_drop=0.2929`. |
| B8h | 531 | K9's solution now states its fatigue model and its dose: Basquin `N(σ)=N₀(σ₀/σ)^{1/b}`, `N₀=10⁴` at `σ₀=60 MPa`, `b=0.12` (labelled assumed), `700` cycles/km per limb → `N=1.10×10⁵`, `157 km`, `39 km/week` at `45 MPa`; `4.6×10⁴`, `65 km`, `16 km/week` at `50 MPa` — an eleven percent stiffer stride costing a factor `2.4` in safe mileage. | `m09/genK.py` K9 block (`N45`, `N50`, `km45`, `km50`, `wk45`, `wk50`, `ratio`); checked by hand: `(60/45)^{1/0.12} = 10.99`, `× 10⁴ = 1.10×10⁵`. |
| B9a–B9e | 259, 260, 263 (×2), 265 | `d` meant both the push-off distance of (6.2) and the stopping distance of (8.1). The stopping distance is renamed `d_s` throughout section 8: Prop 8.1's statement (with a gloss naming the distinction), the boxed (8.1), both occurrences in its proof, and the `1/d` prose. | The collision is stated in `EDITOR_DOMAIN.md`'s notation rule; the rename is mechanical, and `checktex` (715 segments, 0 issues) confirms no delimiter was broken. |
| B9f–B9i | 491 (×3), 492 (×2) | **Not in the report's rename list** — D10 *derives* Prop 8.1 and used the colliding `d` in its figure (aria-label, dimension label, on-plot `F ≈ ½mv²/d`) and twice in its solution. All renamed to `d_s`, and the on-plot annotation given the overbar `F̄`. A partial rename would have left the collision the fix exists to remove. | Found by a regex scan for a standalone `d` over the whole file (`m09/scan_d.py`), which lists every site; the push-off `d` of `:209`, `:215`, `:217`, `:484` is deliberately left alone. |
| B9j, B9k | 371, 377–379 | Lab 3: the `1/d` prose → `1/d_s`, and the code loop variable `d` → `ds` in all three lines that use it. | Lab 3 re-extracted and re-run after the edit: prints the same `11.0, 4.3, 2.7, 2.1 BW` for `5, 15, 30, 45 cm`. `check_code` 0 issues (pycodestyle). |
| B9l, B9m | 280, 283 | `Δt` meant both the stopping time of (8.1) and the impact rise time in the Prop 9.1 proof. The rise time is renamed `t_r`; the boxed (9.1) now defines the loading rate explicitly as `ΔF/Δt ≡ F_peak/t_r`; the proof glosses the distinction and derives the rate as a **display** equation rather than the long inline `$…$` that the report's replacement kept. | The display form was chosen because `verify_dom`'s swallowed-prose advisory was firing on exactly that inline expression; after the edit that advisory is **0** (baseline 1). |
| B9n–B9p | 583, 586, 587 | Appendix notation table: the collision row `$t_{\rm p},\ d$ — push-off time and the push-off / stopping distance — §6, §8` is split. It now reads `push-off time and push-off distance — §6`; the §8 row gains `d_s` ("stopping distance"); the §9 row gains `t_r` and defines the rate as `F_peak/t_r`. Recording a collision is not resolving it; it is now resolved. | Cross-checked against every renamed site above. |
| B10 | 141 | Section 3's sweep no longer offers `2.1 to 3.6 BW` as "the running-realistic band of 2-3". It now locates the 2-3 band *inside* the sweep (`k_leg ≈ 11 to 19 kN/m`) and says what each endpoint means: below `11.1 kN/m` the takeoff vertical velocity is negative — no flight, and by Prop 1.2 not running; above ~19 kN/m the peak leaves the band toward section 9's loading. | `m09/k1.py`: root-finding `v_y(k_leg)=0` gives `11.088 kN/m`, and at the quoted `11 kN/m` endpoint `v_y = −0.013 m/s`; `F_z^max(k_leg)=3mg` gives `19.310 kN/m`. |
| B11 | 157 | Section 4's `v_y ≈ 0.9 m/s` is now labelled: "a representative takeoff, faster in the vertical than the illustrative SLIP runs of Figs. 4 and 6, which leave at $0.46$ and $0.48\ \mathrm{m/s}$, and chosen here so the flight is visible on the page." The three outputs are unchanged (they were right). | `m09/k1.py` at the Appendix's `k_leg=15 kN/m`: `v_y = 0.457 m/s`; `m09/verify.py` section-5 stance: `v_y = 0.479 m/s`. Outputs re-checked: `t_f = 0.1835 s`, `h_apex = 4.13 cm`, `d_f = 0.734 m`. |
| B12 | 601 | Three rows added to the Appendix parameter table: push-off distance `≈0.40 m (assumed)`, mean net push-off force `≈515 N (assumed)`, push-off duration `t_p = 0.30 s (assumed)`. The table recorded only the *outputs* (`v_0`, `h`); these are the inputs they come from, and `t_p` is what K3's `−4.42` depends on. | Arithmetic re-checked: `v_0 = √(2×515×0.40/70) = 2.426 m/s`, `h = 30.0 cm`; `t_p = 0.30 s` is Lab 2's own `Tp`. |
| B13 | 123 | The module now places its models on the level ladder, at the end of section 2: SLIP stance and flight (2.1)-(2.3) are Level 3 (nonlinear multi-DOF integrated in time, no control, no actuator dynamics); the Froude ceiling (4.2) is Level 1 (static balance); the impact law (9.1) is Level 2 (linear oscillator) — with a note that the module never hands a lower-level answer to a higher-level question without saying so. | The three classifications were read off the equations themselves: (4.2) is a one-line vertical force balance, (2.1) a two-DOF nonlinear ODE integrated numerically in Lab 1, (9.1) a 1-DOF linear SHM quarter-cycle. |
| S1 | 92 | "its *net* action is remarkably spring-like" → "is spring-like to within a few percent over a stance". | Hype word with no number attached. |
| S2 | 56 | "it is worth stating in advance because everything after Section 5 is a variation on it" → "State it in advance, because everything after section 5 is a variation on it". Also fixes the stray capital `Section`, lower case everywhere else. | Announcing clause; case consistency. |
| S4 | 207 | "the factor is simply $1/m$" → "the factor is $1/m$". | "Simply" adds nothing; the contrast with $1/2m$ carries it. |
| S6 | 231 | "storing $U\approx31\ \mathrm J$ (Fig. 8, right, and the energy budget of Module 6)" → names the model and the load: "the toe-plus-linear tendon model of Module 6 evaluated at $5\ \mathrm{kN}$, the same model whose $4\ \mathrm{kN}$ point is Module 6's published $13.4\ \mathrm{mm}$ and $20.2\ \mathrm J$". | Reproduced from Module 6's own model by hand: linear branch `416.7 kN/m` offset by half the `7.5 mm` toe ⇒ `5 kN → 15.75 mm`, `U = 3.91 + 27.07 = 30.97 J`; `4 kN → 13.35 mm`, `U = 3.91 + 16.27 = 20.18 J`. `module06.html` states `13.4 mm` and `U_toe ≈ 20.2 J` verbatim. |
| S7 | 239 | "and because both negative and positive muscle work carry a metabolic price, all of it costs" → "and both the negative and the positive half carry a metabolic price". | "All of it costs" restated the clause before it. |
| S9 | 271 | "a brief, much higher spike at first contact" → "a brief spike at first contact - before the knee and ankle have begun to give - that is higher than the average and that (9.1) will compute". Names what the next section actually delivers (the spike), not a spike-to-average ratio (9.1) does not give. | (9.1) computes `F_peak`, not `F_peak/F̄`; the report's proposed wording ("higher by a factor that (9.1) will make explicit") would have overclaimed. |
| S10 | 296 | "This is why \"impact\" alone is the wrong villain." → "This is why impact alone is the wrong quantity to blame." | Register break in an otherwise flat technical voice. (The report quoted this as `&quot;impact&quot;`; the file has plain quotes.) |
| S11 | 300 | "each is a starting point meant to be edited" → "each is a starting point to be edited". | Shorter, same content. |
| S12 | 383 | Lab 3's output line given the same shape as the other three: "Output: average landing forces of $11.0,\ 4.3,\ 2.7$ and $2.1$ body weights for stops of $5,\ 15,\ 30$ and $45\ \mathrm{cm}$ - a factor $5.2$ across a factor $9$ in give." | Lab 3 re-run after the `ds` rename prints exactly those four numbers; `11.0/2.1 = 5.24`, `45/5 = 9`. |
| S13 | 403 | "Each has a figure, a short *Probes* note, and a collapsible solution." → "… and a collapsible solution, and every computational solution reports a number you can check against your own run." | True only after B8; it now is. |
| S15 | 538 | "It is worth naming the debts, because each is repaid" → "Each debt is named below, and each is repaid". | Announcing clause. |
| S16 | 546 | "What survives all of this is the essential physics" → "What survives is the physics the idealisations were chosen to keep". | "Essential" was doing no work. |
| S18 | 591 | Parameter-table preamble gains "Values marked (assumed) are modelling choices, not measurements." | After B3b and B12 the table carries six such rows; the distinction is now stated once rather than inferred from parentheses. |

| A1 | 217 | Fig. 7's CMJ force-time curve redrawn. The drawn curve integrated to `181.0 N s` and `34.06 cm` - the superseded number B2 had removed from every label around it. Replaced by Lab 2's own `profile(0.8)` on the same 80-point grid and the same axis calibration (`y = 260 - (220/3) F`), which integrates to `175.5 N s` and `32.04 cm`. The SJ curve was left alone: it already reproduced `profile(1.0)` to `0.018` BW and `30.06 cm`. | `m09/figfix.py` computes and prints the redraw (`J = 175.5 N.s, h = 32.04 cm, peak = 2.50 BW`); those are the `175.5 N s` and `32.0 cm` of `:219` and `:217`. The old curve was decoded from its own point string and integrated the same way. |
| A2 | 518 | K6's figure rebuilt. The old polyline was byte-identical to K3's descending line at `:506`, so it drew the required stopping distance falling with drop height, against K6's own `d_s = h_drop/5`. New: the computed line `(48,150)` to `(262,65.2)`, tick labels `0 / 0.5 / 1.0 m` and `0 / 10 / 20 cm`, the five solution points `4, 8, 12, 16, 20 cm` marked, annotation `d_s = one fifth of the drop at a tolerance F-bar <= 6mg`, and the aria-label's "peak force" corrected to the average-force relation. | `m09/figfix.py` prints `d_s(1.0 m) = 20.0 cm`, the same `20 cm` K6's solution tabulates; the five marks are that same `h/5` evaluated at `0.2` to `1.0 m`. `check_overlap` 0, `check_frame` 0 clipped and no new wasted-margin advisory (18, the baseline count), `check_svg` 0/0. |
| A3 | 534 | K10's figure rebuilt. The old red curve fell with speed; the exercise's model has `C_run = 3.9 + 0.05 v` rising. New: both curves computed from `C_walk = 2 + 1.6 Fr^2/(1 - 0.85 Fr)` and `C_run`, over `v = 0.8` to `3.3 m/s`, with speed ticks, the crossover marked at the computed point, and the `Fr = 1` ceiling drawn dashed at `v = 3.13 m/s`. | `m09/figfix.py` prints `crossover v = 2.622 m/s, Fr = 0.701; ceiling v = 3.132 m/s`, matching the `2.6 m/s`, `Fr = 0.71` and `sqrt(g L0) = 3.132` that `m09/genK.py` produced for B6's solution text. Curves decimated to 60 points to keep `check_svg` at 0 advisories. |
| A4 | 413 | Fig. 13's stance leg gains a knee: the single hip-to-ground line is split into thigh `(80,120)-(91,145)` and shank `(91,145)-(96,168)` with a joint sphere at the knee, matching the swing leg's two-segment build. (First of the two `HANDOFF.md` anatomy leftovers.) | Rendered with `shoot.py` and read: the stance leg now flexes like the swing leg. `check_bodyprop` unchanged at its single baseline advisory; `check_frame` 0 clipped. |
| A5a-A5e | 48 | Fig. 1's swing foot sat directly on top of the stance foot (swing ankle `(178.8,208.9)`, stance ankle `(180,220)`, ground line `y = 220`). The swing leg is re-posed with the hip fixed and both segment lengths preserved exactly (`61.9 px` each, checked on output): ankle moved to `(178,180)`, `40 px` of ground clearance, knee solved from the two-link constraint at `(229.5,145.7)`, foot rotated `8` degrees forward, and the knee and ankle spheres moved to match. (Second `HANDOFF.md` leftover.) | `m09/figfix.py` prints `knee (229.5, 145.7); thigh 61.9 px, shank 61.9 px, clearance 40`. Rendered and read: two feet, clearly separated, the pose reads as a runner's swing leg. `check_bodyprop` still one advisory (the same Fig. 1 thin-limb one as the pristine file), `check_frame` 0 clipped. |
| A7 | 48 | Fig. 1's flight body had one foot `5.6 px` thick where every other foot in the figure is `10.0`; thickened to `10.0` about the same centre line (`y` `198.4` to `196.2`, `rx` `2.8` to `5.0`). This was the single `check_bodyprop` advisory the pristine file carried - not an arm and not a Winter-proportion question, just one mis-sized rect. | `check_bodyprop` on the edited file: "every body figure's limbs are template-thick", **0** advisories, against 1 on the pristine file. Rendered and read. |
| A6a, A6b | 498 | K1's rebuilt figure had no y-axis scale, so the `163 ms` at the 3-BW limit could not be read off the plot. Three y ticks added (`0`, `170`, `340 ms`), the rotated axis title shifted from `x = 32` to `x = 26` to clear them, and the viewBox widened left from `20 30 280 152` to `14 30 286 152` so nothing is clipped. | Rendered and read. `check_frame` exit 0 with no clipping and no new advisory; `check_overlap` 0. |

Style edits 3, 5 and 8 of section 3 are folded into B10, B2a and B4k respectively;
edits 14 and 17 were "keep as it stands" and needed no change. That is all 16
blocking defects (B14 to B16 are the A1 to A3 rows) and all 18 style edits, plus
the two anatomy repairs of `HANDOFF.md` (A4, A5), one readability fix to the
figure B1b built (A6), and the mis-sized foot behind Fig. 1's `check_bodyprop`
advisory (A7).

### Corrections to the report

The report's *numbers* all held. Ten of its *replacements* were wrong or
incomplete, and the applied text differs from it in these ways:

1. **B2 missed two sites.** Besides `:217`'s caption and `:219`'s prose, Fig. 7
   carries `34 cm` in its own SVG label (`CMJ → 34 cm`) and in its aria-label
   ("34 versus 30 centimetres"). Both fixed (B2c, B2d). Without them the figure
   would still have contradicted its caption.
2. **B9's rename list omitted D10** (`:491` figure, `:492` solution), which is the
   problem that *derives* Prop 8.1. Renamed (B9f–B9i). A partial rename leaves
   the collision in place.
3. **B2's and B3's replacement paragraphs silently dropped "(Fig. 7, right)" and
   "(Fig. 11, left)".** Both cross-references kept.
4. **B4's Fig. 10 caption replacement was written in bare entities**
   (`F&#772;=&#189;m vland&#178;/d&#8347;+mg`) where the file uses `<em>`/`<sub>`
   markup. The applied version keeps the file's markup.
5. **B4's C8 replacement ended with a verbatim paste of `:265`** — the very
   duplication style edit 8 flags. Varied to "Same drop, same momentum; only the
   absorbing distance differs."
6. **B9's Prop 9.1 proof replacement kept the loading-rate algebra as one long
   inline `$…$`** — the construct that was firing `verify_dom`'s swallowed-prose
   advisory in the first place. Rewritten as a display equation; the advisory
   went 1 → 0.
7. **B3's rise-time expression was `\sqrt{8/2\times10^{5}}`**, which reads as
   `√(8/2)×10⁵`. Corrected to `\sqrt{8/(2\times10^{5})}`.
8. **Style edit 9's proposed wording overclaimed.** "higher than the average by a
   factor that (9.1) will make explicit" — (9.1) gives the spike, not the ratio.
   Reworded (S9).
9. **Style edit 10 quoted `&quot;impact&quot;`**; the file has plain `"impact"`.
10. **The report's B1 figure kept `viewBox="0 0 300 190"`** after deleting the
    runner glyph, which left a 23% top margin. Tightened to `20 30 280 152` so
    `check_frame`'s wasted-margin count stays at its baseline 18.

One further correction is to the report's own gate baseline: it did not record
`check_frame`'s figure count. The pristine `module09.html` has **18** wasted-margin
advisories (exit 0, no clipping), not the 2 an early truncated run suggested.

### Reviewer findings (`module09-reviewer-findings.md`)

All eight fixes from the prior Fable 5 rigor review of §0–§5 are present in the
file and all eight hold: the `double support` gloss (`:50`), the
impulse-vs-force correction in the thesis sentence (`:56`, "force acting over a
distance or a time"), the `swing phase` definition (`:64`), the Fig. 2
events-vs-phases repair (`:76`), the `v` de-collision in Prop 2.2 (`:111`), the
`v(t)`-vs-`v_y` de-collision in the Prop 5.2 proof (`:189`), the
non-circular horizontal-impulse argument (`:191`), and the Fig. 6
parameterization caption (`:193`). Nothing from that review is open. Its one
carry-forward — that its `K-DEPTH` dimension had never been exercised, because
§0–§5 carry no problem set — is now answered from the other side: this pass
found all ten K problems pass the depth standard and none is plug-in
substitution, but nine of the ten shipped **without a checkable number**, and B1
is what that permitted. Depth was never the gap; verifiability was.

### Gate results (edited/module09.html)

| gate | baseline (pristine) | after |
|---|---|---|
| `checktex` | 573 segments, **0** issues | 715 segments, **0** issues |
| `checklt` | **0** | **0** |
| `check_links` | 170 links, **0** broken, **0** unlinked §refs | 184 links, **0** broken, **0** unlinked |
| `check_svg` | **0** hard, **0** advisory | **0** hard, **0** advisory |
| `check_code` | 4 blocks, **0** issues | 4 blocks, **0** issues |
| `verify_dom` | 0 mjx-merror, 0 broken, 6 stray `$` (adv.), **1 swallowed-prose (adv.)** | 0 mjx-merror, 0 broken, 6 stray `$` (adv.), **0 swallowed-prose** |
| `check_overlap` | **0** label/curve overlaps | **0** |
| `check_frame` | exit 0; 0 clipped; 18 wasted-margin advisories | exit 0; 0 clipped; 18 advisories |
| `check_bodyprop` | exit 0; 1 thin-limb advisory (Fig. 1) | exit 0; **0** advisories |

Also re-run, though outside the nine: `check_probfig` 30/30 both before and
after; `check_proofs` 0 asserted propositions both; `check_prose` 1 advisory both
(`L221` "The mirror of this section is section 8" — a false positive on the
X-is-X rule, left alone).

All four lab blocks were re-extracted from the *edited* file and re-run: all four
still execute clean and print the same numbers as before the pass.

Every one of the nine was re-run a second time, on the file as it now stands
after the A edits, and the "after" column above is that run. The two figures A2
and A3 rebuilt were first drawn with a taller empty band, which pushed
`check_frame`'s advisory count from 18 to 20; their annotations were moved into
that band and the count is back at the baseline 18. The K10 curves were
decimated from 200 points to 60 for the same reason on `check_svg`, whose
heavy-polyline advisory had gone from 0 to 1.

### Not done, and why

- **The five structural notes of section 4 were not applied.** They are notes,
  not blocking defects or style edits, and two of them (a `<figcaption>` on each
  of the nine remaining K figures; relabelling K5's energy-bar figure to height)
  are new figure work rather than an edit. B1's replacement does add its own
  figcaption, so K1 now carries one. Section 7's unquantified stretch reflex
  (`:250`) is likewise left as the report describes it.
- **The two cosmetic anatomy leftovers named in `HANDOFF.md` are now fixed**
  (A4, A5), which supersedes this entry's earlier "not done". Both needed the
  limb geometry recomputed rather than a one-line edit, so the coordinates come
  from `m09/figfix.py`: Fig. 13's stance leg is split at a knee, and Fig. 1's
  swing leg is re-posed from the two-link constraint with both segment lengths
  preserved to `0.1 px`. `check_bodyprop` still reports its single baseline
  advisory (Fig. 1, a thin limb against a head-sized circle) and no gate moved.
- Nothing else is outstanding. Fig. 1's one long-standing `check_bodyprop`
  advisory was traced to a single mis-sized foot and fixed too (A7), so that gate
  now passes clean where the pristine file had one advisory.
