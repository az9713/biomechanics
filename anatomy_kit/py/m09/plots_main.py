"""Module 9 plots in the house style (group `plots_main`): main text #4, #8, #11, #12, #13, #14 and
problem figures #21 (C3), #27 (C9), #28 (C10), #29 (D1), #35 (D7), #37 (D9).

Every plotted number is computed here from what module09.html states:
  duty factor (Prop. 1.2, caption line 77), the symmetric SLIP stance of section 5 (Lab 1's integrator, line 194),
  Lab 4 (U, R; line 242), the oxidative ceiling and phosphocreatine capacity (lines 277-281), Lab 3 / Prop. 8.1
  (line 296), Prop. 9.1 (line 316), K9's Basquin law (line 557), Module 6 K2's toe tendon (5 kN point, line 234)
  and Module 8 Lab 3's walking template (C3).
The text's printed values are asserted where they are computed.
"""
import html
import math
from functools import lru_cache

import numpy as np

import house as H
import lynch_body as LB
from m05.plots_main import Ax, axes, curve, dot, legend, pts_str, tw, DASH_SER
from m05.plots_prob import Plot, label as plabel, legend as plegend

T_, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"
BOXFILL = "#f7f4ef"
M, G = 70.0, 9.81                         # kg, m/s^2 (Labs 1-3)
BW = M * G


def svg(vb, aria, s, body, extra=""):
    return H.svg_open(vb, html.escape(aria), s, extra=extra) + "".join(body) + "</svg>"


def sub(t, s, size="label2"):
    return H.sub(t, s, size)


def onfill(s, x, y, text):
    """White text on a solid bar: no halo (a white halo would bloat it)."""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-size="{s(H.PX["label2"]):.2f}" fill="#fff" '
            f'text-anchor="middle">{text}</text>')


def box(ax):
    return [round(v, 2) for v in ax.box]


def r2(v):
    return round(float(v), 2)


# ================================================================ models
@lru_cache(maxsize=None)
def slip_sym():
    """Lab 1's slip_stance (symplectic Euler, dt = 1e-4), extended to record the horizontal GRF.
    Section 5 (line 194) gives the run only by its result: symmetric, t_c = 0.169 s, v_y = 0.479 m/s.
    With Lab 1's v_x = 4.0 m/s the leg stiffness and angle of attack below were solved (root-finding, outside this
    file) so that takeoff mirrors touchdown and t_c = 0.169 s; the asserts check the text's impulse split."""
    k, alpha, vx0, vy0, L0, dt = 18625.0, 70.6883, 4.0, -0.479, 1.0, 1e-4
    a = math.radians(alpha)
    x, y, vx, vy = -L0 * math.cos(a), L0 * math.sin(a), vx0, vy0
    t, T, Fz, Fx = 0.0, [], [], []
    while True:
        r = math.hypot(x, y)
        F = k * (L0 - r)
        ax_, ay_ = F * x / r / M, F * y / r / M - G
        T.append(t)
        Fz.append(F * y / r)
        Fx.append(F * x / r)
        vx, vy = vx + ax_ * dt, vy + ay_ * dt
        x, y = x + vx * dt, y + vy * dt
        t += dt
        if math.hypot(x, y) >= L0 and t > 5 * dt:
            break
        if y <= 0 or t > 2.0:
            break
    T, Fz, Fx = np.array(T), np.array(Fz), np.array(Fx)
    tc, J = T[-1], float(np.trapezoid(Fz, T))
    assert abs(vy - 0.479) < 5e-4 and abs(vx - 4.0) < 1e-3, (vx, vy)
    assert round(tc, 3) == 0.169 and round(J, 1) == 183.2, (tc, J)                       # line 194
    assert round(M * G * tc, 1) == 116.1 and round(2 * M * 0.479, 1) == 67.1
    return T, Fz, Fx, tc, J


def walk_template(s):
    """Module 8 Lab 3's assumed walking F_y shape over stance fraction s, in body weights
    (peaks 1.10 W at 28 % and 72 %, trough 0.75 W at midstance; module08 text)."""
    sh = np.sin(np.pi * s) ** 0.40 * (1 - 0.245 * np.cos(4 * np.pi * (s - 0.5)))
    ss = np.linspace(0, 1, 6001)
    norm = np.trapezoid(np.sin(np.pi * ss) ** 0.40 * (1 - 0.245 * np.cos(4 * np.pi * (ss - 0.5))), ss)
    return sh / (2 * 0.62 * norm)                        # Fy = shape (W T/2) / int(shape dt), T_st = 0.62 T


# Prop. 9.1, section 9 values (line 316)
M_IMP, V_IMP = 8.0, 1.0
K_STIFF, K_SOFT = 2.0e5, 4.0e4


def impact(kc):
    """(peak N, rise time s, mean loading rate BW/s, omega) of the mass on the contact spring."""
    pk = V_IMP * math.sqrt(kc * M_IMP)
    tr = math.pi / 2 * math.sqrt(M_IMP / kc)
    return pk, tr, pk / tr / BW, math.sqrt(kc / M_IMP)


_ps, _ts, _ls, _ = impact(K_STIFF)
_pf, _tf, _lf, _ = impact(K_SOFT)
assert round(_ps) == 1265 and round(_ps / BW, 1) == 1.8 and round(_ts * 1e3, 1) == 9.9 and round(_ls) == 185
assert round(_pf) == 566 and round(_pf / BW, 1) == 0.8 and round(_tf * 1e3, 1) == 22.2 and round(_lf) == 37

# K9's Basquin law (line 557): N = N0 (s0/s)^(1/b); "tolerance" = the stress that fails in one load (N = 1)
N0, S0, B_BAS = 1e4, 60.0, 0.12
S_TOL = S0 * N0 ** B_BAS
assert round(N0 * (S0 / 45) ** (1 / B_BAS) / 1e5, 2) == 1.10 and round(N0 * (S0 / 50) ** (1 / B_BAS) / 1e4, 1) == 4.6


def n_fail(f):
    """Cycles to failure at a per-step load f = stress / tolerance."""
    return f ** (-1 / B_BAS)


# Module 6 K2 toe tendon (k_lin, x*), evaluated at the 5 kN running push-off (line 234)
K_LIN, X_STAR = 4.16e5, 0.0075


def f_toe(x):
    return np.where(x <= X_STAR, K_LIN * x ** 2 / (2 * X_STAR), K_LIN * (x - X_STAR / 2))


def tendon_U(F_pk):
    xm = F_pk / K_LIN + X_STAR / 2
    g = np.linspace(0, xm, 200001)
    return xm, float(np.trapezoid(f_toe(g), g))


_x4, _u4 = tendon_U(4000.0)
assert round(_x4 * 1e3, 2) == 13.37 and round(_u4, 2) == 20.21                         # Module 6 K2
X5, U_T = tendon_U(5000.0)
assert round(X5 * 1e3) == 16 and round(U_T) == 31                                       # line 234
R_T = 0.92                                                                              # Lab 4


@lru_cache(maxsize=None)
def unload_p():
    """Unloading branch F_toe(x) (x/xm)^p: closes the loop at 0 and at the peak; p solved so it returns R U."""
    g = np.linspace(0, X5, 20001)
    lo, hi = 0.0, 5.0
    for _ in range(80):
        p = (lo + hi) / 2
        if np.trapezoid(f_toe(g) * (g / X5) ** p, g) > R_T * U_T:
            lo = p
        else:
            hi = p
    return (lo + hi) / 2


# ================================================================ #4 and #29: running-gait timeline
TC, TF = 0.20, 0.10                        # jogging values, caption line 77
T_STR = 2 * (TC + TF)
BETA = TC / T_STR
assert abs(T_STR - 0.60) < 1e-12 and abs(BETA - 1 / 3) < 1e-12


def phase(pc):
    """(right on ground, left on ground) at pc percent of stride (R touchdown at 0)."""
    t = pc / 100 * T_STR % T_STR
    return t < TC, TC + TF <= t < 2 * TC + TF


def fig4():
    VB = (0, 0, 760, 268)
    s = H.Scale(VB[2], VB[3])
    p = "m9f4_"
    x0, x1 = 120, 735
    X = lambda pc: x0 + pc / 100 * (x1 - x0)           # noqa: E731
    yr, yl, bh = 76, 122, 24                           # top of the right / left stance bars
    yb, ya = 182, 208                                  # dimension row, axis
    pr, pl = 100 * TC / T_STR, 100 * (TC + TF) / T_STR
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    for a, b in ((pr, pl), (100 * (2 * TC + TF) / T_STR, 100.0)):
        o.append(f'<rect x="{X(a):.2f}" y="60" width="{X(b) - X(a):.2f}" height="{yb - 14 - 60}" fill="{GRID}"/>')
        o.append(H.label(s, (X(a) + X(b)) / 2, 54, "flight", "label2", I["primary"], "middle"))
    o.append(f'<rect x="{X(0):.2f}" y="{yr}" width="{X(pr) - X(0):.2f}" height="{bh}" fill="{SER[0]}"/>')
    o.append(f'<rect x="{X(pl):.2f}" y="{yl}" width="{X(100 * (2 * TC + TF) / T_STR) - X(pl):.2f}" height="{bh}" fill="{SER[1]}"/>')
    o.append(H.label(s, x0 - 12, yr + 17, "right foot", "label2", I["primary"], "end"))
    o.append(H.label(s, x0 - 12, yl + 17, "left foot", "label2", I["primary"], "end"))
    o.append(onfill(s, X(pr / 2), yr + 17, "stance"))
    o.append(onfill(s, X((pl + 100 * (2 * TC + TF) / T_STR) / 2), yl + 17, "stance"))
    o.append(H.label(s, X((pl + 100 * (2 * TC + TF) / T_STR) / 2), yr + 17, "swing", "label2", I["muted"], "middle"))
    o.append(H.label(s, X(pr / 2), yl + 17, "swing", "label2", I["muted"], "middle"))
    # touchdown / toe-off ticks
    for pc, yy in ((0, yr), (pr, yr), (pl, yl), (100 * (2 * TC + TF) / T_STR, yl)):
        o.append(H.line(s, X(pc), yy - 5, X(pc), yy + bh + 5, I["axis"], "ref"))
    # contact and flight times as dimensions
    o.append(H.arrow(s, p, X(0) + 1, yb, X(pr) - 1, yb, "dim", both=True))
    o.append(H.arrow(s, p, X(pr) + 1, yb, X(pl) - 1, yb, "dim", both=True))
    o.append(H.label(s, X(pr / 2), yb - 9, f'contact t{sub("c", s)} = {TC:.2f} s', "label2", I["primary"], "middle"))
    o.append(H.label(s, X((pr + pl) / 2), yb - 9, f't{sub("f", s)} = {TF:.2f} s', "label2", I["primary"], "middle"))
    o.append(H.label(s, X(pl) + 8, yb + 5, f'stride T = 2(t{sub("c", s)} + t{sub("f", s)}) = {T_STR:.2f} s', "label2", I["secondary"]))
    # axis: percent of stride, with seconds under it
    o.append(H.line(s, x0, ya, x1, ya, I["axis"], "axis"))
    for pc in (0, 25, 50, 75, 100):
        o.append(H.line(s, X(pc), ya, X(pc), ya + 5, I["axis"], "leader"))
        o.append(H.label(s, X(pc), ya + 20, f"{pc}", "tick", I["secondary"], "middle"))
    o.append(H.label(s, (x0 + x1) / 2, ya + 44, "percent of stride (right touchdown to the next right touchdown)", "label",
                     I["primary"], "middle"))
    o.append(H.label(s, 20, 24, f'duty factor β = t{sub("c", s)}/T = {TC:.2f}/{T_STR:.2f} = 1/3 &lt; 1/2: each foot is down '
                     'for a third of the stride', "label", I["primary"]))
    aria = ("Running-gait timeline over one stride of 0.60 s, in percent of stride. The right foot is on the ground (red "
            "bar) from 0 to 33 percent, the left foot (blue bar) from 50 to 83 percent; between the stances are two flight "
            "phases, 33 to 50 and 83 to 100 percent, shaded grey, when neither foot is down. Dimension lines mark the "
            "contact time 0.20 s and the flight time 0.10 s; the duty factor is 0.20/0.60 = 1/3, below 1/2.")
    hv = []
    for i in range(201):
        pc = i / 2
        rr, ll = phase(pc)
        st = "flight" if not (rr or ll) else ("right stance" if rr else "left stance")
        hv.append([r2(X(pc)), r2(yr + bh / 2 if rr else (yl + bh / 2 if ll else 100)),
                   f"{pc:.1f} % of stride (t = {pc / 100 * T_STR:.3f} s): {st}"])
    return svg(VB, aria, s, o, H.hover_attr([x0, 60, x1, yb], hv))


def fig29():
    W = 400
    VB = (0, 0, W, 220)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m9f29_"
    x0, x1 = 64, 390
    X = lambda pc: x0 + pc / 100 * (x1 - x0)           # noqa: E731
    pr, pl, pe = 100 * TC / T_STR, 100 * (TC + TF) / T_STR, 100 * (2 * TC + TF) / T_STR
    yr, yl, bh, yb = 44, 82, 20, 136
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    for a, b in ((pr, pl), (pe, 100.0)):
        o.append(f'<rect x="{X(a):.2f}" y="34" width="{X(b) - X(a):.2f}" height="{yb - 10 - 34}" fill="{GRID}"/>')
        o.append(plabel(s, (X(a) + X(b)) / 2, 28, "flight", "label2", I["primary"], "middle"))
    o.append(f'<rect x="{X(0):.2f}" y="{yr}" width="{X(pr) - X(0):.2f}" height="{bh}" fill="{SER[0]}"/>')
    o.append(f'<rect x="{X(pl):.2f}" y="{yl}" width="{X(pe) - X(pl):.2f}" height="{bh}" fill="{SER[1]}"/>')
    o.append(plabel(s, x0 - 8, yr + 15, "right", "label2", I["primary"], "end"))
    o.append(plabel(s, x0 - 8, yl + 15, "left", "label2", I["primary"], "end"))
    o.append(onfill(s, X(pr / 2), yr + 15, "stance"))
    o.append(onfill(s, X((pl + pe) / 2), yl + 15, "stance"))
    o.append(H.arrow(s, p, X(0) + 1, yb, X(pr) - 1, yb, "dim", both=True))
    o.append(H.arrow(s, p, X(pr) + 1, yb, X(pl) - 1, yb, "dim", both=True))
    o.append(plabel(s, X(pr / 2), yb - 8, f't{sub("c", s)}', "label", I["primary"], "middle", 'font-style="italic"'))
    o.append(plabel(s, X((pr + pl) / 2), yb - 8, f't{sub("f", s)}', "label", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.arrow(s, p, X(0) + 1, yb + 28, X(100) - 1, yb + 28, "dim", both=True))
    o.append(plabel(s, X(62), yb + 18, f'stride T = 2(t{sub("c", s)} + t{sub("f", s)})', "label2", I["primary"], "middle"))
    o.append(plabel(s, W / 2, 208, f'β = t{sub("c", s, "label")}/T = t{sub("c", s, "label")} / [2(t{sub("c", s, "label")} + t{sub("f", s, "label")})]',
                    "label", I["primary"], "middle"))
    aria = ("Problem D1 figure: a running-gait timeline over one stride. The right-foot stance bar (red) and the left-foot "
            "stance bar (blue) are separated by flight gaps (grey) when neither foot is down. Dimension lines mark the "
            "contact time tc, the flight time tf and the stride T = 2(tc + tf); the duty factor is beta = tc / [2(tc + tf)].")
    hv = []
    for i in range(201):
        pc = i / 2
        rr, ll = phase(pc)
        hv.append([r2(X(pc)), r2(yr + bh / 2 if rr else (yl + bh / 2 if ll else 70)),
                   f"{pc:.1f} % of stride: " + ("flight" if not (rr or ll) else ("right stance" if rr else "left stance"))])
    return svg(VB, aria, s, o, H.hover_attr([x0, 34, x1, yb], hv))


# ================================================================ #8: impulse and momentum over one stance
def fig8():
    VB = (0, 0, 760, 470)
    s = H.Scale(VB[2], VB[3])
    p = "m9f8_"
    T, Fz, Fx, tc, J = slip_sym()
    ms = T * 1e3
    fz, fx = Fz / BW, Fx / BW
    A = Ax((90, 64, 735, 258), (0, 175), (0, 2.75))
    B = Ax((90, 318, 735, 418), (0, 175), (-0.4, 0.4))
    k = np.arange(0, len(T), 20).tolist() + [len(T) - 1]
    jw, jm = M * G * tc, 2 * M * 0.479
    half = int(np.argmin(np.abs(T - tc / 2)))
    jb, jp = float(np.trapezoid(Fx[:half + 1], T[:half + 1])), float(np.trapezoid(Fx[half:], T[half:]))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    # top: impulse area, weight rectangle (grey), curve
    o.append(f'<polygon points="{pts_str([(A.X(ms[i]), A.Y(fz[i])) for i in k] + [(A.X(ms[-1]), A.Y(0)), (A.X(0), A.Y(0))])}" '
             f'fill="{SER[0]}" opacity="0.13"/>')
    o.append(f'<rect x="{A.X(0):.2f}" y="{A.Y(1):.2f}" width="{A.X(ms[-1]) - A.X(0):.2f}" height="{A.Y(0) - A.Y(1):.2f}" '
             f'fill="#cfcfcf" opacity="0.75"/>')
    o += axes(s, A, [(v, "") for v in range(0, 176, 25)], [(v, f"{v:g}") for v in (0, 1, 2)], None,
              f'F{sub("z", s, "label")} (body weights)', ylab_x=40)
    o.append(H.line(s, A.x0, A.Y(1), A.x1, A.Y(1), I["secondary"], "ref", H.DASH_REF))
    o.append(curve(s, A, [ms[i] for i in k], [fz[i] for i in k], SER[0]))
    o.append(H.label(s, A.x1 - 2, A.Y(1) - 6, "mg", "label2", I["secondary"], "end"))
    o.append(H.label(s, A.X(tc * 500), A.Y(0.42), f'weight support mg·t{sub("c", s)} = {jw:.1f} N·s', "label2", I["primary"], "middle"))
    o.append(H.label(s, A.X(tc * 500), A.Y(1.55), f'momentum reversal 2m v{sub("y", s)} = {jm:.1f} N·s', "label2", I["primary"], "middle"))
    o.append(H.label(s, A.X(tc * 500), A.Y(fz.max()) - 10, f'vertical impulse ∫F{sub("z", s)} dt = {J:.1f} N·s (shaded)',
                     "label2", I["primary"], "middle"))
    # vertical velocity at touchdown and takeoff
    o.append(H.arrow(s, p, A.X(8), A.Y(2.3), A.X(8), A.Y(1.6), "geometry"))
    o.append(H.label(s, A.X(8) + 8, A.Y(2.3) + 4, f'v{sub("y", s)} = −0.479 m/s', "label2", I["primary"]))
    o.append(H.label(s, A.X(8) + 8, A.Y(2.3) + 20, "at touchdown", "label2", I["secondary"]))
    o.append(H.arrow(s, p, A.X(161), A.Y(1.6), A.X(161), A.Y(2.3), "geometry"))
    o.append(H.label(s, A.X(161) - 8, A.Y(2.3) + 4, f'v{sub("y", s)} = +0.479 m/s', "label2", I["primary"], "end"))
    o.append(H.label(s, A.X(161) - 8, A.Y(2.3) + 20, "at takeoff", "label2", I["secondary"], "end"))
    o.append(H.label(s, A.x0, 30, f'Vertical: the GRF holds the body up and reverses its fall (t{sub("c", s)} = {tc * 1e3:.0f} ms, m = 70 kg)',
                     "label2", I["primary"]))
    # bottom: horizontal GRF, braking then propulsive
    o.append(f'<polygon points="{pts_str([(B.X(ms[i]), B.Y(fx[i])) for i in k if i <= half] + [(B.X(ms[half]), B.Y(0)), (B.X(0), B.Y(0))])}" '
             f'fill="{SER[1]}" opacity="0.16"/>')
    o.append(f'<polygon points="{pts_str([(B.X(ms[half]), B.Y(0))] + [(B.X(ms[i]), B.Y(fx[i])) for i in k if i >= half] + [(B.X(ms[-1]), B.Y(0))])}" '
             f'fill="{SER[1]}" opacity="0.16"/>')
    o += axes(s, B, [(v, f"{v}") for v in range(0, 176, 25)], [(-0.4, "−0.4"), (0, "0"), (0.4, "0.4")],
              "time from touchdown (ms)", f'F{sub("x", s, "label")} (BW)', ylab_x=40, grid=False)
    o.append(H.line(s, B.x0, B.Y(0), B.x1, B.Y(0), I["secondary"], "leader"))
    o.append(curve(s, B, [ms[i] for i in k], [fx[i] for i in k], SER[1]))
    o.append(H.label(s, B.X(42), B.Y(-0.12), f"braking −{-jb:.1f} N·s", "label2", I["primary"], "middle"))
    o.append(H.label(s, B.X(127), B.Y(0.10), f"propulsive +{jp:.1f} N·s", "label2", I["primary"], "middle"))
    o.append(H.label(s, B.x0, 296, f"Horizontal: brake, then propel; net {jb + jp:.2f} N·s ≈ 0, so the forward speed is unchanged",
                     "label2", I["primary"]))
    aria = (f"Two panels over one symmetric SLIP running stance of {tc * 1e3:.0f} ms. Top: the vertical ground reaction in "
            f"body weights, a single hump peaking at {fz.max():.2f}. Its shaded area, the vertical impulse {J:.1f} N s, splits "
            f"into the grey weight-support rectangle mg times tc = {jw:.1f} N s and the excess {jm:.1f} N s = 2 m vy that turns "
            "the vertical velocity from 0.479 m/s downward at touchdown to 0.479 m/s upward at takeoff (blue arrows). "
            f"Bottom: the horizontal ground reaction is negative (braking, {jb:.1f} N s) in the first half and positive "
            f"(propulsive, {jp:.1f} N s) in the second; the two lobes cancel.")
    hk = list(range(0, len(T), 15)) + [len(T) - 1]
    hv = H.hover_attr([
        (box(A), [[r2(A.X(ms[i])), r2(A.Y(fz[i])), f"t = {ms[i]:.0f} ms: Fz = {fz[i]:.2f} BW ({Fz[i]:.0f} N)"] for i in hk]),
        (box(B), [[r2(B.X(ms[i])), r2(B.Y(fx[i])), f"t = {ms[i]:.0f} ms: Fx = {fx[i]:+.2f} BW ({Fx[i]:+.0f} N)"] for i in hk])])
    return svg(VB, aria, s, o, hv)


# ================================================================ #11: muscle work per step
def fig11():
    VB = (0, 0, 760, 366)
    s = H.Scale(VB[2], VB[3])
    U, R = 31.0, R_T                                    # Lab 4
    w_rig, w_el, back = 2 * U, (1 - R) * U, R * U
    assert round(w_rig) == 62 and round(w_el, 1) == 2.5 and round(back, 1) == 28.5 and round(w_rig / w_el) == 25
    ax = Ax((110, 50, 600, 280), (0, 2), (0, 70))
    o = axes(s, ax, [], [(v, f"{v}") for v in range(0, 71, 10)], None, "muscle mechanical work per step (J)", ylab_x=46)
    xa, xb, bw = ax.X(0.5), ax.X(1.5), 144
    o.append(f'<rect x="{xa - bw / 2:.2f}" y="{ax.Y(w_rig):.2f}" width="{bw}" height="{ax.y0 - ax.Y(w_rig):.2f}" fill="{SER[0]}"/>')
    o.append(f'<rect x="{xb - bw / 2:.2f}" y="{ax.Y(w_el):.2f}" width="{bw}" height="{ax.y0 - ax.Y(w_el):.2f}" fill="{SER[0]}"/>')
    o.append(f'<rect x="{xb - bw / 2:.2f}" y="{ax.Y(U):.2f}" width="{bw}" height="{ax.Y(w_el) - ax.Y(U):.2f}" fill="{BOXFILL}" '
             f'stroke="{O["dim"]}" stroke-width="{s(1.2):.2f}" stroke-dasharray="{s(5):.2f} {s(3):.2f}"/>')
    o.append(H.label(s, xa, ax.Y(w_rig) - 9, f"2U = {w_rig:.0f} J", "label", I["primary"], "middle"))
    o.append(H.label(s, xb + bw / 2 + 10, ax.Y(w_el) - 3, f"(1 − R)U = {w_el:.1f} J", "label2", I["primary"]))
    o.append(H.label(s, xb + bw / 2 + 10, ax.Y(w_el) - 19, "muscle work: the loss", "label2", I["secondary"]))
    o.append(H.label(s, xb, ax.Y((U + w_el) / 2) - 4, f"R·U = {back:.1f} J", "label2", I["primary"], "middle"))
    o.append(H.label(s, xb, ax.Y((U + w_el) / 2) + 13, "returned by the tendon", "label2", I["secondary"], "middle"))
    o.append(H.label(s, xb, ax.Y(U) - 9, f"U = {U:.0f} J cycled by the leg spring", "label2", I["secondary"], "middle"))
    for xc, a, b in ((xa, "rigid leg", "muscle absorbs U, then regenerates U"),
                     (xb, "elastic tendon, R = 0.92", "muscle supplies only the loss")):
        o.append(H.label(s, xc, ax.y0 + 22, a, "label2", I["primary"], "middle"))
        o.append(H.label(s, xc, ax.y0 + 39, b, "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.x0, 26, f"factor 2/(1 − R) = {w_rig / w_el:.0f} less mechanical work for the muscle per step",
                     "label", I["primary"]))
    o.append(H.label(s, ax.x0, ax.y0 + 70, "Mechanical work only: the metabolic saving is smaller, because muscle also spends "
                     "energy holding force.", "label2", I["secondary"]))
    aria = (f"Bar chart of muscle mechanical work per running step. A rigid leg makes the muscle absorb the bounce energy "
            f"U = 31 J on landing and regenerate it at push-off: 2U = {w_rig:.0f} J (red bar). With an elastic tendon of "
            f"resilience 0.92 the tendon returns R U = {back:.1f} J (dashed outline) and the muscle supplies only the loss, "
            f"(1 - R) U = {w_el:.1f} J (short red bar): a factor 2/(1 - R) = {w_rig / w_el:.0f} less mechanical work.")
    hv = [[r2(xa), r2(ax.Y(w_rig)), f"rigid leg: muscle work 2U = {w_rig:.1f} J per step"],
          [r2(xb), r2(ax.Y(w_el)), f"elastic tendon: muscle work (1 − R)U = {w_el:.2f} J; tendon returns {back:.2f} J"]]
    return svg(VB, aria, s, o, H.hover_attr(box(ax), hv))


# ================================================================ #12: three ATP-supply systems, log bars
def fig12():
    VB = (0, 0, 760, 346)
    s = H.Scale(VB[2], VB[3])
    p = "m9f12_"
    cp = 75e-3 * M / 60 * 20.9e3                       # VO2max (L/kg/min) x m / 60 x eps_O2 (J/L), line 277
    c_pcr = 20e-3 * 15 * (20.9 * 22.4 / 6)             # [PCr] x 15 kg = 0.3 mol, x 78 kJ/mol (line 281), kJ
    assert round(cp) == 1829 and round(c_pcr, 1) == 23.4, (cp, c_pcr)
    A = Ax((90, 56, 345, 262), (0, 3), (100, 2e4), ylog=True)
    B = Ax((480, 56, 735, 262), (0, 3), (1, 1000), ylog=True)
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, A, [], [(v, t) for v, t in ((100, "100"), (1000, "1000"), (1e4, "10 000"))], None, "rate ceiling (W, log scale)",
              ylab_x=34)
    o += axes(s, B, [], [(v, t) for v, t in ((1, "1"), (10, "10"), (100, "100"), (1000, "1000"))], None,
              "capacity (kJ, log scale)", ylab_x=438)
    names = ("PCr", "glycolytic", "oxidative")
    bw = 54
    dash = f'stroke-dasharray="{s(5):.2f} {s(3):.2f}"'

    def bar(ax, i, v, solid):
        xc = ax.X(i + 0.5)
        if solid:
            return f'<rect x="{xc - bw / 2:.2f}" y="{ax.Y(v):.2f}" width="{bw}" height="{ax.y0 - ax.Y(v):.2f}" fill="{SER[1]}"/>'
        return (f'<rect x="{xc - bw / 2:.2f}" y="{ax.Y(v):.2f}" width="{bw}" height="{ax.y0 - ax.Y(v):.2f}" fill="none" '
                f'stroke="{O["dim"]}" stroke-width="{s(1.3):.2f}" {dash}/>')
    # illustrative (not computed) heights: rate PCr 4 CP, glycolytic 2 CP; glycolytic capacity 2 C_PCr (caption line 264)
    o.append(bar(A, 0, 4 * cp, False))
    o.append(bar(A, 1, 2 * cp, False))
    o.append(bar(A, 2, cp, True))
    o.append(bar(B, 0, c_pcr, True))
    o.append(bar(B, 1, 2 * c_pcr, False))
    o.append(H.arrow(s, p, B.X(2.5), B.y0, B.X(2.5), B.top + 2, "geometry"))
    o.append(H.label(s, A.X(2.5), A.Y(cp) - 8, f"CP = {cp:.0f} W", "label2", I["primary"], "middle"))
    o.append(H.label(s, B.X(0.5), B.Y(c_pcr) - 8, f"{c_pcr:.1f} kJ", "label2", I["primary"], "middle"))
    o.append(H.label(s, B.X(2.5) - 7, B.top + 12, "unbounded", "label2", I["primary"], "end"))
    for ax, i, v in ((A, 0, 4 * cp), (A, 1, 2 * cp), (B, 1, 2 * c_pcr)):
        o.append(H.label(s, ax.X(i + 0.5), ax.Y(v) - 8, "not computed", "label2", I["secondary"], "middle"))
    for ax in (A, B):
        for i, n in enumerate(names):
            o.append(H.label(s, ax.X(i + 0.5), ax.y0 + 20, n, "label2", I["primary"], "middle"))
    o.append(f'<rect x="{A.x0}" y="14" width="22" height="12" fill="{SER[1]}"/>')
    o.append(H.label(s, A.x0 + 30, 25, "computed in the text (§7)", "label2", I["primary"]))
    o.append(f'<rect x="{A.x0 + 240}" y="14" width="22" height="12" fill="none" stroke="{O["dim"]}" stroke-width="{s(1.3):.2f}" {dash}/>')
    o.append(H.label(s, A.x0 + 270, 25, "drawn in order only, not computed", "label2", I["primary"]))
    o.append(H.label(s, A.x0, 318, "PCr = phosphocreatine. Bars start at the axis floor (100 W, 1 kJ). Dashed heights show only the "
                     "order: PCr above", "label2", I["secondary"]))
    o.append(H.label(s, A.x0, 336, "glycolysis above the oxidative ceiling, and glycolysis holding more than PCr (§7).", "label2", I["secondary"]))
    aria = (f"Two bar panels on log scales for a 70 kg runner. Left: rate ceiling in watts. Only the oxidative bar is "
            f"computed, {cp:.0f} W, the critical power CP; the phosphocreatine and glycolytic ceilings are dashed outlines "
            f"drawn above it in illustrative order, not computed. Right: capacity in kilojoules. Phosphocreatine holds "
            f"{c_pcr:.1f} kJ (computed); the glycolytic capacity is a dashed outline drawn larger, not computed; oxidative "
            f"capacity is unbounded, an arrow off the top of the axis.")
    hv = H.hover_attr([
        (box(A), [[r2(A.X(0.5)), r2(A.Y(4 * cp)), "phosphocreatine rate ceiling: not computed (order only)"],
                  [r2(A.X(1.5)), r2(A.Y(2 * cp)), "glycolytic rate ceiling: not computed (order only)"],
                  [r2(A.X(2.5)), r2(A.Y(cp)), f"oxidative rate ceiling CP = {cp:.0f} W"]]),
        (box(B), [[r2(B.X(0.5)), r2(B.Y(c_pcr)), f"phosphocreatine capacity {c_pcr:.1f} kJ"],
                  [r2(B.X(1.5)), r2(B.Y(2 * c_pcr)), "glycolytic capacity: not computed (order only)"],
                  [r2(B.X(2.5)), r2(B.top), "oxidative capacity: unbounded on exercise timescales"]])])
    return svg(VB, aria, s, o, hv)


# ================================================================ #13: landing force and the stopping distance
H_STAT = 1.75                                          # m, assumed stature for drawing the bodies to scale
H_DROP = 0.5


def f_land(ds):
    """Prop. 8.1 / Lab 3, average force in body weights."""
    v2 = 2 * G * H_DROP
    return (0.5 * M * v2 / ds + M * G) / BW


assert [round(f_land(d), 1) for d in (0.05, 0.15, 0.30, 0.45)] == [11.0, 4.3, 2.7, 2.1]        # Lab 3 output


def land_pose(kind, lam):
    """Landing posture, feet flat, arms forward. stiff: knee lam deg, hip 0.6 lam, pelvis 0.2 lam (trunk upright);
    soft: lam x the kit's cmj_crouch angles (pelvis, trunk, hip, knee)."""
    if kind == "stiff":
        pel, tr, hip, knee = 0.2 * lam, 0.0, 0.6 * lam, lam
    else:
        c = LB.POSES["cmj_crouch"]
        pel, tr, hip, knee = lam * c["pelvis"], lam * c["trunk"], lam * c["near"]["hip"], lam * c["near"]["knee"]
    leg = dict(hip=hip, knee=knee, shoulder=35, elbow=25)
    return LB.pose(pelvis=pel, trunk=tr, near=dict(leg), far=dict(leg, shoulder=45))


def com_h(P):
    """Whole-body COM height above the floor, in statures."""
    tot = sum(m for _, m in P.com.values())
    cy = sum(c[1] * m for c, m in P.com.values()) / tot
    return (P.floor_y - cy) / LB.H_U


@lru_cache(maxsize=None)
def land_lams():
    """The posture parameter that lowers the COM by d_s = 5 cm (stiff) and 40 cm (soft) below its upright
    (touchdown) height at stature H_STAT, by bisection."""
    h0 = com_h(land_pose("stiff", 0.0))
    out = []
    for kind, ds, hi in (("stiff", 0.05, 80.0), ("soft", 0.40, 1.6)):
        lo = 0.0
        for _ in range(50):
            mid = (lo + hi) / 2
            if (h0 - com_h(land_pose(kind, mid))) * H_STAT < ds:
                lo = mid
            else:
                hi = mid
        out.append((lo + hi) / 2)
    return h0, out


def fig13():
    VB = (0, 0, 760, 404)
    s = H.Scale(VB[2], VB[3])
    p = "m9f13_"
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    h0, (lam_s, lam_f) = land_lams()
    fy, hpx = 318, 236                                   # floor, drawn stature
    ycom0 = fy - h0 * hpx
    o.append(H.line(s, 14, fy, 400, fy, I["rule"], "ref"))
    o.append(H.line(s, 20, ycom0, 400, ycom0, I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, 400, ycom0 - 24, "COM height", "label2", I["secondary"], "end"))
    o.append(H.label(s, 400, ycom0 - 8, "at touchdown", "label2", I["secondary"], "end"))
    for kind, lam, xh, ds in (("stiff", lam_s, 50, 0.05), ("soft", lam_f, 230, 0.40)):
        b, J = LB.draw(p, s, land_pose(kind, lam), xh, fy, hpx)
        o.append(b)
        cx, cy = J["com"]
        assert abs((cy - ycom0) / hpx * H_STAT - ds) < 1e-3
        o.append(H.com_mark(s, cx, cy))
        f = f_land(ds)
        xf = J["toe"][0] + 14
        o.append(H.arrow(s, p, xf, fy, xf, fy - 10.0 * f, "force"))
        xd = J["bbox"][2] + 14
        o.append(H.line(s, cx + 9, cy, xd + 5, cy, I["rule"], "leader"))
        if kind == "stiff":
            o.append(H.line(s, xd - 5, ycom0, xd + 5, ycom0, O["geometry"], "geom"))
            o.append(H.line(s, xd - 5, cy, xd + 5, cy, O["geometry"], "geom"))
            o.append(H.line(s, xd, ycom0, xd, cy, O["geometry"], "geom"))
            o.append(H.label(s, xd + 9, ycom0 - 9, f'd{sub("s", s)} = 5 cm', "label2", I["primary"]))
            nm = f"stiff: F̄ = {f:.1f} BW"
        else:
            o.append(H.arrow(s, p, xd, ycom0 + 1, xd, cy - 1, "geometry", both=True))
            o.append(H.label(s, xd + 8, (ycom0 + cy) / 2 + 5, f'd{sub("s", s)} = 40 cm', "label2", I["primary"]))
            nm = f"soft: F̄ = {f:.2f} BW"
        xm = (J["heel"][0] + xf) / 2
        o.append(H.label(s, xm, fy + 21, nm, "label2", I["primary"], "middle"))
        o.append(H.label(s, xm, fy + 37, "knees nearly straight" if kind == "stiff" else "knees deeply bent",
                         "label2", I["secondary"], "middle"))
    # right: the 1/d_s law
    ax = Ax((490, 40, 740, 290), (0, 50), (0, 16))
    o += axes(s, ax, [(v, f"{v}") for v in range(0, 51, 10)], [(v, f"{v}") for v in range(0, 17, 4)],
              f'stopping distance d{sub("s", s, "label")} (cm)', "average force F̄ (body weights)", ylab_x=ax.x0 - 40)
    ds = np.linspace(0.5 / 15.0 * 100 * 1.0001, 50, 110)        # starts where F = 16 BW
    o.append(H.line(s, ax.x0, ax.Y(1), ax.x1, ax.Y(1), I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(12), ax.Y(1) - 7, "mg (a very long stop)", "label2", I["secondary"]))
    o.append(curve(s, ax, ds, [f_land(d / 100) for d in ds], SER[0]))
    o.append(dot(s, ax.X(5), ax.Y(f_land(0.05)), O["flag"]))
    o.append(H.label(s, ax.X(5) + 10, ax.Y(f_land(0.05)) + 4, "stiff: 5 cm, 11.0 BW", "label2", I["primary"]))
    o.append(dot(s, ax.X(40), ax.Y(f_land(0.40)), O["flag"]))
    o.append(H.label(s, ax.X(40), ax.Y(f_land(0.40)) - 22, "soft: 40 cm, 2.25 BW", "label2", I["primary"], "middle"))
    for d in (15, 30, 45):
        o.append(dot(s, ax.X(d), ax.Y(f_land(d / 100)), SER[0], hollow=True))
    o.append(H.label(s, ax.X(13), ax.Y(9.4), f'F̄ = ½ m v{sub("land", s)}² / d{sub("s", s)} + mg', "label2", I["primary"]))
    o.append(H.label(s, ax.X(13), ax.Y(9.4) + 17, f"0.5 m drop: v{sub('land', s)} = {math.sqrt(2 * G * H_DROP):.2f} m/s",
                     "label2", I["secondary"]))
    o.append(H.label(s, ax.X(13), ax.Y(9.4) + 34, "hollow dots: Lab 3 at 15, 30, 45 cm", "label2", I["secondary"]))
    o.append(LB.credit(s, 14, 386, width=730, extra=f" Stature drawn as {H_STAT} m."))
    aria = ("Left: two skeleton bodies at the end of a landing from a 0.5 m drop, drawn to scale for a 1.75 m stature. "
            "The stiff landing, knees nearly straight, lowers the centre of mass only 5 cm below its touchdown height "
            "(dashed line) and averages 11.0 body weights (long red arrow); the soft landing, knees deeply bent, lowers it "
            "40 cm and averages 2.25 body weights (short red arrow). Right: average force against stopping distance, the "
            "curve F = half m v squared over d_s plus mg, falling from 16 body weights at 3.3 cm toward the 1 body-weight "
            "limit; orange dots mark 5 cm (11.0) and 40 cm (2.25), hollow dots Lab 3's 15, 30 and 45 cm (4.3, 2.7, 2.1).")
    hd = np.linspace(ds[0], 50, 160)
    hv = H.hover_attr(box(ax), [[r2(ax.X(d)), r2(ax.Y(f_land(d / 100))), f"dₛ = {d:.1f} cm: F̄ = {f_land(d / 100):.2f} BW"]
                                for d in hd])
    return svg(VB, aria, s, o, hv)


# ================================================================ #14: impact transient and tissue tolerance
def half_sine(kc, t):
    pk, tr, lr, w = impact(kc)
    return np.where(t < math.pi / w, pk * np.sin(w * np.clip(t, 0, None)), 0.0) / BW


def fig14():
    VB = (0, 0, 760, 360)
    s = H.Scale(VB[2], VB[3])
    A = Ax((80, 50, 375, 290), (0, 90), (0, 3.0))
    B = Ax((490, 50, 740, 290), (0.2, 1.05), (1, 1e6), ylog=True)
    T, Fz, _, tc, _ = slip_sym()
    o = axes(s, A, [(v, f"{v}") for v in range(0, 91, 15)], [(v, f"{v:g}") for v in (0, 1, 2, 3)],
             "time from touchdown (ms)", "vertical GRF (body weights)", ylab_x=36)
    o += axes(s, B, [(v, f"{v:g}") for v in (0.2, 0.4, 0.6, 0.8, 1.0)],
              [(10 ** e, t) for e, t in ((0, "1"), (2, "10²"), (4, "10⁴"), (6, "10⁶"))],
              "per-step load / tolerance", "cycles to failure (log)", ylab_x=B.x0 - 44)
    t = np.linspace(0, 0.090, 121)
    act = np.interp(t, T, Fz) / BW
    o.append(curve(s, A, t * 1e3, act, I["secondary"], "curve_multi", DASH_SER))
    ys, yf = half_sine(K_STIFF, t), half_sine(K_SOFT, t)
    o.append(curve(s, A, t * 1e3, ys, SER[0], "curve_multi"))
    o.append(curve(s, A, t * 1e3, yf, SER[1], "curve_multi"))
    for (pk, tr, lr, _), col in ((impact(K_STIFF), SER[0]), (impact(K_SOFT), SER[1])):
        o.append(H.line(s, A.X(0), A.Y(0), A.X(tr * 1e3), A.Y(pk / BW), col, "leader", (3, 2)))
        o.append(dot(s, A.X(tr * 1e3), A.Y(pk / BW), col))
    pk, tr, lr, _ = impact(K_STIFF)
    o.append(H.line(s, A.X(tr * 1e3) + 2, A.Y(pk / BW) - 5, A.X(12), A.Y(2.45) + 4, I["rule"], "leader"))
    for k, (txt, col) in enumerate(((f"concrete, k{sub('c', s)} = 200 kN/m:", I["primary"]),
                                    (f"{pk / BW:.1f} BW at {tr * 1e3:.1f} ms", I["primary"]),
                                    (f"loading rate {lr:.0f} BW/s", I["secondary"]))):
        o.append(H.label(s, A.X(12), A.Y(2.85) + 16 * k, txt, "label2", col))
    pk, tr, lr, _ = impact(K_SOFT)
    for k, (txt, col) in enumerate((("cushioned, 40 kN/m:", I["primary"]),
                                    (f"{pk / BW:.1f} BW at {tr * 1e3:.1f} ms", I["primary"]),
                                    (f"loading rate {lr:.0f} BW/s,", I["secondary"]),
                                    (f"{_ls / _lf:.0f}× gentler", I["secondary"]))):
        o.append(H.label(s, A.X(48), A.Y(0.95) + 16 * k, txt, "label2", col))
    o.append(H.label(s, A.X(60), A.Y(1.72), "active force", "label2", I["primary"]))
    o.append(H.label(s, A.X(60), A.Y(1.72) + 16, "(SLIP stance, §5)", "label2", I["secondary"]))
    o += legend(s, A.x0, 26, [(SER[0], None, "stiff"), (SER[1], None, "soft"), (I["secondary"], DASH_SER, "active")], gap=14)
    # right: Basquin fatigue law of K9
    o.append(f'<rect x="{B.X(1.0):.2f}" y="{B.top}" width="{B.x1 - B.X(1.0):.2f}" height="{B.y0 - B.top}" fill="{SER[0]}" opacity="0.12"/>')
    fs = np.linspace(0.2, 1.0, 160)
    o.append(curve(s, B, fs, [n_fail(f) for f in fs], SER[0]))
    for k, txt in enumerate(("single overload:", "one load above", "tolerance (ACL)")):
        o.append(H.label(s, B.X(1.0) - 6, B.Y(3e5) + 16 * k, txt, "label2", I["primary"], "end"))
    for k, txt in enumerate(("cumulative dose:", "many cycles below", "it (stress fracture)")):
        o.append(H.label(s, B.X(0.23), B.Y(25) + 16 * k, txt, "label2", I["primary"]))
    o.append(H.label(s, B.x0, 20, f'K9’s Basquin law, b = {B_BAS}:', "label2", I["primary"]))
    o.append(H.label(s, B.x0, 37, 'N = (tolerance/load)'
                     f'<tspan baseline-shift="super" font-size="{s(9):.2f}">1/b</tspan>', "label2", I["primary"]))
    aria = ("Left: vertical ground reaction in the first 90 ms after touchdown. The impact transients of Proposition 9.1 "
            "(effective mass 8 kg at 1.0 m/s) are half-sine pulses: on concrete (200 kN/m, red) the force peaks at 1.8 body "
            "weights at 9.9 ms, a loading rate of 185 body weights per second (dotted secant); on a cushioned surface (40 "
            "kN/m, blue) it peaks at 0.8 at 22.2 ms, a rate of 37, five times gentler. The dashed grey curve is the active "
            "force of the SLIP stance rising toward its peak. Right: cycles to failure on a log axis against per-step load "
            f"as a fraction of the single-load tolerance, from K9's Basquin law with b = 0.12: a steep fall from about "
            f"{round(n_fail(0.2), -4):.0f} cycles at 0.2 to one cycle at 1.0; the shaded band above 1.0 is single overload (ACL rupture), the "
            "region below is cumulative dose (stress fracture).")
    hv = H.hover_attr([
        (box(A), [[r2(A.X(x * 1e3)), [r2(A.Y(a)), r2(A.Y(b)), r2(A.Y(c))],
                   f"t = {x * 1e3:.1f} ms: stiff {a:.2f}, soft {b:.2f}, active {c:.2f} BW"]
                  for x, a, b, c in zip(t, ys, yf, act)]),
        (box(B), [[r2(B.X(f)), r2(B.Y(n_fail(f))), f"load {f:.2f} of tolerance: {n_fail(f):.3g} cycles to failure"]
                  for f in fs])])
    return svg(VB, aria, s, o, hv)


# ================================================================ #21 C3: one hump against two
def fig21():
    W = 400
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    T, Fz, _, tc, _ = slip_sym()
    P = Plot(s, (58, 50, 358, 206), (0, 100), (0, 2.75))
    pc = np.linspace(0, 100, 201)
    run = np.interp(pc / 100 * tc, T, Fz) / BW
    walk = walk_template(pc / 100)
    assert round(walk.max(), 2) == 1.10 and round(walk[100], 2) == 0.75, (walk.max(), walk[100])
    o = [P.axes([(v, f"{v}") for v in (0, 25, 50, 75, 100)], [(0, "0"), (1, "1"), (2, "2")],
                "percent of stance", "vertical GRF (BW)", grid=(2.0,))]
    o.append(H.line(s, P.x0, P.Y(1), P.x1, P.Y(1), I["secondary"], "ref", H.DASH_REF))
    o.append(P.curve(pc, walk, SER[1], multi=True, dash=DASH_SER))
    o.append(P.curve(pc, run, SER[0], multi=True))
    o.append(plabel(s, P.X(50), P.Y(run.max()) - 8, "running: one hump", "label2", I["primary"], "middle"))
    o.append(plabel(s, P.X(50), P.Y(0.75) + 16, "walking: two humps", "label2", I["primary"], "middle"))
    o.append(plabel(s, P.x1 + 4, P.Y(1) + 4, "1 BW", "label2", I["secondary"]))
    o.append(plegend(s, 58, 22, [(SER[0], "running (SLIP stance)", None), (SER[1], "walking (Module 8)", DASH_SER)]))
    aria = (f"Problem C3 plot: vertical ground reaction in body weights against percent of stance. The running curve (red, "
            f"the SLIP stance of section 5) is a single hump peaking at {run.max():.1f} body weights at midstance; the "
            "walking curve (blue dashed, Module 8's template) has two humps of 1.1 body weights around a dip to 0.75 "
            "at midstance, below the dashed body-weight line.")
    hv = [[r2(P.X(x)), [r2(P.Y(a)), r2(P.Y(b))], f"{x:.0f} % of stance: running {a:.2f}, walking {b:.2f} BW"]
          for x, a, b in zip(pc[::2], run[::2], walk[::2])]
    return svg(VB, aria, s, o, H.hover_attr(P.box, hv))


# ================================================================ #27 C9: same peak, two rise times
def fig27():
    W = 400
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    pk = impact(K_STIFF)[0] / BW
    trs, trf = impact(K_STIFF)[1] * 1e3, impact(K_SOFT)[1] * 1e3
    P = Plot(s, (58, 50, 388, 206), (0, 50), (0, 2.3))
    t = np.linspace(0, 50, 251)
    fs_ = np.where(t < 2 * trs, pk * np.sin(np.pi / 2 * t / trs), 0.0)
    ff_ = np.where(t < 2 * trf, pk * np.sin(np.pi / 2 * t / trf), 0.0)
    o = [P.axes([(v, f"{v}") for v in (0, 10, 20, 30, 40, 50)], [(0, "0"), (1, "1"), (2, "2")],
                "time from first contact (ms)", "force (BW)", grid=(1.0, 2.0))]
    o.append(H.line(s, P.x0, P.Y(pk), P.x1, P.Y(pk), I["secondary"], "ref", H.DASH_REF))
    o.append(plabel(s, P.x1, P.Y(pk) - 7, f"same peak, {pk:.1f} BW", "label2", I["secondary"], "end"))
    o.append(P.curve(t, ff_, SER[1], multi=True))
    o.append(P.curve(t, fs_, SER[0], multi=True))
    for tr, col in ((trs, SER[0]), (trf, SER[1])):
        o.append(H.line(s, P.X(tr), P.Y(pk), P.X(tr), P.y0, col, "leader", (3, 2)))
    o.append(plabel(s, P.X(trs) + 4, P.Y(0.25), f"{trs:.1f} ms", "label2", I["primary"]))
    o.append(plabel(s, P.X(trf) + 4, P.Y(0.25), f"{trf:.1f} ms", "label2", I["primary"]))
    o.append(plabel(s, P.X(trs), P.Y(pk) - 7, "concrete", "label2", I["primary"], "middle"))
    o.append(plabel(s, P.X(trf) + 6, P.Y(pk) - 7, "cushioned", "label2", I["primary"]))
    o.append(plegend(s, 58, 22, [(SER[0], "concrete, 200 kN/m", None), (SER[1], "cushioned, 40 kN/m", None)]))
    aria = (f"Problem C9 plot: two footstrike force pulses with the same peak, {pk:.1f} body weights. On concrete (red) the "
            f"force reaches the peak {trs:.1f} ms after contact; on a cushioned track (blue) it takes {trf:.1f} ms, the "
            "rise times of Proposition 9.1 for contact stiffnesses 200 and 40 kN/m.")
    hv = [[r2(P.X(x)), [r2(P.Y(a)), r2(P.Y(b))], f"t = {x:.1f} ms: concrete {a:.2f}, cushioned {b:.2f} BW"]
          for x, a, b in zip(t[::2], fs_[::2], ff_[::2])]
    return svg(VB, aria, s, o, H.hover_attr(P.box, hv))


# ================================================================ #28 C10: overload against dose
def fig28():
    W = 400
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 50, 388, 206), (0.2, 1.1), (0, 6))          # y in log10 cycles
    fs = np.linspace(0.2, 1.0, 161)
    lg = np.log10(n_fail(fs))
    o = [f'<rect x="{P.X(1.0):.2f}" y="{P.y1}" width="{P.x1 - P.X(1.0):.2f}" height="{P.y0 - P.y1}" fill="{SER[0]}" opacity="0.12"/>']
    o.append(P.axes([(v, f"{v:g}") for v in (0.2, 0.4, 0.6, 0.8, 1.0)], [(0, "1"), (2, "10²"), (4, "10⁴"), (6, "10⁶")],
                    "per-step load / tolerance", "cycles to failure"))
    o.append(P.curve(fs, lg, SER[0]))
    o.append(plabel(s, P.X(1.0) - 6, P.Y(5.4), "single overload:", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(1.0) - 6, P.Y(5.4) + 15, "one load above tolerance", "label2", I["primary"], "end"))
    for k, txt in enumerate(("cumulative dose:", "many loads, each", "below tolerance")):
        o.append(plabel(s, P.X(0.24), P.Y(1.55) + 15 * k, txt, "label2", I["primary"]))
    o.append(plabel(s, 58, 26, "fatigue law: cycles to failure fall steeply with load", "label2", I["secondary"]))
    aria = ("Problem C10 plot: cycles to failure on a log axis against per-step load as a fraction of tolerance. The curve "
            f"falls steeply, from about {round(n_fail(0.2), -4):.0f} cycles at 0.2 to a single cycle at 1.0; the shaded band above tolerance is "
            "the single-overload region, the region below it the cumulative-dose region.")
    hv = [[r2(P.X(f)), r2(P.Y(v)), f"load {f:.2f} of tolerance: {10 ** v:.3g} cycles"] for f, v in zip(fs, lg)]
    return svg(VB, aria, s, o, H.hover_attr(P.box, hv))


# ================================================================ #34 D6: the ballistic parabola
def fig34():
    W = 400
    VB = (0, 0, W, 254)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m9f34_"
    # Prop. 2.3 and (4.1): x = vx t, y = vy t - g t^2/2; tf = 2vy/g, apex vy^2/2g, range 2 vx vy/g (lines 155-158).
    # The text's jog (line 160): vy = 0.9, vx = 4 m/s gives tf = 0.18 s, apex ~4 cm, range ~0.7 m.
    vx, vy = 4.0, 0.9
    tf, hap, dfl = 2 * vy / G, vy ** 2 / (2 * G), 2 * vx * vy / G
    assert round(tf, 2) == 0.18 and round(hap * 100) == 4 and round(dfl, 1) == 0.7
    x0, x1, yf, ya = 62.0, 362.0, 186.0, 86.0              # takeoff, landing, floor, apex (height exaggerated)
    u = np.linspace(0, 1, 81)                               # u = t / tf
    X = lambda v: x0 + v * (x1 - x0)                        # noqa: E731  (x / range)
    Y = lambda v: yf - v * (yf - ya)                        # noqa: E731  (height / apex height)
    hh = 4 * u * (1 - u)                                    # (vy t - g t^2/2) / h_apex with t = u tf
    assert abs(hh.max() - 1) < 1e-12 and abs(vy * 0.5 * tf - 0.5 * G * (0.5 * tf) ** 2 - hap) < 1e-12
    pts = " ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in zip(u, hh))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o.append(H.line(s, 20, yf, 384, yf, I["rule"], "ref"))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{SER[1]}" stroke-width="{s(H.PX["curve"]):.2f}" '
             f'stroke-linejoin="round" stroke-dasharray="{s(6):.2f} {s(4):.2f}"/>')
    o.append(dot(s, x0, yf, I["primary"]))
    o.append(dot(s, x1, yf, I["primary"]))
    # takeoff velocity with its components (slope of v = slope of the parabola at takeoff: 4 h / range)
    cx, cy = 48.0, 48.0 * 4 * (yf - ya) / (x1 - x0)
    tx, ty = x0 + cx, yf - cy
    o.append(H.arrow(s, p, x0, yf - 4, x0, ty, "dim"))
    o.append(H.arrow(s, p, x0, ty, tx, ty, "dim"))
    o.append(H.arrow(s, p, x0, yf, tx, ty, "force"))
    o.append(H.label(s, x0 - 7, (yf + ty) / 2 + 5, f'v{sub("y", s)}', "label", I["primary"], "end", 'font-style="italic"'))
    o.append(H.label(s, (x0 + tx) / 2, ty - 8, f'v{sub("x", s)}', "label", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, tx + 8, yf - cy / 2 + 6, "v", "label", I["primary"], "start", 'font-style="italic"'))
    # apex height and its time
    xm = X(0.5)
    o.append(H.arrow(s, p, xm, yf - 1, xm, ya + 1, "geometry", both=True))
    o.append(H.label(s, xm + 9, (yf + ya) / 2 + 22, f'h{sub("apex", s)} = v{sub("y", s)}² / 2g', "label2", I["primary"]))
    o.append(H.label(s, xm, ya - 10, f'apex at t = v{sub("y", s)} / g', "label2", I["secondary"], "middle"))
    # flight time and range along the floor
    yd = yf + 24
    o.append(H.arrow(s, p, x0 + 1, yd, x1 - 1, yd, "dim", both=True))
    o.append(H.label(s, (x0 + x1) / 2, yd + 17, f'flight time t{sub("f", s)} = 2v{sub("y", s)} / g', "label2", I["primary"], "middle"))
    o.append(H.label(s, (x0 + x1) / 2, yd + 33, f'range d{sub("f", s)} = v{sub("x", s)}t{sub("f", s)} = 2v{sub("x", s)}v{sub("y", s)} / g',
                     "label2", I["primary"], "middle"))
    o.append(H.label(s, 14, 22, "takeoff and landing at the same height; vertical scale exaggerated", "label2", I["secondary"]))
    aria = ("Problem D6 figure: the ballistic parabola of the centre of mass between takeoff and the next touchdown at the "
            "same height, drawn with the vertical scale exaggerated. The takeoff velocity v (red arrow) has components vx "
            "and vy. The apex height is vy squared over 2g, reached at t = vy/g; the flight time is tf = 2vy/g and the "
            "horizontal range is df = vx tf = 2 vx vy / g.")
    hv = [[r2(X(a)), r2(Y(b)), f"t = {a:.2f} tf: x = {a:.2f} range, height = {b:.2f} apex height"]
          for a, b in zip(u[::2], hh[::2])]
    return svg(VB, aria, s, o, H.hover_attr([x0, ya, x1, yf], hv))


# ================================================================ #35 D7: the stance impulse
def fig35():
    W = 400
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    T, Fz, _, tc, J = slip_sym()
    ms, fz = T * 1e3, Fz / BW
    P = Plot(s, (58, 30, 388, 206), (0, 175), (0, 2.75))
    k = list(range(0, len(T), 20)) + [len(T) - 1]
    o = [f'<polygon points="{" ".join(f"{P.X(ms[i]):.1f},{P.Y(fz[i]):.1f}" for i in k)} {P.X(ms[-1]):.1f},{P.Y(0):.1f} '
         f'{P.X(0):.1f},{P.Y(0):.1f}" fill="{SER[0]}" opacity="0.13"/>']
    o.append(f'<rect x="{P.X(0):.2f}" y="{P.Y(1):.2f}" width="{P.X(ms[-1]) - P.X(0):.2f}" height="{P.Y(0) - P.Y(1):.2f}" '
             f'fill="#cfcfcf" opacity="0.75"/>')
    o.append(P.axes([(v, f"{v}") for v in (0, 50, 100, 150)], [(0, "0"), (1, "1"), (2, "2")],
                    "time from touchdown (ms)", f'F{sub("z", s, "label")} (BW)'))
    o.append(H.line(s, P.x0, P.Y(1), P.x1, P.Y(1), I["secondary"], "ref", H.DASH_REF))
    o.append(P.curve(ms, fz, SER[0]))
    o.append(plabel(s, P.x1 - 2, P.Y(1) - 5, "mg", "label2", I["secondary"], "end"))
    o.append(plabel(s, P.X(tc * 500), P.Y(0.45), f'mg·t{sub("c", s)}', "label2", I["primary"], "middle"))
    o.append(plabel(s, P.X(tc * 500), P.Y(1.75), "excess over mg:", "label2", I["primary"], "middle"))
    o.append(plabel(s, P.X(tc * 500), P.Y(1.75) + 15, "momentum reversal", "label2", I["primary"], "middle"))
    o.append(plabel(s, P.X(tc * 500), P.Y(fz.max()) - 7, f'shaded area = ∫F{sub("z", s)} dt', "label2", I["primary"], "middle"))
    aria = ("Problem D7 plot: the vertical ground reaction over one symmetric running stance, a single hump. The shaded "
            "area under it is the stance impulse; a grey rectangle under the dashed body-weight line marks the weight "
            "support mg times tc, and the part above the line is the momentum reversal to be derived.")
    hv = [[r2(P.X(ms[i])), r2(P.Y(fz[i])), f"t = {ms[i]:.0f} ms: Fz = {fz[i]:.2f} BW"] for i in range(0, len(T), 15)]
    return svg(VB, aria, s, o, H.hover_attr(P.box, hv))


# ================================================================ #37 D9: tendon hysteresis loop
def fig37():
    W = 400
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    pw = unload_p()
    x = np.linspace(0, X5, 401)
    up, dn = f_toe(x), f_toe(x) * (x / X5) ** pw
    loss = U_T - float(np.trapezoid(dn, x))
    assert round(U_T, 1) == 31.0 and round(U_T - loss, 1) == 28.5 and round(loss, 1) == 2.5
    P = Plot(s, (58, 50, 388, 206), (0, 17), (0, 5.4))
    mm, uk, dk = x * 1e3, up / 1e3, dn / 1e3
    o = [f'<polygon points="{" ".join(f"{P.X(a):.1f},{P.Y(b):.1f}" for a, b in zip(mm[::4], uk[::4]))} '
         f'{" ".join(f"{P.X(a):.1f},{P.Y(b):.1f}" for a, b in zip(mm[::-4], dk[::-4]))}" fill="{O["flag"]}" opacity="0.30"/>']
    o.append(P.axes([(v, f"{v}") for v in (0, 4, 8, 12, 16)], [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                    "tendon elongation (mm)", "force (kN)", grid=(1, 2, 3, 4, 5)))
    o.append(P.curve(mm, dk, SER[1], multi=True))
    o.append(P.curve(mm, uk, SER[0], multi=True))
    o.append(plabel(s, P.X(0.6), P.Y(4.75), f"store U = {U_T:.1f} J", "label2", I["primary"]))
    o.append(plabel(s, P.X(0.6), P.Y(4.75) + 15, "(area under loading)", "label2", I["secondary"]))
    o.append(plabel(s, P.X(9.3), P.Y(1.0), f"return R·U = {U_T - loss:.1f} J", "label2", I["primary"]))
    o.append(plabel(s, P.X(9.3), P.Y(1.0) + 15, "(area under unloading)", "label2", I["secondary"]))
    xi = int(np.argmax(up - dn))
    o.append(H.line(s, P.X(mm[xi]) + 3, P.Y((uk[xi] + dk[xi]) / 2), P.X(13.2), P.Y(4.6) + 4, I["rule"], "leader"))
    o.append(plabel(s, P.X(13.2) + 3, P.Y(4.6), f"loss = loop = {loss:.1f} J", "label2", I["primary"], "end"))
    o.append(plegend(s, 58, 22, [(SER[0], "loading (stretch)", None), (SER[1], "unloading (recoil)", None)]))
    aria = (f"Problem D9 plot: tendon force against elongation for one stretch-recoil cycle, Module 6's toe tendon loaded "
            f"to 5 kN at {X5 * 1e3:.1f} mm. The loading curve (red) stores {U_T:.1f} J; the unloading curve (blue) lies "
            f"just below it and returns {U_T - loss:.1f} J, resilience 0.92; the thin orange loop between them is the "
            f"{loss:.1f} J lost as heat.")
    hv = [[r2(P.X(a)), [r2(P.Y(b)), r2(P.Y(c))], f"{a:.1f} mm: loading {b:.2f} kN, unloading {c:.2f} kN"]
          for a, b, c in zip(mm[::4], uk[::4], dk[::4])]
    return svg(VB, aria, s, o, H.hover_attr(P.box, hv))


FIGS = {
    4: ("Running-gait timeline over one stride. The right and left le", fig4),
    8: ("Top: the vertical ground reaction over stance; the shaded ar", fig8),
    11: ("Muscle mechanical work per step. A rigid leg would make the ", fig11),
    12: ("Two bar panels, both log scale. Left: rate ceiling in watts;", fig12),
    13: ("Left: a stiff landing with nearly straight legs stops over a", fig13),
    14: ("Left: vertical ground reaction in the first 90 milliseconds ", fig14),
    21: ("A single-humped running ground reaction force over stance.", fig21),
    27: ("Two footstrike force-time curves reaching the same peak, one", fig27),
    28: ("A steep cycles-to-failure versus load curve, with a single-o", fig28),
    29: ("A running-gait timeline: stance bars separated by a flight g", fig29),
    34: ("The ballistic parabola with takeoff velocity, apex height an", fig34),
    35: ("The vertical GRF over stance, its shaded area the stance imp", fig35),
    37: ("A tendon force-elongation hysteresis loop: store, return, an", fig37),
}
