# Editor report — `module08.html` (Walking biomechanics)

**Editor:** `science-editor` pass, 2026-09-07. Domain brief: `EDITOR_DOMAIN.md`.
**Scope:** the whole module — §0 through §12 and the Appendix, every figure caption,
all 30 problems, all 5 diagnostics, the captures/misses table, and the four lab code
blocks (extracted and run before any prose was read).
**Working copy:** `edited/module08.html`. `module08.html` was never touched.
**Verification assets:** `<scratchpad>/m08/nums.py`, `knums.py`, `lab3.py`,
`blocks/blk0{1..4}_L*.py`. Every number quoted below as a replacement was printed by
one of those runs.

---

## 1. Verdict

**Yes, after revision — and the revision is substantial.**

The spine of this module is sound and, in places, genuinely good. Ten propositions
carry real proofs, and I checked all ten: Prop 2.2's contact-constraint derivation of
`Fr ≤ 1` from `N = M(g − v²/ℓ) ≥ 0` is exactly the "smallest setting that shows the
mechanism" the standard asks for; Prop 4.1's angular-momentum-about-the-new-contact
argument for `θ̇⁺ = θ̇⁻cos2α` is correct and is then reused honestly by Prop 5.1 and
Prop 9.1; Prop 9.1's energy balance `MgL sinγ = ½Mv²sin²2α` is right, and its "on the
level the only solution is v = 0" is the kind of limit case the standard demands.
Nothing in the argument structure is faked.

What fails is everything downstream of the arguments: **the numbers, the labs, and
the problems.**

The four labs are the worst of it. All four run, but **not one number they print
appears anywhere in the module.** §11 opens by claiming "each one varies a parameter
and asks what mechanism changes" and then presents four bare code blocks with no
result, no interpretation, and no sensitivity statement. Lab 3 is titled
"inverse-dynamics estimate" and performs no inverse dynamics at all: it asserts a
Gaussian ankle torque and multiplies it by an asserted Gaussian angular velocity.
Meanwhile the module's own optimum step length — computed by Lab 2 as **0.684 m** —
is quoted in K3 and K7 as "≈0.6 m", a number that appears nowhere in any run and that
the reader cannot reproduce because §7's cost proxy `C(v,L)` leaves `A`, `B` and `C₀`
undefined. K10's third sensitivity number, "≈0.30 to step reach", is not reproducible
under any definition of the margin: the capture point does not contain step reach at
all (elasticity exactly 0) and the margin's elasticity to it is 2.68.

Two propositions are internally inconsistent. **Prop 5.2 states a scaling law that
does not produce the result it concludes with:** it proves that splitting a
redirection into `n` dissipative impulses cuts the loss as `1/n`, and then asserts the
classic one-quarter push-off result, which requires `1/n²`. The lemma is true about
the wrong scenario. **The §10 fall-margin inequality is boxed as a stability condition
and never proved**, in a module where ten propositions of lesser weight all are — and
Module 7 already proved exactly the result needed (its Prop 4.2, capturability), four
lines away by citation.

The module also fails a promise the course made on its behalf. `module03.html:1394`
and `:2036` both tell the reader that gait pushes the peak hip joint reaction to
**3–5 body weights**, and `module03.html:2151` names Module 8 as the module that will
cash it. Module 8 never computes a hip reaction, never mentions body weights, and
never returns to the claim.

Finally, two strings render as literal garbage — `a\approximated` at `:199` and
`a\approximately` at `:473` — and every figure cross-reference in §0 from Fig. 2
onward points at the wrong figure, because the stylesheet auto-numbers with
`figcaption::before` and the prose was written against a different figure order.

A graduate reader would follow the derivations and then be unable to reproduce a
single computed number in the module. Seventeen blocking defects and fifteen style
edits below; all are applied.

---

## 2. Blocking defects

### B1 — `module08.html:582-653`: the four labs report no results, and Lab 3 does no inverse dynamics

> `<p>The labs are deliberately small but scientific: each one varies a parameter and
> asks what mechanism changes.</p>`

Then four `<pre><code>` blocks and nothing else. I extracted and ran all four. They
work; their output is:

```
Lab 1  COM rise at step edge: 0.03680138885859705
       [(0.6, 0.039), (0.8, 0.069), (1.0, 0.107), (1.2, 0.155),
        (1.4, 0.21), (1.6, 0.275), (1.8, 0.348)]
Lab 2  best step length: 0.6846733668341708
Lab 3  positive ankle work proxy: 15.794698131538293   (+ DeprecationWarning)
Lab 4  delay 0.08s capture 0.206m 7/7  ...  delay 0.32s capture 0.314m 6/7
```

None of these five numbers appears in the module. This fails part 5 of the standard
(a tie to something concrete) and the brief's rule that the code blocks *are* the
ground truth: a lab whose output the text never states cannot be checked by anyone.

Worse, Lab 3 is titled **"inverse-dynamics estimate"** and contains no inverse
dynamics. It writes `ankle = 70*np.exp(...) - 15*np.exp(...)` — the torque is
asserted, not inferred — and multiplies it by an asserted `omega_a`. Prop 6.1 defines
inverse dynamics as `τ = Iθ̈ − M_ext` driven by the measured ground reaction of §3;
Lab 3 uses neither the ground reaction nor `M_ext`. The `70` N·m amplitude is a bare
empirical number with no table row, no derivation and no "assume".

**Replacement.** Rewrite §11's opening, add a result paragraph after each lab, and
replace Lab 3 with a genuine quasi-static ankle inverse dynamics driven by §3's COP
travel and a vertical ground reaction whose *scale* is fixed by impulse-momentum.

Opening (`:586`):

```html
<p>The labs are small on purpose: each one is short enough to read in a minute and
each one ends in a number this module then has to live with. All four run against the
reference gait of <a class="secref" href="#speedcost">section 7</a> &mdash; a 70&nbsp;kg
walker with $\ell=0.95$&nbsp;m, $v=1.3\ \mathrm{m\,s^{-1}}$, and the step length
$L^{\ast}=0.684$&nbsp;m that Lab&nbsp;2 computes. Every number quoted in the labs and
in the computational problems of <a class="secref" href="#problems">section 12</a> is
the printed output of one of these blocks.</p>
```

Lab 1 result (new paragraph after the Lab 1 code block):

```html
<p><b>What Lab 1 prints.</b> The COM rise at the step edge is
$\Delta h=\ell(1-\cos\alpha)=0.0368$&nbsp;m for $\alpha=16^\circ$, so the vault lifts
and drops the body by under four centimetres: $Mg\Delta h=25.3$&nbsp;J of potential
energy is traded for kinetic energy and back on every step. The Froude sweep gives
$\mathrm{Fr}=0.039,\,0.069,\,0.107,\,0.155,\,0.210,\,0.275,\,0.348$ at
$v=0.6$ to $1.8\ \mathrm{m\,s^{-1}}$. Ordinary walking therefore lives at
$\mathrm{Fr}\approx0.1$&nbsp;&mdash; an order of magnitude below the $\mathrm{Fr}=1$
ceiling of Prop&nbsp;2.2, and a factor of five below the observed walk&ndash;run
switch. The vault is nowhere near its kinematic limit; what ends walking is cost, not
the contact constraint.</p>
```

Lab 2 result:

```html
<p><b>What Lab 2 prints.</b> The minimum sits at $L^{\ast}=0.684$&nbsp;m, which at
$v=1.3\ \mathrm{m\,s^{-1}}$ is a cadence of $c^{\ast}=v/L^{\ast}=1.90$&nbsp;steps per
second, or 114&nbsp;steps per minute, and a stride period of $T=2L^{\ast}/v=1.053$&nbsp;s.
At that step length the transition term is $26.7$&nbsp;J per step and the swing term is
$22.7$&nbsp;J: the optimum is the point where the two are within 15&nbsp;% of each
other, which is what an interior optimum of two opposing power laws looks like. Move
$20$&nbsp;% either way in $L$ and total cost rises, but by less than $5$&nbsp;% &mdash;
the optimum is real and it is flat, which is why people tolerate a wide band of step
lengths without noticing.</p>
```

Lab 3 (replace heading, code block, and add the result). New code block:

```python
import numpy as np

g, M, ell, v = 9.81, 70.0, 0.95, 1.3
W, T = M*g, 1.0529                          # body weight, stride period (Lab 2)
T_st = 0.62*T                               # stance duration, 62% of the stride
s = np.linspace(0, 1, 601)                  # fraction of stance
t = s*T_st
shape = np.sin(np.pi*s)**0.40*(1 - 0.245*np.cos(4*np.pi*(s - 0.5)))
Fy = shape*(W*T/2)/np.trapezoid(shape, t)   # scale fixed by impulse-momentum
x_cop = -0.06 + 0.25*s                      # heel-to-toe COP, ankle at x = 0
tau = Fy*x_cop                              # quasi-static ankle moment
omega = 2.3*np.exp(-((s - 0.80)/0.10)**2)   # plantarflexion rate, rad/s
P = tau*omega
print('stance impulse', np.trapezoid(Fy, t), 'target', W*T/2)
print('peak ankle moment', tau.max(), 'N m =', tau.max()/M, 'N m/kg')
print('peak ankle power', P.max(), 'W =', P.max()/M, 'W/kg')
print('positive ankle work', np.trapezoid(np.maximum(P, 0), t), 'J')
```

Verified output:

```
stance impulse 361.5052 target 361.5052
peak ankle moment 95.06 N m = 1.358 N m/kg
peak ankle power 214.4 W = 3.063 W/kg
positive ankle work 22.51 J
```

Lab 3 result paragraph:

```html
<p><b>What Lab 3 prints.</b> Two of the three inputs are assumptions and the third is
derived, and the difference matters. The <em>shape</em> of the vertical ground reaction
is assumed: the two constants $0.40$ and $0.245$ are chosen so the template reproduces
the double hump that force plates measure, peaks of $1.10\,W$ at $28\,\%$ and
$72\,\%$ of stance around a trough of $0.75\,W$ at midstance. The <em>scale</em> is not
assumed: over one stride each limb must carry the body's weight impulse for half a
stride, so $\int_{\rm stance}F_y\,dt=WT/2=361.5\ \mathrm{N\,s}$, and that one equation
fixes the amplitude. The COP travel is the anatomy of
<a class="secref" href="#copwalk">section 3</a>: the pressure point starts $0.06$&nbsp;m
behind the ankle and ends $0.19$&nbsp;m ahead of it, crossing the ankle at $24\,\%$ of
stance. Multiplying gives a peak plantarflexor moment of $95.1$&nbsp;N&nbsp;m
$=1.36\ \mathrm{N\,m\,kg^{-1}}$ at $77\,\%$ of stance, a peak ankle power of
$214\ \mathrm W=3.06\ \mathrm{W\,kg^{-1}}$ at $79\,\%$, and $22.5$&nbsp;J of positive
ankle work per step. The peak power matches the A2 burst drawn in the joint-power
figure of <a class="secref" href="#powers">section 6</a> to within $1\,\%$, which is
the only cross-check this module has on that figure.</p>
```

Lab 4 result paragraph:

```html
<p><b>What Lab 4 prints.</b> With $x_{\rm com}=0.03$&nbsp;m, $\dot x_{\rm com}=0.45\
\mathrm{m\,s^{-1}}$ and $\ell=0.95$&nbsp;m, the capture point runs from $0.206$&nbsp;m
at a $0.08$&nbsp;s reaction delay to $0.314$&nbsp;m at $0.32$&nbsp;s. Against a step
reach swept from $0.28$ to $0.55$&nbsp;m, every reach recovers the perturbation up to
a $0.24$&nbsp;s delay; at $0.28$&nbsp;s the shortest reach fails, and at $0.32$&nbsp;s
it fails by $0.034$&nbsp;m. Note what the sweep does <em>not</em> show: a $0.24$&nbsp;s
increase in delay moves the capture point by only $0.108$&nbsp;m, while the same
fractional change in COM speed moves it by more. K10 quantifies that comparison; the
lesson here is that reaction delay alone is a weak predictor of who falls.</p>
```

---

### B2 — `module08.html:162`: every figure cross-reference from Fig. 2 onward points at the wrong figure

> `Visual map: Fig. 1 previews the gait cycle; Fig. 2 derives the COM vault; Fig. 3
> shows COP travel; Fig. 4 defines compass gait; Fig. 5 isolates transition loss;
> Fig. 6 shows joint power; Fig. 7 frames speed-cost optimization; Fig. 8 stacks fall
> mechanisms; Fig. 9 anchors the first problem.`

The stylesheet numbers figures automatically:
`figcaption::before{ content:"Fig. " counter(fig) ". "; }` with
`figure{ counter-increment:fig; }`. The actual order in the file is: 1 gait cycle
(`:154`), 2 stride timing (`:187`), 3 COM vault (`:251`), 4 COP (`:283`), 5 compass
gait (`:343`), 6 transition (`:399`), 7 joint power (`:432`), 8 speed-cost (`:460`),
9 arm swing (`:469`), 10 passive walker (`:494`), 11 fall stack (`:542`), 12 the C1
problem figure (`:668`).

So eight of the nine references are wrong: the COM vault is Fig. 3 not Fig. 2, the
fall stack is Fig. 11 not Fig. 8, and the first problem figure is Fig. 12 not Fig. 9.
Fails part 5 of the standard and the house rule that figures are referenced from the
prose. `check_links.py` cannot see this, because these are prose references, not
anchors.

**Replacement:**

```html
<p class="small">Visual map: Fig.&nbsp;1 previews the gait cycle and Fig.&nbsp;2 lays
its phases on a timeline; Fig.&nbsp;3 derives the COM vault; Fig.&nbsp;4 shows COP
travel; Fig.&nbsp;5 defines compass gait; Fig.&nbsp;6 isolates transition loss;
Fig.&nbsp;7 shows joint power; Fig.&nbsp;8 frames speed-cost optimization; Fig.&nbsp;9
is arm swing as momentum cancellation; Fig.&nbsp;10 is the passive walker;
Fig.&nbsp;11 stacks fall mechanisms; Fig.&nbsp;12 anchors the first problem.</p>
```

---

### B3 — `module08.html:387,391`: Prop 5.2's scaling law does not produce its own conclusion

> **Proposition 5.2 (why pre-emptive push-off is cheap).** Splitting a velocity
> redirection of total angle $\beta$ into $n$ equal sequential impulses reduces the
> collision loss from $\tfrac12 Mv^2\beta^2$ to $\tfrac12 Mv^2\beta^2/n$.

and the proof closes:

> it powers the same transition with one-quarter of the work required if the collision
> is left to dissipate and hip work repays it afterward.

The lemma is true — for `n` *dissipative* collisions, the total loss is
`n · ½Mv²(β/n)² = ½Mv²β²/n`. But push-off is not a dissipative collision. In the
push-off strategy exactly **one** impulse dissipates, of angle `β/n`, and the other
`n−1` are supplied as positive muscle work. In steady state the net mechanical work
per step equals what is dissipated, so the cost is `½Mv²sin²(β/n) ≈ ½Mv²β²/n²`. The
loss falls as **1/n², not 1/n**. Only the `1/n²` law gives the one-quarter at `n = 2`
that the proof asserts; the stated `1/n` law gives one-half, and the proof therefore
concludes something its own lemma contradicts. This fails part 3 of the standard
(a proof whose mechanism is visible) and part 1 (a precise statement).

I verified both branches numerically at the module's own reference step
(`2α = 42.22°`, `M = 70` kg, `v = 1.3` m/s, `½Mv²sin²2α = 26.72` J):

| n | one dissipative collision of `β/n` | n dissipative collisions |
|---|---|---|
| 1 | 26.716 J (ratio 1.000) | 1.000 |
| 2 | 7.675 J (ratio **0.287**) | 0.575 |
| 3 | 3.498 J (ratio 0.131) | 0.393 |
| 4 | 1.985 J (ratio 0.074) | 0.297 |

The `n = 2` ratio has a closed form: `sin²α / sin²2α = 1/(4cos²α)`, which is **0.287**
at `α = 21.11°` and tends to exactly `1/4` as `α → 0`. So the classic one-quarter is
the small-angle limit, and at a real step length push-off saves slightly less than the
textbook figure claims.

**Replacement (`:387`):**

```html
<div class="prop"><b>Proposition 5.2 (why pre-emptive push-off is cheap).</b> Let the
COM velocity of magnitude $v$ be redirected through a total angle $\beta=2\alpha$ at
the step-to-step transition. Two accountings must be kept apart.
<b>(a)</b> If the redirection is split into $n$ equal <em>inelastic collisions</em>,
the total dissipation is $n\cdot\tfrac12Mv^2\sin^2(\beta/n)\approx\tfrac12
Mv^2\beta^2/n$: the loss falls as $1/n$.
<b>(b)</b> If instead a trailing-leg <b>push-off</b> supplies $n-1$ of the $n$
redirections as positive muscle work and only the final heel strike dissipates, the
net mechanical work per step in steady state is the single remaining collision,
$$\boxed{\;E_{\rm step}=\tfrac12Mv^2\sin^2\!\frac{\beta}{n}\;\approx\;\frac{1}{n^{2}}\cdot
\tfrac12Mv^2\beta^2\;}$$ and the loss falls as $1/n^{2}$. For the half-and-half split
$n=2$ the exact ratio to the collision-only cost is $\sin^2\alpha/\sin^2
2\alpha=1/(4\cos^{2}\alpha)$, which tends to $\tfrac14$ as $\alpha\to0$.</div>
```

**Replacement (`:391`):**

```html
<div class="proof">For (a), one inelastic redirection through angle $\psi$ destroys
the velocity component normal to the new arc, $v\sin\psi$, and therefore
$\tfrac12Mv^2\sin^2\psi$ of kinetic energy (Prop&nbsp;5.1). Replacing one redirection
by $\beta$ with $n$ redirections by $\beta/n$ gives
$n\cdot\tfrac12Mv^2\sin^2(\beta/n)\approx\tfrac12Mv^2\beta^2/n$, since $\sin^2$ is
quadratic in a small angle and there are $n$ of them. For (b), the bookkeeping is
different because a push-off impulse is not a collision: it is an impulse directed
along the trailing leg that <em>adds</em> energy rather than removing it. Over a
periodic step the walker's mechanical energy must return to its starting value, so the
positive work supplied by push-off exactly equals what the one remaining heel strike
destroys, namely $\tfrac12Mv^2\sin^2(\beta/n)$. That is one term, not $n$ of them, so
the cost carries the full $1/n^{2}$ of the squared angle instead of $1/n$. Taking
$n=2$ &mdash; push-off does the first half of the redirection, the heel strike the
second &mdash; gives the classic simplest-walker result: the ratio to leaving the
collision to dissipate and repaying it with hip work is $\sin^2\alpha/\sin^2 2\alpha =
1/(4\cos^{2}\alpha)$, one quarter in the small-angle limit. At this module's own
reference step ($2\alpha=42.2^\circ$, $v=1.3\ \mathrm{m\,s^{-1}}$, $M=70$&nbsp;kg) the
collision-only cost is $26.7$&nbsp;J per step and the split cost is $7.7$&nbsp;J, a
ratio of $0.287$: the real saving is a factor of $3.5$, not the textbook $4$, because
a $42^\circ$ redirection is not a small angle. <span class="qed">&#8718;</span></div>
```

---

### B4 — `module08.html:407-433`: the peak hip joint reaction that Module 3 promised is never delivered

`module03.html:1394`:

> This is exactly the effect §4 flagged when it noted that gait pushes the peak hip
> reaction to $3$–$5\,W$

`module03.html:2036` repeats it, and `module03.html:2151` says the debt is owed to
"Module 8 (gait inverse dynamics, with measured segment inertias)". `module08.html:411`
acknowledges half of it — "cashing the promise made in Module 3 that measured segment
inertias would later drive a gait torque estimate" — and then never produces a joint
reaction force. The strings "body weight", "hip reaction" and "joint reaction" do not
occur anywhere in Module 8 except inside Prop 6.1's proof.

This fails part 4 (the limit case a claim must land in) and the brief's rule that a
scenario reused in a later module must use the same symbols and values as its first
appearance. It is also the single number a reader will come to this module for.

**Replacement.** Insert a worked subsection after the joint-power figure at `:432`,
built on Module 3's equation (4.1) with Module 3's own symbols and on this module's
§2 and §3.

```html
<h3 id="hipload">6.1 Worked number: the peak hip reaction in walking</h3>

<p>Module&nbsp;3 left this module a specific debt. Its equation (4.1) put the hip joint
reaction in static single-leg stance at $R=W_s\,(1+b/a)$, where $W_s=\tfrac56 W$ is the
body weight less the swinging leg, $b\approx0.10$&nbsp;m is the horizontal distance
from the femoral head to the supported centre of mass, and $a\approx0.05$&nbsp;m is the
hip abductor moment arm. With $W=Mg=686.7$&nbsp;N that is $R=2.5\,W=1717$&nbsp;N
standing still, and Module&nbsp;3 then asserted that walking raises the peak to
$3$&nbsp;to&nbsp;$5\,W$ and pointed here for the reason. Here is the reason.</p>

<p>The frontal-plane balance is unchanged by walking; what changes is the load it
balances. By Prop&nbsp;3.1 the vertical ground reaction is
$F_{{\rm grf},y}=M(g+\ddot y_{\rm com})$, so the supported weight $W_s$ in
Module&nbsp;3's equation is replaced by $n\,W_s$, where $n=F_{{\rm grf},y}/W$ is the
instantaneous vertical ground reaction in body weights. Two values of $n$ can be got
from this module's own results.</p>

<p><b>The midstance trough is derived.</b> Prop&nbsp;2.2 already gives it:
$N=M(g-v^2/\ell)$, so $n_{\rm mid}=1-v^2/(g\ell)=1-\mathrm{Fr}$. At
$v=1.3\ \mathrm{m\,s^{-1}}$ and $\ell=0.95$&nbsp;m, $n_{\rm mid}=0.819$, that is
$562$&nbsp;N. Vaulting <em>unloads</em> the leg at midstance, by exactly the Froude
number.</p>

<p><b>The transition peak follows from the redirection impulse.</b> At the
step-to-step transition the COM's vertical velocity reverses from $-v\sin\alpha$ to
$+v\sin\alpha$, so the two feet together must deliver a vertical impulse
$2Mv\sin\alpha$ above body weight. For the reference gait
($L^{\ast}=0.684$&nbsp;m, $\alpha=21.1^\circ$, $T=1.053$&nbsp;s, double support
$2\times0.62-1=24\,\%$ of the stride split into two periods of $0.126$&nbsp;s), that
impulse is $65.6\ \mathrm{N\,s}$ and the mean excess force is $519$&nbsp;N, so the two
feet together carry $n_{\rm ds}=1.76\,W$ during double support. The two estimates are
consistent: weighting them by their durations,
$0.76\times0.819+0.24\times1.756=1.044$, and periodicity requires the stride mean to
be exactly $1$, so the two independent routes agree to $4\,\%$. How that $1.76\,W$
splits between the trailing and leading limb is a measurement question, forwarded to
Module&nbsp;15; <em>assume</em> the leading limb's peak share is
$n_{\rm peak}=1.10$&nbsp;to&nbsp;$1.20$, the range force plates report.</p>

<div class="keyresult"><b>Peak hip joint reaction in walking.</b> Scaling
Module&nbsp;3's (4.1) by the peak vertical ground reaction,
$$R_{\rm peak}\;\approx\;n_{\rm peak}\,W_s\Big(1+\frac{b}{a}\Big)
\;=\;n_{\rm peak}\times 2.5\,W\;=\;2.75\text{ to }3.00\,W,$$ and using
Module&nbsp;3's honest resultant of $2.6$&nbsp;to&nbsp;$2.8\,W$ (which accounts for the
abductors' $30^\circ$ line of pull) in place of the vertical-only $2.5\,W$ gives
$R_{\rm peak}\approx2.9$&nbsp;to&nbsp;$3.4\,W$. Adding the frontal-plane inertia of the
accelerating swing limb, which this planar model drops, carries the peak into the
$3$&nbsp;to&nbsp;$5\,W$ band Module&nbsp;3 promised. The debt is paid, and the payment
shows where it comes from: not from walking being violent, but from the abductors
working at half the lever arm of the load they balance.</div>

<p>Two things in that chain are assumptions and are labelled as such: the lever ratio
$b/a=2$ is Module&nbsp;3's, and $n_{\rm peak}$ is a measured range this module does not
derive. Everything else &mdash; $n_{\rm mid}=1-\mathrm{Fr}$, the $65.6\ \mathrm{N\,s}$
redirection impulse, the $4\,\%$ periodicity check &mdash; follows from Props&nbsp;2.2,
3.1 and 5.1.</p>
```

---

### B5 — `module08.html:570`: the fall-margin inequality is boxed as a stability condition and never proved

> **Fall-margin inequality.** A step can recover a forward perturbation only if the
> required capture location is within feasible step reach $x_s^{\max}$:
> $x_{\rm com}+\frac{\dot x_{\rm com}}{\omega_0}\le x_s^{\max},\qquad
> \omega_0=\sqrt{g/h_{\rm com}}.$

Ten propositions in this module carry proofs. This is a boxed stability condition of
equal weight to Prop 9.1 and greater weight than Prop 1.1, and it is asserted. The
brief is explicit: "a boxed constitutive law or a stability condition does [need a
proof]". D9 asks the reader to derive it and its solution says only "the divergent
component is $x+\dot x/\omega_0$" — which is the thing to be shown, restated.

The proof is four lines, because **Module 7 already did the work.** `module07.html:341`
gives the linearized inverted pendulum's general solution
$\theta(t)=Ae^{\omega_0t}+Be^{-\omega_0t}$ with its growing mode, and
`module07.html:373-378` proves Prop 4.2 (capturability): $\xi=x_{\rm com}+\dot
x_{\rm com}/\omega_0$ obeys $\dot\xi=\omega_0(\xi-x_{\rm cop})$.

**Replacement:**

```html
<div class="prop"><b>Proposition 10.1 (fall-margin inequality).</b> Model the body
between foot contacts as the linear inverted pendulum of Module&nbsp;7 with
$\omega_0=\sqrt{g/\ell}$. A single step to a new contact point $x_p$ arrests a forward
perturbation if and only if $x_p$ is at least the extrapolated centre of mass,
$$\boxed{\;x_{\rm com}+\frac{\dot x_{\rm com}}{\omega_0}\;\le\;x_p\;\le\;x_s^{\max}\;}$$
where $x_s^{\max}$ is the farthest contact the walker can actually reach. A
perturbation is therefore unrecoverable in one step exactly when the extrapolated COM
exceeds the feasible step reach.</div>

<div class="proof">Take the new contact as the origin. Module&nbsp;7's linearised
inverted pendulum gives $\ddot x_{\rm com}=\omega_0^2\,x_{\rm com}$, whose general
solution is $x_{\rm com}(t)=Ae^{\omega_0t}+Be^{-\omega_0t}$ with
$A=\tfrac12\big(x_{\rm com}(0)+\dot x_{\rm com}(0)/\omega_0\big)$ and
$B=\tfrac12\big(x_{\rm com}(0)-\dot x_{\rm com}(0)/\omega_0\big)$. The second term
decays; the first grows without bound. The motion stays bounded &mdash; the body rocks
up over the new foot and settles instead of toppling past it &mdash; if and only if the
coefficient of the growing mode is not positive, that is $x_{\rm com}(0)+\dot
x_{\rm com}(0)/\omega_0\le0$ measured from the contact point. Restoring the original
origin, the contact must satisfy $x_p\ge x_{\rm com}+\dot x_{\rm com}/\omega_0$. The
quantity $\xi=x_{\rm com}+\dot x_{\rm com}/\omega_0$ is Module&nbsp;7's extrapolated
centre of mass, and Module&nbsp;7's Prop&nbsp;4.2 shows it obeys the first-order law
$\dot\xi=\omega_0(\xi-x_{\rm cop})$: place the pressure point beyond $\xi$ and $\xi$
falls back, place it short and $\xi$ runs away. A step can only place the pressure
point where the foot can go, so the step succeeds if and only if $\xi\le x_s^{\max}$.
<span class="qed">&#8718;</span></div>

<p>Aging attacks both sides of that one inequality, and the model says which attack is
worse. It raises the left side through reaction delay: during a delay $\Delta$ the COM
drifts a further $\dot x_{\rm com}\Delta$ before the foot moves, so the capture
requirement becomes $x_{\rm com}+\dot x_{\rm com}\Delta+\dot x_{\rm com}/\omega_0$. It
lowers the right side through hip range, ankle strength and the confidence to commit to
a long step. For the reference older-adult perturbation of Lab&nbsp;4
($x_{\rm com}=0.03$&nbsp;m, $\dot x_{\rm com}=0.45\ \mathrm{m\,s^{-1}}$,
$\Delta=0.20$&nbsp;s, $\ell=0.95$&nbsp;m, so $\omega_0=3.21\ \mathrm{s^{-1}}$), the
capture point sits at $0.260$&nbsp;m and a typical reachable step of $0.415$&nbsp;m
leaves a margin of $0.155$&nbsp;m. K10 computes which of the three variables spends
that margin fastest.</p>
```

---

### B6 — `module08.html:452,460`: §7's cost proxy has no coefficients, the figure uses a different model, and its marker line is invisible

> $$C(v,L)=A\,v^2\sin^2\!\left(2\arcsin\frac{L}{2\ell}\right)+B\left(\frac{v}{L}\right)^2+C_0,$$

`A`, `B` and `C₀` are never given a value, a unit, or a table row. The figure at `:460`
then uses a *different* model entirely —
`CoT(v)=c₁/v+c₂v` with `v*=√(c₁/c₂)≈1.3 m/s` — whose `c₁` and `c₂` are also never
given, and which collides visually with the cadence symbol `c` defined in §1. Under
the brief's three-class rule the "≈1.3 m/s" is a bare number: not derived (the
coefficients are unknown), not a table parameter, not labelled an assumption.

There is also a rendering defect I found by reading the SVG: the dashed marker for
`v*` is `<line x1="320" y1="210" x2="320" y2="210" .../>` — **zero length**. The label
"preferred v* ≈ 1.3 m/s" floats with no line under it. I decoded the polyline against
the axis ticks (x = 105 → 0.5, 239 → 1.0, 373 → 1.5, 506 → 2.0 m/s) and the curve's
true minimum is at **v = 1.278 m/s**, so the drawn marker at x = 320 (v = 1.302) is
right to within 2 %; only the line is missing.

**Replacements.** §7 body (`:448-456`) gets concrete, calibrated coefficients tied to
Lab 2:

```html
<p>A minimal cost proxy can be written as</p>

$$C(v,L)=\tfrac12 M\,v^2\sin^2\!\left(2\arcsin\frac{L}{2\ell}\right)+b\,M\left(\frac{v}{L}\right)^2+C_0,$$

<p>where the first term is exactly the step-to-step transition cost of Prop&nbsp;5.1,
the second penalises high cadence $c=v/L$, and $C_0$ is a speed-independent baseline
that does not move the optimum and is dropped from here on. The single free constant is
$b$, the swing-cost coefficient, with units of area: <em>assume</em>
$b=0.09\ \mathrm{m^2}$, so that $bM=6.3\ \mathrm{kg\,m^2}$ is an effective swing
inertia. That one assumption is what Lab&nbsp;2 varies and what
<a class="secref" href="#problems">K7</a> tests. With it, and with $M=70$&nbsp;kg,
$\ell=0.95$&nbsp;m and $v=1.3\ \mathrm{m\,s^{-1}}$, the proxy has an interior minimum at
$L^{\ast}=0.684$&nbsp;m, cadence $c^{\ast}=1.90$&nbsp;steps&nbsp;s$^{-1}$
(114&nbsp;steps per minute) &mdash; within a few percent of what people actually choose.
This proxy is not a metabolic model. Its purpose is to make the optimum unavoidable:
one cannot minimise transition cost and cadence cost at the same step length, because
the first rises with $L$ and the second falls with it.</p>
```

Figure caption (`:460`) gets its coefficients and its units:

```html
<figcaption>Preferred speed is a computed compromise, not a magic number. Writing the
cost of transport as $\mathrm{CoT}(v)=c_1/v+c_2v$ in
$\mathrm{J\,kg^{-1}\,m^{-1}}$, the minimum sits at $v^{\ast}=\sqrt{c_1/c_2}$ with
$\mathrm{CoT}^{\ast}=2\sqrt{c_1c_2}$. Fixing the two coefficients from two assumed
observations, a preferred speed of $v^{\ast}=1.3\ \mathrm{m\,s^{-1}}$ and a minimum net
cost of transport of $\mathrm{CoT}^{\ast}=2.2\ \mathrm{J\,kg^{-1}\,m^{-1}}$, gives
$c_1=v^{\ast}\mathrm{CoT}^{\ast}/2=1.43\ \mathrm{J\,kg^{-1}\,s^{-1}}$ and
$c_2=\mathrm{CoT}^{\ast}/(2v^{\ast})=0.85\ \mathrm{J\,s\,kg^{-1}\,m^{-2}}$. Too slow
and the per-distance support/time term $c_1/v$ dominates; too fast and the
transition/swing term $c_2v$ does. Both coefficients are calibration, not derivation;
Module&nbsp;15 supplies the measurement.</figcaption>
```

And the invisible marker is drawn from the curve to the axis:

```
<line x1="320" y1="182" x2="320" y2="210" stroke="#2a7d2a" stroke-width="1.6" stroke-dasharray="6 4"/>
```

---

### B7 — `module08.html:772,788`: K3 and K7 quote a step-length optimum that the module's own code contradicts

> K3 … the grid minimum at $v=1.3$ m/s sits near $L^{*}\approx0.6$ m
> K7 … The minimum lands near $L^{*}\approx0.6$ m (cadence $c\approx2.2$ steps/s at $v=1.3$ m/s)

Lab 2, run: **`best step length: 0.6846733668341708`**. I re-ran the same cost function
on a 70 001-point grid at both v = 1.30 and v = 1.35 m/s: `L* = 0.6844 m` in both
cases, cadence `c* = 1.90 steps/s`, not 2.2. K3 and K7 are 14 % low in `L*` and 16 %
high in `c*`, and as written they are unanswerable anyway because §7's `A` and `B` had
no values (B6). Fails the brief's rule that a mismatch between the code and the prose
is a factual error.

**Replacements.** K3 solution:

```html
Evaluate the section-7 proxy on a grid of feasible $L$ at fixed $v$, or solve
$dC/dL=0$ numerically. With $M=70$&nbsp;kg, $\ell=0.95$&nbsp;m,
$b=0.09\ \mathrm{m^2}$ and $v=1.3\ \mathrm{m\,s^{-1}}$, the grid minimum is at
$L^{\ast}=0.684$&nbsp;m, where the transition term is $26.7$&nbsp;J and the cadence
term $22.7$&nbsp;J. The corresponding cadence is $c^{\ast}=v/L^{\ast}=1.90$&nbsp;steps
per second, or $114$&nbsp;steps per minute. Too-long steps raise transition loss as
$\sin^2 2\alpha$; too-short steps raise cadence cost as $1/L^2$. The optimum is flat:
moving $L$ by $\pm20\,\%$ raises total cost by under $5\,\%$, which is why a walker can
change step length noticeably without feeling the penalty.
```

K7 solution:

```html
Constrain $cL=v$ and evaluate the proxy over feasible $L$; the constraint removes one
of the two variables, so the redundancy in $(L,c)$ is not a free choice. At
$v=1.3\ \mathrm{m\,s^{-1}}$ the minimum lands at $L^{\ast}=0.684$&nbsp;m and
$c^{\ast}=1.90$&nbsp;steps&nbsp;s$^{-1}$ ($114$&nbsp;steps per minute). The redundancy
is broken because the two costs scale oppositely in $L$: transition cost rises as
$\sin^2(2\arcsin(L/2\ell))$ and cadence cost falls as $1/L^2$. Repeat the sweep at
$v=1.0$ and $1.6\ \mathrm{m\,s^{-1}}$ and $L^{\ast}$ barely moves, because $v$ enters
both terms as $v^2$ and cancels out of $dC/dL=0$ &mdash; the model predicts that
preferred step length is set by leg length and the swing coefficient, not by speed,
which is why cadence carries most of the speed change.
```

---

### B8 — `module08.html:800`: K10's third sensitivity number is not reproducible under any definition

> Numerically the margin's elasticity is $\approx0.88$ to speed versus $\approx0.35$ to
> reaction delay and $\approx0.30$ to step reach

The first two numbers are elasticities of the **capture point**
`C = x + vΔ + v/ω₀`, and they check exactly: `0.885` and `0.346`. But step reach does
not appear in `C` at all, so its elasticity there is **exactly 0**, not 0.30. If the
quantity meant is the **margin** `m = x_s^max − C`, then all three change: the
elasticities become `−1.484`, `−0.581` and `+2.678`. There is no reading under which
0.30 is right, and the solution calls the quantity "the margin" while quoting
capture-point numbers.

Verified at the Lab 4 reference point (`x = 0.03 m`, `v = 0.45 m/s`, `Δ = 0.20 s`,
`ℓ = 0.95 m`, `ω₀ = 3.2135 s⁻¹`, `x_s^max = 0.415 m`, capture `0.2600 m`, margin
`0.1550 m`).

**Replacement (K10 solution):**

```html
Write the margin as $m=x_s^{\max}-\big(x_{\rm com}+\dot x_{\rm com}\Delta+\dot
x_{\rm com}/\omega_0\big)$ and compute the elasticity $\partial\ln m/\partial\ln(\cdot)$
of each variable at the Lab&nbsp;4 reference point ($x_{\rm com}=0.03$&nbsp;m,
$\dot x_{\rm com}=0.45\ \mathrm{m\,s^{-1}}$, $\Delta=0.20$&nbsp;s,
$\omega_0=3.21\ \mathrm{s^{-1}}$, $x_s^{\max}=0.415$&nbsp;m), where the capture point
is $0.260$&nbsp;m and the margin is $0.155$&nbsp;m. The elasticities are
$-1.48$ to COM speed, $-0.58$ to reaction delay, and $+2.68$ to step reach. Two
readings follow. First, speed beats delay by a factor of $2.6$, because speed enters
the capture point twice &mdash; once through the reaction drift $\dot x_{\rm com}\Delta$
and once through the divergent term $\dot x_{\rm com}/\omega_0$ &mdash; while delay
enters only once. Second, and against intuition, the largest single elasticity belongs
to step reach: a ten percent loss of reach costs more margin than a ten percent
increase in delay. That is why hip range and the confidence to take a long recovery
step matter as much as reflex speed, and why the elasticities are the interesting
output here and not the raw capture distance. Note also that the elasticities of the
<em>capture point</em> are different numbers ($+0.88$ to speed, $+0.35$ to delay, and
exactly $0$ to step reach, which does not appear in it) &mdash; naming which quantity
is differentiated is half the problem.
```

---

### B9 — `module08.html:219,570` and `:596,613,644`: `ω₀` has two definitions and `ℓ` has two values

`:219` defines $\omega_0=\sqrt{g/\ell}$ with `ℓ` the leg length. `:570` defines
$\omega_0=\sqrt{g/h_{\rm com}}$ with a symbol `h_com` that appears nowhere else, is not
in the notation table, and is never given a value in the text; Lab 4 sets `h = 0.95`.
The Appendix lists `ω₀` with first use "section 10", though it is introduced in §2.
Two symbols for one quantity, and one symbol with two definitions — a defect under the
brief's notation rule, and the kind of collision the course has already had to fix
once for W, k, g and E.

`ℓ` is worse: §2 (`:243`) and §9 (`:522`) use `ℓ ≈ 0.9 m`, while Labs 1, 2 and 4 and
problems K1 and K2 use `0.95 m`. The Appendix parameter table gives only a range,
"0.8–1.1 m", and no reference value. The two are not interchangeable: at ℓ = 0.9 the
walk–run speed is 2.10 m/s and at 0.95 it is 2.16 m/s, and §2 rounds its own arithmetic
down to "≈2.0".

Note that Module 7's `ℓ = 0.9 m` is a *different* distance — COM height above the
**ankle** in quiet standing — while this module measures from the **ground contact
point**, about 0.06 m lower. That difference is the reason the two modules should carry
different values, and the module never says so.

**Resolution.** One symbol `ℓ`, one value 0.95 m, one definition
$\omega_0=\sqrt{g/\ell}$, with the Module 7 relationship stated. `h_com` is deleted.

`:219` replacement:

```html
<p>If no work is done, the mechanical energy $E=\frac12 Mv^2+Mgy$ is nearly conserved
across the middle of stance. The body slows as it rises and speeds up as it falls. This
is the pendular exchange that makes walking economical, and, exactly as in
Module&nbsp;7, the natural rate of the leg-length pendulum is
$\omega_0=\sqrt{g/\ell}$. One caution about $\ell$, because it is the same symbol
Module&nbsp;7 used for a slightly different distance: there it was the COM height above
the <em>ankle</em> in quiet standing, $0.9$&nbsp;m; here the pivot is the
<em>ground contact point</em>, roughly $0.06$&nbsp;m lower, so the reference value used
throughout this module is $\ell=0.95$&nbsp;m and
$\omega_0=\sqrt{g/\ell}=3.21\ \mathrm{s^{-1}}$, against Module&nbsp;7's
$3.1\ \mathrm{s^{-1}}$. The two agree; they are measured from different points.</p>
```

`:243` replacement (last sentence): use `ℓ = 0.95 m`, giving `v = 2.16 m/s`.

```html
Humans switch earlier, near $\mathrm{Fr}\approx\tfrac12$: with $\ell=0.95$&nbsp;m this
is $v=\sqrt{0.5\,g\ell}=2.16\ \mathrm{m\,s^{-1}}$, where the growing push-off and swing
costs overtake the pendular saving. <span class="qed">&#8718;</span></div>
```

`:522` replacement (last part): use `ℓ = 0.95 m`, giving `v = 1.25 m/s`.

```html
For $\ell=0.95$&nbsp;m, a step half-angle $\alpha\approx0.3$&nbsp;rad and a gentle slope
$\gamma\approx0.05$&nbsp;rad ($2.9^\circ$), this gives $v\approx1.25\
\mathrm{m\,s^{-1}}$ &mdash; a realistic walking speed from gravity alone. (The
small-angle step is doing real work at $2\alpha=34^\circ$; K9 solves the same balance
exactly and gets $1.31\ \mathrm{m\,s^{-1}}$, $5\,\%$ higher.)
```

---

### B10 — `module08.html:776`: K4's answer is the small-angle limit of a question posed exactly

> Cutting the redirection angle to $0.75\times$ multiplies the loss by $0.75^2=0.56$, a
> $44\%$ reduction

The loss is `½Mv²sin²(angle)`, and the solution's own first sentence says so ("Apply
the loss $\propto\sin^2$"). Squaring 0.75 is the small-angle approximation, not the
answer. At this module's reference step (`2α = 42.22°`) the exact ratio is
`sin²(0.75·2α)/sin²(2α) = 0.6103`, a **39.0 %** reduction, not 44 %.

**Replacement (whole problem, deepened per the K-standard — see B11):** given below.

---

### B11 — `module08.html:764-796`: five K problems are arithmetic substitution and one prints no number

`CLAUDE.md` and the brief are explicit: "a plug-the-numbers-into-the-box problem is
busywork at this level and is a defect." Measured against that:

- **K1** evaluates `Δh = ℓ(1−cosα)` at three angles.
- **K2** evaluates `Fr = v²/(gℓ)` at three leg lengths.
- **K4** squares 0.75.
- **K8** squares 0.7 — and the 30 % it squares is itself asserted with no model.
- **K9** iterates `z→az+b` for an `a` and `b` with no connection to the module.
- **K6** contains no number at all: its whole solution is "Second derivatives amplify
  noise, so unfiltered kinematics produce large torque artifacts."

None of these requires numerical integration, optimization, an inverse problem, a
sensitivity sweep, or a regime comparison. All six are rewritten below; each ends in a
number I printed.

**K1 — regime comparison; surfaces the vault's real failure.**

```html
<p><b>K1.</b> Integrate the rigid-vault stance arc for $\ell=0.95$&nbsp;m and
$\alpha=12^\circ,16^\circ,20^\circ$ at a midstance speed of $1.3\ \mathrm{m\,s^{-1}}$,
using energy conservation $v(\theta)^2=v_{\rm mid}^2+2g\ell(1-\cos\theta)$ and the
radial force balance to get the <em>vertical</em> ground reaction
$F_y(\theta)=M\cos\theta\,\big(g\cos\theta-v(\theta)^2/\ell\big)$. Plot $F_y$ across
stance. Compare its shape with the double-humped force-plate record that Lab&nbsp;3
assumes. Which one is the model wrong about, and by how much?
<span class="probes">Probes: a model's most visible failure, not its successes.</span></p>
<details class="sol"><summary>Solution</summary>
<p>The rigid vault predicts a <em>single hump</em> with its maximum at midstance and its
minima at the step edges &mdash; the exact inverse of what is measured. Numerically, at
all three angles $F_y$ peaks at $\theta=0$ with $F_y/W=1-\mathrm{Fr}=0.819$, and falls
to $0.737$, $0.675$ and $0.599\,W$ at $\alpha=12^\circ,16^\circ,20^\circ$. Real walking
peaks at about $1.10\,W$ at $28\,\%$ and $72\,\%$ of stance and troughs at $0.75\,W$ at
midstance. The model gets the midstance value nearly right ($0.819$ against $0.75$) and
the peaks qualitatively backwards, and it never exceeds body weight at all.</p>
<p>The reason is in the two factors. Energy conservation makes the COM <em>fastest</em>
at the step edges, so the centripetal term $v^2/\ell$ is largest there and unloads the
leg most; and the $\cos\theta$ projection removes more of an already smaller radial
force. A rigid leg simply has no way to push harder at the edges. The measured peaks
come from the two things the rigid vault deletes: the leading limb's collision at heel
strike and the trailing limb's push-off, which are precisely the step-to-step
transition of <a class="secref" href="#transition">section 5</a>. So the vault's
vertical-force error is not a detail to patch; it is the transition, showing up as the
part of the force record the model cannot draw.</p>
<p>Sweeping $v_{\rm mid}$ upward, the minimum of $F_y$ falls but stays positive:
$+0.576\,W$ at $1.3$, $+0.345\,W$ at $2.0$, $+0.278\,W$ at the
$2.16\ \mathrm{m\,s^{-1}}$ walk&ndash;run speed, and $+0.119\,W$ at
$2.5\ \mathrm{m\,s^{-1}}$. Prop&nbsp;2.2's $\mathrm{Fr}\le1$ constraint binds at
midstance, but on this arc the <em>edges</em> approach zero first, so a real walker
loses ground contact at the step edges before it does at midstance.</p></details>
```

**K2 — inverse problem.**

```html
<p><b>K2.</b> Sweep walking speed from $0.6$ to $2.0\ \mathrm{m\,s^{-1}}$ and compute
$\mathrm{Fr}$ for leg lengths $0.8$, $0.95$ and $1.1$&nbsp;m. Then invert the
relationship: a gait laboratory measures a walk&ndash;run transition speed of
$2.1\ \mathrm{m\,s^{-1}}$ for one subject and $1.9\ \mathrm{m\,s^{-1}}$ for another,
and reports no anthropometry. Recover each subject's effective pendulum length, and say
what assumption you had to make to do it and how much the answer moves if that
assumption is wrong by $\pm0.1$ in $\mathrm{Fr}$.
<span class="probes">Probes: dynamic similarity read backwards, as a measurement.</span></p>
<details class="sol"><summary>Solution</summary>
<p>Forward: at $v=1.3\ \mathrm{m\,s^{-1}}$, $\mathrm{Fr}=0.215,\,0.181,\,0.157$ for
$\ell=0.8,\,0.95,\,1.1$&nbsp;m, and the speeds at which each reaches
$\mathrm{Fr}=0.5$ are $1.98$, $2.16$ and $2.32\ \mathrm{m\,s^{-1}}$. The short-legged
walker sits at a higher Froude number for the same absolute speed and therefore reaches
the walk&ndash;run range sooner &mdash; which is why children run at speeds adults
walk.</p>
<p>Backward: assuming the transition happens at a fixed $\mathrm{Fr}^{\ast}=0.5$,
$\ell=v_{\rm tr}^2/(\mathrm{Fr}^{\ast}g)$, giving $\ell=0.899$&nbsp;m for the
$2.1\ \mathrm{m\,s^{-1}}$ subject and $0.736$&nbsp;m for the
$1.9\ \mathrm{m\,s^{-1}}$ subject. The assumption is that $\mathrm{Fr}^{\ast}$ is a
constant of the gait rather than of the person, which is exactly what dynamic
similarity claims and exactly what the measurement was supposed to test &mdash; the
inversion is only as good as that circularity allows. Sensitivity: since
$\ell\propto1/\mathrm{Fr}^{\ast}$, an error of $\pm0.1$ in $\mathrm{Fr}^{\ast}$ moves
$\ell$ by $-17\,\%/+25\,\%$, so the recovered leg length for the first subject spans
$0.75$ to $1.12$&nbsp;m. That band is wider than the difference between the two
subjects, which is the real lesson: Froude scaling predicts <em>how</em> gaits map onto
each other, but it is a poor instrument for recovering a length from a single
speed.</p></details>
```

**K4 — optimization; verifies the corrected Prop 5.2.**

```html
<p><b>K4.</b> Sweep the fraction $f\in[0,1]$ of the step-to-step redirection that the
trailing-leg push-off performs before the leading heel strikes, with the heel strike
destroying the remaining angle $(1-f)\,2\alpha$. Compute the per-step energy the walker
must supply for the reference gait ($M=70$&nbsp;kg, $v=1.3\ \mathrm{m\,s^{-1}}$,
$2\alpha=42.22^\circ$). Verify Prop&nbsp;5.2's $1/n^2$ law against the exact
$\sin^2$ result, and say by how much the small-angle "one quarter" overstates the real
saving.
<span class="probes">Probes: the difference between a scaling law and its small-angle limit.</span></p>
<details class="sol"><summary>Solution</summary>
<p>In steady state the supplied energy equals the dissipated energy, so the cost is
$\tfrac12Mv^2\sin^2\!\big((1-f)2\alpha\big)$. The collision-only baseline ($f=0$) is
$26.72$&nbsp;J per step. Sweeping $f$: $16.30$&nbsp;J at $f=0.25$, $7.68$&nbsp;J at
$f=0.5$, $1.99$&nbsp;J at $f=0.75$, and zero at $f=1$. The cost falls monotonically, so
the mechanical model alone says "push off as much as possible"; what stops a real
walker at roughly half is that the push-off impulse must be produced by the ankle
plantarflexors within the $0.126$&nbsp;s of double support, and Lab&nbsp;3's peak of
$214$&nbsp;W is close to what that muscle group can deliver.</p>
<p>Equivalently in Prop&nbsp;5.2's $n=1/(1-f)$ form, the exact ratios to the baseline
are $1.000,\,0.287,\,0.131,\,0.074$ for $n=1,2,3,4$, against the small-angle
$1/n^2=1.000,\,0.250,\,0.111,\,0.063$. At $n=2$ the closed form is
$1/(4\cos^2\alpha)=0.287$: the textbook "one quarter" is the $\alpha\to0$ limit and it
<em>overstates</em> the saving by $15\,\%$ at a real $21^\circ$ half-angle. A
$25\,\%$ cut in the redirection angle ($f=0.25$) reduces the loss by $39.0\,\%$
exactly, not the $43.8\,\%$ that $0.75^2$ predicts.</p></details>
```

**K6 — sensitivity sweep with a printed number.**

```html
<p><b>K6.</b> Take a joint angle $\theta(t)=0.35\sin(2\pi t)$&nbsp;rad over one second,
add independent Gaussian noise of standard deviation $2$&nbsp;mrad (a realistic
marker-based estimate), finite-difference twice, and convert to a torque error with a
shank-plus-foot moment of inertia $I=0.035\ \mathrm{kg\,m^2}$ via Prop&nbsp;6.1. Sweep
the sample rate over $60$, $120$ and $240$&nbsp;Hz. Which direction does the error
move, and why is that the opposite of what more data usually buys?
<span class="probes">Probes: why a faster camera makes inverse dynamics worse.</span></p>
<details class="sol"><summary>Solution</summary>
<p>The RMS torque error is $0.136$, $0.642$ and $2.704$&nbsp;N&nbsp;m at $60$, $120$ and
$240$&nbsp;Hz. It grows by a factor of about four for each doubling of the sample rate,
because a central second difference divides by $\Delta t^2$: uncorrelated noise of
standard deviation $\sigma$ becomes an acceleration error of order
$\sigma/\Delta t^{2}$, which scales as $f_s^{2}$. Sampling faster adds no information
about a $1$&nbsp;Hz joint motion and multiplies the noise gain, so the naive pipeline
gets monotonically worse with better hardware.</p>
<p>Set against the $95$&nbsp;N&nbsp;m peak ankle moment of Lab&nbsp;3, even the
$240$&nbsp;Hz error is under $3\,\%$ at this noise level &mdash; but the scaling is the
point, not the size: raise the marker noise to $10$&nbsp;mrad and the $240$&nbsp;Hz
error passes $13$&nbsp;N&nbsp;m. The fix is not a slower camera but a low-pass filter
chosen from the signal bandwidth before differentiating, which is why every real
inverse-dynamics pipeline filters first. Module&nbsp;15 builds that pipeline and its
uncertainty budget.</p></details>
```

**K8 — builds the angular-momentum model instead of assuming its output.**

```html
<p><b>K8.</b> Build the yaw angular momentum of a walking body from segments instead of
assuming a percentage. Treat each leg as a point mass $m_{\rm leg}=0.161M$ at a
mediolateral offset $d_{\rm leg}=0.09$&nbsp;m from the body's vertical axis, moving
fore-aft at $\pm1.3\ \mathrm{m\,s^{-1}}$ relative to the trunk, and each arm as
$m_{\rm arm}=0.050M$ at $d_{\rm arm}=0.20$&nbsp;m moving at
$\mp0.6\ \mathrm{m\,s^{-1}}$. Compute the peak vertical-axis angular momentum with and
without arm swing, and the mean trunk yaw torque each requires over a half stride.
Then say what fraction of the legs' momentum the arms actually cancel, and compare it
with the $30\,\%$ this problem used to assume.
<span class="probes">Probes: deriving a cancellation fraction rather than asserting one.</span></p>
<details class="sol"><summary>Solution</summary>
<p>About the vertical axis, a segment at mediolateral offset $y$ moving fore-aft at
$v_x$ contributes $L_z=-m\,y\,v_x$. The two legs are antiphase <em>and</em> on opposite
sides, so their contributions have the <em>same</em> sign and add:
$|L_{\rm legs}|=2m_{\rm leg}d_{\rm leg}u_{\rm leg}=2(11.27)(0.09)(1.3)=2.637\
\mathrm{kg\,m^2\,s^{-1}}$. Each arm swings opposite its ipsilateral leg, so the arms
subtract: $|L_{\rm arms}|=2(3.50)(0.20)(0.60)=0.840\ \mathrm{kg\,m^2\,s^{-1}}$. The
arms cancel $0.840/2.637=31.9\,\%$ of the legs' yaw momentum, leaving a residual of
$1.797\ \mathrm{kg\,m^2\,s^{-1}}$.</p>
<p>That residual has to reverse sign twice per stride, so over a half stride
($T/2=0.526$&nbsp;s) the trunk must supply a mean yaw torque
$\tau=2|L|/(T/2)$: $10.0$&nbsp;N&nbsp;m with the arms held still, $6.8$&nbsp;N&nbsp;m
with them swinging. If the stabilisation cost is quadratic in torque, arm swing cuts it
by $1-0.68^2=54\,\%$. So the $30\,\%$ figure this problem previously assumed is close
to right &mdash; but it is now a <em>result</em> of segment masses and offsets, and the
model says why: the arms are light (5&nbsp;% of body mass each against 16&nbsp;% for a
leg) but they work at more than twice the moment arm and that is what makes the trade
nearly even.</p></details>
```

**K9 — derives the stride map from Prop 9.1 instead of inventing one.**

```html
<p><b>K9.</b> Derive the passive walker's stride map from Prop&nbsp;9.1 rather than
assuming one. Let $E_n=\tfrac12Mv_n^2$ be the kinetic energy just <em>before</em> heel
strike $n$. Gravity adds $MgL\sin\gamma$ over a step and the collision multiplies the
energy by $\cos^2 2\alpha$, so $E_{n+1}=aE_n+b$ with $a=\cos^2 2\alpha$ and
$b=MgL\sin\gamma$. Identify $a$ and $b$ for $\ell=0.95$&nbsp;m, $\alpha=0.30$&nbsp;rad,
$\gamma=0.05$&nbsp;rad, $M=70$&nbsp;kg, find the fixed point, iterate from a walker
released too slowly, and compare the exact fixed-point speed with Prop&nbsp;9.1's
small-angle estimate.
<span class="probes">Probes: a limit cycle as a fixed point of a map you derived.</span></p>
<details class="sol"><summary>Solution</summary>
<p>With $L=2\ell\sin\alpha=0.5615$&nbsp;m, $a=\cos^2(0.6)=0.6812$ and
$b=MgL\sin\gamma=19.27$&nbsp;J. The fixed point is $E^{\ast}=b/(1-a)=60.44$&nbsp;J, so
$v^{\ast}=\sqrt{2E^{\ast}/M}=1.314\ \mathrm{m\,s^{-1}}$. Stability needs $|a|\lt1$, and
$a=\cos^2 2\alpha$ is <em>always</em> less than one for any non-zero step angle: the
passive gait is locally stable in energy for every slope and every step length, with
perturbations decaying by a factor $0.68$ per step, an e-folding in $2.60$ steps.
Released from $E_0=5$&nbsp;J the walker reaches $57.9$&nbsp;J after eight steps, within
$4\,\%$ of the limit cycle &mdash; a walker set down too slowly speeds itself up, which
is what makes passive walkers robust enough to build.</p>
<p>Prop&nbsp;9.1's small-angle formula $v=\sqrt{g\ell\sin\gamma/\alpha}$ gives
$1.246\ \mathrm{m\,s^{-1}}$, $5.2\,\%$ below the exact $1.314$. The error is entirely
the two small-angle steps in that proof ($L\approx2\ell\alpha$ and
$\sin2\alpha\approx2\alpha$) at $2\alpha=34.4^\circ$, which is not small. Note what this
one-dimensional map does <em>not</em> capture: it tracks energy only, so it cannot see
the swing-leg state, and $|a|\lt1$ here does not prove the full two-state Jacobian
$D\mathcal P$ of <a class="secref" href="#passive">section 9</a> has both eigenvalues
inside the unit circle. Passive walkers do fall over; energy stability is necessary,
not sufficient.</p></details>
```

**K5** is retargeted onto the rewritten Lab 3 so the module has one ankle model, not two:

```html
<p><b>K5.</b> Using Lab&nbsp;3's quasi-static ankle moment and plantarflexion rate,
integrate the positive ankle work over stance. Then compare it with the step-to-step
transition loss that <a class="secref" href="#transition">section 5</a> computes for the
same reference gait. What fraction of the transition does the ankle repay, and what has
to supply the rest?
<span class="probes">Probes: closing the energy books on one step.</span></p>
<details class="sol"><summary>Solution</summary>
<p>Compute $P(t)=\tau(t)\dot\theta(t)$ and integrate only $P^{+}$ by the trapezoid rule
over stance. Lab&nbsp;3 gives $\int P^{+}dt=22.5$&nbsp;J of positive ankle work per
step, peaking at $214\ \mathrm W$ ($3.06\ \mathrm{W\,kg^{-1}}$) at $79\,\%$ of stance.
The collision-only transition loss for the same gait is
$\tfrac12Mv^2\sin^2 2\alpha=26.7$&nbsp;J, so the ankle burst repays $84\,\%$ of it. The
remainder is hip work in early stance and the small residual the corrected
Prop&nbsp;5.2 leaves when push-off and collision split the redirection unevenly. The
number to keep is the ratio, not either energy alone: one joint, acting for about a
tenth of a second, covers most of the entire mechanical cost of walking.</p></details>
```

---

### B12 — `module08.html:199,473`: two strings render as literal backslash text

> `the stance leg is often well a\approximated as a nearly rigid link`
> `arm and leg angular momenta must a\approximately cancel within the body`

Both sit outside `$…$`, so MathJax does not touch them and the reader sees
`a\approximated` and `a\approximately` on the page. `checktex.py` passes them (they are
not inside math and contain no stray control character) and `verify_dom.py` passes them
(no `mjx-merror`). Fix: `well approximated`, `must approximately cancel`.

---

### B13 — `module08.html:680`: C4 has no caption

Of the module's 41 `<figure>` elements, 40 carry a `<figcaption>`. C4's does not — it is
the only problem figure with no caption, which is also why `check_probfig.py` flags it
as "neither a drawn entity nor a labelled plot". Every other problem figure carries a
"CN figure." caption. Fails the house rule that every figure is captioned to stand
alone; and because `figcaption::before` supplies the auto-number, the reader sees a
figure with no number at all.

**Replacement** (append before `</figure>`):

```html
<figcaption>C4 figure. The COP is the pressure-weighted mean of the contact pressure
under the foot: it starts at the heel, crosses the ankle at about a quarter of stance,
and ends under the toes.</figcaption>
```

---

### B14 — `module08.html:832,836`: the Appendix omits most of the module's symbols and gives no reference values

The notation table lists 13 entries. The module uses, and the table omits:
`M`, `g`, `W`, `y`, `\Delta h`, `N`, `\mathbf r_{\rm com}`, `I`, `M_{\rm ext}`,
`E_{\rm loss}`, `\beta`, `n`, `u`, `\gamma`, `\mathcal P`, `\mathbf z_n`,
`\mathbf L_G`, `x_s^{\max}`, `\omega_0` (listed with the wrong first use), and the
cost-proxy constants. The brief's rule: "every symbol in the text appears there."

The parameter table is worse. It gives a *range* for `ℓ` and no reference value; no `g`;
no `α`; no `γ`; no stance fraction (though the §1 figure caption asserts "about 62 %");
no swing coefficient `b`; no foot geometry; and for "Older-adult reaction delay" it
gives "task dependent, often increased", which is not a parameter value at all while
Lab 4 sweeps 0.08–0.32 s and K10 uses 0.20 s. Under the brief's three-class rule every
one of those is a bare number.

**Replacement.** Notation table gains 15 rows; parameter table is rebuilt with values,
symbols, units and a class column (derived / parameter / assumed). Full HTML is in
`apply.py` tags `B14a` and `B14b`; the parameter table becomes:

| Parameter | Symbol | Value | Class | Where |
|---|---|---|---|---|
| Body mass | `M` | 70 kg | parameter (Module 1) | §3 |
| Gravity | `g` | 9.81 m s⁻² | parameter | §2 |
| Body weight | `W = Mg` | 686.7 N | derived | §6.1 |
| Pendulum length, contact to COM | `ℓ` | 0.95 m | assumed (Module 7's 0.9 m + ankle height) | §2 |
| Pendulum rate | `ω₀ = √(g/ℓ)` | 3.21 s⁻¹ | derived | §2 |
| Reference walking speed | `v` | 1.3 m s⁻¹ | assumed | §7 |
| Optimal step length | `L*` | 0.684 m | derived (Lab 2) | §7 |
| Cadence at `L*` | `c*` | 1.90 steps s⁻¹ (114 min⁻¹) | derived | §7 |
| Stride period | `T = 2L*/v` | 1.053 s | derived | §11 |
| Step half-angle at `L*` | `α` | 0.368 rad (21.1°) | derived | §5 |
| Stance fraction of the stride | — | 62 % | assumed | §1 |
| Double-support fraction | — | 24 % | derived (2×62−100) | §6.1 |
| Swing-cost coefficient | `b` | 0.09 m² | assumed | §7 |
| Preferred-speed CoT | `CoT*` | 2.2 J kg⁻¹ m⁻¹ | assumed | §7 |
| Passive-walker slope | `γ` | 0.05 rad (2.9°) | assumed | §9 |
| Peak vertical GRF | `n_peak` | 1.10–1.20 W | assumed | §6.1 |
| Hip lever ratio | `b/a` | 2.0 | parameter (Module 3 §4.2) | §6.1 |
| COP travel, heel to toe | — | −0.06 to +0.19 m about the ankle | assumed | §11 |
| Older-adult reaction delay | `Δ` | 0.20 s reference; 0.08–0.32 s swept | assumed | §10 |
| Marker angle noise | `σ_θ` | 2 mrad | assumed | K6 |

---

### B15 — `module08.html:432`: the joint-power figure claims a model that appears nowhere

> Joint power is signed and computed from a parametric gait model.

No parametric gait model exists in this module. This is the same defect class as
Module 3's B13 ("captioned '(computed)' with no equation"). I decoded the three
polylines against the figure's own axis labels (y: 89 px → 2 W/kg, 185 px → −1 W/kg;
x: 78 px → 0 %, 592 px → 100 %) and the curves do carry real content: the ankle peaks
at **3.08 W/kg at 49.7 %** of the cycle, the knee troughs at **−1.10 W/kg at 16.1 %**,
the hip peaks at **1.09 W/kg at 14.1 %**. Those are physiologically right, and the
ankle peak agrees with the rewritten Lab 3's 3.06 W/kg to within 1 %. The caption
should say so and should stop claiming a computation the module does not contain.

Also, the caption locates the A2 burst at "40–62 % of the cycle" while the drawn peak
is at 49.7 %.

**Replacement:**

```html
<figcaption>Joint power is signed, and its pattern is the anatomy of a step. The
curves are a normalised sagittal-plane template of ankle, knee and hip power for
level walking, not an output of this module's code; what this module computes is the
ankle burst, and Lab&nbsp;3 of <a class="secref" href="#labs">section 11</a> reproduces
its peak of $3.1\ \mathrm{W\,kg^{-1}}$ from the ground reaction and the COP travel
alone, agreeing to within $1\,\%$. The ankle's positive burst (A2, shaded) peaks near
$50\,\%$ of the cycle and is the anatomical push-off of
<a class="secref" href="#transition">section 5</a>; the knee absorbs energy after heel
strike, reaching $-1.1\ \mathrm{W\,kg^{-1}}$ at $16\,\%$, and again in pre-swing; the
hip powers the trunk early in stance, peaking at $1.1\ \mathrm{W\,kg^{-1}}$ at
$14\,\%$. Measured curves and their uncertainty come in Module&nbsp;15.</figcaption>
```

---

### B16 — `module08.html:820`: the captures/misses table omits the vault's most visible failure

> Inverted-pendulum walking | COM vault, energy exchange, Froude scaling | Soft tissue,
> foot roll details, active control

The rigid vault's largest and most easily checked error is not soft tissue: it is that
it predicts a **single-humped vertical ground reaction peaking at midstance
(0.82 W)**, when force plates measure a **double hump peaking at 1.10 W at 28 % and
72 % of stance with a 0.75 W trough at midstance** — and it never exceeds body weight
at all. K1 now computes this. A captures/misses section that lists the model's real
successes and omits its most visible failure fails part 4 of the standard.

**Replacement row:**

```html
<tr><td>Inverted-pendulum walking</td><td>COM vault, energy exchange, Froude scaling,
the $0.82\,W$ midstance unloading</td><td><b>The shape of the vertical ground
reaction</b>: it predicts a single hump peaking at midstance and never exceeding body
weight, against the measured double hump of $1.10\,W$ at $28\,\%$ and $72\,\%$ of
stance about a $0.75\,W$ trough (K1). Also soft tissue, foot roll, and active
control.</td></tr>
```

---

### B17 — `module08.html:468,481`: §8's central claim carries no torque

> If the arms did not swing, the trunk would have to absorb more yaw and roll momentum,
> requiring more muscular stabilization.

and

> the missing counter-swing must be made up by the trunk and hip muscles.

This is exactly the sentence shape the brief bans: a qualitative substitute for
mechanics with no force, torque or moment following it. §8 is the module's only section
with no number anywhere in it. Prop 8.1 states `L̇_G = ΣM_G^ext` and stops.

**Replacement (`:481`):**

```html
<p>That bookkeeping has a size, and it is worth computing rather than gesturing at.
About the body's vertical axis a segment of mass $m$ at mediolateral offset $y$ moving
fore-aft at $v_x$ carries $L_z=-m\,y\,v_x$. The two legs are antiphase <em>and</em> on
opposite sides of the midline, so their contributions carry the same sign and
<em>add</em>: with $m_{\rm leg}=0.161M=11.3$&nbsp;kg at $d_{\rm leg}=0.09$&nbsp;m
moving at $1.3\ \mathrm{m\,s^{-1}}$ relative to the trunk,
$|L_{\rm legs}|=2.64\ \mathrm{kg\,m^2\,s^{-1}}$. Each arm swings opposite its
ipsilateral leg, so the arms subtract: with $m_{\rm arm}=0.050M=3.5$&nbsp;kg at
$d_{\rm arm}=0.20$&nbsp;m moving at $0.6\ \mathrm{m\,s^{-1}}$,
$|L_{\rm arms}|=0.84\ \mathrm{kg\,m^2\,s^{-1}}$, cancelling $32\,\%$ of the legs'
momentum.</p>

<p>The residual $1.80\ \mathrm{kg\,m^2\,s^{-1}}$ must reverse sign twice per stride, so
by Prop&nbsp;8.1 the trunk and hip muscles must supply a mean yaw torque of
$2|L|/(T/2)$ over each half stride of $0.526$&nbsp;s: $10.0$&nbsp;N&nbsp;m with the arms
held still against $6.8$&nbsp;N&nbsp;m with them swinging. That is the number behind
"tying the arms down changes the gait". The arms are light &mdash; five percent of body
mass each against sixteen for a leg &mdash; but they act at more than twice the moment
arm, and that is the whole trade. K8 rebuilds this estimate and tests how hard it
leans on the two assumed offsets.</p>
```

---

## 3. Style and clarity edits

- **S1 `:243`** — "$v\approx\sqrt{0.5\,g\ell}\approx2.0\ \mathrm{m\,s^{-1}}$" understates
  its own arithmetic; with the unified `ℓ = 0.95` m it is `2.16`. Applied with B9.
- **S2 `:633`** — `np.trapz` is deprecated and prints a `DeprecationWarning` on every
  run of the copy-buttoned block. Changed to `np.trapezoid` (applied with B1's Lab 3
  rewrite).
- **S3 `:187`** — the figure caption asserts "about 62 %" with no table row. Row added
  (B14); caption unchanged, since the value is now sourced.
- **S4 `:247`** — "Dynamic similarity" is boxed as a `.keyresult` with no statement of
  where it comes from. Prefix: "This is a corollary of Prop 2.2, not a new claim:".
- **S5 `:452`** — `C` for cost collides visually with `c` for cadence (§1), and D8 uses
  `a, b` for the same two constants §7 calls `A, B`. Unified on `½M` and `bM` in both
  places, so the proxy has one free constant with a name and a unit.
- **S6 `:744`** — D8's cost proxy `C(L)=a sin²(...)+b/L²` is dimensionally different
  from §7's (`b/L²` against `bM(v/L)²`). Rewritten to match §7 exactly.
- **S7 `:522`** — "$\gamma\approx0.05$ rad ($3^\circ$)": 0.05 rad is 2.9°, not 3°.
  Applied with B9.
- **S8 `:199`** — "often well approximated as a nearly rigid link": "often" and
  "nearly" both hedge the same clause. Trimmed to "well approximated as a rigid link,
  an idealisation section 12 returns to".
- **S9 `:586`** — "deliberately small but scientific" is a self-assessment, not a
  claim. Replaced with what the labs actually do (applied with B1).
- **S10 `:668-704`** — every C-problem solution is one sentence. C1, C3, C6 and C9 now
  end with the number the corresponding section computes, so a conceptual answer still
  lands on something concrete: C3 gains "the exchange is 25.3 J per step against a
  26.7 J transition loss", C6 gains "26.7 J to 7.7 J for a half-and-half split", C9
  gains "19.3 J per step of slope work at γ = 0.05 rad".
- **S11 `:832`** — the "First use" column is plain text where Module 4's Appendix links
  each symbol to its section. Converted to `<a class="secref">` links.
- **S12 `:812`** — the diagnostics run together with no separator in the rendered text.
  Left as is; this is the module's house list style and matches Modules 3 and 4.
- **S13 `:566`** — §10's physics layer lists four risk variables with no magnitude.
  A closing sentence now points at the computed margin: "Lab 4 puts numbers on that:
  a 0.20 s delay costs 0.09 m of the 0.155 m margin, and K10 ranks the three."
- **S14 `:460`** — the `v*` marker line has zero length and draws nothing. Fixed with
  B6.
- **S15 `:840`** — the closing paragraph lists forward references but does not say what
  the reader can now do. Opening sentence added: "A reader who has worked through this
  module can take a step length, a walking speed and a leg length and produce the
  collision loss, the push-off saving, the ankle power, and the peak hip reaction, each
  to within the accuracy of one stated assumption."

---

## 4. Structural notes

1. **The labs are in the wrong place relative to the problems.** §11's four labs and
   §12's ten K problems compute overlapping quantities with different constants
   (`ℓ = 0.9` against `0.95`, `v = 1.35` against `1.3`, `L* = 0.684` against `0.6`).
   After this pass they share one reference gait, stated once in §7 and cited by both.
   That is the structural fix; consider making it explicit with a short "reference
   gait" box in §7 if the module is revisited.

2. **§8 is a third the length of any other section and carries one proposition.** Even
   after B17 it is thin next to §5 and §9. The plan file (`module08-plan.md`) asked it
   to "connect to trunk rotation and reduced muscular work"; the trunk rotation half is
   still missing.

3. **§10 has four subsections of biology and chemistry and one boxed inequality of
   physics.** The proportion is defensible for the module's stated purpose, but the
   physics subsection is the only one the rest of the course can check, and it was the
   one left unproved. After B5 it carries a proposition, a proof, and a worked margin.

4. **No section states where its models sit on the level ladder**, which the brief
   requires of every module. §2's vault and §4's compass gait are Level 1–2; §6's
   inverse dynamics is Level 3; §9's limit cycle is Level 4. This is not repaired here
   because it is a course-wide convention question, not a Module 8 defect — flagging it
   for the next pass.

5. **The diagnostics list (`:812`) is good and should be kept.** "If a gait figure has
   arrows but no foot, COP, COM, or event labels, it is not yet a gait figure" is the
   figure standard restated as a test, and it is the only place in the course where
   that happens.

---

## 5. What already works

- **Prop 2.2 is the best passage in the module.** It gets `Fr ≤ 1` out of a contact
  constraint — `N ≥ 0` because a foot pushes and cannot pull — rather than out of
  dimensional analysis, and then it says what happens at the boundary ("the vault turns
  ballistic, so any faster gait must leave the ground"). That is parts 1, 3 and 4 of the
  standard in one paragraph.

- **Prop 4.1's proof.** Choosing the moment about the *new* contact point so the
  impulsive reaction drops out is exactly the right move, and the proof says why it is
  the right move instead of just making it. Its closing line — "precisely the
  redirection loss computed energetically in section 5" — is the kind of cross-check
  that lets a reader trust the next section.

- **Prop 9.1's limit case.** "On the level ($\gamma=0$) the only solution is $v=0$" is
  the honest statement, and the `.keyresult` after it refuses the free-lunch reading in
  plain words. The plan file made "passive dynamic walking must be honest" a locked
  decision and the section keeps it.

- **§10's framing.** Reading the causal stack bottom-up — chemistry sets the substrate,
  biology sets the control reserve, physics is the visible event — is a genuinely good
  organising idea, and the post-fall cascade paragraph is the one place in the course
  that treats a mechanical failure as a biological transition. Nothing in it is
  softened.

- **The gait-cycle figure and the stride-timing bar (Figs. 1–2).** The timing bar in
  particular does something prose cannot: it shows the two double-support overlaps as
  overlaps, which is why the walking/running distinction lands immediately.

- **Prop 6.1's proof** correctly explains *why* the recursion starts at the foot (it is
  the free end, where the only external load is measured), which is the part of inverse
  dynamics students usually take on faith.

---
