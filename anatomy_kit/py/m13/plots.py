"""Module 13 figures, group `plots` (15 figures): Labs A-D (main text), C4, D8 and K1-K9 (problems).

Every plotted number is computed here from the formula or the script the module text states.
Module 13 line numbers (module13.html): Lab A 212-243, Lab B 247-267, Lab C 273-300, Lab D 311-327, C4 358-360,
D8 416-418, K1 431-441, K2 445-455, K3 460-480, K4 482-493, K5 495-508, K6 510-522, K7 524-535, K8 537-552,
K9 554-573; Proposition 4.1 at 118-126.
Constants: m = 70 kg, m_up = 0.8 m (Lab A, K1, K8), tau_max = 1.5 N m/kg (older) / 1.0 N m/kg (frail);
h = 0.17 m, P ceiling 250 W (Lab B, K2, K7); W_tr = 0.60 m g = 412 N, ell_t = 0.30/sin 60 = 0.346 m,
d_m = 0.05 m, NIOSH 3400 N (Prop. 4.1, Lab C, D8, K3); ell = 1.0 m, x0 = 0.05 m, L = 0.60 m (Lab D, K4);
mu_shoe = 0.7, t_step = 0.35 s (K5); F_grip = 60 N, 2 N m lid (K6); M_L = 10 kg, d_b = 0.30 m (K9).
The text states no stature: 1.75 m (course reference, as Module 8) scales the body drawing of C4 only.
"""
import html
import math

import numpy as np

import house as H
import lynch_body as LB
from m05.plots_prob import Plot, label, legend, text_w, hov, svg

O, I, SER = H.OVERLAY, H.INK, H.SERIES
RED, BLUE, ORANGE = SER[0], SER[1], SER[2]
GRID = "#e6e6e6"
BOX = "#f7f4ef"
SAFE_TINT = 0.10
DASH_SER = (7, 4)

G, M = 9.81, 70.0
M_UP = 0.8 * M
W_TR = 0.60 * M * G
ELL_T = 0.30 / math.sin(math.radians(60))
D_M, NIOSH = 0.05, 3400.0


def comp(m_load, d_l, phi_deg):
    """Proposition 4.1 (Lab C code): disc compression, N."""
    c, sn = math.cos(math.radians(phi_deg)), math.sin(math.radians(phi_deg))
    return (W_TR * ELL_T * sn + m_load * G * d_l) / D_M + (W_TR + m_load * G) * c


def safe_load(d_l, phi_deg):
    """K3 code: largest load (kg) that keeps compression at the NIOSH limit."""
    c = math.cos(math.radians(phi_deg))
    d_tr = ELL_T * math.sin(math.radians(phi_deg))
    return (NIOSH - W_TR * (d_tr / D_M + c)) / (d_l / D_M + c) / G


def ref(s, x0, y, x1, col=None):
    """Dashed threshold line (the approved K2 precedent: ink, dashed)."""
    return H.line(s, x0, y, x1, y, col or I["primary"], "ref", H.DASH_REF)


def dpt(P, x, y, col):
    return P.dot(x, y, col)


def band(P, xa, xb):
    """Green safe-region tint over x in [xa, xb] (module 7-10 convention)."""
    return (f'<rect x="{P.X(xa):.2f}" y="{P.y1:.2f}" width="{P.X(xb) - P.X(xa):.2f}" height="{P.y0 - P.y1:.2f}" '
            f'fill="{O["neural"]}" opacity="{SAFE_TINT}"/>')


def it(t):
    return f'<tspan font-style="italic">{t}</tspan>'


def legend_col(s, x, y, items, dy=17):
    """Vertical legend: line swatch + text per row."""
    o = []
    for i, (col, txt) in enumerate(items):
        yy = y + i * dy
        o.append(H.line(s, x, yy - 4.5, x + 20, yy - 4.5, col, "curve_multi"))
        o.append(label(s, x + 25, yy, txt, "label2", I["secondary"]))
    return "".join(o)


def sb(t, s, size="label"):
    return H.sub(t, s, size)


# ================================================================ svg #13  Lab A: chair-rise torque against d
def lab_a():
    VB = (0, 0, 760, 332)
    s = H.Scale(760, 332)
    P = Plot(s, (86, 44, 730, 276), (0.15, 0.28), (0, 170))
    d = np.linspace(0.15, 0.28, 40)
    tau = M_UP * G * d
    tau_max = 1.5 * M
    d_star = tau_max / (M_UP * G)
    assert round(M_UP * G * 0.15) == 82 and round(M_UP * G * 0.28) == 154 and round(d_star, 2) == 0.19
    o = [band(P, 0.15, d_star)]
    o.append(P.axes([(v, f"{v:.2f}") for v in (0.15, 0.20, 0.25)], [(v, f"{v}") for v in (0, 50, 100, 150)],
                    "knee-to-COM distance d (m)", "knee torque τ (N m)", grid=(50, 100, 150), ytx=24))
    o.append(ref(s, P.x0, P.Y(tau_max), P.x1))
    o.append(P.curve(d, tau, RED))
    o.append(label(s, P.X(0.153), P.Y(tau_max) - 8, "ceiling 105 N m", "label2"))
    o.append(P.dot(0.15, tau[0], RED))
    o.append(label(s, P.X(0.15) + 10, P.Y(tau[0]) + 22, "82 N m: high firm chair", "label2"))
    o.append(P.dot(0.28, tau[-1], RED))
    o.append(label(s, P.X(0.28) - 8, P.Y(tau[-1]) - 12, "154 N m: low soft chair", "label2", anchor="end"))
    o.append(P.dot(d_star, tau_max, O["flag"]))
    o.append(label(s, P.X(d_star) + 12, P.Y(tau_max) + 24, f"crossing at d = {d_star:.3f} m", "label2"))
    o.append(label(s, P.X(0.153), P.y0 - 10, "rise possible", "label2", I["secondary"]))
    o.append(label(s, P.x1 - 8, P.y0 - 10, "rise impossible without arms or momentum", "label2", I["secondary"], "end"))
    o.append(legend(s, 86, 22, [(RED, f"required τ = m{sb('up', s, 'label2')} g d, m{sb('up', s, 'label2')} = 56 kg", None),
                                (I["primary"], "older-adult ceiling 1.5 N m/kg × 70 kg", H.DASH_REF)]))
    aria = ("Lab A plot: the required quasi-static knee torque against the knee-to-COM distance d from 0.15 to 0.28 metres. "
            "It rises linearly from 82 newton metres at 0.15 to 154 newton metres at 0.28. A dashed line marks an older "
            "adult's ceiling of 105 newton metres; the line crosses it at d = 0.191 metres. A green tint marks the "
            "distances below the crossing, where the rise is possible.")
    hv = hov(P, d, [tau], lambda i: f"d = {d[i]:.3f} m: required {tau[i]:.0f} N m (ceiling 105 N m)")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #15  Lab B: stair power against cadence
def lab_b():
    VB = (0, 0, 760, 332)
    s = H.Scale(760, 332)
    P = Plot(s, (86, 44, 730, 276), (0.5, 2.5), (0, 320))
    h = 0.17
    f = np.linspace(0.5, 2.5, 40)
    pw = M * G * h * f
    f_max = 250.0 / (M * G * h)
    assert round(M * G * h) == 117 and round(f_max, 1) == 2.1
    o = [band(P, 0.5, f_max)]
    o.append(P.axes([(v, f"{v}") for v in (0.5, 1.0, 1.5, 2.0, 2.5)], [(v, f"{v}") for v in (0, 100, 200, 300)],
                    "cadence f (steps/s)", "gravity power P (W)", grid=(100, 200, 300), ytx=24))
    o.append(ref(s, P.x0, P.Y(250), P.x1))
    o.append(P.curve(f, pw, RED))
    o.append(label(s, P.X(0.53), P.Y(250) - 8, "ceiling 250 W", "label2"))
    o.append(P.dot(f_max, 250, O["flag"]))
    o.append(H.line(s, P.X(f_max), P.Y(250) + 6, P.X(f_max), P.y0, I["rule"], "leader"))
    o.append(label(s, P.X(f_max) - 8, P.Y(130), f"f{sb('max', s, 'label2')} = {f_max:.2f} steps/s", "label2", anchor="end"))
    o.append(label(s, P.X(0.53), P.y0 - 10, "sustainable", "label2", I["secondary"]))
    o.append(label(s, P.x1 - 8, P.y0 - 10, "above the ceiling: cadence must fall", "label2", I["secondary"], "end"))
    o.append(legend(s, 86, 22, [(RED, f"P = m g h f = 117 J × f", None),
                                (I["primary"], "sustained leg power ceiling 250 W", H.DASH_REF)]))
    aria = ("Lab B plot: stair-climbing gravity power against cadence from 0.5 to 2.5 steps per second. Power rises "
            "linearly at 117 joules per step. A dashed line marks the 250 watt sustained-power ceiling, reached at 2.14 "
            "steps per second; a green tint marks the cadences below it.")
    hv = hov(P, f, [pw], lambda i: f"{f[i]:.2f} steps/s: {pw[i]:.0f} W (ceiling 250 W)")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #17  Lab C: compression against load distance
def lab_c():
    VB = (0, 0, 760, 352)
    s = H.Scale(760, 352)
    P = Plot(s, (86, 54, 590, 296), (0.20, 0.55), (1500, 5200))
    dl = np.linspace(0.20, 0.55, 80)
    cases = [(20, 60, RED, None, "20 kg, stoop 60°"), (10, 60, RED, DASH_SER, "10 kg, stoop 60°"),
             (20, 20, BLUE, None, "20 kg, squat 20°"), (10, 20, BLUE, DASH_SER, "10 kg, squat 20°")]
    assert round(comp(20, 0.20, 20)) == 2333 and round(comp(20, 0.55, 60)) == 4934 and round(comp(20, 0.20, 60)) == 3561
    d_cross = (NIOSH - (W_TR + 20 * G) * math.cos(math.radians(20)) - W_TR * ELL_T * math.sin(math.radians(20)) / D_M) \
        / (20 * G / D_M)
    assert round(d_cross, 2) == 0.47
    o = [P.axes([(v, f"{v:.2f}") for v in (0.20, 0.30, 0.40, 0.50)] + [(0.55, "0.55")],
                [(v, f"{v}") for v in (2000, 3000, 4000, 5000)],
                "load distance d" + sb("L", s) + " (m)", "spinal compression F" + sb("comp", s) + " (N)",
                grid=(2000, 3000, 4000, 5000), ytx=22)]
    o.append(ref(s, P.x0, P.Y(NIOSH), P.x1))
    o.append(label(s, P.X(0.235), P.Y(NIOSH) - 6, "NIOSH limit 3400 N", "label2"))
    series = {}
    for ml, phi, col, dash, name in cases:
        ys = [comp(ml, x, phi) for x in dl]
        series[name] = ys
        o.append(P.curve(dl, ys, col, multi=True, dash=dash))
    ends = {n: series[n][-1] for n in series}
    off = {"20 kg, stoop 60°": 0, "10 kg, stoop 60°": -7, "20 kg, squat 20°": 7, "10 kg, squat 20°": 0}
    for n, yv in ends.items():
        o.append(label(s, P.x1 + 10, P.Y(yv) + 4.5 + off[n], n, "label2"))
    o.append(P.dot(d_cross, NIOSH, O["flag"]))
    o.append(H.line(s, P.X(d_cross), P.Y(NIOSH) + 6, P.X(d_cross), P.y0, I["rule"], "leader"))
    o.append(label(s, P.X(d_cross) - 6, P.y0 - 8, "20 kg squat crosses at 0.47 m", "label2", anchor="end"))
    o.append(P.dot(0.20, comp(20, 0.20, 20), BLUE))
    o.append(label(s, P.X(0.20) + 10, P.Y(comp(20, 0.20, 20)) + 20, "2333 N", "label2"))
    o.append(P.dot(0.55, comp(20, 0.55, 60), RED))
    o.append(label(s, P.X(0.55) - 8, P.Y(comp(20, 0.55, 60)) - 10, "4934 N", "label2", anchor="end"))
    o.append(P.dot(0.20, comp(20, 0.20, 60), RED))
    o.append(label(s, P.X(0.20) + 8, P.Y(comp(20, 0.20, 60)) - 17, "3561 N", "label2"))
    o.append(legend(s, 62, 22, [(RED, "stoop 60°", None), (BLUE, "squat 20°", None),
                                (I["secondary"], "20 kg", None), (I["secondary"], "10 kg", DASH_SER)], gap=22))
    aria = ("Lab C plot: spinal compression against load distance from 0.20 to 0.55 metres for a 10 and a 20 kilogram load at "
            "a 60 degree stoop (red) and a 20 degree squat (blue); solid lines are 20 kilograms, dashed lines 10 kilograms. "
            "A dashed horizontal line marks the NIOSH 3400 newton limit. The 20 kilogram stoop starts at 3561 newtons and "
            "ends at 4934, always above the limit; the 20 kilogram squat runs from 2333 newtons and crosses the limit at "
            "0.47 metres.")
    keys = list(series)
    hv = hov(P, dl, [series[k] for k in keys],
             lambda i: f"d = {dl[i]:.2f} m: " + ", ".join(f"{k.split(',')[0]} {k.split(', ')[1]} {series[k][i]:.0f} N" for k in keys))
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #19  Lab D: recovery step against forward speed
def lab_d():
    VB = (0, 0, 760, 332)
    s = H.Scale(760, 332)
    P = Plot(s, (86, 44, 730, 276), (0.3, 1.8), (0, 0.8))
    w0 = math.sqrt(G / 1.0)
    x0, reach = 0.05, 0.60
    v = np.linspace(0.3, 1.8, 76)
    xi = x0 + v / w0
    k = math.exp(w0 * 0.10)
    xid = xi * k
    v_max, v_dly = w0 * (reach - x0), w0 * (reach / k - x0)
    assert round(x0 + 1.0 / w0, 2) == 0.37 and round(v_max, 2) == 1.72 and round(v_dly, 2) == 1.22
    o = [P.axes([(0.5, "0.5"), (1.0, "1.0"), (1.5, "1.5")], [(v_, f"{v_:.1f}") for v_ in (0, 0.2, 0.4, 0.6, 0.8)],
                "forward COM speed ẋ (m/s)", "recovery step (m)", grid=(0.2, 0.4, 0.6, 0.8), ytx=24)]
    o.append(ref(s, P.x0, P.Y(reach), P.x1))
    o.append(label(s, P.X(0.33), P.Y(reach) - 8, "maximum reachable step 0.60 m", "label2"))
    o.append(P.curve(v, xid, ORANGE, multi=True))
    o.append(P.curve(v, xi, RED, multi=True))
    o.append(P.dot(v_max, reach, O["flag"]))
    o.append(label(s, P.X(v_max) - 8, P.Y(reach) - 8, f"{v_max:.2f} m/s", "label2", anchor="end"))
    o.append(P.dot(v_dly, reach, O["flag"]))
    o.append(label(s, P.X(v_dly) - 8, P.Y(reach) - 8, f"{v_dly:.2f} m/s", "label2", anchor="end"))
    o.append(P.dot(1.0, x0 + 1.0 / w0, RED))
    o.append(label(s, P.X(1.0) + 10, P.Y(x0 + 1.0 / w0) + 22, "0.37 m at 1.0 m/s: within reach", "label2"))
    o.append(label(s, P.X(0.33), P.Y(0.745), "to the right of a crossing no single step is long enough", "label2", I["secondary"]))
    o.append(legend(s, 86, 22, [(RED, "required step ξ = x₀ + ẋ/ω₀", None),
                                (ORANGE, "with a 100 ms reaction delay, ξ e" + " " + "<tspan baseline-shift=\"super\" font-size=\"" + f"{s(9.5):.2f}" + "\">ω₀Δt</tspan>", None)]))
    aria = ("Lab D plot: the recovery step a trip demands against forward COM speed from 0.3 to 1.8 metres per second. "
            "The required step, x0 plus speed over omega0, rises linearly from 0.15 to 0.69 metres and is 0.37 metres at "
            "1.0 metres per second. A dashed line marks the maximum reachable step of 0.60 metres, crossed at 1.72 metres "
            "per second. A second line, with a 100 millisecond reaction delay, is steeper and crosses it at 1.22 metres "
            "per second. The lab code draws speeds to 1.5; the curves continue to 1.8 to show the crossing.")
    hv = hov(P, v, [xi, xid], lambda i: f"ẋ = {v[i]:.2f} m/s: step {xi[i]:.2f} m, with delay {xid[i]:.2f} m")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ problem figures (400 px)
W = 400


def pfig(vb_h):
    return (0, 0, W, vb_h), H.Scale(W, vb_h, display_w=400)


# ---------------------------------------------------------------- svg #37 D8: maximum safe load against distance
def d8():
    VB, s = pfig(290)
    P = Plot(s, (58, 48, 388, 218), (0.20, 0.55), (0, 50))
    dl = np.linspace(0.20, 0.55, 80)
    sq = [safe_load(x, 20) for x in dl]
    st = [safe_load(x, 60) for x in dl]
    assert round(safe_load(0.25, 20), 0) == 35 and round(safe_load(0.40, 60), 1) == 8.7
    o = [P.axes([(v, f"{v:.2f}") for v in (0.20, 0.30, 0.40, 0.50)] + [(0.55, "0.55")], [(v, f"{v}") for v in (0, 10, 20, 30, 40, 50)],
                "load distance d" + sb("L", s) + " (m)", "max safe load (kg)", grid=(10, 20, 30, 40, 50), ytx=12)]
    o.append(P.curve(dl, sq, BLUE, multi=True))
    o.append(P.curve(dl, st, RED, multi=True))
    o.append(P.dot(0.25, safe_load(0.25, 20), BLUE))
    o.append(label(s, P.X(0.25) + 9, P.Y(safe_load(0.25, 20)) - 10, "35.0 kg at 0.25 m", "label2"))
    o.append(P.dot(0.40, safe_load(0.40, 60), RED))
    o.append(label(s, P.X(0.40), P.Y(safe_load(0.40, 60)) + 19, "8.7 kg at 0.40 m", "label2", anchor="middle"))
    o.append(label(s, P.X(0.47), P.Y(safe_load(0.47, 20)) - 12, "squat 20°", "label2", anchor="middle"))
    o.append(label(s, P.X(0.47), P.Y(safe_load(0.47, 60)) - 12, "stoop 60°", "label2", anchor="middle"))
    o.append(legend(s, 58, 20, [(BLUE, "squat φ = 20°", None), (RED, "stoop φ = 60°", None)]))
    aria = ("Problem D8 plot: the largest load that keeps spinal compression at the 3400 newton limit against its distance "
            "from the spine, 0.20 to 0.55 metres, falling roughly as one over distance. The squat curve (20 degrees, blue) "
            "is 35.0 kilograms at 0.25 metres; the stoop curve (60 degrees, red) is 8.7 kilograms at 0.40 metres.")
    hv = hov(P, dl, [sq, st], lambda i: f"d = {dl[i]:.2f} m: squat {sq[i]:.1f} kg, stoop {st[i]:.1f} kg")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- svg #40 K1: the chair an older adult can leave
def k1():
    VB, s = pfig(290)
    P = Plot(s, (58, 62, 388, 232), (0.10, 0.30), (0, 180))
    d = np.linspace(0.10, 0.30, 201)
    tau = M_UP * G * d
    old, frail = 1.5 * M, 1.0 * M
    d_old, d_fr = old / (M_UP * G), frail / (M_UP * G)
    assert round(d_old, 2) == 0.19 and round(d_fr, 2) == 0.13
    o = [P.axes([(v, f"{v:.2f}") for v in (0.10, 0.15, 0.20, 0.25, 0.30)], [(v, f"{v}") for v in (0, 50, 100, 150)],
                "knee-to-COM distance d (m)", "knee torque τ (N m)", grid=(50, 100, 150), ytx=12)]
    for c in (old, frail):
        o.append(ref(s, P.x0, P.Y(c), P.x1))
    o.append(P.curve(d, tau, RED, multi=True))
    for dd, c in ((d_old, old), (d_fr, frail)):
        o.append(H.line(s, P.X(dd), P.Y(c) + 5, P.X(dd), P.y0, I["rule"], "leader"))
        o.append(P.dot(dd, c, O["flag"]))
    o.append(label(s, P.X(0.298), P.Y(old) - 7, "older 105 N m", "label2", anchor="end"))
    o.append(label(s, P.X(0.298), P.Y(frail) - 7, "frail 70 N m", "label2", anchor="end"))
    o.append(label(s, P.X(d_old) + 6, P.y0 - 8, f"d ≤ {d_old:.2f} m", "label2"))
    o.append(label(s, P.X(d_fr) + 6, P.y0 - 8, f"d ≤ {d_fr:.2f} m", "label2"))
    o.append(legend(s, 58, 20, [(RED, f"required τ = m{sb('up', s, 'label2')} g d", None)]))
    aria = ("Problem K1 plot: the required knee torque against the knee-to-COM distance d from 0.10 to 0.30 metres, "
            "rising linearly from 55 to 165 newton metres. Two dashed lines mark ceilings: 105 newton metres for a typical "
            "older adult, crossed at d = 0.19 metres, and 70 newton metres for a frail adult, crossed at d = 0.13 metres.")
    hv = hov(P, d, [tau], lambda i: f"d = {d[i]:.3f} m: {tau[i]:.0f} N m")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- svg #42 K2: the cadence ceiling
def k2():
    VB, s = pfig(290)
    P = Plot(s, (58, 62, 388, 232), (0.5, 2.5), (0, 400))
    h = 0.17
    f = np.linspace(0.5, 2.5, 81)
    masses = [(70, RED), (90, BLUE)]
    fm = {m: 250.0 / (m * G * h) for m, _ in masses}
    assert round(fm[70], 2) == 2.14 and round(fm[90], 2) == 1.67
    o = [P.axes([(v, f"{v}") for v in (0.5, 1.0, 1.5, 2.0, 2.5)], [(v, f"{v}") for v in (0, 100, 200, 300, 400)],
                "cadence f (steps/s)", "gravity power P (W)", grid=(100, 200, 300, 400), ytx=12)]
    o.append(ref(s, P.x0, P.Y(250), P.x1))
    o.append(label(s, P.X(0.53), P.Y(250) - 7, "ceiling 250 W", "label2"))
    for m, col in masses:
        o.append(P.curve(f, m * G * h * f, col, multi=True))
    for m, col in masses:
        o.append(H.line(s, P.X(fm[m]), P.Y(250) + 5, P.X(fm[m]), P.y0, I["rule"], "leader"))
        o.append(P.dot(fm[m], 250, col))
    o.append(label(s, P.X(fm[90]) - 6, P.y0 - 8, f"{fm[90]:.2f}", "label2", anchor="end"))
    o.append(label(s, P.X(fm[70]) + 6, P.y0 - 8, f"{fm[70]:.2f}", "label2"))
    o.append(label(s, P.X(1.0), P.Y(m_p := 70 * G * h * 1.0) + 30, "70 kg", "label2", anchor="middle"))
    o.append(label(s, P.X(0.78), P.Y(90 * G * h * 0.78) - 20, "90 kg", "label2", anchor="middle"))
    o.append(legend(s, 58, 20, [(RED, "70 kg: f" + sb("max", s, "label2") + " = 2.14", None),
                                (BLUE, "90 kg: f" + sb("max", s, "label2") + " = 1.67", None)]))
    aria = ("Problem K2 plot: gravity power against stair cadence, 0.5 to 2.5 steps per second, for a 70 kilogram climber "
            "(red) and a 90 kilogram climber (blue). A dashed line marks the 250 watt ceiling. The maximum sustainable "
            "cadence is 2.14 steps per second at 70 kilograms and 1.67 at 90 kilograms, a 22 percent fall for a 29 percent "
            "rise in mass.")
    hv = hov(P, f, [70 * G * h * f, 90 * G * h * f],
             lambda i: f"{f[i]:.2f} steps/s: 70 kg {70 * G * h * f[i]:.0f} W, 90 kg {90 * G * h * f[i]:.0f} W")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- svg #44 K3: the safe-lift envelope, three trunk angles
def k3():
    VB, s = pfig(300)
    P = Plot(s, (58, 62, 358, 242), (0.20, 0.55), (0, 50))
    dl = np.linspace(0.20, 0.55, 80)
    cv = [(20, BLUE), (40, ORANGE), (60, RED)]
    assert round(safe_load(0.25, 20), 1) == 35.0 and round(safe_load(0.55, 60), 1) == 6.4
    assert round(safe_load(0.40, 20), 1) == 23.2 and round(safe_load(0.25, 60), 1) == 13.4
    o = [P.axes([(v, f"{v:.2f}") for v in (0.20, 0.30, 0.40, 0.50)] + [(0.55, "0.55")], [(v, f"{v}") for v in (0, 10, 20, 30, 40, 50)],
                "load distance d" + sb("L", s) + " (m)", "max safe load (kg)", grid=(10, 20, 30, 40, 50), ytx=12)]
    for phi, col in cv:
        o.append(P.curve(dl, [safe_load(x, phi) for x in dl], col, multi=True))
    marks = [(0.25, 20, BLUE, "35.0", (8, -9)), (0.40, 20, BLUE, "23.2", (6, -9)), (0.40, 60, RED, "8.7", (0, 19)),
             (0.25, 60, RED, "13.4", (6, -9)), (0.55, 60, RED, "6.4", (-8, 18))]
    for x, phi, col, t, (dx, dy) in marks:
        o.append(P.dot(x, safe_load(x, phi), col))
        o.append(label(s, P.X(x) + dx, P.Y(safe_load(x, phi)) + dy, t, "label2", anchor="start" if dx > 0 else "end"))
    for phi, col in cv:
        o.append(label(s, P.x1 + 8, P.Y(safe_load(0.55, phi)) + 4.5 + {20: 0, 40: 0, 60: 10}[phi], f"{phi}°", "label2"))
    o.append(legend(s, 58, 20, [(BLUE, "φ = 20°", None), (ORANGE, "φ = 40°", None), (RED, "φ = 60°", None)]))
    aria = ("Problem K3 plot: the largest load that keeps spinal compression under 3400 newtons against load distance, "
            "0.20 to 0.55 metres, for trunk angles of 20 degrees (blue), 40 degrees (orange) and 60 degrees (red). "
            "Marked points in kilograms: 35.0 at 20 degrees and 0.25 metres, 23.2 at 20 degrees and 0.40, 13.4 at 60 degrees "
            "and 0.25, 8.7 at 60 degrees and 0.40, and 6.4 at 60 degrees and 0.55.")
    hv = hov(P, dl, [[safe_load(x, 20) for x in dl], [safe_load(x, 40) for x in dl], [safe_load(x, 60) for x in dl]],
             lambda i: f"d = {dl[i]:.2f} m: 20° {safe_load(dl[i], 20):.1f} kg, 40° {safe_load(dl[i], 40):.1f} kg, "
                       f"60° {safe_load(dl[i], 60):.1f} kg")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- svg #46 K4: recoverable speed against delay
def k4():
    VB, s = pfig(290)
    P = Plot(s, (58, 50, 388, 220), (0, 0.25), (0, 2))
    w0, x0, L = math.sqrt(G / 1.0), 0.05, 0.60
    t = np.linspace(0, 0.25, 101)
    vm = w0 * (L * np.exp(-w0 * t) - x0)
    v_at = lambda dt: w0 * (L * math.exp(-w0 * dt) - x0)          # noqa: E731
    assert round(v_at(0), 2) == 1.72 and round(v_at(0.10), 2) == 1.22
    loss = 100 * (v_at(0) - v_at(0.10)) / v_at(0)
    assert round(loss, 1) == 29.3
    o = [P.axes([(v, f"{v:.2f}") for v in (0, 0.05, 0.10, 0.15, 0.20, 0.25)], [(v, f"{v}") for v in (0, 0.5, 1.0, 1.5, 2.0)],
                "reaction delay Δt (s)", "max recoverable speed (m/s)", grid=(0.5, 1.0, 1.5, 2.0), ytx=12)]
    o.append(P.curve(t, vm, RED))
    for dt in (0.0, 0.05, 0.10, 0.15, 0.20):
        o.append(P.dot(dt, v_at(dt), O["flag"] if dt in (0.0, 0.10) else RED))
    o.append(label(s, P.X(0.0) + 10, P.Y(v_at(0)) - 12, "1.72 m/s, no delay", "label2"))
    o.append(label(s, P.X(0.10) + 10, P.Y(v_at(0.10)) - 12, f"1.22 m/s at 100 ms: −{loss:.0f}%", "label2"))
    o.append(legend(s, 58, 20, [(RED, "ẋ" + sb("max", s, "label2") + " = ω₀(L e" + " " + "<tspan baseline-shift=\"super\" font-size=\"" + f"{s(9.5):.2f}" + "\">−ω₀Δt</tspan> − x₀)", None)]))
    aria = ("Problem K4 plot: the maximum forward speed from which a trip is recoverable in one 0.60 metre step, against "
            "reaction delay from 0 to 0.25 seconds. The curve falls from 1.72 metres per second with no delay to 1.22 at "
            "100 milliseconds, a 29 percent loss; dots mark delays of 0, 50, 100, 150 and 200 milliseconds.")
    hv = hov(P, t, [vm], lambda i: f"Δt = {t[i] * 1000:.0f} ms: {vm[i]:.2f} m/s")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- svg #48 K5: sharpest safe turn
def beta_max(v, mu, t_step=0.35):
    q = mu * G * t_step / (2 * v)
    return 180.0 if q >= 1.0 else 2 * math.degrees(math.asin(q))


def k5():
    VB, s = pfig(290)
    P = Plot(s, (58, 50, 388, 220), (0.8, 2.5), (0, 200))
    v = np.linspace(0.8, 2.5, 171)
    hi = [beta_max(x, 0.7) for x in v]
    lo = [beta_max(x, 0.3) for x in v]
    assert round(beta_max(1.3, 0.7)) == 135 and round(beta_max(2.0, 0.7)) == 74 and round(beta_max(1.3, 0.3), 1) == 46.7
    v_knee = 0.7 * G * 0.35 / 2
    o = [P.axes([(v_, f"{v_}") for v_ in (1.0, 1.5, 2.0, 2.5)], [(0, "0"), (45, "45"), (90, "90"), (135, "135"), (180, "180")],
                "walking speed v (m/s)", "max turn β (deg)", grid=(45, 90, 135, 180), ytx=12)]
    o.append(P.curve(v, lo, BLUE, multi=True))
    o.append(P.curve(v, hi, RED, multi=True))
    o.append(P.dot(1.0, 180, RED))
    o.append(label(s, P.X(1.0) - 6, P.Y(180) - 9, "180° at 1.0 m/s", "label2"))
    o.append(P.dot(1.3, beta_max(1.3, 0.7), RED))
    o.append(label(s, P.X(1.3) + 10, P.Y(135) - 6, "135° at 1.3", "label2"))
    o.append(P.dot(2.0, beta_max(2.0, 0.7), RED))
    o.append(label(s, P.X(2.0) + 6, P.Y(74) - 12, "74° at 2.0", "label2"))
    o.append(P.dot(1.3, beta_max(1.3, 0.3), BLUE))
    o.append(label(s, P.X(1.3) - 8, P.Y(beta_max(1.3, 0.3)) + 20, "47° at 1.3", "label2", anchor="end"))
    o.append(legend(s, 58, 20, [(RED, "μ = 0.7 (dry floor)", None), (BLUE, "μ = 0.3", None)]))
    aria = ("Problem K5 plot: the sharpest turn angle one step allows before the shoe slips, against walking speed from "
            "0.8 to 2.5 metres per second, for shoe-floor friction 0.7 (red) and 0.3 (blue), step time 0.35 seconds. With "
            "friction 0.7 any turn up to 180 degrees is possible up to 1.20 metres per second, then 135 degrees at 1.3 and "
            "74 degrees at 2.0; with friction 0.3 the turn at 1.3 metres per second is 47 degrees.")
    hv = hov(P, v, [hi, lo], lambda i: f"v = {v[i]:.2f} m/s: μ 0.7 {hi[i]:.0f}°, μ 0.3 {lo[i]:.0f}°")
    del v_knee
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- svg #50 K6: which aid opens the jar
def k6():
    VB, s = pfig(290)
    P = Plot(s, (58, 50, 388, 200), (0, 4), (0, 4.5))
    aids = [("bare", "hand", 0.5, 0.035), ("rubber", "pad", 1.0, 0.035), ("jar", "wrench", 0.7, 0.060),
            ("pad +", "wrench", 1.0, 0.060)]
    tq = [mu * 60.0 * r for _, _, mu, r in aids]
    assert [round(t, 2) for t in tq] == [1.05, 2.10, 2.52, 3.60]
    o = []
    for v in (1, 2, 3, 4):
        o.append(H.line(s, P.x0, P.Y(v), P.x1, P.Y(v), GRID, "leader"))
    o.append(H.line(s, P.x0, P.y0, P.x1, P.y0, I["axis"], "axis"))
    o.append(H.line(s, P.x0, P.y0, P.x0, P.y1, I["axis"], "axis"))
    for v in (0, 1, 2, 3, 4):
        o.append(H.line(s, P.x0 - 5, P.Y(v), P.x0, P.Y(v), I["axis"], "leader"))
        o.append(label(s, P.x0 - 8, P.Y(v) + 4.5, f"{v}", "tick", I["secondary"], "end"))
    o.append(label(s, 15, (P.y0 + P.y1) / 2, "opening torque (N m)", "label", I["primary"], "middle",
                   f'transform="rotate(-90 15 {(P.y0 + P.y1) / 2:.2f})"'))
    bw = 50
    pts = []
    for i, ((a, b, mu, r), t) in enumerate(zip(aids, tq)):
        xc = P.X(i + 0.5)
        col = BLUE if t >= 2.0 else RED
        o.append(f'<rect x="{xc - bw / 2:.2f}" y="{P.Y(t):.2f}" width="{bw}" height="{P.y0 - P.Y(t):.2f}" fill="{col}" '
                 f'opacity="0.85"/>')
        o.append(label(s, xc, P.Y(t) - 6, f"{t:.2f}", "label2", anchor="middle"))
        o.append(label(s, xc, P.y0 + 18, a, "label2", I["secondary"], "middle"))
        o.append(label(s, xc, P.y0 + 33, b, "label2", I["secondary"], "middle"))
        pts.append([round(xc, 2), round(P.Y(t), 2), f"{a} {b}: μ = {mu}, r = {r} m, torque {t:.2f} N m, "
                    + ("opens" if t >= 2.0 else "fails")])
    o.append(ref(s, P.x0, P.Y(2.0), P.x1))
    o.append(label(s, P.x0 + 6, P.Y(2.0) - 7, "lid: 2 N m", "label2"))
    o.append(legend(s, 58, 20, [(RED, "fails", None), (BLUE, "opens", None)]))
    o.append(label(s, 388, 20, "grip 60 N, τ = μ F r", "label2", I["secondary"], "end"))
    aria = ("Problem K6 bar chart: opening torque for a 60 newton grip, torque equals friction coefficient times grip times "
            "radius, against the 2 newton metre lid threshold shown as a dashed line. Bare hand 1.05 newton metres (red, "
            "fails); rubber pad 2.10, jar wrench 2.52 and pad plus wrench 3.60 (blue, open).")
    return svg(VB, aria, s, "".join(o), (P.box, pts))


# ---------------------------------------------------------------- svg #52 K7: uphill speed and downhill absorption
def k7():
    VB, s = pfig(400)
    m, P_c = M, 250.0
    A = Plot(s, (58, 44, 388, 168), (4, 20), (0, 6))
    B = Plot(s, (58, 250, 388, 350), (4, 20), (0, 250))
    th = np.linspace(4, 20, 161)
    sn = np.sin(np.radians(th))
    vmx = P_c / (m * G * sn)
    absb = m * G * 1.0 * sn
    chk = lambda a: P_c / (m * G * math.sin(math.radians(a)))      # noqa: E731
    assert [round(chk(a), 1) for a in (5, 10, 15)] == [4.2, 2.1, 1.4]
    o = [A.axes([(a, f"{a}") for a in (5, 10, 15, 20)], [(v, f"{v}") for v in (0, 2, 4, 6)],
                "", "max uphill speed (m/s)", grid=(2, 4, 6), ytx=12)]
    o.append(label(s, A.x0 + 6, A.y1 + 2, "", "label2"))
    o.append(A.curve(th, vmx, RED))
    for a in (5, 10, 15):
        o.append(A.dot(a, chk(a), RED))
        o.append(label(s, A.X(a) + 9, A.Y(chk(a)) - 8, f"{chk(a):.1f} m/s", "label2"))
    o.append(label(s, A.x1, A.y1 + 18, "v" + sb("max", s, "label2") + " = P / (m g sin θ), P = 250 W", "label2", I["secondary"], "end"))
    o.append(label(s, A.x1, A.y1 + 34, "walking up", "label2", I["secondary"], "end"))
    o.append(B.axes([(a, f"{a}") for a in (5, 10, 15, 20)], [(v, f"{v}") for v in (0, 100, 200)],
                    "slope θ (deg)", "downhill absorption (W)", grid=(100, 200), ytx=12))
    o.append(B.curve(th, absb, BLUE))
    for a in (5, 10, 15, 20):
        w = m * G * math.sin(math.radians(a))
        o.append(B.dot(a, w, BLUE))
        if a == 20:
            o.append(label(s, B.X(a) - 6, B.Y(w) - 9, f"{w:.0f} W", "label2", anchor="end"))
        else:
            o.append(label(s, B.X(a) + 7, B.Y(w) + 17, f"{w:.0f} W", "label2"))
    o.append(label(s, B.x1 - 4, B.y0 - 10, "walking down at 1.0 m/s: m g sin θ", "label2", I["secondary"], "end"))
    aria = ("Problem K7, two panels sharing the slope axis from 4 to 20 degrees. Top: the maximum uphill walking speed "
            "for a 250 watt power budget, falling as one over sine theta: 4.2 metres per second at 5 degrees, 2.1 at 10 and "
            "1.4 at 15. Bottom: the power a 70 kilogram walker must absorb going down at 1.0 metres per second, rising "
            "from 60 watts at 5 degrees to 235 watts at 20 degrees.")
    hva = hov(A, th, [vmx], lambda i: f"θ = {th[i]:.1f}°: up at most {vmx[i]:.2f} m/s")
    hvb = hov(B, th, [absb], lambda i: f"θ = {th[i]:.1f}°: down at 1.0 m/s absorbs {absb[i]:.0f} W")
    extra = H.hover_attr([(A.box, hva), (B.box, hvb)])
    return H.svg_open(VB, html.escape(aria), s, extra=extra) + "".join(o) + "</svg>"


# ---------------------------------------------------------------- svg #54 K8: brisk rise torque against time
def k8():
    VB, s = pfig(290)
    P = Plot(s, (58, 50, 388, 220), (0, 1.6), (70, 150))
    H_RISE, d = 0.40, 0.20

    def run(T, n=161):
        t = np.linspace(0, T, n)
        u = t / T
        a = (H_RISE / T ** 2) * (60 * u - 180 * u ** 2 + 120 * u ** 3)
        return t, M_UP * (G + a) * d

    qs = M_UP * G * d
    t12, tau12 = run(1.2, 20001)
    assert round(qs) == 110 and round(tau12.max()) == 128 and round(tau12.min()) == 92
    peak = {Tb: M_UP * (G + (H_RISE / Tb ** 2) * (10 / math.sqrt(3))) * d for Tb in (1.6, 1.2, 0.9)}
    assert round(peak[0.9]) == 142
    cs = [(1.6, BLUE), (1.2, RED), (0.9, ORANGE)]
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.4, 0.8, 1.2, 1.6)], [(v, f"{v}") for v in (70, 90, 110, 130, 150)],
                "time t (s)", "knee torque (N m)", grid=(90, 130, 150), ytx=12)]
    o.append(ref(s, P.x0, P.Y(qs), P.x1))
    o.append(label(s, P.X(1.6) - 2, P.Y(qs) - 7, "quasi-static 110 N m", "label2", anchor="end"))
    data = {}
    for Tb, col in cs:
        t, tau = run(Tb)
        data[Tb] = (t, tau)
        o.append(P.curve(t, tau, col, multi=True))
    for Tb, col in cs:
        t, tau = data[Tb]
        k = int(np.argmax(tau))
        o.append(P.dot(t[k], tau[k], col))
    tmin = M_UP * (G + (H_RISE / 1.44) * -5.7735) * d
    o.append(label(s, P.X(0.99), P.Y(tmin) + 22, "1.2 s: trough 92 N m", "label2", I["secondary"]))
    o.append(label(s, P.X(0.69), P.Y(78.0) + 14, "0.9 s", "label2", I["secondary"], "middle"))
    o.append(label(s, P.X(1.58), P.Y(104.0) + 20, "1.6 s", "label2", I["secondary"], "end"))
    o.append(legend_col(s, 214, 50, [(BLUE, "T = 1.6 s: peak 120 N m"), (RED, "T = 1.2 s: peak 128 N m"),
                                    (ORANGE, "T = 0.9 s: peak 142 N m")]))
    aria = ("Problem K8 plot: knee torque during a 0.40 metre minimum-jerk chair rise against time, for rise times of 1.6 "
            "seconds (blue), 1.2 seconds (red) and 0.9 seconds (orange). A dashed line marks the quasi-static 110 newton "
            "metres. The 1.2 second rise peaks at 128 newton metres early, dips to 92 later; the 0.9 second rise peaks at "
            "142 and the 1.6 second rise at 120.")
    tg = np.arange(0, 1.6001, 0.02)
    ys = []
    for x in tg:
        ys.append([P.Y(float(np.interp(x, *data[Tb]))) for Tb, _ in cs if x <= Tb + 1e-9])
    txt = []
    for x in tg:
        parts = [f"{Tb} s {float(np.interp(x, *data[Tb])):.0f}" for Tb, _ in cs if x <= Tb + 1e-9]
        txt.append(f"t = {x:.2f} s: " + ", ".join(parts) + " N m")
    pts = [[round(P.X(x), 2), (y if len(y) > 1 else y[0]), tx] for x, y, tx in zip(tg, ys, txt)]
    return svg(VB, aria, s, "".join(o), (P.box, pts))


# ---------------------------------------------------------------- svg #56 K9: splitting a carried load
def k9():
    VB, s = pfig(290)
    P = Plot(s, (58, 50, 388, 220), (0, 1), (0, 36))
    d_b, m_l = 0.30, 10.0
    al = np.linspace(0, 1, 101)
    mom = np.abs(2 * al - 1) * m_l * G * d_b
    lean = mom / W_TR
    fside = mom / D_M
    assert round(mom[-1], 1) == 29.4 and round(lean[-1], 3) == 0.071 and round(fside[-1]) == 589
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1.0)], [(v, f"{v}") for v in (0, 10, 20, 30)],
                "split fraction α (one hand)", "lateral moment (N m)", grid=(10, 20, 30), ytx=12)]
    o.append(P.curve(al, mom, RED))
    o.append(P.dot(0.5, 0, O["flag"]))
    o.append(label(s, P.X(0.5), P.Y(21), "even split α = 0.5:", "label2", anchor="middle"))
    o.append(label(s, P.X(0.5), P.Y(21) + 15, "0 N m, no lean", "label2", anchor="middle"))
    o.append(P.dot(1.0, mom[-1], RED))
    o.append(P.dot(0.0, mom[0], RED))
    o.append(label(s, P.X(1.0) - 6, P.Y(mom[-1]) - 9, "one bag: 29.4 N m", "label2", anchor="end"))
    o.append(label(s, P.X(0.0) + 6, P.Y(mom[0]) - 9, "all in the other hand", "label2"))
    o.append(label(s, P.x1 - 4, P.Y(7.2), "lean 0.071 m", "label2", I["secondary"], "end"))
    o.append(label(s, P.x1 - 4, P.Y(7.2) + 15, "side flexors 589 N", "label2", I["secondary"], "end"))
    o.append(legend(s, 58, 20, [(RED, "| 2α − 1 | M" + sb("L", s, "label2") + " g d" + sb("b", s, "label2"), None)]))
    aria = ("Problem K9 plot: the net lateral spinal moment of a 10 kilogram load carried in two hands at 0.30 metres each "
            "side of the spine, against the fraction alpha in one hand from 0 to 1. The curve is a V with its minimum, 0 "
            "newton metres and no trunk lean, at the even split alpha = 0.5; at alpha = 1, one bag, it is 29.4 newton "
            "metres, a 0.071 metre lean and 589 newtons in the side flexors.")
    hv = hov(P, al, [mom], lambda i: f"α = {al[i]:.2f}: {mom[i]:.1f} N m, lean {lean[i]:.3f} m, side flexors {fside[i]:.0f} N")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #23 C4: squat versus stoop (body)
H_M = 1.75


def _hold(P_kwargs, dl_px, height):
    """Shoulder flexion (elbow fixed) at which the hand centre is dl_px ahead of L5/S1; bisection."""
    lo, hi = -20.0, 110.0
    for _ in range(40):
        mid = (lo + hi) / 2
        kw = dict(P_kwargs)
        kw["near"] = dict(kw["near"], shoulder=mid, elbow=12)
        kw["far"] = dict(kw["far"], shoulder=mid, elbow=12)
        _, J = LB.draw("t", None, LB.pose(anchor=("heel", "near"), **kw), 0, 0, height)
        hx = (J["wrist"][0] + J["fingertip"][0]) / 2 - J["l5s1"][0]
        if hx < dl_px:
            lo = mid
        else:
            hi = mid
    return mid


def c4():
    VB = (0, 0, 400, 440)
    s = H.Scale(400, 440, display_w=400)
    p = "m13f23_"
    HP = 262.0                                   # stature, px
    kp = HP / H_M                                # px per metre
    cases = [
        dict(name="squat lift", phi=20, dl=0.25, x=58, tx=6, fcomp=comp(20, 0.25, 20),
             pose=dict(pelvis=10, trunk=10, near=dict(hip=100, knee=130), far=dict(hip=100, knee=130))),
        dict(name="stoop lift", phi=60, dl=0.40, x=214, tx=204, fcomp=comp(20, 0.40, 60),
             pose=dict(pelvis=35, trunk=25, near=dict(hip=45), far=dict(hip=45))),
    ]
    assert round(cases[0]["fcomp"], -1) == 2530 and round(cases[1]["fcomp"], -1) == 4350
    floor = 330.0
    o = [H.markers(p, s), H.line(s, 6, floor, 394, floor, I["rule"], "leader")]
    for c in cases:
        sh = _hold(c["pose"], c["dl"] * kp, HP)
        kw = dict(c["pose"])
        kw["near"] = dict(kw["near"], shoulder=sh, elbow=12)
        kw["far"] = dict(kw["far"], shoulder=sh, elbow=12)
        art, J = LB.draw(p, s, LB.pose(anchor=("heel", "near"), **kw), c["x"], floor, HP)
        lx, ly = J["l5s1"]
        phi = math.radians(c["phi"])
        cx, cy = lx + ELL_T * kp * math.sin(phi), ly - ELL_T * kp * math.cos(phi)
        hx = (J["wrist"][0] + J["fingertip"][0]) / 2
        hy = (J["wrist"][1] + J["fingertip"][1]) / 2
        assert abs((hx - lx) / kp - c["dl"]) < 0.005
        bw = 0.26 * kp
        top = min(J["bbox"][1], cy) - 6
        lt, ll = top - 40, top - 18                  # dimension levels: d_tr, d_L
        d_tr = ELL_T * math.sin(phi)
        o.append(f'<rect x="{hx - bw / 2:.2f}" y="{hy - bw / 2:.2f}" width="{bw:.2f}" height="{bw:.2f}" fill="{BOX}" '
                 f'stroke="{I["secondary"]}" stroke-width="{s(1.4):.2f}"/>')
        o.append(art)
        o.append(H.line(s, lx, ly, lx, lt - 6, O["dim"], "ref", H.DASH_REF))
        o.append(H.line(s, cx, cy, cx, lt, O["dim"], "ref", H.DASH_REF))
        o.append(H.line(s, hx, hy - bw / 2, hx, ll, O["dim"], "ref", H.DASH_REF))
        o.append(H.arrow(s, p, lx, lt, cx, lt, "geometry", both=True))
        o.append(H.arrow(s, p, lx, ll, hx, ll, "geometry", both=True))
        o.append(label(s, max(cx, lx) + 8, lt + 4.5, f"d{sb('tr', s, 'label2')} = {d_tr:.2f} m", "label2"))
        o.append(label(s, max(hx, lx) + 8, ll + 4.5, f"d{sb('L', s, 'label2')} = {c['dl']:.2f} m", "label2"))
        o.append(H.arrow(s, p, cx, cy, cx, cy + 0.085 * W_TR, "load"))
        o.append(H.com_mark(s, cx, cy))
        o.append(label(s, max(cx, hx) + 8, cy + 0.085 * W_TR - 2, f"W{sb('tr', s, 'label2')}", "label2"))
        o.append(H.arrow(s, p, hx, hy + bw / 2, hx, hy + bw / 2 + 0.085 * 196.2, "load"))
        o.append(label(s, hx + 8, hy + bw / 2 + 0.085 * 196.2 - 2, f"W{sb('L', s, 'label2')}", "label2"))
        o.append(H.joint_centre(s, lx, ly))
        o.append(label(s, lx - 9, ly + 4.5, "L5/S1", "label2", anchor="end"))
        o.append(label(s, c["tx"], floor + 18, c["name"] + f", φ = {c['phi']}°", "label"))
        o.append(label(s, c["tx"], floor + 36, f"F{sb('comp', s, 'label2')} ≈ {round(c['fcomp'], -1):.0f} N", "label"))
    o.append(label(s, 6, floor + 54, "20 kg box; upper body W" + sb("tr", s, "label2") + " = 412 N at 0.346 m along the trunk", "label2", I["secondary"]))
    o.append(LB.credit(s, 6, floor + 74, width=388))
    aria = ("Problem C4: two whole-body skeleton drawings lifting a 20 kilogram box, side by side. Left, a squat lift with "
            "the trunk 20 degrees from vertical and the box 0.25 metres ahead of the L5/S1 disc: the upper-body weight acts "
            "at 0.12 metres and spinal compression is about 2530 newtons. Right, a stoop lift with straight legs, trunk 60 "
            "degrees and the box 0.40 metres ahead: the upper-body weight acts at 0.30 metres and compression is about "
            "4350 newtons. Dashed lines drop from L5/S1, the upper-body centre of mass and the box to blue moment-arm "
            "dimensions; brown arrows show the weights.")
    return svg(VB, aria, s, "".join(o))


def com_dot(s, x, y):
    return H.com_mark(s, x, y)


FIGS = {
    13: ("Required chair-rise knee torque rising linearly with the kne", lab_a),
    15: ("Stair-climbing power rising linearly with cadence and meetin", lab_b),
    17: ("Spinal compression rising with load distance for a 10 kg and", lab_c),
    19: ("Required recovery-step length rising with forward COM speed,", lab_d),
    37: ("D8: the safe-lift envelope. From the compression limit, deri", d8),
    40: ("K1: the chair an older adult can leave (threshold + inverse)", k1),
    42: ("K2: the cadence ceiling (inverse + sensitivity). Find the ma", k2),
    44: ("K3: the safe-lift envelope. Three curves of the largest load", k3),
    46: ("K4: the recoverable envelope (2-parameter sweep). Compute th", k4),
    48: ("K5: the sharpest safe turn (friction limit). Find the maximu", k5),
    50: ("K6: which aid opens the jar? (regime comparison). For a weak", k6),
    52: ("K7: how fast can you climb the hill? (inverse + regime). Giv", k7),
    54: ("K8: does a brisk rise cost more torque? (dynamic simulation ", k8),
    56: ("K9: splitting a carried load (optimisation). A total load is", k9),
    23: ("C4: squat versus stoop. Why does squatting to lift load the ", c4),
}
