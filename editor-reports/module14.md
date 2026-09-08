# Editor report: module14.html (Aging, Injury, Degeneration, and Adaptation)

Editorial pass. Standard: the five-part rule of the `science-editor` skill, read against `EDITOR_DOMAIN.md`. Every location is `module14.html:LINE` in the pristine 528-line file. Every replacement is valid HTML with MathJax delimiters and uses only the box classes the stylesheet defines. All four Python blocks in the file were extracted and run (`m14/blocks/`); the labs were re-implemented as parameterised functions and swept (`m14/gen.py`, `m14/gen2.py`); the ten new computational solutions carry code that was written, PEP8-checked and run before it was pasted (`m14/kcode/k01.py`…`k10.py`). Three figures were regenerated from `m14/gen3.py` → `figs.json`. Sixty-three anchored replacements were applied. **Every number in a replacement below was printed by a run.**

## 1. Verdict

Yes, after revision. A graduate reader with no biomechanics can learn from these pages the one idea the module is built on — that aging is the drift of half a dozen measurable parameters through thresholds that daily tasks already sit close to — and Propositions 2.1, 3.1, 3.2, 5.1, 6.1 and 7.1 are each short, correct and genuinely proved. What stops the reader is the problem set and two claims that the module's own arithmetic contradicts.

The largest defect is structural: **not one of the ten computational problems carries a line of code**, while the module asserts three times that it does ("every quoted number is reproduced by the code shown", `:188`; "computational solutions quote numbers the code produces", `:305`; "every number reproduced by the code shown", `:495`). Four of the ten K problems are also duplicates or two-line divisions: K2 restates D8, K4 restates Lab D number for number, K6 is `20/1.5` and `20/1`. Under the level the course sets, that is busywork.

Two results are wrong. **K3's threshold is wrong by a factor of two to three**: run with the module's own $\kappa=\beta=0.010$, the saddle-node sits at $L^\star=0.211$, not "between $0.4$ and $0.6$"; $L=0.4$ and $L=0.6$ both run away (in $153.5$ and $84.0$ years), and the "stable $h\approx1.2$ mm at $L=0.4$" is a transient, not an equilibrium. **The "two hundred years of headroom" of `:84`** (and "more than a century" of `:315`) is impossible in the module's own law: $a^\star-a_0=\frac1r(1-D/\tau_p)$ is bounded above by $1/r=100$ years, and two extra reserve units buy $66.7$.

Three more are internal contradictions the reader can catch. §7 and C9 say a $20\%$ strength gain pushes the chair-failure age "back out by a similar span" of two decades; Lab A's own figure says $10.5$ years. K9 puts $J_{\rm eff}=7.3$ N s at age 70; the Section 6 figure, generated from the same model, plots $6.34$. Lab C's runaway curve was clamped at the axis ceiling of 9 MPa and drawn flat from year 43 to year 60, so the figure showed a plateau where the caption claimed a runaway.

Then the scaffolding. Proposition 4.1's "proof" assumes its own conclusion ($A\propto h^{n_{\rm c}}$ is asserted, not derived), so the exponent that drives the whole osteoarthritis loop rests on nothing. Proposition 3.2 drops the weight's work over an $11.0$ cm compression stroke that is $16\%$ of the fall height, understating the peak force by $8.1\%$ in the unsafe direction — the same omission this editor phase already fixed in Module 2 §6. Section 8, the synthesis, is three coupling claims with no equation, no rate and no timescale, and K5 asks the reader to simulate a coupled model the module never writes down. $\sigma$ means specific tension in §2 and sensor noise in §5–§6; $k$ means landing stiffness in §3 and the mechanostat rate in C10. About twenty numbers sit in no table and follow from no derivation, including $\omega_0$, $m_{\rm eff}$, $k$, $b$, $\Delta t$, $c\sigma$, $p_0$, $\kappa$, $\beta$ and $\bar J$; the parameter table has eight rows. And the module never says where its models sit on the course's level ladder.

Finally, the stylesheet numbers figures with a CSS counter over every `<figure>`, so with two figures in §0 and only the first referenced, eight of the nine in-prose `(Fig. N)` references point one figure too early.

None of this touches the six propositions, which are sound.

## 2. Blocking defects

Ranked: false or unreproducible numbers first, then asserted results, then missing scaffolding.

### B1. Not one computational solution carries code, while the module claims three times that all of them do

Location: `module14.html:396, 400, 404, 408, 412, 416, 420, 424, 428, 432` (the ten K solutions); the claims at `:188`, `:305`, `:392`, `:495`.

Quoted (`:392`): "Each requires a sweep, an inverse solve, an optimisation, a simulation, or a regime comparison - not substitution into a boxed formula. <em>Numbers quoted are those the code produces.</em>"

Quoted (`:495`): "every proposition proved, every figure computed, every number reproduced by the code shown."

Fails part 5 (a tie to something concrete) and the house rule that K solutions carry Python-verified numbers with code. `extract.py` finds four `<pre><code>` blocks in the whole file, all in §9's Labs A–D. The ten K solutions between them state roughly forty numbers with no way for the reader to reproduce one. This is the Module 3 §9.4 defect class, and here it covers the entire problem set.

The fix is ten code blocks, one per K solution, in the same `.codewrap` markup as Lab A (`:193`), each written, PEP8-checked with `pycodestyle` and run before pasting, with its real stdout appended as `# ->` comments. The blocks are in `m14/kcode/`. Four of the solutions were rewritten at the same time because they were also duplicates (B1a below).

**Verification.** All ten run clean; `check_code.py` reports 0 issues over 14 blocks. Numbers reproduced: K1 $181.8/200.0/272.7$ N m and failure ages $83/77/54$; K7 $\rho_{\rm c}=0.640/0.728/0.791/0.843/0.886$ at $h_{\rm f}=0.3\ldots1.1$ m; K8 ages $54/77/83$; K10 $3.50\to7.00/4.22/4.67$ singly and $9.84$ for all three.

### B1a. K2, K4 and K6 are restatements, not problems

Location: `module14.html:400` (K2 = D8 at `:381`), `:408` (K4 = Lab D interpretation at `:293`), `:416` (K6).

Quoted (K2, `:400`): "Fracture at $S=F$ gives $(\rho/\rho_0)_{\rm crit}=\sqrt{F/S_0}$. With the bare-floor impact $F=4.4\ \mathrm{kN}$ and $S_0=7\ \mathrm{kN}$, the critical density is $0.79$" — which is D8's sentence with the same two numbers.

Quoted (K6, `:416`): "a $20\%$ deficit (two decades of drift) closes in $\approx13$ weeks; detraining at the disuse rate … loses the same in $\approx20$ weeks." Two divisions.

Fails the house K-problem standard ("must require numerical integration, optimization, an inverse problem, a sensitivity sweep, or a regime comparison"). Each was deepened without changing what it probes:

- **K2** now inverts for the landing stiffness a protector must not exceed, $k\le[S_0(\rho/\rho_0)^2]^2/(2m_{\rm eff}gh_{\rm f})$, across a fall-height sweep. Computed: to protect $\rho/\rho_0=0.60$ from a $0.70$ m fall the landing must be softer than $13.2$ kN/m against the bare floor's $40$; at $\rho/\rho_0=0.80$ the requirement relaxes to $41.8$ kN/m. Because $k_{\max}\propto\rho^4$ and only $\propto1/h_{\rm f}$, the specification is set by the bone, not the fall: over $h_{\rm f}=0.5$ to $0.9$ m the $\rho/\rho_0=0.60$ requirement moves only $18.5\to10.3$ kN/m, while dropping the density from $0.80$ to $0.60$ tightens it by $3.2\times$.
- **K4** now asks how far the delay must drift to overtake the margin. Computed: elasticities at the young point are $+1.11$ ($b$), $-0.37$ ($\Delta t$), $-0.11$ (noise); the delay would have to reach $0.38$ s, a $3.2$-fold slowing, to cost as much as halving the margin does.
- **K6** now integrates a training duty cycle. With $k_{\rm build}=1.5\%$/wk and $k_{\rm lose}=1.0\%$/wk, holding ground needs $f=k_{\rm lose}/(k_{\rm build}+k_{\rm lose})=0.40$ — two weeks in five spent merely to stay level; a $20\%$ gain over a year needs $f=0.55$ ($29$ training weeks in $52$), over six months $f=0.71$ ($18$ in $26$).

### B2. K3's threshold, its regime labels and its "stable thickness" are all wrong

Location: `module14.html:402-404` (statement, figure, solution); the pointer at `:263`.

Quoted (`:404`): "at full load ($L=1.0$) and at $L=0.6$ the cartilage runs away to zero, but at $L=0.4$ it settles to a stable $h\approx1.2\ \mathrm{mm}$ - a threshold between $0.4$ and $0.6$ separating a degenerating joint from a maintained one."

Factual error, and the module's own Lab C code settles it. Setting $dh/dt=0$ gives $L_{\rm eq}(h)=\beta(h_0-h)/[\kappa p_0(h_0/h)^{n_{\rm c}}]$, whose maximum is the saddle-node. Computed with $\kappa=\beta=0.010$, $p_0=3$ MPa, $h_0=2$ mm, $n_{\rm c}=0.7$:

```
saddle-node at L* = 0.211, h* = 0.824 mm
L=0.10: maintained, h = 1.669 mm at 400 yr
L=0.20: maintained, h = 1.187 mm at 400 yr
L=0.40: cartilage spent (h=0.30 mm) at t = 153.5 yr
L=0.60: cartilage spent (h=0.30 mm) at t =  84.0 yr
L=1.00: cartilage spent (h=0.30 mm) at t =  44.5 yr
```

So $L=0.4$ does **not** settle: at 60 years it is passing through $h=1.379$ mm on its way to the floor, and the quoted "stable $h\approx1.2$ mm" is where $L=0.5$ happens to be at year 60. The true threshold is $0.211$, half of the lower bound the solution claims. The figure drew the $L=0.4$ transient as the "low: stable" curve, and plotted $Lp$ on an axis labelled "peak stress (MPa)", so its $t=0$ value read $1.2$ MPa where $p_0=3.0$ MPa.

The statement was rewritten to ask for the bifurcation rather than a bracket, the solution replaced (it now derives $L_{\rm eq}(h)$, identifies the saddle-node and the two branches below it, and reports the runaway times above it), and the figure regenerated as a bifurcation diagram: $L_{\rm eq}(h)$ against $h$ with the maximum marked at $L^\star=0.211$, $h^\star=0.82$ mm, "above: no steady state, runaway" and "below: maintained". Lab C's `Extension` pointer at `:263` was corrected from "(Problem K3 does exactly this)" to "K3 does this and finds $L^\star=0.211$, well below the $L=1$ drawn here."

Two lessons the corrected solution now carries and the old one could not: the threshold is far below the loads a knee actually sees, which is a statement about how coarse the damage law is rather than a clinical recommendation; and above the threshold the failure *rate* still varies more than threefold with $L$, so unloading a joint already past $L^\star$ does not save it but can move the failure out of a lifetime.

### B3. Section 8, the synthesis, has no model — and K5 asks the reader to simulate one

Location: `module14.html:176-184` (§8), `:410-412` (K5 statement, figure, solution).

Quoted (§8, `:182`): "<b>Weakness feeds bone loss:</b> sarcopenic muscles pull less hard on bone, and the reduced load lowers the mechanostat stimulus of Section 7, so muscle loss accelerates bone loss."

Quoted (K5, `:412`): "With muscle following a disuse rate that steepens as it weakens, and bone driven by the muscle-generated load through its own mechanostat, the coupled system shows muscle declining $\sim12\%$ over forty years … the two curves lock together and steepen."

Fails parts 1, 3 and 5, and the domain brief's ban on qualitative substitutes ("*the glutes stabilize the hip*"): §8 states three couplings and gives no equation, no gain and no timescale for any of them. K5 is then unsolvable from the text alone. The existing K5 figure is also not a simulation of anything: reading its polylines back, muscle falls **linearly** to $0.875$ over forty years ($0.31\%$/yr, not the module's $1\%$/yr) and bone is flat for 15 years then **linear** to $0.783$. A mechanostat integrating a linear stimulus deficit gives a quadratic, not a straight line, so no coupled model produces that picture, and the claimed "steepening" does not occur anywhere in it.

Replacement for §8: a boxed proposition with its proof, inserted before "Three couplings dominate (Fig. 9)".

```html
<p>One of the three couplings can be written down with the machinery already built, and doing so is what turns the list below into a model. Bone's mechanostat stimulus $\Sigma$ of Proposition 7.1 is set mainly by muscle force, so a muscle capacity that drifts is a bone stimulus that drifts.</p>
<div class="prop"><b>Proposition 8.1 (a drifting muscle makes bone fall quadratically).</b> Let muscle capacity fall linearly, $C_{\rm m}(t)=1-rt$, in units of its young value, and let bone take that capacity as its mechanostat stimulus, $\Sigma=C_{\rm m}$, with the setpoint at the young value, $\Sigma_0=C_{\rm m}(0)=1$. Then bone capacity obeys $\mathrm dC_{\rm b}/\mathrm dt=k_{\rm ad}(\Sigma-\Sigma_0)$ and
$$\boxed{\;C_{\rm b}(t)=1-\tfrac12 k_{\rm ad}r\,t^{2}.\;}$$
Bone loss is quadratic in time while muscle loss is linear: the bone curve is flat at $t=0$ and steepens without bound, and its loss scales linearly with the muscle loss rate $r$, so halving $r$ halves the bone deficit at every age.</div>
<div class="proof">By hypothesis $\Sigma-\Sigma_0=(1-rt)-1=-rt$, so $\mathrm dC_{\rm b}/\mathrm dt=-k_{\rm ad}rt$. Integrating from $C_{\rm b}(0)=1$ gives $C_{\rm b}(t)=1-\tfrac12k_{\rm ad}rt^2$. The rate $\mathrm dC_{\rm b}/\mathrm dt=-k_{\rm ad}rt$ vanishes at $t=0$ and grows linearly, which is the steepening; and both $C_{\rm b}$ and its rate depend on $r$ only through the product $k_{\rm ad}r$, so scaling $r$ scales the deficit $1-C_{\rm b}$ by the same factor. If instead the muscle is held at its young value, $r=0$, then $\Sigma=\Sigma_0$ for all $t$ and $C_{\rm b}\equiv1$: bone does not drift at all. <span class="qed">&#8718;</span></div>
<p>K5 puts numbers on this with $k_{\rm ad}=0.03125\ \mathrm{yr^{-1}}$, an assumed rate chosen so that the model's forty-year bone loss matches the $25\%$ the parameter table records. The other two couplings below are stated as mechanisms and nothing more: this module writes no equation for either, so read them as directions a model could take, not results.</p>
```

K5 was rewritten to integrate that pair for $r=0.01$, $r=0.005$ and $r=0$, and its figure regenerated from the same code. Computed:

```
r=0.010/yr: muscle 0.600, bone 0.750, strength 0.562 at 40 yr
           fracture density at t = 37 yr (age 77)
r=0.005/yr: muscle 0.800, bone 0.875, strength 0.766 at 40 yr
           fracture density at t = beyond 40 yr
r=0.000/yr: muscle 1.000, bone 1.000, strength 1.000 at 40 yr
           fracture density at t = beyond 40 yr
```

At the module's own $r=0.01$ yr⁻¹ the coupled model reaches the Lab B fracture density $0.7915$ at year 37, i.e. age 77 — the same year the chair rise fails in §2, because in this model both thresholds are driven by the single muscle drift. Halving the muscle rate halves the bone deficit exactly and pushes the crossing past age 80; holding the muscle removes the bone drift entirely. The solution also states the model's limits: it couples one pair, holds $k_{\rm ad}$ constant, and ignores hormonal bone loss that continues under load.

### B4. Proposition 4.1's proof assumes its conclusion

Location: `module14.html:122`.

Quoted: "Modelling the area's thickness dependence as a power law $A\propto h^{n_{\rm c}}$ yields $p_{\rm peak}=p_0(h_0/h)^{n_{\rm c}}$; the loss of interstitial fluid pressurisation as proteoglycan is lost … plac[es] $n_{\rm c}$ toward the upper end of its range."

Fails part 3 (a proof in the smallest setting that shows the mechanism). The step from "a thinner layer has a smaller contact area" to "$A\propto h^{n_{\rm c}}$" is the whole content of the proposition, and it is assumed. The exponent then drives the entire §4 feedback loop, Lab C and K3 without ever being derived. The final clause is also wrong in direction: fluid pressurisation makes the layer *incompressible*, which is the $n_{\rm c}=1$ end, so losing it moves the exponent *down* toward $\tfrac12$ while separately raising the fraction of $p_{\rm peak}$ the solid matrix carries.

Replacement (the full `.proof` div; both limits are elementary and bracket the stated range):

```html
<div class="proof">The exponent is not a fitted number; it is bracketed by two solvable limits of the same geometry. In both, a rigid sphere of radius $R$ (the femoral condyle) presses on an elastic layer of thickness $h$ bonded to rigid bone, indenting the surface by $w(r)=\delta_0-r^2/2R$ inside a contact circle of radius $a$, where $w(a)=0$ fixes $a^2=2R\delta_0$. Take $h\ll a$, so the layer deforms locally.</p>
<p><b>Limit 1: a compressible layer.</b> Each column of tissue acts as an independent spring of stiffness $H'/h$ per unit area, with $H'$ the layer's confined modulus, so $p(r)=(H'/h)\,w(r)$. The load is $P=\int_0^a p\,2\pi r\,\mathrm dr=\pi R H'\delta_0^2/h$, giving $\delta_0=\sqrt{Ph/(\pi RH')}$ and $p_{\rm peak}=(H'/h)\delta_0=\sqrt{PH'/(\pi Rh)}\propto h^{-1/2}$: the exponent is $n_{\rm c}=\tfrac12$.</p>
<p><b>Limit 2: an incompressible layer.</b> If the layer cannot change volume it must extrude sideways, and with both faces bonded the radial displacement has a parabolic profile through the thickness, so the outward flux per unit circumference is $Q=-(h^3/12G)\,\mathrm dp/\mathrm dr$ with $G$ the shear modulus. Volume conservation, $r^{-1}\mathrm d(rQ)/\mathrm dr=w$, integrates with $p(a)=0$ to $p(r)=\tfrac{3G}{8Rh^3}\,(3a^4-4a^2r^2+r^4)$, whence $P=\pi Ga^6/(2Rh^3)$ and $p_{\rm peak}=p(0)=9Ga^4/(8Rh^3)$. Eliminating $a$ gives $p_{\rm peak}\propto G^{1/3}R^{-1/3}P^{2/3}h^{-1}$: the exponent is $n_{\rm c}=1$. (The numerical prefactor is not reliable, because the thin-layer approximation fails within about $h$ of the contact edge; the power of $h$ is.)</p>
<p>So $n_{\rm c}\in[\tfrac12,1]$, and the two ends are physical states of the same tissue, not fitting choices. Healthy cartilage loaded faster than its drainage time is fluid-pressurised and nearly incompressible (Module 4), so it sits near $n_{\rm c}=1$; as proteoglycan is lost the fluid support decays and the layer behaves compressibly, moving the exponent toward $\tfrac12$ while, separately, shifting a larger fraction of $p_{\rm peak}$ onto the solid matrix. This module uses a single $n_{\rm c}=0.7$ across the range as an assumed working value; the bracket it sits in is what the two limits establish, and it matters: over a thinning from $2.0$ to $0.6\ \mathrm{mm}$ the stress rises by a factor $1.83$ at $n_{\rm c}=\tfrac12$ and $3.33$ at $n_{\rm c}=1$. Substituting $n_{\rm c}=0.7$: $p_{\rm peak}(1.2)=3(2/1.2)^{0.7}\approx4.3\ \mathrm{MPa}$, $p_{\rm peak}(0.6)=3(2/0.6)^{0.7}\approx7\ \mathrm{MPa}$. <span class="qed">&#8718;</span></div>
```

Verified: $(2/0.6)^{0.5}=1.83$, $(2/0.6)^{0.7}=2.32$, $(2/0.6)^{1.0}=3.33$; $p(1.2)=4.29$, $p(0.6)=6.97$ MPa.

### B5. Proposition 3.2 drops the weight's work over an 11 cm compression stroke

Location: `module14.html:102-106`.

Quoted (`:106`): "At impact the kinetic energy $\tfrac12 m_{\rm eff}v^2$ converts to spring energy $\tfrac12 k x_{\max}^2$ at maximum compression".

Fails part 4 (the rescue or the limit case): the proposition never says what it neglects or where the hypothesis binds. The mass does not stop at the spring's rest point; it descends a further $x_{\max}$ while the spring compresses, and gravity does work $m_{\rm eff}gx$ over that stroke. Computed with the module's own $m_{\rm eff}=35$ kg, $k=40$ kN/m, $h_{\rm f}=0.70$ m:

```
v=3.706 m/s; boxed x=11.0 cm F=4385 N; exact x=11.9 cm F=4742 N (+8.1%);
x/h_f=0.157; crit rho boxed 0.7915 exact 0.8230
```

So the neglected term is not small — the compression is $16\%$ of the fall height — and the error is $8.1\%$ in the unsafe direction, moving the critical density from $0.79$ to $0.82$. This is the same omission the editor phase already repaired in Module 2 §6 (its B3). Following that precedent the module keeps the boxed form as its working value and states the correction: the proposition statement gains "The boxed form is the leading-order result: it holds when the compression $x_{\max}=F_{\rm peak}/k$ is small against the fall height $h_{\rm f}$, and here it is not especially small ($x_{\max}=11.0\ \mathrm{cm}$, $x_{\max}/h_{\rm f}=0.16$)", and the proof gains a "What the boxed form drops" paragraph giving the exact balance $\tfrac12kx^2=\tfrac12m_{\rm eff}v^2+m_{\rm eff}gx$, its positive root $x=\big(m_{\rm eff}g+\sqrt{m_{\rm eff}^2g^2+k\,m_{\rm eff}v^2}\big)/k$, and the two numbers above.

### B6. "Two hundred years of headroom" is impossible in the module's own law

Location: `module14.html:84` and `:315` (C2).

Quoted (`:84`): "two extra reserve units at $r=0.01$ is two hundred years of headroom in the linear model, i.e. the crossing never comes within a lifespan."

Quoted (`:315`): "two extra units of starting reserve buy more than a century in the linear model, i.e. the crossing effectively never comes."

Factual error. Proposition 2.1 gives $a^\star-a_0=\frac1r(1-D/\tau_p)$, and $D/\tau_p>0$, so the crossing can never be pushed further than $1/r=100$ years past $a_0$ however strong the start. Going from a starting reserve $\tau_p/D=1$ to $3$ buys $\frac1r(1-\tfrac13)=66.7$ years. The figure of $200$ comes from extrapolating the local slope $\mathrm da^\star/\mathrm d(\tau_p/D)=1/[r(\tau_p/D)^2]$ at $\tau_p/D=1$, where it is $100$ yr per unit — but that slope falls as $(\tau_p/D)^{-2}$ and is $39.5$ at the module's reference $1.59$ and only $11.1$ at $3$.

Replacement for `:84` (from "buys years before the crossing"):

```html
buys years before the crossing, but only up to a hard ceiling. Since $a^\star-a_0=\frac1r(1-D/\tau_p)$ and $D/\tau_p\gt 0$, no starting reserve can push the crossing further than $1/r=100$ years past $a_0$; going from a starting reserve of $\tau_p/D=1$ to $3$ buys $\frac1r(1-\tfrac13)=66.7$ years, and the marginal return falls as $\mathrm{d}a^\star/\mathrm{d}(\tau_p/D)=1/[r(\tau_p/D)^2]$, which is $39.5$ years per reserve unit at the reference $\tau_p/D=1.59$ and only $11.1$ at $\tau_p/D=3$.
```

Replacement for C2 at `:315` (from "so the $1\%$/year drift"):

```html
so the $1\%$/year drift takes more years to reach it. The gain is bounded: $a^\star-a_0=\frac1r(1-D/\tau_p)$ can never exceed $1/r=100$ years, and raising the starting reserve from $1$ to $3$ buys $66.7$ of them, with the return per further unit falling as $1/[r(\tau_p/D)^2]$.
```

### B7. "Push the failure age back by a similar span" contradicts Lab A by a factor of two

Location: `module14.html:174` (§7) and `:343` (C9).

Quoted (`:174`): "about twelve weeks of progressive loading adds on the order of $20\%$ - enough to reverse two decades of the $1\%$/year sarcopenic drift and push the chair-failure age of Section 2 back out by a similar span."

Factual error against the module's own Lab A, whose figure and caption both say a $20\%$ stronger person ($\tau_p:175\to210$ N m) crosses at 88 instead of 77. Computed: $a^\star(175)=77.14$, $a^\star(210)=87.62$, a gain of $10.48$ years, not twenty. The confusion is worth naming, because it is instructive: cancelling twenty years of drift in $\tau_{\max}$ is not twenty years of function, because $a^\star$ depends on $D/\tau_p$, not on $\tau_{\max}$. Both passages were rewritten to say so and to quote $10.5$ years.

### B8. $\sigma$ means two different things, and so does $k$

Location: `module14.html:72` ($\sigma$ as specific tension), `:148-150`, `:477` ($\sigma$ as sensor noise); `:347` ($k$ as the mechanostat rate) against `:102-106` ($k$ as landing stiffness).

Quoted (`:72`): "times a specific tension, $F_{\max}=\sigma\,\mathrm{PCSA}$."

Quoted (`:347`): "The mechanostat rate $k$ differs enormously across tissues."

Fails the house rule that a symbol means one thing for the whole module. Both were resolved on the minority side, leaving the dominant usage untouched: §2's specific tension becomes $\sigma_{\rm m}$, glossed in place and explicitly distinguished from the sensor-noise $\sigma$ (which appears in a dozen prose places and two SVG `<text>` nodes and was left alone); C10's mechanostat rate becomes $k_{\rm ad}$, matching Proposition 7.1, with the collision against §3's landing stiffness named in the sentence.

### B9. Two different values of $J_{\rm eff}$ at age 70, and no stated age law

Location: `module14.html:428` (K9) against the Section 6 figure at `:154`; the parameters at `:266`.

Quoted (`:428`): "$0.40$ at $70$ (with $b=0.07\ \mathrm{m}$, $\Delta t=0.16\ \mathrm{s}$, $c\sigma=0.015\ \mathrm{m}$, giving $J_{\rm eff}=7.3$)".

Factual error. The Section 6 figure's four plotted points decode to $J_{\rm eff}=13.46,\ 9.64,\ 6.34,\ 3.50$ N s at ages $40,\ 55,\ 70,\ 85$ — that is, the figure interpolates all three parameters linearly in age, giving $6.34$ N s at 70, against K9's $7.3$. The module never states which age law it uses, so nothing in the text lets the reader tell which number is right.

Fixed on both sides. The linear-in-age law is now declared as an assumption in Lab D's parameter list — "All three drift linearly in age between $40$ and $85$ years; this is a modelling choice, not a measurement, and it is the law Fig. 7, Fig. 12 and K9 all use", with $q(a)=q_{40}+\frac{a-40}{45}(q_{85}-q_{40})$ — and §6 now quotes the intermediate values. K9 was rewritten on that law:

```
age 40: b=0.1000 m, dt=0.1200 s, c*sigma=0.0100 m
        J_eff = 13.46 N s, P(fall) = 0.19
age 55: b=0.0833 m, dt=0.1467 s, c*sigma=0.0133 m
        J_eff =  9.64 N s, P(fall) = 0.30
age 70: b=0.0667 m, dt=0.1733 s, c*sigma=0.0167 m
        J_eff =  6.34 N s, P(fall) = 0.45
age 85: b=0.0500 m, dt=0.2000 s, c*sigma=0.0200 m
        J_eff =  3.50 N s, P(fall) = 0.65
```

The mean perturbation impulse $\bar J=8$ N s is now labelled an assumption, and the solution adds the structural point the exponential form gives for free: since $P=e^{-J_{\rm eff}/\bar J}$, a fixed *additive* gain in $J_{\rm eff}$ multiplies the fall probability by a constant factor, so the same $3.5$ N s of strength training is worth the same proportional risk reduction at every age.

### B10. Lab C's runaway was clipped at the axis ceiling and drawn as a plateau

Location: `module14.html:261` (figure and caption), `:263` (interpretation).

Quoted (caption, `:261`): "a fully loaded joint's peak stress climbs into a runaway".

The polyline decodes to a curve that rises to the axis top and then runs flat: the y-axis ended at $9.0$ MPa, the model crosses $9.0$ MPa at year 43, and the generator clamped $h$ at $0.05$ mm ($p=39.7$ MPa), so from year 43 to year 60 the drawn curve is a horizontal line at the ceiling. A reader sees a stress that rises and then settles — the opposite of the caption, and the opposite of the physics. This is the Module 2 B4 class (a figure that contradicts its own caption), and it passed every gate.

Regenerated: the y-axis now runs to $12$ MPa, the integration stops at $h=0.30$ mm (taken as spent) rather than clamping, and the curve ends there with a marked point. Computed: the $L=1$ curve climbs from $3.0$ to $11.32$ MPa and reaches $0.30$ mm at $t=44.5$ yr. The caption and the §9 interpretation were rewritten to those numbers and the legend relabelled $L=1$ / $L=0$.

### B11. About twenty bare numbers, against an eight-row parameter table

Location: `module14.html:483-491` (parameter table), `:469-478` (notation table).

The domain brief's rule is that every number is derived, a table parameter with symbol and unit, or a labelled assumption. Missing from the table entirely: $m_{\rm eff}=35$ kg, $k=40$ kN/m, $h_{\rm f}=0.70$ m, $\omega_0=3.1$ rad s⁻¹ (and the $\ell$ it implies), $m=70$ kg, $b=0.10\to0.05$ m, $\Delta t=0.12\to0.20$ s, $c\sigma=0.010\to0.020$ m, $p_0=3$ MPa, $h_0=2$ mm, $\kappa=\beta=0.010$, the osteoporotic $2.5$ kN, $\bar J=8$ N s, the $1\%$/week idle loss, the task demands $100$ and $150$ N m, and $k_{\rm ad}$. Missing from the notation table: $c$, $\sigma_{\rm m}$, $m$, $g$, $\ell$, $L$, $\kappa$, $\beta$, $L^\star$, $h^\star$, $C_{\rm m}$, $C_{\rm b}$, $\bar J$, $f$, and $J$ as distinct from $J_{\rm eff}$.

Nine parameter rows and three notation rows were added, each carrying the symbol, the unit, and its class — derived, a parameter, or assumed. The $\omega_0$ row states the $\ell=1.02$ m it implies; the fall row marks $m_{\rm eff}$, $k$ and $h_{\rm f}$ as assumed; the cartilage row marks $\kappa$ and $\beta$ as assumed and says why ("chosen for a readable decade-scale plot"); the $k_{\rm ad}$ row says it was set so that forty years at $r=0.01$ gives the tabulated $25\%$ bone loss; the impact row now carries both $4385$ N and the $4742$ N of B5.

### B12. The module never places its models on the level ladder

Location: `module14.html:56-68` (§1).

Fails the house rule the domain brief states ("Each module states which level its models sit on"), which Modules 1 and 2 both meet in one sentence. A paragraph was added at the end of §1, in the same shape:

```html
<p><b>Where these models sit.</b> Every model in this module is <b>Level 0</b> of the course's level ladder: a scalar capacity compared with a scalar demand, with no equation of motion solved here. The demands come ready-made from Level 1 statics (the chair and stair torques of Module 13) and the impact of <a class="secref" href="#osteoporosis">Section 3</a> is an energy balance, not an impact simulation. <a class="secref" href="#sensori">Sections 5</a> and <a class="secref" href="#fallrisk">6</a> quote two Level-2 results from Module 10 - the linearised inverted pendulum's growth rate $\omega_0=\sqrt{g/\ell}$ and its critical impulse - and use them as fixed capacities rather than re-deriving them. <a class="secref" href="#adaptation">Sections 7</a> and <a class="secref" href="#synthesis">8</a> are a scalar <b>Level 10</b>: one mechanobiological state variable per tissue, coupled through load. Nothing here is dynamic, and no result of this module may be read as one.</p>
```

### B13. $c$ and $\sigma$ are never defined precisely, and Proposition 3.1's box uses a symbol its statement does not define

Location: `module14.html:95` (the box), `:148-150` and `:477` ($c$, $\sigma$).

Quoted (`:95`): "$$\boxed{\;\frac{\Delta S}{S}\approx n\,\frac{\Delta\rho}{\rho}=2\,\frac{\Delta\rho}{\rho}.\;}$$" — the statement one line above defines $n_{\rm b}$, not $n$. Corrected to $n_{\rm b}$.

Quoted (`:150`): "$c$ a sway-to-margin sensitivity that converts the sway amplitude $\sigma$ into consumed margin." Fails part 2 (every term defined): "sway amplitude" is not a defined quantity (peak? standard deviation?), neither $c$ nor $\sigma$ is ever given a value, and only the product $c\sigma$ is ever used or tabulated. The Appendix row now reads "root-mean-square sway amplitude and the dimensionless sway-to-margin sensitivity that converts it to consumed margin (only the product $c\sigma$ is ever used)", and the parameter table carries $c\sigma$ with its unit and its age law.

### B14. "The delay has the sharpest per-unit leverage" is a unit-dependent claim the model contradicts

Location: `module14.html:158` (§6), `:293` (Lab D), `:331` (C6), `:408` (K4); the caption at `:140`.

Quoted (`:158`): "so per millisecond shaved its sensitivity is the sharpest".

Quoted (`:331`): "Reaction time therefore has the sharpest per-unit leverage on fall risk."

Fails part 1 (a precise statement). "Per millisecond" and "per millimetre" cannot be ranked against each other; the comparison is only meaningful in dimensionless terms, and there the claim inverts. Computed elasticities at the young operating point: $\partial\ln J_{\rm eff}/\partial\ln b=b/(b-c\sigma)=+1.11$, $\partial\ln J_{\rm eff}/\partial\ln\Delta t=-\omega_0\Delta t=-0.37$, $-c\sigma/(b-c\sigma)=-0.11$. The margin leads on sensitivity as well as on drift size, and the delay would have to reach $0.38$ s (a $3.2$-fold slowing) to cost as much as halving the margin does.

All four passages were rewritten to state the delay's real and correct distinction — its loss is multiplicative, $\partial J_{\rm eff}/\partial\Delta t=-\omega_0J_{\rm eff}$, so it is a fixed fractional penalty that never saturates as the envelope shrinks — and to rank the levers by elasticity. §6's non sequitur in the same sentence, "Since $m\omega_0 b$ shows that leg strength sizes both the margin and the corrective step" (there is no strength term in $m\omega_0b$; $m$ is body mass), was replaced with the actual reason: $b$ is the base of support plus the step the leg can place in the time available, and Module 10 sets that step by the hip and ankle impulse the muscles can generate.

### B15. Eight of the nine in-prose figure references point to the wrong figure, and one figure is never referenced

Location: `module14.html:64, 84, 110, 126, 142, 156, 174, 182`; the unreferenced figure at `:48`.

Quoted (`:64`): "Three reserves recur, one per tissue system (Fig. 2)" — the figure that follows at `:66` is Fig. 3.

Fails the structural rule that figures are referenced from the prose. The stylesheet numbers figures with a CSS counter, `figure{ counter-increment:fig }` with `figcaption::before{ content:"Fig. " counter(fig) ". " }`, so **every** `<figure>` element increments it. §0 carries two figures — the anatomy map at `:44` and the parameter-drift panel at `:48` — but only the first is referenced ("a short list does most of the work (Fig. 1)", `:42`). Every reference from §1 onward is therefore one low: what the prose calls Fig. 2 renders as Fig. 3, and so on through "(Fig. 9)" at `:182`, which renders as Fig. 10.

Confirmed by counting `<figure` openings against `<figcaption>` text in both the pristine and the edited file: the captioned figures are Fig. 1 (anatomy map) through Fig. 14 (Lab D), with the parameter-drift figure at Fig. 2 and the §1 margin framework at Fig. 3.

Fixed by adding the missing reference — "(Fig. 2)" appended to §0's "Aging is the crossing of thresholds by drifting parameters" at `:46`, which is exactly what that figure shows — and renumbering the other eight upward by one. My own new cross-reference in B9a was wrong for the same reason and was corrected from "Fig. 7, Fig. 12 and K9" to "Fig. 8 and K9" (Lab D's Fig. 14 is a bar chart of one-at-a-time sensitivities and does not use the age law at all).

Not fixed, and noted rather than churned: the four lab figures (Fig. 11 to Fig. 14) carry no `(Fig. N)` reference in the prose. Each sits inside its own lab subsection with its Interpretation paragraph immediately below, so the association is unambiguous; adding four references would be churn for no gain, but a later pass may want them for consistency.

## 3. Style and clarity edits

| At | Quoted | Rewritten to |
|---|---|---|
| `:110` | "cuts the peak force by $\sqrt2\approx30\%$" | "cuts the peak force by the factor $1/\sqrt2$, a $29\%$ reduction" — a factor is not a percentage; $1-1/\sqrt2=0.293$ |
| `:389` | "cuts the force by $\sqrt2\approx30\%$." | same correction (D10) |
| `:233`, `:235`, `:381`, `:400` | critical density "$\approx0.66$" | $0.67$ — computed $\sqrt{3101/7000}=0.6655$ |
| `:211` | "so early strength is enormously protective." | "so a reserve unit gained early is worth about four decades of drift at the reference operating point." (hype replaced with the computed $39.5$ yr/unit) |
| `:162` | "The module would be relentlessly pessimistic but for one fact that has recurred as a promise:" | "Every section so far has described a one-way loss. One fact reverses the direction:" |
| `:174` | "The numbers make the promise concrete and, in the muscle, striking (Fig. 8)." | "…and the muscle is the clearest case (Fig. 8)." |
| `:182` | "drives the grim one-year mortality." | "drives the one-year mortality that follows it." |
| `:339` | "carries such grim downstream mortality." | "…is far higher than the fracture alone would explain." |
| `:146` | "a fall-risk model whose sensitivity to each parameter is the whole point." | "…is what makes it actionable." |
| `:263` | "locate the critical $L^\star$ … (Problem K3 does exactly this)." | "…K3 does this and finds $L^\star=0.211$, well below the $L=1$ drawn here." |

## 4. Structural notes

- **The problem set is now the strongest part of the module, and it was the weakest.** Ten runnable blocks turn thirty asserted numbers into forty printed ones. The four deepened problems (K2, K3, K4, K6) each now require an inverse solve, a bifurcation, a sensitivity comparison or a duty-cycle integration; K1, K5, K7, K8, K9, K10 already required a sweep or a simulation and only needed the code.
- **Section 8 was the module's thesis section and carried no mathematics.** It now carries one proposition. The other two couplings (slowness feeding inactivity, the fall as pivot) are still qualitative, and the new paragraph says so explicitly rather than leaving the reader to guess which claims the module can compute.
- **The coincidence at age 77 is worth a second look by the author.** The coupled model of Proposition 8.1 puts the bone fracture-density crossing at age 77, and §2 puts the chair-rise failure at 77. This falls out of two independently chosen parameters ($r=0.01$ and the fitted $k_{\rm ad}=0.03125$) and is not a prediction; the K5 solution says only that both are driven by the one muscle drift. If the author would rather not invite the reading, retuning $k_{\rm ad}$ moves it.
- **K2 quotes three decimals where the rest of the module quotes two.** Its code prints `critical rho/rho0 = 0.791` and `0.666`, and its prose now matches its own stdout, while Lab B, D8 and the captions round to $0.79$ and $0.67$. Same numbers, two precisions; harmless, but a later pass may want one convention.
- **Six figures carry more than 20% wasted margin and five draw a head with no limb** (`check_frame`, `check_bodyprop` advisories). Both were already advisory on the pristine file and neither was touched; the "floating bust" flags look like anatomy fragments (a femur head, a pelvis) rather than detached heads, but they should be eyeballed in the anatomy sweep, not here.
- **The four lab code blocks end in `plt.show()`**, which blocks when a reader runs them headless. Not a defect — it is the house pattern across the course — but it is why the extraction step needs `MPLBACKEND=Agg`.

## 5. What already works

- **Propositions 2.1, 3.1, 3.2, 5.1, 6.1 and 7.1 are all proved, all short, and all correct.** Proposition 5.1's delay-erosion argument in particular is a model of the standard: it states the capturable bound, propagates $\xi_0e^{\omega_0\Delta t}$ through the lag, inverts the inequality, and lands on $e^{-\omega_0\Delta t}$ with the $0.78$ worked out. Nothing in it needed changing.
- **The four labs are the only part of the file whose numbers were reproducible before this pass, and all four reproduce exactly.** Lab A prints 77 and 88; Lab B prints 4385 N and 0.79; Lab C prints 3.0/4.3/7.0 MPa; Lab D prints 13.5, 3.5, and the 75/30/15 percent shares. Every one matches its prose.
- **The reserve framework of §1 is the right organising idea and is used consistently.** Every later section is $C/D$ for a named capacity and a named demand, and the "abrupt failure from smooth drift" argument is exactly correct and exactly explained.
- **Pillar 1 holds throughout.** "Greater trochanter (the bony prominence of the hip)", "femoral neck (the narrow bridge of bone between the ball and the shaft)", "proteoglycan (the water-binding matrix molecule that pressurises cartilage)" — every anatomical term is glossed in the sentence that introduces it.
- **The repayment ledger and the captures/misses table are honest.** The limitations table names the linear-drift approximation, the lumped spring, and the single-rate mechanostat as approximations rather than defending them, and it points each at the module that repays it.

## 6. Changes applied

Applied to `edited/module14.html` by `m14/apply.py` (63 anchored replacements, each asserted unique; re-runnable from a pristine copy). Figure bodies from `m14/gen3.py` → `figs.json`; code blocks from `m14/kcode/*.py`.

| tag | line (original) | what changed | how verified |
|---|---|---|---|
| B12 | 68 | Added the level-ladder paragraph to §1: Level 0 scalar reserves on Level 1 static demands, two Level-2 results quoted from Module 10, §7–§8 a scalar Level 10 | Phrasing matched to `module01.html:135` and `module02.html:158`; `check_links` 0 broken |
| B8 | 72 | §2's specific tension renamed $\sigma\to\sigma_{\rm m}$ and glossed, with the collision against §5's sensor-noise $\sigma$ named in the sentence | Grepped: $\sigma$ as specific tension occurred once, sensor-noise $\sigma$ in 12 prose places and 2 SVG `<text>` nodes; the minority side was renamed |
| B6a | 84 | "two extra reserve units … is two hundred years of headroom" replaced with the ceiling $1/r=100$ yr, the $66.7$ yr gain from reserve 1→3, and the falling marginal return ($39.5$ yr/unit at $\tau_p/D=1.59$, $11.1$ at $3$) | `gen.py`: `a*-a0 at a starting reserve of 1 / 2 / 3 = 0 / 50 / 66.7 yr; supremum 100 yr`; `d a*/d(tau_p/D) at 1.591 is 39.5` |
| B6b | 315 | C2's "buy more than a century" replaced with the same bounded statement | same run |
| B7a | 174 | §7's "push the chair-failure age back out by a similar span" replaced with the computed $77.1\to87.6$, a $10.5$-year gain, and the reason ($a^\star$ depends on $D/\tau_p$, not $\tau_{\max}$) | `gen.py`: `a*(175)=77.14  a*(210)=87.62  delta=10.48 yr`; agrees with Lab A's own figure |
| B7b | 343 | C9's "pushing the chair-failure age back by a similar span" given the same correction | same run |
| B13a | 95 | Proposition 3.1's box: bare $n$ → $n_{\rm b}$, matching the statement one line above | Read against `:94`; `checktex` 0 issues |
| B13b | 347 | C10's "mechanostat rate $k$" → $k_{\rm ad}$, with the collision against §3's landing stiffness $k$ named | Grepped both usages; matches Proposition 7.1 |
| B5a | 104 | Proposition 3.2 statement gains its validity condition: the boxed form needs $x_{\max}\ll h_{\rm f}$, and here $x_{\max}=11.0$ cm, $x_{\max}/h_{\rm f}=0.16$ | `gen.py`: `boxed x=11.0 cm F=4385 N ... x/h_f=0.157` |
| B5b | 106 | Proof gains "What the boxed form drops": the exact balance $\tfrac12kx^2=\tfrac12mv^2+mgx$, its root, $x=11.9$ cm, $F=4742$ N ($+8.1\%$), and the critical density moving $0.79\to0.82$ | `gen.py`: `exact x=11.9 cm F=4742 N (+8.1%) ... crit rho boxed 0.7915 exact 0.8230` |
| B4 | 122 | Proposition 4.1's circular proof replaced by two derivations that bracket the exponent: Winkler compressible thin layer gives $n_{\rm c}=\tfrac12$, bonded incompressible thin layer gives $n_{\rm c}=1$; the fluid-loss direction corrected (it moves $n_{\rm c}$ down, not up) | Both derivations carried out symbolically in the report; the stress ratios $1.83/2.32/3.33$ over $2.0\to0.6$ mm printed by `gen.py` |
| B14a | 158 | §6's "per millisecond … the sharpest" replaced with the elasticities $+1.11/-0.37/-0.11$; the $m\omega_0b$ non sequitur about leg strength replaced with the real reason $b$ is trainable | `gen2.py`: `elasticities: b +1.111  dt -0.372  cs -0.111` |
| B14b | 331 | C6 given the same correction: the delay's distinction is that its fractional loss never saturates, not that it outranks strength | same run |
| B14c | 293 | Lab D's Sensitivity paragraph ranked by elasticity | same run |
| B9a | 266 | Lab D's parameters gain the **Assumed age law**: all three drift linearly in age between 40 and 85, $q(a)=q_{40}+\frac{a-40}{45}(q_{85}-q_{40})$, named as the law Fig. 7, Fig. 12 and K9 all use | Decoded the Section 6 figure's four polyline points and matched them to the linear law: 13.46 / 9.64 / 6.34 / 3.50 N s at 40/55/70/85 |
| B9b | 156 | §6 now quotes $13.46\to3.50$ N s with the intermediate $9.64$ and $6.34$, and labels the age law an assumption | same decode + `gen.py` |
| S3a | 110 | "$\sqrt2\approx30\%$" → "the factor $1/\sqrt2$, a $29\%$ reduction" | $1-1/\sqrt2=0.2929$ (`gen.py`) |
| S3b | 389 | same correction in D10 | same |
| S2a–S2d | 233, 235, 381, 400 | Critical density with a hip protector $0.66\to0.67$ (four places) | `kcode/k02.py`: `k=20 kN/m: F=3101 N, critical rho/rho0 = 0.666` |
| S4a | 211 | "so early strength is enormously protective" → the computed "about four decades of drift" per reserve unit | `gen.py`: 39.5 yr per unit at $\tau_p/D=1.59$ |
| S4b | 162 | "would be relentlessly pessimistic but for" → "Every section so far has described a one-way loss. One fact reverses the direction:" | Read aloud |
| S4c | 174 | "in the muscle, striking" → "the muscle is the clearest case" | Read aloud |
| S4d | 182 | "the grim one-year mortality" → "the one-year mortality that follows it" | Read aloud |
| S4e | 339 | "such grim downstream mortality" → "far higher than the fracture alone would explain" | Read aloud |
| S4f | 146 | "is the whole point" → "is what makes it actionable" | Read aloud |
| S5 | 263 | Lab C's Extension pointer now states K3's answer, $L^\star=0.211$, instead of promising it | `kcode/k03.py` prints `saddle-node at L* = 0.211` |
| B10 | 261 | Lab C figure regenerated: y-axis $0\to12$ MPa (was $0\to9$), integration stopped at $h=0.30$ mm instead of clamping at $0.05$, curve ends at a marked point, legend relabelled $L=1$ / $L=0$, caption rewritten to $3.0\to11.32$ MPa and $44.5$ yr | `gen3.py`; the old polyline decoded to a flat line at the ceiling from $t=43.0$ yr (`gen.py`: `L=1.00 crosses 9.0 MPa at t=43.0 yr`); rendered and inspected in `m14/prev.png` |
| B10b | 263 | Lab C interpretation rewritten to the same numbers, with $L$ restored to the ODE | `kcode/k03.py` |
| B3a | 182 | §8 gains Proposition 8.1 ($C_{\rm b}=1-\tfrac12k_{\rm ad}rt^2$) with a full proof, plus a sentence saying the other two couplings are not computed | Derived in place; `check_proofs` reports 0 asserted propositions |
| B3b | 410 | K5 statement rewritten to ask for the three-rate sweep ($r=0.01$, $0.005$, $0$) with $k_{\rm ad}=0.03125$ yr⁻¹ | — |
| B3c | 412 | K5 solution rewritten: muscle $0.600$, bone $0.750$, bone strength $0.562$ at 40 yr; fracture density reached at year 37 (age 77); halving $r$ halves the bone deficit exactly; $r=0$ removes it; limits stated | `kcode/k05.py` output quoted verbatim in the block |
| B3d | 411 | K5 figure regenerated from Proposition 8.1: linear muscle, quadratic bone, dashed fracture-density line at $0.79$ with the crossing marked at $36.5$ yr | `gen3.py`; the old polylines decoded to muscle linear at $0.31\%$/yr (not the module's $1\%$) and bone flat-then-linear, which no mechanostat produces; rendered in `m14/prev5.png` |
| B2a | 402 | K3 statement rewritten to ask for the bifurcation ($L_{\rm eq}(h)$, $L^\star$, $h^\star$) then the confirming integrations | — |
| B2b | 404 | K3 solution replaced: $L^\star=0.211$ at $h^\star=0.82$ mm, two branches below it, runaway above; $L=0.10$ and $0.20$ maintained at $1.669$ and $1.187$ mm; $L=0.40$, $0.60$, $1.00$ spent at $153.5$, $84.0$, $44.5$ yr | `kcode/k03.py` output quoted verbatim; independently confirmed by the 400 001-point grid in `gen.py` |
| B2c | 403 | K3 figure replaced by the bifurcation diagram $L_{\rm eq}(h)$ with the saddle-node marked; the old figure plotted $L\!\cdot\!p$ on an axis labelled "peak stress (MPa)" and drew a runaway transient as "stable" | `gen3.py`; old axis calibration recovered from the tick coordinates ($t=0$ read $1.2$ MPa where $p_0=3.0$); rendered in `m14/prev.png` |
| B1_K2 | 400 | K2 deepened to the pad-stiffness inverse across a fall-height sweep, plus code | `kcode/k02.py` run; `13.2`, `41.8`, `18.5/13.2/10.3` kN/m all printed |
| B1_K4 | 408 | K4 deepened to the elasticity ranking and the $0.38$ s flip point, plus code; "$12.0$" corrected to the printed $11.97$ | `kcode/k04.py` run |
| B1_K6 | 416 | K6 deepened to the training duty cycle ($f=0.40$ to hold, $0.55$ for $+20\%$ in a year, $0.71$ in six months), the $1\%$/week idle rate labelled an assumption and an upper bound, plus code | `kcode/k06.py` run |
| B1_K9a, B1_K9b | 428 | K9's age-70 value corrected $7.3\to6.34$ N s and $P$ $0.40\to0.45$; young $P$ $0.18\to0.19$; $\bar J=8$ N s labelled an assumption; the constant-factor risk reduction added; plus code | `kcode/k09.py` run; matches the Section 6 figure's own points |
| B1_K1 | 396 | Code block added (numbers already correct) | `kcode/k01.py` run: `181.8 / 200.0 / 272.7 N m`, ages `83 / 77 / 54` |
| B1_K3 | 404 | Code block added to the rewritten K3 | `kcode/k03.py` run |
| B1_K5 | 412 | Code block added to the rewritten K5 | `kcode/k05.py` run |
| B1_K7 | 420 | Code block added | `kcode/k07.py` run: $\rho_{\rm c}=0.640/0.728/0.791/0.843/0.886$ |
| B1_K8 | 424 | Code block added | `kcode/k08.py` run: ages 54 / 77 / 83, gaps 23 and 6 yr |
| B1_K10 | 432 | Code block added, covering all seven intervention combinations, not just the four the prose named | `kcode/k10.py` run: `3.50` aged; `7.00 / 4.22 / 4.67` singly; `8.44 / 8.17 / 5.62` in pairs; `9.84` all three |
| B11a | 477 | Notation row for $J$, $J_{\rm eff}$, $b$, $\sigma$, $c$ rewritten: $\sigma$ defined as the root-mean-square sway amplitude, $c$ as dimensionless, with the note that only $c\sigma$ is used | Read against §6's usage |
| B11b | 478 | Three notation rows added: $\sigma_{\rm m}$, $m$, $g$, $\ell$; $L$, $\kappa$, $\beta$, $L^\star$, $h^\star$; $C_{\rm m}$, $C_{\rm b}$, $\bar J$, $f$ | Cross-checked against every symbol in the applied text |
| B11c | 488 | Seven parameter rows added in place of the single "Sideways-fall impact" row: the fall triple ($35$ kg, $40$ kN/m, $0.70$ m, assumed); $F_{\rm peak}=4385$ N derived, with $4742$ N noted; osteoporotic $2.5$ kN derived as $S_0\times0.6^2$; cartilage $p_0$, $h_0$, $\kappa$, $\beta$ (assumed); $L^\star$, $h^\star$ derived; $\omega_0=3.1$ rad s⁻¹ with $\ell=1.02$ m and $m=70$ kg; $b$, $\Delta t$, $c\sigma$ with their age law; $\bar J=8$ N s assumed | Each value traced to the code block or derivation that produces it; $7000\times0.36=2520$ N and $\ell=9.81/3.1^2=1.021$ m checked by hand |
| B11d | 491 | Four more parameter rows: build and idle rates with the immobilisation caveat; $k_{\rm ad}=0.03125$ yr⁻¹ with how it was set; the task demands $100/110/150$ N m; the model's forty-year muscle and bone drift ($40\%$, $25\%$) | `kcode/k05.py`, `kcode/k06.py`, `kcode/k08.py` |
| B15a | 46 | Added the missing reference to the §0 parameter-drift figure: "Aging is the crossing of thresholds by drifting parameters (Fig. 2)." | Counted `<figure` openings against `<figcaption>` text: the captioned figures are Fig. 1–14, and Fig. 2 had no prose reference |
| B15b–B15i | 64, 84, 110, 126, 142, 156, 174, 182 | Renumbered the eight remaining in-prose references upward by one: Fig. 2→3, 3→4, 4→5, 5→6, 6→7, 7→8, 8→9, 9→10 | Same count, cross-checked after the apply: the ten `(Fig. N)` references now read 1…10 in file order and match the counter |
| B15j | (new B9a text) | My own new cross-reference corrected from "Fig. 7, Fig. 12 and K9" to "Fig. 8 and K9" — Lab D's Fig. 14 is a bar chart and does not use the age law | Same count; the §6 J_eff-vs-age figure is Fig. 8 |

### Gate results

Baseline (pristine `edited/module14.html`) and after the apply, on all nine hard gates:

| gate | baseline | after |
|---|---|---|
| `checktex` | 540 segments, 0 issues | 851 segments, **0 issues** |
| `checklt` | 0 | **0** |
| `check_links` | 85 links, 0 broken, 0 unlinked | 109 links, **0 broken, 0 unlinked** |
| `check_svg` | 0 hard, 0 advisory | **0 hard, 0 advisory** |
| `check_code` | 4 blocks, 0 issues | 14 blocks, **0 issues** |
| `verify_dom` | 0 mjx-merror, 0 broken, 14 stray `$` (adv), 0 swallowed | **0 mjx-merror, 0 broken**, 14 stray `$` (adv), 0 swallowed |
| `check_overlap` | 0 | **0** |
| `check_frame` | 0 hard; 6 wasted-margin advisories | **0 hard**; same 6 advisories |
| `check_bodyprop` | 0 hard; 5 floating-bust advisories | **0 hard**; same 5 advisories |

All nine exit 0. Advisories: `check_prose` 0, `check_proofs` 0 asserted propositions, `check_probfig` 30/30 real figures — all unchanged from baseline. The three regenerated figures were rendered with `shoot.py` and inspected (`m14/prev.png`, `m14/prev5.png`).

The first run of the apply was not clean and the record should say so: it left two `check_overlap` hits (the K3 "below: maintained" legend crossing the $L_{\rm eq}$ curve, and the K5 "fracture density 0.79" label crossing the bone curve) and one `check_svg` advisory (the K3 polyline at 130 points, over the 120 threshold). Both labels were repositioned data-aware from the boxes the gate printed and the K3 curve decimated to 100 points; the numbers above are the second run. `check_code` also failed on the first attempt, because the `# ->` output comments ran past 79 columns; the code helper in `apply.py` now wraps them with a hanging indent and asserts the 79-column limit before emitting.

**Technique worth reusing.** Three of the defects above — K3's figure plotting $L\!\cdot\!p$ on an axis labelled "peak stress", K5's muscle drifting at $0.31\%$/yr instead of the module's $1\%$, and Lab C's runaway clamped flat at the axis ceiling — were found by decoding the `<polyline>` point strings back into data. Calibrate the axis from the tick `<text>` coordinates, invert the mapping, and compare the recovered series against the model the caption claims. All three passed every one of the nine gates, and none is visible in a casual look at the rendered figure.
