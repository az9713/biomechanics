"""Module 14 problem figures, group `prob_a` (svg idx 21 C1, 22 C2, 25 C5, 26 C6, 27 C7, 28 C8, 29 C9,
30 C10, 31 D1, 32 D2, 34 D4). Problem figures: 400 units wide, rendered 400 px, so 1 user unit = 1 px.

Every plotted number is computed here from the module's formulas and constants:
  R(a) = tau_p [1 - r (a - a0)] / D, a* = a0 + (1/r)(1 - D/tau_p)   (Prop. 2.1, text line 60-61)
  D = 110 N m, tau_p = 175 N m (210 N m trained), a0 = 40 yr, r = 0.01 /yr   (text line 61, 219)
  S = S0 (rho/rho0)^n_b, n_b = 2                                      (Prop. 3.1, text line 114-118)
  p = p0 (h0/h)^n_c, p0 = 3 MPa, h0 = 2 mm, n_c = 0.7                 (Prop. 4.1, text line 138-140)
  recoverable fraction = exp(-w0 dt), w0 = 3.1 rad/s                  (Prop. 5.1, text line 154-156)
  usable margin = b - c sigma, b = 0.10 / 0.05 m                      (Prop. 6.1, text line 193-203)
"""
import math

import numpy as np

import house as H
from m05.plots_prob import Plot, W, hov, label, legend, svg, text_w

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"
BOX = "#f7f4ef"

# ---------------------------------------------------------------- module constants
D_N, TAU_P, TAU_P2, A0, RATE = 110.0, 175.0, 210.0, 40.0, 0.01     # chair demand, strengths (N m), age (yr), 1/yr
N_B = 2
P0, H0, N_C = 3.0, 2.0, 0.7                                         # MPa, mm, exponent
W0 = 3.1                                                            # rad/s


def astar(tp):
    return A0 + (1 - D_N / tp) / RATE


def reserve(a, tp=TAU_P):
    return tp * (1 - RATE * (np.asarray(a, float) - A0)) / D_N


def sub(t, s, size="label"):
    return H.sub(t, s, size)


def sup(t, s, size="label"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def it(t):
    return f'<tspan font-style="italic">{t}</tspan>'


def defs(p, s):
    return f"<defs>{H.markers(p, s)}</defs>"


def dashed(s, x1, y1, x2, y2, col=None):
    return H.line(s, x1, y1, x2, y2, col or O["dim"], "ref", H.DASH_REF)


def dot(P, x, y, col, hollow=False):
    s = P.s
    r = s(H.PX["dot"])
    cx, cy = P.X(x), P.Y(y)
    if hollow:
        return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="#fff" stroke="{col}" stroke-width="{s(1.8):.2f}"/>'
    return P.dot(x, y, col)


def band(P, y_top, y_bot, col, op):
    return (f'<rect x="{P.x0:.2f}" y="{P.Y(y_top):.2f}" width="{P.x1 - P.x0:.2f}" height="{P.Y(y_bot) - P.Y(y_top):.2f}" '
            f'fill="{col}" opacity="{op}"/>')


def rect_edge(box, tx, ty, gap=4.0):
    """Point on the border of box (x, y, w, h) on the line from its centre towards (tx, ty), pushed out by gap."""
    x, y, w, h = box
    cx, cy = x + w / 2, y + h / 2
    dx, dy = tx - cx, ty - cy
    k = min((w / 2) / abs(dx) if dx else 1e9, (h / 2) / abs(dy) if dy else 1e9)
    L = math.hypot(dx, dy)
    return cx + dx * k + dx / L * gap, cy + dy * k + dy / L * gap


def link(s, p, a, b, meaning="dim", both=False, w=None, gap=4.0):
    """Arrow between two node boxes, border to border along the centre line."""
    acx, acy = a[0] + a[2] / 2, a[1] + a[3] / 2
    bcx, bcy = b[0] + b[2] / 2, b[1] + b[3] / 2
    x1, y1 = rect_edge(a, bcx, bcy, gap)
    x2, y2 = rect_edge(b, acx, acy, gap)
    return H.arrow(s, p, x1, y1, x2, y2, meaning, w=w or ("force" if meaning == "force" else "ref"), both=both)


def node(s, b, title, sub_text=None, accent=None):
    x, y, w, h = b
    o = (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="6" fill="{BOX}" stroke="{I["rule"]}" '
         f'stroke-width="{s(1):.2f}"/>')
    if accent:
        o += f'<rect x="{x:.2f}" y="{y:.2f}" width="{s(5):.2f}" height="{h:.2f}" rx="2" fill="{accent}"/>'
    if sub_text:
        o += H.label(s, x + w / 2 + 2, y + h / 2 - 2, title, "label", I["primary"], "middle")
        o += H.label(s, x + w / 2 + 2, y + h / 2 + 15, sub_text, "label2", I["secondary"], "middle")
    else:
        o += H.label(s, x + w / 2 + 2, y + h / 2 + 5, title, "label", I["primary"], "middle")
    return o


def title_xaxis(s, P, text, dy=40):
    return label(s, (P.x0 + P.x1) / 2, P.y0 + dy, text, "label", I["primary"], "middle")


# ================================================================ svg #21  C1: the sudden cliff
def reserve_plot(p, with_dim):
    """C1 and D1 share the R(a) plot (text line 61: D = 110 N m, tau_p = 175 N m, a0 = 40 yr, r = 0.01/yr)."""
    VB = (0, 0, W, 290)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 40, 382, 215), (40, 95), (0, 2))
    ages = np.arange(40, 95.01, 0.5)
    R = reserve(ages)
    a_s = astar(TAU_P)
    o = [defs(p, s)]
    if not with_dim:
        o.append(band(P, 1, 0, O["force"], 0.10))
        o.append(band(P, 2, 1, BOX, 1))
    o.append(P.axes([(v, f"{v}") for v in range(40, 91, 10)], [(0, "0"), (1, "1"), (2, "2")], "", "reserve R", grid=(1,)))
    o.append(title_xaxis(s, P, "age (yr)"))
    o.append(P.curve(ages, R, SER[0]))
    o.append(dashed(s, P.x0, P.Y(1), P.x1, P.Y(1)))
    o.append(legend(s, 58, 18, [(SER[0], "reserve R = τ" + sub("max", s, "label2") + "/D", None),
                                (O["dim"], "R = 1", H.DASH_REF)]))
    o.append(dot(P, a_s, 1, SER[0]))
    hv = hov(P, ages, [R], lambda i: f"age {ages[i]:.1f} yr: R = {R[i]:.2f} (τmax {R[i] * D_N:.0f} N m)")
    if not with_dim:
        o.append(label(s, P.X(a_s) + 9, P.Y(1) - 9, f"a* = {a_s:.1f} yr", "label", I["primary"]))
        o.append(label(s, P.x1 - 6, P.Y(1.8), "chair rise possible (R > 1)", "label2", I["secondary"], "end"))
        o.append(label(s, P.x1 - 6, P.Y(0.3), "cannot rise (R < 1)", "label2", I["secondary"], "end"))
        o.append(label(s, P.X(42), P.Y(0.42), "τ" + sub("max", s, "label2") + " falls 1 % per year", "label2", I["secondary"]))
        aria = ("Problem C1 plot. The chair-rise strength reserve R equals peak strength 175 newton metres, reduced by 1 percent "
                "of it per year after age 40, divided by the chair demand of 110 newton metres. R falls in a straight line "
                "from 1.59 at age 40 to 0.72 at 95 and crosses the threshold R = 1 at age 77.1. Above 1 the chair rise is "
                "possible and below 1 it is not, so a smooth decline of strength gives an abrupt change of ability.")
    else:
        o.append(dashed(s, P.X(a_s), P.Y(1) + s(7), P.X(a_s), P.Y(0.42)))
        o.append(dashed(s, P.X(A0), P.Y(1.59) + s(7), P.X(A0), P.Y(0.42)))
        o.append(H.arrow(s, p, P.X(A0), P.Y(0.42), P.X(a_s), P.Y(0.42), "geometry", both=True))
        o.append(label(s, (P.X(A0) + P.X(a_s)) / 2, P.Y(0.42) + 18, f"a* − a{sub('0', s)} = {a_s - A0:.1f} yr", "label", I["primary"], "middle"))
        o.append(dot(P, A0, TAU_P / D_N, SER[0], hollow=True))
        o.append(label(s, P.X(A0) + 10, P.Y(TAU_P / D_N) - 10, f"R(a{sub('0', s, 'label2')}) = τ{sub('p', s, 'label2')}/D = {TAU_P / D_N:.2f}", "label2", I["primary"]))
        o.append(label(s, P.x1 - 6, P.Y(1.78), f"a* = a{sub('0', s, 'label2')} + (1/r)(1 − D/τ{sub('p', s, 'label2')})", "label2", I["primary"], "end"))
        o.append(label(s, P.x1 - 6, P.Y(1.5), f"= 40 + 100 × (1 − 0.629) = {a_s:.1f} yr", "label2", I["secondary"], "end"))
        o.append(label(s, P.X(a_s) + 9, P.Y(1) - 9, "R = 1", "label2", I["primary"]))
        aria = ("Problem D1 plot. The reserve R(a) = tau p (1 - r (a - a0)) / D with D = 110, tau p = 175 newton metres, a0 = 40 years, "
                "r = 0.01 per year falls in a straight line from 1.59 at age 40 and crosses the threshold R = 1 at age 77.1. "
                "A double-headed arrow from age 40 to 77.1 marks the interval a star minus a0 = (1/r)(1 - D/tau p) = 37.1 years.")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


def fig21():
    return reserve_plot("m14f21_", False)


def fig31():
    return reserve_plot("m14f31_", True)


# ================================================================ svg #22  C2: strength in the bank
def fig22():
    VB = (0, 0, W, 306)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 40, 382, 215), (110, 260), (40, 150))
    tp = np.arange(110, 260.01, 1.0)
    ast = A0 + (1 - D_N / tp) / RATE
    ceil = A0 + 1 / RATE
    o = [P.axes([(110, "110"), (150, "150"), (200, "200"), (250, "250")], [(v, f"{v}") for v in (40, 60, 80, 100, 120, 140)],
                "", "failure age a* (yr)", grid=(100, 140))]
    o.append(title_xaxis(s, P, "peak strength τ" + sub("p", s) + " (N m)"))
    o.append(label(s, (P.x0 + P.x1) / 2, P.y0 + 57, f"D = 110 N m, a{sub('0', s, 'label2')} = 40 yr, r = 0.01 per yr", "label2", I["secondary"], "middle"))
    o.append(dashed(s, P.x0, P.Y(ceil), P.x1, P.Y(ceil)))
    o.append(P.curve(tp, ast, SER[0]))
    o.append(legend(s, 58, 18, [(SER[0], "a* = a" + sub("0", s, "label2") + " + (1/r)(1 − D/τ" + sub("p", s, "label2") + ")", None)]))
    o.append(label(s, P.x0 + 8, P.Y(ceil) - 8, f"ceiling a{sub('0', s, 'label2')} + 1/r = {ceil:.0f} yr", "label2", I["secondary"]))
    for v, side in ((TAU_P, "ul"), (TAU_P2, "lr")):
        a = astar(v)
        o.append(dot(P, v, a, SER[0]))
        if side == "ul":
            o.append(label(s, P.X(v) - 8, P.Y(a) - 10, f"{v:.0f} N m: {a:.1f} yr", "label2", I["primary"], "end"))
        else:
            o.append(label(s, P.X(v) + 6, P.Y(a) + 22, f"{v:.0f} N m: {a:.1f} yr", "label2", I["primary"]))
    o.append(dot(P, D_N, A0, SER[0], hollow=True))
    aria = ("Problem C2 plot. The failure age a star = 40 + 100 (1 - 110 / tau p) years against peak strength tau p in newton metres, "
            "from 110 to 260. The curve rises steeply and then flattens toward a ceiling at a0 + 1/r = 140 years, drawn as a dashed line. "
            "Marked points: tau p = 175 gives 77.1 years, tau p = 210 gives 87.6 years, and tau p = 110, equal to the demand, gives 40 years.")
    hv = hov(P, tp, [ast], lambda i: f"τp = {tp[i]:.0f} N m: a* = {ast[i]:.1f} yr")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #25  C5: the OA loop
def fig25():
    VB = (0, 0, W, 322)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f25_"
    A = (112, 22, 176, 54)         # thinner
    B = (214, 168, 176, 54)        # higher peak stress
    C = (10, 168, 176, 54)         # more damage
    o = [defs(p, s)]
    o.append(node(s, A, "thinner cartilage", "h falls", T["cartilage"][1]))
    o.append(node(s, B, "higher peak stress", f"p = p{sub('0', s, 'label2')}(h{sub('0', s, 'label2')}/h){sup('n', s, 'label2')}", O["force"]))
    o.append(node(s, C, "faster damage", f"dh/dt ∝ −p", O["flag"]))
    o.append(link(s, p, A, B))
    o.append(link(s, p, B, C))
    o.append(link(s, p, C, A))
    o.append(H.label(s, 200, 128, "positive feedback", "label", I["primary"], "middle"))
    o.append(H.label(s, 200, 146, "runaway", "label2", I["secondary"], "middle"))
    # joint load enters the stress node from below
    o.append(H.arrow(s, p, 352, 290, 352, 226, "load"))
    o.append(H.label(s, 398, 306, "joint load L: weight, alignment", "label2", O["load"], "end"))
    for k, ln in enumerate(("3.0 MPa at 2.0 mm", "4.3 MPa at 1.2 mm", "7.0 MPa at 0.6 mm")):
        o.append(H.label(s, 218, 246 + 16 * k, ln, "label2", I["secondary"]))
    aria = ("Problem C5 diagram. A three-step loop drawn clockwise: thinner cartilage leads to higher peak contact stress, "
            "p = p0 (h0/h) to the power n, which leads to faster damage, dh/dt proportional to minus p, which thins the cartilage "
            "again. The loop is a positive feedback and runs away rather than settling. Joint load L, set by body weight and "
            "alignment, enters at the stress step. Peak stress is 3.0 MPa at 2.0 mm, 4.3 MPa at 1.2 mm and 7.0 MPa at 0.6 mm.")
    return svg(VB, aria, s, "".join(o))


# ================================================================ svg #26  C6: the costly tenth-second
def fig26():
    VB = (0, 0, W, 290)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 40, 382, 215), (0, 0.30), (0, 1.05))
    dt = np.arange(0, 0.3001, 0.005)
    f = np.exp(-W0 * dt)
    o = [P.axes([(0, "0.00"), (0.1, "0.10"), (0.2, "0.20"), (0.3, "0.30")], [(0, "0"), (0.5, "0.5"), (1.0, "1.0")],
                "", "recoverable fraction", grid=(0.5, 1.0))]
    o.append(title_xaxis(s, P, "reaction delay Δt (s)"))
    o.append(P.curve(dt, f, SER[0]))
    o.append(legend(s, 58, 18, [(SER[0], "exp(−ω" + sub("0", s, "label2") + "Δt), ω" + sub("0", s, "label2") + " = 3.1 rad/s", None)]))
    f1, f2 = math.exp(-W0 * 0.12), math.exp(-W0 * 0.20)
    o.append(dot(P, 0.12, f1, SER[0]))
    o.append(dot(P, 0.20, f2, SER[0]))
    o.append(label(s, P.X(0.12) + 9, P.Y(f1) - 10, f"Δt = 0.12 s: {f1:.2f}", "label2", I["primary"]))
    o.append(label(s, P.X(0.20) - 9, P.Y(f2) + 24, f"Δt = 0.20 s: {f2:.2f}", "label2", I["primary"], "end"))
    o.append(label(s, P.x1 - 6, P.Y(1.0) - 4, f"0.12 → 0.20 s: × {f2 / f1:.2f} (−{100 * (1 - f2 / f1):.0f} %)", "label2", I["primary"], "end"))
    o.append(label(s, P.x1 - 6, P.Y(0.1), f"every +0.10 s: × {math.exp(-W0 * 0.1):.2f}", "label2", I["secondary"], "end"))
    aria = ("Problem C6 plot. The recoverable fraction of a perturbation, exp(-omega0 times the reaction delay) with omega0 = 3.1 per second, "
            "against reaction delay from 0 to 0.30 seconds. It falls from 1 to 0.39, with no floor reached. Marked points: 0.69 at 0.12 seconds "
            "and 0.54 at 0.20 seconds, a loss of 22 percent. Every added 0.10 seconds multiplies the fraction by 0.73.")
    hv = hov(P, dt, [f], lambda i: f"Δt = {dt[i]:.3f} s: recoverable fraction {f[i]:.2f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #27  C7: noisy standing
def fig27():
    VB = (0, 0, W, 372)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f27_"
    B_Y, B_A = 0.10, 0.05          # margin b, young and aged (m)
    SIG_Y, SIG_A = 0.010, 0.020    # sway sigma, c = 1 so c sigma = 0.010 and 0.020 m (Lab D code, text line 329-331)
    o = [defs(p, s)]
    # margin budget bar at the young operating point
    x0, x1, by = 58.0, 382.0, 58.0
    ux = (x1 - x0) / B_Y
    xs = x0 + (B_Y - SIG_Y) * ux
    o.append(H.label(s, x0, 22, "margin budget, young: b = 0.10 m", "label", I["primary"]))
    o.append(f'<rect x="{x0:.2f}" y="{by:.2f}" width="{xs - x0:.2f}" height="24" fill="{O["geometry"]}" fill-opacity="0.25" '
             f'stroke="{O["geometry"]}" stroke-width="{s(1):.2f}"/>')
    o.append(f'<rect x="{xs:.2f}" y="{by:.2f}" width="{x1 - xs:.2f}" height="24" fill="{O["flag"]}" fill-opacity="0.45" '
             f'stroke="{O["flag"]}" stroke-width="{s(1):.2f}"/>')
    o.append(H.label(s, (x0 + xs) / 2, by + 17, f"usable b − cσ = {B_Y - SIG_Y:.2f} m", "label2", I["primary"], "middle"))
    o.append(H.label(s, x1, by - 6, f"spent cσ = {SIG_Y:.2f} m", "label2", I["primary"], "end"))
    o.append(H.arrow(s, p, x0, by + 40, x1, by + 40, "geometry", both=True))
    o.append(H.label(s, (x0 + x1) / 2, by + 60, "b (margin to the base edge)", "label2", I["secondary"], "middle"))
    # plot
    P = Plot(s, (58, 166, 382, 312), (0, 0.03), (0, 0.10))
    sg = np.arange(0, 0.03001, 0.0005)
    my, ma = B_Y - sg, B_A - sg
    o.append(P.axes([(0, "0.00"), (0.01, "0.01"), (0.02, "0.02"), (0.03, "0.03")], [(0, "0"), (0.05, "0.05"), (0.10, "0.10")],
                    "", "usable margin b − cσ (m)", grid=(0.05, 0.10)))
    o.append(title_xaxis(s, P, "sensor noise σ (sway amplitude, m)"))
    o.append(P.curve(sg, my, SER[0]))
    o.append(P.curve(sg, ma, SER[1], dash=(7, 4)))
    o.append(legend(s, 58, 152, [(SER[0], "b = 0.10 m (young)", None), (SER[1], "b = 0.05 m (aged)", (7, 4))]))
    o.append(dot(P, SIG_Y, B_Y - SIG_Y, SER[0]))
    o.append(dot(P, SIG_A, B_A - SIG_A, SER[1]))
    o.append(label(s, P.X(SIG_Y) + 9, P.Y(B_Y - SIG_Y) - 10, f"{B_Y - SIG_Y:.2f} m", "label2", I["primary"]))
    o.append(label(s, P.X(SIG_A) - 9, P.Y(B_A - SIG_A) + 24, f"{B_A - SIG_A:.2f} m", "label2", I["primary"], "end"))
    o.append(label(s, P.x0 + 10, P.Y(0.015), "slope −c = −1", "label2", I["secondary"]))
    aria = ("Problem C7 diagram and plot. Top: a bar for the young balance margin b = 0.10 metres, split into the usable part "
            "b minus c sigma = 0.09 metres and the part spent on quiet-standing sway, c sigma = 0.01 metres, with c = 1. "
            "Below: usable margin b minus c sigma against sensor noise sigma from 0 to 0.03 metres, a straight line of slope minus 1, "
            "for b = 0.10 metres (young) and b = 0.05 metres (aged, dashed). Marked points: 0.09 metres at sigma 0.010 for the young "
            "body and 0.03 metres at sigma 0.020 for the aged body.")
    hv = hov(P, sg, [my, ma], lambda i: f"σ = {sg[i]:.4f} m: margin {my[i]:.3f} m (b 0.10), {ma[i]:.3f} m (b 0.05)")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #28  C8: the cascade
def fig28():
    VB = (0, 0, W, 345)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f28_"
    M = (14, 36, 118, 40)
    Bn = (268, 36, 118, 40)
    Ac = (141, 140, 118, 46)
    Ba = (14, 244, 118, 40)
    Fa = (141, 296, 118, 40)       # balance -> fall
    Fr = (268, 244, 118, 40)
    o = [defs(p, s)]
    o.append(node(s, M, "muscle", None, T["muscle"][0]))
    o.append(node(s, Bn, "bone", None, T["bone"][1]))
    o.append(node(s, Ac, "activity", "load on tissue", O["load"]))
    o.append(node(s, Ba, "balance", "controller", T["nerve"][0]))
    o.append(node(s, Fa, "FALL", None, O["force"]))
    o.append(node(s, Fr, "fracture", None, O["force"]))
    o.append(link(s, p, M, Bn))
    o.append(link(s, p, Ac, M))
    o.append(link(s, p, Ac, Bn))
    o.append(link(s, p, Ba, Ac, both=True))
    o.append(link(s, p, Ba, Fa, "force"))
    o.append(link(s, p, Fa, Fr, "force"))
    o.append(link(s, p, Bn, Fr, "force"))
    o.append(link(s, p, Fr, Ac, "force"))
    L2 = lambda x, y, t, a="middle": H.label(s, x, y, t, "label2", I["secondary"], a)  # noqa: E731
    o.append(L2(200, 74, "less pull"))
    o.append(L2(92, 120, "load withdrawn", "middle"))
    o.append(L2(262, 112, "load withdrawn", "end"))
    o.append(L2(60, 206, "precarious: moves less", "start"))
    o.append(L2(250, 224, "immobility", "end"))
    o.append(L2(50, 320, "margin exceeded", "start"))
    o.append(L2(334, 170, "margin", "start"))
    o.append(L2(334, 186, "exceeded", "start"))
    o.append(H.line(s, 10, 12, 34, 12, I["secondary"], "ref"))
    o.append(H.label(s, 40, 16, "drift", "label2", I["primary"]))
    o.append(H.line(s, 100, 12, 124, 12, O["force"], "force"))
    o.append(H.label(s, 130, 16, "fall pivot", "label2", I["primary"]))
    aria = ("Problem C8 network diagram. Six boxes: muscle, bone, activity (load on tissue), balance controller, fall and fracture. "
            "Muscle weakness lowers the pull on bone. Reduced activity withdraws load from both muscle and bone. A precarious "
            "balance controller and reduced activity feed each other. The fall pivot, drawn in red, runs from the balance controller "
            "to a fall, from the fall to a fracture and from bone to the fracture, and the fracture forces immobility, which cuts "
            "activity again. One deficit spreads through the whole coupled network.")
    return svg(VB, aria, s, "".join(o))


# ================================================================ svg #29  C9: reversing years
def fig29():
    VB = (0, 0, W, 520)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f29_"
    o = [defs(p, s)]
    # panel a: twelve weeks of training, strength relative to start (text line 219: 1-2 % per session-week, ~20 % in 12 weeks)
    P = Plot(s, (58, 40, 382, 170), (0, 12), (1.0, 1.26))
    wk = np.arange(0, 12.01, 0.25)
    mid = 1 + 0.20 * wk / 12
    lo, hi = 1 + 0.01 * wk, 1 + 0.02 * wk
    o.append(P.axes([(v, f"{v}") for v in (0, 4, 8, 12)], [(1.0, "1.0"), (1.1, "1.1"), (1.2, "1.2")], "", "strength (start = 1)", grid=(1.1, 1.2)))
    o.append(title_xaxis(s, P, "weeks of resistance training"))
    poly = " ".join(f"{P.X(a):.2f},{P.Y(b):.2f}" for a, b in list(zip(wk, hi)) + list(zip(wk, lo))[::-1])
    o.append(f'<polygon points="{poly}" fill="{SER[1]}" fill-opacity="0.18" stroke="none"/>')
    o.append(P.curve(wk, mid, SER[0]))
    o.append(legend(s, 58, 18, [(SER[0], "+20 % in 12 weeks", None)]))
    o.append(f'<rect x="196" y="9" width="22" height="10" fill="{SER[1]}" fill-opacity="0.18"/>')
    o.append(label(s, 223, 18, "1–2 % per session-week", "label2", I["secondary"]))
    o.append(dot(P, 12, 1.2, SER[0]))
    o.append(label(s, P.X(12) - 9, P.Y(1.2) - 22, "+20 %", "label", I["primary"], "end"))
    hva = hov(P, wk, [mid], lambda i: f"week {wk[i]:.1f}: strength {mid[i]:.3f} (band {lo[i]:.2f} to {hi[i]:.2f})")
    # panel b: the failure age moves 10.5 years, not 20 (text line 219)
    Q = Plot(s, (58, 300, 382, 450), (40, 100), (0, 2.4))
    ag = np.arange(40, 100.01, 0.5)
    r1, r2 = reserve(ag, TAU_P), reserve(ag, TAU_P2)
    a1, a2 = astar(TAU_P), astar(TAU_P2)
    o.append(Q.axes([(v, f"{v}") for v in range(40, 101, 10)], [(0, "0"), (1, "1"), (2, "2")], "", "reserve R", grid=(1, 2)))
    o.append(title_xaxis(s, Q, "age (yr)"))
    o.append(dashed(s, Q.x0, Q.Y(1), Q.x1, Q.Y(1)))
    o.append(Q.curve(ag, r1, SER[0]))
    o.append(Q.curve(ag, r2, SER[1]))
    o.append(legend(s, 58, 278, [(SER[0], "τ" + sub("p", s, "label2") + " = 175 N m", None), (SER[1], "τ" + sub("p", s, "label2") + " = 210 N m", None)]))
    o.append(dot(Q, a1, 1, SER[0]))
    o.append(dot(Q, a2, 1, SER[1]))
    yb = Q.Y(0.45)
    o.append(dashed(s, Q.X(a1), Q.Y(1) + s(7), Q.X(a1), yb))
    o.append(dashed(s, Q.X(a2), Q.Y(1) + s(7), Q.X(a2), yb))
    o.append(H.arrow(s, p, Q.X(a1), yb, Q.X(a2), yb, "geometry", both=True))
    o.append(label(s, (Q.X(a1) + Q.X(a2)) / 2, yb + 17, f"{a2 - a1:.1f} yr", "label", I["primary"], "middle"))
    o.append(label(s, Q.X(a1) - 7, Q.Y(0.12), f"{a1:.1f}", "label2", I["primary"], "end"))
    o.append(label(s, Q.X(a2) + 7, Q.Y(0.12), f"{a2:.1f}", "label2", I["primary"]))
    xv = Q.X(41.5)
    o.append(H.arrow(s, p, xv, Q.Y(float(reserve(41.5, TAU_P))), xv, Q.Y(float(reserve(41.5, TAU_P2))), "geometry", both=True))
    o.append(label(s, xv + 7, Q.Y(2.2), "gap at age 40: +35 N m = 20 yr of 1 %/yr drift", "label2", I["primary"]))
    hvb = hov(Q, ag, [r1, r2], lambda i: f"age {ag[i]:.1f} yr: R {r1[i]:.2f} (175 N m), {r2[i]:.2f} (210 N m)")
    aria = ("Problem C9 plots. Top: strength relative to its start over twelve weeks of resistance training, a straight line to 1.20, "
            "the 20 percent gain, inside a band for gains of 1 to 2 percent per session-week. Bottom: the chair-rise reserve R "
            "against age for peak strength 175 newton metres and, after training, 210 newton metres. The 35 newton metre vertical "
            "gap at age 40 equals twenty years of the 1 percent per year drift, but the failure age, where R = 1, moves only "
            "from 77.1 to 87.6 years, a gain of 10.5 years.")
    return svg(VB, aria, s, "".join(o), ([(P.box, hva), (Q.box, hvb)],))


# ================================================================ svg #30  C10: protect versus load
def fig30():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f30_"
    gx0, gx1 = 140.0, 382.0
    dec = (gx1 - gx0) / 3.0                       # three decades across the axis
    pos = {"muscle": 2.85, "bone": 2.45, "cartilage": 0.55}   # decades above the left edge; ordering only
    rows = [("muscle", "reload", 60, T["muscle"]), ("bone", "reload", 120, T["bone"]), ("cartilage", "protect", 180, T["cartilage"])]
    o = [defs(p, s)]
    for k in range(4):
        x = gx0 + k * dec
        o.append(H.line(s, x, 36, x, 206, GRID, "leader"))
    o.append(H.line(s, gx0, 206, gx1, 206, I["axis"], "axis"))
    o.append(H.label(s, gx0, 224, "slower", "label2", I["secondary"], "start"))
    o.append(H.label(s, gx1, 224, "faster", "label2", I["secondary"], "end"))
    o.append(H.label(s, (gx0 + gx1) / 2, 246, f"adaptation rate k{sub('ad', s)} (log scale)", "label", I["primary"], "middle"))
    o.append(H.label(s, (gx0 + gx1) / 2, 18, "gridlines are decades; positions show order only", "label2", I["secondary"], "middle"))
    for name, msg, y, c in rows:
        x = gx0 + pos[name] * dec
        o.append(H.label(s, 14, y + 2, name, "label", I["primary"]))
        o.append(H.label(s, 14, y + 19, msg, "label2", I["secondary"]))
        o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(9):.2f}" fill="{c[0]}" stroke="{c[1]}" stroke-width="{s(1.6):.2f}"/>')
    xm, xc = gx0 + pos["bone"] * dec, gx0 + pos["cartilage"] * dec
    o.append(H.arrow(s, p, xm - 2, 150, xc + 2, 150, "geometry", both=True))
    o.append(H.label(s, (xm + xc) / 2 - 30, 143, "orders of magnitude", "label2", I["primary"], "middle"))
    aria = ("Problem C10 dot plot on a log axis, positions illustrative of order only. Muscle and bone sit at high adaptation rate "
            "k ad, labelled reload. Cartilage sits orders of magnitude lower, labelled protect. A double-headed arrow spans the "
            "gap between bone and cartilage. The module gives no k ad values for muscle or cartilage.")
    return svg(VB, aria, s, "".join(o))


# ================================================================ svg #32  D2: the squared law
def fig32():
    VB = (0, 0, W, 290)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 40, 382, 215), (50, 100), (0, 100))
    rho = np.arange(50, 100.01, 1.0)
    S2 = 100 * (rho / 100) ** N_B
    S1 = rho
    o = [P.axes([(50, "50"), (75, "75"), (100, "100")], [(0, "0"), (50, "50"), (100, "100")], "", f"strength S (% of S{sub('0', s)})", grid=(50, 100))]
    o.append(title_xaxis(s, P, "bone density ρ (% of ρ" + sub("0", s) + ")"))
    o.append(P.curve(rho, S1, SER[1], dash=(7, 4)))
    o.append(P.curve(rho, S2, SER[0]))
    o.append(legend(s, 58, 18, [(SER[0], "S ∝ ρ² (n = 2)", None), (SER[1], "S ∝ ρ (reference)", (7, 4))]))
    for r in (80, 60):
        v = 100 * (r / 100) ** N_B
        o.append(dot(P, r, v, SER[0]))
        o.append(label(s, P.X(r) + 9, P.Y(v) + 20, f"{r} % → {v:.0f} %", "label2", I["primary"]))
    o.append(label(s, P.x0 + 8, P.Y(93), "dS/S = n dρ/ρ, n = 2", "label2", I["primary"]))
    o.append(label(s, P.x1 - 6, P.Y(6), "20 % less density: 36 % less strength", "label2", I["primary"], "end"))
    aria = ("Problem D2 plot. Bone strength S as a percentage of its young value against bone density from 50 to 100 percent, "
            "for S proportional to density squared (solid) and, as a reference, proportional to density (dashed). "
            "Marked points: 80 percent density gives 64 percent strength, a 36 percent loss, and 60 percent density gives 36 percent strength. "
            "The log derivative is dS/S = 2 d rho / rho.")
    hv = hov(P, rho, [S2, S1], lambda i: f"ρ = {rho[i]:.0f} %: S = {S2[i]:.0f} % (n 2), {S1[i]:.0f} % (n 1)")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #34  D4: cartilage stress
def fig34():
    VB = (0, 0, W, 478)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m14f34_"
    P = Plot(s, (58, 40, 382, 200), (0.4, 2.0), (0, 9.5))
    h = np.arange(0.4, 2.0001, 0.02)
    pk = P0 * (H0 / h) ** N_C
    o = [defs(p, s)]
    o.append(P.axes([(0.5, "0.5"), (1.0, "1.0"), (1.5, "1.5"), (2.0, "2.0")], [(v, f"{v}") for v in (0, 2, 4, 6, 8)],
                    "", "peak stress (MPa)", grid=(4, 8)))
    o.append(title_xaxis(s, P, "cartilage thickness h (mm)"))
    o.append(P.curve(h, pk, SER[0]))
    o.append(label(s, P.x1 - 6, P.Y(8.9), f"p = p{sub('0', s, 'label2')}(h{sub('0', s, 'label2')}/h){sup('n', s, 'label2')}, n = 0.7", "label2", I["primary"], "end"))
    o.append(label(s, P.x1 - 6, P.Y(8.0) + 2, f"p{sub('0', s, 'label2')} = 3 MPa at h{sub('0', s, 'label2')} = 2 mm", "label2", I["secondary"], "end"))
    for hh, side in ((2.0, "ul"), (1.2, "ur"), (0.6, "ur")):
        v = P0 * (H0 / hh) ** N_C
        o.append(dot(P, hh, v, SER[0]))
        if side == "ul":
            o.append(label(s, P.X(hh) - 9, P.Y(v) - 12, f"{v:.1f}", "label2", I["primary"], "end"))
        else:
            o.append(label(s, P.X(hh) + 9, P.Y(v) - 12, f"{v:.1f}", "label2", I["primary"]))
    hv = hov(P, h, [pk], lambda i: f"h = {h[i]:.2f} mm: peak stress {pk[i]:.1f} MPa")
    # cross-sections: contact area A proportional to h^n (text line 138-140 and D4 solution)
    SC = 24.0                        # user units per mm of cartilage, so the layer thickness is to scale
    R = 70.0
    ys = 330.0
    base = 82.0
    for cx, hh, tag in ((110.0, 2.0, "healthy"), (290.0, 0.6, "thinned")):
        ratio = (hh / H0) ** N_C
        a = 36.0 * math.sqrt(ratio)
        ht = hh * SC
        pv = P0 * (H0 / hh) ** N_C
        dy = math.sqrt(R * R - a * a)
        yt = ys - 38.0
        xe = math.sqrt(R * R - (dy - 38.0) ** 2)
        yi = ys + ht
        yb = ys + base
        # bone: interface at yi, wavy lower edge, marrow pores
        bone = (f'M{cx - 75:.1f},{yi:.1f} L{cx + 75:.1f},{yi:.1f} L{cx + 75:.1f},{yb:.1f} '
                f'C{cx + 45:.1f},{yb + 6:.1f} {cx + 20:.1f},{yb - 6:.1f} {cx:.1f},{yb:.1f} '
                f'C{cx - 25:.1f},{yb + 6:.1f} {cx - 50:.1f},{yb - 6:.1f} {cx - 75:.1f},{yb:.1f} Z')
        o.append(f'<path d="{bone}" fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="{s(1.2):.2f}"/>')
        for dx, dyy, rx in ((-46, 14, 9), (-10, 22, 7), (26, 12, 8), (52, 24, 6), (-60, 28, 5)):
            if yi + dyy < yb - 6:
                o.append(f'<ellipse cx="{cx + dx}" cy="{yi + dyy:.1f}" rx="{rx}" ry="{rx * 0.55:.1f}" fill="{T["marrow"][0]}" stroke="{T["marrow"][1]}" stroke-width="{s(0.8):.2f}"/>')
        o.append(f'<rect x="{cx - 75:.1f}" y="{ys:.1f}" width="150" height="{ht:.1f}" fill="{T["cartilage"][0]}" stroke="{T["cartilage"][1]}" stroke-width="{s(1.2):.2f}"/>')
        # condyle (bone-coloured cap) pressing on the surface; its lower arc dips below the surface by R - dy
        cap = f'M{cx - xe:.1f},{yt:.1f} A{R},{R} 0 0 0 {cx + xe:.1f},{yt:.1f} Z'
        o.append(f'<path d="{cap}" fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="{s(1.4):.2f}"/>')
        o.append(H.arrow(s, p, cx, yt - 24, cx, yt - 2, "load"))
        o.append(H.label(s, cx + 8, yt - 12, "P", "label", O["load"]))
        # contact chord and thickness dimension
        o.append(H.line(s, cx - a, ys, cx + a, ys, O["geometry"], "geom"))
        if hh == 2.0:
            o.append(H.label(s, cx, ys + ht / 2 + 5, "cartilage", "label2", I["secondary"], "middle"))
            o.append(H.label(s, cx + 8, yi + 30, "bone", "label2", I["secondary"], "start"))
            o.append(H.label(s, cx, yt + 20, "femoral condyle", "label2", I["secondary"], "middle"))
        o.append(H.label(s, cx, yb + 24, f"{tag}: h = {hh:.1f} mm", "label2", I["primary"], "middle"))
        o.append(H.label(s, cx, yb + 40, f"A × {ratio:.2f}, p = {pv:.1f} MPa", "label2", I["primary"], "middle"))
    aria = ("Problem D4 plot and cross-sections. Peak contact stress p = 3 (2/h) to the power 0.7 MPa against cartilage thickness h "
            "from 0.4 to 2.0 millimetres, rising as the layer thins: 3.0 MPa at 2.0 mm, 4.3 MPa at 1.2 mm and 7.0 MPa at 0.6 mm. "
            "Below: two cross-sections of a bone-coloured condyle loaded by a force P on a cartilage layer over bone. The healthy layer "
            "(2.0 mm) has the full contact area and 3.0 MPa. The thinned layer (0.6 mm, drawn to the same scale) has contact area "
            "scaled by 0.43, so the same load gives 7.0 MPa.")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


FIGS = {
    21: ("C1: the sudden cliff. Muscle and bone decline smoothly at ab", fig21),
    22: ("C2: strength in the bank. Why is peak strength attained in y", fig22),
    25: ("C5: why it accelerates. Osteoarthritis, once it begins, spee", fig25),
    26: ("C6: the costly tenth-second. Why does a modest slowing of re", fig26),
    27: ("C7: noisy standing. Why does losing sensory acuity cost bala", fig27),
    28: ("C8: the cascade. Why does a single deficit - or a single fal", fig28),
    29: ("C9: reversing years. How can twelve weeks of resistance trai", fig29),
    30: ("C10: protect versus load. Why is the right advice 'load it' ", fig30),
    31: ("D1: the failure age. Derive the age at which a declining str", fig31),
    32: ("D2: the squared law. Derive the fractional strength change f", fig32),
    34: ("D4: cartilage stress. Argue why peak contact stress rises as", fig34),
}
