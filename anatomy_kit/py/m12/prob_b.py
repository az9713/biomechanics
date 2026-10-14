"""Module 12 problem figures, group `prob_b` (400 px): D8, D9, D10, K1, K2, K4, K5, K6, K8, K9, K10 (svg #36-#57).

Every plotted number is computed here from what module12.html states: Prop. 7.2 and Lab D (D8), the Adler equation
(D9, K8), M = W C (D10, K9), the K1 profiles (Prop. 3.1 and Euler-Poisson p = 2), the Lab B closed form (K2), the K4
recursion, and the K5, K6, K8, K9, K10 scripts ported line for line. The numbers the solutions quote are asserted.
"""
import math
from functools import lru_cache

import numpy as np

import house as H
from m05.plots_prob import Plot, hov, label, legend, svg
from m05.tissue import muscle_grad, tissue

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
W = 400
BOX, GRID = "#f7f4ef", "#e6e6e6"
L2 = "label2"


# ---------------------------------------------------------------- local helpers
def sub(t, s):
    return H.sub(t, s, L2)


def sup(t, s):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[L2] * 0.7):.2f}">{t}</tspan>'


def dot_over(sym, rest=" "):
    """Dot accent over a symbol with spacing modifiers (Georgia has no combining marks in SVG text)."""
    return f'{sym}<tspan dx="-0.5em" dy="-0.45em">˙</tspan><tspan dy="0.45em">{rest}</tspan>'


def tk(vals, f="{:g}"):
    return [(v, f.format(v).replace("-", "−")) for v in vals]


def dot(P, x, y, col):
    return (f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{P.s(H.PX["dot"]):.2f}" fill="{col}" stroke="#fff" '
            f'stroke-width="{P.s(1.5):.2f}"/>')


def hdot(P, x, y, col):
    return (f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{P.s(H.PX["dot"]):.2f}" fill="#fff" stroke="{col}" '
            f'stroke-width="{P.s(2):.2f}"/>')


def href(s, P, y, col=None, x0=None, x1=None):
    return H.line(s, P.x0 if x0 is None else P.X(x0), P.Y(y), P.x1 if x1 is None else P.X(x1), P.Y(y),
                  col or I["secondary"], "ref", H.DASH_REF)


def vref(s, P, x, col=None, ytop=None, ybot=None):
    return H.line(s, P.X(x), P.y1 if ytop is None else P.Y(ytop), P.X(x), P.y0 if ybot is None else P.Y(ybot),
                  col or I["secondary"], "ref", H.DASH_REF)


def region(pts, fill, op):
    return (f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" fill-opacity="{op}" '
            f'stroke="none"/>')


def rrect(x0, y0, x1, y1, fill, op):
    return (f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" fill="{fill}" '
            f'fill-opacity="{op}" stroke="none"/>')


# ================================================================ #36 D8: the UCM variance ratio (Prop. 7.2, Lab D)
def fig36():
    VB = (0, 0, W, 344)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m12f36_"
    from m12.plots_main import RHO, SIG, VAR_N, VAR_T                      # Lab D (module12.html line 384 on)
    a, b = math.sqrt(2) * SIG, math.sqrt(2 * RHO) * SIG                    # std of n and of t (variances 2s^2, 2 rho s^2)
    assert abs(a * a / (b * b) - 1 / RHO) < 1e-9 and round(1 / RHO, 2) == 6.67
    assert abs(VAR_N / VAR_T - 1 / RHO) < 0.05                              # the simulated ratio, line 395: 6.65
    cx, cy, U = 200, 150, 80.0
    X = lambda v: cx + U * v          # noqa: E731
    Y = lambda v: cy - U * v          # noqa: E731
    th = np.linspace(0, 2 * math.pi, 181)
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o.append(H.arrow(s, p, cx - 134, cy, cx + 138, cy, "dim"))
    o.append(H.arrow(s, p, cx, cy + 128, cx, cy - 132, "dim"))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{U * a:.1f}" fill="none" stroke="{I["secondary"]}" '
             f'stroke-width="{s(H.PX["ref"]):.2f}" stroke-dasharray="{s(6):.1f} {s(4):.1f}"/>')
    ell = " ".join(f"{X(a * math.cos(t)):.2f},{Y(b * math.sin(t)):.2f}" for t in th)
    o.append(f'<polygon points="{ell}" fill="{SER[1]}" fill-opacity="0.16" stroke="{SER[1]}" '
             f'stroke-width="{s(H.PX["curve_multi"]):.2f}" stroke-linejoin="round"/>')
    o.append(label(s, cx + 142, cy + 5, "n", "label", I["primary"]))
    o.append(label(s, cx + 8, cy - 134, "t", "label", I["primary"]))
    o.append(label(s, X(a) + 6, cy - 8, f"√2 σ = {a:.2f}", L2, I["secondary"]))
    o.append(label(s, cx + 8, Y(b) - 6, f"√(2ρ) σ = {b:.2f}", L2, I["secondary"]))
    o.append(label(s, 16, 288, "dashed: no feedback, Var(n) = Var(t) = 2σ² = 2.00", L2, I["secondary"]))
    o.append(label(s, 16, 306, "blue: task-correcting loop, Var(t) = 2ρσ² = 0.30", L2, I["secondary"]))
    o.append(label(s, 16, 324, f"σ = {SIG:g}, ρ = {RHO:g}.  n = y₁ − y₂ (null), t = y₁ + y₂ (task)", L2, I["secondary"]))
    o.append(label(s, 16, 342 - 2, f"Var(n) / Var(t) = 1/ρ = {1 / RHO:.2f} > 1", "label", I["primary"]))
    aria = ("Problem D8: the variance ratio of the uncontrolled-manifold signature in the plane of the null variable n "
            "equals y1 minus y2 and the task variable t equals y1 plus y2. A dashed circle of radius root 2 sigma is the "
            "open-loop scatter, variance 2 sigma squared in both directions. A blue ellipse is the scatter under a "
            f"task-correcting controller: unchanged along n and squeezed along t to variance 2 rho sigma squared. With "
            f"sigma 1 and rho {RHO:g} the ratio of null to task variance is one over rho, {1 / RHO:.2f}, larger than 1.")
    ns = np.linspace(-a, a, 121)
    ts = b * np.sqrt(np.clip(1 - (ns / a) ** 2, 0, None))
    pts = [[X(n), [Y(t), Y(-t)], f"n = {n:+.2f}: closed-loop 1σ range of t is ±{t:.2f} (open loop ±{math.sqrt(max(a * a - n * n, 0)):.2f})"]
           for n, t in zip(ns, ts)]
    return svg(VB, aria, s, "".join(o), ([X(-a), Y(b), X(a), Y(-b)], pts))


# ================================================================ #37 D9: oscillator locking (Adler equation)
KAP9, DW9, DW9_DRIFT = 1.0, 1.0, 2.4


def fig37():
    VB = (0, 0, W, 308)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m12f37_"
    k, dw = KAP9, DW9
    psi_s = math.asin(dw / (2 * k))
    psi_u = math.pi - psi_s
    assert round(math.degrees(psi_s), 1) == 30.0 and abs(dw) <= 2 * k < DW9_DRIFT
    P = Plot(s, (62, 84, 388, 236), (-math.pi, math.pi), (-1.5, 4.6))
    ps = np.linspace(-math.pi, math.pi, 201)
    f1 = dw - 2 * k * np.sin(ps)
    f2 = DW9_DRIFT - 2 * k * np.sin(ps)
    xt = [(-math.pi, "−π"), (-math.pi / 2, "−π/2"), (0, "0"), (math.pi / 2, "π/2"), (math.pi, "π")]
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o.append(P.axes(xt, tk((-1, 0, 1, 2, 3, 4)), "phase difference ψ (rad)", "dψ/dt (rad/s)", grid=(2, 4), ytx=13))
    o.append(href(s, P, 0.0, I["rule"]))
    o.append(P.curve(ps, f2, SER[1], dash=H.DASH_REF))
    o.append(P.curve(ps, f1, SER[0]))
    # flow on the psi axis: right where psi-dot > 0, left where it is < 0
    o.append(H.arrow(s, p, P.X(-2.4), P.Y(0), P.X(-1.1), P.Y(0), "dim"))
    o.append(H.arrow(s, p, P.X(2.2), P.Y(0), P.X(1.1), P.Y(0), "dim"))
    o.append(dot(P, psi_s, 0.0, I["primary"]))
    o.append(hdot(P, psi_u, 0.0, I["primary"]))
    o.append(legend(s, 62, 18, [(SER[0], f"Δω = {dw:g} ≤ 2κ = {2 * k:g}: two zeros, locks", None)]))
    o.append(legend(s, 62, 36, [(SER[1], f"Δω = {DW9_DRIFT:g} > 2κ: no zero, ψ drifts", H.DASH_REF)]))
    o.append(label(s, 62, 54, f"κ = {k:g}. Filled dot: stable, {math.degrees(psi_s):.0f}°.", L2, I["secondary"]))
    o.append(label(s, 62, 70, f"Open dot: unstable, {math.degrees(psi_u):.0f}°.", L2, I["secondary"]))
    aria = ("Problem D9: the Adler equation psi-dot equals delta omega minus 2 kappa sine psi, plotted against the phase "
            f"difference psi from minus pi to pi for kappa {k:g}. The red curve, delta omega {dw:g}, crosses zero twice: "
            f"a stable locked state at {math.degrees(psi_s):.0f} degrees where the slope is negative, and an unstable one at "
            f"{math.degrees(psi_u):.0f} degrees. Arrows on the axis show psi moving toward the stable root. The dashed "
            f"blue curve, delta omega {DW9_DRIFT:g}, larger than 2 kappa, never reaches zero, so the phase difference drifts.")
    hv = hov(P, ps, [f1, f2], lambda i: f"ψ = {ps[i]:+.2f} rad: dψ/dt = {f1[i]:+.2f} (Δω = {dw:g}), {f2[i]:+.2f} (Δω = {DW9_DRIFT:g})")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #38 D10: M = W C, rank <= k (muscle tissue)
def fig38():
    VB = (0, 0, W, 296)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m12f38_"
    nm, ns, k = 6, 8, 2
    Wm = np.array([[0.95, 0.10], [0.75, 0.20], [0.45, 0.55], [0.25, 0.80], [0.10, 0.95], [0.60, 0.50]])
    C = np.random.default_rng(3).random((k, ns))
    M = Wm @ C
    assert np.linalg.matrix_rank(M) == k and np.linalg.matrix_rank(Wm) == k and M.shape == (nm, ns)
    cs = 16.0
    x_m, x_w, x_c = 36.0, 36.0 + ns * cs + 30, 36.0 + ns * cs + 30 + k * cs + 22
    y_m = 92.0
    y_c = y_m + (nm - k) * cs / 2
    j = 4                                                                         # highlighted sample column

    def grid(x0, y0, A, col, edge):
        r, c = A.shape
        q = [f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{c * cs:.1f}" height="{r * cs:.1f}" fill="#fff"/>']
        vmax = A.max()
        for a in range(r):
            for b in range(c):
                q.append(f'<rect x="{x0 + b * cs:.1f}" y="{y0 + a * cs:.1f}" width="{cs:.1f}" height="{cs:.1f}" fill="{col}" '
                         f'fill-opacity="{0.12 + 0.88 * A[a, b] / vmax:.3f}" stroke="#fff" stroke-width="{s(0.8):.2f}"/>')
        q.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{c * cs:.1f}" height="{r * cs:.1f}" fill="none" stroke="{edge}" '
                 f'stroke-width="{s(1.4):.2f}"/>')
        return "".join(q)

    o = [f'<defs>{muscle_grad(p + "mg", 0, 0, 30, 0)}</defs>']
    o.append(grid(x_m, y_m, M, T["muscle"][0], T["muscle"][1]))
    o.append(grid(x_w, y_m, Wm, T["muscle"][0], T["muscle"][1]))
    o.append(grid(x_c, y_c, C, O["neural"], O["neural"]))
    o.append(label(s, x_w - 15, y_m + nm * cs / 2 + 5, "=", "label", I["primary"], "middle"))
    o.append(label(s, x_c - 11, y_m + nm * cs / 2 + 5, "×", "label", I["primary"], "middle"))
    # the j-th column: m(t_j) = W c(t_j)
    for x0, y0, rows in ((x_m, y_m, nm), (x_c, y_c, k)):
        o.append(f'<rect x="{x0 + j * cs:.1f}" y="{y0 - 2:.1f}" width="{cs:.1f}" height="{rows * cs + 4:.1f}" fill="none" '
                 f'stroke="{O["geometry"]}" stroke-width="{s(2):.2f}"/>')
    o.append(label(s, x_m + ns * cs / 2, y_m - 24, "M", "label", I["primary"], "middle"))
    o.append(label(s, x_m + ns * cs / 2, y_m - 8, f"{nm} muscles × {ns} samples", L2, I["secondary"], "middle"))
    o.append(label(s, x_w + k * cs / 2, y_m - 24, "W", "label", I["primary"], "middle"))
    o.append(label(s, x_w + k * cs / 2, y_m - 8, f"{nm} × k, k = {k}", L2, I["secondary"], "middle"))
    o.append(label(s, x_c + ns * cs / 2, y_c - 24 - 20, "C", "label", I["primary"], "middle"))
    o.append(label(s, x_c + ns * cs / 2, y_c - 8 - 20, f"k × {ns}", L2, I["secondary"], "middle"))
    # bracket-free statement under the equation
    yb = y_m + nm * cs + 28
    o.append(label(s, 16, yb, "outlined column j:  m(tⱼ) = W c(tⱼ)", L2, I["secondary"]))
    o.append(label(s, 16, yb + 18, "every column of M is a mix of the k columns of W,", L2, I["secondary"]))
    o.append(label(s, 16, yb + 36, "so rank M ≤ k and k numbers per sample fix M", "label", I["primary"]))
    # legend with a muscle belly glyph (tissue idiom)
    ly = 24
    belly = [(18, ly - 7), (26, ly - 10), (40, ly - 10), (48, ly - 7), (40, ly - 3), (26, ly - 3)]
    o.append(tissue(s, belly, f"url(#{p}mg)", T["muscle"][1], 1.0))
    o.append(label(s, 56, ly - 1, "muscle activation, darker = more active", L2, I["secondary"]))
    o.append(rrect(18, ly + 8, 32, ly + 18, O["neural"], 0.75))
    o.append(label(s, 56, ly + 17, "synergy coefficient (neural drive to a synergy)", L2, I["secondary"]))
    aria = (f"Problem D10: the factorization M equals W times C drawn as three grids. M, {nm} muscles by {ns} samples, "
            f"and W, {nm} muscles by k synergies with k = {k}, are tinted in muscle red, darker meaning a more active "
            f"muscle; C, k by {ns} recruitment coefficients, is tinted green for neural drive. One sample column of M is "
            f"outlined in blue together with the same column of C: it equals W times that column, so every column of M lies "
            f"in the span of the {k} columns of W and the rank of M is at most {k}.")
    return svg(VB, aria, s, "".join(o))


# ================================================================ #39 K1: which smoothness cost?
def fig39():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    tau = np.linspace(0, 1, 201)
    vj = 30 * tau ** 2 * (1 - tau) ** 2
    va = 6 * tau * (1 - tau)
    t2 = np.linspace(0, 1, 200001)                                              # the K1 script, verbatim
    pj, pa_ = (30 * t2 ** 2 * (1 - t2) ** 2).max(), (6 * t2 * (1 - t2)).max()
    assert (round(pj, 4), round(pa_, 4), round(100 * (pj / pa_ - 1), 1)) == (1.875, 1.5, 25.0)
    P = Plot(s, (62, 56, 388, 214), (0, 1), (0, 2.1))
    o = [P.axes(tk((0, 0.25, 0.5, 0.75, 1.0), "{:.2f}"), tk((0, 1, 2)), "normalised time τ = t/T", "speed v·T/D",
                grid=(1, 2))]
    o.append(rrect(P.x0, P.Y(1.9), P.x1, P.Y(1.7), I["rule"], 0.22))
    o.append(P.curve(tau, va, SER[1], dash=H.DASH_REF))
    o.append(P.curve(tau, vj, SER[0]))
    o.append(dot(P, 0.5, pj, SER[0]))
    o.append(dot(P, 0.5, pa_, SER[1]))
    o.append(label(s, P.X(0.02), P.Y(1.8) + 4.5, "measured 1.7–1.9", L2, I["secondary"]))
    o.append(label(s, P.X(0.5), P.Y(pa_) + 19, f"{pa_:.3f}", L2))
    o.append(label(s, P.X(0.5) + 10, P.Y(pj) - 12, f"{pj:.3f}", L2))
    o.append(legend(s, 62, 16, [(SER[0], "minimum jerk (fifth-order)", None)]))
    o.append(legend(s, 62, 34, [(SER[1], "minimum acceleration (cubic)", H.DASH_REF)]))
    o.append(label(s, 62, P.y0 + 62, f"peak/mean {pj:.3f} against {pa_:.3f}: jerk is {100 * (pj / pa_ - 1):.1f}% more peaked",
                   L2, I["secondary"]))
    aria = ("Problem K1: speed profiles of the same reach, speed times T over D against normalised time. The minimum-jerk "
            f"profile, a red solid bell, peaks at {pj:.3f}; the minimum-acceleration profile, a blue dashed parabola, peaks at "
            f"{pa_:.3f}, so the jerk profile is {100 * (pj / pa_ - 1):.1f} percent more sharply peaked. A grey band marks the "
            "measured peak-to-mean range 1.7 to 1.9, which contains the minimum-jerk peak and not the minimum-acceleration one.")
    hv = hov(P, tau, [vj, va], lambda i: f"τ = {tau[i]:.2f}: min jerk {vj[i]:.3f}, min acceleration {va[i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #41 K2: tuning the LQR
def ts_R(R):
    return 4 * math.sqrt(2) * R ** 0.25                                         # t_s = 8/K2 = 4 sqrt2 R^(1/4)


def fig41():
    VB = (0, 0, W, 280)
    s = H.Scale(W, VB[3], display_w=400)
    A = np.array([[0.0, 1.0], [0.0, 0.0]])
    Bm = np.array([[0.0], [1.0]])
    for R in (0.01, 0.1, 1.0, 10.0):                                            # the K2 closed form against the poles
        K = np.array([[R ** -0.5, math.sqrt(2) * R ** -0.25]])
        lam = np.linalg.eigvals(A - Bm @ K)
        assert abs(4 / abs(lam.real[0]) - ts_R(R)) < 1e-9
        try:
            from scipy.linalg import solve_continuous_are
            Pm = solve_continuous_are(A, Bm, np.diag([1.0, 0.0]), np.array([[R]]))
            assert np.allclose(Bm.T @ Pm / R, K, atol=1e-6)
        except ImportError:
            pass
    sw = {R: ts_R(R) for R in (0.01, 0.1, 1.0, 10.0)}
    assert [round(v, 2) for v in sw.values()] == [1.79, 3.18, 5.66, 10.06]       # text
    k2 = 8 / 1.8
    R_t = (2 / k2 ** 2) ** 2
    assert round(k2, 3) == 4.444 and round(R_t, 5) == 0.01025 and abs(ts_R(R_t) - 1.8) < 1e-9
    P = Plot(s, (62, 44, 388, 204), (-2.2, 1.2), (0, 11))
    o = [P.axes([(-2, "0.01"), (-1, "0.1"), (0, "1"), (1, "10")], tk((0, 5, 10)), "effort weight R (log scale)",
                "settling time t" + sub("s", s) + " (s)", grid=(5, 10), ytx=13)]
    lr = np.linspace(-2.2, 1.2, 171)
    ts = 4 * math.sqrt(2) * 10 ** (lr / 4)
    o.append(vref(s, P, math.log10(R_t), O["flag"], ybot=0, ytop=1.8))
    o.append(P.curve(lr, ts, SER[0]))
    for R, v in sw.items():
        o.append(dot(P, math.log10(R), v, SER[0]))
    o.append(dot(P, math.log10(R_t), 1.8, O["flag"]))
    for R in (0.1, 1.0):
        o.append(label(s, P.X(math.log10(R)) + 8, P.Y(sw[R]) + 20, f"{sw[R]:.2f} s", L2, I["primary"]))
    o.append(label(s, P.X(1.0) - 8, P.Y(sw[10.0]) - 8, f"{sw[10.0]:.2f} s", L2, I["primary"], "end"))
    o.append(label(s, P.X(math.log10(R_t)) + 9, P.y0 - 7, f"R = {R_t:.5f}", L2))
    o.append(label(s, 62, 18, "t" + sub("s", s) + " = 8/K" + sub("2", s) + " = 4√2 R" + sup("1/4", s) + "  (2% settling)", L2,
                   I["secondary"]))
    o.append(label(s, 62, 34, "orange: target 1.8 s, K" + sub("2", s) + f" = 8/1.8 = {k2:.3f}", L2, I["secondary"]))
    o.append(label(s, P.X(-2.12), P.Y(8.6), "dots: R = 0.01, 0.1, 1, 10", L2, I["secondary"]))
    o.append(label(s, P.X(-2.12), P.Y(8.6) + 16, "give 1.79, 3.18, 5.66, 10.06 s", L2, I["secondary"]))
    aria = ("Problem K2: the 2 percent settling time of the LQR point-mass reach against the effort weight R on a log axis "
            "from 0.01 to 10. The red curve is t sub s equals 4 root 2 times R to the one quarter; dots at R equals 0.01, 0.1, 1 "
            "and 10 give 1.79, 3.18, 5.66 and 10.06 seconds. An orange dashed line marks the target 1.8 seconds, whose "
            f"inverse is K2 equal to {k2:.3f} and R equal to {R_t:.5f}, a low effort price.")
    hv = hov(P, lr, [ts], lambda i: f"R = {10 ** lr[i]:.3g}: settling {ts[i]:.2f} s")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #45 K4: force-field adaptation
def fig45():
    VB = (0, 0, W, 512)
    s = H.Scale(W, VB[3], display_w=400)
    g, pert = 1.0, 1.0
    etas = (0.2, 0.5, 1.0, 2.5)
    out = {}
    for eta in etas:                                                            # the K4 script, verbatim
        u, hist = 0.0, []
        for n in range(25):
            e = g * (pert - u)
            hist.append(e)
            u = u + eta * e
        out[eta] = (hist, g * (pert - u), u)
    assert round(out[0.2][0][10], 3) == 0.107 and abs(out[0.5][0][10] - 9.77e-4) < 1e-6 and round(out[2.5][0][10], 1) == 57.7
    assert round(out[2.5][1] / 1e4, 1) == -2.5 and [round(-out[e][2] * g, 3) for e in etas[:3]] == [-0.996, -1.0, -1.0]
    A = Plot(s, (62, 44, 388, 190), (0, 12), (-0.1, 1.1))
    B = Plot(s, (62, 314, 388, 432), (0, 3), (0, 1.7))
    ns = np.arange(0, 13)
    cols = {0.2: SER[0], 0.5: SER[1], 1.0: SER[2]}
    o = [A.axes(tk((0, 2, 4, 6, 8, 10, 12)), tk((0, 0.5, 1)), "trial n", "error eₙ", grid=(0.5, 1))]
    o.append(B.axes(tk((0, 0.5, 1, 1.5, 2, 2.5, 3), "{:g}"), tk((0, 0.5, 1, 1.5), "{:g}"), "learning rate η  (g = 1)",
                    "rate |1 − η g|", grid=(0.5, 1.5)))
    for eta in (0.2, 0.5, 1.0):
        o.append(A.curve(ns, (1 - eta * g) ** ns, cols[eta]))
        o.append(A.dot(10, (1 - eta * g) ** 10, cols[eta]) if eta < 1 else "")
    for row, eta in enumerate((0.2, 0.5, 1.0)):
        o.append(legend(s, A.X(5.2), A.Y(1.02) + 4 + row * 18, [(cols[eta], f"η = {eta:g}", None)]))
    o.append(label(s, A.X(10) + 8, A.Y((0.8) ** 10) - 6, f"{out[0.2][0][10]:.3f}", L2))
    o.append(label(s, 62, 18, "eₙ = g (p − uₙ), uₙ₊₁ = uₙ + η eₙ", L2, I["secondary"]))
    o.append(label(s, 62, 34, "g = 1, p = 1: error shrinks by |1 − η g| per trial", L2, I["secondary"]))
    # panel B: the stability sweep
    es = np.linspace(0, 3, 121)
    o.append(rrect(B.X(0), B.Y(1), B.X(2), B.Y(0), O["neural"], 0.10))
    o.append(href(s, B, 1.0))
    o.append(vref(s, B, 2.0, O["flag"]))
    o.append(B.curve(es, np.abs(1 - es * g), I["primary"]))
    for eta in (0.2, 0.5, 1.0):
        o.append(dot(B, eta, abs(1 - eta * g), cols[eta]))
    o.append(dot(B, 2.5, abs(1 - 2.5 * g), I["primary"]))
    o.append(label(s, B.X(2.0) + 6, B.Y(0) - 6, "η g = 2: boundary", L2))
    o.append(label(s, B.X(0.04), B.Y(1.0) - 6, "rate 1", L2, I["secondary"]))
    o.append(label(s, 62, 268, "dot colours as above; green tint: converges", L2, I["secondary"]))
    o.append(label(s, 62, 284, f"black dot η = 2.5: rate 1.50, e₁₀ = {out[2.5][0][10]:.1f}", L2, I["secondary"]))
    o.append(label(s, 62, 300, f"e₂₅ = −2.5×10⁴; η g = 1 is deadbeat, rate 0", L2, I["secondary"]))
    o.append(label(s, 62, B.y0 + 58, "aftereffect −uₙg after 25 trials:", L2, I["secondary"]))
    o.append(label(s, 62, B.y0 + 74, f"{-out[0.2][2]*g:+.3f} (η 0.2), {-out[0.5][2]*g:+.3f} (η 0.5, 1.0)".replace("-", "−"),
                   L2, I["secondary"]))
    aria = ("Problem K4: error-driven adaptation u next equals u plus eta times e, with error e equals g times p minus u, g = 1, "
            "p = 1. Top: the error against trial for eta 0.2 (red, rate 0.80, error 0.107 at trial 10), eta 0.5 (blue, rate "
            "0.50, 0.000977 at trial 10) and eta 1.0 (orange, deadbeat, zero after one trial). Bottom: the per-trial rate "
            "absolute value of 1 minus eta g against eta; the green region below 1, eta g between 0 and 2, converges, and the "
            "orange dashed line at eta g equal to 2 is the stability boundary. At eta 2.5 the rate is 1.50 and the error "
            "grows to 57.7 at trial 10 and minus 2.5 times 10 to the 4 at trial 25. The aftereffect after 25 trials is minus 0.996, "
            "minus 1.000 and minus 1.000.")
    ha = hov(A, ns, [(1 - 0.2) ** ns, 0.5 ** ns, (1 - 1.0) ** ns],
             lambda i: f"trial {ns[i]}: e = {0.8 ** ns[i]:.3f} (η 0.2), {0.5 ** ns[i]:.4f} (η 0.5), {(0.0 ** ns[i]):.0f} (η 1.0)")
    hb = hov(B, es, [np.abs(1 - es * g)], lambda i: f"η = {es[i]:.2f}: rate {abs(1 - es[i] * g):.2f}")
    return svg(VB, aria, s, "".join(o), ([(A.box, ha), (B.box, hb)],))


# ================================================================ #47 K5: fast and slow learning (script ported)
@lru_cache(maxsize=None)
def k5_run():
    Af, Bf, As, Bs = 0.60, 0.30, 0.995, 0.020
    xf = xs = 0.0
    hist = []
    for n in range(340):
        p = 1.0 if n < 200 else (-1.0 if n < 220 else 0.0)
        x = xf + xs
        e = 0.0 if n >= 220 else p - x
        hist.append((xf, xs, x))
        xf, xs = Af * xf + Bf * e, As * xs + Bs * e
    xx, one = 0.0, []
    for n in range(340):
        p = 1.0 if n < 200 else (-1.0 if n < 220 else 0.0)
        e = 0.0 if n >= 220 else p - xx
        one.append(xx)
        xx = 0.95 * xx + 0.15 * e
    return np.array(hist), np.array(one)


def fig47():
    VB = (0, 0, W, 570)
    s = H.Scale(W, VB[3], display_w=400)
    h, one = k5_run()
    xf, xs, net = h[:, 0], h[:, 1], h[:, 2]
    clamp = net[220:]
    n_reb = 220 + int(clamp.argmax())
    assert tuple(round(v, 3) for v in h[199]) == (0.142, 0.669, 0.811) and tuple(round(v, 3) for v in h[219]) == (-0.561, 0.287, -0.275)
    assert round(clamp.max(), 3) == 0.254 and n_reb == 231
    assert round(one[220], 3) == -0.733 and round(one[339], 3) == -0.002
    n = np.arange(340)
    A = Plot(s, (62, 96, 388, 250), (0, 340), (-0.85, 1.05))
    B = Plot(s, (62, 362, 388, 508), (0, 340), (-0.95, 0.95))
    o = [A.axes(tk((0, 100, 200, 300)), tk((-0.5, 0, 0.5, 1), "{:g}"), "trial n", "net command x", grid=(-0.5, 0.5, 1))]
    o.append(B.axes(tk((0, 100, 200, 300)), tk((-0.5, 0, 0.5), "{:g}"), "trial n", "state", grid=(-0.5, 0.5)))
    for Q in (A, B):
        o.append(rrect(Q.X(200), Q.y1, Q.X(220), Q.y0, O["flag"], 0.16))
        o.append(rrect(Q.X(220), Q.y1, Q.x1, Q.y0, I["rule"], 0.12))
    o.append(href(s, A, 0.0, I["rule"]))
    o.append(href(s, B, 0.0, I["rule"]))
    o.append(A.curve(n, one, SER[1], dash=H.DASH_REF))
    o.append(A.curve(n, net, SER[0]))
    o.append(dot(A, n_reb, clamp.max(), O["flag"]))
    o.append(dot(A, 199, net[199], SER[0]))
    o.append(dot(A, 219, net[219], SER[0]))
    o.append(dot(A, 220, one[220], SER[1]))
    o.append(label(s, A.x1, A.Y(clamp.max()) - 28, f"rebound +{clamp.max():.3f}", L2, I["primary"], "end"))
    o.append(label(s, A.x1, A.Y(clamp.max()) - 12, f"at trial {n_reb}", L2, I["primary"], "end"))
    o.append(label(s, A.X(199) - 6, A.Y(net[199]) - 8, f"{net[199]:.3f}", L2, I["primary"], "end"))
    o.append(legend(s, 62, 16, [(SER[0], "two states (fast + slow)", None)]))
    o.append(legend(s, 62, 34, [(SER[1], "one state, A = 0.95, B = 0.15", H.DASH_REF)]))
    o.append(label(s, 62, 52, "orange: reversal p = −1; grey: error clamp", L2, I["secondary"]))
    o.append(label(s, 62, 68, f"end of reversal: two states {net[219]:.3f}, one state {one[220]:.3f}".replace("-", "−"), L2,
                   I["secondary"]))
    o.append(B.curve(n, xs, I["secondary"]))
    o.append(B.curve(n, xf, SER[2]))
    o.append(legend(s, 62, 326, [(SER[2], "fast x" + sub("f", s) + ": A 0.60, B 0.30", None)]))
    o.append(legend(s, 62, 344, [(I["secondary"], "slow x" + sub("s", s) + ": A 0.995, B 0.020", None)]))
    o.append(label(s, B.X(199) - 6, B.Y(xs[199]) - 9, f"x{sub('s', s)} {xs[199]:.3f}", L2, I["primary"], "end"))
    o.append(label(s, B.X(199) - 6, B.Y(xf[199]) - 12, f"x{sub('f', s)} {xf[199]:.3f}", L2, I["primary"], "end"))
    o.append(label(s, B.X(219) + 3, B.Y(xf[219]) + 17, f"{xf[219]:.3f}".replace("-", "−"), L2, I["primary"]))
    o.append(label(s, B.X(222), B.Y(xs[220]) - 8, f"{xs[219]:.3f}", L2, I["primary"]))
    aria = ("Problem K5: a two-state adaptation model over 340 trials, 200 adaptation trials with perturbation plus 1, 20 "
            "reversal trials with minus 1 (orange band), then an error clamp (grey band). Top: the net command of the two-state "
            f"model, red, peaks at {net[199]:.3f} at the end of adaptation, falls to {net[219]:.3f} after the reversal and "
            f"rebounds to plus {clamp.max():.3f} at trial {n_reb}; the one-state control, blue dashed, ends the reversal at "
            f"{one[220]:.3f} and decays to {one[339]:.3f} without crossing zero. Bottom: the fast state, orange, holds "
            f"{xf[199]:.3f} and the slow state, grey, {xs[199]:.3f} at the end of adaptation; after the reversal they are "
            f"{xf[219]:.3f} and {xs[219]:.3f}.")
    sel = list(range(0, 340, 3)) + [339]
    ha = hov(A, [n[i] for i in sel], [[net[i] for i in sel], [one[i] for i in sel]],
             lambda i: f"trial {sel[i]}: two-state {net[sel[i]]:+.3f}, one-state {one[sel[i]]:+.3f}")
    hb = hov(B, [n[i] for i in sel], [[xs[i] for i in sel], [xf[i] for i in sel]],
             lambda i: f"trial {sel[i]}: slow {xs[sel[i]]:+.3f}, fast {xf[sel[i]]:+.3f}")
    return svg(VB, aria, s, "".join(o), ([(A.box, ha), (B.box, hb)],))


# ================================================================ #49 K6: smoothness from noise (script ported)
@lru_cache(maxsize=None)
def k6_run():
    N, Tm, hold = 100, 0.5, 0.3
    tau_m, mass, D = 0.04, 1.0, 0.40
    h = Tm / N
    Nh = int(hold / h)
    a = np.exp(-h / tau_m)
    Phi = np.array([[1.0, h, 0.0], [0.0, 1.0, h / mass], [0.0, 0.0, a]])
    G = np.array([0.0, 0.0, 1 - a])
    S = np.zeros((N + Nh + 1, N, 3))
    for k in range(N):
        z = np.zeros(3)
        for j in range(k, N + Nh):
            z = Phi @ z + (G if j == k else 0.0)
            S[j + 1, k] = z
    Acon = np.vstack([S[N, :, 0], S[N, :, 1]])
    w = (S[N:, :, 0] ** 2).sum(axis=0) / (Nh + 1)
    Winv = np.diag(1.0 / w)
    u = Winv @ Acon.T @ np.linalg.solve(Acon @ Winv @ Acon.T, np.array([D, 0.0]))
    z, vel = np.zeros(3), []
    for k in range(N):
        z = Phi @ z + G * u[k]
        vel.append(z[1])
    vel = np.array(vel)
    sd = np.sqrt(w @ u ** 2)
    fr = np.round(np.arange(0.10, 0.5001, 0.01), 2)
    ratio = []
    for frac in fr:
        nb = int(round(frac * N))
        ub = np.zeros(N)
        ub[:nb] = np.linalg.lstsq(Acon[:, :nb], np.array([D, 0.0]), rcond=None)[0]
        ratio.append(np.sqrt(w @ ub ** 2) / sd)
    return dict(N=N, T=Tm, D=D, vel=vel, end=(S[N, :, 0] @ u, S[N, :, 1] @ u), fr=fr, ratio=np.array(ratio))


def fig49():
    VB = (0, 0, W, 506)
    s = H.Scale(W, VB[3], display_w=400)
    r = k6_run()
    N, Tm, D, vel = r["N"], r["T"], r["D"], r["vel"]
    assert abs(r["end"][0] - 0.4) < 1e-9 and abs(r["end"][1]) < 1e-9
    pk, ipk = vel.max(), int(vel.argmax())
    pm = pk / (D / Tm)
    assert round(pk, 3) == 1.389 and round(ipk / N, 2) == 0.68 and round(pm, 3) == 1.736
    sdm = {f: r["ratio"][int(np.argmin(abs(r["fr"] - f)))] for f in (0.10, 0.25, 0.50)}
    assert [round(sdm[f], 1) for f in (0.5, 0.25, 0.10)] == [3.2, 10.0, 42.4]      # text
    tau = np.concatenate([[0.0], (np.arange(N) + 1) / N])
    v = np.concatenate([[0.0], vel]) / (D / Tm)
    vj = 30 * tau ** 2 * (1 - tau) ** 2
    A = Plot(s, (62, 66, 388, 226), (0, 1), (0, 2.1))
    B = Plot(s, (62, 322, 388, 458), (0.1, 0.5), (0, 46))
    o = [A.axes(tk((0, 0.25, 0.5, 0.75, 1.0), "{:.2f}"), tk((0, 1, 2)), "normalised time τ = t/T", "speed v·T/D", grid=(1, 2))]
    o.append(B.axes(tk((0.1, 0.2, 0.3, 0.4, 0.5), "{:.1f}"), tk((0, 10, 20, 30, 40)), "share of the movement that carries the command",
                    "endpoint SD (× optimum)", grid=(10, 20, 30, 40)))
    o.append(A.curve(tau, vj, SER[1], dash=H.DASH_REF))
    o.append(A.curve(tau, v, SER[0]))
    o.append(dot(A, ipk / N, pm, SER[0]))
    o.append(dot(A, 0.5, 1.875, SER[1]))
    o.append(label(s, A.X(ipk / N) + 8, A.Y(pm) - 9, f"{pm:.3f} at τ = {ipk / N:.2f}", L2))
    o.append(label(s, A.X(0.5) - 8, A.Y(1.875) - 9, "1.875 at 0.50", L2, I["primary"], "end"))
    o.append(legend(s, 62, 16, [(SER[0], "min-variance optimum", None)]))
    o.append(legend(s, 62, 34, [(SER[1], "minimum jerk", H.DASH_REF)]))
    o.append(label(s, 62, 54, f"peak {pk:.3f} m/s, ends at {r['end'][0]:.4f} m and at rest", L2, I["secondary"]))
    o.append(B.curve(r["fr"], r["ratio"], SER[0]))
    for f in (0.10, 0.25, 0.50):
        o.append(dot(B, f, sdm[f], SER[0]))
    o.append(label(s, B.X(0.10) + 9, B.Y(sdm[0.10]) + 5, f"{sdm[0.10]:.1f}×", L2))
    o.append(label(s, B.X(0.25) + 9, B.Y(sdm[0.25]) - 5, f"{sdm[0.25]:.1f}×", L2))
    o.append(label(s, B.X(0.50) - 9, B.Y(sdm[0.50]) - 9, f"{sdm[0.50]:.1f}×", L2, I["primary"], "end"))
    o.append(label(s, 62, 290, "same command crammed into the first 10%, 25%, 50%", L2, I["secondary"]))
    o.append(label(s, 62, 306, "(the optimum spreads over the whole movement = 1)", L2, I["secondary"]))
    aria = ("Problem K6: the minimum-endpoint-variance command for a 0.4 metre reach in 0.5 seconds with a 40 millisecond "
            "command lag and a 0.3 second hold. Top: the speed profile, speed times T over D against normalised time. The "
            f"computed optimum, a solid red curve, peaks at {pm:.3f} at tau {ipk / N:.2f}, lower and later than the dashed "
            "blue minimum-jerk profile, which peaks at 1.875 at tau 0.50. Bottom: the endpoint standard deviation, as a "
            "multiple of the optimum, when the same command is crammed into the first 50, 25 and 10 percent of the movement: "
            f"{sdm[0.5]:.1f}, {sdm[0.25]:.1f} and {sdm[0.1]:.1f} times.")
    ha = hov(A, tau, [v, vj], lambda i: f"τ = {tau[i]:.2f}: optimum {v[i]:.3f}, minimum jerk {vj[i]:.3f}")
    hb = hov(B, r["fr"], [r["ratio"]], lambda i: f"first {100 * r['fr'][i]:.0f}% of the movement: endpoint SD {r['ratio'][i]:.1f}× optimum")
    return svg(VB, aria, s, "".join(o), ([(A.box, ha), (B.box, hb)],))


# ================================================================ #53 K8: entrainment bandwidth (script ported)
@lru_cache(maxsize=None)
def k8_sim():
    """Euler dpsi/dt = dw - 2 kappa sin(psi), dt = 1 ms for 400 s (the K8 script), all runs in one vector."""
    runs = [(0.5, d) for d in (0.5, 0.9, 1.0, 1.2)] + [(k, f * 2 * k) for k in (0.25, 0.5, 1.0) for f in (0.9, 1.1)]
    kap = np.array([r[0] for r in runs])
    dw = np.array([r[1] for r in runs])
    psi = np.zeros(len(runs))
    for _ in range(400000):
        psi += 0.001 * (dw - 2 * kap * np.sin(psi))
    return runs, psi


def fig53():
    VB = (0, 0, W, 528)
    s = H.Scale(W, VB[3], display_w=400)
    runs, psi = k8_sim()
    res = dict(zip(runs, psi))
    lags = {d: math.degrees(res[(0.5, d)]) for d in (0.5, 0.9, 1.0)}
    assert [round(lags[d], 1) for d in (0.5, 0.9, 1.0)] == [30.0, 64.2, 89.7] and round(res[(0.5, 1.2)]) == 265
    for (k, d), v in res.items():                                              # locks below 2 kappa, drifts above
        assert (abs(v) < math.pi) == (d <= 2 * k + 1e-9), (k, d, v)
    cyc = res[(0.5, 1.2)] / (2 * math.pi)
    assert round(cyc) == 42
    A = Plot(s, (62, 82, 388, 232), (0, 1.05), (0, 2.2))
    B = Plot(s, (62, 330, 388, 456), (0, 1.3), (0, 100))
    ks = np.linspace(0, 1.05, 22)
    o = [A.axes(tk((0, 0.25, 0.5, 0.75, 1.0), "{:g}"), tk((0, 1, 2)), "coupling κ (rad/s)", "|Δω| (rad/s)", grid=(1, 2))]
    o.append(B.axes(tk((0, 0.25, 0.5, 0.75, 1.0, 1.25), "{:g}"), tk((0, 30, 60, 90)), "frequency mismatch Δω (rad/s), κ = 0.5",
                    "locked lag ψ* (°)", grid=(30, 60, 90)))
    o.append(region([(A.X(0), A.Y(0)), (A.X(1.05), A.Y(0)), (A.X(1.05), A.Y(2.1)), (A.X(0), A.Y(0))], O["neural"], 0.10))
    o.append(A.curve(ks, 2 * ks, SER[0]))
    for k in (0.25, 0.5, 1.0):
        o.append(dot(A, k, 2 * k, SER[0]))
    o.append(label(s, A.X(0.25) - 8, A.Y(0.5) - 8, "0.50", L2, I["primary"], "end"))
    o.append(label(s, A.X(0.5) + 9, A.Y(1.0) + 19, "1.00", L2, I["primary"]))
    o.append(label(s, A.X(1.0) - 8, A.Y(2.0) - 8, "2.00", L2, I["primary"], "end"))
    for d in (0.5, 0.9):
        o.append(dot(A, 0.5, d, I["primary"]))
    o.append(dot(A, 0.5, 1.0, I["primary"]))
    o.append(hdot(A, 0.5, 1.2, I["primary"]))
    o.append(label(s, A.X(0.62), A.Y(0.4), "locked", "label", I["primary"]))
    o.append(label(s, A.X(0.1), A.Y(1.9), "drifts", "label", I["primary"]))
    o.append(label(s, 62, 16, "|Δω| = 2κ: bandwidth 0.50, 1.00, 2.00 rad/s", L2, I["secondary"]))
    o.append(label(s, 62, 32, "κ = 0.5: Δω = 0.5, 0.9, 1.0 lock (filled dots)", L2, I["secondary"]))
    o.append(label(s, 62, 48, "Δω = 1.2 drifts (open dot); 400 s at 1 ms", L2, I["secondary"]))
    o.append(label(s, 62, 64, "green tint: locked region", L2, I["secondary"]))
    # panel B: lag against mismatch at kappa = 0.5
    kap = 0.5
    ds = np.linspace(0, 2 * kap, 101)
    lag = np.degrees(np.arcsin(ds / (2 * kap)))
    o.append(rrect(B.X(1.0), B.y1, B.x1, B.y0, I["rule"], 0.12))
    o.append(B.curve(ds, lag, SER[1]))
    for d in (0.5, 0.9, 1.0):
        o.append(dot(B, d, lags[d], SER[1]))
    o.append(label(s, B.X(0.5) + 9, B.Y(lags[0.5]) + 14, f"{lags[0.5]:.1f}°", L2))
    o.append(label(s, B.X(0.9) - 9, B.Y(lags[0.9]) - 4, f"{lags[0.9]:.1f}°", L2, I["primary"], "end"))
    o.append(label(s, B.X(1.0) - 9, B.Y(lags[1.0]) - 12, f"{lags[1.0]:.1f}° at 400 s", L2, I["primary"], "end"))
    o.append(label(s, B.X(1.04), B.Y(60), "no lock:", L2, I["secondary"]))
    o.append(label(s, B.X(1.04), B.Y(60) + 16, f"ψ runs to", L2, I["secondary"]))
    o.append(label(s, B.X(1.04), B.Y(60) + 32, f"{res[(0.5, 1.2)]:.0f} rad", L2, I["secondary"]))
    o.append(label(s, 62, 302, "ψ* = arcsin(Δω / 2κ): lag sweeps 0° to 90°", L2, I["secondary"]))
    o.append(label(s, 62, 318, "across the locking band", L2, I["secondary"]))
    aria = ("Problem K8: entrainment of two coupled oscillators, psi-dot equals delta omega minus 2 kappa sine psi integrated "
            "for 400 seconds. Top: the locking boundary, absolute frequency mismatch equal to 2 kappa, a red line through "
            "0.50, 1.00 and 2.00 radians per second at kappa 0.25, 0.5 and 1.0, with the locked region tinted green below it. "
            "At kappa 0.5 the integration locks for mismatch 0.5, 0.9 and 1.0 and drifts for 1.2. Bottom: the locked phase lag "
            f"at kappa 0.5 against mismatch, a blue arcsine curve rising from 0 to 90 degrees; the integration gives "
            f"{lags[0.5]:.1f}, {lags[0.9]:.1f} and {lags[1.0]:.1f} degrees at 0.5, 0.9 and 1.0, and at 1.2 the phase runs "
            f"to {res[(0.5, 1.2)]:.0f} radians.")
    ha = hov(A, ks, [2 * ks], lambda i: f"κ = {ks[i]:.2f}: locks for |Δω| ≤ {2 * ks[i]:.2f} rad/s")
    hb = hov(B, ds, [lag], lambda i: f"Δω = {ds[i]:.2f} rad/s: locked lag {lag[i]:.1f}°")
    return svg(VB, aria, s, "".join(o), ([(A.box, ha), (B.box, hb)],))


# ================================================================ #55 K9: counting synergies (script ported)
@lru_cache(maxsize=None)
def k9_run():
    rng = np.random.default_rng(0)
    n_mus, k_true, n_samp = 8, 3, 300
    Wm = rng.random((n_mus, k_true))
    Wm /= np.linalg.norm(Wm, axis=0)
    C = rng.random((k_true, n_samp))
    M0 = Wm @ C
    M = np.clip(M0 + 0.05 * M0.std() * rng.standard_normal(M0.shape), 0.0, None)
    Mc = M - M.mean(axis=1, keepdims=True)
    sv = np.linalg.svd(Mc, compute_uv=False)
    vaf = np.cumsum(sv ** 2) / (sv ** 2).sum()
    return vaf[:5], np.diff(np.concatenate([[0.0], vaf[:5]]))


def fig55():
    VB = (0, 0, W, 492)
    s = H.Scale(W, VB[3], display_w=400)
    vaf, inc = k9_run()
    assert [round(v, 3) for v in vaf] == [0.745, 0.924, 0.998, 0.998, 0.999]
    assert [round(v, 4) for v in inc[:3]] == [0.7453, 0.1787, 0.0736] and round(inc[3], 6) == 0.000564 and round(inc[4], 6) == 0.000512
    drop = inc[2] / inc[3]
    assert round(drop) == 130
    ks = np.arange(1, 6)
    A = Plot(s, (62, 62, 388, 212), (0.5, 5.5), (0.7, 1.1))
    B = Plot(s, (62, 320, 388, 440), (0.5, 5.5), (-4.3, 0.2))
    lg = np.log10(inc)
    o = [A.axes(tk(ks), tk((0.7, 0.8, 0.9, 1.0), "{:.1f}"), "number of synergies k", "cumulative VAF", grid=(0.8, 1.0))]
    o.append(B.axes(tk(ks), [(0, "1"), (-1, "0.1"), (-2, "0.01"), (-3, "0.001")], "component number k",
                    "variance added", grid=(-1, -2, -3)))
    o.append(href(s, A, 0.9, O["flag"]))
    o.append(vref(s, A, 3, I["rule"]))
    o.append(A.curve(ks, vaf, SER[0]))
    for k, v in zip(ks, vaf):
        o.append(dot(A, k, v, SER[0]))
    o.append(label(s, A.X(1) + 8, A.Y(vaf[0]) + 17, f"{vaf[0]:.3f}", L2, I["primary"]))
    o.append(label(s, A.X(2) - 8, A.Y(vaf[1]) - 9, f"{vaf[1]:.3f}", L2, I["primary"], "end"))
    o.append(label(s, A.X(3) - 6, A.Y(vaf[2]) - 9, f"{vaf[2]:.3f}", L2, I["primary"], "end"))
    for k in (4, 5):
        o.append(label(s, A.X(k), A.Y(vaf[k - 1]) - 9, f"{vaf[k - 1]:.3f}", L2, I["primary"], "middle"))
    o.append(label(s, A.X(3) + 7, A.Y(0.9) + 17, "k = 2 already passes 90%", L2, I["secondary"]))
    o.append(label(s, A.X(3) + 6, A.Y(0.75), "true k = 3", L2, I["secondary"]))
    o.append(label(s, 62, 18, "8 muscles, 3 synergies, noise 5% of the SD, 300 samples", L2, I["secondary"]))
    o.append(label(s, 62, 36, "orange dashed: the 90% threshold", L2, I["secondary"]))
    o.append(vref(s, B, 3, I["rule"]))
    o.append(href(s, B, math.log10(5e-4), O["flag"], x0=3.0, x1=5.5))
    o.append(B.curve(ks, lg, SER[1]))
    for k, v in zip(ks, lg):
        o.append(dot(B, k, v, SER[1]))
    for k in (1, 2, 3):
        o.append(label(s, B.X(k) + 8, B.Y(lg[k - 1]) - 8, f"{inc[k - 1]:.4f}", L2, I["primary"]))
    o.append(label(s, B.X(4) + 8, B.Y(lg[3]) - 9, f"{inc[3]:.6f}", L2, I["primary"]))
    o.append(label(s, B.X(5), B.Y(lg[4]) + 20, f"{inc[4]:.6f}", L2, I["primary"], "end"))
    o.append(label(s, B.X(3.5), B.Y(-1.85), f"{drop:.0f}× drop after k = 3", L2))
    o.append(label(s, 62, 290, "increments, log scale; orange dashed:", L2, I["secondary"]))
    o.append(label(s, 62, 306 - 2, "the 5×10⁻⁴ noise floor", L2, I["secondary"]))
    aria = ("Problem K9: counting synergies in synthetic eight-muscle activity built from 3 synergies plus noise at 5 percent of "
            f"the data standard deviation. Top: the cumulative variance accounted for against k, red: {vaf[0]:.3f}, {vaf[1]:.3f}, "
            f"{vaf[2]:.3f}, {vaf[3]:.3f}, {vaf[4]:.3f}. It crosses the orange dashed 90 percent line already at k = 2, so the "
            "threshold understates the true dimension 3. Bottom: the variance each component adds on a log axis, blue: "
            f"{inc[0]:.4f}, {inc[1]:.4f}, {inc[2]:.4f}, then {inc[3]:.6f} and {inc[4]:.6f}, a factor {drop:.0f} drop after "
            "k = 3 to a flat noise floor near 5 times 10 to the minus 4. The elbow, not the threshold, identifies the rank.")
    ha = hov(A, ks, [vaf], lambda i: f"k = {ks[i]}: cumulative VAF {vaf[i]:.4f}")
    hb = hov(B, ks, [lg], lambda i: f"component {ks[i]} adds {inc[i]:.6f}")
    return svg(VB, aria, s, "".join(o), ([(A.box, ha), (B.box, hb)],))


# ================================================================ #57 K10: gain limited by delay
def fig57():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    tds = (0.05, 0.10, 0.15, 0.20)
    kmax = {t: math.pi / (2 * t) for t in tds}
    assert [round(v, 2) for v in kmax.values()] == [31.42, 15.71, 10.47, 7.85] and abs(kmax[0.05] / kmax[0.10] - 2) < 1e-12
    for tdl, kk, grows in ((0.10, 14.0, False), (0.10, 18.0, True)):          # delayed loop dx/dt = -k x(t - td), Euler
        dt, d = 1e-3, int(round(tdl / 1e-3))
        x = [1.0] * (d + 1)
        for _ in range(40000):
            x.append(x[-1] - dt * kk * x[-1 - d])
        assert (max(abs(v) for v in x[-2000:]) > 1.0) == grows
    P = Plot(s, (62, 66, 388, 214), (0.04, 0.25), (0, 42))
    td = np.linspace(0.04, 0.25, 106)
    km = np.pi / (2 * td)
    o = [P.axes(tk((0.05, 0.10, 0.15, 0.20, 0.25), "{:.2f}"), tk((0, 10, 20, 30, 40)), "delay τ" + sub("d", s) + " (s)",
                "gain ceiling (1/s)", grid=(10, 20, 30, 40), ytx=13)]
    o.append(rrect(P.X(0.10), P.y1, P.X(0.20), P.y0, I["rule"], 0.18))
    below = [(P.X(a), P.Y(b)) for a, b in zip(td, km)] + [(P.X(0.25), P.Y(0)), (P.X(0.04), P.Y(0))]
    o.append(region(below, O["neural"], 0.10))
    o.append(P.curve(td, km, SER[0]))
    for t, v in kmax.items():
        o.append(dot(P, t, v, SER[0]))
    o.append(label(s, P.X(0.05) + 8, P.Y(kmax[0.05]) - 6, f"{kmax[0.05]:.2f}", L2, I["primary"]))
    o.append(label(s, P.X(0.10) + 8, P.Y(kmax[0.10]) - 8, f"{kmax[0.10]:.2f}", L2, I["primary"]))
    o.append(label(s, P.X(0.15) + 8, P.Y(kmax[0.15]) - 8, f"{kmax[0.15]:.2f}", L2, I["primary"]))
    o.append(label(s, P.X(0.20) + 4, P.Y(kmax[0.20]) - 9, f"{kmax[0.20]:.2f}", L2, I["primary"]))
    o.append(label(s, P.X(0.225), P.Y(31), "unstable", "label", I["primary"], "middle"))
    o.append(label(s, P.X(0.225), P.Y(2), "stable", "label", I["primary"], "middle"))
    o.append(label(s, 62, 16, "k" + sub("max", s) + " = π/(2τ" + sub("d", s) + "), from dx/dt = −k x(t − τ" + sub("d", s) + ")", L2,
                   I["secondary"]))
    o.append(label(s, 62, 34, "grey band: arm delay 100–200 ms,", L2, I["secondary"]))
    o.append(label(s, 62, 50, "gain ceiling 15.71 to 7.85 per s", L2, I["secondary"]))
    o.append(label(s, 62, P.y0 + 58, "doubling the delay halves the ceiling: 31.42 to 15.71 per s", L2, I["secondary"]))
    aria = ("Problem K10: the maximum stable feedback gain of the delayed first-order loop dx/dt equals minus k x(t minus "
            "delay), k max equal to pi over twice the delay, against the delay from 0.04 to 0.25 seconds. The red curve falls "
            "as one over the delay; dots at 0.05, 0.10, 0.15 and 0.20 seconds give 31.42, 15.71, 10.47 and 7.85 per second. "
            "Below the curve, tinted green, the loop is stable; above it, unstable. A grey band marks the arm's own 100 to "
            "200 millisecond delay, which caps the gain at 15.71 to 7.85 per second.")
    hv = hov(P, td, [km], lambda i: f"delay {td[i]:.3f} s: k max = {km[i]:.2f} per s")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


FIGS = {
    36: ("D8: the UCM variance ratio. For two noisy effectors whose su", fig36),
    37: ("D9: oscillator locking. Derive the phase-difference dynamics", fig37),
    38: ("D10: synergy rank bound. Show that if muscle activity is a c", fig38),
    39: ("K1: which smoothness cost? (regime comparison). Compute and ", fig39),
    41: ("K2: tuning the LQR (sensitivity + inverse). For the point-ma", fig41),
    45: ("K4: force-field adaptation (simulation + stability sweep). S", fig45),
    47: ("K5: fast and slow learning. Net command over 340 trials: 200", fig47),
    49: ("K6: smoothness from noise (optimisation). With signal-depend", fig49),
    53: ("K8: entrainment bandwidth (simulation + inverse). Integrate ", fig53),
    55: ("K9: counting synergies (dimensionality / inverse). Generate ", fig55),
    57: ("K10: gain limited by delay (regime comparison). For a delaye", fig57),
}
