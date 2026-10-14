"""Module 14 problem figures, group `prob_b` (svg idx 35 D5, 36 D6, 37 D7, 39 D9, 40 D10, 41 K1, 43 K2, 45 K3, 47 K4,
49 K5, 51 K6, 53 K7, 55 K8, 57 K9, 59 K10, 61 K11). Problem figures: 400 units wide, rendered 400 px (1 unit = 1 px).

Every plotted number is computed here from the module's formulas, constants and code:
  recoverable fraction exp(-w0 dt), w0 = 3.1 rad/s                      (Prop. 5.1, text l.154-156, D5 solution l.442)
  J_eff = m w0 (b - c sigma) exp(-w0 dt), m = 70 kg                     (Prop. 6.1, l.215; Lab D l.339)
  dC/dt = k_ad (Sigma - Sigma0)                                         (Prop. 7.1, l.233)
  a* = a0 + (1/r)(1 - D/tau_p), a0 = 40, r = 0.01, D = 100/110/150      (l.458, K1 l.469, K8 l.648)
  F = sqrt(2 g h_f) sqrt(m_eff k), m_eff = 35, k = 40 kN/m, S0 = 7 kN   (Prop. 3.2 l.144; K2/K7 code l.483, l.628)
  K3 code l.512-531 (kappa = beta = 0.010, p0 = 3, h0 = 2, n_c = 0.7, Euler dt 0.5, stop at h <= 0.30)
  K5 code l.578-596 (k_ad = 0.03125, rho_crit = 0.7915); K6 l.607-617; K9 l.665-673; K10 l.688-705; K11 l.720-762
"""
import math

import numpy as np

import house as H
from m05.plots_prob import Plot, W, hov, label, legend, svg, text_w

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"
BOX = "#f7f4ef"

# ---------------------------------------------------------------- module constants
W0, M_KG = 3.1, 70.0
A0, RATE = 40.0, 0.01
TASKS = (("floor", 150.0, SER[0]), ("chair", 110.0, SER[1]), ("stair", 100.0, SER[2]))   # D in N m (l.851)
TAU_TYP = 175.0
G, M_EFF, K_FALL, S0 = 9.81, 35.0, 40e3, 7000.0
P0, H0, N_C, KAP, BET = 3.0, 2.0, 0.7, 0.010, 0.010
YOUNG = dict(b=0.10, dt=0.12, cs=0.010)
AGED = dict(b=0.05, dt=0.20, cs=0.020)


def sub(t, s, size="label"):
    return H.sub(t, s, size)


def sup(t, s, size="label"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def defs(p, s):
    return f"<defs>{H.markers(p, s)}</defs>"


def dashed(s, x1, y1, x2, y2, col=None):
    return H.line(s, x1, y1, x2, y2, col or O["dim"], "ref", H.DASH_REF)


def dot(P, x, y, col, hollow=False):
    s = P.s
    r = s(H.PX["dot"])
    if hollow:
        return (f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{r:.2f}" fill="#fff" stroke="{col}" '
                f'stroke-width="{s(1.8):.2f}"/>')
    return P.dot(x, y, col)


def band(P, y_top, y_bot, col, op):
    return (f'<rect x="{P.x0:.2f}" y="{P.Y(y_top):.2f}" width="{P.x1 - P.x0:.2f}" height="{P.Y(y_bot) - P.Y(y_top):.2f}" '
            f'fill="{col}" opacity="{op}"/>')


def jeff(b, dt, cs):
    return M_KG * W0 * (b - cs) * math.exp(-W0 * dt)


def astar(tp, D):
    return A0 + (1 - D / tp) / RATE


def force(hf, k=K_FALL):
    return math.sqrt(2 * G * hf) * math.sqrt(M_EFF * k)


# ================================================================ svg #35  D5: delay erosion
def fig35():
    VB = (0, 0, W, 476)
    s = H.Scale(W, VB[3], display_w=400)
    A = Plot(s, (58, 44, 382, 196), (0, 0.30), (0, 1.15))
    B = Plot(s, (58, 296, 382, 428), (0, 0.30), (0, 1.05))
    young, aged = 0.12, 0.20
    o = []
    # panel a: the extrapolated COM xi(t) = xi0 exp(w0 t); the response is issued at dt, success iff xi(dt) <= xi_c
    o.append(label(s, 58, 18, "a  Largest push that is still recoverable", "label", I["primary"]))
    o.append(A.axes([(v, f"{v:.2f}") for v in (0, 0.1, 0.2, 0.3)], [(0, "0"), (0.5, "0.5"), (1.0, "1")],
                    "response time Δt (s)", "extrapolated COM ξ / ξc", grid=()))
    o.append(dashed(s, A.x0, A.Y(1), A.x1, A.Y(1)))
    o.append(label(s, A.x0 + 6, A.Y(1) - 9, "ξc: edge of the base", "label2", I["secondary"]))
    t = np.arange(0, 0.2001, 0.005)
    series = []
    for dt, col in ((young, SER[1]), (aged, SER[0])):
        x0 = math.exp(-W0 * dt)
        tt = t[t <= dt + 1e-9]
        xi = x0 * np.exp(W0 * tt)
        series.append((dt, x0, tt, xi, col))
        o.append(A.curve(tt, xi, col))
        o.append(dot(A, dt, 1.0, col))
        o.append(dashed(s, A.X(dt), A.Y(1) + s(7), A.X(dt), A.y0))
        o.append(dot(A, 0, x0, col))
    o.append(label(s, A.X(young) + 6, A.Y(0.12), f"Δt = {young:.2f} s", "label2", I["primary"]))
    o.append(label(s, A.X(aged) + 6, A.Y(0.12), f"Δt = {aged:.2f} s", "label2", I["primary"]))
    o.append(legend(s, 58, 38, [(SER[1], f"starts at ξ0 = {series[0][1]:.2f} ξc", None),
                                (SER[0], f"starts at ξ0 = {series[1][1]:.2f} ξc", None)], gap=10))
    # panel b: the factor
    o.append(label(s, 58, 270, "b  The factor exp(−ω" + sub("0", s) + "Δt)", "label", I["primary"]))
    o.append(B.axes([(v, f"{v:.2f}") for v in (0, 0.1, 0.2, 0.3)], [(0, "0"), (0.5, "0.5"), (1.0, "1")],
                    "reaction delay Δt (s)", "recoverable factor", grid=(0.5, 1.0)))
    dt = np.arange(0, 0.3001, 0.005)
    f = np.exp(-W0 * dt)
    o.append(B.curve(dt, f, I["axis"]))
    for d, col in ((young, SER[1]), (aged, SER[0])):
        o.append(dot(B, d, math.exp(-W0 * d), col))
    f1, f2 = math.exp(-W0 * young), math.exp(-W0 * aged)
    o.append(label(s, B.X(young) + 9, B.Y(f1) - 10, f"{f1:.2f}", "label2", I["primary"]))
    o.append(label(s, B.X(aged) + 9, B.Y(f2) - 10, f"{f2:.2f}", "label2", I["primary"]))
    o.append(label(s, B.x1 - 6, B.Y(0.22), f"0.12 → 0.20 s: × {f2 / f1:.2f} (−{100 * (1 - f2 / f1):.0f} %)", "label2", I["primary"], "end"))
    o.append(label(s, B.x1 - 6, B.Y(0.07), f"every +0.10 s: × {math.exp(-W0 * 0.1):.2f}", "label2", I["secondary"], "end"))
    hva = hov(A, t, [series[1][3]],
              lambda i: f"t = {t[i]:.3f} s: ξ/ξc = {series[1][3][i]:.2f} (ξ0 = 0.54 ξc)"
                        + (f", {series[0][3][i]:.2f} (ξ0 = 0.69 ξc)" if i < len(series[0][3]) else ""))
    hvb = hov(B, dt, [f], lambda i: f"Δt = {dt[i]:.3f} s: factor {f[i]:.2f}")
    aria = ("Problem D5 derivation. Top: the extrapolated centre of mass, as a fraction of its limit xi c at the edge of the base, "
            "grows as xi 0 times e to the omega 0 t. A response issued at delay delta t succeeds only if the push is small enough that "
            "the curve has not passed 1 by then, so the largest recoverable push is xi 0 = e to the minus omega 0 delta t: 0.69 of xi c "
            "for a 0.12 second delay and 0.54 for 0.20 seconds. Bottom: that factor against delay with omega 0 = 3.1 per second, "
            "falling from 1 to 0.39 at 0.30 seconds, a drop of 22 percent between the two marked delays.")
    return svg(VB, aria, s, "".join(o), ([(A.box, hva), (B.box, hvb)],))


# ================================================================ svg #36  D6: assembling J_eff
def fig36():
    VB = (0, 0, W, 214)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f36_"
    cols = [(58, 72), (146, 72), (234, 72), (322, 72)]
    heads = [("margin", "mω" + sub("0", s, "label2") + "b", SER[0]),
             ("noise", "1 − cσ/b", SER[2]),
             ("delay", "exp(−ω" + sub("0", s, "label2") + "Δt)", SER[1]),
             ("result", "J" + sub("eff", s, "label2"), I["primary"])]
    o = [defs(p, s)]
    by, bh = 46, 38
    for (x, w), (nm, fm, col) in zip(cols, heads):
        o.append(f'<rect x="{x}" y="{by}" width="{w}" height="{bh}" rx="6" fill="{BOX}" stroke="{I["rule"]}" stroke-width="{s(1):.2f}"/>')
        o.append(f'<rect x="{x}" y="{by}" width="{s(5):.2f}" height="{bh}" rx="2" fill="{col}"/>')
        o.append(H.label(s, x + w / 2 + 2, by + bh / 2 + 5, fm, "label2", I["primary"], "middle"))
        o.append(H.label(s, x + w / 2, by - 8, nm, "label2", I["secondary"], "middle"))
    for xm, ch in ((cols[0][0] + 72 + 8, "×"), (cols[1][0] + 72 + 8, "×"), (cols[2][0] + 72 + 8, "=")):
        o.append(H.label(s, xm, by + bh / 2 + 6, ch, "label", I["primary"], "middle"))
    rows = []
    for nm, q, y in (("40 yr", YOUNG, 118), ("85 yr", AGED, 148)):
        a = M_KG * W0 * q["b"]
        bb = 1 - q["cs"] / q["b"]
        d = math.exp(-W0 * q["dt"])
        j = a * bb * d
        assert abs(j - jeff(q["b"], q["dt"], q["cs"])) < 1e-9
        rows.append(j)
        o.append(H.label(s, 4, y + 5, nm, "label2", I["primary"]))
        for (x, w), v in zip(cols, (f"{a:.2f} N s", f"{bb:.2f}", f"{d:.2f}", f"{j:.2f} N s")):
            o.append(H.label(s, x + w / 2, y + 5, v, "label2", I["primary"], "middle"))
    assert f"{rows[0]:.2f}" == "13.46" and f"{rows[1]:.2f}" == "3.50"
    o.append(H.line(s, 4, 98, 394, 98, GRID, "leader"))
    o.append(H.label(s, 4, 184, "m = 70 kg, ω" + sub("0", s, "label2") + " = 3.1 rad/s; b 0.10 → 0.05 m, cσ 0.010 → 0.020 m,", "label2", I["secondary"]))
    o.append(H.label(s, 4, 201, "Δt 0.12 → 0.20 s. Recovery needs J ≤ J" + sub("eff", s, "label2") + ".", "label2", I["secondary"]))
    aria = ("Problem D6 diagram. J eff equals three factors multiplied: the young critical impulse m omega 0 b, the noise factor "
            "1 minus c sigma over b, and the delay factor e to the minus omega 0 delta t. At age 40 they are 21.70 newton seconds, 0.90 "
            "and 0.69, giving 13.46 newton seconds. At age 85 they are 10.85 newton seconds, 0.60 and 0.54, giving 3.50 newton seconds. "
            "Recovery needs the encountered impulse J to be no greater than J eff.")
    return svg(VB, aria, s, "".join(o))


# ================================================================ svg #37  D7: the mechanostat
def fig37():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f37_"
    P = Plot(s, (58, 40, 382, 240), (0, 2), (-1.1, 1.1))
    x = np.arange(0, 2.0001, 0.02)
    y = x - 1
    o = [defs(p, s)]
    o.append(f'<rect x="{P.x0:.2f}" y="{P.Y(0):.2f}" width="{P.X(1) - P.x0:.2f}" height="{P.Y(-1.1) - P.Y(0):.2f}" fill="{O["force"]}" fill-opacity="0.10"/>')
    o.append(f'<rect x="{P.X(1):.2f}" y="{P.Y(1.1):.2f}" width="{P.x1 - P.X(1):.2f}" height="{P.Y(0) - P.Y(1.1):.2f}" fill="{O["geometry"]}" fill-opacity="0.10"/>')
    o.append(P.axes([(0, "0"), (1, "1"), (2, "2")], [(-1, "−1"), (0, "0"), (1, "1")], "stimulus Σ / Σ" + sub("0", s),
                    "dC/dt  (units of k" + sub("ad", s) + "Σ" + sub("0", s) + ")"))
    o.append(dashed(s, P.x0, P.Y(0), P.x1, P.Y(0)))
    o.append(P.curve(x, y, I["axis"]))
    o.append(dot(P, 1, 0, O["flag"]))
    o.append(label(s, P.X(1) + 8, P.Y(0) + 38, "steady at Σ = Σ" + sub("0", s, "label2"), "label2", I["primary"]))
    o.append(label(s, P.x0 + 8, P.Y(0.82), "disuse: resorbs", "label", I["primary"]))
    o.append(label(s, P.x0 + 8, P.Y(0.82) + 17, "(Σ < Σ" + sub("0", s, "label2") + ", dC/dt < 0)", "label2", I["secondary"]))
    o.append(label(s, P.x1 - 8, P.Y(-0.80), "training: builds", "label", I["primary"], "end"))
    o.append(label(s, P.x1 - 8, P.Y(-0.80) + 17, "(Σ > Σ" + sub("0", s, "label2") + ", dC/dt > 0)", "label2", I["secondary"], "end"))
    # overload dimension at Sigma = Sigma0 + Delta
    xd = 1.5
    o.append(H.arrow(s, p, P.X(1), P.Y(0) + s(0), P.X(xd), P.Y(0), "geometry", both=True))
    o.append(dashed(s, P.X(xd), P.Y(0) - s(4), P.X(xd), P.Y(xd - 1) + s(6)))
    o.append(H.arrow(s, p, P.X(xd) + s(10), P.Y(0), P.X(xd) + s(10), P.Y(xd - 1), "force", both=True))
    o.append(label(s, (P.X(1) + P.X(xd)) / 2, P.Y(0) + 18, "Δ", "label", I["primary"], "middle"))
    o.append(label(s, P.X(xd) + 20, P.Y(0.25) + 5, "k" + sub("ad", s, "label2") + "Δ", "label2", I["primary"]))
    hv = hov(P, x, [y], lambda i: f"Σ/Σ0 = {x[i]:.2f}: dC/dt = {y[i]:+.2f} kad Σ0")
    aria = ("Problem D7 plot. The mechanostat rate law dC over dt equals k ad times the stimulus minus its setpoint, drawn as a straight "
            "line against the stimulus as a fraction of the setpoint, from minus 1 at zero stimulus to plus 1 at twice the setpoint. "
            "The line crosses zero at the setpoint, where the capacity is steady. Left of it the tissue resorbs (red tint) and right of "
            "it the tissue builds (blue tint). Under an overload delta above the setpoint, double-headed arrows mark the stimulus "
            "excess delta and the building rate k ad delta, which recovers a deficit delta C in time delta C over k ad delta.")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #39  D9: demand shifts the age
def fig39():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f39_"
    P = Plot(s, (58, 40, 382, 240), (60, 160), (40, 110))
    D = np.arange(60, 160.01, 1.0)
    a = A0 + (1 - D / TAU_TYP) / RATE
    slope = -1 / (RATE * TAU_TYP)
    assert abs(slope + 0.5714) < 1e-3
    o = [defs(p, s)]
    o.append(P.axes([(v, f"{v}") for v in (60, 80, 100, 120, 140, 160)], [(v, f"{v}") for v in (40, 60, 80, 100)],
                    "task demand D (N m)", "failure age a* (yr)", grid=(60, 80, 100)))
    o.append(P.curve(D, a, SER[0]))
    pts = []
    for nm, d, side in (("floor", 150.0, "r"), ("chair", 110.0, "r"), ("stair", 100.0, "u")):
        ag = astar(TAU_TYP, d)
        pts.append((nm, d, ag))
        o.append(dot(P, d, ag, SER[0]))
    o.append(label(s, P.X(150) - 9, P.Y(astar(TAU_TYP, 150)) + 22, f"floor rise: {astar(TAU_TYP, 150):.1f} yr", "label2", I["primary"], "end"))
    o.append(label(s, P.X(110) + 10, P.Y(astar(TAU_TYP, 110)) - 12, f"chair: {astar(TAU_TYP, 110):.1f} yr", "label2", I["primary"]))
    o.append(label(s, P.X(100) - 9, P.Y(astar(TAU_TYP, 100)) + 22, f"stair: {astar(TAU_TYP, 100):.1f} yr", "label2", I["primary"], "end"))
    # a 10 N m cut in demand (chair -> stair) buys 5.7 yr
    xa = P.X(105)
    o.append(label(s, P.x1 - 6, P.Y(104), "∂a*/∂D = −1/(r τ" + sub("p", s, "label2") + ") = −0.57 yr per N m", "label2", I["primary"], "end"))
    o.append(label(s, P.x1 - 6, P.Y(97), "(r = 0.01 per yr, τ" + sub("p", s, "label2") + " = 175 N m)", "label2", I["secondary"], "end"))
    o.append(label(s, P.x1 - 6, P.Y(90), "10 N m less demand: +5.7 yr", "label2", I["primary"], "end"))
    hv = hov(P, D, [a], lambda i: f"D = {D[i]:.0f} N m: failure age {a[i]:.1f} yr")
    aria = ("Problem D9 plot. The failure age a star = 40 + 100 (1 - D / 175) years against the task demand D from 60 to 160 newton metres, "
            "for peak strength 175 newton metres. It is a straight line falling by 0.57 years for each newton metre of demand. Marked "
            "points: stair, D = 100, fails at 82.9 years; chair, D = 110, at 77.1; deep floor rise, D = 150, at 54.3. Cutting the demand "
            "by 10 newton metres, as raising a chair does, adds 5.7 years.")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #40  D10: impact scaling
def fig40():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f40_"
    P = Plot(s, (58, 40, 382, 240), (0.2, 1.5), (0, 7000))
    h = np.arange(0.2, 1.5001, 0.01)
    F40 = np.array([force(v) for v in h])
    F20 = np.array([force(v, K_FALL / 2) for v in h])
    o = [defs(p, s)]
    o.append(P.axes([(0.5, "0.5"), (0.7, "0.7"), (1.0, "1.0"), (1.4, "1.4")], [(0, "0"), (2000, "2000"), (4000, "4000"), (6000, "6000")],
                    "fall height h" + sub("f", s) + " (m)", "peak impact force F (N)", grid=(2000, 4000, 6000)))
    o.append(P.curve(h, F40, SER[0]))
    o.append(P.curve(h, F20, SER[1], dash=(7, 4)))
    o.append(legend(s, 58, 18, [(SER[0], "k = 40 kN/m (bare floor)", None), (SER[1], "k = 20 kN/m (half)", (7, 4))], gap=10))
    for hh in (0.7, 1.4):
        o.append(dashed(s, P.X(hh), P.Y(force(hh)) + s(7), P.X(hh), P.y0))
    for hh, k, col in ((0.7, K_FALL, SER[0]), (1.4, K_FALL, SER[0]), (0.7, K_FALL / 2, SER[1]), (1.4, K_FALL / 2, SER[1])):
        o.append(dot(P, hh, force(hh, k), col))
    f07, f14, p07, p14 = force(0.7), force(1.4), force(0.7, K_FALL / 2), force(1.4, K_FALL / 2)
    assert round(f07) == 4385 and round(p07) == 3101
    o.append(label(s, P.X(0.7) - 8, P.Y(f07) - 12, f"{f07:.0f} N", "label2", I["primary"], "end"))
    o.append(label(s, P.X(1.4) - 9, P.Y(f14) - 12, f"{f14:.0f} N (× {f14 / f07:.2f})", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.7) + 9, P.Y(p07) + 22, f"{p07:.0f} N (× {p07 / f07:.2f}, −{100 * (1 - p07 / f07):.0f} %)", "label2", I["primary"]))
    o.append(label(s, P.X(1.4) - 9, P.Y(p14) + 22, f"{p14:.0f} N", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.7) + 6, P.y0 - 8, "hip, 0.70 m", "label2", I["secondary"]))
    o.append(label(s, P.X(1.4) - 6, P.y0 - 8, "chair, 1.40 m", "label2", I["secondary"], "end"))
    o.append(label(s, P.x0 + 8, P.Y(6500), "F ∝ √h" + sub("f", s, "label2") + " · √k", "label", I["primary"]))
    hv = hov(P, h, [F40, F20], lambda i: f"h = {h[i]:.2f} m: F = {F40[i]:.0f} N (k 40), {F20[i]:.0f} N (k 20)")
    aria = ("Problem D10 plot. The peak impact force F = sqrt(2 g h f) sqrt(m eff k), with m eff = 35 kilograms, against fall height "
            "from 0.2 to 1.5 metres, for landing stiffness 40 kilonewtons per metre (solid) and 20 (dashed). Both curves rise as the "
            "square root of height. At the hip height 0.70 metres the force is 4385 newtons; doubling the height to 1.40 metres, a "
            "chair, gives 6201 newtons, a factor 1.41. Halving the stiffness gives 3101 newtons at 0.70 metres, a factor 0.71, a "
            "29 percent cut, and 4385 newtons at 1.40 metres.")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #41  K1: strength to reach age 85
def fig41():
    VB = (0, 0, W, 366)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f41_"
    P = Plot(s, (58, 108, 382, 302), (100, 300), (40, 110))
    o = [defs(p, s)]
    o.append(P.axes([(v, f"{v}") for v in (100, 150, 200, 250, 300)], [(v, f"{v}") for v in (40, 60, 85, 110)],
                    "peak midlife strength τ" + sub("p", s) + " (N m)", "failure age a* (yr)", grid=(60, 110)))
    o.append(dashed(s, P.x0, P.Y(85), P.x1, P.Y(85)))
    o.append(label(s, P.x0 + 6, P.Y(85) - 8, "target age 85", "label2", I["primary"]))
    o.append(dashed(s, P.X(TAU_TYP), P.Y(110), P.X(TAU_TYP), P.y0, I["muted"]))
    tp = np.arange(100, 300.01, 1.0)
    need = {}
    hvs = []
    for nm, d, col in TASKS:
        m = tp >= d
        a = A0 + (1 - d / tp[m]) / RATE
        o.append(P.curve(tp[m], a, col))
        need[nm] = d / (1 - RATE * (85 - A0))
        o.append(dot(P, need[nm], 85, col))
        o.append(dot(P, TAU_TYP, astar(TAU_TYP, d), col, hollow=True))
        hvs.append((tp[m], a, nm, d))
    assert [round(need[n], 1) for n in ("stair", "chair", "floor")] == [181.8, 200.0, 272.7]
    assert [round(astar(TAU_TYP, d)) for _, d, _ in TASKS] == [54, 77, 83]
    for k_, (n, d, c) in enumerate(TASKS):
        y_ = 16 + 17 * k_
        o.append(H.line(s, 58, y_ - 4.5, 78, y_ - 4.5, c, "curve_multi"))
        o.append(label(s, 83, y_, f"{n}, D = {d:.0f}: needs {need[n]:.0f} N m; typical fails at {astar(TAU_TYP, d):.0f} yr", "label2", I["secondary"]))
    o.append(label(s, 58, 72, "dots on the target line: strength needed;", "label2", I["secondary"]))
    o.append(label(s, 58, 88, "hollow dots: typical τ" + sub("p", s, "label2") + " = 175 N m", "label2", I["secondary"]))
    fa = {d: np.array([max(A0, astar(t_, d)) for t_ in tp]) for _, d, _ in TASKS}
    hv = hov(P, tp, [fa[150.0], fa[110.0], fa[100.0]],
             lambda i: f"τp = {tp[i]:.0f} N m fails at: floor {fa[150.0][i]:.0f}, chair {fa[110.0][i]:.0f}, stair {fa[100.0][i]:.0f} yr")
    aria = ("Problem K1 plot. The failure age a star = 40 + 100 (1 - D / tau p) against peak midlife strength tau p from 100 to 300 newton "
            "metres, for three task demands: deep floor rise D = 150, chair D = 110 and gentle stair D = 100 newton metres. A dashed line marks "
            "the target age 85. The strength needed to reach it is D / 0.55: 181.8 for the stair, 200.0 for the chair and 272.7 for the "
            "floor rise, so the hardest task sets the requirement. A typical peak of 175 newton metres, hollow dots, fails the three tasks "
            "at 54, 77 and 83 years.")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #43  K2: critical density and the pad
def fig43():
    VB = (0, 0, W, 580)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f43_"
    A = Plot(s, (58, 72, 382, 222), (55, 100), (0, 2.6))
    lg = lambda v: math.log10(v)  # noqa: E731
    B = Plot(s, (58, 392, 382, 528), (55, 90), (lg(8), lg(100)))
    o = [defs(p, s)]
    o.append(label(s, 58, 18, "a  Fracture margin S/F", "label", I["primary"]))
    rho = np.arange(55, 100.01, 0.5)
    Fb, Fp = force(0.7), force(0.7, K_FALL / 2)
    mb, mp = S0 * (rho / 100) ** 2 / Fb, S0 * (rho / 100) ** 2 / Fp
    o.append(A.axes([(v, f"{v}") for v in (60, 70, 80, 90, 100)], [(0, "0"), (1, "1"), (2, "2")], "bone density ρ (% of young)", "margin S / F", grid=(1,)))
    o.append(dashed(s, A.x0, A.Y(1), A.x1, A.Y(1)))
    o.append(A.curve(rho, mb, SER[0]))
    o.append(A.curve(rho, mp, SER[1], dash=(7, 4)))
    o.append(legend(s, 58, 38, [(SER[0], f"bare floor, F = {Fb:.0f} N", None)]))
    o.append(legend(s, 58, 55, [(SER[1], f"hip protector (half the stiffness), F = {Fp:.0f} N", (7, 4))]))
    cb, cp = 100 * math.sqrt(Fb / S0), 100 * math.sqrt(Fp / S0)
    assert f"{cb:.1f}" == "79.1" and f"{cp:.1f}" == "66.6"
    o.append(dot(A, cb, 1, SER[0]))
    o.append(dot(A, cp, 1, SER[1]))
    o.append(label(s, A.X(cb) + 8, A.Y(1) + 22, f"fractures below {cb:.1f} %", "label2", I["primary"]))
    o.append(label(s, A.X(cp) - 8, A.Y(1) - 11, f"{cp:.1f} %", "label2", I["primary"], "end"))
    hva = hov(A, rho, [mb, mp], lambda i: f"ρ = {rho[i]:.1f} %: S/F = {mb[i]:.2f} (bare), {mp[i]:.2f} (pad)")
    # panel b: stiffest landing that still protects
    o.append(label(s, 58, 318, "b  Stiffest landing that protects the hip", "label", I["primary"]))
    r2 = np.arange(55, 90.01, 0.5)

    def kmax(rr, hf):
        return (S0 * (rr / 100) ** 2) ** 2 / (2 * M_EFF * G * hf) / 1e3
    kk = {hf: np.array([kmax(v, hf) for v in r2]) for hf in (0.5, 0.7, 0.9)}
    o.append(B.axes([(v, f"{v}") for v in (60, 70, 80, 90)], [(lg(v), f"{v}") for v in (10, 20, 40, 80)],
                    "bone density ρ (% of young)", "k" + sub("max", s) + " (kN/m, log scale)", grid=(lg(10), lg(20), lg(40), lg(80)), ytx=15))
    poly = " ".join(f"{B.X(a):.2f},{B.Y(lg(b)):.2f}" for a, b in list(zip(r2, kk[0.9])) + list(zip(r2, kk[0.5]))[::-1])
    o.append(f'<polygon points="{poly}" fill="{SER[1]}" fill-opacity="0.18" stroke="none"/>')
    o.append(B.curve(r2, [lg(v) for v in kk[0.7]], SER[1]))
    o.append(H.line(s, B.x0, B.Y(lg(40)), B.x1, B.Y(lg(40)), O["dim"], "ref", H.DASH_REF))
    o.append(label(s, B.x0 + 6, B.Y(lg(40)) - 7, "bare floor 40 kN/m", "label2", I["primary"]))
    for rr in (60, 80):
        o.append(dot(B, rr, lg(kmax(rr, 0.7)), SER[1]))
    assert [round(kmax(60, h_), 1) for h_ in (0.5, 0.7, 0.9)] == [18.5, 13.2, 10.3]
    assert [round(kmax(80, h_), 1) for h_ in (0.5, 0.7, 0.9)] == [58.5, 41.8, 32.5]
    o.append(label(s, B.X(60) + 9, B.Y(lg(kmax(60, 0.7))) + 22, f"{kmax(60, 0.7):.1f}", "label2", I["primary"]))
    o.append(label(s, B.X(80) + 9, B.Y(lg(kmax(80, 0.7))) + 22, f"{kmax(80, 0.7):.1f}", "label2", I["primary"]))
    o.append(label(s, 58, 336, "line: h" + sub("f", s, "label2") + " = 0.7 m; band: h" + sub("f", s, "label2") + " = 0.9 to 0.5 m", "label2", I["secondary"]))
    o.append(label(s, 58, 352, "band at 60 %: 10.3 to 18.5; at 80 %: 32.5 to 58.5 kN/m", "label2", I["secondary"]))
    o.append(label(s, 58, 368, "k" + sub("max", s, "label2") + " ∝ ρ⁴ and ∝ 1/h" + sub("f", s, "label2"), "label2", I["secondary"]))
    hvb = [[round(B.X(r2[i]), 2), round(B.Y(lg(kk[0.7][i])), 2),
            f"ρ = {r2[i]:.1f} %: kmax = {kk[0.7][i]:.1f} kN/m (h 0.7 m); {kk[0.9][i]:.1f} at 0.9 m, {kk[0.5][i]:.1f} at 0.5 m"] for i in range(len(r2))]
    aria = ("Problem K2 plots. Top: the fracture margin S over F against bone density from 55 to 100 percent of young, for the bare-floor "
            "impact of 4385 newtons (solid) and with a hip protector that halves the landing stiffness, 3101 newtons (dashed). The margin "
            "crosses 1 at 79.1 percent density for the bare floor and 66.6 percent with the protector. Bottom: the stiffest landing that "
            "still protects the hip, on a log axis, against bone density, for a 0.7 metre fall with a band for 0.5 to 0.9 metres: 13.2 "
            "kilonewtons per metre at 60 percent density, 41.8 at 80 percent; the bare floor is 40.")
    return svg(VB, aria, s, "".join(o), ([(A.box, hva), (B.box, hvb)],))


# ================================================================ svg #45  K3: saddle-node and runaway times
def k3_run(L, tmax=400.0):
    hh, t = H0, 0.0
    hs, ts = [hh], [t]
    while hh > 0.30 and t < tmax:
        hh += (-KAP * L * P0 * (H0 / hh) ** N_C + BET * (H0 - hh)) * 0.5
        t += 0.5
        hs.append(hh)
        ts.append(t)
    return np.array(ts), np.array(hs), hh <= 0.30


def fig45():
    VB = (0, 0, W, 600)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f45_"
    A = Plot(s, (58, 40, 382, 196), (0, 2), (0, 0.30))
    B = Plot(s, (58, 358, 382, 508), (0, 160), (0, 2))
    h = np.linspace(1e-3, H0 - 1e-9, 400001)
    Leq_all = BET * (H0 - h) / (KAP * P0 * (H0 / h) ** N_C)
    i = int(Leq_all.argmax())
    Ls, hs_ = Leq_all[i], h[i]
    assert f"{Ls:.3f}" == "0.211" and f"{hs_:.3f}" == "0.824"
    hh = np.arange(0.02, 1.9999, 0.01)
    Le = BET * (H0 - hh) / (KAP * P0 * (H0 / hh) ** N_C)
    o = [defs(p, s)]
    o.append(label(s, 58, 18, "a  Load that holds each thickness steady", "label", I["primary"]))
    o.append(A.axes([(0, "0"), (0.5, "0.5"), (1.0, "1.0"), (1.5, "1.5"), (2.0, "2.0")], [(0, "0"), (0.1, "0.1"), (0.2, "0.2"), (0.3, "0.3")],
                    "cartilage thickness h (mm)", "load factor L", grid=(0.1, 0.2)))
    st, un = hh >= hs_, hh <= hs_
    o.append(A.curve(hh[un], Le[un], SER[0], dash=(7, 4)))
    o.append(A.curve(hh[st], Le[st], SER[1]))
    o.append(dashed(s, A.x0, A.Y(Ls), A.x1, A.Y(Ls), O["flag"]))
    o.append(dot(A, hs_, Ls, O["flag"]))
    o.append(label(s, A.x1 - 6, A.Y(Ls) - 8, f"L* = {Ls:.3f} at h* = {hs_:.2f} mm", "label2", I["primary"], "end"))
    o.append(label(s, A.x1 - 6, A.Y(0.27), "above the peak: no steady state, runaway", "label2", I["primary"], "end"))
    o.append(label(s, A.X(0.25), A.Y(0.045), "unstable branch", "label2", I["primary"]))
    o.append(label(s, A.X(1.0), A.Y(0.03), "stable branch", "label2", I["primary"]))
    eq = {}
    for L in (0.10, 0.20):
        sel = h > hs_
        eq[L] = float(h[sel][np.argmin(np.abs(Leq_all[sel] - L))])
        o.append(dot(A, eq[L], L, SER[1]))
        o.append(label(s, A.X(eq[L]) - 9, A.Y(L) + 20, f"{eq[L]:.2f}", "label2", I["primary"], "end"))
    o.append(label(s, 58, 262, "dots: stable equilibrium h (mm) of the runs at", "label2", I["secondary"]))
    o.append(label(s, 58, 278, "L = 0.20 (h = 1.07) and L = 0.10 (h = 1.66)", "label2", I["secondary"]))
    hva = hov(A, hh, [Le], lambda i_: f"h = {hh[i_]:.2f} mm: L holding it steady = {Le[i_]:.3f}")
    # panel b: integrations
    o.append(label(s, 58, 304, "b  Integrating the loop at five loads", "label", I["primary"]))
    o.append(label(s, 58, 324, "runaway, L =", "label2", I["secondary"]))
    o.append(legend(s, 150, 324, [(SER[0], "1.00", None), (SER[0], "0.60", (2, 3)), (SER[0], "0.40", (7, 4))], gap=10))
    o.append(label(s, 58, 341, "maintained, L =", "label2", I["secondary"]))
    o.append(legend(s, 168, 341, [(SER[1], "0.10", None), (SER[1], "0.20", (7, 4))], gap=10))
    o.append(B.axes([(v, f"{v}") for v in (0, 50, 100, 150)], [(0, "0"), (0.5, "0.5"), (1.0, "1.0"), (1.5, "1.5"), (2.0, "2.0")],
                    "time (yr)", "thickness h (mm)", grid=(0.5, 1.0, 1.5)))
    o.append(dashed(s, B.x0, B.Y(0.30), B.x1, B.Y(0.30)))
    runs = {}
    for L, col, dash in ((0.10, SER[1], None), (0.20, SER[1], (7, 4)), (0.40, SER[0], (7, 4)), (0.60, SER[0], (2, 3)), (1.00, SER[0], None)):
        tt, hv_, spent = k3_run(L)
        runs[L] = (tt, hv_, spent)
        m = tt <= 160
        o.append(B.curve(tt[m], hv_[m], col, dash=dash))
    spent_t = {L: runs[L][0][-1] for L in (0.40, 0.60, 1.00)}
    assert [f"{spent_t[L]:.1f}" for L in (0.40, 0.60, 1.00)] == ["153.5", "84.0", "44.5"]
    assert [f"{runs[L][1][-1]:.3f}" for L in (0.10, 0.20)] == ["1.669", "1.187"]
    for L in (0.40, 0.60, 1.00):
        o.append(dot(B, spent_t[L], 0.30, SER[0]))
        o.append(label(s, B.X(spent_t[L]), B.Y(0.30) + 15, f"{spent_t[L]:.1f} yr", "label2", I["primary"], "middle"))
    for L, dy in ((0.10, -9), (0.20, -9)):
        hend = float(runs[L][1][np.argmax(runs[L][0] >= 160)])
        o.append(label(s, B.x1 - 6, B.Y(hend) + dy, f"L = {L:.2f}", "label2", I["primary"], "end"))
    allt = np.arange(0, 160.01, 0.5)
    rows_ = []
    for k_ in range(len(allt)):
        rows_.append([float(runs[L][1][min(k_, len(runs[L][1]) - 1)]) for L in (0.10, 0.20, 0.40, 0.60, 1.00)])
    hvb = [[round(B.X(t_), 2), [round(B.Y(y), 2) for y in ys],
            f"t = {t_:.0f} yr: h = " + ", ".join(f"{y:.2f}" for y in ys) + " mm (L 0.1, 0.2, 0.4, 0.6, 1.0)"] for t_, ys in zip(allt, rows_)]
    o.append(label(s, 58, 570, "Dashed line: spent (h = 0.30 mm). At 400 yr the", "label2", I["secondary"]))
    o.append(label(s, 58, 586, "L = 0.10 and 0.20 runs are at 1.669 and 1.187 mm.", "label2", I["secondary"]))
    aria = ("Problem K3 plots. Top: the load factor L that holds cartilage thickness h steady, L eq = beta (h0 - h) / [kappa p0 (h0/h) to the "
            "n c], against thickness from 0 to 2 millimetres. It vanishes at both ends and peaks at L star = 0.211 at h star = 0.82 millimetres, "
            "the saddle-node. The branch above 0.82 millimetres is stable (solid, blue) and the branch below is unstable (dashed, red). "
            "Bottom: thickness against time for five loads. L = 0.10 and 0.20 are maintained, still at 1.67 and 1.19 millimetres after 400 years. "
            "L = 0.40, 0.60 and 1.00 run away, reaching 0.30 millimetres at 153.5, 84.0 and 44.5 years.")
    return svg(VB, aria, s, "".join(o), ([(A.box, hva), (B.box, hvb)],))


# ================================================================ svg #47  K4: which factor to fix
def fig47():
    VB = (0, 0, W, 346)
    s = H.Scale(W, VB[3], display_w=400)
    j0, ja = jeff(**YOUNG), jeff(**AGED)
    cats = [("young, 40 yr", "b, Δt, cσ all young", j0, I["rule"], None, None)]
    for nm, key, col, el in (("margin b alone", "b", SER[0], YOUNG["b"] / (YOUNG["b"] - YOUNG["cs"])),
                              ("delay Δt alone", "dt", SER[1], -W0 * YOUNG["dt"]),
                              ("noise cσ alone", "cs", SER[2], -YOUNG["cs"] / (YOUNG["b"] - YOUNG["cs"]))):
        q = dict(YOUNG)
        q[key] = AGED[key]
        j = jeff(**q)
        cats.append((nm, "", j, col, el, 100 * (j0 - j) / (j0 - ja)))
    cats.append(("aged, 85 yr", "all three aged", ja, I["secondary"], None, None))
    assert [f"{c[2]:.2f}" for c in cats] == ["13.46", "5.98", "10.51", "11.97", "3.50"]
    assert [f"{c[5]:.0f}" for c in cats[1:4]] == ["75", "30", "15"]
    x0, sc, top, rh = 112.0, 13.0, 36.0, 48.0
    o = [label(s, 4, 18, "each factor taken to its aged value alone, the others young", "label2", I["secondary"])]
    for g in (0, 4, 8, 12, 16):
        o.append(H.line(s, x0 + g * sc, top - 6, x0 + g * sc, top + rh * 5 - 6, GRID, "leader"))
        o.append(label(s, x0 + g * sc, top + rh * 5 + 8, f"{g}", "tick", I["secondary"], "middle"))
    o.append(label(s, x0 + 8 * sc, top + rh * 5 + 27, "J" + sub("eff", s) + " (N s)", "label", I["primary"], "middle"))
    pts = []
    for k, (nm, cap, j, col, el, share) in enumerate(cats):
        y = top + k * rh
        o.append(label(s, 4, y + 15, nm, "label2", I["primary"]))
        o.append(f'<rect x="{x0}" y="{y}" width="{j * sc:.2f}" height="22" fill="{col}"/>')
        o.append(label(s, x0 + j * sc + 6, y + 16, f"{j:.2f}", "label", I["primary"]))
        if el is not None:
            o.append(label(s, x0, y + 38, f"{share:.0f} % of the drop; elasticity {el:+.2f}".replace("-", "−"), "label2", I["secondary"]))
        else:
            o.append(label(s, x0, y + 38, cap, "label2", I["secondary"]))
        pts.append([x0 + j * sc, y + 11, f"{nm}: J = {j:.2f} N s" + ("" if el is None else f" ({share:.0f} % of the drop, elasticity {el:+.2f})")])
    d_flip = YOUNG["dt"] - math.log(1 - (j0 - jeff(AGED["b"], YOUNG["dt"], YOUNG["cs"])) / j0) / W0
    assert f"{d_flip:.2f}" == "0.38"
    o.append(label(s, 4, 322, f"Delay alone would have to reach {d_flip:.2f} s ({d_flip / YOUNG['dt']:.1f} × 0.12 s)", "label2", I["primary"]))
    o.append(label(s, 4, 338, "to match what halving the margin does.", "label2", I["primary"]))
    aria = ("Problem K4 bar chart of the effective recoverable impulse in newton seconds. Young, 13.46. Taking each parameter to its aged value "
            "alone: margin b to 0.05 metres gives 5.98, 75 percent of the drop; delay to 0.20 seconds gives 10.51, 30 percent; noise c sigma to "
            "0.020 metres gives 11.97, 15 percent. All three aged, 3.50. Elasticities at the young point are plus 1.11 for b, minus 0.37 for delay "
            "and minus 0.11 for noise. The delay would have to reach 0.38 seconds to match the margin loss.")
    return svg(VB, aria, s, "".join(o), ([x0, top - 6, 400, top + rh * 5 - 6], pts))


# ================================================================ svg #49  K5: coupled cascade
def fig49():
    VB = (0, 0, W, 322)
    s = H.Scale(W, VB[3], display_w=400)
    K_AD, RHO_C = 0.03125, 0.7915
    P = Plot(s, (58, 56, 332, 226), (0, 40), (0.55, 1.05))
    t = np.arange(0, 40.001, 0.25)
    o = []
    o.append(P.axes([(0, "0"), (10, "10"), (20, "20"), (30, "30"), (40, "40")], [(0.6, "0.6"), (0.8, "0.8"), (1.0, "1.0")],
                    "years from age 40", "capacity (young = 1)", grid=(0.8, 1.0)))
    ends = {}
    for r, dash in ((0.010, None), (0.005, (7, 4))):
        cm, cb = 1 - r * t, 1 - K_AD * r * t ** 2 / 2
        ends[r] = (cm[-1], cb[-1])
        o.append(P.curve(t, cm, SER[0], dash=dash))
        o.append(P.curve(t, cb, SER[1], dash=dash))
    assert [f"{v:.3f}" for r in (0.010, 0.005) for v in ends[r]] == ["0.600", "0.750", "0.800", "0.875"]
    assert round((1 - 0.75 ** 2) * 0 + 1 - ends[0.010][1] ** 2, 2) == 0.44
    cross = math.sqrt(2 * (1 - RHO_C) / (K_AD * 0.010))
    assert f"{cross:.0f}" == "37"
    o.append(dashed(s, P.x0, P.Y(RHO_C), P.x1, P.Y(RHO_C)))
    o.append(dashed(s, P.X(cross), P.Y(RHO_C) + s(7), P.X(cross), P.y0))
    o.append(dot(P, cross, RHO_C, SER[1]))
    o.append(label(s, P.X(cross) - 4, P.y0 + 19, "37", "tick", I["primary"], "middle"))
    o.append(label(s, P.x0 + 6, P.Y(RHO_C) + 17, "fracture density 0.7915:", "label2", I["primary"]))
    o.append(label(s, P.x0 + 6, P.Y(RHO_C) + 33, "bone crosses at 37 yr (age 77)", "label2", I["primary"]))
    for r in (0.010, 0.005):
        cm, cb = ends[r]
        o.append(label(s, P.x1 + 8, P.Y(cm) + 5, f"{cm:.3f}", "label2", I["primary"]))
        o.append(label(s, P.x1 + 8, P.Y(cb) + 5, f"{cb:.3f}", "label2", I["primary"]))
    o.append(legend(s, 58, 18, [(SER[0], "muscle", None), (SER[1], "bone", None)], gap=10))
    o.append(legend(s, 58, 36, [(I["axis"], "r = 0.010 per yr", None), (I["axis"], "r = 0.005 per yr", (7, 4))], gap=10))
    o.append(label(s, 58, 290, "r = 0: both stay at 1. Bone strength S ∝ ρ²:", "label2", I["secondary"]))
    o.append(label(s, 58, 307, "0.562 at r = 0.010, 0.766 at r = 0.005.", "label2", I["secondary"]))
    hv = hov(P, t, [1 - 0.010 * t, 1 - K_AD * 0.010 * t ** 2 / 2, 1 - 0.005 * t, 1 - K_AD * 0.005 * t ** 2 / 2],
             lambda i: f"t = {t[i]:.1f} yr: r 0.010 muscle {1 - 0.010 * t[i]:.3f}, bone {1 - K_AD * 0.010 * t[i] ** 2 / 2:.3f}; "
                       f"r 0.005 muscle {1 - 0.005 * t[i]:.3f}, bone {1 - K_AD * 0.005 * t[i] ** 2 / 2:.3f}")
    aria = ("Problem K5 plot. Muscle capacity falls linearly, 1 minus r t, and bone capacity as the integral of the muscle deficit, 1 minus "
            "half k ad r t squared, over forty years from age 40, with k ad = 0.03125 per year. For r = 0.010 per year, solid, muscle reaches "
            "0.600 and bone 0.750, a bone strength of 0.562. For r = 0.005, dashed, muscle reaches 0.800 and bone 0.875. For r = 0 both stay "
            "at 1. Bone crosses the fracture density 0.7915 at 37 years, age 77, only for r = 0.010.")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #51  K6: the training dose
def fig51():
    VB = (0, 0, W, 520)
    s = H.Scale(W, VB[3], display_w=400)
    KB, KL = 0.015, 0.010
    A = Plot(s, (58, 56, 382, 196), (0, 24), (0.78, 1.03))
    B = Plot(s, (58, 310, 382, 470), (0, 1), (-1.6, 1.7))
    o = []
    o.append(label(s, 58, 18, "a  Closing a 20 % deficit, and losing it", "label", I["primary"]))
    o.append(A.axes([(v, f"{v}") for v in (0, 5, 10, 15, 20)], [(0.8, "0.8"), (0.9, "0.9"), (1.0, "1.0")], "weeks", "strength (young = 1)", grid=(0.9, 1.0)))
    tb = 0.20 / KB
    tl = 0.20 / KL
    assert f"{tb:.1f}" == "13.3" and f"{tl:.1f}" == "20.0"
    wk = np.arange(0, tb + 1e-9, 0.25)
    wk2 = np.arange(0, tl + 1e-9, 0.25)
    up = 0.80 + KB * wk
    dn = 1.00 - KL * wk2
    o.append(A.curve(wk, up, SER[1]))
    o.append(A.curve(wk2, dn, SER[0]))
    o.append(dot(A, tb, 1.0, SER[1]))
    o.append(dot(A, tl, 0.8, SER[0]))
    o.append(label(s, A.X(tb) + 9, A.Y(1.0) + 18, f"{tb:.1f} wk", "label2", I["primary"]))
    o.append(label(s, A.X(tl) + 9, A.Y(0.8) + 4, f"{tl:.1f} wk", "label2", I["primary"]))
    o.append(legend(s, 58, 38, [(SER[1], "build +1.5 %/wk", None), (SER[0], "idle −1.0 %/wk", None)], gap=10))
    hva = hov(A, wk2, [[0.8 + KB * min(w_, tb) for w_ in wk2], dn], lambda i: f"week {wk2[i]:.1f}: training from 0.80 gives {0.8 + KB * min(wk2[i], tb):.3f}; idle from 1.00 gives {dn[i]:.3f}")
    # panel b: duty cycle
    o.append(label(s, 58, 284, "b  Net rate when a fraction f of weeks is trained", "label", I["primary"]))
    o.append(B.axes([(0, "0"), (0.2, "0.2"), (0.4, "0.4"), (0.6, "0.6"), (0.8, "0.8"), (1.0, "1.0")], [(-1, "−1"), (0, "0"), (1, "1")],
                    "duty fraction f (trained weeks / all weeks)", "net rate (% per wk)", grid=(0,)))
    f = np.arange(0, 1.0001, 0.01)
    net = 100 * (f * KB - (1 - f) * KL)
    o.append(B.curve(f, net, I["axis"]))
    fh = KL / (KB + KL)
    f52 = (0.20 / 52 + KL) / (KB + KL)
    f26 = (0.20 / 26 + KL) / (KB + KL)
    assert (f"{fh:.2f}", f"{f52:.2f}", f"{f26:.2f}") == ("0.40", "0.55", "0.71")
    assert (f"{5 * fh:.1f}", f"{f52 * 52:.0f}", f"{f26 * 26:.0f}") == ("2.0", "29", "18")
    for fx, ytxt in ((fh, 0.0), (f52, 100 * 0.20 / 52), (f26, 100 * 0.20 / 26)):
        o.append(dot(B, fx, ytxt, O["flag"] if fx == fh else SER[1]))
    o.append(label(s, B.X(fh) + 9, B.Y(0) + 20, f"{fh:.2f}", "label2", I["primary"]))
    o.append(label(s, B.X(f52) + 9, B.Y(100 * 0.20 / 52) + 20, f"{f52:.2f}", "label2", I["primary"]))
    o.append(label(s, B.X(f26) + 9, B.Y(100 * 0.20 / 26) + 20, f"{f26:.2f}", "label2", I["primary"]))
    o.append(label(s, B.x1 - 6, B.Y(-0.82), f"f = {fh:.2f}: holds ground, 2.0 weeks in 5", "label2", I["primary"], "end"))
    o.append(label(s, B.x1 - 6, B.Y(-1.16), f"f = {f52:.2f}: +20 % in 52 wk, 29 weeks trained", "label2", I["primary"], "end"))
    o.append(label(s, B.x1 - 6, B.Y(-1.50), f"f = {f26:.2f}: +20 % in 26 wk, 18 weeks trained", "label2", I["primary"], "end"))
    hvb = hov(B, f, [net], lambda i: f"f = {f[i]:.2f}: net rate {net[i]:+.2f} % per week")
    aria = ("Problem K6 plots. Top: strength against weeks. Training at a build rate of 1.5 percent per week closes a 20 percent deficit "
            "in 13.3 weeks; idle loss at 1.0 percent per week gives it back in 20.0 weeks. Bottom: the net rate when a fraction f of weeks "
            "carries the training overload, f k build minus (1 - f) k lose, a straight line from minus 1.0 percent per week at f = 0 to plus "
            "1.5 at f = 1. It crosses zero at f = 0.40, two weeks in five. A gain of 20 percent in 52 weeks needs f = 0.55, 29 training "
            "weeks; in 26 weeks it needs f = 0.71, 18 training weeks.")
    return svg(VB, aria, s, "".join(o), ([(A.box, hva), (B.box, hvb)],))


# ================================================================ svg #53  K7: the fracture map
def fig53():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 40, 382, 240), (0.25, 1.15), (50, 100))
    hf = np.arange(0.3, 1.1001, 0.01)
    rc = 100 * np.sqrt(np.array([force(v) for v in hf]) / S0)
    o = []
    o.append(P.axes([(v, f"{v}") for v in (0.3, 0.5, 0.7, 0.9, 1.1)], [(v, f"{v}") for v in (50, 60, 70, 80, 90, 100)],
                    "fall height h" + sub("f", s) + " (m)", "bone density ρ (% of young)", grid=(60, 70, 80, 90)))
    poly = " ".join(f"{P.X(a):.2f},{P.Y(b):.2f}" for a, b in zip(hf, rc)) + f" {P.X(1.1):.2f},{P.y0:.2f} {P.X(0.3):.2f},{P.y0:.2f}"
    o.append(f'<polygon points="{poly}" fill="{O["force"]}" fill-opacity="0.12" stroke="none"/>')
    o.append(P.curve(hf, rc, SER[0]))
    chk = [round(100 * math.sqrt(force(v) / S0) / 100, 3) for v in (0.3, 0.5, 0.7, 0.9, 1.1)]
    assert chk == [0.640, 0.728, 0.791, 0.843, 0.886]
    o.append(H.line(s, P.X(0.3), P.Y(60), P.X(1.1), P.Y(60), O["dim"], "ref", H.DASH_REF))
    o.append(H.line(s, P.X(0.3), P.Y(90), P.X(1.1), P.Y(90), O["dim"], "ref", H.DASH_REF))
    for k_, v in enumerate((0.3, 0.5, 0.7, 0.9, 1.1)):
        r_ = 100 * math.sqrt(force(v) / S0)
        o.append(dot(P, v, r_, SER[0]))
        o.append(label(s, P.X(v) + 8, P.Y(r_) + (30 if k_ == 0 else 22), f"{r_:.1f}", "label2", I["primary"]))
    o.append(label(s, P.X(0.55), P.Y(60) - 8, "ρ = 60 %: fractures at every height", "label2", I["primary"]))
    o.append(label(s, P.X(0.3) + 4, P.Y(90) - 8, "ρ = 90 %: survives all of them", "label2", I["primary"]))
    o.append(label(s, P.x1 - 6, P.Y(52) , "FRACTURE: S < F", "label", I["primary"], "end"))
    o.append(label(s, P.X(0.7), P.Y(97), "safe: S > F", "label", I["primary"], "middle"))
    o.append(label(s, P.x1 - 6, P.Y(72), "boundary ∝ h" + sub("f", s, "label2") + "¼", "label2", I["primary"], "end"))
    hv = hov(P, hf, [rc], lambda i: f"hf = {hf[i]:.2f} m: fracture below ρ = {rc[i]:.1f} %")
    aria = ("Problem K7 map. Bone density as a percentage of young against fall height from 0.3 to 1.1 metres, for landing stiffness 40 kilonewtons "
            "per metre. The fracture boundary rises as the fourth root of height: 64.0 percent density at 0.3 metres, 72.8 at 0.5, 79.1 at 0.7, "
            "84.3 at 0.9 and 88.6 at 1.1. The region below it, tinted red, fractures the hip. A dashed line at 60 percent lies inside it at every "
            "height and a dashed line at 90 percent lies above it at every height.")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #55  K8: which task fails first
def fig55():
    VB = (0, 0, W, 318)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f55_"
    P = Plot(s, (58, 40, 312, 238), (40, 95), (0, 2))
    ag = np.arange(40, 95.01, 0.5)
    o = [defs(p, s)]
    o.append(P.axes([(v, f"{v}") for v in (40, 50, 60, 70, 80, 90)], [(0, "0"), (1, "1"), (2, "2")], "age (yr)", "reserve R", grid=(1,)))
    o.append(dashed(s, P.x0, P.Y(1), P.x1, P.Y(1)))
    ends = []
    series = {}
    for nm, d, col in TASKS[::-1]:
        R = TAU_TYP * (1 - RATE * (ag - A0)) / d
        series[nm] = R
        o.append(P.curve(ag, R, col))
        ends.append((nm, d, col, float(R[-1])))
    fails = {nm: astar(TAU_TYP, d) for nm, d, _ in TASKS}
    assert [round(fails[n]) for n in ("floor", "chair", "stair")] == [54, 77, 83]
    for nm, d, col in TASKS:
        o.append(dot(P, fails[nm], 1, col))
    # right-hand labels, nudged so the three ends do not overlap
    ypos = {"stair": P.Y(ends[0][3]) - 6, "chair": P.Y(ends[1][3]) + 7, "floor": P.Y(ends[2][3]) + 5}
    for nm, d, col, rr in ends:
        o.append(label(s, P.x1 + 8, ypos[nm] + 4, f"{nm}  D = {d:.0f}", "label2", I["primary"]))
    yb = P.Y(0.40)
    for nm in ("floor", "chair", "stair"):
        o.append(dashed(s, P.X(fails[nm]), P.Y(1) + s(7), P.X(fails[nm]), P.Y(0.40) - s(0), O["dim"]))
    o.append(H.arrow(s, p, P.X(fails["floor"]), yb, P.X(fails["chair"]), yb, "geometry", both=True))
    o.append(H.arrow(s, p, P.X(fails["chair"]), yb, P.X(fails["stair"]), yb, "geometry", both=True))
    o.append(label(s, (P.X(fails["floor"]) + P.X(fails["chair"])) / 2, yb + 17, f"{fails['chair'] - fails['floor']:.0f} yr", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(fails["stair"]) + 10, yb + 5, f"{fails['stair'] - fails['chair']:.0f} yr", "label2", I["primary"]))
    o.append(label(s, P.X(fails["floor"]) - 7, P.Y(0.12), f"{fails['floor']:.0f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(fails["chair"]) - 7, P.Y(0.12), f"{fails['chair']:.0f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(fails["stair"]) + 7, P.Y(0.12), f"{fails['stair']:.0f}", "label2", I["primary"]))
    o.append(label(s, 58, 18, "R = τ" + sub("p", s, "label2") + "(1 − r(a − a" + sub("0", s, "label2") + "))/D, τ" + sub("p", s, "label2") + " = 175 N m", "label2", I["secondary"]))
    hv = hov(P, ag, [series["stair"], series["chair"], series["floor"]],
             lambda i: f"age {ag[i]:.1f} yr: R = {series['stair'][i]:.2f} (stair), {series['chair'][i]:.2f} (chair), {series['floor'][i]:.2f} (floor)")
    aria = ("Problem K8 plot. The strength reserve R = tau p (1 - r (a - a0)) / D against age from 40 to 95, for peak strength 175 newton metres "
            "and three task demands: deep floor rise D = 150, chair D = 110 and gentle stair D = 100 newton metres. Each line falls and crosses "
            "R = 1 in order of demand: the floor rise at 54 years, the chair at 77 and the stair at 83. Double-headed arrows mark the gaps, 23 "
            "years from floor to chair and 6 years from chair to stair.")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #57  K9: fall probability
def fig57():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    JB = 8.0
    P = Plot(s, (58, 56, 382, 240), (0, 16), (0, 1.0))
    J = np.arange(0, 16.001, 0.1)
    Pf = np.exp(-J / JB)
    o = [P.axes([(0, "0"), (4, "4"), (8, "8"), (12, "12"), (16, "16")], [(0, "0"), (0.25, "0.25"), (0.5, "0.5"), (0.75, "0.75"), (1.0, "1.0")],
                "effective recoverable impulse J" + sub("eff", s) + " (N s)", "fall probability per event", grid=(0.5,))]
    o.append(P.curve(J, Pf, SER[0]))
    o.append(label(s, 58, 18, "P = Pr(J > J" + sub("eff", s, "label2") + ") = exp(−J" + sub("eff", s, "label2") + " / J̄), J̄ = 8 N s", "label2", I["secondary"]))
    young, aged = np.array([0.10, 0.12, 0.010]), np.array([0.05, 0.20, 0.020])
    chk = []
    for age in (40, 55, 70, 85):
        b, dt, cs = young + (age - 40) / 45.0 * (aged - young)
        j = M_KG * W0 * (b - cs) * math.exp(-W0 * dt)
        pf = math.exp(-j / JB)
        chk.append((f"{j:.2f}", f"{pf:.2f}"))
        o.append(dot(P, j, pf, SER[0]))
        if age == 40:
            o.append(label(s, P.X(j) - 9, P.Y(pf) + 22, f"age {age}: {pf:.2f}", "label2", I["primary"], "end"))
        else:
            o.append(label(s, P.X(j) + 9, P.Y(pf) - 10, f"age {age}: {pf:.2f}", "label2", I["primary"]))
    assert chk == [("13.46", "0.19"), ("9.64", "0.30"), ("6.34", "0.45"), ("3.50", "0.65")]
    f35 = math.exp(-3.5 / JB)
    o.append(label(s, P.x1 - 6, P.Y(0.88), f"+3.5 N s at any age: P × {f35:.2f}", "label2", I["primary"], "end"))
    hv = hov(P, J, [Pf], lambda i: f"J_eff = {J[i]:.1f} N s: P(fall) = {Pf[i]:.2f}")
    aria = ("Problem K9 plot. The fall probability per event, P = exp(-J eff / 8 newton seconds), for exponentially distributed everyday "
            "perturbation impulses with mean 8 newton seconds, against the effective recoverable impulse J eff from 0 to 16. Marked points "
            "from the Lab D age law: age 40, J eff 13.46 newton seconds, probability 0.19; age 55, 9.64, 0.30; age 70, 6.34, 0.45; age 85, "
            "3.50, 0.65. A fixed gain of 3.5 newton seconds multiplies the probability by 0.65 at any age.")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #59  K10: spending a training budget
def fig59():
    VB = (0, 0, W, 398)
    s = H.Scale(W, VB[3], display_w=400)
    base = dict(b=0.05, d=0.20, cs=0.020)
    move = dict(b=0.08, d=0.14, cs=0.010)
    J = lambda **kw: jeff(kw["b"], kw["d"], kw["cs"])  # noqa: E731
    keys = ("b", "d", "cs")
    chip = {"b": SER[0], "d": SER[1], "cs": SER[2]}
    from itertools import combinations
    rows = []
    for n in (0, 1, 2, 3):
        for combo in combinations(keys, n):
            a = dict(base)
            for c in combo:
                a[c] = move[c]
            rows.append((combo, J(**a)))
    rows.sort(key=lambda r: r[1])
    val = {c: j for c, j in rows}
    assert f"{val[()]:.2f}" == "3.50" and f"{val[('b',)]:.2f}" == "7.00" and f"{val[('d',)]:.2f}" == "4.22"
    assert f"{val[('cs',)]:.2f}" == "4.67" and f"{val[('b', 'd', 'cs')]:.2f}" == "9.84" and f"{val[('b', 'd')]:.2f}" == "8.44"
    assert f"{val[('b', 'cs')]:.2f}" == "8.17" and f"{val[('d', 'cs')]:.2f}" == "5.62"
    add = val[()] + sum(val[(k,)] - val[()] for k in keys)
    x0, x1 = 78.0, 330.0
    sc = (x1 - x0) / 10.0
    top, rh = 100.0, 25.0
    o = []
    names = {"b": "strength: b 0.05 → 0.08 m", "d": "reaction: Δt 0.20 → 0.14 s", "cs": "sensory: cσ 0.020 → 0.010 m"}
    for k, key in enumerate(keys):
        y = 22 + 18 * k
        o.append(f'<circle cx="12" cy="{y - 4}" r="{s(5):.2f}" fill="{chip[key]}"/>')
        o.append(label(s, 24, y, names[key], "label2", I["primary"]))
    for g in (0, 2, 4, 6, 8, 10):
        o.append(H.line(s, x0 + g * sc, top - 8, x0 + g * sc, top + rh * len(rows) - 4, GRID, "leader"))
        o.append(label(s, x0 + g * sc, top + rh * len(rows) + 12, f"{g}", "tick", I["secondary"], "middle"))
    o.append(label(s, (x0 + x1) / 2, top + rh * len(rows) + 31, "J" + sub("eff", s) + " (N s)", "label", I["primary"], "middle"))
    pts = []
    for k, (combo, j) in enumerate(rows):
        y = top + k * rh
        for ci, key in enumerate(keys):
            cx = 14 + ci * 20
            if key in combo:
                o.append(f'<circle cx="{cx}" cy="{y + 9}" r="{s(6):.2f}" fill="{chip[key]}"/>')
            else:
                o.append(f'<circle cx="{cx}" cy="{y + 9}" r="{s(6):.2f}" fill="none" stroke="{GRID}" stroke-width="{s(1.4):.2f}"/>')
        o.append(f'<rect x="{x0}" y="{y}" width="{j * sc:.2f}" height="{rh - 8:.1f}" fill="{I["muted"]}" fill-opacity="{0.35 if combo else 0.18}"/>')
        o.append(label(s, x0 + j * sc + 6, y + 14, f"{j:.2f}" + (" (aged baseline)" if not combo else ""), "label2", I["primary"]))
        nm = " + ".join({"b": "strength", "d": "reaction", "cs": "sensory"}[c] for c in combo) or "aged baseline"
        pts.append([x0 + j * sc, y + 8, f"{nm}: J_eff = {j:.2f} N s"])
    ya = top + rh * (len(rows) - 1)
    o.append(f'<line x1="{x0 + add * sc:.2f}" y1="{ya - 3:.2f}" x2="{x0 + add * sc:.2f}" y2="{ya + rh - 5:.2f}" stroke="{O["flag"]}" stroke-width="{s(2):.2f}"/>')
    o.append(label(s, 4, 378, f"Orange tick: baseline plus the three single gains = {add:.2f} N s.", "label2", I["primary"]))
    o.append(label(s, 4, 394, "All three together give more, so the factors multiply.", "label2", I["primary"]))
    aria = ("Problem K10 bar chart. The effective recoverable impulse J eff in newton seconds for the aged body, 3.50, and for every combination "
            "of three training moves, marked by filled dots: strength (margin b 0.05 to 0.08 metres, red), reaction (delay 0.20 to 0.14 seconds, "
            "blue) and sensory work (c sigma 0.020 to 0.010 metres, orange). Single moves give 4.22 for reaction, 4.67 for sensory and 7.00 for "
            "strength; pairs give 5.62, 8.17 and 8.44; all three give 9.84. Adding the three single gains to the baseline would give "
            f"{add:.2f}, so the combination is super-additive.")
    return svg(VB, aria, s, "".join(o), ([0, top - 8, 380, top + rh * len(rows)], pts))


# ================================================================ svg #61  K11: AGE crossover
K_AGE, K_BONE, K_TENDON = 1.16e-3, 0.10, 0.005
GLC_N, GLC_D = 5.5, 11.0


def _sim(onset, k_turn, age_end=80.0, dt=0.05):
    n = int(round((age_end - 20.0) / dt))
    phi = 0.0
    for i in range(n):
        age = 20.0 + i * dt
        glc = GLC_D if age >= onset else GLC_N
        phi += dt * (K_AGE * glc * (1 - phi) - k_turn * phi)
    return phi


def _closed(onset, k_turn):
    normo, dia = _sim(math.inf, k_turn), _sim(-math.inf, k_turn)
    return (_sim(onset, k_turn) - normo) / (dia - normo)


def fig61():
    VB = (0, 0, W, 560)
    s = H.Scale(W, VB[3], display_w=400)
    A = Plot(s, (58, 56, 382, 206), (math.log10(0.002), math.log10(0.5)), (0, 100))
    B = Plot(s, (58, 352, 382, 476), (0, 3), (0, 112))
    lg = math.log10
    o = []
    o.append(label(s, 58, 18, "a  Gap closed by a 10-year bout, against turnover", "label", I["primary"]))
    ks = np.logspace(lg(0.002), lg(0.5), 40)
    ys = np.array([100 * _closed(70.0, k) for k in ks])
    lo, hi = 0.005, 0.8
    flo = _closed(70.0, lo) - 0.5
    for _ in range(40):
        mid = math.sqrt(lo * hi)
        fm = _closed(70.0, mid) - 0.5
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    kstar = math.sqrt(lo * hi)
    assert f"{kstar:.3f}" == "0.055" and f"{1 / kstar:.0f}" == "18"
    gb, gt = 100 * _closed(70.0, K_BONE), 100 * _closed(70.0, K_TENDON)
    assert (f"{gb:.0f}", f"{gt:.0f}") == ("68", "22")
    o.append(A.axes([(lg(v), f"{v}") for v in (0.005, 0.01, 0.05, 0.1, 0.5)], [(0, "0"), (25, "25"), (50, "50"), (75, "75"), (100, "100")],
                    "collagen turnover k" + sub("turn", s) + " (per yr, log scale)", "% of gap closed", grid=(50,)))
    o.append(A.curve([lg(k) for k in ks], ys, I["axis"]))
    o.append(dashed(s, A.X(lg(kstar)), A.Y(50) + s(7), A.X(lg(kstar)), A.y0))
    o.append(dot(A, lg(kstar), 50, O["flag"]))
    o.append(dot(A, lg(K_BONE), gb, SER[1]))
    o.append(dot(A, lg(K_TENDON), gt, SER[0]))
    o.append(label(s, A.X(lg(kstar)) - 9, A.Y(50) - 28, f"k* = {kstar:.3f} per yr", "label2", I["primary"], "end"))
    o.append(label(s, A.X(lg(kstar)) - 9, A.Y(50) - 11, f"({1 / kstar:.0f}-yr residence)", "label2", I["primary"], "end"))
    o.append(label(s, A.X(lg(K_BONE)) + 9, A.Y(gb) + 20, f"bone {gb:.0f} %", "label2", I["primary"]))
    o.append(label(s, A.X(lg(K_TENDON)) + 9, A.Y(gt) + 20, f"tendon {gt:.0f} %", "label2", I["primary"]))
    hva = [[round(A.X(lg(k)), 2), round(A.Y(y), 2), f"kturn = {k:.4f} per yr: gap closed {y:.0f} %"] for k, y in zip(ks, ys)]
    # panel b: bout length sweep
    o.append(label(s, 58, 304, "b  Bout length: bone against tendon", "label", I["primary"]))
    o.append(B.axes([], [(0, "0"), (25, "25"), (50, "50"), (75, "75"), (100, "100")], "", "% of gap closed", grid=(25, 50, 75, 100), ytx=15))
    vals = {}
    for onset in (70.0, 60.0, 40.0):
        vals[onset] = (100 * _closed(onset, K_BONE), 100 * _closed(onset, K_TENDON))
    assert [(f"{b:.0f}", f"{t:.0f}") for b, t in vals.values()] == [("68", "22"), ("90", "42"), ("99", "74")]
    pts = []
    for g, (onset, (vb, vt)) in enumerate(vals.items()):
        xc = B.X(g + 0.5)
        bw = (B.x1 - B.x0) / 3 * 0.30
        for dx, v, col, nm in ((-bw / 2 - 2, vb, SER[1], "bone"), (bw / 2 + 2, vt, SER[0], "tendon")):
            o.append(f'<rect x="{xc + dx - bw / 2:.2f}" y="{B.Y(v):.2f}" width="{bw:.2f}" height="{B.y0 - B.Y(v):.2f}" fill="{col}"/>')
            o.append(label(s, xc + dx, B.Y(v) - 7, f"{v:.0f} %", "label2", I["primary"], "middle"))
            pts.append([round(xc + dx, 2), round(B.Y(v), 2), f"{80 - onset:.0f} yr bout: {nm} closes {v:.0f} % of its gap"])
        o.append(label(s, xc, B.y0 + 19, f"{80 - onset:.0f} yr", "label2", I["primary"], "middle"))
    o.append(label(s, (B.x0 + B.x1) / 2, B.y0 + 40, "years of hyperglycemia before age 80", "label", I["primary"], "middle"))
    o.append(legend(s, 58, 326, [(SER[1], "bone, k = 0.10 per yr", None)]))
    o.append(legend(s, 58, 343, [(SER[0], "tendon, k = 0.005 per yr", None)]))
    # tendon +10 %
    normo_t = _sim(math.inf, K_TENDON)
    lo_, hi_ = 20.0, 79.0

    def ex(onset):
        return (_sim(onset, K_TENDON) - normo_t) / normo_t - 0.10
    for _ in range(40):
        mid = 0.5 * (lo_ + hi_)
        if (ex(mid) > 0) == (ex(lo_) > 0):
            lo_ = mid
        else:
            hi_ = mid
    yrs10 = 80 - 0.5 * (lo_ + hi_)
    assert f"{yrs10:.1f}" == "6.3"
    o.append(label(s, 58, 534, f"{yrs10:.1f} years of hyperglycemia ending at 80", "label2", I["primary"]))
    o.append(label(s, 58, 551, "raise tendon's AGE burden by 10 %.", "label2", I["primary"]))
    aria = ("Problem K11 plots. Top: the percentage of the gap to a lifelong-diabetic burden that a 10-year hyperglycemic bout ending at age 80 "
            "closes, against collagen turnover on a log axis. It rises from about 19 percent with no turnover to 100 percent and reaches 50 percent at the crossover "
            "turnover 0.055 per year, an 18-year residence. Bone, at 0.10 per year, closes 68 percent; tendon, at 0.005, closes 22 percent. "
            "Bottom: bars of the gap closed for bouts of 10, 20 and 40 years: bone 68, 90 and 99 percent, tendon 22, 42 and 74 percent. "
            f"{yrs10:.1f} years of hyperglycemia raise tendon's burden by 10 percent.")
    return svg(VB, aria, s, "".join(o), ([(A.box, hva), ([B.x0, B.y1, B.x1, B.y0], pts)],))


FIGS = {
    35: ("D5: delay erosion. Derive the factor by which reaction delay", fig35),
    36: ("D6: effective recoverable impulse. Assemble the fall-recover", fig36),
    37: ("D7: the mechanostat. Show that a set-point rate law makes tr", fig37),
    39: ("D9: demand shifts the age. Show how the failure age moves wi", fig39),
    40: ("D10: impact scaling. Show how the fall-impact force scales w", fig40),
    41: ("K1: the strength to reach a target age (inverse + demand swe", fig41),
    43: ("K2: the critical bone density (inverse + regime). Find the b", fig43),
    45: ("K3: the load that holds each cartilage thickness steady, pea", fig45),
    47: ("K4: which fall-risk factor to fix (sensitivity ranking). For", fig47),
    49: ("K5: muscle capacity falling linearly and bone capacity falli", fig49),
    51: ("K6: the training dose (inverse). Compute the time for a resi", fig51),
    53: ("K7: the fracture map (2-D sweep). Map the hip-fracture regio", fig53),
    55: ("K8: which task fails first (multi-task regime). Give three d", fig55),
    57: ("K9: fall probability (simulation). Convolve the effective re", fig57),
    59: ("K10: spending a training budget (optimisation). Given interv", fig59),
    61: ("K11: bone and tendon AGE-fraction gap closed, as a percentag", fig61),
}
