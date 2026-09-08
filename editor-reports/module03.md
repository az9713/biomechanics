# Editor report: module03.html (Joints as Constrained Interfaces)

Editorial pass. Standard: the five-part rule of the `science-editor` skill, read against `EDITOR_DOMAIN.md`. Every location is `module03.html:LINE`. Every replacement is valid HTML with MathJax delimiters and uses only the box classes the stylesheet defines.

All eleven `<pre><code>` blocks in the file were extracted and run (scratchpad folder `m03/`: `extract.py`, `lab.py`, `verify.py`, `k2k10.py`, `hertz.py`). The §7.4 lab was re-implemented exactly as printed and instrumented with the prints it lacks; it reproduces the module's own headline numbers to three figures, so the model is sound and most of the prose numbers are right. Every number in a replacement below was printed by the code shown beside it.

**What the lab actually prints** (release 40° off vertical, the module's own initial pose):

```
W_L = 34.335 N
Rs peak 32.61 N (0.950 W_L)   Rs at release 11.64 N (0.339 W_L)   ratio 2.80
Nc peak 22.32 N   Nc min 6.21 N     Re peak 11.61 N
x2 sweeps 0.358 -> -0.027 m        max |g| 1.027e-06 m
```

Confirmed correct against that run: K1 (22.3 / 71.4 / 120.4 N; $R_s$ pinned at 32.6 N; increments exactly $m_Lg$), K3 (16.3 / 32.6 / 65.2 N), K4 (31.7 / 32.6 / 33.3 N), K5 (11.6 N, 32.6 N, factor 2.8), K6 (0.60 / 0.65 / 0.75 / 0.95 / 1.41 $W_L$), K7 (1.51 s against 1.31 s, $L_{\text{com}}=0.43$ m), K8 (10.7 / 6.2 / −5.9 N), and every §7.5 and §7.6 figure. Also confirmed by hand: §3.4's pendulum tension ($2mg$ at the bottom, $\tfrac12 mg$ at $\theta_0=60^\circ$), §4.2's inclined-abductor correction (2.68 $W$, tilted 21.1°), §6's stability ratios (1.43, 0.40, ratio 3.53), §5.4's shrinking-contact pressures (2.05 → 16.7 MPa), and the Grübler–Kutzbach derivation.

## 1. Verdict

**Yes, after revision.** A graduate reader with no biomechanics can learn from these pages what a degree of freedom is, why a Lagrange multiplier *is* a joint reaction force, why a hip carries two-and-a-half times body weight while standing on one leg, and why the same three-degree-of-freedom count describes both the hip and the shoulder while only one of them dislocates. Theorem 3.1, Proposition 3.2, the hip reaction (4.1), and the stability ratio (6.1) each carry a proof of matching weight; the §3.4 pendulum is the best worked example in the course so far, because it derives a result the reader already knows and so proves the machinery rather than merely using it. The §7 lab is genuinely runnable and its physics is right.

What stops the reader is elsewhere, and it is concentrated in the numbers rather than the arguments. **The module contains two different, mutually inconsistent elbow examples** — §4.1 uses Module 1's reference human (3 cm moment arm, $F_m=630$ N, $R=566$ N) while D2 and the Appendix parameter table use a 5 cm moment arm and report $F_m=401$ N, $R=336$ N — and the Appendix records only the second, so the module's own reference table contradicts its own §4. **K2's numbers are not reproducible from any run of the module's model:** it reports a rail shoulder reaction of 19.7 N and a rail contact of 14.7 → 112.8 N where the code gives 32.6 N and 22.3 → 120.4 N, and a wall shoulder reaction of 20.6 → 26.3 N where the code gives 57.9 → 187.3 N — understating the effect the problem exists to demonstrate by a factor of five. **§9.4's opening promise, "every number quoted below was produced by running the code," is false as shipped:** the §7.4 lab computes $R_s$, $R_e$ and $\lambda_3$ inside its loop and then discards them without a single `print`, and five of the ten K snippets call names (`solve_kkt`, `release_pose`, `Rs_history`, `time_of_first_turning_point`) that are defined nowhere in the module. A reader who copies the code out cannot reproduce one number in the section. One code block has a live `<a>` tag inside it. Two adjacent figure captions in §4.3 give the leaned hip load as 1.3 $W$ and 1.1 $W$. §5.3's stated Poisson ratio does not produce §5.3's stated effective modulus. Roughly a dozen empirical numbers — socket coverage angles, cartilage and bone moduli, the cartilage damage threshold, the Hertz radius, the 3–5 $W$ gait figure — appear in the prose with no derivation, no "assume", and no Appendix entry, while the one parameter the Appendix does list and the text never uses is the friction coefficient.

None of this touches the four proved results, which are sound. All of it is repairable.

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
    print(f"mL={mL:4.1f} kg | rail Rs peak {rail['Rs'].max():7.2f} N"
          f" contact peak {rail['Nc'].max():7.2f} N"
          f" | wall Rs peak {wall['Rs'].max():7.2f} N")
# -&gt; mL= 0.0 kg | rail Rs peak   32.61 N contact peak   22.32 N | wall Rs peak   57.88 N
# -&gt; mL= 5.0 kg | rail Rs peak   32.61 N contact peak   71.37 N | wall Rs peak  121.22 N
# -&gt; mL=10.0 kg | rail Rs peak   32.61 N contact peak  120.42 N | wall Rs peak  187.28 N</code></pre></div>
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

The repair is one change to §7.4 plus a stated contract for the K problems. Replacement for the tail of the §7.4 code block (from the `# released from rest` comment to the end of the block):

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
print(f"shoulder R_s peak      = {h['Rs'].max():.2f} N = {h['Rs'].max()/WL:.2f} W_L")
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
print(f"peak mid-swing:      {h['Rs'].max():.2f} N = {h['Rs'].max()/WL:.2f} W_L")
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
# -&gt; at release: shoulder 19.06 N  elbow 5.26 N  wrist 2.90 N  contact 11.55 N
# -&gt; peaks:      shoulder 66.49 N  elbow 36.73 N  wrist 10.88 N  contact 19.87 N</code></pre></div>
<details class="sol"><summary>Show solution</summary><div><p>Six coordinates and four constraints make the KKT matrix $10\times10$, and one solve returns <em>all</em> the forces at once: at release, shoulder $19.1\ \mathrm N$, elbow $5.3\ \mathrm N$, wrist $2.9\ \mathrm N$, contact $11.6\ \mathrm N$; over the swing the peaks are $66.5$, $36.7$, $10.9$ and $19.9\ \mathrm N$. The proximal-carries-more ranking of <a class="secref" href="#lab-results">§7.5</a> not only survives, it sharpens: each joint carries the weight and the inertia of everything distal to it, so the ordering shoulder $\gt$ elbow $\gt$ wrist is forced by the model, not observed in it. Note also that the peak shoulder reaction has doubled ($32.6\to66.5\ \mathrm N$) for a limb only 29 % heavier — the extra link swings on a longer arm, and its inertial contribution grows faster than its mass. Nothing about the <em>method</em> changed from <a class="secref" href="#lab">§7</a>; only the sizes of $M$, $J_c$ and the system. The same fifty lines scale from this toy to a research-grade model, and what changes is the realism of those matrices, the subject of <a class="secref" href="#model">§8</a>.</p></div></details>
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
<p><b>What (6.1) assumes, and what it costs.</b> Two idealizations are buried in that proof. First, the contact is <em>frictionless</em>: the head slides on the cup with no tangential resistance, so nothing but geometry holds it in. That is a good assumption here, and its own number says why — a synovial joint runs at $\mu\approx0.005$ (Appendix; the lubrication mechanisms that achieve it are Module 4's subject), so friction adds at most $\mu N=0.005N$ to the $N\tan\beta$ of (6.1), a correction of $0.4\,\%$ for the hip and $1.2\,\%$ for the shoulder. Anywhere else in engineering a joint this smooth would be remarkable; here it means the socket's <em>shape</em> is the entire stability story, which is the point of the section. Second, the cup is <em>rigid</em>, so the rim sits at a fixed angle $\beta$. It does not: the labrum and the cartilage deform under $N$, and a deforming rim both deepens the effective socket at low load and rolls away at high load. <a class="secref" href="#stability">§6.3</a> treats that as a change in the effective $\beta$, which is the cheapest honest repair; resolving it properly needs the contact mechanics of <a class="secref" href="#contact">§5.2</a> run on a deformable rim, which is Module 4.</p>
```

### B13. §6.2's mobility curve is plotted with no equation behind it

Location: `module03.html:1156` (caption) and the plotted curve at `module03.html:1129-1154`.

Quoted: "mobility (blue dashed, a normalized range-of-motion proxy) falls."

Missing parts 1 and 3: a curve is drawn against a computed axis and captioned "(computed)", but the module never says what function was computed. "A normalized range-of-motion proxy" is not a statement a reader can check, and the point of §6.2 is that stability and mobility trade along one dial — a claim that needs both curves to be functions of $\beta$. The trade is derivable from the geometry §6.1 already set up: the head swings until the bony neck strikes the rim, so with a neck half-angle $\theta_n$ the range is $\text{ROM}(\beta)=180^\circ-\beta-\theta_n$, falling linearly in $\beta$ while $S=\tan\beta$ rises faster than linearly. Replacement for line 1156:

```html
<figcaption>The mobility–stability trade-off along socket coverage $\beta$ (computed). Stability $S=\tan\beta$ (red) rises; mobility falls. The mobility curve is the geometric range of motion: the head swings until the bony neck, of assumed half-angle $\theta_n=30^\circ$, strikes the rim, so $\text{ROM}(\beta)=180^\circ-\beta-\theta_n$, normalized here by its value at $\beta=10^\circ$. The two curves have different <em>shapes</em>, and that is the whole content of the trade: mobility falls linearly in $\beta$ while stability rises faster than linearly, so every degree of coverage costs the same range but buys more security than the degree before it. The shoulder lives at the mobile, unstable end; the hip at the stable, restricted end. There is no socket depth that maximizes both — evolution placed each joint where its job demands.</figcaption>
```

Add $\theta_n$ to the notation table and $\theta_n\approx30^\circ$ (assumed) to the parameter table. If the plotted blue curve is not $180^\circ-\beta-30^\circ$ normalized, regenerate it from that formula so the caption is true of the figure.

## 3. Style and clarity edits

Line-level, applicable in one pass.

1. `module03.html:233` — "the number of independent quantities that can be varied independently". X-is-X. Read: "the number of quantities that can be varied independently — the dimension of the set of reachable configurations."
2. `module03.html:798` — "almost all of it (566 of the 630 N) is the muscle's doing" reads as if $R$ were a part of $F_m$. Read: "and it is the muscle, not the bag, that puts it there: the muscle pulls with 630 N and the bag with 49 N."
3. `module03.html:798` — "the joint carries twelve times that" against $566/49=11.6$. Read "eleven and a half times".
4. `module03.html:857` — "the honest resultant magnitude is $\approx2.6$–$2.8\,W$" states a range with no source for the spread. Read: "the honest resultant magnitude is $2.7\,W$ at $\alpha=30^\circ$, and $2.6$ to $2.8\,W$ across the $\alpha=20^\circ$ to $40^\circ$ range the abductor line spans between subjects".
5. `module03.html:874` — the SVG label reads "Wₛ ≈ 0.84 BW" where the text uses $W_s=\tfrac56W=0.83\,W$ and the Appendix says $0.85$. Set all three to `5/6 ≈ 0.83`; the Appendix row at line 2132 also uses the symbols $W_b',W_b$, which appear nowhere in §4 — change them to $W_s,W$.
6. `module03.html:1058` — "As the half-width $a$ falls" against §5.2's "a circular patch of radius $a$". Read "as the contact radius $a$ falls".
7. `module03.html:962` — "A couple of atmospheres' worth of pressure" is loose on a page that has just computed 1.7 MPa. Read: "About 17 atmospheres, carried for a lifetime".
8. `module03.html:1039` — the osteoarthritis loop is right but unquantified beside a quantitative figure. Add one clause: "each millimetre lost from a 20 mm contact raises the peak pressure by 10 %, and each millimetre lost from a 7 mm contact raises it by 33 % — the loop tightens as it runs."
9. §0, lines 108, 112, 118, 120, 122 — `<span class="secref"><a class="secref" href="#config">§1</a></span>` nests a `secref` span around a `secref` link. The outer span is a leftover from `autolink_sections.py` and does nothing. Strip the outer spans.
10. `module03.html:573` — "Real joints are idealizations." A joint is not an idealization; the model of it is. Read: "Real joints only approximate these types."
11. `module03.html:1352` — "a single clean oscillation" repeats "clean" from line 1266's parenthesis, which is also the stronger claim and belongs beside the plot. Cut "clean" from 1352.

## 4. Structural notes

- **§9.4 needs one contract, stated once.** The ten K problems are edits to one script, which is the right design, but nothing says what the script's interface is. Fixing B3 by turning §7.4 into `run(**params) -> h` and saying so in the §9.4 preamble makes all ten reproducible with no other change to nine of them.
- **§5.1 and §5.2 reach the contact patch twice, independently, and never notice.** §5.1 asserts $A_c\approx10\ \mathrm{cm^2}$ and §5.2 derives a Hertz radius implying $10.1\ \mathrm{cm^2}$. Forward-referencing §5.2 from §5.1's worked number, as B9 does, turns two assumptions into one derivation.
- **§6 is the only section whose central quantity is never computed.** $S=\tan\beta$ is one line, but the sensitivity is not: $dS/d\beta=\sec^2\beta$ is 3.0 at the hip and 1.16 at the shoulder, so 5° of lost effective coverage removes 10 % of the shoulder's stability and 17 % of the hip's. That is the quantitative form of §6.3's "a torn labrum measurably lowers $S$", and it is worth a computed figure or a K problem.
- **Nothing states the level the module's models sit on.** `EDITOR_DOMAIN.md` requires each module to place itself on the level ladder. §4 is Level 1 statics, §5 Level 2 elastic contact, §7 Level 3 constrained multibody dynamics, and §4.2's "$\approx2.5\,W$ standing on one leg" is repeatedly set beside gait numbers a level above it. One sentence in §0 and one in §4.4 would stop a reader carrying the static number into a dynamic claim.

## 5. What already works

- **§3.4, the pendulum, is the best worked example in the course so far.** It takes a result the reader already knows — $T=mg(3\cos\theta-2\cos\theta_0)$ — and derives it from the multiplier machinery, so the machinery is validated rather than merely applied. Both limits check by hand ($2mg$ at the bottom, $\tfrac12 mg$ at the extremes) and the animation drives its keyframes from the formula the text derives. This is the shape every "here is an abstract method" section should take.
- **§3.5 earns the §7 design decision before §7 needs it.** Explaining that reduced coordinates project the constraint force out of the equations, one section before the lab commits to redundant Cartesian coordinates, is exactly the dependency order the standard asks for. The §7.1 callback closes it.
- **The Grübler–Kutzbach derivation (`module03.html:561-567`) is proved in the smallest setting that shows the mechanism**, then specialized to the serial chain the reader needs, with the independence hypothesis stated and its role identified. Proposition 3.2's invertibility argument does the same.
- **§7's physics is correct and the code reproduces every headline number in §7.5 and §7.6.** The Cartesian-coordinate choice, the constant diagonal $M$, the $3\times4$ Jacobian, the sanity check that a hanging mass gives $|\lambda|L=mg$, and the Baumgarte correction are all right, and the lab's output matches the prose to three figures once the prints are added.
- **§4.2's inclined-abductor correction is the model of how to handle an idealization honestly.** It states the simple answer (2.5 $W$), redoes the balance with the real muscle line, gets 2.7 $W$ tilted 21°, explains that the two are the same analysis read to different fidelity, and reconciles both with the telemetry range. Every one of those numbers checks. Do this everywhere.
- **§6.1's proof of the stability ratio** derives a clinically named quantity from a cone-geometry argument in six lines, notes that $S$ is independent of $N$, and draws the right conclusion: loading the joint harder raises the dislocating force in proportion. Only its unstated assumptions (B12) are missing.
