# Editor report: module11.html (Reaching, Waving, Holding, Gripping, and Manipulation)

Editorial pass. Standard: the five-part rule of the `science-editor` skill, read against `EDITOR_DOMAIN.md`. Every location is `module11.html:LINE`. Every replacement is valid HTML with MathJax delimiters and uses only the box classes the stylesheet defines.

All four `<pre><code>` blocks in the file were extracted and run (`m11/blocks/`). Every model in the module was then re-implemented independently and run (`m11/verify.py`, `m11/branch.py`, `m11/k1res.py`), and the two figures whose geometry contradicts their own text were regenerated (`m11/genfigs.py` → `figs.json`). **Every number in a replacement below was printed by one of those runs.**

## 1. Verdict

**Yes, after revision.** A graduate reader with no biomechanics can learn from these pages what a manipulator is and why one matrix runs the whole story: Propositions 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1 and 8.2 each carry a proof of matching weight, and the proofs are correct — I checked the determinant expansion, the Christoffel evaluation of $C$, the virtual-work argument, the pseudoinverse decomposition and the SVD statement of D5 line by line. The mathematics is the strongest part of the module.

What stops the reader is the arithmetic and the provenance. **Three of the four lab scripts print nothing**, so §10's claim that "every plotted number below was produced by these scripts" is false of Labs A, B and C; only Lab D prints (`manipulability=0.1350`, which matches). **Lab A labels the two inverse-kinematics branches backwards** — `elbow=+1` puts the elbow *below* the shoulder-to-hand line, and the variable named `down` holds the elbow-*up* branch — which then propagates into K6, whose stated elbow-down pose does not produce its stated 34.5 N. **§4 says the arm's own weight makes the cup torques "roughly double"; the module's own Appendix values make them 4.9× at the shoulder and 3.0× at the elbow.** **K8's slip time is wrong** (0.488 s, not 0.425 s) and its figure draws a grip curve that is $1.3\times$ the true load, so the figure shows no slip at all while marking one. **K10's figure clips its own curve**: the y-axis tops at 300 N while the solution reports 593 N and the polyline lies flat along the axis top from $\mu\approx0.63$ upward. **C6 states the slip floor as $L/\mu$** where Proposition 8.1 and Definition 5 both give $L/(2\mu)$. Three of the ten K solutions (K5, K7, K8) quote numbers from integrations whose pose, gains, step and horizon are never stated, so no reader can reproduce them; K7's triple is not a null vector of any pose the module defines. $\beta$ means two different things (the resultant angle in Proposition 7.1, the wrap angle in K10). About a dozen empirical numbers have no Appendix row.

None of this touches a proof. Every fix below is arithmetic, provenance, a label, or a table row.

## 2. Blocking defects

Ranked: wrong numbers and wrong statements first, then false provenance, then unreproducible results, then missing scaffolding.

### B1. §4 says the arm's own weight "roughly doubles" the cup torques; it multiplies them by 4.9 and 3.0

Location: `module11.html:173`.

Quoted: "Add the arm's own weight (Module 1's segment masses, restored in the inverse dynamics of Section 6) and these roughly double."

Factual error, and the one number in §4 that is neither derived nor checkable. Proposition 6.1's own gravity vector, evaluated at $\theta_1=\theta_2=0$ with the Appendix values $m_1=2.1$ kg, $\ell_{c1}=0.15$ m, $m_2=1.65$ kg, $\ell_{c2}=0.22$ m, $\ell_1=0.30$ m, gives $g_1=(m_1\ell_{c1}+m_2\ell_1)g+m_2\ell_{c2}g=7.95+3.56=11.51$ N m and $g_2=m_2\ell_{c2}g=3.56$ N m. Added to the cup's 2.94 and 1.77 N m: 14.45 N m at the shoulder (a factor 4.91) and 5.33 N m at the elbow (a factor 3.02). Printed by `verify.py`:

```
arm-weight gravity torques: g1=11.507  g2=3.561 N m
totals: shoulder 14.450 (x4.91)  elbow 5.327 (x3.02)
```

Replacement for the sentence:

```html
Add the arm's own weight and these grow by much more than the cup alone suggests: the gravity vector of <a class="secref" href="#dynamics">Section 6</a>, evaluated at this posture with the Appendix segment values, contributes $(m_1\ell_{c1}+m_2\ell_1)g+m_2\ell_{c2}g=7.95+3.56=11.51\ \mathrm{N\,m}$ at the shoulder and $m_2\ell_{c2}g=3.56\ \mathrm{N\,m}$ at the elbow, so the totals are $14.45$ and $5.33\ \mathrm{N\,m}$ - the cup's torque multiplied by $4.9$ and $3.0$. The limb is the load; the mug is the surcharge.
```

### B2. Lab A's inverse-kinematics code labels the two elbow branches backwards

Location: `module11.html:292` (docstring), `:303-309` (variables and plot), `:315` (caption), `:317` (interpretation).

Quoted (line 292): `"""Inverse kinematics; elbow=+1 up, -1 down. Returns (th1, th2)."""`
Quoted (line 303): `down = np.array([ik(px, py, elbow=-1) for px, py in path])`

Wrong statement. With Definition 1's convention (forearm absolute angle $\theta_1+\theta_2$, $y$ up), $\theta_2>0$ puts the elbow *below* the straight line from shoulder to hand. At the goal $(0.45,0.10)$, `elbow=+1` gives $\theta_1=-56.3^\circ,\ \theta_2=+107.2^\circ$ with the elbow at $y=-0.250$ m (below the line); `elbow=-1` gives $\theta_1=+81.3^\circ,\ \theta_2=-107.2^\circ$ with the elbow at $y=+0.297$ m (above it). Printed by `branch.py`:

```
tgt=(0.45, 0.1) elbow=+1  th1= -56.28 th2=  107.24  elbow_y=-0.250 (hand-line side BELOW)
tgt=(0.45, 0.1) elbow=-1  th1=  81.33 th2= -107.24  elbow_y=+0.297 (hand-line side ABOVE)
```

So the docstring is inverted and the array named `down` holds the elbow-up branch. The plotted figure is the elbow-up branch: decoding the right-hand panel of the figure at `:315` (ticks $-140,-70,0,70$ at $y=250,197.5,145,92.5$, so $\text{deg}=(145-y)/0.75$), the elbow curve starts at $y=246.6$, i.e. $-135.5^\circ$, and the shoulder curve at $y=128.3$, i.e. $+22.3^\circ$ — exactly the `elbow=-1` values at the start point $(0.10,-0.30)$. The caption's $63^\circ$ and $37^\circ$ are correct **for that branch**; on the elbow-down branch the shoulder sweep is $109.1^\circ$. The §3 figure at `:152` is not affected — its solid arm's elbow is genuinely below the line and its labels are right.

Replacement for the code block body at `:285-313` (the docstring is corrected, the variables carry the branch they hold, the plotted branch is named, and the sweeps are printed so the caption's numbers are output rather than assertion):

```html
<pre><code>import numpy as np
import matplotlib.pyplot as plt

l1, l2 = 0.30, 0.45              # upper arm, forearm+hand (m)


def ik(x, y, elbow=+1):
    """Inverse kinematics. elbow=+1 puts the elbow BELOW the straight
    shoulder-to-hand line (elbow-down); -1 puts it above (elbow-up).
    Returns (th1, th2)."""
    c2 = (x*x + y*y - l1**2 - l2**2)/(2*l1*l2)
    th2 = elbow*np.arccos(np.clip(c2, -1.0, 1.0))
    th1 = np.arctan2(y, x) - np.arctan2(l2*np.sin(th2),
                                        l1 + l2*np.cos(th2))
    return th1, th2


start, goal = np.array([0.10, -0.30]), np.array([0.45, 0.10])
s = np.linspace(0.0, 1.0, 60)
path = (1 - s)[:, None]*start + s[:, None]*goal
down = np.array([ik(px, py, elbow=+1) for px, py in path])
up = np.array([ik(px, py, elbow=-1) for px, py in path])

for name, q in (('elbow-up', up), ('elbow-down', down)):
    print('%s: shoulder sweep %.1f deg, elbow sweep %.1f deg'
          % (name, np.degrees(np.ptp(q[:, 0])),
             np.degrees(np.ptp(q[:, 1]))))

fig, ax = plt.subplots(1, 2, figsize=(9, 4))
ax[0].plot(path[:, 0], path[:, 1], 'k--', label='hand path')
ax[1].plot(s, np.degrees(up[:, 0]), label='shoulder th1')
ax[1].plot(s, np.degrees(up[:, 1]), label='elbow th2')
for a in ax:
    a.legend()
plt.tight_layout()
plt.show()</code></pre>
```

Output:

```
elbow-up: shoulder sweep 62.8 deg, elbow sweep 36.6 deg
elbow-down: shoulder sweep 109.1 deg, elbow sweep 36.6 deg
```

Replacement caption (`:315`), naming the branch drawn:

```html
<figcaption>Lab A, elbow-up branch. The hand travels a straight line from lap to cup (left, dashed), but the joint angles trace curved, non-uniform paths (right): the shoulder sweeps 62.8&#176; and the elbow 36.6&#176;, neither at constant rate, because the Jacobian changes with posture. The nonlinearity of the forward map, made visible.</figcaption>
```

Replacement for the first two sentences of the Interpretation (`:317`), which also uses the branch comparison the print now supplies:

```html
<b>Interpretation.</b> The hand tracks a straight line, but the joint angles trace <em>curved</em>, non-uniform trajectories - the nonlinearity of the forward map made visible. On the elbow-up branch plotted here the shoulder rotates through $62.8^\circ$ and the elbow through $36.6^\circ$; on the elbow-down branch the elbow sweep is identical ($36.6^\circ$, since the two branches differ only in the sign of $\theta_2$) but the shoulder must sweep $109.1^\circ$ - the discrete choice of <a class="secref" href="#ik">Section 3</a> costing nearly twice the shoulder excursion. Neither joint moves at constant rate even though the hand does, because $J$ changes with posture.
```

### B3. Three of the four labs print nothing, so §10's provenance claim is false

Location: `module11.html:280`, and the code blocks at `:285`, `:322`, `:366`.

Quoted: "The code is written to run as-is on NumPy/Matplotlib; every plotted number below was produced by these scripts."

Running all four blocks produces one line of output in total, from Lab D. Labs A, B and C contain no `print`, so the caption numbers $63^\circ/37^\circ$, $4.7/3.5/8/19/22$ N m and $5/32$ N per pad are asserted, not produced. This is the defect class the domain brief names first. The fix is to make the claim true, not to withdraw it. B2 adds Lab A's print. Lab B gains, after the `tot, inert, grav = ...` line:

```python
print('peak: inertial %.2f, gravity %.2f, total %.2f N m'
      % (np.abs(inert).max(), np.abs(grav).max(), np.abs(tot).max()))
```

which prints `peak: inertial 4.66, gravity 3.45, total 8.11 N m`. Lab C gains, after `Fg_lift = ...`:

```python
for mu_i in (0.6, 0.2, 0.1):
    print('mu=%.1f: %.2f N per pad' % (mu_i, (1 + s)*m*g/(2*mu_i)))
```

which prints `mu=0.6: 5.31 N per pad`, `mu=0.2: 15.94 N per pad`, `mu=0.1: 31.88 N per pad`.

### B4. C6 quotes the wrong slip floor

Location: `module11.html:462`.

Quoted: "Grip force is normally set just above the slip floor $F_g^{\min}=L/\mu$".

Wrong statement, contradicting the module's own Proposition 8.1 ($F_g\ge W/(2\mu)$) and Definition 5 ($F_g^{\min}=L/(2\mu)$), and the figure at `:270` which labels the dashed line "slip floor L/2μ". The factor 2 is the whole content of the two-pad balance. Replacement for the opening clause:

```html
Grip force is normally set just above the slip floor $F_g^{\min}=L/(2\mu)$ of <a class="secref" href="#tactile">Definition 5</a> - two pads each supplying half the load - with a small safety margin,
```

### B5. K8's slip and reflex times do not follow from the model, and its figure shows no slip

Location: `module11.html:554` (figure), `:555` (solution).

Quoted: "the slip is detected at $t=0.425\ \mathrm{s}$ and the reflex, arriving $70\ \mathrm{ms}$ later at $t\approx0.495\ \mathrm{s}$".

Factual error. With the module's own lift pulse (Lab C: $a(t)=A\exp[-((t-0.6)/0.12)^2]$), $a_{\rm pred}=1.5$, $a_{\rm true}=9\ \mathrm{m/s^2}$ and $s=0.30$, the margin is $1.3\,(g+1.5p)/(g+9p)-1$. Its minimum is $-0.2183$ at $t=0.600$ s — which does reproduce the solution's "$22\%$ short (minimum margin $-0.22$)" — but it first crosses zero at $t=0.4878$ s, so the reflex lands at $0.5578$ s. Printed by `verify.py`:

```
min margin -0.2183 at t=0.6000 s
margin first negative at t=0.4879 s; reflex at 0.5579 s
```

The figure is worse than the number. Decoding its two polylines against its own axes ($y=165-7.5F$): the red curve runs 4.91 → 9.41 N, which is the true load $0.5(g+9p)$; the blue curve runs 6.37 → 12.23 N, which is $1.3\times$ the **true** load, not the feedforward grip $1.3\times0.5(g+1.5p)$ (peak 7.35 N). So the blue curve never dips below the red one: the figure draws a grip that never fails, while a marker on it claims a slip at 0.43 s, and the marker is not on either curve at that time. Regenerated with `genfigs.py` (same viewBox, same axis box, red = load, blue = feedforward grip capacity switching to $1.3\times$ the instantaneous load at $t_{\rm reflex}$, marker at the true crossing).

Replacement solution text:

```html
<details class="sol"><summary>Solution</summary><div>Take the lift pulse of Lab C, $a(t)=A\exp[-((t-0.6)/0.12)^2]$, with the true peak $A=9\ \mathrm{m/s^2}$ and an internal model predicting only $1.5\ \mathrm{m/s^2}$. The feedforward grip is set from the prediction, $F_g=(1+s)m(g+1.5\,a_{\rm shape})/(2\mu)$ with $s=0.30$, so the friction it can deliver is $2\mu F_g=(1+s)m(g+1.5\,a_{\rm shape})$ while the real load is $L(t)=m(g+9\,a_{\rm shape})$. The margin $2\mu F_g/L-1$ is independent of $\mu$ and of $m$: it is $1.3\,(g+1.5p)/(g+9p)-1$. It first goes negative at $t=0.488\ \mathrm{s}$ and bottoms at $-0.218$ at the acceleration peak $t=0.600\ \mathrm{s}$ - the grip falls $21.8\%$ short of what the load demands. The $70\ \mathrm{ms}$ reflex therefore lands at $t=0.558\ \mathrm{s}$, still on the rising flank, and re-sets the grip to $30\%$ above the <em>instantaneous</em> floor, taking it to $12.23\ \mathrm{N}$ against a load peak of $9.41\ \mathrm{N}$ and arresting the slip. The episode reproduces the everyday "heavier than I thought" jolt and shows the tactile loop as a delayed-feedback catch on a feedforward error - the fingertip instance of Module 10's delayed balance loop. Note what the delay costs: the hand slides for $70\ \mathrm{ms}$ before the correction exists, which is why a badly mispredicted object is felt to slip before it is caught.</div></details>
```

### B6. K6's stated pose is not the pose that gives its number

Location: `module11.html:545` (statement), `:547` (solution).

Quoted (statement): "At the pose reaching $(0.45,0.10)\ \mathrm{m}$ (elbow-down)".
Quoted (solution): "$F_y^{\max}=15(|(J^{-\mathsf T})_{21}|+|(J^{-\mathsf T})_{22}|)=34.5\ \mathrm{N}$ … about $7\times$ the weight of the $0.5\ \mathrm{kg}$ cup".

34.5 N is right — for the **elbow-up** pose. `branch.py` gives $(J^{-\mathsf T})_{2,:}=(1.5246,\,0.7756)$ at $\theta_1=81.3^\circ,\theta_2=-107.2^\circ$, so $15(1.5246+0.7756)=34.50$ N $=7.03\times$ the cup's 4.91 N. The genuine elbow-down pose gives 52.29 N. The figure at `:546` prints "max F_y = 34.5 N", so the cheap and correct repair is the pose label, not the number. Replacement for the statement's parenthesis: `(0.45,0.10)\ \mathrm{m}$ (elbow-up, the branch Lab A plots)`.

### B7. K6's closing claim is false at the pose it names

Location: `module11.html:547`.

Quoted: "at a near-straight bracing pose the same torque box would yield far more vertical force still, because $J^{-\mathsf T}$ blows up toward the singularity".

Wrong statement. Near the boundary singularity $J^{-\mathsf T}$ blows up **along the arm**, not vertically; at a near-horizontal reach the vertical direction is the one that stays weak. On the same elbow-up branch, moving the goal from $(0.45,0.10)$ to $(0.73,0.10)$ takes $F_y^{\max}$ from 34.5 N to 31.9 N — *down* — while $F_x^{\max}$ goes from 99.4 N to 350.5 N. Printed by `verify.py`:

```
J^-T row2 =  [1.5246 0.7756]
Fy_max = 34.50 N   = 7.03 x weight of 0.5 kg cup
Fx_max = 99.44 N
 near-straight goal x=0.700: Fy_max=27.7 N  Fx_max=199.0 N
 near-straight goal x=0.730: Fy_max=31.9 N  Fx_max=350.5 N
```

Replacement for the closing clause:

```html
This is about $7\times$ the weight of the $0.5\ \mathrm{kg}$ cup - ample. Straightening the arm does <em>not</em> raise it: pushing the goal out to $(0.73,0.10)\ \mathrm{m}$ leaves $F_y^{\max}=31.9\ \mathrm{N}$, slightly <em>lower</em>. What the singularity amplifies is force <em>along</em> the arm, and only that: over the same move $F_x^{\max}$ rises from $99.4$ to $350.5\ \mathrm{N}$, because $J^{-\mathsf T}$ diverges in the one direction the hand cannot move (<a class="secref" href="#ik">Section 3</a>). That is C3's bracing intuition made exact, and it also says what bracing cannot do: a straight arm is a strut, not a jack.
```

### B8. K10's figure clips its own curve at the axis top

Location: `module11.html:562`.

The plot's $y$ axis runs 0 to 300 N ($y=165-0.4W$) while the solution reports a power-grip capacity of 593 N at $\mu=0.8$ and the swept range reaches $\mu=0.85$, where the model gives 736.7 N. The drawn polyline is clamped at $y=45.0$ (the axis top) over roughly the last third of the sweep, so the figure reads "300 N" where the text says 593 N — a figure disagreeing with its caption's number, which the domain brief classes as a factual error. Regenerated with `genfigs.py`: same axis box, $y=165-0.15W$, tick labels 0 / 400 / 800, both polylines recomputed, and the two curve labels moved off the curves ("power ∝ e^{μβ}" to the empty upper right, "pinch (∝ μ)" to the empty left, since the pinch curve now lies close to the axis). `check_overlap.py` verifies the placement.

### B9. K7's numbers are unreproducible and it calls the wrong angle the elbow angle

Location: `module11.html:550` (figure labels), `:551` (solution).

Quoted: "moves the three joints by $(+10.0,-24.5,+21.8)^\circ$ and swings the elbow angle $\theta_1+\theta_2$ by $-14.5^\circ$, while the fingertip drifts by only $4.4\times10^{-5}\ \mathrm{m}$".

Two defects. (a) No pose, step size or horizon is given, and the quoted triple is not proportional to the null vector of any pose the module defines: at the three-link pose K5 uses, $\mathbf q_0=(0.4,1.90,0.3)$ rad with $\ell_i=0.25$ m, the unit null vector is $(0.1411,-0.5272,0.8379)$, whose direction is $(10.0,-37.4,59.4)$ when scaled to a $10^\circ$ first component, not $(10.0,-24.5,21.8)$. (b) By Definition 1 the elbow angle *is* $\theta_2$; $\theta_1+\theta_2$ is the forearm's absolute orientation. Restated with the parameters written down, integrating $\dot{\mathbf q}=\mathbf n$ for 1.0 s at $\Delta t=1$ ms from the K5 pose (`branch.py`):

```
K7 1.0 s horizon, dt=1 ms, unit null vector: [ 0.1411 -0.5272  0.8379]
  joint change (deg): [ 15.4 -34.   43.2]
  th2 (elbow joint) change: -34.0 deg
  fingertip drift 3.14e-05 m
```

Replacement solution:

```html
<details class="sol"><summary>Solution</summary><div>Take the same three-link arm as K5 ($\ell_i=0.25\ \mathrm{m}$) at $\mathbf q_0=(0.4,\ 1.90,\ 0.3)\ \mathrm{rad}$. Its $2\times3$ Jacobian has full row rank, so its SVD has one zero singular value and the matching right-singular vector is the unit null vector $\mathbf n=(0.1411,-0.5272,0.8379)$. Integrating $\dot{\mathbf q}=\mathbf n$ (re-evaluating $\mathbf n$ each step, sign-continued) for $1.0\ \mathrm{s}$ at $\Delta t=1\ \mathrm{ms}$ moves the joints by $(+15.4,-34.0,+43.2)^\circ$: the elbow joint angle $\theta_2$ alone swings $34^\circ$, a visible reconfiguration. Over that whole excursion the fingertip drifts $3.1\times10^{-5}\ \mathrm{m}$ - thirty microns, and falling with $\Delta t$, so it is the truncation residual of the finite step and not a real motion. This is C9's pinned-fingertip freedom measured: the joints traverse a one-parameter family of postures with the endpoint held fixed, the internal motion the nervous system exploits for comfort and obstacle avoidance.</div></details>
```

The two figure labels at `:550` change with it: "drift 4×10⁻⁵ m" → "drift 3×10⁻⁵ m", and "elbow angle Δ = −14.5°" → "elbow Δθ₂ = −34°".

### B10. K5's start does not match its own statement, and its run is unreproducible

Location: `module11.html:541` (statement), `:543` (solution).

Quoted (statement): "with the elbow near a soft limit at $2.0\ \mathrm{rad}$".
Quoted (solution): "drives the elbow from $1.90$ to $1.005\ \mathrm{rad}$ … the fingertip position error stays at $1.3\times10^{-9}\ \mathrm{m}$".

The elbow starts at 1.90 rad, not 2.0, and the figure at `:542` says so ("elbow 1.90 → 1.00 rad"); the statement should place the soft limit at 2.0 and the start just inside it. The gains, step and horizon are never given, so $1.3\times10^{-9}$ m is a number no reader can obtain; my run of the same scheme ($k_e=50\ \mathrm{s^{-1}}$, $k_H=3\ \mathrm{s^{-1}}$, $\Delta t=1$ ms, 4 s) gives $\theta_2:1.900\to1.005$ rad and a fingertip error of $6.1\times10^{-11}$ m. The destination and the qualitative claim survive; the parameters must be stated.

Replacement for the statement's second sentence: `A three-link arm ($\ell_i=0.25\ \mathrm{m}$) at $\mathbf q_0=(0.4,\ 1.90,\ 0.3)\ \mathrm{rad}$ holds its fingertip fixed with the elbow pressed toward a soft limit at $2.0\ \mathrm{rad}$.`

Replacement solution:

```html
<details class="sol"><summary>Solution</summary><div>Integrate $\dot{\mathbf q}=J^{+}(k_e\,\mathbf e)-(I-J^{+}J)\,k_H\nabla H$ with the comfort cost $H=\tfrac12(\theta_2-1.0)^2$, the fingertip error $\mathbf e=\mathbf p_0-\mathbf p(\mathbf q)$, gains $k_e=50\ \mathrm{s^{-1}}$ and $k_H=3\ \mathrm{s^{-1}}$, step $\Delta t=1\ \mathrm{ms}$, for $4\ \mathrm{s}$. The elbow runs from $1.900$ to $1.005\ \mathrm{rad}$ - off the limit and onto the comfortable target, the residual $0.005$ being the standoff where the null-space pull balances nothing but its own step - while the fingertip error stays at $6\times10^{-11}\ \mathrm{m}$, i.e. fixed to numerical precision. Note that the first term alone would not move the elbow at all: the task is already satisfied, $\mathbf e=\mathbf 0$, and it is the projector $(I-J^{+}J)$ that turns a comfort gradient into motion the task cannot see. The self-motion reconfigures the arm without disturbing the task, the continuous version of C2's discrete elbow choice, and the mechanism by which the nervous system keeps joints out of their painful extremes during sustained holds.</div></details>
```

### B11. K1's peak rates depend on a sample count the problem never states, and its comparison is wrong

Location: `module11.html:525` (statement), `:527` (solution).

Quoted: "the peak elbow rate is $2.55,4.37,8.79,16.0\ \mathrm{rad/s}$ - it more than doubles over the last $3\ \mathrm{cm}$".

The four numbers are correct, and they pin down an unstated choice: they reproduce **exactly** at 400 path samples and nowhere near it at Lab A's 60. From `k1res.py`:

```
N=   60 ['2.53', '4.31', '8.37', '13.94']  last/third 1.67
N=  400 ['2.55', '4.37', '8.79', '16.00']  last/third 1.82
N= 4000 ['2.55', '4.38', '8.87', '16.45']  last/third 1.85
```

That sensitivity is the point of the problem — near a singularity the finite-difference peak is resolution-limited, and a reader who takes Lab A's 60 samples gets 13.94 and concludes the module is wrong. State $N$. Separately, $16.00/8.79=1.82$: the rate does not "more than double". Replacement solution:

```html
<details class="sol"><summary>Solution</summary><div>Sample the straight path at $N=400$ points, solve IK at each, and central-difference $\theta_2$ against $t=0.6\,s/(N-1)$ per step. With goal $x$-coordinates $0.45,0.60,0.70,0.73\ \mathrm{m}$ (radii $r=0.461,0.608,0.707,0.737\ \mathrm{m}$) the peak elbow rate is $2.55,4.37,8.79,16.00\ \mathrm{rad/s}$: it grows by $1.82\times$ over the last $3\ \mathrm{cm}$ of approach and diverges as $r\to0.75\ \mathrm{m}$. The sample count matters and that is half the lesson: at $N=60$ the same sweep gives $2.53,4.31,8.37,13.94$ and at $N=4000$ it gives $2.55,4.38,8.87,16.45$. The first three values have converged; the fourth has not, because the true peak is unbounded and a finite difference can only resolve as much of it as the sampling allows. The mechanism is $\theta_2=\arccos(\cdot)$ acquiring an infinite slope at full extension: the same hand speed demands ever-larger joint speed. Reaching to the very edge of the workspace is not "a bit harder" but singular - which is why the body recruits trunk lean rather than truly straightening the arm to a target at its limit.</div></details>
```

### B12. $\beta$ means two different things

Location: `module11.html:230` and `:508` (the resultant angle $\beta=\arctan(F_t/F_c)$, and the figure text at `:507`), against `:561` and `:563` (the capstan wrap angle $\beta$).

A symbol collision, and the notation table records neither use. The capstan law is universally written $e^{\mu\beta}$ with $\beta$ the wrap angle, so the wrap angle keeps $\beta$ and the local resultant angle of Proposition 7.1 becomes $\psi$. Three prose occurrences (`:230` twice plus once, `:508` twice) and two SVG `<text>` bodies at `:507` ("resultant β" and "seated iff β ≤ α ⟹ …") change; both new symbols go into the notation table (B15).

### B13. §10 and §11 claim a provenance the K solutions do not have

Location: `module11.html:436`, `:523`, `:643`.

Quoted (`:436`): "The computational solutions quote numbers produced by the same code as the labs; running them is the point."
Quoted (`:643`): "every proposition proved, every figure computed, every number reproduced by the code shown."

False. Six of the ten K solutions run models no lab contains: K1's goal sweep, K5's and K7's three-link null-space integrations, K6's force polytope, K8's slip event, K9's ratio sweep. The labs' four scripts cannot produce them. After B2, B3, B5, B9, B10 and B11 every K solution states the model, the parameters and the scheme it was run with, which is what makes a number checkable; the sentences must say that instead. Replacements:

`:436`: `Thirty problems - ten conceptual, ten derivational, ten computational - plus five quick diagnostics. Each carries a <em>Probes</em> note (what it tests, which section) and a collapsible worked solution. Each computational solution states the model, the parameters and the numerical scheme it was run with, so every number in it can be reproduced from the propositions of Sections 1 to 9; six of them run models the labs do not contain.`

`:523`: `Each computational problem requires simulation, optimisation, an inverse solve, a sensitivity sweep, or a regime comparison - not substitution into a boxed formula. Every quoted number is one a run of the stated model produces; where the answer depends on a discretisation, the discretisation is stated.`

`:643`: `... every proposition proved, every figure computed, and every quoted number reproduced by running the model the text states.`

### B14. Proposition 7.1 does not say it assumes a frictionless socket

Location: `module11.html:226-230`.

The proof resolves $F_c$ and $F_t$ against a contact reaction directed along the socket normal — that is the frictionless assumption, and it is load-bearing: with friction the head stays seated past the rim angle. Section 8 then introduces $\mu$ two sections later without ever saying that §7 set it to zero. Failing part 4 of the standard (the limit case). Add to the proposition statement after "by a compressive force $F_c$ directed into the socket": `Take the socket surface frictionless, so the contact reaction is normal to it; cartilage-on-cartilage friction ($\mu\approx0.005$, Module 4) is small enough that this changes the boundary by well under a degree.` And add one sentence to the end of the paragraph at `:232`: `The frictionless idealisation is conservative: any friction at the contact widens the seated cone slightly, so $\tan\alpha$ is a lower bound on the true stability ratio.`

### B15. Empirical numbers with no Appendix row, and symbols with no notation row

Locations: `:222` (glenoid "about a third of the humeral head"; labrum "deepens the socket by roughly half"), `:234` ("$2\!:\!1$" scapulohumeral rhythm), `:465` figure ("hip: deep, tan α ≈ 1.9"), `:364`/`:377` and `:533` (the lift friction $\mu=0.6$), `:545` (the $15\ \mathrm{N\,m}$ torque bound), `:561` (the $30\ \mathrm{N}$ maximum squeeze), `:320` ($A$, $f$, $\theta_2^0$, $\theta_1$ of the wave).

Each is a bare number: not derived, not in a table with symbol and unit, not labelled an assumption. Seven parameter rows to add after `:636`:

```html
<tr><td>Glenoid coverage of the humeral head</td><td>-</td><td>$\approx1/3$ of the head's articular area</td><td><a class="secref" href="#shoulder">&#167;7</a></td></tr>
<tr><td>Labral deepening of the socket</td><td>-</td><td>$\approx+50\%$ effective depth</td><td><a class="secref" href="#shoulder">&#167;7</a></td></tr>
<tr><td>Scapulohumeral rhythm</td><td>-</td><td>$2\!:\!1$ glenohumeral : scapular rotation</td><td><a class="secref" href="#shoulder">&#167;7</a></td></tr>
<tr><td>Acetabular effective half-arc (for contrast)</td><td>$\alpha_{\rm hip}$</td><td>$\approx62^\circ$ (ratio $\tan\alpha\approx1.9$)</td><td><a class="secref" href="#shoulder">&#167;7</a>, C7</td></tr>
<tr><td>Skin-glass friction during a lift (assumed)</td><td>$\mu$</td><td>$0.6$</td><td>Lab C, K3, K8</td></tr>
<tr><td>Joint-torque ceiling (assumed)</td><td>$\tau_{\max}$</td><td>$15\ \mathrm{N\,m}$ per joint</td><td>K6</td></tr>
<tr><td>Maximum voluntary squeeze (assumed)</td><td>$F_g^{\max}$</td><td>$30\ \mathrm{N}$ per pad</td><td>K10</td></tr>
<tr><td>Wave kinematics (assumed)</td><td>$A,f,\theta_2^0,\theta_1$</td><td>$0.5\ \mathrm{rad}$, $1.5\ \mathrm{Hz}$, $-1.0\ \mathrm{rad}$, $100^\circ$</td><td><a class="secref" href="#dynamics">&#167;6</a>, Lab B, K2</td></tr>
```

Five notation rows to add after `:620`:

```html
<tr><td>$\psi$</td><td>angle of the resultant contact force from the socket axis, $\arctan(F_t/F_c)$</td><td><a class="secref" href="#shoulder">&#167;7</a></td></tr>
<tr><td>$\hat{\mathbf n}$; $\gamma$</td><td>outward contact normal; angle from a contact normal to the line joining the two contacts</td><td><a class="secref" href="#grip">&#167;8</a></td></tr>
<tr><td>$\beta$</td><td>capstan wrap angle of a power grip</td><td>K10</td></tr>
<tr><td>$\mathbf z$; $H(\mathbf q)$</td><td>free null-space parameter; secondary cost minimised inside the null space</td><td><a class="secref" href="#redundancy">&#167;5</a></td></tr>
<tr><td>$\sigma_1,\sigma_2$; $\ell_{\rm tot}$</td><td>singular values of $J$; total arm length $\ell_1+\ell_2$</td><td>D5, K9</td></tr>
```

### B16. The Appendix cites de Leva while two figure captions cite Winter, and the masses differ from Module 1's reference human without a word

Location: `module11.html:624`, against `:90` and `:315`'s aria-label ("Winter-proportion arm reach", "Winter segment lengths") and Module 1's Appendix.

Module 1 fixes the reference human at 70 kg with forearm+hand mass $0.022M=1.54$ kg. Module 11 uses $m_2=1.65$ kg and $m_1=2.1$ kg with no note. The domain brief requires a reused scenario to keep the earlier values or say why it differs. Replacement for `:624`:

```html
<p class="small">Representative adult values used throughout the worked numbers and labs. Lengths follow the Winter segment proportions used for the figures; masses and inertias follow de Leva's anthropometry, which is why $m_2=1.65\ \mathrm{kg}$ here against the $0.022M=1.54\ \mathrm{kg}$ that Module 1's Winter table gives for the same forearm-plus-hand at $M=70\ \mathrm{kg}$ - a $7\%$ difference that moves no conclusion in this module, since every result scales linearly in $m_2$. Contact values are assumed, at the order of magnitude the fingertip-friction literature reports; that literature is not in the repository and the values are unverified here.</p>
```

### B17. The module never places its models on the level ladder

Location: `module11.html:96` (the thesis box).

Required by the domain brief and absent. Add as the last sentence of the thesis box:

```html
On the course's level ladder these models sit at Level 2 to Level 4 - planar rigid-body kinematics (<a class="secref" href="#chain">Section 1</a>), a multibody link chain (<a class="secref" href="#redundancy">Section 5</a>), and inverse kinematics and inverse dynamics (<a class="secref" href="#ik">Sections 3</a> and <a class="secref" href="#dynamics">6</a>) - except the grasp, which is Level 6, a contact and friction model. Nothing here is Level 5 or above: the torques arrive as inputs, not from muscles (Module 5), and no controller chooses the trajectory (Module 12).
```

### B18. C1's sign convention contradicts Proposition 4.1's

Location: `module11.html:442`.

Quoted: "The tray applies a downward force $\mathbf F=(0,-mg)$ at the hand … The joint torques needed to hold it are $\boldsymbol\tau=J^{\mathsf T}\mathbf F$".

Proposition 4.1 defines $\mathbf F$ as the force the **hand applies to the environment**, and §4's own worked cup uses $\mathbf F=(0,+mg)$. C1 substitutes the force the tray applies to the hand into the same formula, which flips the sign of both torques. The magnitudes it then quotes are right, so the defect is the contract, not the answer. Replacement for the opening sentence:

```html
The hand must push up on the tray with $\mathbf F=(0,+mg)$ whatever the posture (Proposition 4.1's $\mathbf F$ is the force the hand applies to the world; the tray pushes back down with $-\mathbf F$).
```

### B19. Lab C's caption and interpretation overstate the grip force at the sweep's end

Location: `module11.html:389` (caption), `:391` (interpretation).

Quoted: "past 32 N as μ → 0.1" / "it climbs past $32\ \mathrm{N}$".

The swept minimum is $\mu=0.1$ exactly and $F_g=(1.3)(0.5)(9.81)/(2\times0.1)=31.88$ N, which K3 correctly reports as 31.9 N. The curve never reaches 32 N on the domain plotted. Replace both with "to $31.9\ \mathrm{N}$ at $\mu=0.1$".

## 3. Style and clarity edits

Apply in one pass.

1. `:102` "the hydrogen atom of manipulation" — a metaphor the module never cashes out. Replace with "the smallest model in which every phenomenon of this module already appears".
2. `:116` delete "innocent-looking".
3. `:162` delete "remarkably".
4. `:169` and `:140` state the ninety-degree ellipsoid duality in nearly identical 40-word clauses two sections apart, and D5 proves it a third time. Trim `:140` to "The transpose of this same matrix, in Section 4, turns this ellipsoid of easy velocities into an ellipsoid of easy forces with the axis lengths reciprocated; D5 proves the exchange."
5. `:195` delete "simply" ("Here we mark that the freedom exists").
6. `:274` "exquisitely sensitive" → "sensitive".
7. `:276` "a hugely inflated margin" → "a much larger margin"; delete "quietly".
8. `:462` "a hugely inflated margin" → "a margin several times larger".
9. `:222` "friction-free geometry alone resists a sideways dislocating force" → "the socket geometry alone resists a sideways dislocating force, with no friction needed" (and B14 states the assumption formally).
10. `:466` and the figure at `:465` say "$\tan\alpha\approx0.5$" where §7 and the parameter table say 0.47. Use 0.47 in the prose; the figure's rounded "≈ 0.5" stays as a figure label but gains the hip's $\alpha$ in the table (B15).
11. `:332-340` Lab B computes `c2` and never uses it, takes `dth2` and never uses it, and computes the Coriolis coefficient `h` only to multiply it by the literal `0.0`. Change the signature to `tau(th1, th2, dth1, ddth2)`, drop `c2`, write the Coriolis term honestly as `cor = h*dth1**2  # zero here: the shoulder is held still`, and call it with `dth1 = 0.0`. The now-unused `dth2 = A*w*np.cos(w*t)` line goes with it.
12. `:189` the proof asserts that $I-J^{+}J$ is the orthogonal projector onto $\mathcal N(J)$. One clause closes it: "(it is symmetric and idempotent, since $J^{+}J$ is, and its range is exactly $\mathcal N(J)$ because $J(I-J^{+}J)=0$ while $(I-J^{+}J)\mathbf r=\mathbf r$ for every $\mathbf r\in\mathcal N(J)$)".
13. `:568` the second diagnostic answers "the sign of $\det J$ encodes the handedness of the mapping" without saying what handedness is. Replace with: "$\det J>0$ means a positive turn of the joints sends the hand counter-clockwise around the elbow-down configuration, $\det J<0$ clockwise; the two IK branches of Proposition 3.1 carry opposite signs, and at $\theta_2=0$ they merge, $J$ drops rank, and the sign flips as the arm passes through the straight configuration."
14. `:563` "pinch $12\ \mathrm{N}$ versus power $22\ \mathrm{N}$" → $22.5\ \mathrm{N}$ (the model gives 22.49). And K10 states no limit case: add "The capstan law assumes an inextensible band wrapped on a rigid cylinder, so the $593\ \mathrm{N}$ at $\mu=0.8$ is the geometry's ceiling, not the hand's: long before it, the finger pads crush, the wrap slips off the ends, and the flexor tendons reach their own force limits (Module 5). Read the exponential as the reason a wrap beats a pinch, not as a number the hand can collect."
15. `:559` "The human upper arm and forearm-plus-hand are not far from equal" — the ratio is $0.45/0.30=1.5$, which is not near 1. Replace with the computed statement: "The human ratio is $1.5$, not $1$, and the cost of that is small: at $r=0.6\,\ell_{\rm tot}$ it gives $w=0.127\ \mathrm{m^2}$, $94\%$ of the optimum. Dexterity is one pressure among several (reach, strength, packing), and it is a weak one here - which is why it cannot by itself explain the proportion."

## 4. Structural notes

- **Dependencies point backwards throughout.** Every object used is built before use: $J$ before $J^{\mathsf T}$, $J^{\mathsf T}$ before the null-space projector, the friction cone before force closure, Proposition 8.1 before Definition 5's margin. The only forward references are to Modules 10 and 12, and each is marked as a repayment rather than an assumption.
- **The problem set passes the depth standard.** All ten K problems require a sweep, an optimisation, an integration, an inverse solve or a regime comparison; none is substitution into a boxed formula. K4 and K9 are the two closest to closed form, and both earn their place — K4 because the interesting part is the width of the peak, K9 because the answer (equal links) is a constrained optimum, not an evaluation.
- **The labs are the weak half of the module.** Each is 25 lines that plot and, after B3, print three numbers. Lab B in particular solves only $\tau_2$ with $\dot\theta_1=\ddot\theta_1=0$, so the module's own $M_{12}$ coupling — which the prose calls out twice as the interesting term — is never computed. The lab's "Extension" says so honestly, which is why this is a note and not a defect, but a five-line addition integrating the full $M\ddot{\mathbf q}+C\dot{\mathbf q}+\mathbf g$ would make §6 pay for its algebra.
- **§7 is the only section without a computed figure**, and the only one whose central number ($\alpha\approx25^\circ$) rests entirely on an unverifiable citation. It is honest about that after B15's table rows, but it is worth knowing that §7's stability ratio is the module's least anchored result.
- **The captures-and-misses table and the repayment ledger are model examples of the form** — five rows each, every borrowed idealisation matched to the module that discharges it, no row without a named mechanism.
- **No new toy body is introduced.** The reference human, the cup, and the two-link arm all come from Module 1; K5 and K7's three-link arm is the same arm with the wrist added, at a stated length.

## 5. What already works

- **Proposition 6.1 and its proof** (`:203-210`) are the best passage in the module: the kinetic energy is written out, $M$ is read off the quadratic form, the Christoffel symbols are evaluated rather than cited, and one entry ($C_{11}$) is computed in full so the reader can reproduce the rest. That is exactly the "smallest setting that shows the mechanism".
- **Proposition 2.1's determinant expansion** (`:134`) writes every cancelling term and names the identity that closes it. D2 then asks the reader to reproduce it.
- **Proposition 8.2** (`:256-258`) is the module's hardest result and it is proved properly — the positive-span condition on $\mathbb R^3$ is stated, the four edge-wrenches are counted, and the failure direction is identified when $\gamma\ge\varphi$. Most texts assert force closure with a picture.
- **Proposition 4.1's virtual-work proof** (`:167`) is four lines and complete, and it pauses to say why it writes $\delta U$ rather than $W$ — a notation collision caught before it happened.
- **Every number I could check against a model reproduces**: Lab B's 4.66 / 3.45 / 8.11 N m and the 3 Hz values 18.63 / 22.08; K2's crossover 1.3117 Hz; K3's 5.31 / 15.94 / 31.88 N; K4's $r=0.5408$ m, $w=0.135\ \mathrm{m^2}$, $\theta_2\in[71.8^\circ,108.2^\circ]$, $r\in[0.456,0.614]$ m, 15.8 cm band; K9's optimum at ratio 1.0 with $w=0.135$; all nine of K10's capstan numbers; §7's $\tan25^\circ=0.4663$; §8's 4.91 and 12.26 N; §1's annulus 0.75 / 0.15 m; §4's 2.94 and 1.77 N m; K1's four peak rates (at $N=400$); K5's 1.005 rad; K8's $-0.218$ minimum margin. That is 34 of 40 numbers checked correct before revision.
- **Pillar 1 holds.** Humerus, glenoid, labrum, rotator cuff, scapula, trapeziometacarpal joint, Meissner and Pacinian corpuscles, concavity-compression, scapulohumeral rhythm and force closure are each glossed in the sentence of first use.
- **The C set is genuinely conceptual** — every one of the ten asks for a mechanism in words and every solution supplies the equation behind it, without a single "it is well known".

## 6. Counts

- Blocking defects: 19 (B1 to B19).
- Style and clarity edits: 15.
- Numbers checked against a re-implementation: 40. Wrong: 6 (§4's "roughly double"; K8's 0.425 s and 0.495 s; K1's "more than doubles"; Lab C's "past 32 N"; K6's 34.5 N attributed to the wrong branch; K7's joint triple and drift).
- Figures regenerated: 2 (K8, K10). Figure text labels edited without regeneration: 3 figures (D7's $\beta\to\psi$, K7's two labels, Lab A's caption).
- Code blocks: 4 of 4 run clean, 0 `NameError`, 0 live HTML tags; 3 of 4 printed nothing before revision.

## 7. Changes applied

Applied to `edited/module11.html` by `m11/apply.py`: one re-runnable script, 60 `rep()` calls, each asserting its anchor occurs exactly once, run against a pristine copy. Figures from `m11/genfigs.py` to `figs.json`. Line numbers are the **original** `module11.html`.

| tag | line (original) | what changed | how verified |
|---|---|---|---|
| B1 | 173 | "these roughly double" replaced by the computed arm-weight gravity torques 11.51 and 3.56 N m and the totals 14.45 and 5.33 N m, i.e. the cup's torque times 4.91 and 3.02 | `verify.py`, evaluating Proposition 6.1's own gravity vector at the stated posture with the Appendix segment values |
| B2a | 292 | Lab A `ik` docstring "elbow=+1 up, -1 down" corrected to "+1 puts the elbow BELOW the shoulder-to-hand line (elbow-down); -1 above (elbow-up)" | `branch.py` prints the elbow's height and its side of the shoulder-to-hand line for both signs at four targets |
| B2b | 303-304 | `down` and `up` swapped so each holds the branch it names; a print of both branches' joint sweeps added | run: `elbow-up: shoulder sweep 62.8 deg, elbow sweep 36.6 deg` and `elbow-down: shoulder sweep 109.1 deg, elbow sweep 36.6 deg` |
| B2c | 308-309 | the right-hand panel now plots `up`, the branch the shipped SVG actually draws | decoded the figure's own polylines: the elbow curve starts at -135.5 deg and the shoulder at +22.3 deg, the `elbow=-1` values at the start point |
| B2d | 315 | Lab A caption names the branch and quotes 62.8 deg / 36.6 deg instead of "~63" / "~37" | printed by the edited block, above |
| B2e | 317 | interpretation gains the elbow-down comparison: identical 36.6 deg elbow sweep, 109.1 deg shoulder sweep | printed by the edited block, above |
| B3a | 280 | "every plotted number below was produced by these scripts" replaced by "each script prints the numbers its caption and interpretation quote" | all four blocks extracted and run after the edit; three printed nothing before it |
| B3b | 349 | Lab B gains a print of the inertial, gravitational and total elbow-torque peaks | run: `peak: inertial 4.66, gravity 3.45, total 8.11 N m`, matching the caption's 4.7 / 3.5 / 8 |
| B3c | 377 | Lab C gains a loop printing the grip floor at mu = 0.6, 0.2, 0.1 | run: `5.31`, `15.94`, `31.88` N per pad, matching K3 |
| B4 | 462 | C6's slip floor `L/mu` corrected to `L/(2 mu)`, with the two-pad reason and a pointer to Definition 5 | Proposition 8.1 and Definition 5 in the same module; the Fig. 9 label already reads "slip floor L/2mu" |
| B5a | 555 | K8's slip time 0.425 s to 0.488 s and reflex 0.495 s to 0.558 s; the margin expression and its independence of mu and m written out; post-reflex grip 12.23 N against the 9.41 N load peak added | `verify.py`: `margin first negative at t=0.4879 s; reflex at 0.5579 s`, `min margin -0.2183 at t=0.6000 s` |
| B5b | 554 | K8 figure regenerated: blue is now the feedforward grip capacity, which dips below the load and steps up at the reflex, and the marker sits on the real crossing | `genfigs.py`; the old blue polyline decoded to 1.3x the TRUE load (6.37 to 12.23 N), so it never crossed the load and the figure showed no slip |
| B6 | 545 | K6's pose label "(elbow-down)" changed to "(elbow-up, the branch Lab A plots)" | `branch.py`: elbow-up gives Fy_max = 34.50 N, the stated and drawn number; elbow-down gives 52.29 N |
| B7 | 547 | K6's closing claim that a near-straight pose yields more vertical force replaced by the computed truth: Fy_max falls to 31.9 N while Fx_max rises 99.4 to 350.5 N | `verify.py` sweep at goals x = 0.45, 0.70, 0.73 on the same branch |
| B8a-b | 562 | K10's two polylines recomputed on a 0-800 N axis so the power curve is no longer clamped at the axis top | `genfigs.py`: the model gives 736.7 N at mu = 0.85; the old mapping pinned it at y = 45.0, the axis top, from mu about 0.63 upward |
| B8c-d | 562 | K10 y-tick labels 150 to 400 and 300 to 800 | same rescale |
| B8e-f | 562 | K10 curve labels moved off the rescaled curves, with a short leader on the pinch label | `check_overlap.py` = 0; render at `m11/k10.png` inspected |
| B9a | 551 | K7 restated with its pose, step and horizon: joint change (+15.4, -34.0, +43.2) deg, elbow theta2 alone -34.0 deg, drift 3.1e-5 m; "the elbow angle theta1+theta2" corrected to theta2 | `branch.py`; the old triple (+10.0, -24.5, +21.8) is not parallel to the null vector (0.1411, -0.5272, 0.8379) of any pose the module defines |
| B9b-c | 550 | K7 figure labels "drift 4x10^-5 m" to "3x10^-5 m" and "elbow angle D = -14.5 deg" to "elbow dtheta2 = -34 deg" | same run |
| B10a | 541 | K5's statement now gives the start pose and puts the soft limit at 2.0 rad, matching its own figure label "elbow 1.90 -> 1.00 rad" | the figure text at line 542 |
| B10b | 543 | K5's gains, step and horizon written down; fingertip error 1.3e-9 m replaced by the computed 6e-11 m; a sentence added on why the task term alone moves nothing | `verify.py`: `elbow th2: 1.9000 -> 1.0054 rad`, `fingertip error 6.073e-11 m` |
| B11 | 527 | K1 now states N = 400 samples and central differencing, quotes 16.00, corrects "more than doubles" to 1.82x, and adds the N = 60 and N = 4000 values as the point of the problem | `k1res.py`: `N=400 ['2.55','4.37','8.79','16.00']`, `N=60 [... '13.94']`, `N=4000 [... '16.45']` |
| B12a-b | 230, 508 | Proposition 7.1's proof and D7's solution rename the resultant angle from beta to psi, freeing beta for K10's capstan wrap angle | symbol collision found by reading section 7 against K10; both symbols added to the notation table under B15b |
| B12c-d | 507 | the D7 figure's two text labels updated to psi | same |
| B13a | 436 | "The computational solutions quote numbers produced by the same code as the labs" replaced: each solution now states its model, parameters and scheme, and the sentence says six run models the labs do not contain | K1, K5, K6, K7, K8 and K9 run models absent from all four lab blocks |
| B13b | 523 | "Numbers quoted are those the code produces" replaced by a statement that the discretisation is stated wherever the answer depends on one | follows B11 |
| B13c | 643 | the footer's "every number reproduced by the code shown" changed to "every quoted number reproduced by running the model the text states" | same |
| B14a | 226 | Proposition 7.1 now states its frictionless-socket assumption, with Module 4's cartilage friction as the size of what is dropped | the proof resolves against a reaction normal to the socket; that is the assumption, and it was unstated |
| B14b | 232 | a limit-case sentence added: friction widens the seated cone, so tan alpha is a lower bound on the true ratio | same |
| B15a | 636 | eight parameter rows added: glenoid coverage 1/3, labral deepening +50%, 2:1 scapulohumeral rhythm, hip half-arc 62 deg, lift friction 0.6, torque ceiling 15 N m, maximum squeeze 30 N, and the wave kinematics | each was a bare empirical or assumed number in the text with no table row, which the domain brief classes as blocking |
| B15b | 620 | five notation rows added: psi; the contact normal and gamma; beta; z and H(q); the singular values and the total arm length | each symbol is used in section 5, 7, 8, D5, K9 or K10 and was absent from the table |
| B16 | 624 | the Appendix note now separates the length source (Winter, as the figure captions say) from the mass source (de Leva), and states the 1.65 vs 1.54 kg difference from Module 1's reference human and why it moves nothing | Module 1's Appendix against this module's m2; every result here is linear in m2 |
| B17 | 96 | the thesis box now places the module on the level ladder: Levels 2-4 for sections 1-6, Level 6 for the grasp, nothing at Level 5 or above | `prompt.txt` lines 286-296 |
| B18 | 442 | C1's sign convention brought into line with Proposition 4.1: F is the force the hand applies to the world | section 4's own worked cup uses +mg in the same formula where C1 used -mg |
| B19a-b | 389, 391 | Lab C's "past 32 N as mu goes to 0.1" changed to "31.9 N at mu = 0.1" in both caption and interpretation | the edited block prints `mu=0.1: 31.88 N per pad`; K3 already said 31.9 |
| S1 | 102 | "the hydrogen atom of manipulation" replaced by "the smallest model in which every phenomenon of this module already appears" | metaphor with no cash value; house rule |
| S2 | 116 | "this innocent-looking map" to "this map" | hedge deleted |
| S3 | 162 | "governed - remarkably - by the transpose" to "governed by the transpose" | hype deleted |
| S4 | 140 | the 40-word ninety-degree-duality clause trimmed to one sentence pointing at D5 | the same statement appears at 140, at 169 and again in D5's proof |
| S5 | 195 | "Here we simply mark" to "Here we mark" | hedge deleted |
| S6 | 274 | "exquisitely sensitive" to "sensitive" | hype deleted |
| S7a-b | 276 | "a hugely inflated margin" to "a much larger margin"; "quietly raising" to "raising" | hype deleted |
| S8 | 462 | "a hugely inflated margin" to "a margin several times larger" | hype deleted |
| S9 | 222 | "friction-free geometry alone resists" to "the socket geometry alone resists, with no friction needed" | pairs with B14a |
| S10 | 466 | C7's stability ratio 0.5 corrected to 0.47, matching section 7 and the parameter table | `verify.py`: `tan25deg = 0.4663` |
| S11a | 332-340 | Lab B's `tau` takes `dth1` instead of the unused `dth2`, drops the unused `c2`, and writes the Coriolis term as `h*dth1**2` with a comment instead of multiplying `h` by the literal 0.0 | `check_code.py` (pycodestyle) 0 issues; the block runs and prints the caption's numbers |
| S11b | 347 | the now-unused `dth2` line removed | same |
| S12 | 189 | Proposition 5.1's proof now proves, rather than asserts, that the projector is the orthogonal projector onto the null space | symmetric, idempotent, and a double range inclusion, written out |
| S13 | 568 | diagnostic 2 rewritten: the sign of det J is the IK branch, not an unexplained "handedness" | `branch.py`'s branch and sign table |
| S14a | 563 | K10's power-grip capacity at mu = 0.2 corrected from 22 N to 22.5 N | `verify.py`: `mu=0.2 pinch=12.0 N amp=1.874 power=22.5 N` |
| S14b | 563 | K10 gains its limit case: the capstan law assumes an inextensible band on a rigid cylinder, so 593 N is the geometry's ceiling and not the hand's | part 4 of the standard, the rescue or limit case, was missing |
| S15 | 559 | K9's "not far from equal" replaced by the computed cost of the real 1.5 ratio: w = 0.127, 94% of the optimum | `verify.py`: `max w=0.13500 at ratio l2/l1=1.0000`, `human ratio 1.5: w=0.12728 (94.3% of max)` |

### Gate results after the apply

| gate | baseline (pristine) | after |
|---|---|---|
| `checktex` | 818 segments, 0 issues | 921 segments, 0 issues |
| `checklt` | 0 | 0 |
| `check_links` | 130 links, 0 broken, 0 unlinked refs | 144 links, 0 broken, 0 unlinked refs |
| `check_svg` | 0 hard, 1 advisory (14 dense polylines) | 0 hard, 1 advisory (unchanged) |
| `check_code` | 4 blocks, 0 issues | 4 blocks, 0 issues |
| `verify_dom` | 0 mjx-merror, 0 broken links | 0 mjx-merror, 0 broken links |
| `check_overlap` | 0 | 0 |
| `check_frame` | 0 clipped; 6 wasted-margin advisories | 0 clipped; the same 6 advisories |
| `check_bodyprop` | 0 hairline; 7+1 advisories | 0 hairline; the same 7+1 advisories |

Advisories (`check_prose` 0, `check_proofs` 0, `check_probfig` 30/30) are unchanged. The six `check_frame` and eight `check_bodyprop` advisories are the untouched baseline set; retightening those viewBoxes risks a clipping hard-fail and is out of scope for this pass. Both regenerated figures were render-verified (`m11/preview.png`, `m11/k10.png`).
