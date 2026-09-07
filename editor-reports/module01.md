# Editor report: module01.html (Mechanical Foundations)

Pilot editorial pass. Standard: the five-part rule of the `science-editor` skill, read against `EDITOR_DOMAIN.md`. Every location is `module01.html:LINE`. Every replacement is valid HTML with MathJax delimiters and uses only the box classes the stylesheet defines. All eleven Python blocks in the file were extracted, run, and compared with the prose (scripts in the session scratchpad, folder `m01/`).

## 1. Verdict

Yes, after revision. A graduate reader with no biomechanics can learn the statics of holding, lifting, and standing from these pages. Sections 1 to 5 and 7 are built the way the brief demands: each boxed law carries a proof of matching weight, the worked example in section 8 reproduces its numbers, and the lab code and all ten computational solutions print exactly the values the text states (0 mismatches in 65 checked numbers). What stops the reader cold is elsewhere. Two free-body figures are unreadable after the July "realism" commit, which set the forearm beam to a 75 px black pill and the muscle arrow to a 144 px wedge. Problem D4 has the elbow flexor pulling the wrong way, so its "compression" follows from a sign error. The low-back compression in section 6 is asserted beside a proved sibling, and its sentence is cut in half by an uncaptioned figure. The module contradicts itself three times (C7 against section 6, C8 against section 6, K9 against K1) and its table of misses says the joint force was dropped when section 5 derives it. The Appendix has no notation table, and six empirical numbers used in the text (upper-body mass fraction, trunk reach, erector-spinae arm, foot length, COM height, the NIOSH limit) are in no table. Five of the ten computational problems are plug-in arithmetic. All of this is repairable without touching the mathematics, which is sound.

## 2. Blocking defects

Ranked by severity: sign and factual errors first, then asserted results, then structure that stops the reader, then missing scaffolding, then problem-set depth.

### B1. D4: the muscle pulls the forearm away from the joint, so the "compression" has the wrong sign

Location: `module01.html:583` (statement), `module01.html:584` (figure), `module01.html:585` (solution).

Quoted: "Force balance: along the forearm (x), $J_x+F_m\cos\varphi=0\Rightarrow J_x=-F_m\cos\varphi$ (a compression pointing into the joint)".

Missing part: precise statement (the frame is never fixed) and a correct proof. With $x$ pointing distally from the elbow, an elbow flexor inserted on the forearm pulls *toward* the shoulder, so its along-bone component is $-F_m\cos\varphi$, not $+F_m\cos\varphi$. The solution's force balance therefore makes the humerus pull the forearm distally, which would be joint tension. The figure at line 584 draws the same error: the red arrow from (132,100) to (145.7,62.4) points distally. The conclusion "compression" is right; the argument that reaches it is wrong.

Replacement for line 585:

```html
<details class="sol"><summary>Show solution</summary><p>Fix the frame: $x$ runs along the forearm from the elbow toward the hand (distal), $y$ points up. The flexor inserts on the forearm at $r_m$ and runs back toward the upper arm, so its pull on the forearm has components $\mathbf F_m=(-F_m\cos\varphi,\;+F_m\sin\varphi)$: proximal along the bone, and upward. Moments about the elbow: only the transverse component has a moment arm, $F_m\sin\varphi\,r_m=W_L r_L$, so $F_m=W_L r_L/(r_m\sin\varphi)$. Force balance along the bone: $J_x-F_m\cos\varphi=0$, hence $J_x=+F_m\cos\varphi$; the humerus pushes the forearm distally with exactly the force the muscle uses to pull it proximally, so the two bones are pressed together and the joint carries an axial <em>compression</em> $F_m\cos\varphi$. Transverse balance: $J_y+F_m\sin\varphi-W_L=0$, so $J_y=W_L-F_m\sin\varphi\lt0$ whenever $r_L\gt r_m$ (the lever disadvantage of Proposition 5.1), which is the downward reaction of Proposition 5.2 recovered as the $\varphi=90^\circ$ case. A shallow insertion angle (small $\varphi$) inflates both $F_m$ and the axial compression $F_m\cos\varphi$. With the Appendix values, $r_m=d_m/\sin\varphi$ for a given $\varphi$ reproduces (5.1).</p></details>
```

Figure fix at line 584: the muscle arrow must run from the insertion toward the elbow side and upward. Replace the arrow element

```html
<line x1="132.0" y1="100.0" x2="145.7" y2="62.4" stroke="#7a1f1f" stroke-width="16.0" marker-end="url(#mRed)"/>
```

with

```html
<line x1="132.0" y1="100.0" x2="118.3" y2="62.4" stroke="#7a1f1f" stroke-width="3" marker-end="url(#mRed)"/>
```

and move the $J_x$ arrow to point distally: replace `<line x1="110.0" y1="100.0" x2="84.0" y2="100.0" …>` with `<line x1="110.0" y1="100.0" x2="136.0" y2="100.0" stroke="#5a3d8a" stroke-width="2.4" marker-end="url(#mPur)"/>` and its label `<text x="80.0" y="96.0" … >Jₓ</text>` with `<text x="140.0" y="96.0" font-size="9" text-anchor="start" fill="#5a3d8a">Jₓ</text>`. Re-run `check_overlap.py` after the move.

### B2. Section 6: the along-spine compression is asserted beside a proved sibling, and the sentence is cut by an uncaptioned figure

Location: `module01.html:357-362`.

Quoted (line 359): "the erector force runs <em>along</em> the flexed spine and the supported weight's along-spine component points the same way, so the two <em>add</em>. Including that weight component ($(m_{\text{ub}}+m_L)g\cos 60^\circ\approx 300\ \mathrm N$ for a trunk near $60^\circ$ from vertical) gives a spinal compression of roughly" then an `<svg>` with no `<figure>` or caption, then the `.keyresult` "Low-back climax."

Missing parts: (3) proof: this is a force balance in a new geometry, the sibling of Proposition 5.2, and it is stated in prose while 5.2 got a `.prop` and a `.proof`. This is exactly the Module 6 §6 gap the brief names. (5) the figure is not referenced and not captioned; the prose sentence ends in mid-air. Also $60^\circ$, $m_{\text{ub}}=0.60\,M$, $r_t=0.30$ m and $d_{\text{es}}=0.05$ m are bare numbers (see B12), and "cut the disc load by more than half" is an unlabelled claim that is true only for a near-upright trunk (computed: 46 % at $\beta=20^\circ$, 57 % at $\beta=10^\circ$, both with the load at 0.20 m).

Replacement for lines 357 to 362 (keep the hidden `<defs>` block at line 360 as is; it is referenced by every later figure):

```html
<p>The low back is the cautionary case, and it earns a real number. Assume a stooped lift (Fig. 6 below): the trunk is flexed $\beta=60^\circ$ from vertical, a box of $m_L=20\ \mathrm{kg}$ is held $r_L=0.40\ \mathrm m$ horizontally ahead of the L5/S1 disc (the intervertebral disc, the cartilage pad between the lowest lumbar vertebra and the sacrum), and the upper body (head, arms, trunk) of mass $m_{\text{ub}}=0.60\,M=42\ \mathrm{kg}$ has its COM $r_t=0.30\ \mathrm m$ ahead of the disc. The erector spinae (the muscles running vertically alongside the spine) act through a moment arm of only $d_{\text{es}}=0.05\ \mathrm m$. All five values are in the Appendix parameter table. Proposition 3.1 gives the extensor torque the back must supply,
$$\tau_{\text{L5/S1}}=g\,(m_{\text{ub}}r_t+m_L r_L)=9.81\,(42\times0.30+20\times0.40)\approx 202\ \mathrm{N\,m},$$
and Proposition 5.1 turns it into an erector-spinae force $F_{\text{es}}=\tau_{\text{L5/S1}}/d_{\text{es}}\approx202/0.05\approx 4040\ \mathrm N$. What the disc carries is set by the force half of Law 1, and here the geometry differs from Proposition 5.2.</p>

<div class="prop"><b>Proposition 6.1 (disc compression in a stooped lift).</b> Model the upper body plus load as one rigid segment hinged at L5/S1 and inclined $\beta$ from vertical, held by an erector-spinae force $F_{\text{es}}$ directed along the segment toward the disc. The compressive force the disc carries along the spine axis is
$$\boxed{\;C=F_{\text{es}}+(m_{\text{ub}}+m_L)\,g\cos\beta.\;}\tag{6.1}$$
Unlike (5.2), the muscle force and the weight component <em>add</em>.</div>
<div class="proof">
Isolate the trunk-plus-load segment (Definition 1.5). Take an axis $s$ along the segment, positive from the disc toward the head. Three forces have components along $s$: the erector-spinae pull, which runs along the segment toward the disc, contributing $-F_{\text{es}}$; the two weights, each vertical, whose components along an axis tilted $\beta$ from vertical are $-(m_{\text{ub}}+m_L)g\cos\beta$ (both point toward the disc when the trunk leans forward); and the disc reaction $C$ on the segment, pushing it away from the pelvis, $+C$. The $s$-component of $\sum\mathbf F=\mathbf 0$ reads $C-F_{\text{es}}-(m_{\text{ub}}+m_L)g\cos\beta=0$, which is (6.1). In Proposition 5.2 the muscle pulled <em>up</em> and the weights pulled <em>down</em>, so they subtracted; here the muscle and the weights both pull the segment onto the disc, so they add. At $\beta=0$ (upright) the muscle term vanishes with the torque and the disc carries only the weight, $(m_{\text{ub}}+m_L)g$. <span class="qed">∎</span>
</div>

<figure>
<!-- the stooped-lift body SVG currently at line 361 goes here, unchanged except for its aria-label -->
<figcaption>Stooped lift at $\beta=60^\circ$. The trunk and the box act at horizontal arms $r_t$ and $r_L$ about the L5/S1 disc; the erector spinae (red, $F_{\text{es}}$) balance both through the short arm $d_{\text{es}}$. Both the muscle pull and the along-spine weight component press the trunk onto the disc, equation (6.1).</figcaption>
</figure>

<div class="keyresult"><b>Low-back climax.</b> With the assumed $\beta=60^\circ$, the weight term is $(42+20)\times9.81\times\cos60^\circ\approx 304\ \mathrm N$, so (6.1) gives $C\approx 4040+304\approx 4.3\ \mathrm{kN}$, about $6\times$ body weight ($687$ N). This exceeds the NIOSH disc-compression action limit of $3.4\ \mathrm{kN}$ for repeated lifting (an external limit, cited without a page; unverified in this repo). Halving the load's reach to $r_L=0.20$ m alone lowers $C$ to $3.56$ kN, an 18 % cut, because $r_t$ is the second long arm. Cutting $C$ by half needs the trunk brought within about $10^\circ$ of vertical with the box at $0.20$ m: $\beta=20^\circ$ gives $2.33$ kN (46 % cut) and $\beta=10^\circ$ gives $1.88$ kN (57 % cut), with $r_t=\ell_t\sin\beta$ and $\ell_t=0.346$ m (K4 sweeps this). That is the quantitative content of "lift with your legs, keep the load close".</div>
```

Change the aria-label of the SVG moved into the figure from "Mechanical foundations instructional diagram" to "Stooped lift: erector-spinae force at L5/S1 and the load at horizontal reach r_L". Its $F_{\text{es}}$ arrow has `stroke-width="16.0"`; set it to `3` (see B9).

### B3. Definition 1.4 asserts that one force at the COM replaces the distributed weight

Location: `module01.html:147`.

Quoted: "For computing gravitational moments, the entire weight of a segment may be replaced by a single force $W=mg$ acting downward through its COM. This replacement is exact for a uniform field and is the workhorse of the whole module."

Missing part: (3) proof. The module rests on this line and never shows it. Replacement for line 147:

```html
<div class="def"><b>Definition 1.4 (center of mass).</b> The <em>center of mass</em> (COM) of a body is the mass-weighted average position, $\mathbf{r}_{\text{COM}}=\frac{1}{M}\sum_i m_i\mathbf{r}_i$ (or the integral $\frac{1}{M}\int \mathbf{r}\,dm$), where $M=\sum_i m_i$ is the total mass.</div>
<div class="lem"><b>Lemma 1.4a (weight acts at the COM).</b> In a uniform gravitational field $\mathbf g$, the net force and the net moment about any point $O$ of the weights of all the particles of a body equal the force and the moment of a single force $M\mathbf g$ applied at $\mathbf r_{\text{COM}}$.</div>
<div class="proof">
The net force is $\sum_i m_i\mathbf g=\bigl(\sum_i m_i\bigr)\mathbf g=M\mathbf g$. The net moment about $O$ is $\sum_i \mathbf r_i\times m_i\mathbf g=\bigl(\sum_i m_i\mathbf r_i\bigr)\times\mathbf g=M\mathbf r_{\text{COM}}\times\mathbf g=\mathbf r_{\text{COM}}\times(M\mathbf g)$, using that $\mathbf g$ is the same for every particle so it factors out of the sum. The last expression is the moment of the single force $M\mathbf g$ placed at the COM. Two particles of $1$ kg at $x=0$ and $x=1$ m give $\mathbf r_{\text{COM}}$ at $0.5$ m and a moment about the origin of $1\times0+1\times1=2\times0.5$ (in units of $g$), as the lemma says. The lemma fails when $\mathbf g$ varies across the body (tidal fields), which never happens at the scale of a limb. <span class="qed">∎</span>
</div>
<p>Lemma 1.4a is the workhorse of the module: every segment's weight is one arrow at its COM.</p>
```

The cross product used here is defined in Definition 2.1; see B18 for the ordering fix that makes this legal.

### B4. C7 contradicts section 6 on what halving the reach buys

Location: `module01.html:549`.

Quoted: "halving $r_L$ (load against the belly) or squatting to shrink $r_t$ cuts the compression nearly in half".

Factual error: section 6 (line 362) states, and the code confirms, that halving $r_L$ alone cuts the compression by 18 % (4346 N to 3561 N). Only the joint squat reaches 46 to 57 %. Replacement for line 549:

```html
<details class="sol"><summary>Show solution</summary><p>The extensor torque about L5/S1 is $g(m_{\text{ub}}r_t+m_L r_L)$ with horizontal reaches of $0.30$ and $0.40$ m, but the erector spinae balance it through an arm of only $d_{\text{es}}=0.05$ m. By (5.1) the muscle force is the torque divided by that arm, $F_{\text{es}}\approx4040$ N, about $6.6\times$ the combined weight of trunk and box, and by Proposition 6.1 all of it enters the disc, plus the along-spine weight component. The torque has two long-arm terms of similar size ($42\times0.30=12.6$ and $20\times0.40=8.0$ kg m), so halving $r_L$ alone removes only the smaller term's half: $C$ drops from $4.35$ kN to $3.56$ kN, 18 %. "Keep the load close" helps most when it is paired with an upright trunk, which shrinks $r_t$ as well: at $\beta=20^\circ$ with $r_L=0.20$ m the compression is $2.33$ kN, a 46 % cut. Reducing the object's mass by the same fraction changes only the $m_L$ term and its share of the weight, so posture, not object mass, is the lever.</p></details>
```

### B5. C8 states a factor of four for the whole spinal torque

Location: `module01.html:553`.

Quoted: "so the spinal torque — and, through the small erector-spinae arm, the compression — is roughly four times smaller when the load is kept close."

Factual error unless the trunk is upright. The box's *contribution* is four times smaller; the total torque is $202$ N m out front against $143$ N m close (ratio 1.4) if the trunk is flexed as in section 6, and $78$ against $20$ N m (ratio 4.0) only if the trunk is vertical so its own moment vanishes. Replacement for line 553:

```html
<details class="sol"><summary>Show solution</summary><p>The box's contribution to the L5/S1 torque is $W_L$ times its horizontal distance from the disc: about $0.4$ m held out front, about $0.1$ m pressed to the belly, so the <em>box's</em> term is four times smaller when close. Whether the whole torque falls by that factor depends on the trunk. Standing upright the trunk's COM sits over the disc ($r_t\approx0$), the box term is all there is, and the torque falls from $9.81\times20\times0.4\approx78$ N m to $\approx20$ N m, a factor of four. If the trunk is flexed as in <a class="secref" href="#general">§6</a> ($r_t=0.30$ m), the trunk term of $124$ N m stays, and the total falls only from $202$ to $143$ N m, a factor of $1.4$. Same physics as the coffee cup, with the trunk's own weight as a second cup you cannot put down.</p></details>
```

### B6. The "misses" table says the joint contact force was dropped; section 5 derives it

Location: `module01.html:502` and `module01.html:498`.

Quoted (line 502): "<tr><td>Joint contact force dropped</td><td>Real joint/bone compressive loads</td><td>Modules 2, 4</td></tr>".

Factual error: Proposition 5.2 derives $J$ and section 8 evaluates it as $567$ N. Also line 498 sends "Inertial/acceleration torques during motion" to "Modules 2–3", which are bones and joints; the dynamics modules are 7 to 9. Replacement for lines 498 and 502:

```html
<tr><td>Static only ($\sum\mathbf M=0$, Level 1)</td><td>Inertial/acceleration torques during motion; Definition 7.5 names the correction but no section computes one</td><td>Modules 7–9 (dynamics)</td></tr>
```

```html
<tr><td>Joint contact force only for a vertical muscle line</td><td>The axial (along-bone) component of $\mathbf J$ with an inclined muscle (D4), and the stress it produces in bone and cartilage</td><td>Modules 2, 4</td></tr>
```

### B7. K9's moment-arm model has the opposite sign to K1's

Location: `module01.html:617` (K1), `module01.html:738-752` (K9).

Quoted (K1): "$d_m(\theta)=0.03-0.012\sin\theta$ (m)", shrinking as the forearm hangs. Quoted (K9 solution): "the moment arm rises from $\approx3.0$ cm at the horizontal forearm to $\approx3.8$ cm near $\theta=90^\circ$", with `d_true = 0.030 + 0.008*np.sin(th)` in the code.

Factual error: the same quantity, in the same module, grows toward extension in K9 and shrinks in K1. K1's sign is the anatomically right one (the flexor moment arm is largest near $90^\circ$ elbow flexion, the horizontal forearm here, and smallest at full extension). K9 also uses $F_{\max}=2000$ N where K5 used $1500$ N for the same quantity without saying why. Replacement for lines 738 to 752 (numbers from the corrected code, run with the same seed):

```html
<p><b>K9.</b> A subject's maximum voluntary elbow torque, measured across forearm angles, does not track $\cos\theta$, because the flexor moment arm changes with angle. Given the noisy measured max-voluntary torque at 20 angles and a known constant flexor force capacity $F_{\max}=2000$ N (assume a stronger subject than K5's $1500$ N; the recovery below does not depend on the value), recover the moment-arm model of K1, $d_m(\theta)=d_0+d_1\sin\theta$, by least squares. Report $d_m$ at the horizontal forearm and near $\theta=90^\circ$. <span class="probes">Probes: a two-parameter least-squares inverse for an angle-varying moment arm (and the identifiability that requires the sweep).</span></p>
<figure><!-- regenerate the computed plot from the code below; the current polylines encode the wrong sign --><figcaption>Measured max-voluntary torque vs. angle, falling as the forearm hangs; the two-parameter least-squares fit recovers $d_m(\theta)=d_0+d_1\sin\theta$ with $d_1\lt0$, the K1 model.</figcaption></figure>
<details class="sol"><summary>Show solution</summary><p>The measured torque is $\tau_{\max}(\theta)=F_{\max}\,d_m(\theta)=F_{\max}(d_0+d_1\sin\theta)$, linear in the two unknowns $d_0,d_1$. Regressing $\tau_{\max}$ on the columns $[F_{\max},\,F_{\max}\sin\theta]$ recovers $d_0\approx3.02$ cm and $d_1\approx-0.0122$ m from noisy data (true $0.030,\,-0.012$), so the moment arm falls from $\approx3.0$ cm at the horizontal forearm to $\approx1.8$ cm near $\theta=90^\circ$, the K1 model recovered from torque data alone. Note the identifiability: a <em>single</em> MVC (maximum voluntary contraction) measurement gives one equation $\tau=F_{\max}d_m$ in two unknowns and cannot separate force from moment arm; sweeping the angle breaks the degeneracy. Measuring $d_m$ directly from imaging is the more reliable route to the same quantity.</p>
<div class="codewrap"><button class="copybtn" onclick="copyCode(this)"><span class="lbl">Copy</span></button><pre><code>import numpy as np

rng = np.random.default_rng(1)
Fmax = 2000.0
th = np.radians(np.linspace(0, 80, 20))
d_true = 0.030 - 0.012*np.sin(th)                 # the K1 model
tau = Fmax*d_true + rng.normal(0, 0.8, th.size)   # noisy MVC torque
A = np.column_stack([np.ones_like(th), np.sin(th)])*Fmax
d0, d1 = np.linalg.lstsq(A, tau, rcond=None)[0]
print(f"d0={d0*100:.2f} cm, d1={d1:.4f} m")
print(f"d_m(0)={d0*100:.2f} cm, d_m(90)={(d0+d1)*100:.2f} cm")
# d0=3.02 cm, d1=-0.0122 m ; d_m(0)=3.02, d_m(90)=1.79 cm</code></pre></div></details>
```

### B8. K6 conflates the center of mass with the center of pressure and uses an equation the module never derives

Location: `module01.html:698-700`.

Quoted: "find when the COM — and thus the required COP — reaches the $0.12\ \mathrm m$ toe limit"; and "Model the fall as the linearized inverted pendulum $\ddot x=\omega_0^2 x$ with $\omega_0^2=g/\ell$ … the gravity-toppling term of the §7 dynamic-equilibrium equation".

Missing parts: (1) precise statement: with the ankle torque switched off the COP sits at the ankle and does not move with the COM; COM and COP coincide only in statics (Proposition 7.4), and the brief lists this pair as one that must not be blurred. (3) proof: $\ddot x=(g/\ell)x$ is not derived anywhere in the module, so the exercise is not solvable from the text. Replacement for the statement (line 698) and the first paragraph of the solution (line 700):

```html
<p><b>K6.</b> A standing person is nudged and begins to topple forward. Model the body as a point mass $M$ at COM height $\ell=1.0\ \mathrm m$ (assumed) on a massless rigid leg hinged at the ankle, with the ankle torque switched off so the COP stays at the ankle. Starting from a $2\ \mathrm{cm}$ COM offset at rest, derive the equation of motion from Definition 7.5, linearize it, integrate it numerically, and find when the COM passes the toe, $L_f=0.12\ \mathrm m$ (Appendix). Beyond that point no admissible COP (Definition 7.3) can produce a restoring moment, so a step is the only recovery. <span class="probes">Probes: integrating an unstable second-order ODE to a threshold crossing, and the difference between COM and COP once the body moves.</span></p>
```

```html
<p>Derivation. With the ankle torque zero the only forces on the body are the weight $Mg$ at the COM and the GRF at the ankle. Take moments about the ankle: the GRF has zero arm, the weight has horizontal arm $x=\ell\sin\phi$ where $\phi$ is the lean angle, so $\sum M=Mg\ell\sin\phi$. By Definition 7.5, $\sum M=I\ddot\phi$ with $I=M\ell^2$ for a point mass, giving $\ddot\phi=(g/\ell)\sin\phi$. For small $\phi$, $\sin\phi\approx\phi$ and $x=\ell\phi$, so $\ddot x=\omega_0^2x$ with $\omega_0=\sqrt{g/\ell}=3.13\ \mathrm{s^{-1}}$. Upright is an <em>unstable</em> equilibrium: the solution grows as $x(t)=x_0\cosh(\omega_0t)$. Stepping the ODE numerically from $x_0=0.02$ m, $\dot x_0=0$ and watching for $x=L_f=0.12$ m, the COM passes the toe at $t\approx0.79$ s (analytically $t=\operatorname{acosh}(6)/\omega_0=0.79$ s). Throughout, the COP has stayed at the ankle; it is the COM that moved. Unlike a linear drift, the fall <em>accelerates</em>, so most of the excursion happens in the final fraction of a second, which is why balance recovery is so time-critical (Modules 7, 10).</p>
```

Change the figure caption at line 699 to: "Inverted-pendulum topple with the ankle torque off: the COM accelerates past the $0.12$ m toe limit at $t\approx0.79$ s while the COP stays at the ankle."

### B9. The section 4 and section 5 free-body figures are unreadable

Location: `module01.html:230`, `244`, `278`, `330`, `334` (and the same defect in `361`, `536`, `544`, `548`, `556`, `566`, `584`, `588`, `598`, `602`).

Quoted (line 230): `<line x1="60" y1="80" x2="400" y2="80" stroke="#1a1a1a" stroke-width="74.8" stroke-linecap="round"/>`; (line 244): `<line x1="95" y1="80" x2="95" y2="22" stroke="#7a1f1f" stroke-width="16.0" marker-end="url(#p4up)"/>`.

Missing part: (5) the tie to something concrete is the figure, and the figure does not show what the caption says. Rendered (scratchpad `m01/fig4.png`, `fig5.png`): the forearm is a black pill 75 px tall that hides the pivot, the COM dot, the dimension lines and the $r_s$ label; the muscle arrow, with `markerUnits` at its default of `strokeWidth`, carries a 144 px red wedge. Commit `3fd6fbe` changed the beam from `stroke-width="5"` to `74.8`. This is the fat-triangle defect `CLAUDE.md` forbids, and every hardening gate passed because none measures stroke width. Replacements:

- line 230: `stroke-width="74.8"` to `stroke-width="6"`.
- line 244: `stroke-width="16.0"` to `stroke-width="3"`.
- line 278: `stroke-width="33.0"` to `stroke-width="6"`.
- line 330: `stroke-width="79.2"` to `stroke-width="6"`.
- line 334: `stroke-width="16.0"` to `stroke-width="3"`.
- line 536: `stroke-width="25.5"` and `"20.2"` (lever bars) to `"6"`.
- every force `<line … stroke-width="16.0" marker-end="url(#mRed)"/>` in lines 361, 548, 556, 566, 584, 588, 602 to `stroke-width="3"`; the tool handle in line 566 (`stroke="#7c5a2e" stroke-width="16.0"`) to `"8"`.
- GRF arrows `stroke-width="19.2"` (line 544) and `"17.7"` (line 598) to `"3.4"` (a heavier load may thicken the shaft modestly; the head stays fixed because `mPur` uses `userSpaceOnUse`).

Add `markerUnits="userSpaceOnUse"` to the four local markers `m2arrow`, `m2arrowr` (lines 173 to 174), `p4dn`, `p4up` (226 to 227), `a4dn` (266), `m5up`, `m5dn` (327 to 328) so a future width change cannot scale the head again. Add a gate: a stroke width above 8 on any `<line>` carrying `marker-end` should fail `check_svg.py`.

### B10. A lumbar figure sits in the course map, and two section 7 figures have no caption

Location: `module01.html:108`, `module01.html:375`, `module01.html:386`.

Quoted (line 108 caption): "Low-back moments act through the lumbar stack (bodies + discs)." It is Fig. 1 of the module, placed above the syllabus table, before "lumbar", "vertebral body" or "disc" is glossed, and no prose refers to it. Lines 375 and 386 are bare `<svg>` elements: no `<figure>`, no caption, no figure number, so the prose cannot cite them.

Replacement: delete line 108. Insert its SVG in section 6, immediately after the new Proposition 6.1 proof of B2 and before the stooped-lift figure, as

```html
<figure><!-- the lumbar-stack SVG from line 108, unchanged --><figcaption>The lumbar stack: vertebral bodies (bone) alternate with intervertebral discs (cartilage pads). The compression $C$ of (6.1) passes through the lowest disc, L5/S1.</figcaption></figure>
```

Wrap line 375:

```html
<figure><!-- SVG of line 375 --><figcaption>Quiet standing. Weight $W=Mg$ acts down through the COM; the resultant GRF acts up through the COP, which must lie inside the base of support (purple), the outline of the contact patch.</figcaption></figure>
```

Wrap line 386:

```html
<figure><!-- SVG of line 386 --><figcaption>Leaning forward. The COM moves a horizontal distance $d_{\text{COM}}$ ahead of the ankle (faded body: upright); by Proposition 7.4 the COP slides the same distance forward under the sole.</figcaption></figure>
```

Add "(Fig. N)" references in the prose at lines 373 and 385 once the figure numbers settle; the counter renumbers every figure when line 108 moves.

### B11. The Appendix has no notation table

Location: `module01.html:769-778`.

Quoted: the Appendix holds one five-row parameter table and no list of symbols. The brief requires every symbol in the text to appear in a notation table. Insert after line 770, before the parameter table:

```html
<h3>Notation</h3>
<table>
<tr><th>Symbol</th><th>Meaning</th><th>Unit</th><th>First used</th></tr>
<tr><td>$m$, $m_i$, $m_k$</td><td>mass of a body, particle, or load</td><td>kg</td><td><a href="#setup">§1</a></td></tr>
<tr><td>$M$</td><td>total mass of the body considered (70 kg reference human)</td><td>kg</td><td><a href="#setup">§1</a></td></tr>
<tr><td>$\mathbf v$, $\lVert\mathbf v\rVert$, $(v_x,v_y)$</td><td>a vector, its magnitude, its sagittal-plane components</td><td>—</td><td><a href="#setup">§1</a></td></tr>
<tr><td>$\mathbf F$, $\mathbf F_i$</td><td>a force, the $i$-th force on a free body</td><td>N</td><td><a href="#setup">§1</a></td></tr>
<tr><td>$\mathbf g$, $g$</td><td>gravitational field and its magnitude</td><td>m s⁻²</td><td><a href="#setup">§1</a></td></tr>
<tr><td>$\mathbf W$, $W$, $W_k$, $W_s$, $W_L$</td><td>weight; of the $k$-th mass, the segment, the load</td><td>N</td><td><a href="#setup">§1</a></td></tr>
<tr><td>$\mathbf r$, $\mathbf r_i$, $\mathbf r_{\text{COM}}$</td><td>position vector from the reference point $O$; of particle $i$; of the COM</td><td>m</td><td><a href="#setup">§1</a></td></tr>
<tr><td>$O$</td><td>reference point for moments (the joint axis in every segment analysis)</td><td>—</td><td><a href="#setup">§1</a></td></tr>
<tr><td>$\mathbf M$, $\mathbf M_i$, $M_z$</td><td>moment (torque) of a force; of the $i$-th force; its signed sagittal-plane scalar</td><td>N m</td><td><a href="#moment">§2</a></td></tr>
<tr><td>$\varphi$</td><td>angle between $\mathbf r$ and $\mathbf F$ (D4: between the muscle line and the forearm)</td><td>rad</td><td><a href="#moment">§2</a></td></tr>
<tr><td>$d$, $d_k$, $d_m$, $d_{\text{es}}$, $d_{\text{COM}}$</td><td>moment arm: generic; of the $k$-th weight; of the elbow flexor; of the erector spinae; of the whole-body weight about the ankle</td><td>m</td><td><a href="#moment">§2</a></td></tr>
<tr><td>$\mathbf a_{\text{COM}}$, $a$, $a_y$</td><td>acceleration of the COM and its vertical component</td><td>m s⁻²</td><td><a href="#setup">§1</a></td></tr>
<tr><td>$\mathbf H$</td><td>angular momentum about a fixed point (see B13)</td><td>kg m² s⁻¹</td><td><a href="#setup">§1</a></td></tr>
<tr><td>$\mathbf J$, $J$, $J_x$, $J_y$</td><td>joint contact (reaction) force on the segment; its magnitude; its along-bone and transverse components</td><td>N</td><td><a href="#equil">§3</a></td></tr>
<tr><td>$\tau$, $\tau(\theta)$, $\tau_{\text{L5/S1}}$, $\tau_{\text{ankle}}$, $\tau_{\text{sh}}$</td><td>net muscle moment about a joint</td><td>N m</td><td><a href="#equil">§3</a></td></tr>
<tr><td>$m_s$, $r_s$</td><td>forearm+hand mass and COM distance from the elbow</td><td>kg, m</td><td><a href="#main">§4</a></td></tr>
<tr><td>$m_L$, $r_L$</td><td>held load mass and its distance from the joint (grip, or horizontal reach in §6)</td><td>kg, m</td><td><a href="#main">§4</a></td></tr>
<tr><td>$\theta$</td><td>forearm angle below the horizontal</td><td>rad</td><td><a href="#main">§4</a></td></tr>
<tr><td>$F_m$, $F_{\max}$</td><td>muscle force; its capacity (K5, K9)</td><td>N</td><td><a href="#muscle">§5</a></td></tr>
<tr><td>$m_{\text{ub}}$, $r_t$, $\ell_t$</td><td>upper-body (head+arms+trunk) mass; its horizontal and along-trunk COM distance from L5/S1</td><td>kg, m, m</td><td><a href="#general">§6</a></td></tr>
<tr><td>$\beta$</td><td>trunk flexion angle from vertical</td><td>rad</td><td><a href="#general">§6</a></td></tr>
<tr><td>$F_{\text{es}}$, $C$</td><td>erector-spinae force; disc compression (6.1)</td><td>N</td><td><a href="#general">§6</a></td></tr>
<tr><td>$m_{\text{HAT}}$, $m_{\text{above}}$, $M_{\text{body}}$, $m_{\text{arm}}$, $m_a$, $r_a$, $d_{\perp}$, $d_{\text{HAT}}$</td><td>segment masses and arms in the §6 joint table and D2 (symbolic; no values assigned)</td><td>kg, m</td><td><a href="#general">§6</a></td></tr>
<tr><td>$\mathbf F_{\text{GRF}}$, $F_{\text{GRF}}$</td><td>ground reaction force and its vertical magnitude</td><td>N</td><td><a href="#ground">§7</a></td></tr>
<tr><td>$p(\mathbf x)$, $\mathbf x_{\text{COP}}$, $x_{\text{COP}}$, $x_{\text{COM}}$</td><td>sole pressure distribution; centre of pressure; horizontal positions of COP and COM</td><td>Pa, m</td><td><a href="#ground">§7</a></td></tr>
<tr><td>$I$, $\alpha$</td><td>moment of inertia and angular acceleration (Definition 7.5)</td><td>kg m², rad s⁻²</td><td><a href="#ground">§7</a></td></tr>
<tr><td>$L_f$</td><td>foot length, ankle to toe</td><td>m</td><td><a href="#ground">§7</a></td></tr>
<tr><td>$\ell$, $\omega_0$</td><td>COM height and inverted-pendulum growth rate $\sqrt{g/\ell}$ (K6)</td><td>m, s⁻¹</td><td>K6</td></tr>
<tr><td>$L$</td><td>linear body size in scaling arguments (C9, D8)</td><td>m</td><td>C9</td></tr>
<tr><td>$s$</td><td>reach extension beyond the fingertips (D1; see B13)</td><td>m</td><td>D1</td></tr>
<tr><td>$\ell_L$</td><td>along-trunk distance of the load (D5)</td><td>m</td><td>D5</td></tr>
<tr><td>$R_L$, $R_R$, $x_L$, $x_R$</td><td>vertical reactions and positions of the left and right foot (D6)</td><td>N, m</td><td>D6</td></tr>
<tr><td>$h$, $f$, $P$, $E_{\text{step}}$, $v$</td><td>step height, cadence, mechanical power, work per step, vertical speed (D10, K8)</td><td>m, s⁻¹, W, J, m s⁻¹</td><td>D10</td></tr>
<tr><td>$v_{\text{TO}}$, $h_{\text{jump}}$</td><td>take-off velocity and jump height (K7)</td><td>m s⁻¹, m</td><td>K7</td></tr>
<tr><td>$d_0$, $d_1$</td><td>coefficients of the moment-arm model $d_m(\theta)=d_0+d_1\sin\theta$ (K1, K9)</td><td>m</td><td>K1</td></tr>
</table>
```

### B12. Six empirical numbers used in the text are in no table

Location: `module01.html:357` ($0.60\times70$, $r_t\approx0.30$, $d_{\text{es}}\approx0.05$, $60^\circ$), `module01.html:362` (NIOSH $3.4$ kN), `module01.html:387` ("A typical foot extends only $\sim12$ cm"), `module01.html:653` (`m_a=0.05*70, r_a=0.28`, values that appear only inside the K3 code), `module01.html:698` ($\ell=1.0$ m).

Missing part: the brief's number classes. None of these is derived, tabulated, or labelled "assume". The Winter citation for the existing rows is unverified (no PDF in the repo) and must not be extended from memory; the new rows are labelled as assumptions of this course. Replacement for the parameter table (lines 771 to 778):

```html
<table>
<tr><th>Quantity</th><th>Symbol</th><th>Fraction / model</th><th>Value (70 kg adult)</th><th>Class</th></tr>
<tr><td>Body mass (reference human)</td><td>$M$</td><td>—</td><td>$70\ \mathrm{kg}$</td><td>assumed</td></tr>
<tr><td>Forearm+hand mass</td><td>$m_s$</td><td>$0.022\,M$</td><td>$1.54\ \mathrm{kg}$</td><td>parameter (Winter regression; citation unverified)</td></tr>
<tr><td>Forearm+hand COM from elbow</td><td>$r_s$</td><td>$\approx 0.43\,\ell_{\text{fa}}$</td><td>$0.116\ \mathrm m$</td><td>parameter (Winter regression; citation unverified)</td></tr>
<tr><td>Grip distance from elbow</td><td>$r_L$</td><td>—</td><td>$0.35\ \mathrm m$</td><td>assumed</td></tr>
<tr><td>Elbow flexor moment arm (horizontal forearm)</td><td>$d_m$</td><td>—</td><td>$0.03\ \mathrm m$</td><td>assumed</td></tr>
<tr><td>Elbow flexor moment arm vs angle (K1, K9)</td><td>$d_m(\theta)$</td><td>$0.030-0.012\sin\theta$</td><td>$0.030\to0.018\ \mathrm m$</td><td>assumed model</td></tr>
<tr><td>Upper-body (head+arms+trunk) mass</td><td>$m_{\text{ub}}$</td><td>$0.60\,M$</td><td>$42\ \mathrm{kg}$</td><td>assumed fraction</td></tr>
<tr><td>Trunk flexion in the §6 stoop</td><td>$\beta$</td><td>—</td><td>$60^\circ$</td><td>assumed</td></tr>
<tr><td>Upper-body COM, horizontal reach from L5/S1 at $\beta=60^\circ$</td><td>$r_t$</td><td>$\ell_t\sin\beta$</td><td>$0.30\ \mathrm m$</td><td>assumed</td></tr>
<tr><td>Upper-body COM, along-trunk distance from L5/S1</td><td>$\ell_t$</td><td>$r_t/\sin60^\circ$</td><td>$0.346\ \mathrm m$</td><td>derived</td></tr>
<tr><td>Load reach in the §6 stoop</td><td>$r_L$ (§6)</td><td>—</td><td>$0.40\ \mathrm m$</td><td>assumed</td></tr>
<tr><td>Erector-spinae moment arm</td><td>$d_{\text{es}}$</td><td>—</td><td>$0.05\ \mathrm m$</td><td>assumed</td></tr>
<tr><td>Disc-compression action limit (NIOSH)</td><td>—</td><td>—</td><td>$3400\ \mathrm N$</td><td>external limit; citation unverified</td></tr>
<tr><td>Foot length, ankle to toe</td><td>$L_f$</td><td>—</td><td>$0.12\ \mathrm m$</td><td>assumed</td></tr>
<tr><td>Whole-body COM height (K6)</td><td>$\ell$</td><td>—</td><td>$1.0\ \mathrm m$</td><td>assumed</td></tr>
<tr><td>Elbow flexor force capacity</td><td>$F_{\max}$</td><td>—</td><td>$1500\ \mathrm N$ (K5), $2000\ \mathrm N$ (K9)</td><td>assumed</td></tr>
<tr><td>Sustainable mechanical power (K8)</td><td>—</td><td>—</td><td>$250\ \mathrm W$</td><td>assumed</td></tr>
<tr><td>Gravitational field</td><td>$g$</td><td>—</td><td>$9.81\ \mathrm{m\,s^{-2}}$</td><td>constant</td></tr>
</table>
```

Then at line 357 write "Assume" before the stoop values (done in the B2 replacement), at line 387 replace "A typical foot extends only $\sim 12\ \mathrm{cm}$ from the ankle to the toe" with "With the Appendix foot length $L_f=0.12\ \mathrm m$ from ankle to toe", and drop $m_a$, $r_a$ from K3 (B15 moves K3 to the elbow, where every value is in the table).

### B13. Symbol collisions

Location: `module01.html:166-169` ($M$ as moment magnitude) against `147`, `156`, `385`, `389`, `703`, `718` ($M$ as mass); `module01.html:565-569` ($a$ as reach offset) against `389`, `543`, `597`, `713` ($a$ as acceleration); `module01.html:156`, `389` ($\mathbf L$ angular momentum) against `555`, `601` ($L$ body size) and `605` ($L_f$); `module01.html:715` ($h$ jump height) against `609`, `727` ($h$ step height); `module01.html:611` ($W_{\text{step}}$ work) against `143` ($W$ weight).

Missing part: notation as a contract. Replacements, cheapest touchpoints:

- Moment magnitude (3 lines plus the caption). Line 166: `magnitude\quad M=\lVert\mathbf{r}\rVert\,\lVert\mathbf{F}\rVert\sin\varphi` to `magnitude\quad \lVert\mathbf M\rVert=\lVert\mathbf{r}\rVert\,\lVert\mathbf{F}\rVert\sin\varphi`. Line 168: `\boxed{\,M = d\,\lVert\mathbf{F}\rVert\,}` to `\boxed{\,\lVert\mathbf M\rVert = d\,\lVert\mathbf{F}\rVert\,}`. Line 169: `reduces to the signed scalar $M=x F_y - y F_x$` to `reduces to the signed scalar $M_z=x F_y - y F_x$`. Line 199: `$M=d\lVert\mathbf F\rVert$` to `$\lVert\mathbf M\rVert=d\lVert\mathbf F\rVert$`.
- Angular momentum: lines 156 and 389, replace every `\mathbf L` and `\dot{\mathbf L}` with `\mathbf H` and `\dot{\mathbf H}` ("with $\mathbf H$ the angular momentum").
- D1 offset: lines 565 to 569, replace the symbol $a$ by $s$ ("a horizontal offset $s$ beyond the fingertips", `$\tau(\theta)=g\cos\theta\bigl(m_s r_s+m_L (r_L+s)\bigr)$`, `$\partial\tau/\partial s=g\,m_L\cos\theta$`); in the SVG at line 566 change the labels `rₗ + a` to `rₗ + s` and `a` to `s`.
- K7: line 715, `$h=v_{\text{TO}}^2/2g\approx0.42$ m` to `$h_{\text{jump}}=v_{\text{TO}}^2/2g\approx0.42$ m`.
- D10: line 611, `$W_{\text{step}}=Mgh$` to `$E_{\text{step}}=Mgh$`.

### B14. Anatomical terms used before they are glossed

Location and replacement, each in the sentence of first use:

- `module01.html:343`: "the calf muscles plantarflexing the foot at push-off" to "the calf muscles plantarflexing the foot (pointing it downward, as when rising on the toes) at push-off"; and "the Achilles pulls up at the heel" to "the Achilles tendon (the cord joining the calf muscles to the heel bone) pulls up at the heel".
- `module01.html:385`: "the ankle plantarflexors must supply a torque" to "the ankle plantarflexors (the calf muscles that point the foot down) must supply a torque".
- `module01.html:351`: "Arm abducted, load in hand" to "Arm abducted (raised sideways away from the trunk), load in hand"; same gloss at the first use in K3 if K3 keeps the shoulder (B15 removes it).
- `module01.html:357`: "from the L5/S1 disc" to "from the L5/S1 disc (the intervertebral disc, the cartilage pad between the lowest lumbar vertebra and the sacrum)" (included in the B2 replacement).
- `module01.html:404`: "the biceps/brachialis must pull" to "the biceps and brachialis (the two main elbow flexors on the front of the upper arm) must pull".
- `module01.html:499`: "Antagonist co-contraction" to "Antagonist co-contraction (the opposing muscle pulling at the same time)".
- `module01.html:603`: "physiological cross-section" to "physiological cross-section (the muscle's fibre area measured perpendicular to the fibres)".
- `module01.html:739` legend "measured MVC": expand "MVC (maximum voluntary contraction)" in the K9 statement (included in the B7 replacement).

### B15. Five computational problems are plug-in arithmetic: K3, K4, K5, K8, K10

Test applied: does solving it surface anything the reader could not read straight off (4.1), (5.1), (6.1), or $P=Mghf$? K3 perturbs a bilinear product by 15 %, so each bar is 15 % of its term by construction. K4 and K5 invert one linear expression at four values. K8 solves $f=250/(Mgh)$ three times. K10 rearranges one line. K1, K2, K6, K7 pass the test and stay; K9 stays after B7. Full replacements follow; every number was produced by the code shown (scratchpad `m01/replacements.py`, `m01/k4new.py`). Figures are to be regenerated from the code, not hand-drawn.

K3 moves from the shoulder to the elbow. Reason: the elbow uses only Appendix values, while the shoulder needed $m_a=0.05M$ and $r_a=0.28$ m, two bare numbers that appeared only in code. The new K3 propagates the same $\pm15\%$ scatter the Appendix states into the muscle force, where the moment arm enters as a divisor.

```html
<p><b>K3.</b> The Appendix warns that anthropometric values scatter by $10$–$15\%$ between people. Propagate a $\pm15\%$ uncertainty in each of $\{m_s, r_s, m_L, r_L, d_m\}$ into the elbow muscle force $F_m$ of <a class="secref" href="#worked">§8</a>, one parameter at a time (a tornado), then all five at once (sample each uniformly within $\pm15\%$, $10^5$ draws) and report the 5th to 95th percentile band. Which parameter is worth measuring, and why is its effect asymmetric? <span class="probes">Probes: a sensitivity sweep through a quotient, where the divisor's uncertainty dominates and is asymmetric.</span></p>
<figure><!-- regenerate: tornado bars of ΔF_m for the five parameters, plus the joint-sweep band --><figcaption>Tornado of $\pm15\%$ perturbations of the elbow muscle force: $d_m$ dominates and is asymmetric ($-15\%$ in $d_m$ raises $F_m$ by $17.6\%$, $+15\%$ lowers it by $13.0\%$); the joint sweep spans $496$ to $797$ N.</figcaption></figure>
<details class="sol"><summary>Show solution</summary><p>With $F_m=g(m_sr_s+m_Lr_L)/d_m=631$ N at the base values, the segment terms hardly matter ($\pm8.8$ N, $1.4\%$) and the load terms move $F_m$ by $\pm85.8$ N ($13.6\%$), both symmetric because they enter linearly. The moment arm enters as a divisor: $d_m$ at $+15\%$ gives $-82$ N ($-13.0\%$) but $d_m$ at $-15\%$ gives $+111$ N ($+17.6\%$), the largest single effect and skewed upward, because $1/(1-\epsilon)\gt1/(1+\epsilon)$ in magnitude. Sampling all five at once, the 5th to 95th percentile band of $F_m$ is $496$ to $797$ N (median $629$ N), a $\pm24\%$ spread from $\pm15\%$ inputs. So the quantity to measure is the moment arm, and a model that reports a single $F_m$ to three figures is overclaiming; Module 15 returns to this uncertainty propagation.</p>
<div class="codewrap"><button class="copybtn" onclick="copyCode(this)"><span class="lbl">Copy</span></button><pre><code>import numpy as np

g = 9.81
p = dict(m_s=0.022*70, r_s=0.116, m_L=5.0, r_L=0.35, d_m=0.03)


def force(m_s, r_s, m_L, r_L, d_m):
    return g*(m_s*r_s + m_L*r_L)/d_m


base = force(**p)
for k in p:
    hi = force(**dict(p, **{k: p[k]*1.15})) - base
    lo = force(**dict(p, **{k: p[k]*0.85})) - base
    print(f"{k}: +15% -> {hi:+.1f} N, -15% -> {lo:+.1f} N")
rng = np.random.default_rng(0)
n = 100000
samp = {k: p[k]*rng.uniform(0.85, 1.15, n) for k in p}
F = force(**samp)
print(f"5th-95th pct {np.percentile(F, 5):.0f}-{np.percentile(F, 95):.0f} N")
# m_L, r_L: +-85.8 N ; d_m: -82.3 / +111.3 N ; band 496-797 N</code></pre></div></details>
```

K4 becomes a joint sweep over trunk angle and reach, which also derives the "more than half" claim of section 6.

```html
<p><b>K4.</b> Sweep the stooped-lift geometry of Proposition 6.1 jointly over trunk angle $\beta\in\{60,45,30,20,10\}^\circ$ and load reach $r_L\in\{0.4,0.3,0.2\}$ m, with the upper-body COM at along-trunk distance $\ell_t=0.346$ m so that $r_t=\ell_t\sin\beta$ (Appendix). For the $20$ kg box report the compression $C$ and, at each geometry, the largest load that keeps $C$ under the NIOSH $3400$ N action limit. Which move, standing up or pulling the box in, buys more, and where do the two combine to halve the load? <span class="probes">Probes: a two-parameter sweep of a safety boundary, separating posture from reach.</span></p>
<figure><!-- regenerate: contour or table of C(β, r_L) with the 3400 N boundary --><figcaption>Disc compression for a 20 kg box across trunk angle and reach. Pulling the box in at a $60^\circ$ stoop cuts $C$ by 18 %; standing to $20^\circ$ with the box at $0.2$ m cuts it by 46 %; only near-upright ($10^\circ$) halves it.</figcaption></figure>
<details class="sol"><summary>Show solution</summary><p>At the section 6 stoop ($\beta=60^\circ$, $r_L=0.4$ m) $C=4346$ N and the safe load is $8.7$ kg. Pulling the box to $0.2$ m at the same stoop gives $3561$ N (18 % cut, safe load $16.4$ kg). Standing to $\beta=30^\circ$ with the box still at $0.4$ m gives $3524$ N (19 %, $18.6$ kg): posture alone buys as much as reach alone. Combining $\beta=20^\circ$ with $0.2$ m gives $2333$ N (46 %, $42$ kg), and $\beta=10^\circ$ with $0.2$ m gives $1879$ N (57 %, $51$ kg). The muscle term scales with $\sin\beta$ through $r_t$ and with $r_L$ through the load; the weight term grows as $\cos\beta$ when standing up but is only $\sim0.6$ kN, so it never reverses the trend. The "more than half" of <a class="secref" href="#general">§6</a> requires both moves.</p>
<div class="codewrap"><button class="copybtn" onclick="copyCode(this)"><span class="lbl">Copy</span></button><pre><code>import numpy as np

g, m_ub, d_es = 9.81, 0.60*70, 0.05
l_t = 0.30/np.sin(np.radians(60))    # along-trunk COM distance


def comp(m_L, r_L, beta_deg):
    b = np.radians(beta_deg)
    tau = g*(m_ub*l_t*np.sin(b) + m_L*r_L)
    return tau/d_es + (m_ub + m_L)*g*np.cos(b)


C0 = comp(20, 0.4, 60)
m = np.linspace(0, 60, 6001)
for beta in [60, 45, 30, 20, 10]:
    for r in [0.4, 0.3, 0.2]:
        C = comp(20, r, beta)
        ok = np.where(comp(m, r, beta) &lt;= 3400)[0]
        print(f"beta={beta:2d} r_L={r}: C={C:.0f} N "
              f"({100*(1 - C/C0):.0f}% cut), max {m[ok[-1]]:.1f} kg")
# 60/0.4: 4346 N, 8.7 kg ; 60/0.2: 3561 N (18%), 16.4 kg
# 30/0.4: 3524 N (19%) ; 20/0.2: 2333 N (46%) ; 10/0.2: 1879 N (57%)</code></pre></div></details>
```

K5 becomes a regime comparison with the K1 moment-arm model and an argmin.

```html
<p><b>K5.</b> Given a fixed elbow-flexor force capacity $F_{\max}=1500$ N, compute the maximum load a person can hold statically as a function of forearm angle $\theta$, first with the constant $d_m=0.03$ m and then with the K1 model $d_m(\theta)=0.030-0.012\sin\theta$. Find the angle of <em>minimum</em> capacity in each case. Is the weakest posture the horizontal one? <span class="probes">Probes: an argmin over angle and a regime comparison of two moment-arm models; the weakest posture moves off horizontal.</span></p>
<figure><!-- regenerate: the two capacity curves with the minimum marked at 23.6° --><figcaption>Maximum holdable load vs. angle. With a constant moment arm the capacity is lowest at the horizontal ($12.6$ kg) and rises monotonically; with the shrinking arm it dips to $11.5$ kg at $23.6^\circ$ before rising.</figcaption></figure>
<details class="sol"><summary>Show solution</summary><p>Inverting $F_{\max}d_m(\theta)=g\cos\theta(m_sr_s+m_Lr_L)$ gives $m_L^{\max}(\theta)=\bigl(F_{\max}d_m(\theta)/(g\cos\theta)-m_sr_s\bigr)/r_L$. With constant $d_m$ the capacity is $12.6$ kg at horizontal and grows monotonically ($13.8$, $18.0$, $25.7$, $75.0$ kg at $23.6^\circ$, $45^\circ$, $60^\circ$, $80^\circ$), because only $\cos\theta$ varies. With the shrinking arm the quotient $d_m(\theta)/\cos\theta$ has a stationary point where $\sin\theta=0.012/0.030=0.4$, that is $\theta=23.6^\circ$, and it is a minimum: the capacity dips to $11.5$ kg there, $9\%$ below the horizontal value, then rises ($12.8$, $16.6$, $45.2$ kg at $45^\circ$, $60^\circ$, $80^\circ$), always below the constant-arm curve. The weakest posture is therefore not the horizontal forearm but one lowered by about $24^\circ$, the same angle at which K1 found the peak muscle force for a fixed load, as it must be. The divergence as $\theta\to90^\circ$ survives in both models: a hanging forearm needs no holding torque.</p>
<div class="codewrap"><button class="copybtn" onclick="copyCode(this)"><span class="lbl">Copy</span></button><pre><code>import numpy as np

g, m_s, r_s, r_L, Fmax = 9.81, 0.022*70, 0.116, 0.35, 1500.0
th = np.linspace(0, np.radians(80), 8001)
cap_con = (Fmax*0.03/(g*np.cos(th)) - m_s*r_s)/r_L
cap_var = (Fmax*(0.03 - 0.012*np.sin(th))/(g*np.cos(th))
           - m_s*r_s)/r_L
i = int(np.argmin(cap_var))
print(f"weakest {np.degrees(th[i]):.1f} deg: {cap_var[i]:.1f} kg")
for d in [0, 23.6, 45, 60, 80]:
    j = int(np.argmin(abs(np.degrees(th) - d)))
    print(f"{d:5.1f} deg: const {cap_con[j]:.1f}, varying {cap_var[j]:.1f} kg")
# weakest 23.6 deg: 11.5 kg ; const 12.6/13.8/18.0/25.7/75.0
# varying 12.6/11.5/12.8/16.6/45.2 kg</code></pre></div></details>
```

K8 becomes a comparison of average against peak demand under a stated rise profile.

```html
<p><b>K8.</b> D10 gives the <em>average</em> stair-climbing power $\bar P=Mghf$. Assume that within each step period $T=1/f$ the COM rises smoothly, $z(t)=\tfrac{h}{2}\bigl(1-\cos(\pi t/T)\bigr)$, so it is momentarily at rest at each step. For $M=70$ kg and $h=0.15,\,0.18,\,0.20$ m, sweep the cadence $f$ from $1$ to $2.5$ steps/s and compute, from Definition 7.5, the instantaneous GRF $M(g+\ddot z)$ and power $M(g+\ddot z)\dot z$. Report the cadence at which $\bar P$ hits the assumed sustainable $250$ W, the ratio of peak to average power, and the cadence at which the peak GRF reaches $1.3$ body weights (assume this as a comfort threshold). Which step height limits the pace, and by what factor does the average criterion understate the peak? <span class="probes">Probes: a regime comparison of average versus peak demand; the inertial term scales as $f^2$ while the average is linear in $f$.</span></p>
<figure><!-- regenerate: average and peak power vs cadence for the three h, with the 250 W line --><figcaption>Average (dashed) and peak (solid) power vs. cadence for three step heights. The average is linear in $f$; the peak runs $1.6$ to $1.8$ times higher and the gap widens with cadence as the inertial term grows as $f^2$.</figcaption></figure>
<details class="sol"><summary>Show solution</summary><p>Differentiating the assumed profile, $\dot z=\tfrac{h\pi f}{2}\sin(\pi ft)$ and $\ddot z=\tfrac{h\pi^2f^2}{2}\cos(\pi ft)$. The average power integrates back to $Mghf$ exactly, because the inertial term $M\ddot z\dot z$ averages to zero over a step. So the $250$ W average is reached at $f=2.43$, $2.02$, $1.82$ steps/s for $h=0.15$, $0.18$, $0.20$ m: the tallest step limits the pace. The peak power is higher: at $f=1.5$ it is $246$, $297$, $331$ W against averages of $154$, $185$, $206$ W (ratio $1.59$ to $1.61$), and at $f=2.5$ the ratio has grown to $1.71$ to $1.80$ because the inertial part of the power scales as $f^3$ while the gravitational part scales as $f$. The peak GRF is $M(g+h\pi^2f^2/2)$: it reaches $1.3$ body weights at $f=1.99$, $1.82$, $1.73$ steps/s, again earliest for the tallest step, and $1.63$ body weights at $2.5$ steps/s on $0.20$ m steps. A sustainable-average criterion therefore understates the instantaneous muscle and joint demand by about $1.6$ at a comfortable pace and by $1.8$ at a fast one. The rest-at-each-step profile is the harshest smooth assumption; a gait that keeps the COM moving lowers $\ddot z$ and closes part of the gap (Module 8).</p>
<div class="codewrap"><button class="copybtn" onclick="copyCode(this)"><span class="lbl">Copy</span></button><pre><code>import numpy as np

M, g, ceil = 70.0, 9.81, 250.0
for h in [0.15, 0.18, 0.20]:
    print(f"h={h}: 250 W average at f={ceil/(M*g*h):.2f}/s, "
          f"1.3 BW peak at f={np.sqrt(0.6*g/(h*np.pi**2)):.2f}/s")
    for f in [1.0, 1.5, 2.0, 2.5]:
        T = 1/f
        t = np.linspace(0, T, 4001)
        v = (h*np.pi/(2*T))*np.sin(np.pi*t/T)
        a = (h*np.pi**2/(2*T**2))*np.cos(np.pi*t/T)
        P = M*(g + a)*v
        print(f"  f={f}: avg {M*g*h*f:.0f} W, peak {P.max():.0f} W, "
              f"ratio {P.max()/(M*g*h*f):.2f}, "
              f"peak GRF {(g + a.max())/g:.2f} BW")
# h=0.18: 250 W at 2.02/s ; f=1.5: avg 185, peak 297 W (1.60), 1.20 BW
# f=2.5: avg 309, peak 546 W (1.77), 1.57 BW ; 1.3 BW at 1.82/s</code></pre></div></details>
```

K10 becomes a three-way regime map over load and angle.

```html
<p><b>K10.</b> To reduce elbow torque you may (a) carry $2$ kg less, (b) shorten the reach by $8$ cm, or (c) lower the forearm by $15^\circ$. From (4.1), compute the torque saved by each intervention over the plane of base load $m_L\in[0,25]$ kg and forearm angle $\theta\in[0,60^\circ]$, and map which intervention wins where. Show that the mass-versus-reach crossover is independent of $\theta$, and find, for a $5$ kg load, the angle beyond which lowering the arm beats both. <span class="probes">Probes: a two-parameter regime map with three competing interventions; one crossover is angle-independent, the other is not.</span></p>
<figure><!-- regenerate: regime map over (m_L, θ) with the three winning regions --><figcaption>Which intervention saves the most torque. Shedding 2 kg wins for light loads at small angles; shortening the reach wins above $8.75$ kg at small angles; lowering the arm $15^\circ$ wins beyond about $30$ to $36^\circ$ at any load.</figcaption></figure>
<details class="sol"><summary>Show solution</summary><p>With $\Delta m=2$ kg, $\Delta r=0.08$ m, $\Delta\theta=15^\circ$, the savings are $S_m=g\,\Delta m\,r_L\cos\theta$, $S_r=g\,m_L\,\Delta r\cos\theta$, and $S_\theta=g\,(m_sr_s+m_Lr_L)\bigl(\cos\theta-\cos(\theta+\Delta\theta)\bigr)$. The first two share the factor $\cos\theta$, so their crossover $m_L=\Delta m\,r_L/\Delta r=8.75$ kg holds at every angle: below it shed mass ($6.87$ N m at horizontal, falling as $\cos\theta$), above it pull the load in. Lowering the arm saves almost nothing at horizontal ($0.64$ N m for $5$ kg, since $\cos\theta$ is stationary there) but grows with $\theta$ while the other two shrink. Solving $S_\theta=S_r$ gives the boundary $\theta=29.8^\circ$, $33.8^\circ$, $35.1^\circ$, $36.1^\circ$ for $m_L=2$, $5$, $8.75$, $20$ kg, nearly load-independent; solving $S_\theta=S_m$ gives $71^\circ$, $52^\circ$, $35^\circ$, $14^\circ$ for the same loads, strongly load-dependent. For a $5$ kg load lowering the arm beats reach-shortening beyond $34^\circ$ and beats shedding mass beyond $52^\circ$, so it wins outright only past $52^\circ$. The practical rule: near horizontal, change the load (mass if light, reach if heavy); once the forearm is well below horizontal, change the angle.</p>
<div class="codewrap"><button class="copybtn" onclick="copyCode(this)"><span class="lbl">Copy</span></button><pre><code>import numpy as np
from scipy.optimize import brentq

g, m_s, r_s, r_L = 9.81, 0.022*70, 0.116, 0.35
dm, dr, dth = 2.0, 0.08, np.radians(15)


def savings(m_L, th):
    c = np.cos(th)
    s_m = g*dm*r_L*c
    s_r = g*m_L*dr*c
    s_t = g*(m_s*r_s + m_L*r_L)*(c - np.cos(th + dth))
    return s_m, s_r, s_t


print(f"mass/reach crossover {dm*r_L/dr:.2f} kg at every angle")
for m_L in [2, 5, 8.75, 20]:
    t_r = brentq(lambda t: savings(m_L, t)[2] - savings(m_L, t)[1],
                 1e-3, np.radians(85))
    t_m = brentq(lambda t: savings(m_L, t)[2] - savings(m_L, t)[0],
                 1e-3, np.radians(85))
    print(f"m_L={m_L}: lowering beats reach beyond {np.degrees(t_r):.1f}, "
          f"beats mass beyond {np.degrees(t_m):.1f} deg")
# crossover 8.75 kg ; m_L=5: beats reach beyond 33.8, mass beyond 51.8 deg</code></pre></div></details>
```

### B16. K7 and D7 present an invented acceleration pulse as a measurement

Location: `module01.html:713` ("A force-plate study gives the vertical COM acceleration during a jump take-off as…") and `module01.html:599` ("K7 evaluates it for a measured pulse").

Missing part: number class. The brief states there are no laboratory measurements in this course. The half-sine is a modelling assumption and must say so. Replacement for the opening of line 713: "Assume a half-sine model of the vertical COM acceleration during a jump take-off, $a(t)=15\sin(\pi t/0.3)\ \mathrm{m\,s^{-2}}$ over $0\le t\le0.3$ s (the shape a force plate typically records; the amplitude is assumed)." Replacement for the end of line 599: "K7 evaluates it for an assumed half-sine pulse."

### B17. Section 0 names the phenomenon but not the question or the level; section 10 does not say what the reader can now do

Location: `module01.html:134-135`, `module01.html:505`.

Missing part: the brief's page shape (level stated, closing capability). Insert after line 135:

```html
<p>The question this module answers is the one in the course map: <em>how hard must a muscle pull to hold a weight, and what does the joint carry as a result?</em> Every model here sits on <b>Level 1</b> of the course's level ladder (static equilibrium of rigid segments, one net muscle moment per joint). Definition 7.5 opens the door to Level 2 (planar rigid-body dynamics) but computes nothing there; Modules 7 to 9 do.</p>
```

Insert after line 505, at the end of section 10:

```html
<p><b>What you can now do.</b> Draw the free body of any segment, take moments about its joint to get the muscle torque (Proposition 3.1), divide by the moment arm to get the muscle force (5.1), close the force balance to get the joint reaction (5.2 or 6.1), and place the center of pressure under the center of mass to test whether a posture can be held at all (7.4). You can put a number on every static hold, lean, and lift in daily life, and you know which single number (the moment arm) your answer is most sensitive to.</p>
```

### B18. Law 1 uses the cross product two sections before it is defined

Location: `module01.html:152-158` (Law 1 and its proof, using $(\mathbf r_i-\mathbf r_A)\times\mathbf F_i$) against `module01.html:165` (Definition 2.1, the moment).

Missing part: dependencies point backward only. The statement of Law 1 even says "The moment $\mathbf M_i$ … is defined in §2." Fix by moving, not rewriting: move the block from line 165 (`<div class="def"><b>Definition 2.1`) through line 201 (the "key consequence" paragraph) to immediately after line 150, under a heading `<h3>The moment of a force</h3>`, and leave section 2 as a one-paragraph pointer ("Definition 2.1 and Fig. 2 in §1 define the moment; this section records the consequence used everywhere below") or delete section 2 and renumber. With B3 in place, Lemma 1.4a also needs the cross product, so the moved block must sit before Definition 1.4 as well: place it right after Definition 1.3.

### B19. The joint table gives torque ranges with no source class

Location: `module01.html:349-355`, column "Order of magnitude" ($10$–$40$, $20$–$70$, $50$–$150$, $30$–$150$, $10$–$120$, $100$–$400$ N m).

Missing part: number class. None of the six ranges is derived, tabulated, or labelled. The elbow row is derivable ($18.9$ N m at $5$ kg from §8) and the low-back row is derived just below ($202$ N m); the other four are bare. Replacement for the header cell at line 349: `<th>Order of magnitude (assumed typical ranges; elbow and low back are computed in §8 and §6)</th>`. Do not add values from memory; a later module that computes the hip, knee, ankle, or shoulder torque should replace the range with its number.

## 3. Style and clarity edits

Apply in one pass.

1. `module01.html:201` "the moment arm is simply the <em>horizontal</em> distance" to "the moment arm is the <em>horizontal</em> distance". Same deletion of "simply" at `323` ("do not simply cancel" to "do not cancel"), `575` ("Proposition 3.1 simply carries" to "Proposition 3.1 carries"), `738` (handled in B7).
2. `module01.html:167` add the one-line argument for the moment arm: after "is the perpendicular distance from $O$ to the force's line of action" insert "(drop a perpendicular from $O$ to the line; its length is $\lVert\mathbf r\rVert\sin\varphi$ by the right triangle with hypotenuse $\mathbf r$)". After "reduces to the signed scalar $M_z=xF_y-yF_x$" insert "(the $z$-component of $\mathbf r\times\mathbf F$ with $\mathbf r=(x,y,0)$, $\mathbf F=(F_x,F_y,0)$)".
3. `module01.html:211` Proposition 3.1 proof, "all gravitational moments share the same rotational sense (they pull the segment down)" to "all gravitational moments share the same rotational sense because every mass lies on the same side of $O$ (distal to the joint) and every weight points down".
4. `module01.html:371` Definition 7.2, after "reproducing the true distribution's net force and moment" add "(the net moment about the origin is $\int\mathbf x\,p\,dA=\mathbf x_{\text{COP}}\int p\,dA$, by the definition of $\mathbf x_{\text{COP}}$, which is the moment of the resultant placed there)".
5. `module01.html:373` Definition 7.3, replace "pressure cannot be negative, so the resultant cannot act outside the contact patch" with "$\mathbf x_{\text{COP}}$ is a weighted average of points of the patch with non-negative weights $p\,dA$, and such an average lies in the convex hull of those points".
6. `module01.html:595` D6 solution, after "which (through moment balance about each foot) raises $R_R$ relative to $R_L$" insert the equations: "moments about the left foot give $R_R=W_{\text{tot}}\,(x_{\text{COM}}-x_L)/(x_R-x_L)$ and $R_L=W_{\text{tot}}-R_R$, so $R_R$ grows linearly as $x_{\text{COM}}$ moves right".
7. `module01.html:494` "correct orders of magnitude with no fitting" to "orders of magnitude the validation protocol below can test, with no fitted parameter".
8. `module01.html:488` "the same as adding $\sim1.5$ kg at the original distance" to "the same as adding $\sim1.4$ kg at the original distance" ($4.91/3.43=1.43$).
9. `module01.html:549` (if B4's rewrite is not taken whole) "an $\sim8\times$ amplification" to "a $6.6\times$ amplification over the combined weight of trunk and box".
10. `module01.html:404` "roughly the force of hanging a 64 kg mass from the tendon" to "the weight of a 64 kg mass hung from the tendon".
11. `module01.html:387` "beyond it the only recovery is a step" to "beyond it no admissible COP exists (Proposition 7.4) and the only recovery is a step".
12. `module01.html:524`, `532`, `536`, `540`, `544`, `548`, `552`, `556`, `560`, `566`, `572`, `578`, `584`, `588`, `594`, `598`, `602`, `606`, `610`: aria-labels are the problem statements sliced at 120 characters, with raw `$\theta=0$` TeX inside screen-reader text. Replace each with a one-clause description of what is drawn (for example C1: "Two elbow poses holding the same dumbbell, forearm horizontal and 60 degrees below horizontal, with muscle and load arrows"). The figcaptions already say this and can be reused.
13. `module01.html:135` "the price of the body's lever geometry" is a metaphor that pays for itself in §5; keep it, but add "(quantified in §5 as the ratio $r_L/d_m$)".
14. `module01.html:343` the caption runs to seven lines and carries the lever-class lesson that C4 then tests. Move the second-class-lever sentence ("Most limb muscles are third-class, but not all: …") into the prose after the figure as its own paragraph, so the caption stands alone.
15. `module01.html:634` K2 uses $A$ for the regression slope; D3 uses $A$, $B$ for points. Both are local, but rename the slope to $b$ to keep $A$ for points.

## 4. Structural notes

- Ordering. The moment is defined in §2 but used in §1 (Law 1, Lemma 1.4a). B18 gives the move. After it, §1 holds definitions plus Law 1, §2 shrinks to the "key consequence" paragraph or disappears, and every later dependency points backward.
- Section 6 is the weakest section. It opens with a table of six torque ranges that are neither derived nor labelled, then delivers the module's most consequential number through a sentence cut in half by an uncaptioned figure, with the along-spine force balance asserted. B2, B10 and B19 rebuild it as: joint table (ranges labelled), stoop assumptions, torque, Proposition 6.1 with proof, lumbar figure, stooped-lift figure, key result. That is the shape of §4 and §5, which is the brief's stated model.
- Section 7 has three figures and none is numbered or cited from the prose (B10). Once wrapped, cite them at lines 373, 385 and in Proposition 7.4.
- Figures. Commit `3fd6fbe` scaled stroke widths on lines and arrows by a factor of 5 to 15 across the module (B9 lists every one). Regenerate from the anatomy kit with shaft widths capped, and add a stroke-width gate, because all nine existing gates passed on figures a reader cannot read.
- The problem set. Every problem has a figure, a probes note and a solution, as the convention requires. Five K problems are plug-in (B15). After the replacements, the set covers optimization (K1, K5), inverse problems (K2, K9), sensitivity through a quotient and through two parameters (K3, K4), ODE integration (K6, K7), average-versus-peak regime comparison (K8), and a regime map (K10).
- Cross-references inside the set (D7 to K7, D10 to K8, C9 to D8) are forward within the problem set only; acceptable.
- The level statement and the closing capability paragraph are missing (B17); both are one paragraph.
- No new toy body is introduced; the reference human, the bag, the stooped lift, the lean and the jump all recur in later modules as the brief requires.

## 5. What already works

- Law 1 (`module01.html:152-159`) is proved, including the "about any point" clause, with the difference-of-moment-sums identity written out. D3 then asks the reader to reproduce it. That is the standard.
- Proposition 3.1, Theorem 4.2, Propositions 5.1, 5.2 and 7.4 each carry a proof of matching weight beside the boxed result, and each proof names the free body, the point about which moments are taken, and why the joint force drops out. Rigor parity holds in §3, §4, §5 and §7.
- The worked example (`module01.html:395-404`) states its inputs by symbol, computes in displayed lines a reader can redo with a pen, and its interpretation box ties the number to the elbow, the bag, and body weight. Every figure in it checks: $18.9$ N m, $631$ N, $567$ N, $12.9\times$, $0.83\times$ body weight.
- The lab (`module01.html:409-439`) prints the table it claims, the plotted polylines match the printed torques to the pixel, and the sensitivity paragraph turns two partial derivatives into a rule ("distance dominates") with a number attached.
- All ten K solutions reproduce their printed numbers and captions from the code shown. K1 (argmax with a moving peak), K2 (least-squares recovery), K6 (unstable ODE to a threshold) and K7 (impulse to jump height) are real computational problems.
- The §4 animation drives its keyframes from $\cos\theta$ and its caption names the loop; the §9 plot marks computed positions. These follow the course's figure rules.
- Pillar 1 holds in §1 to §5 and §7: sagittal plane, COM, FBD, moment arm, flexor, distal, erector spinae, L5/S1, HAT, EMG, IMU, dynamometer and kgf are glossed in the sentence of first use.

## 6. Counts

- Blocking defects: 19 (B1 to B19).
- Style and clarity edits: 15.
- Numeric mismatches between code and text: 0 of 65 numbers checked (lab table 11, §8 9, §9 4, §6 6, §7 1, K1 4, K2 1, K3 2, K4 5, K5 4, K6 2, K7 4, K8 4, K9 3, K10 2, C9 1, D1 2). The four lab-plot polyline endpoints were also checked against the printed torques and match. The factual errors found are prose against prose (B4, B5, B6, B7) and a sign error (B1), not code against prose.
- K problems judged plug-in: K3, K4, K5, K8, K10.
