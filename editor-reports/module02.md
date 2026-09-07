# Editor report: module02.html (Bones as Hierarchical Load-Bearing Structures)

Editorial pass. Standard: the five-part rule of the `science-editor` skill, read against `EDITOR_DOMAIN.md`. Every location is `module02.html:LINE`. Every replacement is valid HTML with MathJax delimiters and uses only the box classes the stylesheet defines. All eleven Python blocks in the file (the lab and K1 to K10) were extracted, run, and compared with the prose (scripts in the session scratchpad, folder `m02/`: `extract_run.py`, `verify.py`, `replacements.py`, `newk.py`). Every number in a replacement below was printed by the code shown beside it. The replacement HTML was written to a temp file and passed `checktex.py` and `checklt.py` (0 issues each).

## 1. Verdict

Yes, after revision. A graduate reader with no biomechanics can learn from these pages how a hollow bone carries compression cheaply, why bending and torsion are the danger, and how one feedback law produces both training gain and disuse loss. Theorem 3.2, Proposition 3.3, and Proposition 4.1 each carry a proof of matching weight, and all eleven code blocks print exactly the numbers the text states. What stops the reader is elsewhere. Two results are wrong: K6 draws elastic similarity as a flat stress line when the module's own scaling gives stress growing as the eighth root of body mass (a factor 4.7 from shrew to elephant), and D5 says similar bones "bow to the same shape" when the relative deflection grows linearly with size. The lab caption says the remodeling equilibria take 100 to 150 days; the code reaches 95 percent of the change in 24 to 36 days and the linearized time constant is 8.3 days. The fall-force law (6.1) is asserted beside two proved siblings and silently drops the weight's work during compression, which is 15 percent of the energy and 8 percent of the force. The bending animation moves the compression fibre along the longest arc. Two mechanostat figures are hidden under 36 px and 18 px black bars from the July realism commit. K2's aging model is not the boxed remodeling law: with the lazy zone of (7.1) a drifting setpoint produces no bone loss at all. The Appendix has no notation table and its parameter table holds 8 of the roughly 30 empirical numbers the text uses. Four of the ten computational problems are plug-in arithmetic. All of this is repairable without touching Theorem 3.2, Proposition 3.3, or Proposition 4.1, which are sound.

## 2. Blocking defects

Ranked by severity: factual errors first (two are drawn into figures), then asserted results, then structure that stops the reader, then missing scaffolding, then problem-set depth.

### B1. K6 draws elastic similarity as constant stress, and D5 says similar bones keep the same shape

Location: `module02.html:595` (D5 solution), `module02.html:731-753` (K6 statement, figure, solution, code).

Quoted (D5, line 595): "Hence curvature $\kappa=M/EI\propto\lambda^4/\lambda^4=\lambda^0$ (similar bones bow to the <em>same</em> shape)".

Quoted (K6, line 753): "<em>Elastic</em> similarity (diameter $\propto L^{3/2}$) instead holds $\sigma$ roughly constant, which is why real large mammals keep peak bone stress near $\sim\!50$ MPa across four decades of body mass". The code at line 741 encodes this: `sig_ela = np.full_like(m, sig_ref)`.

Factual errors. (a) Same curvature is not the same shape. The tip deflection of a beam of length $L$ at curvature $\kappa$ is $\delta\sim\kappa L^2$, so $\delta/L\sim\kappa L\propto\lambda$: the relative sag grows with size. (b) Under elastic similarity, $d\propto L^{3/2}$ gives body mass $M_b\propto Ld^2\propto L^4$, so $L\propto M_b^{1/4}$ and $d\propto M_b^{3/8}$. The self-weight moment is $M\propto M_bL\propto M_b^{5/4}$ and $Z\propto d^3\propto M_b^{9/8}$, so $\sigma\propto M_b^{1/8}$. Computed: 18.0 MPa at 0.02 kg, 50 MPa at 70 kg, 85.3 MPa at 5000 kg, a factor 4.7. Constant stress needs a third rule, $d\propto L^2$ (stress similarity). The flat green line in the K6 figure is therefore not a regime the module derives. Also, K6's anchor "typical peak locomotor stress of $\sim50$ MPa" is a bare number that contradicts §3's "typical vigorous" 99 MPa (see B6).

Replacement for the D5 solution (line 595):

```html
<details class="sol"><summary>Show solution</summary><p>Plane-section geometry gives $\sigma=E\kappa y$; equating to $\sigma=My/I$ yields $\boxed{\kappa=M/(EI)}$, with $EI$ the <em>bending stiffness</em>. Scale every length by $\lambda$: $I\propto d^4\propto\lambda^4$, so $EI\propto\lambda^4$; the self-weight $\propto$ volume $\propto\lambda^3$ acts over a moment arm $\propto\lambda$, so $M\propto\lambda^4$. Hence the curvature $\kappa=M/(EI)\propto\lambda^0$ is the same for all sizes, but the <em>shape</em> is not: a beam of length $L$ at curvature $\kappa$ sags by $\delta\sim\kappa L^2$, so the relative sag $\delta/L\sim\kappa L\propto\lambda$ grows with size. The peak stress $\sigma_\max=Mc/I\propto\lambda^4\cdot\lambda/\lambda^4=\lambda$ grows the same way. Both the relative deflection and the stress of a geometrically scaled bone rise linearly with size; a bone four times longer (the human-to-elephant factor is $\lambda=(5000/70)^{1/3}=4.1$) would sag four times more for its length and carry four times the stress. Two other rules remove one problem each: <em>elastic similarity</em> ($d\propto L^{3/2}$) keeps $\delta/L$ fixed, and <em>stress similarity</em> ($d\propto L^2$) keeps $\sigma$ fixed. K6 works out what each rule does to stress across the mammalian size range.</p></details>
```

Replacement for K6 (lines 731 to 753). The figure is to be regenerated from the code; the current green polyline encodes the wrong regime.

```html
<div class="prob"><p><b>K6 (allometric regime comparison).</b> Anchor a limb bone at the reference human: body mass $M_b=70$ kg and an assumed peak locomotor bending stress $\sigma_{70}=50$ MPa (Appendix; a running-level value, below the vigorous $99$ MPa of <a class="secref" href="#bending">§3</a>). Derive the exponent $p$ in $\sigma\propto M_b^{\,p}$ for three scaling rules: geometric similarity ($d\propto L$), elastic similarity ($d\propto L^{3/2}$), and stress similarity ($d\propto L^2$). Sweep body mass from a shrew ($0.02$ kg) to an elephant ($5000$ kg), and find where each rule crosses the $130$ MPa tensile strength. <span class="probes">Probes: three scaling regimes from one moment-over-section-modulus argument, and which of them a real large animal can afford.</span></p>
<figure><!-- regenerate: three curves sigma(M_b) on log mass, with the 130 MPa line and the two crossovers --><figcaption>Peak bending stress vs. body mass under three scaling rules, anchored at $50$ MPa for $70$ kg. Geometric similarity ($\sigma\propto M_b^{1/3}$) crosses bone strength at $1230$ kg; elastic similarity ($\sigma\propto M_b^{1/8}$) reaches $85$ MPa at $5000$ kg and would cross only at $1.5\times10^5$ kg; stress similarity ($\sigma\propto M_b^{0}$) never crosses.</figcaption></figure>
<details class="sol"><summary>Show solution</summary><p>Write the bone's length as $L$ and diameter as $d$, with body mass $M_b\propto Ld^2$. The self-weight bending moment is $M\propto M_bL$ and the section modulus is $Z\propto d^3$, so $\sigma\propto M_bL/d^3$. Under geometric similarity $d\propto L$ and $M_b\propto L^3$: $\sigma\propto L\propto M_b^{1/3}$. Under elastic similarity $d\propto L^{3/2}$, so $M_b\propto L^4$, $L\propto M_b^{1/4}$, $d\propto M_b^{3/8}$, and $\sigma\propto M_b^{5/4}/M_b^{9/8}=M_b^{1/8}$. Under stress similarity $d\propto L^2$, so $M_b\propto L^5$ and $\sigma\propto M_b^{6/5}/M_b^{6/5}=M_b^{0}$. Anchored at $50$ MPa for $70$ kg, the three rules give $3.3$, $18.0$, and $50$ MPa for the shrew and $207$, $85$, and $50$ MPa for the elephant. Geometric scaling crosses the $130$ MPa strength at $M_b=70\,(130/50)^3=1230$ kg, a rhino-sized ceiling; elastic similarity is still safe at $5000$ kg and would cross only at $70\,(130/50)^8=1.5\times10^5$ kg; stress similarity never crosses, at the price of a diameter-to-length ratio $2.3$ times the human one at elephant size ($1.7$ times for elastic similarity). The lesson is not that elephants keep stress constant (that is outside this model) but that no rule keeps both the relative sag of D5 and the stress fixed without making limbs disproportionately thick. That thickness is the visible cost of size.</p>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np
sig_ref, m_ref, sig_str = 50.0, 70.0, 130.0        # MPa at 70 kg (assumed)
regimes = {"geometric": 1/3, "elastic": 1/8, "stress": 0.0}
for name, p in regimes.items():
    shrew, eleph = (sig_ref*(mb/m_ref)**p for mb in (0.02, 5000.0))
    cross = m_ref*(sig_str/sig_ref)**(1/p) if p else np.inf
    print(f"{name}: shrew {shrew:.1f} elephant {eleph:.1f} MPa, "
          f"crosses 130 MPa at {cross:.3g} kg")
# -&gt; geometric: shrew 3.3 elephant 207.5 MPa, crosses 130 MPa at 1.23e+03 kg
# -&gt; elastic:   shrew 18.0 elephant 85.3 MPa, crosses 130 MPa at 1.46e+05 kg
# -&gt; stress:    shrew 50.0 elephant 50.0 MPa, crosses 130 MPa at inf kg</code></pre></div></details></div>
```

Also change the C9 solution (line 556) "so large animals adopt <em>elastic similarity</em> (diameter $\propto L^{3/2}$), i.e. disproportionately stout bones. Quantified in K6." to "so large animals must depart from geometric similarity toward stouter bones; K6 compares the two rules that do this (elastic similarity, $d\propto L^{3/2}$, and stress similarity, $d\propto L^2$) and shows what each buys."

### B2. The lab caption gives the wrong adaptation timescale

Location: `module02.html:473`.

Quoted: "the equilibria $Z_\text{eq}=M/(E\varepsilon_\text{hi,lo})$ are reached in $\sim$100–150 days, the real timescale of bone turnover."

Factual error: text says 100 to 150 days, code gives 24 days (95 percent of the change) and 37 days (99 percent) for the load increase, 36 and 56 days for disuse. The polyline in the figure already sits at 132.8 percent on day 32 against a final 133.3 percent. D8's own formula gives the linearized time constant $1/(k\varepsilon_\text{hi})=8.3$ days and $1/(k\varepsilon_\text{lo})=12.5$ days with the Appendix $k=80$. Do not fix this by lowering $k$ to make 100 days true: K1's $1602\ \mu\varepsilon$ and K9's true $k=60$ both depend on $k=80$. Replacement for line 473:

```html
<figcaption>Integration of the remodeling ODE (7.1), computed values. Each trajectory settles when peak strain re-enters the lazy zone. With the Appendix gain $k=80$ the linearized time constants are $1/(k\varepsilon_\text{hi})=8.3$ days for formation and $1/(k\varepsilon_\text{lo})=12.5$ days for resorption (D8), so the curves complete 95 percent of their change by day 24 (load increase) and day 36 (disuse). The gain is a toy value chosen for a readable plot; it sets only the speed, never the equilibria $Z_\text{eq}=M/(E\varepsilon_\text{hi,lo})$.</figcaption>
```

### B3. The fall-force law (6.1) is asserted beside two proved siblings, drops the weight's work during compression, and compares against two bare strengths

Location: `module02.html:334-337`.

Quoted (line 334): "An effective mass $m_\text{eff}$ falling a height $h$ … arrives with kinetic energy $m_\text{eff}\,g\,h$; equating this to the spring's stored energy $\tfrac12 k_s x^2$ and using $F=k_s x$ gives the peak force". Quoted (line 337): "A healthy proximal femur tolerates $\sim4\ \mathrm{kN}$ (survives); an osteoporotic one $\sim2\ \mathrm{kN}$ (fractures)."

Missing parts: (3) proof: (3.1) got a `.thm` and (4.1) a `.prop`, each with a `.proof`; (6.1) is a two-line prose derivation, the Module 6 §6 gap the brief names. (4) limit case: the energy balance stops the mass at height $h$ above the spring's rest point, but the mass keeps falling by $x$ while the spring compresses, releasing a further $m_\text{eff}gx$. Computed: $x=0.074$ m, so that term is 15 percent of $m_\text{eff}gh=137$ J; the exact balance gives $F_\text{peak}=3991$ N, 7.7 percent above the 3706 N of (6.1). With that correction the "healthy tolerates 4 kN, survives" margin is gone (3.99 against 4.0). The module may keep (6.1) as the leading-order form, but it must say what it drops and how much. (5) number class: 4 kN and 2 kN are in no table and have no derivation. Replacement for lines 334 to 337:

```html
<p>Why a fall, not standing, breaks the hip: a sideways fall delivers a large force over a few centimetres of soft-tissue compression. Model the impact as energy capture by an effective spring (soft tissue plus pelvis) of stiffness $k_s$ (the subscript $s$ keeps it distinct from the remodeling gain $k$ of <a class="secref" href="#adapt">§7</a>; the symbol $E$ stays reserved for Young's modulus). An effective mass $m_\text{eff}$, the part of the body whose momentum the hip must stop, falls a height $h$ before the hip meets the floor.</p>
<div class="prop"><b>Proposition 6.1 (peak force of a spring-arrested fall).</b> Let a mass $m_\text{eff}$ fall from rest a height $h$ onto a linear spring of stiffness $k_s$, with $g$ the gravitational acceleration. The peak spring force is
$$F_\text{peak}=m_\text{eff}g\left(1+\sqrt{1+\frac{2k_sh}{m_\text{eff}g}}\right)\approx\boxed{\;\sqrt{2\,k_s\,m_\text{eff}\,g\,h}\;}\tag{6.1}$$
where the boxed form holds when the compression $x=F_\text{peak}/k_s$ is small compared with $h$.</div>
<div class="proof">
Take the spring's rest point as the zero of height. The mass starts at height $h$ with no kinetic energy and stops, momentarily, at maximum compression $x$ below the rest point. Between those two states gravity does work $m_\text{eff}g(h+x)$ and the spring stores $\tfrac12k_sx^2$; no other force does work, so $\tfrac12k_sx^2=m_\text{eff}g(h+x)$. This quadratic in $x$ has the positive root $x=\dfrac{m_\text{eff}g}{k_s}\left(1+\sqrt{1+\dfrac{2k_sh}{m_\text{eff}g}}\right)$, and $F_\text{peak}=k_sx$ gives the exact form. When $x\ll h$ the term $m_\text{eff}gx$ is negligible against $m_\text{eff}gh$, the balance reduces to $\tfrac12k_sx^2=m_\text{eff}gh$, and $F_\text{peak}=k_s\sqrt{2m_\text{eff}gh/k_s}=\sqrt{2k_sm_\text{eff}gh}$, the boxed form. The neglected term is exactly the weight's work over the compression stroke. <span class="qed">∎</span>
</div>
<div class="keyresult"><b>Worked number.</b> With the Appendix values $m_\text{eff}=28\ \mathrm{kg}$, $h=0.5\ \mathrm m$, $k_s=5\times10^{4}\ \mathrm{N\,m^{-1}}$: the drop releases $m_\text{eff}gh\approx137\ \mathrm J$, the boxed form gives $F_\text{peak}\approx3.7\ \mathrm{kN}$ at a compression $x=0.074$ m, and the exact form gives $3.99\ \mathrm{kN}$ at $x=0.080$ m, because $m_\text{eff}gx$ adds 15 percent to the energy and $x/h=0.15$ is not small. This module keeps the boxed form and its $3.7$ kN as the working value; the 8 percent it undercounts is the first correction. Against the assumed proximal-femur strengths of the Appendix, $\sim4\ \mathrm{kN}$ healthy and $\sim2\ \mathrm{kN}$ osteoporotic, the healthy hip sits at the edge of its margin and the osteoporotic hip is well past it. The same fall is marginal or catastrophic depending on a strength the body itself sets over years (<a class="secref" href="#adapt">§7</a>).</div>
```

Change the D10 solution (line 620) to cite the proposition: after "$F_\text{peak}=k_sx=\boxed{\sqrt{2k_sm_\text{eff}gh}}$" add "(the small-compression form of Proposition 6.1; the exact balance adds the weight's work $m_\text{eff}gx$ and raises the force by 8 percent at these values)". Change diagnostic 4 (line 507) "Duration is irrelevant; the impulsive <em>force</em> is what breaks bone." to "For a single overload the duration is irrelevant; the peak <em>force</em> is what breaks bone (repeated loading is the separate fatigue route of <a class="secref" href="#failure">§6</a>)."

### B4. The bending animation moves the compression fibre along the longest arc

Location: `module02.html:267-287`.

Quoted (caption, line 287): "Pure-bending kinematics: the outer fibres deform most, the neutral fibre not at all". Quoted keyframes: top fibre `M30,60 Q220,128 410,60`, neutral `M30,90 Q220,150 410,90`, bottom `M30,120 Q220,172 410,120`.

Factual error in the figure: all three fibres keep the same fixed endpoints (chord 380 px) and the top fibre is given the largest sagitta (34 px against 30 and 26). A curve with a fixed chord and a larger sagitta is longer. Computed arc lengths at the mid keyframe: top (labelled compression) 388.0 px, neutral 386.2 px, bottom (labelled tension) 384.7 px. The animation shows the compression fibre lengthening most and the tension fibre least, the opposite of Theorem 3.2 and of its own caption. This is the "SMIL keyframes are physics" rule of `CLAUDE.md` broken. Fix: make the bent state a set of concentric arcs. The neutral fibre keeps its length; the top fibre, on the inside of the bend, shortens; the bottom fibre, on the outside, lengthens. Replacement for the three `<path>` elements (lines 269 to 282):

```html
  <path fill="none" stroke="#1a1a1a" stroke-width="1.6" d="M30,90 Q220,90 410,90">
    <animate attributeName="d" dur="4s" repeatCount="indefinite"
      values="M30,90 Q220,90 410,90; M34,84 Q220,150 406,84; M30,90 Q220,90 410,90"/>
  </path>
  <path fill="none" stroke="#7a1f1f" stroke-width="2.4" d="M30,60 Q220,60 410,60">
    <animate attributeName="d" dur="4s" repeatCount="indefinite"
      values="M30,60 Q220,60 410,60; M52,56 Q220,120 388,56; M30,60 Q220,60 410,60"/>
  </path>
  <path fill="none" stroke="#2a7d2a" stroke-width="2.4" d="M30,120 Q220,120 410,120">
    <animate attributeName="d" dur="4s" repeatCount="indefinite"
      values="M30,120 Q220,120 410,120; M16,112 Q220,180 424,112; M30,120 Q220,120 410,120"/>
  </path>
```

Computed arc lengths of these mid-keyframe paths: top 344.0 px (shortens), neutral 379.7 px (keeps its 380 px length within 1 px), bottom 415.4 px (lengthens). The three are concentric arcs about one centre, so the picture now matches (3.1). Extend the caption: "The three fibres are drawn as concentric arcs about one centre of curvature, so the top fibre shortens, the neutral fibre keeps its length, and the bottom fibre lengthens, as (3.1) requires."

### B5. The two mechanostat figures are unreadable

Location: `module02.html:382` and `module02.html:544`.

Quoted (line 382): `<line x1="160" y1="100" x2="300" y2="100" stroke="#1a1a1a" stroke-width="36.4"/>`; (line 544): `<line x1="128" y1="96" x2="196" y2="96" stroke="#1a1a1a" stroke-width="17.7"/>`.

Missing part: (5) the tie to something concrete is the figure, and the figure does not show what the caption says. Rendered (scratchpad `m02/fig7_mechanostat.png`, `figC7.png`): the "lazy zone", the flat segment of the mechanostat curve where the rate is zero, is drawn as a black bar 36 px tall in §7 and 18 px tall in C7. The bar hides the strain axis, the vertical rate axis, the two threshold ticks, and (in §7) the "lazy zone" label itself, which is black text on the black bar. The reader sees a solid block where the caption promises a zero-rate plateau. Commit `3fd6fbe` (2026-07-20, "Course-wide biological figure realism") introduced both widths; every hardening gate passed because none measures stroke width. Replacements:

- line 382: `stroke-width="36.4"` to `stroke-width="2.4"`.
- line 544: `stroke-width="17.7"` to `stroke-width="2.4"`.

Also add `markerUnits="userSpaceOnUse"` to the local marker `b3ar` (line 193), the only marker in the file without it. The other thick strokes in the file (line 593, `stroke-width="10"`, and line 822, `stroke-width="9"`) are beam bodies, render correctly, and stay.

### B6. §3 blurs the joint torque with the shaft bending moment, and the "typical" stress is four different numbers

Location: `module02.html:183` and `module02.html:262`; against `module02.html:413` (lab, 1250 µε = 21 MPa), `module02.html:712` (K4, 60 MPa), `module02.html:753` (K6, 50 MPa).

Quoted (line 183): "offsets create a <em>bending moment</em> $M$ (the joint torques of Module&nbsp;1, now applied to the shaft)". Quoted (line 262): "At a typical vigorous bending moment $M\approx200$ N·m the femur sits at $\sigma\approx99$ MPa".

Missing parts: (1) precise statement. The brief lists joint torque against joint reaction force as a pair that must not be blurred. The joint torque of Module 1 is the muscle moment about the joint axis; the bending moment in the shaft is the joint <em>reaction force</em> acting off the shaft axis, through the femoral neck of Fig. 1. At $F=1715$ N the 200 N m of the caption implies an offset $M/F=0.117$ m, larger than a femoral neck, so the 200 N m is a vigorous-activity value with muscle and inertial contributions, not a standing-stance number. Number class: 200 N m is in no table. Consistency: the module's habitual stress is $\varepsilon E=1250\times10^{-6}\times17\ \mathrm{GPa}=21$ MPa in the lab, 50 MPa "typical peak locomotor" in K6, 60 MPa in K4, and 99 MPa "typical vigorous" here. Each is defensible for a different activity, but the text never says so. Replacement for line 183:

```html
<p>Body weight rarely acts along the bone axis. The joint reaction force, of the kind <a class="secref" href="module01.html#muscle">Module&nbsp;1</a> derives at the elbow (Proposition 5.2), here the assumed hip load $F$ of <a class="secref" href="#axial">§2</a>, enters the femoral head, which sits off the shaft axis at the end of the femoral neck (Fig. 1), so the shaft carries a <em>bending moment</em> $M=F\,e$ with $e$ the perpendicular offset of the force line from the shaft axis. This is not the joint torque of Module&nbsp;1, which is the muscle moment about the joint; it is the contact force times its lever about the shaft. Muscle pulls and the inertial loads of running add to it. The module uses three activity levels for $M$, all listed in the Appendix as assumptions: the habitual gait value that sets the lab's $1250\ \mu\varepsilon$ ($M_\text{ref}=E\,\varepsilon\,Z=43$ N m, 21 MPa), a running-level $50$ MPa (K6), and a vigorous-activity $M=200$ N m ($99$ MPa) used below for the safety-factor comparison. Bending, not compression, produces the largest stresses. We derive the Euler–Bernoulli result.</p>
```

(The value $M_\text{ref}=1250\times10^{-6}\times17\times10^{9}\times2.02\times10^{-6}=42.9$ N m is the `M_ref` of the lab code.) Change the caption at line 262 "At a typical vigorous bending moment $M\approx200$ N·m" to "At the assumed vigorous-activity bending moment $M=200$ N·m (Appendix)". Change K4's `60e6` and K6's "$\sim\!50$ MPa" to cite the Appendix rows added in B17.

### B7. §2 leans on a forward reference to Module 3, uses "safety factor" four sections before it is defined, and compares against a bare strength

Location: `module02.html:179`.

Quoted: "Single-leg stance loads the femur to roughly $2.5\times$ body weight including hip-muscle force (from <a class="secref" href="module03.html#reaction">Module&nbsp;3, §4</a>) … Against a compressive strength $\sim170\ \mathrm{MPa}$ that is a safety factor of $\sim45$."

Missing parts: dependencies point backward only; the reader is sent to a module they have not read for the load that every later number rests on. "Safety factor" is defined at line 329 (§6) as $n=\sigma_Y/\sigma_\max$ but used here, in the §3 caption, and in diagnostic 1. The compressive strength 170 MPa appears here, in §3, and in C3, and is in no table (the Appendix lists only the tensile 120 to 150 MPa). Replacement for line 179:

```html
<div class="def"><b>Definition 2.1 (safety factor).</b> For a load that produces a peak stress $\sigma_\max$ in a material of strength $\sigma_f$ (the stress at which it fails in that sense of loading), the <em>safety factor</em> is $n=\sigma_f/\sigma_\max$. A factor of $2$ means the load could double before failure.</div>
<div class="keyresult"><b>Worked number.</b> Take the single-leg-stance femoral load as $F=2.5\,Mg$ with $M=70$ kg the reference human of Module&nbsp;1: $F\approx2.5\times70\times9.81\approx1717\ \mathrm N$. The factor $2.5$ is an assumption here (Appendix); it is larger than $1$ because the hip abductors must pull down on the pelvis to balance the trunk over one leg, and their pull adds to the weight on the femoral head. Module&nbsp;3 derives the factor from that balance. With $R=14\ \mathrm{mm}$, $r=7\ \mathrm{mm}$, $A=4.62\times10^{-4}\ \mathrm m^2$, so $\sigma_\text{axial}=1717/4.62\times10^{-4}\approx3.7\ \mathrm{MPa}$. Against the compressive strength of cortical bone, $\sigma_c\approx170\ \mathrm{MPa}$ (Appendix), Definition 2.1 gives $n\approx45$. Pure compression is not what breaks bones: the bone could carry $\sigma_cA\approx78\ \mathrm{kN}$, about eight tonnes-force, before crushing.</div>
```

Delete the sentence "The <em>safety factor</em> is $n=\sigma_Y/\sigma_\max$;" from line 329 and write "By Definition 2.1 the safety factor is $n=\sigma_Y/\sigma_\max$;". The "carries tonnes" of the §0 title is now earned by the 78 kN.

### B8. The 45° principal-stress claim rests on a formula the module never derives, and "Mohr's circle" is never defined

Location: `module02.html:307` (§4) and `module02.html:602-605` (D7).

Quoted (line 307): "Rotate that surface element by $45^\circ$, however, and the shear resolves into pure normal stresses … (the Mohr's-circle result for pure shear; derived in <a class="secref" href="#problems">§10</a>, D7)". Quoted (D7 statement, line 602): "Starting from the plane-stress transformation $\sigma_n(\theta)=\tfrac{\sigma_x+\sigma_y}{2}+\tfrac{\sigma_x-\sigma_y}{2}\cos2\theta+\tau_{xy}\sin2\theta$, prove …".

Missing parts: (3) proof: the spiral-fracture explanation, the module's second headline result, is deferred to a problem whose starting formula is handed to the reader unproved. (2) terms: "Mohr's circle" and "principal stress" are used without definition. The smallest setting is a wedge in equilibrium, four lines. Insert after line 306, before the "Why the fracture spirals" paragraph:

```html
<div class="lem"><b>Lemma 4.2 (pure shear resolves into tension and compression at 45°).</b> Consider a small square element of the bone surface whose faces carry shear stress $\tau$ and no normal stress (a state of <em>pure shear</em>). On the plane inclined at $45^\circ$ to the faces the stress is purely normal and equals $+\tau$ (tension); on the plane at $-45^\circ$ it is purely normal and equals $-\tau$ (compression). These are the element's <em>principal stresses</em>, the largest and smallest normal stresses over all plane orientations, $\sigma_1=+\tau$ and $\sigma_2=-\tau$.</div>
<div class="proof">
Cut the square element along a diagonal and keep the triangular half whose two short faces, of length $a$ each (per unit depth), carry the shear $\tau$; the diagonal face has length $a\sqrt2$. On the two short faces the shear forces are $\tau a$ each, directed along the faces. By the equal-and-opposite pairing of shear on perpendicular faces, their vector sum is perpendicular to the diagonal and has magnitude $\tau a\sqrt2$. Equilibrium of the wedge requires the diagonal face to carry an equal and opposite force $\tau a\sqrt2$, also perpendicular to the diagonal, hence a normal stress of magnitude $\tau a\sqrt2/(a\sqrt2)=\tau$ and no shear. Whether it is tension or compression depends on which diagonal was cut: on one the two face forces pull the wedge apart (tension, $\sigma_1=+\tau$), on the other they push it together (compression, $\sigma_2=-\tau$). For a general orientation $\theta$ the same wedge balance gives a normal stress $\tau\sin2\theta$, which is extremal at $\theta=\pm45^\circ$ (D7 carries out this step), so no other plane carries a larger normal stress. <span class="qed">∎</span>
</div>
```

Then in line 307 replace "(the Mohr's-circle result for pure shear; derived in <a class="secref" href="#problems">§10</a>, D7)" with "(Lemma 4.2)". In the D7 statement (line 602) replace "Starting from the plane-stress transformation" with "The wedge balance of Lemma 4.2, carried out for a general cut angle $\theta$ and a general plane stress state, gives the transformation formula". In the D7 caption and the C4 solution replace "Mohr's circle" and "(Mohr, D7)" with "(Lemma 4.2)"; Mohr's circle is a graphical device the module does not build and should not name.

Also line 311, quoted: "so a hard rotational fall lands within a safety factor of $\sim2$ of a spiral fracture". Computed: $260/150=1.75$ for the idealized tube, and $140/150=0.93$ to $180/150=1.2$ against the real-femur range in the same sentence. Replacement for that clause: "so a hard rotational fall of $150$ N m has a safety factor of $1.75$ against the idealized tube, and between $0.9$ and $1.2$ against the assumed real-femur failure range of $140$ to $180$ N m: a spiral fracture is a matter of which femur."

### B9. §7 asserts the equilibrium and its stability; the proof lives in a problem

Location: `module02.html:399`.

Quoted: "At equilibrium the bone grows or shrinks until strain re-enters the band: $Z_\text{eq}=M/(E\,\varepsilon_\text{hi})$ after a load increase, $Z_\text{eq}=M/(E\,\varepsilon_\text{lo})$ after disuse. <em>The bone chases a target strain, not a target size.</em>"

Missing part: (3) proof, and (4) the limit case. The section's one result, used by the lab, the sensitivity paragraph, C7, and K2, is asserted; D8 proves it at line 610. A forward reference to the problem set is one the reader must accept on faith. Move the proof up. Replace the quoted sentence with "The consequences of (7.1) are Lemma 7.2." and insert after the `.def` box:

```html
<div class="lem"><b>Lemma 7.2 (equilibrium and stability of the remodeling law).</b> Under a constant habitual moment $M$, the law (7.1) has a continuum of rest states: every $Z$ with $M/(E\varepsilon_\text{hi})\le Z\le M/(E\varepsilon_\text{lo})$ is an equilibrium (the lazy zone). A bone starting below that interval grows to $Z_\text{eq}=M/(E\varepsilon_\text{hi})$; a bone starting above it shrinks to $Z_\text{eq}=M/(E\varepsilon_\text{lo})$. Both approaches are exponential, with time constants $1/(k\varepsilon_\text{hi})$ and $1/(k\varepsilon_\text{lo})$.</div>
<div class="proof">
Substitute $\varepsilon=M/(ZE)$ into the formation branch: $\dfrac{dZ}{dt}=kZ\Big(\dfrac{M}{ZE}-\varepsilon_\text{hi}\Big)=k\Big(\dfrac{M}{E}-\varepsilon_\text{hi}Z\Big)$, which is linear in $Z$ with the single zero $Z_\text{eq}=M/(E\varepsilon_\text{hi})$. Write $\delta=Z-Z_\text{eq}$; then $\dot\delta=-k\varepsilon_\text{hi}\delta$, so $\delta(t)=\delta(0)\,e^{-k\varepsilon_\text{hi}t}$ decays with time constant $1/(k\varepsilon_\text{hi})$. The branch applies while $\varepsilon\gt\varepsilon_\text{hi}$, that is while $Z\lt Z_\text{eq}$, so a bone below the band grows toward $Z_\text{eq}$ and stops there, because inside the band the rate is zero. The resorption branch is the same computation with $\varepsilon_\text{lo}$ in place of $\varepsilon_\text{hi}$, approached from above. Inside the band $dZ/dt=0$ identically, so every such $Z$ is a rest state. With the Appendix values the time constants are $8.3$ and $12.5$ days. <span class="qed">∎</span>
</div>
<p>Two things follow. The bone chases a target <em>strain</em>, not a target size: double the load and the equilibrium doubles. And the destination is one edge of the band, never its middle, so where a bone rests depends on its history; a bone whose load only ever rose sits at $\varepsilon_\text{hi}$. The gain $k$ sets only the speed. K2 shows what this history dependence does to an aging prediction.</p>
```

Leave D8 in place; change its statement to "Reproduce Lemma 7.2 for the formation branch: find the equilibrium, prove it is stable by linearizing, and identify the time constant" and its solution's closing "The gain $k$ sets only the speed" stays.

### B10. Definition 3.1 defines the neutral axis as the centroidal line, then Theorem 3.2 and D2 prove that it is

Location: `module02.html:185`, against `module02.html:214-216` and `module02.html:571-576`.

Quoted (Definition 3.1): "Under pure bending the cross-section rotates about a line through its centroid — the <em>neutral axis</em> — where strain is zero."

Missing part: (1) precise statement. The definition asserts the theorem's conclusion; the proof then "establishes" what was defined. Replacement for line 185:

```html
<div class="def"><b>Definition 3.1 (neutral axis, second moment of area, section modulus).</b> Under pure bending each cross-section rotates rigidly about some line in its own plane on which the fibre strain is zero; that line is the <em>neutral axis</em>. (Theorem 3.2 shows it passes through the section's centroid.) Let $y$ be the signed distance of a point of the section from the neutral axis. The <em>second moment of area</em> about that axis is $I=\int_A y^2\,dA$, in $\mathrm m^4$; it measures how far the material sits from the axis. The <em>section modulus</em> is $Z=I/c$, where $c$ is the distance from the axis to the outermost fibre. Example: for the hollow circle of <a class="secref" href="#axial">§2</a>, $I=\tfrac{\pi}{4}(R^4-r^4)=2.83\times10^{-8}\ \mathrm m^4$ and $Z=I/R=2.02\times10^{-6}\ \mathrm m^3$ (D3 does the integral).</div>
```

### B11. K2's aging model is not the boxed law (7.1), and it duplicates the §8 extension box

Location: `module02.html:657-681` (K2) and `module02.html:479` (extension box).

Quoted (K2 statement): "let the strain setpoint drift up at $0.2\%$/yr (aging). Using $Z_\text{eq}=M/(E\varepsilon^*)$ and the fall force (6.1), find the age at which the fall safety factor crosses $1$." Quoted (extension box): "drive the bone with a daily load <em>and</em> a slow age-related rise in $\varepsilon^*$, track $Z(t)$ to age 80, then at each age compute the fall force (6.1) against the strength implied by $Z$. At what age does the safety factor cross 1?"

Missing parts: (1) precise statement. K2 uses a single setpoint $\varepsilon^*=1250\ \mu\varepsilon$, the middle of the band. Under (7.1) the band has a lazy zone, and a bone resting at $1250\ \mu\varepsilon$ does nothing while the band drifts: the lower edge $\varepsilon_\text{lo}=1000\,(1+0.002\,t)\ \mu\varepsilon$ reaches $1250$ only after 125 years. Computed by integrating (7.1) with the drifting band: the safety factor stays at $1.079$ to age 130 and never crosses 1, for the baseline and for both interventions. K2's "age 70" therefore rests on collapsing the band to one setpoint, an assumption stated nowhere. It is also closed-form ($1.079/(1+0.002\,t)\lt1$ gives $t=39.7$ years) and duplicates the extension box, which asks the same question. Replacement for K2 (lines 657 to 681); the extension box at line 479 becomes "<b>Extension challenge.</b> K2 integrates (7.1) with an aging band and finds that the answer depends on where in the lazy zone the adult bone rests; extend it with a slow decline in habitual load $M$ (less activity with age) and find which of the two aging routes, setpoint drift or load decline, crosses the fall threshold first."

```html
<div class="prob"><p><b>K2 (regime comparison: one setpoint against a lazy zone).</b> Starting from peak bone mass at age $30$, with the bone resting at $\varepsilon=1250\ \mu\varepsilon$, let the mechanostat thresholds rise with age at $0.2\%$ per year (an assumed aging drift, Appendix). Take the fall force from (6.1) and the hip strength as $S=S_0\,Z/Z_0$ with $S_0=4$ kN (Appendix). Integrate two versions of the remodeling law day by day to age $130$: (a) the band of (7.1), both edges drifting; (b) the band collapsed to a single setpoint $\varepsilon^*=1250\,(1+0.002\,t)\ \mu\varepsilon$, so $dZ/dt=kZ(\varepsilon-\varepsilon^*)$. For each, find the age at which the fall safety factor $S/F_\text{peak}$ crosses $1$, then repeat with $+10\%$ habitual load and with a $10\%$ lower setpoint. <span class="probes">Probes: the lazy zone makes the remodeling prediction depend on where the adult bone rests; a fractional change in the setpoint beats the same fractional change in load because $\varepsilon^*$ enters inversely.</span></p>
<figure><!-- regenerate: safety factor vs age for the collapsed-setpoint model (three curves) and the flat band-model line --><figcaption>Fall safety factor vs. age. With the band collapsed to one setpoint the baseline crosses $1$ at age $69.7$; $+10\%$ load delays it to $123.7$ and a $10\%$ lower setpoint to $129.7$. With the lazy zone of (7.1) the bone at $1250\ \mu\varepsilon$ never leaves the band and the safety factor stays at $1.08$.</figcaption></figure>
<details class="sol"><summary>Show solution</summary>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np
E, Z0, k = 17e9, 2.02e-6, 80.0
M_ref = 1250e-6*Z0*E
meff, h, g, ks = 28.0, 0.5, 9.81, 5e4
Fpeak = np.sqrt(2*ks*meff*g*h)        # 3706 N, equation (6.1)
S0, drift = 4000.0, 0.002             # strength at Z0; setpoint drift per year


def cross_age(load=1.0, lower=0.0, band=True, years=100):
    Z, M = Z0, load*M_ref
    for day in range(int(years*365)):
        f = (1 + drift*day/365)*(1 - lower)
        e = M/(Z*E)
        if band:                       # (7.1) with the band drifting
            lo, hi = 1000e-6*f, 1500e-6*f
            rr = k*Z*(e - hi) if e &gt; hi else (k*Z*(e - lo) if e &lt; lo else 0.0)
        else:                          # band collapsed to one setpoint
            rr = k*Z*(e - 1250e-6*f)
        if S0*(Z/Z0)/Fpeak &lt; 1:
            return round(30 + day/365, 1)
        Z = max(Z + rr, 1e-9)
    return None


for band in (False, True):
    print(band, cross_age(band=band), cross_age(1.1, band=band),
          cross_age(lower=0.1, band=band))
# -&gt; False 69.7 123.7 129.7
# -&gt; True None None None</code></pre></div>
<p><b>Result:</b> the healthy safety factor is $S_0/F_\text{peak}=1.079$. With the band collapsed to one setpoint the bone tracks $Z_\text{eq}=M/(E\varepsilon^*)$ within days (Lemma 7.2), so the safety factor falls as $1.079/(1+0.002\,t)$ and crosses $1$ at age $69.7$; $+10\%$ load raises strength by $10.0\%$ and delays the crossing to $123.7$, while a $10\%$ lower setpoint raises it by $1/0.9-1=11.1\%$ and delays it to $129.7$, six years more for the same fractional change, because $\varepsilon^*$ enters inversely. With the lazy zone of (7.1) nothing happens: the bone rests at $1250\ \mu\varepsilon$, both edges drift upward, and the lower edge would need $125$ years to reach the operating strain, so the safety factor stays at $1.08$ for the whole sweep and for both interventions. The two models differ in kind, not degree. Under (7.1) an aging bone that once adapted upward rests at $\varepsilon_\text{hi}$ and is protected by the full width of the band; an age-related loss then needs the resorption threshold alone to rise, or the habitual load to fall (the extension challenge of <a class="secref" href="#lab">§8</a>). A prediction of fracture age is therefore only as good as the statement of where in the band the adult bone sits.</p></details></div>
```

### B12. K4's code models a different problem from its statement, with two unexplained constants, and "Miner's rule" is never defined

Location: `module02.html:701-717`.

Quoted (statement, line 701): "As weekly running mileage rises at rate $\rho$ (%/week), find the critical $\rho$ at which per-day microdamage first outpaces repair." Quoted (code, line 712): `sig = 60e6*(1 + 0.5*rate_pct/100*4)   # 4 weeks of ramp`.

Missing parts: (1) precise statement: more mileage means more loading cycles per day at the same stress, but the code holds cycles at 5000 per day and raises the stress amplitude by an unexplained factor $1+2\rho/100$. Under the module's own law (7.1) a change in cycle count does not change peak strain, so the bone does not adapt to mileage at all and the model can produce a critical mileage but not a critical rate. (2) terms: Miner's rule is named in the statement and never defined. (5) number class: 60 MPa, 5000 cycles per day, a 700-day repair time, and $C$ "tuned at 100 MPa" are bare. The mechanism that does produce a critical rate is the one K1 already computed: a ramp in the <em>load</em> lets $Z$ keep up, a step does not, and the fatigue exponent turns the strain overshoot into a damage overshoot. Replacement for K4 (lines 701 to 717); all constants go to the Appendix (B17).

```html
<div class="prob"><p><b>K4 (critical ramp rate from the damage-repair race).</b> Define fatigue damage by <em>Miner's rule</em>: each loading cycle at stress $\sigma$ adds $1/N_f(\sigma)$ to a damage variable $D$, where $N_f(\sigma)=N_\text{hab}(\sigma/\sigma_\text{hab})^{-m}$ is the S-N law of <a class="secref" href="#failure">§6</a> with $m=6$, and failure occurs at $D=1$. Let remodeling repair damage at a first-order rate $D/\tau_r$ with $\tau_r=14$ days, and let the habitual state ($\sigma_\text{hab}=E\times1250\ \mu\varepsilon$, $n_0=5000$ cycles per day) sit at a steady $D=0.25$; this fixes $N_\text{hab}=n_0\tau_r/0.25$. Now raise the running load by $60\%$ as a linear ramp over $T$ days while $Z$ evolves by (7.1) (the K1 integrator), and track $D(t)$. Find the ramp duration below which $D$ reaches $1$, and express it as a weekly percentage rate. Report how the answer moves with $\tau_r$. <span class="probes">Probes: a critical rate exists because adaptation (time constant $8$ days) and fatigue repair compete on the same timescale, and the steep S-N exponent turns a $33\%$ strain overshoot into a $17\times$ damage overshoot.</span></p>
<figure><!-- regenerate: peak D vs ramp duration (or rate in %/week) for tau_r = 14 d, with the D = 1 line; a second curve for tau_r = 7 d --><figcaption>Peak fatigue damage vs. load-ramp rate. A step ($D_\max=1.12$) and ramps faster than $7.2\%$ per week ($T\lt59$ days) reach $D=1$; slower ramps stay below it because $Z$ grows before the strain overshoot accumulates. With a $7$-day repair time the boundary moves to $6.1\%$ per week; with $30$ days or longer the peak never reaches $1$.</figcaption></figure>
<details class="sol"><summary>Show solution</summary>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np
from scipy.optimize import brentq
E, Z0, k = 17e9, 2.02e-6, 80.0
eps_lo, eps_hi = 1000e-6, 1500e-6
M_ref = 1250e-6*Z0*E
m_exp, n0, tau_r, D_hab = 6.0, 5000.0, 14.0, 0.25
sig_hab = 1250e-6*E
Nf_hab = n0*tau_r/D_hab               # Basquin anchor: habitual D = 0.25


def Nf(sig):
    return Nf_hab*(sig/sig_hab)**(-m_exp)


def rate(Z, M):
    e = M/(Z*E)
    if e &gt; eps_hi:
        return k*Z*(e - eps_hi)
    if e &lt; eps_lo:
        return k*Z*(e - eps_lo)
    return 0.0


def max_damage(ramp_days, load=1.6, days=400, dt=0.25):
    Z, D, Dmax = Z0, D_hab, D_hab
    for i in range(int(days/dt) + 1):
        frac = min(i*dt/ramp_days, 1.0) if ramp_days &gt; 0 else 1.0
        M = M_ref*(1 + (load - 1)*frac)
        D += (n0/Nf(M/Z) - D/tau_r)*dt   # Miner increment minus repair
        Dmax = max(Dmax, D)
        Z = max(Z + rate(Z, M)*dt, 1e-9)
    return Dmax


for rd in (0, 28, 56, 84):
    print(rd, round(max_damage(rd), 2))
rd_c = brentq(lambda rd: max_damage(rd) - 1.0, 1, 400)
print(round(rd_c, 1), round(60/rd_c*7, 1))
# -&gt; 0 1.12 / 28 1.09 / 56 1.01 / 84 0.94 ; critical 58.7 days = 7.2 %/week</code></pre></div>
<p><b>Result:</b> a step to $+60\%$ load drives peak strain to $2000\ \mu\varepsilon$ (K1), and by the S-N law the damage rate per cycle rises by $(2000/1250)^6=16.8\times$ while $Z$ takes about three time constants ($25$ days) to catch up; $D$ climbs from $0.25$ to a peak of $1.12$ and the bone fails. A ramp over $28$ days peaks at $1.09$, over $56$ days at $1.01$, and over $84$ days at $0.94$: the critical ramp is $58.7$ days, a rate of $7.2\%$ per week, close to the runners' "10 percent rule". The boundary is real but soft, and it depends on the repair time: with $\tau_r=7$ days it sits at $6.1\%$ per week, and with $\tau_r\ge30$ days the peak damage never reaches $1$ for any ramp, because slow repair averages over the overshoot. Two facts survive every choice of the assumed constants. First, after adaptation the bone rests at $\varepsilon_\text{hi}=1500\ \mu\varepsilon$, so its steady damage is $0.25\times(1500/1250)^6=0.75$, three times the old value: a bone that has adapted upward runs closer to its fatigue limit for good. Second, the sixth power makes the transient, not the destination, the danger, which is why the same total load is safe when it arrives slowly.</p></details></div>
```

### B13. Four computational problems are plug-in arithmetic: K5, K6, K7, K8

Test applied: does solving it surface anything the reader could not read straight off (3.1), (4.1), (6.1), Lemma 4.2, or the Voigt and Reuss formulas? K5 inverts one closed form. K6 (before B1) evaluates a monomial and root-finds it. K7 rearranges (6.1) once. K8 inverts two monotone functions. K1, K3, K9, K10 pass and stay; K2 and K4 pass after B11 and B12; K6 is replaced in B1. Replacements for K5, K7, K8 follow; every number was produced by the code shown (scratchpad `m02/newk.py`). Figures are to be regenerated from the code.

K5 becomes a map of the whole interaction locus against the component-wise rule.

```html
<div class="prob"><p><b>K5 (interaction locus vs. component-wise safety factors).</b> A twisting fall superposes a surface bending stress $\sigma_b$ and a torsional shear $\tau$. For that plane stress state the largest normal stress over all plane orientations is $\sigma_1=\tfrac{\sigma_b}{2}+\sqrt{(\sigma_b/2)^2+\tau^2}$ (the wedge balance of Lemma 4.2 carried out with the normal stress present; D7 states the general formula). Compute the yield locus $\sigma_1=130$ MPa in the $(\sigma_b,\tau)$ plane, then compare the true safety factor $130/\sigma_1$ with the component-wise rule $\min(130/\sigma_b,\,130/\tau)$ over the plane. Where is the component-wise rule most non-conservative, and by what factor? <span class="probes">Probes: stress interaction, why two individually safe loads combine to fail, and the size of the error a component-wise check makes.</span></p>
<figure><!-- regenerate: the yield locus in the (sigma_b, tau) plane, the component-wise square, and a shaded band where the ratio exceeds 1.5 --><figcaption>Yield locus $\sigma_1=130$ MPa (curve) against the component-wise box $\sigma_b\lt130$, $\tau\lt130$. Bending alone at $80$ MPa yields when $\tau=80.6$ MPa is added; along $\sigma_b=\tau$ the component-wise rule overstates the safety factor by the constant factor $1.618$.</figcaption></figure>
<details class="sol"><summary>Show solution</summary>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np
Y = 130e6


def sf_true(sb, tau):
    return Y/(sb/2 + np.sqrt((sb/2)**2 + tau**2))


def sf_comp(sb, tau):
    return min(Y/sb, Y/tau)


sb = np.linspace(0, Y, 1301)
tau_yield = np.sqrt((Y - sb/2)**2 - (sb/2)**2)     # locus sigma_1 = Y
print(round(np.interp(80e6, sb, tau_yield)/1e6, 1))  # -&gt; 80.6 at sb = 80
print(round(Y/(0.5 + np.sqrt(1.25))/1e6, 1))        # -&gt; 80.3 where sb = tau
grid = np.linspace(1e6, Y, 130)
ratio = max(sf_comp(s, t)/sf_true(s, t) for s in grid for t in grid)
print(round(ratio, 3), round(sf_comp(50e6, 50e6)/sf_true(50e6, 50e6), 3))
# -&gt; 1.618 1.618  (largest ratio, reached all along sb = tau)</code></pre></div>
<p><b>Result:</b> the locus is the curve $\tau=\sqrt{(Y-\sigma_b/2)^2-(\sigma_b/2)^2}$, which runs from $\tau=130$ MPa at pure torsion (where $\sigma_1=\tau$, Lemma 4.2) to $\tau=0$ at $\sigma_b=130$ MPa. Bending alone at $80$ MPa (safety factor $1.62$) yields once $\tau=80.6$ MPa is added, a torsion that alone would also have a factor $1.61$. The component-wise rule is exact on the two axes and wrong everywhere between them. Its error is largest along $\sigma_b=\tau$, where $\sigma_1=\sigma_b\,(\tfrac12+\sqrt{\tfrac54})=1.618\,\sigma_b$, so the rule overstates the safety factor by the golden ratio, $1.618$, at every load level on that line; the bone yields there at $\sigma_b=\tau=80.3$ MPa while the component-wise check reports a margin of $1.62$. A fall that both bends and twists, the common mechanism, is the case the component-wise check gets most wrong.</p></details></div>
```

K7 becomes an inverse design with the stroke constraint that the current solution ignores. Its present conclusion, "why they target stiffness, not thickness alone", is contradicted by its own model: at the required $k_s=1.46\times10^4$ N/m the compression is $x=2m_\text{eff}gh/F=0.137$ m, so a pad thinner than that bottoms out.

```html
<div class="prob"><p><b>K7 (inverse design with a stroke limit).</b> A hip protector must cap the fall force of (6.1) at the osteoporotic strength of $2$ kN. Invert (6.1) for the effective stiffness $k_s$ that achieves this, then compute the compression stroke $x=F_\text{peak}/k_s$ it needs. A pad of thickness $t_p$ cannot compress more than $t_p$: for $t_p=3$, $5$, and $10$ cm find the softest linear pad that does not bottom out and the force it transmits, and compare with an ideal crushable pad that holds a constant force over its whole stroke. What does force-limiting actually cost? <span class="probes">Probes: $F\propto\sqrt{k_s}$ as a design lever, and the energy identity force times stroke equals $m_\text{eff}gh$ that makes thickness, not stiffness, the binding constraint.</span></p>
<figure><!-- regenerate: transmitted force vs pad thickness for the linear and crushable pads, with the 2 kN line --><figcaption>Transmitted force vs. pad thickness. Capping at $2$ kN needs $k_s=1.46\times10^4$ N/m and a $13.7$ cm stroke for a linear pad, or $6.9$ cm for a crushable pad. A $3$ cm linear pad cannot go below $9.2$ kN; a $3$ cm crushable pad, $4.6$ kN.</figcaption></figure>
<details class="sol"><summary>Show solution</summary>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np
meff, h, g, ks = 28.0, 0.5, 9.81, 5e4
target = 2000.0
U = meff*g*h                              # 137 J
ks_need = target**2/(2*U)
print(round(ks_need), round(np.sqrt(2*U/ks_need), 3))   # -&gt; 14562 0.137
print(round(1/(1/ks_need - 1/ks)))                        # -&gt; 20547 pad alone
for tp in (0.03, 0.05, 0.10):
    print(tp, round(np.sqrt(2*(2*U/tp**2)*U)), round(U/tp))
# -&gt; 0.03 9156 4578 / 0.05 5494 2747 / 0.10 2747 1373  (N: linear, crushable)</code></pre></div>
<p><b>Result:</b> inverting (6.1), $k_s=F^2/(2m_\text{eff}gh)=1.46\times10^4$ N/m caps the force at $2$ kN, a softening of $3.4\times$ from the bare $5\times10^4$ N/m; because the pad and the tissue act in series, the pad alone must have $k_\text{pad}=2.05\times10^4$ N/m. But a linear spring stores $\tfrac12Fx$, so the stroke at that stiffness is $x=2m_\text{eff}gh/F=0.137$ m. No wearable pad is $14$ cm thick. For a pad of thickness $t_p$ the softest linear spring that does not bottom out has $k_s=2m_\text{eff}gh/t_p^2$ and transmits $F=2m_\text{eff}gh/t_p$: $9.2$ kN at $3$ cm, $5.5$ kN at $5$ cm, $2.7$ kN at $10$ cm, all above the osteoporotic strength. An ideal crushable pad, which holds a constant force over its whole stroke, stores $Fx$ and halves each of these ($4.6$, $2.7$, $1.4$ kN), reaching $2$ kN at $6.9$ cm. The energy identity is the whole design: the $137$ J must be absorbed as force times stroke, so a force cap fixes a minimum stroke, and stiffness is only the means of using it. Real protectors therefore work by crushing (energy-absorbing foam), not by being soft.</p></details></div>
```

K8 becomes an identifiability problem: one modulus cannot pin two microstructural parameters.

```html
<div class="prob"><p><b>K8 (inverse microstructure and its identifiability).</b> The Voigt and Reuss bounds of <a class="secref" href="#composite">§5</a> bracket $E$ for a given mineral fraction $v_m$. Invert each bound for the $v_m$ that reproduces the measured $17$ GPa. Then adopt the two-parameter model $E=\eta\,v_mE_m+(1-v_m)E_c$, where $\eta\in[0,1]$ is the fraction of the mineral's stiffness that a discontinuous platelet architecture can recruit in parallel ($\eta=1$ is Voigt). Show that the single measurement $E=17$ GPa fixes only a curve in the $(v_m,\eta)$ plane, evaluate $\eta$ at $v_m=0.5$, and compute the sensitivity of $E$ to a $10\%$ loss of mineral on that model. <span class="probes">Probes: a bound is not a model; one measurement cannot identify two parameters, and the recruited-stiffness reading of "between the bounds" gives a number a demineralisation model can use.</span></p>
<figure><!-- regenerate: the curve eta(v_m) for E = 17 GPa from v_m = 0.3 to 0.7, with the two single-bound solutions marked at the ends --><figcaption>Every $(v_m,\eta)$ on the curve gives $E=17$ GPa: $\eta=0.54$ at $v_m=0.3$, $0.33$ at $0.5$, $0.24$ at $0.7$. Voigt alone ($\eta=1$) needs $v_m=0.16$; Reuss alone needs $0.95$.</figcaption></figure>
<details class="sol"><summary>Show solution</summary>
<div class="codewrap"><button class="copybtn" type="button" onclick="copyCode(this)" aria-label="Copy code to clipboard"><span>Copy</span></button><pre><code>import numpy as np
Em, Ec, E = 100.0, 1.0, 17.0
v_voigt = (E - Ec)/(Em - Ec)
v_reuss = (1 - Ec/E)/(1 - Ec/Em)
print(round(v_voigt, 2), round(v_reuss, 2))          # -&gt; 0.16 0.95
for v in (0.3, 0.4, 0.5, 0.6, 0.7):
    print(v, round((E - (1 - v)*Ec)/(v*Em), 3))      # eta(v) on E = 17
eta = (E - 0.5*Ec)/(0.5*Em)
print(eta, eta*Em - Ec, round(100*(eta*Em - Ec)*0.05/E, 1))
# -&gt; 0.33 32.0 9.4   (dE/dv in GPa; 10 % demineralisation costs 9.4 % of E)</code></pre></div>
<p><b>Result:</b> the Voigt bound reaches $17$ GPa at $v_m=(17-1)/(100-1)=0.16$ and the Reuss bound at $v_m=(1-1/17)/(1-1/100)=0.95$; neither is the $\sim0.5$ of real bone, so neither bound is a model of it. The two-parameter model gives $\eta=(E-(1-v_m)E_c)/(v_mE_m)$, a curve: $\eta=0.54$, $0.41$, $0.33$, $0.28$, $0.24$ at $v_m=0.3$, $0.4$, $0.5$, $0.6$, $0.7$. One modulus measurement cannot separate how much mineral there is from how well it is recruited; a second measurement (the mineral fraction from density or ash weight) is needed to fix $\eta=0.33$ at $v_m=0.5$, meaning platelets deliver a third of their parallel stiffness. On that model $dE/dv_m=\eta E_m-E_c=32$ GPa per unit fraction, so a $10\%$ loss of mineral ($v_m$ from $0.50$ to $0.45$) costs $1.6$ GPa, $9.4\%$ of $E$, at fixed architecture. The inverse read of the bounds recovers not a microstructure but a one-parameter family of them.</p></details></div>
```

### B14. K9 presents synthetic data as measurements

Location: `module02.html:782` and `module02.html:819`.

Quoted: "Given noisy serial DXA measurements of section modulus during bed rest" and "from $2\%$-noise DXA points the fit recovers gain $k\approx57$ (true $60$)".

Missing part: number class. The brief states the course has no laboratory measurements; the code at line 810 generates the "data" from (7.1) with $k=60$, load fraction $0.5$, and $2\%$ Gaussian noise. Replacement for the opening of line 782: "Generate synthetic bed-rest data by integrating (7.1) with $k=60$ and a disuse load fraction of $0.5$, sampling every $20$ days for $300$ days and adding $2\%$ Gaussian noise (the precision a serial DXA scan might reach). Then, treating $k$ and the load fraction as unknown, recover them by least-squares fitting the ODE trajectory to the samples." Replacement for the opening of line 819: "<b>Result:</b> from the $2\%$-noise synthetic points the fit recovers".

### B15. Two figure cross-references point to the wrong figure, and D5 draws its moments as forces

Location: `module02.html:233`, `module02.html:307`, `module02.html:593`.

Quoted (line 233): "Bending loads one face in tension and the opposite face in equal-magnitude compression (Fig. 1)." Fig. 1 is the femur anatomy figure at line 96; the bending setup is Fig. 2 (line 191) and the animation is Fig. 4. Quoted (line 307): "the classic <em>spiral fracture</em> (Fig. 4)". Fig. 4 is the bending animation; the torsion figure at line 309 is Fig. 5. Replacements: line 233 "(Fig. 1)" to "(Fig. 2)"; line 307 "(Fig. 4)" to "(Fig. 5)". The figure counter renumbers on every insertion, so re-check both after B3 and B8 land.

D5's figure (line 593) labels two downward force arrows "$M$". A moment is a couple, not a force; two downward arrows at the ends read as a two-point load. Replace the two `<line … marker-end="url(#a_red)"/>` elements with curved moment arrows: `<path d="M48,40 A16,16 0 0 1 72,52" fill="none" stroke="#7a1f1f" stroke-width="2" marker-end="url(#a_red)"/>` at the left end and `<path d="M252,40 A16,16 0 0 0 228,52" fill="none" stroke="#7a1f1f" stroke-width="2" marker-end="url(#a_red)"/>` at the right, and change the caption to "A beam bent by equal and opposite end moments $M$ into an arc of radius $1/\kappa$; the curvature is $\kappa=M/(EI)$, and the bending stiffness $EI$ scales as $\lambda^4$ with size." Run `check_overlap.py` after the change.

### B16. The Appendix has no notation table

Location: `module02.html:848-859`.

Quoted: the Appendix holds one eight-row parameter table and no list of symbols. The brief requires every symbol in the text to appear in a notation table. Insert after line 848, before the parameter table (this table also records the symbol changes of B18):

```html
<h3>Notation</h3>
<table>
<tr><th>Symbol</th><th>Meaning</th><th>Unit</th><th>First used</th></tr>
<tr><td>$\sigma$, $\sigma_\text{axial}$, $\sigma_\max$, $\sigma(y)$</td><td>normal stress; under axial load; at the outer fibre; at distance $y$</td><td>Pa</td><td><a href="#setup">§1</a></td></tr>
<tr><td>$\tau$, $\tau(\rho)$, $\tau_\max$</td><td>shear stress; at radius $\rho$; at the surface</td><td>Pa</td><td><a href="#setup">§1</a></td></tr>
<tr><td>$\varepsilon$, $\gamma$</td><td>normal strain; shear strain</td><td>1 (µε = $10^{-6}$)</td><td><a href="#setup">§1</a>, <a href="#torsion">§4</a></td></tr>
<tr><td>$E$, $G$</td><td>Young's modulus; shear modulus</td><td>Pa</td><td><a href="#setup">§1</a>, <a href="#torsion">§4</a></td></tr>
<tr><td>$F$, $A$</td><td>axial force; cross-sectional area</td><td>N, m²</td><td><a href="#axial">§2</a></td></tr>
<tr><td>$R$, $r$, $\beta=r/R$, $a$</td><td>outer and inner radius of the tube; bore ratio; radius of the equal-area solid rod</td><td>m, m, 1, m</td><td><a href="#axial">§2</a>, <a href="#bending">§3</a></td></tr>
<tr><td>$n$, $\sigma_f$, $\sigma_c$, $\sigma_Y$, $\tau_f$</td><td>safety factor; failure stress in a given sense; compressive strength; tensile yield strength; shear strength</td><td>1, Pa</td><td><a href="#axial">§2</a>, <a href="#failure">§6</a></td></tr>
<tr><td>$M$, $M_\text{ref}$, $e$</td><td>bending moment in the shaft; its habitual value; offset of the joint force line from the shaft axis</td><td>N m, N m, m</td><td><a href="#bending">§3</a></td></tr>
<tr><td>$y$, $c$, $I$, $Z$</td><td>distance from the neutral axis; distance to the outermost fibre; second moment of area; section modulus $I/c$</td><td>m, m, m⁴, m³</td><td><a href="#bending">§3</a></td></tr>
<tr><td>$\kappa$, $R_\kappa=1/\kappa$</td><td>curvature; radius of curvature (D5)</td><td>m⁻¹, m</td><td><a href="#bending">§3</a></td></tr>
<tr><td>$T$, $\varphi$, $\vartheta=d\varphi/dz$, $\rho$, $J$, $L$</td><td>torque; angle of twist; rate of twist; radius from the axis; polar second moment of area; shaft or bar length</td><td>N m, rad, rad m⁻¹, m, m⁴, m</td><td><a href="#torsion">§4</a></td></tr>
<tr><td>$\sigma_1$, $\sigma_2$, $\sigma_n(\theta)$, $\sigma_x,\sigma_y,\tau_{xy}$</td><td>principal stresses; normal stress on a plane at angle $\theta$; plane-stress components (D7)</td><td>Pa</td><td><a href="#torsion">§4</a></td></tr>
<tr><td>$E_m$, $E_c$, $v_m$, $E_V$, $E_R$, $\eta$</td><td>mineral and collagen moduli; mineral volume fraction; Voigt and Reuss bounds; recruited-stiffness fraction (K8)</td><td>Pa, Pa, 1, Pa, Pa, 1</td><td><a href="#composite">§5</a></td></tr>
<tr><td>$K_t$, $\sigma_\text{nom}$, $\sigma_\text{local}$</td><td>stress-concentration factor; nominal and local stress at a notch</td><td>1, Pa</td><td><a href="#failure">§6</a></td></tr>
<tr><td>$N_f$, $N_\text{hab}$, $\Delta\sigma$, $m$, $D$, $n_0$, $\tau_r$</td><td>cycles to failure; its habitual anchor; stress range; S-N exponent; Miner damage; cycles per day; repair time (K4)</td><td>1, 1, Pa, 1, 1, day⁻¹, day</td><td><a href="#failure">§6</a></td></tr>
<tr><td>$K$, $K_{Ic}$, $Y_g$, $a_\text{crack}$</td><td>stress intensity; fracture toughness; crack-geometry factor; crack length</td><td>Pa√m, Pa√m, 1, m</td><td><a href="#failure">§6</a></td></tr>
<tr><td>$m_\text{eff}$, $h$, $k_s$, $x$, $F_\text{peak}$, $U$</td><td>effective falling mass; drop height; landing stiffness; compression stroke; peak impact force; impact energy $m_\text{eff}gh$</td><td>kg, m, N m⁻¹, m, N, J</td><td><a href="#failure">§6</a></td></tr>
<tr><td>$t_p$, $k_\text{pad}$</td><td>hip-pad thickness and stiffness (K7)</td><td>m, N m⁻¹</td><td>K7</td></tr>
<tr><td>$\varepsilon_\text{lo}$, $\varepsilon_\text{hi}$, $\varepsilon^*$, $k$, $Z_\text{eq}$, $\tau_Z$</td><td>mechanostat thresholds; collapsed setpoint; remodeling gain; equilibrium section modulus; adaptation time constant $1/(k\varepsilon)$</td><td>1, 1, 1, (strain·day)⁻¹, m³, day</td><td><a href="#adapt">§7</a></td></tr>
<tr><td>$S$, $S_0$</td><td>hip strength and its value at $Z_0$ (K2)</td><td>N</td><td>K2</td></tr>
<tr><td>$M_b$, $\lambda$, $L$, $d$, $p$</td><td>body mass; linear scale factor; bone length and diameter; scaling exponent (C9, D5, K6)</td><td>kg, 1, m, m, 1</td><td>C9</td></tr>
<tr><td>$b$, $h_\text{sec}$</td><td>width and height of the rectangular section (D1)</td><td>m</td><td>D1</td></tr>
<tr><td>$t$, $t_\text{min}$</td><td>wall thickness and its floor (K3)</td><td>m</td><td>K3</td></tr>
<tr><td>$P$, $w(x)$</td><td>tip load and deflection of the cantilever (K10)</td><td>N, m</td><td>K10</td></tr>
</table>
<p class="small">Module&nbsp;1 uses $M$ for the total body mass and $\lVert\mathbf M\rVert$ for a moment; this module reserves $M$ for the bending moment and writes body mass as $M_b$ (K6) or as the numeral $70$ kg.</p>
```

### B17. Roughly twenty empirical numbers used in the text are in no table

Location: `module02.html:170` (trabecular $E$), `179` ($2.5\times$ body weight, $170$ MPa), `233` ($170$, $130$ MPa), `262` ($200$ N m), `296` ($G=3.3$ GPa), `311` ($30$ and $150$ N m, $0.40$ m, $65$ MPa, $140$ to $180$ N m), `315`, `318`, `319`, `322` ($E_m$, $E_c$, $50\%$, $40\%$ volume), `330` ($m=5$ to $8$), `337` ($4$ and $2$ kN), `536` ($K_t=2$ to $3$), `657` ($0.2\%$ per year), `683` ($t_\text{min}=3$ mm), `712` (K4 constants), `753` ($50$ MPa), `810` ($2\%$ noise), `821` ($P=500$ N).

Missing part: the brief's number classes. None of these is derived, tabulated, or labelled "assume". The "Frost mechanostat" note in the existing table is a citation with no page and is unverified (no PDF in the repo); it must not be extended from memory. Replacement for the parameter table (lines 849 to 859):

```html
<h3>Parameters</h3>
<table>
<tr><th>Quantity</th><th>Symbol</th><th>Value</th><th>Class / note</th></tr>
<tr><td>Body mass (reference human, Module 1)</td><td>$70$ kg</td><td>$70\ \mathrm{kg}$</td><td>assumed (Module 1 Appendix)</td></tr>
<tr><td>Gravitational field</td><td>$g$</td><td>$9.81\ \mathrm{m\,s^{-2}}$</td><td>constant</td></tr>
<tr><td>Single-leg-stance femoral load</td><td>$F$</td><td>$2.5\times$ body weight $=1717\ \mathrm N$</td><td>assumed here; derived in Module 3 §4</td></tr>
<tr><td>Femoral outer radius (midshaft)</td><td>$R$</td><td>$0.014\ \mathrm m$</td><td>assumed typical adult</td></tr>
<tr><td>Femoral inner radius (canal)</td><td>$r$</td><td>$0.007\ \mathrm m$</td><td>assumed, $R/r=2$</td></tr>
<tr><td>Shaft length (torsion, cantilever)</td><td>$L$</td><td>$0.40\ \mathrm m$</td><td>assumed</td></tr>
<tr><td>Cross-sectional area, $I$, $Z$, $J$</td><td>$A$, $I$, $Z$, $J$</td><td>$4.62\times10^{-4}\ \mathrm m^2$, $2.83\times10^{-8}\ \mathrm m^4$, $2.02\times10^{-6}\ \mathrm m^3$, $5.66\times10^{-8}\ \mathrm m^4$</td><td>derived from $R$, $r$</td></tr>
<tr><td>Cortical Young's modulus (longitudinal)</td><td>$E$</td><td>$17\ \mathrm{GPa}$</td><td>parameter (typical value; no source verified)</td></tr>
<tr><td>Trabecular Young's modulus</td><td>(none)</td><td>$0.1$ to $2\ \mathrm{GPa}$</td><td>assumed range, illustrative only</td></tr>
<tr><td>Cortical shear modulus</td><td>$G$</td><td>$3.3\ \mathrm{GPa}$ ($\approx E/5$)</td><td>assumed</td></tr>
<tr><td>Tensile yield strength (working value)</td><td>$\sigma_Y$</td><td>$130\ \mathrm{MPa}$ (range $120$ to $150$)</td><td>assumed; every safety factor uses $130$</td></tr>
<tr><td>Compressive strength</td><td>$\sigma_c$</td><td>$170\ \mathrm{MPa}$</td><td>assumed</td></tr>
<tr><td>Shear (torsional) strength</td><td>$\tau_f$</td><td>$65\ \mathrm{MPa}$</td><td>assumed</td></tr>
<tr><td>Real-femur torsional failure torque</td><td>(none)</td><td>$140$ to $180\ \mathrm{N\,m}$</td><td>assumed range; the tube model gives $263$</td></tr>
<tr><td>Fracture toughness</td><td>$K_{Ic}$</td><td>$2$ to $6\ \mathrm{MPa\sqrt m}$</td><td>assumed range</td></tr>
<tr><td>S-N exponent</td><td>$m$</td><td>$6$ (range $5$ to $8$)</td><td>assumed</td></tr>
<tr><td>Stress-concentration factor, circular hole</td><td>$K_t$</td><td>$2$ to $3$</td><td>assumed (C5)</td></tr>
<tr><td>Habitual bending moment (gait)</td><td>$M_\text{ref}$</td><td>$43\ \mathrm{N\,m}$ ($1250\ \mu\varepsilon$, $21$ MPa)</td><td>derived from the mid-band strain</td></tr>
<tr><td>Running-level peak bending stress (K6 anchor)</td><td>$\sigma_{70}$</td><td>$50\ \mathrm{MPa}$</td><td>assumed</td></tr>
<tr><td>Vigorous-activity bending moment</td><td>$M$</td><td>$200\ \mathrm{N\,m}$ ($99$ MPa)</td><td>assumed</td></tr>
<tr><td>Everyday and violent torsional torque</td><td>$T$</td><td>$30$, $150\ \mathrm{N\,m}$</td><td>assumed</td></tr>
<tr><td>Mineral and collagen moduli</td><td>$E_m$, $E_c$</td><td>$100$, $1\ \mathrm{GPa}$</td><td>assumed</td></tr>
<tr><td>Mineral and collagen volume fractions</td><td>$v_m$, $1-v_m$</td><td>$\approx0.5$, $\approx0.4$ (rest water and proteins)</td><td>assumed</td></tr>
<tr><td>Mechanostat strain band</td><td>$\varepsilon_\text{lo}$, $\varepsilon_\text{hi}$</td><td>$1000$, $1500\ \mu\varepsilon$</td><td>assumed (Frost's mechanostat; citation unverified)</td></tr>
<tr><td>Remodeling gain</td><td>$k$</td><td>$80\ \mathrm{(strain\cdot day)^{-1}}$</td><td>toy value; sets speed only ($\tau_Z=8.3$, $12.5$ days)</td></tr>
<tr><td>Setpoint drift with age (K2)</td><td>(none)</td><td>$0.2\%$ per year</td><td>assumed</td></tr>
<tr><td>Fall effective mass, height, landing stiffness</td><td>$m_\text{eff}$, $h$, $k_s$</td><td>$28\ \mathrm{kg}$, $0.5\ \mathrm m$, $5\times10^4\ \mathrm{N\,m^{-1}}$</td><td>assumed (sideways fall)</td></tr>
<tr><td>Proximal-femur strength, healthy and osteoporotic</td><td>$S_0$, (none)</td><td>$4$, $2\ \mathrm{kN}$</td><td>assumed</td></tr>
<tr><td>Wall-thickness floor (K3)</td><td>$t_\text{min}$</td><td>$3\ \mathrm{mm}$</td><td>assumed</td></tr>
<tr><td>Fatigue race constants (K4)</td><td>$n_0$, $\tau_r$, $D_\text{hab}$</td><td>$5000$ cycles/day, $14$ days, $0.25$</td><td>assumed; sensitivity to $\tau_r$ reported in K4</td></tr>
<tr><td>Cantilever tip load (K10)</td><td>$P$</td><td>$500\ \mathrm N$</td><td>assumed</td></tr>
<tr><td>Synthetic DXA noise (K9)</td><td>(none)</td><td>$2\%$</td><td>assumed</td></tr>
</table>
```

### B18. Symbol collisions

Location and replacement, cheapest touchpoints:

- $a$: solid-rod radius (`224-230`, D4 `585-590`) against crack length (`331`). Rename the crack length: line 331 "A crack of length $a$ fails when the stress intensity $K=Y\sigma\sqrt{\pi a}$" to "A crack of length $a_\text{crack}$ fails when the stress intensity $K=Y_g\,\sigma\sqrt{\pi a_\text{crack}}$, with $Y_g$ a dimensionless factor of order $1$ set by the crack and specimen geometry,". ($Y$ is also undefined at present; this defines it.)
- $\theta$: rate of twist (`296`, `302-304`, D6 `600`) against the plane angle of D7 (`602-605`). Rename the rate of twist $\vartheta$ in Definition 4.1, Proposition 4.1's proof, and D6.
- $\tau$: shear stress everywhere against the time constant in D8 (`610`, "time constant $\tau=1/(k\varepsilon_\text{hi})$"). Write $\tau_Z$ for the time constant in D8 and in the B2 caption.
- $\rho$: radius from the axis (§4) against the radius of curvature in D5's figure and caption (`593`, "ρ=1/κ") and the mileage rate in K4 (`701`). Write $R_\kappa=1/\kappa$ in D5 (SVG label `R_κ=1/κ` with the entity for the subscript) and drop $\rho$ from K4 (B12 does).
- $h$: fall height (§6) against the rectangle height in D1 (`564-569`). Rename D1's height $h_\text{sec}$ in the statement, the SVG label, and the solution ($I=bh_\text{sec}^3/12$).
- $M$: bending moment everywhere against body mass in K6 (`731`, "$\propto M^{1/3}$"). B1's K6 uses $M_b$.
- $y$: distance from the neutral axis (§3) against the cantilever deflection in K10 (`821`, "$EI\,y''=M(x)$"). Write $EI\,w''(x)=M(x)$ with $w$ the deflection.
- $\beta$: bore ratio here, trunk flexion angle in Module 1. Different modules, so allowed, but the notation table (B16) should say so in its footnote: "Module 1 uses $\beta$ for the trunk flexion angle."
- $L$: bar length (Definition 1.2), shaft length (§4), cantilever length (K10, `Lb` in code). One meaning, "the length of the member", is fine; say so once in Definition 1.2.

### B19. Anatomical and biological terms used before they are glossed

Location and replacement, each in the sentence of first use:

- `module02.html:156` (Fig. 1 caption): "head, greater trochanter (GT), and distal condyles" to "head (the ball that sits in the hip socket), neck (the short angled segment joining the head to the shaft), greater trochanter (GT, the bony bump on the outer upper shaft where the hip abductor muscles attach), and distal condyles (the two rounded knuckles at the knee end)".
- `module02.html:176`: "(the medullary canal is the hole)" to "(the medullary canal, the marrow-filled cavity along the shaft, is the hole)".
- `module02.html:337`: "A healthy proximal femur" to "A healthy proximal femur (the upper end of the thigh bone: head, neck, and trochanters)" (B3's replacement includes this).
- `module02.html:369-370`: "<b>Osteocytes</b> — the sensor network buried in the matrix" to "<b>Osteocytes</b>, the bone cells sealed inside the mineralized matrix that act as its sensor network,"; "suppresses sclerostin, releasing the brake on osteoblasts" to "suppresses sclerostin (a protein the osteocytes secrete that inhibits bone formation), releasing the brake on osteoblasts (the cells that lay down new bone)"; "raises the RANKL/OPG ratio, activating osteoclasts" to "raises the ratio of RANKL to OPG (two signalling proteins: RANKL recruits bone-removing cells, OPG blocks that recruitment), activating osteoclasts (the cells that dissolve bone)".
- `module02.html:490`: "Hormones (estrogen, PTH)" to "Hormones (estrogen; PTH, parathyroid hormone, which raises bone turnover)".
- `module02.html:492`: "DXA (dual-energy X-ray absorptiometry)/pQCT" to "DXA (dual-energy X-ray absorptiometry, the standard clinical bone-density scan) or pQCT (peripheral quantitative computed tomography, a limb CT that resolves cortical geometry)".
- `module02.html:523` (C3): "bends the femoral neck" to "bends the femoral neck (the short angled segment between the head and the shaft, Fig. 1)".
- `module02.html:528` (C4): "twists the tibia to failure" to "twists the tibia (the shin bone) to failure".
- `module02.html:533` (C5): "leaves a cortex" to "leaves a cortex (the dense outer wall of the bone)". Same gloss at K10 line 844 "Thinning the cortex".
- `module02.html:546` (C7): "an anti-resorptive" to "an anti-resorptive (a drug that slows osteoclast bone removal)".
- `module02.html:559` (C10 caption): "the neck and acetabulum" to "the neck and acetabulum (the cup-shaped hip socket in the pelvis)".
- `module02.html:701` (K4): "Miner's rule" is defined in B12's replacement.
- `module02.html:307`, `602`: "Mohr's circle" is removed by B8.

### B20. §0 names the phenomenon but not the model level; §9 does not say what the reader can now do

Location: `module02.html:94-158` and `module02.html:492`.

Missing part: the brief's page shape (level stated, closing capability). Insert after line 158:

```html
<p>The models here sit on two rungs of the course's level ladder. <a class="secref" href="#setup">§1</a> to <a class="secref" href="#failure">§6</a> are <b>Level 0</b> (scalar stress and strain estimates) built on <b>Level 1</b> static loads: every load is a fixed force or moment, and every result is an elastic stress compared with a strength. <a class="secref" href="#adapt">§7</a> and <a class="secref" href="#lab">§8</a> are a scalar version of <b>Level 10</b>, a mechanobiological adaptation law, with one state variable $Z$ in place of a tissue field. Nothing here is dynamic: the fall of <a class="secref" href="#failure">§6</a> is an energy balance, not an impact simulation.</p>
```

Insert after line 492, at the end of §9:

```html
<p><b>What you can now do.</b> Given a bone's outer and inner radius, compute its area, second moment, section modulus, and polar moment; turn an axial force, a bending moment, or a torque into a peak stress by (2.1), (3.1), and (4.1), and compare it with the right strength (tensile for bending and torsion, by Lemma 4.2); rank two sections of equal mass by Proposition 3.3; estimate a fall's peak force from an energy balance and know what that balance drops; and integrate the remodeling law (7.1) to predict how a change in habitual load moves the section modulus and how fast, with Lemma 7.2 telling you where it stops. You can also say which of these numbers rests on an assumption (the Appendix marks each) and which follows from the boxed results.</p>
```

### B21. §5 contradicts itself on where 17 GPa sits, and "yield" and "ultimate" are used for one number

Location: `module02.html:315` against `module02.html:322`; `module02.html:329` against `module02.html:249` and `854`.

Quoted (line 315): "its modulus lies between the two, near a volume-fraction average". Quoted (line 322): "The measured $17\ \mathrm{GPa}$ sits comfortably inside — nearer the Reuss floor". The volume-fraction average is the Voigt bound, 50 GPa; 17 GPa is far from it and 2 GPa is the Reuss floor. Replacement for the clause at line 315: "its modulus lies between the two, far below the volume-fraction average because the stiff phase is discontinuous (quantified below and in K8),".

Quoted (line 329): "exceeds the yield/ultimate strength $\sigma_Y\ (\sim120$–$150$ MPa in tension), the bone yields then breaks". The §3 plot labels the line "yield ≈130 MPa" and the table row says "Tensile yield strength". Pick one: replacement "exceeds the tensile yield strength $\sigma_Y=130$ MPa (Appendix; cortical bone has little ductility, so its ultimate strength is only slightly higher and this module does not distinguish them), the bone yields and then breaks".

### B22. C1(c) needs unstated knowledge

Location: `module02.html:513-516`.

Quoted: "Rank them for … (c) resistance to local buckling of the wall." Buckling is not defined anywhere in the module; the solution introduces it. Replacement for part (c) of the statement: "(c) resistance to local buckling of the wall, that is, the sideways collapse of a thin compressed wall before the material itself yields (not treated in this module; reason from the geometry alone)".

## 3. Style and clarity edits

Apply in one pass.

1. `module02.html:94` "The same femur routinely survives gait forces of several times body weight, millions of cycles per year, with a large margin to spare — yet" to "The same femur carries gait forces of two to three times body weight, about a million cycles a year, with a large margin in compression; yet". (B7 supplies the 78 kN that makes "tonnes" in the title honest.)
2. `module02.html:156` caption "A real femur is not a capsule. Left: …" to "Left: …". Delete "— the landmarks that matter for bending, torsion, and fall fracture" and write "These landmarks set the lever arms for bending (§3), torsion (§4), and the fall (§6)." Commentary on the drawing style belongs in the attribution note, not the caption.
3. `module02.html:157` "Geometry heroes use typical adult dimensions" to "The drawn outlines use assumed adult dimensions".
4. `module02.html:172` "the rest of the module is bookkeeping of where in a loaded bone $\sigma$ is largest" to "the rest of the module asks where in a loaded bone $\sigma$ is largest".
5. `module02.html:179` "$F\approx 2.5\times70\times9.81\approx 1715\ \mathrm N$": the product is $1717$ N (B7's replacement writes it).
6. `module02.html:216` "which is precisely the definition of the <em>centroid</em>" to "which is the definition of the <em>centroid</em>" (delete "precisely"; also delete "exactly" at `304`, "perfectly" at `294`, "comfortably" at `322`, "precisely" at `521`, "simply" at `553`, "far more" at `729`).
7. `module02.html:222` "The hollow bone is $\sim44\%$ stronger in bending at no extra mass — the engineering reason long bones are tubes." to "The hollow bone is $44\%$ stronger in bending at no extra mass. That is the engineering reason long bones are tubes."
8. `module02.html:233` "and why the safety factor of $\sim1.3$ — not $\sim1.8$ — is the honest one" to "and why the safety factor is $1.3$ (tensile), not $1.7$ (compressive)". The compressive value is $170/99=1.72$, not $1.8$.
9. `module02.html:294` "A planted foot while the trunk rotates — a ski catching an edge, a tackle, a stumble with a fixed shoe — applies" to "A planted foot while the trunk rotates (a ski catching an edge, a tackle, a stumble with a fixed shoe) applies".
10. `module02.html:309` caption "Geometry uses an anatomic lateral outline (neck-shaft ≈125°), not a featureless capsule." Delete; it is commentary on the drawing.
11. `module02.html:311` "this idealized stout tube — real femora, with thinner cortices, fail nearer $140$–$180\ \mathrm{N\,m}$, so" to "this idealized stout tube; femora with thinner cortices are assumed to fail nearer $140$ to $180\ \mathrm{N\,m}$ (Appendix), so" (B8 rewrites the clause that follows).
12. `module02.html:399` "<em>The bone chases a target strain, not a target size.</em>" moves into the paragraph after Lemma 7.2 (B9).
13. `module02.html:444` "Output (computed): increased load drives a $+33\%$ gain, disuse a $-50\%$ loss, habitual load is a stable equilibrium — all from the single law (7.1)." to "Output (computed): the load increase settles at $+33\%$ ($1.6\times1250/1500$), disuse at $-50\%$ ($0.4\times1250/1000$), and the habitual case does not move, all from the single law (7.1) and Lemma 7.2."
14. `module02.html:477` "a drugs/aging-driven rise in the setpoint" to "a rise in the setpoint driven by drugs or aging".
15. `module02.html:507` diagnostic 4, "Duration is irrelevant" is corrected in B3.
16. `module02.html:559` C10 caption "Drawing the head as a sphere without the neck and acetabulum hides why orientation matters for fall fracture." Delete; commentary on the drawing.
17. `module02.html:623` "never substitution into a boxed formula" is false for K5 to K8 as they stand; after B1, B12, B13 it becomes true, so keep the sentence and make it so.
18. `module02.html:753` "$\boxed{\sim\!1230\ \text{kg}}$": no box on a problem-solution number; the box is for stated results (B1's replacement removes it).
19. `module02.html:766` "This is exactly how energy-absorbing hip protectors and compliant flooring work, and why they target stiffness, not thickness alone." Replaced in B13 (the claim is contradicted by the model).
20. Aria-labels at `514`, `519`, `524`, `529`, `534`, `539`, `544`, `549`, `554`, `559`, `565`, `572`, `579`, `586`, `593`, `598`, `603`, `608`, `613`, `618` are adequate one-clause descriptions and stay; the §3 plot (`236`), the animation (`267`), the fall bar chart (`340`), and the lab plot (`447`) lack `class="setupfig"`, so `check_overlap.py` does not inspect them. Add the class so the gate covers them.

## 4. Structural notes

- Ordering. Dependencies now point backward except for three places: §2 to Module 3 (B7), §4 to D7 (B8), and §7 to D8 (B9). After those three fixes every result used in the prose is proved before it is used, and the problem set only reproduces.
- §6 is the weakest section. It lists three failure routes in one paragraph each, with the S-N law, $K_t$, and the stress-intensity criterion each stated in one sentence and none derived or tied to a number except through problems. That is acceptable for the fatigue and fracture-mechanics routes, which the module does not build, if the section says so: add one sentence after line 331, "Routes (ii) and (iii) are stated here as named empirical laws with their parameters in the Appendix; the module builds neither. Route (i) and the fall model below are the ones it derives." The fall model then gets Proposition 6.1 (B3) and the section has the shape of §3 and §4.
- §7 is a bulleted list of cell biology followed by a boxed model. The biology is fine as motivation but it is the only place in the module where the brief's "cellular substrate" step appears, and none of the three bullets carries a number or a testable statement. Keep it, but add Lemma 7.2 (B9) so the section has one proved result.
- The lab is short: one figure, one paragraph of output, one sensitivity paragraph. It is correct after B2. Consider adding one line to the code that prints the two time constants, so the caption's numbers are visible in the output.
- The problem set. Every problem has a figure, a probes note, and a solution, as the convention requires. After the replacements the K set covers ODE integration with transients (K1, K4), regime comparison (K2, K5, K6), constrained optimization (K3), inverse design with a constraint (K7), identifiability (K8), parameter identification (K9), and numerical integration with a sensitivity sweep (K10).
- Cross-references inside the set (C6 to K4, C7 to K2, C9 to K6, D5 to K6, D9 to K8, D10 to K7) are forward within the problem set only; acceptable.
- The reference human and the femur recur from Module 1 as the brief requires; no new toy body is introduced. The one scenario the module introduces, the sideways fall, is the one Modules 14 and 17 reuse, and its four parameters are now in the table.
- Figures. Commit `3fd6fbe` scaled the two mechanostat plateaus to 36 and 18 px (B5). The same commit produced the module's anatomy figures, which render well. Add a gate: a stroke width above 8 on any `<line>` that is not a beam body should fail `check_svg.py`.

## 5. What already works

- Theorem 3.2 (`module02.html:187-219`) is proved the way the brief asks: the neutral-axis location is derived from the zero-force condition rather than assumed, the moment integral is written out, and the setup figure sits inside the proof. D2 then asks the reader to reproduce the centroid step.
- Proposition 3.3 (`module02.html:222-231`) carries the full algebra of the equal-area comparison, states the limit case ("grows without bound as $\beta\to1$"), and D4 reproduces it; C1 supplies the buckling caveat. That is rigor parity.
- Proposition 4.1 (`module02.html:298-305`) runs the torsion derivation in exact parallel with the bending one, and D3 and D6 exploit the parallel ($J=2I$, $\theta/\kappa=E/2G$). The "why 45°" paragraph is the right explanation once Lemma 4.2 (B8) backs it.
- The lab code (`module02.html:404-443`) is PEP8, prints what the prose claims ($+33\%$, $-50\%$, stable habitual), and the plotted polylines match the integration to the pixel ($121.4\%$ on day 8, $132.8\%$ on day 32).
- All ten K solutions print exactly the numbers in their text and captions from the code shown: K1 ($2000$, $1602\ \mu\varepsilon$), K2 ($69.75$, $123.75$, $129.75$), K3 ($16.8$ mm, $287.9$ mm², $37.7\%$), K4 ($17.6\%$), K5 ($80$, $1.62$, $80.6$), K6 ($207$ MPa, $1230$ kg), K7 ($3706$, $14562$), K8 ($0.16$, $0.95$), K9 ($56.7$, $0.50$), K10 ($22.2$, $99.0$; $25.1$, $111.9$). K1, K3, K9, and K10 are real computational problems as they stand.
- K10's self-consistency check ($PL=200$ N m reproducing §3's $99$ MPa) is the kind of tie between sections the brief asks for.
- The §3 stress-versus-moment plot (`module02.html:236-263`) has computed polylines whose endpoints match the section moduli ($119.3$ and $61.4$ px at $300$ N m) and a yield line at the tensile value with the reason stated in the prose.
- Pillar 1 holds in §1 to §4: cortical, trabecular, anisotropic, heterogeneous, medullary canal, neutral axis, section modulus, rate of twist, and shear modulus are each glossed in the sentence of first use.

## 6. Counts

- Blocking defects: 22 (B1 to B22).
- Style and clarity edits: 20.
- Numeric mismatches between code and text: 1 of 64 numbers checked (the lab caption's 100 to 150 days against the computed 24 to 56 days; lab 4, §2 5, §3 7, §4 7, §5 2, §6 5, K1 3, K2 5, K3 3, K4 1, K5 3, K6 2, K7 4, K8 2, K9 2, K10 5, D4 1, D9 2, C5 1). The three §3 polyline endpoints and two lab polyline points were also checked and match. The other factual errors (B1, B3, B4, B11, B15, B21) are prose against physics, prose against figure, or prose against prose, not code against prose.
- K problems judged plug-in: K5, K6, K7, K8 (K2 and K4 pass the depth test but fail the precise-statement test, B11 and B12).
