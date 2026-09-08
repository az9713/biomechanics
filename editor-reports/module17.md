# Editor report: module17.html (Capstone Modeling Projects)

Editorial pass. Standard: the five-part rule of the `science-editor` skill, read against `EDITOR_DOMAIN.md`. Every location is `module17.html:LINE`. Every replacement is valid HTML with MathJax delimiters and uses only the box classes the stylesheet defines (`.def`, `.cap`, `.keyresult`, `.prob`, `.sol`, `.proof`, `.prop`). All three Python blocks in the shipped file were extracted and run (`extract.py` into `m17/blocks/`); all three run clean and none contains a live HTML tag. Every number in a replacement below was printed by code in the session scratchpad, folder `m17/`: `verify.py` (arithmetic audit of all six capstones), `delay.py` (the stability boundary, analytically and by simulation at four time steps), `walk.py` (the inverted-pendulum GRF, integrated), `figs.py` / `figs2.py` (every plot decoded from its own tick calibration and tested against its caption), `newcode.py` and `mkblocks.py` (the eight replacement code blocks, each run and each checked with `pycodestyle`).

## 1. Verdict

Yes, after revision. This is the course's closing module and its structural idea is the right one: an eleven-element template, three principles, six worked projects that each fill the template in, nine briefs, and a section on validation that most textbooks omit. A graduate reader can learn the modeling method from these pages, and the method is genuinely the deliverable. The projects also do span the course, which is what a capstone owes its syllabus.

What stops the reader is that the capstone module is the one module that does not hold itself to the standard it preaches. Principle 1.3 says an answer without an error bar is not a result; the module reports fourteen headline numbers without one. The template's element (6) demands "a table of values with sources and units"; there is no parameter table anywhere in the file, and `prompt.txt` requires one per capstone. Element (7) demands the simulation and its code; three of the six worked capstones have none, while the closing line claims "every number reproduced by the code shown" and §9 preaches that a simulation that runs is not a validated model.

Three results are wrong, and two of them are drawn into figures. Fig. 4 and §4 say the inverted-pendulum vault produces walking's twin-peaked M-shape. It cannot: for a rigid vault $\ddot y_{\rm COM}\lt0$ throughout single support, so Model 4.1 predicts $F\le mg$ at every instant. Integrated, the vault gives a single *hump* — its force is largest at mid-stance, at exactly $mg(1-\mathrm{Fr})=0.70$ BW, and falls to 0.49 BW by $\pm20^\circ$ of leg sweep — which is the inverse of the $\cup$ the figure draws. The two 1.18 BW peaks the figure draws, and the dip shape between them, are the step-to-step transition, which §4 itself lists among the things the model omits. The vault earns one number, the mid-stance value; it does not earn the shape. The critical delay of Capstone I is stated as 150 ms in four places; for the module's own gains the Hopf boundary is at 140.1 ms analytically and 140.2 ms by bisecting the module's own integrator. Model 5.1's boxed 2.5 to 3 body weights is followed by a derivation, "$2mv_{\rm land}/t_c$", that evaluates to 0.5 to 0.75 body weights for any plausible flight time: the chain drops the weight impulse and the peak-to-mean shape factor, and the parameter line then admits the leg stiffness was "tuned so the peak is $\approx2.6$ BW", which is the answer chosen and then presented as the prediction.

Below that: Model 3.1's boxed equation is not the equation that computed 109 N·m (the code carries an unexplained factor 0.6, an absolute value, and a baseline $\tau_0$ worth 13 percent of the answer and defined nowhere), while the inertial term the box leads with is worth 0.48 N·m, four parts in a thousand. The density-squared strength law is attributed to Module 2 three times and in the Appendix; Module 2 does not contain it, and a reader following the pointer finds nothing. It is Proposition 3.1 of Module 14. Model 6.1's boxed derivation is a non-sequitur and calls the mean force a peak. Two symbols, $d$ and $I$, carry two meanings each across sections while the module carefully flags the one collision ($k$ against $k_c$) that it did catch. And the four computational problems, which are the module's only exercises with numbers, carry no code and no computed value; K1's number is the wrong one, K2's three stated scalings are all wrong by a measurable amount, K3 asks for an optimisation over a variable Model 3.1 does not contain, and K4's "$\pm15\%$" is a one-sigma spread reported as though it were the band.

None of this touches the module's argument. The template, the three principles, the validation ladder, the project catalog and the closing are sound and are what a reader takes away. Every defect below is repairable inside the existing structure, and fixing them makes the module practise its own Principle 1.3 instead of only stating it. Fourteen blocking defects and seventeen style edits follow. Three of them - the residue of B8, the unresolved half of B9, and S17 - were found on a second pass over the edited file, by grepping for the superseded wording of every replacement already applied.

## 2. Blocking defects

Ranked by severity: physics errors first (two are drawn into figures), then a boxed result whose stated derivation does not give its stated number, then boxes that disagree with their own code, then wrong attributions and bare numbers, then missing scaffolding, then the problem set.

### B1. Fig. 4 and §4 credit the inverted-pendulum vault with a force it cannot produce

Location: `module17.html:191`, `:193`, `:197`, `:199` (Fig. 4 caption), `:201`, and `:315` (C3's solution).

Quoted (line 201): "The vault produces the M-shaped vertical force of Fig. 4 (blue): a loading peak as the COM rises, a mid-stance dip <em>below</em> body weight as it crests the arc (centripetal unloading), and a push-off peak."

Factual error. Model 4.1 writes $F=m(g+\ddot y_{\rm COM})$ with the COM on a circular arc of radius $L$, so $y=L\cos\theta$ and

$$\ddot y=-L\cos\theta\,\dot\theta^{2}-L\sin\theta\,\ddot\theta=-L\cos\theta\,\dot\theta^{2}-g\sin^{2}\theta,$$

using the passive vault's $\ddot\theta=(g/L)\sin\theta$. Both terms are negative or zero for every $\theta$, so $\ddot y\le0$ and $F\le mg$ at every instant of single support.

**Correction, made on re-verification (`m17/recheck.py`, `m17/vaultchk.py`).** An earlier draft of this report stated that the vault's GRF "runs from 0.599 BW at mid-stance to 0.820 BW at the ends" and called the result "a single U". That has mid-stance and the ends **swapped**, and the shape backwards. The passive vault is *slowest* at the crest of its arc, so $|\ddot y|$ is *smallest* there: $F$ is **maximal at mid-stance** and falls monotonically toward both ends. Analytically, $\ddot y(\theta)-\ddot y(0)=(1-\cos\theta)\big[L\dot\theta_0^{2}-g(1+3\cos\theta)\big]\lt0$ for any $\mathrm{Fr}\lt4$. Integrated with $v=1.72$ m/s as the **mid-stance** speed (which is the convention the boxed $F_{\rm mid}=mg(1-\mathrm{Fr})$ requires, and the one Fig. 4 confirms): $F=0.698$ BW at mid-stance, falling to $0.643$ at $10^\circ$, $0.576$ at $15^\circ$ and $0.486$ at $\pm20^\circ$; $F\le mg$ holds at every speed tested (1.0, 1.5, 1.72, 2.0 m/s). The 0.599/0.820 pair is what you get by reading $v=1.72$ as the speed at the *ends* instead, and even then it is inverted: that convention gives 0.819 at mid-stance and 0.600 at the ends. **The vault gives a single hump, the inverse of walking's $\cup$, not a U.** The consequence for the module is larger than a word swap: the model does not predict the mid-stance *dip*, it predicts the mid-stance *value* and gets the shape wrong. The replacements below say so. Decoding Fig. 4 from its own y-ticks ($y=195.0,139.6,84.3$ for 0, 1, 2 BW; least-squares fit $y=-55.350\,\mathrm{BW}+194.983$, residual 0.033 px) gives the blue curve two peaks of 1.183 BW, a mid-stance value of 0.701 BW, and a red running peak of 2.600 BW. The peaks are real walking, but they come from the step-to-step transition (collision and push-off) of Module 8, which line 201 itself lists among the omissions two sentences later. So is the $\cup$ shape between them. What Model 4.1 does own is the mid-stance *value*: $F=mg(1-\mathrm{Fr})$ gives 0.698 BW at $\mathrm{Fr}=0.302$, that is $v=1.72$ m/s, a normal walking speed, against the 0.701 BW the figure draws there. The section has a quantitative tie to its figure and does not use it. Note the replacements below are written for the corrected reading: **one number earned, the shape borrowed** — which is a sharper teaching point than the original claim, not a weaker one.

Replacement for line 191:

```html
<p><b>Problem.</b> Why does walking unload the body at mid-stance, and what caps its speed? <b>Physical model.</b> The compass / inverted-pendulum gait: the body vaults over a stiff stance leg like a pendulum inverted (Module 8). <b>Mechanism.</b> The stance leg redirects the centre of mass along a circular arc, so part of the weight goes into curving that path instead of pressing on the ground.</p>
```

Replacement for lines 193 to 195, the whole model box (open line, boxed display, closing line). The box gains the unloading result alongside the Froude limit; the derivation is two lines and belongs here, not only in D3:

```html
<div class="def"><b>Model 4.1 (inverted-pendulum vault, mid-stance unloading, and the Froude limit).</b> Put the point-mass COM at the top of a rigid stance leg of length $L$, at angle $\theta$ from vertical, so its height is $y=L\cos\theta$ and the vertical ground reaction is $F=m(g+\ddot y)$. Differentiating twice and using the passive vault's $\ddot\theta=(g/L)\sin\theta$ gives $\ddot y=-L\cos\theta\,\dot\theta^2-g\sin^2\theta$, which is negative for every $\theta$: a rigid vault gives $F\le mg$ at <em>every</em> instant of single support. At mid-stance, where $\theta=0$, the COM crests the arc at its slowest, turning on a circle of radius $L$ at speed $v$ with $\ddot y=-v^2/L$, so
$$\boxed{\;F_{\rm mid}=mg\big(1-\mathrm{Fr}\big),\qquad \mathrm{Fr}=\frac{v^2}{gL}.\;}$$
Away from mid-stance the unloading only deepens, because the passive vault speeds up as it falls away from the crest: $F_{\rm mid}$ is the vault's <em>largest</em> force, not its smallest, and the model therefore predicts a single hump where real walking has two peaks around a dip. That mismatch is the subject of the interpretation below. The leg can push but not pull, so $F\ge0$ forces $\mathrm{Fr}\le1$: that is the Froude limit, a kinematic ceiling at which the foot carries nothing at all. Real walking gives up near $\mathrm{Fr}\approx0.5$, well below it; <a class="secref" href="#problems">D3</a> works out why the bound is not tight.</div>
```

Replacement for line 197:

```html
<div class="cap"><p class="small"><b>Assumptions:</b> rigid stance leg, point-mass COM on a circular arc, single support only, no step-to-step transition. <b>Parameters:</b> $m=70\ \mathrm{kg}$, leg $L=1.0\ \mathrm{m}$, walking speed $v=1.72\ \mathrm{m\,s^{-1}}$ (assumed; <a class="secref" href="#appendix">Appendix</a>); force normalised to body weight (BW). <b>Validation:</b> the mid-stance value $mg(1-\mathrm{Fr})=0.70$ BW and the $\mathrm{Fr}\approx0.5$ transition match measured gait; the twin peaks and the $\cup$ shape do <em>not</em> come from this model (see the interpretation below).</p></div>
```

Replacement for the Fig. 4 caption (line 199, `<figcaption>` contents only):

```html
Capstones III-IV. Walking and running ground-reaction force over one stance, at $v=1.72\ \mathrm{m\,s^{-1}}$ walking and a $0.606$ duty factor running. Walking (blue) is twin-peaked about a mid-stance dip to $0.70$ BW; Model 4.1 predicts that mid-stance <em>value</em> exactly, as $mg(1-\mathrm{Fr})$ at $\mathrm{Fr}=0.30$, but neither the two $1.18$ BW peaks nor the $\cup$ shape between them, which come from the step-to-step transition of Module 8 that a rigid vault leaves out. Running (dark red) is the spring-mass bounce, a single hump peaking at $2.6$ BW. The number of peaks and the peak height separate the two gaits (Modules 8-9).
```

Replacement for line 201:

```html
<p><b>Interpretation and limits.</b> The vault earns exactly one number, the mid-stance <em>value</em>: at $v=1.72\ \mathrm{m\,s^{-1}}$ on a $1\ \mathrm m$ leg, $\mathrm{Fr}=v^2/(gL)=0.30$ and the mid-stance force is $mg(1-\mathrm{Fr})=0.70$ BW, which is what Fig. 4 draws there. Everything else in that curve is borrowed. Integrating a rigid vault gives $F\le mg$ at every instant, because $\ddot y_{\rm COM}\lt0$ throughout the arc, and the force is <em>largest</em> at mid-stance, falling to $0.49$ BW by $\pm20^\circ$ of leg sweep: the model draws a single hump, the inverse of the measured $\cup$, and it never reaches the two $1.18$ BW peaks on either side. Those peaks, and the dip shape between them, are the <em>step-to-step transition</em>, the collision at heel-strike and the push-off that redirect the COM from one arc to the next, which Module 8 models and this idealisation omits along with knee flexion and double support. That is the honest reading of Fig. 4: one number earned, the shape borrowed. The Froude limit is the model's second result and explains why leg length sets the transition speed. <b>Validation:</b> compare the predicted mid-stance value against force-plate mid-stance minima across speeds, which tests $mg(1-\mathrm{Fr})$ directly; <b>extension:</b> add the step-to-step transition cost (Module 8) to predict the peaks and the metabolically optimal speed together, and compare the stride length each speed implies, $\ell_{\rm stride}=2L\sin\theta_{\max}$, against measured gait.</p>
```

Replacement for C3's solution (line 315):

```html
<details class="sol"><summary>Solution</summary><div>Walking is an inverted-pendulum vault: the vertical force is twin-peaked (loading and push-off) about a mid-stance dip <em>below</em> body weight, $mg(1-\mathrm{Fr})=0.70$ BW at $\mathrm{Fr}=0.30$, as the centre of mass crests its arc. Running is a spring-mass bounce: a single hump peaking near $2.6$ body weights, with the force zero during flight. The number of peaks and the peak magnitude separate the two mechanisms unambiguously. Note which feature each model owns: the vault predicts the mid-stance value, but neither the two peaks nor the dip shape between them, which are the step-to-step transition of Module 8 (<a class="secref" href="#walk">Section 4</a>).</div></details></div>
```

### B2. The critical delay is 140 ms, not 150 ms, and nothing in the module computes it

Location: `module17.html:132`, `:160` (Fig. 2 caption), `:162`, `:338` (K1's solution).

Quoted (line 162): "A $200\ \mathrm{ms}$ delay is past the critical delay $\Delta_c\approx150\ \mathrm{ms}$".

Factual error, and a number in none of the three admissible classes: it is not derived, it is in no table, and it is not labelled an assumption. Model 2.1's characteristic equation is $Is^2-mgL+(k_p+k_ds)e^{-s\Delta}=0$. On the boundary $s=i\omega$ the imaginary part gives $k_d\omega\cos\omega\Delta=k_p\sin\omega\Delta$ and the real part gives $I\omega^2+mgL=\sqrt{k_p^2+k_d^2\omega^2}$, whose square is a quadratic in $u=\omega^2$. With the module's own $I=70\ \mathrm{kg\,m^2}$, $mgL=686.70$ N·m, $k_p=1030.05$ N·m, $k_d=150$ N·m·s: $4900u^2+73638u-589446=0$, so $\omega_c=2.404$ rad/s (period 2.61 s) and $\Delta_c=\arctan(k_d\omega_c/k_p)/\omega_c=140.1$ ms (`m17/delay.py`; both residuals below $10^{-13}$). Bisecting the module's own integrator on the growth of the sway envelope confirms it: 137.5 ms at 200 Hz, 139.0 at 500 Hz, 140.2 at 2000 Hz, 140.1 at 8000 Hz (`m17/histchk.py`; an earlier draft reported 139.75 and 139.7 for the last two, from a different growth criterion — the shipped block prints 140.2 and that is what runs). The qualitative conclusion survives (140 ms is still above the human 100 ms) but the number and its status change: it becomes derived instead of asserted. For reference, $\Delta_c=150$ ms would need $k_d=161.8$ N·m·s.

Replacement for line 130, which currently ends the box with the assertion (this also supplies B14's missing limit case):

```html
with $I=mL^2$, gravitational toppling term $mgL\,\theta$ (unstable), and a delayed restoring torque of gains $k_p$ (units N&#183;m) and $k_d$ (units N&#183;m&#183;s). Without delay the equation is $I\ddot\theta+k_d\dot\theta+(k_p-mgL)\theta=0$, a damped oscillator, stable exactly when $k_p\gt mgL$ and $k_d\gt0$. The delay adds phase lag and erodes that stability; Proposition 2.2 says by how much. Being linear, the model has no upright to fall away from: past the boundary $\theta$ grows without bound, and that growth stops meaning "a fall" once $\theta$ leaves the small-angle range (beyond roughly $15^\circ$, where $\sin\theta$ and $\theta$ differ by more than one percent). Read a divergence as the loss of balance, not as a trajectory to the floor.</div>
<div class="prop"><b>Proposition 2.2 (the critical delay).</b> For $k_p\gt mgL$ and $k_d\gt0$ the delayed system of Model 2.1 loses stability through a pair of roots crossing the imaginary axis at $s=\pm i\omega_c$, where $\omega_c^2$ is the positive root of
$$I^{2}u^{2}+\big(2ImgL-k_d^{2}\big)u+\big((mgL)^{2}-k_p^{2}\big)=0,\qquad u=\omega^{2},$$
and the critical delay is
$$\boxed{\;\Delta_c=\frac{1}{\omega_c}\arctan\!\Big(\frac{k_d\,\omega_c}{k_p}\Big).\;}$$</div>
<div class="proof">
Substitute $s=i\omega$ into the characteristic equation $Is^2-mgL+(k_p+k_ds)e^{-s\Delta}=0$ and split into real and imaginary parts, using $e^{-i\omega\Delta}=\cos\omega\Delta-i\sin\omega\Delta$:
$$-I\omega^{2}-mgL+k_p\cos\omega\Delta+k_d\omega\sin\omega\Delta=0,\qquad -k_p\sin\omega\Delta+k_d\omega\cos\omega\Delta=0.$$
The second gives $\tan\omega\Delta=k_d\omega/k_p$, hence $\cos\omega\Delta=k_p/\sqrt{k_p^{2}+k_d^{2}\omega^{2}}$ and $\sin\omega\Delta=k_d\omega/\sqrt{k_p^{2}+k_d^{2}\omega^{2}}$ on the principal branch, both positive because $k_p$, $k_d$ and $\omega$ are. Substituting these into the first collapses its two trigonometric terms into one, $k_p\cos\omega\Delta+k_d\omega\sin\omega\Delta=\sqrt{k_p^{2}+k_d^{2}\omega^{2}}$, leaving
$$I\omega^{2}+mgL=\sqrt{k_p^{2}+k_d^{2}\omega^{2}}.$$
Squaring gives the quadratic in $u=\omega^{2}$ stated above. Its constant term $(mgL)^{2}-k_p^{2}$ is negative exactly when $k_p\gt mgL$, so the quadratic has one positive root and the crossing frequency $\omega_c$ is unique. Inverting $\tan\omega_c\Delta=k_d\omega_c/k_p$ on the principal branch returns the smallest positive $\Delta$ at which the crossing occurs, which is $\Delta_c$. <span class="qed">&#8718;</span>
</div>
<div class="keyresult"><b>Worked number.</b> With the parameters below ($I=70\ \mathrm{kg\,m^2}$, $mgL=686.7\ \mathrm{N\,m}$, $k_p=1.5\,mgL=1030.1\ \mathrm{N\,m}$, $k_d=150\ \mathrm{N\,m\,s}$) the quadratic reads $4900u^{2}+73638u-589446=0$, giving $\omega_c=2.404\ \mathrm{rad\,s^{-1}}$, a $2.61\ \mathrm s$ wobble, and $\Delta_c=140.1\ \mathrm{ms}$. The code below computes both, and <a class="secref" href="#problems">K1</a> recovers $140.2\ \mathrm{ms}$ by bisecting the simulation itself. A human loop delay of about $100\ \mathrm{ms}$ therefore stands with roughly $40\ \mathrm{ms}$ in hand.
```

Note: line 130 currently closes the `.def` with `</div>`; the replacement keeps that `</div>` as its first closing tag and then opens the new `.prop`, `.proof` and `.keyresult`. The `.keyresult` is closed by the line that follows in the replacement for line 132 (B7).

Replacement for line 132:

```html
</div>
<div class="cap"><p class="small"><b>Assumptions:</b> small angle (linearised), single ankle joint, constant gains, planar, no sensory noise. <b>Parameters:</b> $m=70\ \mathrm{kg}$, $L=1.0\ \mathrm{m}$, $k_p=1.5\,mgL$, $k_d=150\ \mathrm{N\,m\,s}$ (all assumed; <a class="secref" href="#appendix">Appendix</a>), delay $\Delta\in\{100,200\}\ \mathrm{ms}$. <b>Validation:</b> the stable sway magnitude (a few degrees) and the critical delay $\Delta_c=140\ \mathrm{ms}$ of Proposition 2.2 match Module 10 and posturography data.</p></div>
```

Replacement for the Fig. 2 caption (line 160, `<figcaption>` contents only):

```html
Capstone I. Quiet standing as a delayed inverted pendulum. Integrating the delayed-feedback balance loop from a $2.9^\circ$ lean, a 100 ms neural delay (green) is inside the stability island and the sway decays, while a 200 ms delay (red) is past the critical delay $\Delta_c=140.1$ ms of Proposition 2.2 and the oscillation grows: the red trace is drawn until it leaves the axis at $34^\circ$ and $4.7$ s, and reaches $63.2^\circ$ by $6$ s, long past the small-angle range in which the model means anything. The delay-induced instability Module 10 predicted, here derived and simulated from the equation of motion.
```

Replacement for K1's solution (line 338) is given under B11.

### B3. Model 5.1's boxed range does not follow from the derivation printed beside it, and its parameter was tuned to the answer

Location: `module17.html:207-211`, `:213`.

Quoted (line 209): "set by an impulse balance: the stance impulse must reverse the vertical flight momentum, $\int F\,dt=2m v_{\rm land}$, and spread over the short contact time $t_c$ this gives a peak of order $2m v_{\rm land}/t_c\approx2.5\text{-}3\,mg$."

Quoted (line 211): "leg stiffness tuned so the peak is $\approx2.6$ BW".

Factual error plus a circular parameter. The stated quantity does not evaluate to the stated range. With $t_c=0.20$ s and a flight time of 0.10 to 0.15 s, $v_{\rm land}=gt_{\rm fl}/2$ is 0.49 to 0.74 m/s and $2mv_{\rm land}/t_c$ is 343 to 515 N, that is 0.50 to 0.75 mg, low by a factor of about four (`m17/verify.py`, section E). Three things are missing. The stance impulse must also carry the body weight during contact, adding $mg\,t_c$. The momentum to reverse is set over the whole step, not the contact alone, so the mean stance force is $mg/\beta$ with $\beta=t_c/t_{\rm step}$ the duty factor. And a peak is not a mean: a half-sine stance profile has a peak $\pi/2$ times its mean. Put together, $F_{\rm peak}=(\pi/2)\,mg/\beta$. With $t_c=0.20$ s and $t_{\rm step}=0.33$ s, $\beta=0.606$, the mean is 1133 N (1.65 BW) and the peak is 1780 N, which is 2.59 BW: exactly the 2.591 BW the figure already draws (decoded from its own ticks, `m17/figs2.py`). The number was right; the route to it was not, and the stiffness never entered. The stiffness question is K2's, and it is a genuine one.

Replacement for lines 207 to 209 (the model box):

```html
<div class="def"><b>Model 5.1 (spring-mass stance, and the peak from a duty factor).</b> During stance the leg spring of stiffness $k$ and rest length $\ell_0$ produces a vertical force $F=k\,(\ell_0-\ell)\cos\phi$ ($\ell$ the instantaneous leg length, $\phi$ the leg's angle from vertical) that rises to a single peak at mid-stance and returns to zero at toe-off. The peak follows from an impulse balance that never mentions $k$. Over one full step of duration $t_{\rm step}$ the runner's vertical momentum returns to where it started, so the mean vertical ground force over the <em>step</em> is exactly $mg$; the ground acts only during the contact time $t_c$, so the mean force over the <em>contact</em> is $mg/\beta$ with the duty factor $\beta=t_c/t_{\rm step}$. Approximating the stance profile by a half-sine, whose peak is $\pi/2$ times its mean,
$$\boxed{\;F_{\rm peak}\approx\frac{\pi}{2}\,\frac{mg}{\beta},\qquad \beta=\frac{t_c}{t_{\rm step}}.\;}$$
With the assumed $t_c=0.20\ \mathrm s$ and $t_{\rm step}=0.33\ \mathrm s$ (<a class="secref" href="#appendix">Appendix</a>), $\beta=0.606$, the mean stance force is $1133\ \mathrm N=1.65$ BW and the peak is $1780\ \mathrm N=2.59$ BW. The leg stiffness sets <em>how</em> that peak and that contact time are produced, and trades one against the other, which is <a class="secref" href="#problems">K2</a>; it does not set the balance that fixes them.</div>
```

Replacement for line 211:

```html
<div class="cap"><p class="small"><b>Assumptions:</b> massless linear leg-spring, symmetric stance, point-mass COM, half-sine stance force profile. <b>Parameters:</b> $m=70\ \mathrm{kg}$; contact $t_c=0.20\ \mathrm s$ and step $t_{\rm step}=0.33\ \mathrm s$ (assumed; <a class="secref" href="#appendix">Appendix</a>), so $\beta=0.606$; leg stiffness $k\approx10\ \mathrm{kN\,m^{-1}}$ (<a class="secref" href="#problems">K2</a>). <b>Validation:</b> the single-hump shape and the derived $2.59$ BW peak match running force-plate data (Module 9), and the duty factor is directly measurable.</p></div>
```

The code block for §5 is new; it is given in B12.

### B4. Model 3.1's box is not the equation that produced 109 N·m

Location: `module17.html:168-172`, `:174-183` (the code block), `:187`.

Quoted (line 170): "the sum of an inertial term $I\ddot q$, the gravitational load of the HAT of mass $m_{\rm HAT}$ acting through a posture-dependent moment arm $d(q)$, and a baseline."

Quoted (the code, line 182): `tau = m_hat*g*d*np.sin(q) + 0.6*Iz*np.abs(qdd) + 0.15*m_hat*g*d`

Missing parts: (1) precise statement, (2) every term defined, (5) number class. The box says $I\ddot q$; the code computes $0.6\,I|\ddot q|$, and neither the 0.6 nor the absolute value appears in the box or the prose. The box says "a baseline"; the code sets it to $0.15\,m_{\rm HAT}gd$ and the text never gives the number, the meaning, or the status. The box says $d(q)$ is posture-dependent; the code realises it as $d_0\sin q$ and the parameter line calls $d$ a constant 0.20 m. Running the decomposition (`m17/verify.py`, section B): gravity 94.18 N·m (86.8 percent of the peak), inertia 0.29 N·m (0.27 percent), baseline 14.13 N·m (13.0 percent). So the term the box names first is worth four parts in a thousand, and an undefined constant carries an eighth of the headline number. That constant is also visible in Fig. 3, whose curve ends at 13.8 N·m at full knee extension, where a standing person's knee extensor torque should be near zero. This is a Level-1 quasi-static estimate presented as the Module 15 inverse-dynamics pipeline. Dropping the 0.6 (an unexplained magic constant) leaves the peak at 108.686 N·m, which still prints 109, so no downstream number moves; this was checked before the anchors were written (`m17/walk.py`).

Replacement for lines 168 to 170:

```html
<div class="def"><b>Model 3.1 (quasi-static knee torque of the rise).</b> With a prescribed knee angle $q(t)$ measured from full extension ($q=\pi/2$ seated, $q=0$ standing), the net knee extensor torque is
$$\boxed{\;\tau_{\rm knee}(t)=m_{\rm HAT}\,g\,d_0\sin q+I_{\rm k}\,\lvert\ddot q\rvert+\tau_0,\;}$$
the sum of the gravitational load of the head-arms-trunk segment (HAT, the body above the hips) of mass $m_{\rm HAT}$ acting through the moment arm $d_0\sin q$, which is largest in deep flexion and vanishes at full extension; an inertial term with $I_{\rm k}$ the moment of inertia of the rising mass about the knee - subscripted to keep it distinct from the whole-body $I=mL^2$ about the ankle in <a class="secref" href="#standing">Section 2</a>, which is a different quantity about a different axis - taken in magnitude so that both the accelerating and the braking half of the movement count as demand; and a baseline $\tau_0$, the assumed patellofemoral and soft-tissue torque the extensors carry even at rest. The estimate is quasi-static in practice: at the parameters below the inertial term peaks at $0.48\ \mathrm{N\,m}$ against a gravitational $94.2\ \mathrm{N\,m}$, four parts in a thousand, so the answer is set almost entirely by posture. That puts Model 3.1 on <b>Level 1</b> of the course's level ladder, static equilibrium of rigid segments, and not on the full multi-segment Level 2 inverse dynamics of Module 15; it borrows Module 15's <em>pipeline</em>, kinematics in and joint torque out, at a single joint.</div>
```

Replacement for line 172:

```html
<div class="cap"><p class="small"><b>Assumptions:</b> planar, single knee joint, prescribed minimum-jerk knee trajectory over $T=1.5\ \mathrm{s}$, quasi-static gravity plus a negligible inertial term, moment arm $d_0\sin q$. <b>Parameters:</b> $m_{\rm HAT}=48\ \mathrm{kg}$ ($0.69M$ for the $70\ \mathrm{kg}$ reference human), $d_0=0.20\ \mathrm{m}$ at seat-off, $I_{\rm k}=0.12\ \mathrm{kg\,m^2}$, $\tau_0=0.15\,m_{\rm HAT}gd_0=14.1\ \mathrm{N\,m}$ (all assumed; <a class="secref" href="#appendix">Appendix</a>). <b>Validation:</b> the $1.55$ N&#183;m/kg peak matches instrumented sit-to-stand studies and Module 13's chair demand.</p></div>
```

Replacement for the code block at lines 174 to 183 (`<pre><code>` contents only; run and PEP8-checked as `m17/final/sec3.py`):

```
import numpy as np

g, T = 9.81, 1.5
t = np.linspace(0, T, 200)
s = t/T
q = (np.pi/2)*(1 - (10*s**3 - 15*s**4 + 6*s**5))   # knee 90 deg -> 0 deg
qdd = np.gradient(np.gradient(q, t), t)
m_hat, d0, Iz = 48.0, 0.20, 0.12
tau0 = 0.15*m_hat*g*d0                 # assumed baseline (Appendix)
grav = m_hat*g*d0*np.sin(q)            # d(q) = d0 sin q
iner = Iz*np.abs(qdd)
tau = grav + iner + tau0
print("peak knee torque = %.0f N m (%.2f N m/kg)" % (tau.max(), tau.max()/70))
print("  gravity %.1f, inertia %.2f, baseline %.1f N m"
      % (grav.max(), iner.max(), tau0))
# -> peak knee torque = 109 N m (1.55 N m/kg)
# ->   gravity 94.2, inertia 0.48, baseline 14.1 N m
```

Replacement for line 187:

```html
<p><b>Interpretation and limits.</b> The torque peaks at seat-off, where the knee is at $90^\circ$ and the whole upper body is cantilevered forward, at $109\ \mathrm{N\,m}$, which is $1.55\ \mathrm{N\,m}$ per kilogram of body mass (Fig. 3). Of that, $94.2\ \mathrm{N\,m}$ is the HAT weight on its moment arm, $14.1\ \mathrm{N\,m}$ is the assumed baseline $\tau_0$, and only $0.48\ \mathrm{N\,m}$ is inertia: rising from a chair is a posture problem, not an acceleration problem, and the curve falls with $\sin q$ as the knee extends. Propagating the parameter uncertainty (<a class="secref" href="#problems">K4</a>) gives a one-sigma spread of $\pm14\%$ and a 95 percent interval of $80$ to $140\ \mathrm{N\,m}$, so the honest headline is $109\ \mathrm{N\,m}$ with that interval, not $109$ alone. This is the number Module 13 tracked as a reserve: when age-thinned quadriceps can no longer supply it, the rise fails without arms or momentum. The model prescribes the kinematics rather than predicting them, lumps the trunk into one mass, and takes $\tau_0$ on assumption; a full model would solve the whole multi-segment inverse dynamics from marker data (Module 15). <b>Validation:</b> compare to force-plate and motion-capture sit-to-stand torques, and measure $\tau_0$ directly as the extensor torque at rest; <b>extension:</b> add the momentum strategy, the forward trunk lean that trades knee demand for hip demand (<a class="secref" href="#problems">K3</a>).</p>
```

### B5. The density-squared strength law is attributed to a module that does not contain it

Location: `module17.html:239` (twice), `:241`, `:367` (Appendix row).

Quoted (line 239): "The femoral neck (Module 16's bone continuum) fails when the impact stress exceeds its strength, which falls as the square of bone density (Module 2)."

Quoted (line 241): "the femoral strength scales as $S=S_0(\rho/\rho_0)^2$ (Module 2)."

Wrong cross-reference, three times in the body and once in the Appendix. `module02.html` contains no strength-density relation at all: `grep -c 'rho_0\|\\rho/\\rho\|apparent density' module02.html` returns 0, and $\rho$ in Module 2 is the radial coordinate of the polar second moment $J=\int_A\rho^2\,dA$, a different quantity entirely. The law is Proposition 3.1 of Module 14, `module14.html#osteoporosis`: "If bone compressive strength follows $S=S_0(\rho/\rho_0)^{n_{\rm b}}$ with exponent $n_{\rm b}\approx2$…", with an adjacent proof. A reader who follows the module's own pointer finds nothing and has to hunt. Fix the three body references (folded into the replacements under B6) and the Appendix row.

Replacement for line 367:

```html
<tr><td>2</td><td>Bones as structures</td><td>stress/strain, Euler-Bernoulli bending, the safety factor, fracture and fatigue, the remodeling ODE</td></tr>
```

The $S\propto\rho^2$ law moves to the Module 14 row; see B7.

### B6. §7's two headline numbers are bare, and the capstone has no code

Location: `module17.html:239`, `:241`, `:244`.

Quoted (line 244): "<b>Parameters:</b> young strength $S_0=7\ \mathrm{kN}$, impact $F\approx4.4\ \mathrm{kN}$."

Number class. Neither number is derived here, in any table, or labelled an assumption, so both fail the brief's three-class test. Both are recoverable, and Module 14 already holds the inputs: `module14.html:214` gives $S_0=7000$ N, $n_{\rm b}=2$, and the fall as $h_{\rm f}=0.70$ m, $m_{\rm eff}=35$ kg, $k=40$ kN/m with $F=\sqrt{2gh_{\rm f}}\sqrt{m_{\rm eff}k}$. Running that (`m17/final/sec7.py`): $v=3.71$ m/s, $F=4385$ N, $(\rho/\rho_0)_{\rm crit}=\sqrt{F/S_0}=79.1$ percent, and with a hip protector cutting $F$ by $\sqrt2$, 66.6 percent. Fig. 6's polyline is calibrated to $F=4400$ N exactly (least-squares fit of the drawn curve against $S_0\rho^2/F$: tick positions 195.0, 103.8, 49.1 predicted against 195.0, 103.8, 49.1 measured, residual 0.10 px), so the figure is sound and only the prose lacks its inputs. Separately, the boxed implication is stated as an inequality that yields an equality: $S/F\lt1$ gives $\rho/\rho_0\lt\sqrt{F/S_0}$, and the critical value is where equality holds.

Replacement for line 239:

```html
<p><b>Problem.</b> Will a sideways fall break a hip, and at what bone density does the risk cross over? <b>Physical model.</b> A margin: the fall-impact force against the femur's strength (Module 2 for the failure criterion, <a class="secref" href="module14.html#osteoporosis">Module 14</a> for the fall and the strength law). <b>Mechanism.</b> The femoral neck, the narrow bridge of bone between the ball of the hip and the shaft, fails when the impact load exceeds its strength, and that strength falls as the <em>square</em> of bone mineral density (Proposition 3.1 of <a class="secref" href="module14.html#osteoporosis">Module 14</a>).</p>
```

Replacement for line 241 (the box's opening line; the boxed display on line 242 follows it):

```html
<div class="def"><b>Model 7.1 (fracture margin).</b> Model the fall as a mass $m_{\rm eff}$ dropping through $h_{\rm f}$ onto a linear contact spring of stiffness $k_c$ (distinct from the leg-spring $k$ of <a class="secref" href="#run">Section 5</a>). Energy capture gives the peak impact $F=v\sqrt{m_{\rm eff}k_c}$ with $v=\sqrt{2gh_{\rm f}}$ (Module 14), and the femoral strength scales as $S=S_0(\rho/\rho_0)^2$ with $\rho$ the bone mineral density and $\rho_0$ its young-adult value (Proposition 3.1 of <a class="secref" href="module14.html#osteoporosis">Module 14</a>). Define the <em>fracture margin</em> as $S/F$. The bone fractures when the margin falls below one, and the critical density is where it equals one:
```

Replacement for line 242, the boxed display, which currently writes an inequality and an equality as one implication (the trailing `</div>` closes the box and is kept):

```html
$$\frac{S}{F}=\frac{S_0(\rho/\rho_0)^2}{F}\lt 1\iff\frac{\rho}{\rho_0}\lt\Big(\frac{\rho}{\rho_0}\Big)_{\rm crit},\qquad\boxed{\;\Big(\frac{\rho}{\rho_0}\Big)_{\rm crit}=\sqrt{F/S_0}.\;}$$</div>
```

Replacement for line 244:

```html
<div class="cap"><p class="small"><b>Assumptions:</b> impact and strength as lumped scalars, quasi-static failure, density-squared strength law, no soft-tissue attenuation. <b>Parameters</b> (all from Module 14; <a class="secref" href="#appendix">Appendix</a>): fall height $h_{\rm f}=0.70\ \mathrm{m}$, effective mass $m_{\rm eff}=35\ \mathrm{kg}$, contact stiffness $k_c=40\ \mathrm{kN\,m^{-1}}$, young femoral strength $S_0=7.0\ \mathrm{kN}$, exponent $n_{\rm b}=2$. These give $v=3.71\ \mathrm{m\,s^{-1}}$ and $F=4.38\ \mathrm{kN}$, which the module rounds to $4.4\ \mathrm{kN}$. <b>Validation:</b> the $\sim$79&#37; critical density and the hip-protector shift match the fragility-fracture data of Module 14.</p></div>
```

The new §7 code block is given in B12.

### B7. There is no parameter table and no notation table, and the module's own template demands one

Location: `module17.html:100-111` (element 6 of the template), `:360-383` (the Appendix).

Quoted (element 6, line 106): "(6) <b>Parameters</b> - a table of values with sources and units."

Missing part: (5) number class, systematically, plus a house-convention violation. `prompt.txt:908` requires a parameter table for each capstone. Every other module's Appendix is a notation table plus a parameter table (`module14.html:465` is titled "A. Appendix - notation and parameters"); Module 17's Appendix is a course-summary table only. About twenty-five numbers are bare: $k_d=150$, $m_{\rm HAT}=48$, $d_0=0.20$, $I=0.12$, the 0.15 baseline factor, $t_c$, $t_{\rm step}$, $S_0=7$ kN, $F=4.4$ kN, $\mathrm{Fr}=0.5$, 2.6 BW, the walking speed, the 1.1 to 1.3 BW peaks, tendon 90 percent return, 200 W stair power, 30 to 50 ms activation lag, 13.5 to 3.5 N·s. Insert two tables before the existing course-summary table, immediately after line 362.

```html
<p>Seventeen modules, one arc: from a single free-body diagram to a modelled, measured, validated human body. Each module's core result is the block the capstones assemble. First, the symbols and the numbers this module itself used.</p>

<h3>Notation</h3>
<table>
<tr><th>Symbol</th><th>Meaning</th><th>Units</th><th>First used</th></tr>
<tr><td>$m$</td><td>body mass of the reference human</td><td>kg</td><td><a class="secref" href="#standing">2</a></td></tr>
<tr><td>$g$</td><td>gravitational acceleration, $9.81$</td><td>m s$^{-2}$</td><td><a class="secref" href="#standing">2</a></td></tr>
<tr><td>$L$</td><td>pendulum height in <a class="secref" href="#standing">2</a>, stance-leg length in <a class="secref" href="#walk">4</a> (the same $1.0$ m)</td><td>m</td><td><a class="secref" href="#standing">2</a></td></tr>
<tr><td>$\theta$, $\Delta$</td><td>lean angle; neural feedback delay</td><td>rad; s</td><td><a class="secref" href="#standing">2</a></td></tr>
<tr><td>$I$</td><td>whole-body moment of inertia about the ankle, $mL^2=70$</td><td>kg m$^2$</td><td><a class="secref" href="#standing">2</a></td></tr>
<tr><td>$I_{\rm k}$</td><td>moment of inertia of the rising mass about the knee, $0.12$ - a different quantity about a different axis, subscripted so the two never share a symbol</td><td>kg m$^2$</td><td><a class="secref" href="#sts">3</a></td></tr>
<tr><td>$k_p$, $k_d$</td><td>proportional and derivative ankle gains</td><td>N m; N m s</td><td><a class="secref" href="#standing">2</a></td></tr>
<tr><td>$\omega_c$, $\Delta_c$</td><td>crossing frequency and critical delay (Proposition 2.2)</td><td>rad s$^{-1}$; s</td><td><a class="secref" href="#standing">2</a></td></tr>
<tr><td>$q$, $\tau_{\rm knee}$, $\tau_0$</td><td>knee angle; net knee extensor torque; assumed baseline torque</td><td>rad; N m; N m</td><td><a class="secref" href="#sts">3</a></td></tr>
<tr><td>$m_{\rm HAT}$</td><td>mass of the head-arms-trunk segment</td><td>kg</td><td><a class="secref" href="#sts">3</a></td></tr>
<tr><td>$d_0$</td><td>knee moment arm at seat-off; at knee angle $q$ the arm is $d_0\sin q$. Not the $d$ of <a class="secref" href="#jump">6</a></td><td>m</td><td><a class="secref" href="#sts">3</a></td></tr>
<tr><td>$\mathrm{Fr}$, $v$</td><td>Froude number $v^2/(gL)$; forward speed</td><td>-; m s$^{-1}$</td><td><a class="secref" href="#walk">4</a></td></tr>
<tr><td>$F$</td><td>force. Ground reaction in <a class="secref" href="#walk">4</a> and <a class="secref" href="#run">5</a>, landing force in <a class="secref" href="#jump">6</a>, fall impact in <a class="secref" href="#fracture">7</a></td><td>N</td><td><a class="secref" href="#walk">4</a></td></tr>
<tr><td>$k$, $\ell_0$, $\ell$</td><td>leg-spring stiffness; rest and instantaneous leg length</td><td>N m$^{-1}$; m; m</td><td><a class="secref" href="#run">5</a></td></tr>
<tr><td>$\phi$</td><td>leg angle from vertical in <a class="secref" href="#run">5</a>; trunk lean in K3 (local to that problem)</td><td>rad</td><td><a class="secref" href="#run">5</a></td></tr>
<tr><td>$t_c$, $t_{\rm step}$, $\beta$</td><td>contact time; step time; duty factor $t_c/t_{\rm step}$</td><td>s; s; -</td><td><a class="secref" href="#run">5</a></td></tr>
<tr><td>$h$, $d$</td><td>drop height; landing cushioning distance. Not the $d_0$ of <a class="secref" href="#sts">3</a></td><td>m; m</td><td><a class="secref" href="#jump">6</a></td></tr>
<tr><td>$h_{\rm f}$, $m_{\rm eff}$, $k_c$</td><td>fall height; effective impacting mass; contact stiffness</td><td>m; kg; N m$^{-1}$</td><td><a class="secref" href="#fracture">7</a></td></tr>
<tr><td>$S$, $S_0$, $\rho$, $\rho_0$</td><td>femoral strength and its young value; bone density and its young value</td><td>N; N; -; -</td><td><a class="secref" href="#fracture">7</a></td></tr>
<tr><td>$\ell_T$</td><td>hip-to-HAT-centre-of-mass distance (K3 only)</td><td>m</td><td><a class="secref" href="#problems">10</a></td></tr>
</table>

<h3>Parameters</h3>
<p class="small">Every number the capstones use, with its class. <b>Assumed</b> means a modeling choice made here; <b>derived</b> means computed from the rows above it; <b>Module N</b> means the value is that module's, unchanged.</p>
<table>
<tr><th>Symbol</th><th>Value</th><th>Class</th><th>Used in</th></tr>
<tr><td>$m$</td><td>$70\ \mathrm{kg}$</td><td>the course's reference human (Module 1)</td><td><a class="secref" href="#standing">2</a>-<a class="secref" href="#jump">6</a></td></tr>
<tr><td>$L$</td><td>$1.0\ \mathrm{m}$</td><td>assumed</td><td><a class="secref" href="#standing">2</a>, <a class="secref" href="#walk">4</a></td></tr>
<tr><td>$k_p$</td><td>$1.5\,mgL=1030\ \mathrm{N\,m}$</td><td>assumed (must exceed $mgL$)</td><td><a class="secref" href="#standing">2</a></td></tr>
<tr><td>$k_d$</td><td>$150\ \mathrm{N\,m\,s}$</td><td>assumed</td><td><a class="secref" href="#standing">2</a></td></tr>
<tr><td>$\omega_c$, $\Delta_c$</td><td>$2.404\ \mathrm{rad\,s^{-1}}$, $140.1\ \mathrm{ms}$</td><td>derived (Proposition 2.2)</td><td><a class="secref" href="#standing">2</a>, K1</td></tr>
<tr><td>$m_{\rm HAT}$</td><td>$48\ \mathrm{kg}$ ($0.69M$)</td><td>assumed</td><td><a class="secref" href="#sts">3</a></td></tr>
<tr><td>$d_0$</td><td>$0.20\ \mathrm{m}$</td><td>assumed</td><td><a class="secref" href="#sts">3</a></td></tr>
<tr><td>$I_{\rm k}$ (about the knee)</td><td>$0.12\ \mathrm{kg\,m^2}$</td><td>assumed</td><td><a class="secref" href="#sts">3</a></td></tr>
<tr><td>$\tau_0$</td><td>$0.15\,m_{\rm HAT}gd_0=14.1\ \mathrm{N\,m}$</td><td>assumed</td><td><a class="secref" href="#sts">3</a></td></tr>
<tr><td>$\tau_{\rm knee}$ peak</td><td>$109\ \mathrm{N\,m}$, 95&#37; interval $80$-$140$</td><td>derived (K4)</td><td><a class="secref" href="#sts">3</a></td></tr>
<tr><td>$v$ (walking)</td><td>$1.72\ \mathrm{m\,s^{-1}}$, so $\mathrm{Fr}=0.30$</td><td>assumed</td><td><a class="secref" href="#walk">4</a></td></tr>
<tr><td>mid-stance GRF</td><td>$mg(1-\mathrm{Fr})=0.70$ BW</td><td>derived (Model 4.1)</td><td><a class="secref" href="#walk">4</a></td></tr>
<tr><td>walk-run transition</td><td>$\mathrm{Fr}\approx0.5$, $v=2.2\ \mathrm{m\,s^{-1}}$</td><td>assumed (observed; the derived bound is $\mathrm{Fr}\le1$)</td><td><a class="secref" href="#walk">4</a></td></tr>
<tr><td>$t_c$, $t_{\rm step}$</td><td>$0.20\ \mathrm s$, $0.33\ \mathrm s$, so $\beta=0.606$</td><td>assumed</td><td><a class="secref" href="#run">5</a></td></tr>
<tr><td>$F_{\rm peak}$ (running)</td><td>$1780\ \mathrm{N}=2.59$ BW</td><td>derived (Model 5.1)</td><td><a class="secref" href="#run">5</a></td></tr>
<tr><td>$k$ (leg spring)</td><td>$10$-$40\ \mathrm{kN\,m^{-1}}$</td><td>assumed sweep (K2)</td><td><a class="secref" href="#run">5</a></td></tr>
<tr><td>tendon energy return</td><td>$\sim$90&#37;</td><td>Module 6</td><td><a class="secref" href="#run">5</a>, <a class="secref" href="#catalog">8</a></td></tr>
<tr><td>$h$, $d$</td><td>$0.40\ \mathrm m$; $0.05$-$0.30\ \mathrm m$</td><td>assumed</td><td><a class="secref" href="#jump">6</a></td></tr>
<tr><td>$h_{\rm f}$, $m_{\rm eff}$, $k_c$</td><td>$0.70\ \mathrm m$, $35\ \mathrm{kg}$, $40\ \mathrm{kN\,m^{-1}}$</td><td>Module 14</td><td><a class="secref" href="#fracture">7</a></td></tr>
<tr><td>$F$ (fall impact)</td><td>$4.38\ \mathrm{kN}$, rounded to $4.4$</td><td>derived</td><td><a class="secref" href="#fracture">7</a></td></tr>
<tr><td>$S_0$, $n_{\rm b}$</td><td>$7.0\ \mathrm{kN}$, $2$</td><td>Module 14, Proposition 3.1</td><td><a class="secref" href="#fracture">7</a></td></tr>
<tr><td>$(\rho/\rho_0)_{\rm crit}$</td><td>$0.791$; $0.666$ with a hip protector</td><td>derived</td><td><a class="secref" href="#fracture">7</a></td></tr>
<tr><td>$\ell_T$</td><td>$0.30\ \mathrm{m}$</td><td>assumed (K3 only)</td><td><a class="secref" href="#problems">10</a></td></tr>
<tr><td>catalog values</td><td>$\sim$200 W stair power; $30$-$50\ \mathrm{ms}$ activation lag; $13.5\to3.5\ \mathrm{N\,s}$ recovery envelope</td><td>Modules 13, 5 and 14 respectively; each brief must re-source its own</td><td><a class="secref" href="#catalog">8</a></td></tr>
</table>

<h3>The course in one page</h3>
```

### B8. Model 6.1's boxed derivation does not produce its own boxed term, and calls a mean force a peak

Location: `module17.html:219-221`, `:326` (D2's solution).

Quoted (line 219): "absorbs its kinetic energy as work $F_{\rm avg}\,d=\tfrac12mv^2$, so the peak force scales as $F_{\rm peak}\approx\frac{mv^2}{2d}+mg$."

Missing parts: (1) precise statement, (3) proof. The stated balance $F_{\rm avg}d=\tfrac12mv^2$ gives $mv^2/2d$ and nothing else; the $+mg$ appears from nowhere. D2 supplies its origin, the weight's work $mgd$ over the compression stroke, but the box does not. Worse, the algebra yields the mean force and the box labels it the peak, and D2 then concedes "the peak is a small factor above the average", so the box's own name for its result is one the module contradicts two hundred lines later. The arithmetic itself is right: $v=2.8014$ m/s, $F(0.05)=6180$ N, $F(0.20)=2060$ N, ratio exactly 3.000, impact-term ratio exactly 4.000 (`m17/verify.py`, section C).

Replacement for lines 219 to 221:

```html
<div class="def"><b>Model 6.1 (mean landing force from the cushioning distance).</b> A body landing at speed $v=\sqrt{2gh}$ (from drop height $h$) is brought to rest over a COM displacement $d$. Apply work-energy between touchdown and the lowest point: the kinetic energy $\tfrac12mv^2=mgh$ goes to zero, gravity does a further $+mgd$ of work over the stroke, and the ground force does $-F_{\rm avg}d$. Hence $F_{\rm avg}\,d=mgh+mgd$, that is
$$\boxed{\;F_{\rm avg}=\frac{mgh}{d}+mg=\frac{mv^2}{2d}+mg.\;}$$
This is the <em>mean</em> force over the cushioning stroke, not the peak: a real landing force rises and falls within the stroke, so its peak exceeds this by the profile's peak-to-mean ratio, about $\pi/2$ for a half-sine as in <a class="secref" href="#run">Section 5</a>. The mean is what the energy balance fixes exactly, and it carries the dependence that matters: the first term falls as $1/d$, a hyperbola in the cushioning distance, above a floor of $mg$ that no amount of flexion removes. Note that $d$ here is a distance the joints travel, and is not the moment arm $d_0$ of <a class="secref" href="#sts">Section 3</a>.</div>
```

Replacement for D2's solution (line 326):

```html
<details class="sol"><summary>Solution</summary><div>Falling from height $h$ gives impact speed $v=\sqrt{2gh}$, hence kinetic energy $\tfrac12mv^2=mgh$. Now apply work-energy between touchdown and the lowest point of the landing, over which the COM descends a further $d$. The kinetic energy goes to zero; gravity adds $mgd$; the ground force removes $F_{\rm avg}d$. Hence $F_{\rm avg}\,d=mgh+mgd$, so $F_{\rm avg}=mgh/d+mg$, which is the box of Model 6.1. Two readings matter. The $mgd$ term is the weight's work over the stroke and is exactly what produces the $+mg$ floor; dropping it leaves $mgh/d$, which falsely predicts an arbitrarily gentle landing for a long enough flexion. And $F_{\rm avg}$ is a mean, not a peak: the instantaneous force rises and falls within the stroke, so the peak is larger by the profile's peak-to-mean ratio, roughly $\pi/2$ for a half-sine. The key dependence is $F\propto1/d$ in the first term, a hyperbola in the cushioning distance.</div></details></div>
```

**Residue of the rename, found on the second pass.** Renaming the box from
$F_{\rm peak}$ to $F_{\rm avg}$ is not the whole fix. Five places outside the
box still call that number a peak, and one of them is the figure's own y-axis,
which a reader believes before they believe the prose. Left as shipped, a
reader who compares this mean against a measured peak force will call the model
wrong for the wrong reason, and the section would contradict its own box within
two lines of it. The figure caption also names the wrong derivation: the box is
work-energy (kinetic energy plus $mgd$ against $F_{\rm avg}d$), not
impulse-momentum, and the two give different answers because only one of them
carries the $+mg$ floor.

`edited/module17.html:286` (the §6 code block's own print label):

```html
print("d=%.2f m -> mean force %.1f kN" % (d, F))
```

`:288`, the Fig. 5 y-axis label, where "peak" and "mean" are the same width so
nothing else in the figure moves:

```html
transform="rotate(-90 38 117)">mean force (kN)</text>
```

`:288`, the Fig. 5 caption, which called the mean a peak twice, attributed the
box to impulse-momentum, and left both endpoint numbers vague ("several
kilonewtons", "about a third") when the section states them exactly:

```html
<figcaption>Capstone V. Mean landing force versus how far the landing is cushioned. Dropping from 0.4 m, the mean force over the cushioning stroke is the work-energy estimate F = mv&#178;/2d + mg of Model 6.1; the instantaneous peak exceeds it by the profile's peak-to-mean ratio, about &#960;/2 for a half-sine. A stiff, 5 cm landing gives 6.2 kN, while flexing to 20 cm cuts it to 2.1 kN. The hyperbola is why landing training teaches deep, soft flexion - the same energy absorbed over a longer distance is a smaller force (Module 9) - and the mg floor is why the returns diminish.</figcaption>
```

`:290`, the interpretation's opening verb and its validation clause. "Spikes"
names a transient; the number is a stroke average, and the validation as
shipped told the reader to compare it against a measured peak:

```html
A stiff, $5\ \mathrm{cm}$ landing averages $6.2\ \mathrm{kN}$ over the stroke, exactly nine body weights
```

```html
<b>Validation:</b> compare the mean force over the stroke, and the stroke's duration, to instrumented drop landings, and check the measured peak against the predicted mean times the profile's peak-to-mean ratio;
```

`:394`, D2's statement, which still asked the reader to derive $F_{\rm peak}$
while its own solution and the box both say the quantity is a mean:

```html
Derive $F_{\rm avg}\approx mgh/d+mg$ for a landing cushioned over distance $d$, and say why the instantaneous peak exceeds it.
```

`:545`, diagnostic 4, same word, same reason:

```html
<b>Cushioning.</b> Doubling the landing flexion distance changes the mean landing force how?
```


### B9. Two symbols carry two meanings each, unflagged, in a module that flags a third

Location: $d$ at `module17.html:170`, `:172` (knee moment arm, 0.20 m) against `:219`, `:221`, `:223` (landing cushioning distance, 0.05 to 0.30 m); $I$ at `:130` ($mL^2=70\ \mathrm{kg\,m^2}$ about the ankle) against `:170`, `:172` ($0.12\ \mathrm{kg\,m^2}$ about the knee).

House convention: a symbol means one thing for the whole module, and a
cross-section collision is a defect. Recording a collision in a notation table
is not resolving it; the reader still meets one symbol carrying two values.
The module demonstrates it knows the rule at line 241, where $k_c$ is
introduced as "distinct from the leg-spring $k$ of Section 5", and again at
line 207 where $\phi$ is defined locally. It does not apply the rule to $d$ or
$I$, and $\phi$ is then reused a third time in K3 for the trunk lean. The fix
is the one Module 2 used for $k$ against $k_s$: subscript one of the two and
say so in both places.

$\phi$ is settled by the K3 replacement in B11, which declares the trunk lean
local to that problem. $d$ is settled by the B4 replacements, which rename the
knee moment arm to $d_0$ - with one leftover: those replacements still wrote it
as a *function* $d(q)=d_0\sin q$, so the bare letter $d$ still appeared in
Section 3 beside the scalar $d$ of Section 6. Writing the arm as $d_0\sin q$
and naming $q$ in words removes the last occurrence and costs nothing.

$I$ was left colliding: $I=mL^2=70\ \mathrm{kg\,m^2}$ about the ankle in
Section 2, and $I=0.12\ \mathrm{kg\,m^2}$ about the knee in Section 3, two
quantities about two axes under one letter, with the notation table merely
recording the fact. Section 2 keeps $I$, since it carries the pendulum equation
and Proposition 2.2's whole proof; Section 3's becomes $I_{\rm k}$. Seven
places in the prose and tables and two code variables change with it.

The knee box, `edited/module17.html:200`:

```html
$$\boxed{\;\tau_{\rm knee}(t)=m_{\rm HAT}\,g\,d_0\sin q+I_{\rm k}\,\lvert\ddot q\rvert+\tau_0,\;}$$
```

The definition beside it, `:201`, which now also says why the subscript is
there - the point a reader needs at exactly this line:

```html
an inertial term with $I_{\rm k}$ the moment of inertia of the rising mass about the knee - subscripted to keep it distinct from the whole-body $I=mL^2$ about the ankle in <a class="secref" href="#standing">Section 2</a>, which is a different quantity about a different axis - taken in magnitude
```

The two remaining $d(q)$ uses, `:201` and `:203`:

```html
the moment arm $d_0\sin q$, which is largest in deep flexion
```

```html
moment arm $d_0\sin q$. <b>Parameters:</b>
```

The §3 parameter line, `:203`, and the notation-table row for $d_0$, `:567`:

```html
$d_0=0.20\ \mathrm{m}$ at seat-off, $I_{\rm k}=0.12\ \mathrm{kg\,m^2}$
```

```html
<td>knee moment arm at seat-off; at knee angle $q$ the arm is $d_0\sin q$. Not the $d$ of <a class="secref" href="#jump">6</a></td>
```

K4's solution, `:518`, which reads the error budget off the symbol:

```html
barely at all by $I_{\rm k}$, which multiplies a term worth
```

The notation table's own row, `:562`, which was the flag standing in for the
fix. One row becomes two, and neither now carries two values:

```html
<tr><td>$I$</td><td>whole-body moment of inertia about the ankle, $mL^2=70$</td><td>kg m$^2$</td><td><a class="secref" href="#standing">2</a></td></tr>
<tr><td>$I_{\rm k}$</td><td>moment of inertia of the rising mass about the knee, $0.12$ - a different quantity about a different axis, subscripted so the two never share a symbol</td><td>kg m$^2$</td><td><a class="secref" href="#sts">3</a></td></tr>
```

The parameter-table row, `:590`:

```html
<tr><td>$I_{\rm k}$ (about the knee)</td>
```

And the two code blocks, so the variable names match the symbols the reader
just learned. The §3 block, `:213`-`:215`:

```html
m_hat, d0, I_k = 48.0, 0.20, 0.12
```

```html
grav = m_hat*g*d0*np.sin(q)            # moment arm d0 sin q
iner = I_k*np.abs(qdd)
```

K4's Monte Carlo block, `:528`-`:531`, where `d` and `Ii` become `d0` and
`I_k` (the comment column stays where it was, so the block is still PEP8):

```html
d0 = rng.normal(0.20, 0.10*0.20, N)     # moment arm, 10%
I_k = rng.normal(0.12, 0.20*0.12, N)    # segment inertia, 20%
pk = np.array([(mh[i]*g*d0[i]*np.sin(q) + I_k[i]*np.abs(qdd)
                + 0.15*mh[i]*g*d0[i]).max() for i in range(N)])
```

After these, the only bare $I$ left in the module is Section 2's ankle inertia
(lines 130-143 and D1's solution at 392) and the one explicit contrast at 201.
Both code blocks were re-run and print exactly what they printed before: the
rename moves no number.

### B10. The Froude transition at 0.5 is the number the module actually uses and is never explained

Location: `module17.html:195`, `:197`, `:329` (D3's solution).

Quoted (line 195): "the Froude number; walking becomes a run near $\mathrm{Fr}\approx0.5$ ($v\approx\sqrt{gL/2}\approx2.2\ \mathrm{m/s}$ for a $1\ \mathrm{m}$ leg)."

Missing part: (4) the rescue or the limit case. The module derives $\mathrm{Fr}\le1$ and then quietly uses $\mathrm{Fr}\approx0.5$ for every quantitative statement, including the 2.2 m/s transition speed that D3 repeats. The gap is a factor of two on a derived bound, and it is the interesting part: the kinematic ceiling is not what a walker meets first. The replacement for line 195 under B1 already points to D3; D3's solution must then close the gap rather than restate the number.

Replacement for D3's solution (line 329):

```html
<details class="sol"><summary>Solution</summary><div>At mid-stance the COM moves on a circular arc of radius $L$ at speed $v$, so its acceleration is $v^2/L$ directed toward the foot, that is downward. Newton vertically gives $mg-F=mv^2/L$, where $F$ is the ground reaction. The leg can push but not pull, so $F\ge0$, hence $mv^2/L\le mg$, i.e. $\boxed{\mathrm{Fr}=v^2/(gL)\le1}$. At $\mathrm{Fr}=1$ the ground force has fallen to zero: the walker is in free fall over the top of the arc and can produce neither propulsion nor a balance correction, so this is a kinematic ceiling and not a comfortable limit. Two things bite well before it. The mid-stance force is $mg(1-\mathrm{Fr})$, so at $\mathrm{Fr}=0.5$ half the body weight has already left the foot and the friction available for propulsion has halved with it. And the step-to-step transition cost (Module 8) grows steeply with speed, because a faster COM must be redirected through a larger velocity change at each heel-strike. Together these make running metabolically cheaper near $\mathrm{Fr}\approx0.5$, that is $v\approx\sqrt{gL/2}=2.2\ \mathrm{m\,s^{-1}}$ on a $1\ \mathrm m$ leg, which is where humans actually switch. The bound is derived; the observed transition at half of it is an assumed empirical value here (<a class="secref" href="#appendix">Appendix</a>) and a prediction of Module 8's cost model.</div></details></div>
```

### B11. The four computational problems carry no code and no computed number, and three of their four claims are wrong

Location: `module17.html:337-347`.

House convention: "K solutions carry Python-verified numbers with code." None of the four does. Taking them in turn:

**K1** (line 338) states "the critical delay lands near $150\ \mathrm{ms}$" (wrong, B2: 140.2 ms by the bisection the problem itself prescribes).

**Correction to K1's replacement, made on re-verification (`m17/sixsec.py`, `m17/histchk.py`).** An earlier draft of the K1 solution offered two "cautions": hold the initial history constant over the delay window, and judge growth over tens of seconds because "a six-second run … reports a critical delay about 20 ms too high". **Both were tested and both are false.** Bisecting with the delayed index clamped at the array start instead of a constant history returns the same 140.2 ms; so does a six-second run (140.2 ms at every run length from 6 s to 80 s). They were replaced with the two sensitivities that were actually measured and that do move the answer: the **time step**, where forward Euler's lag biases the boundary low (137.5 ms at 200 Hz, 139.0 at 500 Hz, converging to 140.2 at 2 kHz and 140.1 at 8 kHz), and the **growth threshold**, where a loose test biases it high (140.7 ms if a 20 % overshoot counts as stable, 141.8 ms if a doubling does, against 140.2 ms at the 0.1 % the shipped code uses). These are better cautions in any case: they are the two knobs of the numerical method, and sweeping each until it stops mattering is exactly the convergence check §9 preaches.

**K2** (line 341) states three scalings and all three miss. Integrating a real planar SLIP over $k=10$ to $40\ \mathrm{kN\,m^{-1}}$ (`m17/final/k2.py`): the peak goes 2.37, 3.09, 3.69, 4.67, 5.48 BW and the contact time 0.210, 0.183, 0.164, 0.139, 0.122 s, giving exponents $F_{\rm peak}\propto k^{0.61}$ and $t_c\propto k^{-0.39}$, not the stated $\pm1/2$; and their product rises from 0.496 to 0.670 BW·s, a 35 percent increase, so it is not "fixed by the flight momentum". The departure from $\pm1/2$ is the science: a pure vertical spring-mass oscillator gives exactly $\pm1/2$, but the SLIP's leg sweeps through an angle during stance, so only the component $k(\ell_0-\ell)y/\ell$ acts vertically and the weight impulse $mg\,t_c$ shrinks with the contact time.

**K3** (line 344) asks the reader to "optimise the forward trunk lean", but Model 3.1 has one degree of freedom, $q$, and no lean variable, so there is nothing to sweep. The solution must build the minimal extension that makes the question well-posed and be honest that it is an extension.

**K4** (line 347) reports "a band of order $\pm15\%$" without saying it is one sigma. The Monte Carlo (20 000 draws, `m17/final/k4.py`) gives a mean of 108.6 N·m, one sigma 15.3 N·m (14.1 percent), and a 95 percent interval of 80 to 140 N·m, which is $\pm27$ percent. Reporting the one-sigma figure as "the band" is the precise error §9 warns against.

Each replacement below adds a copy-buttoned code block; all four were run and pass `pycodestyle` (`m17/mkblocks.py`).

Replacement for K1's solution (line 338):

```html
<details class="sol"><summary>Solution</summary><div>Bisect the delay between a known-stable and a known-unstable value, simulating each and testing whether the lean grows, until the interval closes on $\Delta_c$. Two numerical choices decide whether the answer is right, and each must be swept until it stops mattering. The first is the time step: forward Euler lags the true solution, which biases the boundary <em>low</em>, and the bisection returns $137.5\ \mathrm{ms}$ at $200\ \mathrm{Hz}$ and $139.0\ \mathrm{ms}$ at $500\ \mathrm{Hz}$ before settling at $140.2\ \mathrm{ms}$ for $2\ \mathrm{kHz}$ and $140.1\ \mathrm{ms}$ for $8\ \mathrm{kHz}$. Quote the converged value, not the first one. The second is the threshold that counts as growth: near the boundary the unstable mode grows slowly, one cycle every $2\pi/\omega_c=2.6\ \mathrm s$, so a loose test biases the boundary <em>high</em>. Calling a $20\%$ overshoot stable returns $140.7\ \mathrm{ms}$, and calling a doubling stable returns $141.8\ \mathrm{ms}$; the code below admits only $0.1\%$. Done at $2\ \mathrm{kHz}$ with that tight threshold the bisection returns $140.2\ \mathrm{ms}$, matching the closed-form $140.1\ \mathrm{ms}$ of Proposition 2.2 to one part in a thousand: the simulation and the analysis check each other, which is rung (4) of the validation ladder. A human loop delay of about $100\ \mathrm{ms}$ therefore leaves roughly $40\ \mathrm{ms}$ of margin, and the age-related delay increase of Module 14 eats exactly that. The bisection turns a yes/no simulation into a boundary value.</div>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np

g, L, m = 9.81, 1.0, 70.0
Iz, kp, kd = m*L*L, 1.5*m*g*L, 150.0
fs, tend = 2000.0, 40.0


def peak_lean(delay):
    """Largest |theta| over 40 s from a constant 0.05 rad history."""
    dt = 1/fs
    nd = int(round(delay/dt))
    n = int(tend*fs)
    th = np.zeros(n)
    om = np.zeros(n)
    th[:nd+1] = 0.05
    for k in range(nd, n-1):
        tq = kp*th[k-nd] + kd*om[k-nd]
        om[k+1] = om[k] + (m*g*L*th[k] - tq)/Iz*dt
        th[k+1] = th[k] + om[k+1]*dt
        if abs(th[k+1]) &gt; 1.0:
            return 1e3
    return np.abs(th).max()


lo, hi = 0.10, 0.20                  # known stable, known unstable
for _ in range(40):
    mid = 0.5*(lo + hi)
    if peak_lean(mid) &lt; 0.05*1.001:  # the lean never grows
        lo = mid
    else:
        hi = mid
print("bisected critical delay = %.1f ms" % (500*(lo + hi)))
print("margin over a 100 ms human delay = %.0f ms" % (500*(lo + hi) - 100))
# -&gt; bisected critical delay = 140.2 ms
# -&gt; margin over a 100 ms human delay = 40 ms</code></pre></div></details></div>
```

Replacement for K2's solution (line 341):

```html
<details class="sol"><summary>Solution</summary><div>Integrate the planar SLIP stance from touchdown to lift-off across a range of leg stiffness, holding the touchdown speed and leg angle fixed, and record the peak vertical force and the contact time. A stiffer leg gives a higher, sharper peak over a shorter contact; a softer leg spreads a lower peak over a longer one. Over $k=10$ to $40\ \mathrm{kN\,m^{-1}}$ the peak rises from $2.37$ to $5.48$ BW and the contact falls from $0.210$ to $0.122\ \mathrm s$, which is $F_{\rm peak}\propto k^{0.61}$ and $t_c\propto k^{-0.39}$. The naive expectation is $\pm1/2$: a mass on a vertical spring has $t_c=\pi\sqrt{m/k}$ and, by energy, $F=v\sqrt{mk}$. Two things break that exponent, and they are the point of the sweep. The SLIP leg <em>sweeps</em> through an angle during stance, so only the component $k(\ell_0-\ell)\,y/\ell$ acts vertically and the effective vertical stiffness is lower and posture-dependent. And the stance impulse is not fixed: it must reverse the flight momentum <em>and</em> carry the weight for $t_c$, and that weight part $mg\,t_c$ shrinks as the contact shortens, so the product $F_{\rm peak}t_c$ rises $35\%$ across the sweep rather than staying constant. Leg stiffness is therefore the runner's knob between a jarring, short contact and a soft, long one, but it buys no free lunch on the impulse.</div>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np
from scipy.integrate import solve_ivp

g, m, l0 = 9.81, 70.0, 1.0
alpha = np.radians(68.0)             # touchdown leg angle from horizontal


def stance(k, v_td=4.5):
    """One SLIP stance: return peak vertical GRF (BW) and contact time."""
    vx = v_td*np.cos(np.radians(12.0))
    vy = -v_td*np.sin(np.radians(12.0))

    def rhs(t, s):
        x, y, u, w = s
        ell = np.hypot(x, y)
        f = k*(l0 - ell)/ell
        return [u, w, f*x/m, f*y/m - g]

    def liftoff(t, s):
        return np.hypot(s[0], s[1]) - l0
    liftoff.terminal, liftoff.direction = True, 1
    s0 = [-l0*np.cos(alpha), l0*np.sin(alpha), vx, vy]
    sol = solve_ivp(rhs, [0, 0.6], s0, events=liftoff,
                    rtol=1e-9, atol=1e-11, max_step=1e-4)
    x, y = sol.y[0], sol.y[1]
    ell = np.hypot(x, y)
    return (k*(l0 - ell)*y/ell).max()/(m*g), sol.t[-1]


ks = np.array([10e3, 15e3, 20e3, 30e3, 40e3])
pk, tc = np.array([stance(k) for k in ks]).T
for k, p, t in zip(ks, pk, tc):
    print("k = %5.0f kN/m: peak %.2f BW, contact %.3f s, impulse %.3f BW.s"
          % (k/1e3, p, t, p*t))
print("exponents: peak ~ k**%.2f, contact ~ k**%.2f"
      % (np.polyfit(np.log(ks), np.log(pk), 1)[0],
         np.polyfit(np.log(ks), np.log(tc), 1)[0]))
# -&gt; k =    10 kN/m: peak 2.37 BW, contact 0.210 s, impulse 0.496 BW.s
# -&gt; k =    15 kN/m: peak 3.09 BW, contact 0.183 s, impulse 0.565 BW.s
# -&gt; k =    20 kN/m: peak 3.69 BW, contact 0.164 s, impulse 0.605 BW.s
# -&gt; k =    30 kN/m: peak 4.67 BW, contact 0.139 s, impulse 0.647 BW.s
# -&gt; k =    40 kN/m: peak 5.48 BW, contact 0.122 s, impulse 0.670 BW.s
# -&gt; exponents: peak ~ k**0.61, contact ~ k**-0.39</code></pre></div></details></div>
```

Replacement for K3's statement and solution (lines 343 to 344). The statement changes because the model must be extended before the optimisation is well-posed:

```html
<div class="prob"><b>K3 - the momentum strategy (optimisation).</b> Model 3.1 has one degree of freedom and no trunk lean, so as it stands it cannot answer why older adults swing forward before rising. Extend it: let the trunk lean forward by $\phi$ (local to this problem, not the leg angle of <a class="secref" href="#run">Section 5</a>), which carries the HAT centre of mass forward by $\ell_T\sin\phi$ toward the feet and so shortens the knee's moment arm, at the price of a hip torque that must hold the leaning trunk up. Find the lean that minimises the larger of the two joint torques, and derive it in closed form. <span class="small"><em>Probes: trading one joint's demand for another's; extending a model to make a question well-posed; <a class="secref" href="#sts">Section 3</a>.</em></span>
<details class="sol"><summary>Solution</summary><div>At seat-off the knee's moment arm falls to $d_0-\ell_T\sin\phi$ while the hip must supply $m_{\rm HAT}g\,\ell_T\sin\phi$ to hold the trunk, so with $\ell_T=0.30\ \mathrm m$ assumed (<a class="secref" href="#appendix">Appendix</a>)
$$\tau_{\rm knee}(\phi)=m_{\rm HAT}g\,(d_0-\ell_T\sin\phi),\qquad \tau_{\rm hip}(\phi)=m_{\rm HAT}g\,\ell_T\sin\phi.$$
The first falls and the second rises with $\phi$, so the larger of the two is smallest where they are equal: $d_0-\ell_T\sin\phi=\ell_T\sin\phi$, giving
$$\boxed{\;\sin\phi^{\ast}=\frac{d_0}{2\ell_T}\;}$$
and $\phi^{\ast}=19.5^\circ$ for $d_0=0.20\ \mathrm m$. At that lean each joint carries $47\ \mathrm{N\,m}$ against the upright knee's $94.2\ \mathrm{N\,m}$: the worst joint torque halves, which is why the strategy is worth adopting and why it appears exactly when the knee reserve shrinks (Module 13). Read what the closed form says: the optimum depends only on the <em>ratio</em> $d_0/2\ell_T$ and not on body mass, so it is the same lean for anyone of the same proportions, and leaning past $\phi^{\ast}$ trades a knee problem for a hip problem. This extension is deliberately minimal and is not the full momentum strategy: being quasi-static it captures the moment-arm transfer but not the horizontal momentum a real rise builds and must then arrest, which needs the two-segment dynamic model this module does not build.</div>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np

g = 9.81
m_hat, d0, l_T = 48.0, 0.20, 0.30    # HAT mass, knee arm, hip-to-HAT-COM
phi = np.radians(np.linspace(0, 60, 601))
tau_knee = m_hat*g*(d0 - l_T*np.sin(phi))   # lean carries the COM forward
tau_hip = m_hat*g*l_T*np.sin(phi)           # but the trunk must be held up
worst = np.maximum(tau_knee, tau_hip)
i = worst.argmin()
print("upright : knee %.1f N m, hip %.1f N m" % (tau_knee[0], tau_hip[0]))
print("optimum : phi = %.1f deg, knee %.1f, hip %.1f N m"
      % (np.degrees(phi[i]), tau_knee[i], tau_hip[i]))
print("closed form: phi* = asin(d0/(2*l_T)) = %.1f deg"
      % np.degrees(np.arcsin(d0/(2*l_T))))
print("worst-joint torque falls %.0f%%"
      % (100*(worst[0] - worst[i])/worst[0]))
# -&gt; upright : knee 94.2 N m, hip 0.0 N m
# -&gt; optimum : phi = 19.5 deg, knee 47.0, hip 47.2 N m
# -&gt; closed form: phi* = asin(d0/(2*l_T)) = 19.5 deg
# -&gt; worst-joint torque falls 50%</code></pre></div></details></div>
```

Replacement for K4's solution (line 347):

```html
<details class="sol"><summary>Solution</summary><div>Draw the HAT mass and the moment arm from their $\pm10\%$ one-sigma ranges and the segment inertia from its $\pm20\%$ range, run the estimate on each draw, and collect the peak knee torque. Over $20\,000$ draws the mean is $108.6\ \mathrm{N\,m}$ with a one-sigma spread of $15.3\ \mathrm{N\,m}$, which is $14.1\%$, and a 95 percent interval of $80$ to $140\ \mathrm{N\,m}$, which is $\pm27\%$. Report the interval, and say which one it is: quoting "$\pm14\%$" without saying it is one sigma is the exact failure <a class="secref" href="#validation">Section 9</a> warns about, because a reader will take it for the range and be wrong by a factor of two on the tail. The spread is dominated by $m_{\rm HAT}$ and $d_0$, which enter as a product, and barely at all by $I_{\rm k}$, which multiplies a term worth $0.5\ \mathrm{N\,m}$; that is the error budget's real lesson, and it says where a measurement would pay. Whether the interval clears a clinical threshold is the answer the honest report must give: a bare $109\ \mathrm{N\,m}$ hides it, and so does an unlabelled $\pm14\%$.</div>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np

rng = np.random.default_rng(17)
g, T, N = 9.81, 1.5, 20000
t = np.linspace(0, T, 200)
s = t/T
q = (np.pi/2)*(1 - (10*s**3 - 15*s**4 + 6*s**5))
qdd = np.gradient(np.gradient(q, t), t)
mh = rng.normal(48.0, 0.10*48.0, N)     # HAT mass, 10% (1 sigma)
d0 = rng.normal(0.20, 0.10*0.20, N)     # moment arm, 10%
I_k = rng.normal(0.12, 0.20*0.12, N)    # segment inertia, 20%
pk = np.array([(mh[i]*g*d0[i]*np.sin(q) + I_k[i]*np.abs(qdd)
                + 0.15*mh[i]*g*d0[i]).max() for i in range(N)])
lo, hi = np.percentile(pk, [2.5, 97.5])
print("mean %.1f N m, 1 sigma %.1f N m (%.1f%%)"
      % (pk.mean(), pk.std(), 100*pk.std()/pk.mean()))
print("95%% interval %.0f to %.0f N m (%.0f +/- %.0f%%)"
      % (lo, hi, pk.mean(), 100*(hi - lo)/2/pk.mean()))
# -&gt; mean 108.6 N m, 1 sigma 15.3 N m (14.1%)
# -&gt; 95% interval 80 to 140 N m (109 +/- 27%)</code></pre></div></details></div>
```

### B12. Three of six worked capstones have no code, while the module claims every number came from running it

Location: `module17.html:189-201` (§4), `:203-213` (§5), `:237-248` (§7), and the claim at `:386`.

Quoted (line 386): "every model stated, every figure computed, every number reproduced by the code shown".

The claim is false as shipped: only Capstones I, II and V carry a `<pre><code>` block. This is the same defect class as Module 3's §9.4. Two of the three gaps are now closable with the corrected models. §4 must not get code that produces an M from a rigid vault, because it cannot (B1); its computable content, the dip $mg(1-\mathrm{Fr})$, is a one-line arithmetic already written into the replacement prose, and the honest fix there is the caption and the interpretation, not a script. §5 and §7 get real blocks.

New code block for §5, to be inserted immediately after the `.cap` parameter box at line 211 (run and PEP8-checked as `m17/final/sec5.py`):

```html
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np

g, m = 9.81, 70.0
t_c, t_step = 0.20, 0.33           # contact and step time (assumed)
duty = t_c/t_step
F_mean = m*g/duty                  # mean stance force over the whole step
F_peak = (np.pi/2)*F_mean          # half-sine stance profile
t_fl = t_step - t_c
print("duty factor       = %.3f" % duty)
print("mean stance force = %.0f N = %.2f BW" % (F_mean, F_mean/(m*g)))
print("half-sine peak    = %.0f N = %.2f BW" % (F_peak, F_peak/(m*g)))
print("flight %.3f s, landing speed %.2f m/s" % (t_fl, g*t_fl/2))
# -&gt; duty factor       = 0.606
# -&gt; mean stance force = 1133 N = 1.65 BW
# -&gt; half-sine peak    = 1780 N = 2.59 BW
# -&gt; flight 0.130 s, landing speed 0.64 m/s</code></pre></div>
```

New code block for §7, to be inserted immediately after the `.cap` parameter box at line 244 (`m17/final/sec7.py`):

```html
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np

g = 9.81
h_f, m_eff, k_c, S0 = 0.70, 35.0, 40e3, 7.0e3
v = np.sqrt(2*g*h_f)
F = v*np.sqrt(m_eff*k_c)
print("v = %.2f m/s, impact F = %.0f N = %.2f kN" % (v, F, F/1e3))
print("critical density   = %.1f%% of young" % (100*np.sqrt(F/S0)))
print("with a hip protector (F/sqrt2): %.1f%%"
      % (100*np.sqrt(F/np.sqrt(2)/S0)))
# -&gt; v = 3.71 m/s, impact F = 4385 N = 4.38 kN
# -&gt; critical density   = 79.1% of young
# -&gt; with a hip protector (F/sqrt2): 66.6%</code></pre></div>
```

The §2 block (lines 134 to 158) gains the closed-form boundary of Proposition 2.2, appended after the existing two `print` calls (`m17/final/sec2.py`):

```
# The stability boundary in closed form (Proposition 2.2). At s = i*w the
# characteristic equation splits into
#   imag:  kd*w*cos(w*D) = kp*sin(w*D)
#   real:  Iz*w**2 + m*g*L = sqrt(kp**2 + kd**2*w**2)
# and squaring the second gives a quadratic in u = w**2.
a2 = Iz**2
a1 = 2*Iz*m*g*L - kd**2
a0 = (m*g*L)**2 - kp**2
wc = np.sqrt((-a1 + np.sqrt(a1*a1 - 4*a2*a0))/(2*a2))
Dc = np.arctan2(kd*wc, kp)/wc
print("omega_c = %.3f rad/s (period %.2f s)" % (wc, 2*np.pi/wc))
print("critical delay = %.1f ms" % (Dc*1000))
# -> 100 ms peak lean = 2.9 deg
# -> 200 ms peak lean = 63.2 deg
# -> omega_c = 2.404 rad/s (period 2.61 s)
# -> critical delay = 140.1 ms
```

Replacement for line 386, which can then make the claim truthfully:

```html
<p class="small">Module 17 of the Quantitative Human Musculoskeletal Science course, and its conclusion. Built with the <code>rigorous-explainer</code> method: every model stated, every figure computed, every number either derived in the text, listed in the <a class="secref" href="#appendix">Appendix</a> parameter table, or labelled an assumption, and every headline result offered with the error bar that earns it. The human body has been modelled from a single free-body diagram to a controlled, measured, deformable, aging mechanical-biological system - and, in these capstones, put to work.</p>
```

### B13. Fig. 5's y-axis ticks do not sit at the values they are labelled with

Location: `module17.html:233`.

Quoted (the tick lines): `<line x1="66" y1="117.5" x2="70" y2="117.5" stroke="#333"/>` labelled `8`, and `<line x1="66" y1="47.8" x2="70" y2="47.8" stroke="#333"/>` labelled `14`.

Missing part: (5) the tie to something concrete is the figure, and the figure misreports its own scale. Fitting the drawn polyline against $F(d)=mv^2/2d+mg$ over its 100 points gives $y=-10.2375\,F_{\rm kN}+195.002$ with a residual of 0.15 px, so the curve is exactly linear and the axis is calibrated by it: 0 kN at $y=195.0$, 8 kN at $y=113.1$, 14 kN at $y=51.7$. The drawn ticks sit at 195.0, 117.5 and 47.8, so the tick labelled 8 actually marks 7.57 kN (low by 5.4 percent) and the one labelled 14 marks 14.38 kN (high by 2.7 percent). A reader who reads the 6.2 kN point off the axis rather than off the label gets 6.5 kN (`m17/fig5chk.py`). The 0 tick is correct. Fix by moving the two ticks and their text to the positions the curve implies, keeping the existing +3.0 px text-baseline offset:

- `<line x1="66" y1="117.5" x2="70" y2="117.5" stroke="#333"/>` to `<line x1="66" y1="113.1" x2="70" y2="113.1" stroke="#333"/>`
- `<line x1="66" y1="47.8" x2="70" y2="47.8" stroke="#333"/>` to `<line x1="66" y1="51.7" x2="70" y2="51.7" stroke="#333"/>`
- the `8` label's `y="120.5"` to `y="116.1"`
- the `14` label's `y="50.8"` to `y="54.7"`

Fig. 2, Fig. 3, Fig. 4 and Fig. 6 were decoded the same way and their ticks are all correct: Fig. 6's predicted tick positions (195.0, 103.8, 49.1 for margins 0, 1, 1.6 at $F=4400$ N) match the drawn ones exactly.

### B14. Model 2.1 has no limit case, and the text says a linear model "topples"

Location: `module17.html:130`, `:160`, `:162`.

Quoted (line 130): "beyond a critical $\Delta_c$ the closed loop oscillates and grows - a fall."

Missing part: (4) the rescue or the limit case. Model 2.1 is linearised in $\theta$ and has no floor and no nonlinearity, so past the boundary $\theta$ grows without bound; it does not topple, and the 63.2° the code reports is far outside the range where $\sin\theta\approx\theta$ holds (the two differ by one percent at 14° and by six percent at 34°). Fig. 2's red curve is drawn only to 34.3° at 4.7 s and then simply stops, with nothing in the figure saying it was truncated. The fix is one sentence saying where the linearisation stops meaning anything, plus a caption that admits the truncation; both are carried by the replacements under B2.

## 3. Style and clarity edits

Line-level, applicable in one pass.

**S1** (`:235`). "spikes to $\sim$6 kN (nearly nine body weights)". It is 6180 N and exactly 9.00 BW. Change "nearly nine body weights" to "exactly nine body weights at these parameters".

**S2** (`:235`). "a factor of three on the total force, and a full quarter on the impact term $mv^2/2d$". Correct (3.000 and 4.000 exactly) but the phrasing inverts the sense of "quarter". Change to "a factor of exactly three on the total force, because the impact term $mv^2/2d$ falls by exactly four while the $+mg$ floor does not move at all".

**S3** (`:354`, diagnostic 4). "Doubling the landing flexion distance changes the peak force how? … Roughly halves it, since $F\propto1/d$." Neither clause holds: $F$ is not proportional to $1/d$ (the $+mg$ floor), and doubling $d$ cuts the total force by 1.80 at $d=0.05$, 1.67 at 0.10, 1.57 at 0.15 and 1.50 at 0.20, never by 2. Replacement: "It halves the impact term $mv^2/2d$ exactly, but not the total: the $+mg$ floor does not move, so the force falls by a factor of $1.8$ from $5$ to $10$ cm and only $1.5$ from $20$ to $40$ cm. Cushioning has diminishing returns, and the floor is body weight (Model 6.1)."

**S4** (`:281`). "a knee-torque estimate of $109\pm8\ \mathrm{N\,m}$ can settle whether a patient clears a threshold; one of $109\pm60\ \mathrm{N\,m}$ cannot". These invented bands sit beside the module's own number, whose real interval K4 computes as 80 to 140. Replacement: "the module's own sit-to-stand estimate is $109\ \mathrm{N\,m}$ with a 95 percent interval of $80$ to $140\ \mathrm{N\,m}$ (<a class=\"secref\" href=\"#problems\">K4</a>). Whether that settles a clinical question depends entirely on where the threshold sits: against a threshold of $60\ \mathrm{N\,m}$ the whole interval clears it and the answer is decisive; against one of $100\ \mathrm{N\,m}$ the interval straddles it and the honest report says the estimate cannot decide."

**S5** (`:281`). "the parameters (a body-segment mass known to $\pm15\%$, Module 15)". The module uses $\pm10\%$ for $m_{\rm HAT}$ in K4. Change "$\pm15\%$" to "$\pm10\%$" for consistency with the parameter table.

**S6** (`:332`). "A hip protector cutting $F$ by $\sqrt2$ lowers the threshold to $\approx0.66$". Computed 66.6 percent, which rounds to 0.67. Change "$\approx0.66$" to "$0.666$".

**S7** (`:332`). "$(\rho/\rho_0)_{\rm crit}=\sqrt{0.63}\approx0.79$". With $F=4385$ N the ratio is 0.6264 and the root 0.7915. Change "$\sqrt{0.63}\approx0.79$" to "$\sqrt{0.626}=0.791$" and "a $21\%$ density loss" to "a $20.9\%$ density loss".

**S8** (`:122`). "These are not pieties." A defensive opener that concedes the charge before answering it. Replacement: "Each principle earns its place in the projects below."

**S9** (`:93`). "a closing section (Section 9) treats the part beginners skip and experts obsess over - validation and the honest report". Same construction repeated at line 271 ("The element every beginner skips and every expert dwells on"). Change line 93 to "and a closing section (<a class=\"secref\" href=\"#validation\">Section 9</a>) treats validation and the honest report".

**S10** (`:187`, `:213`). "roughly $1.5\ \mathrm{N\,m}$ per kilogram" against the computed 1.550, and §5's whole interpretation is one undifferentiated paragraph while §2, §3, §4, §6 and §7 all use a bolded "<b>Interpretation and limits.</b>" lead. Give §5's paragraph the same lead so the six capstones read alike.

**S11** (`:1` of §1, line 97). "A model is not a simulation that runs; it is an argument that a chosen abstraction answers a question to a stated accuracy." This is the best sentence in the module. Keep it; no change. Noted here so it is not lost in an edit pass.

**S12** (§1, after line 111). The template has eleven elements and no place for the course's level ladder, which Modules 1 and 2 both use to situate their models. Add a twelfth element: "<li><b>(12) Level</b> - which rung of the course's level ladder the model sits on (Level 0 scalar estimate, Level 1 statics, Level 2 rigid-body dynamics, up to Level 10 multiscale adaptation), stated so a reader knows what class of answer to expect. A Level-1 statics estimate presented as a dynamic result is the commonest way a capstone overclaims.</li>" The B4 replacement already places Model 3.1 on Level 1; §2's Model 2.1 is Level 2 (planar dynamics with delayed feedback control), §4 and §5 are Level 2, §6 and §7 are Level 0.

**S13** (`:191`, Capstone III). `prompt.txt:887` asks Capstone III to "Model walking as an inverted pendulum <em>and compare stride lengths</em>". The module models the vault and never compares stride lengths. Add to the §4 extension clause: "and compare the stride length each speed implies, $\ell_{\rm stride}=2L\sin\theta_{\max}$, against measured gait".

**S14** (`:239`). "The femoral neck (Module 16's bone continuum)". The femoral neck is an anatomical structure, not a Module 16 model; the gloss is also missing. Carried by the B6 replacement, which glosses it and moves the Module 16 pointer to where it belongs, the limitation at line 248.

**S15** (`:304`). "Twelve problems - four on the method, four on the capstone models, four computational extensions - plus five diagnostics." Accurate, but the module elsewhere implies the course's 30-problem standard. Add one clause making the choice explicit: "Twelve problems, fewer than the thirty a content module carries, because a capstone's exercise is the project itself: four on the method, four on the capstone models, four computational extensions, plus five diagnostics."

**S16** (`:213`). "real tendons return $\sim$90%, not 100%, of the energy, Module 6". A bare number; it is also in the catalog at line 261. Add it to the parameter table (done in B7) and change the in-text mention to cite it: "$\sim$90% (Appendix; Module 6)".

**S17** (`:518`, K4's solution; found on the second pass, as residue of S5).
K4's solution warns against quoting a band without labelling it, and
illustrates the trap with "$\pm15\%$". After S5 that number exists nowhere else
in the module: the Monte Carlo prints a one-sigma spread of 14.1 percent, and
the module now quotes $\pm14\%$ at both `:225` and `:350`. An illustration of
mislabelling should use the module's own number, or the reader hunts for a
$\pm15\%$ that is not there. Both occurrences in the sentence change:

```html
quoting "$\pm14\%$" without saying it is one sigma
```

```html
hides it, and so does an unlabelled $\pm14\%$.
```

## 4. Structural notes

**The problem set is a third of the house size, and that is defensible but should be said.** Every other module carries 30 problems plus 5 diagnostics; this one carries 12 plus 5. For a capstone whose exercise is a whole project, twelve is a reasonable choice, and the nine catalog briefs are the real problem set. But the choice is never stated, and a reader coming from Module 16 will read it as thinning. S15 fixes the statement. Writing eighteen more problems would be a module rebuild, not an editorial pass, and is not attempted here.

**No problem carries a figure.** The house standard is a figure per problem. Twelve figures is a build task, not an edit; logged here as the largest remaining gap after this pass.

**The nine catalog briefs are the strongest part of the module and are under-specified in one respect.** Each gives problem, model, key equation and expected result, which is exactly the right level. But six of the nine carry a number in the "expected result" column (200 W, 13.5 to 3.5 N·s, 90 percent, 30 to 50 ms) with no source, and the brief's own instruction is that the reader must "source" the parameters. The parameter table added in B7 gives the four that recur; the rest should say "expected order of magnitude" rather than quoting a value the reader is then meant to derive independently.

**Dependency direction is clean.** Every cross-module reference points backward, and the module introduces no forward reference at all, which is right for a final module. The one broken pointer is B5's, which points backward to the wrong module rather than forward.

**The module closes the course as promised.** Module 15 line 678, Module 16 lines 357, 591 and 619 all promise that Module 17 turns the framework onto complete questions, and it does; `prompt.txt`'s fifteen suggested projects all appear, six worked and nine as briefs. The one unmet promise is `prompt.txt:887`'s stride-length comparison (S13), and the one unmet requirement is `prompt.txt:908`'s parameter table (B7).

## 5. What already works

**The eleven-element template and the three principles.** This is the module's reason to exist and it is well made. Line 97, "A model is not a simulation that runs; it is an argument that a chosen abstraction answers a question to a stated accuracy", is the sentence the whole course has been earning, and Principle 1.1's justification, "A model with more free parameters than the data constrains can fit anything and predicts nothing", is stated once and then actually used to motivate the choice of model in five of the six capstones.

**§9 and the validation ladder.** Four rungs, each concrete, ordered by how much data they need, with the internal checks first because they are free. The distinction in C2 between random and systematic error, and which one averaging removes, is exactly right and is the thing most graduate readers get wrong. The irony that §9's own module does not report error bars is B7's and B11's problem, not §9's: the section states the standard correctly.

**Capstone V is complete as shipped.** Its model box, its assumptions, its parameters, its code and its interpretation all agree, and every number in it checks: $v=2.8014$ m/s, 6180 N at 5 cm, 2060 N at 20 cm, the ratio exactly 3, the impact-term ratio exactly 4. The only defects touching it are the boxed result's name (B8) and its figure's y-ticks (B13); the arithmetic is sound throughout.

**Fig. 6 is exactly what a computed figure should be.** Its polyline reproduces $S_0(\rho/\rho_0)^2/F$ to a 0.10 px residual over 100 points, its tick positions match the values they claim to three significant figures, its crossing is at the 79 percent the caption states, and its caption stands alone. It is the model for the other five.

**Capstone I's simulation.** The delayed-feedback integrator is correct, its two printed numbers (2.9° and 63.2°) reproduce exactly, and the figure's green and red curves decode to 2.87° and a truncated 34.3° against those. What was missing was the analysis beside it, not the code.

**The catalog's breadth and honesty about what a brief is.** Line 267, "the model and equation are given, but the assumptions must be stated, the parameters sourced, the simulation written, and - the part that makes it rigorous - the result validated and its error bar reported", tells the reader precisely what work is left and why it is the work that counts.

**Prose quality throughout.** No hedges, no hype, no "obviously" or "clearly" or "simply" anywhere in the file, and no em-dashes. Active voice, one idea per sentence, and every section opens with its question. The problems this report raises are about numbers, attributions and missing scaffolding, not about the writing.

## 6. Changes applied

All 42 edits below were made by one re-runnable script, `m17/apply.py`
(`--dry` checks every anchor and changes nothing), against a pristine copy at
`edited/module17.html`. `module17.html` itself was never touched and no git
command was run. Line numbers are the **original** `module17.html`.

Three of the report's own numbers were overruled by a fresh run during this
pass and are corrected above and below: the vault force direction (B1), the K1
convergence cautions (B11a), and Fig. 5's misread-value figure (B13).

| tag | line (original) | what changed | how verified |
|---|---|---|---|
| B2a | 130 | Model 2.1's box gains its limit case (a linear model diverges, it does not topple; the small-angle range ends near $15^\circ$), then Proposition 2.2 with a full proof: the imaginary-axis crossing collapses to $I\omega^2+mgL=\sqrt{k_p^2+k_d^2\omega^2}$, a quadratic in $u=\omega^2$, and $\Delta_c=\arctan(k_d\omega_c/k_p)/\omega_c$. A `.keyresult` gives the worked $\omega_c=2.404$ rad/s and $\Delta_c=140.1$ ms. Replaces an asserted "beyond a critical $\Delta_c$". | `m17/recheck.py`: quadratic $4900u^2+73638u-589446=0$; both boundary residuals below $10^{-13}$. The shipped §2 block now prints `omega_c = 2.404 rad/s (period 2.61 s)` and `critical delay = 140.1 ms`, and was run (`m17/runblocks.py`, ALL MATCH). |
| B2b | 132 | §2's parameter box now states $\Delta_c=140$ ms from Proposition 2.2, not an asserted 150 ms, and closes the `.keyresult` that B2a opens. | Whole-file div balance 59 open / 59 close; pristine line 131 confirmed blank, so the two halves abut correctly. |
| B2c | Fig. 2 caption | "$\Delta_c\approx150$ ms" replaced by "$\Delta_c=140.1$ ms of Proposition 2.2". The caption now also admits the red trace is **truncated** at $34^\circ$ and 4.7 s and reaches $63.2^\circ$ by 6 s, outside the small-angle range (this is B14's fix). | 140.1 ms from `recheck.py`; $63.2^\circ$ is the shipped block's own printed value; $34.3^\circ$ decoded from the figure's y-ticks (175.6 / 117.5 / 59.4 for $-30$ / 0 / 30 deg, spacing 58.1 px in both intervals). |
| B12c | 134-158 | The §2 code block gains the closed-form stability boundary, appended after its two existing prints, so the simulation and Proposition 2.2 check each other inside one block. | Extracted from the edited file and run: prints all four lines exactly as its `# ->` comments claim. `check_code`: 9 blocks, 0 pycodestyle issues. |
| B4a | 168-170 | Model 3.1's box rewritten to be the equation the code actually computes: $\tau_{\rm knee}=m_{\rm HAT}gd_0\sin q+I\lvert\ddot q\rvert+\tau_0$. The undocumented factor 0.6 is dropped, the absolute value and $\tau_0$ are now defined, $d(q)=d_0\sin q$ is stated, and the model is placed on **Level 1** of the level ladder. | `recheck.py`: dropping the 0.6 moves the peak 108.52 to 108.686 N·m, which still prints 109, so no downstream number moves. Inertia peak 0.484 N·m against gravity 94.18 N·m, four parts in a thousand, as the new box claims. |
| B4b | 172 | §3's parameter box now lists $d_0=0.20$ m (renamed from $d$, B9), $I=0.12$ kg m², and $\tau_0=0.15\,m_{\rm HAT}gd_0=14.1$ N·m as an explicit assumption. | $\tau_0$ computed at 14.13 N·m (`recheck.py`); every value also appears in the Appendix parameter table (B7). |
| B4c | 174-183 | §3's code block rewritten: the 0.6 removed, `tau0` named and commented as an assumption, gravity / inertia / baseline split into three variables, and a second `print` reporting the decomposition. | Run from the edited file: prints `peak knee torque = 109 N m (1.55 N m/kg)` and `gravity 94.2, inertia 0.48, baseline 14.1 N m`, matching its `# ->` comments verbatim. |
| B4d | 187 | §3's interpretation now names the decomposition (94.2 gravity, 14.1 baseline, 0.48 inertia), states the honest headline as 109 N·m with the 80-140 N·m 95 percent interval, and flags $\tau_0$ as taken on assumption. | Decomposition from `recheck.py`; the interval from the K4 Monte Carlo block, run: `95% interval 80 to 140 N m`. |
| B1a | 191 | §4's opening question changed from "why the twin-peaked force" (which the model cannot answer) to "why walking unloads the body at mid-stance, and what caps its speed" (which it can). | Follows from the B1b physics. |
| B1b | 193-195 | Model 4.1's box now derives $\ddot y=-L\cos\theta\,\dot\theta^2-g\sin^2\theta\le0$, boxes $F_{\rm mid}=mg(1-\mathrm{Fr})$, and states plainly that **$F_{\rm mid}$ is the vault's largest force, not its smallest**, so the model gives a single hump where walking has two peaks around a dip. Replaces a box that gave only $\mathrm{Fr}\le1$. **This reverses the report's own earlier draft**, which had mid-stance and the ends swapped. | `m17/vaultchk.py` and `m17/recheck.py`, `solve_ivp` at `rtol=1e-10`: with $v=1.72$ m/s at mid-stance, $F=0.698$ BW at $\theta=0$, falling monotonically to 0.486 BW at $\pm20^\circ$ (monotonicity asserted and returned True). Analytic check: $\ddot y(\theta)-\ddot y(0)=(1-\cos\theta)[L\dot\theta_0^2-g(1+3\cos\theta)]<0$ for $\mathrm{Fr}<4$. |
| B1d | 197 | §4's parameter box: the validation clause now claims the mid-stance **value** $mg(1-\mathrm{Fr})=0.70$ BW, and says the twin peaks and the dip shape do *not* come from this model. | $1-\mathrm{Fr}=0.6984$ at $v=1.72$, $L=1$ (`recheck.py`). |
| B1e | Fig. 4 caption | The caption no longer credits the vault with the M-shape. It now says the model predicts the mid-stance value exactly and predicts neither the two **1.18** BW peaks nor the shape between them, both of which are Module 8's step-to-step transition. | Figure decoded from its own y-ticks (`m17/fig4chk.py`, least-squares fit $y=-55.350\,\mathrm{BW}+194.983$, residual 0.033 px): peaks 1.183 BW, mid-stance 0.701 BW, running peak 2.600 BW. The report's earlier 1.174 / 0.699 / 2.591 came from a looser tick fit. |
| B1f | 201 | §4's interpretation rewritten to "one number earned, the shape borrowed": the vault owns $mg(1-\mathrm{Fr})=0.70$ BW at mid-stance, its force is largest there and falls to 0.49 BW by $\pm20^\circ$, and it never reaches the 1.18 BW peaks. **Replaces the report's earlier "maximum of 0.82 BW", which was wrong.** Also adds `prompt.txt:887`'s missing stride-length comparison (S13). | 0.486 BW at $20^\circ$ from `m17/sixsec.py`; 0.698 BW at mid-stance from `vaultchk.py`. The 0.82 figure is the mid-stance value under the *other* speed convention, and even there it was attached to the wrong end. |
| B1g | 315 (C3) | C3's solution now says the vault predicts the mid-stance value, not the dip shape, and names the peaks as Module 8's transition. | Same runs as B1b and B1f. |
| B3a | 207-209 | Model 5.1's box rewritten. The shipped chain "$2mv_{\rm land}/t_c\approx2.5$-$3\,mg$" is replaced by a derivation that works: the mean force over the step is $mg$, so over the contact it is $mg/\beta$, and a half-sine profile has a peak $\pi/2$ times its mean, giving the boxed $F_{\rm peak}\approx(\pi/2)mg/\beta$. | `recheck.py`: the shipped chain evaluates to 343-515 N, that is 0.50-0.75 mg, low by about four times, so it could not have produced "2.5-3". The new chain gives $\beta=0.606$, mean 1133 N, peak 1780 N = 2.592 BW, against the 2.600 BW the figure draws. |
| B3b | 211 | §5's parameter box no longer says the leg stiffness was "tuned so the peak is $\approx2.6$ BW" (the answer chosen and then presented as the prediction). $t_c$, $t_{\rm step}$ and $\beta$ are listed as the assumptions the peak follows from, and $k$ is pointed at K2, where it is a genuine question. | The peak now follows from $\beta$ alone, with no free stiffness, as the new §5 block shows: it never mentions $k$. |
| B3c-S10-S16 | 213 | §5's interpretation given the bolded "Interpretation and limits." lead the other five capstones use (S10), the tendon figure cited to the Appendix rather than left bare (S16), and the peak quoted as the derived 2.59 BW. | Lead matches §2, §3, §4, §6 and §7 by inspection; the tendon row was added to the Appendix parameter table in B7. |
| B12a (§5) | after 211 | **New** §5 code block: computes the duty factor, mean stance force, half-sine peak and flight time from $t_c$ and $t_{\rm step}$. Capstone IV had no code while the module claimed every number came from running it. | Run from the edited file: prints `duty factor = 0.606`, `mean stance force = 1133 N = 1.65 BW`, `half-sine peak = 1780 N = 2.59 BW`, `flight 0.130 s, landing speed 0.64 m/s`, all matching its `# ->` comments. pycodestyle clean. |
| B8a | 219-221 | Model 6.1 renamed from a "peak" to the **mean** landing force, and its derivation completed: the $+mg$ term now comes from the weight's work $mgd$ over the compression stroke, which the shipped balance $F_{\rm avg}d=\tfrac12mv^2$ did not produce. The box notes that a real peak exceeds this by the profile's peak-to-mean ratio. | `recheck.py`: $v=2.8014$ m/s, $F(0.05)=6180.3$ N = 9.00 BW, $F(0.20)=2060.1$ N, total ratio exactly 3.000, impact-term ratio exactly 4.000. The arithmetic was always right; the derivation and the name were not. |
| B8b | 326 (D2) | D2's solution now derives the $+mg$ floor from $mgd$ explicitly, says what dropping it would falsely predict, and states that $F_{\rm avg}$ is a mean and not a peak, removing the contradiction with the old box. | Same run. |
| B5a-B6a | 239 | §7's opening: the femoral neck is glossed anatomically, and the density-squared strength law is re-attributed from **Module 2** (which does not contain it) to **Proposition 3.1 of Module 14**, with a working `module14.html#osteoporosis` link. | `grep -c 'rho_0\|apparent density' module02.html` returns 0, and $\rho$ in Module 2 is the radial coordinate of $J=\int_A\rho^2\,dA$. `module14.html:214` carries $S=S_0(\rho/\rho_0)^{n_{\rm b}}$ with $n_{\rm b}\approx2$ and an adjacent proof. |
| B6b | 241 | Model 7.1's box now names $m_{\rm eff}$, $h_{\rm f}$ and $k_c$ (distinguished from §5's leg spring $k$), sources $F=v\sqrt{m_{\rm eff}k_c}$ to Module 14, and defines the fracture margin before using it. | Inputs read from `module14.html:214`; $F$ recomputed below. |
| B6c | 242 | The boxed implication fixed: the shipped line wrote an inequality that yields an equality. It now reads $S/F<1\iff\rho/\rho_0<(\rho/\rho_0)_{\rm crit}$, with the critical value boxed as $\sqrt{F/S_0}$. | Algebra; the figure's crossing sits at margin $=1$, which confirms the equality reading. |
| B6d | 244 | §7's parameter box now lists all five inputs with their Module 14 source and shows $v=3.71$ m/s and $F=4.38$ kN as **derived**, replacing two bare numbers ($S_0=7$ kN, $F\approx4.4$ kN) that were in none of the three admissible classes. | The new §7 block prints `v = 3.71 m/s, impact F = 4385 N = 4.38 kN`. |
| B12a (§7) | after 244 | **New** §7 code block: computes the impact speed, impact force, critical density and the hip-protector case. Capstone VI had no code. | Run from the edited file: `critical density = 79.1% of young` and `with a hip protector (F/sqrt2): 66.6%`, matching its comments. pycodestyle clean. |
| B10 | 329 (D3) | D3's solution now closes the gap between the derived $\mathrm{Fr}\le1$ and the $\mathrm{Fr}\approx0.5$ the module actually uses: at $\mathrm{Fr}=1$ the foot carries nothing, half the body weight is already gone at $\mathrm{Fr}=0.5$, and Module 8's transition cost grows steeply with speed. The bound is derived; the 0.5 is labelled an assumed empirical value. | $v=\sqrt{0.5gL}=2.215$ m/s for $L=1$ (`recheck.py`), matching the module's quoted 2.2. |
| B11a | 338 (K1) | K1's solution: "$\approx150$ ms" replaced by the bisected **140.2 ms**, cross-checked against Proposition 2.2's 140.1 ms, plus a copy-buttoned code block. **The two convergence cautions in the report's draft were tested and both proved false**, and were replaced with the two sensitivities that were actually measured. | `m17/sixsec.py`: a six-second run returns 140.2 ms, identical to 40 s and 80 s, so the draft's "about 20 ms too high" is wrong. `m17/histchk.py`: clamping the delayed index instead of holding a constant history also returns 140.2 ms. What does move the answer is the time step (137.5 ms at 200 Hz, 139.0 at 500 Hz, 140.2 at 2 kHz, 140.1 at 8 kHz) and the growth threshold (140.7 ms if a 20 percent overshoot counts as stable, 141.8 ms if a doubling does). Those are what the shipped text now says. |
| B11b | 341 (K2) | K2's solution: the three stated scalings were all wrong. Replaced with the measured $F_{\rm peak}\propto k^{0.61}$ and $t_c\propto k^{-0.39}$, and a 35 percent **rise** in $F_{\rm peak}t_c$ across the sweep (the shipped text called that product "fixed by the flight momentum"), plus the reason: the SLIP leg sweeps, so only $k(\ell_0-\ell)y/\ell$ acts vertically, and the weight impulse $mg\,t_c$ shrinks with contact time. Code block added. | Planar SLIP integrated over $k=10$ to $40$ kN/m (`recheck.py` and the shipped block, `solve_ivp` at `rtol=1e-9`): peaks 2.37 / 3.09 / 3.69 / 4.67 / 5.48 BW, contacts 0.210 / 0.183 / 0.164 / 0.139 / 0.122 s, impulses 0.496 rising to 0.670 BW·s (+34.9 percent), fitted exponents 0.605 and $-0.392$. |
| B11c | 343-344 (K3) | K3's **statement** rewritten: it asked for an optimisation over a trunk lean that Model 3.1 does not contain, so the problem was ill-posed. It now asks the reader to build the minimal extension first, and $\phi$ is declared local to the problem (B9). | The extension is stated in the problem, so the sweep is now over a variable that exists. |
| B11d | 344 (K3) | K3's solution derives the closed form $\sin\phi^*=d_0/(2\ell_T)$, gives $\phi^*=19.5^\circ$, and is explicit that the extension is quasi-static and not the full momentum strategy. Code block added. | Shipped block run: `optimum : phi = 19.5 deg, knee 47.0, hip 47.2 N m`, `closed form: phi* = asin(d0/(2*l_T)) = 19.5 deg`, `worst-joint torque falls 50%`. Grid optimum and closed form agree to 0.03 degrees. |
| B13a | 233 | Fig. 5's y-tick labelled **8** moved from $y=117.5$ to $y=113.1$ (text baseline 120.5 to 116.1). At 117.5 it marked 7.57 kN, low by 5.4 percent. | `m17/fig5chk.py`: fitting the drawn 100-point polyline against $F(d)=mv^2/2d+mg$ on the figure's own x-mapping (70 px is 0 m, 470 px is 0.30 m) gives $y=-10.2375F_{\rm kN}+195.0022$ with a maximum residual of **0.162 px**, so the curve is exactly linear in $F$ and calibrates its own axis. 8 kN sits at 113.10. |
| B13b | 233 | Fig. 5's y-tick labelled **14** moved from $y=47.8$ to $y=51.7$ (text baseline 50.8 to 54.7). At 47.8 it marked 14.38 kN, high by 2.7 percent. | The same fit puts 14 kN at 51.68. The 0 tick at 195.0 was already right (fit intercept 195.0022). Figures 2, 3, 4 and 6 were decoded the same way and their ticks are all correct (Fig. 6 tick-fit residual 0.008 px). |
| B7 | after 362 | The Appendix gains a **notation table** (19 rows: each symbol with units and first-use section, and both symbol collisions from B9 recorded explicitly) and a **parameter table** (23 rows: every number classed as *assumed*, *derived*, or *Module N*). The module's own template element (6) demands one and `prompt.txt:908` requires one per capstone; there was none. | Every value in the tables is one printed by a script in this pass or read from `module14.html:214`. `check_links` reports 124 internal links, 0 broken, 0 unlinked after the tables were added. |
| B5b | 367 | Appendix course-summary row for Module 2: the $S\propto\rho^2$ law removed, since it is not in Module 2. | Same `grep` evidence as B5a. |
| B5c | 379 | Appendix course-summary row for Module 14: the $S=S_0(\rho/\rho_0)^2$ law added, where it belongs. | `module14.html:214`, Proposition 3.1. |
| B12b | 386 | The closing claim "every number reproduced by the code shown" was false as shipped, since three of six capstones had no code. Now that §5 and §7 have blocks, the claim is restated truthfully: every number is derived in the text, listed in the Appendix parameter table, or labelled an assumption, and every headline result carries its error bar. | 9 code blocks in the edited file, up from 3; all extracted, all run, all printing exactly their `# ->` comments. |
| S9 | 93 | "the part beginners skip and experts obsess over" cut, because the same construction is used again at line 271. | Duplicate construction confirmed by grep. |
| S12 | 111 | A **twelfth** template element added: which rung of the level ladder the model sits on, with the note that a Level-1 statics estimate presented as a dynamic result is the commonest capstone overclaim. Model 3.1 is placed on Level 1 by B4a. | The house convention requires a module to place its models on the ladder; §1's template had no slot for it. |
| S8 | 122 | "These are not pieties." (a defensive opener) replaced with "Each principle earns its place in the projects below", and Principle 1.3 now points at the concrete 80-140 N·m band. | Interval from the K4 block. |
| S1-S2 | 235 | "spikes to ~6 kN (nearly nine body weights)" corrected to 6.2 kN and **exactly** nine body weights; "a full quarter on the impact term" rephrased so the sense of the factor is right; the diminishing-returns floor added. | `recheck.py`: $F(0.05)/(mg)=9.000$ exactly; total-force ratio 3.000, impact-term ratio 4.000; the 20 to 40 cm factor is 1.500. |
| S4-S5 | 281 | The invented $109\pm8$ and $109\pm60$ bands replaced by the module's own computed 80-140 N·m interval, worked against two thresholds (60 N·m decisive, 100 N·m not). The segment-mass uncertainty changed from $\pm15\%$ to $\pm10\%$ to match K4 and the parameter table. | Interval and both sigma figures from the K4 block: `mean 108.6 N m, 1 sigma 15.3 N m (14.1%)` and `95% interval 80 to 140 N m (109 +/- 27%)`. |
| S15 | 304 | The 12-problem count (against the house 30) is now stated as a deliberate choice, with the nine briefs named as the rest of the set. | Counted in the file. |
| S6-S7 | 332 | "$\sqrt{0.63}\approx0.79$" corrected to "$\sqrt{0.626}=0.791$"; "a $21\%$ density loss" to "$20.9\%$"; "$\approx0.66$" to "$0.666$". | `recheck.py`: $F/S_0=0.6264$, its root 0.7915, loss 20.85 percent, protector case 0.6655. |
| S3 | 354 (diagnostic 4) | "Roughly halves it, since $F\propto1/d$" replaced. $F$ is not proportional to $1/d$ because of the $+mg$ floor, and doubling $d$ never halves the force. | `recheck.py`: doubling $d$ cuts the total by 1.800 at 5 cm, 1.667 at 10 cm, 1.571 at 15 cm and 1.500 at 20 cm. |

### Gate results, baseline against final

Run as `python $S/NAME.py edited/module17.html`. The baseline is the pristine copy.

| gate | baseline | final | verdict |
|---|---|---|---|
| `checktex` | 0 issues, 498 segments | 0 issues, 510 segments | clean |
| `checklt` | 0 | 0 | clean |
| `check_links` | 41 links, 0 broken, 0 unlinked | 124 links, 0 broken, 0 unlinked | clean; the link count rose with the two Appendix tables |
| `check_svg` | 0 hard, 0 advisory | 0 hard, 0 advisory | clean |
| `check_code` | 3 blocks, 0 issues | 9 blocks, 0 issues | clean; 6 blocks added |
| `verify_dom` | 0 mjx-merror, 0 broken, 6 stray-$, 0 swallowed | 0 mjx-merror, 0 broken, 6 stray-$, 0 swallowed | clean; stray-$ unchanged |
| `check_overlap` | 0 | 0 | clean |
| `check_frame` | 0 | 0 | clean |
| `check_bodyprop` | clean | clean | clean |

Beyond the gates, all **9** `<pre><code>` blocks were extracted from the edited
file and executed: every one exits 0 and prints stdout matching its `# ->`
comments verbatim (`m17/runblocks.py`, "ALL MATCH"). Whole-file `<div>` balance
is 59 open and 59 close.

### Does it close the course?

Yes, with one gap that is a build task rather than an editorial one.

- **Inbound pointers all land.** No module in `module01` to `module16` uses a
  `module17.html#fragment` link, so there is nothing to break; `index.html`
  carries the single plain link to `module17.html` and it resolves. Every `id`
  the new Appendix tables and the closing line reference (`#appendix`,
  `#standing`, `#sts`, `#walk`, `#run`, `#jump`, `#fracture`, `#catalog`,
  `#validation`, `#problems`) exists in the edited file, and `check_links`
  reports 0 broken.
- **The promises made to Module 17 are kept.** `module15.html:678` and
  `module16.html:357` promise that the capstones take one block of the
  framework each and turn it on a complete question; the six worked capstones
  and the nine briefs do exactly that, and `prompt.txt`'s fifteen suggested
  projects all appear. `prompt.txt:887`'s stride-length comparison, previously
  missing, is added by B1f. `prompt.txt:908`'s per-capstone parameter table is
  supplied by B7.
- **The one gap left.** No problem carries a figure, against the house standard
  of a figure per problem. Twelve figures is a build task, not an editorial
  one, and it is logged in §4 above as the largest remaining item.
