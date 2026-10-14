"""Module 4 problem-set plots (C7, D4-D7, D9, K1, K2, K4-K10): house-style redraws at 400 px.

Every plotted number is computed here: the D/C figures from the formula the problem or its solution
states, the K figures from the K-solution script in module04.html (ported line for line; its printed
numbers are asserted). One-sided drainage throughout: lambda_n = (2n+1) pi/2, T = D t / h^2.
"""
import html
import math
from functools import lru_cache

import numpy as np

import house as H
from m05.plots_prob import Plot, hov, label, legend, sub, svg

O, I, SER = H.OVERLAY, H.INK, H.SERIES
W = 400                     # viewBox width = rendered width, so 1 user unit = 1 px
LOG_T = [(-1, "0.1"), (0, "1"), (1, "10"), (2, "10²"), (3, "10³"), (4, "10⁴"), (5, "10⁵")]


def sup(t, s, size="label"):
    """Superscript tspan (no literal ^ in svg text)."""
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def svg_panels(vb, aria, s, body, panels):
    return H.svg_open(vb, html.escape(aria), s, extra=H.hover_attr(panels)) + body + "</svg>"


def ref(s, P, y=None, x=None, col=I["primary"]):
    """Dashed reference line across the plot box (horizontal at data y, or vertical at data x)."""
    if y is not None:
        return H.line(s, P.x0, P.Y(y), P.x1, P.Y(y), col, "ref", H.DASH_REF)
    return H.line(s, P.X(x), P.y0, P.X(x), P.y1, col, "ref", H.DASH_REF)


# ---------------------------------------------------------------- module models
LAM = (2 * np.arange(2000) + 1) * np.pi / 2           # K1 / K5 / K7: lambda_n, 2000 terms


def F_of_T(T):
    """Fluid load support F(T) = sum 2/lambda_n^2 exp(-lambda_n^2 T) (D5, K1, K5)."""
    T = np.atleast_1d(np.asarray(T, float))
    return (2 / LAM**2 * np.exp(-np.outer(T, LAM**2))).sum(axis=1)


def creep_frac(T):
    """K7: eps/eps_inf = 1 - sum 8/((2n+1)^2 pi^2) exp(-lambda_n^2 T)."""
    n = np.arange(2000)
    T = np.atleast_1d(np.asarray(T, float))
    return 1 - (8 / ((2 * n + 1)**2 * np.pi**2) * np.exp(-np.outer(T, LAM**2))).sum(axis=1)


RG_THETA, C0 = 8.314 * 310, 0.15                      # K2 / K10: J/mol, mol/L


def donnan(cF):
    """K2 / K10: pi(cF) in Pa."""
    return RG_THETA * (np.sqrt(np.asarray(cF)**2 + 4 * C0**2) - 2 * C0) * 1e3


H5, HA5, K5 = 2e-3, 0.6e6, 1e-15                      # K5 / K6 / K7 healthy plug
D5 = HA5 * K5


# ---------------------------------------------------------------- #34 C7: relaxation and creep
def fig34():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (50, 52, 186, 226), (0, 2), (0, 2.2))
    Q = Plot(s, (252, 52, 388, 226), (0, 2), (0, 1.1))
    T = np.linspace(0, 2, 201)
    sr = 1 + F_of_T(T)                 # K4: sigma = HA eps0 (1 + <p>), <p> = F(T)
    cr = creep_frac(T)                 # K7 series
    o = [P.axes([(0, "0"), (1, "1"), (2, "2")], [(0, "0"), (1, "1"), (2, "2")], "time t/τ",
                "stress / drained value")]
    o.append(Q.axes([(0, "0"), (1, "1"), (2, "2")], [(0, "0"), (0.5, "0.5"), (1, "1")], "time t/τ",
                    "strain / drained value", ytx=Q.x0 - 40))
    o.append(label(s, (P.x0 + P.x1) / 2, 18, "relaxation", "label", I["primary"], "middle"))
    o.append(label(s, (P.x0 + P.x1) / 2, 36, "fixed strain", "label2", I["secondary"], "middle"))
    o.append(label(s, (Q.x0 + Q.x1) / 2, 18, "creep", "label", I["primary"], "middle"))
    o.append(label(s, (Q.x0 + Q.x1) / 2, 36, "fixed load", "label2", I["secondary"], "middle"))
    o.append(ref(s, P, y=1))
    o.append(ref(s, Q, y=1))
    o.append(P.curve(T, sr, SER[0]))
    o.append(Q.curve(T, cr, SER[1]))
    o.append(P.dot(0, sr[0], SER[0]))
    o.append(Q.dot(0, cr[0], SER[1]))
    o.append(label(s, P.X(0.14), P.Y(2.0) + 5, f"undrained peak 2σ{sub('∞', s, 'label2')}", "label2"))
    o.append(label(s, P.x1, P.Y(1) + 16, f"σ{sub('∞', s, 'label2')} = H{sub('A', s, 'label2')}ε",
                   "label2", I["primary"], "end"))
    o.append(label(s, Q.x1, Q.Y(1) - 10, f"ε{sub('∞', s, 'label2')} = σ/H{sub('A', s, 'label2')}",
                   "label2", I["primary"], "end"))
    o.append(label(s, Q.X(0.12), Q.Y(0) - 7, "ε(0) = 0, undrained", "label2", I["secondary"]))
    aria = ("Problem C7 plot, two panels on the same time axis t over tau, 0 to 2. Left, relaxation at fixed "
            "strain: the stress starts at twice its drained value, the undrained peak, and decays to sigma-infinity "
            "= HA epsilon. Right, creep at fixed load: the strain starts at zero, because the undrained mixture is "
            "rigid, and rises to epsilon-infinity = sigma/HA. One drainage series over one gel time drives both.")
    hv1 = hov(P, T, [sr], lambda i: f"t/τ = {T[i]:.2f}: σ/σ∞ = {sr[i]:.3f}")
    hv2 = hov(Q, T, [cr], lambda i: f"t/τ = {T[i]:.2f}: ε/ε∞ = {cr[i]:.3f}")
    return svg_panels(VB, aria, s, "".join(o), [(P.box, hv1), (Q.box, hv2)])


# ---------------------------------------------------------------- #41 D4: the square-root law
def fig41():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 62, 388, 226), (0, 0.75), (0, 1.05))
    x = np.linspace(0, 0.75, 151)                     # x = sqrt(T)
    ex = F_of_T(x**2)
    ap = 1 - 2 * x / math.sqrt(math.pi)              # D4: F = 1 - 2 sqrt(T/pi)
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75)], [(0, "0"), (0.5, "0.5"), (1, "1")],
                "√T, with T = Dt/h²", "fluid support F", grid=(0.5,))]
    o.append(P.curve(x, ap, SER[1], multi=True, dash=(6, 4)))
    o.append(P.curve(x, ex, SER[0], multi=True))
    o.append(legend(s, 58, 20, [(SER[0], "exact series", None), (SER[1], "short-time law 1 − 2√(T/π)", (6, 4))]))
    o.append(label(s, P.X(0.75), P.Y(float(ex[x >= 0.57].max())) - 8, "exact series", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.57), P.Y(float(np.interp(0.57, x, ap))) + 16, "1 − 2√(T/π)", "label2", I["primary"],
                   "end"))
    o.append(label(s, P.X(0.2), P.Y(0.98), "the two agree at short time", "label2", I["secondary"]))
    o.append(H.line(s, P.X(0.2) + 4, P.Y(0.98) + 4, P.X(0.13) + 2, P.Y(float(np.interp(0.13, x, ex))) - 3,
                    I["secondary"], "leader"))
    aria = ("Problem D4 plot: fluid load support F against the square root of T = D t / h squared, from 0 to 0.75. "
            "The exact series and the straight short-time law F = 1 minus 2 root(T/pi) start together at F = 1 and "
            "coincide while root T is small; they part only beyond root T of about 0.5, where the exact curve "
            "stays slightly above the line.")
    hv = hov(P, x, [ex, ap], lambda i: f"√T = {x[i]:.3f}: exact {ex[i]:.4f}, 1 − 2√(T/π) = {ap[i]:.4f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #42 D5: the cosine modes
def fig42():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 62, 388, 226), (0, 1), (-1.15, 1.15))
    z = np.linspace(0, 1, 201)
    lam = [(2 * n + 1) * math.pi / 2 for n in range(3)]
    modes = [np.cos(lv * z) for lv in lam]           # D5: Z = cos(mu z), mu_n h = (2n+1) pi/2
    o = [P.axes([(0, "0"), (0.5, "0.5"), (1, "1")], [(-1, "−1"), (0, "0"), (1, "1")],
                "depth z/h  (0 = sealed base, 1 = drained)", "mode shape Z", grid=(0,))]
    for n in (2, 1, 0):
        o.append(P.curve(z, modes[n], SER[n], multi=True))
    o.append(legend(s, 58, 20, [(SER[n], f"n = {n}", None) for n in range(3)]))
    o.append(label(s, 58, 40, f"λ{sub('n', s, 'label2')} = (2n + 1)π/2; mode n decays as exp(−λ"
                   f"{sub('n', s, 'label2')}²T)", "label2", I["secondary"]))
    o.append(label(s, P.X(0.27), P.Y(1.0) - 6, "n = 0: λ₀ = π/2, slowest", "label2"))
    o.append(label(s, P.X(0.8), P.Y(1.0) - 6, "n = 2", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(0.865), P.Y(-0.93), "n = 1", "label2"))
    aria = ("Problem D5 plot: the first three cosine eigenmodes Z = cos(lambda_n z/h) of one-sided drainage, against "
            "depth from the sealed base (0) to the drained face (1), with lambda_n = (2n+1) pi/2. All three equal 1 "
            "at the sealed base and 0 at the drained face; n = 0 falls monotonically and is the slowest mode, which "
            "sets the gel time; n = 1 and n = 2 cross zero once and twice.").replace("_", " ")
    hv = hov(P, z[::2], [m[::2] for m in modes],
             lambda i: f"z/h = {z[::2][i]:.2f}: n=0 {modes[0][::2][i]:.3f}, n=1 {modes[1][::2][i]:.3f}, "
                       f"n=2 {modes[2][::2][i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #43 D6: every thickness on one curve
D6_H = (1e-3, 2e-3, 4e-3)
D6_DASH = (None, (7, 4), (2, 3))


def fig43():
    SER = (H.SERIES[1], H.SERIES[0], H.SERIES[2])   # baseline blue, second red: as plots_main #16, #26
    VB = (0, 0, W, 500)
    s = H.Scale(W, VB[3], display_w=400)
    from scipy.optimize import brentq
    T0 = brentq(lambda T: F_of_T(T)[0] - 0.5, 0.01, 1.0)          # F = 1/2 at a fixed T0
    P = Plot(s, (58, 46, 388, 186), (1, 5), (0, 1.05))
    Q = Plot(s, (58, 300, 388, 440), (0, 1.0), (0, 1.05))
    lt = np.linspace(1, 5, 241)
    T = np.linspace(0, 1.0, 201)
    o = [P.axes([(v, t) for v, t in LOG_T if v >= 1], [(0, "0"), (0.5, "0.5"), (1, "1")],
                "time t (s, log scale), D = 6×10⁻¹⁰ m²/s", "fluid support F")]
    o.append(Q.axes([(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1)], [(0, "0"), (0.5, "0.5"), (1, "1")],
                    "scaled time T = Dt/h²", "fluid support F"))
    o.append(legend(s, 58, 20, [(SER[k], f"h = {h * 1e3:g} mm", D6_DASH[k]) for k, h in enumerate(D6_H)]))
    Fr, th = [], []
    for k, h in enumerate(D6_H):
        Fk = F_of_T(D5 * 10**lt / h**2)
        Fr.append(Fk)
        th.append(T0 * h**2 / D5)
        o.append(P.curve(lt, Fk, SER[k], multi=True, dash=D6_DASH[k]))
    FT = F_of_T(T)
    for k in range(3):                                 # the same three runs: identical in T
        o.append(Q.curve(T, FT, SER[k], multi=True, dash=D6_DASH[k]))
    for k in range(3):
        o.append(P.dot(math.log10(th[k]), 0.5, SER[k]))
    o.append(Q.dot(T0, 0.5, I["primary"]))
    o.append(label(s, P.X(1.05), P.Y(0.33), "F = ½ at", "label2"))
    o.append(label(s, P.X(1.05), P.Y(0.33) + 15, f"{th[0]:.0f} s, {th[1]:.0f} s, {th[2]:.0f} s:", "label2"))
    o.append(label(s, P.X(1.05), P.Y(0.33) + 30, "×4 per doubling of h", "label2"))
    o.append(label(s, Q.X(0.98), Q.Y(0.92), "one master curve in T:", "label2", I["primary"], "end"))
    o.append(label(s, Q.X(0.98), Q.Y(0.92) + 15, f"F = ½ at T₀ = {T0:.3f} for every h", "label2", I["primary"], "end"))
    aria = ("Problem D6 plot in two stacked panels for plugs 1, 2 and 4 millimetres thick with D = 6e-10 square "
            f"metres per second. Top: fluid support against real time on a log axis; the three curves are the same "
            f"shape shifted right by a factor 4 per doubling of thickness, reaching F = 1/2 at {th[0]:.0f}, {th[1]:.0f} "
            f"and {th[2]:.0f} seconds. Bottom: the same three runs against T = D t / h squared lie on one master "
            f"curve, all reaching F = 1/2 at T0 = {T0:.3f}, so the gel time scales as h squared.")
    hv1 = hov(P, lt[::2], [f[::2] for f in Fr],
              lambda i: f"t = {10**lt[::2][i]:.0f} s: F = {Fr[0][::2][i]:.3f}, {Fr[1][::2][i]:.3f}, "
                        f"{Fr[2][::2][i]:.3f} (h = 1, 2, 4 mm)")
    hv2 = hov(Q, T[::2], [FT[::2]], lambda i: f"T = {T[::2][i]:.3f}: F = {FT[::2][i]:.3f} for every h")
    return svg_panels(VB, aria, s, "".join(o), [(P.box, hv1), (Q.box, hv2)])


# ---------------------------------------------------------------- #44 D7: the Hertz exponents
def fig44():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    N, ESTAR = 1715.0, 6.67e6                          # K3: knee reaction and reduced modulus
    a30 = (3 * N * 0.03 / (4 * ESTAR))**(1 / 3)
    p30 = 3 * N / (2 * math.pi * a30**2)
    assert (round(a30 * 1e3, 1), round(p30 / 1e6, 2)) == (18.0, 2.54), (a30, p30)   # K3 printed values
    P = Plot(s, (58, 62, 388, 226), (10, 60), (0, 2.2))
    R = np.linspace(10, 60, 201)
    ar = (R / 30)**(1 / 3)                             # a proportional to R^(1/3) at fixed N
    pr = (R / 30)**(-2 / 3)                            # p0 proportional to R^(-2/3)
    o = [P.axes([(v, f"{v}") for v in (10, 20, 30, 40, 50, 60)], [(0, "0"), (1, "1"), (2, "2")],
                f"effective radius R{sub('eff', s)} (mm), fixed load N", "relative to 30 mm", grid=(1, 2))]
    o.append(P.curve(R, pr, SER[1], multi=True))
    o.append(P.curve(R, ar, SER[0], multi=True))
    o.append(P.dot(30, 1, I["primary"]))
    o.append(P.dot(60, ar[-1], SER[0]))
    o.append(P.dot(60, pr[-1], SER[1]))
    o.append(legend(s, 58, 20, [(SER[0], "contact radius a", None), (SER[1], "peak pressure p₀", None)]))
    o.append(label(s, P.X(60) - 8, P.Y(ar[-1]) - 9, f"×{ar[-1]:.2f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(60) - 8, P.Y(pr[-1]) + 19, f"×{pr[-1]:.2f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(42), P.Y(float(ar[R >= 42].max())) - 9, "a ∝ R" + sup("1/3", s), "label", I["primary"]))
    o.append(label(s, P.X(15.5), P.Y(float(pr[R >= 15.5].max())) - 8, "p₀ ∝ R" + sup("−2/3", s), "label",
                   I["primary"]))
    o.append(label(s, P.X(30), P.Y(0.52), "both = 1 at 30 mm (K3)", "label2", I["secondary"], "middle"))
    o.append(H.line(s, P.X(30), P.Y(0.52) - 13, P.X(30), P.Y(1) + 6, I["secondary"], "leader"))
    aria = ("Problem D7 plot at fixed load: contact radius a and peak Hertz pressure p0 against effective radius from "
            "10 to 60 millimetres, each relative to its value at 30 millimetres (K3: a = 18.0 millimetres, p0 = 2.54 "
            f"megapascals). a grows as the cube root of R and p0 falls as R to the minus two thirds, so doubling R "
            f"from 30 to 60 millimetres multiplies a by {ar[-1]:.2f} and p0 by {pr[-1]:.2f}.")
    hv = hov(P, R[::2], [ar[::2], pr[::2]],
             lambda i: f"R = {R[::2][i]:.1f} mm: a = {a30 * 1e3 * ar[::2][i]:.1f} mm (×{ar[::2][i]:.2f}), "
                       f"p₀ = {p30 / 1e6 * pr[::2][i]:.2f} MPa (×{pr[::2][i]:.2f})")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #46 D9: the endpoint does not depend on k
def fig46():
    SER = (H.SERIES[1], H.SERIES[0], H.SERIES[2])   # baseline blue, second red: as plots_main #16, #26
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 62, 388, 226), (0, 6), (0, 1.12))
    th = np.linspace(0, 6, 241)                        # hours
    ks = (K5, 3 * K5)                                  # healthy, and permeability tripled as in K1 (c)
    cur = [creep_frac(HA5 * k * th * 3600 / H5**2) for k in ks]
    Ts = np.linspace(1e-3, 2, 20000)                   # K7 script: eps/eps_inf = 0.9 at T90
    T90 = Ts[np.argmin(np.abs(creep_frac(Ts) - 0.9))]
    assert round(T90, 3) == 0.848, T90
    t90 = [T90 * H5**2 / (HA5 * k) / 3600 for k in ks]
    o = [P.axes([(v, f"{v}") for v in range(7)], [(0, "0"), (0.5, "0.5"), (1, "1")], "time t (h)",
                "strain / drained value", grid=(0.5,))]
    o.append(ref(s, P, y=1))
    o.append(P.curve(th, cur[1], SER[1], multi=True))
    o.append(P.curve(th, cur[0], SER[0], multi=True))
    for k in range(2):
        o.append(P.dot(t90[k], 0.9, SER[k]))
    o.append(legend(s, 58, 20, [(SER[0], "k = 10⁻¹⁵ m⁴/(N s)", None), (SER[1], "3k", None)]))
    o.append(label(s, P.X(6), P.Y(1) - 10, f"ε{sub('∞', s, 'label2')} = σ/H{sub('A', s, 'label2')} for both",
                   "label2", I["primary"], "end"))
    o.append(label(s, P.X(5.9), P.Y(0.55), "90% of ε∞ reached at", "label2", I["primary"], "end"))
    o.append(label(s, P.X(5.9), P.Y(0.55) + 15, f"{t90[1]:.2f} h (3k), {t90[0]:.2f} h (k)", "label2",
                   I["primary"], "end"))
    o.append(label(s, P.X(5.9), P.Y(0.55) + 30, "k sets the path, not the end", "label2", I["secondary"], "end"))
    aria = ("Problem D9 plot: creep strain over its drained value against time in hours for the 2 millimetre plug "
            "with HA = 0.6 megapascals, at permeability k = 1e-15 and at 3k. Both curves start at zero and rise to "
            f"the same dashed endpoint epsilon-infinity = sigma/HA; the more permeable plug gets there sooner, 90 "
            f"percent at {t90[1]:.2f} hours against {t90[0]:.2f} hours.")
    hv = hov(P, th[::2], [cur[0][::2], cur[1][::2]],
             lambda i: f"t = {th[::2][i]:.2f} h: k {cur[0][::2][i]:.3f}, 3k {cur[1][::2][i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #48 K1: healthy against degraded
def fig48():
    SER = (H.SERIES[1], H.SERIES[0], H.SERIES[2])   # baseline blue, second red: as plots_main #16, #26
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    h, HA = 1.5e-3, 0.8e6                              # K1 script

    def F(k, t=0.5):
        D = HA * k
        T = D * np.atleast_1d(t) / h**2
        return D, h**2 / D, F_of_T(T)

    (_, tau_h, fh), (_, tau_d, fd) = F(2e-15), F(6e-15)
    assert (round(tau_h), round(tau_d), round(fh[0], 3), round(fd[0], 3)) == (1406, 469, 0.979, 0.963)
    P = Plot(s, (58, 62, 388, 226), (-1, 5), (0, 1.05))
    lt = np.linspace(-1, 5, 241)
    Fh, Fd = F(2e-15, 10**lt)[2], F(6e-15, 10**lt)[2]
    o = [P.axes(LOG_T, [(0, "0"), (0.5, "0.5"), (1, "1")], "time t (s, log scale)", "fluid support F", grid=(0.5,))]
    for v in (math.log10(0.5), math.log10(tau_d), math.log10(tau_h)):
        o.append(ref(s, P, x=v, col=O["dim"]))
    o.append(P.curve(lt, Fd, SER[1], multi=True))
    o.append(P.curve(lt, Fh, SER[0], multi=True))
    o.append(P.dot(math.log10(0.5), fh[0], SER[0]))
    o.append(P.dot(math.log10(0.5), fd[0], SER[1]))
    o.append(legend(s, 58, 20, [(SER[0], "healthy, k = 2×10⁻¹⁵", None), (SER[1], "degraded, k = 6×10⁻¹⁵", None)]))
    o.append(label(s, P.X(math.log10(tau_d)) - 4, P.y1 + 13, f"τ = {tau_d:.0f} s", "label2", I["primary"], "end"))
    o.append(label(s, P.X(math.log10(tau_h)) + 4, P.y1 + 13, f"τ = {tau_h:.0f} s", "label2"))
    x5 = P.X(math.log10(0.5))
    o.append(label(s, x5 + 5, P.Y(0.05), "footstep 0.5 s", "label2", I["secondary"]))
    o.append(label(s, x5 + 9, P.Y(0.62), "F at 0.5 s:", "label2"))
    o.append(label(s, x5 + 9, P.Y(0.62) + 15, f"{fh[0]:.3f} healthy", "label2"))
    o.append(label(s, x5 + 9, P.Y(0.62) + 30, f"{fd[0]:.3f} degraded", "label2"))
    o.append(H.line(s, x5 + 7, P.Y(0.62) - 12, x5 + 2, P.Y(fd[0]) + 5, I["secondary"], "leader"))
    aria = ("Problem K1 plot: fluid load support F against loading time on a log axis from 0.1 to 100000 seconds, for "
            f"healthy cartilage (k = 2e-15, gel time {tau_h:.0f} seconds) and degraded cartilage (k = 6e-15, gel time "
            f"{tau_d:.0f} seconds). At the 0.5 second footstep F is {fh[0]:.3f} and {fd[0]:.3f}; the curves part "
            "widely only near their gel times, marked by dashed lines.")
    hv = hov(P, lt, [Fh, Fd], lambda i: f"t = {10**lt[i]:.3g} s: healthy {Fh[i]:.3f}, degraded {Fd[i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #50 K2: halving the charge
def fig50():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    p2, p1 = donnan(0.2) / 1e6, donnan(0.1) / 1e6
    loss = 100 * (p2 - p1) / p2
    assert (round(p2, 3), round(p1, 3), round(loss)) == (0.156, 0.042, 73), (p2, p1, loss)   # K2 printed
    P = Plot(s, (58, 30, 388, 202), (0, 0.4), (0, 0.55))
    c = np.linspace(0, 0.4, 201)
    pc = donnan(c) / 1e6
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3, 0.4)], [(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5)],
                f"fixed-charge density c{sub('F', s)} (mol/L)", "swelling pressure π (MPa)", grid=(0.1, 0.2, 0.3, 0.4, 0.5))]
    for cv, pv in ((0.2, p2), (0.1, p1)):
        o.append(H.line(s, P.x0, P.Y(pv), P.X(cv), P.Y(pv), O["dim"], "ref", H.DASH_REF))
    o.append(P.curve(c, pc, SER[0]))
    o.append(P.dot(0.2, p2, SER[0]))
    o.append(P.dot(0.1, p1, SER[0]))
    o.append(label(s, P.X(0.2) - 8, P.Y(p2) - 8, f"{p2:.3f} MPa", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.1) - 8, P.Y(p1) - 8, f"{p1:.3f} MPa", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.015), P.Y(0.5), f"healthy c{sub('F', s, 'label2')} = 0.2 M, halved to 0.1 M:", "label2"))
    o.append(label(s, P.X(0.015), P.Y(0.5) + 16, f"π falls {p2:.3f} → {p1:.3f} MPa, −{loss:.0f}%", "label2"))
    aria = ("Problem K2 plot: Donnan swelling pressure against fixed-charge density from 0 to 0.4 moles per litre, "
            "with c0 = 0.15 molar and 310 kelvin. The curve rises faster than linearly. Healthy cartilage at 0.2 molar "
            f"has {p2:.3f} megapascals; halving the charge to 0.1 molar leaves {p1:.3f} megapascals, a {loss:.0f} "
            "percent loss.")
    hv = hov(P, c, [pc], lambda i: f"cF = {c[i]:.3f} M: π = {pc[i]:.4f} MPa")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #54 K4: finite-difference relaxation
K4_HA, K4_K, K4_EPS = 0.6e6, 1e-15, 0.10               # K4 script
K4_D = K4_HA * K4_K
K4_DT = 0.4 * (1e-3 / 60)**2 / K4_D                    # one fixed time step in seconds


@lru_cache(None)
def relax(h, N=60, ncycle=3.0):
    """K4 relax(), ported: confined relaxation at held strain eps0 -> (t, sigma, tau)."""
    tau = h**2 / K4_D
    dz = h / N
    r = K4_D * K4_DT / dz**2
    p = np.ones(N + 1)
    p[-1] = 0.0
    t, sig = [], []
    for n in range(int(ncycle * tau / K4_DT) + 1):
        t.append(n * K4_DT)
        sig.append(K4_HA * K4_EPS * (1.0 + p.mean()))
        lap = p[2:] - 2 * p[1:-1] + p[:-2]
        p[1:-1] += r * lap
        p[0] = p[1]
        p[-1] = 0.0
    return np.array(t), np.array(sig), tau


def t_half(t, sig):
    half = sig[-1] + 0.5 * (sig[0] - sig[-1])
    return t[np.argmax(sig <= half)]


def fig54():
    SER = (H.SERIES[1], H.SERIES[0], H.SERIES[2])   # baseline blue, second red: as plots_main #16, #26
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    t, sig, tau = relax(2e-3)
    assert (round(tau), round(sig[0] / 1e6, 3), round(sig[-1] / 1e6, 4)) == (6667, 0.119, 0.06), (tau, sig[0])
    hs = (1e-3, 2e-3, 4e-3)
    ths = [t_half(*relax(h)[:2]) for h in hs]
    assert [round(v, 1) for v in ths] == [333.5, 1334.1, 5336.3], ths            # K4 printed table
    assert all(round(v / h**2 / 1e8, 4) == 3.3352 for v, h in zip(ths, hs))
    P = Plot(s, (66, 62, 388, 226), (1, 5), (0, 0.14))
    o = [P.axes([(v, tt) for v, tt in LOG_T if v >= 1], [(v, f"{v:g}") for v in (0, 0.03, 0.06, 0.09, 0.12)],
                "time t (s, log scale)", "stress σ (MPa)", grid=(0.03, 0.09, 0.12), ytx=13)]
    o.append(ref(s, P, y=0.06))
    curves = []
    for k, h in enumerate(hs):
        tk, sk, _ = relax(h, ncycle=3.0 * (4e-3 / h)**2)   # every run to 3 tau of the 4 mm plug, 80000 s
        lt = np.linspace(1, math.log10(tk[-1]), 200)
        sl = np.interp(10**lt, tk, sk) / 1e6
        curves.append((lt, sl))
        o.append(P.curve(lt, sl, SER[k], multi=True))
    for k, h in enumerate(hs):
        lt, sl = curves[k]
        o.append(P.dot(math.log10(ths[k]), float(np.interp(math.log10(ths[k]), lt, sl)), SER[k]))
    o.append(legend(s, 66, 20, [(SER[k], f"h = {h * 1e3:g} mm", None) for k, h in enumerate(hs)]))
    o.append(label(s, P.X(1.05), P.Y(0.128), f"undrained peak {sig[0] / 1e6:.3f} MPa", "label2", I["secondary"]))
    o.append(label(s, P.x1, P.Y(0.06) + 16, f"σ∞ = H{sub('A', s, 'label2')}ε₀ = {sig[-1] / 1e6:.4f} MPa", "label2",
                   I["primary"], "end"))
    o.append(label(s, P.x1, P.Y(0.06) + 34, f"half-relaxed at {ths[0]:.1f}, {ths[1]:.1f}, {ths[2]:.1f} s", "label2",
                   I["primary"], "end"))
    o.append(label(s, P.x1, P.Y(0.06) + 50, "×4 per doubling of h: t½/h² = 3.3352×10⁸ s/m²", "label2",
                   I["secondary"], "end"))
    aria = ("Problem K4 plot: explicit finite-difference stress relaxation at a held 10 percent strain, HA = 0.6 "
            "megapascals, k = 1e-15, for plugs 1, 2 and 4 millimetres thick, against time on a log axis. Each stress "
            f"starts near the undrained peak {sig[0] / 1e6:.3f} megapascals and relaxes to the dashed drained value "
            f"{sig[-1] / 1e6:.4f}; dots mark half relaxation at {ths[0]:.1f}, {ths[1]:.1f} and {ths[2]:.1f} seconds, "
            "a factor 4 per doubling of thickness.")
    lt0 = curves[2][0]
    ys = [np.interp(lt0, *curves[k]) for k in range(3)]
    hv = hov(P, lt0, ys, lambda i: f"t = {10**lt0[i]:.3g} s: σ = {ys[0][i]:.4f}, {ys[1][i]:.4f}, "
                                   f"{ys[2][i]:.4f} MPa (h = 1, 2, 4 mm)")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #56 K5: footstep against a long stand
def fig56():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    tau = H5**2 / D5
    f05, f1h = F_of_T(D5 * np.array([0.5, 3600]) / H5**2)
    assert (round(tau), round(f05, 3), round(f1h, 3)) == (6667, 0.990, 0.214), (tau, f05, f1h)   # K5 printed
    P = Plot(s, (58, 30, 388, 202), (-1, 5), (0, 1.05))
    lt = np.linspace(-1, 5, 241)
    F = F_of_T(D5 * 10**lt / H5**2)
    o = [P.axes(LOG_T, [(0, "0"), (0.5, "0.5"), (1, "1")], "loading time t (s, log scale)", "fluid support F",
                grid=(0.5,))]
    o.append(ref(s, P, x=math.log10(tau), col=O["dim"]))
    o.append(P.curve(lt, F, SER[0]))
    o.append(P.dot(math.log10(0.5), f05, SER[0]))
    o.append(P.dot(math.log10(3600), f1h, SER[0]))
    xt = P.X(math.log10(tau))
    o.append(label(s, xt - 4, P.y1 + 13, f"τ = {tau:.0f} s ({tau / 3600:.1f} h)", "label2", I["primary"], "end"))
    x5 = P.X(math.log10(0.5))
    o.append(label(s, x5 + 6, P.Y(0.80), "footstep 0.5 s", "label2"))
    o.append(label(s, x5 + 6, P.Y(0.80) + 15, f"F = {f05:.3f}", "label2"))
    o.append(H.line(s, x5 + 2, P.Y(f05) + 6, x5 + 5, P.Y(0.80) - 12, I["secondary"], "leader"))
    x1h = P.X(math.log10(3600))
    o.append(label(s, x1h - 8, P.Y(f1h) + 14, "1 h stand", "label2", I["primary"], "end"))
    o.append(label(s, x1h - 8, P.Y(f1h) + 29, f"F = {f1h:.3f}", "label2", I["primary"], "end"))
    aria = ("Problem K5 plot: fluid load support F against loading time on a log axis for healthy cartilage, h = 2 "
            f"millimetres, HA = 0.6 megapascals, k = 1e-15, gel time {tau:.0f} seconds ({tau / 3600:.1f} hours, "
            f"dashed). A 0.5 second footstep sits at F = {f05:.3f}, fluid carrying 99 percent; a 1 hour stand has "
            f"dropped to F = {f1h:.3f}, the solid now carrying most of the load.")
    hv = hov(P, lt, [F], lambda i: f"t = {10**lt[i]:.3g} s: F = {F[i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #58 K6: friction follows the fluid
def fig58():
    VB = (0, 0, W, 472)
    s = H.Scale(W, VB[3], display_w=400)
    mu_eq = 0.15
    m_step, m_stand = mu_eq * (1 - 0.990), mu_eq * (1 - 0.214)          # K6 script
    assert (round(m_step, 4), round(m_stand, 4)) == (0.0015, 0.1179), (m_step, m_stand)
    ylo, yhi = math.log10(0.0005), math.log10(0.5)
    yt = [(math.log10(v), t) for v, t in ((0.001, "0.001"), (0.01, "0.01"), (0.1, "0.1"))]
    P = Plot(s, (66, 52, 388, 196), (-1, 5), (ylo, yhi))
    Q = Plot(s, (66, 268, 388, 412), (-4, 1), (ylo, yhi))
    lt = np.linspace(-1, 5, 241)
    mu_t = mu_eq * (1 - F_of_T(D5 * 10**lt / H5**2))   # boxed mu_eff = mu_eq (1 - F(t)), K5 tissue
    lS = np.linspace(-4, 1, 300)                       # section 7 Stribeck fit (all three constants assumed)
    S = 10**lS
    mu_S = 0.15 / (1 + (S / 0.5)**2) + 0.012 * S
    gr = [v for v, _ in yt]
    meff = f"μ{sub('eff', s)}"
    o = [P.axes(LOG_T, yt, "loading time t (s, log scale)", "friction μ", grid=gr, ytx=13)]
    o.append(Q.axes([(v, t) for v, t in ((-4, "10⁻⁴"), (-3, "10⁻³"), (-2, "0.01"), (-1, "0.1"), (0, "1"), (1, "10"))],
                    yt, "Stribeck number S = ηU/N (log scale)", "friction μ", grid=gr, ytx=13))
    o.append(legend(s, 66, 16, [(SER[0], f"cartilage {meff} = μ{sub('eq', s)}(1 − F)", None)]))
    o.append(legend(s, 66, 34, [(SER[1], "classical bearing μ(S), the assumed fit of §7", None)]))
    # top panel: mu_eff against loading time
    o.append(ref(s, P, y=math.log10(mu_eq)))
    o.append(P.curve(lt, np.log10(mu_t), SER[0]))
    x5, x1h = math.log10(0.5), math.log10(3600)
    o.append(P.dot(x5, math.log10(m_step), SER[0]))
    o.append(P.dot(x1h, math.log10(m_stand), SER[0]))
    o.append(f"<defs>{H.markers('m4f58_', s)}</defs>")
    o.append(H.arrow(s, "m4f58_", P.X(x5), P.Y(math.log10(m_step)) - 6, P.X(x5), P.Y(math.log10(mu_eq)) + 1,
                     "geometry", both=True))
    o.append(label(s, P.X(x5) + 6, P.Y(math.log10(0.015)) + 5, "×100", "label2", O["geometry"]))
    o.append(label(s, P.X(-0.95), P.Y(math.log10(mu_eq)) - 10, f"μ{sub('eq', s, 'label2')} = 0.15, dry solid contact",
                   "label2", I["primary"]))
    o.append(label(s, P.X(x5) + 8, P.Y(math.log10(m_step)) + 16, f"footstep 0.5 s: {m_step:.4f}", "label2"))
    o.append(label(s, P.X(0.3), P.Y(math.log10(0.05)), f"1 h stand: {m_stand:.3f}", "label2"))
    o.append(H.line(s, P.X(2.35), P.Y(math.log10(0.05)) - 4, P.X(x1h) - 5, P.Y(math.log10(m_stand)) + 1,
                    I["secondary"], "leader"))
    # bottom panel: the speed contrast
    o.append(Q.curve(lS, np.log10(mu_S), SER[1]))
    o.append(Q.curve([-4, 1], [math.log10(m_step)] * 2, SER[0]))
    o.append(label(s, Q.X(-3.95), Q.Y(math.log10(0.15)) - 7, "bearing: 0.15 at low S, no film", "label2"))
    i = int(mu_S.argmin())
    o.append(Q.dot(lS[i], math.log10(mu_S[i]), SER[1]))
    o.append(label(s, Q.X(lS[i]), Q.Y(math.log10(mu_S[i])) + 18, f"valley {mu_S[i]:.3f}", "label2", I["primary"],
                   "middle"))
    o.append(label(s, Q.X(-3.95), Q.Y(math.log10(m_step)) - 7, f"cartilage footstep: {m_step:.4f} at every S",
                   "label2"))
    aria = ("Problem K6 plot in two stacked panels with a log friction axis. Top: cartilage friction mu-eff = mu-eq "
            "(1 - F) against loading time for the K5 tissue; it sits at 0.0015 during a 0.5 second footstep, 100 "
            "times below the dry value 0.15 (dashed), and has climbed to 0.118 after a 1 hour stand. Bottom: against "
            "the Stribeck number, a classical bearing (the assumed fit of section 7) has friction 0.15 at low speed "
            f"and a valley of {mu_S[i]:.3f} only once a film builds, while cartilage during a footstep stays at "
            "0.0015 at every speed, including zero.")
    hv1 = hov(P, lt, [np.log10(mu_t)], lambda k: f"t = {10**lt[k]:.3g} s: μeff = {mu_t[k]:.4f}")
    hv2 = hov(Q, lS, [np.log10(mu_S), np.full_like(lS, math.log10(m_step))],
              lambda k: f"S = {S[k]:.2g}: bearing μ = {mu_S[k]:.3f}, cartilage footstep {m_step:.4f}")
    return svg_panels(VB, aria, s, "".join(o), [(P.box, hv1), (Q.box, hv2)])


# ---------------------------------------------------------------- #60 K7: creep to the drained limit
def fig60():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    sig = 0.3e6
    eps_inf = sig / HA5
    Ts = np.linspace(1e-3, 2, 20000)                   # K7 script, unchanged
    curve = creep_frac(Ts)
    T90 = Ts[np.argmin(np.abs(curve - 0.9))]
    t90 = T90 * H5**2 / D5
    tau = H5**2 / D5
    assert (round(eps_inf, 2), round(T90, 3), round(t90), round(t90 / 3600, 2)) == (0.5, 0.848, 5654, 1.57)
    P = Plot(s, (58, 30, 388, 202), (0, 6), (0, 0.56))
    th = np.linspace(0, 6, 241)
    eps = eps_inf * creep_frac(D5 * th * 3600 / H5**2)
    o = [P.axes([(v, f"{v}") for v in range(7)], [(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5)],
                "time t (h)", "strain ε", grid=(0.1, 0.2, 0.3, 0.4))]
    o.append(ref(s, P, y=eps_inf))
    o.append(P.curve(th, eps, SER[0]))
    o.append(P.dot(t90 / 3600, 0.9 * eps_inf, SER[0]))
    o.append(label(s, P.x1, P.Y(eps_inf) - 10, f"ε{sub('∞', s, 'label2')} = σ/H{sub('A', s, 'label2')} = {eps_inf:.2f}",
                   "label2", I["primary"], "end"))
    xd = P.X(t90 / 3600) + 8
    o.append(label(s, xd, P.Y(0.9 * eps_inf) + 18, f"90% of ε∞ at t = {t90:.0f} s = {t90 / 3600:.2f} h", "label2"))
    o.append(label(s, xd, P.Y(0.9 * eps_inf) + 33, f"T = {T90:.3f}, i.e. {t90 / tau:.2f} τ (τ = h²/D = {tau:.0f} s)",
                   "label2", I["secondary"]))
    aria = ("Problem K7 plot: creep strain against time in hours for the 2 millimetre plug under 0.3 megapascals, "
            f"HA = 0.6 megapascals, k = 1e-15. The strain starts at zero and rises to the dashed drained value "
            f"{eps_inf:.2f}; it reaches 90 percent of it at {t90:.0f} seconds, {t90 / 3600:.2f} hours, which is "
            f"T = {T90:.3f}, or {t90 / tau:.2f} of the gel time h squared over D = {tau:.0f} seconds.")
    hv = hov(P, th, [eps], lambda i: f"t = {th[i]:.2f} h: ε = {eps[i]:.3f} ({100 * eps[i] / eps_inf:.0f}% of ε∞)")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #62 K8: the thickness sweep
def fig62():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    D = 6e-10
    hs = (0.5e-3, 1e-3, 2e-3, 4e-3)
    taus = [h**2 / D for h in hs]
    assert [round(t) for t in taus] == [417, 1667, 6667, 26667]                   # K8 printed table
    P = Plot(s, (66, 30, 388, 202), (math.log10(0.4), math.log10(5)), (2, 5))
    lh = np.linspace(math.log10(0.4), math.log10(5), 121)
    lt = np.log10((10**lh * 1e-3)**2 / D)
    o = [P.axes([(math.log10(v), f"{v:g}") for v in (0.5, 1, 2, 4)],
                [(v, t) for v, t in LOG_T if v >= 2], "thickness h (mm, log scale)", "gel time τ = h²/D (s)",
                grid=(3, 4), ytx=13)]
    o.append(P.curve(lh, lt, SER[0]))
    txt = [f"{t / 60:.0f} min" if t < 3600 else f"{t / 3600:.1f} h" for t in taus]
    for j, (h, t, tx) in enumerate(zip(hs, taus, txt)):
        x, y = P.X(math.log10(h * 1e3)), P.Y(math.log10(t))
        o.append(P.dot(math.log10(h * 1e3), math.log10(t), SER[0]))
        if j == 0:                                     # first dot: below right, clear of the axis
            o.append(label(s, x + 7, y + 17, tx, "label2"))
        else:
            o.append(label(s, x - 7, y - 8, tx, "label2", I["primary"], "end"))
    o.append(label(s, P.x1, P.Y(2.55), "slope 2: each doubling of h", "label2", I["primary"], "end"))
    o.append(label(s, P.x1, P.Y(2.55) + 15, "multiplies τ by 4", "label2", I["primary"], "end"))
    aria = ("Problem K8 plot on log-log axes: gel time tau = h squared over D, with D = 6e-10, against cartilage "
            "thickness. A straight line of slope 2; dots at 0.5, 1, 2 and 4 millimetres give 7 minutes, 28 minutes, "
            "1.9 hours and 7.4 hours, a factor 4 per doubling.")
    hv = hov(P, lh, [lt], lambda i: f"h = {10**lh[i]:.2f} mm: τ = {10**lt[i]:.0f} s = {10**lt[i] / 60:.1f} min")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #64 K9: cycle by cycle
LAM9 = (2 * np.arange(4000) + 1) * np.pi / 2          # K9 script: 4000 terms


def deficit(k, t=1.0):
    return 1 - np.sum(2 / LAM9**2 * np.exp(-LAM9**2 * HA5 * k * t / H5**2))


def cycles(k, r, n=20):
    dF, d, out = deficit(k), 0.0, []
    for _ in range(n):
        out.append(1 - (d + dF))
        d = (1 - r) * (d + dF)
    return np.array(out)


def fig64():
    SER = (H.SERIES[1], H.SERIES[0], H.SERIES[2])   # baseline blue, second red: as plots_main #16, #26
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    Fh, Fd = cycles(1e-15, 1.0), cycles(1e-13, 0.8)
    finf = 1 - deficit(1e-13) / 0.8
    assert (round(Fh[0], 4), round(Fh[19], 4), round(Fd[0], 4), round(Fd[4], 4), round(Fd[19], 4), round(finf, 4)) \
        == (0.9862, 0.9862, 0.8618, 0.8273, 0.8273, 0.8273)                         # K9 printed
    P = Plot(s, (58, 62, 388, 226), (0.3, 20.7), (0.75, 1.0))
    n = np.arange(1, 21)
    o = [P.axes([(v, f"{v}") for v in (1, 5, 10, 15, 20)], [(v, f"{v:.2f}") for v in (0.75, 0.8, 0.85, 0.9, 0.95, 1.0)],
                "loading cycle number", "peak fluid support F", grid=(0.8, 0.85, 0.9, 0.95, 1.0))]
    o.append(ref(s, P, y=finf))
    o.append(P.curve(n, Fd, SER[1], multi=True))
    o.append(P.curve(n, Fh, SER[0], multi=True))
    for k, F in enumerate((Fh, Fd)):
        for x, y in zip(n, F):
            o.append(P.dot(x, y, SER[k]))
    o.append(legend(s, 58, 18, [(SER[0], "healthy: k = 10⁻¹⁵, r = 1", None)]))
    o.append(legend(s, 58, 38, [(SER[1], "degraded: k = 10⁻¹³ (100×), r = 0.8", None)]))
    o.append(label(s, P.x1, P.Y(Fh[0]) + 18, f"{Fh[0]:.4f} at every cycle", "label2", I["primary"], "end"))
    o.append(label(s, P.X(1.6), P.Y(Fd[0]) + 4, f"cycle 1: {Fd[0]:.4f}", "label2"))
    o.append(label(s, P.x1, P.Y(finf) + 18, f"plateau F∞ = 1 − ΔF/r = {finf:.4f}", "label2", I["primary"], "end"))
    o.append(label(s, P.x1, P.Y(finf) + 33, f"cycles 5 and 20: {Fd[4]:.4f}", "label2", I["secondary"], "end"))
    aria = ("Problem K9 plot: peak fluid support at each of 20 load and unload cycles of 1 second. Healthy tissue (k = "
            f"1e-15, full recovery r = 1) holds {Fh[0]:.4f} at every cycle. Degraded tissue (k = 1e-13, r = 0.8) starts "
            f"at {Fd[0]:.4f} and settles onto the dashed plateau 1 minus delta F over r = {finf:.4f}, the value at "
            "cycles 5 and 20: worse, but bounded.")
    hv = hov(P, n, [Fh, Fd], lambda i: f"cycle {n[i]}: healthy {Fh[i]:.4f}, degraded {Fd[i]:.4f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #66 K10: the critical charge
def fig66():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    from scipy.optimize import brentq
    HA = 0.6e6
    p2 = donnan(0.2)
    crit = [brentq(lambda c: donnan(c) - HA * e, 1e-4, 1.0) for e in (0.05, 0.10, 0.15)]

    def slope(cF, dc=1e-6):
        return (np.log(donnan(cF + dc)) - np.log(donnan(cF - dc))) / (np.log(cF + dc) - np.log(cF - dc))

    sl = [slope(c) for c in (0.2, 0.1, 0.05)]
    assert (round(p2 / 1e6, 4), round(p2 / (HA * 0.10), 2)) == (0.1561, 2.6)                     # K10 (a)
    assert [round(c, 4) for c in crit] == [0.0844, 0.1205, 0.1489]                               # K10 (b)
    assert [round(v, 3) for v in sl] == [1.832, 1.949, 1.986]                                    # K10 (c)
    line = HA * 0.10 / 1e6
    P = Plot(s, (66, 30, 388, 202), (0, 0.3), (0, 0.33))
    c = np.linspace(0, 0.3, 201)
    pc = donnan(c) / 1e6
    cF = f"c{sub('F', s, 'label2')}"
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3)], [(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3)],
                f"fixed-charge density c{sub('F', s)} (M)", "swelling pressure π (MPa)", grid=(0.1, 0.2, 0.3), ytx=13)]
    o.append(ref(s, P, y=line))
    o.append(H.line(s, P.X(crit[1]), P.y0, P.X(crit[1]), P.Y(line), O["dim"], "ref", H.DASH_REF))
    o.append(P.curve(c, pc, SER[0]))
    o.append(P.dot(crit[1], line, O["flag"]))
    o.append(P.dot(0.2, p2 / 1e6, SER[0]))
    o.append(label(s, P.X(0.005), P.Y(line) - 26, "(10% squeeze)", "label2", I["secondary"]))
    o.append(label(s, P.X(0.005), P.Y(line) - 10, f"H{sub('A', s, 'label2')}ε = {line:.3f} MPa", "label2"))
    o.append(label(s, P.X(crit[1]) + 6, P.Y(line) + 16, f"{crit[1]:.4f} M = {100 * crit[1] / 0.2:.0f}% of healthy",
                   "label2"))
    o.append(label(s, P.X(0.2) - 8, P.Y(p2 / 1e6) - 8, f"healthy 0.2 M: {p2 / 1e6:.4f} MPa", "label2", I["primary"],
                   "end"))
    o.append(label(s, P.X(0.2) - 8, P.Y(p2 / 1e6) - 23, f"{p2 / (HA * 0.10):.2f}× the squeeze stress", "label2",
                   I["primary"], "end"))
    o.append(label(s, P.X(0.005), P.Y(0.31), f"local log-slope d ln π / d ln {cF}:", "label2", I["secondary"]))
    o.append(label(s, P.X(0.005), P.Y(0.31) + 15, f"{sl[0]:.2f} at 0.2 M, {sl[1]:.2f} at 0.1 M, {sl[2]:.2f} at 0.05 M",
                   "label2", I["secondary"]))
    aria = ("Problem K10 plot: Donnan swelling pre-stress against fixed-charge density from 0 to 0.3 molar, with the "
            f"dashed line HA epsilon = {line:.3f} megapascals for a 10 percent squeeze. Healthy cartilage at 0.2 molar "
            f"has {p2 / 1e6:.4f} megapascals, {p2 / (HA * 0.10):.2f} times the line; the curve crosses the line at "
            f"{crit[1]:.4f} molar, {100 * crit[1] / 0.2:.0f} percent of healthy. The local log-slope rises from "
            f"{sl[0]:.2f} at 0.2 molar to {sl[2]:.2f} at 0.05 molar.")
    hv = hov(P, c, [pc], lambda i: f"cF = {c[i]:.3f} M: π = {pc[i]:.4f} MPa ({pc[i] / line:.2f}× HAε)")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


FIGS = {
    34: ("Left: under fixed strain the stress relaxes from an undraine", fig34),
    41: ("Short-time fluid support versus root-T: the exact series and", fig41),
    42: ("The first three cosine eigenmodes of the drainage problem; t", fig42),
    43: ("Nondimensionalized relaxation: plotted against T = Dt over h", fig43),
    44: ("Hertz scaling at fixed load: contact radius grows slowly as ", fig44),
    46: ("Creep strain normalized by its equilibrium value climbs from", fig46),
    48: ("Fluid load support F versus time on a log axis; healthy and ", fig48),
    50: ("Donnan swelling pressure rising with fixed-charge density; c", fig50),
    54: ("Confined-compression stress relaxation: stress jumps to an u", fig54),
    56: ("Fluid support over one plot: a half-second footstep sits nea", fig56),
    58: ("Friction versus sliding speed: cartilage stays near 0.01 eve", fig58),
    60: ("Creep: under a constant load the strain starts small (stiff ", fig60),
    62: ("Gel time versus cartilage thickness on log-log axes: a strai", fig62),
    64: ("Peak fluid support over twenty loading cycles: healthy tissu", fig64),
    66: ("Donnan swelling pressure against fixed-charge density, cross", fig66),
}
