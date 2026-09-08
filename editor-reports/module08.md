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

### B18 — `module08.html:764-800`: ten K figures describe a plot that was never drawn

Found by decoding, not by reading. Every K problem carried a `<figure>` whose
`aria-label` promised a computed plot — "Froude number against walking speed for three
leg lengths", "RMS torque error against sample rate on logarithmic axes" — while the
`<svg>` body held a schematic with a placeholder `<figcaption>K2 figure.</figcaption>`
and no axes, no ticks and no data. Six of them (K1, K2, K4, K6, K8, K9) were in that
state; three more (K3, K5, K10) drew a number the solution contradicts; K7 drew a bare
schematic and kept its `<figcaption>K7 figure.</figcaption>` placeholder.

The standard this fails is *tie to something concrete*: a figure that names a quantity
it does not plot is worse than no figure, because the reader believes the check has been
done. Replacement: all ten redrawn by `m08b/genk.py` as framed plots with computed tick
labels, and a real caption each. Every plotted vertex is the model evaluated at that
abscissa, so the figures can be — and were — decoded back into data and compared with the
solutions (`m08/decode.py`, `m08/decode2.py`). The decodes agree with `nums_k.json`
to the 0.1-px rounding of the SVG coordinate: K1's midstance `Fy/W` reads `0.8188`
against the model's `1 − Fr = 0.81866`; K3's three marked minima read `0.5767`, `0.6844`,
`0.8067` against `0.57674`, `0.68438`, `0.80664`; K9's fixed-point ring reads
`(60.4449, 60.4572)` against `E* = 60.4435` J; K10's six bars read `−1.48, −0.58, +2.68`
and `+0.88, +0.35, +0.00` against elasticities I re-derived in closed form
(`∂ξ/∂v = Δ + 1/ω₀`, `∂ξ/∂Δ = v`, `∂ξ/∂x_s = 0`); K7's three minima all decode to
`L = 0.6844` m at `29.22`, `49.41` and `74.89` J, which is the coincidence its solution
claims. The redrawn figures were also rendered and looked at, not only gated
(`m08/prevk7.py` → `prevk.png`).

### B19 — `module08.html:432,460`: a decorative "walker" that renders as a beige slab

Both regenerated plots carried an ornamental figure built from limb capsules at the
right-hand margin. At the plot's scale it renders as a `23.9`-px beige bar with two
lentil-shaped ellipses, and in the joint-power figure a head circle floats `130` px above
it with nothing between. It reads as a smudge, not a body, and it is the failure mode
`check_bodyprop` exists to catch — the gate passed only because the pieces are separate
elements. Removed, and each viewBox retightened to its remaining content
(`0 0 760 300 → 0 0 645 300`; `0 0 740 270 → 0 0 590 270`), which is what dropped
`check_frame`'s advisory count from `8` to `4`.

### B20 — `module08.html:784`: K6 quotes three RMS values that no seed reproduces

"With a fixed seed the RMS torque error is `0.137`, `0.643` and `2.704` N m" — but the
problem never says which seed, and no seed gives that triple. Re-running the described
computation under `np.random.default_rng(0)` gives `0.13665`, `0.55621`, `2.46816`
(`m08b/vfy.py`). The same paragraph then claimed the analytic values "bracket the sampled
ones", which is false in both directions: the analytic `0.154, 0.617, 2.469` lie *above*
all three sampled values. Fixed by naming the seed in the problem statement, quoting the
three numbers the run prints, replacing the bracket claim with the true relation (the
analytic form reproduces the sample to within `13 %` at every rate — verified:
`12.7 %`, `11.0 %`, `0.03 %`), and correcting the downstream "even `2.7` N m is under
`3 %`" to `2.5` N m (`2.468 / 95.1 = 2.6 %`).

### B21 — `module08.html:776`: K4's push-off reduction quoted to a digit it cannot hold

The stated `36.8 %` reduction at `f = 0.25` is `36.85 %` at the exact cost optimum
`L* = 0.684379` m (`m08/vfy3.py`), so `36.9 %`. The value moves over `36.844–36.860 %`
across the three roundings of `L*` the module quotes, which is worth knowing: the last
digit is at the edge of what the input supports, and the figure's own label carries no
third digit.

### B22 — `module08.html:772`: K3's grid search finds a spurious edge minimum

Swept over a wide `L` grid, the cost proxy's `κ = 0.15 m²` curve has no interior minimum
below the `α = 45°` turnover — the search runs to the grid edge and returns
`L* = 1.600` m, which is `L → 2ℓ` and not a gait. The solution's robustness claim was
written from that run. Restricted to the well-posed range the minimum is interior at
`0.80664` m, which is the value the redrawn figure marks with a dot and the caption
quotes. The closing sentence about `κ`-sensitivity of the *cost* is kept, since it is
true and does not depend on the bad branch.

### B23 — `module08.html:522`: Prop 9.1's proof compares its two speeds on the wrong base

"K9 solves the same energy balance without them and gets `1.31` m s⁻¹, `5.2 %` higher."
The small-angle result is `1.246035` m s⁻¹ and K9's exact fixed point is `1.314138`
m s⁻¹ (`m08/vfy3.py`), so the exact value is `5.466 %` **higher** than the small-angle
one. `5.2 %` is the *other* comparison — the small-angle value is `5.18 %` *below* the
exact — which is exactly what K9's own solution at `:906` correctly says. One number was
copied between two sentences that divide by different denominators. Replacement:
`$5.5\,\%$ higher`. K9's `:906` sentence is correct as written and is left alone.

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
  `a, b` for the same two constants §7 calls `A, B`. Unified on a single named
  constant `κ` (the swing-cost coefficient, `0.09 m²`, labelled as assumed) in both
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
  lands on something concrete. The values that shipped are the ones the labs and the
  figure generator print, not the draft estimates this bullet first carried: C3 gains
  "the vault exchanges `Mg Δh = 43.8` J each way (Lab 1) while the transition destroys
  `26.7` J", C6 gains "the per-step cost falls from `26.7` J to `8.8` J (Prop 5.2)",
  C9 gains "the descent supplies `MgL sin γ = 19.3` J per step". All three were
  reprinted from `blocks2/blk01_L660.py`, `vfy3.py` and `genk.py` before shipping.
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

## 6. Changes applied

All 66 edits are applied by one re-runnable script,
`scratchpad/m08/apply.py`, whose `rep(old, new, tag)` asserts that each anchor
occurs **exactly once** before replacing it. The protocol is

```
cp module08.html edited/module08.html
python scratchpad/m08/apply.py     # prints "applied 66 edits:" and the tag list
```

Run twice from the pristine copy it produces a byte-identical file
(`md5 7f78d195fc1aa432d8c501e98df9cfe0` both times). The ten figure bodies come
from `genk.py → svgk.json`, which is itself deterministic (regenerating it
reproduces the same file, and the same `nums_k.json`); the cost-of-transport
figure comes from `fig7.py → fig7.json`. All of these now sit **beside**
`apply.py` in `scratchpad/m08/`, and `apply.py` loads `svgk.json` by
`Path(__file__).with_name(...)`, so the pipeline no longer reaches into another
agent's scratchpad folder to build. (`genk.py`, `svgk.json`, `nums_k.json` and
`vfy.py` were originally authored in `scratchpad/m08b/`; identical copies remain
there.)
Line numbers below are lines of the **pristine** `module08.html`, computed
programmatically by locating each anchor string in it
(`scratchpad/m08/apply_map.py → tagmap.json`), not counted by hand. The tags
that act on text an earlier edit created (`K*-fig`, `B20`–`B23`) are listed at
the line of the block they sit inside.

| tag | line (original) | what changed | how verified |
|---|---|---|---|
| B12a+S8 | 199 | §2's "often well approximated as a nearly rigid link" loses the double hedge and gains a forward pointer to §12: "well approximated as a rigid link of length `ℓ` from the contact point to the COM, an idealisation §12 returns to". | Prose only. `checktex` 0, `verify_dom` 0 `mjx-merror`; read aloud. |
| B2 | 162 | The visual map's twelve figure cross-references were each off by one from Fig. 2 onward ("Fig. 2 derives the COM vault" when Fig. 2 is the stride timeline). All twelve clauses re-matched to the figures that exist. | Enumerated the `<figure>` elements in document order and matched each clause against that figure's `aria-label`. |
| B9a | 219 | §2 gains the `ω₀` reconciliation with Module 7: there `ℓ = 0.9` m is the COM height above the **ankle** with `I ≈ 66 kg m²`, giving `ω₀ = √(Mgℓ/I) = 3.1 s⁻¹`; here the pivot is the ground contact point, `ℓ = 0.95` m, point mass, `ω₀ = √(g/ℓ) = 3.21 s⁻¹`. Both the pivot change and the body idealisation are named. | Both cited values checked in `module07.html:356` and its parameter table `:947`; recomputed `√(686.7·0.9/66) = 3.060` and `√(9.81/0.95) = 3.2135`. |
| B9b+S1 | 243 | The Froude proof's "with `ℓ ≈ 0.9` m this is `v ≈ 2.0 m s⁻¹`" replaced by the module's own reference length: "with the module's reference `ℓ = 0.95` m this is `v = √(0.5 gℓ) = 2.16 m s⁻¹`". | `√(0.5 · 9.81 · 0.95) = 2.1585` (`m08/vfy3.py`). |
| S4 | 247 | "Dynamic similarity" prefixed with "This is a corollary of Prop 2.2, not a new claim." | Read-through; no number touched. |
| B3a | 387 | Prop 5.2 restated so the two accountings are separate: `n` equal inelastic collisions dissipate `n·½Mv²sin²(β/n) ≈ ½Mv²β²/n` (falls as `1/n`), while push-off plus one collision falls as `1/n²`. The exact `n = 2` ratio `tan²α/sin²2α = 1/(4cos⁴α)` is stated, `= 0.330` at `α = 21.1°`, not the textbook `¼`. | `m08b/vfy.py`: exact ratios `1.0000, 0.3301, 0.1685, 0.1026` for `n = 1…4`; closed form `1/(4cos⁴α) = 0.3301`. |
| B3b | 391 | Its proof written out, including the step that shows steady state **forces** the half-and-half split (`cos(2α−φ) = cos φ ⇒ φ = α`), and the reference-gait numbers: collision-only `26.7` J against split `8.8` J, a saving of `3.03×` and not `4×`. | `m08b/vfy.py` prints `f = 0.00 → 26.7146 J`, `f = 0.50 → 8.8185 J`, ratio `0.3301`, `1/0.3301 = 3.03`. |
| B9c+S7 | 522 | Prop 9.1's worked example unified on the reference `ℓ = 0.95` m; `α = 0.30` rad; `γ = 0.05` rad relabelled `2.87°` (it was called `3°`); result `v = 1.25 m s⁻¹`; and the small-angle substitutions named as doing real work at `2α = 34.4°`, with K9's exact answer cited. | `m08/vfy3.py`: `√(gℓ sin γ/α) = 1.246035 m s⁻¹`; `0.05 rad = 2.8648°`. |
| B12b+B17b | 473 | Prop 8.1 restated with `H_G` for whole-body angular momentum. `L` is step length everywhere else in the module, so the old `L_G` was a live collision. | Symbol sweep of the whole file for `L` in both senses; `checktex` 0. |
| B17c | 477 | The one surviving `\dot{\mathbf L}_G` inside Prop 8.1's proof changed to `\dot{\mathbf H}_G`. | Same sweep; `check_links`/`checktex` clean. |
| B6a | 448 | §7 rewritten: it now fixes the **reference gait** (`M = 70` kg, `ℓ = 0.95` m, `v = 1.3 m s⁻¹`) that the rest of the module and every K problem use; names the swing-cost coefficient `κ = 0.09 m²` and labels it the section's single assumption (`κM = 6.3 kg m²` as an effective swing inertia); and quotes the computed optimum `L* = 0.684` m, `26.7 + 22.7 = 49.4` J, `α = 21.1°`, `c* = 1.90 s⁻¹ = 114` min⁻¹, `T = 1.053` s, plus the asymmetric flatness `+4.6 % / +8.2 %`. | Lab 2's block re-extracted from the **edited** file and run (`blocks2/blk02_L684.py`): `0.6846734, 26.7341, 22.7123, 49.4464, 1.89872, 1.05334`. Flatness recomputed about that `L*` in `m08/vfy3.py`: `+4.644 % / +8.229 %`. |
| B6b+S14 | 460 | The cost-of-transport figure regenerated (its `v*` marker line previously had zero length and drew nothing), and its caption now derives both coefficients from the two stated calibration conditions instead of asserting them: `c_s = v*·CoT*/2 = 1.43`, `c_f = CoT*/(2v*) = 0.85`. | Decoded the shipped SVG back to data from its tick labels: the marker sits at `(1.3001, 2.2007)`, and the drawn curve's own minimum is `√(1.43/0.85) = 1.297` at `2√(1.43·0.85) = 2.205` — agreeing with the caption to the two significant figures it quotes. |
| B15+B4 | 432 | Two changes in one anchor. (a) The joint-power caption now says the three curves are a **drawn template**, not a computation, gives the read-offs (ankle `3.0 W kg⁻¹` near `50 %`, knee `−1.2` at `16 %`, hip `1.0` at `14 %`), and names Lab 3's `3.06 W kg⁻¹` as the only independent check. (b) §6 gains the whole subsection "Worked number: the peak hip reaction in walking", which pays Module 3's debt: midstance trough `1 − Fr = 0.819 W = 562` N, redirection impulse `2Mv sin α = 65.6 N s` over `0.126` s giving `1.76 W` through double support, a periodicity check closing to `4.4 %`, and `R_peak ≈ (1.10–1.20)×(2.6–2.8) W = 2.9–3.4 W`. | (a) Decoded the three polylines from the shipped file: ankle max `2.981 W kg⁻¹` at `49.75 %`, knee min `−1.194` at `16.09 %`, hip max `0.997` at `14.07 %` — every read-off in the caption is what is drawn. (b) whole chain re-run in `m08b/vfy.py`: `562.17 N`, `65.5563 N s`, `518.86 N`, `1.7556 W`, `1.04352` (err `4.35 %`), `2.86–3.36 W`. |
| S13 | 566 | §10's list of four risk variables gains a closing sentence with the computed margin: `0.155` m recoverable, of which a `0.20` s reaction delay alone spends `0.090` m. | Lab 4 run (`blocks2/blk04_L737.py`): capture `0.260` m against reach `0.415` m; `0.45 × 0.20 = 0.090` m. |
| B5 | 570 | Prop 10.1 was boxed as a stability condition and never proved. Restated as a two-sided inequality `x_com + ẋ_com/ω₀ ≤ x_p ≤ x_s^max`, given a full proof from the linear inverted pendulum (the sign of `A` decides everything; the decaying mode can never carry the COM forward), tied to Module 7's Prop 4.2, and closed with the worked reference perturbation `0.030 + 0.090 + 0.140 = 0.260` m against a `0.415` m reach. | `ω₀ = √(9.81/0.95) = 3.21346`; `0.45/ω₀ = 0.140035`. Module 7's Prop 4.2 (`ξ = x_com + ẋ_com/ω₀`, `ξ̇ = ω₀(ξ − x_cop)`) confirmed verbatim at `module07.html:373`. |
| B17a | 468 | §8's opening no longer calls arm swing "not irrelevant" without a number; it states the torque the section will produce, `≈10 N m` with the arms held still against `6.8 N m` with them swinging. | `m08/vfy3.py`: `2H/(T/2) = 10.014` and `6.824` N m. |
| B17d | 481 | §8's closing computes the yaw-momentum budget from segment masses and offsets rather than asserting a percentage: legs `2.64 kg m² s⁻¹`, arms `0.84`, cancellation `32 %`, residual `1.80`, reversed twice per stride. The three masses and two offsets are labelled as the only assumptions. | `m08/vfy3.py`: `H_legs = 2.63718`, `H_arms = 0.84000`, residual `1.79718`, cancel `31.85 %`, `T/2 = 0.52667` s. |
| B1a+S9 | 586 | §11's opening loses the self-assessment ("deliberately small but scientific") and states instead that all four labs run on one reference gait and that every number quoted after a block is that block's printed output. | Enforced by re-extracting all four blocks from the **edited** file and diffing every printed value against the prose. |
| B1b | 596 | Lab 1 printed nothing usable. Rewritten to print the step half-angle, the COM rise, `MgΔh` and the Froude sweep; its paragraph now quotes them and contrasts the `43.8` J exchanged against the `26.7` J destroyed. | Ran `blocks2/blk01_L660.py`: `21.1228°`, `Δh = 0.0638304` m, `MgΔh = 43.8324` J, `Fr = 0.039, 0.069, 0.107, 0.155, 0.210, 0.275, 0.348`, reference `Fr = 0.1813`. |
| B1c | 613 | Lab 2 rewritten to print the optimum, both cost terms, the cadence and the stride period; its paragraph quotes them and the flatness asymmetry. | Ran `blocks2/blk02_L684.py` (values above). |
| B1d | 623 | Lab 3's heading changed from a name that promised inverse dynamics to "Lab 3: quasi-static ankle inverse dynamics", which is what the code does. | Read against the code it heads. |
| B1e+S2 | 629 | Lab 3 did no inverse dynamics. Rewritten so the GRF **scale** is fixed by the impulse-momentum identity `∫F_y dt = WT/2` rather than assumed; the COP travel is §3's anatomy; `np.trapz` (deprecated, warns on every reader's run) replaced by `np.trapezoid`. Its paragraph separates the two assumptions (GRF shape, plantarflexion rate) from the one derived quantity (the amplitude). | Ran `blocks2/blk03_L708.py`: stance impulse `361.6796` = target `361.6796`, `peak F_y/W = 1.1024`, midstance `0.7523`, peak moment `95.0971 N m`, peak power `214.353 W = 3.0622 W kg⁻¹`, positive work `22.5224` J. No `DeprecationWarning`. `check_code` 0 (pycodestyle). |
| B1f | 644 | Lab 4 rewritten to print the capture point at each reaction delay and count how many step reaches still recover; its paragraph quotes the whole sweep and draws the conclusion the sweep supports (delay alone is a weak predictor). | Ran `blocks2/blk04_L737.py`: `0.206 → 0.314` m across `0.08 → 0.32` s; `7/7` recover to `0.24` s, `6/7` from `0.28` s; failure margin `0.034` m at `0.32` s. |
| C1 | 668 | C1's one-sentence answer now closes on the split's cost: the falling half is nearly conservative, the catching half is where Prop 5.1's `26.7` J per step leaves. | `m08b/vfy.py` `f = 0` value `26.7146` J. |
| C3 | 676 | C3 now contrasts exchange with loss numerically: the vault exchanges `Mg Δh = 43.8` J each way (Lab 1) while the transition destroys `26.7` J. | Lab 1 and `vfy.py` runs above. |
| C6 | 688 | C6 now states the size of the effect it describes: the per-step cost of the reference gait falls from `26.7` J to `8.8` J (Prop 5.2). | `m08b/vfy.py`: `26.7146 → 8.8185` J. |
| C9 | 700 | C9 now gives the slope's energy supply: `MgL sin γ = 19.3` J per step at `γ = 0.05` rad, exactly what the collision destroys. | `m08b/genk.py` prints `b = MgL sin γ = 19.2707` J with `L = 2ℓ sin α = 0.56149` m. |
| B13 | 680 | C4's figure had no caption at all. One added, defining the centre of pressure as the pressure-weighted mean of the contact pressure and stating the heel→ankle→toe travel. | Confirmed the `<figure>` carried no `<figcaption>` in the pristine file; `check_probfig`/`check_svg` clean after. |
| D8 | 744 | D8's cost proxy was dimensionally different from §7's (`b/L²` against `κM(v/L)²`) and used unnamed `a, b`. Restated as §7's exact proxy with `κ`, and the solution now derives the first-order condition rather than quoting an optimum. | Consistency checked term-by-term against B6a's §7 text; the stationary condition re-derived and its root compared with the Lab 2 grid minimum `0.6846734` m. |
| D9 | 748 | D9 asked for a derivation of a capture inequality written in bare `x`; restated in `x_com` and explicitly "from the linear inverted pendulum, rather than quoting it", with the solution supplying the `A`-sign argument. | Matches B5's proof line for line; symbols checked against Module 7's Prop 4.2. |
| K1 | 764 | Was "simulate COM height … which step angle produces the largest exchange?" — geometry with no mechanics. Now: integrate the rigid vault's stance arc and get the **vertical ground reaction** `F_y(θ) = M cos θ (g cos θ − v(θ)²/ℓ)`, discover it predicts a single hump peaking at midstance, and confront that with the measured double hump. | Ran the model: midstance `F_y/W = 1 − Fr = 0.81866`; edge values `0.73665, 0.67523, 0.59928` at `α = 12°, 16°, 20°`; speed sweep edge values `0.5759, 0.3446, 0.2780, 0.1194` at `v = 1.3, 2.0, 2.16, 2.5 m s⁻¹` (`m08b/vfy.py`, re-derived in `m08/vfy3.py`). |
| K2 | 768 | Was a forward Froude sweep only — substitution. Now adds the **inverse problem**: recover a leg length from a measured walk–run transition speed, and state the assumption that makes the inversion possible. | `m08b/vfy.py`: forward `Fr(1.3) = 0.2153, 0.1813, 0.1566`; `v(Fr = 0.5) = 1.9809, 2.1586, 2.3228`; inverse `ℓ = 0.8991` m at `2.1 m s⁻¹` and `0.7360` m at `1.9 m s⁻¹`. |
| K3 | 772 | Was "optimize step length … at `v = 1.3`" — one number. Now adds a **sensitivity sweep** over the one assumed constant, `κ ∈ [0.05, 0.15] m²`, and asks whether the predicted step length is a model output or an artefact. | `m08b/genk.py`: minima `0.57674, 0.68438, 0.80664` m at `κ = 0.05, 0.09, 0.15`; the fourth-root scaling D8 derives. |
| K4 | 776 | Was "compare loss before and after a push-off that reduces the angle by 25 %" — the small-angle limit of a question that can be posed exactly. Now a **regime comparison**: sweep `f ∈ [0,1)` with the exact simplest-walker geometry and compare against the small-angle `1/n²` law. | `m08b/vfy.py`: exact `26.7146, 16.8698, 8.8185, 2.7406` J at `f = 0, 0.25, 0.5, 0.75`; small-angle `26.736, 6.684, 2.971, 1.671` J. |
| K5 | 780 | Was "from synthetic torque and velocity curves, integrate positive work" with no source for the curves. Now uses **Lab 3's own** moment and rate, and asks what fraction of the transition loss the ankle repays. | Ran `blocks2/blk03_L708.py`: `∫P⁺ dt = 22.5224` J, peak `214.353 W = 3.0622 W kg⁻¹` at `79.3 %` of stance; `22.52/26.71 = 84.3 %`. |
| K6 | 784 | Was "add noise … and observe how torque changes" — no numbers to check. Now fully specified: `θ(t) = 0.35 sin 2πt`, `σ_θ = 2` mrad, `np.random.default_rng(0)`, `np.gradient` twice, at `60/120/240` Hz, with the `f_s²` scaling derived rather than observed. | `m08b/vfy.py` under that seed: `0.13665, 0.55621, 2.46816 N m`; analytic `0.15432, 0.61727, 2.46909 N m`; true segment torque `Iθ̈ = 0.4836 N m`. |
| K7 | 788 | Was a single-speed cadence/step-length sweep. Now repeats it at `v = 1.0` and `1.6 m s⁻¹` and asks what the model predicts about **how** humans should change speed. | Cost proxy re-evaluated at the three speeds; the optimal `L*` is speed-independent in this proxy (`m08b/vfy.py` prints `L* = 0.68438` at `v = 1.0` and `1.6`), which is the point the problem now makes. |
| K8 | 792 | Was "model arm swing as reducing amplitude by 30 percent" — the answer handed to the reader. Now builds the yaw momentum from segment masses and offsets, so the `≈32 %` is an **output**, and asks how hard it leans on the two assumed offsets. | `m08/vfy3.py`: `H_legs = 2.63718`, `H_arms = 0.84000`, cancellation `31.85 %`, residual `1.79718 kg m² s⁻¹`, trunk torque `10.014 → 6.824 N m`. |
| K9 | 796 | Was "iterate `z_{n+1} = az_n + b` for different `a`" — a map with no physics behind it. Now **derives** the map from Prop 9.1 (`a = cos²2α`, `b = MgL sin γ`), finds the fixed point, cobwebs from a slow release, and compares the exact fixed-point speed with the small-angle estimate. | `m08b/genk.py`: `L = 0.561488` m, `a = 0.681179`, `b = 19.2707` J, `E* = 60.4435` J, `v* = 1.314138 m s⁻¹`, `E₈ = 57.8735` J (within `4.25 %`); e-folding `−1/ln a = 2.605` steps. |
| K10 | 800 | Was "sweep three variables … which has the strongest effect?" with no metric. Now ranks them by a stated **elasticity** `∂ln m/∂ln(·)` at the Lab 4 reference point, and asks how the ranking changes if the capture point rather than the margin is differentiated. | Re-derived in closed form and matched to `nums_k.json`: `∂ξ/∂v = Δ + 1/ω₀`, `∂ξ/∂Δ = v`, `∂ξ/∂x_s = 0`; margin elasticities `−1.48445, −0.58078, +2.67804`; capture elasticities `+0.88463, +0.34611, 0`. Capture `0.260036` m, margin `0.154964` m. |
| B16 | 820 | The "what the module captures / what it misses" table omitted the vault's most visible failure — that the rigid inverted pendulum predicts a single-hump ground reaction and measurement shows a double hump. Row added, pointing at K1. | The claim is K1's own result, verified above (`0.81866` peak at midstance against the template's `1.1024` at `28 %` and `72 %`). |
| B14a+S11 | 832 | The Appendix's notation table omitted most of the module's symbols and gave no links. Rebuilt to cover every symbol used in §0–§12, each linked to the section of first use with `<a class="secref">`, matching Module 4's Appendix. | Cross-checked symbol-by-symbol against a sweep of the shipped file; `check_links` 108 internal links, 0 broken, 0 unlinked section refs. |
| B14b+S3 | 836 | The Appendix had no parameter table, so several numbers in the body (the `62 %` stance fraction, `κ`, the segment mass fractions) had no admissible class. Table added with Symbol / Value / **Class** (derived, parameter, or assumption) / Where. | Every row's value re-derived or traced: the derived rows recomputed in `m08/vfy3.py`, the assumption rows marked as such. |
| S15 | 840 | The closing paragraph listed forward references but never said what the reader can now do. Opening sentence added naming the four things the module makes computable. | Read-through; each of the four is a number this pass verified. |
| K1-fig | 764 | K1's placeholder schematic replaced by the computed plot (three vault curves plus the measured double hump), with a real caption. | Decoded from the shipped SVG: midstance `0.8188`, edges `0.7362, 0.6751, 0.5994`, template peak `1.102` at `28.1 %`. |
| K2-fig | 768 | K2's schematic replaced by the computed `Fr(v)` plot for three leg lengths, with the walk–run band, the `Fr* = 0.5` line, and a ring marking the inversion. | Decoded: curves read `Fr = v²/(gℓ)` exactly (`0.7341, 0.6179, 0.5336` at `v = 2.4`); the ring sits at `(2.0998, 0.4998)`. |
| K3-fig | 772 | K3's schematic replaced by the computed cost proxy against `L` for three `κ`, each marked at its interior minimum. | Decoded: the three dots sit at `0.5767, 0.6844, 0.8067` m — `nums_k.json` to within `0.0001`. The polyline `argmin` differs by up to `0.02` m because the optimum is flat: `C(0.7849) = C(0.80664) = 62.28` J to four figures. |
| K4-fig | 776 | K4's schematic replaced by the exact curve plus the small-angle points. Its annotation "the small-angle 6.68 J — 32 % low" was ambiguous and wrong under the natural reading; changed to "the small-angle 6.68 J, low by 24 %". | `(8.828 − 6.683)/8.828 = 24.3 %` low; the `32 %` was the reciprocal base (`exact is 32.1 % above small-angle`). Regenerated through `m08b/genk.py`, then re-decoded from the shipped SVG: dashed points `(0, 26.737), (0.5, 6.687), (0.667, 2.963), (0.75, 1.675)`. |
| K5-fig | 780 | K5's schematic replaced by Lab 3's computed ankle-power curve with the positive area shaded. | Decoded: peak `214.30 W` at `79.3 %` of stance, matching the block's printed `214.353 W` at `79.33 %`. |
| K6-fig | 784 | K6's schematic replaced by a log–log plot of RMS error against sample rate, with the slope-2 analytic line and the true segment torque marked. | Decoded on log axes: the three sampled points read `0.1369, 0.5563, 2.4669 N m`; the analytic line has slope 2 (`0.1073 @ 50 Hz → 3.8518 @ 300 Hz`, ratio `36 = 6²`). |
| K7-fig | 788 | K7 was the one problem left with a bare schematic and the placeholder caption "K7 figure." — the gap B18 did not close on its first pass. Replaced by the cost proxy against step length at `v = 1.0, 1.3, 1.6 m s⁻¹`, each curve marked at its minimum, with the cadences `1.46, 1.90, 2.34 s⁻¹` in the legend and a caption that states the falsifiable prediction. | Decoded from the shipped SVG: the three dots read `L = 0.6844` m at `29.22`, `49.41`, `74.89` J — `nums_k.json`'s `0.68438` at `29.2235`, `49.4464`, `74.9010`. Removing this figure's placeholder also took `check_frame` from 4 wasted-margin advisories to 3. A first draft added a full-height dashed line at `L*`; `check_overlap` caught it crossing the note text, so the line was dropped and the gate is back to 0. |
| K8-fig | 792 | K8's schematic replaced by the computed yaw-momentum traces over one stride with the residual shaded. | Decoded: legs `±2.639`, arms `±0.8395`, residual `±1.796 kg m² s⁻¹`, over `x ∈ [0, 1.053]` s — the stride period `T` this module computes. |
| K9-fig | 796 | K9's schematic replaced by the stride map and its cobweb. | Decoded: the map line reads slope `0.6814`, intercept `19.27`; the fixed-point ring at `(60.4449, 60.4572)`; the staircase starts at `5.01` J and reaches `57.86` J. |
| K10-fig | 800 | K10's schematic replaced by a signed elasticity bar chart of the margin and of the capture point. | Decoded the six bars: `−1.4824, −0.5818, +2.6791` and `+0.8856, +0.3460, −0.0461`(zero bar) — matching the closed-form elasticities above. |
| B19a | 432 | The decorative "walker" removed from the joint-power figure: a `23.9`-px beige bar, two lentil ellipses and a head circle floating `130` px above them. | Rendered and looked at; `check_bodyprop` clean before and after (the gate cannot see it, because the pieces are separate elements). |
| B19b | 432 | That figure's viewBox retightened `0 0 760 300 → 0 0 645 300`. | `check_frame`: this figure no longer appears in the wasted-margin list. |
| B19c | 460 | The same decorative walker removed from the cost-of-transport figure. | As B19a. |
| B19d | 460 | That figure's viewBox retightened `0 0 740 270 → 0 0 590 270`. | `check_frame` advisory count fell from `8` (pristine) to `4` here, and to `3` once `K7-fig` landed. |
| B20a | 784 | K6's problem statement now names the seed, `np.random.default_rng(0)`. | Without it the stated RMS values are unreproducible by construction. |
| B20b | 784 | The quoted RMS errors `0.137, 0.643, 2.704 N m` replaced by `0.137, 0.556, 2.468 N m`. | Ran the described computation under that seed (`m08b/vfy.py`): `0.13665, 0.55621, 2.46816`. |
| B20c | 784 | The claim that the analytic values "bracket the sampled ones" deleted and replaced by the true relation: the analytic form reproduces the sample to within `13 %` at every rate. | Analytic `0.15432, 0.61727, 2.46909` lie **above** all three sampled values, so they bracket nothing. Ratios: `12.9 %`, `11.0 %`, `0.04 %`. |
| B20d | 784 | The downstream comparison "even `2.7 N m` is under `3 %`" corrected to `2.5 N m`. | `2.468 / 95.097 = 2.6 %`, using Lab 3's verified peak ankle moment. |
| B20e | 784 | The paragraph's closing sentence re-pointed at the quantity the calculation actually estimates (`Iθ̈`, true peak `0.48 N m`) rather than at the unrelated ankle moment. | `I = 0.48/(0.35·(2π)²) = 0.03474 kg m²`, consistent with `vfy.py`'s printed `0.4836 N m`. |
| B21 | 776 | K4's push-off reduction at `f = 0.25` quoted as `36.8 %` changed to `36.9 %`. | `m08/vfy3.py`: `36.8517 %` at the exact optimum `L* = 0.684379` m. The value ranges over `36.844–36.860 %` across the three roundings of `L*` the module quotes, so the last digit is at the edge of what the inputs support — flagged in B21 rather than hidden. |
| B23 | 522 | Prop 9.1's proof compared its small-angle speed with K9's exact one on the wrong base: "`1.31 m s⁻¹`, `5.2 %` higher" → "`5.5 %` higher". | `m08/vfy3.py`: small-angle `1.246035`, exact `1.314138`; the exact is `5.4656 %` higher. `5.2 %` is the reciprocal comparison (`5.18 %` lower), which is what K9's own solution at `:906` correctly states — that sentence is left alone. |
| B22 | 772 | K3's robustness claim was written from a grid search that ran to the grid edge (`L* → 2ℓ = 1.600` m, not a gait) because the `κ = 0.15 m²` curve has no interior minimum above the `α = 45°` turnover. Restricted to the well-posed range; the surviving sentence about the *cost* scaling with `κ` is kept, since it does not depend on the bad branch. | `m08b/vfy.py` reproduces the edge minimum `1.6000`; `genk.py` on the restricted range gives the interior `0.80664` m, which the redrawn figure marks with a dot and the caption quotes. |

### Figure decode (the check that found B18–B22)

Every touched figure was decoded back into data from the **shipped** file rather
than trusted from the generator: `m08/decode.py` reads each `<svg>`, fits the
pixel→data map from its own tick `<text>` elements (linear or `log10`, whichever
fits; residuals were `≤ 4×10⁻⁴` in every case except the deliberately log axes),
and inverts every `<polyline>`, `<circle>` and `<rect>`. `m08/decode2.py` adds
minima, markers and bar values. The ten K figures, the cost-of-transport figure
and the joint-power figure all decode to the model within the `0.1`-px rounding
of the SVG coordinates. No figure was found duplicated from another problem, no
curve draws its own formula backwards, and no viewBox is stretched to hide
out-of-frame content — `check_frame` reports no clipping and three wasted-margin
advisories, all three inherited from the pristine file (C3, C8, D7). The
regenerated figures were also rendered and read (`m08/prevk7.py` → `prevk.png`),
because a decode confirms the numbers and not the legibility.

### Gate results

| gate | pristine `module08.html` | `edited/module08.html` |
|---|---|---|
| `checktex` | 268 segments, 0 issues | 891 segments, **0 issues** |
| `checklt` | 0 | **0** |
| `check_links` | 46 links, 0 broken, 0 unlinked | 108 links, **0 broken, 0 unlinked** |
| `check_svg` | 0 hard, 1 advisory (4 polylines > 120 pts) | **0 hard**, 1 advisory (4 polylines > 120 pts) |
| `check_code` | 4 blocks, 0 issues | 4 blocks, **0 issues** |
| `verify_dom` | 0 `mjx-merror`, 36 stray `$`, 0 broken, 0 swallowed | **0 `mjx-merror`**, 24 stray `$`, 0 broken, 0 swallowed |
| `check_overlap` | 0 | **0** |
| `check_frame` | 0 clipped, 8 wasted-margin advisories | **0 clipped**, 3 wasted-margin advisories |
| `check_bodyprop` | pass | **pass** |

Zero where the baseline was zero, and better than the baseline on
`check_frame` (8 → 3 advisories) and on `verify_dom`'s stray-`$` count
(36 → 24). `check_svg`'s advisory count is held at the baseline's 4: the ten
regenerated K figures would have taken it to 20, so `genk.py`'s `curve()` now
subsamples any polyline to at most 100 vertices, keeping the endpoints and the
global extrema, which leaves every plotted vertex exactly on the computed curve
(the decode above was run on the subsampled figures that ship).

### Cross-module check

Module 3 forward-references this module for the peak hip reaction in gait. Every
citation in the new §6 subsection was checked against the source:

| claim in Module 8 | source | status |
|---|---|---|
| Module 3's (4.1) `R = W_s(1 + b/a)` with `W_s = ⅚W`, `a ≈ 5` cm, `b ≈ 10` cm, `= 2.5 W` | `module03.html:847,855` | verified verbatim |
| Module 3's "honest resultant" `2.6–2.8 W`, accounting for the abductors' `30°` line of pull | `module03.html:857` | verified; recomputed `|R| = √(2.5² + (1.667 tan 30°)²) = 2.68 W` |
| Module 3 states gait raises the peak to `3–5 W` and points here | `module03.html:859` ("pushing peak hip JRF to roughly `3`–`5 W` while walking and running") | verified |
| Module 3's in-vivo telemetry `2.3–2.9 W` in slow level walking | `module03.html:857,1491` | verified |
| `W = Mg = 686.7 N`, `R = 2.5 W = 1717 N` | this module | `70 × 9.81 = 686.7`; `× 2.5 = 1716.75` |
| Module 8 delivers `R_peak ≈ 2.9–3.4 W` | `m08b/vfy.py` prints `2.86–3.36 W` | consistent with both Module 3 bands (bottom of `3–5`, overlapping `2.3–2.9`) |

Module 7's numbers that §2 and §10 cite were checked the same way:
`ℓ = 0.9` m, `I ≈ 66 kg m²`, `ω₀ = √(Mgℓ/I) ≈ 3.1 s⁻¹` at `module07.html:356,947`;
`ω₀ = √(g/ℓ)` for the point-mass case at `:181,184`; Prop 4.2's
`ξ = x_com + ẋ_com/ω₀` and `ξ̇ = ω₀(ξ − x_cop)` at `:373`. All four match.

**One drift to report, not to fix.** A sibling pass has edited
`edited/module03.html` since this module's §6 was written. Its `:862` now reads
"an assumed `3`–`5 W` while walking and running (**Appendix**), against the
`≈2.3`–`2.9 W` that telemetry reads", its `:1513` adds "the `3`–`5 W` of §4.3
covers faster walking and running", and its Appendix `:2308` adds a row "Peak hip
reaction, walking and running (assumed; **computed in Module 8**)". That makes
the forward reference explicit and is *more* consistent with what this module now
delivers, not less. One number in that sibling edit is worth a second look by
whoever owns Module 3: `:858` says the resultant is "`2.6` to `2.8 W` across the
`α = 20°` to `40°` range", but `|R|` at `α = 40°` is `2.87 W`, which rounds to
`2.9`, not `2.8`.

### What this pass could not settle

Two numbers in the module are quoted to a digit their inputs do not support, and
both are left as they stand with the reason recorded here rather than churned:

1. **K1's `+0.344 W` edge reaction at `v = 2.0 m s⁻¹`** is `0.34442` using Lab 2's
   printed `L* = 0.6846734` m and `0.34462` using the exact optimum `0.684379` m
   — `0.344` under one rounding and `0.345` under the other. Left at `0.344`,
   which is what the figure's own generator computes.
2. **The `+8.2 %` cost of a `20 %` shorter step** (§7, Lab 2 and K3) is `8.229 %`
   about Lab 2's printed `L*` and `8.266 %` about the exact optimum. Left at
   `8.2 %`, which is the value about the `L*` the prose actually quotes.

Both are noted so a later pass does not "fix" one of them into disagreement with
the other places that quote it.
