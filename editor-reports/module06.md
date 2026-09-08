# Editor report — `module06.html`

**Tendons, Ligaments, Fascia, and Elastic Energy Storage** (1039 lines).
Pass run against `EDITOR_DOMAIN.md`, the five-part standard in
`~/.claude/skills/science-editor/SKILL.md`, and the house conventions in
`CLAUDE.md`. Every number quoted below as "computed" was printed by a script
run during this pass; the scripts are listed in §6.

**Gate baseline** (pristine copy, before any edit):

| gate | baseline |
|---|---|
| `checktex` | 842 math segments, **0** issues |
| `checklt` | **0** |
| `check_links` | 217 links, **0** broken, **0** unlinked §refs |
| `check_svg` | **0** hard, **0** advisory |
| `check_code` | 3 blocks, **0** issues |
| `verify_dom` | **0** mjx-merror, 6 stray `$` (advisory), 0 broken, 0 swallowed prose |
| `check_overlap` | **0** |
| `check_frame` | **0** clipped (1 wasted-margin advisory: the §0 Achilles/ACL figure) |
| `check_bodyprop` | **0** hard (1 advisory: the MTU schematic head has no limbs) |

Advisories at baseline: `check_prose` 1 flag (`:828`), `check_proofs` 0,
`check_probfig` 0.

---

## 1. Verdict

**Yes, after revision.** The argument of this module is sound and, in places,
better than sound. Every proposition carries a real proof, and every proof I
followed with a pen checks out: Propositions 1 through 3 build the J-curve from
a recruitment assumption and integrate it correctly; Proposition 4 gets the
rigid-tendon limit exactly right; Propositions 5, 6 and 7 derive Maxwell,
Kelvin-Voigt and the standard linear solid from one clearly stated sharing rule,
and §6's long digression on *why* series shares stress and parallel shares strain
is the single best-taught passage in the module. Propositions 8 and 9 do the loop
integral and the complex modulus honestly. Proposition 10, the instant centre at
the cruciate crossing, is a small gem: the velocity argument is exactly the
smallest setting in which the mechanism is visible. The known §6 rigor-parity
defect recorded in `CLAUDE.md` — results 6.1 and 6.2 asserted beside a proved
6.3 — **has been fixed**, and the §0 shell-mangled caption is also clean; `$W$`
and `$F_{\text{GRF}}$` render as prose.

The damage is in the numbers, and it is of one kind. This module tells the
reader, twice, that its computational answers are "Python-verified" — and then
ships no code with any of the thirty problems. All three §9 labs do run, and I
ran them; Lab 1 and Lab 3 print exactly what the prose claims. But of the ten
computational problems, five (K3, K4, K6, K8, K9) quote numbers that **no stated
parameter set can reproduce**, because the parameters are never stated. That is
the most serious class of defect the domain brief names: a plausible figure in
the gap. Two of the five are worse than unreproducible — K4's off-resonance pair
(0.67, 0.08) is asymmetric while its own formula depends only on
$|k-M\omega^2|$, and K8's ligament resilience of 20% contradicts the table in §7
of the same module, which puts a ligament at 0.80 to 0.90.

Three internal contradictions cut deeper than arithmetic. **(a)** §6 and §7 say
a tendon's relaxation time is "seconds to minutes", which is what puts gait on
the low-loss side of the loss peak and is the module's headline explanation of
why a tendon is a good spring; the Appendix and every lab use 0.05 s, which puts
the peak at 2.25 Hz — running cadence — as K7 itself computes. **(b)** Lab 2
calls a 17 kN/m spring "the tendon" and reports that it banks 197 J; at the
computed peak force that spring stretches 152 mm, which on §2's own 250 mm
Achilles is 61% strain, seven times past rupture, and 197 J is six times §3's
computed 32 J. **(c)** The foot arch stores 17 J in §0 and §8 and 5.4 J in K10,
a factor of three, unreconciled. A graduate reader who checks the module against
itself will hit all three.

Two smaller structural gaps: the module never places its models on the level
ladder, which `EDITOR_DOMAIN.md` requires of every module; and the 80 kg body
mass that Lab 2, K4 and K10 all depend on appears nowhere in the text, while the
course's reference human is 70 kg.

None of this touches the derivations. Fix the numbers, ship the code, and this
is a module a graduate reader can learn from.

---

## 2. Blocking defects

> **Four of the replacements written out below were corrected before they
> shipped** — K1's noise model, K4's half-power band, B15's ladder rungs, and
> the scope of S13. One more, B2b's Fig. 16 caption, was rewritten after
> reading the figure's own SVG. §6 “Corrections to this report” records each
> one. Where this section and §6 differ, §6 is what is in the file.

Ranked. Each gives `module06.html:LINE`, the verbatim text, the part of the
standard it fails, and the full replacement.

---

### B1 — Ten computational solutions claim Python verification and carry no Python

`module06.html:798` and `module06.html:898`

> `the computational answers are Python-verified`

> `Each answer below is Python-verified.`

**Fails part 5 (a tie to something concrete) and part 1 (a precise statement).**
The house convention (`CLAUDE.md`, `EDITOR_DOMAIN.md`) is that "K solutions carry
Python-verified numbers with code". Modules 3, 4 and 5 do. Module 6 has three
`<pre><code>` blocks in the whole file, all in §9; K1 through K10 have none. The
claim is therefore unbacked, and for K3, K4, K6, K8 and K9 it is unbackable,
because those solutions never state the parameters their numbers came from
(B10 through B13 below). I re-derived all ten during this pass; K2, K7 and K10
reproduce exactly, K1 and K5 are seed-dependent, and the other five do not
reproduce from anything the page says.

**Fix.** Change both sentences, then attach a runnable block to every K solution
(the replacements are given under B10 through B13 and in §5, and the code is in
`scratchpad/m06/k/k01.py` … `k10.py`; all ten pass `pycodestyle` and were run).

`:798` replacement:

```html
<p>Thirty problems in three strands &#8212; <b>conceptual</b> (C1&#8211;C10), <b>derivational</b> (D1&#8211;D10), and <b>computational</b> (K1&#8211;K10) &#8212; each with a worked solution; every computational solution ships the Python that prints its numbers. A <b>Probes</b> note names what each tests. The map below shows which section each problem draws on &#8212; and, read by row, that every section is exercised:</p>
```

`:898` replacement:

```html
<p class="small">These require genuine computation &#8212; a simulation, an optimisation, an inverse problem, a sensitivity sweep, or a regime comparison &#8212; not substitution into a boxed formula. Every boxed number below is printed by the code that follows its solution: copy the block, run it, and check.</p>
```

---

### B2 — The tendon's relaxation time contradicts itself, and the contradiction carries the module's headline claim

`module06.html:543` (and `:541`, `:494`)

> `A tendon's relaxation time $\tau_\sigma$ is of order seconds to minutes, while walking and running load it at a few hertz. The product $\omega\tau_\sigma$ is therefore <em>large</em>`

**Fails part 1 (a precise statement) and part 4 (the limit case).** The Appendix
(`:1004`) and every lab and K problem in the module use $\tau_\sigma = 0.05$ s.
At a 2.6 Hz cadence, $\omega\tau_\sigma = 16.34 \times 0.05 = 0.82$ — not large.
Worse, K7 computes the loss peak at $\omega^\ast = 14.13$ rad/s, i.e.
$f^\ast = 2.25$ Hz, which is running cadence. So the module's own parameters put
gait **on** the loss peak while its prose says gait sits far past it. Fig. 16's
caption shades the gait band as $\omega\tau_\sigma\gg1$, which is false for the
$\tau_\sigma$ the figure was drawn with. This is the module's central answer to
"why is a tendon a good spring", so it cannot stay ambiguous.

**Fix.** Say that a real tendon has a spectrum, that the labs use its fast end
because that is what settles inside a short simulation, and that the slow modes
are what carry the measured hysteresis and put gait on the low-loss side. The
Appendix already records the span $10^{-2}$ to $10^{3}$ s; the prose has to use it.

`:543` replacement:

```html
<p><b>Why this makes a tendon a good spring.</b> The loss peak sits at $\omega^\ast=1/\sqrt{\tau_\sigma\tau_\varepsilon}$, so where a tendon sits on Fig.&nbsp;16 depends on which relaxation mode dominates it. Real tendon has a spectrum, not one time constant: the Appendix records a span from $10^{-2}$ to $10^{3}\ \text{s}$. The fast end, $\tau_\sigma\approx0.05\ \text{s}$, is the mode the labs of <a class="secref" href="#labs">§9</a> use, because it settles inside a simulation that runs in a second; taken alone it would put $\omega^\ast\approx14\ \text{rad/s}$, or $2.25\ \text{Hz}$ (K7), squarely at running cadence. The modes that carry a tendon's measured dissipation are the slow ones, $\tau_\sigma$ of order seconds to minutes. With $\tau_\sigma\gtrsim1\ \text{s}$ and gait at a few hertz, $\omega\tau_\sigma\gtrsim10$, and the tissue responds almost elastically at its stiff instantaneous modulus $E_{\text{inst}}$ (the shaded band in Fig.&nbsp;16), losing little. The same tendon, held under a slow steady stretch, works those slow modes directly and creeps. A tendon is a low-loss spring in the regime it works in because its dominant loss peak is parked decades below the operating frequency, not because it has no loss peak.</p>
```

`:541` caption replacement:

```html
<figcaption><b>The loss factor is rate-dependent.</b> $\tan\delta(\omega)$ from Eq.&nbsp;(7.3): near zero when loading is far slower than the material clock (elastic at $E_R$) or far faster (elastic at $E_{\text{inst}}$), peaking at $\omega^\ast=1/\sqrt{\tau_\sigma\tau_\varepsilon}$ where loading rate matches relaxation rate. The curve is drawn with the fast lab mode $\tau_\sigma=0.05\ \text{s}$, whose own peak would fall inside the gait band (K7). A tendon's gait and running loading (shaded) sits far above the peak of the <em>slow</em> modes that dominate real tissue ($\omega\tau_\sigma\gg1$ for $\tau_\sigma$ of order seconds), on the fast, low-loss side, which is why it behaves as a good spring when loaded dynamically.</figcaption>
```

`:494` replacement (the clause in parentheses only):

```html
and $\tau_\sigma,\tau_\varepsilon$ set the crossover timescales (the fast lab mode used in <a class="secref" href="#labs">§9</a> is $\tau_\sigma=0.05\ \text{s}$; the slow modes that set a tendon's measured hysteresis run from seconds to minutes, Appendix)
```

---

### B3 — Lab 2 calls a whole-leg spring "the tendon" and reports an energy six times §3's

`module06.html:670` and `module06.html:714`

> `kT = 1.7e4  # leg (series-tendon) stiffness (N/m)`

> `the tendon stores $\approx197\ \text{J}$ over the bounce`

**Fails part 1 (a precise statement) and the domain brief's rule that a scenario
reused later must keep the same parameter values or say why it differs.** §2
computes the free Achilles at $k_{\text{lin}} = 4.16\times10^{5}$ N/m. Lab 2 uses
$1.7\times10^{4}$ N/m, 24 times softer, with no comment. Instrumenting the block
(scratchpad `lab2_check.py`) gives a peak ground reaction of 2591 N, so that
spring stretches **152.4 mm**; on §2's 250 mm Achilles that is **61% strain**,
against a rupture strain of 9%. The 197 J it banks is six times §3's computed
32 J for the same tendon and six times §0's quoted 35 J.

The stiffness is not wrong — 17 kN/m is a whole-leg SLIP spring, and K4's own
resonant optimum is 21.3 kN/m, the same scale. The *label* is wrong. Changing
$k_T$ would invalidate Fig. 22 and every printed number; relabelling costs
nothing and is what the physics supports.

**Fix.** Rename the element in the code comment, the lab intro and the figure
caption, and state the assumption.

`:670` (inside the code block; the surrounding block is replaced whole under B4):

```python
# a hop: body mass M on a leg = active muscle fibre (Hill) in series with
# an elastic leg spring. Assumed values; kT is a WHOLE-LEG series stiffness
# (Module 9 scale), not the 4.2e5 N/m free Achilles of section 2.
M, g = 80.0, 9.81  # body mass (kg), gravity
kT = 1.7e4  # leg (series) spring stiffness (N/m)
```

`:664` replacement:

```html
<p>This is the payoff simulation. Model a vertical hop as a body mass $M=80\ \text{kg}$ bouncing on a leg that is a <b>muscle&#8211;tendon unit</b> &#8212; the active Hill fibre of <a href="module05.html#hillmodel">Module 5</a> in series with an elastic spring &#8212; under gravity (<a class="secref" href="#see">§4</a>'s series-elastic model, now driven dynamically). One assumption needs naming before the numbers arrive: the series spring here is the <b>whole leg's</b>, $k_T=1.7\times10^{4}\ \text{N/m}$, not the free Achilles of <a class="secref" href="#spring">§2</a>, which is 24 times stiffer at $4.16\times10^{5}\ \text{N/m}$. That is deliberate. A hop compresses the leg by about $16\ \text{cm}$, and no single tendon stretches that far; the lumped leg spring rolls the Achilles together with the arch, the knee and hip tissues, and the compliance of the ground contact, which is the level Module&nbsp;9 works at. Its stored energy is therefore a whole-leg figure and should not be compared with the $32\ \text{J}$ the Achilles alone banks in <a class="secref" href="#energy">§3</a>. The body compresses the leg on landing, stretching the spring; because gravity holds the load high, the fibre stays near its isometric force and moves slowly while the spring stores the energy, then recoils to launch the body. The state equations are Newton's law for the body, $M\ddot s=Mg-F$, coupled to the fibre through the force&#8211;velocity inverse of Eq.&nbsp;(4.3).</p>
```

`:712` caption replacement:

```html
<figcaption><b>The catapult, in the dynamics.</b> Shortening speeds through a hop's stance. During <b>loading</b> (shaded) all three lengthen; at <b>push-off</b> the whole-unit $\dot L_{\text{MTU}}$ (dashed) and the leg-spring recoil (blue) spike together while the fibre (red) stays near zero &#8212; the spring recoils $3.3\times$ faster than the fibre shortens, discharging Module 5's speed-difference debt.</figcaption>
```

---

### B4 — Three of Lab 2's five headline numbers are never printed by the code the reader is told to run

`module06.html:714`

> `The peak ground reaction is <b>3.3&times; body weight</b> … the tendon stores $\approx197\ \text{J}$ … the muscle does only $\approx7\ \text{J}$ of work`

**Fails part 5 (a tie to something concrete).** The block at `:666` prints only
the speed amplification. The ground reaction, the stored energy and the muscle
work appear in the prose and nowhere in the code, so a reader who copies the
block cannot reproduce them. I instrumented the model and all three do check out
— 3.30 body weights, 197.50 J, 6.84 J, hence 96.7% elastic — so the fix is to
print them, not to change them. This is the same defect class as Module 3's B3.

**Fix.** Add the three quantities to the block and print them. The full
replacement block is in `scratchpad/m06/k/lab2.py`; the accumulators are

```python
    Fpk = max(Fpk, F)  # peak ground reaction
    Upk = max(Upk, 0.5*kT*max(xT, 0.0)**2)  # peak spring energy
    Wmus += F*vfib*dt  # muscle work = int F v_fibre dt
```

and the two new prints are

```python
print(f"peak ground reaction {Fpk/(M*g):.1f} body weights; spring banks "
      f"{Upk:.0f} J, muscle does {Wmus:.1f} J -> "
      f"{100*Upk/(Upk + Wmus):.0f}% elastic")
print(f"fibre shortens {1e3*(l0 - l):.0f} mm over stance, but at "
      f"{fib/rec:.2f} of the spring recoil speed")
```

Verified output:

```
peak tendon recoil 1.46 m/s  vs  peak fibre 0.44 m/s -> 3.3x amplification
peak ground reaction 3.3 body weights; spring banks 197 J, muscle does 6.8 J -> 97% elastic
fibre shortens 18 mm over stance, but at 0.30 of the spring recoil speed
```

---

### B5 — "The fibre stays near-isometric" is contradicted by the simulation that is supposed to prove it

`module06.html:714`

> `$\sim97\%$ of the push-off is elastic recoil, the muscle merely holding force`
> (and `:748`) `with the fibre near-isometric`

**Fails part 1 (a precise statement).** Isometric means constant length. The
fibre in Lab 2 shortens from 55.0 mm to 36.6 mm, that is **18.4 mm, 33.5% of
$\ell_0$**, over the stance; its length factor $f_L$ falls from 1.00 to 0.575 in
the process. What is near zero is its *velocity relative to the spring's*, 0.30
of the recoil speed at push-off. The claim as written is false and the
correction strengthens the point rather than weakening it.

**Fix.** `:714` replacement (this also lands B3, B4 and the numbers):

```html
<p>The block prints five numbers. The peak ground reaction is <b>3.3&times; body weight</b>; the leg spring recoils at <b>1.46&nbsp;m/s while the fibre shortens at only 0.44&nbsp;m/s</b>, a $3.3\times$ speed amplification (Fig.&nbsp;22, blue tracks the dashed whole-unit while red stays flat near zero); and over the bounce the spring banks $197\ \text{J}$ while the muscle does $6.8\ \text{J}$ of work, so $97\%$ of the push-off is elastic recoil and the muscle mostly holds force. Be exact about <em>near-isometric</em>, because the simulation is: the fibre is not still. It shortens $18\ \text{mm}$ over the stance, a third of its optimal length $\ell_0$, and its length factor $f_L$ falls from $1.00$ to $0.58$ on the way. What is near zero is its <em>velocity at push-off</em>, $0.30$ of the spring's recoil speed. That is the catapult of <a class="secref" href="#see">§4</a> emerging from the coupled dynamics, and it settles <a href="module05.html#hillmodel">Module 5</a>'s Assumption&nbsp;7.1 debt&nbsp;(b), the fibre&#8211;tendon speed difference, with a computed result rather than an argument.</p>
```

`:748` clause fix: `with the fibre near-isometric` becomes
`with the fibre shortening at a third of the spring's recoil speed`.

---

### B6 — The foot arch stores 17 J in §0 and §8 and 5.4 J in K10

`module06.html:109`, `module06.html:614`, `module06.html:938`

> `The <b>plantar fascia</b> and the ligaments of the foot arch add roughly another <b>17&nbsp;J</b>.`

> `contributing the $\sim17\ \text{J}$ per step noted in §0`

> `the arch stores $\boxed{\approx5.4\ \mathrm{J}}$ at peak load`

**Fails part 1 (a precise statement) and the evidence-grading scheme.** K10's
5.4 J I reproduce exactly (peak tie tension 1.47 kN, stretch 7.36 mm,
$U=\tfrac12Tx=5.41$ J). The 17 J is a bare literature figure with no derivation
and no Appendix row. They differ by 3.1 times, they are one section apart, and
neither acknowledges the other. `EDITOR_DOMAIN.md` forbids repairing a citation
from memory, so the fix is not to pick a winner: it is to label each number with
its class and say why they differ. The single-tie truss models one ligament; the
17 J is attributed to the whole arch.

**Fix.** `:109` replacement:

```html
<p>The bookkeeping is worth doing. In a moderate run the human <b>Achilles tendon</b> &#8212; the thick cord joining the calf muscles to the heel &#8212; stretches by a few percent and stores on the order of <b>35&nbsp;J of elastic energy per step</b>, returning about <b>90&#8211;93%</b> of it in the push-off. The <b>plantar fascia</b> and the ligaments of the foot arch add roughly another <b>17&nbsp;J</b>. That second figure is a literature value for the arch as a whole, every plantar ligament and the joint capsules together; it is quoted here unverified, and the single-tie truss model this module builds in <a class="secref" href="#ligaments">§8</a> accounts for about a third of it (K10), which is what a one-element model of a many-element structure should do. Together these passive springs supply a large share of the energy each stride would otherwise cost the muscles, which is why running is more economical than its jolting appearance suggests.</p>
```

`:614` final clause replacement:

```html
the arch is a second spring in the leg alongside the Achilles. K10 integrates that store over a stance and gets $5.4\ \text{J}$ for the fascia tie alone, against the $\sim17\ \text{J}$ per step quoted in <a href="#origin">§0</a> for the whole arch: one tie is not the whole structure, and the truss model is a lower bound on the arch's elastic return, not an estimate of it.
```

K10's own solution is replaced under B12.

---

### B7 — The Appendix says $E_0$ is the SLS instantaneous modulus; §6 defines it as the equilibrium spring

`module06.html:978` and `module06.html:918`

> `<td>$E_R,\ E_0,\ E_1$</td><td>SLS relaxed, instantaneous, and series-spring moduli</td>`

> `(with $E_0=E_R\tau_\varepsilon/\tau_\sigma$)`

**Fails part 2 (every term defined) and the domain brief's rule that a symbol
means one thing for the whole module.** §6 (`:464`, `:471`) puts the equilibrium
spring $E_0$ in parallel with a Maxwell arm and states
$E_R=E_0$, $E_{\text{inst}}=E_0+E_1$. The Appendix row inverts this, and K5
repeats the inversion, using $E_0$ for the instantaneous modulus. Separately,
$E_{\text{inst}}$ is used throughout §6 and §7 and has **no notation row at all**.

**Fix.** `:978` replacement (two rows for one):

```html
<tr><td>$E_0,\ E_1$</td><td>SLS equilibrium spring and Maxwell-arm spring (the two element moduli of the network)</td><td><a href="#models">&#167;6</a></td></tr>
<tr><td>$E_R,\ E_{\text{inst}}$</td><td>SLS relaxed and instantaneous moduli: $E_R=E_0$, $E_{\text{inst}}=E_0+E_1$</td><td><a href="#models">&#167;6</a></td></tr>
```

K5's use of $E_0$ is corrected in its replacement under B11.

---

### B8 — Eq. (8.1) feeds an angle to a function §2 defines on an elongation

`module06.html:573`

> `$+\,R\,F_{\text{lig}}\big(\theta-\theta_{\text{hi}}\big)$`

**Fails part 1 (a precise statement) and part 2 (every term defined).**
$F_{\text{lig}}$ is the structural law of Eq. (2.1), $F(x)=A_0\sigma(x/L_0)$: its
argument is an elongation in metres. Eq. (8.1) hands it $\theta-\theta_{\text{hi}}$,
an angle in radians. The result is dimensionally meaningless as written. The
missing step is the arc-length relation $x=R\,\Delta\theta$, which is also
exactly where the moment arm $R$ enters twice — once to convert the rotation to
an elongation, once to convert the tension back to a torque.

Lab 3 inherits the confusion: `T = R*k*over**p` with `over` in radians makes
`k = 4.5e6` a quantity in N/rad², which the comment does not say.

**Fix.** Combined with B9 below: the corrected equation appears inside a Lemma
with a proof.

---

### B9 — Eq. (8.1) is a boxed constitutive law with no derivation, beside a fully proved sibling

`module06.html:573`

> `<div class="keyresult">$$\boxed{\;T(\theta)=\begin{cases}…\end{cases}\;}\tag{8.1}$$</div>`

**Fails part 3 (a proof in the smallest setting).** This is the rigor-parity
defect `CLAUDE.md` records for §6, recurring in §8: (8.1) is the section's
governing law for a joint end-stop, and it is asserted, while Proposition 11 in
the same section gets a full moment-balance proof for a much simpler result.
`check_proofs.py` cannot see this — it flags a `.prop`/`.thm`/`.lem` with no
adjacent `.proof`, and (8.1) is a `.keyresult`. It is the judgement call the
gate leaves to the editor.

**Fix.** Promote it to a Lemma with a proof. Numbering it a Lemma rather than a
Proposition avoids renumbering Propositions 10 and 11 and the four cross
references to them (C10, D10, K9, Fig. 18's caption). The proof also lands B8.

`:573` replacement:

```html
<div class="lem"><b>Lemma 1 (the one-sided ligament torque).</b> Let a ligament of moment arm $R$ about the joint axis hang slack over the free range $\theta_{\text{lo}}\le\theta\le\theta_{\text{hi}}$ and, once taut, obey the J-shaped structural law $F_{\text{lig}}$ of Eq.&nbsp;(2.1), whose argument is an elongation. Then the restoring torque it applies to the joint is
$$\boxed{\;T(\theta)=\begin{cases}-\,R\,F_{\text{lig}}\big(R(\theta_{\text{lo}}-\theta)\big), & \theta\lt \theta_{\text{lo}}\ \text{(hyper-extension)}\\[2pt] 0, & \theta_{\text{lo}}\le\theta\le\theta_{\text{hi}}\ \text{(free range: slack)}\\[2pt] +\,R\,F_{\text{lig}}\big(R(\theta-\theta_{\text{hi}})\big), & \theta\gt \theta_{\text{hi}}\ \text{(over-flexion)}\end{cases}\;}\tag{8.1}$$
and it is continuous, with continuous slope, at both limits.</div>
<div class="proof">Inside the free range the ligament is shorter than the gap between its attachments allows. It is a one-sided element: it can pull but not push, so it carries no tension and contributes no torque, $T=0$. Past $\theta_{\text{hi}}$ it is taut and runs at the constant perpendicular distance $R$ from the joint axis, so rotating the joint by $\mathrm{d}\theta$ carries its insertion through an arc $R\,\mathrm{d}\theta$ measured along the line of pull. Integrating from the engagement angle, where the ligament is exactly taut and unstretched, its elongation is $x=R(\theta-\theta_{\text{hi}})$ &#8212; a length in metres, which is what $F_{\text{lig}}$ takes. The tension $F_{\text{lig}}(x)$ then acts at moment arm $R$, so the torque has magnitude $R\,F_{\text{lig}}\big(R(\theta-\theta_{\text{hi}})\big)$ and is directed to reduce $\theta$. Reflecting the argument about the free range gives the hyper-extension branch. For continuity, note from Eq.&nbsp;(2.3) that $F_{\text{lig}}(0)=0$ and $\mathrm{d}F_{\text{lig}}/\mathrm{d}x\to0$ as $x\to0$, because the toe is parabolic: both $T$ and $\mathrm{d}T/\mathrm{d}\theta$ therefore vanish as each limit is approached from outside, and the stop engages smoothly rather than as a jump. <span class="qed">&#8718;</span></div>
```

Lab 3's parameter comment (`:723`) is corrected to name the units the fix
implies:

```python
# a limb rotating fast toward over-flexion; a one-sided ligament stops it
# past the limit. Assumed: segment inertia I (kg m^2), ligament moment arm
# R (m), toe-law stiffness k (N/rad^2 through F_lig(R d_theta)), exponent p
```

---

### B10 — K3, K4, K6 and K9 quote numbers from parameters that are never stated

`module06.html:910`, `:914`, `:922`, `:934`

**Fails part 5 (a tie to something concrete).** In each case the boxed number
cannot be checked from anything on the page.

- **K3** (`:910`): `the fibre carries $\boxed{44\%}$ of the elongation` — depends
  on $A$, $b$ in $F_{PE}(\delta)=A(e^{\delta/b}-1)$ and on the total stretch $S$.
  None is given. I found that $A=60$ N, $b=5$ mm, $S=15$ mm reproduce **44.3%**
  and **93.7%**, so the module's numbers are attainable; they were simply never
  pinned down.
- **K4** (`:914`): `to $\sim0.67$ of peak when too soft, $\sim0.08$ when too
  stiff` — **wrong as stated, not merely unstated.** The solution's own
  $X(k)=F_0/\sqrt{(k-M\omega^2)^2+(c\omega)^2}$ depends on $k$ only through
  $|k-M\omega^2|$, so the response is *symmetric* in detuning. No damping and no
  sweep endpoints can give 0.67 one side and 0.08 the other. $M$ and $c$ are also
  never given (the boxed 21 kN/m implies $M\approx79$ kg).
- **K6** (`:922`): `holds at $E_K\varepsilon_0=20\ \mathrm{MPa}$ … relaxes to the
  finite plateau $E_R\varepsilon_0\approx\boxed{12\ \mathrm{MPa}}$` — needs
  $E_K$, $E_R$, $E_{\text{inst}}$, $\eta$ and the ramp rate, none given. It also
  contradicts K5 and the Appendix: with $E_R=1.20$ GPa at $\varepsilon_0=2\%$ the
  plateau is **24 MPa**, not 12.
- **K9** (`:934`): `migrating $\boxed{\approx1.5}$ link-units … over the first
  $\sim57^\circ$` — "link-units" is not a unit, and the four-bar's link lengths
  are never given, so nothing about the number is checkable.

**Fix.** Replacements with stated parameters and printed numbers are given in §5
(K3, K4, K6, K9). Verified outputs:

```
K3  k_T =      20.0 kN/m -> fibre carries  44.3% of the stretch
    k_T =    1000.0 kN/m -> fibre carries  93.7% of the stretch
    k_T =  100000.0 kN/m -> fibre carries  99.9% of the stretch
K4  k* = M w^2 = 21.3 kN/m   zeta = 0.0056 ; half-power band 1.1%
    k = 0.90 k* -> 0.111 of peak ; k = 1.10 k* -> 0.111 of peak
K6  Maxwell      peak 28.5 MPa -> plateau  0.0 MPa
    Kelvin-Voigt peak 72.0 MPa -> plateau 24.0 MPa
    SLS          peak 39.8 MPa -> plateau 24.0 MPa
K9  centrode arc length 10.6 mm, net migration 10.4 mm over 60 deg
```

---

### B11 — K8's ligament returns 20%, contradicting §7's own table

`module06.html:930`

> `a high-loss ligament ($\tau_\varepsilon/\tau_\sigma=3.2$) returns only $\approx20\%$`

**Fails part 1 and part 5.** §7's table at `:552` gives a ligament resilience of
$\sim0.80$–$0.90$ with $\sim10$–$20\%$ hysteresis. K8 reports $R\approx0.20$,
which is four times worse and matches nothing in the table (not even the
intervertebral disc, at 0.5 to 0.7). Integrating Eq. (6.3) over a tension-only
cycle at 2.6 Hz with $\tau_\sigma=0.05$ s, $\tau_\varepsilon/\tau_\sigma=3.2$
gives **8.3%**, worse still. The fault is the chosen ratio: 3.2 describes a
shock absorber, not a ligament.

Sweeping the ratio locates the two table rows exactly:

```
te/ts = 1.10  ->  R = 92.6%, hysteresis  7.4%   (tendon row: 5-10%, 0.90-0.95)
te/ts = 1.20  ->  R = 85.7%, hysteresis 14.3%   (ligament row: 10-20%, 0.80-0.90)
```

**Fix.** Use 1.10 and 1.20 and quote the computed numbers; replacement in §5.
(K8's `$\approx94\%$` becomes 92.6%, still consistent with C4's "about 93%".)

---

### B12 — K1, K2, K5, K7, K10 are reproducible but ship no code, and two quote seed-dependent numbers as if fixed

`module06.html:902`, `:906`, `:918`, `:926`, `:938`

**Fails part 5.** K2 (9.62 mm / 19.23 J / 13.37 mm / 20.21 J / +5.1%), K7
(14.13 rad/s, 2.25 Hz, $\tan\delta_{\max}=0.354$) and K10 (1.47 kN, 7.36 mm,
5.41 J) all reproduce exactly by hand and by code, so their numbers stand. K1 and
K5 quote the output of a fit to *noisy* data — "recovers $\varepsilon^\ast\approx
3.12\%$, $k_{\text{lin}}\approx424$ kN/m" — with no seed, no sample count and no
noise model, so the numbers are not reproducible even in principle. K1 also gives
no uncertainty, which is the whole point of an inverse problem.

**Fix.** Fix the seed, state the sampling and noise, report the standard errors,
and ship the code. Verified outputs:

```
K1  k_lin = 438.1 +/- 14.6 kN/m (true 416)
    eps*  = 3.23 +/- 0.17 %  (true 3.00)
K5  E_R = 1.203 GPa ; tau_sigma = 0.0480 s ; tau_eps = 0.0866 s
    E_inst = 2.168 GPa (true 2.16)
```

Replacements in §5.

---

### B13 — The 80 kg body mass that three results depend on appears nowhere

`module06.html:669` (`M, g = 80.0, 9.81`), K4 (`:914`), K10 (`:938`)

**Fails the evidence-grading scheme: a number that is neither derived, nor a
table parameter, nor a labelled assumption.** Lab 2 sets $M=80$ kg in code with
no prose mention; K4's boxed 21 kN/m implies $M\approx79$ kg; K10's 1.47 kN
requires $W=2.5\times80\times9.81$ N. The course's reference human
(`EDITOR_DOMAIN.md`, Module 1 Appendix) is **70 kg**. A reader recomputing K10
with 70 kg gets 1.29 kN and 4.1 J and will think the module is wrong.

**Fix.** Add an Appendix parameter row (see B14) and name the mass in the §9
intro (folded into the `:664` replacement under B3) and in K4 and K10 (§5).

---

### B14 — The Appendix parameter table omits every constant the labs and K problems run on

`module06.html:996`–`:1009`

**Fails the evidence-grading scheme.** Fourteen numbers in §9 and §10 have no
table row, no derivation and no "assume": the body mass; Lab 1's $k_R$,
$k_{\text{inst}}$ and 1 kg mass; Lab 2's $k_T$, $F_{\max}$, $\ell_0$ and landing
speed; Lab 3's $I$, $R$, $k$, $p$, the $140^\circ$ limit and the $650^\circ/$s
approach; K3's $A$, $b$, $S$; K9's link lengths.

**Fix.** Insert six rows after `:1004`:

```html
<tr><td>Body mass $M$ (labs of §9, K4, K10)</td><td>$80\ \mathrm{kg}$ (assumed; Module&nbsp;1's reference human is $70\ \mathrm{kg}$)</td><td><a href="#labs">&#167;9</a></td></tr>
<tr><td>Whole-leg series stiffness $k_T$ (Lab&nbsp;2, K4)</td><td>$\approx1.7$&#8211;$2.1\times10^{4}\ \mathrm{N/m}$ (assumed; a lumped leg spring, <em>not</em> the free-tendon $k_{\text{lin}}$)</td><td><a href="#labs">&#167;9</a></td></tr>
<tr><td>Lab-1 SLS stiffnesses $k_R,\ k_{\text{inst}}$; released mass</td><td>$2.0\times10^{5},\ 3.6\times10^{5}\ \mathrm{N/m}$; $1\ \mathrm{kg}$ (assumed)</td><td><a href="#labs">&#167;9</a></td></tr>
<tr><td>Ligament end-stop: inertia $I$, arm $R$, toe constant $k$, exponent $p$</td><td>$0.20\ \mathrm{kg\,m^2}$, $0.03\ \mathrm m$, $4.5\times10^{6}\ \mathrm{N/rad^{2}}$, $2$ (assumed); free-range limit $140^\circ$</td><td><a href="#ligaments">&#167;8</a>, <a href="#labs">&#167;9</a></td></tr>
<tr><td>Passive-fibre law $F_{PE}=A(e^{\delta/b}-1)$; MTU stretch $S$ (K3)</td><td>$A=60\ \mathrm N$, $b=5\ \mathrm{mm}$; $S=15\ \mathrm{mm}$ (assumed)</td><td><a href="#see">&#167;4</a></td></tr>
<tr><td>Cruciate four-bar links: ACL, PCL, tibial, femoral (K9)</td><td>$32,\ 34,\ 28,\ 27\ \mathrm{mm}$ (assumed)</td><td><a href="#ligaments">&#167;8</a></td></tr>
<tr><td>Whole-arch elastic return per step</td><td>$\approx17\ \mathrm J$ (literature, <b>unverified</b>); the single-tie truss model gives $5.4\ \mathrm J$ (K10)</td><td><a href="#origin">&#167;0</a>, <a href="#ligaments">&#167;8</a></td></tr>
```

and replace `:1004` and `:1005` so the time constants and the loss tangent stop
contradicting §7 (B2):

```html
<tr><td>SLS time constants $\tau_\sigma,\ \tau_\varepsilon$</td><td>fast lab mode $0.05,\ 0.09\ \mathrm s$ (assumed; used in §9 and K5&#8211;K8). Real tendon spans $10^{-2}$&#8211;$10^{3}\ \mathrm s$ and its measured hysteresis is set by modes of order seconds to minutes</td><td><a href="#models">&#167;6</a>, <a href="#hysteresis">&#167;7</a>, <a href="#labs">&#167;9</a></td></tr>
<tr><td>Loss tangent in the running band $\tan\delta$</td><td>$\lesssim0.1$ (tendon). The illustrative fast-mode peak of §7 and K7, $\approx0.35$, is a teaching value, not a tendon value</td><td><a href="#hysteresis">&#167;7</a></td></tr>
```

---

### B15 — The module never places its models on the level ladder

`module06.html:117`

**Fails an explicit requirement of `EDITOR_DOMAIN.md`**: "Each module states
which level its models sit on. A Level-1 statics estimate presented as a dynamic
result is a defect." Modules 1 and 2 both do this in §0
(`module01.html:135`, `module02.html:158`); Module 6 does not, and it matters
here more than usual, because §1 to §8 are quasi-static while §9 attaches a mass
and integrates.

**Fix.** Append a paragraph after `:117`:

```html
<p><b>Where this sits on the level ladder.</b> <a class="secref" href="#collagen">§1</a> to <a class="secref" href="#energy">§3</a> and <a class="secref" href="#visco">§5</a> to <a class="secref" href="#ligaments">§8</a> are <b>Level 0</b>: scalar constitutive estimates, one force law per element, loads taken as given, inertia dropped. Every result there is quasi-static, including the hysteresis of <a class="secref" href="#hysteresis">§7</a>, which is a steady-state cyclic response, not a transient. <a class="secref" href="#see">§4</a> raises the muscle&#8211;tendon unit to a dynamic model with its own state variable, the fibre length, and <a class="secref" href="#labs">§9</a> integrates it in time against a single lumped mass; those three simulations are the only place an $m\ddot x$ term appears. Nothing here is a continuum and nothing is multibody: no stress tensor, no spatial field, no fluid phase, and the body never appears except as one mass on one spring. Those rungs are Modules 9 and 16 (<a class="secref" href="#limits">§10</a>, Fig.&nbsp;24).</p>
```

---

### B16 — Fig. 9's "about 6×" is produced by no code and is contradicted by Lab 2's computed 3.3×

`module06.html:335`

> `the tendon recoils about $6\times$ faster than the fibre. Derived from the constraint (4.1) and the tendon law, as ultrasound fascicle measurements confirm.`

**Fails the evidence-grading scheme and part 5.** The figure is a prescribed
decomposition; no code in the module produces the 6, and the same module's
dynamic simulation of the same effect gets 3.3 (Lab 2, verified). The caption
also asserts that ultrasound measurements confirm it, which is an unverified
citation attached to a number the module invented.

**Fix.** `:335` caption replacement:

```html
<figcaption><b>Fibre and tendon move at different speeds.</b> Shortening velocities through a stance phase (pennation $\theta_p=0$ here). During <b>loading</b> the fibre shortens slowly at high force, stretching the tendon (storing energy). During the fast <b>push-off</b> (shaded) the whole-unit velocity $\dot L_{\text{MTU}}$ (dashed) and the tendon recoil $\dot x$ (blue) spike together, while the fibre $\dot\ell$ (red) slows almost to a stop. The split drawn here is <em>prescribed</em>, to show what Eq.&nbsp;(4.4) allows rather than to predict a value; the ratio computed from the coupled dynamics is $3.3\times$ (Lab&nbsp;2, <a class="secref" href="#labs">§9</a>). Ultrasound fascicle tracking reports the same qualitative pattern (unverified here: no source is checked in this repo).</figcaption>
```

---

### B17 — Two arithmetic and range statements in §2 do not hold

`module06.html:217`

> `in the measured range for the free Achilles ($\sim150$–$400\ \text{N/mm}$…)`
> and `consistent with the $\sigma_f\approx100\ \text{MPa}$ of §1 ($\sigma_f A_0\approx7.8\ \text{kN}$)`

**Fails part 1.** The computed $k_{\text{lin}}=416$ N/mm is *above* the stated
range 150 to 400 N/mm, so "in the measured range" is false. And
$100\ \text{MPa}\times80\ \text{mm}^2 = 8.0$ kN, not 7.8; the 7.8 comes from the
model's own $\sigma_f = 97.5$ MPa (Prop. 1), which is the honest number to name.

**Fix.** `:217` replacement:

```html
just above the measured range for the free Achilles ($\sim150$&#8211;$400\ \text{N/mm}$, varying with training and with how much compliant aponeurosis a study includes), which is what a model that ignores the aponeurosis in series should give. The toe ends at $x^\ast=\varepsilon^\ast L_0\approx7.5\ \text{mm}$ and a tension $F(x^\ast)\approx1.6\ \text{kN}$; rupture is near $x_f\approx22.5\ \text{mm}$ and $F_f\approx7.8\ \text{kN}$ &#8212; consistent with <a class="secref" href="#collagen">§1</a>, whose model failure stress is $\sigma_f=97.5\ \text{MPa}$ and gives $\sigma_f A_0=7.8\ \text{kN}$ (the round $100\ \text{MPa}$ would give $8.0\ \text{kN}$).</p>
```

---

### 2A — The ten K-solution replacements in full

Each replaces the `<div>` inside the problem's `<details class="sol">`. Every
one ends with a copy-buttoned code block; in the listings below
`[CODE k0N.py]` stands for the standard `.codewrap` markup of `:630` wrapping
the HTML-escaped contents of `scratchpad/m06/k/k0N.py`. All ten scripts pass
`pycodestyle` and were run; the numbers quoted are their printed output.

**K1** (`:902`):

```html
<details class="sol"><summary>Solution</summary><div>Fit the two-branch $F(x)$ of Eq.&nbsp;(2.3) to 25 points spanning $1$ to $13\ \mathrm{mm}$ of stretch, generated from $\varepsilon^\ast=3.00\%$ and $k_{\text{lin}}=416\ \mathrm{kN/m}$ (<a class="secref" href="#spring">&#167;2</a>) and corrupted with $5\%$ scale noise plus a $40\ \mathrm N$ sensor offset. Nonlinear least squares returns $\boxed{k_{\text{lin}}=438\pm15\ \mathrm{kN/m},\ \varepsilon^\ast=3.23\pm0.17\%}$, both true values inside one standard error: the two-parameter crimp model is identifiable from a single loading curve, and the fit reports how well. The toe strain is what fixes the curvature of the knee between the parabolic and linear branches; fit a straight line instead and the toe vanishes into an over-stiff low-load region, which is how a stiffness quoted without a toe model can be biased high.[CODE k01.py]</div></details>
```

**K2** (`:906`):

```html
<details class="sol"><summary>Solution</summary><div>To reach $4\ \mathrm{kN}$ the linear spring stretches $9.62\ \mathrm{mm}$ and, integrating $\int F\,\mathrm dx$ numerically, stores $U_{\text{lin}}=19.23\ \mathrm{J}$; the toe tendon must stretch further, $13.37\ \mathrm{mm}$, because its compliant toe shifts the linear branch out by $x^\ast/2$, and stores $\boxed{U_{\text{toe}}=20.21\ \mathrm{J}}$, $\mathbf{5.1\%}$ more for the same peak force. The toe is not only protective: the extra low-force excursion banks additional energy at no additional stress, because stress is force per area and the force is capped by the same $4\ \mathrm{kN}$ in both cases.[CODE k02.py]</div></details>
```

**K3** (`:910`):

```html
<details class="sol"><summary>Solution</summary><div>Take the passive fibre law $F_{PE}(\delta)=A\big(e^{\delta/b}-1\big)$ with $A=60\ \mathrm N$ and $b=5\ \mathrm{mm}$, and a total muscle&#8211;tendon stretch $S=15\ \mathrm{mm}$ (all assumed; Appendix). The balance $F_{PE}(\delta)=k_T(S-\delta)$ has no closed form, so each stiffness needs a one-dimensional root find. The fibre then carries $\boxed{44.3\%}$ of the stretch for a soft tendon ($k_T=20\ \mathrm{kN/m}$), $70.7\%$ at $100\ \mathrm{kN/m}$, $93.7\%$ at $1000\ \mathrm{kN/m}$ and $99.9\%$ at $10^{5}\ \mathrm{kN/m}$, approaching $100\%$ as $k_T\to\infty$: the series model reduces numerically to Module&nbsp;5's rigid tendon (Prop.&nbsp;4). The complement, the tendon's share of the elongation, is exactly the stretch the rigid model refuses to have, and so exactly the elastic energy it throws away.[CODE k03.py]</div></details>
```

**K4** (`:914`):

```html
<details class="sol"><summary>Solution</summary><div>Write the bounce as a driven damped oscillator, $M\ddot X+c\dot X+kX=F_0\sin\omega t$, with $M=80\ \mathrm{kg}$ (the body mass assumed throughout <a class="secref" href="#labs">&#167;9</a>), $\omega=2\pi(2.6)\ \mathrm{rad/s}$, and damping set by the tendon's own per-cycle resilience $R=0.93$ (Def.&nbsp;5), which gives $\zeta=(1-R)/4\pi=0.0056$. The steady amplitude $X(k)=F_0/\sqrt{(k-M\omega^2)^2+(c\omega)^2}$ is largest where the elastic and inertial terms cancel, $\boxed{k^\ast=M\omega^2=21.3\ \mathrm{kN/m}}$. Note that $X$ depends on $k$ only through $|k-M\omega^2|$, so the loss is <em>symmetric</em> in detuning: the sweep prints $0.111$ of peak amplitude at $k=0.90k^\ast$ and again at $1.10k^\ast$, and $0.022$ at $0.50k^\ast$ and $1.50k^\ast$. The half-power band is $\Delta k/k^\ast=2\zeta=1.1\%$. Read that sharpness as a limit of the model, not of the leg: a real stance also loses energy to muscle work, soft-tissue damping and the step-to-step collision, all of which raise $\zeta$ and broaden the peak by the same $2\zeta$ rule, while leaving $k^\ast$ where it is. That is why leg stiffness tracks gait frequency, and why a mismatch is costly.[CODE k04.py]</div></details>
```

**K5** (`:918`):

```html
<details class="sol"><summary>Solution</summary><div>Fit the SLS step-strain response $\sigma(t)=\varepsilon_0\big[E_R+(E_{\text{inst}}-E_R)e^{-t/\tau_\sigma}\big]$, with $E_{\text{inst}}=E_R\tau_\varepsilon/\tau_\sigma$ from Prop.&nbsp;7, to 60 samples of a curve generated at $\tau_\sigma=0.050\ \mathrm s$, $\tau_\varepsilon=0.090\ \mathrm s$, $E_R=1.20\ \mathrm{GPa}$ with $2\%$ multiplicative noise. Least squares returns $\boxed{E_R=1.203\ \mathrm{GPa},\ \tau_\sigma=0.0480\ \mathrm s,\ \tau_\varepsilon=0.0866\ \mathrm s}$, hence $E_{\text{inst}}=2.168\ \mathrm{GPa}$ against a true $2.16$. Three features of the curve carry the three constants: the height of the instantaneous jump fixes $E_{\text{inst}}$, the late plateau fixes $E_R$, and the decay rate fixes $\tau_\sigma$. The fourth constant, $\tau_\varepsilon$, is not independent &#8212; it is $\tau_\sigma E_{\text{inst}}/E_R$ &#8212; which is why a single relaxation test suffices.[CODE k05.py]</div></details>
```

**K6** (`:922`):

```html
<details class="sol"><summary>Solution</summary><div>Drive all three models with one history: a $20\ \mathrm{ms}$ ramp to $\varepsilon_0=2\%$, then a $0.6\ \mathrm s$ hold. Use the module's own tendon constants, $E_R=1.20\ \mathrm{GPa}$, $E_{\text{inst}}=2.16\ \mathrm{GPa}$, $\tau_\sigma=0.050\ \mathrm s$ (K5, Appendix), so $\eta=(E_{\text{inst}}-E_R)\tau_\sigma$; give Maxwell the spring $E_M=E_{\text{inst}}$ and Kelvin&#8211;Voigt the spring $E_K=E_R$. Integrating each law: <b>Maxwell</b> peaks at $28.5\ \mathrm{MPa}$ and relaxes to $0.0\ \mathrm{MPa}$; <b>Kelvin&#8211;Voigt</b> spikes to $72.0\ \mathrm{MPa}$ during the ramp (that spike is pure $\eta\dot\varepsilon$, and it would be unbounded for a true step) and then sits at $E_K\varepsilon_0=24.0\ \mathrm{MPa}$ for ever; the <b>SLS</b> peaks at $39.8\ \mathrm{MPa}$, short of its ideal step value $E_{\text{inst}}\varepsilon_0=43.2\ \mathrm{MPa}$ because it already relaxes during the ramp, then decays to the finite plateau $\boxed{E_R\varepsilon_0=24.0\ \mathrm{MPa}}$. Only the SLS shows both signatures at once, an immediate stiffness <em>and</em> a partial, bounded relaxation (<a href="#models">&#167;6</a>).[CODE k06.py]</div></details>
```

**K7** (`:926`):

```html
<details class="sol"><summary>Solution</summary><div>Sweep $\omega$ over six decades through Eq.&nbsp;(7.3) with $\tau_\sigma=0.05\ \mathrm s$, $\tau_\varepsilon=0.10\ \mathrm s$, $E_R=1.20\ \mathrm{GPa}$ and $\varepsilon_0=1\%$. The loop area $W_d=\pi E''\varepsilon_0^2$ and $\tan\delta$ rise, peak and fall together as $\omega$ crosses the material's internal clock: the sweep locates the maximum at $\boxed{\omega^\ast=14.13\ \mathrm{rad/s}}$ against the predicted $1/\sqrt{\tau_\sigma\tau_\varepsilon}=14.14$, with $\tan\delta_{\max}=0.354$ and $W_d=177.6\ \mathrm{kJ/m^3}$ per cycle. Two decades either side the tissue is nearly lossless: $\tan\delta=0.005$ at $0.1\ \mathrm{rad/s}$ and $0.010$ at $1000\ \mathrm{rad/s}$. Dissipation is a resonance of the internal clock, not a monotone property of speed. Now note where that peak lands: $f^\ast=2.25\ \mathrm{Hz}$ is running cadence. This is the <em>fast</em> mode, the one the labs use because it settles inside a short simulation; the modes that dominate a real tendon are slower by one to three decades, which is what puts gait on the low-loss side (<a class="secref" href="#hysteresis">&#167;7</a>, Appendix).[CODE k07.py]</div></details>
```

**K8** (`:930`):

```html
<details class="sol"><summary>Solution</summary><div>Impose a tension-only cycle $\varepsilon(t)=\tfrac12\varepsilon_0(1-\cos\omega t)$ at a cadence of $2.6\ \mathrm{Hz}$, integrate Eq.&nbsp;(6.3) to steady state, and take the resilience as work recovered on the unloading half divided by work done on the loading half. Holding $\tau_\sigma=0.05\ \mathrm s$ fixed, the spread between the two time constants alone sorts the tissues: $\tau_\varepsilon/\tau_\sigma=1.10$ returns $\boxed{92.6\%}$ (hysteresis $7.4\%$) and $\tau_\varepsilon/\tau_\sigma=1.20$ returns $85.7\%$ (hysteresis $14.3\%$). Those are the tendon row and the ligament row of the table in <a class="secref" href="#hysteresis">&#167;7</a>, reproduced from the constitutive law rather than quoted. The governing equation never changes; widening the gap between $\tau_\varepsilon$ and $\tau_\sigma$ alone turns an energy-return spring into a damper, which is the quantitative face of C9.[CODE k08.py]</div></details>
```

**K9** (`:934`):

```html
<details class="sol"><summary>Solution</summary><div>Fix the geometry: femoral attachments at $A_f=(0,0)$ and $P_f=(-26,6)\ \mathrm{mm}$, an ACL of $32\ \mathrm{mm}$, a PCL of $34\ \mathrm{mm}$, and a rigid tibial link of $28\ \mathrm{mm}$ joining their tibial ends (assumed; Appendix). For each tibial orientation one root find places the linkage with both cruciate lengths held fixed, and the instant centre is the intersection of the two cruciate lines (Prop.&nbsp;10). The crossing stays inside both ligaments throughout, moving from $40\%$ along the ACL at full extension to $13\%$ at $60^\circ$, so it is a real crossing and not an extension of the lines outside the joint. The centre itself travels from $(-11.2,-6.3)\ \mathrm{mm}$ to $(-1.1,-4.0)\ \mathrm{mm}$: an arc length of $10.6\ \mathrm{mm}$ and a net migration of $\boxed{10.4\ \mathrm{mm}}$ over $60^\circ$ of flexion, posteriorly and proximally. A fixed-hinge knee would hold one point. The migrating centre is why the femur rolls back on the tibia as it flexes (<a href="#ligaments">&#167;8</a>).[CODE k09.py]</div></details>
```

**K10** (`:938`):

```html
<details class="sol"><summary>Solution</summary><div>Impose a half-sine vertical load peaking at $2.5$ body weights on an $80\ \mathrm{kg}$ body (the mass assumed throughout <a class="secref" href="#labs">&#167;9</a>), pass it through the truss relation $T=Wb/(4h)$ with $b=0.15\ \mathrm m$ and $h=0.05\ \mathrm m$, and load a linear tie of stiffness $k_{PF}=2\times10^{5}\ \mathrm{N/m}$ (Appendix). The peak tie tension is $1.47\ \mathrm{kN}$, the fascia stretches $7.36\ \mathrm{mm}$, and the tie banks $\boxed{5.41\ \mathrm J}$ at peak load, against the Achilles' $32\ \mathrm J$ (<a href="#energy">&#167;3</a>): $14\%$ of the pair. Read the gap to <a href="#origin">&#167;0</a> carefully. The $\sim17\ \mathrm J$ quoted there is an unverified literature figure for the <em>whole</em> arch, every plantar ligament and the joint capsules together; this model has one tie, so a smaller number is the expected result, not a discrepancy. The single-tie truss is a lower bound on the arch's elastic return. Even at that bound, ignoring the arch under-counts the free elastic return of the leg by about a seventh (<a href="#ligaments">&#167;8</a>).[CODE k10.py]</div></details>
```

---

## 3. Style and clarity edits

Line-level. The standard bans "very", "simply", "obviously", "clearly",
"powerful", "elegant" and hedges of that family; each instance below is a real
one, not a false positive.

| # | line | original | rewrite |
|---|---|---|---|
| S1 | 142 | `very compliant` | `compliant` |
| S2 | 192 | `simply rescaled` | `rescaled` … and `very different $F(x)$` → `quite different $F(x)$` becomes `$F(x)$ curves that differ by an order of magnitude` |
| S3 | 153 | `is simply the full straight-collagen modulus scaled by` | `is the full straight-collagen modulus scaled by` |
| S4 | 245 | `worth stating in its three equivalent forms` | `stated here in three equivalent forms` |
| S5 | 275 | `For now the spring is very nearly ideal` | `For now the spring loses under a tenth of what it stores` |
| S6 | 412 | `Elongations along a line simply accumulate` | `Elongations along a line accumulate` |
| S7 | 510 | `<b>Slow</b> loading` … `The small dip … the linear model's viscous 'push'` | keep the physics; replace the straight quotes with `&#8220;push&#8221;` for typographic consistency with the rest of the file |
| S8 | 539 | `near zero when loading is very slow or very fast` | `near zero when loading is far slower or far faster than the material clock` |
| S9 | 603 | `an unrestrained arch under load would simply splay flat` | `an unrestrained arch under load splays flat` |
| S10 | 754 | `It is worth being equally clear about what it leaves out.` | `Be equally clear about what it leaves out.` |
| S11 | 828 | `a ligament's less-ordered architecture dissipates more per cycle` | `a ligament, less strictly ordered, dissipates a larger fraction each cycle` (this is the only `check_prose` flag in the file) |
| S12 | 103 | `the net work the muscles do is surprisingly small` | `the net work the muscles do is a small fraction of the energy that cycles through the leg` |
| S13 | 273 / 1003 | Definition 5 gives `$R\approx0.90$–$0.93$; the missing $7$–$10\%$`, the Appendix gives `$\approx0.90$–$0.93$; $\approx5$–$10\%$`, and §7's table gives `$\sim0.90$–$0.95$ / $\sim5$–$10\%$` — three different bands, and the Appendix row is internally inconsistent (0.93 pairs with 7%, not 5%) | make all three `$0.90$–$0.95$` with `$5$–$10\%$` hysteresis, matching §7's table and bracketing every computed value in the module (Lab 1: 0.911; K8: 0.926) |
| S14 | 109 | `The bookkeeping is striking.` | `The bookkeeping is worth doing.` (folded into B6) |
| S15 | 748 | `with the fibre near-isometric` | `with the fibre shortening at a third of the spring's recoil speed` (folded into B5) |

---

## 4. Structural notes

1. **§5 has no derivational and no computational problem.** The problem map at
   `:806` shows `§5 viscoelasticity | C7 | — | —`. That is defensible: §5 is
   definitional and §6 immediately formalises it, so D6, D7, K5 and K6 exercise
   the same material one section later. No change recommended, but the map's own
   claim in the sentence above it — "read by row, that every section is
   exercised" — is stronger than the table supports. Softening it to "every
   section is exercised, §5 through the models it feeds in §6" would be honest.
2. **§9's three labs are well chosen and genuinely different** (a released
   oscillator, a coupled two-state hop, a one-sided end-stop with a sensitivity
   sweep). Lab 2 is the only one that discharges a stated debt from another
   module, and the module is right to say so.
3. **The K strand is strong in design and weak in delivery.** Every one of the
   ten is a real computation — an inverse problem, a sweep, an optimisation, a
   regime comparison — and none is plug-the-numbers-in, which is exactly the
   `EDITOR_DOMAIN.md` standard that Module 5 §10 had to be retrofitted for. The
   defect is entirely that the computations are described rather than shipped.
4. **Nothing needs cutting.** The §6 digression on series and parallel is long
   for what it proves and it earns every line; leave it.

---

## 5. What already works

- **The §6 derivation of the sharing rule** (`:398`–`:432`). Two principles,
  equilibrium and compatibility, applied twice, with a free-body figure, a
  summary table, a resistor analogy that is then cashed out, and an explicit
  statement of the massless-junction assumption and the quasi-static regime it
  implies. This is what part 3 of the standard asks for and it is rare to see it
  done this carefully.
- **Proposition 10 and its proof** (`:585`–`:588`). The instant centre is
  located by a two-line velocity argument in the smallest setting that shows the
  mechanism, and it then explains roll-then-glide and the screw-home without
  further machinery.
- **Propositions 1, 2 and 3.** One assumption (uniform crimp distribution),
  integrated three times, giving the toe, the structural law and the stored
  energy, with continuity checked at $\varepsilon^\ast$ each time and the numbers
  worked out immediately afterwards. `:170` and `:217` are exactly the "check
  against real tendon" the standard wants.
- **The rescue in §3.3** (`:277`–`:283`): $U=F^2/2k$ read as a design principle,
  with the rigid strut as the degenerate limit, tying straight back to Module 5's
  Assumption 7.1.
- **§7's honesty about its own figure** (`:510`, `:547`): the caption names the
  dip below $\sigma=0$ as a linear-model artefact, and the text says outright
  that the illustrative $\tan\delta\approx0.30$ is fattened to make the loop
  visible. That instinct is right; B2 asks only that it be extended to the time
  constants.
- **The captures-and-misses table** (`:762`–`:766`): four idealisations, each
  with what it omits and the module that repays it. It is the model of an IOU
  table.

---

---

## 6. Changes applied

Applied to `edited/module06.html` by one re-runnable script,
`scratchpad/m06/apply.py` — 52 `rep`/`repline`/`repspan`/`after` edits, each
asserting its anchor occurs exactly once, with a single `write_text` at the end.
Line numbers below are the **original** `module06.html`. The ten K scripts and
the two rewritten lab blocks live in `scratchpad/m06/k/`; all pass
`pycodestyle`, and every number in the table was printed by running them.

### Corrections to this report, made during the apply

The brief's rule is that a run beats the report. Five of the report's own
statements did not survive re-running:

- **K4's "half-power band $\Delta k/k^\ast=2\zeta=1.1\%$" was mislabelled.**
  Amplitude falls to $1/\sqrt2$ of peak at $k=(1\pm2\zeta)k^\ast$, so $2\zeta$
  is the *half*-width and the band is $4\zeta=2.2\%$ wide. Verified by printing
  the amplitude at $k^\ast(1\pm0.0111)$: both give exactly $0.707$. `k04.py`
  and the shipped K4 text now say "half-power half-width $\pm2\zeta$, a band
  $4\zeta=2.2\%$ wide".
- **K1's noise was described as "a $40\ \mathrm N$ sensor offset".** `k01.py`
  adds $40\ \mathrm N$ of Gaussian sensor noise, not a constant offset. The
  shipped text says "a $40\ \mathrm N$ sensor noise floor".
- **B15's ladder paragraph named only Level 0.** The ladder in `prompt.txt`
  (Level 0 scalar → Level 10 multiscale) and the model paragraph at
  `module02.html:158` also name the rung a model *rests on*. The shipped
  paragraph puts §1–§3 and §5–§8 at **Level 0 on Level 1 static loads**, §4 at
  **Level 5** (muscle–tendon actuator), §9's labs at the smallest **Level 2**
  case, and names **Level 3** (Modules 8–9) and **Level 9** (Module 16) as the
  rungs not climbed.
- **S13 had to reconcile five instances of the resilience band, not two.** The
  report named `:273` and `:1003`; `:109`, `:500` and `:660` also carried
  $90$–$93\%$. All five now read $90$–$95\%$ with $5$–$10\%$ hysteresis,
  matching §7's table and bracketing both computed values (Lab 1: 0.911;
  K8: 0.926).
- **B14 was written as "six rows"; it is seven.** All seven are inserted,
  alongside the two rewritten rows.

- **B2b's replacement caption for Fig. 16 was wrong about the figure.**
  The report asserted the curve is “drawn with the fast lab mode
  $\tau_\sigma=0.05\ \mathrm s$, whose own peak would fall inside the gait band”.
  Reading the SVG settles it the other way: the x-axis title is the
  **dimensionless** $\omega\tau_\sigma$, the polyline's minimum-$y$ vertex sits at
  $x=238.4$, i.e. $\omega\tau_\sigma=10^{(238.4-250)/90}=0.74=1/\sqrt{1.8}$, and the
  shaded rect spans $x=331.3$ to $425.9$, i.e. $\omega\tau_\sigma=8$ to $90$. No
  $\tau_\sigma$ is baked into the curve at all, and the peak is far *left* of the
  band. The shipped caption states the axis, the peak's location, the band's
  span, and the fact that the fast lab mode would put a few-hertz gait at
  $\omega\tau_\sigma\approx0.8$ — on the peak, not past it. This is the one defect
  in this pass that no gate could have caught: `check_svg`, `check_overlap`,
  `check_frame` and `verify_dom` were all green on the wrong caption.

Two further inconsistencies surfaced only on the re-run and are fixed in the
shipped text: the Appendix's $\tau_\varepsilon=0.09\ \mathrm s$ against K7's
$0.10\ \mathrm s$ (the row now says so), and Lab 2's "about 16 cm" leg
compression, which was asserted by nobody's code — `lab2.py` now accumulates
and prints it as $164\ \mathrm{mm}$.

### The two defects `CLAUDE.md` records for this module

Both were already repaired before this pass; both are confirmed here rather
than assumed.

- **§6 rigor parity (6.1 and 6.2 asserted beside a proved 6.3): fixed.**
  Confirmed by locating each `\tag{6.N}` and reading its enclosing block, not by
  trusting a gate count: Eq. (6.1) sits inside `.prop` **Proposition 5
  (Maxwell law)**, Eq. (6.2) inside **Proposition 6 (Kelvin–Voigt law)**, and
  Eq. (6.3) inside **Proposition 7 (the standard-linear-solid law)**, each with
  an adjacent `.proof`. What *had* recurred is the same defect one section
  later, in §8, where Eq. (8.1) was a bare `.keyresult` beside a fully proved
  Proposition 11; B8+B9 promotes it to a proved Lemma.
- **§0's shell-mangled caption: clean.** `verify_dom` reports **0 swallowed
  prose**, and Fig. 2's caption renders `$W$` and `$F_{\text{GRF}}$` as two
  separate inline math runs inside ordinary prose, not as one italic run.

### The edits

| tag | line (original) | what changed | how verified |
|---|---|---|---|
| S12 | 103 | "the net work the muscles do is surprisingly small" → "…is a small fraction of the energy that cycles through the leg" | banned hedge removed; the replacement states the comparison the hedge implied |
| B6a+S14 | 109 | "The bookkeeping is striking" → "worth doing"; resilience `90–93%` → `90–95%`; the bare **17 J** now labelled a literature value for the arch as a whole, quoted **unverified**, with the note that §8's single-tie truss accounts for about a third of it (K10) | `k10.py` prints 5.41 J; $5.41/17=0.32$ |
| B15 | after 117 | new paragraph placing the module on the level ladder: Level 0 on Level 1 loads (§1–§3, §5–§8), Level 5 (§4), the smallest Level 2 case (§9's labs); Level 3 and Level 9 named as the rungs not climbed | rung names read from `prompt.txt:286–296` and the model paragraph `module02.html:158` |
| S1 | 142 | "very compliant" → "compliant" | banned intensifier |
| S3 | 153 | "is simply the full straight-collagen modulus scaled by" → "is the full…" | banned "simply" |
| S2a | 192 | "simply rescaled" → "rescaled" | banned "simply" |
| S2b | 192 | "but very different $F(x)$" → "but $F(x)$ curves that differ by the full ratio of their $A_0/L_0$" | the ratio is exactly $k_{\text{lin}}=A_0E_{\text{lin}}/L_0$, derived two lines above; a vague intensifier replaced by the derived scaling |
| B17 | 217 | "in the measured range" → "**just above** the measured range" (the computed 416 N/mm exceeds the quoted 150–400 N/mm), with the reason — no aponeurosis in series; and $\sigma_fA_0=7.8$ kN now attributed to §1's model $\sigma_f=97.5$ MPa, noting that a round 100 MPa gives 8.0 kN | hand arithmetic: $100\ \mathrm{MPa}\times80\ \mathrm{mm^2}=8.0\ \mathrm{kN}$; $97.5\times80=7.80\ \mathrm{kN}$ |
| S4 | 245 | "worth stating in its three equivalent forms" → "stated here in three equivalent forms" | banned "worth VERBing" |
| S13a | 273 | Definition 5: $R\approx0.90$–$0.93$, missing $7$–$10\%$ → $0.90$–$0.95$, missing $5$–$10\%$, cross-linked to §7's table | matches §7's table (`:551`) and brackets Lab 1's 0.911 and K8's 0.926 |
| S5 | 275 | "the spring is very nearly ideal" → "the spring loses under a tenth of what it stores, and we treat it as ideal" | the hedge replaced by the quantity it stood for; consistent with the 5–10% band |
| B16 | 335 | Fig. 9's caption drops the uncomputed "about $6\times$" and the "as ultrasound fascicle measurements confirm" citation; the split is now labelled **prescribed**, the computed ratio $3.3\times$ is cited to Lab 2, and the ultrasound claim is marked unverified in this repository | `lab2.py` prints 3.3×; no code anywhere in the module produces a 6 |
| B2c | 494 | "$\tau_\sigma,\tau_\varepsilon$ set the crossover timescales (seconds to minutes for tendon)" → names both the fast lab mode $0.05\ \mathrm s$ used in §9 and the slow modes that set the measured hysteresis | $\omega\tau_\sigma=2\pi(2.6)(0.05)=0.82$, which is not "large"; hand arithmetic |
| S13c | 500 | "§3 found a resilience of $90$–$93\%$" → "$90$–$95\%$" | S13 reconciliation |
| S7 | 510 | straight quotes `'push'` → `&#8220;push&#8221;` | typographic consistency with the rest of the file |
| S8 | 539 | "near zero when loading is very slow or very fast" → "far slower or far faster **than the material clock**" | banned intensifier; the replacement names the reference the comparison needs |
| B2b | 541 | Fig. 16's caption now says the curve is drawn with the **fast lab mode** $\tau_\sigma=0.05\ \mathrm s$, whose own peak falls inside the gait band (K7), and that the shaded band sits above the peak of the **slow** modes that dominate real tissue | `k07.py`: peak at 14.13 rad/s = 2.25 Hz, inside a 2.6 Hz gait band |
| B2a | 543 | the module's headline answer to "why is a tendon a good spring" rewritten: real tendon has a **spectrum**; the labs use its fast end, the slow modes ($\tau_\sigma\gtrsim1\ \mathrm s$) carry the measured hysteresis and put gait at $\omega\tau_\sigma\gtrsim10$. Replaces a claim the module's own parameters contradicted | `k07.py` (fast-mode peak at 2.25 Hz = running cadence); $2\pi(2.6)\times1\ \mathrm s=16.3$ |
| B8+B9 | 573 | Eq. (8.1) promoted from an asserted `.keyresult` to **Lemma 1 with a proof**, and its argument corrected from the angle $\theta-\theta_{\text{hi}}$ (radians) to the elongation $R(\theta-\theta_{\text{hi}})$ (metres), which is what $F_{\text{lig}}$ takes. The proof derives the arc-length relation, both branches, and $C^1$ continuity at each limit | dimensional check against Eq. (2.1); continuity from Eq. (2.3), where $F(0)=0$ and $\mathrm dF/\mathrm dx=k_{\text{lin}}x/x^\ast\to0$; `check_proofs` still 0 |
| S9 | 603 | "an unrestrained arch under load would simply splay flat" → "…splays flat" | banned "simply" |
| B6b | 614 | the arch's "$\sim17$ J per step noted in §0" reconciled: K10's computed 5.4 J is for the fascia tie alone and is a **lower bound** on the whole-arch figure, not a competing estimate | `k10.py` prints 5.41 J |
| S13d | 660 | Lab 1: "squarely the $90$–$93\%$" → "inside the $90$–$95\%$" | S13 reconciliation; Lab 1 computes 0.911 |
| B3a | 664 | Lab 2's intro now names $M=80\ \mathrm{kg}$; names $k_T=1.7\times10^4$ N/m a **whole-leg** spring, 24× softer than §2's $4.16\times10^5$ N/m free Achilles; says why (the block prints a 164 mm leg compression, which no single tendon supplies); and warns that its stored energy is not comparable with §3's 32 J | `lab2.py` prints 164 mm; $4.16\times10^5/1.7\times10^4=24.5$ |
| B4 | 666–710 | Lab 2's code block replaced: `kT` relabelled a whole-leg series spring, and four accumulators added (`Fpk`, `Upk`, `spk`, `Wmus`) so the peak ground reaction, the peak leg compression, the banked energy, the muscle work and the fibre's final length factor are all **printed** rather than asserted in prose | `lab2.py` prints 3.3 BW, 164 mm, 197 J, 6.8 J, 97% elastic, $f_L=0.57$, speed ratio 0.30; `check_code` 0 issues |
| B3b | 712 | Fig. 22's caption: "the tendon recoils $\sim3.3\times$" → "the leg-spring recoil … the spring recoils $3.3\times$" | relabelling only; the ratio is printed by `lab2.py` |
| B5 | 714 | Lab 2's results paragraph rewritten. All five numbers are now cited as printed, and the claim that the fibre is **near-isometric** is replaced by what the simulation shows: the fibre shortens $18\ \mathrm{mm}$ — a third of $\ell_0$ — and $f_L$ falls from 1.00 to 0.57; what is near zero is its *velocity*, 0.30 of the spring's recoil speed | `lab2.py` printed output |
| B9b | 721–723 | Lab 3's parameter comment now states the units the corrected Eq. (8.1) implies: $T=Rk(\theta-\theta_{\text{hi}})^p$, so $k$ is in N/rad$^p$; cross-referenced to Lemma 1 | follows from B8+B9; `check_code` 0 issues |
| S15 | 748 | "with the fibre near-isometric" → "with the fibre shortening at a third of the spring's recoil speed" | `lab2.py`: 0.30 of the recoil speed |
| S10 | 754 | "It is worth being equally clear about what it leaves out." → "Be equally clear about what it leaves out." | banned "worth VERBing" |
| B1a | 798 | "the computational answers are Python-verified" → "every computational solution ships the Python that prints its numbers"; and the map's "every section is exercised" softened to name §5's actual route, through the models it feeds in §6 | the map at `:806` shows §5 with no D and no K problem, so the old claim over-stated its own table |
| S11 | 828 | "a ligament's less-ordered architecture dissipates more per cycle" → "a ligament, less strictly ordered, dissipates a larger fraction each cycle" | the file's only `check_prose` flag at baseline; now 0 |
| B1b | 898 | "Each answer below is Python-verified." → "Every boxed number below is printed by the code that follows its solution: copy the block, run it, and check." | true once B10–B12 land the ten code blocks |
| B12-K1 | 902 | K1's seedless, sampleless, uncertainty-free fit replaced: 25 points over 1–13 mm, 5% scale noise plus a 40 N sensor noise floor, seed fixed, and the answer now carries standard errors — $k_{\text{lin}}=438\pm15$ kN/m, $\varepsilon^\ast=3.23\pm0.17\%$, both true values inside one standard error. Code block attached | `k01.py` printed output |
| B12-K2 | 906 | numbers sharpened to the printed values (9.62 mm, 19.23 J, 13.37 mm, 20.21 J, **5.1%**), and "at no additional stress" given its reason — the peak force is capped at 4 kN in both cases. Code block attached | `k02.py` printed output |
| B10-K3 | 910 | K3's unstated parameters supplied ($A=60$ N, $b=5$ mm, $S=15$ mm, labelled assumed and added to the Appendix); the stated **44% → 44.3%** and **94% at 1000 kN/m → 93.7%**, with the 70.7% and 99.9% rungs of the sweep shown. Code block attached | `k03.py` printed output |
| B10-K4 | 914 | the asymmetric, unreproducible "$\sim0.67$ of peak when too soft, $\sim0.08$ when too stiff" removed: $X(k)$ depends on $k$ only through $\lvert k-M\omega^2\rvert$, so detuning is **symmetric** — 0.111 at both $0.90k^\ast$ and $1.10k^\ast$, 0.022 at both $0.50k^\ast$ and $1.50k^\ast$. $M=80$ kg, $\zeta=0.0056$ and the half-power band $4\zeta=2.2\%$ now stated. Code block attached | `k04.py` printed output, including amplitude 0.707 at $k^\ast(1\pm2\zeta)$ |
| B12-K5 | 918 | K5's $E_0$ — which §6 defines as the *equilibrium* spring — replaced by $E_{\text{inst}}$ throughout; noise model and sample count stated; results are the printed 1.203 GPa, 0.0480 s, 0.0866 s, hence $E_{\text{inst}}=2.168$ GPa against a true 2.16. Code block attached | `k05.py` printed output; the notation collision itself is fixed by B7 |
| B10-K6 | 922 | K6's unstated constants supplied ($E_R=1.20$ GPa, $E_{\text{inst}}=2.16$ GPa, $\tau_\sigma=0.05$ s, a 20 ms ramp to 2% then a 0.6 s hold). The wrong SLS plateau **12 → 24.0 MPa** and the wrong Kelvin–Voigt hold **20 → 24.0 MPa**; the SLS peak given as the computed 39.8 MPa, short of the ideal 43.2 because it relaxes during the ramp. Code block attached | `k06.py` printed output; $E_R\varepsilon_0=1.20\ \mathrm{GPa}\times0.02=24.0$ MPa |
| B12-K7 | 926 | numbers made exact (14.13 rad/s against a predicted 14.14, $\tan\delta_{\max}=0.354$, $W_d=177.6\ \mathrm{kJ/m^3}$, 0.005 and 0.010 two decades either side), and the fact that $f^\ast=2.25$ Hz **is running cadence** now stated and reconciled with §7 — this is the fast mode. Code block attached | `k07.py` printed output |
| B11-K8 | 930 | K8's ligament resilience **20% → 85.7%** and tendon **94% → 92.6%**. The old $\tau_\varepsilon/\tau_\sigma=3.2$ describes a shock absorber and contradicted §7's own table (ligament 0.80–0.90); ratios 1.10 and 1.20 reproduce the tendon and ligament rows from the constitutive law instead of quoting them. Code block attached | `k08.py` printed output: 92.6% / 7.4% and 85.7% / 14.3%, landing in §7's 5–10% and 10–20% rows |
| B10-K9 | 934 | "$\approx1.5$ **link-units** over the first $\sim57^\circ$" — not a unit, and no geometry given — replaced by a stated four-bar (ACL 32, PCL 34, tibial 28 mm; femoral attachments $(0,0)$ and $(-26,6)$ mm, all assumed and added to the Appendix) and a computed migration of **10.4 mm over $60^\circ$**, arc length 10.6 mm, with the crossing shown to stay inside both ligaments (ACL fraction 0.40 → 0.13). Code block attached | `k09.py` printed output |
| B12-K10 | 938 | numbers made exact (1.47 kN, 7.36 mm, **5.41 J**, 14% of the pair), the 80 kg mass named, and the gap to §0's 17 J explained rather than left standing: one tie is a **lower bound** on a many-element arch. Code block attached | `k10.py` printed output |
| B7 | 978 | the notation row "$E_R,\ E_0,\ E_1$ — SLS relaxed, **instantaneous**, and series-spring moduli" contradicted §6, which defines $E_0$ as the equilibrium spring. Split into two rows: $E_0,E_1$ as the two element moduli, and $E_R,E_{\text{inst}}$ with $E_R=E_0$, $E_{\text{inst}}=E_0+E_1$ — which also gives $E_{\text{inst}}$ the notation row it never had | §6 at `:464` and `:471`; `check_links` 0 broken |
| S13b | 1003 | Appendix resilience row $0.90$–$0.93$ / $5$–$10\%$ → $0.90$–$0.95$ / $5$–$10\%$ (the old row paired 0.93 with 5%, inconsistent on its own terms) | S13 reconciliation |
| B14a | 1004 | the $\tau_\sigma,\tau_\varepsilon$ row now labels 0.05, 0.09 s the **assumed fast lab mode**, records that K7 uses $\tau_\varepsilon=0.10$ s, and says the measured hysteresis comes from modes of order seconds to minutes | B2; `k07.py` uses 0.10 s |
| B14b | 1005 | "loss-tangent **peak** $\lesssim0.1$" was labelled a peak while §7 and K7 compute a peak of 0.354. Retitled "loss tangent in the running band", with the 0.35 named a teaching value rather than a tendon value | `k07.py`: $\tan\delta_{\max}=0.354$ |
| B2b-fix | 541 | Fig. 16's caption rewritten again after reading its SVG: the axis is the dimensionless $\omega\tau_\sigma$, the peak is at $0.74$, the shaded band is $8$ to $90$, and the fast lab mode would put gait at $\approx0.8$ — on the peak, not past it | SVG geometry: axis title `loading frequency ω·τσ (log)`, ticks $10^{-2}$ at $x=70$ and $10^{2}$ at $x=430$ (90 px/decade), polyline min-$y$ vertex at $x=238.4$, shaded `<rect x="331.3" width="94.6">` |
| B3c | 712 | Fig. 22's `aria-label` still said “blue tendon speeds… the tendon recoils” after B3 relabelled the element a whole-leg spring | consistency with B3/B4; the figure plots `lab2.py`'s output |
| B3d | 712 | Fig. 22's legend `v_tendon (recoil)` → `v_spring (recoil)` | same |
| B5c | 712 | Fig. 22's legend `v_fibre ≈ 0 (isometric)` → `v_fibre (slow)` — the simulation this figure plots has the fibre shortening 18 mm | `lab2.py`: $f_L$ falls 1.00 → 0.57; `check_overlap` still 0 after the shorter label |
| B3e | 912 | K4's statement “optimise the leg (tendon) stiffness” → “the leg-spring stiffness”; its $k^\ast=21.3$ kN/m is a leg spring, not a tendon | B3; `k04.py` |
| B13+B14c | after 1008 | seven new parameter rows, each labelled *assumed*: body mass 80 kg (with Module 1's 70 kg reference human named beside it), whole-leg $k_T$, Lab 1's $k_R,k_{\text{inst}}$ and 1 kg mass, the ligament end-stop's $I,R,k,p$ with its $140^\circ$ limit and $650^\circ/\mathrm s$ approach, K3's $A,b,S$, K9's four-bar links, and the whole-arch 17 J marked **literature, unverified** beside K10's computed 5.4 J | each value read out of the code block it appears in; the 17 J is the one number the module cannot derive, and is now labelled as such |

### Gates after the apply

All nine required gates, plus the three advisory scripts. Zero everywhere the
baseline was zero; nothing worse anywhere.

| gate | baseline | after |
|---|---|---|
| `checktex` | 842 segments, **0** issues | 1001 segments, **0** issues |
| `checklt` | **0** | **0** |
| `check_links` | 217 links, **0** broken, **0** unlinked | 250 links, **0** broken, **0** unlinked |
| `check_svg` | **0** hard, **0** advisory | **0** hard, **0** advisory |
| `check_code` | 3 blocks, **0** issues | **13** blocks, **0** issues |
| `verify_dom` | 0 mjx-merror, 6 stray `$`, 0 broken, 0 swallowed | 0 mjx-merror, 6 stray `$`, 0 broken, **0 swallowed** |
| `check_overlap` | **0** | **0** |
| `check_frame` | **0** clipped; 1 margin advisory (§0 Achilles/ACL figure) | **0** clipped; the same 1 advisory |
| `check_bodyprop` | **0** hard; 1 advisory (MTU schematic head) | **0** hard; the same 1 advisory |
| `check_prose` | 1 flag (`:828`) | **0** |
| `check_proofs` | **0** | **0** (Lemma 1 carries its proof) |
| `check_probfig` | **0** | **0** |

Beyond the gates: all 13 `<pre><code>` blocks were extracted **from the edited
file**, HTML-unescaped, checked for live HTML tags (0 found), run to
completion, and their stdout compared line by line against every number the
surrounding prose quotes. The module now ships thirteen runnable blocks where
it shipped three, and the claim that its computational answers are verified is
one the reader can now test.
