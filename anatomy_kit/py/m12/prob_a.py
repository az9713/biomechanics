"""Module 12 problem figures, group `prob_a` (primary class f, 400 px): C2, C5, C6, C7, C10, D1, D2, D3, D4, D6, D7.

svg #20 (C2 scale invariance), #23 (C5 servo against the wall), #24 (C6 aftereffect), #25 (C7 variable but accurate),
#28 (C10 delay caps the gain), #29 (D1 Euler-Poisson variation), #30 (D2 minimum-jerk polynomial), #31 (D3 the 1.875 ratio),
#32 (D4 HJB to gain and Riccati), #34 (D6 reafference cancellation), #35 (D7 adaptation recursion).
Every plotted number is computed here from what module12.html states (line numbers of the page):
  C2 (407), D2 (449), D3 (453): x(tau) = D(10 tau^3 - 15 tau^4 + 6 tau^5), v = D/T (30 tau^2 - 60 tau^3 + 30 tau^4), peak 1.875 D/T.
  C5 (419): Lab C (loop imported from m12.plots_main): servo peak 388 N, settles 238 N; impedance peak 21 N, settles 10 N, factor 23.9.
  C6 (423, Prop. 6.2): aftereffect = -p g, the mirror of the first perturbed error.
  C7 (427): Lab D scatter (imported from m12.plots_main): Var(null) 2.01, Var(task) 0.30, ratio 6.65 against 1/rho = 6.67.
  C10 (439, K10 solution 746): k < pi/(2 tau_d): 31.42, 15.71, 10.47, 7.85 s^-1 at tau_d = 0.05, 0.10, 0.15, 0.20 s.
  D1 (445): x -> x + eps zeta, zeta and its first p-1 derivatives zero at both ends (p = 3 drawn: zeta = 64 [tau(1-tau)]^3).
  D7 (469, Prop. 6.2): e_{n+1} = (1 - eta g) e_n, converges iff 0 < eta g < 2, first error after removal -p g.
D4 (457) and D6 (465) are block diagrams of the solution's equations.
"""
import math

import numpy as np

import house as H
from m05.plots_prob import Plot, hov, label, legend, sub, svg
from m05.schematic import BOX
from m12.plots_main import (RHO, SER, SIG, VAR_N, VAR_T, _RUN, _y1, _y2, hat, steady, DT_C, XW, X_DES, N_TR)

O, I, T = H.OVERLAY, H.INK, H.TISSUE
W = 400


def tk(vals, f="{:g}"):
    return [(v, f.format(v).replace("-", "−")) for v in vals]


def mn(v, f="{:.0f}"):
    return f.format(v).replace("-", "−")


def rowlegend(s, x, y, items, dash=None):
    """Legend rows (one per line): [(colour, text)]."""
    o = []
    for k, (col, txt) in enumerate(items):
        yy = y + 18 * k
        o.append(H.line(s, x, yy - 4.5, x + 24, yy - 4.5, col, "curve_multi", dash))
        o.append(label(s, x + 31, yy, txt, "label2", I["secondary"]))
    return "".join(o)


def dot(P, x, y, col, hollow=False, r=None):
    r = r or P.s(H.PX["dot"])
    if hollow:
        return (f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{r:.2f}" fill="#fff" stroke="{col}" '
                f'stroke-width="1.8"/>')
    return f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{r:.2f}" fill="{col}" stroke="#fff" stroke-width="1.5"/>'


def xd(n, rest=""):
    """x with one (n=1) or two (n=2) dots above it (spacing modifiers; Georgia has no combining marks in SVG)."""
    mark, d1, d2 = ("˙", -0.38, 0.13) if n == 1 else ("¨", -0.42, 0.09)
    return f'x<tspan dx="{d1}em" dy="-0.45em">{mark}</tspan><tspan dy="0.45em" dx="{d2}em">{rest}</tspan>'


def hline(s, P, y, col=None, dash=H.DASH_REF):
    return H.line(s, P.x0, P.Y(y), P.x1, P.Y(y), col or I["secondary"], "ref", dash)


# ---------------------------------------------------------------- minimum-jerk shapes (Prop. 3.1, lines 449-453)
def mj_x(tau):
    return 10 * tau ** 3 - 15 * tau ** 4 + 6 * tau ** 5


def mj_v(tau):
    """v T / D."""
    return 30 * tau ** 2 - 60 * tau ** 3 + 30 * tau ** 4


_tau = np.linspace(0, 1, 401)
assert abs(mj_v(_tau).max() - 1.875) < 1e-9 and abs(mj_v(0.5) - 30 / 16) < 1e-12                # D3, line 453
assert abs(np.trapezoid(mj_v(_tau), _tau) - 1.0) < 1e-6 and abs(mj_x(1.0) - 1.0) < 1e-12           # mean speed D/T


def frame_svg(VB, aria, s, body, hover=None):
    return svg(VB, aria, s, "".join(body), hover)


# ================================================================ #20 C2: fast or slow, same shape
def fig20():
    VB = (0, 0, W, 424)
    s = H.Scale(W, VB[3], display_w=400)
    reaches = [(0.40, 0.50, SER[0]), (0.20, 0.30, SER[1]), (0.10, 0.20, SER[2])]
    tau = np.linspace(0, 1, 201)
    A = Plot(s, (62, 84, 388, 196), (0, 0.5), (0, 1.6))
    B = Plot(s, (62, 276, 388, 376), (0, 1), (0, 2))
    o = [rowlegend(s, 62, 18, [(c, f"reach {D:.2f} m in {Tm:.2f} s: peak {1.875 * D / Tm:.2f} m/s") for D, Tm, c in reaches])]
    o.append(A.axes(tk((0, 0.1, 0.2, 0.3, 0.4, 0.5), "{:.1f}"), tk((0, 0.8, 1.6), "{:.1f}"), "time t (s)", "speed v (m/s)", grid=(0.8,)))
    curves = []
    for D, Tm, c in reaches:
        t, v = tau * Tm, D / Tm * mj_v(tau)
        assert abs(v.max() - 1.875 * D / Tm) < 1e-9
        curves.append((t, v))
        o.append(A.curve(t, v, c, multi=True))
    o.append(B.axes(tk((0, 0.5, 1), "{:.1f}"), tk((0, 1, 2)), "t/T", "v·T/D", grid=(1,)))
    for k, (D, Tm, c) in enumerate(reaches):
        o.append(B.curve(tau, mj_v(tau), c, multi=True, dash=None if k == 0 else (7 + 5 * k, 5)))
    o.append(dot(B, 0.5, 1.875, O["flag"], r=5))
    o.append(label(s, B.X(0.5) - 10, B.Y(1.875) - 12, "peak 1.875 at t/T = ½", "label2", I["primary"], "end"))
    o.append(label(s, B.x1 - 4, B.Y(1.9) + 4, "all three reaches", "label2", I["primary"], "end"))
    o.append(label(s, B.x1 - 4, B.Y(1.9) + 20, "fall on one curve", "label2", I["primary"], "end"))
    aria = ("Problem C2, two panels. Top: the speed against time of three minimum-jerk reaches, 0.40 m in 0.50 s, 0.20 m in "
            "0.30 s and 0.10 m in 0.20 s, symmetric bells with peak speeds 1.50, 1.25 and 0.94 metres per second. Bottom: the same "
            "three reaches with speed scaled by T over D and time scaled by T; the three curves coincide in one bell with peak "
            "1.875 at one half.")
    t0 = curves[0][0]
    pa = hov(A, t0, [np.interp(t0, t, v) for t, v in curves],
             lambda i: f"t = {t0[i]:.3f} s: " + ", ".join(f"{np.interp(t0[i], t, v):.2f}" for t, v in curves) + " m/s")
    pb = hov(B, tau, [mj_v(tau)], lambda i: f"t/T = {tau[i]:.3f}: v·T/D = {mj_v(tau[i]):.3f}")
    return frame_svg(VB, aria, s, o, ([(A.box, pa), (B.box, pb)],))


# ================================================================ #23 C5: the servo against the wall
def fig23():
    VB = (0, 0, W, 396)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m12f23_"
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    px = lambda cm: 70 + 20 * cm                    # schematic: 20 px per cm   # noqa: E731
    fl = 102
    o.append(H.line(s, 30, fl, 392, fl, I["axis"], "axis"))
    o.append(f'<rect x="{px(0) - 18:.1f}" y="{fl - 30}" width="36" height="30" rx="4" fill="{BOX}" stroke="{I["rule"]}" stroke-width="1"/>')
    o.append(f'<rect x="{px(10):.1f}" y="52" width="14" height="{fl - 52}" fill="{I["rule"]}"/>')
    o.append(H.line(s, px(15), 60, px(15), fl, I["secondary"], "ref", H.DASH_REF))
    o.append(dot_xy(px(15), fl - 15, I["secondary"]))
    o.append(H.arrow(s, p, px(0) + 22, fl - 15, px(0) + 92, fl - 15, "force"))
    o.append(label(s, px(0), fl + 20, "hand, 1 kg", "label2", I["primary"], "middle"))
    o.append(label(s, px(10) + 7, fl + 20, "wall at 10 cm", "label2", I["primary"], "middle"))
    o.append(label(s, px(15) + 8, 46, "commanded 15 cm", "label2", I["primary"], "end"))
    o.append(label(s, px(0) + 56, fl - 40, "controller force", "label2", I["primary"], "middle"))
    # force traces (Lab C loop, imported)
    P = Plot(s, (62, 176, 388, 328), (0, 0.6), (-100, 400))
    o.append(rowlegend_row(s, 62, 158, [(SER[0], "position servo"), (SER[1], "impedance controller")]))
    o.append(P.axes(tk((0, 0.2, 0.4, 0.6), "{:.1f}"), tk((-100, 0, 100, 200, 300, 400)), "time t (s)", "controller force (N)",
                    grid=(100, 200, 300, 400)))
    o.append(H.line(s, P.x0, P.Y(0), P.x1, P.Y(0), I["axis"], "ref"))
    n = int(0.6 / DT_C)
    t = np.arange(n) * DT_C
    ptsy, summ = [], {}
    for nm, col in (("servo", SER[0]), ("impedance", SER[1])):
        F, C, fmax = _RUN[nm]
        k0 = int(np.argmax(C))
        summ[nm] = (F, k0, fmax)
        o.append(P.curve(t[k0:n], F[k0:n], col, nmax=700))
        o.append(dot(P, t[k0], F[k0], col, hollow=True, r=4))
        ss = steady(5000.0 if nm == "servo" else 200.0)
        o.append(H.line(s, P.X(0.36), P.Y(ss), P.x1, P.Y(ss), col, "ref", H.DASH_REF))
    Fs, k0s, fms = summ["servo"]
    Fi, k0i, fmi = summ["impedance"]
    kpk = int(np.argmax(np.where(_RUN["servo"][1][:n], Fs[:n], -1e9)))
    o.append(dot(P, t[kpk], Fs[kpk], SER[0], r=4.5))
    o.append(label(s, P.X(t[kpk]) + 10, P.Y(Fs[kpk]) + 4, f"servo peak {fms:.0f} N", "label2", I["primary"]))
    o.append(label(s, P.x1 - 4, P.Y(steady(5000.0)) - 8, f"servo settles at {steady(5000.0):.0f} N", "label2", I["primary"], "end"))
    o.append(label(s, P.x1 - 4, P.Y(steady(200.0)) - 24, f"impedance: peak {fmi:.0f} N,", "label2", I["primary"], "end"))
    o.append(label(s, P.x1 - 4, P.Y(steady(200.0)) - 8, f"settles at {steady(200.0):.0f} N", "label2", I["primary"], "end"))
    o.append(label(s, 62, 388, f"servo settles {steady(5000.0) / steady(200.0):.1f} times higher; open dots: first contact",
                   "label2", I["secondary"]))
    aria = ("Problem C5. Top: a 1 kg hand starts at 0 cm and is commanded to 15 cm, 5 cm behind a rigid wall at 10 cm; the "
            "controller force acts toward the wall. Bottom: the controller force against time for 0 to 0.6 s, from the Lab C "
            "loop. The stiff position servo (red) first touches the wall at 33 ms, peaks at 388 N and settles at 238 N. The "
            "impedance controller (blue) first touches at 168 ms, peaks at 21 N and settles at 10 N, 23.9 times less.")
    k = np.arange(k0s, n)
    ys = [[P.Y(Fs[j]), P.Y(Fi[j])] for j in k]
    pts = [[round(P.X(t[j]), 2), ys[i], f"t = {t[j]:.3f} s: servo {mn(Fs[j])} N, impedance {mn(Fi[j], '{:.1f}')} N"]
           for i, j in enumerate(k)]
    return frame_svg(VB, aria, s, o, (P.box, pts))


def dot_xy(x, y, col):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="#fff" stroke="{col}" stroke-width="1.8"/>'


def rowlegend_row(s, x, y, items):
    return legend(s, x, y, [(c, t_, None) for c, t_ in items])


# ================================================================ #24 C6: the opposite error
def fig24():
    VB = (0, 0, W, 332)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (62, 56, 388, 262), (-1.3, 1.3), (0, 1))
    tau = np.linspace(0, 1, 201)
    prog = mj_x(tau)
    hook = mj_v(tau) / 1.875                 # lateral deviation of the first field trial, in units of its peak (force ~ speed)
    o = [legend(s, 62, 16, [(SER[0], "field on, first trial", None)]) + legend(s, 62, 34, [(SER[1], "field removed, after learning", None)])]
    o.append(P.axes(tk((-1, 0, 1)), tk((0, 0.5, 1), "{:.1f}"), "lateral deviation (first-trial hook = 1)",
                    "progress toward target", grid=(0.5,)))
    o.append(H.line(s, P.X(0), P.y0, P.X(0), P.y1, I["secondary"], "ref", H.DASH_REF))
    o.append(P.curve(hook, prog, SER[0]))
    o.append(P.curve(-hook, prog, SER[1]))
    o.append(label(s, P.X(0.1), P.Y(0.5) + 4, "field on", "label2", I["primary"]))
    o.append(label(s, P.X(-0.1), P.Y(0.5) + 4, "after", "label2", I["primary"], "end"))
    o.append(dot(P, 0, 1, O["flag"], r=5))
    o.append(label(s, P.X(0) + 10, P.y1 - 6, "target", "label2", I["primary"]))
    o.append(label(s, 62, 322, "aftereffect = −p·g, the mirror of the first error", "label2", I["secondary"]))
    aria = ("Problem C6. Hand path toward a target, progress from 0 to 1 against lateral deviation. In the force field on the "
            "first trial the path hooks to the right (red); after learning, with the field removed, the path hooks the same "
            "distance to the left (blue), the mirror image, aftereffect minus p g. A dashed vertical line marks the straight reach. "
            "The deviation is drawn proportional to the minimum-jerk speed, a force proportional to hand speed.")
    pts = sorted(([round(P.X(-hook[i]), 2), P.Y(prog[i]), f"progress {prog[i]:.2f}: hook {mn(hook[i], '{:.2f}')} in the field, "
                   f"{mn(-hook[i], '{:.2f}')} after learning"] for i in range(len(tau))), key=lambda q: q[0])
    return frame_svg(VB, aria, s, o, (P.box, pts))


# ================================================================ #25 C7: variable but accurate (Lab D scatter)
def fig25():
    VB = (0, 0, W, 420)
    s = H.Scale(W, VB[3], display_w=400)
    R = 3.2
    P = Plot(s, (76, 44, 336, 304), (-R, R), (-R, R))
    n = 300
    o = [P.axes(tk((-3, -2, -1, 0, 1, 2, 3)), tk((-3, -2, -1, 0, 1, 2, 3)), "y₁ (effector 1)", "y₂ (effector 2)", ytx=22)]
    o.append(H.line(s, P.X(-R), P.Y(R), P.X(R), P.Y(-R), I["secondary"], "ref", H.DASH_REF))
    o.append(H.line(s, P.X(-R), P.Y(-R), P.X(R), P.Y(R), I["secondary"], "ref", H.DASH_REF))
    d = "".join(f"M{P.X(a):.1f} {P.Y(b):.1f}h0" for a, b in zip(_y1[:n], _y2[:n]))
    o.append(f'<path d="{d}" stroke="{SER[1]}" stroke-opacity="0.55" stroke-width="{s(5):.2f}" stroke-linecap="round" fill="none"/>')
    o.append(label(s, P.x0, P.y1 - 8, "null: y₁ − y₂ free", "label2", I["primary"]))
    o.append(label(s, P.x1, P.y1 - 8, "task: y₁ + y₂ held", "label2", I["primary"], "end"))
    o.append(label(s, 62, 368, f"variance: null {VAR_N:.2f}, task {VAR_T:.2f}, ratio {VAR_N / VAR_T:.2f}", "label2",
                   I["primary"]))
    o.append(label(s, 62, 386, f"prediction 1/ρ = {1 / RHO:.2f}; σ = {SIG:g}, ρ = {RHO:g}", "label2", I["secondary"]))
    o.append(label(s, 62, 404, f"{n} of {N_TR} outcomes drawn; variances use all", "label2", I["secondary"]))
    aria = (f"Problem C7. Scatter of {n} of {N_TR} simulated two-effector outcomes in the plane of y1 and y2, an ellipse "
            f"elongated along the dashed null direction y1 minus y2 and squeezed along the dashed task direction y1 plus y2. The "
            f"variance along the null variable is {VAR_N:.2f} and along the task variable {VAR_T:.2f}, a ratio of "
            f"{VAR_N / VAR_T:.2f} against the predicted one over rho, {1 / RHO:.2f}. The task, the struck key, is held; the "
            f"finger varies where it does not matter.")
    sel = sorted(range(n), key=lambda k: _y1[k])
    pts = hov(P, [_y1[k] for k in sel], [[_y2[k] for k in sel]],
              lambda i: f"outcome {sel[i] + 1}: y₁ = {mn(_y1[sel[i]], '{:.2f}')}, y₂ = {mn(_y2[sel[i]], '{:.2f}')}")
    return frame_svg(VB, aria, s, o, (P.box, pts))


# ================================================================ #28 C10: delay caps the gain
def fig28():
    VB = (0, 0, W, 252)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (62, 34, 388, 196), (0.04, 0.20), (0, 40))
    td = np.linspace(0.04, 0.20, 161)
    kmax = math.pi / (2 * td)
    chk = {0.05: 31.42, 0.10: 15.71, 0.15: 10.47, 0.20: 7.85}                       # K10 solution, line 746
    assert all(round(math.pi / (2 * t_), 2) == v for t_, v in chk.items())
    o = []
    poly = " ".join(f"{P.X(a):.1f},{P.Y(b):.1f}" for a, b in zip(td, kmax))
    o.append(f'<polygon points="{P.X(0.04):.1f},{P.Y(0):.1f} {poly} {P.X(0.20):.1f},{P.Y(0):.1f}" fill="{O["neural"]}" opacity="0.12"/>')
    o.append(f'<rect x="{P.X(0.10):.1f}" y="{P.y1:.1f}" width="{P.X(0.20) - P.X(0.10):.1f}" height="{P.y0 - P.y1:.1f}" '
             f'fill="{I["rule"]}" opacity="0.14"/>')
    o.append(P.axes(tk((0.05, 0.10, 0.15, 0.20), "{:.2f}"), tk((0, 10, 20, 30, 40)), f"delay τ{sub('d', s)} (s)",
                    "max stable gain k (s⁻¹)", grid=(10, 20, 30)))
    o.append(P.curve(td, kmax, SER[0]))
    for t_, v in chk.items():
        o.append(dot(P, t_, v, O["flag"], r=4.5))
    o.append(label(s, P.X(0.05) + 9, P.Y(31.42) - 4, "31.42", "label2", I["primary"]))
    o.append(label(s, P.X(0.10) + 9, P.Y(15.71) - 10, "15.71", "label2", I["primary"]))
    o.append(label(s, P.X(0.15) + 9, P.Y(10.47) - 10, "10.47", "label2", I["primary"]))
    o.append(label(s, P.X(0.20) - 8, P.Y(7.85) - 12, "7.85", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.045), P.Y(5), f"stable: kτ{sub('d', s, 'label2')} &lt; π/2", "label2", I["primary"]))
    o.append(label(s, P.X(0.16), P.Y(34), "unstable", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(0.15), P.Y(1.2), "100–200 ms band", "label2", I["secondary"], "middle"))
    aria = ("Problem C10. The ceiling on the stable gain of a first-order delayed loop, k max = pi over two tau-d, against the "
            "delay from 0.04 to 0.20 s: a red falling curve with a green stable region under it. Orange dots mark 31.42, 15.71, "
            "10.47 and 7.85 per second at delays 0.05, 0.10, 0.15 and 0.20 s. A grey band marks the 100 to 200 ms physiological "
            "delay.")
    pts = hov(P, td, [kmax], lambda i: f"τd = {td[i]:.3f} s: k max = {kmax[i]:.2f} s⁻¹")
    return frame_svg(VB, aria, s, o, (P.box, pts))


# ================================================================ #29 D1: the Euler-Poisson variation
def fig29():
    VB = (0, 0, W, 424)
    s = H.Scale(W, VB[3], display_w=400)
    tau = np.linspace(0, 1, 201)
    zeta = 64 * (tau * (1 - tau)) ** 3
    eps = 0.12
    x = mj_x(tau)
    assert abs(zeta.max() - 1.0) < 1e-12 and zeta[0] == zeta[-1] == 0.0
    A = Plot(s, (62, 52, 388, 192), (0, 1), (0, 1.2))
    B = Plot(s, (62, 262, 388, 356), (0, 1), (0, 1.2))
    o = [legend(s, 62, 22, [(SER[0], "x (minimizer)", None), (SER[1], f"x + εζ, ε = {eps:g}", None)])]
    o.append(A.axes(tk((0, 0.5, 1), "{:.1f}"), tk((0, 0.6, 1.2), "{:.1f}"), "t/T", "x(t)/D"))
    o.append(A.curve(tau, x + eps * zeta, SER[1], multi=True))
    o.append(A.curve(tau, x, SER[0], multi=True))
    o.append(dot(A, 0, 0, I["primary"], r=4))
    o.append(dot(A, 1, 1, I["primary"], r=4))
    o.append(label(s, A.X(0.62), A.Y(0.3), "same endpoints,", "label2", I["primary"]))
    o.append(label(s, A.X(0.62), A.Y(0.3) + 16, "same endpoint slopes", "label2", I["primary"]))
    o.append(B.axes(tk((0, 0.5, 1), "{:.1f}"), tk((0, 0.6, 1.2), "{:.1f}"), "t/T", "ζ(t)"))
    o.append(B.curve(tau, zeta, SER[2], multi=True))
    o.append(dot(B, 0, 0, I["primary"], r=4))
    o.append(dot(B, 1, 0, I["primary"], r=4))
    o.append(label(s, B.X(0.5), B.Y(1.0) - 12, "ζ = 64[τ(1−τ)]³", "label2", I["primary"], "middle"))
    o.append(label(s, 62, 410, "ζ, ζ′, ζ″ = 0 at both ends (p = 3)", "label2", I["secondary"]))
    aria = ("Problem D1. Top: a minimizer x(t) (red, the minimum-jerk S-curve) and the perturbed curve x plus epsilon zeta (blue, "
            "epsilon 0.12) from the same start and end. Bottom: the perturbation zeta equals 64 times tau(1 minus tau) cubed, zero "
            "at both ends together with its first and second derivatives, as required for p equal to 3.")
    pa = hov(A, tau, [x + eps * zeta, x], lambda i: f"t/T = {tau[i]:.3f}: x = {x[i]:.3f}, x + εζ = {x[i] + eps * zeta[i]:.3f}")
    pb = hov(B, tau, [zeta], lambda i: f"t/T = {tau[i]:.3f}: ζ = {zeta[i]:.3f}")
    return frame_svg(VB, aria, s, o, ([(A.box, pa), (B.box, pb)],))


# ================================================================ #30 D2: the minimum-jerk polynomial
def fig30():
    VB = (0, 0, W, 296)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (62, 44, 388, 232), (0, 1), (0, 1))
    tau = np.linspace(0, 1, 201)
    cub = 3 * tau ** 2 - 2 * tau ** 3
    o = [legend(s, 62, 24, [(SER[0], "quintic 10τ³−15τ⁴+6τ⁵", None), (SER[1], "cubic 3τ²−2τ³", (7, 4))], gap=14)]
    o.append(P.axes(tk((0, 0.5, 1), "{:.1f}"), tk((0, 0.5, 1), "{:.1f}"), "τ = t/T", "x/D", grid=(0.5,)))
    o.append(P.curve(tau, cub, SER[1], multi=True, dash=(7, 4)))
    o.append(P.curve(tau, mj_x(tau), SER[0]))
    for a, b in ((0, 0), (1, 1)):
        o.append(dot(P, a, b, O["flag"], r=5))
    o.append(label(s, P.X(0.36), P.Y(0.1), f"τ = 0: x = 0, {xd(1, ' = ')}{xd(2, ' = 0')}", "label2", I["primary"]))
    o.append(label(s, P.X(0.64), P.Y(0.92), f"τ = 1: x = D, {xd(1, ' = ')}{xd(2, ' = 0')}", "label2", I["primary"], "end"))
    o.append(label(s, 62, 284, "six conditions, six coefficients: degree 5", "label2", I["secondary"]))
    aria = ("Problem D2. The normalised position x over D against tau from 0 to 1: the minimum-jerk quintic 10 tau cubed minus 15 "
            "tau to the fourth plus 6 tau to the fifth (red), an S-curve through 0 and 1 with zero velocity and acceleration "
            "at both ends (orange dots), and a dashed blue cubic 3 tau squared minus 2 tau cubed that has zero velocity but not "
            "zero acceleration at its ends.")
    pts = hov(P, tau, [mj_x(tau), cub], lambda i: f"τ = {tau[i]:.3f}: quintic {mj_x(tau[i]):.3f}, cubic {cub[i]:.3f}")
    return frame_svg(VB, aria, s, o, (P.box, pts))


# ================================================================ #31 D3: the 1.875 ratio
def fig31():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (62, 36, 388, 196), (0, 1), (0, 2))
    tau = np.linspace(0, 1, 201)
    v = mj_v(tau)
    o = [P.axes(tk((0, 0.5, 1), "{:.1f}"), tk((0, 1, 2)), "τ = t/T", "v·T/D", grid=(2,))]
    o.append(hline(s, P, 1.0))
    o.append(P.curve(tau, v, SER[0]))
    o.append(dot(P, 0.5, 1.875, O["flag"], r=5))
    o.append(label(s, P.X(0.5) + 10, P.Y(1.875) - 8, "peak 30/16 = 1.875 at τ = ½", "label2", I["primary"]))
    o.append(label(s, P.X(0.5), P.Y(0.7), "mean speed = 1 (D/T)", "label2", I["primary"], "middle"))
    o.append(label(s, 62, 254, "v·T/D = 30 τ²(1−τ)²; peak-to-mean ratio 1.875", "label2", I["secondary"]))
    aria = ("Problem D3. The normalised speed v T over D against tau from 0 to 1, a symmetric bell 30 tau squared times (1 minus "
            "tau) squared with its peak 1.875 at tau one half (orange dot), and a dashed line at the mean speed 1.")
    pts = hov(P, tau, [v], lambda i: f"τ = {tau[i]:.3f}: v·T/D = {v[i]:.3f}")
    return frame_svg(VB, aria, s, o, (P.box, pts))


# ================================================================ block-diagram helpers
def bx(s, x, y, w, h, lines, accent, sizes=None):
    o = [f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="6" fill="{BOX}" stroke="{I["rule"]}" stroke-width="1"/>',
         f'<rect x="{x:.2f}" y="{y:.2f}" width="5" height="{h:.2f}" rx="2" fill="{accent}"/>']
    n = len(lines)
    for k, ln in enumerate(lines):
        sz = (sizes or ["label"] * n)[k]
        yy = y + h / 2 + (k - (n - 1) / 2) * 20 + 5
        o.append(H.label(s, x + w / 2 + 2, yy, ln, sz, I["primary"], "middle"))
    return "".join(o)


def sum_node(s, x, y, r, sign):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{I["axis"]}" stroke-width="{s(1.4):.2f}"/>'
            + H.label(s, x, y + s(5.5), sign, "label", I["primary"], "middle"))


# ================================================================ #32 D4: HJB to gain and Riccati
def fig32():
    VB = (0, 0, W, 372)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m12f32_"
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o.append(bx(s, 20, 14, 360, 52, ["value function", "V(x) = xᵀP x"], SER[2]))
    o.append(H.arrow(s, p, 200, 70, 200, 98, "dim", w="ref"))
    o.append(bx(s, 20, 102, 360, 76, ["HJB equation, minimise over u:", "0 = min [ xᵀQx + uᵀRu + 2xᵀP(Ax + Bu) ]"], SER[1],
                ["label", "label2"]))
    o.append(H.arrow(s, p, 110, 182, 110, 210, "dim", w="ref"))
    o.append(H.arrow(s, p, 290, 182, 290, 210, "dim", w="ref"))
    o.append(H.label(s, 104, 198, "∂/∂u = 0", "label2", I["secondary"], "end"))
    o.append(H.label(s, 296, 198, "substitute u", "label2", I["secondary"]))
    o.append(bx(s, 20, 214, 172, 112, ["optimal feedback", "u = −R⁻¹BᵀP x", "= −K x"], SER[0], ["label", "label2", "label2"]))
    o.append(bx(s, 208, 214, 172, 112, ["true for all x, so", "AᵀP + PA", "− PBR⁻¹BᵀP + Q = 0"], SER[3],
                ["label", "label2", "label2"]))
    o.append(H.label(s, 106, 348, "gain K", "label", I["primary"], "middle"))
    o.append(H.label(s, 294, 348, "algebraic Riccati equation", "label2", I["primary"], "middle"))
    aria = ("Problem D4, a derivation chain. The value function V of x equals x transpose P x. It enters the Hamilton-Jacobi-Bellman "
            "equation, zero equals the minimum over u of x transpose Q x plus u transpose R u plus 2 x transpose P times (A x plus B "
            "u). Setting the derivative with respect to u to zero gives the feedback u equals minus R inverse B transpose P x, "
            "minus K x. Substituting and requiring the result for all x gives the algebraic Riccati equation A transpose P plus P A "
            "minus P B R inverse B transpose P plus Q equals zero.")
    return frame_svg(VB, aria, s, o)


# ================================================================ #34 D6: reafference cancellation
def fig34():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m12f34_"
    sh2 = hat("s", sub("self", s, "label2"), dx=-0.45)
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    ay, by = 64, 176
    o.append(bx(s, 8, ay - 22, 84, 44, ["command u"], SER[2], ["label2"]))
    o.append(H.arrow(s, p, 94, ay, 112, ay, "dim", w="ref"))
    o.append(bx(s, 116, ay - 22, 108, 44, [f"s{sub('self', s, 'label2')}(u)"], SER[0], ["label"]))
    o.append(H.arrow(s, p, 226, ay, 250, ay, "dim", w="ref"))
    o.append(sum_node(s, 262, ay, 12, "+"))
    o.append(H.arrow(s, p, 262, 22, 262, ay - 14, "dim", w="ref"))
    o.append(H.label(s, 270, 26, "s" + sub("ext", s, "label2") + " + ν", "label2", I["primary"]))
    o.append(H.arrow(s, p, 262, ay + 14, 262, by - 14, "dim", w="ref"))
    o.append(H.label(s, 270, 124, "measured s", "label2", I["primary"]))
    o.append(H.line(s, 50, ay + 22, 50, by, I["axis"], "ref"))
    o.append(H.label(s, 58, 124, "efference copy", "label2", I["primary"]))
    o.append(H.arrow(s, p, 50, by, 112, by, "dim", w="ref"))
    o.append(bx(s, 116, by - 22, 108, 44, ["forward model"], SER[1], ["label2"]))
    o.append(H.arrow(s, p, 226, by, 248, by, "dim", w="ref"))
    o.append(H.label(s, 238, by - 10, sh2, "label2", I["primary"], "middle"))
    o.append(sum_node(s, 262, by, 12, "−"))
    o.append(H.arrow(s, p, 276, by, 306, by, "dim", w="ref"))
    o.append(bx(s, 310, by - 28, 80, 56, ["residual r", f"= s{sub('ext', s, 'label2')} + ν"], SER[3], ["label2", "label2"]))
    o.append(H.label(s, 14, 236, "if the prediction is off by Δ: r = s" + sub("ext", s, "label2") + " + ν + Δ", "label2", I["secondary"]))
    aria = ("Problem D6, a signal-flow diagram. The command u produces the self-generated sensation s-self of u, which is added to "
            "the external sensation s-ext plus noise nu to give the measured sensation s. In parallel an efference copy of u "
            "feeds a forward model that predicts s-hat self, which is subtracted from s. The residual is r equals s-ext plus nu; "
            "a prediction error Delta would remain in r.")
    return frame_svg(VB, aria, s, o)


# ================================================================ #35 D7: adaptation dynamics
def fig35():
    VB = (0, 0, W, 422)
    s = H.Scale(W, VB[3], display_w=400)
    A = Plot(s, (62, 52, 388, 176), (0, 20), (-1.5, 1.5))
    B = Plot(s, (62, 262, 388, 358), (0, 30), (-1.2, 1.5))
    n = np.arange(0, 21)
    cases = [(0.3, SER[0]), (1.6, SER[1]), (2.1, SER[2])]
    o = [legend(s, 62, 24, [(c, f"ηg = {a:g}", None) for a, c in cases], gap=14)]
    o.append(A.axes(tk((0, 5, 10, 15, 20)), tk((-1, 0, 1)), "trial n", "error eₙ/e₀", grid=(0,)))
    ends = {}
    for a, c in cases:
        e = (1 - a) ** n
        ok = np.abs(e) <= 1.5
        o.append(A.curve(n[ok], e[ok], c, multi=True))
        for k in n[ok]:
            o.append(dot(A, k, e[k], c, r=2.4))
        ends[a] = (int(n[ok][-1]), e[ok][-1])
    o.append(label(s, A.X(20) - 4, A.Y(0.7 ** 6) - 14, "0 < ηg < 2: converges", "label2", I["primary"], "end"))
    o.append(label(s, A.X(ends[2.1][0]) + 8, A.Y(ends[2.1][1]) + 4, "ηg > 2: grows", "label2", I["primary"]))
    # panel B: adapt, then remove the perturbation
    eta_g, N0, g, pp = 0.3, 15, 1.0, 1.0
    eta = eta_g / g
    nn = np.arange(0, 31)
    u, ee = 0.0, []
    for k in nn:
        pert = pp if k < N0 else 0.0
        e_k = g * (pert - u)
        ee.append(e_k)
        u += eta * e_k
    ee = np.array(ee)
    assert abs(ee[N0] - (-(1 - 0.7 ** N0))) < 1e-12 and ee[N0] < -0.99 * g * pp         # first error after removal -> -p g
    o.append(B.axes(tk((0, 10, 20, 30)), tk((-1, 0, 1)), "trial n", "error eₙ (units of p·g)", grid=(0,)))
    o.append(H.line(s, B.X(N0 - 0.5), B.y1, B.X(N0 - 0.5), B.y0, I["secondary"], "ref", H.DASH_REF))
    o.append(B.curve(nn, ee, SER[0], multi=True))
    for k in nn:
        o.append(dot(B, k, ee[k], SER[0], r=2.4))
    o.append(label(s, B.X(N0 - 0.5) - 6, B.Y(1.2), "perturbation on", "label2", I["primary"], "end"))
    o.append(label(s, B.X(N0 - 0.5) + 6, B.Y(1.2) - 2, "removed at n = 15:", "label2", I["primary"]))
    o.append(label(s, B.X(N0 - 0.5) + 6, B.Y(1.2) + 14, f"first error {mn(ee[N0], '{:.2f}')} ≈ −p·g", "label2", I["primary"]))
    o.append(label(s, 62, 410, "eₙ = (1−ηg)ⁿ e₀; lower panel: ηg = 0.3", "label2", I["secondary"]))
    aria = ("Problem D7, two panels. Top: the error ratio e n over e 0 against trial n from 0 to 20 for eta g equal to 0.3 "
            "(red, monotone decay), 1.6 (blue, decaying with alternating sign) and 2.1 (orange, alternating sign and growing, "
            "leaving the scale after trial 4). Bottom: with eta g 0.3 the error decays over 15 trials of a constant perturbation, "
            "then the perturbation is removed and the first error jumps to about minus p g, the aftereffect, and decays again.")
    pa = hov(A, n, [(1 - 0.3) ** n, (1 - 1.6) ** n, np.clip((1 - 2.1) ** n, -9, 9)],
             lambda i: f"n = {n[i]}: ηg 0.3: {mn((1 - 0.3) ** n[i], '{:.3f}')}, 1.6: {mn((1 - 1.6) ** n[i], '{:.3f}')}, "
                       f"2.1: {mn((1 - 2.1) ** n[i], '{:.2f}')}")
    pb = hov(B, nn, [ee], lambda i: f"n = {nn[i]}: error {mn(ee[i], '{:.3f}')} (units of p·g)")
    return frame_svg(VB, aria, s, o, ([(A.box, pa), (B.box, pb)],))


FIGS = {
    20: ("C2: fast or slow, same shape. A reach's speed profile is a s", fig20),
    23: ("C5: the servo against the wall. Why is a stiff, high-gain po", fig23),
    24: ("C6: the opposite error. After training in a force field, rem", fig24),
    25: ("C7: variable but accurate. A pianist's finger follows a slig", fig25),
    28: ("C10: why gains stay finite. The LQR says lower effort cost g", fig28),
    29: ("D1: the Euler-Poisson equation. Derive the necessary conditi", fig29),
    30: ("D2: the minimum-jerk polynomial. Show the jerk-minimizing tr", fig30),
    31: ("D3: the 1.875 ratio. Derive the peak speed of a minimum-jerk", fig31),
    32: ("D4: the LQR gain. Derive the optimal LQR feedback and the al", fig32),
    34: ("D6: reafference cancellation. Show that subtracting a forwar", fig34),
    35: ("D7: adaptation dynamics. Derive the trial-to-trial error rec", fig35),
}
