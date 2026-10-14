"""Module 2 plots in the house style (group `plots`): main-text plots #3, #7-#11 at 760 px and the plot-type
problem figures C6, C7, D2, D6, D8, K2-K8 (#17, #18, #23, #27, #29, #34-#46) at 400 px.

Every plotted number is computed here from the formula, constant or script the module states:
  sigma = M/Z (Prop. 3.2-3.3), the Reuss/Voigt bracket (sec. 5), the fall force (6.1), the mechanostat (7.1),
  Prop. 7.3's two Hill arms, the sec. 8 lab script, tau = T rho / J (4.1), Lemma 7.2, and the K2-K8 scripts
  (ported line for line; their printed numbers are asserted). K4's damage model also draws C6 (#17).
"""
import math
from functools import lru_cache

import numpy as np

import house as H
from m05.plots_main import Ax, axes, curve, dot, hover, legend, mn, svg
from m05.plots_prob import Plot, hov
from m05.plots_prob import label as plabel
from m05.plots_prob import legend as plegend
from m05.plots_prob import svg as psvg

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"
BOXFILL = "#f7f4ef"
W = 400                                  # problem figures: viewBox width = rendered width
DASH = (7, 4)


def sub(t, s, size="label2"):
    return H.sub(t, s, size)


# ================================================================ module constants (Appendix, lab code)
E = 17e9
R_F, R_I = 0.014, 0.007                                   # femoral tube (m)
Z_H = math.pi / 4 * (R_F ** 4 - R_I ** 4) / R_F           # 2.02e-6 m^3
A_SOLID = math.sqrt(R_F ** 2 - R_I ** 2)                  # equal-area solid rod radius
Z_S = math.pi / 4 * A_SOLID ** 3
EPS_LO, EPS_HI, K_GAIN = 1000e-6, 1500e-6, 80.0
SIG_Y = 130.0                                             # MPa
MEFF, HFALL, G, KS = 28.0, 0.5, 9.81, 5e4
F_PEAK = math.sqrt(2 * KS * MEFF * G * HFALL)             # (6.1) boxed, N
F_EXACT = MEFF * G * (1 + math.sqrt(1 + 2 * KS * HFALL / (MEFF * G)))
U_FALL = MEFF * G * HFALL                                 # 137 J


def rate71(Z, M, Z0, k=K_GAIN):
    """(7.1) as the lab and K1/K4 code write it."""
    e = M / (Z * E)
    if e > EPS_HI:
        return k * Z * (e - EPS_HI)
    if e < EPS_LO:
        return k * Z * (e - EPS_LO)
    return 0.0


# ================================================================ svg #3: bending stress vs moment
def fig3():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 40, 735, 320), (0, 300), (0, 250))
    sh = lambda m: m / Z_H / 1e6           # noqa: E731  MPa
    ss = lambda m: m / Z_S / 1e6           # noqa: E731
    mh, ms = SIG_Y * 1e6 * Z_H, SIG_Y * 1e6 * Z_S
    assert round(Z_H * 1e6, 2) == 2.02 and round(sh(200)) == 99, (Z_H, sh(200))     # line 271
    o = axes(s, ax, [(v, f"{v}") for v in (0, 50, 100, 150, 200, 250, 300)],
             [(v, f"{v}") for v in (0, 50, 100, 150, 200, 250)], "bending moment M (N·m)", "peak bending stress σ (MPa)")
    o.append(H.line(s, ax.x0, ax.Y(SIG_Y), ax.x1, ax.Y(SIG_Y), I["primary"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.x0 + 8, ax.Y(SIG_Y) - 8, "tensile yield σ" + sub("Y", s) + " = 130 MPa", "label2", I["primary"]))
    ms_ = [3 * i for i in range(101)]
    o.append(curve(s, ax, [0, 300], [0, ss(300)], SER[0], "curve_multi"))
    o.append(curve(s, ax, [0, 300], [0, sh(300)], SER[1], "curve_multi"))
    o.append(dot(s, ax.X(ms), ax.Y(SIG_Y), O["flag"]))
    o.append(H.label(s, ax.X(ms) - 10, ax.Y(SIG_Y) - 9, f"solid yields at {ms:.0f} N·m", "label2", I["primary"], "end"))
    o.append(dot(s, ax.X(mh), ax.Y(SIG_Y), O["flag"]))
    o.append(H.label(s, ax.X(mh) + 8, ax.Y(SIG_Y) + 20, "femur yields", "label2", I["primary"]))
    o.append(H.label(s, ax.X(mh) + 8, ax.Y(SIG_Y) + 36, f"at {mh:.0f} N·m", "label2", I["primary"]))
    o.append(dot(s, ax.X(200), ax.Y(sh(200)), O["flag"]))
    o.append(H.label(s, ax.X(206), ax.Y(sh(200)) + 22, f"vigorous activity, M = 200 N·m:", "label2", I["primary"]))
    o.append(H.label(s, ax.X(206), ax.Y(sh(200)) + 38, f"σ = {sh(200):.0f} MPa, safety factor {SIG_Y / sh(200):.2f}",
                     "label2", I["primary"]))
    o.append(H.label(s, ax.X(130), ax.Y(166), "solid rod, equal area", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(130), ax.Y(166) + 16, f"(radius {A_SOLID * 1e3:.1f} mm)", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(298), ax.Y(172), "hollow femur", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(298), ax.Y(172) + 16, "(R = 14, r = 7 mm)", "label2", I["secondary"], "end"))
    o += legend(s, ax.x0 + 12, ax.top + 14, [(SER[0], None, f"solid rod, Z = {Z_S * 1e6:.2f} cm³"),
                                             (SER[1], None, f"hollow femur, Z = {Z_H * 1e6:.2f} cm³")])
    aria = (f"Peak bending stress sigma = M/Z against bending moment from 0 to 300 newton metres for the hollow femur "
            f"(Z = {Z_H * 1e6:.2f} cubic centimetres, blue) and a solid rod of equal area and mass (Z = {Z_S * 1e6:.2f}, red). "
            f"The solid rod reaches the dashed 130 megapascal tensile yield line at {ms:.0f} N m, the femur at {mh:.0f} N m. "
            f"At the vigorous-activity moment 200 N m the femur carries {sh(200):.0f} MPa, a safety factor of {SIG_Y / sh(200):.2f}.")
    hv = hover(ax, [ax.X(m) for m in ms_], [[ax.Y(ss(m)), ax.Y(sh(m))] for m in ms_],
               [f"M = {m} N·m: solid {ss(m):.0f} MPa, femur {sh(m):.0f} MPa" for m in ms_])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #7: the Reuss-Voigt bracket, three end-member sets
def bracket(em, ec, v=0.5):
    return 1 / (v / em + (1 - v) / ec), v * em + (1 - v) * ec


def fig7():
    VB = (0, 0, 760, 372)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((40, 40, 720, 290), (1, 1000), (0, 1), xlog=True)
    em_, ec_ = "E" + sub("m", s), "E" + sub("c", s)
    rows = [(("this module’s round values", f"{em_} = 100, {ec_} = 1 GPa"), 100, 1.0, 95),
            (("Module 0’s derived apatite", f"{em_} = 143, {ec_} = 1.07 GPa"), 143, 1.07, 165),
            (("measured apatite", f"{em_} = 114, {ec_} = 1.07 GPa"), 114, 1.07, 235)]
    got = [tuple(round(x, 2 if x < 10 else 1) for x in bracket(em, ec)) for _, em, ec, _ in rows]
    assert got == [(1.98, 50.5), (2.12, 72.0), (2.12, 57.5)], got                       # lines 348-350
    eta = [(17 - 0.5 * ec) / (0.5 * em) for _, em, ec, _ in rows]
    assert (round(eta[0], 2), round(eta[1], 2)) == (0.33, 0.23), eta                     # line 350
    o = [H.line(s, ax.x0, ax.y0, ax.x1, ax.y0, I["axis"], "axis")]
    for v in (1, 3, 10, 30, 100, 300, 1000):
        o.append(H.line(s, ax.X(v), ax.y0, ax.X(v), ax.y0 + 5, I["axis"], "leader"))
        o.append(H.label(s, ax.X(v), ax.y0 + 20, f"{v}", "tick", I["secondary"], "middle"))
    o.append(H.label(s, (ax.x0 + ax.x1) / 2, ax.y0 + 46, "Young’s modulus E (GPa, log scale)", "label", I["primary"], "middle"))
    x17 = ax.X(17)
    o.append(H.line(s, x17, 54, x17, ax.y0, I["primary"], "ref", H.DASH_REF))
    o.append(H.label(s, x17 + 8, 50, "measured cortical bone, 17 GPa", "label2", I["primary"]))
    panels = []
    cap = s(7)
    for k, (name, em, ec, y) in enumerate(rows):
        er, ev = bracket(em, ec)
        col = SER[k]
        xa, xb = ax.X(er), ax.X(ev)
        o.append(f'<line x1="{xa:.2f}" y1="{y}" x2="{xb:.2f}" y2="{y}" stroke="{col}" stroke-width="{s(5):.2f}"/>')
        for xx in (xa, xb):
            o.append(f'<line x1="{xx:.2f}" y1="{y - cap:.2f}" x2="{xx:.2f}" y2="{y + cap:.2f}" stroke="{col}" '
                     f'stroke-width="{s(2.5):.2f}"/>')
        o.append(H.label(s, 560, y - 3, name[0], "label2", I["primary"]))
        o.append(H.label(s, 560, y + 13, name[1], "label2", I["secondary"]))
        o.append(H.label(s, xa - 10, y + 4.5, f"Reuss {er:.2f}", "label2", I["secondary"], "end"))
        o.append(H.label(s, xb + 10, y + 4.5, f"Voigt {ev:.1f}", "label2", I["secondary"]))
        if k == 1:
            o.append(H.label(s, (xa + x17) / 2, y + 22, f"{17 / er:.1f}× above the floor", "label2", I["secondary"], "middle"))
            o.append(H.label(s, (x17 + xb) / 2, y + 22, f"{ev / 17:.1f}× below the ceiling", "label2", I["secondary"], "middle"))
        panels.append(([ax.x0, y - 34, ax.x1, y + 34],
                       [[xa, y, f"Reuss floor {er:.2f} GPa"], [x17, y, f"measured 17 GPa: {17 / er:.1f}× floor, {ev / 17:.1f}× below ceiling"],
                        [xb, y, f"Voigt ceiling {ev:.1f} GPa ({ev / er:.0f}× the floor)"]]))
    o.append(H.label(s, ax.x0, 362, f"K8’s recruited fraction η at v{sub('m', s)} = 0.5: {eta[0]:.2f} with the round 100 GPa, "
                     f"{eta[1]:.2f} with the derived 143 GPa", "label2", I["primary"]))
    aria = ("Three Reuss-to-Voigt brackets on a logarithmic modulus axis from 1 to 1000 gigapascals, at mineral fraction 0.5. "
            "Red: this module's round end members 100 and 1 gigapascal, 1.98 to 50.5. Blue: Module 0's derived apatite 143 with "
            "measured collagen 1.07, 2.12 to 72.0, a factor of 34; 17 sits 8.0 times above its floor and 4.2 times below its "
            "ceiling. Orange: measured apatite 114, 2.12 to 57.5. A dashed black line marks the measured 17 gigapascals, inside "
            "all three. The recruited fraction eta of K8 is 0.33 with the round values and 0.23 with the derived apatite.")
    return svg(VB, aria, s, o, H.hover_attr(panels))


# ================================================================ svg #8: fall force against hip strength
def fig8():
    VB = (0, 0, 760, 370)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 30, 740, 280), (0, 3), (0, 4.6))
    assert round(F_PEAK / 1e3, 1) == 3.7 and round(F_EXACT / 1e3, 2) == 3.99, (F_PEAK, F_EXACT)   # line 415
    fk = F_PEAK / 1e3
    bars = [("fall impact force", f"(6.1), boxed form: {fk:.1f} kN", fk, O["load"], "none"),
            ("healthy hip strength", f"safety factor {4.0 / fk:.2f}", 4.0, T["bone"][0], T["bone"][1]),
            ("osteoporotic hip", f"safety factor {2.0 / fk:.2f}", 2.0, T["bone_shade"][0], T["bone"][1])]
    o = axes(s, ax, [], [(v, f"{v}") for v in (0, 1, 2, 3, 4)], None, "force (kN)", ylab_x=36)
    hv = []
    for i, (a, b, v, fill, line) in enumerate(bars):
        xc = ax.X(i + 0.5)
        stroke = "none" if i == 0 else line
        o.append(f'<rect x="{xc - 60:.2f}" y="{ax.Y(v):.2f}" width="120" height="{ax.y0 - ax.Y(v):.2f}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{s(1.2):.2f}"/>')
        if i:
            o.append(H.label(s, xc, ax.Y(v) - 8, f"{v:.1f} kN", "label2", I["primary"], "middle"))
        o.append(H.label(s, xc, ax.y0 + 20, a, "label2", I["primary"], "middle"))
        o.append(H.label(s, xc, ax.y0 + 36, b, "label2", I["secondary"], "middle"))
        hv.append([xc, ax.Y(v), f"{a}: {v:.2f} kN" + ("" if i == 0 else f", S/F = {v / fk:.2f}")])
    # the load line, carried across so the two strengths read against it
    o.append(H.line(s, ax.X(0.5) + 60, ax.Y(fk), ax.x1, ax.Y(fk), O["load"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.x1, ax.Y(fk) - 8, f"fall force {fk:.1f} kN", "label2", I["primary"], "end"))
    xc = ax.X(0.5)
    o.append(H.line(s, xc - 60, ax.Y(F_EXACT / 1e3), xc + 60, ax.Y(F_EXACT / 1e3), I["primary"], "leader"))
    o.append(H.label(s, xc, ax.Y(F_EXACT / 1e3) - 8, f"exact form: {F_EXACT / 1e3:.2f} kN", "label2", I["secondary"], "middle"))
    me = "m" + sub("eff", s)
    o.append(H.label(s, 20, 350, f"√(2kₛ{me}gh) with {me} = 28 kg, h = 0.5 m, kₛ = 5×10⁴ N/m; the exact form of (6.1) "
                     f"adds the weight’s work over the stroke.", "label2", I["secondary"]))
    aria = (f"Bar chart in kilonewtons. The fall impact force from the boxed form of (6.1) is {fk:.1f} kilonewtons (brown bar), "
            f"with a thin mark at the exact form, {F_EXACT / 1e3:.2f}. A dashed brown line carries {fk:.1f} kN across the two "
            f"strength bars: the healthy hip, 4.0 kN (bone colour), lies above it with safety factor {4 / fk:.2f}; the "
            f"osteoporotic hip, 2.0 kN (darker bone colour), lies below it with safety factor {2 / fk:.2f}.")
    return svg(VB, aria, s, o, hover(ax, *zip(*hv)))


# ================================================================ svg #9 / #18: the mechanostat (7.1)
def mech_rate(e_us):
    """(7.1) per unit bone, (1/Z) dZ/dt = k (eps - threshold), in percent per day."""
    e = e_us * 1e-6
    if e > EPS_HI:
        return 100 * K_GAIN * (e - EPS_HI)
    if e < EPS_LO:
        return 100 * K_GAIN * (e - EPS_LO)
    return 0.0


def fig9():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    p = "m2f9_"
    ax = Ax((90, 30, 735, 320), (0, 2500), (-9, 9))
    es = list(range(0, 2501, 25))
    o = [f"<defs>{H.markers(p, s)}</defs>",
         f'<rect x="{ax.X(1000):.2f}" y="{ax.top}" width="{ax.X(1500) - ax.X(1000):.2f}" height="{ax.y0 - ax.top}" fill="{BOXFILL}"/>']
    o += axes(s, ax, [(v, f"{v}") for v in (0, 500, 1000, 1500, 2000, 2500)], [(v, mn(v, "{:.0f}", True)) for v in (-8, -4, 0, 4, 8)],
              "peak strain ε (µε)", "(1/Z) dZ/dt  (% per day)")
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["rule"], "leader"))
    o.append(curve(s, ax, [0, 1000, 1500, 2500], [mech_rate(e) for e in (0, 1000, 1500, 2500)], SER[0]))
    o.append(H.label(s, ax.X(1250), ax.Y(5.6), "lazy zone", "label", I["primary"], "middle"))
    o.append(H.label(s, ax.X(1250), ax.Y(5.6) + 18, "dZ/dt = 0", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(1000), ax.Y(-8.2), f"ε{sub('lo', s)} = 1000", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(1500), ax.Y(-8.2), f"ε{sub('hi', s)} = 1500", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(1530), ax.Y(7.6), "formation (overload)", "label", I["primary"]))
    o.append(H.label(s, ax.X(1530), ax.Y(7.6) + 18, f"k Z (ε − ε{sub('hi', s)}): bone gained", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(520), ax.Y(-5.6), "resorption (disuse)", "label", I["primary"]))
    o.append(H.label(s, ax.X(520), ax.Y(-5.6) + 18, f"k Z (ε − ε{sub('lo', s)}): bone lost", "label2", I["secondary"]))
    o.append(dot(s, ax.X(1250), ax.Y(0), O["flag"]))
    o.append(H.label(s, ax.X(1250), ax.Y(0) + 24, "habitual 1250 µε (§8)", "label2", I["primary"], "middle"))
    # the feedback: remodeling moves strain back toward the band
    yA = ax.Y(1.6)
    o.append(H.arrow(s, p, ax.X(420), yA, ax.X(900), yA, "dim"))
    o.append(H.arrow(s, p, ax.X(2300), ax.Y(-1.6), ax.X(1600), ax.Y(-1.6), "dim"))
    o.append(H.label(s, ax.X(420), yA - 9, "losing bone raises ε", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(2300), ax.Y(-1.6) + 21, "gaining bone lowers ε", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(2480), ax.Y(-6.3), f"slope k = {K_GAIN:.0f} per strain per day", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(2480), ax.Y(-6.3) + 16, "(the Appendix toy gain)", "label2", I["muted"], "end"))
    aria = ("The mechanostat law (7.1): fractional remodeling rate in percent per day against peak strain from 0 to 2500 "
            "microstrain, with the Appendix gain k = 80. The red line falls with slope k below 1000 microstrain (resorption, "
            "bone lost, minus 8 percent per day at zero strain), is zero across the shaded lazy zone from 1000 to 1500, and "
            "rises with the same slope above 1500 (formation, plus 8 percent per day at 2500). Grey arrows show the feedback: "
            "losing bone raises the strain, gaining bone lowers it, so strain is driven back into the band. An orange dot marks "
            "the habitual 1250 microstrain of the section 8 lab.")
    hv = hover(ax, [ax.X(e) for e in es], [ax.Y(mech_rate(e)) for e in es],
               [f"ε = {e} µε: {mn(mech_rate(e), '{:.1f}', True)} % per day" for e in es])
    return svg(VB, aria, s, o, hv)


def fig18():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m2f18_"
    P = Plot(s, (62, 30, 376, 202), (0, 2500), (-9, 9))
    es = list(range(0, 2501, 25))
    o = [f"<defs>{H.markers(p, s)}</defs>",
         f'<rect x="{P.X(1000):.2f}" y="{P.y1}" width="{P.X(1500) - P.X(1000):.2f}" height="{P.y0 - P.y1}" fill="{BOXFILL}"/>',
         P.axes([(v, f"{v}") for v in (0, 1000, 1500, 2500)], [(v, mn(v, "{:.0f}", True)) for v in (-8, 0, 8)],
                "peak strain ε (µε)", "(1/Z) dZ/dt (%/day)", ytx=14)]
    o.append(H.line(s, P.x0, P.Y(0), P.x1, P.Y(0), I["rule"], "leader"))
    o.append(P.curve([0, 1000, 1500, 2500], [mech_rate(e) for e in (0, 1000, 1500, 2500)], SER[0]))
    o.append(plabel(s, P.X(1250), P.Y(5.0), "lazy", "label2", I["primary"], "middle"))
    o.append(plabel(s, P.X(1250), P.Y(5.0) + 15, "zone", "label2", I["primary"], "middle"))
    o.append(plabel(s, P.X(1000) - 4, P.Y(-7.4), f"ε{sub('lo', s)}", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(1500) + 4, P.Y(-7.4), f"ε{sub('hi', s)}", "label2", I["primary"]))
    o.append(plabel(s, P.X(1600), P.Y(7.6), "formation", "label2", I["primary"]))
    o.append(plabel(s, P.X(80), P.Y(-1.6), "resorption", "label2", I["primary"]))
    o.append(H.arrow(s, p, P.X(260), P.Y(1.7), P.X(880), P.Y(1.7), "dim"))
    o.append(H.arrow(s, p, P.X(2380), P.Y(-1.7), P.X(1620), P.Y(-1.7), "dim"))
    o.append(plabel(s, P.X(2420), P.Y(-1.7) + 17, "strain driven into band", "label2", I["secondary"], "end"))
    aria = ("Problem C7 plot: the mechanostat law (7.1), fractional remodeling rate in percent per day against peak strain, "
            "with gain k = 80. Negative below 1000 microstrain (resorption), zero in the shaded lazy zone from 1000 to 1500, "
            "positive above 1500 (formation). Grey arrows show the feedback driving strain back into the band, which is why the "
            "bone settles at a target strain, not a target size.")
    hv = hov(P, es, [[mech_rate(e) for e in es]], lambda i: f"ε = {es[i]} µε: {mn(mech_rate(es[i]), '{:.1f}', True)} %/day")
    return psvg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #10: Prop. 7.3, the law from two Hill arms
XI = 0.05


def hill_net(e, n):
    q = ((1 - XI) / XI) ** (1 / n)
    eF, eR = q * 1500.0, 1000.0 / q
    tF = e ** n / (eF ** n + e ** n)
    tR = e ** n / (eR ** n + e ** n)
    return tF - (1 - tR), eF


def hill_slope_hi(n):
    """d(net)/d eps at eps_hi, both arms (Prop. 7.3 proof, theta' = n theta (1 - theta) / eps)."""
    q = ((1 - XI) / XI) ** (1 / n)
    eF, eR, e = q * 1500.0, 1000.0 / q, 1500.0
    tF = e ** n / (eF ** n + e ** n)
    tR = e ** n / (eR ** n + e ** n)
    return n * tF * (1 - tF) / e + n * tR * (1 - tR) / e


def fig10():
    VB = (0, 0, 760, 430)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 60, 735, 350), (200, 4500), (-1.05, 1.05))
    es = list(range(200, 4501, 25))
    half = {n: hill_net(1.0, n)[1] for n in (3, 6, 12)}
    assert [round(half[n], -1 if n == 3 else 0) for n in (3, 6, 12)] == [4000, 2450, 1917], half   # lines 496, 547
    slope = hill_slope_hi(6)
    pw = lambda e: slope * (e - 1500) if e > 1500 else (slope * (e - 1000) if e < 1000 else 0.0)   # noqa: E731
    o = [f'<rect x="{ax.X(1000):.2f}" y="{ax.top}" width="{ax.X(1500) - ax.X(1000):.2f}" height="{ax.y0 - ax.top}" fill="{BOXFILL}"/>']
    o += axes(s, ax, [(v, f"{v}") for v in (500, 1000, 1500, 2000, 3000, 4000)],
              [(v, mn(v, "{:g}")) for v in (-1, -0.5, 0, 0.5, 1)], "peak strain ε (µε)",
              f"net remodeling rate / Φ{H.sub('F', s)}")
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["rule"], "leader"))
    o.append(H.line(s, ax.X(3000), ax.top + 30, ax.X(3000), ax.y0, I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(3000) - 6, ax.Y(-0.5), "Frost’s overload", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(3000) - 6, ax.Y(-0.5) + 16, "threshold ≈ 3000 µε", "label2", I["secondary"], "end"))
    o.append(curve(s, ax, [200, 1000, 1500, 4500], [pw(e) for e in (200, 1000, 1500, 4500)], I["muted"], "curve_multi", DASH))
    ec = list(range(200, 4501, 40)) + [4500]
    for n, col in ((3, SER[0]), (6, SER[1]), (12, SER[2])):
        o.append(curve(s, ax, ec, [hill_net(e, n)[0] for e in ec], col, "curve_multi"))
        o.append(dot(s, ax.X(half[n]), ax.Y(hill_net(half[n], n)[0]), col))
    o.append(H.label(s, ax.X(4000) - 8, ax.Y(hill_net(4000, 3)[0]) - 9, "n = 3: 4000", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(2450) + 9, ax.Y(hill_net(2450, 6)[0]) + 16, "n = 6: 2450", "label2", I["primary"]))
    o.append(H.label(s, ax.X(1917) - 9, ax.Y(hill_net(1917, 12)[0]) + 4, "n = 12: 1917", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(1250), ax.Y(-0.62), "lazy", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(1250), ax.Y(-0.62) + 16, "zone", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(1250), ax.Y(-0.62) + 32, "1000–1500", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(4480), ax.Y(-0.25), "piecewise law (7.1),", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(4480), ax.Y(-0.25) + 16, f"slope {slope * 1e4:.2f}×10⁻⁴ per µε (n = 6 at ε{sub('hi', s)})",
                     "label2", I["secondary"], "end"))
    o += legend(s, ax.x0, 30, [(SER[0], None, f"n{sub('H', s)} = 3"), (SER[1], None, f"n{sub('H', s)} = 6"),
                               (SER[2], None, f"n{sub('H', s)} = 12"), (I["muted"], DASH, "law (7.1)")])
    o.append(H.label(s, 600, 34, "dots: formation half on", "label2", I["secondary"]))
    aria = ("Proposition 7.3 drawn: net remodeling rate, normalised to the maximal formation rate, against peak strain from 200 "
            "to 4500 microstrain, as the difference of two Hill functions with cooperativity 3 (red), 6 (blue) and 12 (orange), "
            "each placed so its arm departs from zero by 5 percent at the thresholds 1000 and 1500. All three are near zero "
            "across the shaded lazy zone; the formation flux is half on at 4000, 2450 and 1917 microstrain (dots). A dashed "
            "grey line marks Frost's overload threshold near 3000. A dashed grey piecewise-linear curve is the module's law (7.1) "
            "with the n = 6 slope at the upper threshold.")
    hv = hover(ax, [ax.X(e) for e in es], [[ax.Y(hill_net(e, n)[0]) for n in (3, 6, 12)] for e in es],
               [f"ε = {e} µε: n=3 {mn(hill_net(e, 3)[0], '{:.2f}')}, n=6 {mn(hill_net(e, 6)[0], '{:.2f}')}, "
                f"n=12 {mn(hill_net(e, 12)[0], '{:.2f}')}" for e in es])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #11: the section 8 lab
@lru_cache(maxsize=None)
def lab_run(scale, days=400, dt=1.0):
    """Section 8 code, unchanged (Z0 = I_h/R, M_ref = 1250e-6 Z0 E)."""
    z0 = Z_H
    m = 1250e-6 * z0 * E
    Z, out = z0, []
    for _ in range(days + 1):
        out.append(Z)
        Z = max(Z + rate71(Z, scale * m, z0) * dt, 1e-8)
    return tuple(100 * np.array(out) / z0)


def fig11():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 50, 735, 320), (0, 400), (40, 145))
    cases = [(1.6, "+60 % load", SER[0]), (1.0, "habitual", SER[1]), (0.4, "disuse −60 %", SER[2])]
    up, mid, dn = (np.array(lab_run(c)) for c, _, _ in cases)
    t95 = {}
    for sc, z in ((1.6, up), (0.4, dn)):
        fr = (z - 100) / (z[-1] - 100)
        t95[sc] = int(np.argmax(fr >= 0.95))
    assert round(up[-1], 1) == 133.3 and round(dn[-1], 1) == 50.0 and t95 == {1.6: 24, 0.4: 36}, (up[-1], dn[-1], t95)
    tt = list(range(401))
    o = axes(s, ax, [(v, f"{v}") for v in (0, 100, 200, 300, 400)], [(v, f"{v}") for v in (40, 60, 80, 100, 120, 140)],
             "time (days)", "section modulus Z (% of initial)")
    tc = list(range(0, 80)) + list(range(80, 401, 10))
    for (sc, _, col), z in zip(cases, (up, mid, dn)):
        o.append(curve(s, ax, tc, [z[k] for k in tc], col, "curve_multi"))
    for sc, z, dy in ((1.6, up, 26), (0.4, dn, -14)):
        k = t95[sc]
        o.append(dot(s, ax.X(k), ax.Y(z[k]), O["flag"]))
        o.append(H.label(s, ax.X(k) + 10, ax.Y(z[k]) + dy, f"95 % of the change by day {k}", "label2", I["primary"]))
    o.append(H.label(s, ax.X(398), ax.Y(up[-1]) - 10, "+60 % load: 133 % = 1.6 × 1250/1500", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(398), ax.Y(100) - 10, "habitual: stays at 100 % (inside the band)", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(398), ax.Y(dn[-1]) - 10, "disuse −60 %: 50 % = 0.4 × 1250/1000", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(398), ax.Y(76), f"time constants 1/(kε{sub('hi', s)}) = {1 / (K_GAIN * EPS_HI):.1f} d, "
                     f"1/(kε{sub('lo', s)}) = {1 / (K_GAIN * EPS_LO):.1f} d", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(398), ax.Y(76) + 16, "(toy gain k = 80: speed only, never the end points)", "label2", I["muted"], "end"))
    o += legend(s, ax.x0, 30, [(c, None, t) for _, t, c in cases])
    aria = ("Section 8 lab output: section modulus in percent of its initial value over 400 days, integrating (7.1) for three "
            "load levels. The +60 percent load (red) rises and settles at 133 percent, 1.6 times 1250 over 1500; habitual load "
            "(blue) stays at 100 percent; disuse at minus 60 percent (orange) falls and settles at 50 percent, 0.4 times 1250 over "
            f"1000. Orange dots mark 95 percent of each change, reached by day {t95[1.6]} and day {t95[0.4]}; the time constants "
            "are 8.3 and 12.5 days.")
    hv = hover(ax, [ax.X(t) for t in tt[::2]], [[ax.Y(up[t]), ax.Y(mid[t]), ax.Y(dn[t])] for t in tt[::2]],
               [f"day {t}: +60 % {up[t]:.1f} %, habitual {mid[t]:.0f} %, disuse {dn[t]:.1f} %" for t in tt[::2]])
    return svg(VB, aria, s, o, hv)


# ================================================================ K4 model (also draws C6, #17)
K_Z0, K_MREF = 2.02e-6, 1250e-6 * 2.02e-6 * E


def k4_run(ramp_days, tau_r=14.0, load=1.6, days=400, dt=0.25):
    """K4's max_damage loop, verbatim, returning the trace. N_hab = n0 tau_r / 0.25 (habitual D = 0.25 for every tau_r)."""
    m_exp, n0, d_hab = 6.0, 5000.0, 0.25
    sig_hab = 1250e-6 * E
    nf_hab = n0 * tau_r / d_hab
    Z, D, out = K_Z0, d_hab, []
    for i in range(int(days / dt) + 1):
        frac = min(i * dt / ramp_days, 1.0) if ramp_days > 0 else 1.0
        M = K_MREF * (1 + (load - 1) * frac)
        D += (n0 / (nf_hab * ((M / Z) / sig_hab) ** (-m_exp)) - D / tau_r) * dt
        out.append(D)
        Z = max(Z + rate71(Z, M, K_Z0) * dt, 1e-9)
    return np.array(out)


@lru_cache(maxsize=None)
def k4_max(ramp_days, tau_r=14.0):
    return max(0.25, float(k4_run(ramp_days, tau_r).max()))


def k4_critical(tau_r):
    """brentq(max_damage - 1) on [1, 400] days, as K4 does (bisection here, same root)."""
    a, b = 1.0, 400.0
    for _ in range(60):
        c = 0.5 * (a + b)
        if (k4_max(a, tau_r) - 1) * (k4_max(c, tau_r) - 1) <= 0:
            b = c
        else:
            a = c
    return 0.5 * (a + b)


def fig17():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 62, 388, 226), (0, 20), (0, 1.25))
    dstep, dramp = k4_run(0), k4_run(84)
    assert (round(dstep.max(), 2), round(dramp.max(), 2)) == (1.12, 0.94), (dstep.max(), dramp.max())   # line 908
    wk = np.arange(len(dstep)) * 0.25 / 7
    keep = wk <= 20.0001
    ws, a, b = wk[keep], dstep[keep], dramp[keep]
    i1 = int(np.argmax(a >= 1.0))
    o = [P.axes([(v, f"{v}") for v in (0, 5, 10, 15, 20)], [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1)],
                "weeks after the load rises", "fatigue damage D", grid=(0.25, 0.5, 0.75))]
    o.append(H.line(s, P.x0, P.Y(1), P.x1, P.Y(1), I["primary"], "ref", H.DASH_REF))
    o.append(plabel(s, P.X(4.2), P.Y(1) - 7, "stress fracture, D = 1", "label2", I["primary"]))
    o.append(P.curve(ws, b, SER[1], multi=True))
    o.append(P.curve(ws, a, SER[0], multi=True))
    ka = int(a.argmax())
    o.append(P.dot(ws[ka], a[ka], SER[0]))
    o.append(plabel(s, P.X(ws[ka]) + 8, P.Y(a[ka]) - 6, f"step: peak {a[ka]:.2f}", "label2", I["primary"]))
    kb = int(b.argmax())
    o.append(P.dot(ws[kb], b[kb], SER[1]))
    o.append(plabel(s, P.x1, P.Y(1) - 7, f"ramp: peak {b[kb]:.2f}", "label2", I["primary"], "end"))
    o.append(H.line(s, P.X(14.4), P.Y(1) - 5, P.X(ws[kb]) + 4, P.Y(b[kb]) - 3, I["rule"], "leader"))
    o.append(plabel(s, P.X(19.6), P.Y(0.75) + 20, "both settle at 0.75", "label2", I["secondary"], "end"))
    o.append(plabel(s, P.X(0.3), P.Y(0.25) + 20, "habitual 0.25", "label2", I["secondary"]))
    o.append(plegend(s, 58, 22, [(SER[0], "+60 % load as a step", None), (SER[1], "same load, 84-day ramp", None)], gap=12))
    o.append(plabel(s, 58, 42, "K4 model: Miner damage minus 14-day repair", "label2", I["secondary"]))
    aria = ("Problem C6 plot, from K4's damage model: fatigue damage D over 20 weeks after the running load rises by 60 percent. "
            f"Applied as a step (red), damage outruns the 14-day repair, crosses the dashed stress-fracture line D = 1 in week "
            f"{ws[i1]:.1f} and peaks at {a[ka]:.2f}. The same load ramped over 84 days (blue) peaks at {b[kb]:.2f} and never "
            "fractures. Both settle at 0.75 once the bone has thickened, from the habitual 0.25.")
    idx = list(range(0, int(keep.sum()), 4))
    hv = hov(P, ws[idx], [a[idx], b[idx]], lambda i: f"week {ws[idx][i]:.1f}: step D = {a[idx][i]:.2f}, ramp D = {b[idx][i]:.2f}")
    return psvg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #23: D2, neutral axis at the centroid
def fig23():
    VB = (0, 0, W, 232)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m2f23_"
    cx, cy, Ro = 78, 112, 58
    ri = Ro / 2                                              # femoral proportions R/r = 2
    bone, line = T["bone"]
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o.append(f'<path d="M{cx - Ro},{cy} a{Ro},{Ro} 0 1 0 {2 * Ro},0 a{Ro},{Ro} 0 1 0 {-2 * Ro},0 Z '
             f'M{cx - ri},{cy} a{ri},{ri} 0 1 1 {2 * ri},0 a{ri},{ri} 0 1 1 {-2 * ri},0 Z" fill="{bone}" '
             f'fill-rule="evenodd" stroke="{line}" stroke-width="{s(1.4):.2f}"/>')
    # stress profile, side view of the same section: sigma = E kappa y, linear in y
    xp = 220
    o.append(H.line(s, cx - Ro - 8, cy, xp + 64, cy, I["primary"], "ref", H.DASH_REF))
    for yy in (cy - Ro, cy + Ro):
        o.append(H.line(s, cx, yy, xp, yy, I["rule"], "leader", (3, 3)))
    o.append(H.line(s, xp, cy - Ro, xp, cy + Ro, I["axis"], "axis"))
    for k in (-4, -3, -2, -1, 1, 2, 3, 4):
        y = cy + k * Ro / 4
        L = abs(k) * 13
        if k > 0:          # below the axis: tension, pulling away from the face
            o.append(H.arrow(s, p, xp, y, xp + L, y, "force", "geom"))
        else:              # above: compression, pushing into the face
            o.append(H.arrow(s, p, xp + L, y, xp, y, "geometry", "geom"))   # compression: SERIES[1] blue, as beam.py
    for y2, col in ((cy - Ro, SER[1]), (cy + Ro, SER[0])):     # compression blue above, tension red below
        o.append(f'<path d="M{xp},{cy} L{xp + 52},{y2}" fill="none" stroke="{col}" '
                 f'stroke-width="{s(1):.2f}" stroke-dasharray="{s(2):.1f} {s(2):.1f}"/>')
    o.append(H.com_mark(s, cx, cy))
    o.append(H.arrow(s, p, cx + ri + 6, cy, cx + ri + 6, cy + Ro - 4, "dim"))   # y toward the tension face, as beam.py
    o.append(plabel(s, cx + ri + 11, cy + Ro / 2 + 5, "y", "label", I["primary"], extra='font-style="italic"'))
    o.append(plabel(s, cx, cy + Ro + 20, "centroid C", "label2", I["primary"], "middle"))
    o.append(plabel(s, xp - 6, cy - Ro - 8, "compression", "label2", I["primary"]))
    o.append(plabel(s, xp - 6, cy + Ro + 20, "tension", "label2", I["primary"]))
    o.append(plabel(s, xp + 68, cy + 4.5, "neutral axis", "label2", I["primary"]))
    o.append(plabel(s, xp + 60, cy - Ro / 2, "σ = Eκy", "label2", I["primary"]))
    o.append(plabel(s, 10, 20, "∫σ dA = Eκ ∫y dA = 0 (no net axial force)", "label2", I["primary"]))
    o.append(plabel(s, 10, VB[3] - 10, "κ ≠ 0  ⇒  ∫y dA = 0  ⇒  the zero-stress line passes through C", "label2", I["primary"]))
    aria = ("Problem D2 figure. Left: a hollow bone cross-section (outer radius twice the inner) with its centroid C marked and "
            "the neutral axis dashed through it. Right: the same section seen side-on, with bending-stress arrows sigma = "
            "E kappa y growing linearly with distance y from the axis (y measured downward, toward the tension face): blue compression above, red tension below. Zero net axial force "
            "means the integral of sigma over the area vanishes, so the integral of y dA vanishes and the zero-stress line "
            "passes through the centroid.")
    return psvg(VB, aria, s, "".join(o))


# ================================================================ svg #27: D6, shear grows with radius; tau_max = sigma_max / 2
def fig27():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m2f27_"
    I_ = math.pi / 4 * (R_F ** 4 - R_I ** 4)
    J = 2 * I_
    Mt = 30.0                                                # N m, the everyday pivoting torque of sec. 4
    tmax, smax = Mt * R_F / J / 1e6, Mt * R_F / I_ / 1e6
    assert round(J * 1e8, 2) == 5.66 and round(tmax, 1) == 7.4, (J, tmax)                 # line 325
    cx, cy, Ro = 74, 150, 54
    ri = Ro / 2
    bone, line = T["bone"]
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o.append(f'<path d="M{cx - Ro},{cy} a{Ro},{Ro} 0 1 0 {2 * Ro},0 a{Ro},{Ro} 0 1 0 {-2 * Ro},0 Z '
             f'M{cx - ri},{cy} a{ri},{ri} 0 1 1 {2 * ri},0 a{ri},{ri} 0 1 1 {-2 * ri},0 Z" fill="{bone}" '
             f'fill-rule="evenodd" stroke="{line}" stroke-width="{s(1.4):.2f}"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{s(2):.2f}" fill="{I["primary"]}"/>')
    for mm in (8, 11, 14):                                   # tangential shear at radius rho, length proportional to rho
        x = cx + Ro * mm / 14
        L = 2.1 * mm
        o.append(H.arrow(s, p, x, cy, x, cy - L, "dim", "geom"))           # shear grey, as bone.py fig6
        o.append(H.arrow(s, p, 2 * cx - x, cy, 2 * cx - x, cy + L, "dim", "geom"))
    o.append(H.arrow(s, p, cx, cy, cx + Ro, cy, "geometry"))
    o.append(plabel(s, cx + Ro / 2 - 6, cy + 16, "ρ", "label", I["primary"], "middle", 'font-style="italic"'))
    # counter-clockwise torque, the same sense as the shear arrows (up on the right, down on the left)
    o.append(f'<path d="M{cx + 38},{cy - Ro - 12} A{Ro + 16},{Ro + 16} 0 0 0 {cx - 38},{cy - Ro - 12}" fill="none" '
             f'stroke="{O["load"]}" stroke-width="{s(2):.2f}" marker-end="url(#{p}a_load)"/>')
    o.append(plabel(s, cx, cy - Ro - 26, "T", "label", I["primary"], "middle", 'font-style="italic"'))
    o.append(plabel(s, cx, cy + Ro + 22, "τ ∝ ρ, largest", "label2", I["primary"], "middle"))
    o.append(plabel(s, cx, cy + Ro + 38, "at the surface", "label2", I["primary"], "middle"))
    P = Plot(s, (200, 74, 388, 220), (0, 14), (0, 18))
    o.append(f'<rect x="{P.X(0):.2f}" y="{P.y1}" width="{P.X(7) - P.X(0):.2f}" height="{P.y0 - P.y1}" fill="{BOXFILL}"/>')
    o.append(P.axes([(v, f"{v}") for v in (0, 7, 14)], [(v, f"{v}") for v in (0, 5, 10, 15)],
                    "distance from axis (mm)", "stress (MPa)", grid=(5, 10, 15), ytx=166))
    o.append(plabel(s, P.X(3.5), P.Y(16.2), "bore", "label2", I["secondary"], "middle"))
    ys = np.linspace(7, 14, 36)
    o.append(P.curve(ys, Mt * ys * 1e-3 / I_ / 1e6, SER[0], multi=True))
    o.append(P.curve(ys, Mt * ys * 1e-3 / J / 1e6, I["secondary"], multi=True))
    o.append(P.dot(14, smax, SER[0]))
    o.append(P.dot(14, tmax, I["secondary"]))
    o.append(plabel(s, P.X(14) - 6, P.Y(smax) - 9, f"{smax:.1f}", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(14) - 6, P.Y(tmax) - 9, f"{tmax:.1f}", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(6.6), P.Y(smax / 2) + 4.5, "σ = My/I", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(6.6), P.Y(tmax / 2) + 4.5, "τ = Tρ/J", "label2", I["primary"], "end"))
    o.append(plabel(s, 10, 20, "femoral tube R = 14, r = 7 mm, M = T = 30 N·m:", "label2", I["primary"]))
    o.append(plabel(s, 10, 37, f"τ{sub('max', s)} = σ{sub('max', s)}/2 because J = 2I", "label2", I["primary"]))
    o.append(plabel(s, 10, 278, "twist per unit moment, over curvature per unit", "label2", I["secondary"]))
    o.append(plabel(s, 10, 294, "moment: E/(2G) ≈ 2.5 for bone (E/G ≈ 5)", "label2", I["secondary"]))
    aria = ("Problem D6 figure. Left: a hollow femoral cross-section under torque T with grey shear arrows tangent to circles, "
            "their length growing linearly with radius rho, largest at the surface. Right: stress against distance from the axis "
            f"across the wall from 7 to 14 millimetres for M = T = 30 newton metres: bending stress My/I (red) reaches {smax:.1f} "
            f"megapascals at the surface, torsional shear T rho / J (grey) reaches {tmax:.1f}, half as much, because J = 2I. The "
            "twist per unit moment exceeds the curvature per unit moment by E/(2G), about 2.5 for bone.")
    hr = np.linspace(7, 14, 71)
    hv = hov(P, hr, [Mt * hr * 1e-3 / I_ / 1e6, Mt * hr * 1e-3 / J / 1e6],
             lambda i: f"{hr[i]:.1f} mm: σ = {Mt * hr[i] * 1e-3 / I_ / 1e6:.1f}, τ = {Mt * hr[i] * 1e-3 / J / 1e6:.1f} MPa")
    return psvg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #29: D8, the phase line of (7.1)
def fig29():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m2f29_"
    load = 1.6                                               # the lab's +60 % case: Z_eq = 1.6 x 1250/1500 Z0
    zeq, zlo = load * 1250 / 1500, load * 1250 / 1000
    f = lambda z: K_GAIN * (load * 1250e-6 - EPS_HI * z) if z < zeq else (                       # noqa: E731
        K_GAIN * (load * 1250e-6 - EPS_LO * z) if z > zlo else 0.0)      # dZ/dt in Z0 per day, (7.1) with eps = M/(ZE)
    assert round(1 / (K_GAIN * EPS_HI), 1) == 8.3                                              # line 765
    P = Plot(s, (62, 46, 388, 226), (0.8, 2.4), (-0.04, 0.07))
    zs = np.linspace(0.8, 2.4, 161)
    zf = zs[zs <= zeq]
    o = [f"<defs>{H.markers(p, s)}</defs>",
         P.axes([(v, f"{v:g}") for v in (0.8, 1.2, 1.6, 2.0, 2.4)], [(v, mn(v, "{:.2f}", True) if v else "0") for v in (-0.04, 0, 0.04)],
                "section modulus Z / Z₀", "dZ/dt (Z₀ per day)", ytx=13)]
    o.append(H.line(s, P.x0, P.Y(0), P.x1, P.Y(0), I["rule"], "leader"))
    o.append(P.curve(list(zs[zs >= zeq]), [f(z) for z in zs[zs >= zeq]], I["muted"], multi=True, dash=DASH))
    o.append(P.curve(list(zf) + [zeq], [f(z) for z in zf] + [0.0], SER[0]))
    o.append(P.dot(zeq, 0, O["flag"]))
    o.append(H.arrow(s, p, P.X(0.9), P.Y(0) + 12, P.X(1.22), P.Y(0) + 12, "dim"))
    o.append(plabel(s, P.X(0.9), P.Y(0) + 30, "grows toward", "label2", I["secondary"]))
    o.append(plabel(s, P.X(zeq) + 6, P.Y(0) - 10, f"Z{sub('eq', s)} = M/(Eε{sub('hi', s)}) = {zeq:.2f} Z₀", "label2", I["primary"]))
    o.append(plabel(s, P.X(1.0), P.Y(0.064), f"formation branch, slope −kε{sub('hi', s)} = −{K_GAIN * EPS_HI:.2f}/day", "label2",
                    I["primary"]))
    o.append(plabel(s, P.X(1.0), P.Y(0.064) + 16, f"⇒ stable, τ{sub('Z', s)} = 1/(kε{sub('hi', s)}) = {1 / (K_GAIN * EPS_HI):.1f} days",
                    "label2", I["primary"]))
    o.append(plabel(s, P.X(1.95), P.Y(-0.016), "rest of (7.1):", "label2", I["secondary"], "end"))
    o.append(plabel(s, P.X(1.95), P.Y(-0.016) + 15, "lazy zone, resorption", "label2", I["secondary"], "end"))
    o.append(plabel(s, 58, 22, "the lab’s +60 % load, k = 80", "label2", I["secondary"]))
    aria = ("Problem D8 plot: the phase line of the remodeling law for the section 8 lab's +60 percent load, dZ/dt in units of "
            "the initial section modulus per day against Z over Z0 from 0.8 to 2.4. The formation branch (red) is a straight "
            f"line of slope minus k epsilon-hi = minus {K_GAIN * EPS_HI:.2f} per day that reaches zero at Z_eq = M/(E epsilon-hi) "
            f"= {zeq:.2f} Z0 (orange dot); below it dZ/dt is positive, so the bone grows toward it and the fixed point is stable, "
            f"time constant {1 / (K_GAIN * EPS_HI):.1f} days. Dashed grey: the rest of (7.1), zero across the lazy zone up to "
            f"{zlo:.1f} Z0, then the resorption branch.")
    hv = hov(P, zs, [[f(z) for z in zs]], lambda i: f"Z = {zs[i]:.2f} Z₀: dZ/dt = {mn(f(zs[i]), '{:.3f}', True)} Z₀/day")
    return psvg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #34: K2, fall safety factor with age
@lru_cache(maxsize=None)
def k2_run(load=1.0, lower=0.0, band=True, years=100):
    """K2's cross_age loop, verbatim, also recording S/F each day (test before the update, as K2 does)."""
    S0, drift = 4000.0, 0.002
    Z, M = K_Z0, load * K_MREF
    sf, cross = [], None
    for day in range(int(years * 365)):
        f = (1 + drift * day / 365) * (1 - lower)
        e = M / (Z * E)
        if band:
            lo, hi = 1000e-6 * f, 1500e-6 * f
            rr = K_GAIN * Z * (e - hi) if e > hi else (K_GAIN * Z * (e - lo) if e < lo else 0.0)
        else:
            rr = K_GAIN * Z * (e - 1250e-6 * f)
        v = S0 * (Z / K_Z0) / F_PEAK
        sf.append(v)
        if v < 1 and cross is None:
            cross = round(30 + day / 365, 1)
        Z = max(Z + rr, 1e-9)
    return np.array(sf), cross


def fig34():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    cases = [(1.0, 0.0, SER[0], "one setpoint, baseline"), (1.1, 0.0, SER[1], "one setpoint, +10 % load"),
             (1.0, 0.1, SER[2], "one setpoint, 10 % lower")]
    runs = [k2_run(ld, lw, False) for ld, lw, _, _ in cases]
    bands = [k2_run(ld, lw, True) for ld, lw, _, _ in cases]
    assert [r[1] for r in runs] == [69.7, 123.7, 129.7] and [b[1] for b in bands] == [None] * 3, (runs, bands)  # line 843
    assert round(4000 / F_PEAK, 3) == 1.079
    P = Plot(s, (58, 82, 388, 240), (30, 130), (0.85, 1.25))
    age = 30 + np.arange(len(runs[0][0])) / 365
    o = [P.axes([(v, f"{v}") for v in (30, 50, 70, 90, 110, 130)], [(v, f"{v:.1f}") for v in (0.9, 1.0, 1.1, 1.2)],
                "age (years)", "fall safety factor S/F", grid=(0.9, 1.1, 1.2), ytx=13)]
    o.append(H.line(s, P.x0, P.Y(1), P.x1, P.Y(1), I["primary"], "ref", H.DASH_REF))
    o.append(plabel(s, P.X(31), P.Y(1) + 17, "fracture threshold S/F = 1", "label2", I["primary"]))
    o.append(P.curve([30, 130], [bands[0][0][0], bands[0][0][-1]], I["secondary"], multi=True))
    for (ld, lw, col, _), (sf, cr) in zip(cases, runs):
        k = list(range(0, 40, 3)) + list(range(40, len(sf), 365)) + [len(sf) - 1]     # the first days hold the jump
        o.append(P.curve(age[k], sf[k], col, multi=True, nmax=200))
        o.append(P.dot(cr, 1.0, col))
    o.append(plabel(s, P.X(69.7), P.Y(1) - 8, "69.7", "label2", I["primary"], "middle"))
    o.append(plabel(s, P.X(123.7) - 6, P.Y(1) + 17, "123.7", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(129.7) - 4, P.Y(1.04), "129.7", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(129.5), P.Y(bands[0][0][0]) - 7, "band (7.1): 1.08 in all cases", "label2", I["primary"], "end"))
    o.append(plegend(s, 58, 22, [(SER[0], "baseline", None), (SER[1], "+10 % load", None),
                                 (SER[2], "10 % lower setpoint", None)], gap=12))
    o.append(plegend(s, 58, 42, [(I["secondary"], "lazy-zone band (7.1)", None)]))
    o.append(plabel(s, 236, 42, "coloured: one setpoint", "label2", I["secondary"]))
    aria = ("Problem K2 plot: fall safety factor, hip strength over the fall force, against age from 30 to 130 with thresholds "
            "drifting up 0.2 percent a year. With the band collapsed to one setpoint the baseline (red) falls from 1.08 and "
            "crosses the dashed line at 1 at age 69.7; plus 10 percent habitual load (blue) first rises to about 1.19 and crosses "
            "at 123.7; a 10 percent lower setpoint (orange) rises to about 1.20 and crosses at 129.7. With the lazy-zone band of "
            "(7.1) (grey) the bone never leaves the band and the safety factor stays at 1.08 for all three cases.")
    yrs = list(range(0, 36500, 365))
    hv = hov(P, age[yrs], [bands[0][0][yrs]] + [r[0][yrs] for r in runs],
             lambda i: f"age {age[yrs][i]:.0f}: band {bands[0][0][yrs][i]:.3f}; one setpoint {runs[0][0][yrs][i]:.3f}, "
                       f"+10 % {runs[1][0][yrs][i]:.3f}, lower {runs[2][0][yrs][i]:.3f}")
    return psvg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #36: K3, minimum-mass tube
def k3():
    """K3's sweep, verbatim (wall at t_min, reject Z < Z_req)."""
    tmin, zreq = 0.003, 2.02e-6
    R = np.linspace(0.0085, 0.025, 4000)
    r = R - tmin
    Z = (np.pi / 4) * (R ** 4 - r ** 4) / R
    area = np.where(Z >= zreq, np.pi * (R ** 2 - r ** 2), np.inf)
    i = int(np.argmin(area))
    base = np.pi * (0.014 ** 2 - 0.007 ** 2)
    return R[i], area[i], base


def fig36():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    Ropt, aopt, base = k3()
    assert (round(Ropt * 1e3, 1), round(aopt * 1e6, 1), round(100 * (1 - aopt / base), 1)) == (16.8, 287.9, 37.7)  # line 862
    tmin, zreq = 3.0, 2.02e-6 * 1e9                          # mm, mm^3
    rsol = (4 * zreq / math.pi) ** (1 / 3)                   # solid rod meeting Z_req
    # left of the optimum the wall must be thicker than t_min to reach Z_req: r^4 = R^4 - 4 Z_req R / pi
    RL = np.linspace(rsol, Ropt * 1e3, 60)
    aL = math.pi * (RL ** 2 - np.clip(RL ** 4 - 4 * zreq * RL / math.pi, 0, None) ** 0.5)
    RR = np.linspace(Ropt * 1e3, 25, 60)
    aR = math.pi * (RR ** 2 - (RR - tmin) ** 2)
    P = Plot(s, (62, 70, 388, 236), (13, 25), (150, 650))
    o = [P.axes([(v, f"{v}") for v in (13, 16, 19, 22, 25)], [(v, f"{v}") for v in (200, 300, 400, 500, 600)],
                "outer radius R (mm)", "area for Z = Z₀ (mm²)", grid=(300, 400, 500, 600), ytx=13)]
    o.append(P.curve(RL, aL, SER[0]))
    o.append(P.curve(RR, aR, SER[0]))
    o.append(P.dot(Ropt * 1e3, aopt * 1e6, O["flag"]))
    o.append(P.dot(14, base * 1e6, SER[1]))
    o.append(plabel(s, P.X(14) + 8, P.Y(base * 1e6) - 6, f"femur: {base * 1e6:.0f} mm², wall 7 mm", "label2", I["primary"]))
    o.append(plabel(s, P.X(15.0), P.Y(aopt * 1e6) + 20, f"optimum R = {Ropt * 1e3:.1f} mm, wall 3 mm:", "label2", I["primary"]))
    o.append(plabel(s, P.X(15.0), P.Y(aopt * 1e6) + 36, f"{aopt * 1e6:.0f} mm², {100 * (1 - aopt / base):.0f} % less bone",
                    "label2", I["primary"]))
    o.append(plabel(s, P.X(14.2), P.Y(600), "wall > 3 mm, Z = Z₀ exactly", "label2", I["secondary"]))
    o.append(plabel(s, P.X(24.8), P.Y(330), "wall at 3 mm floor", "label2", I["secondary"], "end"))
    o.append(plabel(s, P.X(24.8), P.Y(330) + 15, "Z > Z₀", "label2", I["secondary"], "end"))
    # the two sections to scale (1 mm = 1.2 units)
    bone, line = T["bone"]
    for cxx, Rm, rm, cap in ((200, 14.0, 7.0, "femur"), (300, Ropt * 1e3, Ropt * 1e3 - 3, "optimum")):
        Ro, ri, cyy = 1.2 * Rm, 1.2 * rm, 30
        o.append(f'<path d="M{cxx - Ro:.2f},{cyy} a{Ro:.2f},{Ro:.2f} 0 1 0 {2 * Ro:.2f},0 a{Ro:.2f},{Ro:.2f} 0 1 0 {-2 * Ro:.2f},0 Z '
                 f'M{cxx - ri:.2f},{cyy} a{ri:.2f},{ri:.2f} 0 1 1 {2 * ri:.2f},0 a{ri:.2f},{ri:.2f} 0 1 1 {-2 * ri:.2f},0 Z" '
                 f'fill="{bone}" fill-rule="evenodd" stroke="{line}" stroke-width="{s(1.2):.2f}"/>')
        o.append(plabel(s, cxx + Ro + 5, cyy + 4.5, cap, "label2", I["primary"]))
    o.append(plabel(s, 62, 34, "same Z₀, to scale:", "label2", I["secondary"]))
    aria = ("Problem K3 plot: the least cross-sectional area that meets the femur's section modulus Z0 with a wall of at least "
            "3 millimetres, against outer radius from 13 to 25 millimetres (red). Left of 16.8 mm the wall must be thicker than 3 mm "
            f"and the area falls as the radius grows, from the {rsol:.1f} mm solid rod; right of it the wall sits at the 3 mm floor "
            f"and the area rises again. The minimum (orange dot) is R = 16.8 mm, {aopt * 1e6:.0f} square millimetres, 38 percent "
            f"less than the femur's {base * 1e6:.0f} at R = 14 mm with a 7 mm wall (blue dot). Two cross-sections are drawn to scale.")
    Rh = np.concatenate([RL, RR[1:]])
    ah = np.concatenate([aL, aR[1:]])
    hv = hov(P, Rh, [ah], lambda i: f"R = {Rh[i]:.1f} mm: area {ah[i]:.0f} mm²")
    return psvg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #38: K4, critical ramp rate
def fig38():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    crit = {tr: k4_critical(tr) for tr in (14.0, 7.0)}
    rates = {tr: 60 / c * 7 for tr, c in crit.items()}
    assert round(crit[14.0], 1) == 58.7 and (round(rates[14.0], 1), round(rates[7.0], 1)) == (7.2, 6.1), rates  # line 868
    assert round(k4_max(0), 2) == 1.12 and max(k4_max(rd, 30.0) for rd in (0, 30, 60, 120)) < 1
    P = Plot(s, (58, 82, 388, 240), (0, 26), (0.6, 1.6))
    rr = np.linspace(2.6, 26, 40)
    Ts = 60 * 7 / rr
    cs = [(14.0, SER[0], "repair τᵣ = 14 d"), (7.0, SER[1], "τᵣ = 7 d"), (30.0, SER[2], "τᵣ = 30 d")]
    ys = {tr: np.array([k4_max(round(float(t), 3), tr) for t in Ts]) for tr, _, _ in cs}
    o = [P.axes([(v, f"{v}") for v in (0, 5, 10, 15, 20, 25)], [(v, f"{v:.1f}") for v in (0.6, 0.8, 1.0, 1.2, 1.4, 1.6)],
                "load-ramp rate (% per week)", "peak damage D", grid=(0.8, 1.2, 1.4), ytx=13)]
    o.append(H.line(s, P.x0, P.Y(1), P.x1, P.Y(1), I["primary"], "ref", H.DASH_REF))
    o.append(plabel(s, P.X(13.5), P.Y(1) + 17, "failure, D = 1", "label2", I["primary"]))
    for tr, col, _ in cs:
        o.append(P.curve(rr, ys[tr], col, multi=True))
    for tr in (14.0, 7.0):
        o.append(P.dot(rates[tr], 1.0, SER[0] if tr == 14 else SER[1]))
    o.append(plabel(s, P.X(rates[14.0]) + 8, P.Y(1) + 17, f"{rates[14.0]:.1f} %/wk", "label2", I["primary"]))
    o.append(plabel(s, P.X(rates[7.0]) - 6, P.Y(1) - 8, f"{rates[7.0]:.1f} %/wk", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(25.6), P.Y(ys[30.0][-1]) + 17, "30 d: never reaches 1", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(25.6), P.Y(ys[14.0][-1]) - 8, "14 d", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(25.6), P.Y(ys[7.0][-1]) - 8, "7 d", "label2", I["primary"], "end"))
    o.append(plegend(s, 58, 22, [(c, t, None) for _, c, t in cs], gap=12))
    o.append(plabel(s, 58, 42, f"+60 % load ramped over T days (rate = 420/T % per week);", "label2", I["secondary"]))
    o.append(plabel(s, 58, 58, f"a step gives {k4_max(0):.2f} (14 d), {k4_max(0, 7.0):.2f} (7 d), {k4_max(0, 30.0):.2f} (30 d)",
                    "label2", I["secondary"]))
    aria = ("Problem K4 plot: peak fatigue damage against the load-ramp rate in percent per week, for a 60 percent load rise and "
            f"three repair times. With 14-day repair (red) the peak reaches the dashed failure line D = 1 at {rates[14.0]:.1f} percent "
            f"per week, a {crit[14.0]:.1f}-day ramp, and a step gives {k4_max(0):.2f}; with 7-day repair (blue) the boundary is "
            f"{rates[7.0]:.1f} percent per week; with 30-day repair (orange) the peak stays near 0.8 to 0.86 and never reaches 1.")
    hv = hov(P, rr, [ys[14.0], ys[7.0], ys[30.0]],
             lambda i: f"{rr[i]:.1f} %/wk (T = {Ts[i]:.0f} d): D = {ys[14.0][i]:.2f}, {ys[7.0][i]:.2f}, {ys[30.0][i]:.2f}")
    return psvg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #40: K5, yield locus vs component-wise box
def fig40():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    Y = 130.0
    sb = np.linspace(0, Y, 1301)
    ty = np.sqrt((Y - sb / 2) ** 2 - (sb / 2) ** 2)
    t80 = float(np.interp(80, sb, ty))
    t_eq = Y / (0.5 + math.sqrt(1.25))
    assert (round(t80, 1), round(t_eq, 1), round(0.5 + math.sqrt(1.25), 3)) == (80.6, 80.3, 1.618)   # line 934
    # ratio comp/true > 1.5 exactly where 0.8333 < sigma_b / tau < 1/0.8660 (homogeneous in the load level)
    lo, hi = math.atan(math.sqrt(0.75)), math.atan(1 / (5 / 6))                     # tau/sigma_b = tan(angle)
    P = Plot(s, (62, 62, 388, 240), (0, 140), (0, 140))
    o = [P.axes([(v, f"{v}") for v in (0, 35, 70, 105, 140)], [(v, f"{v}") for v in (0, 35, 70, 105, 140)],
                "bending stress σ" + sub("b", s, "label") + " (MPa)", "torsional shear τ (MPa)", ytx=13)]
    ang = np.linspace(lo, hi, 30)
    rad = [Y / (0.5 * math.cos(a) + math.sqrt(0.25 * math.cos(a) ** 2 + math.sin(a) ** 2)) for a in ang]
    wedge = " ".join(f"{P.X(r * math.cos(a)):.1f},{P.Y(r * math.sin(a)):.1f}" for r, a in zip(rad, ang))
    o.append(f'<polygon points="{P.X(0):.1f},{P.Y(0):.1f} {wedge}" fill="{O["flag"]}" fill-opacity="0.22"/>')
    o.append(P.curve([0, Y, Y], [Y, Y, 0], SER[1], multi=True, dash=DASH))
    o.append(P.curve(sb, ty, SER[0]))
    o.append(P.dot(t_eq, t_eq, O["flag"]))
    o.append(plabel(s, P.X(t_eq) + 8, P.Y(t_eq) - 8, f"σ{sub('b', s)} = τ = {t_eq:.1f}", "label2", I["primary"]))
    o.append(plabel(s, P.X(4), P.Y(42) + 45, f"σ{sub('b', s)} = 80 alone yields once τ = {t80:.1f} is added", "label2",
                    I["secondary"]))
    o.append(plabel(s, P.X(4), P.Y(42), "shaded: the box overstates the", "label2", I["secondary"]))
    o.append(plabel(s, P.X(4), P.Y(42) + 15, "safety factor by more than 1.5;", "label2", I["secondary"]))
    o.append(plabel(s, P.X(4), P.Y(42) + 30, "along σ" + sub("b", s) + " = τ by 1.618;", "label2", I["secondary"]))
    o.append(plegend(s, 62, 22, [(SER[0], "yield locus σ₁ = 130 MPa", None), (SER[1], "component-wise box", DASH)], gap=12))
    o.append(plabel(s, 62, 42, "σ₁ = σ" + sub("b", s) + "/2 + √((σ" + sub("b", s) + "/2)² + τ²)", "label2", I["secondary"]))
    aria = ("Problem K5 plot in the plane of bending stress and torsional shear, both 0 to 140 megapascals. The red yield locus "
            "sigma-1 = 130 MPa runs from tau = 130 on the shear axis to sigma = 130 on the bending axis, well inside the dashed "
            f"blue square a component-wise check allows. Bending at 80 MPa yields once tau = {t80:.1f} is added (red dot); along "
            f"sigma = tau the bone yields at {t_eq:.1f} MPa (orange dot), where the component-wise rule overstates the safety "
            "factor by the golden ratio 1.618. A shaded orange wedge marks where the overstatement exceeds 1.5.")
    idx = list(range(0, 1301, 11))
    hv = hov(P, sb[idx], [ty[idx]], lambda i: f"σb = {sb[idx][i]:.0f}: yields at τ = {ty[idx][i]:.1f} MPa")
    return psvg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #42: K6, allometric regimes
def fig42():
    VB = (0, 0, W, 320)
    s = H.Scale(W, VB[3], display_w=400)
    sref, mref, sstr = 50.0, 70.0, 130.0
    regimes = [("geometric", 1 / 3, SER[0]), ("elastic", 1 / 8, SER[1]), ("stress similarity", 0.0, SER[2])]
    sig = lambda mb, p: sref * (mb / mref) ** p              # noqa: E731
    cross = [mref * (sstr / sref) ** (1 / p) if p else math.inf for _, p, _ in regimes]
    assert (round(cross[0], -1), round(sig(5000, 1 / 3), 1), round(sig(5000, 1 / 8), 1), round(sig(0.02, 1 / 8), 1)) == \
        (1230, 207.5, 85.3, 18.0), cross                                                  # line 949-951
    lx = lambda m: math.log10(m)                             # noqa: E731
    P = Plot(s, (62, 102, 380, 260), (lx(0.02), lx(5000)), (0, 220))
    ms = np.logspace(lx(0.02), lx(5000), 120)
    o = [P.axes([(lx(v), t) for v, t in ((0.02, "0.02"), (0.2, "0.2"), (2, "2"), (20, "20"), (200, "200"), (5000, "5000"))],
                [(v, f"{v}") for v in (0, 50, 100, 150, 200)], "body mass (kg, log scale)", "peak bending stress (MPa)",
                grid=(50, 100, 150, 200), ytx=13)]
    o.append(H.line(s, P.x0, P.Y(sstr), P.x1, P.Y(sstr), I["primary"], "ref", H.DASH_REF))
    o.append(plabel(s, P.X(lx(0.025)), P.Y(sstr) - 7, "tensile strength 130 MPa", "label2", I["primary"]))
    for name, p, col in regimes[::-1]:
        o.append(P.curve(np.log10(ms), sig(ms, p), col, multi=True))
    o.append(P.dot(lx(cross[0]), sstr, SER[0]))
    o.append(P.dot(lx(70), 50, I["primary"]))
    o.append(H.line(s, P.X(lx(70)), P.y0, P.X(lx(70)), P.Y(50) + 5, I["rule"], "leader", (3, 3)))
    o.append(plabel(s, P.X(lx(cross[0])) - 8, P.Y(sstr) - 7, f"{cross[0]:.0f} kg", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(lx(70)) + 8, P.Y(50) + 18, "70 kg, 50 MPa", "label2", I["primary"]))
    o.append(plabel(s, P.x1 - 10, P.Y(sig(5000, 1 / 3)) + 2, f"{sig(5000, 1 / 3):.0f}", "label2", I["primary"], "end"))
    o.append(plabel(s, P.x1 - 4, P.Y(sig(5000, 1 / 8)) - 8, f"{sig(5000, 1 / 8):.0f}", "label2", I["primary"], "end"))
    o.append(plegend(s, 62, 22, [(SER[0], "geometric similarity, exponent 1/3", None)]))
    o.append(plegend(s, 62, 42, [(SER[1], "elastic similarity, exponent 1/8", None)]))
    o.append(plegend(s, 62, 62, [(SER[2], "stress similarity, exponent 0 (never crosses)", None)]))
    o.append(plabel(s, 62, 82, f"elastic would cross only at {cross[1]:.2g} kg".replace("e+05", "×10⁵"), "label2", I["secondary"]))
    aria = ("Problem K6 plot: peak bending stress against body mass on a log axis from a 0.02 kilogram shrew to a 5000 kilogram "
            "elephant, anchored at 50 megapascals for 70 kilograms. Geometric similarity (red, exponent one third) crosses the dashed "
            f"130 MPa strength at {cross[0]:.0f} kg and reaches {sig(5000, 1 / 3):.0f} MPa at 5000 kg; elastic similarity (blue, "
            f"exponent one eighth) reaches {sig(5000, 1 / 8):.0f} MPa and would cross only at 1.5 times 10 to the 5 kg; stress "
            "similarity (orange) stays at 50 and never crosses.")
    hv = hov(P, np.log10(ms), [sig(ms, p) for _, p, _ in regimes],
             lambda i: f"{ms[i]:.3g} kg: {sig(ms[i], 1 / 3):.0f}, {sig(ms[i], 1 / 8):.0f}, 50 MPa")
    return psvg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #44: K7, pad thickness and the energy identity
def fig44():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    target = 2000.0
    ks_need = target ** 2 / (2 * U_FALL)
    x_need = math.sqrt(2 * U_FALL / ks_need)
    lin = lambda tp: math.sqrt(2 * (2 * U_FALL / tp ** 2) * U_FALL)   # noqa: E731  K7's expression (= 2U/tp)
    crush = lambda tp: U_FALL / tp                                     # noqa: E731
    assert (round(ks_need), round(x_need, 3), round(lin(0.03)), round(crush(0.03))) == (14562, 0.137, 9156, 4578)   # line 966
    tc = U_FALL / target
    P = Plot(s, (58, 82, 388, 240), (2, 16), (0, 10))
    tp = np.linspace(0.03, 0.16, 131)
    o = [P.axes([(v, f"{v}") for v in (2, 4, 6, 8, 10, 12, 14, 16)], [(v, f"{v}") for v in (0, 2, 4, 6, 8, 10)],
                "pad thickness tₚ (cm)", "transmitted force (kN)", grid=(4, 6, 8, 10), ytx=13)]
    o.append(H.line(s, P.x0, P.Y(2), P.x1, P.Y(2), I["primary"], "ref", H.DASH_REF))
    o.append(plabel(s, P.X(2.15), P.Y(2) + 17, "osteoporotic 2 kN", "label2", I["primary"]))
    o.append(P.curve(tp * 100, [lin(t) / 1e3 for t in tp], SER[0]))
    o.append(P.curve(tp * 100, [crush(t) / 1e3 for t in tp], SER[1]))
    for t in (0.03, 0.05, 0.10):
        o.append(P.dot(t * 100, lin(t) / 1e3, SER[0]))
        o.append(P.dot(t * 100, crush(t) / 1e3, SER[1]))
    for t, dx, dy in ((0.03, 8, 4), (0.05, 8, -4), (0.10, 6, -8)):
        o.append(plabel(s, P.X(t * 100) + dx, P.Y(lin(t) / 1e3) + dy, f"{lin(t) / 1e3:.1f}", "label2", I["primary"]))
    for t, dx, dy, anc in ((0.03, 7, 2, "start"), (0.05, 7, -7, "start"), (0.10, 0, 19, "middle")):
        o.append(plabel(s, P.X(t * 100) + dx, P.Y(crush(t) / 1e3) + dy, f"{crush(t) / 1e3:.1f}", "label2", I["primary"], anc))
    o.append(P.dot(x_need * 100, 2, O["flag"]))
    o.append(P.dot(tc * 100, 2, O["flag"]))
    o.append(plabel(s, P.X(x_need * 100), P.Y(2) - 9, f"{x_need * 100:.1f} cm", "label2", I["primary"], "middle"))
    o.append(H.line(s, P.X(tc * 100), P.Y(2) + 4, P.X(tc * 100), P.y0, I["rule"], "leader"))
    o.append(plabel(s, P.X(tc * 100) + 4, P.Y(0.3), f"{tc * 100:.1f} cm", "label2", I["primary"]))
    o.append(plegend(s, 58, 22, [(SER[0], "linear pad, F = 2U/tₚ", None), (SER[1], "crushable pad, F = U/tₚ", None)], gap=12))
    o.append(plabel(s, 58, 42, f"U = m{sub('eff', s)}gh = {U_FALL:.0f} J; dots at tₚ = 3, 5, 10 cm", "label2", I["secondary"]))
    aria = ("Problem K7 plot: the force a hip pad transmits against its thickness from 3 to 16 centimetres, for the 137 joule fall. "
            f"The softest linear pad that does not bottom out (red) transmits 2U over tp: {lin(0.03) / 1e3:.1f}, {lin(0.05) / 1e3:.1f} "
            f"and {lin(0.10) / 1e3:.1f} kilonewtons at 3, 5 and 10 cm, and reaches the dashed 2 kN osteoporotic strength only at "
            f"{x_need * 100:.1f} cm. An ideal crushable pad (blue) transmits U over tp, half as much ({crush(0.03) / 1e3:.1f}, "
            f"{crush(0.05) / 1e3:.1f}, {crush(0.10) / 1e3:.1f} kN), and reaches 2 kN at {tc * 100:.1f} cm.")
    hv = hov(P, tp * 100, [[lin(t) / 1e3 for t in tp], [crush(t) / 1e3 for t in tp]],
             lambda i: f"tₚ = {tp[i] * 100:.1f} cm: linear {lin(tp[i]) / 1e3:.2f} kN, crushable {crush(tp[i]) / 1e3:.2f} kN")
    return psvg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #46: K8, one measurement fixes only a curve
def fig46():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    Em, Ec, Eb = 100.0, 1.0, 17.0
    v_voigt = (Eb - Ec) / (Em - Ec)
    v_reuss = (1 - Ec / Eb) / (1 - Ec / Em)
    eta = lambda v, em=Em, ec=Ec: (Eb - (1 - v) * ec) / (v * em)                     # noqa: E731
    assert (round(v_voigt, 2), round(v_reuss, 2), round(eta(0.5), 2)) == (0.16, 0.95, 0.33)       # line 977-982
    assert [round(eta(v), 2) for v in (0.3, 0.5, 0.7)] == [0.54, 0.33, 0.24] and round(eta(0.5, 143, 1.07), 2) == 0.23
    P = Plot(s, (62, 82, 388, 240), (0.1, 1.0), (0, 1.1))
    v = np.linspace(v_voigt, 1.0, 120)
    v2 = np.linspace((Eb - 1.07) / (143 - 1.07), 1.0, 120)
    o = [P.axes([(x, f"{x:g}") for x in (0.2, 0.4, 0.6, 0.8, 1.0)], [(x, f"{x:g}") for x in (0, 0.25, 0.5, 0.75, 1)],
                "mineral volume fraction vₘ", "recruited fraction η", grid=(0.25, 0.5, 0.75, 1.0), ytx=13)]
    o.append(H.line(s, P.X(v_reuss), P.y0, P.X(v_reuss), P.Y(0.62), I["secondary"], "ref", H.DASH_REF))
    o.append(plabel(s, P.X(v_reuss) - 6, P.Y(0.62), "Reuss bound alone", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(v_reuss) - 6, P.Y(0.62) + 15, f"needs vₘ = {v_reuss:.2f}", "label2", I["primary"], "end"))
    o.append(P.curve(v2, eta(v2, 143, 1.07), SER[1], multi=True, dash=DASH))
    o.append(P.curve(v, eta(v), SER[0]))
    o.append(P.dot(v_voigt, 1.0, O["flag"]))
    o.append(plabel(s, P.X(v_voigt) + 8, P.Y(1.0) + 4, f"Voigt bound (η = 1) needs vₘ = {v_voigt:.2f}", "label2", I["primary"]))
    for vv, dx, dy, anc in ((0.3, 8, -6, "start"), (0.5, 8, -8, "start"), (0.7, 6, -8, "start")):
        o.append(P.dot(vv, eta(vv), SER[0]))
        o.append(plabel(s, P.X(vv) + dx, P.Y(eta(vv)) + dy, f"{eta(vv):.2f}", "label2", I["primary"], anc))
    o.append(P.dot(0.5, eta(0.5, 143, 1.07), SER[1]))
    o.append(plabel(s, P.X(0.5) - 6, P.Y(eta(0.5, 143, 1.07)) + 18, f"{eta(0.5, 143, 1.07):.2f}", "label2", I["primary"], "end"))
    o.append(plegend(s, 62, 22, [(SER[0], f"E{sub('m', s)} = 100, E{sub('c', s)} = 1 GPa (K8)", None)]))
    o.append(plegend(s, 62, 42, [(SER[1], "Module 0 apatite 143, collagen 1.07 (§5)", DASH)]))
    o.append(plabel(s, 62, 62, "every point on a curve gives E = 17 GPa", "label2", I["secondary"]))
    aria = ("Problem K8 plot: recruited stiffness fraction eta against mineral volume fraction, along the curve on which the "
            "two-parameter model gives E = 17 gigapascals. With K8's end members 100 and 1 GPa (red) eta is 1 at the Voigt "
            f"fraction {v_voigt:.2f} and falls to 0.54, 0.33 and 0.24 at 0.3, 0.5 and 0.7; a dashed line marks the {v_reuss:.2f} "
            "the Reuss bound alone would need. With section 5's derived apatite 143 and collagen 1.07 GPa (blue dashed) eta at 0.5 "
            "is 0.23.")
    hv = hov(P, v, [eta(v)], lambda i: f"vₘ = {v[i]:.2f}: η = {eta(v[i]):.3f} (with 143 GPa: {eta(v[i], 143, 1.07):.3f})")
    return psvg(VB, aria, s, "".join(o), (P.box, hv))


FIGS = {
    3: ('Maximum bending stress versus applied moment for a hollow fe', fig3),
    7: ('Three horizontal brackets on a logarithmic modulus axis from', fig7),
    8: ('Bar chart: fall impact force about 3.7 kilonewtons compared ', fig8),
    9: ('Mechanostat curve: remodeling rate versus strain. Resorption', fig9),
    10: ('Net remodeling rate, normalised to the maximal formation rat', fig10),
    11: ('Section modulus over 400 days for three load levels: increas', fig11),
    17: ('Microdamage accumulates faster than remodeling repair when l', fig17),
    18: ('The mechanostat: net remodeling rate is negative below the l', fig18),
    23: ('A section in bending with tensile stress above and compressi', fig23),
    27: ('A circular shaft cross-section with shear arrows growing lin', fig27),
    29: ('Phase line of the remodeling rate versus section modulus: dZ', fig29),
    34: ('Fall safety factor from age 30 to 130 for three collapsed-se', fig34),
    36: ('Cross-sectional area versus outer radius for a tube meeting ', fig36),
    38: ('Peak fatigue damage against load-ramp rate for three repair ', fig38),
    40: ('Yield locus of the largest principal stress in the bending-s', fig40),
    42: ('Peak bending stress against body mass on a log scale for thr', fig42),
    44: ('Transmitted fall force against hip-pad thickness for a linea', fig44),
    46: ('The curve of recruited stiffness fraction against mineral vo', fig46),
}
