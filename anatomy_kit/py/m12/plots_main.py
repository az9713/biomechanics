"""Module 12 main-text plots and block diagrams in the house style (group `plots_main`).

svg #3 (three nested levels of redundancy), #4 (minimum-jerk reach, Lab A), #5 (LQR recovery, Lab B), #7 (internal-model
loop), #8 (uncontrolled-manifold ellipse), #9 (Adler equation), #10 (the whole architecture), #12 (scale invariance),
#14 (LQR gain and settling time against R), #16 (contact force, Lab C), #18 (Lab D scatter).
Every plotted number is computed here from what module12.html states: Prop. 3.1 and the Lab A code (line 266 on), the Lab B
code and its closed forms K = (R^-1/2, sqrt2 R^-1/4), t_s = 4 sqrt2 R^1/4 (line 322 on), the Lab C code (line 362 on),
the Lab D code (line 384 on), Prop. 7.2 and Prop. 8.2 (Adler equation).
All figures use a 760-unit-wide viewBox, so one user unit is one rendered px.
"""
import math

import numpy as np

import house as H
from m05.plots_main import DASH_SER, GRID, Ax, axes, poly, dot, legend, mn, svg
from m05.schematic import box

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
SEC = "label2"


def sub(t, s):
    return H.sub(t, s, SEC)


def sup(t, s):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[SEC] * 0.7):.2f}">{t}</tspan>'


def it(t):
    return f'<tspan font-style="italic">{t}</tspan>'


def ticks(vals, f="{:g}"):
    return [(v, mn(v, f)) for v in vals]


def hat(sym, rest="", em=0.38, dx=-0.6):
    """Spacing-modifier hat (Georgia has no combining marks in SVG): the caret is moved by dx/dy and dy is reset."""
    return (f'{sym}<tspan dx="{dx}em" dy="-{em}em">ˆ</tspan><tspan dy="{em}em">{rest}</tspan>')


def hpts(xs, ys, texts):
    """[[x, y or [y...], text], ...] in user units, sorted by x."""
    pts = [[x, y, t] for x, y, t in zip(xs, ys, texts)]
    pts.sort(key=lambda q: q[0])
    return pts


def hov(ax, xs, ys, texts):
    return H.hover_attr([round(v, 1) for v in ax.box], hpts(xs, ys, texts))


# ================================================================ Lab A: minimum jerk (Prop. 3.1, text line 266 on)
D_A, T_A = 0.40, 0.50


def minjerk(D, Tm, n=201):
    t = np.linspace(0, Tm, n)
    tau = t / Tm
    x = D * (10 * tau ** 3 - 15 * tau ** 4 + 6 * tau ** 5)
    v = D / Tm * (30 * tau ** 2 - 60 * tau ** 3 + 30 * tau ** 4)
    a = D / Tm ** 2 * (60 * tau - 180 * tau ** 2 + 120 * tau ** 3)
    return t, x, v, a


_t, _x, _v, _a = minjerk(D_A, T_A, 401)
assert abs(_v.max() - 1.5) < 1e-3 and abs(1.875 * D_A / T_A - 1.5) < 1e-12           # peak speed 1.5 m/s = 1.875 D/T
assert abs(_a.max() - 9.24) < 1e-2 and abs(5.77 * D_A / T_A ** 2 - 9.24) < 1e-2       # peak accel 9.24 m/s^2 = 5.77 D/T^2
TAU_PK = (3 - math.sqrt(3)) / 6                                                         # 0.2113: zeros of d(a)/d(tau)
assert abs(_a.max() - D_A / T_A ** 2 * (60 * TAU_PK - 180 * TAU_PK ** 2 + 120 * TAU_PK ** 3)) < 0.02


# ================================================================ svg #3: three nested levels of redundancy (Fig. 2)
def fig3():
    VB = (0, 0, 760, 390)
    s = H.Scale(VB[2], VB[3])
    p = "m12f3_"
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    x, bw, bh = 20, 452, 58
    ys = [24, 120, 216, 312]                                                           # top = task, bottom = motor units
    rows = [("hand pose", "task variables: m = 3 (position) or m = 6 (position and orientation)", O["load"]),
            ("joint angles q", "n = 7: shoulder 3, elbow 1, forearm rotation 1, wrist 2", O["geometry"]),
            ("muscle forces", "roughly 50 muscles cross the shoulder, elbow, forearm and wrist", O["force"]),
            ("motor-unit activity", "hundreds to thousands of motor units in each muscle", O["neural"])]
    for (name, note, col), y in zip(rows, ys):
        o.append(box(s, x, y, bw, bh, col))
        o.append(H.label(s, x + 18, y + 24, name, "label", I["primary"]))
        o.append(H.label(s, x + 18, y + 44, note, SEC, I["secondary"]))
    maps = [("kinematics: p = f(q)", "kinematic redundancy", "null space of the Jacobian J,",
             "n − m = 4 (position)", "or 1 (full pose)"),
            ("muscle forces to joint torques", "actuation redundancy", "more muscles than joints:",
             "roughly 50 − 7 = 43", "spare"),
            ("motor-unit activity to muscle force", "neural redundancy", "many motor units",
             "drive each muscle", "")]
    xm = x + 58
    for k, (m1, m2, m3, m4, m5) in enumerate(maps):
        ya, yb = ys[k + 1], ys[k]                                                      # arrow runs up from level k+1 to level k
        o.append(H.arrow(s, p, xm, ya - 3, xm, yb + bh + 4, "dim", w="ref"))
        o.append(H.label(s, xm + 12, (ya + yb + bh) / 2 + 5, m1, SEC, I["secondary"]))
        yt = (ya + yb + bh) / 2 - 10
        o.append(H.label(s, 500, yt, m2, "label", I["primary"]))
        o.append(H.label(s, 500, yt + 18, m3, SEC, I["secondary"]))
        o.append(H.label(s, 500, yt + 34, m4, SEC, I["primary"]))
        if m5:
            o.append(H.label(s, 500, yt + 50, m5, SEC, I["primary"]))
    o.append(H.label(s, 500, 50, "each level has more variables", "label2", I["muted"]))
    o.append(H.label(s, 500, 67, "than the one above it", "label2", I["muted"]))
    aria = ("Three nested levels of redundancy drawn as four stacked boxes with arrows pointing up. From the bottom: "
            "motor-unit activity (hundreds to thousands of motor units in each muscle), muscle forces (roughly 50 muscles), "
            "joint angles q (n = 7), hand pose (m = 3 for position, 6 for position and orientation). Each upward map has a "
            "null space: the Jacobian null space of dimension n minus m, which is 4 for position and 1 for full pose; the "
            "muscles-to-torques map, with roughly 43 spare; and the motor-unit-to-force map.")
    return svg(VB, aria, s, o)


# ================================================================ svg #4: minimum-jerk reach (Fig. 3, Lab A)
def fig4():
    VB = (0, 0, 760, 508)
    s = H.Scale(VB[2], VB[3])
    p = "m12f4_"
    x0, x1 = 100, 720
    tx = (0, T_A)
    A1 = Ax((x0, 26, x1, 138), tx, (0, 0.46))
    A2 = Ax((x0, 188, x1, 300), tx, (0, 1.95))
    A3 = Ax((x0, 350, x1, 462), tx, (-17, 17))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, A1, [], ticks((0, 0.2, 0.4), "{:.1f}"), None, "position (m)", ylab_x=x0 - 56)
    o += axes(s, A2, [], ticks((0, 0.5, 1.0, 1.5), "{:.1f}"), None, "speed (m/s)", ylab_x=x0 - 56)
    o += axes(s, A3, ticks((0, 0.1, 0.2, 0.3, 0.4, 0.5), "{:.1f}"), ticks((-9, 0, 9)), "time t (s)", "accel. (m/s²)",
              ylab_x=x0 - 56, xlab_dy=42, grid=False)
    o.append(H.line(s, A3.x0, A3.Y(0), A3.x1, A3.Y(0), I["rule"], "leader"))
    xm = A1.X(T_A / 2)
    o.append(H.line(s, xm, A1.top, xm, A3.y0, I["rule"], "ref", H.DASH_REF))
    o.append(poly(s, [(A1.X(a), A1.Y(b)) for a, b in zip(_t, _x)], SER[0], "curve"))
    o.append(poly(s, [(A2.X(a), A2.Y(b)) for a, b in zip(_t, _v)], SER[1], "curve"))
    o.append(poly(s, [(A3.X(a), A3.Y(b)) for a, b in zip(_t, _a)], SER[2], "curve"))
    # direct labels and peak marks (computed positions)
    o.append(H.label(s, A1.X(0.30), A1.Y(0.13), f"{it('D')} = {D_A:.1f} m in {it('T')} = {T_A:.1f} s", "label2", I["primary"]))
    o.append(dot(s, xm, A2.Y(_v.max()), SER[1], r=5))
    o.append(H.label(s, xm + 12, A2.Y(_v.max()) - 10, f"peak {_v.max():.1f} m/s = 1.875 {it('D/T')} at {it('τ')} = 0.5", "label2", I["primary"]))
    k1, k2 = int(_a.argmax()), int(_a.argmin())
    o.append(dot(s, A3.X(_t[k1]), A3.Y(_a[k1]), SER[2], r=5))
    o.append(dot(s, A3.X(_t[k2]), A3.Y(_a[k2]), SER[2], r=5))
    o.append(H.label(s, xm - 14, A3.Y(_a[k1]) - 10, f"+{_a[k1]:.2f} m/s² = 5.77 {it('D/T')}{sup('2', s)} at {it('τ')} = {_t[k1] / T_A:.2f}",
                     "label2", I["primary"], "end"))
    o.append(H.label(s, A3.X(_t[k2]), A3.Y(_a[k2]) + 22, f"−{abs(_a[k2]):.2f} m/s² at {it('τ')} = {_t[k2] / T_A:.2f}", "label2",
                     I["primary"], "middle"))
    o.append(dot(s, xm, A3.Y(0), I["primary"], r=3.5))
    o.append(H.label(s, xm + 10, A3.Y(0) - 7, "a = 0 at the speed peak", "label2", I["secondary"]))
    aria = ("Three stacked panels against time from 0 to 0.5 seconds for a minimum-jerk reach of 0.4 m in 0.5 s. Top: position, "
            "a smooth S-curve from 0 to 0.4 m, in red. Middle: speed, a symmetric bell peaking at 1.5 m/s, which is 1.875 times "
            "D over T, at mid-movement, in blue. Bottom: acceleration, an antisymmetric wave peaking at plus and minus 9.24 "
            "m/s squared near tau 0.21 and 0.79 and crossing zero at mid-movement, in orange. A dashed vertical line marks mid-movement.")
    hv = H.hover_attr([(A1.box, hpts([A1.X(a) for a in _t], [A1.Y(b) for b in _x],
                                     [f"t = {a:.3f} s: position {b:.3f} m" for a, b in zip(_t, _x)])),
                       (A2.box, hpts([A2.X(a) for a in _t], [A2.Y(b) for b in _v],
                                     [f"t = {a:.3f} s: speed {b:.3f} m/s" for a, b in zip(_t, _v)])),
                       (A3.box, hpts([A3.X(a) for a in _t], [A3.Y(b) for b in _a],
                                     [f"t = {a:.3f} s: acceleration {mn(b, '{:.2f}')} m/s²" for a, b in zip(_t, _a)]))])
    return svg(VB, aria, s, o, hv)


# ================================================================ Lab B: LQR (text lines 322-345)
def lqr_gain(R):
    """Riccati solution for the double integrator, Q = diag(1, 0): K = [R^-1/2, sqrt2 R^-1/4]."""
    return np.array([R ** -0.5, math.sqrt(2) * R ** -0.25])


def lqr_euler(R, n=500, t_end=10.0):
    """Lab B loop, verbatim: Euler on x' = (A - B K) x from x = [1, 0] with dt = t[1] - t[0]."""
    A = np.array([[0.0, 1.0], [0.0, 0.0]])
    B = np.array([[0.0], [1.0]])
    K = lqr_gain(R).reshape(1, 2)
    t = np.linspace(0, t_end, n)
    dt = t[1] - t[0]
    x = np.array([1.0, 0.0])
    xs = []
    for _ in t:
        x = x + dt * (A - B @ K) @ x
        xs.append(x[0])
    return t, np.array(xs), K.flatten(), np.linalg.eigvals(A - B @ K)


def settle(R):
    return 4 * math.sqrt(2) * R ** 0.25


try:                                                                                    # check the closed form against SciPy
    from scipy.linalg import solve_continuous_are
    for _R in (0.01, 1.0, 100.0):
        _P = solve_continuous_are(np.array([[0.0, 1.0], [0.0, 0.0]]), np.array([[0.0], [1.0]]), np.diag([1.0, 0.0]),
                                  np.array([[_R]]))
        assert np.allclose(np.array([0.0, 1.0]) @ _P / _R, lqr_gain(_R), atol=1e-8)
except ImportError:                                                                     # pragma: no cover
    pass
assert np.allclose(lqr_gain(100), [0.1, 0.45], atol=0.005) and np.allclose(lqr_gain(0.01), [10, 4.5], atol=0.05)   # line 337
assert abs(settle(0.01) - 1.79) < 0.005 and abs(settle(100) - 17.9) < 0.05                                           # line 326


def fig5():
    VB = (0, 0, 760, 392)
    s = H.Scale(VB[2], VB[3])
    p = "m12f5_"
    ax = Ax((90, 30, 722, 312), (0, 10), (-0.1, 1.05))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, ax, ticks((0, 2, 4, 6, 8, 10)), ticks((0, 0.5, 1.0), "{:.1f}"), "time t (s)", "position error (m)",
              ylab_x=ax.x0 - 56, xlab_dy=44)
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["axis"], "ref"))
    runs = [(0.01, SER[0], "cheap effort"), (1.0, SER[2], ""), (100.0, SER[1], "dear effort")]
    data = []
    for R, col, _ in runs:
        t, x, K, lam = lqr_euler(R)
        data.append((R, col, t, x, K, lam))
        o.append(poly(s, [(ax.X(a), ax.Y(b)) for a, b in zip(t[::2], x[::2])], col, "curve_multi" if R == 1.0 else "curve"))
    # legend column: swatch, R, then gains and 2 % settling time (text ink, swatch carries the identity)
    lx, ly = 478, 62
    for k, (R, col, t, x, K, lam) in enumerate(data):
        y = ly + k * 52
        o.append(f'<line x1="{lx}" y1="{y - 4}" x2="{lx + 24}" y2="{y - 4}" stroke="{col}" stroke-width="{s(H.PX["curve_multi"]):.2f}"/>')
        tag = {0.01: " (cheap effort)", 1.0: "", 100.0: " (dear effort)"}[R]
        o.append(H.label(s, lx + 32, y, f"{it('R')} = {R:g}{tag}", "label", I["primary"]))
        o.append(H.label(s, lx + 32, y + 18, f"{it('K')} = [{K[0]:.2g}, {K[1]:.2g}],  {it('t')}{sub('s', s)} = {settle(R):.3g} s",
                         "label2", I["secondary"]))
    aria = ("Position error of a point-mass hand against time from 0 to 10 seconds after a one-metre error, under LQR feedback "
            "for three effort weights R. R = 0.01 (cheap effort, red): gain K = [10, 4.5], settles in 1.79 s with a small "
            "undershoot. R = 1 (orange): K = [1, 1.41], settles in 5.66 s. R = 100 (dear effort, blue): K = [0.1, 0.45], "
            "settles in 17.9 s and has only fallen to about 0.01 m by 10 s.")
    hx = data[0][2]
    hv = hov(ax, [ax.X(a) for a in hx], [[ax.Y(d[3][i]) for d in data] for i in range(len(hx))],
             [f"t = {hx[i]:.2f} s: error R=0.01 {mn(data[0][3][i], '{:.3f}')} m, R=1 {mn(data[1][3][i], '{:.3f}')} m, "
              f"R=100 {mn(data[2][3][i], '{:.3f}')} m" for i in range(len(hx))])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #7: the internal-model loop (Fig. 6, Prop. 6.1)
def fig7():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    p = "m12f7_"
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    bh, ym = 70, 190                                                                    # main row: centre line y = 190 + 35
    yc = ym + bh / 2
    B = {"ctl": (112, 150, "controller", "feedback laws, §4–§5", O["neural"]),
         "plant": (330, 140, "plant (the arm)", "", O["force"]),
         "sens": (540, 170, "sensors, delay Δ", "100–200 ms (Module 10)", I["rule"])}
    for k, (x, w, n1, n2, col) in B.items():
        o.append(box(s, x, ym, w, bh, col))
        o.append(H.label(s, x + w / 2 + 2, ym + (28 if n2 else 41), n1, "label", I["primary"], "middle"))
        if n2:
            o.append(H.label(s, x + w / 2 + 2, ym + 50, n2, SEC, I["secondary"], "middle"))
    fx, fw, fy, fh = 250, 220, 38, 66                                                   # forward model on top
    o.append(box(s, fx, fy, fw, fh, O["geometry"]))
    o.append(H.label(s, fx + fw / 2 + 2, fy + 27, "forward model", "label", I["primary"], "middle"))
    o.append(H.label(s, fx + fw / 2 + 2, fy + 47, "predicts state and sensation", SEC, I["secondary"], "middle"))
    xc = 60                                                                             # estimate junction left of the controller
    r = 14
    o.append(f'<circle cx="{xc}" cy="{yc}" r="{r}" fill="#fff" stroke="{I["axis"]}" stroke-width="{s(1.4):.2f}"/>')
    o.append(H.label(s, xc, yc + 5, "+", "label", I["primary"], "middle"))
    xs_, ysb = 625, 300                                                                 # subtractor under the sensors
    o.append(f'<circle cx="{xs_}" cy="{ysb}" r="{r}" fill="#fff" stroke="{I["axis"]}" stroke-width="{s(1.4):.2f}"/>')
    o.append(H.label(s, xs_, ysb + 5, "−", "label", I["primary"], "middle"))
    # main row arrows
    o.append(H.arrow(s, p, xc + r + 3, yc, 108, yc, "neural"))
    o.append(H.arrow(s, p, 264, yc, 326, yc, "neural"))
    o.append(H.label(s, 279, yc - 10, "u", "label", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.arrow(s, p, 472, yc, 536, yc, "dim", w="ref"))
    # efference copy: branch off u, up into the forward model
    xb = 295
    o.append(f'<circle cx="{xb}" cy="{yc}" r="{s(3.5):.2f}" fill="{I["primary"]}"/>')
    o.append(H.arrow(s, p, xb, yc - 4, xb, fy + fh + 4, "geometry"))
    o.append(H.label(s, xb + 10, 148, "efference copy of u", SEC, I["primary"]))
    # predicted state: forward model left output, along the top, down to the estimate junction
    yo = fy + fh / 2
    o.append(H.line(s, fx, yo, xc, yo, O["geometry"], "geom"))
    o.append(H.arrow(s, p, xc, yo, xc, yc - r - 3, "geometry"))
    o.append(H.label(s, 156, yo - 8, hat("x", ", predicted current state"), SEC, I["primary"], "middle"))
    # predicted self-sensation: right output, along the top, down to the subtractor
    xr = 730
    o.append(H.line(s, fx + fw, yo, xr, yo, O["geometry"], "geom"))
    o.append(H.line(s, xr, yo, xr, ysb, O["geometry"], "geom"))
    o.append(H.arrow(s, p, xr, ysb, xs_ + r + 3, ysb, "geometry"))
    o.append(H.label(s, 590, yo - 8, hat("s", sub("self", s) + ", predicted self-sensation", 0.34, -0.47), SEC, I["primary"], "middle"))
    # sensed signal down into the subtractor, residual back to the junction
    o.append(H.arrow(s, p, xs_, ym + bh + 3, xs_, ysb - r - 3, "dim", w="ref"))
    o.append(H.label(s, xs_ - 10, 276, f"s = s{sub('self', s)} + s{sub('ext', s)} + ν", SEC, I["primary"], "end"))
    o.append(H.line(s, xs_ - r - 3, ysb, xc, ysb, O["dim"], "ref"))
    o.append(H.arrow(s, p, xc, ysb, xc, yc + r + 3, "dim", w="ref"))
    o.append(H.label(s, 342, ysb - 10, f"residual r = s − s{sub('self', s)} = s{sub('ext', s)} + ν   (Prop. 6.1)", SEC, I["primary"], "middle"))
    o.append(H.label(s, 342, ysb + 28, "an inverse model (not shown) supplies the feedforward command", SEC, I["muted"], "middle"))
    aria = ("Block diagram of the internal-model loop. A controller sends the command u to the plant, the arm, whose output "
            "reaches the sensors after a delay of 100 to 200 ms. The sensed signal s, the sum of a self-generated part, an external "
            "part and noise, goes to a subtractor. A forward model, fed an efference copy of u, sends a predicted current state "
            "x-hat to an estimate junction in front of the controller and a predicted self-sensation to the subtractor. The "
            "residual r, which is only the external part plus noise, returns to the estimate junction. An inverse model is not shown.")
    return svg(VB, aria, s, o)


# ================================================================ svg #8 and #18: uncontrolled manifold (Prop. 7.2, Lab D)
SIG, RHO, N_TR, N_SHOW = 1.0, 0.15, 4000, 500


def labd():
    """Lab D code, verbatim."""
    rng = np.random.default_rng(0)
    n1 = rng.normal(0, SIG, N_TR)
    n2 = rng.normal(0, SIG, N_TR)
    task = n1 + n2
    corr = (1 - np.sqrt(RHO)) * task / 2
    y1, y2 = n1 - corr, n2 - corr
    return y1, y2, y1 + y2, y1 - y2


_y1, _y2, _tt, _nn = labd()
VAR_T, VAR_N = float(np.var(_tt)), float(np.var(_nn))
assert round(VAR_T, 2) == 0.30 and round(VAR_N, 2) == 2.01 and round(VAR_N / VAR_T, 2) == 6.65      # caption and line 395
assert abs(1 / RHO - 6.67) < 0.005


def ell_pts(k, n=181):
    """k-sigma ellipse of the (y1, y2) cloud (Prop. 7.2): null axis along (1, -1) with std sigma, task axis along (1, 1) with
    std sqrt(rho) sigma (Var(n) = 2 sigma^2 and Var(t) = 2 rho sigma^2 are variances of the unnormalised sums)."""
    a, b = k * SIG, k * math.sqrt(RHO) * SIG
    th = np.linspace(0, 2 * math.pi, n)
    return (a * np.cos(th) / math.sqrt(2) + b * np.sin(th) / math.sqrt(2),
            -a * np.cos(th) / math.sqrt(2) + b * np.sin(th) / math.sqrt(2))


def fig8():
    VB = (0, 0, 760, 410)
    s = H.Scale(VB[2], VB[3])
    p = "m12f8_"
    cx, cy, U = 380, 206, 74.0                                                           # px per unit of y (equal scale on both axes)
    X = lambda v: cx + U * v          # noqa: E731
    Y = lambda v: cy - U * v          # noqa: E731
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o.append(H.line(s, X(-3.7), cy, X(3.7), cy, GRID, "ref"))
    o.append(H.line(s, cx, Y(-2.3), cx, Y(2.3), GRID, "ref"))
    o.append(H.label(s, X(3.7), cy - 8, f"{it('y')}{sub('1', s)}", "label", I["primary"], "end"))
    o.append(H.label(s, cx + 8, Y(2.3) + 8, f"{it('y')}{sub('2', s)}", "label", I["primary"]))
    for k, fo in ((2, 0.0), (1, 0.0)):
        ex, ey = ell_pts(k)
        o.append(f'<polygon points="{" ".join(f"{X(a):.2f},{Y(b):.2f}" for a, b in zip(ex, ey))}" fill="{SER[1]}" '
                 f'fill-opacity="{0.10 if k == 2 else 0.16}" stroke="{I["secondary"]}" stroke-width="{s(H.PX["curve_multi"]):.2f}" '
                 f'stroke-linejoin="round"/>')
    # uncontrolled manifold y1 + y2 = 0 (the null line) and the task direction y1 = y2
    L = 2.4
    o.append(H.line(s, X(-L), Y(L), X(L), Y(-L), O["dim"], "ref", H.DASH_REF))
    o.append(H.line(s, X(-1.5), Y(-1.5), X(1.5), Y(1.5), O["dim"], "ref", H.DASH_REF))
    # 1-sigma semi-axes
    a1 = SIG / math.sqrt(2)
    b1 = math.sqrt(RHO) * SIG / math.sqrt(2)
    o.append(H.arrow(s, p, cx, cy, X(a1), Y(-a1), "geometry"))
    o.append(H.arrow(s, p, cx, cy, X(b1), Y(b1), "geometry"))
    o.append(dot(s, cx, cy, I["primary"], r=3.5))
    # labels (null line ends lower right, task line ends upper right; the key numbers sit bottom left)
    o.append(H.label(s, X(a1) + 8, Y(-a1) - 8, "σ", "label2", I["primary"]))
    o.append(H.label(s, X(b1) + 10, Y(b1) + 20, "√ρ σ", "label2", I["primary"]))
    o.append(H.label(s, X(L) + 8, Y(-L) - 36, "null direction", "label", I["primary"]))
    o.append(H.label(s, X(L) + 8, Y(-L) - 18, "y₁ − y₂ varies; uncorrected", SEC, I["secondary"]))
    o.append(H.label(s, X(L) + 8, Y(-L), "this line, y₁ + y₂ = 0, is the", SEC, I["secondary"]))
    o.append(H.label(s, X(L) + 8, Y(-L) + 16, "uncontrolled manifold", SEC, I["secondary"]))
    o.append(H.label(s, X(1.5) + 8, Y(1.5) - 12, "task direction", "label", I["primary"]))
    o.append(H.label(s, X(1.5) + 8, Y(1.5) + 6, "y₁ + y₂ varies; feedback", SEC, I["secondary"]))
    o.append(H.label(s, X(1.5) + 8, Y(1.5) + 22, "shrinks the variance here", SEC, I["secondary"]))
    o.append(H.label(s, 16, 318, "1σ and 2σ contours of the", SEC, I["secondary"]))
    o.append(H.label(s, 16, 334, f"(y₁, y₂) outcomes; σ = {SIG:g}, ρ = {RHO:g}", SEC, I["secondary"]))
    o.append(H.label(s, 16, 350, f"1σ semi-axes: {SIG:g} (null), {math.sqrt(RHO) * SIG:.2f} (task)", SEC, I["secondary"]))
    o.append(H.label(s, 16, 374, f"Var(n)/Var(t) = 1/ρ = {1 / RHO:.2f}", "label", I["primary"]))
    aria = ("A scatter-free sketch of the uncontrolled-manifold signature in the plane of two effector outputs y1 and y2: an "
            "ellipse, drawn at one and two standard deviations, stretched along the diagonal y1 = minus y2, the null direction "
            "and the uncontrolled manifold, and squeezed along the diagonal y1 = y2, the task direction. With noise sigma = 1 "
            "and loop factor rho = 0.15 the semi-axes at one sigma are 1 and 0.39, so the variance ratio of null to task "
            "direction is one over rho, 6.67.")
    # hover: at each y1 the 2-sigma range of y2
    xs = np.linspace(-1.9, 1.9, 120)
    a2, b2 = 2 * SIG, 2 * math.sqrt(RHO) * SIG
    # ellipse in (y1,y2): (u/a2)^2 + (v/b2)^2 = 1 with u=(y1-y2)/sqrt2, v=(y1+y2)/sqrt2 ; solve for y2
    pts = []
    for x in xs:
        A_ = 0.5 / a2 ** 2 + 0.5 / b2 ** 2
        B_ = 2 * (-0.5 * x / a2 ** 2 + 0.5 * x / b2 ** 2)
        C_ = x * x * (0.5 / a2 ** 2 + 0.5 / b2 ** 2) - 1
        disc = B_ * B_ - 4 * A_ * C_
        if disc < 0:
            continue
        r1, r2 = (-B_ - math.sqrt(disc)) / (2 * A_), (-B_ + math.sqrt(disc)) / (2 * A_)
        pts.append([X(x), [Y(r1), Y(r2)], f"y₁ = {mn(x, '{:.2f}')}: the 2σ ellipse spans y₂ from {mn(r1, '{:.2f}')} to {mn(r2, '{:.2f}')}"])
    hv = H.hover_attr([X(-2.0), Y(2.0), X(2.0), Y(-2.0)], pts)
    return svg(VB, aria, s, o, hv)


def fig18():
    VB = (0, 0, 760, 486)
    s = H.Scale(VB[2], VB[3])
    p = "m12f18_"
    R = 3.2
    ax = Ax((80, 28, 80 + 416, 28 + 416), (-R, R), (-R, R))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    tk = ticks((-3, -2, -1, 0, 1, 2, 3))
    o += axes(s, ax, tk, tk, "y₁", "y₂", ylab_x=ax.x0 - 40, xlab_dy=36)
    L = R
    o.append(H.line(s, ax.X(-L), ax.Y(L), ax.X(L), ax.Y(-L), O["dim"], "ref", H.DASH_REF))
    o.append(H.line(s, ax.X(-L), ax.Y(-L), ax.X(L), ax.Y(L), O["dim"], "ref", H.DASH_REF))
    d = "".join(f"M{ax.X(a):.1f} {ax.Y(b):.1f}h0" for a, b in zip(_y1[:N_SHOW], _y2[:N_SHOW]))
    o.append(f'<path d="{d}" stroke="{SER[1]}" stroke-opacity="0.55" stroke-width="{s(5):.2f}" stroke-linecap="round" fill="none"/>')
    # right column: key numbers (ink), no text over the cloud; each direction block sits next to its dashed line's end
    rx = 522
    o.append(H.label(s, rx, 46, "task direction", "label", I["primary"]))
    o.append(H.label(s, rx, 64, "y₁ + y₂ varies; corrected", SEC, I["secondary"]))
    o.append(H.label(s, rx, 90, f"Var(t) = {VAR_T:.2f}", "label", I["primary"]))
    o.append(H.label(s, rx, 190, f"ratio Var(n)/Var(t) = {VAR_N / VAR_T:.2f}", "label", I["primary"]))
    o.append(H.label(s, rx, 208, f"prediction 1/ρ = {1 / RHO:.2f}", SEC, I["secondary"]))
    o.append(H.label(s, rx, 250, f"{N_SHOW} of {N_TR} simulated outcomes", SEC, I["secondary"]))
    o.append(H.label(s, rx, 267, f"are plotted; the variances use", SEC, I["secondary"]))
    o.append(H.label(s, rx, 284, f"all {N_TR}. σ = {SIG:g}, ρ = {RHO:g}.", SEC, I["secondary"]))
    o.append(H.label(s, rx, 380, f"Var(n) = {VAR_N:.2f}", "label", I["primary"]))
    o.append(H.label(s, rx, 408, "null direction", "label", I["primary"]))
    o.append(H.label(s, rx, 426, "y₁ − y₂ varies; uncorrected", SEC, I["secondary"]))
    aria = ("Scatter of 500 of 4000 simulated two-effector outcomes in the plane of y1 and y2, in blue, forming an ellipse "
            f"elongated along the null direction y1 equals minus y2 and squeezed along the task direction y1 equals y2. Variance "
            f"along the null variable n = y1 minus y2 is {VAR_N:.2f}, along the task variable t = y1 plus y2 it is {VAR_T:.2f}, a "
            f"ratio of {VAR_N / VAR_T:.2f} against the predicted one over rho, {1 / RHO:.2f}.")
    sel = list(range(N_SHOW))
    sel.sort(key=lambda k: _y1[k])
    hv = hov(ax, [ax.X(_y1[k]) for k in sel], [ax.Y(_y2[k]) for k in sel],
             [f"outcome {k + 1}: y₁ = {mn(_y1[k], '{:.2f}')}, y₂ = {mn(_y2[k], '{:.2f}')}" for k in sel])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #9: Adler equation (Prop. 8.2)
DW, KAPPA = 0.6, 0.7


def adler(psi, dw):
    return dw - 2 * KAPPA * np.sin(psi)


def fig9():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    p = "m12f9_"
    ax = Ax((90, 36, 722, 310), (-math.pi, math.pi), (-1.6, 3.4))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    xt = [(v, mn(v, "{:g}") if v == 0 else lab) for v, lab in ((-math.pi, "−π"), (-math.pi / 2, "−π/2"), (0, "0"),
                                                                  (math.pi / 2, "π/2"), (math.pi, "π"))]
    o += axes(s, ax, xt, ticks((-1, 0, 1, 2, 3)), "phase difference ψ (rad)", "dψ/dt (rad/s)", ylab_x=ax.x0 - 46, xlab_dy=44)
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["rule"], "ref"))
    xs = np.linspace(-math.pi, math.pi, 241)
    DW2 = 1.6                                                                            # |dw| > 2 kappa: no lock
    assert abs(DW) <= 2 * KAPPA < DW2
    o.append(poly(s, [(ax.X(a), ax.Y(b)) for a, b in zip(xs, adler(xs, DW2))], SER[2], "curve_multi", H.DASH_REF))
    o.append(poly(s, [(ax.X(a), ax.Y(b)) for a, b in zip(xs, adler(xs, DW))], SER[0], "curve"))
    ps_st = math.asin(DW / (2 * KAPPA))
    ps_un = math.pi - ps_st
    # flow arrows on the zero line: dpsi/dt > 0 moves right, < 0 moves left
    o.append(H.arrow(s, p, ax.X(-2.5), ax.Y(0), ax.X(-1.3), ax.Y(0), "dim", w="ref"))          # dpsi/dt > 0 left of the stable point
    o.append(H.arrow(s, p, ax.X(1.6), ax.Y(0), ax.X(0.9), ax.Y(0), "dim", w="ref"))
    o.append(H.arrow(s, p, ax.X(2.88), ax.Y(0), ax.X(3.12), ax.Y(0), "dim", w="ref"))
    o.append(dot(s, ax.X(ps_st), ax.Y(0), SER[3], r=6))
    o.append(dot(s, ax.X(ps_un), ax.Y(0), SER[0], hollow=True, r=6))
    o.append(H.label(s, ax.X(ps_st) - 4, ax.Y(0) + 24, f"stable ψ* = {ps_st:.2f}", "label2", I["primary"], "end"))
    o.append(H.line(s, ax.X(ps_un), ax.Y(0) + 8, ax.X(ps_un) + 8, ax.Y(-1.5) - 12, I["rule"], "leader"))
    o.append(H.label(s, ax.x1 - 4, ax.Y(-1.5), f"unstable, π − ψ* = {ps_un:.2f}", "label2", I["primary"], "end"))
    pk = -math.pi / 2
    o.append(dot(s, ax.X(pk), ax.Y(DW + 2 * KAPPA), SER[0], r=4))
    o.append(H.label(s, ax.X(pk), ax.Y(DW + 2 * KAPPA) - 12, f"Δω + 2κ = {DW + 2 * KAPPA:.1f}", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(math.pi / 2), ax.Y(DW - 2 * KAPPA) + 22, f"Δω − 2κ = {mn(DW - 2 * KAPPA, '{:.1f}')}", "label2", I["primary"], "middle"))
    o += legend(s, ax.x0 + 4, 20, [(SER[0], None, f"Δω = {DW:g}: locks (|Δω| = {DW:g} ≤ 2κ = {2 * KAPPA:g})"),
                                    (SER[2], H.DASH_REF, f"Δω = {DW2:g}: drifts (never zero)")], gap=18)
    aria = ("Plot of the Adler equation, the rate of change of the phase difference psi of two coupled oscillators, "
            f"psi-dot = delta-omega minus 2 kappa sin psi, with kappa = {KAPPA:g}, for psi from minus pi to pi. For delta-omega = "
            f"{DW:g}, solid red, the curve crosses zero twice: a stable fixed point at psi* = {ps_st:.2f} (filled green dot, where "
            f"the curve falls through zero) and an unstable one at pi minus psi* = {ps_un:.2f} (open red dot, where it rises). "
            "Arrows on the zero line show psi moving toward the stable point. For delta-omega = 1.6, dashed orange, which exceeds "
            "2 kappa = 1.4, the curve never reaches zero, so the oscillators do not lock.")
    pts = [[ax.X(a), [ax.Y(b), ax.Y(c)], f"ψ = {mn(a, '{:.2f}')} rad: dψ/dt = {mn(b, '{:.2f}')} (Δω = {DW:g}), {mn(c, '{:.2f}')} (Δω = {DW2:g})"]
           for a, b, c in zip(xs, adler(xs, DW), adler(xs, DW2))]
    hv = H.hover_attr(ax.box, pts)
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #10: the architecture whole (Fig. 9)
def fig10():
    VB = (0, 0, 806, 394)
    s = H.Scale(VB[2], VB[3])
    p = "m12f10_"
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    bw, bh, ym, gap, x0 = 134, 76, 130, 72, 14
    yc = ym + bh / 2
    B = [("optimal feedback", "controller", "§7", O["neural"]),
         ("synergies", "and CPGs", "§8", O["neural"]),
         ("arm plant", "M, C, g", "Module 11", O["force"]),
         ("sensors", "delay and noise", "§6, Module 10", I["rule"])]
    xs = [x0 + k * (bw + gap) for k in range(4)]
    for (n1, n2, tag, col), x in zip(B, xs):
        o.append(box(s, x, ym, bw, bh, col))
        o.append(H.label(s, x + bw / 2 + 2, ym + 31, n1, "label", I["primary"], "middle"))
        o.append(H.label(s, x + bw / 2 + 2, ym + 53, n2, SEC, I["secondary"], "middle"))
        o.append(H.label(s, x + bw / 2, ym - 8, tag, SEC, I["muted"], "middle"))
    for k, nm in enumerate(("synergy commands", "muscle activation")):
        a, b = xs[k] + bw + 4, xs[k + 1] - 4
        o.append(H.arrow(s, p, a, yc, b, yc, "neural" if k == 0 else "neural"))
        o.append(H.label(s, (a + b) / 2, yc - 22, nm.split()[0], SEC, I["secondary"], "middle"))
        o.append(H.label(s, (a + b) / 2, yc - 8, nm.split()[1], SEC, I["secondary"], "middle"))
    a, b = xs[2] + bw + 4, xs[3] - 4
    o.append(H.arrow(s, p, a, yc, b, yc, "force"))
    o.append(H.label(s, (a + b) / 2, yc - 8, "motion", SEC, I["secondary"], "middle"))
    # delayed, noisy feedback along the top
    yt = 58
    xcx, xsx = xs[0] + bw - 24, xs[3] + bw - 24
    o.append(H.line(s, xsx, ym - 3, xsx, yt, O["dim"], "ref"))
    o.append(H.line(s, xsx, yt, xcx, yt, O["dim"], "ref"))
    o.append(H.arrow(s, p, xcx, yt, xcx, ym - 3, "dim", w="ref"))
    o.append(H.label(s, (xcx + xsx) / 2, yt - 9, "delayed, noisy feedback", "label2", I["primary"], "middle"))
    # internal model underneath
    ix, iw, iy, ih = xs[1] - 6, xs[2] + bw - xs[1] + 12, 290, 70
    o.append(box(s, ix, iy, iw, ih, O["geometry"]))
    o.append(H.label(s, ix + iw / 2 + 2, iy + 29, "internal model (§6)", "label", I["primary"], "middle"))
    o.append(H.label(s, ix + iw / 2 + 2, iy + 51, "predicts the state and learns from error", SEC, I["secondary"], "middle"))
    xef = xs[0] + bw / 2
    o.append(H.line(s, xef, ym + bh + 3, xef, iy + ih / 2, O["geometry"], "geom"))
    o.append(H.arrow(s, p, xef, iy + ih / 2, ix - 3, iy + ih / 2, "geometry"))
    o.append(H.label(s, xef + 10, ym + bh + 70, "efference copy", SEC, I["primary"]))
    xp, xe = xs[3] + bw / 2 - 30, xs[3] + bw / 2 + 22
    o.append(H.line(s, ix + iw + 3, iy + 22, xp, iy + 22, O["geometry"], "geom"))
    o.append(H.arrow(s, p, xp, iy + 22, xp, ym + bh + 4, "geometry"))
    o.append(H.label(s, xp - 8, ym + bh + 70, "predicted state", SEC, I["primary"], "end"))
    o.append(H.line(s, xe, ym + bh + 3, xe, iy + ih - 20, O["flag"], "geom"))
    o.append(H.arrow(s, p, xe, iy + ih - 20, ix + iw + 3, iy + ih - 20, "flag"))
    o.append(H.label(s, xe + 8, ym + bh + 70, "prediction", SEC, I["primary"]))
    o.append(H.label(s, xe + 8, ym + bh + 85, "error", SEC, I["primary"]))
    aria = ("Block diagram of the human motor-control architecture as one loop. An optimal feedback controller (Section 7) "
            "commands synergies and central pattern generators (Section 8), which send muscle activations to the arm plant "
            "(Module 11); the plant's motion is sensed by delayed, noisy sensors (Section 6, Module 10), and delayed noisy "
            "feedback returns to the controller. An internal model (Section 6) receives an efference copy from the controller, "
            "sends a predicted state to the sensing stage to beat the delay, and learns from the prediction error that returns from the sensors.")
    return svg(VB, aria, s, o)


# ================================================================ svg #12: scale invariance (Lab A extension)
def fig12():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    p = "m12f12_"
    reaches = [(0.5, 0.6, SER[0]), (0.05, 0.3, SER[1])]
    curves = []
    for D, Tm, col in reaches:
        t, _, v, _ = minjerk(D, Tm)
        curves.append((D, Tm, col, t, v))
    norm = [v * Tm / D for D, Tm, col, t, v in curves]
    diff = float(np.abs(norm[0] - norm[1]).max())
    assert diff < 1e-12 and abs(norm[0].max() - 1.875) < 1e-3
    L = Ax((84, 80, 340, 320), (0, 0.6), (0, 1.9))
    Rt = Ax((466, 80, 722, 320), (0, 1), (0, 2.1))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, L, ticks((0, 0.2, 0.4, 0.6), "{:.1f}"), ticks((0, 0.5, 1.0, 1.5), "{:.1f}"), "time t (s)", "speed v (m/s)",
              ylab_x=L.x0 - 48, xlab_dy=42)
    o += axes(s, Rt, ticks((0, 0.25, 0.5, 0.75, 1), "{:g}"), ticks((0, 1, 2)), "normalised time t/T", "normalised speed v·T/D",
              ylab_x=Rt.x0 - 40, xlab_dy=42)
    for (D, Tm, col, t, v), nv in zip(curves, norm):
        o.append(poly(s, [(L.X(a), L.Y(b)) for a, b in zip(t, v)], col, "curve"))
    o.append(poly(s, [(Rt.X(a / curves[0][1]), Rt.Y(b)) for a, b in zip(curves[0][3], norm[0])], SER[0], "curve"))
    o.append(poly(s, [(Rt.X(a / curves[1][1]), Rt.Y(b)) for a, b in zip(curves[1][3], norm[1])], SER[1], "curve_multi",
                  H.DASH_REF))
    o.append(dot(s, Rt.X(0.5), Rt.Y(1.875), I["primary"], r=4.5))
    o.append(H.label(s, Rt.X(0.5), Rt.Y(1.875) - 12, "peak 1.875 = 15/8 for both", "label2", I["primary"], "middle"))
    for (D, Tm, col, t, v) in curves:
        k = int(v.argmax())
        o.append(dot(s, L.X(t[k]), L.Y(v[k]), col, r=4))
    o.append(H.label(s, L.X(0.3) + 12, L.Y(1.5625) - 6, "peak 1.56 m/s", "label2", I["primary"]))
    o.append(H.label(s, L.X(0.15) + 12, L.Y(0.3125) - 24, "peak 0.31 m/s", "label2", I["primary"]))
    o += legend(s, 84, 28, [(SER[0], None, "0.5 m in 0.6 s"), (SER[1], H.DASH_REF, "0.05 m in 0.3 s")], gap=24)
    o.append(H.label(s, 466, 28, "the dashed curve lies on the solid one", "label2", I["primary"]))
    o.append(H.label(s, 466, 46, f"largest difference {diff:.0e} (rounding error)", "label2", I["secondary"]))
    aria = ("Two panels for two minimum-jerk reaches, 0.5 m in 0.6 s in red and 0.05 m in 0.3 s in blue. Left: speed in "
            "metres per second against time in seconds; the bell curves differ, peaking at 1.56 and 0.31 m/s. Right: the same "
            "speeds multiplied by T over D against t over T; the two curves coincide exactly in one bell peaking at "
            "1.875, which shows scale invariance. The blue curve is dashed so the red curve beneath stays visible.")
    ptsL = hpts([L.X(a) for a in curves[0][3]], [L.Y(b) for b in curves[0][4]],
                [f"t = {a:.3f} s: 0.5 m reach {b:.3f} m/s" for a, b in zip(curves[0][3], curves[0][4])])
    ptsR = hpts([Rt.X(a / curves[0][1]) for a in curves[0][3]], [Rt.Y(b) for b in norm[0]],
                [f"t/T = {a / curves[0][1]:.3f}: v·T/D = {b:.3f} for both reaches" for a, b in zip(curves[0][3], norm[0])])
    hv = H.hover_attr([(L.box, ptsL), (Rt.box, ptsR)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #14: K1 and t_s against R (Lab B)
def fig14():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    p = "m12f14_"
    ax = Ax((90, 28, 722, 304), (-2, 2), (0, 20))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, ax, ticks((-2, -1, 0, 1, 2)), ticks((0, 5, 10, 15, 20)), "log₁₀ R (effort weight R)", "K₁ or tₛ (s)",
              ylab_x=ax.x0 - 46, xlab_dy=44)
    lg = np.linspace(-2, 2, 81)
    Rv = 10.0 ** lg
    k1, ts = Rv ** -0.5, 4 * math.sqrt(2) * Rv ** 0.25
    o.append(poly(s, [(ax.X(a), ax.Y(b)) for a, b in zip(lg, k1)], SER[0], "curve"))
    o.append(poly(s, [(ax.X(a), ax.Y(b)) for a, b in zip(lg, ts)], SER[1], "curve"))
    for e in (-2, 2):
        o.append(dot(s, ax.X(e), ax.Y((10.0 ** e) ** -0.5), SER[0], r=4.5))
        o.append(dot(s, ax.X(e), ax.Y(settle(10.0 ** e)), SER[1], r=4.5))
    sw = s(H.PX["curve_multi"])
    for k, (col, txt) in enumerate(((SER[0], f"position gain K₁ = R{sup('−1/2', s)}: 10 at R = 0.01, 0.1 at R = 100"),
                                    (SER[1], f"settling time tₛ = 4√2 R{sup('1/4', s)}: {settle(0.01):.2f} s at R = 0.01, "
                                             f"{settle(100):.1f} s at R = 100"))):
        y = 58 + 22 * k
        o.append(f'<line x1="{ax.x0 + 24}" y1="{y - 4}" x2="{ax.x0 + 48}" y2="{y - 4}" stroke="{col}" stroke-width="{sw:.2f}"/>')
        o.append(H.label(s, ax.x0 + 56, y, txt, "label2", I["primary"]))
    aria = ("Position gain K1 and 2 percent settling time t-s against log base 10 of the effort weight R from minus 2 to 2, on one "
            "vertical axis from 0 to 20. The red gain K1 = R to the minus one half falls from 10 to 0.1; the blue settling time "
            "t-s = 4 root 2 R to the one quarter climbs from 1.79 s to 17.9 s. The two curves cross near R = 0.1.")
    pts = [[ax.X(a), [ax.Y(b), ax.Y(c)], f"log₁₀ R = {mn(a, '{:.2f}')}: K₁ = {b:.3g}, tₛ = {c:.3g} s"] for a, b, c in zip(lg, k1, ts)]
    hv = H.hover_attr(ax.box, pts)
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #16: contact force (Lab C)
M_C, DT_C, XW, X_DES, KW = 1.0, 0.001, 0.10, 0.15, 1e5


def contact_run(kc, dc, n=4000):
    """Lab C loop, verbatim, but the whole force trace is kept."""
    x, v, fmax = 0.0, 0.0, 0.0
    F, C = [], []
    for _ in range(n):
        f = kc * (X_DES - x) - dc * v
        fwall = -KW * (x - XW) if x > XW else 0.0
        v += DT_C * (f + fwall) / M_C
        x += DT_C * v
        inc = x >= XW - 1e-4
        if inc:
            fmax = max(fmax, f)
        F.append(f)
        C.append(inc)
    return np.array(F), np.array(C), fmax


def steady(kc):
    xx = (kc * X_DES + KW * XW) / (kc + KW)
    return kc * (X_DES - xx)


_CASES = [("impedance", 200.0, 30.0, SER[1]), ("servo", 5000.0, 150.0, SER[0])]
_RUN = {nm: contact_run(kc, dc) for nm, kc, dc, _ in _CASES}
assert round(_RUN["servo"][2]) == 388 and round(_RUN["impedance"][2]) == 21                       # caption, line 373
assert abs(steady(5000.0) - 238.1) < 0.05 and abs(steady(200.0) - 9.98) < 0.005                    # settled 238 N and 10 N
assert abs(steady(5000.0) / steady(200.0) - 23.9) < 0.05 and abs(_RUN["servo"][2] / _RUN["impedance"][2] - 18.6) < 0.05


def fig16():
    VB = (0, 0, 760, 410)
    s = H.Scale(VB[2], VB[3])
    p = "m12f16_"
    n = 1200
    t = np.arange(n) * DT_C
    A = Ax((84, 56, 420, 330), (0, 1.2), (-100, 400))
    Z = Ax((516, 56, 722, 330), (0.15, 0.45), (-5, 25))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, A, ticks((0, 0.4, 0.8, 1.2), "{:.1f}"), ticks((-100, 0, 100, 200, 300, 400)), "time t (s)", "controller force (N)",
              ylab_x=A.x0 - 56, xlab_dy=44)
    o += axes(s, Z, ticks((0.15, 0.25, 0.35, 0.45), "{:.2f}"), ticks((-5, 0, 5, 10, 15, 20, 25)), "time t (s)", "controller force (N)",
              ylab_x=Z.x0 - 46, xlab_dy=44)
    o.append(H.line(s, A.x0, A.Y(0), A.x1, A.Y(0), I["axis"], "ref"))
    o.append(H.line(s, Z.x0, Z.Y(0), Z.x1, Z.Y(0), I["axis"], "ref"))
    traces = {}
    for nm, kc, dc, col in _CASES:
        F, C, fmax = _RUN[nm]
        k0 = int(np.argmax(C))                                                                      # first contact
        traces[nm] = (F[:n], k0, fmax, col)
        o.append(poly(s, [(A.X(t[k]), A.Y(F[k])) for k in range(k0, n)], col, "curve"))
        o.append(dot(s, A.X(t[k0]), A.Y(F[k0]), col, hollow=True, r=4))
        ss = steady(kc)
        o.append(H.line(s, A.X(0.62), A.Y(ss), A.x1, A.Y(ss), col, "ref", H.DASH_REF))
        if nm == "impedance":
            o.append(poly(s, [(Z.X(t[k]), Z.Y(F[k])) for k in range(k0, 451)], col, "curve"))
            o.append(dot(s, Z.X(t[k0]), Z.Y(F[k0]), col, hollow=True, r=4))
            o.append(H.line(s, Z.x0, Z.Y(ss), Z.x1, Z.Y(ss), col, "ref", H.DASH_REF))
    Fs, k0s, fms, cs = traces["servo"]
    Fi, k0i, fmi, ci = traces["impedance"]
    kpk = int(np.argmax(np.where(_RUN["servo"][1][:n], Fs, -1e9)))
    o.append(dot(s, A.X(t[kpk]), A.Y(Fs[kpk]), cs, r=4.5))
    o.append(H.label(s, A.X(t[kpk]) + 12, A.Y(Fs[kpk]) + 5, f"servo peak {fms:.0f} N", "label2", I["primary"]))
    kmn = int(np.argmin(np.where(_RUN["servo"][1][:n], Fs, 1e9)))
    o.append(H.label(s, A.X(t[kmn]) + 14, A.Y(Fs[kmn]) + 3, f"reverses to {mn(Fs[kmn], '{:.0f}')} N", "label2", I["primary"]))
    o.append(H.label(s, A.X(0.64), A.Y(steady(5000.0)) - 8, f"servo settles at {steady(5000.0):.0f} N", "label2", I["primary"]))
    o.append(H.label(s, A.X(0.64), A.Y(steady(200.0)) - 26, f"impedance settles at {steady(200.0):.0f} N", "label2", I["primary"]))
    o.append(H.label(s, A.X(0.64), A.Y(steady(200.0)) - 10, f"(peak {fmi:.0f} N, see zoom)", "label2", I["secondary"]))
    kz = int(np.argmax(np.where(_RUN["impedance"][1][:n], Fi, -1e9)))
    o.append(dot(s, Z.X(t[kz]), Z.Y(Fi[kz]), ci, r=4.5))
    o.append(H.label(s, Z.X(t[kz]) + 10, Z.Y(Fi[kz]) + 3, f"peak {fmi:.0f} N", "label2", I["primary"]))
    o.append(H.label(s, Z.x1 - 6, Z.Y(5.0), f"settles at {steady(200.0):.2f} N", "label2", I["primary"], "end"))
    o.append(H.label(s, Z.x1 - 6, Z.Y(5.0) + 16, "(dashed line)", "label2", I["secondary"], "end"))
    o.append(H.label(s, (A.x0 + A.x1) / 2, 24, "both controllers, one scale", "label", I["primary"], "middle"))
    o.append(H.label(s, (Z.x0 + Z.x1) / 2, 24, "impedance only, zoomed", "label", I["primary"], "middle"))
    o += legend(s, 84, 44, [(SER[0], None, "position servo"), (SER[1], None, "impedance controller")], gap=18)
    o.append(H.label(s, 84, 396, "each curve starts at its first contact with the wall (open dot); dashed lines are the settled forces", "label2",
                     I["secondary"]))
    aria = ("Two panels of the controller force against time as a point mass is commanded 5 cm behind a stiff wall. Left: both "
            "controllers on one scale from minus 100 to 400 newtons over 1.2 seconds. The stiff position servo (red) starts at its "
            "first contact at 33 ms, peaks at 388 N, reverses to about minus 87 N and settles at 238 N. The impedance controller "
            "(blue) starts at 168 ms, peaks at 21 N and settles at 10 N, which is almost flat on this scale. Right: the impedance "
            "force alone, zoomed, from 0.15 to 0.45 s on a scale from minus 5 to 25 N, showing the 21 N peak, the small rings "
            "as the mass touches and leaves the wall, and the 9.98 N settled force.")
    ptsA = hpts([A.X(t[k]) for k in range(n)], [[A.Y(Fs[k]), A.Y(Fi[k])] for k in range(n)],
                [f"t = {t[k]:.3f} s: servo {mn(Fs[k], '{:.0f}')} N, impedance {mn(Fi[k], '{:.1f}')} N" for k in range(n)])
    ptsZ = hpts([Z.X(t[k]) for k in range(k0i, 451)], [Z.Y(Fi[k]) for k in range(k0i, 451)],
                [f"t = {t[k]:.3f} s: impedance {mn(Fi[k], '{:.2f}')} N" for k in range(k0i, 451)])
    hv = H.hover_attr([(A.box, ptsA), (Z.box, ptsZ)])
    return svg(VB, aria, s, o, hv)


FIGS = {
    3: ("Three nested levels of redundancy: a few task variables driv", fig3),
    4: ("Minimum-jerk reach: position an S-curve, velocity a symmetri", fig4),
    5: ("Closed-loop recovery of a point-mass hand from a unit positi", fig5),
    7: ("Block diagram of a forward-model control loop: controller, p", fig7),
    8: ("The uncontrolled-manifold signature: a cloud of two-effector", fig8),
    9: ("Phase-difference dynamics of two coupled oscillators: the cu", fig9),
    10: ("The human motor-control architecture as one loop: optimal fe", fig10),
    12: ("Two minimum-jerk reaches of different size and duration, the", fig12),
    14: ("Position gain and settling time versus the effort weight R o", fig14),
    16: ("Contact force over time as a point mass reaches a target beh", fig16),
    18: ("Simulated scatter of 500 two-effector outcomes, forming an e", fig18),
}
