"""Module 4 main-text plots in the house style (group `plots_main`).

Every plotted number is computed here from the formula or the code the module states:
  the Donnan law (sec. 2 box, R_g Theta = 2577 J/mol), the Terzaghi series (Prop. 3.1),
  F(T) (sec. 4 eq. 1, summed as Lab 2's F()), Lab 1 (sec. 5 code, unchanged; only h, t0 and
  tmax vary in svg #16), Hertz and the load-conserving parabola (sec. 6 eq. 1 and the paragraph
  after it), the Stribeck model and mu_eff = mu_eq (1 - F) (Lab 2 code), the GAG stoichiometry
  c_F = 2m/458 (sec. 1) and Prop. 8.1.
All figures use a 760-unit-wide viewBox, so one user unit is one rendered px.
"""
import math
from functools import lru_cache

import numpy as np

import house as H
from m05.plots_main import Ax, axes, curve, dot, legend, hover, svg, mn, lead, DASH_SER, BOXFILL

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES


def sub(t, s):
    return H.sub(t, s, "label2")


def band(ax, x0, x1, col, op=0.12):
    return (f'<rect x="{ax.X(x0):.2f}" y="{ax.top:.2f}" width="{ax.X(x1)-ax.X(x0):.2f}" '
            f'height="{ax.y0-ax.top:.2f}" fill="{col}" opacity="{op}"/>')


def hband(ax, y0, y1, col, op=0.18):
    return (f'<rect x="{ax.x0:.2f}" y="{ax.Y(y1):.2f}" width="{ax.x1-ax.x0:.2f}" '
            f'height="{ax.Y(y0)-ax.Y(y1):.2f}" fill="{col}" opacity="{op}"/>')


SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def dec(e, unit=""):
    """Log-axis tick text 10^e (Unicode superscript)."""
    t = {0: "1", 1: "10"}.get(e, "10" + str(e).translate(SUP))
    return t + (f" {unit}" if unit else "")


def tticks():
    """0.1 s ... 10^5 s."""
    return [(10.0 ** e, {-1: "0.1 s"}.get(e, dec(e, "s"))) for e in range(-1, 6)]


def logspace(a, b, n):
    return [10 ** (math.log10(a) + (math.log10(b) - math.log10(a)) * i / (n - 1)) for i in range(n)]


def bisect(f, a, b, n=80):
    """Root of f on [a, b] (sign change), on a log scale when a > 0."""
    lg = a > 0
    lo, hi = (math.log10(a), math.log10(b)) if lg else (a, b)
    flo = f(10 ** lo if lg else lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(10 ** mid if lg else mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    m = (lo + hi) / 2
    return 10 ** m if lg else m


# ---------------------------------------------------------------- shared models (text values)
RT = 8.314 * 310                              # J/mol, sec. 2 "R_g Theta = 2577 J/mol"
C0 = 0.15                                     # M, bath
H0, HA, K0 = 2e-3, 0.6e6, 1e-15               # m, Pa, m^4/(N s): sec. 3 table
D0 = HA * K0                                  # 6e-10 m^2/s
TAU = H0 ** 2 / D0                            # 6667 s
MU_EQ = 0.15
LAM = (2 * np.arange(1500) + 1) * np.pi / 2   # Lab 2's F(): N = 1500 terms


def donnan(cf, c0=C0):
    """Sec. 2 box, cf and c0 in mol/L, pi in Pa."""
    return RT * (math.sqrt((1e3 * cf) ** 2 + 4 * (1e3 * c0) ** 2) - 2e3 * c0)


def Fsup(Tn):
    """Sec. 4 eq. (1)."""
    return float(np.sum(2 / LAM ** 2 * np.exp(-LAM ** 2 * Tn)))


def F_t(t, h=H0, k=K0):
    return Fsup(HA * k * t / h ** 2)


def pore(Z, Tn, n=400):
    """Prop. 3.1, p / sigma0 at Z = z/h."""
    lam = LAM[:n]
    return float(np.sum(2 * (-1.0) ** np.arange(n) / lam * np.cos(lam * Z) * np.exp(-lam ** 2 * Tn)))


@lru_cache(maxsize=None)
def lab1(h=H0, t0=200.0, tmax=20000.0):
    """Sec. 5 code, unchanged except h, t0, tmax. Returns t, sigma (Pa), sigma_inf (Pa)."""
    k = 1e-15
    D = HA * k
    eps0 = 0.10
    N = 50
    dz = h / N
    dt = 0.4 * dz ** 2 / D
    r = D * dt / dz ** 2
    assert r <= 0.5
    u = np.zeros(N + 1)
    Uh = eps0 * h
    t_hist, sig_hist = [], []
    for n in range(int(tmax / dt) + 1):
        t = n * dt
        u[0] = 0.0
        u[N] = Uh * min(t / t0, 1.0)
        sigma = HA * (3 * u[N] - 4 * u[N - 1] + u[N - 2]) / (2 * dz)
        t_hist.append(t)
        sig_hist.append(sigma)
        u[1:N] += r * (u[2:N + 1] - 2 * u[1:N] + u[0:N - 1])
    return np.array(t_hist), np.array(sig_hist), HA * eps0


def logpick(t, lo, hi, n=160):
    """Indices of t nearest a log-uniform grid on [lo, hi] (unique, sorted)."""
    idx = {int(np.argmin(np.abs(t - v))) for v in logspace(lo, hi, n)}
    return sorted(idx)


# Hertz / parabola (sec. 6)
R_J = 1715.0
E_STAR = 10e6 / (2 * (1 - 0.5 ** 2))          # 6.67 MPa
A_H = (3 * R_J * 0.030 / (4 * E_STAR)) ** (1 / 3)   # 17.95 mm
A_P = 1.3 * A_H                               # 23.3 mm
A_D = 0.016                                   # degenerate cap, sec. 8 caption


def hertz(r, a):
    p0 = 3 * R_J / (2 * math.pi * a ** 2)
    return p0 * math.sqrt(max(0.0, 1 - (r / a) ** 2))


def parab(r, a):
    pm = 2 * R_J / (math.pi * a ** 2)
    return pm * max(0.0, 1 - (r / a) ** 2)


def load_of(f, a, n=4000):
    """Integral of p 2 pi r dr (N), midpoint rule."""
    dr = a / n
    return sum(f((i + 0.5) * dr, a) * 2 * math.pi * (i + 0.5) * dr * dr for i in range(n))


# Stribeck (Lab 2)
MU_BL, S0, ALPHA = 0.15, 0.5, 0.012


def mu_S(S):
    return MU_BL / (1 + (S / S0) ** 2) + ALPHA * S


# ================================================================ svg #6: Donnan swelling pressure
def fig6():
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 60, 735, 330), (0, 0.4), (0, 0.55))
    cs = [0.4 * i / 80 for i in range(81)]
    p15 = [donnan(c) / 1e6 for c in cs]
    p30 = [donnan(c, 0.30) / 1e6 for c in cs]
    lo, op, hi = donnan(0.1) / 1e6, donnan(0.2) / 1e6, donnan(0.25) / 1e6
    o = [band(ax, 0.1, 0.25, BOXFILL, 1)]
    o += axes(s, ax, [(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3, 0.4)], [(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5)],
              f"fixed charge density c{sub('F', s)} (mol/L)", "swelling pressure π (MPa)")
    o.append(H.label(s, ax.X(0.175), ax.top + 18, "healthy range, c" + sub("F", s) + " ≈ 0.1–0.25 M", "label2", I["primary"], "middle"))
    o.append(curve(s, ax, cs, p30, SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, ax, cs, p15, SER[0], "curve_multi"))
    o.append(H.line(s, ax.X(0.2), ax.Y(op), ax.X(0.2), ax.y0, I["secondary"], "leader", (3, 3)))
    o.append(H.line(s, ax.x0, ax.Y(op), ax.X(0.2), ax.Y(op), I["secondary"], "leader", (3, 3)))
    for c, p in ((0.1, lo), (0.25, hi)):
        o.append(dot(s, ax.X(c), ax.Y(p), SER[0], hollow=True))
    o.append(dot(s, ax.X(0.2), ax.Y(op), SER[0]))
    o.append(H.label(s, ax.X(0.2) - 10, ax.Y(op) - 30, f"operating point: c{sub('F', s)} = 0.2 M,", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(0.2) - 10, ax.Y(op) - 14, f"π = {op:.3f} MPa ≈ 0.16", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(0.1) - 8, ax.Y(lo) - 8, f"{lo:.3f}", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(0.25) + 9, ax.Y(hi) + 14, f"{hi:.3f} MPa", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(0.335), ax.Y(donnan(0.35) / 1e6), f"c{sub('0', s)} = 0.15 M", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(0.33), ax.Y(donnan(0.33, 0.30) / 1e6) + 22, f"c{sub('0', s)} = 0.30 M", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.012), ax.Y(0.05), f"π → 0 as c{sub('F', s)} → 0", "label2", I["secondary"]))
    o += legend(s, ax.x0, 30, [(SER[0], None, f"bath c{sub('0', s)} = 0.15 M (physiological)"),
                               (SER[1], DASH_SER, f"bath c{sub('0', s)} = 0.30 M (more salt: screened)")])
    aria = (f"Donnan swelling pressure in megapascals against fixed charge density from 0 to 0.4 mol per litre, from the boxed "
            f"formula at body temperature. The solid red curve for a 0.15 molar bath passes {lo:.3f} MPa at 0.1 M, the "
            f"operating point {op:.3f} MPa at 0.2 M, {hi:.3f} MPa at 0.25 M and {donnan(0.4)/1e6:.2f} MPa at 0.4 M. A shaded "
            f"band marks the healthy range 0.1 to 0.25 M. The dashed blue curve for a 0.30 molar bath lies lower everywhere "
            f"({donnan(0.2, 0.3)/1e6:.3f} MPa at 0.2 M): added salt screens the fixed charge. Both curves start at zero with no charge.")
    hv = hover(ax, [ax.X(c) for c in cs], [[ax.Y(a), ax.Y(b)] for a, b in zip(p15, p30)],
               [f"cF = {c:.3f} M: π = {a:.3f} MPa (c0 0.15 M), {b:.3f} MPa (c0 0.30 M)" for c, a, b in zip(cs, p15, p30)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #9: Terzaghi profiles
T9 = (0.05, 0.1, 0.2, 0.5, 1.0)


def tmin(Tn):
    t = Tn * TAU
    return f"{t/60:.0f} min" if t < 3600 else f"{t/3600:.1f} h"


def fig9():
    p = "m4f9_"
    VB = (0, 0, 760, 430)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((110, 70, 640, 350), (0, 1.08), (0, 1))
    Zs = [i / 50 for i in range(51)]
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, ax, [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1.0)], [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1.0)],
              f"pore pressure p/σ{sub('0', s)} (fluid's share)", "height z/h above the sealed base", grid=False)
    # top scale: the solid's share at the same depth, sigma_E / sigma0 = 1 - p / sigma0
    o.append(H.line(s, ax.x0, ax.top, ax.x1, ax.top, I["axis"], "axis"))
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        o.append(H.line(s, ax.X(v), ax.top, ax.X(v), ax.top - 5, I["axis"], "leader"))
        o.append(H.label(s, ax.X(v), ax.top - 10, f"{1 - v:g}", "tick", I["secondary"], "middle"))
    o.append(H.label(s, (ax.x0 + ax.x1) / 2, ax.top - 32, f"solid's share σ{sub('E', s)}/σ{sub('0', s)} = 1 − p/σ{sub('0', s)}",
                     "label", I["primary"], "middle"))
    o.append(H.line(s, ax.X(1.0), ax.y0, ax.X(1.0), ax.top, I["primary"], "curve_multi"))
    o.append(H.label(s, ax.X(1.0) + 10, ax.Y(0.55), "t = 0⁺:", "label2", I["primary"]))
    o.append(H.label(s, ax.X(1.0) + 10, ax.Y(0.55) + 16, "fluid carries", "label2", I["primary"]))
    o.append(H.label(s, ax.X(1.0) + 10, ax.Y(0.55) + 32, "all, p = σ" + sub("0", s), "label2", I["primary"]))
    prof = {Tn: [pore(Z, Tn) for Z in Zs] for Tn in T9}
    for Tn in T9:
        o.append(curve(s, ax, prof[Tn], Zs, SER[1], "curve_multi"))
    # label each profile at its base value (p at z = 0, the slowest point to drain)
    for Tn, yr in zip(T9, (0.24, 0.12, None, None, None)):
        pb = prof[Tn][0]
        o.append(dot(s, ax.X(pb), ax.y0, SER[1]))
        if yr is None:
            o.append(H.label(s, ax.X(pb) - 6, ax.y0 - 16, f"T = {Tn:g} ({tmin(Tn)})", "label2", I["primary"], "end"))
        else:                                          # the two near p = 1: labelled right of the plot, with a leader
            o.append(H.line(s, ax.X(pb) + 3, ax.y0 - 3, ax.x1 + 8, ax.Y(yr) + 4, I["rule"], "leader"))
            o.append(H.label(s, ax.x1 + 11, ax.Y(yr) + 4, f"T = {Tn:g} ({tmin(Tn)})", "label2", I["primary"]))
    o.append(H.arrow(s, p, ax.X(0.86), ax.Y(0.80), ax.X(0.50), ax.Y(0.80), "dim"))
    o.append(H.label(s, ax.X(0.68), ax.Y(0.80) - 9, "time T = Dt/h² increases", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.x1 - 4, ax.top + 18, "drained platen, p = 0 at z = h", "label2", I["secondary"], "end"))
    aria = ("Pore-pressure depth profiles from the Terzaghi series of Proposition 3.1. Horizontal axis: pore pressure over "
            "the applied stress, the fluid's share; the top scale reads the solid's share, one minus it. Vertical axis: height "
            "above the sealed base, with the drained platen at the top where the pressure is zero. At t = 0+ the profile is "
            "the vertical line at 1: the fluid carries everything. Five blue profiles at dimensionless times T = 0.05, 0.1, "
            f"0.2, 0.5 and 1 ({tmin(0.05)}, {tmin(0.1)}, {tmin(0.2)}, {tmin(0.5)}, {tmin(1.0)} for 2 mm healthy cartilage) "
            "drain from the top down; the base pressure falls from "
            f"{prof[0.05][0]:.3f} to {prof[0.1][0]:.2f}, {prof[0.2][0]:.2f}, {prof[0.5][0]:.2f} and {prof[1.0][0]:.2f}.")
    hp = []
    for Tn in T9:
        for k in range(0, 51, 2):
            hp.append([ax.X(prof[Tn][k]), ax.Y(Zs[k]), f"T = {Tn:g}, z/h = {Zs[k]:.2f}: p/σ0 = {prof[Tn][k]:.3f}"])
    hp.sort(key=lambda q: q[0])
    return svg(VB, aria, s, o, H.hover_attr([round(v, 2) for v in ax.box], hp))


# ================================================================ svg #10: fluid load support F(t)
def fig10():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 50, 735, 320), (0.1, 1e5), (0, 1.05), xlog=True)
    ts = logspace(0.1, 1e5, 121)
    Fs = [F_t(t) for t in ts]
    t90 = bisect(lambda t: F_t(t) - 0.9, 1, 1000)
    te = bisect(lambda t: F_t(t) - 1 / math.e, 100, 1e4)
    f1 = F_t(1.0)
    o = [band(ax, 0.1, t90, BOXFILL, 1)]
    o += axes(s, ax, tticks(), [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1.0)], "time under load (log scale)",
              f"fluid load support F = ⟨p⟩/σ{sub('0', s)}")
    o.append(H.line(s, ax.X(TAU), ax.top, ax.X(TAU), ax.y0, I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(TAU) + 6, ax.Y(0.80), "gel time", "label2", I["primary"]))
    o.append(H.label(s, ax.X(TAU) + 6, ax.Y(0.80) + 16, f"τ = h²/D = {TAU:.0f} s", "label2", I["primary"]))
    o.append(H.label(s, ax.X(TAU) + 6, ax.Y(0.80) + 32, f"≈ {TAU/3600:.1f} h", "label2", I["primary"]))
    o.append(curve(s, ax, ts, Fs, SER[1]))
    o.append(dot(s, ax.X(1.0), ax.Y(f1), SER[1]))
    o.append(lead(s, ax.X(1.0), ax.Y(f1) + 5, ax.X(1.0), ax.Y(0.80) - 12, SER[1]))
    o.append(H.label(s, ax.X(1.0), ax.Y(0.80), "footstep, 1 s:", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(1.0), ax.Y(0.80) + 16, f"F = {f1:.3f}", "label2", I["primary"], "middle"))
    o.append(dot(s, ax.X(te), ax.Y(1 / math.e), SER[1]))
    o.append(H.label(s, ax.X(te) - 10, ax.Y(1 / math.e) + 4, f"F = 1/e at {te:.0f} s ≈ {te/60:.0f} min", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(np.sqrt(0.1 * t90)), ax.Y(0.20), "steps & gait:", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(np.sqrt(0.1 * t90)), ax.Y(0.20) + 16, f"F ≥ 0.9 up to {t90:.0f} s", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(np.sqrt(0.1 * t90)), ax.Y(0.55), "fluid carries", "label2", I["secondary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, ax.X(np.sqrt(0.1 * t90)), ax.Y(0.55) + 16, "the load", "label2", I["secondary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, ax.X(3e4), ax.Y(0.30), "solid matrix", "label2", I["secondary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, ax.X(3e4), ax.Y(0.30) + 16, "carries the load", "label2", I["secondary"], "middle", 'font-style="italic"'))
    aria = (f"Fluid load support F against time under load on a log axis from 0.1 second to 100000 seconds, equation 1 for "
            f"2 mm healthy cartilage. F stays near 1, is {f1:.3f} at a 1 second footstep, falls below 0.9 at {t90:.0f} seconds "
            f"(the shaded band of steps and gait), passes 1/e at {te:.0f} seconds, about {te/60:.0f} minutes, and is "
            f"{F_t(TAU):.3f} at the gel time of {TAU:.0f} seconds, about {TAU/3600:.1f} hours, marked by a dashed line.")
    hv = hover(ax, [ax.X(t) for t in ts], [ax.Y(f) for f in Fs],
               [f"t = {t:.3g} s: F = {f:.3f}, solid share {1 - f:.3f}" for t, f in zip(ts, Fs)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #11: who carries the load
def fig11():
    VB = (0, 0, 760, 360)
    s = H.Scale(VB[2], VB[3])
    cases = [("footstep", "1 s", 1.0), ("held 45 min", "2700 s", 2700.0), ("held 6 h (drained)", "21 600 s", 21600.0)]
    y0, ytop, bw = 285, 60, 96
    hgt = y0 - ytop
    o = [H.line(s, 40, y0, 720, y0, I["axis"], "axis")]
    hv = []
    for i, (name, tt, t) in enumerate(cases):
        f = F_t(t)
        xc = 125 + 225 * i
        yf = y0 - f * hgt
        o.append(f'<rect x="{xc-bw/2:.2f}" y="{yf:.2f}" width="{bw}" height="{y0-yf:.2f}" fill="{T["fluid"][0]}" '
                 f'stroke="{T["fluid"][1]}" stroke-width="{s(1.2):.2f}"/>')
        o.append(f'<rect x="{xc-bw/2:.2f}" y="{ytop}" width="{bw}" height="{yf-ytop:.2f}" fill="{T["bone"][1]}"/>')
        fl = f"{100*f:.1f} %" if f > 0.01 else f"{100*f:.2f} %"
        sl = f"{100*(1-f):.1f} %" if 1 - f < 0.999 else "100 %"
        yfl = (yf + y0) / 2 if f > 0.12 else y0 - 12
        ysl = (ytop + yf) / 2 if 1 - f > 0.12 else ytop + 12
        o.append(H.label(s, xc + bw / 2 + 8, yfl + 5, f"fluid {fl}", "label2", I["primary"]))
        o.append(H.label(s, xc + bw / 2 + 8, ysl + 5, f"solid {sl}", "label2", I["primary"]))
        o.append(H.label(s, xc, y0 + 22, name, "label", I["primary"], "middle"))
        o.append(H.label(s, xc, y0 + 40, f"t = {tt}, F = {f:.4f}" if f < 0.01 else f"t = {tt}, F = {f:.3f}", "label2",
                         I["secondary"], "middle"))
        hv.append([xc, yf, f"{name}: fluid {100*f:.2f} %, solid {100*(1-f):.2f} %"])
    o += legend(s, 40, 32, [(T["fluid"][0], None, "interstitial fluid, pore pressure p (share F)", "band"),
                            (T["bone"][1], None, f"solid matrix, effective stress σ{sub('E', s)} (share 1 − F)", "band")])
    # legend 'band' swatches are drawn at 0.22 opacity: repaint them solid to match the bars
    o = [x.replace('opacity="0.22"', 'opacity="1"') for x in o]
    aria = (f"Stacked bars of the share of load carried by the interstitial fluid (light blue, bottom) and by the solid "
            f"matrix (light brown, top), from equation 1 for 2 mm healthy cartilage. Footstep, 1 s: fluid {100*F_t(1):.1f} percent, "
            f"solid {100*(1-F_t(1)):.1f}. Held 45 minutes: fluid {100*F_t(2700):.1f}, solid {100*(1-F_t(2700)):.1f}. Held 6 hours: "
            f"fluid {100*F_t(21600):.2f}, the solid carries essentially all of it.")
    box = [40, ytop, 720, y0]
    return svg(VB, aria, s, o, H.hover_attr(box, hv))


# ================================================================ svg #15: Lab 1 stress relaxation
def fig15():
    VB = (0, 0, 760, 460)
    s = H.Scale(VB[2], VB[3])
    t, sig, sinf = lab1()
    tmax = float(t[-1])
    A = Ax((90, 40, 735, 120), (10, 2e4), (0, 1.15), xlog=True)
    B = Ax((90, 160, 735, 390), (10, 2e4), (0, 7.2), xlog=True)
    xt = [(v, txt) for v, txt in ((10, "10 s"), (100, "100 s"), (1e3, dec(3, "s")), (1e4, dec(4, "s")), (2e4, ""))]
    strain = [min(x / 200.0, 1.0) for x in t]
    rat = sig / sinf
    kp = int(np.argmax(rat))
    o = axes(s, A, [(v, "") for v, _ in xt], [(0, "0"), (1, "1")], None, f"ε/ε{sub('0', s)}", ylab_x=40)
    o += axes(s, B, xt, [(v, f"{v}") for v in (0, 2, 4, 6)], "time (log scale)", f"stress σ/σ{sub('∞', s)}", ylab_x=40)
    o.append(H.label(s, B.X(2e4), B.y0 + 20, "2×" + dec(4, "s"), "tick", I["secondary"], "middle"))
    for ax in (A, B):
        o.append(H.line(s, ax.X(TAU), ax.top, ax.X(TAU), ax.y0, I["secondary"], "ref", H.DASH_REF))
    o.append(H.line(s, B.x0, B.Y(1.0), B.x1, B.Y(1.0), I["secondary"], "ref", H.DASH_REF))
    sel = logpick(t, 10, tmax, 110) + [kp]
    sel = sorted(set(sel))
    o.append(curve(s, A, [t[k] for k in sel], [strain[k] for k in sel], SER[1], "curve_multi"))
    o.append(curve(s, B, [t[k] for k in sel], [rat[k] for k in sel], SER[0]))
    o.append(dot(s, B.X(t[kp]), B.Y(rat[kp]), SER[0]))
    an = 2 * H0 / math.sqrt(math.pi * D0 * 200.0)
    o.append(H.label(s, B.X(t[kp]) + 12, B.Y(rat[kp]) + 4, f"peak {rat[kp]:.3f} σ{sub('∞', s)} = {rat[kp]*sinf/1e6:.2f} MPa,",
                     "label2", I["primary"]))
    o.append(H.label(s, B.X(t[kp]) + 12, B.Y(rat[kp]) + 20, f"t = {t[kp]:.0f} s, end of the ramp", "label2", I["primary"]))
    o.append(H.label(s, B.X(t[kp]) + 12, B.Y(rat[kp]) + 36, f"(N = 50 grid; analytic 2h/√(πDt₀) = {an:.3f})", "label2", I["secondary"]))
    o.append(H.label(s, B.X(700), B.Y(3.6), "fluid exudes:", "label2", I["secondary"], "start", 'font-style="italic"'))
    o.append(H.label(s, B.X(700), B.Y(3.6) + 16, "relaxes to the drained matrix", "label2", I["secondary"], "start", 'font-style="italic"'))
    o.append(H.label(s, B.X(12), B.Y(1.0) + 19, f"σ{sub('∞', s)} = H{sub('A', s)}ε{sub('0', s)} = {sinf/1e6:.3f} MPa (drained matrix)",
                     "label2", I["primary"]))
    o.append(H.label(s, A.X(TAU) - 6, A.Y(0.45), f"gel time τ = h²/D = {TAU:.0f} s ≈ {TAU/3600:.1f} h", "label2", I["primary"], "end"))
    o.append(H.label(s, A.X(14), A.Y(0.30), "ramp, t₀ = 200 s", "label2", I["primary"]))
    o.append(H.label(s, A.X(800), A.Y(1.0) - 8, f"strain held at ε{sub('0', s)} = 0.10", "label2", I["primary"], "middle"))
    aria = (f"Two panels sharing a log time axis from 10 seconds to 20000 seconds, from the Lab 1 code. Top: the platen "
            f"strain over its held value ramps linearly to 1 at 200 seconds and is then held. Bottom: the reaction stress over "
            f"the drained value rises during the ramp to a peak of {rat[kp]:.2f} times sigma infinity, {rat[kp]*sinf/1e6:.2f} MPa, "
            f"at 200 seconds, then relaxes to sigma infinity = {sinf/1e6:.3f} MPa (dashed line) over the gel time of "
            f"{TAU:.0f} seconds (dashed vertical line); at the end of the run it is {rat[-1]:.3f} times sigma infinity.")
    hk = logpick(t, 10, tmax, 150)
    hv = H.hover_attr([
        ([round(v, 2) for v in A.box], [[round(A.X(t[k]), 2), round(A.Y(strain[k]), 2),
                                         f"t = {t[k]:.0f} s: ε/ε0 = {strain[k]:.3f}"] for k in hk]),
        ([round(v, 2) for v in B.box], [[round(B.X(t[k]), 2), round(B.Y(rat[k]), 2),
                                         f"t = {t[k]:.0f} s: σ/σ∞ = {rat[k]:.3f} ({rat[k]*sinf/1e6:.3f} MPa)"] for k in hk])])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #16: thickness sensitivity
HS = ((1e-3, SER[1]), (2e-3, SER[0]), (3e-3, SER[2]))


def fig16():
    p = "m4f16_"
    VB = (0, 0, 760, 410)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 60, 735, 330), (10, 1e5), (0, 7.2), xlog=True)
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, ax, [(10.0 ** e, dec(e, "s") if e > 1 else "10 s") for e in range(1, 6)], [(v, f"{v}") for v in (0, 2, 4, 6)],
              "time (log scale)", f"stress σ/σ{sub('∞', s)}")
    o.append(H.line(s, ax.x0, ax.Y(1.0), ax.x1, ax.Y(1.0), I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(1.2e4), ax.Y(1.0) - 8, f"σ{sub('∞', s)} = H{sub('A', s)}ε{sub('0', s)} for every h", "label2", I["primary"]))
    runs, items, peaks, hv_runs = [], [], [], []
    for h, col in HS:
        t0 = 200.0 * (h / H0) ** 2
        t, sig, sinf = lab1(h, t0, 1e5)
        rat = sig / sinf
        kp = int(np.argmax(rat))
        sel = sorted(set(logpick(t, 10, 1e5, 110) + [kp]))
        runs.append(curve(s, ax, [t[k] for k in sel], [rat[k] for k in sel], col, "curve_multi"))
        tau = h ** 2 / D0
        tt = f"{tau/60:.0f} min" if tau < 3600 else f"{tau/3600:.1f} h"
        items.append((col, None, f"h = {h*1e3:.0f} mm: t₀ = {t0:.0f} s, τ = {tau:.0f} s ≈ {tt}"))
        peaks.append((t[kp], rat[kp], col, h))
        hv_runs.append((t, rat))
    o += runs
    for tp, rp, col, h in peaks:
        o.append(dot(s, ax.X(tp), ax.Y(rp), col))
    for (ta, ra, _, ha), (tb, rb, _, hb) in zip(peaks, peaks[1:]):
        y = ax.Y(6.85)
        o.append(H.line(s, ax.X(ta) + 5, y, ax.X(tb) - 5, y, O["geometry"], "geom",
                        extra=f'marker-start="url(#{p}a_geometry)" marker-end="url(#{p}a_geometry)"'))
        o.append(H.label(s, (ax.X(ta) + ax.X(tb)) / 2, y - 8, f"×{(hb/ha)**2:.2f}".rstrip("0").rstrip("."), "label2",
                         I["primary"], "middle"))
    o.append(H.label(s, ax.X(peaks[0][0]) - 8, ax.Y(peaks[0][1]) + 4, f"{peaks[0][1]:.2f}", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(1.5e3), ax.Y(5.2), "same peak, same shape:", "label2", I["secondary"], "start", 'font-style="italic"'))
    o.append(H.label(s, ax.X(1.5e3), ax.Y(5.2) + 16, "each curve slides right by (h₂/h₁)²", "label2", I["secondary"], "start",
                     'font-style="italic"'))
    for k, it_ in enumerate(items):
        o += legend(s, ax.X(1.5e3), ax.Y(4.2) + k * 20, [it_])
    aria = ("Three stress-relaxation curves from the Lab 1 code for layer thicknesses 1, 2 and 3 mm, the ramp time scaled "
            "with h squared (50, 200 and 450 seconds) so the peaks coincide at "
            f"{peaks[0][1]:.2f}, {peaks[1][1]:.2f} and {peaks[2][1]:.2f} times sigma infinity. On the log time axis the curves "
            "are the same shape shifted right by a factor 4 from 1 to 2 mm and 2.25 from 2 to 3 mm; the gel times are "
            "1667, 6667 and 15000 seconds, about 28 minutes, 1.9 hours and 4.2 hours. All relax to the same sigma infinity.")
    grid = logspace(10, 1e5, 150)
    hp = []
    for v in grid:
        ys, tx = [], []
        for (t, rat), (h, _) in zip(hv_runs, HS):
            k = int(np.argmin(np.abs(t - v)))
            ys.append(ax.Y(rat[k]))
            tx.append(f"{h*1e3:.0f} mm {rat[k]:.2f}")
        hp.append([ax.X(v), ys, f"t = {v:.3g} s: σ/σ∞ " + ", ".join(tx)])
    return svg(VB, aria, s, o, H.hover_attr([round(v, 2) for v in ax.box], hp))


# ================================================================ svg #18: Hertz vs biphasic
def contact(idx, aria, curves, ymax, notes):
    p = f"m4f{idx}_"
    VB = (0, 0, 760, 410)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 60, 735, 330), (-27, 27), (0, ymax))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, ax, [(v, mn(v, "{:.0f}")) for v in (-20, -10, 0, 10, 20)],
              [(v, f"{v:g}") for v in np.arange(0, ymax + 0.01, 1.0)], "radial position r (mm)", "contact pressure p (MPa)")
    rs = [-27 + 54 * i / 540 for i in range(541)]
    vals = []
    for f, a, col, _ in curves:
        ys = [f(r / 1e3, a) / 1e6 for r in rs]
        vals.append(ys)
        rr = [a * 1e3 * math.sin(math.pi * (j / 60 - 0.5)) for j in range(61)]   # dense at the rim
        pts = [(r, f(r / 1e3, a) / 1e6) for r in rr]
        o.append(curve(s, ax, [q[0] for q in pts], [q[1] for q in pts], col, "curve_multi"))
    o += notes(s, ax, p)
    o += legend(s, ax.x0, 30, [(col, None, txt) for _, _, col, txt in curves])
    hv = hover(ax, [ax.X(r) for r in rs[::3]], [[ax.Y(v[i]) for v in vals] for i in range(0, len(rs), 3)],
               [f"r = {rs[i]:.1f} mm: " + ", ".join(f"{v[i]:.2f}" for v in vals) + " MPa" for i in range(0, len(rs), 3)])
    return svg(VB, aria, s, o, hv)


def halfwidth(s, ax, p, a_mm, y, text, side):
    """Dimension arrow from r = 0 to r = side * a, label above it."""
    o = [H.line(s, ax.X(0), ax.Y(y), ax.X(side * a_mm), ax.Y(y), O["geometry"], "geom",
                extra=f'marker-start="url(#{p}a_geometry)" marker-end="url(#{p}a_geometry)"')]
    o.append(H.label(s, ax.X(side * a_mm / 2), ax.Y(y) - 8, text, "label2", I["primary"], "middle"))
    return o


def fig18():
    ph, pm = hertz(0, A_H) / 1e6, parab(0, A_P) / 1e6
    pbar = R_J / (math.pi * A_H ** 2) / 1e6
    LH, LP = load_of(hertz, A_H), load_of(parab, A_P)
    assert abs(LH - R_J) < 1 and abs(LP - R_J) < 1

    def notes(s, ax, p):
        o = [H.line(s, ax.x0, ax.Y(pbar), ax.x1, ax.Y(pbar), I["secondary"], "ref", H.DASH_REF)]
        o.append(H.label(s, ax.X(26.5), ax.Y(pbar) - 8, f"mean p̄ = R/πa² = {pbar:.2f} MPa", "label2", I["primary"], "end"))
        o.append(dot(s, ax.X(0), ax.Y(ph), SER[0]))
        o.append(dot(s, ax.X(0), ax.Y(pm), SER[1]))
        o.append(H.label(s, ax.X(0), ax.Y(ph) - 12, f"Hertz peak p₀ = 1.5 p̄ = {ph:.2f} MPa", "label2", I["primary"], "middle"))
        o.append(H.label(s, ax.X(0), ax.Y(pm) - 9, f"biphasic peak {pm:.2f} MPa", "label2", I["primary"], "middle"))
        o += halfwidth(s, ax, p, A_H * 1e3, 0.35, f"a = {A_H*1e3:.1f} mm", 1)
        o += halfwidth(s, ax, p, A_P * 1e3, 0.35, f"a′ = 1.3a = {A_P*1e3:.1f} mm", -1)
        o.append(H.label(s, ax.X(0), ax.Y(1.05), f"both carry ∫p·2πr dr = {R_J:.0f} N", "label2", I["secondary"], "middle"))
        return o
    curves = [(hertz, A_H, SER[0], f"Hertz cap, dry elastic: p₀√(1 − r²/a²)"),
              (parab, A_P, SER[1], "biphasic: flatter parabola on a′ = 1.3a")]
    aria = (f"Contact pressure against radial position for one load R = 1715 N, two models. Red: the Hertz elastic cap on a "
            f"contact radius a = {A_H*1e3:.1f} mm, peak {ph:.2f} MPa, half again the mean {pbar:.2f} MPa (dashed line). Blue: the "
            f"biphasic parabola on a' = 1.3a = {A_P*1e3:.1f} mm, lower and wider, peak {pm:.2f} MPa. Each profile integrates "
            f"(p times 2 pi r dr) to {LH:.0f} N and {LP:.0f} N.")
    return contact(18, aria, curves, 3.0, notes)


# ================================================================ svg #26: healthy vs degraded
def fig26():
    pm, pd = parab(0, A_P) / 1e6, hertz(0, A_D) / 1e6
    LP, LD = load_of(parab, A_P), load_of(hertz, A_D)
    assert abs(LP - R_J) < 1 and abs(LD - R_J) < 1

    def notes(s, ax, p):
        o = [dot(s, ax.X(0), ax.Y(pd), SER[0]), dot(s, ax.X(0), ax.Y(pm), SER[1])]
        o.append(H.label(s, ax.X(0), ax.Y(pd) - 12, f"degenerate: p₀ = 3R/(2πa²) = {pd:.2f} MPa", "label2", I["primary"], "middle"))
        o.append(H.label(s, ax.X(0), ax.Y(pm) - 9, f"healthy: 2R/(πa′²) = {pm:.2f} MPa", "label2", I["primary"], "middle"))
        o += halfwidth(s, ax, p, A_D * 1e3, 0.35, f"a = {A_D*1e3:.0f} mm (worn)", 1)
        o += halfwidth(s, ax, p, A_P * 1e3, 0.35, f"a′ = {A_P*1e3:.1f} mm", -1)
        o.append(H.label(s, ax.X(0), ax.Y(1.25), f"both carry ∫p·2πr dr = {R_J:.0f} N", "label2", I["secondary"], "middle"))
        return o
    curves = [(hertz, A_D, SER[0], "fluid support lost: Hertz cap on a worn contact"),
              (parab, A_P, SER[1], "fluid support intact: parabola of §6")]
    aria = (f"Contact pressure against radial position, same load 1715 N. Blue: the healthy joint, fluid support intact, the "
            f"flat parabola of section 6 on a' = {A_P*1e3:.1f} mm with peak {pm:.2f} MPa. Red: fluid support lost, a Hertzian cap "
            f"on a contact shrunk by wear to a = {A_D*1e3:.0f} mm, peak {pd:.2f} MPa. Both integrate to {LP:.0f} and {LD:.0f} N: "
            "the same force, focused.")
    return contact(26, aria, curves, 3.5, notes)


# ================================================================ svg #20: Stribeck curve
def fig20():
    p = "m4f20_"
    VB = (0, 0, 760, 430)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 60, 735, 330), (1e-4, 10), (0, 0.18), xlog=True)
    Ss = list(np.logspace(-4, 1, 300))                 # Lab 2's grid
    mus = [mu_S(x) for x in Ss]
    km = int(np.argmin(mus))
    s_bl = S0 / 3                                      # boundary term = 0.9 mu_bl
    s_ff = bisect(lambda x: ALPHA * x - MU_BL / (1 + (x / S0) ** 2), 0.1, 5)   # film term = boundary term
    o = [f"<defs>{H.markers(p, s)}</defs>", band(ax, 1e-4, s_bl, BOXFILL, 1), band(ax, s_ff, 10, BOXFILL, 1),
         hband(ax, 0.005, 0.02, SER[1])]
    o += axes(s, ax, [(10.0 ** e, dec(e)) for e in range(-4, 2)], [(v, f"{v:.2f}") for v in (0, 0.05, 0.10, 0.15)],
              "Stribeck number S = ηU/N (log scale)", "friction coefficient μ")
    for x, txt in ((10 ** -2.4, "boundary"), (math.sqrt(s_bl * s_ff), "mixed"), (math.sqrt(s_ff * 10), "fluid-film")):
        o.append(H.label(s, ax.X(x), ax.top + 18, txt, "label2", I["primary"], "middle"))
    o.append(curve(s, ax, sorted(Ss[::3] + [Ss[km], Ss[-1]]), [mu_S(x) for x in sorted(Ss[::3] + [Ss[km], Ss[-1]])], SER[0]))
    o.append(dot(s, ax.X(Ss[km]), ax.Y(mus[km]), SER[0]))
    o.append(H.label(s, ax.X(Ss[km]), ax.Y(mus[km]) + 22, f"minimum μ = {mus[km]:.3f}", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(Ss[km]), ax.Y(mus[km]) + 38, f"at S = {Ss[km]:.2f}", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(1.3e-4), ax.Y(MU_BL) + 20, f"plateau μ ≈ μ{sub('bl', s)} = {MU_BL}", "label2", I["primary"]))
    o.append(H.label(s, ax.X(1.3e-4), ax.Y(0.0125) + 5, "cartilage, measured μ = 0.005–0.02", "label2", I["primary"]))
    xa = 10 ** -2.5
    o.append(H.line(s, ax.X(xa), ax.Y(0.02) - 2, ax.X(xa), ax.Y(MU_BL) + 4, O["geometry"], "geom",
                    extra=f'marker-start="url(#{p}a_geometry)" marker-end="url(#{p}a_geometry)"'))
    o.append(H.label(s, ax.X(xa) + 8, ax.Y(0.09), "×30 the measured 0.005", "label2", I["primary"]))
    o.append(H.label(s, ax.X(xa) + 8, ax.Y(0.09) + 16, "at low S: standing,", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(xa) + 8, ax.Y(0.09) + 32, "slow load, heel-strike", "label2", I["secondary"]))
    o.append(H.label(s, (ax.x0 + ax.x1) / 2, ax.y0 + 66,
                     f"regime edges from the model: boundary term ≥ 0.9 μ{sub('bl', s)} for S ≤ {s_bl:.2f}; "
                     f"film term αS above it for S ≥ {s_ff:.2f}", "label2", I["secondary"], "middle"))
    aria = (f"Stribeck curve from the Lab 2 model, friction coefficient against the Stribeck number on a log axis from "
            f"0.0001 to 10. Friction sits on the boundary plateau 0.15 at low S, falls through the mixed regime to a minimum of "
            f"{mus[km]:.3f} at S = {Ss[km]:.2f}, then rises with viscous drag to {mus[-1]:.3f} at S = 10. Shaded columns mark the "
            f"boundary regime (S up to {s_bl:.2f}) and the fluid-film regime (S from {s_ff:.2f}). A blue band at 0.005 to 0.02 "
            "is measured cartilage friction: at low S the classical curve is 30 times the measured 0.005.")
    hv = hover(ax, [ax.X(x) for x in Ss], [ax.Y(m) for m in mus], [f"S = {x:.3g}: μ = {m:.4f}" for x, m in zip(Ss, mus)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #22: biphasic friction vs time
def fig22():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 50, 735, 320), (0.1, 1e5), (0, 0.17), xlog=True)
    ts = logspace(0.1, 1e5, 121)
    mus = [MU_EQ * (1 - F_t(t)) for t in ts]
    t90 = bisect(lambda t: F_t(t) - 0.9, 1, 1000)
    o = [band(ax, 0.1, t90, BOXFILL, 1)]
    o += axes(s, ax, tticks(), [(v, f"{v:.2f}") for v in (0, 0.05, 0.10, 0.15)], "time under static load (log scale)",
              f"effective friction μ{sub('eff', s)} = μ{sub('eq', s)}(1 − F)")
    o.append(H.line(s, ax.x0, ax.Y(MU_EQ), ax.x1, ax.Y(MU_EQ), I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(0.13), ax.Y(MU_EQ) - 8, f"μ{sub('eq', s)} = {MU_EQ} (drained solid)", "label2", I["primary"]))
    o.append(H.line(s, ax.X(TAU), ax.top, ax.X(TAU), ax.y0, I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(TAU) + 6, ax.Y(0.06), f"gel time τ = {TAU:.0f} s", "label2", I["primary"]))
    o.append(curve(s, ax, ts, mus, SER[0]))
    lab = [(1, "start", 10, -12), (60, "start", 10, 18), (3600, "end", -10, -4), (20000, "start", 6, 20)]
    for t, anc, dx, dy in lab:                          # Lab 2's four printed times
        m = MU_EQ * (1 - F_t(t))
        o.append(dot(s, ax.X(t), ax.Y(m), SER[0]))
        o.append(H.label(s, ax.X(t) + dx, ax.Y(m) + dy, f"{t:g} s: {m:.4f}" if m < 0.01 else f"{t:g} s: {m:.3f}", "label2",
                         I["primary"], anc))
    m1, m2 = MU_EQ * (1 - F_t(1)), MU_EQ * (1 - F_t(20000))
    o.append(H.label(s, ax.X(np.sqrt(0.1 * t90)), ax.Y(0.075), "steps & gait", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(np.sqrt(0.1 * t90)), ax.Y(0.075) + 16, f"(F ≥ 0.9, to {t90:.0f} s)", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(0.15), ax.Y(0.115), f"fluid drains: friction climbs ×{m2/m1:.0f} from 1 s to 20 000 s",
                     "label2", I["secondary"], "start", 'font-style="italic"'))
    aria = (f"Effective friction mu eff = 0.15 times (1 minus F) against time under static load on a log axis from 0.1 s to "
            f"100000 s, from the Lab 2 code. At Lab 2's four printed times it is {m1:.4f} at 1 s (a footstep), "
            f"{MU_EQ*(1-F_t(60)):.4f} at 60 s, {MU_EQ*(1-F_t(3600)):.3f} at 3600 s and {m2:.3f} at 20000 s, a {m2/m1:.0f}-fold "
            f"climb toward the drained value 0.15 (dashed line). A dashed vertical line marks the gel time {TAU:.0f} s; a shaded "
            f"band marks steps and gait, where F stays at or above 0.9, up to {t90:.0f} s.")
    hv = hover(ax, [ax.X(t) for t in ts], [ax.Y(m) for m in mus],
               [f"t = {t:.3g} s: F = {F_t(t):.3f}, μeff = {m:.4f}" for t, m in zip(ts, mus)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #23: swelling pressure and GAG content
def fig23():
    VB = (0, 0, 760, 440)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 90, 735, 350), (0, 0.3), (0, 330))
    cs = [0.3 * i / 75 for i in range(76)]
    ps = [donnan(c) / 1e3 for c in cs]
    ph, pl = donnan(0.2) / 1e3, donnan(0.1) / 1e3
    lam = 1 + 1 / math.sqrt(1 + (0.2 / (2 * C0)) ** 2)
    lavg = math.log(ph / pl) / math.log(2)
    o = axes(s, ax, [(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3)], [(v, f"{v}") for v in (0, 100, 200, 300)],
             f"fixed charge density c{sub('F', s)} (M)", "Donnan swelling pressure π (kPa)")
    # top scale: GAG mass concentration m = 458 cF / 2 (g/L = mg/mL of tissue water), sec. 1
    o.append(H.line(s, ax.x0, ax.top, ax.x1, ax.top, I["axis"], "axis"))
    for m in (0, 20, 40, 60):
        x = ax.X(2 * m / 458)
        o.append(H.line(s, x, ax.top, x, ax.top - 5, I["axis"], "leader"))
        o.append(H.label(s, x, ax.top - 10, f"{m}", "tick", I["secondary"], "middle"))
    o.append(H.label(s, (ax.x0 + ax.x1) / 2, ax.top - 32, f"GAG content m (mg/mL of tissue water), c{sub('F', s)} = 2m/458",
                     "label", I["primary"], "middle"))
    o.append(H.label(s, ax.x0 + 12, ax.top + 22, f"π = R{sub('g', s)}Θ(√(c{sub('F', s)}² + 4c{sub('0', s)}²) − 2c{sub('0', s)}), "
                     f"c{sub('0', s)} = 0.15 M, R{sub('g', s)}Θ = {RT:.0f} J/mol", "label2", I["primary"]))
    o.append(curve(s, ax, cs, ps, SER[0]))
    for c, pv in ((0.1, pl), (0.2, ph)):
        o.append(H.line(s, ax.X(c), ax.Y(pv) + 5, ax.X(c), ax.y0, I["secondary"], "leader", (3, 3)))
        o.append(dot(s, ax.X(c), ax.Y(pv), O["flag"]))
    o.append(H.label(s, ax.X(0.2) - 10, ax.Y(ph) - 26, f"healthy 0.2 M (m = {458*0.2/2:.1f} mg/mL):", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(0.2) - 10, ax.Y(ph) - 10, f"π = {ph:.0f} kPa, local Λ{sub('π', s)} = {lam:.2f}", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(0.1) - 10, ax.Y(pl) - 10, f"half the charge, 0.1 M: π = {pl:.0f} kPa", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(0.02), ax.Y(205), f"−50 % charge → −{100*(1-pl/ph):.0f} % pressure", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.02), ax.Y(205) + 16, f"(log-average elasticity {lavg:.2f})", "label2", I["secondary"]))
    aria = (f"Donnan swelling pressure in kilopascals against fixed charge density from 0 to 0.30 molar, with a top scale "
            f"giving the equivalent glycosaminoglycan content, c F = 2m/458. The convex red curve passes {ph:.0f} kPa at the "
            f"healthy 0.2 M (45.8 mg/mL, local elasticity {lam:.2f}) and {pl:.0f} kPa at half that charge: a "
            f"{100*(1-pl/ph):.0f} percent loss of pressure for a 50 percent loss of charge, log-average elasticity {lavg:.2f}.")
    hv = hover(ax, [ax.X(c) for c in cs], [ax.Y(v) for v in ps],
               [f"cF = {c:.3f} M (GAG {458*c/2:.1f} mg/mL): π = {v:.1f} kPa" for c, v in zip(cs, ps)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #25: support and friction vs permeability
def fig25():
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 60, 668, 320), (1e-15, 1e-11), (0, 1.0), xlog=True)
    axr = Ax((90, 60, 668, 320), (1e-15, 1e-11), (0, 0.15), xlog=True)
    ks = logspace(1e-15, 1e-11, 121)
    Fk = [F_t(1.0, k=k) for k in ks]
    Mk = [MU_EQ * (1 - f) for f in Fk]
    o = [band(ax, 1e-14, 1e-12, BOXFILL, 1)]
    o += axes(s, ax, [(10.0 ** e, dec(e)) for e in range(-15, -10)], [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1.0)],
              "matrix permeability k (m⁴/(N·s), log scale)", "fluid support F(1 s), left axis")
    o.append(H.line(s, axr.x1, axr.y0, axr.x1, axr.top, I["axis"], "axis"))
    for v in (0, 0.05, 0.10, 0.15):
        o.append(H.line(s, axr.x1, axr.Y(v), axr.x1 + 5, axr.Y(v), I["axis"], "leader"))
        o.append(H.label(s, axr.x1 + 9, axr.Y(v) + 4.5, f"{v:.2f}", "tick", I["secondary"]))
    yr = (axr.y0 + axr.top) / 2
    o.append(H.label(s, axr.x1 + 58, yr, f"friction μ{sub('eff', s)} = μ{sub('eq', s)}(1 − F), right axis", "label", I["primary"],
                     "middle", f'transform="rotate(90 {axr.x1 + 58:.2f} {yr:.2f})"'))
    o.append(H.label(s, ax.X(1.15e-14), ax.Y(0.80), "osteoarthritic:", "label2", I["primary"]))
    o.append(H.label(s, ax.X(1.15e-14), ax.Y(0.80) + 16, "k up 10–1000×", "label2", I["primary"]))
    o.append(curve(s, ax, ks, Fk, SER[1]))
    o.append(curve(s, axr, ks, Mk, SER[0], "curve", DASH_SER))
    marks = [(1e-15, "healthy", 1e-15), (1e-14, "×10", 1e-14), (1e-12, "×1000", 1e-12)]
    for k, name, _ in marks:
        f = F_t(1.0, k=k)
        o.append(dot(s, ax.X(k), ax.Y(f), SER[1]))
        o.append(dot(s, axr.X(k), axr.Y(MU_EQ * (1 - f)), SER[0]))
    f15, f14, f12 = (F_t(1.0, k=k) for k in (1e-15, 1e-14, 1e-12))
    m15, m12 = MU_EQ * (1 - f15), MU_EQ * (1 - f12)
    o.append(H.label(s, ax.X(1e-15) + 10, ax.Y(f15) + 30, f"healthy k = 10⁻¹⁵:", "label2", I["primary"]))
    o.append(H.label(s, ax.X(1e-15) + 10, ax.Y(f15) + 46, f"F = {f15:.3f}, μ = {m15:.4f}", "label2", I["primary"]))
    o.append(H.label(s, ax.X(1e-14) + 8, ax.Y(f14) - 10, f"×10: F = {f14:.3f}", "label2", I["primary"]))
    xb = ax.X(10 ** -12.4)
    o.append(H.line(s, xb + 4, ax.Y(0.40) - 4, ax.X(1e-12) - 5, ax.Y(f12) + 3, I["rule"], "leader"))
    o.append(H.label(s, xb, ax.Y(0.40), f"×1000 (k = 10⁻¹²): τ = {H0**2/(HA*1e-12):.1f} s,", "label2", I["primary"], "end"))
    o.append(H.label(s, xb, ax.Y(0.40) + 16, f"F = {f12:.2f}, μ = {m12:.3f} (×{m12/m15:.0f})", "label2", I["primary"], "end"))
    o += legend(s, ax.x0, 30, [(SER[1], None, "fluid support during a 1 s footstep, F(1 s)"),
                               (SER[0], DASH_SER, f"friction μ{sub('eff', s)} (right axis)")])
    aria = (f"Two curves against matrix permeability k on a log axis from 10 to the minus 15 to 10 to the minus 11. Solid blue, "
            f"left axis: fluid support during a 1 second footstep, {f15:.3f} at the healthy 10 to the minus 15, {f14:.3f} at ten "
            f"times that, {f12:.2f} at a thousand times (gel time 6.7 s) and {Fk[-1]:.2f} at 10 to the minus 11. Dashed red, right "
            f"axis: friction 0.15 times (1 minus F), its mirror image, rising from {m15:.4f} to {m12:.3f} at a thousandfold k, "
            f"{m12/m15:.0f} times higher. A shaded band marks the osteoarthritic rise of 10 to 1000 times.")
    hv = hover(ax, [ax.X(k) for k in ks], [[ax.Y(f), axr.Y(m)] for f, m in zip(Fk, Mk)],
               [f"k = {k:.2e}: F(1 s) = {f:.3f}, μeff = {m:.4f}" for k, f, m in zip(ks, Fk, Mk)])
    return svg(VB, aria, s, o, hv)


FIGS = {
    6: ("Computed Donnan swelling pressure versus fixed charge densit", fig6),
    9: ("Computed consolidation: pore-pressure depth profiles at incr", fig9),
    10: ("Computed fluid load support fraction versus time on a logari", fig10),
    11: ("Stacked bars showing the share of load carried by interstiti", fig11),
    15: ("Two-panel result: the top panel shows strain ramped to a hel", fig15),
    16: ("Sensitivity: three stress-relaxation curves for layer thickn", fig16),
    18: ("Computed contact pressure across the contact: the Hertz elas", fig18),
    20: ("Computed Stribeck curve: friction stays near 0.15 at low Str", fig20),
    22: ("Computed biphasic friction versus loading time: friction is ", fig22),
    23: ("Donnan swelling pressure against fixed charge density from 0", fig23),
    25: ("Computed fluid load support during a footstep falling and fr", fig25),
    26: ("Pressure redistribution: the healthy contact spreads the loa", fig26),
}
