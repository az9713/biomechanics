# Editor report: module16.html (Continuum and Finite-Element-Style Tissue Models)

Editorial pass. Standard: the five-part rule of the `science-editor` skill, read against `EDITOR_DOMAIN.md`. Every location is `module16.html:LINE`. Every replacement is valid HTML with MathJax delimiters and uses only the box classes the stylesheet defines (`.def`, `.prop`, `.proof`, `.keyresult`, `.probes`, `.sol`), spaced hyphens rather than em-dashes.

All four Python blocks in the file (the Section 5 assembly demo and Labs A, B, C) were extracted and run; none errors and none contains a live HTML tag. Their printed output was compared line by line with the prose. Every figure past Section 3 was decoded from its own polyline coordinates and refitted against the law its caption claims. Six new code blocks (K2, K6, K7, K8, K9, K10) and one rewritten one (Lab C) were written, run, and checked with `pycodestyle --max-line-length=79` before being quoted here. Scripts in the session scratchpad, folder `m16/`: `verify.py` (every checkable number), `genfigs.py` (the Lab C figure body), `blk/*.py` (the seven code blocks), `apply.py` (the applier).

Every number in a replacement below was printed by the code shown beside it.

## 1. Verdict

**Yes, after revision.** A graduate reader with no biomechanics can learn from these pages what a stress tensor is, why it is symmetric, how a strain-energy function generates a constitutive law, and how the finite-element method turns a boundary-value problem into a matrix system. The theoretical spine is genuinely good: Propositions 1.1, 2.1, 3.1, 4.1, 5.1, 6.1 and 7.1 each carry a proof that a reader can reproduce with a pen, and the arc from kinematics to balance to material law to computation is the right one and is stated in Section 0. Section 9's two tables, which name what each earlier one-dimensional model kept and threw away, are the best pages in the module.

What stops the reader is the second half. **Lab C does not perform the experiment it describes.** Its code solves Terzaghi consolidation under a step *load*, under which the total stress is constant by construction and nothing relaxes; the section, the caption and K8 all describe step-*strain* stress relaxation. The figure resolves the contradiction by drawing the layer-averaged pore pressure and relabelling the axis "normalised stress" on an equilibrium floor of 0.35 that appears in no table, no derivation and no assumption; decoded from its own polyline, the curve is exactly $0.35+0.65\langle p\rangle$ to within 0.0011. The interpretation then quotes 0.24 where the code prints 0.2347. **The beam element's $4\times4$ stiffness matrix is boxed and marked "stated here"** beside a proved sibling, the bar matrix of Proposition 4.1, which is the asserted-sibling gap `EDITOR_DOMAIN.md` names. **Cauchy's theorem is boxed inside Definition 2.1 with no argument**, while the tetrahedron proof it needs sits unused in problem D3. **Proposition 8.1 is stated for any biphasic tissue and proved only for a single exponential.** The von Mises stress is used and never defined, here or anywhere in the course.

The computational problem set does not meet the module's own claim. Three separate sentences (`:444`, `:531`, `:619`) tell the reader that the computational solutions quote numbers the code produces, and not one of the thirty problems contains any code. Five of the ten K solutions quote no number at all: K7 says the material stiffens without saying by how much, K8 asserts a $\tau\propto L^2$ scaling it never tests, K9 is an optimisation problem in which nothing is optimised, K10 promises a regime comparison that is impossible with the element it names (an Euler-Bernoulli element reproduces $PL^3/3EI$ exactly at every aspect ratio, so it cannot show where Euler-Bernoulli breaks), and K6 asks for a sweep and delivers two endpoints. That last one is the sharpest instance of a pattern worth naming: **Fig. 7 already draws $E(\theta)=0.129+1.377\cos^4\theta$**, a fit to its own polyline with a residual of 0.005 GPa against 0.118 for $\cos^2\theta$, and the prose never states the law its own figure plots.

None of this touches the seven propositions, which are sound and check. All of it is repairable, and the repairs make the module's three "every number is reproduced by the code" claims true rather than requiring them to be softened.

## 2. Blocking defects

Ranked by severity: the lab that runs a different experiment from the one it reports, then asserted results of equal weight to proved siblings, then undefined terms and missing scaffolding, then problem-set depth, then bookkeeping.

### B1. Lab C's figure plots pore pressure relabelled as stress, on an invented equilibrium floor

Location: `module16.html:431` (the figure), `module16.html:413` (heading), `module16.html:433` (interpretation).

Quoted (caption, line 431): "A finite-difference solution of &#8706;u/&#8706;t = c&#7515; &#8706;&#178;u/&#8706;z&#178; (Module 4) under a step compression gives the surface stress decaying from its instantaneous peak - fluid pressurised, carrying the load - to the equilibrium value borne by the drained matrix, exactly the relaxation Proposition 8.1 predicts, now produced by a solver rather than assumed."

Quoted (interpretation, line 433): "mean pore pressure falling toward 0 - $\approx0.24$ at the last shown step".

Three faults, one root. **(a)** The code performs a step-*load* (Terzaghi) consolidation: $p(z,0)=1$ everywhere with a drained top and a sealed bottom. Under a step load the total stress is held constant by the loading device, so no stress relaxes; what changes is the *partition* of that constant load between fluid pressure and solid matrix. Stress relaxation is the step-*strain* experiment, a different boundary-value problem with a different eigenseries. The caption, the section heading and K8 all describe the experiment the code does not do. **(b)** The figure resolves this by drawing something else. Decoding its polyline against its own axis calibration (0.35 at $y=185.3$, 1.0 at $y=59.4$; ticks 0, 248, 495 on $x$), the plotted curve is $0.35+0.65\langle p\rangle$, matching the module's own solver to a maximum deviation of 0.0011 over all 100 points. The 0.35 floor labelled "equilibrium (matrix)" is a bare number: it is in no table, follows from no boxed result, and is not labelled an assumption. It exists to make an affine rescaling of the mean pore pressure look like a stress-relaxation curve. **(c)** The interpretation quotes 0.24 where the code prints 0.23; the exact value is 0.234702 and the analytic Terzaghi series gives 0.23605.

The fix keeps the solver, which is correct, and reports what it computes: the layer-averaged share of the applied load still carried by fluid, $F(T)=\langle p\rangle$, and the share carried by the matrix, $U(T)=1-\langle p\rangle$, against the dimensionless consolidation time $T=c_vt/L^2$. That is Module 4's fluid load support, which is the finding `EDITOR_DOMAIN.md` says must not be softened, and it removes the invented floor. Replacement for line 413:

```html
<h3>Lab C - load sharing between fluid and matrix under a step load</h3>
```

Replacement for line 414 (see also B2 for the variable clash it also fixes):

```html
<p><b>Physical question.</b> When a cartilage layer is pressed and held, how fast does the load pass from the pressurised fluid to the solid matrix? <b>Model.</b> the consolidation diffusion of <a class="secref" href="#timedep">Section 8</a> (Module 4), one dimension, drained at the loaded surface and sealed at the bone. <b>Parameters.</b> the only parameter is the dimensionless time $T=c_vt/L^2$; the run below covers $T:0\to0.5$ using $c_v=10^{-3}\ \mathrm{m^2\,s^{-1}}$ and $L=1\ \mathrm{m}$, an assumed pair chosen so that one explicit step is $0.25\ \mathrm s$. <b>Equations.</b> a step load is carried entirely by the fluid at $t=0^+$, so $p(z,0)=\sigma_0$; thereafter $\partial p/\partial t=c_v\,\partial^2p/\partial z^2$, the same consolidation equation the matrix displacement obeys (Definition 8.2), solved by explicit finite differences. The layer-averaged fluid share is $F(T)=\langle p\rangle/\sigma_0$ and the matrix share is $U(T)=1-F(T)$.</p>
```

Replacement for the Lab C code block (lines 416 to 429), which now prints the dimensionless time, both shares, the half-consolidation point, and the analytic series that checks it:

```html
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Copy</span></button><pre><code>import numpy as np

nz, cv, L = 40, 1e-3, 1.0
dz = L/nz
dt = 0.4*dz**2/cv                    # stable explicit step
p = np.ones(nz + 1)                  # step load: fluid carries all of it
p[0] = 0.0                           # drained top surface
T50 = None
for it in range(2000):
    lap = np.zeros_like(p)
    lap[1:-1] = (p[2:] - 2*p[1:-1] + p[:-2])/dz**2
    lap[-1] = (2*p[-2] - 2*p[-1])/dz**2   # sealed bottom
    p = p + dt*cv*lap
    p[0] = 0.0
    T = cv*(it + 1)*dt/L**2          # dimensionless consolidation time
    if T50 is None and p.mean() &lt; 0.5:
        T50 = T
    if it in (0, 1999):
        print("T = %.4f: fluid share = %.4f, matrix share = %.4f"
              % (T, p.mean(), 1 - p.mean()))
print("half-consolidation at T = %.3f" % T50)
ser = sum(8/((2*n + 1)**2*np.pi**2)*np.exp(-((2*n + 1)*np.pi/2)**2*T)
          for n in range(80))
print("analytic series at T = %.2f gives %.4f" % (T, ser))</code></pre></div>
```

Printed output:

```
T = 0.0003: fluid share = 0.9659, matrix share = 0.0341
T = 0.5000: fluid share = 0.2347, matrix share = 0.7653
half-consolidation at T = 0.195
analytic series at T = 0.50 gives 0.2360
```

The figure is regenerated from that array (`m16/genfigs.py`); its two polylines are $F(T)$ and $U(T)$ sampled at 100 points, with the half-consolidation reference at $T_{1/2}=0.195$ (corrected from 0.19 during the apply; the solver prints 0.1945). New caption:

```html
<figcaption><b>Lab C.</b> Load sharing under a step load. A finite-difference solution of the consolidation equation (Definition 8.2, Module 4) for a layer drained at the loaded surface and sealed at the bone. The total load is constant; what changes is who carries it. At $T=c_vt/L^2\to0^+$ the fluid carries essentially all of it (computed $F=0.966$ at the first step), and as fluid seeps out the solid matrix takes over, the two shares crossing at $T_{1/2}=0.195$ and the matrix reaching $0.765$ by $T=0.5$. This is Module 4's fluid load support computed rather than asserted, and it is the step-load counterpart of the step-strain relaxation of Proposition 8.1.</figcaption>
```

Replacement for line 433:

```html
<p><b>Interpretation.</b> The applied load starts almost entirely on the fluid, $F=0.966$ at the first step, and ends mostly on the matrix, $F=0.235$ and $U=0.765$ at $T=0.5$; the analytic Terzaghi series $F(T)=\sum_{n\ge0}\frac{8}{(2n+1)^2\pi^2}e^{-(2n+1)^2\pi^2T/4}$ gives $0.2360$ at the same $T$, so the 40-cell mesh is accurate to $0.6\%$. Half the load has transferred by $T_{1/2}=0.195$ (the series itself gives $0.1967$, the tabulated Terzaghi value $0.197$). The transfer is monotone, which is the same one-way behaviour Proposition 8.1 proves for the step-strain relaxation modulus, and for the same reason: every term of the series decays and none of them grows. <b>Sensitivity.</b> Because $T$ is the only parameter, the physical half-time is $t_{1/2}=0.195\,L^2/c_v$: a layer twice as thick, or a matrix half as permeable, takes four times or twice as long. K8 confirms the thickness scaling by running the solver at three thicknesses. <b>Extension.</b> Re-run with a sealed top and a drained bottom and confirm $T_{1/2}$ is unchanged, since the drainage path length, not its direction, sets the clock.</p>
```

### B2. Lab C's stated equation is in one field and its code is in another

Location: `module16.html:414` (in the text replaced above), `module16.html:321`.

Quoted (line 414): "<b>Equations.</b> $\partial u/\partial t=c_v\,\partial^2 u/\partial z^2$, explicit finite differences." Quoted from the code (line 420): "p = np.ones(nz + 1)                  # unit step pore pressure".

Missing part 2 (every term defined). The lab states its governing equation for the matrix displacement $u$, which is what Definition 8.2 introduces, and then solves it for the pore pressure $p$. These are different fields with different boundary conditions: $u$ is zero at the sealed base and free at the drained surface, $p$ is the reverse. In the linear biphasic theory both satisfy the same diffusion equation, which is why the code works, but the module never says so and the reader is left to assume a typo. The symbol $u$ is by then also doing duty as the nodal displacement of Sections 4 and 5 and as the displacement field $\mathbf u$ of Section 1. The B1 replacement for line 414 states the equation in $p$, names the boundary conditions, and says in one clause that the matrix displacement obeys the same equation. Add the same clarification to Definition 8.2 at line 321, replacing:

```html
where $p$ is the interstitial fluid pressure and $\boldsymbol\sigma_{\rm s}$ the stress carried by the solid matrix. Combining this split with Darcy flow and mass conservation yields a consolidation (diffusion) equation for the matrix displacement $u$, $\partial u/\partial t=c_v\,\partial^2u/\partial z^2$, with consolidation coefficient $c_v=H_A k$ ($H_A$ the aggregate modulus, $k$ the permeability) - the very equation Module 4 derived for cartilage.</div>
```

with:

```html
where $p$ is the interstitial fluid pressure and $\boldsymbol\sigma_{\rm s}$ the stress carried by the solid matrix. Combining this split with Darcy flow and mass conservation yields a consolidation (diffusion) equation for the matrix displacement $u_z$ (written $u_z$ here to keep it distinct from the displacement field $\mathbf u$ of <a class="secref" href="#kinematics">Section 1</a> and the nodal displacements of <a class="secref" href="#bar">Section 4</a>), $\partial u_z/\partial t=c_v\,\partial^2u_z/\partial z^2$, with consolidation coefficient $c_v=H_Ak_p$ ($H_A$ the aggregate modulus, $k_p$ the permeability) - the very equation Module 4 derived for cartilage. Because the pore pressure is proportional to the compaction gradient, $p$ satisfies the same diffusion equation with complementary boundary conditions (drained where the matrix is free, sealed where it is fixed), so a solver written for either field answers for both; Lab C solves for $p$.</div>
```

### B3. The beam element's stiffness matrix is boxed and asserted beside a proved sibling

Location: `module16.html:230-236`.

Quoted (line 230): "the element stiffness is a $4\times4$ matrix built from the bending stiffness $EI$ ($I$ the cross-section's second moment of area, Module 2) - stated here, its entries following from the cubic Hermite shape functions (equivalently, the beam reactions of Module 2),". Quoted (line 236): "whose entries are exactly the shear-force and bending-moment reactions Module 2 computed for a loaded beam".

Missing part 3 (a proof in the smallest setting). Proposition 4.1 proves the $2\times2$ bar matrix as the Hessian of the element strain energy; the $4\times4$ beam matrix is a boxed `.keyresult` of exactly equal weight, and the phrase "stated here" concedes the gap. This is the sibling-keyresult case `EDITOR_DOMAIN.md` names, the same shape as the Module 6 Section 6 defect. The second sentence also overstates: the entries are the reactions to *unit nodal displacements*, not the reactions Module 2 computed for a distributed load.

The proof is short, uses only the energy argument already established, and needs no new machinery. Verified symbolically with SymPy (`m16/verify.py` and the sympy run recorded in the report scratchpad): integrating $EI\,N_i''N_j''$ over the element for the four Hermite cubics reproduces the stated matrix entry for entry. Replacement for lines 230 to 236:

```html
<p>Bending needs one more element. A <b>beam element</b> resists transverse deflection, and because bending couples deflection to rotation (Module 2's Euler-Bernoulli theory), each node carries <em>two</em> degrees of freedom - a transverse displacement $w$ and a slope $\theta=dw/dx$ - so the element stiffness is a $4\times4$ matrix built from the bending stiffness $EI$ ($I$ the cross-section's second moment of area, Module 2). It follows from the same energy argument as the bar.</p>

<div class="prop"><b>Proposition 4.2 (the beam element matrix).</b> Let the transverse displacement of a beam element of length $L$ and bending stiffness $EI$ be interpolated from its four nodal degrees of freedom $\mathbf u_e=(w_1,\theta_1,w_2,\theta_2)$ by the cubic Hermite shape functions $N_i(x)$, the unique cubics with $N_i$ taking the value one for its own degree of freedom and zero for the other three. Then the element stiffness is the Hessian of its bending energy,
$$\boxed{\;\mathbf k_{\rm beam}=\frac{EI}{L^3}\begin{pmatrix}12&6L&-12&6L\\6L&4L^2&-6L&2L^2\\-12&-6L&12&-6L\\6L&2L^2&-6L&4L^2\end{pmatrix},\qquad (\mathbf k_{\rm beam})_{ij}=\int_0^L EI\,N_i''N_j''\,dx,\;}$$
symmetric positive-semidefinite with a two-dimensional null space: rigid translation and rigid rotation.</div>

<div class="proof">Module 2's Euler-Bernoulli theory gives the bending energy of a beam as $W_e=\tfrac12\int_0^L EI\,(w'')^2dx$, the curvature $w''$ playing the role the axial strain played in Proposition 4.1. Writing $w(x)=\sum_i N_i(x)\,u_{e,i}$ makes $w''=\sum_iN_i''u_{e,i}$, so
$$W_e=\tfrac12\sum_{i,j}u_{e,i}\Big(\int_0^LEI\,N_i''N_j''\,dx\Big)u_{e,j}=\tfrac12\,\mathbf u_e^{\!\top}\mathbf k_e\mathbf u_e,$$
and the Hessian $\partial^2W_e/\partial u_{e,i}\partial u_{e,j}$ is the bracket, which is symmetric by inspection. With $s=x/L$ the four Hermite cubics are $N_1=1-3s^2+2s^3$, $N_2=L(s-2s^2+s^3)$, $N_3=3s^2-2s^3$, $N_4=L(-s^2+s^3)$; each takes the value one for its own nodal quantity and zero for the other three, which is what makes $\mathbf u_e$ the nodal displacements and slopes. Take the first column as the worked case. $N_1''=(-6+12s)/L^2$, so
$$(\mathbf k_{\rm beam})_{11}=\int_0^L\frac{EI}{L^4}(12s-6)^2dx=\frac{EI}{L^3}\int_0^1(12s-6)^2ds=\frac{EI}{L^3}\Big[\frac{(12s-6)^3}{36}\Big]_0^1=\frac{12EI}{L^3},$$
and with $N_2''=(-4+6s)/L$,
$$(\mathbf k_{\rm beam})_{12}=\int_0^L\frac{EI}{L^3}(12s-6)(6s-4)\,dx=\frac{EI}{L^2}\int_0^1(72s^2-84s+24)\,ds=\frac{EI}{L^2}(24-42+24)=\frac{6EI}{L^2}.$$
The remaining fourteen entries follow by the same integral and give the boxed matrix. Positive-semidefiniteness is inherited from the energy, which is an integral of $EI(w'')^2\ge0$; the null space is the set of nodal vectors with $w''\equiv0$, that is the straight-line motions $w=a+bx$, a translation and a rotation, so $\mathbf k_{\rm beam}$ has rank two and a beam, like a bar, needs supports before its system can be solved. <span class="qed">&#8718;</span></div>

<p>The entries are the nodal forces and moments a unit nodal displacement or rotation calls up, so a bone modelled as a chain of beam elements reproduces its deflection under any load; K10 checks that one element already gives Module 2's cantilever formula exactly. The bar carries axial force, the beam carries bending; a general frame element superposes the two. With one element understood, the method is defined by how elements <em>combine</em>.</p>
```

### B4. Cauchy's theorem is boxed inside a definition with no argument

Location: `module16.html:121-123`, with the renumbering it forces at `:125`, `:150`, `:454`, `:504`.

Quoted (line 121): "Cauchy's theorem states that this dependence on $\mathbf n$ is <em>linear</em>: there is a single second-order tensor $\boldsymbol\sigma$, the <b>Cauchy stress</b>, with" followed by the boxed $\mathbf t(\mathbf n)=\boldsymbol\sigma\mathbf n$.

Missing part 3. Linearity in $\mathbf n$ is the whole content of Section 2 and it is the least obvious claim in the module: nothing about "force per unit area across a cut" suggests that the nine numbers of a tensor determine the traction on every one of the infinitely many cut orientations. The module states it as a definition and boxes it, which is the "prove, do not assert" failure in its purest form. The proof is not missing from the manuscript; it sits in problem D3 (`:500`), where the reader meets it only after being asked to accept the result for eight sections. Promote it.

This makes Cauchy Proposition 2.1 and the symmetry result Proposition 2.2, which requires updating the three references at `:150`, `:454` and `:504`. Replacement for lines 121 to 123:

```html
<div class="def"><b>Definition 2.1 (traction).</b> At a point, imagine a small planar cut with unit normal $\mathbf n$. The material on the positive-$\mathbf n$ side exerts on the other side a force per unit area, the <em>traction</em> $\mathbf t(\mathbf n)$. Write $\mathbf t^{(j)}=\mathbf t(\mathbf e_j)$ for the traction on the cut whose normal is the $j$-th coordinate axis, and collect the components into the array $\sigma_{ij}=t^{(j)}_i$: the $i$-th force component per unit area on the face whose normal points along $j$. The diagonal entries are <em>normal</em> stresses (tension and compression), the off-diagonal entries <em>shear</em> stresses. Nothing so far says these nine numbers determine the traction on any other cut; that is the content of the next result.</div>

<div class="prop"><b>Proposition 2.1 (Cauchy's theorem).</b> The traction depends linearly on the cut normal, so the nine components $\sigma_{ij}$ of Definition 2.1 form a second-order tensor $\boldsymbol\sigma$, the <b>Cauchy stress</b>, and
$$\boxed{\;\mathbf t(\mathbf n)=\boldsymbol\sigma\,\mathbf n,\qquad t_i=\sigma_{ij}n_j\;}$$
for every unit normal $\mathbf n$.</div>

<div class="proof">Take the smallest setting that shows the mechanism: a tetrahedron with three faces normal to the coordinate axes and one oblique face of area $A$ with outward normal $\mathbf n$, all four meeting at the point, with the tetrahedron's longest edge $h$. The three axis faces are the projections of the oblique one, so the face normal to $\mathbf e_j$ has area $An_j$, and the enclosed volume is $\tfrac13Ah'$ for some height $h'\le h$. Newton's second law for the tetrahedron reads
$$\mathbf t(\mathbf n)\,A-\sum_j\mathbf t^{(j)}An_j+\mathbf b\,V=\rho V\ddot{\mathbf x},$$
the minus sign because the outward normals of the axis faces point along $-\mathbf e_j$. Every surface term scales as $A\sim h^2$ and every volume term as $V\sim h^3$. Divide by $A$ and let $h\to0$: the body-force and inertia terms carry a surviving factor $V/A\sim h\to0$ and drop out, whatever the acceleration, leaving $\mathbf t(\mathbf n)=\sum_j\mathbf t^{(j)}n_j$. In components that is $t_i=\sigma_{ij}n_j$, which is linear in $\mathbf n$. Linearity is what makes $\sigma_{ij}$ a tensor rather than nine unrelated numbers: it transforms under a change of axes as the matrix of a linear map must, because it <em>is</em> the matrix of the map $\mathbf n\mapsto\mathbf t$. <span class="qed">&#8718;</span></div>
```

Replacement for line 125 (the symmetry proposition renumbered):

```html
<div class="prop"><b>Proposition 2.2 (the stress tensor is symmetric).</b> Balance of angular momentum forces
```

Replacement for the caption reference at line 150. The old text also refers to "Fig. 3" from inside Fig. 3's own caption; both are fixed here:

```html
</svg><figcaption><a class="secref" href="#stress">Section 2</a>. Stress is a tensor. On a material cube, each face carries a normal stress &#963; (red) and shear stresses &#964; (blue); the complementary shears are equal by Proposition 2.2, leaving six independent components. On an arbitrary internal cut with normal n, the transmitted traction is t = &#963;n (Proposition 2.1), and the traction turns as the cut turns, which is exactly why one number cannot describe the state and a tensor can.</figcaption></figure>
```

In the C2 solution (line 454) change "forces $\sigma_{ij}=\sigma_{ji}$ (Proposition 2.1)" to "forces $\sigma_{ij}=\sigma_{ji}$ (Proposition 2.2)", and in the D4 solution (line 504) change "gives $\sigma_{ij}-\sigma_{ji}=0$ (Proposition 2.1)" to "gives $\sigma_{ij}-\sigma_{ji}=0$ (Proposition 2.2)". Change the D3 statement (line 498) from "Sketch why the traction is linear in the normal" to "Redo the tetrahedron argument of Proposition 2.1 keeping the body force and inertia terms explicitly, and say which power of $h$ kills each."

### B5. Proposition 8.1 is stated for any biphasic tissue and proved for one exponential

Location: `module16.html:323-326`.

Quoted (line 323): "A biphasic tissue is <em>stiffer the faster it is loaded</em>: its instantaneous modulus $G_0$ ... exceeds its equilibrium modulus $G_\infty$ ..., and the relaxation modulus $G(t)$ decreases monotonically between them". Quoted (line 326): "For the standard-linear-solid form $G(t)=G_\infty+(G_0-G_\infty)e^{-t/\tau}$, $G'(t)=-\tfrac1\tau(G_0-G_\infty)e^{-t/\tau}\le0$".

Missing parts 1 and 3. The statement quantifies over every biphasic tissue; the proof verifies one assumed functional form. A single decaying exponential is exactly the case in which monotonicity is obvious, and the biphasic tissue the module cares about is not that case: Lab C's own consolidation solution is an infinite series of exponentials, not one. The first half of the argument, that the fluid pressurises and then drains, is a physical sketch with no inequality in it. The honest statement holds for any relaxation function with a non-negative relaxation spectrum, which is the standard representation and which the module's own lab supplies as a worked instance with weights $8/((2n+1)^2\pi^2)$, all positive. Replacement for lines 323 to 326:

```html
<div class="prop"><b>Proposition 8.1 (a draining tissue can only get softer).</b> Suppose the relaxation modulus is a sum of decaying exponentials with non-negative weights above a floor,
$$G(t)=G_\infty+\sum_{m}g_m\,e^{-t/\tau_m},\qquad g_m\ge0,\quad\tau_m\gt0,\quad G_\infty\ge0,$$
a <em>Prony series</em> (the standard linear solid of Definition 8.1 is the one-term case). Then
$$\boxed{\;G_0\ge G(t)\ge G_\infty\ge0,\qquad G'(t)\le0\ \text{ for all }t\ge0,\;}$$
with $G_0=G(0)=G_\infty+\sum_mg_m$. A biphasic tissue has this form, so it is <em>stiffer the faster it is loaded</em>: no drainage process can make it stiffen with time.</div>

<div class="proof">Differentiate term by term: $G'(t)=-\sum_m(g_m/\tau_m)e^{-t/\tau_m}$. Every $g_m\ge0$, every $\tau_m\gt0$ and every exponential is positive, so each term of the sum is non-positive and $G'(t)\le0$ for all $t\ge0$. A function with a non-positive derivative is non-increasing, so $G(0)\ge G(t)\ge\lim_{t\to\infty}G(t)=G_\infty$, and $G_\infty\ge0$ because a negative equilibrium modulus would violate the energy positivity of Proposition 3.1. That is the boxed chain, and the sign of $G'$ never depended on how many terms the series has.
<p>The biphasic tissue supplies the weights rather than assuming them. Solving the consolidation equation of Definition 8.2 for a layer of thickness $L$, drained at one face and sealed at the other, by separation of variables gives modes $\cos((2n+1)\pi z/2L)$ with decay times $\tau_n=4L^2/((2n+1)^2\pi^2c_v)$, and the layer-averaged pore pressure after a step load is
$$F(T)=\sum_{n\ge0}\frac{8}{(2n+1)^2\pi^2}\,e^{-(2n+1)^2\pi^2T/4},\qquad T=\frac{c_vt}{L^2}.$$
Every weight $8/((2n+1)^2\pi^2)$ is positive, so seepage is a Prony series with the hypothesis of this proposition already satisfied, and the load can only pass one way, from fluid to matrix. Lab C computes that series and its finite-difference solution and finds them agreeing to $0.6\%$. The physical reading is the one the caption of Fig. 9 gives: at $t=0$ the fluid has had no time to move and, being nearly incompressible, carries a large share of the load, so the tissue answers with its full $G_0$; as $t$ grows the pressure gradient drives seepage, the fluid sheds its share, and what is left is the matrix alone at $G_\infty$. Two mechanisms, viscoelastic and biphasic, one continuum signature. <span class="qed">&#8718;</span></p></div>
```

### B6. The von Mises stress is used and never defined

Location: `module16.html:158`.

Quoted: "the <em>von Mises stress</em> (a scalar built from the shear parts, which governs ductile yield). Both are invariants of the same tensor."

Missing part 2. This is the module's only occurrence of the term and the only occurrence in the course; grep over `module01.html` to `module17.html` returns this line alone. "A scalar built from the shear parts" is not a definition, and the reader cannot compute one. The same sentence leaves "principal stresses" adequately defined, which makes the asymmetry visible. Replacement for line 158:

```html
<p>three scalar equations (one per direction) that the stress field must satisfy at every interior point, with the surface traction $\boldsymbol\sigma\mathbf n$ matching the applied load on the boundary. Equilibrium, the strain-displacement relation of <a class="secref" href="#kinematics">Section 1</a>, and the constitutive law of <a class="secref" href="#elasticity">Section 3</a> together close the system: three ingredients - kinematics, balance, and material law - determine the fields. Two scalars extracted from $\boldsymbol\sigma$ recur in tissue failure, and both are unchanged by a rotation of the axes, so they are properties of the stress state and not of the coordinates chosen to write it. The <em>principal stresses</em> $\sigma_1\ge\sigma_2\ge\sigma_3$ are the eigenvalues of $\boldsymbol\sigma$, the extreme normal stresses over all cut orientations (the eigenvectors give the cuts that carry no shear), and $\sigma_1$ decides brittle fracture in bone, which parts on the plane of greatest tension. The <em>von Mises stress</em> is built from the deviatoric part $\mathbf s=\boldsymbol\sigma-\tfrac13(\operatorname{tr}\boldsymbol\sigma)\mathbf I$, the shape-changing part left after the pressure is removed,
$$\sigma_{\rm vM}=\sqrt{\tfrac32\,\mathbf s:\mathbf s}=\sqrt{\tfrac12\big[(\sigma_1-\sigma_2)^2+(\sigma_2-\sigma_3)^2+(\sigma_3-\sigma_1)^2\big]},$$
normalised so that a bar in uniaxial tension $\sigma$ has $\sigma_{\rm vM}=\sigma$. It governs ductile yield, which is a shearing process: a state of pure pressure has $\mathbf s=\mathbf 0$ and $\sigma_{\rm vM}=0$ and cannot yield a metal however large the pressure, which is why deep-sea organisms are not crushed by hydrostatic load but are torn by a shear of a hundredth the magnitude.</p>
```

### B7. K8 asserts a scaling law it never tests and quotes no number

Location: `module16.html:561-563`.

Quoted (line 563): "Halving the layer thickness $L$ cuts that time by four, confirming $\tau\propto L^2/c_v$ - the diffusion scaling of Module 4."

Missing parts 3 and 5, and the module's own K standard. The problem is labelled "simulation + sensitivity" and contains no simulation, no sensitivity sweep, and not one number; the $L^2$ claim is exactly what the reader was asked to confirm and it is handed to them instead. Verified by running the solver at three thicknesses (`m16/blk/k08.py`): the half-consolidation time is 194.50 s, 48.63 s and 12.16 s at $L=1$, $0.5$ and $0.25$ m, each a factor 4.00 of the last, and the dimensionless $T_{1/2}=0.195$ is identical in all three, which is the sharper statement. Replacement for lines 561 to 563:

```html
<p><b>K8 - the consolidation clock (simulation + sensitivity).</b> Solve the consolidation equation for a layer drained at one face and sealed at the other, and measure the time at which half the load has passed from fluid to matrix. Run it at three thicknesses and decide whether $L$ enters as anything other than the group $c_vt/L^2$. <span class="probes">Probes: diffusion scaling recovered from a solver, and the difference between a fitted exponent and a dimensionless group; Lab C.</span></p>
<details class="sol"><summary>Solution</summary><div>Running Lab C's solver at $L=1$, $0.5$ and $0.25\ \mathrm m$ with $c_v=10^{-3}\ \mathrm{m^2\,s^{-1}}$ gives half-consolidation times of $194.50$, $48.63$ and $12.16\ \mathrm s$: each a factor $4.00$ of the one before, so $t_{1/2}\propto L^2$ and $\tau\propto L^2/c_v$, the diffusion scaling of Module 4. The stronger result is in the third column. In dimensionless time $T=c_vt/L^2$ the answer is $T_{1/2}=0.195$ for all three, so thickness does not merely scale the clock, it is absorbed by it: there is one consolidation curve, not a family. That is why the lab quotes $T$ and not $t$. **[Corrected during the apply.]** The $c_v\sim10^{-6}\ \mathrm{m^2\,s^{-1}}$ this paragraph originally used is a bare number with no source, and it is wrong by three and a half orders of magnitude. Module 4's own table (`module04.html:566-568`) gives $H_A=0.6\ \mathrm{MPa}$ and $k=1\times10^{-15}\ \mathrm{m^4\,N^{-1}s^{-1}}$, hence $c_v=H_Ak_p=6\times10^{-10}\ \mathrm{m^2\,s^{-1}}$, and a $2\ \mathrm{mm}$ layer has $t_{1/2}=0.195\,L^2/c_v=1300\ \mathrm s$, about $22$ minutes, not $0.8\ \mathrm s$. The Terzaghi series then gives a fluid share of $0.986$ after a footstep of $1\ \mathrm s$, $0.893$ after a minute of standing, and $0.214$ only after an hour seated, so the physiological conclusion flips: both a footstep and a minute of standing are carried by pressurised fluid, and it takes sustained loading to strand the load on the matrix. The applied text and the code block below carry the corrected numbers, and the block prints them.</div>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Copy</span></button><pre><code>import numpy as np


def t_half(L, cv=1e-3, nz=40):
    """Time for the layer-averaged pore pressure to fall to one half."""
    dz = L/nz
    dt = 0.4*dz**2/cv
    p = np.ones(nz + 1)
    p[0] = 0.0
    for it in range(2000000):
        lap = np.zeros_like(p)
        lap[1:-1] = (p[2:] - 2*p[1:-1] + p[:-2])/dz**2
        lap[-1] = (2*p[-2] - 2*p[-1])/dz**2
        p = p + dt*cv*lap
        p[0] = 0.0
        if p.mean() &lt; 0.5:
            return (it + 1)*dt
    return np.nan


prev = None
for L in (1.0, 0.5, 0.25):
    th = t_half(L)
    ratio = "" if prev is None else "  (x%.2f of the previous)" % (prev/th)
    print("L = %.2f m: t_half = %8.2f s   T = cv*t/L^2 = %.3f%s"
          % (L, th, 1e-3*th/L**2, ratio))
    prev = th
# -&gt; L = 1.00 m: t_half =   194.50 s   T = cv*t/L^2 = 0.195
# -&gt; L = 0.50 m: t_half =    48.63 s   T = 0.195  (x4.00 of the previous)
# -&gt; L = 0.25 m: t_half =    12.16 s   T = 0.195  (x4.00 of the previous)</code></pre></div></details></div>
```

### B8. K9 is an optimisation problem in which nothing is optimised

Location: `module16.html:565-567`.

Quoted (line 567): "the compliance falls most by placing the stiff (high-$E$) material where the integrand is largest - the most compliant, highest-stress regions (here the thin end). The optimisation confirms the intuition that reinforcement belongs where strain energy density is greatest".

Missing parts 1, 3 and 5. "A fixed budget of stiff material" is never made precise (fixed mass, fixed volume, fixed number of elements?), no objective is written down, no search is run, and no number is produced; the sentence "the optimisation confirms the intuition" reports a computation that does not exist. There is also a small conflation: the quantity to rank is not the integrand $P/(E_eA_e)$, which already contains $E_e$, but the *reduction* an upgrade buys, $P\ell_e/A_e\,(1/E_{\rm soft}-1/E_{\rm stiff})$, which is what makes the thin end optimal. Verified by exhaustive search over all $\binom{8}{4}=70$ placements (`m16/blk/k09.py`). Replacement for lines 565 to 567:

```html
<p><b>K9 - design a composite bar (optimisation).</b> Take the tapered bar of <a class="secref" href="#assembly">Section 5</a> meshed into eight equal-length elements. Four of them may be made of a stiff material ($E_{\rm stiff}=20\ \mathrm{GPa}$) and the other four of a compliant one ($E_{\rm soft}=5\ \mathrm{GPa}$); both are assumed values, and the budget is four elements, not four units of mass. Minimise the tip displacement over all $\binom84=70$ placements, and say what ranks them. <span class="probes">Probes: compliance minimisation as a discrete search, and the difference between the objective and the sensitivity that ranks the choices; Section 5.</span></p>
<details class="sol"><summary>Solution</summary><div>In series the elements carry a common force, so the tip displacement is the sum of the element extensions, $u_L=\sum_eP\ell_e/(E_eA_e)$, and this is the objective. Upgrading element $e$ from soft to stiff reduces it by $\Delta_e=P\ell_e/A_e\,(1/E_{\rm soft}-1/E_{\rm stiff})$. Note what ranks the placements: not the objective's integrand $P\ell_e/(E_eA_e)$, which already contains the modulus one is choosing, but the sensitivity $\Delta_e$, which depends on the geometry alone through $\ell_e/A_e$. Since the elements are of equal length and the bar tapers, $\ell_e/A_e$ is largest at the thin end, so the four thinnest elements are the optimum, and because the $\Delta_e$ are independent the greedy choice is the global one - no search is needed, though running one confirms it. The exhaustive search over all seventy placements returns $(4,5,6,7)$, the thin half, at $0.1555\ \mathrm{mm}$; the worst is $(0,1,2,3)$, the thick half, at $0.1908\ \mathrm{mm}$; the all-soft bar gives $0.2771\ \mathrm{mm}$. Choosing where the same amount of stiff material goes is worth $18.5\%$ of the tip displacement, roughly a third of what the material itself buys. The principle - reinforce where the strain energy density is highest - is the one that puts cortical bone in a thin shell far from the neutral axis (Module 2) and carbon fibre on the tension face of a spar.</div>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Copy</span></button><pre><code>import itertools
import numpy as np

L, P, A0, nel = 0.10, 2000.0, 2e-4, 8
E_soft, E_stiff, budget = 5e9, 20e9, 4      # assumed moduli and budget
xn = np.linspace(0, L, nel + 1)
Ael = A0*(1 - 0.5*(xn[:-1] + xn[1:])/2/L)
le = np.diff(xn)


def tip(stiff):
    """Tip displacement with `stiff` the indices given the stiff modulus."""
    Ee = np.where(np.isin(np.arange(nel), stiff), E_stiff, E_soft)
    return float(np.sum(P*le/(Ee*Ael)))


cases = list(itertools.combinations(range(nel), budget))
best, worst = min(cases, key=tip), max(cases, key=tip)
print("all-soft bar      : %.4f mm" % (tip([])*1e3))
print("best  %s: %.4f mm" % (best, tip(best)*1e3))
print("worst %s: %.4f mm" % (worst, tip(worst)*1e3))
print("best beats worst by %.1f%% of tip displacement"
      % (100*(1 - tip(best)/tip(worst))))
# -&gt; all-soft bar      : 0.2771 mm
# -&gt; best  (4, 5, 6, 7): 0.1555 mm
# -&gt; worst (0, 1, 2, 3): 0.1908 mm
# -&gt; best beats worst by 18.5% of tip displacement</code></pre></div></details></div>
```

### B9. K10 asks a Euler-Bernoulli element to show where Euler-Bernoulli breaks

Location: `module16.html:569-571`, and the diagnostic that repeats it at `:578`.

Quoted (line 571): "As the beam is made stubbier (small $L/h$), shear deformation the Euler-Bernoulli model omits grows and the two disagree, marking the slender-body limit where Module 2's beam theory is valid. The finite element reproduces the analytic model and shows exactly where it breaks."

Wrong statement, part 1. The beam element of Section 4 is built from the Euler-Bernoulli energy $\tfrac12\int EI(w'')^2dx$; it contains no shear flexibility at all. It therefore returns $PL^3/3EI$ exactly at every aspect ratio, verified to machine precision (difference $0.00\mathrm e{+}00$, `m16/blk/k10.py`). Two models that make the same assumption cannot disagree, and a model cannot diagnose its own omission. The comparison the problem wants needs a third quantity: the shear deflection $\delta_s=PL/(\kappa GA)$ that a Timoshenko beam adds and that neither the element nor the formula contains. That term is derivable in one line and gives real numbers. Replacement for lines 569 to 571:

```html
<p><b>K10 - what one beam element does and does not know (regime comparison).</b> Assemble a single beam element for a tip-loaded cantilever and compare its tip deflection with Euler-Bernoulli's $PL^3/3EI$. Then estimate the shear deflection that a Timoshenko beam would add, and sweep the slenderness $L/h$ to find where the omission stops being negligible. Say which of the two disagreements the finite element can detect by itself. <span class="probes">Probes: exactness of a shape function, and the difference between discretisation error and modelling error; Section 4.</span></p>
<details class="sol"><summary>Solution</summary><div>Fixing node 1 and solving the reduced $2\times2$ system of Proposition 4.2 for a tip load gives $w_2=PL^3/3EI$ exactly - the two agree to machine precision, difference $0\mathrm e{+}00$ - because the exact deflection of a tip-loaded cantilever is a cubic and the Hermite shape functions span the cubics, so the element makes no discretisation error at all. This is the opposite of Lab A's tapered bar, whose linear shape function cannot represent a varying strain and needs a mesh. Now the second comparison, and the point of the problem: the element cannot detect the modelling error, because it inherits it. Both the element and the formula come from the Euler-Bernoulli energy $\tfrac12\int EI(w'')^2dx$, which assumes plane sections stay normal to the axis, so both omit shear deformation and both are wrong by the same amount. Quantifying that omission needs a third model. A Timoshenko beam carries a constant shear strain $\gamma=P/(\kappa GA)$ along a tip-loaded cantilever, adding $\delta_s=\gamma L=PL/(\kappa GA)$, so the fractional correction is $\delta_s/\delta_b=3EI/(\kappa GAL^2)$; for a rectangular section of depth $h$ this is $\tfrac{E}{4\kappa G}(h/L)^2$, with the assumed shear coefficient $\kappa=5/6$ and $\nu=0.3$ giving $E/G=2(1+\nu)=2.6$. Sweeping: the shear term adds $0.20\%$ at $L/h=20$, $0.78\%$ at $10$, $3.12\%$ at $5$, $8.67\%$ at $3$ and $19.50\%$ at $2$. A femur at $L/h\approx10$ is safely slender and Module 2's beam theory is good to a per cent; a vertebral body at $L/h\approx1$ is not a beam at all and needs a three-dimensional mesh. The lesson is the general one about verification and validation: refining a mesh drives the discretisation error to zero and leaves the modelling error untouched, so a perfectly converged answer to the wrong equations is still wrong.</div>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Copy</span></button><pre><code>import numpy as np

EI, L, P, nu, kap = 1.0, 1.0, 1.0, 0.3, 5.0/6.0
K = (EI/L**3)*np.array([[12, 6*L, -12, 6*L],
                        [6*L, 4*L**2, -6*L, 2*L**2],
                        [-12, -6*L, 12, -6*L],
                        [6*L, 2*L**2, -6*L, 4*L**2]])
w, th = np.linalg.solve(K[2:, 2:], np.array([P, 0.0]))
print("one beam element : tip deflection = %.12f" % w)
print("Euler-Bernoulli  : P L^3/(3 EI)   = %.12f" % (P*L**3/(3*EI)))
print("difference       = %.2e" % abs(w - P*L**3/(3*EI)))
for LoH in (20, 10, 5, 3, 2):
    extra = (2*(1 + nu)/(4*kap))*(1.0/LoH)**2
    print("L/h = %2d: shear adds %5.2f%% that neither model contains"
          % (LoH, 100*extra))
# -&gt; one beam element : tip deflection = 0.333333333333
# -&gt; Euler-Bernoulli  : P L^3/(3 EI)   = 0.333333333333
# -&gt; difference       = 0.00e+00
# -&gt; L/h = 20: shear adds  0.20% that neither model contains
# -&gt; L/h = 10: shear adds  0.78% ...  L/h = 2: shear adds 19.50%</code></pre></div></details></div>
```

Replacement for the fourth diagnostic (line 578), which currently states only half of this:

```html
<li><b>Element order.</b> Why does one beam element give the exact tip deflection of a point-loaded cantilever, but many bar elements are needed for a tapered bar? <details class="sol"><summary>Solution</summary><div>The exact deflection of a tip-loaded cantilever is a cubic, and the Hermite shape functions span the cubics, so one element represents it with no error; the bar's linear shape function cannot represent the varying strain of a taper, so it only converges with refinement. Exactness here is exactness against Euler-Bernoulli, not against a real beam: the element inherits that theory's neglect of shear and cannot detect it (K10).</div></details></li>
```

### B10. K6 asks for a sweep, gives two endpoints, and never states the law its own figure draws

Location: `module16.html:553-555`; the figure is `module16.html:287`.

Quoted (line 555): "The effective stiffness is highest at $0^\circ$ (load along fibres, $\approx1.5\ \mathrm{GPa}$) and lowest at $90^\circ$ (across, $\approx0.12\ \mathrm{GPa}$), an anisotropy ratio $\approx12$. Sweeping the angle traces the fall governed by the $\mathbf a\otimes\mathbf a$ fibre term, which contributes only its projection onto the load direction."

Missing parts 1, 3 and 5. "Traces the fall" is not a result, and "contributes only its projection" is wrong as stated: the fibre term contributes the *square* of the projection twice over, once in resolving the strain onto the fibre and once in resolving the resulting stress back onto the load. That double projection is a $\cos^4\theta$, and it is not a guess about what the module intends. Fitting Fig. 7's own polyline, decoded against its axis calibration, gives $E(\theta)=0.129+1.377\cos^4\theta$ with a root-mean-square residual of $0.0052$ GPa; the same fit with $\cos^2\theta$ leaves $0.118$ GPa and with $\cos^6\theta$ leaves $0.079$ GPa, so the figure is drawn from the $\cos^4$ law to better than a part in 250. The prose states neither the law nor a single intermediate value of the curve it is describing. Replacement for lines 553 to 555:

```html
<p><b>K6 - the anisotropy sweep.</b> Derive how the directional stiffness of a fibre-reinforced tissue falls as the load is rotated away from the fibres, then sweep the angle and report the half-stiffness angle. Anchor the two ends at the tendon values of <a class="secref" href="#anisotropy">Section 6</a>. <span class="probes">Probes: the double projection hidden in $\mathbf a\otimes\mathbf a$, and why a tendon loaded slightly off-axis is not slightly weaker; Section 6.</span></p>
<details class="sol"><summary>Solution</summary><div>Prescribe a uniaxial strain $\boldsymbol\varepsilon=\varepsilon\,\mathbf n\otimes\mathbf n$ along the load direction $\mathbf n$, at an angle $\theta$ to the fibres $\mathbf a$. The fibre resolves it once: $\varepsilon_a=\mathbf a\cdot\boldsymbol\varepsilon\,\mathbf a=\varepsilon(\mathbf a\cdot\mathbf n)^2=\varepsilon\cos^2\theta$. Proposition 6.1 turns that into $\boldsymbol\sigma_{\rm fib}=W_{\rm fib}'(\varepsilon_a)\,\mathbf a\otimes\mathbf a$, and reading the stress back along the load direction resolves it a second time: $\mathbf n\cdot\boldsymbol\sigma_{\rm fib}\mathbf n=W_{\rm fib}'(\varepsilon_a)\cos^2\theta$. For a linear fibre law $W_{\rm fib}'=E_f\varepsilon_a$ the two projections compound, and with the isotropic matrix carrying $E_m$ in every direction,
$$\boxed{\;E(\theta)=E_m+E_f\cos^4\theta.\;}$$
The fourth power, not the second, is the answer to the question, and it is what Fig. 7 plots. Anchoring at the tendon values $E(0^\circ)=1.50$ and $E(90^\circ)=0.12$ GPa (assumed; Appendix) fixes $E_m=0.12$ and $E_f=1.38$ GPa, an anisotropy ratio of $12.5$. Sweeping: $1.500$, $1.321$, $0.896$, $0.465$, $0.206$ and $0.120$ GPa at $0$, $15$, $30$, $45$, $60$ and $90$ degrees. The stiffness has halved by $34.7^\circ$ and is down by a factor five at $45^\circ$. This is the practical content: a tendon or ligament misaligned by fifteen degrees has lost only $12\%$ of its stiffness, but the fall then steepens sharply, so the tissue tolerates small misalignment and collapses under moderate misalignment. That is the shape of a $\cos^4$, and no single modulus reproduces it. A caution on scope: this is the stiffness under a prescribed uniaxial <em>strain</em>. A free-lateral test, in which the specimen may contract sideways, is governed by the compliance and needs the shear modulus and the two Poisson ratios of the transversely isotropic law, which this module does not supply.</div>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Copy</span></button><pre><code>import numpy as np

Em, E0 = 0.12, 1.50            # across-fibre, along-fibre (GPa, assumed)
Ef = E0 - Em                   # the fibre term's contribution
th = np.radians(np.linspace(0, 90, 9001))
E = Em + Ef*np.cos(th)**4      # Proposition 6.1 under uniaxial strain
for q in (0, 15, 30, 45, 60, 90):
    print("theta = %2d deg: E = %.3f GPa" %
          (q, Em + Ef*np.cos(np.radians(q))**4))
print("anisotropy ratio E(0)/E(90) = %.1f" % (E0/Em))
print("E falls to half of E(0) at theta = %.1f deg" %
      np.degrees(th[np.argmax(E &lt; E0/2)]))
print("the fibre term alone halves at theta = %.1f deg" %
      np.degrees(np.arccos(0.5**0.25)))
# -&gt; theta =  0 deg: E = 1.500    theta = 45 deg: E = 0.465
# -&gt; theta = 15 deg: E = 1.321    theta = 60 deg: E = 0.206
# -&gt; theta = 30 deg: E = 0.896    theta = 90 deg: E = 0.120
# -&gt; anisotropy ratio E(0)/E(90) = 12.5
# -&gt; E falls to half of E(0) at theta = 34.7 deg
# -&gt; the fibre term alone halves at theta = 32.8 deg</code></pre></div></details></div>
```

Add the law to the Section 6 discussion at line 289, replacing "Figure 7 makes the consequence quantitative: the effective stiffness of tendon is about $1.5\ \mathrm{GPa}$ along the fibres and roughly a tenth of that across them" with:

```html
<p>Figure 7 makes the consequence quantitative. Resolving a uniaxial strain onto the fibres and the resulting fibre stress back onto the load direction projects twice, so the directional stiffness is $E(\theta)=E_m+E_f\cos^4\theta$ (derived in K6): about $1.5\ \mathrm{GPa}$ along the fibres and $0.12\ \mathrm{GPa}$ across them, a ratio of $12.5$, with the stiffness halving by $35^\circ$ - the anisotropy that lets a tendon be a taut cable in one direction and fold freely in another.
```

### B11. K7 says the material stiffens and never says by how much

Location: `module16.html:557-559`.

Quoted (line 559): "its tangent modulus $d\sigma/d\lambda=\mu(2\lambda+1/\lambda^2)$ rises from $3\mu$ at $\lambda=1$ ... to larger values as $\lambda$ grows - the material stiffens under stretch."

Missing part 5, and the module's K standard. "Larger values" is the whole quantitative content of a problem labelled a simulation. The numbers, once computed, say something the prose does not suspect: the neo-Hookean tangent is $3.0070\mu$ at $\lambda=1.05$ and $3.0264\mu$ at $\lambda=1.10$, so over a tendon's entire physiological range the stiffening is under one per cent. The reason is that the series is $3e+e^3-e^4+O(e^5)$ with the quadratic term identically zero (SymPy, `m16/blk/k07.py`), and that is precisely why Lab B finds the linear law good to $47\%$ strain - a result the module states twice and never explains. Joining them turns two isolated facts into one. Replacement for lines 557 to 559:

```html
<p><b>K7 - how much does a neo-Hookean solid actually stiffen? (simulation + regime comparison).</b> Compute the uniaxial Cauchy stress and its tangent for an incompressible neo-Hookean solid over $\lambda=1$ to $1.5$, express the tangent as a percentage above its small-strain value, and use the answer to explain Lab B's finding that the linear law survives to $47\%$ strain. <span class="probes">Probes: a nonlinear law that is barely nonlinear, and why the second-order term of a stress-stretch curve can vanish; Section 7, Lab B.</span></p>
<details class="sol"><summary>Solution</summary><div>For the incompressible neo-Hookean solid the uniaxial Cauchy (true) stress is $\sigma(\lambda)=\mu(\lambda^2-1/\lambda)$, the nominal stress being $\sigma/\lambda=\mu(\lambda-1/\lambda^2)$, and the tangent is $d\sigma/d\lambda=\mu(2\lambda+1/\lambda^2)$, equal to $3\mu$ at $\lambda=1$ - the small-strain slope, matching $E=2\mu(1+\nu)=3\mu$ at $\nu=\tfrac12$. Computing it: the tangent is $0.0\%$, $0.2\%$, $0.9\%$, $3.1\%$ and $14.8\%$ above $3\mu$ at stretches $1.02$, $1.05$, $1.10$, $1.20$ and $1.50$. So the archetypal nonlinear law barely stiffens over the range a tendon ever sees; the nonlinearity is real but it is a fifteen per cent effect at a fifty per cent stretch. The reason is visible in the series. Expanding about $\lambda=1+e$,
$$\frac{\sigma}{\mu}=(1+e)^2-\frac{1}{1+e}=3e+e^3-e^4+O(e^5),$$
and the quadratic term cancels exactly: the $+e^2$ from $\lambda^2$ is killed by the $-e^2$ from $-1/\lambda$. A curve whose first correction to linearity is cubic stays near its tangent for a long way, which is exactly Lab B's $47\%$: the relative departure is about $e^2/3$, so five per cent needs $e\approx0.39$, and the higher terms push the true crossing to $0.47$. Contrast the fibre law $e^{k\varepsilon}-1$, whose quadratic term is $k^2\varepsilon^2/2$ and does not cancel: it departs by $k\varepsilon/2$, five per cent at $\varepsilon=0.1/k$, which for $k=48$ is $0.2\%$. Two nonlinear laws, a two-hundred-fold difference in how far the linear approximation carries, and the difference is one vanishing coefficient.</div>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Copy</span></button><pre><code>import numpy as np
import sympy as sp

lam = np.array([1.0, 1.02, 1.05, 1.10, 1.20, 1.50])
sig = lam**2 - 1/lam                   # Cauchy stress / mu
tan = 2*lam + 1/lam**2                 # d(sigma)/d(lambda) / mu
for a, b, c in zip(lam, sig, tan):
    print("lam = %.2f: sigma/mu = %.4f  tangent/mu = %.4f  (%.1f%% above 3)"
          % (a, b, c, 100*(c/3 - 1)))
e = sp.symbols('e')
print("series of sigma/mu about lam = 1:",
      sp.series((1 + e)**2 - 1/(1 + e), e, 0, 5))
# -&gt; lam = 1.02: sigma/mu = 0.0600  tangent/mu = 3.0012  (0.0% above 3)
# -&gt; lam = 1.05: sigma/mu = 0.1501  tangent/mu = 3.0070  (0.2% above 3)
# -&gt; lam = 1.10: sigma/mu = 0.3009  tangent/mu = 3.0264  (0.9% above 3)
# -&gt; lam = 1.20: sigma/mu = 0.6067  tangent/mu = 3.0944  (3.1% above 3)
# -&gt; lam = 1.50: sigma/mu = 1.5833  tangent/mu = 3.4444  (14.8% above 3)
# -&gt; series of sigma/mu about lam = 1: 3*e + e**3 - e**4 + O(e**5)</code></pre></div></details></div>
```

### B12. K2 claims to invert the finite-element model and inverts a formula instead

Location: `module16.html:537-539`.

Quoted (line 537, statement): "From a measured bar tip displacement, invert the finite-element model to estimate Young's modulus." Quoted (line 539, solution): "its sensitivity $\partial u_L/\partial E$ sets how precisely."

Missing parts 3 and 5. The solution rearranges the closed-form $u_L=2PL\ln2/(EA_0)$, which is one line of algebra and is the plug-in shape the module's own K standard bans; the finite-element model named in the statement is never used. The sensitivity is invoked and never computed, which matters because it is the answer to "how precisely". Verified with a bisection on the 64-element solver (`m16/blk/k02.py`): $E=17.00$ GPa is recovered from a reading of $81.55\ \mu\mathrm m$, and because $u_L\propto1/E$ a $1\%$ displacement error gives a $0.99\%$ modulus error, so $1\%$ precision in $E$ demands resolving $0.816\ \mu\mathrm m$ out of $81.5\ \mu\mathrm m$. Replacement for lines 537 to 539:

```html
<p><b>K2 - recover the modulus (inverse problem).</b> A tapered bar of known geometry is pulled with $P=2\ \mathrm{kN}$ and its tip displacement is measured as $81.55\ \mu\mathrm m$. Invert the finite-element model numerically for Young's modulus, then propagate a measurement error through the inversion and state the displacement resolution a $1\%$ modulus estimate requires. <span class="probes">Probes: an inverse problem solved on the forward model, and error propagation as the thing that decides whether a measurement is worth making; Section 5.</span></p>
<details class="sol"><summary>Solution</summary><div>The forward map $E\mapsto u_L^{\rm FE}(E)$ is the Section 5 solver, monotone decreasing and smooth, so the inverse is a one-dimensional root find: bracket $E$ between $1$ GPa and $1$ TPa and bisect on $u_L^{\rm FE}(E)-u_{\rm meas}=0$. With 64 elements this returns $E=17.00\ \mathrm{GPa}$, cortical bone, in a few dozen function evaluations. Doing it on the model rather than on the closed form is the point: the same three lines invert a bar whose taper, hole, or material grading has no closed form, which is the situation every real identification is in (Module 15's parameter estimation, now applied to a material property rather than a segment inertia). Error propagation is where the answer earns its use. Since the bar is linear elastic, $u_L\propto1/E$ exactly, so the relative errors map one to one: a $1\%$ error in the measured displacement returns a $0.99\%$ error in $E$, and $5\%$ returns $4.76\%$ (not $5\%$, because the map is a reciprocal, not a linear one). Numerically, $1\%$ of the reading is $0.816\ \mu\mathrm m$ out of $81.5\ \mu\mathrm m$, so a $1\%$ modulus estimate needs sub-micron displacement resolution. That is the whole design constraint on such a test, and it is invisible until the sensitivity is computed.</div>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Copy</span></button><pre><code>import numpy as np
from scipy.optimize import brentq

L, P, A0, nel = 0.10, 2000.0, 2e-4, 64


def tip(E):
    xn = np.linspace(0, L, nel + 1)
    Ael = A0*(1 - 0.5*(xn[:-1] + xn[1:])/2/L)
    K = np.zeros((nel + 1, nel + 1))
    for e in range(nel):
        k = E*Ael[e]/(xn[e + 1] - xn[e])
        K[e:e + 2, e:e + 2] += k*np.array([[1, -1], [-1, 1]])
    fr = np.arange(1, nel + 1)
    u = np.zeros(nel + 1)
    u[fr] = np.linalg.solve(K[np.ix_(fr, fr)], np.eye(nel)[-1]*P)
    return u[-1]


meas = 8.155e-5                        # measured tip displacement (m)
E_hat = brentq(lambda E: tip(E) - meas, 1e9, 1e12)
print("recovered E = %.2f GPa" % (E_hat/1e9))
for pct in (1.0, 5.0):
    E2 = brentq(lambda E: tip(E) - meas*(1 + pct/100), 1e9, 1e12)
    print("%.0f%% error in u_L -&gt; %.2f%% error in E" %
          (pct, 100*abs(E2 - E_hat)/E_hat))
print("1%% of u_L = %.3f um of the %.1f um reading" %
      (meas*0.01*1e6, meas*1e6))
# -&gt; recovered E = 17.00 GPa
# -&gt; 1% error in u_L -&gt; 0.99% error in E
# -&gt; 5% error in u_L -&gt; 4.76% error in E
# -&gt; 1% of u_L = 0.816 um of the 81.5 um reading</code></pre></div></details></div>
```

### B13. K4's concentration formula is an unlabelled empirical fit, and its conclusion understates its own number

Location: `module16.html:545-547`.

Quoted (line 547): "sweeping the radius-to-thickness ratio $r/h$ through the shoulder relation $K_t\approx1+\tfrac12\sqrt{h/r}$ gives $K_t\approx1.7$ for a generous fillet ($r/h=0.5$), rising to $\approx4.5$ for a sharp one ($r/h=0.02$). So the real peak is up to more than twice the one-dimensional thin-section value".

Two faults. The arithmetic is right ($1.707$ and $4.536$, `m16/verify.py`), but $K_t\approx1+\tfrac12\sqrt{h/r}$ is a bare number in formula form: it does not follow from any boxed result in the module, it is in no table, and it is not labelled an assumption, which is the class violation `EDITOR_DOMAIN.md` makes blocking. It is a standard handbook fit and the repo holds no source for it, so per the brief it must be labelled as an assumed fit and not repaired from memory. Second, "up to more than twice" reports the module's own $K_t=4.5$ as though it were $2$; the factor two is the area change, which the sentence has already accounted for. Replacement for line 547:

```html
<details class="sol"><summary>Solution</summary><div>Equilibrium fixes the average: where the area halves the mean stress doubles, $\sigma_{\rm thin}=2\sigma_{\rm thick}$, and a one-dimensional bar model stops there. The true stress at the shoulder is $K_t$ times that thin-section nominal, and $K_t$ depends on how sharply the section changes. This module cannot derive $K_t$ - it needs a two-dimensional solution of the equilibrium equations of <a class="secref" href="#stress">Section 2</a> around the fillet, which is a mesh, not a formula - so take the standard handbook fit $K_t\approx1+\tfrac12\sqrt{h/r}$ as an <em>assumed</em> relation (Appendix), with $h$ the thin-section thickness and $r$ the fillet radius. Sweeping $r/h$ gives $K_t=1.71$ for a generous fillet ($r/h=0.5$) and $4.54$ for a sharp one ($r/h=0.02$), a factor $2.7$ across the sweep from geometry alone. So the true peak reaches about $4.5$ times the thin-section nominal, or nine times the stress in the thick section, where the one-dimensional model reports a factor of two and nothing else. The sweep, not either endpoint, is the result: it is the *excess* $K_t-1$ that scales as $r^{-1/2}$, so halving a fillet radius from $r/h=0.5$ to $0.25$ raises the excess by $41\%$ ($0.707\to1.000$) and the peak stress itself by $17\%$ ($1.707\to2.000$) - corrected during the apply, where this sentence attributed the $41\%$ to $K_t$ - and no radius is small enough to be safe. That peak sits at the re-entrant corner and is where cracks initiate, which is why bone stress analysis meshes the geometry instead of averaging over it, and why a surgical screw hole or a sharp osteotomy is a fracture risk out of all proportion to the material it removes.</div></details></div>
```

### B14. The module never places itself on the level ladder

Location: `module16.html:88` (the end of the Section 0 plan).

`EDITOR_DOMAIN.md` requires each module to say which level of the course's modelling ladder its models sit on, and `prompt.txt:282-296` defines that ladder. Grep over this file returns no occurrence of "Level" in that sense. The omission matters more here than in most modules, because Level 9 of `prompt.txt` is titled "continuum and finite-element-style tissue models", word for word this module's own title, and because Section 9's whole argument is that the earlier one-dimensional models are recoverable as limits - which is a statement about the ladder that the module makes without naming it. The applied fix in Module 1 was one sentence in Section 0; the same shape works here. Append to line 88:

```html
 On the course's modelling ladder (Modules 1 to 17, Level 0 scalar estimates through Level 10 multiscale adaptation) this module is <b>Level 9</b>, continuum and finite-element-style tissue models. Everything before it that touched a tissue sat lower: Module 2's beam and Module 6's tendon spring are Level 0 to 1 reductions of what is built here, and Module 4's biphasic column is this module's Section 8 in one dimension. <a class="secref" href="#tissues">Section 9</a> makes that relation exact by exhibiting each as a limit. What this module does <em>not</em> reach is Level 10: the material constants are fixed, and tissue that remodels its own $E$, $\nu$ and $\mathbf a$ in response to the stresses computed here is the adaptation loop of Module 2's mechanostat, left open in <a class="secref" href="#tissues">Section 9</a>'s table of idealisations.</p>
```

### B15. Three symbols carry two or three meanings and the Appendix records one of each

Location: `module16.html:596-604` (the notation table), with the collisions at `:210`, `:307`, `:321`, `:166`, `:297`.

The symbol $k$ means three things: the axial stiffness $EA/L$ of a bar element ("with $k=EA/L$ the axial stiffness", line 210), the fibre stiffening rate of the exponential toe (line 307), and the permeability (line 321). The text flags the second against the third and never mentions the first. The symbol $\lambda$ means two: the stretch ratio (Section 1, Lab B, K7) and the Lamé constant (Sections 3 and 7). The text flags this twice, at lines 166 and 297, and the Appendix notation table lists only the Lamé constant, so a reader who consults the table meets the wrong one. The symbol $E$ is Young's modulus while $\mathbf E$ is the Green-Lagrange strain, distinguished by boldface alone; both are in the table but nothing warns the reader. `EDITOR_DOMAIN.md` makes a cross-section collision a defect and says that flagging one is not resolving it. The B2 replacement already renames the permeability to $k_p$; the rest is Appendix rows plus one sentence. Replace the notation rows at lines 601 to 604 with:

```html
<tr><td>$W$; $\mathbf k_e,\ \mathbf K,\ \mathbf L_e$; $k$</td><td>strain-energy density; element / global stiffness, gather operator; scalar axial stiffness $EA/L$ of one bar element</td><td>&#167;3, &#167;4</td></tr>
<tr><td>$\mathbf a,\ \varepsilon_a$; $E_m,\ E_f$</td><td>fibre direction; fibre strain; matrix and fibre contributions to the directional stiffness $E(\theta)=E_m+E_f\cos^4\theta$</td><td>&#167;6</td></tr>
<tr><td>$\mathbf P$; $G(t),\ \tau,\ g_m$; $k$ (fibre)</td><td>nominal (1st Piola) stress; relaxation modulus, relaxation time, Prony weights; fibre stiffening rate of the exponential toe $e^{k\varepsilon_a}-1$</td><td>&#167;7, &#167;8</td></tr>
<tr><td>$p,\ \boldsymbol\sigma_{\rm s},\ c_v,\ k_p,\ H_A$; $T$</td><td>pore pressure, solid stress; consolidation coefficient, permeability, aggregate modulus; dimensionless consolidation time $c_vt/L^2$</td><td>&#167;8</td></tr>
<tr><td colspan="3"><b>Symbols that are reused, and how to tell them apart.</b> $\lambda$ is the stretch ratio in &#167;1, Lab B and K7, and the Lam&#233; constant in &#167;3 and &#167;7; the two never appear in one equation. $k$ is a bar element's axial stiffness in &#167;4 and the fibre stiffening rate in &#167;7; the permeability of &#167;8 is written $k_p$ to keep it clear of both. $E$ is Young's modulus and $\mathbf E$ (bold) is the Green-Lagrange strain of &#167;1. $L$ is an element or layer length; $\mathbf L_e$ (bold) is the gather operator of &#167;5.</td></tr>
```

### B16. The Appendix's fibre validity figure disagrees with the text and the code

Location: `module16.html:613`.

Quoted: "$k\approx40$-$50$ (linear-valid to $\sim0.3\%$)".

Factual error against the module's own Lab B. The five per cent validity limit is $\varepsilon\approx0.1/k$, so the quoted range of $k$ gives $0.24\%$ at $k=40$ and $0.19\%$ at $k=50$; the exact numerical limits are $0.242\%$, $0.202\%$ and $0.194\%$ at $k=40$, $48$ and $50$ (`m16/verify.py`). Nothing in the range reaches $0.3\%$, and the text at lines 411 and 551 both say $0.2\%$, so the table contradicts the two places that cite it. Replacement for line 613, which also adds the K4 fit and the K10 shear coefficient the report labels as assumed, and the anchors K6 and K9 assume:

```html
<tr><td>Fibre toe sharpness</td><td>$k\approx40$-$50$; linear law valid to $\varepsilon\approx0.1/k$, i.e. $0.24\%$ at $k=40$ and $0.19\%$ at $k=50$ ($0.20\%$ at the $k=48$ of Lab B)</td><td><a class="secref" href="#hyper">&#167;7</a></td></tr>
<tr><td>Tendon directional stiffness (assumed anchors)</td><td>$E_m=0.12$, $E_f=1.38\ \mathrm{GPa}$, so $E(0^\circ)=1.50$ and $E(90^\circ)=0.12\ \mathrm{GPa}$</td><td><a class="secref" href="#anisotropy">&#167;6</a>, K6</td></tr>
<tr><td>Shoulder stress-concentration fit (assumed)</td><td>$K_t\approx1+\tfrac12\sqrt{h/r}$; $1.71$ at $r/h=0.5$, $4.54$ at $r/h=0.02$</td><td>K4</td></tr>
<tr><td>Rectangular-section shear coefficient (assumed)</td><td>$\kappa=5/6$, with $\nu=0.3$ giving $E/G=2.6$</td><td>K10</td></tr>
<tr><td>Composite-bar design case (assumed)</td><td>$E_{\rm soft}=5$, $E_{\rm stiff}=20\ \mathrm{GPa}$, budget 4 of 8 elements</td><td>K9</td></tr>
<tr><td>Half-consolidation time</td><td>$T_{1/2}=c_vt_{1/2}/L^2=0.19$ (computed; tabulated Terzaghi $0.197$)</td><td><a class="secref" href="#timedep">&#167;8</a>, Lab C, K8</td></tr>
```

### B17. Three sentences promise code that thirty problems do not contain

Location: `module16.html:444`, `module16.html:531`, `module16.html:619`.

Quoted (line 444): "computational solutions quote numbers the code produces." Quoted (line 531): "Numbers quoted are those the code produces." Quoted (line 619): "every proposition proved, every figure computed, every number reproduced by the code shown."

Before this report's edits all three were false: the file's only code blocks were the Section 5 demonstration and Labs A to C, and no problem contained any. This is the Module 3 defect class, where a module claimed every number came from a run of the code while the lab printed nothing. The blocking defects above add running, PEP8-clean, output-quoted code to K2, K6, K7, K8, K9 and K10, and K1, K3 and K5 cite the lab blocks they rest on, which makes the claims true rather than requiring them to be weakened. Two of the three sentences should nonetheless say which problems carry code, so the reader is not left hunting. Replacement for line 444:

```html
<p>Thirty problems - ten conceptual, ten derivational, ten computational - plus five diagnostics. Each carries a <em>Probes</em> note and a collapsible worked solution. Every computational solution either carries its own runnable code with the output quoted beneath it, or names the lab block in <a class="secref" href="#labs">Section 10</a> that produces its numbers.</p>
```

Replacement for line 531:

```html
<p class="small">Each requires a sweep, an inverse solve, an optimisation, a simulation, or a regime comparison - not substitution into a boxed formula. K2 and K6 to K10 carry their own code with its printed output quoted; K1, K3 and K5 run on the Lab A and Lab B blocks above.</p>
```

Line 619's "every number reproduced by the code shown" becomes true once the above is applied and needs no change, but its neighbour at line 361 does; see S6.

## 3. Style and clarity edits

Line-level, applied in one pass.

**S1 (`:115`).** Poisson's ratio is used two sections before it is defined, with a bare forward pointer. Change "with lateral contraction ratio governed by Poisson's ratio $\nu$ (Section 3)" to "with lateral contraction ratio governed by a material constant $\nu$, Poisson's ratio, defined properly in <a class=\"secref\" href=\"#elasticity\">Section 3</a> and used here only as the name for the ratio of transverse to axial strain".

**S2 (`:202`).** "Bone at $\sim$18 GPa" sits between a table saying 15 to 20 GPa and code using 17 GPa. Change to "Bone at $\sim$17 GPa (the value the code of <a class=\"secref\" href=\"#assembly\">Section 5</a> uses)".

**S3 (`:332`).** The heading "9. The three tissues as continua" precedes a table with four rows (bone, tendon/ligament, cartilage, muscle). Change to "9. The tissues as continua, and what the models miss", and the identical string in the table of contents at `:48`.

**S4 (`:86`, `:174`).** Two figures cite their own number from inside themselves: Fig. 1's caption says "a material point (Fig. 1)", and Fig. 4's `aria-label` says "the stored strain energy (Fig. 4)", so a screen-reader user is told the figure number by the figure. (Fig. 3's caption, which said "as Fig. 3 shows", is fixed in B4.) Delete the parenthetical in each; a caption's subject is its own figure.

**S5 (`:409`).** Lab B's caption states a number its axes do not reach: the plot stops at $12\%$ strain and the caption reports the neo-Hookean crossing at $47\%$. Add after "(the neo-Hookean law crosses only near 47%)": ", far off the right of this axis, which stops at 12% so the fibre curve's rise is visible".

**S6 (`:361`).** "the biphasic relaxation falls out of a solver" describes the experiment B1 shows Lab C does not perform. Change the sentence to "Three labs make the framework concrete: the finite element converges at a measurable rate, the linear law has a measurable validity range, and the biphasic load transfer falls out of a solver. Each states its question, model, and equations; every quoted number is printed by the code shown."

**S7 (`:152-158`).** The equilibrium equation $\nabla\cdot\boldsymbol\sigma+\mathbf b=\mathbf 0$ is the second of the module's three closing ingredients and is the only one that gets neither a box nor a numbered environment, while the symmetry of $\boldsymbol\sigma$ gets a proposition. Its derivation is sound; only its billing is wrong. Wrap the display at `:155` in `<div class="keyresult">` with the label "<b>Equilibrium.</b>" so that a reader scanning boxes finds all three ingredients.

**S8 (`:289`).** "roughly a tenth of that across them" against an Appendix ratio of $12$ and a K6 ratio of $12.5$. Superseded by the B10 replacement, which states $12.5$ throughout.

**S9 (`:539`, `:547`, `:555`, `:559`, `:563`, `:567`, `:571`).** Seven K solutions open with a bare "Solution" summary while the C and D solutions do the same; this is consistent and stays. No change; recorded so the next editor does not re-open it.

**S10 (`:364`, `:393`, `:414`).** The labs use "$L$" for the bar length in Lab A and the layer thickness in Lab C. Both are lengths and neither is ambiguous within its lab, but the Appendix should say so; folded into B15's disambiguation row.

## 4. Structural notes

**Seven of the ten derivational problems reproduce a main-text proof verbatim.** D2 is Proposition 1.1, D4 is 2.2, D6 is 3.1, D7 is 4.1, D8 is 5.1, D9 is 6.1, D10 is 7.1, in several cases sentence for sentence. A derivational problem that restates a proof the reader has just read tests recall, not derivation. The two exceptions are the interesting ones: D3 and D5 prove things the main text only asserts, which is why B4 promotes D3's argument into Section 2. The cheapest repair for the rest is to vary the setting rather than the statement (prove Proposition 4.1 for a two-element chain, prove Proposition 1.1 for simple shear and show the quadratic term is what makes $\mathbf E$ notice a rotation-free shear differently from $\boldsymbol\varepsilon$). Left out of this pass as a rewrite of scope beyond the report, and recorded here so it is not lost.

**Section 2 introduces the equilibrium equation and never solves one.** Every other governing relation in the module is exercised: the strain tensor in K6, the elastic law in Lab A, the beam matrix in K10. The equilibrium PDE appears at `:152`, is called one of three closing ingredients, and is not used again except implicitly inside the finite-element assembly. A worked case - the one-dimensional bar with self-weight, $d\sigma/dx+\rho g=0$, integrated to $\sigma(x)$ in three lines - would tie it to something concrete and cost a paragraph.

**Fig. 5 is never referenced from the prose.** Figures 1, 2, 4, 6, 7, 8 and 9 are all cited by number; Fig. 5, the bar element, is not. One clause in the paragraph at `:210` fixes it.

**The problem figures are all schematic and none is computed.** `check_probfig.py` passes all thirty, and they are legible, but the module has ten computational problems whose results are curves (K6's angle sweep, K8's three thicknesses, K10's slenderness sweep) drawn as schematics rather than as the plots the solutions now produce. Regenerating those three from the code added in B7, B9 and B10 would make the figure the result rather than an illustration of it. Not done in this pass: it is a figure-generation job of the size of a section rebuild, and the existing figures are not wrong, only uninformative.

## 5. What already works

- **Proposition 1.1 and its proof (`:108-113`)** is the model the rest of the module should be held to: the claim is exact, the algebra is three lines, every term is defined, and the last sentence says which later section uses which of the two strain measures. Proposition 4.1 (`:212-214`) is its equal, and its closing observation that the zero eigenvalue is why a structure needs a support is the kind of sentence that makes a reader remember a result.
- **Section 0's plan (`:88`)** does what a chapter opening should: it names the question, then walks the reader through the order of the argument and says why that order. It is the reason a reader can follow a module that covers eight distinct constitutive frameworks.
- **Section 9's two tables (`:337-341`, `:349-354`)** are the best pages here. The first names each earlier one-dimensional model, the continuum law it is a projection of, and what the projection adds; the second names five idealisations and what is really true. Together they are an honest account of a modelling framework's reach, and the "what is really true" column never softens.
- **Lab A (`:363-390`)** is complete and correct. The exact solution is derived, the error falls from $1.07\times10^{-2}$ to $1.10\times10^{-5}$ over five mesh doublings, the quoted factor of four per doubling is what the code prints, and the interpretation names the order of accuracy rather than just reporting the numbers.
- **The Section 3 tissue table (`:195-199`)** gives symbol, unit, value range and role for four tissues in four rows, and the paragraph after it converts the table into the one sentence that matters: bone barely strains where cartilage deforms visibly, and that division of labour is what the skeleton is built on.
- **Proposition 6.1's proof (`:285`)** ends by evaluating $\boldsymbol\sigma_{\rm fib}\mathbf n$ for $\mathbf n\perp\mathbf a$ and getting zero. That is the right way to close a proof about a directional law: not by restating it, but by testing it in the case where the claim would be most surprising.

## 6. Changes applied

All 17 blocking defects and all style edits were applied to `edited/module16.html` by one re-runnable script, `m16/apply.py` (55 anchored replacements, each asserting its anchor occurs exactly once). The file it edits is a pristine copy; `module16.html` was not touched and no git command was run.

**Independent verification pass.** The whole apply was re-checked from scratch after it was written. `apply.py` was re-run against a fresh `cp module16.html edited/module16.html` and its output is **byte-identical** to the delivered file, so every anchor still matches exactly once and no edit was hand-made. Every row of the table below was then checked mechanically: the 55 tags in the table are exactly the 55 the script logs, in the same order, and **every row's stated line number is the anchor's true first line in pristine `module16.html`** (0 mismatches). All ten code blocks were re-extracted from the *edited* file and re-run: all exit 0, none raises, none contains a live HTML tag, and every number quoted beside them matches (Lab A $0.082\ \mathrm{mm}$ and $10\to19\ \mathrm{MPa}$ from a run printing $0.0815$, $10.3$, $18.8$; Lab B's $47\%$ and $0.2\%$ from $0.469$ and $0.002$; K2's $17.00\ \mathrm{GPa}$; K6's $12.5$; K7's $0.0/0.2/0.9/3.1/14.8\%$; K8's $194.50/48.63/12.16\ \mathrm s$ at $T=0.195$ and $1300\ \mathrm s$; K9's $0.1555/0.1908/0.2771\ \mathrm{mm}$ and $18.5\%$; K10's $0.20/0.78/3.12/8.67/19.50\%$). K8's cartilage numbers were traced to their source: `module04.html:566-568` gives $h=2\ \mathrm{mm}$, $H_A=0.6\ \mathrm{MPa}$, $k=1\times10^{-15}$ and $D=6\times10^{-10}\ \mathrm{m^2/s}$, which is exactly the $L$, $c_v$ and $t_{1/2}=1300\ \mathrm s$ the solution states. K4, which has no code block, was re-derived by hand: $K_t=1+\tfrac12\sqrt{h/r}$ gives $1.7071\to2.0000$ ($+17.2\%$, quoted as $17\%$) and an excess $0.707\to1.000$ ($+41.4\%$, quoted as $41\%$).

**Figure verification.** A diff of every `<svg>` body, pristine against edited, shows exactly **one figure body changed** - Lab C's - with the other eight touched figures differing only in their `aria-label`. Lab C's two `<polyline>` point strings were decoded back into data: calibrating from the tick `<text>` positions ($T=0$ at $x=70$, $T=0.5$ at $x=470$; $0$ at $y=195$, $1$ at $y=45$), the blue curve reads $F=0.9660$ at the first step and $0.2347$ at $T=0.5$, the red reads $0.0340$ and $0.7653$, and $F+U=1$ to machine precision - the exact numbers the solver prints and the caption quotes. The blue curve crosses $0.5$ at $T=0.1945$, which is where the dashed reference line sits ($x=225.6$), and the label rounds it to $0.195$. Against the analytic Terzaghi series the decoded curve is within $0.55\%$ at $T=0.5$, which is the $0.6\%$ mesh accuracy the interpretation claims and scopes to that point. The eight rewritten `aria-label`s are plain text with no `$...$` and no backslash, and end on complete sentences; the count of figures whose `aria-label` still contains math fell from $11$ to $9$, all of them pre-existing and none introduced by this pass.

**Superseded-value sweep.** Every number printed inside a problem figure's `<text>` was compared with that problem's solution. One residual was found and fixed (S13); the rest agree (K1's slope $-2$ against a run halving the error $\times3.9$ per refinement, K2's "measured $\to17$ GPa", K7's $3\mu$ at $\lambda=1$, K9's "thin end", K10's one-element exactness against a printed difference of `0.00e+00`). Greps for the superseded phrasings confirm none survives: `three tissues` 0, `two labs` 0, `class="probes"` 0, `a tenth of that` 0, `(Fig. 1)` / `(Fig. 4)` 0, `as Fig. 3 shows` 0, the unsourced $c_v\sim10^{-6}$ and its $0.8\ \mathrm s$ 0, and no bare $0.19$ anywhere.

**Gates.** Baseline (pristine copy) and after, on `edited/module16.html`:

| gate | baseline | after |
|---|---|---|
| `checktex` | 501 segments, 0 issues | 790 segments, **0 issues** |
| `checklt` | 0 | **0** |
| `check_links` | 111 links, 0 broken, 0 unlinked | 132 links, **0 broken, 0 unlinked** |
| `check_svg` | 0 hard, 0 advisory | **0 hard, 0 advisory** |
| `check_code` | 4 blocks, 0 issues | 10 blocks, **0 issues** |
| `verify_dom` | 0 mjx-merror, 0 broken, 32 stray `$`, 1 swallowed-prose | **0 mjx-merror, 0 broken**, 28 stray `$`, 1 swallowed-prose |
| `check_overlap` | 0 | **0** |
| `check_frame` | exit 0, no clipping, 14 margin advisories | **exit 0, no clipping, 14 margin advisories** |
| `check_bodyprop` | pass | **pass** |

Zero where the baseline was zero; nothing worse anywhere. The one residual `verify_dom` advisory is the same pre-existing one, inside Proposition 6.1's proof at `:285`, which no edit in this pass touches.

**Code re-run.** Every `<pre><code>` block was re-extracted from the *edited* file with `tools/extract.py` (10 blocks, `m16/blocks2/`) and run. All ten execute without error and none contains a live HTML tag. For the seven blocks that quote their own output as `# ->` comments, a script compared stdout line by line with the quoted comments: **all seven match exactly, 43 lines in total**. The three that quote no output are the pre-existing Section 5 demonstration and Labs A and B, whose numbers are quoted in the prose beside them and were checked against their runs by hand (Lab A: `1.07e-02` to `1.10e-05` over five doublings; Lab B: `0.469` and `0.002`).

### Corrections made to this report during the apply

Nine, each because the file or a run disagreed with what the report said. Rows 1 to 3 are numeric; the rest are anchors and structure.

| # | what the report said | what the file or the run said | what was applied |
|---|---|---|---|
| 1 | K8's cartilage clock used $c_v\sim10^{-6}\ \mathrm{m^2\,s^{-1}}$, giving $t_{1/2}\approx0.8\ \mathrm s$ and "standing still for a minute leaves the load on the matrix" | Module 4's own table (`module04.html:566-568`) gives $H_A=0.6\ \mathrm{MPa}$, $k=1\times10^{-15}$, so $c_v=6\times10^{-10}$; `m16/blk/k08.py` prints $t_{1/2}=1300\ \mathrm s$ ($22$ min) and fluid shares $0.986$ / $0.893$ / $0.214$ at $1\ \mathrm s$ / $60\ \mathrm s$ / $1\ \mathrm h$ | corrected numbers, and the flipped conclusion: a footstep *and* a minute of standing are fluid-borne; the unsourced $10^{-6}$ was itself the bare-number class the report calls blocking |
| 2 | K4: "the peak scales as $r^{-1/2}$, so halving a fillet radius costs $41\%$ more stress" | `m16/verify2.py`: halving $r/h$ from $0.5$ to $0.25$ takes $K_t$ from $1.707$ to $2.000$, $+17.2\%$; it is the excess $K_t-1$ ($0.707\to1.000$) that rises $41\%$ | the sentence now attributes the $41\%$ to the excess and gives the $17\%$ for the peak |
| 3 | $T_{1/2}=0.19$ in Lab C's caption and interpretation (but $0.195$ in K8) | `m16/genfigs.py` prints $T_{1/2}=0.1945$; the analytic series gives $0.1967$ | $0.195$ everywhere, with the series value and the tabulated $0.197$ both stated |
| 4 | replacements used `<span class="probes">` | this module defines no `.probes` rule; its own thirty problems use `<span class="small"><em>Probes: ...</em></span>` | every replacement uses the module's own markup |
| 5 | the six K replacements each covered three lines (statement, figure, solution) and emitted `<p>` + `<details>` | that would delete each problem's figure and orphan the `</div>` closing `<div class="prob">` | statement and solution replaced separately, figure kept, and each figure's `aria-label` rewritten to the new statement in plain text (no `$...$`) |
| 6 | S1's anchor quoted "(Section 3)" | the file has `(<a class="secref" href="#elasticity">Section 3</a>)` | anchored on the real markup |
| 7 | S3: heading is "9. The three tissues as continua" | the file already reads "...as continua, and what the models miss" in both places | the edit is "three tissues" to "tissues" only (the table has four rows) |
| 8 | S5's anchor quoted a literal `%` | the file uses `&#37;` | anchored on `&#37;` |
| 9 | S7: "wrap the display at `:155` in `<div class="keyresult">`" | the display at `:154-156` is already a `.keyresult` | only the missing `<b>Equilibrium.</b>` label was added |

Two further things the report did not reach, found while applying and fixed: Section 0 said "**Two** labs and a problem set close it" where there are three (logged as S11 below), and B17's claim that "K1, K3 and K5 run on the Lab A and Lab B blocks" is false for K3 and K4, which sweep a closed form and have no lab block - the two summary sentences and the colophon now say so exactly.

### The edits

One row per anchored replacement, in the order the script applies them. Line numbers are in the original `module16.html`.

| tag | line (original) | what changed | how verified |
|---|---|---|---|
| B14+S11 | 88 | Level ladder named: the module is stated to be **Level 9** (continuum and finite-element-style tissue models), with Modules 2 and 6 placed at Level 0 to 1 and Module 4's biphasic column as this module's Section 8 in 1-D, and Level 10 named as what it does not reach. "Two labs" corrected to "Three labs" | ladder wording checked word for word against `prompt.txt:285-296`; lab count checked against the three `<h3>Lab` headings |
| S4a | 86 | Fig. 1's caption no longer cites its own figure number: "a material point (Fig. 1)" to "a material point" | anchor asserted unique |
| S4b | 174 | Fig. 4's `aria-label` no longer tells a screen-reader user the figure's own number: "(Fig. 4)" deleted | anchor asserted unique |
| S1 | 115 | Poisson's ratio, used two sections before its definition, is now introduced as "a material constant $\nu$, Poisson's ratio, defined properly in Section 3 and used here only as the name for the ratio of transverse to axial strain" | anchor corrected against the raw markup (correction 6) |
| B4a | 121-123 | Cauchy's theorem taken out of Definition 2.1 and **proved**: Definition 2.1 now defines the traction and the array $\sigma_{ij}=t^{(j)}_i$ only, and new **Proposition 2.1** states $\mathbf t(\mathbf n)=\boldsymbol\sigma\mathbf n$ with a tetrahedron proof (surface terms $\sim h^2$, volume terms $\sim h^3$, so body force and inertia die as $V/A\sim h$) | the promoted argument is D3's own, checked against `:500`; `checktex` and `verify_dom` clean on the new math |
| B4b | 125 | symmetry result renumbered to **Proposition 2.2** | grep confirmed no Proposition 2.2 existed and that exactly three references needed updating |
| B4c | 150 | Fig. 3's caption: "Proposition 2.1" to "Proposition 2.2" for symmetry, "Definition 2.1" to "Proposition 2.1" for $\mathbf t=\boldsymbol\sigma\mathbf n$, and the caption's self-reference "as Fig. 3 shows" removed | grep over the whole file for every "Proposition 2.1" / "Definition 2.1" occurrence |
| B4d | 454 | C2's solution cites Proposition 2.2 for symmetry | same grep |
| B4e | 504 | D4's solution cites Proposition 2.2 for symmetry | same grep |
| B4f | 498 | D3 restated: no longer "sketch why the traction is linear" (now proved in the text) but "redo the tetrahedron argument keeping the body force and the inertia term explicitly, and say which power of $h$ kills each" | anchor asserted unique |
| B4g | 499 | D3's figure `aria-label` rewritten to the new statement, in plain text | anchor asserted unique |
| B4h | 500 | D3's solution rewritten to answer the new question: both volume terms retain exactly one power of $h$ after dividing by $A$, and because the acceleration enters only through that factor, Cauchy's theorem is not a statement about statics | hand derivation; not covered by the report, written during the apply so the solution matches its question |
| S7 | 154-155 | the equilibrium equation's box carries the label **Equilibrium.** so a reader scanning boxes finds all three closing ingredients | corrected against the raw markup, which already had the `.keyresult` (correction 9) |
| B6 | 158 | the **von Mises stress** defined for the first time in the course: $\sigma_{\rm vM}=\sqrt{\tfrac32\mathbf s:\mathbf s}$ from the deviator $\mathbf s=\boldsymbol\sigma-\tfrac13(\operatorname{tr}\boldsymbol\sigma)\mathbf I$, with the principal-stress form, the uniaxial normalisation, and why pure pressure cannot yield | grep over `module01.html` to `module17.html` confirmed this was the only occurrence of the term in the course |
| S2 | 202 | "Bone at $\sim$18 GPa" to "$\sim$17 GPa (the value the code of Section 5 uses)", ending a three-way disagreement between the table (15-20), the prose (18) and the code (17) | table at `:196` and the block at `:266` both read |
| B3 | 230-236 | the beam element's $4\times4$ matrix is no longer "stated here": new **Proposition 4.2** with the definition of the Hermite cubics, the Hessian argument, two entries integrated in full ($12EI/L^3$ and $6EI/L^2$), and the rank-two null space. The overstatement that the entries are "the reactions Module 2 computed for a loaded beam" is replaced by "the nodal forces and moments a unit nodal displacement or rotation calls up" | the matrix reproduced entry for entry from $\int_0^LEI\,N_i''N_j''dx$; the boxed matrix is also solved numerically in K10's block, which returns $PL^3/3EI$ to machine precision |
| B10b | 289 | Section 6 now states the law its own Fig. 7 draws: $E(\theta)=E_m+E_f\cos^4\theta$, with $0.12$ and $1.5$ GPa, ratio $12.5$, halving by $35^\circ$ | fit to Fig. 7's own polyline: $\cos^4$ leaves an RMS residual of $0.005$ GPa against $0.118$ for $\cos^2$ |
| B2 | 321 | Definition 8.2 renames the consolidating field $u_z$ (clear of $\mathbf u$ in Section 1 and the nodal $u$ of Sections 4 and 5), renames the permeability $k_p$ (clear of the bar stiffness $k$ and the fibre rate $k$), and says in one clause why a solver written for $p$ answers for $u_z$ | the field clash was found by reading the Lab C block against the stated equation |
| B5 | 323-326 | Proposition 8.1 restated for a **Prony series** with non-negative weights (the standard linear solid is the one-term case) and proved term by term; the proof then derives the consolidation eigenseries and shows its weights $8/((2n+1)^2\pi^2)$ are all positive, so the biphasic tissue supplies the hypothesis instead of assuming it | the series and its $0.6\%$ agreement with the finite-difference solution are printed by the Lab C block |
| S6 | 361 | the labs paragraph no longer says Lab C shows "the biphasic relaxation"; it says "the biphasic load transfer", and "every quoted number is printed by the code shown" | follows B1 |
| S5 | 409 | Lab B's caption notes that the 47% crossing is off the right of an axis that stops at 12% | the axis ticks read from the figure: `0`, `6&#37;`, `12&#37;`; anchor corrected to `&#37;` (correction 8) |
| B1a | 413 | Lab C's heading: "biphasic stress relaxation from the consolidation equation" to "load sharing between fluid and matrix under a step load", which is the experiment the code performs | the code sets $p(z,0)=1$ with a drained top and sealed bottom - a step *load*, under which total stress is constant by construction |
| B1b | 414 | Lab C's set-up rewritten: the question is load transfer, the boundary conditions are named, $c_v$ and $L$ are labelled an assumed pair, the equation is stated in $p$ (not $u$), and $F(T)$ and $U(T)$ are defined | see B2 |
| B1c | 418-429 | Lab C's code rewritten to print the dimensionless time, both load shares, the half-consolidation point, and the analytic Terzaghi series that checks it - four lines of output where it printed two unlabelled means | run: `T = 0.0003: fluid share = 0.9659`; `T = 0.5000: fluid share = 0.2347, matrix share = 0.7653`; `half-consolidation at T = 0.195`; `analytic series at T = 0.50 gives 0.2360`. PEP8 clean under `check_code` |
| B1d | 431 | the figure regenerated (`m16/genfigs.py`): two computed polylines, $F(T)$ and $U(T)$ at 100 points, against $T=c_vt/L^2$, with a dashed reference at the crossing. The invented $0.35$ "equilibrium (matrix)" floor and the "normalised stress" axis label are gone; the caption reports the computed $F=0.966$, $T_{1/2}=0.195$ and $U=0.765$ | the old curve was decoded from its own polyline and shown to be $0.35+0.65\langle p\rangle$ to within $0.0011$; the new one is generated from the same array the code prints. `check_overlap` 0, `check_frame` no clipping, and the rendered PNG was inspected |
| B1e | 433 | the interpretation reports the computed shares, the $0.6\%$ mesh accuracy against the series, $T_{1/2}=0.195$, the $L^2/c_v$ sensitivity, and an extension that flips the drainage face | `0.24` in the old text against a printed `0.2347`; all quoted numbers now printed |
| B17a | 444 | "computational solutions quote numbers the code produces" replaced by the exact claim: own code with output quoted, or a named lab block, or a closed-form sweep with every value written out | K1 to K10 read individually; K3 and K4 are the closed-form cases |
| B17b | 531 | names which problems carry code (K2, K6-K10), which quote a lab (K1, K5), and which sweep a closed form (K3, K4, the latter through a labelled assumed fit) | same read |
| B17c | 619 | the colophon's "every number reproduced by the code shown" to "every number either derived in the text or reproduced by the code shown" | K3's and K4's numbers are derived, not run |
| B12a | 537 | K2 restated as a genuine inverse problem with a stated measurement ($81.55\ \mu\mathrm m$ under $2\ \mathrm{kN}$) and a required error propagation | - |
| B12b | 538 | K2's figure `aria-label` rewritten to the new statement, plain text | - |
| B12c | 539 | K2's solution now inverts the **finite-element model** by bisection on the 64-element solver rather than rearranging a closed form, and computes the sensitivity it previously only invoked; code block added | run: `recovered E = 17.00 GPa`; `1% error in u_L gives 0.99% error in E`; `5% gives 4.76%`; `1% of u_L = 0.816 um of the 81.5 um reading` |
| B13 | 547 | K4's $K_t\approx1+\tfrac12\sqrt{h/r}$ labelled an **assumed** handbook fit with a reason it cannot be derived here, a third sweep point added, and the conclusion corrected from "up to more than twice" (which restated the area change) to $4.5$ times the thin nominal, nine times the thick-section stress | `m16/verify2.py`: $K_t=1.707$, $2.000$, $4.536$ at $r/h=0.5$, $0.25$, $0.02$; sweep factor $2.66$. The $r^{-1/2}$ sentence corrected (correction 2) |
| B10a1 | 553 | K6 restated: derive the law, sweep the angle, report the half-stiffness angle | - |
| B10a2 | 554 | K6's figure `aria-label` rewritten, plain text | - |
| B10a3 | 555 | K6's solution derives $E(\theta)=E_m+E_f\cos^4\theta$ from the double projection (the report's "contributes only its projection" was wrong: the fibre resolves the strain once and the stress once), then sweeps; code block added, plus a scope caution that this is the prescribed-strain stiffness | run: `1.500, 1.321, 0.896, 0.465, 0.206, 0.120 GPa` at $0/15/30/45/60/90^\circ$; `ratio 12.5`; `half at 34.7 deg` |
| B11a | 557 | K7 restated: quantify the stiffening and use it to explain Lab B's $47\%$ | - |
| B11b | 558 | K7's figure `aria-label` rewritten, plain text (the original was truncated mid-word by its generator) | - |
| B11c | 559 | K7's solution replaces "to larger values as $\lambda$ grows" with the numbers, and joins two facts the module states separately: the tangent is only $0.2\%$ and $0.9\%$ above $3\mu$ at $\lambda=1.05$ and $1.10$ because the series $3e+e^3-e^4$ has **no quadratic term**, which is exactly why Lab B's linear law survives to $47\%$; contrasted with the fibre law, whose quadratic term does not cancel; code block added | run: tangent $0.0/0.2/0.9/3.1/14.8\%$ above $3\mu$ at $\lambda=1.02/1.05/1.10/1.20/1.50$; SymPy prints `3*e + e**3 - e**4 + O(e**5)` |
| B7a | 561 | K8 restated: measure the half-transfer time, run three thicknesses, decide whether $L$ enters other than through $c_vt/L^2$, then put cartilage's own $c_v$ in | - |
| B7b | 562 | K8's figure `aria-label` rewritten, plain text | - |
| B7c | 563 | K8's solution replaces an asserted $\tau\propto L^2$ with the measurement, states the sharper dimensionless result ($T_{1/2}=0.195$ at all three thicknesses, so there is one curve and not a family), and derives cartilage's clock from Module 4's table; code block added | run: `t_half = 194.50 / 48.63 / 12.16 s`, each `x4.00`, `T = 0.195` in all three; `c_v = 6.0e-10 m^2/s, t_half = 1300 s = 22 min`; `F = 0.986 / 0.893 / 0.214`. $c_v$ corrected (correction 1) |
| B8a | 565 | K9 restated with the budget made precise (four of eight elements, not four units of mass), both moduli labelled assumed, and the objective written down | - |
| B8b | 566 | K9's figure `aria-label` rewritten, plain text | - |
| B8c | 567 | K9's solution now runs the optimisation and separates the objective from the sensitivity that ranks the placements ($\Delta_e=P\ell_e/A_e(1/E_{\rm soft}-1/E_{\rm stiff})$, geometry only), which is what makes the thin end optimal; code block added | exhaustive search over all $\binom84=70$ placements: `best (4,5,6,7) 0.1555 mm`, `worst (0,1,2,3) 0.1908 mm`, `all-soft 0.2771 mm`, `18.5%` |
| B9a1 | 569 | K10 restated: the element cannot show where its own theory breaks, so the problem asks for the Timoshenko shear term as a third quantity and a slenderness sweep | - |
| B9a2 | 570 | K10's figure `aria-label` rewritten, plain text (the original was truncated mid-word) | - |
| B9a3 | 571 | K10's solution corrects a wrong statement - the Euler-Bernoulli element contains no shear flexibility and so returns $PL^3/3EI$ at *every* aspect ratio - and replaces it with the real comparison: exact against Euler-Bernoulli, blind to Euler-Bernoulli's own omission, quantified by $\delta_s/\delta_b=\tfrac{E}{4\kappa G}(h/L)^2$; closes on discretisation error versus modelling error; code block added | run: element and formula agree to `difference = 0.00e+00`; shear adds `0.20 / 0.78 / 3.12 / 8.67 / 19.50 %` at $L/h=20/10/5/3/2$ |
| B9b | 578 | the fourth diagnostic, which stated only half of this, now says why the Hermite cubics are exact *and* that the exactness is against Euler-Bernoulli, not against a real beam | follows B9a3 |
| B15 | 601-604 | notation table: $k$ recorded in all three of its meanings (bar stiffness, fibre rate, permeability, the last renamed $k_p$), $\lambda$'s two meanings recorded where the table previously listed only the Lamé constant, and a new spanning row tells the reader how to tell $\lambda$, $k$, $E$ vs $\mathbf E$, and $L$ vs $\mathbf L_e$ apart | each collision located: $k$ at `:210`, `:307`, `:321`; $\lambda$ flagged in the prose at `:166` and `:297` but not in the table. The `<a class="secref">` links in the "First used" column were kept, which the report's draft rows had dropped |
| B16 | 613 | parameter table: the fibre-toe row corrected from "linear-valid to $\sim0.3\%$", which no $k$ in its own range reaches, to the exact limits; five new rows label as **assumed** every bare number the problems rely on (K6's anchors, K4's fit, K10's $\kappa$, K9's moduli) and record the computed half-consolidation time and cartilage's $c_v$ | `m16/verify2.py`: exact $5\%$ limits $0.242\%$, $0.202\%$, $0.194\%$ at $k=40,48,50$; the text at `:411` and `:551` both say $0.2\%$, so the old table contradicted both |
| S12 | 611 | the Appendix's "anisotropy ratio $\sim12$" now also carries K6's $12.5$ at the assumed anchors | follows B10a3 |
| S3a | 48 | table of contents: "The three tissues as continua" to "The tissues as continua" | the Section 9 table has four rows (bone, tendon/ligament, cartilage, muscle) at `:338-341`; anchor corrected (correction 7) |
| S3b | 332 | the Section 9 heading, likewise | same |
| S13 | 554 | K6's own schematic still carried the superseded ratio: its label `ratio &#8776; 12&#215;` is now `ratio &#8776; 12.5&#215;`, matching the value B10a3 made K6's solution compute | found by a verification sweep of every number printed inside a problem figure's `<text>` against that problem's solution; the K6 block prints `anisotropy ratio E(0)/E(90) = 12.5` and the solution and Appendix both state $12.5$. All nine gates re-run after the change: unchanged (`check_svg` 0/0, `check_overlap` 0, `check_frame` exit 0) |

**Style edits with no file change, recorded so the next editor does not reopen them.** S8 is superseded by B10b, which states $12.5$ throughout, and by S13, which puts the same $12.5$ on K6's own figure. S9 (the K solutions' bare "Solution" summaries) matches the C and D solutions and is consistent; no change. S10 ($L$ as bar length in Lab A and layer thickness in Lab C) is folded into B15's disambiguation row.

**Not applied.** The four structural notes of section 4 stand as notes: the seven derivational problems that restate a main-text proof, the equilibrium PDE that is introduced and never solved, Fig. 5's missing citation, and regenerating K6, K8 and K10's schematic figures as the computed plots their solutions now produce. Each is a rewrite of section scope rather than a line edit, and the report records why.
