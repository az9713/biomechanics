# Editor report: module10.html (Balance, Stability, and Sensorimotor Control)

Reader: a graduate in a quantitative field, fluent in linear algebra, ODEs and
probability, with no prior exposure to biomechanics or motor control.

Baseline gates on the pristine copy (`edited/module10.html`, 733 lines): all nine
exit 0. `checktex` 0 issues / 725 math segments; `checklt` 0; `check_links` 177
internal, 0 broken, 0 unlinked; `check_svg` 0 hard, 3 advisory; `check_code` 4
blocks, 0 issues; `verify_dom` 0 `mjx-merror`, 22 stray `$`, 3 swallowed-prose
advisories (all three are `\begin{smallmatrix}` runs, not mangled prose);
`check_overlap` 0; `check_frame` 0 clipped, 8 wasted-margin advisories;
`check_bodyprop` 0 hard, 3 advisory. The `check_frame` clipping bug that this
module motivated is already fixed: nothing is clipped.

## 1. Verdict

**Yes, after revision.** The mathematical spine is the best in the course so far.
Every proposition carries a proof, and the proofs are correct: I re-derived the
delayed characteristic equation, the imaginary-axis crossing conditions, the
Lyapunov solution for the stationary covariance, the scalar Kalman gain, and the
capture-point placement, and each one holds. Four of the computed figures decode
back to exactly the model their caption claims. The stability island in Fig. 6
matches the analytic boundary to within a pixel across the whole sweep
(kp = 27.82 at tau = 0.10, 18.28 at 0.15, 13.78 at 0.20, 11.31 at 0.25, 9.86 at
0.30). Fig. 8's three Gaussians decode to sigma_p = 1.00, sigma_m = 0.600, fused
sigma = 0.514, against the theoretical K = 0.735 and (1-K)sigma_p^2 = 0.265,
sigma = 0.515: correct to three figures. Fig. 11's success curves cross 50 % at
51.4 and 19.3 N s, exactly Lab D's printed output.

What blocks it is a set of defects that every gate is blind to, and one of them is
a contradiction between two boxed results of the module's own.

The worst is B1. Proposition 1.2 boxes `J_max = m*omega0*b = 21.7 N s` as the
*iff* bound for arresting a push without a step, and Proposition 7.1 proves the
ankle's authority is bounded by the foot. Lab A then simulates an **unbounded**
ankle and reports arresting 32.4 N s, and K1 tells the reader that this number is
the boxed budget "eroded by the whole delayed transient". It is not eroded; it is
49 % larger, because the simulated controller places the centre of pressure
outside the foot, which Proposition 7.1 forbids. Fig. 12 draws the same wrong
curve, reading 37 N s at tau = 0.02. Saturating the command at
`|u| <= omega0^2 * (b/l) = 0.961 rad/s^2` fixes it: the bisection then returns
21.6 N s as tau goes to zero, against the boxed 21.7, and falls monotonically to
18.5, 15.5 and 0.8 N s at 50, 100 and 150 ms. The lab stops contradicting the
theory and starts confirming it, which is what a lab is for.

Second, every figure cross-reference in the module is off by one. There are twelve
`<figure>` elements and the CSS numbers all twelve; the prose cites Fig. 1 through
Fig. 11 and never cites Fig. 2. A reader who follows "the stability island
(Fig. 5)" from Section 4 lands on the sensor map.

Third, four symbols carry two meanings each, and the Appendix notation table
*records* two of the collisions rather than resolving them.

Fourth, six of the ten computational solutions carry numbers that appear in no
code anywhere in the module, under a sentence in Section 11 promising that "the
computational solutions use Python-verified numbers". Two of those six are wrong.
K3's stated optimum is not the optimum and is not, as claimed, "pressed against
the island edge": at k_d = 6.8 and tau = 0.10 the island ceiling is k_p = 52.5,
so the stated k_p = 27 sits at half the ceiling, and a grid search over
k_p in [10, 55], k_d in [0.5, 16] finds an interior optimum at (29.0, 8.2) with
0.480 s settling against 0.856 s at the stated pair. K6 cannot be solved at all:
its motor-noise model `q(k_p) = q0(1 + (k_p/k_ref)^2)` never gives `q0` or
`k_ref`, so its answers 22 s^-2 and 0.9 deg are unreachable. (They are
recoverable: `q0 = 2.20e-3 rad^2 s^-3` and `k_ref = 8 s^-2` reproduce both to
three figures, and the optimum has the closed form
`k_p* = omega0^2 + sqrt(omega0^4 + k_ref^2)`, which the solution should give.)

Fixed, this is a strong module. Nothing about the physics needs rebuilding.

## 2. Blocking defects

### B1. Lab A simulates an unbounded ankle, so its budget exceeds the bound Proposition 1.2 proves and Proposition 7.1 requires

Location: `module10.html:353` (lab intro), `355-389` (code), `392` (figure),
`394` (output), `598` (K1 solution).

Quoted (`394`): "Output: $J_{\max}\approx32,\ 25,\ 1\ \mathrm{N\,s}$ at delays
$\tau=50,100,150\ \mathrm{ms}$".
Quoted (`598`): "The number is not the impulse-momentum $m\omega_0 b$ of D1 but
that budget eroded by the whole delayed transient."

Fails part 1 (precise statement) and part 4 (the limit case). Proposition 1.2
boxes `J <= m*omega0*b`, giving 70 x 3.1 x 0.10 = 21.7 N s. The lab's
`om[i+1] = om[i] + dt*(w0*w0*th[i] - kp*thd - kd*omd)` applies whatever angular
acceleration the gains ask for. At the moment of a 32 N s push the damping term
alone commands `kd * J/(m*l) = 3 x 0.457 = 1.37 rad/s^2`, which by
`u = -omega0^2 * theta_cop` corresponds to a centre of pressure 0.143 m from the
ankle: outside the foot, and outside what Proposition 7.1 permits. The lab's
`theta_max` test also tests the wrong quantity: it checks whether the *centre of
mass* crosses the foot edge, while the module's own capturability condition is a
test on the *extrapolated* centre of mass.

The fix is one saturation and one changed failure test. With
`u_max = omega0^2 * theta_edge = 0.961 rad/s^2` and divergence (not COM lean) as
the failure mode, the bisection returns 21.62 N s as tau goes to zero against the
boxed 21.70 (0.4 % low, the bisection's own resolution), and the answer is
insensitive to the divergence threshold: 0.25, 0.35 and 0.50 rad all give
21.62 / 18.48 / 15.48 / 0.76 at tau = 0.001 / 0.05 / 0.10 / 0.15.

Replacement code block for `355-389`:

```python
import numpy as np

w0, kd, kp, ell, m = 3.1, 3.0, 20.0, 1.0, 70.0
theta_edge = 0.10         # COP limit: foot margin b divided by ell (rad)
u_max = w0*w0*theta_edge  # bounded ankle authority, Prop. 7.1 (rad/s^2)


def recover(J, tau, T=8.0, dt=0.002):
    """Delayed closed loop after a push impulse J (N s), with the ankle
    command saturated at the foot edge. True if the controller arrests
    the sway instead of letting it diverge."""
    n = int(T/dt)
    d = max(1, int(round(tau/dt)))
    th = np.zeros(n+1)
    om = np.zeros(n+1)
    om[0] = J/(m*ell)                  # theta-dot kick from the impulse
    for i in range(n):
        thd = th[i-d] if i-d >= 0 else 0.0
        omd = om[i-d] if i-d >= 0 else 0.0
        u = np.clip(-(kp*thd + kd*omd), -u_max, u_max)
        om[i+1] = om[i] + dt*(w0*w0*th[i] + u)
        th[i+1] = th[i] + dt*om[i+1]
        if abs(th[i+1]) > 0.35:        # diverged: a step is unavoidable
            return False
    return abs(th[-1]) < 0.02 and abs(om[-1]) < 0.05


def max_impulse(tau):                  # bisection on the pass/fail flag
    lo, hi = 0.0, 40.0
    for _ in range(34):
        mid = 0.5*(lo+hi)
        lo, hi = (mid, hi) if recover(mid, tau) else (lo, mid)
    return lo


print("bound m*w0*b = %.1f N s" % (m*w0*theta_edge*ell))
for tau in (0.001, 0.05, 0.10, 0.15):
    print(f"tau={tau*1000:4.0f} ms -> J_max = {max_impulse(tau):.1f} N s")
```

Output:

```
bound m*w0*b = 21.7 N s
tau=   1 ms -> J_max = 21.6 N s
tau=  50 ms -> J_max = 18.5 N s
tau= 100 ms -> J_max = 15.5 N s
tau= 150 ms -> J_max = 0.8 N s
```

Replacement for the lab intro (`353`):

```html
<p>Simulate the delayed closed loop of <a class="secref" href="#delay">Section 4</a> after a horizontal push and find, by bisection, the largest impulse the ankle can still arrest without a step. Two modelling choices make the lab a test of the theory rather than a separate story. The ankle command is <b>saturated</b> at $u_{\max}=\omega_0^2\,(b/\ell)$, because <a class="secref" href="#recovery">Proposition 7.1</a> confines the centre of pressure to the foot; without that clip the simulation would arrest impulses no real ankle can. And the failure test is <em>divergence</em> - the lean running away past $0.35\ \mathrm{rad}$, where a step becomes unavoidable - not the instantaneous position of the centre of mass. With these, the delay-free limit must reproduce the boxed $J_{\max}=m\omega_0 b$ of <a class="secref" href="#margin">Proposition 1.2</a>, and everything below it is the budget that delay takes away.</p>
```

Replacement for the output note (`394`):

```html
<p class="small">Output: the bisection returns $J_{\max}=21.6\ \mathrm{N\,s}$ as $\tau\to0$, against the boxed $m\omega_0 b=21.7\ \mathrm{N\,s}$ - the lab reproduces <a class="secref" href="#margin">Proposition 1.2</a> to the resolution of its own bisection. Delay then eats it: $18.5,\ 15.5,\ 0.8\ \mathrm{N\,s}$ at $\tau=50,100,150\ \mathrm{ms}$ (Fig. 12). The budget is more than halved well before the loop itself goes unstable at $\tau_c\approx137\ \mathrm{ms}$, which is why a slowed reflex is dangerous while quiet standing still looks steady. <b>Try:</b> raise <code>u_max</code> and watch the budget climb past the bound - the simulated ankle then places the centre of pressure off the foot, which is the modelling error the clip prevents. <b>Try:</b> add the hip and step rungs of <a class="secref" href="#recovery">Section 7</a> and watch the arrestable impulse jump when a step is allowed.</p>
```

Replacement for K1's solution (`598`), with the impulse-momentum comparison
turned the right way round and code added (see B9):

```html
<details class="sol"><summary>Solution</summary><div>Integrate the delay-differential equation from a velocity kick $\dot\theta_0=J/(m\ell)$ with the ankle command saturated at $u_{\max}=\omega_0^2(b/\ell)$, mark success when the lean is arrested rather than diverging, and bisect on $J$. As $\tau\to0$ the bisection returns $21.6\ \mathrm{N\,s}$, recovering the impulse-momentum bound $m\omega_0 b=21.7\ \mathrm{N\,s}$ of D1: with no delay, the only thing standing between the push and a step is the capturability condition, exactly as Proposition 1.2 says. Delay is what erodes it - $18.5,\,15.5,\,0.8\ \mathrm{N\,s}$ at $\tau=50,100,150\ \mathrm{ms}$. The shape of $J_{\max}(\tau)$ is a slow decline followed by a collapse: while the loop is well damped the budget falls roughly linearly, because the saturated ankle spends part of its authority correcting a stale state; once $\tau$ approaches $\tau_c\approx137\ \mathrm{ms}$ the damping the velocity term supplies vanishes, so even a small kick rings up instead of down and the budget falls to a fiftieth of its delay-free value.</div></details>
```

### B2. Every figure cross-reference is off by one, and Fig. 1 is never cited

Location: `module10.html:53, 65, 117, 135, 155, 199, 209, 233, 251, 265, 269,
295, 333, 344, 394, 397, 430, 433`.

Quoted (`199`): "traces the boundary of the <b>stability island</b> in the
$(\tau,k_p)$ plane at fixed $k_d$ (Fig. 5)".

Fails the structural rule that figures are referenced from the prose. The page
holds twelve `<figure>` elements. The stylesheet sets `counter-reset:fig` on
`body` and `counter-increment:fig` on `figure`, so the rendered captions run
Fig. 1 to Fig. 12 with no exception. The prose cites Fig. 1 to Fig. 11 and never
cites Fig. 2. The stability island is the sixth figure, not the fifth; the
sensor map is the fifth, not the fourth; and so on for every reference from
Fig. 1 upward. The Section 0 body figure, rendered as Fig. 1, is cited nowhere.

Fix: raise every existing numeric reference by one (1 to 2, 3 to 4, 4 to 5, 5 to
6, 6 to 7, 7 to 8, 8 to 9, 9 to 10, 10 to 11, 11 to 12), and cite Fig. 1 in
Section 0. Add to the end of `module10.html:47`:

```html
 Figure 1 fixes the geometry the module argues about: a body, its centre of mass, the base of support its feet enclose, and the region a step could still reach.
```

### B3. The module never places its models on the level ladder

Location: after `module10.html:65`.

Fails the course-wide requirement that each module states which rungs its models
sit on. Nowhere in 733 lines does the word "level" appear in that sense. Insert
after line 65:

```html
<p class="small">Where these models sit on the course's level ladder. <a class="secref" href="#margin">Section 1</a>'s margin of stability is <b>Level 1</b>: a rigid-body dynamic statement about one segment, with no actuator model at all. <a class="secref" href="#statespace">Sections 2</a> to <a class="secref" href="#kalman">6</a> are <b>Level 4</b>, closed-loop control of a linear plant: a two-state linearised pendulum, a linear feedback law, a linear measurement model, and a linear estimator, every one of them exact and every one of them valid only for small sway. <a class="secref" href="#recovery">Section 7</a>'s step is <b>Level 5</b>, a change of contact topology, but it is handled by a placement rule rather than by simulating the swing, so the multibody dynamics of the step itself are not here. <a class="secref" href="#aging">Section 9</a> is a <b>Level 1</b> parameter study, not a model of ageing tissue. Nothing in this module is nonlinear, multi-segment, or three-dimensional; those live in Modules 12 and 13.</p>
```

### B4. Four symbols carry two meanings each, and the notation table records two of them instead of resolving them

Location: `module10.html:111, 218, 224, 227, 246, 251, 263, 327-329, 338, 340,
342, 346, 541, 653, 683, 684, 694, 699`.

Fails the notation contract. The four collisions:

- **`\tau`.** Line 111 defines it as the ankle torque: "the commanded angular
  acceleration produced by the ankle torque $\tau$". Line 188 onward defines it
  as the total feedback delay. Section 9 then uses both at once, in one table:
  "Reflex/loop delay $\tau$" on line 327 sits two rows above "Peak ankle torque
  $\tau_{\max}$" on line 328 and "Torque rate $\dot\tau$" on line 329. The
  Appendix already commits to `\tau_{\rm ank}` for the torque (line 683) but the
  body text never uses it. Resolve in favour of the Appendix: write
  `\tau_{\rm ank}` at line 111, and `\tau_{\rm ank,\max}` and
  `\dot\tau_{\rm ank}` everywhere `\tau_{\max}` and `\dot\tau` now appear
  (lines 328, 329, 338, 342, 346, 541, 653, 699).
- **`\xi`.** Defined on line 78 as the extrapolated centre of mass and used that
  way in Sections 1, 7, 8 and 9. Definition 5 (line 218) then writes
  `\ddot\theta+a_1\dot\theta+a_0\theta=\xi(t)` with
  `\langle\xi(t)\xi(t')\rangle=q\,\delta(t-t')`: the same letter is now the white
  noise. Rename the noise `\eta` at lines 218, 219 and 227.
- **`K`.** Line 125 is the state-feedback gain row `K=[k_p\ k_d]`; line 246 is
  the scalar Kalman gain. The notation table has both (lines 684 and 694) and
  labels the second "$K$ (scalar)", which names the collision without removing
  it. Rename the Kalman gain `K_f` in Proposition 6.1, its proof, the discussion
  at line 251, the Fig. 8 caption, C6, D6, and the notation table.
- **`Q`.** Definition 3 (line 142) is the LQR state weight; the proof of
  Proposition 5.1 (line 227) is the process-noise covariance `Q=GqG^{\mathsf T}`,
  and Lab C's code reuses the name a third time. Rename the noise covariance
  `\Sigma_w` at line 227.

### B5. Proposition 7.1's proof states the inverted-pendulum law with the sign reversed

Location: `module10.html:277`.

Quoted: "the ground reaction (vertical component $\approx mg$ in slow sway)
acting at the COP a horizontal distance $(x_{\rm cop}-x_{\rm com})$ from the COM
produces a horizontal COM acceleration
$\ddot x_{\rm com}=\tfrac{g}{\ell}(x_{\rm cop}-x_{\rm com})$ in the linearised
pendulum (dividing the restoring moment $mg(x_{\rm cop}-x_{\rm com})$ by the
moment of inertia $m\ell^2$ and multiplying by the lever $\ell$ to get a linear
acceleration)."

Fails part 1 (a precise statement) and part 3 (a proof whose mechanism is
visible). The linear inverted-pendulum law is
`x_com_ddot = (g/l)(x_com - x_cop)`: the centre of mass accelerates *away* from
the centre of pressure, which is why pushing the COP toward the toe decelerates a
forward lean. The stated form has the opposite sign and contradicts the module's
own Section 1, where the COP sits at the ankle (`x_cop = 0`) and the free body
obeys `x_ddot = +omega0^2 x`. The parenthetical recipe ("divide the moment by the
inertia and multiply by the lever") gets the right magnitude by accident and
hides the argument. Replacement:

```html
<div class="proof">Model the body as a point mass $m$ at height $\ell$ carried by a massless leg, with the ground reaction acting at the COP. Its vertical component is $\approx mg$ in slow sway. Take angular momentum about the COP: the reaction force has no moment there, so the only moment is gravity's, $mg(x_{\rm com}-x_{\rm cop})$, and the angular momentum of the point mass about the COP is $m\ell\,\dot x_{\rm com}$. Equating the rate of change to the moment gives $m\ell\,\ddot x_{\rm com}=mg(x_{\rm com}-x_{\rm cop})$, i.e. $$\ddot x_{\rm com}=\frac{g}{\ell}\big(x_{\rm com}-x_{\rm cop}\big),$$ the linear inverted-pendulum law: the COM accelerates <em>away</em> from the COP, so a forward lean is arrested by driving the COP forward, past the COM. With $x_{\rm cop}=0$ this is the $\ddot x=\omega_0^2 x$ of <a class="secref" href="#margin">Section 1</a>. The magnitude $|\ddot x_{\rm com}|$ is largest when the COP is driven to whichever foot edge is farther from the COM, giving the stated bound. Since arresting a forward lean requires $x_{\rm cop}\gt x_{\rm com}$ and the COP cannot pass the toe, the available restoring acceleration falls to zero as $x_{\rm com}$ itself reaches the toe: the ankle saturates at the foot boundary. <span class="qed">&#8718;</span></div>
```

### B6. K3's answer is wrong in value and in interpretation

Location: `module10.html:606`.

Quoted: "The fastest settling ($\approx0.5\ \mathrm{s}$) sits at high
$k_p\approx27$ with strong damping $k_d\approx6.8$ - pressed against the island
edge. The optimum is a corner solution bounded by the delay, not an interior
one".

Fails part 1 and part 5. Three checks, all against code:

1. The island ceiling at `k_d = 6.8` and `tau = 0.10`, from Proposition 4.2, is
   `k_p = 52.5`. The stated `k_p = 27` sits at 51 % of the ceiling. It is not
   pressed against the edge.
2. A grid search over `k_p` in [10, 55] step 0.5 and `k_d` in [0.5, 16] step 0.1,
   scoring by the time for `|theta|` to fall under 10 % of its peak after a
   velocity kick at `tau = 0.10`, finds the optimum at `(29.0, 8.2)` with 0.480 s.
   The stated pair scores 0.856 s. The design gains (20, 3) score 4.170 s.
3. The optimum is interior under every settling definition tried: 2 % settling
   puts it at (23.5, 6.7) with 0.713 s; a tilt initial condition at (33.0, 8.4)
   with 0.446 s. None sits on a search-box edge, and none is near the island
   ceiling.

The interesting fact the problem should surface is the opposite of the one
stated: the delay bounds the *useful* gain long before it bounds the *stable*
gain. Replacement:

```html
<details class="sol"><summary>Solution</summary><div>Grid-search $(k_p,k_d)$ at $\tau=100\ \mathrm{ms}$, discard the pairs whose late-time amplitude does not decay, and score the survivors by the settling time - the last instant at which $|\theta|$ still exceeds $10\%$ of its peak after a velocity kick. Over $k_p\in[10,55]$ and $k_d\in[0.5,16]$ the fastest recovery is $0.48\ \mathrm{s}$ at $k_p=29.0\ \mathrm{s^{-2}}$, $k_d=8.2\ \mathrm{s^{-1}}$; the design gains $(20,3)$ take $4.17\ \mathrm{s}$, so tuning is worth a factor of nine. The optimum is <em>interior</em>, and that is the point. The stability island at $k_d=8.2$ and $\tau=0.10$ does not close until $k_p\approx58$, so the best gains sit at half the ceiling: what stops the search is not instability but the delayed correction beginning to overshoot, adding a second swing that costs more time than the faster first approach saves. Delay therefore bounds the <em>useful</em> gain well before it bounds the <em>stable</em> gain, and the two bounds must not be confused - a controller tuned to the island edge would be fast in the first half-second and ringing for four.</div></details>
```

### B7. K6 cannot be solved: neither parameter of its noise model is given

Location: `module10.html:616` (statement), `618` (solution).

Quoted (`616`): "With signal-dependent motor noise
$q(k_p)=q_0\big(1+(k_p/k_{\rm ref})^2\big)$, sweep the gain and find the
sway-minimising $k_p$."
Quoted (`618`): "giving an interior optimum near $k_p\approx22\ \mathrm{s^{-2}}$
(RMS $\approx0.9^\circ$)".

Fails part 2 (every term defined) and the exercise rule that every problem is
solvable from the text alone. `q_0` and `k_ref` are given no values here, in
Section 5, or in the Appendix, so neither 22 nor 0.9 can be reproduced. The
optimum depends on `k_ref` alone, through the closed form derived below, and
slides from 20.9 to 31.8 s^-2 as `k_ref` goes from 6 to 20; the RMS depends on
`q_0`. The two values that reproduce the stated answers are
`q_0 = 2.20e-3 rad^2 s^-3` (which is also the intensity Fig. 7 was drawn with,
see B13) and `k_ref = 8 s^-2`: they give `k_p* = 22.11 s^-2` and RMS 0.912 deg.

The solution also says "minimise numerically" when the minimisation is exact.
Setting the derivative of `(1 + c k^2)/(k - a)` to zero with `a = omega0^2` and
`c = 1/k_ref^2` gives `c k^2 - 2 a c k - 1 = 0`, hence
`k_p* = omega0^2 + sqrt(omega0^4 + k_ref^2)`.

Replacement statement (`616`):

```html
<div class="prob"><b>K6.</b> Motor noise grows with the command. Take the intensity of the forcing in <a class="secref" href="#noise">Proposition 5.1</a> to be $q(k_p)=q_0\big(1+(k_p/k_{\rm ref})^2\big)$ with the two <em>assumed</em> constants $q_0=2.20\times10^{-3}\ \mathrm{rad^2\,s^{-3}}$ (the baseline intensity that reproduces the quiet-standing sway of Fig. 7) and $k_{\rm ref}=8\ \mathrm{s^{-2}}$ (the gain at which command noise equals the baseline). Sweep the gain, find the sway-minimising $k_p$, derive it in closed form, and say what happens to it as $k_{\rm ref}$ rises. <span class="probes"><b>Probes:</b> <a class="secref" href="#noise">Section 5</a>; sensitivity + optimization.</span></div>
```

Replacement solution (`618`):

```html
<details class="sol"><summary>Solution</summary><div>Substituting into $\operatorname{Var}(\theta)=q(k_p)/[2(k_p-\omega_0^2)k_d]$ and writing $a=\omega_0^2$, $c=k_{\rm ref}^{-2}$, the minimiser of $(1+ck_p^2)/(k_p-a)$ solves $ck_p^2-2ack_p-1=0$, so $$\boxed{\;k_p^\star=\omega_0^2+\sqrt{\omega_0^4+k_{\rm ref}^2}\;}$$ With $\omega_0=3.1$ and $k_{\rm ref}=8$ this is $k_p^\star=22.11\ \mathrm{s^{-2}}$, matching a numerical sweep to four figures, and $q_0=2.20\times10^{-3}$ then gives RMS sway $0.912^\circ$. Sway falls at first, because tighter control suppresses the baseline noise faster than the command grows, then rises, because the command's own noise scales as $k_p^2$ while the suppression only scales as $k_p$. The sensitivity is the deeper result: $k_p^\star$ climbs with $k_{\rm ref}$ - $20.9$, $22.1$, $31.8\ \mathrm{s^{-2}}$ at $k_{\rm ref}=6,8,20$ - and crosses the $\tau=100\ \mathrm{ms}$ island ceiling of $27.8\ \mathrm{s^{-2}}$ at $k_{\rm ref}\approx15.4$. A person with clean motor noise cannot use the gain that would minimise their sway, because the delay forbids it; below that crossing noise binds, above it delay does. A constant-noise model shows neither trade-off.</div></details>
```

### B8. K8's admissible window rests on a number that is not what it is called

Location: `module10.html:626`.

Quoted: "Capture requires $\xi'\in[-\text{BoS},0]$, i.e.
$0\le e\le\text{BoS}$, where the base-of-support depth is a foot length
$\approx0.10\ \mathrm{m}$ (the same scale as the margin $b$ of the Appendix)".

Fails the number rule. An adult foot is about 0.25 m, not 0.10 m; and 0.10 m is
the Appendix's `b`, the *extrapolated-COM headroom of the standing base*, which
is a different quantity from the depth of the double-support base after a step.
The parenthesis notices the coincidence and treats it as a justification.

The window is real, but its binding upper limit is reach, not base depth, and
Definition 6 already supplies the reach. Replacement:

```html
<details class="sol"><summary>Solution</summary><div>Take the push of Definition 6: an impulse $J$ sets $\xi^+=J/(m\omega_0)$, which grows as $\xi(t)=\xi^+e^{\omega_0 t}$ while the step is prepared, so at touchdown $t_{\rm step}=\tau+t_{\rm move}$ the extrapolated COM sits at $\xi_s=\xi^+e^{\omega_0 t_{\rm step}}$. Plant the foot at $x_{\rm foot}=\xi_s+e$. By D8 the post-step divergent coordinate is $\xi'=-e$, so capture needs $e\ge0$: any <em>undershoot</em> leaves $\xi$ ahead of the new pivot and the body keeps diverging, with no second chance at that step. The upper limit is the leg, not the base - the foot cannot be planted past the reachable step length, so $\xi_s+e\le L_{\rm step}$. The window is therefore $$0\le e\le L_{\rm step}-\xi_s.$$ For the young parameter set ($\tau=0.10$, $t_{\rm move}=0.20\ \mathrm{s}$, $L_{\rm step}=0.60\ \mathrm{m}$, $m=70\ \mathrm{kg}$, $\omega_0=3.1$) and a $40\ \mathrm{N\,s}$ push, $\xi_s=0.467\ \mathrm{m}$ and the window is $0\le e\le0.133\ \mathrm{m}$: a 13 cm overshoot is survivable, a 1 cm undershoot is not. For the aged set ($\tau=0.18$, $t_{\rm move}=0.32$, $L_{\rm step}=0.42$) the same push gives $\xi_s=0.599\ \mathrm{m}$ against a reach of $0.42\ \mathrm{m}$: the window is empty and the step cannot be made at all. The window closes exactly at $\xi_s=L_{\rm step}$, i.e. at $J=m\omega_0 L_{\rm step}e^{-\omega_0 t_{\rm step}}=51.4\ \mathrm{N\,s}$, which is $J_{\rm crit}$ of Definition 6 - so the reach model is not a separate result but the statement that the capture window has shrunk to a point. The asymmetry, forward error tolerated and backward error fatal, is why reactive steps are aimed deliberately long.</div></details>
```

### B9. Six of the ten computational solutions carry numbers produced by no code, under a sentence promising Python-verified numbers

Location: `module10.html:507`, and the solutions to K3 (`606`), K4 (`610`),
K6 (`618`), K7 (`622`), K8 (`626`), K10 (`634`).

Quoted (`507`): "the computational solutions use Python-verified numbers."

The module holds four `<pre><code>` blocks, all four in Section 10. K1, K2, K5
and K9 name the lab whose code produced their numbers, which is honest. The other
six give numbers with no source anywhere on the page. Fix in two parts: state the
provenance rule accurately, and add a code block to each of the six. Replacement
for line 507:

```html
<p>Thirty problems in three families - ten conceptual, ten derivational, ten computational - plus five quick diagnostics, then an honest account of what this single-segment, sagittal, linearised model captures and misses, and the ledger of debts it hands forward. Every problem carries a figure and a collapsible solution. Every number in a computational solution is one a script on this page printed: K1, K2, K5 and K9 name the lab of <a class="secref" href="#labs">Section 10</a> that produced theirs, and K3, K4, K6, K7, K8 and K10 carry their own copy-buttoned block.</p>
```

The six code blocks are written out in the applied edit (tags B9a to B9f) and
their outputs are in the change table of Section 6. Each is PEP8 and each was run
before it was pasted.

### B10. Fig. 7's caption says the sway trace stays inside the sigma band; the drawn trace leaves it on a third of its samples

Location: `module10.html:231`.

Quoted: "a simulated sway trace wanders like a damped random walk, staying within
the $\pm\sigma$ band set by the stationary variance of Proposition 5.1
(dashed)."

Decoding the trace (2400 points; x calibrated from the 0/8/16/24 s ticks, y from
the -2/-1/0/1/2 deg ticks): the band is at +/- 0.340 deg, the trace RMS is
0.358 deg, 33.9 % of samples lie outside the band in 14 separate excursions, and
the peak excursion is 0.944 deg, 2.8 sigma. The figure is right and the caption
is wrong: a Gaussian process leaves its one-sigma band about a third of the time,
and saying otherwise teaches the reader that sigma is a bound. Replacement clause:

```html
Left: a simulated sway trace wanders like a damped random walk about upright, crossing the $\pm\sigma$ band of Proposition 5.1 (dashed) on about a third of its samples and peaking near $3\sigma$, as a Gaussian process must; what the theory fixes is not a bound but the trace's RMS, which matches the band's own value.
```

### B11. Fig. 8's Kalman-gain label writes the wrong subscript

Location: `module10.html:263` (the SVG `<text>` inside the figure).

Quoted (rendered): `K = σ²ₖ/(σ²ₖ+σ²ₘ) = 0.74`.

Proposition 6.1 boxes `K = sigma_p^2/(sigma_p^2 + sigma_m^2)`, with `p` for
prediction. The figure writes `k`, a subscript that appears nowhere in the
module. The figure's geometry is otherwise exactly right: the three Gaussians
decode to sigma_p = 0.998, sigma_m = 0.600 and fused sigma = 0.514, against the
theoretical 0.515, and K = 0.735 against the labelled 0.74. Replace the entity
`&#8342;` (subscript k) with `&#8346;` (subscript p) in both occurrences, and
rename `K` to `K_f` per B4.

### B12. Lab C and Fig. 8 run at sixteen times the module's own quiet-standing noise, and the caption calls it a real sway

Location: `module10.html:263` (caption), `265`, `433` (lab intro), `446` (code).

Quoted (`265`): "Fig. 7 (right) runs both steps on a real sway".

Lab C sets `qp=0.6`. Through Proposition 5.1 with `k_p=20`, `k_d=3` that is a
stationary RMS of 5.62 deg, against the Appendix's quiet-standing 0.3 to 0.9 deg
and the 0.34 deg that Fig. 7 was drawn with. The drawn true-sway curve in Fig. 8
decodes to 0.0955 rad = 5.5 deg, confirming the figure is stationary at the
inflated intensity. This is a legitimate choice - at 0.34 deg the estimator's
work would be invisible at figure scale - but it must be declared, or the reader
carries 5 deg away as the amplitude of quiet standing. Add to the lab intro
(`433`):

```html
 The noise is deliberately exaggerated: <code>qp=0.6</code> gives a stationary sway of $5.6^\circ$ by <a class="secref" href="#noise">Proposition 5.1</a>, some sixteen times real quiet standing, so that the estimator's advantage is visible at figure scale. Lower it to $2.2\times10^{-3}$ for the true amplitude and the same conclusion survives with the curves on top of one another.
```

And to the Fig. 8 caption, replacing "a real sway" with "a simulated sway at
sixteen times the quiet-standing noise amplitude, so the curves separate".

### B13. The noise intensity q, the only parameter of Proposition 5.1, is given no value anywhere

Location: `module10.html:218`, `224`, `233`, `231` (caption), Appendix table
(`702-717`).

Proposition 5.1 boxes `Var(theta) = q / (2(k_p - omega0^2) k_d)`. `q` is defined
as an intensity and never given a number, so no reader can evaluate the boxed
result or check the Appendix's "Quiet-standing RMS sway 0.3 to 0.9 deg" against
it. Fig. 7's own analytic curve fixes the value: fitting `c/sqrt(k_p - a)` to the
drawn solid curve returns `a = 9.615` (against `omega0^2 = 9.61`) and
`c = 1.0974 deg`, with maximum residual 0.0036 deg, which inverts to
`q = 6 c^2 = 2.20e-3 rad^2 s^-3`. Add the row to the Appendix parameter table:

```html
<tr><td>Noise intensity</td><td>$q$</td><td>$2.2\times10^{-3}\ \mathrm{rad^2\,s^{-3}}$</td><td>assumed; sets the Fig. 7 sway</td></tr>
```

and state it at the point of use, appending to line 233:

```html
 The intensity itself is a modelling assumption: $q=2.2\times10^{-3}\ \mathrm{rad^2\,s^{-3}}$ is the value used throughout this section and in Fig. 7, chosen so that the boxed variance reproduces the $0.34^\circ$ RMS sway of a healthy adult at the design gains.
```

### B14. Bare numbers with no class

Each is a number that is neither derived, nor a table parameter with symbol and
unit, nor labelled an assumption.

- `module10.html:161`: "with a latency near $40\ \mathrm{ms}$" for the Golgi
  tendon organ. The other three latencies are Appendix rows. Add the row:
  `<tr><td>Golgi tendon organ latency</td><td>$\tau_s$</td><td>$\approx40\ \mathrm{ms}$</td><td>Ib afferent</td></tr>`.
- `module10.html:494-495` (Lab D): `tau=0.10/0.18`, `t_move=0.20/0.32`,
  `l_step=0.60/0.42`. The symbols are in the notation table; the values are
  nowhere. Add a young/aged parameter block to the Appendix (applied as B14b).
- `module10.html:342` (Fig. 11 caption): the aged island is drawn at
  `k_d = 1.7 s^-1` against the young 3.0 (recovered by matching the drawn
  boundary: the aged curve passes k_p = 16.55 at tau = 0.10 and 11.19 at 0.15,
  which `k_d = 1.68` reproduces to 0.15). That number is stated nowhere, and
  reduced damping gain is not one of Section 9's four drifts, so the figure shows
  a fifth parameter the model does not list. Name it in the caption and tie it to
  the torque-rate row.
- `module10.html:342`: the shaded everyday-perturbation density is undefined. It
  decodes to a lognormal with median 17.9 N s and log-SD 0.51 (mode 13.8,
  95th percentile 40.3). Declare it as an assumption and give the two overlaps it
  produces: 1.8 % of everyday perturbations exceed the young `J_crit` of
  51.4 N s, 44.5 % exceed the aged 19.3 N s.
- `module10.html:634` (K10): `mu_avail = 0.30, 0.15, 0.08` and, in the revised
  solution, the slip duration. Label them assumed surface values and an assumed
  slide interval.

### B15. Section 1's concrete tie-in is off by a factor of five

Location: `module10.html:105`.

Quoted: "$J_{\max}\approx70\times3.1\times0.10\approx22\ \mathrm{N\,s}$ - about
the impulse of a firm shove or a $3\ \mathrm{kg}$ mass swung at walking speed."

A 3 kg mass at walking speed (1.4 m/s) carries 4.2 N s, a fifth of 22. Part 5
(the tie to something concrete) is the part that must be checked hardest, because
a wrong anchor number is the one the reader remembers. Replacement clause:

```html
 - the momentum of a $16\ \mathrm{kg}$ mass moving at walking speed ($1.4\ \mathrm{m\,s^{-1}}$), or of your own $70\ \mathrm{kg}$ brought to $0.31\ \mathrm{m\,s^{-1}}$, which is a firm shove and not a gentle one.
```

### B16. Fig. 4's caption describes a flow the panel does not draw

Location: `module10.html:137`.

Quoted: "Left: uncontrolled, upright is a saddle - the unstable manifold (slope
$+\omega_0$) carries almost every state away, which is Proposition 1.1 drawn as a
flow."

The left panel contains axes, a dot at the origin, and four straight arrows: two
red outward along slope +3.10 and two green inward along slope -3.10 (both
correct, `omega0 = 3.1`). There is no flow field and no trajectory. The right
panel is fully correct: the bold curve starts at `(theta, theta_dot) = (0, 0.932)`
as the caption says, follows the closed-loop solution for
`k_p = 20, k_d = 3` and ends within 0.001 rad of the origin, and the poles are
`-1.5 +/- 2.853 i` as line 135 states. Replacement clause:

```html
Left: uncontrolled, upright is a saddle. The two eigendirections of Proposition 1.1 are drawn: arrows run outward along the unstable one (slope $+\omega_0$, the line $\dot\theta=\omega_0\theta$ on which $\xi$ grows) and inward along the stable one (slope $-\omega_0$, the single direction $\dot\theta=-\omega_0\theta$ from which the body returns to upright). Every other initial state has a component on the unstable direction and is carried away.
```

## 3. Style and clarity edits

- `module10.html:392` caption (Fig. 12), after B1's regeneration: state the two
  endpoints, since the curve now carries the boxed bound as a reference line.
  Replacement: "Result of Lab A: the largest push impulse the fixed-support
  controller can arrest, found by bisection over the delayed closed loop with the
  ankle command saturated at the foot edge. As $\tau\to0$ the curve meets the
  impulse-momentum bound $m\omega_0 b=21.7\ \mathrm{N\,s}$ of Proposition 1.2
  (green dashed), confirming the boxed result; delay then takes it away, slowly
  at first and then in a collapse as $\tau$ approaches the critical delay
  $\tau_c\approx137\ \mathrm{ms}$ of Section 4 (red dashed). The budget is more
  than halved while quiet standing still looks steady, which is why a slowed
  reflex is dangerous before it is visible."
- `module10.html:263` caption: "the predicted estimate (red) overlays the true
  present state (black)" overstates. It tracks it at 0.033 rad RMS against the
  raw measurement's 0.075 rad (Lab C's printed output), so the honest word is
  "tracks", with the ratio given.
- `module10.html:231` caption, right panel: the analytic law is drawn past the
  island edge in grey dashes with no explanation. Say that the continuation is
  the formula extrapolated where the closed loop is no longer stable.
- `module10.html:610` (K4): the stated `$\hat J=18.0$` is not what a fit returns.
  A least-squares fit over the first 100 ms of the clean trace gives 18.26 N s
  for a true 18; with 2 mrad of measurement noise, 18.3 +/- 0.7 over 400 trials,
  and with 5 mrad, 18.3 +/- 1.6. Quote the numbers and the scatter, which is what
  the problem asks about.
- `module10.html:344`: "the fraction of daily perturbations that exceed it - the
  fall probability - climbs steeply" should carry the two numbers B14 recovers:
  1.8 % for the young envelope, 44.5 % for the aged.
- `module10.html:430` (Lab B): "The simulated stable region should match the
  analytic island" is the only lab whose text does not report a printed number.
  It prints `stable fraction: 0.37`. Say so.
- `module10.html:342` (Fig. 11 caption): name the two damping gains and the
  everyday distribution, per B14.
- `module10.html:507`: replaced by B9.

## 4. Structural notes

- The module has no closing statement of what the reader can now do. Every other
  house-shaped module ends with one, and the domain brief lists its absence as a
  known defect class. It belongs after the repayment ledger.
- Section 10's four labs are the module's strongest asset once Lab A is fixed,
  because each one *checks* a boxed result rather than illustrating it: Lab A
  against Proposition 1.2, Lab B against Proposition 4.2, Lab C against
  Proposition 6.2, Lab D against Definition 6. The lab intros should say so; two
  of them nearly do.
- Section 6 defers the matrix Riccati equation to Module 12 and proves only the
  scalar case. That is the right call and the text says why. No change.
- The 8 wasted-margin advisories from `check_frame` are all problem figures with
  20 to 40 % blank top margin. Retightening is cosmetic and I have left them.
- `check_bodyprop` flags a floating bust in C9's figure (a head with no limb) and
  two thin limbs beside a head-gradient circle. C9 is about the semicircular
  canals, so a head alone is the right drawing. The HANDOFF note about "m10
  wishbone shoulders" refers to the Section 0 body figure and the C3 body; both
  are cosmetic and neither is worth a regeneration pass in this edit.

## 5. What already works

- **The proofs.** Every one of the eleven propositions carries an adjacent proof,
  and I checked each by hand or by code. Proposition 4.2's separation of real and
  imaginary parts is exactly right, and the numbers it yields for the operating
  gains, `tau_c = 137.4 ms` and `Omega = 3.628 rad/s`, match the module's stated
  137 ms and 3.6 rad/s and the 28 degree phase lag it quotes.
- **Fig. 6.** The drawn island boundary sits on the analytic curve at every
  delay I sampled, and the three trajectories in the right panel behave exactly
  as labelled: final amplitude 0.002 rad inside the island, 0.021 rad ringing at
  constant amplitude on the boundary, 0.109 rad and growing outside.
- **Fig. 8, left.** A textbook illustration of Proposition 6.1, correct to three
  significant figures in all four quantities.
- **Fig. 11 and Fig. 12.** Both decode to their labs' printed output. Fig. 11's
  50 % points are 51.4 and 19.3 N s; Lab D prints 51.4 and 19.3.
- **K7.** The only computational solution whose numbers I could verify without
  changing anything: `tau_c = 196.6, 137.4, 99.4 ms` at `k_p = 14, 20, 28`, and
  `140.2 to 135.3 ms` over `ell = 0.8 to 1.3 m`. The module says 197, 137, 99 and
  140 to 135. It also draws the right lesson, that gain and not stature sets the
  delay tolerance.
- **Section 3.** The measurement model is introduced as a definition, each
  channel is mapped onto a row of `C`, every anatomical term is glossed in the
  sentence that uses it, and Proposition 3.1 then earns the estimator by proving
  observability from either channel alone. This is the module's best section and
  the shape other sections should copy.
- **Section 9's framing.** "Age is not itself a variable in any equation here" is
  the right sentence, and C8 makes the reader produce it. Once the fifth
  parameter in Fig. 11 is named, the argument is airtight.
