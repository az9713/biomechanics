# Editor report: module13.html (Daily-Life Movement Case Studies)

Editorial pass. Standard: the five-part rule of the `science-editor` skill, read
against `EDITOR_DOMAIN.md`. Every location is `module13.html:LINE` (the pristine
file; the edit was applied to `edited/module13.html`). Every replacement is valid
HTML with MathJax delimiters and uses only the box classes the stylesheet defines
(`.def`, `.prop`, `.proof`, `.keyresult`, `.prob`, `.probes`, `.sol`).

All four Python blocks in the file were extracted, run, and compared with the
prose (scripts in the session scratchpad, folder `m13/`: `blocks/`, `verify.py`,
`cascade.py`, `kcode.py`). Sixty-one numbers were checked. Every number in a
replacement below was printed by a run recorded in this report. The Module 1
cross-check that drives B2 reproduces `module01.html`'s own published K4 output to
the newton (3561 N and 2333 N), which is the evidence that the reconstruction is
Module 1's model and not a new one.

## 1. Verdict

**Yes, after revision.** The mechanics is right and the six propositions are all
genuinely proved: 2.1, 3.1, 4.1, 5.1, 6.1 and 7.1 each carry an adjacent `.proof`
that derives the boxed result rather than restating it, and every one of their
worked numbers reproduces (109.87, 116.74, 210.13, 3629.7, 91.00, 81.63, 59.85,
119.24, 177.73). That is rigor parity, and it is the module's real strength. A
graduate reader can follow how a chair rise, a stair, a lift, a turn, a jar and a
hill each reduce to one line of statics or one line of impulse.

What stops the reader is four things. First, the module's organising concept is
defined backwards: §1 defines a margin as demand over capacity and then says a
movement is possible when the margin exceeds one, which is the failure condition,
while §2 uses the opposite convention four lines later. Every section and the
whole §8 table rest on that word. Second, §4 analyses the identical stooped lift
that Module 1 §6 already analyses (same 20 kg box, same 0.40 m reach, same 0.30 m
trunk arm, same 0.05 m muscle arm) but with an upper body of 0.50 M instead of
Module 1's 0.60 M, so the same lift yields 3630 N here and 4040 N there, with no
word about the difference. Third, the module claims four times that its
computational solutions carry code; no computational problem has any code at all,
and the one lab that declares a dynamic model (Lab A: rise height H, rise time T,
a vertical ground reaction) never computes it, then draws a conclusion that K8
computes to be the opposite sign. Fourth, roughly eighteen empirical numbers are
used with no table row, no derivation and no "assume", including every parameter
of Lab D and K5.

Three smaller failures are worth naming because they are wrong, not merely
unsupported: K2 says the mass-sensitivity of cadence "steepens at low power
ceilings" when it is directly proportional to the ceiling; Lab C says each
centimetre of load distance costs about 4 N of muscle force when the computed
figure is 39 N; and C3 says the muscle arm amplifies "about fortyfold per metre"
when $1/d_m$ is 20 per metre. K10 asks which task fails first and computes one
threshold, then asserts the ordering of the rest. K3 is D8 restated word for word.

None of this touches the six proofs, which are sound as they stand.

## 2. Blocking defects

Ranked: the inverted organising definition first, then factual errors, then
asserted results, then missing scaffolding, then problem-set depth.

### B1. §1 defines "margin" as demand over capacity, then says a movement is possible when it exceeds one; §2 uses the opposite convention

Location: `module13.html:79`, contradicted at `module13.html:97`.

Quoted (line 79): "The third recurring quantity is a <b>margin</b>: the ratio of
what a task demands to what the body can supply. … A movement is <em>possible</em>
when every margin exceeds one and <em>safe</em> with room to spare; aging and
injury shrink the numerators' headroom".

Quoted (line 97): "Sit-to-stand fails when the demanded torque exceeds the
available: a strength margin below one."

Fails part 1 (a precise statement) and part 2 (every term defined). Demand over
capacity exceeding one is exactly the failure condition, not the possibility
condition; and under that definition the numerator is the demand, which aging
raises rather than shrinking. Line 97 silently uses capacity over demand. The word
carries the §8 table's whole middle column, so the reader has to guess which sense
each row means. The balance margin is also called a ratio in the same sentence and
then defined as a distance.

Replacement for line 79:

```html
<p>The third recurring quantity is a <b>margin</b>: the ratio of what the body can supply to what the task demands. A <b>strength margin</b> is the maximum voluntary joint torque over the demanded torque; a <b>tissue margin</b> is the tissue's tolerance over the applied stress (Modules 2, 16). A movement is <em>possible</em> when every margin exceeds one and <em>safe</em> with room to spare, and aging or injury shrink the numerator, the capacity, while chair height, load distance, and speed set the denominator. The <b>balance margin</b> is the one exception to the ratio form: Module 10 defines it as a length, the distance of the extrapolated centre of mass inside the base of support, so its threshold is zero rather than one, and a movement is possible while it stays positive. Each case below reports its binding margin in whichever of the two forms the quantity has. With the template fixed, we turn it on the first movement of the day.</p>
```

Line 97's "Aging lowers the numerator's headroom" is then correct as written and
needs no change.

### B2. §4 analyses Module 1's stooped lift with a lighter upper body, so the same lift gives 3630 N here and 4040 N there

Location: `module13.html:119-135` (the whole of §4's prose and Proposition 4.1),
`module13.html:268-293` (Lab C), and downstream at `:344`, `:348`, `:386`, `:406`,
`:414`, `:429`, `:453`.

Quoted (line 125): "For a $20\ \mathrm{kg}$ load at $d_L=0.40\ \mathrm{m}$, trunk
mass $W_{\rm tr}=0.5mg$ at $d_{\rm tr}=0.30\ \mathrm{m}$, and $d_m=0.05\
\mathrm{m}$: $F_m\approx3630\ \mathrm{N}$ and $F_{\rm comp}\approx4200\
\mathrm{N}$ (a conservative upper bound - see the proof)".

`module01.html:365` sets up the identical scenario: "a box of $m_L=20\
\mathrm{kg}$ is held $r_L=0.40\ \mathrm m$ horizontally ahead of the L5/S1 disc …
and the upper body (head, arms, trunk) of mass $m_{\text{ub}}=0.60\,M=42\
\mathrm{kg}$ has its COM $r_t=0.30\ \mathrm m$ ahead of the disc. The erector
spinae … act through a moment arm of only $d_{\text{es}}=0.05\ \mathrm m$. All five
values are in the Appendix parameter table." Module 1 gets $F_{\text{es}}\approx
4040\ \mathrm N$ and, at the $\beta=60^\circ$ stoop, $C=4346\ \mathrm N$.

Factual error against the domain brief's running-example rule ("a scenario reused
in a later module uses the same symbols and the same parameter values as its first
appearance, or states why they differ"). Module 13 silently drops the upper body
from 0.60 M to 0.50 M and does not say why. Recomputing with Module 1's own values
(script `cascade.py`) gives $F_m=4041.7\ \mathrm N$ and $F_{\rm comp}=4345.8\
\mathrm N$, matching Module 1 exactly.

There is a second error inside the same passage. The proof evaluates the axial
weight term at $\cos\phi\le1$, an upright trunk, while the geometry it is
evaluating is a $60^\circ$ stoop with the load 0.40 m out. Module 1 evaluates
$\cos\beta$ at the actual stoop angle. Taking $\phi$ at its real value removes the
"conservative upper bound" hedge and makes §4 a determinate calculation.

The fix threads one further parameter through, which repairs B3 at the same time:
the trunk moment arm is not free, it is $d_{\rm tr}=\ell_t\sin\phi$ with $\ell_t=
0.346\ \mathrm m$ the along-trunk distance to the upper-body centre of mass
(`module01.html:695`). Posture then enters the formula, which is what §4's own
"squat, don't stoop" sentence claims and what the present Lab C does not compute.

Computed with `cascade.py` (all figures reproduced above from the Module 1 model):

| posture | $\phi$ | $d_{\rm tr}$ | $d_L$ | $F_m$ | $F_{\rm comp}$ |
|---|---|---|---|---|---|
| stoop | 60° | 0.300 m | 0.40 m | 4042 N | 4346 N |
| stoop, load pulled in | 60° | 0.300 m | 0.25 m | 3453 N | 3757 N |
| squat, load out | 20° | 0.118 m | 0.40 m | 2546 N | 3118 N |
| squat | 20° | 0.118 m | 0.25 m | 1957 N | 2529 N |

Replacement for Proposition 4.1 and its proof (lines 123 to 127):

```html
<div class="prop"><b>Proposition 4.1 (spinal compression in a lift).</b> Balancing moments about L5/S1, the erector spinae force and the resulting disc compression are
$$\boxed{\;F_m=\frac{W_{\rm tr}d_{\rm tr}+W_L d_L}{d_m},\qquad F_{\rm comp}=F_m+(W_{\rm tr}+W_L)\cos\phi,\;}$$
with $\phi$ the trunk's inclination from vertical and $d_{\rm tr}=\ell_t\sin\phi$, where $\ell_t$ is the fixed along-trunk distance from the disc to the upper body's centre of mass. Posture therefore enters through $\phi$ alone. Taking Module 1's values for the same lift (upper body $m_{\rm ub}=0.60M=42\ \mathrm{kg}$, so $W_{\rm tr}=412\ \mathrm{N}$; $\ell_t=0.346\ \mathrm{m}$; $d_m=0.05\ \mathrm{m}$), a $20\ \mathrm{kg}$ box at $d_L=0.40\ \mathrm{m}$ lifted from a $\phi=60^\circ$ stoop gives $d_{\rm tr}=0.30\ \mathrm{m}$, $F_m\approx4040\ \mathrm{N}$ and $F_{\rm comp}\approx4350\ \mathrm{N}$, reproducing <a href="module01.html#compression">Module 1 §6</a> exactly. The same box lifted from a $\phi=20^\circ$ squat with the load pulled to $d_L=0.25\ \mathrm{m}$ gives $F_{\rm comp}\approx2530\ \mathrm{N}$. The NIOSH (US National Institute for Occupational Safety and Health) action limit is $3400\ \mathrm{N}$: the stoop is well over it, the squat well under.</div>
<div class="proof">Take moments about the L5/S1 disc. The external flexing moments are $W_{\rm tr}d_{\rm tr}$ (trunk weight) and $W_L d_L$ (load); the erector spinae supplies the balancing extensor moment $F_m d_m$. Quasi-static balance $\sum M=0$ gives $F_m d_m=W_{\rm tr}d_{\rm tr}+W_L d_L$, hence $F_m=(W_{\rm tr}d_{\rm tr}+W_L d_L)/d_m$. The trunk's centre of mass sits a fixed distance $\ell_t$ along the trunk from the disc, so tipping the trunk $\phi$ from vertical puts it a horizontal distance $d_{\rm tr}=\ell_t\sin\phi$ ahead: standing up shortens that arm as $\sin\phi$, which is the whole of the squat's postural benefit. For the compression, resolve forces along the spine's long axis: the muscle force $F_m$ acts nearly parallel to the spine, and the upper body plus load contribute their axial component $(W_{\rm tr}+W_L)\cos\phi$, so the disc reaction is $F_{\rm comp}=F_m+(W_{\rm tr}+W_L)\cos\phi$. Substituting the stoop, $W_{\rm tr}=412\ \mathrm{N}$, $W_L=196\ \mathrm{N}$, $d_{\rm tr}=0.346\sin60^\circ=0.300\ \mathrm{m}$: $F_m=(412\times0.300+196\times0.40)/0.05=(123.6+78.5)/0.05\approx4040\ \mathrm{N}$, and $F_{\rm comp}=4040+608\times\cos60^\circ\approx4350\ \mathrm{N}$. Substituting the squat, $d_{\rm tr}=0.346\sin20^\circ=0.118\ \mathrm{m}$ and $d_L=0.25\ \mathrm{m}$: $F_m\approx1960\ \mathrm{N}$ and $F_{\rm comp}\approx2530\ \mathrm{N}$. Both moves matter, and the derivation says which is which: standing up shrinks $d_{\rm tr}$ as $\sin\phi$, pulling the load in shrinks $d_L$ directly. <span class="qed">∎</span>
</div>
```

Replacement for line 131 (which also repairs the "fivefold" of B7 below):

```html
<p>Four and a third kilonewtons (Fig. 5) is $6.3$ times body weight, pressed through one disc, to lift a box a fifth of body weight. The amplification is the lever ratio and nothing else: the load's own contribution to the muscle force is $d_L/d_m=8$ times its weight, the trunk's is $d_{\rm tr}/d_m=6$ times its weight, and the two sum to $F_m/W_L=20.6$ times the box's weight. Two everyday rules fall straight out of the formula, and the formula also ranks them. Keep the load close: $F_m$ is linear in $d_L$, and pulling the box from $0.40$ to $0.25\ \mathrm{m}$ at the same stoop cuts the compression from $4350$ to $3760\ \mathrm{N}$, a $14\%$ saving. Stand up: the trunk arm shrinks as $\sin\phi$, and coming from $60^\circ$ to $20^\circ$ with the box still at $0.40\ \mathrm{m}$ cuts it to $3120\ \mathrm{N}$, a $28\%$ saving. Posture buys twice what reach buys, and doing both, the squat lift, gives $2530\ \mathrm{N}$, a $42\%$ cut and the difference between clearly hazardous and comfortably safe. K3 sweeps the two together.</p>
```

Replacement for line 135:

```html
<p><b>Failure mode.</b> Lifting fails when disc compression (or shear) exceeds tissue tolerance: acute failure is disc herniation or, in osteoporotic bone (Module 2), a vertebral compression fracture; chronic overload is the mechanics behind much low-back pain. Tolerance falls with age as discs dehydrate and bone thins, while the demand is set by load, distance, and posture - which is why safe-lifting guidance is entirely about shrinking $d_L$ and $\phi$, and why a young back tolerating a careless stoop lift is running the same $4350\ \mathrm{N}$ that fractures an old one.</p>
```

The Fig. 5 caption (line 129) must carry the new number:

```html
<figcaption>Lifting and the low back. Bent forward at $\phi$ from vertical, the upper-body weight $W_{\rm tr}$ acts at arm $d_{\rm tr}=\ell_t\sin\phi$ and the load $W_L$ at arm $d_L$ about the L5/S1 disc; the erector spinae, at a short arm $d_m\approx5\ \mathrm{cm}$, must balance them, so $F_m=(W_{\rm tr}d_{\rm tr}+W_L d_L)/d_m$ is large and the disc is compressed to $\approx4350\ \mathrm{N}$ lifting $20\ \mathrm{kg}$ from a $60^\circ$ stoop - above the $3400\ \mathrm{N}$ NIOSH limit. Squatting ($\phi=20^\circ$, load pulled to $0.25\ \mathrm{m}$) brings it to $\approx2530\ \mathrm{N}$.</figcaption>
```

The downstream numbers change with it. D3 (`:386`) gains the $d_{\rm tr}=\ell_t
\sin\phi$ step; D8 and K3 (`:406`, `:429`) get safe loads of $35.0$ kg squatting
and $8.7$ kg stooping instead of 17 and 9 (the 8.7 kg reproduces
`module01.html:691` exactly); D10 and K9 (`:414`, `:453`) get a lean of $0.071$ m
instead of 0.09, because the lean is $W_bd_b/W_{\rm tr}$ and $W_{\rm tr}$ changed.
The replacements are written out under B3, B8 and B9 below.

### B3. Lab C declares a squat/stoop comparison, then computes it with the posture held fixed, at a third squat distance

Location: `module13.html:268-293`.

Quoted (line 268, Parameters): "trunk $0.5m$ at $d_{\rm tr}=0.30\ \mathrm{m}$,
muscle arm $d_m=0.05\ \mathrm{m}$; load $10$-$25\ \mathrm{kg}$; load distance
$d_L$ from $0.20$ (squat) to $0.55\ \mathrm{m}$ (stoop)."

The code at line 275 sweeps `dL = np.linspace(0.22, 0.55, 40)` and the printed
"squat" number at line 283 is evaluated at `0.25`. Three different squat
distances are given for one quantity in one lab: 0.20 in the parameters, 0.22 in
the sweep, 0.25 in the print. The choice decides the lab's headline claim:
computed, a 20 kg load gives 3385 N at $d_L=0.20$ (under the NIOSH limit) and
3581 N at $d_L=0.25$ (over it), so the caption's "over the 3400 N NIOSH limit even
squatting" is true only for the distance the parameters do not name. The stated
load range 10 to 25 kg is also not the range the code runs, which is 10 and 20.

Worse, the lab holds `d_tr = 0.30` for both postures, so the squat/stoop contrast
it computes is entirely a change of reach. §4's own prose (line 131) attributes
half the benefit to the trunk arm. The lab therefore does not compute the
mechanism the section claims. Fails part 3 (the proof in the smallest setting that
shows the mechanism) and part 5 (a tie to something concrete: the number does not
tie to the stated model).

Replacement for lines 268 to 293. The code was run; every number below is from its
output.

```html
<p><b>Physical question.</b> How does spinal compression vary from a squat to a stoop, and where does it cross the safety limit? <b>Model.</b> Proposition 4.1, with posture entering through $\phi$ via $d_{\rm tr}=\ell_t\sin\phi$. <b>Parameters.</b> Upper body $0.60m=42\ \mathrm{kg}$ (Module 1) at along-trunk distance $\ell_t=0.346\ \mathrm{m}$, muscle arm $d_m=0.05\ \mathrm{m}$; load $10$ and $20\ \mathrm{kg}$; trunk angle $\phi=20^\circ$ (squat) and $60^\circ$ (stoop); load distance $d_L$ from $0.20$ to $0.55\ \mathrm{m}$. <b>Equations.</b> $F_{\rm comp}=(W_{\rm tr}\ell_t\sin\phi+W_L d_L)/d_m+(W_{\rm tr}+W_L)\cos\phi$.</p>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np
import matplotlib.pyplot as plt

g, m, d_m, NIOSH = 9.81, 70.0, 0.05, 3400.0
W_tr = 0.60*m*g                           # Module 1 upper-body fraction
ell_t = 0.30/np.sin(np.radians(60))       # along-trunk COM distance
dL = np.linspace(0.20, 0.55, 40)


def comp(mL, dL, phi_deg):
    c, s = np.cos(np.radians(phi_deg)), np.sin(np.radians(phi_deg))
    return (W_tr*ell_t*s + mL*g*dL)/d_m + (W_tr + mL*g)*c


for mL in (10, 20):
    for phi in (20, 60):
        plt.plot(dL, comp(mL, dL, phi),
                 label='%d kg, %d deg' % (mL, phi))
        print('%2d kg at %2d deg: %4.0f N at dL=0.20, %4.0f N at dL=0.55'
              % (mL, phi, comp(mL, 0.20, phi), comp(mL, 0.55, phi)))
plt.axhline(NIOSH, ls='--')
plt.xlabel('load distance dL (m)')
plt.ylabel('spinal compression (N)')
plt.legend()
plt.show()</code></pre></div>
```

Output, and therefore the caption and interpretation:

```
10 kg at 20 deg: 1848 N at dL=0.20, 2535 N at dL=0.55
10 kg at 60 deg: 3120 N at dL=0.20, 3806 N at dL=0.55
20 kg at 20 deg: 2333 N at dL=0.20, 3706 N at dL=0.55
20 kg at 60 deg: 3561 N at dL=0.20, 4934 N at dL=0.55
```

```html
<figcaption>Lab C. Spinal compression against load distance for four postures. Posture separates the pairs and reach tilts each line: a 20 kg box costs 2333 N squatting with the load in and 4934 N stooping with it out, and the $60^\circ$ stoop is already over the 3400 N NIOSH limit at the closest reach the lab draws (3561 N at $d_L=0.20$ m), while the $20^\circ$ squat stays under it until $d_L=0.47$ m. The amplifier is the 5 cm muscle arm; posture and reach are the two arms it multiplies.</figcaption>
```

```html
<p><b>Interpretation.</b> Posture separates the four lines into two pairs and reach tilts each one. A $20\ \mathrm{kg}$ box costs $2333\ \mathrm{N}$ squatting with the load in and $4934\ \mathrm{N}$ stooping with it out; the $60^\circ$ stoop is over the $3400\ \mathrm{N}$ limit even at the closest reach the lab draws ($3561\ \mathrm{N}$ at $d_L=0.20\ \mathrm{m}$), while the $20^\circ$ squat stays under it until $d_L=0.47\ \mathrm{m}$. <b>Sensitivity.</b> The slope in $d_L$ is $W_L/d_m$, so for the $20\ \mathrm{kg}$ box every centimetre the load moves out adds $39\ \mathrm{N}$ of erector spinae force ($20\ \mathrm{N}$ for the $10\ \mathrm{kg}$ box); the slope in posture is $W_{\rm tr}\ell_t\cos\phi/d_m$, which at $\phi=60^\circ$ is $1430\ \mathrm{N}$ per radian, or $25\ \mathrm{N}$ per degree of stoop. The tiny $5\ \mathrm{cm}$ muscle arm is the amplifier in both. <b>Failure mode.</b> Crossing tissue tolerance - lower in aged discs and osteoporotic bone. <b>Extension.</b> Add intra-abdominal pressure as a second extensor moment and quantify how much it offloads the discs.</p>
```

(The posture slope was computed as $W_{\rm tr}\ell_t\cos60^\circ/d_m =
412.0\times0.346\times0.5/0.05 = 1426\ \mathrm{N\,rad^{-1}} = 24.9\
\mathrm{N\,deg^{-1}}$.)

### B4. Lab A declares a dynamic model it never runs, and its conclusion is the opposite sign to K8's

Location: `module13.html:219` (the Model and Parameters), `module13.html:241`
(the Extension).

Quoted (line 219): "<b>Model.</b> Proposition 2.1 for the quasi-static torque; a
point-mass COM raised by $H$ in time $T$ for the dynamic version, whose peak
vertical ground reaction sets the extra torque. <b>Parameters.</b> … rise height
$H=0.40\ \mathrm{m}$, $T=1.2\ \mathrm{s}$. <b>Equations.</b> $\tau=m_{\rm up}gd$;
dynamic vGRF $\approx m(g+a)$."

The code at lines 221 to 237 contains no $H$, no $T$, no $a$, and no dynamic term.
It computes $\tau=m_{\rm up}gd$ and nothing else. The lab's own physical question
("how much does trunk-flexion momentum lower the peak?") is never answered.

Quoted (line 241): "<b>Extension.</b> Add the dynamic momentum term: a brisk rise
($T=0.9\ \mathrm{s}$) needs peak vGRF $\approx1.3\ \mathrm{BW}$ but front-loads it
into the momentum phase, lowering the extension-phase torque - quantify the
trade."

K8 (line 449) computes the same model and finds the opposite: "the brisk rise
peaks higher at $\approx128\ \mathrm{N\,m}$ … so speed costs a higher transient
torque". Verified: on a minimum-jerk path the peak acceleration is
$(10/\sqrt3)H/T^2$, giving 1.16 BW at $T=1.2$ s and 1.29 BW at $T=0.9$ s, and knee
torques of 127.8 and 141.8 N m against the quasi-static 109.9. A brisk vertical
rise costs more torque, not less. `\Delta t` also appears nowhere. Fails part 1
and part 4 (the rescue case is asserted in the direction the model refutes).

Also, "vGRF" is used without expansion (B14).

Replacement for line 219:

```html
<p><b>Physical question.</b> How does the required knee torque depend on chair height, and where does it cross the strength a person has? <b>Model.</b> Proposition 2.1, quasi-static. <b>Parameters.</b> $m=70\ \mathrm{kg}$, $m_{\rm up}=0.8m$ (assumed, Appendix), knee-to-COM distance $d$ from $0.15$ to $0.28\ \mathrm{m}$ (high firm chair to low soft one); available peak knee extensor torque taken as $1.5\ \mathrm{N\,m}$ per kg of body mass for an older adult (Appendix). <b>Equations.</b> $\tau=m_{\rm up}gd$; the ceiling is $\tau_{\max}=1.5m$. The dynamic case, where a brisk rise adds $m_{\rm up}a_zd$, is K8; this lab is the static envelope it perturbs.</p>
```

Replacement for the Extension sentence in line 241 (the rest of the paragraph is
correct and stays):

```html
<b>Extension.</b> K8 adds the vertical inertial term and finds it a cost, not a saving: on a minimum-jerk path the peak torque rises from $110$ to $128\ \mathrm{N\,m}$ at $T=1.2\ \mathrm{s}$ and to $142\ \mathrm{N\,m}$ at $T=0.9\ \mathrm{s}$. The flexion-momentum benefit is a different mechanism - horizontal trunk momentum redirected into the rise - and it needs the coupled two-segment model this lab does not build. Extend the code to sweep $T$ and plot the two effects on one axis.
```

The code block gets one added line so that the caption's numbers appear in the
output rather than only on the plot (see B5):

```python
print("d=0.15 m: %.0f N m; d=0.28 m: %.0f N m; crossing at d=%.3f m"
      % (m_up*g*0.15, m_up*g*0.28, tau_max/(m_up*g)))
```

Run: `d=0.15 m: 82 N m; d=0.28 m: 154 N m; crossing at d=0.191 m`.

### B5. The module claims four times that its computational solutions carry code; no computational problem has any

Location: `module13.html:216`, `:330`, `:417`, `:524`.

Quoted (line 330): "computational solutions quote numbers the code produces."
Quoted (line 417): "Numbers quoted are those the code produces."
Quoted (line 524): "every proposition proved, every figure computed, every number
reproduced by the code shown."
Quoted (line 216): "every plotted number was produced by the code shown."

The file contains four `<pre><code>` blocks, all in §9. K1 through K10 have none.
This is the defect class the domain brief names ("A module can claim 'every number
was produced by running the code' while its lab prints nothing"). Line 216 is also
false of the labs themselves: Lab A's 82, 154 and 0.19 and Lab D's 1.72 appear in
captions and interpretations but are printed by no code.

The fix is to write the code, not to withdraw the claim. Ten blocks were written,
run and linted (`kcode.py` → `kblocks/*.py`; `pycodestyle` clean). Each is spliced
into its solution inside a `<div class="codewrap">` with the module's existing copy
button, in the shape §9 already uses. The blocks and their output are given under
B6, B8, B9 and B13 where they change a stated number, and are listed in §6 by tag
otherwise. Lab A gains the print line of B4; Lab D gains

```python
print("max recoverable speed with no delay: %.2f m/s" % (w0*(max_step - x0)))
```

which prints `max recoverable speed with no delay: 1.72 m/s`.

### B6. K2's sensitivity claim is backwards

Location: `module13.html:425`.

Quoted: "the sensitivity $\partial f_{\max}/\partial m=-250/(m^2gh)$ steepens at
low power ceilings."

Factual error. $f_{\max}=P/(mgh)$, so $\partial f_{\max}/\partial m=-P/(m^2gh)$:
the magnitude is directly proportional to the ceiling. Computed at 70 kg:
0.0184 steps/s per kg at $P=150$ W, 0.0306 at 250 W, 0.0489 at 400 W. The
sensitivity steepens at *high* ceilings. Writing the constant 250 inside a
derivative also hides the dependence that the sentence is about.

Replacement for the K2 solution (line 421 to 425), with its code:

```html
<details class="sol"><summary>Solution</summary><div><p>From $P=mghf$, the maximum cadence at a ceiling $P$ is $f_{\max}=P/(mgh)$. At $P=250\ \mathrm{W}$ and $h=0.17\ \mathrm{m}$ this is $2.14\ \mathrm{steps/s}$ at $70\ \mathrm{kg}$ but only $1.67\ \mathrm{steps/s}$ at $90\ \mathrm{kg}$: a $29\%$ mass increase costs $22\%$ of cadence, which is why load carriage and obesity slow stair climbing measurably. The sensitivity is $\partial f_{\max}/\partial m=-P/(m^2gh)$, proportional to the ceiling itself: at $70\ \mathrm{kg}$ it is $0.018\ \mathrm{steps\,s^{-1}kg^{-1}}$ for a $150\ \mathrm{W}$ ceiling and $0.049$ for a $400\ \mathrm{W}$ one. A fit climber therefore loses more absolute cadence per added kilogram than a frail one, while both lose the same $1\%$ of cadence per $1\%$ of mass, since the relative sensitivity $\mathrm{d}\ln f_{\max}/\mathrm{d}\ln m=-1$ is independent of $P$. That distinction is the point: the fractional cost of carrying weight upstairs is a property of the geometry, not of the climber.</p>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np

g, h, P = 9.81, 0.17, 250.0
mass = np.array([50.0, 70.0, 90.0, 110.0])
f_max = P/(mass*g*h)
for mb, f in zip(mass, f_max):
    print("m = %5.1f kg -> f_max = %.3f steps/s" % (mb, f))
print("70 -> 90 kg: mass +%.1f%%, cadence %.1f%%"
      % (100*(90-70)/70, 100*(f_max[2]-f_max[1])/f_max[1]))
for Pc in (150.0, 250.0, 400.0):
    print("ceiling %5.1f W -> |df_max/dm| at 70 kg = %.4f steps/s per kg"
          % (Pc, Pc/(70.0**2*g*h)))</code></pre></div></div></details>
```

Output:

```
m =  50.0 kg -> f_max = 2.998 steps/s
m =  70.0 kg -> f_max = 2.142 steps/s
m =  90.0 kg -> f_max = 1.666 steps/s
m = 110.0 kg -> f_max = 1.363 steps/s
70 -> 90 kg: mass +28.6%, cadence -22.2%
ceiling 150.0 W -> |df_max/dm| at 70 kg = 0.0184 steps/s per kg
ceiling 250.0 W -> |df_max/dm| at 70 kg = 0.0306 steps/s per kg
ceiling 400.0 W -> |df_max/dm| at 70 kg = 0.0489 steps/s per kg
```

### B7. Two statements of the same lever sensitivity, both wrong

Location: `module13.html:293` (Lab C) and `module13.html:344` (C3).

Quoted (line 293): "every centimetre the load moves out adds $W_L/d_m\approx4\
\mathrm{N}$ of muscle force per newton-metre of extra moment."

Quoted (line 344): "the muscle arm $d_m\approx5\ \mathrm{cm}$ is tiny, so the load
term $W_Ld_L/d_m$ amplifies the load's moment about fortyfold per metre."

Factual errors, and the sentence at 293 also mixes two quantities. Computed:
$W_L/d_m = 3924\ \mathrm{N\,m^{-1}}$ for the 20 kg box, so one centimetre of
extra reach costs $39.2\ \mathrm{N}$ of muscle force, not 4; and $1/d_m = 20$ per
metre, not forty. Line 293's replacement is inside B3. Replacement for the C3
solution (line 344):

```html
<details class="sol"><summary>Solution</summary><div>Spinal compression is dominated by the erector spinae force $F_m=(W_{\rm tr}d_{\rm tr}+W_Ld_L)/d_m$, and the muscle arm $d_m\approx5\ \mathrm{cm}$ is tiny, so every newton-metre of extra external moment costs $1/d_m=20\ \mathrm{N}$ of muscle force. For a $20\ \mathrm{kg}$ box that is $W_L/d_m=3924\ \mathrm{N}$ per metre of reach, or $39\ \mathrm{N}$ for every centimetre the load drifts away from the body. Halving the horizontal load distance $d_L$ halves the load's whole contribution to the muscle force and, with it, most of the compression. The one change that competes with it is standing up, which shrinks the <em>other</em> arm as $d_{\rm tr}=\ell_t\sin\phi$; K3 sweeps the two together and finds posture the larger lever at the geometry of §4. Neither is a matter of strength: the compression is set by geometry, and $d_L$ is the piece of geometry the lifter controls with the least effort.</div></details>
```

Line 344's "No other single change - not strength, not a back belt - moves the
compression as much" is deleted with it: K3 now computes that posture moves it
more.

### B8. K10 asks which task fails first and computes one threshold, then asserts the order of the rest

Location: `module13.html:455-457`.

Quoted: "The chair rise (demand $110\ \mathrm{N\,m}$ from a standard seat) is
crossed first, at $\approx63\%$ of young strength; stair ascent power and descent
control follow as strength falls further."

Fails part 3 and part 5. The problem's whole content is the ordering, and the
ordering is asserted. No demand is computed for stair ascent or for descent
control, so "follow" rests on nothing; and the 63% figure, which is right
(109.87/175 = 62.8%), is the threshold for the *standard* chair, while §2's own
point is that the low chair is what defeats people.

Computed (`kblocks/K10.py`), scaling both reserves by one factor:

```
rise from a low chair (d = 0.28 m)       fails at 87.9% of the young reserve
climb stairs at 1.8 steps/s              fails at 84.1% of the young reserve
rise from a standard chair (d = 0.20 m)  fails at 62.8% of the young reserve
walk a 10 deg slope at 1.0 m/s           fails at 47.7% of the young reserve
rise from a high firm chair (d = 0.15 m) fails at 47.1% of the young reserve
```

Replacement for the K10 statement and solution:

```html
<div class="prob"><p><b>K10 - which task fails first? (multi-margin sweep).</b> Scale a young adult's two leg reserves - peak knee extensor torque $2.5\ \mathrm{N\,m/kg}$ and sustained leg power $250\ \mathrm{W}$ - down by a common factor, and compute the factor at which each everyday task's margin reaches one. Which task is the first casualty, and does the answer depend on the chair? <span class="probes">Probes: shared reserves and the ordering of thresholds; Section 8.</span></p>
```

```html
<details class="sol"><summary>Solution</summary><div><p>Assume the two reserves decline together by a common factor $s$; that is a modelling assumption, not a result, and it is what lets a torque-limited task and a power-limited one be ranked on one axis. Each task fails when $s$ falls to its demand divided by the young reserve. The low chair goes first at $s=0.88$, stair climbing at habitual cadence next at $0.84$, the standard chair at $0.63$, and only near half strength do the gentle slope ($0.48$) and the high firm chair ($0.47$) fail. Two things follow. The first casualty is not "rising from a chair" but rising from a <em>particular</em> chair: the same person with the same legs keeps the high stool for another forty percent of decline after the low sofa is lost, which is why §2's advice is about the furniture and not only about the quadriceps. And the two tasks at the top of the list, the low chair and the stairs, are separated by four points of reserve, so a person who has just started avoiding the sofa is already close to slowing on the stairs - the shared-reserve effect of §8 made into a schedule.</p>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np

g, m, m_up, h = 9.81, 70.0, 0.8*70.0, 0.17
tau_young, P_young = 2.5*m, 250.0             # young reserves
tasks = (("rise from a low chair (d = 0.28 m)", m_up*g*0.28, tau_young),
         ("climb stairs at 1.8 steps/s", m*g*h*1.8, P_young),
         ("rise from a standard chair (d = 0.20 m)", m_up*g*0.20, tau_young),
         ("walk a 10 deg slope at 1.0 m/s",
          m*g*1.0*np.sin(np.radians(10)), P_young),
         ("rise from a high firm chair (d = 0.15 m)", m_up*g*0.15,
          tau_young))
order = sorted(tasks, key=lambda t: -t[1]/t[2])
for name, demand, reserve in order:
    print("%-40s fails at %4.1f%% of the young reserve "
          "(demand %5.1f of %5.1f)"
          % (name, 100*demand/reserve, demand, reserve))</code></pre></div></div></details></div>
```

### B9. K3 is D8 restated word for word

Location: `module13.html:406` (D8) and `module13.html:429` (K3).

D8's solution ends: "The safe load falls as $\sim1/d_L$: with $F_{\rm lim}=3400\
\mathrm{N}$ it is $\approx17\ \mathrm{kg}$ close ($d_L=0.25$) and $\approx9\
\mathrm{kg}$ at arm's length ($d_L=0.50$)."

K3's solution is the same inversion with the same two numbers. A derivational
problem and a computational one cannot be the same problem, and the domain brief's
K-depth standard rules out a computational problem that only evaluates a formula
the derivational set has already inverted. K3's own statement names a sweep ("as a
function of load distance") and a regime contrast that it never runs.

Both numbers also change under B2. Recomputed with Module 1's upper body: the safe
load is $35.0$ kg squatting ($\phi=20^\circ$, $d_L=0.25$ m) and $8.7$ kg stooping
($60^\circ$, $0.40$ m); the 8.7 kg reproduces `module01.html:691`.

Replacement for D8's last sentence:

```html
The safe load falls roughly as $1/d_L$ at fixed posture, and as $1/\sin\phi$ in the trunk term: with $F_{\rm lim}=3400\ \mathrm{N}$ it is $\approx35\ \mathrm{kg}$ squatting ($\phi=20^\circ$, $d_L=0.25\ \mathrm{m}$) and only $\approx8.7\ \mathrm{kg}$ stooping ($\phi=60^\circ$, $d_L=0.40\ \mathrm{m}$), the same $8.7\ \mathrm{kg}$ Module 1 derives for this lift. K3 sweeps the two arms jointly.
```

Replacement for K3, which becomes the two-parameter sweep its statement promises:

```html
<div class="prob"><p><b>K3 - the safe-lift envelope (two-parameter sweep).</b> Sweep trunk angle $\phi$ and load distance $d_L$ jointly and compute the largest load that keeps spinal compression under the $3400\ \mathrm{N}$ limit on each. Which single move buys more, standing up or pulling the box in, and where do the two together change the answer by a factor rather than a fraction? <span class="probes">Probes: a two-parameter safety boundary that separates posture from reach; Section 4.</span></p>
```

```html
<details class="sol"><summary>Solution</summary><div><p>Inverting Proposition 4.1 at $F_{\rm comp}=F_{\rm lim}$ gives $W_L^{\max}=\big[F_{\rm lim}-W_{\rm tr}(\ell_t\sin\phi/d_m+\cos\phi)\big]\big/\big(d_L/d_m+\cos\phi\big)$, a surface over the two arms rather than a curve over one. Across the grid the safe load runs from $35.0\ \mathrm{kg}$ at the squat corner ($\phi=20^\circ$, $d_L=0.25\ \mathrm{m}$) to $6.4\ \mathrm{kg}$ at the deep-stoop corner ($60^\circ$, $0.55\ \mathrm{m}$). Taken one at a time from the $60^\circ$, $0.40\ \mathrm{m}$ stoop, standing to $20^\circ$ raises the safe load from $8.7$ to $23.2\ \mathrm{kg}$ and pulling the box in to $0.25\ \mathrm{m}$ raises it to $13.4\ \mathrm{kg}$: posture buys roughly twice what reach buys, because the trunk's own $412\ \mathrm{N}$ acts at an arm that collapses as $\sin\phi$ while the load's arm falls only in proportion to itself. Together they give $35.0\ \mathrm{kg}$, four times the stoop value. That is the quantitative form of "squat, don't stoop": not a fractional improvement but a change of what the lift <em>is</em>, and it is why safe-lifting guidance leads with posture and not with strength.</p>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np

g, m, d_m, F_lim = 9.81, 70.0, 0.05, 3400.0
W_tr = 0.60*m*g
ell_t = 0.30/np.sin(np.radians(60))       # along-trunk COM distance


def safe_load(dL, phi_deg):
    c = np.cos(np.radians(phi_deg))
    d_tr = ell_t*np.sin(np.radians(phi_deg))
    return (F_lim - W_tr*(d_tr/d_m + c))/(dL/d_m + c)


for phi in (20, 40, 60):
    row = [safe_load(dL, phi)/g for dL in (0.25, 0.40, 0.55)]
    print("phi=%2d deg: safe load %5.1f / %5.1f / %5.1f kg "
          "at dL = 0.25 / 0.40 / 0.55 m" % (phi, row[0], row[1], row[2]))
print("squat (20 deg, 0.25 m) buys %.1fx the stoop (60 deg, 0.40 m)"
      % (safe_load(0.25, 20)/safe_load(0.40, 60)))</code></pre></div></div></details></div>
```

Output:

```
phi=20 deg: safe load  35.0 /  23.2 /  17.4 kg at dL = 0.25 / 0.40 / 0.55 m
phi=40 deg: safe load  22.1 /  14.5 /  10.8 kg at dL = 0.25 / 0.40 / 0.55 m
phi=60 deg: safe load  13.4 /   8.7 /   6.4 kg at dL = 0.25 / 0.40 / 0.55 m
squat (20 deg, 0.25 m) buys 4.0x the stoop (60 deg, 0.40 m)
```

### B10. The momentum strategy is asserted in §2 and deferred in all three places that should prove it

Location: `module13.html:95` (assertion), `:241` (Lab A), `:402` (D7), `:449`
(K8).

Quoted (line 95): "the <b>momentum strategy</b> is not a stylistic quirk but a
torque-reducing necessity: pitching the trunk forward first gives the COM an
upward-forward velocity at seat-off, so part of the body's rise is already underway
and the legs need supply only a fraction of the full quasi-static torque."

Quoted (D7, line 402): "the extensor impulse need only make up the shortfall
$m\,\Delta v-m\dot x_0$ … (The full reduction requires the coupled two-segment
model; the point here is the momentum offset.)"

K8 defers it too ("needs the coupled two-segment model of the extension"). The
claim is made once and deferred three times, so it is never earned. D7's statement
is also imprecise in a way that hides the gap: $\Delta v$ is never defined, and the
sentence calls the momentum "upward-forward" and then writes it as the horizontal
component $\dot x_0$.

Fails part 3. The mechanism *is* provable in the smallest setting, in one
paragraph, and the module should do it rather than promise it. Replacement for D7:

```html
<details class="sol"><summary>Solution</summary><div><p>Work in the vertical direction and treat the body above the knees as a point mass $m_{\rm up}$ that must be raised through $H$ and arrive at rest. Let the extension phase begin at seat-off with upward velocity $v_0$ and last a time $T_e$. Vertical impulse-momentum over the extension phase gives $\int_0^{T_e}\!\big(F_z-m_{\rm up}g\big)\,dt=m_{\rm up}(0-v_0)=-m_{\rm up}v_0$, so the extra ground impulse the legs must supply beyond holding the weight is reduced by exactly $m_{\rm up}v_0$: the momentum the flexion phase already put into the body is momentum the extensors do not have to create. Equivalently in energy, the rise needs $m_{\rm up}gH$ of work and the flexion phase has already delivered $\tfrac12m_{\rm up}v_0^2$ of it, so the extensors supply $m_{\rm up}gH-\tfrac12m_{\rm up}v_0^2$. With $m_{\rm up}=56\ \mathrm{kg}$, $H=0.40\ \mathrm{m}$ and a modest $v_0=0.25\ \mathrm{m/s}$, that is $220-1.8=218\ \mathrm{J}$ against $220\ \mathrm{J}$: the energy saving is under one percent, and the real saving is in the <em>impulse</em>, $m_{\rm up}v_0=14\ \mathrm{N\,s}$ against the $m_{\rm up}gT_e\approx 220\ \mathrm{N\,s}$ of a $0.4\ \mathrm{s}$ extension, about six percent. So the flexion phase buys a small direct reduction, and the larger part of the strategy is geometric: pitching the trunk forward moves the centre of mass toward the feet and shrinks $d$ in $\tau=m_{\rm up}gd$, which is a first-order effect on torque. Quantifying the transfer of <em>horizontal</em> trunk momentum into the rise needs the coupled two-segment model; this module does not build it, and §2's claim should be read as the geometric effect plus this six percent, not more.</p></div></details>
```

And line 95's clause is rewritten so the module claims only what it proves:

```html
And the <b>momentum strategy</b> is not a stylistic quirk: pitching the trunk forward before seat-off does two mechanical things, and D7 separates them. It moves the centre of mass toward the feet, shrinking $d$ in $\tau_{\rm knee}=m_{\rm up}gd$, which is a first-order reduction; and it gives the body upward momentum $m_{\rm up}v_0$ that the extensors then do not have to create, which D7 computes at about six percent of the extension impulse. The often-quoted third effect, transferring the trunk's <em>horizontal</em> momentum into the rise, needs a coupled two-segment model this module does not build, and is not claimed here.
```

### B11. §0 and §1 never place the module's models on the level ladder, and §8 never says what the reader can now do

Location: `module13.html:57` (the thesis box), `module13.html:212` (the close).

The domain brief requires each module to state which level its models sit on, and
names both "a motivation section that names the phenomenon but not the question the
module answers" and "a closing section that does not say what the reader can now
do" as known defect classes. §0 states the thesis well but never says the models
are Level 1 statics with one Level 2 excursion; a reader meeting
$\tau_{\rm knee}=m_{\rm up}gd$ has no way to know how much of a chair rise it is
meant to capture. §8 ends on an observation about frailty and hands over to
Module 14 without a "you can now" sentence.

Insert after the thesis box (line 57):

```html
<p><b>Where these models sit.</b> Every case in this module is a Level 1 model in the course's sense: one or two rigid segments, a single equilibrium or conservation law, closed-form arithmetic, and parameters taken from the reference human. Sections 2, 4, 6 and 7 are quasi-static, so they drop inertial terms entirely; Sections 3 and 5 are Level 1 dynamic, using work-energy and impulse-momentum without integrating an equation of motion. Only K8 steps to Level 2, integrating a prescribed trajectory to recover the inertial correction the quasi-static estimates omit, and it finds that correction to be sixteen percent at an ordinary rise speed. Nothing here is inverse dynamics (Module 8), a muscle model (Module 5), or a controller (Module 12); the point of a Level 1 pass is that it already puts a number on every task of the day, and names which of them run close to a limit. Where a case needs more, the section says which module supplies it.</p>
```

Insert at the end of §8 (after line 212):

```html
<p><b>What the reader can now do.</b> Given any everyday movement, you can now run the pipeline of Definition 1 on it unaided: idealize it to one or two segments, choose between moment balance and an impulse or energy law by asking whether the accelerations matter, put the reference human's masses and moment arms in, and get a joint torque, a spinal load, a required impulse, or a required step length with its units right. You can then convert that demand into a margin against a stated capacity, invert the relation to find the threshold value of the parameter the person or the furniture controls, and say which reserve has to fall, and by how much, before the movement becomes impossible. The problem set exercises exactly this: C1 to C10 ask which lever a familiar piece of advice is pulling, D1 to D10 rebuild each result from its balance law, and K1 to K10 sweep, invert, and optimise the margins the sections estimate. Module 14 supplies the biology of why the reserves fall; this module is what they fall against.</p>
```

### B12. Two symbols carry two meanings each

Location: `module13.html:175`, `:364` (the letter $d$); `module13.html:167`,
`:437` (the letter $\mu$); Appendix `:499`, `:505`.

The Appendix (line 499) defines $d$ as "horizontal knee-to-COM distance at
seat-off", §2's meaning. §6 then writes "the hand's force $F_{\rm hand}$ at
distance $d$ from the hinge" and C8 repeats it, so one letter is a chair geometry
and a door geometry within four sections. §1's indexed $d_i$ and $d_{\rm muscle}$
are generic and cause no collision.

The Appendix (line 505) defines $\mu$ as skin-lid friction. K5 uses the same letter
for shoe-floor friction, a different contact with a different value in general
(they happen to be given the same 0.7 here, which hides the collision rather than
excusing it).

The domain brief makes a cross-section collision a defect. Rename: the door arm
becomes $d_{\rm hinge}$ (§6 line 175, C8 line 364), and the two frictions become
$\mu_{\rm lid}$ (§6, C7, K6) and $\mu_{\rm shoe}$ (K5). Both go in the notation
table with their sections. The full replacement strings are listed in §6 by tag.

### B13. §6 assumes $\mu=0.7$ for the contact K6 gives $\mu=0.5$

Location: `module13.html:167`, `:173`, `:441`.

Quoted (line 167): "For $\tau_{\rm resist}=2\ \mathrm{N\,m}$, $r=0.035\
\mathrm{m}$, $\mu=0.7$: a tangential force of $\approx57\ \mathrm{N}$ around the
rim, needing a grip force of $\approx82\ \mathrm{N}$."

Quoted (line 441, K6): "bare hand ($\mu=0.5$, $r=0.035\ \mathrm{m}$) gives $1.05\
\mathrm{N\,m}$".

Both arithmetic checks (81.63 N and 1.05 N m), but the same physical contact, a
bare hand on a lid, is given two friction coefficients three sections apart with no
word about it, and §6's own worked threshold at line 173 ("trivial at $150\
\mathrm{N}$ of grip and impossible at $60\ \mathrm{N}$") uses 0.7 while K6 uses
0.5 for the same 60 N grip and reaches the same verdict by a different route. The
Appendix records the range 0.5 to 1.0 without saying which end is which contact.

The fix states the range and its ends once, in §6, and makes 0.7 the labelled
mid-value. Replacement for the sentence at line 167:

```html
so opening a lid that resists with $\tau_{\rm resist}$ requires $F_{\rm grip}\ge\tau_{\rm resist}/(\mu_{\rm lid} r)$. Skin on a lid runs from about $\mu_{\rm lid}=0.5$ (dry skin on smooth steel) to about $1.0$ (a rubber pad); take the mid-range $0.7$ for the worked number and let K6 work the ends. For $\tau_{\rm resist}=2\ \mathrm{N\,m}$, $r=0.035\ \mathrm{m}$, $\mu_{\rm lid}=0.7$: a tangential force of $\approx57\ \mathrm{N}$ around the rim, needing a grip force of $\approx82\ \mathrm{N}$.
```

and for the threshold sentence at line 173:

```html
The task is grip-limited, and grip strength is among the first capacities to fall with age and the worst hit by hand arthritis - so a stuck jar is a threshold task: at the mid-range $\mu_{\rm lid}=0.7$ a $150\ \mathrm{N}$ grip delivers $3.7\ \mathrm{N\,m}$ and opens the lid easily, while a $60\ \mathrm{N}$ grip delivers $1.5\ \mathrm{N\,m}$ and does not. On dry skin at $\mu_{\rm lid}=0.5$ that same $60\ \mathrm{N}$ grip delivers only $1.05\ \mathrm{N\,m}$ (K6), which is why the aid, not the effort, is what changes the outcome.
```

Line 173's closing clause "which is why grip strength is a validated proxy for
whole-body frailty" is moved to the style edits (S1): it is an empirical claim the
module cannot derive.

### B14. Eighteen numbers used in the text are in no table, and four abbreviations are never expanded

Location: the parameter table at `module13.html:509-520`; the notation table at
`:495-506`.

The domain brief's rule is that every number is derived, is a table parameter with
its symbol and unit, or is labelled an assumption. The following are none of the
three: $m_{\rm up}=0.8m$ (B15); the upper-body fraction and $\ell_t$ (now
Module 1's, B2); trunk angles $20^\circ$ and $60^\circ$; load distances 0.25 and
0.55 m; walking speed $1.3\ \mathrm{m\,s^{-1}}$; turn angle $60^\circ$; lid radius
0.035 m and wrench radius 0.060 m; lid resisting torque $2\ \mathrm{N\,m}$; door
closer torque $20\ \mathrm{N\,m}$ and handle distance 0.8 m; grip forces 150 and
60 N; COM height $\ell=1.0\ \mathrm{m}$; initial COM offset $x_0=0.05\ \mathrm{m}$;
maximum step $L=0.60\ \mathrm{m}$; step duration $t_{\rm step}=0.35\ \mathrm{s}$;
shoe-floor friction 0.7; reaction delay $\Delta t=100\ \mathrm{ms}$; stair cadence
$f=1.8\ \mathrm{steps/s}$; rise height $H=0.40\ \mathrm{m}$ and rise time
$T=1.2\ \mathrm{s}$; young peak knee torque $2.5\ \mathrm{N\,m/kg}$.

Every parameter of Lab D and of K5 falls in this list, so two of the module's
computations rest entirely on unrecorded numbers.

Four abbreviations are used before expansion: "BoS" in the Fig. 1 caption (line 49,
where a caption must stand alone), "vGRF" in Lab A (line 219), "XcoM" at its first
prose use (line 151), and "VO₂" in the §8 table (line 202). "Patellofemoral" (lines
113, 189) and "sarcopenia" (line 97) are used without the plain-words gloss
Pillar 1 requires.

The replacement parameter table (nineteen rows added, every value carrying its
symbol, unit and section) and the seven added notation rows are written out in full
in §6 under tags `B14-params` and `B14-notation`. The four expansions and two
glosses are single-phrase edits, also listed there.

### B15. $m_{\rm up}\approx0.8m$ is neither derived, tabulated, nor labelled an assumption

Location: `module13.html:85`, `:496`.

Quoted: "everything above the knees - thighs, pelvis, trunk, head, arms, the HAT
(head, arms, trunk) plus thigh mass $m_{\rm up}\approx0.8\,m$".

The notation table records the fraction but no table gives it as a parameter with a
provenance, and the text does not call it an assumption. It is also not obviously
consistent with Module 1, whose Appendix gives the head-arms-trunk fraction as
$0.60M$ and labels it an assumed fraction; adding two thighs to that would exceed
0.8. Replacement for line 85:

```html
<p>Idealize the body at seat-off as two segments: the shanks, fixed at the ankles, and everything above the knees - thighs, pelvis, trunk, head and arms - pivoting about the knees. Take that upper mass as $m_{\rm up}=0.8\,m$: this is an assumption, not a regression. Module 1's Appendix puts the head-arms-trunk fraction at $0.60\,m$, also assumed, and two thighs add roughly a further $0.20\,m$, so $0.8\,m$ is the sum with the thighs counted in full. Counting them in full slightly overstates the moment, because a thigh's own centre of mass sits nearer the knee pivot than the trunk's does and so acts at a shorter arm than the common $d$ this model gives every part of the upper body. The overstatement is conservative for a strength margin and it is the only fraction this section needs; K1 shows how the whole conclusion moves if it is wrong, since $d_{\max}=\tau_{\max}/(m_{\rm up}g)$ is inversely proportional to it. Its centre of mass sits a horizontal distance $d$ ahead of the knee joint, and gravity's moment there must be balanced by the knee extensors (the quadriceps, through the patellar tendon of Module 6).</p>
```

### B16. Four detached heads in Fig. 2, and the "climb" label printed across the stair blocks

Location: `module13.html:53`.

Rendered (`m13/fig1.png`, headless Chrome via `shoot.py`) and measured from the
SVG coordinates. In each of the four vignettes the head circle floats clear of the
shoulder sphere with no neck: "rise" leaves a 10.1 px gap between the head's edge
and the shoulder's, "climb" 6.4 px, "lift" and "catch a stumble" 9.5 px each. This
is the "m13 residual detached head" left open in `HANDOFF.md`. It passes all nine
gates, because a gap is not a clipped bounding box, a label over a curve, or a
hairline limb.

Second, the "climb" text at $(190,226)$ sits inside the three stair rectangles,
which run to $y=240$; the halo makes it legible but it reads as text stamped on a
step.

Fix, computed with the `CLAUDE.md` bone generator from the existing shoulder and
head coordinates, adding one neck capsule per figure inside the existing
`<g filter="url(#b_sh)">` group so the head circle, drawn later, overlaps its top:

| figure | shoulder | head | neck rect |
|---|---|---|---|
| rise | (78, 108) | (92, 86) | `x="71.3" y="92.5" width="27.4" height="9" rx="4.5" rotate(-57.5 85 97)` |
| climb | (196, 74) | (200, 52) | `x="186.1" y="58.5" width="23.7" height="9" rx="4.5" rotate(-79.7 198 63)` |
| lift | (360, 110) | (378, 92) | `x="355.6" y="96.5" width="26.8" height="9" rx="4.5" rotate(-45.0 369 101)` |
| stumble | (516, 108) | (534, 90) | `x="511.6" y="94.5" width="26.8" height="9" rx="4.5" rotate(-45.0 525 99)` |

and the three stair rectangles shorten to end at $y=212$ (heights 12, 28, 44 from
tops 200, 184, 168), clearing the label row.

### B17. §9's provenance sentence and §4's amplification factor each state a number the module does not have

Location: `module13.html:216`, `module13.html:131`.

Line 216's "every plotted number was produced by the code shown" is repaired by the
print lines of B4 and B5. Line 131's "more than five times body weight … the
fivefold amplification is entirely the $d_L/d_m$ lever ratio" names one factor
three times with three values: the compression is 6.1 body weights on the old
numbers and 6.3 on the corrected ones, while $d_L/d_m$ is 8 and $F_m/W_L$ is 20.6.
The replacement is inside B2.

## 3. Style and clarity edits

Grouped so they can be applied in one pass. Quote, then rewrite.

**S1** (line 173). "which is why grip strength is a validated proxy for whole-body
frailty" → "which is also why grip strength is measured in frailty assessment,
though the module derives only the jar, not the correlation." An epidemiological
claim the module cannot derive should be flagged as borrowed, per the brief's
"claims are earned by derivation … not by citation".

**S2** (line 113, repeated at line 340). "That is exactly why descent dominates
stair-fall statistics" → "That is the mechanical reason a descent failure becomes a
fall rather than a stop; the epidemiology is not derived here."

**S3** (line 151). "This is why turning is a disproportionate fall trigger in the
elderly" → "This is the mechanical reason turning is harder than walking straight,
and the reason balance rehabilitation drills turning steps specifically."

**S4** (line 111). "it is comparable to a brisk cycling effort, delivered by the
legs alone" → "it is roughly the sustained output of a brisk cycling effort, and it
sits at $84\%$ of the $250\ \mathrm{W}$ ceiling this module assumes (Lab B), which
is why a long staircase cannot be climbed at that cadence indefinitely." The
analogy is cashed into the module's own ceiling.

**S5** (line 216). "Four labs put numbers under the cases" → "Four labs compute
the cases."

**S6** (line 195). "This is the module's unifying payoff:" → deleted; the sentence
that follows does the work.

**S7** (line 179). "A slope tilts gravity's bookkeeping." → "A slope changes what
gravity does over a stride." The metaphor is used at line 101 too; one use is
enough and the §3 one is the better of the pair.

**S8** (line 364). "so the required force blows up toward infinity as $d\to0$" →
"so the required force grows without bound as $d\to0$; a door pushed on its hinge
line cannot be opened at all."

**S9** (line 55). "it lives at the edge, which is why the edge moving inward - with
age or injury - is felt so sharply" → "daily life runs near the edge of the
envelope, which is why the envelope shrinking with age or injury is felt as a
sudden loss rather than a gradual one."

**S10** (line 47 against line 57 and the Fig. 2 caption). "reading off the forces,
torques, powers, and stresses the body actually meets" appears three times in
eleven lines. Keep it in §0's opening sentence, cut it from line 57's thesis box
(which ends better on "measures case by case"), and change the Fig. 2 caption's
tail to "…on these everyday acts, one movement at a time."

**S11** (line 101). "Stairs make gravity's bookkeeping vivid because every step
changes the body's height by a fixed amount." → "Stairs are the clearest case of
work against gravity, because every step changes the body's height by a fixed
amount." (Paired with S7.)

**S12** (line 417). "Each requires a sweep, an inverse solve, an optimisation, a
simulation, or a regime comparison - not substitution into a boxed formula." Keep,
but it is only true after B9; note the dependency.

**S13** (line 131 old text). "the difference between borderline and clearly
hazardous" is used at line 131 and again at line 348 for the same pair of numbers.
The C4 instance is rewritten under B2's cascade; keep the phrase once, in §4.

**S14** (line 449). "This is why the pure vertical model shows a penalty" → "The
pure vertical model therefore shows a penalty, not a saving". "This is why" points
at nothing prior.

**S15** (line 293). "Failure mode. Crossing tissue tolerance - lower in aged discs
and osteoporotic bone." → "Failure mode. Compression crosses tissue tolerance,
which is lower in aged discs and osteoporotic bone (Module 2)." A sentence fragment
in a box that is otherwise full sentences.

**S16** (line 469). "These case studies are first-order estimates - the right order
of magnitude and the right dependencies, but deliberately simplified." → add "Every
one is Level 1 in the sense of §0, and the table below says what each idealisation
costs." Ties the closing audit to the level statement B11 adds.

**S17** (line 51). "The value of doing this is threefold." → "Doing this pays three
ways." Cuts an announcing construction.

**S18** (line 83). "Watch it and it has two phases" → "The movement has two
phases".

**S19** (line 119). "and the reason is a lever with a cruel ratio" → "and the
reason is the lever ratio". "Cruel" is a hedge word doing the job a number should
do, and the number arrives two sentences later.

**S20** (line 189). "the reason a long descent leaves the thighs sore" → "the
reason a long descent leaves the quadriceps sore for days: eccentric loading is the
regime that produces delayed muscle soreness (Module 5)." Names the mechanism
rather than the sensation.

**S21** (line 212). "The margins are thin to begin with" → "The margins are thin
before any decline: a healthy chair rise already spends $63\%$ of a young adult's
knee torque (K10) and a careless lift already exceeds the recommended spinal load
by $28\%$ (§4)." Replaces two vague claims with the module's own computed numbers.

**S22** (line 55). "a template we set up once in Section 1 and then apply to nine
everyday movements" - the module treats nine cases in six sections; the §8 table
has nine rows. Change to "nine everyday movements across six sections" so the
count is checkable.

## 4. Structural notes

- The module's shape is right and unusually disciplined: one template in §1, six
  case sections that each run it, one synthesis section, four labs, thirty
  problems. Nothing needs reordering.
- §6 carries two cases (jar and door) but only one proposition, and it says why
  ("a one-line lever balance beside the jar's friction subtlety, needing no
  separate proposition"). That is the right call and the correct way to make it;
  the boxed-result parity rule is satisfied because the door result is not boxed.
- §5 likewise imports the capturability result from Module 10 in a `.keyresult`
  labelled "(imported from Module 10)" rather than reproving it. That is the right
  treatment of a borrowed result and the repayment ledger records it.
- Fig. 2's four vignettes have no arms, while Fig. 1's figures do. At 90 px per
  vignette that is a defensible simplification, but the "rise" vignette also has no
  chair, so it does not read as rising from anything. Worth a small addition when
  the figure is next touched; not fixed here, since it needs the body kit rather
  than a coordinate edit.
- `check_frame.py` reports seventeen figures with more than twenty percent wasted
  viewBox margin (all advisory, no clipping). Seven of them are problem figures
  with margins above thirty percent on one side. Retightening is a judgement call
  and was left alone; the suggested viewBoxes are in the gate output.
- The labs are thin relative to the problem set: four short scripts, each a
  closed-form evaluation and a plot, against ten computational problems that now
  each carry a script. After the edit the K set covers an inverse solve with a
  threshold (K1), an inverse with a sensitivity (K2), a two-parameter sweep (K3,
  K4), a constraint boundary (K5), a regime comparison (K6, K7), a prescribed
  trajectory integration (K8), an optimisation (K9), and a multi-margin ranking
  (K10). That is the depth standard met.
- The repayment ledger and the captures/misses table are both good and both
  complete. The ledger's six rows each name a module that actually discharges the
  borrowing.

## 5. What already works

- All six propositions are proved to the same weight, and each proof derives its
  boxed result rather than restating it. Proposition 5.1's proof
  (`module13.html:147`) is the best of them: it names the isosceles construction
  that gives $2v\sin(\beta/2)$ instead of asserting the identity, and it states the
  impulse's direction, which is the part a reader would otherwise have to guess.
- Proposition 7.1's proof gives the result twice, once by resolving the weight
  along the path and once by the vertical speed, and says the two are the same
  statement. That is the kind of redundancy that teaches.
- Every one of the six worked numbers reproduces exactly: 109.87, 116.74 and
  210.13, 3629.7, 91.00, 81.63 and 57.14, 59.85 and 119.24 and 177.73. So do the
  grade conversions ($8.7\%$, $17.6\%$, $26.8\%$) and every K arithmetic that is
  not itself a defect: K1's 0.1911 and 0.1274, K4's 1.7227 and 1.2173 and the
  $29.3\%$ loss, K5's $135.2^\circ$ and $73.9^\circ$, K6's 1.05, 2.10 and 2.52,
  K7's 4.18, 2.10 and 1.41, K8's 127.8 and 91.9, K9's 29.43 and 0.0857, D8's 16.93
  and 9.24, D10's 0.0857. Fifty-two of the sixty-one numbers checked are right as
  they stand.
- K8 is the model computational problem of the module. It integrates a prescribed
  minimum-jerk trajectory, reports a peak and a trough rather than one number, and
  then says explicitly which mechanism the model does and does not capture. It is
  also the only place in the module that corrects a claim made elsewhere in it,
  which is why B4 resolves in K8's favour.
- K4's exponential envelope, $\dot x_{\max}=\omega_0(Le^{-\omega_0\Delta t}-x_0)$,
  is exactly the right way to make Module 10's capturability result bite on daily
  life, and the $29\%$ loss from a tenth of a second is the module's single most
  persuasive number.
- §1's Definition 1 is a real definition: five numbered steps, each an instruction
  a reader can carry out, and every later section visibly instantiates it.
- Pillar 1 holds through most of the module: "HAT (head, arms, trunk)", "L5/S1 disc
  (the lumbosacral junction, the most loaded level)", "the erector spinae, running
  just behind the spine", "NIOSH (US National Institute for Occupational Safety and
  Health)", and the concentric/eccentric pair at line 75 are all glossed in the
  sentence of first use.
- The §8 synthesis table earns its place. Every row names a binding margin, a
  failure mode, an aging change, and a training response, and the middle column is
  a formula rather than a word in six of the nine rows.

## 6. Changes applied

Applied to `edited/module13.html` by one re-runnable script, `m13/apply.py`
(98 `rep()`/`rep_svg()` edits, each asserting its anchor occurs exactly once).
Figures regenerated by `m13/figs13.py` → `figs13.json`. Code blocks spliced from
`m13/kblocks/*.py`, HTML-escaped.

**Re-verification of the report's own numbers.** Every one of the 61 numbers
this report asserts was recomputed in the apply run (`cascade.py`,
`kblocks/K1.py` … `K10.py`, `figs13.py`) and every one reproduced. No number in
the report had to be corrected. Three of the report's *non-numeric* premises did
have to be corrected during apply, and are logged as such below (rows `S10`,
`B8-K10fig`, and the `class="probes"` note under `B9-K3stmt`).

| tag | line (original) | what changed | how verified |
|---|---|---|---|
| B1 | 79 | "margin" redefined as capacity over demand (it was demand over capacity, which is the failure condition); the balance margin split out as the one length-valued exception, threshold zero not one | reads consistently with `:97` "a strength margin below one", which then needed no change |
| B15 | 85 | $m_{\rm up}=0.8\,m$ labelled an assumption and reconciled with Module 1's $0.60\,m$ HAT fraction plus two thighs; the overstatement named and called conservative | `module01.html` Appendix fraction; K1 shows the inverse dependence the sentence now cites |
| B10a | 95 | the momentum strategy split into the geometric effect and the 6% impulse offset that D7 now proves; the horizontal-momentum claim withdrawn | D7's arithmetic, row B10-D7 |
| B14-gloss-sarcopenia | 97 | "sarcopenia" glossed at first use | Pillar 1 read-through |
| B2-box | 124 | $F_{\rm comp}\approx$ → $F_{\rm comp}=$; the $\cos\phi\le1$ hedge is gone | the proof now evaluates $\phi$ at its real value |
| B2-prop | 125 | Proposition 4.1 rebuilt on Module 1's parameters — $W_{\rm tr}=412$ N (0.60 M), $\ell_t=0.346$ m, $d_{\rm tr}=\ell_t\sin\phi$ — giving stoop 4040 N / 4350 N and squat 2530 N in place of 3630 N / 4200 N | `cascade.py`: $F_m=4041.7$ N, $F_{\rm comp}=4345.8$ N, matching `module01.html`'s published 4040 N and 4346 N to the newton |
| B2-proof | 127 | the proof carries the $d_{\rm tr}=\ell_t\sin\phi$ step and both substitutions (stoop 4040 / 4350, squat 1960 / 2530); the "conservative upper bound" branch deleted | same run, stoop and squat rows |
| B2-fig5cap | 129 | Fig. 5 caption: 4200 N → 4350 N, $\phi$ and $d_{\rm tr}=\ell_t\sin\phi$ named, squat value 2530 N added | same run |
| B2-amp, B7, B17, S13, S19 | 131 | "more than five times body weight … the fivefold amplification" → 6.3 BW with the three lever ratios stated separately ($d_L/d_m=8$, $d_{\rm tr}/d_m=6$, $F_m/W_L=20.6$); the two rules ranked and costed at 14% for reach, 28% for posture, 42% together | `cascade.py`: 4346→3757 is 13.5%, 4346→3117 is 28.3%, 4346→2529 is 41.8% |
| B2-failmode | 135 | 4200 N → 4350 N; "shrinking $d_L$ and $d_{\rm tr}$" → "$d_L$ and $\phi$", since posture is the variable the lifter sets | consistency with B2-prop |
| B11-level | after 57 | new paragraph placing every case on the level ladder: Level 1 statics and energy, K8 the single Level 2 excursion, the inertial correction 16% | `kblocks/K8.py`: 127.8 / 109.9 = 1.163 |
| B11-cando | after 212 | new closing "what the reader can now do" paragraph | domain-brief requirement for a closing section |
| B14-BoS | 49 | "BoS" expanded in the Fig. 1 caption, which has to stand alone | read-through |
| B14-XcoM | 151 | "(XcoM)" attached at the first prose use of extrapolated centre of mass | read-through |
| B14-VO2, B14-VO2b | 202, 208 | "VO₂" expanded in both §8 table rows that use it | grep found two occurrences; both edited |
| B14-patellofemoral | 113 | "patellofemoral joint" glossed in plain words | Pillar 1 |
| B12-mu-163, -165, -box, -proof, -C7, -K6, -K6probe, -table | 163, 165, 166, 169, 360, 441, 206 | $\mu$ → $\mu_{\rm lid}$ at all eight jar-contact sites | grep for `\mu` after the pass: only $\mu_{\rm lid}$ and $\mu_{\rm shoe}$ remain |
| B12-mu-K5 | 437 | $\mu$ → $\mu_{\rm shoe}$ in K5, the contact named as shoe-on-floor and its 0.7 labelled an assumption | same grep; the collision with the jar's $\mu$ is gone |
| B12-d-175, -C8, -table | 175, 364, 207 | the door arm $d$ → $d_{\rm hinge}$, with a parenthesis reserving plain $d$ for §2's chair arm | the Appendix at `:499` defines $d$ as the chair arm; one letter, one meaning |
| B12-fig7-svg1/2/3, -cap, -svg2b | 171 | Fig. 7's three SVG labels and its caption carry $\mu_{\rm lid}$ and $d_{\rm hinge}$; the $d_{\rm hinge}$ label moved from y=94 to y=86 to clear the dashed hinge line | `check_overlap.py` flagged the widened label, box [360, 85, 21, 14], hitting the dashed line at [360, 96]; 0 overlaps after the move |
| B13-prop | 167 | the skin-lid friction range 0.5–1.0 stated with both ends named, and 0.7 labelled the mid-value | §6 and K6 no longer give the same contact two coefficients without comment |
| B13-threshold, S1 | 173 | the 150 N / 60 N threshold worked at $\mu_{\rm lid}=0.7$ (3.7 and 1.5 N·m) and at 0.5 (1.05 N·m, K6); the frailty-proxy claim marked as borrowed, not derived | $0.7\times150\times0.035=3.675$; $0.7\times60\times0.035=1.47$; `kblocks/K6.py` gives 1.05 |
| B4-model | 219 | Lab A no longer declares an $H$, $T$, dynamic-vGRF model its code never runs; the ceiling $\tau_{\max}=1.5m$ is stated and the dynamic case handed to K8 | the lab's code contains no $H$, no $T$, no $a$ |
| B4-extension | 241 | the Extension claimed a brisk rise *lowers* the extension torque; replaced by K8's computed result, 110 → 128 N·m at $T=1.2$ s and 142 N·m at $T=0.9$ s | `kblocks/K8.py` run |
| B4-print | 223 | Lab A gains a print line for the 82 and 154 N·m endpoints and the 0.191 m crossing its caption quotes | run prints `d=0.15 m: 82 N m; d=0.28 m: 154 N m; crossing at d=0.191 m` |
| B5-labD-print | 307 | Lab D gains a print line for the 1.72 m/s boundary its caption quotes | run prints `max recoverable speed with no delay: 1.72 m/s` |
| B3-params | 268 | Lab C's parameters fixed: one squat distance instead of three (0.20 in the text, 0.22 in the sweep, 0.25 in the print), the load set 10 and 20 kg rather than the stated 10–25, and posture entering through $\phi$ | the old code swept from 0.22 and printed at 0.25 while the parameters said 0.20 |
| B3-code | 270–289 | the lab now varies posture as well as reach — `comp(mL, dL, phi)` with $W_{\rm tr}=0.60mg$ and $d_{\rm tr}=\ell_t\sin\phi$ — so it computes the mechanism §4 claims | run gives 1848 / 2535 (10 kg, 20°), 3120 / 3806 (10 kg, 60°), 2333 / 3706 (20 kg, 20°), 3561 / 4934 (20 kg, 60°) N |
| B3-fig, B3-fig-viewbox | 291 | Lab C's plot regenerated from the new model: four curves, the NIOSH line, and a computed crossing marker at $d_L=0.472$ m; viewBox widened 500 → 620 so the legend sits outside the plotted frame | `figs13.py`; `check_overlap.py` had flagged both stoop legend labels sitting on curves, 0 after the move; `check_frame.py` exit 0 |
| B3-cap | 291 | caption rewritten to the computed numbers: 2333 N, 4934 N, 3561 N, and the squat crossing at 0.47 m | same run |
| B3-interp | 293 | interpretation rewritten; the sensitivity "$W_L/d_m\approx4$ N" corrected to 39 N per centimetre for the 20 kg box and 20 N for the 10 kg box, and the posture slope 1430 N per radian (25 N per degree) added; S15's sentence fragment made a sentence | $W_L/d_m=196.2/0.05=3924$ N/m; $W_{\rm tr}\ell_t\cos60^\circ/d_m=1426$ N/rad |
| B7-C3 | 344 | C3's "about fortyfold per metre" corrected to $1/d_m=20$ N per N·m and 39 N per centimetre of reach; "no other single change moves the compression as much" deleted, because K3 shows posture moves it more | `cascade.py` sensitivity block |
| B2-C4, B2-C4fig-a, B2-C4fig-b | 347, 348 | C4's 3600 / 4800 N replaced by §4's 2530 / 4350 N in the prose and in the figure's two SVG labels, and the two moves ranked | `cascade.py` posture rows |
| B2-D3 | 386 | D3 gains the $d_{\rm tr}=\ell_t\sin\phi$ step, so posture is in the derivation and not only in the prose | matches the new Proposition 4.1 proof |
| B10-D7 | 402 | D7 now proves the momentum offset in the smallest setting — vertical impulse-momentum, then the energy version — instead of deferring it; the undefined $\Delta v$ replaced by a defined $v_0$, with $v_0$ and $T_e$ labelled assumptions and tabulated | hand derivation: $m_{\rm up}gH=56\times9.81\times0.40=219.7$ J; $\tfrac12m_{\rm up}v_0^2=1.75$ J; $m_{\rm up}v_0=14$ N·s; $m_{\rm up}gT_e=219.7$ N·s; $14/220=6.4\%$ |
| B9-D8, B9-D8fig | 405, 406 | D8's safe loads 17 kg and 9 kg replaced by 35.0 kg squatting and 8.7 kg stooping, with the $1/\sin\phi$ dependence named; its figure regenerated as two posture curves on a 0–50 kg axis (the old 0–20 axis could not hold 35 kg) | `kblocks/K3.py` prints 35.0 and 8.7; the 8.7 kg reproduces Module 1's own safe-load figure |
| B9-K3stmt, B9-K3sol, B9-K3fig | 427, 428, 429 | K3 was D8 restated word for word; it is now the two-parameter sweep its title promises, with the $\phi$–$d_L$ surface, the one-at-a-time comparison (8.7 → 23.2 kg by standing up against 8.7 → 13.4 kg by pulling in), the 4.0× corner ratio, its own code, and a three-posture figure. **The report's replacement HTML used `<span class="probes">`; the file's own markup is `<span class="small"><em>Probes: …</em></span>`, and the file's markup was used** — the stylesheet defines no `.probes` class | `kblocks/K3.py` run: the 3×3 grid and `squat (20 deg, 0.25 m) buys 4.0x the stoop`; grep of the file's other 29 problems for the Probes markup |
| B6-K2 | 425 | K2's backwards sensitivity claim ("steepens at low power ceilings") corrected: $\partial f_{\max}/\partial m=-P/(m^2gh)$ is proportional to the ceiling — 0.0184 at 150 W, 0.0489 at 400 W — while the log-sensitivity is $-1$ regardless of $P$; code added | `kblocks/K2.py` run |
| B8-K10stmt, B8-K10sol | 455, 457 | K10 asserted the ordering after computing one threshold; it now scales both reserves by a common factor and computes all five — 0.88 low chair, 0.84 stairs, 0.63 standard chair, 0.48 slope, 0.47 high firm chair — with the shared-decline assumption labelled as an assumption | `kblocks/K10.py` run |
| B8-K10fig | 456 | **A defect the report did not reach:** K10's figure was byte-for-byte K1's chair-torque-versus-$d$ plot but for its aria-label, so the problem about ranking five tasks showed a plot of one. Replaced by a ranking bar chart of the five computed thresholds | found by diffing the two SVG bodies (2590 vs 2591 chars, differing only in the aria-label); the new chart's five bars are `kblocks/K10.py`'s five percentages |
| B5-K1, -K4, -K5, -K6, -K7, -K8, -K9 | 421, 433, 437, 441, 445, 449, 453 | the seven remaining computational solutions gain the code the module claims four times that they carry | all seven extracted from the edited file and run; each prints the numbers quoted in the solution beside it |
| B5-K9, B2-D10 | 453, 414 | the carry lean 0.09 m corrected to 0.071 m in both places — the moment 29.4 N·m is unchanged, only $W_{\rm tr}$ moved from 343 to 412 N — and the 589 N side-flexor force added | `kblocks/K9.py`: `moment 29.43 N m, lean 0.071 m, side-flexor 588.6 N` |
| B5-lab-intro, S5 | 216 | "Four labs put numbers under the cases … every plotted number was produced by the code shown" → "Four labs compute the cases … every number quoted in a lab's caption or interpretation is printed by the code shown", which is now true given B4-print and B5-labD-print | all four labs re-run from the edited file |
| B17-colophon | 524 | "every number reproduced by the code shown" narrowed to "every computational number reproduced by the code shown beside it" | 14 code blocks in the file, all run |
| S2a, S2b | 113, 340 | two epidemiological claims ("descent dominates stair-fall statistics") replaced by the mechanical statement, with the epidemiology marked as not derived here | the brief's rule that claims are earned by derivation, not citation |
| S3 | 151 | the elderly-fall-trigger claim replaced by the mechanical one plus the rehabilitation practice it explains | same |
| S4 | 111 | "comparable to a brisk cycling effort" cashed into the module's own ceiling: 84% of the 250 W it assumes | $210.13/250=0.841$ |
| S6 | 195 | "This is the module's unifying payoff:" deleted | the sentence that follows does the work |
| S7, S11 | 179, 101 | "gravity's bookkeeping" now used once, not twice; §3 keeps the plainer phrasing | grep: the metaphor is gone from both |
| S8 | 364 | "blows up toward infinity" → "grows without bound … a door pushed on its hinge line cannot be opened at all" (applied inside B12-d-C8) | read-aloud |
| S9 | 55 | "it lives at the edge, which is why the edge moving inward …" rewritten | read-aloud |
| S10 | 53 | Fig. 2's caption tail → "on these everyday acts, one movement at a time." **The report's premise was wrong here and is corrected:** the phrase "reading off the forces, torques, powers, and stresses" occurs at `:47` only, not at `:57`, and the Fig. 2 caption carries a variant ("joint torques, spinal loads, and balance margins"). Two occurrences, not three, so only the caption was cut and `:57` needed no edit | grep of the phrase across `:47`, `:53` and `:57` |
| S14 | 449 | "This is why the pure vertical model shows a penalty" → "The pure vertical model therefore shows a penalty, not a saving" | "This is why" pointed at nothing prior |
| S15 | 293 | Lab C's "Failure mode." fragment made a full sentence with its Module 2 pointer (applied inside B3-interp) | read-aloud |
| S16 | 469 | the captures-and-misses preamble now ties to the level statement B11 adds | consistency with B11-level |
| S17, S18 | 51, 83 | two announcing constructions cut | read-aloud |
| S20 | 189 | "leaves the thighs sore" → names the mechanism: eccentric loading, delayed muscle soreness, Module 5 | read-aloud |
| S21 | 212 | "The margins are thin to begin with" replaced by the module's own computed numbers: 63% of a young adult's knee torque (K10), 28% over the recommended spinal load (§4) | $109.87/175=0.628$; $4346/3400=1.278$ |
| S22 | 55 | "nine everyday movements" → "nine everyday movements across six sections", so the count is checkable | §8's table has nine rows drawn from six case sections |
| B14-notation-lift, B14-notation-manip | 495–506 | nine notation rows added ($\ell_t$; $W_b,d_b,x_{\rm lean}$; $F_{\rm lim}$; $\tau_{\rm resist},\tau_{\rm door},d_{\rm hinge}$; $\mu_{\rm shoe}$; $L,t_{\rm step},\Delta t$; $H,T,v_0,T_e$), and $\mu$ and $d$ renamed in the rows they already had | every symbol used in §§1–10 now has a row with its section |
| B14-params | 509–520 | eighteen parameter rows added, each with symbol, value, unit and the section or problem that uses it, and each empirical value marked "(assumed)" or attributed to Module 1 | the eighteen unsupported numbers listed in B14 are now table rows, Lab D's and K5's parameters among them |
| B16-neck-rise, -climb, -lift, -stumble | 53 | one neck capsule per vignette, computed with the `CLAUDE.md` bone generator from the existing shoulder and head coordinates and inserted inside the existing `<g filter="url(#b_sh)">` so the head circle overlaps its top — the four detached heads left open in `HANDOFF.md` | geometry re-derived from the SVG coordinates (rise: L = 27.43, angle −57.53° about (85, 97)), matching the report to 0.1 px; then rendered in headless Chrome (`shoot.py` → `m13/preview.png`) and looked at — all four heads now join their shoulders |
| B16-stair-a, -b, -c | 53 | the three stair rectangles shortened to end at $y=212$ (heights 12, 28, 44 from unchanged tops 200, 184, 168) so the "climb" label at $y=226$ no longer sits inside a step | same render; the step tops are unchanged, so the figure still stands on its steps |

| B12-mu-174 | 174 | the last bare $\mu$ in §6's interpretation ("a rubber pad or a dry hand raises $\mu$") renamed to $\mu_{\rm lid}$ — B12's rename had missed it, leaving a symbol the notation table no longer defines | grep of the edited file for `\mu` not followed by `_`: 5 hits before this pass, 0 after |
| B12-mu-D5 | 405 | D5's solution carried four more bare $\mu$; all four now $\mu_{\rm lid}$ | same grep |
| B9-K3fig-aria | 460 | K3's figure was replaced by B9-K3fig but kept the aria-label of the problem it replaced — and that label was itself truncated mid-sentence with an ellipsis and quoted raw TeX (`$3400\ \mathrm{N}$`) at a screen reader. Rewritten to describe the three curves actually drawn, in words | read the label against the decoded polylines; `verify_dom`'s stray-`$` advisory fell 18 → 16 |
| B14-params-mulid | 518 | the parameter table's skin-lid friction row carried a bare range and no symbol (the three cells read `Skin-lid friction`, `$0.5$-$1.0$`, `§6`) while its sibling $\mu_{\rm shoe}$ row carried symbol, value and an assumed marker. Upgraded in place to name $\mu_{\rm lid}$, give the three values §6 and K6 actually use, mark them assumed, and cite K6 as well as §6 | the values 0.5 / 0.7 / 1.0 are the ones §6's prose and `kblocks/K6.py` use; `check_links` still 106 links, 0 broken. A first attempt appended a *new* row and was withdrawn once the grep found the existing one — the file had it at `module13.html:518` all along |

**Gates, before and after.** Identical on eight of nine; `verify_dom`'s stray-`$` advisory improved from 18 to 16 when B9-K3fig-aria removed the raw TeX from an aria-label. Nothing regressed.

| gate | baseline (pristine) | after |
|---|---|---|
| `checktex` | 515 segments, 0 issues | 713 segments, 0 issues |
| `checklt` | 0 | 0 |
| `check_links` | 84 links, 0 broken, 0 unlinked | 106 links, 0 broken, 0 unlinked |
| `check_svg` | 0 hard, 0 advisory | 0 hard, 0 advisory |
| `check_code` | 4 blocks, 0 issues | 14 blocks, 0 issues |
| `verify_dom` | 0 mjx-merror, 0 broken links, 18 stray-$ (advisory), 0 swallowed prose | 0 mjx-merror, 0 broken links, **16** stray-$ (advisory), 0 swallowed prose |
| `check_overlap` | 0 | 0 (this pass introduced 3; all 3 fixed) |
| `check_frame` | exit 0; 0 clipped, 17 wasted-margin (advisory) | exit 0; 0 clipped, 17 wasted-margin (advisory) |
| `check_bodyprop` | 1 advisory (Fig. 1 sit-to-stand, limb/head ratio 0.41) | 1 advisory, unchanged |

`check_frame` did fire HARD once during the pass — the new K10 chart spilled
about 8 px past the right edge — and the chart was rebuilt inside its viewBox
before the final run.

All fourteen `<pre><code>` blocks in the edited file were extracted and run
(`m13/final/blk01…blk14`); every one exits clean and prints the numbers the
prose beside it quotes.

**Not done, and why.** The structural notes of §4 remain notes. The Fig. 2
"rise" vignette still has no chair, so it does not read as rising from
anything, and the four vignettes still have no arms; both need the body kit
rather than a coordinate edit. The seventeen wasted-margin viewBoxes are left
alone, since retightening is the judgement call `check_frame` declines to
force. The `check_bodyprop` advisory on Fig. 1 is unchanged from the baseline:
the 5.6 px element it flags is a forearm beside a 14 px head, which is anatomy,
not a hairline limb.


## 7. Verification pass

A second agent re-ran the whole pass on the finished file. What it settled:

- **The apply is reproducible and complete.** `cp module13.html
  edited/module13.html && python apply.py` reproduces the edited file
  byte-for-byte from the pristine one. No edit was made by hand outside the
  script, so the table above is the complete list of changes. 102 `rep()` calls
  (98 from the first pass, 4 from this one), every one covered by a table row.
- **The four residual edits went through `apply.py` too**, and the file was rebuilt from pristine after each, so the byte-identical guarantee still holds: 102 `rep()` calls produce `edited/module13.html` from `module13.html`.
- **All nine gates re-run on both files.** Baseline and edited agree exactly
  except for the improved stray-`$` count; no gate is worse than the baseline
  and no gate has a hard failure.
- **All fourteen `<pre><code>` blocks re-extracted from the edited file and
  re-run** (matplotlib forced to the `Agg` backend — four of them end in
  `plt.show()`, which blocks on an interactive backend). All exit 0. Every
  number the prose quotes beside a block is a number that block printed:
  K1 0.191/0.127 m, K2 2.142/1.666 steps/s and 0.0184/0.0489, K3 35.0/23.2/
  13.4/8.7/6.4 kg and 4.0x, K4 1.723/1.217 m/s and 29.3%, K5 135.2°/73.9°,
  K6 1.05/2.10/2.52 N·m, K7 4.18/2.10/1.41 m/s and −49.8%, K8 109.9/127.8/
  91.9 N·m (the "sixteen percent" of §0's level statement is 127.8/109.9 =
  1.16), K9 29.43 N·m / 0.071 m / 588.6 N, K10 87.9/84.1/62.8/47.7/47.1%.
- **The Module 1 cross-check passes.** Every value §4 borrows matches
  `module01.html`: $m_{\rm ub}=0.60M=42$ kg (its Appendix row, marked "assumed
  fraction"), $W_{\rm tr}=412$ N, $\ell_t=0.346$ m, $d_m=d_{\rm es}=0.05$ m,
  the 20 kg box at 0.40 m from a $60^\circ$ stoop, $F_m=4040$ N, $F_{\rm comp}
  \approx4.34$ kN, the 3400 N NIOSH limit, and body weight 687 N. The four
  savings §4 quotes recompute from those values to 13.6%, 28.3%, 41.8% and the
  20.6x amplification. The reference human's *upper-limb* values (elbow flexor
  moment arm 0.03 m, forearm-plus-hand COM 0.116 m, grip at 0.35 m,
  $m_s=1.54$ kg) are not used anywhere in Module 13, so there is nothing to
  conflict.
- **The level ladder is placed.** `edited/module13.html:58` states it (Level 1
  throughout, quasi-static in §§2, 4, 6, 7; Level 1 dynamic in §§3 and 5; K8
  the single Level 2 excursion), and `:603` holds §9 to the same statement.
- **Every touched figure was decoded from its `<polyline>` points back into
  data**, by calibrating on the tick `<text>` coordinates and inverting.
  Lab A's torque line reads 82 N·m at $d=0.15$ and 153 N·m at $d=0.28$ against
  the code's 82 and 154. Lab C's four compression curves read 3551/4923,
  3110/3795, 2323/3694 and 1837/2524 N against the code's 3561/4934,
  3120/3806, 2333/3706 and 1848/2535 — a uniform 11 N offset that is the
  text-baseline allowance, so all four match. Its "squat crosses at 0.47 m"
  label recomputes to 0.472 m. D8's two curves read 41.8 and 17.2 kg (squat)
  and 16.1 and 6.2 kg (stoop) against 42.0/17.4 and 16.4/6.4. K3's three
  curves add the $40^\circ$ case at 26.5 and 10.6 kg against 26.7 and 10.8.
  K10's five bar widths are in the exact ratio of the five computed
  percentages. No figure contradicts its caption or its code.
- **No detached head remains.** Fig. 1 and Fig. 2 were re-rendered in headless
  Chrome from the current edited file and looked at: all five bodies join head
  to shoulder, and the "climb" label clears the shortened stair blocks. The
  `check_bodyprop` advisory on Fig. 1 is the baseline one (a 5.6 px forearm
  beside a 14 px head — anatomy, not a hairline limb). The `HANDOFF.md` open
  item "m13 any residual detached head" is closed.

Still not done, unchanged from the first pass: Fig. 2's "rise" vignette has no
chair and none of the four vignettes have arms (both need the body kit, not a
coordinate edit), the seventeen wasted-margin viewBoxes are left alone, and
§4's structural notes remain notes.
