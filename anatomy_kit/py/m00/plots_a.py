"""Module 0 main-text plots in the house style (group `plots_a`): svg #5, 6, 7, 10, 11, 14, 15, 16, 17.

Every plotted number is computed here from the formula, constant or data module00.html states:
  counting noise (Prop. 1.2, V of the half-sarcomere cylinder), the Born potential (Def. 2.1, Lemma 2.1),
  the two bulk-modulus routes (boxed rocksalt formula, Prop. 2.2), Delta G against ln Q (Prop. 3.3, 3.4),
  the fatigue path of Delta G and the force ceiling |Delta G|/(N_A d) (sec. 3 table and caption), the Gaussian
  network modulus 3 rho N_A k_B T / M_c (Prop. 4.3), the warming test (Prop. 4.1, steel dE/dT), the Bjerrum and
  Debye lengths (Def. 5.1, Prop. 5.1), the Nernst potentials and the pump bill (Prop. 5.2, sec. 5).
Plot helpers come from the approved m05.plots_main. All figures use a 760-unit-wide viewBox (1 unit = 1 px).
"""
import math

import house as H
from m05.plots_main import Ax, axes, curve, dot, legend, legend_col, lead, mn, poly, svg, sub, tw, DASH_SER

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
ION = T["fluid"][1]                      # ions are drawn in the fluid blue (the author, 2026-10-12)
REST, FATIG = SER[3], SER[2]             # resting muscle green, fatigued orange (svg #10, #11; svg #12 should match)
BAND = I["rule"]

# ---------------------------------------------------------------- constants the module states
NA = 6.02214076e23          # 1/mol
CE = 2.307e-28              # J m, e^2 / (4 pi eps0)      (Def. 2.1)
KBT = 4.28e-21              # J at 37 °C                  (sec. 1)
RG, TB = 8.314, 310.15      # J/(mol K), K
RT = RG * TB / 1e3          # kJ/mol, 2.58 (Prop. 3.3)
EV = 1.602176634e-19        # J
FARADAY = 96485.0           # C/mol                       (Def. 5.3)

SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def p10(e):
    """10 to the power e, as Unicode text."""
    return "10" + str(e).translate(SUP)


def lin(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


def logs(a, b, n):
    la, lb = math.log10(a), math.log10(b)
    return [10 ** (la + (lb - la) * i / (n - 1)) for i in range(n)]


def clip_y(ax, xs, ys, lo, hi):
    """Keep the part of a curve with lo <= y <= hi (cut at the bound, linear in plot space)."""
    out = []
    for k, (x, y) in enumerate(zip(xs, ys)):
        if lo <= y <= hi:
            if out == [] and k > 0:
                x0, y0 = xs[k - 1], ys[k - 1]
                b = hi if y0 > hi else lo
                out.append((x0 + (x - x0) * (b - y0) / (y - y0), b))
            out.append((x, y))
        elif out:
            x0, y0 = xs[k - 1], ys[k - 1]
            b = hi if y > hi else lo
            out.append((x0 + (x - x0) * (b - y0) / (y - y0), b))
            break
    return [p[0] for p in out], [p[1] for p in out]


def panel_hover(ax, pts):
    return ([round(v, 2) for v in ax.box], sorted(pts, key=lambda p: p[0]))


def conc(c):
    """A molar concentration in the unit a physiologist would quote."""
    for f, u in ((1, "M"), (1e-3, "mM"), (1e-6, "µM"), (1e-9, "nM"), (1e-12, "pM")):
        if c >= f:
            return f"{c / f:.3g} {u}"
    return f"{c:.3g} M"


# ================================================================ svg #5 (Fig. 4): counting noise
V_HS = math.pi / 4 * 1.0 ** 2 * 1.35 * 1e-15        # L: cylinder 1 µm across, 1.35 µm long = 1.06 fL (line 356)


def nbar(c):
    return c * NA * V_HS


def noise(c):
    """Prop. 1.2: sigma_N / N-bar, in per cent."""
    return 100 / math.sqrt(nbar(c))


def fig5():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((92, 64, 735, 326), (1e-9, 1e-2), (0.01, 300), xlog=True, ylog=True)
    o = axes(s, ax, [(10 ** e, p10(e)) for e in range(-9, -1)], [(v, f"{v:g}") for v in (0.01, 0.1, 1, 10, 100)],
             "concentration c (M, log scale)", f'relative fluctuation σ{sub("N", s)}/N̄ (%)', ylab_x=30)
    # top axis: the same concentrations read as a mean count in the volume
    o.append(H.line(s, ax.x0, ax.top, ax.x1, ax.top, I["axis"], "axis"))
    for k in range(0, 7):
        x = ax.X(10 ** k / (NA * V_HS))
        o.append(H.line(s, x, ax.top - 5, x, ax.top, I["axis"], "leader"))
        o.append(H.label(s, x, ax.top - 9, "1" if k == 0 else p10(k), "tick", I["secondary"], "middle"))
    o.append(H.label(s, (ax.x0 + ax.x1) / 2, ax.top - 30, "mean count N̄ = c N" + sub("A", s) + " V in one half-sarcomere, "
                     "V = 1.06 fL", "label2", I["primary"], "middle"))
    c10 = 100 / (NA * V_HS)                         # N-bar = 100  <=>  10 %
    o.append(H.line(s, ax.x0, ax.Y(10), ax.x1, ax.Y(10), O["flag"], "ref", H.DASH_REF))
    o.append(H.line(s, ax.X(c10), ax.Y(10), ax.X(c10), ax.y0, I["rule"], "leader", H.DASH_REF))
    cs = logs(1e-9, 1e-2, 120)
    o.append(curve(s, ax, cs, [noise(c) for c in cs], SER[0]))
    o.append(H.label(s, ax.x1 - 4, ax.Y(10) - 8, "10 %", "label2", I["primary"], "end"))
    for k, txt in enumerate(("above 10 %, a continuum", "stops describing", "one compartment")):
        o.append(H.label(s, ax.X(1.2e-9), ax.Y(0.1) + 16 * k, txt, "label2", I["secondary"]))
    o.append(H.label(s, ax.X(c10) + 6, ax.y0 - 8, f"{c10 * 1e6:.2f} µM: N̄ = 100", "label2", I["primary"]))
    o.append(H.label(s, ax.X(10 ** -8.75) + 18, ax.Y(noise(10 ** -8.75)) - 12, "slope −½: 100× dilution, 10× noise",
                     "label2", I["secondary"]))
    for c in (1e-7, 1.4e-6, 1e-5):
        o.append(dot(s, ax.X(c), ax.Y(noise(c)), ION, r=4.5))
    val = lambda c: f"N̄ = {nbar(c):.0f}, σ{sub('N', s)}/N̄ = {noise(c):.{1 if noise(c) > 3 else 2}f} %"  # noqa: E731
    x, y = ax.X(1e-7), ax.Y(noise(1e-7))
    o.append(H.label(s, x - 10, y + 30, "resting Ca²⁺, 0.1 µM", "label2", I["primary"], "end"))
    o.append(H.label(s, x - 10, y + 46, val(1e-7), "label2", I["secondary"], "end"))
    x, y = ax.X(1.4e-6), ax.Y(noise(1.4e-6))
    yt = ax.Y(10) - 26
    o.append(lead(s, x + 3, y - 5, x + 20, yt + 22, I["rule"]))
    o.append(H.label(s, x + 22, yt, "single-twitch peak, 1.4 µM", "label2", I["primary"]))
    o.append(H.label(s, x + 22, yt + 16, val(1.4e-6), "label2", I["secondary"]))
    x, y = ax.X(1e-5), ax.Y(noise(1e-5))
    o.append(H.label(s, x + 10, y - 26, "top of activation, 10 µM", "label2", I["primary"]))
    o.append(H.label(s, x + 10, y - 10, val(1e-5), "label2", I["secondary"]))
    aria = (f"Log-log plot of relative counting noise against concentration for a fixed half-sarcomere volume of "
            f"{V_HS * 1e15:.2f} femtolitres, by Proposition 1.2: a straight red line of slope minus one half. A top axis "
            f"reads the same concentrations as mean counts from 1 to one million. A dashed orange line marks 10 per cent, "
            f"crossed at {c10 * 1e6:.2f} micromolar. Blue dots mark calcium at rest, 0.1 micromolar, {nbar(1e-7):.0f} ions "
            f"and {noise(1e-7):.1f} per cent; the single-twitch peak, 1.4 micromolar, {nbar(1.4e-6):.0f} ions and "
            f"{noise(1.4e-6):.1f} per cent; and the top of the activation range, 10 micromolar, {nbar(1e-5):.0f} ions and "
            f"{noise(1e-5):.2f} per cent.")
    hc = logs(1e-9, 1e-2, 141)
    hv = [[ax.X(c), ax.Y(noise(c)), f"c = {conc(c)}: N̄ = {nbar(c):.3g}, σN/N̄ = {noise(c):.3g} %"] for c in hc]
    return svg(VB, aria, s, o, H.hover_attr(ax.box, hv))


# ================================================================ svg #6 (Fig. 5): the Born potential
R0, NB, ZZ = 0.240, 8, 4                           # nm, Born exponent, |z1 z2| (line 417)
A_EV = ZZ * CE / EV * 1e9                          # eV nm
B_EV = A_EV * R0 ** (NB - 1) / NB                  # Lemma 2.1 proof: B = A r0^(n-1) / n
K_PAIR = (NB - 1) * ZZ * CE / (R0 * 1e-9) ** 3     # N/m


def u_att(r):
    return -A_EV / r


def u_rep(r):
    return B_EV / r ** NB


def u_born(r):
    return u_att(r) + u_rep(r)


def fig6():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 30, 520, 320), (0.18, 0.60), (-30, 15))
    o = axes(s, ax, [(v, f"{v:.1f}") for v in (0.2, 0.3, 0.4, 0.5, 0.6)], [(v, mn(v, "{:.0f}")) for v in (-30, -20, -10, 0, 10)],
             "separation r (nm)", "energy U (eV)", ylab_x=32)
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["axis"], "leader"))
    depth = -u_born(R0)
    k_ev = K_PAIR / EV * 1e-18                     # eV / nm^2
    rs = lin(0.18, 0.60, 106)
    xa, ya = clip_y(ax, rs, [u_att(r) for r in rs], -30, 15)
    xr, yr = clip_y(ax, rs, [u_rep(r) for r in rs], -30, 15)
    xb, yb = clip_y(ax, rs, [u_born(r) for r in rs], -30, 15)
    rh = lin(0.18, 0.32, 71)
    xh, yh = clip_y(ax, rh, [-depth + 0.5 * k_ev * (r - R0) ** 2 for r in rh], -30, -12)
    o.append(curve(s, ax, xa, ya, SER[0], "curve_multi", DASH_SER))
    o.append(curve(s, ax, xr, yr, SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, ax, xh, yh, SER[3], "curve_multi", (2, 3)))
    o.append(curve(s, ax, xb, yb, I["primary"], "curve"))
    # the minimum
    o.append(H.line(s, ax.X(R0), ax.Y(-depth), ax.X(R0), ax.y0, I["rule"], "leader", H.DASH_REF))
    o.append(dot(s, ax.X(R0), ax.Y(-depth), I["primary"]))
    o.append(H.label(s, ax.X(R0) + 4, ax.y0 - 8, f"r₀ = {R0:.3f} nm", "label2", I["primary"]))
    kj = round(depth * EV * NA / 1e3, -1)
    xw = ax.X(0.335)
    o.append(lead(s, ax.X(R0) + 5, ax.Y(-depth) + 4, xw - 4, ax.Y(-23.0), I["rule"]))
    o.append(H.label(s, xw, ax.Y(-23.0) + 4, f"well depth {depth:.1f} eV = {kj:.0f} kJ/mol", "label2", I["primary"]))
    o.append(H.label(s, xw, ax.Y(-23.0) + 20, f"≈ {round(depth * EV / KBT, -1):.0f} k" + sub("B", s) + "T per bond, far outside",
                     "label2", I["secondary"]))
    o.append(H.label(s, xw, ax.Y(-23.0) + 36, "the thermal window", "label2", I["secondary"]))
    # direct labels
    o.append(H.label(s, ax.X(0.222), ax.Y(12), "repulsion B/r⁸", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.262), ax.Y(-9.5), f"harmonic fit, k = {K_PAIR:.0f} N/m", "label2", I["primary"]))
    o.append(lead(s, ax.X(0.268), ax.Y(-9.5) + 4, ax.X(0.300) - 1, ax.Y(-depth + 0.5 * k_ev * (0.300 - R0) ** 2) - 3, SER[3]))
    o.append(H.label(s, ax.X(0.43), ax.Y(-8.8), "sum U(r): one minimum", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.43), ax.Y(-17.6), "attraction −|z₁z₂|C" + sub("e", s) + "/r", "label2", I["primary"]))
    rr = 0.35
    o.append(H.label(s, ax.X(0.335), ax.Y(5.5), f"beyond {rr} nm the repulsion is under {u_rep(rr):.2f} eV,", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(0.335), ax.Y(5.5) + 16, "so the sum and the attraction coincide", "label2", I["secondary"]))
    o += legend_col(s, 545, 52, [(SER[0], DASH_SER, "Coulomb attraction alone"), (SER[1], DASH_SER, "Born repulsion alone"),
                                 (I["primary"], None, "their sum: the Born potential"),
                                 (SER[3], (2, 3), f"harmonic fit, k{sub('pair', s)} = {K_PAIR:.0f} N/m")], dy=22)
    o.append(H.label(s, 545, 160, f"Ca²⁺–O²⁻, |z₁z₂| = {ZZ}, n = {NB}", "label2", I["secondary"]))
    aria = (f"Energy against separation for a calcium-oxygen ion pair, |z1 z2| = {ZZ}, n = {NB}. A dashed red curve, the "
            "Coulomb attraction, falls without a minimum; a dashed blue curve, the Born repulsion, rises without a minimum. "
            f"Their solid black sum has one minimum, {depth:.1f} electronvolts deep at {R0:.3f} nanometres, which is "
            f"{kj:.0f} kilojoules per mole or about {round(depth * EV / KBT, -1):.0f} kBT. A dotted green parabola of "
            f"curvature {K_PAIR:.0f} newtons per metre follows the black curve only near the floor. Beyond 0.35 nanometres "
            f"the repulsion is under {u_rep(0.35):.2f} electronvolts and the black and red curves coincide.")
    hr = lin(0.19, 0.60, 140)
    hv = []
    for r in hr:
        ys = [ax.Y(min(15, max(-30, f(r)))) for f in (u_born, u_att, u_rep)]
        hv.append([ax.X(r), ys, f"r = {r:.3f} nm: U = {mn(u_born(r), '{:.2f}')} eV, attraction {mn(u_att(r), '{:.2f}')}, "
                                f"repulsion {u_rep(r):.2f}"])
    return svg(VB, aria, s, o, H.hover_attr(ax.box, hv))


# ================================================================ svg #7 (Fig. 6): predicted against measured K
ALPHA_M = 1.7476
CRYST = [  # name, |z1 z2|, r0 (nm), n, |U_latt| (kJ/mol), K measured (GPa)  (table, lines 482-484)
    ("NaCl", 1, 0.282, 8, 786, 24.4), ("MgO", 4, 0.2106, 7, 3795, 160), ("CaO", 4, 0.2405, 8, 3414, 111)]


def k_route_a(zz, r0, n):
    return (n - 1) * ALPHA_M * zz * CE / (18 * (r0 * 1e-9) ** 4) / 1e9


def k_route_b(u, vf_m3, n):
    return n * (u * 1e3 / NA) / (9 * vf_m3) / 1e9


VF_HAP = math.sqrt(3) / 2 * 0.94166 ** 2 * 0.68745 * 1e-27      # m^3 (line 501)
K_HAP = k_route_b(34191, VF_HAP, 8)                                # 95.6 GPa (line 505)


def fig7():
    VB = (0, 0, 760, 390)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((92, 24, 392, 324), (15, 400), (15, 400), xlog=True, ylog=True)
    tk = [(v, f"{v}") for v in (20, 50, 100, 200, 400)]
    o = axes(s, ax, tk, tk, "measured K (GPa)", "predicted K (GPa)", ylab_x=34)
    for v, _ in tk:
        o.append(H.line(s, ax.X(v), ax.top, ax.X(v), ax.y0, "#e6e6e6", "leader"))
    o.append(poly(s, [(ax.X(15), ax.Y(15)), (ax.X(400), ax.Y(400))], I["secondary"], "ref", H.DASH_REF))
    o.append(poly(s, [(ax.X(15), ax.Y(25.5)), (ax.X(400 / 1.7), ax.Y(400))], O["flag"], "ref", (2, 3)))
    rows = [(nm, k_route_a(zz, r0, n), k_route_b(u, 2 * (r0 * 1e-9) ** 3, n), km) for nm, zz, r0, n, u, km in CRYST]
    hv = []
    for nm, ka, kb, km in rows:
        o.append(dot(s, ax.X(km), ax.Y(kb), SER[0], hollow=True, r=7))
        o.append(H.line(s, ax.X(km), ax.Y(ka), ax.X(km), ax.Y(kb), SER[0], "geom"))
        o.append(dot(s, ax.X(km), ax.Y(ka), SER[0], r=3.5))
        hv.append([ax.X(km), [ax.Y(ka), ax.Y(kb)], f"{nm}: measured {km:g} GPa, route A {ka:.1f}, route B {kb:.1f} GPa"])
    o.append(dot(s, ax.X(85), ax.Y(K_HAP), SER[0], hollow=True, r=7))
    hv.append([ax.X(85), ax.Y(K_HAP), f"hydroxyapatite: measured 85 GPa, route B {K_HAP:.1f} GPa"])
    (na, naa, nab, _), (mg, mga, mgb, mgm), (ca, caa, cab, cam) = rows
    o.append(H.label(s, ax.X(24.4) + 12, ax.Y(25.3) + 20, f"NaCl  {naa:.1f} / {nab:.1f} vs 24.4", "label2", I["primary"]))
    o.append(H.label(s, ax.X(cam) - 12, ax.Y(caa) - 2, f"CaO  {caa:.0f} / {cab:.0f} vs 111", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(mgm) - 12, ax.Y(mga) - 2, f"MgO  {mga:.0f} / {mgb:.0f} vs 160", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(85) + 8, ax.Y(K_HAP) + 30, f"hydroxyapatite  {K_HAP:.1f} vs 85", "label2", I["primary"]))
    o.append(H.label(s, ax.X(85) + 8, ax.Y(K_HAP) + 46, "(route B only)", "label2", I["secondary"]))

    o.append(H.label(s, ax.X(150) + 14, ax.Y(150) + 6, "agreement", "label2", I["secondary"], "start", 'font-style="italic"'))
    o.append(H.label(s, ax.X(40) - 14, ax.Y(68) - 10, "1.7×", "label2", I["secondary"], "end", 'font-style="italic"'))
    o.append(H.label(s, ax.X(40) - 14, ax.Y(68) + 6, "too stiff", "label2", I["secondary"], "end", 'font-style="italic"'))
    x0 = 420
    sw = []
    for k, (txt, hol) in enumerate((("route A: boxed rocksalt formula (Coulomb sum)", False),
                                    ("route B: Prop. 2.2 with a Born–Haber energy", True))):
        yy = 46 + 22 * k
        sw.append(dot(s, x0 + 11, yy - 4, SER[0], hollow=hol, r=7 if hol else 3.5))
        sw.append(H.label(s, x0 + 31, yy, txt, "label2", I["primary"]))
    o += sw
    o += legend_col(s, x0, 90, [(I["secondary"], H.DASH_REF, "predicted = measured"),
                                (O["flag"], (2, 3), "predicted = 1.7 × measured")], dy=22)
    o.append(H.label(s, x0, 134, "labels: route A / route B vs measured (GPa)", "label2", I["secondary"]))
    notes = ["No elastic measurement is an input to either route.",
             "The vertical bar joins the two routes for one crystal:",
             "it is their whole disagreement.",
             "NaCl, the alkali halide that fixed Pauling's exponents,",
             "passes. The divalent oxides overshoot by 1.7 whichever",
             "route is used: the fault is in the point-ion potential.",
             "Apatite, a framework, lands near agreement."]
    for k, t in enumerate(notes):
        o.append(H.label(s, x0, 170 + 18 * k, t, "label2", I["secondary"]))
    aria = ("Log-log plot of predicted against measured bulk modulus in gigapascals, equal decades on both axes. A dashed "
            "diagonal marks perfect agreement and a dotted orange line marks predictions 1.7 times too stiff. Filled red dots "
            "are route A, the rocksalt Coulomb formula; open dots are route B, Proposition 2.2 with a Born-Haber lattice "
            f"energy; a short bar joins the two for each rocksalt crystal. Sodium chloride sits on the agreement line at "
            f"{naa:.1f} and {nab:.1f} against 24.4 measured. Calcium oxide, {caa:.0f} and {cab:.0f} against 111, and "
            f"magnesium oxide, {mga:.0f} and {mgb:.0f} against 160, sit on the 1.7 times line. Hydroxyapatite has route B "
            f"only, {K_HAP:.1f} against 85 measured, close to agreement.")
    return svg(VB, aria, s, o, H.hover_attr(ax.box, sorted(hv, key=lambda p: p[0])))


# ================================================================ svg #10 (Fig. 9): Delta G against ln Q
DG0 = -20.5 - TB * (-20.5 + 30.5) / 298.15         # kJ/mol: -30.90 at 310.15 K (line 690)
LNK = -DG0 / RT                                    # 11.98 (Prop. 3.4)
METAB = {"rest": (5.5e-3, 13e-6, 2.0e-3), "fatigued": (5.0e-3, 70e-6, 15e-3)}   # ATP, ADP, Pi in M (table, lines 702-704)


def ln_q(atp, adp, pi):
    return math.log(adp * pi / atp)


def dg(lnq):
    return DG0 + RT * lnq


def fig10():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    p = "m0f10_"
    ax = Ax((90, 30, 735, 320), (-32, 16), (-110, 10))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    q_r, q_f = ln_q(*METAB["rest"]), ln_q(*METAB["fatigued"])
    o.append(f'<rect x="{ax.X(q_r):.2f}" y="{ax.top}" width="{ax.X(q_f) - ax.X(q_r):.2f}" height="{ax.y0 - ax.top}" '
             f'fill="{BAND}" opacity="0.16"/>')
    o += axes(s, ax, [(v, mn(v, "{:.0f}")) for v in range(-30, 16, 10)], [(v, mn(v, "{:.0f}")) for v in range(-100, 1, 20)],
              "ln Q", "ΔG (kJ/mol)", ylab_x=34)
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["secondary"], "ref", H.DASH_REF))
    o.append(H.line(s, ax.X(LNK), ax.Y(0), ax.X(LNK), ax.y0, O["flag"], "ref", H.DASH_REF))
    o.append(poly(s, [(ax.X(-32), ax.Y(dg(-32))), (ax.X(16), ax.Y(dg(16)))], SER[1]))
    # slope triangle, 10 units of ln Q
    xa, xb = -30, -20
    o.append(H.line(s, ax.X(xa), ax.Y(dg(xa)), ax.X(xa), ax.Y(dg(xb)), O["dim"], "ref"))
    o.append(H.line(s, ax.X(xa), ax.Y(dg(xb)), ax.X(xb), ax.Y(dg(xb)), O["dim"], "ref"))
    o.append(H.label(s, ax.X(-25), ax.Y(dg(xb)) - 6, "10", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(xa) + 5, ax.Y((dg(xa) + dg(xb)) / 2) + 5, f"{10 * RT:.1f}", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(-31), ax.Y(-62), f"slope = R{sub('g', s)}T = {RT:.2f} kJ/mol", "label2", I["primary"]))
    o.append(H.label(s, ax.X(-31), ax.Y(-62) + 16, "per unit of ln Q", "label2", I["secondary"]))
    # budget at rest: vertical distance to the zero line
    o.append(H.arrow(s, p, ax.X(q_r) - 14, ax.Y(dg(q_r)) - 2, ax.X(q_r) - 14, ax.Y(0) + 2, "geometry", both=True))
    o.append(H.label(s, ax.X(q_r) - 22, ax.Y(-24), f"budget |ΔG| = {-dg(q_r):.1f}", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(q_r) - 22, ax.Y(-24) + 16, "available for work", "label2", I["secondary"], "end"))
    # distance from the band to equilibrium
    yd = ax.Y(-88)
    o.append(H.arrow(s, p, ax.X(q_f) + 2, yd, ax.X(LNK) - 2, yd, "geometry", both=True))
    o.append(H.label(s, ax.X((q_f + LNK) / 2), yd + 20, f"{LNK - q_f:.1f} units of ln Q from equilibrium",
                     "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X((q_r + q_f) / 2), ax.top + 16, "living muscle", "label2", I["primary"], "middle"))
    pts = [(q_r, REST, "resting", "start", 12, 30), (q_f, FATIG, "fatigued", "start", 12, 22),
           (0.0, SER[0], "standard state, all at 1 M", "end", -10, -26)]
    for q, col, name, anc, dx, dy in pts:
        x, y = ax.X(q), ax.Y(dg(q))
        o.append(dot(s, x, y, col, r=5))
        o.append(H.label(s, x + dx, y + dy, name, "label2", I["primary"], anc))
        o.append(H.label(s, x + dx, y + dy + 16, f"ln Q = {mn(q, '{:.2f}')}, ΔG = {mn(dg(q))}", "label2", I["secondary"], anc))
    o.append(dot(s, ax.X(LNK), ax.Y(0), I["primary"], hollow=True, r=5))
    o.append(H.label(s, ax.X(LNK) - 10, ax.Y(0) - 26, "equilibrium, ΔG = 0", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(LNK) - 10, ax.Y(0) - 10, f"ln K{sub('eq', s)} = {LNK:.2f}", "label2", I["secondary"], "end"))
    o += legend_col(s, ax.x0 + 10, ax.top + 18, [(REST, None, "resting muscle", "dot"), (FATIG, None, "fatigued muscle", "dot"),
                                                 (SER[0], None, "standard state", "dot")])
    aria = (f"Straight blue line of the free energy of ATP hydrolysis against the logarithm of the reaction quotient, "
            f"by Proposition 3.3, of slope RgT = {RT:.2f} kilojoules per mole. It crosses zero at ln Keq = {LNK:.2f}, the "
            f"equilibrium, marked by an open dot and a dashed orange drop line. Marked compositions: the standard state in "
            f"red at ln Q = 0 and {mn(DG0)}; resting muscle in green at {mn(q_r, '{:.2f}')} and {mn(dg(q_r))}; fatigued "
            f"muscle in orange at {mn(q_f, '{:.2f}')} and {mn(dg(q_f))}. A grey band between rest and fatigue is where a "
            f"living muscle operates, {LNK - q_f:.1f} units of ln Q left of equilibrium; a blue arrow from the resting point "
            f"to the zero line is the {-dg(q_r):.1f} kilojoule per mole budget available for work.")
    hq = lin(-32, 16, 121)
    hv = [[ax.X(q), ax.Y(dg(q)), f"ln Q = {mn(q, '{:.1f}')}: ΔG = {mn(dg(q), '{:.2f}')} kJ/mol"] for q in hq]
    return svg(VB, aria, s, o, H.hover_attr(ax.box, hv))


# ================================================================ svg #11 (Fig. 10): Delta G through a fatiguing bout
D_STROKE = 10e-9                                   # m (line 716)


def bout(u):
    """Caption path: Pi linear in progress u, free ADP log-linear, ATP linear (M)."""
    (a0, d0, p0), (a1, d1, p1) = METAB["rest"], METAB["fatigued"]
    return a0 + (a1 - a0) * u, math.exp(math.log(d0) + (math.log(d1) - math.log(d0)) * u), p0 + (p1 - p0) * u


def f_ceil(dgv):
    """Prop. 3.1 ceiling |Delta G| / (N_A d), pN, for Delta G in kJ/mol."""
    return abs(dgv) * 1e3 / NA / D_STROKE * 1e12


def fig11():
    VB = (0, 0, 760, 390)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 30, 640, 310), (0, 16), (-66, -48))
    us = lin(0, 1, 101)
    path = [bout(u) for u in us]
    pis = [p[2] * 1e3 for p in path]
    dgs = [dg(ln_q(*p)) for p in path]
    o = axes(s, ax, [(v, f"{v}") for v in range(0, 17, 4)], [(v, mn(v, "{:.0f}")) for v in range(-66, -47, 3)],
             "inorganic phosphate [Pᵢ] (mM)", "ΔG of ATP hydrolysis (kJ/mol)", ylab_x=34)
    # right axis: the same curve read as the force ceiling (pN), increasing downward
    o.append(H.line(s, ax.x1, ax.y0, ax.x1, ax.top, O["load"], "axis"))
    for fpn in (8.0, 8.5, 9.0, 9.5, 10.0, 10.5):
        y = ax.Y(-fpn * 1e-12 * D_STROKE * NA / 1e3)
        o.append(H.line(s, ax.x1, y, ax.x1 + 5, y, O["load"], "leader"))
        o.append(H.label(s, ax.x1 + 9, y + 4.5, f"{fpn:.1f}", "tick", I["secondary"]))
    ym = (ax.y0 + ax.top) / 2
    o.append(H.label(s, ax.x1 + 56, ym, f"force ceiling |ΔG|/(N{sub('A', s)}d) (pN)", "label", I["primary"], "middle",
                     f'transform="rotate(90 {ax.x1 + 56:.2f} {ym:.2f})"'))
    o.append(H.line(s, ax.x0, ax.Y(-50), ax.x1, ax.Y(-50), I["rule"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(0.4), ax.Y(-50) - 8, f"§1's round 50 kJ/mol: {f_ceil(-50):.2f} pN", "label2", I["secondary"]))
    o.append(curve(s, ax, pis, dgs, SER[0]))
    g0, g1 = dgs[0], dgs[-1]
    o.append(dot(s, ax.X(pis[0]), ax.Y(g0), REST, r=5))
    o.append(dot(s, ax.X(pis[-1]), ax.Y(g1), FATIG, r=5))
    o.append(H.label(s, ax.X(pis[0]) + 12, ax.Y(g0) + 20, f"rest, [Pᵢ] = 2 mM: ΔG = {mn(g0)} kJ/mol", "label2", I["primary"]))
    o.append(H.label(s, ax.X(pis[0]) + 12, ax.Y(g0) + 36, f"ceiling {f_ceil(g0):.2f} pN", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(pis[-1]) - 8, ax.Y(g1) - 24, f"end of a hard bout, [Pᵢ] = 15 mM: {mn(g1)} kJ/mol", "label2",
                     I["primary"], "end"))
    o.append(H.label(s, ax.X(pis[-1]) - 8, ax.Y(g1) - 8, f"ceiling {f_ceil(g1):.2f} pN", "label2", I["secondary"], "end"))
    drop = f_ceil(g0) - f_ceil(g1)
    xn = ax.X(8.3)
    o.append(H.label(s, xn, ax.Y(-59.5), f"ceiling on one crossbridge: −{drop:.2f} pN "
                     f"({100 * drop / f_ceil(g0):.0f} %)", "label2", I["primary"]))
    o.append(H.label(s, xn, ax.Y(-59.5) + 16, "measured head force, 3–6 pN:", "label2", I["secondary"]))
    o.append(H.label(s, xn, ax.Y(-59.5) + 32, "below both ceilings", "label2", I["secondary"]))
    aria = ("Curve of the free energy of ATP hydrolysis against inorganic phosphate from 2 to 15 millimolar through a "
            "fatiguing contraction, by Proposition 3.3 along the interpolated path of the caption. The free energy rises "
            f"from {mn(g0)} kilojoules per mole at rest to {mn(g1)} at the end of the bout, steeply at first and then "
            "flatter. A brown right-hand axis, increasing downward, reads the same curve as the thermodynamic ceiling on "
            f"crossbridge force over a 10 nanometre stroke: {f_ceil(g0):.2f} piconewtons at rest and {f_ceil(g1):.2f} at "
            f"the end, a drop of {drop:.2f}. A dashed line marks the round 50 kilojoules per mole, {f_ceil(-50):.2f} "
            "piconewtons, of section 1.")
    hv = [[ax.X(x), ax.Y(y), f"[Pi] = {x:.1f} mM: ΔG = {mn(y, '{:.2f}')} kJ/mol, ceiling {f_ceil(y):.2f} pN"]
          for x, y in zip(pis, dgs)]
    return svg(VB, aria, s, o, H.hover_attr(ax.box, hv))


# ================================================================ svg #14 (Fig. 13): the network test
def e_gauss(rho, mc_kg):
    """Prop. 4.3: E = 3 rho N_A k_B T / M_c (Pa)."""
    return 3 * rho * NA * KBT / mc_kg


def fig14():
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    p = "m0f14_"
    ax = Ax((100, 30, 430, 360), (1e5, 1e10), (1e5, 1e10), xlog=True, ylog=True)
    tk = [(10 ** e, p10(e)) for e in range(5, 11)]
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, ax, tk, tk, "measured modulus E (Pa)", f"predicted modulus 3nk{sub('B', s)}T (Pa)", ylab_x=36)
    for v, _ in tk[1:]:
        o.append(H.line(s, ax.X(v), ax.top, ax.X(v), ax.y0, "#e6e6e6", "leader"))
    o.append(poly(s, [(ax.X(1e5), ax.Y(1e5)), (ax.X(1e10), ax.Y(1e10))], I["secondary"], "ref", H.DASH_REF))
    rub, ela = e_gauss(950, 5.0), e_gauss(1300, 6.5)
    c_real, c_hi, c_lo = e_gauss(1400, 6.5), e_gauss(1400, 3.0), e_gauss(1400, 5.0)
    e_col = 1.07e9
    hv = [[ax.X(1.1e6), ax.Y(ela), f"elastin: measured 1.1 MPa, predicted {ela / 1e6:.2f} MPa ({ela / 1.1e6:.2f}×)"],
          [ax.X(1.5e6), ax.Y(rub), f"natural rubber: measured 1.5 MPa, predicted {rub / 1e6:.2f} MPa ({rub / 1.5e6:.2f}×)"],
          [ax.X(e_col), [ax.Y(e_col), ax.Y(c_hi), ax.Y(c_real)],
           f"collagen fibril 1.07 GPa: Gaussian ceiling {c_lo / 1e6:.1f}–{c_hi / 1e6:.1f} MPa, real spacing {c_real / 1e6:.2f} MPa"]]
    o.append(dot(s, ax.X(1.5e6), ax.Y(rub), SER[1], r=5.5))
    o.append(dot(s, ax.X(1.1e6), ax.Y(ela), SER[1], r=5.5))
    o.append(H.label(s, ax.X(1.5e6) + 12, ax.Y(rub) + 20, f"natural rubber, {rub / 1.5e6:.2f}× measured", "label2", I["primary"]))
    o.append(H.label(s, ax.x0 + 10, ax.Y(1e8), f"elastin, {ela / 1.1e6:.2f}× measured", "label2", I["primary"]))
    o.append(lead(s, ax.x0 + 40, ax.Y(1e8) + 5, ax.X(1.1e6) - 2, ax.Y(ela) - 6, I["rule"]))
    # collagen: what agreement would need, and the Gaussian ceiling
    xc = ax.X(e_col)
    o.append(dot(s, xc, ax.Y(e_col), SER[0], hollow=True, r=5.5))
    o.append(f'<rect x="{xc - 5:.2f}" y="{ax.Y(c_hi):.2f}" width="10" height="{ax.Y(c_lo) - ax.Y(c_hi):.2f}" '
             f'fill="{SER[0]}" opacity="0.35"/>')
    o.append(H.arrow(s, p, xc, ax.Y(e_col) + 8, xc, ax.Y(c_hi) - 1, "force"))
    o.append(H.line(s, xc - 12, ax.Y(c_real), xc + 12, ax.Y(c_real), SER[0], "geom", (4, 3)))
    o.append(H.label(s, xc + 12, ax.Y(e_col) + 20, "collagen fibril, measured 1.07 GPa", "label2", I["primary"]))
    o.append(H.label(s, xc + 16, ax.Y(3e8) + 14, f"Gaussian ceiling {c_lo / 1e6:.1f}–{c_hi / 1e6:.1f} MPa", "label2", I["primary"]))
    o.append(H.label(s, xc + 16, ax.Y(3e8) + 30, f"(N ≳ 10 Kuhn segments, M{sub('c', s)} = 3–5 kDa):", "label2", I["secondary"]))
    o.append(H.label(s, xc + 16, ax.Y(3e8) + 46, f"short by {e_col / c_hi:.0f}–{e_col / c_lo:.0f}×", "label2", I["primary"]))
    o.append(H.label(s, xc + 16, ax.Y(c_hi) - 2, f"{c_hi / 1e6:.1f} MPa", "label2", I["secondary"]))
    o.append(H.label(s, xc + 16, ax.Y(c_real) + 16, f"real crosslink spacing, 6.5 kDa: {c_real / 1e6:.2f} MPa,", "label2",
                     I["primary"]))
    o.append(H.label(s, xc + 16, ax.Y(c_real) + 32, f"short by {e_col / c_real:.0f}×", "label2", I["primary"]))
    o.append(H.label(s, ax.X(3e6) + 14, ax.Y(3e6) + 6, "predicted = measured", "label2", I["secondary"], "start",
                     'font-style="italic"'))
    o += legend_col(s, 470, 54, [(SER[1], None, "predicted from crosslink chemistry", "dot"),
                                 (SER[0], None, "collagen at the agreement line", "hdot"),
                                 (I["secondary"], H.DASH_REF, "predicted = measured (45°)")], dy=22)
    aria = ("Square log-log plot of predicted against measured modulus from 10 to the 5 to 10 to the 10 pascals, equal "
            "spacing per decade on both axes, so the dashed diagonal of agreement is a true 45 degrees. Natural rubber and "
            f"elastin, predicted from crosslink chemistry by Proposition 4.3, sit on the diagonal near one megapascal at "
            f"{rub / 1.5e6:.2f} and {ela / 1.1e6:.2f} times measured. The collagen fibril is measured at 1.07 gigapascals; "
            f"a red arrow runs from the diagonal down to {c_hi / 1e6:.1f} megapascals, the stiffest Gaussian network with "
            f"ten Kuhn segments between crosslinks, a shaded bar spans {c_lo / 1e6:.1f} to {c_hi / 1e6:.1f}, short by "
            f"{e_col / c_hi:.0f} to {e_col / c_lo:.0f} times, and a dashed tick at {c_real / 1e6:.2f} megapascals marks a "
            f"real protein crosslink spacing, short by {e_col / c_real:.0f} times.")
    return svg(VB, aria, s, o, H.hover_attr(ax.box, sorted(hv, key=lambda q: q[0])))


# ================================================================ svg #15 (Fig. 14): warm it and see
DEDT_STEEL = -0.0003                               # per K (line 939)


def k_ent(t):
    return (t + 273.15) / 293.15


def k_en(t):
    return 1 + DEDT_STEEL * (t - 20)


def fig15():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 46, 560, 306), (10, 50), (0.95, 1.11))
    o = axes(s, ax, [(v, f"{v}") for v in range(10, 51, 10)], [(v, f"{v:.2f}") for v in (0.95, 1.0, 1.05, 1.10)],
             "temperature (°C)", "stiffness relative to 20 °C", ylab_x=30)
    o.append(H.line(s, ax.X(37), ax.top, ax.X(37), ax.y0, I["rule"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(37) + 6, ax.y0 - 8, "body temperature, 37 °C", "label2", I["secondary"]))
    ts = lin(10, 50, 81)
    o.append(curve(s, ax, ts, [k_ent(t) for t in ts], SER[1]))
    o.append(curve(s, ax, ts, [k_en(t) for t in ts], O["load"]))
    o.append(dot(s, ax.X(20), ax.Y(1.0), I["primary"], hollow=True, r=4.5))
    o.append(H.label(s, ax.X(20) + 6, ax.Y(1.0) + 24, "both = 1 at 20 °C", "label2", I["secondary"]))
    e37, n37 = k_ent(37), k_en(37)
    o.append(dot(s, ax.X(37), ax.Y(e37), SER[1], r=5))
    o.append(dot(s, ax.X(37), ax.Y(n37), O["load"], r=5))
    o.append(H.label(s, ax.X(37) - 10, ax.Y(e37) - 10, f"{mn(100 * (e37 - 1), '{:.1f}', True)} % (= 310.15/293.15)", "label2",
                     I["primary"], "end"))
    o.append(H.label(s, ax.X(37) - 10, ax.Y(n37) + 44, f"{mn(100 * (n37 - 1), '{:.2f}')} % (dE/dT ≈ −0.03 %/K)", "label2",
                     I["primary"], "end"))
    xe = ax.x1 + 10
    o.append(H.label(s, xe, ax.Y(k_ent(50)) + 4, "entropic spring, ∝ T", "label2", I["primary"]))
    o.append(H.label(s, xe, ax.Y(k_ent(50)) + 20, "elastin, rubber", "label2", I["secondary"]))
    o.append(H.label(s, xe, ax.Y(k_en(50)) + 4, "energetic spring", "label2", I["primary"]))
    o.append(H.label(s, xe, ax.Y(k_en(50)) + 20, "steel, bone mineral,", "label2", I["secondary"]))
    o.append(H.label(s, xe, ax.Y(k_en(50)) + 36, "straightened collagen", "label2", I["secondary"]))
    o += legend(s, ax.x0, 26, [(SER[1], None, "entropic: stiffens on warming (Prop. 4.1)"),
                               (O["load"], None, "energetic: softens on warming")])
    aria = ("Relative stiffness against temperature from 10 to 50 degrees Celsius, normalised to 20 degrees. A blue line "
            f"rises in proportion to absolute temperature, the entropic spring of elastin and rubber, reaching plus "
            f"{100 * (e37 - 1):.1f} per cent at body temperature. A brown line falls gently, the energetic spring of steel, "
            f"bone mineral and straightened collagen, reaching minus {100 * (1 - n37):.2f} per cent. A dashed line marks "
            "37 degrees. The two slopes have opposite signs, which is the measurement that tells the mechanisms apart.")
    hv = [[ax.X(t), [ax.Y(k_ent(t)), ax.Y(k_en(t))], f"{t:.1f} °C: entropic {k_ent(t):.4f}, energetic {k_en(t):.4f}"]
          for t in lin(10, 50, 121)]
    return svg(VB, aria, s, o, H.hover_attr(ax.box, hv))


# ================================================================ svg #16 (Fig. 15): screening
EPS0, EPS_R, E_CH = 8.854e-12, 73.2, 1.602e-19
L_B = CE / (EPS_R * KBT) * 1e9                       # nm, Def. 5.1: 0.736
I_PLASMA = 0.1425                                     # M (line 988)


def lam_d(i_molar):
    """Prop. 5.1, I in mol/m^3 inside the root; nm."""
    return math.sqrt(EPS0 * EPS_R * KBT / (2 * E_CH ** 2 * NA * i_molar * 1e3)) * 1e9


def fig16():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    L = Ax((80, 60, 360, 320), (0, 3), (0, 4))
    R = Ax((480, 60, 735, 320), (1e-4, 0.3), (0.3, 40), xlog=True, ylog=True)
    ld = lam_d(I_PLASMA)
    o = axes(s, L, [(v, f"{v}") for v in range(0, 4)], [(v, f"{v}") for v in range(0, 5)], "separation r (nm)",
             f"energy (k{sub('B', s)}T)", ylab_x=36)
    o += axes(s, R, [(1e-4, "0.1"), (1e-3, "1"), (1e-2, "10"), (1e-1, "100")], [(v, f"{v:g}") for v in (0.3, 1, 3, 10, 30)],
              "ionic strength I (mM, log scale)", f"Debye length λ{sub('D', s)} (nm)", ylab_x=R.x0 - 46)
    o.append(H.label(s, (L.x0 + L.x1) / 2, 24, "one charge, seen by another, in water", "label", I["primary"], "middle"))
    o.append(H.label(s, (R.x0 + R.x1) / 2, 24, "how far screening reaches", "label", I["primary"], "middle"))
    o.append(H.line(s, L.x0, L.Y(1), L.x1, L.Y(1), I["rule"], "ref", H.DASH_REF))
    o.append(H.line(s, L.X(ld), L.top, L.X(ld), L.y0, O["dim"], "ref", (2, 3)))
    rs = lin(0.18, 3.0, 101)
    xu, yu = clip_y(L, rs, [L_B / r for r in rs], 0, 4)
    o.append(curve(s, L, xu, yu, O["load"], "curve_multi", DASH_SER))
    o.append(curve(s, L, rs, [L_B / r * math.exp(-r / ld) for r in rs], SER[1], "curve_multi"))
    o.append(dot(s, L.X(L_B), L.Y(1), O["load"], r=4.5))
    o.append(lead(s, L.X(L_B) + 3, L.Y(1) - 5, L.X(1.12) - 2, L.Y(2.15) + 3, I["rule"]))
    o.append(H.label(s, L.X(1.12), L.Y(2.15), f"ℓ{sub('B', s)} = {L_B:.2f} nm: the unscreened", "label2", I["primary"]))
    o.append(H.label(s, L.X(1.12), L.Y(2.15) + 16, f"energy is 1 k{sub('B', s)}T here", "label2", I["secondary"]))
    o.append(H.label(s, L.X(ld) + 5, L.top + 14, f"λ{sub('D', s)} = {ld:.3f} nm", "label2", I["primary"]))
    for k, r in enumerate((1.0, 2.0)):
        e = L_B / r * math.exp(-r / ld)
        yl = L.Y(1.4) + 18 * k
        o.append(dot(s, L.X(r), L.Y(e), SER[1], r=4))
        o.append(lead(s, L.X(1.5) - 2, yl - 4, L.X(r) + 2, L.Y(e) - 4, SER[1]) if k == 0 else
                 lead(s, L.X(r), yl + 6, L.X(r), L.Y(e) - 5, SER[1]))
        o.append(H.label(s, L.X(1.5), yl, f"screened: {e:.2f} k{sub('B', s)}T at {r:.0f} nm", "label2", I["primary"]))
    o.append(H.label(s, L.x1 - 4, L.Y(1) + 18, f"1 k{sub('B', s)}T", "label2", I["secondary"], "end"))
    o += legend_col(s, L.X(1.12), L.Y(2.9), [(O["load"], DASH_SER, f"in water (ε{sub('r', s)} = {EPS_R}), unscreened"),
                                              (SER[1], None, "in water with plasma salt, screened")])
    # right: lambda_D against I
    iss = logs(1e-4, 0.3, 61)
    o.append(curve(s, R, iss, [lam_d(i) for i in iss], SER[0]))
    for i, name, val, dx, dy, anc in ((1e-3, "1 mM buffer", f"{lam_d(1e-3):.2f} nm", 10, -22, "start"),
                                      (I_PLASMA, f"plasma, {I_PLASMA * 1e3:.1f} mM", f"{ld:.3f} nm", -10, 24, "end")):
        x, y = R.X(i), R.Y(lam_d(i))
        o.append(dot(s, x, y, SER[0], r=5))
        o.append(H.label(s, x + dx, y + dy, name, "label2", I["primary"], anc))
        o.append(H.label(s, x + dx, y + dy + 16, val, "label2", I["secondary"], anc))
    o.append(H.label(s, R.X(1.3e-4), R.Y(0.75), f"1 mM reaches {lam_d(1e-3) / ld:.1f}×", "label2", I["secondary"]))
    o.append(H.label(s, R.X(1.3e-4), R.Y(0.75) + 16, "as far as plasma", "label2", I["secondary"]))
    o.append(H.label(s, R.X(2.5e-2) + 8, R.Y(lam_d(2.5e-2)) - 12, "slope −½", "label2", I["secondary"]))
    aria = ("Two panels. Left: the interaction energy of two elementary charges in water against their separation, in "
            f"units of kBT. A dashed brown curve is the unscreened energy in water, which crosses one kBT at the Bjerrum "
            f"length {L_B:.2f} nanometres. A solid blue curve is the same energy screened by plasma salt; it is "
            f"{L_B * math.exp(-1 / ld):.2f} kBT at 1 nanometre and {L_B / 2 * math.exp(-2 / ld):.2f} at 2. A dotted vertical "
            f"line marks the Debye length {ld:.3f} nanometres. Right: log-log plot of the Debye length against ionic strength "
            f"from 0.1 to 300 millimolar, a red line of slope minus one half, {lam_d(1e-3):.2f} nanometres at 1 millimolar "
            f"and {ld:.3f} at plasma strength, {I_PLASMA * 1e3:.1f} millimolar.")
    hl = [[L.X(r), [L.Y(min(4, L_B / r)), L.Y(L_B / r * math.exp(-r / ld))],
           f"r = {r:.2f} nm: {L_B / r:.2f} kBT unscreened, {L_B / r * math.exp(-r / ld):.3f} kBT screened"]
          for r in lin(0.2, 3.0, 113)]
    hr = [[R.X(i), R.Y(lam_d(i)), f"I = {i * 1e3:.3g} mM: λD = {lam_d(i):.3g} nm"] for i in logs(1e-4, 0.3, 113)]
    return svg(VB, aria, s, o, H.hover_attr([panel_hover(L, hl), panel_hover(R, hr)]))


# ================================================================ svg #17 (Fig. 16): Nernst potentials and the pump bill
RTF = RG * TB / FARADAY * 1e3                         # mV, 26.73 (Prop. 5.2)
IONS = [("K⁺", 1, 4e-3, 140e-3), ("Na⁺", 1, 145e-3, 12e-3), ("Cl⁻", -1, 116e-3, 4e-3), ("Ca²⁺", 2, 1.8e-3, 0.1e-6)]
V_REST = -90.0                                        # mV (line 1058)


def nernst(z, co, ci):
    return RTF / z * math.log(co / ci)


def fig17():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    p = "m0f17_"
    L = Ax((90, 40, 360, 320), (0, 1), (-120, 150))
    R = Ax((490, 40, 735, 320), (0, 2), (0, 60))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, L, [], [(v, mn(v, "{:.0f}", True)) for v in range(-100, 151, 50)], None, "equilibrium potential (mV)",
              ylab_x=36)
    o += axes(s, R, [], [(v, f"{v}") for v in range(0, 61, 10)], None, "cost per mole of Ca²⁺ (kJ/mol)", ylab_x=R.x0 - 44)
    o.append(H.label(s, (L.x0 + L.x1) / 2, 22, "where each ion would sit at rest", "label", I["primary"], "middle"))
    o.append(H.label(s, (R.x0 + R.x1) / 2, 22, "the bill §3 was let off", "label", I["primary"], "middle"))
    E = {n: nernst(z, co, ci) for n, z, co, ci in IONS}
    o.append(H.line(s, L.x0, L.Y(V_REST), L.x1, L.Y(V_REST), I["primary"], "curve"))
    o.append(H.label(s, L.x1 - 4, L.Y(V_REST) + 20, f"resting potential {mn(V_REST, '{:.0f}')} mV", "label2", I["primary"], "end"))
    xpos = {"K⁺": 0.14, "Ca²⁺": 0.30, "Na⁺": 0.62, "Cl⁻": 0.90}
    hl = []
    for n, z, co, ci in IONS:
        x, y = L.X(xpos[n]), L.Y(E[n])
        o.append(H.line(s, x - 14, y, x + 14, y, ION, "curve"))
        o.append(dot(s, x, y, ION, r=4.5))
        hl.append([x, y, f"{n}: {co * 1e3:g} mM out, {ci * 1e3:g} mM in, E = {mn(E[n], '{:.1f}', True)} mV"])
    o.append(H.label(s, L.X(0.14) - 16, L.Y(E["K⁺"]) + 20, f"K⁺ {mn(E['K⁺'])} mV", "label2", I["primary"]))
    o.append(H.label(s, L.X(0.90), L.Y(E["Cl⁻"]) - 26, f"Cl⁻ {mn(E['Cl⁻'])} mV", "label2", I["primary"], "middle"))
    o.append(H.label(s, L.X(0.62) - 20, L.Y(E["Na⁺"]) + 5, f"Na⁺ {mn(E['Na⁺'], '{:.1f}', True)} mV", "label2", I["primary"],
                     "end"))
    o.append(H.label(s, L.X(0.30) + 20, L.Y(E["Ca²⁺"]) + 5, f"Ca²⁺ {mn(E['Ca²⁺'], '{:.1f}', True)} mV", "label2", I["primary"]))
    for n, dx in (("Na⁺", 26), ("Ca²⁺", -26)):
        xa = L.X(xpos[n]) + dx
        o.append(H.arrow(s, p, xa, L.Y(V_REST) - 3, xa, L.Y(E[n]) + 3, "geometry", both=True))
        o.append(H.label(s, xa + 6, L.Y((E[n] + V_REST) / 2) + 5, f"{E[n] - V_REST:.0f} mV", "label2", I["secondary"]))
    # right: the bill
    sr = RT * math.log(1e-3 / 0.1e-6)                 # §3 reticulum climb, 10^4
    chem = RT * math.log(1.8e-3 / 0.1e-6)
    elec = 2 * FARADAY * 0.090 / 1e3
    bw = 66
    bars = [(0.5, [(sr, SER[1])], "into the SR", "chemical only"),
            (1.5, [(chem, SER[1]), (elec, SER[0])], "out of the cell", "chemical + electrical")]
    hr = []
    for xc, segs, name, note in bars:
        base = 0.0
        for v, col in segs:
            o.append(f'<rect x="{R.X(xc) - bw / 2:.2f}" y="{R.Y(base + v):.2f}" width="{bw}" height="{R.Y(base) - R.Y(base + v):.2f}" '
                     f'fill="{col}"/>')
            base += v
        o.append(H.label(s, R.X(xc), R.y0 + 20, name, "label2", I["primary"], "middle"))
        o.append(H.label(s, R.X(xc), R.y0 + 36, f"({note})", "label2", I["secondary"], "middle"))
        o.append(H.label(s, R.X(xc), R.Y(base) - 8, f"{base:.2f}", "label", I["primary"], "middle"))
        hr.append([R.X(xc), R.Y(base), f"{name}: " + " + ".join(f"{v:.2f}" for v, _ in segs) + f" = {base:.2f} kJ/mol"])
    xr = R.X(1.5) + bw / 2 + 6
    o.append(H.label(s, xr, R.Y(chem / 2) + 4, f"{chem:.2f}", "label2", I["primary"]))
    o.append(H.label(s, xr, R.Y(chem + elec / 2) + 4, f"{elec:.2f}", "label2", I["primary"]))
    for k, (col, txt) in enumerate(((SER[1], "chemical, R" + sub("g", s) + "T ln(c" + sub("out", s) + "/c" + sub("in", s) + ")"),
                                    (SER[0], "electrical, zFΔφ = 2F × 90 mV"))):
        yy = R.top + 16 + 20 * k
        o.append(f'<rect x="{R.x0 + 10}" y="{yy - 10:.2f}" width="22" height="11" fill="{col}"/>')
        o.append(H.label(s, R.x0 + 40, yy, txt, "label2", I["primary"]))
    gap = chem + elec - sr
    for k, txt in enumerate((f"gap {gap:.1f} kJ/mol =", f"{elec:.1f} electrical ({100 * elec / gap:.0f} %)",
                             f"+ {chem - sr:.1f} steeper gradient")):
        o.append(H.label(s, R.x0 + 6, R.top + 80 + 16 * k, txt, "label2", I["secondary"]))
    aria = ("Two panels. Left: the Nernst potentials of four ions in skeletal muscle on one scale from minus 120 to plus "
            f"150 millivolts, each a blue mark: potassium {mn(E['K⁺'])}, chloride {mn(E['Cl⁻'])}, sodium "
            f"{mn(E['Na⁺'], plus=True)} and calcium {mn(E['Ca²⁺'], plus=True)} millivolts. A black line marks the resting "
            f"membrane potential, minus 90, which lies almost on potassium and chloride; blue arrows show sodium "
            f"{E['Na⁺'] - V_REST:.0f} and calcium {E['Ca²⁺'] - V_REST:.0f} millivolts away from it. Right: the cost of "
            f"pumping one mole of calcium. Into the sarcoplasmic reticulum it is {sr:.1f} kilojoules per mole, chemical work "
            f"only. Out of the cell it is {chem:.1f} chemical plus {elec:.1f} electrical, in red, {chem + elec:.1f} in total.")
    return svg(VB, aria, s, o, H.hover_attr([panel_hover(L, hl), panel_hover(R, hr)]))


FIGS = {
    5: ("Log-log plot of relative counting noise against concentratio", fig5),
    6: ("Energy against separation for a calcium-oxygen ion pair. A d", fig6),
    7: ("Log-log plot of predicted against measured bulk modulus for ", fig7),
    10: ("Straight line of Gibbs free energy against the logarithm of ", fig10),
    11: ("Curve of the Gibbs free energy of ATP hydrolysis against cyt", fig11),
    14: ("Square log-log plot of predicted against measured modulus ov", fig14),
    15: ("Relative stiffness against temperature from 10 to 50 degrees", fig15),
    16: ("Two panels. Left: the interaction energy of two elementary c", fig16),
    17: ("Two panels. Left: the equilibrium potential of four ions in ", fig17),
}
