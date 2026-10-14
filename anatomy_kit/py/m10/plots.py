"""Module 10 plots (group `plots`): main text #5, #7, #8, #9, #12, #14 and the computed K plots #38-#52.

Every plotted number is computed here from the formula or the lab code module10.html states:
  #5   phase portraits of x' = A x (Prop. 1.1, 2.2): eigenlines +-w0, hyperbolas xi*eta = const, and the
       closed-loop spiral for kp = 20, kd = 3 (poles -1.5 +- 2.85 i, line 136);
  #7   Prop. 4.2 boundary (line 199) at kd = 3 and the delayed loop of line 185 integrated as in Lab B
       (semi-implicit Euler, history zero, theta(0) = 0.02) at tau = 100 ms, tau_c = 137.4 ms, 172 ms;
  #8   Prop. 5.1 (line 225), q = 2.2e-3 (line 234), Euler-Maruyama simulation (the trace seed and the dots);
  #9   Prop. 6.1 (line 247) and Lab C verbatim (lines 449-481);
  #12  Prop. 4.2 at kd = 3.0 and 1.7 (line 343), Def. 6 with Lab D's young and aged sets (lines 497-498),
       the lognormal of line 343 (median 18 N s, log-sd 0.5);
  #14, K1  Lab A verbatim (lines 358-393);  K2  Lab B verbatim (lines 404-430);  K3  its own code (lines 611-656);
  K4   its own code (lines 662-689);  K5  Lab C;  K6  its own code (lines 699-716);  K7  its own code (lines 722-742);
  K8   Def. 6 (lines 748-756);  K9  Lab D;  K10  Def. 6 and the K10 code (lines 766-776).
The printed solution numbers are asserted.
"""
import html
import math
from functools import lru_cache

import numpy as np

import house as H
from m05 import plots_main as PM
from m05.plots_prob import Plot, label, legend, text_w, hov, svg, sub

O, I, SER = H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"
BOX = "#f7f4ef"
W = 400                                     # problem figures: viewBox width = rendered width
mn = PM.mn

# ---------------------------------------------------------------- the standing adult (Appendix, lines 849-855)
G, M, ELL = 9.81, 70.0, 1.0
W0, KP, KD = 3.1, 20.0, 3.0                 # the text rounds w0 = sqrt(g/ell) to 3.1 (lines 106, 136, 358)
B_FOOT = 0.10
U_MAX = W0 * W0 * B_FOOT                    # Prop. 7.1 saturation (line 360)
Q0 = 2.2e-3                                 # noise intensity (line 234)
YOUNG = dict(tau=0.10, t_move=0.20, l_step=0.60)      # Lab D (lines 497-498)
AGED = dict(tau=0.18, t_move=0.32, l_step=0.42)


def j_crit(tau, t_move, l_step, w0=W0, m=M):
    """Def. 6 (line 337): largest recoverable impulse."""
    return m * w0 * l_step * math.exp(-w0 * (tau + t_move))


# ---------------------------------------------------------------- Prop. 4.2: the stability-island boundary
OM = np.geomspace(1e-3, 80.0, 30000)


def boundary(kd, w0=W0):
    """(tau, kp) on the Prop. 4.2 boundary, Omega from 1e-3 to 80: tau falls and kp rises with Omega."""
    s = kd * OM / (OM ** 2 + w0 ** 2)
    a = np.arcsin(s)
    return a / OM, (OM ** 2 + w0 ** 2) * np.cos(a)


def tau_crit(kp, kd, w0=W0):
    t, k = boundary(kd, w0)
    return float(np.interp(kp, k, t))


def kp_ceiling(tau, kd, w0=W0):
    t, k = boundary(kd, w0)
    return float(np.interp(tau, t[::-1], k[::-1]))


TC = tau_crit(KP, KD)
_OMC = float(np.interp(KP, boundary(KD)[1], OM))                  # crossing frequency at the design gains
assert round(1000 * TC) == 137 and round(_OMC, 1) == 3.6 and 28 <= math.degrees(_OMC * TC) <= 29   # lines 208-210


# ---------------------------------------------------------------- the delayed loop (line 185), Lab B's integrator
def dde(tau, kp=KP, kd=KD, th0=0.02, T=4.5, dt=0.0005):
    n, d = int(round(T / dt)), max(1, int(round(tau / dt)))
    th, om, a = [0.0] * (n + 1), [0.0] * (n + 1), W0 * W0
    th[0] = th0
    for i in range(n):
        if i - d >= 0:
            thd, omd = th[i - d], om[i - d]
        else:
            thd = omd = 0.0
        om[i + 1] = om[i] + dt * (a * th[i] - kp * thd - kd * omd)
        th[i + 1] = th[i] + dt * om[i + 1]
    return np.arange(n + 1) * dt, np.array(th)


# ---------------------------------------------------------------- Lab A (lines 358-393), arithmetic unchanged
def recover(J, tau, T=8.0, dt=0.002):
    n, d = int(T / dt), max(1, int(round(tau / dt)))
    th, om, a = [0.0] * (n + 1), [0.0] * (n + 1), W0 * W0
    om[0] = J / (M * ELL)
    for i in range(n):
        if i - d >= 0:
            thd, omd = th[i - d], om[i - d]
        else:
            thd = omd = 0.0
        u = -(KP * thd + KD * omd)
        u = U_MAX if u > U_MAX else (-U_MAX if u < -U_MAX else u)
        om[i + 1] = om[i] + dt * (a * th[i] + u)
        th[i + 1] = th[i] + dt * om[i + 1]
        if abs(th[i + 1]) > 0.35:
            return False
    return abs(th[-1]) < 0.02 and abs(om[-1]) < 0.05


def max_impulse(tau):
    lo, hi = 0.0, 40.0
    for _ in range(34):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if recover(mid, tau) else (lo, mid)
    return lo


@lru_cache(maxsize=None)
def lab_a():
    taus = sorted({0.001} | {round(0.005 * k, 4) for k in range(1, 39)} | {round(0.11 + 0.0025 * k, 4) for k in range(21)})
    jm = [max_impulse(t) for t in taus]
    pick = {t: j for t, j in zip(taus, jm)}
    assert round(m_bound(), 1) == 21.7 and round(pick[0.001], 1) == 21.6
    assert [round(pick[t], 1) for t in (0.05, 0.1, 0.15)] == [18.5, 15.5, 0.8]
    return np.array(taus), np.array(jm)


def m_bound():
    return M * W0 * B_FOOT * ELL


# ---------------------------------------------------------------- Lab B (lines 404-430)
def classify(tau, kp, T=8.0, dt=0.002):
    n, d = int(T / dt), max(1, int(round(tau / dt)))
    th, om, a = [0.0] * (n + 1), [0.0] * (n + 1), W0 * W0
    th[0] = 0.02
    for i in range(n):
        if i - d >= 0:
            thd, omd = th[i - d], om[i - d]
        else:
            thd = omd = 0.0
        om[i + 1] = om[i] + dt * (a * th[i] - kp * thd - KD * omd)
        th[i + 1] = th[i] + dt * om[i + 1]
    late = max(abs(v) for v in th[int(0.7 * n):])
    if late > 0.3:
        return 2
    return 0 if late < 0.25 * abs(th[0]) else 1


@lru_cache(maxsize=None)
def lab_b():
    taus, kps = np.linspace(0.02, 0.30, 40), np.linspace(11, 32, 30)
    grid = np.array([[classify(float(t), float(k)) for t in taus] for k in kps])
    assert round(float((grid == 0).mean()), 2) == 0.37
    return taus, kps, grid


# ---------------------------------------------------------------- K3 (lines 611-656)
def settle(kp, kd, tau=0.10, T=6.0, dt=0.002):
    n, d = int(T / dt), int(round(tau / dt))
    th, om, a = [0.0] * (n + 1), [0.0] * (n + 1), W0 * W0
    om[0] = 0.30
    for i in range(n):
        if i - d >= 0:
            thd, omd = th[i - d], om[i - d]
        else:
            thd = omd = 0.0
        om[i + 1] = om[i] + dt * (a * th[i] - kp * thd - kd * omd)
        th[i + 1] = th[i] + dt * om[i + 1]
    ab = np.abs(np.array(th))
    if not np.isfinite(ab.max()) or ab[-150:].max() > 0.1 * ab.max():
        return math.inf
    return float(np.where(ab > 0.1 * ab.max())[0][-1] * dt)


def ceiling(kd, tau=0.10):
    """Island ceiling in kp at this kd and delay: the first sign change of Prop. 4.2's sine condition."""
    Om = np.linspace(1e-4, 60.0, 600000)
    f = np.sin(Om * tau) - kd * Om / (Om * Om + W0 * W0)
    i = np.where(np.sign(f[:-1]) != np.sign(f[1:]))[0][0]
    return float((Om[i] ** 2 + W0 ** 2) * np.cos(Om[i] * tau))


@lru_cache(maxsize=None)
def lab_k3():
    kps, kds = np.arange(12.0, 45.1, 1.0), np.arange(1.0, 14.01, 0.25)
    S = np.array([[settle(float(kp), float(kd)) for kd in kds] for kp in kps])      # [kp][kd]
    best = (math.inf, 0.0, 0.0)
    for i, kp in enumerate(kps):
        for j, kd in enumerate(kds):
            if S[i, j] < best[0]:
                best = (float(S[i, j]), float(kp), float(kd))
    s0, kp0, kd0 = best
    ref = (math.inf, 0.0, 0.0)
    for kp in np.arange(kp0 - 2.0, kp0 + 2.01, 0.5):
        for kd in np.arange(kd0 - 1.0, kd0 + 1.01, 0.1):
            v = settle(float(kp), float(kd))
            if v < ref[0]:
                ref = (v, float(kp), float(kd))
    design = settle(20.0, 3.0)
    ceil = ceiling(ref[2])
    assert (round(s0, 2), kp0, kd0) == (0.50, 28.0, 8.0)
    assert (round(ref[0], 2), round(ref[1], 1), round(ref[2], 1)) == (0.49, 28.5, 8.1)
    assert round(design, 2) == 4.17 and round(ceil, 1) == 57.0
    return kps, kds, S, best, ref, design


# ---------------------------------------------------------------- Lab C (lines 441-481), unchanged
def expm(Mx, terms=25):
    S, term = np.eye(len(Mx)), np.eye(len(Mx))
    for k in range(1, terms):
        term = term @ Mx / k
        S = S + term
    return S


@lru_cache(maxsize=None)
def lab_c(tau=0.10, w0=3.1, kp=20.0, kd=3.0, dt=0.005, T=8.0, qp=0.6, rm=0.07, seed=11):
    rng = np.random.default_rng(seed)
    A = np.array([[0, 1.0], [-(kp - w0 * w0), -kd]])
    F, Fp = expm(A * dt), expm(A * tau)
    n, d = int(T / dt), int(round(tau / dt))
    xt = np.zeros((n, 2))
    xt[0] = [0.08, 0.0]
    for i in range(n - 1):
        kick = np.sqrt(qp * dt) * rng.standard_normal()
        xt[i + 1] = F @ xt[i] + [0, kick]
    z = np.full(n, np.nan)
    for i in range(d, n):
        z[i] = xt[i - d, 0] + rm * rng.standard_normal()
    Hm = np.array([[1.0, 0.0]])
    Q = np.array([[0, 0], [0, qp * dt]])
    P, xc = np.eye(2) * 0.05, np.array([0.08, 0.0])
    pred = np.full(n, np.nan)
    for i in range(1, n):
        xc, P = F @ xc, F @ P @ F.T + Q
        if not np.isnan(z[i]):
            S = (Hm @ P @ Hm.T)[0, 0] + rm * rm
            Kk = (P @ Hm.T)[:, 0] / S
            xc = xc + Kk * (z[i] - (Hm @ xc)[0])
            P = (np.eye(2) - np.outer(Kk, Hm[0])) @ P
        pred[i] = (Fp @ xc)[0]
    mm = ~np.isnan(z)
    raw = float(np.sqrt(np.nanmean((z[mm] - xt[mm, 0]) ** 2)))
    prd = float(np.sqrt(np.nanmean((pred[mm] - xt[mm, 0]) ** 2)))
    assert (round(raw, 3), round(prd, 3)) == (0.075, 0.033)
    return np.arange(n) * dt, xt[:, 0], z, pred, raw, prd, d


# ---------------------------------------------------------------- Prop. 5.1 and its simulation (lines 225, 232-234)
def sigma_deg(kp, q=Q0, kd=KD):
    return math.degrees(math.sqrt(q / (2.0 * (kp - W0 * W0) * kd)))


def em_run(kp, T, dt, seed, rec):
    """Euler-Maruyama for theta'' + kd theta' + (kp - w0^2) theta = eta, <eta eta> = q delta, started stationary."""
    a0, a1 = kp - W0 * W0, KD
    rng = np.random.default_rng(seed)
    th = rng.normal(0.0, math.sqrt(Q0 / (2 * a0 * a1)))
    om = rng.normal(0.0, math.sqrt(Q0 / (2 * a1)))
    n = int(round(T / dt))
    kick = rng.standard_normal(n) * math.sqrt(Q0 * dt)
    out = [th]
    for i in range(n):
        om += (-a0 * th - a1 * om) * dt + kick[i]
        th += om * dt
        if (i + 1) % rec == 0:
            out.append(th)
    return np.array(out)


TRACE_SEED = 134                                    # chosen so the 24 s trace shows what the caption says (see fig8)


@lru_cache(maxsize=None)
def noise_dots():
    out = []
    for kp in (12.0, 16.0, 20.0, 26.0):
        x = em_run(kp, 2000.0, 0.005, 7, 10)
        out.append((kp, math.degrees(math.sqrt(float(np.mean(x ** 2))))))
    return out


# ---------------------------------------------------------------- shared small pieces
def hollow(s, x, y, col):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(H.PX["dot"]):.2f}" fill="#fff" stroke="{col}" '
            f'stroke-width="{s(1.8):.2f}"/>')


def fdot(s, x, y, col, r=None):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r or H.PX["dot"]):.2f}" fill="{col}" stroke="#fff" '
            f'stroke-width="{s(1.5):.2f}"/>')


def tk(vals, f="{:g}"):
    return [(v, mn(v, f)) for v in vals]


def vref(s, ax, x, col, y_top=None, y_bot=None):
    return H.line(s, ax.X(x), y_top if y_top is not None else getattr(ax, 'top', None) or ax.y1, ax.X(x), y_bot if y_bot is not None else ax.y0,
                  col, "ref", H.DASH_REF)


def href(s, ax, y, col, x0=None, x1=None):
    return H.line(s, x0 if x0 is not None else ax.x0, ax.Y(y), x1 if x1 is not None else ax.x1, ax.Y(y),
                  col, "ref", H.DASH_REF)


def swatch(s, x, y, col, txt, op=0.35):
    """Filled legend square (a region) + ink text."""
    return (f'<rect x="{x:.2f}" y="{y - 10:.2f}" width="14" height="11" fill="{col}" fill-opacity="{op}" '
            f'stroke="{col}" stroke-width="{s(0.8):.2f}"/>' + label(s, x + 19, y, txt, "label2", I["secondary"]))


def tint(col, a):
    """The colour as it looks at opacity a over white, as an opaque hex (adjacent opaque cells show no seams)."""
    r, g, b = (int(col[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(round(255 - a * (255 - v)) for v in (r, g, b))


def poly_fill(pts, col, op):
    return f'<polygon points="{PM.pts_str(pts)}" fill="{col}" fill-opacity="{op}"/>'


def deg(v):
    return f"{v:.2f}°"


# ================================================================ svg #5 (Fig. 4): phase portraits
W0S = "ω₀"


def hyperbolas(c=0.05, w0=W0):
    """Level sets xi*eta = +-c of the free pendulum in (theta, theta-dot); time runs with increasing u (xi grows)."""
    u = np.linspace(-3.2, 3.2, 801)
    r = math.sqrt(c)
    out = []
    for sg in (1, -1):
        out.append((sg * r * np.cosh(u), sg * w0 * r * np.sinh(u)))            # right and left branch (xi*eta = +c)
        out.append((sg * r * np.sinh(u), sg * w0 * r * np.cosh(u)))            # upper and lower branch (xi*eta = -c)
    keep = []
    for th, td in out:
        idx = np.where((np.abs(th) <= 0.3) & (np.abs(td) <= 0.9))[0]
        keep.append((th[idx[0]:idx[-1] + 1:8], td[idx[0]:idx[-1] + 1:8]))
    return keep


def closed_loop(x0, T=3.5, dt=0.025):
    A = np.array([[0.0, 1.0], [-(KP - W0 * W0), -KD]])
    lam, V = np.linalg.eig(A)
    t = np.arange(0, T + dt / 2, dt)
    c = np.linalg.solve(V, np.array(x0, dtype=complex))
    X = np.real(V @ (c[:, None] * np.exp(lam[:, None] * t[None, :])))
    return t, X[0], X[1]


def along(s, ax, th, txt, col=I["primary"], off=12):
    """A label set parallel to an eigenline through the origin (slope w0 or -w0), beside it."""
    td = W0 * th
    x, y = ax.X(th), ax.Y(td)
    dx, dy = ax.X(th + 0.01) - x, ax.Y(td + W0 * 0.01) - y
    n = math.hypot(dx, dy)
    ang = math.degrees(math.atan2(dy, dx))
    nx, ny = dy / n, -dx / n                           # the normal that points up on the screen
    if ny > 0:
        nx, ny = -nx, -ny
    cx, cy = x + off * nx, y + off * ny + 4
    return label(s, cx, cy, txt, "label2", col, "middle", f'transform="rotate({ang:.2f} {cx:.2f} {cy:.2f})"')


def fig5():
    VB = (0, 0, 760, 432)
    s = H.Scale(VB[2], VB[3])
    p = "m10f5_"
    Lx = PM.Ax((74, 74, 354, 324), (-0.3, 0.3), (-0.9, 0.9))
    Rx = PM.Ax((452, 74, 732, 324), (-0.3, 0.3), (-0.9, 0.9))
    xt = [(v, mn(v, "{:g}")) for v in (-0.2, 0.0, 0.2)]
    yt = [(v, mn(v, "{:g}")) for v in (-0.8, -0.4, 0.0, 0.4, 0.8)]
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    for ax in (Lx, Rx):
        o += PM.axes(s, ax, xt, yt, "θ (rad)", "θ̇ (rad s⁻¹)", ylab_x=ax.x0 - 50)
        o.append(H.line(s, ax.X(0), ax.top, ax.X(0), ax.y0, I["rule"], "ref"))
        o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["rule"], "ref"))
    cl = lambda ax: (ax.x0 + ax.x1) / 2                                         # noqa: E731
    o.append(label(s, cl(Lx), 30, "open loop, u = 0: saddle", "label", I["primary"], "middle"))
    o.append(label(s, cl(Lx), 50, f"eigenvalues ±{W0S} = ±{W0} rad s⁻¹", "label2", I["secondary"], "middle"))
    lam, om_d = -KD / 2, math.sqrt((KP - W0 * W0) - (KD / 2) ** 2)
    assert (round(lam, 2), round(om_d, 2)) == (-1.5, 2.85)                       # line 136
    o.append(label(s, cl(Rx), 30, "closed loop, u = −Kx: stable spiral", "label", I["primary"], "middle"))
    o.append(label(s, cl(Rx), 50, f"k{sub('p', s, 'label2')} = {KP:g}, k{sub('d', s, 'label2')} = {KD:g}: poles −1.5 ± 2.85 i",
                   "label2", I["secondary"], "middle"))
    # left: other initial states, then the two eigendirections (Prop. 1.1)
    for th, td in hyperbolas():
        o.append(PM.poly(s, [(Lx.X(a), Lx.Y(b)) for a, b in zip(th, td)], I["rule"], "leader", None,
                         f'marker-end="url(#{p}a_dim)"'))
    te = 0.285
    for sg in (1, -1):
        o.append(H.arrow(s, p, Lx.X(sg * 0.012), Lx.Y(sg * W0 * 0.012), Lx.X(sg * te), Lx.Y(sg * W0 * te), "force"))
        o.append(H.arrow(s, p, Lx.X(sg * te), Lx.Y(-sg * W0 * te), Lx.X(sg * 0.012), Lx.Y(-sg * W0 * 0.012), "geometry"))
    o.append(PM.dot(s, Lx.X(0), Lx.Y(0), I["primary"]))
    o.append(along(s, Lx, 0.155, "unstable"))
    o.append(along(s, Lx, -0.155, "stable"))
    # right: thin spirals, the push, the bold recovery
    for x0 in [(-0.26, 0.55), (0.25, -0.50), (-0.22, -0.60), (0.20, 0.45), (-0.12, 0.80), (0.12, -0.80)]:
        t, th, td = closed_loop(x0, 3.0)
        assert np.abs(th).max() <= 0.3 and np.abs(td).max() <= 0.9, x0
        o.append(PM.poly(s, [(Rx.X(a), Rx.Y(b)) for a, b in zip(th, td)], I["rule"], "curve_multi"))
    push = 0.85
    t, th, td = closed_loop((0.0, push), 3.5)
    o.append(PM.poly(s, [(Rx.X(a), Rx.Y(b)) for a, b in zip(th, td)], I["primary"], "curve"))
    for k in range(1, 7):
        i = int(round(0.5 * k / 0.025))
        o.append(PM.dot(s, Rx.X(th[i]), Rx.Y(td[i]), I["primary"], hollow=True, r=3))
    o.append(PM.dot(s, Rx.X(0), Rx.Y(0), O["neural"]))
    o.append(PM.dot(s, Rx.X(0), Rx.Y(push), O["flag"], r=5))
    o.append(label(s, Rx.X(0) + 10, Rx.Y(push) + 4, f"push: θ̇ = {push} rad s⁻¹", "label2", I["primary"]))
    yl = 394
    o += PM.legend(s, Lx.x0, yl, [(SER[0], None, "unstable: ξ grows"), (SER[1], None, "stable: returns")])
    o += PM.legend(s, Lx.x0, yl + 20, [(I["rule"], None, "other states")])
    o += PM.legend(s, Rx.x0, yl, [(I["primary"], None, "recovery from the push"), (O["neural"], None, "upright", "dot")])
    o += PM.legend(s, Rx.x0, yl + 20, [(I["rule"], None, "other states"), (I["primary"], None, "every 0.5 s", "hdot")])
    aria = ("Two phase portraits in the sway-angle plane, theta against theta-dot. Left, the uncontrolled inverted "
            "pendulum is a saddle: arrows run outward along the unstable eigendirection, slope plus omega-zero, "
            "and inward along the stable one, slope minus omega-zero, while every other state follows a hyperbola "
            "past the origin and away. Right, with state feedback kp = 20 and kd = 3 the origin is a stable "
            "spiral with poles minus 1.5 plus or minus 2.85 i; the bold curve is the computed recovery from a "
            "push of 0.85 radians per second at upright, marked every half second.")
    ptsL = [[Lx.X(x), [Lx.Y(W0 * x), Lx.Y(-W0 * x)],
             f"θ = {mn(x, '{:.2f}')} rad: unstable line θ̇ = {mn(W0 * x, '{:.2f}')}, stable line θ̇ = {mn(-W0 * x, '{:.2f}')} rad/s"]
            for x in np.linspace(-0.285, 0.285, 60)]
    ptsR = sorted([[Rx.X(a), Rx.Y(b), f"t = {tt:.2f} s: θ = {mn(a, '{:.3f}')} rad, θ̇ = {mn(b, '{:.3f}')} rad/s"]
                   for tt, a, b in zip(t, th, td)], key=lambda q: q[0])
    return PM.svg(VB, aria, s, o, H.hover_attr([(Lx.box, ptsL), (Rx.box, ptsR)]))


# ================================================================ svg #7 (Fig. 6): stability island and three trajectories
def island_poly(ax, kd, kp_top, w0=W0):
    t, k = boundary(kd, w0)
    sel = k <= kp_top
    tb, kb = t[sel], k[sel]
    floor = w0 * w0
    pts = [(ax.X(0), ax.Y(floor)), (ax.X(t[0]), ax.Y(floor))]
    curve = [(ax.X(a), ax.Y(b)) for a, b in zip(tb[::40], kb[::40])] + [(ax.X(tb[-1]), ax.Y(kb[-1]))]
    pts += curve + [(ax.X(0), ax.Y(kp_top))]
    return pts, curve


def fig7():
    VB = (0, 0, 760, 392)
    s = H.Scale(VB[2], VB[3])
    Lx = PM.Ax((84, 64, 354, 324), (0, 0.34), (6, 36))
    Rx = PM.Ax((456, 64, 734, 324), (0, 4.5), (-0.14, 0.14))
    floor = W0 * W0
    o = PM.axes(s, Lx, tk((0, 0.1, 0.2, 0.3)), tk((10, 20, 30)), "feedback delay τ (s)",
                f"position gain k{sub('p', s)} (s⁻²)", ylab_x=30)
    poly, curve = island_poly(Lx, KD, 36)
    o.insert(0, poly_fill(poly, SER[1], 0.14))
    o.append(PM.poly(s, curve, I["primary"], "curve"))
    o.append(href(s, Lx, floor, I["secondary"]))
    o.append(label(s, Lx.X(0.335), Lx.Y(floor) + 17, f"k{sub('p', s, 'label2')} = {W0S}² = {floor:.2f}",
                   "label2", I["secondary"], "end"))
    taus = [(0.10, SER[1]), (TC, SER[2]), (0.172, SER[0])]
    for tau, col in taus:
        o.append(fdot(s, Lx.X(tau), Lx.Y(KP), col))
    o.append(label(s, Lx.X(0.012), Lx.Y(KP) - 11, f"k{sub('p', s, 'label2')} = 20", "label2", I["secondary"]))
    o.append(label(s, Lx.X(0.05), Lx.Y(14), "stable", "label", I["primary"], "middle"))
    o.append(label(s, Lx.X(0.23), Lx.Y(31), "unstable", "label", I["primary"], "middle"))
    o.append(label(s, Lx.X(0.335), Lx.Y(26.5), f"boundary, k{sub('d', s, 'label2')} = {KD:g} s⁻¹", "label2",
                   I["secondary"], "end"))
    # right: the three delayed trajectories
    o += PM.axes(s, Rx, tk((0, 1, 2, 3, 4)), tk((-0.1, 0, 0.1), "{:g}"), "time (s)", "sway θ (rad)", ylab_x=Rx.x0 - 58)
    o.append(H.line(s, Rx.x0, Rx.Y(0), Rx.x1, Rx.Y(0), I["rule"], "ref"))
    runs = [dde(tau) for tau, _ in taus]
    for (t, th), (_, col) in zip(runs, taus):
        sel = np.arange(0, len(t), 80)
        o.append(PM.curve(s, Rx, t[sel], th[sel], col, "curve_multi"))
    thb = runs[1][1]                                        # the boundary run keeps its amplitude
    pk = [abs(thb[i]) for i in range(1, len(thb) - 1) if (thb[i] - thb[i - 1]) * (thb[i + 1] - thb[i]) < 0]
    assert max(pk) / min(pk) < 1.08, pk
    assert abs(runs[0][1].min() + 0.0137) < 0.0005 and runs[2][1].max() > 0.12
    items = [(SER[1], "τ = 100 ms: decays"), (SER[2], f"τ = {1000 * TC:.0f} ms: marginal"),
             (SER[0], "τ = 172 ms: grows")]
    yy = Rx.top + 18
    for col, txt in items:
        o.append(H.line(s, Rx.x0 + 10, yy - 4.5, Rx.x0 + 34, yy - 4.5, col, "curve_multi"))
        o.append(label(s, Rx.x0 + 40, yy, txt, "label2", I["primary"]))
        yy += 19
    aria = ("Left, the stability island in the delay-gain plane at damping gain 3: a boundary curve from Proposition "
            "4.2 separates a shaded stable region, small delay and gain above omega-zero squared = 9.61, from the "
            "unstable region above and to the right. Three points on the line kp = 20 sit at delays 100, 137 and 172 "
            "milliseconds. Right, the delayed sway trajectory at each: it decays inside, rings at constant amplitude "
            "on the boundary and grows past it.")
    tb_, kb_ = boundary(KD)
    tpts = np.linspace(float(np.interp(36, kb_, tb_)), float(tb_[0]), 100)
    ptsL = [[Lx.X(t), Lx.Y(min(kp_ceiling(t, KD), 36)),
             f"τ = {1000 * t:.0f} ms: ceiling kp = {kp_ceiling(t, KD):.1f} s⁻², floor {floor:.2f}"] for t in tpts]
    ptsR = [[Rx.X(runs[0][0][i]), [Rx.Y(r[1][i]) for r in runs],
             f"t = {runs[0][0][i]:.2f} s: θ = {mn(runs[0][1][i], '{:.3f}')} (100 ms), {mn(runs[1][1][i], '{:.3f}')} (137 ms), "
             f"{mn(runs[2][1][i], '{:.3f}')} (172 ms) rad"] for i in range(0, len(runs[0][0]), 45)]
    return PM.svg(VB, aria, s, o, H.hover_attr([(Lx.box, ptsL), (Rx.box, ptsR)]))


# ================================================================ svg #8 (Fig. 7): stochastic sway
def fig8():
    VB = (0, 0, 760, 428)
    s = H.Scale(VB[2], VB[3])
    Lx = PM.Ax((84, 46, 354, 316), (0, 24), (-1.5, 1.5))
    Rx = PM.Ax((500, 46, 734, 316), (10, 34), (0, 1.4))
    sig = sigma_deg(KP)
    assert f"{sig:.2f}" == "0.34"                                           # caption: the band's value 0.34 deg
    x = np.degrees(em_run(KP, 24.0, 0.005, TRACE_SEED, 10))                  # one sample every 0.05 s
    t = np.arange(len(x)) * 0.05
    rms = float(np.sqrt(np.mean(x ** 2)))
    outside = float(np.mean(np.abs(x) > sig))
    assert abs(rms / sig - 1) < 0.02 and 0.30 <= outside <= 0.36 and 2.9 <= np.abs(x).max() / sig <= 3.2, (rms, outside)
    o = PM.axes(s, Lx, tk((0, 8, 16, 24)), tk((-1, 0, 1)), "time (s)", "sway angle θ (deg)", ylab_x=32)
    o.append(PM.curve(s, Lx, t, x, SER[1], "curve_multi"))
    for sg in (1, -1):
        o.append(href(s, Lx, sg * sig, SER[0]))
    o.append(label(s, Lx.x1 + 8, Lx.Y(sig) + 4.5, f"+σ = {sig:.2f}°", "label2", I["primary"]))
    o.append(label(s, Lx.x1 + 8, Lx.Y(-sig) + 4.5, "−σ", "label2", I["primary"]))
    o.append(label(s, Lx.x0 + 8, Lx.top + 17, f"trace RMS {rms:.2f}°; {100 * outside:.0f} % of samples outside ±σ",
                   "label2", I["secondary"]))
    o += PM.legend(s, Lx.x0, 392, [(SER[1], None, "simulated sway"), (SER[0], H.DASH_REF, "±σ, Proposition 5.1")])
    # right: RMS against kp
    o += PM.axes(s, Rx, tk((12, 16, 20, 24, 28, 32)), tk((0, 0.5, 1.0), "{:g}"), f"position gain k{sub('p', s)} (s⁻²)",
                 "RMS sway (deg)", ylab_x=Rx.x0 - 48)
    edge = kp_ceiling(0.10, KD)
    assert round(edge, 1) == 27.8                                            # K6, line 697
    ks = np.linspace(10.45, 34, 240)
    sg = np.array([sigma_deg(k) for k in ks])
    below = ks <= edge
    o.append(PM.curve(s, Rx, ks[below][::3], sg[below][::3], I["primary"], "curve"))
    j = int(np.where(below)[0][-1])
    o.append(PM.curve(s, Rx, ks[j:][::3], sg[j:][::3], I["rule"], "curve_multi", PM.DASH_SER))
    o.append(vref(s, Rx, edge, SER[0]))
    for kp, r in noise_dots():
        assert abs(r / sigma_deg(kp) - 1) < 0.06, (kp, r)
        o.append(PM.dot(s, Rx.X(kp), Rx.Y(r), SER[1]))
    o.append(label(s, Rx.X(edge) - 7, Rx.top + 16, "island edge,", "label2", I["primary"], "end"))
    o.append(label(s, Rx.X(edge) - 7, Rx.top + 32, "τ = 100 ms:", "label2", I["secondary"], "end"))
    o.append(label(s, Rx.X(edge) - 7, Rx.top + 48, f"k{sub('p', s, 'label2')} = {edge:.1f}", "label2", I["secondary"], "end"))
    o.append(label(s, Rx.X(14.6), Rx.Y(0.82), "analytic law", "label2", I["primary"]))
    o.append(label(s, Rx.X(15.5), Rx.Y(0.20), "simulation (dots)", "label2", I["primary"]))
    o += PM.legend(s, Rx.x0 - 20, 392, [(I["primary"], None, "analytic law"), (SER[1], None, "simulation", "dot")])
    o += PM.legend(s, Rx.x0 - 20, 412, [(I["rule"], PM.DASH_SER, "extrapolated: the loop is unstable there")])
    aria = ("Left, a simulated 24-second quiet-standing sway trace at kp = 20: the angle wanders about upright, "
            f"crossing the dashed plus and minus sigma band of {sig:.2f} degrees on about a third of its samples and "
            f"peaking near three sigma, with an RMS of {rms:.2f} degrees. Right, RMS sway against position gain: the "
            "analytic law of Proposition 5.1 falls as gain rises, Euler-Maruyama dots lie on it, and a red dashed line "
            f"marks the island edge at kp = {edge:.1f} for a 100 millisecond delay; beyond it the grey dashed "
            "continuation is the same formula where the loop is unstable.")
    ptsL = [[Lx.X(a), Lx.Y(b), f"t = {a:.2f} s: θ = {mn(b, '{:.2f}')} deg (σ = {sig:.2f})"] for a, b in zip(t, x)]
    ptsR = [[Rx.X(k), Rx.Y(v), f"kp = {k:.1f}: RMS {v:.2f} deg" + ("" if k <= edge else " (loop unstable, formula not valid)")]
            for k, v in zip(ks, sg)]
    return PM.svg(VB, aria, s, o, H.hover_attr([(Lx.box, ptsL), (Rx.box, ptsR)]))


# ================================================================ svg #9 (Fig. 8): fusion and prediction
def gauss(x, mu, var):
    return np.exp(-(x - mu) ** 2 / (2 * var)) / math.sqrt(2 * math.pi * var)


def fig9():
    VB = (0, 0, 760, 432)
    s = H.Scale(VB[2], VB[3])
    mu_p, var_p, mu_m, var_m = -0.5, 1.0, 1.1, 0.36                    # an illustration with K_f = 0.74
    Kf = var_p / (var_p + var_m)
    mu_f, var_f = mu_p + Kf * (mu_m - mu_p), (1 - Kf) * var_p
    assert round(Kf, 2) == 0.74 and var_f < min(var_p, var_m)
    assert abs(var_f - var_p * var_m / (var_p + var_m)) < 1e-12
    Lx = PM.Ax((84, 74, 374, 314), (-4, 4), (0, 0.9))
    Rx = PM.Ax((458, 74, 734, 314), (0, 8), (-0.3, 0.3))
    xs = np.linspace(-4, 4, 81)
    C_PRED, C_MEAS, C_FUSED = SER[2], SER[1], SER[0]
    ser = [(C_PRED, mu_p, var_p), (C_MEAS, mu_m, var_m), (C_FUSED, mu_f, var_f)]
    o = PM.axes(s, Lx, tk((-2, 0, 2)), tk((0, 0.3, 0.6, 0.9), "{:g}"), "state estimate (arbitrary units)",
                "probability density", ylab_x=30)
    for col, mu, var in ser:
        o.append(PM.curve(s, Lx, xs, gauss(xs, mu, var), col, "curve" if col == C_FUSED else "curve_multi"))
    cl = lambda ax: (ax.x0 + ax.x1) / 2                                         # noqa: E731
    o.append(label(s, cl(Lx), 30, f"K{sub('f', s)} = σ{sub('p', s)}² / (σ{sub('p', s)}² + σ{sub('m', s)}²) = {Kf:.2f}",
                   "label", I["primary"], "middle"))
    o.append(label(s, cl(Lx), 50, f"σ{sub('p', s, 'label2')}² = {var_p:.2f}, σ{sub('m', s, 'label2')}² = {var_m:.2f}, "
                   f"fused σ{sub('+', s, 'label2')}² = {var_f:.2f}", "label2", I["secondary"], "middle"))
    o.append(label(s, Lx.X(-1.55), Lx.Y(0.29), "prediction", "label2", I["primary"], "end"))
    o.append(label(s, Lx.X(1.75), Lx.Y(0.45), "measurement", "label2", I["primary"]))
    o.append(label(s, Lx.X(mu_f), Lx.Y(gauss(mu_f, mu_f, var_f)) - 8, "fused", "label2", I["primary"], "middle"))
    # right: Lab C
    t, xt, z, pred, raw, prd, d = lab_c()
    o += PM.axes(s, Rx, tk((0, 2, 4, 6, 8)), tk((-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3), "{:g}"), "time (s)", "sway θ (rad)",
                 ylab_x=Rx.x0 - 58)
    o.append(PM.curve(s, Rx, t[d::4], z[d::4], C_MEAS, "curve_multi", extra='opacity="0.55"'))
    o.append(PM.curve(s, Rx, t[::6], xt[::6], I["primary"], "curve"))
    o.append(PM.curve(s, Rx, t[1::6], pred[1::6], C_FUSED, "curve"))
    o.append(label(s, cl(Rx), 30, "Lab C: predictor against the true state", "label", I["primary"], "middle"))
    o.append(label(s, cl(Rx), 50, f"RMS error: predictor {prd:.3f}, raw {raw:.3f} rad",
                   "label2", I["secondary"], "middle"))
    yl = 394
    o += PM.legend(s, Lx.x0, yl, [(C_PRED, None, "prediction"), (C_MEAS, None, "measurement"), (C_FUSED, None, "fused")])
    o += PM.legend(s, Rx.x0, yl, [(I["primary"], None, "true θ"), (C_FUSED, None, "predictor")])
    o += PM.legend(s, Rx.x0, yl + 20, [(C_MEAS, None, "delayed noisy measurement")])
    aria = ("Left, three Gaussian densities: a broad model prediction with variance 1.00, a narrower measurement with "
            f"variance 0.36 and the fused estimate, sharper than both with variance {var_f:.2f} and placed between them "
            f"by the Kalman gain {Kf:.2f}. Right, Lab C on a simulated sway at sixteen times the quiet-standing "
            "noise: the delayed noisy measurement scatters widely, the true state is a smooth curve, and the predictor "
            f"follows it closely, with RMS error {prd:.3f} radians against {raw:.3f} for the raw measurement.")
    ptsL = [[Lx.X(a), [Lx.Y(gauss(a, mu, var)) for _, mu, var in ser],
             f"x = {mn(a, '{:.2f}')}: prediction {gauss(a, mu_p, var_p):.2f}, measurement {gauss(a, mu_m, var_m):.2f}, "
             f"fused {gauss(a, mu_f, var_f):.2f}"] for a in xs]
    ptsR = [[Rx.X(t[i]), [Rx.Y(xt[i]), Rx.Y(pred[i])] + ([Rx.Y(z[i])] if i >= d else []),
             f"t = {t[i]:.2f} s: true {mn(xt[i], '{:.3f}')}, predictor {mn(pred[i], '{:.3f}')}" +
             (f", measurement {mn(z[i], '{:.3f}')} rad" if i >= d else " rad")] for i in range(1, len(t), 8)]
    return PM.svg(VB, aria, s, o, H.hover_attr([(Lx.box, ptsL), (Rx.box, ptsR)]))


# ================================================================ svg #12 (Fig. 11): aging as parameter drift
SOFT = 6.0                                           # N s: the softening of the success edge (a drawing choice)
DAILY_MED, DAILY_SD = 18.0, 0.5                      # assumed lognormal of daily impulses (line 343)


def lognorm_pdf(J):
    return np.exp(-(np.log(J / DAILY_MED)) ** 2 / (2 * DAILY_SD ** 2)) / (J * DAILY_SD * math.sqrt(2 * math.pi))


def p_exceed(jc):
    """Fraction of daily impulses above jc: the fall probability of line 345."""
    return 0.5 * math.erfc(math.log(jc / DAILY_MED) / DAILY_SD / math.sqrt(2))


def success(J, jc):
    return 1.0 / (1.0 + np.exp((J - jc) / SOFT))


def fig12():
    VB = (0, 0, 760, 452)
    s = H.Scale(VB[2], VB[3])
    p = "m10f12_"
    jy, ja = j_crit(**YOUNG), j_crit(**AGED)
    assert (round(jy, 1), round(ja, 1)) == (51.4, 19.3)                         # lines 343, 869
    fy, fa = p_exceed(jy), p_exceed(ja)
    assert (round(100 * fy, 1), round(100 * fa, 1)) == (1.8, 44.3), (fy, fa)    # line 345 prints 44.5 (see the report)
    Lx = PM.Ax((84, 64, 354, 324), (0, 0.34), (6, 36))
    Rx = PM.Ax((470, 64, 734, 324), (0, 70), (0, 1.05))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    floor = W0 * W0
    o += PM.axes(s, Lx, tk((0, 0.1, 0.2, 0.3)), tk((10, 20, 30)), "reflex delay τ (s)",
                 f"position gain k{sub('p', s)} (s⁻²)", ylab_x=30)
    cl = lambda ax: (ax.x0 + ax.x1) / 2                                         # noqa: E731
    o.append(label(s, cl(Lx), 38, "stability island: the damping gain falls, the delay rises", "label2", I["secondary"], "middle"))
    pa, ca = island_poly(Lx, 1.7, 36)
    py, cy = island_poly(Lx, KD, 36)
    o.insert(0, poly_fill(pa, SER[0], 0.14))
    o.insert(0, poly_fill(py, SER[1], 0.14))
    o.append(PM.poly(s, cy, SER[1], "curve"))
    o.append(PM.poly(s, ca, SER[0], "curve"))
    o.append(href(s, Lx, floor, I["secondary"]))
    ta_c = tau_crit(KP, 1.7)
    assert round(1000 * ta_c) == 83 and AGED["tau"] > ta_c and YOUNG["tau"] < TC
    o.append(H.arrow(s, p, Lx.X(YOUNG["tau"]) + 8, Lx.Y(KP), Lx.X(AGED["tau"]) - 8, Lx.Y(KP), "dim"))
    o.append(fdot(s, Lx.X(YOUNG["tau"]), Lx.Y(KP), SER[1]))
    o.append(fdot(s, Lx.X(AGED["tau"]), Lx.Y(KP), SER[0]))
    o.append(label(s, Lx.X(AGED["tau"]) + 10, Lx.Y(KP) + 4.5, "delay τ rises", "label2", I["primary"]))
    o.append(label(s, Lx.X(0.145), Lx.Y(12.4), "young", "label2", I["primary"]))
    o.append(label(s, Lx.X(0.035), Lx.Y(12.4), "aged", "label2", I["primary"]))
    o.append(label(s, Lx.X(0.335), Lx.Y(floor) + 17, f"k{sub('p', s, 'label2')} = {W0S}²", "label2", I["secondary"], "end"))
    # right: recovery success against the impulse, over the everyday distribution
    Js = np.linspace(0.5, 70, 200)
    dens = lognorm_pdf(Js)
    dens = 0.42 * dens / dens.max()                                             # arbitrary vertical scale
    o += PM.axes(s, Rx, tk((0, 20, 40, 60)), tk((0, 0.5, 1.0), "{:g}"), "perturbation impulse J (N s)", "recovery success",
                 ylab_x=Rx.x0 - 48)
    o.append(label(s, cl(Rx), 38, f"fall probability {100 * fy:.1f} % (young), {100 * fa:.1f} % (aged)", "label2",
                   I["secondary"], "middle"))
    base = [(Rx.X(Js[0]), Rx.Y(0))]
    o.append(poly_fill(base + [(Rx.X(a), Rx.Y(b)) for a, b in zip(Js[::3], dens[::3])] + [(Rx.X(Js[-1]), Rx.Y(0))],
                       I["rule"], 0.25))
    Jf = np.linspace(0, 70, 141)
    o.append(PM.curve(s, Rx, Jf, success(Jf, jy), SER[1], "curve"))
    o.append(PM.curve(s, Rx, Jf, success(Jf, ja), SER[0], "curve"))
    o.append(PM.dot(s, Rx.X(jy), Rx.Y(0.5), SER[1]))
    o.append(PM.dot(s, Rx.X(ja), Rx.Y(0.5), SER[0]))
    o.append(label(s, Rx.X(jy) + 8, Rx.Y(0.5) - 6, f"{jy:.1f}", "label2", I["primary"]))
    o.append(label(s, Rx.X(ja) + 8, Rx.Y(0.5) - 6, f"{ja:.1f}", "label2", I["primary"]))
    o.append(label(s, Rx.X(33), Rx.Y(0.34), "everyday", "label2", I["secondary"]))
    o.append(label(s, Rx.X(33), Rx.Y(0.34) + 15, "perturbations", "label2", I["secondary"]))
    o.append(H.line(s, Rx.X(32.3), Rx.Y(0.285), Rx.X(27.5), Rx.Y(0.16), I["rule"], "leader"))
    yl = 396
    o += PM.legend(s, Lx.x0, yl, [(SER[1], None, f"young: k{sub('d', s, 'label2')} = 3.0 s⁻¹, τ = 0.10 s", "band")])
    o += PM.legend(s, Lx.x0, yl + 20, [(SER[0], None, f"aged: k{sub('d', s, 'label2')} = 1.7 s⁻¹, τ = 0.18 s", "band")])
    o += PM.legend(s, Rx.x0, yl, [(SER[1], None, "young"), (SER[0], None, "aged")])
    o += PM.legend(s, Rx.x0, yl + 20, [(I["rule"], None, "everyday impulses (lognormal, assumed)", "band")])
    o.append(label(s, Rx.x0, yl + 40, f"success edge softened: logistic, width {SOFT:g} N s", "label2", I["muted"]))
    aria = ("Left, the stability island of the delay-gain plane drawn twice, at damping gain 3.0 for a young parameter set "
            "and 1.7 for an aged one; the aged island is smaller, and the operating point at kp = 20 moves right from a "
            "delay of 0.10 to 0.18 seconds, out of the aged island. Right, recovery success against perturbation "
            f"impulse for the two sets, crossing one half at {jy:.1f} newton seconds young and {ja:.1f} aged, over a "
            "shaded assumed lognormal distribution of everyday impulses with median 18; the fall probability is "
            f"{100 * fy:.1f} percent young and {100 * fa:.1f} percent aged.")
    tb_, kb_ = boundary(KD)
    tpts = np.linspace(float(np.interp(36, kb_, tb_)), float(tb_[0]), 100)
    ta_, ka_ = boundary(1.7)
    ptsL = [[Lx.X(t), [Lx.Y(min(kp_ceiling(t, KD), 36)), Lx.Y(min(kp_ceiling(t, 1.7), 36))],
             f"τ = {1000 * t:.0f} ms: ceiling kp = {kp_ceiling(t, KD):.1f} (young), {kp_ceiling(t, 1.7):.1f} (aged)"] for t in tpts]
    ptsR = [[Rx.X(j), [Rx.Y(success(j, jy)), Rx.Y(success(j, ja))],
             f"J = {j:.1f} N s: success {success(j, jy):.2f} young, {success(j, ja):.2f} aged"] for j in Jf]
    return PM.svg(VB, aria, s, o, H.hover_attr([(Lx.box, ptsL), (Rx.box, ptsR)]))


# ================================================================ svg #14 (Fig. 12): Lab A
def fig14():
    VB = (0, 0, 760, 450)
    s = H.Scale(VB[2], VB[3])
    taus, jm = lab_a()
    ax = PM.Ax((84, 40, 730, 370), (0, 0.2), (0, 25))
    bound = m_bound()
    o = PM.axes(s, ax, tk((0, 0.05, 0.1, 0.15, 0.2)), tk((0, 5, 10, 15, 20, 25)), "feedback delay τ (s)",
                "largest arrestable impulse (N s)", ylab_x=30)
    o.append(href(s, ax, bound, I["secondary"]))
    o.append(vref(s, ax, TC, SER[0]))
    o.append(PM.curve(s, ax, taus, jm, SER[1], "curve"))
    at = {round(float(t), 4): float(j) for t, j in zip(taus, jm)}
    for t in (0.05, 0.10, 0.15):
        o.append(PM.dot(s, ax.X(t), ax.Y(at[t]), SER[1]))
        o.append(label(s, ax.X(t) + (9 if t == 0.15 else 0), ax.Y(at[t]) - (7 if t == 0.15 else 12), f"{at[t]:.1f}",
                       "label2", I["primary"], "start" if t == 0.15 else "middle"))
    o.append(PM.dot(s, ax.X(0.001), ax.Y(at[0.001]), SER[1]))
    o.append(label(s, ax.X(0.004), ax.Y(bound) - 8, f"τ → 0: {at[0.001]:.1f}", "label2", I["primary"]))
    o.append(label(s, ax.X(0.198), ax.Y(bound) - 8, f"m{W0S}b = {bound:.1f} N s", "label2", I["primary"], "end"))
    o.append(label(s, ax.X(TC) + 9, ax.Y(9), f"critical delay", "label2", I["primary"]))
    o.append(label(s, ax.X(TC) + 9, ax.Y(9) + 16, f"τ{sub('c', s, 'label2')} ≈ {1000 * TC:.0f} ms", "label2", I["secondary"]))
    o += PM.legend(s, ax.x0, 438, [(SER[1], None, "largest impulse, Lab A"), (I["secondary"], H.DASH_REF, f"bound m{W0S}b, Proposition 1.2"),
                                   (SER[0], H.DASH_REF, "critical delay")])
    aria = ("Largest arrestable push impulse against feedback delay, found by bisection over the delayed closed loop with the "
            f"ankle command saturated at the foot edge. As the delay goes to zero the curve meets the impulse-momentum bound "
            f"of {bound:.1f} newton seconds, a grey dashed line, at {at[0.001]:.1f}. It then falls gently, "
            f"{at[0.05]:.1f} at 50 milliseconds and {at[0.1]:.1f} at 100, and collapses near the critical delay of 137 "
            f"milliseconds, a red dashed line, to {at[0.15]:.1f} at 150 milliseconds.")
    ptsd = [[ax.X(t), ax.Y(j), f"τ = {1000 * t:.1f} ms: largest arrestable impulse {j:.1f} N s"] for t, j in zip(taus, jm)]
    return PM.svg(VB, aria, s, o, H.hover_attr(ax.box, ptsd))


# ================================================================ K plots (400 px)
def fig38():
    VB = (0, 0, W, 292)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (56, 40, 384, 232), (0, 0.2), (0, 25))
    taus, jm = lab_a()
    at = {round(float(t), 4): float(j) for t, j in zip(taus, jm)}
    bound = m_bound()
    o = [P.axes(tk((0, 0.05, 0.1, 0.15, 0.2)), tk((0, 5, 10, 15, 20, 25)), "feedback delay τ (s)",
                "largest arrestable impulse (N s)", grid=(5, 10, 15, 20, 25), ytx=14)]
    o.append(href(s, P, bound, I["secondary"]))
    o.append(vref(s, P, TC, SER[0]))
    o.append(P.curve(taus, jm, SER[1], multi=True))
    for t in (0.001, 0.05, 0.10, 0.15):
        o.append(P.dot(t, at[t], SER[1]))
    o.append(label(s, P.X(0.006), P.Y(at[0.001]) + 22, f"{at[0.001]:.1f}", "label2", I["primary"]))
    o.append(label(s, P.X(0.05) + 5, P.Y(at[0.05]) - 9, f"{at[0.05]:.1f}", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(0.10) + 5, P.Y(at[0.10]) - 9, f"{at[0.10]:.1f}", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(0.15) + 7, P.Y(at[0.15]) - 6, f"{at[0.15]:.1f}", "label2", I["primary"]))
    o.append(label(s, P.x1 - 3, P.Y(bound) - 6, f"m{W0S}b = {bound:.1f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(TC) + 6, P.Y(9), f"τ{sub('c', s, 'label2')} ≈ 137 ms", "label2", I["primary"]))
    o += [legend(s, 56, 18, [(SER[1], f"J{sub('max', s, 'label2')}(τ)", None), (I["secondary"], "bound", H.DASH_REF),
                             (SER[0], "critical delay", H.DASH_REF)])]
    aria = ("Problem K1 plot: the largest arrestable impulse against feedback delay. It starts at "
            f"{at[0.001]:.1f} newton seconds as the delay goes to zero, just under the impulse-momentum bound of "
            f"{bound:.1f}, and falls to {at[0.05]:.1f} at 50 milliseconds, {at[0.1]:.1f} at 100 and {at[0.15]:.1f} at 150: "
            "a slow decline, then a collapse at the critical delay of 137 milliseconds.")
    hv = [[P.X(t), P.Y(j), f"τ = {1000 * t:.1f} ms: Jmax = {j:.1f} N s"] for t, j in zip(taus, jm)]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


def fig39():
    VB = (0, 0, W, 312)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (52, 40, 384, 232), (0, 0.32), (10, 33))
    taus, kps, grid = lab_b()
    dt, dk = float(taus[1] - taus[0]), float(kps[1] - kps[0])
    COL = {0: SER[1], 1: SER[2], 2: SER[0]}
    cells, bad_s, bad_u = [], 0, 0
    for i, kp in enumerate(kps):
        for j, t in enumerate(taus):
            tc = tau_crit(float(kp), KD)
            bad_s += int(grid[i, j] == 0 and t > tc)
            bad_u += int(grid[i, j] == 2 and t < tc)
        j = 0
        while j < len(taus):
            k = j
            while k + 1 < len(taus) and grid[i, k + 1] == grid[i, j]:
                k += 1
            x0, x1 = P.X(taus[j] - dt / 2), P.X(taus[k] + dt / 2)
            y0, y1 = P.Y(kp - dk / 2) + 0.6, P.Y(kp + dk / 2) - 0.6
            cells.append(f'<rect x="{x0:.2f}" y="{y1:.2f}" width="{x1 - x0:.2f}" height="{y0 - y1:.2f}" '
                         f'fill="{tint(COL[int(grid[i, j])], 0.40)}"/>')
            j = k + 1
    assert bad_s == 0 and bad_u == 0, (bad_s, bad_u)
    n0, n2 = int((grid == 0).sum()), int((grid == 2).sum())
    o = cells
    o.append(P.axes(tk((0, 0.1, 0.2, 0.3)), tk((10, 15, 20, 25, 30)), "feedback delay τ (s)", f"position gain k{sub('p', s)} (s⁻²)",
                    ytx=14))
    tb, kb = boundary(KD)
    sel = (kb <= 33) & (tb <= 0.32)
    o.append(PM.poly(s, [(P.X(a), P.Y(b)) for a, b in zip(tb[sel][::40], kb[sel][::40])], I["primary"], "curve"))
    o.append(label(s, P.X(0.012), P.Y(12.5), f"stable fraction {float((grid == 0).mean()):.2f}", "label2", I["primary"]))
    o.append(label(s, P.X(0.215), P.Y(20.5), "analytic boundary,", "label2", I["primary"]))
    o.append(label(s, P.X(0.215), P.Y(20.5) + 15, "Proposition 4.2", "label2", I["primary"]))
    o.append(label(s, P.x1 - 4, P.Y(32), f"stable cells above the curve: {bad_s}", "label2", I["secondary"], "end"))
    o.append(label(s, P.x1 - 4, P.Y(32) + 15, f"unstable cells below it: {bad_u}", "label2", I["secondary"], "end"))
    o.append(swatch(s, 52, 296, SER[1], "decays"))
    o.append(swatch(s, 128, 296, SER[2], "marginal"))
    o.append(swatch(s, 214, 296, SER[0], "grows"))
    aria = ("Problem K2 plot: Lab B's classification of each simulated delay-gain point on a 40 by 30 grid, decays in blue, "
            f"marginal in orange, grows in red, with the analytic island boundary of Proposition 4.2 drawn over it. "
            f"{float((grid == 0).mean()):.2f} of the cells decay, all of them on the low-delay side of the curve; the "
            "orange marginal band straddles the curve and the red cells lie beyond it.")
    pts = []
    for t in np.linspace(float(np.interp(33, kb, tb)), 0.31, 90):
        pts.append([P.X(t), P.Y(min(kp_ceiling(float(t), KD), 33)), f"τ = {1000 * t:.0f} ms: analytic ceiling kp = {kp_ceiling(float(t), KD):.1f} s⁻²"])
    return svg(VB, aria, s, "".join(o), (P.box, pts))


def fig40():
    VB = (0, 0, W, 346)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (52, 40, 384, 232), (10, 60), (0, 15))
    kps, kds, S, best, ref, design = lab_k3()
    cut = (1.0, 2.0, 4.0)
    OPS = (0.80, 0.55, 0.32, 0.14)

    def band(v):
        if not math.isfinite(v):
            return 4
        return sum(v >= c for c in cut)

    cells = []
    for i, kp in enumerate(kps):
        j = 0
        while j < len(kds):
            k = j
            while k + 1 < len(kds) and band(S[i, k + 1]) == band(S[i, j]):
                k += 1
            b = band(S[i, j])
            x0, x1 = P.X(kp - 0.5), P.X(kp + 0.5)
            ya, yb = P.Y(kds[k] + 0.125), P.Y(kds[j] - 0.125)
            fill = f'fill="{tint(I["rule"], 0.22)}"' if b == 4 else f'fill="{tint(SER[1], OPS[b])}"'
            cells.append(f'<rect x="{x0 - 0.3:.2f}" y="{ya - 0.3:.2f}" width="{x1 - x0 + 0.6:.2f}" height="{yb - ya + 0.6:.2f}" {fill}/>')
            j = k + 1
    o = cells
    o.append(P.axes(tk((10, 20, 30, 40, 50, 60)), tk((0, 5, 10, 15)), f"position gain k{sub('p', s)} (s⁻²)",
                    f"damping gain k{sub('d', s)} (s⁻¹)", ytx=14))
    kd_line = np.arange(1.0, 14.01, 0.25)
    ce = [ceiling(float(k)) for k in kd_line]
    o.append(PM.poly(s, [(P.X(c), P.Y(k)) for c, k in zip(ce, kd_line)], I["primary"], "curve_multi"))
    o.append(P.dot(best[1], best[2], O["flag"]))
    o.append(hollow(s, P.X(20), P.Y(3), I["primary"]))
    o.append(label(s, P.X(best[1]) + 8, P.Y(best[2]) + 4, f"fastest: {best[0]:.2f} s", "label2", I["primary"]))
    o.append(label(s, P.X(best[1]) + 8, P.Y(best[2]) + 19, f"kp = {best[1]:g}, kd = {best[2]:g}", "label2", I["secondary"]))
    o.append(label(s, P.X(20) - 10, P.Y(3) - 27, "design", "label2", I["primary"]))
    o.append(label(s, P.X(20) - 10, P.Y(3) - 12, f"{design:.2f} s", "label2", I["primary"]))
    o.append(label(s, P.x1 - 4, P.Y(14.4), "island ceiling,", "label2", I["primary"], "end"))
    o.append(label(s, P.x1 - 4, P.Y(14.4) + 15, "τ = 100 ms", "label2", I["secondary"], "end"))
    c81 = ceiling(ref[2])
    o.append(label(s, P.x0 + 6, P.Y(14.2), f"kd = {ref[2]:.1f}: ceiling {c81:.1f}", "label2", I["secondary"]))
    names = ["< 1 s", "1–2 s", "2–4 s", "≥ 4 s"]
    x = 52
    for b in range(4):
        o.append(f'<rect x="{x}" y="{296 - 10}" width="14" height="11" fill="{SER[1]}" fill-opacity="{OPS[b]}"/>'
                 + label(s, x + 19, 296, names[b], "label2", I["secondary"]))
        x += 19 + 8 * len(names[b]) + 10
    o.append(f'<rect x="52" y="306" width="14" height="11" fill="{I["rule"]}" fill-opacity="0.22"/>'
             + label(s, 71, 316, "not settled (still ringing at 6 s)", "label2", I["secondary"]))
    o.append(label(s, 52, 336, "dot: fastest gains; ring: design gains (20, 3)", "label2", I["muted"]))
    aria = ("Problem K3 map: settling time of the delayed recovery over a grid of position gain kp from 12 to 45 and damping "
            f"gain kd from 1 to 14 at a delay of 100 milliseconds, darker meaning faster. The fastest cell, "
            f"{best[0]:.2f} seconds, is at kp = {best[1]:g}, kd = {best[2]:g}; the design gains 20 and 3 take {design:.2f}. "
            f"A curve marks the island ceiling, which at kd = {ref[2]:.1f} is kp = {c81:.1f}, so the optimum sits at about "
            "half the ceiling, well inside the island.")
    pts = []
    for i, kp in enumerate(kps):
        j = int(np.argmin(S[i]))
        pts.append([P.X(kp), P.Y(kds[j]), f"kp = {kp:g}: fastest at kd = {kds[j]:g}, settles in {S[i, j]:.2f} s"])
    return svg(VB, aria, s, "".join(o), (P.box, pts))


def sway(J, T=0.4, dt=0.002):
    """K4's lean trace after a push (lines 666-678): the delayed loop with the ankle saturated."""
    n, d = int(T / dt), int(round(0.10 / dt))
    th, om = np.zeros(n + 1), np.zeros(n + 1)
    om[0] = J / (M * ELL)
    for i in range(n):
        thd = th[i - d] if i - d >= 0 else 0.0
        omd = om[i - d] if i - d >= 0 else 0.0
        u = np.clip(-(KP * thd + KD * omd), -U_MAX, U_MAX)
        om[i + 1] = om[i] + dt * (W0 * W0 * th[i] + u)
        th[i + 1] = th[i] + dt * om[i + 1]
    return np.arange(n + 1) * dt, th


@lru_cache(maxsize=None)
def k4():
    t, th = sway(18.0)
    w = t <= 0.10
    clean = M * ELL * np.polyfit(t[w], th[w], 1)[0]
    rng = np.random.default_rng(3)
    stats, first = [], None
    for sd in (0.002, 0.005):
        e = []
        for _ in range(400):
            nz = rng.standard_normal(int(w.sum()))
            if sd == 0.005 and first is None:
                first = nz.copy()
            e.append(M * ELL * np.polyfit(t[w], th[w] + sd * nz, 1)[0])
        stats.append((float(np.mean(e)), float(np.std(e))))
    assert round(float(clean), 1) == 18.3 and [(round(a, 1), round(b, 1)) for a, b in stats] == [(18.3, 0.7), (18.3, 1.6)]
    return t, th, w, float(clean), stats, first


def fig42():
    VB = (0, 0, W, 332)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (56, 40, 384, 232), (0, 0.4), (0, 100))
    t, th, w, clean, stats, nz = k4()
    sd = 0.005
    obs = th[w] + sd * nz
    b, a = np.polyfit(t[w], obs, 1)
    jhat = M * ELL * b
    o = [f'<rect x="{P.X(0):.2f}" y="{P.y1:.2f}" width="{P.X(0.1) - P.X(0):.2f}" height="{P.y0 - P.y1:.2f}" fill="{BOX}"/>']
    o.append(P.axes(tk((0, 0.1, 0.2, 0.3, 0.4)), tk((0, 25, 50, 75, 100)), "time (s)", "lean θ (mrad)", grid=(25, 50, 75, 100),
                    ytx=14))
    o.append(P.curve(t, 1000 * th, I["primary"], dash=None))
    for x, y in zip(t[w], obs):
        o.append(f'<circle cx="{P.X(x):.2f}" cy="{P.Y(1000 * y):.2f}" r="{s(2.2):.2f}" fill="{SER[1]}" fill-opacity="0.8"/>')
    tl = np.array([0.0, 0.22])
    o.append(P.curve(tl, 1000 * (a + b * tl), SER[0], multi=True, dash=PM.DASH_SER))
    o.append(label(s, P.X(0.006), P.Y(94), "fit window 0–100 ms", "label2", I["secondary"]))
    o.append(label(s, P.X(0.006), P.Y(94) + 15, "(51 samples)", "label2", I["secondary"]))
    y0 = P.Y(29)
    o.append(label(s, P.X(0.17), y0, "Ĵ over 400 trials (true 18):", "label2", I["primary"]))
    o.append(label(s, P.X(0.17), y0 + 15, f"clean trace {clean:.1f}", "label2", I["secondary"]))
    o.append(label(s, P.X(0.17), y0 + 30, f"2 mrad noise {stats[0][0]:.1f} ± {stats[0][1]:.1f}", "label2", I["secondary"]))
    o.append(label(s, P.X(0.17), y0 + 45, f"5 mrad noise {stats[1][0]:.1f} ± {stats[1][1]:.1f}", "label2", I["secondary"]))
    o.append(legend(s, 56, 296, [(I["primary"], "clean trace", None)]))
    o.append(f'<circle cx="{56 + 120:.2f}" cy="{296 - 4.5:.2f}" r="{s(2.2):.2f}" fill="{SER[1]}"/>'
             + label(s, 56 + 130, 296, "noisy samples, 5 mrad", "label2", I["secondary"]))
    o.append(legend(s, 56, 316, [(SER[0], f"line fitted to the window: slope gives Ĵ = {jhat:.1f}", PM.DASH_SER)]))
    aria = ("Problem K4 plot: the lean trace after a push of 18 newton seconds, rising to about 86 milliradians in 0.4 seconds, "
            "with the first 100 milliseconds shaded as the fit window. Noisy samples at 5 milliradians scatter about the "
            f"start of the trace and a dashed fitted line gives this trial an impulse estimate of {jhat:.1f}. Over 400 "
            f"trials the estimate is {stats[0][0]:.1f} plus or minus {stats[0][1]:.1f} at 2 milliradians of noise and "
            f"{stats[1][0]:.1f} plus or minus {stats[1][1]:.1f} at 5.")
    hv = [[P.X(x), P.Y(1000 * y), f"t = {1000 * x:.0f} ms: θ = {1000 * y:.1f} mrad"] for x, y in zip(t, th)]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


def fig44():
    VB = (0, 0, W, 328)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (56, 40, 384, 232), (0, 8), (-0.3, 0.3))
    t, xt, z, pred, raw, prd, d = lab_c()
    er, ep = z[d:] - xt[d:], pred[d:] - xt[d:]
    assert abs(math.sqrt(float(np.mean(er ** 2))) - raw) < 1e-9 and abs(math.sqrt(float(np.mean(ep ** 2))) - prd) < 1e-9
    ratio = prd / raw
    assert round(ratio, 2) == 0.45
    o = [P.axes(tk((0, 2, 4, 6, 8)), tk((-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3), "{:g}"), "time (s)", "estimate − true θ (rad)",
                grid=(-0.2, -0.1, 0.1, 0.2), ytx=14)]
    o.append(H.line(s, P.x0, P.Y(0), P.x1, P.Y(0), I["rule"], "ref"))
    o.append(P.curve(t[d::2], er[::2], SER[1], multi=True, nmax=400))
    o.append(P.curve(t[d::2], ep[::2], SER[0], multi=False, nmax=400))
    o.append(label(s, P.x1 - 4, P.Y(0.27), f"RMS {prd:.3f} / {raw:.3f} = {ratio:.2f}: less than half", "label2",
                   I["primary"], "end"))
    o.append(legend(s, 56, 296, [(SER[1], f"raw delayed measurement, RMS {raw:.3f} rad", None)]))
    o.append(legend(s, 56, 316, [(SER[0], f"Kalman filter + predictor, RMS {prd:.3f} rad", None)]))
    aria = ("Problem K5 plot: the state-estimate error over 8 seconds of Lab C's simulated sway. The raw delayed measurement's "
            f"error is wide, RMS {raw:.3f} radians; the error of the Kalman filter plus predictor stays close to zero, "
            f"RMS {prd:.3f}, {ratio:.2f} of the raw value, less than half.")
    hv = [[P.X(t[i]), [P.Y(z[i] - xt[i]), P.Y(pred[i] - xt[i])],
           f"t = {t[i]:.2f} s: raw error {mn(z[i] - xt[i], '{:.3f}')}, predictor error {mn(pred[i] - xt[i], '{:.3f}')} rad"]
          for i in range(d, len(t), 4)]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


def rms_q(kp, kref):
    """K6: RMS sway with q(kp) = q0 (1 + (kp/kref)^2), in degrees."""
    return math.degrees(math.sqrt(Q0 * (1 + (kp / kref) ** 2) / (2.0 * (kp - W0 * W0) * KD)))


def fig45():
    VB = (0, 0, W, 344)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (56, 40, 384, 232), (10, 40), (0, 2))
    ks = np.linspace(10.0, 40.0, 301)[1:]
    ceil = kp_ceiling(0.10, KD)
    kopt = {kr: W0 * W0 + math.sqrt(W0 ** 4 + kr ** 2) for kr in (6.0, 8.0, 20.0)}
    assert round(kopt[8.0], 2) == 22.11 and round(rms_q(kopt[8.0], 8.0), 3) == 0.912
    assert [round(kopt[k], 1) for k in (6.0, 8.0, 20.0)] == [20.9, 22.1, 31.8]
    kr_cross = math.sqrt((ceil - W0 * W0) ** 2 - W0 ** 4)                         # kp* = ceiling
    assert round(ceil, 1) == 27.8 and 15.4 <= round(kr_cross, 1) <= 15.5      # line 697 prints 15.4; exact is 15.47
    o = [P.axes(tk((10, 15, 20, 25, 30, 35, 40)), tk((0, 0.5, 1.0, 1.5, 2.0), "{:g}"), f"position gain k{sub('p', s)} (s⁻²)",
                "RMS sway (deg)", grid=(0.5, 1.0, 1.5, 2.0), ytx=14)]
    o.append(vref(s, P, ceil, I["primary"]))
    sg = np.array([sigma_deg(k) for k in ks])
    m0 = sg <= 2.0
    o.append(P.curve(ks[m0], sg[m0], I["rule"], multi=True, dash=PM.DASH_SER))
    cols = {6.0: SER[2], 8.0: SER[0], 20.0: SER[1]}
    series = {}
    for kr, col in cols.items():
        y = np.array([rms_q(k, kr) for k in ks])
        m = y <= 2.0
        series[kr] = y
        o.append(P.curve(ks[m], y[m], col, multi=(kr != 8.0)))
    for kr, col in cols.items():
        k = kopt[kr]
        o.append(hollow(s, P.X(k), P.Y(rms_q(k, kr)), col) if k > ceil else P.dot(k, rms_q(k, kr), col))
    o.append(label(s, P.X(ceil) + 6, P.Y(1.95), "island ceiling,", "label2", I["primary"]))
    o.append(label(s, P.X(ceil) + 6, P.Y(1.95) + 15, f"τ = 100 ms: {ceil:.1f}", "label2", I["secondary"]))
    o.append(label(s, P.X(kopt[8.0]) - 30, P.Y(rms_q(kopt[8.0], 8.0)) - 11, f"{kopt[8.0]:.2f}, {rms_q(kopt[8.0], 8.0):.3f}°",
                   "label2", I["primary"]))
    o.append(label(s, P.X(ceil) + 5, P.Y(0.60), f"{kopt[20.0]:.1f}: beyond the ceiling", "label2", I["primary"]))
    o.append(label(s, P.X(kopt[6.0]), P.Y(rms_q(kopt[6.0], 6.0)) - 9, f"{kopt[6.0]:.1f}", "label2", I["primary"], "middle"))
    o.append(legend(s, 56, 296, [(SER[2], f"k{sub('ref', s, 'label2')} = 6", None), (SER[0], "8", None), (SER[1], "20 s⁻²", None)]))
    o.append(legend(s, 56, 316, [(I["rule"], "constant q", PM.DASH_SER)]))
    o.append(label(s, 56, 336, "dots: minima; ring: beyond the ceiling", "label2", I["muted"]))
    aria = ("Problem K6 plot: RMS sway against position gain when motor noise grows with the command. Curves for kref = 6, 8 "
            "and 20 per second squared each have an interior minimum, marked: 20.9, 22.11 with 0.912 degrees, and 31.8, "
            f"while a grey dashed constant-noise curve only falls. A vertical line marks the island ceiling at {ceil:.1f} "
            "for a 100 millisecond delay; the minimum for kref = 20 lies beyond it, and the minimum reaches the ceiling "
            f"at kref = {kr_cross:.1f}.")
    hv = [[P.X(ks[i]), [P.Y(series[kr][i]) for kr in cols if series[kr][i] <= 2.0],
           f"kp = {ks[i]:.1f}: RMS {series[6.0][i]:.2f}, {series[8.0][i]:.2f}, {series[20.0][i]:.2f} deg (kref = 6, 8, 20)"]
          for i in range(len(ks)) if series[6.0][i] <= 2.0 and series[8.0][i] <= 2.0 and series[20.0][i] <= 2.0]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


def tau_c_text(kp, w0):
    """K7's tau_c (lines 725-734), unchanged."""
    om = np.linspace(1e-3, 40.0, 400000)
    sn = KD * om / (om ** 2 + w0 ** 2)
    ok = sn <= 1.0
    u = np.arcsin(sn[ok])
    kpb = (om[ok] ** 2 + w0 ** 2) * np.cos(u)
    tt = u / om[ok]
    order = np.argsort(kpb)
    return float(np.interp(kp, kpb[order], tt[order]))


def axes_one(s, P, xt, yt, xtitle, ytitle=None, ytx=14, grid=()):
    o = []
    for g in grid:
        o.append(H.line(s, P.x0, P.Y(g), P.x1, P.Y(g), GRID, "leader"))
    o.append(H.line(s, P.x0, P.y0, P.x1, P.y0, I["axis"], "axis"))
    o.append(H.line(s, P.x0, P.y0, P.x0, P.y1, I["axis"], "axis"))
    for v, tx in yt:
        o.append(H.line(s, P.x0 - 5, P.Y(v), P.x0, P.Y(v), I["axis"], "leader"))
        o.append(label(s, P.x0 - 8, P.Y(v) + 4.5, tx, "tick", I["secondary"], "end"))
    for v, tx in xt:
        o.append(H.line(s, P.X(v), P.y0, P.X(v), P.y0 + 5, I["axis"], "leader"))
        o.append(label(s, P.X(v), P.y0 + 19, tx, "tick", I["secondary"], "middle"))
    if xtitle:
        o.append(label(s, (P.x0 + P.x1) / 2, P.y0 + 40, xtitle, "label", I["primary"], "middle"))
    if ytitle:
        yc = (P.y0 + P.y1) / 2
        o.append(label(s, ytx, yc, ytitle, "label", I["primary"], "middle", f'transform="rotate(-90 {ytx} {yc:.2f})"'))
    return "".join(o)


def fig47():
    VB = (0, 0, W, 296)
    s = H.Scale(W, VB[3], display_w=400)
    P1 = Plot(s, (52, 56, 196, 232), (10, 32), (0, 250))
    P2 = Plot(s, (254, 56, 386, 232), (0.6, 1.5), (0, 250))
    yt = tk((0, 50, 100, 150, 200, 250))
    kv = np.linspace(11.0, 31.0, 81)
    t1 = np.array([1000 * tau_c_text(float(k), W0) for k in kv])
    lv = np.linspace(0.6, 1.5, 61)
    t2 = np.array([1000 * tau_c_text(KP, math.sqrt(G / float(l))) for l in lv])
    pk = {k: 1000 * tau_c_text(k, W0) for k in (14.0, 20.0, 28.0)}
    pl = {l: 1000 * tau_c_text(KP, math.sqrt(G / l)) for l in (0.8, 1.0, 1.3)}
    assert [round(v) for v in pk.values()] == [197, 137, 99] and (round(pl[0.8]), round(pl[1.3])) == (140, 135)
    o = [axes_one(s, P1, tk((10, 15, 20, 25, 30)), yt, f"position gain k{sub('p', s)} (s⁻²)", "critical delay τc (ms)",
                  grid=(50, 100, 150, 200, 250))]
    o.append(axes_one(s, P2, tk((0.8, 1.0, 1.2, 1.4), "{:g}"), yt, "COM height ℓ (m)", None, grid=(50, 100, 150, 200, 250)))
    o.append(P1.curve(kv, t1, SER[1], multi=False))
    o.append(P2.curve(lv, t2, SER[1], multi=False))
    for k, v in pk.items():
        o.append(P1.dot(k, v, SER[1]))
        o.append(label(s, P1.X(k) + 6, P1.Y(v) - 8, f"{v:.0f}", "label2", I["primary"]))
    for l, v in pl.items():
        o.append(P2.dot(l, v, SER[1]))
        o.append(label(s, P2.X(l), P2.Y(v) - 10, f"{v:.0f}", "label2", I["primary"], "middle"))
    o.append(label(s, P1.x0, 40, "gain: τc halves", "label", I["primary"]))
    o.append(label(s, P2.x0 - 12, 40, "height: barely moves", "label", I["primary"]))
    aria = ("Problem K7 plot, two panels with the same vertical axis: the critical delay in milliseconds. Left, against "
            "position gain it falls from 197 at 14 to 137 at 20 and 99 at 28 per second squared. Right, against COM height "
            "from 0.6 to 1.5 metres at gain 20 it barely moves: 140 at 0.8, 138 at 1.0 and 135 at 1.3 metres.")
    h1 = [[P1.X(k), P1.Y(v), f"kp = {k:.1f}: τc = {v:.0f} ms"] for k, v in zip(kv, t1)]
    h2 = [[P2.X(l), P2.Y(v), f"ℓ = {l:.2f} m: τc = {v:.0f} ms"] for l, v in zip(lv, t2)]
    return H.svg_open(VB, html.escape(aria), s, extra=H.hover_attr([(P1.box, h1), (P2.box, h2)])) + "".join(o) + "</svg>"


def fig49():
    VB = (0, 0, W, 308)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (56, 40, 384, 232), (-0.06, 0.20), (-0.1, 1.2))
    J = 40.0
    xi0 = J / (M * W0)
    xs = {k: xi0 * math.exp(W0 * (v["tau"] + v["t_move"])) for k, v in (("young", YOUNG), ("aged", AGED))}
    win = YOUNG["l_step"] - xs["young"]
    assert round(xs["young"], 3) == 0.467 and round(win, 3) == 0.133 and round(xs["aged"], 3) == 0.868
    assert AGED["l_step"] - xs["aged"] < 0
    jc = (j_crit(**YOUNG), j_crit(**AGED))
    assert [round(v, 1) for v in jc] == [51.4, 19.3]
    e = np.linspace(-0.06, 0.20, 521)
    cap = ((e >= 0) & (e <= win)).astype(float)
    o = [f'<rect x="{P.X(0):.2f}" y="{P.y1:.2f}" width="{P.X(win) - P.X(0):.2f}" height="{P.y0 - P.y1:.2f}" fill="{SER[1]}" fill-opacity="0.12"/>']
    o.append(P.axes(tk((-0.05, 0, 0.05, 0.1, 0.15, 0.2), "{:g}"), tk((0, 1)), "foot-placement error e (m)", "capture (1 = yes)",
                    ytx=14))
    pts = [(-0.06, 0), (0, 0), (0, 1), (win, 1), (win, 0), (0.20, 0)]
    o.append(PM.poly(s, [(P.X(a), P.Y(b)) for a, b in pts], SER[1], "curve"))
    o.append(label(s, P.X(win / 2), P.Y(1) - 9, f"window 0 ≤ e ≤ {win:.3f} m", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(-0.056), P.Y(0.5), "undershoot:", "label2", I["secondary"]))
    o.append(label(s, P.X(-0.056), P.Y(0.5) + 15, "body keeps", "label2", I["secondary"]))
    o.append(label(s, P.X(-0.056), P.Y(0.5) + 30, "diverging", "label2", I["secondary"]))
    o.append(label(s, P.X(win) + 7, P.Y(0.5), "beyond", "label2", I["secondary"]))
    o.append(label(s, P.X(win) + 7, P.Y(0.5) + 15, "the leg's", "label2", I["secondary"]))
    o.append(label(s, P.X(win) + 7, P.Y(0.5) + 30, "reach", "label2", I["secondary"]))
    cx = P.X(win / 2)
    for k, (txt, col) in enumerate([(f"young: ξ{sub('s', s, 'label2')} = {xs['young']:.3f} m", I["primary"]),
                                    ("reach 0.60 m", I["secondary"]),
                                    ("aged, same push:", I["primary"]),
                                    (f"ξ{sub('s', s, 'label2')} = {xs['aged']:.3f} m > 0.42 m", I["primary"]),
                                    ("window empty", I["secondary"])]):
        o.append(label(s, cx, P.Y(0.78) + 16 * k, txt, "label2", col, "middle"))
    o.append(label(s, 56, 296, f"push J = 40 N s; J{sub('crit', s, 'label2')} = {jc[0]:.1f} (young), {jc[1]:.1f} (aged) N s",
                   "label2", I["muted"]))
    aria = ("Problem K8 plot: capture against foot-placement error e after a 40 newton second push, for the young parameter set. "
            f"Capture is 1 only in the shaded window from e = 0 to {win:.3f} metres: any undershoot leaves the extrapolated "
            f"centre of mass ahead of the new pivot, and beyond {win:.3f} the foot is out of reach. For the aged set the "
            f"same push puts the extrapolated COM at {xs['aged']:.3f} metres, past a reach of 0.42, so the window is empty.")
    ee = np.linspace(-0.06, 0.20, 90)
    hv = [[P.X(x), P.Y(1.0 if 0 <= x <= win else 0.0),
           f"e = {mn(x, '{:.3f}')} m: " + ("captured" if 0 <= x <= win else ("undershoot, not captured" if x < 0 else "beyond reach, not captured"))]
          for x in ee]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


def fig51():
    VB = (0, 0, W, 322)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (52, 40, 392, 232), (0, 5), (0, 60))
    jy = j_crit(**YOUNG)
    sets = [("young", "", jy, SER[1]),
            ("delay", "only", j_crit(**dict(YOUNG, tau=AGED["tau"])), SER[2]),
            ("travel", "only", j_crit(**dict(YOUNG, t_move=AGED["t_move"])), SER[2]),
            ("reach", "only", j_crit(**dict(YOUNG, l_step=AGED["l_step"])), SER[2]),
            ("aged", "all three", j_crit(**AGED), SER[0])]
    vals = [v for _, _, v, _ in sets]
    assert [round(v) for v in vals] == [51, 40, 35, 36, 19]                       # K9 / line 760
    ratios = [v / jy for v in vals[1:4]]
    prod = ratios[0] * ratios[1] * ratios[2]
    assert abs(prod * jy - vals[4]) < 1e-9
    additive = jy - sum(jy - v for v in vals[1:4])
    o = [axes_one(s, P, [], tk((0, 20, 40, 60)), None, "critical impulse (N s)", grid=(20, 40, 60))]
    bw = 0.62
    for k, (n1, n2, v, col) in enumerate(sets):
        xc = k + 0.5
        o.append(f'<rect x="{P.X(xc - bw / 2):.2f}" y="{P.Y(v):.2f}" width="{P.X(xc + bw / 2) - P.X(xc - bw / 2):.2f}" '
                 f'height="{P.y0 - P.Y(v):.2f}" fill="{col}" fill-opacity="0.75"/>')
        o.append(label(s, P.X(xc), P.Y(v) - 6, f"{v:.1f}", "label2", I["primary"], "middle"))
        o.append(label(s, P.X(xc), P.y0 + 17, n1, "tick", I["secondary"], "middle"))
        if n2:
            o.append(label(s, P.X(xc), P.y0 + 31, n2, "tick", I["secondary"], "middle"))
    xt = P.X(1.95)
    o.append(label(s, xt, P.Y(58), "ratios to young:", "label2", I["primary"]))
    o.append(label(s, xt, P.Y(58) + 15, f"{ratios[0]:.3f} × {ratios[1]:.3f} × {ratios[2]:.3f}", "label2", I["primary"]))
    o.append(label(s, xt, P.Y(58) + 30, f"= {prod:.3f}: {prod * jy:.1f} N s", "label2", I["primary"]))
    o.append(label(s, xt, P.Y(58) + 45, f"adding the losses: {additive:.1f}", "label2", I["secondary"]))
    o.append(label(s, 52, 296, "delay τ 0.10 → 0.18 s; travel: foot-travel time 0.20 → 0.32 s;", "label2", I["muted"]))
    o.append(label(s, 52, 311, "reach: step length 0.60 → 0.42 m", "label2", I["muted"]))
    aria = ("Problem K9 bar chart of the critical impulse in newton seconds: 51.4 for the young parameter set; 40.1, 35.4 and "
            "36.0 when only the delay, only the foot-travel time or only the step reach is drifted to its aged value; and "
            f"19.3 with all three. The three single-drift ratios {ratios[0]:.3f}, {ratios[1]:.3f} and {ratios[2]:.3f} "
            f"multiply to {prod:.3f}; adding the three losses would instead give {additive:.1f}.")
    hv = [[P.X(k + 0.5), P.Y(v), f"{(n1 + ' ' + n2).strip()}: Jcrit = {v:.1f} N s"] for k, (n1, n2, v, _) in enumerate(sets)]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


def fig52():
    VB = (0, 0, W, 324)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (56, 40, 384, 232), (0, 0.4), (0, 0.8))
    mu_req, dts = 0.20, 0.25
    vmax = {k: W0 * v["l_step"] * math.exp(-W0 * (v["tau"] + v["t_move"])) for k, v in (("young", YOUNG), ("aged", AGED))}
    vs = lambda mu: max(0.0, mu_req - mu) * G * dts                              # noqa: E731
    surf = [("dry", 0.30), ("wet tile", 0.15), ("ice", 0.08)]
    assert [round(vs(m), 2) for _, m in surf] == [0.0, 0.12, 0.29]
    assert (round(vmax["young"], 2), round(vmax["aged"], 2)) == (0.73, 0.28)
    assert round(vmax["aged"] - vs(0.08), 3) == -0.018                           # the aged walker misses by 1.8 cm/s
    mu_x = mu_req - vmax["aged"] / (G * dts)
    o = [P.axes(tk((0, 0.1, 0.2, 0.3, 0.4), "{:g}"), tk((0, 0.2, 0.4, 0.6, 0.8), "{:g}"), "available friction μ",
                "COM speed gained while sliding (m s⁻¹)", grid=(0.2, 0.4, 0.6, 0.8), ytx=14)]
    o.append(href(s, P, vmax["young"], SER[1]))
    o.append(href(s, P, vmax["aged"], SER[0]))
    o.append(PM.poly(s, [(P.X(0), P.Y(vs(0))), (P.X(mu_req), P.Y(0)), (P.X(0.4), P.Y(0))], I["primary"], "curve"))
    o.append(hollow(s, P.X(mu_x), P.Y(vmax["aged"]), O["flag"]))
    for nm, mu in surf:
        o.append(P.dot(mu, vs(mu), I["primary"]))
    o.append(label(s, P.X(0.30), P.Y(0) - 10, "dry 0.30", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(0.15) + 8, P.Y(vs(0.15)) - 7, "wet tile 0.15", "label2", I["primary"]))
    o.append(label(s, P.X(0.08) + 8, P.Y(vs(0.08)) - 9, "ice 0.08", "label2", I["primary"]))
    o.append(label(s, P.x1 - 4, P.Y(vmax["young"]) - 6, f"young walker can catch {vmax['young']:.2f}", "label2", I["primary"], "end"))
    o.append(label(s, P.x1 - 4, P.Y(vmax["aged"]) - 6, f"aged {vmax['aged']:.2f}", "label2", I["primary"], "end"))
    o.append(label(s, P.x1 - 4, P.Y(vmax["aged"]) + 16, f"aged falls for μ < {mu_x:.3f}", "label2", I["secondary"], "end"))
    o.append(legend(s, 56, 296, [(I["primary"], f"slide speed (μ{sub('req', s, 'label2')} − μ) g Δt", None)]))
    o.append(legend(s, 56, 316, [(SER[1], "young ceiling", H.DASH_REF), (SER[0], "aged ceiling", H.DASH_REF)]))
    aria = ("Problem K10 plot: the COM speed gained while the foot slides, (0.20 minus mu) g times 0.25 seconds, against the "
            "available friction mu, falling to zero at mu = 0.20. Two dashed ceilings show the speed a capture step can "
            f"still absorb: {vmax['young']:.2f} metres per second for the young parameter set and {vmax['aged']:.2f} for the "
            f"aged. Dry floor, wet tile and ice sit at mu 0.30, 0.15 and 0.08: ice gives 0.29, above the aged ceiling by "
            f"1.8 centimetres per second, and the aged walker falls for any mu below {mu_x:.3f}.")
    mus = np.linspace(0, 0.4, 81)
    hv = [[P.X(m), P.Y(vs(m)), f"μ = {m:.2f}: slide speed {vs(m):.3f} m/s; aged margin {vmax['aged'] - vs(m):+.3f} m/s"] for m in mus]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


FIGS = {
    5: (r"Two phase portraits in the sway-angle plane theta versus the", fig5),
    7: (r"Left, the stability island in the delay-gain plane: a bounda", fig7),
    8: (r"Left, a simulated quiet-standing sway trace: the angle wande", fig8),
    9: (r"Left, two Gaussian bumps - a broad model prediction and a no", fig9),
    12: (r"Left, the stability island for a young parameter set and a s", fig12),
    14: (r"The largest arrestable push impulse starts at the impulse-mo", fig14),
    38: (r"K1: Simulate the delayed closed loop after a push and find, ", fig38),
    39: (r"K2: Map the delay-gain plane by classifying each simulated t", fig39),
    40: (r"K3: Within the stability island at $\tau=100\ \mathrm{ms}$, ", fig40),
    42: (r"K4: Given only an observed sway trace following an unknown p", fig42),
    44: (r"K5: Close the loop with a Kalman filter plus predictor and c", fig44),
    45: (r"K6: With signal-dependent motor noise $q(k_p)=q_0\big(1+(k_p", fig45),
    47: (r"K7: Sweep the critical delay against the position gain and t", fig47),
    49: (r"K8: After a push that requires a step, sweep the foot-placem", fig49),
    51: (r"K9: Sweep the four aging parameters and compute the critical", fig51),
    52: (r"K10: Compare slip outcomes across available friction and rea", fig52),
}
