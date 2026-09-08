# Editor report: module15.html (Measurement, Estimation, and Inverse Dynamics)

Edited copy: `edited/module15.html`. The original `module15.html` was not
touched. Every number quoted below as a replacement was printed by a run
recorded in this report; no number was carried over from the manuscript or
from memory.

---

## 1. Verdict

**Yes, after revision — and the revision is not cosmetic.**

This module has the best architecture of any in the second half of the
course. It sets out to teach the one thing the previous fourteen modules
quietly assumed: that a joint torque is not measured, it is *inferred*,
through a chain of instruments and derivatives each of which degrades the
estimate. The spine is right — measurement chain, segment model, the
noise-amplification of differentiation, the bias-variance choice of cutoff,
the centre-of-mass cross-check, the Newton-Euler recursion, a synthetic
end-to-end test, error propagation, identification — and it ends where it
should, with an error bar rather than a curve. The thirty problems are
genuinely at level: every K problem demands a sweep, an optimisation, an
inverse solve, or a regime comparison, and not one is substitution into a
boxed formula.

What fails is the arithmetic layer, and it fails systematically. The module
states three times that every quoted number is reproduced by the code shown.
That claim is false in both directions. **Four of the five shipped code
blocks raise `NameError` on the first run** — they reference `q_meas`,
`q_true`, and `a_com_kin`, none of which is ever defined in the listing the
reader is handed — and the fifth runs but prints nothing at all. Meanwhile
the numbers the prose quotes beside those listings are not what the code
computes: §7's headline pair is quoted as 0.08 and 6.8 N m where a run gives
0.07 and 1.70; §4's velocity optimum is quoted as 7 Hz where the computation
gives 3.0; Lab C quotes a one-standard-deviation fraction (±17 %) in the
sentence that names the 95 % interval, understating the reported uncertainty
by a factor of two. A reader who does what this module tells them to do —
run the code, check the numbers — finds neither half of the promise kept.

Three defects are worse than wrong numbers, because they teach a wrong
mechanism. §10 explains that the torque optimum lies *below* the velocity
optimum because "each differentiation is noisier"; for this joint the
ordering is the other way round (3.4 Hz against 3.0 Hz), and the reason is
that seven eighths of the torque is the gravity term, a function of the
angle that is never differentiated at all. Lab D explains that a trial must
have acceleration in it or total mass cannot be identified; with `g` known a
force plate is a weighing scale, and the module's own procedure run on a
motionless hold returns 69.97 kg. And §6 promises the reader the knee moment
"the very torque Module 13 used", then stops at the formula and never
computes it. Each of these is a place where a careful reader would conclude
the physics rather than the prose is wrong.

The fixes are all local and all now applied: 16 blocking defects and 12
style edits, 64 replacements in total. Nothing structural had to move. With
them the module does what it promises, and a graduate reader new to
biomechanics can learn inverse dynamics from these pages — including the
part that matters most, which is how far to trust the answer.

---

## 2. Blocking defects

Ranked by severity; the numbering is the rank. Locations are lines in the
**original** `module15.html`.

### B1. §4 states the velocity optimum as 7 Hz; it is 3.0 Hz, and Figure 4 was never computed

`module15.html:258` and `module15.html:260` (the figure), `module15.html:262`
(the caption).

> Figure 4 is this proposition computed for the Section 3 signal: the bias
> falls and the variance rises with $f_c$, and their sum bottoms out near
> $f_c^\star\approx7\ \mathrm{Hz}$

> Their sum is U-shaped, with a minimum-error cutoff near 7 Hz for this 1 Hz
> motion

Fails part 5 (tie to something concrete) and the house rule that every
number is derived, tabulated, or labelled an assumption. The figure is
called "this proposition computed" and it was not computed: decoding its
polylines back through its own axes gives curves that no bias-variance
calculation on any signal in this module produces.

Computing the proposition exactly — the filter-then-differentiate path is
linear, so bias and passed-noise separate — gives, for the synthetic joint
§7 and all four labs actually use (0.8 Hz, 0.40 rad, $f_s=100$ Hz,
$\sigma=0.006$ rad):

```
fc* = 3.02 Hz   bias 0.0132   noise 0.0156   total 0.0205 rad/s
fc = 7 Hz  ->   total 0.0497 rad/s          (2.4x the minimum)
```

Two errors compound here. The prose attributes the figure to the "Section 3
signal" (1 Hz, 0.30 rad) but every downstream use — Lab A's knee, Lab B's
torque optimum, §10's comparison — is against the 0.8 Hz lab signal, so the
comparison the module then draws is between two different signals. And 7 Hz
is not the optimum of *either*: on the §3 signal the optimum is 3.36 Hz.

The replacement recomputes the figure from the lab signal, states the
optimum with the bias and noise that meet there, and — the part the original
never supplied — explains why the optimum is so low and when it is not:

> Figure 4 is this proposition computed for the synthetic joint that Section
> 7 and the labs use throughout — a $0.8\ \mathrm{Hz}$, $0.40\ \mathrm{rad}$
> motion sampled at $f_s=100\ \mathrm{Hz}$ with $\sigma=0.006\ \mathrm{rad}$
> of marker noise. The bias falls and the passed noise rises with $f_c$, and
> their quadrature sum bottoms out at $f_c^\star=3.0\ \mathrm{Hz}$, where a
> bias of $0.013\ \mathrm{rad/s}$ meets a passed-noise standard deviation of
> $0.016\ \mathrm{rad/s}$ for a total RMS velocity error of
> $0.021\ \mathrm{rad/s}$. The minimum is shallow but real: filtering at
> $7\ \mathrm{Hz}$ instead costs $0.050\ \mathrm{rad/s}$, two and a half
> times the minimum. The optimum is this low *because the test signal is a
> single $0.8\ \mathrm{Hz}$ harmonic*: almost no true motion lives above
> $3\ \mathrm{Hz}$, so the bias term stays small down to a low cutoff. A
> broadband movement — a heel strike, the reversal at the bottom of a squat
> — carries real spectral content past $10\ \mathrm{Hz}$, its bias curve
> climbs sooner, and its optimum moves up into the $6$–$10\ \mathrm{Hz}$
> band the Appendix quotes for walking. The shape of Fig. 4 is general; the
> position of its minimum is a property of the movement, and must be found
> for each recording.

The figure body is regenerated from the same array. Decoding the new
polylines back through the axes reproduces the model to a maximum deviation
of 0.00046 rad/s, and the drawn minimum sits at 3.02 Hz.

### B2. Lab A, Lab B and §10 contradict each other on the cutoff, and the stated reason for the ordering is backwards

`module15.html:446`, `:449`, `:468`, `:471`, `:673`.

> The knee — here near 4 Hz — is the cutoff that removes the noise without
> the signal

> It lands a little below the velocity optimum of Fig. 4 ($\sim$7 Hz) and,
> as Lab B shows, right on the torque optimum

> This optimum sits below the velocity optimum of Section 4 (~7 Hz): each
> differentiation is noisier, so the torque, built on the second derivative,
> wants more smoothing than the velocity.

> The torque RMSE is U-shaped and bottoms near $4\ \mathrm{Hz}$ — *below*
> Lab A's $7\ \mathrm{Hz}$ angle knee.

Fails parts 1 and 3. Four passages quote four different cutoffs (4, 7, "a
few Hz lower", "right on"), the last two swap which figure owns which
number, and the *explanation* is wrong.

Running the module's own rules gives one consistent set:

```
Lab A knee (the module's own 1.5x-tail rule, 200 draws):
    median 3.09 Hz, 5-95% [2.79, 3.80]
Lab B torque optimum:  3.43 Hz  (RMSE 0.022 N m)
Fig 4 velocity optimum: 3.02 Hz
```

So the torque optimum is *above* the velocity optimum, not below it. The
reason is visible in the split of $\tau=I\ddot q+mg\ell\sin q$ for this
joint:

```
gravity term peak 3.8199 N m     inertial term peak 0.5053 N m
at fc = 1.5 Hz: gravity-term error 0.2401, inertial-term error 0.0765
```

Seven eighths of the torque is the gravity term — a function of the angle
itself, never differentiated — so over-smoothing damages the torque through
a path that has nothing to do with derivative order. The general rule is
that the optimum follows the *dominant term of the dynamics*, not the
highest derivative in it. The replacement says exactly that, adds the
trial-to-trial scatter of the knee rule (a single trial's knee moves by a
factor of 1.4 between draws, which the original never mentioned), and gives
the extension that tests the claim: rerun with $I=0.5\ \mathrm{kg\,m^2}$ so
the inertial term leads, and the torque optimum then does fall below the
velocity optimum.

The Lab A marker and the Lab B curve are both redrawn from these runs.

### B3. Four of the five shipped code blocks do not run, and the module claims three times that they do

`module15.html:360, 429, 452, 474, 495` (the listings); `:424`, `:518`,
`:678` (the claims).

Extracting every `<pre><code>` block and running it:

```
blk01_L360.py  (Sec 7 pipeline)  runs, prints NOTHING
blk02_L429.py  (Lab A)   NameError: name 'q_meas' is not defined
blk03_L452.py  (Lab B)   NameError: name 'q_meas' is not defined
blk04_L474.py  (Lab C)   NameError: name 'q_true' is not defined
blk05_L495.py  (Lab D)   NameError: name 'a_com_kin' is not defined
```

Against which the module says:

> Each states its physical question, model, parameters, and equations; every
> quoted number is reproduced by the code shown.

> every proposition proved, every figure computed, every number reproduced
> by the code shown.

Fails part 5 outright, and it is the most serious class of defect in this
manuscript because the code blocks are the *only* ground truth the domain
brief recognises for a computed number. A reader cannot check a single
figure in this module against the listing they are given.

All five listings are replaced with self-contained, PEP8, fixed-seed scripts
that define what they use and print what the prose quotes:

```
nb1.py  true peak torque 3.31 N m / filtered 0.071 / unfiltered 1.70
nb2.py  chosen cutoff: median 3.09 Hz, 5-95% [2.79, 3.80]
nb3.py  torque-optimal cutoff 3.4 Hz (RMSE 0.022 N m); 1.5 -> 0.23; 30 -> 1.34
nb4.py  peak 3.41 +/- 0.58 N m (1 sd); 95% CI [2.22, 4.53]; true 3.31
nb5.py  identified M: 70.03 (N=20) ... 70.00 (N=200); static hold 69.97
```

and the three claims are narrowed to what is now true: *every quoted number
is printed by the code shown, which is self-contained and runs as printed
with no other input. The random seeds are fixed, so the numbers below are
the numbers you will get.*

### B4. §7's two headline numbers are wrong, and two different stencils are silently conflated

`module15.html:354` and `:628` (the K4 solution).

> the recovered torque tracks the truth to a root-mean-square error of
> $0.08\ \mathrm{N\,m}$ on a $3.3\ \mathrm{N\,m}$ signal … the estimate has
> an error of $6.8\ \mathrm{N\,m}$, twice the signal itself

Running the pipeline the module actually ships:

```
true peak torque   = 3.31 N m
filtered (6 Hz)    = 0.071 N m RMSE
unfiltered         = 1.70 N m RMSE
```

Neither quoted number survives, and the discrepancy in the second is a
factor of four with a cause worth teaching. The pipeline differentiates by
applying `np.gradient` twice, which is the **wide** stencil
$(q_{k+2}-2q_k+q_{k-2})/(4\Delta t^2)$, not the compact
$(q_{k+1}-2q_k+q_{k-1})/\Delta t^2$ that Proposition 3.1 analyses. The wide
stencil's noise variance is $6\sigma^2/(16\Delta t^4)$, sixteen times
smaller, so its error is four times smaller:

```
unfiltered, np.gradient twice (as shipped)      1.783 N m
unfiltered, compact (1,-2,1)/dt^2 (Prop 3.1)    7.308 N m
```

6.8 is neither, but it is close enough to 7.31 to show where it came from:
the number belongs to a stencil the code does not use. The replacement
quotes 0.07 and 1.70, names both stencils, gives 7.31 as what the compact
one would produce on the same data, and states the rule that a scaling
comparison must hold the stencil fixed. It also records the second detail
needed to reproduce the numbers at all — that the first and last eight
samples are discarded because the zero-lag filter leaves an edge transient
there.

### B5. Lab C reports a one-sigma fraction as if it were the 95 % interval

`module15.html:488` (caption) and `:491`.

> a spread with mean 3.39 N m and 95 % interval [2.28, 4.51] straddling the
> true 3.31. Reporting the single mean would hide that the honest answer
> carries a ±17 % uncertainty

Fails part 1. The sentence names the 95 % interval and then attaches ±17 %
to it, but ±17 % is one standard deviation. The 95 % interval is ±34 %. This
is the commonest way to understate an inverse-dynamics error bar, and the
module makes it in the one lab whose entire subject is reporting the width
honestly. Running the shipped Lab C:

```
peak = 3.41 +/- 0.58 N m (1 sd); 95% CI [2.22, 4.53]
1 sd = 17% of the mean; 95% half-width = 34% of the mean
```

The replacement gives mean, standard deviation and interval as three
separate quantities, states that the two widths differ by a factor of two,
and names the error the original committed so the reader does not repeat it.

### B6. Three of the error budget's four numbers cannot be reproduced, and the "poorly chosen cutoff" is never named

`module15.html:398`, `:402` (the bars), `:404` (caption), `:686`.

> the $15\%$ body-segment-parameter uncertainty contributes far more RMS
> error ($0.41\ \mathrm{N\,m}$) than the marker noise ($0.09$) or even a
> poorly chosen cutoff ($0.31$)

Fails parts 1 and 5. The passage does not say what statistic these are (per
draw or pooled), over how many draws, or — for the cutoff bar — *what
cutoff*. "A poorly chosen cutoff" is not a number, and without it the 0.31
cannot be checked. Pinning every choice down and running it:

```
pooled RMS over draws and interior samples, one source at a time
  BSP 15% alone, fc=6         0.414   (20 000 draws; closed form 0.415)
  marker noise alone, fc=6    0.059
  cutoff alone, fc=1.5        0.228   (deterministic, no averaging needed)
  filter bias alone, fc=6     0.004   (deterministic)
```

So 0.09 and 0.31 are both wrong, and 0.41 is right by luck: at the 600 draws
a first pass would use, that bar still moves by ±0.02 between seeds. The BSP
term has a closed form, which is what settles it — linearising in the
parameter errors,

$$u\sqrt{\langle(I\ddot q_f)^2+(mg\ell\sin q_f)^2\rangle}=0.415\ \mathrm{N\,m}
\quad\text{at } u=15\%,$$

and the 20 000-draw Monte Carlo reproduces it. The replacement states the
statistic, the draw count, the cutoff (1.5 Hz, over-smoothed by more than a
factor of two below the optimum of Fig. 4), and the closed form; it also
notes that averaging the per-draw RMSE instead of pooling reports 0.33,
because the mean of $|\delta m|$ is $\sqrt{2/\pi}$ times its standard
deviation — same data, different statistic, unchanged ranking. Verified:
the per-draw mean is 0.3295 against $\sqrt{2/\pi}\times0.4146=0.3308$.

The four bars are redrawn to the corrected values, and the §10 crossover
argument is made explicit rather than gestured at: both terms are linear in
their uncertainty near the operating point, so the parameter contribution
falls to the marker contribution at
$u^\star=15\%\times(0.059/0.414)=2.1\%$ — a precision on a segment mass that
no regression table or scale delivers, so in practice the allocation never
tips.

### B7. Lab D's stated reason for needing movement is false, and the module's own code disproves it

`module15.html:502`, `:508`, `:711`.

> The information comes from acceleration: only when the body accelerates
> does the force plate constrain the mass (at rest, $F_y=Mg$ fixes only
> $Mg$, not $M$ separately from $g$).

> at rest $F_y=Mg$ constrains only the product, so a static trial cannot
> identify $M$

Fails part 1 and part 4. The claim is simply untrue when $g$ is known, which
it is everywhere else in this course. The residual the lab regresses,
$\ddot y^{\rm kin}-(F_y/M-g)$, is not blind to $M$ at rest: hold still and
$F_y=M_{\rm true}g$, so the residual is $g(1-M_{\rm true}/M)$, which
vanishes only at $M=M_{\rm true}$. Running the identification on a
motionless hold:

```
N= 20  identified M = 70.03 kg  (predicted s.e. 0.19 kg)
N=200  identified M = 70.00 kg  (predicted s.e. 0.06 kg)
static hold (no acceleration at all): M = 69.97 kg
```

The estimate does not converge as frames are added because it starts
converged. What more data buys is precision — the standard error
$\sigma_aM/(g\sqrt N)$ falls from 0.19 kg to 0.06 kg — not identifiability.

The rescue case is the interesting one and the original omitted it: what
genuinely *needs* acceleration is the mass **distribution**, the segment
fractions $f_i$ and COM fractions $\rho_i$, because at rest those enter the
measurements only through the single weighted sum $\sum_if_i\mathbf r_{c,i}$
— one equation for many unknowns — whereas accelerating segments enter with
different time courses and separate them. The replacement states the
principle in the form that is actually true: an inverse problem is well-posed
for a parameter exactly when the motion excites the term that parameter
multiplies, and gravity already excites the term total mass multiplies. The
extension now asks the reader to confirm that a static trial leaves the
segment-mass design matrix rank-deficient, which is the precise sense in
which movement is required.

### B8. The §6 worked example promises the knee moment and never computes it

`module15.html:311`.

> The Euler step then returns the net knee moment $M_p=I\alpha-M_d-(\mathbf
> r_d\times\mathbf F_d)-(\mathbf r_p\times\mathbf F_p)$ once the segment's
> pose fixes the moment arms … the very knee torque Module 13 used to
> analyse the chair rise, now produced from measured motion rather than
> assumed.

Fails parts 3 and 5. The example carefully sets up mass, inertia,
accelerations, the distal reaction and the ankle moment, works the Newton
step to $\mathbf F_p=(-13.7,-653.7)$ N, and then hands the reader a formula
and a promise instead of the number. The pose is never fixed, so the moment
arms are never resolved into components, so the cross products are never
taken. This is the module's only worked instance of its central recursion.

The replacement assumes a pose explicitly (labelled as an assumption), works
both cross products, and gets the number:

```
unit vector along shank (cos75, sin75) = (0.2588, 0.9659)
r_p = ( 0.0448,  0.1673) m   |r_p| = 0.173 m
r_d = (-0.0587, -0.2191) m   |r_d| = 0.227 m
r_d x F_d = -37.22 N m       r_p x F_p = -27.00 N m
I alpha   =   0.144 N m
M_p = 0.144 + 8 + 37.22 + 27.00 = 72.4 N m
```

The lengths 0.173 and 0.227 m reproduce the 0.17 and 0.23 the surrounding
prose already quotes, so the assumed pose is consistent with the figure.
Vectors are given to four decimals precisely so that a reader retyping them
lands on 72.4 rather than on a different last digit.

The number then earns a point the module makes nowhere else: the inertial
term $I\alpha=0.144\ \mathrm{N\,m}$ is negligible beside the two
force-moment terms, 37.22 and 27.00. At squat speeds a joint moment is
almost entirely the moment of the joint *forces* about the segment centre —
which is why an error in the measured $\mathbf F_d$ at the foot propagates
almost undamped into every joint above it, and why the force plate must be
the accurate instrument in the chain.

### B9. Proposition 4.1 claims a unique minimum from hypotheses that do not give one

`module15.html:254` (statement) and `:256` (proof).

> If both are smooth with $B^2$ convex-decreasing and $V$ increasing from
> zero, the total has a unique interior minimum

> the derivative $\tfrac{d}{df_c}(B^2+V)$ moves from negative … to positive
> …, crossing zero once

Fails parts 1 and 3. Monotone-increasing $V$ is not enough: $(B^2)'$ is
nondecreasing by convexity, but $V'$ may oscillate, so the sum need not be
monotone and may cross zero many times. The proof asserts the single
crossing rather than deriving it. The fix is one word in the hypothesis —
$V$ **convex**-increasing — after which $(B^2)'+V'$ is a sum of two
nondecreasing functions, hence nondecreasing, hence crosses zero at most
once. The replacement proof says that, and adds the limit case the original
lacked: drop convexity of $V$ and a minimum still exists on any compact
range of cutoffs, but need not be unique.

### B10. $L$ means the segment length in Definition 2.2 and the joint-to-COM distance in every torque formula

`module15.html:344`, `:392`, `:394`, `:396`, `:560`, `:614`, `:628`, `:686`,
`:700`, `:711` — ten sites plus one SVG label.

Definition 2.2 fixes $L_i$ as the segment length and $\rho_i$ as the COM
fraction, so the joint-to-COM distance is $\rho_iL_i$. Every subsequent
appearance of the single-joint torque writes it $\tau=I\ddot q+mgL\sin q$
with $L=0.25\ \mathrm{m}$ — which is the *distance to the COM*, not a
segment length. The same letter carries two meanings a factor $\rho\approx
0.43$ apart, in a module whose subject is getting the gravity term right.
This is a defect by the manuscript's own symbol rule, and flagging it is not
resolving it.

Resolved by giving the second meaning its own symbol $\ell=\rho_iL_i$
throughout: the §7 model, the §8 sensitivity partials
($\partial\tau/\partial m=g\ell\sin q$), the D9 linearisation, the two
gravity-torque limit cases, the K4 parameter block, the C10 solution, and
the C10 figure's own label, which becomes `τ = mgℓ` (as the entity
`&#8467;`, since MathJax does not typeset inside `<svg><text>`). §7 now also
says in words that $\ell$ is the joint-to-COM distance, not the segment
length, and that confusing them misplaces the gravity term.

### B11. The Appendix records neither the synthetic joint's assumed numbers nor half the symbols the text uses

`module15.html:684` (notation table) and `:690` (parameter table).

Fails the evidence rule: a number that is neither derived, nor a table
parameter with symbol and unit, nor labelled an assumption is a blocking
defect. The entire synthetic joint — $I=0.05\ \mathrm{kg\,m^2}$,
$m=4\ \mathrm{kg}$, $\ell=0.25\ \mathrm{m}$, the test motion, the sampling
rate, the marker noise, the 6 Hz working cutoff, the 2.5 N plate noise Lab D
assumes, the 0.12 m/s² kinematic noise — carries the whole of §7 to §10 and
appears in no table. Nor is it labelled: §7 introduces it as though it were
measured.

The notation table was missing $\mathbf a_{c,i}$, $\alpha_i$, $\mathbf r_p$,
$\mathbf r_d$, $\mathbf r_{\rm COP}$, $\tau$, $\ell$, $\mathbf x$, $b$,
$\nu$ and $u$ — every symbol of §6 and most of §7 to §8. Four notation rows
and six parameter rows were added, each labelled **assumed** where it is an
assumption, each linked to its section, and §7 now states in the text that
the joint's numbers are assumed and are round numbers bracketing the human
shank of §2 ($m=3.3$ kg, $I=0.048\ \mathrm{kg\,m^2}$, $\rho L=0.17$ m),
verified:

```
m = 0.0465*70 = 3.2550 kg    c = 0.433*0.40 = 0.1732 m
I = m*(0.302*0.40)^2 = 0.04750 kg m2
```

### B12. The module never places its models on the level ladder

`module15.html:64`.

The domain brief requires every module to say which level of the ladder its
models sit on; §0 named the phenomenon and the four labs but not the level.
The replacement places these sections at **Level 4** (inverse kinematics and
inverse dynamics), built on the **Level 3** multibody link-segment model of
§2, and says what is and is not new: the mechanics is the rigid-body
mechanics of Modules 1 to 3, and what is new is running it backwards, from
measured motion to the forces that caused it, with an error bar attached. No
new tissue law and no controller enters here. (Checked against
`prompt.txt:289–290`, which define Level 3 as multibody link-segment models
and Level 4 as inverse kinematics and inverse dynamics.)

### B13. §5 quotes two numbers its own figure contradicts

`module15.html:295`.

> track each other to within a residual of about $0.13\ \mathrm{m/s^2}$ on a
> signal peaking near $1.6\ \mathrm{m/s^2}$

Decoding the two polylines of Figure 5 back through its own axes
(y = 123 px → 0, y = 83 px → 1 m/s²):

```
force-plate curve peak |a| = 1.730 m/s2
kinematic curve   peak |a| = 1.818 m/s2
drawn residual: rms 0.123, max 0.295 m/s2
```

So the peak is 1.7, not 1.6, and the residual is 0.12 rms. "About 0.13"
also leaves the statistic unstated. The replacement says root-mean-square
residual 0.12 m/s² on a signal peaking at 1.7 m/s², makes the consistency
"about seven per cent" rather than "a few per cent" (0.12/1.7 = 7.1 %), and
ties the number forward: that residual is the noise level Lab D later
assumes for the kinematic side, which is where the 0.12 in the parameter
table comes from.

### B14. K1 computes its two halves with different stencils, so every ratio it reports is wrong

`module15.html:611`.

> The *raw* acceleration noise $\sigma\sqrt6/\Delta t^2$ climbs from
> $37\ \mathrm{rad/s^2}$ at $50\ \mathrm{Hz}$ to $2360$ at $400\
> \mathrm{Hz}$ … $10$ to $500\times$ smaller than the raw value

Fails part 1. The "raw" column uses the compact stencil
($\sigma\sqrt6/\Delta t^2$) while the "filtered" column runs `np.gradient`
twice — the wide stencil, four times quieter. The comparison therefore
divides one stencil by another, and the ratios are inflated fourfold. The
problem's whole point is a ratio.

Holding the pipeline's own stencil on both sides:

```
fs= 50 Hz  raw sd =    9.2  filtered RMSE = 2.04  ratio    5x
fs=100 Hz  raw sd =   36.7  filtered RMSE = 1.97  ratio   19x
fs=200 Hz  raw sd =  147.0  filtered RMSE = 1.56  ratio   94x
fs=400 Hz  raw sd =  587.9  filtered RMSE = 1.13  ratio  519x
```

The corrected numbers also make the problem's conclusion *stronger* and more
accurate. The original said the filtered error "stays essentially flat"; it
does not — it **falls**, 2.04 → 1.13, because a faster camera puts more
independent samples inside the filter's passband. The replacement states the
$64\times$ raw rise (unchanged, and noted as identical for either stencil),
the falling filtered column, and why the residual ~2 rad/s² does not go to
zero with $f_s$: it is dominated by the filter bias on a signal whose true
acceleration peaks at 10.1 rad/s², not by the noise. The Probes note now
also names the mechanism the problem tests — holding one stencil fixed
across a comparison.

### B15. K1's four-row table is produced by no code in the module

`module15.html:611`.

K1 is a computational problem whose solution quotes a four-row sweep. Under
the manuscript's own standard — K solutions carry Python-verified numbers
*with code* — the table needs its listing, and there was none. The
corrected sweep is added as a copy-buttoned block that prints exactly the
four rows quoted (`nb6.py`, PEP8-clean, fixed seed).

### B16. The Lab C figure still draws the superseded distribution

`module15.html:488`.

Found by decoding, not by reading: after B5 corrected the caption to the
interval the shipped code prints, the figure underneath it was still drawn
from the old run. Its green bar, labelled "95 % interval", spans

```
drawn [2.28, 4.51]   vs   caption and code [2.22, 4.53]
```

A figure that disagrees with its own caption is a factual error by the
domain brief, and this is the same defect class as B13 — with the twist that
the correction to B5 is what created it. The histogram, the true-value
marker and the interval bar are all redrawn from the same 2000 draws the
shipped Lab C listing prints, keeping the axis calibration
($x = 75 + 105.38\,(v-1.5)$) so the tick labels still land on their ticks.
Decoding the new figure returns the interval [2.220, 4.534] against the
model's [2.220, 4.534].

---

## 3. Style and clarity edits

Twelve line-level edits, all applied. The dominant pattern is a reflex use
of "honest" as an intensifier — six occurrences, each doing no work and two
of them actively misleading, since the passage that calls a ±17 % figure
"the honest answer" is the one understating the interval (B5).

| tag | original | replacement |
|---|---|---|
| S1 | "how loudly its muscles fire" | "what voltage its muscles put on the skin" — EMG measures potential, not loudness, and the module is about knowing what each instrument records |
| S2 | "amplifies noise catastrophically" | "amplifies noise by a factor that grows as a power of the sampling rate" — the hyperbole replaced by the actual law |
| S3 | "the single most dangerous step in all of biomechanics" | "the step that most often ruins a biomechanics result" |
| S4 | "the pipeline's most treacherous step" | "the pipeline's most error-prone step" |
| S5 | "The numbers are sobering." | "The numbers settle it." |
| S6 | "the honest output is a torque with an uncertainty band" | "the useful output is …" |
| S7 | "the honest goal is not \"no noise\" but *minimum total error*" | "the goal is not the smoothest curve but *the smallest total error*" |
| S8 | "the honest tool is **Monte Carlo**" | "the reliable tool is **Monte Carlo**" |
| S9 | "How wide is the honest error bar" | "How wide is the error bar" |
| S10 | "The only honest way to test such a pipeline" | "The only way to test such a pipeline" |
| S11 | "This is the whole idea in twenty lines:" | "This is the whole idea in one screen of code:" — the listing is not twenty lines |
| S12 | "halving the marker noise barely changes it." | adds *why* both halves behave as they do: the parameter term is linear in its uncertainty, the marker term is already an order of magnitude smaller |

---

## 4. Structural notes

**Nothing needs to move.** The section order is correct and the dependencies
point backwards throughout: §3 establishes noise amplification before §4
needs it, §4 fixes the cutoff before §7 uses it, §6 derives the recursion
before §7 codes it, §8 prices the uncertainty before §9 identifies against
it. I found no forward reference the reader must accept on faith.

Three observations that are not defects:

1. **§7's synthetic joint is the module's running example and should be
   named as such.** It carries §7 through §10 and all thirty problems, but
   it is introduced almost in passing. The B10a/B11b replacements now
   state its parameters, label them assumed, tie them to the §2 shank, and
   table them — which is as far as an edit should go. If the module is ever
   revised further, promoting it to a named example in §0 would help.

2. **The 6 Hz working cutoff is an assumption that the module's own
   computation argues against.** §7 to §10 filter at 6 Hz while Fig. 4 and
   Lab B compute optima of 3.0 and 3.4 Hz. This is defensible — 6 Hz is the
   conventional gait-analysis setting the Appendix quotes, and the error
   budget shows the penalty is small — but it was nowhere acknowledged. The
   Appendix row added in B11b now states the working cutoff and both
   computed optima side by side, so the reader sees the gap rather than
   tripping over it.

3. **The problem set is the strongest in the module and needed almost no
   work.** Only K1 required correction (B14, B15), and that was an
   arithmetic defect, not a design one.

---

## 5. What already works

Named so the author knows what to imitate.

- **§1's instrument-by-instrument table.** Each device is introduced by what
  it physically records, not by what it is used for — cameras record marker
  positions, plates record the resultant and its point of application, EMG
  records a potential. This is the discipline the rest of the course's
  "measure the torque" shorthand needs, and it is exactly right.

- **§3's derivation of noise amplification.** Proposition 3.1 is stated
  precisely, proved in the smallest setting, and tied to a number the reader
  can check: 0.006 rad of marker noise becomes 0.42 rad/s of velocity noise
  and 147 rad/s² of acceleration noise against a true acceleration of 11.8 —
  twelve times the signal. Every one of those numbers reproduces (verified:
  0.4243, 146.97, 11.8435, ratio 12.41). This is the model section.

- **§6's Newton-Euler recursion.** The derivation is complete and correct:
  Newton for the free-body force, Euler about the centre of mass for the
  moment, the observation that $\mathbf F_p$ is already known so the moment
  equation has one unknown, and the third-law hand-off that propagates the
  measured ground reaction up the chain. Only the worked instance was
  missing (B8).

- **The thirty problems.** Every K problem requires a sweep, an
  optimisation, an inverse solve, a simulation, or a regime comparison. K9
  (find where marker noise and parameter uncertainty trade dominance) and
  K10 (allocate a fixed measurement budget between them) are the kind of
  problem the domain brief asks for and most modules do not supply.

- **The closing move of the module.** Ending on identification and
  validation — how you would know the pipeline is wrong — rather than on the
  pipeline itself is the right structural choice, and §9's dynamic residual
  as a diagnostic that distinguishes a mass error from a smoothing error is
  a genuinely good idea, well figured.

---

## 6. Changes applied

64 replacements: 16 blocking defects (52 edits) and 12 style edits. Applied
to `edited/module15.html` by one re-runnable script,
`scratchpad/m15/apply.py`, each anchor asserted to occur exactly once.
Line numbers are in the original `module15.html`.

| tag | line | what changed | how verified |
|---|---|---|---|
| B12 | 64 | §0 gained the level-ladder placement: Level 4 (inverse kinematics and inverse dynamics) built on the Level 3 link-segment model of §2, plus a sentence saying no new tissue law or controller enters | `prompt.txt:289-290` defines Level 3 and Level 4 in those words |
| B9a | 254 | Proposition 4.1 hypothesis "$V$ increasing from zero" replaced by "$V$ convex-increasing from zero" | the uniqueness step needs $(B^2)'+V'$ nondecreasing; monotone $V$ alone does not give it |
| B9b | 256 | proof rewritten to derive the single crossing from the sum of two nondecreasing derivatives, plus the limit case if convexity is dropped | hand derivation |
| B1a | 258 | §4 prose: optimum 7 Hz → 3.0 Hz; figure re-attributed from the §3 signal to the lab signal actually used; bias 0.013, noise 0.016, total 0.021 rad/s added; cost at 7 Hz 0.050 (2.5x) added; the bandwidth argument for why the optimum is low, and when it is not, added | `v3.py` exact bias-variance split: fc*=3.02, bias 0.0132, noise 0.0156, total 0.0205; `v1.py` fc=7 → 0.0504 |
| B1b | 260 | Figure 4 body regenerated from the computed arrays (bias, noise, total over a 60-point log grid), and the two curve labels moved out of the curves | `figaudit2.py` decodes the new polylines to max deviation 0.00046 rad/s from the model, drawn minimum at 3.02 Hz; `check_overlap` 0 |
| B1c | 262 | Fig. 4 caption: "minimum near 7 Hz for this 1 Hz motion" → "at 3.0 Hz for this 0.8 Hz motion", plus the note that the minimum moves up with bandwidth | same run as B1a |
| B2a | 445 | Lab A knee marker redrawn at the computed knee and relabelled with its value | `nb2.py` median 3.09 Hz |
| B2b | 446 | Lab A caption: knee "near 4 Hz" → "at 3.1 Hz, the median over 200 independent noise draws"; "data-free" → "truth-free"; now says it lands on the velocity optimum (3.0 Hz) | `nb2.py` (200 draws, seed 15) prints median 3.09 |
| B2c | 449 | Lab A interpretation: adds the 5-95 % range 2.8-3.8 Hz, states agreement with Fig. 4 to within single-trial scatter, corrects the Lab B relation to "just below the torque optimum (3.4 Hz)", and adds that one trial's knee moves by a factor 1.4 between draws | `nb2.py` [2.79, 3.80]; ratio 3.80/2.79 = 1.36 |
| B2d | 468 | Lab B: "minimised near 4 Hz" → "at 3.4 Hz (0.022 N m)"; adds 1.34 N m at 30 Hz; corrects the ordering to *above* the velocity optimum and replaces the "each differentiation is noisier" explanation with the gravity-term-dominance one | `nb3.py` 3.4 Hz / 0.022 / 1.34; `v3.py` gravity peak 3.8199 vs inertial 0.5053 |
| B2e | 471 | Lab B interpretation rewritten: the full split (7/8 of the torque is the gravity term), the fc=1.5 Hz error decomposition 0.24 vs 0.08, the general rule (the optimum follows the dominant term, not the highest derivative), corrected sensitivity, and an extension that flips the ordering by raising $I$ | `v3.py` at fc=1.5: gravity-term error rms 0.2401, inertial 0.0765 |
| B2f | 467 | Lab B figure body regenerated (torque RMSE vs cutoff, 30-point log grid, minimum marker at the computed optimum) | `figaudit2.py` decodes drawn min 0.0217 at 3.43 Hz against model 0.0218 at 3.43 Hz, max deviation 0.00045; value at 30 Hz 1.3358 |
| B2g | 673 | §10 reconciliation rewritten: knee median 3.1 vs velocity optimum 3.0, why narrowband motion makes them agree, torque optimum 3.4 above both, and the condition under which the surrogate fails | `nb2.py`, `v3.py` as above |
| B10a | 344 | §7: $mgL$ → $mg\ell$; adds that $\ell=\rho_iL_i$ is the joint-to-COM distance and not the segment length; labels the synthetic joint's numbers **assumed**; brackets them against the §2 shank; points at the Appendix | `v1.py` shank m=3.2550, c=0.1732, I=0.04750 |
| B10b | 392 | §8 sensitivity model: $\tau=I\ddot q+mg\ell\sin q$, with $\ell$ named | symbol audit |
| B10c | 394 | partial $\partial\tau/\partial m=gL\sin q$ → $g\ell\sin q$ | symbol audit |
| B10d | 396 | proof line "differentiating $\tau=I\ddot q+mgL\sin q$" → $mg\ell$ | symbol audit |
| B10e | 700 | D9 solution: full linearisation rewritten in $\ell$, with the parenthetical distinguishing it from segment length | symbol audit |
| B10f | 560 | limit case "should return exactly the gravity torque $mgL$" → $mg\ell$ | symbol audit |
| B10g | 628 | K4 parameter block: $L=0.25$ → $\ell=0.25$, and the parameters attributed to the §7 assumed joint | symbol audit |
| B10h | 686 | "collapses to the pure gravity torque $mgL$" → $mg\ell$ | symbol audit |
| B10i | 711 | C10 solution "Exactly the gravity torque $mgL$" → $mg\ell$ | symbol audit |
| B10j | 560 | the C10 figure's own SVG label `τ = mgL` → `τ = mg&#8467;` | SVG `<text>` cannot carry MathJax, so the script ell goes in as an entity; `check_svg` 0 |
| B4a | 354 | §7 headline numbers 0.08 / 6.8 N m → 0.07 / 1.70 N m on a 3.31 N m peak; adds the wide-vs-compact stencil distinction with 7.31 N m for the compact one, and the eight-sample edge trim | `nb1.py` 3.31 / 0.071 / 1.70; `v2.py` compact stencil 7.3080 |
| B4b | 356 | Figure 7 body regenerated from the shipped pipeline (true, filtered, unfiltered torque) | the shipped figure decoded to a true peak of 3.54 N m and an unfiltered RMSE of 4.38, matching neither the code nor the prose; regenerated from `nb1.py`'s arrays |
| B4c | 628 | K4 solution: same two numbers corrected, $mg\ell$, and the compact-stencil figure added | `nb1.py`, `v2.py` |
| B8 | 311 | §6 worked example completed: pose assumed at 75°, both moment arms resolved, both cross products taken, $M_p=72.4\ \mathrm{N\,m}$, and the observation that the inertial term is negligible beside the force-moment terms | `v4.py` exact: r_p=(0.0448,0.1673), r_d=(-0.0587,-0.2191), r_d×F_d=-37.2170, r_p×F_p=-27.0136, Iα=0.144, M_p=72.3746; retyping the printed 4-dp vectors gives 72.36, also 72.4 |
| B13 | 295 | §5: residual "about 0.13" → "root-mean-square 0.12 m/s²"; peak "near 1.6" → "at 1.7"; "a few per cent" → "about seven per cent"; ties the residual to Lab D's assumed kinematic noise | `figchk.py` decodes Fig. 5: force-plate peak 1.730, drawn residual rms 0.123 |
| B6a | 398 | §8 budget prose: 0.41/0.09/0.31 → 0.414/0.059/0.228 with 0.004 for filter bias; names the statistic (pooled RMS), the draw count (20 000), and the bad cutoff (1.5 Hz); adds the closed form 0.415 and the note that 600 draws leaves ±0.02 of scatter | `v4.py` analytic 0.4146, MC 0.4145 (N=20 000) / 0.4141 (N=200 000); deterministic cutoff 0.2285 and bias 0.0036; `genfig15.py` bars 0.414/0.059/0.228/0.004 |
| B6b | 402 | the four error-budget bars redrawn to the corrected values | `figaudit2.py`: bar heights 105.0/14.9/57.9/1.0 px scale to 0.4140/0.0587/0.2283/0.0039, matching their printed labels |
| B6c | 404 | Fig. 8 caption states the pooling, the draw count, the bad cutoff and where the bias is measured | same run |
| B6d | 686 | K7 solution: corrected numbers, and the per-draw-vs-pooled distinction with 0.33 and the $\sqrt{2/\pi}$ reason | `v4.py` per-draw mean 0.3295 against $\sqrt{2/\pi}\times0.4146=0.3308$ |
| B6e | 686 | K10 solution: corrected numbers and an explicit crossover $u^\star=15\%\times(0.059/0.414)=2.1\%$, with why the allocation never tips in practice | arithmetic on the verified bar values |
| B5a | 488 | Lab C caption: mean 3.39 → 3.41, sd 0.58 added, interval [2.28,4.51] → [2.22,4.53]; the ±17 % that was attached to the 95 % interval separated into 1 sd = 17 % and 95 % = ±34 % | `nb4.py` 3.41 ± 0.58, CI [2.22, 4.53], 17 % and 34 % |
| B5b | 491 | Lab C interpretation: same correction, plus the statement that the two widths differ by a factor of two and that quoting the first as the interval is the commonest understatement | `nb4.py` |
| B16 | 488 | the Lab C figure body redrawn from the same 2000 draws as the caption: histogram, true-value marker and the green 95 % interval bar, which had still spanned the superseded [2.28, 4.51] | `figaudit2.py` decodes the new bar to [2.220, 4.534] against the model's [2.220, 4.534]; axis calibration preserved (x = 75 + 105.38(v−1.5)), ticks unmoved |
| B7a | 502 | Lab D caption: "scatters … settles onto the true 70 kg" → sits within half a kilogram from 20 frames on; standard error 0.19 → 0.06 kg; states that more data buys precision, not identifiability | `nb5.py` 70.03 (N=20) to 70.00 (N=200), s.e. 0.19 → 0.06 |
| B7b | 508 | Lab D interpretation rewritten: the residual is not blind to $M$ at rest ($g(1-M_{\rm true}/M)$), the static-hold run returns 69.97 kg, what actually needs acceleration is the mass distribution, corrected sensitivity, and an extension about rank deficiency | `nb5.py` static hold 69.97 kg |
| B7c | 711 | K8 solution: same correction, ending on the correct principle — an inverse problem is well-posed for a parameter when the motion excites the term that parameter multiplies | `nb5.py` |
| B14a | 611 | K1 solution: both halves put on the pipeline's own stencil, so raw 9.2 → 588 (not 37 → 2360) and ratios 5x → 519x (not 10x → 500x); "stays essentially flat" corrected to "falls" with the four values; adds why the residual does not vanish with $f_s$ | `nb6.py` 9.2/36.7/147.0/587.9 raw, 2.04/1.97/1.56/1.13 filtered; true acceleration peak 0.40(2π·0.8)² = 10.10 rad/s² |
| B14b | 611 | K1 Probes note now names the mechanism: holding one stencil fixed across a comparison | — |
| B3a | 360 | §7 listing replaced by a self-contained script that defines its own signal and prints the three numbers §7 quotes | `nb1.py` runs; prints 3.31 / 0.071 / 1.70; `check_code` 0 |
| B3b | 429 | Lab A listing replaced (the original raised `NameError: q_meas`) | `nb2.py` runs; prints median 3.09 Hz, [2.79, 3.80] |
| B3c | 452 | Lab B listing replaced (the original raised `NameError: q_meas`) | `nb3.py` runs; prints 3.4 Hz / 0.022 / 0.23 / 0.74 / 1.34 |
| B3d | 474 | Lab C listing replaced (the original raised `NameError: q_true`) | `nb4.py` runs; prints 3.41 ± 0.58, [2.22, 4.53] |
| B3e | 495 | Lab D listing replaced (the original raised `NameError: a_com_kin`) | `nb5.py` runs; prints 70.03 → 70.00 and the static hold 69.97 |
| B3f | 424 | "every quoted number is reproduced by the code shown" → "printed by the code shown, which is self-contained and runs as printed", plus the fixed-seed guarantee | true of the five replacements |
| B3g | 518 | problem-set preamble: computational solutions "quote numbers the code produces" → quote only numbers printed by a run, naming which run | true after B3a-e and B15 |
| B3h | 678 | the repayment section's "every number reproduced by the code shown" narrowed to "every quoted number printed by a run of the code shown" | true after B3a-e |
| B11a | 684 | four notation rows added: §6's $\mathbf a_{c,i},\alpha_i,\mathbf r_p,\mathbf r_d,\mathbf r_{\rm COP}$; §7's $\tau$ and $\ell$ (with $\ell=\rho_iL_i$ distinguished from $L_i$); §1/§4/§8's $\mathbf x$, $b$, $\nu$, $u$ | symbol audit against §0-§10 |
| B11b | 690 | six parameter rows added: the assumed synthetic joint, the assumed test motion with its 3.31 N m peak, the working cutoff with both computed optima, Lab D's 2.5 N plate noise, the 0.12 m/s² kinematic noise matched to Fig. 5, and the Monte Carlo draw counts; each marked assumed where it is one | `v1.py`, `nb4.py`, `figchk.py`, `genfig15.py` |
| B15 | 611 | K1's four-row table given the listing that produces it, as a copy-buttoned code block | `nb6.py` prints exactly the four quoted rows; `check_code` 0 across 6 blocks |
| S1 | 62 | "how loudly its muscles fire" → "what voltage its muscles put on the skin" | — |
| S2 | 228 | "amplifies noise catastrophically" → "by a factor that grows as a power of the sampling rate" | — |
| S3 | 230 | "the single most dangerous step in all of biomechanics" → "the step that most often ruins a biomechanics result" | — |
| S4 | 232 | "most treacherous step" → "most error-prone step" | — |
| S5 | 240 | "The numbers are sobering." → "The numbers settle it." | — |
| S6 | 390 | "the honest output" → "the useful output" | — |
| S7 | 250 | "the honest goal is not \"no noise\"" → "the goal is not the smoothest curve but the smallest total error" | — |
| S8 | 392 | "the honest tool is Monte Carlo" → "the reliable tool is Monte Carlo" | — |
| S9 | 480 | "How wide is the honest error bar" → "How wide is the error bar" | — |
| S10 | 340 | "The only honest way to test such a pipeline" → "The only way to test such a pipeline" | — |
| S11 | 358 | "the whole idea in twenty lines" → "the whole idea in one screen of code" | the listing is not twenty lines |
| S12 | 404 | adds why each half of the sensitivity behaves as it does (linearity of the parameter term; the marker term already an order of magnitude smaller) | `v4.py` budget values |

### Gate results

Nine gates on `edited/module15.html`, against the baseline recorded on the
pristine copy before any edit.

| gate | baseline | after |
|---|---|---|
| `checktex` | 444 segments, 0 issues | 583 segments, **0 issues** |
| `checklt` | 0 | **0** |
| `check_links` | 140 links, 0 broken, 0 unlinked | 158 links, **0 broken, 0 unlinked** |
| `check_svg` | 0 hard, 0 advisory | **0 hard, 0 advisory** |
| `check_code` | 5 blocks, 0 issues | 6 blocks, **0 issues** |
| `verify_dom` | 0 mjx-merror, 0 broken, 0 swallowed (12 stray `$` advisory) | **0 mjx-merror, 0 broken, 0 swallowed** (12 stray `$` advisory, unchanged) |
| `check_overlap` | 0 | **0** |
| `check_frame` | pass (no clipping; wasted-margin advisories on C1, C2, D6) | **pass** (same three advisories, unchanged) |
| `check_bodyprop` | pass | **pass** |

Zero everywhere the baseline was zero, and no gate worse anywhere.
