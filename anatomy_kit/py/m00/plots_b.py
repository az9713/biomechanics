"""Module 0 plots, group `plots_b`: svg 18-22, 24, 27, 29 (main text, 760 px) and 30-33 (K2, K4, K5, K7, 400 px).

Every plotted number is computed here from the formula, constant or script the Module 0 text states:
  Lemma 5.1 buffer capacity (sec. 5), the OSF persistence length with Proposition 5.1's Debye length,
  the Hill equation (Def. 6.2) and Prop. 6.2, Arrhenius (Prop. 6.3), Michaelis-Menten (Prop. 6.4),
  c_F = 2m/458 (sec. 7), Lab 8A and Lab 8B (their code, ported unchanged), and the K2/K4/K5/K7 set-ups.
The numbers the page prints are asserted at import, so drift fails loudly.
"""
import math

import numpy as np

import house as H
from m05.plots_main import Ax, axes, curve, poly, dot, legend, tw, hover, svg, mn, lead, DASH_SER

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
BAND = I["muted"]                       # neutral shaded range (labelled directly)
SUPT = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")

# ---------------------------------------------------------------- constants the text states
R_G, T_BODY, N_A = 8.314462618, 310.15, 6.02214076e23
E_CH, EPS0, K_B = 1.602176634e-19, 8.8541878128e-12, 1.380649e-23
LN10 = math.log(10)


def p10(k):
    """10 to an integer power as tick text (Unicode superscript, Unicode minus)."""
    return "1" if k == 0 else "10" + str(k).translate(SUPT)


def sub(t, s, size="label2"):
    return H.sub(t, s, size)


def band(ax, xa, xb, col=BAND, op=0.12):
    xl, xr = sorted((ax.X(xa), ax.X(xb)))
    return f'<rect x="{xl:.2f}" y="{ax.top:.2f}" width="{xr - xl:.2f}" height="{ax.y0 - ax.top:.2f}" fill="{col}" opacity="{op}"/>'


def lab(s, x, y, t, size="label2", fill=I["primary"], anchor="start", extra=""):
    return H.label(s, x, y, t, size, fill, anchor, extra)


def defs(p, s):
    return f"<defs>{H.markers(p, s)}</defs>"


# ================================================================ svg #18: buffer capacity (Lemma 5.1)
BUFFERS = [("bicarbonate", 24.0, 6.10, SER[0]), ("protein histidine", 8.0, 7.30, SER[1]), ("phosphate", 1.0, 6.80, SER[2])]


def beta(ph, c_tot, pka):
    """Lemma 5.1, mM per pH unit."""
    h, k = 10 ** -ph, 10 ** -pka
    return LN10 * c_tot * k * h / (k + h) ** 2


BETA_OPEN = LN10 * 24.0                                       # lungs hold CO2 fixed: ln10 [HCO3-]
assert round(beta(7.4, 24, 6.10), 2) == 2.51 and round(BETA_OPEN, 1) == 55.3 and round(BETA_OPEN / beta(7.4, 24, 6.1)) == 22


def fig18():
    VB = (0, 0, 760, 392)
    s = H.Scale(VB[2], VB[3])
    p = "m0f18_"
    ax = Ax((80, 72, 740, 322), (4, 10), (0, 16))
    phs = np.linspace(4, 10, 109)
    o = [defs(p, s), band(ax, 7.35, 7.45)]
    o += axes(s, ax, [(v, f"{v}") for v in range(4, 11)], [(v, f"{v}") for v in (0, 4, 8, 12, 16)],
              "pH", "buffer capacity β (mM per pH unit)", ylab_x=28)
    for name, c, pk, col in BUFFERS:
        o.append(curve(s, ax, phs, [beta(x, c, pk) for x in phs], col, "curve_multi"))
    # lungs open: bicarbonate's real capacity, off the top of the axis
    b74 = beta(7.4, 24, 6.10)
    o.append(H.line(s, ax.X(7.4), ax.Y(b74) - 6, ax.X(7.4), ax.top + 2, SER[0], "curve_multi", DASH_SER,
                    extra=f'marker-end="url(#{p}a_force)"'))
    for name, c, pk, col in BUFFERS:
        o.append(dot(s, ax.X(7.4), ax.Y(beta(7.4, c, pk)), col))
    o.append(lab(s, ax.X(7.35) - 8, ax.top - 8, "blood, pH 7.35–7.45", "label2", I["secondary"], "end"))
    o.append(lab(s, ax.X(7.4) + 12, ax.Y(15.0), f"lungs open: {BETA_OPEN:.1f} mM per pH at 7.40,"))
    o.append(lab(s, ax.X(7.4) + 12, ax.Y(15.0) + 17, f"{BETA_OPEN / b74:.0f}× the closed value, off this axis", "label2", I["secondary"]))
    vals = {n: beta(7.4, c, pk) for n, c, pk, _ in BUFFERS}
    o.append(lab(s, ax.X(7.6), ax.Y(11.0), "closed system at pH 7.40 (dots):"))
    o.append(lab(s, ax.X(7.6), ax.Y(11.0) + 17, f"histidine {vals['protein histidine']:.2f}, bicarbonate "
                 f"{vals['bicarbonate']:.2f},", "label2", I["secondary"]))
    o.append(lab(s, ax.X(7.6), ax.Y(11.0) + 34, f"phosphate {vals['phosphate']:.2f} mM per pH", "label2", I["secondary"]))
    # direct labels
    o.append(lab(s, ax.X(5.93), ax.Y(14.4), f"bicarbonate, pK{sub('a', s)} 6.10, 24 mM", anchor="end"))
    o.append(lab(s, ax.X(7.72), ax.Y(5.0), f"protein histidine, pK{sub('a', s)} 7.3, 8 mM"))
    o.append(lab(s, ax.X(8.45), ax.Y(1.9), f"phosphate, pK{sub('a', s)} 6.8, 1 mM"))
    o.append(lead(s, ax.X(8.42), ax.Y(1.75), ax.X(7.75), ax.Y(beta(7.75, 1, 6.8)) - 3, SER[2]))
    o += legend(s, ax.x0, 26, [(SER[0], None, "bicarbonate"), (SER[1], None, "protein histidine"),
                               (SER[2], None, "phosphate"), (SER[0], DASH_SER, "bicarbonate, lungs open")], gap=22)
    o += legend(s, ax.x0, 46, [(BAND, None, "blood pH range", "band")])
    aria = ("Buffer capacity in millimolar per pH unit against pH from 4 to 10 for the body's three buffers, each a bell "
            "curve peaking at its own pKa by Lemma 5.1: bicarbonate, 24 millimolar, peaks at pH 6.10 with 13.8; protein "
            "histidine, 8 millimolar, peaks at 7.3 with 4.6; phosphate, 1 millimolar, peaks at 6.8 with 0.58. A shaded "
            f"band marks the blood range 7.35 to 7.45. At pH 7.40 the closed-system capacities are {vals['protein histidine']:.2f} "
            f"for histidine, {vals['bicarbonate']:.2f} for bicarbonate and {vals['phosphate']:.2f} for phosphate. A dashed red "
            f"arrow at pH 7.40 points off the top of the axis to bicarbonate's open-system capacity, {BETA_OPEN:.1f} "
            "millimolar per pH unit when the lungs hold carbon dioxide fixed, 22 times the closed value.")
    hp = np.linspace(4, 10, 241)
    hv = hover(ax, [ax.X(x) for x in hp], [[ax.Y(beta(x, c, pk)) for _, c, pk, _ in BUFFERS] for x in hp],
               [f"pH {x:.2f}: bicarbonate {beta(x, 24, 6.1):.2f}, histidine {beta(x, 8, 7.3):.2f}, "
                f"phosphate {beta(x, 1, 6.8):.2f} mM per pH" for x in hp])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #19: OSF persistence length
EPS_R, A_CH, LP0, I_PLASMA = 73.2, 1e-9, 14.5, 0.1425      # -, m (one charge per nm), nm, M


def lam_d(i_molar):
    """Proposition 5.1, I converted to mol per m3; returns m."""
    return math.sqrt(EPS0 * EPS_R * K_B * T_BODY / (2 * E_CH ** 2 * N_A * i_molar * 1e3))


L_B = E_CH ** 2 / (4 * math.pi * EPS0 * EPS_R * K_B * T_BODY)


def l_osf(i_molar):
    """OSF electrostatic persistence length, nm."""
    return L_B * lam_d(i_molar) ** 2 / (4 * A_CH ** 2) * 1e9


def _bisect_log(f, lo, hi):
    for _ in range(200):
        m = math.sqrt(lo * hi)
        lo, hi = (m, hi) if f(m) > 0 else (lo, m)
    return math.sqrt(lo * hi)


I_CROSS = _bisect_log(lambda i: l_osf(i) - LP0, 1e-5, 1.0)
assert round(L_B * 1e9, 3) == 0.736 and round(lam_d(I_PLASMA) * 1e9, 3) == 0.794 and round(lam_d(1e-3) * 1e9, 2) == 9.47
assert round(l_osf(I_PLASMA), 3) == 0.116 and round(l_osf(1e-3), 1) == 16.5 and round(I_CROSS * 1e3, 2) == 1.14


def fig19():
    VB = (0, 0, 760, 392)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((92, 40, 740, 316), (1e-4, 1.0), (0.01, 1000), xlog=True, ylog=True)
    o = [band(ax, 1e-3, 1e-2)]
    o += axes(s, ax, [(10.0 ** k, p10(k)) for k in range(-4, 1)], [(10.0 ** k, f"{10.0 ** k:g}") for k in range(-2, 4)],
              "ionic strength I (M, log scale)", f"ℓ{sub('OSF', s, 'label')} (nm, log scale)", ylab_x=30)
    ii = [10 ** (-4 + 4 * k / 100) for k in range(101)]
    o.append(H.line(s, ax.x0, ax.Y(LP0), ax.x1, ax.Y(LP0), I["secondary"], "ref", H.DASH_REF))
    o.append(curve(s, ax, ii, [l_osf(i) for i in ii], SER[0]))
    o.append(lab(s, ax.x1 - 4, ax.Y(LP0) - 9, f"intrinsic ℓ{sub('p', s)}⁰ = {LP0} nm", "label2", I["secondary"], "end"))
    o.append(dot(s, ax.X(I_CROSS), ax.Y(LP0), O["flag"]))
    o.append(lab(s, ax.X(I_CROSS) + 12, ax.Y(LP0) - 9, f"equal at I ≈ {I_CROSS * 1e3:.1f} mM"))
    o.append(dot(s, ax.X(1e-3), ax.Y(l_osf(1e-3)), SER[0], hollow=True))
    o.append(lab(s, ax.X(1e-3) - 10, ax.Y(l_osf(1e-3)) + 24, f"1 mM buffer: {l_osf(1e-3):.1f} nm", anchor="end"))
    o.append(dot(s, ax.X(I_PLASMA), ax.Y(l_osf(I_PLASMA)), O["flag"]))
    o.append(lab(s, ax.X(I_PLASMA) - 12, ax.Y(l_osf(I_PLASMA)) + 26, f"plasma, I = {I_PLASMA * 1e3:.1f} mM:", anchor="end"))
    o.append(lab(s, ax.X(I_PLASMA) - 12, ax.Y(l_osf(I_PLASMA)) + 43,
                 f"{l_osf(I_PLASMA):.3f} nm, {100 * l_osf(I_PLASMA) / LP0:.1f} % of {LP0}", "label2", I["secondary"], "end"))
    o.append(lab(s, ax.X(1.3e-4), ax.Y(0.05), f"slope −1: ℓ{sub('OSF', s)} = ℓ{sub('B', s)}λ{sub('D', s)}²/4A² ∝ 1/I"))
    o.append(lab(s, ax.X(1.3e-4), ax.Y(0.05) + 17, "one net charge per nm (A = 1 nm)", "label2", I["secondary"]))
    o.append(lab(s, ax.X(math.sqrt(1e-5)), ax.top + 18, "single-molecule buffers,", "label2", I["secondary"], "middle"))
    o.append(lab(s, ax.X(math.sqrt(1e-5)), ax.top + 34, "1–10 mM", "label2", I["secondary"], "middle"))
    aria = ("Log-log plot of the electrostatic contribution to a persistence length, from the Odijk-Skolnick-Fixman estimate "
            "with one net charge per nanometre, against ionic strength from 0.1 millimolar to 1 molar: a straight line of "
            "slope minus one, because it goes as the Debye length squared and so as one over ionic strength. A dashed line "
            f"marks tropocollagen's intrinsic 14.5 nanometres; the two are equal at about {I_CROSS * 1e3:.1f} millimolar. "
            f"A dilute 1 millimolar buffer gives {l_osf(1e-3):.1f} nanometres. Plasma, at 142.5 millimolar, gives "
            f"{l_osf(I_PLASMA):.3f} nanometres, 0.8 per cent of the intrinsic value. A shaded band marks the 1 to 10 "
            "millimolar buffers single-molecule experiments are often run in, around the crossing.")
    hv = hover(ax, [ax.X(i) for i in ii], [ax.Y(l_osf(i)) for i in ii],
               [f"I = {i * 1e3:.3g} mM: λD = {lam_d(i) * 1e9:.2f} nm, ℓOSF = {l_osf(i):.3g} nm" for i in ii])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #20: Hill occupancy against pCa
def hill(c, n, k=1.0):
    return c ** n / (k ** n + c ** n)


W10_90 = {n: 2 * math.log10(9) / n for n in (1, 3)}
assert round(hill(0.1, 3) * 100, 2) == 0.10 and round(hill(10, 3) * 100, 1) == 99.9
assert round(hill(0.1, 1) * 100, 1) == 9.1 and round(hill(10, 1) * 100, 1) == 90.9
assert round(W10_90[3], 2) == 0.64 and round(W10_90[1], 2) == 1.91


def fig20():
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 64, 740, 294), (8, 5), (0, 1.0))
    pcas = np.linspace(8, 5, 109)
    o = [band(ax, 7, 5)]
    o += axes(s, ax, [(v, f"{v}") for v in (8, 7, 6, 5)], [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1.0)],
              None, "fraction of sites bound θ", ylab_x=28)
    o.append(lab(s, (ax.x0 + ax.x1) / 2, ax.y0 + 112, "pCa = −log₁₀[Ca²⁺] (calcium rises to the right)", "label", I["primary"], "middle"))
    o.append(H.line(s, ax.X(6), ax.top, ax.X(6), ax.y0, I["rule"], "leader"))
    o.append(curve(s, ax, pcas, [hill(10 ** (6 - x), 1) for x in pcas], SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, ax, pcas, [hill(10 ** (6 - x), 3) for x in pcas], SER[0]))
    # resting and activated points, both curves
    for x in (7, 5):
        for n, col in ((3, SER[0]), (1, SER[1])):
            o.append(dot(s, ax.X(x), ax.Y(hill(10 ** (6 - x), n)), col))
    o.append(lab(s, ax.X(7.95), ax.Y(0.80), "resting, 0.1 µM (pCa 7):"))
    o.append(lab(s, ax.X(7.95), ax.Y(0.80) + 17, f"{100 * hill(0.1, 3):.2f} % bound (n{sub('H', s)} = 3), "
                 f"{100 * hill(0.1, 1):.1f} % (n{sub('H', s)} = 1)", "label2", I["secondary"]))
    o.append(lab(s, ax.X(7.95), ax.Y(0.80) + 40, "activated, 10 µM (pCa 5):"))
    o.append(lab(s, ax.X(7.95), ax.Y(0.80) + 57, f"{100 * hill(10, 3):.1f} % bound (n{sub('H', s)} = 3), "
                 f"{100 * hill(10, 1):.1f} % (n{sub('H', s)} = 1)", "label2", I["secondary"]))
    o.append(lab(s, ax.X(6.38), ax.top + 18, "twitch window, pCa 7 → 5", "label2", I["secondary"], "middle"))
    o.append(lab(s, ax.X(6) + 6, ax.Y(0.5) + 18, "half-bound at pCa 6 (1 µM)", "label2", I["secondary"]))
    # direct labels on the two curves
    o.append(lab(s, ax.X(5.95), ax.Y(0.30), f"n{sub('H', s)} = 3"))
    o.append(lead(s, ax.X(5.95) - 3, ax.Y(0.30) - 4, ax.X(6.08) + 2, ax.Y(hill(10 ** -0.08, 3)), SER[0]))
    o.append(lab(s, ax.X(5.35), ax.Y(0.62), f"n{sub('H', s)} = 1"))
    o.append(lead(s, ax.X(5.24), ax.Y(0.62) + 4 - 22, ax.X(5.24), ax.Y(hill(10 ** 0.76, 1)) + 3, SER[1]))
    # 10-90 % widths: hollow dots on the curves, bars under the axis at the same x
    for k, (n, col) in enumerate(((3, SER[0]), (1, SER[1]))):
        xa, xb = 6 + W10_90[n] / 2, 6 - W10_90[n] / 2
        o.append(dot(s, ax.X(xa), ax.Y(0.1), col, hollow=True))
        o.append(dot(s, ax.X(xb), ax.Y(0.9), col, hollow=True))
        yy = ax.y0 + 42 + 20 * k
        o.append(H.line(s, ax.X(xa), yy, ax.X(xb), yy, col, "curve"))
        for xe in (xa, xb):
            o.append(H.line(s, ax.X(xe), yy - 6, ax.X(xe), yy + 6, col, "ref"))
        o.append(lab(s, ax.X(xa) - 8, yy + 4.5, f"{W10_90[n]:.2f} decades", anchor="end"))
        o.append(lab(s, ax.x0 - 9, yy + 4.5, f"n{sub('H', s)} = {n}", anchor="end"))
    o.append(lab(s, ax.X(4.97), ax.y0 + 86, "10 % to 90 % bound", "label2", I["secondary"], "end"))
    o += legend(s, ax.x0, 24, [(SER[0], None, f"cooperative, n{sub('H', s)} = 3 (Definition 6.2)"),
                               (SER[1], DASH_SER, f"independent sites, n{sub('H', s)} = 1 (Proposition 6.2)")])
    o += legend(s, ax.x0, 44, [(BAND, None, "the window one twitch traverses", "band")])
    aria = ("Fraction of calcium-binding sites occupied against pCa, from pCa 8 on the left to pCa 5 on the right, so "
            "calcium rises to the right; half-occupancy at pCa 6, 1 micromolar, for both curves. A shaded band marks the "
            "window one twitch traverses, pCa 7 to 5. The solid red cooperative curve, Hill coefficient 3, is 0.10 per cent "
            "bound at resting 0.1 micromolar and 99.9 per cent at 10 micromolar. The dashed blue single-site hyperbola runs "
            "only from 9.1 to 90.9 per cent over the same range. Bars under the axis show the 10 to 90 per cent widths: "
            "0.64 decades for the cooperative curve and 1.91 for the independent one.")
    hp = np.linspace(8, 5, 181)
    hv = hover(ax, [ax.X(x) for x in hp], [[ax.Y(hill(10 ** (6 - x), 3)), ax.Y(hill(10 ** (6 - x), 1))] for x in hp],
               [f"pCa {x:.2f} ({10 ** (6 - x):.3g} µM): θ = {hill(10 ** (6 - x), 3):.3f} (nH 3), "
                f"{hill(10 ** (6 - x), 1):.3f} (nH 1)" for x in hp])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #21: Arrhenius cooling factor
EA = R_G * 298.15 * 308.15 / 10 * math.log(2.5)                 # Prop. 6.3 with Q10 = 2.5


def rate_rel(t_c, ea=EA):
    return math.exp(-ea / R_G * (1 / (t_c + 273.15) - 1 / T_BODY))


assert round(EA / 1e3, 1) == 70.0 and round(rate_rel(25), 3) == 0.335 and round(1 / rate_rel(25), 2) == 2.98
assert round(rate_rel(40), 2) == 1.30


def fig21():
    VB = (0, 0, 760, 372)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 30, 740, 300), (10, 40), (0, 1.5))
    ts = np.linspace(10, 40, 101)
    o = axes(s, ax, [(v, f"{v}") for v in range(10, 41, 5)], [(v, f"{v:g}") for v in (0, 0.5, 1.0, 1.5)],
             "temperature (°C)", "rate, relative to 37 °C", ylab_x=28)
    o.append(H.line(s, ax.x0, ax.Y(1.0), ax.x1, ax.Y(1.0), I["secondary"], "ref", H.DASH_REF))
    o.append(curve(s, ax, ts, [rate_rel(t) for t in ts], SER[0]))
    r25, r40 = rate_rel(25), rate_rel(40)
    o.append(dot(s, ax.X(25), ax.Y(r25), O["flag"]))
    o.append(dot(s, ax.X(37), ax.Y(1.0), SER[0]))
    o.append(dot(s, ax.X(40), ax.Y(r40), O["flag"]))
    o.append(lead(s, ax.X(25) - 4, ax.Y(r25) - 4, ax.X(23.4), ax.Y(0.62) + 5, I["rule"]))
    o.append(lab(s, ax.X(23.4), ax.Y(0.62) - 17, "cooled limb, 25 °C:", anchor="end"))
    o.append(lab(s, ax.X(23.4), ax.Y(0.62), f"every rate × {r25:.3f}, a {1 / r25:.2f}× slowdown", "label2", I["secondary"], "end"))
    o.append(lab(s, ax.X(37) - 10, ax.Y(1.0) - 10, "body temperature, 37 °C: 1", anchor="end"))
    o.append(lab(s, ax.X(40) - 10, ax.Y(r40) - 12, f"fever, 40 °C: × {r40:.2f}", anchor="end"))
    o.append(lab(s, ax.X(11), ax.Y(1.38), f"Q{sub('10', s, 'label')} = 2.5, so E{sub('a', s, 'label')} = {EA / 1e3:.1f} kJ mol⁻¹", "label"))
    o.append(lab(s, ax.X(11), ax.Y(1.38) + 18, f"k(T) ∝ exp(−E{sub('a', s)}/R{sub('g', s)}T), Proposition 6.3", "label2", I["secondary"]))
    aria = (f"Rate relative to its value at 37 degrees Celsius against temperature from 10 to 40 degrees, for the activation "
            f"energy of {EA / 1e3:.1f} kilojoules per mole that a Q-ten of 2.5 implies. The Arrhenius curve passes through "
            f"1 at body temperature, marked by a dashed line. At 25 degrees every rate is {r25:.3f} of its warm value, a "
            f"{1 / r25:.2f}-fold slowdown; at a 40 degree fever it is {r40:.2f} times faster.")
    hv = hover(ax, [ax.X(t) for t in ts], [ax.Y(rate_rel(t)) for t in ts],
               [f"{t:.2f} °C: rate × {rate_rel(t):.3f}" for t in ts])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #22: Michaelis-Menten for myosin ATPase
KM = 50e-6                                                     # M


def mm(c):
    return c / (KM + c)


DROP_RATE = (mm(5.5e-3) - mm(5.0e-3)) / mm(5.5e-3) * 100
assert round(mm(5.5e-3), 3) == 0.991 and round(mm(5.0e-3), 3) == 0.990 and round(DROP_RATE, 2) == 0.09


def fig22():
    VB = (0, 0, 760, 372)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 30, 740, 300), (1e-7, 1e-2), (0, 1.0), xlog=True)
    cs = [10 ** (-7 + 5 * k / 100) for k in range(101)]
    o = [f'<rect x="{ax.X(5.0e-3):.2f}" y="{ax.top:.2f}" width="{ax.X(5.5e-3) - ax.X(5.0e-3):.2f}" '
         f'height="{ax.y0 - ax.top:.2f}" fill="{SER[0]}" opacity="0.85"/>']
    tk = [(1e-7, "0.1 µM"), (1e-6, "1 µM"), (1e-5, "10 µM"), (1e-4, "100 µM"), (1e-3, "1 mM"), (1e-2, "10 mM")]
    o += axes(s, ax, tk, [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1.0)], "[ATP] (log scale)",
              f"rate v / v{sub('max', s, 'label')}", ylab_x=28)
    o.append(H.line(s, ax.x0, ax.Y(0.5), ax.X(KM), ax.Y(0.5), I["rule"], "leader", H.DASH_REF))
    o.append(H.line(s, ax.X(KM), ax.Y(0.5), ax.X(KM), ax.y0, I["rule"], "leader", H.DASH_REF))
    o.append(curve(s, ax, cs, [mm(c) for c in cs], SER[1]))
    o.append(dot(s, ax.X(KM), ax.Y(0.5), O["flag"]))
    o.append(lab(s, ax.X(KM) + 12, ax.Y(0.5) + 18, f"K{sub('M', s)} = 50 µM: half-maximal rate"))
    o.append(lab(s, ax.X(1.3e-7), ax.Y(0.92), "a whole fatiguing bout, ATP 5.5 → 5.0 mM (red band):"))
    o.append(lab(s, ax.X(1.3e-7), ax.Y(0.92) + 18, f"rate {mm(5.5e-3):.3f} → {mm(5.0e-3):.3f}, a {DROP_RATE:.2f} % change;",
                 "label2", I["secondary"]))
    o.append(lab(s, ax.X(1.3e-7), ax.Y(0.92) + 35, "free energy (§3) 15.7 %, of which ATP's own fall 0.39 %",
                 "label2", I["secondary"]))
    o.append(lead(s, ax.X(1.3e-7) + tw("a whole fatiguing bout, ATP 5.5 → 5.0 mM (red band):") + 6, ax.Y(0.92) - 4,
                  ax.X(5.0e-3) - 3, ax.Y(0.92) - 4, I["rule"]))
    aria = ("Michaelis-Menten curve of myosin ATPase rate over maximal rate against ATP concentration on a logarithmic axis "
            "from 0.1 micromolar to 10 millimolar. The curve passes half-maximal at the Michaelis constant of 50 micromolar "
            "and is saturated well before 1 millimolar. A narrow red band at 5.0 to 5.5 millimolar marks the whole range a "
            f"muscle traverses through a fatiguing bout, far out on the flat part: the rate goes from {mm(5.5e-3):.3f} to "
            f"{mm(5.0e-3):.3f}, a 0.09 per cent change, while section 3 showed the free energy of the same reaction changes "
            "by 15.7 per cent, only 0.39 per cent of it from ATP's own fall.")
    hv = hover(ax, [ax.X(c) for c in cs], [ax.Y(mm(c)) for c in cs],
               [f"[ATP] = {c * 1e6:.3g} µM: v/vmax = {mm(c):.4f}" for c in cs])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #24: fixed charge from GAG content
M_DIS = 458.0                                                    # g/mol, two charges each


def c_f(m):
    return 2 * m / M_DIS


assert round(c_f(40), 3) == 0.175 and round(c_f(70), 3) == 0.306 and round(0.2 * M_DIS / 2, 1) == 45.8


def fig24():
    VB = (0, 0, 760, 372)
    s = H.Scale(VB[2], VB[3])
    p = "m0f24_"
    ax = Ax((80, 40, 740, 300), (0, 80), (0, 0.4))
    m02 = 0.2 * M_DIS / 2
    o = [defs(p, s), band(ax, 40, 70)]
    o += axes(s, ax, [(v, f"{v}") for v in range(0, 81, 10)], [(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3, 0.4)],
              "glycosaminoglycan content m (mg mL⁻¹)", f"fixed charge c{sub('F', s, 'label')} (M)", ylab_x=28)
    o.append(H.line(s, ax.x0, ax.Y(0.2), ax.X(m02), ax.Y(0.2), I["rule"], "leader", H.DASH_REF))
    o.append(H.line(s, ax.X(m02), ax.Y(0.2), ax.X(m02), ax.y0, I["rule"], "leader", H.DASH_REF))
    o.append(poly(s, [(ax.X(0), ax.Y(0)), (ax.X(80), ax.Y(c_f(80)))], SER[0]))
    o.append(dot(s, ax.X(0), ax.Y(0), SER[0]))
    o.append(dot(s, ax.X(m02), ax.Y(0.2), O["flag"]))
    o.append(lab(s, ax.X(55), ax.top + 20, "healthy cartilage, 40–70 mg mL⁻¹", "label2", I["secondary"], "middle"))
    o.append(lab(s, ax.X(55), ax.top + 37, f"c{sub('F', s)} = {c_f(40):.3f} to {c_f(70):.3f} M", "label2", I["secondary"], "middle"))
    o.append(lab(s, ax.X(m02) + 10, ax.Y(0.2) + 22, f"§5's c{sub('F', s)} = 0.2 M needs {m02:.1f} mg mL⁻¹"))
    o.append(lab(s, ax.X(2), ax.Y(0.37), f"c{sub('F', s)} = 2m / 458: two charges per", "label"))
    o.append(lab(s, ax.X(2), ax.Y(0.37) + 18, "458 g mol⁻¹ disaccharide, through the origin", "label2", I["secondary"]))
    # osteoarthritis: GAG loss slides a tissue down the line
    d = 0.03                                                         # M offset above the line
    o.append(H.arrow(s, p, ax.X(42), ax.Y(c_f(42) + d), ax.X(26), ax.Y(c_f(26) + d), "dim"))
    o.append(lab(s, ax.X(3), ax.Y(0.275), "GAG loss (osteoarthritis):", "label2", I["primary"]))
    o.append(lab(s, ax.X(3), ax.Y(0.275) + 16, "down the line; swelling pressure", "label2", I["secondary"]))
    o.append(lab(s, ax.X(3), ax.Y(0.275) + 32, "falls roughly in proportion", "label2", I["secondary"]))
    aria = ("Fixed charge concentration in molar against glycosaminoglycan content from 0 to 80 milligrams per millilitre: a "
            "straight line through the origin, c F = 2 m over 458, because each 458 gram per mole disaccharide carries two "
            "fixed negative charges. A shaded band marks the 40 to 70 milligrams per millilitre of healthy cartilage, which "
            "gives 0.175 to 0.306 molar. Dashed guides mark section 5's 0.2 molar, which needs 45.8 milligrams per "
            "millilitre, inside the healthy range. An arrow down the line marks glycosaminoglycan loss in osteoarthritis.")
    hm = np.linspace(0, 80, 161)
    hv = hover(ax, [ax.X(m) for m in hm], [ax.Y(c_f(m)) for m in hm],
               [f"m = {m:.1f} mg/mL: cF = {c_f(m):.3f} M" for m in hm])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #27: Lab 8A, binding with depletion (code ported unchanged)
K_HALF = 1.0e-6          # M, half-activation, section 6
N_HILL = 3.0             # Hill coefficient, section 6
S_TOT = 70.0e-6          # M, troponin C regulatory sites in muscle


def theta(c, k_half=K_HALF, n=N_HILL):
    if c <= 0.0:
        return 0.0
    return c ** n / (k_half ** n + c ** n)


def bound(c, s_tot=S_TOT):
    return s_tot * theta(c)


def free_from_total(c_tot, s_tot=S_TOT, tol=1e-18):
    def residual(c):
        return c + bound(c, s_tot) - c_tot

    lo, hi = 0.0, max(c_tot, 1e-12)
    while residual(hi) < 0.0:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if residual(mid) < 0.0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def lab8a_rows(totals):
    return [{"c_tot": ct, "c_free": free_from_total(ct), "theta_true": theta(free_from_total(ct)),
             "theta_naive": theta(ct)} for ct in totals]


LAB8A = lab8a_rows([10 ** (-7.0 + 3.2 * i / 60.0) for i in range(61)])
HALF8A = [r for r in LAB8A if r["theta_true"] >= 0.5][0]
WORST8A = max(LAB8A, key=lambda r: r["theta_naive"] - r["theta_true"])
assert round(HALF8A["c_tot"] * 1e6, 1) == 36.3 and round(WORST8A["c_tot"] * 1e6, 2) == 3.98
assert round(WORST8A["theta_naive"], 3) == 0.984 and round(WORST8A["theta_true"], 3) == 0.051
assert round(WORST8A["theta_naive"] - WORST8A["theta_true"], 2) == 0.93
assert round(free_from_total(0.1e-6) * 1e9, 1) == 72.9


def fig27():
    VB = (0, 0, 760, 372)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 54, 740, 300), (1e-7, 10 ** -3.8), (0, 1.0), xlog=True)
    rows = lab8a_rows([10 ** (-7.0 + 3.2 * i / 110.0) for i in range(111)])
    xs = [r["c_tot"] for r in rows]
    o = axes(s, ax, [(10.0 ** k, p10(k)) for k in range(-7, -3)], [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1.0)],
             f"TOTAL calcium c{sub('tot', s, 'label')} (M, log scale)", "fraction of sites bound θ",
             ylab_x=28)
    o.append(H.line(s, ax.X(S_TOT), ax.top, ax.X(S_TOT), ax.y0, I["secondary"], "ref", H.DASH_REF))
    o.append(curve(s, ax, xs, [r["theta_naive"] for r in rows], SER[2], "curve_multi", DASH_SER))
    o.append(curve(s, ax, xs, [r["theta_true"] for r in rows], SER[1]))
    w = WORST8A
    o.append(H.line(s, ax.X(w["c_tot"]), ax.Y(w["theta_naive"]), ax.X(w["c_tot"]), ax.Y(w["theta_true"]), SER[0], "curve"))
    o.append(dot(s, ax.X(w["c_tot"]), ax.Y(w["theta_naive"]), SER[2]))
    o.append(dot(s, ax.X(w["c_tot"]), ax.Y(w["theta_true"]), SER[1]))
    o.append(lab(s, ax.X(w["c_tot"]) + 12, ax.Y(0.86), f"widest gap {w['theta_naive'] - w['theta_true']:.2f}", "label"))
    o.append(lab(s, ax.X(w["c_tot"]) + 12, ax.Y(0.86) + 18, f"at {w['c_tot'] * 1e6:.2f} µM total:", "label2", I["secondary"]))
    o.append(lab(s, ax.X(w["c_tot"]) + 12, ax.Y(0.86) + 35, f"{w['theta_naive']:.3f} against {w['theta_true']:.3f}",
                 "label2", I["secondary"]))
    h = HALF8A
    o.append(dot(s, ax.X(h["c_tot"]), ax.Y(h["theta_true"]), O["flag"]))
    o.append(lab(s, ax.X(h["c_tot"]) - 12, ax.Y(0.56), f"half-bound at {h['c_tot'] * 1e6:.1f} µM total", anchor="end"))
    o.append(lab(s, ax.X(h["c_tot"]) - 12, ax.Y(0.56) + 17, "(fixed ligand: 1.0 µM)", "label2", I["secondary"], "end"))
    o.append(lab(s, ax.X(S_TOT) + 8, ax.Y(0.08) - 16, "70 µM", "label2", I["secondary"]))
    o.append(lab(s, ax.X(S_TOT) + 8, ax.Y(0.08), "of sites", "label2", I["secondary"]))
    o.append(lab(s, ax.X(2.2e-7), ax.Y(0.60), "if free = total", "label2", I["primary"]))
    o.append(lead(s, ax.X(7.0e-7), ax.Y(0.60) + 4, ax.X(9.5e-7), ax.Y(theta(9.5e-7)) - 2, SER[2]))
    o.append(lab(s, ax.X(5.0e-6), ax.Y(0.30), "solved with depletion", "label2", I["primary"]))
    o.append(lead(s, ax.X(1.2e-5), ax.Y(0.30) + 4, ax.X(1.6e-5), ax.Y(theta(free_from_total(1.6e-5))) - 3, SER[1]))
    o += legend(s, ax.x0, 26, [(SER[2], DASH_SER, "free = total (§6, ligand in excess)"),
                               (SER[1], None, "conservation solved (Lab 8A)"), (SER[0], None, "widest gap")], gap=20)
    aria = ("Fraction of sites bound against total calcium on a logarithmic axis from 0.1 to 158 micromolar, for 70 "
            "micromolar of cooperative sites with half-activation 1 micromolar and Hill coefficient 3, computed with the Lab 8A "
            "code. A dashed orange curve takes the free concentration equal to the total and saturates by about 4 micromolar. "
            "A solid blue curve solves conservation with depletion and reaches half occupancy only at "
            f"{h['c_tot'] * 1e6:.1f} micromolar total. A red bar marks the widest gap, "
            f"{w['theta_naive'] - w['theta_true']:.2f} in absolute occupancy at {w['c_tot'] * 1e6:.2f} micromolar total, "
            f"{w['theta_naive']:.3f} against {w['theta_true']:.3f}. A dashed vertical line marks the 70 micromolar of sites, "
            "past which the solid curve saturates.")
    hv = hover(ax, [ax.X(x) for x in xs], [[ax.Y(r["theta_true"]), ax.Y(r["theta_naive"])] for r in rows],
               [f"total {r['c_tot'] * 1e6:.3g} µM, free {r['c_free'] * 1e6:.3g} µM: θ = {r['theta_true']:.3f} "
                f"(free = total: {r['theta_naive']:.3f})" for r in rows])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #29: Lab 8B, the cooled pump (code ported unchanged)
DH0P = -20.5e3           # J/mol, ATP hydrolysis, section 3
DG0P_298 = -30.5e3       # J/mol at 298.15 K, section 3
DS0P = (DH0P - DG0P_298) / 298.15        # J/(mol K), assuming dCp = 0
Q_WORK = 2.10e-4         # reaction quotient, working muscle, section 3
CA_RATIO = 1.0e4         # SR lumen over cytosol, section 3
N_CA = 2                 # calcium ions per ATP
EA8B = 70.0e3            # J/mol, from Q_10 = 2.5, section 6


def dg0_prime(t):
    return DH0P - t * DS0P


def dg_atp(t, q=Q_WORK):
    return dg0_prime(t) + R_G * t * math.log(q)


def dg_climb(t, ratio=CA_RATIO, n=N_CA):
    return n * R_G * t * math.log(ratio)


def margin(t):
    return dg_atp(t) + dg_climb(t)


def rate_factor(t, ea=EA8B, t_ref=T_BODY):
    return math.exp(-ea / R_G * (1.0 / t - 1.0 / t_ref))


TEMPS8B = [283.15 + 27.0 * i / 54.0 for i in range(55)]
assert round(dg_atp(T_BODY) / 1e3, 2) == -52.74 and round(dg_atp(283.15) / 1e3, 2) == -49.93
assert round(dg_climb(T_BODY) / 1e3, 2) == 47.50 and round(dg_climb(283.15) / 1e3, 2) == 43.37
assert round(margin(T_BODY) / 1e3, 2) == -5.24 and round(margin(283.15) / 1e3, 2) == -6.57
assert round(rate_factor(283.15), 3) == 0.075 and round(1 / rate_factor(283.15), 1) == 13.3
assert all(margin(t) < 0 for t in TEMPS8B)


def fig29():
    VB = (0, 0, 760, 372)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((88, 56, 668, 300), (10, 37), (-7, 0))
    axr = Ax((88, 56, 668, 300), (10, 37), (0, 1.0))
    tc = [t - 273.15 for t in TEMPS8B]
    o = axes(s, ax, [(v, f"{v}") for v in (10, 15, 20, 25, 30, 35, 37)], [(v, mn(v, "{:.0f}")) for v in range(-7, 1)],
             "temperature (°C)", "net margin of the pump cycle (kJ mol⁻¹)", ylab_x=30)
    # right axis, drawn locally
    o.append(H.line(s, axr.x1, axr.y0, axr.x1, axr.top, I["axis"], "axis"))
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        o.append(H.line(s, axr.x1, axr.Y(v), axr.x1 + 5, axr.Y(v), I["axis"], "leader"))
        o.append(lab(s, axr.x1 + 9, axr.Y(v) + 4.5, f"{v:g}", "tick", I["secondary"]))
    yr = (axr.y0 + axr.top) / 2
    o.append(lab(s, axr.x1 + 62, yr, "every rate, relative to 37 °C", "label", I["primary"], "middle",
                 f'transform="rotate(90 {axr.x1 + 62:.2f} {yr:.2f})"'))
    o.append(H.line(s, ax.x0, ax.top, ax.x1, ax.top, I["secondary"], "ref", H.DASH_REF))
    o.append(lab(s, ax.x0 + 10, ax.top + 18, "stall: margin = 0 (never reached; all 55 points negative)", "label2", I["secondary"]))
    o.append(curve(s, ax, tc, [margin(t) / 1e3 for t in TEMPS8B], SER[3]))
    o.append(curve(s, axr, tc, [rate_factor(t) for t in TEMPS8B], SER[0], "curve", DASH_SER))
    m37, m10 = margin(T_BODY) / 1e3, margin(283.15) / 1e3
    o.append(dot(s, ax.X(37), ax.Y(m37), SER[3]))
    o.append(dot(s, ax.X(10), ax.Y(m10), SER[3]))
    o.append(dot(s, axr.X(10), axr.Y(rate_factor(283.15)), SER[0]))
    o.append(dot(s, axr.X(37), axr.Y(1.0), SER[0]))
    o.append(lab(s, ax.X(10.6), ax.Y(-4.45), "margin: MORE favourable when cold", "label"))
    o.append(lab(s, ax.X(10.6), ax.Y(-4.45) + 18, f"{mn(m37, '{:.2f}')} kJ mol⁻¹ at 37 °C → {mn(m10, '{:.2f}')} at 10 °C",
                 "label2", I["secondary"]))
    o.append(lab(s, ax.X(27.0), ax.Y(-2.6), "rate: collapses", "label", I["primary"], "end"))
    o.append(lab(s, ax.X(27.0), ax.Y(-2.6) + 18, f"{rate_factor(283.15):.3f} at 10 °C, a {1 / rate_factor(283.15):.1f}× slowdown",
                 "label2", I["secondary"], "end"))
    o += legend(s, ax.x0, 26, [(SER[3], None, "net free-energy margin (left axis)"),
                               (SER[0], DASH_SER, "every rate constant, Arrhenius (right axis)")])
    aria = ("Two quantities against temperature from 10 to 37 degrees Celsius, from the Lab 8B code. A solid green curve on "
            "the left axis, from minus 7 to 0 kilojoules per mole, is the net free-energy margin of the coupled calcium pump: "
            "it becomes more negative, so more favourable, as the muscle cools, from minus 5.24 at 37 degrees to minus 6.57 at "
            "10. A dashed line at zero marks the stall, which none of the 55 computed points reaches. A dashed red curve on "
            "the right axis, from 0 to 1, is every rate constant relative to body temperature, collapsing to 0.075 at 10 "
            "degrees, a 13.3-fold slowdown.")
    hv = hover(ax, [ax.X(x) for x in tc], [[ax.Y(margin(t) / 1e3), axr.Y(rate_factor(t))] for t in TEMPS8B],
               [f"{x:.1f} °C: margin {mn(margin(t) / 1e3, '{:.2f}')} kJ/mol, rate × {rate_factor(t):.3f}"
                for x, t in zip(tc, TEMPS8B)])
    return svg(VB, aria, s, o, hv)


# ================================================================ problem figures, 400 px
W = 400


def pscale(h):
    return H.Scale(W, h, display_w=400)


# ---------------------------------------------------------------- svg #30, K2: the ceiling along a fatiguing bout
DG0P_37 = dg0_prime(T_BODY)                                      # J/mol at 310.15 K (Lab 8B's dG0'(T))
D_STROKE = 10e-9                                                 # m


def k2_state(t):
    pi = 2e-3 + 0.22e-3 * t
    adp = 13e-6 * (pi / 2e-3) ** 1.35
    atp = 5.5e-3 - 0.5e-3 * t / 60.0
    return pi, adp, atp


def ceiling(t):
    """|dG| / (N_A d), pN."""
    pi, adp, atp = k2_state(t)
    dg = DG0P_37 + R_G * T_BODY * math.log(adp * pi / atp)
    return abs(dg) / N_A / D_STROKE * 1e12


K2_T = np.arange(0.0, 60.0 + 1e-9, 0.05)                        # dt = 0.05 s, as the solution
K2_F = np.array([ceiling(t) for t in K2_T])


def _cross(level):
    lo, hi = 0.0, 60.0
    for _ in range(80):
        m = 0.5 * (lo + hi)
        lo, hi = (m, hi) if ceiling(m) > level else (lo, m)
    return 0.5 * (lo + hi)


K2_CROSS = _cross(9.0)
K2_HALF = _cross(0.5 * (ceiling(0) + ceiling(60)))
assert round(ceiling(0), 2) == 10.38 and round(ceiling(60), 2) == 8.30 and round(k2_state(60)[0] * 1e3, 1) == 15.2
assert round(K2_CROSS, 1) == 26.2 and round(k2_state(K2_CROSS)[0] * 1e3, 1) == 7.8 and round(K2_HALF) == 16


def fig30():
    VB = (0, 0, W, 262)
    s = pscale(VB[3])
    ax = Ax((58, 22, 388, 196), (0, 60), (8, 10.5))
    o = axes(s, ax, [(v, f"{v}") for v in range(0, 61, 10)], [(v, f"{v:g}") for v in (8, 8.5, 9, 9.5, 10, 10.5)],
             "time into the bout (s)", "force ceiling (pN)", ylab_x=16, xlab_dy=42)
    o.append(H.line(s, ax.x0, ax.Y(9), ax.x1, ax.Y(9), I["secondary"], "ref", H.DASH_REF))
    o.append(curve(s, ax, K2_T[::12], K2_F[::12], SER[0]))
    o.append(lab(s, ax.x1 - 4, ax.Y(9) - 7, "9 pN", "label2", I["secondary"], "end"))
    o.append(dot(s, ax.X(K2_CROSS), ax.Y(9), O["flag"]))
    o.append(lab(s, ax.X(K2_CROSS) - 8, ax.Y(9) + 20, f"crosses at t = {K2_CROSS:.1f} s,", anchor="end"))
    o.append(lab(s, ax.X(K2_CROSS) - 8, ax.Y(9) + 36, f"[P{sub('i', s)}] = {k2_state(K2_CROSS)[0] * 1e3:.1f} mM",
                 "label2", I["secondary"], "end"))
    fh = ceiling(K2_HALF)
    o.append(dot(s, ax.X(K2_HALF), ax.Y(fh), SER[0], hollow=True))
    o.append(lab(s, ax.X(K2_HALF) + 9, ax.Y(fh) - 10, f"half the drop by {K2_HALF:.0f} s"))
    o.append(lab(s, ax.X(1.5), ax.Y(8.22), f"{ceiling(0):.2f} → {ceiling(60):.2f} pN over 60 s", "label2", I["secondary"]))
    aria = (f"Problem K2: the thermodynamic ceiling on crossbridge force against time through a 60 second fatiguing bout, "
            f"falling from {ceiling(0):.2f} to {ceiling(60):.2f} piconewtons as phosphate rises from 2 to 15.2 millimolar. "
            f"The curve is steep at first and flattens: half the total drop has happened by {K2_HALF:.0f} seconds. A dashed "
            f"line at 9 piconewtons is crossed at {K2_CROSS:.1f} seconds, when phosphate has reached "
            f"{k2_state(K2_CROSS)[0] * 1e3:.1f} millimolar.")
    hv = hover(ax, [ax.X(t) for t in K2_T[::12]], [ax.Y(f) for f in K2_F[::12]],
               [f"t = {t:.1f} s, Pi = {k2_state(t)[0] * 1e3:.1f} mM: ceiling {ceiling(t):.2f} pN" for t in K2_T[::12]])
    return svg(VB, aria, s, o, hv)


# ---------------------------------------------------------------- svg #31, K4: the stoichiometry staircase
DG_STATES = {"resting": 62.52e3, "working": 52.74e3}            # |dG|, J/mol (sec. 3)
RT = R_G * T_BODY


def n_max(ratio, dg):
    return math.floor(dg / (RT * math.log(ratio)))


def stair(dg, lo=1e2, hi=1e6):
    """Exact step polyline: n drops from k to k-1 at ratio exp(dg / (k RT))."""
    pts, r = [], lo
    n = n_max(lo, dg)
    pts.append((lo, n))
    while n >= 1:
        edge = math.exp(dg / (n * RT))
        if edge >= hi:
            break
        pts += [(edge, n), (edge, n - 1)]
        n -= 1
    pts.append((hi, n))
    return pts


assert [n_max(10.0 ** k, DG_STATES["working"]) for k in range(2, 7)] == [4, 2, 2, 1, 1]
assert [n_max(10.0 ** k, DG_STATES["resting"]) for k in range(2, 7)] == [5, 3, 2, 2, 1]
G21_WORK = math.exp(DG_STATES["working"] / (2 * RT))
assert round(G21_WORK / 1e4, 1) == 2.8 and [round(RT * math.log(10.0 ** k) / 1e3, 2) for k in (2, 4, 6)] == [11.88, 23.75, 35.63]


def fig31():
    VB = (0, 0, W, 282)
    s = pscale(VB[3])
    ax = Ax((50, 58, 388, 214), (1e2, 1e6), (0, 6), xlog=True)
    o = axes(s, ax, [(10.0 ** k, p10(k)) for k in range(2, 7)], [(v, f"{v}") for v in range(0, 7)],
             "concentration ratio held (log scale)", f"n{sub('max', s, 'label')}, ions per ATP", ylab_x=16, xlab_dy=42)
    o.append(H.line(s, ax.X(1e4), ax.top, ax.X(1e4), ax.y0, I["secondary"], "ref", H.DASH_REF))
    for (name, dg), col, dash, w in ((("resting", DG_STATES["resting"]), SER[0], None, "curve"),
                                     (("working", DG_STATES["working"]), SER[1], DASH_SER, "curve_multi")):
        o.append(poly(s, [(ax.X(x), ax.Y(y)) for x, y in stair(dg)], col, w, dash))
    o.append(dot(s, ax.X(1e4), ax.Y(2), O["flag"]))
    o.append(lab(s, ax.X(1e4) + 7, ax.Y(5.2), "reticulum, 10⁴:"))
    o.append(lab(s, ax.X(1e4) + 7, ax.Y(5.2) + 16, "both allow 2 = observed", "label2", I["secondary"]))
    o.append(lab(s, ax.X(1e4) + 7, ax.Y(5.2) + 32, f"working → 1 at {G21_WORK / 1e4:.1f}×10⁴", "label2", I["secondary"]))
    o.append(lab(s, ax.X(1e4) + 7, ax.Y(5.2) + 48, "(open dot)", "label2", I["secondary"]))
    o.append(dot(s, ax.X(G21_WORK), ax.Y(1), SER[1], hollow=True))
    o.append(lab(s, ax.X(450), ax.Y(3) - 6, "resting"))
    o.append(lab(s, ax.X(1100), ax.Y(2) + 17, "working"))
    o += legend(s, ax.x0 - 40, 22, [(SER[0], None, "resting, |ΔG| 62.52"), (SER[1], DASH_SER, "working, 52.74 kJ/mol")], gap=10)
    aria = ("Problem K4: the largest whole number of ions per ATP the free-energy budget can pay for, against the concentration "
            "ratio the pump must hold, on a log axis from a hundredfold to a millionfold. Two exact staircases: resting muscle "
            "(solid red, 62.52 kilojoules per mole) steps 5, 4, 3, 2, 1; working muscle (dashed blue, 52.74) steps 4, 3, 2, 1. "
            "At ten thousand, the reticulum's gradient, marked by a dashed line, both allow exactly two, the observed "
            f"stoichiometry. The working pump drops from two to one at {G21_WORK / 1e4:.1f} times ten to the four.")
    hr = [10 ** (2 + 4 * k / 160) for k in range(161)]
    hv = hover(ax, [ax.X(r) for r in hr], [[ax.Y(n_max(r, DG_STATES["resting"])), ax.Y(n_max(r, DG_STATES["working"]))] for r in hr],
               [f"ratio {r:.3g}: climb {RT * math.log(r) / 1e3:.2f} kJ/mol per ion; n = {n_max(r, DG_STATES['resting'])} "
                f"resting, {n_max(r, DG_STATES['working'])} working" for r in hr])
    return svg(VB, aria, s, o, hv)


# ---------------------------------------------------------------- svg #32, K5: total closed-system capacity
def beta_tot(ph):
    return sum(beta(ph, c, pk) for _, c, pk, _ in BUFFERS)


K5_PH = np.arange(4.0, 10.0 + 1e-9, 0.001)
K5_B = np.array([beta_tot(x) for x in K5_PH])
K5_OPT = float(K5_PH[int(K5_B.argmax())])
assert round(K5_OPT, 2) == 6.18 and round(float(K5_B.max()), 2) == 15.27 and round(beta_tot(7.4), 2) == 7.43
assert round(100 * (1 - beta_tot(7.4) / K5_B.max())) == 51


def fig32():
    VB = (0, 0, W, 262)
    s = pscale(VB[3])
    ax = Ax((52, 22, 388, 196), (4, 10), (0, 17))
    hp = K5_PH[::60]
    o = axes(s, ax, [(v, f"{v}") for v in range(4, 11)], [(v, f"{v}") for v in (0, 5, 10, 15)],
             "pH", "total capacity (mM per pH)", ylab_x=16, xlab_dy=42)
    bmax, b74 = float(K5_B.max()), beta_tot(7.4)
    o.append(H.line(s, ax.X(K5_OPT), ax.Y(bmax), ax.X(K5_OPT), ax.y0, I["rule"], "leader", H.DASH_REF))
    o.append(H.line(s, ax.X(7.4), ax.Y(b74), ax.X(7.4), ax.y0, I["rule"], "leader", H.DASH_REF))
    o.append(curve(s, ax, hp, [beta_tot(x) for x in hp], SER[0]))
    o.append(dot(s, ax.X(K5_OPT), ax.Y(bmax), O["flag"]))
    o.append(dot(s, ax.X(7.4), ax.Y(b74), O["flag"]))
    o.append(lab(s, ax.X(4.1), ax.Y(15.4), f"optimum, pH {K5_OPT:.2f}:"))
    o.append(lab(s, ax.X(4.1), ax.Y(15.4) + 16, f"{bmax:.2f} mM/pH", "label2", I["secondary"]))
    o.append(lead(s, ax.X(4.1) + tw(f"optimum, pH {K5_OPT:.2f}:") + 4, ax.Y(15.4) - 4, ax.X(K5_OPT) - 6, ax.Y(bmax), I["rule"]))
    o.append(lab(s, ax.X(7.4) + 18, ax.Y(b74) - 6, f"body, pH 7.40: {b74:.2f}"))
    o.append(lab(s, ax.X(7.4) + 18, ax.Y(b74) + 10, f"{100 * (1 - b74 / bmax):.0f} % below the optimum", "label2", I["secondary"]))
    o.append(lab(s, ax.X(7.15), ax.Y(15.6), "not a mistake: capacity is a", "label2", I["secondary"]))
    o.append(lab(s, ax.X(7.15), ax.Y(15.6) + 16, "constraint, not the objective", "label2", I["secondary"]))
    aria = (f"Problem K5: total closed-system buffer capacity of bicarbonate, phosphate and protein histidine, summed, against "
            f"pH from 4 to 10. The curve peaks at pH {K5_OPT:.2f} with {bmax:.2f} millimolar per pH unit, dominated by "
            f"bicarbonate whose pKa is 6.10. At the body's pH 7.40 the total is {b74:.2f}, 51 per cent below the optimum. "
            "A note says this is not a mistake: buffer capacity is a constraint, not the quantity being optimised.")
    hv = hover(ax, [ax.X(x) for x in hp], [ax.Y(beta_tot(x)) for x in hp],
               [f"pH {x:.2f}: total {beta_tot(x):.2f} mM per pH" for x in hp])
    return svg(VB, aria, s, o, hv)


# ---------------------------------------------------------------- svg #33, K7: one twitch with and without the buffer
def k7(buffered, c0=0.1, dt=0.02, t_end=60.0):
    """Free Ca (µM) against t (ms). Release (R/tau) e^(-t/tau), R = 135 µM, tau = 4 ms; Michaelis-Menten pump
    vmax = 6 mM/s = 6 µM/ms, KM = 0.5 µM; 70 µM Hill sites, K = 1 µM, nH = 3. Euler at 20 µs.
    c0 = 0.1 µM, sec. 1's resting level (the problem does not state it; c0 = 0 gives a different peak)."""
    n = int(round(t_end / dt))
    ts, cs = np.zeros(n + 1), np.zeros(n + 1)
    c = c0
    cs[0] = c
    for i in range(n):
        t = i * dt
        j_in = 135.0 / 4.0 * math.exp(-t / 4.0)
        j_out = 6.0 * c / (0.5 + c)
        f = 1.0 + (70.0 * 3.0 * c ** 2 / (1.0 + c ** 3) ** 2 if buffered else 0.0)
        c = max(c + dt * (j_in - j_out) / f, 0.0)
        ts[i + 1], cs[i + 1] = t + dt, c
    return ts, cs


K7_B = k7(True)
K7_U = k7(False)
K7_PB, K7_PU = float(K7_B[1].max()), float(K7_U[1].max())
assert round(K7_PB, 2) == 10.08 and round(K7_PU, 1) == 70.7 and round(K7_PU / K7_PB, 1) == 7.0
assert round(hill(K7_PB, 3), 3) == 0.999


def above_floor(ts, cs, floor=0.1):
    """Points of the curve down to its first crossing below the axis floor (interpolated to the floor)."""
    k = int(np.argmax(cs))
    j = k + int(np.argmax(cs[k:] < floor))
    t_end = ts[j - 1] + (ts[j] - ts[j - 1]) * (cs[j - 1] - floor) / (cs[j - 1] - cs[j])
    return list(ts[:j]) + [t_end], list(np.maximum(cs[:j], floor)) + [floor], t_end


def fig33():
    VB = (0, 0, W, 268)
    s = pscale(VB[3])
    ax = Ax((58, 50, 388, 204), (0, 50), (0.1, 100), ylog=True)
    o = axes(s, ax, [(v, f"{v}") for v in range(0, 51, 10)], [(v, f"{v:g}") for v in (0.1, 1, 10, 100)],
             "time (ms)", "free Ca²⁺ (µM, log)", ylab_x=16, xlab_dy=42)
    o.append(H.line(s, ax.x0, ax.Y(10), ax.x1, ax.Y(10), I["secondary"], "ref", H.DASH_REF))
    o.append(lab(s, ax.x1 - 4, ax.Y(10) - 7, "§1's activated level, 10 µM", "label2", I["secondary"], "end"))
    ends = {}
    for key, (ts, cs), col, dash in (("u", K7_U, SER[2], DASH_SER), ("b", K7_B, SER[1], None)):
        xs, ys, te = above_floor(ts, cs)
        ends[key] = te
        sel = list(range(0, len(xs) - 1, 16)) + [len(xs) - 1]
        o.append(curve(s, ax, [xs[i] for i in sel], [ys[i] for i in sel], col, "curve_multi" if dash else "curve", dash))
    tb, tu = float(K7_B[0][K7_B[1].argmax()]), float(K7_U[0][K7_U[1].argmax()])
    o.append(dot(s, ax.X(tu), ax.Y(K7_PU), SER[2]))
    o.append(dot(s, ax.X(tb), ax.Y(K7_PB), SER[1]))
    o.append(lab(s, ax.X(15), ax.Y(K7_PU) + 4, f"no buffer: peak {K7_PU:.1f} µM"))
    o.append(lead(s, ax.X(15) - 3, ax.Y(K7_PU), ax.X(tu) + 6, ax.Y(K7_PU), I["rule"]))
    o.append(lab(s, ax.X(33.5), ax.Y(3.2), "70 µM of sites:"))
    o.append(lab(s, ax.X(33.5), ax.Y(3.2) + 16, f"peak {K7_PB:.2f} µM,", "label2", I["secondary"]))
    o.append(lab(s, ax.X(33.5), ax.Y(3.2) + 32, f"÷ {K7_PU / K7_PB:.1f} by buffering", "label2", I["secondary"]))
    o += legend(s, ax.x0 - 40, 20, [(SER[2], DASH_SER, "no buffer"), (SER[1], None, "70 µM of cooperative sites")], gap=12)
    o.append(lab(s, ax.x0 - 40, 38, "Both end below the 0.1 µM start (no leak in the model).", "label2", I["secondary"]))
    aria = (f"Problem K7: free cytosolic calcium against time through one twitch, 0 to 50 milliseconds, on a log axis from "
            f"0.1 to 100 micromolar, starting from 0.1 micromolar. A dashed orange curve is the transient with no buffering, "
            f"peaking at {K7_PU:.1f} micromolar at {tu:.1f} milliseconds. A solid blue curve is the same release with 70 "
            f"micromolar of cooperative sites, peaking at {K7_PB:.2f} micromolar at {tb:.1f} milliseconds, rising and decaying "
            f"more slowly. A dashed line marks section 1's activated level of 10 micromolar, which the buffered peak "
            f"reproduces. Buffering divides the peak by {K7_PU / K7_PB:.1f}. Both curves fall below the 0.1 micromolar start, "
            f"at {ends['u']:.0f} and {ends['b']:.0f} milliseconds, because the model has no leak.")
    ht = np.arange(0.0, 50.0 + 1e-9, 0.5)
    ib = [int(round(t / 0.02)) for t in ht]
    hv = hover(ax, [ax.X(t) for t in ht],
               [[ax.Y(max(K7_B[1][i], 0.1)), ax.Y(max(K7_U[1][i], 0.1))] for i in ib],
               [f"t = {t:.1f} ms: {K7_B[1][i]:.3g} µM buffered, {K7_U[1][i]:.3g} µM unbuffered" for t, i in zip(ht, ib)])
    return svg(VB, aria, s, o, hv)


FIGS = {
    18: ("Buffer capacity in millimolar per pH unit, against pH from 4", fig18),
    19: ("Log-log plot of the electrostatic contribution to a persiste", fig19),
    20: ("Fraction of calcium-binding sites occupied against pCa, from", fig20),
    21: ("Rate relative to its value at 37 degrees Celsius, against te", fig21),
    22: ("Michaelis-Menten curve of reaction rate over maximal rate ag", fig22),
    24: ("Fixed charge concentration in molar against glycosaminoglyca", fig24),
    27: ("Fraction of sites bound against TOTAL calcium on a logarithm", fig27),
    29: ("Two quantities against temperature from 10 to 37 degrees Cel", fig29),
    30: ("The thermodynamic ceiling on crossbridge force against time ", fig30),
    31: ("A staircase of the largest integer number of ions per ATP th", fig31),
    32: ("Total closed-system buffer capacity of the three intracellul", fig32),
    33: ("Free cytosolic calcium against time through one twitch, over", fig33),
}
