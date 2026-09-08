# Editor report: module04.html (Cartilage, Synovial Fluid, Joint Contact Biophysics)

Edited copy: `edited/module04.html`. Original `module04.html` untouched.
Every number below was produced by running code in this pass, not recalled.

## 1. Verdict

**Yes, after revision.** The spine of this module is sound and, in places, exemplary.
The consolidation equation is assembled from three named ingredients, each stated and
each proved, and the boxed result carries a real proof. The Hertz box carries a full
Boussinesq-matching derivation, not a citation. All twelve `<pre><code>` blocks run
clean with no exceptions and no undefined names, which is more than Module 3 could
say. I re-derived the module's headline numbers independently and they hold: the gel
time is 6667 s, `F(1 s) = 0.9862`, `F(0.5 s) = 0.9902`, `F(1 h) = 0.214`, the Hertz
contact radius is 17.95 mm for a mean pressure of 1.694 MPa, and `E* = 6.67 MPa`
follows correctly from `nu = 0.5` (the error Module 3 shipped is not repeated here).
I integrated both "identical load" figures numerically: the section 6 pair carry
1706 N and 1701 N, the section 8 pair 1702 N and 1710 N, all within 0.8 % of 1715 N.
Those figures are honest.

The damage is concentrated in three places. First, the module's central mathematical
object is missing: section 4 averages "the Terzaghi series" that section 3 named but
never wrote, so the reader is asked to integrate term by term an expression they have
never seen, and the derivation that supplies it sits a thousand lines later inside a
problem. Second, the problem set contains two computational problems that do not meet
the course's own standard: K9's solution abandons the recovery fraction its statement
defines and substitutes an envelope with two invented constants, and K10 is two
divisions. Third, the notation contract is broken in three places, and the Appendix
records one meaning for each colliding symbol while flagging none. Alongside these sit
a factor-of-two error in D2's limit, two problems that undo section 6's own caveat by
applying Hertz to the hip, a missing level-ladder statement, and an uncomputed loop
gain at the module's dramatic climax. None of this is unfixable and none of it touches
the physics; all thirteen are repaired below with the replacement HTML written out.

## 2. Blocking defects

### B1. The Terzaghi series is never written down; section 4 averages a series the reader has never seen

Location: `module04.html:526` (names it), `module04.html:596` (averages it).

Quoted (line 526): "Thereafter pressure bleeds off through the drained platen ($p=0$
at $z=h$) and the profile relaxes — exactly the Terzaghi solution of the consolidation
equation:"

Quoted (line 596): "<a class="secref" href="#biphasic">§3</a> already solved for
$p(z,t)$ (the Terzaghi series). Averaging that series over the depth term by term —
each cosine integrates to $\int_0^1\cos(\lambda_n Z)\,\mathrm dZ=(-1)^n/\lambda_n$ —
collapses every spatial factor..."

Section 3 never solved for `p(z,t)`. It states the initial condition, shows a figure
captioned "Terzaghi series solution", and moves on. No series, no eigenfunctions, no
coefficients appear anywhere in sections 0 to 8. So equation (1) of section 4 — the
fluid load support function on which sections 5, 7 and 8 and eleven problems all rest
— is obtained by averaging an object the text has not produced. The derivation exists
only in D5, at line 1652, which is both a forward reference the reader must accept on
faith and a violation of the rule that dependencies point backwards. This fails part 3
of the standard (a proof in the smallest setting) for the module's most-used result.

Fix: promote D5's separation of variables into section 3 as a proved proposition,
immediately before the consolidation figure. I checked the coefficients: expanding the
uniform initial pressure `p = sigma_0` in the cosine modes gives
`4(-1)^n/((2n+1)pi)`, and depth-averaging with `int_0^1 cos(lambda_n Z) dZ =
(-1)^n/lambda_n` yields `2/lambda_n^2`, whose sum at `T=0` is the Basel value 1.

Insert after line 526 (before the `<figure>` that follows):

```html
<div class="prop"><b>Proposition 3.1 (Terzaghi series).</b> Under a total stress $\sigma_0$ applied suddenly at $t=0$ to the confined layer of <a class="secref" href="#biphasic">§3</a>, with sealed base ($\partial p/\partial z=0$ at $z=0$) and drained platen ($p=0$ at $z=h$), the pore pressure is
$$p(z,t)=\sigma_0\sum_{n=0}^{\infty}\frac{2(-1)^{n}}{\lambda_n}\,\cos\!\big(\lambda_n Z\big)\,e^{-\lambda_n^{2}T},\qquad Z=\frac zh,\quad T=\frac{Dt}{h^{2}},\quad \lambda_n=\frac{(2n+1)\pi}{2}.$$</div>
<div class="proof"><b>Proof.</b> The pore pressure obeys the same diffusion equation as $u$ (boxed result above). Separate variables, $p=\sigma_0\,Z(z)\,e^{-D\mu^{2}t}$, so that $Z''+\mu^{2}Z=0$. The sealed base gives $Z'(0)=0$, selecting $Z=\cos(\mu z)$; the drained platen gives $Z(h)=0$, so $\cos(\mu h)=0$ and $\mu_n h=(2n+1)\pi/2\equiv\lambda_n$. The eigenfunctions $\cos(\lambda_n Z)$ are orthogonal on $Z\in[0,1]$ with $\int_0^1\cos^{2}(\lambda_n Z)\,\mathrm dZ=\tfrac12$. The initial condition is uniform, $p(z,0)=\sigma_0$, because no fluid has yet moved; its coefficients are therefore
$$a_n=\frac{\int_0^1\cos(\lambda_n Z)\,\mathrm dZ}{\int_0^1\cos^{2}(\lambda_n Z)\,\mathrm dZ}=\frac{(-1)^{n}/\lambda_n}{1/2}=\frac{2(-1)^{n}}{\lambda_n},$$
using $\int_0^1\cos(\lambda_n Z)\,\mathrm dZ=\sin\lambda_n/\lambda_n=(-1)^{n}/\lambda_n$. Each mode decays at its own rate $e^{-D\mu_n^{2}t}=e^{-\lambda_n^{2}T}$, which assembles the stated series. Setting $T=0$ recovers $p=\sigma_0$ at every depth; setting $Z=1$ gives $p=0$ at the platen for all $t$, as required. &#8718;</div>
```

Then replace line 596 with a version that averages a series the reader now has:

```html
<p>Proposition&nbsp;3.1 gives $p(z,t)$ explicitly. Averaging it over the depth term by term — each cosine contributes $\int_0^1\cos(\lambda_n Z)\,\mathrm dZ=(-1)^{n}/\lambda_n$, which cancels the $(-1)^{n}$ in the coefficient and leaves $2/\lambda_n^{2}$ — collapses every spatial factor and leaves a pure function of the dimensionless time $T=Dt/h^2$:</p>
```

Finally, D5 (line 1629 statement, line 1652 solution) now re-derives a result the text
owns. Retarget it so it is not a duplicate. Replace the D5 statement:

```html
<p>Proposition&nbsp;3.1 quotes the mode set for one-sided drainage without dwelling on why those boundary conditions and no others select it. Re-derive it: find the eigenfunctions and eigenvalues of the pressure diffusion problem from scratch, show that the depth-average of the series is $F(T)=\sum_n 2/\lambda_n^2\,e^{-\lambda_n^2T}$, and identify which single mode sets the gel time and why the others are invisible after one $\tau$.</p>
```

and append to the D5 solution, before `</div></details>`:

```html
<p>Why the other modes are invisible: mode $n$ decays as $e^{-\lambda_n^{2}T}$ with $\lambda_n^{2}=(2n+1)^{2}\pi^{2}/4$, so at $T=1$ the $n=1$ mode is down by $e^{-(9-1)\pi^{2}/4}=e^{-19.7}\approx3\times10^{-9}$ relative to $n=0$. After a fraction of a gel time the series is a single exponential; that is why $\tau=4h^{2}/(\pi^{2}D)$ is a sharp number and not a fitted one.</p>
```

### B2. K9's solution abandons the recovery fraction its own statement defines, and invents two constants

Location: `module04.html:2070` (statement), `module04.html:2089` (solution),
`module04.html:2090-2095` (code), `module04.html:2071` (figure caption).

Quoted (statement, line 2070): "If healthy tissue fully recovers each cycle but
degraded tissue recovers only a fraction $r\lt1$, show how peak $F$ evolves and
contrast the two after $20$ cycles."

Quoted (solution, line 2089): "a simple envelope is
$F_n=F_\infty+(F_0-F_\infty)e^{-n/N_c}$, with $F_\infty$ the drained floor. With
$F_0=0.97$, $F_\infty\approx0.15$, $N_c\approx22$..."

Three failures at once. (a) The recovery fraction `r` is introduced in the problem and
never appears in the solution; the reader is asked to model incomplete recovery and is
handed a formula in which incomplete recovery does not appear. (b) `F_inf = 0.15` and
`N_c = 22` are in none of the domain brief's three classes: not derived, not in the
Appendix parameter table, not labelled assumptions. `N_c = 22` in particular is a
fitted-looking constant chosen so that 20 cycles land on a dramatic number. (c) `F_0 =
0.97` matches no computed value in the module: section 4 gives 0.9862 at 1 s, K5 gives
0.9902 at 0.5 s, K1 gives 0.979. This is the most serious defect in the module, because
it is the one place where a number in a solution was manufactured rather than computed.

It is also the easiest to fix honestly, because the recurrence the statement asks for
has a clean closed form. Let `dF = 1 - F(t_load)` be the deficit one loading opens, and
let unloading recover a fraction `r` of the accumulated deficit. Then
`d_{n+1} = (1-r)(d_n + dF)`, whose fixed point is `d* = (1-r)dF/r`, so the peak
support settles at `F* = 1 - dF/r` exactly. Computed, with `t_load = 1 s`: healthy
(`k = 1e-15`, `r = 1`) gives `dF = 0.0138` and `F_n = 0.9862` flat; degraded
(`k = 100e-15`, `r = 0.8`) gives `dF = 0.1382`, `F_1 = 0.8618` and a plateau
`F* = 0.8273` reached by cycle 5. The steady-state deficit is exactly `dF/r`, so the
friction multiplier relative to a single step is exactly `1/r`: it doubles at
`r = 0.500` and is `5x` at `r = 0.2`. That closed form is the real lesson, and it is
the one that connects to D10: incomplete recovery alone gives a **bounded** offset, so
runaway needs `r` itself to fall with damage — which is exactly D10's `G > 1`.

Replacement for the K9 statement (line 2070):

```html
<p>Model repeated load/unload cycles by their fluid-support deficit. One loading of duration $t_{\rm load}$ opens a deficit $\Delta F=1-F(t_{\rm load})$; the following unloaded interval re-imbibes a fraction $r$ of the accumulated deficit, so $d_{n+1}=(1-r)\,(d_n+\Delta F)$ with $d_0=0$. <b>(a)</b> Solve the recurrence for the steady-state peak support $F_\infty$ in closed form. <b>(b)</b> Evaluate it for healthy tissue ($k=10^{-15}$, full recovery $r=1$) and for degraded tissue ($k=10^{-13}$, $r=0.8$), taking $t_{\rm load}=1\ \mathrm s$, $h=2\ \mathrm{mm}$, $H_A=0.6\ \mathrm{MPa}$, and contrast them at cycles $1$, $5$ and $20$. <b>(c)</b> Sweep $r$ and find the recovery fraction at which the steady-state friction $\mu_{\rm eff}=\mu_{\rm eq}(1-F_\infty)$ is twice its single-step value. <b>(d)</b> Say what this model does <em>not</em> predict, and what would have to change for it to.</p>
```

Replacement for the K9 solution and code (line 2089 onward, replacing the whole
`<details>`):

```html
<details class="sol"><summary>solution</summary><div><p><b>(a)</b> The recurrence $d_{n+1}=(1-r)(d_n+\Delta F)$ is affine with ratio $(1-r)$, so for $r\gt0$ it converges to the fixed point $d_*=(1-r)\Delta F/r$. The deficit <em>at peak load</em> in the steady state is $d_*+\Delta F=\Delta F\big[(1-r)/r+1\big]=\Delta F/r$, so $$\boxed{\;F_\infty=1-\frac{\Delta F}{r}\;}$$ Incomplete recovery multiplies the single-step deficit by exactly $1/r$ — and nothing more. The approach is geometric with ratio $(1-r)$, so for $r=0.8$ the plateau is reached to within $1\%$ by cycle $3$.</p><p><b>(b)</b> With $D=H_Ak$ and $T=Dt_{\rm load}/h^2$, the series gives $\Delta F=1-F(1\ \mathrm s)=0.0138$ for healthy tissue and $0.1382$ for the hundred-fold-more-permeable degraded tissue (the short-time law of D4 reproduces both exactly: $\Delta F=2\sqrt{T/\pi}$). Healthy tissue has $r=1$, so $d_*=0$ and $F_n=0.9862$ at every cycle — flat. Degraded tissue with $r=0.8$ starts at $F_1=0.8618$ and settles at $F_\infty=1-0.1382/0.8=0.8273$, reached by cycle $5$ and unchanged at cycle $20$.</p><p><b>(c)</b> Since the steady-state deficit is $\Delta F/r$ and the single-step deficit is $\Delta F$, the friction ratio $\mu_{\rm eff}^{\infty}/\mu_{\rm eff}^{(1)}$ is exactly $1/r$. It reaches $2$ at $r=0.500$ and $5$ at $r=0.2$: $F_\infty=0.7236$ ($\mu_{\rm eff}=0.042$) and $F_\infty=0.3090$ ($\mu_{\rm eff}=0.104$) respectively.</p><p><b>(d)</b> What this model does <em>not</em> predict is runaway. With $r$ fixed the deficit is bounded by $\Delta F/r$ however many cycles you run, so incomplete recovery alone produces a worse but <em>stable</em> joint. Runaway needs the loop of D10: the raised solid stress and friction must themselves degrade the matrix, lowering $r$ and raising $k$ on later cycles. That is the difference between a joint that is merely stiff and sore and one that is progressing — and it is why <a class="secref" href="#degeneration">§8</a>'s threshold is a statement about a gain, not about a number of steps.</p>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Copy</span></button><pre><code>import numpy as np

h, HA, mu_eq = 2e-3, 0.6e6, 0.15
lam = (2*np.arange(4000) + 1)*np.pi/2


def deficit(k, t=1.0):
    """1 - F(t): the support lost in one loading."""
    return 1 - np.sum(2/lam**2 * np.exp(-lam**2 * HA*k*t/h**2))


def cycles(k, r, n=20):
    """Peak support at the end of each of n load/unload cycles."""
    dF, d, out = deficit(k), 0.0, []
    for _ in range(n):
        out.append(1 - (d + dF))
        d = (1 - r)*(d + dF)
    return np.array(out)


for name, k, r in (("healthy ", 1e-15, 1.0), ("degraded", 1e-13, 0.8)):
    F = cycles(k, r)
    print(f"{name} dF={deficit(k):.4f}  F1={F[0]:.4f}  F5={F[4]:.4f} "
          f" F20={F[19]:.4f}  F_inf={1 - deficit(k)/r:.4f}")

print("\nsweep r -> steady-state support and friction")
dFd = deficit(1e-13)
for r in (1.0, 0.9, 0.8, 0.5, 0.2):
    Finf = 1 - dFd/r
    print(f"  r={r:.1f}  F_inf={Finf:.4f}  mu_eff={mu_eq*(1 - Finf):.4f}"
          f"  ({1/r:.2f}x the single-step value)")
# healthy  dF=0.0138  F1=0.9862  F5=0.9862  F20=0.9862  F_inf=0.9862
# degraded dF=0.1382  F1=0.8618  F5=0.8273  F20=0.8273  F_inf=0.8273
#   r=1.0  F_inf=0.8618  mu_eff=0.0207  (1.00x the single-step value)
#   r=0.5  F_inf=0.7236  mu_eff=0.0415  (2.00x the single-step value)
#   r=0.2  F_inf=0.3090  mu_eff=0.1036  (5.00x the single-step value)</code></pre></div></details></div>
```

Replacement for the K9 figure caption (line 2071), which currently states the invented
numbers:

```html
<figcaption><b>Incomplete recovery is bounded, not runaway.</b> Peak fluid support cycle by cycle. Healthy tissue ($r=1$) holds $F=0.9862$ indefinitely. Degraded tissue ($k=10^{-13}$, $r=0.8$) starts a step at $F=0.8618$ and settles onto the plateau $F_\infty=1-\Delta F/r=0.8273$ within about five cycles — worse, but stable. The dashed line is the closed-form plateau. Getting past it into runaway needs $r$ itself to fall as damage accumulates, which is D10's loop gain.</figcaption>
```

### B3. The module never places its models on the level ladder

Location: `module04.html:158-166` (the end of section 0).

`EDITOR_DOMAIN.md` requires each module to state which rung of the level ladder its
models sit on; `grep -i level module04.html` returns only the phrase "strain level" at
line 823 and a code comment. Module 1 (`module01.html:135`) and Module 2
(`module02.html:158`) both carry an explicit paragraph. Module 4 has none, so a reader
cannot tell that its contact section is a Level-1 statics result dressed in a field,
while its consolidation PDE is a genuine continuum-transport model, and that nothing
here is dynamic.

Insert after line 166 (the "By the end you will be able to..." paragraph):

```html
<p>Where this sits on the course's level ladder. Almost everything here is <b>Level 3</b> — a continuum field theory with a governing partial differential equation, solved in one spatial dimension: the consolidation equation of <a class="secref" href="#biphasic">§3</a>, its series solution in <a class="secref" href="#fluidload">§4</a>, and the finite-difference lab of <a class="secref" href="#relaxlab">§5</a> are all of that kind. Two sections sit lower on purpose. <a class="secref" href="#donnan">§2</a> is <b>Level 0</b>, a scalar equilibrium estimate with no space and no time in it. <a class="secref" href="#contact">§6</a> is <b>Level 1</b>: a static contact solution that takes the joint reaction of Module&nbsp;3 as a given load and returns a pressure distribution, with no inertia anywhere. Nothing in this module is dynamic — no term in any equation here contains an acceleration, and the quasi-static assumption that removes them is stated where it is used (<a class="secref" href="#biphasic">§3</a>, eq.&nbsp;5). The <b>Level 10</b> question this module opens and does not answer — how the chondrocyte reads these stresses and remodels the matrix — is named in <a class="secref" href="#synthesis">§9</a> and handed to Module&nbsp;14.</p>
```

### B4. The tipping point at the module's climax is asserted, its gain is never computed, and it carries two different symbols

Location: `module04.html:1183` (section 8, "Why it has a threshold"),
`module04.html:1733` and `module04.html:1756` (D10).

Quoted (line 1183): "Because the loop has a <b>gain</b>. Each pass multiplies the
damage by some factor $g$. Healthy cartilage keeps $g\lt1$: its fluid-support margin is
enormous ($F\approx0.99$ leaves vast headroom before the solid is overloaded)..."

Quoted (D10 solution, line 1756): "$$G=\frac{\partial(\text{damage})}{\partial(\downarrow
F)}\cdot\frac{\partial k}{\partial(\text{damage})}\cdot\frac{\partial(\text{stress})}
{\partial k}\cdot\frac{\partial(\downarrow F)}{\partial(\text{stress})}\cdots$$"

The module's dramatic conclusion — osteoarthritis has a tipping point — rests on a
quantity that is called `g` in section 8 and `G` in D10, is in neither the notation
table nor the parameter table, is never given a value, and whose defining formula
literally ends in an ellipsis. "Its fluid-support margin is enormous" is the
qualitative substitute for mechanics that the domain brief bans. This fails parts 1, 3
and 5 of the standard.

The module can compute one link of that loop exactly, and should say so rather than
gesture at all four. From D4, the short-time deficit is `1 - F = 2 sqrt(T/pi)` with
`T = H_A k t/h^2`, so `1 - F` is proportional to `sqrt(k)` and the log-sensitivity is
exactly `1/2`. I confirmed it numerically against the full series at `t = 1 s`: the
deficit runs 0.0138, 0.0437, 0.1382, 0.4369 for `k` at 1, 10, 100 and 1000 times
healthy — a ratio of 3.162 per decade, which is `sqrt(10)` to four figures.

Replacement for line 1183:

```html
<p>Why doesn't a healthy joint spiral like this on its own? Because the loop has a <b>gain</b>, and one of its links is computable from what this module has already built. Write the loop as a map on the fluid-support deficit $d=1-F$: extra permeability raises $d$, the extra solid stress and friction that follow abrade the matrix, and the abrasion raises the permeability again. In logarithmic variables the per-pass amplification is the product of the links' sensitivities, $$G=\underbrace{\frac{\partial\ln d}{\partial\ln k}}_{\text{this module}}\cdot\underbrace{\frac{\partial\ln(\text{wear rate})}{\partial\ln d}\cdot\frac{\partial\ln k}{\partial\ln(\text{wear})}}_{\text{assumed; Module 14}},$$ and a perturbation heals if $G\lt1$ and runs away if $G\gt1$ (D10).</p>
<p>The first factor is exact. The short-time law of D4 gives $d=2\sqrt{T/\pi}$ with $T=H_Akt/h^2$, so $d\propto\sqrt k$ and $$\frac{\partial\ln d}{\partial\ln k}=\frac12.$$ Checked against the full series at $t=1\ \mathrm s$, the deficit runs $0.0138\to0.0437\to0.1382\to0.4369$ as $k$ rises by factors of ten — a ratio of $3.162$ per decade, which is $\sqrt{10}$ to four figures. So the mechanical link <em>attenuates</em>: a decade of extra permeability buys only a $\sqrt{10}$-fold loss of support. That half-power is the whole margin. For the loop to close with $G\gt1$ the two biological links — how strongly lost support drives wear, and how strongly wear opens the matrix — must together supply a gain above $2$. This module cannot measure those; they are the mechanobiology of Module&nbsp;14, and they are assumptions here, not results.</p>
<p>Two consequences follow, and they are the reason the threshold is worth stating. First, the tipping point is not a critical permeability or a critical pressure — it is a condition on a <em>product of sensitivities</em>, so a joint can sit at a frankly degraded $k$ and still be stable, while another tips at a milder one because its biological links are steeper. Second, every intervention that works acts on a factor of $G$ rather than on the current state: unloading lowers the wear driven by a given deficit, and restoring charge and $F$ lowers the deficit itself. That is why intervention works best <em>early</em> — not because damage is small then, but because $G$ is still under one and the fluid-support margin can still be defended.</p>
```

Replacement for D10's gain formula and the sentence around it (line 1756, the second
paragraph of the solution):

```html
<p>The loop gain is the product of the sensitivities around the cycle, most naturally written in logarithmic variables so that each factor is a dimensionless elasticity: $$G=\frac{\partial\ln d}{\partial\ln k}\cdot\frac{\partial\ln(\text{wear rate})}{\partial\ln d}\cdot\frac{\partial\ln k}{\partial\ln(\text{wear})},\qquad d\equiv1-F.$$ Only the first factor belongs to this module, and it is exact: D4 gives $d=2\sqrt{H_Akt/(\pi h^2)}\propto\sqrt k$, so $\partial\ln d/\partial\ln k=\tfrac12$ (<a class="secref" href="#degeneration">§8</a> checks it against the full series). The remaining two are mechanobiological and are assumed, not derived, here; $G\gt1$ therefore requires them to supply a combined gain above $2$. Interventions — lower load, restore charge and $F$, reduce friction — all act by shrinking one factor of $G$ below what it was, which is why they work on the loop rather than on the current damage.</p>
```

Also unify the symbol: section 8 line 1183 now uses `G` throughout (done in the
replacement above), and both `G` and `d` get Appendix rows (B5).

### B5. Three symbol collisions, each recorded in the Appendix under one meaning only and none flagged

Location: `module04.html:315` and `module04.html:2166` (`T`), `module04.html:315`,
`module04.html:866-906`, `module04.html:2158` (`F`), `module04.html:98`,
`module04.html:963` (`W`).

- **`F` carries three meanings.** Line 315: "$F$ the Faraday constant". Lines 866 to
  929 and the section 6 table: "$F=R\approx1715\ \mathrm N$", "$p_0=\frac{3F}{2\pi
  a^2}$", "Same load $F=1715\ \mathrm N$". Line 2158 and everywhere in sections 4, 7, 8
  and eleven problems: `F(t)`, the fluid load support fraction. The Appendix records
  only the third. A reader meeting "$p_0=3F/(2\pi a^2)$" in section 6 has just spent
  section 4 learning that `F` is a dimensionless fraction.
- **`T` carries two.** Line 2166: "$R_g,\ T$ gas constant and absolute temperature".
  Line 2159: "$T$ dimensionless time, $T=Dt/h^2$". Both are listed in the same table,
  eight rows apart, with no cross-reference.
- **`W` carries two.** Line 98: "$R\approx2.5\,W$" and line 102 "$8$–$10\,W$", body
  weight. Line 963: "$S=\frac{\eta\,U}{W}$, viscosity times sliding speed over load".
  `W` appears in no Appendix row at all.

Section 2 already shows the module knows how to do this — it writes `R_g` "to keep it
distinct from the joint reaction $R$ of §0" — so the omission is inconsistency, not
oversight. The domain brief is explicit that flagging a collision is not resolving it.

Fixes, chosen to disturb the least text. The dimensionless time `T` appears in every
code block and in a dozen problem statements, so it keeps `T`; the temperature moves.
The fluid support fraction `F` is the module's signature symbol, so it keeps `F`; the
contact load and the Faraday constant move.

1. Section 2, line 315: replace `$T$ the absolute temperature` with `$\Theta$ the
   absolute temperature` and `$F$ the Faraday constant` with `$\mathcal F$ the Faraday
   constant`, propagating through lines 315 to 337 (`R_g T` becomes `R_g\Theta`,
   `F\Delta\psi` becomes `\mathcal F\Delta\psi`). The boxed result at line 330, the
   proof at 333, D2 at 1580, K2 at 1817 and 1842, and the Appendix rows follow.
2. Section 6, lines 866 to 929: the contact load becomes `R`, matching K3, which
   already writes `a=(3RR_{\rm eff}/4E^*)^{1/3}`. This removes the collision and makes
   section 6 and K3 agree symbol for symbol.
3. Section 7, line 963: the Stribeck denominator becomes `N` (normal load), matching
   D8, which already writes "The normal load $N$".
4. D7, line 1675: "a rigid sphere of effective radius $R$" becomes `R_{\rm eff}`, and
   the load `N` is kept.

Appendix additions (insert into the notation table after line 2166), and the `T` row
at 2159 gets a disambiguating clause:

```html
<tr><td>$\Theta$</td><td>absolute temperature ($310\ \mathrm K$); written $\Theta$, not $T$, because $T$ is the dimensionless time of <a class="secref" href="#fluidload">§4</a></td><td><a class="secref" href="#donnan">§2</a></td></tr>
<tr><td>$\mathcal F$</td><td>Faraday constant; written $\mathcal F$, not $F$, because $F$ is the fluid load support fraction</td><td><a class="secref" href="#donnan">§2</a></td></tr>
<tr><td>$W$</td><td>body weight ($\approx686\ \mathrm N$ for the $70\ \mathrm{kg}$ reference human); joint loads are quoted as multiples of it</td><td><a class="secref" href="#origin">§0</a></td></tr>
<tr><td>$N$</td><td>normal load across the contact (Stribeck number, friction law)</td><td><a class="secref" href="#lubrication">§7</a></td></tr>
<tr><td>$d,\ G$</td><td>fluid-support deficit $d=1-F$ and the degeneration loop gain</td><td><a class="secref" href="#degeneration">§8</a></td></tr>
```

### B6. C5 and K3 apply Hertz to the hip, which section 6 says three times you must not do

Location: `module04.html:1375` and `module04.html:1376` (C5 statement and caption),
`module04.html:1396` (C5 solution), `module04.html:1854-1856` and `module04.html:1876`
(K3).

Quoted (section 6, line 915): "the hip of <a class="secref" href="#origin">§0</a> is a
conforming ball-in-socket that wraps the load over a large congruent area, for which
Hertz badly under-predicts the contact area and over-predicts the peak. That is exactly
why the worked geometry here is the knee, with only the load magnitude carried over
from the hip."

Quoted (C5, line 1375): "A dry-elastic (Hertz) contact calculation <b>for the hip</b>
gives a peak pressure $p_0\approx2.5\ \mathrm{MPa}$."

Quoted (K3, line 1854): "<b>K3 — the hip contact patch.</b> ... The hip reaction is
$R=1715\ \mathrm N$ (Module 3). Model the contact as a sphere of effective radius
$R_{\rm eff}=30\ \mathrm{mm}$..."

Section 6 goes out of its way to explain that it uses a knee, names the hip as the case
Hertz gets wrong, and calls the choice deliberate. Two problems then do precisely what
it forbids and present the result as a success. K3's caption compounds it: "the mean
matches Module 3's force/area estimate exactly, an independent check". It is not
independent — `R_eff = 30 mm` is a chosen representative curvature, and section 6
itself calls the agreement "the same order", not "exact". (The computed mean is
1.694 MPa against Module 3's 1.7 MPa, so "exactly" is also an overstatement of a
two-figure agreement.)

Replacement for C5's statement (line 1375):

```html
<p>A dry-elastic (Hertz) contact calculation for the tibiofemoral (knee) contact of <a class="secref" href="#contact">§6</a> gives a peak pressure $p_0\approx2.5\ \mathrm{MPa}$. The real cartilage peak is lower and broader. Give two independent reasons the dry calculation overestimates the true peak, and say which of them would <em>also</em> apply, more strongly, to the conforming hip.</p>
```

Replacement for C5's figure caption (line 1376):

```html
<figcaption><b>Same load, two profiles.</b> The peaked dry-Hertz dome ($p_0\approx2.5\ \mathrm{MPa}$) and the broader biphasic profile ($\approx2.0\ \mathrm{MPa}$) carry the identical knee load $\int p\,\mathrm dA=R=1715\ \mathrm N$; the thin bonded layer and the plateau-like fluid pressurisation spread it wider and lower the peak.</figcaption>
```

Append to C5's solution (line 1396), before `</div></details>`:

```html
<p><b>Which applies to the hip.</b> Both, and the first far more strongly. The hip is a conforming ball-in-socket, so the surfaces are congruent over a large area before any load is applied; Hertz, which assumes two convex bodies touching at a point, under-predicts that area badly and over-predicts the peak correspondingly. That is why <a class="secref" href="#contact">§6</a> works the knee — a genuine convex-on-flat contact — and carries over only the load magnitude from Module&nbsp;3's hip.</p>
```

Replacement for K3's title, statement and caption (lines 1854 to 1856):

```html
<div class="qbox"><b>K3 &mdash; the knee contact patch.</b> <span class="small"><em>Probes: computing contact radius, peak and mean pressure, and testing them against Module&nbsp;3's force-over-area estimate (<a class="secref" href="#contact">§6</a>).</em></span>
<p>Carry the lower-limb joint reaction $R=1715\ \mathrm N$ (Module&nbsp;3) onto the tibiofemoral contact of <a class="secref" href="#contact">§6</a>: a condyle of effective radius $R_{\rm eff}=30\ \mathrm{mm}$ on cartilage of reduced modulus $E^*=6.67\ \mathrm{MPa}$. Compute <b>(a)</b> the contact radius $a=(3RR_{\rm eff}/4E^*)^{1/3}$, <b>(b)</b> the peak Hertz pressure $p_0=3R/(2\pi a^2)$, <b>(c)</b> the mean pressure $\bar p=R/(\pi a^2)$, and compare $\bar p$ with the Module&nbsp;3 estimate of $1.7\ \mathrm{MPa}$. <b>(d)</b> $R_{\rm eff}$ was chosen as a representative condylar curvature, not measured. Using D7's exponents, say how much $R_{\rm eff}$ would have to be wrong to move $\bar p$ by $20\%$, and hence how much the agreement in (c) is worth.</p>
<figure><svg viewBox="0 0 300 180" class="setupfig" role="img" aria-label="Hertz contact numbers for the knee"></svg><figcaption><b>Two routes to one mean pressure.</b> Hertz gives $a=18.0\ \mathrm{mm}$, $p_0=2.54\ \mathrm{MPa}$, $\bar p=1.69\ \mathrm{MPa}$ — the mean agrees with Module&nbsp;3's force-over-area estimate to two figures. Part (d) asks what that agreement does and does not establish.</figcaption></figure>
```

Append to K3's solution (line 1876), replacing its closing sentence:

```html
<p>The Hertz mean ($1.69\ \mathrm{MPa}$) agrees with the Module&nbsp;3 force-over-area estimate ($1.7\ \mathrm{MPa}$) to two figures. The peak is $\tfrac32\times$ the mean; the biphasic flattening of C5 brings the true peak down toward $\approx2.0\ \mathrm{MPa}$.</p><p><b>(d)</b> From D7, $a\propto R_{\rm eff}^{1/3}$ at fixed load, so $\bar p=R/(\pi a^2)\propto R_{\rm eff}^{-2/3}$. A $20\%$ change in $\bar p$ therefore needs $R_{\rm eff}$ to change by $1.2^{-3/2}=0.76$ or $0.8^{-3/2}=1.40$ — that is, a condylar radius of $23$ or $42\ \mathrm{mm}$ instead of $30$. Both are inside the real anatomical spread. So the agreement in (c) is a <em>consistency</em> check, not an independent confirmation: it says the two models are compatible given a plausible curvature, not that the curvature is right. The genuinely independent content of the Hertz calculation is the <em>shape</em> — the $\tfrac32$ peak-to-mean ratio, which follows from the cap alone and is untouched by $R_{\rm eff}$.</p>
```

### B7. D2's small-charge limit is wrong by a factor of two, and contradicts section 2's correct version

Location: `module04.html:1580` (D2 solution, final sentence).

Quoted (D2): "$\pi\approx R_gT\,c_F^2/(2c_0)$ grows quadratically for $c_F\ll c_0$ —
the rising curve of K2."

Quoted (section 2, line 384): "for $c_0\gg c_F$, expanding the root gives $\pi\approx
R_gT\,c_F^2/(4c_0)\to0$."

Section 2 is right and D2 is wrong. Expanding,
`pi = R_g T * 2c_0 (sqrt(1 + c_F^2/(4c_0^2)) - 1) ~ R_g T * 2c_0 * c_F^2/(8c_0^2) =
R_g T c_F^2/(4c_0)`. Checked numerically at `c_F = 0.01 M`, `c_0 = 0.15 M`: the exact
formula gives 429.44 Pa, the `4c_0` form gives 429.56 Pa, the `2c_0` form gives
859.11 Pa. D2 is off by exactly two.

The trailing clause is also wrong on its own terms: K2 evaluates two points,
`c_F = 0.2` and `0.1 M`, both of which are comparable to or larger than `c_0 = 0.15 M`,
so neither sits in the `c_F << c_0` regime this limit describes.

Replacement for D2's final sentence:

```html
<p><b>Check</b> the limits: $\pi\to0$ as $c_F\to0$ (an uncharged gel does not swell), and for $c_F\ll c_0$ expanding the root gives $\pi=2R_g\Theta c_0\big[\sqrt{1+c_F^2/(4c_0^2)}-1\big]\approx R_g\Theta\,c_F^2/(4c_0)$ — quadratic in the fixed charge, matching <a class="secref" href="#donnan">§2</a>. (At $c_F=0.01\ \mathrm M$, $c_0=0.15\ \mathrm M$ the exact formula gives $429.4\ \mathrm{Pa}$ and this limit $429.6\ \mathrm{Pa}$.) The healthy operating point $c_F=0.2\ \mathrm M$ is <em>not</em> in that regime — it sits above $c_0$ — which is why K10 finds a local slope of $1.83$ there rather than the asymptotic $2$.</p>
```

### B8. K10 is two divisions, which the course's own standard calls busywork

Location: `module04.html:2097-2098` (statement), `module04.html:2123` (solution),
`module04.html:2123-2127` (code).

Quoted (statement): "Cartilage tensile modulus is $E_{\rm tens}\approx12\
\mathrm{MPa}$, compressive aggregate modulus $H_A\approx0.6\ \mathrm{MPa}$, swelling
pre-stress $\pi\approx0.16\ \mathrm{MPa}$. (a) Compute the tension/compression
stiffness ratio. (b) What fraction of the extra effective stress at $10\%$ compression
does the swelling pre-stress represent?"

The whole code block is `print(E_tens/HA)` and `print(pi/(HA*0.1))`. `EDITOR_DOMAIN.md`
is explicit: a computational problem must require numerical integration, optimization,
an inverse problem, a sensitivity sweep, or a regime comparison, and "a
plug-the-numbers-into-the-box problem is busywork at this level and is a defect". K10
is three constants and two divisions, and both answers are already printed in its own
figure caption.

Replace it with the inverse problem the module has been setting up since section 2 and
never asks: at what fixed-charge density does the swelling pre-stress stop dominating
the compressive response? This is a root-find plus a log-sensitivity sweep, it gives
K2's asserted "steeper than linear" an actual number, and it lands on section 8's
cascade. Computed: `pi(0.2 M) = 0.1561 MPa`; `pi = H_A * 0.10 = 0.060 MPa` at
`c_F = 0.1205 M`, which is 60 % of healthy; the local log-slope `dln(pi)/dln(c_F)` is
1.832 at 0.2 M, 1.949 at 0.1 M, 1.986 at 0.05 M.

Replacement for the K10 statement (lines 2097-2098):

```html
<div class="qbox"><b>K10 &mdash; how much charge can cartilage afford to lose?</b> <span class="small"><em>Probes: inverting the Donnan formula for a mechanical criterion, and measuring the amplification K2 asserts (<a class="secref" href="#donnan">§2</a>, <a class="secref" href="#degeneration">§8</a>).</em></span>
<p>The resting swelling pre-stress $\pi(c_F)=R_g\Theta(\sqrt{c_F^2+4c_0^2}-2c_0)$ is what keeps the matrix turgid; the extra effective stress needed to squeeze the drained matrix by a strain $\varepsilon$ is $H_A\varepsilon$. Call the tissue <em>pre-stress-dominated</em> while $\pi\gt H_A\varepsilon$. With $c_0=0.15\ \mathrm M$, $\Theta=310\ \mathrm K$, $H_A=0.6\ \mathrm{MPa}$: <b>(a)</b> verify that healthy cartilage ($c_F=0.2\ \mathrm M$) is pre-stress-dominated at $\varepsilon=0.10$, and by what factor. <b>(b)</b> Solve $\pi(c_F)=H_A\varepsilon$ numerically for the critical fixed-charge density $c_F^{\rm crit}$ at $\varepsilon=0.05,\,0.10,\,0.15$, and express each as a percentage of healthy. <b>(c)</b> Compute the logarithmic sensitivity $\partial\ln\pi/\partial\ln c_F$ at $c_F=0.2,\,0.1,\,0.05\ \mathrm M$, and reconcile the answer with D2's asymptotic limit and with K2's claim that the dependence is "steeper than linear". <b>(d)</b> Interpret: does losing charge degrade the tissue gracefully or abruptly?</p>
```

Replacement for the K10 solution and code:

```html
<details class="sol"><summary>solution</summary><div><p><b>(a)</b> $\pi(0.2\ \mathrm M)=0.1561\ \mathrm{MPa}$ against $H_A\varepsilon=0.6\times0.10=0.060\ \mathrm{MPa}$: the resting pre-stress is $2.60\times$ the stress a $10\%$ squeeze adds. Healthy cartilage is comfortably pre-stress-dominated — it is a pre-loaded structure, not a slack one.</p><p><b>(b)</b> Root-finding $\pi(c_F)=H_A\varepsilon$ (the function is monotone, so a bisection converges immediately): $c_F^{\rm crit}=0.0844\ \mathrm M$ at $\varepsilon=0.05$ ($42\%$ of healthy), $0.1205\ \mathrm M$ at $\varepsilon=0.10$ ($60\%$), $0.1489\ \mathrm M$ at $\varepsilon=0.15$ ($74\%$). Against a $10\%$ working strain, the tissue crosses out of pre-stress dominance having lost only $40\%$ of its fixed charge — well inside the range K2's degeneration scenario covers.</p><p><b>(c)</b> $\partial\ln\pi/\partial\ln c_F=1.832$ at $c_F=0.2\ \mathrm M$, $1.949$ at $0.1\ \mathrm M$, $1.986$ at $0.05\ \mathrm M$. The exponent rises toward $2$ as $c_F$ falls, which is exactly D2's asymptotic limit $\pi\approx R_g\Theta c_F^2/(4c_0)$ reasserting itself once $c_F\ll c_0$. K2's "steeper than linear" is correct and now has a number: near the operating point the elasticity is $1.83$, so halving the charge costs a factor $2^{1.83}\approx3.6$ of swelling pressure — the $73\%$ loss K2 computes.</p><p><b>(d)</b> Abruptly, and worse than abruptly: the sensitivity <em>increases</em> as the tissue degrades. The first $10\%$ of charge lost costs about $18\%$ of the pre-stress; by the time half is gone each further increment costs nearly the square. A tissue losing charge slides down a curve that steepens under it, which is the osmotic half of <a class="secref" href="#degeneration">§8</a>'s loop, and it is why the swelling pre-stress is the strut that fails first.</p>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Copy</span></button><pre><code>import numpy as np
from scipy.optimize import brentq

RgT, c0, HA = 8.314*310, 0.15, 0.6e6      # J/mol, M, Pa


def pi(cF):
    """Donnan swelling pressure [Pa] for fixed charge cF in mol/L."""
    return RgT*(np.sqrt(cF**2 + 4*c0**2) - 2*c0)*1e3


print(f"(a) pi(0.2 M) = {pi(0.2)/1e6:.4f} MPa  vs  HA*0.10 = "
      f"{HA*0.10/1e6:.3f} MPa  -> ratio {pi(0.2)/(HA*0.10):.2f}")

print("(b) critical fixed charge where pi = HA*eps")
for eps in (0.05, 0.10, 0.15):
    cc = brentq(lambda c: pi(c) - HA*eps, 1e-4, 1.0)
    print(f"    eps={eps:.2f}: cF_crit={cc:.4f} M  ({cc/0.2*100:.0f}% of healthy)")

print("(c) logarithmic sensitivity d ln(pi) / d ln(cF)")
for cF in (0.2, 0.1, 0.05):
    dc = 1e-6
    s = (np.log(pi(cF + dc)) - np.log(pi(cF - dc))) / \
        (np.log(cF + dc) - np.log(cF - dc))
    print(f"    cF={cF:.2f} M: {s:.3f}")
# (a) pi(0.2 M) = 0.1561 MPa  vs  HA*0.10 = 0.060 MPa  -> ratio 2.60
# (b)     eps=0.05: cF_crit=0.0844 M  (42% of healthy)
#         eps=0.10: cF_crit=0.1205 M  (60% of healthy)
#         eps=0.15: cF_crit=0.1489 M  (74% of healthy)
# (c)     cF=0.20 M: 1.832
#         cF=0.10 M: 1.949
#         cF=0.05 M: 1.986</code></pre></div></details></div>
```

Replacement for the K10 figure caption (line 2098):

```html
<figcaption><b>The curve steepens as it falls.</b> Swelling pre-stress $\pi(c_F)$ against the $H_A\varepsilon=0.06\ \mathrm{MPa}$ needed for a $10\%$ squeeze. Healthy cartilage sits $2.6\times$ above the line; the crossing is at $c_F=0.12\ \mathrm M$, only $60\%$ of healthy. The local log-slope rises from $1.83$ at the operating point toward $2$ as charge is lost, so each further loss costs more than the last.</figcaption>
```

### B9. Section 5's peak-ratio scaling is asserted with a tilde beside two proved siblings, and its exact constant is available

Location: `module04.html:816-821`.

Quoted (line 821): "The peak, by contrast, is <em>not</em> a fixed material number: it
scales as $\sigma_{\rm peak}/\sigma_\infty\sim h/\sqrt{D\,t_0}$ — ramp faster (smaller
$t_0$) and the fluid is trapped harder, so the spike is taller."

Quoted (line 816): "Two independent checks that the simulation is right, not merely
plausible".

Section 3's gel time and section 6's Hertz radius both get full derivations. This
scaling — the third quantitative claim the lab makes, and the one describing the most
visible feature of its own figure — gets a tilde and no constant, so the reader cannot
check it and the lab claims only two validations when three are available. This is the
sibling-keyresult case the domain brief says no script catches.

The constant follows from the same similarity solution D4 already uses. During the
ramp the surface strain is the drained strain concentrated into the diffusion boundary
layer of depth `sqrt(pi D t0)/2`, giving
`sigma_peak/sigma_inf = 2h/sqrt(pi D t0)`. Evaluated for the lab's parameters
(`h = 2 mm`, `D = 6e-10`, `t0 = 200 s`) this is **6.5147**. I re-ran the module's own
solver at three grid resolutions: `N = 50` gives 6.4941 (the value the lab prints),
`N = 100` gives 6.5117, `N = 200` gives 6.5140. The finite-difference peak converges to
the analytic constant, so this is a genuine third check and the printed 6.494 is a
2-node discretisation error, not a discrepancy.

Replacement for lines 816 to 821 (the two-check list and the paragraph after it):

```html
<p>Three independent checks that the simulation is right, not merely plausible — the kind of validation a model owes you:</p>
<ol>
<li>the equilibrium the curve settles to equals $H_A\varepsilon_0$ <em>exactly</em> — the finite-difference scheme returns the drained modulus we put in;</li>
<li>the relaxation timescale matches the closed-form gel time $\tau=h^2/(H_Ak)=6.7\times10^3\ \mathrm s$ from <a class="secref" href="#biphasic">§3</a>, with no fitting parameter;</li>
<li>the height of the peak matches the analytic ramp estimate below, to within the discretisation error of the grid.</li>
</ol>
<p>The peak, unlike the equilibrium, is <em>not</em> a fixed material number — it belongs to the loading, and it has a closed form. During a ramp short against $\tau$, only a diffusion boundary layer near the platen has drained; by the similarity solution of D4 its depth is $\sqrt{\pi Dt_0}/2$, and the whole imposed displacement $\varepsilon_0h$ is taken up across it. The surface strain is therefore $\varepsilon_0h$ divided by that depth, so</p>
$$\frac{\sigma_{\rm peak}}{\sigma_\infty}\;\simeq\;\frac{2h}{\sqrt{\pi D\,t_0}}.$$
<p>For the lab's parameters ($h=2\ \mathrm{mm}$, $D=6\times10^{-10}\ \mathrm{m^2/s}$, $t_0=200\ \mathrm s$) this is $6.515$. The solver prints $6.494$ on the $N=50$ grid of the code above; refining to $N=100$ and $N=200$ gives $6.512$ and $6.514$, converging on the analytic value. So the spike is not a numerical artefact and not a material property: ramp faster (smaller $t_0$) and the ratio grows as $t_0^{-1/2}$, because the fluid is trapped in a thinner layer. The equilibrium is the material; the peak is the loading rate, and the exponent $-\tfrac12$ is the diffusion signature of D4 seen once more.</p>
```

### B10. Roughly a dozen empirical numbers belong to none of the three admissible classes

Location: `module04.html:102`, `:179`, `:681`, `:924`, `:995`, `:1026`, `:1051`,
`:1055`, `:1416`.

The domain brief allows a number to be derived, a parameter with a symbol and unit in a
table, or an assumption labelled as such. These are none of the three:

- Line 1026, the Stribeck model constants: `mu_bl, S0, alpha = 0.15, 0.5, 0.012`. These
  three numbers *are* the section 7 Stribeck figure — they set the computed boundary
  plateau of 0.15 and the minimum of 0.03 at `S = 1.77` that the figure labels and the
  prose quotes at line 1014 ("thirty times what cartilage actually shows"). `S_0` and
  `alpha` appear nowhere but inside the code, with no units, no table row and no
  justification. The module's most rhetorically important comparison rests on them.
- Line 102: "$\mu\approx0.03$ of an ice skate on ice"; "hip forces reach $8$–$10\,W$".
- Line 681 and repeated at line 924: "direct measurements with pressure transducers in
  loaded cartilage find interstitial fluid sustaining $85$–$95\%$ of the load".
- Line 1416 and the C6 figure: "$E_{\mathrm{tens}}\sim10$–$15\ \mathrm{MPa}$" against
  the Appendix's single `E_tens ≈ 12 MPa`.
- Line 179: collagen "$50$–$75\%$ of the tissue's dry weight"; proteoglycans "$15$–
  $30\%$ of dry weight" — dry-weight fractions with no dry-weight row anywhere.

Per the domain brief I have added no citation and repaired none: the transducer
measurement and the ice figure stay in the prose as stated, but are labelled as
external empirical values the module does not derive, and the model constants get
labelled as the fitted choices they are. Add these rows to the parameter table after
line 2218:

```html
<tr><td colspan="4" class="grp">Lubrication model constants (chosen to fit the classical curve; <a class="secref" href="#lubrication">§7</a>)</td></tr>
<tr><td>boundary friction plateau</td><td>$\mu_{\rm bl}$</td><td>$0.15$ (assumed = $\mu_{\rm eq}$)</td><td><a class="secref" href="#lubrication">§7</a></td></tr>
<tr><td>Stribeck transition</td><td>$S_0$</td><td>$0.5$ (assumed)</td><td><a class="secref" href="#lubrication">§7</a></td></tr>
<tr><td>hydrodynamic slope</td><td>$\alpha$</td><td>$0.012$ (assumed)</td><td><a class="secref" href="#lubrication">§7</a></td></tr>
<tr><td colspan="4" class="grp">External empirical values (quoted, not derived here)</td></tr>
<tr><td>measured fluid load support</td><td>&mdash;</td><td>$85$–$95\%$ under cyclic load</td><td><a class="secref" href="#fluidload">§4</a></td></tr>
<tr><td>ice on ice, for comparison</td><td>&mdash;</td><td>$\mu\approx0.03$</td><td><a class="secref" href="#origin">§0</a></td></tr>
<tr><td>peak hip load, stumble/jump</td><td>&mdash;</td><td>$8$–$10\,W$</td><td><a class="secref" href="#origin">§0</a></td></tr>
<tr><td>dry-weight fractions</td><td>&mdash;</td><td>collagen $50$–$75\%$, proteoglycan $15$–$30\%$</td><td><a class="secref" href="#composite">§1</a></td></tr>
```

And label the model constants where they are used. Replace line 995:

```html
<p>A compact model captures the first three: $\mu(S)=\mu_{\rm bl}/\big(1+(S/S_0)^2\big)+\alpha S$ — a boundary term $\mu_{\rm bl}$ that rules when slow/heavy, plus a hydrodynamic term $\alpha S$ that rules when fast/light. The three constants are <em>assumed</em>, not measured here: we take $\mu_{\rm bl}=0.15$ (the intrinsic drained friction $\mu_{\rm eq}$ of the boxed law below, so that the two models share one boundary value), and choose $S_0=0.5$ and $\alpha=0.012$ to put the film minimum near $\mu\approx0.03$ — a representative engineered bearing. Nothing in the argument depends on their exact values; what matters is the <em>shape</em>, and specifically that the curve rises at low $S$. Compute it:</p>
```

Replace the second sentence of line 681 to mark the measurement as external:

```html
<p>Loading and recovery together keep $F$ high indefinitely. This is not just theory: direct measurements with pressure transducers in loaded cartilage find interstitial fluid sustaining $85$–$95\%$ of the load through normal cyclic activity. That figure is quoted from the experimental literature, not derived here (the repo holds no source to check it against); it is an independent check on the picture equation&nbsp;(1) draws, and equation&nbsp;(1)'s own prediction for a footstep, $F=0.986$, sits just above it as it should, since a transducer averages over the whole cycle including the unloaded phase.</p>
```

### B11. The water fraction is given as three different ranges in three places

Location: `module04.html:181`, `module04.html:239` (table), `module04.html:256`,
`module04.html:2220` (Appendix).

- Line 181: "Interstitial water: $65$–$80\%$ of the tissue by wet weight".
- Line 239 (the section 1 table): "Water + mobile ions $\approx65$–$80\%$".
- Line 256 (the boxed idealisation): "with typically $\varphi^w\approx0.75$–$0.80$".
- Line 2220 (the Appendix parameter table): "water $\varphi^w$ $\approx 70$–$80\%$".

Three ranges for one parameter, and the Appendix — which the domain brief makes the
authority — agrees with none of the other two. A text-versus-table mismatch is a
factual error by the brief's rule. Unify on the widest defensible statement, which is
the one section 1 makes twice, and let the boxed idealisation state the narrower
load-bearing-zone value as the sub-range it is.

Replace line 256's parenthetical:

```html
$$\varphi^s+\varphi^w=1,\qquad \text{with typically }\varphi^w\approx0.65\text{–}0.80.$$
```

Replace the Appendix row at line 2220:

```html
<tr><td>water</td><td>$\varphi^w$</td><td>$\approx 65$–$80\%$</td><td><a class="secref" href="#composite">§1</a></td></tr>
```

### B12. The two flattened-peak numbers cannot be reproduced from anything the text states

Location: `module04.html:927` and `module04.html:929` (section 6),
`module04.html:1151` (section 8).

Quoted (line 927): "A load-conserving estimate — the same $F$ spread over a $\sim30\%$
wider patch — cuts the peak from the Hertzian $2.5\ \mathrm{MPa}$ toward $\approx2.0\
\mathrm{MPa}$".

Quoted (line 1151): "the same $1715\ \mathrm N$ concentrates into a high, narrow peak
(dark, $\approx3.2\ \mathrm{MPa}$) on a smaller, already-damaged patch. Both curves
carry the identical load".

The figures are correct — I integrated all four polylines and they carry 1706, 1701,
1702 and 1710 N against a target of 1715 N. But the prose gives the reader no way to
get there. A 30 % wider patch reduces a *Hertz cap* to 1.50 MPa, not 2.0; 2.0 MPa
requires the profile to change shape as well as width, and the text never says to what.
Reading the drawn curves back: the biphasic profile is a parabola `p = p_max
(1 - (r/a')^2)` at `a' = 23.2 mm` (which is `1.29 a`, the "30 % wider"), for which load
conservation gives `p_max = 2F/(pi a'^2) = 2.00 MPa` exactly. The section 8 degenerate
curve is a Hertz cap: reading the polyline back gives `a = 15.73 mm` and a drawn
peak of 3.25 MPa, and `p_0 = 3R/(2 pi a^2)` reproduces the figure's own `3.2 MPa`
label at `a ~ 16 mm`, which is the value the applied caption quotes. Both are right; neither is stated. This fails part 3 — a reader must be able
to reproduce every line with a pen.

Replacement for line 927:

```html
<p>Put a number on it. Keep the load fixed at $F$ and let the fluid pressurisation change the profile's <em>shape</em> as well as its width: replace the Hertzian cap $p\propto\sqrt{1-(r/a)^2}$ with the flatter parabola $p=p_{\max}\big(1-(r/a')^2\big)$, which has the plateau-like interior that a broad pressure field produces. Load conservation then fixes the peak, since $\int_0^{a'}p\,2\pi r\,\mathrm dr=\tfrac12\pi a'^2p_{\max}$, giving $p_{\max}=2F/(\pi a'^2)$ — note the factor $2$ where the cap gave $\tfrac32$. Spreading the contact by $30\%$ ($a'=1.3a=23.3\ \mathrm{mm}$) therefore yields $p_{\max}=2(1715)/(\pi\cdot0.0233^2)=2.0\ \mathrm{MPa}$, against the Hertzian $2.5\ \mathrm{MPa}$, with the edges correspondingly lifted (blue curve). The real joint runs gentler than the elastic estimate, and it does so by changing the shape of the pressure field, not merely its footprint.</p>
```

Replacement for the section 8 caption (line 1151):

```html
<figcaption><b>Same load, redistributed.</b> With fluid support intact the load spreads into a low, flat parabolic pressure (blue, $p_{\max}=2.0\ \mathrm{MPa}$ over $a'=23.3\ \mathrm{mm}$, <a class="secref" href="#contact">§6</a>); once it is lost the profile reverts to a Hertzian cap on a contact shrunk by wear to $a\approx16\ \mathrm{mm}$, and the same $1715\ \mathrm N$ concentrates into $p_0=3R/(2\pi a^2)=3.2\ \mathrm{MPa}$ (dark). Both curves integrate to the identical $1715\ \mathrm N$ — degeneration does not add force, it <em>focuses</em> it.</figcaption>
```

### B13. K4's code confirms neither of the two things K4 asks for, and two code comments state numbers the code does not print

Location: `module04.html:1885` (statement), `module04.html:1902-1918` (K4 code),
`module04.html:2033` (K7 code comment).

Quoted (K4 statement): "Confirm the stress decays from an undrained peak to
$\sigma_\infty=H_A\varepsilon_0$ over a few $\tau$, and that the relaxation time scales
as $h^2$."

K4's code prints one line: `tau=6667 s; mean p after 3*tau = 0.000`. It never computes
a stress, so it cannot confirm the decay to `H_A eps0`; it never varies `h`, so it
cannot confirm the `h^2` scaling. The figure caption ("doubling $h$ shifts the curve
right by $4$ in real time") is unsupported by the code beneath it. Its final comment
reads `# tau=6667 s; mean p after 3*tau = 0.0xx` — a literal placeholder that was never
replaced with the run's output.

K7's comment (line 2033) reads `# eps_inf=0.50 T90=0.848 t90=5653 s = 1.57 h`. Running
it prints `t90=5654 s`. The exact value is 5653.9 s, so the comment rounded down where
the code rounds to nearest. Section 9 line 1257 promises "the computational solutions
carry Python-verified numbers"; a comment that disagrees with its own block's output
breaks that promise, however narrowly.

Replacement for K4's code block:

```html
<pre><code>import numpy as np

h0, HA, k, eps0 = 2e-3, 0.6e6, 1e-15, 0.10
D = HA*k
# ONE fixed time step in seconds, used at every h, so that the three runs
# below are genuinely different computations and not one rescaled.
DT = 0.4*(1e-3/60)**2/D


def relax(h, N=60, ncycle=3.0):
    """Confined relaxation at held strain eps0: (t, sigma, tau)."""
    tau = h**2/D
    dz = h/N
    r = D*DT/dz**2          # 0.4, 0.1, 0.025 for h = 1, 2, 4 mm; all &lt;= 1/2
    p = np.ones(N + 1)      # uniform initial pressure (undrained)
    p[-1] = 0.0             # drained top face
    t, sig = [], []
    for n in range(int(ncycle*tau/DT) + 1):
        t.append(n*DT)
        # total stress = drained elastic stress + mean pore pressure,
        # both referred to the held strain eps0
        sig.append(HA*eps0*(1.0 + p.mean()))
        lap = p[2:] - 2*p[1:-1] + p[:-2]
        p[1:-1] += r*lap
        p[0] = p[1]         # sealed base: zero flux (mirror node)
        p[-1] = 0.0
    return np.array(t), np.array(sig), tau


# (i) the stress decays from an undrained peak to HA*eps0
t, sig, tau = relax(h0)
print(f"tau={tau:.0f} s  sigma_peak={sig[0]/1e6:.3f} MPa  "
      f"sigma_end={sig[-1]/1e6:.4f} MPa  HA*eps0={HA*eps0/1e6:.4f} MPa")

# (ii) the relaxation time scales as h^2
print("h (mm)   t_half (s)   t_half / h^2")
for h in (1e-3, 2e-3, 4e-3):
    t, sig, tau = relax(h)
    half = sig[-1] + 0.5*(sig[0] - sig[-1])
    th = t[np.argmax(sig &lt;= half)]
    print(f"  {h*1e3:.0f}      {th:8.1f}      {th/h**2:.4e}")
# tau=6667 s  sigma_peak=0.119 MPa  sigma_end=0.0600 MPa  HA*eps0=0.0600 MPa
# h (mm)   t_half (s)   t_half / h^2
#   1         333.5      3.3352e+08
#   2        1334.1      3.3352e+08
#   4        5336.3      3.3352e+08</code></pre>
```

(The `t_half / h^2` column is the $h^2$ law. The three runs share ONE time step in
seconds, so they are genuinely different computations (Courant number 0.4, 0.1,
0.025) rather than one rescaled run, and the column is still constant to five figures.
The prior report's 499 / 1995 / 7981 s and 4.988e+08 do not reproduce; see the
corrections note at the end.)


Replacement for K7's comment line (line 2033):

```
# eps_inf=0.50  T90=0.848  t90=5654 s = 1.57 h
```

## 3. Style and clarity edits

**S1. Section 2's worked arithmetic does not reproduce with a pen.** Line 336 rounds
the root to 361 and the excess to 61 mol/m³, then line 337 writes "$\pi = 2577\times61
\approx 1.56\times10^5$". But `2577 x 61 = 157197`, i.e. `1.57e5`. The 1.56e5 comes
from the unrounded 60.555, which the display has already thrown away. D2 at line 1580
does it correctly with 60.6. Make section 2 match D2. Replace lines 336-337:

```html
$$\sqrt{200^2+4(150)^2}=\sqrt{1.30\times10^5}=360.6\ \mathrm{mol/m^3},\qquad 360.6-300=60.6\ \mathrm{mol/m^3},$$
$$\pi = 2577\times60.6 \approx 1.56\times10^5\ \mathrm{Pa} \approx 0.16\ \mathrm{MPa}.$$
```

**S2. Line 1020's multiplication gives a different answer from the one printed.**
"$\mu_{\rm eff}\approx0.15\times0.01\approx0.002$" — the shown product is 0.0015. The
0.002 is the correct value for a 1 s footstep (`F = 0.9862`), so the factor is wrong,
not the answer. Replace:

```html
<p>with $F(t)$ the fluid load support fraction of <a class="secref" href="#fluidload">§4</a>. During a $1\ \mathrm s$ footstep $F=0.986$, so $\mu_{\rm eff}=0.15\times0.014=0.0021$ — the measured value — and it needs <em>no sliding speed at all</em>. Cartilage is slippery not because a film floats the surfaces, but because the fluid inside it carries the load. Both curves come from one short program:</p>
```

**S3. The module uses two footstep durations without saying so.** Section 4 (line 631)
and section 8 use `t_load = 1 s`, giving `F = 0.986`; K1, K5, K6 and blocks 7 and 8 use
0.5 s, giving `F = 0.990`. Both are defensible but the reader meets 0.986, 0.990 and
"~0.99" for the same event. Add to the section 4 paragraph at line 631, after the first
sentence: `(A footstep is stance phase, not the whole gait cycle; the problems use
$0.5\ \mathrm s$ for a brisk walk, which changes $F$ only in the third decimal, from
$0.986$ to $0.990$.)`

**S4. Section 8's summary table quotes a friction the module does not compute.** Line
1176: "friction $\mu_{\rm eff}$ | $\sim0.005$ | rises (toward $0.1$) | §7". Section 7
computes `mu_eff = 0.0021`; `0.005` is the low end of the *measured* range at line 1051.
The "from" column says §7, so it should carry §7's number. Replace the cell value with
`$\sim0.002$ (computed; $0.005$–$0.02$ measured)`.

**S5. Four code comments carry live `<a>` anchors** (lines 728, 757, 1034, 1038). These
are artefacts of `autolink_sections.py` matching "§3" and "§4" inside `<code>`. They are
harmless to the reader — `code.textContent` strips tags, so the copy button yields
`# gel time (§3)` — but stripping the tag alone will be undone by the next autolink
run. Change the comment *text* so there is no `§N` to match: `# consolidation
diffusivity [m^2/s], section 3`, `# explicit update of every interior node -- the
discretized PDE of section 3`, `# gel time (section 3) ~ 6667 s`, `# fluid support,
section 4`.

**S6. The `<summary>` labels are mixed.** `check_svg` reports both "Answer" and
"solution" in use. The diagnostics use `answer`, the 30 problems use `solution`.
Unify the five diagnostics to `solution`.

**S7. Section 6 line 910 overstates a two-figure agreement.** "matching its contact
area and mean pressure — reassuring" reads as confirmation; with `R_eff` chosen it is
consistency. Replace "matching its contact area and mean pressure" with "consistent
with its contact area and mean pressure, given a plausible condylar radius (K3(d)
quantifies how much that agreement is worth)".

**S8. C6's tensile modulus range and the Appendix's point value differ.** Line 1416
gives `10–15 MPa`, the C6 figure and K10 give 12 MPa, the Appendix gives 12 MPa. Make
line 1416 read `$E_{\mathrm{tens}}\approx12\ \mathrm{MPa}$ (Appendix; the reported
range is $10$–$15$)`.

**S9. Hedging and filler.** Line 158: "That one mechanism organizes everything that
follows" is a promise the paragraph then keeps — keep it. But line 507's "Everything in
the rest of the module ... is this diffusion equation seen from a different angle" and
line 1196's "Almost everything in this module radiates from the single governing
equation" say the same thing twice, 700 lines apart, and line 1196 is immediately
followed by a figure making the point a third time. Cut the sentence at 1196 to "Six
phenomena, one equation:".

**S10. Line 102 ends on a flourish that adds nothing.** "A soft, thin, living gasket
that out-performs steel-on-PTFE and never gets a service interval: that is the object
of this module." "steel-on-PTFE" is undefined and the comparison is unquantified.
Replace with: "A soft, thin, living gasket that carries these pressures for decades,
with a friction coefficient six times lower than ice on ice and no service interval:
that is the object of this module."

**S11. Six figures have oversized viewBoxes** (`check_frame` advisory, all under the
hard threshold): the confined-compression figure wastes 21 % on the left, the
effective-stress partition 30 %, the control-slab figure 29 %. Tighten to the values
`check_frame` suggests. Advisory only; applied.

## 4. Structural notes

**The problem set is front-loaded onto two ideas.** Of thirty problems, C1, C3, C7, C9,
D1, D3, D4, D5, D6, D9, K1, K4, K5, K7 and K8 — half the set — test the consolidation
equation and its timescale. Meanwhile section 6 (contact) gets C5, D7 and K3; section 7
(lubrication) gets C4, D8 and K6, and both of those are one-line applications of the
same partition. Nothing anywhere tests the Stribeck curve the module spends a third of
section 7 building, and nothing tests the shear-thinning synovial fluid or the boundary
lubricants at all. The gel time is the module's best idea and it is over-examined; the
lubrication section is under-examined relative to its length. If a future pass trims,
K8 (four divisions of `h^2/D`) is the most redundant with D6 and C9.

**Section 3's two definitions of the gel time are never reconciled in one place.** The
tables use `tau = h^2/D = 6667 s`; D1 and D5 use `tau_1 = 4h^2/(pi^2 D) = 2702 s`;
line 575 notes the factor in a parenthesis and moves on. Both are used freely
afterwards. A one-line convention statement in the section 3 gel-time box ("we use the
scaling estimate `h^2/D` for all quoted values; the exact slowest-mode constant
`4/pi^2 = 0.405` appears in D1 and D5") would settle it.

**Fifty-three figures and not one "Fig. N" reference** (`check_svg` advisory). Every
figure is introduced by an adjacent sentence, which mostly works, but section 8's three
figures in a row and section 6's two make the prose ambiguous about which is meant. Not
applied — numbering fifty-three figures is a module-wide convention change, not an
editorial fix, and it should be decided for the whole course at once.

**Section 9's closing does say what the reader can now do** (line 2129, "That closes
the mechanics..."), but it says it about the *course*, not the reader. Module 1 and 2
both close on the reader's new capability. Minor; not applied.

## 5. What already works

**The assembly of the consolidation equation (section 3, lines 439 to 507) is the best
writing in the module and should be the template for the rest of the course.** Three
ingredients, each named, each given a physical sentence before its equation, each
numbered, then a summary table that puts statement and equation side by side, then the
substitution done in the open with the eliminated variable pointed at. The proof that
follows is complete and the heat-conduction analogy table afterwards is exactly the
"analogy plus where it cashes out" the standard asks for. Nothing is asserted.

**The Hertz derivation (line 876) does the thing most textbooks skip.** It proves the
peak-to-mean ratio by actually integrating the cap, then gets the contact radius by
matching the `r^2` coefficient of the Boussinesq displacement to the parabolic gap. A
reader can reproduce both lines with a pen. The "Where classical Hertz is stretched"
list that follows is better still: it names three violated assumptions, gives the
numerical size of each violation (`a/R_eff = 0.6`, `a/h = 9`), and says which direction
the error runs. That is the rescue-or-limit-case part of the standard, done properly.

**The section 5 caveat on the strain level (line 823) is a model of intellectual
honesty.** It admits that 10 % strain sits at the edge of the linear theory, names both
neglected effects, says what the lab is still entitled to conclude, and defers the rest
to a named module. Most manuscripts would have quietly used 10 % and said nothing.

**Section 4's re-imbibition answer to the obvious objection (line 657).** The reader's
question — a footstep is short, but why doesn't `10^4` of them drain the tissue? — is
raised before the reader can raise it, and answered with the mechanism from section 2
rather than a hand-wave. The animated figure is driven by the same solution as the
static chart.

**D4 and D6 are excellent problems.** D4 asks why the correction is `sqrt(T)` and not
`T`, which is the one question that distinguishes a reader who has understood diffusion
from one who has memorised a series; D6 gets the `h^2` law from nondimensionalisation
alone, without touching the eigenfunctions. Both are short, both have a single idea,
and both are solvable from the text.

**Twelve of twelve code blocks run clean.** No exceptions, no undefined names, no
imports missing, all PEP8. After Module 3, this is worth saying.
