# Editor report: module05.html (Muscles as Chemo-Electro-Mechanical Actuators)

Editorial pass. Standard: the five-part rule of the `science-editor` skill, read
against `EDITOR_DOMAIN.md`. Every location is `module05.html:LINE` in the
**original** file. Every replacement is valid HTML with MathJax delimiters and
uses only the box classes the stylesheet defines.

Both Python blocks in the original file (Lab 1 and Lab 2) were extracted and run,
and the labs were re-implemented as parameterised functions. The ten K problems
carried **no code at all**, so each one's model was re-implemented and run before
its number was accepted; those ten scripts are the ones now spliced into the
solutions. Every `<polyline>` in every figure was decoded back into data
(`m05/decode.py`: calibrate the axis map from the tick `<text>` coordinates,
invert it, compare against the model the prose claims). Scripts in the session
scratchpad, folder `m05/`: `extract.py` output in `blocks/`, `ver2.py`, `ver3.py`,
`decode.py`, `probfig.py`, `genfigs.py`, `genfig2.py`, `new/k1.py`…`new/k10.py`,
`apply.py`.

Applied to `edited/module05.html`; the original is untouched.

## 1. Verdict

**Yes, after revision.** The spine of this module is sound and, in places,
exemplary: the sarcomere overlap geometry is derived rather than asserted, the
size principle falls out of one line of Ohm's law, and the two labs print numbers
their figures actually draw. Decoding every polyline confirmed that the
length-tension curve, the four tetanus traces, the force-frequency curve, the
step response, the force-velocity hyperbola, the moment-arm curve, the passive
curve and both lab plots all agree with the models the prose states, to the
resolution of the drawing. That is unusual and worth saying first.

What stops the reader is elsewhere, and most of it is one class of failure:
**the module computes with models it never writes down.** The entire §3-§4 chain
(the twitch, the four tetanus traces, the fusion frequency, the ceiling
$a_\infty=0.73$) comes from a calcium-pulse model with four constants that appear
nowhere in the text. The parallel elastic element is drawn and used in the labs
with no constitutive law. The eccentric shape constant $k$ is named, used at the
value 20 in the code, and never given a value in the prose. Lab 1's
fibre-length map and moment-arm law exist only inside a code comment. A reader
cannot reproduce a single §3, §4, §7 or §9 number from the page.

Three results are wrong rather than missing. Fig. 30's constraint line and cost
ellipses are drawn for maximal forces in the ratio 1:2 (decoded ellipse semi-axes
70.7 and 141.4 N), which contradicts §1's own 135 N and 210 N, so its quoted
optimum 57/144 N is the answer to a different problem; the correct optimum is
76/114 N. K10 states a fitted $\tau_a$ of 41.5 ms; the least-squares fit it
describes returns 43.7 ms. K6's solution says the strength peak falls where
neither factor is maximal, when $f_L$ is flat across a plateau that contains the
peak.

Two structural faults. Two decorative `<figure>` banners sit before the first
`<h2>`; the stylesheet numbers every `<figure>` with a CSS counter, so **every
in-text "Fig. N" in the module points two figures earlier than the one the reader
sees**. And the section header promises "every answer is Python-verified" above
ten problems, eight of which carry no code; one of the two that did (Lab 1's) has
live `<a>` tags inside the `<pre><code>`, so the copy button hands the reader
something that is not Python.

On the K-problem depth standard the retrofit **mostly held**: K2, K3, K5, K6, K8,
K9 and K10 each require simulation, optimisation, an inverse problem or a sweep.
Two did not. K4 was two evaluations of the boxed $f_V$, and K7 integrated a
constant-torque limb that used none of the module's own factors, leaving §7 with
no problem at all. Both are rewritten.

## 2. Blocking defects

Ranked: reader-stopping structure first, then wrong results, then models used but
never stated, then missing scaffolding, then problem depth.

### B1. Every in-text figure number is off by two

Location: `module05.html:73` and `module05.html:93`.

Two decorative `<figure>` elements sit before the first `<h2>`: a triceps-surae
banner after the subtitle, and a pennation banner inside `<div class="toc">`.
Neither is referenced from the prose. The stylesheet numbers every `<figure>`:

```
counter-reset: fig;            /* line 18  */
figure{ counter-increment: fig; }   /* line 35 */
figcaption::before{ content:"Fig. " counter(fig) ". "; }  /* line 37 */
```

So the first referenced figure renders as **Fig. 3** while the prose calls it
Fig. 1, and the offset carries through all 33 references. Confirmed by decoding:
the figure the prose calls "Fig. 12" is the fourteenth `<figure>`, "Fig. 17" the
nineteenth, "Fig. 26" the twenty-eighth.

Fails part 5 (the tie to something concrete: a figure reference that lands on the
wrong figure is worse than none) and the house rule that every figure is
referenced from the prose.

Fix: keep both graphics, drop the `<figure>`/`<figcaption>` wrapper so they stop
counting. Replacement pattern (applied to both):

```html
<div style="text-align:center;margin:1.5rem 0">SVG-UNCHANGED<p class="small" style="font-style:italic;margin:.35rem 0 0">ORIGINAL-CAPTION-TEXT</p></div>
```

### B2. The excitation model that produces §3 and §4 is never written down

Location: `module05.html:826`.

Quoted: "which is exactly the activation dynamics §5 will formalise".

The twitch of Fig. 12, the four tetanus traces of Fig. 15, the force-frequency
curve of Fig. 17, the ceiling $a_\infty\approx0.73$, and K2's and K10's answers
all come from a calcium-pulse shape with four constants ($\tau_r$, $\tau_d$,
$\mathrm{Ca}_{\text{rest}}$, $\mathrm{Ca}_{\text{peak}}$) that appear nowhere.
Fails parts 1, 2 and 3: no precise statement, undefined constants, nothing a
reader can reproduce.

Replacement (inserted before the quoted clause; the clause is retained, reworded
to "The relaxation above is exactly the activation dynamics …"):

```html
<div class="def"><b>Modelling assumption 3.2 (the calcium pulse and its constants).</b> One impulse releases a calcium pulse whose normalised shape is the difference of a fast release and a slow re-uptake, the two processes drawn in Fig.&nbsp;9:
$$p(t)=\frac{1}{p_{\max}}\Big(1-e^{-t/\tau_r}\Big)e^{-t/\tau_d},\qquad t\ge 0,$$
with a release constant $\tau_r=3.6\ \mathrm{ms}$ (RyR opening) and a re-uptake constant $\tau_d=18\ \mathrm{ms}$ (SERCA pumping); $p_{\max}$ normalises the peak to $1$, which the shape reaches at $t=\tau_r\ln(1+\tau_d/\tau_r)=6.4\ \mathrm{ms}$. The free calcium is then $[\mathrm{Ca}^{2+}](t)=\mathrm{Ca}_{\text{rest}}+(\mathrm{Ca}_{\text{peak}}-\mathrm{Ca}_{\text{rest}})\,p(t)$ with $\mathrm{Ca}_{\text{rest}}=0.1\ \mu\mathrm M$ and $\mathrm{Ca}_{\text{peak}}=1.4\ \mu\mathrm M$, and the activation follows the relaxation above with $\tau_a=41\ \mathrm{ms}$. These four constants are <em>assumed</em>, chosen so the twitch matches the measured fast-fibre features quoted below; K10 estimates $\tau_a$ from those features instead. Every computed number in this section and in <a class="secref" href="#recruitment">&#167;4</a> comes from integrating this model, and the code is in K2's solution.</div>
```

Verified: integrating this model at $\tau_a=41$ ms gives peak $a=0.2248$,
time-to-peak 24.82 ms, half-relaxation 38.07 ms, and $a_\infty(1.4\,\mu\mathrm M)
=0.7329$ (`ver2.py`, `ver3.py`; features stable to 0.05 ms across step sizes
0.05 to 0.005 ms).

### B3. Fig. 30 is drawn for maximal forces that contradict §1

Location: `module05.html:1124` (figure and caption), `module05.html:1126`.

Quoted caption: "Here that puts more force on the stronger brachialis
($F_{br}\approx144$&nbsp;N) than the biceps ($F_{bi}\approx57$&nbsp;N)".

Decoded from the SVG: the blue constraint line runs from $(0,235)$ to $(147,0)$,
so $d_{bi}=4.0$ cm, $d_{br}=2.5$ cm, $\tau=5.89$ N m; the innermost gold ellipse
has semi-axes 70.7 and 141.4 N, a ratio of exactly 1:2. The tangency of that
ellipse with that line is $(57.4, 143.6)$, which is the caption's pair. But §1
computes $F_{bi,\max}=135$ N and $F_{br,\max}=210$ N, a ratio of 1:1.56. The
figure answers a different problem from the one the module set. A factual error,
and it fails part 5.

Solving $F_i\propto d_iF_{i,\max}^2$ against $d_{bi}F_{bi}+d_{br}F_{br}=5.886$
gives $F_{bi}=75.65$ N and $F_{br}=114.41$ N, relative stresses 0.560 and 0.545,
total 190.06 N (`genfigs.py`). Figure regenerated from those inputs.

Replacement caption text (the sentence-level fix inside the existing
`<figcaption>`):

```html
so infinitely many force pairs on the blue <em>torque constraint</em> line produce the required $\tau$. Its inputs all come from this module: $F_{bi,\max}=135\ \mathrm N$ and $F_{br,\max}=210\ \mathrm N$ from <a class="secref" href="#architecture">&#167;1</a>, moment arms $d_{bi}=4.0$ and $d_{br}=2.5\ \mathrm{cm}$ (<em>assumed</em>), and the $\tau=5.89\ \mathrm{N\,m}$ of the $2\ \mathrm{kg}$ dumbbell above. The nervous system is thought to pick the least-stressed combination, minimising $\sum(F_i/F_{i,\max})^2$ &#8212; the smallest gold cost ellipse that still touches the line (its tangent point). Solving $F_i\propto d_iF_{i,\max}^2$ against the constraint gives $F_{bi}=76$&nbsp;N and $F_{br}=114$&nbsp;N, leaving both at nearly the same relative stress ($0.56$ and $0.54$).
```

And, after the figure (line 1126), the point the original never draws:

```html
Note the price of sharing: the pair carries $76+114=190\ \mathrm N$ where a single muscle on the $4\ \mathrm{cm}$ arm would need $147\ \mathrm N$, because the brachialis pulls at a shorter arm. Minimising stress is not minimising force.
```

### B4. K10's fitted time constant is not what the fit returns

Location: `module05.html:1421` (statement), `1423` (solution), `1421` (figure).

Quoted: "recovers $\boxed{\tau_a\approx41.5\ \mathrm{ms}}$ (giving
$t_{\text{pk}}=25.2$, $t_{\text{half}}=40.0\ \mathrm{ms}$)". The figure's own
label and `aria-label` repeat "41.5 ms".

Minimising $(t_{\text{pk}}-25)^2+(t_{\text{half}}-40)^2$ over $\tau_a$ returns
**43.71 ms**, and it is 43.71 ms that produces the quoted $t_{\text{pk}}=25.2$
and $t_{\text{half}}=40.0$; 41.5 ms produces neither. A factual error inside the
one problem whose subject is parameter estimation.

The solution is replaced with the code (`new/k10.py`, printed output
`fitted tau_a = 43.7 ms / peak a 0.215, time to peak 25.2 ms, half-relaxation
40.0 ms`) and this text:

```html
<p>which prints <code>fitted tau_a = 43.7 ms</code> with <code>peak a 0.215, time to peak 25.2 ms, half-relaxation 40.0 ms</code>. So $\boxed{\tau_a\approx43.7\ \mathrm{ms}}$, against the $41.0\ \mathrm{ms}$ Modelling assumption 3.2 assumed &#8212; a $6.6\%$ discrepancy, and it is not numerical error (the features move by under $0.05\ \mathrm{ms}$ between step sizes $0.05$ and $0.005\ \mathrm{ms}$). The forward model with $\tau_a=41\ \mathrm{ms}$ produces a half-relaxation of $38.1\ \mathrm{ms}$, not the $40\ \mathrm{ms}$ measured, so the fit lengthens $\tau_a$ until the tail matches and pays for it with a slightly late peak and a slightly low amplitude. Two scalar features are a lossy summary of a whole trace, and both of them also depend on the calcium constants $\tau_r$ and $\tau_d$, which the fit holds fixed; the estimate absorbs part of their contribution into $\tau_a$. That is the general lesson of an inverse fit: what you recover is the parameter <em>conditioned on everything you froze</em>, and reporting it without that condition overstates what the twitch measured.</p>
```

The figure is regenerated (`genfig2.py`, key `pK10`) with the fitted curve, both
fitted features marked, and the label corrected to 43.7 ms.

### B5. K6's solution gives the wrong reason for the strength peak

Location: `module05.html:1407`.

Quoted: "The joint is therefore strongest where <em>neither</em> factor alone is
maximal".

With $\ell(\theta)/\ell_0=1-0.003(\theta^\circ-70)$, the fibre sits on the
length-tension **plateau** ($0.963\le\ell/\ell_0\le1$) for the whole interval
$[70^\circ, 82.3^\circ]$, so $f_L$ *is* at its maximum at the strength peak. The
peak is at $82.3^\circ$ because the plateau's far edge is where the falling $f_L$
first bites (`new/k6.py`). A wrong statement, and it teaches the wrong lesson.

Replacement (with `new/k6.py` spliced in above it):

```html
<p>With $\ell(\theta)/\ell_0=1-0.003(\theta^\circ-70)$ the fibre sits at $\ell_0$ at $\theta=70^\circ$ and stays on the length&#8211;tension <em>plateau</em> ($0.963\le\ell/\ell_0\le1$) all the way to $\theta=82.3^\circ$; below $70^\circ$ it is on the descending limb and above $82.3^\circ$ on the ascending limb. The moment arm $d_m=1.8+2.2\sin\theta$ rises monotonically to $90^\circ$. So on $[70^\circ,82.3^\circ]$ the product is $1\times d_m(\theta)$, still rising, and beyond $82.3^\circ$ the falling $f_L$ beats the flattening $d_m$: the strength peaks at $\boxed{82.3^\circ}$, at $3.98\ \mathrm{cm}$ of effective arm, the far edge of the plateau. The lesson is not that neither factor is maximal there &#8212; $f_L$ <em>is</em> at its maximum across the whole plateau &#8212; but that a flat factor hands the choice of optimum entirely to the other one. Read either curve alone and you would place the strongest angle at $70^\circ$ or at $90^\circ$; both are wrong.</p>
```

### B6. Lab 1's quoted output is not what Lab 1 prints

Location: `module05.html:1197`.

Quoted: `<code>peak torque 13.3 N m at t = 0.76 s</code>`. Running the block as
shipped gives 13.3504 N m at t = 0.758 s, which its own `f"{...:.1f}"` prints as
**13.4**. Decoding the Fig. 34 lower panel independently gives a peak of
13.34 N m at 0.752 s (tick map 3 N m per 17 px, 306.7 px per second), so the
figure agrees with the code and the prose does not.

Replacement: `<code>peak torque 13.4 N m at t = 0.76 s</code>`.

### B7. Live HTML inside the Lab 1 code block

Location: `module05.html:1153, 1158, 1168, 1172, 1180`.

Five `<a class="secref" …>§N</a>` tags sit inside the `<pre><code>` block, e.g.
`# activation ODE constants (s), <a class="secref" href="#activation">§5</a>`.
The copy button hands the reader text that is not Python. Fails part 5.

Replacement: each becomes a plain comment, `# activation ODE constants (s),
sec. 5`, and likewise for `sec. 2`, `sec. 6`, `sec. 8`, `sec. 5`.

### B8. Proposition 3.1 and Proposition 6.1 are asserted beside proved siblings

Location: `module05.html:794` (Prop. 3.1), `module05.html:1014` (Prop. 6.1).

Quoted (3.1): "an empirical fit to titration data, taken as given here rather
than derived from the underlying binding kinetics, which is why it is stated as a
cited relation and not proved."

Quoted (6.1): "This hyperbola is an empirical fit to Hill's heat-and-work
measurements, taken as given here rather than derived …".

Both are boxed constitutive results of the same weight as the proved sarcomere
overlap law, so under the sibling rule of `EDITOR_DOMAIN.md` both owe a proof.
Both have one in the smallest setting.

3.1 is proved from all-or-none cooperative binding: one equilibrium
$T+n\,\mathrm{Ca}^{2+}\ \rightleftharpoons\ T\!\cdot\!\mathrm{Ca}_n$ with
$K_d=[T][\mathrm{Ca}]^n/[T\!\cdot\!\mathrm{Ca}_n]$ gives
$a_\infty=[\mathrm{Ca}]^n/(K_d+[\mathrm{Ca}]^n)$ with $Ca_{50}=K_d^{1/n}$; the
limit case $n=1$ is the ordinary isotherm, too gentle to switch, and the price of
the approximation is that the fitted $n$ is apparent, not a site count.

6.1 is proved from Hill's own two measurements: shortening heat rate $a_Hv$ and
the linear energy-rate law $Fv+a_Hv=b_H(F_0-F)$. Add $b_H(F+a_H)$ to both sides
and the left factors into $(F+a_H)(v+b_H)=(F_0+a_H)b_H$. The hypothesis binds at
steady shortening, so the hyperbola says nothing about the transient after a load
step. Full replacement `<div class="proof">` blocks are in `apply.py`, tags B7a
and B7b. (The equilibrium arrow is written as `&#8652;`; `\rightleftharpoons`
trips `checktex`'s `\left`/`\right` balance test on its `\right` prefix, the same
false positive `CLAUDE.md` records for `\leftrightarrow`.)

### B9. The parallel elastic element has no constitutive law

Location: `module05.html:1064`.

Quoted: "The passive force is negligible up to about the optimal length, then
climbs steeply, like a rubber band taken up past its slack."

Fig. 28 draws the passive curve, §7's assembled model adds it to the contractile
force, and K7 needs it, but no equation is given. Decoding the green polyline in
Fig. 28 recovers exactly the exponential law with $k_{PE}=3$ and
$\varepsilon_0=0.6$: 0.076 at $1.18\,\ell_0$ (law: 0.0765), 0.201 at
$1.32\,\ell_0$ (law: 0.207), 1.000 at $1.6\,\ell_0$ (law: 1.000). The law was
used and never stated. Fails parts 1 and 3.

Replacement:

```html
<p>The curve drawn above is the exponential law the module uses throughout, stated once here so every later figure and lab can be reproduced:</p>

<div class="keyresult">$$\boxed{\;\frac{F_{PE}(\ell)}{F_{\max}}=\begin{cases}0, & \ell\le\ell_0,\\[6pt]\dfrac{e^{\,k_{PE}(\ell/\ell_0-1)/\varepsilon_0}-1}{e^{\,k_{PE}}-1}, & \ell\gt\ell_0,\end{cases}\;}$$</div>

<p>with a shape constant $k_{PE}=3$ and a reference strain $\varepsilon_0=0.6$, both <em>assumed</em> (Appendix). The two constants have a plain reading: $\varepsilon_0$ is the stretch beyond $\ell_0$ at which the passive tension alone equals $F_{\max}$ (here $60\%$, so $\ell=1.6\,\ell_0$, the right-hand edge of the figure), and $k_{PE}$ says how much of that rise is saved for the last part of the stretch. At $\ell=1.2\,\ell_0$ the law gives $F_{PE}=0.090\,F_{\max}$, at $1.4\,\ell_0$ it gives $0.335\,F_{\max}$: passive force is negligible near the optimum and then climbs steeply, like a rubber band taken up past its slack. The element is called <em>parallel</em> because it bears load side by side with the contractile element, so the two tensions simply add.
```

### B10. The eccentric shape constant $k$ is named but never valued

Location: `module05.html:1020`.

Quoted: "with curvature $c=a_H/F_0\approx0.25$, an eccentric plateau
$f_{\text{ecc}}\approx1.5$, and a shape constant $k$."

Lab 1's code uses `1 + 0.5*20*(-v)/(1 + 20*(-v))`, i.e. $k=20$, and decoding
Fig. 24's eccentric branch confirms it (1.428 at $v=-0.3$ against the law's
1.4286, 1.461 at $v=-0.55$ against 1.4615). The prose's own claim — eccentric
force climbs about twice as steeply as concentric force falls — fixes $k$
exactly, so it should be derived, not left blank.

Replacement:

```html
<p>with curvature $c=a_H/F_0\approx0.25$ and an eccentric plateau $f_{\text{ecc}}\approx1.5$. The concentric branch falls from $f_V=1$ at isometric to $0$ at $v_{\max}$; the eccentric branch <em>rises</em> above $1$, levelling near $1.5\,F_0$. The join at $v=0$ is a kink, not a smooth peak, and the shape constant $k$ is what fixes how sharp it is. Differentiate each branch at $v=0$: the concentric slope is $-(1+1/c)/v_{\max}$ and the eccentric slope is $-(f_{\text{ecc}}-1)k/v_{\max}$. Requiring the eccentric branch to climb twice as steeply as the concentric branch falls gives
$$k=\frac{2\,(1+1/c)}{f_{\text{ecc}}-1}=\frac{2\,(1+4)}{0.5}=20,$$
the value every eccentric curve in this module and the labs of <a class="secref" href="#labs">&#167;9</a> use. So a muscle gives up force reluctantly as it shortens but gains it readily as it is stretched.</p>
```

Independently confirmed by `new/k4.py`, which prints the numerical slope ratio at
$v\to0$ as exactly 2.00.

### B11. Lab 1's fibre-length map, moment-arm law and $F_{\max}$ live only in the code

Location: `module05.html:1143, 1147`.

The lab's parameter table lists $F_{\max}$ and $\theta(t)$ but not
$\ell(\theta)/\ell_0=1-0.003(\theta^\circ-70)$ or
$d_m(\theta)=1.8+2.2\sin\theta$ cm, both of which the reader needs for K6, K7 and
every torque number. And $F_{\max}=500$ N is presented as "peak isometric force
(§1)" when §1 computes 135 N for the biceps; it is a lumped-group assumption.
Bare numbers under `EDITOR_DOMAIN.md`'s three-class rule.

Replacement rows:

```html
<tr><td>$\ell(\theta)/\ell_0$</td><td>$1-0.003\,(\theta^\circ-70)$</td><td>fibre length from joint angle; <em>assumed</em> linear, optimal at $\theta=70^\circ$</td></tr>
<tr><td>$d_m(\theta)$</td><td>$1.8+2.2\sin\theta\ \mathrm{cm}$</td><td>moment arm; <em>assumed</em> form, peak $4\ \mathrm{cm}$ at $90^\circ$ (<a class="secref" href="#torque">&#167;8</a>)</td></tr>
```

and, for $F_{\max}$: "peak isometric force of the <em>lumped</em> elbow flexor
group; <em>assumed</em>, sitting inside the several hundred newtons §1 estimates
for biceps + brachialis + brachioradialis".

Decoding Fig. 31 confirms the moment-arm law: 1.80 cm at $0^\circ$, 3.64 at
$57^\circ$ (law 3.645), 4.00 at $90^\circ$.

### B12. §8's lever ratio is wrong and its load arm collides with §0

Location: `module05.html:1098`.

Quoted: "the muscle's moment arm is roughly a tenth of the load's, so it pays
roughly tenfold in force." With $d_m=4$ cm and $r=30$ cm the ratio is a seventh,
and the forces quoted in the same sentence (147 N against 19.6 N) are a factor
7.5. The load arm is also called $r_m$ here and $r_L$ in §0, and §0 uses
$d_m=3$ cm where §8 uses 4 cm with no reconciliation.

Replacement: rename to $r_L$, correct the ratio, and add the reconciliation
paragraph:

```html
<p>One number needs reconciling before we go on. <a class="secref" href="#origin">&#167;0</a> took the elbow flexor moment arm as $d_m\approx3\ \mathrm{cm}$, the constant Module&nbsp;1 carries for its reference human; here it is $4\ \mathrm{cm}$. Both are right, at different angles: Module&nbsp;1's $3\ \mathrm{cm}$ is a single value chosen to stand for the whole flexion range, while $4\ \mathrm{cm}$ is the peak of the angle-dependent curve of the next subsection, reached near $90^\circ$. Wherever this module quotes a single moment arm it means the value at the stated angle, and the curve $d_m(\theta)$ below supersedes the constant.</p>
```

### B13. §3's validation quotes a half-relaxation the model does not produce

Location: `module05.html:857`.

Quoted: "The computed twitch has a time-to-peak of ${\sim}25$ ms and a
half-relaxation of ${\sim}40$ ms". The model gives 24.8 ms and **38.1 ms**
(stable across four step sizes), and the drawn Fig. 12 agrees with 38, not 40.

Replacement: "The computed twitch has a peak activation $a=0.22$, a time-to-peak
of $24.8$ ms and a half-relaxation of $38.1$ ms (Modelling assumption 3.2
integrated; the code is in K2's solution) &#8212; squarely in the measured
range".

### B14. C6's figure cannot show what C6 asks about

Location: `module05.html:1320` (figure), `module05.html:1313` (C4's aria-label).

C6 asks why force lags the command at onset and lingers after release. Its figure
is a single monotone rising curve, shared byte-for-byte with C4, D6 and D10
(MD5 of the polyline string is identical across all four). It shows no command
trace and no release, so neither the lag nor the linger is visible. Fails part 5.

Replacement: a new two-trace figure (`genfig2.py`, key `pC6`) drawing the
rectangular command on from 20 to 140 ms in blue and the activation in red,
integrated with $\tau_{\text{act}}=10$ ms and $\tau_{\text{deact}}=40$ ms.
Verified against the closed form: $a(40\ \mathrm{ms})=0.876$ against
$1-e^{-2}=0.865$, $a(160\ \mathrm{ms})=0.603$ against $e^{-0.5}=0.607$.

C4's shared figure is correct for C4 (it rises from the single-twitch value 0.22
to the ceiling 0.73, which is exactly C4's answer) but its `aria-label` reads
"twitch relaxing toward ceiling", which describes neither. Relabelled to
"Activation climbing toward the fused-tetanus ceiling: successive twitches sum
from the single-twitch value 0.22 up to the calcium ceiling a-infinity of 0.73,
drawn as the dashed line."

### B15. K7 tested none of the module, and §7 had no problem at all

Location: `module05.html:1409` (statement), `1411` (solution), `1410` (figure),
`1293-1294` (coverage table).

Quoted: "a one-DOF limb $I\ddot\theta=a\,\tau_{\max}-k\theta-b\dot\theta$". No
$f_L$, no $f_V$, no moment arm, no pennation: the problem integrates a linear
second-order system that could appear in any module. The coverage table records
"§7 Hill model — — —", so the module's assembled result was probed by nothing.

Rewritten as a regime comparison: integrate the *assembled* §7 model on the same
limb and compare it with the constant-torque shortcut. The full replacement
statement and solution are in `apply.py`, tags B10c/B10d; the figure is
regenerated (`genfigs.py`, key `pK7`) to draw both trajectories.

Verified (`new/k7.py`): shortcut equilibrium 50.1°, overshoot 16.1%, settling
0.65 s, $\zeta=0.50$; assembled model equilibrium 63.4° (root-finding: 63.45°),
**no overshoot**, settling 1.47 s, torque-angle slope 5.24 N m rad⁻¹, effective
stiffness 4.36 N m rad⁻¹, $\zeta$ from the reduced stiffness alone 0.74. The
coverage table row for §7 now reads K7, and K7 is removed from the §8 row.

### B16. K4 was two substitutions into the boxed $f_V$

Location: `module05.html:1397` (statement), `1399` (solution).

Quoted solution: "$f_V$ is $0.32$ concentric ($v=+0.3$) but $1.43$ eccentric
($v=-0.3$)". Two evaluations of a boxed formula: exactly the busywork the §10
retrofit was supposed to remove, and exactly what `EDITOR_DOMAIN.md` calls a
defect at this level.

Rewritten as a sweep with both limit cases. Verified (`new/k4.py`): ratio 2.07 at
$|v|=0.1$, 4.49 at 0.3, 8.73 at 0.5, 18.58 at 0.7, 67.79 at 0.9; first reaches 3
at $|v|=0.19$; $\to1$ as $v\to0$ with a slope ratio of exactly 2.00; diverges as
$v\to v_{\max}$ because $f_V\to0$ concentrically while the eccentric branch is
still climbing.

The metabolic claim ("the ATP cost per unit force is far lower") is kept but
relabelled: it does not follow from the force-velocity curve, since the work per
unit tension-time integral is $|v|v_{\max}$ in both directions. It is an
assumption imported from Hill's heat measurements, and the replacement says so.

### B17. Eight K solutions carry no code under a header claiming otherwise

Location: `module05.html:1383`.

Quoted: "not substitution into a boxed formula; every answer is Python-verified."
Of the ten K solutions, only K2's and K10's mentioned any computation and neither
showed code; the module contains just two `<pre><code>` blocks in total, both in
§9. This is the same defect class recorded for Module 14.

Fix: nine new PEP8 code blocks spliced into K1, K2, K3, K4, K5, K6, K7, K8, K9
and K10, each printing the numbers its solution quotes. `check_code.py` now
reports 12 blocks, 0 issues. The header sentence is replaced with a claim that is
true:

```html
an inverse problem, or a sensitivity sweep &#8212; not substitution into a boxed formula. Every number below was printed by the code shown with the problem; the two that carry no code (K1's optimum and K9's endurance times) are closed forms derived in the solution and confirmed by the code in K3 and K9.</p>
```

### B18. K9 asserts a threshold and two times with no derivation, and the threshold is wrong

Location: `module05.html:1419`.

Quoted: "Below $F_t\approx0.5$ the steady capacity stays above the target".

Substituting $a=F_{\text{hold}}/C$ makes the fatigue equation linear:
$\dot C=-F_fF_{\text{hold}}+F_r(1-C)$, so $C(t)=C_\infty+(1-C_\infty)e^{-F_rt}$
with $C_\infty=1-(F_f/F_r)F_{\text{hold}}$, and the hold is sustainable exactly
below $F_r/(F_r+F_f)=\mathbf{0.526}$, not 0.5. The endurance times follow in
closed form: 67.5 s at 0.6, 32.3 s at 0.7, 16.3 s at 0.8, 6.6 s at 0.9
(`new/k9.py`; simulation and closed form agree to the printed digit).

### B19. The module never places itself on the level ladder

Location: `module05.html:234` (§0), `module05.html:1252` (captures/misses table).

`EDITOR_DOMAIN.md` requires each module to state which level its models sit on.
Added to §0: every model here is **Level 5** (muscle-tendon actuator models),
with the labs prescribing joint kinematics rather than integrating the limb, so
nothing is a Level-2 planar rigid-body result except K7. The captures/misses row
for "prescribed joint kinematics" now names the same thing.

### B20. Symbol collisions

Location: `module05.html:342, 374, 376, 384` ($F_f$), `1385, 1387` ($t$),
`1370, 1372` ($a$, $b$), `1417` ($F_t$).

- $F_f$ is the fibre force in §1 and the **fatigue rate** in §9. Renamed
  $F_{\text{fibre}}$ in §1 (four places, prose and the SVG `aria-label`), since
  §9's $F_f$/$F_r$ pair is used in both labs and both figures.
- $F_t$ is the tendon force in §1 and the **held force target** in K9. K9's is
  renamed $F_{\text{hold}}$; §1's tendon-directed component is written out rather
  than named.
- $t$ is time everywhere and the **belly thickness** in K1. K1's is renamed $h$.
- $a$ and $b$ are activation and the Hill constant everywhere, and **two
  distances** in D8. D8's are renamed $r_1$, $r_2$.

### B21. Appendix: wrong values, and about a dozen numbers with no row

Location: `module05.html:1438-1475`.

Quoted: "$F_{\max}$: biceps / quadriceps / gastrocnemius — $\sim135$ N /
$\sim10^3$ N / $\sim10^3$ N" and "Pennation $\theta_p$: biceps / quadriceps /
gastrocnemius — $\sim0^\circ$ / $\sim15^\circ$ / $\sim15$–$30^\circ$".

§1's own table gives four muscles with specific PCSAs and pennations; computing
$\sigma\,\mathrm{PCSA}\cos\theta_p$ from them gives 135, 861, 1360 and 4400 N,
not "$\sim10^3$" twice, and the quadriceps figure of $\sim10^3$ N is out by a
factor of 4.4. Both rows are replaced with the four-muscle versions, and thirteen
rows are added for numbers the text uses with no table entry: PCSA values, muscle
density, the maximal elbow-flexion torque, the filament lengths, the resting and
peak calcium, $\tau_r$ and $\tau_d$, $\tau_a$, the three twitch features, the
tetanus ceiling, $k=20$, $k_{PE}$ and $\varepsilon_0$, and the fatigue rates
(flagged as rates, not forces).

The notation table gains $F_0$, $k$, $\theta$, $r_L$, $\lambda$, $I_J$, $k_J$,
$b_J$, $m$, $V$, $\rho$, $L_f$, $h$, $p(t)$, $\tau_r$, $\tau_d$, $I$, $R$,
$\Delta V$, $F_{\text{hold}}$, $k_{PE}$ and $\varepsilon_0$.

### B22. The fatigue sensitivity confuses capacity with force

Location: `module05.html:1231`.

Quoted: "The steady force under sustained effort is $F_r/(F_r+F_f\,a)$".

That expression is the steady **capacity** $C_\infty$; the steady force is
$a\,C_\infty$. At $a=0.9$: $C_\infty=0.552$, force 0.497. The run reaches 0.543
at 60 s because the hold ends before the capacity has settled — a point worth
making, and the replacement makes it.

## 3. Style and clarity edits

| tag | line | change |
|---|---|---|
| S9a | 324 | "it is remarkably constant" → "it varies by less than a factor of two" (the module's own range is 0.2–0.35 MPa, a factor 1.75; "remarkably constant" is hype over a stated spread) |
| S9b | 904 | "and the remarkable thing is that the nervous system does not have to *arrange* it" → "and the nervous system does not have to *arrange* it" |
| S9c | 914 | "Fine motor resolution is a free gift of $\Delta V=IR$." → "Fine motor resolution follows from $\Delta V=IR$ alone." |
| S9d | 1036 | "which is precisely what gear ratios … exist to arrange" → "which is what gear ratios … exist to arrange" |
| S16 | 386 | "The table spans the range …:" gains a sentence naming which columns are measured and which is computed by (1.3) |
| S4 | 1395 | K3: "**nearly triples** peak power" → "multiplies peak power by **2.5** ($0.134/0.054$)" |
| S7a | 928 | §4: "$\bar a\approx0.39$" at 25 Hz → $0.38$ (computed 0.380) |
| S7b | 938 | the fusion frequency sentence now names K2's swept value, 42.5 Hz |
| S12a | 1229 | "sags to little more than half its start (to ${\approx}0.54$)" → "falls to $60\%$ of its starting value in one minute ($0.90$ to $0.54$)" (0.543/0.9 = 0.604; "little more than half" understates it) |
| S12b | 1231 | "force sags to little more than half within a minute" → "force falls by $40\%$ within a minute" |
| S14 | 1415 | K8 gains the totals: 351 N against 250 N, so min-stress spends 40% more total force to hold all three at 0.17/0.18/0.15 |

## 4. Structural notes

- **The figure counter is the one thing a reader cannot work around.** Fixing it
  by un-wrapping the two banners (B1) is the smallest change; the alternative,
  renumbering 33 in-text references, is larger and leaves two unreferenced
  figures in the count.
- **Problem figures are shared across problems.** Four problems (C4, C6, D6, D10)
  used one identical polyline, three (C7, D3, D4) share the $f_V$ curve, and two
  pairs (C8/D9, C10/D7) share a plot. Only C6's was actually wrong, and only that
  one is replaced; the others are the same curve serving the same content, which
  is defensible. But a reader meeting the same picture four times learns less
  than one meeting four pictures, and this is worth a pass if the module is ever
  revisited.
- **§7 is the module's summit and had no problem.** K7 now probes it. §5 still
  carries only K5; §2 only K6. The coverage table is now accurate about this.
- **The `<details class="sol">` solutions are long.** Adding code to nine of them
  pushes the file from 388 KB to 419 KB, which trips `check_svg.py`'s new
  large-file advisory. That is the cost of making the "Python-verified" claim
  true, and I judged the trade worth it.

## 5. What already works

- **The sarcomere overlap derivation.** The length-tension curve is built from
  filament lengths, not asserted, and decoding the drawn polyline returns exactly
  the piecewise law: zero below 1.27 µm, plateau 2.60–2.70, zero at 4.21.
- **The size principle.** One line of $\Delta V=IR$ produces the recruitment
  order, and the figure that follows is honest about what it shows.
- **Both labs.** Lab 1's activation trace, torque trace and command trace all
  decode to the code's own output (command reaches 0.85 at 0.27 s, activation at
  0.32 s, torque peaks 13.34 N m at 0.752 s). Lab 2's capacity curve decodes to
  1.000, minimum 0.603 at 60 s, 0.878 at 120 s, against the code's 1.000, 0.6034,
  0.8805. These are the two places the module already met the standard it claims
  everywhere.
- **The step-response figure (Fig. 21).** Decodes to $1-e^{-t/10}$ on the rise
  and $e^{-t/40}$ on the fall, to three digits. It is the clearest single
  demonstration in the module of a stated model matching a drawn curve.
- **Fig. 24, the force-velocity curve.** Both branches decode to the boxed law
  with $c=0.25$, $f_{\text{ecc}}=1.5$, $k=20$ — which is how the missing $k$ in
  B10 was recovered.
- **The §0 motivation.** Four numbered failures of the cable picture, each one
  answered by a later section. It is the shape the domain brief asks for.
