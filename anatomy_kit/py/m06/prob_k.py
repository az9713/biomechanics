"""Module 6 computational-problem plots (K1-K8, K10): house-style redraws at 400 px.

Every plotted number is computed here from the K solution scripts in module06.html (ported line for
line; their printed numbers are asserted). K8's cadence sweep uses the closed-form steady state of the
same SLS cycle, checked against the ported integrator at the solution's 2.6 Hz.
"""
import math
from functools import lru_cache

import numpy as np

import house as H
from m05.plots_prob import Plot, hov, label, legend, sub, svg

O, I, SER = H.OVERLAY, H.INK, H.SERIES
W = 400


def dot_legend(s, x, y, col, txt):
    """Legend entry for a scatter series: one dot + name."""
    return (f'<circle cx="{x + 10:.2f}" cy="{y - 4.5:.2f}" r="{s(H.PX["dot"]) * 0.8:.2f}" fill="{col}"/>'
            + label(s, x + 25, y, txt, "label2", I["secondary"]))


def dots(P, xs, ys, col, r=2.6):
    return "".join(f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{r:.2f}" fill="{col}"/>' for x, y in zip(xs, ys))


# ---------------------------------------------------------------- #51 K1: inverting the crimp model
L0 = 0.25                                                   # tendon rest length (m), Appendix
K_TRUE, E_TRUE = 4.16e5, 0.030


def F_crimp(x, k_lin, x_star):                              # Eq. 2.3, both branches
    return np.where(x <= x_star, k_lin * x**2 / (2 * x_star), k_lin * (x - x_star / 2))


@lru_cache(None)
def k1_fit():
    from scipy.optimize import curve_fit
    rng = np.random.default_rng(3)
    xd = np.linspace(0.001, 0.013, 25)
    yd = F_crimp(xd, K_TRUE, E_TRUE * L0) * (1 + 0.05 * rng.standard_normal(25)) + 40 * rng.standard_normal(25)
    p, cov = curve_fit(F_crimp, xd, yd, p0=[3.0e5, 0.005], maxfev=20000)
    return xd, yd, p, np.sqrt(np.diag(cov))


def fig51():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    xd, yd, p, sd = k1_fit()
    k, ks, e, es = p[0] / 1e3, sd[0] / 1e3, p[1] / L0 * 100, sd[1] / L0 * 100
    assert (round(k), round(ks), round(e, 2), round(es, 2)) == (438, 15, 3.23, 0.17), (k, ks, e, es)
    P = Plot(s, (66, 62, 388, 226), (0, 14), (0, 4200))
    x = np.linspace(0, 0.014, 281)
    fit, true = F_crimp(x, *p), F_crimp(x, K_TRUE, E_TRUE * L0)
    xs_mm = p[1] * 1e3
    o = [P.axes([(v, f"{v}") for v in (0, 2, 4, 6, 8, 10, 12, 14)],
                [(0, "0"), (1000, "1000"), (2000, "2000"), (3000, "3000"), (4000, "4000")],
                "elongation x (mm)", "force F (N)", grid=(1000, 2000, 3000, 4000), ytx=13)]
    o.append(H.line(s, P.X(xs_mm), P.y0, P.X(xs_mm), P.Y(F_crimp(p[1], *p)), O["dim"], "leader", H.DASH_REF))
    o.append(P.curve(x * 1e3, true / 1, SER[1], multi=True, dash=(5, 3)))
    o.append(P.curve(x * 1e3, fit, SER[0], multi=True))
    o.append(dots(P, xd * 1e3, yd, I["secondary"]))
    o.append(dot_legend(s, 66, 20, I["secondary"], "25 noisy samples"))
    o.append(legend(s, 210, 20, [(SER[0], "crimp fit", None)]))
    o.append(legend(s, 66, 40, [(SER[1], f"true model (k{sub('lin', s, 'label2')} = 416 kN/m, ε* = 3.00%)", (5, 3))]))
    o.append(label(s, P.X(0.4), P.Y(3700), f"fit: k{sub('lin', s, 'label2')} = {k:.0f} ± {ks:.0f} kN/m", "label2"))
    o.append(label(s, P.X(0.4), P.Y(3700) + 16, f"ε* = {e:.2f} ± {es:.2f}%", "label2"))
    o.append(label(s, P.X(xs_mm) + 5, P.y0 - 8, f"x* = ε*L{sub('0', s, 'label2')} = {xs_mm:.1f} mm", "label2",
                   I["secondary"]))
    o.append(label(s, P.X(3.2), P.Y(600), "toe", "label2", I["secondary"], "middle"))
    o.append(label(s, P.X(12.6), P.Y(2500), "linear", "label2", I["secondary"], "middle"))
    aria = (f"Problem K1 plot: 25 noisy force-elongation samples from 1 to 13 millimetres and the crimp model fitted "
            f"to them by nonlinear least squares, beside the dashed true model. The fit recovers a linear stiffness of "
            f"{k:.0f} plus or minus {ks:.0f} kilonewtons per metre and a toe strain of {e:.2f} plus or minus {es:.2f} "
            f"percent, against true values of 416 and 3.00; a dashed drop line marks the fitted end of the toe at "
            f"{xs_mm:.1f} millimetres.")
    hv = hov(P, x[::2] * 1e3, [fit[::2], true[::2]],
             lambda i: f"x = {x[::2][i] * 1e3:.2f} mm: fit {fit[::2][i]:.0f} N, true {true[::2][i]:.0f} N")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #53 K2: linear versus toe energy at one peak force
def fig53():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    k_lin, x_star, F_pk = 4.16e5, 0.0075, 4000.0
    x_lin, x_toe = F_pk / k_lin, F_pk / k_lin + x_star / 2
    U = {}
    for name, xm, law in (("linear", x_lin, lambda z: k_lin * z), ("toe", x_toe, lambda z: F_crimp(z, k_lin, x_star))):
        grid = np.linspace(0.0, xm, 200001)
        U[name] = np.trapezoid(law(grid), grid)
    more = 100 * (U["toe"] / U["linear"] - 1)
    assert (round(x_lin * 1e3, 2), round(x_toe * 1e3, 2), round(U["linear"], 2), round(U["toe"], 2), round(more, 1)) \
        == (9.62, 13.37, 19.23, 20.21, 5.1), (x_lin, x_toe, U, more)
    P = Plot(s, (66, 62, 388, 226), (0, 14), (0, 4600))
    xl = np.linspace(0, x_lin, 121)
    xt = np.linspace(0, x_toe, 241)
    Fl, Ft = k_lin * xl, F_crimp(xt, k_lin, x_star)
    o = [P.axes([(v, f"{v}") for v in (0, 2, 4, 6, 8, 10, 12, 14)],
                [(0, "0"), (1000, "1000"), (2000, "2000"), (3000, "3000"), (4000, "4000")],
                "elongation x (mm)", "force F (N)", grid=(1000, 2000, 3000), ytx=13)]
    o.append(H.line(s, P.x0, P.Y(F_pk), P.x1, P.Y(F_pk), I["primary"], "ref", H.DASH_REF))
    for xm in (x_lin, x_toe):
        o.append(H.line(s, P.X(xm * 1e3), P.y0, P.X(xm * 1e3), P.Y(F_pk), O["dim"], "leader", H.DASH_REF))
    o.append(P.curve(xl * 1e3, Fl, SER[1], multi=True))
    o.append(P.curve(xt * 1e3, Ft, SER[0], multi=True))
    o.append(P.dot(x_lin * 1e3, F_pk, SER[1]))
    o.append(P.dot(x_toe * 1e3, F_pk, SER[0]))
    o.append(legend(s, 66, 20, [(SER[1], "linear spring F = kx", None), (SER[0], "toe tendon (Eq. 2.3)", None)]))
    o.append(label(s, P.X(0.3), P.Y(F_pk) - 7, "same peak force 4 kN", "label2", I["primary"]))
    o.append(label(s, P.X(x_lin * 1e3) - 5, P.y0 - 8, f"{x_lin * 1e3:.2f} mm", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(x_toe * 1e3) - 5, P.y0 - 8, f"{x_toe * 1e3:.2f} mm", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(4.6), P.Y(2600), f"U{sub('lin', s, 'label2')} = {U['linear']:.2f} J", "label2", I["primary"],
                   "end"))
    xm = (x_lin + x_toe) / 2 * 1e3                         # under the toe curve only, between the drop lines
    o.append(label(s, P.X(xm), P.Y(1900), f"U{sub('toe', s, 'label2')} =", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(xm), P.Y(1900) + 16, f"{U['toe']:.2f} J", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(xm), P.Y(1900) + 32, f"+{more:.1f}%", "label2", I["secondary"], "middle"))
    aria = (f"Problem K2 plot: force against elongation for a linear spring and a toe tendon of the same linear "
            f"stiffness, both loaded to the same 4 kilonewton peak. The linear spring reaches it at {x_lin * 1e3:.2f} "
            f"millimetres and stores {U['linear']:.2f} joules; the toe tendon must stretch to {x_toe * 1e3:.2f} "
            f"millimetres and stores {U['toe']:.2f} joules, {more:.1f} percent more.")
    hv = []
    for xv in np.linspace(0, x_toe, 135):
        ys = [P.Y(float(F_crimp(xv, k_lin, x_star)))]
        txt = f"x = {xv * 1e3:.2f} mm: toe {float(F_crimp(xv, k_lin, x_star)):.0f} N"
        if xv <= x_lin:
            ys.append(P.Y(k_lin * xv))
            txt += f", linear {k_lin * xv:.0f} N"
        hv.append([P.X(xv * 1e3), ys, txt])
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #55 K3: the fibre/tendon split
A3, B3, S3 = 60.0, 0.005, 0.015                             # assumed passive-fibre law and MTU stretch (K3)


def fibre_stretch(k_T, S):
    from scipy.optimize import brentq
    return brentq(lambda z: A3 * (np.exp(z / B3) - 1) - k_T * (S - z), 0.0, S)


def fig55():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    shares = {k: 100 * fibre_stretch(k, S3) / S3 for k in (2.0e4, 1.0e5, 1.0e6, 1.0e8)}
    assert [round(v, 1) for v in shares.values()] == [44.3, 70.7, 93.7, 99.9], shares
    P = Plot(s, (58, 62, 310, 226), (0, 15), (0, 15))
    Sg = np.linspace(0.00015, S3, 100)
    ks = (2.0e4, 1.0e5, 1.0e6)
    curves = {k: np.array([fibre_stretch(k, v) for v in Sg]) * 1e3 for k in ks}
    o = [P.axes([(v, f"{v}") for v in (0, 5, 10, 15)], [(0, "0"), (5, "5"), (10, "10"), (15, "15")],
                "MTU stretch S (mm)", "fibre stretch δ (mm)", grid=(5, 10, 15))]
    o.append(P.curve([0, 15], [0, 15], I["rule"], multi=True, dash=(6, 4)))
    for n, k in enumerate(ks):
        o.append(P.curve([0] + list(Sg * 1e3), [0] + list(curves[k]), SER[n], multi=True))
        o.append(P.dot(15, curves[k][-1], SER[n]))
        o.append(label(s, P.X(15) + 8, P.Y(curves[k][-1]) + 4.5, f"δ/S = {shares[k]:.1f}%", "label2"))
    o.append(legend(s, 58, 20, [(SER[0], f"k{sub('T', s, 'label2')} = 20", None), (SER[1], "100", None),
                                (SER[2], "1000 kN/m", None)], gap=12))
    o.append(legend(s, 58, 40, [(I["rule"], "rigid tendon δ = S (10⁵ kN/m gives 99.9%)", (6, 4))]))
    aria = ("Problem K3 plot: fibre stretch against total muscle-tendon stretch, from the root-found force balance, "
            "for tendon stiffness 20, 100 and 1000 kilonewtons per metre, beside the dashed rigid-tendon line delta "
            f"equals S. At 15 millimetres the fibre carries {shares[2.0e4]:.1f}, {shares[1.0e5]:.1f} and "
            f"{shares[1.0e6]:.1f} percent of the stretch; a 10 to the 5 kilonewton per metre tendon gives "
            f"{shares[1.0e8]:.1f} percent, the rigid limit.")
    hv = hov(P, Sg * 1e3, [curves[k] for k in ks],
             lambda i: f"S = {Sg[i] * 1e3:.1f} mm: δ = {curves[ks[0]][i]:.2f}, {curves[ks[1]][i]:.2f}, "
                       f"{curves[ks[2]][i]:.2f} mm")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #57 K4: resonance tuning of the leg spring
def fig57():
    VB = (0, 0, W, 294)
    s = H.Scale(W, VB[3], display_w=400)
    M, f_stride = 80.0, 2.6
    w = 2 * np.pi * f_stride
    k_star = M * w**2
    zeta = 0.07 / (4 * np.pi)
    c = 2 * zeta * np.sqrt(k_star * M)

    def amp(k):
        return (c * w) / np.hypot(k - M * w**2, c * w)
    assert (round(k_star / 1e3, 1), round(zeta, 4), round(4 * zeta * 100, 1)) == (21.3, 0.0056, 2.2)
    assert [round(float(amp(f * k_star)), 3) for f in (0.5, 0.9, 1.1, 1.5)] == [0.022, 0.111, 0.111, 0.022]
    lo, hi = math.log10(0.01), 0.0
    P = Plot(s, (66, 70, 388, 234), (0.5 * k_star / 1e3, 1.5 * k_star / 1e3), (lo, hi + 0.08))
    fac = np.linspace(0.5, 1.5, 601)                       # step 1/600, includes k = k* exactly
    kk = fac * k_star
    A = amp(kk)
    o = [P.axes([(v, f"{v}") for v in (15, 20, 25, 30)],
                [(math.log10(v), t) for v, t in ((0.01, "0.01"), (0.1, "0.1"), (1, "1"))],
                "leg stiffness k (kN/m)", "amplitude X / X(k*)", grid=(-1.0, 0.0), ytx=13)]
    o.append(H.line(s, P.X(k_star / 1e3), P.y0, P.X(k_star / 1e3), P.y1, O["dim"], "leader", H.DASH_REF))
    o.append(P.curve(kk / 1e3, np.log10(A), SER[0], nmax=len(kk)))
    for f in (0.5, 0.9, 1.1, 1.5):
        o.append(P.dot(f * k_star / 1e3, math.log10(amp(f * k_star)), SER[0]))
    a9, a5 = amp(0.9 * k_star), amp(0.5 * k_star)
    o.append(label(s, P.X(0.9 * k_star / 1e3) - 8, P.Y(math.log10(a9)) + 4, f"0.9k*: {a9:.3f}", "label2", I["primary"],
                   "end"))
    o.append(label(s, P.X(1.1 * k_star / 1e3) + 8, P.Y(math.log10(a9)) + 4, f"1.1k*: {a9:.3f}", "label2"))
    o.append(label(s, P.X(0.5 * k_star / 1e3) + 6, P.Y(math.log10(a5)) + 19, f"0.5k*: {a5:.3f}", "label2"))
    o.append(label(s, P.X(1.5 * k_star / 1e3) - 6, P.Y(math.log10(a5)) + 19, f"1.5k*: {a5:.3f}", "label2",
                   I["primary"], "end"))
    o.append(label(s, P.X(k_star / 1e3) + 6, P.y1 - 8, f"k* = Mω² = {k_star / 1e3:.1f} kN/m", "label2"))
    o.append(label(s, P.X(k_star / 1e3) - 6, P.y1 - 8, "peak", "label2", I["secondary"], "end"))
    o.append(label(s, P.x0 + 2, 22, f"stride 2.6 Hz, M = 80 kg, ζ = {zeta:.4f}", "label2", I["secondary"]))
    o.append(label(s, P.x0 + 2, 40, f"half-power band 4ζ = {4 * zeta * 100:.1f}% of k*", "label2", I["secondary"]))
    aria = (f"Problem K4 plot: steady bounce amplitude, as a fraction of its peak and on a log axis, against leg "
            f"stiffness from half to one and a half times the resonant value k star = M omega squared = "
            f"{k_star / 1e3:.1f} kilonewtons per metre at a 2.6 hertz stride. The curve is a narrow symmetric spike at "
            f"k star: {a9:.3f} of peak at 0.9 and 1.1 k star, {a5:.3f} at 0.5 and 1.5 k star.")
    hv = hov(P, kk / 1e3, [np.log10(A)], lambda i: f"k = {kk[i] / 1e3:.2f} kN/m ({fac[i]:.3f} k*): {A[i]:.3f} of peak")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #59 K5: inverting a relaxation curve
E0_5, TS5, TE5, ER5 = 0.01, 0.050, 0.090, 1.20e9


def relax(t, ER, ts, te):
    """SLS step-strain response; E_inst = ER te/ts (Prop. 7)."""
    return E0_5 * (ER + ER * (te / ts - 1.0) * np.exp(-t / ts))


@lru_cache(None)
def k5_fit():
    from scipy.optimize import curve_fit
    rng = np.random.default_rng(3)
    td = np.linspace(0.002, 0.5, 60)
    sd = relax(td, ER5, TS5, TE5) * (1 + 0.02 * rng.standard_normal(60))
    q, _ = curve_fit(relax, td, sd, p0=[1.0e9, 0.04, 0.07], maxfev=20000)
    return td, sd, q


def fig59():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    td, sd, q = k5_fit()
    ei = q[0] * q[2] / q[1]
    assert (round(q[0] / 1e9, 3), round(q[1], 4), round(q[2], 4), round(ei / 1e9, 3)) == (1.203, 0.048, 0.0866, 2.168), q
    P = Plot(s, (58, 62, 388, 226), (0, 0.5), (0, 24))
    t = np.linspace(0, 0.5, 251)
    fit = relax(t, *q) / 1e6
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5)], [(0, "0"), (6, "6"), (12, "12"), (18, "18"), (24, "24")],
                "time t (s)", "stress σ (MPa)", grid=(6, 18, 24))]
    pl = q[0] * E0_5 / 1e6
    o.append(H.line(s, P.x0, P.Y(pl), P.x1, P.Y(pl), I["primary"], "ref", H.DASH_REF))
    o.append(P.curve(t, fit, SER[0]))
    o.append(dots(P, td, sd / 1e6, I["secondary"]))
    o.append(P.dot(0, ei * E0_5 / 1e6, SER[0]))
    o.append(dot_legend(s, 58, 20, I["secondary"], "60 noisy samples"))
    o.append(legend(s, 200, 20, [(SER[0], "SLS fit", None)]))
    o.append(label(s, P.X(0.008), P.Y(ei * E0_5 / 1e6) - 8, f"jump E{sub('inst', s, 'label2')}ε{sub('0', s, 'label2')}"
                   f" = {ei * E0_5 / 1e6:.1f} MPa", "label2"))
    o.append(label(s, P.X(0.49), P.Y(pl) - 8, f"plateau E{sub('R', s, 'label2')}ε{sub('0', s, 'label2')} = {pl:.1f} MPa",
                   "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.49), P.Y(7.6), f"fit: E{sub('R', s, 'label2')} = {q[0] / 1e9:.3f} GPa,", "label2",
                   I["primary"], "end"))
    o.append(label(s, P.X(0.49), P.Y(7.6) + 16, f"τ{sub('σ', s, 'label2')} = {q[1]:.4f} s, "
                   f"τ{sub('ε', s, 'label2')} = {q[2]:.4f} s", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.49), P.Y(7.6) + 32, "(true 1.20 GPa, 0.050 s, 0.090 s)", "label2", I["secondary"], "end"))
    aria = (f"Problem K5 plot: 60 noisy stress-relaxation samples after a 1 percent strain step and the standard linear "
            f"solid fitted to them by least squares. The fitted curve jumps to {ei * E0_5 / 1e6:.1f} megapascals and "
            f"decays to the dashed plateau of {pl:.1f} megapascals; the fit recovers E R = {q[0] / 1e9:.3f} gigapascals, "
            f"tau sigma = {q[1]:.4f} seconds and tau epsilon = {q[2]:.4f} seconds.")
    hv = hov(P, t, [fit], lambda i: f"t = {t[i]:.3f} s, fit σ = {fit[i]:.2f} MPa")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #61 K6: three models under one ramp-and-hold
@lru_cache(None)
def k6_run():
    ER, E_inst, ts = 1.20e9, 2.16e9, 0.050
    eta = (E_inst - ER) * ts
    EM, EK = E_inst, ER
    e0, t_ramp, t_end, dt = 0.02, 0.02, 0.60, 1.0e-5
    sM = sS = sK = 0.0
    T, Ms, Ks, Ss = [0.0], [0.0], [0.0], [0.0]
    for i in range(int(t_end / dt)):
        t = i * dt
        ed = e0 / t_ramp if t < t_ramp else 0.0
        e = min(e0, e0 * t / t_ramp)
        sM += dt * (EM * ed - sM * EM / eta)
        sK = EK * e + eta * ed
        sS += dt * ((ER * (e + (ts * E_inst / ER) * ed) - sS) / ts)
        if (i < 4000 and i % 20 == 0) or i % 500 == 0 or i in (1999, 2000, 2001) or i == int(t_end / dt) - 1:
            T.append(t)
            Ms.append(sM / 1e6)
            Ks.append(sK / 1e6)
            Ss.append(sS / 1e6)
    return tuple(T), tuple(Ms), tuple(Ks), tuple(Ss), E_inst * e0 / 1e6, ER * e0 / 1e6


def fig61():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    T, Ms, Ks, Ss, sinst, splat = k6_run()
    pk = (max(Ms), max(Ks), max(Ss))
    assert [round(v, 1) for v in pk] == [28.5, 72.0, 39.8] and (round(Ms[-1], 1), round(Ks[-1], 1), round(Ss[-1], 1)) \
        == (0.0, 24.0, 24.0) and (round(sinst, 1), round(splat, 1)) == (43.2, 24.0), (pk, Ms[-1], Ks[-1], Ss[-1])
    P = Plot(s, (58, 62, 388, 226), (0, 0.6), (0, 80))
    n = len(T)
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6)],
                [(0, "0"), (20, "20"), (40, "40"), (60, "60"), (80, "80")],
                "time t (s)", "stress σ (MPa)", grid=(20, 40, 60, 80))]
    o.append(H.line(s, P.X(0.2), P.Y(sinst), P.x1, P.Y(sinst), I["primary"], "ref", H.DASH_REF))
    c = next(i for i, t in enumerate(T) if t > 0.03)        # KV dashed on the plateau it shares with the SLS
    o.append(P.curve(T[:c + 1], Ks[:c + 1], SER[2], multi=True, nmax=n))
    o.append(P.curve(T, Ms, SER[1], multi=True, nmax=n))
    o.append(P.curve(T, Ss, SER[0], multi=True, nmax=n))
    o.append(P.curve(T[c:], Ks[c:], SER[2], multi=True, dash=(6, 4), nmax=n))
    o.append(legend(s, 58, 20, [(SER[0], "SLS", None), (SER[1], "Maxwell", None), (SER[2], "Kelvin–Voigt", None)]))
    o.append(label(s, P.x0, 40, "strain: 20 ms ramp to 2%, then hold", "label2", I["secondary"]))
    o.append(label(s, P.X(0.025), P.Y(72) + 4, f"KV spike {pk[1]:.1f} MPa (η dε/dt)", "label2"))
    o.append(label(s, P.X(0.56), P.Y(sinst) - 10, f"ideal step E{sub('inst', s, 'label2')}ε{sub('0', s, 'label2')} = "
                   f"{sinst:.1f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.04), P.Y(pk[2]) + 4, f"SLS peak {pk[2]:.1f}", "label2"))
    o.append(label(s, P.X(0.045), P.Y(14), f"Maxwell peak {pk[0]:.1f}", "label2"))
    for ys, col in ((Ss, SER[0]), (Ms, SER[1])):
        o.append(P.dot(T[int(np.argmax(ys))], max(ys), col))
    o.append(label(s, P.X(0.56), P.Y(splat) - 10, f"SLS and KV plateau E{sub('R', s, 'label2')}ε{sub('0', s, 'label2')}"
                   f" = {splat:.1f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.56), P.Y(0) - 8, "Maxwell relaxes to 0", "label2", I["primary"], "end"))
    aria = (f"Problem K6 plot: stress against time for Maxwell, Kelvin-Voigt and standard linear solid models under one "
            f"strain history, a 20 millisecond ramp to 2 percent and a hold to 0.6 seconds. Kelvin-Voigt spikes to "
            f"{pk[1]:.1f} megapascals during the ramp and then sits at {splat:.1f}; Maxwell peaks at {pk[0]:.1f} and "
            f"relaxes to zero; the SLS peaks at {pk[2]:.1f}, below its dashed ideal step value {sinst:.1f}, and relaxes "
            f"to the finite plateau {splat:.1f} megapascals.")
    idx = [i for i in range(n) if T[i] >= 0.03 or i % 3 == 0]
    hv = [[P.X(T[i]), [P.Y(Ss[i]), P.Y(Ms[i]), P.Y(Ks[i])],
           f"t = {T[i] * 1e3:.0f} ms: SLS {Ss[i]:.1f}, Maxwell {Ms[i]:.1f}, KV {Ks[i]:.1f} MPa"] for i in idx]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #63 K7: the SLS loss peak
def fig63():
    VB = (0, 0, W, 372)
    s = H.Scale(W, VB[3], display_w=400)
    ts, te, e0, ER = 0.050, 0.100, 0.01, 1.20e9
    w = np.logspace(-2, 4, 4001)
    Es = ER * (1 + 1j * w * te) / (1 + 1j * w * ts)
    tand, Wd = Es.imag / Es.real, np.pi * Es.imag * e0**2 / 1e3
    i, j = int(tand.argmax()), int(Wd.argmax())

    def td_at(v):
        e = ER * (1 + 1j * v * te) / (1 + 1j * v * ts)
        return e.imag / e.real
    assert (round(w[i], 2), round(tand[i], 3), round(Wd[i], 1)) == (14.13, 0.354, 177.6), (w[i], tand[i], Wd[i])
    assert (round(td_at(0.1), 3), round(td_at(1000.0), 3)) == (0.005, 0.010)
    assert (round(w[j], 1), round(Wd[j], 1)) == (20.0, 188.5), (w[j], Wd[j])
    lw = np.log10(w)
    P = Plot(s, (66, 62, 388, 186), (-2, 4), (0, 0.4))
    Q = Plot(s, (66, 214, 388, 330), (-2, 4), (0, 200))
    xt = [(v, f"10{t}") for v, t in ((-2, "⁻²"), (-1, "⁻¹"), (0, "⁰"), (1, "¹"), (2, "²"), (3, "³"), (4, "⁴"))]
    o = [P.axes([], [(0, "0"), (0.2, "0.2"), (0.4, "0.4")], "", "tan δ", grid=(0.2, 0.4), ytx=13)]
    for v, _ in xt:
        o.append(H.line(s, P.X(v), P.y0, P.X(v), P.y0 + 5, I["axis"], "leader"))
    o.append(Q.axes(xt, [(0, "0"), (100, "100"), (200, "200")], "frequency ω (rad/s)", f"W{sub('d', s)} (kJ/m³)",
                    grid=(100, 200), ytx=13))
    xs = math.log10(1 / math.sqrt(ts * te))
    for R in (P, Q):
        o.append(H.line(s, R.X(xs), R.y0, R.X(xs), R.y1, O["dim"], "leader", H.DASH_REF))
    o.append(H.line(s, Q.X(math.log10(1 / ts)), Q.y0, Q.X(math.log10(1 / ts)), Q.Y(Wd[j]), O["dim"], "leader",
                    (2, 3)))
    o.append(P.curve(lw, tand, SER[0], nmax=400))
    o.append(Q.curve(lw, Wd, SER[1], nmax=400))
    o.append(P.dot(lw[i], tand[i], SER[0]))
    o.append(P.dot(-1, td_at(0.1), SER[0]))
    o.append(P.dot(3, td_at(1000.0), SER[0]))
    o.append(Q.dot(lw[i], Wd[i], SER[1]))
    o.append(Q.dot(lw[j], Wd[j], SER[1]))
    o.append(legend(s, 66, 20, [(SER[0], "loss tangent tan δ", None), (SER[1], f"loop area W{sub('d', s, 'label2')} per cycle", None)]))
    o.append(label(s, P.X(xs) - 28, P.Y(tand[i]) + 4, f"max {tand[i]:.3f} at ω = {w[i]:.2f}", "label2", I["primary"],
                   "end"))
    o.append(label(s, P.X(xs) + 6, P.y1 + 2, "ω* = 1/√(τ" + sub("σ", s, "label2") + "τ" + sub("ε", s, "label2")
                   + ") = 14.14", "label2"))
    o.append(label(s, P.X(-1), P.Y(td_at(0.1)) - 10, f"{td_at(0.1):.3f}", "label2", I["secondary"], "middle"))
    o.append(label(s, P.X(3), P.Y(td_at(1000.0)) - 10, f"{td_at(1000.0):.3f}", "label2", I["secondary"], "middle"))
    o.append(label(s, Q.X(lw[i]) - 26, Q.Y(Wd[i]) + 4, f"{Wd[i]:.1f} at ω*", "label2", I["primary"], "end"))
    o.append(label(s, Q.X(lw[j]) + 26, Q.Y(Wd[j]) + 4, f"max {Wd[j]:.1f}", "label2"))
    o.append(label(s, Q.X(lw[j]) + 26, Q.Y(Wd[j]) + 20, f"at 1/τ{sub('σ', s, 'label2')} = {w[j]:.0f} rad/s", "label2"))
    o.append(label(s, P.x0 + 4, 46, "SLS: τ" + sub("σ", s, "label2") + " = 0.05 s, τ" + sub("ε", s, "label2")
                   + " = 0.10 s, ε" + sub("0", s, "label2") + " = 1%", "label2", I["secondary"]))
    aria = (f"Problem K7 plot, two panels sharing a log frequency axis from 0.01 to 10000 radians per second. Top: the "
            f"loss tangent of the standard linear solid peaks at {tand[i]:.3f} at omega star = {w[i]:.2f}, on the dashed "
            f"line 1 over the square root of tau sigma tau epsilon, and is {td_at(0.1):.3f} at 0.1 and "
            f"{td_at(1000.0):.3f} at 1000. Bottom: the loop area per cycle is {Wd[i]:.1f} kilojoules per cubic metre at "
            f"omega star but peaks later, at {Wd[j]:.1f} at omega = 1 over tau sigma = {w[j]:.0f} radians per second.")
    k = list(range(0, len(w), 20))
    hp = [[P.X(lw[m]), P.Y(tand[m]), f"ω = {w[m]:.3g} rad/s: tan δ = {tand[m]:.3f}"] for m in k]
    hq = [[Q.X(lw[m]), Q.Y(Wd[m]), f"ω = {w[m]:.3g} rad/s: Wd = {Wd[m]:.1f} kJ/m³"] for m in k]
    return svg(VB, aria, s, "".join(o), ([(P.box, hp), (Q.box, hq)],))


# ---------------------------------------------------------------- #65 K8: resilience across cadence
TS8, ER8, E08 = 0.050, 1.20e9, 0.01


@lru_cache(None)
def k8_integrate(te, f=2.6, ncyc=8, dt=1.0e-5):
    """K8 resilience(), ported (math instead of numpy scalars): W_out/W_in of the last cycle."""
    w, per, s = 2 * math.pi * f, 1.0 / f, 0.0
    w_in = w_out = 0.0
    n = int(per / dt)
    for cyc in range(ncyc):
        for i in range(n):
            t = i * dt
            e = 0.5 * E08 * (1 - math.cos(w * t))
            ed = 0.5 * E08 * w * math.sin(w * t)
            s += dt * ((ER8 * (e + te * ed) - s) / TS8)
            if cyc == ncyc - 1:
                if ed > 0:
                    w_in += s * ed * dt
                else:
                    w_out -= s * ed * dt
    return w_out / w_in


def resilience(ratio, f):
    """Steady state of the same cycle: R = (4 - pi E''/E_R)/(4 + pi E''/E_R), E''/E_R = w(te - ts)/(1 + w^2 ts^2)."""
    w = 2 * np.pi * np.asarray(f)
    q = np.pi * w * TS8 * (ratio - 1) / (1 + (w * TS8)**2)
    return (4 - q) / (4 + q)


def fig65():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    r_int = [100 * k8_integrate(TS8 * r) for r in (1.10, 1.20)]
    r_cf = [100 * float(resilience(r, 2.6)) for r in (1.10, 1.20)]
    assert [round(v, 1) for v in r_int] == [92.6, 85.7] and max(abs(a - b) for a, b in zip(r_int, r_cf)) < 0.1, (r_int, r_cf)
    P = Plot(s, (58, 62, 388, 226), (1.0, 4.0), (80, 100))
    f = np.linspace(1.0, 4.0, 241)
    Rt, Rl = 100 * resilience(1.10, f), 100 * resilience(1.20, f)
    fmin = 1 / (2 * math.pi * TS8)
    o = [P.axes([(v, f"{v:g}") for v in (1, 1.5, 2, 2.5, 3, 3.5, 4)],
                [(80, "80"), (85, "85"), (90, "90"), (95, "95"), (100, "100")],
                "cadence f (Hz)", "resilience R (%)", grid=(85, 90, 95, 100))]
    o.append(H.line(s, P.X(2.6), P.y0, P.X(2.6), P.y1, O["dim"], "leader", H.DASH_REF))
    o.append(P.curve(f, Rt, SER[0], multi=True))
    o.append(P.curve(f, Rl, SER[1], multi=True))
    o.append(P.dot(2.6, r_cf[0], SER[0]))
    o.append(P.dot(2.6, r_cf[1], SER[1]))
    o.append(legend(s, 58, 20, [(SER[0], f"tendon, τ{sub('ε', s, 'label2')}/τ{sub('σ', s, 'label2')} = 1.10", None),
                                (SER[1], "ligament, 1.20", None)]))
    o.append(label(s, P.x0, 40, f"SLS, τ{sub('σ', s, 'label2')} = 0.05 s; minimum at f = 1/(2πτ{sub('σ', s, 'label2')})"
                   f" = {fmin:.2f} Hz", "label2", I["secondary"]))
    o.append(label(s, P.X(2.6) + 7, P.Y(r_cf[0]) - 8, f"{r_int[0]:.1f}%", "label2"))
    o.append(label(s, P.X(2.6) + 7, P.Y(r_cf[1]) - 8, f"{r_int[1]:.1f}%", "label2"))
    o.append(label(s, P.X(2.6) - 5, P.Y(81), "2.6 Hz", "label2", I["secondary"], "end"))
    aria = (f"Problem K8 plot: energy-return resilience against cadence from 1 to 4 hertz for a standard linear solid "
            f"with tau sigma 0.05 seconds and two time-constant ratios: a tendon at 1.10 and a ligament at 1.20. Both "
            f"curves dip shallowly to a minimum at {fmin:.2f} hertz; at the dashed 2.6 hertz cadence the tendon returns "
            f"{r_int[0]:.1f} percent and the ligament {r_int[1]:.1f} percent.")
    hv = hov(P, f, [Rt, Rl], lambda i: f"f = {f[i]:.2f} Hz: tendon {Rt[i]:.1f}%, ligament {Rl[i]:.1f}%")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #69 K10: energy banked by the plantar-fascia tie
def fig69():
    VB = (0, 0, W, 266)
    s = H.Scale(W, VB[3], display_w=400)
    M, g, b, h, k_PF = 80.0, 9.81, 0.15, 0.05, 2.0e5
    t = np.linspace(0.0, 1.0, 20001)
    Wl = 2.5 * M * g * np.sin(np.pi * t)
    T = Wl * b / (4 * h)
    x = T / k_PF
    U = 0.5 * T * x
    share = 100 * U.max() / (U.max() + 32)
    assert (round(T.max() / 1e3, 2), round(x.max() * 1e3, 2), round(U.max(), 2), round(share)) == (1.47, 7.36, 5.41, 14)
    P = Plot(s, (58, 42, 388, 206), (0, 1.0), (0, 6.0))
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1)], [(0, "0"), (2, "2"), (4, "4"), (6, "6")],
                "stance fraction", "arch energy U (J)", grid=(2, 4, 6))]
    o.append(P.curve(t, U, SER[0], nmax=200))
    o.append(P.dot(0.5, U.max(), SER[0]))
    o.append(label(s, P.X(0.5) + 9, P.Y(U.max()) - 8, f"peak {U.max():.2f} J", "label2"))
    for n, t_ in enumerate(("at 2.5 body weights:", f"tie tension {T.max() / 1e3:.2f} kN",
                            f"stretch {x.max() * 1e3:.2f} mm")):
        o.append(label(s, P.X(0.5), P.Y(2.8) + 16 * n, t_, "label2", I["secondary"], "middle"))
    o.append(label(s, P.x0, 22, f"Achilles 32 J (§3): the tie is {share:.0f}% of the pair", "label2", I["primary"]))
    aria = (f"Problem K10 plot: elastic energy in the plantar-fascia tie of the truss arch over one stance phase under a "
            f"half-sine load peaking at 2.5 body weights. The energy rises from zero to a peak of {U.max():.2f} joules at "
            f"mid-stance, where the tie tension is {T.max() / 1e3:.2f} kilonewtons and its stretch {x.max() * 1e3:.2f} "
            f"millimetres, and returns to zero; against the Achilles' 32 joules the tie is {share:.0f} percent of the pair.")
    k = list(range(0, len(t), 100))
    hv = [[P.X(t[m]), P.Y(U[m]), f"stance {t[m]:.2f}: U = {U[m]:.2f} J, T = {T[m]:.0f} N"] for m in k]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


FIGS = {
    51: ("force F (N) versus elongation x (mm)", fig51),
    53: ("force F (N) versus elongation x (mm)", fig53),
    55: ("fibre stretch δ (mm) versus MTU stretch S (mm)", fig55),
    57: ("energy return (norm.) versus leg stiffness k (kN/m)", fig57),
    59: ("stress σ (MPa) versus time t (s)", fig59),
    61: ("stress σ (MPa) versus time t (s)", fig61),
    63: ("loss tangent tan δ versus frequency ω (rad/s)", fig63),
    65: ("resilience R versus cadence ω (rad/s)", fig65),
    69: ("arch energy U (J) versus stance fraction", fig69),
}
