"""Module 15 problem-set plots (group `prob_k`; svg #25 26 27 34 35 36 42 43 45 47 49 51 54 56), 400 px figures.

Every plotted number is computed here from the module's own formula or listing (module15.html):
  #25 C3   Prop. 3.1 set-up: sigma 0.006 rad, 0.40 rad at 0.8 Hz, fs 100 Hz; np.gradient twice (listing stencil)
  #26 C4   Prop. 3.1 compact second difference, sd = sigma sqrt(6)/dt^2 (line 735), simulated at 4 rates
  #27 C5   Prop. 4.1 (bias, noise, total RMS velocity error; Fig. 4 data) + velocity traces at 1.2 and 3.0 Hz
  #34 D2   Var = sigma^2/(2 dt^2) (line 769), #35 D3 Var = 6 sigma^2/dt^4 (line 773), checked by simulation
  #36 D4   MSE = bias^2 + variance (line 777), checked against the directly simulated MSE
  #42 D10  normal equations (line 801) on the Lab D squat data (seed 15), beta = 1/M
  #43 K1   the K1 listing (line 811-828), #45 K2 the K2 listing (line 833-880) + Lab A knee
  #47 K3   Lab B pipeline at 1.5, 3.4 and 20 Hz on one trial, #49 K5 Lab D squat with a 15% mass error / under-smoothing
  #51 K7   the K7 listing (20 000 draws), #54 K9 the K9 listing (sweeps), #56 K10 the quadrature model (line 1005)
This file does NOT expose SHARED_DEFS (no body art here).
"""
import html
import math
import re
from functools import lru_cache

import numpy as np
from scipy.signal import butter, filtfilt

import house as H
from m05.plots_prob import Plot, label, legend, hov, sub, text_w
from m15.plots_main import (A0, DT, F0, G, IZ, LAB_FCS, LL, MZ, Q_TRUE, QDD_TRUE, SIG, TAU_TRUE, TRIM, TT,
                            bias_variance, lab_a, lab_b, lab_d_data, mn, pipeline, smooth)

O, I, SER = H.OVERLAY, H.INK, H.SERIES
RED, BLUE, ORANGE = SER[0], SER[1], SER[2]
GRID = "#e6e6e6"
W = 400                     # viewBox width = rendered width: one user unit is one rendered px


# ---------------------------------------------------------------- scaffold
class LP(Plot):
    """Plot with optional log axes. Ticks and curves use the same X, Y (data units in, user units out)."""

    def __init__(self, s, box, xr, yr, xlog=False, ylog=False):
        super().__init__(s, box, xr, yr)
        self.xlog, self.ylog = xlog, ylog

    @staticmethod
    def _f(v, r, log):
        if log:
            return (math.log10(v) - math.log10(r[0])) / (math.log10(r[1]) - math.log10(r[0]))
        return (v - r[0]) / (r[1] - r[0])

    def X(self, v):
        return self.x0 + self._f(v, self.xr, self.xlog) * (self.x1 - self.x0)

    def Y(self, v):
        return self.y0 - self._f(v, self.yr, self.ylog) * (self.y0 - self.y1)


def fin(VB, aria, s, body, panels):
    """Wrap: svg_open with hover on every panel; drop the empty axis titles of stacked panels."""
    body = re.sub(r"<text[^>]*></text>", "", "".join(body))
    return H.svg_open(VB, html.escape(aria), s, extra=H.hover_attr(panels)) + body + "</svg>"


def tag(s, x, y, col, text, dash=None):
    """One legend entry: coloured line, then ink text."""
    return legend(s, x, y, [(col, text, dash)])


def leg(s, x, y, items, dot_text=None, gap=14, dot_col=I["primary"]):
    """Legend row of line entries, then (optionally) a black dot entry. Widths use the same estimate as legend()."""
    o = []
    for col, txt, dash in items:
        o.append(legend(s, x, y, [(col, txt, dash)]))
        x += 25 + text_w(txt, 13) + gap
    if dot_text:
        o.append(f'<circle cx="{x + 8:.2f}" cy="{y - 4:.2f}" r="{s(3):.2f}" fill="{dot_col}"/>')
        o.append(label(s, x + 18, y, dot_text, "label2", I["secondary"]))
    return "".join(o)


def hat(c, s):
    """Letter with a circumflex (Georgia has no combining marks in SVG text): spacing modifier placed by dx, dy."""
    return f'{c}<tspan dx="{-s(2):.2f}" baseline-shift="super" font-size="{s(13):.2f}">ˆ</tspan>'


def sup(t, s):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX["label"] * 0.7):.2f}">{t}</tspan>'


def dots(P, xs, ys, col, r=2.4):
    s = P.s
    return "".join(f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{s(r):.2f}" fill="{col}"/>' for x, y in zip(xs, ys))


def mark(P, x, y, col=I["primary"], hollow=False):
    s = P.s
    r = s(H.PX["dot"])
    if hollow:
        return (f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{r:.2f}" fill="#fff" stroke="{col}" '
                f'stroke-width="{s(1.8):.2f}"/>')
    return P.dot(x, y, col)


def vline(P, x, col=O["dim"], y_top=None, y_bot=None):
    s = P.s
    return H.line(s, P.X(x), P.y1 if y_top is None else y_top, P.X(x), P.y0 if y_bot is None else y_bot, col, "ref", H.DASH_REF)


def hline(P, y, col=O["dim"]):
    return H.line(P.s, P.x0, P.Y(y), P.x1, P.Y(y), col, "ref", H.DASH_REF)



# ================================================================ svg #25 C3: invisible noise, visible ruin
@lru_cache(None)
def c3_data():
    qm = Q_TRUE + np.random.default_rng(15).normal(0, SIG, TT.size)
    acc = np.gradient(np.gradient(qm, DT), DT)
    return qm, acc


def fig25():
    VB = (0, 0, W, 428)
    s = H.Scale(W, VB[3], display_w=400)
    qm, acc = c3_data()
    t = TT[TRIM]
    sd_th = SIG * math.sqrt(6) / (4 * DT ** 2)                                 # np.gradient twice (K1 line 811)
    sd_obs = float(np.std((acc - QDD_TRUE)[TRIM]))
    pk = float(np.abs(QDD_TRUE).max())
    assert abs(sd_th - 36.7) < 0.1 and abs(sd_obs / sd_th - 1) < 0.15 and abs(pk - 10.1) < 0.05, (sd_th, sd_obs, pk)
    A = LP(s, (58, 38, 388, 168), (0, 2), (-0.5, 0.5))
    B = LP(s, (58, 212, 388, 342), (0, 2), (-130, 130))
    o = [A.axes([], [(-0.4, "−0.4"), (0, "0"), (0.4, "0.4")], "", "angle (rad)", grid=(-0.4, 0, 0.4), ytx=14),
         B.axes([(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)], [(-100, "−100"), (0, "0"), (100, "100")], "time (s)",
                "acceleration (rad/s²)".replace("acceleration", "accel."), grid=(-100, 0, 100), ytx=14)]
    o.append(dots(A, t[::3], qm[TRIM][::3], ORANGE, 2.6))
    o.append(A.curve(t, Q_TRUE[TRIM], RED))
    o.append(B.curve(t, acc[TRIM], ORANGE, multi=True))
    o.append(B.curve(t, QDD_TRUE[TRIM], RED, multi=True, dash=(7, 4)))
    o.append(leg(s, 58, 18, [(RED, "true", None)], "measured, σ = 0.006 rad", gap=12, dot_col=ORANGE))
    o.append(label(s, 58, 190, "noise is 1.5% of the 0.40 rad amplitude: invisible", "label2", I["secondary"]))
    o.append(label(s, 58, 404, f"raw second difference: noise sd {sd_obs:.0f} rad/s² in this trial", "label2", I["secondary"]))
    o.append(label(s, 58, 420, f"(theory {sd_th:.1f}); the true acceleration peaks at {pk:.1f}", "label2", I["secondary"]))
    hv = [(A.box, hov(A, t, [Q_TRUE[TRIM], qm[TRIM]], lambda i: f"t = {t[i]:.2f} s: true {Q_TRUE[TRIM][i]:.3f} rad, measured {qm[TRIM][i]:.3f}")),
          (B.box, hov(B, t, [QDD_TRUE[TRIM], acc[TRIM]], lambda i: f"t = {t[i]:.2f} s: true {mn(QDD_TRUE[TRIM][i], '{:.1f}')} rad/s², raw {mn(acc[TRIM][i], '{:.1f}')}"))]
    aria = ("Problem C3 plot, two panels over two seconds. Top: a 0.40 rad, 0.8 Hz joint angle in red with orange measured samples "
            "carrying 0.006 rad noise, lying almost on the curve. Bottom: the second difference of those samples in orange swings "
            f"about {sd_obs:.0f} radians per second squared either side of the red dashed true acceleration, which peaks at only {pk:.1f}.")
    return fin(VB, aria, s, o, hv)


# ================================================================ svg #26 C4: faster is worse
def fig26():
    VB = (0, 0, W, 306)
    s = H.Scale(W, VB[3], display_w=400)
    fs_grid = np.arange(50, 400.1, 5.0)
    sd = lambda f: SIG * math.sqrt(6) * f ** 2                                  # Prop. 3.1: sigma sqrt(6)/dt^2   # noqa: E731
    pk = float(np.abs(QDD_TRUE).max())
    rng = np.random.default_rng(15)
    sim = []
    for f in (50, 100, 200, 400):
        e = rng.normal(0, SIG, 40000)
        sim.append(float(np.std((e[2:] - 2 * e[1:-1] + e[:-2]) * f ** 2)))
    assert all(abs(a / sd(f) - 1) < 0.03 for a, f in zip(sim, (50, 100, 200, 400))), sim
    assert abs(sd(400) / sd(50) - 64) < 1e-9
    P = LP(s, (58, 40, 372, 224), (50, 400), (8, 4000), ylog=True)
    o = [P.axes([(v, str(v)) for v in (50, 100, 200, 400)], [(10, "10"), (100, "100"), (1000, "1000")], "",
                "noise sd (rad/s²)", grid=(10, 100, 1000), ytx=14)]
    o.append(hline(P, pk, I["primary"]))
    o.append(P.curve(fs_grid, [sd(f) for f in fs_grid], ORANGE))
    o.append(dots(P, (50, 100, 200, 400), sim, I["primary"], 3))
    for f, dt in ((50, "20 ms"), (100, "10 ms"), (200, "5 ms"), (400, "2.5 ms")):
        o.append(label(s, P.X(f), P.y0 + 34, dt, "label2", I["secondary"], "middle"))
    o.append(label(s, 58 + 330 / 2 - 14, P.y0 + 54, "sampling rate (Hz) and interval Δt", "label", I["primary"], "middle"))
    o.append(label(s, P.x1 - 4, P.Y(pk) - 7, f"true acceleration peak {pk:.1f}", "label2", I["primary"], "end"))
    o.append(label(s, P.x0 + 10, P.y1 + 14, f"{sd(50):.0f} at 50 Hz, {sd(400):.0f} at 400 Hz: ×64", "label2", I["primary"]))
    o.append(leg(s, 58, 18, [(ORANGE, "σ√6/Δt² (Prop. 3.1)", None)], "simulated", gap=12))
    hv = hov(P, fs_grid, [[sd(f) for f in fs_grid]], lambda i: f"fs = {fs_grid[i]:.0f} Hz (Δt = {1000 / fs_grid[i]:.1f} ms): sd {sd(fs_grid[i]):.0f} rad/s²")
    aria = ("Problem C4 plot: the standard deviation of the raw second-difference acceleration against sampling rate from 50 to 400 "
            f"hertz, on a log axis. The orange curve, sigma root six over delta t squared, rises from {sd(50):.0f} to {sd(400):.0f} "
            "radians per second squared, a factor of 64; black dots from simulation lie on it. A dashed line marks the true "
            f"acceleration peak of {pk:.1f}.")
    return fin(VB, aria, s, o, [(P.box, hv)])


# ================================================================ svg #27 C5 and #36 D4: bias and variance
@lru_cache(None)
def bv_rows():
    """Fig. 4 data (bias_variance, seed 1, 400 draws) with 15 extra cutoffs around the minimum, so the minimum is resolved."""
    base = bias_variance()
    v_true = A0 * 2 * np.pi * F0 * np.cos(2 * np.pi * F0 * TT)
    noise = np.random.default_rng(1).normal(0, SIG, (400, TT.size))
    extra = []
    for fc in np.geomspace(2.4, 3.8, 15):
        vb = np.gradient(smooth(Q_TRUE, fc), DT)
        vs = np.gradient(smooth(Q_TRUE[None, :] + noise, fc), DT, axis=-1)
        bias = float(np.sqrt(np.mean((vb - v_true)[TRIM] ** 2)))
        sd = float(np.sqrt(np.mean((vs - vb)[:, TRIM] ** 2)))
        extra.append((fc, bias, sd, math.hypot(bias, sd)))
    r = np.vstack([base, np.array(extra)])
    return r[np.argsort(r[:, 0])]


@lru_cache(None)
def vel_traces():
    qm = Q_TRUE + np.random.default_rng(15).normal(0, SIG, TT.size)
    v_true = A0 * 2 * np.pi * F0 * np.cos(2 * np.pi * F0 * TT)
    return v_true, {fc: np.gradient(smooth(qm, fc), DT) for fc in (1.2, 3.0)}


def fig27():
    VB = (0, 0, W, 502)
    s = H.Scale(W, VB[3], display_w=400)
    r = bv_rows()
    j = int(r[:, 3].argmin())
    assert abs(r[j, 0] - 3.0) < 0.15 and abs(r[j, 3] - 0.0205) < 0.0006                      # Fig. 4, lines 252-253
    A = LP(s, (58, 40, 388, 200), (1.2, 45), (0, 0.45), xlog=True)
    o = [A.axes([(v, str(v)) for v in (2, 5, 10, 20, 40)], [(0, "0"), (0.15, "0.15"), (0.30, "0.30"), (0.45, "0.45")],
                "filter cutoff f (Hz)", "RMS velocity error (rad/s)".replace("RMS velocity error", "RMS error"), grid=(0.15, 0.30, 0.45), ytx=14)]
    o[0] = o[0].replace(">filter cutoff f (Hz)<", f">filter cutoff f{sub('c', s)} (Hz)<")
    o.append(vline(A, r[j, 0]))
    o.append(A.curve(r[:, 0], r[:, 2], ORANGE, multi=True, dash=(7, 4)))
    o.append(A.curve(r[:, 0], r[:, 1], BLUE, multi=True, dash=(7, 4)))
    o.append(A.curve(r[:, 0], r[:, 3], RED))
    o.append(mark(A, r[j, 0], r[j, 3]))
    o.append(label(s, A.X(r[j, 0]) + 12, A.Y(0.22), f"minimum ≈ {r[j, 3]:.2f} rad/s", "label2", I["primary"]))
    o.append(label(s, A.X(r[j, 0]) + 12, A.Y(0.22) + 16, f"at {r[j, 0]:.1f} Hz", "label2", I["primary"]))
    o.append(label(s, A.X(1.2) + 4, A.Y(0.42), "smoothest:", "label2", I["secondary"]))
    o.append(label(s, A.X(1.2) + 4, A.Y(0.42) + 16, f"error {r[0, 3]:.2f}", "label2", I["secondary"]))
    o.append(leg(s, 58, 18, [(RED, "total", None), (BLUE, "bias", (7, 4)), (ORANGE, "noise sd", (7, 4))]))
    v_true, vv = vel_traces()
    t = TT[TRIM]
    B = LP(s, (58, 308, 388, 432), (0, 2), (-2.4, 2.4))
    o.append(B.axes([(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)], [(-2, "−2"), (0, "0"), (2, "2")], "time (s)", "velocity (rad/s)", grid=(-2, 0, 2), ytx=14))
    o.append(B.curve(t, v_true[TRIM], RED, multi=True, dash=(7, 4)))
    o.append(B.curve(t, vv[3.0][TRIM], I["primary"], multi=True))
    o.append(B.curve(t, vv[1.2][TRIM], BLUE))
    pk12 = float(np.abs(vv[1.2][TRIM]).max())
    pk_t = float(np.abs(v_true[TRIM]).max())
    o.append(leg(s, 58, 290, [(RED, "true", (7, 4)), (BLUE, "1.2 Hz", None), (I["primary"], "3.0 Hz", None)], gap=12))
    o.append(label(s, 58, 270, "velocity estimated at two cutoffs:", "label2", I["secondary"]))
    o.append(label(s, 58, 494, f"1.2 Hz curve peaks at {pk12:.2f} rad/s; the true peak is {pk_t:.2f}", "label2", I["secondary"]))
    hv = [(A.box, hov(A, r[:, 0], [r[:, 3], r[:, 1], r[:, 2]], lambda i: f"fc = {r[i, 0]:.2f} Hz: total {r[i, 3]:.3f}, bias {r[i, 1]:.3f}, noise {r[i, 2]:.3f} rad/s")),
          (B.box, hov(B, t, [v_true[TRIM], vv[3.0][TRIM], vv[1.2][TRIM]], lambda i: f"t = {t[i]:.2f} s: true {mn(v_true[TRIM][i])}, 3.0 Hz {mn(vv[3.0][TRIM][i])}, 1.2 Hz {mn(vv[1.2][TRIM][i])} rad/s"))]
    aria = ("Problem C5 plot, two panels. Top: RMS velocity error against filter cutoff on a log axis from 1.2 to 45 hertz: the red total "
            f"is U-shaped with a minimum of {r[j, 3]:.3f} rad per second at {r[j, 0]:.1f} hertz; blue dashed bias falls from 0.39 as the cutoff rises; "
            "orange dashed noise rises. Bottom: velocity over two seconds: the 1.2 hertz filter gives a clean blue curve whose peak "
            f"is only {pk12:.2f} rad per second against the true {pk_t:.2f}, while the 3.0 hertz curve lies on the red dashed truth.")
    return fin(VB, aria, s, o, hv)


@lru_cache(None)
def d4_check():
    """Directly simulated MSE of the velocity estimate at 10 cutoffs (400 draws), against bias^2 + variance."""
    v_true = A0 * 2 * np.pi * F0 * np.cos(2 * np.pi * F0 * TT)
    noise = np.random.default_rng(1).normal(0, SIG, (400, TT.size))
    out = []
    for fc in np.geomspace(1.5, 40, 10):
        vb = np.gradient(smooth(Q_TRUE, fc), DT)
        vs = np.gradient(smooth(Q_TRUE[None, :] + noise, fc), DT, axis=-1)
        mse = float(np.mean((vs - v_true)[:, TRIM] ** 2))
        b2 = float(np.mean((vb - v_true)[TRIM] ** 2))
        var = float(np.mean((vs - vb)[:, TRIM] ** 2))
        out.append((fc, mse, b2, var))
    return np.array(out)


def fig36():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    r = bv_rows()
    mse, b2, var = r[:, 3] ** 2, r[:, 1] ** 2, r[:, 2] ** 2
    chk = d4_check()
    assert np.allclose(chk[:, 1], chk[:, 2] + chk[:, 3], rtol=0.02)                    # the identity of D4, simulated
    j = int(mse.argmin())
    ylo = 2e-5
    P = LP(s, (62, 40, 388, 232), (1.2, 45), (ylo, 0.3), xlog=True, ylog=True)
    o = [P.axes([(v, str(v)) for v in (2, 5, 10, 20, 40)], [(1e-4, "10" + sup("−4", s)), (1e-3, "10" + sup("−3", s)), (1e-2, "0.01"), (1e-1, "0.1")],
                "filter cutoff f (Hz)", "MSE ((rad/s)²)", grid=(1e-4, 1e-3, 1e-2, 1e-1), ytx=14)]
    o[0] = o[0].replace(">filter cutoff f (Hz)<", f">filter cutoff f{sub('c', s)} (Hz)<")
    o.append(vline(P, r[j, 0]))
    keep = b2 > ylo
    o.append(P.curve(r[keep, 0], b2[keep], BLUE, multi=True, dash=(7, 4)))
    o.append(P.curve(r[:, 0], var, ORANGE, multi=True, dash=(7, 4)))
    o.append(P.curve(r[:, 0], mse, RED))
    o.append(dots(P, chk[:, 0], chk[:, 1], I["primary"], 3))
    o.append(mark(P, r[j, 0], mse[j]))
    o.append(label(s, P.X(6.5), P.y0 - 10, f"minimum {mse[j]:.4f} at {r[j, 0]:.1f} Hz", "label2", I["primary"]))
    o.append(leg(s, 62, 18, [(RED, "MSE = B² + V", None), (BLUE, "bias² B²", (7, 4)), (ORANGE, "variance V", (7, 4))], gap=10))
    o.append(leg(s, 62, 36, [], "simulated MSE directly, 400 draws", gap=0))
    hv = hov(P, r[:, 0], [mse, np.maximum(b2, ylo), var], lambda i: f"fc = {r[i, 0]:.2f} Hz: MSE {mse[i]:.4f} = bias² {b2[i]:.4f} + variance {var[i]:.4f}")
    aria = ("Problem D4 plot: mean-square velocity error against filter cutoff on log axes, from 1.2 to 45 hertz. The red total equals the "
            "blue dashed bias squared, which falls steeply as the cutoff rises, plus the orange dashed variance, which rises. "
            f"The total is V-shaped with a minimum of {mse[j]:.4f} at {r[j, 0]:.1f} hertz. Ten black dots, the mean square error simulated directly, "
            "lie on the red curve.")
    return fin(VB, aria, s, o, [(P.box, hv)])


# ================================================================ svg #34 D2 and #35 D3: noise of the difference stencils
def stencil_sim(order, dts, n=200000):
    rng = np.random.default_rng(15)
    out = []
    for dt in dts:
        e = rng.normal(0, SIG, n)
        d = (e[2:] - e[:-2]) / (2 * dt) if order == 1 else (e[2:] - 2 * e[1:-1] + e[:-2]) / dt ** 2
        out.append(float(np.std(d)))
    return out


def stems(P, s, xs, ws, wtext):
    o = []
    for x, w, t in zip(xs, ws, wtext):
        o.append(H.line(s, P.X(x), P.Y(0), P.X(x), P.Y(w), RED, "force"))
        o.append(P.dot(x, w, RED))
        ty = P.Y(w) - 9 if w >= 0 else P.Y(w) + 19
        o.append(label(s, P.X(x), ty, t, "label2", I["primary"], "middle"))
    return o


def aj(s):
    return "a" + sub("j", s)


def fig34():
    VB = (0, 0, W, 404)
    s = H.Scale(W, VB[3], display_w=400)
    dts = np.geomspace(0.0025, 0.020, 40)
    sd = lambda dt: SIG / (math.sqrt(2) * dt)                                           # noqa: E731
    dd = (0.0025, 0.005, 0.01, 0.02)
    sim = stencil_sim(1, dd)
    assert all(abs(a / sd(d) - 1) < 0.01 for a, d in zip(sim, dd)) and abs(sd(0.01) - 0.424) < 0.001
    A = LP(s, (58, 60, 388, 168), (0, 4), (-1.3, 0.95))
    o = [A.axes([(1, "k−1"), (2, "k"), (3, "k+1")], [(-0.5, "−½"), (0, "0"), (0.5, "+½")], "", "weight (× 1/Δt)", grid=(-0.5, 0, 0.5), ytx=14)]
    o += stems(A, s, (1, 2, 3), (-0.5, 0, 0.5), ("−1/(2Δt)", "0", "+1/(2Δt)"))
    o.append(label(s, 58, 18, f"Σ {aj(s)}² = (½)² + 0 + (½)² = ½  (× 1/Δt²)", "label", I["primary"]))
    o.append(label(s, 58, 38, f"Var = σ² Σ {aj(s)}² = σ²/(2Δt²)", "label", I["primary"]))
    B = LP(s, (58, 246, 388, 350), (0.002, 0.025), (0.08, 4), xlog=True, ylog=True)
    o.append(B.axes([(0.0025, "2.5"), (0.005, "5"), (0.01, "10"), (0.02, "20")], [(0.2, "0.2"), (0.5, "0.5"), (1, "1"), (2, "2")],
                    "sampling interval Δt (ms)", "noise sd (rad/s)", grid=(0.2, 0.5, 1, 2), ytx=14))
    o.append(B.curve(dts, [sd(d) for d in dts], RED))
    o.append(dots(B, dd, sim, I["primary"], 3))
    o.append(leg(s, 58, 226, [(RED, "σ/(√2 Δt)", None)], "simulated, σ = 0.006 rad", gap=14))
    o.append(label(s, B.X(0.02) - 6, B.Y(sd(0.02)) + 20, f"{sd(0.02):.2f} at 20 ms", "label2", I["primary"], "end"))
    o.append(label(s, B.X(0.0025) + 10, B.Y(sd(0.0025)) - 9, f"{sd(0.0025):.2f} at 2.5 ms", "label2", I["primary"]))
    hv = [(A.box, [[round(A.X(x), 1), round(A.Y(w), 1), t] for x, w, t in ((1, -0.5, "weight of q(k−1): −1/(2Δt)"), (2, 0, "weight of q(k): 0"), (3, 0.5, "weight of q(k+1): +1/(2Δt)"))]),
          (B.box, hov(B, dts, [[sd(d) for d in dts]], lambda i: f"Δt = {1000 * dts[i]:.2f} ms: sd {sd(dts[i]):.3f} rad/s"))]
    aria = ("Problem D2 plot, two panels. Top: the weights of the central difference as red stems: minus one over two delta t at sample k minus 1, "
            "zero at k, plus one over two delta t at k plus 1; their squares sum to one half over delta t squared. Bottom: the velocity noise "
            f"standard deviation sigma over root two delta t against the sampling interval from 2.5 to 20 milliseconds on log axes, falling "
            f"from {sd(0.0025):.2f} to {sd(0.02):.2f} radians per second, with simulated black dots on the curve.")
    return fin(VB, aria, s, o, hv)


def fig35():
    VB = (0, 0, W, 418)
    s = H.Scale(W, VB[3], display_w=400)
    dts = np.geomspace(0.0025, 0.020, 40)
    sdv = lambda dt: SIG / (math.sqrt(2) * dt)                                          # noqa: E731
    sda = lambda dt: SIG * math.sqrt(6) / dt ** 2                                       # noqa: E731
    dd = (0.0025, 0.005, 0.01, 0.02)
    sim_a, sim_v = stencil_sim(2, dd), stencil_sim(1, dd)
    assert all(abs(a / sda(d) - 1) < 0.01 for a, d in zip(sim_a, dd))
    assert abs(sda(0.0025) / sda(0.02) - 64) < 1e-9 and abs(sdv(0.0025) / sdv(0.02) - 8) < 1e-9
    A = LP(s, (58, 60, 388, 168), (0, 4), (-3.4, 1.9))
    o = [A.axes([(1, "k−1"), (2, "k"), (3, "k+1")], [(-2, "−2"), (0, "0"), (1, "+1")], "", "weight (× 1/Δt²)", grid=(-2, 0, 1), ytx=14)]
    o += stems(A, s, (1, 2, 3), (1, -2, 1), ("+1/Δt²", "−2/Δt²", "+1/Δt²"))
    o.append(label(s, 58, 18, f"Σ {aj(s)}² = 1 + 4 + 1 = 6  (× 1/Δt⁴)", "label", I["primary"]))
    o.append(label(s, 58, 38, f"Var = σ² Σ {aj(s)}² = 6σ²/Δt⁴", "label", I["primary"]))
    B = LP(s, (58, 246, 388, 350), (0.002, 0.025), (0.6, 200), xlog=True, ylog=True)
    rel = lambda f, dt: f(dt) / f(0.02)                                                  # noqa: E731
    o.append(B.axes([(0.0025, "2.5"), (0.005, "5"), (0.01, "10"), (0.02, "20")], [(1, "1"), (10, "10"), (100, "100")],
                    "sampling interval Δt (ms)", "noise sd ratio", grid=(10,), ytx=14))
    o.append(B.curve(dts, [rel(sda, d) for d in dts], RED))
    o.append(B.curve(dts, [rel(sdv, d) for d in dts], BLUE))
    o.append(dots(B, dd, [a / sim_a[-1] for a in sim_a], I["primary"], 3))
    o.append(dots(B, dd, [a / sim_v[-1] for a in sim_v], I["primary"], 3))
    o.append(leg(s, 58, 226, [(RED, "acceleration", None), (BLUE, "velocity", None)], "simulated", gap=12))
    o.append(label(s, B.X(0.0025) + 10, B.Y(64) - 9, "×64 at 2.5 ms", "label2", I["primary"]))
    o.append(label(s, B.X(0.0025) + 10, B.Y(8) + 30, "×8 at 2.5 ms", "label2", I["primary"]))
    o.append(label(s, 58, 408, "ratio of the noise sd to its value at Δt = 20 ms", "label2", I["secondary"]))
    hv = [(A.box, [[round(A.X(x), 1), round(A.Y(w), 1), t] for x, w, t in ((1, 1, "weight of q(k−1): +1/Δt²"), (2, -2, "weight of q(k): −2/Δt²"), (3, 1, "weight of q(k+1): +1/Δt²"))]),
          (B.box, hov(B, dts, [[rel(sda, d) for d in dts], [rel(sdv, d) for d in dts]],
                      lambda i: f"Δt = {1000 * dts[i]:.2f} ms: acceleration noise ×{rel(sda, dts[i]):.1f}, velocity noise ×{rel(sdv, dts[i]):.1f}"))]
    aria = ("Problem D3 plot, two panels. Top: the weights of the second difference as red stems: plus 1 over delta t squared at samples k minus 1 and "
            "k plus 1 and minus 2 over delta t squared at k; their squares sum to 6 over delta t to the fourth. Bottom: the noise standard deviation "
            "relative to its value at 20 milliseconds, against the sampling interval from 2.5 to 20 milliseconds on log axes. The red acceleration noise "
            "grows 64 times, the blue velocity noise 8 times, with simulated black dots on the curves.")
    return fin(VB, aria, s, o, hv)


# ================================================================ svg #42 D10: least squares
def fig42():
    VB = (0, 0, W, 474)
    s = H.Scale(W, VB[3], display_w=400)
    t, a_true, fy, a_kin = lab_d_data()
    y, Acol = a_kin + G, fy                                                              # y = A beta with beta = 1/M
    bh = float(Acol @ y / (Acol @ Acol))                                                 # normal equation
    ms = np.linspace(60, 80, 801)
    grid_best = ms[int(np.argmin([np.sqrt(np.mean((a_kin - (fy / m - G)) ** 2)) for m in ms]))]
    assert abs(1 / bh - grid_best) < 0.03 and abs(1 / bh - 70) < 0.5, (1 / bh, grid_best)
    e = y - Acol * bh
    assert abs(Acol @ e) < 1e-6 * np.abs(Acol).sum()                                    # A^T r = 0
    betas = np.linspace(1 / 80, 1 / 63, 121)
    R = np.array([np.mean((y - Acol * b) ** 2) for b in betas])
    xb = betas * 1e3
    A = LP(s, (58, 84, 388, 212), (xb[0], xb[-1]), (0, 1.7))
    o = [A.axes([(v, f"{v:g}") for v in (13, 14, 15)], [(0, "0"), (0.5, "0.5"), (1, "1"), (1.5, "1.5")],
                "β (10⁻³ kg⁻¹)", "R(β) ((m/s²)²)", grid=(0.5, 1, 1.5), ytx=14)]
    o.append(vline(A, bh * 1e3))
    o.append(A.curve(xb, R, RED))
    o.append(mark(A, bh * 1e3, float(np.mean(e ** 2))))
    o.append(label(s, 58, 18, "β = 1/M,  y = a + g,  A = F" + sub("y", s) + " ,  y = Aβ", "label2", I["secondary"]))
    o.append(label(s, 58, 40, "∇R = 0  gives  A" + sup("T", s) + "A " + hat("β", s) + " = A" + sup("T", s) + "y", "label", I["primary"]))
    o.append(label(s, 58, 62, hat("β", s) + f" = {bh * 1e3:.2f} × 10⁻³ kg⁻¹, so " + hat("M", s) + f" = {1 / bh:.2f} kg", "label", I["primary"]))
    B = LP(s, (58, 322, 388, 420), (float(Acol.min()) - 20, float(Acol.max()) + 20), (-0.6, 0.6))
    o.append(B.axes([(v, str(v)) for v in (600, 700, 800)], [(-0.5, "−0.5"), (0, "0"), (0.5, "0.5")], "plate force A = F" + sub("y", s) + " (N)",
                    "residual (m/s²)", grid=(-0.5, 0, 0.5), ytx=14))
    o.append(H.line(s, B.x0, B.Y(0), B.x1, B.Y(0), O["dim"], "ref", H.DASH_REF))
    o.append(dots(B, Acol, e, ORANGE, 2.4))
    o.append(label(s, 58, 288, "residual y − A" + hat("β", s) + " against A, 200 frames:", "label2", I["primary"]))
    o.append(label(s, 58, 306, f"A{sup('T', s)}(y − A" + hat("β", s) + f") = {float(Acol @ e):.0e} ≈ 0, no trend", "label2", I["secondary"]))
    order = np.argsort(Acol)
    hv = [(A.box, hov(A, xb, [R], lambda i: f"β = {xb[i]:.2f}e-3 /kg (M = {1 / betas[i]:.1f} kg): R = {R[i]:.3f}")),
          (B.box, [[round(B.X(Acol[k]), 1), round(B.Y(e[k]), 1), f"A = {Acol[k]:.0f} N: residual {mn(e[k])} m/s²"] for k in order])]
    aria = ("Problem D10 plot, two panels, from the Lab D squat data with beta equal to one over the body mass. Top: the mean squared residual R of beta, a "
            f"red parabola with its minimum at beta hat {bh * 1e3:.2f} times ten to the minus three per kilogram, a mass of {1 / bh:.2f} kilograms. Bottom: "
            "the residuals at that minimum, orange dots against the plate force, scatter evenly about zero with no trend, so the residual is orthogonal to A.")
    return fin(VB, aria, s, o, hv)


# ================================================================ svg #43 K1: raw versus filtered, across sampling rates
@lru_cache(None)
def k1_data():
    fss = list(range(50, 401, 10))
    raw, filt = [], []
    for fs in fss:
        dt = 1.0 / fs
        t = np.arange(0, 2, dt)
        q_true = 0.40 * np.sin(2 * np.pi * 0.8 * t)
        qdd_true = -0.40 * (2 * np.pi * 0.8) ** 2 * np.sin(2 * np.pi * 0.8 * t)
        raw.append(SIG * math.sqrt(6) / (4 * dt ** 2))
        b, a = butter(2, 7.0 / (fs / 2))
        rng = np.random.default_rng(15)
        err = []
        for _ in range(60):
            qf = filtfilt(b, a, q_true + rng.normal(0, SIG, t.size))
            n = int(0.1 * fs)
            err.append(np.mean((np.gradient(np.gradient(qf, dt), dt)[n:-n] - qdd_true[n:-n]) ** 2))
        filt.append(float(np.sqrt(np.mean(err))))
    return fss, np.array(raw), np.array(filt)


def fig43():
    VB = (0, 0, W, 330)
    s = H.Scale(W, VB[3], display_w=400)
    fss, raw, filt = k1_data()
    at = lambda f, arr: float(arr[fss.index(f)])                                         # noqa: E731
    assert [round(at(50, raw), 1), round(at(400, raw))] == [9.2, 588], (at(50, raw), at(400, raw))   # line 808
    assert [round(at(f, filt), 2) for f in (50, 100, 200, 400)] == [2.04, 1.97, 1.56, 1.13], [at(f, filt) for f in (50, 100, 200, 400)]
    assert round(at(50, raw) / at(50, filt)) == 5 and round(at(400, raw) / at(400, filt)) == 519
    pk = float(np.abs(QDD_TRUE).max())
    P = LP(s, (58, 60, 388, 248), (50, 400), (0.4, 1500), ylog=True)
    o = [P.axes([(v, str(v)) for v in (50, 100, 200, 300, 400)], [(1, "1"), (10, "10"), (100, "100"), (1000, "1000")], "sampling rate (Hz)",
                "error (rad/s²)", grid=(1, 10, 100, 1000), ytx=14)]
    o.append(hline(P, pk, I["primary"]))
    o.append(P.curve(fss, raw, ORANGE))
    o.append(P.curve(fss, filt, BLUE))
    for f in (50, 100, 200, 400):
        o.append(mark(P, f, at(f, raw), ORANGE, True))
        o.append(mark(P, f, at(f, filt), BLUE, True))
    o.append(label(s, P.X(50) + 8, P.Y(at(50, raw)) + 18, f"{at(50, raw):.1f}", "label2", I["primary"]))
    o.append(label(s, P.X(400) - 8, P.Y(at(400, raw)) + 20, f"{at(400, raw):.0f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(50) + 8, P.Y(at(50, filt)) + 18, f"{at(50, filt):.2f}", "label2", I["primary"]))
    o.append(label(s, P.X(400) - 8, P.Y(at(400, filt)) + 18, f"{at(400, filt):.2f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(400) - 6, P.Y(pk) - 7, f"true acceleration peak {pk:.1f}", "label2", I["primary"], "end"))
    o.append(label(s, P.x0 + 10, P.Y(500), "raw: ×64 from 50 to 400 Hz", "label2", I["secondary"]))
    o.append(label(s, P.X(150), P.Y(2.9), "filtered at 7 Hz: falls", "label2", I["secondary"]))
    o.append(leg(s, 58, 18, [(ORANGE, "raw np.gradient twice, sd", None)], None))
    o.append(leg(s, 58, 36, [(BLUE, "filtered at 7 Hz, RMSE", None)], None))
    o.append(label(s, 58, 322, f"raw ÷ filtered: {at(50, raw) / at(50, filt):.0f}× at 50 Hz, {at(400, raw) / at(400, filt):.0f}× at 400 Hz", "label2", I["secondary"]))
    hv = hov(P, fss, [raw, filt], lambda i: f"fs = {fss[i]} Hz: raw sd {raw[i]:.1f}, filtered RMSE {filt[i]:.2f} rad/s²")
    aria = ("Problem K1 plot: acceleration error against sampling rate from 50 to 400 hertz on a log axis. The orange raw np.gradient estimate rises "
            f"from {at(50, raw):.1f} to {at(400, raw):.0f} radians per second squared, a factor of 64; the blue estimate filtered at 7 hertz falls "
            f"from {at(50, filt):.2f} to {at(400, filt):.2f}. A dashed line marks the true acceleration peak of {pk:.1f}.")
    return fin(VB, aria, s, o, [(P.box, hv)])


# ================================================================ svg #45 K2: the cutoff two ways
@lru_cache(None)
def k2_data():
    """The K2 listing, line for line (vectorised draws, same stream)."""
    qd_true = A0 * (2 * np.pi * F0) * np.cos(2 * np.pi * F0 * TT)
    fine = np.geomspace(1.2, 45, 60)
    bias, noise = [], []
    for fc in fine:
        bias.append(np.sqrt(np.mean((np.gradient(smooth(Q_TRUE, fc), DT)[TRIM] - qd_true[TRIM]) ** 2)))
        rng = np.random.default_rng(9)
        nz = rng.normal(0, SIG, (200, TT.size))
        noise.append(np.sqrt(np.mean(np.gradient(smooth(nz, fc), DT, axis=-1)[:, TRIM] ** 2)))
    return fine, np.array(bias), np.array(noise)


def fig45():
    VB = (0, 0, W, 450)
    s = H.Scale(W, VB[3], display_w=400)
    fine, bias, noise = k2_data()
    tot = np.hypot(bias, noise)
    j = int(tot.argmin())
    cur, knees = lab_a()
    med, p5, p95 = float(np.median(knees)), *np.percentile(knees, [5, 95])
    mean = cur.mean(0)
    assert abs(fine[j] - 3.02) < 0.01 and abs(tot[j] - 0.0205) < 0.0005 and abs(bias[j] - 0.0132) < 0.0005 and abs(noise[j] - 0.0156) < 0.0005
    assert abs(med - 3.1) < 0.1 and abs(p5 - 2.8) < 0.1 and abs(p95 - 3.8) < 0.1
    xr = (1.2, 45)
    xt = [(v, str(v)) for v in (2, 5, 10, 20, 40)]
    A = LP(s, (58, 56, 388, 200), xr, (0, 0.45), xlog=True)
    B = LP(s, (58, 268, 388, 398), xr, (0, 0.06), xlog=True)
    o = [f'<rect x="{A.X(p5):.2f}" y="{A.y1:.2f}" width="{A.X(p95) - A.X(p5):.2f}" height="{A.y0 - A.y1:.2f}" fill="{BLUE}" opacity="0.14"/>',
         f'<rect x="{B.X(p5):.2f}" y="{B.y1:.2f}" width="{B.X(p95) - B.X(p5):.2f}" height="{B.y0 - B.y1:.2f}" fill="{BLUE}" opacity="0.14"/>']
    o.append(A.axes(xt, [(0, "0"), (0.15, "0.15"), (0.30, "0.30"), (0.45, "0.45")], "", "RMSE (rad/s)", grid=(0.15, 0.30, 0.45), ytx=14))
    o.append(B.axes(xt, [(0, "0"), (0.02, "0.02"), (0.04, "0.04"), (0.06, "0.06")], "filter cutoff f (Hz)", "residual (rad)",
                    grid=(0.02, 0.04, 0.06), ytx=14))
    o[-1] = o[-1].replace(">filter cutoff f (Hz)<", f">filter cutoff f{sub('c', s)} (Hz)<")
    o.append(vline(A, fine[j]))
    o.append(vline(B, fine[j]))
    o.append(A.curve(fine, tot, RED))
    o.append(B.curve(LAB_FCS, mean, RED))
    o.append(mark(A, fine[j], tot[j]))
    o.append(mark(B, med, float(np.interp(med, LAB_FCS, mean))))
    o.append(label(s, A.X(fine[j]) + 12, A.Y(0.40), "truth-driven optimum", "label2", I["primary"]))
    o.append(label(s, A.X(fine[j]) + 12, A.Y(0.40) + 16, f"{fine[j]:.2f} Hz, {tot[j]:.4f} rad/s", "label2", I["primary"]))
    o.append(label(s, A.X(fine[j]) + 12, A.Y(0.40) + 32, f"bias {bias[j]:.4f}, noise {noise[j]:.4f}", "label2", I["primary"]))
    o.append(label(s, B.X(p95) + 8, B.Y(0.049), "data-driven knee", "label2", I["primary"]))
    o.append(label(s, B.X(p95) + 8, B.Y(0.049) + 16, f"median {med:.1f} Hz", "label2", I["primary"]))
    o.append(label(s, B.X(p95) + 8, B.Y(0.049) + 32, f"5–95%: {p5:.1f} to {p95:.1f} Hz", "label2", I["primary"]))
    o.append(label(s, 58, 42, "(a) total RMS velocity error, uses the truth", "label2", I["primary"]))
    o.append(label(s, 58, 254, "(b) residual of the measured angle, no truth", "label2", I["primary"]))
    o.append(f'<rect x="{58}" y="{7}" width="22" height="10" fill="{BLUE}" opacity="0.25"/>')
    o.append(label(s, 58 + 28, 16, "5–95% range of the knee, 200 draws", "label2", I["secondary"]))
    hv = [(A.box, hov(A, fine, [tot], lambda i: f"fc = {fine[i]:.2f} Hz: velocity RMSE {tot[i]:.4f} rad/s (bias {bias[i]:.4f}, noise {noise[i]:.4f})")),
          (B.box, hov(B, LAB_FCS, [mean], lambda i: f"fc = {LAB_FCS[i]:.2f} Hz: residual {mean[i]:.4f} rad"))]
    aria = ("Problem K2 plot, two panels on one log cutoff axis from 1.2 to 45 hertz. Top: the red RMS velocity error, found with the true signal, is "
            f"U-shaped with a minimum of {tot[j]:.4f} rad per second at {fine[j]:.2f} hertz. Bottom: the red residual of the measured angle, found without "
            f"the truth, is flat at high cutoff and climbs below about 3 hertz; its knee has a median of {med:.1f} hertz. A blue band marks the 5 to 95 "
            f"percent range of the knee, {p5:.1f} to {p95:.1f} hertz, and a dashed line marks {fine[j]:.2f} hertz in both panels.")
    return fin(VB, aria, s, o, hv)


# ================================================================ svg #47 K3: three cutoffs for the torque
@lru_cache(None)
def k3_data():
    qm = Q_TRUE + np.random.default_rng(15).normal(0, SIG, TT.size)
    return {fc: pipeline(qm, fc) for fc in (1.5, 3.4, 20.0)}


def fig47():
    VB = (0, 0, W, 352)
    s = H.Scale(W, VB[3], display_w=400)
    tr = k3_data()
    errs = lab_b()
    e = {fc: float(np.interp(fc, LAB_FCS, errs)) for fc in (1.5, 20.0)}
    j = int(errs.argmin())
    e[3.4] = float(errs[j])
    assert abs(LAB_FCS[j] - 3.4) < 0.1 and abs(e[3.4] - 0.022) < 0.002 and abs(e[1.5] - 0.23) < 0.01 and abs(e[20.0] - 0.74) < 0.01, e   # lines 882, 626
    sel = (TT >= 0.1) & (TT <= 1.35)
    t = TT[sel]
    P = LP(s, (58, 68, 388, 264), (0.1, 1.35), (-5.2, 5.2))
    o = [P.axes([(v, f"{v:g}") for v in (0.25, 0.5, 0.75, 1.0, 1.25)], [(-4, "−4"), (-2, "−2"), (0, "0"), (2, "2"), (4, "4")], "time (s)",
                "torque (N m)", grid=(-4, -2, 0, 2, 4), ytx=14)]
    o.append(P.curve(t, tr[20.0][sel], ORANGE, multi=True))
    o.append(P.curve(t, tr[1.5][sel], BLUE))
    o.append(P.curve(t, TAU_TRUE[sel], RED, multi=True, dash=(7, 4)))
    o.append(P.curve(t, tr[3.4][sel], I["primary"], multi=True))
    o.append(leg(s, 58, 18, [(RED, "true", (7, 4)), (I["primary"], f"3.4 Hz, {e[3.4]:.3f}", None)], gap=12))
    o.append(leg(s, 58, 38, [(BLUE, f"1.5 Hz, {e[1.5]:.2f}", None), (ORANGE, f"20 Hz, {e[20.0]:.2f}", None)], gap=12))
    o.append(label(s, 58, 324, "RMSE in N m over 300 draws; curves: one trial", "label2", I["secondary"]))
    o.append(label(s, 58, 340, f"true peak {float(np.abs(TAU_TRUE).max()):.2f} N m; 1.5 Hz curve peaks at {float(np.abs(tr[1.5][sel]).max()):.2f}", "label2", I["secondary"]))
    hv = hov(P, t, [TAU_TRUE[sel], tr[1.5][sel], tr[3.4][sel], tr[20.0][sel]],
             lambda i: f"t = {t[i]:.2f} s: true {mn(TAU_TRUE[sel][i])}, 1.5 Hz {mn(tr[1.5][sel][i])}, 3.4 Hz {mn(tr[3.4][sel][i])}, 20 Hz {mn(tr[20.0][sel][i])} N m")
    aria = ("Problem K3 plot: the recovered joint torque over one 1.25 second cycle for one trial, at three cutoffs, against the red dashed true torque "
            "that peaks at 3.31 newton metres. The blue 1.5 hertz curve is a smooth, shrunken copy; the black 3.4 hertz curve lies on the truth; the orange "
            "20 hertz curve straddles it inside a high-frequency fringe. Their RMS errors pooled over 300 draws are "
            f"{e[1.5]:.2f}, {e[3.4]:.3f} and {e[20.0]:.2f} newton metres.")
    return fin(VB, aria, s, o, [(P.box, hv)])


# ================================================================ svg #49 K5: reading the dynamic residual
SIG_Y, FC_OK, FC_BAD = 0.0004, 6.0, 15.0


@lru_cache(None)
def k5_data():
    """Lab D squat (seed 15). Camera COM height with 0.4 mm noise, smoothed, differentiated twice; plate noise 2.5 N."""
    t = np.arange(0, 2, DT)
    y_true = 0.175 * np.cos(np.pi * t)                       # its second derivative is Lab D's a_true
    a_true = -0.35 * np.pi ** 2 * np.cos(np.pi * t) / 2.0
    assert np.allclose(np.gradient(np.gradient(y_true, DT), DT)[2:-2], a_true[2:-2], atol=0.02)
    rng = np.random.default_rng(15)
    fy = 70.0 * (G + a_true) + rng.normal(0, 2.5, t.size)
    ym = y_true + rng.normal(0, SIG_Y, t.size)

    def a_kin(fc):
        return np.gradient(np.gradient(smooth(ym, fc), DT), DT)
    plate = lambda m: fy / m - G                             # noqa: E731
    return dict(t=t, a_true=a_true, mass=a_kin(FC_OK) - plate(70.0 * 1.15), jit=a_kin(FC_BAD) - plate(70.0),
                ok=a_kin(FC_OK) - plate(70.0))


def fig49():
    VB = (0, 0, W, 508)
    s = H.Scale(W, VB[3], display_w=400)
    d = k5_data()
    sl = TRIM
    t = d["t"][sl]
    m, jt, ok = d["mass"][sl], d["jit"][sl], d["ok"][sl]
    off = G * (1 - 70.0 / 80.5)
    assert abs(m.mean() - off) < 0.1 and np.corrcoef(m, d["a_true"][sl])[0, 1] > 0.5       # offset 0.13 g, tracks the force
    P = LP(s, (58, 62, 388, 202), (0, 2), (-1.5, 2.0))
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)], [(-1, "−1"), (0, "0"), (1, "1"), (2, "2")], "time (s)",
                "residual (m/s²)", grid=(-1, 1, 2), ytx=14)]
    o.append(H.line(s, P.x0, P.Y(0), P.x1, P.Y(0), O["dim"], "ref", H.DASH_REF))
    o.append(P.curve(t, jt, ORANGE))
    o.append(P.curve(t, ok, I["primary"]))
    o.append(P.curve(t, m, RED, multi=True))
    o.append(leg(s, 58, 18, [(RED, "15% mass error", None), (ORANGE, f"{FC_BAD:.0f} Hz filter", None)], gap=12))
    o.append(leg(s, 58, 38, [(I["primary"], f"no fault, {FC_OK:.0f} Hz filter: sd {float(ok.std()):.2f}", None)], gap=12))
    fr = np.fft.rfftfreq(m.size, DT)

    def spec(x):
        return 2 * np.abs(np.fft.rfft(x)) / x.size
    sm, sj = spec(m), spec(jt)
    keep = (fr >= 0.5) & (fr <= 50)
    B = LP(s, (58, 312, 388, 440), (0.5, 50), (0.0005, 3), xlog=True, ylog=True)
    sm, sj = np.maximum(sm, 6e-4), np.maximum(sj, 6e-4)
    o.append(B.axes([(v, str(v)) for v in (1, 2, 5, 10, 20, 50)], [(0.001, "10" + sup("−3", s)), (0.01, "0.01"), (0.1, "0.1"), (1, "1")],
                    "frequency (Hz)", "amplitude (m/s²)", grid=(0.01, 0.1, 1), ytx=14))
    o.append(B.curve(fr[keep], sj[keep], ORANGE))
    o.append(B.curve(fr[keep], sm[keep], RED, multi=True))
    o.append(label(s, 58, 290, "amplitude spectra of the two residuals", "label2", I["primary"]))
    o.append(label(s, 58, 500, f"mass error: mean {m.mean():.2f} = 0.13 g; jitter sd {float(jt.std()):.2f} m/s²", "label2", I["secondary"]))
    hv = [(P.box, hov(P, t, [m, jt, ok], lambda i: f"t = {t[i]:.2f} s: mass error {mn(m[i])}, 15 Hz filter {mn(jt[i])}, no fault {mn(ok[i])} m/s²")),
          (B.box, hov(B, fr[keep], [sm[keep], sj[keep]], lambda i: f"{fr[keep][i]:.1f} Hz: mass error {sm[keep][i]:.3f}, jitter {sj[keep][i]:.3f} m/s²"))]
    aria = ("Problem K5 plot, two panels, for the Lab D squat. Top: the dynamic residual over two seconds under two faults. With the assumed mass 15 percent too "
            f"high the red residual is a smooth curve near {m.mean():.2f} metres per second squared that follows the plate force; with the angle under-smoothed at "
            f"{FC_BAD:.0f} hertz the orange residual is a high-frequency jitter about zero; the black no-fault residual stays near zero. Bottom: the amplitude "
            "spectra of the two faults on log axes: the mass error sits at low frequency and falls steeply, the jitter is broadband.")
    return fin(VB, aria, s, o, hv)


# ================================================================ svg #51 K7: the error budget
@lru_cache(None)
def k7_data():
    """The K7 listing (lines 900-940): 20 000 draws, one source at a time, pooled."""
    N, U = 20000, 0.15
    tau_true = IZ * QDD_TRUE + MZ * G * LL * np.sin(Q_TRUE)

    def torque(qf, iz=IZ, m=MZ):
        qdd = np.gradient(np.gradient(qf, DT, axis=-1), DT, axis=-1)
        return iz * qdd + m * G * LL * np.sin(qf)

    def pooled(err):
        return float(np.sqrt(np.mean(err[..., TRIM] ** 2)))
    qf6 = smooth(Q_TRUE, 6.0)
    eps = np.random.default_rng(9).normal(0, U, (N, 2))
    e_bsp = torque(qf6, IZ * (1 + eps[:, 0:1]), MZ * (1 + eps[:, 1:2])) - tau_true
    qm = Q_TRUE + np.random.default_rng(21).normal(0, SIG, (N, TT.size))
    e_mrk = torque(smooth(qm, 6.0)) - tau_true
    return dict(bsp=pooled(e_bsp), mrk=pooled(e_mrk), cut=pooled(torque(smooth(Q_TRUE, 1.5)) - tau_true),
                bias=pooled(torque(smooth(Q_TRUE, 6.0)) - tau_true),
                per=float(np.sqrt(np.mean(e_bsp[:, TRIM] ** 2, axis=1)).mean()))


def fig51():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    d = k7_data()
    assert [round(d[k], 3) for k in ("bsp", "cut", "mrk", "bias")] == [0.414, 0.228, 0.059, 0.004], d      # line 898
    assert round(d["per"], 2) == 0.33 and abs(d["per"] / d["bsp"] - math.sqrt(2 / math.pi)) < 0.01
    rows = [("15% body-segment", "parameters", d["bsp"]), ("cutoff 1.5 Hz", "instead of 6 Hz", d["cut"]),
            ("marker noise", "σ = 0.006 rad", d["mrk"]), ("filter bias", "at 6 Hz", d["bias"])]
    P = LP(s, (140, 36, 388, 190), (0, 0.5), (0, 4))
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5)], [], "pooled RMS torque error (N m)", "", grid=())]
    for v in (0.1, 0.2, 0.3, 0.4, 0.5):
        o.append(H.line(s, P.X(v), P.y1, P.X(v), P.y0, GRID, "leader"))
    o.append(H.line(s, P.x0, P.y1, P.x0, P.y0, I["axis"], "axis"))
    for k, (a, b, v) in enumerate(rows):
        yc = P.y1 + (k + 0.5) * (P.y0 - P.y1) / 4
        h = 26.0
        o.append(f'<rect x="{P.x0:.2f}" y="{yc - h / 2:.2f}" width="{P.X(v) - P.x0:.2f}" height="{h}" fill="{BLUE}"/>')
        o.append(label(s, P.x0 - 8, yc - 1, a, "label2", I["primary"], "end"))
        o.append(label(s, P.x0 - 8, yc + 14, b, "label2", I["secondary"], "end"))
        o.append(label(s, P.X(v) + 6, yc + 5, f"{v:.3f}", "label", I["primary"]))
    yc0 = P.y1 + 0.5 * (P.y0 - P.y1) / 4
    o.append(f'<line x1="{P.X(d["per"]):.2f}" y1="{yc0 - 13:.2f}" x2="{P.X(d["per"]):.2f}" y2="{yc0 + 13:.2f}" stroke="#fff" stroke-width="{s(2.5):.2f}"/>')
    o.append(label(s, 140, 18, "20 000 draws, one source active at a time", "label2", I["secondary"]))
    o.append(label(s, 58, 250, f"white tick {d['per']:.2f}: mean of per-draw RMSE", "label2", I["secondary"]))
    aria = ("Problem K7 plot: horizontal bars of the pooled RMS torque error from each source alone, over 20 000 draws: 15 percent body-segment "
            "parameters 0.414 newton metres, a 1.5 hertz cutoff instead of 6 hertz 0.228, marker noise 0.059, and the filter's own bias at 6 hertz 0.004. "
            "A white tick on the first bar marks 0.33, the mean of the per-draw RMS errors, which is root two over pi times the pooled value.")
    px = sorted([[round(P.X(v), 1), round(P.Y(2), 1), f"{a} {b}: {v:.3f} N m"] for a, b, v in rows], key=lambda q: q[0])
    return fin(VB, aria, s, o, [(P.box, px)])


# ================================================================ svg #54 K9: the noise-versus-parameter crossover
@lru_cache(None)
def k9_data():
    """The K9 listing (lines 956-1000): operating point at 20 000 draws, 40-point sweeps at 2000 draws."""
    tau_true = IZ * QDD_TRUE + MZ * G * LL * np.sin(Q_TRUE)
    b, a = butter(2, 6.0 / (100.0 / 2))
    qf = filtfilt(b, a, Q_TRUE)

    def torque(qs, iz=IZ, m=MZ):
        qdd = np.gradient(np.gradient(qs, DT, axis=-1), DT, axis=-1)
        return iz * qdd + m * G * LL * np.sin(qs)

    def pooled(err):
        return float(np.sqrt(np.mean(err[..., TRIM] ** 2)))

    def marker(sig, n, seed=21):
        qm = Q_TRUE + np.random.default_rng(seed).normal(0, sig, (n, TT.size))
        return pooled(torque(filtfilt(b, a, qm, axis=-1)) - tau_true)

    def bsp(u, n, seed=9):
        e = np.random.default_rng(seed).normal(0, u, (n, 2))
        return pooled(torque(qf, IZ * (1 + e[:, 0:1]), MZ * (1 + e[:, 1:2])) - tau_true)
    ref_mk, ref_bs = marker(0.006, 20000), bsp(0.15, 20000)
    sigs, us = np.geomspace(0.001, 0.20, 40), np.geomspace(0.005, 0.60, 40)
    mk = np.array([marker(x, 2000) for x in sigs])
    bs = np.array([bsp(u, 2000) for u in us])
    return ref_mk, ref_bs, sigs, mk, us, bs, float(np.interp(ref_bs, mk, sigs)), float(np.interp(ref_mk, bs, us))


def fig54():
    VB = (0, 0, W, 470)
    s = H.Scale(W, VB[3], display_w=400)
    ref_mk, ref_bs, sigs, mk, us, bs, sstar, ustar = k9_data()
    assert abs(sstar - 0.042) < 0.001 and abs(100 * ustar - 2.1) < 0.1 and abs(ref_bs / ref_mk - 7.0) < 0.1, (sstar, ustar, ref_mk, ref_bs)   # line 952
    A = LP(s, (62, 50, 388, 184), (0.001, 0.2), (0.005, 3), xlog=True, ylog=True)
    B = LP(s, (62, 276, 388, 402), (0.5, 60), (0.01, 3), xlog=True, ylog=True)
    o = [A.axes([(0.001, "0.001"), (0.01, "0.01"), (0.1, "0.1")], [(0.01, "0.01"), (0.1, "0.1"), (1, "1")], "marker noise σ (rad)",
                "error (N m)", grid=(0.01, 0.1, 1), ytx=14),
         B.axes([(0.5, "0.5"), (1, "1"), (2, "2"), (5, "5"), (10, "10"), (20, "20"), (50, "50")], [(0.01, "0.01"), (0.1, "0.1"), (1, "1")],
                "BSP uncertainty u (%)", "error (N m)", grid=(0.01, 0.1, 1), ytx=14)]
    o.append(hline(A, ref_bs, RED))
    o.append(A.curve(sigs, mk, ORANGE))
    o.append(mark(A, sstar, ref_bs))
    o.append(mark(A, 0.006, ref_mk, I["primary"], True))
    o.append(label(s, A.X(sstar) - 10, A.Y(ref_bs) - 10, f"σ* = {sstar:.3f} rad = {math.degrees(sstar):.1f}°", "label2", I["primary"], "end"))
    o.append(label(s, A.X(0.006) + 10, A.Y(ref_mk) + 22, "working point 0.006", "label2", I["primary"]))
    o.append(leg(s, 62, 18, [(RED, "BSP error", None), (ORANGE, "marker error", None)], gap=14))
    o.append(label(s, 62, 38, "(a) σ varies; BSP fixed at u = 15%", "label2", I["secondary"]))
    o.append(hline(B, ref_mk, ORANGE))
    o.append(B.curve(100 * us, bs, RED))
    o.append(mark(B, 100 * ustar, ref_mk))
    o.append(mark(B, 15, ref_bs, I["primary"], True))
    o.append(label(s, B.X(100 * ustar) + 10, B.Y(ref_mk) + 20, f"u* = {100 * ustar:.1f}%", "label2", I["primary"]))
    o.append(label(s, B.X(15) - 10, B.Y(ref_bs) - 8, "working point 15%", "label2", I["primary"], "end"))
    o.append(label(s, 62, 264, "(b) u varies; markers fixed at 0.006 rad", "label2", I["secondary"]))
    o.append(label(s, 62, 462, f"working point: BSP {ref_bs:.3f}, markers {ref_mk:.3f} N m, ratio {ref_bs / ref_mk:.1f}", "label2", I["secondary"]))
    hv = [(A.box, hov(A, sigs, [mk], lambda i: f"σ = {sigs[i]:.4f} rad: marker torque error {mk[i]:.3f} N m (BSP at 15%: {ref_bs:.3f})")),
          (B.box, hov(B, 100 * us, [bs], lambda i: f"u = {100 * us[i]:.2f}%: BSP torque error {bs[i]:.3f} N m (marker at 0.006 rad: {ref_mk:.3f})"))]
    aria = ("Problem K9 plot, two panels on log axes. Top: torque error from marker noise, an orange line rising with the noise from 0.001 to 0.20 radian, "
            f"crosses the flat red 0.414 newton metre line from 15 percent body-segment parameters at sigma star {sstar:.3f} radian, {math.degrees(sstar):.1f} degrees; "
            "a hollow dot marks the working point 0.006 radian. Bottom: torque error from the parameters, a red line rising with the uncertainty from 0.5 to 60 percent, "
            f"falls to the flat orange {ref_mk:.3f} line of marker noise at u star {100 * ustar:.1f} percent; a hollow dot marks the working point 15 percent.")
    return fin(VB, aria, s, o, hv)


# ================================================================ svg #56 K10: spending a measurement budget
def fig56():
    VB = (0, 0, W, 316)
    s = H.Scale(W, VB[3], display_w=400)
    d = k7_data()
    a, b = k9_data()[0], k9_data()[1]                         # marker 0.059 and BSP 0.414 at the operating point (K9 listing)
    xo = a ** 2 / (a ** 2 + b ** 2)
    xs = np.unique(np.concatenate([np.geomspace(0.001, 1, 200), [xo]]))
    e_m, e_b = a * (1 - xs), b * xs                           # model: spend x on markers, 1-x on inertias; each reduction proportional
    tot = np.hypot(e_m, e_b)
    eo = math.hypot(a * (1 - xo), b * xo)
    assert abs(d["bsp"] - b) < 0.002 and abs(a - 0.059) < 0.001 and abs(b - 0.414) < 0.002, (a, b)
    assert abs(xs[int(tot.argmin())] - xo) < 1e-9
    P = LP(s, (58, 40, 388, 220), (0.001, 1), (0, 0.45), xlog=True)
    o = [P.axes([(0.001, "0.001"), (0.01, "0.01"), (0.1, "0.1"), (1, "1")], [(0, "0"), (0.15, "0.15"), (0.30, "0.30"), (0.45, "0.45")],
                "fraction of the budget spent on markers (log)", "error (N m)", grid=(0.15, 0.30, 0.45), ytx=14)]
    o.append(P.curve(xs, e_b, BLUE, multi=True, dash=(7, 4)))
    o.append(P.curve(xs, e_m, ORANGE, multi=True, dash=(7, 4)))
    o.append(P.curve(xs, tot, RED))
    o.append(mark(P, xo, eo))
    o.append(label(s, P.x0 + 10, P.Y(0.30), f"optimum: {100 * xo:.0f}% to markers", "label2", I["primary"]))
    o.append(label(s, P.x0 + 10, P.Y(0.30) + 16, f"error {eo:.3f}", "label2", I["primary"]))
    o.append(H.line(s, P.X(xo), P.Y(0.30) + 22, P.X(xo), P.Y(eo) - 7, I["rule"], "leader"))
    o.append(label(s, P.X(0.95), P.Y(b) - 8, f"all on markers: {b:.3f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.0012), P.Y(0.025), f"all on inertias: {a:.3f}", "label2", I["primary"]))
    o.append(leg(s, 58, 18, [(RED, "total", None), (BLUE, "parameter term", (7, 4)), (ORANGE, "marker term", (7, 4))], gap=10))
    o.append(label(s, 58, 280, "model: x to markers, 1 − x to inertias; each term", "label2", I["secondary"]))
    o.append(label(s, 58, 296, "falls in proportion to its spend (assumed)", "label2", I["secondary"]))
    o.append(label(s, 58, 312, f"start: markers {a:.3f}, parameters {b:.3f} N m", "label2", I["secondary"]))
    hv = hov(P, xs, [tot, e_b, e_m], lambda i: f"{100 * xs[i]:.2f}% on markers: total {tot[i]:.3f} (parameters {e_b[i]:.3f}, markers {e_m[i]:.3f}) N m")
    aria = ("Problem K10 plot: torque error against the fraction of a fixed budget spent on markers, on a log axis from 0.001 to 1, with the rest on "
            "subject-specific inertias, under the quadrature model with each term falling in proportion to its spend. The blue dashed parameter term rises "
            "to 0.414 newton metres and the orange dashed marker term falls from 0.059 to 0; the red total has its minimum of "
            f"{eo:.3f} at {100 * xo:.0f} percent to markers, against 0.059 with everything on inertias and 0.414 with everything on markers.")
    return fin(VB, aria, s, o, [(P.box, hv)])


FIGS = {
    25: ('C3: invisible noise, visible ruin. Position noise too small ', fig25),
    26: ('C4: faster is worse. Buying a faster camera (smaller $\\Delta', fig26),
    27: ('C5: not as smooth as possible. Why is there a best cutoff fr', fig27),
    34: ('D2: velocity noise. Derive the noise variance of the central', fig34),
    35: ('D3: acceleration noise. Derive the noise variance of the sec', fig35),
    36: ('D4: bias-variance. Show that the mean-square error of a smoo', fig36),
    42: ('D10: least squares. Derive the normal equations for the param', fig42),
    43: ('K1: raw versus filtered noise across sampling rates (sensiti', fig43),
    45: ('K2: finding the cutoff two ways (optimisation + inverse). On ', fig45),
    47: ('K3: three cutoffs for the torque (regime). Recover the joint ', fig47),
    49: ('K5: reading the dynamic residual (simulation + regime). Intr', fig49),
    51: ('K7: the error budget (sensitivity). The RMS torque error each', fig51),
    54: ('K9: the noise-versus-parameter crossover (sensitivity). Vary ', fig54),
    56: ('K10: spending a measurement budget (optimisation). Given a f', fig56),
}
