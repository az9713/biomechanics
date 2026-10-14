"""Module 6 problem plots C1-C9, D1-D9 (svg #31-#49 of the C/D strands): house-style redraws at 400 px.

Every plotted number is computed here from the law or the constants the module states:
the crimp law (Eq. 1.2 / 2.3) with E_lin = 1.3 GPa, eps* = 3 %, A0 = 80 mm^2, L0 = 0.25 m
(module06 lines 264-266, 1290-1293), the SLS (Eq. 6.3 / 7.3) with the K5-K8 constants
(lines 1064, 1113, 1139), and the tissue table of section 7 (lines 600-603).
"""
import math

import numpy as np

import house as H
from m05.plots_prob import Plot, hov, label, legend, sub, svg

O, I, SER = H.OVERLAY, H.INK, H.SERIES
W = 400

# ---------------------------------------------------------------- module constants
E_LIN, EPS_S = 1.3e9, 0.03                       # Pa, toe-limit strain (section 1, Appendix)
A0, L0 = 80e-6, 0.25                             # m^2, m (section 2)
K_LIN = A0 * E_LIN / L0                          # N/m, Eq. 2.2
X_S = EPS_S * L0                                 # m, toe end
assert round(K_LIN / 1e3) == 416 and round(X_S * 1e3, 1) == 7.5 and round(K_LIN * X_S / 2) == 1560
E_R, TS = 1.20e9, 0.050                          # SLS relaxed modulus, tau_sigma (K5-K8)


def sigma(e):
    """Eq. 1.2, the crimp material law (Pa)."""
    e = np.asarray(e, float)
    return np.where(e <= EPS_S, E_LIN * e**2 / (2 * EPS_S), E_LIN * (e - EPS_S / 2))


def force(x):
    """Eq. 2.3, the structural law (N), x in m."""
    x = np.asarray(x, float)
    return np.where(x <= X_S, K_LIN * x**2 / (2 * X_S), K_LIN * (x - X_S / 2))


def estar(w, te, ts=TS, er=E_R):
    """Eq. 7.3, the SLS complex modulus."""
    return er * (1 + 1j * w * te) / (1 + 1j * w * ts)


def k8_loop(ratio, e0=0.01, f=2.6, n=4000):
    """K8 tension-only cycle eps = e0/2 (1 - cos wt), SLS steady state in closed form.
    Returns eps, sigma over one cycle (loading half first) and the resilience W_out / W_in."""
    w = 2 * math.pi * f
    Es = estar(w, ratio * TS)
    a = e0 / 2
    ph = np.linspace(0, 2 * math.pi, n + 1)
    e = a - a * np.cos(ph)
    s = E_R * a - a * (Es.real * np.cos(ph) - Es.imag * np.sin(ph))
    de = np.diff(e)
    sm = (s[1:] + s[:-1]) / 2
    w_in, w_out = (sm * de)[de > 0].sum(), -(sm * de)[de < 0].sum()
    return e, s, w_out / w_in


R_TEN, R_LIG = k8_loop(1.10)[2], k8_loop(1.20)[2]
assert (round(100 * R_TEN, 1), round(100 * R_LIG, 1)) == (92.6, 85.7), (R_TEN, R_LIG)   # K8, line 1139


def poly(P, xs, ys, col, op):
    pts = " ".join(f"{P.X(x):.1f},{P.Y(y):.1f}" for x, y in zip(xs, ys))
    return f'<polygon points="{pts}" fill="{col}" opacity="{op}"/>'


def dashv(P, x, y_top=None):
    return H.line(P.s, P.X(x), P.y0, P.X(x), P.y1 if y_top is None else P.Y(y_top), O["dim"], "ref", H.DASH_REF)


# ---------------------------------------------------------------- #31 C1: the J-curve against a Hookean line
def fig31():
    VB = (0, 0, W, 268)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 46, 388, 210), (0, 8), (0, 90))
    e = np.linspace(0, 0.08, 321)
    sg = sigma(e) / 1e6
    eh = np.linspace(0, 90e6 / E_LIN, 50)
    s_star = float(sigma(EPS_S)) / 1e6
    assert round(s_star, 1) == 19.5
    o = [P.axes([(v, f"{v}") for v in (0, 2, 4, 6, 8)], [(0, "0"), (30, "30"), (60, "60"), (90, "90")],
                "strain ε (%)", "stress σ (MPa)", grid=(30, 60, 90))]
    o.append(dashv(P, 3, s_star))
    o.append(P.curve(eh * 100, E_LIN * eh / 1e6, SER[1], multi=True, dash=(6, 4)))
    o.append(P.curve(e * 100, sg, SER[0]))
    o.append(P.dot(3, s_star, SER[0]))
    o.append(legend(s, 58, 20, [(SER[0], "tendon (J-curve)", None), (SER[1], "ideal Hookean σ = E" + sub("lin", s, "label2") + "ε", (6, 4))]))
    o.append(label(s, P.X(0.15), P.Y(25), "toe (crimp)", "label2", I["primary"]))
    o.append(H.line(s, P.X(0.9), P.Y(24), P.X(1.4), P.Y(float(sigma(0.014)) / 1e6) - 3, I["secondary"], "leader"))
    o.append(label(s, P.X(3) + 6, P.Y(s_star) + 16, f"ε* = 3%, σ = {s_star:.1f} MPa", "label2", I["secondary"]))
    o.append(label(s, P.X(7.9), P.Y(40), "linear: all", "label2", I["primary"], "end"))
    o.append(label(s, P.X(7.9), P.Y(40) + 15, "fibrils recruited", "label2", I["primary"], "end"))
    o.append(label(s, P.X(5.6), P.Y(78), "Hookean", "label2", I["secondary"], "end"))
    aria = ("Problem C1 plot: tendon stress against strain from 0 to 8 percent, from the crimp law with E lin = 1.3 "
            "gigapascals and toe strain 3 percent. The curve starts flat and bends upward through the toe, where crimped "
            "fibrils are recruited, reaching 19.5 megapascals at 3 percent, then continues as a straight line of slope "
            "E lin. A dashed straight Hookean line of the same slope from the origin lies above it.")
    hv = hov(P, e[::3] * 100, [sg[::3]], lambda i: f"ε = {e[::3][i] * 100:.2f}%, σ = {sg[::3][i]:.1f} MPa")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #33 C3: tangent against secant stiffness
def fig33():
    VB = (0, 0, W, 268)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 46, 388, 210), (0, 12), (0, 3))
    xw = 0.006                                   # working point in the toe (x* = 7.5 mm)
    fw = float(force(xw))
    ksec, ktan = fw / xw, K_LIN * xw / X_S       # chord slope; local slope dF/dx (Eq. 2.2)
    assert (round(fw), round(ksec / 1e3), round(ktan / 1e3)) == (998, 166, 333), (fw, ksec, ktan)
    x = np.linspace(0, 0.012, 241)
    F = force(x) / 1e3
    o = [P.axes([(v, f"{v}") for v in (0, 3, 6, 9, 12)], [(0, "0"), (1, "1"), (2, "2"), (3, "3")],
                "elongation x (mm)", "force F (kN)", grid=(1, 2, 3))]
    o.append(H.line(s, P.X(7.5), P.y0, P.X(7.5), P.y1, I["rule"], "leader", H.DASH_REF))
    o.append(P.curve([0, 6], [0, fw / 1e3], SER[1], multi=True, dash=(6, 4)))
    xt = np.array([3.2, 10.5])
    o.append(P.curve(xt, fw / 1e3 + ktan * (xt - 6) / 1e6, SER[2], multi=True))
    o.append(P.curve(x * 1e3, F, SER[0]))
    o.append(P.dot(6, fw / 1e3, SER[0]))
    o.append(legend(s, 58, 20, [(SER[0], "F(x)", None), (SER[1], "secant", (6, 4)), (SER[2], "tangent", None)]))
    o.append(label(s, P.X(6) - 8, P.Y(fw / 1e3) - 8, "working point, 6 mm", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(0.3), P.Y(2.2), f"secant F/x = {ksec / 1e3:.0f} N/mm", "label2", I["primary"]))
    o.append(label(s, P.X(0.3), P.Y(2.2) + 15, "(chord from the origin)", "label2", I["secondary"]))
    o.append(label(s, P.X(11.9), P.Y(0.75), "tangent k = dF/dx", "label2", I["primary"], "end"))
    o.append(label(s, P.X(11.9), P.Y(0.75) + 15, f"= {ktan / 1e3:.0f} N/mm", "label2", I["primary"], "end"))
    o.append(label(s, P.X(7.5) + 4, P.y1 + 12, "x* = 7.5 mm", "label2", I["muted"]))
    aria = ("Problem C3 plot: tendon force against elongation from 0 to 12 millimetres, with a working point in the toe "
            "at 6 millimetres and 1.0 kilonewton. A dashed secant from the origin to the point has slope F over x = 166 "
            "newtons per millimetre; the tangent at the point, the local slope dF/dx, is twice as steep at 333 newtons "
            "per millimetre. Small vibrations about the point see the tangent stiffness.")
    hv = hov(P, x[::3] * 1e3, [F[::3]], lambda i: f"x = {x[::3][i] * 1e3:.1f} mm, F = {F[::3][i]:.2f} kN, "
             f"secant {F[::3][i] / max(x[::3][i] * 1e3, 1e-9):.0f} N/mm")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #34 C4: tendon and ligament loops (K8 cycle)
def fig34():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    yr = (-1, 14)
    Ps = [Plot(s, (58, 46, 210, 206), (0, 1), yr), Plot(s, (236, 46, 388, 206), (0, 1), yr)]
    o, panels = [], []
    for k, (P, ratio, name, R, col) in enumerate(((Ps[0], 1.10, "tendon", R_TEN, SER[0]),
                                                  (Ps[1], 1.20, "ligament", R_LIG, SER[1]))):
        e, sg, _ = k8_loop(ratio)
        ep, sp = e * 100, sg / 1e6
        o.append(P.axes([(0, "0"), (0.5, "0.5"), (1, "1")], [(0, "0"), (5, "5"), (10, "10")],
                        "strain ε (%)", "stress σ (MPa)" if k == 0 else "", grid=(5, 10)))
        o.append(poly(P, ep[::20], sp[::20], col, 0.18))
        o.append(P.curve(ep, sp, col, multi=True))
        o.append(label(s, P.x0 + 6, P.y1 - 10, f"{name}, τ{sub('ε', s, 'label2')}/τ{sub('σ', s, 'label2')} = {ratio:.2f}",
                       "label2", I["primary"]))
        o.append(label(s, P.X(0.97), P.Y(1.6), f"R = {100 * R:.1f}%", "label", I["primary"], "end"))
        o.append(label(s, P.X(0.97), P.Y(1.6) - 17, f"lost {100 * (1 - R):.1f}%", "label2", I["secondary"], "end"))
        idx = list(range(0, len(e) // 2 + 1, 25))
        panels.append((P.box, [[round(P.X(ep[i]), 2), [round(P.Y(sp[i]), 2), round(P.Y(sp[-1 - i]), 2)],
                                f"ε = {ep[i]:.2f}%: loading {sp[i]:.1f} MPa, unloading {sp[-1 - i]:.1f} MPa"] for i in idx]))
    o.append(label(s, W / 2, 20, "shaded loop = energy lost per cycle (K8: 1% cycle at 2.6 Hz)", "label2",
                   I["secondary"], "middle"))
    aria = ("Problem C4 plot, the K8 tension-only cycle to 1 percent strain at 2.6 hertz through the standard linear "
            "solid. Left, a tendon with tau epsilon over tau sigma = 1.10 traces a thin loop and returns 92.6 percent of "
            "the work put in. Right, a ligament with ratio 1.20 traces a fatter loop and returns 85.7 percent. The shaded "
            "loop area is the energy lost as heat per cycle.")
    return svg(VB, aria, s, "".join(o), (panels,))


# ---------------------------------------------------------------- #37 C7: creep and relaxation, SLS step tests
def fig37():
    VB = (0, 0, W, 322)
    s = H.Scale(W, VB[3], display_w=400)
    TE = 0.090                                   # tau_eps (s), K5 constants (line 1064)
    EI = E_R * TE / TS
    assert round(EI / 1e9, 2) == 2.16
    E0, S0 = 0.02, 24e6                          # 2 % step strain; the stress that holds 2 % at equilibrium
    t = np.linspace(-0.1, 0.5, 241)
    on = t >= 0
    creep = np.where(on, S0 / E_R - (S0 / E_R - S0 / EI) * np.exp(-np.clip(t, 0, None) / TE), 0.0) * 100
    relax = np.where(on, E0 * (E_R + (EI - E_R) * np.exp(-np.clip(t, 0, None) / TS)), 0.0) / 1e6
    assert (round(S0 / EI * 100, 2), round(E0 * EI / 1e6, 1)) == (1.11, 43.2)
    xt = [(0, "0"), (0.2, "0.2"), (0.4, "0.4")]
    pin = [Plot(s, (58, 76, 210, 112), (-0.1, 0.5), (0, 30)), Plot(s, (236, 76, 388, 112), (-0.1, 0.5), (0, 2.5))]
    pout = [Plot(s, (58, 138, 210, 262), (-0.1, 0.5), (0, 2.5)), Plot(s, (236, 138, 388, 262), (-0.1, 0.5), (0, 50))]
    step = lambda v: ([-0.1, 0, 0, 0.5], [0, 0, v, v])          # noqa: E731
    o = [legend(s, 40, 20, [(I["primary"], "held step", None), (SER[0], "strain response", None),
                            (SER[1], "stress response", None)])]
    o.append(label(s, 134, 46, "creep: hold σ", "label", I["primary"], "middle"))
    o.append(label(s, 312, 46, "relaxation: hold ε", "label", I["primary"], "middle"))
    for P, yt, yl in ((pin[0], [(0, "0"), (24, "24")], "σ (MPa)"), (pin[1], [(0, "0"), (2, "2")], "ε (%)")):
        o.append(P.axes([], yt, "", "", grid=()))
        o.append(label(s, P.x0 + 4, P.y1 - 2, yl, "label2", I["secondary"]))
    o.append(pin[0].curve(*step(24), I["primary"], multi=True))
    o.append(pin[1].curve(*step(2), I["primary"], multi=True))
    for k, (P, yt, yl) in enumerate(((pout[0], [(0, "0"), (1, "1"), (2, "2")], "ε (%)"),
                                     (pout[1], [(0, "0"), (24, "24"), (43.2, "43")], "σ (MPa)"))):
        o.append(P.axes(xt, yt, "time t (s)", "", grid=()))
        o.append(label(s, P.x0 + 4, P.y1 - 2, yl, "label2", I["secondary"]))
    o.append(H.line(s, pout[0].x0, pout[0].Y(2), pout[0].x1, pout[0].Y(2), O["dim"], "ref", H.DASH_REF))
    o.append(H.line(s, pout[1].x0, pout[1].Y(24), pout[1].x1, pout[1].Y(24), O["dim"], "ref", H.DASH_REF))
    o.append(pout[0].curve(t, creep, SER[0], multi=True))
    o.append(pout[1].curve(t, relax, SER[1], multi=True))
    o.append(label(s, pout[0].X(0.48), pout[0].Y(0.75), "ε grows", "label2", I["primary"], "end"))
    o.append(label(s, pout[0].X(0.48), pout[0].Y(0.75) + 15, "1.11 → 2.00%", "label2", I["secondary"], "end"))
    o.append(label(s, pout[1].X(0.48), pout[1].Y(15), "σ decays", "label2", I["primary"], "end"))
    o.append(label(s, pout[1].X(0.48), pout[1].Y(15) + 15, "43.2 → 24 MPa", "label2", I["secondary"], "end"))
    aria = ("Problem C7 plot: the two step tests on one standard linear solid with the K5 tendon constants, relaxed "
            "modulus 1.20 and instantaneous modulus 2.16 gigapascals. Left, creep: a stress of 24 megapascals is held "
            "from t = 0, and the strain jumps to 1.11 percent then grows toward 2 percent with the creep time 0.09 "
            "seconds. Right, relaxation: a strain of 2 percent is held, and the stress jumps to 43.2 megapascals then "
            "decays toward 24 megapascals with the relaxation time 0.05 seconds.")
    j = list(range(0, len(t), 2))
    panels = []
    for P, src, f in ((pin[0], np.where(on, 24.0, 0.0), "σ = {:.0f} MPa"), (pin[1], np.where(on, 2.0, 0.0), "ε = {:.0f}%"),
                      (pout[0], creep, "ε = {:.2f}%"), (pout[1], relax, "σ = {:.1f} MPa")):
        panels.append((P.box, hov(P, t[j], [src[j]], lambda i, src=src, f=f: f"t = {t[j][i]:.2f} s, " + f.format(src[j][i]))))
    return svg(VB, aria, s, "".join(o), (panels,))


# ---------------------------------------------------------------- #39 C9: the resilience spectrum (section 7 table)
TISSUES = [("tendon (Achilles)", 0.90, 0.95), ("ligament", 0.80, 0.90), ("skin / fascia", 0.60, 0.80),
           ("intervertebral disc", 0.50, 0.70)]                       # module06 lines 600-603


def fig39():
    VB = (0, 0, W, 252)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (138, 50, 388, 190), (0.5, 1.0), (0, 4))
    o = [P.axes([(v, f"{v:g}") for v in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)], [], "resilience R = energy returned / stored", "")]
    hv = []
    for k, (name, lo, hi) in enumerate(TISSUES):
        yc = P.Y(3.5 - k)
        o.append(f'<rect x="{P.X(lo):.2f}" y="{yc - 9:.2f}" width="{P.X(hi) - P.X(lo):.2f}" height="18" '
                 f'fill="{SER[1]}" opacity="0.75"/>')
        o.append(label(s, P.x0 - 8, yc + 4.5, name, "label2", I["primary"], "end"))
        hv.append([round(P.X((lo + hi) / 2), 2), round(yc, 2), f"{name}: R ≈ {lo:.2f}–{hi:.2f}, loss {100 * (1 - hi):.0f}–{100 * (1 - lo):.0f}%"])
    for k, R in ((0, R_TEN), (1, R_LIG)):
        o.append(P.dot(R, 3.5 - k, SER[0]))
    o.append(legend(s, 58, 20, [(SER[1], "measured range (§7 table)", None)]))
    o.append(f'<circle cx="{262:.2f}" cy="15.5" r="{s(H.PX["dot"]):.2f}" fill="{SER[0]}" stroke="#fff" stroke-width="{s(1.5):.2f}"/>')
    o.append(label(s, 271, 20, "SLS loop (K8)", "label2", I["secondary"]))
    o.append(label(s, P.X(1.0), P.y1 - 8, "spring (returns) →", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.5), P.y1 - 8, "← damper (absorbs)", "label2", I["primary"], "start"))
    aria = ("Problem C9 plot: resilience ranges of four collagenous tissues from the section 7 table, on an axis from "
            "0.5 to 1. Tendon returns 0.90 to 0.95 of the energy it stores, ligament 0.80 to 0.90, skin and fascia 0.6 "
            "to 0.8, and the intervertebral disc 0.5 to 0.7. Dots mark the K8 standard-linear-solid loops, 0.926 for "
            "tendon and 0.857 for ligament. The high end is a spring that returns energy, the low end a damper that "
            "absorbs impact.")
    hv.sort(key=lambda q: q[0])
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #41 D1: linear recruitment gives the parabolic toe
def fig41():
    VB = (0, 0, W, 322)
    s = H.Scale(W, VB[3], display_w=400)
    Pf = Plot(s, (58, 22, 388, 92), (0, 6), (0, 1.2))
    Ps = Plot(s, (58, 120, 388, 270), (0, 6), (0, 60))
    e = np.linspace(0, 0.06, 241)
    phi = np.minimum(e / EPS_S, 1.0)
    sg = sigma(e) / 1e6
    s_star = float(sigma(EPS_S)) / 1e6
    d = 1e-7                                      # C1 check at eps*: value and slope agree on both sides
    sl = (float(sigma(EPS_S)) - float(sigma(EPS_S - d))) / d
    sr = (float(sigma(EPS_S + d)) - float(sigma(EPS_S))) / d
    assert abs(sl / E_LIN - 1) < 1e-4 and abs(sr / E_LIN - 1) < 1e-4 and round(s_star, 1) == 19.5
    o = [Pf.axes([], [(0, "0"), (1, "1")], "", "", grid=(1.0,))]
    o.append(label(s, Pf.x0 + 6, Pf.y1 - 6, "engaged fibril fraction Φ", "label2", I["secondary"]))
    o.append(dashv(Pf, 3))
    o.append(Pf.curve(e * 100, phi, SER[1]))
    o.append(label(s, Pf.X(1.7), Pf.Y(0.35), "Φ = ε/ε*", "label2", I["primary"]))
    o.append(label(s, Pf.X(5.9), Pf.Y(1.0) + 16, "Φ = 1, all fibrils taut", "label2", I["primary"], "end"))
    o.append(Ps.axes([(v, f"{v}") for v in range(7)], [(0, "0"), (20, "20"), (40, "40"), (60, "60")],
                     "strain ε (%)", "stress σ (MPa)", grid=(20, 40, 60)))
    o.append(H.line(s, Ps.X(3), Ps.y0, Ps.X(3), Pf.y0, O["dim"], "ref", H.DASH_REF))
    o.append(Ps.curve([1.5, 3], [0, s_star], O["dim"], dash=(4, 3)))
    o.append(Ps.curve(e * 100, sg, SER[0]))
    o.append(Ps.dot(3, s_star, SER[0]))
    o.append(label(s, Ps.X(3) + 4, Ps.Y(50), "ε* = 3%", "label2", I["secondary"]))
    o.append(label(s, Ps.X(0.2), Ps.Y(14), "toe: E" + sub("lin", s, "label2") + "ε²/(2ε*)", "label2", I["primary"]))
    o.append(label(s, Ps.X(3) - 6, Ps.Y(s_star) - 10, f"{s_star:.1f} MPa = E" + sub("lin", s, "label2") + "ε*/2",
                   "label2", I["secondary"], "end"))
    o.append(label(s, Ps.X(5.9), Ps.Y(12), "linear: E" + sub("lin", s, "label2") + "(ε − ε*/2)", "label2", I["primary"], "end"))
    o.append(label(s, Ps.X(5.9), Ps.Y(12) + 15, "same value and slope at ε*", "label2", I["secondary"], "end"))
    aria = ("Problem D1 plot, two panels on one strain axis from 0 to 6 percent. Top: the engaged fibril fraction Phi "
            "rises linearly as epsilon over epsilon star and stays at 1 beyond epsilon star = 3 percent. Bottom: the "
            "stress, a parabolic toe E lin epsilon squared over 2 epsilon star up to 19.5 megapascals at 3 percent, "
            "then the straight line E lin times epsilon minus epsilon star over 2. A dashed extension of the line meets "
            "zero at 1.5 percent; value and slope match at the join.")
    j = list(range(0, len(e), 2))
    hv = [(Pf.box, hov(Pf, e[j] * 100, [phi[j]], lambda i: f"ε = {e[j][i] * 100:.2f}%, Φ = {phi[j][i]:.2f}")),
          (Ps.box, hov(Ps, e[j] * 100, [sg[j]], lambda i: f"ε = {e[j][i] * 100:.2f}%, σ = {sg[j][i]:.1f} MPa"))]
    return svg(VB, aria, s, "".join(o), (hv,))


# ---------------------------------------------------------------- #42 D2: the force law and its tangent stiffness
def fig42():
    VB = (0, 0, W, 322)
    s = H.Scale(W, VB[3], display_w=400)
    Pf = Plot(s, (58, 22, 388, 132), (0, 15), (0, 5))
    Pk = Plot(s, (58, 160, 388, 270), (0, 15), (0, 500))
    x = np.linspace(0, 0.015, 301)
    F = force(x) / 1e3
    k = np.where(x <= X_S, K_LIN * x / X_S, K_LIN) / 1e3
    o = [Pf.axes([], [(0, "0"), (2, "2"), (4, "4")], "", "F (kN)", grid=(2, 4))]
    o.append(H.line(s, Pf.X(7.5), Pk.y0, Pf.X(7.5), Pf.y1, O["dim"], "ref", H.DASH_REF))
    o.append(Pf.curve(x * 1e3, F, SER[0]))
    o.append(Pf.dot(7.5, K_LIN * X_S / 2e3, SER[0]))
    o.append(label(s, Pf.X(7.5) - 6, Pf.Y(1.56) - 8, "1.56 kN", "label2", I["secondary"], "end"))
    o.append(label(s, Pf.X(1.0), Pf.Y(1.3), "toe: k" + sub("lin", s, "label2") + "x²/(2x*)", "label2", I["primary"]))
    o.append(label(s, Pf.X(14.8), Pf.Y(1.6), "linear: k" + sub("lin", s, "label2") + "(x − x*/2)", "label2", I["primary"], "end"))
    o.append(Pk.axes([(v, f"{v}") for v in (0, 3, 6, 9, 12, 15)], [(0, "0"), (200, "200"), (416, "416")],
                     "elongation x (mm)", "k (N/mm)", grid=(200,)))
    o.append(Pk.curve(x * 1e3, k, SER[1]))
    o.append(label(s, Pk.X(7.5) + 4, Pk.y0 - 6, "x* = 7.5 mm", "label2", I["secondary"]))
    o.append(label(s, Pk.X(1.4), Pk.Y(300), "k = k" + sub("lin", s, "label2") + "x/x*", "label2", I["primary"]))
    o.append(label(s, Pk.X(7.5) + 8, Pk.Y(416) + 18, "k" + sub("lin", s, "label2") + " = A₀E" + sub("lin", s, "label2")
                   + "/L₀ = 416 N/mm", "label2", I["primary"]))
    aria = ("Problem D2 plot, two panels on one elongation axis from 0 to 15 millimetres, for the Achilles values A0 = 80 "
            "square millimetres, L0 = 250 millimetres, E lin = 1.3 gigapascals. Top: force F(x), a parabolic toe up to "
            "1.56 kilonewtons at x star = 7.5 millimetres, then a straight line. Bottom: the tangent stiffness k = dF/dx "
            "rises linearly from 0 through the toe and is constant at k lin = 416 newtons per millimetre beyond x star.")
    j = list(range(0, len(x), 3))
    hv = [(Pf.box, hov(Pf, x[j] * 1e3, [F[j]], lambda i: f"x = {x[j][i] * 1e3:.1f} mm, F = {F[j][i]:.2f} kN")),
          (Pk.box, hov(Pk, x[j] * 1e3, [k[j]], lambda i: f"x = {x[j][i] * 1e3:.1f} mm, k = {k[j][i]:.0f} N/mm"))]
    return svg(VB, aria, s, "".join(o), (hv,))


# ---------------------------------------------------------------- #43 D3: triangle energy and the toe's third
def fig43():
    VB = (0, 0, W, 268)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 46, 388, 210), (0, 8), (0, 3.5))
    x = np.linspace(0, X_S, 151)
    Fl, Ft = K_LIN * x / 1e3, force(x) / 1e3
    U_l, U_t = 0.5 * K_LIN * X_S**2, np.trapezoid(force(x), x)
    assert (round(U_l, 1), round(U_t, 2), round(U_l / U_t, 3)) == (11.7, 3.90, 3.0), (U_l, U_t)
    xm = x * 1e3
    o = [P.axes([(0, "0"), (2, "2"), (4, "4"), (6, "6"), (7.5, "x*")], [(0, "0"), (1, "1"), (2, "2"), (3, "3")],
                "elongation x (mm)", "force F (kN)", grid=(1, 2, 3))]
    o.append(poly(P, [0, 7.5, 7.5], [0, Fl[-1], 0], SER[1], 0.14))
    o.append(poly(P, list(xm[::5]) + [7.5, 7.5], list(Ft[::5]) + [Ft[-1], 0], SER[0], 0.22))
    o.append(dashv(P, 7.5, Fl[-1]))
    o.append(P.curve(xm, Fl, SER[1], multi=True))
    o.append(P.curve(xm, Ft, SER[0], multi=True))
    o.append(legend(s, 58, 20, [(SER[1], "linear F = k" + sub("lin", s, "label2") + "x", None),
                                (SER[0], "toe F = k" + sub("lin", s, "label2") + "x²/(2x*)", None)]))
    o.append(label(s, P.X(3.8), P.Y(1.25), "½k" + sub("lin", s, "label2") + f"x*² = {U_l:.1f} J", "label2", I["primary"]))
    o.append(label(s, P.X(4.6), P.Y(0.12), "⅙k" + sub("lin", s, "label2") + f"x*² = {U_t:.1f} J", "label2", I["primary"]))
    o.append(label(s, P.X(7.5) - 6, P.Y(Fl[-1]) - 6, f"{Fl[-1]:.2f} kN", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(7.5) - 6, P.Y(Ft[-1]) - 8, f"{Ft[-1]:.2f} kN", "label2", I["secondary"], "end"))
    aria = ("Problem D3 plot: force against elongation up to the toe end x star = 7.5 millimetres for k lin = 416 newtons "
            "per millimetre. A linear spring F = k lin x reaches 3.12 kilonewtons and stores the triangle area one half "
            "k lin x star squared = 11.7 joules. The toe curve reaches 1.56 kilonewtons and stores one sixth k lin x star "
            "squared = 3.9 joules, one third of the triangle.")
    hv = hov(P, xm[::2], [Fl[::2], Ft[::2]], lambda i: f"x = {xm[::2][i]:.2f} mm: linear {Fl[::2][i]:.2f} kN, toe {Ft[::2][i]:.2f} kN")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #44 D4: stored, returned and lost energy in one loop
def fig44():
    VB = (0, 0, W, 268)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 46, 388, 210), (0, 1), (-3, 15))
    e, sg, R = k8_loop(1.80)                     # section 7's illustrative SLS, E_inst = 1.8 E_R (line 596)
    assert round(R, 3) == 0.529, R
    ep, sp = e * 100, sg / 1e6
    n = len(e) // 2
    up_e, up_s = ep[:n + 1], sp[:n + 1]
    dn_e, dn_s = ep[n:], sp[n:]
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1)], [(0, "0"), (5, "5"), (10, "10"), (15, "15")],
                "strain ε (%)", "stress σ (MPa)", grid=(5, 10, 15))]
    o.append(H.line(s, P.x0, P.Y(0), P.x1, P.Y(0), I["rule"], "leader"))
    o.append(poly(P, list(dn_e[::20]) + [0, 1], list(dn_s[::20]) + [0, 0], SER[1], 0.16))
    o.append(poly(P, ep[::20], sp[::20], SER[0], 0.28))
    o.append(P.curve(dn_e, dn_s, SER[1], multi=True))
    o.append(P.curve(up_e, up_s, SER[0], multi=True))
    o.append(legend(s, 58, 20, [(SER[0], "loading: work in = U" + sub("stored", s, "label2"), None),
                                (SER[1], "unloading", None)]))
    o.append(label(s, P.X(0.36), P.Y(9.0), "loading", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.99), P.Y(2.0), "unloading", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.55), P.Y(0.6), "returned U" + sub("ret", s, "label2"), "label2", I["primary"], "middle"))
    o.append(H.line(s, P.X(0.86), P.Y(6.4), P.X(0.8), P.Y(10.4), I["secondary"], "leader"))
    o.append(label(s, P.X(0.99), P.Y(5.0), "loop W" + sub("d", s, "label2") + " = heat", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.03), P.Y(13.2), f"R = 1 − W{sub('d', s, 'label2')}/U{sub('stored', s, 'label2')} = {R:.3f}",
                   "label2", I["primary"]))
    o.append(label(s, P.X(0.03), P.Y(13.2) + 15, "SLS with E" + sub("inst", s, "label2") + " = 1.8 E" + sub("R", s, "label2")
                   + ", 2.6 Hz", "label2", I["secondary"]))
    aria = ("Problem D4 plot: one tension-only cycle to 1 percent strain at 2.6 hertz through the illustrative standard "
            "linear solid of section 7, instantaneous modulus 1.8 times the relaxed one; stress against strain. "
            "The loading branch lies above the unloading branch. The area under the unloading branch, shaded light, is the "
            "energy returned; the enclosed loop, shaded darker, is the energy W d lost as heat; together they are the "
            "work put in on loading. Resilience R = 1 minus W d over U stored = 0.529.")
    idx = list(range(0, n + 1, 25))
    hv = [[round(P.X(ep[i]), 2), [round(P.Y(sp[i]), 2), round(P.Y(sp[-1 - i]), 2)],
           f"ε = {ep[i]:.2f}%: loading {sp[i]:.1f} MPa, unloading {sp[-1 - i]:.1f} MPa"] for i in idx]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #46 D6 and #47 D7: Maxwell and Kelvin-Voigt step tests
def two_panel(s, left, right, cols=(SER[0], SER[1])):
    """Side-by-side normalised step-response panels; left/right = (title, ytitle, yr, yt, t, y, ref, notes, tip).
    cols: creep (strain under held stress) red, relaxation (stress under held strain) blue, as Fig. 10 and #17."""
    Ps = [Plot(s, (58, 46, 210, 206), (-0.5, 5), left[2]), Plot(s, (248, 46, 388, 206), (-0.5, 5), right[2])]
    o, panels = [], []
    for k, (P, (title, ytitle, yr, yt, t, y, ref, notes, tip)) in enumerate(zip(Ps, (left, right))):
        o.append(P.axes([(0, "0"), (1, "τ"), (3, "3τ"), (5, "5τ")], yt, "time t", "", grid=()))
        o.append(label(s, (P.x0 + P.x1) / 2, 20, title, "label2", I["primary"], "middle"))
        o.append(label(s, P.x0 + 4, P.y1 - 4, ytitle, "label2", I["secondary"]))
        if ref is not None:
            o.append(H.line(s, P.x0, P.Y(ref), P.x1, P.Y(ref), O["dim"], "ref", H.DASH_REF))
        o.append(P.curve(t, y, cols[k]))
        for kind, a, b, txt, anchor in notes:
            if kind == "dot":
                o.append(P.dot(a, b, cols[k]))
            else:
                o.append(label(s, P.X(a), P.Y(b), txt, "label2", I["primary"] if kind == "t" else I["secondary"], anchor))
        j = list(range(0, len(t), 2))
        panels.append((P.box, hov(P, t[j], [y[j]], lambda i, t=t, y=y, j=j, tip=tip: tip(t[j][i], y[j][i]))))
    return "".join(o), panels


def fig46():
    t = np.linspace(-0.5, 5, 221)
    G = np.where(t >= 0, np.exp(-np.clip(t, 0, None)), 0.0)
    cr = np.where(t >= 0, 1 + np.clip(t, 0, None), 0.0)
    assert round(math.exp(-1), 3) == 0.368
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    SM = sub("M", s, "label2")
    body, panels = two_panel(
        s,
        ("relaxation, step strain", "G/E" + SM, (0, 1.1),
         [(0, "0"), (0.368, "0.37"), (1, "1")], t, G, None,
         [("dot", 1, 0.368, "", ""), ("t", 1.25, 0.47, "e⁻¹ at t = τ", "start"),
          ("t", 4.9, 0.17, "→ 0: full", "end"), ("t", 4.9, 0.17 - 0.09, "relaxation", "end")],
         lambda a, b: f"t = {a:.2f} τ, G/EM = {b:.3f}"),
        ("creep, step stress", "εE" + SM + "/σ₀", (0, 6.6),
         [(0, "0"), (1, "1"), (3, "3"), (6, "6")], t, cr, None,
         [("t", 4.9, 2.5, "slope σ₀/η:", "end"), ("t", 4.9, 1.85, "grows without", "end"),
          ("t", 4.9, 1.2, "bound", "end")],
         lambda a, b: f"t = {a:.2f} τ, ε EM/σ0 = {b:.2f}"), cols=(SER[1], SER[0]))
    aria = ("Problem D6 plot, the Maxwell model, time in units of tau = eta over E M. Left, step strain: the relaxation "
            "modulus G over E M jumps to 1 and decays as e to the minus t over tau, to 0.37 at t = tau and on to zero, "
            "full relaxation. Right, step stress: the strain jumps to the elastic value and then grows as a straight "
            "line of slope sigma 0 over eta, without bound.")
    return svg(VB, aria, s, body, (panels,))


def fig47():
    t = np.linspace(-0.5, 5, 221)
    J = np.where(t >= 0, 1 - np.exp(-np.clip(t, 0, None)), 0.0)
    sg = np.where(t >= 0, 1.0, 0.0)
    assert round(1 - math.exp(-1), 3) == 0.632
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    SK = sub("K", s, "label2")
    body, panels = two_panel(
        s,
        ("creep, step stress", "J·E" + SK, (0, 1.25),
         [(0, "0"), (0.632, "0.63"), (1, "1")], t, J, 1.0,
         [("dot", 1, 0.632, "", ""), ("t", 1.25, 0.5, "1 − e⁻¹ at t = τ", "start"),
          ("t", 4.9, 1.06, "bound 1/E" + SK, "end")],
         lambda a, b: f"t = {a:.2f} τ, J EK = {b:.3f}"),
        ("step strain", "σ/(E" + SK + "ε₀)", (0, 1.25),
         [(0, "0"), (1, "1")], t, sg, None,
         [("t", 4.9, 0.78, "σ = E" + SK + "ε₀ held:", "end"),
          ("t", 4.9, 0.66, "no relaxation", "end")],
         lambda a, b: f"t = {a:.2f} τ, σ/(EK ε0) = {b:.0f}"))
    aria = ("Problem D7 plot, the Kelvin-Voigt model, time in units of tau = eta over E K. Left, step stress: the creep "
            "compliance times E K rises from 0 as 1 minus e to the minus t over tau, 0.63 at t = tau, toward the dashed "
            "bound 1, bounded creep. Right, step strain: the stress is E K epsilon 0 and stays constant, no relaxation.")
    return svg(VB, aria, s, body, (panels,))


# ---------------------------------------------------------------- #48 D8: the SLS loss peak (K7 constants)
def fig48():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    TE = 0.100                                   # K7: tau_sigma = 0.05 s, tau_eps = 0.10 s (line 1113)
    lw = np.linspace(-1, 3, 401)
    Es = estar(10**lw, TE)
    td = Es.imag / Es.real
    wpk = 1 / math.sqrt(TS * TE)
    tdpk = (TE - TS) / (2 * math.sqrt(TS * TE))
    assert (round(wpk, 2), round(tdpk, 3)) == (14.14, 0.354), (wpk, tdpk)
    assert abs(td.max() - tdpk) < 1e-4
    P = Plot(s, (58, 30, 378, 202), (-1, 3), (0, 0.4))
    o = [P.axes([(v, t) for v, t in ((-1, "0.1"), (0, "1"), (1, "10"), (2, "100"), (3, "1000"))],
                [(0, "0"), (0.1, "0.1"), (0.2, "0.2"), (0.3, "0.3")], "angular frequency ω (rad/s, log)", "loss tangent tan δ",
                grid=(0.1, 0.2, 0.3))]
    o.append(dashv(P, math.log10(wpk), tdpk))
    o.append(P.curve(lw, td, SER[0]))
    o.append(P.dot(math.log10(wpk), tdpk, SER[0]))
    o.append(label(s, P.X(math.log10(wpk)) + 8, P.Y(tdpk) - 4, f"peak tan δ = {tdpk:.3f}", "label2", I["primary"]))
    o.append(label(s, P.X(3), P.Y(0.30), "ω* = 1/√(τ" + sub("σ", s, "label2") + "τ" + sub("ε", s, "label2") + ")",
                   "label2", I["secondary"], "end"))
    o.append(label(s, P.X(3), P.Y(0.30) + 15, f"= {wpk:.1f} rad/s", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(-0.95), P.Y(0.30), "τ" + sub("σ", s, "label2") + " = 0.05 s, τ" + sub("ε", s, "label2") + " = 0.10 s",
                   "label2", I["secondary"]))
    aria = ("Problem D8 plot: the standard-linear-solid loss tangent against angular frequency on a log axis from 0.1 to "
            "1000 radians per second, for tau sigma = 0.05 seconds and tau epsilon = 0.10 seconds (the K7 values). tan "
            "delta is near zero at both ends and peaks at 0.354 at omega = 1 over the square root of tau sigma tau "
            "epsilon = 14.1 radians per second, marked by a dashed line.")
    hv = hov(P, lw[::3], [td[::3]], lambda i: f"ω = {10**lw[::3][i]:.3g} rad/s, tan δ = {td[::3][i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #49 D9: stress leads strain by delta; the loop area
def fig49():
    VB = (0, 0, W, 264)
    s = H.Scale(W, VB[3], display_w=400)
    DL = math.pi / 6                                 # illustrative loss angle, 30 degrees (problem is symbolic)
    Pt = Plot(s, (58, 50, 248, 196), (0, 2 * math.pi), (-1.25, 1.25))
    Pe = Plot(s, (284, 64, 388, 182), (-1.25, 1.25), (-1.25, 1.25))
    ph = np.linspace(0, 2 * math.pi, 181)
    ee, ss = np.sin(ph), np.sin(ph + DL)
    area = np.trapezoid(ss * np.cos(ph), ph)        # one cycle: integral of sigma d eps
    assert abs(area - math.pi * math.sin(DL)) < 1e-3
    o = [Pt.axes([(0, "0"), (math.pi, "π"), (2 * math.pi, "2π")], [(-1, "−1"), (0, "0"), (1, "1")], "phase ωt", "",
                 grid=())]
    o.append(H.line(s, Pt.x0, Pt.Y(0), Pt.x1, Pt.Y(0), I["rule"], "leader"))
    o.append(Pt.curve(ph, ee, SER[1], multi=True))
    o.append(Pt.curve(ph, ss, SER[0], multi=True))
    xa, xb, yb = Pt.X(math.pi / 2 - DL), Pt.X(math.pi / 2), Pt.Y(1.13)
    o.append(H.line(s, xa, yb, xb, yb, O["geometry"], "geom"))
    o.append(H.line(s, xa, yb - 4, xa, yb + 4, O["geometry"], "geom"))
    o.append(H.line(s, xb, yb - 4, xb, yb + 4, O["geometry"], "geom"))
    o.append(label(s, (xa + xb) / 2, yb - 6, "δ", "label", I["primary"], "middle", 'font-style="italic"'))
    o.append(legend(s, 58, 20, [(SER[1], "strain ε/ε₀", None), (SER[0], "stress σ/σ₀, leads by δ", None)]))
    o.append(label(s, xa - 9, Pt.Y(1.02), "σ", "label", I["primary"], "end", 'font-style="italic"'))
    o.append(label(s, xb + 9, Pt.Y(1.02), "ε", "label", I["primary"], "start", 'font-style="italic"'))
    th = np.linspace(0, 2 * math.pi, 121)
    ex, sy = np.sin(th), np.sin(th + DL)
    o.append(H.line(s, Pe.x0, Pe.Y(0), Pe.x1, Pe.Y(0), I["axis"], "axis"))
    o.append(H.line(s, Pe.X(0), Pe.y0, Pe.X(0), Pe.y1, I["axis"], "axis"))
    o.append(poly(Pe, ex, sy, SER[0], 0.18))
    o.append(Pe.curve(ex, sy, SER[0], multi=True))
    o.append(label(s, Pe.x1, Pe.Y(0) + 15, "ε/ε₀", "label2", I["secondary"], "end"))
    o.append(label(s, Pe.X(0) + 4, Pe.y1 - 4, "σ/σ₀", "label2", I["secondary"]))
    o.append(label(s, (Pe.x0 + Pe.x1) / 2, Pe.y0 + 24, "loop area W" + sub("d", s, "label2"), "label2", I["primary"], "middle"))
    o.append(label(s, (Pe.x0 + Pe.x1) / 2, Pe.y0 + 40, "= πσ₀ε₀ sin δ", "label2", I["primary"], "middle"))
    o.append(label(s, Pt.x0, Pt.y0 + 60, "δ = 30° here, for visibility; tendon tan δ ≲ 0.1 (δ ≲ 6°)", "label2",
                   I["secondary"]))
    aria = ("Problem D9 plot. Left: strain epsilon over epsilon 0 = sin omega t and stress sigma over sigma 0 = sin of "
            "omega t plus delta over one cycle, with delta = 30 degrees for visibility; the stress peaks a phase delta "
            "before the strain. Right: stress against strain traces an ellipse whose area, the energy dissipated per "
            "cycle, is pi sigma 0 epsilon 0 sin delta.")
    j = list(range(0, len(ph), 2))
    hv = [(Pt.box, hov(Pt, ph[j], [ee[j], ss[j]], lambda i: f"ωt = {math.degrees(ph[j][i]):.0f}°: ε/ε0 = {ee[j][i]:.2f}, "
                                                          f"σ/σ0 = {ss[j][i]:.2f}"))]
    k = np.argsort(ex[:-1])
    hv.append((Pe.box, [[round(Pe.X(ex[i]), 2), round(Pe.Y(sy[i]), 2), f"ε/ε0 = {ex[i]:.2f}, σ/σ0 = {sy[i]:.2f}"] for i in k]))
    return svg(VB, aria, s, "".join(o), (hv,))


FIGS = {
    31: ("J-shaped stress-strain curve", fig31),
    33: ("tangent vs secant stiffness", fig33),
    34: ("tendon vs ligament hysteresis loops", fig34),
    37: ("creep versus stress relaxation", fig37),
    39: ("resilience spectrum from spring to damper", fig39),
    41: ("recruitment producing the parabolic toe", fig41),
    42: ("force law and tangent stiffness", fig42),
    43: ("triangular energy under the linear force line", fig43),
    44: ("hysteresis loop, resilience", fig44),
    46: ("Maxwell relaxation to zero", fig46),
    47: ("Kelvin-Voigt bounded creep", fig47),
    48: ("loss tangent peak versus frequency", fig48),
    49: ("phase-shifted stress and strain", fig49),
}
