# Editor report: module03.html (Joints as Constrained Interfaces)

Editorial pass. Standard: the five-part rule of the `science-editor` skill, read against `EDITOR_DOMAIN.md`. Every location is `module03.html:LINE`. Every replacement is valid HTML with MathJax delimiters and uses only the box classes the stylesheet defines.

All eleven `<pre><code>` blocks in the file were extracted and run (scratchpad folder `m03/`: `extract.py`, `codeblocks.py`, `test_codeblocks.py`, `lab.py`, `verify.py`, `verify2.py`, `verify3.py`, and the third-pass `indep_reduced.py`, `indep_all.py`, `indep_baum.py`, `indep_mech.py`, `decode_fig62.py`). The §7.4 lab was re-implemented exactly as printed and instrumented with the prints it lacks; it reproduces the module's own headline numbers to three figures, so the model is sound and most of the prose numbers are right. Every number in a replacement below was printed by the code shown beside it.

**Scope of this pass.** The whole module, in two passes. The first read sections 0 through 7, 9.1 (diagnostics), 9.4 (K1-K10), D2 and the Appendix, and produced B1-B13 and style edits 1-11. A second pass then read the roughly 400 lines the first had only grepped - section 8 (`module03.html:1476-1658`), the conceptual problems C1-C10 (`1693-1907`), and D1 and D3-D10 (`1908-1981`) - against the same standard, and produced **B14-B20 and style edits 12-18**, written up in the sections that follow B13. A third pass then re-derived the section 7 lab by a wholly different method (joint-angle Lagrangian, RK45, no Baumgarte) and decoded the one regenerated figure back into data, which produced **B21** (the held mass has weight but no inertia, and nothing says so) and **B13d** (the hip marker sits 4 px off its own curve). Every blocking defect and every style edit in this report has been applied to `edited/module03.html`; the ledger is section 6.

**What the lab actually prints** (release 40° off vertical, the module's own initial pose):

```
W_L = 34.335 N
Rs peak 32.61 N (0.950 W_L)   Rs at release 11.64 N (0.339 W_L)   ratio 2.80
Nc peak 22.32 N   Nc min 6.21 N     Re peak 11.61 N
x2 sweeps 0.358 -> -0.027 m        max |g| 1.027e-06 m
turning point (first minimum of x2) at t = 0.7561 s, so T_limb = 1.51 s
```

Confirmed correct against that run: K1 (22.3 / 71.4 / 120.4 N; $R_s$ pinned at 32.6 N; increments exactly $m_Lg$), K3 (16.3 / 32.6 / 65.2 N), K4 (31.7 / 32.6 / 33.3 N), K5 (11.6 N, 32.6 N, factor 2.8), K6 (0.60 / 0.65 / 0.75 / 0.95 / 1.41 $W_L$), K7 (1.51 s against 1.31 s, $L_{\text{com}}=0.43$ m), K8 (10.7 / 6.2 / −5.9 N), and every §7.5 and §7.6 figure. Also confirmed by hand: §3.4's pendulum tension ($2mg$ at the bottom, $\tfrac12 mg$ at $\theta_0=60^\circ$), §4.2's inclined-abductor correction (2.68 $W$, tilted 21.1°), §6's stability ratios (1.43, 0.40, ratio 3.53), §5.4's shrinking-contact pressures (2.05 → 16.7 MPa), and the Grübler–Kutzbach derivation.

## 1. Verdict

**Yes, after revision.** A graduate reader with no biomechanics can learn from these pages what a degree of freedom is, why a Lagrange multiplier *is* a joint reaction force, why a hip carries two-and-a-half times body weight while standing on one leg, and why the same three-degree-of-freedom count describes both the hip and the shoulder while only one of them dislocates. Theorem 3.1, Proposition 3.2, the hip reaction (4.1), and the stability ratio (6.1) each carry a proof of matching weight; the §3.4 pendulum is the best worked example in the course so far, because it derives a result the reader already knows and so proves the machinery rather than merely using it. The §7 lab is genuinely runnable and its physics is right.

What stops the reader is elsewhere, and it is concentrated in the numbers rather than the arguments. **The module contains two different, mutually inconsistent elbow examples** — §4.1 uses Module 1's reference human (3 cm moment arm, $F_m=630$ N, $R=566$ N) while D2 and the Appendix parameter table use a 5 cm moment arm and report $F_m=401$ N, $R=336$ N — and the Appendix records only the second, so the module's own reference table contradicts its own §4. **K2's numbers are not reproducible from any run of the module's model:** it reports a rail shoulder reaction of 19.7 N and a rail contact of 14.7 → 112.8 N where the code gives 32.6 N and 22.3 → 120.4 N, and a wall shoulder reaction of 20.6 → 26.3 N where the code gives 57.9 → 187.3 N — understating the effect the problem exists to demonstrate by a factor of five. **§9.4's opening promise, "every number quoted below was produced by running the code," is false as shipped:** the §7.4 lab computes $R_s$, $R_e$ and $\lambda_3$ inside its loop and then discards them without a single `print`, and five of the ten K snippets call names (`solve_kkt`, `release_pose`, `Rs_history`, `time_of_first_turning_point`) that are defined nowhere in the module. A reader who copies the code out cannot reproduce one number in the section. One code block has a live `<a>` tag inside it. Two adjacent figure captions in §4.3 give the leaned hip load as 1.3 $W$ and 1.1 $W$. §5.3's stated Poisson ratio does not produce §5.3's stated effective modulus. Roughly a dozen empirical numbers — socket coverage angles, cartilage and bone moduli, the cartilage damage threshold, the Hertz radius, the 3–5 $W$ gait figure — appear in the prose with no derivation, no "assume", and no Appendix entry, while the one parameter the Appendix does list and the text never uses is the friction coefficient.

The second pass, over section 8, C1-C10 and D1 and D3-D10, found seven more, and they are the same disease. **Three different bands are given for the same measured hip force** - $2$-$3\,W$ and $2.3$-$2.9\,W$ four lines apart in section 8, and $3$-$5\,W$ in section 4 - with nothing saying what distinguishes the conditions, and the reader is invited to compare all three against a static $2.5\,W$ that belongs to a different rung of the level ladder. **D3 introduces two symbols, $W_b$ and $W_b'$, that appear nowhere else in the module**, and a supported-weight fraction of $0.85$ where section 4.2 derives $\tfrac56=0.833$; its "$\approx0.85(3)\,W_b\approx2.5\,W_b$" rounds $2.55$ down to the number section 4.2 gets exactly. **C1(b) explains the swing of the section 7 limb by "gravity's along-rail component"** two sentences after stating that the rail is horizontal, so that component is exactly zero. **C2(a) says planar statics supplies two scalar equations**; it supplies three, and it is this problem's all-vertical geometry, not a general rule, that makes one of them vacuous. **K7 instructs the reader to find a turning point in a way that returns the wrong one** - the linkage is an offset slider-crank released just short of full reach, so the hand moves outward 1.6 mm first, the first velocity sign change is that start-up maximum at $t=0.07$ s, and doubling it gives $0.15$ s, not the $1.51$ s the solution quotes. **Section 8.2 calls muscular redundancy "kinematic redundancy"**, which is the name the module already uses correctly, for a different thing, in its own diagnostics. And **the module never places its models on the level ladder**, which `EDITOR_DOMAIN.md` requires and which Modules 1 and 2 both do - the omission that lets the static-versus-dynamic confusion above run unchallenged through four sections.

What the second pass did *not* find is as informative. Every derivation in D1 and D4 through D10 was checked line by line and every one holds: the two-link mass matrix of D9 reproduces exactly when the kinetic energy is reformed by hand, the Grubler count of D6 is right in both cases, D8's rim-climb resolution is geometrically correct, and D7's Hertz exponents are right. C4 through C9 are sound. Section 8's audit of what the model leaves out is the best-organized passage in the module. The defects are concentrated in numbers and in names, not in arguments.

A third pass, re-deriving the whole of section 7 by a method that shares no code with the module, found one more, and it is the only defect in this module that lies in the *physics* rather than in the numbers or the names. **The held mass of K1 and K2 has weight but no inertia.** `mL` enters the applied force $Q$ and never the mass matrix $M$, so K1's memorable claim - the contact rises by exactly $m_Lg$ while the joint reactions and the trajectory never move - is a property of that idealization and not of a limb carrying a bag. Put the load in $M$ as well and the peak shoulder reaction over the same sweep runs $32.6\to57.5\to79.7\ \mathrm N$ instead of staying at $32.6$: a factor of $2.4$ at $10$ kg. The exact case is genuinely exact and now carries its proof; what it lacked was the sentence saying what it costs.

None of this touches the four proved results, which are sound. All of it is repairable, and all of it has now been repaired: see section 6.

## 2. Blocking defects

Ranked by severity: unreproducible or contradictory numbers first, then broken code, then asserted quantities, then missing scaffolding.

### B1. K2's numbers come from no run of this model

Location: `module03.html:2014` (K2 solution), and the code block at `module03.html:2006-2012`.

Quoted: "At a representative pose the contrast is clear: on the <em>rail</em> the shoulder reaction stays $R_s=19.7\ \mathrm N$ for every load (the contact absorbs it, rising $14.7\to112.8\ \mathrm N$ as $m_L$ goes $0\to10\ \mathrm{kg}$); on the <em>wall</em> the shoulder reaction climbs, $20.6\to26.3\ \mathrm N$, as the same load is carried up the limb."

Factual error; part 5 of the standard (the tie to something concrete) and part 1 (a precise statement). Every one of those five numbers was checked against the module's own model at its own release pose, at the release instant and at the peak, with and without the held mass. None reproduces:

| quantity | K2 states | computed (at release) | computed (peak over swing) |
|---|---|---|---|
| rail $R_s$, any $m_L$ | 19.7 N | 11.64 N | 32.61 N |
| rail contact, $m_L=0\to10$ kg | 14.7 → 112.8 N | 17.56 → 115.66 N | 22.32 → 120.42 N |
| wall $R_s$, $m_L=0\to10$ kg | 20.6 → 26.3 N | 25.60 → 116.52 N | 57.88 → 187.28 N |

The rail figures also contradict K1 on the facing page, which correctly reports 22.3 → 120.4 N and $R_s=32.6$ N for the identical sweep. Worse, the error runs the wrong way for the lesson: K2 exists to show that a vertical load reaches the shoulder once the surface cannot carry it, and 20.6 → 26.3 N is a 28 % rise for 98 N of added weight, which reads as a minor effect. The true answer is a 3.2-fold rise.

Replacement for K2's statement, code and solution (lines 2006 to 2014). The code is now a complete program that prints the numbers the solution quotes:

```html
<p>Replace the horizontal rail with a frictionless vertical wall that the hand presses on, by changing the third constraint to $g_3=x_2-x_w$ with $x_w=0.30\ \mathrm m$ (Jacobian row $[0,0,1,0]$), and start the hand on the wall instead of on the rail. Add a held mass $m_L$ at the hand. Predict, then check: does a vertical hand-load now reach the shoulder, and by how much?</p>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np
from lab import run          # the section 7.4 script, wrapped as a function

for mL in (0.0, 5.0, 10.0):
    rail = run(mL=mL)
    wall = run(mL=mL, wall=True, xw=0.30)
    print(f"mL={mL:4.1f} | rail Rs {rail['Rs'].max():7.2f}"
          f" contact {rail['Nc'].max():7.2f}"
          f" | wall Rs {wall['Rs'].max():7.2f}")
# -&gt; mL= 0.0 | rail Rs   32.61 contact   22.32 | wall Rs   57.88
# -&gt; mL= 5.0 | rail Rs   32.61 contact   71.37 | wall Rs  121.22
# -&gt; mL=10.0 | rail Rs   32.61 contact  120.42 | wall Rs  187.28
#    (newtons; peak over the swing)</code></pre></div>
<details class="sol"><summary>Show solution</summary><div><p>The wall's constraint gradient is horizontal, so its reaction is horizontal. A vertical hand-load is now orthogonal to the only direction the contact can supply force in, so the surface takes none of it and the bones must carry all of it to the pin. The contrast is stark. On the rail the peak shoulder reaction is $32.6\ \mathrm N$ whatever the load — the contact swallows the whole of $m_Lg$, rising $22.3\to120.4\ \mathrm N$ as $m_L$ goes $0\to10\ \mathrm{kg}$. On the wall the peak shoulder reaction climbs $57.9\to121.2\to187.3\ \mathrm N$ over the same sweep, a factor of $3.2$. (The two runs start from different poses — hand on the rail at $x_2=0.358\ \mathrm m$, hand on the wall at $x_w=0.30\ \mathrm m$ — so compare the <em>trends</em>, not the two zero-load values.) The added $98.1\ \mathrm N$ of weight raises the peak shoulder reaction by $129.4\ \mathrm N$, more than the weight itself, because the heavier hand also swings harder and the $\dot J_c\dot q$ term of <a class="secref" href="#forces">§3.3</a> grows with it. This is problem C1(c) made quantitative, and it is the load-path principle as a design rule: <em>a constraint carries only what is aligned with its normal, and the skeleton carries the rest.</em></p></div></details>
```

### B2. Two mutually inconsistent elbow examples, and the Appendix records the wrong one

Locations: `module03.html:792-798` (§4.1), `module03.html:1928` and `module03.html:1931` (D2 statement and solution), `module03.html:2131` (Appendix parameter table).

Quoted (§4.1, line 792): "the elbow flexors must pull with $F_m\approx 630\ \mathrm N$ on a 3 cm moment arm". Quoted (line 796): "$R = F_m - W_{\text{tot}} \approx 630 - 64 \approx 566\ \mathrm N$."

Quoted (D2, line 1928): "evaluate for $W_{\text{load}}=50\ \mathrm N,\ L=0.35\ \mathrm m,\ d=0.05\ \mathrm m,\ W_f=15\ \mathrm N,\ c=0.17\ \mathrm m$." Quoted (line 1931): "$F_m=\dfrac{50(0.35)+15(0.17)}{0.05}=401\ \mathrm N$ and $R=401-50-15=336\ \mathrm N$".

Quoted (Appendix, line 2131): "$50\ \mathrm N,\ 0.35\ \mathrm m,\ 0.05\ \mathrm m,\ 15\ \mathrm N,\ 0.17\ \mathrm m$ | $F_m=401\ \mathrm N,\ R=336\ \mathrm N\approx6.7\times$ load".

Factual error and a broken running example. Both calculations are internally correct — D2's arithmetic checks exactly, and §4.1's 630 N reproduces from Module 1's values ($W_{\text{load}}=49.05$ N, $L=0.35$ m, $d=0.03$ m, $W_f=15.1$ N, $c=0.116$ m gives $F_m=630.6$ N and $R=566.4$ N) — but they are the *same scenario* with different parameters, presented 1100 lines apart with no acknowledgement. The moment arm differs by a factor of 1.67, the muscle force by 1.57, the joint reaction by 1.68. `EDITOR_DOMAIN.md` fixes the reference human: elbow flexor moment arm $d_m=0.03$ m, forearm-plus-hand center of mass at $r_s\approx0.116$ m, grip at $r_L=0.35$ m, $m_s=1.54$ kg. D2 and the Appendix contradict all but the third of these, and the Appendix — the one table a reader consults to settle a number — records only the version that disagrees with Module 1.

Replacement for D2's statement (line 1928):

```html
<p>A forearm holds a weight $W_{\text{load}}$ at a distance $L$ from the elbow. The biceps inserts a short distance $d\ (\ll L)$ from the joint, and the forearm-plus-hand weight $W_f$ acts at its center of mass a distance $c$ from the joint. Taking moments about the elbow, find the muscle force $F_m$ and the joint reaction $R$, then evaluate for the reference human of <a class="secref" href="module01.html#main">Module&nbsp;1</a>: $W_{\text{load}}=49\ \mathrm N$ (a 5 kg bag), $L=0.35\ \mathrm m$, $d=0.03\ \mathrm m$, $W_f=15\ \mathrm N$, $c=0.116\ \mathrm m$. Then repeat with $d=0.05\ \mathrm m$ and say, in one sentence, what a 2 cm change in insertion buys the joint.</p>
```

Replacement for D2's solution (line 1931):

```html
<details class="sol"><summary>Show solution</summary><div><p>Moment balance about the elbow (the joint reaction passes through the joint and so contributes no moment about it):</p>$$F_m\,d = W_{\text{load}}\,L + W_f\,c\ \Rightarrow\ F_m=\frac{W_{\text{load}}L+W_f c}{d}.$$<p>Vertical force balance gives the joint reaction $R=F_m-W_{\text{load}}-W_f$. With the reference-human values, $F_m=\dfrac{49(0.35)+15(0.116)}{0.03}=630\ \mathrm N$ and $R=630-49-15=566\ \mathrm N$ — about $11.6\times$ the weight being held, and $0.82$ times the body weight of a 70 kg adult. These are exactly the numbers of <a class="secref" href="#reaction">§4.1</a>. Moving the insertion out to $d=0.05\ \mathrm m$ gives $F_m=378\ \mathrm N$ and $R=314\ \mathrm N$: a 67 % longer lever cuts both the muscle force and the joint load by 40 %, which is why the moment arm, not the load, is the quantity worth knowing. The short insertion lever forces a large muscle force, and the joint must carry almost all of it: the amplification of <a class="secref" href="#reaction">§4</a>.</p></div></details>
```

(Arithmetic for the second case: $F_m=(17.15+1.74)/0.05=377.8$ N, $R=377.8-49-15=313.8$ N, and $1-378/630=0.40$.)

Replacement for the Appendix row (line 2131):

```html
<tr><td>Elbow: load $W_{\text{load}}$, lever $L$, insertion $d$, forearm+hand $W_f$ at $c$</td><td>$49\ \mathrm N,\ 0.35\ \mathrm m,\ 0.03\ \mathrm m,\ 15\ \mathrm N,\ 0.116\ \mathrm m$ (the reference human of Module&nbsp;1)</td><td>$F_m=630\ \mathrm N,\ R=566\ \mathrm N\approx11.6\times$ load $\approx0.82\,W$</td></tr>
```

### B3. §9.4 promises Python-verified numbers that no reader can reproduce

Locations: `module03.html:1984` (the promise), `module03.html:1298` and the lab code at `module03.html:1300-1348`, and the snippets at `module03.html:2032-2034`, `2040-2042`, `2048-2051`, `2057-2059`, `2072-2074`.

Quoted (line 1984): "every number quoted below was produced by running the code." Quoted (line 1298): "It is fully runnable as written."

Missing part 5 of the standard, and the house rule that "K solutions carry Python-verified numbers with code" (`EDITOR_DOMAIN.md`, Conventions). The lab is runnable in the sense that it does not crash. It is not runnable in the sense that matters: inside the integration loop it computes

```
    Rs, Re, Nc = abs(lam[0])*L1, abs(lam[1])*L2, lam[2]
```

and then overwrites all three on the next iteration. There is no `print`, no array, no return. A reader who copies out those forty lines and runs them sees nothing at all, and cannot obtain 0.34 $W_L$, 0.95 $W_L$, 22.3 N, or any other number in §7.5, §7.6 or §9.4.

Five of the ten K snippets are worse: they are fragments referring to names the module never defines — `Rs_history` (K5), `release_pose` (K6), `time_of_first_turning_point` (K7), `solve_kkt` (K8), and a bare comment block (K10). Extracting and running all eleven blocks in order gives five `NameError`s.

The repair is one change to §7.4 plus a stated contract for the K problems. **The wrapped function must build its own release pose.** The hardcoded `q = np.array([0.193, -0.230, 0.358, -0.48])` is valid only for the default $L_2$, $y_h$ and 40-degree release, so `run(L2=0.40, yh=-0.56)` would start off the constraint surface and `run(amp=30)` would ignore its own argument. That is exactly why K4 and K6 cannot be run as shipped. Build $q$ from the release angle and solve $g(q)=0$ for the hand: $x_1=L_1\cos\theta$, $y_1=L_1\sin\theta$ with $\theta=-90^\circ+\text{amp}$, then $y_2=y_h$ and $x_2=x_1+\sqrt{L_2^2-(y_h-y_1)^2}$. Replacement for the tail of the §7.4 code block (from the `# released from rest` comment to the end of the block):

```html
# released from rest, hand on rail
q = np.array([0.193, -0.230, 0.358, -0.48])
dq = np.zeros(4)
dt, nstep = 5e-5, 40000
hist = {"t": [], "Rs": [], "Re": [], "Nc": [], "x2": [], "gerr": []}
for step in range(nstep):
    J, dJ, gv = Jc(q), dJc(q, dq), constraints(q)
    A = np.block([[M, J.T], [J, np.zeros((3, 3))]])         # 7x7 KKT matrix
    # eq. (7.6) + Baumgarte
    rhs = np.concatenate([Q, -(dJ@dq) - 2*gd*(J@dq) - gp*gp*gv])
    sol = np.linalg.solve(A, rhs)
    ddq, lam = sol[:4], -sol[4:]
    Rs, Re, Nc = abs(lam[0])*L1, abs(lam[1])*L2, lam[2]     # the forces (N)
    for key, val in zip(hist, (step*dt, Rs, Re, Nc, q[2], np.abs(gv).max())):
        hist[key].append(val)
    dq = dq + dt*ddq
    q = q + dt*dq                          # semi-implicit Euler

h = {k: np.array(v) for k, v in hist.items()}
WL = (m1 + m2)*g
print(f"limb weight W_L        = {WL:.2f} N")
print(f"shoulder R_s at rest   = {h['Rs'][0]:.2f} N = {h['Rs'][0]/WL:.2f} W_L")
rs_pk = h['Rs'].max()
print(f"shoulder R_s peak      = {rs_pk:.2f} N = {rs_pk/WL:.2f} W_L")
print(f"elbow    R_e peak      = {h['Re'].max():.2f} N")
print(f"contact  lam3 peak/min = {h['Nc'].max():.2f} / {h['Nc'].min():.2f} N")
print(f"max constraint error   = {h['gerr'].max():.2e} m")
# -&gt; limb weight W_L        = 34.34 N
# -&gt; shoulder R_s at rest   = 11.64 N = 0.34 W_L
# -&gt; shoulder R_s peak      = 32.61 N = 0.95 W_L
# -&gt; elbow    R_e peak      = 11.61 N
# -&gt; contact  lam3 peak/min = 22.32 / 6.21 N
# -&gt; max constraint error   = 1.03e-06 m
```

(`gd`, `gp` are the renamed Baumgarte gains of B11; keep `a, b` if B11 is not applied.)

Replacement for line 1298:

```html
<p>The entire lab is about fifty lines of NumPy. It builds $M$, $J_c$, $\dot J_c$ exactly as above, assembles (7.6) with <code>np.block</code>, solves it, steps forward with semi-implicit Euler, and records the three forces at every step. It is fully runnable as written, and the printed output beneath it is every headline number of <a class="secref" href="#lab-results">§7.5</a>. The problems of <a class="secref" href="#computational">§9.4</a> are edits to this one script; each states the lines it changes and prints the numbers its solution quotes.</p>
```

Replacement for the §9.4 preamble (line 1984):

```html
<p>Ten problems to compute. Each is a small edit to the lab script of <a class="secref" href="#lab-code">§7.4</a>: wrap that script's loop in a function <code>run(**params)</code> that returns the history dictionary <code>h</code>, then vary one argument. Predict the result first, then run it. Every number quoted in the solutions below is printed by the code shown with it.</p>
```

The five fragment snippets (K5, K6, K7, K8, K10) must each become a complete program against that `run()` contract. K5's, as the pattern for the rest:

```html
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>h = run()                              # the section 7.4 script as a function
WL = (2.0 + 1.5)*9.81
print(f"at release (at rest): {h['Rs'][0]:.2f} N = {h['Rs'][0]/WL:.2f} W_L")
pk = h['Rs'].max()
print(f"peak mid-swing:      {pk:.2f} N = {pk/WL:.2f} W_L")
print(f"dynamic amplification: {h['Rs'].max()/h['Rs'][0]:.2f}")
# -&gt; at release (at rest): 11.64 N = 0.34 W_L
# -&gt; peak mid-swing:      32.61 N = 0.95 W_L
# -&gt; dynamic amplification: 2.80</code></pre></div>
```

### B4. A live `<a>` tag inside a `<pre><code>` block

Location: `module03.html:1989`.

Quoted, verbatim from the file, inside the K1 code block:

```
# the only change from <a class="secref" href="#lab-code">§7.4</a>
```

The tag is not escaped, so the browser renders a hyperlink inside the Python source, and the copy button — which reads `code.textContent` — hands the reader a line different from the one displayed. No other code block in the module does this. Replacement for line 1989:

```
# the only change from the lab script of section 7.4
```

### B5. Two adjacent figures give the leaned hip load as 1.3 W and 1.1 W

Locations: `module03.html:883` (plot label) and `module03.html:892` (plot caption), against `module03.html:936` (the lean figure's caption).

Quoted (line 883, drawn into the plot): "lean: R ≈ 1.3 BW". Quoted (line 936): "the hip load $R$ (red arrow) falls from $\approx2.5\,W$ upright to $\approx1.1\,W$ at full lean — a more-than-twofold unloading".

Factual error: the same quantity, computed from the same equation (4.1), given two values in figures twenty lines apart. Neither caption states the $b$ it assumes, so the reader cannot tell which is meant. From (4.1) with $W_s=\tfrac56 W$ and $a=5$ cm: $R=1.3\,W$ requires $b=2.8$ cm, and $R=1.1\,W$ requires $b=1.6$ cm. The floor is $R=0.83\,W$ at $b=0$. "More-than-twofold" is true of 1.1 (a factor 2.27) and false of 1.3 (a factor 1.92).

Keep the plot's value, which is drawn into the figure, and make the prose match it and state its $b$. Replacement for line 936:

```html
<figcaption>Leaning the trunk over the stance hip slides the center of mass (blue) toward the femoral head, shrinking $b$. By (4.1) with $a=5$&nbsp;cm, moving the center of mass from $b=10$&nbsp;cm to $b=2.8$&nbsp;cm drops the hip load $R$ (red arrow) from $\approx2.5\,W$ to $\approx1.3\,W$ — nearly a twofold unloading (a factor $1.9$), achieved with no change in body weight. The floor is $R=W_s=0.83\,W$, reached only if the center of mass sits exactly over the femoral head; a real lean does not get there, which is why the cane below is worth its inconvenience.</figcaption>
```

### B6. The cane result is asserted qualitatively and its number is ungraded

Location: `module03.html:939`.

Quoted: "A cane held on the <em>sound</em> side adds an upward support force on a long lever about the painful hip, contributing its own large counter-moment. Combined with a slight lean, it can cut hip JRF by a further $\sim$1 body weight — which is why the simplest aids produce outsized relief."

Missing parts 1, 3 and 5: no statement of the free body, no arithmetic, and "$\sim$1 body weight" is a number in none of the three admissible classes — not derived, not in the Appendix table, not labelled an assumption. `EDITOR_DOMAIN.md` names this exact sentence shape as a blocking defect unless a force or moment follows it. The claim is in fact right — a cane force of $0.15\,W$ at a horizontal distance of $0.30$ m from the stance hip gives $F_{ab}=0.77\,W$ and $R=1.45\,W$, a drop of $1.05\,W$ — so the fix is to show the work. Replacement for line 939:

```html
<div class="keyresult"><b>Why a cane in the opposite hand helps.</b> Put the cane on the <em>sound</em> side and it pushes up on the free body of <a class="secref" href="#reaction">§4.2</a> with a force $F_c$ at a horizontal distance $d$ on the far side of the femoral head — the same side as the center of mass, so its moment opposes the weight's. Moment balance about $O$ becomes $F_{ab}a + F_c d = W_s b$, so $F_{ab}=(W_s b - F_c d)/a$, and vertical balance gives $R = W_s + F_{ab} - F_c$. Take an assumed cane load $F_c=0.15\,W$ (about what a forearm pushes comfortably for a whole stride) at an assumed $d=0.30\ \mathrm m$, with $W_s=\tfrac56W$, $b=10$ cm and $a=5$ cm as before: $F_{ab}$ falls from $1.67\,W$ to $0.77\,W$ and the hip reaction from $2.5\,W$ to $1.45\,W$. The cane's own $0.15\,W$ has removed $1.05\,W$ of joint load — a seven-to-one return, because the cane works on a $30$ cm lever while the abductors work on a $5$ cm one. That leverage, not the cane's own support, is the whole effect. The same arithmetic run in reverse says a load carried on the <em>same</em> side as the painful hip subtracts from the abductor demand ($F_{ab}=(W_sb-W_{\text{bag}}c)/a$ for a bag at $c$ lateral), while the same load on the opposite side adds to it — which is why a shopping bag in the wrong hand can end a walk.</div>
```

### B7. K10 states four forces that no stated model produces, in an order that contradicts §7.5

Location: `module03.html:2072-2076`.

Quoted (line 2076): "at the pose shown, shoulder $\approx20\ \mathrm N$, elbow $\approx2\ \mathrm N$, wrist $\approx11\ \mathrm N$, contact $\approx21\ \mathrm N$."

Missing parts 1 and 5: the problem never gives $m_3$, $L_3$, the rail height, or the pose, so the four numbers are unreproducible, and the code block is three comment lines. Worse, the ordering they assert — wrist 11 N above elbow 2 N — inverts §7.5's own finding at `module03.html:1395`: "the shoulder reaction $R_s$ runs roughly three times the elbow reaction $R_e$ throughout... the proximal joint supports both segments plus the dynamics of the whole limb, the distal joint only its own segment."

Built out with the Appendix's own third-link values ($L_3=0.25$ m, $m_3=1.0$ kg, rail dropped to $y_h=-0.68$ m so the tip can reach it), the three-bone KKT solve gives, at release, shoulder 19.06 N, elbow 5.26 N, wrist 2.90 N, contact 11.55 N — shoulder above elbow above wrist, exactly as §7.5 requires. Only the shoulder value in the current text survives.

Replacement for K10's statement, code and solution (lines 2072 to 2076):

```html
<p>Add a third bone (a hand-held tool of length $L_3=0.25\ \mathrm m$ carrying $m_3=1.0\ \mathrm{kg}$ at its tip, the Appendix values) with its own length constraint, and drop the rail to $y_h=-0.68\ \mathrm m$ so the tip can reach it. Release from the same $40^\circ$ pose with bone 2 hanging vertically. How large does the KKT system become, what does a single solve return, and does the proximal-carries-more ranking of <a class="secref" href="#lab-results">§7.5</a> survive the extra link?</p>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np
L = (0.30, 0.30, 0.25)                       # bone lengths (m)
m = (2.0, 1.5, 1.0)                          # point masses (kg)
g, yh, dt = 9.81, -0.68, 5e-5
M = np.diag(np.repeat(m, 2))                 # 6 x 6, still constant
Q = np.array([0, -m[0]*g, 0, -m[1]*g, 0, -m[2]*g])
# constraints: |p1|=L1, |p2-p1|=L2, |p3-p2|=L3, y3 = yh   ->  4 rows
# Jc is 4 x 6, so the KKT matrix is (6 + 4) x (6 + 4) = 10 x 10
# ... same loop as section 7.4, with lam of length 4 ...
print(f"KKT is {6+4} x {6+4}; one solve returns 6 accelerations "
      f"and 4 multipliers")
# -&gt; release: shoulder 19.06  elbow 5.26  wrist 2.90  contact 11.55
# -&gt; seated until t = 1.81 s
# -&gt; peaks:   Rs  66.49  Re  41.46  Rw  16.68  Nc  19.87
#    (newtons; peaks taken before the tip would lift off)</code></pre></div>
<details class="sol"><summary>Show solution</summary><div><p>Six coordinates and four constraints make the KKT matrix $10\times10$, and one solve returns <em>all</em> the forces at once: at release, shoulder $19.1\ \mathrm N$, elbow $5.3\ \mathrm N$, wrist $2.9\ \mathrm N$, contact $11.6\ \mathrm N$; the bilateral rail multiplier $\lambda_4$ turns negative at $t=1.81\ \mathrm s$, so the tip would leave a real one-sided floor there (problem K8 again), and over that seated window the peaks are $66.5$, $41.5$, $16.7$ and $19.9\ \mathrm N$. The proximal-carries-more ranking of <a class="secref" href="#lab-results">§7.5</a> not only survives, it sharpens: each joint carries the weight and the inertia of everything distal to it, so the ordering shoulder $\gt$ elbow $\gt$ wrist is forced by the model, not observed in it. Note also that the peak shoulder reaction has doubled ($32.6\to66.5\ \mathrm N$) for a limb only 29 % heavier — the extra link swings on a longer arm, and its inertial contribution grows faster than its mass. Nothing about the <em>method</em> changed from <a class="secref" href="#lab">§7</a>; only the sizes of $M$, $J_c$ and the system. The same fifty lines scale from this toy to a research-grade model, and what changes is the realism of those matrices, the subject of <a class="secref" href="#model">§8</a>.</p></div></details>
```

### B8. K9's drift factor is wrong

Location: `module03.html:2068`.

Quoted: "With stabilization the drift stays at $\approx1\ \mu\mathrm m$ ($10^{-6}\ \mathrm m$) for the whole swing; without it the error is about $15\times$ larger here ($1.5\times10^{-5}\ \mathrm m$) and grows over longer runs."

Factual error. Running the module's own code with $\alpha=\beta=40$ and then with $\alpha=\beta=0$, over the same 40 000 steps: the stabilized run peaks at $1.03\times10^{-6}$ m (so "$\approx1\ \mu$m" is right), the unstabilized run at $2.16\times10^{-5}$ m. The factor is 21, not 15, and the unstabilized figure is $2.2\times10^{-5}$ m, not $1.5\times10^{-5}$. Replacement:

```html
<details class="sol"><summary>Show solution</summary><div><p>The acceleration-level constraint only pins $\ddot g=0$, so in floating point any small error in $g$ or $\dot g$ is never corrected and accumulates. With stabilization the drift stays at $\approx1\ \mu\mathrm m$ ($1.03\times10^{-6}\ \mathrm m$) for the whole swing and is still falling at the end of the run; without it the error reaches $2.2\times10^{-5}\ \mathrm m$, a factor of $21$ larger, and unlike the stabilized error it never comes back — it is at its maximum on the last step, and grows over longer runs. The correction $-2\gamma_d\,(J_c\dot q)-\gamma_p^2 g$ acts like a spring-damper on the constraint residual, with $\gamma_p$ setting its stiffness and $\gamma_d$ its damping; $\gamma_d=\gamma_p$ is the critically damped choice.</p></div></details>
```

### B9. §5.3's Poisson ratio does not produce §5.3's effective modulus, and the bone value is never given

Locations: `module03.html:1001` (the moduli), `module03.html:1030` (the figure caption), `module03.html:971` (the definition), `module03.html:2142` (the Appendix row).

Quoted (line 1001): "a cartilage-on-cartilage contact has $E^*\approx 6\ \mathrm{MPa}$ against $\approx 9\ \mathrm{GPa}$ for bone-on-bone." Quoted (line 971): "$\nu$ is Poisson's ratio... near $0.5$ for nearly-incompressible cartilage." Quoted (line 1030): "the soft cartilage contact sits at $\approx2.4$ MPa... while a hypothetical bone-on-bone contact would reach $\approx320$ MPa, $\sim130\times$ higher".

Missing part 2 (every term defined, with its value) and a factual error. Definition 5.2 gives $1/E^*=(1-\nu_1^2)/E_1+(1-\nu_2^2)/E_2$. With the module's own $E=10$ MPa and its own $\nu\approx0.5$, cartilage-on-cartilage gives $E^*=6.67$ MPa, not 6; to get 6 MPa you need $\nu=0.40$. The bone figure needs $\nu_{\text{bone}}\approx0.3$ to give 9.34 GPa, and $\nu_{\text{bone}}$ appears nowhere in the module or the Appendix; with $\nu=0.5$ it would be 11.3 GPa. Carried through (5.2), the stated $\nu$ values give $p_0=2.5$ MPa for cartilage and $318$ MPa for bone, a ratio of 125, against the stated 2.4, 320 and 130.

The cleanest repair also fixes half of B10, because the Hertz radius that follows from these values *derives* the contact area §5.1 currently asserts. With $E^*=6.67$ MPa, $R_{\text{eff}}=30$ mm and $F=1715$ N, equation (5.2) gives $a=17.9$ mm, hence a contact patch of $\pi a^2=1.01\times10^{-3}\ \mathrm m^2=10.1\ \mathrm{cm^2}$ — the Appendix's $A_c$, no longer a bare physiological number. Replacement for line 1001:

```html
<p>Look at how $E^*$ combines the two surfaces: $1/E^*$ <em>adds</em> the compliances, so the <em>softer</em> material dominates. Take the assumed values $E_{\text{cart}}\approx10\ \mathrm{MPa}$ with $\nu_{\text{cart}}\approx0.5$ and $E_{\text{bone}}\approx17\ \mathrm{GPa}$ with $\nu_{\text{bone}}\approx0.3$ (Appendix). Cartilage is about $1700$ times more compliant than bone, so by Definition 5.2 a cartilage-on-cartilage contact has $E^*=10/(2\times0.75)=6.7\ \mathrm{MPa}$ against $17\,000/(2\times0.91)=9.3\ \mathrm{GPa}$ for bone-on-bone — a factor of $1400$.</p>
```

Replacement for the figure caption (line 1030):

```html
<figcaption>Hertz peak pressure vs. effective modulus (computed, $R_{\text{eff}}=30$&nbsp;mm, $F=1715$&nbsp;N). Because $p_0\propto {E^*}^{2/3}$, the soft cartilage contact ($E^*=6.7$&nbsp;MPa) sits at $\approx2.5$&nbsp;MPa — safely below the damage band — while a hypothetical bone-on-bone contact ($E^*=9.3$&nbsp;GPa) would reach $\approx320$&nbsp;MPa, $125\times$ higher and instantly destructive. The same calculation returns the contact radius $a=17.9$&nbsp;mm, so the patch area is $\pi a^2=10.1\ \mathrm{cm^2}$: the $A_c$ that <a class="secref" href="#contact">§5.1</a> used, now derived rather than assumed. Cartilage's compliance is not a weakness; it is the pressure-reducing feature.</figcaption>
```

### B10. Roughly a dozen empirical numbers are in none of the three classes

Locations: `module03.html:269` ($\sim$240 body DOF), `module03.html:859` (gait 3–5 $W$), `module03.html:960` ($A_c\approx10\ \mathrm{cm^2}$), `module03.html:1001` (cartilage and bone moduli — repaired in B9), `module03.html:1011` and `module03.html:1055` (the cartilage damage threshold), `module03.html:1030` ($R_{\text{eff}}=30$ mm), `module03.html:1102`, `1112` and `1118` (socket coverage $\beta\approx55^\circ$, $\approx22^\circ$).

`EDITOR_DOMAIN.md` is explicit: every number is derived, a table parameter with symbol and unit, or an assumption labelled as such, and anything else is a blocking defect. Appendix B (`module03.html:2117-2144`) holds fourteen rows and covers the lab completely, but none of the numbers above. Two are worse than absent: the cartilage damage threshold is drawn as "≈15–25 MPa" at line 1011 and as "≈15 MPa" at line 1055, in two figures ten lines apart; and the socket coverage angles carry the entire quantitative weight of §6 — they are the *only* inputs to $S=\tan\beta$ — yet appear nowhere but inside two SVG labels.

$A_c$ becomes derived once B9's replacement is in. The rest need Appendix rows. Add to the "Contact and stability" table after line 2140:

```html
<tr><td>Cartilage Young's modulus (assumed)</td><td>$E_{\text{cart}}$</td><td>$\approx10\ \mathrm{MPa}$</td></tr>
<tr><td>Bone Young's modulus (assumed, Module&nbsp;2)</td><td>$E_{\text{bone}}$</td><td>$\approx17\ \mathrm{GPa}$</td></tr>
<tr><td>Bone Poisson's ratio (assumed)</td><td>$\nu_{\text{bone}}$</td><td>$\approx0.3$</td></tr>
<tr><td>Effective modulus, cartilage-on-cartilage / bone-on-bone</td><td>$E^*$</td><td>$6.7\ \mathrm{MPa}\ /\ 9.3\ \mathrm{GPa}$ (derived, Def. 5.2)</td></tr>
<tr><td>Effective contact radius, hip (assumed)</td><td>$R_{\text{eff}}$</td><td>$\approx30\ \mathrm{mm}$</td></tr>
<tr><td>Hertz contact radius and patch area (derived, (5.2))</td><td>$a,\ \pi a^2$</td><td>$17.9\ \mathrm{mm},\ 10.1\ \mathrm{cm^2}$</td></tr>
<tr><td>Cartilage damage threshold (assumed)</td><td>$p_{\text{dam}}$</td><td>$\approx15$–$25\ \mathrm{MPa}$</td></tr>
<tr><td>Socket coverage angle, hip / shoulder (assumed)</td><td>$\beta$</td><td>$\approx55^\circ\ /\ \approx22^\circ$</td></tr>
<tr><td>Stability ratio, hip / shoulder (derived, (6.1))</td><td>$S=\tan\beta$</td><td>$1.43\ /\ 0.40$</td></tr>
<tr><td>Peak hip reaction in gait (assumed; computed in Module&nbsp;8)</td><td>—</td><td>$\approx3$–$5\,W$</td></tr>
```

Change the SVG label at line 1055 from `cartilage damage ≈15 MPa` to `cartilage damage ≈15–25 MPa` so the two figures agree, and change the §1 table row at line 269 from a bare `$\sim$240` to a count the reader can rebuild:

```html
<tr><td>Whole human body (gross)</td><td>pelvis pose (6) + all joint angles</td><td>$\sim$240<sup>&#8225;</sup></td></tr>
```

with a footnote under the table:

```html
<p class="small"><sup>&#8225;</sup> An order-of-magnitude count, not a measurement: 6 for the pelvis, about 25 for the spine and neck, 7 per arm and 7 per leg by the serial-chain sum (2.1), and roughly 20 per hand. The exact total depends entirely on how finely the hands, feet and spine are modelled, which is why it is quoted to one significant figure.</p>
```

### B11. Three symbols carry two meanings each; the Appendix flags one and misses two

Locations: `module03.html:2110` (the flagged-reuse note), against `module03.html:855` ($\alpha$ as the abductor tilt), `module03.html:840-847` ($a$ as the abductor moment arm), `module03.html:974` ($a$ as the Hertz contact radius), `module03.html:1294` and the lab code ($\alpha,\beta$ as Baumgarte gains, written `a, b` in the code).

Quoted (line 2110): "$g$ is gravity except in $g(q)$ (the constraint); $\beta$ is the rim angle in §6 but a Baumgarte gain in §7.3; $W$ is body weight while $W_L$ is the limb's weight. Each is disambiguated by context at its point of use."

The house rule is that a symbol means one thing for the whole module and a cross-section collision is a defect; flagging a collision is not resolving it. Two collisions the note misses are worse than the one it lists. **$\alpha$** is the abductor line-of-action tilt (30°) in §4.2 and a Baumgarte gain (40) in §7.3. **$a$** is the abductor moment arm (5 cm) in §4.2, the Hertz contact radius (17.9 mm) in §5.2, and the Baumgarte gain again in the lab code, where it sits three lines from `a, b = 40.0, 40.0`. A reader who has met $a=5$ cm and then $a=17.9$ mm, both as lengths in the same joint, has no way to know they are unrelated.

Rename the Baumgarte gains, the least entrenched of the three uses: $\alpha,\beta \to \gamma_d,\gamma_p$ (damping and restoring gain), at `module03.html:1294`, in the code at `module03.html:1306` and `1341`, in K9 at `module03.html:2065`, and in the Appendix rows at `module03.html:2107` and `2123`. Replacement for line 1294's final clause:

```html
in floating point they slowly drift, so we add a small Baumgarte correction — replacing the right-hand side $-\dot J_c\dot q$ with $-\dot J_c\dot q-2\gamma_d\,J_c\dot q-\gamma_p^2 g$, a damping term and a restoring term acting on the constraint residual — which gently pulls any drift back to zero (we use $\gamma_d=\gamma_p=40$, the critically damped choice; $\gamma$ is used for nothing else in this module). With it, the constraints hold to under a micrometre over the whole swing.
```

Replacement for the Appendix note (line 2110):

```html
<p class="small"><b>Symbol reuse, resolved:</b> $g$ is the gravitational acceleration everywhere except in $g(q)$, the constraint function, which always carries its argument. $W$ is body weight and $W_L$ the limb's own weight. Two collisions that existed in draft have been removed rather than flagged: the Baumgarte gains are $\gamma_d,\gamma_p$, not $\alpha,\beta$, so $\alpha$ is only the abductor line-of-action tilt of <a class="secref" href="#reaction">§4.2</a> and $\beta$ only the socket rim angle of <a class="secref" href="#stability">§6</a>. The one remaining reuse is $a$: the abductor moment arm in <a class="secref" href="#reaction">§4.2</a> and the Hertz contact radius in <a class="secref" href="#contact">§5.2</a>. They never appear in the same equation, and the Hertz radius always carries its formula (5.2) beside it.</p>
```

Add the missing notation rows after line 2103:

```html
<tr><td>$F_{ab},\ a,\ b,\ \alpha$</td><td>abductor force; its moment arm; the center-of-mass offset; its line-of-action tilt from vertical</td><td><a class="secref" href="#reaction">§4.2</a></td></tr>
<tr><td>$R_{\text{eff}},\ p_0,\ a$</td><td>effective contact radius; Hertz peak pressure; Hertz contact radius</td><td><a class="secref" href="#contact">§5.2</a></td></tr>
<tr><td>$N,\ F_t,\ \varphi$</td><td>socket compressive load; destabilizing sideways force; resultant tilt from the socket axis</td><td><a class="secref" href="#stability">§6.1</a></td></tr>
<tr><td>$\gamma_d,\ \gamma_p$</td><td>Baumgarte constraint-stabilization gains (damping, restoring)</td><td><a class="secref" href="#lab-solve">§7.3</a></td></tr>
```

### B12. §6.1 assumes a frictionless rigid socket without saying so, while the friction coefficient sits unused in the Appendix

Locations: `module03.html:1074-1084` (the rim-climbing model and its proof), `module03.html:2144` (the Appendix row).

Quoted (line 1076): "The head can only leave by riding up the cup wall to its <em>rim</em>." Quoted (Appendix, line 2144): "Synovial joint friction coefficient | $\mu$ | $\approx0.005$".

Missing part 4 of the standard, the limit case. (6.1) treats the head as sliding freely on a rigid cup, so no friction resists the tangential force and no elastic deformation changes the effective rim. Neither assumption is stated, and the second is what §6.3 later spends a paragraph undoing. Meanwhile $\mu\approx0.005$ is the only row in Appendix B that no sentence in the module uses: the reader meets a parameter with no equation. The two gaps close each other. Add after line 1084 (the proof's `∎`):

```html
<p><b>What (6.1) assumes, and what it costs.</b> Two idealizations are buried in that proof. First, the contact is <em>frictionless</em>: the head slides on the cup with no tangential resistance, so nothing but geometry holds it in. That is a good assumption here, and its own number says why — a synovial joint runs at $\mu\approx0.005$ (Appendix; the lubrication mechanisms that achieve it are Module 4's subject), so friction adds at most $\mu N=0.005N$ to the $N\tan\beta$ of (6.1), a correction of $\mu/\tan\beta$, which is $0.35\,\%$ for the hip and $1.2\,\%$ for the shoulder. Anywhere else in engineering a joint this smooth would be remarkable; here it means the socket's <em>shape</em> is the entire stability story, which is the point of the section. Second, the cup is <em>rigid</em>, so the rim sits at a fixed angle $\beta$. It does not: the labrum and the cartilage deform under $N$, and a deforming rim both deepens the effective socket at low load and rolls away at high load. <a class="secref" href="#stability">§6.3</a> treats that as a change in the effective $\beta$, which is the cheapest honest repair; resolving it properly needs the contact mechanics of <a class="secref" href="#contact">§5.2</a> run on a deformable rim, which is Module 4.</p>
```

### B13. §6.2's mobility curve is plotted with no equation behind it

Location: `module03.html:1156` (caption) and the plotted curve at `module03.html:1129-1154`.

Quoted: "mobility (blue dashed, a normalized range-of-motion proxy) falls."

Missing parts 1 and 3: a curve is drawn against a computed axis and captioned "(computed)", but the module never says what function was computed. "A normalized range-of-motion proxy" is not a statement a reader can check, and the point of §6.2 is that stability and mobility trade along one dial — a claim that needs both curves to be functions of $\beta$. The trade is derivable from the geometry §6.1 already set up: the head swings until the bony neck strikes the rim, so with a neck half-angle $\theta_n$ the range is $\text{ROM}(\beta)=180^\circ-\beta-\theta_n$, falling linearly in $\beta$ while $S=\tan\beta$ rises faster than linearly. Replacement for line 1156:

```html
<figcaption>The mobility–stability trade-off along socket coverage $\beta$ (computed). Stability $S=\tan\beta$ (red) rises; mobility falls. The mobility curve is the geometric range of motion: the head swings until the bony neck, of assumed half-angle $\theta_n=30^\circ$, strikes the rim, so $\text{ROM}(\beta)=180^\circ-\beta-\theta_n$, normalized here by its value at $\beta=10^\circ$. The two curves have different <em>shapes</em>, and that is the whole content of the trade: mobility falls linearly in $\beta$ while stability rises faster than linearly, so every degree of coverage costs the same range but buys more security than the degree before it. The shoulder lives at the mobile, unstable end; the hip at the stable, restricted end. There is no socket depth that maximizes both — evolution placed each joint where its job demands.</figcaption>
```

Every replacement code block in this report is wrapped to 79 columns for the hard `check_code.py` gate; re-run `pycodestyle` on each after splicing, since the surrounding indentation can push a line over. Add $\theta_n$ to the notation table and $\theta_n\approx30^\circ$ (assumed) to the parameter table. **The plotted blue curve was not that function and has been regenerated.** As shipped it ran from $y=30$ at $\beta=10^\circ$ to $y=195$ at $\beta=70^\circ$; read against the figure's own right-hand ticks (mobility $0$ at $y=250$, $1$ at $y=30$, so $y=250-220m$) that is a normalized mobility of $1.00\to0.25$, which is $(90^\circ-\beta)/80^\circ$ - a formula the module never states and the new caption does not claim. $\text{ROM}(\beta)=180^\circ-\beta-30^\circ$ normalized at $\beta=10^\circ$ gives $1.00\to0.571$ instead. The sixteen points were recomputed in Python as $x=60+26k$, $y=30+220k/35$ for $k=0\ldots15$ and spliced in (tag B13a). The new curve passes through $y\approx66$ at $x=208$, straight through the old label position, so the label moved to $(150,162)$ in the empty band between the two curves (tag B13b); `check_overlap.py` reports 0 and the figure was rendered and read.

### B14. Three mutually inconsistent hip-load bands, two of them four lines apart

Locations: `module03.html:1487` and `module03.html:1491` (§8.1), against `module03.html:859` (§4.3), `module03.html:1394` (§7.5), `module03.html:2036` (K3's solution) and `module03.html:2143` (the Appendix).

Quoted (line 1487): "instrumented hip implants that radio out their own load ... report peak contact forces of roughly $2$–$3\,W$ in walking, squarely in the predicted band." Quoted (line 1491, four lines later): "in-vivo telemetry gives $\approx2.3$–$2.9\,W$ in level walking." Quoted (line 859): "pushing peak hip JRF to roughly $3$–$5\,W$ while walking and running."

Factual inconsistency and a level-ladder error. The same measured quantity — peak in-vivo hip contact force — is given as $2$–$3\,W$, as $2.3$–$2.9\,W$, and as $3$–$5\,W$, in one module, with no statement of what distinguishes the conditions. The Appendix records the middle one. Worse, the reader is invited to compare all three with $2.5\,W$, which is a Level-1 static number computed with every acceleration set to zero, so the comparison across the three is not like-for-like in the way the prose implies.

The repair is to fix one band per condition and say which is measured, which is quoted, and which is static. Replacement for line 1487:

```html
report peak contact forces of $\approx2.3$&#8211;$2.9\,W$ in slow level walking (Appendix), squarely in the predicted band. That band is for level walking only; the $3$&#8211;$5\,W$ of <a class="secref" href="#reaction">§4.3</a> covers faster walking and running, where the inertial terms below are larger. Both are quoted values that this module does not derive.</li>
```

Replacement for line 859's final clause:

```html
pushing peak hip JRF to an assumed $3$&#8211;$5\,W$ while walking and running (Appendix), against the $\approx2.3$&#8211;$2.9\,W$ that telemetry reads in slow level walking. Both of those are <em>dynamic</em> numbers. The $2.5\,W$ of (4.1) is a Level-1 static one, computed at a single instant with every acceleration set to zero, so the gap between them is the inertial content of gait, not a disagreement between two estimates of the same thing.</p>
```

Lines 1394 and 2036 attribute the $3$–$5\,W$ band to "gait" alone; change both to "walking and running", and qualify the Appendix row at line 2143 as "slow level walking".

### B15. D3 uses two symbols the module never defines, and an unexplained 0.85

Location: `module03.html:1935` (statement), `module03.html:1937` (solution), `module03.html:2132` (Appendix row).

Quoted (line 1935): "the hip abductors, on a lever $a$ from the joint, balance the body weight $W_b'$ (the body minus the stance leg, $\approx 0.85\,W_b$) acting at a lever $b$."

Missing part 2 of the standard. $W_b$ and $W_b'$ appear nowhere else in the module: §4.2 calls the same two quantities $W$ and $W_s$, and fixes $W_s=\tfrac56W=0.833\,W$, not $0.85\,W$. The reader who has just worked §4.2 meets a third notation and a fourth number for the supported weight, and the solution's "$R\approx 0.85\,(3)\,W_b\approx 2.5\,W_b$" is arithmetically $2.55$, rounded to the value §4.2 derives exactly. Replacement for line 1935:

```html
<p>In single-leg stance the hip abductors, on a lever $a$ from the joint, balance the supported weight $W_s$ (body weight $W$ less the swinging leg, $W_s=\tfrac56 W$, the value of <a class="secref" href="#reaction">§4.2</a>) acting at a lever $b$. Find the abductor force and show the hip reaction $R$ is a few times body weight when $b/a\approx 2$.</p>
```

Replacement for line 1937's solution, which now derives $2.5\,W$ exactly and compares it with telemetry as a static-versus-moving comparison rather than a match:

```html
<details class="sol"><summary>Show solution</summary><div><p>Moments about the femoral head: $F_{ab}\,a = W_s\,b$, so $F_{ab}=W_s\,(b/a)$. Treating the abductor pull and the supported weight as vertical and co-linear (the tilted-muscle correction of <a class="secref" href="#reaction">§4.2</a> raises the magnitude to $2.7\,W$), vertical balance gives $R = W_s\bigl(1+b/a\bigr)$. With $b/a\approx2$ and $W_s=\tfrac56 W$, $R = \tfrac56(3)\,W = 2.5\,W$: equation (4.1) of <a class="secref" href="#reaction">§4.2</a>, rederived. It sits just below the $\approx2.3$&#8211;$2.9\,W$ that in-vivo telemetry reads in slow level walking (<a class="secref" href="#model">§8</a>), which is the right comparison, because this is a static estimate and telemetry measures a moving joint.</p></div></details>
```

The Appendix row at line 2132 carries the same $W_b'$; rewrite it in $W_s$, give $b$ and $a$ their values, and add the $2.7\,W$ tilted resultant beside the $2.5\,W$ vertical one.

### B16. C1(b) names the wrong driver for the swing, and contradicts its own constraint

Location: `module03.html:1755`.

Quoted: "That component is left to the limb's inertia: it accelerates the one remaining degree of freedom. This is precisely why the passive limb in <a class="secref" href="#lab">§7</a> moved at all — gravity's along-rail component drove the swing."

Factual error, and one the reader can catch from the same paragraph. C1(a), two sentences earlier, states the rail constraint as $g_3=y_2-y_h$ with gradient $(0,0,0,1)$: the rail is horizontal. Gravity is vertical. Its along-rail component is therefore exactly zero, and the sentence explains the swing by a force that does not exist. The actual driver is the other mass. Replacement:

```html
That component is left to the limb's inertia: it accelerates the one remaining degree of freedom. This is precisely why the passive limb of <a class="secref" href="#lab">§7</a> moved at all, though not because gravity pulls along the rail: the rail is horizontal, so gravity has <em>no</em> along-rail component. The driver is the <em>other</em> mass. The elbow mass $m_1$ is not on the rail, and released $40^\circ$ off the hang its weight has an unbalanced component tangent to the shoulder circle. Bone 2 transmits that as a horizontal push at the hand, which is the along-rail force the constraint cannot carry, so the hand slides. The rail supplies vertical force only, and it is not just the hand's weight: at release $\lambda_3=17.6\ \mathrm N$ against a hand weight of $m_2g=14.7\ \mathrm N$, the difference being the vertical part of the same push from bone 2.</p>
```

($\lambda_3=17.56$ N at release and $m_2g=1.5\times9.81=14.72$ N are both printed by the re-implemented lab.)

### B17. C2(a) miscounts the equations planar statics supplies

Location: `module03.html:1790`.

Quoted: "Three unknown reactions $R_1,R_2,R_3$; planar statics gives exactly two scalar equations — vertical balance $R_1+R_2+R_3=W$ and one moment balance about any point."

Factual error, part 1 of the standard. Planar statics supplies three scalar equations, not two: $\sum F_x=0$, $\sum F_y=0$, $\sum M=0$. The problem's own geometry is what reduces three to two — every unknown here is vertical, so $\sum F_x=0$ reads $0=0$ and says nothing about the $R_i$. Stated as it is, a reader carries away a false general rule and will miscount the next indeterminate problem they meet. Replacement:

```html
<p><b>(a)</b> Three unknown reactions $R_1,R_2,R_3$. Planar statics supplies three scalar equations, $\sum F_x=0$, $\sum F_y=0$ and $\sum M=0$, but here every unknown is vertical, so $\sum F_x=0$ reads $0=0$ and carries no information about the $R_i$. Two useful equations remain: vertical balance $R_1+R_2+R_3=W$ and one moment balance about any point.
```

### B18. K7's turning point cannot be found the way the problem implies

Locations: `module03.html:2048` (statement and code) and `module03.html:2053` (solution).

Quoted (line 2048): "Measure the period of the constrained swing (twice the time between turning points)."

Missing part 5 of the standard: the instruction as written does not produce the answer the solution quotes. Running the lab and taking the first sign change of $\dot x_2$ returns $t=0.0731$ s, because the hand moves *outward* by $1.6$ mm ($x_2:0.3584\to0.3600$ m) before it turns. That is not solver drift. Bone 1, bone 2 and the rail form an *offset slider-crank*, and the $40^\circ$ release pose sits just short of the slider's outermost reach, so $x_2$ rises for the first $3.7^\circ$ of the swing. The same maximum appears with the Baumgarte gains set to zero and in an independent reduced-coordinate integration that has no stabilization term at all (`indep_reduced.py`, `indep_all.py`: maximum at $t=0.0731$ s in both). Doubling that start-up maximum gives $0.15$ s rather than $1.51$ s. The turning point is the first *minimum* of $x_2$, at $t=0.7561$ s, and only a test for a negative-to-positive velocity crossing finds it. A reader following the stated instruction gets an answer an order of magnitude wrong and no clue why. The replacement statement says so, and the replacement code tests for the minimum explicitly:

```html
<p>Measure the period of the constrained swing (twice the time to the first turning point) and compare it with a simple pendulum whose length is the limb's centre-of-mass distance. Take care over what counts as the turning point, because the hand does not start by moving inward. Bone&nbsp;1, bone&nbsp;2 and the rail form an <em>offset slider-crank</em>, and the $40^\circ$ release pose sits just short of the slider's outermost reach, so $x_2$ first <em>rises</em> — from $0.3584$ to $0.3600\ \mathrm m$ — and turns over about $3.7^\circ$ into the swing, at $t=0.073\ \mathrm s$. That is real kinematics and not solver drift: the constraint error never exceeds $10^{-6}\ \mathrm m$ (problem K9), and the same maximum appears with the Baumgarte gains set to zero. It does mean the <em>first</em> sign change of $\dot x_2$ is that outward maximum, and doubling it gives $0.15\ \mathrm s$. The turning point is the first <em>minimum</em> of $x_2$.</p>
```

and the solution states the turning time before doubling it:

```html
<p>The hand reaches its innermost point at $t=0.756\ \mathrm s$, so the constrained limb's period is $2\times0.756=1.51\ \mathrm s$; a simple pendulum of length $L_{\text{com}}=0.43\ \mathrm m$ gives $\approx1.31\ \mathrm s$.
```

### B19. "Kinematic redundancy" names two different things in one module

Locations: `module03.html:1551` (§8.2), against `module03.html:1667` (a §9.1 diagnostic) and `module03.html:1904` (C10's solution).

Quoted (line 1551): "the body has more muscles than degrees of freedom — a <em>kinematic redundancy</em> resolved only by optimization (Modules 5 and 7)." Quoted (line 1667): "The arm can still flex its elbow while the hand stays put: the <em>kinematic redundancy</em> of §2." Quoted (line 1904): "the muscle-redundancy problem flagged in §8."

Missing part 2 of the standard and a direct violation of the house rule that a symbol or term means one thing for the whole module. Line 1667 uses "kinematic redundancy" correctly: more joint freedoms than the task needs, so the configuration can change with the task output fixed. Line 1551 applies the same phrase to a different gap — more actuators than freedoms, so the *forces* are underdetermined at a fixed configuration. These are not the same problem: the first is about the null space of a task Jacobian, the second about the null space of a moment-arm matrix, and only the second changes the joint reaction. C10 then cross-references §8 by the name §8 does not use. "Resolved only by optimization" is also an overclaim: optimization is one way to pick a point in the null space, not the only one. Replacement for line 1551's clause:

```html
and the body has more muscles than degrees of freedom. That is <em>muscular redundancy</em> (equivalently, actuator redundancy): the motion fixes the net moment the muscles must produce but not how they divide it, so infinitely many force patterns give the same motion while each presses a different reaction across the joint (problem C10 works this through). It is a different gap from the <em>kinematic redundancy</em> of the diagnostics in <a class="secref" href="#diagnostics">§9.1</a>, where a limb keeps more joint freedoms than its task needs and can move while the hand stays put. Muscular redundancy closes only by adding a selection criterion — least effort, least fatigue, least metabolic cost — which is an optimization, and Modules&nbsp;5&nbsp;and&nbsp;7 choose one explicitly.
```

### B20. The module never places its models on the level ladder

Location: `module03.html:172` (the end of §0).

`EDITOR_DOMAIN.md:73-75` is explicit: "Each module states which level its models sit on. A Level-1 statics estimate presented as a dynamic result is a defect." Module 3 states nothing, and it commits precisely the error the rule exists to prevent: §4.2's static $2.5\,W$ is set beside gait bands three times (B14) with no marker that it is a different kind of number. Modules 1 and 2 both carry the statement (`module01.html:135`, `module02.html:158`); Module 3 is the gap. Insert before the "Builds on" line at 172:

```html
<p>The models here sit on three rungs of the course's level ladder, and it is worth fixing which model sits where before any number is quoted. <a class="secref" href="#config">§1</a> and <a class="secref" href="#taxonomy">§2</a> sit below the ladder entirely: they are kinematics, counting freedoms with no force in them at all. <a class="secref" href="#reaction">§4</a> and <a class="secref" href="#stability">§6</a> are <b>Level 1</b> (static equilibrium of rigid segments) — the $2.5\,W$ hip reaction and the stability ratio $S=\tan\beta$ are both single-instant force balances with every acceleration set to zero. <a class="secref" href="#contact">§5</a> is the elastic corner of <b>Level 6</b> (contact and lubrication), used only to convert a force into a peak pressure. <a class="secref" href="#forces">§3</a> and <a class="secref" href="#lab">§7</a> are <b>Level 3</b> (planar multibody link-segment models), and <a class="secref" href="#lab">§7</a> is the only section that integrates in time. Nothing here reaches <b>Level 5</b>: there is no muscle model anywhere in this module, only a muscle force taken as known. A static number read as a dynamic one is the standing hazard — <a class="secref" href="#reaction">§4</a> says so where it happens.</p>
```

(Ladder rungs from `prompt.txt:286-296`: Level 1 static equilibrium, Level 3 multibody link-segment, Level 5 muscle-tendon actuator, Level 6 contact/friction/lubrication.)

### B21. The held mass has weight but no inertia, and nothing says so

Locations: `module03.html:2001` (K1's solution), `module03.html:1988-1992` (K1's code and statement), and the §9.4 preamble at `module03.html:1984`.

Quoted (K1's solution, line 2001): "This is Problem&nbsp;1(a) made quantitative: the held weight is vertical, parallel to the rail's reaction direction, so the contact absorbs precisely $m_L g$ and the joints never feel it. The motion itself is also unchanged — the trajectory does not depend on $m_L$, only the contact force does."

Missing part 4 of the standard, the limit case, and part 1, a precise statement. K1's code adds the held mass to the applied force only:

```
mL = 5.0                                   # held hand mass (kg)
Q = np.array([0, -m1*g, 0, -(m2+mL)*g])
```

$M$ is left at $\mathrm{diag}(m_1,m_1,m_2,m_2)$. So `mL` is a *weight without inertia*, not a mass, and the headline claim — contact up by exactly $m_Lg$, joint reactions and trajectory untouched — is a property of that idealization rather than of a limb carrying a bag. Nothing in the module says so. The whole of K1, half of K2, and the K1 figure caption ("the joint reactions do not move") rest on it.

Two independent re-implementations written for this pass settle both halves. Re-run with the load in $M$ as well (`M = np.diag([m1, m1, m2+mL, m2+mL])`), over the same $m_L=0,5,10$ kg sweep:

| $m_L$ | rail peak $R_s$, weight-only | rail peak $R_s$, with inertia | rail peak contact, weight-only | with inertia |
|---|---|---|---|---|
| 0 kg | 32.61 N | 32.61 N | 22.32 N | 22.32 N |
| 5 kg | 32.61 N | 57.45 N | 71.37 N | 74.95 N |
| 10 kg | 32.61 N | 79.73 N | 120.42 N | 130.93 N |

The invariance is gone: at 10 kg the shoulder sees 2.4 times what the module says it sees. The mechanism is the moved mass, not a faster swing: with the load in $M$ the peak speed *falls* from $1.2554$ to $0.6576\ \mathrm{m\,s^{-1}}$ and the peak $|\dot J_c\dot q|$ from $0.837$ to $0.429$ (`indep_mech.py`), so the reaction rises because the pin is accelerating a hand nearly eight times heavier, more slowly. (In K2's *wall* case, by contrast, the same print shows both quantities rising with the load, which is why B1c's explanation there stands.) The qualitative lesson (the rail carries far more of a vertical load than a wall can) survives and in fact strengthens, so the repair is not to delete K1 but to prove the exact case and then price it. The exact case *is* exact: the added force is $-m_Lg$ in the fourth slot of $Q$ and nowhere else, the rail's constraint gradient is $\nabla g_3=(0,0,0,1)$, so the addition equals $J_c^{\mathsf T}\delta$ with $\delta=(0,0,-m_Lg)$. Substituting a right-hand-side perturbation of that form into (7.6) leaves the acceleration block untouched and shifts only the multiplier, $\lambda_3\to\lambda_3+m_Lg$. A change in $M$ is *not* of that form, which is exactly why inertia breaks it.

Replacement for K1's closing paragraph (line 2001), which now proves the cancellation and names what it costs:

```html
<p>This is Problem&nbsp;1(a) made quantitative, and the cancellation is exact rather than approximate. The held weight adds $-m_Lg$ to the fourth slot of $Q$ and to no other slot, while the rail's constraint gradient is $\nabla g_3=(0,0,0,1)$, which points into that slot and no other. The addition can therefore be written $J_c^{\mathsf T}\delta$ with $\delta=(0,0,-m_Lg)$, and substituting it into (7.6) leaves the acceleration block untouched and moves only the multiplier, $\lambda_3\to\lambda_3+m_Lg$. So the contact absorbs precisely $m_Lg$, the joints never feel it, and the trajectory does not depend on $m_L$ at all — which is why the table's increments are $5g$ and $10g$ exactly, not to two figures.</p>
<p><b>What that exactness costs.</b> It belongs to the model, not to a real bag. As the preamble to these problems said, $m_L$ enters $Q$ but not $M$: this load has weight and no inertia, and the proof just given used precisely that, because a change in $M$ is not of the form $J_c^{\mathsf T}\delta$. Give the load its inertia as well — <code>M = np.diag([m1, m1, m2 + mL, m2 + mL])</code> — and the invariance goes. Over the same $m_L=0,\ 5,\ 10\ \mathrm{kg}$ sweep the peak shoulder reaction then runs $32.6\to57.5\to79.7\ \mathrm N$ and the peak contact $22.3\to75.0\to130.9\ \mathrm N$, because the shoulder pin must now accelerate a hand nearly eight times heavier. The swing is in fact <em>slower</em> — the peak speed falls from $1.26$ to $0.66\ \mathrm{m\,s^{-1}}$ and the peak $|\dot J_c\dot q|$ from $0.84$ to $0.43$ — so it is not that the limb swings harder; it is that the inertial part of the reaction scales with the mass being moved, and the extra mass more than repays the lost speed. The load-path lesson survives and sharpens; only the exact cancellation is a property of the inertia-free load, and anyone modelling a real carried bag must add $m_L$ in both places. <b>Going further:</b> swap the rail for a wall (constraint <code>x2 - xw</code>, Jacobian row <code>[0,0,1,0]</code>) and the same held weight drives the shoulder reaction up instead — Problem&nbsp;1(c), and K2 next.</p>
```

The §9.4 preamble's `mL` sentence gains the same statement in one clause, and K2's solution gains a parenthesis so that its flat $32.6\ \mathrm N$ carries the caveat where it is quoted.

### B13d. The hip marker does not sit on its own curve

Location: `module03.html:1151` (the marker circles of the §6.2 figure).

Quoted: `<circle cx="352.5" cy="149.1" r="4" fill="#7a1f1f"/>`

Factual error, found by decoding the figure rather than by reading it. Calibrating from the figure's own tick `<text>` elements — $x=60+6.5(\beta-10)$ from the five x ticks, $S=(250-y)/73.333$ from the four left ticks — the hip marker at $x=352.5$ sits at $\beta=55^\circ$, where $S=\tan 55^\circ=1.4281$ and the correct $y$ is $145.3$. At $y=149.1$ the marker reads $S=1.376$, which is $\beta=54^\circ$: it was placed at the neighbouring *polyline vertex* rather than on the curve at its own $x$. The dot therefore floats 4 px below the curve it is meant to mark, half a marker radius. The shoulder marker at $(138, 220.4)$ is correct because $x=138$ happens to be a vertex. Replacement: `cy="145.3"`.

Both polylines in this figure were then decoded point by point against the same calibration (`decode_fig62.py`). The red curve reproduces $S=\tan\beta$ to $6\times10^{-4}$ and the regenerated blue curve reproduces $\mathrm{ROM}(\beta)/\mathrm{ROM}(10^\circ)=(150^\circ-\beta)/140^\circ$ to $2\times10^{-4}$, over all sixteen points, on one shared $x$ mapping.

## 3. Style and clarity edits

Line-level, applicable in one pass.

1. `module03.html:233` — "the number of independent quantities that can be varied independently". X-is-X. Read: "the number of quantities that can be varied independently — the dimension of the set of reachable configurations."
2. `module03.html:798` — "almost all of it (566 of the 630 N) is the muscle's doing" reads as if $R$ were a part of $F_m$. Read: "and it is the muscle, not the bag, that puts it there: the muscle pulls with 630 N and the bag with 49 N."
3. `module03.html:798` — "the joint carries twelve times that" against $566/49=11.6$. Read "eleven and a half times".
4. `module03.html:857` — "the honest resultant magnitude is $\approx2.6$–$2.8\,W$" states a range with no source for the spread. Read: "the honest resultant magnitude is $2.7\,W$ at $\alpha=30^\circ$, and $2.6$ to $2.8\,W$ across the $\alpha=20^\circ$ to $40^\circ$ range the abductor line spans between subjects".
5. `module03.html:874` — the SVG label reads "Wₛ ≈ 0.84 BW" where the text uses $W_s=\tfrac56W=0.83\,W$ and the Appendix says $0.85$. Set all three to `5/6 ≈ 0.83`; the Appendix row at line 2132 also uses the symbols $W_b',W_b$, which appear nowhere in §4 — change them to $W_s,W$.
6. `module03.html:1058` — "As the half-width $a$ falls" against §5.2's "a circular patch of radius $a$". Read "as the contact radius $a$ falls".
7. `module03.html:962` — "A couple of atmospheres' worth of pressure" is loose on a page that has just computed 1.7 MPa. Read: "About 17 atmospheres, carried for a lifetime".
8. `module03.html:1039` — the osteoarthritis loop is right but unquantified beside a quantitative figure. Add one clause: "each millimetre lost from a 20 mm contact raises the peak pressure by 11 %, and each millimetre lost from a 7 mm contact raises it by 36 % — the loop tightens as it runs."
9. §0, lines 108, 112, 118, 120, 122 — `<span class="secref"><a class="secref" href="#config">§1</a></span>` nests a `secref` span around a `secref` link. The outer span is a leftover from `autolink_sections.py` and does nothing. Strip the outer spans.
10. `module03.html:573` — "Real joints are idealizations." A joint is not an idealization; the model of it is. Read: "Real joints only approximate these types."
11. `module03.html:1352` — "a single clean oscillation" repeats "clean" from line 1266's parenthesis, which is also the stronger claim and belongs beside the plot. Cut "clean" from 1352.

12. `module03.html:1971` — D9 asks for a mass matrix in $(\theta_1,\theta_2)$ but never says what they measure from; the solution silently assumes $\theta_2$ is relative. Read: "For a planar two-link limb with joint angles $(\theta_1,\theta_2)$, where $\theta_1$ is measured from the horizontal and $\theta_2$ is the *relative* angle at the elbow (so the second link points along $\theta_1+\theta_2$), point masses ..."
13. `module03.html:1848` — C3's solution is entirely qualitative next to a figure that carries numbers. Add: "the figure in §4.3 puts numbers on it, with $b$ cut from 10 cm to 2.8 cm dropping $R$ from $2.5\,W$ to $1.3\,W$."
14. `module03.html:1488` — "made the shoulder reaction in §7 nearly triple over a swing" beside a lab that computed the factor. Add: "The lab's own factor was $2.80$ between the static and the moving value of the *same* reaction."
15. `module03.html:1910` — "computed checks are given where they exist" tells the reader nothing about which. Read: "Two of the ten close with a numerical check: D1 recovers $|\lambda|L=mg$ for a hanging mass, and D3 reproduces the $2.5\,W$ of (4.1)."
16. `module03.html:669` — "The $\dot J_c\dot q$ term is the force needed to keep the body curving along the constraint". It is not a force; it is an acceleration, and calling it a force in the sentence that introduces (3.5) invites a dimensional error. Read: "The $\dot J_c\dot q$ term is the centripetal part: not a force, but the acceleration $J_c\ddot q$ must cancel merely to keep the body curving along the constraint."
17. `module03.html:1943` — the same phrase in D4's solution. Same fix.
18. `module03.html:1146` — the hip marker circle at $(352.5,\,149.1)$ is drawn on top of the "stability $S=\tan\beta$" label at $(300,150)$, so the dot renders as the label's equals sign. Move the label to $x=232$, which keeps it above its own curve and clear of both markers.

## 4. Structural notes

- **§9.4 needs one contract, stated once.** The ten K problems are edits to one script, which is the right design, but nothing says what the script's interface is. Fixing B3 by turning §7.4 into `run(**params) -> h` and saying so in the §9.4 preamble makes all ten reproducible with no other change to nine of them.
- **§5.1 and §5.2 reach the contact patch twice, independently, and never notice.** §5.1 asserts $A_c\approx10\ \mathrm{cm^2}$ and §5.2 derives a Hertz radius implying $10.1\ \mathrm{cm^2}$. Forward-referencing §5.2 from §5.1's worked number, as B9 does, turns two assumptions into one derivation.
- **§6 is the only section whose central quantity is never computed.** $S=\tan\beta$ is one line, but the sensitivity is not: $dS/d\beta=\sec^2\beta$ is 3.0 at the hip and 1.16 at the shoulder, so 5° of lost effective coverage removes 10 % of the shoulder's stability and 17 % of the hip's. That is the quantitative form of §6.3's "a torn labrum measurably lowers $S$", and it is worth a computed figure or a K problem. **Left open by this pass**: adding a K problem is new content, not an edit, and the §9.4 slate is full at ten. Recommend it for the next revision of §6.
- **Nothing states the level the module's models sit on.** *(Closed by B20; the other three notes are closed by B3d, B9b and, for the section 6 sensitivity, left open - see below.)* `EDITOR_DOMAIN.md` requires each module to place itself on the level ladder. §4 is Level 1 statics, §5 Level 2 elastic contact, §7 Level 3 constrained multibody dynamics, and §4.2's "$\approx2.5\,W$ standing on one leg" is repeatedly set beside gait numbers a level above it. One sentence in §0 and one in §4.4 would stop a reader carrying the static number into a dynamic claim.

## 5. What already works

- **§3.4, the pendulum, is the best worked example in the course so far.** It takes a result the reader already knows — $T=mg(3\cos\theta-2\cos\theta_0)$ — and derives it from the multiplier machinery, so the machinery is validated rather than merely applied. Both limits check by hand ($2mg$ at the bottom, $\tfrac12 mg$ at the extremes) and the animation drives its keyframes from the formula the text derives. This is the shape every "here is an abstract method" section should take.
- **§3.5 earns the §7 design decision before §7 needs it.** Explaining that reduced coordinates project the constraint force out of the equations, one section before the lab commits to redundant Cartesian coordinates, is exactly the dependency order the standard asks for. The §7.1 callback closes it.
- **The Grübler–Kutzbach derivation (`module03.html:561-567`) is proved in the smallest setting that shows the mechanism**, then specialized to the serial chain the reader needs, with the independence hypothesis stated and its role identified. Proposition 3.2's invertibility argument does the same.
- **§7's physics is correct and the code reproduces every headline number in §7.5 and §7.6.** The Cartesian-coordinate choice, the constant diagonal $M$, the $3\times4$ Jacobian, the sanity check that a hanging mass gives $|\lambda|L=mg$, and the Baumgarte correction are all right, and the lab's output matches the prose to three figures once the prints are added.
- **§4.2's inclined-abductor correction is the model of how to handle an idealization honestly.** It states the simple answer (2.5 $W$), redoes the balance with the real muscle line, gets 2.7 $W$ tilted 21°, explains that the two are the same analysis read to different fidelity, and reconciles both with the telemetry range. Every one of those numbers checks. Do this everywhere.
- **§6.1's proof of the stability ratio** derives a clinically named quantity from a cone-geometry argument in six lines, notes that $S$ is independent of $N$, and draws the right conclusion: loading the joint harder raises the dislocating force in proportion. Only its unstated assumptions (B12) are missing.

## 6. Changes applied

All 21 blocking defects and all 18 style edits are applied to `edited/module03.html` by one re-runnable script, `scratchpad/m03/apply.py`, which asserts each of its 68 anchors occurs exactly once before it writes anything (70 logged edits: the 68 anchors plus the 18-site `secref` sweep and the inserted footnote). Reproduce the whole file with `cp module03.html edited/module03.html && python apply.py`; the script is deliberately not idempotent, so a second run fails its pre-flight rather than double-applying. The Python that the replacements splice into the page lives in `scratchpad/m03/codeblocks.py`; `scratchpad/m03/test_codeblocks.py` writes each block to disk, runs `pycodestyle` on it, executes it, and diffs stdout against the block's own `# ->` comment lines. All nine blocks pass both checks, so every number printed inside a code block in the shipped page is a number that block actually produces. The independent re-implementations that settled the disputed values are `lab.py` (the §7.4 lab as `run(L1, L2, m1, m2, mL, g, yh, amp, gd, gp, dt, nstep, wall, xw) -> dict of arrays`, building its release pose from the release angle), `verify.py`, `verify2.py` and `verify3.py`.

Two numbers in the first draft of this report did not survive that re-verification and were corrected here: B7's peak forces (the elbow and wrist peaks were 41.46 N and 16.68 N, not 36.73 N and 10.88 N, and they must be read over the seated window that ends at $t=1.81$ s), and B13's mobility curve, which had to be regenerated rather than merely re-captioned.

**A third, independent re-verification** was then run before the file was gated, because a re-implementation that shares the original's formulation cannot expose a defect in that formulation. `indep_all.py` re-derives the whole lab in joint-ANGLE coordinates: a numerically assembled mass matrix, an adaptive RK45 integrator, constraints satisfied exactly by construction with no Baumgarte term, and the joint forces recovered afterwards from Newton's equations on the point masses by least squares (maximum residual $3.9\times10^{-14}$ N, so the recovery is exact and over-determined). `indep_baum.py` independently re-types the module's own Cartesian KKT loop from the printed page. The two agree with each other, and with `lab.py`, to 0.01 N on every number in this report:

```
W_L 34.335 N;  Rs 11.640 N at release (0.3390 W_L), 32.605 N peak (0.9496 W_L), ratio 2.8012
Re peak 11.605 N;  contact 17.561 N at release, 22.324 N peak, 6.216 N min
x2 0.35839 -> 0.36000 (max, t=0.0731 s) -> -0.02729 m (min, t=0.7562 s);  period 1.5124 s
L_com 0.4286 m -> simple-pendulum period 1.3133 s
max |g| 1.0267e-06 stabilised / 2.1562e-05 unstabilised, ratio 21.00
B7 three-link, release: Rs 19.06, Re 5.26, Rw 2.90, Nc 11.55 N;  lam4 < 0 from t = 1.8117 s
   seated peaks: Rs 66.49, Re 41.45, Rw 16.67, Nc 19.87 N
B9 Hertz: E* 6.667 MPa / 9.341 GPa (ratio 1401), a 17.955 mm, pi a^2 10.13 cm^2,
   p0 2.54 MPa / 318.05 MPa, ratio 125.2
B6 cane: F_ab 1.6667 -> 0.7667 W, R 2.5000 -> 1.4500 W, drop 1.0500 W
B5 lean: b = 10 / 2.8 / 1.6 / 0 cm  ->  R = 2.500 / 1.300 / 1.100 / 0.833 W
B2 elbow: Fm 629.67 N, R 565.67 N, 11.54x load;  d = 0.05 m -> 377.80 / 313.80 N, -40 %
B12 mu/tan b = 0.350 % hip, 1.238 % shoulder;  S8 (20/19)^2 = +10.8 %, (7/6)^2 = +36.1 %
```

Every one of those matches what the applied file now says. The one thing the independent method did **not** confirm is B1's rail column, and that turned out to be a defect in the module rather than in the report: `indep_all.py` gives the held mass its inertia, the module's code does not, and the difference is a factor of 2.4 in the peak shoulder reaction at $m_L=10$ kg. That is the new **B21**, applied as tags B21a-c. The report's B1 numbers are correct *for the module's own model* and were left as they stand; B21 states that model and prices it. `decode_fig62.py` then inverted the one regenerated figure (B13) back into data, which surfaced **B13d**.

| tag | line (original) | what changed | how verified |
|---|---|---|---|
| B1a | 2006 | K2's statement now fixes $x_w=0.30$ m, says the hand starts on the wall, and asks "by how much" | without the pose the numbers are irreproducible; the pose is what `run(wall=True, xw=0.30)` uses |
| B1b | 2006 | K2's code fragment replaced by a complete program that imports `run()` and prints the rail-versus-wall sweep | `test_codeblocks.py`: block runs, stdout matches its `# ->` lines exactly |
| B1c | 2014 | K2's solution numbers replaced. Rail $R_s$ 19.7 N → 32.6 N (pinned for every $m_L$); rail contact 14.7→112.8 N → 22.3→120.4 N; wall $R_s$ 20.6→26.3 N → 57.9→121.2→187.3 N, a factor 3.2 rather than the 1.28 the old text implied | `verify.py` load sweep $m_L=0/5/10$ kg, rail and wall, peak over the swing |
| B2a | 1929 | D2's parameters moved to Module 1's reference human: $W_{\text{load}}$ 50→49 N, $d$ 0.05→0.03 m, $c$ 0.17→0.116 m, and a second case at $d=0.05$ m added | `EDITOR_DOMAIN.md` reference-human row (elbow moment arm 0.03 m, forearm+hand CoM 0.116 m) |
| B2b | 1931 | D2's solution now gives $F_m=630$ N and $R=566$ N (was 401 and 336) and $11.6\times$ the load (was $6.7\times$); the $d=0.05$ m case gives 378 N and 314 N | hand arithmetic, printed: $(49(0.35)+15(0.116))/0.03=630.4$; $(17.15+1.74)/0.05=377.8$; $1-378/630=0.40$ |
| B2c | 2131 | Appendix elbow row rewritten to the same reference-human values, so the module's own parameter table stops contradicting §4.1 | same arithmetic |
| B3a | 1306 | §7.4 code: Baumgarte gains renamed `a, b` → `gd, gp` | `test_codeblocks.py` PEP8 + run |
| B3b | 1334 | §7.4 code tail: the hardcoded `q = np.array([0.193, -0.230, 0.358, -0.48])` replaced by a pose built from the release angle, plus a history dict and six `print` calls with their output | `test_codeblocks.py`: prints 34.34 N, 11.64 N (0.34 $W_L$), 32.61 N (0.95 $W_L$), 11.61 N, 22.32/6.21 N, 1.03e-06 m — matching the block's own `# ->` lines |
| B3c | 1298 | §7.4's "fully runnable" paragraph now says the printed output is every headline number of §7.5 and names the `run(**params) -> h` contract | read against the new block |
| B3d | 1984 | §9.4's preamble states the `run(**params)` contract once, for all ten K problems, replacing the unbacked promise that every number was produced by running the code | the promise is now true: see the `test_codeblocks.py` row above |
| B3e | 1988 | K1's block: the live `<a class="secref">` tag inside `<pre><code>` replaced by plain text (this was B4) | grep for `<a ` inside a `<pre><code>` in `edited/module03.html` returns 0; `test_codeblocks.py` PEP8 |
| B3f | 2032 | K5's fragment (called `Rs_history`, defined nowhere) replaced by a complete program printing 11.64 N, 32.61 N and the amplification 2.80 | `test_codeblocks.py` run |
| B3g | 2040 | K6's fragment (called `release_pose`, defined nowhere) replaced by a complete amplitude sweep printing 20.66 / 22.37 / 25.75 / 32.61 / 48.39 N | `test_codeblocks.py` run; same values as `verify.py` |
| B3h | 2048 | K7's fragment (called `time_of_first_turning_point`, defined nowhere) replaced by a program that tests for the first *minimum* of $x_2$ and prints 0.756 s, 1.51 s, 0.43 m, 1.31 s | `verify3.py` lists every sign change of $\Delta x_2$: start-up maximum at $t=0.0731$ s, first minimum at $t=0.7561$ s |
| B3i | 2057 | K8's fragment (called `solve_kkt`, defined nowhere) replaced by a program printing $\min\lambda_3=10.71/6.21/-5.88$ N for release 30/40/50° | `test_codeblocks.py` run; `verify2.py` independently |
| B3j | 2065 | K9's fragment replaced by a program printing 1.03e-06 m, 2.16e-05 m and the factor 21 | `test_codeblocks.py` run |
| B5 | 936 | the lean caption's $\approx1.1\,W$ replaced by $\approx1.3\,W$ with its $b$ stated (10 cm → 2.8 cm), "more-than-twofold" corrected to a factor 1.9, and the $0.83\,W$ floor at $b=0$ added | `verify2.py` $R$-versus-$b$ table: $b=10$ cm → $2.500\,W$, $b=2.8$ cm → $1.300\,W$, $b=1.6$ cm → $1.100\,W$, $b=0$ → $0.833\,W$ |
| B6 | 939 | the cane's ungraded "$\sim$1 body weight" replaced by the free body, the balance $F_{ab}a+F_cd=W_sb$, and the arithmetic for an assumed $F_c=0.15\,W$ at an assumed $d=0.30$ m | `verify2.py` cane block: $F_{ab}$ $1.667\to0.767\,W$, $R$ $2.500\to1.450\,W$, drop $1.050\,W$ |
| B7a | 2072 | K10's statement now supplies $L_3=0.25$ m, $m_3=1.0$ kg, $y_h=-0.68$ m and the release pose, and asks whether §7.5's proximal-carries-more ranking survives | the four forces were unreproducible without them |
| B7b | 2072 | K10's three comment lines replaced by a complete $10\times10$ KKT program that prints release forces, the lift-off time and the seated-window peaks | `test_codeblocks.py` run; the same numbers come out of `verify3.py`'s independently written `run3()` |
| B7c | 2076 | K10's asserted forces (shoulder $\approx$20, elbow $\approx$2, wrist $\approx$11, contact $\approx$21 N — an ordering that inverted §7.5's own finding) replaced by release 19.06 / 5.26 / 2.90 / 11.55 N and seated-window peaks 66.49 / 41.46 / 16.68 / 19.87 N, with $\lambda_4$ going negative at $t=1.81$ s | `verify3.py`: release and peaks as listed, first negative $\lambda_4$ at $t=1.8117$ s, maximum constraint error $4.15\times10^{-6}$ m |
| B8 | 2068 | K9's drift factor $15\times$ → $21\times$ and $1.5\times10^{-5}$ m → $2.2\times10^{-5}$ m, plus the observation that the stabilized error is still falling at the end while the unstabilized one peaks on the last step | `verify.py` Baumgarte on/off over the same 40 000 steps: 1.027e-06 m (final 6.51e-07) against 2.156e-05 m (final 2.156e-05), ratio 21.00 |
| B9a | 1001 | §5.3's effective moduli corrected, 6 MPa → 6.7 MPa and 9 GPa → 9.3 GPa, and the two Poisson ratios stated ($\nu_{\text{cart}}=0.5$, $\nu_{\text{bone}}=0.3$ — the second appeared nowhere in the module) | `verify2.py` Hertz block from Definition 5.2: $E^*_{\text{cart}}=6.667$ MPa, $E^*_{\text{bone}}=9.341$ GPa, ratio 1401 |
| B9b | 1030 | the Hertz caption: $p_0$ 2.4 → 2.5 MPa, ratio 130 → 125, and the contact radius $a=17.9$ mm with patch area $\pi a^2=10.1\ \mathrm{cm^2}$ added, which turns §5.1's asserted $A_c$ into a derived one | `verify2.py`: $a=17.95$ mm, $\pi a^2=10.13\ \mathrm{cm^2}$, $p_0=2.5$ MPa and 318.0 MPa, ratio 125.2 |
| B10a | 269 | the $\sim$240 whole-body DOF row gains a footnote marker | see B10d |
| B10b | 1055 | the SVG label "cartilage damage ≈15 MPa" → "≈15–25 MPa", so the two figures ten lines apart agree | direct comparison with the band drawn at line 1011 |
| B10c | 2144 | eleven rows added to Appendix B — $E_{\text{cart}}$, $E_{\text{bone}}$, $\nu_{\text{bone}}$, $E^*$, $R_{\text{eff}}$, $a$ and $\pi a^2$, $p_{\text{dam}}$, $\beta$, $\theta_n$, $S$, and the 3–5 $W$ gait band — each marked derived or assumed | every value in the table is either computed above (and printed by `verify2.py`) or carries "(assumed)" |
| B10d | 269 | the footnote itself: the $\sim$240 count broken into pelvis 6, spine and neck $\approx$25, 7 per limb, $\approx$20 per hand, and declared an order-of-magnitude count | the per-limb 7 is the serial-chain sum (2.1) already proved in §2 |
| B11a | 1294 | the Baumgarte gains renamed $\alpha,\beta\to\gamma_d,\gamma_p$ in §7.3's prose, with the damping and restoring roles named and the critically damped choice stated | removes the collision with §4.2's abductor tilt $\alpha$ and §6's rim angle $\beta$ |
| B11b | 2065 | K9's statement renamed to $\gamma_d=\gamma_p=0$ | same rename |
| B11c | 2107 | the single $\alpha,\beta$ notation row replaced by four rows covering §4.2 ($F_{ab},a,b,\alpha$), §5.2 ($R_{\text{eff}},p_0,a$), §6.1 ($N,F_t,\varphi,\theta_n$) and §7.3 ($\gamma_d,\gamma_p$) | each symbol now has a row naming its section of first use |
| B11d | 2110 | the "Symbol reuse, flagged" note rewritten as "resolved": two collisions removed rather than flagged, and the one that remains ($a$) stated with the reason it is safe | flagging a collision is not resolving it (house rule) |
| B11e | 2123 | the Appendix's Baumgarte parameter row renamed to $\gamma_d,\gamma_p$ | same rename |
| B12 | 1084 | a paragraph added after (6.1)'s proof naming its two buried idealizations — frictionless contact and a rigid cup — and costing the first from the Appendix's own $\mu$ | $\mu N/(N\tan\beta)$: $0.005/\tan55^\circ=0.350\,\%$ at the hip, $0.005/\tan22^\circ=1.238\,\%$ at the shoulder. This also gives $\mu\approx0.005$ its first use in the module |
| B13a | 1148 | the mobility polyline regenerated from $\text{ROM}(\beta)=180^\circ-\beta-\theta_n$ normalized at $\beta=10^\circ$: it now runs $1.00\to0.571$ ($y$ 30 → 124.29), replacing a curve that ran $1.00\to0.25$ and matched no stated formula | 16 points computed in Python as $x=60+26k$, $y=30+220k/35$, against the figure's own right-hand ticks ($m=0$ at $y=250$, $m=1$ at $y=30$) |
| S18 | 1146 | the red "stability $S=\tan\beta$" label moved from $x=300$ to $x=232$, so the hip marker dot at $(352.5,149.1)$ no longer renders as the label's equals sign | figure rendered to PNG and read, then `check_overlap.py` = 0 |
| B13b | 1149 | the mobility label moved from $(208,74)$ — which the regenerated curve passes through at $y\approx66$ — to $(150,162)$, in the empty band between the two curves | `check_overlap.py` = 0 on the whole page, and the figure rendered and read |
| B13c | 1156 | the caption now states the function plotted, $\text{ROM}(\beta)=180^\circ-\beta-\theta_n$ with $\theta_n=30^\circ$ assumed, and reads the difference in curve shape as the content of the trade-off | true of the regenerated curve, by construction |
| B13d | 1151 | the hip marker circle moved from $cy=149.1$ to $cy=145.3$: at its own $x=352.5$ ($\beta=55^\circ$) the curve is at $S=\tan55^\circ=1.4281$, and $149.1$ reads $S=1.376$, so the dot floated 4 px off the curve it marks | `decode_fig62.py`: both polylines and both markers inverted against the figure's own tick coordinates; red reproduces $\tan\beta$ to $6\times10^{-4}$, blue reproduces $(150^\circ-\beta)/140^\circ$ to $2\times10^{-4}$ |
| B14a | 1487 | §8.1's telemetry band "roughly 2–3 $W$" → "$\approx2.3$–$2.9\,W$ in slow level walking", with the 3–5 $W$ of §4.3 reconciled as a faster condition and both marked as quoted, not derived | the two bands were already four lines apart in the file (1487 and 1491) |
| B14b | 859 | §4.3's 3–5 $W$ marked assumed, set beside the telemetry band, and (4.1)'s $2.5\,W$ named a Level-1 static number | level ladder, `prompt.txt:287` |
| B14c | 1394 | §7.5's "gait pushes the peak hip reaction to 3–5 $W$" → "walking and running push", so the band is not attributed to level walking | consistency with B14a |
| B14d | 2036 | the same fix inside K3's solution | same |
| B14e | 2143 | the Appendix telemetry row qualified to "slow level walking" | same |
| B15a | 1935 | D3's $W_b'$ and its unexplained $0.85$ replaced by §4.2's $W_s=\tfrac56W$ | $W_b$ and $W_b'$ appear nowhere else in the module; §4.2 fixes $W_s=\tfrac56W=0.833\,W$ |
| B15b | 1937 | D3's solution now derives $R=W_s(1+b/a)=2.5\,W$ exactly rather than rounding $0.85\times3=2.55$ to it, and compares with telemetry as static-versus-moving | $\tfrac56\times3=2.5$ exactly |
| B15c | 2132 | the Appendix hip row rewritten in $W_s$ with $b$ and $a$ given, and the $2.7\,W$ tilted resultant added beside the $2.5\,W$ vertical one | §4.2's inclined-abductor result |
| B16 | 1755 | C1(b)'s "gravity's along-rail component drove the swing" replaced: the rail is horizontal ($g_3=y_2-y_h$), so gravity has no along-rail component; the driver is the elbow mass pushing through bone 2 | the constraint is stated two sentences earlier in the same solution; `verify.py` gives $\lambda_3=17.56$ N at release against a hand weight of $m_2g=14.72$ N, so the rail carries more than the hand's own weight |
| B17 | 1790 | C2(a)'s "planar statics gives exactly two scalar equations" replaced: statics supplies three, but $\sum F_x=0$ is vacuous when every unknown is vertical, which leaves two useful ones | the general count is three; the reduction is this problem's geometry, not a rule |
| B18a | 2048 | K7's statement warns that the first sign change of $\dot x_2$ is a 1.6 mm start-up maximum at $t=0.07$ s — offset-slider-crank kinematics, not solver drift — and defines the turning point as the first minimum of $x_2$ | `verify3.py`: maximum at $t=0.0731$ s ($x_2$ 0.3584 → 0.3600 m), first minimum at $t=0.7561$ s |
| B18b | 2053 | K7's solution states the turning time 0.756 s explicitly before doubling it to 1.51 s | same run |
| B19 | 1551 | §8.2's "kinematic redundancy", used there for more muscles than freedoms, renamed *muscular redundancy* and distinguished from the kinematic redundancy of §9.1; "resolved only by optimization" replaced by the selection-criterion statement | the module uses "kinematic redundancy" correctly at line 1667 and for a different concept at 1551, and C10 (line 1904) cross-refers to §8 by the name §8 did not use |
| B20 | 172 | a paragraph added at the end of §0 placing every section on the level ladder: §1–§2 kinematics, §4 and §6 Level 1, §5 Level 6, §3 and §7 Level 3, nothing at Level 5 | required by `EDITOR_DOMAIN.md:73-75`; rungs from `prompt.txt:286-296`; matches the form used at `module01.html:135` and `module02.html:158` |
| B21a | 1984 | (folded into the B3d anchor) the §9.4 preamble's `mL` description now states that the held mass enters $Q$ but never $M$, which stays $\operatorname{diag}(m_1,m_1,m_2,m_2)$, and names it as the idealization K1's result depends on | `indep_baum.py` reruns the module's own KKT with `mL` in $M$ as well; see B21c's row |
| B21b | 2001 | K1's closing paragraph replaced. The exact cancellation is now *proved* (the added force is $J_c^{\mathsf T}\delta$ with $\delta=(0,0,-m_Lg)$, so (7.6)'s acceleration block is untouched and only $\lambda_3$ moves by $m_Lg$), and a second paragraph prices the idealization with the inertial numbers | proof checked by hand and by perturbing $Q$ in `indep_baum.py`; the inertial sweep printed by two independent codes. The *reason* for the rise was checked too and the first draft of this sentence had it backwards: `indep_mech.py` prints max $|\dot q|$ falling $1.2554\to0.6576\ \mathrm{m\,s^{-1}}$ and max $|\dot J_c\dot q|$ falling $0.837\to0.429$ when the rail load is given inertia, so the rise is the larger moved mass, not a harder swing |
| B21c | 2014 | (folded into the B1c anchor) K2's solution gains a parenthesis at the flat $32.6\ \mathrm N$: with $m_L$ given its inertia the rail figure rises to $32.6\to79.7\ \mathrm N$ | `indep_baum.py` (module KKT, semi-implicit Euler) 32.61 / 57.45 / 79.73 N and `indep_all.py` (angle-coordinate Lagrangian, RK45, Newton force recovery, residual $4\times10^{-14}$ N) 32.61 / 57.45 / 79.72 N |
| S1 | 231 | Definition 1.2's "independent quantities that can be varied independently" de-duplicated | `check_prose.py` X-is-X class |
| S2+S3 | 798 | "almost all of it (566 of the 630 N) is the muscle's doing" rewritten so $R$ no longer reads as a part of $F_m$; "twelve times that" → "eleven and a half times the load" | $566/49=11.55$ |
| S4 | 857 | the bare range "$\approx2.6$–$2.8\,W$" given its source: $2.7\,W$ at $\alpha=30^\circ$, the spread being $\alpha$ from 20° to 40° | §4.2's own formula evaluated at the endpoints |
| S5 | 874 | the SVG label "Wₛ ≈ 0.84 BW" → "Wₛ = 5/6 ≈ 0.83 BW", so figure, text and Appendix agree | $5/6=0.8333$ |
| S6 | 1058 | "as the half-width $a$ falls" → "as the contact radius $a$ falls", matching §5.2's own definition of $a$ | §5.2 defines a circular patch of radius $a$ |
| S7 | 962 | "a couple of atmospheres' worth of pressure" → "about 17 atmospheres", on a page that has just computed 1.7 MPa | $1.7\times10^6/1.01325\times10^5=16.8$ |
| S8 | 1039 | the osteoarthritis feedback loop quantified: 1 mm off a 20 mm contact is +11 % peak pressure, 1 mm off a 7 mm contact is +36 % | $p_0\propto1/a^2$: $(20/19)^2=1.108$ (+10.8 %), $(7/6)^2=1.361$ (+36.1 %) |
| S9 | 18 sites | 18 leftover `<span class="secref">` wrappers around `secref` links stripped (they came from `autolink_sections.py` and did nothing) | count asserted $\ge18$ in the script; `check_links.py` still 0 broken, 0 unlinked |
| S10 | 573 | "Real joints are idealizations" → "Real joints only approximate these types"; a joint is not an idealization, the model of it is | — |
| S11 | 1352 | the repeated "clean" cut from §7.5's "a single clean oscillation" | it duplicates line 1266's parenthesis |
| S12 | 1971 | D9's statement now says $\theta_1$ is measured from the horizontal and $\theta_2$ is the relative elbow angle, which the solution had silently assumed | the solution's $\phi=\theta_1+\theta_2$ requires it; the derived $M$ was checked by hand and is correct as printed |
| S13 | 1848 | C3's qualitative solution given the numbers from §4.3's figure: $b$ 10 cm → 2.8 cm drops $R$ from $2.5\,W$ to $1.3\,W$ | `verify2.py` lean table |
| S14 | 1488 | §8.1's "nearly triple" given its number: 2.80 | `verify.py` / `lab.py`: 32.61/11.64 = 2.80 |
| S15 | 1910 | §9.3's "computed checks are given where they exist" made specific: D1 and D3 | D1 recovers a pivot reaction of $mg$ for a hanging mass; D3 reproduces $2.5\,W$ after B15b |
| S16 | 669 | §3.3's "the $\dot J_c\dot q$ term is the force needed to keep the body curving" corrected: it is an acceleration, not a force | dimensions: $J_c\ddot q=-\dot J_c\dot q$ |
| S17 | 1943 | the same phrase in D4's solution, same fix | same |

### Gate results

Nine gates, run on the pristine copy before any edit and again on the finished file. Every one is unchanged, and every hard gate is zero.

| gate | baseline | after |
|---|---|---|
| `checktex` | 833 math segments, 0 issues | 1037 math segments, 0 issues |
| `checklt` | 0 | 0 |
| `check_links` | 229 links, 0 broken, 0 unlinked | 258 links, 0 broken, 0 unlinked |
| `check_svg` | 0 hard, 3 advisory | 0 hard, the same 3 advisory |
| `check_code` | 6 blocks, 0 issues | 10 blocks, 0 issues |
| `verify_dom` | 0 mjx-merror, 0 broken, 6 stray `$` (advisory), 0 swallowed prose | identical |
| `check_overlap` | 0 | 0 |
| `check_frame` | 0 clipped; 4 wasted-margin advisories | identical |
| `check_bodyprop` | 0 hairline limbs; 3 advisories | identical |

The three `check_svg` advisories, the four `check_frame` wasted-margin advisories and the three `check_bodyprop` advisories are all pre-existing and none is a hard failure; they were left alone because retightening a viewBox and recutting anatomy are judgement calls outside this pass.
