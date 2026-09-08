# Editor report: module07.html (Balance, Posture, and Load Bearing)

Pass run against `edited/module07.html` (988 lines, pristine copy of `module07.html`).
Every number quoted below was printed by a script in this pass, not recalled.
Verification assets (session-transient): `m07/sd.py` (semi-discretisation stability
test), `m07/cheb.py` (Chebyshev generator discretisation — the rightmost
characteristic root of the standing DDE, spectrally accurate), `m07/k5t.py` (the
triple-root solve), `m07/k28.py`, `m07/k8b.py`, `m07/k79.py`, `m07/k7.py`,
`m07/v1.py`, `m07/genfig.py`.

## 1. Verdict

**Yes, after revision — and the revision is larger than it looks.** The
mathematical spine of this module is the best in the course so far. Ten
propositions, every one proved, and the proofs are real: Prop 1.1 derives the
gravity-line condition from a moment balance and then reads the failure mode off
the same equation; Prop 2.2 gets the force-plate COP formula from one cross
product; Prop 4.2 turns capturability into a first-order pursuit; Prop 6.2 does
D-subdivision honestly and Prop 6.3 eliminates the delay by squaring and adding.
A graduate reader new to biomechanics can follow every line with a pen. Both labs
run, and both print the numbers the prose quotes.

The damage is in three places, and two of them are invisible to every hardening
gate. First, **ten problem figures render with their axes drawn as 20–60 px black
slabs** that cover the tick labels and part of the data (B1); one of them (C5)
is destroyed outright. All nine gates pass on this file. Second, **every numbered
figure reference in the module points at the wrong figure** (B2), because an
uncited lumbar-spine figure was inserted at the top of §0 and shifted the CSS
counter by one. Third, **five of the ten computational solutions quote numbers
that no run of the model reproduces** — K5's optimum is off by a factor of 2.3 in
the decay rate it reports, K4's body model contradicts the module's own $\ell$,
K2's area ratio is 4.45 not 4.6, K1's crossing frequency is 2.93 not 3.0, and
K7's numbers come from a run that is never specified. K8 is not a computational
problem at all: it is a one-line proportionality.

None of this touches the derivations. Fix the figures, fix the eight numbers, and
this is a chapter that teaches.

## 2. Blocking defects

### B1. Ten problem figures draw their axes as black slabs that hide the plot

`module07.html:778, :782, :786, :812, :824, :832, :851, :863, :875, :879, :883`

```
<line x1="55" y1="155" x2="260" y2="155" stroke="#333" stroke-width="49.2"/>
<line x1="55" y1="155" x2="55"  y2="50"  stroke="#333" stroke-width="25.2"/>
```

Twenty-two axis lines carry `stroke-width` between 21.6 and 62.4. Rendered
(`shoot.py` on the extracted figures, `m07/prev.png`), each plot has a solid black
rectangle across its lower left that swallows the x-axis title, the tick labels
and the first third of the curve. `C5` (`:782`) is worse still: its dashed
reference line is `stroke-width="57.6" stroke-dasharray="5 4"`, which renders as a
picket fence of red bars over the whole panel. `D2` (`:812`) draws its two
eigenlines at `stroke-width="50.0"`, so the saddle's stable and unstable manifolds
are two crossed slabs.

Fails part 5 of the standard (a tie to something concrete: the figure is the tie,
and it is unreadable) and the house figure rule. It passes `checktex`, `checklt`,
`check_links`, `check_svg`, `check_code`, `verify_dom`, `check_overlap`,
`check_frame` and `check_bodyprop` — `getBBox()` ignores stroke width, and
`check_overlap` excludes solid lines by design.

**Fix.** Three mechanical rules over the whole file:

- every `<line>` with `stroke="#333"` and `stroke-width` &ge; 10 &rarr;
  `stroke-width="1.2"` (22 lines);
- the dashed reference line at `:782` &rarr; `stroke-width="1.6"`;
- the two eigenlines at `:812` &rarr; `stroke-width="2.6"`.

The same generator bug put a "thickness" into the shaft of every vector arrow:
31 `<line ... marker-end="url(#a_*)">` elements carry `stroke-width` between 12
and 56.6, against the house rule of 2.5–3 with a fixed 10–13 px head. A 20 px
shaft with a `markerUnits="userSpaceOnUse"` head is a brick with a notch, not an
arrow (`m07/prev2.png`, Fig. 7's `Mg`). Fixed to `stroke-width="3"` for the pure
vector colours `#b0361f`, `#2a6ca8`, `#c9761a`, `#6a2fa0`, `#555`; the muscle
colour `#8a3d3d` and the limb colours `#c98a5e`/`#5a86a8` are left alone, because
there a thick stroke is the anatomy, not a shaft.

### B2. Every numbered figure reference points at the wrong figure

`module07.html:106` (the intruding figure) and `:123, :149, :179, :326, :383,
:428, :435, :503` (twice), `:669`, `:754`, `:884` (the references).

`:106` is a lumbar-spine figure with the caption

> Low-back load paths pass through vertebral bodies and discs. Disc height is
> small relative to the bodies — a short lever stack that still carries large
> moments when the trunk leans (stoop lift).

It sits in §0, whose subject is the inverted pendulum, and no sentence in §0
refers to it. Figure numbers come from a CSS counter (`figcaption::before{
content:"Fig. " counter(fig) ". " }`, `:37`), so this figure is Fig. 1 and every
later figure is one higher than the prose says. `:123` — "The distinction drawn in
**Fig. 1**" — sends the reader to the lumbar spine instead of the two pendulums;
`:326` and `:503` send "the stabilogram of **Fig. 5**" to the pressure
distribution; "the diverging saddle of **Fig. 8**" (`:428`) lands on the COP
lever. The intended numbering is recorded in the file itself: the two-pendulums
figure carries the marker `<!--FIG:fig1-->`.

Fails part 5 (the concrete tie is mis-addressed eleven times).

**Fix.** Move the whole of `:106` out of §0 and into §8, immediately before the
"mechanical disadvantage" figure, where it illustrates the lever it describes;
cite it from the §8 prose; and bump the one reference that then falls after it
(`:884`, `Fig. 20` &rarr; `Fig. 21`). New §8 paragraph and figure placement:

```html
<p>The junction between the last lumbar vertebra and the sacrum, <b>L5/S1</b>, is
the pivot about which the trunk bends forward. When you lean, the weight of the
upper body — and any load in the hands — hangs forward of this pivot on a long
moment arm, while the muscles that resist the bend, the erector spinae running
vertically just behind the spine, pull on a very short one. That mismatch is the
whole story. The anatomy sets the short arm (<b>Fig. 17</b>): the lumbar
vertebral bodies are stacked with thin intervertebral discs between them, so the
whole extensor apparatus acts within a few centimetres of the joint line.</p>
```

### B3. K5 reports gains that are not the optimum, and a decay rate 2.3 times too small

`module07.html:868`

> the optimum sits near $K_p\approx940$, $K_d\approx260\ \mathrm{N\,m\,s\,rad^{-1}}$,
> with a decay rate of ${\approx}\,1.5\ \mathrm{s^{-1}}$ (recovery time constant
> ${\approx}\,0.7$ s).

The rate quoted for those gains is right — the rightmost characteristic root at
$(940,260,\Delta=0.15)$ is $-1.458\ \mathrm{s^{-1}}$ — but the pair is not the
maximiser. The fastest stable recovery over a two-parameter gain plane is a
**triple real root** of the quasi-polynomial
$f(s)=Is^2-Mg\ell+(K_p+K_ds)e^{-s\Delta}$: solving $f=f'=f''=0$ gives

```
sigma = 3.4211 s^-1   Kp = 784.88 N m/rad   Kd = 256.45 N m s/rad
residuals: [-1.6e-09, -1.5e-10, 2.9e-11]
```

confirmed independently by a Chebyshev generator discretisation (`m07/cheb.py`,
N = 20/30/40/60 agree to five decimals: rightmost root $-3.4204$), and by a grid
search over $K_p$ with the damping optimised at each point (max 3.4206 at
$K_p=785$). The claim "the best gains lie well inside the island" survives; the
numbers do not. Fails the derived-number rule.

**Replacement for `:868`:**

```html
<details class="sol"><summary>Solution</summary><div>Sweeping the island and reading the rightmost characteristic root at each gain pair, the decay rate peaks at $K_p\approx785\ \mathrm{N\,m\,rad^{-1}}$ (that is $1.27\,Mg\ell$) and $K_d\approx256\ \mathrm{N\,m\,s\,rad^{-1}}$, giving $\sigma_{\max}\approx3.42\ \mathrm{s^{-1}}$ and a recovery time constant $1/\sigma\approx0.29$&nbsp;s — about twice the delay. The optimum is exactly where three real characteristic roots coalesce, the delayed analogue of critical damping: it solves $f(s)=f'(s)=f''(s)=0$ for $f(s)=Is^2-Mg\ell+(K_p+K_ds)e^{-s\Delta}$. It sits well inside the island, not at its edge; the softer pair $K_p=940,\ K_d=260$ recovers at only $1.46\ \mathrm{s^{-1}}$, and pushing $K_p$ past $785$ trades decay rate for proximity to the oscillatory boundary.</div></details></div>
```

### B4. K8 is substitution, not computation

`module07.html:878, :880`

> K8. To stiffen from $K_p=Mg\ell$ to $K_p=1.5\,Mg\ell$ by co-contraction,
> estimate the relative metabolic cost, taking cost proportional to total muscle
> activation.
>
> ...cost scales with total activation $\propto k_a+k_b=K_p$. Raising $K_p$ by
> $50\%$ therefore raises the co-contraction cost by ${\approx}\,50\%$.

The problem is "if cost is proportional to $K_p$, what is the cost of raising
$K_p$ by 50 %". It requires no integration, no optimisation, no inverse solve, no
sweep and no regime comparison, and it is the defect the course conventions name
explicitly. Its figure (`:879`) plots a straight line through the origin, which is
the restatement of the assumption.

**Replacement.** The interesting question is not what stiffness costs but what
speed costs, and the answer inverts the intuition the old problem trained: at the
true delay, recovery speed is almost free in activation, and what caps it is the
delay. Computed with `m07/k8b.py` (damping optimised at each $K_p$, rightmost
root from `cheb.py`):

```
sigma=0.50: cheapest Kp=  632.5 (1.023 Mgl)  Kd= 148.8
sigma=1.00: cheapest Kp=  660.0 (1.068 Mgl)  Kd= 184.9
sigma=2.00: cheapest Kp=  732.5 (1.185 Mgl)  Kd= 235.1
sigma=3.00: cheapest Kp=  780.0 (1.262 Mgl)  Kd= 254.9
sigma=3.40: cheapest Kp=  785.0 (1.270 Mgl)  Kd= 256.5   (sigma_max = 3.4206)
```

New statement and solution (the figure is regenerated to match, see §6):

```html
<li><b>K8.</b> Co-contraction is how the nervous system buys the proportional gain $K_p$, and Proposition 7.3 makes the metabolic cost proportional to $k_a+k_b=K_p$. At the true neural delay $\Delta=0.15$&nbsp;s, compute the <em>price of speed</em>: for each required recovery rate $\sigma$ (the decay rate of the slowest closed-loop mode), find the cheapest $K_p$ that achieves it, with $K_d$ free to be optimised. What does doubling the recovery speed cost, and what stops the body buying more? <span class="probes"><b>Probes:</b> constrained optimisation over the stable island; which resource actually binds.</span></li>
```

```html
<details class="sol"><summary>Solution</summary><div>For each $K_p$, optimise $K_d$ and read the rightmost characteristic root; then invert to get the cheapest $K_p$ meeting each $\sigma$. A recovery rate of $1\ \mathrm{s^{-1}}$ costs $K_p=660\ \mathrm{N\,m\,rad^{-1}}=1.07\,Mg\ell$ (with $K_d=185$); doubling it to $2\ \mathrm{s^{-1}}$ costs $K_p=732=1.19\,Mg\ell$ (with $K_d=235$). Doubling the speed therefore raises total activation by only ${\approx}\,11\%$ — although the <em>active</em> part, $K_p-Mg\ell$, goes from $42$ to $114\ \mathrm{N\,m\,rad^{-1}}$, a factor of $2.7$. The curve then turns vertical: no gain whatever achieves $\sigma\gt3.42\ \mathrm{s^{-1}}$, the triple-root optimum of K5. So the binding resource is not metabolism but the delay, and stiffening past $1.27\,Mg\ell$ buys nothing and eventually costs stability (<a class="secref" href="#delay">§6</a>). That is why we destiffen as soon as a surface feels secure: the extra activation was never buying speed.</div></details></div>
```

### B5. K7's numbers come from no stated run

`module07.html:876`

> Building the COM as band-limited sway and the COP via $x_{\text{cop}}=x_{\text{com}}-\ddot x_{\text{com}}/\omega_0^2$ (Prop 3.3), a representative run gives COP RMS ${\approx}\,6.6$ mm against COM RMS ${\approx}\,4.5$ mm.

"Band-limited sway" fixes neither the bandwidth nor the amplitude, so nothing here
is reproducible, and the problem asks the reader to *simulate* a sway signal
without saying what generates it. Fails part 1 (a precise statement) and the
derived-number rule.

**Fix.** Specify the simulation and quote what it prints (`m07/k7.py`): closed
loop at $K_p=900$, $K_d=120$, $\Delta=0.12$ s (inside the island, rightmost root
$-0.078\ \mathrm{s^{-1}}$), white ankle-torque disturbance of strength
$0.35\ \mathrm{N\,m\,s^{1/2}}$, $dt=1$ ms, $T=600$ s, first 30 s discarded:

```
seed  7: COM RMS 4.47 mm  COP RMS 6.79 mm  ratio 1.5181
seed  8: COM RMS 4.57 mm  COP RMS 6.95 mm  ratio 1.5190
seed  9: COM RMS 4.73 mm  COP RMS 7.18 mm  ratio 1.5189
seed 10: COM RMS 4.11 mm  COP RMS 6.25 mm  ratio 1.5184
seed 11: COM RMS 4.36 mm  COP RMS 6.62 mm  ratio 1.5180
```

The ratio is seed-independent because it is a property of the transfer function,
and that gives a free analytic check: the COM's spectral peak is at 0.35 Hz, and
$1+(2\pi f)^2/\omega_0^2 = 1.52$ there.

**Replacement for `:876`:**

```html
<details class="sol"><summary>Solution</summary><div>Drive the closed loop of Proposition 6.1 with a white ankle-torque disturbance and read both signals off the same run: $x_{\text{com}}=\ell\theta$ and $x_{\text{cop}}=\tau/(Mg)$ (Prop 3.2). With $K_p=900$, $K_d=120$ and $\Delta=0.12$&nbsp;s — inside the island, rightmost root $-0.078\ \mathrm{s^{-1}}$ — a torque noise of $0.35\ \mathrm{N\,m\,s^{1/2}}$ integrated at $dt=1$&nbsp;ms for $600$&nbsp;s (first $30$&nbsp;s discarded) gives COM RMS $4.5$&nbsp;mm against COP RMS $6.8$&nbsp;mm: the COP swings $1.52\times$ wider. The ratio is the same to four figures across five random seeds, because it is not a property of the noise but of Proposition 3.3: the COP is the COM plus its acceleration over $\omega_0^2$, so a sway component at frequency $f$ is amplified by $1+(2\pi f)^2/\omega_0^2$. The simulated COM peaks at $0.35$&nbsp;Hz, where that factor is $1.52$.</div></details></div>
```

### B6. K4 models the body with a length the module has already fixed at another value

`module07.html:862, :864`

> Model the body as a point mass with $\ell=0.55\,h$ ... $\omega_0$ falls from
> $3.34\ \mathrm{s^{-1}}$ at $1.6$ m to $3.06\ \mathrm{s^{-1}}$ at $1.9$ m.

§1 says the COM lies "about $55\%$ of stature above **the floor**"; $\ell$ is
defined in §3 as the ankle-to-COM distance. They differ by the ankle height. For
the module's own reference human, $0.55\times1.75=0.9625$ m, against the
$\ell=0.9$ m used everywhere from §4 to K6 — a 7 % contradiction inside one
module, and the coincidence that $\sqrt{g/(0.55\times1.9)}=3.064$ almost equals
the reference human's $\omega_0=3.060$ hides it. Fails the running-example rule
(a scenario reused later must use the same parameter values or say why not).

**Fix.** Introduce the ankle height $h_a=0.06$ m as an Appendix parameter and
derive $\ell$ from it, which also turns §4's asserted $\ell=0.9$ m into a derived
number: $0.55\times1.75-0.06=0.9025$ m. Recomputed (`m07/v1.py`):

```
K4 h=1.6: ell=0.8200 w0=3.4588
K4 h=1.9: ell=0.9850 w0=3.1559     ratio 1.0960  (+9.6 %)
```

**Replacement for `:864`:**

```html
<details class="sol"><summary>Solution</summary><div>Take the COM at $0.55h$ above the floor and the ankle axis at $h_a=0.06$&nbsp;m, so the pendulum length is $\ell=0.55h-h_a$ (which returns the module's $\ell=0.90$&nbsp;m at $h=1.75$&nbsp;m). With $\omega_0=\sqrt{g/\ell}$, the toppling rate falls from $3.46\ \mathrm{s^{-1}}$ at $1.6$&nbsp;m to $3.16\ \mathrm{s^{-1}}$ at $1.9$&nbsp;m, about $9.6\%$ slower. The toppling clock and the tolerable delay both scale as $1/\omega_0$, so the taller person tolerates ${\approx}\,10\%$ more delay: a bigger inverted pendulum falls more slowly. The ankle offset matters here — with $\ell$ taken as $0.55h$ the scaling would be exactly $\sqrt{h}$ and the gain $9.0\%$; subtracting a fixed $h_a$ makes the short person relatively shorter and the effect slightly larger. (This is why toddlers, short and fast-toppling, wobble more than adults.)</div></details></div>
```

The K4 figure (`:863`) labels the two endpoints `1.6 m: 3.34 s⁻¹` and
`1.9 m: 3.06 s⁻¹`; its curve and both labels are regenerated from the new formula
(`m07/genfig.py`).

### B7. K6 calls the forward stability margin `d_toe`, and the Appendix row does not reproduce K6's own answer

`module07.html:872` and `:957`

> Recovery needs $\xi\le d_{\text{toe}}\approx0.10$ m, i.e. $J\le M\omega_0 d_{\text{toe}}$.

`d_toe` is $0.12$ m in §7 (`:521`), in C3 (`:775`), in the D8 figure label
(`70 kg × 9.81 × 0.12 m`) and in the Appendix (`:955`). With $0.12$ m the same
formula gives $J=25.7$ N·s, not the $21$ N·s K6 states. The quantity K6 actually
needs is the **forward margin** — the distance from the quiet-standing COM
projection to the toe edge — which §1 already calls $0.10$ m. The Appendix row
`Max recoverable impulse | $M\omega_0 d_{\text{toe}}$ | ≈21 N·s` is therefore
self-contradicting: its own formula and its own $d_{\text{toe}}$ give 25.7.

**Fix.** Name the margin $m_{\text{toe}}$, use it in K6 and in the Appendix row,
and add the sensitivity the house rules require.

**Replacement for `:872`:**

```html
<details class="sol"><summary>Solution</summary><div>An impulse $J$ gives $\dot x_{\text{com}}=J/M$ with the COM still at its quiet-standing position, so the extrapolated centre of mass jumps by $\xi-x_{\text{com}}=\dot x_{\text{com}}/\omega_0=J/(M\omega_0)$. Recovery without a step needs that jump to stay inside the forward margin $m_{\text{toe}}\approx0.10$&nbsp;m (<a class="secref" href="#support">§1</a>: the toe edge is $d_{\text{toe}}=0.12$&nbsp;m ahead of the ankle and the COM already sits about $0.02$&nbsp;m ahead of it), i.e. $J\le M\omega_0 m_{\text{toe}}$. With $M=70$&nbsp;kg and $\omega_0=3.06\ \mathrm{s^{-1}}$ the COM velocity limit is $0.31\ \mathrm{m\,s^{-1}}$ and the largest recoverable impulse is $21.4$&nbsp;N·s. The bound is linear in the margin: every centimetre of margin is worth $M\omega_0=2.14$&nbsp;N·s, so standing with the feet already spread forward buys recoverable impulse in direct proportion. Beyond it a step is unavoidable.</div></details></div>
```

### B8. §1's stability margins contradict the foot they are computed from

`module07.html:175`

> For a $1.75$ m adult with feet $\sim0.25$ m long, quiet standing parks the COM
> near mid-foot, leaving roughly $0.10$ m of margin toward the toes and
> $\sim0.05$ m toward the heels.

$0.10+0.05=0.15\ne0.25$, and "near mid-foot" would give equal margins, which
contradicts the asymmetry the next sentence draws from them. Neither number is
derived, and neither is a table parameter. Fails the number rule and part 1.

**Replacement for `:175`:**

```html
<div class="keyresult"><b>Stability margin.</b> The <b>margin</b> is the shortest distance from the gravity-line point to the edge of the base, $\;m_{\text{stab}}=\operatorname{dist}(x_{\text{com}},\partial\,\text{BoS})$. Measure it from the ankle, which is where the foot's extent is tabulated: the usable base reaches $d_{\text{toe}}=0.12$&nbsp;m forward of the ankle axis and $d_{\text{heel}}=0.05$&nbsp;m behind it (Appendix), and quiet standing parks the COM projection about $0.02$&nbsp;m ahead of the ankle (an assumption; it is what puts the resting centre of pressure under the mid-foot). The margins are therefore $m_{\text{toe}}=0.12-0.02=0.10$&nbsp;m forward and $m_{\text{heel}}=0.05+0.02=0.07$&nbsp;m backward. The asymmetry — more room in front — is why a shove is met by rising onto the balls of the feet rather than rocking onto the heels, and $m_{\text{toe}}$ is the number that sets the largest recoverable shove (K6).</div>
```

### B9. K2's area ratio is 4.45, and the figure repeats the wrong 4.6

`module07.html:856` and the `fig44` label `stable area ratio ≈4.6`

Two independent computations disagree with the module. Green's theorem on the
Hopf boundary of Proposition 6.2, closed by the segment $K_p=Mg\ell$:

```
D=0.12: analytic area = 1189023      D=0.18: analytic area = 267447
analytic ratio: 4.4458
```

and a $160\times160$ grid tested with the Chebyshev rightmost root:

```
K2 cheb-grid areas: 1190105  267281  ratio 4.453
```

**Replacement for `:856`:**

```html
<details class="sol"><summary>Solution</summary><div>Testing stability on a grid over $(K_p,K_d)$ and summing the stable cells gives $1.19\times10^6$ for $\Delta=0.12$&nbsp;s against $2.67\times10^5$ for $\Delta=0.18$&nbsp;s, a ratio of $4.45$. The boundary of Proposition 6.2 makes the same number exactly: the area enclosed between the Hopf curve and the divergence line $K_p=Mg\ell$, by Green's theorem, is $1.189\times10^6$ and $2.674\times10^5$, ratio $4.446$. A $50\%$ longer delay therefore costs $78\%$ of the usable gain space — the island shrinks far faster than the delay grows, which is why a small slowing of conduction (cooling, neuropathy, fatigue) has an outsized effect on balance.</div></details></div>
```

### B10. K1's crossing frequency

`module07.html:852`

> the crossing frequency is $\omega_c\approx3.0\ \mathrm{s^{-1}}$, i.e. $f_c\approx0.47$ Hz

The quartic of Proposition 6.3 at $K_p=1100$, $K_d=150$ gives (`m07/v1.py`)

```
Kp=1100.0 Kd=150.0: wc=2.9298 f=0.4663 Hz Dcrit=129.73 ms
```

$f_c$ is right; $\omega_c$ is not $3.0$. "Agree to the millisecond" is also worth
making concrete: 129.5 ms from the bisection against 129.7 ms from the quartic.

**Replacement for `:852`:**

```html
<details class="sol"><summary>Solution</summary><div>Bisection on the delay gives $\Delta_{\text{crit}}=129.5$&nbsp;ms against the quartic's $129.7$&nbsp;ms; the crossing frequency is $\omega_c=2.93\ \mathrm{s^{-1}}$, i.e. $f_c=0.47$&nbsp;Hz — higher than the $0.35$&nbsp;Hz of the softer gains, since stiffer control sways faster. Note that the critical delay is almost unchanged (129.7 against 129.7&nbsp;ms for $K_p=900,\ K_d=120$): raising both gains together moves the operating point almost along the boundary, buying speed of response rather than delay tolerance.</div></details></div>
```

### B11. Lab 2's headline claim is contradicted by its own printed output

`module07.html:706`

> Tripling the reach cuts the safe load by more than three.

The block above it prints `reach 0.15 m -> 42.5 kg` and `reach 0.45 m -> 14.5 kg`:
a factor of $2.9$, not more than three. Bisected rather than gridded
(`m07/k79.py`), $42.596$ against $14.777$, a factor of $2.88$. Only the step out
to $0.50$ m, which is $3.3$ times the reach, exceeds three.

**Replacement for `:706`:**

```html
Tripling the reach — $0.15$&nbsp;m to $0.45$&nbsp;m — cuts the safe load from $42.5$ to $14.5$&nbsp;kg, a factor of $2.9$; the cost is close to proportional because the trunk's own moment $m_tr_t$ sits in the sum alongside $m_Lr_L$ and does not shrink with reach. The erector's moment arm $d$ is fixed by anatomy, so the only lever you control is the reach — which is the entire content of "lift with your legs and keep the load close."</div>
```

### B12. The D1 figure states the equation of motion with the wrong sign

`module07.html:808`, the SVG label

```
Iθ̈ = Mgℓ sinθ + τ
```

Proposition 3.1 and the D1 solution directly beneath both give
$I\ddot\theta = Mg\ell\sin\theta - \tau$, and the sign of $\tau$ is the entire
point of the problem (the ankle torque restores; gravity topples). Fails part 1.
**Fix:** `Iθ̈ = Mgℓ sinθ &#8722; τ`.

### B13. Symbol collisions the Appendix does not flag

- `d` is the **ankle height above the ground** in the proof of Proposition 3.2
  (`:299`, `:301`) and the **erector-spinae moment arm** in §8 (`:591` onward, and
  the Appendix row at `:960`). Fix: rename the ankle height to $h_a$, which then
  does double duty as the parameter B6 needs.
- `h` is the **COM height** in the proof of Proposition 1.1 (`:160`) and
  **stature** in K4 (`:862`). Fix: use the Appendix's existing $h_{\text{com}}$ in
  the proof, and keep `h` for stature, adding it to the notation table.
- `F` is the horizontal ground force in the proof of Proposition 1.1 (`:160`,
  `:163`, `:164`) and `H` everywhere else (§2, §7, Appendix). Fix: use `H`.

### B14. Proposition 3.2 discards the shear term as "third-order" with no estimate

`module07.html:301`

> For quiet standing the shear $H$ is a few percent of body weight and the ankle
> height $d$ is small, so the $Hd$ term is third-order; dropping it,

$Hd$ is a product of two first-order-small quantities, not a third-order term, and
"small" is not a number. Fails part 4 (where the hypothesis binds).

**Replacement for `:301`:**

```html
For quiet standing the shear is bounded by $|H|\le0.02\,Mg$ (assumed, <a class="secref" href="#cop">§2</a>) and the ankle sits $h_a=0.06$&nbsp;m above the ground, so $|H|h_a\le0.0012\,Mg\cdot\mathrm m$, while the retained term $N(x_{\text{cop}}-x_{\text{ankle}})$ is about $0.02\,Mg\cdot\mathrm m$ at a typical quiet-standing pressure offset and grows to $0.12\,Mg\cdot\mathrm m$ at the toe. The shear term is therefore at most about $6\%$ of the torque it corrects, and in true statics it vanishes with $H$ (Proposition 1.1). Dropping it,
```

### B15. The toppling time constant is quoted as 0.32 s; it is 0.327 s

`module07.html:359`, `:813`, `:949`, and the `fig10` labels `0.32` and
`τc=1/ω₀≈0.32 s`.

$\omega_0=3.0600\ \mathrm{s^{-1}}$ and $1/\omega_0=0.3268$ s. The module rounds
$\omega_0$ up to $3.1$ and $\tau_c$ down to $0.32$, so the two printed numbers are
not reciprocals; the very next sentence calls it "every third of a second", which
is $0.33$. Fix: $0.33$ s in all five places.

### B16. Bare empirical numbers with no symbol, no table row, and no assumption label

Each of the following is none of the three admissible classes.

| `:line` | number | fix |
|---|---|---|
| `:424` | intrinsic ankle stiffness "measured at only ${\sim}\,90\%$ of this value" | give it the symbol $K_p^{\text{int}}$, state it as a reported measurement whose source is not in this repository, and put it in the table with that symbol |
| `:204` | "the shear is small — a few percent of body weight" | state as an assumption, $|H|\le0.02\,Mg$, and add the table row |
| `:356`, `:947` | $I\approx66\ \mathrm{kg\,m^2}$ | label it assumed and bracket it: a point mass at $0.9$ m gives $57\ \mathrm{kg\,m^2}$, a uniform $1.8$ m rod about its end gives $76$ |
| `:494` | the measured sway band $0.2$–$0.5$ Hz | name it as a reported range, not a derived one |
| `:600`, `:962` | the $3.4$ kN disc threshold, tabulated with an em-dash for a symbol | give it the symbol $F_{\text{lim}}$, which the lab code already calls `LIMIT` |
| `:143` | COM at $55\%$ of stature | add the fraction to the parameter table, since B6 now derives $\ell$ from it |
| — | ankle height $h_a$ | new row, $0.06$ m, used by B6, B13 and B14 |
| — | quiet-standing COM offset | new row, $0.02$ m, assumed, used by B7 and B8 |
| — | forward/backward margins | new rows, $m_{\text{toe}}=0.10$ m, $m_{\text{heel}}=0.07$ m, derived |

### B17. The module never places its models on the level ladder

`module01.html:135` does it in one sentence ("Every model here sits on Level 1 of
the course's level ladder... Modules 7 to 9 do [Level 2]"). Module 7 never says
which rung it is on, although it spans three: §1 and §8 are Level 1 statics, §3 to
§4 are Level 2 planar rigid-body dynamics, and §5 to §7 are Level 7 feedback
control. Fails a stated convention and leaves the reader unable to place §8's
quasi-static spine beside §6's delayed controller.

**Fix — added to the end of `:129` (the "arc of this module" paragraph):**

```html
<p><b>Where these models sit.</b> The module climbs three rungs of the course's level ladder. <a class="secref" href="#support">§1</a> and <a class="secref" href="#load">§8</a> are <b>Level 1</b>, static equilibrium of rigid segments: the gravity-line condition and the L5/S1 lever are moment balances with no inertia in them. <a class="secref" href="#dynamics">§3</a> and <a class="secref" href="#linear">§4</a> are <b>Level 2</b>, planar rigid-body dynamics: one segment, one degree of freedom, Euler's law and its linearisation. <a class="secref" href="#pd">§5</a> to <a class="secref" href="#hip">§7</a> are <b>Level 7</b>, feedback control: a control law, a stability condition, and a computed margin. Nothing here is Level 3 or above, and that is the module's main limitation — the body is one rigid stick, and every multi-segment effect is deferred to Module 8.</p>
```

### B18. §10 lists what the module owes but never says what the reader can now do

`module07.html:965` closes on a list of IOUs to Modules 8, 9, 12 and 14. A chapter
closes with the capability it has conferred.

**Replacement for `:965`:**

```html
<p>This closes Module 7. You can now take a person's mass, height and neural delay, write down the equation of motion of their standing body, decide whether a given feedback gain holds them up, compute the sway frequency it will produce and the delay at which it will fail, say how large a shove they can absorb without stepping, and put a number on what a lift costs their spine. The standing body — an unstable inverted pendulum held upright by a delayed feedback loop, sensing its lean through muscle spindles and steering its centre of pressure with the calf — carries every idealisation forward as an IOU: to walking (Module&nbsp;8), to running and jumping (Module&nbsp;9), to whole-limb control (Module&nbsp;12), and to the tissue mechanics of load and fatigue (Module&nbsp;14).</p>
```

### B19. The reader-facing lab code is formatter-damaged

`module07.html:658-663`

```python
print(
    f"critical delay : simulation {
        1e3 *
        Dcrit:5.1f} ms   theory {
            1e3 *
            Dtheory:5.1f} ms")
```

A multi-line expression inside an f-string is PEP 701, i.e. Python 3.12 and later:
a reader on 3.11 gets a `SyntaxError` from a block the module tells them to copy
and run. The same pass mangled `acc = (Mgl*th[k] - Kp*thd - Kd*wd) / \` onto a
backslash continuation and, in Lab 2, broke `max(m for m in np.arange(0, 60, 0.5)
if peak_compression(m, rL) < LIMIT)` across five lines. Both blocks are PEP8-clean
(`check_code` passes), which is exactly why nothing caught it.

**Fix.** Rewrite both to readable, 79-column, 3.8-compatible form; both must print
byte-identical output (verified in §6).

## 3. Style and clarity edits

| `:line` | original | rewrite |
|---|---|---|
| `:127` | "is a notoriously treacherous problem" | "destabilises easily: the correction arrives aimed at a lean the body no longer has" |
| `:433` | "Proposition 5.1 is almost suspiciously permissive." | "Proposition 5.1 is too permissive to be the whole truth." |
| `:196` | "That is all statics needs — but the controller of standing works precisely by moving that point." | delete "precisely" |
| `:204` | "a force plate is, in this sense, a very accurate scale" | "a force plate is, in this sense, an accurate scale" |
| `:242` | "It is tempting to picture the COP as..." | "The COP is not the COM's shadow, although in perfect statics the two coincide." |
| `:341` | "almost every initial lean diverges exponentially" | "every initial lean diverges exponentially except those on the line $\dot\theta=-\omega_0\theta$" |
| `:569` | "each of these is simply a shifted equilibrium" | delete "simply" |
| `:503` | "the delay is why it can never quite win" | "the delay is why it never quite wins" |
| `:816` (fig35) | `xcop = xcom - ẍ̈com/ω₀²` | `xcop = xcom &#8722; ẍcom/ω₀²` (the label carries two combining diaereses) |
| `:886` (K10) | elasticities quoted with no posture | state that they are evaluated at full flexion, $\varphi=90^\circ$, where the axial term vanishes |
| `:728` | "advanced control (noted in §6)" in the repayment table | "beyond this course (the requirement is made precise in §6)" — every sibling row names a module |

## 4. Structural notes

- **The vector arrows are bricks.** 31 arrow shafts carry `stroke-width` from 12
  to 56.6 against the house rule of 2.5–3 (B1). I have thinned the ones whose
  colour marks them unambiguously as vectors; the muscle-coloured arrows
  (`#8a3d3d`, at `:802`, `:844`, `:887`) are left, because there the thickness may
  be the muscle belly. They should be looked at.
- **None of the ten K solutions carries a code block**, although the course
  convention is that "K solutions carry Python-verified numbers with code" and
  Modules 4 and 6 do. The numbers are now verified, but the reader cannot rerun
  them. Adding ten blocks is a separate pass.
- **`check_svg` advisory: mixed disclosure labels.** Diagnostics use
  `<summary>Answer</summary>`, problems use `<summary>Solution</summary>`. Both
  read fine and the split is meaningful; left alone.
- **Four polylines exceed 120 points** (`check_svg` advisory). Left alone: they
  are computed sway traces where decimation would visibly change the signal.
- §2's caveat that the force plate's load cells sit at depth $z_0$ introduces
  $z_0$ and never tabulates it; it is used only inside its own sentence, so it is
  left, but it is the same class as B16.

## 5. What already works

- **§6 is the best section in the course to date.** Proposition 6.1 derives the
  quasi-polynomial and says why it has infinitely many roots; 6.2 does
  D-subdivision by separating real and imaginary parts, with the $\omega\to0$
  limit recovering the §5 boundary as a check; 6.3 eliminates the delay by
  squaring and adding. Every step is reproducible with a pen, and the lab then
  walks the simulation up to the boundary and matches it to 0.2 ms.
- **Proposition 3.2 and Proposition 3.3 together** turn an abstract control input
  into a measurable quantity and then into the exact COP–COM law. The pedagogical
  order — promise it in §2, pay it in §3, use it in §4 — is exactly right.
- **Proposition 4.2 (capturability)** is a model of how to derive a famous
  criterion: one substitution, one first-order system, and the reachability
  argument falls out of $\omega_0\gt0$.
- **§5's "measured surprise"** — that intrinsic ankle stiffness lands just inside
  the unstable region — is the module's best single fact, and it is put where it
  does the most work.
- **The captures/misses table** names seven idealisations and points each at the
  module that repays it. Six of the seven point at a real module.
- Anatomical glossing is complete: calcaneus, metatarsal heads, L5/S1, screw-home,
  plantarflexors, erector spinae and muscle spindle are all glossed in the
  sentence that first uses them.
