"""Module 1 plots, group `plots`: svg #10 (section 9 lab, 760 px) and #31-#40 (K1-K10, 400 px).

Every plotted number is computed here from Eq. (4.1), Proposition 6.1 or the K-problem script the
Module 1 text states (ported line for line, same random seeds and draw order). The numbers the page
prints are asserted at import, so drift fails loudly.
"""
import math
from functools import lru_cache

import numpy as np

import house as H
from m05.plots_main import Ax, axes, curve, poly, dot, legend, tw, hover, svg, mn, lead, DASH_SER

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
BAND = I["muted"]
GRID = "#e6e6e6"
BOX = "#f7f4ef"
W = 400

# ---------------------------------------------------------------- constants the text states (sec. 8, Appendix)
G, M_S, R_S, R_L, D_M = 9.81, 0.022 * 70.0, 0.116, 0.35, 0.03


def tau(theta, m_l):
    """Eq. (4.1): required elbow torque, theta in rad."""
    return G * np.cos(theta) * (M_S * R_S + m_l * R_L)


def pscale(h):
    return H.Scale(W, h, display_w=400)


def sub(t, s, size="label2"):
    return H.sub(t, s, size)


def lab(s, x, y, t, size="label2", fill=I["primary"], anchor="start", extra=""):
    return H.label(s, x, y, t, size, fill, anchor, extra)


def cut(xs, ys, top):
    """Points up to the axis top; the last one interpolated onto it (check_frame ignores clip-paths)."""
    xs, ys = list(xs), list(ys)
    for i in range(1, len(ys)):
        if ys[i] > top:
            f = (top - ys[i - 1]) / (ys[i] - ys[i - 1])
            return xs[:i] + [xs[i - 1] + f * (xs[i] - xs[i - 1])], ys[:i] + [top]
    return xs, ys


def swatch(x, y, col, op=1.0):
    return f'<rect x="{x:.2f}" y="{y - 10:.2f}" width="22" height="11" fill="{col}" opacity="{op}"/>'


# ================================================================ svg #10: the section 9 lab, tau(theta) for four loads
LOADS = [(10, SER[0]), (5, SER[1]), (2, SER[2]), (0, SER[3])]
assert [round(float(tau(0.0, m)), 2) for m in (0, 2, 5, 10)] == [1.75, 8.62, 18.92, 36.09]          # line 451-454
assert [round(float(tau(0.0, m)) / D_M) for m in (0, 2, 5, 10)] == [58, 287, 631, 1203]


def fig10():
    VB = (0, 0, 760, 392)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 56, 740, 322), (0, 90), (0, 40))
    th = np.linspace(0, math.pi / 2, 91)                     # Eq. (4.1) is smooth: 1 degree steps
    deg = np.degrees(th)
    o = axes(s, ax, [(v, f"{v}°") for v in range(0, 91, 15)], [(v, f"{v}") for v in range(0, 41, 10)],
             "forearm angle below horizontal θ", "required elbow torque τ (N·m)", ylab_x=28, xlab_dy=46)
    for m, col in LOADS:
        o.append(curve(s, ax, deg, tau(th, m), col, "curve_multi"))
    for m, col in LOADS:
        o.append(dot(s, ax.X(0), ax.Y(float(tau(0.0, m))), col))
    for m, col in LOADS:
        t0 = float(tau(0.0, m))
        txt = f"{m} kg: {t0:.2f} N·m, F{sub('m', s)} = {t0 / D_M:.0f} N"
        o.append(lab(s, ax.X(1.5), ax.Y(t0) - 9, txt))
    o += legend(s, ax.x0, 30, [(col, None, f"m{sub('L', s)} = {m} kg") for m, col in LOADS], gap=24)
    o.append(lab(s, ax.X(89), ax.Y(37), f"τ(θ) = g cos θ (m{sub('s', s)}r{sub('s', s)} + m{sub('L', s)}r{sub('L', s)})",
                 "label", anchor="end"))
    o.append(lab(s, ax.X(89), ax.Y(37) + 20, "largest at the horizontal, zero at 90°;", "label2", I["secondary"], "end"))
    o.append(lab(s, ax.X(89), ax.Y(37) + 37, f"curve spacing set by m{sub('L', s)}r{sub('L', s)}, r{sub('L', s)} = 0.35 m",
                 "label2", I["secondary"], "end"))
    aria = ("Plot of required elbow torque from Eq. 4.1 against forearm angle below horizontal, 0 to 90 degrees, for loads "
            "of 10, 5, 2 and 0 kilograms. Every curve is a cosine: largest at the horizontal, where it is 36.09, 18.92, "
            "8.62 and 1.75 newton metres (muscle force 1203, 631, 287 and 58 newtons with a 3 centimetre moment arm), "
            "and zero at 90 degrees. The spacing between curves is set by the load term mass times grip distance.")
    hd = np.linspace(0, 90, 181)
    hv = hover(ax, [ax.X(d) for d in hd], [[ax.Y(float(tau(math.radians(d), m))) for m, _ in LOADS] for d in hd],
               [f"θ = {d:.1f}°: τ = " + ", ".join(f"{float(tau(math.radians(d), m)):.2f}" for m, _ in LOADS)
                + " N·m (10, 5, 2, 0 kg)" for d in hd])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #31, K1: muscle force, constant vs shrinking arm
K1_TH = np.linspace(0, np.pi / 2, 2001)
K1_TAU = G * np.cos(K1_TH) * (M_S * R_S + 5 * R_L)
K1_VAR = K1_TAU / (0.03 - 0.012 * np.sin(K1_TH))
K1_CON = K1_TAU / 0.03
K1_I = int(np.argmax(K1_VAR))
assert (round(float(K1_VAR[K1_I])), round(math.degrees(K1_TH[K1_I]), 1), round(float(K1_CON[0]))) == (688, 23.6, 631)


def fig31():
    VB = (0, 0, W, 286)
    s = pscale(VB[3])
    ax = Ax((58, 62, 388, 226), (0, 90), (0, 800))
    deg = np.degrees(K1_TH)
    o = axes(s, ax, [(v, f"{v}°") for v in (0, 15, 30, 45, 60, 75, 90)], [(v, f"{v}") for v in (0, 200, 400, 600, 800)],
             "forearm angle θ", f"muscle force F{sub('m', s, 'label')} (N)", ylab_x=16, xlab_dy=42)
    o.append(curve(s, ax, deg[::20], K1_CON[::20], SER[1], "curve_multi"))
    o.append(curve(s, ax, deg[::20], K1_VAR[::20], SER[0], "curve_multi"))
    pk, pd = float(K1_VAR[K1_I]), math.degrees(K1_TH[K1_I])
    o.append(H.line(s, ax.X(pd), ax.y0, ax.X(pd), ax.Y(pk), O["dim"], "leader", H.DASH_REF))
    o.append(dot(s, ax.X(pd), ax.Y(pk), SER[0]))
    o.append(dot(s, ax.X(0), ax.Y(float(K1_CON[0])), SER[1]))
    o.append(lab(s, ax.X(pd), ax.Y(pk) - 10, f"peak {pk:.0f} N at {pd:.1f}°", anchor="middle"))
    o.append(lab(s, ax.X(89), ax.Y(745), "up to 67% apart near 90°", "label2", I["secondary"], "end"))
    o.append(lab(s, ax.X(54), ax.Y(625), f"shrinking d{sub('m', s)}"))
    o.append(lab(s, ax.X(44), ax.Y(250), f"constant d{sub('m', s)}", anchor="end"))
    o += legend(s, ax.x0, 20, [(SER[0], None, f"shrinking d{sub('m', s)}(θ)"),
                               (SER[1], None, f"constant d{sub('m', s)} = 0.030 m")], gap=14)
    o.append(lab(s, ax.x0, 40, f"d{sub('m', s)}(θ) = 0.030 − 0.012 sin θ m; both {K1_CON[0]:.0f} N at θ = 0",
                 "label2", I["secondary"]))
    o.append(lab(s, ax.X(26), ax.Y(60), "load 5 kg at 0.35 m", "label2", I["secondary"]))
    aria = ("Problem K1 plot: elbow muscle force for a 5 kilogram load against forearm angle from 0 to 90 degrees, for a "
            "constant 3 centimetre moment arm and for the moment arm 0.030 minus 0.012 sine theta metres that shrinks as "
            "the forearm lowers. Both start at 631 newtons at the horizontal. The constant-arm force falls as cosine theta; "
            f"the shrinking-arm force rises first, peaks at {pk:.0f} newtons at {pd:.1f} degrees, then falls, and runs up "
            "to 67 percent above the constant-arm force near 90 degrees.")
    hi = list(range(0, len(K1_TH), 20))
    hv = hover(ax, [ax.X(deg[i]) for i in hi], [[ax.Y(K1_VAR[i]), ax.Y(K1_CON[i])] for i in hi],
               [f"θ = {deg[i]:.1f}°: shrinking {K1_VAR[i]:.0f} N, constant {K1_CON[i]:.0f} N" for i in hi])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #32, K2: least-squares recovery of m_L
_rng = np.random.default_rng(0)
K2_TH = np.linspace(0, np.radians(80), 25)
K2_TAU = G * np.cos(K2_TH) * (M_S * R_S + 6.0 * 0.33) + _rng.normal(0, 0.4, 25)
_X = G * np.cos(K2_TH)
K2_B = float(np.sum(_X * K2_TAU) / np.sum(_X * _X))
K2_ML = (K2_B - M_S * R_S) / 0.33
assert round(K2_ML, 2) == 5.98, K2_ML                                                         # line 651


def fig32():
    VB = (0, 0, W, 286)
    s = pscale(VB[3])
    ax = Ax((58, 62, 388, 226), (0, 80), (0, 25))
    o = axes(s, ax, [(v, f"{v}°") for v in range(0, 81, 20)], [(v, f"{v}") for v in range(0, 26, 5)],
             "forearm angle θ", "measured torque τ (N·m)", ylab_x=16, xlab_dy=42)
    hd = np.linspace(0, 80, 81)
    fit = K2_B * G * np.cos(np.radians(hd))
    o.append(curve(s, ax, hd, fit, SER[0]))
    for t, y in zip(np.degrees(K2_TH), K2_TAU):
        o.append(dot(s, ax.X(t), ax.Y(y), I["secondary"]))
    o.append(lab(s, ax.X(2), ax.Y(9.0), f"slope b = m{sub('s', s)}r{sub('s', s)} + m{sub('L', s)}r{sub('L', s)}"
                 f" = {K2_B:.3f} kg·m"))
    o.append(lab(s, ax.X(2), ax.Y(9.0) + 17, f"m{sub('L', s)} = (b − m{sub('s', s)}r{sub('s', s)})/0.33 m"
                 f" = {K2_ML:.2f} kg", "label2", I["secondary"]))
    o.append(lab(s, ax.X(2), ax.Y(9.0) + 34, "true value 6.0 kg, noise σ = 0.4 N·m", "label2", I["secondary"]))
    o += legend(s, ax.x0, 20, [(I["secondary"], None, "measured, 25 angles", "dot"),
                               (SER[0], None, "least-squares fit")], gap=16)
    aria = ("Problem K2 plot: 25 noisy torque measurements, grey dots, against forearm angle from 0 to 80 degrees, and the "
            "least-squares fit, torque equal to slope b times g cosine theta. The slope is "
            f"{K2_B:.3f} kilogram metres; subtracting the segment term and dividing by the 0.33 metre grip distance "
            f"recovers a load of {K2_ML:.2f} kilograms against the true 6.0, from data with 0.4 newton metre noise.")
    hv = hover(ax, [ax.X(d) for d in hd], [ax.Y(f) for f in fit], [f"θ = {d:.1f}°: fit τ = {f:.2f} N·m" for d, f in zip(hd, fit)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #33, K3: tornado of +-15 % perturbations
K3_P = dict(m_s=0.022 * 70, r_s=0.116, m_L=5.0, r_L=0.35, d_m=0.03)


def k3_force(m_s, r_s, m_L, r_L, d_m):
    return G * (m_s * r_s + m_L * r_L) / d_m


K3_BASE = k3_force(**K3_P)
K3_HI = {k: k3_force(**dict(K3_P, **{k: K3_P[k] * 1.15})) - K3_BASE for k in K3_P}
K3_LO = {k: k3_force(**dict(K3_P, **{k: K3_P[k] * 0.85})) - K3_BASE for k in K3_P}


@lru_cache(None)
def k3_band():
    rng = np.random.default_rng(0)
    n = 100000
    samp = {k: K3_P[k] * rng.uniform(0.85, 1.15, n) for k in K3_P}
    F = k3_force(**samp)
    return float(np.percentile(F, 5)), float(np.median(F)), float(np.percentile(F, 95))


assert (round(K3_HI["m_L"], 1), round(K3_HI["d_m"], 1), round(K3_LO["d_m"], 1), round(K3_HI["m_s"], 1)) == \
    (85.8, -82.3, 111.3, 8.8)                                                                     # line 666, 687
assert (round(100 * K3_HI["d_m"] / K3_BASE, 1), round(100 * K3_LO["d_m"] / K3_BASE, 1)) == (-13.0, 17.6)


def fig33():
    VB = (0, 0, W, 344)
    s = pscale(VB[3])
    lo5, med, hi95 = k3_band()
    assert (round(lo5), round(med), round(hi95)) == (496, 629, 797), (lo5, med, hi95)
    ax = Ax((74, 44, 388, 262), (-150, 175), (0, 6))
    o = []
    for v in range(-150, 176, 50):
        o.append(H.line(s, ax.X(v), ax.top, ax.X(v), ax.y0, GRID, "leader"))
    o.append(H.line(s, ax.x0, ax.y0, ax.x1, ax.y0, I["axis"], "axis"))
    for v in range(-150, 176, 50):
        o.append(H.line(s, ax.X(v), ax.y0, ax.X(v), ax.y0 + 5, I["axis"], "leader"))
        o.append(lab(s, ax.X(v), ax.y0 + 19, mn(v, "{:.0f}", True), "tick", I["secondary"], "middle"))
    o.append(lab(s, (ax.x0 + ax.x1) / 2, ax.y0 + 40, f"change in muscle force ΔF{sub('m', s, 'label')} (N),"
                 f" base {K3_BASE:.0f} N", "label", I["primary"], "middle"))
    names = [("m_s", f"m{sub('s', s, 'label')}"), ("r_s", f"r{sub('s', s, 'label')}"), ("m_L", f"m{sub('L', s, 'label')}"),
             ("r_L", f"r{sub('L', s, 'label')}"), ("d_m", f"d{sub('m', s, 'label')}")]
    bh, panels = 11, []
    for k, (key, txt) in enumerate(names):
        yc = ax.Y(5.5 - k)
        o.append(lab(s, ax.x0 - 12, yc + 5, txt, "label", I["primary"], "end", 'font-style="italic"'))
        pts = []
        for dv, col, dy, tag in ((K3_HI[key], SER[0], -bh, "+15%"), (K3_LO[key], SER[1], 0, "−15%")):
            xa, xb = sorted((ax.X(0), ax.X(dv)))
            o.append(f'<rect x="{xa:.2f}" y="{yc + dy:.2f}" width="{xb - xa:.2f}" height="{bh}" fill="{col}"/>')
            right = dv > 0
            o.append(lab(s, ax.X(dv) + (5 if right else -5), yc + dy + 9.5, mn(dv, "{:.1f}", True), "tick", I["secondary"],
                         "start" if right else "end"))
            pts.append([ax.X(dv), yc + dy + bh / 2, f"{key.replace('_', '')} {tag}: ΔFm = {mn(dv, '{:.1f}', True)} N "
                        f"({mn(100 * dv / K3_BASE, '{:.1f}', True)}%)"])
        pts.sort(key=lambda q: q[0])
        panels.append(([ax.x0, yc - 15, ax.x1, yc + 15], pts))
    yc = ax.Y(0.5)
    xa, xb = ax.X(lo5 - K3_BASE), ax.X(hi95 - K3_BASE)
    o.append(f'<rect x="{xa:.2f}" y="{yc - bh:.2f}" width="{xb - xa:.2f}" height="{2 * bh}" fill="{BAND}" opacity="0.35"/>')
    o.append(H.line(s, ax.X(med - K3_BASE), yc - bh - 3, ax.X(med - K3_BASE), yc + bh + 3, I["primary"], "ref"))
    o.append(lab(s, ax.x0 - 12, yc - 2, "all", "label2", I["primary"], "end"))
    o.append(lab(s, ax.x0 - 12, yc + 12, "five", "label2", I["primary"], "end"))
    o.append(lab(s, xa + 4, yc + 4, f"{lo5:.0f} N", "tick", I["primary"]))
    o.append(lab(s, xb - 4, yc + 4, f"{hi95:.0f} N", "tick", I["primary"], "end"))
    o.append(lab(s, ax.X(med - K3_BASE) + 5, yc + 4, f"median {med:.0f}", "tick", I["primary"]))
    panels.append(([ax.x0, yc - 15, ax.x1, yc + 15],
                   [[xa, yc, f"all five ±15%, 5th percentile: {lo5:.0f} N"], [ax.X(med - K3_BASE), yc, f"median {med:.0f} N"],
                    [xb, yc, f"95th percentile: {hi95:.0f} N"]]))
    o.append(H.line(s, ax.X(0), ax.top, ax.X(0), ax.y0, I["axis"], "axis"))
    o.append(swatch(ax.x0, 22, SER[0]))
    o.append(lab(s, ax.x0 + 28, 22, "+15%"))
    o.append(swatch(ax.x0 + 80, 22, SER[1]))
    o.append(lab(s, ax.x0 + 108, 22, "−15%"))
    o.append(swatch(ax.x0 + 160, 22, BAND, 0.35))
    o.append(lab(s, ax.x0 + 188, 22, "5th–95th %, all five"))
    o.append(lab(s, (ax.x0 + ax.x1) / 2, ax.y0 + 60, f"d{sub('m', s)} is a divisor: −15% → +17.6%, +15% → −13.0%",
                 "label2", I["secondary"], "middle"))
    aria = ("Problem K3 tornado chart: the change in the elbow muscle force of section 8, 631 newtons, when each of five "
            "parameters is raised or lowered by 15 percent. The segment mass and its centre-of-mass distance move it by "
            "plus or minus 8.8 newtons; the load mass and grip distance by plus or minus 85.8; the moment arm, a divisor, "
            "by minus 82.3 when raised and plus 111.3 when lowered, plus 17.6 against minus 13.0 percent, the largest and "
            f"asymmetric. A grey band for all five varied at once spans the 5th to 95th percentile, {lo5:.0f} to "
            f"{hi95:.0f} newtons, median {med:.0f}.")
    return svg(VB, aria, s, o, H.hover_attr(panels))


# ================================================================ svg #34, K4: disc compression across trunk angle and reach
M_UB, D_ES = 0.60 * 70, 0.05
L_T = 0.30 / np.sin(np.radians(60))                      # along-trunk COM distance, 0.346 m


def comp(m_l, r_l, beta_deg):
    """Proposition 6.1 with r_t = l_t sin(beta)."""
    b = np.radians(beta_deg)
    return G * (M_UB * L_T * np.sin(b) + m_l * r_l) / D_ES + (M_UB + m_l) * G * np.cos(b)


def safe_load(r_l, beta_deg):
    """Largest m_L with C <= 3400 N (C is linear in m_L)."""
    b = np.radians(beta_deg)
    return (3400 - G * M_UB * (L_T * np.sin(b) / D_ES + np.cos(b))) / (G * (r_l / D_ES + np.cos(b)))


K4_C0 = float(comp(20, 0.4, 60))
assert [round(float(comp(20, r, b))) for b, r in ((60, .4), (60, .2), (30, .4), (20, .2), (10, .2))] == \
    [4346, 3561, 3524, 2333, 1879]                                                                # line 691, 712-713
assert [round(float(safe_load(r, b)), 1) for b, r in ((60, .4), (60, .2), (30, .4))] == [8.7, 16.4, 18.6]
REACH = [(0.4, SER[0]), (0.3, SER[1]), (0.2, SER[2])]


def fig34():
    VB = (0, 0, W, 286)
    s = pscale(VB[3])
    ax = Ax((58, 62, 388, 226), (0, 60), (1.5, 4.5))
    o = axes(s, ax, [(v, f"{v}°") for v in (0, 10, 20, 30, 45, 60)], [(v, f"{v:g}") for v in (2, 3, 4)],
             "trunk angle β from vertical", "disc compression C (kN)", ylab_x=16, xlab_dy=42)
    bs = np.linspace(10, 60, 101)
    o.append(H.line(s, ax.x0, ax.Y(3.4), ax.x1, ax.Y(3.4), I["primary"], "ref", H.DASH_REF))
    o.append(H.line(s, ax.x0, ax.Y(K4_C0 / 2e3), ax.x1, ax.Y(K4_C0 / 2e3), I["muted"], "ref", H.DASH_REF))
    for r, col in REACH:
        o.append(curve(s, ax, bs, comp(20, r, bs) / 1e3, col, "curve_multi"))
    for r, col in REACH:
        for b in (10, 20, 30, 45, 60):
            o.append(dot(s, ax.X(b), ax.Y(float(comp(20, r, b)) / 1e3), col, r=3))
        o.append(lab(s, ax.X(9), ax.Y(float(comp(20, r, 10)) / 1e3) - 2, f"{r} m", "label2", I["primary"], "end"))
    o.append(lab(s, ax.X(1), ax.Y(3.4) - 6, "NIOSH 3.4 kN"))
    o.append(lab(s, ax.X(59), ax.Y(K4_C0 / 2e3) + 15, f"half of {K4_C0:.0f} N", "label2", I["secondary"], "end"))
    for b, r, dx, dy, anc in ((60, 0.4, -8, -8, "end"), (60, 0.2, -8, 34, "end"), (10, 0.2, 8, 15, "start"),
                              (30, 0.4, -6, -26, "end"), (20, 0.2, 8, 21, "start")):
        c = float(comp(20, r, b))
        txt = f"{c:.0f} N" if b == 60 and r == 0.4 else f"{c:.0f} N, −{100 * (1 - c / K4_C0):.0f}%"
        txt = f"{b}°: " + txt if (b, r) == (20, 0.2) else txt
        o.append(lab(s, ax.X(b) + dx, ax.Y(c / 1e3) + dy, txt, "label2", I["secondary"], anc))
    c30 = float(comp(20, 0.4, 30))
    o.append(lead(s, ax.X(30) - 5, ax.Y(c30 / 1e3) - 22, ax.X(30) - 1, ax.Y(c30 / 1e3) - 5, SER[0]))
    o += legend(s, ax.x0, 20, [(col, None, f"r{sub('L', s)} = {r} m") for r, col in REACH], gap=16)
    o.append(lab(s, ax.x0, 40, "20 kg box; dots: the swept angles", "label2", I["secondary"]))
    aria = ("Problem K4 plot: lumbar disc compression for a 20 kilogram box against trunk angle from vertical, 10 to 60 "
            "degrees, for load reach 0.4, 0.3 and 0.2 metres, with dots at the swept angles 10, 20, 30, 45 and 60. "
            "At the section 6 stoop, 60 degrees and 0.4 metres, compression is 4346 newtons, above the dashed NIOSH 3.4 "
            "kilonewton line. Pulling the box to 0.2 metres at 60 degrees gives 3561 newtons, minus 18 percent; standing to "
            "30 degrees at 0.4 metres gives 3524, minus 19 percent; 20 degrees at 0.2 metres gives 2333, minus 46 percent; "
            "only 10 degrees at 0.2 metres, 1879 newtons, falls below the dotted half of 4346.")
    hv = hover(ax, [ax.X(b) for b in bs], [[ax.Y(float(comp(20, r, b)) / 1e3) for r, _ in REACH] for b in bs],
               [f"β = {b:.1f}°: C = " + ", ".join(f"{float(comp(20, r, b)):.0f}" for r, _ in REACH)
                + " N; safe load " + ", ".join(f"{float(safe_load(r, b)):.1f}" for r, _ in REACH) + " kg (0.4, 0.3, 0.2 m)"
                for b in bs])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #35, K5: maximum holdable load
FMAX5 = 1500.0
K5_TH = np.linspace(0, np.radians(80), 8001)
K5_CON = (FMAX5 * 0.03 / (G * np.cos(K5_TH)) - M_S * R_S) / R_L
K5_VAR = (FMAX5 * (0.03 - 0.012 * np.sin(K5_TH)) / (G * np.cos(K5_TH)) - M_S * R_S) / R_L
K5_I = int(np.argmin(K5_VAR))


def k5_at(arr, d):
    return float(arr[int(np.argmin(abs(np.degrees(K5_TH) - d)))])


assert (round(math.degrees(K5_TH[K5_I]), 1), round(float(K5_VAR[K5_I]), 1)) == (23.6, 11.5)       # line 730
assert [round(k5_at(K5_CON, d), 1) for d in (0, 23.6, 45, 60, 80)] == [12.6, 13.8, 18.0, 25.7, 75.0]
assert [round(k5_at(K5_VAR, d), 1) for d in (0, 23.6, 45, 60, 80)] == [12.6, 11.5, 12.8, 16.6, 45.2]


def fig35():
    VB = (0, 0, W, 286)
    s = pscale(VB[3])
    YT = 30.0
    ax = Ax((58, 62, 388, 226), (0, 80), (0, YT))
    o = axes(s, ax, [(v, f"{v}°") for v in range(0, 81, 20)], [(v, f"{v}") for v in (0, 10, 20, 30)],
             "forearm angle θ", "max holdable load (kg)", ylab_x=16, xlab_dy=42)
    deg = np.degrees(K5_TH)[::80]
    c0 = float(K5_CON[0])
    o.append(H.line(s, ax.x0, ax.Y(c0), ax.x1, ax.Y(c0), I["muted"], "ref", H.DASH_REF))
    o.append(curve(s, ax, *cut(deg, K5_CON[::80], YT), SER[1], "curve_multi"))
    o.append(curve(s, ax, *cut(deg, K5_VAR[::80], YT), SER[0], "curve_multi"))
    md, mv = math.degrees(K5_TH[K5_I]), float(K5_VAR[K5_I])
    o.append(dot(s, ax.X(md), ax.Y(mv), SER[0]))
    o.append(dot(s, ax.X(0), ax.Y(c0), SER[1]))
    o.append(lab(s, ax.X(md), ax.Y(mv) + 20, f"weakest: {mv:.1f} kg at {md:.1f}°", anchor="middle"))
    o.append(lab(s, ax.X(md), ax.Y(mv) + 36, "9% below the horizontal value", "label2", I["secondary"], "middle"))
    o.append(lab(s, ax.X(79), ax.Y(c0) + 16, f"horizontal: {c0:.1f} kg", "label2", I["secondary"], "end"))
    o.append(lab(s, ax.X(55), ax.Y(26), "constant", anchor="end"))
    o.append(lab(s, ax.X(64), ax.Y(15), "shrinking"))
    o.append(lab(s, ax.X(2), ax.Y(27), f"at 80°: {k5_at(K5_CON, 80):.1f} and", "label2", I["secondary"]))
    o.append(lab(s, ax.X(2), ax.Y(27) + 15, f"{k5_at(K5_VAR, 80):.1f} kg, off scale", "label2", I["secondary"]))
    o += legend(s, ax.x0, 20, [(SER[1], None, f"constant d{sub('m', s)} = 0.030 m"),
                               (SER[0], None, f"shrinking d{sub('m', s)}(θ), K1")], gap=14)
    o.append(lab(s, ax.x0, 40, f"F{sub('max', s)} = 1500 N", "label2", I["secondary"]))
    aria = ("Problem K5 plot: the maximum load a 1500 newton elbow flexor can hold against forearm angle from 0 to 80 "
            "degrees, for a constant 3 centimetre moment arm and for the shrinking K1 moment arm. Both start at 12.6 "
            "kilograms at the horizontal, marked by a dashed line. The constant-arm capacity rises monotonically; the "
            f"shrinking-arm capacity first dips to its minimum, {mv:.1f} kilograms at {md:.1f} degrees, 9 percent lower, "
            "then rises below the constant-arm curve. Both leave the top of the axis toward 90 degrees: at 80 degrees "
            "they are 75.0 and 45.2 kilograms.")
    hi = list(range(0, len(K5_TH), 50))
    hv = hover(ax, [ax.X(math.degrees(K5_TH[i])) for i in hi],
               [[ax.Y(min(K5_VAR[i], YT)), ax.Y(min(K5_CON[i], YT))] for i in hi],
               [f"θ = {math.degrees(K5_TH[i]):.1f}°: shrinking {K5_VAR[i]:.1f} kg, constant {K5_CON[i]:.1f} kg" for i in hi])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #36, K6: inverted-pendulum topple
def k6_run(t_end=None, g=9.81, L=1.0, toe=0.12):
    """K6 script (explicit Euler, dt = 1e-4) up to the toe; with t_end, keep stepping to t_end."""
    w2 = g / L
    x, v, t, dt = 0.02, 0.0, 0.0, 1e-4
    ts, xs, t_toe = [0.0], [x], None
    while (t_end is None and x < toe) or (t_end is not None and t < t_end):
        v += w2 * x * dt
        x += v * dt
        t += dt
        if t_toe is None and x >= toe:
            t_toe = t
        ts.append(t)
        xs.append(x)
    return np.array(ts), np.array(xs), t_toe


K6_TT = k6_run()[2]
assert round(K6_TT, 2) == 0.79 and round(math.acosh(6) / math.sqrt(9.81), 2) == 0.79                    # line 735, 746


def fig36():
    VB = (0, 0, W, 286)
    s = pscale(VB[3])
    YT = 0.16
    ax = Ax((58, 62, 388, 226), (0, 0.9), (-0.02, YT))
    t, x, _ = k6_run(0.9)
    o = axes(s, ax, [(v, f"{v:g}") for v in (0, 0.3, 0.6, 0.9)], [(v, f"{v:.2f}") for v in (0, 0.04, 0.08, 0.12, 0.16)],
             "time t (s)", "horizontal position (m)", ylab_x=16, xlab_dy=42)
    o.append(H.line(s, ax.x0, ax.Y(0.12), ax.x1, ax.Y(0.12), I["primary"], "ref", H.DASH_REF))
    o.append(curve(s, ax, [0, 0.9], [0, 0], SER[1], "curve_multi"))
    o.append(curve(s, ax, *cut(t[::100], x[::100], YT), SER[0], "curve_multi"))
    o.append(H.line(s, ax.X(K6_TT), ax.y0, ax.X(K6_TT), ax.Y(0.12), O["dim"], "leader", H.DASH_REF))
    o.append(dot(s, ax.X(K6_TT), ax.Y(0.12), O["flag"]))
    o.append(lab(s, ax.X(0.01), ax.Y(0.12) - 9, f"toe limit L{sub('f', s)} = 0.12 m"))
    o.append(lab(s, ax.X(K6_TT) - 8, ax.Y(0.12) - 22, f"COM passes the toe", "label2", I["primary"], "end"))
    o.append(lab(s, ax.X(K6_TT) - 8, ax.Y(0.12) - 7, f"at t = {K6_TT:.2f} s", "label2", I["primary"], "end"))
    o.append(lab(s, ax.X(0.02), ax.Y(0.085), f"COM x(t) = 0.02 cosh(ω{sub('0', s)}t), ω{sub('0', s)} = 3.13/s",
                 "label2", I["primary"]))
    o.append(lab(s, ax.X(0.75), ax.Y(0) - 7, "COP stays at the ankle, x = 0", "label2", I["primary"], "end"))
    o += legend(s, ax.x0, 20, [(SER[0], None, "COM"), (SER[1], None, "COP")], gap=16)
    o.append(lab(s, ax.x0 + 150, 20, "ankle torque off, ℓ = 1.0 m", "label2", I["secondary"]))
    aria = ("Problem K6 plot: horizontal position against time for a body toppling forward with the ankle torque off, "
            "an inverted pendulum with the centre of mass 1.0 metre above the ankle, starting 2 centimetres forward and at "
            "rest. The centre-of-mass curve grows as 0.02 times cosh of 3.13 t, slowly at first and then faster, and "
            f"crosses the dashed 0.12 metre toe limit at {K6_TT:.2f} seconds, an orange dot. The centre-of-pressure line "
            "stays flat at zero, at the ankle.")
    hi = list(range(0, len(t), 75))
    hv = hover(ax, [ax.X(t[i]) for i in hi], [[ax.Y(min(x[i], YT)), ax.Y(0.0)] for i in hi],
               [f"t = {t[i]:.2f} s: COM {x[i]:.3f} m, COP 0 m" for i in hi])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #37, K7: vertical GRF during take-off
M7 = 70.0
K7_T = np.linspace(0, 0.3, 3001)
K7_A = 15 * np.sin(np.pi * K7_T / 0.3)
K7_GRF = M7 * (G + K7_A)
K7_V = float(np.trapezoid(K7_A, K7_T))
K7_H = K7_V**2 / (2 * G)
assert (round(float(K7_GRF.max())), round(float(K7_GRF.max()) / (M7 * G), 2), round(K7_V, 2), round(100 * K7_H)) == \
    (1737, 2.53, 2.86, 42)                                                                          # line 760


def fig37():
    VB = (0, 0, W, 286)
    s = pscale(VB[3])
    ax = Ax((58, 62, 388, 226), (0, 0.3), (0, 2.0))
    o = axes(s, ax, [(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3)], [(v, f"{v:g}") for v in (0, 0.5, 1.0, 1.5, 2.0)],
             "time t (s)", "vertical GRF (kN)", ylab_x=16, xlab_dy=42)
    bw = M7 * G / 1e3
    tt, gg = K7_T[::30], K7_GRF[::30] / 1e3
    area = [(ax.X(a), ax.Y(b)) for a, b in zip(tt, gg)] + [(ax.X(0.3), ax.Y(bw)), (ax.X(0), ax.Y(bw))]
    o.append(f'<polygon points="{" ".join(f"{a:.2f},{b:.2f}" for a, b in area)}" fill="{SER[0]}" opacity="0.14"/>')
    o.append(H.line(s, ax.x0, ax.Y(bw), ax.x1, ax.Y(bw), I["primary"], "ref", H.DASH_REF))
    o.append(curve(s, ax, tt, gg, SER[0]))
    pk = float(K7_GRF.max())
    o.append(dot(s, ax.X(0.15), ax.Y(pk / 1e3), SER[0]))
    o.append(lab(s, ax.X(0.15), ax.Y(pk / 1e3) - 10, f"peak {pk / 1e3:.2f} kN = {pk / (M7 * G):.2f} × body weight",
                 anchor="middle"))
    o.append(lab(s, ax.X(0.15), ax.Y(1.25), "impulse above body weight", "label2", I["primary"], "middle"))
    o.append(lab(s, ax.X(0.15), ax.Y(1.25) + 15, f"= M v{sub('TO', s)} = {M7 * K7_V:.0f} N·s", "label2", I["primary"], "middle"))
    o.append(lab(s, ax.X(0.15), ax.Y(bw) + 19, f"body weight {M7 * G:.0f} N", "label2", I["secondary"], "middle"))
    o.append(lab(s, ax.X(0.15), ax.Y(bw) + 40, f"v{sub('TO', s)} = {K7_V:.2f} m/s → jump height v²/2g = {100 * K7_H:.0f} cm",
                 "label2", I["primary"], "middle"))
    o += legend(s, ax.x0, 20, [(SER[0], None, "GRF = M(g + a)")])
    o.append(swatch(ax.x0 + 136, 20, SER[0], 0.14))
    o.append(lab(s, ax.x0 + 164, 20, "impulse above body weight"))
    o.append(lab(s, ax.x0, 40, f"a(t) = 15 sin(πt/0.3) m/s², M = 70 kg", "label2", I["secondary"]))
    aria = ("Problem K7 plot: vertical ground reaction force against time over a 0.3 second jump take-off with a half-sine "
            "acceleration of amplitude 15 metres per second squared, for a 70 kilogram jumper. The force rises from body "
            f"weight, 687 newtons, a dashed line, to a peak of {pk / 1e3:.2f} kilonewtons, {pk / (M7 * G):.2f} body weights, "
            "at 0.15 seconds and returns. The shaded area above body weight is the impulse, "
            f"{M7 * K7_V:.0f} newton seconds, which gives a take-off velocity of {K7_V:.2f} metres per second and a "
            f"{100 * K7_H:.0f} centimetre jump.")
    hv = hover(ax, [ax.X(a) for a in tt], [ax.Y(b) for b in gg],
               [f"t = {a:.3f} s: GRF {b:.3f} kN = {b * 1e3 / (M7 * G):.2f} BW" for a, b in zip(tt, gg)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #38, K8: average vs peak stair power
M8, CEIL = 70.0, 250.0
HEIGHTS = [(0.15, SER[0]), (0.18, SER[1]), (0.20, SER[2])]


def k8_peak(h, f):
    """K8 script: peak of M (g + z'') z' over one step period, 4001 samples."""
    T_ = 1 / f
    t = np.linspace(0, T_, 4001)
    v = (h * np.pi / (2 * T_)) * np.sin(np.pi * t / T_)
    a = (h * np.pi**2 / (2 * T_**2)) * np.cos(np.pi * t / T_)
    return float((M8 * (G + a) * v).max()), float((G + a.max()) / G)


K8_F = np.linspace(1.0, 2.5, 61)


@lru_cache(None)
def k8_curves():
    return {h: np.array([k8_peak(h, f)[0] for f in K8_F]) for h, _ in HEIGHTS}


assert [round(CEIL / (M8 * G * h), 2) for h, _ in HEIGHTS] == [2.43, 2.02, 1.82]                     # line 764
assert [round(k8_peak(h, 1.5)[0]) for h, _ in HEIGHTS] == [246, 297, 331]
assert [round(k8_peak(h, 2.5)[0] / (M8 * G * h * 2.5), 2) for h, _ in HEIGHTS] == [1.71, 1.77, 1.80]
assert [round(math.sqrt(0.6 * G / (h * np.pi**2)), 2) for h, _ in HEIGHTS] == [1.99, 1.82, 1.73]


def fig38():
    VB = (0, 0, W, 286)
    s = pscale(VB[3])
    ax = Ax((58, 62, 344, 226), (1.0, 2.5), (0, 700))
    o = axes(s, ax, [(v, f"{v:g}") for v in (1.0, 1.5, 2.0, 2.5)], [(v, f"{v}") for v in range(0, 701, 200)],
             "stair cadence f (steps/s)", "mechanical power (W)", ylab_x=16, xlab_dy=42)
    o.append(H.line(s, ax.x0, ax.Y(CEIL), ax.x1, ax.Y(CEIL), I["primary"], "ref", H.DASH_REF))
    pk = k8_curves()
    for h, col in HEIGHTS:
        fc = CEIL / (M8 * G * h)
        o.append(H.line(s, ax.X(fc), ax.Y(CEIL), ax.X(fc), ax.y0, O["dim"], "leader", H.DASH_REF))
        o.append(lab(s, ax.X(fc) + 3, ax.y0 - 6, f"{fc:.2f}", "tick", I["secondary"]))
    for h, col in HEIGHTS:
        o.append(curve(s, ax, K8_F, M8 * G * h * K8_F, col, "curve_multi", DASH_SER))
        o.append(curve(s, ax, K8_F, pk[h], col, "curve_multi"))
    for h, col in HEIGHTS:
        o.append(dot(s, ax.X(CEIL / (M8 * G * h)), ax.Y(CEIL), col, r=3.5))
        o.append(lab(s, ax.x1 + 5, ax.Y(float(pk[h][-1])) + 4, f"{h:.2f} m", "label2", I["primary"]))
    o.append(lab(s, ax.x1 + 5, ax.Y(CEIL) + 4, "250 W", "label2", I["primary"]))
    o.append(lab(s, ax.X(1.03), ax.Y(640), "peak/average: 1.6 at f = 1.5,", "label2", I["secondary"]))
    o.append(lab(s, ax.X(1.03), ax.Y(640) + 15, "1.7–1.8 at f = 2.5", "label2", I["secondary"]))
    o += legend(s, ax.x0, 20, [(col, None, f"h = {h:.2f} m") for h, col in HEIGHTS], gap=14)
    o += legend(s, ax.x0, 40, [(I["secondary"], None, "peak"), (I["secondary"], DASH_SER, "average Mghf")], gap=14)
    o.append(lab(s, ax.x0 + 210, 40, "dots: average = 250 W", "label2", I["secondary"]))
    aria = ("Problem K8 plot: stair-climbing power for a 70 kilogram climber against cadence from 1 to 2.5 steps per "
            "second, for step heights 0.15, 0.18 and 0.20 metres. Dashed lines are the average power M g h f, straight in "
            "f; solid lines are the peak power of the rest-at-each-step profile, which runs 1.6 times the average at 1.5 "
            "steps per second and 1.7 to 1.8 times at 2.5. Dots mark where the average reaches the dashed 250 watt line: "
            "2.43, 2.02 and 1.82 steps per second, earliest for the tallest step, with drop lines to the cadence axis.")
    hv = hover(ax, [ax.X(f) for f in K8_F], [[ax.Y(pk[h][i]) for h, _ in HEIGHTS] for i in range(len(K8_F))],
               [f"f = {f:.3f}/s: peak " + ", ".join(f"{pk[h][i]:.0f}" for h, _ in HEIGHTS) + " W; average "
                + ", ".join(f"{M8 * G * h * f:.0f}" for h, _ in HEIGHTS) + " W (h = 0.15, 0.18, 0.20 m)"
                for i, f in enumerate(K8_F)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #39, K9: recover d_m(theta) from MVC torque
_rng9 = np.random.default_rng(1)
FMAX9 = 2000.0
K9_TH = np.radians(np.linspace(0, 80, 20))
K9_TAU = FMAX9 * (0.030 - 0.012 * np.sin(K9_TH)) + _rng9.normal(0, 0.8, K9_TH.size)
_A9 = np.column_stack([np.ones_like(K9_TH), np.sin(K9_TH)]) * FMAX9
K9_D0, K9_D1 = (float(v) for v in np.linalg.lstsq(_A9, K9_TAU, rcond=None)[0])
assert (round(K9_D0 * 100, 2), round(K9_D1, 4), round((K9_D0 + K9_D1) * 100, 2)) == (3.02, -0.0122, 1.79)   # line 797


def fig39():
    VB = (0, 0, W, 286)
    s = pscale(VB[3])
    ax = Ax((58, 62, 388, 226), (0, 80), (30, 65))
    o = axes(s, ax, [(v, f"{v}°") for v in range(0, 81, 20)], [(v, f"{v}") for v in range(30, 66, 10)],
             "forearm angle θ", "max voluntary torque (N·m)", ylab_x=16, xlab_dy=42)
    hd = np.linspace(0, 80, 81)
    fit = FMAX9 * (K9_D0 + K9_D1 * np.sin(np.radians(hd)))
    o.append(curve(s, ax, hd, fit, SER[0]))
    for t, y in zip(np.degrees(K9_TH), K9_TAU):
        o.append(dot(s, ax.X(t), ax.Y(y), I["secondary"]))
    o.append(lab(s, ax.X(2), ax.Y(38.5), f"fit: d{sub('0', s)} = {K9_D0 * 100:.2f} cm, d{sub('1', s)} = "
                 f"{mn(K9_D1, '{:.4f}')} m"))
    o.append(lab(s, ax.X(2), ax.Y(38.5) + 16, "true 0.030 m, −0.012 m", "label2", I["secondary"]))
    o.append(lab(s, ax.X(2), ax.Y(38.5) + 32, f"d{sub('m', s)}(0) = {K9_D0 * 100:.2f} cm, d{sub('m', s)}(90°) = "
                 f"{(K9_D0 + K9_D1) * 100:.2f} cm", "label2", I["secondary"]))
    o += legend(s, ax.x0, 20, [(I["secondary"], None, "measured MVC, 20 angles", "dot"),
                               (SER[0], None, f"F{sub('max', s)}(d{sub('0', s)} + d{sub('1', s)} sin θ)")], gap=14)
    o.append(lab(s, ax.x0, 40, f"F{sub('max', s)} = 2000 N, noise σ = 0.8 N·m", "label2", I["secondary"]))
    aria = ("Problem K9 plot: 20 noisy maximum voluntary elbow torques, grey dots, against forearm angle from 0 to 80 "
            "degrees, falling from about 60 to about 36 newton metres, and the two-parameter least-squares fit "
            f"2000 newtons times d0 plus d1 sine theta. The fit recovers d0 = {K9_D0 * 100:.2f} centimetres and "
            f"d1 = {K9_D1:.4f} metres against the true 0.030 and minus 0.012, so the moment arm falls from "
            f"{K9_D0 * 100:.2f} centimetres at the horizontal to {(K9_D0 + K9_D1) * 100:.2f} near 90 degrees.")
    hv = hover(ax, [ax.X(d) for d in hd], [ax.Y(f) for f in fit],
               [f"θ = {d:.1f}°: fit {f:.1f} N·m, dm = {f / FMAX9 * 100:.2f} cm" for d, f in zip(hd, fit)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #40, K10: which intervention saves the most torque
DM10, DR10, DTH10 = 2.0, 0.08, np.radians(15)


def savings(m_l, th):
    c = np.cos(th)
    s_m = G * DM10 * R_L * c
    s_r = G * m_l * DR10 * c
    s_t = G * (M_S * R_S + m_l * R_L) * (c - np.cos(th + DTH10))
    return s_m, s_r, s_t


def _brentq(f, a, b):
    from scipy.optimize import brentq
    return brentq(f, a, b)


def th_reach(m_l):
    return math.degrees(_brentq(lambda t: savings(m_l, t)[2] - savings(m_l, t)[1], 1e-3, np.radians(85)))


def th_mass(m_l):
    return math.degrees(_brentq(lambda t: savings(m_l, t)[2] - savings(m_l, t)[0], 1e-3, np.radians(85)))


K10_X = DM10 * R_L / DR10
assert round(K10_X, 2) == 8.75                                                                     # line 801
assert [round(th_reach(m), 1) for m in (2, 5, 8.75, 20)] == [29.8, 33.8, 35.1, 36.1]
assert [round(th_mass(m)) for m in (2, 5, 8.75, 20)] == [71, 52, 35, 14] and round(th_mass(5), 1) == 51.8
assert (round(float(savings(5, 0)[0]), 2), round(float(savings(5, 0)[2]), 2)) == (6.87, 0.64)


def fig40():
    VB = (0, 0, W, 300)
    s = pscale(VB[3])
    ax = Ax((58, 76, 388, 240), (0, 25), (0, 60))
    m60 = _brentq(lambda m: th_mass(m) - 60.0, 0.5, K10_X)            # mass boundary leaves the top at 60 degrees
    mm = np.linspace(m60, K10_X, 40)
    tm = [th_mass(m) for m in mm]
    mr = np.linspace(K10_X, 25, 50)
    tr = [th_reach(m) for m in mr]
    t_x = th_reach(K10_X)
    pt = lambda xy: " ".join(f"{ax.X(a):.2f},{ax.Y(b):.2f}" for a, b in xy)        # noqa: E731
    reg_m = [(0, 0), (K10_X, 0), (K10_X, t_x)] + list(zip(mm[::-1], tm[::-1])) + [(0, 60)]
    reg_r = [(K10_X, 0), (25, 0), (25, tr[-1])] + list(zip(mr[::-1], tr[::-1]))
    reg_t = list(zip(mm, tm)) + list(zip(mr, tr)) + [(25, 60), (m60, 60)]
    cols = (SER[1], SER[0], SER[2])
    o = []
    for reg, col in zip((reg_m, reg_r, reg_t), cols):
        o.append(f'<polygon points="{pt(reg)}" fill="{col}" opacity="0.2"/>')
    o += axes(s, ax, [(v, f"{v}") for v in range(0, 26, 5)], [(v, f"{v}°") for v in range(0, 61, 15)],
              f"base load m{sub('L', s, 'label')} (kg)", "forearm angle θ", grid=False, ylab_x=16, xlab_dy=42)
    ml = np.linspace(2.0, K10_X, 28)
    o.append(curve(s, ax, ml, [th_reach(m) for m in ml], I["secondary"], "leader", DASH_SER))
    o.append(curve(s, ax, [K10_X, K10_X], [0, t_x], I["primary"], "curve_multi"))
    o.append(curve(s, ax, mm, tm, I["primary"], "curve_multi"))
    o.append(curve(s, ax, mr, tr, I["primary"], "curve_multi"))
    t5 = th_mass(5)
    o.append(dot(s, ax.X(5), ax.Y(t5), O["flag"]))
    o.append(lab(s, ax.X(5) + 8, ax.Y(t5) + 4, f"5 kg: {t5:.0f}°"))
    o.append(lab(s, ax.X(K10_X) + 5, ax.Y(4), f"{K10_X:.2f} kg at every θ", "label2", I["primary"]))
    o.append(lab(s, ax.X(4.4), ax.Y(8), "shed 2 kg", "label", anchor="middle"))
    o.append(lab(s, ax.X(17), ax.Y(14), "shorten reach 8 cm", "label", anchor="middle"))
    o.append(lab(s, ax.X(17), ax.Y(50), "lower the arm 15°", "label", anchor="middle"))
    o.append(lab(s, ax.X(0.4), ax.Y(22), "lowering = reach,", "label2", I["secondary"]))
    o.append(lab(s, ax.X(0.4), ax.Y(22) + 14, f"{th_reach(2):.0f}–{th_reach(20):.0f}°, 2–20 kg", "label2", I["secondary"]))
    o.append(swatch(ax.x0, 22, cols[0], 0.2))
    o.append(lab(s, ax.x0 + 28, 22, "shed 2 kg"))
    o.append(swatch(ax.x0 + 104, 22, cols[1], 0.2))
    o.append(lab(s, ax.x0 + 132, 22, "shorten reach 8 cm"))
    o.append(swatch(ax.x0, 42, cols[2], 0.2))
    o.append(lab(s, ax.x0 + 28, 42, "lower the arm 15°"))
    o += legend(s, ax.x0 + 150, 42, [(I["secondary"], DASH_SER, "lowering = reach")], gap=10)
    o.append(lab(s, ax.x0, 62, "solid lines: where the winner changes", "label2", I["secondary"]))
    aria = ("Problem K10 regime map over base load from 0 to 25 kilograms and forearm angle from 0 to 60 degrees, shaded "
            "by the intervention that saves the most elbow torque: shedding 2 kilograms (blue), shortening the reach by "
            "8 centimetres (red) or lowering the forearm 15 degrees (orange). A vertical boundary at 8.75 kilograms, the "
            "same at every angle, separates shedding mass from shortening reach. Above about 35 to 36 degrees lowering "
            "the arm beats shortening reach; for light loads it must also beat shedding mass, whose boundary rises from "
            f"35 degrees at 8.75 kilograms to {t5:.0f} degrees at 5 kilograms, an orange dot, and leaves the top of the map "
            f"at {m60:.1f} kilograms. A dashed line shows where lowering equals shortening reach, 30 to 36 degrees.")
    hm = np.linspace(0, 25, 101)
    pts = []
    for m in hm:
        r = th_reach(m) if m > 0.2 else float("nan")
        if m < K10_X:
            b = th_mass(m) if m > 0.5 else 90.0
            txt = f"mL = {m:.2f} kg: shed mass wins below {min(b, 90):.1f}°" + (", then lower the arm" if b < 60 else "")
            yb = min(b, 60)
        else:
            txt = f"mL = {m:.2f} kg: shorten reach wins below {r:.1f}°, then lower the arm"
            yb = r
        pts.append([ax.X(m), ax.Y(yb), txt])
    return svg(VB, aria, s, o, H.hover_attr(ax.box, pts))


FIGS = {
    10: ("Plot of required elbow torque versus forearm angle for loads", fig10),
    31: ("computed plot", fig31),
    32: ("computed plot", fig32),
    33: ("Tornado chart of the change in elbow muscle force for plus a", fig33),
    34: ("Disc compression versus load reach for five trunk angles, wi", fig34),
    35: ("Maximum holdable load versus forearm angle for a constant an", fig35),
    36: ("computed plot", fig36),
    37: ("computed plot", fig37),
    38: ("Average and peak stair-climbing power versus cadence for thr", fig38),
    39: ("Measured maximum voluntary torque falling with forearm angle", fig39),
    40: ("Regime map over load mass and forearm angle showing where sh", fig40),
}
