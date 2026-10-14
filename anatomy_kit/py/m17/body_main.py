"""Module 17 main-text figures in the house style (group `body_main`).

No figure of Module 17 draws a whole body, so the Lynch kit is not shared: SHARED_DEFS is empty.
Every plotted number is computed here from the formula or the code the module states:
  svg #4  Capstone I   the delayed-feedback simulation of the code in section 2 (Euler, 200 Hz, 1200 samples)
  svg #6  Capstone II  the minimum-jerk sit-to-stand code of section 3 (Model 3.1)
  svg #7  Capstones III-IV  Model 4.1 mid-stance value mg(1 - Fr) and the half-sine of Model 5.1
  svg #9  Capstone V   Model 6.1, F = m v^2 / 2d + m g
  svg #10 Capstone VI  Model 7.1, S/F = S0 (rho/rho0)^2 / (v sqrt(m_eff k_c))
  svg #2, #11 block diagrams (section 0 arc, Capstone VII chain); svg #13 is an illustration, not data.
"""
import math

import numpy as np

import house as H
from m05.plots_main import Ax, axes, curve, dot, hover, legend, poly, svg

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
BOX = "#f7f4ef"
RED, BLUE = SER[0], SER[1]


def SHARED_DEFS():  # noqa: N802 (apply_figs calls this name)
    return ""


def mn(v, f="{:.1f}"):
    """Number with a Unicode minus."""
    t = f.format(v)
    return "−" + t[1:] if t.startswith("-") else t


def sub(t, s):
    return H.sub(t, s, "label2")


# ================================================================ svg #4: Capstone I, delayed standing
def standing(delay):
    """The code of section 2, line for line (note: its loop starts at k = 1, so sample 1 is zero)."""
    g, L, m = 9.81, 1.0, 70.0
    Iz, kp, kd = m * L * L, 1.5 * m * g * L, 150.0
    dt = 1 / 200.0
    n = int(delay / dt)
    th, om = np.zeros(1200), np.zeros(1200)
    th[0] = 0.05
    for k in range(1, len(th) - 1):
        kk = max(0, k - n)
        thdd = (m * g * L * th[k] - (kp * th[kk] + kd * om[kk])) / Iz
        om[k + 1] = om[k] + thdd * dt
        th[k + 1] = th[k] + om[k + 1] * dt
    return np.arange(1200) * dt, np.degrees(th)


def fig4():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    t, a = standing(0.10)
    _, b = standing(0.20)
    peak100, peak200, end200 = np.abs(a).max(), np.abs(b).max(), b[-1]
    assert round(peak100, 1) == 2.9 and round(peak200, 1) == 63.2          # section 2 code comments
    lim = 34.4                                                              # the red trace leaves the axis here
    i_out = int(np.argmax(np.abs(b) > lim))
    t_out = t[i_out - 1] + (t[i_out] - t[i_out - 1]) * (lim - b[i_out - 1]) / (b[i_out] - b[i_out - 1])
    assert round(t_out, 1) == 4.7
    ax = Ax((80, 56, 730, 330), (0, 6), (-lim, lim))
    o = axes(s, ax, [(k, str(k)) for k in range(7)], [(-30, "−30"), (0, "0"), (30, "30")],
             "time (s)", "lean angle θ (degrees)")
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["rule"], "leader"))
    for v in (15, -15):                                                     # small-angle range, Model 2.1
        o.append(H.line(s, ax.x0, ax.Y(v), ax.x1, ax.Y(v), I["rule"], "ref", dash=H.DASH_REF))
    o.append(H.label(s, ax.x1 - 4, ax.Y(-15) + 17, "small-angle range ±15°", "label2", I["secondary"], "end"))
    draw = [0, 1, 2] + list(range(12, 1200, 12))            # 5 ms samples kept at the start, then every 60 ms
    o.append(curve(s, ax, t[draw], a[draw], BLUE, "curve_multi"))
    keep = [k for k in draw if k < i_out]
    xs = [ax.X(t[k]) for k in keep] + [ax.X(t_out)]
    ys = [ax.Y(b[k]) for k in keep] + [ax.Y(lim)]
    o.append(poly(s, list(zip(xs, ys)), RED, "curve_multi"))
    o.append(dot(s, ax.X(0), ax.Y(a[0]), O["flag"]))
    o.append(H.label(s, ax.X(0) + 11, ax.Y(a[0]) - 8, "initial lean 2.9°", "label2", I["primary"]))
    o.append(dot(s, ax.X(t_out), ax.Y(lim), RED, hollow=True))
    o.append(H.label(s, ax.X(t_out) + 12, ax.Y(lim) + 14, "leaves the axis at 34°, 4.7 s;", "label2", I["primary"]))
    o.append(H.label(s, ax.X(t_out) + 12, ax.Y(lim) + 30, f"reaches {mn(end200)}° at 6 s", "label2", I["primary"]))
    o.append(H.label(s, ax.X(2.75), ax.Y(-27.5), "Δ = 200 ms: falls", "label2", I["primary"], "start"))
    o.append(H.label(s, ax.X(5.97), ax.Y(-6.5), "Δ = 100 ms: stable", "label2", I["primary"], "end"))
    o += legend(s, 80, 30, [(BLUE, None, "Δ = 100 ms (stable)"), (RED, None, "Δ = 200 ms (falls)")], gap=34)
    aria = ("Lean angle against time for the delayed-feedback inverted pendulum, started from a 2.9 degree lean. With a "
            "100 ms delay (blue) the sway decays to a few tenths of a degree and stays inside the small-angle range of "
            "15 degrees. With a 200 ms delay (red), past the critical delay of 140.1 ms, the oscillation grows, leaves "
            "the axis at 34 degrees and 4.7 s, and reaches minus 63.2 degrees at 6 s.")
    hv = hover(ax, [ax.X(x) for x in t], [[ax.Y(p), ax.Y(max(-lim, min(lim, q)))] for p, q in zip(a, b)],
               [f"t = {x:.2f} s: 100 ms {mn(p)}°, 200 ms {mn(q)}°" for x, p, q in zip(t, a, b)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #6: Capstone II, knee torque
def sit_to_stand():
    """The code of section 3 (np.linspace 200 points, minimum jerk, two np.gradient calls)."""
    g, T_ = 9.81, 1.5
    t = np.linspace(0, T_, 200)
    sr = t / T_
    q = (np.pi / 2) * (1 - (10 * sr ** 3 - 15 * sr ** 4 + 6 * sr ** 5))
    qdd = np.gradient(np.gradient(q, t), t)
    m_hat, d0, I_k = 48.0, 0.20, 0.12
    tau0 = 0.15 * m_hat * g * d0
    grav = m_hat * g * d0 * np.sin(q)
    iner = I_k * np.abs(qdd)
    return t, q, grav, iner, tau0, grav + iner + tau0


def fig6():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    t, q, grav, iner, tau0, tau = sit_to_stand()
    kpk = int(np.argmax(tau))
    assert round(tau.max()) == 109 and round(tau.max() / 70, 2) == 1.55          # text: 109 N m, 1.55 N m/kg
    assert round(grav.max(), 1) == 94.2 and round(iner.max(), 2) == 0.48 and round(tau0, 1) == 14.1
    ax = Ax((80, 50, 730, 330), (0, 1.5), (0, 120))
    o = axes(s, ax, [(0, "0"), (0.5, "0.5"), (1.0, "1.0"), (1.5, "1.5")], [(v, str(v)) for v in (0, 30, 60, 90, 120)],
             "time (s)", "knee extensor torque (N m)")
    o.append(H.line(s, ax.x0, ax.Y(tau0), ax.x1, ax.Y(tau0), O["dim"], "ref", dash=H.DASH_REF))
    o.append(H.label(s, ax.X(0.04), ax.Y(tau0) - 8, f"baseline τ{sub('0', s)} = {tau0:.1f} N m", "label2", I["secondary"]))
    dr = list(range(0, 200, 2)) + [199]
    o.append(curve(s, ax, t[dr], tau[dr], RED))
    o.append(dot(s, ax.X(t[kpk]), ax.Y(tau[kpk]), O["flag"]))
    o.append(H.label(s, ax.X(t[kpk]) + 12, ax.Y(tau[kpk]) - 14, f"peak {tau.max():.0f} N m = {tau.max()/70:.2f} N m/kg", "label2",
                     I["primary"]))
    for k, txt in enumerate((f"at the peak: HAT weight on its moment arm {grav.max():.1f} N m,",
                             f"baseline {tau0:.1f} N m, inertia {iner.max():.2f} N m")):
        o.append(H.label(s, ax.X(0.06), ax.Y(52) + k * 17, txt, "label2", I["primary"]))
    o += legend(s, 80, 28, [(RED, None, "knee torque, Model 3.1 (minimum-jerk rise, T = 1.5 s)")])
    aria = ("Knee extensor torque against time over a 1.5 s sit-to-stand with a minimum-jerk knee trajectory. The torque "
            "starts at 108 newton-metres at seat-off, peaks at 109 newton-metres (1.55 newton-metres per kilogram) at about "
            "0.2 s, then falls with the sine of the knee angle to the 14.1 newton-metre baseline at standing.")
    hv = hover(ax, [ax.X(x) for x in t], [ax.Y(v) for v in tau],
               [f"t = {x:.2f} s: knee {math.degrees(a):.0f}°, torque {v:.1f} N m" for x, a, v in zip(t, q, tau)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #7: Capstones III-IV, walking and running GRF
def walking(x, fr):
    """Stylised walking GRF in BW against stance fraction x. Model 4.1 fixes only the mid-stance value 1 - Fr = 0.70;
    the 1.18 BW peaks come from the text; their position (26 %, 74 %) and the cosine joins are a drawing choice."""
    kn = [(0.0, 0.0), (0.26, 1.18), (0.50, 1 - fr), (0.74, 1.18), (1.0, 0.0)]
    for (x0, y0), (x1, y1) in zip(kn, kn[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (1 - math.cos(math.pi * (x - x0) / (x1 - x0))) / 2
    return 0.0


def fig7():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    g, L, v = 9.81, 1.0, 1.72
    fr = v * v / (g * L)                                                    # Model 4.1, Froude number
    beta = 0.20 / 0.33
    f_peak = (math.pi / 2) / beta                                           # Model 5.1, in BW
    assert round(fr, 2) == 0.30 and round(1 - fr, 2) == 0.70 and round(f_peak, 2) == 2.59
    xs = np.linspace(0, 1, 101)
    w = [walking(x, fr) for x in xs]
    r = [f_peak * math.sin(math.pi * x) for x in xs]
    ax = Ax((80, 50, 730, 330), (0, 1), (0, 3))
    o = axes(s, ax, [(0, "0"), (0.25, "25%"), (0.5, "50%"), (0.75, "75%"), (1, "100%")],
             [(0, "0"), (1, "1"), (2, "2"), (3, "3")], "stance phase", "vertical GRF (BW)")
    o.append(H.line(s, ax.x0, ax.Y(1), ax.x1, ax.Y(1), O["dim"], "ref", dash=H.DASH_REF))
    o.append(H.label(s, ax.x0 + 6, ax.Y(1) - 7, "1 BW", "label2", I["secondary"]))
    o.append(curve(s, ax, xs, r, RED, "curve_multi"))
    o.append(curve(s, ax, xs, w, BLUE, "curve_multi"))
    o.append(H.label(s, ax.X(0.5), ax.Y(f_peak) - 12, f"running: single hump, {f_peak:.2f} BW", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(0.5), ax.Y(1.62), "walking: twin peaks", "label2", I["primary"], "middle"))
    for x in (0.26, 0.74):
        o.append(H.label(s, ax.X(x), ax.Y(1.18) - 10, "1.18", "label2", I["primary"], "middle"))
    o.append(dot(s, ax.X(0.5), ax.Y(1 - fr), O["flag"]))
    o.append(H.label(s, ax.X(0.5), ax.Y(0.40), f"mid-stance {1 - fr:.2f} BW = mg(1 − Fr), Fr = {fr:.2f}:", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(0.5), ax.Y(0.40) + 17, "the one walking value Model 4.1 predicts", "label2", I["primary"], "middle"))
    o += legend(s, 80, 28, [(BLUE, None, "walking, v = 1.72 m/s"), (RED, None, "running, duty factor 0.606")], gap=34)
    aria = ("Vertical ground-reaction force in body weights over one stance. Walking (blue) has two 1.18 BW peaks around a "
            "mid-stance dip to 0.70 BW, the value Model 4.1 predicts as mg(1 - Fr) with Fr = 0.30; the peaks and the dip "
            "shape are drawn, not predicted. Running (red) is a single half-sine hump peaking at 2.59 BW. A dashed line "
            "marks 1 BW.")
    hv = hover(ax, [ax.X(x) for x in xs], [[ax.Y(a), ax.Y(b)] for a, b in zip(w, r)],
               [f"stance {100 * x:.0f}%: walking {a:.2f} BW, running {b:.2f} BW" for x, a, b in zip(xs, w, r)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #9: Capstone V, landing force
def fig9():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    g, m, h = 9.81, 70.0, 0.40
    v2 = 2 * g * h
    F = lambda d: (m * v2 / (2 * d) + m * g) / 1000                         # noqa: E731  Model 6.1, kN
    assert round(F(0.05), 1) == 6.2 and round(F(0.20), 1) == 2.1
    bw = m * g / 1000
    ds = np.linspace(0.02, 0.30, 113)
    fs = [F(d) for d in ds]
    ax = Ax((80, 50, 730, 330), (0, 0.30), (0, 15))
    o = axes(s, ax, [(k * 0.05, f"{k * 0.05:.2f}") for k in range(7)], [(v, str(v)) for v in (0, 5, 10, 15)],
             "landing displacement d (m)", "mean landing force (kN)")
    o.append(H.line(s, ax.x0, ax.Y(bw), ax.x1, ax.Y(bw), O["dim"], "ref", dash=H.DASH_REF))
    o.append(H.label(s, ax.X(0.12), ax.Y(bw) - 7, f"floor: mg = {bw:.2f} kN, the same at every d", "label2", I["secondary"]))
    o.append(curve(s, ax, ds, fs, RED))
    for d, txt in ((0.05, "stiff landing, d = 5 cm"), (0.20, "soft landing, d = 20 cm")):
        o.append(dot(s, ax.X(d), ax.Y(F(d)), O["flag"]))
        o.append(H.label(s, ax.X(d) + 14, ax.Y(F(d)) - 30, txt, "label2", I["primary"]))
        o.append(H.label(s, ax.X(d) + 14, ax.Y(F(d)) - 14, f"{F(d):.1f} kN ({F(d) / bw:.1f} BW)", "label2", I["primary"]))
    o += legend(s, 80, 28, [(RED, None, "F = mv²/2d + mg, drop h = 0.4 m (v = 2.8 m/s), m = 70 kg")])
    aria = ("Mean landing force against cushioning distance for a 70 kg body dropped from 0.4 m. The force falls as a "
            "hyperbola, 6.2 kN (9.0 body weights) at d = 5 cm and 2.1 kN (3.0 body weights) at d = 20 cm, towards a floor "
            "of mg = 0.69 kN shown as a dashed line.")
    hv = hover(ax, [ax.X(d) for d in ds], [ax.Y(f) for f in fs],
               [f"d = {100 * d:.1f} cm: mean force {f:.2f} kN ({f / bw:.1f} BW)" for d, f in zip(ds, fs)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #10: Capstone VI, fracture margin
def fig10():
    VB = (0, 0, 760, 410)
    s = H.Scale(VB[2], VB[3])
    g, h_f, m_eff, k_c, S0 = 9.81, 0.70, 35.0, 40e3, 7.0e3
    v = math.sqrt(2 * g * h_f)
    Fi = v * math.sqrt(m_eff * k_c)                                         # Model 7.1, N
    crit = math.sqrt(Fi / S0)
    assert round(v, 2) == 3.71 and round(Fi / 1e3, 1) == 4.4 and round(100 * crit, 1) == 79.1
    M = lambda r: S0 * r * r / Fi                                           # noqa: E731  fracture margin S/F
    rs = np.linspace(0.5, 1.0, 101)
    ms = [M(r) for r in rs]
    ax = Ax((80, 62, 730, 335), (0.5, 1.0), (0, 1.8))
    xc = ax.X(crit)
    o = [f'<rect x="{ax.x0}" y="{ax.top}" width="{xc - ax.x0:.2f}" height="{ax.y0 - ax.top}" fill="{O["force"]}" opacity="0.08"/>',
         f'<rect x="{xc:.2f}" y="{ax.top}" width="{ax.x1 - xc:.2f}" height="{ax.y0 - ax.top}" fill="{O["neural"]}" opacity="0.10"/>']
    o += axes(s, ax, [(0.5 + 0.1 * k, f"{0.5 + 0.1 * k:.1f}") for k in range(6)],
              [(0, "0"), (0.5, "0.5"), (1, "1"), (1.5, "1.5")], "bone density ρ/ρ₀ (fraction of young)", "fracture margin S/F")
    o.append(H.line(s, ax.x0, ax.Y(1), ax.x1, ax.Y(1), O["dim"], "ref", dash=H.DASH_REF))
    o.append(H.line(s, xc, ax.y0, xc, ax.top, O["flag"], "ref", dash=H.DASH_REF))
    o.append(curve(s, ax, rs, ms, RED))
    o.append(dot(s, xc, ax.Y(1), O["flag"]))
    o.append(H.label(s, xc, ax.top - 8, f"critical density {100 * crit:.0f}% of young (S/F = 1)", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.x0 + 8, ax.top + 20, "fracture: S/F < 1", "label2", I["primary"]))
    o.append(H.label(s, ax.x1 - 8, ax.Y(0.35), "safe: S/F > 1", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.x0 + 8, ax.Y(0.12), f"S = S{sub('0', s)}(ρ/ρ₀)², S{sub('0', s)} = 7.0 kN; F = {Fi / 1e3:.1f} kN", "label2", I["primary"]))
    o.append(H.label(s, ax.x0 + 8, ax.Y(1) - 7, "margin = 1", "label2", I["secondary"]))
    o += legend(s, 80, 30, [(RED, None, "S/F, femoral strength over fall impact")])
    aria = ("Fracture margin S over F against bone density as a fraction of young bone. Strength S = S0 times density "
            "squared with S0 = 7.0 kN; the fall impact is F = 4.4 kN. The curve rises from 0.40 at half the young density "
            "to 1.60 at the young density and crosses 1 at 79 percent. Below that density the same fall fractures the hip; "
            "above it the fall does not.")
    hv = hover(ax, [ax.X(r) for r in rs], [ax.Y(m) for m in ms],
               [f"ρ/ρ₀ = {r:.2f}: S = {S0 * r * r / 1e3:.2f} kN, margin S/F = {m:.2f}" for r, m in zip(rs, ms)])
    return svg(VB, aria, s, o, hv)


# ================================================================ block diagrams
def block(s, x, y, w, h, accent, title, lines, tag=None, title_px="label", line_px="label2", gap=19, pad=26):
    """A box with an accent bar, a title, centred text lines and an optional muted tag line at the foot."""
    o = [f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="6" fill="{BOX}" stroke="{I["rule"]}" stroke-width="1"/>',
         f'<rect x="{x:.2f}" y="{y:.2f}" width="5" height="{h:.2f}" rx="2" fill="{accent}"/>',
         H.label(s, x + w / 2 + 2, y + pad, title, title_px, I["primary"], "middle", 'font-weight="bold"')]
    for k, ln in enumerate(lines):
        o.append(H.label(s, x + w / 2 + 2, y + pad + 24 + k * gap, ln, line_px, I["secondary"], "middle"))
    if tag:
        o.append(tag(x + w / 2 + 2, y + h - 10))
    return o


def link(href, inner):
    return f'<a href="{href}">{inner}</a>'


# ---------------------------------------------------------------- svg #2: the capstone arc (Section 0)
def fig2():
    VB = (0, 0, 760, 210)
    s = H.Scale(VB[2], VB[3])
    p = "m17f2_"
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    muted = lambda t: (lambda x, y: H.label(s, x, y, t, "label2", I["muted"], "middle"))      # noqa: E731
    o += block(s, 8, 15, 190, 180, I["rule"], "the toolkit",
               ["forces, beams, muscle,", "joints, gait, control,", "reaching, tissue,", "measurement"], muted("Modules 1–16"))
    o.append(H.arrow(s, p, 202, 105, 262, 105, "dim", w="ref"))
    o += block(s, 266, 35, 200, 140, I["rule"], "the method",
               ["question → model", "→ equations → simulate", "→ validate → limits"], muted("Section 1"))
    o.append(H.arrow(s, p, 470, 105, 530, 105, "dim", w="ref"))
    qs = ["why standing sways", "the knee torque of a chair-rise", "the speed limit of walking", "the force of a landing",
          "whether a fall breaks a hip", "the grip a jar demands"]
    o += [f'<rect x="534" y="15" width="218" height="180" rx="6" fill="{BOX}" stroke="{I["rule"]}" stroke-width="1"/>',
          f'<rect x="534" y="15" width="5" height="180" rx="2" fill="{I["rule"]}"/>',
          H.label(s, 645, 41, "answered questions", "label", I["primary"], "middle", 'font-weight="bold"')]
    for k, q in enumerate(qs):
        o.append(H.label(s, 552, 71 + k * 22, "· " + q, "label2", I["secondary"]))
    aria = ("A three-stage diagram. Left, the toolkit of Modules 1 to 16: forces, beams, muscle, joints, gait, control, "
            "reaching, tissue, measurement. An arrow leads to the method of Section 1: question, model, equations, "
            "simulate, validate, limits. An arrow leads to the answered questions: why standing sways, the knee torque of "
            "a chair-rise, the speed limit of walking, the force of a landing, whether a fall breaks a hip, the grip a "
            "jar demands.")
    return svg(VB, aria, s, o)


# ---------------------------------------------------------------- svg #11: Capstone VII chain
def fig11():
    VB = (0, 0, 760, 312)
    s = H.Scale(VB[2], VB[3])
    p = "m17f11_"
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    M0, M3, M4 = "module00.html#macro", "module03.html#reaction", "module04.html"

    def a(href, txt):
        return f'<a class="secref" href="{href}">{txt}</a>'

    def ref(text):
        return lambda x, y: H.label(s, x, y, text, "label2", I["muted"], "middle")

    ym, h, y0 = 109, 116, 51                       # arrow row y, box height, box top; the tissue box is centred on ym
    arrow_lbl = lambda x, l1, l2: [H.label(s, x, ym - 29, l1, "label2", I["secondary"], "middle"),     # noqa: E731
                                   H.label(s, x, ym - 13, l2, "label2", I["secondary"], "middle")]
    o += block(s, 6, y0, 108, h, I["rule"], "molecule", ["GAG assay", f"m{sub('GAG', s)} (mg/mL)"],
               ref(a(M0, "Module 0 §7")))
    o.append(H.arrow(s, p, 118, ym, 183, ym, "dim", w="ref"))
    o += arrow_lbl(150, a(M0, "M0 §7"), a(M0, "Def. 7.3"))
    tx, tw_, ty, th = 187, 196, 14, 190
    o += [f'<rect x="{tx}" y="{ty}" width="{tw_}" height="{th}" rx="6" fill="{BOX}" stroke="{I["rule"]}" stroke-width="1"/>',
          f'<rect x="{tx}" y="{ty}" width="5" height="{th}" rx="2" fill="{I["rule"]}"/>',
          H.label(s, tx + tw_ / 2 + 2, ty + 26, "tissue", "label", I["primary"], "middle", 'font-weight="bold"')]
    for k, ln in enumerate((f"fixed charge c{sub('F', s)}", "Donnan π: 156 → 42 kPa", "contact peak:", "2.0 → 3.2 MPa (fixed R)")):
        o.append(H.label(s, tx + tw_ / 2 + 2, ty + 52 + k * 19, ln, "label2", I["secondary"], "middle"))
    o.append(H.label(s, tx + tw_ / 2 + 2, ty + 138, "healthy → OA (50% GAG lost)", "label2", I["secondary"], "middle"))
    o.append(H.label(s, tx + tw_ / 2 + 2, ty + 172,
                     f'Module 4 {a(M4 + "#donnan", "§2")}, {a(M4 + "#contact", "§6")}, {a(M4 + "#degeneration", "§8")}',
                     "label2", I["muted"], "middle"))
    o.append(H.arrow(s, p, 387, ym, 452, ym, "dim", w="ref"))
    o += arrow_lbl(420, f'M4 {a(M4 + "#contact", "§6")}/{a(M4 + "#degeneration", "§8")}', "(fixed R)")
    o += block(s, 456, y0, 142, h, I["rule"], "joint", ["reaction R", f"R = W{sub('s', s)}(1 + b/a{sub('ab', s)})"],
               ref(a(M3, "Module 3 §4")))
    o.append(H.arrow(s, p, 602, ym, 648, ym, "dim", w="ref"))
    o += arrow_lbl(625, a(M3, "M3 §4"), "(4.1)")
    o += block(s, 652, y0, 100, h, I["rule"], "body", ["lean", "cane", "gait"], ref(a(M3, "Module 3 §4.3")), gap=18)
    col = O["geometry"]
    o.append(f'<path d="M702,{y0 + h + 4} C702,268 285,268 285,{ty + th + 10}" fill="none" stroke="{col}" '
             f'stroke-width="{s(H.PX["geom"]):.2f}" marker-end="url(#{p}a_geometry)"/>')
    o.append(H.label(s, 500, 278, f'{a(M3, "M3 §4.3")} (lean, cane): a postural choice changes R,', "label2", I["primary"], "middle"))
    o.append(H.label(s, 500, 296, "which changes the contact pressure the tissue above must carry", "label2", I["primary"], "middle"))
    aria = ("A chain diagram of Capstone VII. A molecule box (GAG assay, mass of GAG in mg per mL, Module 0 section 7) feeds a "
            "tissue box (fixed charge, Donnan pressure 156 to 42 kPa, contact peak 2.0 to 3.2 MPa at fixed R, healthy to "
            "osteoarthritis with 50 percent GAG lost) which feeds a joint box (reaction R = Ws(1 + b/aab), Module 3 section 4) "
            "which feeds a body box (lean, cane, gait). A feedback arrow runs from the body box back to the tissue box: a "
            "postural choice changes R and so the contact pressure the tissue carries.")
    return svg(VB, aria, s, o)


# ================================================================ svg #13: a validated result (illustration)
def fig13():
    VB = (0, 0, 760, 360)
    s = H.Scale(VB[2], VB[3])
    # Illustrative, not data: a smooth hump through the heights of the old figure, a constant band, two points inside it.
    kx = np.array([0, 0.17, 0.34, 0.5, 0.66, 0.83, 1.0])
    ky = np.array([39, 64, 89, 99, 87, 59, 31]) / 99.0
    cf = np.polyfit(kx, ky, 4)
    xs = np.linspace(0, 1, 101)
    ys = np.polyval(cf, xs)
    half = 0.11
    ax = Ax((80, 50, 730, 280), (0, 1), (0, 1.4))
    o = axes(s, ax, [], [], "movement phase", "predicted quantity (relative units)", grid=False)
    up = [(ax.X(x), ax.Y(y + half)) for x, y in zip(xs, ys)]
    dn = [(ax.X(x), ax.Y(y - half)) for x, y in zip(xs, ys)]
    o.append(f'<polygon points="{" ".join(f"{a:.2f},{b:.2f}" for a, b in up + dn[::-1])}" fill="{BLUE}" opacity="0.18"/>')
    o.append(curve(s, ax, xs, ys, BLUE))
    data = [(0.34, float(np.polyval(cf, 0.34)) - 0.03), (0.68, float(np.polyval(cf, 0.68)) - 0.07)]
    for x, y in data:
        assert abs(y - np.polyval(cf, x)) < half
        o.append(dot(s, ax.X(x), ax.Y(y), RED))
    o.append(H.label(s, ax.X(0.10), ax.Y(1.28), "model prediction", "label2", I["primary"]))
    o.append(H.line(s, ax.X(0.10) + 40, ax.Y(1.28) + 6, ax.X(0.15), ax.Y(float(np.polyval(cf, 0.15))) - 10, BLUE, "leader"))
    o.append(H.label(s, ax.X(0.70), ax.Y(1.30), "uncertainty band", "label2", I["primary"]))
    o.append(H.line(s, ax.X(0.76), ax.Y(1.30) + 6, ax.X(0.80), ax.Y(float(np.polyval(cf, 0.80)) + half) - 2, BLUE, "leader"))
    o.append(H.label(s, ax.X(0.50), ax.Y(0.58), "independent data", "label2", I["primary"], "middle"))
    o.append(H.line(s, ax.X(0.43), ax.Y(0.58) - 14, ax.X(0.355), ax.Y(data[0][1]) + 8, RED, "leader"))
    o.append(H.line(s, ax.X(0.57), ax.Y(0.58) - 14, ax.X(0.665), ax.Y(data[1][1]) + 8, RED, "leader"))
    o += legend(s, 80, 28, [(BLUE, None, "model prediction"), (BLUE, None, "± uncertainty band", "band"),
                            (RED, None, "independent data", "dot")], gap=26)
    aria = ("Illustration, not data: a model prediction (blue curve) rises and falls over the movement phase inside a "
            "shaded uncertainty band, and two independent data points (red) fall inside the band. Agreement inside the band "
            "is validation.")
    hv = hover(ax, [ax.X(x) for x in xs], [[ax.Y(y), ax.Y(y - half), ax.Y(y + half)] for y in ys],
               [f"illustration, phase {x:.2f}: model {y:.2f} ± {half:.2f} (relative units)" for x, y in zip(xs, ys)])
    return svg(VB, aria, s, o, hv)


FIGS = {
    2: ("The course modules on the left feeding into a modeling metho", fig2),
    4: ("Capstone I quiet standing stable versus unstable delay", fig4),
    6: ("Capstone II knee torque during a sit-to-stand", fig6),
    7: ("Capstones III-IV walking M-shape and running single-hump gro", fig7),
    9: ("Capstone V. Peak landing force versus how far the landing is", fig9),
    10: ("Capstone VI hip-fracture risk: the fracture margin, femoral ", fig10),
    11: ("A chain diagram: a molecule box (GAG assay) feeds a tissue b", fig11),
    13: ("A model prediction shown as a curve inside a shaded uncertai", fig13),
}
